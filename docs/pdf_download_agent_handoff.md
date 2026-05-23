# Handoff: PDF Download Task for Competency Trap Literature Review

## Context

I am running a research project on the "competency trap" phenomenon — the tendency for expertise at a task to become a liability when the environment changes. A prior agent has already:

1. Conducted a systematic literature search across 6 topic areas
2. Written a comprehensive literature review (`docs/competency_trap_literature_review.md`)
3. Created a campus access checklist (`docs/papers_for_campus_access.md`)
4. Set up organized folders at `docs/papers/01_core_competency_trap/` through `07_reference_games_collab/`

Your job is to download PDFs of as many of the papers listed below as possible from open-access sources, saving them into the folder structure described. For papers you cannot access, append them to a file at `docs/papers/COULD_NOT_DOWNLOAD.md` with the URL(s) you tried.

---

## Download Strategy (use in this order for each paper)

1. **Check Unpaywall** — the best first stop for legally free versions:
   `https://api.unpaywall.org/v2/{DOI}?email=james.p.houghton@gmail.com`
   Parse `best_oa_location.url_for_pdf` from the JSON response.

2. **Check Semantic Scholar** for an open-access PDF link:
   `https://api.semanticscholar.org/graph/v1/paper/search?query={TITLE_AUTHOR}&fields=title,authors,year,openAccessPdf,externalIds`
   Use `openAccessPdf.url` if present.

3. **Try known open-access mirrors** (listed per paper below).

4. **Try the author's institutional page** — many authors post PDFs directly on their university websites.

5. **Try Google Scholar** — search `"{title}" filetype:pdf` and follow any PDF links (not Sci-Hub).

6. **Do NOT use Sci-Hub or any other piracy site.** Only open-access, preprint, or author-posted versions.

When downloading, use `curl -L -A "Mozilla/5.0" -o {filepath} {url}` and verify the file is a real PDF (starts with `%PDF`), not an HTML error page.

---

## Papers to Download

### Folder: `docs/papers/01_core_competency_trap/`

