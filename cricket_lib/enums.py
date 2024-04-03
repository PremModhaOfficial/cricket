from enum import Enum


class BallType(Enum):
	NORMAL = "normal"
	WIDE = "wide"
	NO_BALL = "no_ball"
	BYES = "byes"
	LEG_BYES = "leg_byes"
	WICKET = "wicket"


class Opted(Enum):
	BAT = 'batting'
	NOT = "not_decided"
	BOWL = "bowling"
	
	def __str__(self):
		return self.value
	
	def opposite(self):
		
		if self == Opted.BOWL:
			return Opted.BAT
		elif self == Opted.BAT:
			return Opted.BOWL
		
		return Opted.NOT
