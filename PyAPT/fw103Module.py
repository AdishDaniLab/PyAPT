#!/usr/bin/env python
"""
FW103S Thorlabs filter wheel control.

Gayatri 04/19
"""
from PyAPT.PyAPT import APTMotor
import time
import traceback


class FW103S():

    def __init__(self):
        super().__init__()
        # Initializing motors
        try:
            self.Motor1 = APTMotor(80831436, HWTYPE=29)
            self.Motor2 = APTMotor(80831430, HWTYPE=29)
            self.Motor3 = APTMotor(80831429, HWTYPE=29)
            self.Motor4 = APTMotor(80828888, HWTYPE=29)

            self.Motor1.initializeHardwareDevice()
            self.Motor2.initializeHardwareDevice()
            self.Motor3.initializeHardwareDevice()
            self.Motor4.initializeHardwareDevice()
            print("fw103s : Initialized all hardware")
            time.sleep(.1)
        except:
            print(traceback.format_exc())
            print("Failed to connect to FW103S filter wheels !")
            # self.Motor1.cleanUpAPT()
            # self.Motor2.cleanUpAPT()
            # self.Motor3.cleanUpAPT()
            # self.Motor4.cleanUpAPT()
            #print("Did a proper shutdown!")
      
       
    def cleanUpAll(self):
        self.Motor1.cleanUpAPT()
        self.Motor2.cleanUpAPT()
        self.Motor3.cleanUpAPT()
        self.Motor4.cleanUpAPT()

    def initPositions(self):
        p561 = self.Motor1.getPos()
        p488 = self.Motor2.getPos()
        p460 = self.Motor3.getPos()
        p405 = self.Motor4.getPos()
        positions = [p561, p488, p460, p405]
        return positions
        

    def gotoPos(self, position, wavelength):

        if wavelength == 561:
            self.Motor1.mAbs(position)
            # print('fw103s : Moving ',wavelength, ' filter wheel to position', position )
        if wavelength == 488:
            self.Motor2.mAbs(position)
            # print('fw103s : Moving ',wavelength, ' filter wheel to position', position )
        if wavelength == 460:
            self.Motor3.mAbs(position)
            # print('fw103s : Moving ',wavelength, ' filter wheel to position', position )
        if wavelength == 405:
            self.Motor4.mAbs(position)
            # print('fw103s : Moving ',wavelength, ' filter wheel to position', position )
        else:
            pass

    def getPosition(self,wavelength):

        if wavelength == 561:
            pos = self.Motor1.getPos()
            # pos = 0.0
        if wavelength == 488:
            pos = self.Motor2.getPos()
            # pos = 60.0
        if wavelength == 460:
            pos = self.Motor3.getPos()
            # pos = 240.0
        if wavelength == 405:
            pos = self.Motor4.getPos()
            # pos = 120.0
        else:
            pass
        return pos


