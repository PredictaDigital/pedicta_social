from rest_framework import serializers
from .models import AuthModel

class AuthModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModel
        fields = '__all__'