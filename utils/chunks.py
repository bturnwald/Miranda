
#define some arbitrary list/array
#21 numbers
data = [(1,0),(3,4),(2,2),(1,2),(4,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(2,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)]

#modulus x%y

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
		chunk_length = len(i)
		highs_split = [i[x][0] for x in xrange(0, chunk_length)]
		highs.append(max(highs_split))

	print highs
	return chunks

split_arr(2, data)


