from flask import Flask
import os
import pymysql
import time
from pymysql import err as pymysql_err


def get_db_connection():
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', 3306))
    user = os.environ.get('DB_USER', 'root')
    password = os.environ.get('DB_PASSWORD', '')
    db = os.environ.get('DB_NAME', 'docker_messages')
    return pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8mb4', autocommit=True)


def create_database():
    '''
    create messages table if it doesn't exist
    '''
    retries = 10
    delay = 3
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            conn = get_db_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        message TEXT,
                        username VARCHAR(255),
                        date VARCHAR(255)
                    )''')
                return None
            finally:
                conn.close()
        except pymysql_err.OperationalError as e:
            last_exc = e
            if attempt == retries:
                raise
            time.sleep(delay)


def create_app():
    app = Flask(__name__)
    from .views import router
    app.register_blueprint(router)
    from .api import Api
    app.register_blueprint(Api)
    create_database()
    return app