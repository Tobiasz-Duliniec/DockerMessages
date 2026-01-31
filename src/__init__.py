from flask import Flask
import os
import sqlite3


def create_database():
    '''
    create database if it doesn't exist
    '''
    if(os.path.isfile('instance/messages.db')):
        return None
    if(not os.path.isdir('instance')):
        os.mkdir('instance')
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

def create_app():
    app = Flask(__name__)
    from .views import router
    app.register_blueprint(router)
    from .api import Api
    app.register_blueprint(Api)
    create_database()
    return app
