# urls.py
from django.urls import path
from .views import SocialUserCreateView

urlpatterns = [
    path('user-register/', SocialUserCreateView.as_view(), name='create_social_user'),
]
