from datetime import date

from ligastorrinha import model 
from ligastorrinha.sql_db import db
from ligastorrinha.tools import reify
from sqlalchemy import Column, Integer , String , Text, ForeignKey, Table , Date
from sqlalchemy.orm import relationship
from flask import session , url_for

class Player(db.Model ,model.Model, model.Base):
    __tablename__ = 'players'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    full_name =  Column(Text, unique=True)
    birthday = Column(Date)

    user = relationship("User",back_populates='player', uselist=False, lazy='subquery')
    games = relationship("Game", secondary='players_in_game', lazy='subquery',back_populates='players')
    editions = relationship("Edition", secondary='players_in_edition', lazy='subquery',back_populates='players')
    
    def games_played_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'games_played_on_edition' not in session[edition.name][self.name]:
            #Verify the edition exists
            editions = self.get_table('editions').all()
            if edition not in editions:
                raise ValueError
            session[edition.name][self.name]['games_played_on_edition'] =  [game for game in self.games if game.edition_id == edition.id]
        return session[edition.name][self.name]['games_played_on_edition']

    def player_in_game_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'player_in_game_on_edition' not in session[edition.name][self.name]:
            games_on_edition = self.games_played_on_edition(edition)
            session[edition.name][self.name]['player_in_game_on_edition'] =  [self.get_table('players_in_game').filter_by(player_id=self.id,game_id = game.id).one() for game in games_on_edition]
        return session[edition.name][self.name]['player_in_game_on_edition']
    
    def n_games_won_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'n_games_won_on_edition' not in session[edition.name][self.name]:
            session[edition.name][self.name]['n_games_won_on_edition'] = len([pig for pig in self.player_in_game_on_edition(edition) if (pig.get_game().winner == 1 and pig.team == 'Branquelas') or (pig.get_game().winner == -1 and pig.team == 'Maregões')])
            print(self, session[edition.name][self.name]['n_games_won_on_edition'])
        return session[edition.name][self.name]['n_games_won_on_edition']

    def n_games_tied_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'n_games_tied_on_edition' not in session[edition.name][self.name]:
            session[edition.name][self.name]['n_games_tied_on_edition'] = len([game for game in self.games_played_on_edition(edition) if game.winner == 0])
        return session[edition.name][self.name]['n_games_tied_on_edition'] 

    def n_games_lost_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'n_games_lost_on_edition' not in session[edition.name][self.name]:
            session[edition.name][self.name]['n_games_lost_on_edition'] = len([pig for pig in self.player_in_game_on_edition(edition) if (pig.get_game().winner == -1 and pig.team == 'Branquelas') or (pig.get_game().winner == 1 and pig.team == 'Maregões')])
        return session[edition.name][self.name]['n_games_lost_on_edition']
    
    def goals_scored_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'goals_scored_on_edition' not in session[edition.name][self.name]:
            player_in_game = self.player_in_game_on_edition(edition)
            goals  = 0
            for game_played in player_in_game:
                goals += game_played.goals
            session[edition.name][self.name]['goals_scored_on_edition'] = goals
        return session[edition.name][self.name]['goals_scored_on_edition']

    def goals_scored_by_team_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'goals_scored_by_team_on_edition' not in session[edition.name][self.name]:
            goals = 0
            for pig in self.player_in_game_on_edition(edition):
                if pig.team == 'Branquelas':
                    goals += pig.get_game().goals_team1
                else:
                    goals += pig.get_game().goals_team2
            session[edition.name][self.name]['goals_scored_by_team_on_edition'] = goals
        return session[edition.name][self.name]['goals_scored_by_team_on_edition']

    def goals_suffered_by_team_on_edition(self,edition):
        if edition.name not in session.keys():
            session[edition.name] = {}
        if self.name not in session[edition.name].keys():
            session[edition.name][self.name] = {}
        if 'goals_suffered_by_team_on_edition' not in session[edition.name][self.name]:
            goals = 0
            for pig in self.player_in_game_on_edition(edition):
                if pig.team == 'Branquelas':
                    goals += pig.get_game().goals_team2
                else:
                    goals += pig.get_game().goals_team1
            session[edition.name][self.name]['goals_suffered_by_team_on_edition'] = goals
        return session[edition.name][self.name]['goals_suffered_by_team_on_edition']

    def points_on_edition(self,edition):
        #Formula to calculate points: 
        #   3 points times the number of victories
        #   1 point times the number of ties
        #   1 point times the number of presences
        #   0.1 points times the goals scored
        return 3*self.n_games_won_on_edition(edition) + self.n_games_tied_on_edition(edition) + len(self.games_played_on_edition(edition)) + .1 * self.goals_scored_on_edition(edition)

    def image_url(self):
        filename = 'images/Players/' + str(self.id) + '.jpg'
        return url_for('static', filename=filename)

    def result_on_game(self,game):
        association = self.get_table('players_in_game').filter_by(player_id=self.id,game_id = game.id).one()
        if association.team == 'Maregões':
            factor = -1
        else:
            factor = 1
        return game.winner * factor

    def goals_on_game(self,game):
        association = self.get_table('players_in_game').filter_by(player_id=self.id,game_id = game.id).one()
        return association.goals

    def age(self):
        if self.birthday:
            today = date.today()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return None