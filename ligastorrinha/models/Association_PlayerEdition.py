from ligastorrinha import model 
from ligastorrinha.sql_db import db
from sqlalchemy import Table, Column, Integer, ForeignKey , Sequence , Float
from sqlalchemy.orm import relationship , backref

from . import Player , Edition

class Association_PlayerEdition(db.Model ,model.Model, model.Base):
    __tablename__ = 'players_in_edition'
    __table_args__ = {'extend_existing': True}
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    edition_id = Column(Integer, ForeignKey('editions.id'), primary_key=True)

    place = Column(Integer)
    last_place = Column(Integer)
    points = Column(Float)
    appearances = Column(Integer)
    goals = Column(Integer)
    percentage_of_appearances = Column(Float)
    wins = Column(Integer)
    draws = Column(Integer)
    losts = Column(Integer)
    goals_scored_by_team = Column(Integer)
    goals_suffered_by_team = Column(Integer)
    matchweek = Column(Integer)

    def get_edition(self):
        return Edition.query.filter_by(id=self.edition_id).first()

    def get_player(self):
        return Player.query.filter_by(id=self.player_id).first()

    def get_player_results(self,recalculate = False):
        if self.get_edition().games:
            if recalculate:
                percentage_of_appearances = round((len(self.get_player().games_played_on_edition(self.get_edition()))/len(self.get_edition().games)) * 100, 2) if len(self.get_edition().games) else 0.00
                self.last_place = self.place
                self.place = 1
                self.points = self.get_player().points_on_edition(self.get_edition())
                self.appearances = len(self.get_player().games_played_on_edition(self.get_edition()))
                self.goals = self.get_player().goals_scored_on_edition(self.get_edition())
                self.percentage_of_appearances =percentage_of_appearances
                self.wins = self.get_player().n_games_won_on_edition(self.get_edition())
                self.draws = self.get_player().n_games_tied_on_edition(self.get_edition())
                self.losts = self.get_player().n_games_lost_on_edition(self.get_edition())
                self.goals_scored_by_team = self.get_player().goals_scored_by_team_on_edition(self.get_edition())
                self.goals_suffered_by_team = self.get_player().goals_suffered_by_team_on_edition(self.get_edition())
                self.matchweek = self.get_edition().get_ordered_games()[-1].matchweek
                self.save()
        else:
            self.last_place = self.place
            self.place = 1
            self.points = 0
            self.appearances = 0
            self.goals = 0
            self.percentage_of_appearances = 0.00
            self.wins = 0
            self.draws = 0
            self.losts = 0
            self.goals_scored_by_team = 0
            self.goals_suffered_by_team = 0
            self.matchweek = 0
        
        scores = {
            'place' : self.place,
            'last_place' : self.last_place,
            'points': self.points,
            'appearances': self.appearances,
            'goals': self.goals,
            'percentage of appearances':self.percentage_of_appearances,
            'wins': self.wins,
            'draws': self.draws,
            'losts': self.losts,
            'goals scored by team': self.goals_scored_by_team,
            'goals suffered by team': self.goals_suffered_by_team
        }

        return scores
