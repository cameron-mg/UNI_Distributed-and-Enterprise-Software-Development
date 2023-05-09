from typing import Any
from app.models import *
from app.forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import datetime

# Class used to check user roles
class RoleCheck:
    def __init__(self, *args):
        self.check = args
    
    def __call__(self, user):
        return hasattr(user, 'role') and user.role in self.check

# Home and Main VIEWS

def home(request):
    return render(request, 'app/home.html')

def films(request):
    film = Film.objects.all()
    return render(request, 'app/films.html', {"films":film})

def bookingPage(request, pk):
    film = Film.objects.get(pk=pk)
    showings = Showing.objects.all().filter(film=film)
    return render(request, 'app/bookingPage.html', {"film": film, "showings": showings})

def aboutUs(request):
    return render(request, 'app/aboutUs.html')

def contactUs(request):
    return render(request, 'app/contactUs.html')

@login_required
@user_passes_test(RoleCheck("STUDENT", "CLUBREP", "CINEMAMAN", "ACCOUNTMAN"))
def roleHomeLink(request):
    role = request.user.role
    if role == "CLUBREP":
        return redirect("crHome")
    elif role == "CINEMAMAN":
        return redirect("cmHome")
    elif role == "ACCOUNTMAN":
        return redirect("amHome")
    elif role == "STUDENT":
        return redirect("sHome")
    
#Login/Register views
def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request=request, data=request.POST)
        
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                role = user.get_role()
                login(request, user)
                if role == "STUDENT":
                    return redirect("home")
                elif role == "CLUBREP":
                    return redirect("crHome")
                elif role == "CINEMAMAN":
                    return redirect("cmHome")
                elif role == "ACCOUNTMAN":
                    return redirect("amHome")
                else:
                    error = "Error no role allocated!"
                    return render(request, "app/login.html", context={"form":form, "error":error})
            else:
                error = "Invalid login credentials!"
                return render(request=request, template_name="registration/login.html", context={"form":form, "error":error})

        else:
            error = "Please enter a username and password!"
            form = AuthenticationForm()
            return render(request=request, template_name="registration/login.html", context={"form":form, "error":error})

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

            newAccount = accountRequest(
                user = form.cleaned_data["username"],
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                psw = password1
            )
            newAccount.save()

            return redirect("home")
        else:
            return render(request, "registration/register.html", {"form":form})

    else:
        form = UserRegistrationForm()
        return render(request=request, template_name="registration/register.html", context={"form":form})

@login_required
def logout_request(request):
    logout(request)
    return redirect("home")


# Customer VIEWS
def customerBooking(request):
    form = CustomerBookingDateForm(request.POST or None)
    dated = False

    if request.method == "POST":
        if form.is_valid():
            
            customerBookingDate = form.cleaned_data["customerBookingDate"]
            try:
                showings = Showing.objects.filter(date=customerBookingDate).order_by("time")
                dated = True
                return render(request, "app/customer/customerBooking.html", {"dated":dated, "showings":showings})
            except:
                return render(request, "app/customer/customerBooking.html", {"form": form, "dated":dated})
        else:
            return render(request, "app/customer/customerBooking.html", {"form": form, "dated":dated})
    else:
        return render(request, "app/customer/customerBooking.html", {"form": form, "dated":dated}) 