| # | Filename to save as | Citation | DOI | Notes |
|---|---|---|---|---|
| 1 | `march_1991_exploration_exploitation.pdf` | March, J.G. (1991). Exploration and exploitation in organizational learning. *Organization Science, 2*(1), 71-87. | 10.1287/orsc.2.1.71 | Try NTNU mirror: `http://www.iot.ntnu.no/innovation/norsi-pims-courses/Levinthal/March%20(1991).pdf` |
| 2 | `levitt_march_1988_organizational_learning.pdf` | Levitt, B., & March, J.G. (1988). Organizational learning. *Annual Review of Sociology, 14*, 319-340. | 10.1146/annurev.so.14.080188.001535 | Try NTNU: `http://www.iot.ntnu.no/innovation/norsi-pims-courses/Greve/Levitt%20&%20March%20(1988).pdf` |
| 3 | `levinthal_march_1993_myopia_learning.pdf` | Levinthal, D.A., & March, J.G. (1993). The myopia of learning. *Strategic Management Journal, 14*(S2), 95-112. | 10.1002/smj.4250141009 | Try NTNU: `http://www.iot.ntnu.no/innovation/norsi-pims-courses/Lavie/Levinthal%20&%20March%20(1993).pdf` |
| 4 | `henderson_clark_1990_architectural_innovation.pdf` | Henderson, R.M., & Clark, K.B. (1990). Architectural innovation. *Administrative Science Quarterly, 35*(1), 9-30. | 10.2307/2393549 | Try NTNU: `http://www.iot.ntnu.no/innovation/norsi-pims-courses/tushman/Handerson%20&%20Clark%20(1990).pdf` |
| 5 | `tushman_anderson_1986_technological_discontinuities.pdf` | Tushman, M.L., & Anderson, P. (1986). Technological discontinuities and organizational environments. *Administrative Science Quarterly, 31*(3), 439-465. | 10.2307/2392832 | Try NTNU: `http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Tushman%20&%20Anderson%20(1986).PDF` |
| 6 | `leonard_barton_1992_core_capabilities.pdf` | Leonard-Barton, D. (1992). Core capabilities and core rigidities. *Strategic Management Journal, 13*(S1), 111-125. | 10.1002/smj.4250131009 | Check HBS working paper repository; try ResearchGate |
| 7 | `tripsas_gavetti_2000_capabilities_cognition.pdf` | Tripsas, M., & Gavetti, G. (2000). Capabilities, cognition, and inertia. *Strategic Management Journal, 21*(10-11), 1147-1161. | 10.1002/1097-0266(200010/11)21:10/11<1147::AID-SMJ128>3.0.CO;2-R | Try HBS: `https://www.hbs.edu/ris/Publication%20Files/00-067_cdcafdf1-d946-44ec-96ad-558ad606477d.pdf` |
| 8 | `audia_locke_smith_2000_paradox_success.pdf` | Audia, P.G., Locke, E.A., & Smith, K.G. (2000). The paradox of success. *Academy of Management Journal, 43*(5), 837-853. | 10.5465/1556411 | **PRIORITY 1** — only prior controlled lab test of competency trap. Try Unpaywall and Semantic Scholar first. |
| 9 | `sorensen_stuart_2000_aging_obsolescence.pdf` | Sorensen, J.B., & Stuart, T.E. (2000). Aging, obsolescence, and organizational innovation. *ASQ, 45*(1), 81-112. | 10.2307/2667187 | Try Columbia: `https://business.columbia.edu/sites/default/files-efs/pubfiles/434/aging00.pdf` |
| 10 | `hannan_freeman_1984_structural_inertia.pdf` | Hannan, M.T., & Freeman, J.H. (1984). Structural inertia and organizational change. *American Sociological Review, 49*(2), 149-164. | 10.2307/2095567 | Try NTNU: `http://www.iot.ntnu.no/innovation/norsi-pims-courses/harrison/Hannan%20&%20Freeman%20(1984).PDF` |
| 11 | `hannan_freeman_1977_population_ecology.pdf` | Hannan, M.T., & Freeman, J.H. (1977). The population ecology of organizations. *American Journal of Sociology, 82*(5), 929-964. | 10.1086/226424 | Try Unpaywall; or ResearchGate |
| 12 | `teece_pisano_shuen_1997_dynamic_capabilities.pdf` | Teece, D.J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities and strategic management. *Strategic Management Journal, 18*(7), 509-533. | 10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z | Try Unpaywall; widely cited, many preprint versions available |
| 13 | `sull_1999_active_inertia.pdf` | Sull, D.N. (1999). The dynamics of standing firm. *Harvard Business Review, 77*(1), 56-70. | N/A | Try HBR website or London Business School repository |
| 14 | `miller_1994_perils_excellence.pdf` | Miller, D. (1994). What happens after success. *Journal of Management Studies, 31*(3), 325-358. | 10.1111/j.1467-6486.1994.tb00914.x | Try Unpaywall; check McGill repository |
| 15 | `crossan_lane_white_1999_organizational_learning.pdf` | Crossan, M.M., Lane, H.W., & White, R.E. (1999). An organizational learning framework. *Academy of Management Review, 24*(3), 522-537. | 10.5465/amr.1999.2202135 | Try Unpaywall or Western University (Ivey) repository |
| 16 | `kelly_amburgey_1991_organizational_inertia.pdf` | Kelly, E., & Amburgey, T.L. (1991). Organizational inertia and momentum. *Academy of Management Journal, 34*(3), 591-612. | 10.5465/256406 | Try Unpaywall |
| 17 | `zollo_winter_2002_deliberate_learning.pdf` | Zollo, M., & Winter, S.G. (2002). Deliberate learning and the evolution of dynamic capabilities. *Organization Science, 13*(3), 339-351. | 10.1287/orsc.13.3.339.2780 | Try Semantic Scholar or Wharton repository |
| 18 | `greve_1998_performance_aspirations.pdf` | Greve, H.R. (1998). Performance, aspirations, and risky organizational change. *Administrative Science Quarterly, 43*(1), 58-86. | 10.2307/2393591 | Try Unpaywall; INSEAD or NHH repository |
| 19 | `ocasio_1997_attention_based_view.pdf` | Ocasio, W. (1997). Towards an attention-based view of the firm. *Strategic Management Journal, 18*(S1), 187-206. | 10.1002/(SICI)1097-0266(199707)18:1+<187::AID-SMJ936>3.0.CO;2-Y | Try Unpaywall or Northwestern repository |

