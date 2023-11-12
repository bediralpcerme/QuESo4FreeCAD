from FreeCAD_PySide import *
import FreeCADGui as Gui

#__dirname__ = C:\Users\DanielP\AppData\Roaming\FreeCAD\Mod\ExampleWorkbench



class TIBRA4FreeCAD (Workbench):

    MenuText = "TIBRA4FreeCAD"
    ToolTip = "TIBRA4FreeCAD Workbench"
    Icon = """
			/* XPM */
			static const char *test_icon[]={
			"16 16 2 1",
			"a c #0065bd",
			". c None",
			"................",
			"................",
			"..############..",
			"..############..",
			"..############..",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"................",
			"................"};
			"""
	
	
	
	
	
	#os.path.join(__dirname__, 'icon', 'ExampleLogo.svg')
	
	

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import MyCommands#, MyModuleB # import here all the needed files that create your FreeCAD commands
        self.list = ["Set QuESo Parameters", 'Run QuESo' , 'Visualize Result' ] # A list of command names created in the line above
        self.appendToolbar("My Commands",self.list) # creates a new toolbar with your commands
        self.appendMenu("Example Menu",self.list) # creates a new menu
        self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed when the workbench is activated"""
		#Gui.SendMsgToActiveView("ViewFit")

        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(TIBRA4FreeCAD())