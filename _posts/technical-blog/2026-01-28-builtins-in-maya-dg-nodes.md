---
title: "KTCG.ART | Modifying standard Maya dependency graph node programming syntax to use getattr and setattr Builtins"
shortname: "getattr, settattr, and compound attributes in  Maya dependency graph nodes"
date: "2026-01-28"
tags: 
  - "maya"
  - "python"
  - "graphics"
cover-image: "/img/2026-01-28-builtins-in-maya-dg-nodes/cover-image.jpg"
cover-big: "/img/2026-01-28-builtins-in-maya-dg-nodes/cover-big.jpg"
show-date: T
type: blog
featured: T
uri: "/2025/01/28/maya-node-getattr-setattr.html"
description: A writeup of using the getattr and setattr builtin functions when creating custom Autodesk Maya nodes using Python.
permalink: maya-node-getattr-setattr
---
The purpose of this post is to give Maya Python developers an example of using `getattr` and `setattr` to set class attributes when writing a custom <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Dependency_graph_plug_ins_Attributes_html">dependency graph plugin</a>. This technique allows programmers to take advantage of Python language features with minimal changes to the standard Maya dependency graph node programming syntax laid out by Autodesk. This post includes:
- An example of syntax that uses `getattr` and `setattr` instead of the hardcoded attribute names commonly shown in examples of dependency graph nodes
- An example of working with compound attributes
- A node development test loop
- Start-to-finish walkthrough of setting up and testing a node, with completed code

I use this technique in several nodes that are part of my custom animation pipeline. You can see my pipeline in-action by checking out <a href="cg-projects#bugmuthur">Bugmuthur</a>. In my pipeline, the node attribute names are defined by an external configuration. Taking advantage of the builtins allows easier implementation of object-oriented programming patterns. For instance, you could pass node classes to a builder method. Finally, using the builtins with a compound attribute allows a low-impact solution to creating attributes with unknown names. 
<!--break-->

**GOAL**: I will replicate my animation pipeline's use case with a simple example node that
- Has a compound attribute with five children attributes
- Has a typed attribute for a user-defined string
- Has a compute function that multiplies together the attributes called out by the user-defined string.

<div class='captioned-image'>
    <img alt="a maya node" src='img/2026-01-28-builtins-in-maya-dg-nodes/finished-node.jpg' style='max-width:max-content;'>
    <p>My example node</p>
</div>

**SET UP**: The first step of creating a new node is fussing over the unique hexacimal numeric ID to assign to it. If the node is internal to your organization, you can use any hexadecimal number `0 - 0x7fff`. If you intend to distribute your node publicly, you can also request to reserve a block of nodes IDs with Autodesk. I was able to easily reserve a 64 ID block on the <a href="https://adn.autodesk.io/maya?_gl=1*l5ck3i*_ga*ODcyNDYzMDcxLjE3Njk2MjcwNjc.*_ga_NZSJ72N6RX*czE3Njk2MjcxMDUkbzEkZzEkdDE3Njk2MjcxNDAkajI1JGwwJGgw">Autodesk Developer Network</a> in Novemeber 2024.

For this example, I'll use `0x00141A44`. You can read more about the Maya Node TypeIDs <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Maya_Python_API_Dependency_Graph_Plug_in_Basics_Dependency_Graph_Plug_ins_html">here</a> and review their Python 2.0 API reference <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=MAYA_API_REF_py_ref_class_open_maya_1_1_m_type_id_html">here</a>.

When starting a new node, I make a little skeleton with the essential node functions:

{% highlight python %}
{% include example_node_py/01_skeleton.py %}
{% endhighlight %}

I also make a little script to load the node called `load.py`.

{% highlight python %}
{% include example_node_py/load_example.py %}
{% endhighlight %}

**INITIALIZE function**: Example initialize functions will generally look something like this:

{% highlight python %}
def initialize():
  n_attr = om.MFnNumericAttribute()
  ExampleNode.output = n_attr.create("output", "out", MFnNumericData::kFloat, 0.0)
  om.MPxNode.addAttribute(ExampleNode.output)
{% endhighlight %}

An update to this syntax using the builtins looks like this:
{% highlight python %}
def initialize():
  n_attr = om.MFnNumericAttribute()
  op = n_attr.create("output", "out", MFnNumericData::kFloat, 0.0)
  setattr(ExampleNode,"output",op)
  om.MPxNode.addAttribute(getattr(ExampleNode,"output"),op)
{% endhighlight %}

Additionally, note that the attribute names are set as class attributes:
{% highlight python %}
class ExampleNode(om.MPxNode):
    id = om.MTypeId(0x00141A44)
    output = None
    inputs = None
    called_out = None
{% endhighlight %}

