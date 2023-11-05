from FreeCAD_PySide import *
import subprocess
import FreeCAD
import sys, os, stat, platform
import json


class RunQuESo(QtGui.QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #position and geometry of the dialog box
        width = 300
        height = 160
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-0.5*width, centerPoint.y()-0.5*height, width, height)
        self.setWindowTitle("Run QuESo?")

        #label text
        self.label_ = QtGui.QLabel("Run QuESo?", self)
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

        docName =  "/" + FreeCAD.ActiveDocument.Label + ".FCStd"
        work_dir = FreeCAD.ActiveDocument.FileName
        work_dir = work_dir.replace(docName,"")

        os.chdir(work_dir)

        with open('DirectoryInfo.json', 'r') as myfile:
            mydata = json.load(myfile)

        kratos_dirOrg = mydata['kratos_directory']
        kratos_lib_dirOrg = mydata['kratos_lib_directory']
        QuESo_dirOrg = mydata['QuESo_directory']
        QuESo_lib_dirOrg = mydata['QuESo_lib_directory']

        os.chdir(work_dir)

        if platform.system() == 'Linux':

            Run_script = \
            '''#!/bin/bash

gnome-terminal --title="Running QuESo and Kratos" -- bash -c "source ~/.bashrc; cd {dir}; export PYTHONPATH=$PYTHONPATH:{kratos_dir}:{QuESo_dir}; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{kratos_lib_dir}:{QuESo_lib_dir}; python3 QuESo_main.py; echo 'Press ENTER to exit'; read"'''.format(dir=work_dir, kratos_dir=kratos_dirOrg, QuESo_dir=QuESo_dirOrg, kratos_lib_dir = kratos_lib_dirOrg, QuESo_lib_dir=QuESo_lib_dirOrg)

            with open("RunQuESo_Shell.sh", "w") as rtsh:
                rtsh.write(Run_script)
                pass

            rtsh.close()

            RunQuESo_Shell_dir = work_dir + "/RunQuESo_Shell.sh"
            
            current_st = os.stat(RunQuESo_Shell_dir)

            os.chmod(RunQuESo_Shell_dir, current_st.st_mode | stat.S_IEXEC)

            subprocess.run(RunQuESo_Shell_dir, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, text = True)
        
        elif platform.system() == 'Windows':
            
            Run_script = \
            '''Start %SystemRoot%\System32\cmd.exe /K "cd {dir} & set PYTHONPATH=%PYTHONPATH%;{QuESo_dir};{kratos_dir} & set PATH=%PATH%;{QuESo_lib_dir};{kratos_lib_dir} & python3 QuESo_main.py & pause && exit"'''.format(dir=work_dir, QuESo_dir=QuESo_dirOrg, kratos_dir=kratos_dirOrg, kratos_lib_dir = kratos_lib_dirOrg, QuESo_lib_dir=QuESo_lib_dirOrg)
            
            with open("RunQuESo_Shell.bat", "w") as rtsh:
                rtsh.write(Run_script)
                pass

            rtsh.close()
            
            RunQuESo_Shell_dir = work_dir + "/RunQuESo_Shell.bat"
            
            current_st = os.stat(RunQuESo_Shell_dir)

            os.chmod(RunQuESo_Shell_dir, current_st.st_mode | stat.S_IEXEC)
            
            subprocess.run('RunQuESo_Shell.bat', cwd=work_dir, shell=True, text=True)
        

        self.close()

    def onCancel(self):
        self.result = "Cancel"
        self.close()

    
