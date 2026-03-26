# Lewis — Pew Research Benchmark Results

Validation of Lewis models against published Pew Research Center survey distributions.
MAE measures the average gap between Lewis agent opinion distributions and real-world
Pew polling data across 63 questions covering government, economy, immigration, race,
healthcare, climate, Ohio-specific issues, and social topics.

---

## Pre-Calibration Baseline: Lewis 2.0 (Social Behavior Model)

**Date:** March 26, 2026
**Model:** Lewis 2.0 social behavior base — trained on agent simulation data
(posts, conversations, memory narratives, personality expression). No survey-specific training.

| Metric | Result |
|---|---|
| Questions scored | 63 |
| Overall MAE | 0.3263 (target: <0.05) |
| Pass rate | 0% of questions within 5pts |
| Valid responses | 60,513 / 117,000 (51.7%) |
| Survey-calibrated | NO — pre-calibration baseline |

### Per-Question Breakdown (10 Highest MAE)

| Question ID | MAE | Topic |
|---|---|---|
| china_threat_01 | 0.573 | Do you consider China to be an adversary, a competitor, or a... |
| climate_real_01 | 0.560 | From what you've read and heard, is there solid evidence of climate change... |
| ohio_direction_01 | 0.540 | Overall, do you think Ohio is headed in the right direction |
| econ_inequality_01 | 0.476 | Do you think the economic system in this country unfairly favors... |
| climate_priority_01 | 0.476 | Which should be the higher priority for the country's energy policy... |
| ohio_opioid_01 | 0.475 | How important is addressing the opioid and fentanyl crisis... |
| ohio_third_frontier_01 | 0.474 | How important is it for Ohio to invest in technology, biotech... |
| foreign_aid_01 | 0.461 | Generally speaking, do you think it is best for the future of... |
| ohio_housing_01 | 0.461 | How serious of a problem is housing affordability in your community... |
| race_system_01 | 0.456 | Which statement comes closer to your view? The country has made... |

### Interpretation

This baseline was measured on the social behavior model before survey calibration.
The model was trained to generate human-like social media posts, hold persistent opinions,
and maintain personality across interactions — not to answer constrained survey questions
in a structured format. An MAE of 0.3263 with 0% pass rate is the expected result for
an uncalibrated social behavior model. This is the controlled baseline for measuring
the impact of survey fine-tuning.

---

## Post-Calibration: Lewis 2.0 (Survey Fine-Tuned)

**Date:** March 26, 2026
**Status:** Training in progress — ETA ~4 hours from baseline run.

| Metric | Result |
|---|---|
| Questions scored | — |
| Overall MAE | PENDING |
| Pass rate | PENDING |
| Valid responses | PENDING |
| Survey-calibrated | PENDING |

### Target Improvement

| Metric | Pre-calibration | Target (post-calibration) |
|---|---|---|
| Overall MAE | 0.3263 | <0.05 |
| Pass rate | 0% | >60% |
| Valid response rate | 51.7% | >80% |

---

## Methodology

- **Population:** 1,000 Ohio agents drawn from a swarm of 19,731 autonomous agents with
  persistent memory, inherited personality traits, and demographic grounding (age, gender,
  race, education, occupation, political leaning, Ohio state legislative district)
- **Survey pipeline:** 63 questions with published Pew benchmarks, administered to all agents
  via the Lewis inference API (vLLM, localhost)
- **Scoring:** Per-question MAE between agent response distribution and published
  Pew Research Center distribution for matched demographics
- **Pass threshold:** MAE < 0.05 (within 5 percentage points of real poll)
- **Valid response filter:** Responses that match a survey option string exactly;
  verbose or malformed outputs are excluded
- **Source code:** https://github.com/swarmgram/swarmgrampublic

---

## Changelog

| Date | Event |
|---|---|
| 2026-03-26 | Pre-calibration baseline recorded: MAE 0.3263, 0% pass (social model, no survey training) |
| 2026-03-26 | Survey fine-tuning started on 60,513 Ohio agent response pairs |
| 2026-03-26 | Post-calibration benchmark — PENDING |
