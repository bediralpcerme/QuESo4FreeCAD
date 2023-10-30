import FreeCADGui
import FreeCAD
from random import *
from FreeCAD_PySide import *

import TibraParameters
import RunTibra
import StlExportManager
import __main__
    
class SetTibraParameters():
    """My new command"""

    def GetResources(self):
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/set_parameter.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Tibra Parameters",
                'ToolTip' : "Set TIBRA Parameters"}

    def Activated(self):
        __main__.form = TibraParameters.TibraParameters()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


class RunTibra_Class():
  

    def GetResources(self):
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/run_icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Run Tibra",
                'ToolTip' : "Run Tibra"}

    def Activated(self):
        tibra = RunTibra.RunTibra()
        tibra.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


FreeCADGui.addCommand('Set Tibra Parameters',SetTibraParameters())
FreeCADGui.addCommand('Run Tibra',RunTibra_Class())
