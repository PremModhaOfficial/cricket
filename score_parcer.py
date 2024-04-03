
from main import Team, Opted, Player, BallType

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
$ OVER $ normal 1 batter_1 $ wicket 0 batter_1::batter_3 $ normal 6 batter_3 $ wide 1 batter_1 $ normal 6 batter_3 $ wide 1 batter_1


"""


def include(pattern: str, string: str):
	if (string.find(pattern)) == 0:
		return string[len(pattern):]
	else:
		return False


lines = score.splitlines()

commands = list(filter(lambda line: len(line) and line[0] == '$', lines))
commands = list(map(lambda a: include("$ ", a), commands))

teams_objects = []
toss_winner = ""
toss_winner_opted = Opted.NOT
players = []
current_baller: Player

current_index = 0
for index, command in enumerate(commands):
	
	if "TEAM" in command:
		teams = eval(include("TEAM ", command))
		teams_objects = list(map(lambda team_name: Team(team_name), teams))
		continue
	
	if "TOSS" in command:
		toss = command.split(" ")
		toss_winner = toss[1]
		toss_winner_opted: Opted = Opted(toss[2])
		continue
	
	if "BATTERS" in command:
		batter_names = include("BATTERS ", command).split(" ")
		players = [Player_1, Player_2] = batter_names
		players = list(map(lambda player_name: Player(player_name), players))
		continue
	
	if "BALLER" in command:
		current_baller = Player(include("BALLER ", command))
	
	if "OVER" in command:
		over_commands = include("OVER $", command)
		
		for over_command in over_commands.split("$"):
			(ball_type, runs, player) = over_command.strip().split(" ")
			current_ball_type: BallType = BallType(ball_type)
			if current_ball_type == BallType.NORMAL:
				print(f"{player} run {runs} in {ball_type}")

# if DEVMODE:
# 	print(teams_objects, toss_winner, toss_winner_opted, players)
# 	for team in teams_objects:
# 		print(team)
#
# 	for player in players:
# 		print(player)
