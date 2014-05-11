__author__ = 'nsonti'

import uuid
import ast
from DBStuffAPI import *

center_latlng = [{'lat' : 13.001658, 'lng' : 77.551099}, {'lat' : 12.9261416, 'lng' : 77.5975514}]

class Clustering:
    def __init__(self):
        self.lat_lng_cost_db = LngLatCostDB()
        self.element_db = ElementLngLatCostDB()
        self.element_db.remove()
        pass

    def high_level_clustering(self):
        rows = self.lat_lng_cost_db.get_all()
        fh = open('cluster.output','w+')
        count = 0
        for row in rows:
            if (u'dest' in row) and (u'origin' in row) and (u'time' in row) and (u'distance' in row):
                dest_coor = {}
                dest_coor[u'dest'] = row[u'dest']

                rows_corresponding = self.lat_lng_cost_db.get_data(dest_coor)
                min_cost = 0
                origin_coor = None
                if len(self.element_db.get_data(dest_coor)) == 0:
                    print 'Computing for destination ',str(dest_coor)
                    for row in rows_corresponding:
                        if origin_coor == None:
                            origin_coor = {}
                            origin_coor[u'origin'] = row[u'origin']
                            min_cost = self.cost_function(time=row[u'time'], distance=row[u'distance'])
                            #print 'initial min cost', min_cost
                            #print 'origin', str(origin_coor)

                        else:
                            cur_coor = {}
                            cur_cost = self.cost_function(time=row[u'time'], distance=row[u'distance'])
                            #print 'current cost', cur_cost

                            if cur_cost < min_cost:
                                #print 'old origin', str(origin_coor)
                                origin_coor[u'origin'] = row[u'origin']
                                min_cost = cur_cost
                            #print 'new origin', str(origin_coor)
                        count +=1
                        print count

                    #end for
                    store = {}
                    store['_id']=count
                    store.update(origin_coor)
                    store.update(dest_coor)
                    store.update({'cost': int(min_cost)})
                    fh.write(str(store)+'\n')
                    #self.element_db.add_to_db(store)

        fh.close()
        #self.populate_element_db_from_file()

    def populate_element_db_from_file(self,file_name='cluster.output'):
        self.element_db.remove()
        fh = open(file_name,'Ur')
        row = []
        for line in fh:
            _cur_row = ast.literal_eval(str(line.rstrip('\n')))
            row.append(_cur_row)
            self.element_db.add_to_db(_cur_row)

        fh.close()


    def get_lat_lng_list_1(self,file_name='cluster.output'):
        fh = open(file_name, 'Ur')
        lat_lng_1 = []
        for line in fh:
            cur_row = ast.literal_eval(str(line.rstrip('\n')))
            if cur_row[u'origin'][u'lat'] == center_latlng[0]['lat'] and cur_row[u'origin'][u'lng'] == center_latlng[0]['lng']:
                tmp_dict = {}
                tmp_dict[u'origin'] = cur_row[u'origin']
                tmp_dict[u'dest'] = cur_row[u'dest']
                lat_lng_1.append(tmp_dict)


        print 'length of lat_lng_list_1', len(lat_lng_1)

    def get_lat_lng_list_2(self,file_name='cluster.output'):
        fh = open(file_name, 'Ur')
        lat_lng_2 = []
        for line in fh:
            cur_row = ast.literal_eval(str(line.rstrip('\n')))
            if cur_row[u'origin'][u'lat'] == center_latlng[1]['lat'] and cur_row[u'origin'][u'lng'] == center_latlng[1]['lng']:
                tmp_dict = {}
                tmp_dict[u'origin'] = cur_row[u'origin']
                tmp_dict[u'dest'] = cur_row[u'dest']
                lat_lng_2.append(tmp_dict)

        print 'length of lat_lng_list_2', len(lat_lng_2)

    def cost_function(self,time, distance):
        return distance


def main():
    clustering = Clustering()
    clustering.high_level_clustering()
    clustering.get_lat_lng_list_1()
    clustering.get_lat_lng_list_2()


if __name__ == '__main__':
    main()
