# Papers and pages to fetch through the library

What survived an open-access-only verification pass of every attributed claim in the wiki.
Ten readers checked 165 pages and about 1,000 attributed claims against arXiv abstracts,
ar5iv full text, DOI landing pages, author copies and institutional repositories.

Everything below is currently marked in the wiki as unverified rather than deleted, so no
page depends on it silently. Sci-Hub and similar sites were not used.

## Papers

| Paper | Identifier | What to check |
|---|---|---|
| Johns et al., 2023 — *A framework for robotic excavation and dry stone construction using on-site materials* | 10.1126/scirobotics.abp9758 | Is stone grasping and placement **force-controlled** rather than position-controlled? Find the sentence naming the control mode. |
| Johns et al., 2023 — same paper | 10.1126/scirobotics.abp9758 | Does the per-stone reconstruction estimate **mass or inertial properties**, or only geometry? |
| Zhang et al., 2021 — *An autonomous excavator system for material loading tasks* | 10.1126/scirobotics.abc3164 | Does the **body** give an hourly throughput figure with a unit, as the companion preprint's "145 operations … 36.25 m³ per hour" does? And does it state 6.5 t compact and 49 t standard? |
| Lundeen, Kamat, Menassa & McGee, 2019 — *Autonomous motion planning and task execution in geometrically adaptive robotized construction work* | 10.1016/j.autcon.2018.12.020 | Was the joint-filling study run on a **laboratory testbed or an active site**? The wiki's Michigan-line framing rests on "testbed, not a site". |
| Liang, Kamat, Menassa & McGee, 2022 — *Trajectory-Based Skill Learning for Overhead Construction Robots Using Generalized Cylinders with Orientation* | 10.1061/(ASCE)CP.1943-5487.0001004 | Confirm **82.0% against 71.3%**, and what the 71.3% baseline is. |
| Davila Delgado et al., 2019 — *Robotics and automated systems in construction: Understanding industry-specific challenges for adoption* | 10.1016/j.jobe.2019.100868 | Does the item-level ranking put **high initial capital investment first overall**? |
| Egli, Gaschen, Kerscher, Jud & Hutter, 2022 — *Soil-Adaptive Excavation Using Reinforcement Learning* | 10.1109/LRA.2022.3189834 | Does the method adapt **without identifying the soil**, and over what randomized ranges was it trained? |
| Liu, Habibnezhad & Jebelli, 2021 — *Brain-computer interface for hands-free teleoperation of construction robots* | 10.1016/j.autcon.2020.103523 | Number of subjects, whether trials were lab-only, and whether per-user calibration is stated. |
| Feng, Xiao, Willette, McGee & Kamat, 2015 — *Vision guided autonomous robotic assembly and as-built scanning on unstructured construction sites* | 10.1016/j.autcon.2015.06.002 | Does the paper itself introduce the term **"reversed spatial relationship"**, and is fiducial-marker metrology the localization method? |
| Liang, Wang, Kamat & Menassa, 2021 — *Human–Robot Collaboration in Construction: Classification and Research Trends* | 10.1061/(ASCE)CO.1943-7862.0002154 | A citation count **with its index named**. Crossref returned 209 and Semantic Scholar 145 on the same day; the page previously said 283. |
| Kim & Cho — *Adaptive 3D Scanning and View Planning for Autonomous Mobile Robots* | 10.1061/JCCEE5.CPENG-7252 | The official publication year. JCCE volume 40 is 2026; the wiki calls it 2025. |
| Dietrich, Ott & Albu-Schäffer, 2015 — *An overview of null space projections for redundant, torque-controlled robots* | 10.1177/0278364914566516 | Confirm that only the dynamically consistent inverse satisfies $JM^{-1}N^\top = 0$, and that a Moore-Penrose projector is already statically consistent. |
| Axehill & Morari, 2012 — *An alternative use of the Riccati recursion for efficient optimization* | 10.1016/j.sysconle.2011.09.018 | Does the paper state a flop count **quadratic in the horizon** for its Cholesky factorization? |
| Unhelkar, Lasota et al., 2018 — *Human-Aware Robotic Assistant for Collaborative Assembly* | RA-L 3(3) | Confirm the authors' own statement that the BMW test environment is not representative of a real factory deployment. |

## Books and standards

| Source | What to check |
|---|---|
| Springer Handbook of Robotics, 2nd ed., ch. 38 (10.1007/978-3-319-32552-1) | Does ch. 38 state that under the **hard-finger** model some 3D geometries admit force closure with **three** non-collinear contacts? |
| Same handbook, grasping chapter bibliography | Is Ferrari & Canny, *Planning optimal grasps*, misdated **1986** there? The correct date is ICRA 1992, pp. 2290–2295. |
| ISO/TS 15066:2016, §5.5.4 | Confirm the protective separation distance as the six-term sum $S_p = S_h + S_r + S_s + C + Z_d + Z_r$, with those term definitions. |

