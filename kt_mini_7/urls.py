"""kt_mini_7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from kt_mini_7.views import *

urlpatterns = [
                  path('', index, name='main'),
                  path('admin/', admin.site.urls),
                  path('accountapp/', include('accountapp.urls')),
                  path('api/',include('api.urls')),
                  path('newchatgpt/',include('newchatgpt.urls')),
                  path('signchatgpt/',include('signchatgpt.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
