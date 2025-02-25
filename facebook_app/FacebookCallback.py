from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os 
from urllib.parse import parse_qs
from .models import FB_Oauth  # Assuming you're using a model for storing Facebook OAuth details

class FacebookCallback(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        state_param = request.GET.get("state")
        if not state_param:
            return Response({"error": "Missing state"}, status=status.HTTP_400_BAD_REQUEST)

        state_data = parse_qs(state_param)
        email = state_data.get("email", [None])[0]

        if not email:
            return Response({"error": "Email not found in state"}, status=status.HTTP_400_BAD_REQUEST)

        client_id = "385745461007462"
        client_secret = "39838a1fd0b95af866f368acc81f77b0"
        redirect_uri = os.getenv('FB_REDIRECT_URL')

        token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "client_secret": client_secret,
            "code": code,
        }

        response = requests.get(token_url, params=params)
        try:
            response_data = response.json()
        except ValueError:
            return Response({"error": "Invalid JSON response from Facebook"}, status=response.status_code)

        if response.status_code == 200:
            access_token = response_data.get("access_token")

            pages_url = "https://graph.facebook.com/v22.0/me/accounts"
            pages_params = {"access_token": access_token}
            pages_response = requests.get(pages_url, params=pages_params)
            try:
                pages_data = pages_response.json()
            except ValueError:
                return Response({"error": "Invalid JSON response from Facebook for pages"}, status=pages_response.status_code)

            page_id = None
            page_access_token = None
            if "data" in pages_data and pages_data["data"]:
                page = pages_data["data"][0]  # Assuming the first page is selected
                page_id = page.get("id")
                page_access_token = page.get("access_token")

            business_url = "https://graph.facebook.com/v22.0/me/businesses"
            business_params = {"access_token": access_token}
            business_response = requests.get(business_url, params=business_params)
            try:
                business_data = business_response.json()
            except ValueError:
                return Response({"error": "Invalid JSON response from Facebook for business profiles"}, status=business_response.status_code)

            business_profiles = []
            ad_accounts = {}
            if "data" in business_data:
                for business in business_data["data"]:
                    business_id = business.get("id")
                    business_profiles.append(business_id)

                    ad_accounts_url = f"https://graph.facebook.com/v22.0/{business_id}/adaccounts"
                    ad_accounts_params = {"access_token": access_token}
                    ad_accounts_response = requests.get(ad_accounts_url, params=ad_accounts_params)
                    try:
                        ad_accounts_data = ad_accounts_response.json()
                    except ValueError:
                        return Response({"error": "Invalid JSON response from Facebook for ad accounts"}, status=ad_accounts_response.status_code)

                    ad_accounts[business_id] = [ad.get("id") for ad in ad_accounts_data.get("data", [])] if ad_accounts_response.status_code == 200 else []

            instagram_url = f"https://graph.facebook.com/v22.0/{page_id}"
            instagram_params = {"fields": "instagram_business_account", "access_token": page_access_token}
            instagram_response = requests.get(instagram_url, params=instagram_params)
            try:
                instagram_data = instagram_response.json()
            except ValueError:
                return Response({"error": "Invalid JSON response from Facebook for Instagram ID"}, status=instagram_response.status_code)

            instagram_account = instagram_data.get("instagram_business_account", {}).get("id") if instagram_response.status_code == 200 else None

            # Extract first ad account ID if available
            ad_account_id = None
            if business_profiles:
                first_business_id = business_profiles[0]
                ad_account_list = ad_accounts.get(first_business_id, [])
                if ad_account_list:
                    ad_account_id = ad_account_list[0].strip('"')

            # Store in the database
            data = FB_Oauth(
                access_token=access_token,
                page_id=page_id,
                instagram_account=instagram_account,
                business_profiles=business_profiles,
                ad_accounts=ad_account_id,
                social_user_id=email
            )
            data.save()

            # Construct the final response
            datafb = {
                "access_token": bool(access_token),
                "page_id": bool(page_id),
                "instagram_account": bool(instagram_account),
                "business_profiles": bool(business_profiles),
                "ad_accounts": bool(ad_accounts)
            }

            return Response(datafb, status=status.HTTP_200_OK)

        return Response({"error": response_data.get('error', 'Failed to fetch access token')}, status=response.status_code)
