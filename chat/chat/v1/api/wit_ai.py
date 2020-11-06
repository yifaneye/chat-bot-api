import requests

from .reply import WeatherReply, RestaurantsReply
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
			return WeatherReply(location).get_reply()
		elif jsonResponse['intents'][0]['name'] == "FindRestaurant":
			location = jsonResponse['entities']['wit$location:location'][0]['resolved']['values'][0]['name']
			query = jsonResponse['entities']['wit$local_search_query:local_search_query'][0]['value']
			return RestaurantsReply(query, location).get_reply()
	except:
		return DEFAULT_REPLY
