from pymongo import MongoClient
import time

#connect to MongoClient
client = MongoClient()
db = client['coinbase']

#calculates the average for an array of numbers
def avg(numbers):
    av = float(sum(numbers))/len(numbers)
    return av

# calculates the sma of a given arr with n window
# WARNING: this returns an array padded by n-1 0's.  This is correct
# when starting w/ 0 data but if you areappending to a
# running list you must remove these 0's to retain accurate moving averages
def sma(arr, n):
	sma_arr = [avg(arr[x-n:x]) if x-n > -1 else 0 for x in range(1, len(arr)+1)]
	return sma_arr

def stoch(price,high,low, n):
	high_arr = [max(high[x-n:x]) if x-n > -1 else 0 for x in range(1, len(high)+1)]
	low_arr = [min(low[x-n:x]) if x-n > -1 else 0 for x in range(1, len(low)+1)]

	stoch_arr = [(price[x]-low_arr[x])/(high_arr[x]-low_arr[x]) if high_arr[x]-low_arr[x] != 0 else 0 for x in range(len(price))]

	return stoch_arr

#finds the sma for a given array, modifying it according to fit live stream and inserts into db
def add_sma(n):

	cursor_data = db.chunk_data.find().count()
	cursor_sma = db.sma_data.find().count()

	if cursor_sma > n:
		sma_diff = (cursor_data - cursor_sma) + n #need to go n back in history to cont trend
	else:
		sma_diff = cursor_data - cursor_sma
	#print sma_diff
	
	if sma_diff > 0:
		cursor = list(db.chunk_data.find().limit(sma_diff).sort("_id", -1))
		cursor.reverse() # chunk_data is a dict by default
		price_data = [float(x['end']) for x in cursor]
		#print price_data

	else:
		price_data = []

	#calculate the sma's of new data
	if price_data:  #only call sma if cursor contains data, empty lists evaluate to Boolean False
		new_sma_data = sma(price_data, n)
		if cursor_sma > 0: # remove leading 0's
			del new_sma_data[0:n-1]
		else: # do nothing
			pass
		for i in new_sma_data:
			result = db.sma_data.insert_one(
				{
				"price": i
				})
			print 'sma: '+ str(i)
		#print new_sma_data


def add_stoch(n): # n is stoch lookback period 'standard' is 14

	cursor_data = db.chunk_data.find().count()
	cursor_stoch = db.stoch_data.find().count()

	#determine index of data needed from db
	if cursor_stoch > n:
		stoch_diff = (cursor_data - cursor_stoch) + n
	else:
		stoch_diff = cursor_data - cursor_stoch

	#get data from db
	if stoch_diff > 0:
		cursor = list(db.chunk_data.find().limit(stoch_diff).sort("_id", -1))
		cursor.reverse() # chunk_data is a dict by default, use only end (price) data
		end_data = [float(x['end']) for x in cursor]
		high_data = [float(x['high']) for x in cursor]
		low_data = [float(x['low']) for x in cursor]
		#print price_data

	else:
		end_data = []
	#generate rolling list of highs and lows

	#calculate the sma's of new data
	if end_data:  #only call stoch if cursor contains data, empty lists evaluate to Boolean False
		new_stoch_data = stoch(end_data, high_data, low_data, n)
		if cursor_stoch > 0: # remove leading 0's
			del new_stoch_data[0:n-1]
		else: # do nothing
			pass
		for i in new_stoch_data:
			result = db.stoch_data.insert_one(
				{
				"price": i
				})
			print 'stoch: '+ str(i)
		#print new_sma_data

while True:
	k = add_sma(5)
	v = add_stoch(14)
	time.sleep(0.2)


