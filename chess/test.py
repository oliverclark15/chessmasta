from chess import Game
from pgn_parser import parse

games = parse()

i=1
for game in games[2:3]:
	test_game = Game()
	print(f"================Game #{i}====================")
	for move in game:
		print(move)
		test_game.move(move)
		test_game.board.print_board()
		i+=1



