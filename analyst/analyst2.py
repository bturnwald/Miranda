from pymongo import MongoClient
import time

#connect to Mongo
client = MongoClient()
db = client['coinbase']

#
def get_data(n):

	# get count of both db's
	cursor1 = db.chunk_data.find().count()
	cursor2 = db.price_data.find().count()
	#find the difference in number of records between them
	rec_dif = cursor2 - cursor1*n # chunked data is always shorter by n
	if rec_dif > 0:
		cursor = list(db.price_data.find().limit(rec_dif).sort("_id", -1))
		cursor.reverse()
	else:
		cursor = [] 


	return cursor # return the array of the difference in the 2 collections

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
		#get highs
		highs_split = [i[x]['price'] for x in xrange(0, chunk_length)]
		high= max(highs_split)
		low= min(highs_split)
		begin = highs_split[0]
		end = highs_split[-1]

		result = db.chunk_data.insert_one(
			{
			"high": high,
			"low": low,
			"begin": begin,
			"end": end
			})
		#print result
		print "High: %s, Low: %s, Close: %s" %(high, low,end)

	#return highs
	#return chunks

# if current db length > closes[-1] + n_records
# get all records between current db and closes[-1]
# return that array to split_arr to be split into chunks
# note this should really be stored in different db's with 'tag' 'n' chunk length 

while True:
	x = get_data(50)
	split_arr(50, x)
	time.sleep(0.5)


#split_arr(2, data)
#arr = get_data(10)
#split_arr(2,arr)


# get the count of both db's (chunk_data, indicators)
# cursor1 = db.chunk_data.find().count()
# cursor2 = db.indicators.find().count()


#def analyze(n):

	#cursor1 = db.chunk_data.find().count()
	#cursor2 = db.indicators.find().count()
	#diff = cursor1 - cursor2



