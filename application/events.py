from flask import request
from .routes.jwt import is_valid_jwt
from flask_socketio import SocketIO, ConnectionRefusedError

socketio = SocketIO()

@socketio.on("connect")
def handle_connect(auth):
    print(auth)
    if "jwt" in auth and is_valid_jwt(auth["jwt"]):
        print("client connected")
    else:
        raise ConnectionRefusedError("unauthorized")
    
@socketio.on("user_join")
def handle_user_join(username):
    print(f"{username} connected to the chat")
    
@socketio.on("message")
def handle_message(data):
    print("message received " + data)
