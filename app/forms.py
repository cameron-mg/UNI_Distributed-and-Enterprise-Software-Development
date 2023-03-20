from django import forms
from app.models import User, Club

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


class registerClub(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("id", "name", "address", "contact", "payment", "discount", "balance",)
