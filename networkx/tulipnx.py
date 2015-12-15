# Proxy module to access the networkx one
# It also defines utility functions in order to interact with the tulip module

from tulip import *

nxOk = False

try:
	
	import networkx as nx
	import networkx.generators.atlas as nx_atlas
	try:
		import networkx.generators.bipartite as nx_bipartite_generators
		bipartite_random_graph = nx_bipartite_generators.bipartite_random_graph
		
	except:
		bipartite_random_graph = nx.bipartite.generators.random_graph
		
	  
	nxOk = True
	
	def getTulipProperty(graph, attrName, attrType):
		prop = None
		if attrType == int:
			prop = graph.getIntegerProperty(attrName)
		elif attrType == float:
			prop = graph.getDoubleProperty(attrName)
		elif attrType == str or attrType == unicode:
			prop = graph.getStringProperty(attrName)
		elif attrType == bool:
			prop = graph.getBooleanProperty(attrName)
		return prop
	
	# convert a networkx graph to a tulip graph
	def nxGraphToTlpGraph(nxGraph, tlpGraph=None):
		graph = tlpGraph
		if not graph:
			graph = tlp.newGraph()
		nodes = {}
		for n in nxGraph.nodes():
			nodes[n] = graph.addNode()
			for attrName in nxGraph.node[n]:
				attrValue = 	nxGraph.node[n][attrName]
				prop = getTulipProperty(graph, attrName, type(attrValue))
				if prop:
					prop[nodes[n]] = attrValue
		for e in nxGraph.edges():
			eTlp = graph.addEdge(nodes[e[0]], nodes[e[1]])
			for attrName in nxGraph.edge[e[0]][e[1]]:
				attrValue = 	nxGraph.edge[e[0]][e[1]][attrName]
				prop = getTulipProperty(graph, attrName, type(attrValue))
				if prop:
					prop[eTlp] = attrValue
			
		return graph

except ImportError:
  pass
  
def checkNetworkX(pluginProgress):
	if not nxOk and pluginProgress:
		pluginProgress.setError("The required NetworkX python module is not installed. You can get it through the pip tool (pip install network).")
	return nxOk

	


