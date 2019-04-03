import maya as maya
import maya.cmds as commands
from functools import partial
import ConfigParser
import os
import Functions.UI as UI
import Functions.Statics as Statics 

config = ConfigParser.RawConfigParser()
configDir = os.path.dirname(__file__) + "\config.cfg";

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
        window                                          = UI.Window("Maximo To Unreal", (500, 400), True, True, False)
        window.MenuBar(True)
        menu = UI.Menu("File", True)
        menu.AddItem("Save Settings", self.SaveConfig)
        menu.AddItem("Reset Settings", self.ResetConfig)

        '''tab'''
        tabs                                            = UI.Tab(500.0, 500.0, (50.0,50.0))
        '''columns'''
        column1                                         = UI.Column("column1")
        column1.SetAdjustable(True)
        column1.SetRowSpacing(10)
        column1.SetWidth(500.0)
        column1.SetBackgroundColorOne(.3)
        
        self.textDirectory = UI.TextButton("Animation Export Directory", "Browse")
        self.textDirectory.SetCommand(self.SetDirectory)
        
        self.worldUpAxis                                = UI.OptionMenu("World Up         ",["Y","Z"], 200)
        self.worldForwardAxis                           = UI.OptionMenu("World Forward",["Z","X"], 200)
        self.worldUpAxis.SetAnnotation("The current up world axis of the scene used for conversion")
        self.worldForwardAxis.SetAnnotation("The current forward world axis of the scene used for conversion")
        
        self.rootName                                   = UI.TextField("Root Joint Name" , 200)
        self.hipName                                    = UI.TextField("Hip Joint Name" , 200)
        self.rootName.SetAnnotation("The name to give the root joint")
        self.hipName.SetAnnotation("The name of the existing hip joint")
        
        bttnParent = UI.Button("Parent", 200)
        bttnParent.SetCommand('Statics.Commands.ParentSelected()')
        bttnParent.SetAnnotation("Parent selected objects")
        
        bttnRootJoint = UI.Button("Add Root Joint", 200)
        bttnRootJoint.SetCommand(self.AddRootJoint)
        
        UI.Button("Undo <-", 200.0).SetCommand("Statics.Commands.undo()")
        UI.Button("Redo ->", 200.0).SetCommand("Statics.Commands.redo()")
        
        column1.SetParent( tabs.GetUI() )
        
        '''column2'''
        column2                 = UI.Column("column2")
        column2.SetAdjustable(True)
        column2.SetRowSpacing(10)
        column2.SetWidth(500.0)
        column2.SetBackgroundColorOne(.3)
        
        self.bRootJoint                                     = UI.CheckBox("Add Root Joint", False)
        self.bRootJoint.SetAnnotation("Add a root joint to the converted animation")
        
        bttnConvert                                         = UI.Button("Convert Animation To In Place", 200)
        bttnConvert.SetCommand(self.ConvertAnimationToInPlace)
        UI.Button("Export Animation", 200).SetCommand(self.ShowExportWindow)
        
        UI.Button("Undo <-", 200.0).SetCommand("Statics.Commands.undo()")
        UI.Button("Redo ->", 200.0).SetCommand("Statics.Commands.redo()")
        
        column2.SetParent( tabs.GetUI() )
        
        #column2 controls
        column3                                             = UI.Column("column3")
        column3.SetAdjustable(True)
        column3.SetRowSpacing(10)
        column3.SetWidth(500.0)
        column3.SetBackgroundColorOne(.3)
        
        '''Hip joint height'''
        self.ffHeight                                       = UI.FloatFieldGrp("Hip Height", 1, 200)
        self.ffHeight.SetAdjustable(1)
        self.ffHeight.SetAlignment(1, "left")
        
        self.btnHeight                                      = UI.Button("Set Hip Height", 200)
        self.btnHeight.SetCommand(self.GetAndSetHipHeight)
        self.btnHeight.SetAnnotation("Set the Hip Height from the hip joint name specified in settings")
        
        '''Add root motion button'''
        self.omClamp                                        = UI.OptionMenu("Clamp Root",["UnConstrain 0","Constrain 0"], 200)
        self.omClamp.SetAnnotation("Constrain the animation to 0 on the world up axis")
        
        self.btnCutPaste                                    = UI.Button("Add Root Motion", 200)
        self.btnCutPaste.SetCommand(self.CutAndPasteKeys)
        
        UI.Button("Export Animation", 200).SetCommand(self.ShowExportWindow)
        
        UI.Button("Undo <-", 200.0).SetCommand("Statics.Commands.undo()")
        UI.Button("Redo ->", 200.0).SetCommand("Statics.Commands.redo()")
        
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
        self.exportWindow = UI.Window("Export", (500, 100), False, False)
        
        column = UI.Column("Export column")
        column.SetAdjustable(True)
        column.SetRowSpacing(10)
        column.SetWidth(200.0)
        
        self.textField2 = UI.TextField("Animation Name", 300)
        
        button = UI.Button("Export", 50)
        button.SetCommand(self.ExportAnimation)
        self.exportWindow.Show()
        
    def ExportAnimation(self, *args):
        if(self.rootName.GetText()):
            Statics.Commands.Select(self.rootName.GetText())
            commands.file(self.directory + "/" + self.textField2.GetText(), es = True, options = "v=0" , force = True, typ = "FBX export", pr = True )
            self.exportWindow.Remove()
        else:
            Statics.Commands.Warning("Root joint not provided in Settings")
        
    def ConvertAnimationToInPlace(self, *args):
        Statics.Commands.DeselectAll()
        if(self.bRootJoint.GetValue()):
            self.AddRootJoint()
        if(self.hipName.GetText() and self.rootName.GetText()):
            Statics.Commands.Select(self.hipName.GetText())
            Statics.Commands.SetTime(0)
            height = Statics.Commands.GetTranslation(self.hipName.GetText())[0][1]
            times = Statics.Commands.GetAnimatedTimes(self.hipName.GetText(), "translate" + self.worldUpAxis.GetValue())           
            keys = commands.keyframe(self.hipName.GetText() + "_" + "translate" + self.worldUpAxis.GetValue(), q= True, vc = True) or []
            for f in range(len(keys)):
                if(keys[f] > height):                  
                    commands.cutKey(self.hipName.GetText(), attribute = "translate" + self.worldUpAxis.GetValue(), index= (f, (f)))
                    commands.setKeyframe(self.hipName.GetText(),attribute = "translate" + self.worldUpAxis.GetValue(), time = (times[f],times[f]), value = height)
                elif(keys[f] < 0):
                    commands.setKeyframe(self.hipName.GetText(), attribute = "translate" + self.worldUpAxis.GetValue(), time = (times[f],times[f]), value = 0)       
            commands.cutKey(self.hipName.GetText(), attribute = "translate" + self.worldForwardAxis.GetValue(), time = ())
        else:
            Statics.Commands.Warning("Please provide a hip|root name in Settings tab")
            
    def AddRootJoint(self, *args):
        if(self.hipName.GetText() and self.rootName.GetText()):
            Statics.Commands.SetTime(0)
            joint = Statics.Commands.CreateJoint([0.0,0.0,0.0])
            Statics.Commands.Rename(joint, self.rootName.GetText())
            Statics.Commands.Deselect(self.rootName.GetText())
            Statics.Commands.Deselect(self.hipName.GetText())
            if(self.hipName.GetText() != self.rootName.GetText()):
                Statics.Commands.ParentObjects(self.hipName.GetText(), self.rootName.GetText())
                return
        else:
            Statics.Commands.Warning("Provide the name of the hip|root joint in Settings tab")
            return
        return

    def GetAndSetHipHeight(self, *args):
        if(self.hipName.GetText()):
            height = Statics.Commands.GetTranslation(self.hipName.GetText())[0][1]
            self.ffHeight.SetValue([height , 0.0, 0.0, 0.0])
        else:
            Statics.Commands.Warning("Provide the name of the hip joint in Settings tab")

    def CutAndPasteKeys(self, *args):
        if(self.rootName.GetText()):
            Statics.Commands.DeselectAll()
            self.AddRootJoint()
            attributes = ['translateX','translateY','translateZ']
            currentOption = self.omClamp.GetValue()
            Statics.Commands.SetTime(0)
            position = Statics.Commands.GetTranslation(self.hipName.GetText())
            for i in range(len(attributes)):
                    times = Statics.Commands.GetAnimatedTimes(self.hipName.GetText(), attributes[i]) or []       
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
            Statics.Commands.Warning("No root joint name povided in Settings tab")

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

