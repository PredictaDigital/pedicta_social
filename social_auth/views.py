from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AuthModel, AuthProvider
from .serializers import AuthModelSerializer

class AuthAPIView(APIView):
    def post(self, request):
        """
        Handles LinkedIn authentication and stores authentication details in the database.
        """
        try:
            email = request.data.get("email")
            access_token = request.data.get("access_token")
            refresh_token = request.data.get("refresh_token", None)
            expires_in = request.data.get("expires_in")
            provider = request.data.get("provider")
            
            if not email and not access_token and provider:
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
            
            auth_instance, created = AuthModel.objects.update_or_create(
                email=email,
                provider=provider,
                defaults={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": expires_in,
                }
            )
            
            serializer = AuthModelSerializer(auth_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)


class LinkedRefreshTokenAPIView(APIView):
    def post(self, request):
        """
        Updates the access token using the email and refresh token.
        """
        try:
            email = request.data.get("email")
            refresh_token = request.data.get("refresh_token")
            new_access_token = request.data.get("new_access_token")
            expires_in = request.data.get("expires_in")
            provider = request.data.get("provider")
            
            if not email and not refresh_token and not new_access_token and not provider:
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
            
            auth_instance = get_object_or_404(AuthModel, email=email, provider=provider)
            
            if auth_instance.refresh_token != refresh_token:
                return Response({"error": "Invalid refresh token."}, status=status.HTTP_403_FORBIDDEN)
            
            auth_instance.access_token = new_access_token
            auth_instance.expires_in = expires_in
            auth_instance.provider = provider
            auth_instance.save()
            
            serializer = AuthModelSerializer(auth_instance)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
