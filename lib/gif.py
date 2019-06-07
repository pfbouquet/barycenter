import urllib.request
import json


def get_random_gif_url(term, giphy_credentials):
    data = json.loads(urllib.request.urlopen(
        "http://api.giphy.com/v1/gifs/random?tag={term}&api_key={giphy_api}".format(
            giphy_api=giphy_credentials['api_key'],
            term=term)).read())
    return data['data']['images']['fixed_height']['url']
