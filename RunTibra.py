from FreeCAD_PySide import *
import subprocess
import FreeCAD
import sys, os, stat, platform
import json


class RunTibra(QtGui.QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #position and geometry of the dialog box
        width = 300
        height = 160
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Run Tibra?")

        #label text
        self.label_ = QtGui.QLabel("Run Tibra?", self)
        self.label_.move(100, 20)

        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.move(10, 90)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)
        okButton.move(170, 90)

    def onOk(self):
       
        #By subprocess
        self.docName =  FreeCAD.ActiveDocument.Label + ".FCStd"
        self.work_dir = FreeCAD.ActiveDocument.FileName
        self.work_dir = self.work_dir.replace(self.docName,"")
        self.data_dir = self.work_dir + 'TIBRA/data'

        os.chdir(self.data_dir)

        with open('DirectoryInfo.json', 'r') as myfile:
            mydata = json.load(myfile)

        kratos_dirOrg = mydata['kratos_directory']
        kratos_lib_dirOrg = mydata['kratos_lib_directory']
        QuESo_dirOrg = mydata['QuESo_directory']
        QuESo_lib_dirOrg = mydata['QuESo_lib_directory']

        if platform.system() == 'Linux':

            Run_script = \
            '''gnome-terminal --title="Running QuESo and Kratos" -- bash -c "cd {dir}; env LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{kratos_lib_dir}:{QuESo_lib_dir} /usr/bin/python3.10 -x QuESo_main.py {dir}"'''.format(dir=self.data_dir, kratos_lib_dir = kratos_lib_dirOrg, QuESo_lib_dir=QuESo_lib_dirOrg)

            with open("RunTibra_Shell.sh", "w") as rtsh:
                rtsh.write(Run_script)
                pass

            rtsh.close()

            RunTibra_Shell_dir = self.data_dir + "/RunTibra_Shell.sh"
            
            current_st = os.stat(RunTibra_Shell_dir)

            os.chmod(RunTibra_Shell_dir, current_st.st_mode | stat.S_IEXEC)

            subprocess.run(RunTibra_Shell_dir, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, text = True)
        
        elif platform.system() == 'Windows':
            
            Run_script = \
            '''Start %SystemRoot%\System32\cmd.exe /K "cd {dir} & set PYTHONPATH=%PYTHONPATH%;{QuESo_dir};{kratos_dir} & set PATH=%PATH%;{QuESo_lib_dir};{kratos_lib_dir}"'''.format(dir=self.data_dir, QuESo_dir=QuESo_dirOrg, kratos_dir=kratos_dirOrg, kratos_lib_dir = kratos_lib_dirOrg, QuESo_lib_dir=QuESo_lib_dirOrg)
            
            with open("RunTibra_Shell.bat", "w") as rtsh:
                rtsh.write(Run_script)
                pass

            rtsh.close()
            
            RunTibra_Shell_dir = self.data_dir + "/RunTibra_Shell.bat"
            
            current_st = os.stat(RunTibra_Shell_dir)

            os.chmod(RunTibra_Shell_dir, current_st.st_mode | stat.S_IEXEC)
            
            subprocess.run('RunTibra_Shell.bat', cwd=self.data_dir, shell=True, text=True)
        

        self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()

    
