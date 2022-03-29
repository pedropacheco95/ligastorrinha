from datetime import date
from email.policy import default

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
    image_url = Column(Text,default= "default_player.jpg")

    user = relationship("User",back_populates='player')
    games_relations = relationship('Association_PlayerGame', back_populates='player')
    editions_relations = relationship('Association_PlayerEdition', back_populates='player')

    def editions(self):
        return [rel.edition for rel in self.editions_relations] 

    def games_played(self):
        #[rel.game for rel in self.games_relations if rel.game.played]
        return [rel.game for rel in self.games_relations] 
    
    def games_played_on_edition(self,edition):
        #[rel.game for rel in self.games_relations if rel.game.edition_id == edition.id and rel.game.played]
        return [rel.game for rel in self.games_relations if rel.game.edition_id == edition.id]

    def result_on_game(self,game):
        association = [rel for rel in self.games_relations if rel.game == game][0]
        factor = 1
        if association.team == 'Maregões':
            factor = -1
        return game.winner * factor

    def goals_on_game(self,game):
        association = [rel for rel in self.games_relations if rel.game == game][0]
        return association.goals

    def age(self):
        if self.birthday:
            today = date.today()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return None

    def full_image_url(self):
        return url_for('static', filename="images/Players/{url}".format(url=self.image_url))

    def get_games_relations_played(self,edition = None):
        relations = self.games_relations
        if edition:
            relations = [relation for relation in self.games_relations if relation.game.edition==edition]
        #[relation for relation in relations if relation.game.played]
        return relations

    def goals_scored_by_team(self,edition=None):
        relations = self.get_games_relations_played(edition)
        goals_scored_by_team = [relation.game.goals_team1 if relation.team=='Branquelas' else relation.game.goals_team2 for relation in relations]
        return sum(goals_scored_by_team)

    def goals_suffered_by_team(self,edition=None):
        relations = self.get_games_relations_played(edition)
        goals_suffered_by_team = [relation.game.goals_team1 if relation.team=='Maregões' else relation.game.goals_team2 for relation in relations]
        return sum(goals_suffered_by_team)

    def games_won(self, edition):
        relations = self.get_games_relations_played(edition)
        return [rel.game for rel in relations if rel.team=='Branquelas' and rel.game.winner==1 or rel.team=='Maregões' and rel.game.winner==-1 ]

    def games_drawn(self, edition):
        relations = self.get_games_relations_played(edition)
        return [rel.game for rel in relations if rel.game.winner==0]

    def games_lost(self, edition):
        relations = self.get_games_relations_played(edition)
        return [rel.game for rel in relations if rel.team=='Maregões' and rel.game.winner==1 or rel.team=='Branquelas' and rel.game.winner==-1 ]

    def get_all_results(self, edition):
        relations = self.get_games_relations_played(edition)
        won = [rel.game for rel in relations if rel.team=='Branquelas' and rel.game.winner==1 or rel.team=='Maregões' and rel.game.winner==-1 ]
        drawn = [rel.game for rel in relations if rel.game.winner==0]
        lost = [rel.game for rel in relations if rel.team=='Maregões' and rel.game.winner==1 or rel.team=='Branquelas' and rel.game.winner==-1 ]
        return won, drawn , lost

    def goals(self, edition):
        relations = self.get_games_relations_played(edition)
        goals = [rel.goals for rel in relations]
        return sum(goals)