from FreeCAD_PySide import *
import os
import subprocess
import FreeCAD
import sys
import numpy as np
import re
import FreeCADGui
import FemGui
import femresult.resulttools as resulttools
import Fem
import FreeCADGui as Gui
import Draft, Sketcher, Mesh, Part
from pivy import coin
from femobjects import result_mechanical
from PySide2 import QtWidgets


class PostProcess(QtGui.QDialog):

    def __init__(self):
        super(PostProcess, self).__init__()
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)
        self.setMaximumHeight(220)
        self.setMinimumHeight(220)
        self.visulizerun=False
        self.initUI()

    def initUI(self):
        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")

        #position and geometry of the dialog box
        width = 300
        height = 220

        self.centerPoint = QtGui.QDesktopWidget().availableGeometry().center()

        std_validate = QtGui.QIntValidator()
        scientific_validate = QtGui.QDoubleValidator()
        scientific_validate.setNotation(QtGui.QDoubleValidator.ScientificNotation)

        self.setGeometry(self.centerPoint.x()-0.5*width, self.centerPoint.y()-0.5*height, height, width)
        self.setWindowTitle("Post Process")

        layout = QtGui.QVBoxLayout()

        self.min_val, self.max_val = self.get_min_max_values()

        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, on = True)

        #Initial Parameters input:

        #path to the file
        self.label_pathname_ = QtGui.QLabel("Path to the result file:", self)

        #Text edit of pathname
        self.textInput_pathname_ = QtGui.QLineEdit(self)
        self.textInput_pathname_.setText("")
        self.textInput_pathname_.setFixedWidth(140)

        #file browser button
        self.fileBrowseButton = QtGui.QPushButton('Browse files',self)
        self.fileBrowseButton.clicked.connect(self.onBrowseButton)
        self.fileBrowseButton.setFixedWidth(80)
        self.fileBrowseButton.setAutoDefault(False)

        #method setting
        self.label_result_ = QtGui.QLabel("Results:", self)
        self.popup_result = QtGui.QComboBox(self)
        self.popup_result_items = ("Displacement X","Displacement Y","Displacement Z","Total Displacement","Cauchy Stress Vector XX", "Cauchy Stress Vector YY","Cauchy Stress Vector ZZ","Cauchy Stress Vector XY","Cauchy Stress Vector XZ","Cauchy Stress Vector YZ","Von Misses Stress")
        self.popup_result.addItems(self.popup_result_items)
        self.popup_result.currentTextChanged.connect(self.onVisualize__)
        self.popup_result.setFixedWidth(140)
        
        # visulize button
        self.visualizeButton = QtGui.QCheckBox('Visualize the output', self)
        self.visualizeButton.stateChanged.connect(self.onVisualize)
        self.visualizeButton.move(10, self.label_result_.y()+45)

        #push button
        self.run_button = QtGui.QPushButton("Run Task",self)
        self.run_button.clicked.connect(self.run_task)
        #self.run_button.move(10, self.visualizeButton.y()+45)

        
        self.colorGradient=GradientBar(self.min_val, self.max_val)

        layout1 = QtGui.QVBoxLayout()
        layout2 = QtGui.QVBoxLayout()
        layout3 = QtGui.QVBoxLayout()
        layout1.addWidget(self.label_pathname_)
        layout1.addWidget(self.textInput_pathname_)
        layout1.addWidget(self.fileBrowseButton)
        layout1.addWidget(self.label_result_)
        layout1.addWidget(self.popup_result)
        layout1.addWidget(self.visualizeButton)
        layout1.addWidget(self.run_button)


        layout2.addWidget(self.colorGradient)

        layout3.addLayout( layout1 )
        layout3.addLayout( layout2 )
        self.setLayout(layout3)
        self.show()

    def Visualize(self):
        self.visulizerun=True

        #mesh is colored by the scalars
        if (self.popup_result.currentText()=="Total Displacement"):
            self.mesh_obj.Visibility= True
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.DisplacementLengths)
        elif (self.popup_result.currentText()=="Displacement X"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, list(self.displacement[:,0]))
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Displacement Y"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, list(self.displacement[:,1]))
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Displacement Z"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, list(self.displacement[:,2]))
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Cauchy Stress Vector XX"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.NodeStressXX)
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Cauchy Stress Vector YY"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.NodeStressYY)
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Cauchy Stress Vector ZZ"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.NodeStressZZ)
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Cauchy Stress Vector XY"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.NodeStressXY)
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Cauchy Stress Vector XZ"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.NodeStressXZ)
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Cauchy Stress Vector YZ"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.NodeStressYZ)
            self.mesh_obj.Visibility= True
        elif (self.popup_result.currentText()=="Von Misses Stress"):
            self.mesh_obj.ViewObject.setNodeColorByScalars(self.result_obj.NodeNumbers, self.result_obj.vonMises)
            self.mesh_obj.Visibility= True

        self.mesh_obj.ViewObject.DisplayMode="Faces"

    def deVisualize(self):
        if self.visulizerun:
            self.mesh_obj.ViewObject.resetNodeColor()
            self.mesh_obj.Visibility= False

    def deVisualize_(self):
        if self.visulizerun:
            FreeCAD.activeDocument().removeObject('mesh_result')
            FreeCAD.activeDocument().removeObject('ResultMechanical')
            self.lines=[]
            self.FloatingPoints=[]
            self.locations=[]
            self.NumCell=[]
            self.cells=[]
            self.celltypes=[]
            self.displacement=[]
            self.cauchy=[]
            self.vonmisses=[]

    def onBrowseButton(self):
        self.browseWindow = QtGui.QFileDialog(self)
        self.browseWindow.setFileMode(QtGui.QFileDialog.ExistingFile)
        self.browseWindow.setNameFilter(str("*.vtk"))
        self.browseWindow.setViewMode(QtGui.QFileDialog.Detail)
        self.browseWindow.setDirectory(self.work_dir)

        if self.browseWindow.exec_():
            path_name_list = self.browseWindow.selectedFiles()
            self.textInput_pathname_.setText(path_name_list[0])
            self.deVisualize_()
            self.read_result()
            self.onVisualize_()

    def onCancel(self):
        self.result = "Cancel"
        self.close()
    
    def read_result(self):
        with open(self.textInput_pathname_.text(),'r') as f:
            self.lines = f.readlines()

        self.FloatingPoints=int(re.findall(r'\d+', self.lines[4])[0])

        self.locations=np.empty([self.FloatingPoints,3],dtype=float)
        for i in range(self.FloatingPoints):
            stringsofloc=re.findall("[-+]?[.]?[\\d]+(?:,\\d\\d\\d)*[\\.]?\\d*(?:[eE][-+]?\\d+)?", self.lines[5+i])
            floatofloc = list(map(float, stringsofloc))
            self.locations[i,:]=floatofloc
        
        self.NumCell=int(re.findall(r'\d+', self.lines[6+self.FloatingPoints])[0])
        self.cells=np.empty([self.NumCell,3],dtype=int)
        for i in range(self.NumCell):
            stringsofcell=re.findall("[-+]?[.]?[\\d]+(?:,\\d\\d\\d)*[\\.]?\\d*(?:[eE][-+]?\\d+)?", self.lines[7+self.FloatingPoints+i])
            stringsofcell.pop(0)
            intofcell = list(map(int, stringsofcell))
            self.cells[i,:]=intofcell

        self.celltypes=np.empty([self.NumCell,1],dtype=int)
        for i in range(self.NumCell):
            stringsofcelltype=re.findall("[-+]?[.]?[\\d]+(?:,\\d\\d\\d)*[\\.]?\\d*(?:[eE][-+]?\\d+)?", self.lines[9+self.FloatingPoints+self.NumCell+i])
            intofcelltype = list(map(int, stringsofcelltype))
            self.celltypes[i,:]=intofcelltype

        self.displacement=np.empty([self.FloatingPoints,3],dtype=float)
        for i in range(self.FloatingPoints):
            stringsofdisp=re.findall("[-+]?[.]?[\\d]+(?:,\\d\\d\\d)*[\\.]?\\d*(?:[eE][-+]?\\d+)?", self.lines[12+self.FloatingPoints+2*self.NumCell+i])
            floatsofdisp = list(map(float, stringsofdisp))
            self.displacement[i,:]=floatsofdisp

        self.cauchy=np.empty([self.FloatingPoints,6],dtype=float)
        for i in range(self.FloatingPoints):
            stringsofcauchy=re.findall("[-+]?[.]?[\\d]+(?:,\\d\\d\\d)*[\\.]?\\d*(?:[eE][-+]?\\d+)?", self.lines[13+2*self.FloatingPoints+2*self.NumCell+i])
            floatsofcauchy = list(map(float, stringsofcauchy))
            self.cauchy[i,:]=floatsofcauchy

        self.vonmisses=[]
        for i in range(self.FloatingPoints):
            stringsofvonmisses=re.findall("[-+]?[.]?[\\d]+(?:,\\d\\d\\d)*[\\.]?\\d*(?:[eE][-+]?\\d+)?", self.lines[14+3*self.FloatingPoints+2*self.NumCell+i])
            self.vonmisses.append(float(stringsofvonmisses[0]))

        #result mesh is created and nodes are added
        mesh_result=Fem.FemMesh()

        self.min_val=0
        self.max_val=10

        #add nodes
        for i in range(self.FloatingPoints):
            mesh_result.addNode(self.locations[i,0],self.locations[i,1],self.locations[i,2],i+1)
        
        #add faces
        for i in range(self.NumCell):
            mesh_result.addFace([self.cells[i,0]+1, self.cells[i,1]+1, self.cells[i,2]+1])

        self.obj=FreeCAD.ActiveDocument.addObject("Fem::FemMeshObject", "mesh_result")
        self.obj.FemMesh=mesh_result

        self.mechenical_result= FreeCAD.ActiveDocument.addObject("Fem::FemResultObjectPython", "ResultMechanical")
        self.mechenical_result.Mesh = FreeCAD.ActiveDocument.mesh_result
        result_mechanical.ResultMechanical(self.mechenical_result)

        #node numbers
        node_numbers=[]
        for i in range(self.FloatingPoints):
            node_numbers.append(i+1)

        self.mechenical_result.NodeNumbers=node_numbers
        
        #displacement vectors
        disp_vectors=[]
        for i in range(self.FloatingPoints):
            disp_vectors.append(FreeCAD.Vector(self.displacement[i,0],self.displacement[i,1], self.displacement[i,2]))
        
        self.mechenical_result.DisplacementVectors =disp_vectors

        #displacement lengths
        disp_lengths=[]
        for i in range(self.FloatingPoints):
            disp_lengths.append(pow(pow(self.displacement[i,0],2)+pow(self.displacement[i,1],2)+pow(self.displacement[i,2],2),0.5))
        
        self.mechenical_result.DisplacementLengths =disp_lengths

        self.mechenical_result.NodeStressXX=self.cauchy[:,0]
        self.mechenical_result.NodeStressYY=self.cauchy[:,1]
        self.mechenical_result.NodeStressZZ=self.cauchy[:,2]
        self.mechenical_result.NodeStressYZ=self.cauchy[:,3]
        self.mechenical_result.NodeStressXZ=self.cauchy[:,4]
        self.mechenical_result.NodeStressXY=self.cauchy[:,5]

        self.mechenical_result.vonMises=self.vonmisses

        self.mesh_obj=FreeCAD.ActiveDocument.getObject("mesh_result")
        self.result_obj=FreeCAD.ActiveDocument.getObject("ResultMechanical")

        self.mesh_obj.ViewObject.setNodeDisplacementByVectors(self.result_obj.NodeNumbers, self.result_obj.DisplacementVectors)
        self.mesh_obj.Visibility= False

    def onVisualize(self):
        if (self.visualizeButton.isChecked()):
            self.Visualize()
            self.update_gradient()
        else:
            self.deVisualize()

    def onVisualize_(self):
        if( self.visualizeButton.isChecked() ):
            self.Visualize()
            self.update_gradient()

    def onVisualize__(self):
        if self.visulizerun:
            if( self.visualizeButton.isChecked() ):
                self.Visualize()
                self.update_gradient()

    def run_task(self):
        print('in runtask')

    def get_min_max_values(self):
        if self.visulizerun:
            if (self.popup_result.currentText()=="Total Displacement"):
                return min(self.result_obj.DisplacementLengths), max(self.result_obj.DisplacementLengths)
            elif (self.popup_result.currentText()=="Displacement X"):
                return min(list(self.displacement[:,0])), max(list(self.displacement[:,0]))
            elif (self.popup_result.currentText()=="Displacement Y"):
                return min(list(self.displacement[:,1])), max(list(self.displacement[:,1]))
            elif (self.popup_result.currentText()=="Displacement Z"):
                return min(list(self.displacement[:,2])), max(list(self.displacement[:,2]))
            elif (self.popup_result.currentText()=="Cauchy Stress Vector XX"):
                return min(self.result_obj.NodeStressXX), max(self.result_obj.NodeStressXX)
            elif (self.popup_result.currentText()=="Cauchy Stress Vector YY"):
                return min(self.result_obj.NodeStressYY), max(self.result_obj.NodeStressYY)
            elif (self.popup_result.currentText()=="Cauchy Stress Vector ZZ"):
                return min(self.result_obj.NodeStressZZ), max(self.result_obj.NodeStressZZ)
            elif (self.popup_result.currentText()=="Cauchy Stress Vector XY"):
                return min(self.result_obj.NodeStressXY), max(self.result_obj.NodeStressXY)
            elif (self.popup_result.currentText()=="Cauchy Stress Vector XZ"):
                return min(self.result_obj.NodeStressXZ), max(self.result_obj.NodeStressXZ)
            elif (self.popup_result.currentText()=="Cauchy Stress Vector YZ"):
                return min(self.result_obj.NodeStressYZ), max(self.result_obj.NodeStressYZ)
            elif (self.popup_result.currentText()=="Von Misses Stress"):
                return min(self.result_obj.vonMises), max(self.result_obj.vonMises)
        else:
            return 0, 1
           
    def update_gradient(self):
        self.min_val, self.max_val=self.get_min_max_values()
        gradient_bar = GradientBar(self.min_val, self.max_val)
        self.layout().replaceWidget(self.layout().itemAt(1).itemAt(0).widget(), gradient_bar)
        self.colorGradient=gradient_bar
        self.layout().update()

