from django.db import models

# Create your models here.

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
    cardNumber = models.CharField(primary_key=True, unique=True, max_length=16)
    expiryDate = models.CharField(max_length=4)



# Cinema Manager
class Film(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    title = models.CharField(max_length=50)
    ageRating = models.IntegerField(max_length=2)
    duration = models.IntegerField(max_length=3)
    desc = models.CharField(max_length=150)

class Screen(models.Model):
    id = models.CharField(max_length=2)
    capacity = models.IntegerField(max_length=4)

class Showing(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    film = models.ForeignKey(Film)
    screen = models.ForeignKey(Screen)
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
    payment = models.ForeignKey(Payment)
    cost = models.IntegerField(max_length=3)
    datetime = models.DateTimeField() # ***CHECK***



# Club Representative
class Club(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    name = models.CharField(max_length=30)
    address = models.ForeignKey(Address)
    contact = models.ForeignKey(Contact)
    payment = models.ForeignKey(Payment)
    discount = models.IntegerField(max_length=2)
    balance = models.IntegerField(max_length=4)

class ClubRep(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=8)
    club = models.ForeignKey(Club)
    password = models.CharField(unique=True, max_length=8)
    contact = models.ForeignKey(Contact)

class Transaction(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=6)
    account = models.ForeignKey(Club)
    amount = models.IntegerField(max_length=4)
    datetime = models.DateTimeField() # ***CHECK***

class BlockBooking(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=3)
    quantity = models.IntegerField(max_length=2)
    payment = models.ForeignKey(Payment)
    cost = models.IntegerField(max_length=3)
    datetime = models.DateTimeField() # ***CHECK***