from dataclasses import dataclass, field

import score_parcer
from cricket_lib.classes.player import Player
from cricket_lib.classes.team import Team
from cricket_lib.enums import BallType, Opted
# TODO remove these
from score_parcer import include


def handel_byes_ball(ball_info, player_ran, runs):
	player_ran.update_runs(int(runs) + 1, ball_info)


def handel_no_ball(ball_info, player_ran, runs):
	player_ran.update_runs(int(runs) + 1, ball_info)


def handel_wide_ball(ball_info, player_ran, runs):
	player_ran.update_runs(int(runs) + 1, ball_info)


def handel_normal_ball(ball_info, player_ran: Player, runs):
	player_ran.update_runs(int(runs), ball_info)


@dataclass
class Scorer(object):
	game_name: str = field(default="No game name provided", init=False)
	batting_team: Team = field(default=None, init=False)
	playing_teams: list[Team] = field(default_factory=list, init=False)
	current_baller: Player = field(default=False, init=False)
	active_batsman: Player = field(default=None, init=False)
	passive_batsman: Player = field(default=None, init=False)
	
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
					self.set_team_preference(toss[0], toss[1])
				continue
			
			if "BATTERS" in command:
				batter_names = include("BATTERS ", command).split(" ")
				players = batter_names
				[self.active_batsman, self.passive_batsman] = list(
					map(lambda player_name: Player(player_name), players))
				continue
			
			if "BALLER" in command:
				if self.current_baller:
					self.get_team(Opted.BOWL).append_player(self.current_baller, Opted.BOWL)
				self.current_baller = Player(include("BALLER ", command))
				continue
			
			if "OVER" in command:
				self.current_baller.append_over(command)
				over_commands = include("OVER $ ", command)
				
				for ball_info in over_commands.split(" $ "):
					
					(ball_type, runs, name_of_player) = ball_info.strip().split(" ")
					current_ball_type: BallType = BallType(ball_type)
					
					if "=>" in name_of_player:
						pass
					
					player_ran: Player = self.get_batsman(name_of_player)
					
					# normal ball
					if current_ball_type == BallType.NORMAL:
						print(self.active_batsman, self.passive_batsman, name_of_player, sep="\n")
						handel_normal_ball(ball_info, player_ran, runs)
						continue
					
					if current_ball_type == BallType.NO_BALL:
						handel_no_ball(ball_info, player_ran, runs)
						continue
					
					if current_ball_type == BallType.WIDE:
						handel_wide_ball(ball_info, player_ran, runs)
						continue
					
					if current_ball_type == BallType.BYES or current_ball_type == BallType.LEG_BYES:
						handel_byes_ball(ball_info, player_ran, runs)
						continue
					
					if current_ball_type == BallType.WICKET:
						self.handel_wicket(ball_info, runs)
						continue
				
				continue
	
	def set_team_preference(self, team_name: str, opted_in: str):
		team_index = -1
		opted: Opted = Opted(opted_in)
		if team_name == self.playing_teams[0].name:
			team_index = 0
			self.batting_team = self.playing_teams[0]
		elif team_name == self.playing_teams[1].name:
			team_index = 1
			self.batting_team = self.playing_teams[1]
		
		self.playing_teams[team_index].opted = opted
		# INFO to catch any error
		team_index -= 1
		self.playing_teams[team_index].opted = opted.opposite()
	
	def handel_wicket(self, ball_info, runs):
		prev_player_name, new_player_name = ball_info[9:].split('=>')
		self.get_batsman(prev_player_name).update_runs(runs, ball_info)
		print(self.get_batsman(prev_player_name))
		self.replace_batsman(prev=prev_player_name, new=new_player_name)
	
	# print(f"{prev_player_name} is replaced by {new_player_name}")
	
	def get_team(self, opted_in: Opted):
		return self.playing_teams[0] if self.playing_teams[0].opted == opted_in else self.playing_teams[1]
	
	def replace_batsman(self, prev, new):
		if self.active_batsman.name.strip() == prev.strip():
			self.active_batsman = Player(new)
			self.batting_team.append_player(self.active_batsman, Opted.BAT)
		elif self.passive_batsman.name.strip() == prev.strip():
			self.batting_team.append_player(self.passive_batsman, Opted.BAT)
			self.passive_batsman = Player(new)
	
	def get_batsman(self, name_of_player):
		if name_of_player == self.active_batsman.name:
			return self.active_batsman
		elif name_of_player == self.passive_batsman.name:
			return self.passive_batsman
