from flask import Flask, render_template, request, url_for, redirect, session 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User
import sqlite3

app = Flask(__name__)
app.secret_key = 'key_session_user'
app.config['SqlAlchemy_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.quesry.filter_by(sername = username).first():
            return render_template('Register.html', errore='Questo utente esiste già')
        new_user = User(username = username, password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('Register.html', errore = None)


if __name__ == '__main__': #debug
    app.run(debug=True)