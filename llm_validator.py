import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "TinyLLaMA/TinyLLaMA-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)

def generate_validation_params(block_height, pending_txs, node_cpu, node_txs, stake):
    prompt = f"""
    Current blockchain state: Block height {block_height}, {pending_txs} transactions pending, network load 70%.
    Node profile: CPU power {node_cpu}GHz, {node_txs} transactions validated, {stake} FC staked.
    Task: Assign validation subtasks and difficulty target to optimize efficiency.
    Output format: {{ "subtasks": [num_transactions], "difficulty": number }}
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    json_str = response.split("Output:")[-1].strip() if "Output:" in response else response
    return json.loads(json_str)

if __name__ == "__main__":
    import sys
    params = generate_validation_params(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    print(json.dumps(params))
