# -*- coding: utf-8 -*-
"""
Example code showing how to control Thorlabs TDC Motors using PyAPT
V1.2
20141125 V1.0    First working version
20141201 V1.0a   Updated to short notation
20150324 V1.1    Added more descriptions
20150417 V1.2    Implemented motor without serial

Michael Leung
mcleung@stanford.edu
"""

# Import APTMotor class from PyAPT
from PyAPT.PyAPT import APTMotor
import time

# Create object corresponding to the motor.
Motor1 = APTMotor(80831436, HWTYPE=29) # The number should correspond to the serial number.
# Use help APTMotor to obtain full list of hardware (HW) supported.

# Note: You can control multiple motors by creating more APTMotor Objects
def ApplyFilter(MotorHandle, ND):
    if ND == 0 :
        MotorHandle.go_home()
        time.sleep(.5)
    elif ND == 0.5 :
        MotorHandle.mAbs(60.0)
        time.sleep(.5)
    elif ND == 1 :
        MotorHandle.mAbs(120.0)
        time.sleep(.5)
    elif ND == 1.3 :
        MotorHandle.mAbs(180.0)
        time.sleep(.5)
    elif ND == 2 :
        MotorHandle.mAbs(240.0)
        time.sleep(.5)
    elif ND == 3 :
        MotorHandle.mAbs(300.0)
        time.sleep(.5)

# Obtain current position of motor

if __name__ == '__main__':
    #print(Motor1.getHardwareInformation())
    Motor1.initializeHardwareDevice()
    #print(Motor1.getPos())
    kapish = True
    while(kapish):
        ND = float(input("Enter ND filter OD value : "))
        ApplyFilter(Motor1, ND)
        if input("Again? : ")=='y':
            kapish = True
        else :
            kapish = False
    Motor1.cleanUpAPT()

# You can control multiple motors by creating more APTMotor Objects
# Serial numbers can be added later by using setSerialNumber and initializeHardwareDevice
# This functionality is particularly useful in the GUI setup.

# Motor2 = APTMotor()
# Motor2.setSerialNumber(83828393)
# Motor2.initializeHardwareDevice()
# print(Motor2.getPos())

# Move motor forward by 1mm, wait half a second, and return to original position.
# mRel is move relative. mAbs is move absolute (go to position xxx)

# Motor1.mRel(1) # advance 1mm
# time.sleep(.5)
# Motor1.mRel(-1) # retract 1mm

# time.sleep(1)

# Move motor forward by 1mm, wait half a second, and return to original position, at a velocity of 0.5mm/sec

# motVel = 0.5 #motor velocity, in mm/sec
# Motor1.mcRel(1, motVel) # advance 1mm
# time.sleep(.5)
# Motor1.mcRel(-1, motVel) # retract 1mm


# Clean up APT object, free up memory

