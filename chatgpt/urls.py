from django.urls import path

from chatgpt.views import index , chat

app_name = 'chatgpt'

urlpatterns = [
    path('', index, name='index'),
    path('chat', chat, name='chat'),
]