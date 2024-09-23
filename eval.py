import logging
import chess
import numpy

p_mg = [0,   0,   0,   0,   0,   0,  0,   0,
       98, 134,  61,  95,  68, 126, 34, -11,
       -6,   7,  26,  31,  65,  56, 25, -20,
      -14,  13,   6,  21,  23,  12, 17, -23,
      -27,  -2,  -5,  12,  17,   6, 10, -25,
      -26,  -4,  -4, -10,   3,   3, 33, -12,
      -35,  -1, -20, -23, -15,  24, 38, -22,
        0,   0,   0,   0,   0,   0,  0,   0,]

p_eg = [0,   0,   0,   0,   0,   0,   0,   0,
      178, 173, 158, 134, 147, 132, 165, 187,
       94, 100,  85,  67,  56,  53,  82,  84,
       32,  24,  13,   5,  -2,   4,  17,  17,
       13,   9,  -3,  -7,  -7,  -8,   3,  -1,
        4,   7,  -6,   1,   0,  -5,  -1,  -8,
       13,   8,   8,  10,  13,   0,   2,  -7,
        0,   0,   0,   0,   0,   0,   0,   0,]

n_mg = [-167, -89, -34, -49,  61, -97, -15, -107,
         -73, -41,  72,  36,  23,  62,   7,  -17,
         -47,  60,  37,  65,  84, 129,  73,   44,
          -9,  17,  19,  53,  37,  69,  18,   22,
         -13,   4,  16,  13,  28,  19,  21,   -8,
         -23,  -9,  12,  10,  19,  17,  25,  -16,
         -29, -53, -12,  -3,  -1,  18, -14,  -19,
        -105, -21, -58, -33, -17, -28, -19,  -23,]

n_eg = [-58, -38, -13, -28, -31, -27, -63, -99,
        -25,  -8, -25,  -2,  -9, -25, -24, -52,
        -24, -20,  10,   9,  -1,  -9, -19, -41,
        -17,   3,  22,  22,  22,  11,   8, -18,
        -18,  -6,  16,  25,  16,  17,   4, -18,
        -23,  -3,  -1,  15,  10,  -3, -20, -22,
        -42, -20, -10,  -5,  -2, -20, -23, -44,
        -29, -51, -23, -15, -22, -18, -50, -64,]

b_mg = [-29,   4, -82, -37, -25, -42,   7,  -8,
        -26,  16, -18, -13,  30,  59,  18, -47,
        -16,  37,  43,  40,  35,  50,  37,  -2,
         -4,   5,  19,  50,  37,  37,   7,  -2,
         -6,  13,  13,  26,  34,  12,  10,   4,
          0,  15,  15,  15,  14,  27,  18,  10,
          4,  15,  16,   0,   7,  21,  33,   1,
        -33,  -3, -14, -21, -13, -12, -39, -21,]

b_eg = [-14, -21, -11,  -8, -7,  -9, -17, -24,
         -8,  -4,   7, -12, -3, -13,  -4, -14,
          2,  -8,   0,  -1, -2,   6,   0,   4,
         -3,   9,  12,   9, 14,  10,   3,   2,
         -6,   3,  13,  19,  7,  10,  -3,  -9,
        -12,  -3,   8,  10, 13,   3,  -7, -15,
        -14, -18,  -7,  -1,  4,  -9, -15, -27,
        -23,  -9, -23,  -5, -9, -16,  -5, -17,]

q_mg = [-28,   0,  29,  12,  59,  44,  43,  45,
        -24, -39,  -5,   1, -16,  57,  28,  54,
        -13, -17,   7,   8,  29,  56,  47,  57,
        -27, -27, -16, -16,  -1,  17,  -2,   1,
         -9, -26,  -9, -10,  -2,  -4,   3,  -3,
        -14,   2, -11,  -2,  -5,   2,  14,   5,
        -35,  -8,  11,   2,   8,  15,  -3,   1,
         -1, -18,  -9,  10, -15, -25, -31, -50,]

