import maya.cmds as commands
from functools import partial

class UIObject(object):
    def __init__(self,_label):
        self.UI = None
        self.label = _label
        self.parent = None
        self.bVisible = True
        self.bEnabled = True
        self.backgroundColor = None
        self.Construct()
        
    def GetUI(self):
        return self.UI

    def GetLabel(self):
        return self.label

    def Remove(self):
        commands.deleteUI(self.UI)
        self.UI = None
        
    def Construct(self):
        pass

    def SetVisibility(self,  visibility = True):
        self.bVisible = visibility
        commands.control(self.UI, edit = True, visible = visibility)
        
    def Enable(self, enable = True):
        self.bEnabled = enable
        commands.control(self.UI, edit = True, enable = enable)
        
    def SetParent(self, parent = None):
        self.parent = parent;
        commands.setParent(parent)
        
    def SetBackgroundColorThree(self, color ):
        self.backgroundColor = color
        commands.control(self.UI, edit = True, backgroundColor = self.backgroundColor)
        
    def SetBackgroundColorOne(self, value):
        self.backgroundColor = (value, value, value)
        commands.control(self.UI, edit = True, backgroundColor = self.backgroundColor)

class Window(UIObject):
    def __init__(self,_label,_widthHeight = [200,200],_minimizeButton = True,_sizeable = True):
        self.widthHeight = _widthHeight
        self.minimize = _minimizeButton
        self.sizeable = _sizeable
        return super(Window,self).__init__(_label)

    def Construct(self):
        self.UI = commands.window(title = self.label, widthHeight = self.widthHeight ,minimizeButton = self.minimize,sizeable = self.sizeable);
        super(Window,self).Construct()

    def Show(self):
        commands.showWindow(self.UI)
        

class Text(UIObject):
    def __init__(self, _label):
        return super(Text, self).__init__(_label)
        
    def Construct(self):
        self.UI = commands.text(label = self.label, align = "center")
        super(Text, self).Construct()
        
    def SetText(self, text):
        commands.text(self.UI, edit = True, label = text)
        
    def SetAlignment(self, alignment):
        commands.text(self.UI, edit = True, align = alignment)
        
    def SetHighlightColor(self, color = [1.0, 1.0, 1.0]):
        commands.text(self.UI, edit = True, highlightColor = color)
        
class FloatFieldGrp(UIObject):
    def __init__(self,_label,_numFields = 1,_width = 100,_startValues = [0.0, 0.0, 0.0, 0.0]):
        self.width = _width
        self.values = _startValues
        self.numFields = _numFields
        return super(FloatFieldGrp,self).__init__(_label)

    def Construct(self):
        self.UI = commands.floatFieldGrp(label = self.label, width = self.width, value = self.values, numberOfFields = self.numFields)
        super(FloatFieldGrp,self).Construct()

    def GetValue(self):
        return commands.floatFieldGrp(self.UI, query =True, value =True)
        
    def SetValue(self, value):
        commands.floatFieldGrp(self.UI, edit = True, value = value)
        
    def SetWidth(self, width = int):
        commands.floatFieldGrp(self.UI, edit = True, width = width)
        
    def SetHeight(self, height = int):
        commands.floatFieldGrp(self.UI, edit = True, height = height)
        
    def SetAdjustable(self, columnNumber = int):
        commands.floatFieldGrp(self.UI, edit = True, adjustableColumn = columnNumber)
    
    def SetAlignment(self, columnNumber = int, alignment = ""):
        commands.floatFieldGrp(self.UI, edit = True, columnAlign = [columnNumber, alignment]) 

    def SetAttachment(self, columnNumber = int, attachment = "", offset = int):
        commands.floatFieldGrp(self.UI, edit = True, columnAttach = [columnNumber, attachment, offset])

    def SetColumnWidth(self, columnNumber = int, width = int):
        commands.floatFieldGrp(self.UI, edit = True, columnWidth = [columnNumber, width])  
        
