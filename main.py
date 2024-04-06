import score_parcer
from cricket_lib.classes.ploter import Plotter
from cricket_lib.classes.score_writer import ScoreWriter
from cricket_lib.classes.scorer import Scorer

NOBALL = {"RUN": 1, "RETHROW": True}
WIDEBALL = {"RUN": 1, "RETHROW": True}
PLAYERS_PER_TEAM = 11


scorer = Scorer()

score_writer = ScoreWriter(scorer)
#scorer.match_reader(score_parcer.score)

scorer.match_reader(score_writer.get_team_names())
scorer.match_reader(score_writer.get_toss_info())

scorer.match_reader(score_writer.get_init_batsman())

# play overs
total_overs = int(input('How many overs would you like to play? '))
for over in range(total_overs):
    print()
    scorer.match_reader(score_writer.get_bowler_name())
    print("over", over + 1, score_writer.scorer.current_baller.name)
    scorer.match_reader(score_writer.get_over())

scorer.match_reader(score_writer.change_sides())
scorer.match_reader(score_writer.get_init_batsman())
for over in range(total_overs):
    print()
    scorer.match_reader(score_writer.get_bowler_name())
    print("over", over + 1, score_writer.scorer.current_baller.name)
    scorer.match_reader(score_writer.get_over())
# scorer.match_reader(score)

plot = Plotter(scorer)
plot.plot_over_wise_runs()
print(score_writer.log)

scorer.match_reader(score_writer.end_game())