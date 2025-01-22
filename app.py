from flask import Flask, render_template, request, url_for, redirect, session 
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from models import db, User
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'key_session_user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #check se l'utente esiste nel db
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")
#crea user e lo salva nel db
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', error=None)



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password): #se user esiste
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error="Credenziali non valide.") #errore se credenziali errate
    return render_template('login.html', error=None)

@app.route('/home')
@login_required #solo se user è autenticato
def home():
    user_logged = current_user.username
    return render_template('home.html', username=current_user.username, user_logged=user_logged)

@app.route('/logout')
@login_required
def logout():
    logout_user() #logout user
    return redirect(url_for('login'))


if __name__ == '__main__': #debug
    app.run(debug=True)