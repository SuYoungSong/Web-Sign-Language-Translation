from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings



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
        return JsonResponse(payload)
    
    else:
        # 잘못된 메소드로의 요청에 대한 처리
        return JsonResponse({'error': 'Invalid request method'})
        
    