def customerConfirmBooking(request, pk):
    form = CustomerBookingQuantity(request.POST or None)
    showing = Showing.objects.get(pk=pk)
    qPicked = False

    if request.method == "POST":
        if form.is_valid():
            qPicked = True
            aq = form.cleaned_data["customerQuantity"]
            cq = form.cleaned_data["customerChildQuantity"]
            sq = form.cleaned_data["customerStudentQuantity"]
            q = aq+cq+sq
            if q >= 1:
                if showing.remainingSeats > q:
                    try:
                        overallCost = ((showing.price*aq)+(showing.price*cq/2)+(showing.price*sq*0.9))
                        return render(request, "app/customer/customerBookingConfirmation.html", {"showing":showing, "q":q, "aq":aq, "cq":cq, "sq":sq, "qPicked":qPicked, "cost":overallCost})
                    except:
                        postConf = True
                        processed = False
                        error = "Not a valid user"
                        return render(request, "app/customer/customerBookingConfirmation.html", {"postConf":postConf, "processed":processed, "error":error})
                else:
                    error = "Insufficient seats to accomodate booking."
                    return render(request, "app/customer/customerBookingConfirmation.html", {"showing":showing, "form":form, "error":error})
            else:
                error = "A minimum of 1 ticket must be selected."
                return render(request, "app/customer/customerBookingConfirmation.html", {"showing":showing, "form":form, "error":error})
        else:
            error = "Quantity selction invalid."
            return render(request, "app/customer/customerBookingConfirmation.html", {"showing":showing, "form":form, "error":error})
    else:
        return render(request, "app/customer/customerBookingConfirmation.html", {"showing":showing, "form":form})


def customerSaveBooking(request, pk, q, aq, cq, sq):
    showing = Showing.objects.get(pk=pk)
    postConf = True
    if showing.remainingSeats > q:
        try:
            overallCost = ((showing.price*aq)+(showing.price*cq/2)+(showing.price*sq*0.9))

            newCustomerBooking = Booking.objects.create(
                showing=showing,
                adultQuantity = aq,
                childQuantity = cq,
                studentQuantity = sq,
                cost = overallCost,
                datetime = datetime.datetime.now()
            )

            showing.remainingSeats = showing.remainingSeats - q

            newCustomerBooking.save()
            showing.save()

            processed = True
            return render(request, "app/customer/customerBookingConfirmation.html", {"postConf":postConf, "processed":processed})
        
        except:
            processed = False
            error = ""
            return render(request, "app/customer/customerBookingConfirmation.html", {"postConf":postConf, "processed":processed, "error":error})

    else:
        processed = False
        error = "Insufficient seats to accomodate booking."
        return render(request, "app/customer/customerBookingConfirmation.html", {"postConf":postConf, "processed":processed, "error":error})


# Student VIEWS
@login_required
@user_passes_test(RoleCheck("STUDENT"))
def sHome(request):
    try:
        student = Student.objects.filter(user=request.user).get()
        club = student.club
        bookings = BlockBooking.objects.all().filter(club=club)
        curbookings = bookings
        # Get current bookings 
        # curbookings = bookings.filter(bookings.datetime>=datetime.datetime.now())
        return render(request, "app/student/sHome.html", {"student":student, "bookings":curbookings})
    except:
        clubs = Club.objects.all()
        return render(request, "app/student/sHome.html", {"clubs":clubs})

@login_required
@user_passes_test(RoleCheck("STUDENT"))
def joinRequest(request, pk):
    form = ClubRequestForm(request.POST or None)
    club = Club.objects.all().filter(id=pk).get()

    if request.method == "POST":
        if form.is_valid():

            msg = form.cleaned_data["message"]
            newClubRequest = clubRequest(
                user = request.user,
                club = club,
                message = msg
            )
            newClubRequest.save()
            
            return render(request, "app/student/confRequest.html")
        else:
            return render(request, "app/student/joinRequest.html", {"club":club, "form":form})
    else:
        return render(request, "app/student/joinRequest.html", {"club":club, "form":form})


