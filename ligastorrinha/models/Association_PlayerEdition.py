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
    last_place = Column(Integer,default=0)
    points = Column(Float,default=0)
    appearances = Column(Integer,default=0)
    goals = Column(Integer,default=0)
    percentage_of_appearances = Column(Float,default=0)
    wins = Column(Integer,default=0)
    draws = Column(Integer,default=0)
    losts = Column(Integer,default=0)
    goals_scored_by_team = Column(Integer,default=0)
    goals_suffered_by_team = Column(Integer,default=0)
    matchweek = Column(Integer,default=0)

    edition = relationship('Edition', back_populates='players_relations')
    player = relationship('Player', back_populates='editions_relations')