Here is the initialize function in my final node, written to the specifications laid out in the 'GOAL' section:
{% highlight python %}
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
{% endhighlight %}


**COMPUTE function**: Example compute functions will generally look something like this:
{% highlight python %}
def compute(self, plug, datablock):
    # Recall that the compute function is called on each plug for the node
    if plug == ExampleNode.output:
        called_out = datablock.inputValue(ExampleNode.called_out).asString()
        # DO SOME OPERATIONS TO CALCULATE A VALUE FOR ExampleNode.output, store as a variable called output_value
        out_handle = datablock.outputValue(plug)
        out_handle.setFloat(output_value)
        out_handle.setClean()
    return self
{% endhighlight %}

An update to this syntax using the builtins looks like this:
{% highlight python %}
def compute(self, plug, datablock):
    # Recall that the compute function is called on each plug for the node
    if plug == getattr(ExampleNode,"output"):
        called_out = datablock.inputValue(getattr(ExampleNode,"called_out")).asString()
        # DO SOME OPERATIONS TO CALCULATE A VALUE FOR ExampleNode.output, store as a variable called output_value
        out_handle = datablock.outputValue(plug)
        out_handle.setFloat(output_value)
        out_handle.setClean()
    return self
{% endhighlight %}

Here is the compute function in my final node, written to the specifications laid out in the 'GOAL' section:
{% highlight python %}
def compute(self, plug, datablock):
    if plug == getattr(ExampleNode,"output"):
        # ExampleNode.output is the MObject itself. Not mine! The datablock allows me to access the value
        called_out = datablock.inputValue(getattr(ExampleNode,"calledOut")).asString()
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
{% endhighlight %}


**FINAL CODE**: Here is my completed node, written to the specifications in the 'GOAL' section:

{% highlight python %}
{% include example_node_py/02_node.py %}
{% endhighlight %}


**TEST LOOP**: Here is a test loop for this node. You can write a script for the test loop. I prefer to test with the UI to get a sense of the artist workflow when using my node.
- (Re)launch Maya. 
  - You have to do this each time you update the node code
- Run the load.py script. This will load the node.
  - **Windows > General Editors > <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=GUID-7C861047-C7E0-4780-ACB5-752CD22AB02E">Script Editor</a>**
  - From the Script Editor, **File > Open Script**, and open your `load.py` file
  - Highlight all of code and hit the **Play** button
  - You have to do this each time you update the node code until you're ready to <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Distributing_Maya_Plug_ins_html">distribute your plugin</a>
<div class='captioned-image'>
    <img alt="maya script editor" src='img/2026-01-28-builtins-in-maya-dg-nodes/script-editor.jpg' style='max-width:max-content;'>
    <p>Maya Script Editor. For my development projects I use Chris Zurbrigg's <a href="https://zurbrigg.com/charcoal-editor-2">Charcoal Editor</a> instead</p>
</div>
- Add the node to your scene
  - **Windows > <a href="https://help.autodesk.com/view/MAYAUL/2026/ENU/?guid=GUID-23277302-6665-465F-8579-9BC734228F69">Node Editor</a>**.
  - Hit Tab and begin typing **ExampleNode_py**. Note that 'ExampleNode_py' is the name I gave the node in the `registerPlugin` function
  - Select **ExampleNode_py** when it comes up
  - You can see a node added to the Node Editor
<div class='captioned-image'>
    <img alt="maya node editor" src='img/2026-01-28-builtins-in-maya-dg-nodes/node-editor.jpg' style='max-width:max-content;'>
    <p>Maya Node Editor. You can certainly add the node to your scene using the <a href="https://help.autodesk.com/cloudhelp/ENU/MayaCRE-Tech-Docs/CommandsPython/createNode.html">createNode command</a> instead.</p>
</div>
- Select the node and open the Attribute Editor (**Windows > General Editors > Attribute Editor**)
<div class='captioned-image'>
    <img alt="a maya node" src='img/2026-01-28-builtins-in-maya-dg-nodes/finished-node.jpg' style='max-width:max-content;'>
    <p>The node should appear like this in the Attribute Editor</p>
</div>
- Trigger the `compute` function
  - Recall that, on each scene evaluation Maya <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Dependency_graph_plug_ins_html">only recomputes the values required to update "dirty" plugs</a>.
  - In this instance, messing with the **Inputs** child attributes or the **Called Out** attribute with trigger the `compute` function. 
  - Set the **Called Out** attribute to the following string: 'attrA,attrB,attrE'
  - Set the five inputs attributes to the following values: `'attrA:2.0','attrB:6.0','attrC:0.0','attrD:100.0','attrE:1.5'`
  - Observe that the **Output** attribute is updated to `(2.0 * 6.0 * 1.5) = 18`