### Folder: `docs/papers/03_cognitive_mechanisms/`

| # | Filename to save as | Citation | DOI | Notes |
|---|---|---|---|---|
| 20 | `luchins_1942_einstellung.pdf` | Luchins, A.S. (1942). Mechanization in problem solving. *Psychological Monographs, 54*(6), 1-43. | 10.1037/h0093502 | 1942 — may be public domain. Try Internet Archive (`archive.org`), APA's older holdings, or Google Scholar |
| 21 | `bilalic_mcleod_gobet_2008a_good_thoughts.pdf` | Bilalic, M., McLeod, P., & Gobet, F. (2008). Why good thoughts block better ones. *Cognition, 108*(3), 652-661. | 10.1016/j.cognition.2008.05.008 | **PRIORITY 1** — key attentional mechanism paper. Try Unpaywall, then ResearchGate, then Brunel University repository |
| 22 | `bilalic_mcleod_gobet_2008b_inflexibility_experts.pdf` | Bilalic, M., McLeod, P., & Gobet, F. (2008). Inflexibility of experts. *Cognitive Psychology, 56*(2), 73-102. | 10.1016/j.cogpsych.2007.04.001 | **PRIORITY 1** — experts more susceptible to Einstellung. Same sources as above |
| 23 | `bilalic_mcleod_gobet_2010_einstellung_mechanism.pdf` | Bilalic, M., McLeod, P., & Gobet, F. (2010). The mechanism of the Einstellung (set) effect. *Current Directions in Psychological Science, 19*(2), 111-115. | 10.1177/0963721410363571 | Try Unpaywall; SAGE sometimes open |
| 24 | `dane_2010_cognitive_entrenchment.pdf` | Dane, E. (2010). Reconsidering the trade-off between expertise and flexibility. *Academy of Management Review, 35*(4), 579-603. | 10.5465/amr.2010.53503239 | Try Unpaywall; check Rice University repository |
| 25 | `wiley_1998_expertise_mental_set.pdf` | Wiley, J. (1998). Expertise as mental set. *Memory & Cognition, 26*(4), 716-730. | 10.3758/BF03211392 | Try Unpaywall; Psychonomic Society / Springer; check ResearchGate |
| 26 | `anderson_pichert_1978_perspective_recall.pdf` | Anderson, J.R., & Pichert, J.W. (1978). Recall of previously unrecallable information following a shift in perspective. *JVLVB, 17*(1), 1-12. | 10.1016/S0022-5371(78)90485-1 | Try Internet Archive or ResearchGate |
| 27 | `camerer_loewenstein_weber_1989_curse_knowledge.pdf` | Camerer, C., Loewenstein, G., & Weber, M. (1989). The curse of knowledge in economic settings. *Journal of Political Economy, 97*(5), 1232-1254. | 10.1086/261651 | Try Unpaywall; Caltech or CMU repositories |
| 28 | `hinds_1999_curse_expertise.pdf` | Hinds, P.J. (1999). The curse of expertise. *JEP: Applied, 5*(2), 205-221. | 10.1037/1076-898X.5.2.205 | Try Unpaywall; APA |
| 29 | `clark_2013_predictive_brains.pdf` | Clark, A. (2013). Whatever next? *Behavioral and Brain Sciences, 36*(3), 181-204. | 10.1017/S0140525X12000477 | Try Cambridge BBS; this is a major BBS target paper — commentary version sometimes OA |
| 30 | `hogarth_lejarraga_soyer_2015_kind_wicked.pdf` | Hogarth, R.M., Lejarraga, T., & Soyer, E. (2015). The two settings of kind and wicked learning environments. *Current Directions in Psychological Science, 24*(5), 379-385. | 10.1177/0963721415585878 | Note: the review cites a slightly wrong title/journal — correct title is "The two settings of kind and wicked learning environments". Try SAGE/Unpaywall. |
| 31 | `croskerry_2002_cognitive_bias_diagnosis.pdf` | Croskerry, P. (2002). Achieving quality in clinical decision making. *Academic Emergency Medicine, 9*(11), 1184-1204. | 10.1111/j.1553-2712.2002.tb01574.x | Try Wiley OA check; ResearchGate |
| 32 | `knoblich_ohlsson_1999_insight_problem.pdf` | Knoblich, G., Ohlsson, S., Haider, H., & Rhenius, D. (1999). Constraint relaxation and chunk decomposition. *JEP:LMC, 25*(6), 1534-1555. | 10.1037/0278-7393.25.6.1534 | Try Unpaywall; check ResearchGate |
| 33 | `staw_sandelands_dutton_1981_threat_rigidity.pdf` | Staw, B.M., Sandelands, L.E., & Dutton, J.E. (1981). Threat-rigidity effects in organizational behavior. *ASQ, 26*(4), 501-524. | 10.2307/2392337 | Try Unpaywall; JSTOR with institutional access or author repositories |
| 34 | `arkes_blumer_1985_sunk_cost.pdf` | Arkes, H.R., & Blumer, C. (1985). The psychology of sunk cost. *OBHDP, 35*(1), 124-140. | 10.1016/0749-5978(85)90049-4 | Try Unpaywall; ResearchGate |
| 35 | `nickerson_1998_confirmation_bias.pdf` | Nickerson, R.S. (1998). Confirmation bias. *Review of General Psychology, 2*(2), 175-220. | 10.1037/1089-2680.2.2.175 | Try APA; this is a widely cited review — likely available |

