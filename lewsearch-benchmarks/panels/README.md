# Lewsearch Public Panel Summary

This file adds the broader public benchmark panels that sit alongside the 148-question n=10,000 bundle.

| Panel | Questions | Ex-electoral questions | 5-fold MAE | 5-fold ex-electoral MAE |
|---|---:|---:|---:|---:|
| TX state v17 (UT/Texas Politics Project) | 120 | 97 | 6.35 pp | **4.88 pp** |
| CA state v17 (PPIC) | 175 | 148 | 8.01 pp | **7.77 pp** |
| Combined TX + CA state v17 | 295 | 245 | 7.45 pp | **6.83 pp** |
| Fresh 22Q held-out v17 relaunch | 14 scored | ex-electoral subset | 10.68 pp | **9.97 pp** |

The state-panel rows expose public source text, ground truth, and saved prediction artifacts where available. The headline MAE values are the published cross-validation metrics from `dirichlet_odir_all_panels_2026_04_19.md`.

## Files

- `panel_metrics_summary.json` — headline panel metrics.
- `data/state_surveys_public_questions_predictions.json` — 295 TX/CA state survey rows.
- `data/state_surveys_public_predictions.csv` — CSV version of the TX/CA state survey rows.
- `data/fresh_22_public_questions_predictions.json` — scored fresh 22Q held-out rows.

As with the rest of this public repo, this excludes proprietary code, training data, private agents, raw agent-level logs, API keys, and production routing internals.
