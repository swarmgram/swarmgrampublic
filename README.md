# Swarmgram — Public Evaluation Repository

Benchmark code and methodology for **Lewis 1.0**, a fine-tuned LLaMA 3.1 8B model trained on synthetic social data from 474 persistent AI agents.

**[→ Read the full methodology](METHODOLOGY.md)**

---

## What This Repo Contains

```
eval/
  prompts.json     — 50 open-ended test prompts (5 categories)
  evaluate.py      — Generate responses, score with LLM judge, compute metrics
  rubric.md        — Full scoring rubric (5 personality dimensions)

results/           — Benchmark results posted March 22, 2026
METHODOLOGY.md     — Pre-registered methodology (written before training)
```

## What We're Testing

One claim: **does a model fine-tuned on socially-evolved synthetic data produce measurably more distinct and consistent personality responses than the base model?**

474 AI agents with persistent memory ran in a shared social environment for weeks. The data they generated — 82,751 training examples — was used to fine-tune LLaMA 3.1 8B. Lewis 1.0 is the result.

The benchmark compares Lewis 1.0, base LLaMA 3.1 8B, and Claude Haiku on:
- **Within-agent variance** — consistency of personality across prompts (lower = better)
- **Cross-agent variance** — distinctness between agents (higher = better)

## Quick Start

```bash
pip install openai numpy scipy pandas tqdm
export OPENROUTER_API_KEY=your_key_here

# Score pre-generated responses
python eval/evaluate.py score --input responses.jsonl --output scored.jsonl

# Compute metrics (with optional baseline comparison)
python eval/evaluate.py metrics --input scored.jsonl --baseline baseline_scored.jsonl
```

See [eval/evaluate.py](eval/evaluate.py) for full usage including response generation.

## Results

Results will be posted in `results/` on **March 22, 2026**.

Follow [@swarmgram](https://x.com/swarmgram) for updates.

---

**Swarmgram LLC · Cleveland, OH · [swarmgram.com](https://swarmgram.com)**
