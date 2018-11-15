from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

# basic info
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    altitude = models.DecimalField(max_digits=6, decimal_places=0) # m

    def __str__(self):
        return f'{self.name}'

class Distance(models.Model):
    start = models.ForeignKey(Location, related_name='location_start', on_delete=models.CASCADE)
    end = models.ForeignKey(Location, related_name='location_end', on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=8, decimal_places=2) # km

    def __str__(self):
        return f'{self.start}--{self.end}: {self.distance}'

class MedicineSupply(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    hospital = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='supply')

    def __str__(self):
        return f'{self.name}'

# role info
class ClinicManager(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    #password = models.CharField(max_length=200)
    #first_name = models.CharField(max_length=200)
    #last_name = models.CharField(max_length=200)
    #email = models.CharField(max_length=200)


    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name}'



class Dispatcher(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

# order
class Order(models.Model):
    # this value is for 'status'
    STATUS_CHOICES =\
    (
        ('QP', 'Queued for Processing'),
        ('PW', 'Processing by Warehouse'),
        ('QD', 'Queued for Dispatch'),
        ('DI', 'Dispatched'),
        ('DE', 'Delivered'),
    )

    PRIORITY_CHOICES =\
    (
        ('3', 'High'),
        ('2', 'Medium'),
        ('1', 'Low'),
    )

    id = models.AutoField(primary_key=True)
    clinic_manager = models.ForeignKey(ClinicManager, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    items = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2) # kg
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='3')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='QP')
    timeQP = models.DateTimeField()
    timePW = models.DateTimeField(null=True)
    timeQD = models.DateTimeField(null=True)
    timeDI = models.DateTimeField(null=True)
    timeDE = models.DateTimeField(null=True)

    def __str__(self):
        return f'order from {self.clinic_manager} (NO.{self.id})'