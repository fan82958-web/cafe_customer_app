# app.py

import sqlite3
# render_template だけでなく、g もインポートする
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)

# --- データベース接続のヘルパー関数 ---
DATABASE = 'database.db'

def get_db():
    # g はリクエストごとに存在する特殊なオブジェクト。
    # 同じリクエスト内で get_db が複数回呼ばれても、接続は一度だけ行われる。
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # 辞書のように列名でアクセスできるようにする
        db.row_factory = sqlite3.Row 
    return db

# アプリケーションコンテキストが終了する際に、データベース接続を閉じる
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- データベース初期化 (変更なし) ---
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- ↓↓↓ ここからが今回のメイン ↓↓↓ ---

@app.route('/')
def index():
    db = get_db()
    customers_data = db.execute('SELECT * FROM customers ORDER BY id').fetchall()
    
    for customer in customers_data:
        print(dict(customer)) # 辞書形式で見やすく表示
    print("---------------------------------")
    
    return render_template('index.html', customers=customers_data)

# --- ↑↑↑ ここまでが今回のメイン ↑↑↑ ---
# app.py の末尾に追記

# --- 新規顧客を追加するための処理 ---
@app.route('/add', methods=['POST'])
def add_customer():
    # フォームから 'customer_name' の値を取得
    name = request.form['customer_name']
    
    # データベースに接続
    db = get_db()
    # 新しい顧客をcustomersテーブルに挿入
    db.execute('INSERT INTO customers (name) VALUES (?)', (name,))
    # 変更を確定
    db.commit()
    
    # 登録が終わったら、トップページにリダイレクト（再表示）する
    return redirect(url_for('index'))
# このファイルが直接実行された場合にアプリを起動 (変更なし)
if __name__ == '__main__':
    # データベース初期化用のコマンドを追加 (後で使う)
    # init_db() # 起動時に毎回初期化するのはやめる
    app.run(debug=True)