
class Rook:
	def __init__(self,color):
		self.color = color
		self.has_moved = False
	def isValidMove(self,move):
		if (move.x == move.x1 and move.y != move.y1):
			return True
		elif (move.x != move.x1 and move.y == move.y1):
			return True
		else:
			return False
	def as_string(self):
		return self.color+"R"
class Knight:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,move):
		xmd = abs(move.x-move.x1)
		ymd = abs(move.y-move.y1)
		if (xmd == 2 and ymd == 1):
			return True
		if (xmd == 1 and ymd == 2):
			return True
		return False
	def as_string(self):
		return self.color+"k"

class Bishop:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,move):
		if (abs(move.x-move.x1) == abs(move.y-move.y1)):
			return True
		else:
			return False
	def as_string(self):
		return self.color+"B"

class Queen:
	def __init__(self,color):
		self.color = color
	def isValidMove(self,move):
		if (move.x == move.x1 and move.y != move.y1):
			return True
		elif (move.x != move.x1 and move.y == move.y1):
			return True
		elif (abs(move.x-move.x1) == abs(move.y-move.y1)):
			return True
		else:
			print("hi")
			return False
	def as_string(self):
		return self.color+"Q"

class King:
	def __init__(self,color):
		self.color = color
		self.has_moved = False
	def isValidMove(self,move):
		xmd = abs(move.x-move.x1)
		ymd = abs(move.y-move.y1)
		"""
		print('\n')
		print('\n')
		print(xmd)
		print('\n')
		print('\n')
		print(ymd)
		print('\n')
		print('\n')
		"""
		if (ymd == 2 and xmd == 0):
			return True
		elif (xmd > 1 or ymd > 1):
			return False
		else:
			print("hi")
			return True
	def as_string(self):
		return self.color+"K"

class Pawn:
	def __init__(self,color):
		self.color = color
		self.first_move = True
	def isValidMove(self,move):

		x_move_distance = abs(move.x-move.x1)
		y_move_distance = abs(move.y-move.y1)
		total_move_distance = x_move_distance + y_move_distance
		if (((move.x-move.x1) > 0) and self.color == "Black"): # check direction of pawn move
			return False
		if (((move.x-move.x1) < 0) and self.color == "White"): # check direction of pawn move
			return False


		if (x_move_distance == 2):
			if (self.first_move and y_move_distance == 0):
				self.first_move = False
				return True
			else: return False
		elif (x_move_distance > 2 or x_move_distance < 1 or y_move_distance > 1):
			
			return False
		else: # xmd == 1, ymd == 1 or 0
			self.first_move = False
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


	def get_move_type(self,move):
		active_piece = self.board_state[move.x][move.y]
		x_move_distance, y_move_distance = abs(move.x-move.x1), abs(move.y-move.y1)
		if(isinstance(active_piece, King) and y_move_distance == 2 and x_move_distance == 0):
			return "Castling"
		elif(False):
			return "Promotion"
		elif(False):
			return "En-passant"
		else:
			return "Normal"

	def validate_pawn(self,move):
		active_piece = self.board_state[move.x][move.y]
		if (not active_piece.isValidMove(move)): 
			print("140")
			return False
		y_move_distance = abs(move.y-move.y1) # implicitly know xmd == 0, ymd == 0 or 1
		if (y_move_distance == 0):
			if(not self.board_state[move.x1][move.y1]):
				return True
			else:
				print("146")
				return False
		elif (y_move_distance == 1):
			if(self.board_state[move.x1][move.y1].color == self.turn):
				return True
			else:
				print("150")
				return True
		else:
			print("shouldnt happen")

	def validate_castling(self,move):
		active_piece = self.board_state[move.x][move.y]
		dest_piece = self.board_state[move.x1][move.y1]
		castle_y = 7 if move.y1 == 6 else 0
		castle_piece = self.board_state[move.x1][castle_y]
		
		if(not castle_piece):
			return False
		if(not isinstance(castle_piece,Rook)):
			return False
		if (active_piece.has_moved or castle_piece.has_moved):
			return False

		return True
		# check if pieces between
		# check if king is in check
		# pass through square attacked
		# king does not end up in check

	

	def validate_move(self,move):
		active_piece = self.board_state[move.x][move.y]
		dest_piece = self.board_state[move.x1][move.y1]


		x_move_distance, y_move_distance = abs(move.x-move.x1), abs(move.y-move.y1)
		total_move_distance = x_move_distance + y_move_distance
		if (isinstance(active_piece,Pawn)):
			if(self.validate_pawn(move)):
				return True
			else:
				raise InvalidMoveError 
		if (isinstance(active_piece, King) and y_move_distance == 2):
			if(self.validate_castling(move)):
				return True
			else:
				raise InvalidMoveError 

		if(not active_piece):
			raise NoPieceHereError

		if(not active_piece.isValidMove(move)): 
			raise InvalidMoveError 

		#if(dest_piece):
			#if(dest_piece.color == self.turn):
				#raise InvalidMoveError 

		# if (check path btw active and dest (call piece method)

		return True

	def perform_move(self,move):
		self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = None, self.board_state[move.x][move.y]
		self.turn = "White" if self.turn == "Black" else "Black"
		self.turn_number += 1
		print(f"turn number:{self.turn_number}")
		return


	def perform_castling(self,move):
		castle_x = move.x
		castle_y = 7 if move.y1 == 6 else 0
		castle_final_y = 5 if castle_y > 4 else 3
		castle_piece = self.board_state[move.x1][castle_y]
		self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = None, self.board_state[move.x][move.y]
		self.board_state[castle_x][castle_y], self.board_state[castle_x][castle_final_y] = None, self.board_state[castle_x][castle_y]
		self.turn = "White" if self.turn == "Black" else "Black"
		self.turn_number += 1
		print(f"turn number:{self.turn_number}")
		return

	def print_board(self):
		r = [[x.as_string() if x else "empty" for x in self.board_state[i]] for i in range(8)]
		for i in range(8):
			print(r[i])

