import chess
import chess.pgn
import os

def pgn_to_uci(pgn_files, uci_file):
    with open(uci_file, 'w') as uci:
        for pgn_file in pgn_files:
            with open(pgn_file) as pgn:
                while True:
                    game = chess.pgn.read_game(pgn)
                    if game is None:
                        break
                    
                    board = game.board()
                    moves = []
                    for move in game.mainline_moves():
                        moves.append(move.uci())
                    
                    uci.write(' '.join(moves) + '\n')

# Usage
pgn_directory = 'pgn files'
pgn_files = [os.path.join(pgn_directory, f) for f in os.listdir(pgn_directory) if f.endswith('.pgn')]
pgn_to_uci(pgn_files, 'output2.uci')