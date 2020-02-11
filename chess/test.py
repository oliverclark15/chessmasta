from piece import Move, Game
from pgn_parser import parse

games = parse()


test_game = Game()
for game in games[:1]:
	for move in game:
		print(move)

	for move in game:
		print(move)
		test_game.move(move)
		test_game.board.print_board()



