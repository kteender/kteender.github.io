from maya.api import OpenMaya as om
maya_useNewAPI = True

my_dict = {
  "attrA":"aa",
  "attrB":"ab",
  "attrC":"ac",
  "attrD":"ad",
  "attrE":"ae"
}

class ExampleNode(om.MPxNode):
    id = om.MTypeId(0x00141A44)
    output = None
    inputs = None
    called_out = None

    @staticmethod
    def creator():
        return ExampleNode()
    
    @staticmethod
    def initialize():
        # The attribute Function Sets. Operate on the data using the Function Set!
        n_attr = om.MFnNumericAttribute()
        c_attr = om.MFnCompoundAttribute()
        t_attr = om.MFnTypedAttribute()

        # The attribute MObjects. The data itself. Not mine!
        output = n_attr.create('output', 'op', om.MFnNumericData.kFloat, defaultValue=1.0)
        setattr(ExampleNode, "output", output)
        inputs = c_attr.create('inputs', 'ip')
        setattr(ExampleNode, "inputs", inputs)
        value_names = t_attr.create("called_out", "co", om.MFnData.kString)
        setattr(ExampleNode, "called_out", value_names)

        om.MPxNode.addAttribute(getattr(ExampleNode, "output"))
        om.MPxNode.addAttribute(getattr(ExampleNode, "called_out"))

        for k,v in my_dict.items():
            inp = n_attr.create(k, v, om.MFnNumericData.kFloat, defaultValue=0.0)
            # I do not need to use addAttribute on children of compound attributes. addChild is sufficient
            c_attr.addChild(inp)

            # I add all the child attributes to the node class so I can access them in the compute function
            # Not strictly necessary -- could also iterate through compound plug children. But this solution is clean.
            setattr(ExampleNode,k,inp)
        
        # Notice how I don't add the compound attribute until I add all its children
        # This doesn't matter for the typed attributes and numeric attributes, but for compound attributes
        # called addChild on a compound attribute that has already been added will crash Maya when creating the node
        om.MPxNode.addAttribute(getattr(ExampleNode, "inputs"))

        om.MPxNode.attributeAffects(getattr(ExampleNode, "called_out"), getattr(ExampleNode, "output"))

        # Note how I set the compound attribute as the affecting attribute, not each child
        om.MPxNode.attributeAffects(getattr(ExampleNode, "inputs"), getattr(ExampleNode, "output"))
        return
    
    def compute(self, plug, datablock):
        if plug == getattr(ExampleNode,"output"):
            # ExampleNode.output is the MObject itself. Not mine! The datablock allows me to access the value
            called_out = datablock.inputValue(getattr(ExampleNode,"called_out")).asString()
            if called_out == '':
                return self
            called_out_attr_names = called_out.split(',')
            called_out_inputs = [getattr(ExampleNode,an) for an in called_out_attr_names]
            product = 1.0
            for inp in called_out_inputs:
                multiple = datablock.inputValue(inp).asFloat()
                product = product * multiple
            
            out_handle = datablock.outputValue(plug)
            out_handle.setFloat(product)
            out_handle.setClean()
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
