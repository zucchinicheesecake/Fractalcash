import hashlib
from typing import List

class MerkleTree:
    def __init__(self, leaves: List[bytes]):
        self.leaves = leaves
        self.root = self.build_tree(leaves)

    def build_tree(self, nodes: List[bytes]) -> bytes:
        if len(nodes) == 1:
            return nodes[0]
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])  # Duplicate last if odd
        parents = []
        for i in range(0, len(nodes), 2):
            combined = nodes[i] + nodes[i+1]
            hashed = hashlib.sha256(combined).digest()
            parents.append(hashed)
        return self.build_tree(parents)

    def get_root(self) -> str:
        return self.root.hex()
