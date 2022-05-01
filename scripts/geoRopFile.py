import hou
out = hou.node("/out")

def createNodes():
    for node in hou.selectedNodes():
        curParent = node.parent().name()
        
        rop = out.createNode("geometry",node.name())
        rop.moveToGoodPosition()
        file = node.parent().createNode("file")
        file.setPosition(node.position() + hou.Vector2(0,-1))

        try:
            outNode = node.outputs()[0]
            outNode.setInput(0,file)
        except:
            print 'no output'
        
        rop.parm("soppath").set(node.path())
        ropOutput = '`chs("'+ rop.path() +'/sopoutput")`'
        file.parm("file").set(ropOutput)
        file.parm("missingframe").set(1)
        
        txt = 'create "' + rop.path()+'" and "'+ file.path() +'"'
        hou.ui.setStatusMessage(txt,severity=hou.severityType.ImportantMessage)
        

if len(hou.selectedNodes())>0:
    node = hou.selectedNodes()[0]      
    nodeType = hou.hscript('optype -s %s' % node.path())[0][:-1]  
    if nodeType == "sop":
        txt = "Create 'geometry rop' and 'file' nodes?"
        #if hou.ui.displayMessage(txt, buttons=('OK','Cancel',)) == 0 : 
        createNodes()