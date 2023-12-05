from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
import mlflow
import mlflow.keras
from chatgpt.views import chatGPT

logger = logging.getLogger('mylogger')
# signlanguage/models.py의 Result 모델을 import한다.
from .models import ChatResult, Result

# Create your views here.

'''
1. 원칙은 ORM을 사용하여 별도 sql 문이 없는 것이다.
2. 하지만, ORM을 사용하면서도 sql문을 사용해야 하는 경우가 있다.
3. 이때는 아래와 같이 사용한다.
 - 물론 이 부분도 view가 sql을 알면 안되서 분리해야 하지만, 짧은 교육상 이곳에 둔다. 
'''


def getChatResult(self, id):
    query = "SELECT * FROM signlanguagetochatgpt_chatresult WHERE id = {0}".format(id)
    logger.info(">>>>>>>> getChatResult SQL : " + query)
    chatResult = self.t_exec(query)


def index(request):
    return render(request, 'signlanguagetochatgpt/index.html')


def chat(request):
    if request.method == 'POST' and request.FILES['files']:

        results = []
        # form에서 전송한 파일을 획득한다.
        # 각 파일별 예측 결과들을 모아야 질문을 위한 언어가 완성된다.
        files = request.FILES.getlist('files')
        chatGptPrompt = ""
        for idx, file in enumerate(files, start=0):
            # files:

            # logger.error('file', file)
            # class names 준비
            class_names = list(string.ascii_lowercase)
            class_names = np.array(class_names)

            # mlflow 로딩
            mlflow_uri = "http://mini7-mlflow.carpediem.so/"
            mlflow.set_tracking_uri(mlflow_uri)
            model_uri = "models:/Sign_Signal/production"
            model = mlflow.keras.load_model(model_uri)

            # history 저장을 위해 객체에 담아서 DB에 저장한다.
            # 이때 파일시스템에 저장도 된다.
            result = Result()
            result.image = file
            result.pub_date = timezone.datetime.now()
            result.save()

            # 흑백으로 읽기
            img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)

            # 크기 조정
            img = cv2.resize(img, (28, 28))

            # input shape 맞추기
            test_sign = img.reshape(1, 28, 28, 1)

            # 스케일링
            test_sign = test_sign / 255.

            # 예측 : 결국 이 결과를 얻기 위해 모든 것을 했다.
            pred = model.predict(test_sign)
            pred_1 = pred.argmax(axis=1)

            result_str = class_names[pred_1][0]

            # 결과를 DB에 저장한다.
            result.result = result_str
            # result.is_correct =
            result.save()
            results.append(result)

            # result.result의 결과를 하나씩 chatGptPrompt에 추가한다.
            chatGptPrompt += result.result

        # 질문을 DB에 저장한다.
        chatResult = ChatResult()
        chatResult.prompt = chatGptPrompt
        chatResult.pub_date = timezone.datetime.now()
        chatResult.save()

        # 저장된 질문을 DB에서 가져온다.
        selectedChatResult = ChatResult.objects.get(id=chatResult.id)

        # chatGptPrompt를 chatGPT에게 전달한다.
        content = chatGPT(selectedChatResult.prompt)
        selectedChatResult.content = content
        selectedChatResult.save()

        context = {
            'question': selectedChatResult.prompt,
            'result': selectedChatResult.content
        }

    return render(request, 'signlanguagetochatgpt/result.html', context)
