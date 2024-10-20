import logging
from eval import SpecificValuation
from log_config import setup_logging
from zobrist_hash import ZobristHash
from transposition_table import TranspositionTable

logger = setup_logging()

class Search:
    def __init__(self):
        logging.debug("Initializing search class")
        self.valuation = SpecificValuation()
        self.zobrist = ZobristHash()
        self.tt = TranspositionTable(524288)  # Using the size you specified

    def best_move(self, board, depth, time):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        legal_moves = list(board.legal_moves)

        zobrist_key = self.zobrist.compute_initial_hash(board)
        logging.debug(f"Initial zobrist key for the board: {zobrist_key}")

        tt_entry = self.tt.lookup(zobrist_key)
        if tt_entry and tt_entry['depth_searched'] >= depth:
            logging.debug(f"TT hit: {tt_entry}")
            return tt_entry['best_move']

        if board.turn:  # White to move
            best_score = float('-inf')
            for move in legal_moves:
                logging.debug(f"Starting evaluation of move: {move.uci()}")
                try:
                    new_board = board.copy()
                    new_board.push(move)
                    new_key = self.zobrist.update_hash(zobrist_key, move, board)
                    score = self.alphaBetaMin(new_board, alpha, beta, depth - 1, new_key)
                    new_board.pop()
                    if score > best_score:
                        best_score = score
                        best_move = move
                    alpha = max(alpha, best_score)
                except Exception as e:
                    logging.error(f"Error evaluating move {move.uci()}: {str(e)}")
        else:  # Black to move
            best_score = float('inf')
            for move in legal_moves:
                logging.debug(f"Starting evaluation of move: {move.uci()}")
                try:
                    new_board = board.copy()
                    new_board.push(move)
                    new_key = self.zobrist.update_hash(zobrist_key, move, board)
                    score = self.alphaBetaMax(new_board, alpha, beta, depth - 1, new_key)
                    new_board.pop()
                    if score < best_score:
                        best_score = score
                        best_move = move
                    beta = min(beta, best_score)
                except Exception as e:
                    logging.error(f"Error evaluating move {move.uci()}: {str(e)}")

        # Store the result in the transposition table
        self.tt.store(zobrist_key, depth, best_score, 'PV' if best_move else 'ALL', best_move)

        logging.debug(f"Best move found: {best_move.uci() if best_move else 'None'}")
        return best_move

    def alphaBetaMax(self, board, alpha, beta, depthleft, zobrist_key):
        logging.debug("entering max")

        # Transposition table lookup
        tt_entry = self.tt.lookup(zobrist_key)
        if tt_entry and tt_entry['depth_searched'] >= depthleft:
            if tt_entry['flag'] == 'EXACT':
                return tt_entry['score']
            elif tt_entry['flag'] == 'LOWERBOUND':
                alpha = max(alpha, tt_entry['score'])
            elif tt_entry['flag'] == 'UPPERBOUND':
                beta = min(beta, tt_entry['score'])
            if alpha >= beta:
                return tt_entry['score']

        if depthleft == 0 or board.is_game_over():
            return self.quiescence_search(board, alpha, beta, zobrist_key, 4)
        
        bestValue = float('-inf')
        best_move = None
        
        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            new_key = self.zobrist.update_hash(zobrist_key, move, board)
            score = self.alphaBetaMin(new_board, alpha, beta, depthleft - 1, new_key)
            if score > bestValue:
                bestValue = score
                best_move = move
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break

        # Store the result in the transposition table
        if bestValue <= alpha:
            flag = 'UPPERBOUND'
        elif bestValue >= beta:
            flag = 'LOWERBOUND'
        else:
            flag = 'EXACT'
        self.tt.store(zobrist_key, depthleft, bestValue, flag, best_move)

        return bestValue

    def alphaBetaMin(self, board, alpha, beta, depthleft, zobrist_key):
        logging.debug("entering min")

        # Transposition table lookup
        tt_entry = self.tt.lookup(zobrist_key)
        if tt_entry and tt_entry['depth_searched'] >= depthleft:
            if tt_entry['flag'] == 'EXACT':
                return tt_entry['score']
            elif tt_entry['flag'] == 'LOWERBOUND':
                alpha = max(alpha, tt_entry['score'])
            elif tt_entry['flag'] == 'UPPERBOUND':
                beta = min(beta, tt_entry['score'])
            if alpha >= beta:
                return tt_entry['score']
            
        if depthleft == 0 or board.is_game_over():
            return self.quiescence_search(board, alpha, beta, zobrist_key, 3)

        bestValue = float('inf')
        best_move = None

        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            new_key = self.zobrist.update_hash(zobrist_key, move, board)
            score = self.alphaBetaMax(new_board, alpha, beta, depthleft - 1, new_key)
            if score < bestValue:
                bestValue = score
                best_move = move
            beta = min(beta, bestValue)
            if beta <= alpha:
                break

        # Store the result in the transposition table
        if bestValue <= alpha:
            flag = 'UPPERBOUND'
        elif bestValue >= beta:
            flag = 'LOWERBOUND'
        else:
            flag = 'EXACT'
        self.tt.store(zobrist_key, depthleft, bestValue, flag, best_move)

        return bestValue
    
    def quiescence_search(self, board, alpha, beta, zobrist_key, depth):
        if depth <= 0:
            return self.valuation.evaluate(board)

        stand_pat = self.valuation.evaluate(board)

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if self.is_capture_or_promotion(board, move):
                new_board = board.copy()
                new_board.push(move)
                new_key = self.zobrist.update_hash(zobrist_key, move, board)
                score = -self.quiescence_search(new_board, -beta, -alpha, new_key, depth - 1)

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    def is_capture_or_promotion(self, board, move):
        return board.is_capture(move) or move.promotion is not None

    def is_check_or_promotion(self, board, move):
        new_board = board.copy()
        new_board.push(move)
        return new_board.is_check() or move.promotion is not None