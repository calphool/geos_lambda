import geopandas
import GISModule

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g1 = GISModule.GISModuleClass('gis')
    g1.load_shapefile("zip:///users/jrounceville/downloads/WFIGS_-_2022_Wildland_Fire_Perimeters_to_Date.zip")

    dict = [
             {'lat': 32.28103, 'lng': -113.270, 'km': 1.5},
             {'lat': 37.28103, 'lng': -113.270, 'km': 0.5},
             {'lat': 37.28103, 'lng': -112.270, 'km': 0.5}
            ]
    wfigs_data = g1.properties_near_region_between_dates("2022-08-01", "2022-08-31", dict)
    print(wfigs_data)


