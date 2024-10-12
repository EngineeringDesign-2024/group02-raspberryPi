import matplotlib.pyplot as plt
import smbus
import math
import time
import requests


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
        if(ax > 0.6):
            print("jump!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = True
            sign = True
        if(ax < -0.6):
            print("jump!!!!!!!!!!!!!!!!!!!!!!!!!")
            jump = True
            sign = False

#グラフセットアップ
x_data = range(1,21)
ax_data = [-2.0,2.0]
ay_data = [-2.0,2.0]
az_data = [-2.0,2.0]
for _ in range(18):
    ax_data.append(0.0)
    ay_data.append(0.0)
    az_data.append(0.0)

plt.ion()  # インタラクティブモードを有効化
fig, axs = plt.subplots()

# ラベルとタイトル
axs.set_title('Real-time acceleration')
axs.set_xlabel('Time (100ms)')
axs.set_ylabel('acceleration')

# 初期プロットを設定
line1, = axs.plot(x_data, ax_data, label='ax', color='r')
line2, = axs.plot(x_data, ay_data, label='ay', color='g')
line3, = axs.plot(x_data, az_data, label='az', color='b')

# 凡例を表示
axs.legend()


while True:
    try:
        ax, ay, az = getAccel()
    except:
        ax,ay,az = 0.0
    a = ay+az
    #ジャンプの検出
    jumpCheck(a)

    #新しいデータをリストに追加
    ax_data.append(ax)
    ay_data.append(ay)
    az_data.append(az)
    del ax_data[0]
    del ay_data[0]
    del az_data[0]

    #グラフを再描画
    plt.draw()
    #0.1秒待機
    plt.pause(1)

    
    