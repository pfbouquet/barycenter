import urllib
import requests
import pandas as pd
import sqlalchemy


def call_yelp(yelp_api_key, yelp_host, yelp_search_endpoint, categories, location, offset, limit):
    url = '{0}{1}'.format(yelp_host, urllib.parse.quote(yelp_search_endpoint.encode('utf8')))

    headers = {
        'Authorization': 'Bearer %s' % yelp_api_key,
    }

    url_params = {
        'categories': categories.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'offset': offset,
        'limit': limit,
        'sort_by': 'rating'
    }

    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def format_places_yelp(places_json):
    cols = [
        'business_id',
        'name',
        'categories',
        'price',
        'rating',
        'review_count',
        'location',
        'latitude',
        'longitude',
        'phone',
        'image_url',
        'url']

    places_df = pd.DataFrame.from_records(places_json['businesses'])

    places_df['latitude'] = [b['latitude'] for b in places_df['coordinates']]
    places_df['longitude'] = [b['longitude'] for b in places_df['coordinates']]
    places_df.rename({'id':'business_id'}, axis=1, inplace=True)

    return places_df[cols]


def get_places_yelp(yelp_api_key, yelp_host, yelp_search_endpoint, categories, location, nb, db_conn_str, table):
    call_limit = 50
    all_df = []
    is_first_batch = True
    engine = sqlalchemy.create_engine(db_conn_str)

    for offset in range(0, nb, call_limit):
        rep = call_yelp(yelp_api_key, yelp_host, yelp_search_endpoint, categories, location, offset=offset, limit=min(nb - offset, call_limit))
        rep_df = format_places_yelp(rep)
        all_df.append(rep_df)

        if is_first_batch:
            mode = 'replace'
        else:
            mode = 'append'

        rep_df.to_sql(table, engine, index=False, if_exists=mode, dtype={
            'categories': sqlalchemy.types.JSON,
            'location': sqlalchemy.types.JSON})

        is_first_batch = False

    return pd.concat(all_df)

