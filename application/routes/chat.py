from flask import Blueprint, request, url_for, render_template, redirect

from application import db
from application.models import User

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/", methods=["GET"])
def chat():
    
    
    return render_template("chat.html")