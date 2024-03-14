# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CabIdleTimeView, HighDemandCitiesView
from . import views

router = DefaultRouter()
router.register(r'cities', views.CityViewSet)
# router.register(r'cabs/logs', views.CabAudit)
router.register(r'cabs', views.CabViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('cabs/<id>/idle', CabIdleTimeView.as_view(), name='cab_idle_time'),
    path('city/demand', HighDemandCitiesView.as_view(), name='high_Demand_time'),
    path('bookings/book', views.book),
    path('bookings/<id>/end', views.end),
    path('', include(router.urls))
    
]
