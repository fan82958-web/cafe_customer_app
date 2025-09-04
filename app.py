# app.py

# FlaskというWebフレームワークをインポートします
from flask import Flask, render_template

# Flaskアプリのインスタンスを作成します
app = Flask(__name__)

# --- ルーティングの設定 ---
# '/' というURLにアクセスがあった場合に、helloという関数を実行します
@app.route('/')
def hello():
    # 'index.html' を画面に表示するように指示します
    return render_template('index.html')

# --- アプリの起動 ---
# このファイルが直接実行された場合に、アプリを起動します
if __name__ == '__main__':
    # デバッグモードを有効にして、開発しやすくします
    app.run(debug=True)