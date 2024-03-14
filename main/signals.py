# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Cab

# @receiver(pre_save, sender=Booking)
# def update_cab_state(sender, instance, **kwargs):
#     # Update Cab state to BUSY when a Booking object is created
#     if kwargs.get('created', False):
#         if(instance.cab.state != "IDLE"):

#         instance.cab.state = 'BOOKED'
#         instance.cab.save()
