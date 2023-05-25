from FreeCAD_PySide import *
import sys
import os
import FreeCAD
import Mesh

class StlExportManager(QtGui.QDialog):
    """"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #position and geometry of the dialog box
        width = 230
        height = 125
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("STL Export Manager")

        #label text
        self.label_ = QtGui.QLabel("Please enter the file name:", self)
        self.label_.move(10, 20)
        self.textInput_ = QtGui.QLineEdit(self)
        self.textInput_.setText("Appear Trial")
        self.textInput_.setFixedWidth(200)
        self.textInput_.move(10, 50)

        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.move(30, 90)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)
        okButton.move(120, 90)

    def onOk(self):
        object = []
        docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        save_dir = FreeCAD.ActiveDocument.FileName
        save_dir = save_dir.replace(docName,"")
        object.append(FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.myBox.Name))
        Mesh.export(object,save_dir + self.textExtractor() + ".stl")
        infoBox = QtGui.QMessageBox.information(self, "STL Export Manager", "The STL file has been successfully exported to " \
                                                 + "'" + save_dir + "'" + " directory.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()
    
    def textExtractor(self):
         self.myStr = self.textInput_.text()
         return self.myStr
