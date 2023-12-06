from django.urls import path

from api.views import *

app_name = 'api'

urlpatterns = [
    path('chatgpt/', chat_gpt_answer, name='chatgpt'),
    path('get_previous_chat/',get_previous_message , name='get_previous_chat'),
]