# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helpers import *
from rest_framework import generics
from .models import LinkedinAuth
from .serializers import LinkedinAuthSerializer
from social_auth.models import SocialUser
from dotenv import load_dotenv
import os
import requests
import urllib.parse

# Load environment variables from .env file
load_dotenv()
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
LINKEDIN_AUTH_URL = os.getenv("LINKEDIN_AUTH_URL")
LINKEDIN_TOKEN_URL = os.getenv("LINKEDIN_TOKEN_URL")

class LinkedinAPIView(APIView):
    def get(self, request, format=None):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            auth_instance = LinkedinAuth.objects.filter(social_user__email=email).first()
            if not auth_instance or not auth_instance.access_token:
                return Response({"error": "No LinkedIn access token found for this email"}, status=status.HTTP_404_NOT_FOUND)
            access_token = auth_instance.access_token
            
            print("Country_data")
           
            fetch_and_insert_linkedin_country_data(access_token)
            print("Country Group Data")
            fetch_and_insert_linkedin_country_group_data(access_token)
            print("Followers Data")
            fetch_and_insert_linkedin_followers_data(access_token)
            print("linkedin_followers_gain_data")
            fetch_and_insert_linkedin_followers_gain_data(access_token)
            print("_linkedin_functions_data")
            fetch_and_insert_linkedin_functions_data(access_token)
            print("linkedin_industries_data")
            fetch_and_insert_linkedin_industries_data(access_token)
            print("_linkedin_regions_data")
            fetch_and_insert_linkedin_regions_data(access_token)
            print("linkedin_seniorities_data")
            fetch_and_insert_linkedin_seniorities_data(access_token)
            print("insert_linkedin_location_data")
            fetch_and_insert_linkedin_location_data(access_token)
            print("insert_linkedin_posts_statistics")
            fetch_and_insert_linkedin_posts_statistics(access_token)
            print("linkedin_followers_gain_data_separate")
            fetch_and_insert_linkedin_followers_gain_data_separate(access_token)
            return Response({"message": "Data fetched and inserted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LinkedinAuthCreateView(generics.CreateAPIView):
    queryset = SocialUser.objects.all()
    serializer_class = LinkedinAuthSerializer


class LinkedinLoginView(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not SocialUser.objects.filter(email=email).exists():
            return Response({"error": "Email not exist in database"}, status=status.HTTP_400_BAD_REQUEST)

        encoded_email = urllib.parse.quote(email)

        auth_url = (
            f"{LINKEDIN_AUTH_URL}?"
            f"response_type=code&"
            f"client_id={LINKEDIN_CLIENT_ID}&"
            f"redirect_uri={urllib.parse.quote(LINKEDIN_REDIRECT_URI)}&"
            f"scope=r_organization_social"
            f"%20rw_organization_admin%20r_ads_reporting&"
            f"state={encoded_email}"
        )

        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)

class LinkedinCallbackView(APIView):
    def get(self, request):
        """Handle LinkedIn Callback"""
        code = request.GET.get("code")
        encoded_email = request.GET.get("state")  # Retrieve email from state parameter

        if not code:
            return Response({"error": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if not encoded_email:
            return Response({"error": "Email is missing in callback"}, status=status.HTTP_400_BAD_REQUEST)
        
        email = urllib.parse.unquote(encoded_email)
        print(email)
        # Exchange Code for Access Token
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": LINKEDIN_REDIRECT_URI,
            "client_id": LINKEDIN_CLIENT_ID,
            "client_secret": LINKEDIN_CLIENT_SECRET,
        }

        token_response = requests.post(LINKEDIN_TOKEN_URL, data=token_data)
        if token_response.status_code != 200:
            print(token_response.status_code)
            print(token_response.text)
            return Response({"error": "Failed to retrieve access token"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_json = token_response.json()
        access_token = token_json.get("access_token")
        expires_in = token_json.get("expires_in")
        refresh_token = token_json.get("refresh_token")  # Get refresh token


        # Save or Update User & Auth Data
        social_user, _ = SocialUser.objects.get_or_create(email=email)
        LinkedinAuth.objects.update_or_create(
            social_user=social_user,
            defaults={"access_token": access_token, "expires_in": expires_in, "refresh_token":refresh_token},
        )

        return Response(
            {
                "message": "LinkedIn Authentication successful",
                "user": social_user.email,
                "access_token": access_token,
            },
            status=status.HTTP_200_OK,
        )


