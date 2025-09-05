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

# app.py の index() 関数を書き換える

# URLに<int:customer_id>を追加し、デフォルト値をNoneに
@app.route('/', defaults={'customer_id': None})
@app.route('/<int:customer_id>')
def index(customer_id):
    db = get_db()
    customers_data = db.execute('SELECT * FROM customers ORDER BY name').fetchall()
    
    selected_customer = None
    visits_data = []

    if customer_id:
        # 顧客が選択されている場合
        selected_customer = db.execute('SELECT * FROM customers WHERE id = ?', (customer_id,)).fetchone()
        visits_data = db.execute('SELECT * FROM visits WHERE customer_id = ? ORDER BY visit_date DESC', (customer_id,)).fetchall()

    return render_template(
        'index.html', 
        customers=customers_data, 
        selected_customer=selected_customer, 
        visits=visits_data
    )

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

# app.py の末尾に追記

# --- 来店履歴を追加するための処理 ---
@app.route('/<int:customer_id>/add_visit', methods=['POST'])
def add_visit(customer_id):
    # フォームからデータを取得
    visit_date = request.form['visit_date']
    orders = request.form['orders']
    memo = request.form['memo']
    
    db = get_db()
    # 1. visitsテーブルに新しい履歴を挿入
    db.execute(
        'INSERT INTO visits (customer_id, visit_date, orders, memo) VALUES (?, ?, ?, ?)',
        (customer_id, visit_date, orders, memo)
    )
    
    # 2. customersテーブルの来店回数(visit_count)を1増やす
    db.execute(
        'UPDATE customers SET visit_count = visit_count + 1 WHERE id = ?',
        (customer_id,)
    )
    
    # 3. 変更をデータベースに確定
    db.commit()
    
    # 登録が終わったら、同じ顧客の詳細ページにリダイレクトして結果をすぐに見られるようにする
    return redirect(url_for('index', customer_id=customer_id))

if __name__ == '__main__':
    # データベース初期化用のコマンドを追加 (後で使う)
    # init_db() # 起動時に毎回初期化するのはやめる
    app.run(debug=True)