from abc import abstractmethod

from http import HTTPStatus
import requests


class Reply:
    """A reply to user's request"""

    entityName = __qualname__

    def __init__(self):
        """Initializes the reply"""
        self.url = ''
        self.headers = {}

    def get_api_json_response(self):
        """Returns the JSON response by making an API call"""
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != HTTPStatus.OK:
            raise response.raise_for_status()
        return response.json()

    @abstractmethod
    def process_api_json_response(self):
        """Returns the reply processed from JSON response"""
        raise NotImplementedError

    @classmethod
    def get_default_reply(cls):
        """Returns the default reply"""
        return f'{cls.entityName} data processing error'

    def get_reply(self):
        """Returns the reply to the given parameter(s)"""
        try:
            return self.process_api_json_response()
        except:
            return self.get_default_reply()


class WeatherReply(Reply):
    """A reply to user's request on weather information"""

    entityName = __qualname__

    def __init__(self, location):
        super().__init__()
        self.location = location
        from chat.chat.v1.api.secrets import OPEN_WEATHER_MAP_API_KEY
        self.url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPEN_WEATHER_MAP_API_KEY}'

    @staticmethod
    def convert_kelvin_to_celsius(temperatureInKelvin):
        """Return the temperature in Celsius of it given it Kelvin."""
        DIFFERENCE = 273.15
        return temperatureInKelvin - DIFFERENCE

    def process_api_json_response(self):
        jsonResponse = self.get_api_json_response()
        weather = jsonResponse['weather'][0]['description']
        temperature = int(self.convert_kelvin_to_celsius(jsonResponse['main']['temp']))
        return f"We have {weather} in {self.location}, the temperature is {temperature}'C."


class RestaurantsReply(Reply):
    """A reply to user's request on restaurants information"""

    entityName = __qualname__

    def __init__(self, term, location):
        super().__init__()
        self.term = term
        self.location = location
        self.url = f'https://api.yelp.com/v3/businesses/search?term={term}&location={location}'
        from chat.chat.v1.api.secrets import YELP_API_KEY
        self.headers = {'Authorization': YELP_API_KEY}

    def process_api_json_response(self):
        jsonResponse = self.get_api_json_response()
        nRestaurants = len(jsonResponse['businesses'])
        return {
            "message": f"We have these {nRestaurants} {self.term} in {self.location}",
            "restaurants": [
                {"name": business["name"], "phone": business["phone"]}
                for business in jsonResponse['businesses']
            ]
        }
