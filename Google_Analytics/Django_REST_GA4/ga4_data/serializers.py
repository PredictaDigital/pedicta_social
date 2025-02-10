

from rest_framework import serializers
from .models import GA4Session, GA4Event, GA4WebPage

class GA4SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GA4Session
        fields = '__all__'

class GA4EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GA4Event
        fields = '__all__'

class GA4WebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GA4WebPage
        fields = '__all__'
