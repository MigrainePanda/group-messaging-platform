import json, ast
import hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256

from dotenv import load_dotenv
import os
from datetime import datetime, timezone

from flask import Blueprint, request, url_for, render_template, redirect, make_response

from application import engine
from application.models import User

from sqlalchemy.orm import Session
from sqlalchemy import select

load_dotenv()

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        with Session(engine) as session, session.begin():
            users = session.execute(select(User).order_by(User.id)).scalars()
            users = [user.__dict__ for user in users]
        return render_template("users.html", users=users)
    
    if request.method == "POST":
        match request.form['user_button']:
            case 'create_user': return redirect(url_for("users.create_user"))
            case 'login_user': return redirect(url_for('users.user_login'))
        

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
        if 'jwt' in request.cookies:
            # should check valid secret key first before running below as malicious data could be uploaded
            data = "{" + urlsafe_b64decode(request.cookies['jwt'].split(".")[1] + "==").decode("utf-8") + "}"
            data = json.loads(data)
            print(data)
            
            return redirect(url_for('home_page'))
        
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
        
        encoding = 'utf-8'
        secret_key = os.getenv('SECRET_KEY')
        iat_time = datetime.now(timezone.utc).timestamp()
        exp_time = iat_time + 6048000
        
        header = '{"alg":"HS256","typ":"JWT"}'
        payload = f'"id":"{user["id"]}","iat":{iat_time},"exp":{exp_time}'
        
        encoded_header = urlsafe_b64encode(bytes(header, encoding)).decode().replace("=", "")
        encoded_payload = urlsafe_b64encode(bytes(payload, encoding)).decode().replace("=", "")

        signature = hmac.new(bytes(secret_key, encoding), bytes(encoded_header + '.' + encoded_payload, encoding), digestmod=sha256).digest()
        encoded_signature = urlsafe_b64encode(signature).decode().replace("=", "")
        
        jwt = encoded_header + '.' + encoded_payload + '.' + encoded_signature
        
        response = make_response(render_template("index.html", cookies=request.cookies))
        response.set_cookie("jwt", jwt)

        return response
            
    
    
    
    