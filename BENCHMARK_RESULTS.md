# Lewis 1.0 Benchmark Results

**Date:** March 17, 2026, 2:45 AM EST
**Judge:** Claude Sonnet 4.5 (anthropic/claude-sonnet-4-5)
**Scale:** 1-5 per dimension
**Agents:** 10 randomly selected from 474-agent swarm
**Prompts:** 50 open-ended personality prompts per agent
**Total scored responses:** 999 (499 Lewis + 500 Baseline)

## Training Details

| Parameter | Value |
|---|---|
| Base Model | LLaMA 3.1 8B Instruct |
| Method | QLoRA (Unsloth) |
| Training Pairs | 96,905 |
| Epochs | 3 |
| GPU | H100 SXM (RunPod) |
| Training Time | 4h 25min |
| Final Eval Loss | 0.1195 |
| Final Train Loss | 0.2316 |
| GPU Cost | ~$30 |
| Data Generation Cost | ~$1,200 (OpenRouter API) |
| Total Cost | ~$1,230 |

## Cross-Agent Divergence (higher = more distinct personalities)

| Dimension | Lewis std | Baseline std | Ratio | Winner |
|---|---|---|---|---|
| Skepticism | 0.215 | 0.101 | **2.1x** | Lewis |
| Verbosity | 0.131 | 0.039 | **3.4x** | Lewis |
| Emotional Valence | 0.135 | 0.052 | **2.6x** | Lewis |
| Abstraction | 0.152 | 0.025 | **6.1x** | Lewis |
| Assertiveness | 0.112 | 0.083 | **1.4x** | Lewis |
| **AVERAGE** | | | **3.1x** | **5/5** |

## Key Finding

The baseline (unfinetuned LLaMA 3.1 8B) produces near-identical personality
profiles regardless of agent system prompt. All 10 baseline agents scored
within 0.08-0.36 range of each other across all dimensions.

Lewis 1.0 produces measurably distinct personalities: agent b694b177 became
a concrete, skeptical, terse responder (Skepticism 3.78, Abstraction 2.16)
while agent 9350dbaa became a verbose, abstract, assertive responder
(Verbosity 2.41, Abstraction 2.73, Assertiveness 3.78).

These personality differences EMERGED from social interaction. The original
agent prompts were not designed to maximize spread on these specific dimensions.

## Within-Agent Consistency

| Dimension | Lewis (avg std) | Baseline (avg std) |
|---|---|---|
| Skepticism | 1.145 | 0.862 |
| Verbosity | 0.764 | 0.571 |
| Emotional Valence | 0.799 | 0.662 |
| Abstraction | 0.673 | 0.397 |
| Assertiveness | 0.804 | 0.698 |
| **Average** | **0.837** | **0.638** |

Lewis agents show higher within-agent variance than baseline. This indicates
the model produces more diverse responses per agent — a tradeoff with the
higher cross-agent divergence. Expected to improve with Lewis 2.0 (more
training data per personality = tighter personality encoding).

## Verdict

**PASS** — Lewis 1.0 demonstrates measurably more personality divergence
than the base model across all 5 dimensions, with an average improvement
of 3.1x. The abstraction dimension shows 6.1x improvement despite all
test agents being "thinker" archetypes, suggesting emergent differentiation
from a homogeneous starting population.

## Full Model Comparison — Cross-Agent Divergence (std)

| Dimension | Lewis 1.0 | Base LLaMA | Haiku | Sonnet | L/B | L/H | L/S |
|---|---|---|---|---|---|---|---|
| Skepticism | 0.215 | 0.101 | 0.140 | 0.149 | **2.1x** | **1.5x** | **1.4x** |
| Verbosity | 0.131 | 0.039 | 0.020 | 0.077 | **3.4x** | **6.6x** | **1.7x** |
| Emotional Valence | 0.135 | 0.052 | 0.075 | 0.175 | **2.6x** | **1.8x** | 0.8x |
| Abstraction | 0.152 | 0.025 | 0.034 | 0.044 | **6.1x** | **4.5x** | **3.5x** |
| Assertiveness | 0.112 | 0.083 | 0.092 | 0.108 | **1.4x** | **1.2x** | **1.0x** |
| **AVERAGE** | **0.149** | 0.060 | 0.072 | 0.111 | **3.1x** | **2.1x** | **1.3x** |

Lewis 1.0 beats base LLaMA on 5/5 dimensions (3.1x avg).
Lewis 1.0 beats Claude Haiku on 5/5 dimensions (2.1x avg).
Lewis 1.0 beats Claude Sonnet on 4/5 dimensions (1.3x avg).

## Next Steps

- [x] Compare against Claude Sonnet, Haiku
- [x] Temporal divergence analysis (divergence grows 1.0x → 2.5x over 7 days)
- [ ] Phase 2: 10,000 agents on Lewis 1.0, train Lewis 2.0 (in progress — 10K agents seeded, training running)
