from flask import request

from application.utils.jwt import is_valid_jwt, extract_data
from application.utils.query import get_user_by_id
from application import socketio


@socketio.on('connect')
def handle_connect():
    if is_valid_jwt(request.headers.get('token')):
        print("client connected")
    else:
        raise ConnectionRefusedError('unauthorized')
    
@socketio.on('message')
def handle_message(data):
    token = request.headers.get('token')
    if is_valid_jwt(token):
        user_id = extract_data(token)['id']
        user = get_user_by_id(user_id)
        
        socketio.emit('recieve_message', {'user': user['username'], 'message': data})
