from flask import request
from flask_socketio import join_room, leave_room

from application.utils.jwt import is_valid_jwt, extract_data
from application.utils.query import get_user_by_id, add_user_connected, rm_user_connected, save_msg
from application import socketio


@socketio.on('connect')
def handle_connect():
    if is_valid_jwt(request.headers.get('token')):
        print("client connected")
    else:
        raise ConnectionRefusedError('unauthorized')

@socketio.on('join_room')
def handle_room_join(data):
    jwt = request.headers.get('token')
    if is_valid_jwt(jwt):
        jwt_data = extract_data(jwt)
        user = get_user_by_id(jwt_data["id"])
        room_id = data['room_id']
        add_user_connected(jwt_data['id'], room_id)
        join_room(room_id)
        socketio.emit('recieve_message', {'user': "SERVER", 'message': f"{user['username']} has joined the chat."})
        print(f"joined room {room_id}")
    else:
        raise ConnectionRefusedError('unauthorized')
    
@socketio.on('message')
def handle_message(data):
    token = request.headers.get('token')
    if is_valid_jwt(token):
        user_id = extract_data(token)['id']
        user = get_user_by_id(user_id)
        
        socketio.emit('recieve_message', {'user': user['username'], 'message': data["msg"]}, to=data["room_id"])
        save_msg({ 'user_id': user_id, 'chatlog_id': user['current_chat_id'], 'body': data['msg'] })
        
@socketio.on('disconnect')
def handle_disconnect():
    jwt = request.headers.get('token')
    if is_valid_jwt(jwt):
        jwt_data = extract_data(jwt)
        user = get_user_by_id(jwt_data["id"])
        room_id = user["current_chat_id"]
        rm_user_connected(jwt_data['id'], room_id)
        leave_room(room_id)
        socketio.emit('recieve_message', {'user': "SERVER", 'message': f"{user['username']} has disconnected from the chat."})
        print(f"left room {room_id}") 
        print("client disconnected")