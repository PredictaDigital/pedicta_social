from django.db import models

# Create your models here.
from social_auth.models import BaseModel,SocialUser
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone




class GoogleCredentials(BaseModel):
    user = models.OneToOneField(SocialUser,on_delete=models.CASCADE,related_name='google_user')
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    expiry = models.DateTimeField()

    def is_expired(self):
        return self.expiry <= timezone.now()

    class Meta:
        verbose_name_plural = "Google Credentials"