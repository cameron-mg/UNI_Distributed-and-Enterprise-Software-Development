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
    films = Film.objects.all()
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
                    return render(request, "app/cinemamanager/cmHome.html", {"username":username, "role":role, "logged":logged, "films":films})
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
    form = UserRegistrationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            if password1 != password2:
                return render(request, "registration/register.html", {"error":"Passwords do not match!", "form":form})

            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                return render(request, "registration/register.html", {"error": "Username already in use!", "form":form})

            User.objects.create_user(username=form.cleaned_data["username"], password=password1, role=User.Role.CUSTOMER)
            return redirect("login")
        else:
            return render(request, "registration/register.html", {"form":form})

    else:
        form = UserRegistrationForm()
        return render(request=request, template_name="registration/register.html", context={"form":form})

# CMG VIEWS

def clubAccount(request):
    return render(request, "app/clubrep/clubAccount.html")

# TW VIEWS


def cmHome(request):
    films = Film.objects.all()
    screens = Screen.objects.all()
    showings = Showing.objects.all()
    return render(request, "app/cinemamanager/cmHome.html", {"films" : films, "screens" : screens, "showings" : showings})

def addFilm(request):
    form = addFilmForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            filmTitle = form.cleaned_data["title"]
            filmRating = form.cleaned_data["ageRatings"]
            filmDuration = form.cleaned_data["duration"]
            filmDescription = form.cleaned_data["desc"]

            Film.objects.create(title=filmTitle, ageRatings=filmRating,duration=filmDuration, desc=filmDescription)
            print(Film)
            return redirect("cmHome")
        else:
            print(form.errors)
            return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})
    else:
        return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})

def deleteFilm(request, pk):
    if request.method == "POST":
        film = Film.objects.get(pk=pk)
        film.delete()
        return redirect('cmHome')
    else:
        return redirect('cmHome')

def deleteScreen(request, pk):
    if request.method == "POST":
        screen = Screen.objects.get(pk=pk)
        screen.delete()
        return redirect('cmHome')
    else:
        return redirect('cmHome')

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

def addScreen(request):
    form = addScreenForm(request.POST or None)
    
    if request.method == "POST":
        
        if form.is_valid():
            screenNumber = form.cleaned_data["screenNo"]
            screenCapacity = form.cleaned_data["capacity"]
            Screen.objects.create(screenNo=screenNumber, capacity=screenCapacity)
            print(Screen)

            return redirect("cmHome")
        else:
            return render(request, "app/cinemamanager/cmAddScreen.html", {"form" : form})
    else:
        return render(request, "app/cinemamanager/cmAddScreen.html", {"form" : form})

def addShowing(request):
    form = addShowingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            showing = Showing.objects.create(
                film=form.cleaned_data['film'],
                screen=form.cleaned_data['screen'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                remainingSeats=form.cleaned_data['remainingSeats']
            )
            
            return redirect('cmAddShowing')
        else:
            return render(request, 'app/cinemamanager/cmAddShowing.html', {'form' : form})
    else:
        return render(request, 'app/cinemamanager/cmAddShowing.html', {'form' : form})


    
# CR VIEWS

# JD VIEWS
