from flask import Flask, Blueprint, render_template, send_from_directory
from api import Api
import os
import sqlite3

app = Flask(__name__)
app.register_blueprint(Api)

def create_database():
    if(os.path.isfile('instance/messages.db')):
        return
    with sqlite3.connect('instance/messages.db') as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE "messages" (
        "id" INTEGER,
        "message" TEXT,
        "username" TEXT,
        "date" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        )''')
        cur.close()
        conn.commit()

def get_all_messages():
    with sqlite3.connect('instance/messages.db') as conn:
        cur = conn.cursor()
        messages = cur.execute('''SELECT message, username, date FROM messages''').fetchall()
        cur.close()
    return messages

@app.route('/style.css')
def send_css():
    return send_from_directory('static', 'style.css')

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/form_handler.js')
def formHandler():
    return send_from_directory('static', 'formHandler.js')

@app.route('/')
def index():
    return render_template('index.html', messages = get_all_messages())

if(__name__ == '__main__'):
    create_database()
    app.run()