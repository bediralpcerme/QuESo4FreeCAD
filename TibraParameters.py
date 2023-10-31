from FreeCAD_PySide import QtGui, QtCore
import os
import FreeCAD
import FreeCADGui as Gui
import Draft, Mesh
import json
from pivy import coin
import numpy as np
from collections import OrderedDict

##################

# The code is not finished yet

##################

#TO DO LIST:
# - Normalization of the force direction
# - Visual improvements and name changes


class TibraParameters(QtGui.QDialog):

    def __init__(self):

        super(TibraParameters, self).__init__()
        self.initUI()
        self.visulizerun=0
        self.gridList=[]     
            

    def initUI(self):

        #position and geometry of the dialog box
        width = 350
        height = 790
        
        self.centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        std_validate = QtGui.QIntValidator()
        scientific_validate = QtGui.QDoubleValidator()
        scientific_validate.setNotation(QtGui.QDoubleValidator.ScientificNotation)
        self.setGeometry(self.centerPoint.x()-0.5*width, self.centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("QuESo Parameters")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, on = True)

        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)


        # self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        # self.work_dir = FreeCAD.ActiveDocument.FileName
        # self.work_dir = self.work_dir.replace(self.docName,"")
        # self.ActiveDocument_Name = FreeCAD.ActiveDocument.Name # string

        # Go back button to project name and directory:

        self.goback_button = QtGui.QPushButton("Go Back", self)
        left_arrow = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_ArrowBack)
        self.goback_button.setIcon(left_arrow)
        self.goback_button.move(10,10)
        self.goback_button.clicked.connect(self.onGoBackButton)
        

        #main (general) head
        self.label_main_ = QtGui.QLabel("General settings:", self)
        self.label_main_.move(10, 40)
        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        boldUnderlinedFont=QtGui.QFont()
        boldUnderlinedFont.setBold(True)
        boldUnderlinedFont.setUnderline(True)
        blueFont = QtGui.QPalette()
        blueFont.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#005293'))
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #path to the QuESo
        self.label_QuESo_ = QtGui.QLabel("Directory of the QuESo:", self)
        self.label_QuESo_.move(10, self.label_main_.y()+30)

        #Text edit of QuESo
        self.textInput_QuESo_ = QtGui.QLineEdit(self)
        self.textInput_QuESo_.setText("")
        self.textInput_QuESo_.setFixedWidth(200)
        self.textInput_QuESo_.move(10, self.label_QuESo_.y()+20)

        #file browser button QuESo
        self.fileBrowseButton_QuESo = QtGui.QPushButton('Browse files',self)
        self.fileBrowseButton_QuESo.clicked.connect(self.onBrowseButton_QuESodirectory)
        self.fileBrowseButton_QuESo.setAutoDefault(False)
        self.fileBrowseButton_QuESo.move(220, self.textInput_QuESo_.y())

        #path to the Kratos
        self.label_Kratos_ = QtGui.QLabel("Directory of the Kratos:", self)
        self.label_Kratos_.move(10, self.textInput_QuESo_.y()+30)

        #Text edit of Kratos
        self.textInput_Kratos_ = QtGui.QLineEdit(self)
        self.textInput_Kratos_.setText("")
        self.textInput_Kratos_.setFixedWidth(200)
        self.textInput_Kratos_.move(10, self.label_Kratos_.y()+20)

        #file browser button Kratos
        self.fileBrowseButton_Kratos = QtGui.QPushButton('Browse files',self)
        self.fileBrowseButton_Kratos.clicked.connect(self.onBrowseButton_Kratosdirectory)
        self.fileBrowseButton_Kratos.setAutoDefault(False)
        self.fileBrowseButton_Kratos.move(220, self.textInput_Kratos_.y())

        #label text
        self.label_echo_ = QtGui.QLabel("Echo level:", self)
        self.label_echo_.move(10, self.textInput_Kratos_.y()+30)
        self.textInput_echo_ = QtGui.QLineEdit(self)
        self.textInput_echo_.setPlaceholderText("1")
        self.textInput_echo_.setFixedWidth(50)
        self.textInput_echo_.setValidator(std_validate)
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
        self.textInput_polynomialOrder_x_.setValidator(std_validate)
        self.textInput_polynomialOrder_x_.move(25, self.label_polynomialOrder_.y()+20)

        self.label_polynomialOrder_y_ = QtGui.QLabel("y: ", self)
        self.label_polynomialOrder_y_.move(110, self.label_polynomialOrder_.y()+25)
        self.textInput_polynomialOrder_y_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_y_.setPlaceholderText("2")
        self.textInput_polynomialOrder_y_.setFixedWidth(60)
        self.textInput_polynomialOrder_y_.setValidator(std_validate)
        self.textInput_polynomialOrder_y_.move(125, self.label_polynomialOrder_.y()+20)

        self.label_polynomialOrder_z_ = QtGui.QLabel("z: ", self)
        self.label_polynomialOrder_z_.move(210, self.label_polynomialOrder_.y()+25)
        self.textInput_polynomialOrder_z_ = QtGui.QLineEdit(self)
        self.textInput_polynomialOrder_z_.setPlaceholderText("3")
        self.textInput_polynomialOrder_z_.setFixedWidth(60)
        self.textInput_polynomialOrder_z_.setValidator(std_validate)
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
        self.textInput_nElements_x_.setValidator(std_validate)
        self.textInput_nElements_x_.move(25, self.label_nElements_.y()+20)

        self.label_nElements_y_ = QtGui.QLabel("y: ", self)
        self.label_nElements_y_.move(110, self.label_nElements_.y()+25)
        self.textInput_nElements_y_ = QtGui.QLineEdit(self)
        self.textInput_nElements_y_.setPlaceholderText("20")
        self.textInput_nElements_y_.setFixedWidth(60)
        self.textInput_nElements_y_.setValidator(std_validate)
        self.textInput_nElements_y_.move(125, self.label_nElements_.y()+20)

        self.label_nElements_z_ = QtGui.QLabel("z: ", self)
        self.label_nElements_z_.move(210, self.label_nElements_.y()+25)
        self.textInput_nElements_z_ = QtGui.QLineEdit(self)
        self.textInput_nElements_z_.setPlaceholderText("30")
        self.textInput_nElements_z_.setFixedWidth(60)
        self.textInput_nElements_z_.setValidator(std_validate)
        self.textInput_nElements_z_.move(225, self.label_nElements_.y()+20)

        # visulize button
        self.visualizeButton = QtGui.QCheckBox('Visualize Grids', self)
        self.visualizeButton.stateChanged.connect(self.onVisualize)

        self.visualizeButton.move(10, self.textInput_nElements_z_.y()+45)

        #solution settings head
        self.label_main_ = QtGui.QLabel("Solution Settings:", self)
        self.label_main_.move(10, self.visualizeButton.y()+45)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #residual setting
        self.label_residual_ = QtGui.QLabel("Moment fitting residual:", self)
        self.label_residual_.move(10, self.label_main_.y()+30)
        self.textInput_residual_ = QtGui.QLineEdit(self)
        self.textInput_residual_.setPlaceholderText("1e-6")
        self.textInput_residual_.setFixedWidth(50)
        self.textInput_residual_.setValidator(scientific_validate)
        self.textInput_residual_.move(10, self.label_residual_.y()+20)

        # min_element_volume ratio
        ### self.label_min_el_vol_rat = QtGui.QLabel("Minimum element volume ratio:", self)
        ### self.label_min_el_vol_rat.move(10, self.textInput_residual_.y()+30)
        ### self.textInput__min_el_vol_rat = QtGui.QLineEdit(self)
        ### self.textInput__min_el_vol_rat.setPlaceholderText("1e-3")
        ### self.textInput__min_el_vol_rat.setFixedWidth(50)
        ### self.textInput__min_el_vol_rat.setValidator(scientific_validate)
        ### self.textInput__min_el_vol_rat.move(10, self.label_min_el_vol_rat.y()+20)


        #integration method setting
        self.label_integration_ = QtGui.QLabel("Integration method:", self)
        self.label_integration_.move(10, self.textInput_residual_.y()+30)
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

        self.button_PenaltySupport_ = QtGui.QPushButton('Apply Penalty Support Condition',self)
        self.button_PenaltySupport_.clicked.connect(self.onPenaltySupportBC)
        self.button_PenaltySupport_.setAutoDefault(False)
        self.button_PenaltySupport_.setFixedWidth(230)

        self.button_SurfaceLoad_ = QtGui.QPushButton('Apply Surface Load Condition',self)
        self.button_SurfaceLoad_.clicked.connect(self.onSurfaceLoadBC)
        self.button_SurfaceLoad_.setAutoDefault(False)
        self.button_SurfaceLoad_.setFixedWidth(230)

        self.container_PenaltySupportSurfaceLoad = QtGui.QWidget(self)
        self.container_PenaltySupportSurfaceLoad.setContentsMargins(0, 0, 0, 0)

        layout_PenaltySupportSurfaceLoad = QtGui.QVBoxLayout(self.container_PenaltySupportSurfaceLoad)
        layout_PenaltySupportSurfaceLoad.setContentsMargins(0, 0, 0, 0)
        layout_PenaltySupportSurfaceLoad.addWidget(self.button_PenaltySupport_)
        layout_PenaltySupportSurfaceLoad.addWidget(self.button_SurfaceLoad_)
        layout_PenaltySupportSurfaceLoad.setSpacing(10)

        self.container_PenaltySupportSurfaceLoad.move(10, self.label_ApplyBC_.y()+25)

        #Solver settings button
        self.label_SolverSettings_ = QtGui.QLabel("Solver Settings:", self)
        self.label_SolverSettings_.move(10, self.container_PenaltySupportSurfaceLoad.y()+80)
        self.label_SolverSettings_.setFont(boldUnderlinedFont)
        self.label_SolverSettings_.setPalette(blueFont)
        

        self.SolverSettingsButton = QtGui.QPushButton('Apply Solver Settings',self)
        self.SolverSettingsButton.clicked.connect(self.onSolverSettingsButton)
        self.SolverSettingsButton.setAutoDefault(False)
        self.SolverSettingsButton.setFixedWidth(155)

        self.container_SolverSettingsButton = QtGui.QWidget(self)
        self.container_SolverSettingsButton.setContentsMargins(0, 0, 0, 0)

        layout_SolverSettingsButton = QtGui.QHBoxLayout(self.container_SolverSettingsButton)
        layout_SolverSettingsButton.setContentsMargins(0, 0, 0, 0)
        layout_SolverSettingsButton.addWidget(self.SolverSettingsButton)

        self.container_SolverSettingsButton.move(10, self.label_SolverSettings_.y()+25)


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
                                     self.container_SolverSettingsButton.y()+60)

        # show the dialog box and creates instances of other required classes
        self.PenaltySupportBCBox_obj = PenaltySupportBCBox()
        self.SurfaceLoadBCBox_obj = SurfaceLoadBCBox()
        self.projectNameWindow_obj = projectNameWindow()
        self.SolverSettingsBox_obj = SolverSettingsBox()

        self.PenaltySupportFacesList_Obj = PenaltySupportFacesList()
        self.PenaltySupportFacesList_Obj.Modify_button.clicked.connect(self.ModifyButtonClicked_PenaltySupportFacesList)
        self.PenaltySupportFacesList_Obj.Delete_button.clicked.connect(self.DeleteButtonClicked_PenaltySupportFacesList)
        self.PenaltySupportFacesList_Obj.okButton.clicked.connect(self.okButtonClicked_PenaltySupportFacesList)
        self.PenaltySupportFacesList_Obj.DiscardButton.clicked.connect(self.DiscardButtonClicked_PenaltySupportFacesList)

        self.SurfaceLoadFacesList_Obj = SurfaceLoadFacesList()
        self.SurfaceLoadFacesList_Obj.Modify_button.clicked.connect(self.ModifyButtonClicked_SurfaceLoadFacesList)
        self.SurfaceLoadFacesList_Obj.Delete_button.clicked.connect(self.DeleteButtonClicked_SurfaceLoadFacesList)
        self.SurfaceLoadFacesList_Obj.okButton.clicked.connect(self.okButtonClicked_SurfaceLoadFacesList)
        self.SurfaceLoadFacesList_Obj.DiscardButton.clicked.connect(self.DiscardButtonClicked_SurfaceLoadFacesList)

        self.PenaltySupport_displacement_arr = []
        self.SurfaceLoad_modulus_arr=[]
        self.SurfaceLoad_force_arr = []
        self.PenaltySupportSelectionList = []
        self.SurfaceLoadSelectionList = []
        
        self.projectNameWindow_obj.exec_()
        self.work_dir = self.projectNameWindow_obj.project_dir
        self.ActiveDocument_Name = FreeCAD.ActiveDocument.Name

        if (self.projectNameWindow_obj.project_Name != "") and (self.projectNameWindow_obj.project_dir != "") and (self.projectNameWindow_obj.okFlag == True):
            self.previousValuesCheck()
            self.show()
        else:
            pass


    #################################################################################################################################
                            ############################# FUNCTION DEFINITIONS #############################
    #################################################################################################################################

                                                ##### Browse Files Function #####

    def previousValuesCheck(self):

        try:
            os.chdir(self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name)
            work_dir = os.getcwd()
            with open('DirectoryInfo.json', 'r') as myfile:
                mydata_directory = json.load(myfile)

            kratos_dirOrg = mydata_directory['kratos_directory']
            QuESo_dirOrg = mydata_directory['QuESo_directory']
            STL_dir = mydata_directory['STL_directory']

                        ## Setting Up QuESo Parameters and changing values on the pop-up screen ##

            with open('QuESoParameters.json', 'r') as myfile:
                mydata_QuESo = json.load(myfile)

            # Reading general_settings:
            general_settings = mydata_QuESo['general_settings']

            echo_level = str(general_settings['echo_level'])

            # Reading mesh settings
            mesh_settings = mydata_QuESo['mesh_settings']

            polynomial_order = mesh_settings['polynomial_order']
            polynomial_order_x = str(polynomial_order[0])
            polynomial_order_y = str(polynomial_order[1])
            polynomial_order_z = str(polynomial_order[2])

            number_of_elements = mesh_settings['number_of_elements']
            number_of_elements_x = str(number_of_elements[0])
            number_of_elements_y = str(number_of_elements[1])
            number_of_elements_z = str(number_of_elements[2])

            # Reading trimmed_quadrature_rule_settings

            trimmed_quadrature_rule_settings = mydata_QuESo['trimmed_quadrature_rule_settings']
            moment_fitting_residual = str(trimmed_quadrature_rule_settings['moment_fitting_residual'])

            # Reading non_trimmed_quadrature_rule_settings

            non_trimmed_quadrature_rule_settings = mydata_QuESo['non_trimmed_quadrature_rule_settings']
            integration_method = str(non_trimmed_quadrature_rule_settings['integration_method'])
            myfile.close()
            #######

            # Maybe, I can also read boudnary conditions ? Let's skip it for now.

            #######

            self.textInput_echo_.setText(echo_level)
            self.textInput_QuESo_.setText(QuESo_dirOrg)
            self.textInput_Kratos_.setText(kratos_dirOrg)
            self.textInput_polynomialOrder_x_.setText(polynomial_order_x)
            self.textInput_polynomialOrder_y_.setText(polynomial_order_y)
            self.textInput_polynomialOrder_z_.setText(polynomial_order_z)
            self.textInput_nElements_x_.setText(number_of_elements_x)
            self.textInput_nElements_y_.setText(number_of_elements_y)
            self.textInput_nElements_z_.setText(number_of_elements_z)
            self.textInput_residual_.setText(moment_fitting_residual)
            self.popup_integration.setCurrentText(integration_method)

                        ## Setting Up Kratos Parameters and changing values on the pop-up screen ##

            with open('KratosParameters.json', 'r') as myfile:
                mydata_Kratos = json.load(myfile)

            # Reading problem data
            problem_data = mydata_Kratos['problem_data']
            
            parallel_type = str(problem_data['parallel_type'])
            echo_level_problemdata = str(problem_data['echo_level'])
            start_time = str(problem_data['start_time'])
            end_time = str(problem_data['end_time'])

            # Reading solver settings
            solver_settings = mydata_Kratos['solver_settings']

            solver_type = str(solver_settings['solver_type'])
            analysis_type = str(solver_settings['analysis_type'])
            model_part_name = str(solver_settings['model_part_name'])
            echo_level_solversettings = str(solver_settings['echo_level'])
            model_import_settings = solver_settings['model_import_settings']

            input_type = str(model_import_settings['input_type'])
            linear_solver_settings = solver_settings['linear_solver_settings']
            preconditioner_type = str(linear_solver_settings['preconditioner_type'])
            solver_type_linearsolversettings = str(linear_solver_settings['solver_type'])
            tolerance = str(linear_solver_settings['tolerance'])
            rotation_dofs = str(solver_settings['rotation_dofs'])
            residual_relative_tolerance = str(solver_settings['residual_relative_tolerance'])
            builder_and_solver_settings = solver_settings['builder_and_solver_settings']
            use_block_builder = str(builder_and_solver_settings['use_block_builder'])


            # Reading modelers
            modelers = mydata_Kratos['modelers']
            modeler_name = str(modelers[0]['modeler_name'])
            parameters_modelers = modelers[0]['Parameters']
            model_part_name_modelers = str(parameters_modelers['model_part_name'])
            geometry_name = str(parameters_modelers['geometry_name'])
            myfile.close()


            self.SolverSettingsBox_obj.textInput_parallel_type_.setText(parallel_type)
            self.SolverSettingsBox_obj.textInput_echo_level2_.setText(echo_level_problemdata)
            self.SolverSettingsBox_obj.textInput_start_time_.setText(start_time)
            self.SolverSettingsBox_obj.textInput_end_time_.setText(end_time)
            self.SolverSettingsBox_obj.textInput_solver_type_.setText(solver_type)
            self.SolverSettingsBox_obj.popup_analysis_type_.setCurrentText(analysis_type)
            self.SolverSettingsBox_obj.textInput_model_part_name_.setText(model_part_name)
            self.SolverSettingsBox_obj.textInput_echo_level3_.setText(echo_level_solversettings)
            self.SolverSettingsBox_obj.textInput_input_type_.setText(input_type)
            self.SolverSettingsBox_obj.textInput_preconditioner_type_.setText(preconditioner_type)
            self.SolverSettingsBox_obj.textInput_solver_type2_.setText(solver_type_linearsolversettings)
            self.SolverSettingsBox_obj.textInput_tolerance_.setText(tolerance)
            self.SolverSettingsBox_obj.popup_rotation_dofs_.setCurrentText(rotation_dofs)
            self.SolverSettingsBox_obj.popup_block_builder_.setCurrentText(use_block_builder)
            self.SolverSettingsBox_obj.textInput_relative_tolerance_.setText(residual_relative_tolerance)
            self.SolverSettingsBox_obj.textInput_modeler_name_.setText(modeler_name)
            self.SolverSettingsBox_obj.textInput_modeler_part_name_.setText(model_part_name_modelers)
            self.SolverSettingsBox_obj.textInput_modeler_geometry_name_.setText(geometry_name)

            ## Setting Up Structural Materials Parameters and changing values on the pop-up screen ##

            with open('StructuralMaterials.json', 'r') as myfile:
                mydata_StMat = json.load(myfile)

            # Reading properties
            properties = mydata_StMat['properties']

            model_part_name_stm = str(properties[0]['model_part_name'])
            properties_id = str(properties[0]['properties_id'])
            Material = properties[0]['Material']
            consitutive_law = Material['constitutive_law']
            name_constLaw = str(consitutive_law['name'])
            Variables = Material['Variables']
            density = str(Variables['DENSITY'])
            young_modulus = str(Variables['YOUNG_MODULUS'])
            poisson_ratio = str(Variables['POISSON_RATIO'])
            myfile.close()

            self.SolverSettingsBox_obj.textInput_modeler_part_name_.setText(model_part_name_stm)
            self.SolverSettingsBox_obj.textInput_properties_id_.setText(properties_id)
            self.SolverSettingsBox_obj.textInput_constitutive_id_.setText(name_constLaw)
            self.SolverSettingsBox_obj.textInput_density_.setText(density)
            self.SolverSettingsBox_obj.textInput_young_modulus_.setText(young_modulus)
            self.SolverSettingsBox_obj.textInput_poisson_ratio_.setText(poisson_ratio)

        except:
            pass


    def onGoBackButton(self):

        self.projectNameWindow_obj.textInput_dir.setText(self.projectNameWindow_obj.project_dir)
        self.projectNameWindow_obj.textInput_name.setText(self.projectNameWindow_obj.project_Name)
        self.hide()
        self.projectNameWindow_obj.exec_()

        self.work_dir = self.projectNameWindow_obj.project_dir
        self.ActiveDocument_Name = FreeCAD.ActiveDocument.Name

        if (self.projectNameWindow_obj.project_Name != "") and (self.projectNameWindow_obj.project_dir != "") and (self.projectNameWindow_obj.okFlag == True):
            self.show()
        else:
            pass


    def onBrowseButton_QuESodirectory(self):
        self.QuESo_directory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.work_dir, QtGui.QFileDialog.ShowDirsOnly)
        self.textInput_QuESo_.setText(self.QuESo_directory)
        self.QuESo_lib_directory = self.QuESo_directory + '/libs'
    
    def onBrowseButton_Kratosdirectory(self):
        self.Kratos_directory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.work_dir, QtGui.QFileDialog.ShowDirsOnly)
        self.textInput_Kratos_.setText(self.Kratos_directory)
        self.Kratos_directory = self.Kratos_directory + '/bin/Release'
        self.Kratos_lib_directory = self.Kratos_directory + '/libs'


    def onPenaltySupportBC(self):
        infoBox = QtGui.QMessageBox.information(self, "Apply PenaltySupport Boundary Conditions", \
                                                "Please select faces subject to PenaltySupport BC one by one!")

        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_PenaltySupportBCBox)
            self.setVisible(False)
            self.PenaltySupportFacesList_Obj.show()

            ############################ PenaltySupport FACES LIST FUNCTIONS #################################

    def okButtonClicked_PenaltySupportFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.PenaltySupportFacesList_Obj.result = True
        self.PenaltySupportFacesList_Obj.close()

    def DiscardButtonClicked_PenaltySupportFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.PenaltySupportFacesList_Obj.result = False
        self.PenaltySupport_displacement_arr = []
        self.PenaltySupportFacesList_Obj.close()

    def DeleteButtonClicked_PenaltySupportFacesList(self):
        current_Item = self.PenaltySupportFacesList_Obj.listwidget.currentItem()
        indexToDel = self.PenaltySupportFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        del self.PenaltySupport_displacement_arr[indexToDel]
        print(str(self.PenaltySupport_displacement_arr))
        self.PenaltySupportFacesList_Obj.listwidget.takeItem(self.PenaltySupportFacesList_Obj.listwidget.row(current_Item))

    def ModifyButtonClicked_PenaltySupportFacesList(self):
        current_Item = self.PenaltySupportFacesList_Obj.listwidget.currentItem()
        indexToMod = self.PenaltySupportFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        prev_vals = self.PenaltySupport_displacement_arr[indexToMod]
        prev_x = prev_vals[0]
        prev_y = prev_vals[1]
        prev_z = prev_vals[2]
        self.PenaltySupportBCBox_obj.text_x_constraint.setText(str(prev_x))
        self.PenaltySupportBCBox_obj.text_y_constraint.setText(str(prev_y))
        self.PenaltySupportBCBox_obj.text_z_constraint.setText(str(prev_z))
        self.PenaltySupportBCBox_obj.exec_()

        self.PenaltySupport_displacement_arr[indexToMod] = \
                                                    [float(self.PenaltySupportBCBox_obj.x_val),\
                                                     float(self.PenaltySupportBCBox_obj.y_val),\
                                                     float(self.PenaltySupportBCBox_obj.z_val)]



                                                ##### PenaltySupport Event Button #####

    def getMouseClick_PenaltySupportBCBox(self, event_cb):
        event = event_cb.getEvent()

        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) \
        &  (Gui.Selection.hasSelection() == False) & (event.getState() == coin.SoMouseButtonEvent.DOWN):
            pos = event.getPosition().getValue()
            element_list = Gui.ActiveDocument.ActiveView.getObjectInfo((int(pos[0]), int(pos[1])))
            print(str(element_list))
            if(element_list != None):
                self.PenaltySupportBCBox_obj.element_list = element_list
                self.PenaltySupportBCBox_obj.okButton_Flag = False
                self.PenaltySupportBCBox_obj.exec_()
                if(self.PenaltySupportBCBox_obj.okButton_Flag):
                    self.PenaltySupport_displacement_arr.append(\
                                                                [float(self.PenaltySupportBCBox_obj.x_val), \
                                                                 float(self.PenaltySupportBCBox_obj.y_val), \
                                                                 float(self.PenaltySupportBCBox_obj.z_val)])
                    print(str(self.PenaltySupport_displacement_arr))
                    self.PenaltySupportFacesList_Obj.listwidget.addItem(element_list.get('Component'))

                    Gui.Selection.addSelection(element_list.get('Document'), element_list.get('Object'), \
                                               element_list.get('Component'), element_list.get('x'), element_list.get('y'))
                    sel = Gui.Selection.getSelectionEx()
                    # object = Draft.makeFacebinder(sel, 'D' + str(self.PenaltySupportBCBox_obj.PenaltySupport_count))
                    self.PenaltySupportSelectionList.append(sel)
                    Gui.Selection.clearSelection()
                                        


    def onSolverSettingsButton(self):

        self.SolverSettingsBox_obj.exec_()


    def onSurfaceLoadBC(self):
        infoBox = QtGui.QMessageBox.information(self, "Apply SurfaceLoad Boundary Conditions", \
                                                "Please select faces subject to SurfaceLoad BC one by one!")

        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_SurfaceLoadBCBox)
            self.setVisible(False)
            self.SurfaceLoadFacesList_Obj.show()

            ############################ SurfaceLoad FACES LIST FUNCTIONS #################################

    def okButtonClicked_SurfaceLoadFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.SurfaceLoadFacesList_Obj.result = True
        self.SurfaceLoadFacesList_Obj.close()

    def DiscardButtonClicked_SurfaceLoadFacesList(self):
        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.SurfaceLoadFacesList_Obj.result = False
        self.SurfaceLoad_force_arr = []
        self.SurfaceLoad_modulus_arr=[]
        self.SurfaceLoadFacesList_Obj.close()

    def DeleteButtonClicked_SurfaceLoadFacesList(self):
        current_Item = self.SurfaceLoadFacesList_Obj.listwidget.currentItem()
        indexToDel = self.SurfaceLoadFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        del self.SurfaceLoad_force_arr[indexToDel]
        print(str(self.SurfaceLoad_force_arr))
        self.SurfaceLoadFacesList_Obj.listwidget.takeItem(self.SurfaceLoadFacesList_Obj.listwidget.row(current_Item))

    def ModifyButtonClicked_SurfaceLoadFacesList(self):
        current_Item = self.SurfaceLoadFacesList_Obj.listwidget.currentItem()
        indexToMod = self.SurfaceLoadFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        prev_vals_direction = self.SurfaceLoad_force_arr[indexToMod]
        prev_vals_modulus = self.SurfaceLoad_modulus_arr[indexToMod]
        prev_x = prev_vals_direction[0]
        prev_y = prev_vals_direction[1]
        prev_z = prev_vals_direction[2]
        self.SurfaceLoadBCBox_obj.text_x_constraint.setText(str(prev_x))
        self.SurfaceLoadBCBox_obj.text_y_constraint.setText(str(prev_y))
        self.SurfaceLoadBCBox_obj.text_z_constraint.setText(str(prev_z))
        self.SurfaceLoadBCBox_obj.text_SurfaceLoad_modulus.setText(str(prev_vals_modulus))
        self.SurfaceLoadBCBox_obj.exec_()

        self.SurfaceLoad_force_arr[indexToMod] = \
                                                    [float(self.SurfaceLoadBCBox_obj.x_val),\
                                                     float(self.SurfaceLoadBCBox_obj.y_val),\
                                                     float(self.SurfaceLoadBCBox_obj.z_val)]
        self.SurfaceLoad_modulus_arr = float(self.SurfaceLoadBCBox_obj.modulus_val)
        print(str(self.SurfaceLoad_force_arr))
        Gui.Selection.clearSelection()

    def getMouseClick_SurfaceLoadBCBox(self, event_cb):
        event = event_cb.getEvent()

        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) \
        &  (Gui.Selection.hasSelection() == False) & (event.getState() == coin.SoMouseButtonEvent.DOWN):
            pos = event.getPosition().getValue()
            element_list = Gui.ActiveDocument.ActiveView.getObjectInfo((int(pos[0]), int(pos[1])))
            print(str(element_list))
            if(element_list != None):
                self.SurfaceLoadBCBox_obj.element_list = element_list
                self.SurfaceLoadBCBox_obj.okButton_Flag = False
                self.SurfaceLoadBCBox_obj.exec_()
                if(self.SurfaceLoadBCBox_obj.okButton_Flag):
                    self.SurfaceLoad_force_arr.append(\
                                                                [float(self.SurfaceLoadBCBox_obj.x_val), \
                                                                 float(self.SurfaceLoadBCBox_obj.y_val), \
                                                                 float(self.SurfaceLoadBCBox_obj.z_val)])
                    self.SurfaceLoad_modulus_arr.append(\
                                                                float(self.SurfaceLoadBCBox_obj.modulus_val))
                    print(str(self.SurfaceLoad_force_arr))
                    self.SurfaceLoadFacesList_Obj.listwidget.addItem(element_list.get('Component'))

                    Gui.Selection.addSelection(element_list.get('Document'), element_list.get('Object'), \
                                               element_list.get('Component'), element_list.get('x'), element_list.get('y'))
                    sel = Gui.Selection.getSelectionEx()
                    # object = Draft.makeFacebinder(sel, 'D' + str(self.PenaltySupportBCBox_obj.PenaltySupport_count))
                    self.SurfaceLoadSelectionList.append(sel)
                    Gui.Selection.clearSelection()

    def onVisualize(self):
            
            if (self.visualizeButton.isChecked()):
                self.VisualizeGrid_Fun()
            else:
                self.deVisualizeGrid_Fun()


    def onSave(self):
        #bounds

        reply = QtGui.QMessageBox.question(self, "QuESo Parameters", "Upon Yes, all files related to the project will be saved. \n \n"
                                           "Are you sure you want to continue?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply ==  QtGui.QMessageBox.No:
            pass

        elif reply == QtGui.QMessageBox.Yes:

            #  Creating Project and data directories (changing to project directory):
            os.chdir(self.work_dir)

            if os.path.isdir(os.getcwd() + "/" + self.projectNameWindow_obj.project_Name):
                self.work_dir = os.getcwd() + "/" + self.projectNameWindow_obj.project_Name
                os.chdir(self.work_dir)

                if os.path.isdir(os.getcwd() + "/data"):
                    self.data_dir = os.getcwd() + "/data"

                else:
                    os.mkdir(os.getcwd() + "/data")
                    self.data_dir = os.getcwd() + "/data"
            
            else:
                os.mkdir(os.getcwd() + "/" + self.projectNameWindow_obj.project_Name)
                self.work_dir = os.getcwd() + "/" + self.projectNameWindow_obj.project_Name
                os.chdir(self.work_dir)
                os.mkdir(os.getcwd() + "/data")
                self.data_dir = os.getcwd() + "/data"

            temp_name = FreeCAD.ActiveDocument.Name
            FreeCAD.getDocument(temp_name).saveAs(self.work_dir + "/" + self.projectNameWindow_obj.project_Name + ".FCStd")

            self.STL_directory = self.data_dir + "/" + self.projectNameWindow_obj.project_Name + ".stl"
            object = []
            object.append(FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.Objects[0].Name))
            Mesh.export(object, self.STL_directory)

            mybounds=self.bounds()

            #bounds with 0.1 offset in total

            self.lowerbound_x_=mybounds[0]-(abs(mybounds[0]-mybounds[3]))*0.05
            self.lowerbound_y_=mybounds[1]-(abs(mybounds[1]-mybounds[4]))*0.05
            self.lowerbound_z_=mybounds[2]-(abs(mybounds[2]-mybounds[5]))*0.05
            self.upperbound_x_=mybounds[3]+(abs(mybounds[0]-mybounds[3]))*0.05
            self.upperbound_y_=mybounds[4]+(abs(mybounds[1]-mybounds[4]))*0.05
            self.upperbound_z_=mybounds[5]+(abs(mybounds[2]-mybounds[5]))*0.05


            QuESoParam = \
            {

                "general_settings"   : {
                    "input_filename"  :  self.STL_directory,
                    "echo_level"      :  int(self.textInput_echo_.text())
                },
                "mesh_settings"     : {
                    "lower_bound_xyz": list([self.lowerbound_x_, self.lowerbound_y_, self.lowerbound_z_]),
                    "upper_bound_xyz": list([self.upperbound_x_, self.upperbound_y_, self.upperbound_z_]),
                    "lower_bound_uvw": list([self.lowerbound_x_, self.lowerbound_y_, self.lowerbound_z_]),
                    "upper_bound_uvw": list([self.upperbound_x_, self.upperbound_y_, self.upperbound_z_]),
                    "polynomial_order" : list([int(self.textInput_polynomialOrder_x_.text()), int(self.textInput_polynomialOrder_y_.text()), int(self.textInput_polynomialOrder_z_.text())]),
                    "number_of_elements" : list([int(self.textInput_nElements_x_.text()),  int(self.textInput_nElements_y_.text()), int(self.textInput_nElements_z_.text())])
                },
                "trimmed_quadrature_rule_settings"     : {
                    "moment_fitting_residual": float(self.textInput_residual_.text())
                },
                "non_trimmed_quadrature_rule_settings" : {
                    "integration_method" : self.popup_integration.currentText()
                },
                "conditions"    :  [
                ]
            }

            self.DirectoryInfo = \
            {
                "working_directory"     : self.work_dir,
                "STL_directory"         : self.STL_directory,
                "QuESo_directory"       : self.textInput_QuESo_.text(),
                "QuESo_lib_directory"   : self.textInput_QuESo_.text() + "/libs",
                "kratos_directory"      : self.textInput_Kratos_.text() + '/bin/Release',
                "kratos_lib_directory"  : self.textInput_Kratos_.text() + '/bin/Release/libs'
            }


            # Creating QuESoParameters.json file and Exporting surface STL files:

            with open('QuESoParameters.json', 'w') as f:
                json.dump(QuESoParam, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass

            for i in range (int(len(self.SurfaceLoad_force_arr))):
                force_direction = list(self.SurfaceLoad_force_arr[i])
                magnitude = self.SurfaceLoad_modulus_arr[i]
                SurfaceLoad_json = {"SurfaceLoadCondition": {
                    "input_filename" : str(self.data_dir) + "/" + "N" + str(i+1) + ".stl",
                    "modulus"        : magnitude,
                    "direction"      : force_direction,
                    }
                }
                self.append_json(SurfaceLoad_json)

                faceObject_Name = ('N' + str(i+1))
                Draft.makeFacebinder(self.SurfaceLoadSelectionList[i], faceObject_Name)
                SurfaceLoad_STL_Face_Object = [(FreeCAD.getDocument(self.ActiveDocument_Name).getObject(faceObject_Name))]
                Mesh.export(SurfaceLoad_STL_Face_Object, self.data_dir + "/" + faceObject_Name + '.stl')

            for i in range (int(len(self.PenaltySupport_displacement_arr))):
                out_arr = list(self.PenaltySupport_displacement_arr[i])
                PenaltySupport_jason = {"PenaltySupportCondition": {
                    "input_filename" : str(self.data_dir)+ "/" + "D" + str(i+1) + ".stl",
                    "value"          : out_arr,
                    "penalty_factor" : 1e10
                    }
                }
                self.append_json(PenaltySupport_jason)

                faceObject_Name = ('D' + str(i+1))
                Draft.makeFacebinder(self.PenaltySupportSelectionList[i], faceObject_Name)
                PenaltySupport_STL_Face_Object = [(FreeCAD.getDocument(self.ActiveDocument_Name).getObject(faceObject_Name))]
                Mesh.export(PenaltySupport_STL_Face_Object, self.data_dir + "/" + faceObject_Name + '.stl')

            # Creating KratosParameters.json file:
            with open('KratosParameters.json', 'w') as f:
                json.dump(self.SolverSettingsBox_obj.KratosParam, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass
            
            # Creating StructuralMaterials.json file:
            with open('StructuralMaterials.json', 'w') as f:
                json.dump(self.SolverSettingsBox_obj.StructuralMat, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass

            # Creating DirectoryInfo.json file:
            with open('DirectoryInfo.json', 'w') as f:
                json.dump(self.DirectoryInfo, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass

            QuESo_main_script = \
            '''from QuESo_PythonApplication.PyQuESo import PyQuESo

def main():
    pyqueso = PyQuESo("{QuESo_param_json}")
    pyqueso.Run()

if __name__ == "__main__":
    main()'''.format(QuESo_param_json="QuESoParameters.json")

            # Creating QuESo_main.py file:
            with open('QuESo_main.py', 'w') as f:
                f.write(QuESo_main_script)
                pass


            #BOUNDINGBOX&GRID

            if self.visulizerun>0:
                FreeCAD.activeDocument().removeObject('Grid')
                #FreeCAD.activeDocument().removeObject('_BoundBoxVolume')
                for i in self.gridList:
                    FreeCAD.activeDocument().removeObject(i)
                self.gridList=[]
            BDvol = FreeCAD.ActiveDocument.addObject("Part::Box","_BoundBoxVolume")
            conteneurRectangle = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Grid")

            Gui.ActiveDocument.getObject(BDvol.Name).Transparency = 100
            BDvol.Length.Value = (self.upperbound_x_-self.lowerbound_x_)
            BDvol.Width.Value  = (self.upperbound_y_-self.lowerbound_y_)
            BDvol.Height.Value = (self.upperbound_z_-self.lowerbound_z_)
            BDvol.Placement = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
            BDPl = BDvol.Placement
            oripl_X=BDvol.Placement.Base.x
            oripl_Y=BDvol.Placement.Base.y
            oripl_Z=BDvol.Placement.Base.z


            if (mybounds[6] and mybounds[7]) > 0.0:
                pl_z_first=[]
                pl_z_sec=[]
                stepz=abs(self.upperbound_z_-self.lowerbound_z_)/float(self.textInput_nElements_z_.text())
                
                for i in range(int(self.textInput_nElements_z_.text())+1):
    
                    pl_z_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,stepz*(i)+self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_z_sec[i],face=False,support=None) #Ok
                    self.gridList.append(duble.Name)
                    duble.Label = "_BoundBoxRectangle_z_fill"+str(i)
                    Gui.activeDocument().activeObject().LineColor = (1.0 , 1.0, 0.0)
                    conteneurRectangle.addObject(duble)
    
    
            if (mybounds[6] and mybounds[8]) > 0.0:
                pl_y_first=[]
                pl_y_sec=[]
                stepy=abs(self.upperbound_y_-self.lowerbound_y_)/float(self.textInput_nElements_y_.text())
    
                for i in range(int(self.textInput_nElements_y_.text())+1):
    
                    pl_y_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,stepy*(i)+self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_y_sec[i],face=False,support=None) #Ok
                    duble.Label = "_BoundBoxRectangle_y_fill"+str(i)
                    self.gridList.append(duble.Name)
                    Gui.activeDocument().activeObject().LineColor = (0.0 , 1.0, 0.0)
                    conteneurRectangle.addObject(duble)
    
            if (mybounds[7] and mybounds[8]) > 0.0:
                pl_x_first=[]
                pl_x_sec=[]
                stepx=abs(self.upperbound_x_-self.lowerbound_x_)/float(self.textInput_nElements_x_.text())
    
                for i in range(int(self.textInput_nElements_x_.text())+1):
    
                    pl_x_sec.append(FreeCAD.Placement(FreeCAD.Vector(stepx*(i)+self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_x_sec[i],face=False,support=None) #Ok
                    duble.Label = "_BoundBoxRectangle_x_fill"+str(i)
                    self.gridList.append(duble.Name)
                    Gui.activeDocument().activeObject().LineColor = (0.0 , 0.0, 1.0)
                    conteneurRectangle.addObject(duble)
    
            FreeCAD.ActiveDocument.recompute()
            FreeCAD.activeDocument().removeObject('_BoundBoxVolume')
            self.result = "Ok"
            os.chdir(self.work_dir)
            self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()


    def bounds(self):
        try:
            mesh = Mesh.Mesh(self.STL_directory)

        except:
            object = []
            object.append(FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.Objects[0].Name))
            STL_temp_directory = self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name + "_temp.stl"
            Mesh.export(object, STL_temp_directory)
            mesh = Mesh.Mesh(STL_temp_directory)

        # boundBox
        boundBox_    = mesh.BoundBox

        try:
            os.remove(STL_temp_directory)
        except:
            pass

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
    
    def VisualizeGrid_Fun(self):

        mybounds=self.bounds()
        self.visulizerun=self.visulizerun+1

        #bounds with 0.1 offset in total
        self.lowerbound_x_=mybounds[0]-(abs(mybounds[0]-mybounds[3]))*0.05
        self.lowerbound_y_=mybounds[1]-(abs(mybounds[1]-mybounds[4]))*0.05
        self.lowerbound_z_=mybounds[2]-(abs(mybounds[2]-mybounds[5]))*0.05
        self.upperbound_x_=mybounds[3]+(abs(mybounds[0]-mybounds[3]))*0.05
        self.upperbound_y_=mybounds[4]+(abs(mybounds[1]-mybounds[4]))*0.05
        self.upperbound_z_=mybounds[5]+(abs(mybounds[2]-mybounds[5]))*0.05
        #BOUNDINGBOX&GRID
        #if vizualize run for the first time
        '''
        if self.visulizerun>1:
            FreeCAD.activeDocument().removeObject('Grid')
            for i in self.gridList:
                FreeCAD.activeDocument().removeObject(i)
            self.gridList=[]
        '''
        BDvol = FreeCAD.ActiveDocument.addObject("Part::Box","_BoundBoxVolume")
        conteneurRectangle = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Grid")
            
        
        BDvol.Length.Value = (self.upperbound_x_-self.lowerbound_x_)
        BDvol.Width.Value  = (self.upperbound_y_-self.lowerbound_y_)
        BDvol.Height.Value = (self.upperbound_z_-self.lowerbound_z_)
        BDvol.Placement = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
        BDPl = BDvol.Placement
        oripl_X=BDvol.Placement.Base.x
        oripl_Y=BDvol.Placement.Base.y
        oripl_Z=BDvol.Placement.Base.z
        Gui.ActiveDocument.getObject(BDvol.Name).Transparency = 100
        

        if (mybounds[6] and mybounds[7]) > 0.0:
            pl_z_first=[]
            pl_z_sec=[]
            stepz=abs(self.upperbound_z_-self.lowerbound_z_)/float(self.textInput_nElements_z_.text())
            
            for i in range(int(self.textInput_nElements_z_.text())+1):

                pl_z_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,stepz*(i)+self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0) ))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_z_sec[i],face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_z_fill"+str(i)
                self.gridList.append(duble.Name)
                Gui.activeDocument().activeObject().LineColor = (1.0 , 1.0, 0.0)
                conteneurRectangle.addObject(duble)


        if (mybounds[6] and mybounds[8]) > 0.0:
            pl_y_first=[]
            pl_y_sec=[]
            stepy=abs(self.upperbound_y_-self.lowerbound_y_)/float(self.textInput_nElements_y_.text())

            for i in range(int(self.textInput_nElements_y_.text())+1):

                pl_y_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,stepy*(i)+self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_y_sec[i],face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_y_fill"+str(i)
                self.gridList.append(duble.Name)
                Gui.activeDocument().activeObject().LineColor = (0.0 , 1.0, 0.0)
                conteneurRectangle.addObject(duble)

        if (mybounds[7] and mybounds[8]) > 0.0:
            pl_x_first=[]
            pl_x_sec=[]
            stepx=abs(self.upperbound_x_-self.lowerbound_x_)/float(self.textInput_nElements_x_.text())

            for i in range(int(self.textInput_nElements_x_.text())+1):

                pl_x_sec.append(FreeCAD.Placement(FreeCAD.Vector(stepx*(i)+self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90) ))
                duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_x_sec[i],face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_x_fill"+str(i)
                self.gridList.append(duble.Name)
                Gui.activeDocument().activeObject().LineColor = (0.0 , 0.0, 1.0)
                conteneurRectangle.addObject(duble)

        FreeCAD.ActiveDocument.recompute()
        FreeCAD.activeDocument().removeObject('_BoundBoxVolume')

    def deVisualizeGrid_Fun(self):

        ######### INSERT YOUR CODE HERE #########

        if self.visulizerun>0:
            FreeCAD.activeDocument().removeObject('Grid')
            for i in self.gridList:
                FreeCAD.activeDocument().removeObject(i)
            self.gridList=[]
            self.visulizerun = 0
            


    def append_json(self, entry, filename='QuESoParameters.json'):
            with open(filename, "r") as file:
                data = json.load(file, object_pairs_hook=OrderedDict)
                # Update json object
            data["conditions"].append(entry)
                # Write json file
            with open(filename, "w") as file:
                json.dump(data, file, indent = 4, separators=(", ", ": "), sort_keys=False)

            

