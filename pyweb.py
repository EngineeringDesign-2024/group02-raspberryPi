from flask import Flask, jsonify
from flask_cors import CORS
import time
import random
import threading

app = Flask(__name__)

# CORSを有効化
CORS(app)


# ランダムな値を格納するグローバル変数
current_random_value = 0


# JSONデータを返すエンドポイント
@app.route('/data')
def get_data():
    global current_random_value
    data = {"jump": True}
    return jsonify(data)
  


# ランダムな値を定期的に更新する関数
def update_random_value():
    global current_random_value
    while True:
        current_random_value = random.randint(1, 100)  # 1〜100のランダムな値
        time.sleep(2)  # 2秒ごとに値を更新




# バックグラウンドでランダムな値を更新し続けるスレッドを開始
if __name__ == '__main__':
    # 別スレッドでランダムな値を更新し続ける
    thread = threading.Thread(target=update_random_value)
    thread.daemon = True
    thread.start()
    
    # Flaskサーバーの起動
    app.run(debug=True)


