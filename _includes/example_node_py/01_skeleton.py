from maya.api import OpenMaya as om
maya_useNewAPI = True

class ExampleNode(om.MPxNode):
    id = om.MTypeId(0x00141A44)

    @staticmethod
    def creator():
        return ExampleNode()
    
    @staticmethod
    def initialize():
        return
    
    def compute(self, plug, datablock):
        return self
    
def initializePlugin(mobject):
	mplugin = om.MFnPlugin(mobject)
	try: 
		node_name = 'ExampleNode_py'
		node_id = ExampleNode.id
		mplugin.registerNode(node_name, node_id, ExampleNode.creator, ExampleNode.initialize)
	except:
		print("Failed to register node: %s" % node_name)
		raise
      
def uninitializePlugin(mobject):
	mplugin = om.MFnPlugin(mobject)

	try:
		node_name = 'ExampleNode_py'
		node_id = ExampleNode.id
		mplugin.deregisterNode(node_id)
	except:
		print("Failed to deregister node: %s" % node_name)
