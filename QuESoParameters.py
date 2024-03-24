##--------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------##
##                                                                                      ##
##    Software Lab Project: FreeCAD Plug-in "QuESo4FreeCAD" by:                         ##
##                                                                                      ##
##    Bediralp Çerme                                                                    ##
##    Daniel Perka                                                                      ##      
##    Barış Egemen Sucu                                                                 ##
##                                                                                      ##
##--------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------##


from FreeCAD_PySide import QtGui, QtCore
import os, shutil
import FreeCAD
import FreeCADGui as Gui
import Draft, Mesh, MeshPart, ImportGui
import json
from pivy import coin
from collections import OrderedDict
import math
import subprocess
import OpenSCADUtils

class QuESoParameters(QtGui.QMainWindow): 

    def __init__(self): 

        super(QuESoParameters, self).__init__()
        self.visulizerun    = 0
        self.gridList       = []
        self.mainObjectName = ""
        self.initUI()           

    def initUI(self):

##########################################################################################
##                                                                                      ##
##                     SETTING UP THE QuESoParameters POP-UP WINDOW                     ##
##                                                                                      ##
##########################################################################################

        #The original QuESoParameters pop-up window is a QMainWindow object because we 
        #wanted to include scrolling option in it. It is our primary window on which everything 
        #is displayed.\n
        #'viewport' is a QDialog object, and every label, text input box is an object of viewport.
        #The reason not creating the QuESoParameters primary window as QDialog object is solely 
        #to be able to use scrolling feature.

        self.viewport   = QtGui.QDialog()
        self.scrollArea = QtGui.QScrollArea()
        layout_dialog   = QtGui.QGridLayout()

        std_validate        = QtGui.QIntValidator()                                # The validation method for an input to be integer.
        scientific_validate = QtGui.QDoubleValidator()                             # The validation method for an input to be double.
        scientific_validate.setNotation(QtGui.QDoubleValidator.ScientificNotation) # The validation method for an input to be in scientific notation.
        double_validate = QtGui.QDoubleValidator()
        self.setWindowTitle("QuESo Parameters")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, on = True)
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        boldUnderlinedFont = QtGui.QFont()
        boldUnderlinedFont.setBold(True)
        boldUnderlinedFont.setUnderline(True)
        blueFont = QtGui.QPalette()
        blueFont.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#005293'))

        # Introducing Qt's built-in icons for visual enchancements

        back_arrow_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_ArrowBack)
        cancel_icon     = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogCancelButton)
        save_icon       = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogSaveButton)
        browse_icon     = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DirOpenIcon)

        self.viewport.goback_button = QtGui.QPushButton("Go Back", self)
        self.viewport.goback_button.setIcon(back_arrow_icon)
        layout_dialog.addWidget(self.viewport.goback_button, 0, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(1, 10)

##**************************************************************************************##
##                          Beginning of General Settings Head                          ##
##**************************************************************************************##


        self.viewport.label_main_ = QtGui.QLabel("General settings", self)
        self.viewport.label_main_.setFont(boldUnderlinedFont)
        self.viewport.label_main_.setPalette(blueFont)
        layout_dialog.addWidget(self.viewport.label_main_, 2, 0, QtCore.Qt.AlignHCenter)

        layout_dialog.setRowMinimumHeight(3, 5)

        self.viewport.label_QuESo_ = QtGui.QLabel("Directory of the QuESo:", self)
        layout_dialog.addWidget(self.viewport.label_QuESo_, 4, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(5, 0)

        layout_QuESo_text              = QtGui.QHBoxLayout()
        self.viewport.textInput_QuESo_ = QtGui.QLineEdit(self)
        self.viewport.textInput_QuESo_.setText("")
        self.viewport.textInput_QuESo_.setMinimumWidth(200)
        layout_QuESo_text.addWidget(self.viewport.textInput_QuESo_)

        self.viewport.fileBrowseButton_QuESo = QtGui.QPushButton('Browse files',self)
        self.viewport.fileBrowseButton_QuESo.setIcon(browse_icon)
        self.viewport.fileBrowseButton_QuESo.setAutoDefault(False)
        layout_QuESo_text.addWidget(self.viewport.fileBrowseButton_QuESo)

        layout_dialog.addLayout(layout_QuESo_text, 6, 0, 1, -1)

        layout_dialog.setRowMinimumHeight(7, 5)

        self.viewport.label_Kratos_ = QtGui.QLabel("Directory of the Kratos:", self)
        layout_dialog.addWidget(self.viewport.label_Kratos_, 8, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(9, 0)

        layout_kratos_text              = QtGui.QHBoxLayout()
        self.viewport.textInput_Kratos_ = QtGui.QLineEdit(self)
        self.viewport.textInput_Kratos_.setText("")
        self.viewport.textInput_Kratos_.setMinimumWidth(200)
        layout_kratos_text.addWidget(self.viewport.textInput_Kratos_)

        self.viewport.fileBrowseButton_Kratos = QtGui.QPushButton('Browse files',self)
        self.viewport.fileBrowseButton_Kratos.setIcon(browse_icon)
        self.viewport.fileBrowseButton_Kratos.setAutoDefault(False)
        layout_kratos_text.addWidget(self.viewport.fileBrowseButton_Kratos)

        layout_dialog.addLayout(layout_kratos_text, 10, 0, 1, -1)

        layout_dialog.setRowMinimumHeight(11, 5)

        self.viewport.label_echo_ = QtGui.QLabel("Echo level:", self)
        layout_dialog.addWidget(self.viewport.label_echo_, 12, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(13, 0)

        self.viewport.textInput_echo_ = QtGui.QLineEdit(self)
        self.viewport.textInput_echo_.setPlaceholderText("1")
        self.viewport.textInput_echo_.setFixedWidth(50)
        self.viewport.textInput_echo_.setValidator(std_validate)

        layout_dialog.addWidget(self.viewport.textInput_echo_, 14, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(15, 10)

##  **************************************************************************************

##**************************************************************************************##
##                           Beginning of Mesh Settings Head                            ##
##**************************************************************************************##


        self.viewport.label_main_ = QtGui.QLabel("Mesh Settings", self)
        self.viewport.label_main_.setFont(boldUnderlinedFont)
        self.viewport.label_main_.setPalette(blueFont)
        layout_dialog.addWidget(self.viewport.label_main_, 16, 0, QtCore.Qt.AlignHCenter)

        layout_dialog.setRowMinimumHeight(17, 5)
        
## ---- Mesher Type Section --------------------------------------------------------------

        self.viewport.label_mesh_type = QtGui.QLabel("Mesher Type:", self)
        self.viewport.label_mesh_type.setFont(boldFont)
        layout_dialog.addWidget(self.viewport.label_mesh_type, 18, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(19, 0)

        # Creating a subLayout for Mesher Type

        sublayout_mesh_types = QtGui.QGridLayout()

        self.viewport.standardUse_group = QtGui.QGroupBox("Standard mesher", self)
        self.viewport.standardUse_group.setCheckable(True)      
        sublayout_standardUse                 = QtGui.QGridLayout()
        self.viewport.surface_deviation_label = QtGui.QLabel("Surface Deviation:", self)
        sublayout_standardUse.addWidget(self.viewport.surface_deviation_label, 0, 0)
        sublayout_standardUse.setRowMinimumHeight(1, 0)
        self.viewport.surface_deviation_textInput = QtGui.QLineEdit(self)
        self.viewport.surface_deviation_textInput.setPlaceholderText("units in mm")
        sublayout_standardUse.addWidget(self.viewport.surface_deviation_textInput, 2, 0)
        sublayout_standardUse.setRowMinimumHeight(3, 0)
        self.viewport.angular_deviation_label = QtGui.QLabel("Angular Deviation:", self)
        sublayout_standardUse.addWidget(self.viewport.angular_deviation_label, 4, 0)
        sublayout_standardUse.setRowMinimumHeight(5, 0)
        self.viewport.angular_deviation_textInput = QtGui.QLineEdit(self)
        self.viewport.angular_deviation_textInput.setPlaceholderText("units in rad")
        sublayout_standardUse.addWidget(self.viewport.angular_deviation_textInput, 6, 0)
        self.viewport.standardUse_group.setLayout(sublayout_standardUse)

        self.viewport.gmshUse_group = QtGui.QGroupBox("Gmsh mesher", self)
        self.viewport.gmshUse_group.setCheckable(True)
        self.viewport.gmshUse_group.setChecked(False)     
        sublayout_gmshUse             = QtGui.QGridLayout()
        self.viewport.maxElSize_label = QtGui.QLabel("Max Element Size:", self)
        sublayout_gmshUse.addWidget(self.viewport.maxElSize_label, 0, 0)
        sublayout_gmshUse.setRowMinimumHeight(1, 0)
        self.viewport.maxElSize_textInput = QtGui.QLineEdit(self)
        self.viewport.maxElSize_textInput.setValidator(double_validate)
        self.viewport.maxElSize_textInput.setPlaceholderText("units in mm")
        sublayout_gmshUse.addWidget(self.viewport.maxElSize_textInput, 2, 0)
        sublayout_gmshUse.setRowMinimumHeight(3, 0)
        self.viewport.minElSize_label = QtGui.QLabel("Min Element Size:", self)
        sublayout_gmshUse.addWidget(self.viewport.minElSize_label, 4, 0)
        sublayout_gmshUse.setRowMinimumHeight(5, 0)
        self.viewport.minElSize_textInput = QtGui.QLineEdit(self)
        self.viewport.minElSize_textInput.setValidator(double_validate)
        self.viewport.minElSize_textInput.setPlaceholderText("units in mm")
        sublayout_gmshUse.addWidget(self.viewport.minElSize_textInput, 6, 0)
        self.viewport.gmshUse_group.setLayout(sublayout_gmshUse)

        sublayout_mesh_types.addWidget(self.viewport.standardUse_group, 0, 0, QtCore.Qt.AlignLeft)
        sublayout_mesh_types.addWidget(self.viewport.gmshUse_group, 0, 1, QtCore.Qt.AlignRight)

        layout_dialog.addLayout(sublayout_mesh_types, 20, 0)

##  --------------------------------------------------------------------------------------

        layout_dialog.setRowMinimumHeight(21, 0)

## ---- Polynomial Order Section ---------------------------------------------------------

        self.viewport.label_polynomialOrder_ = QtGui.QLabel("Polynomial order:", self)
        self.viewport.label_polynomialOrder_.setFont(boldFont)
        layout_dialog.addWidget(self.viewport.label_polynomialOrder_, 22, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(23, 0)

        # Creating a subLayout for Polynomial Order

        layout_poly_xyz = QtGui.QGridLayout()

        self.viewport.label_polynomialOrder_x_ = QtGui.QLabel("x: ", self)
        layout_poly_xyz.addWidget(self.viewport.label_polynomialOrder_x_, 0, 0, QtCore.Qt.AlignLeft)

        layout_poly_xyz.setColumnMinimumWidth(1, 0)

        self.viewport.textInput_polynomialOrder_x_ = QtGui.QLineEdit(self)
        self.viewport.textInput_polynomialOrder_x_.setPlaceholderText("1")
        self.viewport.textInput_polynomialOrder_x_.setFixedWidth(50)
        self.viewport.textInput_polynomialOrder_x_.setValidator(std_validate)
        layout_poly_xyz.addWidget(self.viewport.textInput_polynomialOrder_x_, 0, 2, QtCore.Qt.AlignLeft)

        layout_poly_xyz.setColumnMinimumWidth(3, 20)

        self.viewport.label_polynomialOrder_y_ = QtGui.QLabel("y: ", self)
        layout_poly_xyz.addWidget(self.viewport.label_polynomialOrder_y_, 0, 4, QtCore.Qt.AlignLeft)

        layout_poly_xyz.setColumnMinimumWidth(5, 0)

        self.viewport.textInput_polynomialOrder_y_ = QtGui.QLineEdit(self)
        self.viewport.textInput_polynomialOrder_y_.setPlaceholderText("1")
        self.viewport.textInput_polynomialOrder_y_.setFixedWidth(50)
        self.viewport.textInput_polynomialOrder_y_.setValidator(std_validate)

        layout_poly_xyz.addWidget(self.viewport.textInput_polynomialOrder_y_, 0, 6, QtCore.Qt.AlignLeft)

        layout_poly_xyz.setColumnMinimumWidth(7, 20)

        self.viewport.label_polynomialOrder_z_ = QtGui.QLabel("z: ", self)
        layout_poly_xyz.addWidget(self.viewport.label_polynomialOrder_z_, 0, 8, QtCore.Qt.AlignLeft)

        layout_poly_xyz.setColumnMinimumWidth(9, 0)

        self.viewport.textInput_polynomialOrder_z_ = QtGui.QLineEdit(self)
        self.viewport.textInput_polynomialOrder_z_.setPlaceholderText("1")
        self.viewport.textInput_polynomialOrder_z_.setFixedWidth(50)
        self.viewport.textInput_polynomialOrder_z_.setValidator(std_validate)

        layout_poly_xyz.addWidget(self.viewport.textInput_polynomialOrder_z_, 0, 10, QtCore.Qt.AlignLeft)

        layout_dialog.addLayout(layout_poly_xyz, 24, 0, QtCore.Qt.AlignCenter)

##  --------------------------------------------------------------------------------------

        layout_dialog.setRowMinimumHeight(25, 5)

## ---- Number of Elements Section -------------------------------------------------------

        self.viewport.label_nElements_ = QtGui.QLabel("Number of elements:", self)
        self.viewport.label_nElements_.setFont(boldFont)
        layout_dialog.addWidget(self.viewport.label_nElements_, 26, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(27, 0)

        # Creating a subLayout for Number of Elements

        layout_nElements_ = QtGui.QGridLayout()

        self.viewport.label_nElements_x_ = QtGui.QLabel("x: ", self)
        layout_nElements_.addWidget(self.viewport.label_nElements_x_, 0, 0, QtCore.Qt.AlignLeft)

        layout_nElements_.setColumnMinimumWidth(1, 0)

        self.viewport.textInput_nElements_x_ = QtGui.QLineEdit(self)
        self.viewport.textInput_nElements_x_.setPlaceholderText("1")
        self.viewport.textInput_nElements_x_.setFixedWidth(50)
        self.viewport.textInput_nElements_x_.setValidator(std_validate)
        layout_nElements_.addWidget(self.viewport.textInput_nElements_x_, 0, 2, QtCore.Qt.AlignLeft)

        layout_nElements_.setColumnMinimumWidth(3, 20)

        self.viewport.label_nElements_y_ = QtGui.QLabel("y: ", self)
        layout_nElements_.addWidget(self.viewport.label_nElements_y_, 0, 4, QtCore.Qt.AlignLeft)

        layout_nElements_.setColumnMinimumWidth(5, 0)

        self.viewport.textInput_nElements_y_ = QtGui.QLineEdit(self)
        self.viewport.textInput_nElements_y_.setPlaceholderText("1")
        self.viewport.textInput_nElements_y_.setFixedWidth(50)
        self.viewport.textInput_nElements_y_.setValidator(std_validate)
        layout_nElements_.addWidget(self.viewport.textInput_nElements_y_, 0, 6, QtCore.Qt.AlignLeft)

        layout_nElements_.setColumnMinimumWidth(7, 20)

        self.viewport.label_nElements_z_ = QtGui.QLabel("z: ", self)
        layout_nElements_.addWidget(self.viewport.label_nElements_z_, 0, 8, QtCore.Qt.AlignLeft)

        layout_nElements_.setColumnMinimumWidth(9, 0)

        self.viewport.textInput_nElements_z_ = QtGui.QLineEdit(self)
        self.viewport.textInput_nElements_z_.setPlaceholderText("1")
        self.viewport.textInput_nElements_z_.setFixedWidth(50)
        self.viewport.textInput_nElements_z_.setValidator(std_validate)

        layout_nElements_.addWidget(self.viewport.textInput_nElements_z_, 0, 10, QtCore.Qt.AlignLeft)

        layout_dialog.addLayout(layout_nElements_, 28, 0, QtCore.Qt.AlignCenter)

##  --------------------------------------------------------------------------------------

        layout_dialog.setRowMinimumHeight(29, 5)

## ---- Visualize Grids Section ----------------------------------------------------------

        self.viewport.visualizeButton = QtGui.QCheckBox('Visualize Grids', self)
        layout_dialog.addWidget(self.viewport.visualizeButton, 30, 0)

##  --------------------------------------------------------------------------------------

        layout_dialog.setRowMinimumHeight(31, 10)

##  **************************************************************************************

##**************************************************************************************##
##                         Beginning of Solution Settings Head                          ##
##**************************************************************************************##


        self.viewport.label_main_ = QtGui.QLabel("Solution Settings:", self)
        self.viewport.label_main_.setFont(boldUnderlinedFont)
        self.viewport.label_main_.setPalette(blueFont)
        layout_dialog.addWidget(self.viewport.label_main_, 32, 0, QtCore.Qt.AlignCenter)

        layout_dialog.setRowMinimumHeight(33, 5)

        self.viewport.label_residual_ = QtGui.QLabel("Moment fitting residual:", self)
        layout_dialog.addWidget(self.viewport.label_residual_, 34, 0, QtCore.Qt.AlignLeft)

        layout_dialog.setRowMinimumHeight(35, 0)

        self.viewport.textInput_residual_ = QtGui.QLineEdit(self)
        self.viewport.textInput_residual_.setPlaceholderText("1e-6")
        self.viewport.textInput_residual_.setFixedWidth(50)
        self.viewport.textInput_residual_.setValidator(scientific_validate)
        layout_dialog.addWidget(self.viewport.textInput_residual_, 36, 0, 1, 1)

        layout_dialog.setRowMinimumHeight(37, 5)

        self.viewport.label_integration_ = QtGui.QLabel("Integration method:", self)
        layout_dialog.addWidget(self.viewport.label_integration_, 38, 0, 1, 1)

        layout_dialog.setRowMinimumHeight(39, 0)

        self.viewport.popup_integration       = QtGui.QComboBox(self)
        self.viewport.popup_integration_items = ("Gauss","Gauss_Reduced1","Gauss_Reduced2","GGQ_Optimal","GGQ_Reduced1", "GGQ_Reduced2")
        self.viewport.popup_integration.addItems(self.viewport.popup_integration_items)
        self.viewport.popup_integration.setMinimumWidth(140)
        layout_dialog.addWidget(self.viewport.popup_integration, 40, 0, 1, 0)

        layout_dialog.setRowMinimumHeight(41, 10)

##  **************************************************************************************

##**************************************************************************************##
##                        Beginning of Boundary Conditions Head                         ##
##**************************************************************************************##


        self.viewport.label_ApplyBC_ = QtGui.QLabel("Boundary Conditions", self)
        self.viewport.label_ApplyBC_.setFont(boldUnderlinedFont)
        self.viewport.label_ApplyBC_.setPalette(blueFont)
        layout_dialog.addWidget(self.viewport.label_ApplyBC_, 42, 0, QtCore.Qt.AlignCenter)

        layout_dialog.setRowMinimumHeight(43, 5)

        self.viewport.button_PenaltySupport_ = QtGui.QPushButton('Apply Penalty Support Condition',self)
        self.viewport.button_PenaltySupport_.setAutoDefault(False)
        self.viewport.button_PenaltySupport_.setMinimumWidth(230)
        layout_dialog.addWidget(self.viewport.button_PenaltySupport_, 44, 0, QtCore.Qt.AlignCenter)

        layout_dialog.setRowMinimumHeight(45, 0)

        self.viewport.button_SurfaceLoad_ = QtGui.QPushButton('Apply Surface Load Condition',self)
        self.viewport.button_SurfaceLoad_.setAutoDefault(False)
        self.viewport.button_SurfaceLoad_.setMinimumWidth(230)
        layout_dialog.addWidget(self.viewport.button_SurfaceLoad_, 46, 0, QtCore.Qt.AlignCenter)

        layout_dialog.setRowMinimumHeight(47, 10)

##  **************************************************************************************

##**************************************************************************************##
##                          Beginning of Solver Settings Head                           ##
##**************************************************************************************##

        self.viewport.label_SolverSettings_ = QtGui.QLabel("Solver Settings", self)
        self.viewport.label_SolverSettings_.setFont(boldUnderlinedFont)
        self.viewport.label_SolverSettings_.setPalette(blueFont)
        layout_dialog.addWidget(self.viewport.label_SolverSettings_, 48, 0, QtCore.Qt.AlignCenter)

        layout_dialog.setRowMinimumHeight(49, 5)

        self.viewport.SolverSettingsButton = QtGui.QPushButton('Apply Solver Settings',self)
        self.viewport.SolverSettingsButton.setAutoDefault(False)
        self.viewport.SolverSettingsButton.setMinimumWidth(155)
        layout_dialog.addWidget(self.viewport.SolverSettingsButton, 50, 0, QtCore.Qt.AlignCenter)

        layout_dialog.setRowMinimumHeight(51, 20)

##  **************************************************************************************

##**************************************************************************************##
##                           Placement of Save-Cancel buttons                           ##
##**************************************************************************************##

        layout_saveCancel = QtGui.QHBoxLayout()
        cancelButton      = QtGui.QPushButton("Cancel", self)
        cancelButton.setIcon(cancel_icon)
        saveButton = QtGui.QPushButton("Save", self)
        saveButton.setIcon(save_icon)
        layout_saveCancel.addWidget(saveButton)
        layout_saveCancel.addWidget(cancelButton)
        layout_saveCancel.setSpacing(40)

        layout_dialog.addLayout(layout_saveCancel, 52, 0, QtCore.Qt.AlignCenter)

##  **************************************************************************************

        self.viewport.setLayout(layout_dialog)

##**************************************************************************************##
## Adjusting the position and geometry of the QuESoParameters pop-up window as well as  ##
##                  establishing the scrolling option and its features                  ##
##**************************************************************************************##

        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.viewport)
        self.setCentralWidget(self.scrollArea)
        width       = self.sizeHint().width()
        height      = self.viewport.sizeHint().height()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setMinimumWidth(self.sizeHint().width())
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)

##  **************************************************************************************

##**************************************************************************************##
##         Establishing the signal/slot pairs for the buttons/checkboxes put in         ##
##                            QuESoParameters pop-up window                             ##
##**************************************************************************************##
        
        self.viewport.goback_button.clicked.connect(self.onGoBackButton)
        self.viewport.fileBrowseButton_QuESo.clicked.connect(self.onBrowseButton_QuESodirectory)
        self.viewport.fileBrowseButton_Kratos.clicked.connect(self.onBrowseButton_Kratosdirectory)
        self.viewport.standardUse_group.toggled.connect(self.onStandardUseButton)
        self.viewport.gmshUse_group.toggled.connect(self.onGmshUseButton)
        self.viewport.visualizeButton.stateChanged.connect(self.onVisualize)
        self.viewport.button_PenaltySupport_.clicked.connect(self.onPenaltySupportBC)
        self.viewport.button_SurfaceLoad_.clicked.connect(self.onSurfaceLoadBC)
        self.viewport.SolverSettingsButton.clicked.connect(self.onSolverSettingsButton)
        cancelButton.clicked.connect(self.onCancel)
        saveButton.clicked.connect(self.onSave)

##  **************************************************************************************

##**************************************************************************************##
##      Creating the other class instances for the pop-up window to work properly       ##
##**************************************************************************************##

        #Since some of those class instances have some buttons/checkboxes that perform 
        #several tasks, their signal/slot pairs are also declared here.

        self.PenaltySupportBCBox_obj = PenaltySupportBCBox()
        self.SurfaceLoadBCBox_obj    = SurfaceLoadBCBox()
        self.projectNameWindow_obj   = projectNameWindow()
        self.SolverSettingsBox_obj   = SolverSettingsBox()

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

##  **************************************************************************************

##**************************************************************************************##
##           Creating the arrays/dictionaries that will be used in the script           ##
##**************************************************************************************##

        #The main idea is keeping track of the boudnary conditions applied.

        self.PenaltySupport_displacement_arr = []
        self.SurfaceLoad_modulus_arr         = []
        self.SurfaceLoad_force_arr           = []
        self.PenaltySupportSelectionList     = []
        self.SurfaceLoadSelectionList        = []
        self.Dirichlet_BC_icons              = {}
        self.Neumann_BC_icons                = {}
        self.PenaltySupport_faces            = []
        self.SurfaceLoad_faces               = []

##  **************************************************************************************

##**************************************************************************************##
##  Executing the dialog box, in which the project name and its directory is given by   ##
##                                       the user                                       ##
##**************************************************************************************##

        #Although our primary pop-up window is the QuESoParameters window, it is not the 
        #pop-up window that is shown to the user firstly, when the user wants to use the 
        #whole plug-in. Instead, the first pop-up window shown is the project name window
        #(which is an instance of the class 'projectNameWindow', and belongs to our primary 
        #window 'QuESoParameters' QMainWindow). The user enters the name and directory of the 
        #project. If they are not blank and the 'Ok' button is clicked on the project name 
        #window, it is checked whether the project name already exists within the directory
        #provided by the user. If yes, previous values are used to fill the relevant sections
        #in the QuESoParameters main window. If not, a blank QuESoParameters main window is
        #shown.
        
        self.projectNameWindow_obj.exec_()
        self.work_dir            = self.projectNameWindow_obj.project_dir
        self.ActiveDocument_Name = FreeCAD.ActiveDocument.Name

        if (self.projectNameWindow_obj.project_Name != "") and (self.projectNameWindow_obj.project_dir != "") and (self.projectNameWindow_obj.okFlag == True): 
            self.previousValuesCheck_QuESoKratosParam()
            self.previousValuesCheck_BC()
            self.show()
        else: 
            pass

##  **************************************************************************************

## #######################################################################################


##########################################################################################
##                                                                                      ##
##            FUNCTION DEFINITIONS OF PREVIOUS VALUE/BOUNDARY CONDITION CHECK            ##
##                                                                                      ##
##########################################################################################



##**************************************************************************************##
##      Checking the Previous Values of QuESO and Kratos Parameters (if possible)       ##
##**************************************************************************************##


    def previousValuesCheck_QuESoKratosParam(self):

## ---- Reading the directory information ------------------------------------------------

        try:
            os.chdir(self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name)
            work_dir = os.getcwd()
            with open('OtherInfos.json', 'r') as myfile:
                mydata_directory = json.load(myfile)

            kratos_dirOrg = mydata_directory['kratos_directory']
            kratos_dirOrg = kratos_dirOrg.replace("/bin/Release","")
            QuESo_dirOrg = mydata_directory['QuESo_directory']
            STL_dir = mydata_directory['STL_directory']
            self.mainObjectName = mydata_directory['mainObjectName']

            self.viewport.textInput_QuESo_.setText(QuESo_dirOrg)
            self.viewport.textInput_Kratos_.setText(kratos_dirOrg)

        except:
            pass

##  --------------------------------------------------------------------------------------

## ---- Setting Up QuESo Parameters and changing values on the pop-up screen -------------

        try:
            os.chdir(self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name)
            work_dir = os.getcwd()
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

            self.viewport.textInput_echo_.setText(echo_level)
            self.viewport.textInput_polynomialOrder_x_.setText(polynomial_order_x)
            self.viewport.textInput_polynomialOrder_y_.setText(polynomial_order_y)
            self.viewport.textInput_polynomialOrder_z_.setText(polynomial_order_z)
            self.viewport.textInput_nElements_x_.setText(number_of_elements_x)
            self.viewport.textInput_nElements_y_.setText(number_of_elements_y)
            self.viewport.textInput_nElements_z_.setText(number_of_elements_z)
            self.viewport.textInput_residual_.setText(moment_fitting_residual)
            self.viewport.popup_integration.setCurrentText(integration_method)

        except:
            pass

##  --------------------------------------------------------------------------------------

## ---- Setting Up Kratos Parameters and changing values on the pop-up screen ------------
      
        try:
            os.chdir(self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name)
            work_dir = os.getcwd()
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
            echo_level_solversettings = str(solver_settings['echo_level'])
            myfile.close()

            self.SolverSettingsBox_obj.popup_parallel_type_.setCurrentText(parallel_type)
            self.SolverSettingsBox_obj.popup_echo_level2_.setCurrentText(echo_level_problemdata)
            self.SolverSettingsBox_obj.textInput_start_time_.setText(start_time)
            self.SolverSettingsBox_obj.textInput_end_time_.setText(end_time)
            self.SolverSettingsBox_obj.popup_solver_type_.setCurrentText(solver_type)
            self.SolverSettingsBox_obj.popup_analysis_type_.setCurrentText(analysis_type)
            self.SolverSettingsBox_obj.popup_echo_level3_.setCurrentText(echo_level_solversettings)

        except:
            pass

##  --------------------------------------------------------------------------------------

## ---- Setting Up Structural Materials Parameters and changing values on the pop-up screen ----

        try:
            os.chdir(self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name)
            work_dir = os.getcwd()
            with open('StructuralMaterials.json', 'r') as myfile:
                mydata_StMat = json.load(myfile)

            # Reading properties
            properties = mydata_StMat['properties']

            properties_id = str(properties[0]['properties_id'])
            Material = properties[0]['Material']
            consitutive_law = Material['constitutive_law']
            name_constLaw = str(consitutive_law['name'])
            Variables = Material['Variables']
            density = str(Variables['DENSITY'])
            young_modulus = str(Variables['YOUNG_MODULUS'])
            poisson_ratio = str(Variables['POISSON_RATIO'])
            myfile.close()

            self.SolverSettingsBox_obj.textInput_properties_id_.setText(properties_id)
            self.SolverSettingsBox_obj.popup_constitutive_id_.setCurrentText(name_constLaw)
            self.SolverSettingsBox_obj.textInput_density_.setText(density)
            self.SolverSettingsBox_obj.textInput_young_modulus_.setText(young_modulus)
            self.SolverSettingsBox_obj.textInput_poisson_ratio_.setText(poisson_ratio)

        except:
            pass

##  --------------------------------------------------------------------------------------

##  **************************************************************************************
        
##**************************************************************************************##
##                      Checking the previous boundary conditions                       ##
##**************************************************************************************##

    def previousValuesCheck_BC(self):

        try:
            os.chdir(self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name)
            work_dir = os.getcwd()
            with open('QuESoParameters.json', 'r') as myfile:
                mydata_QuESo = json.load(myfile)

            conditions = mydata_QuESo['conditions']
            
            for member in conditions:
                if('SurfaceLoadCondition' in member):
                    self.SurfaceLoad_force_arr.append(member['SurfaceLoadCondition']['direction'])
                    self.SurfaceLoad_modulus_arr.append(member['SurfaceLoadCondition']['modulus'])
                
                elif('PenaltySupportCondition' in member):
                    self.PenaltySupport_displacement_arr.append(member['PenaltySupportCondition']['value'])

            myfile.close()

            with open('OtherInfos.json', 'r') as myfile:
                mydata_OtherInfos = json.load(myfile)

            for member_OtherInfos in mydata_OtherInfos:
                if ('SurfaceLoadFaces' in member_OtherInfos):
                    for idx, member_SurfaceLoadFaces in enumerate(mydata_OtherInfos['SurfaceLoadFaces']):
                        self.SurfaceLoad_faces.append(member_SurfaceLoadFaces)
                        self.SurfaceLoadFacesList_Obj.listwidget.addItem(member_SurfaceLoadFaces)
                        Gui.Selection.addSelection(FreeCAD.ActiveDocument.Name, self.mainObjectName, member_SurfaceLoadFaces)
                        sel = Gui.Selection.getSelectionEx()
                        self.SurfaceLoadSelectionList.append(sel)
                        #Loop over all vertices			
                        for sel in Gui.Selection.getSelectionEx('', 0):
                            for path in sel.SubElementNames if sel.SubElementNames else ['']:
                                shape = sel.Object.getSubObject(path)

			                    #Calculating vector components
                                neuVector = FreeCAD.Vector(float(self.SurfaceLoad_force_arr[idx][0]),float(self.SurfaceLoad_force_arr[idx][1]),float(self.SurfaceLoad_force_arr[idx][2]))
                                exeptVector = FreeCAD.Vector(0.00,0.00,-1.00)
                                vX = FreeCAD.Vector(1,0,0)
                                vY = FreeCAD.Vector(0,1,0)
                                vZ = FreeCAD.Vector(0,0,1)

                                axis1 = FreeCAD.Vector.cross(vX, neuVector)
                                axis2 = FreeCAD.Vector.cross(vY, neuVector)
                                axis3 = FreeCAD.Vector.cross(vZ, neuVector)
    
			                    #Calculating angles between main vector and origin
                                angle1 = math.degrees(vX.getAngle(neuVector))
                                angle2 = math.degrees(vY.getAngle(neuVector))
                                angle3 = math.degrees(vZ.getAngle(neuVector))

                                iconNeu = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Neumann BC_" + member_SurfaceLoadFaces)
                                n = 1 
			                    #Loop over all vertices
                                for i in [v.Point for v in shape.Vertexes]:
                                
                                    #Creating icons
                                    bcTip = FreeCAD.ActiveDocument.addObject("Part::Cone")
                                    bcTip.Height = 7.5	
                                    bcTip.Radius1 = 2
                                    bcTip.Radius2 = 0
                                    bcTip.Label = "_bcTip_" + str(n)

                                    bcTip.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, -7.5),FreeCAD.Rotation(0, 0, 0))
                                    bcCyl = FreeCAD.ActiveDocument.addObject("Part::Cone")
                                    bcCyl.Height = 7.5
                                    bcCyl.Radius1 = 1.1
                                    bcCyl.Radius2 = 1.0

                                    bcCyl.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, -15.0), FreeCAD.Rotation(0, 0, 0))
                                    bcCyl.Label = "_bcCyl_" + str(n)
                                    FreeCAD.ActiveDocument.recompute()

                                    fusion_arrow = FreeCAD.ActiveDocument.addObject("Part::MultiFuse", "Part::MultiFuse" + member_SurfaceLoadFaces + str(n))
                                    fusion_arrow.Shapes = [bcTip, bcCyl]
                                    FreeCAD.ActiveDocument.recompute()
                                    fusion_arrow.Label = "Neumann_BC_" + member_SurfaceLoadFaces + "_" + str(n)
    
				                    #Orienting and locating icone into vertex
                                    fusion_arrow.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis1,angle1))
                                    fusion_arrow.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis2,180 - angle2))
                                    fusion_arrow.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis3,angle3))
                                    if neuVector == exeptVector:
                                        fusion_arrow.Placement = FreeCAD.Placement(i,FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                                    else:
                                        fusion_arrow.Placement = FreeCAD.Placement(i,FreeCAD.Rotation(axis3,angle3))

                                    Gui.ActiveDocument.getObject("Part__MultiFuse" + member_SurfaceLoadFaces + str(n)).Selectable = False
                                    Gui.ActiveDocument.getObject("Part__MultiFuse" + member_SurfaceLoadFaces + str(n)).ShowInTree = True
                                    Gui.ActiveDocument.getObject("Part__MultiFuse" + member_SurfaceLoadFaces + str(n)).ShapeColor = (0.0,0.0,1.0)

                                    FreeCAD.ActiveDocument.recompute()
    
				                    #Adding icon's label on list
                                    iconNeu.addObject(fusion_arrow)        
                                    n +=1

                        self.Neumann_BC_icons.update({str(member_SurfaceLoadFaces): str(n)})
                        Gui.Selection.clearSelection()

                elif ('PenaltySupportFaces' in member_OtherInfos):
                    for member_PenaltySupportFaces in mydata_OtherInfos['PenaltySupportFaces']:
                        self.PenaltySupport_faces.append(member_PenaltySupportFaces)
                        self.PenaltySupportFacesList_Obj.listwidget.addItem(member_PenaltySupportFaces)
                        Gui.Selection.addSelection(FreeCAD.ActiveDocument.Name, self.mainObjectName, member_PenaltySupportFaces)
                        sel = Gui.Selection.getSelectionEx()
                        self.PenaltySupportSelectionList.append(sel)
                        n = 1 
                        for sel in Gui.Selection.getSelectionEx('', 0): 
                            for path in sel.SubElementNames if sel.SubElementNames else ['']:
                                shape = sel.Object.getSubObject(path)                          
                                iconDir = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Dirichlet BC_" + member_PenaltySupportFaces)

			                    #Loop over all vertices
                                for i in [v.Point for v in shape.Vertexes]:

                                    # i <- coordinates of vertex
                                    #Calculating normals:
                                    sub = sel.SubObjects[0]
                                    suv = sub.Surface.parameter(i)
                                    snv = sub.normalAt(suv[0], suv[1]).normalize()

                                    pnt = sel.PickedPoints[0]
                                    sub = sel.SubObjects[0]
                                    u, v = sub.Surface.parameter(pnt)
                                    nv = sub.Surface.normal(u,v)

                                    #Defining base axes
                                    vX = FreeCAD.Vector(1,0,0)
                                    vY = FreeCAD.Vector(0,1,0)
                                    vZ = FreeCAD.Vector(0,0,1)
    
				                    #Defining rotation axes
                                    axis1 = FreeCAD.Vector.cross(vX,snv)
                                    axis2 = FreeCAD.Vector.cross(vY,snv)
                                    axis3 = FreeCAD.Vector.cross(vZ,snv)
    
				                    #Calculating rotation angles:
                                    angle1 = math.degrees(vX.getAngle(snv))
                                    angle2 = math.degrees(vY.getAngle(snv))
                                    angle3 = math.degrees(vZ.getAngle(snv))

                                    #Creating icons:
                                    bcCone = FreeCAD.ActiveDocument.addObject("Part::Cone")
                                    bcCone.Height = 5	
                                    bcCone.Radius1 = 0
                                    bcCone.Radius2 = 2
                                    bcCone.Label = "_bcCone_" + str(n)

                                    bcBox = FreeCAD.ActiveDocument.addObject("Part::Box")
                                    bcBox.Height = 1
                                    bcBox.Length = 5
                                    bcBox.Width = 5
                                    bcBox.Label = "_bcBox_" + str(n)

                                    bcBox.Placement = FreeCAD.Placement(FreeCAD.Vector(-2.5, -2.5, 5.0),FreeCAD.Rotation(0, 0, 0), FreeCAD.Vector(0, 0, 0))
                                    FreeCAD.ActiveDocument.recompute()

                                    fusion = FreeCAD.ActiveDocument.addObject("Part::MultiFuse", "Part::MultiFuse" + member_PenaltySupportFaces + str(n))
                                    fusion.Shapes = [bcCone, bcBox]
    
				                    #Orienting and locating icone into vertex
                                    fusion.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis1, angle1))
                                    fusion.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis2, angle2))
                                    fusion.Placement = FreeCAD.Placement(i + FreeCAD.Vector(0, 0, 0),FreeCAD.Rotation(axis3,  angle3))
                                    FreeCAD.ActiveDocument.recompute()
    
				                    #Adding icon's label on list
                                    fusion.Label = "Dirichlet_BC_" + member_PenaltySupportFaces + "_" + str(n)
                                    Gui.ActiveDocument.getObject("Part__MultiFuse" + member_PenaltySupportFaces + str(n)).Selectable = False
                                    Gui.ActiveDocument.getObject("Part__MultiFuse" + member_PenaltySupportFaces + str(n)).ShowInTree = True
                                    Gui.ActiveDocument.getObject("Part__MultiFuse" + member_PenaltySupportFaces + str(n)).ShapeColor = (1.0,0.0,0.0)
                                    FreeCAD.ActiveDocument.recompute()

                                    iconDir.addObject(fusion)
                                    n +=1

		                #Adding icon to component list
                        self.Dirichlet_BC_icons.update({str(member_PenaltySupportFaces): str(n)})
                        Gui.Selection.clearSelection()

        except:
            pass

