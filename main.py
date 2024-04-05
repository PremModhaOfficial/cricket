from enum import Enum

from cricket_lib.classes.score_writer import ScoreWriter
from cricket_lib.classes.scorer import Scorer
from score_parcer import score

NOBALL = {"RUN": 1, "RETHROW": True}
WIDEBALL = {"RUN": 1, "RETHROW": True}
PLAYERS_PER_TEAM = 11


def main(host_team="host team", visitor_team="visitor team", dev_mode=False):

	scorer = Scorer()
	score_writer = ScoreWriter(scorer)
	#
	# scorer.match_reader(score_writer.get_team_names())
	# scorer.match_reader(score_writer.get_toss_info())
	#
	# scorer.match_reader(score_writer.get_init_batsman())
	# scorer.match_reader(score_writer.get_init_bowler())
	scorer.match_reader(score)

	print(scorer)


if __name__ == '__main__':
	main(dev_mode=True)