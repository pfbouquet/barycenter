import sqlalchemy
import pandas as pd
from lib import isochrones
from lib import scoring

def get_isochrones(coordinates):
    several_isochrones = isochrones.GroupIsochrones(
        array_points_lon_lat=coordinates,
        array_transport_mode=['cycling']*len(coordinates)
    )
    several_isochrones.compute_isochrones()
    return several_isochrones


def get_geomatching_places(iso, database_uri, geomatching_target=50):

    engine = sqlalchemy.create_engine(database_uri)

    geo_places_query = """
        SELECT
            b.*
        FROM
            places_bar b
        WHERE
            ST_CONTAINS(ST_GeomFromText('{shape}'), ST_POINT(b.longitude, b.latitude))
        """

    geomatching_places = []

    for i in iter(sorted(iso.poi_isochrone_builder.keys())):
        poly = iso.poi_isochrone_builder[i]
        if not poly.is_empty:
            df = pd.read_sql_query(geo_places_query.format(shape=poly), con=engine)

            if len(df) == 0:
                continue

            df['time'] = i
            geomatching_places.append(df)
            geomatching_places_df = pd.concat(geomatching_places).reset_index(drop=True)
            geomatching_places_df_unique = geomatching_places_df.loc[geomatching_places_df.groupby('business_id')['time'].idxmin()]
            print('time: {time} > {nb_place} places'.format(time=i, nb_place=len(geomatching_places_df_unique)))
            if len(geomatching_places_df_unique) >= geomatching_target:
                break

    return geomatching_places_df_unique


def match_bars(coordinates, database_uri, limit=3):

    iso = get_isochrones(coordinates)
    place_df = get_geomatching_places(iso, database_uri, 50)
    place_df_scored = scoring.score_places(place_df, nb_trip = len(coordinates)

    return place_df_scored.sort_values(by=['score'], ascending=False).head(limit).to_dict('records')
