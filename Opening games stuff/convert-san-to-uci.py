import chess
import re

def convert_to_uci(game_string):
    board = chess.Board()
    # Use regex to separate moves from the result
    match = re.match(r'^(.*?)\s*(?:1-0|0-1|1/2-1/2|\\*)\s*$', game_string)
    if match:
        moves = match.group(1).split()
    else:
        moves = game_string.split()
    
    uci_moves = []

    for move in moves:
        try:
            san_move = board.parse_san(move)
            uci_move = san_move.uci()
            uci_moves.append(uci_move)
            board.push(san_move)
        except ValueError:
            print(f"Skipping non-move: {move}")
    
    return ' '.join(uci_moves)

# File processing
input_file = "Games.txt"
output_file = "output_games_uci.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for i, line in enumerate(infile, 1):
        game = line.strip()
        uci_game = convert_to_uci(game)
        if uci_game:
            outfile.write(uci_game + '\n')
        else:
            print(f"Failed to convert game on line {i}")