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
    # CR URLS

    # JD URLS
    
    
]