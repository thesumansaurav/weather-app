"""
The views functions to handle all the api functions for the project.
"""
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from weather_app.models import Location
from .serializers import LocationSerializer

import uuid


def generate_user_identifier():
    """Generates unique identifier for session to store in the database."""
    return str(uuid.uuid4())


class LocationWeatherUpdateView(APIView):
    """A class to handles the weather data coming from 3rd party API and store in the DB."""
    def get(self, request, *args, **kwargs):

        city = request.query_params.get('city')

        if not city:
            return Response({'error': 'City parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = "b1c50931cea24784a6e105909230412"
        url = f'https://api.weatherapi.com/v1/forecast.json?q={city}&days=3&key={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()
        except requests.RequestException as e:
            return Response({'error': f'Error fetching weather data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get or create a user identifier
        user_identifier = request.session.get('user_identifier', None)
        if not user_identifier:
            # Implement your function to generate a unique identifier
            user_identifier = generate_user_identifier()
            request.session['user_identifier'] = user_identifier
            request.session.save()

        # Create or update the location with weather data
        location, created = Location.objects.update_or_create(
            user_identifier=user_identifier,
            name=city,
            defaults={'weather_data': weather_data},
        )

        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityWeatherFromDatabaseView(APIView):
    """A class to get the weather data for a particular city fo that particular session_id."""
    def post(self, request, *args, **kwargs):
        user_identifier = request.session.get('user_identifier')

        if not user_identifier:
            return Response({'error': 'User identifier not found in the session'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            locations = Location.objects.filter(
                user_identifier=user_identifier)
        except Location.DoesNotExist:
            return Response({'error': f'Weather data for user identifier {user_identifier} not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
