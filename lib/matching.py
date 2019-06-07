import sqlalchemy
import pandas as pd
from lib.isochrones import GroupIsochrones


def get_isochrones(coordinates):
    several_isochrones = GroupIsochrones(
        array_points_lon_lat=coordinates,
        array_transport_mode=['cycling']*len(coordinates)
    )
    several_isochrones.compute_isochrones()
    return several_isochrones


def get_geomatching_places(iso, credentials_db, geomatching_target=50):
    db_conn_str = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**credentials_db)
    engine = sqlalchemy.create_engine(db_conn_str)

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


def match_bars(coordinates, credentials_db, limit=3):

    iso = get_isochrones(coordinates)

    geomatching_places_df = get_geomatching_places(iso, credentials_db, 50)