## Publisher pages that block automated access

These need a browser session, not a subscription.

| Page | What to check |
|---|---|
| IJRR submission guidelines, journals.sagepub.com/author-instructions/IJR | The sentence "the mere inclusion of more details, experiments, or discussion is typically considered not substantial", and the **≤80-word** novelty-statement limit. |
| *Automation in Construction* and *J. Computing in Civil Engineering* guides for authors | Review model: single- versus double-anonymized, and whether an editor screens before ≥2 reviewers. |
| *Science Robotics* editorial policy | The editorial triage timeline ("1–2 weeks") and ≥2 external referees. |

## Cleared during this pass

- Lasota & Shah's five percentages — all five match the authors' own copy exactly.
- HEAP's embankment errors — "0.03 m average error" and "0.05 m average error" confirmed verbatim in the ETH copy.
- Apolinarska's robot platform — appendix A.2 names an ABB IRB4600-40/2.55 on an overhead gantry, driven through Externally Guided Motion at 50 Hz with a BOTA force-torque sensor. The paper is open access; no fetch needed.
- The π0 third-party evaluation — located at the Penn GRASP Lab project page, and the note now cites it.

## Library session, 2026-09-12

Read through UT Libraries EZproxy in a browser the user signed into. ASCE, IEEE Xplore, SAGE,
SpringerLink and science.org information pages opened; ScienceDirect refused the automated
browser, and UT has no *Science Robotics* subscription.

Cleared, with what changed in the wiki:

- **Dietrich, Ott & Albu-Schäffer 2015** — static consistency holds for every weighting matrix
  (§3.2); only the inertia-weighted pseudoinverse satisfies $JM^{-1}N=0$ within that form
  (Khatib 1987, §3.3.1), but a differently structured projector $M(I-J^{+}J)M^{-1}$ is also
  dynamically consistent (§3.3.2). The force-control page now says so.
- **Liang et al. 2022, JCCE** — 82.0% and 71.3% are both in the paper but come from different
  tables: same-condition comparisons are 75.3 vs 71.3 (Table 1, 150 trials) and 82.0 vs 66.0
  (Table 3, 100 trials at new locations). Generalized cylinders come from Ahmadzadeh & Chernova
  2018; this paper adds orientation. Note corrected.
- **Egli et al. 2022, soil-adaptive** — adapts without explicit soil parameters, confirmed; ranges
  from Table I now in the note. **The note was wrong on two points**: the policy is a memoryless
  128-128 MLP, not recurrent, and it does not reuse the learned actuator model (joint-velocity
  commands tracked by PID + feed-forward valve-flow controllers). Also checked the sibling
  general-approach paper: pilot-stage commands, no fine-tuning, M545 12 t — all confirmed.
- **Kim & Cho, JCCE** — Volume 40, Issue 5, published online 2 June 2026, print September 2026;
  tested in simulation and at a disaster site. Every "2025" mention of it changed to 2026.
- **Liang, Wang, Kamat & Menassa 2021** — five levels (Preprogramming 135, Adaptive
  Manipulation 72, Imitation Learning 3, Improvisatory Control 18, Full Autonomy 31; 259 total).
  The note's "which sit empty" was wrong; none is empty. Citation count left as index-named.
- **Unhelkar, Lasota et al. 2018** — confirmed in §VII: one robot, one worker, small cell, "not
  representative"; quantitative results from simulation. Detail added.
- **Springer Handbook ch. 38** — §38.4.2 gives two soft-finger or three non-collinear hard-finger
  contacts for force closure (seven for form closure); reference [38.44] does misdate Ferrari &
  Canny as 1986. Attribution now marked read.
- **IJRR guidelines** — "not substantial" sentence, ≤80-word novelty statement, conference
  version upload, single-anonymized, ≥2 referees: all confirmed verbatim.
- **Science Robotics information for authors** — ~1–2 weeks for papers not selected, ≥2 outside
  referees, 4-week reviewer deadline. The wiki's "rejects most" was not on the page and was removed.
- **ASCE journals (JCCE)** — ASCE-wide single anonymous peer review with a chief-editor scope
  check, confirmed.

Still open — need the PDFs saved from a normal browser:

- Johns et al. 2023 and Zhang et al. 2021 (*Science Robotics*, no UT subscription).
- Lundeen 2019, Davila Delgado 2019, Liu 2021, Feng 2015, Axehill & Morari 2012 (ScienceDirect).
- *Automation in Construction* guide for authors (ScienceDirect).
- ISO/TS 15066:2016 §5.5.4 (not attempted).
