from app.models import *
from app.forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
                    return redirect("crHome")
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

def crHome(request):
    return render(request, "app/clubrep/crHome.html")

def clubAccount(request):
    form = ClubAccountForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

            clubid = form.cleaned_data["clubid"]
            try:
                print(clubid)
                club = Club.objects.filter(clubid=clubid).get()
                c_logged = True
                error = ""
                return render(request, "app/clubrep/clubAccount.html", {"c_logged":c_logged, "error":error, "name":club.name})
            except:
                c_logged = False
                error = "Please enter a valid club identification number."
                return render(request, "app/clubrep/clubAccount.html", {"c_logged":c_logged, "error":error})
        else:
            c_logged = False
            return render(request, "app/clubrep/clubAccount.html", {"form":form, "c_logged":c_logged})
    else:
        c_logged = False
        return render(request, "app/clubrep/clubAccount.html", {"form":form, "c_logged":c_logged})


# TW VIEWS

def cmHome(request):
    films = Film.objects.all()
    return render(request, "app/cinemamanager/cmHome.html", {"films":films})

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
            Film.objects.create(title=form.cleaned_data["title"], ageRatings=form.cleaned_data["ageRatings"],duration=form.cleaned_data['duration'], desc=form.cleaned_data['desc'])
            print(Film)
            return redirect("cmHome")
        else:
            print(form.errors)
            return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})
    else:
        return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})

    
# CR VIEWS

# JD VIEWS
