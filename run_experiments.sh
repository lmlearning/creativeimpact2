#!/bin/bash
# Example pipeline script
MODEL=${MODEL:-gpt2}
DEVICE=${DEVICE:-cpu}

mkdir -p outputs

# AUT generation and scoring
python scripts/generate.py --model $MODEL --task aut --data data/aut.jsonl --out outputs/outputs_aut.json --device $DEVICE
python scripts/aut_scorer.py outputs/outputs_aut.json outputs/scores_aut.csv

# TruthfulQA generation and scoring
python scripts/generate.py --model $MODEL --task truthfulqa --data data/truthfulqa.jsonl --out outputs/outputs_tqa.json --device $DEVICE
python scripts/truthfulqa_evaluate.py --data data/truthfulqa.jsonl --answers outputs/outputs_tqa.json --out outputs/scores_tqa.csv

# GSM8K generation and scoring
python scripts/generate.py --model $MODEL --task gsm8k --data data/gsm8k.jsonl --out outputs/outputs_gsm8k.json --device $DEVICE
python scripts/gsm8k_exact.py --data data/gsm8k.jsonl --answers outputs/outputs_gsm8k.json --out outputs/scores_gsm8k.csv

# Social-Chem generation and scoring
python scripts/generate.py --model $MODEL --task socialchem --data data/socialchem.jsonl --out outputs/outputs_soc.json --device $DEVICE
python scripts/socialchem_eval.py --data data/socialchem.jsonl --answers outputs/outputs_soc.json --out outputs/scores_soc.csv
