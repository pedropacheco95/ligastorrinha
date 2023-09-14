import functools
import random
import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import Player , Edition , Game , Association_PlayerEdition

bp = Blueprint('edit', __name__, url_prefix='/edit')

@bp.route('edition/replace_player/<id>', methods=('GET', 'POST'))
def edition_replace_player(id):
    edition = Edition.query.filter_by(id=id).first()
    if request.method == 'POST':
        player_1_id = int(request.form['player_1']) if request.form['player_1'] else None
        player_2_id = int(request.form['player_2']) if request.form['player_2'] else None
        if player_1_id and player_2_id:
            player_1 = Player.query.filter_by(id=player_1_id).first()
            player_2 = Player.query.filter_by(id=player_2_id).first()
            check = edition.replace_players(player_1,player_2)
        else:
            check = False
        if not check:
            players = Player.query.all()
            return render_template('edit/edition_replace_player.html',edition=edition,players=players,error = 'Nao foi possivel alterar os jogadores')
        return render_template('scores/table.html', view='table',league = edition.league, edition = edition)
    players = Player.query.all()
    return render_template('edit/edition_replace_player.html',edition=edition,players=players)


@bp.route('edition/close', methods=('GET', 'POST'))
def close_editions():
    edition_ended = Edition.query.filter(Edition.final_game < datetime.date.today()).all()
    for edition in edition_ended:
        edition.has_ended = True
        edition.save()

    return 'Done'