from enum import Enum


class BallType(Enum):
    NORMAL = "normal"
    WIDE = "wide"
    NO_BALL = "no_ball"
    BYES = "byes"
    LEG_BYES = "leg_byes"
    WICKET = "wicket"

    @classmethod
    def get_all_types(cls):
        yield f"{cls.NORMAL.value}"
        yield f"{cls.WIDE.value}"
        yield f"{cls.NO_BALL.value}"
        yield f"{cls.BYES.value}"
        yield f"{cls.LEG_BYES.value}"
        yield f"{cls.WICKET.value}"


class Opted(Enum):
    BAT = 'batting'
    NOT = "not_decided"
    BOWL = "bowling"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.value}"

    def __str__(self):
        return self.value

    def opposite(self):

        if self == Opted.BOWL:
            return Opted.BAT
        elif self == Opted.BAT:
            return Opted.BOWL

        return Opted.NOT