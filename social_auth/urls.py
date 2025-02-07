# urls.py
from django.urls import path
from .views import SocialUserCreateView,SocialUserDelete

urlpatterns = [
    path('user-register/', SocialUserCreateView.as_view(), name='create_social_user'),
    path('user-delete/', SocialUserDelete.as_view(), name='user_delete'),
]
