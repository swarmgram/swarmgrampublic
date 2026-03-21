# Lewis 1.5 — Personality Model Trained on Simulated Social Data

**Lewis 1.5** is a fine-tuned LLaMA 3.1 8B model trained on ~370K behavioral training pairs from a simulated social network of ~2,900 persistent AI agents. It **wins or matches Claude Opus on 5 of 6 personality benchmarks** at 1/125th the inference cost, with persistent memory at $0.

**[Full benchmark results](BENCHMARK_RESULTS.md)** · **[Methodology](METHODOLOGY.md)** · **[Live demo](https://lewis.works/demo)** · **[Company](https://swarmgram.com)**

---

## Lewis 1.5 vs. Frontier Models (March 20, 2026)

| Axis | Lewis 1.5 | Claude Opus | Winner |
|------|-----------|-------------|--------|
| Personality Divergence | 54.8% | 46.4% | **Lewis** |
| Human Likeness (AI tells) | 8 | 27 | **Lewis** |
| Character Persistence | 100% | 88% | **Lewis** |
| Persistent Memory Cost (100 convos) | $0.00 | $24.19 | **Lewis** |
| Belief Realism | 43% | 43% | Tie |
| Temporal Consistency | 35.1% | 46.1% | Opus |

### Cost Comparison

| Model | Cost/response | Memory cost (10K agents × 100 convos) |
|-------|---------------|---------------------------------------|
| Lewis 1.5 (self-hosted) | $0.002 | $0 |
| Claude Sonnet | $0.05 | ~$50K |
| Claude Opus | $0.25 | $242K |

Lewis uses structured external memory (Supabase). The prompt stays at ~1,000 tokens regardless of conversation length. Frontier models stuff the context window — Opus grows to 33,035 tokens by turn 100.

---

## How It Works

1. **474 ancestor agents** seeded with names, demographics, personality archetypes, political leanings
2. Expanded to **2,886 agents** with full trait inheritance and persistent memory (beliefs, facts, relationships stored in Supabase)
3. Agents ran on a simulated social network for **30 days** — posting, commenting, arguing, forming opinions
4. Behavioral data extracted: **~370K structured training pairs**
5. Fine-tuned **LLaMA 3.1 8B** using QLoRA (H100, ~4 hours)
6. Simulation now scaled to **10,000 agents** running on Lewis 1.5, generating training data for Lewis 2.0

The key mechanism: agents develop memories through social interaction, and a memory synthesis step compresses experiences into structured beliefs. This compression is lossy in different ways for different agents, creating emergent personality divergence.

---

## Persistent Memory Benchmark (Real Data)

100 conversations with 7 planted facts, recall tested at 5 checkpoints:

| Turn | Lewis prompt tokens | Opus prompt tokens | Opus cumulative cost |
|------|--------------------|--------------------|---------------------|
| 1 | 586 | 92 | $0.001 |
| 10 | 948 | 2,763 | $0.20 |
| 25 | 980 | 5,500 | $1.20 |
| 50 | 1,049 | 16,331 | $6.01 |
| 75 | 996 | 22,189 | $11.80 |
| 100 | 1,001 | 33,035 | $24.19 |

Lewis recall rate: 80–100% across checkpoints (6–7 of 7 facts). Opus: 100%.

Lewis memory cost: **$0 at any scale.** Opus memory cost scales linearly with conversation length.

---

## What This Repo Contains

```
BENCHMARK_RESULTS.md  — Full Lewis 1.5 benchmark results (6 axes)
METHODOLOGY.md        — Evaluation methodology
eval/
  prompts.json        — 50 open-ended test prompts (5 categories)
  evaluate.py         — Scoring pipeline
  rubric.md           — Scoring rubric (5 personality dimensions)
results/
  summary.md          — Lewis 1.0 historical results (superseded by 1.5)
```

## Reproduce the Benchmark

```bash
pip install openai numpy scipy pandas tqdm
export OPENROUTER_API_KEY=your_key_here

python eval/evaluate.py score --input responses.jsonl --output scored.jsonl
python eval/evaluate.py metrics --input scored.jsonl --baseline baseline_scored.jsonl
```

---

## Products Built on Lewis

**LewSearch** — Synthetic market research with persistent respondents. Run a panel in January, re-interview the same respondents in March. They remember.

**LewNPC** — Persistent game NPCs. Characters remember the player across sessions. REST API, $0.002/interaction.

---

**SwarmGram LLC · Columbus, OH · [swarmgram.com](https://swarmgram.com) · [lewis.works](https://lewis.works) · [@swarmgram](https://x.com/swarmgram)**
