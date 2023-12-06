from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='update-weather'),
    # path('/', views.index, name='update-weather'),
    path('add_city', views.get_city, name="get-city"),
    path('weather-data/<str:city_name>/',
         views.weather_data, name='weather_data'),
    path("second-task", views.task, name="task-two"),
    path("interleaving", views.get_interleaving, name="get-interleaving")
]
