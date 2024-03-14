from django.contrib import admin

# Register your models here.

from django.contrib import admin
from main.models import City, Cab, Bookings


class CityAdmin(admin.ModelAdmin):
    pass


class CabAdmin(admin.ModelAdmin):
    pass

class BookingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(City, CityAdmin)
admin.site.register(Cab, CabAdmin)
admin.site.register(Bookings, BookingsAdmin)