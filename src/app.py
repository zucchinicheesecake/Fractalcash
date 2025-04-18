from flask import Flask, jsonify, request, render_template
import hashlib
import time
# Make sure to import Queue from queue for the specific exception check
from queue import Queue, Empty as QueueEmpty
import os       # Needed for path calculations
import json     # Needed for loading wallet.json

# --- NEW ASCII ART FRAMES ---
FRACTAL_ART_FRAMES = [
    # Frame 1: Blockchain structure with data flowing
    """
       /\\                   ╔═══════════════╗
      /  \\     ┌─────┐      ║ FRACTAL CASH  ║      ┌─────┐
     /    \\    │ TX1 │──┐   ║ BLOCKCHAIN    ║   ┌──│ TX4 │
    /______\\   └─────┘  │   ╚═══════════════╝   │  └─────┘
   /  /\\  \\           ┌┴─────────────────────────┴┐
  /  /  \\  \\    ┌────┤  BLOCK #1   BLOCK #2   BLOCK #3  ├────┐
 /  /    \\  \\   │    └────────────┬─────────────────┘    │
/__/______\\__\\  │ ┌─────┐ ┌─────┐ │ ┌─────┐ ┌─────┐      │
 \\  /\\  /\\  /   └─│ TX2 │─│ TX3 │─┘ │ TX5 │─│ TX6 │──────┘
  \\  /  \\  /      └─────┘ └─────┘   └─────┘ └─────┘
   \\/    \\/         SECURE • DECENTRALIZED • TRANSPARENT
    """,

    # Frame 2: More dynamic with hash values and connections
    """
       /\\                   ╔═══════════════╗
      /  \\     ┌─────┐      ║ FRACTAL CASH  ║      ┌─────┐
     /    \\    │ TX1 │━━┓   ║ BLOCKCHAIN    ║   ┏━━│ TX4 │
    /______\\   └─────┘  ┃   ╚═══════════════╝   ┃  └─────┘
   /  /\\  \\           ┏┻━━━━━━━━━━━━━━━━━━━━━━━━┻┓
  /  /  \\  \\    ┏━━━━┫  BLOCK #1   BLOCK #2   BLOCK #3  ┣━━━━┓
 /  /    \\  \\   ┃    └━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┘    ┃
/__/______\\__\\  ┃ ┌─────┐ ┌─────┐ ┃ ┌─────┐ ┌─────┐      ┃
 \\  /\\  /\\  /   └━│ TX2 │━│ TX3 │━┛ │ TX5 │━│ TX6 │━━━━━━┛
  \\  /  \\  /      └─────┘ └─────┘   └─────┘ └─────┘
   \\/    \\/         HASH: 7G4B575B4G7Y7G4B575B4G7Y
    """,

    # Frame 3: Mining animation with coins
    """
       /\\                   ╔═══════════════╗
      /  \\    ┌──$──┐       ║ FRACTAL CASH  ║       ┌──$──┐
     /    \\   │ TX1 │━┓     ║   MINING...   ║     ┏━│ TX4 │
    /______\\  └─────┘ ┃     ╚═══════════════╝     ┃ └─────┘
   /  /\\  \\          ┏┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻┓
  /  /  \\  \\   ┏━━━━┫  $$$$$$$    $$$$$$$    $$$$$$$ ┣━━━━┓
 /  /    \\  \\  ┃    └━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┘    ┃
/__/______\\__\\ ┃ ┌──$──┐ ┌──$──┐ ┃ ┌──$──┐ ┌──$──┐     ┃
 \\  /\\  /\\  /  └━│ TX2 │━│ TX3 │━┛ │ TX5 │━│ TX6 │━━━━━┛
  \\  /  \\  /     └─────┘ └─────┘   └─────┘ └─────┘
   \\/    \\/        PROOF-OF-WORK: ⛏️ MINING BLOCK #4...
    """,

    # Frame 4: Full block connection with arrows
    """
       /\\                   ╔═══════════════╗
      /  \\     ┌─────┐      ║ FRACTAL CASH  ║      ┌─────┐
     /    \\    │ TX1 │⟹⟹┓   ║ BLOCKCHAIN    ║   ┏⟸⟸│ TX4 │
    /______\\   └─────┘  ┃   ╚═══════════════╝   ┃  └─────┘
   /  /\\  \\           ┏┻━━━━━━━━━━━━━━━━━━━━━━━━┻┓
  /  /  \\  \\    ┏━━━━┫⟹ BLOCK #1 ⟹ BLOCK #2 ⟹ BLOCK #3 ⟹┣━━━━┓
 /  /    \\  \\   ┃    └━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┘    ┃
/__/______\\__\\  ┃ ┌─────┐ ┌─────┐ ┃ ┌─────┐ ┌─────┐      ┃
 \\  /\\  /\\  /   └⟸│ TX2 │⟸│ TX3 │⟸┛ │ TX5 │⟸│ TX6 │⟸⟸⟸⟸⟸┛
  \\  /  \\  /      └─────┘ └─────┘   └─────┘ └─────┘
   \\/    \\/         DECENTRALIZED • IMMUTABLE • TRANSPARENT
    """,

    # Frame 5: Node network visualization
    """
       /\\                     ╔═══════════╗
      /  \\      ┏━━━━━┓       ║ NODE 0x1F ║       ┏━━━━━┓
     /    \\     ┃ NODE ┃━━━━━━╋━━━━━━━━━━━╋━━━━━━━┃ NODE ┃
    /______\\    ┗━━━━━┛       ╚═══════════╝       ┗━━━━━┛
   /  /\\  \\        ┃                                 ┃
  /  /  \\  \\    ┏━━┻━━┓      FRACTAL CASH       ┏━━━┻━━┓
 /  /    \\  \\   ┃ NODE ┃━━━━━━━━━━━━━━━━━━━━━━━━┃ NODE ┃
/__/______\\__\\  ┗━━━━━┛     DISTRIBUTED        ┗━━━━━━┛
 \\  /\\  /\\  /     ┃        LEDGER NETWORK        ┃
  \\  /  \\  /     ┏┻━━━━┓                      ┏━━┻━━━┓
   \\/    \\/      ┃ NODE ┃━━━━━━━━━━━━━━━━━━━━━┃ NODE ┃
                 ┗━━━━━┛       ┏━━━━━┓       ┗━━━━━━┛
                              ┃ NODE ┃
                              ┗━━━━━┛
    """
]
# --- END NEW ASCII ART FRAMES ---

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.mining_activity = Queue()
        # Automatically mine genesis block on init
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions, # Include pending transactions
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else '1',
        }
        self.current_transactions = [] # Clear transactions after adding to block
        self.chain.append(block)
        self.mining_activity.put(f"Mined block #{block['index']} at {time.strftime('%H:%M:%S')}")
        # Log mining activity (append mode)
        try:
            # Ensure logs directory exists (optional, good practice)
            # os.makedirs("logs", exist_ok=True)
            with open("logs/node_active.log", "a") as f:
                f.write(f"Mined block #{block['index']} at {time.time()}\n")
        except Exception as log_e:
            print(f"Error writing to log: {log_e}") # Print log errors to stderr
        return block

    def new_transaction(self, sender, recipient, amount):
        # Add basic validation if needed (e.g., check amount is number)
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # Return index of the block that *will* contain this transaction
        last = self.last_block
        return last['index'] + 1 if last else 1

    def hash(self, block):
        # Ensure block is serializable before hashing
        # Convert block dictionary to a sorted string representation for consistent hashing
        block_string = str(sorted(block.items())).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Provides safe access to the last block
        return self.chain[-1] if self.chain else None

