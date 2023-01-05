from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from advertisings.models import Advertising
from advertisings.serializers import AdvertisingSerializer
from sites.models import Site
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi

# Create your views here.


class Advertisings(APIView):

    permission_classes = [IsAuthenticated]

    def facebook_api(self, date, site):
        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET
        access_token = settings.FACEBOOK_ACCESS_TOKEN
        FacebookAdsApi.init(access_token=access_token)
        insight_fields = [
            AdsInsights.Field.campaign_id,  # 캠페인 아이디
            AdsInsights.Field.campaign_name,  # 캠페인 이름
            AdsInsights.Field.reach,  # 도달수 - 일치확인완료
            AdsInsights.Field.impressions,  # 노출- 일치확인완료
            # 게제 - 보류
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
        ]

        params = {
            "time_range": {"since": date, "until": date},
            "level": "campaign",
        }
        ad_account_id = site.ad_account_id
        insights = AdAccount(f"act_{ad_account_id}").get_insights(
            params=params,
            fields=insight_fields,
        )
        results = []
        for insight in insights:
            website_ctr = insight["website_ctr"][0]
            actions = insight["actions"]
            purchase = 0
            landing_page_view = 0
            link_click = 0
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
            # dict 을 가져올때 get을 이용하자. 이유는 가져오려는 항목의 수치가 없을경우 facebook에서는 그 항목을 응답하지 않기 때문에
            # get을 이용해서 항목의 value를 가져오고 없을경우 0을 defalut로 보여주자
            result = {
                "campaign_id": insight.get("campaign_id", 0),
                "campaign_name": insight.get("campaign_name", 0),
                "reach": insight.get("reach", 0),
                "impressions": insight.get("impressions", 0),
                "spend": insight.get("spend", 0),
                "cpm": insight.get("cpm", 0),
                "purchase_roas": insight.get("purchase_roas", 0),
                "website_ctr": website_ctr.get("value", 0),
                "cost_per_unique_inline_link_click": insight.get(
                    "cost_per_unique_inline_link_click", 0
                ),
                "cost_per_unique_inline_link_click": insight.get(
                    "cost_per_unique_inline_link_click", 0
                ),
                "purchase": purchase,
                "landing_page_view": landing_page_view,
                "link_click": link_click,
            }
            results.append(result)
        return results

    def get(self, request):
        try:
            site = request.query_params["site"]
            site = Site.objects.get(pk=site)
            date = request.query_params["date"]
            advertisings = Advertising.objects.filter(site=site, ad_date=date)
        except Site.DoesNotExist:
            raise NotFound
        if advertisings.count() == 0:
            results = self.facebook_api(date, site)
            if results:
                print(results)
            else:
                serializer = AdvertisingSerializer(advertisings, many=True)
                return Response(serializer.data)
        else:
            serializer = AdvertisingSerializer(advertisings, many=True)
            return Response(serializer.data)
