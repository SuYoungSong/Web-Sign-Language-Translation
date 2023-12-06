from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


def gpt_ownership_required(func):
    def decorated(request, *args, **kwargs):  # 안에 user 가 존재
        # target user 는 DB 에서 가져와서 사용
        target_user = User.objects.get(pk=kwargs['pk'])  # kwargs pk 의 정보가 담겨져있음 + user.objects.get() 하나의 인자만 얻고 싶을때
        if target_user == request.user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()  # 접근 금지 경고창을 띄운다.

    return decorated
