from rest_framework import serializers
from .models import FB_Oauth

class FB_OauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = FB_Oauth
        fields = ['access_token', 'page_id', 'instagram_account', 'business_profiles', 'ad_accounts', 'social_user']