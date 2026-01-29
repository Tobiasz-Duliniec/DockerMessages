from flask import Blueprint, jsonify, request
import datetime
import sqlite3

Api = Blueprint('api', __name__, url_prefix = '/api')

max_message_length = 255

@Api.route('/add', methods = ['POST'])
def add_message():
    username = request.json.get("username", None)
    message = request.json.get("message", None)
    if((username in ('', None)) or (message in ('', None))):
        return jsonify({'response code': 400, 'status': 'You must provide both the username and the message'}), 400
    if((message_length := len(message)) > max_message_length):
        return jsonify({'response code': 400, 'status': f'Max message length is {max_message_length}, yours was {message_length}'}), 400
    date = datetime.datetime.now(datetime.timezone.utc).strftime('%d/%m/%Y, %H:%M:%S (%Z)')
    with sqlite3.connect('instance/messages.db') as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO messages(message, username, date) VALUES (?, ?, ?)', (message, username, date))
        cur.close()
        conn.commit()
    return jsonify({'response code': 200, 'message': message, 'username': username, 'date': date})