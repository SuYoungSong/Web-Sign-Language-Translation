from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings

from newchatgpt.models import ChatRecord, ChatUserCount

client = OpenAI(api_key=settings.GPT_KEY)


def chat_gpt_answer(request):
    if request.method == 'POST':
        prompt = request.POST.get('question')
        completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                    messages=[{"role": "user", "content": prompt}])
        result = completion.choices[0].message.content

        payload = {
            'question': prompt,
            'result': result
        }

        ## ChatRecord 에 저장
        user_count = ChatUserCount.objects.get(user=request.user).count
        ChatRecord.objects.create(question=prompt, answer=result, page=user_count, user=request.user)

        return JsonResponse(payload)

    else:
        # 잘못된 메소드로의 요청에 대한 처리
        return JsonResponse({'error': 'Invalid request method'})


def get_previous_message(request):
    if request.method == 'GET':
        count = ChatUserCount.objects.get(user=request.user).count
        print(count)
        user_record = ChatRecord.objects.filter(user=request.user, page=count).order_by('-pub_date')
        question = list(user_record.values('question'))
        answer = list(user_record.values('answer'))
        print(f'질문: {question}')
        print(f'답변: {answer}')
        message = [{'question': question, 'answer': answer}]

        return JsonResponse({'message': message})

    else:
        return JsonResponse({'error': 'Invalid request method'})
