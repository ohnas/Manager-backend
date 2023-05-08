from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from brands.models import Brand
from sites.models import Site
from products.serializers import TinyBrandSerializer
from sites.serializers import SiteSerializer


class Sites(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        all_site = Site.objects.all()
        serializer = SiteSerializer(all_site, many=True)
        return Response(serializer.data)


class CreateSite(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = TinyBrandSerializer(all_brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        brand = request.data.get("brand")
        api_key = request.data.get("apiKey")
        secret_key = request.data.get("secretKey")
        ad_account_id = request.data.get("adAccountId")
        kind = request.data.get("kind")
        if not name or not brand or not kind:
            raise ParseError
        brand = Brand.objects.get(pk=brand)
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                site = serializer.save(
                    brand=brand,
                    api_key=api_key,
                    secret_key=secret_key,
                    ad_account_id=ad_account_id,
                )
                serializer = SiteSerializer(site)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UpdateSite(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Site.objects.get(pk=pk)
        except Site.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        site = self.get_object(pk)
        serializer = SiteSerializer(site)
        return Response(serializer.data)

    def put(self, request, pk):
        site = self.get_object(pk)
        serializer = SiteSerializer(site, data=request.data, partial=True)
        brand = request.data.get("brand")
        if brand is None:
            if serializer.is_valid():
                with transaction.atomic():
                    site = serializer.save()
                    serializer = SiteSerializer(site)
                    return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            brand = Brand.objects.get(pk=brand)
            if serializer.is_valid():
                with transaction.atomic():
                    site = serializer.save(brand=brand)
                    serializer = SiteSerializer(site)
                    return Response(serializer.data)
            else:
                return Response(serializer.errors)

    def delete(self, request, pk):
        site = self.get_object(pk)
        site.delete()
        return Response(status=status.HTTP_200_OK)
