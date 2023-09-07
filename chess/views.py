from django.shortcuts import render
from django import http

# Create your views here.

def home(request):
    return http.HttpResponse("Hello World")