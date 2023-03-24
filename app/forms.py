from django import forms
from app.models import *

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")


class registerClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("name", "address", "contact", "payment", "discount", "balance",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'payment': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.TextInput(attrs={'class': 'form-control'})
        }

class addFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ("title", "ageRatings", "duration", "desc")
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'ageRatings': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'})
        }
