from django.urls import path
from .views import LinkedinAPIView

urlpatterns = [
    path('linkedin-dump-data/', LinkedinAPIView.as_view(), name='linkedin-dump-data'),
]