from flask import Flask, jsonify, request, render_template
import hashlib
import time

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else '1',
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def hash(self, block):
        block_string = str(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

# Initialize the Blockchain
blockchain = Blockchain()

# Create the Flask app
app = Flask(__name__)

@app.route('/mine', methods=['GET'])
def mine():
    # Proof of work logic
    previous_block = blockchain.last_block
    proof = previous_block['proof'] + 1  # Simplified proof of work for example
    block = blockchain.new_block(proof, previous_block['previous_hash'])
    response = {
        'message': 'New block mined',
        'block': block
    }
    return jsonify(response), 200

@app.route('/transactions', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing values'}), 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
