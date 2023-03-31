from django.urls import path
from app import views

urlpatterns = [
    #Home & Films URLS
    path("", views.home, name="home"),
    path("films/", views.films, name="films"),

    # Showings URLS
    path("showings/", views.showings, name="showings"),
    path("showDetails/<showing_id>", views.showDetails, name="showDetails"),

    # About Us & Contact Us URLS
    path("aboutUs/", views.aboutUs, name="aboutUs"),
    path("contactus/", views.contactUs, name="contactUs"),

    #Booking/payment URLS

    # Login/register URLS
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),

    # CMG URLS
    path("crHome/", views.crHome, name="crHome"),
    path("clubAccount/", views.clubAccount, name="clubAccount"),
    path("clubBooking/", views.blockBooking, name="clubBooking"),

    # TW URLS
    path("registerClub/", views.registerClub, name="registerClub"),
    path("cmAddFilm/", views.addFilm, name="cmAddFilm"),
    path("cmHome/", views.cmHome, name="cmHome"),

    # CR URLS

    # JD URLS
    
]