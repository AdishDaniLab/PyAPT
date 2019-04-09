
# -*- coding: utf-8 -*-
"""
APT Motor Controller GUI for Thorlabs

V1.0
20150417 V1.0    First working version

Michael Leung
mcleung@stanford.edu
"""
#Title: OpenFFOCT
version='1.0'
#Date: April 17, 2015
#Python Version 2.7.9


import os
import platform
import sys
# import PyQt5.QtWidgets as QtWidgets
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import struct
import time
# import multiprocessing
# import pdb

from PyAPT.PyAPT import APTMotor
# TODO: Implement multiprocess and OpenCL
#MULTIPROCESS = False
#USEOCL = False
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, verbose=False):
        """
        Main window
        """
        self.setWindowTitle("OpenFFOCT "+version)

        #Set central widget - Main Scan window
        self.mainWindow = MainScanWindow(self.dataObject)
        self.setCentralWidget(self.mainWindow)

        #Set main toolbar
        mainToolBar = self.addToolBar("Tools")


    def closeEvent(self, event):
        """
        Clean up child widgets before exit
        1) Close the active COM port before application exit
        2) Kill the child process if MULTIPROCESS is True
        """
        self.mcuWidget.MCU.close()
        self.mainWindow.dataObject.terminate()

        event.accept()

