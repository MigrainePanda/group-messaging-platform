from flask import Blueprint, request, url_for, render_template, redirect
from application.utils.query import get_chat_rooms, create_chat_room, get_chat_by_id

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
            
        