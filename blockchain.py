import json
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.file_path = "data/blockchain.json"
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.load()

    def load(self):
        """Load blockchain from file if it exists."""
        try:
            with open(self.file_path, "r") as f:
                self.chain = json.load(f)
        except FileNotFoundError:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Create the genesis block if the chain is empty."""
        if not self.chain:
            genesis_block = {
                "index": 0,
                "transactions": [],
                "previous_hash": "0" * 64,
                "text": "Genesis Block",
                "nonce": 0
            }
            self.chain.append(genesis_block)
            self.save()

    def add_block(self, transactions):
        """Add a new block to the chain."""
        block = {
            "index": len(self.chain),
            "transactions": transactions,
            "previous_hash": self.chain[-1]["previous_hash"] if self.chain else "0" * 64,
            "text": f"Block header: block_{len(self.chain)}_{self.chain[-1]['previous_hash'] if self.chain else '0' * 64}",
            "nonce": 0  # Will be updated by mining
        }
        self.chain.append(block)
        self.save()
        return block

    def save(self):
        """Save the blockchain to file."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.chain, f, indent=4)
        except Exception as e:
            print(f"Error saving blockchain: {e}")

    def validate_block(self, block):
        """Placeholder for validation (already working in main.py)."""
        return True  # Simplified for now
