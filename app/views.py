from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from app.models import *


def home(request):
    return render(request, 'app/template.html')
    
def clubrephome(request):
    tn = "test name"
    return render(request, 'app/clubrephome.html', {"name": tn})