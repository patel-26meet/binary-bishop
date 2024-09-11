class TranspositionTable: 
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.hits = 0
        self.stores = 0

    def store(self, zobrist_key, depth_searched, score, flag, best_move):
        self.stores += 1
        index = zobrist_key % self.size
        entry = {
            'key': zobrist_key,
            'depth-searched': depth_searched,  # Note the underscore here
            'score': score,
            'flag': flag,
            'best_move': best_move
        }
        self.table[index] = entry

    def lookup(self, zobrist_key):
        index = zobrist_key % self.size
        entry = self.table[index]
        if entry and entry['key'] == zobrist_key:
            self.hits += 1
            return entry
        return None

    def get_stats(self):
        return f"TT Stats: Hits: {self.hits}, Stores: {self.stores}, Hit rate: {self.hits/self.stores:.2%}" if self.stores else "No TT activity"