class Rook:
	def __init__(self,color):
		self.color = color
		self.has_moved = False

	def get_inbetween(self,move):
		return []

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
	def get_inbetween(self,move):
		return []
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
	def get_inbetween(self,move):
		return []
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
	def get_inbetween(self,move):
		return []
	def isValidMove(self,move):
		if (move.x == move.x1 and move.y != move.y1):
			return True
		elif (move.x != move.x1 and move.y == move.y1):
			return True
		elif (abs(move.x-move.x1) == abs(move.y-move.y1)):
			return True
		else:
			return False
	def as_string(self):
		return self.color+"Q"

class King:
	def __init__(self,color):
		self.color = color
		self.has_moved = False
	def get_inbetween(self,move):
		return []
	def isValidMove(self,move):
		xmd = abs(move.x-move.x1)
		ymd = abs(move.y-move.y1)
		if (ymd == 2 and xmd == 0):
			return True
		elif (xmd > 1 or ymd > 1):
			return False
		else:
			return True
	def as_string(self):
		return self.color+"K"

class Pawn:
	def __init__(self,color):
		self.color = color
		self.first_move = True
	def get_inbetween(self,move):
		return []
	def isValidMove(self,move):
		#print("hi")
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

if (__name__ == "__main__"):
	print("probably dont run this")