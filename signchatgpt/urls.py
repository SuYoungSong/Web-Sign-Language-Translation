from django.urls import path

from signchatgpt.views import *

app_name = 'signchatgpt'

urlpatterns = [
    path('', index, name='index'),
]