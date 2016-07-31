import websocket
import json, time, urllib2
import sqlite3 as lite

stamp = str(int(time.time()))

#get last 100 trade (prepopulate streaming database)
def getHistorical(stamp):
    #connect to DB
    db = lite.connect('temp/cb_'+stamp)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE cb_data(trade_id TEXT, price TEXT, size TEXT)''')

    #call URL
    response = urllib2.urlopen('https://api.exchange.coinbase.com/products/BTC-USD/trades')
    info = json.loads(response.read())
    #records come from coinbase newest first, need to organize database oldest first
    data = reversed(info)

    trade_id = []
    price = []
    size = []
    #insert into database
    for row in data:
        db_tuple = [str(row['trade_id']),str(row['price']),str(row['size']),]
        cursor.execute('''INSERT INTO cb_data VALUES(?,?,?)''', db_tuple)
        #print db_tuple
        db.commit()
    db.close()

#on message check for match records and insert into database if trade_id is greater that last trade
def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'match':
        db = lite.connect('temp/cb_'+stamp)
        cursor = db.cursor()
        cursor.execute('''SELECT max(trade_id) from cb_data''')
        max_trade = int(cursor.fetchone()[0])

        #check = []
        #for row in records:
            #check.append(row)
        #x = max(check)
        print max_trade
        print data['trade_id']
        
        if max_trade < int(data['trade_id']):
            print message
            trade_id = data['trade_id']
            price = data['price']
            size = data['size']
            db_tuple = [str(data['trade_id']),str(data['price']),str(data['size']),]
            cursor.execute('''INSERT INTO cb_data VALUES(?,?,?)''', db_tuple)
            #print db_tuple
            db.commit()
            db.close()
        else:
            print "Got Here"

def on_close(ws):
    print "WebSocket connection terminated"

def on_open(ws):
    msg = {"type": "subscribe", "product_id": "BTC-USD"}
    sub_msg = json.dumps(msg)
    ws.send(sub_msg)

def socketStream(stamp):
    getHistorical(stamp)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws-feed.exchange.coinbase.com", on_message = on_message, on_close = on_close, on_open = on_open)
    ws.run_forever()

socketStream(stamp)

