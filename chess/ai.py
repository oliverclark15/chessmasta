from chess import *



class Agent:

    def __init__(self,max_depth):
        self.max_depth = max_depth
        self.best_move = None

    def minimax(self, current_depth, board, alpha=-1000, beta=1000):
        # Recursive base check
        if (current_depth == self.max_depth) or (board.gameover()):
            return board.evaluate()
        # White = MAX
        # Black = MIN
        max_turn = board.turn == "White"
        best_score = float('-inf') if max_turn else float('inf')
        best_move = None
        possible_moves = board.get_all_moves(board.turn)
        #board.print_board()
        #print(f"Iterating over {len(possible_moves)} possible moves @ depth {current_depth}")
        #board.print_board()
        #print(possible_moves)

        for possible_move in possible_moves:
            next_board = board.get_next_board(possible_move) # board.perform needs implementation (return value needed)
            child_score = self.minimax(current_depth + 1, next_board, alpha, beta)
            if max_turn and best_score < child_score:
                best_score = child_score
                best_move = possible_move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            if (not max_turn) and best_score > child_score:
                best_score = child_score
                best_move = possible_move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        #print(f"Concluded iterating over {len(possible_moves)} possible moves")
        #print(best_score)
        print(best_move)
        self.best_move = best_move
        return best_score


a = Agent(4)
b = Board()
b.perform_move(Move(6,3,4,3))
b.perform_move(Move(1,5,3,5))
b.perform_move(Move(7,2,3,6))
b.perform_move(Move(1,7,2,7))
b.perform_move(Move(3,6,4,5))
b.perform_move(Move(1,6,3,6))
b.perform_move(Move(4,5,5,6))
b.perform_move(Move(3,5,4,5))
b.perform_move(Move(6,4,5,4))
b.perform_move(Move(2,7,3,7))
b.perform_move(Move(7,3,3,7))
b.perform_move(Move(7,5,5,3))
b.perform_move(Move(5,3,2,6))
b.perform_move(Move(0,7,2,7))
b.perform_move(Move(7,3,3,7))
b.perform_move(Move(2,7,3,7))
#b.perform_move(Move(0,7,2,7))

print(b.is_in_checkmate("Black"))
b.print_board()
print(a.minimax(0,b))
print(a.best_move)