##  **************************************************************************************
        
##  ######################################################################################
        
##########################################################################################
##                                                                                      ##
##   SIGNAL/SLOT FUNCTIONS FOR THE BUTTONS AND CHECKBOXES ON THE QuESoParameters MAIN   ##
##                         WINDOW (EXCEPT Ok and Cancel Button)                         ##
##                                                                                      ##
##########################################################################################

## ---- Go back button from QuESoParameters main window to the Project Name and Directory Dialog Box ----

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

##  --------------------------------------------------------------------------------------

## ---- Selecting between Gmsh or FreeCAD's Standard Mesher (Exclusive Group Box Objects) ----

    def onStandardUseButton(self):
        if self.viewport.standardUse_group.isChecked():
            self.viewport.gmshUse_group.setChecked(False)

    def onGmshUseButton(self):
        if self.viewport.gmshUse_group.isChecked():
            self.viewport.standardUse_group.setChecked(False)

##  --------------------------------------------------------------------------------------

## ---- Browse Files to set up the directory of QuESo and Kratos -------------------------

    def onBrowseButton_QuESodirectory(self):
        self.QuESo_directory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.work_dir, QtGui.QFileDialog.ShowDirsOnly)
        self.viewport.textInput_QuESo_.setText(self.QuESo_directory)
        self.QuESo_lib_directory = self.QuESo_directory + '/libs'
    
    def onBrowseButton_Kratosdirectory(self):
        self.Kratos_directory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.work_dir, QtGui.QFileDialog.ShowDirsOnly)
        self.viewport.textInput_Kratos_.setText(self.Kratos_directory)
        self.Kratos_directory = self.Kratos_directory + '/bin/Release'
        self.Kratos_lib_directory = self.Kratos_directory + '/libs'

