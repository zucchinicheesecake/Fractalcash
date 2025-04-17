import json
import time
import secrets
from flask import Flask, render_template
import threading

class FractalWallet:
    def __init__(self, blockchain, diagnostic_file="node_active.log"):
        self.blockchain = blockchain
        self.diagnostic_file = diagnostic_file
        self.address = None
        self.balance = 0
        self.transactions = []
        self.load_or_create_wallet()

    def load_or_create_wallet(self):
        try:
            with open("wallet.txt", "r") as f:
                self.address = f.read().strip()
        except FileNotFoundError:
            self.address = "0x" + secrets.token_hex(20)
            try:
                with open("wallet.txt", "w") as f:
                    f.write(self.address)
            except Exception as e:
                self._log_error(f"Failed to write wallet.txt: {str(e)}")
                self.address = "0xDEFAULT_WALLET_ADDRESS"
        except Exception as e:
            self._log_error(f"Failed to read wallet.txt: {str(e)}")
            self.address = "0xDEFAULT_WALLET_ADDRESS"
        self.sync_with_blockchain()
        return self.address

    def sync_with_blockchain(self):
        self.balance = 0
        self.transactions = []
        try:
            for block in self.blockchain.chain:
                transactions = block.get("transactions", [])
                if not isinstance(transactions, list):
                    self._log_error(f"Invalid transactions list in block: {block}")
                    continue
                for tx in transactions:
                    if not isinstance(tx, dict) or not all(key in tx for key in ["sender", "receiver", "amount"]):
                        self._log_error(f"Skipping invalid transaction: {tx}")
                        continue
                    self.transactions.append(tx)
                    if tx["receiver"] == self.address:
                        self.balance += tx["amount"]
                    if tx["sender"] == self.address:
                        self.balance -= tx["amount"]
            self.report_diagnostics()
        except Exception as e:
            self._log_error(f"Blockchain sync failed: {str(e)}")

    def report_diagnostics(self):
        data = {
            "event": "wallet_sync",
            "address": self.address,
            "balance": self.balance,
            "tx_count": len(self.transactions),
            "timestamp": int(time.time())
        }
        log_line = json.dumps(data) + "\n"
        try:
            with open(self.diagnostic_file, "a") as f:
                f.write(log_line)
        except Exception as e:
            print(f"Failed to write to {self.diagnostic_file}: {str(e)}")

    def _log_error(self, error_msg):
        error_data = {
            "event": "error",
            "message": error_msg,
            "timestamp": int(time.time())
        }
        try:
            with open(self.diagnostic_file, "a") as f:
                f.write(json.dumps(error_data) + "\n")
        except Exception:
            print(f"Failed to log error: {error_msg}")

    def get_balance(self):
        return self.balance

class FractalStake:
    def __init__(self):
        self.pool = {"total_staked": 0}

    def stake(self, amount):
        self.pool["total_staked"] += amount

class Blockchain:
    chain = [
        {"transactions": [
            {"sender": "0x0", "receiver": "0x1234", "amount": 50},
            {"sender": "0x1234", "receiver": "0x5678", "amount": 20}
        ]},
        {"transactions": [
            {"sender": "0x0", "receiver": "0x1234", "amount": 30}
        ]}
    ]

    def is_active(self):
        return False

app = Flask(__name__)

@app.route('/')
def dashboard():
    wallet.sync_with_blockchain()
    return render_template('dashboard.html',
                          address=wallet.address,
                          balance=wallet.get_balance(),
                          tx_count=len(wallet.transactions),
                          node_status="Running" if blockchain.is_active() else "Idle")

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

from rich.console import Console
console = Console()

def main():
    total_mined = 0
    console.print(f"[cyan]Mined: {total_mined} FRAC[/cyan]")
    blockchain = Blockchain()
    wallet = FractalWallet(blockchain)
    console.print(f"[cyan]Wallet Address: {wallet.address}[/cyan]")
    console.print(f"[cyan]Balance: {wallet.get_balance()} FRAC[/cyan]")

if __name__ == "__main__":
    blockchain = Blockchain()
    wallet = FractalWallet(blockchain)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    main()
