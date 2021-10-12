import functools
import os
import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from ligastorrinha.sql_db import db
from ligastorrinha.models import User , Game , League , Edition , Player , Association_PlayerGame , Association_PlayerEdition

bp = Blueprint('uploads', __name__, url_prefix='/uploads')

@bp.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        model = request.form['models']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = os.path.join('ligastorrinha/uploads', secure_filename(file.filename))

            file.save(filename)
            
            d = dict()
            f = open(filename)
            for line in f:
                line = line.strip('\n')
                columns = line.split(",")
                if model == 'players':
                    d[columns[0]] = {}
                    d[columns[0]]['name'] = columns[1]
                    d[columns[0]]['full_name'] = columns[3]

            d.pop('Id_jogador')

            if model == 'players':
                for key in d:
                    row = d[key]
                    check_player = Player.query.filter_by(name=row['name']).first()
                    if check_player is None:
                        if row['full_name']:
                            player = Player(name=row['name'], full_name=row['full_name'])
                        else:
                            player = Player(name=row['name'])
                        player.create()
            
            return redirect(url_for('main.index'))
    
    models = ['users','editions','game','leagues','teams','players']

    return render_template('uploads/upload.html',models=models)

@bp.route('/upload_csv_to_db', methods=['GET', 'POST'])
def upload_csv_to_db():

    leagues = dict()
    f = open(os.path.join('ligastorrinha/uploads', 'Ligas.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id_Liga':
            liga = League(name=columns[1])
            liga.create()
            leagues[columns[0]] = liga
    f.close()

    editions = dict()
    f = open(os.path.join('ligastorrinha/uploads', 'Edições.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id_Edição':
            date = datetime.datetime.strptime(columns[4], '%d/%m/%Y')
            edicao = Edition(name=columns[1],league_id=leagues[columns[2]].id,time = columns[3],final_game=date)
            editions[columns[0]] = edicao
            edicao.create()
    f.close()

    players = dict()
    f = open(os.path.join('ligastorrinha/uploads', 'Jogadores.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id_jogador':
            if columns[3]:
                player = Player(name=columns[1], full_name=columns[3])
            else:
                player = Player(name=columns[1])
            player.create()
            players[columns[0]] = player
    f.close()

    teams = dict()
    f = open(os.path.join('ligastorrinha/uploads', 'Equipas.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id_equipa':
            if columns[1] == '':
                columns[1] = 0
            teams[columns[0]] = {'golos':columns[1]}
    f.close()

    games = dict()
    f = open(os.path.join('ligastorrinha/uploads', 'Jogos.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id_jogo':
            edition = editions[columns[4]]
            date = datetime.datetime.strptime(columns[5], '%d/%m/%Y')
            game = Game(goals_team1=int(teams[columns[1]]['golos']),goals_team2=int(teams[columns[2]]['golos']),winner=int(columns[3]),edition_id=edition.id,matchweek = len(edition.games)+1,date=date)
            games[columns[0]] = game
            game.create()
    f.close()

    f = open(os.path.join('ligastorrinha/uploads', 'Jogadores_por_equipa.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id_equipa':
            player = players[columns[1]]
            game = games[columns[2]]
            team = 'Branquelas' if int(columns[0])%2 == 1 else 'Maregões'
            association = Association_PlayerGame(player_id= player.id, game_id = game.id,team = team,goals=int(columns[3]))
            association.create()
    f.close()

    f = open(os.path.join('ligastorrinha/uploads', 'JogadoresPorEdicao.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'Id':
            player = players[columns[1]]
            edition = editions[columns[2]]
            association = Association_PlayerEdition(player_id = player.id, edition_id = edition.id)
            association.create()
    f.close()

    return redirect(url_for('main.index'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}
