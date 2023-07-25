import geocoder as gc
from geopy.geocoders import Nominatim
import pyowm
from tkinter import Tk
from tkinter.messagebox import askyesno

root = Tk()
root.withdraw()
allowloc = askyesno('Permissions Required', 
    'CBT would like to access your location.\nGrant access to this application to access weather functions')

if allowloc == True:
    g = gc.ip('me')
    location = Nominatim(user_agent='GetLoc')
    locationName = location.reverse(g.latlng)
    location = locationName.address
    locationlist = location.split(sep = ', ')
    owm = pyowm.OWM('c47ab2899ea8aef42f862b1dc30c0678')
    weather_mgr = owm.weather_manager()
    observation = weather_mgr.weather_at_place(locationlist[-3])
    temperature = observation.weather.temperature('celsius')['temp']
    humidity = observation.weather.humidity
    wind = observation.weather.wind()
    weather = observation.weather.status
    root.destroy()
else:
    root.destroy()
