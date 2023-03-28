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

class addScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ("screenNo", "capacity")
        widgets = {
            'screenNo' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'capacity' : forms.NumberInput(attrs={'class' : 'form-control'})
        }

class addShowingForm(forms.ModelForm):
    film = forms.ModelChoiceField(queryset=Film.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}))
    screen = forms.ModelChoiceField(queryset=Screen.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-control', 'type' : 'date'}), input_formats=['%Y-%m-%d'])
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class' : 'form-control', 'type' : 'time'}), input_formats=['%H:%M'])
    remainingSeats = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Showing
        fields = ('film', 'screen', 'date', 'time', 'remainingSeats')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['film'].queryset = Film.objects.all()
        self.fields['screen'].queryset = Screen.objects.all()

    