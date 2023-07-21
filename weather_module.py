import geocoder as gc
from geopy.geocoders import Nominatim
import pyowm
import tkinter as tk

g = gc.ip('me')
location = Nominatim(user_agent='GetLoc')
locationName = location.reverse(g.latlng)
location = locationName.address
locationlist = location.split(sep = ', ')
owm = pyowm.OWM('API KEY')
weather_mgr = owm.weather_manager()
observation = weather_mgr.weather_at_place(locationlist[-3])
temperature = observation.weather.temperature('celsius')['temp']
humidity = observation.weather.humidity
wind = observation.weather.wind()
weather = observation.weather.status