from FreeCAD_PySide import QtGui, QtCore
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
import math

class PostProcess(QtGui.QDialog):
    #Class containing GUI and its variables
    #Beginning with defining a signal which will be emitted upon resizing the window

    resized = QtCore.Signal()

    def __init__(self):
        #Initialization of starting parameters and GUI
        super(PostProcess, self).__init__()
        self.visulizerun=False
        self.slider_num=1
        self.initUI()

    def initUI(self):

##########################################################################################
##                                                                                      ##
##                       SETTING UP THE PostProcess POP-UP WINDOW                       ##
##                                                                                      ##
##########################################################################################

        '''Constructs the GUI and other usables
        '''
        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")

        #position and geometry of the dialog box is set
        std_validate = QtGui.QIntValidator()
        scientific_validate = QtGui.QDoubleValidator()
        scientific_validate.setNotation(QtGui.QDoubleValidator.ScientificNotation)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, on = True)
        self.setWindowTitle("Post Process")

        self.small_font = QtGui.QFont("Arial", 8)
        self.layout = QtGui.QGridLayout()

        self.min_val, self.max_val = self.get_min_max_values()

        #path to the file
        self.label_pathname_ = QtGui.QLabel("Path to the result file:", self)
        self.layout.addWidget(self.label_pathname_, 0, 0, QtCore.Qt.AlignLeft)

        self.layout.setRowMinimumHeight(1, 3)

        #Text edit of pathname
        self.textInput_pathname_ = QtGui.QLineEdit(self)
        self.textInput_pathname_.setText("")

##**************************************************************************************##
##                          Beginning Definition of Buttons                             ##
##**************************************************************************************##

        #file browser button
        fileBrowseButton = QtGui.QPushButton('Browse files', self)
        fileBrowseButton.setAutoDefault(False)

        sublayout = QtGui.QHBoxLayout()
        sublayout.addWidget(self.textInput_pathname_)
        sublayout.addWidget(fileBrowseButton)
        sublayout.setSpacing(5)

        self.layout.addLayout(sublayout, 2, 0)

        self.layout.setRowMinimumHeight(3, 7)

        #method setting
        self.label_result_ = QtGui.QLabel("Results:", self)
        self.popup_result = QtGui.QComboBox(self)
        self.popup_result_items = ("Displacement X","Displacement Y","Displacement Z","Total Displacement","Cauchy Stress Vector XX", "Cauchy Stress Vector YY","Cauchy Stress Vector ZZ","Cauchy Stress Vector XY","Cauchy Stress Vector XZ","Cauchy Stress Vector YZ","Von Misses Stress")
        self.popup_result.addItems(self.popup_result_items)

        sublayout = QtGui.QHBoxLayout()
        sublayout.addWidget(self.label_result_, 0, QtCore.Qt.AlignLeft)
        sublayout.addWidget(self.popup_result, 1, QtCore.Qt.AlignLeft)
        sublayout.setSpacing(5)

        self.layout.addLayout(sublayout, 4, 0)

        self.layout.setRowMinimumHeight(5, 3)
        
        # visualize button
        self.visualizeButton = QtGui.QCheckBox('Visualize the output', self)

        self.layout.addWidget(self.visualizeButton, 6, 0, QtCore.Qt.AlignLeft)

        self.layout.setRowMinimumHeight(7, 7)

        # slider
        self.label_slider_ = QtGui.QLabel('Scale: ' + str(self.get_max_length()), self)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(50)
        self.slider.setValue((self.get_max_length()))

        sublayout = QtGui.QHBoxLayout()
        sublayout.addWidget(self.label_slider_, 0, QtCore.Qt.AlignLeft)
        sublayout.addWidget(self.slider, 1)
        sublayout.setSpacing(5)

        self.layout.addLayout(sublayout, 8, 0, 1, -1)

        self.layout.setRowMinimumHeight(9, 5)

        self.min_label = QtGui.QLabel("Min. value: " + str(self.min_val), self)
        self.min_label.setFont(self.small_font)
        self.max_label = QtGui.QLabel("Max. value: " + str(self.max_val), self)
        self.max_label.setFont(self.small_font)

        sublayout = QtGui.QHBoxLayout()
        sublayout.addWidget(self.min_label, 0, QtCore.Qt.AlignLeft)
        sublayout.addWidget(self.max_label, 1, QtCore.Qt.AlignRight)
        sublayout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(sublayout, 10, 0)

        self.layout.setRowMinimumHeight(11, 0)


        # color gradient
        self.colorGradient = GradientBar(self.min_val, self.max_val, self.width())
        self.layout.addWidget(self.colorGradient, 12, 0)

        self.setLayout(self.layout)

        width = self.sizeHint().width() + 100
        height = self.sizeHint().height()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setFixedHeight(height)
        self.setMinimumWidth(width)

        fileBrowseButton.clicked.connect(self.onBrowseButton)
        self.popup_result.currentTextChanged.connect(self.onVisualize__)
        self.visualizeButton.stateChanged.connect(self.onVisualize)
        self.slider.valueChanged.connect(self.slider_function)
        self.resized.connect(self.windowSizedChanged)

        self.show()

