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
    game_name: str = field(default="", init=False)
    batting_team: Team = field(default=None, init=False)
    bowling_team: Team = field(default=None, init=False)
    current_baller: Player = field(default=False, init=False)
    active_batsman: Player = field(default=None, init=False)
    passive_batsman: Player = field(default=None, init=False)
    first_team_played: bool = field(default=False, init=False)

    def match_reader(self, score=score_parcer.score):
        if not score:
            return f"no score given"
        lines = score.splitlines()
        commands = list(filter(lambda line: len(line) and line[0] == '$', lines))
        commands = list(map(lambda a: include("$ ", a), commands))
        self.current_baller: Player = Player("NONE")

        for index, command in enumerate(commands):

            if "TEAM" in command:
                teams = eval(include("TEAM ", command))
                [self.batting_team, self.bowling_team] = list(map(lambda team_name: Team(team_name), teams))
                continue

            if "TOSS" in command:
                """:param toss => which team by name won toss and what they opted to do first"""
                toss = include("TOSS ", command).split(" ")

                if toss[0] == self.batting_team.name:
                    self.set_team_preference(self.batting_team, toss[1])
                else:
                    self.set_team_preference(self.bowling_team, toss[1])
                continue

            if "BATTERS" in command:
                batter_names = include("BATTERS ", command).split(" ")
                players = batter_names
                [self.active_batsman, self.passive_batsman] = list(
                    map(lambda player_name: Player(player_name), players))
                self.batting_team.players.append(self.active_batsman)
                self.batting_team.players.append(self.passive_batsman)
                continue

            if "BALLER" in command:
                # check if baller exists
                baller_exists = False
                for baller in self.bowling_team.players:
                    baller_exists = baller_exists or baller.name == include("BALLER ", command)
                    self.current_baller = baller
                    if baller_exists: break

                if self.current_baller:
                    self.get_team_by_what_they_doing(Opted.BOWL).append_player(self.current_baller, Opted.BOWL)

                if not baller_exists:
                    self.current_baller = Player(include("BALLER ", command))

                if len(self.bowling_team.players) >= 11:
                    raise Exception(f"Bowling team: {self.bowling_team} has more Than 11 players")
                self.bowling_team.players.append(self.current_baller)
                continue

            if "CHANGE" in command:
                print(self.batting_team)
                self.first_team_played = True
                self.switch_team_state()

            if "END" in command:
                exit(f"{self.batting_team.name} has won by {self.bowling_team.runs - self.batting_team.runs} runs")

            if "OVER" in command:
                self.current_baller.append_over(command)
                over_commands = include("OVER $ ", command)

                for ball_info in over_commands.split(" $ "):

                    info_tuple = (ball_type, runs, name_of_player) = ball_info.strip().split(" ")

                    current_ball_type: BallType = BallType(ball_type)

                    player_ran: Player = self.get_batsman_by_name(name_of_player)

                    # normal ball
                    if current_ball_type == BallType.NORMAL:
                        self.update_runs(runs)
                        print(self.active_batsman, self.passive_batsman, name_of_player, sep="\n")
                        handel_normal_ball(ball_info, player_ran, runs)
                        continue

                    if current_ball_type == BallType.NO_BALL:
                        self.update_runs(int(runs) + 1)
                        handel_no_ball(ball_info, player_ran, runs)
                        continue

                    if current_ball_type == BallType.WIDE:
                        self.update_runs(int(runs) + 1)
                        handel_wide_ball(ball_info, player_ran, runs)
                        continue

                    if current_ball_type == BallType.BYES or current_ball_type == BallType.LEG_BYES:
                        self.update_runs(int(runs) + 1)
                        handel_byes_ball(ball_info, player_ran, runs)
                        continue

                    if current_ball_type == BallType.WICKET:
                        self.update_runs(runs)
                        self.batting_team.wicket += 1
                        if self.batting_team.wicket >= 10:
                            exit(
                                f"{self.bowling_team} wins the game by {self.bowling_team.runs - self.batting_team.runs} runs")
                        self.handel_wicket(ball_info, runs)
                        continue

                continue

    def set_team_preference(self, team: Team, opted_in: str):
        opted: Opted = Opted(opted_in)
        self.batting_team.opted = opted
        self.bowling_team.opted = opted.opposite()

        if (self.batting_team.name == team.name and opted == Opted.BOWL) or (
                self.bowling_team.name == team.name and opted == Opted.BAT):
            temp = self.batting_team.name
            self.batting_team.name = self.bowling_team.name
            self.bowling_team.name = temp

    def get_team_by_what_they_doing(self, opted: Opted):
        if opted == Opted.BOWL:
            return self.bowling_team
        else:
            return self.batting_team

    def update_runs(self, runs):
        self.batting_team.runs += int(runs)
        if self.first_team_played and self.batting_team.runs >= self.batting_team.runs:
            exit(f'Game won by: {self.batting_team.name} by {11 - self.batting_team.wicket} wickets')

    def handel_wicket(self, ball_info, runs):

        prev_player_name, new_player_name = ball_info[9:].split('=>')
        self.get_batsman_by_name(prev_player_name).update_runs(runs, ball_info)
        print(self.get_batsman_by_name(prev_player_name))
        self.replace_batsman(prev=prev_player_name, new=new_player_name)

    # print(f"{prev_player_name} is replaced by {new_player_name}")

    def get_team_by_what_they_opted(self, opted_in: Opted):
        return self.batting_team if self.batting_team.opted == opted_in else self.bowling_team

    def replace_batsman(self, prev, new):
        if self.active_batsman.name.strip() == prev.strip():
            self.active_batsman = Player(new)
            self.batting_team.append_player(self.active_batsman, Opted.BAT)
        elif self.passive_batsman.name.strip() == prev.strip():
            self.batting_team.append_player(self.passive_batsman, Opted.BAT)
            self.passive_batsman = Player(new)

    def get_batsman_by_name(self, name_of_player):
        if name_of_player == self.active_batsman.name:
            return self.active_batsman
        elif name_of_player == self.passive_batsman.name:
            return self.passive_batsman

    def get_team_by_name(self, team_name):
        return self.batting_team if team_name == self.batting_team.name else self.bowling_team

    def get_team_opponent_by_name(self, team_name):
        return self.batting_team if team_name != self.batting_team.name else self.bowling_team

    def update_runs(self, runs):
        self.batting_team.update_runs(int(runs))
        if self.batting_team.runs >= self.bowling_team.runs and self.first_team_played:
            exit(f'batting team: {self.batting_team.name} won the match by {11 - self.batting_team.wicket} wickets')

    def switch_team_state(self):
        temp = self.batting_team
        self.batting_team = self.bowling_team
        self.bowling_team = temp

        self.batting_team.opted = Opted.BAT
        self.bowling_team.opted = Opted.BOWL