import random
import chess
import logging
from search import Search
from eval import Valuation

logging.basicConfig(level=logging.DEBUG, filename='chess_bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

game_phase_table = [0,0,0,1,1,1,1,2,2,4,4,0,0]

class UCIEngine:
    def __init__(self):
        self.board = chess.Board()
        self.name = "CHESS_BOT"
        self.author = "Tmkp"
        self.search = Search()
        self.eval = Valuation()
        self.opening_book = self.load_opening_book('openings.txt')
        self.move_count = 0
        self.move_overhead = 30

    def uci(self):
        print(f"id name {self.name}")
        print(f"id author {self.author}")
        print("uciok")

    def is_ready(self):
        print("readyok")

    def set_option(self, name, value):
        if name.lower() == "move overhead":
            try:
                self.move_overhead = int(value)
            except ValueError:
                logging.error(f"Invalid value for Move Overhead: {value}")

    def new_game(self):
        self.board.reset()
        self.move_count = 0
        self.move_overhead = 30

    def set_position(self, command):
        words = command.split()
        if len(words) < 2:
            return
        
        if words[1] == "startpos":
            self.board.reset()
            moves_start = 2
        elif words[1] == "fen":
            fen = " ".join(words[2:8])
            self.board.set_fen(fen)
            moves_start = 8
        else:
            return

        self.move_count = 0  # Reset move count when setting a new position
        if len(words) > moves_start and words[moves_start] == "moves":
            for move in words[moves_start+1:]:
                self.board.push_uci(move)
                self.move_count += 1  # Increment move count for each move

        logging.debug(f"Position set. Move count: {self.move_count}")
    
    def load_opening_book(self, filename):
        book = {}
        try:
            with open(filename, 'r') as f:
                for line in f:
                    moves = line.strip().split()
                    current_dict = book
                    for move in moves:
                        if move not in current_dict:
                            current_dict[move] = {}
                        current_dict = current_dict[move]
            logging.debug(f"Successfully loaded opening book from {filename}")
        except Exception as e:
            logging.error(f"Failed to load opening book: {str(e)}")
        return book
    
    def get_book_move(self):
        if self.move_count >= 10:
            logging.debug("Move count >= 10, not using opening book")
            return None
        
        current_dict = self.opening_book
        for move in self.board.move_stack:
            if move.uci() not in current_dict:
                logging.debug(f"Move {move.uci()} not found in opening book")
                return None
            current_dict = current_dict[move.uci()]
        
        if not current_dict:
            logging.debug("No more moves in this opening line")
            return None
        
        book_moves = list(current_dict.keys())
        logging.debug(f"Available book moves: {book_moves}")
        book_move = random.choice(book_moves)
        return chess.Move.from_uci(book_move)
    
    def calculate_time(self, time_params):
        if 'movetime' in time_params:
            return time_params['movetime']

        our_time = time_params['wtime' if self.board.turn else 'btime']
        our_inc = time_params.get('winc' if self.board.turn else 'binc', 0)
        moves_to_go = time_params.get('movestogo', 30)  # Assume 30 moves if not specified

        # Basic time management algorithm
        base_time = our_time / moves_to_go
        inc_time = our_inc * 0.95  # Use 80% of the increment

        allocated_time = base_time + inc_time

        # Ensure we don't use too little time in critical positions
        allocated_time = max(allocated_time, our_time * 0.01)

        return int(allocated_time)


    def go(self, command):
        logging.debug(f"Received go command: {command}")
        logging.debug(f"Current board state: {self.board.fen()}")
        logging.debug(f"Current move count: {self.move_count}")

        params = command.split()[1:]
        time_params = {}
        for i in range(0, len(params), 2):
            if params[i] in ['wtime', 'btime', 'winc', 'binc', 'movetime', 'movestogo']:
                time_params[params[i]] = int(params[i+1])

        allocated_time = self.calculate_time(time_params)

        adjusted_time = max(allocated_time - self.move_overhead, 10)


        book_move = self.get_book_move()
        if book_move and book_move in self.board.legal_moves:
            best_move = book_move
            logging.debug(f"Using book move: {best_move}")
        else:
            logging.debug("No book move available or not a legal move, using search")
            game_phase = self.eval.get_game_phase(self.board)

            depth = 4

            if game_phase < 12:
                depth = 4
            elif game_phase > 12 & game_phase < 18:
                depth = 6
            elif game_phase > 18:
                depth = 7
            
            evaluation = self.eval.evaluate(self.board)

            if abs(evaluation) > 1500:
                depth = 6
            
            best_move = self.search.best_move(self.board, depth, adjusted_time)
            logging.debug(f"Found best move: {best_move}")

        if best_move:
            print(f"bestmove {best_move}")
            self.move_count += 1
            logging.debug(f"Move made. New move count: {self.move_count}")
        else:
            print("bestmove (none)")

    def run(self):
        logging.debug(f"Starting engine loop")
        while True:
            command = input()
            logging.debug(f"Received command: {command}")

            if command == "uci":
                self.uci()
            elif command == "isready":
                self.is_ready()
            elif command == "ucinewgame":
                self.new_game()
            elif command.startswith("setoption"):
                parts = command.split()
                if len(parts) >= 5 and parts[1] == "name" and parts[3] == "value":
                    self.set_option(" ".join(parts[2:-2]), parts[-1])
            elif command.startswith("position"):
                self.set_position(command)
            elif command.startswith("go"):
                self.go(command)
            elif command == "quit":
                break
            logging.debug("Engine loop ended")


if __name__ == "__main__":
    engine = UCIEngine()
    engine.run()