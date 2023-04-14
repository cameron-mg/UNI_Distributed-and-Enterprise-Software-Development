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

    # Login/register URLS
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("register/", views.register_request, name="register"),

    # CMG URLS
    path("crHome/", views.crHome, name="crHome"),
    path("clubAccount/", views.clubAccount, name="clubAccount"),
    path("clubBooking/", views.clubBooking, name="clubBooking"),
    path("clubBooking/confirmation/<int:pk>", views.confirmBooking, name="confirmBooking"),
    path("clubBooking/confirmation/<int:pk>/<int:q>", views.saveClubBooking, name="saveClubBooking"),

    # TW URLS
    path("cmHome/", views.cmHome, name="cmHome"),
    path("registerClub/", views.registerClub, name="registerClub"),

    path("registerClubRep", views.registerClubRep, name="registerClubRep"),
    path("updateClub/<int:pk>", views.updateClub, name="updateClub"),
    path("deleteClub/<int:pk>", views.deleteClub, name="deleteClub"),

    path("cmAddFilm/", views.addFilm, name="cmAddFilm"),
    path("updateFilm/<int:pk>", views.updateFilm, name="updateFilm"),
    path("deleteFilm/<int:pk>/", views.deleteFilm, name="deleteFilm"),

    path("cmAddScreen/", views.addScreen, name="cmAddScreen" ),
    path("updateScreen/<int:pk>,", views.updateScreen, name="updateScreen"),
    path("deleteScreen/<int:pk>", views.deleteScreen, name="deleteScreen"),

    path("cmAddShowing", views.addShowing, name="cmAddShowing"),
    path("updateShowing/<int:pk>/", views.updateShowing, name="updateShowing"),
    path("deleteShowing/<int:pk>/", views.deleteShowing, name="deleteShowing"),
    
    # CR URLS

    # JD URLS
]