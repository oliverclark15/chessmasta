import itertools
from piece import Rook, Knight, Bishop, King, Queen, Pawn, PieceFactory
class Board:
	def __init__(self):
		pf = PieceFactory()
		self.turn = "White"
		self.board_state = [[pf.new_piece(x,y) for y in range(8)] for x in range(8)]
		self.turn_number = 1

	def get_king_moves(self,kcolor):
		kloc = self.find_king(kcolor)
		kx = kloc[0]
		ky = kloc[1]
		xl = []
		yl = []
		xl.append(kx)
		yl.append(ky)
		print(kloc)
		if (kx < 7):
			xl.append(kx+1)
		if (kx > 0):
			xl.append(kx-1)
		if (ky < 7):
			yl.append(ky+1)
		if (ky > 0):
			yl.append(ky-1)
		print(list(itertools.product(xl,yl)))
		return list(itertools.product(xl,yl))

	def find_king(self,kcolor):
		for x in range(8):
			for y in range(8):
				bs = self.board_state[x][y]
				if(not bs):
					continue
				if(isinstance(bs,King) and bs.color == kcolor):
					return (x,y)

	def is_in_check(self,kcolor):
		kloc = self.find_king(kcolor)
		for x in range(8):
			for y in range(8):
				bs = self.board_state[x][y]
				if(not bs):
					continue
				if(bs.color == kcolor):
					continue
				attack_move = Move(x,y,kloc[0],kloc[1])
				if(bs.isValidMove(attack_move)):
					for p in self.get_path(attack_move):
						if (p):
							continue
					return True
		return False

	def try_escape(self,move,kcolor):
		saved_board = self.board_state
		tmp = self.board_state[move.x1][move.y1]
		if(not tmp or tmp.color != kcolor):
			self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = None, self.board_state[move.x][move.y]
			in_check = self.is_in_check(kcolor)
			self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = self.board_state[move.x1][move.y1], tmp
			return (not in_check)
		else:
			return False

	
	def is_in_checkmate(self,kcolor):
		kloc = self.find_king(kcolor)
		kdestinations = self.get_king_moves(kcolor)
		print(kloc)
		print(kdestinations)
		kmoves = [Move(kloc[0],kloc[1],kdest[0],kdest[1]) for kdest in kdestinations]
		for km in kmoves:
			print(f"Trying {km}")
			if(self.try_escape(km,kcolor)):
				print("escape found")
				return False
		return True
			
	def get_path(self, move):
		x_curr = move.x
		y_curr = move.y
		x_end = move.x1
		y_end = move.y1
		results = []
		while (x_curr != x_end or y_curr != y_end):
			if (not y_curr == y_end):
				y_curr = y_curr + 1 if (y_curr < y_end) else y_curr - 1
			if (not x_curr == x_end):
				x_curr = x_curr + 1 if (x_curr < x_end) else x_curr - 1
			results.append((x_curr,y_curr))
		return results[:-1]


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
				if (self.board.is_in_check("White")):
					if (self.board.is_in_checkmate("White")):
						print("White is in checkmate, Black wins!")
						break
					else:
						print("White is in check")
				if (self.board.is_in_check("Black")):
					if (self.board.is_in_checkmate("Black")):
						print("Black is in checkmate, white wins!")
						break
					else:
						print("Black is in check")
				#print(f"White: {self.board.board_state.is_in_check("White")}   Black: {self.board.board_state.is_in_check("Black")}")
				#self.move(c[0],c[1],c[2],c[3])
			except InvalidInputError:
				print("Invalid input! Move must be inputted in correct format")
			except InvalidMoveError:
				print("Move is invalid. Learn how to play chess.")
		return

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
	'''
	mm = Move(0,0,7,0)
	mm1 = Move(0,0,0,7)
	mm2 = Move(0,0,7,7)
	mm3 = Move(5,5,0,0)
	mm4 = Move(2,3,4,5)
	print("0,0")
	print(list(get_king_moves(0,0)))
	print("7,7")
	print(list(get_king_moves(7,7)))
	print("0,7")
	print(list(get_king_moves(0,7)))
	print("7,0")
	print(list(get_king_moves(7,0)))
	print("0,1")
	print(list(get_king_moves(0,1)))
	print("1,0")
	print(list(get_king_moves(1,0)))
	print("3,3")
	print(list(get_king_moves(3,3)))
	print("7,2")
	print(list(get_king_moves(7,2)))
		'''

	g = Game()
	g.game_loop()