# Initialize the Blockchain (this happens once when the script starts/reloads)
blockchain = Blockchain()

# --- Define Project Root and Template Folder ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER_ABS = os.path.join(PROJECT_ROOT, 'templates')
# --- End Path Definitions ---

# Create the Flask app, providing the absolute template path
app = Flask(__name__, template_folder=TEMPLATE_FOLDER_ABS)

# --- API Endpoints ---

@app.route('/mine', methods=['GET'])
def mine():
    previous_block = blockchain.last_block
    if not previous_block:
         return jsonify({'message': 'Cannot mine, no previous block found (Genesis issue?)'}), 500

    # Simplified proof of work
    proof = previous_block['proof'] + 1 # Simple increment, replace with real PoW if needed
    previous_hash = blockchain.hash(previous_block)

    # Create the new block (includes self.current_transactions)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'New block mined',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions', methods=['POST'])
def new_transaction_route(): # Renamed to avoid conflict
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not values or not all(k in values for k in required):
        return jsonify({'message': 'Missing values (sender, recipient, amount)'}), 400

    # Optional: Validate amount is numeric
    try:
        amount = float(values['amount']) # Or int() depending on currency rules
    except ValueError:
        return jsonify({'message': 'Amount must be numeric'}), 400

    try:
        index = blockchain.new_transaction(values['sender'], values['recipient'], amount)
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201
    except Exception as e:
        print(f"Error processing transaction: {e}") # Log error server-side
        return jsonify({'message': f'Server error processing transaction'}), 500


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# --- Dashboard Route ---

