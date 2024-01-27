##########################################################################################
##                                                                                      ##
##              Defining the commands that will be added to the workbench               ##
##                                                                                      ##
##########################################################################################

import FreeCADGui
import FreeCAD
from random import *
from FreeCAD_PySide import *
import os

# We import the *.py files necessary because we will create an instance from those objects

import QuESoParameters
import RunQuESo
import PostProcess
import __main__

# To create a command, we define a class, and execute/show it in the 'Activated' method \n
# in that class. In the 'GetResources' method, the 'ToolTip' key is the one whose value \n
# appear on the workbench when we hover on it.

class SetQuESoParameters():

    def GetResources(self):
        icon_path = os.path.dirname(__file__)+'/icon/set_parameter.svg'
        return {'Pixmap'  :  str(icon_path),
                'MenuText': "QuESo and Kratos Parameters",
                'ToolTip' : "Set QuESo and Kratos Parameters"}

    def Activated(self):

        # Observe that we do not execute the QuESoParameters class, because we want \n
        # hide or minimize it if necessary when we run the plug-in. Otherwise, we would \n
        # execute it - refer to RunQuESo_Class below.
        __main__.form = QuESoParameters.QuESoParameters()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    

class RunQuESo_Class():
  
    def GetResources(self):
        icon_path = os.path.dirname(__file__) + '/icon/run_icon.svg'
        return {'Pixmap'  :  str(icon_path),
                'MenuText': "Run QuESo and Kratos",
                'ToolTip' : "Run QuESo and Kratos"}

    def Activated(self):
        QuESo = RunQuESo.RunQuESo()
        QuESo.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


class RunPostProcess():

    def GetResources(self):
        icon_path = os.path.dirname(__file__) + '/icon/fem_postprocess.svg'
        return {'Pixmap'  :  str(icon_path),
                'MenuText': "Post Process",
                'ToolTip' : "Post Process"}

    def Activated(self):
        __main__.form = PostProcess.PostProcess()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    
# When using addCommand, the first one (string) is the name of the command, which we \n
# will use to insert them on the toolbar of the workbench. The second one (class \n
# instance) is the one that will appear when the command is clicked/run.

FreeCADGui.addCommand('Set QuESo Parameters',SetQuESoParameters())
FreeCADGui.addCommand('Run QuESo',RunQuESo_Class())
FreeCADGui.addCommand('Visualize Results',RunPostProcess())

## ######################################################################################