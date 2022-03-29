import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import Edition , League

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/choose_new_edition_scores/<view>', methods=('GET', 'POST'))
def choose_new_edition_scores(view):
    if request.method == 'POST':
        edition_name = request.form['edicao']
        edition = Edition.query.filter_by(name=edition_name).first()
        league = League.query.filter_by(id=edition.league_id).first()
        return redirect(url_for('scores.index',view = view ,league_id = league.id, edition_id = edition.id))

    return redirect(url_for('main.index'))

@bp.route('/choose_new_edition_players/<view>/<player_name>', methods=('GET', 'POST'))
def choose_new_edition_players(view,player_name):
    if request.method == 'POST':
        edition_name = request.form['edicao']
        edition = Edition.query.filter_by(name=edition_name).first()
        return redirect(url_for('players.index',view = view ,player_name = player_name, edition_name = edition.name))

    return redirect(url_for('main.index'))