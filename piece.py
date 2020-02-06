
class Rook:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,x,y,x1,y1):
		if (x == x1 and y != y1):
			return True
		elif (x != x1 and y == y1):
			return True
		else:
			return False
	def as_string(self):
		return self.color+"R"
class Knight:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,x,y,x1,y1):
		return True
	def as_string(self):
		return self.color+"k"

class Bishop:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,x,y,x1,y1):
		if (abs(x-y) == abs(x1-y1)):
			return True
		else:
			return False
	def as_string(self):
		return self.color+"B"

class Queen:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		if (x == x1 and y != y1):
			return True
		elif (x != x1 and y == y1):
			return True
		elif (abs(x-y) == abs(x1-y1)):
			return True
		else:
			return False
	def as_string(self):
		return self.color+"Q"

class King:
	def __init__(self,color):
		self.color = color
	def isValidMove(self):
		return True
	def as_string(self):
		return self.color+"K"

class Pawn:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,x,y,x1,y1,turn_number):
		x_move_distance = abs(x-x1)
		y_move_distance = abs(y-y1)
		total_move_distance = x_move_distance + y_move_distance
		if (x_move_distance == 2):
			if (turn_number < 3 and y_move_distance == 0):
				return True
			else: return False
		elif (x_move_distance > 2 or x_move_distance < 1 or y_move_distance > 1):
			return False
		else: # xmd == 1, ymd == 1 or 0
			return True
	def as_string(self):
		return self.color+"P"

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
		self.turn = "White"
		self.board_state = [[pf.new_piece(x,y) for y in range(8)] for x in range(8)]
		self.turn_number = 1

	def validate_pawn(self,x,y,x1,y1):
		active_piece = self.board_state[x][y]
		if (not active_piece.isValidMove(x,y,x1,y1,self.turn_number)): 
			return False
		y_move_distance = abs(y-y1) # implicitly know xmd == 0, ymd == 0 or 1
		if (y_move_distance == 0):
			if(not self.board_state[x1][y1]):
				return True
			else: return False
		elif (y_move_distance == 1):
			if(self.board_state[x1][y1].color == self.turn):
				return True
			else: return False
		else:
			print("shouldnt happen")

	def validate_move(self,x,y,x1,y1):
		active_piece = self.board_state[x][y]
		x_move_distance = abs(x-x1)
		y_move_distance = abs(y-y1)
		total_move_distance = x_move_distance + y_move_distance
		if (isinstance(active_piece,Pawn)):
			if(self.validate_pawn(x,y,x1,y1)):
				self.board_state[x][y], self.board_state[x1][y1] = None, self.board_state[x][y]
				return True
			else: 
				print("line 142 failed")
				return False
		elif (isinstance(active_piece,Rook)):
			if(x_move_distance != 0 and y_move_distance != 0): return False
			elif(total_move_distance > 8): return False
			else: 
				self.board_state[x][y], self.board_state[x1][y1] = None, self.board_state[x][y]
				return True
		else:
			return True
	def perform_move(self):
		self.turn = "White" if self.turn == "Black" else "Black"
		self.turn_number += 1
		print(f"turn number:{self.turn_number}")
		return
	def print_board(self):
		r = [[x.as_string() if x else "empty" for x in self.board_state[i]] for i in range(8)]
		for i in range(8):
			print(r[i])
			
	def is_valid_move(self,x,y,x1,y1,target_piece):
		pass






class Move:
	def __init__(self,x,y,x1,y1):
		self.x = x
		self.y = y
		self.x1 = x1
		self.y1 = y1


class Game:
	def __init__(self):
		self.board = Board()
		self.move_history = []
	def take_input(self):
		cmd = input("Enter move: x,y,x1,y1:")
		c = cmd.split(",")
		return [int(x) for x in c]

	def game_loop(self):
		while(True):
			g.board.print_board()
			c = self.take_input()
			self.move(c[0],c[1],c[2],c[3])


	def move(self,x,y,x1,y1):
		if(self.board.validate_move(x,y,x1,y1)):
			print("performing move....")
			self.board.perform_move()
			self.move_history.append(Move(x,y,x1,y1))

g = Game()
g.game_loop()

