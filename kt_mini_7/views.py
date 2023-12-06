from django.shortcuts import render


# def homepage(request):
    # return render(request , 'homepage.html')


def index(request):
    return render(request , 'index.html')