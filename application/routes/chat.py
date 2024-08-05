from flask import Blueprint, request, url_for, render_template, redirect, make_response
from application.utils.query import get_chat_rooms, create_chat_room, get_chat_by_id, get_connected_users

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/room", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        room_id = int(request.args.get('room_id'))
        chatlog = get_chat_by_id(room_id)
        return render_template("chat.html", chatlog=chatlog)

    if request.method == "POST":
        match request.form["chatlog_buttons"]:
            case "leave": return redirect(url_for("chat.chat_list"))
            

@chat_bp.route("/list", methods=["GET", "POST"])
def chat_list():
    if request.method == "GET":
        chatlogs = get_chat_rooms()
        connected_users = get_connected_users()
        for chat in chatlogs:
            if chat['id'] in connected_users:
                chat['connected_users'] = connected_users[chat['id']]
            else:
                chat['connected_users'] = 0
        return render_template("chat_list.html", chatlogs=chatlogs)

    if request.method == "POST":
        match request.form['chat_button']:
            case 'new_submit': 
                name = request.form['chatname']
                create_chat_room(name)
                return redirect(url_for('chat.chat_list'))
            
            case 'join_submit':
                room_id = request.form['room_id']
                chatlog = get_chat_by_id(room_id)
                print(chatlog)
                return redirect(url_for("chat.chat", room_id=chatlog['id']))

            case 'home':
                return redirect(url_for("home_page"))