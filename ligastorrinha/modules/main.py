from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import User , Player , Edition , League

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('main/index.html')

@bp.route('/leagues', methods=('GET', 'POST'))
def leagues():
    leagues = League.query.all()
    return render_template('main/leagues.html',leagues=leagues)

@bp.route('/players', methods=('GET', 'POST'))
def players():
    players = Player.query.all()
    players.sort(key=lambda x: len(x.games_won()), reverse=True)
    return render_template('main/players.html',players=players)
