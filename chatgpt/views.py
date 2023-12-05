from django.shortcuts import render
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.GPT_KEY)


# client = OpenAI(api_key=settings.CHAT_GPT_KEY)
# Create your views here.


# chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "user", "content": prompt}])
    print(completion)
    result = completion.choices[0].message.content
    return result


# chatGPT에게 그림 요청 API
def imageGPT(prompt):
    response = client.images.generate(prompt=prompt,
                                      n=1,
                                      size="256x256")
    result = response['data'][0]['url']
    return result


def index(request):
    return render(request, 'gpt/index.html')


def chat(request):
    # post로 받은 question
    prompt = request.POST.get('question')

    # type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
    result = chatGPT(prompt)

    context = {
        'question': prompt,
        'result': result
    }

    return render(request, 'gpt/result.html', context)
