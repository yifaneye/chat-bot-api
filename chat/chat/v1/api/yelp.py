import requests

from .secrets import YELP_API_KEY

DEFAULT_REPLY = "Restaurant data processing error"


def get_restaurant(term, location):
    """Return the restaurant information of a given location as a reply."""
    url = 'https://api.yelp.com/v3/businesses/search?term={}&location={}'.format(term, location)
    headers = {'Authorization': YELP_API_KEY}
    response = requests.get(url, headers=headers)
    jsonResult = response.json()
    try:
        return [
            {"name": business["name"], "phone": business["phone"]}
            for business in jsonResult['businesses']
        ]
    except:
        return DEFAULT_REPLY