##  --------------------------------------------------------------------------------------

## ---- Apply Boundary Condition buttons -------------------------------------------------

    #The lines involving self.callback = ... enable FreeCAD to keep track of that where 
    #is clicked (which coordinates, edge, line etc.) by the user. It activates recognizing
    #the mouse button events by FreeCAD.

    def onPenaltySupportBC(self):
        infoBox = QtGui.QMessageBox.information(self, "Apply PenaltySupport Boundary Conditions", \
                                                "Please select faces subject to PenaltySupport BC one by one!")

        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_PenaltySupportBCBox)
            self.setVisible(False)
            self.PenaltySupportFacesList_Obj.show()

    def onSurfaceLoadBC(self):
        infoBox = QtGui.QMessageBox.information(self, "Apply SurfaceLoad Boundary Conditions", \
                                                "Please select faces subject to SurfaceLoad BC one by one!")

        if infoBox == QtGui.QMessageBox.StandardButton.Ok:
            self.view = Gui.ActiveDocument.ActiveView
            self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick_SurfaceLoadBCBox)
            self.setVisible(False)
            self.SurfaceLoadFacesList_Obj.show()

##  --------------------------------------------------------------------------------------

## ---- The pop-up window (an object of QuESoParameters main window still) to set up Solver Settings ----

    def onSolverSettingsButton(self):

        self.SolverSettingsBox_obj.exec_()

