from lib.isochrones import GroupIsochrones


def main():
    several_isochrones = GroupIsochrones(
        array_points_lon_lat=[
            (2.337960+i*0.02, 48.869719) for i in range(2)
        ],
        array_transport_mode=['cycling' for i in range(2)]
    )
    several_isochrones.compute_isochrones()
    print(several_isochrones.poi_isochrone_builder)


if __name__=='__main__':
    main()