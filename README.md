# Creative Impact Experiment Scripts

This repository provides a minimal setup for running four evaluation tasks comparing
"plain" and "creative" prompt framing. The pipeline generates model outputs and
scores them automatically.

## Directory layout
- `data/` contains small JSONL samples for each task.
- `scripts/` holds generation and scoring utilities.
- `outputs/` will be populated by the pipeline.

## Requirements
- Python 3.8+
- `transformers`, `torch`, and `scikit-learn` libraries.
- A local HuggingFace model path or name (e.g. `gpt2`).

Install dependencies with:
```bash
pip install transformers torch scikit-learn
```

## Running the pipeline
Execute `run_experiments.sh` with optional environment variables `MODEL` and `DEVICE`:
```bash
MODEL=gpt2 DEVICE=cpu ./run_experiments.sh
```
The script will:
1. Generate answers for each dataset under plain and creative prompts.
2. Score the generations with task-specific metrics.
3. Write CSV files in `outputs/` summarizing fluency, novelty and accuracy measures.

The provided datasets are tiny examples to illustrate the workflow. Replace them
with full datasets for real experiments.
