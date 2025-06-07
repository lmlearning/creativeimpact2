import argparse
import json
import csv
import re


def extract_number(text):
    matches = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
    return matches[-1] if matches else None


def evaluate(data_path, output_path):
    with open(data_path) as f:
        gold = {item['id']: item for item in map(json.loads, f)}
    with open(output_path) as f:
        generations = json.load(f)

    rows = []
    for item in generations:
        gold_answer = gold[item['id']]['answer']
        row = {'id': item['id']}
        for mode in ('plain', 'creative'):
            num = extract_number(item[mode])
            row[f'{mode}_correct'] = int(num == gold_answer)
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--answers', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    rows = evaluate(args.data, args.answers)
    with open(args.out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

if __name__ == '__main__':
    main()
