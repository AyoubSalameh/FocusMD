from django.shortcuts import render
from django.http import HttpResponse

def foo(text):
    return text #LLM

# Create your views here.
def home_view(request):
    return render(request, 'home.html', {})

def patient_view(request):
    return render(request, 'patient.html', {})

def summary_view(request):
    output = None
    if request.method == 'POST':
        text = request.POST.get('text')
        output = foo(text)
    return render(request, 'summary.html', {'output': output})