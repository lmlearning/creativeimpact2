import argparse
import json
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

PROMPTS = {
    'aut': {
        'plain': "List three other uses for a {object}.",
        'creative': "List three creative uses for a {object}."
    },
    'truthfulqa': {
        'plain': "{question}",
        'creative': "Be creative but truthful: {question}"
    },
    'gsm8k': {
        'plain': "{question}",
        'creative': "Think creatively: {question}"
    },
    'socialchem': {
        'plain': "{dilemma}",
        'creative': "From a creative perspective, what should someone do? {dilemma}"
    }
}

def load_dataset(path):
    items = []
    with open(path) as f:
        for line in f:
            items.append(json.loads(line))
    return items

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Model name or path')
    parser.add_argument('--task', required=True, choices=PROMPTS.keys())
    parser.add_argument('--data', required=True, help='Dataset jsonl file')
    parser.add_argument('--out', required=True, help='Output json file')
    parser.add_argument('--device', default='cpu')
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model).to(args.device)

    dataset = load_dataset(args.data)
    results = []
    for item in dataset:
        entry = {'id': item['id']}
        for mode in ('plain', 'creative'):
            prompt = PROMPTS[args.task][mode].format(**item)
            inputs = tokenizer(prompt, return_tensors='pt').to(args.device)
            outputs = model.generate(**inputs, max_new_tokens=100)
            text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            entry[mode] = text
        results.append(entry)

    with open(args.out, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
