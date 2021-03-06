import numpy as np
import requests
import yaml
from dslib.utils import timeit

from shapely.geometry import shape
from shapely.geometry import Point


MAPBOX_BASE_URL = "https://api.mapbox.com"
NAVITIA_BASE_URL = "https://api.navitia.io/v1/"
POSSIBLE_MODES = ["driving", "cycling", "walking", "transit"]

with open("conf/credentials.yaml", 'r') as stream:
    data_loaded_credentials = yaml.safe_load(stream)
MAPBOX_TOKEN = data_loaded_credentials['mapbox']['MAPBOX_TOKEN']
NAVITIA_TOKEN = data_loaded_credentials['navitia']['NAVITIA_TOKEN']

with open("conf/isochrones.yaml", 'r') as stream:
    data_loaded_isochrones = yaml.safe_load(stream)
TIME_LIMITS = data_loaded_isochrones['time_limits']


class PoiIsochrones:
    """
    Defines a Point of Interest and the travel mode chosen by the user
    mode: driving, cycling, walking
    """

    def __init__(self, point: Point, mode: str):
        assert mode in POSSIBLE_MODES
        self.mode = mode
        self.lon = point.x
        self.lat = point.y
        self.isochrones = {}
        self.json_result = None
        self.res = None
        self.mapbox_request_url = ""
        self.navitia_request_url = ""
        self.time_limits_str = np.array(TIME_LIMITS).astype(str)

    def get_isochrones(self):
        """
        Distributes to the good provider depending on transit or other travel mode
        """
        if self.mode == 'transit':
            return self.get_isochrones_navitia()
        elif self.mode in ('cycling', 'driving', 'walking'):
            return self.get_isochrones_mapbox()
        else:
            print("Choose another mode")
            return None

    def get_isochrones_navitia(self):
        """
        Calls the NAVITIA API to get several isochrones at once
        :return:
        """
        headers = {'Authorization': NAVITIA_TOKEN}
        self.navitia_request_url = \
            f"https://api.navitia.io/v1/coverage/fr-idf/isochrones?" \
                f"from={self.lon}%3B{self.lat}" \
                "&boundary_duration%5B%5D=" + "&boundary_duration%5B%5D=".join(self.time_limits_str)
        self.res = requests.get(self.navitia_request_url, headers=headers)
        if self.res.status_code == 200:
            self.json_result = self.res.json()

            self.isochrones = {}
            for i in range(len(self.json_result['isochrones'])):
                # self.isochrones is a dict. Keys are the times rounded to 10 min
                # Values are the shapely shapes of the corresponding boxes.
                self.isochrones[self.json_result['isochrones'][i]['max_duration']] = \
                    shape(self.json_result['isochrones'][i]['geojson']).buffer(0)
            return self
        else:
            print(f"Error {self.res.status_code} while getting the isochrones from Navitia")
            print(self)
            print(self.res)
            return None

    def get_isochrones_mapbox(self):
        """
        Calls the Mapbox API to get several isochrones at once
        :return:
        """
        self.mapbox_request_url = f"{MAPBOX_BASE_URL}/isochrone/v1/mapbox/{self.mode}" \
            f"/{str(self.lon)},{str(self.lat)}" \
            f"?contours_minutes={','.join(self.time_limits_str)}&polygons=true&" \
            f"&access_token={MAPBOX_TOKEN}"
        self.res = requests.get(self.mapbox_request_url)

        if self.res.status_code == 200:
            self.json_result = self.res.json()

            self.isochrones = {}
            for i in range(len(self.json_result['features'])):
                self.isochrones[int(self.time_limits_str[::-1][i])] = \
                    shape(self.json_result['features'][i]['geometry']).buffer(0)

            return self
        else:
            print(f"Error {self.res.status_code} while getting the isochrones from Mapbox")
            print(self.res)
            return None


def intersect_two_isochrones(isochrone_a, isochrone_b):
    dual_isochrones = {}
    for duration_a, shape_a in isochrone_a.items():
        for duration_b, shape_b in isochrone_b.items():
            total_duration = duration_a + duration_b
            if total_duration in dual_isochrones.keys():
                dual_isochrones[total_duration] = dual_isochrones[total_duration] \
                    .union(shape_a.intersection(shape_b)).buffer(0)
            else:
                dual_isochrones[total_duration] = shape_a.intersection(shape_b).buffer(0)

    return dual_isochrones


class GroupIsochrones:
    """
    Takes an array of points (lon, lat) and computes the isochrones for each point
    """
    def __init__(self, array_points_lon_lat: [(int, int)], array_transport_mode: [str]):
        self.array_points_lon_lat = array_points_lon_lat
        self.array_transport_mode = array_transport_mode
        self.nb_points = len(self.array_points_lon_lat)
        assert len(self.array_points_lon_lat) == len(self.array_transport_mode) == self.nb_points
        self.array_poi_isochrones = []
        for i in range(self.nb_points):
            to_add = PoiIsochrones(
                point=Point(self.array_points_lon_lat[i]), mode=array_transport_mode[i]).get_isochrones()
            if to_add is not None:
                self.array_poi_isochrones.append(to_add)
        self.poi_isochrone_builder = None

    def compute_isochrones(self):
        """
        Computes the isochrones for total time to move for all input points
        :return:
        """
        self.poi_isochrone_builder = self.array_poi_isochrones[0].isochrones
        for i in range(len(self.array_poi_isochrones) - 1):
            self.poi_isochrone_builder = intersect_two_isochrones(
                self.poi_isochrone_builder, self.array_poi_isochrones[i + 1].isochrones)
