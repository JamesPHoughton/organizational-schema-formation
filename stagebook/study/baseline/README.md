# Seeing Like an Organization

When does a shared way of understanding a task help a group coordinate, and when
does it make adapting harder? These two studies examine **shared cognitive
schemas**: reusable rules that groups develop for interpreting and naming what
they see.

Pairs of participants play an image-labeling and recall game over four rounds.
They discuss the images over a video call and agree on a unique label for each,
then independently recall the labels and receive feedback on whether their
answers match. Round 1 introduces 2, then 4, then 8 images; later rounds each use
8 images.

## The experimental conditions

Rounds 1 and 2 shape how groups learn to label the images:

- **Schema training:** LEGO figures have recurring features, such as hat, arm,
  and foot colors, that encourage a reusable naming rule.
- **Non-schema training:** Varied LEGO figures encourage individual descriptive
  names, with less opportunity to reuse a consistent rule across rounds.

All groups see the same new LEGO figures in round 3, where the color-based schema
remains useful. Round 4 changes the task in one of two ways. The **LEGO** ending
keeps familiar features, but those features no longer distinguish all the images:
the change is *ambiguously incompatible* with the earlier schema. The **tangram**
ending replaces the LEGO figures with black-and-white silhouettes, making the
old color-based schema *obviously incompatible* with the new images.

| Treatment in the viewer | Rounds 1–2 | Round 4 |
| --- | --- | --- |
| `schema` | Schema training | LEGO figures |
| `nonschema` | Non-schema training | LEGO figures |
| `schema_tangrams` | Schema training | Tangrams |
| `nonschema_tangrams` | Non-schema training | Tangrams |

**Study 1** compares `schema` and `nonschema`. **Study 2** includes all four
conditions, testing whether groups adapt differently when the old schema's
inapplicability is obvious. Both studies use groups of two participants.

## Using the viewer

1. Select a treatment and click **View** to open its participant screens.
2. To read the instructions and comprehension questions first, choose **Default**
   from the top-left menu. Use that menu to return to a treatment or compare
   another condition.
3. Use the stage arrows or stage menu to browse the discussions, recall questions,
   feedback, and exit surveys. You can move freely without waiting for timers or
   completing every answer.

The **Position** control switches between participants **0** and **1**. You can
enter a recall answer for each position to explore agreement feedback. This is a
solo preview: live video and the shared labeling editor appear as placeholders.

## Replication details

This directory translates the experimental manipulation used in the original
Study 1 and Study 2 into **Stagebook 0.35 syntax**, to make the studies easier to
replicate on the current platform. The aim is an exact translation of the
implemented manipulation: the original two-person conditions, stimuli and their
order, configured timing, instructions, comprehension flow, and recall-feedback
rules are preserved.

The entry point is [baseline.stagebook.yaml](https://github.com/JamesPHoughton/organizational-schema-formation/blob/main/stagebook/study/baseline/baseline.stagebook.yaml).
Keep its relative prompt and image files alongside it, use the `Default` intro
sequence, and select the treatments for the study listed above.

### Original study sources

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
actually used. See the [Study 1 preregistration export](https://github.com/JamesPHoughton/organizational-schema-formation/blob/main/data/study_1_schema_nonschema/batch_20260203_1909_study1.preregistration.jsonl)
and [Study 2 preregistration export](https://github.com/JamesPHoughton/organizational-schema-formation/blob/main/data/study_2/batch_20260507_1531_study2.preregistration.jsonl).
Both record `projects/exaptation/revision_202509/baseline.treatments.yaml` and the
`Default` intro sequence, with the treatment selections above. They also retain
the original treatment hashes. The remaining batch preregistration exports in
those directories record the same selections.

### Compatibility and historical details

The translation includes the compatibility changes needed by Stagebook 0.35:
version declarations, explicit intro compatibility, updated reference syntax,
and `allEqual` over `everyone` in place of the former `percentAgreement` check.
Shared sequence templates remove repeated definitions; their expanded round
configurations were checked against the original source for identical timing,
ordered stimuli, and parameters.

The retired host-rendered DiscussionGeneral and Demographics surveys are
represented by [local survey prompts](https://github.com/JamesPHoughton/organizational-schema-formation/blob/main/stagebook/study/baseline/exit/surveys/surveys.stagebook.yaml), with
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
