from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from brands.models import Brand
from brands.serializers import BrandSerializer
from sites.serializers import SiteSerializer


class CreateSite(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = BrandSerializer(all_brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        url = request.data.get("url")
        brand = request.data.get("brand")
        api_key = request.data.get("apiKey")
        secret_key = request.data.get("secretKey")
        ad_account_id = request.data.get("adAccountId")
        kind = request.data.get("kind")
        if not name or not url or not brand:
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
                    kind=kind,
                )
                serializer = SiteSerializer(site)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)