##  --------------------------------------------------------------------------------------
        
## ---- Visualizing the bounding box grids -----------------------------------------------

    #Visualizing/devisualizing grids uses a function called 'VisualizeGrid_Fun' and 
    #'deVisualizeGrid_Fun'. Their definition is given in the Supplementary Functions Section. 
    #(At the end of methods of QuESoParameters main window)

    def onVisualize(self):
            
            if (self.viewport.visualizeButton.isChecked()):
                self.VisualizeGrid_Fun()
            else:
                self.deVisualizeGrid_Fun()

##  --------------------------------------------------------------------------------------
            
##  ######################################################################################

##########################################################################################
##                                                                                      ##
##   PenaltySupportFacesList CLASS INSTANCE'S FUNCTIONS THAT INVOLVE AT AN ACTION OF    ##
##                             QuESoParameters MAIN WINDOW                              ##
##                                                                                      ##
##########################################################################################
            
## ---- To confirm the applied penalty support boundary conditions and their values ------

    def okButtonClicked_PenaltySupportFacesList(self):

        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.PenaltySupportFacesList_Obj.result = True
        self.PenaltySupportFacesList_Obj.close()

##  --------------------------------------------------------------------------------------

## ---- To completely discard all the penalty support boundary conditions applied (Face IDs and values) ----

    def DiscardButtonClicked_PenaltySupportFacesList(self):

        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.PenaltySupportFacesList_Obj.result = False
        self.PenaltySupport_displacement_arr = []
        self.PenaltySupport_faces = []
        self.PenaltySupportSelectionList = []
        self.PenaltySupportFacesList_Obj.close()

##  --------------------------------------------------------------------------------------

## ---- To delete the penalty support boundary condition selected on the list ------------

    def DeleteButtonClicked_PenaltySupportFacesList(self):

        current_Item = self.PenaltySupportFacesList_Obj.listwidget.currentItem()
        current_Item_text = self.PenaltySupportFacesList_Obj.listwidget.currentItem().text()
        indexToDel = self.PenaltySupportFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        k = self.Dirichlet_BC_icons[current_Item_text]
        for i in range (1, int(k), 1):
            obj  = FreeCAD.ActiveDocument.getObjectsByLabel("Dirichlet_BC_" + str(current_Item_text) + "_" + str(i))
            OpenSCADUtils.removesubtree(obj)
        else:
            pass
        FreeCAD.ActiveDocument.removeObject('Dirichlet_BC_' + current_Item_text)
        self.Dirichlet_BC_icons.pop(str(current_Item_text))
        del self.PenaltySupport_displacement_arr[indexToDel]
        del self.PenaltySupport_faces[indexToDel]
        del self.PenaltySupportSelectionList[indexToDel]
        self.PenaltySupportFacesList_Obj.listwidget.takeItem(self.PenaltySupportFacesList_Obj.listwidget.row(current_Item))

##  --------------------------------------------------------------------------------------
        
## ---- To modify the value of the penalty support boundary condition selected on the list ----

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
        
##  --------------------------------------------------------------------------------------
        
##  ######################################################################################

##########################################################################################
##                                                                                      ##
##     SurfaceLoadFacesList CLASS INSTANCE'S FUNCTIONS THAT INVOLVE AT AN ACTION OF     ##
##                             QuESoParameters MAIN WINDOW                              ##
##                                                                                      ##
##########################################################################################
        
## ---- To confirm the applied surface load boundary conditions and their values ---------


    def okButtonClicked_SurfaceLoadFacesList(self):

        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.SurfaceLoadFacesList_Obj.result = True
        self.SurfaceLoadFacesList_Obj.close()

##  --------------------------------------------------------------------------------------

## ---- To completely discard all the surface load boundary conditions applied (Face IDs and values) ----


    def DiscardButtonClicked_SurfaceLoadFacesList(self):

        self.setVisible(True)
        self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)
        self.SurfaceLoadFacesList_Obj.result = False
        self.SurfaceLoad_force_arr = []
        self.SurfaceLoad_faces = []
        self.SurfaceLoad_modulus_arr=[]
        self.SurfaceLoadSelectionList = []
        self.SurfaceLoadFacesList_Obj.close()

##  --------------------------------------------------------------------------------------

## ---- To delete the penalty surface load condition selected on the list ----------------

    def DeleteButtonClicked_SurfaceLoadFacesList(self):

        current_Item = self.SurfaceLoadFacesList_Obj.listwidget.currentItem()
        current_Item_text = self.SurfaceLoadFacesList_Obj.listwidget.currentItem().text()
        indexToDel = self.SurfaceLoadFacesList_Obj.listwidget.indexFromItem(current_Item).row()
        k = self.Neumann_BC_icons[current_Item_text]
        for i in range (1, int(k), 1):
            obj  = FreeCAD.ActiveDocument.getObjectsByLabel("Neumann_BC_" + str(current_Item_text) + "_" + str(i))
            OpenSCADUtils.removesubtree(obj)
        else:
            pass
        FreeCAD.ActiveDocument.removeObject('Neumann_BC_' + current_Item_text)
        self.Neumann_BC_icons.pop(str(current_Item_text))
        del self.SurfaceLoad_force_arr[indexToDel]
        del self.SurfaceLoad_modulus_arr[indexToDel]
        del self.SurfaceLoad_faces[indexToDel]
        del self.SurfaceLoadSelectionList[indexToDel]
        self.SurfaceLoadFacesList_Obj.listwidget.takeItem(self.SurfaceLoadFacesList_Obj.listwidget.row(current_Item))

##  --------------------------------------------------------------------------------------

## ---- To modify the penalty surface load condition selected on the list ----------------

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
        self.SurfaceLoad_modulus_arr[indexToMod] = float(self.SurfaceLoadBCBox_obj.modulus_val)
        Gui.Selection.clearSelection()

##  --------------------------------------------------------------------------------------

##  ######################################################################################

##########################################################################################
##                                                                                      ##
##   PENALTY SUPPORT MOUSE CLICK EVENT- Getting the coordinate of where the mouse is    ##
##                 clicked to apply penalty support boundary condition                  ##
##                                                                                      ##
##########################################################################################

    def getMouseClick_PenaltySupportBCBox(self, event_cb):
        event = event_cb.getEvent()

##**************************************************************************************##
##  Getting the coordinate of the mouse click and asking the user to enter the penalty  ##
## support boundary condition value - Storing the Face IDs and corresponding values     ## 
##**************************************************************************************##

        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) \
        &  (Gui.Selection.hasSelection() == False) & (event.getState() == coin.SoMouseButtonEvent.DOWN):
            pos = event.getPosition().getValue()
            element_list = Gui.ActiveDocument.ActiveView.getObjectInfo((int(pos[0]), int(pos[1])))
            if(element_list != None):
                self.PenaltySupportBCBox_obj.okButton_Flag = False
                self.PenaltySupportBCBox_obj.exec_()
                if(self.PenaltySupportBCBox_obj.okButton_Flag):
                    self.PenaltySupport_displacement_arr.append(\
                                                                [float(self.PenaltySupportBCBox_obj.x_val), \
                                                                 float(self.PenaltySupportBCBox_obj.y_val), \
                                                                 float(self.PenaltySupportBCBox_obj.z_val)])
                    self.PenaltySupportFacesList_Obj.listwidget.addItem(element_list.get('Component'))

                    Gui.Selection.addSelection(element_list.get('Document'), element_list.get('Object'), \
                                               element_list.get('Component'), element_list.get('x'), element_list.get('y'))
                    sel = Gui.Selection.getSelectionEx()
                    self.PenaltySupportSelectionList.append(sel)
                    self.PenaltySupport_faces.append(element_list['Component'])
                    self.mainObjectName = element_list['Object']

##  **************************************************************************************
                                        
