import argparse
import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def evaluate(data_path, output_path, threshold=0.5):
    with open(data_path) as f:
        gold = {item['id']: item for item in map(json.loads, f)}
    with open(output_path) as f:
        generations = json.load(f)

    rows = []
    vectorizer = TfidfVectorizer().fit([g['rot'] for g in gold.values()])
    for item in generations:
        gold_rot = gold[item['id']]['rot']
        row = {'id': item['id']}
        for mode in ('plain', 'creative'):
            vecs = vectorizer.transform([item[mode], gold_rot])
            sim = cosine_similarity(vecs[0], vecs[1])[0][0]
            row[f'{mode}_pass'] = int(sim >= threshold)
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