class Move:
	def __init__(self,x,y,x1,y1):
		self.x = x
		self.y = y
		self.x1 = x1
		self.y1 = y1
		self.type = None
	def __str__(self):
		return f'({self.x},{self.y}) -> ({self.x1},{self.y1})'


class Error(Exception):
	"""Base class for other exceptions"""
	pass

class InvalidInputError(Error):
	"""Raised when the user provides invalid input"""
	pass

class InvalidMoveError(Error):
	"""Raised when the selected move is invalid"""
	pass

class NoPieceHereError(Error):
	"""Raised when no piece exists at initial coord"""
	pass	

class Game:
	def __init__(self):
		self.board = Board()
		self.move_history = []

	def take_input(self):
		cmd = input("Enter move: x,y,x1,y1:")
		c = cmd.split(",")
		if (len(c) != 4):
			raise InvalidInputError
		return [int(x) for x in c]

	def game_loop(self):
		while(True):
			try:
				g.board.print_board()
				c = self.take_input()
				m = Move(c[0],c[1],c[2],c[3])
				self.move(m)
				#self.move(c[0],c[1],c[2],c[3])
			except InvalidInputError:
				print("Invalid input! Move must be inputted in correct format")
			except InvalidMoveError:
				print("Move is invalid. Learn how to play chess.")

	def move(self,move):
		try:
			move.type = self.board.get_move_type(move)
			if(self.board.validate_move(move)):
				print("performing move....")
				if (move.type == "Castling"):
					print("\n\n\n\n WE CASTLING BOY \n\n\n")
					self.board.perform_castling(move)
				elif(move.type == "Promotion"):
					pass
				elif(move.type == "En-passant"):
					pass
				else:
					self.board.perform_move(move)
				self.move_history.append(move)
		except InvalidMoveError:
			print(move)
			print("Move is invalid. Learn how to play chess.")
		except NoPieceHereError:
			print(move)
			print(f"No piece located at {move.x},{move.y}")

if (__name__ == "__main__"):
	g = Game()
	g.game_loop()

