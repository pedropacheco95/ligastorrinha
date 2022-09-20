import functools
import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.tools import admin_required

from ligastorrinha.models import Player , Edition , League , Association_PlayerEdition , Game , Association_PlayerGame

bp = Blueprint('create', __name__, url_prefix='/create')

@admin_required
@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('create/index.html')

@bp.route('/player', methods=('GET', 'POST'))
def player():
    if request.method == 'POST':
        name = request.form.get('name')
        full_name = request.form.get('full_name')
        if request.form.get('birth_date'):
            birth_date = datetime.datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d')
        else:
            birth_date = False
        if not name:
            redirect(url_for('errors.missing_information' , model='player',field ='name'))
        player = Player(name = name)
        if full_name:
            player.full_name = full_name
        if birth_date:
            player.birth_date = birth_date
        player.create()
        return redirect(url_for('main.index'))

    return render_template('create/player.html')

@bp.route('/edition', methods=('GET', 'POST'))
def edition():
    leagues = League.query.all()
    players = Player.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        league = League.query.filter_by(name = request.form.get('league')).first()
        time = request.form.get('time')
        number_of_players = int(request.form.get('number_of_players')) if request.form.get('number_of_players') else 0
        final_game = datetime.datetime.strptime(request.form.get('final_game'), '%Y-%m-%d')
        if not league or not name:
            redirect(url_for('errors.missing_information' , model='edition',field ='name or league'))
        

        edition = Edition(name=name,league_id=league.id,time = time,final_game=final_game)
        edition.create()
        players = []
        for i in range(number_of_players):
            field = 'player_' + str(i)
            player_name = request.form.get(field)
            player = Player.query.filter_by(name = player_name).first()
            if player:
                association = Association_PlayerEdition(player_id = player.id, edition_id = edition.id)
                association.create()
        return redirect(url_for('main.index'))

    return render_template('create/edition.html', leagues = leagues, players = players)

@bp.route('/choose_edition/<view>', methods=('GET', 'POST'))
def choose_edition(view):
    editions = Edition.query.all()
    if request.method == 'POST':
        edition_name = request.form.get('edition_name')
        url = 'create.' + view
        return redirect(url_for(url,edition_name=edition_name))

    return render_template('create/choose_edition.html', editions = editions)

@admin_required
@bp.route('/game', methods=('GET', 'POST'))
@bp.route('/game/<edition_name>', methods=('GET', 'POST'))
def game(edition_name=None):
    edition = Edition.query.filter_by(name=edition_name).first()
    if not edition:
        return redirect(url_for('create.choose_edition' , view='game'))
    if request.method == 'POST':
        error = None
        goals_team1 = [int(goals) for goals in request.form.getlist('goals_team1') if goals]
        goals_team2 = [int(goals) for goals in request.form.getlist('goals_team2') if goals]
        if not goals_team1 or not goals_team2:
            error = 'Uma das equipas não tem um numero de golos definido'

        player_team1_ids = [int(id) for id in request.form.getlist('player_team_1') if id and id != 'player_missing']
        players_team1 = Player.query.filter(Player.id.in_(tuple(player_team1_ids))).all()

        player_team2_ids = [int(id) for id in request.form.getlist('player_team_2') if id and id != 'player_missing']
        players_team2 = Player.query.filter(Player.id.in_(tuple(player_team2_ids))).all()

        if list(set(players_team1).intersection(players_team2)):
            error = 'Houve um jogador posto nas duas equipas'
        if not error:
            goals_team1 = goals_team1[0]
            goals_team2 = goals_team2[0]
            winner = 1 if goals_team1 > goals_team2 else -1 if goals_team1 < goals_team2 else 0
            date = datetime.datetime.strptime(request.form.get('game_date'), '%Y-%m-%d')
            matchweek = max([game.matchweek for game in edition.games]) + 1 if [game.matchweek for game in edition.games] else 1
            game = Game(goals_team1=goals_team1,goals_team2=goals_team2,winner=winner,edition_id=edition.id,matchweek = matchweek,date=date)
            game.create()

            for player in players_team1:
                goals_string = request.form.get('goals_{id}'.format(id=player.id))
                goals = int(goals_string) if goals_string else 0
                team = 'Branquelas'
                association = Association_PlayerGame(player_id= player.id, game_id = game.id,team = team,goals=goals)
                association.create()

            for player in players_team2:
                goals_string = request.form.get('goals_{id}'.format(id=player.id))
                goals = int(goals_string) if goals_string else 0
                team = 'Maregões'
                association = Association_PlayerGame(player_id= player.id, game_id = game.id,team = team,goals=goals)
                association.create()

            return redirect(url_for('scores.table',league_id = edition.league.id,edition_id=edition.id,recalculate=True))
        flash(error)

    default_day = datetime.date.today()
    if edition.league.name == 'MasterLeague':
        offset = (default_day.weekday() - 3) % 7
        default_day -= datetime.timedelta(days=offset)
    elif edition.league.name == 'TuesdayLeague':
        offset = (default_day.weekday() - 1) % 7
        default_day -= datetime.timedelta(days=offset)

    player_ids = edition.players_ids_last_team()
    players = [Player.query.filter_by(id=player_id).first() for player_id in player_ids] 

    edition_players = [rel.player for rel in edition.players_relations]

    return render_template('create/game.html', edition=edition , default_day=default_day,players=players,edition_players=edition_players)
