from flask import request
from application.jwt import is_valid_jwt
from flask_socketio import SocketIO, ConnectionRefusedError

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    if is_valid_jwt(request.headers.get('user-auth')):
        print("client connected")
    else:
        raise ConnectionRefusedError('unauthorized')
    
@socketio.on('message')
def handle_message(data):
    print("message received " + data)
    socketio.emit('recieve_message', {'user': "meow", 'message': "meow"})
    
@socketio.on('receive_message')
def handle_receieve_message(data):
    print(data)