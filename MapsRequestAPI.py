__author__ = 'nsonti'

import simplejson
import urllib


class MapsAPI:
    def __init__(self):
        pass

    # coordinates should be dicationary with 'lat' and 'lng' as keys
    def get_cost_from_coor(self, origin_coor, dest_coor):
        # https://maps.googleapis.com/maps/api/distancematrix/json?origins=(13.001658,%2077.551099)&destinations=(13.055447,%2077.459648)&mode=driving&language=en-EN&sensor=false&key=AIzaSyBU3xlwGUFuZASWZ9lPqCnHb590yZSrjAM
        if type(origin_coor) is dict:
            tmp = origin_coor['lat'], origin_coor['lng']
            origin_coor = tmp
            tmp = dest_coor['lat'], dest_coor['lng']
            dest_coor = tmp

        #url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(origin_coor),str(dest_coor))
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false&key=AIzaSyBU3xlwGUFuZASWZ9lPqCnHb590yZSrjAM".format(str(origin_coor),str(dest_coor))
        print url
        result= simplejson.load(urllib.urlopen(url))
        # sample output
        # {'status': 'OK', 'rows': [{'elements': [{'duration': {'text': '51 mins', 'value': 3074}, 'distance': {'text': '34.9 km', 'value': 34933}, 'status': 'OK'}]}], 'origin_addresses': ['Prestige Monte Carlo Street, Bangalore, Karnataka 560064, India'], 'destination_addresses': ['Salarpuria Softzone, Green Glen Layout, Bellandur, Bangalore, Karnataka 560037, India']}

        print result
        if 'duration' in result['rows'][0]['elements'][0]:
            driving_time = result['rows'][0]['elements'][0]['duration']['value']*60 # in sec
            driving_distance = result['rows'][0]['elements'][0]['distance']['value']*1000 # in m
            res_dict = {}
            res_dict['distance'] = driving_distance
            res_dict['time'] = driving_time
            return res_dict
        else:
            return None

    def get_coor_from_address(self, address):
        # sample url = http://maps.google.com/maps/api/geocode/json?address=akamai%20bangalore&sensor=false

        url = "http://maps.google.com/maps/api/geocode/json?address={0}&sensor={1}".format(str(address), str('false'))
        result = simplejson.load(urllib.urlopen(url))

        # sample output
        # {'status': 'OK', 'results': [{'geometry': {'location': {'lat': 12.9327621, 'lng': 77.6140289}, 'viewport': {'northeast': {'lat': 12.9341110802915, 'lng': 77.6153778802915}, 'southwest': {'lat': 12.9314131197085, 'lng': 77.6126799197085}}, 'location_type': 'APPROXIMATE'}, 'address_components': [{'long_name': 'Akamai Technologies India Pvt Ltd', 'types': ['premise'], 'short_name': 'Akamai Technologies India Pvt Ltd'}, {'long_name': 'Jyoti Nivas College Road', 'types': ['route'], 'short_name': 'Jyoti Nivas College Road'}, {'long_name': 'Koramangala Industrial Layout', 'types': ['sublocality', 'political'], 'short_name': 'Koramangala Industrial Layout'}, {'long_name': 'Koramangala', 'types': ['sublocality', 'political'], 'short_name': 'Koramangala'}, {'long_name': 'Bangalore', 'types': ['locality', 'political'], 'short_name': 'Bangalore'}, {'long_name': 'Bangalore Urban', 'types': ['administrative_area_level_2', 'political'], 'short_name': 'Bangalore Urban'}, {'long_name': 'Karnataka', 'types': ['administrative_area_level_1', 'political'], 'short_name': 'KA'}, {'long_name': 'India', 'types': ['country', 'political'], 'short_name': 'IN'}, {'long_name': '560034', 'types': ['postal_code'], 'short_name': '560034'}], 'partial_match': True, 'formatted_address': 'Akamai Technologies India Pvt Ltd, Jyoti Nivas College Road, Koramangala Industrial Layout, Koramangala, Bangalore, Karnataka 560034, India', 'types': ['premise']}]}
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
        res_dict = {}
        res_dict['lat'] = lat
        res_dict['lng'] = lng
        return res_dict

    def test_get_cost(self):
        orig_coord = 41.8337329, -87.7321555 #lat, lng
        dest_coord = 40.4313684, -79.9805005
        # result = self.get_cost_from_coor(orig_coord, dest_coord)
        result = self.get_directions_between_source_and_destination(orig_coord, dest_coord)
        print result

    def test_get_coor_from_address(self):
        test_address = 'akamai bangalore'
        result = self.get_coor_from_address(test_address)
        print result

    def get_directions_between_source_and_destination(self, origin_coordinates, destination_coordinates):
        if type(origin_coordinates) is dict:
            tmp = origin_coordinates['lat'], origin_coordinates['lng']
            origin_coordinates = tmp
            tmp = destination_coordinates['lat'], destination_coordinates['lng']
            destination_coordinates = tmp
        print destination_coordinates
        url = "http://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&mode=driving&language=en-EN&sensor=false".format(str(origin_coordinates),str(destination_coordinates))

        result= simplejson.load(urllib.urlopen(url))

        route_points = [[]]
        for step in result['routes'][0]['legs'][0]['steps']:
            start_location = [step][0]['start_location']
            end_location = [step][0]['end_location']
            location=(start_location,end_location)
            route_points.append(location)
            print route_points
        return None


def main():
    maps_api = MapsAPI()
    maps_api.test_get_cost()
    maps_api.test_get_coor_from_address()

if __name__ == '__main__':
    main()


