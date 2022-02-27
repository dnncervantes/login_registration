from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/successful')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valid_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.new_user(data)
    session['id'] = user_id
    return redirect('/welcome')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
        'password' : request.form['password']
    }
    if not User.valid_login(data):
        return redirect('/')
    user_id = User.get_email(data)
    session['id'] = user_id.id
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': session["id"]
        }
    user = User.get_user(data)
    return render_template('welcome.html', user=user)

@app.route('/signout')
def signout():
    session.clear()
    flash('You have signed off', 'signout')
    return redirect('/')




