import matplotlib.pyplot as plt
import smbus
import math
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import requests

#サーバセットアップ
app = Flask(__name__)

#CORSを有効化
CORS(app)

#JSONデータを返すエンドポイント
@app.route('/data')
def get_data():
    global current_random_value
    data = {"jump": True}
    return jsonify(data)


#加速度センサセットアップ
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

coolTime = time.time() 
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


def jumpCheck(a):
    global jump, sign
    if(jump == True):
        if(ax > 0.0 and sign == False):
            jump = False
        if(ax < -0.0 and sign == True):
            jump = False
    else:
        if(ax > 0.6):
            jump = True
            sign = True
        if(ax < -0.6):
            jump = True
            sign = False
            

def accel():
    global ax, ay, az
    while True:
        try:
            ax, ay, az = getAccel()
        except:
            ax,ay,az = 0.0
        a = az + ay
        #ジャンプの検出
        jumpCheck(a)

        time.sleep(0.1)
    
    
#ジャンプの判定を更新し続けるスレッドを開始
if __name__ == '__main__':
    # 別スレッドでランダムな値を更新し続ける
    thread = threading.Thread(target=accel)
    thread.daemon = True
    thread.start()
    
    # Flaskサーバーの起動
    app.run(debug=False, host="0.0.0.0")