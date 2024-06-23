from flask import Blueprint, request, url_for, render_template, redirect

from application import db, engine
from application.models import User

from sqlalchemy.orm import Session
from sqlalchemy import select

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        with Session(engine) as session, session.begin():
            users = session.execute(select(User).order_by(User.id)).scalars()
            users = [user.__dict__ for user in users]
        return render_template("users.html", users=users)
    
    if request.method == "POST":
        return redirect(url_for("users.create_user"))

@users_bp.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    
    if request.method == "POST":
        with Session(engine) as session, session.begin():
            user = User(
                username = request.form["username"],
                email = request.form["email"],
                messages = []
            )

            session.add(user)
            session.commit()
            
        return redirect(url_for("users.users"))
    
    
    