from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import requests

# Create your views here.


def sale_retrieve(request):
    # KEY = settings.NPR_API_KEY
    # SECREAT = settings.NPR_SECRET_KEY
    # access_token = requests.get(
    #     f"https://api.imweb.me/v2/auth?key={KEY}&secret={SECREAT}"
    # )
    # access_token = access_token.json()
    # access_token = access_token["access_token"]
    headers = {"access-token": "d7144a45432192b5f4e9dbd7437798e8", "version": "latest"}
    sales = requests.get("https://api.imweb.me/v2/shop/orders", headers=headers)
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
                    "deliv_price": prod_deliv_price,
                }
                prod_orders.append(prod_order)
    print(prod_orders)
    return HttpResponse(prod_orders)
