import geopandas
import urllib.request
import json
import pickle
from shapely.geometry import Point
import math


class GISModuleClass:
    def __init__(self, name):
        self.shape_data = None
        self.shape_size = 0
        self.name = name
        self.lat_long_dictionary = {}

        try:
            with open('dictionary.txt', 'rb') as handle:
                self.lat_long_dictionary = pickle.loads(handle.read())
        except:
            self.lat_long_dictionary = {}


    def get_nearest_address_label_from_lat_long(self, lat, long):
        str_url = "http://api.positionstack.com/v1/reverse?access_key=1ae2c49bd517acc9e1c7a2b44c2c0d83&query="
        str_url += str(lat)
        str_url += ","
        str_url += str(long)

        dict_value = self.lat_long_dictionary.get(str_url)
        if dict_value is not None:
            return dict_value

        with urllib.request.urlopen(str_url) as url:
            json_data = json.load(url)

        return_value = json_data['data'][0]['label']
        nv_pair = {str_url: return_value}
        self.lat_long_dictionary.update(nv_pair)

        with open('dictionary.txt', 'wb') as handle:
            pickle.dump(self.lat_long_dictionary, handle)

        return return_value

    def load_shapefile(self, the_file):
        try:
            self.shape_data = geopandas.read_file(the_file)
            self.shape_size = len(self.shape_data.index)
        except BaseException as err:
            raise

    def get_shapedata_indexes_containing_point(self, long, lat):
        index_list = []
        search_point = Point(long, lat)
        for i, row in self.shape_data.iterrows():
            polygon = row['geometry']
            if polygon.contains(search_point):
                index_list.append(i)

        return index_list

    # def get_shapedata_indexes_containing_point(self, p):
    #    return self.get_shapedata_indexes_containing_point(self, p.x, p.y)

    def get_shapedata_indexes_between_dates(self, start_date, end_date):
        index_list = []
        for i, row in self.shape_data.iterrows():
            if start_date <= row['poly_DateC'] <= end_date:
                index_list.append(i)

        return index_list

    def get_wildfire_name_at_index(self, index):
        if index > self.shape_size - 1 or index < 0:
            return ""

        return self.shape_data.loc[index, 'poly_Incid']

    def get_centroid_at_index(self, index):
        if index > self.shape_size - 1 or index < 0:
            return ""

        return self.shape_data.loc[index, 'geometry'].centroid

    def deg2rad(self, deg):
        return deg * (3.14159265358979 / 180)

    def get_hexagon_pts_from_center_with_km_distance(self, lat, lng, km):
        half_km = km / 2
        hexagon_points = []
        step_value = 0.001

        # get distance north
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_lat = w_lat - step_value

        # get distance south
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_lat = w_lat + step_value

        # get distance west
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_long = w_long - step_value

        # get distance east
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_long = w_long + step_value

        # get distance north-east
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_lat = w_lat - step_value
            w_long = w_long + step_value

        # get distance south-east
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_lat = w_lat + step_value
            w_long = w_long - step_value

        # get distance south-west
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_lat = w_lat + step_value
            w_long = w_long + step_value

        # get distance north-west
        dist = 0.0
        w_lat = lat
        w_long = lng
        while dist < half_km:
            dist = self.get_lat_long_dist_in_km(lat, lng, w_lat, w_long)
            if dist >= half_km:
                p = Point(w_long, w_lat)
                hexagon_points.append(p)
            w_lat = w_lat - step_value
            w_long = w_long - step_value

        return hexagon_points

    def get_lat_long_dist_in_km(self, lat1, long1, lat2, long2):
        r = 6371
        dlat = self.deg2rad(lat2 - lat1)
        dlong = self.deg2rad(long2 - long1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(self.deg2rad(lat1)) * math.cos(
            self.deg2rad(lat2)) * math.sin(dlong / 2) * math.sin(dlong / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = r * c
        return d

    def property_near_region_between_dates_json(self, start_date, end_date, lat, lng, km_distance):
        indexes = self.get_shapedata_indexes_between_dates(start_date, end_date)
        for an_index in indexes:
            if self.property_near_region(lat, lng, km_distance, an_index):
                return self.shape_data.loc[[an_index]].to_json()

        return None

    def property_near_region(self, lat, lng, km_distance, region_index):
        hex_pts = self.get_hexagon_pts_from_center_with_km_distance(lat, lng, km_distance)
        region = self.shape_data.loc[region_index, 'geometry']

        p = Point(lng, lat)
        if region.contains(p):
            return True

        for a_point in hex_pts:
            if region.contains(a_point):
                return True

        return False

    def properties_near_region_between_dates(self, start_date, end_date, lat_lng_km_triplet_array):
        response_array_of_dictionaries = []

        for a_triplet in lat_lng_km_triplet_array:
            lat = a_triplet['lat']
            lng = a_triplet['lng']
            km = a_triplet['km']
            resp = self.property_near_region_between_dates_json(start_date, end_date, lat, lng, km)
            dict = {'lat': lat, 'lng': lng, 'km': km, 'result': resp}
            response_array_of_dictionaries.append(dict)

        return response_array_of_dictionaries
