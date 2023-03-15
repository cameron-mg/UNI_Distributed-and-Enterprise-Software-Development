from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    
    # CMG URLS

    # TW URLS
    path("registerClub/", views.registerClub, name="registerClub"),
    # CR URLS

    # JD URLS
    
    
]