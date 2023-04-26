from django.http import HttpResponse
from django.shortcuts import render

from myapp.models import Person


def home(request):
    return render(request, 'index.html')


def hello(request):
    return HttpResponse("Hello, world! My name is wadda Engineer")


def review_form(request):
    return render(request, 'review_form.html')


def person_list(request):
    # Create a new Person object
    person1 = Person(name='Alice', age=15)

    # Save the Person object to the database
    person1.save()

    # Create another Person object and save it in one step
    person2 = Person.objects.create(name='Bob', age=30)
    person2.save()

    persons = Person.objects.all()
    return render(request, 'person_list.html', {'persons': persons})
