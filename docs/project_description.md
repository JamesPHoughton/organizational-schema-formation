# Project Description: The Competency Trap

## What this project is about

This project studies **competency traps** — the phenomenon in which the process of developing competence at a task becomes a liability when the environment changes. The core claim is that building a successful strategy doesn't just help you in the current environment; it actively hinders you when the environment shifts, even when you could in principle adapt. This is not just "you practiced the wrong thing" (though that's part of it) — it's that the process of becoming competent changes how you think about the problem in ways that make adaptation harder.

The phenomenon is well-known in the organizational strategy literature under various names: competency trap (Levitt & March 1988), core rigidities (Leonard-Barton 1992), the myopia of learning (Levinthal & March 1993), competence-destroying change (Tushman & Anderson 1986), and is closely related to the innovator's dilemma (Christensen 1997) and the exploration-exploitation tradeoff (March 1991). It has been documented extensively through case studies (Kodak, Nokia, Blockbuster, etc.) and cross-sectional organizational research.

The problem with the existing evidence base is that it cannot identify the mechanism. When Nokia fails to adapt to smartphones, dozens of factors are operating simultaneously — sunk costs in manufacturing, stakeholder resistance, identity commitments, regulatory capture, path-dependent ecosystems of suppliers and developers, executive hubris, and also possibly some cognitive or strategic mechanism related to how Nokia's engineers and managers thought about phones. Case studies and observational data cannot distinguish between these explanations, no matter how detailed they are.

Our contribution is to bring the phenomenon into a controlled laboratory paradigm where we can isolate the cognitive and coordination mechanisms from all the organizational confounds, and then systematically test which mechanisms are actually producing the trap.

## The experimental paradigm

### The task

Pairs of participants (dyads) play a collaborative image-labeling and recall game across multiple rounds. In each round:

1. **Labeling phase:** Both participants see a set of images and together assign a unique text label to each one.
2. **Recall phase:** Both participants independently see the same images one at a time, in a random order,and must recall which label was assigned to which image. They type their answers separately.
3. **Scoring:** A pair scores a "match" for an image if both participants independently recall the same unique label for it. Accuracy = number of matches out of the total images, discounting duplicate labels.

The game proceeds through several rounds with increasing numbers of images:

- **Round 1a:** 2 images (warm-up, learning the interface)
- **Round 1b:** 4 images (images from 1a + 2 new images)
- **Round 1c:** 8 images (images from 1b + 4 new images)
- **Round 2:** 8 new images
- **Round 3:** 8 new images
- **Round 4:** 8 new images

### Strategy development manipulation

In the first study, all images are figures made from lego bricks that differ in their construction and coloring.

Two experimental conditions differ in what images groups see during rounds 1 and 2:

- **Schema description training condition:** Images are designed to encourage participants to describe the features of each figure using a systematic labeling strategy. Specifically, images can be uniquely identified by a 3-part code based on the color and position of the figure's hat, hands, and feet. Groups in this condition reliably discover this schema within 1-2 rounds and converge on compressed, systematic labels (e.g., "RLB" for red-left-blue). The 3-part code is consistent, so that it can be reused verbatim between rounds.

- **Holistic description training condition:** Images are designed to encourage participants to use holistic, descriptive labels (e.g., "robot", "owl", "woman"). Groups develop idiosyncratic, item-specific labels.

All participants see the same set of images in round 3, which are diverse enough to support the use of holistic names, and also consistent with the schema established in rounds 1 and 2. Both conditions perform comparably in R3. The difference is in the _type_ of competence they've developed, not the _level_.

In Round 4, all groups again see a new set of 8 images. In study 1, these are similar figures with the same pieces for hands, hat and feet - however, these are no longer sufficient to uniquely distinguish the images from one another, as particular combinations of hat, hand, and foot color/position are repeated multiple times in the image set. Participants must recognize that their original schema no longer applies, and decide what to do about it.

