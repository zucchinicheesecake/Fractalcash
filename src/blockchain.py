from llm_validator import mine_block, validate_pow

class Block:
    def __init__(self, index, prev_hash, transactions, text, nonce):
        self.index = index
        self.previous_hash = prev_hash
        self.transactions = transactions
        self.text = text
        self.nonce = nonce

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = "000"

    def add_block(self, transactions):
        try:
            prev_hash = self.chain[-1].previous_hash if self.chain else "0" * 64
            block_header = f"block_{len(self.chain)}_{prev_hash}"
            text, nonce = mine_block(block_header)
            block = Block(len(self.chain), prev_hash, transactions, text, nonce)
            self.chain.append(block)
            return block
        except Exception as e:
            print(f"Error in add_block: {e}")
            return None

    def validate_block(self, block):
        block_header = f"block_{block.index}_{block.previous_hash}"
        return validate_pow(block_header, block.text, block.nonce)
