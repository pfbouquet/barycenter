import folium
import yaml
from folium.features import CustomIcon
from shapely.wkt import loads
import geopandas

with open("conf/credentials.yaml", 'r') as stream:
    data_loaded_credentials = yaml.safe_load(stream)
GOOGLEMAPS_TOKEN = data_loaded_credentials['googlemaps']['GOOGLEMAPS_TOKEN']


bounding_box_fr = loads('POLYGON((-7 52,10 52,10 41,-7 41,-7 52))')


def erase_old_maps():
    """Mock, to write later"""
    folder = 'app/templates/maps/'


def generate_html_map(
        destination: str,
        dict_isochrones: {},
        array_lon_lat_users: [(float, float)],
        array_popup_users: [str],
        array_lon_lat_bars: [(float, float)],
        array_popup_bars: [str]) -> str:
    """
    Generates a Folium map
    :return: HTML map as a string
    """
    my_map = folium.Map(
        location=[48.869719, 2.337960],  # Centered on Paris by default
        tiles='https://mts1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        API_key=GOOGLEMAPS_TOKEN,
        attr='Google Maps',
        max_zoom=18,
        zoom_start=12
    )

    # Folium does not support Polygons with holes,
    # so I need to convert it to GeoJSON first to plot it
    for duration, poi_isochrone in dict_isochrones.items():
        polygon = bounding_box_fr.difference(poi_isochrone)
        polygon_geojson = geopandas.GeoSeries([polygon]).__geo_interface__
        folium.features.Choropleth(
            polygon_geojson,
            fill_opacity=0.10,
            fill_color='green',
            line_weight=0
        ).add_to(my_map)

    # Adding the markers of the locations of the users
    assert len(array_lon_lat_users) == len(array_popup_users)
    for i in range(len(array_lon_lat_users)):
        folium.Marker(
            [array_lon_lat_users[i][1], array_lon_lat_users[i][0]],
            popup=array_popup_users[i]
        ).add_to(my_map)

    emoji_beer_png = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/" \
                     "320/facebook/65/clinking-beer-mugs_1f37b.png"

    # Adding the markers of the locations of the bars
    assert len(array_lon_lat_bars) == len(array_popup_bars)
    for i in range(len(array_lon_lat_bars)):
        folium.Marker(
            [array_lon_lat_bars[i][1], array_lon_lat_bars[i][0]],
            popup=array_popup_bars[i] + "🍻",
            icon=CustomIcon(emoji_beer_png, icon_size=(40, 40), icon_anchor=(20, 20))
        ).add_to(my_map)
    # alternative way: save to a .html file
    my_map.save(destination)
    # Documentation on how to embed a map here: https://github.com/python-visualization/folium/issues/781
    #html_string = my_map.get_root().render()
    return 0
