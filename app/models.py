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

    # base_role = Role.CUSTOMER

    role = models.CharField(max_length=50, choices=Role.choices)

    # def save(self, *args, **kwargs):
    #     self.role = self.role
    #     return super().save(*args, **kwargs)
        
    def get_role(self):
        return self.role
    
    REQUIRED_FIELDS = ["role"]


# Multiple Role Access
class Address(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    number = models.CharField(max_length=4)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postCode = models.CharField(max_length=8)

class Contact(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    landline = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    firstName = models.CharField(max_length=20)
    surName = models.CharField(max_length=50)

class Payment(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    cardNumber = models.CharField(unique=True, max_length=19)
    expiryDate = models.DateField()


# Cinema Manager
class Film(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    title = models.CharField(max_length=50)
    ageRating = models.IntegerField()
    duration = models.IntegerField()
    desc = models.CharField(max_length=150)

class Screen(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    capacity = models.IntegerField()

class Showing(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    date = models.DateField() # ***CHECK***
    time = models.TimeField() # ***CHECK***


# Account Manager
class Employee(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    initial = models.CharField(max_length=1)
    surname = models.CharField(max_length=50)


# Customer
class Booking(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    tickettype = models.CharField(max_length=10)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    cost = models.IntegerField()
    datetime = models.DateTimeField() # ***CHECK***


# Club Representative
class Club(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    name = models.CharField(max_length=30)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    discount = models.IntegerField()
    balance = models.IntegerField()

class ClubRep(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=8)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

class Transaction(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=6)
    account = models.ForeignKey(Club, on_delete=models.CASCADE)
    amount = models.IntegerField()
    datetime = models.DateTimeField() # ***CHECK***

class BlockBooking(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    quantity = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    cost = models.IntegerField()
    datetime = models.DateTimeField() # ***CHECK***