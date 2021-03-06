import icons_rc
class Survey (Workbench):
 
    MenuText = "Survey"
    ToolTip = "Working with point, terrains and alignments"
    Icon = ":icons/Survey.svg"
 
    def Initialize(self):
        "This function is executed when FreeCAD starts"
        from SurveyTools import Punt, Importa, Triangula, Tools, newProject, Codes
        import icons_rc # import here all the needed files that create your FreeCAD commands
        self.list = ["New project","Crear punt","Importa", "Triangula", "Codis"] # A list of command names created in the line above
        self.appendToolbar("Survey",self.list) # creates a new toolbar with your commands
        self.appendMenu("Survey",self.list) # creates a new menu
        #self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu
 
    def Activated(self):
        "This function is executed when the workbench is activated"
        try:
            
            grp = FreeCAD.activeDocument().Punts
            
        except:
            import newProject as np
            np.creaProjecte()
            grp = FreeCAD.activeDocument().Punts
            
        return
 
    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return
 
    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("Survey",self.list) # add commands to the context menu
 
    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
 
Gui.addWorkbench(Survey())
