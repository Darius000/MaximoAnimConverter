import maya.cmds as commands
from functools import partial

class Commands():
    @staticmethod
    def Error(text):
        commands.error(text)
    @staticmethod
    def Warning(text):
        commands.warning(text)
        
    @staticmethod
    def SetTime(time):
        commands.currentTime(time)
        return
    
    @staticmethod
    def Delete(uiobject):
        if(uiobject is not None):
            commands.deleteUI(uiobject.UI)
    
    @staticmethod
    def DeselectAll():
        selected = Commands.GetSelected()
        for i in selected:
            Commands.Deselect(i)
    
    @staticmethod
    def Deselect(object):
        if(object):
            #print("Deselected " + object)
            commands.select(object, d = True)
      
    @staticmethod
    def Select(object):
        if(object):
            #print("Selected " + object)
            commands.select(object)
            
    @staticmethod
    def FlipFlop(A,first, second):
        if(A):
            return first
        else:
            return second
    
    @staticmethod
    def FlipBool(a):
        a = not a   
    
    @staticmethod
    def GetSelected():
        selected = commands.ls(sl = True)
        if(len(selected) > 0):
            return selected
        else:
            return ""
    
    @staticmethod
    def GetNumSelected():
        selected = commands.ls(sl = True)
        return len(selected)

    @staticmethod
    def Rename(name = "",newname = ""):
        commands.rename(name,newname)
        return newname

    
    @staticmethod
    def GetTranslation(name):
        return commands.getAttr(name + ".translate")

    @staticmethod
    def GetRotation(name):
        return commands.getAttr(name + ".rotate")

    @staticmethod
    def GetScale(name):
        return commands.getAttr(name + ".scale")

    @staticmethod
    def ParentObjects(first = "",second = ""):
        if(first and second):
            Commands.DeselectAll()
            commands.parent(first,second)
            return
        else:
            Commands.Error("no objects to parent")
            return
    
    @staticmethod
    def ParentSelected(*args):
        if(Commands.GetNumSelected() > 1):
            children = []
            first = Commands.GetSelected()[0]
            for i in range(len(Commands.GetSelected()) - 1):
                children.append(Commands.GetSelected()[i + 1])
            commands.parent(first,children)
            #Commands.Error("Object parented")
        elif(Commands.GetNumSelected() > 0):
            Commands.Error("Select at least two objects")
        else:
            Commands.Error("No objects selected")
            
    @staticmethod
    def ParentShapes(*args):
        children = [] 
        first = Commands.GetSelected()[0]
        for i in range(len(Commands.GetSelected()) - 1):
            children.append(Commands.GetSelected()[i + 1])
        commands.parent(first,children,absolute = True,shape = True)  

    @staticmethod
    def CreateJoint(location, radius = 1.0):
        return commands.joint(position = location, radius = radius)

    @staticmethod
    def KeySelectedAttribute(objectName, attributes):
        for attr in range(len(attributes)):
            if(commands.getAttr(objectName + "." + attributes[attr],k = True) or commands.getAttr(objectName + "." + attributes[attr],channelBox = True)):
                commands.setKeyframe(objectName + "." + attributes[attr])

    @staticmethod
    def SelectAllAnimationKeys(objectName, attributes):
        for attr in range(len(attributes)):
            return commands.selectKey(objectName,attribute = attributes[attr],time=())  

    @staticmethod
    def GetAnimatedTimes(objectName, attribute):
        return commands.keyframe(objectName,q= True, attribute = attribute) or []

    @staticmethod
    def GetAnimatedAttributeValues(attribute):
        return commands.keyframe(attribute = attribute, q= True, vc = True) or []
      
