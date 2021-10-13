import functools
import datetime
import os

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for , current_app
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import User , Player , League

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            user = User(username=username, email=email , password= password)
            user.create()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            leagues = League.query.all()
            session['leagues'] = leagues
            session['user'] = user
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/edit', methods=('GET', 'POST'))
def edit():
    if request.method == 'POST':
        error = None
        username = request.form.get('username')
        if User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."
        email = request.form.get('email')
        if User.query.filter_by(email=email).first() is not None:
            error = f"User {email} is already registered."
        player_id = request.form.get('player')
        player = Player.query.filter_by(id = player_id).first()
        full_name = request.form.get('name')
        birth_date = None
        if request.form.get('birth_date'):
            birth_date = datetime.datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d')
        file = request.files['picture']
        if file.filename != '':
            if player_id:
                filename = os.path.join('images','Players',str(player_id) + '.jpg')
                path = current_app.root_path + url_for('static', filename = filename)
                file_exists = os.path.exists(path)
                if not file_exists:
                    img_file = open(path,'wb')
                    img_file.close()
                file.save(path)


        if error is None:
            if username:
                session['user'].username = username
            if email:
                session['user'].email = email
            if player:
                session['user'].player_id = player.id
                session['user'].save()
                if full_name:
                    player.full_name = full_name
                if birth_date:
                    player.birthday = birth_date
                player.save()
            return redirect(url_for('main.index'))
        
        flash(error)
        available_players = Player.query.filter_by(user = None).all()
        return render_template('auth/edit.html',available_players=available_players)

    available_players = Player.query.filter_by(user = None).all()

    return render_template('auth/edit.html',available_players=available_players)

@bp.route('/logout')
def logout():
    session.clear()
    leagues = League.query.all()
    session['leagues'] = leagues
    return redirect(url_for('main.index'))

def allowed_picture(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg','png','jpeg'}