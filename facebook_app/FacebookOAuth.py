from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import FB_Oauth
from datetime import timedelta
import requests
import os
from urllib.parse import urlencode


class FacebookOAuth(APIView):
    def get(self, request):
        # Facebook App credentials
        # Get email from the query parameters
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Set the email in a cookie for future use
        response = Response({"message": "Redirecting to Facebook OAuth"})
        redirect_uri = os.getenv('FB_REDIRECT_URL')  # Adjust to your callback URL
        scope = "email,pages_show_list,pages_manage_metadata,ads_management,ads_read,business_management,instagram_basic"  # Include Instagram and Business permissions
        # Create the authorization URL for Facebook OAuth
        state_data = {"email": email}
        state_encoded = urlencode(state_data)
        auth_url = "https://www.facebook.com/v22.0/dialog/oauth?" + urlencode({
            "response_type": "code",
            "client_id": os.getenv('FB_CLIENT_ID'),
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state_encoded  # Send email in state
        })
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)

class GetLatestTokenView(APIView):
    def get(self, request):
        email = request.query_params.get('email')  # Extract email from query parameters
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        fb_oauth = FB_Oauth.get_latest_token_by_email(email)
        if not fb_oauth:
            return Response({"error": "No token found for the given email"}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the response with the latest token details
        return Response({
            "access_token": fb_oauth.access_token,
            "page_id": fb_oauth.page_id,
            "instagram_account": fb_oauth.instagram_account,
            "business_profiles": fb_oauth.business_profiles,
            "ad_accounts": fb_oauth.ad_accounts,
            "email": fb_oauth.email,
        }, status=status.HTTP_200_OK)
