# Brute-Force Calibration Sweep — 20260421T004256Z

- Benchmark: n=10,000 agents, 151 questions (internal aggregate prediction log (not published))
- CV: 5-fold stratified on (category, n_opts), seed=42
- Strategies tried: 41

## Top 15

| Rank | Strategy | CV MAE (pp) | Std (pp) |
|-----:|----------|------------:|---------:|
| 1 | `dir_cat_nopts_od0.01_b0.001` | 8.031 | 5.13 |
| 2 | `isotonic_per_option` | 8.059 | 5.04 |
| 3 | `dir_cat_nopts_od0.05_b0.01` | 8.060 | 5.12 |
| 4 | `dir_cat_nopts_od0.1_b0.01` | 8.078 | 5.14 |
| 5 | `dir_cat_nopts_then_floor` | 8.078 | 5.14 |
| 6 | `stack_raw+dir_a=0.0` | 8.078 | 5.14 |
| 7 | `dir_cat_nopts_od0.3_b0.01` | 8.114 | 5.16 |
| 8 | `dir_cat_nopts_od1.0_b0.1` | 8.130 | 5.14 |
| 9 | `stack_raw+dir_a=0.1` | 8.148 | 4.98 |
| 10 | `stack_raw+dir_a=0.2` | 8.272 | 4.87 |
| 11 | `stack_raw+dir_a=0.3` | 8.443 | 4.80 |
| 12 | `dir_nopts_od0.01_b0.001` | 8.610 | 5.12 |
| 13 | `dir_nopts_od0.05_b0.01` | 8.628 | 5.11 |
| 14 | `dir_nopts_od0.1_b0.01` | 8.639 | 5.12 |
| 15 | `dir_nopts_od1.0_b0.1` | 8.644 | 5.12 |

## Winner — per-category breakdown

| Category | MAE (pp) |
|----------|---------:|
| civic_legal | 9.442 |
| directional | 9.198 |
| political_approval | 8.548 |
| brand | 7.352 |
| policy | 7.228 |
| electoral | 4.052 |

## Winner — per n_opts

| n_opts | MAE (pp) |
|-------:|---------:|
| 3 | 8.670 |
| 4 | 7.533 |
| 5 | 8.320 |
| 6 | 4.715 |
| 7 | 6.638 |
| 9 | 5.112 |
| 10 | 2.437 |

