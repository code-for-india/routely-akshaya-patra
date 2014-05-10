from pymongo import MongoClient

db = MongoClient().routely

def add_to_db(start_point , end_point , distance,  time):
    db.things.insert({"start_point": start_point,"end_point": end_point,"distance": distance,"time": time })


def get_data(start_point, end_point):
    return list(db.things.find({"start_point": start_point,"end_point": end_point}))

