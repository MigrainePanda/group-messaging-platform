from flask import request, url_for, render_template, redirect
from application import create_app
from application.utils.events import socketio
from application.utils.jwt import is_valid_jwt, extract_data

app = create_app()

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == "GET":
        logged_in = False
        if "jwt" in request.cookies and is_valid_jwt(request.cookies["jwt"]):
            logged_in = True
        return render_template("index.html", logged_in=logged_in)
    
    if request.method == 'POST':
        match request.form['home_button']:
            case 'create_user': return redirect(url_for('users.create_user'))
            case 'login_user': return redirect(url_for('users.user_login'))
            case 'chat': return redirect(url_for('chat.chat_list'))
            case 'users': return redirect(url_for('users.users'))
            case 'profile': 
                jwt_data = extract_data(request.cookies["jwt"])
                return redirect(url_for('users.user_page', user_id=jwt_data["id"]))
            case 'logout_user': return redirect(url_for('users.user_logout'), code=307)

if __name__ == "__main__":
    # socketio.run(app, ssl_context=('cert.pem', 'key.pem'))
    socketio.run(app)