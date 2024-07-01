from flask import Blueprint, request, url_for, render_template, redirect

from application import db, engine
from application.models import User, ChatLog

from sqlalchemy.orm import Session
from sqlalchemy import select

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/room/<int:room_id>", methods=["POST"])
def chat(room_id):
    return render_template("chat.html", room_id=room_id)

@chat_bp.route("/list", methods=["GET", "POST"])
def chat_list():
    if request.method == "GET":
        with Session(engine) as session, session.begin():
            chatlogs = session.execute(select(ChatLog).order_by(ChatLog.id)).scalars()
            chatlogs = [chatlog.__dict__ for chatlog in chatlogs]
        # print(chatlogs)
        return render_template("chat_list.html", chatlogs=chatlogs)

    if request.method == "POST":
        match request.form['chat_button']:
            case 'new_submit': 
                with Session(engine) as session, session.begin():
                    chatlog = ChatLog(
                        name = request.form['chatname'],
                        messages = []
                    )
                    session.add(chatlog)
                    session.commit()
                return redirect(url_for('chat.chat_list'))
            
            case 'join_submit':
                with Session(engine) as session, session.begin():
                    chatlog = session.execute(select(ChatLog).filter_by(id=request.form['room_id'])).scalar()
                    chatlog = chatlog.__dict__
                # print(chatlog)
                return redirect(url_for("chat.chat", room_id=chatlog["id"]), code=307)
            
        