class IntFieldGrp(UIObject):
    def __init__(self,_label,_numFields = 1,_width = 100,_startValues = [0, 0, 0, 0]):
        self.width = _width
        self.values = _startValues
        self.numFields = _numFields
        return super(IntFieldGrp,self).__init__(_label)

    def Construct(self):
        self.UI = commands.intFieldGrp(label = self.label, width = self.width, value = self.values, numberOfFields = self.numFields)
        super(IntFieldGrp,self).Construct()

    def GetValue(self):
        return commands.intFieldGrp(self.UI, query =True, value =True)
        
    def SetValue(self, value):
        commands.intFieldGrp(self.UI, edit = True, value = value)
        
    def SetWidth(self, width = int):
        commands.intFieldGrp(self.UI, edit = True, width = width)
        
    def SetHeight(self, height = int):
        commands.intFieldGrp(self.UI, edit = True, height = height)
        
    def SetAdjustable(self, columnNumber = int):
        commands.intFieldGrp(self.UI, edit = True, adjustableColumn = columnNumber)
    
    def SetAlignment(self, columnNumber = int, alignment = ""):
        commands.intFieldGrp(self.UI, edit = True, columnAlign = [columnNumber, alignment]) 

    def SetAttachment(self, columnNumber = int, attachment = "", offset = int):
        commands.intFieldGrp(self.UI, edit = True, columnAttach = [columnNumber, attachment, offset])

    def SetColumnWidth(self, columnNumber = int, width = int):
        commands.intFieldGrp(self.UI, edit = True, columnWidth = [columnNumber, width]) 
        
class FloatSlider(UIObject):
    def __init__(self, _label, _min = 0.0, _max = 1.0, _step = .01):
        self.min = _min
        self.max = _max
        self.step = _step
        super(FloatSlider, self).__init__(_label)

    def Construct(self):
        self.UI =  commands.floatSliderGrp(adjustableColumn = 1,label = self.label,columnAlign =(1,"center"), field = True,min = self.min, max = self.max, value = 1, step = self.step)
        super(FloatSlider,self).Construct()

    def GetValue(self):
        return commands.floatSliderGrp(self.UI,q=True,v=True)
        
    def SetValue(self, value):
        commands.floatSliderGrp(self.UI,edit = True, v = value)
        
    def SetCommand(self, command):
        commands.floatSliderGrp(self.UI, edit = True, dragCommand = command)
        

class Button(UIObject):
    def __init__(self, _label,_width = 1):
        self.width = _width
        super(Button, self).__init__(_label)
             
    def Construct(self):
        self.UI = commands.button(label = self.label, width = self.width)
        super(Button,self).Construct()
        
    def SetCommand(self, command):
        commands.button(self.UI, edit = True , command = command)
        
    def Enable(self, enable):
        super(Button, self).Enable(enable)
        color = []
        if(enable):
            color = self.backgroundColor
        else:
            color = [0.3, 0.3, 0.3]
        self.SetBackgroundColor(self.backgroundColor)
              
class CheckBox(UIObject):
    def __init__(self, _label,_value = True):
        self.value = _value
        super(CheckBox,self).__init__(_label)

    def Construct(self):
        self.UI = commands.checkBox(label = self.label, value = self.value)
        super(CheckBox,self).Construct()
    
    def SetCommand(self, command):
        commands.checkBox(self.UI, edit = True , changeCommand  = command)
        
    def SetOnCommand(self, command):
        commands.checkBox(self.UI, edit = True , onCommand  = command)
        
    def SetOffCommand(self, command):
        commands.checkBox(self.UI, edit = True , offCommand  = command)
     
    def GetValue(self):
        return commands.checkBox(self.UI, query = True, value = True)
        
    def Enable(self, enable):
        super(CheckBox, self).Enable(enable)
        color = []
        if(enable):
            color = self.backgroundColor
        else:
            color = [0.3, 0.3, 0.3]
        commands.checkBox(self.UI, edit = True, enable = enable, backgroundColor = color)

class OptionMenu(UIObject):
    def __init__(self, _label, _items = None, _width = 200):
        self.width = _width
        self.items = _items;
        super(OptionMenu,self).__init__(_label)

    def Construct(self):
        self.UI = commands.optionMenu(label = self.label, width = self.width)
        for i in range(len(self.items)):
            commands.menuItem(label = self.items[i])
        super(OptionMenu,self).Construct()

    def GetValue(self):
         return commands.optionMenu(self.UI,query = True,v = True)
         
    def SetCommand(self, command):
        commands.optionMenu(self.UI, edit = True, changeCommand = command)
        
    def EnableBackground(self):
        commands.optionMenu(self.UI, edit = True, ebg = True)
        
    def Enable(self, enable):
        super(OptionMenu, self).Enable(enable)
        color = []
        if(enable):
            color = self.backgroundColor
        else:
            color = [0.3, 0.3, 0.3]
        commands.optionMenu(self.UI, edit = True, enable = enable, backgroundColor = color)

