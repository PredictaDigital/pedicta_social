from django.urls import path
from .views import LinkedinAuthCreateView, LinkedinAPIView

urlpatterns = [
    path('fetch-record/', LinkedinAPIView.as_view(), name='linkedin-dump-data'),
    path('auth/', LinkedinAuthCreateView.as_view(), name='linkedin-auth-create'),
]