from app.models import *
from app.forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

def home(request):
    return render(request, 'app/home.html')

def login_request(request):
    films = Film.objects.all()
    showings = Showing.objects.all()
    screens = Screen.objects.all()
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
                    return render(request, "app/cinemamanager/cmHome.html", {"username":username, "role":role, "logged":logged, "films":films, "screens" : screens, "showings": showings})
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
    try:
        clubrep = ClubRep.objects.filter(user=request.user).get()
        error = ""
        return render(request, "app/clubrep/crHome.html", {"clubrep":clubrep, "error":error})
    except:
        error = "ClubRep profile not found!"
        return render(request, "app/clubrep/crHome.html", {"error":error})

def clubAccount(request):
    form = ClubAccountForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():

            clubid = form.cleaned_data["clubid"]
            try:
                club = Club.objects.filter(clubid=clubid).get()
                transactions = Transaction.objects.all().filter(account=club)
                c_logged = True
                error = ""
                return render(request, "app/clubrep/clubAccount.html", {"c_logged":c_logged, "error":error, "club":club, "transactions":transactions})
            except:
                c_logged = False
                error = "Please enter a valid club identification number."
                return render(request, "app/clubrep/clubAccount.html", {"form":form, "c_logged":c_logged, "error":error})
        else:
            c_logged = False
            return render(request, "app/clubrep/clubAccount.html", {"form":form, "c_logged":c_logged})
    else:
        c_logged = False
        return render(request, "app/clubrep/clubAccount.html", {"form":form, "c_logged":c_logged})

def clubBooking(request):
    form = BookingDateForm(request.POST or None)
    dated = False

    if request.method == "POST":
        if form.is_valid():

            bookingDate = form.cleaned_data["bookingDate"]
            try:
                showings = Showing.objects.filter(date=bookingDate)
                dated = True
                return render(request, "app/clubrep/blockBooking.html", {"dated":dated, "showings":showings})
            except:
                return render(request, "app/clubrep/blockBooking.html", {"form": form, "dated":dated})
        else:
            return render(request, "app/clubrep/blockBooking.html", {"form": form, "dated":dated})
    else:
        return render(request, "app/clubrep/blockBooking.html", {"form": form, "dated":dated})

def confirmBooking(request, pk):
    form = BlockBookingQuantity(request.POST or None)
    showing = Showing.objects.get(pk=pk)
    qPicked = False

    if request.method == "POST":
        if form.is_valid():
            qPicked = True
            q = form.cleaned_data["quantity"]
            return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "q":q, "qPicked":qPicked})
        else:
            return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "form":form})
    else:
        return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "form":form})

def saveClubBooking(request, pk, q):
    showing = Showing.objects.get(pk=pk)
    postConf = True
    if showing.remainingSeats > q:
        try:
            user = request.user
            rep = ClubRep.objects.filter(user=user).get()
            club = rep.club
            afterDiscount = 100-club.discount
            overallCost = ((showing.price*q)/100)*afterDiscount
            
            newBlockBooking = BlockBooking.objects.create(
                quantity = q,
                club = club, 
                cost = overallCost,
                datetime = datetime.datetime.now()
            )

            newTransaction = Transaction.objects.create(
                account = club,
                madeby = user,
                quantity = q,
                cost = overallCost,
                datetime = datetime.datetime.now()
            )
            
            showing.remainingSeats = showing.remainingSeats - q
            club.balance = club.balance + overallCost

            newBlockBooking.save()
            newTransaction.save()
            showing.save()
            club.save()

            processed = True
            return render(request, "app/clubrep/blockBookingConfirmation.html", {"postConf": postConf, "processed":processed})
        
        except:
            processed = False
            error = "Error: You are not registered to a club."
            return render(request, "app/clubrep/blockBookingConfirmation.html", {"postConf": postConf, "processed":processed, "error":error})
    
    else:
        processed = False
        error = "Insufficient seats to accomodate booking."
        return render(request, "app/clubrep/blockBookingConfirmation.html", {"postConf": postConf, "processed":processed, "error":error})

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
        try:
            showing = Showing.objects.filter(film=film).get()
            return redirect('cmHome')
        except:
            film.delete()
            return redirect('cmHome')
    else:
        return redirect('cmHome')


def updateFilm(request, pk):
    film = Film.objects.get(pk=pk)
    form = addFilmForm(request.POST or None, instance=film)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("cmHome")
        else:
            return render(request, "app/cinemamanager/cmUpdateDetails.html", {"form" : form})
    else:
        return render(request, "app/cinemamanager/cmUpdateDetails.html", {"form" : form})

def registerClub(request):
    form = RegisterClubForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            address = Address.objects.create(number=form.cleaned_data["aNumber"], street=form.cleaned_data["aStreet"], city=form.cleaned_data["aCity"], postCode=form.cleaned_data["aPostCode"])
            contact = Contact.objects.create(landline=form.cleaned_data["cLandline"], mobile=form.cleaned_data["cMobile"], email=form.cleaned_data["cEmail"], firstName=form.cleaned_data["cFirstName"], surName=form.cleaned_data["cSurName"])
            payment = Payment.objects.create(cardNumber=form.cleaned_data["pCardNumber"], expiryDate=form.cleaned_data["pExpiryDate"])
            Club.objects.create(clubid=form.cleaned_data["clubid"], name=form.cleaned_data["clubname"], address=address, contact=contact, payment=payment, discount=form.cleaned_data["discount"], balance=0)

            return redirect("cmHome")
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
    
def deleteScreen(request, pk):
    if request.method == "POST":
        screen = Screen.objects.get(pk=pk)
        screen.delete()
        return redirect('cmHome')
    else:
        return redirect('cmHome')
    
def updateScreen(request, pk):
    screen = Screen.objects.get(pk=pk)
    form = addScreenForm(request.POST or None, instance=screen)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("cmHome")
        else:
            return render(request, "app/cinemamanager/cmUpdateDetails.html", {"form" : form})
    else:
        return render(request, "app/cinemamanager/cmUpdateDetails.html", {"form" : form})

def addShowing(request):
    form = addShowingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            showing = Showing.objects.create(
                film=form.cleaned_data['film'],
                screen=form.cleaned_data['screen'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                remainingSeats=form.cleaned_data['screen'].capacity
            )
            
            return redirect('cmHome')
        else:
            return render(request, 'app/cinemamanager/cmAddShowing.html', {'form' : form})
    else:
        return render(request, 'app/cinemamanager/cmAddShowing.html', {'form' : form})
    
def deleteShowing(request, pk):
    if request.method == "POST":
        screen = Showing.objects.get(pk=pk)
        screen.delete()
        return redirect('cmHome')
    else:
        return redirect('cmHome')

def updateShowing(request, pk):
    showing = Showing.objects.get(pk=pk)
    form = addShowingForm(request.POST or None, instance=showing)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("cmHome")
        else:
            return render(request, "app/cinemamanager/cmUpdateDetails.html", {"form" : form})
    else:
        return render(request, "app/cinemamanager/cmUpdateDetails.html", {"form" : form})


    
# CR VIEWS

# JD VIEWS
