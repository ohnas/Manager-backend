from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from sales.models import Sale
from sales.serializers import SaleSerializer
from products.models import Product
from sites.models import Site
from datetime import datetime, timedelta
import requests
import time


class Sales(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        from_date = request.query_params["dateFrom"]
        to_date = request.query_params["dateTo"]
        order_date_from = from_date + " 00:00:00"
        order_date_from = datetime.strptime(order_date_from, "%Y-%m-%d %H:%M:%S")
        order_date_from = order_date_from + timedelta(hours=9)
        order_date_from = round(order_date_from.timestamp())
        order_date_to = to_date + " 23:59:59"
        order_date_to = datetime.strptime(order_date_to, "%Y-%m-%d %H:%M:%S")
        order_date_to = order_date_to + timedelta(hours=9)
        order_date_to = round(order_date_to.timestamp())
        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta
        KEY = ""
        SECREAT = ""
        access_token = requests.get(
            f"https://api.imweb.me/v2/auth?key={KEY}&secret={SECREAT}"
        )
        access_token = access_token.json()
        access_token = access_token["access_token"]
        headers = {"access-token": access_token, "version": "latest"}

        data = requests.get(
            f"https://api.imweb.me/v2/shop/orders?order_date_from={order_date_from}&order_date_to={order_date_to}",
            headers=headers,
        )
        data = data.json()
        data = data["data"]
        sales = data["list"]
        order_no_list = []
        for sale in sales:
            order_time = sale["order_time"]
            order_time = datetime.fromtimestamp(order_time)
            order_time = order_time - timedelta(hours=9)
            order_time = order_time.strftime("%Y-%m-%d")
            order = {"order_no": sale["order_no"], "order_time": order_time}
            order_no_list.append(order)
        pagenation = data["pagenation"]
        total_page = pagenation["total_page"]
        pages = []
        if total_page > 1:
            for page_no in range(total_page):
                pages.append(page_no + 1)
            pages.remove(1)
            for page in pages:
                time.sleep(1)
                data = requests.get(
                    f"https://api.imweb.me/v2/shop/orders?order_date_from={order_date_from}&order_date_to={order_date_to}&offset={page}",
                    headers=headers,
                )
                data = data.json()
                data = data["data"]
                sales = data["list"]
                for sale in sales:
                    order_time = sale["order_time"]
                    order_time = datetime.fromtimestamp(order_time)
                    order_time = order_time - timedelta(hours=9)
                    order_time = order_time.strftime("%Y-%m-%d")
                    order = {"order_no": sale["order_no"], "order_time": order_time}
                    order_no_list.append(order)

        order_list = []
        for order_no in order_no_list:
            time.sleep(0.5)
            data = requests.get(
                f"https://api.imweb.me/v2/shop/orders/{order_no['order_no']}/prod-orders",
                headers=headers,
            )
            data = data.json()
            data = data["data"]
            for d in data:
                pay_time = d["pay_time"]
                pay_time = datetime.fromtimestamp(pay_time)
                pay_time = pay_time - timedelta(hours=9)
                pay_time = pay_time.strftime("%Y-%m-%d")
                for item in d["items"]:
                    order = {
                        "order_no": order_no["order_no"],
                        "order_time": order_no["order_time"],
                        "status": d["status"],
                        "pay_time": pay_time,
                        "prod_name": item["prod_name"],
                        "payment": item["payment"],
                        "option": item["options"][0][0]["value_name_list"][0],
                        "count": item["options"][0][0]["payment"]["count"],
                    }
                    order_list.append(order)

        modified_order_list = []
        for order in order_list:
            if (
                order["status"] == "PAY_COMPLETE"
                or order["status"] == "STANDBY"
                or order["status"] == "DELIVERING"
                or order["status"] == "COMPLETE"
            ) and order["order_time"] == order["pay_time"]:
                modified_order_list.append(order)

        print(len(order_list))
        print(len(modified_order_list))

        return Response(modified_order_list)

    # def imweb_api(self, product, date, site):
    #     # 프론트에서 입력받은 날짜를 stamptime(imweb date 검색 조건)으로 변경해서 검색하기
    #     order_date_from = date + " 00:00:00"
    #     order_date_from = datetime.strptime(order_date_from, "%Y-%m-%d %H:%M:%S")
    #     order_date_from = order_date_from + timedelta(hours=9)
    #     order_date_from = round(order_date_from.timestamp())
    #     order_date_to = date + " 23:59:59"
    #     order_date_to = datetime.strptime(order_date_to, "%Y-%m-%d %H:%M:%S")
    #     order_date_to = order_date_to + timedelta(hours=9)
    #     order_date_to = round(order_date_to.timestamp())
    #     site = Site.objects.get(pk=site)
    #     KEY = site.api_key
    #     SECREAT = site.secret_key
    #     access_token = requests.get(
    #         f"https://api.imweb.me/v2/auth?key={KEY}&secret={SECREAT}"
    #     )
    #     access_token = access_token.json()
    #     access_token = access_token["access_token"]
    #     headers = {"access-token": access_token, "version": "latest"}
    #     sales = requests.get(
    #         f"https://api.imweb.me/v2/shop/orders?order_date_from={order_date_from}&order_date_to={order_date_to}",
    #         headers=headers,
    #     )
    #     sales = sales.json()
    #     sales = sales["data"]
    #     sales = sales["list"]
    #     sales_order_list = []
    #     for sale in sales:
    #         order_time = sale["order_time"]
    #         order_time = datetime.fromtimestamp(order_time)
    #         sale_order_list = {
    #             "order_no": sale["order_no"],
    #             "order_time": order_time,
    #         }
    #         sales_order_list.append(sale_order_list)
    #     prod_orders = []
    #     for order in sales_order_list:
    #         order_no = order["order_no"]
    #         order_time = order["order_time"]
    #         prod_order = requests.get(
    #             f"https://api.imweb.me/v2/shop/orders/{order_no}/prod-orders",
    #             headers=headers,
    #         )
    #         prod_order = prod_order.json()
    #         prod_order = prod_order["data"]
    #         for prod in prod_order:
    #             items = prod["items"]
    #             pay_time = prod["pay_time"]
    #             pay_time = datetime.fromtimestamp(pay_time)
    #             for item in items:
    #                 if product.name == item["prod_name"]:
    #                     prod_name = item["prod_name"]
    #                     payment = item["payment"]
    #                     if "count" in payment:
    #                         prod_count = payment["count"]
    #                     else:
    #                         for option in item["options"]:
    #                             option_item = option[0]
    #                             payment = option_item["payment"]
    #                             prod_count = payment["count"]
    #                     prod_price = payment["price"]
    #                     prod_deliv_price = payment["deliv_price"]
    #                     prod_order = {
    #                         "order_no": order_no,
    #                         "name": prod_name,
    #                         "count": prod_count,
    #                         "price": prod_price,
    #                         "delivery_price": prod_deliv_price,
    #                         "order_time": order_time,
    #                         "pay_time": pay_time,
    #                     }
    #                     prod_orders.append(prod_order)
    #     return prod_orders

    # def get(self, request):
    #     try:
    #         product = request.query_params["product"]
    #         site = request.query_params["site"]
    #         date = request.query_params["date"]
    #         product = Product.objects.get(pk=product)
    #         sales = Sale.objects.filter(product=product, order_time__date=date)
    #     except Product.DoesNotExist:
    #         raise NotFound
    #     # db에 저장되어 있는 데이터가 없을경우 imweb 데이터를 요청하고 해당데이터를 db에 저장한 후 response
    #     if sales.count() == 0:
    #         results = self.imweb_api(product, date, site)
    #         if results:
    #             with transaction.atomic():
    #                 for result in results:
    #                     product = Product.objects.get(name=result["name"])
    #                     sale = Sale(
    #                         product=product,
    #                         count=result["count"],
    #                         price=result["price"],
    #                         delivery_price=result["delivery_price"],
    #                         pay_time=result["pay_time"],
    #                         order_no=result["order_no"],
    #                         order_time=result["order_time"],
    #                     )
    #                     sale.save()
    #                 serializer = SaleSerializer(sales, many=True)
    #                 return Response(serializer.data)
    #         else:
    #             serializer = SaleSerializer(sales, many=True)
    #             return Response(serializer.data)
    #     else:
    #         serializer = SaleSerializer(sales, many=True)
    #         return Response(serializer.data)