q_eg = [-9,  22,  22,  27,  27,  19,  10,  20,
       -17,  20,  32,  41,  58,  25,  30,   0,
       -20,   6,   9,  49,  47,  35,  19,   9,
         3,  22,  24,  45,  57,  40,  57,  36,
       -18,  28,  19,  47,  31,  34,  39,  23,
       -16, -27,  15,   6,   9,  17,  10,   5,
       -22, -23, -30, -16, -16, -23, -36, -32,
       -33, -28, -22, -43,  -5, -32, -20, -41,]

r_mg = [32,  42,  32,  51, 63,  9,  31,  43,
         27,  32,  58,  62, 80, 67,  26,  44,
         -5,  19,  26,  36, 17, 45,  61,  16,
        -24, -11,   7,  26, 24, 35,  -8, -20,
        -36, -26, -12,  -1,  9, -7,   6, -23,
        -45, -25, -16, -17,  3,  0,  -5, -33,
        -44, -16, -20,  -9, -1, 11,  -6, -71,
        -19, -13,   1,  17, 16,  7, -37, -26,]

r_eg = [13, 10, 18, 15, 12,  12,   8,   5,
        11, 13, 13, 11, -3,   3,   8,   3,
         7,  7,  7,  5,  4,  -3,  -5,  -3,
         4,  3, 13,  1,  2,   1,  -1,   2,
         3,  5,  8,  4, -5,  -6,  -8, -11,
        -4,  0, -5, -1, -7, -12,  -8, -16,
        -6, -6,  0,  2, -9,  -9, -11,  -3,
        -9,  2,  3, -1, -5, -13,   4, -20,]

k_mg = [-65,  23,  16, -15, -56, -34,   2,  13,
         29,  -1, -20,  -7,  -8,  -4, -38, -29,
         -9,  24,   2, -16, -20,   6,  22, -22,
        -17, -20, -12, -27, -30, -25, -14, -36,
        -49,  -1, -27, -39, -46, -44, -33, -51,
        -14, -14, -22, -46, -44, -30, -15, -27,
          1,   7,  -8, -64, -43, -16,   9,   8,
        -15,  36,  12, -54,   8, -28,  24,  14,]

k_eg = [-74, -35, -18, -18, -11,  15,   4, -17,
        -12,  17,  14,  17,  17,  38,  23,  11,
         10,  17,  23,  15,  20,  45,  44,  13,
         -8,  22,  24,  27,  26,  33,  26,   3,
        -18,  -4,  21,  24,  27,  23,   9, -11,
        -19,  -3,  11,  21,  23,  16,   7,  -9,
        -27, -11,   4,  13,  14,   4,  -5, -17,
        -53, -34, -21, -11, -28, -14, -24, -43]

game_phase_table = [0,0,0,1,1,1,1,2,2,4,4,0,0]

mg_table = [
    None,
    p_mg, 
    k_mg, 
    b_mg, 
    r_mg, 
    q_mg,
    k_mg, 
]

eg_table = [
    None,
    p_eg, 
    k_eg, 
    b_eg, 
    r_eg, 
    q_eg,
    k_eg, 
]

#Midgame mobility values of minor adn major pieces; based on number of squares controlling!
mobility_mg = [
    [-62,-53,-12,-4,3,13,22,28,33],  #Knight
    [-48,-20,16,26,38,51,55,63,63,68,81,81,91,98],  #Bishop
    [-58,-27,-15,-10,-5,-2,9,16,30,29,32,38,46,48,58],  #Rook
    [-39,-21,3,3,14,22,28,41,43,48,56,60,60,66,67,70,71,73,79,88,88,99,102,102,106,109,113,116]  #Queen
]

#Endgame mobility values of major and minor pieces 
mobility_eg = [
    [-81,-56,-30,-14,8,15,23,27,33],  #Knight
    [-59,-23,-3,13,24,42,54,57,65,73,78,86,88,97],  #Bishop
    [-76,-18,28,55,69,82,112,118,132,142,155,165,166,169,171],  #Rook
    [-36,-15,8,18,34,54,61,73,79,92,94,104,113,120,123,126,133,136,140,143,148,166,170,175,184,191,206,212]  #Queen
]

