#!/usr/bin/env python
"""
FW103S Thorlabs filter wheel GUI.

Gayatri 04/19
"""
import os
import platform
import sys
import numpy as np
import struct
import time
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QComboBox, QDialog,
# QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
# QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
# QVBoxLayout, QAction, QMessageBox, QGroupBox, QInputDialog, QStyleFactory, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyAPT.PyAPT import APTMotor

# import pdb    
#Initializing motor
Motor1 = APTMotor(80831430, HWTYPE=29)
print('Declared object')
Motor1.initializeHardwareDevice()
print('Initialized hardware')
time.sleep(.5)

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'FW103S Control'

        # For initializing size and position of main window wrt computer screen
        self.left = 600
        self.top = 300
        self.width = 550
        self.height = 500



        #Initializing some variables here...
        self.pos561 = Motor1.getPos()
        pos488 = float(0.0)
        pos460 = float(0.0)
        pos405 = float(0.0)

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('p202.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        #Grid arrangement of widgets

        # self.createGridLayout()
        # windowLayout = QVBoxLayout()
        # windowLayout.addWidget(self.horizontalGroupBox)
        # self.setLayout(windowLayout)

        
        grid = QGridLayout()
        grid.addWidget(self.fw561Control(), 0, 0)
        grid.addWidget(self.fw488Control(), 1, 0)
        grid.addWidget(self.fw460Control(), 0, 1)
        grid.addWidget(self.fw405Control(), 1, 1)
        self.setLayout(grid)

        self.show()
               

    @pyqtSlot()
    def disconnectM(self):
        print('Terminating connection with motor and releasing allocated memory...')
        Motor1.cleanUpAPT()
        print('Done.')

    @pyqtSlot()
    def gotoPosition(self):
        print('Moving to specified position...')
        #print("Position now : ", Motor1.getPos()) # Can I see position updated in real time?
        #textboxValue = self.textbox.text()
        #pos = float(textboxValue)
        #Motor1.mAbs(pos)
        #time.sleep(.5)
        #print("Updated position : ", Motor1.getPos())
        #self.textbox.setText("")
        print('Done.')
        #Update position value display somewhere

    @pyqtSlot()
    def selectNDfilter(self):
        print('Moving to selected ND filter...')
        nd = [['ND 0',0.0], ['ND 0.5',60.0], ['ND 1',120.0], ['ND 1.3',180.0], ['ND 2',240.0], ['ND 3',300]]
        for (ndval,pos) in nd:
            if ndval == self.sender().text() :
                position = pos
            else:
                pass
        Motor1.mAbs(position)
        time.sleep(.5)
        print('Done.')
        #Update position value display somewhere
        self.pos561 = Motor1.getPos()
        posinfo = "Position : " + str(round(self.pos561,2))
        self.label.setText(posinfo)

    @pyqtSlot()
    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Select an ND filter")
        layout = QHBoxLayout()
        
        #Buttons

        b1 = QPushButton('ND 0', self)
        b2 = QPushButton('ND 0.5', self)
        b3 = QPushButton('ND 1', self)
        b4 = QPushButton('ND 1.3', self)
        b5 = QPushButton('ND 2', self)
        b6 = QPushButton('ND 3', self)

        b1.clicked.connect(self.selectNDfilter)
        b2.clicked.connect(self.selectNDfilter)
        b3.clicked.connect(self.selectNDfilter)
        b4.clicked.connect(self.selectNDfilter)
        b5.clicked.connect(self.selectNDfilter)
        b6.clicked.connect(self.selectNDfilter)

        layout.addWidget(b1)        
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(b4)
        layout.addWidget(b5)
        layout.addWidget(b6)
        
        self.horizontalGroupBox.setLayout(layout)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("561")
        layout = QGridLayout()

        b1 = QPushButton('ND 0', self)
        b2 = QPushButton('ND 0.5', self)
        b3 = QPushButton('ND 1', self)
        b4 = QPushButton('ND 1.3', self)
        b5 = QPushButton('ND 2', self)
        b6 = QPushButton('ND 3', self)

        #Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self) #Name of button
        #Label saying position
        self.label = QLabel()
        self.label.setText('Position : ')

        #Connecting buttons to functions
        b1.clicked.connect(self.selectNDfilter)
        b2.clicked.connect(self.selectNDfilter)
        b3.clicked.connect(self.selectNDfilter)
        b4.clicked.connect(self.selectNDfilter)
        b5.clicked.connect(self.selectNDfilter)
        b6.clicked.connect(self.selectNDfilter)
        b7.activated[str].connect(self. gotoPosition)   
        b8.clicked.connect(self.disconnectM)  

        layout.addWidget(self.label,0,0)  
        layout.addWidget(b7,0,1)  
        layout.addWidget(b8,2,0) 
        layout.addWidget(b1,0,2)        
        layout.addWidget(b2,1,2)
        layout.addWidget(b3,2,2)
        layout.addWidget(b4,3,2)
        layout.addWidget(b5,4,2)
        layout.addWidget(b6,5,2)
    
        self.horizontalGroupBox.setLayout(layout)

    def fw561Control(self):
        groupBox = QGroupBox('561')
        
        b1 = QRadioButton('ND 0', self)
        b2 = QRadioButton('ND 0.5', self)
        b3 = QRadioButton('ND 1', self)
        b4 = QRadioButton('ND 1.3', self)
        b5 = QRadioButton('ND 2', self)
        b6 = QRadioButton('ND 3', self)

        b1.setChecked(True)

        #Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self) #Name of button

        #Label saying position
        self.label = QLabel()
        posinfo = "Position : " + str(round(self.pos561,2))
        self.label.setText(posinfo)

        b1.clicked.connect(self.selectNDfilter)
        b2.clicked.connect(self.selectNDfilter)
        b3.clicked.connect(self.selectNDfilter)
        b4.clicked.connect(self.selectNDfilter)
        b5.clicked.connect(self.selectNDfilter)
        b6.clicked.connect(self.selectNDfilter)
        b7.activated[str].connect(self. gotoPosition)   
        b8.clicked.connect(self.disconnectM)  

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1,0,1)
        grid_layout.addWidget(b2,1,1)
        grid_layout.addWidget(b3,2,1)
        grid_layout.addWidget(b4,3,1)
        grid_layout.addWidget(b5,4,1)
        grid_layout.addWidget(b6,5,1)
        grid_layout.addWidget(b7,0,0)
        grid_layout.addWidget(b8,1,0)
        grid_layout.addWidget(self.label,2,0)
     
        groupBox.setLayout(grid_layout)

        return groupBox

    def fw488Control(self):
        groupBox = QGroupBox('488')
        
        b1 = QRadioButton('ND 0', self)
        b2 = QRadioButton('ND 0.5', self)
        b3 = QRadioButton('ND 1', self)
        b4 = QRadioButton('ND 1.3', self)
        b5 = QRadioButton('ND 2', self)
        b6 = QRadioButton('ND 3', self)

        b1.setChecked(True)

        #Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self) #Name of button

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1,0,1)
        grid_layout.addWidget(b2,1,1)
        grid_layout.addWidget(b3,2,1)
        grid_layout.addWidget(b4,3,1)
        grid_layout.addWidget(b5,4,1)
        grid_layout.addWidget(b6,5,1)
        grid_layout.addWidget(b7,0,0)
        grid_layout.addWidget(b8,1,0)

     
        groupBox.setLayout(grid_layout)

        return groupBox

    def fw460Control(self):
        groupBox = QGroupBox('460')
        
        b1 = QRadioButton('ND 0', self)
        b2 = QRadioButton('ND 0.5', self)
        b3 = QRadioButton('ND 1', self)
        b4 = QRadioButton('ND 1.3', self)
        b5 = QRadioButton('ND 2', self)
        b6 = QRadioButton('ND 3', self)

        b1.setChecked(True)

        #Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self) #Name of button

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1,0,1)
        grid_layout.addWidget(b2,1,1)
        grid_layout.addWidget(b3,2,1)
        grid_layout.addWidget(b4,3,1)
        grid_layout.addWidget(b5,4,1)
        grid_layout.addWidget(b6,5,1)
        grid_layout.addWidget(b7,0,0)
        grid_layout.addWidget(b8,1,0)

     
        groupBox.setLayout(grid_layout)

        return groupBox

    def fw405Control(self):
        groupBox = QGroupBox('405')
        
        b1 = QRadioButton('ND 0', self)
        b2 = QRadioButton('ND 0.5', self)
        b3 = QRadioButton('ND 1', self)
        b4 = QRadioButton('ND 1.3', self)
        b5 = QRadioButton('ND 2', self)
        b6 = QRadioButton('ND 3', self)

        b1.setChecked(True)

        #Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self) #Name of button

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1,0,1)
        grid_layout.addWidget(b2,1,1)
        grid_layout.addWidget(b3,2,1)
        grid_layout.addWidget(b4,3,1)
        grid_layout.addWidget(b5,4,1)
        grid_layout.addWidget(b6,5,1)
        grid_layout.addWidget(b7,0,0)
        grid_layout.addWidget(b8,1,0)

     
        groupBox.setLayout(grid_layout)

        return groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = QStyleFactory.create('Fusion')
    app.setStyle(s)
    ex = App()
    #dialog = Dialog()
    sys.exit(app.exec_())
