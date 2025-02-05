# views.py
from rest_framework import generics
from .models import SocialUser
from .serializers import SocialUserSerializer

class SocialUserCreateView(generics.CreateAPIView):
    queryset = SocialUser.objects.all()
    serializer_class = SocialUserSerializer
