from flask import Blueprint, jsonify, request
import datetime
import pymysql
import os


Api = Blueprint('api', __name__, url_prefix='/api')

max_message_length = 255


def get_db_connection():
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', 3306))
    user = os.environ.get('DB_USER', 'root')
    password = os.environ.get('DB_PASSWORD', '')
    db = os.environ.get('DB_NAME', 'docker_messages')
    return pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8mb4', autocommit=True)


@Api.route('/add', methods=['POST'])
def add_message():
    '''
    add message to the database
    '''
    username = request.json.get("username", None)
    message = request.json.get("message", None)
    if ((username in ('', None)) or (message in ('', None))):
        return jsonify({'response code': 400, 'status': 'You must provide both the username and the message'}), 400
    if ((message_length := len(message)) > max_message_length):
        return jsonify({'response code': 400, 'status': f'Max message length is {max_message_length}, yours was {message_length}'}), 400
    status = None
    date = datetime.datetime.now(datetime.timezone.utc).strftime('%d/%m/%Y, %H:%M:%S (%Z)')
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO messages(message, username, date) VALUES (%s, %s, %s)', (message, username, date))
        status = True
    except Exception:
        status = False
    finally:
        conn.close()
    if(status):
        return jsonify({'response code': 200, 'message': message, 'username': username, 'date': date})
    else:
        return jsonify({'response code': 500, 'status': 'Something went wrong when saving your message.'}), 500