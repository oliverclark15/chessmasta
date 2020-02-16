from chess import Game, GameOver
from pgn_parser import parse

games = parse()

#print(games)
i=1
for game in games[5:6]:
	test_game = Game()
	print(f"================Game #{i}====================")
	for move in game:
		try:
			print(move)
			test_game.move(move)
			test_game.board.print_board()		
		except GameOver:
			test_game.board.print_board()
			print(f"================Game #{i} OVER====================")
			print(len(games))
			i+=1
			break
			



