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

#filter_wheels = FW103S()
#positions = filter_wheels.initPositions()
print("Pretending filter wheels are initialized")


class App(QWidget):

    def __init__(self):
        super().__init__()

        # For initializing size and position of main window wrt computer screen
        self.title = 'FW103S Control'
        self.left = 600
        self.top = 300
        self.width = 550
        self.height = 500

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('p202.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)

        grid = QGridLayout()
        grid.addWidget(self.fw561Control(), 0, 0)
        grid.addWidget(self.fw488Control(), 1, 0)
        grid.addWidget(self.fw460Control(), 0, 1)
        grid.addWidget(self.fw405Control(), 1, 1)
        self.setLayout(grid)

        self.show()

    @pyqtSlot()
    def disconnectM(self, pressed):
        print('Terminating connection with motor and releasing allocated memory...')
        # filter_wheels.cleanUpAll()
        #print("Wavelength = ", wavelength)
        print('Done.')

    @pyqtSlot()
    def gotoPosition(self, serialno=None, pos=None):
        print('Moving to specified position...')
        print('Done.')

    @pyqtSlot()
    def selectNDfilter(self, wavelength=None):
        print('Moving to selected ND filter...')
        nd = [['ND 0', 0.0], ['ND 0.5', 60.0], ['ND 1', 120.0],
              ['ND 1.3', 180.0], ['ND 2', 240.0], ['ND 3', 300]]
        for (ndval, pos) in nd:
            if ndval == self.sender().text():
                position = pos
            else:
                pass
        # filter_wheels.gotoPos(position,wavelength)
        # Motor1.mAbs(position)
        print('Done.')
        # filter_wheels.getPosition(wavelength)
        posinfo = "Position : " + str(round(position, 2))
        self.label.setText(posinfo)

    def fw561Control(self):
        groupBox = QGroupBox('561')

        # b1 = QRadioButton('ND 0', self)
        # b2 = QRadioButton('ND 0.5', self)
        # b3 = QRadioButton('ND 1', self)
        # b4 = QRadioButton('ND 1.3', self)
        # b5 = QRadioButton('ND 2', self)
        # b6 = QRadioButton('ND 3', self)

        b1.setChecked(True)

        # Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self)  # Name of button

        # Label saying position
        self.label = QLabel()
        #posinfo = "Position : " + str(round(self.pos561, 2))
        self.label.setText("posinfo")

        b1.clicked.connect(self.selectNDfilter)
        b2.clicked.connect(self.selectNDfilter)
        b3.clicked.connect(self.selectNDfilter)
        b4.clicked.connect(self.selectNDfilter)
        b5.clicked.connect(self.selectNDfilter)
        b6.clicked.connect(self.selectNDfilter)
        b7.activated[str].connect(self. gotoPosition)
        b8.clicked[bool].connect(self.disconnectM)

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1, 0, 1)
        grid_layout.addWidget(b2, 1, 1)
        grid_layout.addWidget(b3, 2, 1)
        grid_layout.addWidget(b4, 3, 1)
        grid_layout.addWidget(b5, 4, 1)
        grid_layout.addWidget(b6, 5, 1)
        grid_layout.addWidget(b7, 0, 0)
        grid_layout.addWidget(b8, 1, 0)
        grid_layout.addWidget(self.label, 2, 0)

        groupBox.setLayout(grid_layout)

        return groupBox

    def fw488Control(self):
        groupBox = QGroupBox('488')

        tb = ButtonBlock()

        # Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self)  # Name of button

        # Label saying position
        self.label = QLabel()
        #posinfo = "Position : " + str(round(self.pos561, 2))
        self.label.setText("posinfo")

        b7.activated[str].connect(self. gotoPosition)
        b8.clicked.connect(self.disconnectM)

        grid_layout = QGridLayout()
        grid_layout.addWidget(b7, 0, 0)
        grid_layout.addWidget(b8, 1, 0)
        grid_layout.addWidget(self.label, 2, 0)

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

        # Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self)  # Name of button

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1, 0, 1)
        grid_layout.addWidget(b2, 1, 1)
        grid_layout.addWidget(b3, 2, 1)
        grid_layout.addWidget(b4, 3, 1)
        grid_layout.addWidget(b5, 4, 1)
        grid_layout.addWidget(b6, 5, 1)
        grid_layout.addWidget(b7, 0, 0)
        grid_layout.addWidget(b8, 1, 0)

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

        # Dropdown menu for selecting wheel position
        b7 = QComboBox(self)
        b7.addItem("0.0")
        b7.addItem("60.0")
        b7.addItem("120.0")
        b7.addItem("180.0")
        b7.addItem("240.0")
        b7.addItem("300.0")

        #Button : Disconnect
        b8 = QPushButton('Disconnect', self)  # Name of button

        grid_layout = QGridLayout()
        grid_layout.addWidget(b1, 0, 1)
        grid_layout.addWidget(b2, 1, 1)
        grid_layout.addWidget(b3, 2, 1)
        grid_layout.addWidget(b4, 3, 1)
        grid_layout.addWidget(b5, 4, 1)
        grid_layout.addWidget(b6, 5, 1)
        grid_layout.addWidget(b7, 0, 0)
        grid_layout.addWidget(b8, 1, 0)

        groupBox.setLayout(grid_layout)

        return groupBox


class ButtonBlock(QtGui.QWidget):

    def __init__(self, *args):
        super(QtGui.QWidget, self).__init__()
        grid = QtGui.QGridLayout()

        names = ('ND 0', 'ND 0.5', 'ND 1', 'ND 1.3', 'ND 2', 'ND 3')
        for i, name in enumerate(names):
            button = QtGui.QRadioButton(name, self)
            button.clicked.connect(self.make_calluser(name))
            # row, col = divmod(i, 5)
            grid.addWidget(button, i, 1)
            if i == 0:
                button.setChecked(True)
            else:
                pass

        self.setLayout(grid)

    def make_calluser(self, name):
        def calluser():
            print(name)
        return calluser


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = QStyleFactory.create('Fusion')
    app.setStyle(s)
    ex = App()
    #dialog = Dialog()
    sys.exit(app.exec_())
