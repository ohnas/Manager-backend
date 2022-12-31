from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from brands.serializers import BrandSerializer
from brands.models import Brand


class Brands(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        brands = Brand.objects.filter(user=request.user.pk)
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
