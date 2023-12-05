from django.urls import path

from newchatgpt.views import *

app_name = 'newchatgpt'

urlpatterns = [
    path('', index, name='index'),
]