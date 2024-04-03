import random
from enum import Enum

NOBALL = {"RUN": 1, "RETHROW": True}
WIDEBALL = {"RUN": 1, "RETHROW": True}
PLAYERS_PER_TEAM = 11


class BallType(Enum):
	NORMAL = "normal"
	WIDE = "wide"
	NO_BALL = "no_ball"
	BYES = "byes"
	LEG_BYES = "leg_byes"
	WICKET = "wicket"


class Player(object):
	
	def __init__(self, name):
		self.name = name
		self.runs = 0
	
	def __str__(self):
		return f"Player {self.name}"
	
	@classmethod
	def update_player_stats(cls, player_name: str, runs, player_list: list):
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


class Opted(Enum):
	BAT = 'batting'
	NOT = "not_decided"
	BOWL = "bowling"
	
	def __str__(self):
		return self.value


class Team(object):
	
	def __init__(self, name):
		self.opted = Opted.NOT
		self.name = name
	
	def __str__(self):
		return f"Team {self.name}"


def main(host_team="host team", visitor_team="visitor team", dev_mode=False):
	print("Teams\n") if dev_mode else None
	teams = (host_team, visitor_team) = (Team(host_team), Team(visitor_team))


if __name__ == '__main__':
	main(dev_mode=True)
