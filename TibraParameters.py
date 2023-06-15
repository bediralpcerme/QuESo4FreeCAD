from FreeCAD_PySide import *
import os
import FreeCAD
import FreeCADGui as Gui
import Mesh
import json
from pivy import coin

##################

# The code is not finished yet

##################

#TO DO LIST: 
# - Font size in pop-up windows could be greater a bit

class TibraParameters(QtGui.QDialog):
    """"""
    def __init__(self):
        super(TibraParameters, self).__init__()
        self.initUI()

    def initUI(self):

        #position and geometry of the dialog box
        width = 340
        height = 700
        self.centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(self.centerPoint.x()-0.5*width, self.centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Tibra Parameters")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")
        self.Neumann_count = 1
        self.dirichlet_count = 1

        #Initial Parameters input:

        #main (general) head
        self.label_main_ = QtGui.QLabel("General settings:", self)
        self.label_main_.move(10, 10)
        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        self.label_main_.setFont(boldFont)

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
        self.label_main_.setFont(boldFont)

        # we dont need it anymore but im leaving it here just in case
        # #lower bound
        # self.label_lowerbound_ = QtGui.QLabel("Lower bound:", self)
        # self.label_lowerbound_.move(10, 190)

        # self.textInput_lowerbound_x_ = QtGui.QLineEdit(self)
        # self.textInput_lowerbound_x_.setText("x")
        # self.textInput_lowerbound_x_.setFixedWidth(70)
        # self.textInput_lowerbound_x_.move(10, 210)

        # self.textInput_lowerbound_y_ = QtGui.QLineEdit(self)
        # self.textInput_lowerbound_y_.setText("y")
        # self.textInput_lowerbound_y_.setFixedWidth(70)
        # self.textInput_lowerbound_y_.move(110, 210)
 
        # self.textInput_lowerbound_z_ = QtGui.QLineEdit(self)
        # self.textInput_lowerbound_z_.setText("z")
        # self.textInput_lowerbound_z_.setFixedWidth(70)
        # self.textInput_lowerbound_z_.move(210, 210)

        # #upper bound
        # self.label_upperbound_ = QtGui.QLabel("Upper bound:", self)
        # self.label_upperbound_.move(10, 240)

        # self.textInput_upperbound_x_ = QtGui.QLineEdit(self)
        # self.textInput_upperbound_x_.setText("x")
        # self.textInput_upperbound_x_.setFixedWidth(70)
        # self.textInput_upperbound_x_.move(10, 260)

        # self.textInput_upperbound_y_ = QtGui.QLineEdit(self)
        # self.textInput_upperbound_y_.setText("y")
        # self.textInput_upperbound_y_.setFixedWidth(70)
        # self.textInput_upperbound_y_.move(110, 260)

        # self.textInput_upperbound_z_ = QtGui.QLineEdit(self)
        # self.textInput_upperbound_z_.setText("z")
        # self.textInput_upperbound_z_.setFixedWidth(70)
        # self.textInput_upperbound_z_.move(210, 260)
        # 

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
        self.label_main_.setFont(boldFont)

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

        #BC settings
        self.label_ApplyBC_ = QtGui.QLabel("Boundary Conditions:", self)
        self.label_ApplyBC_.move(10, 535)
        self.label_ApplyBC_.setFont(boldFont)

        self.button_Dirichlet_ = QtGui.QPushButton('Apply Dirichlet B.C.',self)
        self.button_Dirichlet_.clicked.connect(self.onDirichletBC)
        self.button_Dirichlet_.setAutoDefault(False)
        self.button_Dirichlet_.move(10, 555)

        self.button_Neumann_ = QtGui.QPushButton('Apply Neumann B.C.',self)
        self.button_Neumann_.clicked.connect(self.onNeumannBC)
        self.button_Neumann_.setAutoDefault(False)
        self.button_Neumann_.move(180, 555)

        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.move(200, 650)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)
        okButton.move(80, 650)

        # show the dialog box
        self.DirichletBCBox_flag = False
        self.DirichletBCBox_Fun()
        self.show()

                            ############################# FUNCTION DEFINITIONS #############################

    def onBrowseButton(self):
        self.browseWindow = QtGui.QFileDialog(self)
        self.browseWindow.setFileMode(QtGui.QFileDialog.ExistingFile)
        self.browseWindow.setNameFilter(str("*.stl"))
        self.browseWindow.setViewMode(QtGui.QFileDialog.Detail)
        self.browseWindow.setDirectory(self.work_dir)

        if self.browseWindow.exec_():
            path_name_list = self.browseWindow.selectedFiles()
            self.textInput_pathname_.setText(path_name_list[0])


    def onDirichletBC(self):
        self.DirichletDialogBox_Fun()
        self.DirichletDialogBox.exec_()

    def DirichletDialogBox_Fun(self):

        self.DirichletDialogBox = QtGui.QDialog(self)
        width = 470
        height = 100
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.DirichletDialogBox.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.DirichletDialogBox.setWindowTitle("Apply Dirichlet Boundary Condition")

        self.DirichletDialogBox.label_dirichlet = QtGui.QLabel("Please enter the number faces subject to Dirichlet BC:", self.DirichletDialogBox)
        self.DirichletDialogBox.label_dirichlet.move(10, 30)

        self.DirichletDialogBox.DirichletFaceNumber = QtGui.QLineEdit(self.DirichletDialogBox)
        self.DirichletDialogBox.DirichletFaceNumber.setPlaceholderText("example: 3")
        self.DirichletDialogBox.DirichletFaceNumber.setFixedWidth(80)
        self.DirichletDialogBox.DirichletFaceNumber.move(380, 28)

        okButton_DirichletDialogBox = QtGui.QPushButton('OK', self.DirichletDialogBox)
        okButton_DirichletDialogBox.move(0.5*width - 15, 65)
        okButton_DirichletDialogBox.clicked.connect(self.okButton_DirichletDialogBox)
        okButton_DirichletDialogBox.setAutoDefault(True)
        

    def okButton_DirichletDialogBox(self):
        self.dirichlet_faces= self.DirichletDialogBox.DirichletFaceNumber.text()
        infoBox = QtGui.QMessageBox.information(self.DirichletDialogBox, "Apply Dirichlet Boundary Conditions", \
                                                "Please select " + self.dirichlet_faces + \
                                                " faces subject to Dirichlet BC one by one!")
        
        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_DirichletBCBox)
            self.DirichletDialogBox.close()
            self.setVisible(False)


    def getMouseClick_DirichletBCBox(self, event_cb):   
        event = event_cb.getEvent()
        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) & (Gui.Selection.hasSelection() == True):
            if (self.dirichlet_count <= int(self.dirichlet_faces)):
                    self.DirichletBCBox_Fun()               
                    self.DirichletBCBox.exec_()
                    if(self.dirichlet_count > int(self.dirichlet_faces)):
                        self.setVisible(True)
                        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
                        

    def DirichletBCBox_Fun(self):
            self.DirichletBCBox = QtGui.QDialog(self)
            width = 350
            height = 120
            centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
            self.DirichletBCBox.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
            self.DirichletBCBox.setWindowTitle("Apply Dirichlet Boundary Condition")
            self.DirichletBCBox.label_dirichlet = QtGui.QLabel("Please enter the displacement constraint values:", self.DirichletBCBox)
            self.DirichletBCBox.label_dirichlet.move(10, 20)

            self.DirichletBCBox.label_x_constraint = QtGui.QLabel("x: ", self.DirichletBCBox)
            self.DirichletBCBox.label_x_constraint.move(10,48)
            self.DirichletBCBox.text_x_constraint = QtGui.QLineEdit(self.DirichletBCBox)
            self.DirichletBCBox.text_x_constraint.setFixedWidth(80)
            self.DirichletBCBox.text_x_constraint.move(30, 45)

            self.DirichletBCBox.label_y_constraint = QtGui.QLabel("y: ", self.DirichletBCBox)
            self.DirichletBCBox.label_y_constraint.move(120,48)
            self.DirichletBCBox.text_y_constraint = QtGui.QLineEdit(self.DirichletBCBox)
            self.DirichletBCBox.text_y_constraint.setFixedWidth(80)
            self.DirichletBCBox.text_y_constraint.move(140, 45)

            self.DirichletBCBox.label_z_constraint = QtGui.QLabel("z: ", self.DirichletBCBox)
            self.DirichletBCBox.label_z_constraint.move(230, 48)
            self.DirichletBCBox.text_z_constraint = QtGui.QLineEdit(self.DirichletBCBox)
            self.DirichletBCBox.text_z_constraint.setFixedWidth(80)
            self.DirichletBCBox.text_z_constraint.move(250, 45)

            okButton_DirichletBCBox = QtGui.QPushButton('OK', self.DirichletBCBox)
            okButton_DirichletBCBox.move(140, 85)
            okButton_DirichletBCBox.clicked.connect(self.okButton_DirichletBCBox)
            okButton_DirichletBCBox.setAutoDefault(True)

    def okButton_DirichletBCBox(self):
            print("Mouse Click " + str(self.dirichlet_count))
            self.dirichlet_count = self.dirichlet_count + 1
            Gui.Selection.clearSelection()
            self.DirichletBCBox.close()


    def onNeumannBC(self):
        self.NeumannDialogBox = QtGui.QDialog(self)
        width = 470
        height = 100
        self.NeumannDialogBox.setGeometry(self.centerPoint.x()-0.5*width, self.centerPoint.y()-0.5*height, width, height)
        self.NeumannDialogBox.setWindowTitle("Apply Neumann Boundary Condition")

        self.NeumannDialogBox.label_Neumann = QtGui.QLabel("Please enter the number faces subject to Neumann BC:", self.NeumannDialogBox)
        self.NeumannDialogBox.label_Neumann.move(10, 30)

        self.NeumannDialogBox.NeumannFaceNumber = QtGui.QLineEdit(self.NeumannDialogBox)
        self.NeumannDialogBox.NeumannFaceNumber.setPlaceholderText("example: 3")
        self.NeumannDialogBox.NeumannFaceNumber.setFixedWidth(80)
        self.NeumannDialogBox.NeumannFaceNumber.move(380, 28)

        okButton_Neumann = QtGui.QPushButton('OK', self.NeumannDialogBox)
        okButton_Neumann.move(0.5*width - 15, 65)
        okButton_Neumann.clicked.connect(self.okButton_Neumann)
        okButton_Neumann.setAutoDefault(True)
        self.NeumannDialogBox.exec_()

    def okButton_Neumann(self):
        self.Neumann_faces = self.NeumannDialogBox.NeumannFaceNumber.text()
        infoBox = QtGui.QMessageBox.information(self.NeumannDialogBox, "Apply Neumann Boundary Conditions", \
                                                "Please select " + self.Neumann_faces + \
                                                " faces subject to Neumann BC one by one!")
        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.NeumannDialogBox.close()
            self.setVisible(False)



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

        
        #bounds without 0.1 offset in total
        # self.lowerbound_x_=mybounds[0]
        # self.lowerbound_y_=mybounds[1]
        # self.lowerbound_z_=mybounds[2]
        # self.upperbound_x_=mybounds[3]
        # self.upperbound_y_=mybounds[4]
        # self.upperbound_z_=mybounds[5]
        

        #  Creating TIBRA directory:
        os.chdir(self.work_dir)

        if os.path.isdir(os.getcwd() + '/TIBRA'):
            self.data_dir = os.getcwd() + '/TIBRA'
            os.chdir(self.data_dir)

            if os.path.isdir(self.data_dir + '/data'):
                self.data_dir = self.data_dir + '/data'
                os.chdir(self.data_dir)
            else:
                os.mkdir('data')
                self.data_dir = self.data_dir + '/data'
                os.chdir(self.data_dir)

        else:
            os.mkdir('TIBRA')
            self.data_dir = os.getcwd() + '/TIBRA'
            os.chdir(self.data_dir)
            os.mkdir('data')
            self.data_dir = self.data_dir + '/data'
            os.chdir(self.data_dir)
       
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
    