from django.urls import path
from .views import LinkedinAuthCreateView, LinkedinAPIView, LinkedinLoginView, LinkedinCallbackView

urlpatterns = [
    path('fetch-record/', LinkedinAPIView.as_view(), name='linkedin-dump-data'),
    path('auth/', LinkedinAuthCreateView.as_view(), name='linkedin-auth-create'),
    path("login/", LinkedinLoginView.as_view(), name="linkedin-login"),
    path("callback/", LinkedinCallbackView.as_view(), name="linkedin-callback"),
]