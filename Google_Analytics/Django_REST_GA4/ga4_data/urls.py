


from django.urls import path
from . import views

urlpatterns = [
    path('ga4_data/', views.GA4DataAPIView.as_view(), name='ga4_data'),
]

