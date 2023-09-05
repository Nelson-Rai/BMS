from django.contrib import admin

# Register your models here.

from .models import busRoute, Passenger, Vehicle, bookTicket

admin.site.register(busRoute)
admin.site.register(Passenger)
admin.site.register(Vehicle)
admin.site.register(bookTicket)