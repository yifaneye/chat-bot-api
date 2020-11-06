import requests

from .secrets import OPEN_WEATHER_MAP_API_KEY

DEFAULT_REPLY = "Weather data processing error"


def get_weather(location):
	"""Return the weather information of a given location as a reply."""
	url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPEN_WEATHER_MAP_API_KEY}'
	response = requests.get(url)
	jsonResult = response.json()
	try:
		weather = jsonResult['weather'][0]['description']
		temperature = int(convert_kelvin_to_celsius(jsonResult['main']['temp']))
		return f"We have {weather} in {location}, the temperature is {temperature}'C."
	except:
		return DEFAULT_REPLY


def convert_kelvin_to_celsius(temperatureInKelvin):
	"""Return the temperature in Celsius of it given it Kelvin."""
	DIFFERENCE = 273.15
	return temperatureInKelvin - DIFFERENCE
