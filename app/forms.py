from django import forms
from app.models import *
# from PIL import Image
from django.utils.html import format_html

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")

class ClubAccountForm(forms.Form):
    clubid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20, label="Club Identification Number")

class BookingDateForm(forms.Form):
    bookingDate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type' : 'date'}), input_formats=['%Y-%m-%d'], label="Booking Date")

class BlockBookingQuantity(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Quantity")

class RegisterClubForm(forms.Form):
    clubid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=8, label="Club ID")
    clubname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30, label="Club Name")
    discount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Discount")

    aNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=4, label="Address Number")
    aStreet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="Street")
    aCity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="City")
    aPostCode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=8, label="Postcode")

    cLandline = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=12, label="Landline")
    cMobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=12, label="Mobile")
    cEmail = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="Email")
    cFirstName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20, label="First Name")
    cSurName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="Surname")

    pCardNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=19, label="Card Number")
    pExpiryDate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Expiry Date (MM/YY)")

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("number", "street", "city", "postCode")
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postCode': forms.TextInput(attrs={'class': 'form-control'})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("landline", "mobile", "email", "firstName", "surName")
        widgets = {
            'landline': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'surName': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("cardNumber", "expiryDate")
        widgets = {
            'cardNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'expiryDate': forms.TextInput(attrs={'class': 'form-control'})
        }

class registerClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = ('user', 'club')
        widgets ={
            'user' : forms.Select(attrs={'class' : 'form-control'}),
            'club' : forms.Select(attrs={'class' : 'form-control'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club'].queryset= Club.objects.all()
        self.fields['user'].querysdet= User.objects.all()
        self.fields['club'].label_from_instance = lambda obj : obj.name
        self.fields['user'].label_from_instance = lambda obj : obj.username
    

class addFilmForm(forms.ModelForm):


    filmImage = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Film
        fields = ("title", "ageRatings", "duration", "desc","filmImage")
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
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Price Without Discount")

    class Meta:
        model = Showing
        fields = ('film', 'screen', 'date', 'time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['film'].queryset = Film.objects.all()
        self.fields['screen'].queryset = Screen.objects.all()
        self.fields['film'].label_from_instance = lambda obj: obj.title
        self.fields['screen'].label_from_instance = lambda obj: obj.screenNo

class CustomerBookingDateForm(forms.Form):
    customerBookingDate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), input_formats=['%Y-%m-%d'], label="Booking Date")

class CustomerBookingQuantity(forms.Form):
    customerQuantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Adult Quantity")
    customerChildQuantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Child Quantity")
    customerStudentQuantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Student Quantity")

# class CustomerTicketType(forms.Form):
#     tickettype = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=10, label="Ticket Type")

class ClubRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Message") 


class UserDetailsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)

class AddClubAccountForm(forms.Form):
    clubid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=8, label="Club ID")
    clubname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30, label="Club Name")
    discount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Discount")

    aNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=4, label="Address Number")
    aStreet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="Street")
    aCity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="City")
    aPostCode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=8, label="Postcode")

    cLandline = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=12, label="Landline")
    cMobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=12, label="Mobile")
    cEmail = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="Email")
    cFirstName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20, label="First Name")
    cSurName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label="Surname")

    pCardNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=19, label="Card Number")
    pExpiryDate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Expiry Date (MM/YY)")
