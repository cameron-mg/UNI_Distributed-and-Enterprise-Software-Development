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
    path("deleteFilm/<int:film_id>", views.deleteFilm, name="deleteFilm"),
    path("cmAddScreen/", views.addScreen, name="cmAddScreen" ),
    # CR URLS

    # JD URLS
    
    
]