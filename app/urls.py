from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    # CMG URLS
    path("clubrephome/", views.clubrephome, name="clubrephome"),
    # TW URLS
    path("registerClub/", views.registerClub, name="registerClub")
    # CR URLS

    # JD URLS
    
]