import yaml
from lib.yelp import places

with open("conf/credentials.yaml", 'r') as ymlfile:
    credentials = yaml.load(ymlfile)

params = {
    'db_conn_str': 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**credentials['db']),
    'yelp_api_key': credentials['yelp_api']['api_key'],
    'yelp_host': credentials['yelp_api']['api_host'],
    'yelp_search_endpoint': credentials['yelp_api']['api_endpoint'],
    'table': 'places_bar',
    'categories': 'bars',
    'location': 'Paris, FR',
    'nb': 10000
}

places.get_places_yelp(**params)

