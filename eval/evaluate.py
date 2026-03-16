#!/usr/bin/env python3
"""
Lewis 1.0 — Personality Divergence Benchmark
=============================================
Evaluates whether a fine-tuned model produces measurably distinct and
consistent personality responses compared to a baseline model.

Usage:
  # Step 1: Generate responses from a model
  python evaluate.py generate --model <openrouter-model-id> --agents <agent_system_prompts.json>

  # Step 2: Score responses using LLM judge (Claude Sonnet)
  python evaluate.py score --input responses.jsonl

  # Step 3: Compute divergence metrics
  python evaluate.py metrics --input scored.jsonl

  # Run all steps
  python evaluate.py run --model <model-id> --agents <agents.json>

Requirements:
  pip install openai numpy scipy pandas tqdm
  OPENROUTER_API_KEY environment variable must be set.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np

try:
    from openai import OpenAI
    import pandas as pd
    from scipy.spatial.distance import cosine
    from tqdm import tqdm
except ImportError:
    print("Missing dependencies. Run: pip install openai numpy scipy pandas tqdm")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
JUDGE_MODEL = "anthropic/claude-haiku-4.5"   # cost-efficient judge; swap to sonnet for higher fidelity
PROMPTS_FILE = Path(__file__).parent / "prompts.json"

DIMENSION_WEIGHTS = {
    "skepticism": 1.5,
    "assertiveness": 1.5,
    "emotional_valence": 1.0,
    "abstraction": 1.0,
    "verbosity": 0.5,
}
WEIGHT_SUM = sum(DIMENSION_WEIGHTS.values())  # 6.5

JUDGE_SYSTEM = """You are an objective personality analyst scoring AI-generated responses.
Score the following response on exactly 5 dimensions using the rubric provided.
Return ONLY a valid JSON object with no explanation:
{"skepticism": N, "verbosity": N, "emotional_valence": N, "abstraction": N, "assertiveness": N}
where N is an integer from 1 to 5."""

JUDGE_RUBRIC = """
Skepticism (1-5):
  1=fully agreeable/accepts all premises
  2=mildly accepting, acknowledges counterpoints
  3=neutral
  4=skeptical, questions at least one assumption
  5=deeply skeptical, challenges the framing itself

Verbosity (1-5):
  1=<30 words (extremely terse)
  2=30-80 words (brief)
  3=80-150 words (moderate)
  4=150-250 words (verbose)
  5=250+ words (very verbose)

Emotional Valence (1-5):
  1=strongly negative/cynical/anxious
  2=mildly negative/cautious
  3=neutral/analytical
  4=mildly positive/optimistic
  5=strongly positive/enthusiastic

Abstraction Level (1-5):
  1=purely abstract, only concepts/frameworks
  2=mostly abstract with occasional examples
  3=mixed, balances abstract and concrete
  4=mostly concrete, specific examples/data
  5=purely concrete, anecdotal/case-by-case

Assertiveness (1-5):
  1=highly deferential, hedges everything
  2=tentative, qualifies heavily
  3=moderate, states view but acknowledges complexity
  4=direct, clear position with minimal hedging
  5=blunt, strong stance, dismisses alternatives
"""


# ─────────────────────────────────────────────────────────────────────────────
# API client
# ─────────────────────────────────────────────────────────────────────────────

def get_client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("Error: OPENROUTER_API_KEY not set.")
        sys.exit(1)
    return OpenAI(api_key=key, base_url=OPENROUTER_BASE)


def call_model(
    client: OpenAI,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 512,
    retries: int = 3,
) -> Optional[str]:
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  API error after {retries} attempts: {e}")
                return None


# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Generate responses
# ─────────────────────────────────────────────────────────────────────────────

def generate_responses(model: str, agents_file: str, output_file: str, num_prompts: int = 50):
    """
    Run all prompts through each agent and save responses.
    agents_file: JSON array of {"agent_id": str, "system_prompt": str}
    """
    client = get_client()
    prompts = json.loads(PROMPTS_FILE.read_text())[:num_prompts]

    with open(agents_file) as f:
        agents = json.load(f)

    out = open(output_file, "w")
    total = len(agents) * len(prompts)

    print(f"Generating {total} responses ({len(agents)} agents × {len(prompts)} prompts)...")

    with tqdm(total=total) as pbar:
        for agent in agents:
            for prompt_obj in prompts:
                response = call_model(
                    client,
                    model=model,
                    system=agent["system_prompt"],
                    user=prompt_obj["prompt"],
                )
                if response:
                    record = {
                        "agent_id": agent["agent_id"],
                        "prompt_id": prompt_obj["id"],
                        "prompt": prompt_obj["prompt"],
                        "category": prompt_obj["category"],
                        "response": response,
                        "model": model,
                    }
                    out.write(json.dumps(record) + "\n")
                pbar.update(1)
                time.sleep(0.1)  # light rate limiting

    out.close()
    print(f"Saved to {output_file}")


# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Score responses with LLM judge
# ─────────────────────────────────────────────────────────────────────────────

def score_responses(input_file: str, output_file: str, batch_size: int = 10):
    """
    Score each response on 5 personality dimensions using Claude as judge.
    Processes in batches to avoid context bleed.
    """
    client = get_client()

    records = [json.loads(line) for line in open(input_file)]
    out = open(output_file, "w")
    failed = 0

    print(f"Scoring {len(records)} responses (batches of {batch_size})...")

    for i, record in enumerate(tqdm(records)):
        user_msg = f"""{JUDGE_RUBRIC}

