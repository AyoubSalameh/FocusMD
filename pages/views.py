from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import time, os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import openai
import spin



def foo(text):
    output = 'a '
    for i in range(10):
        output+=output
    #return output #LLM
    return output

# Set up the openai module with your API key
openai.api_key = "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"

# Define a function to send a prompt to Chat GPT and receive a response
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",  # Choose the Chat GPT engine to use
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text


# Create your views here.
def home_view(request):
    return render(request, 'home.html', {})

def patient_view(request):
    return render(request, 'patient.html', {})

def summary_view_changed(request):
    def summary_stream():
        long_string = "This is a very long string that we want to stream word by word."
        words = long_string.split()
        for word in words:
            yield word + ' '
            time.sleep(0.5) # simulate long-running process
        
    response = StreamingHttpResponse(summary_stream())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename="mydata.txt"'
    return response
        



def summary_view(request):

    response = None
    if request.method == 'POST':
        text = request.POST.get('text')
        openai.api_key = "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"
        output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text}
        ])
        response = output['choices'][0]['message']['content']
        
    return render(request, 'summary.html', {'output': response})

          

