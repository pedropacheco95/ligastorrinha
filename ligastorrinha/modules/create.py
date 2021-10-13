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

@admin_required
@bp.route('/game', methods=('GET', 'POST'))
@bp.route('/game/<edition_name>', methods=('GET', 'POST'))
def game(edition_name = None):

    edition = Edition.query.filter_by(name=edition_name).first()
    if not edition:
        return redirect(url_for('create.choose_edition' , view = 'game'))

    today = datetime.date.today()
    if edition.league == 'MasterLeague':
        offset = (today.weekday() - 3) % 7
        default_day = today - datetime.timedelta(days=offset)
    if edition.league == 'TuesdayLeague':
        offset = (today.weekday() - 1) % 7
        default_day = today - datetime.timedelta(days=offset)
    else:
        default_day = today

    if request.method == 'POST':
        branquelas = []
        maregoes = []
        for i in range(6):
            player_key = 'jogador_Branquelas_' + str(i)
            goals_key = 'goals_jogador_Branquelas_' + str(i)
            player_name = request.form.get(player_key)
            goals = request.form.get(goals_key)
            branquelas.append({'player':Player.query.filter_by(name = player_name).first(), 'goals':int(goals) if goals else 0})
            
            player_key = 'jogador_Maregões_' + str(i)
            goals_key = 'goals_jogador_Maregões_' + str(i)
            player_name = request.form.get(player_key)
            goals = request.form.get(goals_key)
            maregoes.append({'player':Player.query.filter_by(name = player_name).first(), 'goals':int(goals) if goals else 0})
        
        goals_team1 = request.form.get('goals_teams1')
        goals_team2 = request.form.get('goals_teams2')
        date = datetime.datetime.strptime(request.form.get('game_date'), '%Y-%m-%d')

        winner = 0
        if int(goals_team2) > int(goals_team1):
            winner = -1
        elif int(goals_team1) > int(goals_team2):
            winner = 1

        game = Game(goals_team1=int(goals_team1),goals_team2=int(goals_team2),winner=winner,edition_id=edition.id,matchweek = len(edition.games)+1,date=date)
        game.create()
        for dic in branquelas:
            player = dic['player']
            if player:
                team = 'Branquelas'
                association = Association_PlayerGame(player_id= player.id, game_id = game.id,team = team,goals=int(dic['goals']))
                association.create()
                Association_PlayerEdition.query.filter_by(player_id = player.id, edition_id = edition.id).first().get_player_results(True)
        for dic in maregoes:
            player = dic['player']
            if player:
                team = 'Maregões'
                association = Association_PlayerGame(player_id= player.id, game_id = game.id,team = team,goals=int(dic['goals']))
                association.create()
                Association_PlayerEdition.query.filter_by(player_id = player.id, edition_id = edition.id).first().get_player_results(True)
        return redirect(url_for('main.index'))
    return render_template('create/game.html', edition = edition , default_day=default_day)

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
        final_game = datetime.datetime.strptime(request.form.get('final_game'), '%Y-%m-%d')
        if not league or not name:
            redirect(url_for('errors.missing_information' , model='edition',field ='name or league'))
        

        edition = Edition(name=name,league_id=league.id,time = time,final_game=final_game)
        edition.create()
        players = []
        for i in range(12):
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
