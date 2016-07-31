from pymongo import MongoClient

#connect to Mongo
client = MongoClient()
db = client['coinbase']

def delete_all(coll):
	db[coll].drop()

	print "Deleted all records in %s" % (coll)

delete_all("chunk_data")