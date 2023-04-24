from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('hello/', views.hello, name='hello'),
    path('review_form/', views.review_form, name='review_form'),
]
