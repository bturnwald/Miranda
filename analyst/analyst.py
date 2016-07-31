from pymongo import MongoClient

#connect to Mongo
def get_data(n_records):
	client = MongoClient()
	db = client['coinbase']
	cursor = list(db.price_data.find().limit(n_records).sort("_id", -1))
	cursor.reverse()
	print cursor
	#data = reversed(cursor)  #sorted in descending order already
	return cursor
	#for item in data:
		#print item
#cursor = db.price_data.find_one(sort=[("trade_id", -1)])


def split_arr(n, data):
	total = len(data)
	#split a data array in 'chunks' of length n minus modulus.  Used to 'bin' price data to make tick graphing easier
	#doens't return the modulus in the new array
	chunks = [data[x:x+n] for x in xrange(0, (total-total%n), n)]
	#print chunks

	#extract HLOC prices from array into separate arrays for tick graph
	#should also add volume, should be sum of all points in chunk
	highs = []
	lows = []
	opens = []
	closes = []
	for i in chunks:
		#tip: i[x][0], change the '0' the the data value index you wish to extract
		#return an ((x,y),(x,y),...) array  of data points
		chunk_length = len(i)
		highs_split = [i[x]['price'] for x in xrange(0, chunk_length)]
		highs.append(max(highs_split))

	return highs
	#return chunks

#split_arr(2, data)
#arr = get_data(10)
#split_arr(2,arr)


