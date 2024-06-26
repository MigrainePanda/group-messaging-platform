import json
from base64 import urlsafe_b64encode
import hmac
from hashlib import sha256

from flask import Blueprint, request, url_for, render_template, redirect

from application import engine
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
        
        # check cookies for token
        
        email = request.args.get("email")
        return render_template("login.html", email=email)
    
    if request.method == "POST":        
        email = request.form["email"]
        password = request.form["password"] 
        with Session(engine) as session, session.begin():
            user = session.execute(select(User).filter_by(email=email)).scalar()
            if not user: return redirect(url_for("users.user_login", error=1))
            if user.password != password: return redirect(url_for("users.user_login", error=2, email=email))
            user = user.__dict__

        print(user)
        
        header = {
            "alg": "HS256",
            "typ": "JWT",
        }
        
        payload = {
            "sub": user["email"],
            "iat": 5516239024,
            # "admin": False,
            # "exp": new date
        }
        
        encoding = 'utf-8'
        encoded_header = urlsafe_b64encode(str(header).encode(encoding))
        encoded_payload = urlsafe_b64encode(str(payload).encode(encoding))
        
        signature_payload = f'{encoded_header}.{encoded_payload}'
        
        secret_key = b'your-256-bit-secret'
        
        signature = hmac.new(
            secret_key,
            msg = signature_payload.encode(encoding),
            digestmod=sha256
        ).digest()
        
        encoded_signature = urlsafe_b64encode(str(signature).encode(encoding))
        
        jwt_token = f'{signature_payload}.{encoded_signature}'
        
        print(jwt_token)
        
        resp = {
            "token": jwt_token
        }
        
        
        
        
        
        
        # encoded_header = urlsafe_b64encode(json.dumps(header).encode('utf-8'))
        # encoded_header_urlsafe_bytes = urlsafe_b64encode(json.dumps(header).encode('utf-8'))
        # encoded_header_urlsafe_str = str(encoded_header_urlsafe_bytes, "utf-8")


        # encoded_payload_urlsafe_bytes = urlsafe_b64encode(json.dumps(payload).encode('utf-8'))
        # encoded_payload_urlsafe_str = str(encoded_payload_urlsafe_bytes, "utf-8")
        
        
        # API_SECRET = 892374928347928347283473
        # message = f'{encoded_header_urlsafe_str} {encoded_payload_urlsafe_str} {API_SECRET}'
        # signature = hmac.new(
        #     str(API_SECRET),
        #     msg=message,
        #     digestmod=sha256
        # ).hexdigest().upper()
        
        
        
        # signature = HMACSHA256(  base64UrlEncode(header) + "." +   base64UrlEncode(payload),   secret)
        # sha256(input_.encode('utf-8')).hexdigest()
        # signature = sha256(encoded_header + encoded_payload)
        
        # print(encoded_header)
        # print(encoded_payload)
        # print(signature.hexdigest())
        
        # return redirect(url_for("set_cookie", ))

        return redirect(url_for("home_page"))
            
    
    
    
    # from hashlib import sha256
    # input_ = input('Enter something: ')
    # print(sha256(input_.encode('utf-8')).hexdigest())
    
    