# Club Rep VIEWS
@login_required
@user_passes_test(RoleCheck("CLUBREP"))
def crHome(request):
    try:
        clubrep = ClubRep.objects.filter(user=request.user).get()
        error = ""
        return render(request, "app/clubrep/crHome.html", {"clubrep":clubrep, "error":error})
    except:
        error = "ClubRep profile not found!"
        return render(request, "app/clubrep/crHome.html", {"error":error})

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
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

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
def clubBooking(request):
    form = BookingDateForm(request.POST or None)
    dated = False

    if request.method == "POST":
        if form.is_valid():

            bookingDate = form.cleaned_data["bookingDate"]
            try:
                showings = Showing.objects.filter(date=bookingDate).order_by("time")
                dated = True
                return render(request, "app/clubrep/blockBooking.html", {"dated":dated, "showings":showings})
            except:
                return render(request, "app/clubrep/blockBooking.html", {"form": form, "dated":dated})
        else:
            return render(request, "app/clubrep/blockBooking.html", {"form": form, "dated":dated})
    else:
        return render(request, "app/clubrep/blockBooking.html", {"form": form, "dated":dated})

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
def confirmBooking(request, pk):
    form = BlockBookingQuantity(request.POST or None)
    showing = Showing.objects.get(pk=pk)
    qPicked = False

    if request.method == "POST":
        if form.is_valid():
            qPicked = True
            q = form.cleaned_data["quantity"]
            if q >= 10:    
                if showing.remainingSeats > q:
                    try:
                        user = request.user
                        rep = ClubRep.objects.filter(user=user).get()
                        club = rep.club
                        afterDiscount = 100-club.discount
                        overallCost = ((showing.price*q)/100)*afterDiscount
                        return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "q":q, "qPicked":qPicked, "cost":overallCost})
                    except:
                        postConf = True
                        processed = False
                        error = "Error: Club account not found."
                        return render(request, "app/clubrep/blockBookingConfirmation.html", {"postConf": postConf, "processed":processed, "error":error}) 
                else:
                    error = "Insufficient seats to accomodate booking."
                    return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "form":form, "error":error})
            else:
                error = "A minimum of 10 tickets must be selected."
                return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "form":form, "error":error})
        else:
            error = "Quantity selection invalid."
            return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "form":form, "error":error})
    else:
        return render(request, "app/clubrep/blockBookingConfirmation.html", {"showing":showing, "form":form})

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
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
                showing=showing,
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

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
def crPending(request):
    try:
        rep = ClubRep.objects.all().filter(user=request.user).get()
        myclub = rep.club
        clubRequests = clubRequest.objects.all().filter(club=myclub)
        return render(request, "app/clubrep/pendingRequests.html", {"clubrequests":clubRequests})
    except:
        return render(request, "app/clubrep/pendingRequests.html")

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
def acceptClubRequest(request, pk):
    clubreq = clubRequest.objects.all().filter(pk=pk).get()
    user = clubreq.user
    club = clubreq.club

    newStudent = Student(
        user = user,
        club = club
    )
    newStudent.save()
    clubreq.delete()
    
    return redirect("crPending")

@login_required
@user_passes_test(RoleCheck("CLUBREP"))
def declineClubRequest(request, pk):
    clubreq = clubRequest.objects.all().filter(pk=pk).get()
    clubreq.delete()
    return redirect("crPending")

