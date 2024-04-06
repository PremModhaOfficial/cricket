import matplotlib.pyplot as plt
import numpy as np

from cricket_lib.classes.scorer import Scorer
from cricket_lib.classes.team import Team


def plot_run_rate(ax, team: Team):
    run_rate_list = []
    for over_index, run in enumerate(team.runs_per_over):
        over_number = over_index + 1
        run_rate_list.append(run / over_number)
    ax.plot(np.arange(start=1, stop=(len(run_rate_list) + 1)), run_rate_list)


def plot_per_player_runs(ax, team: Team):
    ax.set_title(f"per player runs of {team.name}")
    p_list = []
    r_list = []
    for player in team.players:
        p_list.append(player.name)
        r_list.append(player.runs)
    ax.bar(p_list, r_list)


class Plotter(object):

    def __init__(self, scorer):
        self.scorer: Scorer = scorer

    def plot_over_wise_runs(self):
        fig = plt.figure(figsize=(20, 20))
        fig.set_dpi(500)

        ax1 = fig.add_subplot(411)
        ax2 = fig.add_subplot(412)
        ax3 = fig.add_subplot(413)
        ax4 = fig.add_subplot(414)

        ax1.set_title("Runs per Over")
        bat_overs = len(self.scorer.batting_team.runs_per_over)
        bat_overs = np.arange(start=1, stop=bat_overs + 1, step=1)
        ax1.plot(bat_overs, self.scorer.batting_team.runs_per_over)
        bowl_overs = len(self.scorer.bowling_team.runs_per_over)
        bowl_overs = np.arange(start=1, stop=bowl_overs + 1, step=1)
        ax1.plot(bowl_overs, self.scorer.bowling_team.runs_per_over)
        ax1.legend([self.scorer.batting_team.name, self.scorer.bowling_team.name])
        self.plot_both_run_rate(ax2)
        plot_per_player_runs(ax3, self.scorer.batting_team)
        plot_per_player_runs(ax4, self.scorer.bowling_team)

    def plot_both_run_rate(self, ax2):
        ax2.set_title("Run RATE")
        ax2.legend([self.scorer.batting_team.name, self.scorer.bowling_team.name])
        plot_run_rate(ax2, self.scorer.batting_team)
        plot_run_rate(ax2, self.scorer.bowling_team)
        ax2.legend([self.scorer.batting_team.name, self.scorer.bowling_team.name])