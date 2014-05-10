from pymongo import MongoClient

class LngLatDB:
    def __init__(self):
        self.db = MongoClient().routely

    def add_to_db(self, row):
        self.db.lnglat.insert(row)

    def get_data(self, query_dict):
        return list(self.db.lnglat.find(query_dict))

    def get_all(self):
        return list(self.db.lnglat.find())

class LngLatCostDB:
    def __init__(self):
        self.db = MongoClient().routely
        pass

    def add_to_db(self, row):
        self.db.lnglatcost.insert(row)

    def get_data(self, query_dict):
        return list(self.db.lnglatcost.find(query_dict))

# db = MongoClient().routely
# def add_to_db(start_point , end_point , distance,  time):
#     db.things.insert({"start_point": start_point,"end_point": end_point,"distance": distance,"time": time })
#
#
# def get_data(start_point, end_point):
#     return list(db.things.find({"start_point": start_point,"end_point": end_point}))

