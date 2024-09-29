# -*- coding: utf-8 -*-

#graf
import matplotlib.pyplot as plt
#import numpy as np

import smbus
import math
from time import sleep
import time

DEV_ADDR = 0x68

ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

PWR_MGMT_1 = 0x6b
PWR_MGMT_2 = 0x6c   

bus = smbus.SMBus(1)
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)

jump = False
sign = True

def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val

def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):  return -((65535 - val) + 1)
    else:  return val

def get_temp():
    temp = read_word_sensor(TEMP_OUT)
    x = temp / 340 + 36.53      # data sheet(register map)より
    return x

def getGyro():
    x = read_word_sensor(GYRO_XOUT)/ 131.0
    y = read_word_sensor(GYRO_YOUT)/ 131.0
    z = read_word_sensor(GYRO_ZOUT)/ 131.0
    return [x, y, z]


def getAccel():
    x = read_word_sensor(ACCEL_XOUT)/ 16384.0
    y= read_word_sensor(ACCEL_YOUT)/ 16384.0
    z= read_word_sensor(ACCEL_ZOUT)/ 16384.0
    return [x, y, z]


def jumpCheck(ax):
    global jump, sign
    if(jump == True):
        if(ax > 0.0 and sign == False):
            print("fin!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = False
        if(ax < -0.0 and sign == True):
            print("fin!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = False
    else:
        if(ax > 0.3):
            print("jump!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = True
            sign = True
        if(ax < -0.3):
            print("jump!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = True
            sign = False
            
        
    

x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
y = [0.0,0.0,0.0,0.0,0.0,-2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0]

fig,ax = plt.subplots(1,1)
lines, = ax.plot(x,y)


while 1:
    try:
        ax, ay, az = getAccel()
        gx, gy, gz = getGyro()
    except:
        ax = 0.0
    
    #print ('x:{:4.3f}, y:{:4.3f}, z:{:4.3f}' .format(gx, gy, gz))
    #ジャンプの検出
    jumpCheck(ax)
    print('y:{:4.3f}'.format(y[0]))

    #最新の2秒間のデータを表示
    y.append(ax)
    del y[0]
    
    lines.set_data(x,y)
    
    plt.pause(.1)
    
    