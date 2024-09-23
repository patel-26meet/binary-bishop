import chess
import logging
import hashlib

class ZobristHash:
    def __init__(self):
        self.zobrist_table = {}
        self.zobrist_black_to_move = 0
        self.zobrist_castling_rights = []
        self.zobrist_en_passant = []
        self.initialize_zobrist_table()

    def initialize_zobrist_table(self) -> None:
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        
        # Use a seed for consistency
        seed = "terimakapati" 
        
        #consistent 64-bit numbers for each piece on each square
        for piece in pieces:
            for square in range(64):
                key = f"{piece}_{square}_{seed}"
                self.zobrist_table[(piece, square)] = int(hashlib.sha256(key.encode()).hexdigest()[:16], 16)

        #player turn
        self.zobrist_black_to_move = int(hashlib.sha256(f"black_to_move_{seed}".encode()).hexdigest()[:16], 16)

        #Castling rights
        self.zobrist_castling_rights = [
            int(hashlib.sha256(f"castling_{i}_{seed}".encode()).hexdigest()[:16], 16)
            for i in range(4)
        ]

        #en passant files
        self.zobrist_en_passant = [
            int(hashlib.sha256(f"en_passant_{i}_{seed}".encode()).hexdigest()[:16], 16)
            for i in range(8)
        ]

    def compute_initial_hash(self, board: chess.Board) -> int:
        hash_value = 0

        # Hash in all pieces on the board
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                hash_value ^= self.zobrist_table[(piece.symbol(), square)]

        # Hashing castling rights
        if board.has_kingside_castling_rights(chess.WHITE):
            hash_value ^= self.zobrist_castling_rights[0]
        if board.has_queenside_castling_rights(chess.WHITE):
            hash_value ^= self.zobrist_castling_rights[1]
        if board.has_kingside_castling_rights(chess.BLACK):
            hash_value ^= self.zobrist_castling_rights[2]
        if board.has_queenside_castling_rights(chess.BLACK):
            hash_value ^= self.zobrist_castling_rights[3]

        # Hash in en passant square if available
        ep_square = board.ep_square
        if ep_square is not None:
            hash_value ^= self.zobrist_en_passant[ep_square % 8]
        
        # Hash in side to move
        if board.turn == chess.BLACK:
            hash_value ^= self.zobrist_black_to_move

        return hash_value

    def update_hash(self, hash_value, move, board):
        from_square = move.from_square
        to_square = move.to_square
        piece = board.piece_at(from_square)
        
        if piece is None:
            raise ValueError(f"No piece found at square {from_square}")
        
        piece_symbol = piece.symbol()
        
        #remove piece from from_square
        hash_value ^= self.zobrist_table[(piece_symbol, from_square)]
        
        #captures
        captured_piece = board.piece_at(to_square)
        if captured_piece:
            hash_value ^= self.zobrist_table[(captured_piece.symbol(), to_square)]
        
        #move piece to to_square
        hash_value ^= self.zobrist_table[(piece_symbol, to_square)]
        
        #pawn promotion
        if move.promotion:
            promoted_piece_symbol = chess.PIECE_SYMBOLS[move.promotion]
            hash_value ^= self.zobrist_table[(promoted_piece_symbol, to_square)] #add piece
            hash_value ^= self.zobrist_table[(piece_symbol, to_square)]  #remove pawn
        
        #en passant
        old_ep_square = board.ep_square
        if old_ep_square:
            hash_value ^= self.zobrist_en_passant[old_ep_square % 8]
        
        if board.is_en_passant(move):
            ep_pawn_square = to_square + (-8 if board.turn == chess.WHITE else 8)
            ep_pawn = board.piece_at(ep_pawn_square)
            if ep_pawn:
                hash_value ^= self.zobrist_table[(ep_pawn.symbol(), ep_pawn_square)]
        
        # Update en passant square
        if piece.piece_type == chess.PAWN and abs(to_square - from_square) == 16:
            new_ep_square = (from_square + to_square) // 2
            hash_value ^= self.zobrist_en_passant[new_ep_square % 8]
        
        #castling
        if board.is_castling(move):
            if to_square == chess.G1:
                rook_from, rook_to = chess.H1, chess.F1
            elif to_square == chess.C1:
                rook_from, rook_to = chess.A1, chess.D1
            elif to_square == chess.G8:
                rook_from, rook_to = chess.H8, chess.F8
            elif to_square == chess.C8:
                rook_from, rook_to = chess.A8, chess.D8
            
            rook = board.piece_at(rook_from)
            if rook:
                hash_value ^= self.zobrist_table[(rook.symbol(), rook_from)]
                hash_value ^= self.zobrist_table[(rook.symbol(), rook_to)]
        
        # Update castling rights
        old_castling_rights = board.castling_rights
        new_castling_rights = old_castling_rights
        
        if piece.piece_type == chess.KING:
            if board.turn == chess.WHITE:
                new_castling_rights &= ~(chess.BB_H1 | chess.BB_A1)
            else:
                new_castling_rights &= ~(chess.BB_H8 | chess.BB_A8)
        
        # Rook moves remove the corresponding castling right
        elif piece.piece_type == chess.ROOK:
            if from_square == chess.H1:
                new_castling_rights &= ~chess.BB_H1
            elif from_square == chess.A1:
                new_castling_rights &= ~chess.BB_A1
            elif from_square == chess.H8:
                new_castling_rights &= ~chess.BB_H8
            elif from_square == chess.A8:
                new_castling_rights &= ~chess.BB_A8
        
        # Rook captures remove the corresponding castling right
        if captured_piece and captured_piece.piece_type == chess.ROOK:
            if to_square == chess.H1:
                new_castling_rights &= ~chess.BB_H1
            elif to_square == chess.A1:
                new_castling_rights &= ~chess.BB_A1
            elif to_square == chess.H8:
                new_castling_rights &= ~chess.BB_H8
            elif to_square == chess.A8:
                new_castling_rights &= ~chess.BB_A8
        
        # Update the hash if castling rights have changed
        if old_castling_rights != new_castling_rights:
            for i, mask in enumerate([chess.BB_H1, chess.BB_A1, chess.BB_H8, chess.BB_A8]):
                if bool(old_castling_rights & mask) != bool(new_castling_rights & mask):
                    hash_value ^= self.zobrist_castling_rights[i]
        
        
        #side to move change
        hash_value ^= self.zobrist_black_to_move
        
        return hash_value