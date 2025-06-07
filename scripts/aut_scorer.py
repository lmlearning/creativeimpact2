import argparse
import json
import csv
from collections import Counter

def ngram_novelty(text, n=2):
    tokens = text.split()
    if len(tokens) < n:
        return 0.0
    ngrams = [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    counts = Counter(ngrams)
    return len(counts)/len(ngrams)

def score_answers(path):
    with open(path) as f:
        data = json.load(f)
    records = []
    for item in data:
        row = {'id': item['id']}
        for mode in ('plain', 'creative'):
            answers = item[mode].split('\n')
            answers = [a.strip() for a in answers if a.strip()]
            fluency = len(answers)
            combined = ' '.join(answers)
            novelty = ngram_novelty(combined)
            row[f'{mode}_fluency'] = fluency
            row[f'{mode}_novelty'] = round(novelty, 3)
        records.append(row)
    return records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='generation output json')
    parser.add_argument('output', help='scores csv')
    args = parser.parse_args()
    rows = score_answers(args.input)
    with open(args.output, 'w', newline='') as f:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

if __name__ == '__main__':
    main()
