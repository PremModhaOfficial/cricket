from dataclasses import dataclass, field

import score_parcer
from cricket_lib.classes.player import Player
from cricket_lib.classes.team import Team
from cricket_lib.enums import BallType, Opted
# TODO remove these
from score_parcer import include


@dataclass
class Scorer(object):
	game_name: str = field(default="No game name provided", init=False)
	batting_team: Team = field(default=None, init=False)
	playing_teams: list[Team] = field(default_factory=list)
	current_baller: Player = field(default=None, init=False)
	active_player_1: Player = field(default=None, init=False)
	active_player_2: Player = field(default=None, init=False)
	
	def update_player_stats(self, player_name: str, runs, player_list: list[Player]):
		if not player_list:
			print("!!!" * 10, " Player list Empty", sep="\n")
			return False
		
		current_player: Player
		for player in player_list:
			if player.name == player_name:
				current_player = player
				break
		else:
			print(f"Player {player_name} not found")
			return False
		
		current_player.runs += int(runs)
	
	# TODO implement better score
	def match_reader(self, score=score_parcer.score):
		lines = score.splitlines()
		commands = list(filter(lambda line: len(line) and line[0] == '$', lines))
		commands = list(map(lambda a: include("$ ", a), commands))
		self.current_baller: Player = Player("NONE")
		for index, command in enumerate(commands):
			
			if "TEAM" in command:
				teams = eval(include("TEAM ", command))
				self.playing_teams = list(map(lambda team_name: Team(team_name), teams))
				continue
			
			if "TOSS" in command:
				""":param toss => which team by name won toss and what they opted to do first"""
				toss = include("TOSS ", command).split(" ")
				
				if toss[0] == self.playing_teams[0].name:
					self.set_team_preference(toss[0], toss[2])
				continue
			
			if "BATTERS" in command:
				batter_names = include("BATTERS ", command).split(" ")
				players = [Player_1, Player_2] = batter_names
				players = list(map(lambda player_name: Player(player_name), players))
				continue
			
			if "BALLER" in command:
				self.current_baller = Player(include("BALLER ", command))
				continue
			
			if "OVER" in command:
				self.current_baller.append_over(command)
				over_commands = include("OVER $", command)
				
				for over_command in over_commands.split("$"):
					(ball_type, runs, player) = over_command.strip().split(" ")
					current_ball_type: BallType = BallType(ball_type)
					if current_ball_type == BallType.NORMAL:
						print(f"{player} run {runs} in {ball_type}")
				continue
	
	def set_team_preference(self, team_name: str, opted_in: str, opted_out: str):
		team_index = -1
		opted: Opted = Opted(opted_in)
		if team_name == self.playing_teams[0].name:
			team_index = 0
		elif team_name == self.playing_teams[1].name:
			team_index = 1
		
		self.playing_teams[team_index].opted = opted
		# INFO to catch any error
		team_index -= 1
		self.playing_teams[team_index].opted = opted.opposite()
