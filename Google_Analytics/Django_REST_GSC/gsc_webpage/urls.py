

from django.urls import path
from . import views

urlpatterns = [
    path('gsc_webpage/', views.GSCDataAPIView.as_view(), name='gsc_webpage'),
]

