from django.db import transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from datetime import datetime, timedelta
from dateutil import relativedelta
from brands.serializers import BrandSerializer, BrandDetailSerializer
from brands.models import Brand, BrandData
from users.serializers import UserSerializer
from users.models import User


class Brands(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = BrandSerializer(all_brands, many=True)
        return Response(serializer.data)


class MyBrand(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brands = Brand.objects.filter(user=request.user.pk)
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandDetailSerializer(brand)
        return Response(serializer.data)


class CreateBrand(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        user = request.data.get("user")
        if not name or not user:
            raise ParseError
        user = User.objects.get(pk=user)
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                brand = serializer.save(user=user)
                serializer = BrandSerializer(brand)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UpdateBrand(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    def put(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        user = request.data.get("user")
        if user is None:
            if serializer.is_valid():
                with transaction.atomic():
                    brand = serializer.save()
                    serializer = BrandSerializer(brand)
                    return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            user = User.objects.get(pk=user)
            if serializer.is_valid():
                with transaction.atomic():
                    brand = serializer.save(user=user)
                    serializer = BrandSerializer(brand)
                    return Response(serializer.data)
            else:
                return Response(serializer.errors)

    def delete(self, request, pk):
        brand = self.get_object(pk)
        brand.delete()
        return Response(status=status.HTTP_200_OK)


class MonthlyBrandData(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        brand = self.get_object(pk)
        from_month = request.query_params["monthFrom"]
        to_month = request.query_params["monthTo"]
        selected_month_from = datetime.strptime(from_month, "%Y-%m")
        selected_month_to = datetime.strptime(to_month, "%Y-%m")
        selected_year_from = selected_month_from.year
        selected_month_from = selected_month_from.month
        selected_month_to = selected_month_to.month
        data = {}
        month_list = []
        while selected_month_from <= selected_month_to:
            month_list.append(f"{selected_year_from}-{selected_month_from}")
            selected_month_from += 1
        for item in month_list:
            year_month = item.split("-")
            year = year_month[0]
            month = year_month[1]
            if not BrandData.objects.filter(
                brand=brand, date__year=year, date__month=month
            ).exists():
                data[item] = f"{item}의 저장된 데이터가 없습니다"
            else:
                current_month = datetime.strptime(item, "%Y-%m")
                yesterday = datetime.today() - timedelta(days=1)
                if (
                    current_month.year == yesterday.year
                    and current_month.month == yesterday.month
                ):
                    current_month_last_day = yesterday.date()
                else:
                    current_next_month = current_month + relativedelta.relativedelta(
                        months=1
                    )
                    current_month_last_day = current_next_month - timedelta(days=1)
                    current_month_last_day = current_month_last_day.date()

                current_month_first_day = current_month.date()
                delta = timedelta(days=1)
                current_month_day_list = []
                while current_month_first_day <= current_month_last_day:
                    current_month_day_list.append(
                        current_month_first_day.strftime("%Y-%m-%d")
                    )
                    current_month_first_day += delta
                missing_day_list = []
                for day in current_month_day_list:
                    if not BrandData.objects.filter(brand=brand, date=day).exists():
                        missing_day_list.append(day)

                brand_month_data = BrandData.objects.filter(
                    brand=brand, date__year=year, date__month=month
                ).aggregate(
                    sum_imweb_price=Sum("imweb_price"),
                    sum_imweb_deliv_price=Sum("imweb_deliv_price"),
                    sum_product_cost=Sum("product_cost"),
                    sum_product_profit=Sum("product_profit"),
                    sum_facebook_ad_expense_krw=Sum("facebook_ad_expense_krw"),
                    sum_expense=Sum("expense"),
                    sum_operating_profit=Sum("operating_profit"),
                    sum_imweb_nomal_order_counter=Sum("imweb_nomal_order_counter"),
                    sum_imweb_npay_order_counter=Sum("imweb_npay_order_counter"),
                    sum_imweb_count=Sum("imweb_count"),
                )
                brand_month_data["sum_price"] = (
                    brand_month_data["sum_imweb_price"]
                    + brand_month_data["sum_imweb_deliv_price"]
                )
                brand_month_data["total_operating_profit_rate"] = (
                    brand_month_data["sum_operating_profit"]
                    / brand_month_data["sum_imweb_price"]
                ) * 100
                brand_month_data["total_product_cost_rate"] = (
                    brand_month_data["sum_product_cost"]
                    / brand_month_data["sum_imweb_price"]
                ) * 100
                brand_month_data["total_facebook_ad_expense_krw_rate"] = (
                    brand_month_data["sum_facebook_ad_expense_krw"]
                    / brand_month_data["sum_imweb_price"]
                ) * 100
                brand_month_data["total_roas"] = (
                    brand_month_data["sum_imweb_price"]
                    / brand_month_data["sum_facebook_ad_expense_krw"]
                ) * 100
                data[item] = {
                    "missing_day_list": missing_day_list,
                    "brand_month_data": brand_month_data,
                }

        return Response(data)
