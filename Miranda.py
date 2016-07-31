import kivy
#kivy.require('1.0.6') # replace with your current kivy version !

from analyst import analyst

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from kivy.garden.graph import Graph, MeshLinePlot

#from math import sin
from pymongo import MongoClient
 
class MirandaWidget(BoxLayout):

	def __init__(self, **kwargs):
		super(MirandaWidget, self).__init__(**kwargs)

		#connect to mongo
		self.client = MongoClient()
		self.db = self.client['coinbase']

		#define the plots for main data
		self.plot = []
		self.plot.append(MeshLinePlot(color=[0, 1, 0, .5])) # High
		self.plot.append(MeshLinePlot(color=[1, 0, 0, .5])) # Low
		self.plot.append(MeshLinePlot(color=[0, 0, 1, .8])) # Close
		self.plot.append(MeshLinePlot(color=[0, 1, 0, 1])) # SMA

		#define the plot for the stoch data
		self.plot_stoch = MeshLinePlot(color=[0, 1, 0, .5])

		#get the id of the plot to use
		#data plot
		self.graph = self.ids.graph_plot
		self.update_graph()

		self.stoch_graph = self.ids.stoch_plot
		self.update_stoch()

		Clock.schedule_interval(lambda dt: self.update_graph(),1.0)
		Clock.schedule_interval(lambda dt: self.update_stoch(),1.0)


	def update_graph(self):
		#fetch and format the data
		self.graph = self.ids.graph_plot
		self.cursor = list(self.db.chunk_data.find().limit(100).sort("_id", -1))
		self.cursor.reverse()
		self.highs = [float(i['high']) for i in self.cursor]
		self.lows = [float(i['low']) for i in self.cursor]
		self.ends = [float(i['end']) for i in self.cursor]

		self.cursor_sma = list(self.db.sma_data.find().limit(100).sort("_id", -1))
		self.cursor_sma.reverse()
		self.sma = [float(i['price']) for i in self.cursor_sma]

		#self.arr = analyst.get_data(self.data_cnt)
		#self.data = analyst.split_arr(self.chunks,self.arr)
		#float_data = [float(i) for i in self.data]

		#set the graph details
		self.graph.xmin = -0
		self.graph.xmax = len(self.highs)
		self.graph.ymin = min(self.highs) - (max(self.highs)-min(self.highs))*.1
		self.graph.ymax = max(self.highs) + (max(self.highs)-min(self.highs))*.1
		self.graph.x_ticks_major = 1
		self.graph.y_ticks_major = (self.graph.ymax-self.graph.ymin)/10

		#plot the points
		self.plot[0].points = [(j,self.highs[j]) for j in range(len(self.highs))]
		self.plot[1].points = [(j,self.lows[j]) for j in range(len(self.lows))]
		self.plot[2].points = [(j,self.ends[j]) for j in range(len(self.ends))]
		self.plot[3].points = [(j,self.sma[j]) for j in range(len(self.sma))]

		#self.plot1.points = [(j,self.highs[j]) for j in range(len(self.highs))] ##tuple [(x,y)]
		for plot in self.plot:
			self.graph.add_plot(plot)

	def update_stoch(self):
		self.stoch_graph = self.ids.stoch_plot
		self.cursor = list(self.db.stoch_data.find().limit(100).sort("_id", -1))
		self.cursor.reverse()
		
		self.stochs = [float(i['price']) for i in self.cursor]
		#print self.stochs

		#set the graph details
		self.stoch_graph.xmax = len(self.stochs)
		self.plot_stoch.points = [(j,self.stochs[j]) for j in range(len(self.stochs))]

		self.stoch_graph.add_plot(self.plot_stoch)
	
	#def update_graph(self,*args):
		#update the data
		#self.arr = analyst.get_data(self.data_cnt)
		#self.data = analyst.split_arr(self.chunks,self.arr)
		#self.float_data = [float(i) for i in self.data]

		#set the new graph details
		#self.graph.xmin = -0
		#self.graph.xmax = len(self.float_data)
		#self.graph.ymin = min(self.float_data)*.99
		#self.graph.ymax = max(self.float_data)*1.01
		#self.graph.x_ticks_major = 1
		#self.graph.y_ticks_major = (self.graph.ymax-self.graph.ymin)/10
		#plot the new points
		#self.plot1.points = [(j,float(self.data[j])) for j in range(len(self.data))] ##tuple [(x,y)]
		#self.graph.add_plot(self.plot1)

	#Clock.schedule_interval(update_graph, 1)


class Miranda(App):

	def build(self):
		return MirandaWidget()


if __name__ == '__main__':
    Miranda().run()