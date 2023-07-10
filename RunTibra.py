from FreeCAD_PySide import *
import os
import subprocess
import FreeCAD

import sys
import os


class RunTibra(QtGui.QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #position and geometry of the dialog box
        width = 300
        height = 160
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Run Tibra?")

        #label text
        self.label_ = QtGui.QLabel("Run Tibra?", self)
        self.label_.move(100, 20)

        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.move(10, 90)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)
        okButton.move(170, 90)

    def onOk(self):
       
        #By subprocess
        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")
        self.work_dir = self.work_dir + '/TIBRA/data'

        os.chdir(self.work_dir)

        #TIBRA is run with parameters and B.C.s
        from TIBRA_PythonApplication.PyTIBRA import PyTIBRA
        pytibra = PyTIBRA("TIBRAParameters.json")
        pytibra.Run()
        # Direct Analysis with kratos
        if( os.path.exists(self.work_dir+'\StructuralMaterials.json') and os.path.exists(self.work_dir+'\KratosParameters.json')):
            pytibra.RunKratosAnalysis()
            pytibra.PostProcess()


        self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()

    
