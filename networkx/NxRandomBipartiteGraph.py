# That plugin imports a random bipartite graph using the generator from the networkx module

from tulip import *
import tulipplugins
import tulipnx

class NxRandomBipartiteGraph(tlp.ImportModule):
	def __init__(self, context):
		tlp.ImportModule.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)
		self.addIntegerParameter("n", "The number of nodes in the first bipartite set.", "10")
		self.addIntegerParameter("m", "The number of nodes in the second bipartite set.", "10")
		self.addFloatParameter("p", "Probability for edge creation.", "0.5")

	def importGraph(self):
		# This method is called to import a new graph.
		# An empty graph to populate is accessible through the "graph" class attribute
		# (see documentation of class tlp.Graph).

		# The parameters provided by the user are stored in a Tulip DataSet 
		# and can be accessed through the "dataSet" class attribute
		# (see documentation of class tlp.DataSet).

		# The method must return a boolean indicating if the
		# graph has been successfully imported.
		
		if not tulipnx.checkNetworkX(self.pluginProgress):
			return False
			
		graph = self.graph
		
		n = self.dataSet["n"]
		m = self.dataSet["m"]
		p = self.dataSet["p"]
		
		bp_graph = tulipnx.bipartite_random_graph(n, m, p)
		
		tulipnx.nxGraphToTlpGraph(bp_graph, graph)	
		
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("NxRandomBipartiteGraph", "Random Bipartite Graph (NetworkX)", "Antoine Lambert", "09/12/2015", 
"""
Imports a bipartite random graph. 
This is a bipartite version of the binomial (Erdos-Renyi) graph.
""", "1.0", "Graph")
