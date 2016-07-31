from pymongo import MongoClient

def print_data():
    client = MongoClient()
    db = client['coinbase']
    cursor = list(db.chunk_data.find().limit(2).sort("_id", -1))
    cursor.reverse()
    for item in cursor:
        print item   #print cursor

    cursor = list(db.price_data.find().limit(30).sort("_id", -1))
    cursor.reverse()
    for item in cursor:
        print item   #print cursor

y = print_data()