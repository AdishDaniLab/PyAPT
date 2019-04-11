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
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from PyAPT.PyAPT import APTMotor
from PyAPT.fw103Module import FW103S

filter_wheels = FW103S()

class App(QWidget):
    '''
    The main GUI window. There is only one.
    '''

    def __init__(self):
        super().__init__()

        # For initializing size and position of main window wrt computer screen
        self.title = 'FW103S Control'
        self.left = 600
        self.top = 300
        self.width = 400
        self.height = 400
        # Check initial positions of filter wheels 
        self.positions = filter_wheels.initPositions()
        # Initialize user interface
        self.initUI()

    def initUI(self):
        # Set window title , icon and geometry 
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('p202.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Divide box into 4 parts,one part for each filter wheel
        grid = QGridLayout()
        grid.addWidget(self.fw561Control(), 0, 0)
        grid.addWidget(self.fw488Control(), 1, 0)
        grid.addWidget(self.fw460Control(), 0, 1)
        grid.addWidget(self.fw405Control(), 1, 1)
        self.setLayout(grid)

        self.show()
        # This is for making sure filter wheels are shutdown properly on close
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        '''
        Shut down motors
        '''
        print('Closing application..')
        filter_wheels.cleanUpAll()
        print('Shutting down motors...')
        print('Done')

    @pyqtSlot()
    def setPosition(self, wavelength):
        '''
        Move filter wheels to indicated nd filter position
        '''
        nd = [['ND 0', 0.0], ['ND 0.5', 60.0], ['ND 1', 120.0],
              ['ND 1.3', 180.0], ['ND 2', 240.0], ['ND 3', 300]]

        #Each filter wheel has a fixed angular position      

        for (ndval, pos) in nd:
            if ndval == self.sender().text():
                position = pos
            else:
                pass
        filter_wheels.gotoPos(position,wavelength)
        ang = filter_wheels.getPosition(wavelength)
        posinfo = "Position : " + str(round(ang, 2))
        labels = [[561, self.label1], [488, self.label2], [460, self.label3], [405, self.label4]]
        for (wv, name) in labels:
            if wavelength == wv:
                name.setText(posinfo) # Update position display
            else:
                pass
        
    def fw561Control(self):
        '''
        561 illumination path filter-wheel control
        '''
        groupBox = QGroupBox('561')
        grid = QGridLayout()
        wavelength = float(561)
        #Add buttons for nd filters
        names = ('ND 0', 'ND 0.5', 'ND 1', 'ND 1.3', 'ND 2', 'ND 3')
        for i, name in enumerate(names):
            button = QRadioButton(name, self)
            button.clicked.connect(lambda: self.setPosition(wavelength))
            grid.addWidget(button, i, 1)
            if i == 0:
                button.setChecked(True)
            else:
                pass
        # Label saying position
        self.label1 = QLabel()
        posinfo = "Position : " + str(round(self.positions[0], 2))
        self.label1.setText(posinfo)

        grid.addWidget(self.label1, 2, 0)
        groupBox.setLayout(grid)
        return groupBox

    def fw488Control(self):
        '''
        488 illumination path filter-wheel control
        '''
        groupBox = QGroupBox('488')
        grid = QGridLayout()
        wavelength = float(488)
        names = ('ND 0', 'ND 0.5', 'ND 1', 'ND 1.3', 'ND 2', 'ND 3')
        for i, name in enumerate(names):
            button = QRadioButton(name, self)
            button.clicked.connect(lambda: self.setPosition(wavelength))
            grid.addWidget(button, i, 1)
            if i == 0:
                button.setChecked(True)
            else:
                pass
        # Label saying position
        self.label2 = QLabel()
        posinfo = "Position : " + str(round(self.positions[1], 2))
        self.label2.setText(posinfo)

        grid.addWidget(self.label2, 2, 0)
        groupBox.setLayout(grid)
        return groupBox

    def fw460Control(self):
        '''
        460 illumination path filter-wheel control
        '''
        groupBox = QGroupBox('460')
        grid = QGridLayout()
        wavelength = float(460)
        names = ('ND 0', 'ND 0.5', 'ND 1', 'ND 1.3', 'ND 2', 'ND 3')
        for i, name in enumerate(names):
            button = QRadioButton(name, self)
            button.clicked.connect(lambda: self.setPosition(wavelength))
            grid.addWidget(button, i, 1)
            if i == 0:
                button.setChecked(True)
            else:
                pass


        # Label saying position
        self.label3 = QLabel()
        posinfo = "Position : " + str(round(self.positions[2], 2))
        self.label3.setText(posinfo)

        grid.addWidget(self.label3, 2, 0)
        groupBox.setLayout(grid)
        return groupBox

    def fw405Control(self):
        '''
        405 illumination path filter-wheel control
        '''
        groupBox = QGroupBox('405')
        grid = QGridLayout()
        wavelength = float(405)
        names = ('ND 0', 'ND 0.5', 'ND 1', 'ND 1.3', 'ND 2', 'ND 3')
        for i, name in enumerate(names):
            button = QRadioButton(name, self)
            button.clicked.connect(lambda: self.setPosition(wavelength))
            grid.addWidget(button, i, 1)
            if i == 0:
                button.setChecked(True)
            else:
                pass

        # Label saying position
        self.label4 = QLabel()
        posinfo = "Position : " + str(round(self.positions[3], 2))
        self.label4.setText(posinfo)

        grid.addWidget(self.label4, 2, 0)
        groupBox.setLayout(grid)
        return groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = QStyleFactory.create('Fusion') # Fusion is a button style
    app.setStyle(s)
    ex = App()
    sys.exit(app.exec_())
