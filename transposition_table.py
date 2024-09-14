class TranspositionTable: 
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.hits = 0
        self.stores = 0

    def store(self, zobrist_key, depth_searched, score, flag, best_move):
        self.stores += 1
        index = zobrist_key % self.size
        self.table[index] = (zobrist_key, depth_searched, score, flag, best_move)

    def lookup(self, zobrist_key):
        index = zobrist_key % self.size
        entry = self.table[index]
        if entry and entry[0] == zobrist_key:
            self.hits += 1
            return {
                'key': entry[0],
                'depth_searched': entry[1],
                'socre':entry[2],
                'flag': entry[3],
                'best_move': entry[4]
            }
        return None

    def get_stats(self):
        return f"TT Stats: Hits: {self.hits}, Stores: {self.stores}, Hit rate: {self.hits/self.stores:.2%}" if self.stores else "No TT activity"