<div class='captioned-image'>
    <img alt="a maya node" src='img/2026-01-28-builtins-in-maya-dg-nodes/tested-node.jpg' style='max-width:max-content;'>
    <p>Notice how attrC and attrD values did not get included in the product</p>
</div>

**(Optional) TEST USING SCENE TIME**: My favorite way to test a node with numeric inputs is to hook it up to the <a href="https://help.autodesk.com/cloudhelp/ENU/MayaCRE-Tech-Docs/Nodes/time.html">scene's time node</a>. This forces the compute function to re-evaluate each frame, meaning you can observe the node behavior by simply scrubbing the timeline.
- Locate the **time1** node
  - In the Outliner, under Display, untick 'DAG objects only'. <a href="https://help.autodesk.com/view/MAYAUL/2026/ENU/?guid=GUID-5029CF89-D420-4236-A7CF-884610828B70">'DAG' is not the same as 'dependency graph'</a>
  - Locate the node called **time1**. You can use the search bar to find it.
  - Select it
<div class='captioned-image'>
    <img alt="finding the time1 node in the outliner" src='img/2026-01-28-builtins-in-maya-dg-nodes/time-1.jpg' style='max-width:max-content;'>
    <p>There is only one time1 node per scene</p>
</div>
- Add the **time1** node to the Node Editor
  - In the Node Editor, hit the **Add selected nodes to graph** button
  - The **time1** node will pop up in the editor
  - You can also locate the **time1** node using a code snippet. `time1_node = cmds.ls(type='time')[0]`
<div class='captioned-image'>
    <img alt="maya node editor add node button" src='img/2026-01-28-builtins-in-maya-dg-nodes/add-node.jpg' style='max-width:max-content;'>
    <p>The add node button</p>
</div>
- Connect the **time1** node to the **Attr A** input on the ExampleNode
  - Expose all the attributes on the ExampleNode via **right-click > Show All Attributes**
  - Expand the **'Inputs'** attribute
  - Click + drag on the **time1** node's **Out Time** plug to connect it to the **ExampleNode** node's **Attr A** plug
<div class='captioned-image'>
    <img alt="maya node editor connected nodes" src='img/2026-01-28-builtins-in-maya-dg-nodes/connected-node.jpg' style='max-width:max-content;'>
    <p>If you want to hide the unconnected attributes after doing this process, hit the hamburger icon in the ExampleNode upper-right corner</p>
</div>
- Returning to the ExampleNode in the Attribute Editor, we now see the **Attr A** attribute has an incoming connection. Scrub the timeline to observe **Output** attribute updating based on current frame
<div class="captioned-image" style="max-width:500px">
    <video controls autoplay loop muted preload="none">
        <source src="/img/2026-01-28-builtins-in-maya-dg-nodes/time-driven.mp4" type="video/mp4" />
        <source src="/img/2026-01-28-builtins-in-maya-dg-nodes/time-driven.webm" type="video/webm" />
    </video>
    <p>updating based on time</p>
</div>


**ADDITIONAL RESOURCES**: I hope experimenting with builtins in the context of Maya dependency graph nodes gives you a better grasp of the Maya Python API 2.0. Here are some of my favorite resources to learn more about the API: 
- <a href="https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Maya_API_introduction_MObject_html">MObject entry in the Maya API</a>
- <a href="https://images.autodesk.com/adsk/files/maya_api_whitepaper.pdf?">This 2007 whitepaper about the Maya API
- <a href="https://www.amazon.com/Complete-Maya-Programming-Extensive-Kaufmann/dp/1558608354">Complete Maya Programming by David Gould</a>. My copy is one of my most cherished possessions. It's written for the C++ API (because the Python API did not exist in 2003), which I really like to read when I'm doing Python development because I feel it allows me a better grasp of the underlying architecture. 
- This 2012 webcast series by Kristine Middlemiss really rocks if you are trying to wrap your head around the Maya architecture. 
  - Autodesk has the download hosted here `http://download.autodesk.com/media/adn/MayaAPI_Webcast_Recordings.zip`
  - My VLC media player was having a hard time with the .wmv files that are extracted from the ZIP Archive, so I used FFMPEG in the terminal to convert them. From the folder I extracted into, I ran: `ffmpeg -i livemeeting.wmv -c:v libx264 -crf 23 -c:a aac -q:a 100 output.mp4`
<br>