##  **************************************************************************************

##**************************************************************************************##
##                          Beginning of Functions Doing Tasks                          ##
##**************************************************************************************##

## ---- Visualize Function for Different Modes -------------------------------------------

    def Visualize(self):
        '''Visualization function, it makes mesh visible depending on which mode is selected on the combo box for the same mesh
        '''
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

##  --------------------------------------------------------------------------------------

## ---- Devisualize Function for the Mesh  -----------------------------------------------
        
    def deVisualize(self):
        '''Makes mesh unvisible for the same mesh
        '''
        if self.visulizerun:
            self.mesh_obj.ViewObject.resetNodeColor()
            self.mesh_obj.Visibility= False

##  --------------------------------------------------------------------------------------

## ---- Devisualize Function for Another Mesh  -------------------------------------------
            
    def deVisualize_(self):
        '''Deletes mesh and empties variables for other mesh installation
        '''
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

##  --------------------------------------------------------------------------------------

## ---- Browse Function -----------------------------------------------------------------
            
    def onBrowseButton(self):
        '''When browse button is clicked, mesh is deleted, new mesh is read and visualized
        '''
        browseWindow = QtGui.QFileDialog.getOpenFileName(self, "Select the Result File", self.work_dir, "*.vtk")
        print(browseWindow[0])
        print(browseWindow[1])
        self.textInput_pathname_.setText(browseWindow[0])
        self.deVisualize_()
        self.read_result()
        self.onVisualize_()

##  --------------------------------------------------------------------------------------

## ---- Resizing Function for Whole Pop-op Window  ---------------------------------------
        
    def resizeEvent(self, event):
        '''Does resizing of the window. Also, the signal is emitted to be caught 
        by update_gradient, when window width is divisible with 50.
        '''
        if (self.width()%50 == 0):
            self.resized.emit()
        return super(PostProcess, self).resizeEvent(event)
    
##  --------------------------------------------------------------------------------------
 
## ---- Resizing and Updating Color Gradient Function ------------------------------------

    def windowSizedChanged(self):
        '''It catches the signal emitted by the resizeEvent, and calls update_gradient function.
        '''
        self.update_gradient()

##  --------------------------------------------------------------------------------------

## ---- Cancel ---------------------------------------------------------------------------

    def onCancel(self):
        '''Cancel button
        '''
        self.result = "Cancel"
        self.close()

##  --------------------------------------------------------------------------------------

## ---- Read VTK File Function -----------------------------------------------------------

    def read_result(self):
        '''Reads vtk file and constructs mesh objects needed
        '''
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

        self.update_slider(self.get_max_length())
        self.slider.setValue(self.get_max_length())

##  --------------------------------------------------------------------------------------

## ---- Visulize Function for Visualize Button -------------------------------------------

    def onVisualize(self):
        '''Visulizes or devisualize depending on the visualize button
        '''
        if (self.visualizeButton.isChecked()):
            self.Visualize()
            self.update_gradient()
        else:
            self.deVisualize()

## --------------------------------------------------------------------------------------

## ---- Visulize Function for Reading File -----------------------------------------------

    def onVisualize_(self):
        '''First visualization after reading vtk file
        '''
        if( self.visualizeButton.isChecked() ):
            self.Visualize()
            self.update_gradient()

##  --------------------------------------------------------------------------------------

## ---- Visulize Function for Mode Changing ----------------------------------------------

    def onVisualize__(self):
        '''Combo box mode changing triggers this visualization with visulaization and gradient updatig
        '''
        if self.visulizerun:
            if( self.visualizeButton.isChecked() ):
                self.Visualize()
                self.update_gradient()

##  --------------------------------------------------------------------------------------

## ---- Slider Function for Mesh Displacement --------------------------------------------

    def slider_function(self):
        '''Depending on which number slider is on, displacement of the mesh changes
        '''
        if self.visulizerun:
            if( self.visualizeButton.isChecked() ):
                self.update_slider(self.slider.value())
                self.mesh_obj.ViewObject.applyDisplacement(self.slider.value())

