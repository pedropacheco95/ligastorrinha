
import random

from ligastorrinha import model 
from ligastorrinha.sql_db import db
from sqlalchemy import Column, Integer , String , Text, ForeignKey , Boolean, Date
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
    last_team = Column(String(40))

    games = relationship('Game', back_populates='edition')
    league = relationship('League',back_populates='editions')
    players_relations = relationship('Association_PlayerEdition', back_populates='edition')

    def get_ordered_games(self):
        self.games.sort(key=lambda x: x.matchweek)
        return self.games

    def get_played_matches(self):
        #[game for game in self.games if game.played]
        return self.games

    def players_classification(self,update_places=None):
        return [rel.player for rel in self.players_relations_classification(update_places)]

    def players_relations_classification(self,update_places=None):
        sorted_by_points = self.players_relations
        sorted_by_points.sort(key=lambda x: x.points, reverse=True)
        incomplete_relation = [rel for rel in self.players_relations if not rel.place]
        if update_places or incomplete_relation:
            for index,rel in enumerate(sorted_by_points):
                rel.last_place = rel.place
                rel.place = index + 1
                rel.save()
        return sorted_by_points

    def players_relations_classification_by_goals(self):
        sorted_by_goals = self.players_relations
        sorted_by_goals.sort(key=lambda x: x.goals, reverse=True)
        return sorted_by_goals

    def player_position(self,player):
        return self.players_classification().index(player) + 1
    
    def player_in_position(self, position):
        return self.players_classification()[position-1]

    def last_updated_matchweek(self):
        return self.players_relations[0].matchweek

    def matchweek_updated(self):
        last_upadted_matchweek = self.last_updated_matchweek()
        matchweek = self.get_ordered_games()[-1].matchweek
        return last_upadted_matchweek == matchweek

    def update_table(self,force_update=False):
        matchweek = self.get_ordered_games()[-1].matchweek
        if not self.matchweek_updated() or force_update:
            for relation in self.players_relations:
                player = relation.player
                games_won , games_drawn , games_lost = player.get_all_results(self)
                wins = len(games_won)
                draws = len(games_drawn)
                losts = len(games_lost)
                goals = player.goals(self)
                goals_scored_by_team = player.goals_scored_by_team(self)
                goals_suffered_by_team = player.goals_suffered_by_team(self)

                points = wins * 4 + draws * 2 + losts + goals*0.1
                appearances = len(player.games_played_on_edition(self))
                percentage_of_appearances = round((appearances / len(self.get_played_matches()))*100,2)

                relation.points = points
                relation.appearances = appearances
                relation.percentage_of_appearances = percentage_of_appearances
                relation.wins = wins
                relation.draws = draws
                relation.losts = losts
                relation.goals = goals
                relation.goals_scored_by_team = goals_scored_by_team
                relation.goals_suffered_by_team = goals_suffered_by_team
                relation.matchweek = matchweek
                relation.save()

        self.players_classification(update_places=True) 
        return True

    def add_game_to_table(self,game):
        for game_relation in game.players_relations:
            goals = game_relation.goals
            win = 1 if (game.winner == 1 and game_relation.team == 'Branquelas') or  (game.winner == -1 and game_relation.team == 'Maregões') else 0
            draw = 1 if game.winner == 0 else 0
            lost = 1 if (game.winner == -1 and game_relation.team == 'Branquelas') or  (game.winner == 1 and game_relation.team == 'Maregões') else 0
            goals_scored_by_team = game.goals_team1
            goals_suffered_by_team = game.goals_team2

            points = win*3 + draw*1

            edition_relation = [relation for relation in game_relation.player.editions_relations if relation.edition == self][0]
            edition_relation.points += points
            edition_relation.appearances += 1
            edition_relation.percentage_of_appearances = round((edition_relation.appearances / len(self.games))*100,2)
            edition_relation.wins += win
            edition_relation.draws += draw
            edition_relation.losts += lost
            edition_relation.goals = goals
            edition_relation.goals_scored_by_team += goals_scored_by_team
            edition_relation.goals_suffered_by_team += goals_suffered_by_team
            edition_relation.matchweek = game.matchweek
            edition_relation.save()
        self.players_classification(update_places=True) 
        return True

    def players_ids_last_team(self):
        players = [rel.player.id for rel in self.players_relations]
        if self.last_team:
            players = [int(player_id) for player_id in self.last_team[:-1].split(';')]
        return players

    def make_teams(self):
        players = self.players_classification(update_places=True)

        if self.league.name == 'MasterLeague':
            random.shuffle(players)

        teams = {
            'Branquelas':[players[0],players[3],players[5],players[7],players[8],players[11]],
            'Maregões':[players[1],players[2],players[4],players[6],players[9],players[10]],
        }

        return teams