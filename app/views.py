from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from app import forms
from app import models


def home(request):
    return render(request, 'app/home.html')
    
def registerClub(request):
    form = forms.registerClub(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()

            return redirect("home")
        else:
            return render(request, "app/registerClub.html", {"form": form})
    else:
        return render(request, "app/registerClub.html", {"form": form})