##  --------------------------------------------------------------------------------------
                
## ---- Min/Max Function for Colour Gradient ---------------------------------------------

    def get_min_max_values(self):
        '''Minimum or maximum values are return depending on the physical quantity mode
        '''
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
        
##  --------------------------------------------------------------------------------------

## ---- Ratio to Set Slider for Mesh Displacement ----------------------------------------

    def get_max_length(self):
        '''Ratio for scaling displacement on mesh to make it naked to eye is obtained
        '''
        if self.visulizerun:
            list_length=[np.max(self.locations[0,:])-np.min(self.locations[0,:]),np.max(self.locations[1,:])-np.min(self.locations[1,:]),np.max(self.locations[2,:])-np.min(self.locations[2,:])]
            ratio=max(list_length)/max(self.result_obj.DisplacementLengths)*0.1
            return ratio
        else:
            return  1
        
##  --------------------------------------------------------------------------------------

## ---- Slider Update Function -----------------------------------------------------------

    def update_slider(self,new_ratio):
        '''Slider size update
        '''
        self.layout.itemAtPosition(8, 0).itemAt(0).widget().setText('Scale: ' + str(new_ratio))
        self.layout.update()

##  --------------------------------------------------------------------------------------

## ---- Update Colour Gradient Function --------------------------------------------------

    def update_gradient(self):
        '''Color gradient is obtained with texts and max/min values.
        Depending on the signal emitted by the resizeEvent, when the windowSizedChanged 
        catches that signal, it calls this function.
        '''
        self.min_val, self.max_val = self.get_min_max_values()
        gradient_bar = GradientBar(self.min_val, self.max_val, self.width())

        self.layout.itemAtPosition(12, 0).widget().setParent(None)
        self.layout.addWidget(gradient_bar, 12, 0)
        self.colorGradient = gradient_bar
        
        min_val_round = "{:.4f}".format(self.min_val)
        min_label_text = "Min. value: " + min_val_round
        self.layout.itemAtPosition(10, 0).itemAt(0).widget().setText(min_label_text)
        self.layout.itemAtPosition(10, 0).itemAt(0).widget().setFont(self.small_font)
        max_val_round = "{:.4f}".format(self.max_val)
        max_label_text = "Max. value: " + str(max_val_round)
        self.layout.itemAtPosition(10, 0).itemAt(1).widget().setText(max_label_text)
        self.layout.itemAtPosition(10, 0).itemAt(1).widget().setFont(self.small_font)
        self.layout.update()

##  --------------------------------------------------------------------------------------

##  **************************************************************************************

##--------------------------------------------------------------------------------------##
##                         Construction of Colour Gradient Bar                          ##
##--------------------------------------------------------------------------------------##

class GradientBar(QtGui.QWidget):
    '''Class to define and have color gradient bar depending on the maximum/minimum values and width
    '''
    def __init__(self, min_val, max_val, width_val):
        ''' Initialization of starting parameters and widget
        '''
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.width_val = width_val
        self.initUI()

    def initUI(self):
        ''' Aligns the widget and writes maximum/minimum values
        '''
        self.setMinimumHeight(30)
        self.min_val_label = QtGui.QLabel(f'{self.min_val:.2e}')
        self.max_val_label = QtGui.QLabel(f'{self.max_val:.2e}')
        self.min_val_label.setAlignment(QtCore.Qt.AlignLeft)
        self.max_val_label.setAlignment(QtCore.Qt.AlignRight)

    def paintEvent(self, event):
        ''' Coloring of the bar is done
        '''
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create a gradient for the bar
        gradient = QtGui.QLinearGradient(0, 0, self.width(), 0)
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

        if (self.width_val < 400):
            num_intervals = 5
        else:
            num_intervals = 5 + math.floor((self.width_val - 400)/100)
        
        interval = (self.max_val - self.min_val) / num_intervals

        # Draw scale (tick marks)
        painter.setPen(QtGui.QColor(0, 0, 0))
        for i in range(num_intervals + 1):
            x = i * (self.width() / num_intervals)
            painter.drawLine(x, self.height() - 5, x, self.height())

        small_font = QtGui.QFont("Arial", 8)
        painter.setPen(QtGui.QPen())
        painter.setFont(small_font)
        for i in range(num_intervals + 1):
            x = i * (self.width() / num_intervals)
            value = f'{self.min_val + i * interval:.2e}'
            if(x != QtCore.QRectF(rect).x()) and (x != QtCore.QRectF(rect).width()):
                painter.drawText(x - 20 , self.height() - 20, value)

##  **************************************************************************************
                
## #######################################################################################