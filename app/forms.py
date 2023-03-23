from django import forms
from app.models import User, Club

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


class registerClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ("id", "name", "address", "contact", "payment", "discount", "balance",)
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
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
        fields = ("title", "ageRating", "duration", "desc",)
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'ageRating': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'})
        }
