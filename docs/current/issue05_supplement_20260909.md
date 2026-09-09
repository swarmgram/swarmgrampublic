# Issue 05 supplement (post-output)

**Published:** The Lewsearch Report Issue 05 is live. The primary forecast remains ICS 55.4.

**Dated:** September 9, 2026, after synthetic August and September outputs were on disk, and after an independent CPU reproduction. Before Friday’s Michigan preliminary (September 11, 10:00 a.m. ET).

**Status:** Companion memo. The original pre-registration is immutable.

Public protocol: [issue05_prereg_20260909.md](https://github.com/swarmgram/swarmgrampublic/blob/1c0b054cbfa6506aea6eee9c96a72ea41df87b93/docs/current/issue05_prereg_20260909.md), SHA `1c0b054cbfa6506aea6eee9c96a72ea41df87b93`. That commit froze the recipe. It did not freeze or publish 55.4.

Primary forecast remains **ICS 55.4** (ICC 61.8, ICE 51.4). Do not treat whichever companion is closer on Friday as “our prediction.”

## What was added after seeing the outputs

These calculations used existing raw cells. No new Lewis inference. No GPU job.

### August-anchored nowcast: 52.1

Formula locked in this memo, not in the original prereg:

`ICS_nowcast = ICS_Sep_full + (51.7 − ICS_Aug_full)`

= 55.43556647621303 + (51.7 − 54.991503596909325)

= **52.14406287930371**, one decimal **52.1**.

The original registration banned a nowcast as the lead. This number was added after seeing synthetic August and September, and before Friday’s human print. Exploratory companion only.

### No-floor verbalized aggregates

Same cells, skip the clip-then-renorm floor.

| Wave | ICS | ICC | ICE | x |
|---|---:|---:|---:|---|
| August no-floor | 54.8 | 60.7 | 51.1 | 77, 81, 62, 59, 78 |
| September no-floor | 55.4 | 61.8 | 51.4 | 78, 82, 63, 58, 80 |

September’s published relatives did not move when the floor was removed. August DUR relative moved from 79 to 78, so August ICS moved from 55.0 to 54.8. Post-output sensitivity only.

### Argmax aggregation

Each persona’s vector is reduced to its modal option. Ties split evenly. No floor. Internal diagnostic, not a forecast.

| Wave | ICS | ICC | ICE | x |
|---|---:|---:|---:|---|
| August argmax | 51.4 | 58.8 | 46.7 | 75, 76, 54, 54, 75 |
| September argmax | 52.6 | 60.7 | 47.5 | 76, 78, 56, 53, 79 |

### Finite-roster bootstrap

2,000 within-state resamples of the frozen 1,000-row roster, both dates, all five items. This is finite-roster sensitivity, not a margin of error.

September ICS full: 2.5th 54.10, median 55.58, 97.5th 57.06.

August to September move full: 2.5th −0.30, median +0.44, 97.5th +1.18.

## CPU reproduction

Second implementation (`eval/issue05_michigan/reproduce_independent_20260909.py`) did not import the scoring path in `algebra.py`. It matched:

- 5,000 / 5,000 valid cells each wave, full roster membership, zero permutation-decode mismatches
- original-option means after reversing stored permutations
- single aggregate floor, ε=0.03 clip-then-renorm
- unrounded F minus U balances
- five integer relatives and ICS / ICC / ICE to one decimal

**PASS.** Lead stays 55.4.

## Parser compliance (what the files can support)

Successful completions stored `text=null`. Complete keys, unexpected keys, omitted keys, and token-limit cuts cannot be reconstructed.

| Wave | Valid under parser | First-try ok | Retries | Presented not exact hundredths |
|---|---:|---:|---:|---:|
| August | 5000 | 4930 | 70 | 735 |
| September | 5000 | 4942 | 58 | 757 |

“5000/5000 valid under parser” is not “every completion followed the contract.”

## Hashes

- Registration: `1c0b054cbfa6506aea6eee9c96a72ea41df87b93`
- Roster: `e16e31518c1546d4b4b4ca8618aed217aa0232b0f14deeb071c3dd00f793b524`
- August cells: `b500dbd826718d1c10ece28091c337286840120318ee1184a5f946ba5da7779b`
- September cells: `523c04b069e81f66b0d97e9fc3cc0e54dbca60c1ff2273a0b5c05c00ccb7b8e5`
- Runner: `f06ca50ec6866d98d5e77baa1cb8e97e7327b687a733f6b157aee2dad3a5ceac`

## Hardware

Pod `px6lldqc2inp48` deleted. GET /pods empty. Volume `o9x1gw85my` retained. Volume `2d4ef4kh4w` not attached and not deleted. No new Lewis inference.
