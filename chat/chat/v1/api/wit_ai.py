import requests

from .open_weather_map import get_weather
from .yelp import get_restaurant
from .secrets import WIT_TOKEN

DEFAULT_REPLY = "Sorry, I don't understand"


def get_reply(message):
	"""Return the reply of a given message after processing."""
	url = f'https://api.wit.ai/message?v=20201026&q={message}'
	headers = {'Authorization': WIT_TOKEN}
	response = requests.get(url, headers=headers)
	jsonResponse = response.json()
	try:
		if jsonResponse['intents'][0]['name'] == "GetWeatherInformation":
			location = jsonResponse['entities']['wit$location:location'][0]['resolved']['values'][0]['name']
			return get_weather(location)
		elif jsonResponse['intents'][0]['name'] == "FindRestaurant":
			location = jsonResponse['entities']['wit$location:location'][0]['resolved']['values'][0]['name']
			query = jsonResponse['entities']['wit$local_search_query:local_search_query'][0]['value']
			return get_restaurant(query, location)
	except:
		return DEFAULT_REPLY
