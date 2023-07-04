from FreeCAD_PySide import QtGui, QtCore
import os
import FreeCAD
import FreeCADGui as Gui
import Draft, Sketcher, Mesh, Part
import json
from pivy import coin
import numpy as np
from collections import OrderedDict

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
        height = 615
        self.centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(self.centerPoint.x()-0.5*width, self.centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Tibra Parameters")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, on = True)
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)


        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")
        self.json_dir = self.work_dir
        self.ActiveDocument_Name = FreeCAD.ActiveDocument.Name # string

        #Initial Parameters input:

        #main (general) head
        self.label_main_ = QtGui.QLabel("General settings:", self)
        self.label_main_.move(10, 10)
        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        boldUnderlinedFont=QtGui.QFont()
        boldUnderlinedFont.setBold(True)
        boldUnderlinedFont.setUnderline(True)
        blueFont = QtGui.QPalette()
        blueFont.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#005293'))
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #path to the file
        self.label_pathname_ = QtGui.QLabel("Path to the STL file:", self)
        self.label_pathname_.move(10, self.label_main_.y()+30)

        #Text edit of pathname
        self.textInput_pathname_ = QtGui.QLineEdit(self)
        self.textInput_pathname_.setText("")
        self.textInput_pathname_.setFixedWidth(200)
        self.textInput_pathname_.move(10, self.label_pathname_.y()+20)

        #file browser button
        self.fileBrowseButton = QtGui.QPushButton('Browse files',self)
        self.fileBrowseButton.clicked.connect(self.onBrowseButton)
        self.fileBrowseButton.setAutoDefault(False)
        self.fileBrowseButton.move(220, self.textInput_pathname_.y())


        #label text
        self.label_echo_ = QtGui.QLabel("Echo level:", self)
        self.label_echo_.move(10, self.textInput_pathname_.y()+30)
        self.textInput_echo_ = QtGui.QLineEdit(self)
        self.textInput_echo_.setPlaceholderText("1")
        self.textInput_echo_.setFixedWidth(50)
        self.textInput_echo_.move(10, self.label_echo_.y()+20)

        #mesh head
        self.label_main_ = QtGui.QLabel("Mesh settings:", self)
        self.label_main_.move(10, self.textInput_echo_.y()+45)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #polynomial order
        self.label_polynomialOrder_ = QtGui.QLabel("Polynomial order:", self)
        self.label_polynomialOrder_.move(10, self.label_main_.y()+30)
        self.label_polynomialOrder_.setFont(boldFont)

        self.label_polynomialOrder_x_ = QtGui.QLabel("x: ", self)
        self.label_polynomialOrder_x_.move(10, self.label_polynomialOrder_.y()+25)
        self.textInput_polynomialOrder_x_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_x_.setPlaceholderText("1")
        self.textInput_polynomialOrder_x_.setFixedWidth(60)
        self.textInput_polynomialOrder_x_.move(25, self.label_polynomialOrder_.y()+20)

        self.label_polynomialOrder_y_ = QtGui.QLabel("y: ", self)
        self.label_polynomialOrder_y_.move(110, self.label_polynomialOrder_.y()+25)
        self.textInput_polynomialOrder_y_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_y_.setPlaceholderText("2")
        self.textInput_polynomialOrder_y_.setFixedWidth(60)
        self.textInput_polynomialOrder_y_.move(125, self.label_polynomialOrder_.y()+20)

        self.label_polynomialOrder_z_ = QtGui.QLabel("z: ", self)
        self.label_polynomialOrder_z_.move(210, self.label_polynomialOrder_.y()+25)
        self.textInput_polynomialOrder_z_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_z_.setPlaceholderText("3")
        self.textInput_polynomialOrder_z_.setFixedWidth(60)
        self.textInput_polynomialOrder_z_.move(225, self.label_polynomialOrder_.y()+20)

        #number of elements
        self.label_nElements_ = QtGui.QLabel("Number of elements:", self)
        self.label_nElements_.move(10, self.textInput_polynomialOrder_z_.y()+30)
        self.label_nElements_.setFont(boldFont)

        self.label_nElements_x_ = QtGui.QLabel("x: ", self)
        self.label_nElements_x_.move(10, self.label_nElements_.y()+25)
        self.textInput_nElements_x_ = QtGui.QLineEdit(self)
        self.textInput_nElements_x_.setPlaceholderText("10")
        self.textInput_nElements_x_.setFixedWidth(60)
        self.textInput_nElements_x_.move(25, self.label_nElements_.y()+20)

        self.label_nElements_y_ = QtGui.QLabel("y: ", self)
        self.label_nElements_y_.move(110, self.label_nElements_.y()+25)
        self.textInput_nElements_y_ = QtGui.QLineEdit(self)
        self.textInput_nElements_y_.setPlaceholderText("20")
        self.textInput_nElements_y_.setFixedWidth(60)
        self.textInput_nElements_y_.move(125, self.label_nElements_.y()+20)

        self.label_nElements_z_ = QtGui.QLabel("z: ", self)
        self.label_nElements_z_.move(210, self.label_nElements_.y()+25)
        self.textInput_nElements_z_ = QtGui.QLineEdit(self)
        self.textInput_nElements_z_.setPlaceholderText("30")
        self.textInput_nElements_z_.setFixedWidth(60)
        self.textInput_nElements_z_.move(225, self.label_nElements_.y()+20)

        #solution settings head
        self.label_main_ = QtGui.QLabel("Solution Settings:", self)
        self.label_main_.move(10, self.textInput_nElements_z_.y()+45)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #residual setting
        self.label_residual_ = QtGui.QLabel("Moment fitting residual:", self)
        self.label_residual_.move(10, self.label_main_.y()+30)
        self.textInput_residual_ = QtGui.QLineEdit(self)
        self.textInput_residual_.setPlaceholderText("1e-6")
        self.textInput_residual_.setFixedWidth(50)
        self.textInput_residual_.move(10, self.label_residual_.y()+20)

        # min_element_volume ratio
        self.label_min_el_vol_rat = QtGui.QLabel("Minimum element volume ratio:", self)
        self.label_min_el_vol_rat.move(10, self.textInput_residual_.y()+30)
        self.textInput__min_el_vol_rat = QtGui.QLineEdit(self)
        self.textInput__min_el_vol_rat.setPlaceholderText("1e-3")
        self.textInput__min_el_vol_rat.setFixedWidth(50)
        self.textInput__min_el_vol_rat.move(10, self.label_min_el_vol_rat.y()+20)


        #integration method setting
        self.label_integration_ = QtGui.QLabel("Integration method:", self)
        self.label_integration_.move(10, self.textInput__min_el_vol_rat.y()+30)
        self.popup_integration = QtGui.QComboBox(self)
        self.popup_integration_items = ("Gauss","Gauss_Reduced1","Gauss_Reduced2","GGQ_Optimal","GGQ_Reduced1", "GGQ_Reduced2")
        self.popup_integration.addItems(self.popup_integration_items)
        self.popup_integration.setFixedWidth(140)
        self.popup_integration.move(10, self.label_integration_.y()+20)

        #BC settings
        self.label_ApplyBC_ = QtGui.QLabel("Boundary Conditions:", self)
        self.label_ApplyBC_.move(10, self.popup_integration.y()+45)
        self.label_ApplyBC_.setFont(boldUnderlinedFont)
        self.label_ApplyBC_.setPalette(blueFont)

        self.button_Dirichlet_ = QtGui.QPushButton('Apply Dirichlet B.C.',self)
        self.button_Dirichlet_.clicked.connect(self.onDirichletBC)
        self.button_Dirichlet_.setAutoDefault(False)
        self.button_Dirichlet_.setFixedWidth(145)

        self.button_Neumann_ = QtGui.QPushButton('Apply Neumann B.C.',self)
        self.button_Neumann_.clicked.connect(self.onNeumannBC)
        self.button_Neumann_.setAutoDefault(False)
        self.button_Neumann_.setFixedWidth(145)

        self.container_DirichletNeumann = QtGui.QWidget(self)
        self.container_DirichletNeumann.setContentsMargins(0, 0, 0, 0)

        layout_DirichletNeumann = QtGui.QHBoxLayout(self.container_DirichletNeumann)
        layout_DirichletNeumann.setContentsMargins(0, 0, 0, 0)
        layout_DirichletNeumann.addWidget(self.button_Dirichlet_)
        layout_DirichletNeumann.addWidget(self.button_Neumann_)
        layout_DirichletNeumann.setSpacing(10)

        self.container_DirichletNeumann.move(0.5*width - self.button_Dirichlet_.geometry().width() -
                                             0.5*layout_DirichletNeumann.spacing(), self.label_ApplyBC_.y()+25)


        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.setFixedWidth(80)
        # OK button
        saveButton = QtGui.QPushButton('Save', self)
        saveButton.clicked.connect(self.onSave)
        saveButton.setAutoDefault(True)
        saveButton.setFixedWidth(80)

        self.container_saveCancel = QtGui.QWidget(self)
        self.container_saveCancel.setContentsMargins(0, 0, 0, 0)

        layout_saveCancel = QtGui.QHBoxLayout(self.container_saveCancel)
        layout_saveCancel.setContentsMargins(0, 0, 0,0)
        layout_saveCancel.addWidget(saveButton)
        layout_saveCancel.addWidget(cancelButton)
        layout_saveCancel.setSpacing(40)

        self.container_saveCancel.move(0.5*width - saveButton.geometry().width() - 0.5*layout_saveCancel.spacing(),
                                     self.container_DirichletNeumann.y()+50)

        # show the dialog box and creates instances of other required classes
        self.DirichletBCBox_obj = DirichletBCBox()
        self.NeumannBCBox_obj = NeumannBCBox()

        self.DirichletFacesList_Obj = DirichletFacesList()
        self.DirichletFacesList_Obj.Modify_button.clicked.connect(self.ModifyButtonClicked_DirichletFacesList)
        self.DirichletFacesList_Obj.Delete_button.clicked.connect(self.DeleteButtonClicked_DirichletFacesList)
        self.DirichletFacesList_Obj.okButton.clicked.connect(self.okButtonClicked_DirichletFacesList)
        self.DirichletFacesList_Obj.DiscardButton.clicked.connect(self.DiscardButtonClicked_DirichletFacesList)

        self.NeumannFacesList_Obj = NeumannFacesList()
        self.NeumannFacesList_Obj.Modify_button.clicked.connect(self.ModifyButtonClicked_NeumannFacesList)
        self.NeumannFacesList_Obj.Delete_button.clicked.connect(self.DeleteButtonClicked_NeumannFacesList)
        self.NeumannFacesList_Obj.okButton.clicked.connect(self.okButtonClicked_NeumannFacesList)
        self.NeumannFacesList_Obj.DiscardButton.clicked.connect(self.DiscardButtonClicked_NeumannFacesList)

        self.dirichlet_displacement_arr = []
        self.neumann_force_arr = []
        self.DirichletSelectionList = []
        self.NeumannSelectionList = []
        self.show()

    #################################################################################################################################
                            ############################# FUNCTION DEFINITIONS #############################
    #################################################################################################################################

                                                ##### Browse Files Function #####

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
        infoBox = QtGui.QMessageBox.information(self, "Apply Dirichlet Boundary Conditions", \
                                                "Please select faces subject to Dirichlet BC one by one!")

        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_DirichletBCBox)
            self.setVisible(False)
            self.DirichletFacesList_Obj.show()

            ############################ DIRICHLET FACES LIST FUNCTIONS #################################

    def okButtonClicked_DirichletFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.DirichletFacesList_Obj.result = True
        self.DirichletFacesList_Obj.close()

    def DiscardButtonClicked_DirichletFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.DirichletFacesList_Obj.result = False
        self.dirichlet_displacement_arr = []
        self.DirichletFacesList_Obj.close()

    def DeleteButtonClicked_DirichletFacesList(self):
        current_Item = self.DirichletFacesList_Obj.listwidget.currentItem()
        indexToDel = self.DirichletFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        del self.dirichlet_displacement_arr[indexToDel]
        print(str(self.dirichlet_displacement_arr))
        self.DirichletFacesList_Obj.listwidget.takeItem(self.DirichletFacesList_Obj.listwidget.row(current_Item))

    def ModifyButtonClicked_DirichletFacesList(self):
        current_Item = self.DirichletFacesList_Obj.listwidget.currentItem()
        indexToMod = self.DirichletFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        prev_vals = self.dirichlet_displacement_arr[indexToMod]
        prev_x = prev_vals[0]
        prev_y = prev_vals[1]
        prev_z = prev_vals[2]
        self.DirichletBCBox_obj.text_x_constraint.setText(str(prev_x))
        self.DirichletBCBox_obj.text_y_constraint.setText(str(prev_y))
        self.DirichletBCBox_obj.text_z_constraint.setText(str(prev_z))
        self.DirichletBCBox_obj.exec_()

        self.dirichlet_displacement_arr[indexToMod] = \
                                                    [float(self.DirichletBCBox_obj.x_val),\
                                                     float(self.DirichletBCBox_obj.y_val),\
                                                     float(self.DirichletBCBox_obj.z_val)]



                                                ##### Dirichlet Event Button #####

    def getMouseClick_DirichletBCBox(self, event_cb):
        event = event_cb.getEvent()

        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) \
        &  (Gui.Selection.hasSelection() == False) & (event.getState() == coin.SoMouseButtonEvent.DOWN):
            pos = event.getPosition().getValue()
            element_list = Gui.ActiveDocument.ActiveView.getObjectInfo((int(pos[0]), int(pos[1])))
            print(str(element_list))
            if(element_list != None):
                self.DirichletBCBox_obj.element_list = element_list
                self.DirichletBCBox_obj.okButton_Flag = False
                self.DirichletBCBox_obj.exec_()
                if(self.DirichletBCBox_obj.okButton_Flag):
                    self.dirichlet_displacement_arr.append(\
                                                                [float(self.DirichletBCBox_obj.x_val), \
                                                                 float(self.DirichletBCBox_obj.y_val), \
                                                                 float(self.DirichletBCBox_obj.z_val)])
                    print(str(self.dirichlet_displacement_arr))
                    self.DirichletFacesList_Obj.listwidget.addItem(element_list.get('Component'))

                    Gui.Selection.addSelection(element_list.get('Document'), element_list.get('Object'), \
                                               element_list.get('Component'), element_list.get('x'), element_list.get('y'))
                    sel = Gui.Selection.getSelectionEx()
                    # object = Draft.makeFacebinder(sel, 'D' + str(self.DirichletBCBox_obj.dirichlet_count))
                    self.DirichletSelectionList.append(sel)
                    Gui.Selection.clearSelection()
                                        


    def onNeumannBC(self):
        infoBox = QtGui.QMessageBox.information(self, "Apply Neumann Boundary Conditions", \
                                                "Please select faces subject to Neumann BC one by one!")

        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_NeumannBCBox)
            self.setVisible(False)
            self.NeumannFacesList_Obj.show()

            ############################ NEUMANN FACES LIST FUNCTIONS #################################

    def okButtonClicked_NeumannFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.NeumannFacesList_Obj.result = True
        self.NeumannFacesList_Obj.close()

    def DiscardButtonClicked_NeumannFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.NeumannFacesList_Obj.result = False
        self.neumann_force_arr = []
        self.NeumannFacesList_Obj.close()

    def DeleteButtonClicked_NeumannFacesList(self):
        current_Item = self.NeumannFacesList_Obj.listwidget.currentItem()
        indexToDel = self.NeumannFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        del self.neumann_force_arr[indexToDel]
        print(str(self.neumann_force_arr))
        self.NeumannFacesList_Obj.listwidget.takeItem(self.NeumannFacesList_Obj.listwidget.row(current_Item))

    def ModifyButtonClicked_NeumannFacesList(self):
        current_Item = self.NeumannFacesList_Obj.listwidget.currentItem()
        indexToMod = self.NeumannFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        prev_vals = self.neumann_force_arr[indexToMod]
        prev_x = prev_vals[0]
        prev_y = prev_vals[1]
        prev_z = prev_vals[2]
        self.NeumannBCBox_obj.text_x_constraint.setText(str(prev_x))
        self.NeumannBCBox_obj.text_y_constraint.setText(str(prev_y))
        self.NeumannBCBox_obj.text_z_constraint.setText(str(prev_z))
        self.NeumannBCBox_obj.exec_()

        self.neumann_force_arr[indexToMod] = \
                                                    [float(self.NeumannBCBox_obj.x_val),\
                                                     float(self.NeumannBCBox_obj.y_val),\
                                                     float(self.NeumannBCBox_obj.z_val)]
        Gui.Selection.clearSelection()

    def getMouseClick_NeumannBCBox(self, event_cb):
        event = event_cb.getEvent()

        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) \
        &  (Gui.Selection.hasSelection() == False) & (event.getState() == coin.SoMouseButtonEvent.DOWN):
            pos = event.getPosition().getValue()
            element_list = Gui.ActiveDocument.ActiveView.getObjectInfo((int(pos[0]), int(pos[1])))
            print(str(element_list))
            if(element_list != None):
                self.NeumannBCBox_obj.element_list = element_list
                self.NeumannBCBox_obj.okButton_Flag = False
                self.NeumannBCBox_obj.exec_()
                if(self.NeumannBCBox_obj.okButton_Flag):
                    self.neumann_force_arr.append(\
                                                                [float(self.NeumannBCBox_obj.x_val), \
                                                                 float(self.NeumannBCBox_obj.y_val), \
                                                                 float(self.NeumannBCBox_obj.z_val)])
                    print(str(self.neumann_force_arr))
                    self.NeumannFacesList_Obj.listwidget.addItem(element_list.get('Component'))

                    Gui.Selection.addSelection(element_list.get('Document'), element_list.get('Object'), \
                                               element_list.get('Component'), element_list.get('x'), element_list.get('y'))
                    sel = Gui.Selection.getSelectionEx()
                    # object = Draft.makeFacebinder(sel, 'D' + str(self.DirichletBCBox_obj.dirichlet_count))
                    self.NeumannSelectionList.append(sel)
                    Gui.Selection.clearSelection()




    def face2sketch(self, face_list, name):
        try:
            sketch = Draft.makeSketch(face_list, autoconstraints=True, addTo=None, delete=False, name=name,  \
                     radiusPrecision=-1, tol=1e-3)
            return sketch
        except:
            sketch = Draft.makeSketch(face_list, autoconstraints=False, addTo=None, delete=False, name=name,  \
                     radiusPrecision=-1, tol=1e-3)
            return sketch

    def Constraints_Fun(self, sketch) :
        geoList = sketch.Geometry
        Lines = []
        Arcs  = []
        Circles = []
        for i in range(sketch.GeometryCount):
            if geoList[i].TypeId == 'Part::GeomLineSegment':
               Lines.append([i,geoList[i]])
            elif geoList[i].TypeId == 'Part::GeomArcOfCircle':
               Arcs .append([i,geoList[i]])
            elif geoList[i].TypeId == 'Part::GeomCircle':
               Circles.append([i,geoList[i]])
        for i in range(len(Circles)):
            sketch.addConstraint(Sketcher.Constraint('Radius', \
                 Circles[i][0],Circles[i][1].Radius))

    def onSave(self):
        #bounds

        reply = QtGui.QMessageBox.question(self, "Tibra Parameters", "Upon Yes, the TibraParameters.json file and all STL files related to boundary conditions will be saved. If you want to modify Tibra Parameters, you will need to set them up from scratch. \n \n"
                                           "Are you sure you want to continue?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply ==  QtGui.QMessageBox.No:
            pass

        elif reply == QtGui.QMessageBox.Yes:

            mybounds=self.bounds()

            #bounds with 0.1 offset in total

            self.lowerbound_x_=mybounds[0]-(abs(mybounds[0]-mybounds[3]))*0.05
            self.lowerbound_y_=mybounds[1]-(abs(mybounds[1]-mybounds[4]))*0.05
            self.lowerbound_z_=mybounds[2]-(abs(mybounds[2]-mybounds[5]))*0.05
            self.upperbound_x_=mybounds[3]+(abs(mybounds[0]-mybounds[3]))*0.05
            self.upperbound_y_=mybounds[4]+(abs(mybounds[1]-mybounds[4]))*0.05
            self.upperbound_z_=mybounds[5]+(abs(mybounds[2]-mybounds[5]))*0.05


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

            TibraParam = \
            {

                "general_settings"   : {
                    "input_filename"  :  self.textInput_pathname_.text(),
                    "postprocess_filename" : self.data_dir + "/postprocess_STL.stl",
                    "echo_level"      :  int(self.textInput_echo_.text())
                },
                "mesh_settings"     : {
                    "lower_bound": list([self.lowerbound_x_, self.lowerbound_y_, self.lowerbound_z_]),
                    "upper_bound": list([self.upperbound_x_, self.upperbound_y_, self.upperbound_z_]),
                    "polynomial_order" : list([int(self.textInput_polynomialOrder_x_.text()), int(self.textInput_polynomialOrder_y_.text()), int(self.textInput_polynomialOrder_z_.text())]),
                    "number_of_elements" : list([int(self.textInput_nElements_x_.text()),  int(self.textInput_nElements_y_.text()), int(self.textInput_nElements_z_.text())])
                },
                "trimmed_quadrature_rule_settings"     : {
                    "moment_fitting_residual": float(self.textInput_residual_.text()),
                    "min_element_volume_ratio": float(self.textInput__min_el_vol_rat.text())
                },
                "non_trimmed_quadrature_rule_settings" : {
                    "integration_method" : self.popup_integration.currentText()
                },
                "conditions"    :  [
                ]
            }

            print(self.work_dir)

            # Creating TibraParameters.json file and Exporting surface STL files:

            with open('TIBRAParameters.json', 'w') as f:
                json.dump(TibraParam, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass

            for i in range (int(len(self.NeumannSelectionList))):
                out_arr = list(self.neumann_force_arr[i])
                neumann_json = {"neumann": {
                    "filename" : str(self.json_dir) + "N" + str(i+1) + ".stl",
                    "force" : out_arr,
                    }
                }
                self.append_json(neumann_json)

                faceObject_Name = ('N' + str(i+1))
                Draft.makeFacebinder(self.NeumannSelectionList[i], faceObject_Name)
                Neumann_STL_Face_Object = [(FreeCAD.getDocument(self.ActiveDocument_Name).getObject(faceObject_Name))]
                Mesh.export(Neumann_STL_Face_Object, self.work_dir + faceObject_Name + '.stl')

            for i in range (int(len(self.DirichletSelectionList))):
                out_arr = list(self.dirichlet_displacement_arr[i])
                dirichlet_jason = {"dirichlet": {
                    "filename" : str(self.json_dir) + "D" + str(i+1) + ".stl",
                    "displacement" : out_arr,
                    "penalty_factor" : 1e10
                    }
                }
                self.append_json(dirichlet_jason)

                faceObject_Name = ('D' + str(i+1))
                Draft.makeFacebinder(self.DirichletSelectionList[i], faceObject_Name)
                Dirichlet_STL_Face_Object = [(FreeCAD.getDocument(self.ActiveDocument_Name).getObject(faceObject_Name))]
                Mesh.export(Dirichlet_STL_Face_Object, self.work_dir + faceObject_Name + '.stl')


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


            #BOUNDINGBOX&GRID
    
            red   = 1.0  # 1 = 255
            green = 0.0  #
            blue  = 0.0  #
    
            BDvol = FreeCAD.ActiveDocument.addObject("Part::Box","_BoundBoxVolume")
            BDvol.Length.Value = (self.upperbound_x_-self.lowerbound_x_)
            BDvol.Width.Value  = (self.upperbound_y_-self.lowerbound_y_)
            BDvol.Height.Value = (self.upperbound_z_-self.lowerbound_z_)
            BDvol.Placement = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
            BDPl = BDvol.Placement
            oripl_X=BDvol.Placement.Base.x
            oripl_Y=BDvol.Placement.Base.y
            oripl_Z=BDvol.Placement.Base.z
            Gui.ActiveDocument.getObject(BDvol.Name).LineColor  = (red, green, blue)
            Gui.ActiveDocument.getObject(BDvol.Name).PointColor = (red, green, blue)
            Gui.ActiveDocument.getObject(BDvol.Name).ShapeColor = (red, green, blue)
            Gui.ActiveDocument.getObject(BDvol.Name).Transparency = 90
    
            conteneurRectangle = []
            del conteneurRectangle[:]
            conteneurRectangle = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Grid")
    
            if (mybounds[6] and mybounds[7]) > 0.0:
                pl_0 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
                #pl_0 = adjustedGlobalPlacement(objs[0], boundBoxLocation)
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_0,face=False,support=None) #OK
                duble.Label = "_BoundBoxRectangle_Bo"
                Gui.activeDocument().activeObject().LineColor = (1.0, 1.0, blue)
                conteneurRectangle.addObject(duble)
    
                pl_1 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
                #pl_1 =adjustedGlobalPlacement(objs[0], boundBoxLocation + FreeCAD.Vector(0,0,boundBoxLZ))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_1,face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_To"
                Gui.activeDocument().activeObject().LineColor = (1.0, 1.0, blue)
                conteneurRectangle.addObject(duble)
    
                pl_z_first=[]
                pl_z_sec=[]
                stepz=abs(self.upperbound_z_-self.lowerbound_z_)/float(self.textInput_nElements_z_.text())
    
                for i in range(int(self.textInput_nElements_z_.text())-1):
                    #pl_z_first.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,stepz*(i+1)+self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0) ))
                    #duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_z_first[i],face=False,support=None) #Ok
                    #duble.Label = "_BoundBoxRectangle_z_line"+str(i+1)
                    #conteneurRectangle.addObject(duble)
    
                    pl_z_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,stepz*(i+1)+self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_z_sec[i],face=False,support=None) #Ok
                    duble.Label = "_BoundBoxRectangle_z_fill"+str(i+1)
                    Gui.activeDocument().activeObject().LineColor = (1.0 , 1.0, blue)
                    conteneurRectangle.addObject(duble)
    
    
            if (mybounds[6] and mybounds[8]) > 0.0:
                pl_2 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90))
                #pl_2 = pl_0.multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_2,face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_Fr"
                Gui.activeDocument().activeObject().LineColor = (0.0, 1.0, blue)
                conteneurRectangle.addObject(duble)
                pl_3 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.upperbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90))
                #pl_3 = adjustedGlobalPlacement(objs[0], boundBoxLocation+App.Vector(0, boundBoxLY, 0)).multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_3,face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_Re"
                Gui.activeDocument().activeObject().LineColor = (0.0, 1.0, blue)
                conteneurRectangle.addObject(duble)
    
    
                pl_y_first=[]
                pl_y_sec=[]
                stepy=abs(self.upperbound_y_-self.lowerbound_y_)/float(self.textInput_nElements_y_.text())
    
                for i in range(int(self.textInput_nElements_y_.text())-1):
                    #pl_y_first.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                    #duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_y_first[i],face=False,support=None) #Ok
                    #duble.Label = "_BoundBoxRectangle_y_line"+str(i+1)
                    #conteneurRectangle.addObject(duble)
    
                    pl_y_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,stepy*(1+i)+self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_y_sec[i],face=False,support=None) #Ok
                    duble.Label = "_BoundBoxRectangle_y_fill"+str(i+1)
                    Gui.activeDocument().activeObject().LineColor = (0.0 , 1.0, blue)
                    conteneurRectangle.addObject(duble)
    
            if (mybounds[7] and mybounds[8]) > 0.0:
                pl_4 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90))
                #pl_2 = pl_0.multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
                duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_4,face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_Le"
                Gui.activeDocument().activeObject().LineColor = (0.0, 0.0, 1.0)
                conteneurRectangle.addObject(duble)
    
                pl_5= FreeCAD.Placement(FreeCAD.Vector(self.upperbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90))
                #pl_3 = adjustedGlobalPlacement(objs[0], boundBoxLocation+App.Vector(0, boundBoxLY, 0)).multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
                duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_5,face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_Ri"
                Gui.activeDocument().activeObject().LineColor = (0.0, 0.0, 1.0)
                conteneurRectangle.addObject(duble)
    
                pl_x_first=[]
                pl_x_sec=[]
                stepx=abs(self.upperbound_x_-self.lowerbound_x_)/float(self.textInput_nElements_x_.text())
    
                for i in range(int(self.textInput_nElements_x_.text())-1):
                    #pl_y_first.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                    #duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_y_first[i],face=False,support=None) #Ok
                    #duble.Label = "_BoundBoxRectangle_y_line"+str(i+1)
                    #conteneurRectangle.addObject(duble)
    
                    pl_x_sec.append(FreeCAD.Placement(FreeCAD.Vector(stepx*(1+i)+self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_x_sec[i],face=False,support=None) #Ok
                    duble.Label = "_BoundBoxRectangle_x_fill"+str(i+1)
                    Gui.activeDocument().activeObject().LineColor = (0.0 , 0.0, 1.0)
                    conteneurRectangle.addObject(duble)
    
            FreeCAD.ActiveDocument.recompute()
    
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

        boundBoxLX=boundBox_.XLength
        boundBoxLY=boundBox_.YLength
        boundBoxLZ=boundBox_.ZLength

        return [boundBoxXMin, boundBoxYMin, boundBoxZMin, boundBoxXMax, boundBoxYMax, boundBoxZMax, boundBoxLX, boundBoxLY, boundBoxLZ]

    def append_json(self, entry, filename='TIBRAParameters.json'):
            with open(filename, "r") as file:
                data = json.load(file, object_pairs_hook=OrderedDict)
                # Update json object
            data["conditions"].append(entry)
                # Write json file
            with open(filename, "w") as file:
                json.dump(data, file, indent = 4, separators=(", ", ": "), sort_keys=False)

################################## OTHER REQUIRED CLASS DEFINITIONS #############################################

class DirichletBCBox(QtGui.QDialog):
    """"""
    def __init__(self):
        super(DirichletBCBox, self).__init__()
        self.initUI()

    def initUI(self):
            width = 350
            height = 120
            centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
            self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
            self.setWindowTitle("Apply Dirichlet Boundary Condition")
            self.label_dirichlet = QtGui.QLabel("Please enter the displacement constraint values:", self)
            self.label_dirichlet.move(10, 20)
            self.element_list = []
            self.x_val = 0
            self.y_val = 0
            self.z_val = 0

            self.label_x_constraint = QtGui.QLabel("x: ", self)
            self.label_x_constraint.move(10,48)
            self.text_x_constraint = QtGui.QLineEdit(self)
            self.text_x_constraint.setFixedWidth(80)
            self.text_x_constraint.move(30, 45)

            self.label_y_constraint = QtGui.QLabel("y: ", self)
            self.label_y_constraint.move(120,48)
            self.text_y_constraint = QtGui.QLineEdit(self)
            self.text_y_constraint.setFixedWidth(80)
            self.text_y_constraint.move(140, 45)

            self.label_z_constraint = QtGui.QLabel("z: ", self)
            self.label_z_constraint.move(230, 48)
            self.text_z_constraint = QtGui.QLineEdit(self)
            self.text_z_constraint.setFixedWidth(80)
            self.text_z_constraint.move(250, 45)

            okButton_DirichletBCBox = QtGui.QPushButton('OK', self)
            okButton_DirichletBCBox.move(140, 85)
            okButton_DirichletBCBox.clicked.connect(self.okButton_DirichletBCBox)
            okButton_DirichletBCBox.setAutoDefault(True)

            self.dirichlet_count = 0

    def closeEvent(self, event):
        self.resetInputValues()
        event.accept()

    def okButton_DirichletBCBox(self):
        print("Mouse Click " + str(self.dirichlet_count))
        self.dirichlet_count = self.dirichlet_count + 1
        self.x_val = self.text_x_constraint.text()
        self.y_val = self.text_y_constraint.text()
        self.z_val = self.text_z_constraint.text()
        self.resetInputValues()

        self.okButton_Flag = True
        self.close()

    def resetInputValues(self):
        self.text_x_constraint.setText("")
        self.text_y_constraint.setText("")
        self.text_z_constraint.setText("")

class NeumannBCBox(QtGui.QDialog):
    """"""
    def __init__(self):
        super(NeumannBCBox, self).__init__()
        self.initUI()

    def initUI(self):
            width = 350
            height = 120
            centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
            self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
            self.setWindowTitle("Apply Neumann Boundary Condition")
            self.label_neumann = QtGui.QLabel("Please enter the force constraint values:", self)
            self.label_neumann.move(10, 20)
            self.element_list = []
            self.x_val = 0
            self.y_val = 0
            self.z_val = 0


            self.label_x_constraint = QtGui.QLabel("x: ", self)
            self.label_x_constraint.move(10,48)
            self.text_x_constraint = QtGui.QLineEdit(self)
            self.text_x_constraint.setFixedWidth(80)
            self.text_x_constraint.move(30, 45)

            self.label_y_constraint = QtGui.QLabel("y: ", self)
            self.label_y_constraint.move(120,48)
            self.text_y_constraint = QtGui.QLineEdit(self)
            self.text_y_constraint.setFixedWidth(80)
            self.text_y_constraint.move(140, 45)

            self.label_z_constraint = QtGui.QLabel("z: ", self)
            self.label_z_constraint.move(230, 48)
            self.text_z_constraint = QtGui.QLineEdit(self)
            self.text_z_constraint.setFixedWidth(80)
            self.text_z_constraint.move(250, 45)

            okButton_NeumannBCBox = QtGui.QPushButton('OK', self)
            okButton_NeumannBCBox.move(140, 85)
            okButton_NeumannBCBox.clicked.connect(self.okButton_NeumannBCBox)
            okButton_NeumannBCBox.setAutoDefault(True)

            self.neumann_count = 1

    def closeEvent(self, event):
        self.resetInputValues()
        event.accept()

    def okButton_NeumannBCBox(self):
        print("Mouse Click " + str(self.neumann_count))
        self.neumann_count = self.neumann_count + 1
        self.x_val = self.text_x_constraint.text()
        self.y_val = self.text_y_constraint.text()
        self.z_val = self.text_z_constraint.text()
        self.resetInputValues()
        
        self.okButton_Flag = True
        self.close()

    def resetInputValues(self):
        self.text_x_constraint.setText("")
        self.text_y_constraint.setText("")
        self.text_z_constraint.setText("")

class DirichletFacesList(QtGui.QWidget):
    """"""
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("List of Faces")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on = True)
        layout = QtGui.QGridLayout()

        FaceID_label = QtGui.QLabel("Faces Under Dirichlet BC:", self)
        layout.addWidget(FaceID_label, 0, 0, 1, 1)

        layout.setColumnMinimumWidth(1, 10)

        self.Modify_button = QtGui.QPushButton("Modify", self)
        self.Modify_button.setFixedWidth(80)
        layout.addWidget(self.Modify_button, 1, 2, 1, 1)

        layout.setRowMinimumHeight(2, 10)

        self.Delete_button = QtGui.QPushButton("Delete", self)
        self.Delete_button.setFixedWidth(80)
        layout.addWidget(self.Delete_button, 3, 2, 1, 1)

        layout.setRowMinimumHeight(4, 70)

        self.listwidget = QtGui.QListWidget(self)
        layout.addWidget(self.listwidget, 1, 0, 4, 1)

        layout.setRowMinimumHeight(5, 10)

        self.okButton = QtGui.QPushButton('OK', self)
        self.okButton.setAutoDefault(True)
        self.okButton.setFixedWidth(80)

        self.DiscardButton = QtGui.QPushButton('Discard', self)
        self.DiscardButton.setFixedWidth(80)

        layout4OkDiscard = QtGui.QHBoxLayout()
        layout4OkDiscard.addWidget(self.okButton)
        layout4OkDiscard.addWidget(self.DiscardButton)

        layout.addLayout(layout4OkDiscard, 6, 0, 1, -1)

        self.finished_flag = QtGui.QAction("Quit", self)

        self.setLayout(layout)


    def closeEvent(self, event):
        if (self.result):
            event.accept()
        else:
            self.listwidget.clear()
            event.accept()

class NeumannFacesList(QtGui.QWidget):
    """"""
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("List of Faces")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on = True)
        layout = QtGui.QGridLayout()

        FaceID_label = QtGui.QLabel("Faces Under Neumann BC:", self)
        layout.addWidget(FaceID_label, 0, 0, 1, 1)

        layout.setColumnMinimumWidth(1, 10)

        self.Modify_button = QtGui.QPushButton("Modify", self)
        self.Modify_button.setFixedWidth(80)
        layout.addWidget(self.Modify_button, 1, 2, 1, 1)

        layout.setRowMinimumHeight(2, 10)

        self.Delete_button = QtGui.QPushButton("Delete", self)
        self.Delete_button.setFixedWidth(80)
        layout.addWidget(self.Delete_button, 3, 2, 1, 1)

        layout.setRowMinimumHeight(4, 70)

        self.listwidget = QtGui.QListWidget(self)
        layout.addWidget(self.listwidget, 1, 0, 4, 1)

        layout.setRowMinimumHeight(5, 10)

        self.okButton = QtGui.QPushButton('OK', self)
        self.okButton.setAutoDefault(True)
        self.okButton.setFixedWidth(80)

        self.DiscardButton = QtGui.QPushButton('Discard', self)
        self.DiscardButton.setFixedWidth(80)

        layout4OkDiscard = QtGui.QHBoxLayout()
        layout4OkDiscard.addWidget(self.okButton)
        layout4OkDiscard.addWidget(self.DiscardButton)

        layout.addLayout(layout4OkDiscard, 6, 0, 1, -1)

        self.finished_flag = QtGui.QAction("Quit", self)

        self.setLayout(layout)


    def closeEvent(self, event):
        if (self.result):
            event.accept()
        else:
            self.listwidget.clear()
            event.accept()
