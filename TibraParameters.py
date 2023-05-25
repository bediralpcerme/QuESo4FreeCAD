from FreeCAD_PySide import *
import sys
import os
import FreeCAD
import Mesh
import json


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
        width = 400
        height = 600
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Tibra Parameters")

        #Initial Parameters input:

        #main (general) head
        self.label_main_ = QtGui.QLabel("General settings:", self)
        self.label_main_.move(10, 10)

        #name of file
        self.label_filename_ = QtGui.QLabel("Name of exporting file:", self)
        self.label_filename_.move(10, 40)
        self.textInput_filename_ = QtGui.QLineEdit(self)
        self.textInput_filename_.setText("Box_1")
        self.textInput_filename_.setFixedWidth(200)
        self.textInput_filename_.move(10, 60)

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
 
        self.textInput_nElemets_z_ = QtGui.QLineEdit(self)
        self.textInput_nElemets_z_.setText("z")
        self.textInput_nElemets_z_.setFixedWidth(70)
        self.textInput_nElemets_z_.move(210, 360)

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
        self.textInput_integration_ = QtGui.QLineEdit(self)
        self.textInput_integration_.setText("GGQ_Optimal")
        self.textInput_integration_.setFixedWidth(200)
        self.textInput_integration_.move(10, 490)


        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.move(200, 550)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)
        okButton.move(80, 550)

    
    def onOk(self):
        #Setting working directory - NEED TO BE CHANGED
        os.chdir('C:\\Users\DanielP\Desktop\Example')

        #Creating TIBRA directory:
        if os.path.isdir('TIBRA'):
            os.chdir('TIBRA')
        else:
            os.mkdir('TIBRA')
            os.chdir('TIBRA')
            
        if os.path.isdir('data'):
            None
        else:
            os.mkdir('data')
       

        TibraParam = {
        
            "general_settings"   : {
            "input_filename"  : "data/steering_knuckle.stl",
            "echo_level"      : 1
            },
            "mesh_settings"     : {
                "lower_bound": [0.0, 0.0, 0.0],
                "upper_bound": [20.0, 190.0, 190.0],
                "polynomial_order" : [2, 2, 2],
                "number_of_elements" : [60, 120, 120]
            },
            "trimmed_quadrature_rule_settings"     : {
                "moment_fitting_residual": 1e-6
            },
            "non_trimmed_quadrature_rule_settings" : {
                "integration_method" : "GGQ_Optimal"
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
    
    def textExtractor(self):
         self.myStr = self.textInput_.text()
         return self.myStr
    