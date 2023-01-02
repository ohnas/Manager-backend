from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from sales.models import Sale
from sales.serializers import SaleSerializer
from products.models import Product
from datetime import datetime
import time
import requests


class Sales(APIView):

    permission_classes = [IsAuthenticated]

    def imweb_api(self, date):
        # 프론트에서 입력받은 날짜를 stamptime으로 변경해서 검색하기
        order_date_from = date + " 00:00:00"
        order_date_from = time.mktime(
            datetime.strptime(order_date_from, "%Y-%m-%d %H:%M:%S").timetuple()
        )
        order_date_to = date + " 23:59:59"
        order_date_to = time.mktime(
            datetime.strptime(order_date_to, "%Y-%m-%d %H:%M:%S").timetuple()
        )
        KEY = settings.NPR_API_KEY
        SECREAT = settings.NPR_SECRET_KEY
        access_token = requests.get(
            f"https://api.imweb.me/v2/auth?key={KEY}&secret={SECREAT}"
        )
        access_token = access_token.json()
        access_token = access_token["access_token"]
        headers = {"access-token": access_token, "version": "latest"}
        sales = requests.get(
            f"https://api.imweb.me/v2/shop/orders?order_date_from={order_date_from}&order_date_to={order_date_to}",
            headers=headers,
        )
        sales = sales.json()
        sales = sales["data"]
        sales = sales["list"]
        sales_order_no_list = []
        for sale in sales:
            sales_order_no_list.append(sale["order_no"])
        prod_orders = []
        for order_no in sales_order_no_list:
            prod_order = requests.get(
                f"https://api.imweb.me/v2/shop/orders/{order_no}/prod-orders",
                headers=headers,
            )
            prod_order = prod_order.json()
            prod_order = prod_order["data"]
            for prod in prod_order:
                items = prod["items"]
                pay_time = prod["pay_time"]
                pay_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(pay_time))
                for item in items:
                    prod_name = item["prod_name"]
                    payment = item["payment"]
                    prod_count = payment["count"]
                    prod_price = payment["price"]
                    prod_deliv_price = payment["deliv_price"]
                    prod_order = {
                        "name": prod_name,
                        "count": prod_count,
                        "price": prod_price,
                        "delivery_price": prod_deliv_price,
                        "pay_time": pay_time,
                    }
                    prod_orders.append(prod_order)
        return prod_orders

    def get(self, request):
        try:
            product_name = request.query_params["product"]
            date = request.query_params["date"]
            product = Product.objects.get(name=product_name)
            sales = Sale.objects.filter(product=product.pk, pay_time__date=date)
        except Product.DoesNotExist:
            raise NotFound
        # db에 저장되어 있는 데이터가 없을경우 imweb 데이터를 요청하고 해당데이터를 db에 저장한 후 response
        if sales.count() == 0:
            results = self.imweb_api(date)
            with transaction.atomic():
                for result in results:
                    product = Product.objects.get(name=result["name"])
                    sale = Sale(
                        product=product,
                        count=result["count"],
                        price=result["price"],
                        delivery_price=result["delivery_price"],
                        pay_time=result["pay_time"],
                    )
                    sale.save()
                serializer = SaleSerializer(sales, many=True)
                return Response(serializer.data)
        else:
            serializer = SaleSerializer(sales, many=True)
            return Response(serializer.data)
