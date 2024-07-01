from flask import request, url_for, render_template, redirect
from application import create_app
from .events import socketio

app = create_app()

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template("index.html")
    
    if request.method == 'POST':
        match request.form['home_button']:
            case 'login': return redirect(url_for('users.user_login'))
            case 'users': return redirect(url_for('users.users'))
            case 'chat': return redirect(url_for('chat.chat_list'))

if __name__ == "__main__":
    # socketio.run(app, ssl_context=('cert.pem', 'key.pem'))
    socketio.run(app)