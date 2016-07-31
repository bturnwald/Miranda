# Miranda

*Nowhere near usable yet, will add instructions for use once it is*

Miranda is a Bitcoin price monitoring and trading bot written in python.  Prices will be retreived real time via websockets from exchanges that provide them and stored in a local database (MongoDB).  The front end is in Kivy and uses the graph module from the Kivy Garden.  Currently the goal is to use tick charts instead of typical time series data used in most trading software.  The reason for tick charts is they seem to fit bitcoin's market better (opinion, not advice, we'll see how it works out).  

Targeted Exchanges:
Currently using GDAX and Bitfinex for data.  Working on adding OKCoin but their data has been a bit sketchy, most likely an issue with the way the websocket calls are currently implemented in Miranda.

Data:
Miranda stores each trade from the selected exchange in a collection.  This 'raw' data is then split into 'chunks' and added to a second collection to provide data for the tick chart.

Indicators:
Simple Moving Average with user selectable window.
Stochastic Oscillator with user selectable window.

UI:
The kivy UI is currently very early and needs a ton of works.  Mostly proof a concept and testing the garden.graph module at this point.  The main chart currenlty shows the high, low, and close price of each tick as well as a single simple moving average.  A second chart shows the stochastic oscillator.


Immediate Goals:
 - Add reconnection trys to the websocket implementations, GDAX seems to terminate the connection after a certain period
 - Add volume to the 'chunk' data and add a 3rd graph displaying it.
 - Clean up formalize indicator.py and analyst.py
 - Add threading to the kivy front end so all 3 modules don't need to run independently

