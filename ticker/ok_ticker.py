import websocket
import json, time
from pymongo import MongoClient

# Need a better way to handle this, shouldn't have global client and db variables
# Should probably put this whole thing into a Ticker class to make error id/handling easier 
# but it works for now 

#connect to mongo client
client = MongoClient()
#connect to database
db = client['okcoin']


def on_message(ws, message):
	
	data = json.loads(message)

	if isinstance(data, dict):
		print data
	
	elif data[1] == 'tu':
		print 'New Message'
		print data
	else:
		pass

def on_close(ws):
	print "Websocket connection terminated"

def on_open(ws):
	msg = {'event':'subscribe','channel':'trades','pair':'BTCUSD'}
	sub_msg = json.dumps(msg)
	ws.send(sub_msg)

def socketStream():
	#prepopulate the database with most recent 100 trades
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp('wss://api2.bitfinex.com:3000/ws', on_message = on_message, on_close = on_close, on_open = on_open)
	ws.run_forever()

#COMMENT OUT WHEN USING. Call from another module with x = ticker.socketStream()
socketStream()
