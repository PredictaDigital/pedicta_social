from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .FB_Ads_Insights import FetchAdInsightsView
from .FB_ads_insights_by_age_gender import FetchAdInsightsViewbyAgeGender
from .FB_Ads_insights_by_device import FetchAdInsightsByDeviceView
from .FB_Ads_insights_by_location import FetchAdInsightsBylocation
from .FB_Campaign_Insights import FetchAdInsightsByCampaigns
from .FB_Followers_Statistics import FetchFollowersStatistics
from .FB_Followers_by_City import FetchFollowersCity
from .FB_Insights import FetchFBPageInsigths
from django.http import HttpRequest

class FacebookAPIHandler(APIView):
    def get(self, request):
        """Call all APIs and return a combined response, passing email and code."""
        
        email = request.query_params.get('email', None)
        if not email:
            return Response({"error": "Missing email or code in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

        responses = {}
        try:
            # Create a new HttpRequest instance from the DRF Request object
            django_request = HttpRequest()
            django_request.META = request.META
            django_request.method = 'GET'
            django_request.GET = request.query_params
            responses["ads_insights"] = FetchAdInsightsView.as_view()(django_request).data
            responses["ads_insights_age_gender"] = FetchAdInsightsViewbyAgeGender.as_view()(django_request).data
            responses["ads_insights_device"] = FetchAdInsightsByDeviceView.as_view()(django_request).data
            responses["ads_insights_location"] = FetchAdInsightsBylocation.as_view()(django_request).data
            responses["campaign_insights"] = FetchAdInsightsByCampaigns.as_view()(django_request).data
            responses["get_followers"] = FetchFollowersStatistics.as_view()(django_request).data
            responses["get_followers_city"] = FetchFollowersCity.as_view()(django_request).data
            responses["get_page_insights"] = FetchFBPageInsigths.as_view()(django_request).data
            return Response(responses, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
