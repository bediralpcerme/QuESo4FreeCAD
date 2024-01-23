from FreeCAD_PySide import *
import FreeCADGui as Gui

##########################################################################################
##                                                                                      ##
##                                CREATING THE WORKBENCH                                ##
##                                                                                      ##
##########################################################################################


class QuESo4FreeCAD (Workbench):

##**************************************************************************************##
##                     Defining the name and icon of the workbench                      ##
##**************************************************************************************##

    MenuText = "QuESo4FreeCAD"
    ToolTip = "QuESo4FreeCAD Workbench"
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

##  **************************************************************************************

##**************************************************************************************##
##   Adding the commands created in 'MyCommands.py' into the toolbar of the workbench   ##
##**************************************************************************************##

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import MyCommands# import here all the needed files that create your FreeCAD commands
        self.list = ['Set QuESo Parameters', 'Run QuESo', 'Visualize Results'] # A list of command names created in MyCommands.py
        self.appendToolbar("My Commands", self.list) # creates a new toolbar with your commands

##  **************************************************************************************

    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        return

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(QuESo4FreeCAD())

## ######################################################################################