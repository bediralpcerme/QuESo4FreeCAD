from FreeCAD_PySide import *
import os
import FreeCAD
import Mesh

class SurfaceSTL(QtGui.QDialog):
    """"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
    

    def onBrowseButton(self):



    def onCancel(self):
        self.result = "Cancel"
        self.close()