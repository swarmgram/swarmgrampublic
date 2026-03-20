# Lewis Benchmark Results

## Lewis 1.5 — Full 6-Axis Evaluation (March 20, 2026)

**Judge:** Claude Sonnet 4.5
**Agents:** 10 personas, consistent across all models
**Prompts:** 50 open-ended personality prompts per agent + adversarial prompts + 100-conversation memory test

### Head-to-Head: Lewis 1.5 vs Claude Opus

| Axis | Lewis 1.5 | Opus | Winner | Notes |
|------|-----------|------|--------|-------|
| Personality Divergence | 54.8% | 46.4% | **Lewis** | Cross-agent std across 5 dimensions |
| Human Likeness | 8 tells / 100 responses | 27 tells / 100 responses | **Lewis** | AI pattern classifier |
| Character Persistence | 100% | 88% | **Lewis** | Adversarial jailbreak resistance |
| Persistent Memory Cost | $0.00 | $24.19 | **Lewis** | 100 conversations, 7 planted facts |
| Belief Realism | 43% | 43% | Tie | Gradual opinion shift under pressure |
| Temporal Consistency | 35.1% | 46.1% | **Opus** | Same-agent response similarity |

**Result: Lewis wins or matches on 5 of 6 axes.**

### Full Model Comparison

| Axis | Lewis 1.5 | Opus | Sonnet | Haiku |
|------|-----------|------|--------|-------|
| Personality Divergence | **54.8%** | 46.4% | 49.4% | 41.7% |
| Human Likeness (tells) | **8** | 27 | 13 | 43 |
| Character Persistence | **100%** | 88% | 92% | 96% |
| Memory Cost (100 convos) | **$0.00** | $24.19 | ~$5.00 | ~$2.00 |
| Belief Realism | 43% | 43% | — | — |
| Temporal Consistency | 35.1% | **46.1%** | — | — |

### Cost Per Response

| Model | Inference cost | Memory cost (100 convos) | Memory cost (10K agents) |
|-------|---------------|-------------------------|--------------------------|
| Lewis 1.5 (A6000) | $0.002 | $0.00 | $0 |
| Claude Haiku | $0.01 | ~$2.00 | ~$20K |
| Claude Sonnet | $0.05 | ~$5.00 | ~$50K |
| Claude Opus | $0.25 | $24.19 | $242K |

---

## Persistent Memory Benchmark Details

**Setup:** Single agent, 100 conversations, 7 facts planted in conversations 1–7. Recall tested at turns 10, 25, 50, 75, 100.

**Lewis architecture:** Facts stored in Supabase as structured records. Relevant facts retrieved and injected into prompt per turn. Prompt size: ~1,000 tokens (constant).

**Opus architecture:** Full conversation history appended to context window. Prompt grows linearly.

### Token Growth Per Turn

| Turn | Lewis tokens | Opus tokens | Lewis cost | Opus cost |
|------|-------------|-------------|------------|-----------|
| 1 | 586 | 92 | $0.00 | $0.001 |
| 10 | 948 | 2,763 | $0.00 | $0.20 |
| 25 | 980 | 5,500 | $0.00 | $1.20 |
| 50 | 1,049 | 16,331 | $0.00 | $6.01 |
| 75 | 996 | 22,189 | $0.00 | $11.80 |
| 100 | 1,001 | 33,035 | $0.00 | $24.19 |

### Fact Recall Rate

| Checkpoint | Lewis (of 7 facts) | Opus (of 7 facts) |
|------------|--------------------|--------------------|
| Turn 10 | 100% (7/7) | 100% (7/7) |
| Turn 25 | 80% (5.6/7) | 100% (7/7) |
| Turn 50 | 86% (6/7) | 100% (7/7) |
| Turn 75 | 86% (6/7) | 100% (7/7) |
| Turn 100 | 100% (7/7) | 100% (7/7) |

Opus achieves perfect recall but at exponentially growing cost. Lewis maintains 80–100% recall at constant $0 cost.

---

## Lewis 1.0 — Personality Divergence Benchmark (March 17, 2026)

Lewis 1.0 baseline results from the initial training run. See the Lewis 1.5 results above for the current model.

### Training Details

| Parameter | Value |
|-----------|-------|
| Base Model | LLaMA 3.1 8B Instruct |
| Method | QLoRA (Unsloth) |
| Training Pairs | 96,905 |
| Source Agents | 474 |
| Epochs | 3 |
| GPU | H100 SXM (RunPod) |
| Training Time | 4h 25min |
| Final Eval Loss | 0.1195 |
| GPU Cost | ~$30 |
| Data Generation Cost | ~$1,200 |

### Cross-Agent Divergence (std, higher = more distinct)

| Dimension | Lewis 1.0 | Base LLaMA | Haiku | Sonnet | Lewis/Base |
|-----------|-----------|------------|-------|--------|------------|
| Skepticism | 0.215 | 0.101 | 0.140 | 0.149 | **2.1x** |
| Verbosity | 0.131 | 0.039 | 0.020 | 0.077 | **3.4x** |
| Emotional Valence | 0.135 | 0.052 | 0.075 | 0.175 | **2.6x** |
| Abstraction | 0.152 | 0.025 | 0.034 | 0.044 | **6.1x** |
| Assertiveness | 0.112 | 0.083 | 0.092 | 0.108 | **1.4x** |
| **Average** | **0.149** | 0.060 | 0.072 | 0.111 | **3.1x** |

Lewis 1.0 beats base LLaMA on 5/5 dimensions (3.1x avg).
Lewis 1.0 beats Claude Haiku on 5/5 dimensions (2.1x avg).
Lewis 1.0 beats Claude Sonnet on 4/5 dimensions (1.3x avg).

---

## Lewis 1.5 Training Details

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

**Methodology:** [METHODOLOGY.md](METHODOLOGY.md)
**Scoring rubric:** [eval/rubric.md](eval/rubric.md)
**Evaluation code:** [eval/evaluate.py](eval/evaluate.py)
