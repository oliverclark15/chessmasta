import itertools
import copy 
if (__name__ == "__main__"):
    from piece import Rook, Knight, Bishop, King, Queen, Pawn, PieceFactory
else:
    from piece import Rook, Knight, Bishop, King, Queen, Pawn, PieceFactory

class Board:
    def __init__(self, turn_number=1, turn="White", board_state=None):
        self.turn = turn
        self.turn_number = turn_number
        if (board_state):
            self.board_state = board_state
        else:
            pf = PieceFactory()
            self.board_state = [[pf.new_piece(x, y) for y in range(8)] for x in range(8)]
    
    def find_pieces(self,color):
        piece_locations = []
        for x in range(8):
            for y in range(8):
                p = self.board_state[x][y]
                if(not p):
                    continue
                if(p.color == color):
                    piece_locations.append((x,y))
        return piece_locations

    
    def get_all_moves(self,color):
        piece_locations = self.find_pieces(color)
        moves = []
        for piece_location in piece_locations:
            px,py = piece_location[0], piece_location[1]
            for x in range(8):
                for y in range(8):
                    candidate_move = Move(px,py,x,y)
                    candidate_move.type = self.get_move_type(candidate_move)
                    try:
                        if(self.validate_move(candidate_move)):
                            #print(candidate_move)
                            moves.append(candidate_move)
                    except InvalidMoveError:
                        pass
                    except NoPieceHereError:
                        pass
        return moves

    def get_king_moves(self,kcolor):
        kloc = self.find_king(kcolor)
        kx = kloc[0]
        ky = kloc[1]
        xl,yl = [kx],[ky]
        if (kx < 7): xl.append(kx+1)
        if (kx > 0): xl.append(kx-1)
        if (ky < 7): yl.append(ky+1)
        if (ky > 0): yl.append(ky-1)
        return list(itertools.product(xl, yl))

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
        flag = True
        for x in range(8):
            for y in range(8):
                flag = True
                bs = self.board_state[x][y]
                if(not bs):
                    continue
                if(bs.color == kcolor):
                    continue
                if(not kloc):
                    return False
                attack_move = Move(x, y, kloc[0], kloc[1])
                #print(attack_move)
                if(bs.isValidMove(attack_move)):
                    #print(self.get_path(attack_move))
                    for p in self.get_path(attack_move):
                        #print(p)
                        if (self.board_state[p[0]][p[1]]):
                            flag = False
                            break
                    #print(flag)
                    if (flag):
                        #print(f"Attack move {attack_move}")
                        return True
        return False

    def try_escape(self,move,kcolor):
        dest = self.board_state[move.x1][move.y1]
        if(not dest or dest.color != kcolor):
            self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = None, self.board_state[move.x][move.y]
            in_check = self.is_in_check(kcolor)
            self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = self.board_state[move.x1][move.y1], dest
            return (not in_check)
        else:
            return False

    def gameover(self):
        return self.is_in_checkmate("Black") or self.is_in_checkmate("White")

    def is_in_checkmate(self, kcolor):
        if (not self.is_in_check(kcolor)):
            return False
        kloc = self.find_king(kcolor)
        kdestinations = self.get_king_moves(kcolor)
        print(kloc)
        print(kdestinations)
        kmoves = [Move(kloc[0], kloc[1], kdest[0], kdest[1]) for kdest in kdestinations]
        for km in kmoves:
            print(f"Trying {km}")
            if(self.try_escape(km, kcolor)):
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
        dest_piece = self.board_state[move.x1][move.y1]
        if (not active_piece.isValidMove(move)): 
            #print("140")
            return False
        y_move_distance = abs(move.y-move.y1)   # implicitly know xmd == 0, ymd == 0 or 1
        if (y_move_distance == 0):
            if(not self.board_state[move.x1][move.y1]):
                return True
            else:
                #print("146")
                return False
        elif (y_move_distance == 1):
            if(dest_piece and (dest_piece.color == self.turn)):
                return True
            else:
                #print("150")
                return False
        else:
            print("shouldnt happen")

    def validate_castling(self,move):
        active_piece = self.board_state[move.x][move.y]
        castle_y = 7 if move.y1 == 6 else 0
        castle_piece = self.board_state[move.x1][castle_y]
        
        if(not castle_piece):
            return False
        if(not isinstance(castle_piece, Rook)):
            return False
        if (active_piece.has_moved or castle_piece.has_moved):
            return False

        between = self.get_path(move)
        for btw in between:
            piece = self.board_state[btw[0]][btw[1]]
            if(piece):
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
        #total_move_distance = x_move_distance + y_move_distance

        if (isinstance(active_piece,Pawn)):
            if(self.validate_pawn(move)):
                return True
            else:
               return False
               #raise InvalidMoveError 
        if (isinstance(active_piece, King) and y_move_distance == 2):
            if(self.validate_castling(move)):
                return True
            else:
                return False
                #raise InvalidMoveError 

        if(not active_piece):
            return False
            #raise NoPieceHereError

        if(not active_piece.isValidMove(move)): 
            return False
            #raise InvalidMoveError 
        
        if(dest_piece):
            if(dest_piece.color == self.turn):
                return False
                #raise InvalidMoveError 
        '''
        if (check path btw active and dest (call piece method)   
        '''

        if(not isinstance(active_piece, Knight)):
            for sq in self.get_path(move):
                if(self.board_state[sq[0]][sq[1]]):
                    raise InvalidMoveError 
        
        return True

    def perform_move(self,move):
        self.board_state[move.x][move.y], self.board_state[move.x1][move.y1] = None, self.board_state[move.x][move.y]
        self.turn = "White" if self.turn == "Black" else "Black"
        self.turn_number += 1
        print(f"turn number:{self.turn_number}")
        return


    def get_next_board(self,move):
        next_bs = copy.deepcopy(self.board_state)
        next_bs[move.x][move.y], next_bs[move.x1][move.y1] = None, next_bs[move.x][move.y]
        turn = "White" if self.turn == "Black" else "Black"
        return Board(self.turn_number + 1, turn, next_bs)

    def evaluate(self):
        return 10



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

class GameOver(Error):
    """Raised when game over (checkmate)"""
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
        print("----------------------START-----------------------")
        while(True):
            try:
                self.board.print_board()
                c = self.take_input()
                m = Move(c[0],c[1],c[2],c[3])
                self.move(m)
                print("======================================")
                #print(f"White: {self.board.board_state.is_in_check("White")}   Black: {self.board.board_state.is_in_check("Black")}")
                #self.move(c[0],c[1],c[2],c[3])
            except InvalidInputError:
                print("Invalid input! Move must be inputted in correct format")
            except InvalidMoveError:
                print("Move is invalid. Learn how to play chess.")
            except GameOver:
                print("gameover")
                break
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
                if (self.board.is_in_check("White")):
                    print("White is in check")
                    if (self.board.is_in_checkmate("White")):
                        print("White is in checkmate, Black wins!")
                        raise GameOver
                if (self.board.is_in_check("Black")):
                    print("Black is in check")
                    if (self.board.is_in_checkmate("Black")):
                        print("Black is in checkmate, white wins!")
                        raise GameOver
        except InvalidMoveError:
            print(move)
            print("Move is invalid. Learn how to play chess.")
            print("\n\n\n\n\n\n\n")
        except NoPieceHereError:
            print(move)
            print(f"No piece located at {move.x},{move.y}")



if (__name__ == "__main__"):
    g = Game()
    g.game_loop()