class GradientBar(QtWidgets.QWidget):
    def __init__(self, min_val, max_val):
        super().__init__()
        self.setMinimumWidth(280)
        self.setMaximumWidth(280)
        self.setMinimumHeight(30)
        self.min_val = min_val
        self.max_val = max_val
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(280)
        self.setMaximumWidth(280)
        self.setMinimumHeight(30)
        self.min_val_label = QtGui.QLabel(f'{self.min_val:.2e}')
        self.max_val_label = QtGui.QLabel(f'{self.max_val:.2e}')
        self.min_val_label.setAlignment(QtGui.Qt.AlignLeft)
        self.max_val_label.setAlignment(QtGui.Qt.AlignRight)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create a gradient for the bar
        gradient = QtGui.QLinearGradient(0, 0, self.width(), 0)
        self.min_val
        self.max_val
        if((self.min_val>0) and (self.max_val>0)):
            ratio=self.max_val/(255*2)
            min_valgoes=self.min_val/ratio
            if(min_valgoes>255):
                gradient.setColorAt(0, QtGui.QColor(255,255-(min_valgoes-255),0))
            elif(min_valgoes<=255):
                gradient.setColorAt(0, QtGui.QColor(min_valgoes,255,0)) 
            gradient.setColorAt(1, QtGui.QColor(255,0,0))
        elif((self.min_val==0) and (self.max_val>0)):
            gradient.setColorAt(0, QtGui.QColor(0,255,0))
            gradient.setColorAt(1, QtGui.QColor(255,0,0))
        elif((self.min_val<0) and (self.max_val>0)):
            ratio=(-self.min_val)/(self.max_val-self.min_val)
            gradient.setColorAt(0, QtGui.QColor(0,0,255))
            gradient.setColorAt(ratio, QtGui.QColor(0,255,0))
            gradient.setColorAt(1, QtGui.QColor(255,0,0))
        elif((self.min_val<0) and (self.max_val==0)):
            gradient.setColorAt(0, QtGui.QColor(0,0,255))
            gradient.setColorAt(1, QtGui.QColor(0,255,0))
        elif((self.min_val<0) and (self.max_val<0)):
            gradient.setColorAt(0, QtGui.QColor(0,0,255))
            ratio=self.min_val/(255*2)
            max_valgoes=self.max_val/ratio
            if(max_valgoes>255):
                gradient.setColorAt(1, QtGui.QColor(0,255-(max_valgoes-255),255))
            elif(max_valgoes<=255):
                gradient.setColorAt(1, QtGui.QColor(0,255,max_valgoes)) 

        rect = event.rect()
        painter.fillRect(rect, gradient)

        num_intervals = 5
        interval = (self.max_val - self.min_val) / num_intervals

        # Draw scale (tick marks)
        painter.setPen(QtGui.QColor(0, 0, 0))
        for i in range(num_intervals + 1):
            x = i * (self.width() / num_intervals)
            painter.drawLine(x, self.height() - 5, x, self.height())

        # Draw numerical values
        values = [f'{self.min_val + i * interval:.2e}' for i in range(num_intervals + 1)]
        for i, value in enumerate(values):
            x = i * (self.width() / num_intervals) - 10
            label = QtGui.QLabel(value)
            label.setAlignment(QtGui.Qt.AlignCenter)
            label.setGeometry(x, self.height() - 20, 40, 20)
            label.setParent(self)
            label.show()