from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ligastorrinha.models import User , Player , Edition , League

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@bp.route('/experience_player', methods=('GET', 'POST'))
def experience_player():
    player = Player.query.filter_by(name='Pacheco').first()

    edition = Edition.query.filter_by(name='1ª Edição MasterLeague').first()

    print('____________________________')
    print('____________________________')
    print(player.games_played_on_edition(edition))
    print(player.n_games_won_on_edition(edition))
    print(player.n_games_tied_on_edition(edition))
    print(player.n_games_lost_on_edition(edition))
    print(player.goals_scored_on_edition(edition))
    print('Player points:' , player.points_on_edition(edition))
    print('____________________________')
    print('____________________________')

    players = edition.players

    table_values = {}
    for player in players:
        table_values[player.name] = {
            'place' : 1,
            'points': player.points_on_edition(edition),
            'appearances': len(player.games_played_on_edition(edition)),
            'goals': player.goals_scored_on_edition(edition),
            'percentage of appearances': (len(player.games_played_on_edition(edition))/len(edition.games)) * 100,
            'wins': player.n_games_won_on_edition(edition),
            'draws': player.n_games_tied_on_edition(edition),
            'losts': player.n_games_lost_on_edition(edition),
            'goals scored by team': player.goals_scored_by_team_on_edition(edition),
            'goals suffered by team': player.goals_suffered_by_team_on_edition(edition)
        }

    table_values = {key: value for key, value in sorted(table_values.items(), key=lambda item: item[1]['points'], reverse=True)}

    print(list(table_values.keys()))
    for index in range(len(table_values)):
        key = list(table_values.keys())[index]
        table_values[key]['place'] = index + 1
        
    print('____________________________')
    print('____________________________')
    print(table_values)
    print('____________________________')
    print('____________________________')
    print([league.name for league in League.query.all()])
    print('____________________________')
    print('____________________________')
    print(url_for('scores.table',league_name = 'MasterLeague', edition_name = '1ª Edição MasterLeague'))
    print('____________________________')
    print('____________________________')

    return render_template('index.html')