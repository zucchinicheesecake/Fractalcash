import hashlib

def fracBlock(text, depth=3):
    """A recursive fractal hashing function that applies SHA-256 multiple times in a fractal pattern"""
    if depth <= 0:
        return hashlib.sha256(text.encode()).hexdigest()
    
    # Generate initial hash
    current_hash = hashlib.sha256(text.encode()).hexdigest()
    
    # Apply recursive hashing in a fractal pattern
    left = fracBlock(current_hash[:32], depth-1)
    right = fracBlock(current_hash[32:], depth-1)
    
    # Combine and hash again
    return hashlib.sha256((left + right).encode()).hexdigest()

text = "test"
nonce = 0
while not fracBlock(text + str(nonce)).startswith("0000"):
    nonce += 1

print("Text:", text, "Nonce:", nonce)