##**************************************************************************************##
##   Preprocessing Icons to visualize them on the model for Penalty Support Boundary    ##
##                                      Condition                                       ##
##**************************************************************************************##
                    
                    n = 1 
                    for sel in Gui.Selection.getSelectionEx('', 0): 
                        for path in sel.SubElementNames if sel.SubElementNames else ['']:
                            shape = sel.Object.getSubObject(path)                          
                            iconDir = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Dirichlet BC_" + element_list.get('Component'))

			                #Loop over all vertices
                            for i in [v.Point for v in shape.Vertexes]:

                                # i <- coordinates of vertex
                                #Calculating normals:
                                sub = sel.SubObjects[0]
                                suv = sub.Surface.parameter(i)
                                snv = sub.normalAt(suv[0], suv[1]).normalize()

                                pnt = sel.PickedPoints[0]
                                sub = sel.SubObjects[0]
                                u, v = sub.Surface.parameter(pnt)
                                nv = sub.Surface.normal(u,v)

                                #Defining base axes
                                vX = FreeCAD.Vector(1,0,0)
                                vY = FreeCAD.Vector(0,1,0)
                                vZ = FreeCAD.Vector(0,0,1)
				    
				                #Defining rotation axes
                                axis1 = FreeCAD.Vector.cross(vX,snv)
                                axis2 = FreeCAD.Vector.cross(vY,snv)
                                axis3 = FreeCAD.Vector.cross(vZ,snv)
				    
				                #Calculating rotation angles:
                                angle1 = math.degrees(vX.getAngle(snv))
                                angle2 = math.degrees(vY.getAngle(snv))
                                angle3 = math.degrees(vZ.getAngle(snv))

                                #Creating icons:
                                bcCone = FreeCAD.ActiveDocument.addObject("Part::Cone")
                                bcCone.Height = 5	
                                bcCone.Radius1 = 0
                                bcCone.Radius2 = 2
                                bcCone.Label = "_bcCone_" + str(n)

                                bcBox = FreeCAD.ActiveDocument.addObject("Part::Box")
                                bcBox.Height = 1
                                bcBox.Length = 5
                                bcBox.Width = 5
                                bcBox.Label = "_bcBox_" + str(n)

                                bcBox.Placement = FreeCAD.Placement(FreeCAD.Vector(-2.5, -2.5, 5.0),FreeCAD.Rotation(0, 0, 0), FreeCAD.Vector(0, 0, 0))
                                FreeCAD.ActiveDocument.recompute()
                                
                                fusion = FreeCAD.ActiveDocument.addObject("Part::MultiFuse", "Part::MultiFuse" + element_list.get('Component') + str(n))
                                fusion.Shapes = [bcCone, bcBox]
				
				                #Orienting and locating icone into vertex
                                fusion.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis1, angle1))
                                fusion.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis2, angle2))
                                fusion.Placement = FreeCAD.Placement(i + FreeCAD.Vector(0, 0, 0),FreeCAD.Rotation(axis3,  angle3))
                                FreeCAD.ActiveDocument.recompute()
				    
				                #Adding icon's label on list
                                fusion.Label = "Dirichlet_BC_" + element_list.get('Component') + "_" + str(n)
                                Gui.ActiveDocument.getObject("Part__MultiFuse" + element_list.get('Component') + str(n)).Selectable = False
                                Gui.ActiveDocument.getObject("Part__MultiFuse" + element_list.get('Component') + str(n)).ShowInTree = True
                                Gui.ActiveDocument.getObject("Part__MultiFuse" + element_list.get('Component') + str(n)).ShapeColor = (1.0,0.0,0.0)
                                FreeCAD.ActiveDocument.recompute()

                                iconDir.addObject(fusion)
                                n +=1
                                
		            #Adding icon to component list
                    self.Dirichlet_BC_icons.update({str(element_list.get('Component')): str(n)})
                    Gui.Selection.clearSelection()

##  **************************************************************************************

##  ######################################################################################

##########################################################################################
##                                                                                      ##
##     SURFACE LOAD MOUSE CLICK EVENT- Getting the coordinate of where the mouse is     ##
##                   clicked to apply surface load boundary condition                   ##
##                                                                                      ##
##########################################################################################

    def getMouseClick_SurfaceLoadBCBox(self, event_cb):
        event = event_cb.getEvent()

##**************************************************************************************##
##                                                                                      ##
##  Getting the coordinate of the mouse click and asking the user to enter the penalty  ##
## support boundary condition value - Storing the Face IDs and corresponding values in  ##
##                                     a dictionary                                     ##
##                                                                                      ##
##**************************************************************************************##

        if (coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.BUTTON1) == True) \
        &  (Gui.Selection.hasSelection() == False) & (event.getState() == coin.SoMouseButtonEvent.DOWN):
            pos = event.getPosition().getValue()
            element_list = Gui.ActiveDocument.ActiveView.getObjectInfo((int(pos[0]), int(pos[1])))
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
                    self.SurfaceLoadFacesList_Obj.listwidget.addItem(element_list.get('Component'))

                    Gui.Selection.addSelection(element_list.get('Document'), element_list.get('Object'), \
                                               element_list.get('Component'), element_list.get('x'), element_list.get('y'))
                    sel = Gui.Selection.getSelectionEx()
                    self.SurfaceLoadSelectionList.append(sel)
                    self.SurfaceLoad_faces.append(element_list['Component'])
                    self.mainObjectName = element_list['Object']

##  **************************************************************************************
                                        
