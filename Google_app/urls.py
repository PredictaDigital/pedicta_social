


from django.urls import path
from . import views

urlpatterns = [
    path('ga_ga4/', views.GA4DataAPIView.as_view(), name='GA4'),
    path('ga_gsc/', views.GSCDataAPIView.as_view(), name='GSC'),
]

