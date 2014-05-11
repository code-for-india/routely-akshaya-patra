from MapsRequestAPI import  *
from DBStuffAPI import *
from XlsxReader import *
from MapRequestThreadPool import MapRequestThreadPool
from Clustering import  *
import ast
import uuid

center_latlng = [{'lat' : 13.001658, 'lng' : 77.551099}, {'lat' : 12.9261416, 'lng' : 77.5975514}]


class XlxsToMapsWrapper:
    LAT_LOG_FILE_NAME = './akshaya-patra-data/lon and log details-xls.xlsx'
    def __init__(self):
        self.lat_lng_db = LngLatDB()
        self.lat_lng_db.remove() #erase it
        pass

    def getLatLngData(self, file_name=LAT_LOG_FILE_NAME):
        self.rows = readXlsx(file_name, sheet=1, header=True)
        self.lat_lng_db.add_to_db(self.rows)


class GetAndStoreCost:
    def __init__(self):
        self.lat_lng_db = LngLatDB()
        self.lat_lng_cost_db = LngLatCostDB()
        self.maps_request_api = MapsAPI()

        # clear latlngcost database
        self.lat_lng_cost_db.remove()
        pass

    def compute_costs(self):
        fh = open('cost.output','w')
        all_rows_list = self.lat_lng_db.get_all()
        count = 0
        center_count = 0
        res_count_correct = 0
        res_count_incorrect  = 0
        for row in all_rows_list:
            for center in center_latlng:
                try:
                    _id = row[u'_id']
                    if (u'log' in row) and (u'lon' in row):
                        lng = row[u'log']
                        lat = row[u'lon']
                        dest_coor = {}
                        dest_coor['lat'] = float(lat)
                        dest_coor['lng'] = float(lng)
                        cost = self.maps_request_api.get_cost_from_coor(origin_coor=center, dest_coor=dest_coor)
                        cost['dest'] = dest_coor
                        cost['origin'] = center
                        #cost['_id'] = _id
                        cost['_id'] = uuid.uuid4()
                        #self.lat_lng_cost_db.add_to_db(cost)
                        fh.write(str(cost)+'\n')
                        #print cost
                        import time
                        time.sleep(.25)
                        res_count_correct += 1
                except:
                    print 'Got screwed!'
                    res_count_incorrect += 1
            print count
            count += 1
            #print 'res_count_none', res_count_none, 'res count not done', res_count_not_none
            # if count == 5:
            #     break
            count += 1
        center_count += 1
        fh.close()
        print 'res_count_correct',res_count_correct, 'res count not done', res_count_incorrect

    def compute_cost_based_on_saved_text_file(self):
        fh = open('cost.output','Ur')
        count = 0
        for line in fh:
            print line
            row_dict = ast.literal_eval(str(line.rstrip()))
            row_dict['_id'] = uuid.uuid4() #adding some count to avoid duplicate key error
            print row_dict
            self.lat_lng_cost_db.add_to_db(row_dict)
            count += 1


    def compute_costs_thread_pool(self):
        all_rows_list = self.lat_lng_db.get_all()
        map_request_thread_pool = MapRequestThreadPool(20)
        map_request_thread_pool.create_threads()

        count = 0
        # Adding tasks to thread pool
        for center in center_latlng:
            for row in all_rows_list:
                # try:
                _id = row[u'_id']
                if u'log' in row and u'lon' in row:
                    lng = row[u'log']
                    lat = row[u'lon']
                    dest_coor = {}
                    data_dictionary = {}
                    try:
                        dest_coor['lat'] = float(lat)
                        dest_coor['lng'] = float(lng)
                    except:
                        print "Got screwed"
                    data_dictionary['dest'] = dest_coor
                    data_dictionary['origin'] = center
                    data_dictionary['_id'] = _id
                    map_request_thread_pool.add_to_queue(data_dictionary)
                    # except:
                #print 'Got screwed!'
            count +=1
            if count == 20:
                break

        # Wait for all threads to terminate
        map_request_thread_pool.join_all(wait_for_tasks=True)
        result = map_request_thread_pool.result_queue

        count = 0
        for res in result:
            print res
            if count == 5:
                break
            count += 1
        return



def main():
    xlxs_to_maps = XlxsToMapsWrapper()
    xlxs_to_maps.getLatLngData()

    # Compute the cost of all Schools from all centers for clustering
    get_and_store_cost = GetAndStoreCost()
    get_and_store_cost.compute_cost_based_on_saved_text_file()
    # get_and_store_cost.compute_costs()
    # get_and_store_cost.compute_costs_thread_pool()

    # Identify the high level clusters
    clustering = Clustering()
    clustering.high_level_clustering()

    return

if __name__ == '__main__':
    main()
