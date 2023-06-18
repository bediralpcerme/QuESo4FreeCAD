import FreeCADGui
import FreeCAD
from random import *
from FreeCAD_PySide import *

import TibraParameters
import RunTibra
import StlExportManager

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
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/test-icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Export STL",
                'ToolTip' : "Export the STL file"}

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
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/test-icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Tibra Parameters",
                'ToolTip' : "Setting Path"}

    def Activated(self):
        
        form = TibraParameters.TibraParameters()
        form.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


class RunTibra_Class():
  

    def GetResources(self):
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/test-icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'MenuText': "Run Tibra",
                'ToolTip' : "Run Tibra"}

    def Activated(self):
        
        form = RunTibra.RunTibra()
        form.exec_()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True



FreeCADGui.addCommand('Create Random Box',Random_Box())
FreeCADGui.addCommand('Export STL',STLExporter())
FreeCADGui.addCommand('Set Tibra Parameters',SetTibraParameters())
FreeCADGui.addCommand('Run Tibra',RunTibra_Class())
