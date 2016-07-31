from pymongo import MongoClient

#connect to Mongo
client = MongoClient()
db = client['coinbase']

def delete_all(coll):
	db[coll].drop()

	print "Deleted all records in %s" % (coll)

print '%s, %s, %s, or %s' %('price_data', "chunk_data", 'sma_data','stoch_data' )
x = raw_input("Type one DB to drop:")

delete_all(str(x))