class Valuation:
    def __init__(self):
        logging.debug("Initializing Valuation class")
        self.mg_piece_values = {
            chess.PAWN: 82,
            chess.KNIGHT: 337,
            chess.BISHOP: 365,
            chess.ROOK: 477,
            chess.QUEEN: 1025,
            chess.KING: 0
        }
        self.eg_piece_values = {
            chess.PAWN: 94,
            chess.KNIGHT: 281,
            chess.BISHOP: 297,
            chess.ROOK: 512,
            chess.QUEEN: 936,
            chess.KING: 0
        }

    def evaluate(self, board):
        try:
            if board.is_checkmate():
                return -9999 if board.turn else 9999
            if board.is_stalemate() or board.is_insufficient_material():
                return 0

            evaluation = 0
            game_phase = 0
            

            for square in chess.SQUARES:
                piece = board.piece_at(square)
            
                if piece is not None:
                    game_phase += game_phase_table[piece.piece_type]

                    mg_piece_value = self.mg_piece_values[piece.piece_type]
                    eg_piece_value = self.eg_piece_values[piece.piece_type]
                    mg_pos_value = mg_table[piece.piece_type][square if piece.color == chess.WHITE else chess.square_mirror(square)]
                    eg_pos_value = eg_table[piece.piece_type][square if piece.color == chess.WHITE else chess.square_mirror(square)]
                    mg_value = mg_pos_value + mg_piece_value
                    eg_value = eg_pos_value + eg_piece_value

                    piece_eval = mg_value * (24 - game_phase) + eg_value * game_phase
                    evaluation += piece_eval if piece.color == chess.WHITE else -piece_eval

            return evaluation // 24
        except Exception as e:
            logging.error(f"Error in evaluate method: {str(e)}")
            raise

    def get_game_phase(self, board):
        game_phase = 0

        for square in chess.SQUARES:
                piece = board.piece_at(square)
            
                if piece is not None:
                    game_phase += game_phase_table[piece.piece_type]
            
        return game_phase
    


class SpecificValuation(Valuation):
    def __init__(self):
        super().__init__()
        
    def evaluate(self, board):
        evaluation =  super().evaluate(board)

        mobility_score = self.evaluate_mobility(board)
        space_score = self.evaluate_space(board)

        evaluation += (mobility_score + space_score)

        return evaluation 
    
    def evaluate_mobility(self, board):
        mobility_score = 0
        game_phase = self.get_game_phase(board)

        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN ]:
                mobility = self.get_piece_mobility(board, color, piece_type)
                mg_score = mobility_mg[piece_type - 2][mobility]
                eg_score = mobility_eg[piece_type - 2][mobility]
                score = (mg_score * (24 - game_phase) + eg_score * game_phase) // 24
                mobility_score += score if color == chess.WHITE else -score

        return mobility_score
    
    def evaluate_space(self, board):
        space_score = 0
        game_phase = self.get_game_phase(board)

        if game_phase >= 12:
            return 0
        
        for color in [chess.WHITE, chess.BLACK]:
            space = self.get_space_score(board, color)
            space_score += space if color == chess.WHITE else -space

        return space_score
    
    def get_space_score(self, board, color):
        space = 0
        behind_pawns = 0
        center_files = [2, 3, 4, 5]

        pawn_ranks = [1, 2, 3] if color == chess.WHITE else [6, 5, 4]

        for file in center_files:
            for rank in pawn_ranks:
                square = chess.square(file, rank)
                if not board.piece_at(square):
                    space += 1
                    if board.piece_at(square + (8 if color == chess.WHITE else -8)) == chess.Piece(chess.PAWN, color):
                        behind_pawns += 1

        return (space + behind_pawns) * (len(board.pieces(chess.PAWN, color)) - 2) // 4
    
    def get_piece_mobility(self, board, color, piece_type):
        mobility = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == color and piece.piece_type == piece_type:
                mobility += len(list(board.attacks(square)))
        return min(mobility, len(mobility_mg[piece_type - 2]) - 1)


