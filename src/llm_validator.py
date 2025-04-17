import os
import logging
import contextlib
from rich.console import Console
from transformers import pipeline, set_seed
import hashlib

console = Console()

def fracBlock(text, depth=3):
    if depth <= 0:
        return hashlib.sha256(text.encode()).hexdigest()
    current_hash = hashlib.sha256(text.encode()).hexdigest()
    left = fracBlock(current_hash[:32], depth-1)
    right = fracBlock(current_hash[32:], depth-1)
    return hashlib.sha256((left + right).encode()).hexdigest()

def generate_pow_text(block_header: str) -> str:
    os.environ["TQDM_DISABLE"] = "1"
    logging.getLogger("transformers").setLevel(logging.ERROR)
    with open(os.devnull, "w") as devnull:
        with contextlib.redirect_stdout(devnull):
            llm = pipeline("text-generation", model="distilgpt2", max_new_tokens=10)
            set_seed(42)  # Fixed seed for reproducibility
    return llm(f"Block header: {block_header.strip()}")[0]["generated_text"].strip()

def mine_block(block_header: str) -> tuple[str, int]:
    text = generate_pow_text(block_header)
    nonce = 0
    while not fracBlock(text + str(nonce)).startswith("000"):
        nonce += 1
    return text, nonce

def validate_pow(block_header: str, submitted_text: str, nonce: int) -> bool:
    expected_text = generate_pow_text(block_header)
    if submitted_text != expected_text:
        console.print("[bold red]Validation failed: Text mismatch. Expected: {}, Got: {}[/bold red]".format(expected_text, submitted_text))
        return False
    hash_result = fracBlock(submitted_text + str(nonce))
    if hash_result.startswith("000"):
        console.print(f"[bold green]Validation passed! Hash: {hash_result}[/bold green]")
        return True
    console.print("[bold red]Validation failed: Hash does not meet target.[/bold red]")
    return False

# Test
block_header = "block_1234_prevhash_abcdef"
text, nonce = mine_block(block_header)
console.print(f"[bold green]FractalHash PoW Result[/bold green]")
console.print(f"[cyan]Block Header:[/cyan] {block_header}")
console.print(f"[cyan]Text:[/cyan] {text}")
console.print(f"[cyan]Nonce:[/cyan] {nonce}")
console.print(f"[cyan]Hash:[/cyan] {fracBlock(text + str(nonce))}")
console.print(f"[cyan]Validation:[/cyan] {validate_pow(block_header, text, nonce)}")
