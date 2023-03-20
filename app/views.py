from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from app.models import *
from django.shortcuts import redirect
from app import forms, models
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, 'app/home.html')

def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request=request, data=request.POST)
        
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                role = user.get_role()
                logged = True
                login(request, user)
                if role == "CUSTOMER":
                    return render(request, "app/customer/cHome.html", {"username":username, "role":role, "logged":logged})
                elif role == "CLUBREP":
                    return render(request, "app/clubrep/crHome.html", {"username":username, "role":role, "logged":logged})
                elif role == "CINEMAMAN":
                    return render(request, "app/cinemamanager/cmHome.html", {"username":username, "role":role, "logged":logged})
                elif role == "ACCOUNTMAN":
                    return render(request, "app/accountmanager/amHome.html", {"username":username, "role":role, "logged":logged})
                else:
                    return render(request, "app/home.html", {"username":username, "role":role, "logged":logged})
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"form":form})


def register_request(request):
    if request.POST == "POST":

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = forms.save(commit=False)
            user.role = "CUSTOMER"
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("home")

    else:
        form = UserRegistrationForm()
        return render(request=request, template_name="registration/register.html", context={"form":form})

# CMG VIEWS

def clubAccount(request):
    return render(request, "app/clubrep/clubAccount.html")

# TW VIEWS

def registerClub(request):
    form = registerClubForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()

            return redirect("home")
        else:
            return render(request, "app/cinemamanager/registerClub.html", {"form": form})
    else:
        return render(request, "app/cinemamanager/registerClub.html", {"form": form})

def addFilm(request):
    form = addFilmForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()

            return redirect("home")
        else:
            return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})
    else:
        return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})

    
# CR VIEWS

# JD VIEWS
