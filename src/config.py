def load_config(config_path="config.json"):
    import json
    with open(config_path, "r") as f:
        return json.load(f)
