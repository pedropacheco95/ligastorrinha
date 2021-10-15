import functools
import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.tools import admin_required

from ligastorrinha.models import Player , Edition , League , Association_PlayerEdition , Game , Association_PlayerGame

bp = Blueprint('delete', __name__, url_prefix='/delete')

@admin_required
@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('delete/index.html')

@admin_required
@bp.route('/game', methods=('GET', 'POST'))
def game():

    if request.method == 'POST':
        game =  Game.query.filter_by(id = request.form["game_id"]).first()
        game.delete()
        return redirect(url_for('main.index'))

    games = Game.query.all()

    return render_template('delete/game.html', games = games)
