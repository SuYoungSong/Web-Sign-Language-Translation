from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
import numpy as np
import mlflow
import mlflow.tensorflow
import cv2
from django.utils import timezone
import string

from newchatgpt.models import ChatRecord, ChatUserCount
from signchatgpt.models import ImageCount, ImageRecord

client = OpenAI(api_key=settings.GPT_KEY)


def chat_gpt(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "user", "content": prompt}])
    result = completion.choices[0].message.content

    payload = {
        'question': prompt,
        'result': result
    }

    return payload


def chat_gpt_answer(request):
    if request.method == 'POST':
        prompt = request.POST.get('question')

        payload = chat_gpt(prompt)

        ## ChatRecord 에 저장
        user_count = ChatUserCount.objects.get(user=request.user).count
        ChatRecord.objects.create(question=payload['question'], answer=payload['result'], page=user_count,
                                  user=request.user)

        return JsonResponse(payload)

    else:
        # 잘못된 메소드로의 요청에 대한 처리
        return JsonResponse({'error': 'Invalid request method'})


def sign_chat_gpt_answer(request):
    if request.method == 'POST' and request.FILES['files']:
        files = request.FILES.getlist('files')

        # mlflow 로딩
        mlflow_uri = "http://mini7-mlflow.carpediem.so/"
        mlflow.set_tracking_uri(mlflow_uri)
        model_uri = "models:/model_hj/production"
        model = mlflow.tensorflow.load_model(model_uri)

        chatGptPrompt = ""
        for idx, file in enumerate(files, start=0):
            class_names = list(string.ascii_lowercase)
            class_names = np.array(class_names)

            # 파일의 내용을 메모리에 로드
            file_content = np.frombuffer(file.read(), np.uint8)

            # OpenCV로 이미지 읽기
            img = cv2.imdecode(file_content, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (28, 28))
            img = img.reshape(1, 28, 28, 1)
            img = img / 255.

            pred = model.predict(img)
            pred_1 = pred.argmax(axis=1)

            result_str = class_names[pred_1][0]
            chatGptPrompt += result_str

        payload = chat_gpt((chatGptPrompt))

        ## ChatRecord 에 저장
        user_count = ImageCount.objects.get(user=request.user).count
        ImageRecord.objects.create(question=payload['question'], answer=payload['result'], page=user_count,
                                  user=request.user)

        return JsonResponse(payload)
    else:
        # 잘못된 메소드로의 요청에 대한 처리
        return JsonResponse({'error': 'Invalid request method'})


#


def get_previous_message(request):
    if request.method == 'POST':
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
