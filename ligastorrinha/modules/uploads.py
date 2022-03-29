import functools
import os
import datetime
import csv

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from ligastorrinha import model 

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
    f = open(os.path.join('ligastorrinha/static/data/csv', 'leagues.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'id':
            liga = League(name=columns[1])
            if columns[2]:
                liga.picture = columns[2]
            liga.create()
            leagues[columns[0]] = liga
    f.close()

    editions = dict()
    f = open(os.path.join('ligastorrinha/static/data/csv', 'editions.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'id':
            date = datetime.datetime.strptime(columns[3], '%Y-%m-%d')
            has_ended = True if columns[4]=='True' else False
            number_of_teams_made = int(columns[5]) if columns[5] else 0
            edicao = Edition(name=columns[1],time = columns[2],final_game=date,has_ended=has_ended,number_of_teams_made=number_of_teams_made,league_id=leagues[columns[6]].id)
            editions[columns[0]] = edicao
            edicao.create()
    f.close()

    players = dict()
    f = open(os.path.join('ligastorrinha/static/data/csv', 'players.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'id':
            name = columns[1]
            full_name = columns[2] if columns[2] else None
            birthday = datetime.datetime.strptime(columns[3], '%Y-%m-%d') if columns[3] else None
            image_url = columns[4] if columns[4] else None
            player = Player(name=name,full_name=full_name,birthday=birthday)
            if image_url:
                player.image_url = image_url
            player.create()
            players[columns[0]] = player
    f.close()

    games = dict()
    f = open(os.path.join('ligastorrinha/static/data/csv', 'games.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'id':
            edition = editions[columns[6]]
            date = datetime.datetime.strptime(columns[3], '%Y-%m-%d')
            game = Game(goals_team1=int(columns[1]),goals_team2=int(columns[2]),winner=int(columns[4]),edition_id=edition.id,matchweek = int(columns[5]),date=date)
            games[columns[0]] = game
            game.create()
    f.close()

    f = open(os.path.join('ligastorrinha/static/data/csv', 'players_in_game.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'player_id':
            player = players[columns[0]]
            game = games[columns[1]]
            team = columns[2]
            association = Association_PlayerGame(player_id= player.id, game_id = game.id,team = team,goals=int(columns[3]))
            association.create()
    f.close()

    f = open(os.path.join('ligastorrinha/static/data/csv', 'players_in_edition.csv'))
    for line in f:
        line = line.strip('\n')
        columns = line.split(",")
        if columns[0] != 'player_id':
            place = int(columns[2]) if columns[3] else None
            last_place = int(columns[3]) if columns[3] else None
            points = float(columns[4]) if columns[4] else None
            appearances = int(columns[5]) if columns[5] else None
            goals = int(columns[6]) if columns[6] else None
            percentage_of_appearances = float(columns[7]) if columns[7] else None
            wins = int(columns[8]) if columns[8] else None
            draws = int(columns[9]) if columns[9] else None
            losts = int(columns[10]) if columns[10] else None
            goals_scored_by_team = int(columns[11]) if columns[11] else None
            goals_suffered_by_team = int(columns[12]) if columns[12] else None
            matchweek = int(columns[13]) if columns[13] else None

            player = players[columns[0]]
            edition = editions[columns[1]]
            association = Association_PlayerEdition(
                player_id = player.id,
                edition_id = edition.id,
                place=place,
                last_place=last_place,
                points=points,
                appearances=appearances,
                goals = goals,
                percentage_of_appearances = percentage_of_appearances,
                wins = wins,
                draws = draws,
                losts = losts,
                goals_scored_by_team = goals_scored_by_team,
                goals_suffered_by_team = goals_suffered_by_team,
                matchweek = matchweek
            )
            association.create()
    f.close()

    return redirect(url_for('main.index'))

@bp.route('/export_db_to_csv', methods=['GET', 'POST'])
def export_db_to_csv():
    models = Game.query.first().all_tables_object()
    instances = Game.query.first().get_all_tables()
    for model in models.keys():
        models[model] = models[model].__table__.columns.keys()
    for model in instances.keys():
        instances[model] = instances[model].all()

    values = {}
    for model in models.keys():
        values[model] = []
        for instance in instances[model]:
            instance_values = []
            for field in models[model]:
                instance_values.append(getattr(instance, field))
            values[model].append(instance_values)

    for model in models.keys():
        file = os.path.join('ligastorrinha/static/data/csv', '%s.csv' % model)
        fields = models[model]
        rows = values[model]

        with open(file, 'w') as f:
            write = csv.writer(f)

            write.writerow(fields)
            write.writerows(rows)
    return redirect(url_for('main.index'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}
