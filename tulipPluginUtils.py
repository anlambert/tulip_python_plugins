from tulip import *

def tulipVersionCheck(major, minor, patch, pluginProgress = None):
	tulipVersionNumbers = list(map(lambda s: int(s), tlp.getTulipRelease().split('.')))
	tulipVersionOk = tulipVersionNumbers[0] >= major and tulipVersionNumbers[1] >= minor and tulipVersionNumbers[2] >= patch
	if not tulipVersionOk and pluginProgress:
		pluginProgress.setError('Error : Minimum Tulip version to execute that plugin is 4.8.0')
	return tulipVersionOk
	