##**************************************************************************************##
##   Preprocessing Icons to visualize them on the model for Surface load Boundary       ##
##                                      Condition                                       ##
##**************************************************************************************##
		            #Loop over all vertices			
                    for sel in Gui.Selection.getSelectionEx('', 0):
                        for path in sel.SubElementNames if sel.SubElementNames else ['']:
                            shape = sel.Object.getSubObject(path)
				
			                #Calculating vector components
                            neuVector = FreeCAD.Vector(float(self.SurfaceLoadBCBox_obj.x_val),float(self.SurfaceLoadBCBox_obj.y_val),float(self.SurfaceLoadBCBox_obj.z_val))
                            exeptVector = FreeCAD.Vector(0.00,0.00,-1.00)
                            vX = FreeCAD.Vector(1,0,0)
                            vY = FreeCAD.Vector(0,1,0)
                            vZ = FreeCAD.Vector(0,0,1)

                            axis1 = FreeCAD.Vector.cross(vX, neuVector)
                            axis2 = FreeCAD.Vector.cross(vY, neuVector)
                            axis3 = FreeCAD.Vector.cross(vZ, neuVector)
				
			                #Calculating angles between main vector and origin
                            angle1 = math.degrees(vX.getAngle(neuVector))
                            angle2 = math.degrees(vY.getAngle(neuVector))
                            angle3 = math.degrees(vZ.getAngle(neuVector))

                            iconNeu = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Neumann BC_" + element_list.get('Component'))
                            n = 1 
			                #Loop over all vertices
                            for i in [v.Point for v in shape.Vertexes]:
				    
                                #Creating icons
                                bcTip = FreeCAD.ActiveDocument.addObject("Part::Cone")
                                bcTip.Height = 7.5	
                                bcTip.Radius1 = 2
                                bcTip.Radius2 = 0
                                bcTip.Label = "_bcTip_" + str(n)
                            
                                bcTip.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, -7.5),FreeCAD.Rotation(0, 0, 0))
                                bcCyl = FreeCAD.ActiveDocument.addObject("Part::Cone")
                                bcCyl.Height = 7.5
                                bcCyl.Radius1 = 1.1
                                bcCyl.Radius2 = 1.0

                                bcCyl.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, -15.0), FreeCAD.Rotation(0, 0, 0))
                                bcCyl.Label = "_bcCyl_" + str(n)
                                FreeCAD.ActiveDocument.recompute()
                                
                                fusion_arrow = FreeCAD.ActiveDocument.addObject("Part::MultiFuse", "Part::MultiFuse" + element_list.get('Component') + str(n))
                                fusion_arrow.Shapes = [bcTip, bcCyl]
                                FreeCAD.ActiveDocument.recompute()
                                fusion_arrow.Label = "Neumann_BC_" + element_list.get('Component') + "_" + str(n)
				    
				                #Orienting and locating icone into vertex
                                fusion_arrow.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis1,angle1))
                                fusion_arrow.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis2,180 - angle2))
                                fusion_arrow.Placement = FreeCAD.Placement(FreeCAD.Vector(0.00,0.00,0.00),FreeCAD.Rotation(axis3,angle3))
                                if neuVector == exeptVector:
                                    fusion_arrow.Placement = FreeCAD.Placement(i,FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                                else:
                                    fusion_arrow.Placement = FreeCAD.Placement(i,FreeCAD.Rotation(axis3,angle3))

                                Gui.ActiveDocument.getObject("Part__MultiFuse" + element_list.get('Component') + str(n)).Selectable = False
                                Gui.ActiveDocument.getObject("Part__MultiFuse" + element_list.get('Component') + str(n)).ShowInTree = True
                                Gui.ActiveDocument.getObject("Part__MultiFuse" + element_list.get('Component') + str(n)).ShapeColor = (0.0,0.0,1.0)

                                FreeCAD.ActiveDocument.recompute()
				    
				                #Adding icon's label on list
                                iconNeu.addObject(fusion_arrow)        
                                n +=1

                    self.Neumann_BC_icons.update({str(element_list.get('Component')): str(n)})
                    Gui.Selection.clearSelection()

##  **************************************************************************************
                    
##  ######################################################################################
                    
##########################################################################################
##                                                                                      ##
##             TASKS DONE BY THE SAVE BUTTON ON QuESoParameters MAIN WINDOW             ##
##                                                                                      ##
##########################################################################################

    def onSave(self):

##**************************************************************************************##
##                                Error Handling Section                                ##
##**************************************************************************************##

## ---- Error Handling for QuESo Parameters Main Window ----------------------------------

        if (self.viewport.standardUse_group.isChecked() == False) & (self.viewport.gmshUse_group.isChecked() == False):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "No mesher type selected!\n\nYou must select a mesher type!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
        
        elif (self.viewport.gmshUse_group.isChecked() == True):
            try:
                import gmsh
                self.gmsh_use_flag = True
            except:
                print("You must install Gmsh to your computer by 'pip install --upgrade gmsh' to use it!")

            if not (self.viewport.maxElSize_textInput.text()):
                errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Max. Element Size is left blank!\n\nWhen you choose to use Gmsh mesher, please make sure to enter the max. element size as well!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                if errorMsg == QtGui.QMessageBox.Ok:
                    return
                
            if not (self.viewport.minElSize_textInput.text()):
                errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Min. Element Size is left blank!\n\nWhen you choose to use Gmsh mesher, please make sure to enter the min. element size as well!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                if errorMsg == QtGui.QMessageBox.Ok:
                    return
            
        elif (self.viewport.standardUse_group.isChecked() == True):
            self.gmsh_use_flag = False

            if not (self.viewport.surface_deviation_textInput.text()):
                errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Surface Deviation is left blank!\n\nWhen you choose to use FreeCAD's Standard mesher, please make sure to enter the surface deviation value as well!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                if errorMsg == QtGui.QMessageBox.Ok:
                    return
                
            if not (self.viewport.angular_deviation_textInput.text()):
                errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Angular Deviation is left blank!\n\nWhen you choose to use FreeCAD's Standard mesher, please make sure to enter the angular deviation value as well!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                if errorMsg == QtGui.QMessageBox.Ok:
                    return
                

        if not (self.viewport.textInput_QuESo_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Directory of QuESo is left blank!\n\nPlease make sure to give the directory of QuESo!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.viewport.textInput_Kratos_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Directory of Kratos is left blank!\n\nPlease make sure to give the directory of Kratos!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.viewport.textInput_echo_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Echo level is left blank!\n\nPlease make sure to enter the value of the echo level!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.viewport.textInput_polynomialOrder_x_.text() and self.viewport.textInput_polynomialOrder_y_.text() and self.viewport.textInput_polynomialOrder_z_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "At least one polynomial order box is left blank!\n\nPlease make sure to enter a value for the polynomial order of x, y and z!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.viewport.textInput_nElements_x_.text() and self.viewport.textInput_nElements_y_.text() and self.viewport.textInput_nElements_z_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "At least one number of elements box is left blank!\n\nPlease make sure to enter a value for the number of elements along x, y and z!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.viewport.textInput_residual_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in QuESo Parameters", "Moment fitting residual is left blank!\n\nPlease make sure to enter a value for the moment fitting residual!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
##  --------------------------------------------------------------------------------------
            
## ---- Error Handling for Kratos Solver Settings Main Window ----------------------------
            
        if not (self.SolverSettingsBox_obj.textInput_start_time_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in Kratos Solver Settings", "Start time is left blank!\n\nPlease make sure to enter a value for the start time!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.SolverSettingsBox_obj.textInput_end_time_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in Kratos Solver Settings", "End time is left blank!\n\nPlease make sure to enter a value for the end time!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            

        if not (self.SolverSettingsBox_obj.textInput_density_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in Kratos Solver Settings", "Density is left blank!\n\nPlease make sure to enter a value for the density!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
            
        if not (self.SolverSettingsBox_obj.textInput_young_modulus_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in Kratos Solver Settings", "Young Modulus is left blank!\n\nPlease make sure to enter a value for the Young Modulus!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            

        if not (self.SolverSettingsBox_obj.textInput_poisson_ratio_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in Kratos Solver Settings", "Poisson Ratio is left blank!\n\nPlease make sure to enter a value for the Poisson Ratio!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            

        if not (self.SolverSettingsBox_obj.textInput_properties_id_.text()):
            errorMsg = QtGui.QMessageBox.critical(self, "Error in Kratos Solver Settings", "Properties ID is left blank!\n\nPlease make sure to enter a value for the Properties ID!", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if errorMsg == QtGui.QMessageBox.Ok:
                return
            
##  --------------------------------------------------------------------------------------
    
##  **************************************************************************************

        reply = QtGui.QMessageBox.question(self, "QuESo Parameters", "Upon Yes, all files related to the project will be saved. \n \n"
                                           "Are you sure you want to continue?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply ==  QtGui.QMessageBox.No:
            pass

        elif reply == QtGui.QMessageBox.Yes:

##**************************************************************************************##
##    Creating Project (if they don't already exist) and data directories as well as    ##
##                     changing the working directory of the script                     ##
##**************************************************************************************##

            os.chdir(self.work_dir)

            if os.path.isdir(os.getcwd() + "/" + self.projectNameWindow_obj.project_Name):
                self.work_dir = os.getcwd() + "/" + self.projectNameWindow_obj.project_Name
                os.chdir(self.work_dir)
            
            else:
                os.mkdir(os.getcwd() + "/" + self.projectNameWindow_obj.project_Name)
                self.work_dir = os.getcwd() + "/" + self.projectNameWindow_obj.project_Name
                os.chdir(self.work_dir)

            if os.path.isdir(os.getcwd() + "/data"):
                shutil.rmtree(os.getcwd() + "/data")
            
            os.mkdir(os.getcwd() + "/data")
            
            self.data_dir = os.getcwd() + "/data"

            temp_name = FreeCAD.ActiveDocument.Name
            FreeCAD.getDocument(temp_name).saveAs(self.work_dir + "/" + self.projectNameWindow_obj.project_Name + ".FCStd")

            #Step directory is needed in case the user wants to use Gmsh mesher
            self.STL_directory = self.data_dir + "/" + self.projectNameWindow_obj.project_Name + ".stl"
            self.step_directory = self.data_dir + "/" + self.projectNameWindow_obj.project_Name + ".step"

## **************************************************************************************
            
##**************************************************************************************##
##                        Bounding Box with 0.1 offset in total                         ##
##**************************************************************************************##

            mybounds=self.bounds()
            self.lowerbound_x_=mybounds[0]-(abs(mybounds[0]-mybounds[3]))*0.05
            self.lowerbound_y_=mybounds[1]-(abs(mybounds[1]-mybounds[4]))*0.05
            self.lowerbound_z_=mybounds[2]-(abs(mybounds[2]-mybounds[5]))*0.05
            self.upperbound_x_=mybounds[3]+(abs(mybounds[0]-mybounds[3]))*0.05
            self.upperbound_y_=mybounds[4]+(abs(mybounds[1]-mybounds[4]))*0.05
            self.upperbound_z_=mybounds[5]+(abs(mybounds[2]-mybounds[5]))*0.05

## **************************************************************************************
            
##**************************************************************************************##
##          Creating QuESoParameters.json file and Exporting surface STL files          ##
##**************************************************************************************##

            QuESoParam = \
            {

                "general_settings"   : {
                    "input_filename"  :  self.STL_directory,
                    "echo_level"      :  int(self.viewport.textInput_echo_.text())
                },
                "mesh_settings"     : {
                    "lower_bound_xyz": list([self.lowerbound_x_, self.lowerbound_y_, self.lowerbound_z_]),
                    "upper_bound_xyz": list([self.upperbound_x_, self.upperbound_y_, self.upperbound_z_]),
                    "lower_bound_uvw": list([self.lowerbound_x_, self.lowerbound_y_, self.lowerbound_z_]),
                    "upper_bound_uvw": list([self.upperbound_x_, self.upperbound_y_, self.upperbound_z_]),
                    "polynomial_order" : list([int(self.viewport.textInput_polynomialOrder_x_.text()), int(self.viewport.textInput_polynomialOrder_y_.text()), int(self.viewport.textInput_polynomialOrder_z_.text())]),
                    "number_of_elements" : list([int(self.viewport.textInput_nElements_x_.text()),  int(self.viewport.textInput_nElements_y_.text()), int(self.viewport.textInput_nElements_z_.text())])
                },
                "trimmed_quadrature_rule_settings"     : {
                    "moment_fitting_residual": float(self.viewport.textInput_residual_.text())
                },
                "non_trimmed_quadrature_rule_settings" : {
                    "integration_method" : self.viewport.popup_integration.currentText()
                },
                "conditions"    :  [
                ]
            }

            #In the QuESoParameters.json file, in order to include the name of the surfaces that \n
            #are subject to boundary conditions, the function called 'append_json' is used. \n
            #Its definition is at the Supplementary Functions section (at the end of the \n
            #QuESoParameters main window's methods)
            #It basically appends the names of the respective surfaces in the 'conditions' key.

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

## **************************************************************************************
                
##**************************************************************************************##
##    Creating the OtherInfos.json file, which contains other several things for the    ##
##                         proper functionality of the plug-in                          ##
##**************************************************************************************##

            self.OtherInfos = \
            {
                "mainObjectName"        : self.mainObjectName,
                "SurfaceLoadFaces"      : self.SurfaceLoad_faces,
                "PenaltySupportFaces"   : self.PenaltySupport_faces,
                "working_directory"     : self.work_dir,
                "STL_directory"         : self.STL_directory,
                "QuESo_directory"       : self.viewport.textInput_QuESo_.text(),
                "QuESo_lib_directory"   : self.viewport.textInput_QuESo_.text() + "/libs",
                "kratos_directory"      : self.viewport.textInput_Kratos_.text() + '/bin/Release',
                "kratos_lib_directory"  : self.viewport.textInput_Kratos_.text() + '/bin/Release/libs'
            }

            with open('OtherInfos.json', 'w') as f:
                json.dump(self.OtherInfos, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass

## **************************************************************************************

##**************************************************************************************##
##          Creating KratosParameters.json and StructuralMaterials.json files           ##
##**************************************************************************************##
            KratosParam = \
        {
            "problem_data"    : {
                "parallel_type" : self.SolverSettingsBox_obj.popup_parallel_type_.currentText(),
                "echo_level"    : int(self.SolverSettingsBox_obj.popup_echo_level2_.currentText()),
                "start_time"    : float(self.SolverSettingsBox_obj.textInput_start_time_.text()),
                "end_time"      : float(self.SolverSettingsBox_obj.textInput_end_time_.text())
            },
            "solver_settings" : {
                "solver_type"              : self.SolverSettingsBox_obj.popup_solver_type_.currentText(),
                "analysis_type"            : self.SolverSettingsBox_obj.popup_analysis_type_.currentText(),
                "model_part_name"          : "NurbsMesh",
                "echo_level"               : int(self.SolverSettingsBox_obj.popup_echo_level3_.currentText()),
                "domain_size"              : 3,
                "model_import_settings"    : {
                    "input_type"     : "use_input_model_part"
                },
                "material_import_settings"        : {
                    "materials_filename" : "StructuralMaterials.json"
                },
                "time_stepping"            : {
                    "time_step" : 1.1       
                },
                "linear_solver_settings":{
                    "preconditioner_type" : "additive_schwarz",
                    "solver_type": "pardiso_lu",
                    "max_iteration" : 5000,
                    "tolerance" : 1e-6
                },
                "rotation_dofs"            : False,
                "builder_and_solver_settings" : {
                    "use_block_builder" : True
                },
                "residual_relative_tolerance"        : 1e-6
            },
            "modelers" : [{
                        "modeler_name": "NurbsGeometryModeler",
                        "Parameters": {
                            "model_part_name" : "NurbsMesh",
                            "geometry_name"   : "NurbsVolume"}
                    }],
            
            "output_processes": 
            {
                "vtk_output": 
                [
                    {
                        "python_module": "vtk_embedded_geometry_output_process",
                        "kratos_module": "KratosMultiphysics.IgaApplication",
                        "process_name": "VtkEmbeddedGeometryOutputProcess",
                        "help": "This process writes postprocessing files for Paraview",
                        "Parameters": {
                            "mapping_parameters": {
                                "main_model_part_name": "NurbsMesh",
                                "nurbs_volume_name": "NurbsVolume",
                                "embedded_model_part_name": "EmbeddedModelPart"
                            },
                            "vtk_parameters": {
                                "model_part_name": "EmbeddedModelPart",
                                "output_control_type": "step",
                                "output_interval": 1,
                                "file_format": "ascii",
                                "output_precision": 7,
                                "output_sub_model_parts": False,
                                "output_path": "kratos_output",
                                "save_output_files_in_folder": True,
                                "nodal_solution_step_data_variables": [
                                    "DISPLACEMENT"
                                ],
                                "nodal_data_value_variables": [
                                    "CAUCHY_STRESS_VECTOR",
                                    "VON_MISES_STRESS"
                                ],
                                "nodal_flags": [],
                                "element_data_value_variables": [],
                                "element_flags": [],
                                "condition_data_value_variables": [],
                                "condition_flags": [],
                                "gauss_point_variables_extrapolated_to_nodes": []
                            }
                        }
                    }
                ]
            }
        }


            StructuralMat = \
            {
                "properties" : [{
                    "model_part_name" : "NurbsMesh",
                    "properties_id"   : int(self.SolverSettingsBox_obj.textInput_properties_id_.text()),
                    "Material"        : {
                        "constitutive_law" : {
                            "name" : self.SolverSettingsBox_obj.popup_constitutive_id_.currentText()
                        },
                        "Variables"        : {
                            "DENSITY"       : float(self.SolverSettingsBox_obj.textInput_density_.text()),
                            "YOUNG_MODULUS" : float(self.SolverSettingsBox_obj.textInput_young_modulus_.text()),
                            "POISSON_RATIO" : float(self.SolverSettingsBox_obj.textInput_poisson_ratio_.text())
                        },
                        "Tables"           : {}
                    }
                }]
            }


            with open('KratosParameters.json', 'w') as f:
                json.dump(KratosParam, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass
            
            with open('StructuralMaterials.json', 'w') as f:
                json.dump(StructuralMat, f, indent=4, separators=(", ", ": "), sort_keys=False)
                pass

## **************************************************************************************

##**************************************************************************************##
##   Creating the QuESo_main.py file, which must be run by Python interpreter so that   ##
##                    QuESo and then Kratos can perform their tasks                     ##
##**************************************************************************************##

            QuESo_main_script = \
'''from QuESo_PythonApplication.PyQuESo import PyQuESo

def main():
    pyqueso = PyQuESo("{QuESo_param_json}")
    pyqueso.Run()
    pyqueso.RunKratosAnalysis()

if __name__ == "__main__":
    main()'''.format(QuESo_param_json="QuESoParameters.json")

            with open('QuESo_main.py', 'w') as f:
                f.write(QuESo_main_script)
                pass

## **************************************************************************************
            
##**************************************************************************************##
##  Performing the surface mesh and saving the resultant STL file to be used later by   ##
##                                        QuESo                                         ##
##**************************************************************************************##
            
## ---- In case user wants to use Gmsh mesher (Gmsh takes STEP file as input and saves STL as output) ----

            if self.gmsh_use_flag == True:
                object = []
                object.append(FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.Objects[0].Name))
                ImportGui.export(object, self.step_directory)
                Gmsh_main_script = \
'''import gmsh
gmsh.initialize()
gmsh.open("{step_directory}")
gmsh.option.setNumber("Mesh.Algorithm", 1)
gmsh.option.setNumber("Mesh.MeshSizeMax", {max_mesh_size})
gmsh.option.setNumber("Mesh.MeshSizeMin", {min_mesh_size})
gmsh.model.mesh.generate(dim = 2)
gmsh.write("{stl_directory}")
gmsh.finalize()'''.format(step_directory = self.step_directory, max_mesh_size = str(self.viewport.maxElSize_textInput.text()), min_mesh_size = str(self.viewport.minElSize_textInput.text()), stl_directory = self.STL_directory)

                with open('Gmsh_main.py', 'w') as f:
                    f.write(Gmsh_main_script)
                    pass

                #Although Gmsh_main.py is to be run by Python interpreter, we wanted to \n
                #open it in a separate system console so that the user can see the \n
                #progress. Therefore, Gmsh_main.py is run by Python interpreter in \n
                #a subprocess
                
                subprocess_command = "gnome-terminal --title='Running Gmsh' -- bash -c 'cd {dir}; python3 Gmsh_main.py'".format(dir=self.work_dir)
                subprocess.run(subprocess_command, timeout=None, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, text = True)

##  --------------------------------------------------------------------------------------

## ---- In case user wants to use FreeCAD's Standard mesher ------------------------------

            elif self.gmsh_use_flag == False:
                object = []
                object.append(FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.Objects[0].Name))
                msh = FreeCAD.ActiveDocument.addObject("Mesh::Feature", "Mesh")
                msh.Mesh = MeshPart.meshFromShape(Shape=object[0].Shape, LinearDeflection = float(self.viewport.surface_deviation_textInput.text()), AngularDeflection = float(self.viewport.angular_deviation_textInput.text()), Relative = True)
                Mesh.export([FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject("Mesh")], str(self.STL_directory))

##  --------------------------------------------------------------------------------------
                
##  **************************************************************************************

##**************************************************************************************##
##                      Visualizing the bounding box for the model                      ##
##**************************************************************************************##

            if self.visulizerun>0:
                FreeCAD.activeDocument().removeObject('Grid')
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
                stepz=abs(self.upperbound_z_-self.lowerbound_z_)/float(self.viewport.textInput_nElements_z_.text())
                
                for i in range(int(self.viewport.textInput_nElements_z_.text())+1):
    
                    pl_z_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,stepz*(i)+self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_z_sec[i],face=False,support=None) #Ok
                    self.gridList.append(duble.Name)
                    duble.Label = "_BoundBoxRectangle_z_fill"+str(i)
                    Gui.activeDocument().activeObject().LineColor = (1.0 , 1.0, 0.0)
                    conteneurRectangle.addObject(duble)
    
            if (mybounds[6] and mybounds[8]) > 0.0:
                pl_y_first=[]
                pl_y_sec=[]
                stepy=abs(self.upperbound_y_-self.lowerbound_y_)/float(self.viewport.textInput_nElements_y_.text())
    
                for i in range(int(self.viewport.textInput_nElements_y_.text())+1):
    
                    pl_y_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,stepy*(i)+self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                    duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_y_sec[i],face=False,support=None) #Ok
                    duble.Label = "_BoundBoxRectangle_y_fill"+str(i)
                    self.gridList.append(duble.Name)
                    Gui.activeDocument().activeObject().LineColor = (0.0 , 1.0, 0.0)
                    conteneurRectangle.addObject(duble)
    
            if (mybounds[7] and mybounds[8]) > 0.0:
                pl_x_first=[]
                pl_x_sec=[]
                stepx=abs(self.upperbound_x_-self.lowerbound_x_)/float(self.viewport.textInput_nElements_x_.text())
    
                for i in range(int(self.viewport.textInput_nElements_x_.text())+1):
    
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

## **************************************************************************************

## ######################################################################################
            
##########################################################################################
##                                                                                      ##
##            TASKS DONE BY THE CANCEL BUTTON ON QuESoParameters MAIN WINDOW            ##
##                                                                                      ##
##########################################################################################

    def onCancel(self):
        self.result = "Cancel"
        self.close()

## ######################################################################################

##########################################################################################
##                                                                                      ##
##                          SUPPLEMENTARY FUNCTION DEFINITIONS                          ##
##                                                                                      ##
##########################################################################################

##**************************************************************************************##
##          Visualize grids function for the checkbox item on the main window           ##
##**************************************************************************************##

# VisualizeGrid_Fun and deVisualizeGrid_Fun functions make use of another function defined,
# namely 'bounds'. Its definition is given in a separate section
        
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
            stepz=abs(self.upperbound_z_-self.lowerbound_z_)/float(self.viewport.textInput_nElements_z_.text())
            
            for i in range(int(self.viewport.textInput_nElements_z_.text())+1):

                pl_z_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,stepz*(i)+self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0) ))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_z_sec[i],face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_z_fill"+str(i)
                self.gridList.append(duble.Name)
                Gui.activeDocument().activeObject().LineColor = (1.0 , 1.0, 0.0)
                conteneurRectangle.addObject(duble)

        if (mybounds[6] and mybounds[8]) > 0.0:
            pl_y_first=[]
            pl_y_sec=[]
            stepy=abs(self.upperbound_y_-self.lowerbound_y_)/float(self.viewport.textInput_nElements_y_.text())

            for i in range(int(self.viewport.textInput_nElements_y_.text())+1):

                pl_y_sec.append(FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,stepy*(i)+self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90) ))
                duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_y_sec[i],face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_y_fill"+str(i)
                self.gridList.append(duble.Name)
                Gui.activeDocument().activeObject().LineColor = (0.0 , 1.0, 0.0)
                conteneurRectangle.addObject(duble)

        if (mybounds[7] and mybounds[8]) > 0.0:
            pl_x_first=[]
            pl_x_sec=[]
            stepx=abs(self.upperbound_x_-self.lowerbound_x_)/float(self.viewport.textInput_nElements_x_.text())

            for i in range(int(self.viewport.textInput_nElements_x_.text())+1):

                pl_x_sec.append(FreeCAD.Placement(FreeCAD.Vector(stepx*(i)+self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90) ))
                duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_x_sec[i],face=False,support=None) #Ok
                duble.Label = "_BoundBoxRectangle_x_fill"+str(i)
                self.gridList.append(duble.Name)
                Gui.activeDocument().activeObject().LineColor = (0.0 , 0.0, 1.0)
                conteneurRectangle.addObject(duble)

        FreeCAD.ActiveDocument.recompute()
        FreeCAD.activeDocument().removeObject('_BoundBoxVolume')

