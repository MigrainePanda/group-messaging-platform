from flask import request
from flask_socketio import join_room, leave_room

from application.utils.jwt import is_valid_jwt, extract_data
from application.utils.query import get_user_by_id, add_user_connected, rm_user_connected, save_msg, check_user_in_room
from application import socketio



@socketio.on('connect')
def handle_connect():
    jwt = request.headers.get('token')
    if is_valid_jwt(jwt):
        jwt_data = extract_data(jwt)
        user_id = jwt_data['id']
        if check_user_in_room(user_id):
            raise ConnectionRefusedError('user already has an established connection.')
        print("client connected")
    else:
        raise ConnectionRefusedError('unauthorized')

@socketio.on('join_room')
def handle_room_join(data: dict):
    jwt = request.headers.get('token')
    if is_valid_jwt(jwt):
        jwt_data = extract_data(jwt)
        user_id = jwt_data['id']
        user = get_user_by_id(user_id)
        room_id = data['room_id']
        add_user_connected(user_id, room_id)
        join_room(room_id)
        socketio.emit('recieve_message', {'user': "SERVER", 'message': f"{user['username']} has joined the chat."})
        print(f"joined room {room_id}")
    else:
        raise ConnectionRefusedError('unauthorized')
    
@socketio.on('message')
def handle_message(data: dict):    
    jwt = request.headers.get('token')
    if is_valid_jwt(jwt):
        user_id = extract_data(jwt)['id']
        user = get_user_by_id(user_id)
        room_id = user['current_chat_id']
        if room_id == data['room_id']:
            socketio.emit('recieve_message', {'user': user['username'], 'message': data["msg"]}, to=data["room_id"])
            save_msg({ 'user_id': user_id, 'chatlog_id': user['current_chat_id'], 'body': data['msg'] })
            
@socketio.on('disconnect')
def handle_disconnect():
    jwt = request.headers.get('token')
    room_id = int(request.headers.get('roomid'))
    if not is_valid_jwt(jwt):
        print("invalid jwt")
        return
    jwt_data = extract_data(jwt)
    user = get_user_by_id(jwt_data["id"])
    if user["current_chat_id"] == room_id:
        rm_user_connected(jwt_data['id'], room_id)
        leave_room(room_id)
        socketio.emit('recieve_message', {'user': "SERVER", 'message': f"{user['username']} has disconnected from the chat."}, to=room_id)