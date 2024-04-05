from dataclasses import dataclass, field

from cricket_lib.classes.player import Player
from cricket_lib.enums import Opted


@dataclass
class Team(object):
    name: str = field(init=True)
    # this creates a new list everytime
    opted: Opted = field(default=Opted.NOT, init=False)
    players: list[Player] = field(default_factory=list)
    runs: int = field(default=0, init=False)
    wicket: int = field(default=0, init=False)

    def append_player(self, current_baller: Player, player_type: Opted):
        self.players.append(current_baller)

    def update_runs(self, runs):
        self.runs += int(runs)