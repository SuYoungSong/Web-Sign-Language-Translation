from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from newchatgpt.decorators import gpt_ownership_required
from newchatgpt.models import ChatRecord, ChatUserCount
from django.db.models import Subquery, OuterRef, Count
from django.db.models import F
from django.db.models.functions import TruncDate
from django.db.models import Max
import pandas as pd


# Create your views here.

# has_ownership = [login_required, gpt_ownership_required]


def chat_history(user):
    user_record = ChatRecord.objects.filter(user=user)

    group_data = user_record.values('pub_date', 'page').annotate(
        question=F('question'),
        datetime=F('pub_datetime'),
    )

    date = []
    page = []
    questions = []
    answers = []
    pub_date_times = []
    for data in group_data:
        date.append(data['pub_date'])
        page.append(data['page'])
        questions.append(data['question'])
        pub_date_times.append(data['datetime'])

    user_data = pd.DataFrame(
        {'date': date, 'datetime': pub_date_times, 'page': page, 'question': questions})
    test = user_data.sort_values(by='datetime', ascending=False).groupby(['date', 'page']).head(1)
    dates = test['date'].unique()

    result = []
    for d in dates:
        date_data = test.loc[test['date'] == d, :]
        result.append({
            'pub_date': d,
            'message': [{'page': p, 'question': q} for p, q in
                        zip(date_data['page'], date_data['question'])]
        })

    return result

@login_required(login_url='/accountapp/login/')  # 비로그인시 login 페이지로 추방
def index(request):
    is_exist = ChatUserCount.objects.filter(user=request.user).exists()  # 계정에서 GPT 사용한적이 있는지 여부
    is_refresh = request.headers.get('Cache-Control') == 'max-age=0'  # 새로고침 판단 여부
    result = dict()
    if is_refresh and is_exist:
        print('새로고침 상태 이기 떄문에 gpt 의 페이지가 증가하지 않습니다')
        is_exist_record = ChatRecord.objects.filter(user=request.user).exists()
        if is_exist_record:
            count = ChatUserCount.objects.get(user=request.user).count
            page = ChatRecord.objects.filter(user=request.user).latest('page').page
            result = chat_history(user=request.user)
            # 만약 새로고침을 했는데 ChatUserCount 에 있는 count 값이 Chatrecord 에 page 값에 있는 경우 -> 현재 카운트 페이지로 gpt 를 사용한적 있다 -> 이전 내용을
            # 불러온다
            if page == count:
                print('이전 내용이 있는 상태에서 새로고침 했기때문에 이전 내용을 띄워줍니다.')

            # 만약 새로고침을 했는데 ChatUserCount 에 있는 count 값이 Chatrecord 에 page 값에 없는 경우 -> 현재 카운트 페이지에서 그냥 새로고침 했다 -> 이전 데이터 가없다.
            else:
                print("첫 화면에서 새로고침 이라 이전 대화 내용이 없습니다")
        else:
            return render(request,'newchatgpt/index.html')

    else:
        if is_exist:
            print('gpt 사용기록이 존재합니다 새로운 페이지 입니다')
            user = ChatUserCount.objects.get(user=request.user)
            user.count += 1
            user.save()
            result = chat_history(user=request.user)
            # return render(request, 'newchatgpt/index.html', {'result': chat_history(user=request.user)})
        else:
            ChatUserCount.objects.create(user=request.user, count=1)
    return render(request, 'newchatgpt/index.html', {'result': result})
