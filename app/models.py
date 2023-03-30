from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager, PermissionsMixin

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        CLUBREP = "CLUBREP", "Club Representative"
        ACCOUNTMAN = "ACCOUNTMAN", "Account Manager"
        CINEMAMAN = "CINEMAMAN", "Cinema Manager"

    role = models.CharField(max_length=50, choices=Role.choices)
        
    def get_role(self):
        return self.role
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    REQUIRED_FIELDS = ["role"]


# Multiple Role Access
class Address(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    number = models.CharField(max_length=4)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postCode = models.CharField(max_length=8)

class Contact(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    landline = models.CharField(max_length=12)
    mobile = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    firstName = models.CharField(max_length=20)
    surName = models.CharField(max_length=50)

class Payment(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    cardNumber = models.CharField(unique=True, max_length=19)
    expiryDate = models.CharField(max_length=5)


# Cinema Manager
class Film(models.Model):
    class ageRating(models.TextChoices):
        U= "U","U"
        PG= "PG", "PG"
        T= "12","12"
        TA= "12A", "12A"
        FT= "15", "15"
        ET = "18", "18" 
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    ageRatings = models.CharField(max_length=3, choices=ageRating.choices, default='12')
    duration = models.IntegerField()
    desc = models.CharField(max_length=150)

class Screen(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    screenNo = models.IntegerField()
    capacity = models.IntegerField()

class Showing(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    date = models.DateField() # ***CHECK***
    time = models.TimeField() # ***CHECK***
    remainingSeats = models.IntegerField()

# Account Manager
class Employee(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    initial = models.CharField(max_length=1)
    surname = models.CharField(max_length=50)


# Customer
class Booking(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    tickettype = models.CharField(max_length=10)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    cost = models.IntegerField()

# Club Representative
class Club(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    clubid = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    discount = models.IntegerField()
    balance = models.IntegerField()

class ClubRep(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)

class Transaction(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    account = models.ForeignKey(Club, on_delete=models.CASCADE)
    madeby = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    cost = models.IntegerField()
    datetime = models.DateTimeField()

class BlockBooking(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    quantity = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    cost = models.IntegerField()
    datetime = models.DateTimeField()
