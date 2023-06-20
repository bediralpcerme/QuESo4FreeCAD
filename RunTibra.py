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
        #Idk how to automatize this but python in freecad doesnt see the path in the system so you add it again
        sys.path.append("D:\COMPUTATIONAL MECHANICS\SOFTWARE_LAB\TIBRA")
        from TIBRA_PythonApplication.PyTIBRA import PyTIBRA
        pytibra = PyTIBRA("TIBRAParameters.json")
        pytibra.Run()

        '''
        from TIBRA_PythonApplication.PyTIBRA import PyTIBRA
        exec(open('TIBRA_main.py').read())

        # By cmd
        
        
        os.system('cd C:\\Users\DanielP\Desktop\Example\TIBRA')
        
        setPath1 = 'set PYTHONPATH=%PYTHONPATH%;C:\KRATOS\Kratos\bin\Release'

        setPath2 = 'set PYTHONPATH=%PYTHONPATH%;C:\TIBRA\TIBRA-windows_installation'

        runTibra = 'python -m TIBRA_main'

        os.system(setPath1)

        os.system(setPath2)

        os.system(runTibra)
        '''
        self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()

    
