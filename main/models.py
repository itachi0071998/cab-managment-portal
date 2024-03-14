from django.db import models 
from auditlog.registry import auditlog

class LowerCase(models.Transform):
    lookup_name = "lower"
    function = "LOWER"

models.CharField.register_lookup(LowerCase)

class City(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name
    

class Cab(models.Model):
    CAB_STATES = (
        ('IDLE', 'IDLE'),
        ('ON_TRIP', 'ON_TRIP')
    )
    number = models.CharField(max_length=255, unique=True)
    state = models.CharField(choices=CAB_STATES,max_length=10, null=False, blank=False, default='IDLE')
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

auditlog.register(Cab)

class Bookings(models.Model):
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    