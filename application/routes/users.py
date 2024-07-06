import json
import hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256

from dotenv import load_dotenv
from datetime import datetime, timezone

from flask import Blueprint, request, url_for, render_template, redirect, make_response

from application import engine
from application.models import User
from application.jwt import is_valid_jwt, generate_jwt

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        with Session(engine) as session, session.begin():
            users = session.execute(select(User).order_by(User.id)).scalars()
            users = [user.__dict__ for user in users]

        logged_in = False
        if "jwt" in request.cookies:
            if is_valid_jwt(request.cookies["jwt"]):
                logged_in = True
        return render_template("users.html", users=users, logged_in=logged_in)
    
    if request.method == "POST":
        match request.form['user_button']:
            case 'create_user': return redirect(url_for("users.create_user"))
            case 'login_user': return redirect(url_for('users.user_login'))
            case 'logout_user': return redirect(url_for('users.user_logout'), code=307)

        
@users_bp.route("/<int:user_id>", methods=["GET", "POST"])
def user_page(user_id):
    with Session(engine) as session, session.begin():
        user = session.execute(select(User).filter_by(id=user_id)).scalar()
        user = user.__dict__
    return f'<h1>{user["username"]}</h1>'


@users_bp.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    
    if request.method == "POST":
        with Session(engine) as session, session.begin():
            user = User(
                username = request.form["username"],
                email = request.form["email"],
                password = request.form["password"],
                messages = []
            )
            
            session.add(user)
            session.commit()
            
        return redirect(url_for("users.users"))
    
    
@users_bp.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        if 'jwt' in request.cookies and is_valid_jwt(request.cookies['jwt']):
            data = urlsafe_b64decode(request.cookies['jwt'].split(".")[1] + "==").decode("utf-8")
            data = json.loads(data)
            return redirect(url_for("users.user_page", user_id=data["id"]))
        
        email = request.args.get("email")
        error = request.args.get("error")
        return render_template("login.html", email=email, error=error)
    
    if request.method == "POST":  
        email = request.form["email"]
        password = request.form["password"] 
        with Session(engine) as session, session.begin():
            user = session.execute(select(User).filter_by(email=email)).scalar()
            if not user: return redirect(url_for("users.user_login", error=1))
            if user.password != password: return redirect(url_for("users.user_login", error=2, email=email))
            user = user.__dict__

        jwt = generate_jwt(user)
        response = make_response(redirect(url_for("users.user_page", user_id=user["id"])))
        response.set_cookie("jwt", jwt)

        return response
            
@users_bp.route("/logout", methods=["POST"])
def user_logout():
    if request.method == "POST":
        response = make_response(redirect(url_for("home_page")))
        if 'jwt' in request.cookies:
            response.set_cookie("jwt", "")
        
        return response