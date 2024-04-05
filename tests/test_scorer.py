import unittest

from cricket_lib.classes.scorer import Scorer


class MyTestCase(unittest.TestCase):
    def test_scorer_b_a(self):
        scorer = Scorer()

        scorer.match_reader("$ TEAM ['a' ,'b']")
        scorer.match_reader("$ TOSS b bowling")
        self.assertEqual(scorer.batting_team.name, 'a')  # add assertion here

    def test_scorer_a_b(self):
        scorer = Scorer()
        scorer.match_reader("$ TEAM ['a' ,'b']")
        scorer.match_reader("$ TOSS a bowling")
        self.assertEqual(scorer.batting_team.name, 'b')  # add assertion here

    def test_scorer_a_a(self):
        scorer = Scorer()
        scorer.match_reader("$ TEAM ['a' ,'b']")
        scorer.match_reader("$ TOSS a batting")
        self.assertEqual(scorer.batting_team.name, 'a')  # add assertion here

    def test_scorer_b_b(self):
        scorer = Scorer()
        scorer.match_reader("$ TEAM ['a' ,'b']")
        scorer.match_reader("$ TOSS b batting")
        self.assertEqual(scorer.batting_team.name, 'b')  # add assertion here


if __name__ == '__main__':
    unittest.main()