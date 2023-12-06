# weather/urls.py
from django.urls import path
from .views import LocationWeatherUpdateView, CityWeatherFromDatabaseView

urlpatterns = [
    path('update_weather/', LocationWeatherUpdateView.as_view(),
         name='update_weather'),
    path('get_weather/', CityWeatherFromDatabaseView.as_view(), name='get_weather'),
]
