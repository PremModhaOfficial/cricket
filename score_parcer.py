DEVMODE = True
score = """
$ TEAM ['host_team_name', 'visitor_team_name']

BAT = 'batting' ||  NOT = "not_decided" ||  BOWL = "bowling"
toss    won_by           opted to
$ TOSS host_team_name batting

begin match


$ BATTERS batter_1 batter_2

over 1
$ BALLER baller_1
$ OVER $ normal 9 batter_1 $ wicket 9 batter_1=>batter_3 $ normal 9 batter_3 $ wide 1 batter_2 $ normal 6 batter_3 $ wide 1 batter_2

$ CHANGE

$ BATTERS batter_1 batter_2

over 1
$ BALLER baller_1
$ OVER $ normal 9 batter_1 $ wicket 9 batter_1=>batter_3 $ normal 6 batter_3 $ wide 1 batter_2 $ normal 6 batter_3 $ wide 1 batter_2

$ END
"""


def include(pattern: str, string: str):
	if (string.find(pattern)) == 0:
		return string[len(pattern):]
	else:
		return False