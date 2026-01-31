from flask import Blueprint, render_template, send_from_directory
import sqlite3


router = Blueprint('router', __name__)

@router.route('/style.css')
def send_css():
    return send_from_directory('static', 'style.css')

@router.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'favicon.ico')

@router.route('/form_handler.js')
def send_formHandler():
    return send_from_directory('static', 'formHandler.js')

@router.route('/')
def index():
    with sqlite3.connect('instance/messages.db') as conn:
        cur = conn.cursor()
        messages = cur.execute('''SELECT message, username, date FROM messages''').fetchall()
        cur.close()
    return render_template('index.html', messages = messages)
