from django.shortcuts import get_object_or_404,render
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, F, Value, Count, Max
from django.db.models.functions import Coalesce
from django.utils.dateparse import parse_datetime

import datetime

from django.db import connection
from .models import City, Cab, Bookings
from .serializers import CitySerializer, CabUpdateSerializer, CabSerializer, BookingSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from django.views.generic import DetailView
from auditlog.mixins import LogAccessMixin
from rest_framework import generics

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CabViewSet(viewsets.ModelViewSet):
    queryset = Cab.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CabUpdateSerializer
        return CabSerializer



class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city__name','cab__number']




class CabIdleTimeView(APIView):
    def get(self, request, id):
        cab_id = id
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not cab_id or not start_time or not end_time:
            return Response({"error": "cab_id, start_time, and end_time are required query parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cab = Cab.objects.get(id=cab_id)
        except Cab.DoesNotExist:
            return Response({"error": "Cab not found"}, status=400)

        start_time_dt = parse_datetime(start_time)
        end_time_dt = parse_datetime(end_time)

        
        non_idle_time = Bookings.objects.filter( cab=cab, end_time__gte=start_time, start_time__lte=end_time).aggregate(non_idle_time=Sum(Coalesce(F('end_time'), end_time_dt) - Coalesce(F('start_time'), start_time_dt)))
        delta = end_time_dt - start_time_dt
        if non_idle_time["non_idle_time"]:
            delta = end_time_dt - start_time_dt - non_idle_time["non_idle_time"]
    
        
        days, seconds = delta.days, delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        formatted_time = ""
        if days > 0:
            formatted_time = formatted_time + "days: {} ".format(days)
        if hours > 0:
            formatted_time = formatted_time + "hours: {} ".format(hours)
         
        if minutes > 0:
            formatted_time = formatted_time + "minutes: {}".format(minutes)
            
        return Response({"cab_id": cab_id, "idle_time": formatted_time}, status=200) 



class HighDemandCitiesView(APIView):
    def get(self, request):
        high_demand_cities = Bookings.objects.values('city__name').annotate(
            demand_count=Count('city')
        ).order_by('-demand_count')[:1]
        peak_time = Bookings.objects.values('start_time__hour').annotate(booking_count=Count('id')).order_by('-booking_count').first()
        result = []
        for entry in high_demand_cities:
            result.append({
                "city_with_high_demand": entry['city__name'],
                "booking_count": entry['demand_count'],
                
                "peak_demand_hour": peak_time['start_time__hour'],
                "booking_count__in_peak_hour": peak_time['booking_count']
            })

        return Response(result, status=200)





@api_view(['POST'])
def book(request):
    data = request.data
    cursor = connection.cursor()
    cursor.execute('''SELECT cab.id as cab_id, bookings.end_time-bookings.start_time as non_idle_time FROM main_bookings as bookings RIGHT OUTER JOIN main_cab as cab ON bookings.cab_id=cab.id JOIN main_city as city ON city.id==cab.city_id WHERE city.name=%s and state="IDLE" order by non_idle_time''', [data['city']])
    row = cursor.fetchone()
    if row is None:
        return Response({"error":"No cabs found"}, status=200)
    serializer = BookingSerializer(data={
        "city": data['city'],
        "cab": row[0]
    })

    if serializer.is_valid(raise_exception=True):
        Cab.objects.filter(id=row[0]).update(state="ON_TRIP")
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def end(request,id):
    instance = get_object_or_404(Bookings, id=id)
    if instance.end_time is not None:
        return Response({"error": "Trip already ended"}, status=422)
    instance.end_time = datetime.datetime.now()
    instance.save()
    cab_instance = get_object_or_404(Cab, id=instance.cab.id)
    cab_instance.state = 'IDLE'
    cab_instance.save()
    return Response({'message': 'Trip ended'}, status=200)