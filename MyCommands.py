import FreeCADGui
import FreeCAD
from random import *
from FreeCAD_PySide import *
import StlExportManager
import Mesh
import sys

class Function1_Class():
    """My new command"""

    def GetResources(self):
        icon_path = FreeCAD.getUserAppDataDir()+'/Mod/TIBRA4FreeCAD/icon/test-icon.svg'
        return {'Pixmap'  :  str(icon_path), # the name of a svg file available in the resources
                'Accel' : "Shift+M", # a default shortcut (optional)
                'MenuText': "My New Command 1",
                'ToolTip' : "What my new command 1 does"}

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        box = doc.addObject("Part::Box", "myBox")
        box.Height = random()*100
        box.Width = random()*100
        box.Length = random()*100
        print("Big box created!!")
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True

class Function2_Class():
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
    
class Function3_Class():
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
        
class Function4_Class():
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



FreeCADGui.addCommand('Create Random Box',Function2_Class())
FreeCADGui.addCommand('Export STL',Function3_Class())
FreeCADGui.addCommand('Set Tibra Parameters',Function4_Class())
FreeCADGui.addCommand('Run Tibra',RunTibra_Class())
