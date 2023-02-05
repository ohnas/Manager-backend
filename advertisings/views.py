from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from sites.models import Site
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
from datetime import datetime, timedelta

# Create your views here.


class Advertisings(APIView):

    permission_classes = [IsAuthenticated]

    def facebook_api(self, site, from_date, to_date):
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
            AdsInsights.Field.purchase_roas,  # 구매 roas- 일치확인완료
            AdsInsights.Field.website_ctr,  # CTR(링크 클릭률)-일치확인완료
            AdsInsights.Field.cost_per_unique_inline_link_click,  # CPC(링크 클릭당 비용)-일치확인완료
            AdsInsights.Field.actions,
            # 구매항목은 actions 항목 중 "action_type":"purchase"의 value 값
            # 랜딩 페이지 조회 항목은 actions 항목 중 "action_type":"landing_page_view"의 value 값
            # 링크 클릭 항목은 actions 항목 중 "action_type":"link_click" 의 value 값
            # 결제정보추가 항목은 actions 항목 중 "action_type":"add_payment_info" 의 value 값
            # 장바구니 항목은 actions 항목 중 "action_type":"add_to_cart" 의 value 값
            AdsInsights.Field.adset_name,  # 광고세트 이름
        ]

        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta
        site = Site.objects.get(pk=site)
        ad_account_id = site.ad_account_id
        advertisings_dict = {}
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
                advertisings_dict[insight["date_start"]] = {
                    insight.get("campaign_name", 0): {
                        "campaign_id": insight.get("campaign_id", 0),
                        "adset_name": insight.get("adset_name", 0),
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
                }
        return advertisings_dict

    def get(self, request):
        try:
            site = request.query_params["advertisingSite"]
            from_date = request.query_params["dateFrom"]
            to_date = request.query_params["dateTo"]
        except KeyError:
            raise NotFound
        retrieve_data = self.facebook_api(site, from_date, to_date)
        return Response(retrieve_data)
