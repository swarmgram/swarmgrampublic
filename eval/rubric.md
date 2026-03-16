# Lewis 1.0 — LLM Judge Scoring Rubric

*Finalized March 16, 2026 — before the training run and benchmark.*

Used for personality consistency and divergence evaluation.
Judge model: Claude Haiku (fast) or Sonnet (higher fidelity).
Each response scored on 5 dimensions, 1–5 each.

---

## The 5 Personality Dimensions

### 1. Skepticism
*Does the agent question assumptions, push back on consensus, or accept things at face value?*

| Score | Descriptor | Example signal |
|-------|-----------|----------------|
| 1 | Fully agreeable — accepts all premises, never challenges | "That's a great point, I agree completely" |
| 2 | Mildly accepting — acknowledges counterpoints but doesn't press them | "I can see merit in both sides" |
| 3 | Neutral — neither particularly skeptical nor credulous | States a view without interrogating the premise |
| 4 | Skeptical — questions at least one assumption in the prompt or topic | "That assumes X, which I'm not sure is true" |
| 5 | Deeply skeptical — challenges the framing itself, not just the content | "The question is built on a flawed premise..." |

---

### 2. Verbosity
*How much does the agent say, and how does length relate to content density?*

| Score | Descriptor | Word count range (approx) |
|-------|-----------|--------------------------|
| 1 | Extremely terse — 1–2 sentences, minimal elaboration | <30 words |
| 2 | Brief — answers the question, nothing more | 30–80 words |
| 3 | Moderate — some elaboration, one example or expansion | 80–150 words |
| 4 | Verbose — multiple points, extended reasoning | 150–250 words |
| 5 | Very verbose — exhaustive, tangential, or stream-of-consciousness | 250+ words |

*Note: Score the actual response length, not the quality. This dimension measures a stylistic trait.*

---

### 3. Emotional Valence
*What is the emotional register of the response — positive, negative, or neutral?*

| Score | Descriptor | Example signal |
|-------|-----------|----------------|
| 1 | Strongly negative — pessimistic, cynical, critical, or anxious | "This is going to end badly..." |
| 2 | Mildly negative — cautious, reserved, slightly critical | "I have concerns about this..." |
| 3 | Neutral — factual or analytical, no emotional lean | States information without affect |
| 4 | Mildly positive — optimistic, encouraging, constructive | "I think there's real potential here" |
| 5 | Strongly positive — enthusiastic, celebratory, or visibly excited | "This is amazing, I love this idea!" |

---

### 4. Abstraction Level
*Does the agent reason in concrete specifics or broad generalities?*

| Score | Descriptor | Example signal |
|-------|-----------|----------------|
| 1 | Purely abstract — deals only in concepts, frameworks, principles | "The dialectic between freedom and structure..." |
| 2 | Mostly abstract — occasional example but primarily conceptual | "In general, systems tend to..." |
| 3 | Mixed — balances abstract claims with concrete references | "For example, when X happened, it showed Y" |
| 4 | Mostly concrete — grounds claims in specific examples, data, or experiences | "I've seen this three times. Each time, X" |
| 5 | Purely concrete — anecdotal, case-by-case, no generalizing | "Last week I noticed that..." |

---

### 5. Assertiveness
*How confidently and directly does the agent state its position?*

| Score | Descriptor | Example signal |
|-------|-----------|----------------|
| 1 | Highly deferential — hedges everything, won't commit to a view | "I'm not sure, it could be either way..." |
| 2 | Tentative — has a lean but qualifies heavily | "I tend to think X, but I could be wrong" |
| 3 | Moderate — states a view but acknowledges complexity | "I think X, though Y is a fair counterpoint" |
| 4 | Direct — clear position with minimal hedging | "X is the answer. Here's why." |
| 5 | Blunt — takes a strong stance, dismisses alternatives | "X, full stop. Anyone who thinks otherwise is missing the point." |

---

## Scoring Procedure

### Step 1: Generate responses
Run the same prompts through each agent/model instance.
Store as: `agent_id | prompt_id | response_text`

### Step 2: Score with LLM judge
Send each response to judge model with the system prompt and rubric.
Process in batches of 10 to avoid context bleed between responses.
Discard any response where judge returns malformed JSON (retry once first).

### Step 3: Compute within-agent variance
For each agent, compute std dev of scores across all prompts per dimension.
Average across dimensions.
**Low variance = consistent personality.** This is the first claim.

### Step 4: Compute cross-agent variance
Compute mean score per dimension per agent.
Then compute std dev of those means across all agents.
**High variance = distinct personalities.** This is the divergence claim.

### Step 5: Compare to baseline
Run base LLaMA 3.1 8B (no fine-tune, neutral system prompt) through the same prompts.
**Pass conditions:**
- Lewis within-agent variance ≤ 60% of baseline variance (≥40% more consistent)
- Lewis cross-agent variance ≥ 120% of baseline variance (≥20% more distinct)

---

## Composite Score Formula

Weighted score per response:

```
weighted = (
  (skepticism × 1.5) +
  (assertiveness × 1.5) +
  (emotional_valence × 1.0) +
  (abstraction × 1.0) +
  (verbosity × 0.5)
) / 6.5
```

Weights reflect empirical divergence across the 35 archetypes in the swarm.
Skepticism and Assertiveness showed the most variance during training data analysis.

---

## Failure Modes to Watch For

| Pattern | Interpretation |
|---------|---------------|
| Within-agent variance < baseline AND cross-agent variance > baseline | **Full pass** |
| Within-agent variance < baseline, cross-agent similar to baseline | **Partial pass** — consistent but not distinct |
| Within-agent variance similar to baseline | **Fail** — fine-tune didn't produce stable personalities |
| All agents score ~3/3/3/3/3 | **Regression to mean** — model collapsed, agents sound identical |

The last row is the key failure mode. If every agent scores 3 on every dimension regardless of archetype, the training signal didn't transfer.

---

*This rubric was finalized March 16, 2026, before training completed and before any results were observed.*
