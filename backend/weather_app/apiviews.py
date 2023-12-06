import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer

import uuid


def generate_user_identifier():
    return str(uuid.uuid4())


class LocationWeatherUpdateView(APIView):
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
