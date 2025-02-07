# views.py
from rest_framework import generics
from .models import SocialUser
from .serializers import SocialUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class SocialUserCreateView(generics.CreateAPIView):
    queryset = SocialUser.objects.all()
    serializer_class = SocialUserSerializer


class SocialUserDelete(APIView):
    def get(self, request, format=None):
        email = request.query_params.get("email")
        try:
             SocialUser.objects.filter(email=email).delete()
        except Exception as e:
            print(e)
        return Response({"message":"User Deleted Sucessfully"},status=status.HTTP_200_OK)
