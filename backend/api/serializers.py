from rest_framework import serializers
from weather_app.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'user_identifier', 'name', 'weather_data']
