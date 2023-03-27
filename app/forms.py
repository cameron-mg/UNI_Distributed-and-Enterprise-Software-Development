from django import forms
from app.models import *

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


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

class addScreeningForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ("screenNo", "capacity")
        widgets = {
            'screenNo' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'capacity' : forms.NumberInput(attrs={'class' : 'form-control'})
        }