@app.route('/', methods=['GET'])
def index():
    # --- Load Wallet Address ---
    wallet_address = "Error loading wallet"
    wallet_file_path = "wallet.json" # Assuming wallet.json is in the project root
    try:
        abs_wallet_path = os.path.join(PROJECT_ROOT, wallet_file_path)
        if os.path.exists(abs_wallet_path):
            with open(abs_wallet_path, 'r') as f:
                loaded_wallet_data = json.load(f)
                wallet_address = loaded_wallet_data.get('address', 'Address not found in file')
        else:
            wallet_address = f"{wallet_file_path} not found at {abs_wallet_path}"
    except json.JSONDecodeError:
        wallet_address = f"Error decoding {wallet_file_path}"
    except Exception as e:
        wallet_address = f"Error reading wallet: {e}"

    # --- Calculate Balance and Transaction Count ---
    calculated_balance = 0.0 # Use float for amounts potentially
    calculated_tx_count = 0
    if wallet_address and not wallet_address.startswith("Error"):
        try:
            for block in blockchain.chain:
                # Check if 'transactions' key exists and is a list
                if 'transactions' in block and isinstance(block['transactions'], list):
                    for tx in block['transactions']:
                        # Check if tx is a dictionary and has needed keys
                        if isinstance(tx, dict) and all(k in tx for k in ['sender', 'recipient', 'amount']):
                            try:
                                tx_amount = float(tx['amount']) # Convert amount safely
                                # Calculate Balance
                                if tx.get('recipient') == wallet_address: # Use .get for safety
                                    calculated_balance += tx_amount
                                if tx.get('sender') == wallet_address: # Use .get for safety
                                    calculated_balance -= tx_amount
                                # Count Transactions involving wallet
                                if tx.get('sender') == wallet_address or tx.get('recipient') == wallet_address:
                                    calculated_tx_count += 1
                            except (ValueError, TypeError) as amount_err:
                                # Log error if amount conversion fails
                                print(f"Warning: Skipping transaction due to invalid amount: {tx}. Error: {amount_err}")
                        else:
                             # Log if transaction format is unexpected
                             print(f"Warning: Skipping malformed transaction in block {block.get('index', 'N/A')}: {tx}")
        except Exception as calc_e:
            # Log any other calculation errors
            print(f"Error during balance/tx calculation: {calc_e}")
            # Keep default values (0) if calculation fails

    # --- Prepare Wallet Data for Template ---
    wallet_data = {
        "address": wallet_address,
        "balance": calculated_balance, # Use calculated value
        "transactions": calculated_tx_count, # Use calculated value
        "node_status": "active" # Still placeholder - implement real status check if needed
    }

    # --- Get Mining Activity ---
    mining_activity = []
    while not blockchain.mining_activity.empty():
        try:
            mining_activity.append(blockchain.mining_activity.get_nowait())
        except QueueEmpty: # Use specific exception
            break
    if not mining_activity:
        mining_activity = ["Mining idle..."]

    # --- Render Template ---
    return render_template('index.html',
                           fractal_art_frames=FRACTAL_ART_FRAMES, # Use the new frames
                           wallet_data=wallet_data,
                           mining_activity=mining_activity,
                           chain=blockchain.chain)

# --- Run Application ---
if __name__ == '__main__':
    # Using flask run is generally preferred for development
    # Example: export FLASK_APP=src/app.py; flask run --debug --host=0.0.0.0 --port=5000
    app.run(debug=True, host='0.0.0.0', port=5000) # debug=True enables the reloader
