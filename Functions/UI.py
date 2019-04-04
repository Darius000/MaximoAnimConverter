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

class Control(UIObject):
    def __init__(self,_label):
        return super(Control,self).__init__(_label)
        
    def SetAnnotation(self, _annotation):
        commands.control(self.UI, edit = True, annotation = _annotation)
        
class Window(UIObject):
    def __init__(self,_label,_widthHeight = [200,200],menuBar = False,_minimizeButton = True,_sizeable = True):
        self.widthHeight = _widthHeight
        self.minimize = _minimizeButton
        self.sizeable = _sizeable
        self.menuBar = menuBar
        return super(Window,self).__init__(_label)

    def Construct(self):
        self.UI = commands.window(title = self.label, menuBar = self.menuBar, widthHeight = self.widthHeight ,minimizeButton = self.minimize,sizeable = self.sizeable);
        super(Window,self).Construct()

    def Show(self):
        commands.showWindow(self.UI)
        
    def MenuBar(self, show, barWidth = 200):
        commands.window(self.UI, edit = True, mainMenuBar = show)
        

class Text(Control):
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
        
class FloatFieldGrp(Control):
    def __init__(self,_label,_numFields = 1,_width = 100,_startValues = [0.0, 0.0, 0.0, 0.0]):
        self.width = _width
        self.values = _startValues
        self.numFields = _numFields
        return super(FloatFieldGrp,self).__init__(_label)

    def Construct(self):
        self.UI = commands.floatFieldGrp(label = self.label, width = self.width, value = self.values, numberOfFields = self.numFields)
        super(FloatFieldGrp,self).Construct()

    def GetValues(self):
        return commands.floatFieldGrp(self.UI, query =True, value =True)
        
    def GetValue1(self):
        return commands.floatFieldGrp(self.UI, query =True, value1 =True)
        
    def SetValue1(self, value):
        commands.floatFieldGrp(self.UI, edit = True, value1 = value)
        
    def SetValues(self, value):
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
        
class IntFieldGrp(Control):
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
        
class FloatSlider(Control):
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
        

class Button(Control):
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
              
class CheckBox(Control):
    def __init__(self, _label, numBoxes = 1):
        self.numBoxes = numBoxes
        super(CheckBox,self).__init__(_label)

    def Construct(self):
        self.UI = commands.checkBoxGrp(label = self.label, numberOfCheckBoxes = self.numBoxes)
        super(CheckBox,self).Construct()
    
    def SetCommand1(self, command):
        commands.checkBoxGrp(self.UI, edit = True , changeCommand1  = command)

    def SetCommand2(self, command):
        commands.checkBoxGrp(self.UI, edit = True , changeCommand2  = command)

    def SetCommand3(self, command):
        commands.checkBoxGrp(self.UI, edit = True , changeCommand3  = command)

    def SetCommand4(self, command):
        commands.checkBoxGrp(self.UI, edit = True , changeCommand4  = command)
        
    def SetOnCommand1(self, command):
        commands.checkBoxGrp(self.UI, edit = True , onCommand1  = command)

    def SetOnCommand2(self, command):
        commands.checkBoxGrp(self.UI, edit = True , onCommand2  = command)

    def SetOnCommand3(self, command):
        commands.checkBoxGrp(self.UI, edit = True , onCommand3  = command)

    def SetOnCommand4(self, command):
        commands.checkBoxGrp(self.UI, edit = True , onCommand4  = command)
        
    def SetOffCommand1(self, command):
        commands.checkBoxGrp(self.UI, edit = True , offCommand1  = command)

    def SetOffCommand2(self, command):
        commands.checkBoxGrp(self.UI, edit = True , offCommand2  = command)

    def SetOffCommand3(self, command):
        commands.checkBoxGrp(self.UI, edit = True , offCommand3  = command)

    def SetOffCommand4(self, command):
        commands.checkBoxGrp(self.UI, edit = True , offCommand4  = command)
     
    def GetValue1(self):
        return commands.checkBoxGrp(self.UI, query = True, value1 = True)

    def GetValue2(self):
        return commands.checkBoxGrp(self.UI, query = True, value2 = True)

    def GetValue3(self):
        return commands.checkBoxGrp(self.UI, query = True, value3 = True)

    def GetValue4(self):
        return commands.checkBoxGrp(self.UI, query = True, value4 = True)
    
    def SetValue1(self, value):
        commands.checkBoxGrp(self.UI, edit = True, value1 = value)

    def SetValue2(self, value):
        commands.checkBoxGrp(self.UI, edit = True, value2 = value)

    def SetValue3(self, value):
        commands.checkBoxGrp(self.UI, edit = True, value3 = value)

    def SetValue4(self, value):
        commands.checkBoxGrp(self.UI, edit = True, value4 = value)
        
    def Enable(self, enable):
        super(CheckBox, self).Enable(enable)
        color = []
        if(enable):
            color = self.backgroundColor
        else:
            color = [0.3, 0.3, 0.3]
        commands.checkBoxGrp(self.UI, edit = True, enable = enable, backgroundColor = color)

class OptionMenu(Control):
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
         
    def SetValue(self, value):
         commands.optionMenu(self.UI, edit = True, v = value)
         
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

class TextField(Control):
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
     
class TextButton(Control):
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
        
class Image(Control):
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

class Menu(UIObject):
    def __init__(self, label, tearOff = False):
        self.tearOff = tearOff;
        super(Menu, self).__init__(label)
        
    def Construct(self):
        self.UI = commands.menu(label=self.label, tearOff = self.tearOff)
        super(Menu, self).Construct()
    
    def AddItem(self, label, command):
        commands.menuItem(label = label, c = command)
    
    def AddDivider(self, label = ""):
        commands.menuItem(label = label, divider = True)
    