# Issue 05 pre-registration — University of Michigan Consumer Sentiment

**Protocol frozen. No synthetic Michigan responses generated yet.**

| | |
|---|---|
| Study | Lewsearch Report Issue 05 |
| Protocol date | **September 9, 2026** |
| Written (ET) | 2026-09-08 23:58:23 America/New_York |
| Written (UTC) | 2026-09-09 03:58:23Z |
| Public freeze | this file, committed and pushed to [swarmgram/swarmgrampublic](https://github.com/swarmgram/swarmgrampublic) |
| Status at freeze | Registration only. Lewis has not been asked any Michigan index question for this Issue. The prediction page is not published. |

This document locks the recipe before the first August or September cell is generated. Later commits may add artifacts, hashes of a frozen roster, and serving metadata. They may not change the recipe below.

---

## 1. What this is

A prospective public audit of one synthetic panel against one named human release.

We will administer **Michigan’s published index questions and algebra, through a synthetic adaptation**, to 1,000 census-grounded adult personas, freeze the resulting indexes, and score them against the University of Michigan Surveys of Consumers **September 2026 preliminary** print.

This is **not** a claim that we reproduced the Michigan survey. Michigan has used web interviewing since July 2024. A preliminary typically uses about 420 completed interviews; a final about 1,000. The human universe is the 48 coterminous states and D.C. Our stems, closed options, sample, and mode are a disclosed adaptation of that published instrument.

Official sources used at lock (do not silently replace):

- Index stems and algebra: https://data.sca.isr.umich.edu/fetchdoc.php?docid=24770
- 2026 release calendar: https://data.sca.isr.umich.edu/fetchdoc.php?docid=79628
- 2026 interview dates: https://data.sca.isr.umich.edu/fetchdoc.php?docid=79629
- Technical note on web mode (July 2024–): https://data.sca.isr.umich.edu/fetchdoc.php?docid=75437
- FAQ (prelim ~420 / final ~1,000; 48 + D.C.): https://data.sca.isr.umich.edu/faq.php
- Homepage / latest print: https://www.sca.isr.umich.edu/

Do **not** use docid 75442 as the 2026 interview calendar.

---

## 2. Calendar and targets

| Event | Official 2026 date |
|---|---|
| September interviewing begins | Tuesday, August 25 |
| Preliminary interviewing ends | Monday, September 7 |
| **Primary Y: September preliminary release** | **Friday, September 11, 10:00 a.m. ET** |
| September interviewing ends (final) | Monday, September 21 |
| September final release (secondary note only) | Friday, September 25 |

August interviewing for the **final** print ended Monday, August 24.

### August finals already public (qualification targets)

| Index | August 2026 final |
|---|---|
| ICS | **51.7** |
| ICC | **51.9** |
| ICE | **51.5** |

August preliminary (context only, not the gate): ICS 51.0, ICC 51.8, ICE 50.6.

---

## 3. Locked recipe

| Lever | Frozen value |
|---|---|
| Model | lewis-v17 (Gemma 4 26B-A4B MoE fine-tune; served merged FP8 on vLLM) |
| Weights volume | `o9x1gw85my` on US-CA-2 only |
| Elicitation | Verbalized JSON percentages (not letter logprobs) |
| Closer | Production `VERBALIZED_CLOSER` from `eval/replication_attack/run_arm.py` (hash below) |
| Floor | ε = 0.03, **clip-then-renorm**, once, on the equal-weight mean of valid persona vectors. Implementation = `applyFloorCalibration` in `lib/lewisInference.ts` |
| Calibrator | **Identity**. No Dirichlet / ODIR, no additive shift, no probability-temperature T tweak, no type-scale, no peek-adjust, no August-derived bias correction, no nowcast-as-lead |
| Decoding | Temperature 1.0, `max_tokens` 40, no logprobs. Record the exact serve flags from `scripts/H100_VLLM_QUICKSTART.md` (`--enforce-eager`, fp8, `--served-model-name lewis-v17`) |
| n | **1,000** unique adult personas |
| Roster | **One frozen roster**. Same 1,000 people on all five items and both datelines (10,000 scheduled cells; 5,000 per dateline) |
| Frame | **48 coterminous states + D.C.** Alaska and Hawaii **excluded**. D.C. **included** |
| Allocation | Hamilton largest-remainder on Census Vintage 2023 civilian 18+ (`ADULT_POP_2023`), after dropping AK and HI and **renormalizing** the remaining 49 jurisdictions. Same method as the YouGov concordance national sample minus AK/HI |
| Aggregation weights | **Equal weight** of the 1,000 roster members after allocation. No second population weight, no raking |
| Items | Five index questions only. Inflation (PX1 / PX5) **out** |
| BUS12 | Short four-way (Good / uncertain-mixed / bad / DK) |
| Primary endpoint | **ICS only** |
| Secondary | ICC and ICE. Mandatory audit: all five `x_i` and all option shares (A/B/C/D published separately) |
| August dateline | Method B, **August 24, 2026** (diagnostic / qualification) |
| September dateline | Method B, **September 7, 2026** (the forecast wave) |
| Method B meaning | An **instruction**, not a knowledge cutoff. The weights may still know later 2026. We do not claim respondents could not have seen later news |
| Live retrieval | Off. No news, no Michigan prints, no Street numbers in the persona prompt |
| Option permutation | Production `permuteOptions` (letter-position shuffle), then decode to original A–D before aggregation. Coding is always on original letters |
| Adaptive boosting | Forbidden. No extra batch after seeing either wave |

### Floor (clip-then-renorm)

Production function, hashed at freeze. `p` is the equal-weight mean share of a letter after valid cells are averaged (already a simplex). Then:

```
floored_k = max(p_k, 0.03)
p'_k = floored_k / sum(floored)
```

Not Dirichlet. Not an additive 0.03 shift. Not a mixture with uniform. After this step a bucket can be below 3% only if the renormalizer would require it; the operation is clip then divide by the new sum.

```
function applyFloorCalibration(counts: number[], total: number, eps = 0.03): number[] {
  if (total === 0) return counts.map(() => 0);
  const raw = counts.map(c => c / total);
  const floored = raw.map(p => Math.max(p, eps));
  const sum = floored.reduce((a, b) => a + b, 0);
  return floored.map(p => p / sum);
}
```

**SHA-256** of that function text (UTF-8, as it stood in `lib/lewisInference.ts` at freeze):

`2ce677892ddca337348c4466da207d3157470b087524bb28134272ab37db07a1`

Floor is applied **once**, to the roster-mean vector of each item, not to each persona and not a second time after index algebra.

### Verbalized closer (byte-identical)

```
Give the probability you would pick each option as percentages that sum to 100. Reply with one JSON object only, keys = the letters as presented, values = integers that sum to 100. You are this person, not a pollster. Example: {"A": 62, "B": 30, "C": 8}
```

**SHA-256:** `155de3c9a9fdfdfac9a326e60bb9550b15a42e3e066d67883a720f38ae674eff`

This worktree’s TypeScript `resolveScoringMode` is letters | logprobs only. Issue 05 implements verbalized in the Python runner (V50-style splice of this closer). That is a serving-path choice, not a recipe change.

### Method B dateline sentences (frozen)

August diagnostic:

> Today's date is August 24, 2026. Answer based on how you feel as of this date — not based on events after it.

September forecast:

> Today's date is September 7, 2026. Answer based on how you feel as of this date — not based on events after it.

Canonical factory: `lib/temporalContext.ts` `datelineFor()`.

---

## 4. Frame, Hamilton allocation, roster

Population source: U.S. Census Bureau, Population Estimates Program, Vintage 2023, file `SC-EST2023-AGESEX-CIV`, civilian resident population ages 18–85+ (`SEX=0`, `AGE` in 18..85, `POPEST2023_CIV`). Copied in `eval/yougov_concordance/_census_adult_pop.py` as `ADULT_POP_2023`.

Start from that 51-jurisdiction table (50 states + D.C.). **Drop AK and HI. Keep D.C. Renormalize.** Hamilton largest-remainder (`hamilton_allocate`) with leftover seats going to the largest fractional remainder, ties broken by larger population then USPS code.

**SHA-256** of `hamilton_allocate` as frozen in that file:

`9d80836dfa6b7301ae2c43c15b662661e42af9a268dc4a8676fcffa5e06cfe66`

Frame adult civilian population after drop: **259,381,271**. AK+HI were 1,637,477 (~0.63% of the 51-jurisdiction total). They are out of Michigan’s published universe and out of this study.

Roster seed: **20260909**. Within each jurisdiction, draw `n_i` personas without replacement from that jurisdiction’s `seed_pums_*` pool using `random.Random(20260909 + hash32("draw:" + USPS)).sample(pool, n_i)`, the same within-state draw as the YouGov concordance fielder. `hash32` is the FNV-1a implementation in `eval/state_pums/run_v3_50state_n1000.py`. Pool order is the Supabase `agent_id` order used by that fielder. The realized roster (agent ids, USPS, run_id) will be written to disk before any Michigan completion is requested and will not be replaced.

After allocation, every roster member has weight **1/1000**.

Frozen Hamilton seats for **n = 1,000**:

| USPS | Adult pop 2023 civ | Share of 48+DC | Quota | n |
|---|---:|---:|---:|---:|
| CA | 30,382,648 | 0.117135 | 117.1351 | 117 |
| TX | 22,830,131 | 0.088018 | 88.0177 | 88 |
| FL | 18,169,966 | 0.070051 | 70.0512 | 70 |
| NY | 15,592,010 | 0.060112 | 60.1123 | 60 |
| PA | 10,329,938 | 0.039825 | 39.8253 | 40 |
| IL | 9,827,372 | 0.037888 | 37.8877 | 38 |
| OH | 9,201,157 | 0.035473 | 35.4735 | 36 |
| GA | 8,433,848 | 0.032515 | 32.5153 | 33 |
| NC | 8,399,220 | 0.032382 | 32.3818 | 32 |
| MI | 7,923,446 | 0.030547 | 30.5475 | 31 |
| NJ | 7,273,191 | 0.028041 | 28.0405 | 28 |
| VA | 6,734,491 | 0.025964 | 25.9637 | 26 |
| WA | 6,116,015 | 0.023579 | 23.5792 | 24 |
| AZ | 5,831,020 | 0.022480 | 22.4805 | 23 |
| MA | 5,656,232 | 0.021807 | 21.8066 | 22 |
| TN | 5,536,083 | 0.021343 | 21.3434 | 21 |
| IN | 5,273,876 | 0.020333 | 20.3325 | 20 |
| MO | 4,806,973 | 0.018532 | 18.5325 | 19 |
| MD | 4,787,258 | 0.018456 | 18.4565 | 18 |
| WI | 4,660,450 | 0.017968 | 17.9676 | 18 |
| CO | 4,628,635 | 0.017845 | 17.8449 | 18 |
| MN | 4,436,369 | 0.017104 | 17.1037 | 17 |
| SC | 4,191,266 | 0.016159 | 16.1587 | 16 |
| AL | 3,966,537 | 0.015292 | 15.2923 | 15 |
| KY | 3,492,517 | 0.013465 | 13.4648 | 13 |
| LA | 3,491,906 | 0.013462 | 13.4624 | 13 |
| OR | 3,400,109 | 0.013109 | 13.1085 | 13 |
| OK | 3,068,908 | 0.011832 | 11.8316 | 12 |
| CT | 2,889,338 | 0.011139 | 11.1393 | 11 |
| NV | 2,496,089 | 0.009623 | 9.6232 | 10 |
| UT | 2,480,142 | 0.009562 | 9.5618 | 10 |
| IA | 2,476,590 | 0.009548 | 9.5481 | 10 |
| AR | 2,358,369 | 0.009092 | 9.0923 | 9 |
| MS | 2,247,247 | 0.008664 | 8.6639 | 9 |
| KS | 2,225,777 | 0.008581 | 8.5811 | 9 |
| NM | 1,649,613 | 0.006360 | 6.3598 | 6 |
| ID | 1,493,865 | 0.005759 | 5.7593 | 6 |
| NE | 1,490,917 | 0.005748 | 5.7480 | 6 |
| WV | 1,417,669 | 0.005466 | 5.4656 | 5 |
| NH | 1,149,457 | 0.004432 | 4.4315 | 4 |
| ME | 1,146,013 | 0.004418 | 4.4183 | 4 |
| MT | 893,832 | 0.003446 | 3.4460 | 3 |
| RI | 888,564 | 0.003426 | 3.4257 | 3 |
| DE | 816,505 | 0.003148 | 3.1479 | 3 |
| SD | 694,108 | 0.002676 | 2.6760 | 3 |
| ND | 591,991 | 0.002282 | 2.2823 | 2 |
| DC | 549,187 | 0.002117 | 2.1173 | 2 |
| VT | 532,679 | 0.002054 | 2.0537 | 2 |
| WY | 451,747 | 0.001742 | 1.7416 | 2 |
| **Sum** | **259,381,271** | **1.000000** | **1000** | **1000** |

AK = 0. HI = 0.

---

## 5. Instrument

Stems are verbatim from UM doc 24770. Options are the locked closed set (Astra §3 / advisor brief). **A = favorable, C = unfavorable, B and D = neutral** in the index algebra. **Publish B and D separately**; both are neutral in ICS/ICC/ICE.

### x1 PAGO

We are interested in how people are getting along financially these days. Would you say that you (and your family living there) are better off or worse off financially than you were a year ago?

- A. Better off financially
- B. About the same financially
- C. Worse off financially
- D. Uncertain / don't know

### x2 PEXP

Now looking ahead--do you think that a year from now you (and your family living there) will be better off financially, or worse off, or just about the same as now?

- A. Better off financially
- B. Just about the same financially
- C. Worse off financially
- D. Uncertain / don't know

### x3 BUS12 (short)

Now turning to business conditions in the country as a whole--do you think that during the next twelve months we'll have good times financially, or bad times, or what?

- A. Good times financially
- B. Uncertain / mixed
- C. Bad times financially
- D. Don't know

### x4 BUS5

Looking ahead, which would you say is more likely--that in the country as a whole we'll have continuous good times during the next five years or so, or that we will have periods of widespread unemployment or depression, or what?

- A. Continuous good times
- B. Uncertain / mixed
- C. Periods of widespread unemployment or depression
- D. Don't know

### x5 DUR

About the big things people buy for their homes--such as furniture, a refrigerator, stove, television, and things like that. Generally speaking, do you think now is a good or bad time for people to buy major household items?

- A. Good time to buy
- B. Uncertain / depends
- C. Bad time to buy
- D. Don't know

No extra text about August’s print, consumer sentiment, Lewsearch, Friday, Street, or the expected direction. Stems, locked options, verbalized closer, Method B dateline. Fresh context per persona × item × dateline. No conversation between personas. No previous answers in context.

Inflation questions are **not asked**.

---

## 6. Algebra

Let `q_{j,k}` be persona `j`’s probability on original letter `k` after decode (a simplex). Equal-weight mean across **valid** personas:

`p_k = (1/n_valid) Σ_j q_{j,k}`

Apply clip-then-renorm once → `p'`. Then:

```
F = 100 * p'_A
U = 100 * p'_C
x = floor(100 + F − U + 0.5)
```

Neutral mass (B and D, and any residual) **stays in the denominator**. Do not condition on having a directional opinion.

Then:

```
ICS = (x1 + x2 + x3 + x4 + x5) / 6.7558 + 2
ICC = (x1 + x5)                 / 2.6424 + 2
ICE = (x2 + x3 + x4)            / 4.1134 + 2
```

Archive full precision. **Published indexes are one decimal, half-up** (round half away from zero on the first unused decimal). Use that same release-scale number for the August gate and for Friday’s score.

Identity check (exact before display rounding):

```
ICS = (2.6424·ICC + 4.1134·ICE) / 6.7558
```

Independent algebra fixtures are required (balanced 50/50 → all `x_i = 100` and ICS ≈ 76.0; ICC/ICE membership; neutrals in the denominator; half-integer `x_i`; one-decimal half-up; floor once). **Do not invert August’s published totals as the only test.** Those three totals do not identify the five relatives.

---

## 7. August qualification (required) and September (always)

Both waves are locked **now**, before any Michigan completion exists.

1. Field August 24 on the frozen roster.
2. Compute release-scale ICS.
3. Gate: if `|ICS_Aug − 51.7| > 15`, this is a **failed-qualification prospective test**. Change the public title to say so. Equality at 15 **passes**.
4. **September is still fielded and still published**, including a valid print near 76. The gate changes the headline, not the existence of the forecast.
5. The gate does **not** authorize a new calibrator, a nowcast, or suppression of a valid September vector.

Passing the gate is a weak retrospective check against a number that is already public. It does not prove temporal blindness or forecast skill.

If August is a technical abort (section 9), stop and publish the technical-failure record. That is the only path that skips September.

---

## 8. Friday score, comparators, language

Primary error:

```
e = ICS_Sep_hat − ICS_UM_Sep_prelim
a = |e|
```

| Rule | Meaning |
|---|---|
| `a ≤ 5` | **Win** |
| `a > 5` | **Loss** |
| `5 < a ≤ 10` | miss (still a loss) |
| `10 < a ≤ 20` | bad miss |
| `a > 20` | embarrassing |

ICC and ICE get signed and absolute errors. They cannot rescue a failed ICS.

**Mandatory comparator:** naive repeat of August final ICS **51.7**. Report `|51.7 − ICS_UM_Sep_prelim|` next to Lewis’s `a`.

**Street comparator (optional, frozen Thursday):** Reuters median if posted by **Thursday, September 10, 23:59 ET**; else Bloomberg median if posted by that instant. Record source, statistic, URL, publication time, and retrieval time. Do not pick the source that flatters Lewis. If neither is posted by the deadline, Street is “not posted.”

Official Y remains Michigan. **No “we beat the Street” claim**, even if the arithmetic would support it.

### Copy constraints (locked)

- Say: “Michigan’s published index questions and algebra, administered through a synthetic adaptation.”
- Do **not** say we reproduced the Michigan survey.
- If the freeze clock is September 9, say **September 9**.
- Do not glue the April **7.47** figure to the **10.02** as-sold MAE. Prefer leaving 10.02 out of the lead.
- No ECHO. No KS&R ranks. No winner-call grades. No iPhone Pulse on this page or this run.
- No probability-sample claim. No human margin of error. No official PX1/PX5.

Default title if August qualifies:

**Issue 05: A Synthetic Estimate of September Consumer Sentiment, Frozen Before Michigan’s Release**

Default title if August fails the 15-point gate:

**Issue 05: Failed-Qualification Prospective Test of September Consumer Sentiment**

---

## 9. Technical failure policy

A **cell** is one (persona × item × dateline) completion. Each dateline has 5,000 cells.

- Parser: first valid JSON object whose letter keys yield a non-negative vector with at least one positive mass; renormalize to a simplex. Invalid JSON or transport failure: **two identical retries**, then the cell is **missing**.
- Keep the **first valid** vector. **Never retry a valid vector** because the distribution looks wrong, extreme, or flat.
- Do not substitute a new persona. Do not recode a refusal as DK. Do not soften BUS5.
- **Abort that dateline** (and do not compute its indexes) if missing cells **> 2% of 5,000** (more than 100 missing). Publish the abort.
- September is still attempted if August **completed** (including a failed qualification). September is not attempted if August **aborted**.
- No letter-logprob fallback. Missing stays missing.

---

## 10. Hardware and serving (after this commit)

- One H100. Datacenter **US-CA-2 only**. Volume **`o9x1gw85my`**. Never delete that volume. Never attach `2d4ef4kh4w`. Never override `dockerStartCmd`.
- If CA-2 is dry, **stop**. Do not fall through to IL / WA / MTL.
- After SSH: `/workspace/START_VLLM.sh` with `--enforce-eager`. Transformers **5.5.4** if `gemma4` is unregistered.
- Smoke `GET /v1/models` and one tiny chat completion **before** any Michigan cell.
- Kill the **pod** after artifacts are copied off. Never delete the volume.

---

## 11. What is frozen now vs later

Frozen **in this commit**, before any Michigan inference:

- Stems, option order, fav/unfav/neutral map
- n, frame, Hamilton table, roster seed and draw rule
- Elicitation, closer hash, floor hash and position, identity calibrator
- Both datelines and the Method B disclosure
- Algebra, rounding, endpoints, gate, score bands, comparators
- Retry / missing / abort rules
- Copy constraints

To be written to disk **after** this commit and **before** the first Michigan completion: the realized 1,000-row roster (agent ids + USPS + `seed_pums` run_id) and the serving pod id / model listing.

To be written after each wave: raw completions, option aggregates, `x_i`, ICS/ICC/ICE at full precision and one decimal, missing-cell counts, prompt hashes.

The Lewsearch `/report/issue5` page stays **local** until an explicit PUBLISH instruction. This public repo is the timing proof for the **protocol**, not yet for the numbers.

---

## 12. Claims we are not making

- That this is a probability sample of human Americans
- That Method B is an enforced cutoff
- That passing the August gate proves the model had not seen August’s print
- Official inflation medians
- Broad forecasting accuracy from one Friday
- That the historical poll-question MAE is an ICS error allowance
- Economist superiority, ECHO, or KS&R
- An iPhone or Apple-event result

---

## 13. Operator note

Jeffrey L. Mead authorized publishing this pre-registration on the night of September 8–9, 2026, dated September 9. Advisors and Astra designed; Jeffrey locked the overrides in this file (48+D.C. frame, September always publishes, clip-then-renorm floor, short BUS12, ICS-only primary, inflation out, win at ≤5 ICS points).

**No synthetic Michigan responses have been generated under this protocol as of the timestamps above.**
