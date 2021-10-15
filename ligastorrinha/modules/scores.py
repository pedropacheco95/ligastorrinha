import functools
import random

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import Player , Edition , League , Association_PlayerEdition

bp = Blueprint('scores', __name__, url_prefix='/scores')

@bp.route('/', methods=('GET', 'POST'))
@bp.route('/<view>/<league_name>', methods=('GET', 'POST'))
@bp.route('/<view>/<league_name>/<edition_name>', methods=('GET', 'POST'))
def index(view,league_name,edition_name):
    if view == 'table':
        return redirect(url_for('scores.table',league_name = league_name, edition_name = edition_name))
    elif view == 'games':
        return redirect(url_for('scores.games',league_name = league_name, edition_name = edition_name))
    elif view == 'scorers':
        return redirect(url_for('scores.scorers',league_name = league_name, edition_name = edition_name))
    elif view == 'create_teams':
        return redirect(url_for('scores.create_teams',league_name = league_name, edition_name = edition_name))
    return render_template('index.html')

@bp.route('/table/<league_name>', methods=('GET', 'POST'))
@bp.route('/table/<league_name>/<edition_name>', methods=('GET', 'POST'))
@bp.route('/table/<league_name>/<edition_name>/<recalculate>', methods=('GET', 'POST'))
def table(league_name,edition_name=None,recalculate=None):

    league = League.query.filter_by(name=league_name).first()
    if not league:
        return redirect(url_for('errors.no_model_with_name', model = 'league',name = 'league_name'))
    if not edition_name:
        return redirect(url_for('scores.table', league_name = league_name, edition_name = league.editions[-1].name))


    editions , edition , players = checkLeague(league,edition_name)

    if recalculate == 'recalculate':
        recalculate_bool = True
    else:
        recalculate_bool = False

    table_values = {}
    for player in players:
        association = Association_PlayerEdition.query.filter_by(player_id= player.id , edition_id = edition.id).first()
        table_values[player.name] = association.get_player_results(recalculate_bool)

    table_values = {key: value for key, value in sorted(table_values.items(), key=lambda item: item[1]['points'], reverse=True)}

    for index in range(len(table_values)):
        key = list(table_values.keys())[index]
        association.place = index + 1
        table_values[key]['place'] = index + 1

    return render_template('scores/table.html', view='table',table_values=table_values,editions=editions,league = league, edition = edition)

@bp.route('/games/<league_name>', methods=('GET', 'POST'))
@bp.route('/games/<league_name>/<edition_name>', methods=('GET', 'POST'))
def games(league_name,edition_name=None):

    league = League.query.filter_by(name=league_name).first()
    if not league:
        return redirect(url_for('errors.no_model_with_name', model = 'league',name = 'league_name'))
    if not edition_name:
        return redirect(url_for('scores.games',league_name = league_name, edition_name = league.editions[-1].name))

    editions , edition , players = checkLeague(league,edition_name)
    games = edition.games
    return render_template('scores/games.html', view='games',games=games ,editions=editions,league = league, edition = edition)

@bp.route('/scorers/<league_name>', methods=('GET', 'POST'))
@bp.route('/scorers/<league_name>/<edition_name>', methods=('GET', 'POST'))
def scorers(league_name,edition_name=None):

    league = League.query.filter_by(name=league_name).first()
    if not league:
        return redirect(url_for('errors.no_model_with_name', model = 'league',name = 'league_name'))
    if not edition_name:
        return redirect(url_for('scores.scorers',league_name = league_name, edition_name = league.editions[-1].name))
    
    editions , edition , players = checkLeague(league,edition_name)

    table_values = {}
    for player in players:
        association = Association_PlayerEdition.query.filter_by(player_id= player.id , edition_id = edition.id).first()
        table_values[player.name] = association.get_player_results()

    table_values = {key: value for key, value in sorted(table_values.items(), key=lambda item: item[1]['goals'], reverse=True)}

    for index in range(len(table_values)):
        key = list(table_values.keys())[index]
        table_values[key]['place'] = index + 1

    return render_template('scores/scorers.html', table_values = table_values , view='scorers',editions=editions,league = league, edition = edition)

@bp.route('/create_teams/<league_name>', methods=('GET', 'POST'))
@bp.route('/create_teams/<league_name>/<edition_name>', methods=('GET', 'POST'))
def create_teams(league_name,edition_name=None):

    league = League.query.filter_by(name=league_name).first()
    if not league:
        return redirect(url_for('errors.no_model_with_name', model = 'league',name = 'league_name'))
    if not edition_name:
        return redirect(url_for('scores.create_teams',league_name = league_name, edition_name = league.editions[-1].name))
    
    editions , edition , players = checkLeague(league,edition_name)

    if request.method == 'POST':
        table_values = {}
        for player in players:
            association = Association_PlayerEdition.query.filter_by(player_id= player.id , edition_id = edition.id).first()
            table_values[player.name] = association.get_player_results()

        table_values = {key: value for key, value in sorted(table_values.items(), key=lambda item: item[1]['points'], reverse=True)}

        for index in range(len(table_values)):
            key = list(table_values.keys())[index]
            association.place = index + 1
            table_values[key]['place'] = index + 1

        players = list(table_values.keys())

        if league.name == 'MasterLeague':
            random.shuffle(players)

        edition.number_of_teams_made += 1
        edition.save()

        return render_template('scores/create_teams.html', view='create_teams', show = True, players=players , editions=editions,league = league, edition = edition)

    return render_template('scores/create_teams.html', view='create_teams', show = False , editions=editions,league = league, edition = edition)

def checkLeague(league,edition_name):

    editions = league.editions
    edition = Edition.query.filter_by(name=edition_name).first()
    players = edition.players
    
    return editions , edition , players