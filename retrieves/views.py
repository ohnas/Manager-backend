from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
from brands.models import Brand
from products.models import Product
from sites.models import Site
from datetime import datetime, timedelta
import requests
import time
import pandas as pd
import numpy as np


class Retrieves(APIView):

    permission_classes = [IsAuthenticated]

    def imweb_api(self, sale_site, from_date, to_date):
        order_date_from = from_date + " 00:00:00"
        order_date_from = datetime.strptime(order_date_from, "%Y-%m-%d %H:%M:%S")
        order_date_from = round(order_date_from.timestamp())
        order_date_to = to_date + " 23:59:59"
        order_date_to = datetime.strptime(order_date_to, "%Y-%m-%d %H:%M:%S")
        order_date_to = round(order_date_to.timestamp())
        site = Site.objects.get(pk=sale_site)
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
        if sales:
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
                        if "options" in item:
                            order = {
                                "imweb_order_no": order_no["order_no"],
                                "imweb_order_time": order_no["order_time"],
                                "imweb_status": d["status"],
                                "imweb_pay_time": pay_time,
                                "imweb_prod_name": item["prod_name"],
                                "imweb_price": item["payment"]["price"],
                                "imweb_deliv_price": item["payment"]["deliv_price"],
                                "imweb_island_price": item["payment"]["island_price"],
                                "imweb_price_sale": item["payment"]["price_sale"],
                                "imweb_point": float(item["payment"]["point"]),
                                "imweb_coupon": item["payment"]["coupon"],
                                "imweb_membership_discount": item["payment"][
                                    "membership_discount"
                                ],
                                "imweb_period_discount": item["payment"][
                                    "period_discount"
                                ],
                                "imweb_option": item["options"][0][0][
                                    "value_name_list"
                                ][0],
                                "imweb_count": item["options"][0][0]["payment"][
                                    "count"
                                ],
                            }
                        else:
                            order = {
                                "imweb_order_no": order_no["order_no"],
                                "imweb_order_time": order_no["order_time"],
                                "imweb_status": d["status"],
                                "imweb_pay_time": pay_time,
                                "imweb_prod_name": item["prod_name"],
                                "imweb_price": item["payment"]["price"],
                                "imweb_deliv_price": item["payment"]["deliv_price"],
                                "imweb_island_price": item["payment"]["island_price"],
                                "imweb_price_sale": item["payment"]["price_sale"],
                                "imweb_point": float(item["payment"]["point"]),
                                "imweb_coupon": item["payment"]["coupon"],
                                "imweb_membership_discount": item["payment"][
                                    "membership_discount"
                                ],
                                "imweb_period_discount": item["payment"][
                                    "period_discount"
                                ],
                                "imweb_option": "No option",
                                "imweb_count": item["payment"]["count"],
                            }
                        order_list.append(order)

            modified_order_list = []
            for order in order_list:
                if (
                    order["imweb_status"] == "PAY_COMPLETE"
                    or order["imweb_status"] == "STANDBY"
                    or order["imweb_status"] == "DELIVERING"
                    or order["imweb_status"] == "COMPLETE"
                ):
                    modified_order_list.append(order)
        else:
            modified_order_list = []

        return modified_order_list

    def facebook_api(self, advertising_site, date_list):
        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET
        access_token = settings.FACEBOOK_ACCESS_TOKEN
        FacebookAdsApi.init(access_token=access_token)
        insight_fields = [
            AdsInsights.Field.campaign_id,  # 캠페인 아이디
            AdsInsights.Field.campaign_name,  # 캠페인 이름
            AdsInsights.Field.reach,  # 도달수 - 일치확인완료
            AdsInsights.Field.impressions,  # 노출- 일치확인완료
            AdsInsights.Field.frequency,  # 빈도- 일치확인완료
            AdsInsights.Field.spend,  # 지출금액- 일치확인완료
            AdsInsights.Field.cpm,  # CPM(1,000회 노출당 비용)- 일치확인완료
            AdsInsights.Field.website_ctr,  # CTR(링크 클릭률)-일치확인완료
            AdsInsights.Field.purchase_roas,  # 구매 roas- 일치확인완료
            AdsInsights.Field.cost_per_unique_inline_link_click,  # CPC(링크 클릭당 비용)-일치확인완료
            AdsInsights.Field.actions,
            # 구매항목은 actions 항목 중 "action_type":"purchase"의 value 값
            # 랜딩 페이지 조회 항목은 actions 항목 중 "action_type":"landing_page_view"의 value 값
            # 링크 클릭 항목은 actions 항목 중 "action_type":"link_click" 의 value 값
            # 결제정보추가 항목은 actions 항목 중 "action_type":"add_payment_info" 의 value 값
            # 장바구니 항목은 actions 항목 중 "action_type":"add_to_cart" 의 value 값
            AdsInsights.Field.adset_name,  # 광고세트 이름
        ]
        site = Site.objects.get(pk=advertising_site)
        ad_account_id = site.ad_account_id
        advertisings_list = []
        for date in date_list:
            params = {
                "time_range": {"since": date, "until": date},
                "level": "adset",
            }
            insights = AdAccount(f"act_{ad_account_id}").get_insights(
                params=params,
                fields=insight_fields,
            )
            for insight in insights:
                if insight.get("website_ctr") is None:
                    website_ctr = 0
                else:
                    website_ctr = insight["website_ctr"][0]["value"]
                if insight.get("purchase_roas") is None:
                    purchase_roas = 0
                else:
                    purchase_roas = insight["purchase_roas"][0]["value"]
                actions = insight["actions"]
                purchase = 0
                landing_page_view = 0
                link_click = 0
                add_payment_info = 0
                add_to_cart = 0
                for action in actions:
                    if action["action_type"] == "purchase":
                        index_no = actions.index(action)
                        purchase = actions[index_no]["value"]
                    if action["action_type"] == "landing_page_view":
                        index_no = actions.index(action)
                        landing_page_view = actions[index_no]["value"]
                    if action["action_type"] == "link_click":
                        index_no = actions.index(action)
                        link_click = actions[index_no]["value"]
                    if action["action_type"] == "add_payment_info":
                        index_no = actions.index(action)
                        add_payment_info = actions[index_no]["value"]
                    if action["action_type"] == "add_to_cart":
                        index_no = actions.index(action)
                        add_to_cart = actions[index_no]["value"]
                    # dict 을 가져올때 get을 이용하자. 이유는 가져오려는 항목의 수치가 없을경우 facebook에서는 그 항목을 응답하지 않기 때문에
                    # get을 이용해서 항목의 value를 가져오고 없을경우 0을 defalut로 보여주자
                advertisings = {
                    "campaign_id": insight.get("campaign_id", 0),
                    "campaign_name": insight.get("campaign_name", 0),
                    "adset_name": insight.get("adset_name", 0),
                    "date": insight["date_start"],
                    "reach": int(insight.get("reach", 0)),
                    "impressions": int(insight.get("impressions", 0)),
                    "frequency": float(insight.get("frequency", 0)),
                    "spend": float(insight.get("spend", 0)),
                    "cpm": float(insight.get("cpm", 0)),
                    "website_ctr": float(website_ctr),
                    "purchase_roas": float(purchase_roas),
                    "cost_per_unique_inline_link_click": float(
                        insight.get("cost_per_unique_inline_link_click", 0)
                    ),
                    "purchase": int(purchase),
                    "landing_page_view": int(landing_page_view),
                    "link_click": int(link_click),
                    "add_payment_info": int(add_payment_info),
                    "add_to_cart": int(add_to_cart),
                }
                advertisings_list.append(advertisings)
        # if advertisings_list:
        #     df = pd.DataFrame.from_records(advertisings_list)
        #     campaigns_df = df[
        #         [
        #             "date",
        #             "campaign_name",
        #             "reach",
        #             "impressions",
        #             "frequency",
        #             "spend",
        #             "cpm",
        #             "website_ctr",
        #             "purchase_roas",
        #             "cost_per_unique_inline_link_click",
        #             "purchase",
        #             "landing_page_view",
        #             "link_click",
        #             "add_payment_info",
        #             "add_to_cart",
        #         ]
        #     ]
        #     brand = Brand.objects.get(pk=brand)
        #     products = brand.product_set.all()
        #     prod_list = []
        #     for product in products:
        #         prod_list.append(str(product))
        #     campaigns_dict = {}
        #     for product in prod_list:
        #         campaign_df = campaigns_df.loc[
        #             campaigns_df["campaign_name"].eq(product), :
        #         ]
        #         campaign_dict = (
        #             pd.DataFrame.pivot_table(
        #                 campaign_df,
        #                 index=["date", "campaign_name"],
        #                 values=[
        #                     "reach",
        #                     "impressions",
        #                     "frequency",
        #                     "spend",
        #                     "cpm",
        #                     "website_ctr",
        #                     "purchase_roas",
        #                     "cost_per_unique_inline_link_click",
        #                     "purchase",
        #                     "landing_page_view",
        #                     "link_click",
        #                     "add_payment_info",
        #                     "add_to_cart",
        #                 ],
        #                 aggfunc={
        #                     "reach": sum,
        #                     "impressions": sum,
        #                     "frequency": sum,
        #                     "spend": sum,
        #                     "cpm": sum,
        #                     "website_ctr": sum,
        #                     "purchase_roas": sum,
        #                     "cost_per_unique_inline_link_click": sum,
        #                     "purchase": sum,
        #                     "landing_page_view": sum,
        #                     "link_click": sum,
        #                     "add_payment_info": sum,
        #                     "add_to_cart": sum,
        #                 },
        #                 fill_value=0,
        #             )
        #             .reset_index(level="campaign_name")
        #             .to_dict(orient="index")
        #         )
        #         if campaign_dict:
        #             campaigns_dict[product] = campaign_dict

        #     by_date_df = df[
        #         [
        #             "date",
        #             "reach",
        #             "impressions",
        #             "frequency",
        #             "spend",
        #             "cpm",
        #             "website_ctr",
        #             "purchase_roas",
        #             "cost_per_unique_inline_link_click",
        #             "purchase",
        #             "landing_page_view",
        #             "link_click",
        #             "add_payment_info",
        #             "add_to_cart",
        #         ]
        #     ]
        #     by_date_dict = pd.DataFrame.pivot_table(
        #         by_date_df,
        #         index=["date"],
        #         values=[
        #             "reach",
        #             "impressions",
        #             "frequency",
        #             "spend",
        #             "cpm",
        #             "website_ctr",
        #             "purchase_roas",
        #             "cost_per_unique_inline_link_click",
        #             "purchase",
        #             "landing_page_view",
        #             "link_click",
        #             "add_payment_info",
        #             "add_to_cart",
        #         ],
        #         aggfunc={
        #             "reach": sum,
        #             "impressions": sum,
        #             "frequency": sum,
        #             "spend": sum,
        #             "cpm": sum,
        #             "website_ctr": sum,
        #             "purchase_roas": sum,
        #             "cost_per_unique_inline_link_click": sum,
        #             "purchase": sum,
        #             "landing_page_view": sum,
        #             "link_click": sum,
        #             "add_payment_info": sum,
        #             "add_to_cart": sum,
        #         },
        #         fill_value=0,
        #     ).to_dict(orient="index")
        #     exchange_rate = {}
        #     for date in date_list:
        #         exchange_rate_api = requests.get(
        #             f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/usd/krw.json"
        #         )
        #         exchange_rate_api = exchange_rate_api.json()
        #         exchange_rate[exchange_rate_api["date"]] = round(
        #             exchange_rate_api["krw"], 2
        #         )

        #     facebook_dict = {
        #         "by_date": by_date_dict,
        #         "campaigns": campaigns_dict,
        #         "adsets": advertisings_list,
        #         "exchange_rate": exchange_rate,
        #     }
        # else:
        #     facebook_dict = {
        #         "by_date": {},
        #         "campaigns": {},
        #         "adsets": {},
        #         "exchange_rate": {},
        #     }

        # return facebook_dict
        return advertisings_list

    def exchange_rate_api(self, date_list):
        exchange_rate_list = []
        for date in date_list:
            exchange_rate = requests.get(
                f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/usd/krw.json"
            )
            exchange_rate = exchange_rate.json()
            exchange_rate_list.append(
                {
                    "date": date,
                    "krw": round(exchange_rate["krw"], 2),
                }
            )
        return exchange_rate_list

    def get(self, request):
        try:
            brand = request.query_params["brandPk"]
            sale_site = request.query_params["saleSite"]
            advertising_site = request.query_params["advertisingSite"]
            from_date = request.query_params["dateFrom"]
            to_date = request.query_params["dateTo"]
        except KeyError:
            raise NotFound
        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta

        imweb_data = self.imweb_api(sale_site, from_date, to_date)
        facebook_data = self.facebook_api(advertising_site, date_list)
        exchange_rate_data = self.exchange_rate_api(date_list)

        if not imweb_data:
            imweb_total_df = pd.DataFrame(
                {
                    "date": date_list,
                    "imweb_price": 0,
                    "imweb_deliv_price": 0,
                    "imweb_island_price": 0,
                    "imweb_price_sale": 0,
                    "imweb_point": 0.0,
                    "imweb_coupon": 0,
                    "imweb_membership_discount": 0,
                    "imweb_period_discount": 0,
                    "imweb_count": 0,
                    "logistic_fee": 0,
                    "product_cost": 0,
                    "product_profit": 0,
                    "sale_expense": 0,
                }
            )
        else:
            brand = Brand.objects.get(pk=brand)
            products = brand.product_set.values(
                "id", "name", "cost", "logistic_fee", "quantity", "gift_quantity"
            )
            options = []
            for product in products:
                pk = product["id"]
                selected_product = Product.objects.get(pk=pk)
                option_query_set = selected_product.options_set.values(
                    "name", "logistic_fee", "quantity", "gift_quantity"
                )
                for option in option_query_set:
                    options.append(option)
            imweb_df = pd.DataFrame.from_records(imweb_data)
            products_df = pd.DataFrame.from_records(products)
            products_df = products_df.drop("id", axis=1).rename(
                columns={"name": "imweb_prod_name"}
            )
            options_df = pd.DataFrame.from_records(options)
            options_df = options_df.rename(columns={"name": "imweb_option"})

            imweb_df = imweb_df.merge(products_df, on="imweb_prod_name").drop(
                ["logistic_fee", "quantity", "gift_quantity"], axis=1
            )
            imweb_without_option_df = imweb_df[imweb_df["imweb_option"] == "No option"]
            imweb_with_option_df = imweb_df[imweb_df["imweb_option"] != "No option"]
            products_df = products_df.drop("cost", axis=1)
            imweb_product_merge_df = imweb_without_option_df.merge(
                products_df, on="imweb_prod_name"
            )
            imweb_option_merge_df = imweb_with_option_df.merge(
                options_df, on="imweb_option"
            )
            imweb_df = pd.concat([imweb_product_merge_df, imweb_option_merge_df])
            imweb_df["shipment_quantity"] = (
                imweb_df["imweb_count"] * imweb_df["quantity"]
            ) + (imweb_df["imweb_count"] * imweb_df["gift_quantity"])
            imweb_df["product_cost"] = imweb_df["cost"] * imweb_df["shipment_quantity"]
            imweb_df["product_profit"] = (
                imweb_df["imweb_price"]
                + imweb_df["imweb_deliv_price"]
                - imweb_df["product_cost"]
            )
            imweb_df["sale_expense"] = imweb_df["imweb_price"] * 0.033
            imweb_total_df = (
                imweb_df.groupby(by="imweb_order_time", as_index=False)
                .agg(
                    {
                        "imweb_price": "sum",
                        "imweb_deliv_price": "sum",
                        "imweb_island_price": "sum",
                        "imweb_price_sale": "sum",
                        "imweb_point": "sum",
                        "imweb_coupon": "sum",
                        "imweb_membership_discount": "sum",
                        "imweb_period_discount": "sum",
                        "imweb_count": "sum",
                        "logistic_fee": "sum",
                        "product_cost": "sum",
                        "product_profit": "sum",
                        "sale_expense": "sum",
                    }
                )
                .rename(columns={"imweb_order_time": "date"})
            )
            for d in date_list:
                if imweb_total_df[imweb_total_df["date"] == d].empty:
                    imweb_without_day_df = pd.DataFrame(
                        [
                            {
                                "date": d,
                                "imweb_price": 0,
                                "imweb_deliv_price": 0,
                                "imweb_island_price": 0,
                                "imweb_price_sale": 0,
                                "imweb_point": 0.0,
                                "imweb_coupon": 0,
                                "imweb_membership_discount": 0,
                                "imweb_period_discount": 0,
                                "imweb_count": 0,
                                "logistic_fee": 0,
                                "product_cost": 0,
                                "product_profit": 0,
                                "sale_expense": 0,
                            }
                        ]
                    )
                    imweb_total_df = pd.concat([imweb_total_df, imweb_without_day_df])
        if not facebook_data:
            facebook_total_df = pd.DataFrame(
                {
                    "date": date_list,
                    "reach": 0,
                    "impressions": 0,
                    "frequency": 0.0,
                    "spend": 0.0,
                    "cpm": 0.0,
                    "website_ctr": 0.0,
                    "purchase_roas": 0.0,
                    "cost_per_unique_inline_link_click": 0.0,
                    "purchase": 0,
                    "landing_page_view": 0,
                    "link_click": 0,
                    "add_payment_info": 0,
                    "add_to_cart": 0,
                    "conversion_rate": 0.0,
                }
            )
        else:
            facebook_df = pd.DataFrame.from_records(facebook_data)
            facebook_total_df = facebook_df.groupby(by="date", as_index=False).agg(
                {
                    "reach": "sum",
                    "impressions": "sum",
                    "frequency": "sum",
                    "spend": "sum",
                    "cpm": "sum",
                    "website_ctr": "sum",
                    "purchase_roas": "sum",
                    "cost_per_unique_inline_link_click": "sum",
                    "purchase": "sum",
                    "landing_page_view": "sum",
                    "link_click": "sum",
                    "add_payment_info": "sum",
                    "add_to_cart": "sum",
                }
            )
            facebook_total_df["conversion_rate"] = (
                facebook_total_df["purchase"] / facebook_total_df["landing_page_view"]
            ) * 100
            facebook_total_df["conversion_rate"] = facebook_total_df[
                "conversion_rate"
            ].fillna(0.0)
            for d in date_list:
                if facebook_total_df[facebook_total_df["date"] == d].empty:
                    facebook_without_day_df = pd.DataFrame(
                        [
                            {
                                "date": d,
                                "reach": 0,
                                "impressions": 0,
                                "frequency": 0.0,
                                "spend": 0.0,
                                "cpm": 0.0,
                                "website_ctr": 0.0,
                                "purchase_roas": 0.0,
                                "cost_per_unique_inline_link_click": 0.0,
                                "purchase": 0,
                                "landing_page_view": 0,
                                "link_click": 0,
                                "add_payment_info": 0,
                                "add_to_cart": 0,
                                "conversion_rate": 0.0,
                            }
                        ]
                    )
                    facebook_total_df = pd.concat(
                        [facebook_total_df, facebook_without_day_df]
                    )
        exchange_rate_df = pd.DataFrame.from_records(exchange_rate_data)
        facebook_total_df = facebook_total_df.merge(
            exchange_rate_df,
            on="date",
        )
        facebook_total_df["facebook_ad_expense_krw"] = (
            facebook_total_df["spend"] * facebook_total_df["krw"]
        )

        total_df = imweb_total_df.merge(facebook_total_df, on="date")
        total_df["expense"] = (
            total_df["logistic_fee"]
            + total_df["sale_expense"]
            + total_df["facebook_ad_expense_krw"]
            + total_df["imweb_price_sale"]
            + total_df["imweb_point"]
            + total_df["imweb_coupon"]
            + total_df["imweb_membership_discount"]
            + total_df["imweb_period_discount"]
        )
        total_df["operating_profit"] = total_df["product_profit"] - total_df["expense"]
        total_df["operating_profit_rate"] = (
            total_df["operating_profit"] / total_df["imweb_price"]
        ) * 100
        total_df["operating_profit_rate"] = (
            total_df["operating_profit_rate"]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0.0)
        )
        total_df["product_cost_rate"] = (
            total_df["product_cost"] / total_df["imweb_price"]
        ) * 100
        total_df["product_cost_rate"] = (
            total_df["product_cost_rate"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
        )
        total_df["facebook_ad_expense_krw_rate"] = (
            total_df["facebook_ad_expense_krw"] / total_df["imweb_price"]
        ) * 100
        total_df["facebook_ad_expense_krw_rate"] = (
            total_df["facebook_ad_expense_krw_rate"]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0.0)
        )
        total_df = total_df.set_index("date")
        total = total_df.to_dict("index")
        return Response(total)