################################## OTHER REQUIRED CLASS DEFINITIONS #############################################

class projectNameWindow(QtGui.QDialog):

    def __init__(self):
        super(projectNameWindow, self).__init__()
        self.initUI()
        self.project_Name = ""
        self.project_dir = ""
        self.okFlag = False

    def initUI(self):
        width = 340
        height = 210
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Project Name")
        self.label_name1 = QtGui.QLabel("Please give your project a name (or the name", self)
        self.label_name1.move(10, 10)
        self.label_name2 = QtGui.QLabel("of the existing project):", self)
        self.label_name2.move(10, self.label_name1.y()+20)
        self.textInput_name = QtGui.QLineEdit(self)
        self.textInput_name.setPlaceholderText("e.g: Cantilever, Knuckle ... ")
        self.textInput_name.setFixedWidth(210)
        self.textInput_name.move(10, self.label_name2.y()+25)

        self.label_dir1 = QtGui.QLabel("Please give the directory where the project will", self)
        self.label_dir1.move(10, self.textInput_name.y()+40)
        self.label_dir2 = QtGui.QLabel("be saved (or the path to the existing project):", self)
        self.label_dir2.move(10, self.label_dir1.y()+20)

        self.textInput_dir = QtGui.QLineEdit(self)
        self.textInput_dir.setFixedWidth(210)
        self.textInput_dir.move(10, self.label_dir2.y()+25)

        browseButton = QtGui.QPushButton('Browse Files', self)
        browseButton.move(230, self.textInput_dir.y())
        browseButton.clicked.connect(self.onBrowseButton)

        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancelButton)
        cancelButton.setFixedWidth(80)
       
        # OK button
        okButton = QtGui.QPushButton('Next', self)
        okButton.clicked.connect(self.onOkButton)
        okButton.setAutoDefault(True)
        okButton.setFixedWidth(80)

        self.container_okCancel = QtGui.QWidget(self)
        self.container_okCancel.setContentsMargins(0, 0, 0, 0)

        layout_okCancel = QtGui.QHBoxLayout(self.container_okCancel)
        layout_okCancel.setContentsMargins(0, 0, 0,0)
        layout_okCancel.addWidget(okButton)
        layout_okCancel.addWidget(cancelButton)
        layout_okCancel.setSpacing(40)
        

        self.container_okCancel.move(0.5*width - okButton.geometry().width() - 0.5*layout_okCancel.spacing(),
                                     height-35)

    def onOkButton(self):
        self.okFlag = True
        self.project_Name = self.textInput_name.text()
        self.project_dir = self.textInput_dir.text()
        self.close()
    
    def onCancelButton(self):
        self.okFlag = False
        self.setResult(0)
        self.close()

    def onBrowseButton(self):
        project_dir = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory",os.getcwd(), QtGui.QFileDialog.ShowDirsOnly)
        self.textInput_dir.setText(project_dir)


