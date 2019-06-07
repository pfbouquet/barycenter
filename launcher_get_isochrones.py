from lib.isochrones import GroupIsochrones
from dslib.utils.logging import timeit
import numpy as np


def main():
    size = 10
    array_transport_mode = ['transit' for i in range(size)]
    array_transport_mode[3:6]='walking'
    array_transport_mode[1] = 'cycling'
    with timeit():
        several_isochrones = GroupIsochrones(
            array_points_lon_lat=[
                (
                    2.337960+np.random.rand()*0.1+i*0.02,
                    48.86971+np.random.rand()*0.1+i*0.02
                ) for i in range(size)
            ],
            array_transport_mode=['transit' for i in range(size)]
        )
    with timeit():
        several_isochrones.compute_isochrones()
    print(several_isochrones.poi_isochrone_builder)


if __name__=='__main__':
    main()