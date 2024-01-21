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
        self.setWindowTitle("Run QuESo")
        layout = QtGui.QGridLayout()
        cancel_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogCancelButton)
        ok_icon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.StandardPixmap.SP_DialogApplyButton)

        #label text
        self.label_ = QtGui.QLabel("Are you sure you want to run QuESo and Kratos?", self)
        layout.addWidget(self.label_, 0, 0, QtCore.Qt.AlignCenter)

        layout.setRowMinimumHeight(1, 20)

        # cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.setIcon(cancel_icon)
        cancelButton.clicked.connect(self.onCancel)
        # OK button
        okButton = QtGui.QPushButton('OK', self)
        okButton.setIcon(ok_icon)
        okButton.clicked.connect(self.onOk)
        okButton.setAutoDefault(True)

        # Sublayout for Ok-Cancel

        layout_okCancel = QtGui.QHBoxLayout()
        layout_okCancel.addWidget(okButton)
        layout_okCancel.addWidget(cancelButton)
        layout_okCancel.setSpacing(40)

        layout.addLayout(layout_okCancel, 2, 0, QtCore.Qt.AlignCenter)

        self.setLayout(layout)

    def onOk(self):
       
        #Changing working directory to read JSON file containing the directory info

        docName =  "/" + FreeCAD.ActiveDocument.Label + ".FCStd"
        work_dir = FreeCAD.ActiveDocument.FileName
        work_dir = work_dir.replace(docName,"")

        os.chdir(work_dir)

        #Reading the directories

        with open('OtherInfos.json', 'r') as myfile:
            mydata = json.load(myfile)

        kratos_dirOrg = mydata['kratos_directory']
        kratos_lib_dirOrg = mydata['kratos_lib_directory']
        QuESo_dirOrg = mydata['QuESo_directory']
        QuESo_lib_dirOrg = mydata['QuESo_lib_directory']

        #Creating the bash file based on the operating system (except macOS). The extension of the file is ".sh" for Linux and ".bat" for Windows.
        #The bash file is made to be executable, and run as subprocess.

        if platform.system() == 'Linux':

            Run_script = \
            '''#!/bin/bash

gnome-terminal --title="Running QuESo and Kratos" -- bash -c "source ~/.bashrc; cd {dir}; export PYTHONPATH=$PYTHONPATH:{kratos_dir}:{QuESo_dir}; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{kratos_lib_dir}:{QuESo_lib_dir}; source /opt/intel/oneapi/setvars.sh intel64; python3 QuESo_main.py; echo 'Press ENTER to exit'; read"'''.format(dir=work_dir, kratos_dir=kratos_dirOrg, QuESo_dir=QuESo_dirOrg, kratos_lib_dir = kratos_lib_dirOrg, QuESo_lib_dir=QuESo_lib_dirOrg)

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

    