##  **************************************************************************************
        
##**************************************************************************************##
##         Removing Bounding Box grids when the checkbox item's tick is removed         ##
##**************************************************************************************##


    def deVisualizeGrid_Fun(self):

        if self.visulizerun>0:
            FreeCAD.activeDocument().removeObject('Grid')
            for i in self.gridList:
                FreeCAD.activeDocument().removeObject(i)
            self.gridList=[]
            self.visulizerun = 0

##  **************************************************************************************

##**************************************************************************************##
##                          Obtaining the bounds of the grid box                        ##
##**************************************************************************************##

    def bounds(self):
        try:
            mesh = Mesh.Mesh(self.STL_directory)

        except:
            object = []
            object.append(FreeCAD.getDocument(FreeCAD.ActiveDocument.Name).getObject(FreeCAD.ActiveDocument.Objects[0].Name))
            STL_temp_directory = self.projectNameWindow_obj.project_dir + "/" + self.projectNameWindow_obj.project_Name + "_temp.stl"
            Mesh.export(object, STL_temp_directory)
            mesh = Mesh.Mesh(STL_temp_directory)

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

##  **************************************************************************************

##**************************************************************************************##
##               Appending boundary conditions to the relevant JSON file                ##
##**************************************************************************************##


    def append_json(self, entry, filename='QuESoParameters.json'):
            with open(filename, "r") as file:
                data = json.load(file, object_pairs_hook=OrderedDict)
                # Update json object
            data["conditions"].append(entry)
                # Write json file
            with open(filename, "w") as file:
                json.dump(data, file, indent = 4, separators=(", ", ": "), sort_keys=False)

##  **************************************************************************************

##  ######################################################################################
                
## _______________________________________________________________________________________
## _______________________________________________________________________________________

##########################################################################################
##                                                                                      ##
##                           OTHER REQUIRED CLASS DEFINITIONS                           ##
##                                                                                      ##
##########################################################################################

##**************************************************************************************##
##             Dialog Box to give project a name and specify its directory              ##
##**************************************************************************************##

class projectNameWindow(QtGui.QDialog):

    def __init__(self):
        super(projectNameWindow, self).__init__()
        self.initUI()
        self.project_Name = ""
        self.project_dir = ""
        self.okFlag = False

    def initUI(self):

        layout = QtGui.QGridLayout()

        self.setWindowTitle("Project Name")

        # Introducing QtGui's built-in icons for visual enchancements
        forward_arrow_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_ArrowForward)
        cancel_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogCancelButton)
        browse_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DirOpenIcon)

        self.label_name = QtGui.QLabel("Please give your project a name (or the name of the existing project):", self)
        self.label_name.setWordWrap(True)
        layout.addWidget(self.label_name, 0, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(1, 3)

        self.textInput_name = QtGui.QLineEdit(self)
        self.textInput_name.setPlaceholderText("e.g: Cantilever, Knuckle ... ")
        self.textInput_name.setFixedWidth(250)
        layout.addWidget(self.textInput_name, 2, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(3, 7)

        self.label_dir = QtGui.QLabel("Please give the directory where the project will be saved (or the path to the existing project folder):", self)
        self.label_dir.setWordWrap(True)
        layout.addWidget(self.label_dir, 4, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(5, 3)

        sublayout = QtGui.QHBoxLayout()
        self.textInput_dir = QtGui.QLineEdit(self)
        self.textInput_dir.setFixedWidth(250)
        browseButton = QtGui.QPushButton('Browse Files', self)
        browseButton.setIcon(browse_icon)
        browseButton.clicked.connect(self.onBrowseButton)
        sublayout.addWidget(self.textInput_dir, 0)
        sublayout.setSpacing(5)
        sublayout.addWidget(browseButton, 1)

        layout.addLayout(sublayout, 6, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(7, 10)

        sublayout = QtGui.QHBoxLayout()
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancelButton)
        cancelButton.setIcon(cancel_icon)
        okButton = QtGui.QPushButton('Next', self)
        okButton.setAutoDefault(True)

        okButton.clicked.connect(self.onOkButton)
        okButton.setAutoDefault(True)
        okButton.setIcon(forward_arrow_icon)
        sublayout.addWidget(okButton, 0)
        sublayout.addWidget(cancelButton)
        sublayout.setSpacing(40)

        layout.addLayout(sublayout, 8, 0, QtCore.Qt.AlignCenter)

        self.setLayout(layout)

        width = self.sizeHint().width()
        height = self.sizeHint().height()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.textInput_name.size().width()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setFixedSize(width, height)


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

##  **************************************************************************************
        
##**************************************************************************************##
## Penalty Support Boundary Condition Dialog Box - the one that appears after clicking  ##
##                     on a surface and on which values are entered                     ##
##**************************************************************************************##

# The reason of implementing it separately from QuESoParameters main window is to be \n
# able reset the values in the text input fields upon closing the dialog box. Also, \n
# error handling is easier that such that if the user leaves the value input fields, \n
# we can pop an error message and return to dialog box again. Also, it is not really \n
# dependent QuESoParameters main window - i.e. it is not a button or checkbox that is \n
# located directly on the main window. It is a separate dialog box, and we may want to \n
# show/execute it (depending on the situation) several times when the user decides so.
# It is also more convenient script-based, because we already created an instace of it \n
# that is an object of QuESoParameters main window. So, it does not go out of scope \n
# and we can show/execute it whenever we want.

class PenaltySupportBCBox(QtGui.QDialog):

    def __init__(self):
        super(PenaltySupportBCBox, self).__init__()
        self.initUI()

    def initUI(self):
            width = 350
            height = 120
            std_validate = QtGui.QDoubleValidator() #Validating the input to be a double
            std_validate.setNotation(QtGui.QDoubleValidator.StandardNotation)
            centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
            self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
            self.setWindowTitle("Apply PenaltySupport Boundary Condition")
            self.label_PenaltySupport = QtGui.QLabel("Please enter the displacement constraint values:", self)
            self.label_PenaltySupport.move(10, 20)
            # self.element_list = [] #It seems redundant?
            # self.icon_element_list = [] #It seems redundant?

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

    # Adding the feature of resetting the input values upon closing the dialog box

    def closeEvent(self, event):
        self.resetInputValues()
        event.accept()

    def okButton_PenaltySupportBCBox(self):
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

    # The simple function to reset values in the text input fields
    def resetInputValues(self):
        self.text_x_constraint.setText("")
        self.text_y_constraint.setText("")
        self.text_z_constraint.setText("")

##  **************************************************************************************

##**************************************************************************************##
##    Surface Load Boundary Condition Dialog Box - the one that appears after clicking  ##
##                     on a surface and on which values are entered                     ##
##**************************************************************************************##

# The reason of implementing it separately from QuESoParameters main window is to be \n
# able reset the values in the text input fields upon closing the dialog box. Also, \n
# error handling is easier that such that if the user leaves the value input fields, \n
# we can pop an error message and return to dialog box again. Also, it is not really \n
# dependent QuESoParameters main window - i.e. it is not a button or checkbox that is \n
# located directly on the main window. It is a separate dialog box, and we may want to \n
# show/execute it (depending on the situation) several times when the user decides so.
# It is also more convenient script-based, because we already created an instace of it \n
# that is an object of QuESoParameters main window. So, it does not go out of scope \n
# and we can show/execute it whenever we want.

class SurfaceLoadBCBox(QtGui.QDialog):

    def __init__(self):
        super(SurfaceLoadBCBox, self).__init__()
        self.initUI()

    def initUI(self):
            width = 350
            height = 175
            std_validate = QtGui.QDoubleValidator() #Validating the input to be a double
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

    # Adding the feature of resetting the input values upon closing the dialog box

    def closeEvent(self, event):
        self.resetInputValues()
        event.accept()

    def okButton_SurfaceLoadBCBox(self):
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

    # The simple function to reset values in the text input fields

    def resetInputValues(self):
        self.text_x_constraint.setText("")
        self.text_y_constraint.setText("")
        self.text_z_constraint.setText("")
        self.text_SurfaceLoad_modulus.setText("")

##  **************************************************************************************

##**************************************************************************************##
##  The list showing the surfaces subject to Penalty Support Boundary Condition by the  ##
##                                         user                                         ##
##**************************************************************************************##

# The reason of implementing it separately from QuESoParameters main window is to be \n
# able delete the FaceIDs completely in the closing event when user decides to discard \n
# them. Also, if the user does not discard, we must be capable of keeping track of the \n
# surfaces subject to Penalty Support Boundary Condition - that is to say, we must not \n
# get a blank list every time user launches unless he/she does not discard it. Moreover, \n
# it is not really dependent QuESoParameters main window - i.e. it is not a button or \n 
# checkbox that is located directly on the main window. It is a separate dialog box, \n
# and we may want to show several times when the user decides so. It is also more \n 
# convenient script-based, because we already created an instace of it that is an object \n 
# of QuESoParameters main window. So, it does not go out of scope and we can show it \n
# whenever we want.


class PenaltySupportFacesList(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("List of Faces")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on = True)
        layout = QtGui.QGridLayout()
        discard_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogDiscardButton)
        ok_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogApplyButton)

        FaceID_label = QtGui.QLabel("Faces Under Penalty Support BC:", self)
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
        self.okButton.setIcon(ok_icon)
        self.okButton.setAutoDefault(True)
        self.okButton.setFixedWidth(80)

        self.DiscardButton = QtGui.QPushButton('Discard', self)
        self.DiscardButton.setIcon(discard_icon)
        self.DiscardButton.setFixedWidth(80)

        layout4OkDiscard = QtGui.QHBoxLayout()
        layout4OkDiscard.addWidget(self.okButton)
        layout4OkDiscard.addWidget(self.DiscardButton)

        layout.addLayout(layout4OkDiscard, 6, 0, 1, -1)

        self.finished_flag = QtGui.QAction("Quit", self)

        self.setLayout(layout)

        # Setting the position such that it will always appear at the top-left corner
        topLeftPoint = QtGui.QDesktopWidget().availableGeometry().topLeft()
        frameGm = self.frameGeometry()
        frameGm.moveTopLeft(topLeftPoint)
        self.move(frameGm.topLeft())

    def closeEvent(self, event):
        if (self.result):
            event.accept()
        else:
            self.listwidget.clear()
            event.accept()

##  **************************************************************************************

##**************************************************************************************##
##     The list showing the surfaces subject to Surface Load Boundary Condition by the  ##
##                                         user                                         ##
##**************************************************************************************##

# The reason of implementing it separately from QuESoParameters main window is to be \n
# able delete the FaceIDs completely in the closing event when user decides to discard \n
# them. Also, if the user does not discard, we must be capable of keeping track of the \n
# surfaces subject to Surface Load Boundary Condition - that is to say, we must not \n
# get a blank list every time user launches unless he/she does not discard it. Moreover, \n
# it is not really dependent QuESoParameters main window - i.e. it is not a button or \n 
# checkbox that is located directly on the main window. It is a separate dialog box, \n
# and we may want to show several times when the user decides so. It is also more \n 
# convenient script-based, because we already created an instace of it that is an object \n 
# of QuESoParameters main window. So, it does not go out of scope and we can show it \n
# whenever we want.

class SurfaceLoadFacesList(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("List of Faces")
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint, on = True)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, on = True)
        layout = QtGui.QGridLayout()
        discard_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogDiscardButton)
        ok_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogApplyButton)

        FaceID_label = QtGui.QLabel("Faces Under Surface Load BC:", self)
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
        self.okButton.setIcon(ok_icon)
        self.okButton.setAutoDefault(True)
        self.okButton.setFixedWidth(80)

        self.DiscardButton = QtGui.QPushButton('Discard', self)
        self.DiscardButton.setIcon(discard_icon)
        self.DiscardButton.setFixedWidth(80)

        layout4OkDiscard = QtGui.QHBoxLayout()
        layout4OkDiscard.addWidget(self.okButton)
        layout4OkDiscard.addWidget(self.DiscardButton)

        layout.addLayout(layout4OkDiscard, 6, 0, 1, -1)

        self.finished_flag = QtGui.QAction("Quit", self)

        self.setLayout(layout)

        # Setting the position such that it will always appear at the top-left corner
        topLeftPoint = QtGui.QDesktopWidget().availableGeometry().topLeft()
        frameGm = self.frameGeometry()
        frameGm.moveTopLeft(topLeftPoint)
        self.move(frameGm.topLeft())


    def closeEvent(self, event):
        if (self.result):
            event.accept()
        else:
            self.listwidget.clear()
            event.accept()

