from django.http import HttpResponse
from fshec2.main import load_path
from django.shortcuts import render, redirect


def home(request):
    # return HttpResponse('Hello')
    return render(request, 'index.html')


def hello(request):
    load_path()
    return HttpResponse("Hello, world!")
