from FreeCAD_PySide import *
import sys
import os
import FreeCAD
import Mesh
import json


### UPDATE ###
# Bediralp currently commented "Creating TIBRA directory" part. Please tell him what is the goal 
# of creating such a directory.

#TO DO LIST: 
# - make option to choose working directory manually (on Windows its not established automatically while saving project)
# - would be nice to have checkbox while setting the integration method instead of textblock 
# - Font size in pop-up windows could be greater a bit

class TibraParameters(QtGui.QDialog):
    """"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #position and geometry of the dialog box
        width = 340
        height = 600
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Tibra Parameters")

        #Initial Parameters input:

        #main (general) head
        self.label_main_ = QtGui.QLabel("General settings:", self)
        self.label_main_.move(10, 10)

        #path to the file
        self.label_pathname_ = QtGui.QLabel("Path to the STL file:", self)
        self.label_pathname_.move(10, 40)

        #Text edit of pathname
        self.textInput_pathname_ = QtGui.QLineEdit(self)
        self.textInput_pathname_.setText("")
        self.textInput_pathname_.setFixedWidth(200)
        self.textInput_pathname_.move(10, 60)

        #file browser button
        self.fileBrowseButton = QtGui.QPushButton('Browse files',self)
        self.fileBrowseButton.clicked.connect(self.onBrowseButton)
        self.fileBrowseButton.setAutoDefault(False)
        self.fileBrowseButton.move(220, 60)


        #label text
        self.label_echo_ = QtGui.QLabel("Echo level:", self)
        self.label_echo_.move(10, 100)
        self.textInput_echo_ = QtGui.QLineEdit(self)
        self.textInput_echo_.setText("1")
        self.textInput_echo_.setFixedWidth(50)
        self.textInput_echo_.move(10, 120)
        
        #mesh head
        self.label_main_ = QtGui.QLabel("Mesh settings:", self)
        self.label_main_.move(10, 160)

        '''we dont need it anymore but im leaving it here just in case
        #lower bound
        self.label_lowerbound_ = QtGui.QLabel("Lower bound:", self)
        self.label_lowerbound_.move(10, 190)

        self.textInput_lowerbound_x_ = QtGui.QLineEdit(self)
        self.textInput_lowerbound_x_.setText("x")
        self.textInput_lowerbound_x_.setFixedWidth(70)
        self.textInput_lowerbound_x_.move(10, 210)

        self.textInput_lowerbound_y_ = QtGui.QLineEdit(self)
        self.textInput_lowerbound_y_.setText("y")
        self.textInput_lowerbound_y_.setFixedWidth(70)
        self.textInput_lowerbound_y_.move(110, 210)
 
        self.textInput_lowerbound_z_ = QtGui.QLineEdit(self)
        self.textInput_lowerbound_z_.setText("z")
        self.textInput_lowerbound_z_.setFixedWidth(70)
        self.textInput_lowerbound_z_.move(210, 210)

        #upper bound
        self.label_upperbound_ = QtGui.QLabel("Upper bound:", self)
        self.label_upperbound_.move(10, 240)

        self.textInput_upperbound_x_ = QtGui.QLineEdit(self)
        self.textInput_upperbound_x_.setText("x")
        self.textInput_upperbound_x_.setFixedWidth(70)
        self.textInput_upperbound_x_.move(10, 260)

        self.textInput_upperbound_y_ = QtGui.QLineEdit(self)
        self.textInput_upperbound_y_.setText("y")
        self.textInput_upperbound_y_.setFixedWidth(70)
        self.textInput_upperbound_y_.move(110, 260)

        self.textInput_upperbound_z_ = QtGui.QLineEdit(self)
        self.textInput_upperbound_z_.setText("z")
        self.textInput_upperbound_z_.setFixedWidth(70)
        self.textInput_upperbound_z_.move(210, 260)
        '''

        #polynomial order
        self.label_polynomialOrder_ = QtGui.QLabel("Polynomial order:", self)
        self.label_polynomialOrder_.move(10, 290)

        self.textInput_polynomialOrder_x_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_x_.setText("x")
        self.textInput_polynomialOrder_x_.setFixedWidth(70)
        self.textInput_polynomialOrder_x_.move(10, 310)

        self.textInput_polynomialOrder_y_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_y_.setText("y")
        self.textInput_polynomialOrder_y_.setFixedWidth(70)
        self.textInput_polynomialOrder_y_.move(110, 310)
 
        self.textInput_polynomialOrder_z_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_z_.setText("z")
        self.textInput_polynomialOrder_z_.setFixedWidth(70)
        self.textInput_polynomialOrder_z_.move(210, 310)

        #number of elements
        self.label_nElements_ = QtGui.QLabel("Number of elements:", self)
        self.label_nElements_.move(10, 340)

        self.textInput_nElements_x_ = QtGui.QLineEdit(self)
        self.textInput_nElements_x_.setText("x")
        self.textInput_nElements_x_.setFixedWidth(70)
        self.textInput_nElements_x_.move(10, 360)

        self.textInput_nElements_y_ = QtGui.QLineEdit(self)
        self.textInput_nElements_y_.setText("y")
        self.textInput_nElements_y_.setFixedWidth(70)
        self.textInput_nElements_y_.move(110, 360)
 
        self.textInput_nElements_z_ = QtGui.QLineEdit(self)
        self.textInput_nElements_z_.setText("z")
        self.textInput_nElements_z_.setFixedWidth(70)
        self.textInput_nElements_z_.move(210, 360)

        #solution settings head
        self.label_main_ = QtGui.QLabel("Solution settings:", self)
        self.label_main_.move(10, 400)

        #residual setting
        self.label_residual_ = QtGui.QLabel("Moment fitting residual:", self)
        self.label_residual_.move(10, 420)
        self.textInput_residual_ = QtGui.QLineEdit(self)
        self.textInput_residual_.setText("1e-6")
        self.textInput_residual_.setFixedWidth(50)
        self.textInput_residual_.move(10, 440)

        #integration method setting
        self.label_integration_ = QtGui.QLabel("Integration method:", self)
        self.label_integration_.move(10, 470)
        self.popup_integration = QtGui.QComboBox(self)
        self.popup_integration_items = ("Gauss","Gauss_Reduced1","Gauss_Reduced2","GGQ_Optimal","GGQ_Reduced1", "GGQ_Reduced2")
        self.popup_integration.addItems(self.popup_integration_items)
        self.popup_integration.setFixedWidth(200)
        self.popup_integration.move(10, 490)
        
        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.move(200, 550)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)
        okButton.move(80, 550)

    def onBrowseButton(self):
        docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        open_dir = FreeCAD.ActiveDocument.FileName
        open_dir = open_dir.replace(docName,"")

        self.browseWindow = QtGui.QFileDialog(self)
        self.browseWindow.setFileMode(QtGui.QFileDialog.ExistingFile)
        self.browseWindow.setNameFilter(str("*.stl"))
        self.browseWindow.setViewMode(QtGui.QFileDialog.Detail)
        self.browseWindow.setDirectory(open_dir)

        if self.browseWindow.exec_():
            path_name_list = self.browseWindow.selectedFiles()
            self.textInput_pathname_.setText(path_name_list[0])
    
    def onOk(self):
        #bounds
        mybounds=self.bounds()

        #bounds with 0.1 offset in total
        
        self.lowerbound_x_=mybounds[0]-(abs(mybounds[0]-mybounds[3]))*0.05
        self.lowerbound_y_=mybounds[1]-(abs(mybounds[1]-mybounds[4]))*0.05
        self.lowerbound_z_=mybounds[2]-(abs(mybounds[2]-mybounds[5]))*0.05
        self.upperbound_x_=mybounds[3]+(abs(mybounds[0]-mybounds[3]))*0.05
        self.upperbound_y_=mybounds[4]+(abs(mybounds[1]-mybounds[4]))*0.05
        self.upperbound_z_=mybounds[5]+(abs(mybounds[2]-mybounds[5]))*0.05

        '''
        #bounds without 0.1 offset in total
        self.lowerbound_x_=mybounds[0]
        self.lowerbound_y_=mybounds[1]
        self.lowerbound_z_=mybounds[2]
        self.upperbound_x_=mybounds[3]
        self.upperbound_y_=mybounds[4]
        self.upperbound_z_=mybounds[5]
        '''

        #Creating TIBRA directory:
        # if os.path.isdir('TIBRA'):
        #     os.chdir('TIBRA')
        # else:
        #     os.mkdir('TIBRA')
        #     os.chdir('TIBRA')
            
        # if os.path.isdir('data'):
        #     None
        # else:
        #     os.mkdir('data')
       
        TibraParam = {
        
            "general_settings"   : {
            "echo_level"      :  int(self.textInput_echo_.text()),
            "input_filename"  :  self.textInput_pathname_.text()
            },
            "mesh_settings"     : {
                "lower_bound": [ self.lowerbound_x_,self.lowerbound_y_, self.lowerbound_z_],
                "upper_bound": [ self.upperbound_x_, self.upperbound_y_, self.upperbound_z_],
                "polynomial_order" : [ int(self.textInput_polynomialOrder_x_.text()), int(self.textInput_polynomialOrder_y_.text()), int(self.textInput_polynomialOrder_z_.text())],
                "number_of_elements" : [ int(self.textInput_nElements_x_.text()),  int(self.textInput_nElements_y_.text()), int(self.textInput_nElements_z_.text())]
            },
            "trimmed_quadrature_rule_settings"     : {
                "moment_fitting_residual": float(self.textInput_residual_.text())
            },
            "non_trimmed_quadrature_rule_settings" : {
                "integration_method" : self.popup_integration.currentText()
            }
        }

        # Creating TibraParameters.json file:
        with open('TIBRAParameters.json', 'w') as f:
            json.dump(TibraParam, f, indent=4, separators=(", ", ": "), sort_keys=True)
            pass
            
        # Creating Tibra_main.py file:
        with open('TIBRA_main.py', 'w') as f:
            f.write('''
# Project imports
from TIBRA_PythonApplication.PyTIBRA import PyTIBRA

def main():
    pytibra = PyTIBRA("TIBRAParameters.json")
    pytibra.Run()

if __name__ == "__main__":
    main()''')

            pass

        self.result = "Ok"
        self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()
  
    
    def bounds(self):
        print(os.getcwd())
        mesh = Mesh.Mesh(self.textInput_pathname_.text())
        
        # boundBox
        boundBox_    = mesh.BoundBox

        boundBoxXMin = boundBox_.XMin
        boundBoxYMin = boundBox_.YMin
        boundBoxZMin = boundBox_.ZMin

        boundBoxXMax = boundBox_.XMax
        boundBoxYMax = boundBox_.YMax
        boundBoxZMax = boundBox_.ZMax

        return [boundBoxXMin,boundBoxYMin,boundBoxZMin,boundBoxXMax,boundBoxYMax,boundBoxZMax]
    