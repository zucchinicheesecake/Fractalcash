import time
import hashlib
from src.fractalhash.fractalhash import FractalHash
from src.fractalhash.merkle_tree import MerkleTree

class FractalBlock:
    def __init__(self, index, previous_hash, transactions, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = 0
        self.merkle_root = self.compute_merkle_root()
        self.hash = self.mine_block()

    def compute_merkle_root(self):
        fh = FractalHash()
        hashed_txs = [bytes.fromhex(fh.compute(tx.encode())) for tx in self.transactions]
        tree = MerkleTree(hashed_txs)
        return tree.get_root()

    def compute_hash(self):
        fh = FractalHash()
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}"
        return fh.compute(block_string.encode())

    def mine_block(self):
        prefix = '0' * self.difficulty
        while True:
            hash_result = self.compute_hash()
            if hash_result.startswith(prefix):
                return hash_result
            self.nonce += 1
