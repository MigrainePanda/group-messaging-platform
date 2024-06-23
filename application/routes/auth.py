
from flask import Blueprint, request, url_for, render_template, redirect

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        return redirect(url_for('home_page'))

