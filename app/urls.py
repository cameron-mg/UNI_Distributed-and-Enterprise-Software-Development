from django.urls import path
from app import views

urlpatterns = [
    #Home & Main URLS
    path("", views.home, name="home"),
    path("films/", views.films, name="films"),
    path("aboutUs/", views.aboutUs, name="aboutUs"),
    path("contactus/", views.contactUs, name="contactUs"),
    path("roleHomeLink/", views.roleHomeLink, name="roleHomeLink"),

    # Login/Register URLS
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("register/", views.register_request, name="register"),

    # Customer URLS
    path("cHome/", views.cHome, name="cHome"),
    path("showings/", views.showings, name="showings"),
    path("showDetails/<showing_id>/", views.showDetails, name="showDetails"),
    path("bookingPage/<int:pk>/", views.bookingPage, name="bookingPage"),
    
    # Student URLS
    path("s/", views.sHome, name="sHome"),
    path("s/joinRequest/<int:pk>", views.joinRequest, name="joinRequest"),

    # Club Rep URLS
    path("cr/home/", views.crHome, name="crHome"),
    path("cr/clubAccount/", views.clubAccount, name="clubAccount"),
    path("cr/clubBooking/", views.clubBooking, name="clubBooking"),
    path("cr/clubBooking/confirmation/<int:pk>/", views.confirmBooking, name="confirmBooking"),
    path("cr/clubBooking/confirmation/<int:pk>/<int:q>", views.saveClubBooking, name="saveClubBooking"),
    path("cr/pending/", views.crPending, name="crPending"),
    path("cr/pending/accept/<int:pk>", views.acceptClubRequest, name="acceptClubRequest"),
    path("cr/pending/decline/<int:pk>", views.declineClubRequest, name="declineClubRequest"),

    # Cinema Manager URLS
    path("cm/home/", views.cmHome, name="cmHome"),
    path("cm/registerClub/", views.registerClub, name="registerClub"),

    path("cm/registerClubRep", views.registerClubRep, name="registerClubRep"),
    path("cm/updateClub/<int:pk>/", views.updateClub, name="updateClub"),
    path("cm/deleteClub/<int:pk>/", views.deleteClub, name="deleteClub"),

    path("cm/AddFilm/", views.addFilm, name="cmAddFilm"),
    path("cm/updateFilm/<int:pk>/", views.updateFilm, name="updateFilm"),
    path("cm/deleteFilm/<int:pk>/", views.deleteFilm, name="deleteFilm"),

    path("cm/AddScreen/", views.addScreen, name="cmAddScreen" ),
    path("cm/updateScreen/<int:pk>/,", views.updateScreen, name="updateScreen"),
    path("cm/deleteScreen/<int:pk>/", views.deleteScreen, name="deleteScreen"),

    path("cm/AddShowing", views.addShowing, name="cmAddShowing"),
    path("cm/updateShowing/<int:pk>/", views.updateShowing, name="updateShowing"),
    path("cm/deleteShowing/<int:pk>/", views.deleteShowing, name="deleteShowing"),

    path("cm/pending/", views.cmPending, name="cmPending"),

    # Account Manager URLS
    path("am/", views.amHome, name="amHome"),
    path("am/ViewDetails/<int:pk>", views.ViewDetails, name="ViewDetails"),
    path("am/UpdateDetails", views.UpdateDetails, name="UpdateDetails")
]