from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# DB 생성
def init_db():
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    
    # 기존 테이블이 있는지 확인
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='guestbook'")
    table_exists = c.fetchone() is not None
    
    if not table_exists:
        # 새 테이블 생성
        c.execute('''
            CREATE TABLE guestbook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    else:
        # 기존 테이블에 created_at 컬럼 추가 (없는 경우에만)
        try:
            c.execute('ALTER TABLE guestbook ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        except sqlite3.OperationalError:
            # 컬럼이 이미 존재하는 경우 무시
            pass
    
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        c.execute('INSERT INTO guestbook (name, message) VALUES (?, ?)', (name, message))
        conn.commit()
        return redirect('/')

    c.execute('SELECT name, message, created_at FROM guestbook ORDER BY id DESC')
    entries = c.fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    init_db()
    # 배포 환경에서는 debug=False, 로컬에서는 debug=True
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
