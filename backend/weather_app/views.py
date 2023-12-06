

from django.shortcuts import render, redirect
import uuid
import requests
from django.contrib import messages
from .models import Location
from django.http import HttpResponse


def generate_user_identifier():
    return str(uuid.uuid4())

def all_interleavings(s1, s2):
    def generate_interleavings(interleaving, remaining_s1, remaining_s2):
        if not remaining_s1 and not remaining_s2:
            result.append(interleaving)
            return

        if remaining_s1:
            generate_interleavings(interleaving + remaining_s1[0], remaining_s1[1:], remaining_s2)

        if remaining_s2:
            generate_interleavings(interleaving + remaining_s2[0], remaining_s1, remaining_s2[1:])

    result = []
    generate_interleavings('', s1, s2)
    return result


def index(request, *args, **kwargs):
    user_identifier = request.session.get('user_identifier', None)
    print(args)
    print(kwargs)
    saved_cities = Location.objects.filter(
        user_identifier=user_identifier)
    forecast_data = []
    if saved_cities:
        # Extract forecast data from the JSON field
        forecast_data = saved_cities[0].weather_data.get(
            'forecast', {}).get('forecastday', [])
    return render(request, "index.html", {'cities': saved_cities, 'forecast': forecast_data})
 
def task(request):
    return render(request, 'task2.html')

def get_city(request):
    print("I am heer")
    if request.method == "POST":
        city = request.POST["city"]
    
        api_key = "b1c50931cea24784a6e105909230412"
        url = f'https://api.weatherapi.com/v1/forecast.json?q={city}&days=4&key={api_key}'
        weather_data = { }
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()
        except requests.RequestException as e:
           return HttpResponse(e)
        if weather_data:
            # Get or create a user identifier
            user_identifier = request.session.get('user_identifier', None)
            if not user_identifier:
                # Implement your function to generate a unique identifier
                user_identifier = generate_user_identifier()
                request.session['user_identifier'] = user_identifier
                request.session.save()

            # Create or update the location with weather data
            Location.objects.update_or_create(
                user_identifier=user_identifier,
                name=city,
                defaults={'weather_data': weather_data},
            )
            
            return redirect('http://127.0.0.1:8000/')
        else:

            return HttpResponse("Sorry ! no weather data for this city at weatherapi.com")
        

def weather_data(request, city_name):
    user_identifier = request.session.get('user_identifier', None)
    saved_cities = Location.objects.filter(
        user_identifier=user_identifier)
    # Fetch the specific city data for the user
    city_data = Location.objects.filter(
        user_identifier=user_identifier, name=city_name).first()

    if city_data:
        # Extract forecast data from the JSON field
        forecast_data = city_data.weather_data.get(
            'forecast', {}).get('forecastday', [])

        return render(request, 'index.html', {'cities': saved_cities, 'forecast_city': forecast_data})
    else:
        # Handle the case where the city data is not found
        messages.warning(
            request, "You have not added this city"
        )
        return redirect('http://127.0.0.1:8000/')


def get_interleaving(request):
    if request.method == "POST":
        s1 = request.POST['s1']
        s2 = request.POST['s2']

    interleavings = all_interleavings(s1, s2)

    return render(request, "task2results.html", {'results': interleavings})
