from cricket_lib.classes.score_writer import ScoreWriter
from cricket_lib.classes.scorer import Scorer

NOBALL = {"RUN": 1, "RETHROW": True}
WIDEBALL = {"RUN": 1, "RETHROW": True}
PLAYERS_PER_TEAM = 11


def main(host_team="host team", visitor_team="visitor team", dev_mode=False):
    scorer = Scorer()
    score_writer = ScoreWriter(scorer)

    scorer.match_reader(score_writer.get_team_names())
    scorer.match_reader(score_writer.get_toss_info())

    scorer.match_reader(score_writer.get_init_batsman())

    # play overs
    total_overs = int(input('How many overs would you like to play? '))
    for over in range(total_overs):
        print()
        print("over", over + 1)
        scorer.match_reader(score_writer.get_bowler_name())
        scorer.match_reader(score_writer.get_over())

    scorer.match_reader(score_writer.change_sides())
    for over in range(total_overs):
        print()
        print("over", over + 1)
        scorer.match_reader(score_writer.get_bowler_name())
        scorer.match_reader(score_writer.get_over())
    # scorer.match_reader(score)

    scorer.match_reader(score_writer.end_game())

    print(scorer)


if __name__ == '__main__':
    main(dev_mode=True)