# That plugin uses the Graph Atlas generator from the networkx module.
# It creates one subgraph from each of the graph in the atlas and draw them
# using a force directed algorithm.
# It also creates a map of the whole atlas through the use of a quotient graph.

from tulip import *
import tulipplugins
import tulipnx

class NxGraphAtlas(tlp.ImportModule):
	def __init__(self, context):
		tlp.ImportModule.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)
	
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
		
		graph.setName("Graphs Atlas")
		
		viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
		viewLabel = graph.getStringProperty("viewLabel")
		viewLayout = graph.getLayoutProperty("viewLayout")
		viewSize = graph.getSizeProperty("viewSize")
		viewShape = graph.getIntegerProperty("viewShape")
		viewColor = graph.getColorProperty("viewColor")
		viewBorderColor = graph.getColorProperty("viewBorderColor")
		
		viewBorderWidth.setAllNodeValue(1.0)
		
		clone = graph.addCloneSubGraph("graphs")
		atlas = tulipnx.nx_atlas.graph_atlas_g()
		
		layoutAlgorithm = "FM^3 (OGDF)"
		
		i = 0
		for g in atlas:
			if i == 0:
				i = i + 1
				continue
			gi = clone.addSubGraph("G"+str(i))
			tulipnx.nxGraphToTlpGraph(g, gi)
			giLayout = gi.getLocalLayoutProperty("viewLayout")
			algoParameters = tlp.getDefaultPluginParameters(layoutAlgorithm, gi)
			gi.applyLayoutAlgorithm(layoutAlgorithm, giLayout, algoParameters)
			algoParameters = tlp.getDefaultPluginParameters("Connected Component Packing (Polyomino)", gi)
			gi.applyLayoutAlgorithm("Connected Component Packing (Polyomino)", giLayout, algoParameters)
			viewLayout.copy(giLayout)
			gi.delLocalProperty("viewLayout")
			i = i + 1
		
		quotient = graph.addSubGraph("map")
		quotientLayout = quotient.getLocalLayoutProperty("viewLayout")
		quotientSize = quotient.getLocalSizeProperty("viewSize")
		quotientSize.setAllNodeValue(tlp.Size(1,1,1))
		
		graph.createMetaNodes(clone.getSubGraphs(), quotient)
		
		layoutAlgorithm = "MMM Example Nice Layout (OGDF)"
		
		algoParameters = tlp.getDefaultPluginParameters(layoutAlgorithm, quotient)
		quotient.applyLayoutAlgorithm(layoutAlgorithm, quotientLayout, algoParameters)
		
		algoParameters = tlp.getDefaultPluginParameters("Auto Sizing", quotient)
		quotient.applySizeAlgorithm("Auto Sizing", quotientSize, algoParameters)
		
		for n in quotient.getNodes():
			quotient.openMetaNode(n)
		
		viewLayout.copy(quotientLayout)
		viewSize.copy(quotientSize)
		
		quotient.delLocalProperty("viewLayout")
		quotient.delLocalProperty("viewSize")
		
		for sg in clone.getSubGraphs():
			metaNode = quotient.createMetaNode(sg)
			viewLabel[metaNode] = sg.getName()
		
		for n in quotient.getNodes():
			viewShape[n] = tlp.NodeShape.Square
			viewColor[n] = tlp.Color(255,255,255,0)
			viewBorderColor[n] = tlp.Color.Black
		
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("NxGraphAtlas", "Graph Atlas (NetworkX)", "Antoine Lambert", "26/03/2015", """
Generators for the small graph atlas. See \"An Atlas of Graphs\" by Ronald C. Read and Robin J. Wilson, Oxford University Press, 1998.
""", "1.0", "Misc")
