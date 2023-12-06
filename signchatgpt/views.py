from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.db.models import F
from django.shortcuts import render

from signchatgpt.models import ImageCount, ImageRecord
import pandas as pd


# Create your views here.

def chat_history(user):
    user_record = ImageRecord.objects.filter(user=user)

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


@login_required(login_url=reverse_lazy('accountapp:login'), redirect_field_name='next')  # 비로그인시 login 페이지로 추방
def index(request):
    is_exist = ImageCount.objects.filter(user=request.user).exists()
    is_refresh = request.headers.get('Cache-Control') == 'max-age=0'
    result = dict()

    if is_refresh and is_exist:
        is_exist_record = ImageRecord.objects.filter(user=request.user).exists()
        if is_exist_record:
            count = ImageCount.objects.get(user=request.user).count
            page = ImageRecord.objects.filter(user=request.user).latest('page').page
            result = chat_history(user=request.user)

            if page == count:
                print('이전 내용이 있는 상태에서 새로고침 했기때문에 이전 내용을 띄워줍니다.')
            else:
                print("첫 화면에서 새로고침이라 이전 대화 내용이 없습니다")
        else:
            return render(request , 'signchatgpt/index.html')

    else:
        if is_exist:
            print('gpt 사용기록이 존재합니다 새로운 페이지 입니다')
            user = ImageCount.objects.get(user=request.user)
            user.count += 1
            user.save()
            result = chat_history(user=request.user)
        else:
            ImageCount.objects.create(user=request.user , count=1)
    return render(request, 'signchatgpt/index.html' , {'result':result})
