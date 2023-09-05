from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class busRoute(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Passenger(models.Model):
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=10)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, default=None, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class bookTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 'Vehicle' is use because Vehicle model is created below this class
    # User is directly imported on the top so no need to use ''.
    vehicle_id = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='vehicleid')
    booked_ticket = models.IntegerField(default=0)
    ticketNumber = models.IntegerField(default=0000)
    cost = models.IntegerField(null=True)
    ticket_status = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    # def __str__ (self):
    #     return self.user


class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=15)
    source = models.CharField(max_length=50, null=True)
    destination = models.CharField(max_length=50, null=True)
    date = models.DateField(null=True)
    v_status = models.BooleanField(default=True)
    departure = models.TimeField(null=True, blank=True)
    arrive = models.TimeField(null=True, blank=True)
    total_seats = models.IntegerField(default=0)
    booked_seats = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