##  **************************************************************************************
            
##**************************************************************************************##
##                 The dialog box to set up the Kratos Solver Settings                  ##
##**************************************************************************************##

class SolverSettingsBox(QtGui.QDialog):

    def __init__(self):
        super(SolverSettingsBox, self).__init__()
        self.initUI()

    def initUI(self):

        std_validate        = QtGui.QIntValidator()                                # The validation method for an input to be integer.
        scientific_validate = QtGui.QDoubleValidator()                             # The validation method for an input to be double.
        scientific_validate.setNotation(QtGui.QDoubleValidator.ScientificNotation) # The validation method for an input to be in scientific notation.
        double_validate = QtGui.QDoubleValidator()
    
        self.setWindowTitle("Kratos Solver Settings")
        boldFont=QtGui.QFont()
        boldFont.setBold(True)
        boldUnderlinedFont=QtGui.QFont()
        boldUnderlinedFont.setBold(True)
        boldUnderlinedFont.setUnderline(True)
        blueFont = QtGui.QPalette()
        blueFont.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#005293'))

        layout = QtGui.QGridLayout()

        #solution settings head
        self.label_main_ = QtGui.QLabel("Problem data", self)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)
        layout.addWidget(self.label_main_, 0, 0, QtCore.Qt.AlignCenter)

        layout.setRowMinimumHeight(1, 5)

        #parallel type
        sublayout = QtGui.QGridLayout()
        self.label_parallel_type_ = QtGui.QLabel("Parallel type:", self)

        self.label_echo_level2_ = QtGui.QLabel("Echo level:", self)
        sublayout.addWidget(self.label_parallel_type_,0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.label_echo_level2_,0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 2, 0)

        layout.setRowMinimumHeight(3, 0)

        sublayout = QtGui.QGridLayout()
        self.popup_parallel_type_ = QtGui.QComboBox(self)
        self.popup_parallel_type_items = ("OpenMP", "MPI")
        self.popup_parallel_type_.addItems(self.popup_parallel_type_items)
        self.popup_echo_level2_ = QtGui.QComboBox(self)
        self.popup_echo_level2_items = ("0", "1", "2")
        self.popup_echo_level2_.addItems(self.popup_echo_level2_items)
        sublayout.addWidget(self.popup_parallel_type_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.popup_echo_level2_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 4, 0)

        layout.setRowMinimumHeight(5, 3)

        sublayout = QtGui.QGridLayout()
        self.label_start_time_ = QtGui.QLabel("Start time:", self)
        self.label_end_time_ = QtGui.QLabel("End time:", self)
        sublayout.addWidget(self.label_start_time_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.label_end_time_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 6, 0)

        layout.setRowMinimumHeight(7, 0)

        sublayout = QtGui.QGridLayout()
        self.textInput_start_time_ = QtGui.QLineEdit(self)
        self.textInput_start_time_.setValidator(double_validate)
        self.textInput_start_time_.setPlaceholderText("0.0")
        self.textInput_end_time_ = QtGui.QLineEdit(self)
        self.textInput_end_time_.setValidator(double_validate)
        self.textInput_end_time_.setPlaceholderText("1.0")
        sublayout.addWidget(self.textInput_start_time_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.textInput_end_time_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 8, 0)

        layout.setRowMinimumHeight(9, 7)

        #Solver settings head
        self.label_main_ = QtGui.QLabel("Solver settings", self)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)
        layout.addWidget(self.label_main_, 10, 0, QtCore.Qt.AlignCenter)

        layout.setRowMinimumHeight(11, 5)

        #solver type
        sublayout = QtGui.QGridLayout()
        self.label_solver_type_ = QtGui.QLabel("Solver type:", self)
        self.label_analysis_type_ = QtGui.QLabel("Analysis type:", self)
        sublayout.addWidget(self.label_solver_type_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.label_analysis_type_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 12, 0)

        layout.setRowMinimumHeight(13, 0)
        
        sublayout = QtGui.QGridLayout()
        self.popup_solver_type_ = QtGui.QComboBox(self)
        self.popup_solver_type_items = ("Static", " ")
        self.popup_solver_type_.addItems(self.popup_solver_type_items)
        self.popup_analysis_type_ = QtGui.QComboBox(self)
        self.popup_analysis_type_items = ('linear', 'nonlinear')
        self.popup_analysis_type_.addItems(self.popup_analysis_type_items)

        sublayout.addWidget(self.popup_solver_type_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.popup_analysis_type_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 14, 0)

        layout.setRowMinimumHeight(15, 3)

        self.label_echo_level3_ = QtGui.QLabel("Echo level:", self)
        layout.addWidget(self.label_echo_level3_, 16, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(17, 3)

        self.popup_echo_level3_ = QtGui.QComboBox(self)
        self.popup_echo_level3_items = ("0", "1", "2")
        self.popup_echo_level3_.addItems(self.popup_echo_level3_items)
        layout.addWidget(self.popup_echo_level3_, 18, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(19, 7)


        #Material properties head
        self.label_main_ = QtGui.QLabel("Material Properties:", self)
        self.label_main_.setFont(boldUnderlinedFont)
        self.label_main_.setPalette(blueFont)
        layout.addWidget(self.label_main_, 20, 0, QtCore.Qt.AlignCenter)

        layout.setRowMinimumHeight(21, 5)

        #Density
        sublayout = QtGui.QGridLayout()
        self.label_density_ = QtGui.QLabel("Density:", self)
        self.label_young_modulus_ = QtGui.QLabel("Young Modulus:", self)
        sublayout.addWidget(self.label_density_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.label_young_modulus_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 22, 0)

        layout.setRowMinimumHeight(23, 0)

        sublayout = QtGui.QGridLayout()
        self.textInput_density_ = QtGui.QLineEdit(self)
        self.textInput_density_.setValidator(double_validate)
        self.textInput_density_.setPlaceholderText("1.0")
        self.textInput_young_modulus_ = QtGui.QLineEdit(self)
        self.textInput_young_modulus_.setValidator(double_validate)
        self.textInput_young_modulus_.setPlaceholderText("100")
        sublayout.addWidget(self.textInput_density_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.textInput_young_modulus_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 24, 0)

        layout.setRowMinimumHeight(25, 3)

        #Poisson Ratio
        sublayout = QtGui.QGridLayout()
        self.label_poisson_ratio_ = QtGui.QLabel("Poisson Ratio:", self)
        self.label_properties_id_ = QtGui.QLabel("Properties ID:", self)
        sublayout.addWidget(self.label_poisson_ratio_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.label_properties_id_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 26, 0)

        layout.setRowMinimumHeight(27, 0)
        
        sublayout = QtGui.QGridLayout()
        self.textInput_poisson_ratio_ = QtGui.QLineEdit(self)
        self.textInput_poisson_ratio_.setValidator(double_validate)
        self.textInput_poisson_ratio_.setPlaceholderText("0.0")
        self.textInput_properties_id_ = QtGui.QLineEdit(self)
        self.textInput_properties_id_.setValidator(std_validate)
        self.textInput_properties_id_.setPlaceholderText("1")
        sublayout.addWidget(self.textInput_poisson_ratio_, 0, 0, QtCore.Qt.AlignLeft)
        sublayout.setColumnMinimumWidth(1, 20)
        sublayout.addWidget(self.textInput_properties_id_, 0, 2, QtCore.Qt.AlignLeft)
        layout.addLayout(sublayout, 28, 0)

        layout.setRowMinimumHeight(29, 3)

        #Constitutive law
        self.label_constitutive_id_ = QtGui.QLabel("Constitutive law name:", self)
        layout.addWidget(self.label_constitutive_id_, 30, 0, QtCore.Qt.AlignLeft)
        
        layout.setRowMinimumHeight(31, 0)

        self.popup_constitutive_id_ = QtGui.QComboBox(self)
        self.popup_constitutive_id_items = ("LinearElastic3DLaw", " ")
        self.popup_constitutive_id_.addItems(self.popup_constitutive_id_items)
        layout.addWidget(self.popup_constitutive_id_, 32, 0, QtCore.Qt.AlignLeft)

        layout.setRowMinimumHeight(33, 20)

        sublayout = QtGui.QHBoxLayout()
        self.cancelButton = QtGui.QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.onCancel)
        self.okButton = QtGui.QPushButton('OK', self)
        self.okButton.clicked.connect(self.onOk)
        self.okButton.setAutoDefault(True)
        sublayout.addWidget(self.okButton)
        sublayout.addWidget(self.cancelButton)
        sublayout.setSpacing(40)
        layout.addLayout(sublayout, 34, 0, QtCore.Qt.AlignCenter)

        self.setLayout(layout)

        width = self.sizeHint().width()
        height = self.sizeHint().height()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setFixedSize(width, height)

    # When the Ok button is clicked, the key:value pairs that will be in KratosParameters.json
    # file are created, but the JSON file is not dumped yet. Dumping it takes place upon clicking
    # the Ok button of QuESoParameters main window.
    
    def onOk(self):
        self.result = "Ok"
        self.close()

            
    def onCancel(self):
        self.result = "Cancel"
        self.close()

##  **************************************************************************************

##  ######################################################################################
