# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .helpers import *
from rest_framework import generics
from .models import LinkedinAuth
from .serializers import LinkedinAuthSerializer

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




