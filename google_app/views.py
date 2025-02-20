


from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from .utils import *
import logging
from .config import * 
import os
from rest_framework.response import Response
from google_auth_oauthlib.flow import Flow
import json
import urllib.parse

GOOGLE_OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/webmasters.readonly',
    'https://www.googleapis.com/auth/analytics.readonly'
]
# Logger setup
logger = logging.getLogger(__name__)

def test_api(request):
    data = {"Message": f"{__name__}"}
    return JsonResponse(data)





from google_auth_oauthlib.flow import Flow
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import redirect
import os

GOOGLE_OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/webmasters.readonly',
    'https://www.googleapis.com/auth/analytics.readonly'
]


def initialize_flow():
    """Initialize OAuth 2.0 flow"""
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # ✅ Allow HTTP for OAuth calls

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv('GOOGLE_REDIRECT_URI')]
            }
        },
        scopes=GOOGLE_OAUTH_SCOPES
    )
    flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    return flow


class StartAuthAPIView(APIView):
    """Start OAuth flow"""

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        state_data = json.dumps({"user_id": user_id})
        encoded_state = urllib.parse.quote(state_data) 
        flow = initialize_flow()
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=encoded_state

        )
        # auth_url += f"&state={user_id}"  # Pass user_id as state
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)


from django.utils.timezone import now, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from .models import GoogleCredentials  # Your Django Model


class Oauth2callbackAPIView(APIView):
    """Handle OAuth callback and store credentials in database"""

    def get(self, request):
        state_param = request.GET.get('state')  # Extract state
        if not state_param:
            return Response({"error": "Missing state"}, status=400)
        try:
            # ✅ Decode state properly
            state_data = json.loads(urllib.parse.unquote(state_param))
            print(state_data)
            user_id = state_data.get("user_id")
        except Exception:
            return Response({"error": "Invalid state format"}, status=400)

        if not user_id:
            return Response({"error": "Invalid user_id"}, status=400)

        flow = initialize_flow()
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials

        # Store credentials in database
        google_creds, created = GoogleCredentials.objects.update_or_create(
            user_id=user_id,  # Storing by user_id instead of request.user
            defaults={
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'expiry': credentials.expiry or (now() + timedelta(hours=1))
            }
        )

        return Response({"message": "Credentials saved."}, status=status.HTTP_200_OK)


def get_valid_credentials(user_id):
    """Fetch valid credentials and refresh if expired"""
    try:
        google_creds = GoogleCredentials.objects.get(user_id=user_id)
        
        credentials = Credentials(
            token=google_creds.token,
            refresh_token=google_creds.refresh_token,
            token_uri=google_creds.token_uri,
            client_id=google_creds.client_id,
            client_secret=google_creds.client_secret,
            scopes=GOOGLE_OAUTH_SCOPES
        )

        # Refresh the token if expired
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

            # Update stored credentials
            google_creds.token = credentials.token
            google_creds.expiry = credentials.expiry
            google_creds.save()

        return credentials

    except GoogleCredentials.DoesNotExist:
        return None




class GA4DataAPIView(APIView):
    def get(self, request):
        try:
            # OAuth 2.0 authentication
            # creds = get_credentials()
            user_id = request.GET.get("user_id")
            creds = get_valid_credentials(user_id)
            

            # Extract data from GA4
            # data_sessions = extract_GA4_session_data(creds)
            # data_event = extract_GA4_event_data(creds)
            data_webpage = extract_GA4_webpage_data(creds)
            data_webpage.to_excel('out_ga4.xlsx')

            # Save to Predicta Database
            # insert_data_to_db(data_sessions,'Session') if not data_sessions.empty else logging.warning("No Session-data fetched from GA4.")
            # insert_data_to_db(data_event,'Event') if not data_event.empty else logging.warning("No Event-data fetched from GA4.")
            insert_data_to_db(data_webpage,'WebPage') if not data_webpage.empty else logging.warning("No Web-Page-data fetched from GA4.")


            # Refresh token if necessary
            check_and_refresh_token(creds)

            return JsonResponse({"message": "Data successfully collected and inserted into database."}, status=status.HTTP_200_OK)
        except Exception as e:
            # logger.error(f"Error fetching GA4 data: {str(e)}")
            return JsonResponse({"message": f"{str(e)}"}, status=status.HTTP_200_OK)




class GSCDataAPIView(APIView):
    def get(self, request):

        logging.info("Starting Data extraction process...")

        user_id = request.GET.get("user_id")
        creds = get_valid_credentials(user_id)
        # OAuth 2.0 authentication
        # creds = get_credentials()
        service = get_google_service(creds)

        try:        
            # Extract GSC data for littlecheeks.com
            data_gsc_webpage = extract_GSC_webpage_data(service, SITE_URL)

            # Save to Predicta Database
            # insert_data_to_db(data_gsc_webpage,'WebPage') if not data_gsc_webpage.empty else logging.warning("No GSC Web-Page-data fetched from GA4.")

            # Save to Excel file
            data_gsc_webpage.to_excel('GSC_Test_WebPage.xlsx',index=False)


            # Refresh token if necessary
            check_and_refresh_token(creds)

            return JsonResponse({"message": "Data successfully collected and saved."}, status=status.HTTP_200_OK)


        except Exception as e:
            logging.error(f"Error fetching GA4 data: {str(e)}")
            return JsonResponse({"message": f"{str(e)}"}, status=status.HTTP_200_OK)


