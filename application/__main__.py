from flask import request, url_for, render_template, redirect
from application import create_app

app = create_app()

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template("index.html")
    
    if request.method == 'POST':
        match request.form['home_button']:
            case 'login': return redirect(url_for('users.user_login'))
            case 'users': return redirect(url_for('users.users'))
            case 'chat': return redirect(url_for('chat.chat'))

if __name__ == "__main__":
    app.run(debug=True)