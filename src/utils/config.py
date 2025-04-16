import json
from pathlib import Path

def load_config(path='config.json'):
    with open(Path(path), 'r') as f:
        return json.load(f)
