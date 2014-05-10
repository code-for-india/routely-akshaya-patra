__author__ = 'nsonti'

from DBStuffAPI import *

class Clustering:
    def __init__(self):
        self.lat_lng_cost_db = LngLatCostDB()
        self.element_db = ElementLngLatCostDB()
        pass

    def high_level_clustering(self):
        rows = self.lat_lng_cost_db.get_all()
        self.element_db.remove()
        count = 0
        # read and all to lat_lng_cost_db
        # for row in rows:
        #     store_dict = {}
        #     if (u'dest' in row) and (u'origin' in row) and (u'time' in row) and (u'distance' in row):
        #         store_dict[u'dest'] = row[u'dest']
        #         store_dict[u'origin'] = row[u'origin']
        #         store_dict[u'time'] = row[u'time']
        #         store_dict[u'distance'] = row[u'distance']
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
                    store.update(origin_coor)
                    store.update(dest_coor)
                    store.update({'cost': int(min_cost)})
                    self.element_db.add_to_db(store)



    def cost_function(self,time, distance):
        return (int(time)*1.2)+(int(distance)*0.8)




def main():
    clustering = Clustering()
    clustering.high_level_clustering()

if __name__ == '__main__':
    main()
