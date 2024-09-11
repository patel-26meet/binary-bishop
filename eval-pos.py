from eval import Valuation
import chess
from search import Search
from zobrist_hash import ZobristHash

class CurrentPos:
    def __init__(self):
        self.valuation = Valuation()
        self.search = Search()

    def score(self, board):
        evaluation = self.valuation.evaluate(board)
        print(evaluation)

    def best_move_print(self, board):
        depth = 7
        best_move = self.search.best_move(board, depth)
        print(best_move)


# Create an instance of CurrentPos
#urrent_pos = CurrentPos()

# Call the score method on the instance
#current_pos.score(board)
#current_pos.best_move_print(board)


#check castling and en passant in hashing
board = chess.Board('r1bqk2r/1ppp1ppp/2n2n2/2b1p3/pPB1P3/P1P2N2/3P1PPP/RNBQ1RK1 b kq b3 0 7')

zobrist = ZobristHash()
hash = zobrist.compute_initial_hash(board)
print("Initial hash:", hash)

move = chess.Move.from_uci('a4b3')

updated_hash = zobrist.update_hash(hash, move, board)
print("Updated hash before move:", updated_hash)

board.push(move)

new_hash = zobrist.compute_initial_hash(board)
print("New hash after move:", new_hash)
print("Hashes match:", updated_hash == new_hash)

#965 something?
#14834408390181040922 .. after white castles --black to move
#before white castles 3477825247043057720 --white to move

#castling with update hash function - 