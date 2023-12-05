from django.urls import path
from signlanguagetochatgpt.views import index , chat

app_name = 'signlanguagetochatgpt'
urlpatterns = [
    path('', index, name='index'),
    path('chat', chat, name='chat'),
]