### Folder: `docs/papers/04_group_social_mechanisms/`

| # | Filename to save as | Citation | DOI | Notes |
|---|---|---|---|---|
| 36 | `clark_wilkes_gibbs_1986_referring_collaborative.pdf` | Clark, H.H., & Wilkes-Gibbs, D. (1986). Referring as a collaborative process. *Cognition, 22*(1), 1-39. | 10.1016/0010-0277(86)90010-7 | **PRIORITY 1** — foundational paradigm. Try Unpaywall; Stanford repository; ResearchGate |
| 37 | `brennan_clark_1996_conceptual_pacts.pdf` | Brennan, S.E., & Clark, H.H. (1996). Conceptual pacts and lexical choice. *JEP:LMC, 22*(6), 1482-1493. | 10.1037/0278-7393.22.6.1482 | Try Unpaywall; Stony Brook repository (Brennan) |
| 38 | `garrod_doherty_1994_conversation_coordination.pdf` | Garrod, S., & Doherty, G. (1994). Conversation, co-ordination and convention. *Cognition, 53*(3), 181-215. | 10.1016/0010-0277(94)90047-7 | Try Unpaywall; University of Glasgow repository (Garrod) |
| 39 | `metzing_brennan_2003_conceptual_pacts_broken.pdf` | Metzing, C., & Brennan, S.E. (2003). When conceptual pacts are broken. *JML, 49*(2), 201-213. | 10.1016/S0749-596X(03)00028-7 | Try Unpaywall; Stony Brook or Göttingen repository |
| 40 | `pickering_garrod_2004_mechanistic_psychology.pdf` | Pickering, M.J., & Garrod, S.C. (2004). Toward a mechanistic psychology of dialogue. *BBS, 27*(2), 169-226. | 10.1017/S0140525X04000056 | Try Cambridge BBS; Edinburgh repository (Pickering) |
| 41 | `hawkins_frank_goodman_2020_reference_games.pdf` | Hawkins, R.D., Frank, M.C., & Goodman, N.D. (2020). Characterizing the dynamics of learning in repeated reference games. *Cognitive Science, 44*(6), e12845. | 10.1111/cogs.12845 | Try Unpaywall; likely available on PsyArXiv or author site at Stanford |
| 42 | `hawkins_frank_goodman_2023_partners_populations.pdf` | Hawkins, R.D., Frank, M.C., & Goodman, N.D. (2023). From partners to populations. *Psychological Review, 130*(4), 890-915. | 10.1037/rev0000360 | Try Unpaywall; check PsyArXiv preprint |
| 43 | `centola_baronchelli_2015_emergence_conventions.pdf` | Centola, D., & Baronchelli, A. (2015). The spontaneous emergence of conventions. *PNAS, 112*(7), 1989-1994. | 10.1073/pnas.1418838112 | PNAS is open access — should be freely available at `https://www.pnas.org/doi/10.1073/pnas.1418838112` |
| 44 | `young_1993_evolution_conventions.pdf` | Young, H.P. (1993). The evolution of conventions. *Econometrica, 61*(1), 57-84. | 10.2307/2951778 | Try Unpaywall; JSTOR; check Johns Hopkins repository |
| 45 | `van_huyck_battalio_beil_1990_coordination_failure.pdf` | Van Huyck, J.B., Battalio, R.C., & Beil, R.O. (1990). Tacit coordination games. *American Economic Review, 80*(1), 234-248. | 10.2307/2006968 | Try AEA/JSTOR or Unpaywall |
| 46 | `stasser_titus_1985_unshared_information.pdf` | Stasser, G., & Titus, W. (1985). Pooling of unshared information in group decision making. *JPSP, 48*(6), 1467-1478. | 10.1037/0022-3514.48.6.1467 | Try Unpaywall; ResearchGate |
| 47 | `wegner_1987_transactive_memory.pdf` | Wegner, D.M. (1987). Transactive memory. *Review of Personality and Social Psychology, 9*, 185-208. | N/A (book chapter) | Try ResearchGate; author repository; may be partially on Google Books |

