from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    # CMG URLS
    path("clubAccount/", views.clubAccount, name="clubAccount"),
    # TW URLS
    path("registerClub/", views.registerClub, name="registerClub"),
    path("cmAddFilm/", views.addFilm, name="cmAddFilm"),
    path("cmHome/", views.cmHome, name="cmHome"),
    path("deleteFilm/<int:pk>/", views.deleteFilm, name="deleteFilm"),
    path("cmAddScreen/", views.addScreen, name="cmAddScreen" ),
    path("deleteScreen/<int:pk>", views.deleteScreen, name="deleteScreen"),
    path("cmAddShowing", views.addShowing, name="cmAddShowing"),
    path("deleteShowing/<int:pk>", views.deleteShowing, name="deleteShowing")
    # CR URLS

    # JD URLS
    
    
]