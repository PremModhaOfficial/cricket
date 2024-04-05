from cricket_lib.classes.scorer import Scorer
from cricket_lib.enums import Opted, BallType
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

    def get_bowler_name(self):
        baller_name = input(f"Enter Baller name: ")
        self.current_info = f"$ BALLER {baller_name}"
        self.log += self.current_info
        return self.current_info

    def get_over(self):
        batting_runs = self.scorer.batting_team.runs
        bowling_runs = self.scorer.bowling_team.runs
        self.current_info = "$ OVER"

        valid_balls_remain = 6
        while valid_balls_remain > 0 and not (self.scorer.first_team_played and batting_runs - bowling_runs > 0):
            # get full over when not first_team_played
            prompt: dict = dict.fromkeys(range(0, 6))
            print("Select ball type")

            ball_number = None
            while ball_number not in prompt.keys():
                for index, ball_type in enumerate(BallType.get_all_types()):
                    print(index, ball_type)
                    prompt[int(index)] = ball_type
                ball_number = int(input("\n"))

            current_ball_type: BallType = BallType(prompt[ball_number])
            runs = input('enter runs made')
            players = dict.fromkeys(range(2))
            players[0] = self.scorer.active_batsman.name
            players[1] = self.scorer.passive_batsman.name
            print('enter player')
            print(players)
            player = -1
            current_ball_type = current_ball_type.value

            while player not in ['1', '0']:
                player = input("enter player number")
            if current_ball_type != BallType.WICKET.value:
                self.current_info += f" $ {current_ball_type} {runs} {players[int(player)]}"
            else:
                new_player = input("enter player name")
                self.current_info += f" $ {current_ball_type} {runs} {players[int(player)]}::{new_player}"

            self.log += self.current_info
            print(self.current_info)

            if current_ball_type == BallType.WIDE.value or current_ball_type == BallType.NO_BALL.value:
                continue
            valid_balls_remain -= 1

    def end_game(self):
        self.current_info = "$ END"
        self.log += self.current_info
        return "$ END"

    def change_sides(self):
        self.current_info = "$ CHANGE"
        self.log += self.current_info
        return "$ CHANGE"