RESPONSE TO SCORE:
\"\"\"{record['response']}\"\"\"

Return only the JSON object."""

        raw = call_model(client, JUDGE_MODEL, JUDGE_SYSTEM, user_msg, max_tokens=100)

        scores = None
        if raw:
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3].strip()
            try:
                scores = json.loads(raw)
                # Validate keys and range
                expected = set(DIMENSION_WEIGHTS.keys())
                if not expected.issubset(scores.keys()):
                    scores = None
                else:
                    for k in expected:
                        scores[k] = max(1, min(5, int(scores[k])))
            except (json.JSONDecodeError, ValueError, KeyError):
                scores = None

        if scores is None:
            failed += 1
            if failed > len(records) * 0.05:
                print(f"Warning: {failed} scoring failures so far. Check API key / model.")
            continue

        # Compute weighted composite score
        weighted = sum(scores[dim] * w for dim, w in DIMENSION_WEIGHTS.items()) / WEIGHT_SUM

        out.write(json.dumps({**record, "scores": scores, "weighted_score": round(weighted, 4)}) + "\n")

        # Small delay between batches
        if (i + 1) % batch_size == 0:
            time.sleep(0.5)

    out.close()
    print(f"Scored {len(records) - failed}/{len(records)} responses → {output_file}")
    if failed:
        print(f"  {failed} records discarded (judge parse failures)")


# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Compute metrics
# ─────────────────────────────────────────────────────────────────────────────

def compute_metrics(input_file: str, baseline_file: Optional[str] = None):
    """
    Compute personality divergence metrics.

    Key metrics:
    - Within-agent variance: std dev of scores per agent across all prompts
      Low = consistent personality (what Lewis 1.0 should show)
    - Cross-agent variance: std dev of mean scores across all agents
      High = distinct personalities (the divergence claim)
    """
    records = [json.loads(line) for line in open(input_file) if "scores" in line]
    df = pd.DataFrame(records)
    df_scores = pd.json_normalize(df["scores"])
    df = pd.concat([df.drop(columns=["scores"]), df_scores], axis=1)

    dims = list(DIMENSION_WEIGHTS.keys())
    print(f"\n{'='*60}")
    print(f"LEWIS 1.0 BENCHMARK RESULTS")
    print(f"{'='*60}")
    print(f"Agents: {df['agent_id'].nunique()}")
    print(f"Prompts per agent: {df.groupby('agent_id')['prompt_id'].nunique().mean():.1f}")
    print(f"Total scored responses: {len(df)}")

    # ── Within-agent variance ──────────────────────────────────────────────
    print(f"\n── Within-Agent Variance (lower = more consistent personality) ──")
    within_vars = []
    for agent_id, group in df.groupby("agent_id"):
        agent_var = group[dims].std().mean()
        within_vars.append(agent_var)
    mean_within = np.mean(within_vars)
    print(f"  Mean within-agent std dev: {mean_within:.4f}")

    # ── Cross-agent variance ───────────────────────────────────────────────
    print(f"\n── Cross-Agent Variance (higher = more distinct personalities) ──")
    agent_means = df.groupby("agent_id")[dims].mean()
    cross_var = agent_means.std().mean()
    print(f"  Cross-agent std dev of mean scores: {cross_var:.4f}")

    # ── Per-dimension summary ──────────────────────────────────────────────
    print(f"\n── Per-Dimension Mean Scores ──")
    print(f"  {'Dimension':<22} {'Mean':>6} {'Std Dev':>8} {'Min':>6} {'Max':>6}")
    print(f"  {'-'*52}")
    for dim in dims:
        print(f"  {dim:<22} {df[dim].mean():>6.2f} {df[dim].std():>8.4f} {df[dim].min():>6} {df[dim].max():>6}")

    # ── Weighted score distribution ────────────────────────────────────────
    print(f"\n── Weighted Score Distribution ──")
    print(f"  Mean: {df['weighted_score'].mean():.4f}")
    print(f"  Std:  {df['weighted_score'].std():.4f}")
    print(f"  Min:  {df['weighted_score'].min():.4f}")
    print(f"  Max:  {df['weighted_score'].max():.4f}")

    # ── Baseline comparison ────────────────────────────────────────────────
    if baseline_file:
        base_records = [json.loads(l) for l in open(baseline_file) if "scores" in l]
        df_base = pd.DataFrame(base_records)
        df_base_scores = pd.json_normalize(df_base["scores"])
        df_base = pd.concat([df_base.drop(columns=["scores"]), df_base_scores], axis=1)

        base_within_vars = []
        for agent_id, group in df_base.groupby("agent_id"):
            base_within_vars.append(group[dims].std().mean())
        mean_base_within = np.mean(base_within_vars)

        base_cross = df_base.groupby("agent_id")[dims].mean().std().mean()

        print(f"\n── Baseline Comparison ──")
        print(f"  {'Metric':<40} {'Lewis':>8} {'Baseline':>10} {'Ratio':>8}")
        print(f"  {'-'*68}")
        ratio_within = mean_within / mean_base_within if mean_base_within > 0 else float("nan")
        ratio_cross = cross_var / base_cross if base_cross > 0 else float("nan")
        print(f"  {'Within-agent variance':<40} {mean_within:>8.4f} {mean_base_within:>10.4f} {ratio_within:>8.3f}x")
        print(f"  {'Cross-agent variance':<40} {cross_var:>8.4f} {base_cross:>10.4f} {ratio_cross:>8.3f}x")

        print(f"\n── Pass/Fail ──")
        within_pass = mean_within <= mean_base_within * 0.60
        cross_pass = cross_var >= base_cross * 1.20
        print(f"  Within-agent consistency (need ≤60% of baseline): {'PASS ✓' if within_pass else 'FAIL ✗'}")
        print(f"  Cross-agent distinctness (need ≥120% of baseline): {'PASS ✓' if cross_pass else 'FAIL ✗'}")
        if within_pass and cross_pass:
            print(f"\n  → FULL PASS: Agents are consistent AND distinct from each other.")
        elif within_pass:
            print(f"\n  → PARTIAL PASS: Agents are consistent but not sufficiently distinct.")
        else:
            print(f"\n  → FAIL: Fine-tune did not produce stable personality signatures.")

    print(f"\n{'='*60}\n")

    # Save summary JSON
    summary = {
        "total_agents": int(df["agent_id"].nunique()),
        "total_responses": len(df),
        "mean_within_agent_variance": round(float(mean_within), 6),
        "mean_cross_agent_variance": round(float(cross_var), 6),
        "weighted_score_mean": round(float(df["weighted_score"].mean()), 6),
        "weighted_score_std": round(float(df["weighted_score"].std()), 6),
        "per_dimension": {
            dim: {
                "mean": round(float(df[dim].mean()), 4),
                "std": round(float(df[dim].std()), 4),
            }
            for dim in dims
        },
    }
    out_path = Path(input_file).parent / "metrics_summary.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"Summary saved to {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Lewis 1.0 personality divergence benchmark")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Generate model responses to prompts")
    gen.add_argument("--model", required=True, help="OpenRouter model ID")
    gen.add_argument("--agents", required=True, help="Path to agents JSON file")
    gen.add_argument("--output", default="responses.jsonl")
    gen.add_argument("--prompts", type=int, default=50, help="Number of prompts (1-50)")

    score = sub.add_parser("score", help="Score responses with LLM judge")
    score.add_argument("--input", required=True, help="Path to responses JSONL")
    score.add_argument("--output", default="scored.jsonl")

    metrics = sub.add_parser("metrics", help="Compute divergence metrics")
    metrics.add_argument("--input", required=True, help="Path to scored JSONL")
    metrics.add_argument("--baseline", default=None, help="Optional baseline scored JSONL for comparison")

    args = parser.parse_args()

    if args.command == "generate":
        generate_responses(args.model, args.agents, args.output, args.prompts)
    elif args.command == "score":
        score_responses(args.input, args.output)
    elif args.command == "metrics":
        compute_metrics(args.input, args.baseline)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
