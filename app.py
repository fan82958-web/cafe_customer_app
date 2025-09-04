# app.py

# --- ↓↓↓ 1. 必要なモジュールをインポート ↓↓↓ ---
import sqlite3 # SQLiteを扱うためのモジュール
from flask import Flask, render_template, request, redirect, url_for # requestなどを追加

app = Flask(__name__)

# --- ↓↓↓ 2. データベース初期化のための関数 ↓↓↓ ---
def init_db():
    # 'database.db' という名前のデータベースに接続（なければ新規作成）
    conn = sqlite3.connect('database.db')
    # データベースを操作するためのカーソルを作成
    cursor = conn.cursor()

    # 'customers' テーブルが存在しない場合のみ、新しく作成する
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        visit_count INTEGER DEFAULT 0
    )
    ''')
    # 変更を確定
    conn.commit()
    # 接続を閉じる
    conn.close()

# --- ↓↓↓ 3. アプリ起動時に一度だけデータベースを初期化 ↓↓↓ ---
init_db()


# '/' というURLにアクセスがあった場合に、helloという関数を実行します
@app.route('/')
def hello():
    # 'index.html' を画面に表示するように指示します
    return render_template('index.html')


# このファイルが直接実行された場合に、アプリを起動します
if __name__ == '__main__':
    # デバッグモードを有効にして、開発しやすくします
    app.run(debug=True)