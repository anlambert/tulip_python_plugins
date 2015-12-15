# That plugin imports a graph from a file in the GraphML format.
# The graph is first imported through the use of the networkx module,
# then converted to a Tulip graph (mapping GraphML attributes to TLP properties)

from tulip import *
import tulipplugins
import tulipnx

class NxGraphMLImport(tlp.ImportModule):
	def __init__(self, context):
		tlp.ImportModule.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)
		self.addStringParameter("file::filename", "GraphML file to import")

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
		
		graphMLFile = self.dataSet["file::filename"]
		
		nx_graph = None

		try:	
			nx_graph = tulipnx.nx.read_graphml(graphMLFile)
		except:
			pass
		
		if nx_graph:
			tulipnx.nxGraphToTlpGraph(nx_graph, graph)		
			return True
		else:
			if self.pluginProgress:
				self.pluginProgress.setError("An error occurred when trying to import the GraphML file")
			return False

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("NxGraphMLImport", "GraphML Import (NetworkX)", "", "15/12/2015", 
"""
Imports a graph from a file in the GraphML format.
GraphML is a comprehensive and easy-to-use file format for graphs.
It consists of a language core to describe the structural properties 
of a graph and a flexible extension mechanism to add application-specific data.
""", "1.0", "File")
