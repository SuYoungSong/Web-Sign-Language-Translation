from django.urls import path

from api.views import *

app_name = 'api'

urlpatterns = [
    path('chatgpt/', chat_gpt_answer, name='chatgpt'),
]