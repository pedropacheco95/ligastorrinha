from ligastorrinha import model 
from ligastorrinha.sql_db import db
from sqlalchemy import Table, Column, Integer, ForeignKey ,Enum , Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship , backref
import enum

from . import Player , Game

class Association_PlayerGame(db.Model ,model.Model, model.Base):
    __tablename__ = 'players_in_game'
    __table_args__ = {'extend_existing': True}
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    team = Column(Enum('Branquelas','Maregões',name='teams'), primary_key=True)
    goals =  Column(Integer)

    def get_game(self):
        return Game.query.filter_by(id=self.game_id).first()

    def get_player(self):
        return Player.query.filter_by(id=self.player_id).first()