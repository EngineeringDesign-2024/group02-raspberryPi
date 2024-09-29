import matplotlib.pyplot as plt
import smbus
import math
from time import sleep
import time
import time
import requests

#サーバ側の受信サーブレットのURL
URL='http://10.22.241.48.:8080/webapp-pi/saveImageServlet' 

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
            sendMessage()
        if(ax < -0.3):
            print("jump!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = True
            sign = False
            sendMessage()
            
        
def sendMessage():
    # HTTPで送るデータをセット
    PAYLOAD = {
        "text_tag":('jumped!', 'plain/text')
    }
    
    # HTTPのPOSTメゾッドを使って、サーバへファイルを送る
    # 受信側のサーブレットではdoGet()ではなくdoPost()に処理を書く  
    response = requests.post(URL, files = PAYLOAD)

    # (デバッグ用)通信内容の表示
    print('REQUEST (POST): ' + URL)
    print('RESPONSE (' + str(response.status_code) + '): ' + response.text)



x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
y = [0.0,0.0,0.0,0.0,0.0,-2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0]

fig,ax = plt.subplots(1,1)
lines, = ax.plot(x,y)


while 1:
    try:
        ax, ay, az = getAccel()
    except:
        ax = 0.0
    
    #ジャンプの検出
    jumpCheck(ax)
    print('y:{:4.3f}'.format(y[0]))

    #最新の2秒間のデータを表示
    y.append(ax)
    del y[0]
    
    lines.set_data(x,y)
    
    plt.pause(.1)
    
    