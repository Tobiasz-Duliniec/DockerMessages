from flask import Blueprint, render_template, send_from_directory
import pymysql
import os


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


def get_db_connection():
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', 3306))
    user = os.environ.get('DB_USER', 'root')
    password = os.environ.get('DB_PASSWORD', '')
    db = os.environ.get('DB_NAME', 'docker_messages')
    return pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8mb4')


@router.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT message, username, date FROM messages')
        messages = cur.fetchall()
        cur.close()
        raise Exception
    except Exception:
        return render_template('index.html')
    finally:
        conn.close()
    return render_template('index.html', messages=messages)
