from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.urls import reverse


class CustomErrorPagesMiddleWare:
    def __init__(self, get_response):  # 객체가 생성될떄 호출되는 메서드 / get_response 는 호출되는 함수
        self.get_response = get_response

    def __call__(self, request):  # 메서드에서 미들웨어 객체가 호출될때 실행되는 메서드 / request 는 그다음 미들웨어 또는 뷰 요청을 전달합니다.
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return HttpResponseRedirect(redirect('main'))
        elif isinstance(exception, HttpResponseBadRequest):
            return HttpResponseRedirect(redirect('main'))
        elif isinstance(exception, HttpResponseServerError):
            return HttpResponseRedirect(redirect('main'))
        return None
