from lib.generate_dynamic_map import generate_html_map
from lib.isochrones import GroupIsochrones
from dslib.utils.logging import timeit
import numpy as np


def main():
    size = 2
    array_transport_mode = ['walking', 'cycling']#, 'transit', 'transit', 'transit',
                            #'transit', 'walking', 'transit', 'cycling', 'cycling']
    with timeit():
        several_isochrones = GroupIsochrones(
            array_points_lon_lat=[
                (
                    2.337960+np.random.rand()*0.1+i*0.02,
                    48.86971+np.random.rand()*0.1+i*0.02
                ) for i in range(size)
            ],
            array_transport_mode=array_transport_mode
        )
    with timeit():
        several_isochrones.compute_isochrones()
    print(several_isochrones.poi_isochrone_builder)

    generate_html_map(
        dict_isochrones = several_isochrones.poi_isochrone_builder,
        array_lon_lat_users=[(2.2, 48.8), (2.3, 48.81)],
        array_popup_users=['Mike house', 'Mike work'],
        array_lon_lat_bars=[(2.21, 48.81), (2.31, 48.811)],
        array_popup_bars=['Chez Jacquie', 'Le Favart']
    )


if __name__=='__main__':
    main()