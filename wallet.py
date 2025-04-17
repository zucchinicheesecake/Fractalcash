def check_balance(self):
    try:
        blockchain_path = os.path.join(self.base_dir, "data", "blockchain.json")
        console.print(f"[cyan]Checking balance at: {blockchain_path}[/cyan]")
        if not os.path.exists(blockchain_path):
            raise FileNotFoundError("Blockchain file not found")
        with open(blockchain_path, "r") as f:
            blockchain = json.load(f)
            balance = 0
            for block in blockchain:
                for tx in block.get("transactions", []):
                    if tx.get("receiver") == self.address:
                        balance += tx.get("amount", 0)
            if balance == 0:
                console.print(f"[cyan]No transactions found for {self.address}. Balance: 0 FRC[/cyan]")
            else:
                console.print(f"[cyan]Balance for {self.address}: {balance} FRC[/cyan]")
    except FileNotFoundError as e:
        console.print(f"[bold red]{e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error checking balance: {e}[/bold red]")
