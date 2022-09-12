import sys
import GISModule


def handler(event, context): 

    print("Inside app.handler\n")

    g1 = GISModule.GISModuleClass('gis')

    print("load_shapefile")

    g1.load_shapefile("zip://WFIGS_-_Current_Wildland_Fire_Perimeters.zip")

    print("setting up dict")

    dict = [
             {'lat': 32.28103, 'lng': -113.270, 'km': 1.5},
             {'lat': 37.28103, 'lng': -113.270, 'km': 0.5},
             {'lat': 37.28103, 'lng': -112.270, 'km': 0.5}
            ]


    print("invoking properties_near_region_between_dates")

    wfigs_data = g1.properties_near_region_between_dates("2022-08-01", "2022-08-31", dict)

    print(wfigs_data)
    return wfigs_data

