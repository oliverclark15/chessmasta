from piece import Move
from pgn_parser import parse

games = parse()

for game in games[:1]:
	for move in game:
		print(move)



