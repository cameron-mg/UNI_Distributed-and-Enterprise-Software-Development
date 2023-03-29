from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
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