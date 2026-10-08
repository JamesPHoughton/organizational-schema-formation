# Study 1 and Study 2 replication materials

This directory translates the experimental manipulation used in the original
Study 1 and Study 2 into **Stagebook 0.35 syntax**, to make the studies easier to
replicate on the current platform. The aim is an exact translation of the
implemented manipulation: the original two-person conditions, stimuli and their
order, configured timing, instructions, comprehension flow, and recall-feedback
rules are preserved. Future changes to the study design belong in a separate
project.

The entry point is [baseline.stagebook.yaml](baseline.stagebook.yaml). Keep its
relative prompt and image files alongside it, use the `Default` intro sequence,
and select the treatments used by the study being replicated:

| Study | Treatment names | Players per group |
| --- | --- | --- |
| Study 1 | `schema`, `nonschema` | 2 |
| Study 2 | `schema`, `nonschema`, `schema_tangrams`, `nonschema_tangrams` | 2 |

The additional two-person treatments are retained from the original source;
they were not selected for these two studies.

The original studies ran from the following files in
**Watts-Lab/deliberation-assets**. These source links are pinned to commit
`c505289affdb17df831b6f782c59ce469207f94b`, the last change to the original
treatment file before data collection:

- [Original `revision_202509/baseline.treatments.yaml`](https://github.com/Watts-Lab/deliberation-assets/blob/c505289affdb17df831b6f782c59ce469207f94b/projects/exaptation/revision_202509/baseline.treatments.yaml):
  the treatment definitions used to run both studies, including their templates,
  intro sequence, image lists, stage durations, and exit sequence.
- [Original `revision_202509` materials](https://github.com/Watts-Lab/deliberation-assets/tree/c505289affdb17df831b6f782c59ce469207f94b/projects/exaptation/revision_202509):
  the instructions, comprehension questions, round instructions, discussion
  prompts, exit questions, and stimuli referenced by that treatment file.
- [Original `revision_202508` materials reused by the studies](https://github.com/Watts-Lab/deliberation-assets/tree/c505289affdb17df831b6f782c59ce469207f94b/projects/exaptation/revision_202508):
  `recall.md`, `labels_correct.md`, and `labels_incorrect.md`, plus the
  `instructions_demo_labeling.jpg` and `instructions_demo_recall.jpg` images
  embedded in the original instructions.

The recorded batch configurations establish which files and conditions were
actually used. See the [Study 1 preregistration export](../../../data/study_1_schema_nonschema/batch_20260203_1909_study1.preregistration.jsonl)
and [Study 2 preregistration export](../../../data/study_2/batch_20260507_1531_study2.preregistration.jsonl).
Both record `projects/exaptation/revision_202509/baseline.treatments.yaml` and the
`Default` intro sequence, with the treatment selections above. They also retain
the original treatment hashes. The remaining batch preregistration exports in
those directories record the same selections.

The translation includes the compatibility changes needed by Stagebook 0.35:
version declarations, explicit intro compatibility, updated reference syntax,
and `allEqual` over `everyone` in place of the former `percentAgreement` check.
Shared sequence templates remove repeated definitions; their expanded round
configurations were checked against the original source for identical timing,
ordered stimuli, and parameters.

The retired host-rendered DiscussionGeneral and Demographics surveys are
represented by [local survey prompts](exit/surveys/surveys.stagebook.yaml), with
the original question wording, choices, required items, and conditional pages.
Their rendering and exported response format follow the current platform:
responses use prompt fields, some stored values have different encodings, and
the former host-generated `discussionOverall` score must be calculated in
analysis. The survey module documents the original source hashes and these
compatibility differences. Historical study data retain their original format.

Historical implementation details are retained for replication. In particular,
the original discussion stages are configured for **300 seconds**, although the
instruction text describes two minutes for training and four minutes for later
rounds. This directory preserves both the original text and the implemented
durations.
