import FreeCADGui
import FreeCAD
from random import *
from FreeCAD_PySide import *
import os

import QuESoParameters
import RunQuESo
import PostProcess

import __main__
    
class SetQuESoParameters():
    """My new command"""

    def GetResources(self):
        icon_path = os.path.dirname(__file__)+'/icon/set_parameter.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "QuESo Parameters",
                'ToolTip' : "Set QuESo Parameters"}

    def Activated(self):
        __main__.form = QuESoParameters.QuESoParameters()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


class RunQuESo_Class():
  

    def GetResources(self):
        icon_path = os.path.dirname(__file__) + '/icon/run_icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Run QuESo",
                'ToolTip' : "Run QuESo"}

    def Activated(self):
        QuESo = RunQuESo.RunQuESo()
        QuESo.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

class RunPostProcess():
    """My new command"""
    def GetResources(self):
        icon_path = os.path.dirname(__file__) + '/icon/fem_postprocess.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Post Process",
                'ToolTip' : "Post Process"}

    def Activated(self):
        __main__.form = PostProcess.PostProcess()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


FreeCADGui.addCommand('Set QuESo Parameters',SetQuESoParameters())
FreeCADGui.addCommand('Run QuESo',RunQuESo_Class())
FreeCADGui.addCommand('Visualize Result',RunPostProcess())
