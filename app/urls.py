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
    path("registerClubRep", views.registerClubRep, name="registerClubRep"),
    path("deleteClub/<int:pk>", views.deleteClub, name="deleteClub"),
    path("updateClub/<int:pk>", views.updateClub, name="updateClub"),
    path("cmAddFilm/", views.addFilm, name="cmAddFilm"),
    path("updateFilm/<int:pk>", views.updateFilm, name="updateFilm"),
    path("cmHome/", views.cmHome, name="cmHome"),
    path("deleteFilm/<int:pk>/", views.deleteFilm, name="deleteFilm"),
    path("cmAddScreen/", views.addScreen, name="cmAddScreen" ),
    path("updateScreen/<int:pk>,", views.updateScreen, name="updateScreen"),
    path("deleteScreen/<int:pk>", views.deleteScreen, name="deleteScreen"),
    path("cmAddShowing", views.addShowing, name="cmAddShowing"),
    path("deleteShowing/<int:pk>/", views.deleteShowing, name="deleteShowing"),
    path("updateShowing/<int:pk>/", views.updateShowing, name="updateShowing"),
    
    # CR URLS

    # JD URLS
    
]