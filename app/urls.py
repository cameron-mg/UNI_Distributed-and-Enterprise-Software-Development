from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("clubrephome/", views.clubrephome, name="clubrephome"),
    path("registerClub/", views.registerClub, name="registerClub")
]