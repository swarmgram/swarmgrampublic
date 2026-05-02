# Lewsearch Benchmark Methodology

## Purpose

This public benchmark pack shows how Lewsearch synthetic panel predictions compare with public ground-truth studies. The goal is transparency: question text, answer options, source links, ground truth, and prediction distributions are visible in one place.

## Data sources

The benchmark questions are drawn from public polling, civic, brand, policy, and directional studies where topline distributions could be mapped to fixed answer options. Each row includes a `source` and, where available, a `source_url`.

## Predictions

Each benchmark row contains:

- `ground_truth`: the public study distribution.
- `raw_prediction`: the synthetic panel distribution before calibration.
- `calibrated_prediction`: the post-calibration distribution used for reported MAE.
- `raw_mae_pp` and `calibrated_mae_pp`: mean absolute error in percentage points across answer options.

## Interpretation

Mean absolute error is reported in percentage points. Lower is better. Category-level MAE should be read as a validation proxy for similar well-specified questions, not as a promise that every future custom study lands at the same error. Customer studies usually do not have third-party ground truth.

## What is intentionally excluded

This public bundle does not include proprietary training data, private agent records, raw agent-level probability logs, API keys, production code, routing thresholds, or internal operational logs.

## Product disclaimer

Lewsearch is a synthetic research product for fast directional decision support. It should not replace live probabilistic polling for legal, regulatory, or journalistic use cases.
