from django import forms
from app import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class registerClub(forms.ModelForm):
    class Meta:
        model = models.Club
        fields = ("id", "name", "address", "contact", "payment", "discount", "balance",)
