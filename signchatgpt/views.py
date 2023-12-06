from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accountapp/login/')  # 비로그인시 login 페이지로 추방
def index(request):
    return render(request, 'signchatgpt/index.html')

