from django.urls import path

from api.views import *

app_name = 'api'

urlpatterns = [
    path('chatgpt/', chat_gpt_answer, name='chatgpt'),
    path('signchatgpt/', sign_chat_gpt_answer, name='signchatgpt'),
    path('get_previous_chat/',get_previous_message , name='get_previous_chat'),
    path('sign_get_previous_message/',sign_get_previous_message , name='sign_get_previous_message'),
]