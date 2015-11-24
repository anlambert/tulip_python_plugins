# Tulip import plugin written in Python for importing the dependencies graph of a
# CMake project (target -> target dependencies + target -> external libraries dependencies)

# The plugin use the graphviz output feature of CMake enabling to generate dot files
# representing the different dependencies graphs of the project (global + target specific)
# The global dot file is then imported in Tulip through the graphviz import plugin
# included in the framework

from tulip import *
import tulipplugins
import tempfile
import subprocess
import os

cmakeProjectSourceDirParamName = "dir::CMake project source dir"
cmakeExecutableParamName = "file::CMake executable"
cmakeParametersParamName = "CMake parameters"

cmakeProjectDotFileName = "cmake_project" 

class CMakeDependenciesGraphImport(tlp.ImportModule):
	def __init__(self, context):
		tlp.ImportModule.__init__(self, context)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)
		self.addStringParameter(cmakeProjectSourceDirParamName, "The root source directory of the CMake project")
		self.addStringParameter(cmakeExecutableParamName, """Optional parameter in order to provide the path to the CMake executable.
By default CMake executable path is assumed to be in your PATH environment variable""", "cmake")
		self.addStringParameter(cmakeParametersParamName, "Optionnal parameter for providing some parameters to CMake in order to correctly configure the project")
		
		

	def importGraph(self):
		# This method is called to import a new graph.
		# An empty graph to populate is accessible through the "graph" class attribute
		# (see documentation of class tlp.Graph).

		# The parameters provided by the user are stored in a Tulip DataSet 
		# and can be accessed through the "dataSet" class attribute
		# (see documentation of class tlp.DataSet).
	
		# The method must return a boolean indicating if the
		# graph has been successfully imported.
	
		# Check that we are using at least Tulip 4.8
		tulipVersionNumbers = list(map(lambda s: int(s), tlp.getTulipRelease().split('.')))	
		tulipVersionOk = tulipVersionNumbers[0] >= 4 and tulipVersionNumbers[1] >= 8	
		if not tulipVersionOk:
			if self.pluginProgress:
				self.pluginProgress.setError('Error : Minimum Tulip version to execute that plugin is 4.8.0')
			return False
	
		# get the CMake project source directory path
		cmakeProjectSourceDir = self.dataSet[cmakeProjectSourceDirParamName]
		
		# create a temporary directory that we will use as a CMake binary directory
		tmpdir = tempfile.TemporaryDirectory()

		# build the command line to execute cmake and generate the dot files
		command = self.dataSet[cmakeExecutableParamName] + ' ' + self.dataSet[cmakeParametersParamName] + ' ' \
		          + ' --graphviz=' + cmakeProjectDotFileName + ' ' + cmakeProjectSourceDir
		
		# create a temporary file in which we will redirect stderr
		stderrfile = tmpdir.name + '/stderr.txt'
		
		# execute the cmake process
		p = subprocess.Popen(command, cwd=tmpdir.name, shell=True, stdout=subprocess.PIPE, stderr=open(stderrfile, 'wb'))
		# add some execution feedback trough the plugin progress
		for line in p.stdout.readlines():
			lineStr = line.decode('utf-8')[:-1]
			if self.pluginProgress:
				self.pluginProgress.setComment(lineStr)
		
		# wait for the process to complete
		retval = p.wait()	
		
		# something went wrong
		if retval != 0:
			# read stderr file and transmit error string to the plugin progress
			errors = open(stderrfile, 'rb').read().decode('utf-8')
			if self.pluginProgress:
				self.pluginProgress.setError(errors)
			return False	
		
		# check if CMake has generated the expected dot file
		cmakeProjectDotFilePath = tmpdir.name + '/' + cmakeProjectDotFileName
		if not os.path.exists(cmakeProjectDotFilePath):
			cmakeProjectDotFilePath = tmpdir.name + '/' + cmakeProjectDotFileName + '.dot'
			if not os.path.exists(cmakeProjectDotFilePath):
				self.pluginProgress.setError("Error : the graphviz file has not been generated by CMake")
			return False	
		
		# import the dot file in Tulip trough the graphviz import plugin
		dotImportParams = tlp.getDefaultPluginParameters("graphviz", self.graph)
		dotImportParams['file::filename'] = cmakeProjectDotFilePath
		tlp.importGraph("graphviz", dotImportParams, self.graph)
		
		# set some visual attributes to the imported graph
		self.graph['viewSize'].setAllNodeValue(tlp.Size(1,1,1))
		self.graph['viewShape'].setAllNodeValue(tlp.NodeShape.Circle)
		
		# apply a force directed algorithm to draw the graph
		self.graph.applyLayoutAlgorithm('Fast Multipole Multilevel Embedder (OGDF)')
		
		# done
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("CMakeDependenciesGraphImport", "CMake dependencies graph", "Antoine Lambert", "24/11/2015", "", "1.0", "Misc")
