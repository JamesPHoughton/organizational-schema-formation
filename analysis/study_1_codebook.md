# Study 1 (Schema / Non-schema) — Data Codebook

This codebook documents the released data tables for Study 1. All tables are
produced by [`study_1_analysis.ipynb`](study_1_analysis.ipynb) from the raw
session logs in [`../data/study_1_schema_nonschema/`](../data/study_1_schema_nonschema/).

## Files

| File | Grain (unit of observation) | Rows | Purpose |
|------|------|------|---------|
| `study_1_participant_data.csv` | one row per **participant** | 140 | Canonical wide table: raw responses + timings + derived DVs + session metadata. Start here for secondary analysis. |
| `study_1_analysis_ready.csv` | one row per **game** (pair), post-exclusions | 66 | Trimmed modeling table (accuracy / time / score per stage) used for the reported analyses. |

The R4 label **coding** is *not* in these tables — see
[R4 label coding](#r4-label-coding) below.

## Unit of observation — read this first

Study 1 is a **dyadic** design. Participants completed the task in **two-person
games (pairs)**:

- `study_1_participant_data.csv` has **140 participants** nested in **70 games**
  (`position` 0 or 1 within each game).
- **Treatment is assigned at the game level** — both partners in a game are in
  the same condition (`schema` or `nonschema`). It is *not* independently
  randomized per participant.
- Several derived measures (`accuracy_*`) are defined at the **pair level** and
  are therefore **identical for both partners** in a game.

Practical implication: observations are **not independent**. Analyses that treat
participants as independent will understate standard errors. **Cluster on
`gameId`** (or analyze at the game level, as `study_1_analysis_ready.csv` does).

## `study_1_participant_data.csv` — column dictionary

### Identifiers & design
| Column | Type | Description |
|--------|------|-------------|
| `treatment` | category | Condition: `schema` or `nonschema`. Assigned per game (both partners share it). |
| `sampleId` | string | Anonymized participant ID (UUID). Unique per row. |
| `gameId` | string | 6-character game (pair) ID. **Join / cluster key.** Two participants share a `gameId`. |
| `gameId_full` | string | Full-length game ID (`gameId` is its last 6 chars). |
| `position` | int | Slot within the pair: `0` or `1`. |

### Session & device metadata (browser / connection)
| Column | Type | Description |
|--------|------|-------------|
| `country` | category | Two-letter country code (geo-IP). *Quasi-identifier.* |
| `timezone` | category | IANA timezone (e.g., `America/Los_Angeles`). *Quasi-identifier.* |
| `isKnownVpn`, `isLikelyVpn` | bool | VPN-detection flags. |
| `effectiveType` | category | Network Information API connection class (e.g., `4g`). |
| `saveData` | bool | Browser data-saver mode on/off. |
| `downlink` | float | Estimated downlink bandwidth (Mbps). |
| `rtt` | float | Estimated network round-trip time (ms). |
| `screenWidth`, `screenHeight` | int | Physical screen size (px). |
| `width`, `height` | int | Browser viewport size (px). |
| `language` | category | Browser locale (e.g., `en-US`). |
| `device` | string | Parsed OS / browser (e.g., `Windows desktop / Chrome`). |

### Exit quality-control survey
| Column | Type | Description |
|--------|------|-------------|
| `participateAgain` | category | Would participate again (yes/no). |
| `adequateCompensation` | category | Perceived pay adequacy. |
| `adequateTime` | category | Perceived time adequacy. |
| `clearInstructions` | category | Instruction clarity. |
| `videoQuality` | float | Video-quality rating (1–5). |
| `joiningProblems` | category | Reported problems joining (yes/no). |
| `technicalProblems` | category | Reported technical problems (yes/no). |
| `technicalDetail` | free text | Open description of technical problems. Reviewed and retained (see [Privacy](#privacy--re-identification)). |
| `textExpansion` | free text | Open comment field. Reviewed and retained. |
| `joiningDetail` | free text | Open description of joining problems. Reviewed and retained. |
| `num_reports` | int | Number of reports the participant filed during the session. |

### Timing
| Column | Type | Description |
|--------|------|-------------|
| `time_labeling_1a` … `time_labeling_4` | float | Seconds to submit each labeling stage. **Missing values are filled with `300`** (the 5-minute per-stage cap). |

### Generated labels (raw text)
| Column | Type | Description |
|--------|------|-------------|
| `labeling_1a`, `labeling_1b`, `labeling_1c`, `labeling_2`, `labeling_3`, `labeling_4` | free text | The label text the pair generated at each stage. Multi-line (one line per image). |

### Recall responses (raw, per slot)
| Column | Type | Description |
|--------|------|-------------|
| `recall_{round}_{slot}` | string | The item the participant recalled in a given slot, lower-cased and stripped; empty string = blank. **38 columns.** Slots are 0-indexed. Item counts per round: `1a`=2, `1b`=4, `1c`=8, `2`=8, `3`=8, `4`=8. |
| `empty_recall_counts` | int | Number of blank recall slots for the participant. |

### Derived dependent variables
| Column | Type | Description |
|--------|------|-------------|
| `accuracy_1a` … `accuracy_4` | float | **Pair-level coordination score** for the stage: the number of items both partners recalled identically (0–8; "points" counted on distinct labels). Identical for both partners in a game. Exact definition in the notebook `[load-data]` cell. |

**Dropped scaffolding.** Earlier revisions of this table also carried
`treatmentGroup` (an exact duplicate of `treatment`) and per-slot
`match_*` / `matched_recall_*` columns. These were **intermediate scoring
artifacts**, fully reproducible from `recall_*` plus the answer key, so they are
excluded from the release to keep the table legible. Re-derive them from the
notebook if needed.

## `study_1_analysis_ready.csv`

Per-game modeling table after exclusions (66 games). Columns: `treatment`,
`gameId`, and per-stage `accuracy_*`, `time_labeling_*`, and `score_*`. This is
the table behind the reported statistical tests; see `study_1_analysis.ipynb`
for the exclusion criteria that take the sample from 70 games to 66.

## R4 label coding

The round-4 labels were separately hand-coded (adaptation category, schema use,
generation-vs-memory). That coding is **kept out of the wide participant table
on purpose** — it is at a different grain (per game, some of it per game × round,
some schema-only) and it is interpretive rather than observed. The primary coding
artifacts are the per-label annotation files (one per participant × label) in
[`../annotation/r4_label_coding/`](../annotation/r4_label_coding/), each with a
`.sidecar.json` recording its provenance. To attach coding to this data, join on
`gameId` (+ `position` where the code is per-participant).

## Privacy & re-identification

This data was screened for personally identifying information prior to release.
The fields below were reviewed and **deliberately retained**; the residual
re-identification risk is considered negligible.

- **Quasi-identifiers** (`country`, `timezone`, `device`, screen resolution) are
  retained. Each attribute value is shared by a large number of participants, so
  no combination isolates an individual (large equivalence classes).
- **Free-text fields** (`technicalDetail`, `textExpansion`, `joiningDetail`) were
  reviewed and judged non-identifying (brief task/technical remarks) and are
  retained as written.
- `sampleId` / `gameId` are random identifiers with no link to platform worker
  IDs.
