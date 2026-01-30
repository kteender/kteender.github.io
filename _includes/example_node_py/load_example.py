import maya.cmds as cmds
import platform

def load_plugin():
	if platform.system() == 'Windows':
		plugin_path = 'The path to your plugin if you are developing on Windows'
	else:
		plugin_path = 'The path to your plugin if you are developing on Unix'
	cmds.loadPlugin(plugin_path)

load_plugin()