class PenaltySupportBCBox(QtGui.QDialog):
    """"""
    def __init__(self):
        super(PenaltySupportBCBox, self).__init__()
        self.initUI()

    def initUI(self):
            width = 350
            height = 120
            std_validate = QtGui.QDoubleValidator()
            std_validate.setNotation(QtGui.QDoubleValidator.StandardNotation)
            centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
            self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
            self.setWindowTitle("Apply PenaltySupport Boundary Condition")
            self.label_PenaltySupport = QtGui.QLabel("Please enter the displacement constraint values:", self)
            self.label_PenaltySupport.move(10, 20)
            self.element_list = []
            self.x_val = 0
            self.y_val = 0
            self.z_val = 0

            self.label_x_constraint = QtGui.QLabel("x: ", self)
            self.label_x_constraint.move(10,48)
            self.text_x_constraint = QtGui.QLineEdit(self)
            self.text_x_constraint.setFixedWidth(80)
            self.text_x_constraint.setValidator(std_validate)
            self.text_x_constraint.move(30, 45)

            self.label_y_constraint = QtGui.QLabel("y: ", self)
            self.label_y_constraint.move(120,48)
            self.text_y_constraint = QtGui.QLineEdit(self)
            self.text_y_constraint.setFixedWidth(80)
            self.text_y_constraint.setValidator(std_validate)
            self.text_y_constraint.move(140, 45)

            self.label_z_constraint = QtGui.QLabel("z: ", self)
            self.label_z_constraint.move(230, 48)
            self.text_z_constraint = QtGui.QLineEdit(self)
            self.text_z_constraint.setFixedWidth(80)
            self.text_z_constraint.setValidator(std_validate)
            self.text_z_constraint.move(250, 45)

            okButton_PenaltySupportBCBox = QtGui.QPushButton('OK', self)
            okButton_PenaltySupportBCBox.move(140, 85)
            okButton_PenaltySupportBCBox.clicked.connect(self.okButton_PenaltySupportBCBox)
            okButton_PenaltySupportBCBox.setAutoDefault(True)

            self.PenaltySupport_count = 0

    def closeEvent(self, event):
        self.resetInputValues()
        event.accept()

    def okButton_PenaltySupportBCBox(self):
        #print("Mouse Click " + str(self.PenaltySupport_count))
        self.PenaltySupport_count = self.PenaltySupport_count + 1
        self.x_val = self.text_x_constraint.text()
        self.y_val = self.text_y_constraint.text()
        self.z_val = self.text_z_constraint.text()
        if (self.x_val == '') or (self.y_val == '') or (self.z_val == ''):
            errorMsg = QtGui.QMessageBox.critical(self, "Error: PenaltySupport Boundary Condition","Displacement constraint values cannot be blank!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
        
        self.resetInputValues()
        self.okButton_Flag = True
        self.close()

    def resetInputValues(self):
        self.text_x_constraint.setText("")
        self.text_y_constraint.setText("")
        self.text_z_constraint.setText("")

class SurfaceLoadBCBox(QtGui.QDialog):
    """"""
    def __init__(self):
        super(SurfaceLoadBCBox, self).__init__()
        self.initUI()

    def initUI(self):
            width = 350
            height = 175
            std_validate = QtGui.QDoubleValidator()
            std_validate.setNotation(QtGui.QDoubleValidator.StandardNotation)
            centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
            self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
            self.setWindowTitle("Apply SurfaceLoad Boundary Condition")

            self.label_SurfaceLoad_modulus = QtGui.QLabel("Please enter the magnitude of the load:", self)
            self.label_SurfaceLoad_modulus.move(10, 20)
            self.text_SurfaceLoad_modulus = QtGui.QLineEdit(self)
            self.text_SurfaceLoad_modulus.setValidator(std_validate)
            self.text_SurfaceLoad_modulus.setFixedWidth(80)
            self.text_SurfaceLoad_modulus.move(140, self.label_SurfaceLoad_modulus.y()+25)

            self.label_SurfaceLoad_direction = QtGui.QLabel("Please enter the acting direction of the force :", self)
            self.label_SurfaceLoad_direction.move(10, self.text_SurfaceLoad_modulus.y()+30)
            self.element_list = []
            self.x_val = 0
            self.y_val = 0
            self.z_val = 0

            self.label_x_constraint = QtGui.QLabel("x: ", self)
            self.label_x_constraint.move(10,self.label_SurfaceLoad_direction.y()+28)
            self.text_x_constraint = QtGui.QLineEdit(self)
            self.text_x_constraint.setFixedWidth(80)
            self.text_x_constraint.setValidator(std_validate)
            self.text_x_constraint.move(30, self.label_x_constraint.y()-3)

            self.label_y_constraint = QtGui.QLabel("y: ", self)
            self.label_y_constraint.move(120,self.label_x_constraint.y())
            self.text_y_constraint = QtGui.QLineEdit(self)
            self.text_y_constraint.setFixedWidth(80)
            self.text_y_constraint.setValidator(std_validate)
            self.text_y_constraint.move(140, self.text_x_constraint.y())

            self.label_z_constraint = QtGui.QLabel("z: ", self)
            self.label_z_constraint.move(230, self.label_x_constraint.y())
            self.text_z_constraint = QtGui.QLineEdit(self)
            self.text_z_constraint.setFixedWidth(80)
            self.text_z_constraint.setValidator(std_validate)
            self.text_z_constraint.move(250, self.text_x_constraint.y())

            okButton_SurfaceLoadBCBox = QtGui.QPushButton('OK', self)
            okButton_SurfaceLoadBCBox.move(140, self.text_x_constraint.y()+40)
            okButton_SurfaceLoadBCBox.clicked.connect(self.okButton_SurfaceLoadBCBox)
            okButton_SurfaceLoadBCBox.setAutoDefault(True)

            self.SurfaceLoad_count = 1

    def closeEvent(self, event):
        self.resetInputValues()
        event.accept()

    def okButton_SurfaceLoadBCBox(self):
        #print("Mouse Click " + str(self.SurfaceLoad_count))
        self.SurfaceLoad_count = self.SurfaceLoad_count + 1
        self.x_val = self.text_x_constraint.text()
        self.y_val = self.text_y_constraint.text()
        self.z_val = self.text_z_constraint.text()
        self.modulus_val = self.text_SurfaceLoad_modulus.text()
        if (self.x_val == '') or (self.y_val == '') or (self.z_val == ''):
            errorMsg = QtGui.QMessageBox.critical(self, "Error: SurfaceLoad Boundary Condition","Force direction cannot be blank!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
        
        self.resetInputValues()
        self.okButton_Flag = True
        self.close()

    def resetInputValues(self):
        self.text_x_constraint.setText("")
        self.text_y_constraint.setText("")
        self.text_z_constraint.setText("")

class PenaltySupportFacesList(QtGui.QWidget):
    """"""
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("List of Faces")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on = True)
        layout = QtGui.QGridLayout()

        FaceID_label = QtGui.QLabel("Faces Under PenaltySupport BC:", self)
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

class SurfaceLoadFacesList(QtGui.QWidget):
    """"""
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("List of Faces")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on = True)
        layout = QtGui.QGridLayout()

        FaceID_label = QtGui.QLabel("Faces Under SurfaceLoad BC:", self)
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

