import websocket
import json, time, urllib2
from pymongo import MongoClient

# Need a better way to handle this, shouldn't have global client and db variables
# Should probably put this whole thing into a Ticker class to make error id/handling easier 
# but it works for now 

#connect to mongo client
client = MongoClient()
#connect to database
db = client['coinbase']

def getHistory():
    #connet to mongo client
    #client = MongoClient()
    #connect to database
    #db = client['coinbase']

    #call the exchange open api
    response = urllib2.urlopen('https://api.exchange.coinbase.com/products/BTC-USD/trades')
    raw_info = json.loads(response.read())
    data = reversed(raw_info)

    trade_id = []
    price = []
    size = []

    #insert into database

    for row in data:
        #convert to strings for easier passing later
        trade_id = str(row['trade_id'])
        price = str(row['price'])
        size = str(row['size'])

        result = db.price_data.insert_one(
            {
            "trade_id": trade_id,
            "price": price,
            "size": size
            })

def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'match':

        #find most recent record
        cursor = db.price_data.find_one(sort=[("trade_id", -1)])
        last_trade = cursor['trade_id']
        #only insert if message trade_id is greater than last trade trade_id
        if int(last_trade) < int(data['trade_id']):
            print message
            #convert to strings for easier passing later
            trade_id = str(data['trade_id'])
            price = str(data['price'])
            size = str(data['size'])

            # insert result into collection
            result = db.price_data.insert_one(
                {
                "trade_id": trade_id,
                "price": price,
                "size": size
                })

        else:
            pass

def on_close(ws):
    print "Websocket connection terminated"

def on_open(ws):
    msg = {"type": "subscribe", "product_id": "BTC-USD"}
    sub_msg = json.dumps(msg)
    ws.send(sub_msg)

def socketStream():
    #prepopulate the database with most recent 100 trades
    getHistory()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws-feed.exchange.coinbase.com", on_message = on_message, on_close = on_close, on_open = on_open)
    ws.run_forever()

#COMMENT OUT WHEN USING. Call from another module with x = ticker.socketStream()
socketStream()

##########   Mongo Testing Stuff ###########

#def print_data():
#    client = MongoClient()
#    db = client['coinbase']
#    cursor = db.price_data.find()
#    for document in cursor:
#        print document
#x = getHistory(stamp)
#y = print_data()


#def print_collections():
#    client = MongoClient()
#    db = client['coinbase']
#    names = db.collection_names()
#    print names
#x = print_collections()

#def find_max():
#    client = MongoClient()
#    db = client['coinbase']
#    #find most recent record
#    cursor = db.price_data.find_one(sort=[("trade_id", -1)])
#    last_trade = cursor['trade_id']
#    if max_trade < int(data)

#    print cursor
#    print last_trade
#x=find_max()