class TextField(UIObject):
    def __init__(self, _label, _width = 100):
        self.width = _width
        super(TextField,self).__init__(_label)

    def Construct(self):
        self.UI = commands.textFieldGrp(label = self.label, width = self.width)
        super(TextField,self).Construct()

    def GetText(self):
        return commands.textFieldGrp(self.UI, query = True, text = True)
        
    def SetText(self,text):
        commands.textFieldGrp(self.UI, edit = True, text = text)
     
class TextButton(UIObject):
    def __init__(self, _label, _buttonLabel = "Button", _edit = True):
        self.buttonLabel = _buttonLabel
        self.edit = _edit
        super(TextButton,self).__init__(_label)

    def Construct(self):
        self.UI = commands.textFieldButtonGrp(label = self.label, buttonLabel = self.buttonLabel, editable = self.edit)
        super(TextButton,self).Construct()
    
    def SetPlaceHolderText(self, text):
        commands.textFieldButtonGrp(self.UI, edit = True, placeholderText = text)
        
    def GetText(self):
        return commands.textFieldButtonGrp(self.UI, query = True, text = True)
        
    def SetText(self,text):
        commands.textFieldButtonGrp(self.UI,edit = True,text = text)
    
    def SetCommand(self, command):
        commands.textFieldButtonGrp(self.UI, edit = True , buttonCommand = command)
        
    def SetWidthHeight(self, widthHeight):
        commands.textFieldButtonGrp(self.UI, edit = True, width = widthHeight[0])
        commands.textFieldButtonGrp(self.UI, edit = True, height = widthHeight[1])
        
    def SetColumWidth(self, width):
        commands.textFieldButtonGrp(self.UI, edit = True, columnWidth = width)
    
    def SetColumnAlignment(self, alignment):
        commands.textFieldButtonGrp(self.UI, edit = True, columnAlign = alignment)
        
class Image(UIObject):
    def __init__(self, _label, _filePath = "",_width = 128,_height = 128):
        self.filepath = _filePath
        self.width = _width
        self.height = _height
        super(Image,self).__init__(_label)

    def Construct(self):
        self.UI = commands.image(width = self.width, height = self.height, image =self.filePath)
        super(Image,self).Construct()

class Column(UIObject):
    def __init__(self, _label):
        super(Column,self).__init__(_label)

    def Construct(self):
        self.UI = commands.columnLayout()
        super(Column, self).Construct()

    def SetWidth(self, width):
        commands.columnLayout(self.UI, edit = True, width = width)
        
    def SetColumnAlignment(self, alignment = "center"):
        commands.columnLayout(self.UI, edit = True, columnAlign = alignment)
        
    def SetRowSpacing(self, spacing = 0):
        commands.columnLayout(self.UI, edit = True, rowSpacing = spacing)
     
    def SetAdjustable(self, adjustable):
        commands.columnLayout(self.UI, edit = True, adjustableColumn = adjustable)


class Row(UIObject):
    def __init__(self, _label, _numColumns = 1, _width = [1, 30]):
        self.num = _numColumns
        self.width = _width
        super(Row,self).__init__(_label)

    def Construct(self):
        self.UI = commands.rowLayout(numberOfColumns = self.num , columnAttach = [1,"both", 0], columnWidth = self.width)
        super(Row,self).Construct()

class Tab(UIObject):
    def __init__(self, _width = 100.0, _height = 100.0, _margin = [0.0,0.0]):
        self.width  = _width;
        self.height = _height;
        self.margin = _margin;
        super(Tab, self).__init__("")
        
    def Construct(self):
        self.UI = commands.tabLayout(width = self.width, height = self.height , innerMarginWidth = self.margin[0], innerMarginHeight = self.margin[1])
        super(Tab, self).Construct()
        
    def SetWidthHeight(self, width = 100.0, height = 100.0):
        commands.tabLayout(self.UI, edit = True, width = width)
        commands.tabLayout(self.UI, edit = True, height = height)
        
    def SetImage(self, image = ""):
        commands.tabLayout(self.UI, edit = True, image = image)
        
    def SetImageVisibility(self, visibility):
        commands.tabLayout(self.UI, edit = True, imageVisible = visibility)
        
    def SetTabLabel(self, labels = None):
        commands.tabLayout(self.UI, edit = True, tabLabel = labels)
        
    
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
    def ParentSelected():
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
    def ParentShapes():
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