from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import date
import uuid
from django.contrib import admin


class ServiceType(models.Model):
    name = models.CharField(max_length=122)
    tag = models.CharField(max_length=50, default='NA')

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ServicePage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=122)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    header = models.CharField(max_length=122)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.TextField(default='', blank=True, null=True)
    state = models.TextField(default='')
    featured_package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    organizer = models.CharField(max_length=122, default='')

    def __str__(self):
        return self.title


class Weddingbooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_page = models.ForeignKey(ServicePage, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    featured_package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.service_page.title} Booking in the name of {self.customer} on {self.date_booked}'



