from email.policy import default
from ligastorrinha import model 
from ligastorrinha.sql_db import db
from sqlalchemy import Column, Integer , String , Table, ForeignKey , Boolean, Date
from sqlalchemy.orm import relationship

class Edition(db.Model ,model.Model , model.Base):
    __tablename__ = 'editions'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    time = Column(String(10))
    final_game = Column(Date)
    has_ended = Column(Boolean,default=False)
    number_of_teams_made = Column(Integer,default=0)
    league_id = Column(Integer, ForeignKey('leagues.id'))

    games = relationship('Game', back_populates='edition')
    league = relationship("League",back_populates='editions', lazy='subquery')
    players = relationship('Player',secondary='players_in_edition', lazy='subquery',back_populates='editions')

    def get_ordered_games(self):
        self.games.sort(key=lambda x: x.matchweek)
        return self.games
