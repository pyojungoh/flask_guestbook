from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# DB 생성
def init_db():
    conn = sqlite3.connect('guestbook.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
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

    c.execute('SELECT name, message FROM guestbook ORDER BY id DESC')
    entries = c.fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
