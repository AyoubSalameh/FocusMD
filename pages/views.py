from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
#import models 
import time, os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import openai
import spin
import html

med_hist = """Name: Bessie Popkin

         Age: 82

         Gender: Female

         weight: 66kg

         height: 161cm

         Born 1940 in Poland, immigrated to US 1946. Married with one child, retired(2003) math professor.

         Medical History:

         Hypertension, hyperlipidemia.

         Diagnosed with diabetes and chronic heart failure in 2008.

         Thyroidectomy in 2004 due to thyroid cancer.

         Pancreatectomy in 1999 due to mucinus carcinoma

         During childhood had tuberculosis

         no known allergies or sensitivities.

         Medication

         euthytox 150mcg\day, was 100mcg\day, last changed december 2022.

         fusid 30mg\day. was 20mg\day, last changed at feb. 23, 2020

         lipitor 20mg\day, prescribed in 1997.

         cardiloc 20mg\day. was 35mg\day, last changed at sept. 22, 2017

         clonex 0.5mg\day, prescribed march 2020

         Used to take aspirin until oct. 2014

         Date of Vaccination: july 15, 2022

         Chief Complaint: None

         History of Present Illness: The patient received the COVID-19 vaccine on july 15, 2022, without any immediate adverse reactions or side effects. The vaccine was administered at the local clinic and the patient reported feeling well throughout the day.

         Past Medical History: The patient has a history of hypertension, which is currently well-controlled with medication. No other significant medical history was reported.

         past hospitalizations

         feb. 10 - feb. 14, 2023:

         january 2 - january 8, 2022: Severe Covid-19. Received oxygen support.

         september 17 - september 20, 2017: cataract operation. Following the operation, the patient experienced infection in right eye, treated with antibiotics.

         feb. 13 - feb. 18, 2014: community acquired pneumonia and

         march 28 - april 4, 2008: diabetes related. Had difficulties in mobility.

         november 7 - november 30 2004: thyroidectomy. following the operation, the patient experienced internal bleeding in the abdomen.

         july 18 - aug. 7, 1999: Pancreatectomy. no complication reported.

         specialists report

         endocrinology, January 2, 2023:

         Cardiology, November 11, 2022: no change in the chronic heart failure

         Nephrology, september 18, 2017: ultrasound results are satisfactory.

         Cardiology, May 3, 2017: no change in the chronic heart failure

         lab tests:

         feb. 11th, 2023:

         - Glucose: 135 mg/dL(Normal range: 70-100 mg/dL)
         - Hemoglobin A1C: 7.2 % (Normal range: less than 5.7 %)
         - Total Cholesterol: 205 mg/dL(Normal range: less than 200 mg/dL)
         - LDL Cholesterol: 130 mg/dL(Normal range: less than 100 mg/dL)
         - HDL Cholesterol: 50 mg/dL(Normal range: greater than 40 mg/dL for men, greater than 50 mg/dL for women)
         - Triglycerides: 165 mg/dL

         July 14th, 2022:

         - Complete Blood Count(CBC):
         - White Blood Cell Count(WBC): 7.0 x 10 ^ 3/uL(Normal range: 4.5 - 11.0 x 10 ^ 3/uL)
         - Red Blood Cell Count(RBC): 4.4 x 10 ^ 6/uL(Normal range: 3.9 - 5.2 x 10 ^ 6/uL)
         - Hemoglobin(Hb): 12.3 g/dL(Normal range: 12.0 - 16.0 g/dL)
         - Hematocrit (Hct): 36.7 % (Normal range: 37.0 - 47.0 %)
         - Platelet Count: 250 x 10 ^ 3/uL(Normal range: 150 - 400 x 10 ^ 3/uL)
         - Comprehensive Metabolic Panel(CMP):
         - Fasting Glucose: 120 mg/dL(Normal range: 70-100 mg/dL)
         - Hemoglobin A1C: 6.9 % (Normal range: less than 5.7 %)
         - Blood Urea Nitrogen(BUN): 26 mg/dL(Normal range: 8-20 mg/dL)
         - Creatinine: 1.1 mg/dL(Normal range: 0.6-1.3 mg/dL)
         - Sodium: 142 mmol/L(Normal range: 135-145 mmol/L)
         - Potassium: 3.8 mmol/L(Normal range: 3.5-5.1 mmol/L)
         - Chloride: 101 mmol/L(Normal range: 98-107 mmol/L)
         - Calcium: 9.2 mg/dL(Normal range: 8.5-10.5 mg/dL)
         - Total Protein: 7.3 g/dL(Normal range: 6.0-8.3 g/dL)
         - Albumin: 4.2 g/dL(Normal range: 3.5-5.0 g/dL)
         - Bilirubin, Total: 0.7 mg/dL(Normal range: 0.2-1.2 mg/dL)
         - Alkaline Phosphatase: 78 U/L(Normal range: 44-147 U/L)
         - Aspartate Aminotransferase(AST): 26 U/L(Normal range: 5-34 U/L)
         - Alanine Aminotransferase(ALT): 27 U/L(Normal range: 0-55 U/L)
         - Lipid Panel:
         - Total Cholesterol: 190 mg/dL(Normal range: less than 200 mg/dL)
         - LDL Cholesterol: 120 mg/dL(Normal range: less than 100 mg/dL)
         - HDL Cholesterol: 55 mg/dL(Normal range: greater than 40 mg/dL for men, greater than 50 mg/dL for women)
         - Triglycerides: 150 mg/dL(Normal range: less than 150 mg/dL)"""




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
    #obj = MyModel.objects.first()
    #context = {'image': obj.image}
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
        
msgs = [
    {"role": "user", "content": "Act as a medical assistant. The following is a detailed medical history of a patient that were checked in general medicine department. later, You will be asked to answer questions about the patient history. be concise and professional. If you are missing information, inform that relevant data is not available."},
    {"role": "assistant", "content": "Certainly, I'd be happy to assist as a medical assistant. Please provide me with the patient's medical history, and I'll review it carefully."},
    {"role": "user", "content": med_hist},
    {"role": "assistant", "content": "ready for questions"}
]

def summary_view(request):
    response = None
    if request.method == 'POST':
        text = request.POST.get('text')
        openai.api_key = "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"
        msgs.append({"role": "user", "content": text})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msgs
        )
        response = completion["choices"][0]["message"]
        msgs.append(response)
        response = response["content"] 
    return render(request, 'summary.html', {'output': html.escape(response or "")})

def summary_view_og(request):
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

          

