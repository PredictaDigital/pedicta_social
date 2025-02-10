


from rest_framework.views import APIView
from rest_framework import status
from .models import GA4Session, GA4Event, GA4WebPage
from django.http import JsonResponse
from .utils import *
import logging
from .config import * 

# Logger setup
logger = logging.getLogger(__name__)

def test_api(request):
    data = {"Message": f"{__name__}"}
    return JsonResponse(data)

class GA4DataAPIView(APIView):
    def get(self, request):
        try:
            # Select a user from the all OAuth2.0 existed users
            # user_path_oauth = select_user_oauth() 
            user_path_oauth = USET_PATH_OAUTH

            # OAuth 2.0 authentication
            creds = get_credentials(user_path_oauth)

            # Extract data from GA4
            data_sessions = extract_GA4_session_data(creds)
            data_event = extract_GA4_event_data(creds)
            data_webpage = extract_GA4_webpage_data(creds)

            # Save to Predicta Database
            insert_data_to_db(data_sessions,'Session') if not data_sessions.empty else logging.warning("No Session-data fetched from GA4.")
            insert_data_to_db(data_event,'Event') if not data_event.empty else logging.warning("No Event-data fetched from GA4.")
            insert_data_to_db(data_webpage,'WebPage') if not data_webpage.empty else logging.warning("No Web-Page-data fetched from GA4.")



            # Refresh token if necessary
            check_and_refresh_token(creds)

            return JsonResponse({"message": "Data successfully collected and saved."}, status=status.HTTP_200_OK)
        except Exception as e:
            # logger.error(f"Error fetching GA4 data: {str(e)}")
            return JsonResponse({"message": f"{str(e)}"}, status=status.HTTP_200_OK)



