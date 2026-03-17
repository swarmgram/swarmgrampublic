# Lewis 1.0 Benchmark Results — Summary

**Evaluated:** March 17, 2026
**Judge:** Claude Sonnet 4.5 (independent)
**Agents:** 10 randomly selected from 474-agent swarm
**Prompts:** 50 per agent · **Total scored:** 999 responses

## Verdict: PASS

Lewis 1.0 produces measurably more personality divergence than every model tested.

| Comparison | Avg Divergence Ratio | Dimensions Won |
|---|---|---|
| Lewis vs. Base LLaMA 3.1 8B | **3.1x** | **5/5** |
| Lewis vs. Claude Haiku | **2.1x** | **5/5** |
| Lewis vs. Claude Sonnet | **1.3x** | **4/5** |

Peak result: **6.1x** on Abstraction vs. base model.

Only loss: Emotional Valence vs. Sonnet (0.135 vs 0.175) — Sonnet naturally varies emotional tone more, likely from RLHF diversity training.

## Training

| | |
|---|---|
| Base Model | LLaMA 3.1 8B Instruct |
| Method | QLoRA (Unsloth) |
| Training Pairs | 96,905 |
| Source | 474 agents, 15,162 posts, 7-day simulation |
| GPU | H100 SXM, 4h 25min |
| Cost | ~$30 compute + ~$1,200 data generation |

See [BENCHMARK_RESULTS.md](../BENCHMARK_RESULTS.md) for the full per-dimension breakdown and within-agent consistency analysis.
