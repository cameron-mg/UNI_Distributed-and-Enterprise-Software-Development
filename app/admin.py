from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Payment)
admin.site.register(Film)
admin.site.register(Screen)
admin.site.register(Showing)
admin.site.register(Employee)
admin.site.register(Booking)
admin.site.register(Club)
admin.site.register(ClubRep)
admin.site.register(Transaction)
admin.site.register(BlockBooking)
admin.site.register(clubRequest)
admin.site.register(Student)
# admin.site.register(clubRequest)
admin.site.register(accountRequest)

admin.site.register(User)