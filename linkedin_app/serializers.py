from rest_framework import serializers
from .models import LinkedinAuth

class LinkedinAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedinAuth
        fields = ['access_token', 'refresh_token', 'expires_in', 'social_user']
