# Tulip import plugin written in Python for importing the dependencies graph of a npm package (node package manager)
# The plugin simply parses the package.json files to extract the whole dependencies graph of a package.
# Be sure to have called 'npm install' in the package directory first in order to get the complete dependencies graph

from tulip import *
import tulipplugins
import json
import os

npmPackageDirParamName = "dir::npm package dir"

packageNode = {}

def parsePackageJsonForDependenciesGraph(npmPackageDir, graph, packageName = None):
	
	# get package.json file path
	if not packageName:
		# no package name provided as parameter, it is the root package
		packageJsonFilePath = npmPackageDir + '/package.json'
	else:
		# depedency package from the node_modules directory
		packageJsonFilePath = npmPackageDir + '/node_modules/' + packageName + '/package.json'
	
	# package.json does not exist, abort
	if not os.path.exists(packageJsonFilePath):
		return
		
	# parse package.json file
	packageInfos = json.load(open(packageJsonFilePath))

	# create a string property that will store dependency type on edges
	dependencyType = graph.getStringProperty('dependencyType')
	
	# create the top level package node (entry point)
	if not packageName:
		packageName = packageInfos['name']
		packageNode[packageName] = graph.addNode()
		graph['viewLabel'][packageNode[packageName]] = packageName
	
	currentPackageNode = packageNode[packageName]
	
	# iterate over package dependencies
	for depType in ['dependencies', 'peerDependencies', 'devDependencies']:
		if depType in packageInfos:
			for dep in packageInfos[depType]:
				# create a node associated to the package if it does not exist yet
				if not dep in packageNode:
					packageNode[dep] = graph.addNode()
					graph['viewLabel'][packageNode[dep]] = dep
					# parse depedency package dependencies
					parsePackageJsonForDependenciesGraph(npmPackageDir, graph, dep)
					parsePackageJsonForDependenciesGraph(npmPackageDir + '/node_modules/' + packageName, graph, dep)
				# add an edge between the package and its depdency if it has not already be created	
				if not graph.hasEdge(currentPackageNode, packageNode[dep]):
					depEdge = graph.addEdge(currentPackageNode, packageNode[dep])
					dependencyType[depEdge] = depType
				

class NpmPackageDependenciesGraphImport(tlp.ImportModule):
	def __init__(self, context):
		tlp.ImportModule.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)
		self.addStringParameter(npmPackageDirParamName, "The root directory of the npm package")

	def importGraph(self):
		# This method is called to import a new graph.
		# An empty graph to populate is accessible through the "graph" class attribute
		# (see documentation of class tlp.Graph).

		# The parameters provided by the user are stored in a Tulip DataSet 
		# and can be accessed through the "dataSet" class attribute
		# (see documentation of class tlp.DataSet).

		# The method must return a boolean indicating if the
		# graph has been successfully imported.
		
		npmPackageDir = self.dataSet[npmPackageDirParamName]
		
		# Check if the directory contains a npm package first
		rootPackageJson = npmPackageDir + '/package.json'
		if not os.path.exists(rootPackageJson):
			if self.pluginProgress:
				self.pluginProgress.setError('Error : directory ' + npmPackageDir + ' does not seem to contain a npm package.')
			return False
		
		# parse package depedencies graph
		parsePackageJsonForDependenciesGraph(npmPackageDir, self.graph)
		
		# apply a force directed algorithm to draw the graph
		self.graph.applyLayoutAlgorithm('Fast Multipole Multilevel Embedder (OGDF)')	
		
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("NpmPackageDependenciesGraphImport", "Npm package dependencies graph", "Antoine Lambert", "26/11/2015",\
 "Import the packages dependencies graph from a npm package", "1.0", "Misc")
