import FreeCADGui
import FreeCAD
from random import *
from FreeCAD_PySide import *

import TibraParameters
import RunTibra
import StlExportManager
import __main__

class Random_Box():
    """My new command"""

    def GetResources(self):
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/test2-icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'Accel' : "Shift+J", # a default shortcut (optional)
                'MenuText': "Create Random Box",
                'ToolTip' : "Create Random Box"}

    def Activated(self):
        if FreeCAD.ActiveDocument == None:
            doc = FreeCAD.newDocument()
        else:
            doc = FreeCAD.ActiveDocument
        box = doc.addObject("Part::Box", "myBox")
        box.Height = random()*10
        box.Width = random()*10
        box.Length = random()*10
        print("Box created!!")
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    
class STLExporter():
    """My new command"""

    def GetResources(self):
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/export_STL.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Export STL",
                'ToolTip' : "Export the STL file (Without Running TIBRA)"}

    def Activated(self):
        
        form = StlExportManager.StlExportManager()
        form.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True
        
        
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



FreeCADGui.addCommand('Create Random Box',Random_Box())
FreeCADGui.addCommand('Export STL',STLExporter())
FreeCADGui.addCommand('Set Tibra Parameters',SetTibraParameters())
FreeCADGui.addCommand('Run Tibra',RunTibra_Class())
