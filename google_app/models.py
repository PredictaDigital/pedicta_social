
from django.db import models
from social_auth.models import BaseModel,SocialUser

class GA4Session(BaseModel):
    date = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    deviceCategory = models.CharField(max_length=225, null=True, blank=True)
    firstUserSourceMedium = models.CharField(max_length=225, null=True, blank=True)
    sessionSource = models.CharField(max_length=225, null=True, blank=True)
    sessions = models.IntegerField(null=True, blank=True)
    activeusers = models.IntegerField(null=True, blank=True)
    newUsers = models.IntegerField(null=True, blank=True)
    totalUsers = models.IntegerField(null=True, blank=True)
    bounceRate = models.FloatField(null=True, blank=True)
    averageSessionDuration = models.FloatField(null=True, blank=True)
    eventCount = models.IntegerField(null=True, blank=True)
    conversions = models.IntegerField(null=True, blank=True)
    screenPageViews = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_google_ga4_session', on_delete=models.CASCADE)

    class Meta:
        db_table = "google_ga4_session"

class GA4Event(BaseModel):
    date = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    deviceCategory = models.CharField(max_length=225, null=True, blank=True)
    firstUserSourceMedium = models.CharField(max_length=225, null=True, blank=True)
    sessionSource = models.CharField(max_length=225, null=True, blank=True)
    pagePath = models.CharField(max_length=100, null=True, blank=True)
    pageTitle = models.CharField(max_length=100, null=True, blank=True)
    eventName = models.CharField(max_length=50, null=True, blank=True)
    sessions = models.IntegerField(null=True, blank=True)
    activeusers = models.IntegerField(null=True, blank=True)
    newUsers = models.IntegerField(null=True, blank=True)
    totalUsers = models.IntegerField(null=True, blank=True)
    bounceRate = models.FloatField(null=True, blank=True)
    averageSessionDuration = models.FloatField(null=True, blank=True)
    eventCount = models.IntegerField(null=True, blank=True)
    conversions = models.IntegerField(null=True, blank=True)
    screenPageViews = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_google_ga4_event', on_delete=models.CASCADE)

    class Meta:
        db_table = "google_ga4_event"

class GA4WebPage(BaseModel):
    date = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    cityId = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    deviceCategory = models.CharField(max_length=225, null=True, blank=True)
    pagePath = models.CharField(max_length=100, null=True, blank=True)
    pagePathPlusQueryString = models.CharField(max_length=200, null=True, blank=True)
    pageTitle = models.CharField(max_length=100, null=True, blank=True)
    startDate = models.CharField(max_length=50, null=True, blank=True)
    endDate = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_google_ga4_webpage', on_delete=models.CASCADE)

    class Meta:
        db_table = "google_ga4_webpage"
