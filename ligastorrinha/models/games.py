from ligastorrinha import model 
from ligastorrinha.sql_db import db
from sqlalchemy import Column, Integer , String , Text, ForeignKey , Date
from sqlalchemy.orm import relationship

class Game(db.Model ,model.Model, model.Base):
    __tablename__ = 'games'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    goals_team1 = Column(Integer, nullable=False)
    goals_team2 = Column(Integer, nullable=False)
    date = Column(Date)
    winner = Column(Integer, nullable=False)
    matchweek = Column(Integer, nullable=False)
    edition_id =  Column(Integer, ForeignKey('editions.id'))

    edition = relationship("Edition",back_populates='games', lazy='subquery')
    players = relationship('Player', secondary='players_in_game', lazy='subquery',back_populates='games')

    def players_by_team(self):
        teams = {}
        teams['Branquelas'] = []
        teams['Maregões'] = []
        associations = [self.get_table('players_in_game').filter_by(player_id=player.id,game_id = self.id).one() for player in self.players]
        for association in associations:
            player = association.get_player()
            teams[association.team].append((association,player))

        return teams
