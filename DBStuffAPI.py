from pymongo import MongoClient

class LngLatDB:
    def __init__(self):
        self.db = MongoClient().routel

    def add_to_db(self, row):
        self.db.lnglat.insert(row)

    def get_data(self, query_dict):
        return list(self.db.lnglat.find(query_dict))

    def get_all(self):
        return list(self.db.lnglat.find())

    def remove(self):
        self.db.lnglat.remove()
        return

class LngLatCostDB:
    def __init__(self):
        self.db = MongoClient().routely
        pass

    def add_to_db(self, row):
        self.db.lnglatcost.insert(row)

    def get_data(self, query_dict):
        return list(self.db.lnglatcost.find(query_dict))

    def get_distinct(self, query_dict):
        return list(self.db.lnglatcost.distinct(query_dict))

    def get_all(self):
        return list(self.db.lnglatcost.find())

    def remove(self):
        self.db.lnglatcost.remove()
        return


class ElementLngLatCostDB:
    def __init__(self):
        self.db = MongoClient().routely
        pass

    def add_to_db(self, row):
        self.db.element_lng_lat_db.insert(row)

    def get_data(self,query_dict,pat):
        return list(self.db.element_lng_lat_db.find(query_dict, pat))

    def remove(self):
        self.db.element_lng_lat_db.remove()
        return

# db = MongoClient().routely
# def add_to_db(start_point , end_point , distance,  time):
#     db.things.insert({"start_point": start_point,"end_point": end_point,"distance": distance,"time": time })
#
#
# def get_data(start_point, end_point):
#     return list(db.things.find({"start_point": start_point,"end_point": end_point}))

