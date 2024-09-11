def limit_to_ten_moves(uci_game):
    moves = uci_game.split()
    return ' '.join(moves[:20])  # 20 half-moves = 10 full moves

input_file = "output.uci"
output_file = "openings3.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        game = line.strip()
        limited_game = limit_to_ten_moves(game)
        outfile.write(limited_game + '\n')

print(f"Conversion complete. 10-move UCI format games saved to {output_file}")