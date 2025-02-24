"""
URL configuration for predicta_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from google_app.views import Oauth2callbackAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_auth.urls')),
    path('linkedin/', include('linkedin_app.urls')),
    path('facebook_app/', include('facebook_app.urls')),
    path('instagram/', include('instagram.urls')),
    path('google/', include('google_app.urls')),
    path('',Oauth2callbackAPIView.as_view(),name='/'),
]
