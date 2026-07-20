# Organizational Schema Formation

Experimental paradigm, data, and analysis code for a research program studying
**competency traps** — how developing a successful strategy can become a
liability when the environment changes, even when adapting is in principle
possible. The project brings a phenomenon usually studied through
organizational case studies (Kodak, Nokia, Blockbuster) into a controlled
lab paradigm, so that cognitive and coordination mechanisms can be isolated
from the sunk costs, politics, and identity commitments that confound
real-world observation.

See [`docs/project_description.md`](docs/project_description.md) for the
full write-up (paradigm details, mechanism taxonomy, literature connections,
open questions). The summary below is just enough to navigate the repo.

## The task

Pairs of participants (dyads) play a collaborative image-labeling and recall
game across several rounds of different images. In each round, both partners
see a set of images and jointly assign each one a unique text label
(**labeling phase**), then independently try to recall which label went with
which image (**recall phase**). A pair's accuracy is the number of images
both partners label the same way.

Early rounds are constructed so that one group of participants (**Schema**
condition) discovers a compact, systematic labeling rule (e.g., a 3-part code
based on an image's color/position features), while another group
(**Non-Schema**) develops idiosyncratic, holistic labels. Both strategies
perform comparably on a shared middle round, with the schema condition taking
less time for players to coordinate. In the final round, the images
change in a way that breaks the schema's usefulness, and the question is how
each group adapts to this environmental change.

## Study 1: does the trap exist?

Schema groups are faster and at least as accurate as Non-Schema groups right
up until the schema-breaking round, where they significantly _underperform_
— establishing the competency trap as a real causal effect of having built a
schema-based strategy, not an artifact of selection, motivation, or
environment. A follow-up hand-coding of failure modes finds the dominant
pattern isn't groups failing to notice their schema broke (~14%) — it's
groups noticing but responding at the wrong level, patching the schema
instead of rethinking it (~53%).

## Study 2: what drives the trap?

A 2×2 design — Schema vs. Non-Schema ×
whether the schema-breaking round is _Ambiguously Incompatible_ (the schema
looks applicable but silently fails, as in Study 1) or _Obviously
Incompatible_ (an unrelated stimulus set that makes the schema visibly
inapplicable) — tests whether the trap is worse when the environmental
change is deceptively similar rather than radical.

## Repository layout

| Path                        | Contents                                                                                                                                                                                                                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`docs/`](docs)             | Full project description and preregistrations (Study 1: AsPredicted #269965; Study 2: AsPredicted #286030).                                                                                                                                                        |
| [`stagebook/`](stagebook)   | Experiment definitions for the [Stagebook](https://github.com/watts-lab/stagebook)/Empirica-based platform: the `study/baseline` task flow participants played, plus `annotation/` task templates used to collect human coding (R4 label coding, cheating review). |
| [`data/`](data)             | Raw, anonymized session exports (JSONL) per data-collection batch, one subfolder per study: `study_1_schema_nonschema/`, `study_2/`. Each batch has a `scienceData` file (the actual game data) and a `preregistration`/`postFlightReport` config file.            |
| [`pilot/`](pilot)           | Pilot rounds (`revision_2024xx`–`revision_2025xx`) run while the paradigm and manipulations were refined, plus `study_2_pilots_analysis.ipynb`. Not part of the released studies — useful for design history and power calculations.                               |
| [`annotation/`](annotation) | Human coding of Round 4 labels (per-participant JSON), classifying whether each label is schema-based, one-off, or ambiguous. Feeds both the Study 1 exploratory adaptation analysis and the Study 2 H1 test.                                                      |
| [`analysis/`](analysis)     | Analysis notebooks, released data tables, and figures. Start here.                                                                                                                                                                                                 |

### `analysis/` in detail

- [`study_1_analysis.ipynb`](analysis/study_1_analysis.ipynb) / [`study_2_analysis.ipynb`](analysis/study_2_analysis.ipynb) — canonical notebooks: participant-flow (CONSORT), sample description, preregistered hypothesis tests, exploratory analyses, and figure generation, in pipeline order.
- [`study_1_codebook.md`](analysis/study_1_codebook.md) — column-by-column data dictionary for the released Study 1 tables; read this before doing secondary analysis on the CSVs.
- `study_1_participant_data.csv`, `study_1_analysis_ready.csv`, `study_2_analysis_results.csv` — released data tables produced by the notebooks (see the codebook for grain/units of observation).
- [`figures/`](analysis/figures) — output figures: `figure1`–`figure3` are main-text, `figureS*` are supplement. Each is rendered as both PDF (vector, for the paper) and PNG (preview).
- `consort.py`, `dashboard.py` — helpers: a reusable CONSORT-diagram generator, and an interactive Study 1 + Study 2 results dashboard (`dashboard.html`).

## Getting started

```bash
pip install -r requirements.txt
jupyter notebook analysis/study_1_analysis.ipynb   # or study_2_analysis.ipynb
```

Both notebooks run top-to-bottom against the raw data in `data/` and
regenerate the released CSVs and figures.

## License

Copyright (c) 2026 James Houghton. Licensed under CC BY-NC 4.0.

All materials in this repository — the study design and images (`stagebook/`),
the data, and the analysis code — are licensed under the
[Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).
See [`LICENSE`](LICENSE) for the full text.

You are free to **share** and **adapt** these materials for **non-commercial**
purposes, provided you give appropriate **attribution**. Commercial use —
including selling the materials or incorporating them into for-profit products
or services — is not permitted under this license. For commercial use, please
contact the author to arrange separate permission.

When reusing these materials, please cite this work and link back to this
repository:

> Volvovsky, H., Houghton, J., & Zuckerman Sivan, E. (2026). _Seeing Like an Organization: An Experimental Paradigm for Analyzing how Shared Cognitive Schemas Enable and Trap._ https://github.com/JamesPHoughton/organizational-schema-formation
