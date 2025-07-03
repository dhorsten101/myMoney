from django.urls import path

from .views import weather_widget, weather_list

urlpatterns = [
	path("weather_widget/", weather_widget, name="weather_widget"),
	path("weather/", weather_list, name="weather_list"),

]
