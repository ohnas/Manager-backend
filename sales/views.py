from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from sites.models import Site
from datetime import datetime
import requests
import time
import pandas as pd


class Sales(APIView):

    permission_classes = [IsAuthenticated]

    def imweb_api(self, site, from_date, to_date):
        order_date_from = from_date + " 00:00:00"
        order_date_from = datetime.strptime(order_date_from, "%Y-%m-%d %H:%M:%S")
        order_date_from = round(order_date_from.timestamp())
        order_date_to = to_date + " 23:59:59"
        order_date_to = datetime.strptime(order_date_to, "%Y-%m-%d %H:%M:%S")
        order_date_to = round(order_date_to.timestamp())
        site = Site.objects.get(pk=site)
        KEY = site.api_key
        SECREAT = site.secret_key
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
                pay_time = pay_time.strftime("%Y-%m-%d")
                for item in d["items"]:
                    order = {
                        "order_no": order_no["order_no"],
                        "order_time": order_no["order_time"],
                        "status": d["status"],
                        "pay_time": pay_time,
                        "prod_name": item["prod_name"],
                        "prod_count": 1,
                        "price": item["payment"]["price"],
                        "deliv_price": item["payment"]["deliv_price"],
                        "island_price": item["payment"]["island_price"],
                        "price_sale": item["payment"]["price_sale"],
                        "point": float(item["payment"]["point"]),
                        "coupon": item["payment"]["coupon"],
                        "membership_discount": item["payment"]["membership_discount"],
                        "period_discount": item["payment"]["period_discount"],
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
            ):
                modified_order_list.append(order)

        df = pd.DataFrame.from_records(modified_order_list)
        prod_df = df[["order_time", "prod_name", "prod_count"]]
        prod_df = pd.DataFrame.pivot_table(
            prod_df,
            values="prod_count",
            index=["order_time"],
            columns=["prod_name"],
            aggfunc=sum,
            fill_value=0,
        )
        prod_dict = prod_df.to_dict(orient="index")

        option_df = df[
            [
                "order_time",
                "option",
                "count",
            ]
        ]
        option_df = pd.DataFrame.pivot_table(
            option_df,
            values="count",
            index=["order_time"],
            columns=["option"],
            aggfunc=sum,
            fill_value=0,
        )
        option_dict = option_df.to_dict(orient="index")

        payment_df = df[
            [
                "order_time",
                "price",
                "deliv_price",
                "island_price",
                "price_sale",
                "point",
                "coupon",
                "membership_discount",
                "period_discount",
            ]
        ]
        payment_df = pd.DataFrame.pivot_table(
            payment_df,
            index=["order_time"],
            values=[
                "price",
                "deliv_price",
                "island_price",
                "price_sale",
                "point",
                "coupon",
                "membership_discount",
                "period_discount",
            ],
            aggfunc={
                "price": sum,
                "deliv_price": sum,
                "island_price": sum,
                "price_sale": sum,
                "point": sum,
                "coupon": sum,
                "membership_discount": sum,
                "period_discount": sum,
            },
            fill_value=0,
        )
        payment_dict = payment_df.to_dict(orient="index")

        order_dict = {
            "product": prod_dict,
            "option": option_dict,
            "payment": payment_dict,
        }

        return order_dict

    def get(self, request):
        try:
            site = request.query_params["saleSite"]
            from_date = request.query_params["dateFrom"]
            to_date = request.query_params["dateTo"]
        except KeyError:
            raise NotFound
        retrieve_data = self.imweb_api(site, from_date, to_date)
        return Response(retrieve_data)
