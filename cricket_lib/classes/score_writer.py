from cricket_lib.classes.scorer import Scorer
from cricket_lib.enums import Opted
from score_parcer import DEVMODE


class ScoreWriter:

    def __init__(self, scorer):
        self.log = ""
        self.current_info: str = ""
        self.scorer: Scorer = scorer

    def get_game_name(self):
        if self.scorer.game_name:
            return self.scorer.game_name
        self.scorer.game_name = input("Enter game name: ")

    def get_team_names(self):
        host_team_name = input("Enter host team name: ")
        visitor_team_name = input("Enter visitor team name: ")
        current_info = f"$ TEAM ['{host_team_name}' ,'{visitor_team_name}']"
        self.log += current_info

        (print(current_info) if DEVMODE else None)

        return current_info

    def get_toss_info(self):
        got_valid_info = False
        while not got_valid_info:
            match input(f'who won the toss?: \n1: {self.scorer.batting_team.name}\n2: {self.scorer.bowling_team.name}'):
                case '1':
                    match input(f"{self.scorer.batting_team.name}: opted to?\n1: Bat \n2: Ball"):
                        case '1':
                            self.current_info = f"$ TOSS {self.scorer.batting_team.name} {Opted.BAT.value}"
                            got_valid_info = True
                            break
                        case '2':
                            self.current_info = f"$ TOSS {self.scorer.batting_team.name} {Opted.BOWL.value}"
                            got_valid_info = True
                            break
                case '2':
                    match input(f"{self.scorer.bowling_team.name}: opted to?\n1: Bat \n2: Ball"):
                        case '1':
                            self.current_info = f"$ TOSS {self.scorer.bowling_team.name} {Opted.BAT.value}"
                            got_valid_info = True
                            break
                        case '2':
                            self.current_info = f"$ TOSS {self.scorer.bowling_team.name} {Opted.BOWL.value}"
                            got_valid_info = True
                            break
        print(self.current_info) if DEVMODE else None
        self.log += self.current_info
        return self.current_info

    def get_init_batsman(self):
        batter_1 = input(f"Enter Batter No: {len(self.scorer.batting_team.players) + 1} Name: ")
        batter_2 = input(f"Enter Batter No: {len(self.scorer.batting_team.players) + 2} Name: ")
        self.current_info = f"$ BATTERS {batter_1} {batter_2}"
        self.log += self.current_info
        print(self.current_info) if DEVMODE else None
        return self.current_info

    def get_init_bowler(self):
        baller_name = input(f"Enter Baller name: ")
        self.current_info = f"$ BALLER {baller_name}"
        self.log += self.current_info
        return self.current_info