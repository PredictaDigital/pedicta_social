from django.urls import path
from .views import AuthAPIView, LinkedRefreshTokenAPIView

urlpatterns = [
    path('auth-token/', AuthAPIView.as_view(), name='auth-token/'),
    path('Linked-refresh-token/', LinkedRefreshTokenAPIView.as_view(), name='linked_refresh_token'),
]