### What the paradigm controls for

The paradigm is specifically designed to rule out a large number of alternative explanations for the competency trap that plague observational research:

- **Selection effects:** Random assignment to schema vs non-schema condition eliminates the possibility that the type of person/group who develops a schema is also the type who fails to adapt.
- **Environmental confounds:** Both conditions face identical R4 images, so any performance difference is due to their R1-R3 history, not the R4 environment.
- **Sunk costs, identity, stakeholder politics:** Dyads are transient (they don't know each other), the task has no identity stakes, there are no sunk costs or external stakeholders. These factors are absent by construction.
- **Feedback and information:** Both conditions get the same feedback structure. There are no intermediaries or delegated observers.
- **Practice with the macro task:** Both conditions play the same number of rounds on the same interface, so general task familiarity is matched.

We enumerate over 40 candidate explanations for competency traps (from selection effects to statistical artifacts to cognitive mechanisms to group dynamics) and document which ones our design rules out vs. which survive as live candidates. This enumeration lives in a supplement table (Table S1) and is a contribution in its own right — it provides a comprehensive taxonomy of why competency traps might occur and what evidence would be needed to distinguish between explanations.

### Study 1 Results: The existence proof

In round 3, schema groups are substantially faster at generating labels than "holistic" groups, using approximately 60% of the time. They also perform at or above the accuracy of the "holistic" groups, demonstrating that they have developed a strategic competency that allows them to outperform rivals on the same task.

However, in round 4, schema groups significantly underperform non-schema groups in both accuracy and labeling time. The effect is large (roughly 2 points out of 8, or ~25% of the scale) and robust. This establishes that the competency trap is a real causal effect of the process of developing a schema-based strategy, not an artifact of selection, environment, motivation, or any of the ~30 other confounds that plague observational research.

Study 1 data: ~32 groups in either condition.

### Exploratory analysis: How groups actually fail

A detailed hand-coding of R4 labeling behavior for all Study 1 schema groups (done by Hagay Volvovsky) reveals a surprising failure-mode distribution:

- **~14% blindly persist** with the unchanged R3 schema. These are the catastrophic failures (accuracy ~2/8). They produce duplicate labels and don't notice.
- **~53% add complexity** — they recognize the schema doesn't work and add a 4th feature element. This is the most common response but produces mediocre outcomes (accuracy ~5/8) because the added feature is often ambiguous or hard to coordinate.
- **~11% substitute** one feature element for another. Better outcomes (~7/8).
- **~14% simplify** to a 2-feature schema. Also better (~7.25/8).
- **~15% abandon the schema entirely** and switch to holistic, descriptive labels.
- A small number use arbitrary labels (months, fruits, etc.) — these do poorly.

The headline finding: **the dominant failure mode is not blind persistence — it's inadequate incremental adaptation.** Most groups (86%) recognize the schema needs to change. But they respond at the wrong level: making tactical fixes to the schema (adding features, tweaking elements) rather than questioning whether schematic thinking is still the right approach. This is what we call "tactical vs strategic" level thinking, and it connects to the literature on incremental vs radical change, exploration vs exploitation, and the levels of organizational learning.

Groups that voluntarily switch to holistic descriptions tend to outperform incremental adapters, but this comparison is correlational — better groups might be more likely to switch (selection), rather than switching causing better outcomes. This motivates a causal test.

### What we think is happening

The competency trap has (at least) four candidate cognitive/coordination mechanisms, which we organize into a taxonomy:

1. **Detection failure.** Groups don't notice that the environment has changed in ways that make their strategy maladaptive. In our task, this would mean groups applying the old schema without recognizing that it produces duplicates. Our exploratory data suggest this is a minority failure mode (~14%), not the dominant one.

2. **Tactical lock-in / level-of-thinking failure.** Groups detect that something is wrong but respond at the wrong level of abstraction. They make incremental adjustments to the schema (add a feature, substitute an element) rather than questioning whether the schematic approach itself is still appropriate. This is the dominant failure mode in our Study 1 data. It connects to the broader literature on incremental vs radical organizational change: the competency trap may be worst not when the environmental change is most radical, but when it's deceptively similar — similar enough to keep actors focused on tactical adaptation rather than strategic rethinking.

3. **Strategy-switching cost / practice deficit.** Even groups that correctly identify the need for a new approach and choose a good alternative may be at a disadvantage compared to groups that have been practicing that alternative all along. This is partly trivial (of course you're worse at something you haven't practiced) and partly interesting (the shared ground and coordination conventions you built around the old strategy are lost, and building new ones takes time).

4. **Residual interference.** The old strategy continues to bias what comes to mind even after conscious abandonment. Groups that switch away from the schema might still produce schema-influenced labels, or might struggle to generate alternatives because the schema dominates their mental search space.

These mechanisms are not mutually exclusive — all four can operate simultaneously — and our research program is designed to progressively test which ones are actually contributing.

### The counter-intuitive claim

The literature on competency traps (and related phenomena like the innovator's dilemma) tends to assume that the trap is worst when the environmental change is large — when the new environment is so different that existing capabilities are useless. We are curious if this bears out - the opposite may be true: **the trap is worst when the change is deceptively similar.** A sufficiently radical change (like tangrams replacing faces) forces actors out of their existing frame entirely. A subtle change (like new faces that look similar but have overlapping features) keeps actors trapped in incremental adaptation that feels productive but isn't.

This connects to a version of the Nokia/iPhone story: the iPhone wasn't radical enough to scare Nokia away from their phone-making frame. If the disruption had been Neuralink (something so different that no phone-making competency could possibly apply), Nokia might have pivoted immediately. The trap was that smartphones looked enough like phones that Nokia thought they could incrementally adapt.

### The intervention implication

Different mechanisms imply different interventions:

- If detection failure: build monitoring and feedback systems
- If tactical lock-in: implement strategic review processes ("are we thinking about this the right way?" prompts, pre-mortems, red teams)
- If practice deficit: cross-train, maintain a portfolio of strategies, invest in exploration even when exploitation is working
- If coordination cost: build explicit strategy-discussion norms, reduce the social cost of proposing radical alternatives

## Study 2 (planned): Testing mechanisms of the competency trap

### Motivation

The Study 1 exploratory analysis reveals that the dominant failure mode is not blind persistence but incremental adaptation at the wrong level of abstraction. Groups that voluntarily switched to holistic descriptions tended to outperform those that incrementally adapted, but this comparison is correlational — smarter or more flexible groups might both switch more readily AND perform better, without the switching itself being what helps.

Study 2 should advance our understanding of the mechanism. We have not committed to a final design. Below we describe the candidate designs we are considering, what each would test, what each controls for, and what confounds each leaves unresolved.

### Candidate Design A: Radical vs incremental environmental change (Tangrams 2x2)

**Design:** 2x2 between-groups: (Schema vs Non-Schema) x (Ambiguous R4 / "UV" vs Incompatible R4 / "Tangrams").

- UV R4: new lego-figure images where the schema seems applicable but produces duplicates (same as Study 1).
- Tangrams R4: abstract geometric shapes that bear no resemblance to R1-R3 images, making the schema visibly inapplicable.

**What it tests:** Does the magnitude of environmental change affect how groups respond to the competency trap? Specifically, does a radical change (tangrams) force groups out of the incremental-adaptation mode that dominates in the ambiguous-change (UV) condition?

**What it would show:**

- Manipulation check: does radical change produce more schema abandonment than ambiguous change? (Pilot says yes — ~80% vs ~15%.)
- Primary comparison: is the schema penalty (Schema minus Non-Schema on R4 accuracy) smaller in the tangrams condition than in the UV condition?
- If the penalty shrinks: radical change helps, suggesting that part of the trap is about the environment keeping groups in incremental mode.
- If the penalty persists: the trap is robust to how groups respond — having built a schema hurts even when you successfully abandon it.

**Strengths:**

- We have pilot data (17 schema-tangrams, 13 non-schema-tangrams, plus the full Study 1 UV data).
- The manipulation check is already known to work dramatically.
- Connects directly to the incremental vs radical change literature.
- The counter-intuitive claim — that the trap is worst when the change is deceptively similar, not when it's radical — is a strong hook.

**Confounds and limitations:**

1. **Practice confound.** Non-schema-tangrams groups have 3 rounds of holistic-labeling practice; schema-tangrams groups are doing it for the first time. The gap between them conflates schema interference with practice deficit.
2. **Shared-ground confound.** Non-schema groups have 3 rounds of shared holistic vocabulary; schema groups that switch must build new shared ground from scratch.
3. **Stimulus confound.** UV and tangrams R4 have different intrinsic difficulty. The non-schema cells absorb this in the interaction, but the parallel-difficulty assumption (that the UV-vs-tangrams difficulty difference is the same for schema and non-schema groups) is untestable.
4. **The non-schema control answers the wrong question.** It tells you "how hard is this task for a group that practiced the right strategy all along?" not "how hard is this task for a group that just switched strategies?" These are different, and the difference is exactly the set of mechanisms we want to isolate.
5. **Cannot distinguish why radical change helps (if it does).** Is it because groups think more strategically? Because the schema can't interfere when the stimuli are unrelated? Because starting truly from scratch is easier than adapting a broken schema? The design can't tell.

**Pilot results:** The interaction contrast is small in the pilot (~0.44 points, n.s.), but the pilot is heavily underpowered for this comparison (n=17/13 in the tangrams cells). The within-tangrams schema penalty is ~1.55 points (p=.033), suggesting the trap persists even after forced abandonment — though this could be the practice confound.

### Candidate Design B: Strategic vs tactical prompt (intervention study)

**Design:** All groups are in the schema condition. Identical R1-R3. Before R4, random assignment to one of two prompts matched in length and tone:

- **Strategic prompt:** "Before you begin, discuss with your partner: is your overall labeling approach still the best one for these new images, or should you consider a completely different approach?"
- **Tactical prompt:** "Before you begin, discuss with your partner: are there any adjustments you should make to your labeling approach to handle these new images?"

R4: Same UV images as Study 1 for everyone.

**What it tests:** Does the level of reflection — tactical vs strategic — causally affect how groups respond to the competency trap? This directly tests the level-of-thinking mechanism identified in the exploratory analysis.

**What it would show:**

- Manipulation check: does the strategic prompt shift groups from incremental adaptation to strategic-level change (as coded by the five-level taxonomy)?
- If accuracy improves: the level-of-thinking mechanism is operative. Framing matters, independent of practice or capability. Practical implication: strategic review processes can help.
- If accuracy doesn't change: the trap is robust to conscious reframing. The surviving mechanisms are practice deficit, residual interference, and coordination costs. Practical implication: you need structural interventions, not just better thinking.
- If abandonment increases but accuracy doesn't: the trap has two layers — a framing layer (fixable) and a capability layer (not fixable by prompting alone).

**Strengths:**

- Controls for everything except the level of reflection: practice, shared ground, stimuli, demand effects, schema strength at R4 entry are all identical.
- The tactical prompt is not a straw man — it actively encourages the failure mode documented in the exploratory analysis. It maps onto "continuous improvement" in management practice. The strategic prompt maps onto "strategic review."
- Informative under every outcome. Each result narrows the set of viable mechanisms differently.
- Directly actionable: if the strategic prompt helps, the intervention is something organizations can implement (periodic "are we thinking about this the right way?" reviews).

**Confounds and limitations:**

1. **Prompt wording is load-bearing.** The exact phrasing matters and hasn't been piloted. Different wordings might produce different results. This is a sensitivity concern that needs piloting before pre-registration.
2. **No non-schema baseline within the study.** We don't know "how much of the gap does the prompt close?" without a non-schema reference group. We can compare descriptively to Study 1's non-schema results, but this is cross-study and informal.
3. **Compliance uncertainty.** Groups might ignore the prompt, or both prompts might produce the same behavior if groups are already inclined to adapt incrementally regardless of what they're asked.
4. **Cannot distinguish between sub-mechanisms within "strategic thinking."** If the prompt helps, is it because groups (a) recognized the schema was broken, (b) generated a better alternative, or (c) had a productive discussion with their partner that they wouldn't have had otherwise? The design conflates these.

### Candidate Design C: Radical change as a "natural prompt" (Schema-only tangrams vs Schema-only UV)

**Design:** All groups are in the schema condition. Random assignment to UV R4 vs Tangrams R4. No non-schema groups.

**What it tests:** Does radical environmental change — which naturally forces strategic-level thinking — produce better outcomes than ambiguous environmental change? This is a variant of Design A that drops the non-schema cells entirely.

**What it would show:**

- If schema-tangrams accuracy > schema-UV accuracy: radical change helps schema groups, suggesting that the ambiguity of the UV condition is what keeps them trapped.
- If schema-tangrams accuracy ≈ schema-UV accuracy: the trap produces similar costs regardless of whether groups are incrementally adapting or radically switching.
- If schema-tangrams accuracy < schema-UV accuracy: the tangrams task is intrinsically harder, and the stimuli confound dominates.

**Strengths:**

- Simple: two cells, both schema, random assignment.
- Directly tests the "deceptive similarity" claim: is the trap worse when the change is subtle?
- No practice confound (both groups practiced schema, neither practiced holistic labeling).

**Confounds and limitations:**

1. **Stimulus confound is uncontrolled.** UV and tangrams have different intrinsic difficulty, and without non-schema cells there is no way to subtract this out. If schema-UV groups outperform schema-tangrams groups, you can't tell if it's because ambiguous change is easier to handle or because the tangrams images are just harder to label.
2. **This is the fundamental problem:** you're comparing performance on two different tasks. Any difference could be about the tasks, not about the mechanism.
3. **Probably not viable as a standalone design** because of the stimulus confound, but might be useful as a supplementary comparison alongside Design A or B.

### Candidate Design D: Verbal detection handover (telling groups the schema won't work)

**Design:** All groups are in the schema condition. Before R4 (UV images for everyone), random assignment to:

- **Detection prompt:** "In this round, the images have changed so that your previous labeling system will produce duplicate labels. You will need a different approach."
- **Neutral prompt:** "In this round, you will see a new set of images." (matched length, no strategic content)

**What it tests:** Is detection failure a meaningful component of the trap? If telling groups the schema won't work improves performance, detection was a bottleneck. If it doesn't, the trap persists even after detection.

**What it would show:**

- If accuracy improves: detection failure is operative. Some groups in Study 1 were trapped partly because they didn't notice the schema was broken. Handing them this information helps.
- If accuracy doesn't improve: detection isn't the bottleneck. Groups already know (consistent with the exploratory analysis showing only ~14% blind persistence) — the problem is what they do with that knowledge.

**Strengths:**

- Directly tests the detection-failure mechanism.
- Clean: same stimuli, same history, only the information changes.
- If detection doesn't help, it's a strong piece of evidence that the trap is about response, not recognition — consistent with the exploratory analysis.

**Confounds and limitations:**

1. **The detection prompt does more than hand over detection.** It also tells groups WHY the schema fails ("duplicate labels") and implicitly suggests what to look for. It's detection + diagnosis, not pure detection.
2. **Demand-effect asymmetry.** The detection prompt is more alarming and attention-grabbing than the neutral prompt, which could produce a "try harder" effect independent of the detection content.
3. **The exploratory analysis already suggests detection is a small part of the story** (~14% blind persistence), so this design might be testing a mechanism that's already known to be minor. It would confirm the exploratory finding causally, which has value, but might not be the most informative use of a study.
4. **Doesn't test the level-of-thinking mechanism**, which the exploratory analysis suggests is more important.

### Candidate Design E: Strategic prompt + radical change (combining B and A)

**Design:** All groups are in the schema condition. 2x2: (Strategic prompt vs Tactical prompt) x (UV R4 vs Tangrams R4).

**What it tests:** Does the strategic prompt help MORE when the environmental change is ambiguous (where groups need the most help recognizing the need for strategic change) vs when it's radical (where the environment already forces strategic change)? An interaction would show that the prompt and the environmental change are doing the same thing — elevating the level of thinking — through different routes.

**Strengths:**

- Tests whether the prompt and radical change are substitutes (same mechanism, different routes) or complements (different mechanisms that stack).
- If the prompt helps in UV but not in tangrams: the prompt is doing what radical change does naturally — elevating the level of thinking. The mechanism is confirmed and the practical implication is clear.
- If the prompt helps in both: the prompt adds something beyond what radical change provides (perhaps coordination, or a richer search for alternatives).

**Confounds and limitations:**

1. **Four cells, all schema.** Needs more participants for the same per-cell power.
2. **Inherits the stimulus confound from Design A** (UV and tangrams have different intrinsic difficulty), though this matters less when comparing within-stimulus (prompt effect within UV, prompt effect within tangrams).
3. **Complexity.** More conditions = more parameters = more ways for the results to be ambiguous. May be overkill for a first mechanism study.

### Current thinking on design choice

We have not committed to a final design. The leading candidate is **Design B (strategic vs tactical prompt)** because:

- It has the cleanest controls (everything held constant except the level of reflection)
- It's informative under every outcome
- It directly tests the mechanism the exploratory analysis points to
- It produces a practically actionable finding
- It's the simplest design that addresses the question

However, **Design A (tangrams 2x2)** remains attractive because it connects to the incremental-vs-radical-change literature and produces the counter-intuitive "deceptive similarity" claim. Its confounds are real but may be acceptable if the paper frames the finding carefully.

We may also run Design A and Design B as separate studies (Study 2 and Study 3, or as a single study with more conditions), or run one as a pilot alongside the other. The decision depends on:

- Whether the strategic prompt actually shifts behavior (needs piloting before committing)
- How much space the publication venue allows
- Whether the paper's arc needs the tangrams comparison for the "radical vs incremental" framing, or whether the exploratory analysis alone is sufficient to motivate the intervention
- Ezra's strategic judgment on what clears the bar for the target venue

### Existing pilot data for Study 2

Regardless of which design we choose, we have useful pilot data:

- **Tangrams pilot:** 17 schema-tangrams groups, 13 non-schema-tangrams groups. Schema-reliance coding complete. Demonstrates that radical change produces ~80% schema abandonment. Shows a within-tangrams schema penalty of ~1.55 points (p=.033).
- **UV pilot (Study 1 data):** 52 schema groups, 46 non-schema groups. Hagay's five-level failure-mode coding complete. Provides the baseline failure-mode distribution that any Study 2 manipulation check should shift.
- **Schema-reliance coding:** Human-coded 0-8 scores available for both UV and tangrams conditions, enabling direct comparison of abandonment rates across conditions.

The strategic/tactical prompt (Design B) has NOT been piloted. If we go with Design B, a small pilot (5-10 groups per condition) should be run before pre-registration to verify that the prompt actually shifts behavior.

## Connection to existing literature

### Organizational strategy / management

- **Competency trap / capability trap:** Levitt & March 1988, March 1991 (exploration/exploitation), Levinthal & March 1993
- **Core rigidities:** Leonard-Barton 1992
- **Competence-destroying vs competence-enhancing change:** Tushman & Anderson 1986
- **Innovator's dilemma:** Christensen 1997
- **Dynamic capabilities:** Teece, Pisano, Shuen 1997 — and the problematic infinite regression of "higher-order" capabilities
- **Ambidexterity:** The ability to both explore and exploit — but this literature has a tendency to name the solution without explaining the mechanism
- **Incremental vs radical change:** The standard taxonomy of how organizations respond to environmental shifts. Our finding that incremental change IS the trap connects to and challenges this literature.

### Cognitive psychology

- **Einstellung effect / mental set:** Luchins (water jar problems) — prior experience with one solution method blocks discovery of a simpler one
- **Functional fixedness:** Duncker — inability to see novel uses for objects with a known function
- **Cognitive entrenchment:** Dane 2010 — experts become entrenched in domain schemas
- **Schema theory:** Bartlett, Rumelhart — how schemas organize perception and memory, and how they resist updating
- **Predictive processing / Bayesian updating:** Strong priors slow updating when the generative process changes — a normative account of why competence produces rigidity

### Social / coordination

- **Common ground:** Clark — shared knowledge and conventions that accumulate through interaction and become hard to revise
- **Shared mental models:** Cannon-Bowers — how teams develop shared representations and how those can become liabilities
- **Convention formation:** Lewis, Skyrms — how coordination equilibria become self-reinforcing
- **Reference games / collaborative labeling:** Krauss & Weinheimer, Brennan & Clark — the specific paradigm family our task belongs to

### Terminology note

The literature uses many overlapping terms: schema, mental model, cognitive frame, dominant logic, organizational routine, strategy, competency, capability. These are not identical constructs, but they overlap substantially in the way they are used. After reviewing the literature (particularly Hagay's analysis of how different sub-literatures use these terms), "mental model" may be a slightly better fit for our construct than "schema," because the people who use "schema" tend to be more qualitative/sensemaking-oriented, while the people who use "mental model" tend to be doing the kind of empirical work closer to ours. However, "schema" is more immediately intuitive and we have been using it throughout our experimental materials. We use "schema" in the paper and note the terminological landscape.

## Technical details

### Data and code

- **Repository:** The project lives in a git repository with analysis code, experimental data, and documentation.
- **Analysis notebook:** `pilot/study_2_pilots_analysis.ipynb` contains the current analysis of pilot data, including power calculations, diagnostic plots, and exploratory analyses.
- **Data files:** Science data is stored as JSONL files in `data/` and `pilot/revision_*/` directories. Human-coded schema-reliance data is in `pilot/Pooled Study 1 & Study 2 Pilot.xlsx`.
- **Experiment platform:** The game runs on a custom web platform (Empirica/Meteor-based) that handles participant matching, round timing, image display, label entry, and recall testing.

### Measurement

- **Primary DV:** R4 accuracy = number of images (out of 8) for which both partners recalled the same label. Measured at the group level (each group produces one accuracy score per round).
- **Schema-reliance score:** Human-coded, 0-8 per group per round. For each of the 8 R4 labels, two research assistants independently code whether the label relies on the schema the group formed in R1-R3 (1 = schema-based, 0 = not). Sum of the 8 item-level codes.
- **Labeling time:** Time in seconds from the start of the labeling phase to the labeler's submission. A proxy for schema strength (faster = more automated/compressed strategy) and for effort.
- **Labels themselves:** The actual text labels assigned to each image. Available for content analysis (vocabulary diversity, schema features used, holistic vs systematic, etc.).
- **Video/audio recordings:** Available for a subset of groups. Have been used for qualitative spot-checks of behavior during the transition.

### Sample sizes and power

Study 1: ~52 schema groups, ~46 non-schema groups. The schema penalty on R4 accuracy is ~2 points (out of 8), detectable with high power at these sample sizes.

Study 2 (planned): The intervention study needs to be powered for a potentially smaller effect (the difference between strategic and tactical prompting, not the full schema-vs-nonschema gap). Power simulations should be run at a range of assumed effect sizes. Based on pilot data, we expect to need 30-50 groups per condition for 80% power, but this depends on the true effect size of the prompt manipulation, which we don't have pilot data for yet.

The schema-reliance manipulation check (does the strategic prompt shift schema reliance?) will likely be well-powered at any N sufficient for the accuracy test, based on the dramatic shifts observed in the tangrams pilot.

## Epistemological stance

Our studies do not identify THE mechanism of the competency trap. They progressively narrow the set of candidate mechanisms by showing which are unnecessary for the trap to occur and which are insufficient to explain it.

Study 1 shows that ~30 candidate explanations (selection, environmental, motivational, identity, information, statistical artifacts) are NOT NECESSARY — the trap occurs without them. This does not mean they are irrelevant in the real world; they may amplify or sustain the trap. It means they are not required.

The candidates that survive Study 1 are the cognitive and coordination mechanisms (Families 6 and 7 in our taxonomy). The exploratory analysis further narrows these by showing which are consistent with observed failure modes. Study 2 tests one specific survivor (level-of-thinking) with a causal manipulation.

The logic is always: "this mechanism is not necessary for the trap to occur" or "this mechanism is operative in this setting." Never: "this mechanism is THE cause." The competency trap in the real world is almost certainly multiply determined. Our contribution is showing which ingredients are sufficient on their own, which are not necessary, and which are operative when isolated.

This framing also addresses the "toy example" criticism. The simplicity of our paradigm is not a limitation — it is the identification strategy. If the trap only appeared in complex organizational settings, you could never know which of the many co-occurring factors produced it. By showing that it occurs in a 30-minute dyadic labeling task with none of the organizational complexity, we establish that the cognitive and coordination dynamics alone are sufficient. The organizational factors are amplifiers, not causes.

## Current status and next steps

1. **Study 1 data is collected and analyzed.** The main effect is robust. The exploratory failure-mode analysis (Hagay's coding) is complete for Study 1 schema groups.

2. **Study 2 design is converging on the intervention study** (strategic vs tactical prompt). Exact wording of prompts needs to be finalized and piloted. The tangrams 2x2 has been piloted but has confound issues (practice differential in the non-schema control) that make it less clean as a mechanism test. The tangrams data remains useful as a manipulation check and descriptive reference.

3. **The paper outline exists** (see `docs/paper_outline.md`) with a clear arc: introduction (phenomenon + identification problem + desiderata), Study 1 (existence proof), exploratory analysis (failure modes), Study 2 (intervention), discussion (what's ruled out, what survives, implications for practice).

4. **The alternative-explanations table** (Table S1 for the supplement) is drafted with 44 entries organized into 8 families, each with a description and an assessment of how we address it.

5. **A literature review is needed** covering the organizational strategy, cognitive psychology, and social/coordination literatures that bear on competency traps. A detailed handoff document for this review exists separately.

6. **Pre-registration for Study 2** needs to be written once the design is finalized, including: exact prompt wording, primary DV, manipulation check, exclusion criteria, sample size justification, and the three-outcome interpretation framework.

7. **Target venue:** PNAS or similar. The paper should be empirically driven (not theory-heavy), with the theoretical contribution emerging from the systematic elimination of alternatives and the identification of the dominant failure mode. The format is space-limited, which means the argument needs to be tight and the supplement does heavy lifting.

## Key collaborators

- **James Houghton** — experimental design, data analysis, paradigm development, codebase
- **Hagay Volvovsky** — qualitative coding of failure modes, video spot-checks, connection to org theory literature
- **Ezra Zuckerman Sivan** — senior collaborator, strategic guidance on framing and publication
- **Trini Feng** — collaborator (role to be clarified in handoff)
