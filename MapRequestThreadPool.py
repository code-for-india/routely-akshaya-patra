__author__ = 'nsonti'

import time
import threading
import simplejson
import urllib

# Log levels
# - 0 = Debug
# - 1 = Info
LOG_LEVEL = 1

def logging(string,log_level=0):
    if log_level <= LOG_LEVEL:
        print string
    return

#job of this thread is to download youtube videos using  url and store it in download_path
class MapRequestThreadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.queue_access_lock = threading.Condition(threading.Lock())
        self.result_access_queue_lock = threading.Condition(threading.Lock())
        self.task_queue = [] # each element of task queue contains a dict which stores keys - url, image_store_path
        self.result_queue = []
        self.input_count = 0
        self.result_count = 0
        self.threads = [] # stores all the threads
        self.is_join = False # when this is set to True threadPool has joined all threads

    def get_thread_count(self):
        return self.num_threads

    def get_queue_size(self):
        self.queue_access_lock.acquire()
        queue_len = len(self.task_queue)
        self.queue_access_lock.release()
        return queue_len

    def create_threads(self):
        for i in range(self.num_threads):
            new_thread = MapRequestThreadClass(_pool=self,_id=i)
            self.threads.append(new_thread)
            new_thread.start()

    # data_dictionary can contain any number of fields.
    def add_to_queue(self, data_dictionary):
        self.queue_access_lock.acquire()
        self.task_queue.append(data_dictionary)
        self.input_count += 1
        self.queue_access_lock.release()

    def add_to_result_queue(self, data_dictionary):
        self.result_access_queue_lock.acquire()
        self.result_queue.append(data_dictionary)
        self.result_count += 1
        self.result_access_queue_lock.release()

    def get_next_task(self):
        tmp = {}
        self.queue_access_lock.acquire()
        if len(self.task_queue) != 0:
            tmp = self.task_queue.pop(0)
        else:
            tmp = None
        self.queue_access_lock.release()
        return tmp

    def get_total_image_count(self):
        return self.input_count

    def join_all(self, wait_for_tasks=True):
        self.is_join = False

        if wait_for_tasks:
            while self.task_queue != []:
                time.sleep(2)

        for thread in self.threads:
            thread.set_quit()
            thread.join()

        self.is_join = True


class MapRequestThreadClass (threading.Thread):
    def __init__(self, _pool, _id=0):
        threading.Thread.__init__(self)
        self.tid = _id
        self.parent_pool = _pool
        self.die = False
    def run(self):
        logging(str("Thread Started %d" %(self.tid)),0)
        # self.die is set to True, the thread will come out of while loop in next iteration
        while self.die == False:
            job = self.parent_pool.get_next_task()
            if job == None:
                time.sleep(2)
            else:
                # execute the job
                # job is basically a Data dictionary which was pushed in the taskqueue
                result_dict = self.get_cost_from_coor(job['origin'],job['dest'])
                self.parent_pool.add_to_result_queue(result_dict)


    def get_cost_from_coor(self, origin_coor, dest_coor):
        if type(origin_coor) is dict:
            tmp = origin_coor['lat'], origin_coor['lng']
            origin_coor = tmp
            tmp = dest_coor['lat'], dest_coor['lng']
            dest_coor = tmp

        url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(origin_coor),str(dest_coor))
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

    def set_quit(self):
        self.die = True
