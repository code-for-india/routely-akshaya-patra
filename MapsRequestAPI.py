__author__ = 'nsonti'

import simplejson
import urllib

def get_cost(origin_coor, dest_coor):
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(origin_coor),str(dest_coor))
    result= simplejson.load(urllib.urlopen(url))
    # sample output
    # {'status': 'OK', 'rows': [{'elements': [{'duration': {'text': '51 mins', 'value': 3074}, 'distance': {'text': '34.9 km', 'value': 34933}, 'status': 'OK'}]}], 'origin_addresses': ['Prestige Monte Carlo Street, Bangalore, Karnataka 560064, India'], 'destination_addresses': ['Salarpuria Softzone, Green Glen Layout, Bellandur, Bangalore, Karnataka 560037, India']}

    driving_time = result['rows'][0]['elements'][0]['duration']['value']*60 # in sec
    driving_distance = result['rows'][0]['elements'][0]['distance']['value']*1000 # in m
    res_dict = {}
    res_dict['distance'] = driving_distance
    res_dict['time'] = driving_time
    return res_dict

def test():
    orig_coord = 13.1152648, 77.5774666
    dest_coord = 12.924574, 77.670285
    result = get_cost(orig_coord, dest_coord)
    print result
