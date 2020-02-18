from chess import *



class Agent:

    def __init__(self,max_depth):
        self.max_depth = max_depth

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
        print(f"Iterating over {len(possible_moves)} possible moves @ depth {current_depth}")
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
        print(f"Concluded iterating over {len(possible_moves)} possible moves")
        print(best_score)
        return best_score


a = Agent(4)
b = Board()
a.minimax(0,b)