class widgetAPT(QtWidgets.QWidget):
    # pdb.set_trace()
    #def __init__(self, parent = None, serial=00000000, verbose=False):
    def __init__(self, parent = None, serial=80831436, verbose=False):
        super(widgetAPT, self).__init__(parent)
        self.resize(200, 100)
        #self.move(100, 100)
        #setGeometry sets both location and size
        #self.setGeometry(50, 50, 1180, 900)
        self.setWindowTitle('APT Motor')
        #self.m = APTMotor(0)

        # QT GridLayout
        # TODO: Implement GridLayout
        #grid = QGridLayout()
        # Layout objects
        sAuthor = QtWidgets.QLabel("QT-APT", self)
        sAuthor.resize(100, 20)
        sAuthor.move(100, 0)
        sAuthor.setAlignment(QtCore.Qt.AlignRight)
        sVersion = QtWidgets.QLabel("v1.0.0", self)
        sVersion.resize(100, 20)
        sVersion.move(100, 15)
        sVersion.setAlignment(QtCore.Qt.AlignRight)
        sEmail = QtWidgets.QLabel("Michael Leung", self)
        sEmail.resize(100, 40)
        sEmail.move(100, 30)
        sEmail.setAlignment(QtCore.Qt.AlignRight)


        # Motor Serial Number
        sSer = QtWidgets.QLabel("Serial:", self)
        sSer.resize(60, 20)
        sSer.move(0, 0)
        self.txtSerial = QtWidgets.QSpinBox(self)
        self.txtSerial.resize(70,20)
        self.txtSerial.move(30,0)
        self.txtSerial.setRange(0, 99999999)
        self.txtSerial.setSingleStep(1)
        self.txtSerial.setValue(83840946)
        # qle.textChanged[str].connect(self.onChanged) #do onChanged when changed
        self._Motor_ = APTMotor(verbose=verbose)

        # Motor Connect
        self.btnConnect = QtWidgets.QPushButton("Connect", self)
        self.btnConnect.setStyleSheet("background-color: grey")
        self.btnConnect.setText("Connect")
        self.btnConnect.setCheckable(True)
        self.btnConnect.setToolTip("Connect to Motor")
        self.btnConnect.resize(50, 20)
        self.btnConnect.move(105, 0)
        self.btnConnect.clicked[bool].connect(self.connectAPT)

        sPos = QtWidgets.QLabel("Pos:", self)
        sPos.resize(70, 20)
        sPos.move(0, 25)
        self.txtPos = QtWidgets.QDoubleSpinBox(self)
        self.txtPos.resize(60, 20)
        self.txtPos.move(30, 25)
        #self.txtPos.setMaxLength(7)
        self.txtPos.setRange(0, 20)
        self.txtPos.setSingleStep(.1)
        self.txtPos.setDecimals(5)
        self.txtPos.setValue(0.0000000)
        self.txtPos.setToolTip("Current Motor Position")
        #self.txtPos.setValidator( QDoubleValidator(0, 100, 2) )
        self.txtPos.setEnabled(False)

        # Go to position
        btnGOp = QtWidgets.QPushButton("Go", self)
        btnGOp.resize(25, 20)
        btnGOp.move(100, 25)
        btnGOp.clicked.connect(lambda: self.motAbs(float(self.txtPos.text())))

        # Movement buttons
        btnN3 =QtWidgets.QPushButton("-100", self)
        btnN3.resize(32, 20)
        btnN3.move(0, 50)
        btnN3.clicked.connect(lambda: self.motRel(-.1))

        btnN2 = QtWidgets.QPushButton("-10", self)
        btnN2.resize(32, 20)
        btnN2.move(33, 50)
        btnN2.clicked.connect(lambda: self.motRel(-.01))

        btnN1 = QtWidgets.QPushButton("-1", self)
        btnN1.resize(32, 20)
        btnN1.move(66, 50)
        btnN1.clicked.connect(lambda: self.motRel(-.001))

        btnP1 = QtWidgets.QPushButton("+1", self)
        btnP1.resize(32, 20)
        btnP1.move(100, 50)
        btnP1.clicked.connect(lambda: self.motRel(.001))

        btnP2 = QtWidgets.QPushButton("+10", self)
        btnP2.resize(32, 20)
        btnP2.move(133, 50)
        btnP2.clicked.connect(lambda: self.motRel(.01))

        btnP3 = QtWidgets.QPushButton("+100", self)
        btnP3.resize(32, 20)
        btnP3.move(166, 50)
        btnP3.clicked.connect(lambda: self.motRel(.1))


        sVel = QtWidgets.QLabel("Vel:", self)
        sVel.resize(60, 20)
        sVel.move(0, 75)
        self.txtVel = QtWidgets.QDoubleSpinBox(self)
        self.txtVel.resize(60, 20)
        self.txtVel.move(30, 75)
        #self.txtVel.setMaxLength(7)
        self.txtVel.setRange(0, 2.2)
        self.txtVel.setSingleStep(.1)
        self.txtVel.setValue(0.000)
        self.txtVel.setToolTip("Current Motor Position")
        self.txtVel.setEnabled(False)
        # Go to velocity
        btnGOv = QtWidgets.QPushButton("Go", self)
        btnGOv.resize(25, 20)
        btnGOv.move(100, 75)
        btnGOv.clicked.connect(lambda: self._Motor_.setVel(float(self.txtVel.text())))

        sBack = QtWidgets.QLabel("Backlash:", self)
        sBack.resize(60, 20)
        sBack.move(130, 75)
        self.cbBacklash = QtWidgets.QCheckBox(self)
        self.cbBacklash.resize(60, 20)
        self.cbBacklash.move(180, 75)


        self.show()

    def connectAPT(self, pressed):
        if pressed:
            #APT Motor connect
            Serial = int(self.txtSerial.text())
            self._Motor_.setSerialNumber(Serial)
            self._Motor_.initializeHardwareDevice()

            # Success
            self.btnConnect.setStyleSheet("background-color: green")
            self.btnConnect.setText("Connected")

            self.txtSerial.setEnabled(False)
            self.txtPos.setEnabled(True)
            # Update text to show position
            self.txtPos.setValue( self._Motor_.getPos() )

            self.txtVel.setEnabled(True)
            _, _, maxVel = self._Motor_.getVelocityParameters()
            self.txtVel.setValue( maxVel )

            return True
        else:
            #APT Motor disconnect
            self._Motor_.cleanUpAPT()
            # Success
            self.btnConnect.setStyleSheet("background-color: grey")
            self.btnConnect.setText("Connect")

            self.txtSerial.setEnabled(True)
            self.txtPos.setEnabled(False)
            self.txtVel.setEnabled(False)
            self.txtPos.setValue(0.0000)
            self.txtPos.setToolTip("Current Motor Position")
            return True

    def motRel(self, relDistance):
        if self.cbBacklash.isChecked() :
            self._Motor_.mbRel(relDistance)
        else:
            self._Motor_.mRel(relDistance)
        # Update text to show position
        self.txtPos.setValue( self._Motor_.getPos() )

    def motAbs(self, absDistance):
        if self.cbBacklash.isChecked() :
            self._Motor_.mbAbs(absDistance)
        else:
            self._Motor_.mAbs(absDistance)
        # Update text to show position
        self.txtPos.setValue( self._Motor_.getPos() )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    splash_pix = QtGui.QPixmap('')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    form = widgetAPT(parent=None, serial = 80831436, verbose=True)
    form.setWindowState(QtCore.Qt.WindowMaximized)
    form.show()
    splash.finish(form)
    sys.exit(app.exec_())