# Cinema Manager VIEWS
@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def cmHome(request):
    films = Film.objects.all()
    screens = Screen.objects.all()
    showings = Showing.objects.all()
    clubs = Club.objects.all()
    return render(request, "app/cinemamanager/cmHome.html", {"films" : films, "screens" : screens, "showings" : showings, "clubs" : clubs})

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def addFilm(request):
    if request.method == "POST":
        form = addFilmForm(request.POST, request.FILES or None) 
        if form.is_valid():
            filmTitle = form.cleaned_data["title"]
            filmRating = form.cleaned_data["ageRatings"]
            filmDuration = form.cleaned_data["duration"]
            filmDescription = form.cleaned_data["desc"]
            filmImagePoster = form.cleaned_data["filmImage"]

            Film.objects.create(title=filmTitle, ageRatings=filmRating,duration=filmDuration, desc=filmDescription, filmImage=filmImagePoster)
            print(Film)
            return redirect("cmHome")
        else:
            form = addFilmForm()
            print(form.errors)
            return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})
    else:
        form = addFilmForm()
        return render(request, "app/cinemamanager/cmAddFilm.html", {"form": form})

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def deleteFilm(request, pk):
    if request.method == "POST":
        film = Film.objects.get(pk=pk)
        try:
            showing = Showing.objects.all().filter(film=film)
            return redirect('cmHome')
        except:
            film.delete()
            return redirect('cmHome')
    else:
        return redirect('cmHome')

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
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

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
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
            return render(request, "app/cinemamanager/cmRegisterClub.html", {"form": form})
    else:
        return render(request, "app/cinemamanager/cmRegisterClub.html", {"form": form})

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def registerClubRep(request):
    club = Club.objects.all()
    user = User.objects.all()
    form = registerClubRepForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            userName = form.cleaned_data['user']
            RepsClub = form.cleaned_data['club']
            ClubRep.objects.create(user=userName, club=RepsClub)
            print(ClubRep)
            return redirect('cmHome')
        else:
            return render(request, "app/cinemamanager/cmRegisterClubRep.html", {"form" : form})
    else:
        return render(request, "app/cinemamanager/cmRegisterClubRep.html", {"form" : form})

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def deleteClub(request, pk):
    if request.method == "POST":
        club = Club.objects.get(pk=pk)
        club.delete()   
        club.address.delete()
        club.contact.delete()
        club.payment.delete()
    
        return redirect('cmHome')
    else:
        return redirect('cmHome')

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def updateClub(request,pk):
    club = Club.objects.get(pk=pk)
    if request.method == "POST":
        form = RegisterClubForm(request.POST)
        if form.is_valid():
            club.name = form.cleaned_data['clubname']
            club.discount = form.cleaned_data['discount']
            club.address.street = form.cleaned_data['aStreet']
            club.address.city = form.cleaned_data['aCity']
            club.address.postCode = form.cleaned_data['aPostCode']
            club.contact.landline = form.cleaned_data['cLandline']
            club.contact.mobile = form.cleaned_data['cMobile']
            club.contact.email = form.cleaned_data['cEmail']
            club.contact.firstName = form.cleaned_data['cFirstName']
            club.contact.surName = form.cleaned_data['cSurName']
            club.payment.cardNumber = form.cleaned_data['pCardNumber']
            club.payment.expiryDate = form.cleaned_data['pExpiryDate']
            club.save()
            club.contact.save()
            club.address.save()
            club.payment.save()
            return redirect("cmHome")
    else:
        dataPopulation = {
            'clubid' : club.clubid,
            'clubname' : club.name,
            'discount' : club.discount,
            'aNumber' : club.address.number,
            'aStreet' : club.address.street,
            'aCity' : club.address.city,
            'aPostCode' : club.address.postCode,
            'cLandline' : club.contact.landline,
            'cMobile' : club.contact.mobile,
            'cEmail' : club.contact.email,
            'cFirstName' : club.contact.firstName,
            'cSurName' : club.contact.surName,
            'pCardNumber' : club.payment.cardNumber,
            'pExpiryDate' : club.payment.expiryDate
        }
        form = RegisterClubForm(initial=dataPopulation)
    return render(request, "app/cinemamanager/cmUpdateDetails.html", {'form':form})

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
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

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def deleteScreen(request, pk):
    if request.method == "POST":
        screen = Screen.objects.get(pk=pk)
        try:
            showing = Showing.objects.all().filter(screen=screen)
            return redirect('cmHome')
        except:
            screen.delete()
            return redirect('cmHome')
    else:
        return redirect('cmHome')

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
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

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def addShowing(request):
    form = addShowingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            showing = Showing.objects.create(
                film=form.cleaned_data['film'],
                screen=form.cleaned_data['screen'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                price = form.cleaned_data["price"],
                remainingSeats=form.cleaned_data['screen'].capacity
            )
            
            return redirect('cmHome')
        else:
            return render(request, 'app/cinemamanager/cmAddShowing.html', {'form' : form})
    else:
        return render(request, 'app/cinemamanager/cmAddShowing.html', {'form' : form})

@login_required
@user_passes_test(RoleCheck("CINEMAMAN")) 
def deleteShowing(request, pk):
    if request.method == "POST":
        screen = Showing.objects.get(pk=pk)
        screen.delete()
        return redirect('cmHome')
    else:
        return redirect('cmHome')

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
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

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def cmPending(request):
    try:
        requests = accountRequest.objects.all()
        print(requests)
        return render(request, "app/cinemamanager/pendingRequests.html", {"userrequests":requests})
    except:
        return render(request, "app/cinemamanager/pendingRequests.html")

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def acceptAccountRequest(request, pk):
    accreq = accountRequest.objects.all().filter(pk=pk).get()
    User.objects.create_user(username=accreq.user, 
                             password=accreq.psw, 
                             first_name = accreq.first_name, 
                             last_name = accreq.last_name, 
                             role=User.Role.STUDENT)
    accreq.delete()
    return redirect("cmPending")

@login_required
@user_passes_test(RoleCheck("CINEMAMAN"))
def declineAccountRequest(request, pk):
    accreq = accountRequest.objects.all().filter(pk=pk).get()
    accreq.delete()
    return redirect("cmPending")

# Account Manager VIEWS
@login_required
@user_passes_test(RoleCheck("ACCOUNTMAN"))
def amHome(request):
    # students = Student.objects.all()
    users = User.objects.all()
    clubReps = ClubRep.objects.all()
    clubs = Club.objects.all()
    return render(request, "app/accountmanager/amHome.html", {"users" : users, "clubReps" : clubReps, "clubs" : clubs})

@login_required
@user_passes_test(RoleCheck("ACCOUNTMAN"))
def ViewDetails(request, pk):
    clubRep = ClubRep.objects.get(pk=pk)
    user = User.objects.get(pk=pk)
    
    return render(request, 'app/accountmanager/amViewDetails.html', { "clubRep" : clubRep, "user" : user})

@login_required
@user_passes_test(RoleCheck("ACCOUNTMAN"))
def ClubDetails(request, pk):
    club = Club.objects.get(pk=pk)
    students = Student.objects.all()
    clubReps = ClubRep.objects.all()
    if request.method == "POST":
        form = RegisterClubForm(request.POST)
        if form.is_valid():
            club.name = form.cleaned_data['clubname']
            club.discount = form.cleaned_data['discount']
            club.address.street = form.cleaned_data['aStreet']
            club.address.city = form.cleaned_data['aCity']
            club.address.postCode = form.cleaned_data['aPostCode']
            club.contact.landline = form.cleaned_data['cLandline']
            club.contact.mobile = form.cleaned_data['cMobile']
            club.contact.email = form.cleaned_data['cEmail']
            club.contact.firstName = form.cleaned_data['cFirstName']
            club.contact.surName = form.cleaned_data['cSurName']
            club.payment.cardNumber = form.cleaned_data['pCardNumber']
            club.payment.expiryDate = form.cleaned_data['pExpiryDate']
            club.save()
            club.contact.save()
            club.address.save()
            club.payment.save()
            return redirect("cmHome")
    else:
        dataPopulation = {
            'clubid' : club.clubid,
            'clubname' : club.name,
            'discount' : club.discount,
            'aNumber' : club.address.number,
            'aStreet' : club.address.street,
            'aCity' : club.address.city,
            'aPostCode' : club.address.postCode,
            'cLandline' : club.contact.landline,
            'cMobile' : club.contact.mobile,
            'cEmail' : club.contact.email,
            'cFirstName' : club.contact.firstName,
            'cSurName' : club.contact.surName,
            'pCardNumber' : club.payment.cardNumber,
            'pExpiryDate' : club.payment.expiryDate
        }
        form = RegisterClubForm(initial=dataPopulation)
    return render(request, 'app/accountmanager/amClubDetails.html', { "club" : club, "students" : students, "clubReps" : clubReps, "form" : form})

@login_required
@user_passes_test(RoleCheck("ACCOUNTMAN"))
def deleteAccount(request, pk):
    users = User.objects.get(pk=pk)
    if request.method == "POST":
        users.delete()
        return redirect('cmHome')
    else:
        return redirect('cmHome')

@login_required
@user_passes_test(RoleCheck("ACCOUNTMAN"))
def generate_ms(request):
    pass