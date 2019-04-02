import maya as maya
import maya.cmds as commands
from functools import partial
import ConfigParser
import os

config = ConfigParser.RawConfigParser()
configDir = os.path.dirname(__file__) + "\config.cfg";

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
    
    def SetValue(self, value):
        commands.checkBox(self.UI, edit = True, value = value)
        
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
      

class Converter:
    def __init__(self):
        self.bConvertAnimInPlace    = True
        self.bCutAllKeys            = False
        self.bRootJoint             = None
        self.rootName               = None
        self.hipName                = None
        self.worldUpAxis            = None
        self.worldForwardAxis       = None
        self.ffHeight               = None
        self.btnHeight              = None
        self.omClamp                = None
        self.btnCutPaste            = None
        self.exportWindow           = None
        self.textField              = None
        self.directory              = ""
        
    def Construct(self):
        '''window'''
        window                                          = Window("Maximo To Unreal", (500, 400), True, False)
        window.MenuBar(True)
        menu = Menu("File", True)
        menu.AddItem("Save Settings", self.SaveConfig)
        menu.AddItem("Reset Settings", self.ResetConfig)
        menu.AddDivider()
        menu.AddItem("Quit", "")
        '''tab'''
        tabs                                            = Tab(500.0, 500.0, (50.0,50.0))
        '''columns'''
        column1                                         = Column("column1")
        column1.SetAdjustable(True)
        column1.SetRowSpacing(10)
        column1.SetWidth(500.0)
        column1.SetBackgroundColorOne(.3)
        
        self.textDirectory = TextButton("Animation Export Directory", "Browse")
        self.textDirectory.SetCommand(self.SetDirectory)
        
        self.worldUpAxis                                = OptionMenu("World Up         ",["Y","Z"], 200)
        self.worldForwardAxis                           = OptionMenu("World Forward",["Z","X"], 200)
        
        self.rootName                                   = TextField("Root Joint Name" , 200)
        self.hipName                                    = TextField("Hip Joint Name" , 200)
        
        bttnParent = Button("Parent", 200)
        bttnParent.SetCommand('Commands.ParentSelected()')
        
        bttnRootJoint = Button("Add Root Joint", 200)
        bttnRootJoint.SetCommand(self.AddRootJoint)
        
        Button("Undo <-", 200.0).SetCommand("commands.undo()")
        Button("Redo ->", 200.0).SetCommand("commands.redo()")
        
        column1.SetParent( tabs.GetUI() )
        
        '''column2'''
        column2                 = Column("column2")
        column2.SetAdjustable(True)
        column2.SetRowSpacing(10)
        column2.SetWidth(500.0)
        column2.SetBackgroundColorOne(.3)
        
        self.bRootJoint                                     = CheckBox("Add Root Joint", False)
        
        bttnConvert                                         = Button("Convert Animation To In Place", 200)
        bttnConvert.SetCommand(self.ConvertAnimationToInPlace)
        Button("Export Animation", 200).SetCommand(self.ShowExportWindow)
        
        Button("Undo <-", 200.0).SetCommand("commands.undo()")
        Button("Redo ->", 200.0).SetCommand("commands.redo()")
        
        column2.SetParent( tabs.GetUI() )
        
        #column2 controls
        column3                                             = Column("column3")
        column3.SetAdjustable(True)
        column3.SetRowSpacing(10)
        column3.SetWidth(500.0)
        column3.SetBackgroundColorOne(.3)
        
        '''Hip joint height'''
        self.ffHeight                                       = FloatFieldGrp("Hip Height", 1, 200)
        self.ffHeight.SetAdjustable(1)
        self.ffHeight.SetAlignment(1, "left")
        
        self.btnHeight                                      = Button("Set Hip Height", 200)
        self.btnHeight.SetCommand(self.GetAndSetHipHeight)
        
        '''Add root motion button'''
        self.omClamp                                        = OptionMenu("Clamp Root",["UnConstrain 0","Constrain 0"], 200)
        self.btnCutPaste                                    = Button("Add Root Motion", 200)
        self.btnCutPaste.SetCommand(self.CutAndPasteKeys)
        
        Button("Export Animation", 200).SetCommand(self.ShowExportWindow)
        
        Button("Undo <-", 200.0).SetCommand("commands.undo()")
        Button("Redo ->", 200.0).SetCommand("commands.redo()")
        
        column3.SetParent( tabs.GetUI() )
        
       
        #add colums to tab
        tabs.SetTabLabel(((column1.GetUI(), "Settings"), (column2.GetUI(), "Movement to InPlace"), (column3.GetUI(), "Root Motion")))

        window.Show()
        
        self.LoadConfig()
        
    def SetDirectory(self, *args):
        fileDir = commands.fileDialog2(fileMode = 2,dialogStyle = 2, fileFilter = 'FBX export')
        print(fileDir)
        if(len(fileDir) > 0):
            self.directory = fileDir[0]
        else:
            self.directory = ""
        self.textDirectory.SetText(self.directory)
    
    def ShowExportWindow(self, *args):
        self.exportWindow = Window("Export", (500, 100), False, False)
        
        column = Column("Export column")
        column.SetAdjustable(True)
        column.SetRowSpacing(10)
        column.SetWidth(200.0)
        
        self.textField2 = TextField("Animation Name", 300)
        
        button = Button("Export", 50)
        button.SetCommand(self.ExportAnimation)
        self.exportWindow.Show()
        
    def ExportAnimation(self, *args):
        if(self.rootName.GetText()):
            Commands.Select(self.rootName.GetText())
            commands.file(self.directory + "/" + self.textField2.GetText(), es = True, options = "v=0" , force = True, typ = "FBX export", pr = True )
            self.exportWindow.Remove()
        else:
            Commands.Warning("Root joint not provided in Settings")
        
    def ConvertAnimationToInPlace(self, *args):
        Commands.DeselectAll()
        if(self.bRootJoint.GetValue()):
            self.AddRootJoint()
        if(self.hipName.GetText() and self.rootName.GetText()):
            Commands.Select(self.hipName.GetText())
            Commands.SetTime(0)
            height = Commands.GetTranslation(self.hipName.GetText())[0][1]
            times = Commands.GetAnimatedTimes(self.hipName.GetText(), "translate" + self.worldUpAxis.GetValue())           
            keys = commands.keyframe(self.hipName.GetText() + "_" + "translate" + self.worldUpAxis.GetValue(), q= True, vc = True) or []
            for f in range(len(keys)):
                if(keys[f] > height):                  
                    commands.cutKey(self.hipName.GetText(), attribute = "translate" + self.worldUpAxis.GetValue(), index= (f, (f)))
                    commands.setKeyframe(self.hipName.GetText(),attribute = "translate" + self.worldUpAxis.GetValue(), time = (times[f],times[f]), value = height)
                elif(keys[f] < 0):
                    commands.setKeyframe(self.hipName.GetText(), attribute = "translate" + self.worldUpAxis.GetValue(), time = (times[f],times[f]), value = 0)       
            commands.cutKey(self.hipName.GetText(), attribute = "translate" + self.worldForwardAxis.GetValue(), time = ())
        else:
            Commands.Warning("Please provide a hip|root name in Settings tab")
            
    def AddRootJoint(self, *args):
        if(self.hipName.GetText() and self.rootName.GetText()):
            Commands.SetTime(0)
            joint = Commands.CreateJoint([0.0,0.0,0.0])
            Commands.Rename(joint, self.rootName.GetText())
            Commands.Deselect(self.rootName.GetText())
            Commands.Deselect(self.hipName.GetText())
            if(self.hipName.GetText() != self.rootName.GetText()):
                Commands.ParentObjects(self.hipName.GetText(), self.rootName.GetText())
                return
        else:
            Commands.Warning("Provide the name of the hip|root joint in Settings tab")
            return
        return

    def GetAndSetHipHeight(self, *args):
        if(self.hipName.GetText()):
            height = Commands.GetTranslation(self.hipName.GetText())[0][1]
            self.ffHeight.SetValue([height , 0.0, 0.0, 0.0])
        else:
            Commands.Warning("Provide the name of the hip joint in Settings tab")

    def CutAndPasteKeys(self, *args):
        if(self.rootName.GetText()):
            Commands.DeselectAll()
            self.AddRootJoint()
            attributes = ['translateX','translateY','translateZ']
            currentOption = self.omClamp.GetValue()
            Commands.SetTime(0)
            position = Commands.GetTranslation(self.hipName.GetText())
            for i in range(len(attributes)):
                    times = Commands.GetAnimatedTimes(self.hipName.GetText(), attributes[i]) or []       
                    keys = commands.keyframe(self.hipName.GetText() + "_" + attributes[i], q= True, vc = True) or []
                    if(attributes[i] == "translateY"):
                        if(self.bCutAllKeys  == False):
                            if(currentOption == "Constrain To Ground"):
                                for f in range(len(keys)):
                                    if(keys[f] > position[0][1]):
                                        commands.setKeyframe(self.rootName.GetText(), attribute = "translateY", time = (0,0), value = 0)                    
                                        commands.cutKey(self.hipName.GetText(), attribute = "translateY", index= (f, (f)))
                                        commands.setKeyframe(self.hipName.GetText(), attribute = "translateY", time = (times[f],times[f]), value = position[0][1])
                                        commands.pasteKey(self.rootName.GetText(), attribute = "translateY", time = (times[f],times[f]), valueOffset = -position[0][1])
                                    elif(keys[f] < position[0][1]):
                                        commands.setKeyframe(self.rootName.GetText(),attribute = "translateY", time = (times[f],times[f]), value = 0)
                            elif(currentOption == "UnConstrain To Ground"):
                                commands.cutKey(self.hipName.GetText(), attribute = "translateY", time = ())
                                commands.pasteKey(self.rootName.GetText(), attribute = "translateY",time = (0,0), valueOffset = -position[0][1])
                        else:
                            commands.cutKey(self.hipName.GetText(), attribute = attributes[i],time = ())
                            commands.pasteKey(self.rootName.GetText(), attribute = attributes[i],time = (0,0), valueOffset = -position[0][1])
                    else:
                        commands.cutKey(self.hipName.GetText(), attribute = attributes[i], time = ())
                        commands.pasteKey(self.rootName.GetText(), attribute = attributes[i], time = (0,0), valueOffset = -position[0][2])
        else:
            Commands.Warning("No root joint name povided in Settings tab")

    def SaveConfig(self, *args):
        if(config.has_section("Settings") == False):
            config.add_section("Settings")
        config.set("Settings", "ExportDir", self.directory)
        config.set("Settings", "RootJoint", self.rootName.GetText())
        config.set("Settings", "HipJoint", self.hipName.GetText())
        config.set("Settings", "HipHeight", self.ffHeight.GetValue1())
        config.set("Settings", "ClampRoot", self.omClamp.GetValue())
        config.set("Settings", "WorldUp", self.worldUpAxis.GetValue())
        config.set("Settings", "WorldForward", self.worldForwardAxis.GetValue())
        state = self.bRootJoint.GetValue()
        config.set("Settings", "AddRoot", "true" if state == True else "false" )
        file = open(configDir, "wb")
        with file as configFile:
            config.write(configFile)
        file.close()

    def LoadConfig(self, *args):
        file = open(configDir, "r")
        if(file):
            config.read(configDir)
            self.directory = config.get("Settings", "ExportDir")
            self.textDirectory.SetText(self.directory)
            self.rootName.SetText(config.get("Settings", "RootJoint"))
            self.hipName.SetText(config.get("Settings", "HipJoint"))
            self.omClamp.SetValue(config.get("Settings", "ClampRoot"))
            self.worldUpAxis.SetValue(config.get("Settings", "WorldUp"))
            self.worldForwardAxis.SetValue(config.get("Settings", "WorldForward"))
            self.ffHeight.SetValue1(config.getfloat("Settings", "hipheight"))
            self.bRootJoint.SetValue(config.getboolean("Settings", "AddRoot"))
            file.close()

    def ResetConfig(self, *args):
        self.directory = ""
        self.textDirectory.SetText(self.directory)
        self.rootName.SetText("")
        self.hipName.SetText("")
        self.omClamp.SetValue("UnConstrain 0")
        self.worldUpAxis.SetValue("Y")
        self.worldForwardAxis.SetValue("Z")
        self.ffHeight.SetValue1(0.0)
        self.bRootJoint.SetValue(False)

