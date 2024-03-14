from rest_framework import serializers
from .models import City, Cab, Bookings
from rest_framework.validators import UniqueValidator

class CitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=City.objects.all())])
    class Meta:
        model = City
        fields = ["id", "name"]


class CityField(serializers.RelatedField):
    def to_internal_value(self, data):
        cities = City.objects.filter(name=data)
        if cities.exists():
            return City.objects.get(name=data)
        raise serializers.ValidationError("Not Found")
    def to_representation(self, value):
        return value.name

class CabSerializer(serializers.ModelSerializer):
    city = CityField(queryset=City.objects.all())
    number = serializers.CharField(validators=[UniqueValidator(queryset=Cab.objects.all())])
    state = serializers.CharField(required=False, default="IDLE", validators=[])
    
    class Meta:
        model = Cab
        fields = ["id","number","state","city"]

    
    def create(self, validated_data):
        if validated_data["state"] != 'IDLE':
            raise serializers.ValidationError({"state": ["Can only update if the state is 'IDLE'"]})   
        return super().create(validated_data)
    

class CabUpdateSerializer(serializers.ModelSerializer):
    city = CityField(queryset=City.objects.all())
    number = serializers.CharField(read_only=True)
    state = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        if instance and instance.state != 'IDLE':
            raise serializers.ValidationError("Can only update if the state is 'IDLE'")
        return super().update(instance, validated_data)
    
    class Meta:
        model = Cab
        fields = ["id","number","state","city"]



class CabField(serializers.RelatedField):
    def to_internal_value(self, data):
        return Cab.objects.get(id=data)
    def to_representation(self, value):
        return value.number


class BookingSerializer(serializers.ModelSerializer):
    cab = CabField(queryset=Cab.objects.all())
    city = CityField(queryset=City.objects.all())
    
    class Meta:
        model = Bookings
        fields = ["cab", "city", "id", "start_time", "end_time"]
