from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def hello(request):
    return HttpResponse("Hello, world! My name is wadda Engineer")
def review_form(request):
    return render(request,'review_form.html')
