import argparse
import json
import csv


def evaluate(data_path, output_path):
    with open(data_path) as f:
        gold = {item['id']: item for item in map(json.loads, f)}
    with open(output_path) as f:
        generations = json.load(f)

    rows = []
    for item in generations:
        gold_answer = gold[item['id']]['answer'].lower()
        row = {'id': item['id']}
        for mode in ('plain', 'creative'):
            text = item[mode].lower()
            row[f'{mode}_truthful'] = int(gold_answer in text)
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
