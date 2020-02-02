
class Rook:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return self.color
class Knight:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return self.color
class Bishop:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return self.color
class Queen:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return self.color
class King:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return self.color
class Pawn:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return self.color
class PieceFactory:
	def new_piece(self,x,y):
		board_map = {
			(0,0) : Rook("Black"),
			(0,1) : Knight("Black"),
			(0,2) : Bishop("Black"),
			(0,3) : Queen("Black"),
			(0,4) : King("Black"),
			(0,5) : Bishop("Black"),
			(0,6) : Knight("Black"),
			(0,7) : Rook("Black"),
			(1,0) : Pawn("Black"),
			(1,1) : Pawn("Black"),
			(1,2) : Pawn("Black"),
			(1,3) : Pawn("Black"),
			(1,4) : Pawn("Black"),
			(1,5) : Pawn("Black"),
			(1,6) : Pawn("Black"),
			(1,7) : Pawn("Black"),
			(6,0) : Pawn("White"),
			(6,1) : Pawn("White"),
			(6,2) : Pawn("White"),
			(6,3) : Pawn("White"),
			(6,4) : Pawn("White"),
			(6,5) : Pawn("White"),
			(6,6) : Pawn("White"),
			(6,7) : Pawn("White"),
			(7,0) : Rook("White"),
			(7,1) : Knight("White"),
			(7,2) : Bishop("White"),
			(7,3) : Queen("White"),
			(7,4) : King("White"),
			(7,5) : Bishop("White"),
			(7,6) : Knight("White"),
			(7,7) : Rook("White")
		}

		return board_map.get((x,y),)
class Board:
	def __init__(self):
		pf = PieceFactory()
		self.board_state = [[pf.new_piece(x,y) for y in range(8)] for x in range(8)]
	def validate_move(self,x,y,x1,y1):
		return True
	def perform_move(self,x,y,x1,y1):
		pass


class Game:
	def __init__(self):
		self.turn = "White"
		self.board = Board()

	def move(self,x,y,x1,y1):
		active_piece = self.board.board_state[x][y]
		destination_piece = self.board.board_state[x1][y1]
		if (not self.turn == active_piece.color):
			print("You can't move this piece")
			return
		if (destination_piece):
			print("Someone is already located here")
			return
		if(not self.board.validate_move(x,y,x1,y1)):
			print("invalid move")
			pass
		else:
			self.board.perform_move(x,y,x1,y1)
			self.turn = "White" if self.turn == "Black" else "Black"		
		#print(active_piece.color)
		#print(destination_piece.color)	


g = Game()
g.move(7,7,5,5)

