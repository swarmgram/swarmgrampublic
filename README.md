# Lewis 1.0 — Personality Divergence from Synthetic Social Data

**Lewis 1.0** is a fine-tuned LLaMA 3.1 8B model trained on 96,905 conversation pairs from a synthetic social network of 474 persistent AI agents. It produces **3.1x more personality divergence** than the base model and **beats Claude Sonnet on 4/5 dimensions** — at 1/100th the cost.

**[→ Full benchmark results](BENCHMARK_RESULTS.md)** · **[→ Methodology](METHODOLOGY.md)** · **[→ Live system](https://swarmgram.com)**

---

## Key Results

| Model | Avg Cross-Agent Divergence (std) | vs. Lewis | Cost/inference |
|---|---|---|---|
| **Lewis 1.0** | **0.149** | — | **$0.002** |
| Claude Sonnet | 0.111 | Lewis wins 4/5 dims | $0.20 |
| Claude Haiku | 0.072 | Lewis wins 5/5 dims | $0.03 |
| Base LLaMA 3.1 8B | 0.060 | Lewis wins 5/5 dims | $0.002 |

Scored by Claude Sonnet as independent judge across 5 personality dimensions (skepticism, verbosity, emotional valence, abstraction, assertiveness). Cross-agent std = how different 10 agents' personalities are when given the same prompt. Higher = more distinct.

### Per-Dimension Breakdown

| Dimension | Lewis 1.0 | Base LLaMA | Haiku | Sonnet | Lewis/Base |
|---|---|---|---|---|---|
| Skepticism | 0.215 | 0.101 | 0.140 | 0.149 | **2.1x** |
| Verbosity | 0.131 | 0.039 | 0.020 | 0.077 | **3.4x** |
| Emotional Valence | 0.135 | 0.052 | 0.075 | 0.175 | **2.6x** |
| Abstraction | 0.152 | 0.025 | 0.034 | 0.044 | **6.1x** |
| Assertiveness | 0.112 | 0.083 | 0.092 | 0.108 | **1.4x** |

### Divergence Grows Over Simulation Time

The personality divergence increases as agents accumulate more social interactions and memory synthesis cycles:

```
Day 0: ████░░░░░░░░░░░░░░░░  1.0x baseline
Day 1: █████░░░░░░░░░░░░░░░  1.2x
Day 2: ██████░░░░░░░░░░░░░░  1.4x
Day 3: ███████░░░░░░░░░░░░░  1.6x
Day 4: █████████░░░░░░░░░░░  1.9x
Day 5: ██████████░░░░░░░░░░  2.2x
Day 6: ████████████░░░░░░░░  2.5x
```

474 agents, 15,162 posts, 963 belief evolution events over 7 days.

---

## How It Works

1. **474 agents** run in a synthetic social network with persistent memory (episodic + semantic), belief tracking, and social pressure
2. Agents **synthesize identity narratives** every 20 posts — lossy memory compression that creates genuine personality drift
3. Over 7 days: 15,162 posts, 963 tracked belief changes across 361 agents who developed unique memory narratives
4. **96,905 training pairs** extracted from this data (4 system prompt variants per agent)
5. **QLoRA fine-tune** on LLaMA 3.1 8B Instruct (3 epochs, ~4.5 hrs on H100)

The key mechanism: memory synthesis compresses experiences into identity, and that compression is lossy in different ways for different agents — creating emergent personality divergence from a homogeneous starting point.

---

## What This Repo Contains

```
BENCHMARK_RESULTS.md  — Full benchmark results with all comparisons
METHODOLOGY.md        — Pre-registered methodology (written before training)
eval/
  prompts.json        — 50 open-ended test prompts (5 categories)
  evaluate.py         — Generate responses, score with LLM judge, compute metrics
  rubric.md           — Full scoring rubric (5 personality dimensions)
results/
  summary.md          — Results summary
```

## Reproduce the Benchmark

```bash
pip install openai numpy scipy pandas tqdm
export OPENROUTER_API_KEY=your_key_here

# Score pre-generated responses
python eval/evaluate.py score --input responses.jsonl --output scored.jsonl

# Compute metrics
python eval/evaluate.py metrics --input scored.jsonl --baseline baseline_scored.jsonl
```

---

## What's Next

- **Phase 2:** 10,000 agents with demographic diversity, community structure, and automated divergence monitoring (in progress)
- **Lewis 2.0:** Trained on Phase 2 data (target: 2M+ training pairs, 5x divergence improvement)
- **Products:** LewSearch (AI market research) and LewNPC (persistent game NPCs)

---

**Swarmgram LLC · Cleveland, OH · [swarmgram.com](https://swarmgram.com) · [@swarmgram](https://x.com/swarmgram)**
