from flask import Blueprint, request, url_for, render_template, redirect, make_response

from application.utils.jwt import is_valid_jwt, generate_jwt, extract_data
from application.utils.query import get_users, get_user_by_id, add_user, check_login, get_msgs_by_user_id

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        logged_in = False
        users = get_users()
        if "jwt" in request.cookies and is_valid_jwt(request.cookies["jwt"]):
            logged_in = True
        return render_template("users.html", users=users, logged_in=logged_in)
    
    if request.method == "POST":
        match request.form['user_button']:
            case 'home': return redirect(url_for("home_page"))
            case 'create_user': return redirect(url_for("users.create_user"))
            case 'profile': 
                jwt_data = extract_data(request.cookies["jwt"])
                return redirect(url_for("users.user_page", user_id=jwt_data["id"]))
            case 'login_user': return redirect(url_for('users.user_login'))
            case 'logout_user': return redirect(url_for('users.user_logout'), code=307)

        
@users_bp.route("/<int:user_id>", methods=["GET", "POST"])
def user_page(user_id):
    if request.method == "GET":
        user = get_user_by_id(user_id)
        if user:
            messages = get_msgs_by_user_id(user['id'])
            return render_template("userpage.html", user=user, messages=messages)
    
    if request.method == "POST":
        match request.form['user_button']:
            case 'home': return redirect(url_for("home_page"))
            case 'chat': return redirect(url_for('chat.chat_list'))
                    

@users_bp.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("create_user.html")
    
    if request.method == "POST":
        resp = add_user(request.form)
        if (resp): 
            return redirect(url_for("users.user_login"))
        return render_template('create_user.html', error="Please try again.")
        
    
    
@users_bp.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        if 'jwt' in request.cookies and is_valid_jwt(request.cookies['jwt']):
            jwt_data = extract_data(request.cookies['jwt'])
            return redirect(url_for("users.user_page", user_id=jwt_data["id"]))
        
        email = request.args.get("email")
        error = request.args.get("error")
        return render_template("login.html", email=email, error=error)
    
    if request.method == "POST":  
        email = request.form["email"]
        password = request.form["password"]
        
        user = check_login(email, password)
        if 'error' not in user:
            jwt = generate_jwt(user)
            response = make_response(redirect(url_for("users.user_page", user_id=user["id"])))
            response.set_cookie("jwt", jwt)
            return response
        else:
            print(user)
            return redirect(url_for("users.user_login", **user))
            
@users_bp.route("/logout", methods=["POST"])
def user_logout():
    if request.method == "POST":
        response = make_response(redirect(url_for("home_page")))
        if 'jwt' in request.cookies:
            response.set_cookie("jwt", "")
        
        return response