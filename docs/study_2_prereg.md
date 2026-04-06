**1\. Have any data been collected for this study already?**

No, no data has been collected for this study yet

**2\. What's the main question being asked or hypothesis being tested in this study?**

This study (“Study 2”) replicates and extends a previous study (“Study 1”), examining whether shared cognitive schemas can both enable and hinder adaptation under environmental change using a four-round coordination task. In both studies, participants are randomized into small groups and assigned to one of two conditions (Schema vs. Non-Schema). Each group completes four rounds of a coordination task. The first two rounds are condition-specific: in the Schema condition, rounds 1-2 share a consistent feature structure that encourages schema formation; in the Non-Schema condition, rounds 1-2 lack such structure and thus discourage schema formation. Rounds 3-4 are identical across conditions. Round 3 introduces an environmental change but remains solvable using schemas developed for rounds 1-2 of the Schema condition. In Study 1, round 4 featured a change that appeared solvable using the Schema-condition schema but was not (“schema-ambiguous” change). Study 2 introduces a 2 × 2 design crossing Schema vs. Non-Schema with two types of round-4 environmental change: the schema-ambiguous change used in Study 1 and a new change that appears clearly incompatible with the schema (“schema-incompatible” change).

We test whether apparent schema compatibility amplifies the maladaptive consequences of shared schemas by comparing the performance gap between Schema and Non-Schema in round 4 across schema-ambiguous and schema-incompatible change.

Hypothesis 1: The difference in round-4 performance between Non-Schema and Schema groups will be larger under schema-ambiguous than under schema-incompatible change.

Hypothesis 2a: Accuracy for Schema groups in round 4 will be higher under schema-incompatible than schema-ambiguous change.

Hypothesis 2b: The change in accuracy from round-3 to round-4 for Schema will be more negative under schema-ambiguous than schema-incompatible change.

**3\. Describe the key dependent variable(s) specifying how they will be measured.**

Each round of the coordination task will be composed of two stages. First, during the Discussion Stage, participants will engage in a discussion and be asked to name a set of 8 images such that each image receives a unique name. Second, during the Recall Stage, participants will be asked to recall the names given to each image, one by one (“recall stage”). Outcomes will be analyzed at the group level. For each round, we compute Accuracy \- the number of images (out of 8\) for which all group members recalled the same unique name in the Recall Stage (i.e., no name repetition)

**4\. How many and which conditions will participants be assigned to?**

We will randomly assign participants approximately evenly to one of four conditions in a 2 × 2 design: Schema vs. Non-Schema × type of round-4 environmental change (schema-ambiguous vs. schema-incompatible).

**5\. Specify exactly which analyses you will conduct to examine the main question/hypothesis.**

To test Hypothesis 1, we will compute an interaction contrast on round-4 group-level accuracy. For each change type, we compute the accuracy penalty of schematization: penalty(ambiguous) = mean(Schema, ambiguous) - mean(Non-Schema, ambiguous), and penalty(incompatible) = mean(Schema, incompatible) - mean(Non-Schema, incompatible). These penalties are expected to be negative when Schema groups perform worse. The interaction contrast is penalty(ambiguous) - penalty(incompatible), which captures the additional penalty attributable to schema-ambiguous (vs. schema-incompatible) change. We will assess significance using a restricted permutation test (one-tailed, alpha = 0.05): within each Schema condition (Schema and Non-Schema separately), we permute the change-type labels (ambiguous vs. incompatible) across groups, recompute the interaction contrast, and repeat 10,000 times. The one-sided p-value is the proportion of permuted interaction contrasts <= the observed value. We will report the observed interaction contrast, the permutation-based p-value, and Cliff’s delta for the Schema vs. Non-Schema comparison within each change-type arm as descriptive nonparametric effect sizes.

To test Hypothesis 2a, we will compare round-4 accuracy between Schema groups in the schema-incompatible and schema-ambiguous arms using a one-tailed Mann-Whitney U test at alpha = 0.05, testing whether accuracy is higher under schema-incompatible than schema-ambiguous change. We will use a permutation-based one-sided p-value with standard tie handling. We will report group medians, the Hodges-Lehmann estimate of the location shift (incompatible - ambiguous) with a 95% bootstrap confidence interval, and Cliff’s delta as a nonparametric effect size.

To test Hypothesis 2b, we will compute the change in accuracy from round 3 to round 4 (delta = round 4 - round 3) for each Schema group and compare delta between the schema-ambiguous and schema-incompatible arms using a one-tailed Mann-Whitney U test at alpha = 0.05, testing whether delta is more negative under schema-ambiguous than schema-incompatible change. We will use a permutation-based one-sided p-value and report Hodges-Lehmann estimates with 95% bootstrap confidence intervals and Cliff’s delta.

**6\. Describe exactly how outliers will be defined and handled, and your precise rule(s) for excluding observations?**

We will exclude groups where:

- One or more participants are reported as not participating in the Discussion Stage, and don’t check in within 60 seconds, or are reported as not participating more than once.
- One or more participant drops out of the study before all rounds are complete.
- Video recordings or text entry results reveal cheating. Examples: recording names and images during the Discussion Stage of the round, or communicating during the Recall Stage of the round.

**7\. How many observations will be collected or what will determine the sample size? No need to justify decision, but be precise about exactly how the number will be determined.**

Our final sample size for collected data will be approximately N \= XXX participants after excluding observations listed in item 6 above (approximately YYY per condition).

**8\. Anything else you would like to pre-register? (e.g., data exclusions, variables collected for exploratory purposes, unusual analyses planned?)**

- Pilot data were collected prior to pre-registration for QA purposes. It will not be used in the analysis.
- At the end of the experiment, participants will be asked to complete a demographic survey including questions on Age, Gender, Education, and Race. These data may be used for ex post exploratory analysis. They will also be asked to answer open-ended questions explaining their choices in stage 2\. This data may be used in future exploratory analysis.
- Participants will be able to communicate with one another via video chat and text boxes during the first stage. This video and textual data, coupled with the names assigned by participants to images in the first stage, will also be collected for potential future exploratory analysis.
- As a replication check, the schema-ambiguous arm of Study 2 uses identical stimuli and procedures to Study 1. We will confirm that the primary effects of schematization observed in Study 1 replicate in this arm.
