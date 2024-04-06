DEVMODE = False
score = """
$ TEAM ['host_team_name', 'visitor_team_name']

$ TOSS host_team_name batting

$ BATTERS batter_1 batter_2

$ BALLER baller_1

$ OVER $ normal 9 batter_1 $ wicket 9 batter_1=>batter_3 $ normal 9 batter_3 $ wide 1 batter_2 $ normal 6 batter_3 $ wide 1 batter_2
$ OVER $ normal 1 batter_3 $ wicket 9 batter_3=>batter_4 $ normal 3 batter_4 $ wide 1 batter_2 $ normal 6 batter_4 $ wide 1 batter_2
$ OVER $ normal 6 batter_4 $ wicket 9 batter_4=>batter_5 $ normal 6 batter_5 $ wide 6 batter_2 $ normal 6 batter_5 $ wide 6 batter_2

$ CHANGE

$ BATTERS batter_1 batter_2

$ BALLER baller_1

$ OVER $ normal 0 batter_1 $ wicket 9 batter_1=>batter_3 $ normal 9 batter_3 $ wide 1 batter_2 $ normal 6 batter_3 $ wide 1 batter_2
$ OVER $ normal 1 batter_3 $ wicket 9 batter_3=>batter_4 $ normal 3 batter_4 $ wide 1 batter_2 $ normal 6 batter_4 $ wide 1 batter_2
$ OVER $ normal 0 batter_4 $ wicket 9 batter_4=>batter_5 $ normal 6 batter_5 $ wide 6 batter_2 $ normal 6 batter_5 $ wide 6 batter_2
$ OVER $ normal 0 batter_2 $ normal 6 batter_5 $ wide 6 batter_2 $ normal 6 batter_5 $ wide 6 batter_2 $ normal 6 batter_5 $ wide 6 batter_2

"""


def include(pattern: str, string: str):
	if (string.find(pattern)) == 0:
		return string[len(pattern):]
	else:
		return False