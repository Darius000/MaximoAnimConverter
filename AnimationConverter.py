import maya.cmds as commands
from functools import partial

class Converter:
    def __init__(self):
        pass
        
        
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
        window                                          = MayaUI.Window("Maximo To Unreal", (500, 400), True, False)
        
        '''tab'''
        tabs                                            = MayaUI.Tab(500.0, 500.0, (50.0,50.0))
        '''columns'''
        column1                                         = MayaUI.Column("column1")
        column1.SetAdjustable(True)
        column1.SetRowSpacing(10)
        column1.SetWidth(500.0)
        column1.SetBackgroundColorOne(.3)
        
        self.textDirectory = MayaUI.TextButton("Animation Export Directory", "Browse")
        self.textDirectory.SetCommand(self.SetDirectory)
        
        self.worldUpAxis                                = MayaUI.OptionMenu("World Up         ",["Y","Z"], 200)
        self.worldForwardAxis                           = MayaUI.OptionMenu("World Forward",["Z","X"], 200)
        
        self.rootName                                   = MayaUI.TextField("Root Joint Name" , 200)
        self.hipName                                    = MayaUI.TextField("Hip Joint Name" , 200)
        
        bttnParent = MayaUI.Button("Parent", 200)
        bttnParent.SetCommand('Commands.ParentSelected()')
        
        MayaUI.Button("Undo <-", 200.0).SetCommand("commands.undo()")
        MayaUI.Button("Redo ->", 200.0).SetCommand("commands.redo()")
        
        column1.SetParent( tabs.GetUI() )
        
        '''column2'''
        column2                 = Column("column2")
        column2.SetAdjustable(True)
        column2.SetRowSpacing(10)
        column2.SetWidth(500.0)
        column2.SetBackgroundColorOne(.3)
        
        self.bRootJoint                                     = MayaUI.CheckBox("Add Root Joint", False)
        
        bttnConvert                                         = MayaUI.Button("Convert Animation To In Place", 200)
        bttnConvert.SetCommand(self.ConvertAnimationToInPlace)
        MayaUI.Button("Export Animation", 200).SetCommand(self.ShowExportWindow)
        
        MayaUI.Button("Undo <-", 200.0).SetCommand("commands.undo()")
        MayaUI.Button("Redo ->", 200.0).SetCommand("commands.redo()")
        
        column2.SetParent( tabs.GetUI() )
        
        #column2 controls
        column3                                             = MayaUI.Column("column3")
        column3.SetAdjustable(True)
        column3.SetRowSpacing(10)
        column3.SetWidth(500.0)
        column3.SetBackgroundColorOne(.3)
        
        '''Hip joint height'''
        self.ffHeight                                       = MayaUI.FloatFieldGrp("Hip Height", 1, 200)
        self.ffHeight.SetAdjustable(1)
        self.ffHeight.SetAlignment(1, "left")
        
        self.btnHeight                                      = MayaUI.Button("Set Hip Height", 200)
        self.btnHeight.SetCommand(self.GetAndSetHipHeight)
        
        '''Add root motion button'''
        self.omClamp                                        = MayaUI.OptionMenu("Clamp Root",["UnConstrain 0","Constrain 0"], 200)
        self.btnCutPaste                                    = MayaUI.Button("Add Root Motion", 200)
        self.btnCutPaste.SetCommand(self.CutAndPasteKeys)
        
        MayaUI.Button("Export Animation", 200).SetCommand(self.ShowExportWindow)
        
        MayaUI.Button("Undo <-", 200.0).SetCommand("commands.undo()")
        MayaUI.Button("Redo ->", 200.0).SetCommand("commands.redo()")
        
        column3.SetParent( tabs.GetUI() )
        
       
        #add colums to tab
        tabs.SetTabLabel(((column1.GetUI(), "Settings"), (column2.GetUI(), "Movement to InPlace"), (column3.GetUI(), "Root Motion")))

        window.Show()
        
    def SetDirectory(self, *args):
        self.directory = commands.fileDialog2(fileMode = 2,dialogStyle = 2, fileFilter = 'FBX export')[0]
        self.textDirectory.SetText(self.directory)
    
    def ShowExportWindow(self, *args):
        self.exportWindow = MayaUI.Window("Export", (500, 100), False, False)
        
        column = MayaUI.Column("Export column")
        column.SetAdjustable(True)
        column.SetRowSpacing(10)
        column.SetWidth(200.0)
        
        self.textField2 = MayaUI.TextField("Animation Name", 300)
        
        button = MayaUI.Button("Export", 50)
        button.SetCommand(self.ExportAnimation)
        self.exportWindow.Show()
        
    def ExportAnimation(self, *args):
        if(self.rootName.GetText()):
            MayaUI.Commands.Select(self.rootName.GetText())
            commands.file(self.directory + "/" + self.textField2.GetText(), es = True, options = "v=0" , force = True, typ = "FBX export", pr = True )
            self.exportWindow.Remove()
        else:
            MayaUI.Commands.Warning("Root joint not provided in Settings")
        
    def ConvertAnimationToInPlace(self, *args):
        MayaUI.Commands.DeselectAll()
        if(self.bRootJoint.GetValue()):
            self.AddRootJoint()
        if(self.hipName.GetText() and self.rootName.GetText()):
            MayaUI.Commands.Select(self.hipName.GetText())
            MayaUI.Commands.SetTime(0)
            height = MayaUI.Commands.GetTranslation(self.hipName.GetText())[0][1]
            times = MayaUI.Commands.GetAnimatedTimes(self.hipName.GetText(), "translate" + self.worldUpAxis.GetValue())           
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
            MayaUI.Commands.SetTime(0)
            joint = MayaUI.Commands.CreateJoint([0.0,0.0,0.0])
            MayaUI.Commands.Rename(joint, self.rootName.GetText())
            MayaUI.Commands.Deselect(self.rootName.GetText())
            MayaUI.Commands.Deselect(self.hipName.GetText())
            if(self.hipName.GetText() != self.rootName.GetText()):
                MayaUI.Commands.ParentObjects(self.hipName.GetText(), self.rootName.GetText())
                return
        else:
            MayaUI.Commands.Warning("Provide the name of the hip|root joint in Settings tab")
            return
        return
        
    def GetAndSetHipHeight(self, *args):
        if(self.hipName.GetText()):
            height = MayaUI.Commands.GetTranslation(self.hipName.GetText())[0][1]
            self.ffHeight.SetValue([height , 0.0, 0.0, 0.0])
        else:
            MayaUI.Commands.Warning("Provide the name of the hip joint in Settings tab")


    def CutAndPasteKeys(self, *args):
        if(self.rootName.GetText()):
            MayaUI.Commands.DeselectAll()
            self.AddRootJoint()
            attributes = ['translateX','translateY','translateZ']
            currentOption = self.omClamp.GetValue()
            MayaUI.Commands.SetTime(0)
            position = MayaUI.Commands.GetTranslation(self.hipName.GetText())
            for i in range(len(attributes)):
                    times = MayaUI.Commands.GetAnimatedTimes(self.hipName.GetText(), attributes[i]) or []       
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
            MayaUI.Commands.Warning("No root joint name povided in Settings tab")
        
#Create UI
converter = Converter()
converter.Construct()


    