# serializers.py
from rest_framework import serializers
from .models import SocialUser

class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ['email']  # Include other fields as needed, e.g., 'created_on', 'updated_on' are auto-managed
