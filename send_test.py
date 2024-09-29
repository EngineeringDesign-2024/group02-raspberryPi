import time
import requests

#サーバ側の受信サーブレットのURL
URL='http://10.22.241.48.:8080/webapp-pi/saveImageServlet' 


time = 0
while True:
    #連続して送らないようにタイマーセット
    if( time.time() - timer >= 10 ):

        timer = time.time()
        
        #file = open('./image.jpg','rb')
        #img_data = file.read()
        #file.close
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

    else:
        # print("No motion")
        pass

