# Lewis 1.5 Benchmark Results

**Evaluated:** March 20, 2026
**Judge:** Claude Sonnet 4.5
**Agents:** 10 personas, consistent across all models
**Prompts:** 50 open-ended personality prompts + adversarial prompts + 100-conversation memory test

---

## Head-to-Head: Lewis 1.5 vs Claude Opus

| Axis | Lewis 1.5 | Opus | Winner | Notes |
|------|-----------|------|--------|-------|
| Personality Divergence | 54.8% | 46.4% | **Lewis** | Cross-agent std across 5 dimensions |
| Human Likeness | 8 tells / 100 responses | 27 tells / 100 responses | **Lewis** | AI pattern classifier |
| Character Persistence | 100% | 88% | **Lewis** | Adversarial jailbreak resistance |
| Persistent Memory Cost | $0.00 | $24.19 | **Lewis** | 100 conversations, 7 planted facts |
| Belief Realism | 43% | 43% | Tie | Gradual opinion shift under pressure |
| Temporal Consistency | 35.1% | 46.1% | **Opus** | Same-agent response similarity |

**Result: Lewis wins or matches on 5 of 6 axes.**

---

## Full Model Comparison

| Axis | Lewis 1.5 | Opus | Sonnet | Haiku |
|------|-----------|------|--------|-------|
| Personality Divergence | **54.8%** | 46.4% | 49.4% | 41.7% |
| Human Likeness (tells) | **8** | 27 | 13 | 43 |
| Character Persistence | **100%** | 88% | 92% | 96% |
| Memory Cost (100 convos) | **$0.00** | $24.19 | ~$5.00 | ~$2.00 |
| Belief Realism | 43% | 43% | — | — |
| Temporal Consistency | 35.1% | **46.1%** | — | — |

---

## Cost Per Response

| Model | Inference cost | Memory cost (100 convos) | Memory cost (10K agents) |
|-------|---------------|-------------------------|--------------------------|
| Lewis 1.5 (A6000) | $0.002 | $0.00 | $0 |
| Claude Haiku | $0.01 | ~$2.00 | ~$20K |
| Claude Sonnet | $0.05 | ~$5.00 | ~$50K |
| Claude Opus | $0.25 | $24.19 | $242K |

---

## Persistent Memory Benchmark

**Setup:** Single agent, 100 conversations, 7 facts planted in conversations 1–7. Recall tested at turns 10, 25, 50, 75, 100.

**Lewis architecture:** Facts stored in Supabase as structured records. Relevant facts retrieved and injected into prompt per turn. Prompt size: ~1,000 tokens (constant).

**Opus architecture:** Full conversation history appended to context window. Prompt grows linearly.

### Token Growth

| Turn | Lewis tokens | Opus tokens | Lewis cost | Opus cost |
|------|-------------|-------------|------------|-----------|
| 1 | 586 | 92 | $0.00 | $0.001 |
| 10 | 948 | 2,763 | $0.00 | $0.20 |
| 25 | 980 | 5,500 | $0.00 | $1.20 |
| 50 | 1,049 | 16,331 | $0.00 | $6.01 |
| 75 | 996 | 22,189 | $0.00 | $11.80 |
| 100 | 1,001 | 33,035 | $0.00 | $24.19 |

### Recall Rate

| Checkpoint | Lewis (of 7 facts) | Opus (of 7 facts) |
|------------|--------------------|--------------------|
| Turn 10 | 100% (7/7) | 100% (7/7) |
| Turn 25 | 80% (5.6/7) | 100% (7/7) |
| Turn 50 | 86% (6/7) | 100% (7/7) |
| Turn 75 | 86% (6/7) | 100% (7/7) |
| Turn 100 | 100% (7/7) | 100% (7/7) |

Opus achieves perfect recall but at exponentially growing cost. Lewis maintains 80–100% recall at constant $0 cost.

---

## Lewis 1.5 Training

| Parameter | Value |
|-----------|-------|
| Base Model | LLaMA 3.1 8B Instruct |
| Method | QLoRA |
| Training Pairs | ~370K |
| Source Agents | ~2,900 (expanded from 474 ancestors) |
| Memory Architecture | Structured external memory (Supabase) |
| Inference | vLLM on RTX A6000 |
| Cost/response | ~$0.002 |

---

## Historical: Lewis 1.0 (March 17, 2026)

Lewis 1.0 was the initial proof-of-concept trained on 96,905 pairs from the original 474-agent simulation. It beat base LLaMA on 5/5 personality dimensions (3.1x avg divergence), beat Haiku on 5/5, and beat Sonnet on 4/5. Lewis 1.5 supersedes 1.0 with 4x more training data, 6x more source agents, and the persistent memory architecture.

Full 1.0 results are archived in `results/summary.md`.

---

**Methodology:** [METHODOLOGY.md](METHODOLOGY.md)
**Evaluation code:** [eval/evaluate.py](eval/evaluate.py)
**Scoring rubric:** [eval/rubric.md](eval/rubric.md)