class SolverSettingsBox(QtGui.QDialog):

    def __init__(self):
        super(SolverSettingsBox, self).__init__()
        self.initUI()

    def initUI(self):    
        width = 330
        height = 1070
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Kratos Solver Settings")

        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        boldUnderlinedFont=QtGui.QFont()
        boldUnderlinedFont.setBold(True)
        boldUnderlinedFont.setUnderline(True)
        blueFont = QtGui.QPalette()
        blueFont.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#005293'))

        #solution settings head
        self.label_main_ = QtGui.QLabel("Problem data:", self)
        self.label_main_.move(10, 10)
       
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #parallel type
        self.label_parallel_type_ = QtGui.QLabel("Parallel type:", self)
        self.label_parallel_type_.move(10, self.label_main_.y()+30)
        self.textInput_parallel_type_ = QtGui.QLineEdit(self)
        self.textInput_parallel_type_.setPlaceholderText("OpenMP")
        self.textInput_parallel_type_.setFixedWidth(100)
        self.textInput_parallel_type_.move(10, self.label_parallel_type_.y()+20)

        #echo level
        self.label_echo_level2_ = QtGui.QLabel("Echo level:", self)
        self.label_echo_level2_.move(200, self.label_main_.y()+30)
        self.textInput_echo_level2_ = QtGui.QLineEdit(self)
        self.textInput_echo_level2_.setPlaceholderText("1")
        self.textInput_echo_level2_.setFixedWidth(100)
        self.textInput_echo_level2_.move(200, self.label_echo_level2_.y()+20)

        #start time
        self.label_start_time_ = QtGui.QLabel("Start time:", self)
        self.label_start_time_.move(10, self.textInput_echo_level2_.y()+30)
        self.textInput_start_time_ = QtGui.QLineEdit(self)
        self.textInput_start_time_.setPlaceholderText("0.0")
        self.textInput_start_time_.setFixedWidth(100)
        self.textInput_start_time_.move(10, self.label_start_time_.y()+20)

        #end time
        self.label_end_time_ = QtGui.QLabel("End time:", self)
        self.label_end_time_.move(200, self.textInput_echo_level2_.y()+30)
        self.textInput_end_time_ = QtGui.QLineEdit(self)
        self.textInput_end_time_.setPlaceholderText("1.0")
        self.textInput_end_time_.setFixedWidth(100)
        self.textInput_end_time_.move(200, self.label_end_time_.y()+20)

        #Solver settings head
        self.label_main_ = QtGui.QLabel("Solver settings:", self)
        self.label_main_.move(10, self.textInput_end_time_.y()+40)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #solver type
        self.label_solver_type_ = QtGui.QLabel("Solver type:", self)
        self.label_solver_type_.move(10, self.label_main_.y()+30)
        self.textInput_solver_type_ = QtGui.QLineEdit(self)
        self.textInput_solver_type_.setPlaceholderText("Static")
        self.textInput_solver_type_.setFixedWidth(100)
        self.textInput_solver_type_.move(10, self.label_solver_type_.y()+20)

        #analysis type
        self.label_analysis_type_ = QtGui.QLabel("Analysis type:", self)
        self.label_analysis_type_.move(200, self.label_main_.y()+30)
        self.popup_analysis_type_ = QtGui.QComboBox(self)
        self.popup_analysis_type_items = ('linear', 'nonlinear')
        self.popup_analysis_type_.addItems(self.popup_analysis_type_items)
        self.popup_analysis_type_.setFixedWidth(100)
        self.popup_analysis_type_.move(200, self.label_analysis_type_.y()+20)

        #model part name
        self.label_model_part_name_ = QtGui.QLabel("Model part name:", self)
        self.label_model_part_name_.move(10, self.popup_analysis_type_.y()+30)
        self.textInput_model_part_name_ = QtGui.QLineEdit(self)
        self.textInput_model_part_name_.setPlaceholderText("NurbsMesh")
        self.textInput_model_part_name_.setFixedWidth(100)
        self.textInput_model_part_name_.move(10, self.label_model_part_name_.y()+20)

        #echo level 
        self.label_echo_level3_ = QtGui.QLabel("Echo level:", self)
        self.label_echo_level3_.move(200, self.popup_analysis_type_.y()+30)
        self.textInput_echo_level3_ = QtGui.QLineEdit(self)
        self.textInput_echo_level3_.setPlaceholderText("1")
        self.textInput_echo_level3_.setFixedWidth(100)
        self.textInput_echo_level3_.move(200, self.label_echo_level3_.y()+20)

        #Material import setting - Input type
        self.label_input_type_ = QtGui.QLabel("Material import setting - Input type:", self)
        self.label_input_type_.move(10, self.textInput_echo_level3_.y()+35)
        self.textInput_input_type_ = QtGui.QLineEdit(self)
        self.textInput_input_type_.setPlaceholderText("use_input_model_part")
        self.textInput_input_type_.setFixedWidth(300)
        self.textInput_input_type_.move(10, self.label_input_type_.y()+20)

        #linear solver settings head
        self.label_main_ = QtGui.QLabel("Linear solver settings:", self)
        self.label_main_.move(10, self.textInput_input_type_.y()+40)
       
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #Preconditioner type
        self.label_preconditioner_type_ = QtGui.QLabel("Preconditioner type:", self)
        self.label_preconditioner_type_.move(10, self.label_main_.y()+30)
        self.textInput_preconditioner_type_ = QtGui.QLineEdit(self)
        self.textInput_preconditioner_type_.setPlaceholderText("additive_schwarz")
        self.textInput_preconditioner_type_.setFixedWidth(300)
        self.textInput_preconditioner_type_.move(10, self.label_preconditioner_type_.y()+20)

        #Solver type
        self.label_solver_type2_ = QtGui.QLabel("Solver type:", self)
        self.label_solver_type2_.move(10, self.textInput_preconditioner_type_.y()+30)
        self.textInput_solver_type2_ = QtGui.QLineEdit(self)
        self.textInput_solver_type2_.setPlaceholderText("bicgstab")
        self.textInput_solver_type2_.setFixedWidth(300)
        self.textInput_solver_type2_.move(10, self.label_solver_type2_.y()+20)


        #Tolerance
        self.label_tolerance_ = QtGui.QLabel("Tolerance:", self)
        self.label_tolerance_.move(200, self.textInput_solver_type2_.y()+30)
        self.textInput_tolerance_ = QtGui.QLineEdit(self)
        self.textInput_tolerance_.setPlaceholderText("1e-6")
        self.textInput_tolerance_.setFixedWidth(100)
        self.textInput_tolerance_.move(200, self.label_tolerance_.y()+20)

        #Rotation dofs
        self.label_rotation_dofs_ = QtGui.QLabel("Rotation dof:", self)
        self.label_rotation_dofs_.move(10, self.textInput_solver_type2_.y()+30)
        self.popup_rotation_dofs_ = QtGui.QComboBox(self)
        self.popup_rotation_dofs_items = ("false", "true")
        self.popup_rotation_dofs_.addItems(self.popup_rotation_dofs_items)
        self.popup_rotation_dofs_.setFixedWidth(100)
        self.popup_rotation_dofs_.move(10, self.label_rotation_dofs_.y()+20)

        #use block builder
        self.label_block_builder_ = QtGui.QLabel("Use block builder:", self)
        self.label_block_builder_.move(200, self.textInput_tolerance_.y()+30)
        self.popup_block_builder_ = QtGui.QComboBox(self)
        self.popup_block_builder_items = ("true", "false")
        self.popup_block_builder_.addItems(self.popup_block_builder_items)
        self.popup_block_builder_.setFixedWidth(100)
        self.popup_block_builder_.move(200, self.label_block_builder_.y()+20)

        #Residual relative tolerance
        self.label_relative_tolerance_ = QtGui.QLabel("Residual relative tol.:", self)
        self.label_relative_tolerance_.move(10, self.textInput_tolerance_.y()+30)
        self.textInput_relative_tolerance_ = QtGui.QLineEdit(self)
        self.textInput_relative_tolerance_.setPlaceholderText("0.000001")
        self.textInput_relative_tolerance_.setFixedWidth(100)
        self.textInput_relative_tolerance_.move(10, self.label_relative_tolerance_.y()+20)

        #Modelers head
        self.label_main_ = QtGui.QLabel("Modelers:", self)
        self.label_main_.move(10, self.textInput_relative_tolerance_.y()+40)
       
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #Modeler Name
        self.label_modeler_name_ = QtGui.QLabel("Modeler name:", self)
        self.label_modeler_name_.move(10, self.label_main_.y()+30)
        self.textInput_modeler_name_ = QtGui.QLineEdit(self)
        self.textInput_modeler_name_.setPlaceholderText("NurbsGeometryModeler")
        self.textInput_modeler_name_.setFixedWidth(300)
        self.textInput_modeler_name_.move(10, self.label_modeler_name_.y()+20)

        #Modeler Part Name
        self.label_modeler_part_name_ = QtGui.QLabel("Modeler part name:", self)
        self.label_modeler_part_name_.move(10, self.textInput_modeler_name_.y()+30)
        self.textInput_modeler_part_name_ = QtGui.QLineEdit(self)
        self.textInput_modeler_part_name_.setPlaceholderText("NurbsMesh")
        self.textInput_modeler_part_name_.setFixedWidth(300)
        self.textInput_modeler_part_name_.move(10, self.label_modeler_part_name_.y()+20)

        #Modeler Geometry Name
        self.label_modeler_geometry_name_ = QtGui.QLabel("Modeler geometry name:", self)
        self.label_modeler_geometry_name_.move(10, self.textInput_modeler_part_name_.y()+30)
        self.textInput_modeler_geometry_name_ = QtGui.QLineEdit(self)
        self.textInput_modeler_geometry_name_.setPlaceholderText("NurbsVolume")
        self.textInput_modeler_geometry_name_.setFixedWidth(300)
        self.textInput_modeler_geometry_name_.move(10, self.label_modeler_geometry_name_.y()+20)


        #Material properties head
        self.label_main_ = QtGui.QLabel("Material Properties:", self)
        self.label_main_.move(10, self.textInput_modeler_geometry_name_.y()+30)
       
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)

        #Density
        self.label_density_ = QtGui.QLabel("Density:", self)
        self.label_density_.move(10, self.label_main_.y()+30)
        self.textInput_density_ = QtGui.QLineEdit(self)
        self.textInput_density_.setPlaceholderText("1.0")
        self.textInput_density_.setFixedWidth(100)
        self.textInput_density_.move(10, self.label_density_.y()+20)

        #Young Modulus
        self.label_young_modulus_ = QtGui.QLabel("Young Modulus:", self)
        self.label_young_modulus_.move(200, self.label_main_.y()+30)
        self.textInput_young_modulus_ = QtGui.QLineEdit(self)
        self.textInput_young_modulus_.setPlaceholderText("100")
        self.textInput_young_modulus_.setFixedWidth(100)
        self.textInput_young_modulus_.move(200, self.label_young_modulus_.y()+20)

        #Poisson Ratio
        self.label_poisson_ratio_ = QtGui.QLabel("Poisson Ratio:", self)
        self.label_poisson_ratio_.move(10, self.textInput_young_modulus_.y()+30)
        self.textInput_poisson_ratio_ = QtGui.QLineEdit(self)
        self.textInput_poisson_ratio_.setPlaceholderText("0.0")
        self.textInput_poisson_ratio_.setFixedWidth(100)
        self.textInput_poisson_ratio_.move(10, self.label_poisson_ratio_.y()+20)

        #Properties id
        self.label_properties_id_ = QtGui.QLabel("Properties ID:", self)
        self.label_properties_id_.move(200, self.textInput_young_modulus_.y()+30)
        self.textInput_properties_id_ = QtGui.QLineEdit(self)
        self.textInput_properties_id_.setPlaceholderText("1")
        self.textInput_properties_id_.setFixedWidth(100)
        self.textInput_properties_id_.move(200, self.label_properties_id_.y()+20)

        #Constitutive law
        self.label_constitutive_id_ = QtGui.QLabel("Constitutive law name:", self)
        self.label_constitutive_id_.move(10, self.textInput_properties_id_.y()+30)
        self.textInput_constitutive_id_ = QtGui.QLineEdit(self)
        self.textInput_constitutive_id_.setPlaceholderText("LinearElastic3DLaw")
        self.textInput_constitutive_id_.setFixedWidth(150)
        self.textInput_constitutive_id_.move(10, self.label_constitutive_id_.y()+20)


        # cancel button
        self.cancelButton = QtGui.QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.onCancel)
        self.cancelButton.setFixedWidth(80)

        # OK button
        self.okButton = QtGui.QPushButton('OK', self)
        self.okButton.clicked.connect(self.onOk)
        self.okButton.setAutoDefault(True)
        self.okButton.setFixedWidth(80)
        
        self.container_okCancel = QtGui.QWidget(self)
        self.container_okCancel.setContentsMargins(0, 0, 0, 0)
    
        self.layout_okCancel = QtGui.QHBoxLayout(self.container_okCancel)
        self.layout_okCancel.setContentsMargins(0, 0, 0,0)
        self.layout_okCancel.addWidget(self.okButton)
        self.layout_okCancel.addWidget(self.cancelButton)
        self.layout_okCancel.setSpacing(40)

        self.container_okCancel.move(0.5*width - self.okButton.geometry().width() - 0.5*self.layout_okCancel.spacing(), 
                                     self.textInput_constitutive_id_.y()+50)
    
    def onOk(self):

        self.result = "Ok"


        self.KratosParam = \
        {
            "problem_data"    : {
                "parallel_type" : self.textInput_parallel_type_.text(),
                "echo_level"    : int(self.textInput_echo_level2_.text()),
                "start_time"    : float(self.textInput_start_time_.text()),
                "end_time"      : float(self.textInput_end_time_.text())
            },
            "solver_settings" : {
                "solver_type"              : self.textInput_solver_type_.text(),
                "analysis_type"            : self.popup_analysis_type_.currentText(),
                "model_part_name"          : self.textInput_model_part_name_.text(),
                "echo_level"               : int(self.textInput_echo_level3_.text()),
                "domain_size"              : 3,
                "model_import_settings"    : {
                    "input_type"     : self.textInput_input_type_.text()
                },
                "material_import_settings"        : {
                    "materials_filename" : "StructuralMaterials.json"
                },
                "time_stepping"            : {
                    "time_step" : 1.1       
                },
                "linear_solver_settings":{
                    "preconditioner_type" : self.textInput_preconditioner_type_.text(),
                    "solver_type": self.textInput_solver_type2_.text(),
                    "max_iteration" : 5000,
                    "tolerance" : float(self.textInput_tolerance_.text())
                },
                "rotation_dofs"            : self.popup_rotation_dofs_.currentText(),
                "builder_and_solver_settings" : {
                    "use_block_builder" : self.popup_block_builder_.currentText()
                },
                "residual_relative_tolerance"        : float(self.textInput_relative_tolerance_.text())
            },
            "modelers" : [{
                        "modeler_name": self.textInput_modeler_name_.text(),
                        "Parameters": {
                            "model_part_name" : self.textInput_modeler_part_name_.text(),
                            "geometry_name"   : self.textInput_modeler_geometry_name_.text()}
                    }]
        }


        self.StructuralMat = \
        {
            "properties" : [{
                "model_part_name" : self.textInput_modeler_part_name_.text(),
                "properties_id"   : int(self.textInput_properties_id_.text()),
                "Material"        : {
                    "constitutive_law" : {
                        "name" : self.textInput_constitutive_id_.text()
                    },
                    "Variables"        : {
                        "DENSITY"       : float(self.textInput_density_.text()),
                        "YOUNG_MODULUS" : float(self.textInput_young_modulus_.text()),
                        "POISSON_RATIO" : float(self.textInput_poisson_ratio_.text())
                    },
                    "Tables"           : {}
                }
            }]
        }

        self.close()

            
    def onCancel(self):
        self.result = "Cancel"
        self.close()
