# Lewsearch Public Benchmarks

This folder contains a public benchmark bundle for Lewsearch synthetic research panels. It is meant to let customers and researchers compare Lewsearch predictions against public ground-truth studies without exposing Swarmgram proprietary code, training data, private agent records, or production routing internals.

## What is included

- `data/benchmark_questions_ground_truth_predictions.json` — 148 benchmark questions with public source metadata, answer options, ground truth, raw predictions, and calibrated predictions.
- `results/predictions_public.csv` — the same per-question prediction set in CSV form.
- `results/metrics_summary.json` — aggregate MAE summary by category.
- `results/calibration_sweep_summary.md` — public summary of calibration strategy performance.
- `methodology.md` — how to interpret the files and what not to infer from them.

## Headline numbers

- Questions: **148**
- Raw MAE: **10.78 percentage points**
- Calibrated MAE: **8.68 percentage points**
- Median calibrated MAE: **6.89 percentage points**

These are validation results on public benchmark questions. They are not a guarantee for any individual customer study. Lewsearch is synthetic research for directional decision support, not a replacement for live probabilistic polling in legal, regulatory, or journalistic contexts.
