from django import forms
from app.models import User, Club
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username",)


class registerClub(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("id", "name", "address", "contact", "payment", "discount", "balance",)