### Folder: `docs/papers/05_methodological_precedents/`

| # | Filename to save as | Citation | DOI | Notes |
|---|---|---|---|---|
| 48 | `meiran_1996_task_switching.pdf` | Meiran, N. (1996). Reconfiguration of processing mode prior to task performance. *JEP:LMC, 22*(6), 1423-1442. | 10.1037/0278-7393.22.6.1423 | Try Unpaywall |
| 49 | `monsell_2003_task_switching.pdf` | Monsell, S. (2003). Task switching. *Trends in Cognitive Sciences, 7*(3), 134-140. | 10.1016/S1364-6613(03)00028-7 | Try Unpaywall; Exeter repository |
| 50 | `hills_et_al_2015_exploration_exploitation.pdf` | Hills, T.T., et al. (2015). Exploration versus exploitation in space, mind, and society. *Trends in Cognitive Sciences, 19*(1), 46-54. | 10.1016/j.tics.2014.10.004 | Try Unpaywall; Indiana University repository |
| 51 | `lazaridou_2017_emergent_language.pdf` | Lazaridou, A., Peysakhovich, A., & Baroni, M. (2017). Multi-agent cooperation and the emergence of natural language. ICLR 2017. | N/A | Try `https://openreview.net/forum?id=Hk8N3Sclg` or arXiv |

---

## Additional Papers Worth Searching (not in primary list but mentioned in review)

Search for and download if openly available:

- **Audia & Brion (2007)** — "Reluctant to change" — AMJ — follow-up to Audia et al. (2000)
- **Brehmer (1980)** — "In one word: Not from experience" — Acta Psychologica — feedback and learning
- **Krauss & Weinheimer (1964, 1966)** — original reference game studies — Psychonomic Science / JPSP
- **Clark & Schaefer (1989)** — "Contributing to discourse" — Cognitive Science
- **Hollingshead (1998)** — "Communication, learning, and retrieval in transactive memory systems" — JESP
- **Cannon-Bowers, Salas & Converse (1993)** — "Shared mental models" — chapter in Castellan book

---

## Output File

After completing all downloads, create a file at:
`docs/papers/DOWNLOAD_REPORT.md`

With two sections:
1. **Successfully downloaded** — list each paper with filename and file size
2. **Could not download** — list each paper with full citation, DOI, and the URLs tried (so the researcher can get them through campus library access instead)

---

## Notes

- The researcher's email is `james.p.houghton@gmail.com` (use for Unpaywall API calls if needed)
- Verify PDFs are real by checking file starts with `%PDF` — reject HTML error pages
- Prioritize papers marked **PRIORITY 1** in the notes column
- The NTNU mirror URLs (`http://www.iot.ntnu.no/innovation/norsi-pims-courses/...`) are the most promising source for the March/Levitt/Levinthal/Henderson/Tushman/Hannan papers — try those first with `curl -L`
- For PNAS papers (Centola & Baronchelli), always try `https://www.pnas.org/doi/{DOI}` directly as PNAS is fully open access
- For ICLR and arXiv papers, try `https://arxiv.org/search/?query={title}&searchtype=all`
