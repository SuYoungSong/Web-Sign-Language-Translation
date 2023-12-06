from django.shortcuts import render, redirect

def index(request):
    return render(request , 'index.html')

def bad_request_page(request, exception):
    return render(request , 'index.html')

def page_not_found_page(request, exception):
    return render(request , 'index.html')

def server_error_page(request):
    return render(request , 'index.html')