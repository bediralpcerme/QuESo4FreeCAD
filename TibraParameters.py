from FreeCAD_PySide import *
import os
import FreeCAD
import Mesh
import json
import FreeCADGui, Draft, Part, PySide


#TO DO LIST: 
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
        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")

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
        self.browseWindow = QtGui.QFileDialog(self)
        self.browseWindow.setFileMode(QtGui.QFileDialog.ExistingFile)
        self.browseWindow.setNameFilter(str("*.stl"))
        self.browseWindow.setViewMode(QtGui.QFileDialog.Detail)
        self.browseWindow.setDirectory(self.work_dir)

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
        FreeCADGui.ActiveDocument.getObject(BDvol.Name).LineColor  = (red, green, blue)
        FreeCADGui.ActiveDocument.getObject(BDvol.Name).PointColor = (red, green, blue)
        FreeCADGui.ActiveDocument.getObject(BDvol.Name).ShapeColor = (red, green, blue)
        FreeCADGui.ActiveDocument.getObject(BDvol.Name).Transparency = 90

        conteneurRectangle = []
        del conteneurRectangle[:]
        conteneurRectangle = FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Grid")

        if (mybounds[6] and mybounds[7]) > 0.0:
            pl_0 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
            #pl_0 = adjustedGlobalPlacement(objs[0], boundBoxLocation)
            duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_0,face=False,support=None) #OK
            duble.Label = "_BoundBoxRectangle_Bo"
            FreeCADGui.activeDocument().activeObject().LineColor = (1.0, 1.0, blue)
            conteneurRectangle.addObject(duble)
           
            pl_1 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,0.0))
            #pl_1 =adjustedGlobalPlacement(objs[0], boundBoxLocation + FreeCAD.Vector(0,0,boundBoxLZ))
            duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_y_-self.lowerbound_y_),placement=pl_1,face=False,support=None) #Ok
            duble.Label = "_BoundBoxRectangle_To"
            FreeCADGui.activeDocument().activeObject().LineColor = (1.0, 1.0, blue)
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
                FreeCADGui.activeDocument().activeObject().LineColor = (1.0 , 1.0, blue)
                conteneurRectangle.addObject(duble)


        if (mybounds[6] and mybounds[8]) > 0.0:
            pl_2 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90))
            #pl_2 = pl_0.multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
            duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_2,face=False,support=None) #Ok
            duble.Label = "_BoundBoxRectangle_Fr"
            FreeCADGui.activeDocument().activeObject().LineColor = (0.0, 1.0, blue)
            conteneurRectangle.addObject(duble)
            pl_3 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.upperbound_y_,self.lowerbound_z_), FreeCAD.Rotation(0.0,0.0,90))
            #pl_3 = adjustedGlobalPlacement(objs[0], boundBoxLocation+App.Vector(0, boundBoxLY, 0)).multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
            duble = Draft.makeRectangle(length=(self.upperbound_x_-self.lowerbound_x_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_3,face=False,support=None) #Ok
            duble.Label = "_BoundBoxRectangle_Re"
            FreeCADGui.activeDocument().activeObject().LineColor = (0.0, 1.0, blue)
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
                FreeCADGui.activeDocument().activeObject().LineColor = (0.0 , 1.0, blue)
                conteneurRectangle.addObject(duble)

        if (mybounds[7] and mybounds[8]) > 0.0:
            pl_4 = FreeCAD.Placement(FreeCAD.Vector(self.lowerbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90))
            #pl_2 = pl_0.multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
            duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_4,face=False,support=None) #Ok
            duble.Label = "_BoundBoxRectangle_Le"
            FreeCADGui.activeDocument().activeObject().LineColor = (0.0, 0.0, 1.0)
            conteneurRectangle.addObject(duble)

            pl_5= FreeCAD.Placement(FreeCAD.Vector(self.upperbound_x_,self.lowerbound_y_,self.lowerbound_z_), FreeCAD.Rotation(90,0.0,90))
            #pl_3 = adjustedGlobalPlacement(objs[0], boundBoxLocation+App.Vector(0, boundBoxLY, 0)).multiply(App.Placement(App.Vector(0.,0.,0.),App.Rotation(0.0,0.0,90)))
            duble = Draft.makeRectangle(length=(self.upperbound_y_-self.lowerbound_y_),height=(self.upperbound_z_-self.lowerbound_z_),placement=pl_5,face=False,support=None) #Ok
            duble.Label = "_BoundBoxRectangle_Ri"
            FreeCADGui.activeDocument().activeObject().LineColor = (0.0, 0.0, 1.0)
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
                FreeCADGui.activeDocument().activeObject().LineColor = (0.0 , 0.0, 1.0)
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

        return [boundBoxXMin,boundBoxYMin,boundBoxZMin,boundBoxXMax,boundBoxYMax,boundBoxZMax,boundBoxLX,boundBoxLY,boundBoxLZ]
    