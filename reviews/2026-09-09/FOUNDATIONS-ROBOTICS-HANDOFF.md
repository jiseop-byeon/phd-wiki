# Foundations–Robotics audit: continuation brief

## Purpose

Continue the **read-only curriculum audit** of `content/02-foundations/` and
`content/04-robotics/`. The target reader is an engineering graduate student who
has previously taken engineering mathematics and wants research literacy for
Physical AI. Do not assume the repository owner's personal background.

The question to answer is:

> Are Foundations and Robotics independently understandable, mutually integrated,
> and sufficiently complete for reading Physical AI papers accurately?

Do **not** edit wiki content unless the user later gives explicit permission.

## Repository state

- Repository: `/Users/jiseopbyeon/Downloads/phd`
- Audited commit: `e919cbd`
- Public content:
  - `content/02-foundations/` — 14 Markdown files
  - `content/04-robotics/` — 44 Markdown files, including the new haptics track
- Private, gitignored corpus: `reference/`
- Previous full-site audit: `reviews/2026-09-07/FINAL-REVIEW.md`
- Previous implementation record: `.plan/implementation-review.md`

Preserve the user's work and keep `reference/` out of Git.

## Work already completed

### Reference corpus

The entire reference tree was inventoried and text-extracted:

- 231 total files, approximately 1.0 GB
- 191 PDFs
- 13,171 PDF pages
- 28,764,727 extracted characters

Manifest and extracted text are temporary and may survive during this local session:

- `/private/tmp/reference-audit/manifest.tsv`
- `/private/tmp/reference-audit/text/`
- `/private/tmp/reference-files.txt`

The corpus includes:

- canonical texts: Åström–Murray, Boyd, Murphy, MacKay, Sutton–Barto, LaValle,
  Borrelli and Rawlings;
- Matthew Bartos's CE397 control packet;
- Modern Robotics;
- two probability/random-process course sequences;
- optimization, signal-processing and introductory deep-learning lectures;
- haptics/teleoperation and tactile-sensing courses.

All files were indexed and compared by curriculum/topic coverage. Do not claim that
all 13,171 pages received a sentence-by-sentence independent peer review. For any
strong factual conclusion, read the relevant extracted section or original PDF.

### Current wiki integrity

Previously run checks:

- `verify_content.py`: 218 files, 0 problems
- `audit_parity.py`: 0 English/Korean section-reference mismatches
- 123 arithmetic expressions recomputed: 0 unexplained errors
- 0 pages relying on an undeclared study page
- 0 self-check blocks missing answers
- 0 of 100 display equations lacking nearby explanation

The full undefined-term detector in `audit_gaps.py` was interrupted because its
n-gram pass was too expensive. Do not report that detector as completed.

### Cross-track integration

For the 58 Foundation and Robotics pages:

- 1,145 internal links
- 363 unique internal edges
- 35 unique edges from Foundations to Robotics
- 65 unique edges from Robotics to Foundations

This is strong evidence that the two areas are not isolated silos. Inspect semantic
quality, not merely link counts.

## Current high-level finding

The provisional verdict is **conditional pass / well designed for its stated goal**:

- Foundations is independently usable as a prerequisite refresher and paper-reading
  bridge, but is not a first-ever mathematics textbook.
- Robotics is independently usable as a research-literacy map. Modern Robotics
  summaries and some control pages intentionally require linked textbooks/videos
  for Working-level calculation and implementation.
- The integration is unusually strong: linear algebra, probability, optimization,
  signal processing, SE(3) and dynamics feed directly into estimation, perception,
  planning, control, contact and learning.
- No blocking omission was found for **research-literacy entry**.

Do not convert this into the stronger claim that the wiki alone provides Working or
Mastery competence in every topic.

## External benchmarks already checked

Use official/primary sources only for technical comparisons.

- MIT Robotic Manipulation: <https://manipulation.mit.edu/>
- MIT 2025 course description: <https://manipulation.mit.edu/Fall2025/index.html>
- MIT Underactuated Robotics: <https://underactuated.mit.edu/>
- Modern Robotics official supplements:
  <https://modernrobotics.northwestern.edu/chapters/introduction/>
- Feedback Systems: <https://fbswiki.org/wiki/index.php/Feedback_Systems%3A_An_Introduction_for_Scientists_and_Engineers>
- Probabilistic Robotics, MIT Press:
  <https://mitpress.mit.edu/9780262201629/probabilistic-robotics/>
- Dive into Deep Learning: <https://d2l.ai/>
- LaValle, Planning Algorithms: <https://lavalle.pl/planning/booka4.pdf>

The strongest external validation is that MIT Robotic Manipulation organizes the
subject around the same perception–planning–control–contact–learning stack. Its
prerequisites—linear algebra, probability, algorithms and basic neural networks—are
provided explicitly by this wiki.

## Remaining audit tasks

Perform these in priority order. Stop if the additional evidence no longer changes
the conclusion.

### P1 — verify the most plausible remaining conceptual gaps

1. **System identification and model validation**
   - Current explicit coverage is very thin.
   - Determine whether a concise bridge is needed among sensor data, mechanical
     parameters, dynamics, control and sim-to-real.
   - Compare with Underactuated Robotics Chapter 18: kinematic/inertial/friction
     identification, equation vs simulation error, experiment design, residual
     models and online adaptation.

2. **LLN, CLT and empirical uncertainty**
   - The private probability courses treat weak LLN, CLT and confidence intervals
     explicitly; the wiki discusses sample means and uncertainty but does not name
     LLN/CLT clearly.
   - Decide whether a short Probability subsection is needed for interpreting run
     averages, confidence intervals and non-independent robot episodes.

3. **Continuous model to digital controller**
   - Sampling, ZOH, Z-transform, latency, jitter, quantization and haptic stability
     all exist, but are distributed across several pages.
   - Judge whether the existing links form a sufficient bridge or whether one
     explicit overview is warranted.

### P2 — inspect integration details

4. **Markov chain to MDP bridge**
   - MDP/Bellman content is strong, but transition matrices, stationary behavior and
     the Markov-chain foundation are largely implicit.
   - Treat as optional unless it blocks RL/world-model literacy.

5. **Haptics reciprocal integration**
   - Four new haptics subpages have only one inbound link, from the haptics index.
   - Check whether Signal Processing, Control, Robot Systems, HRI and Force Control
     should link back to device design, experiments, Hapkit and human haptics.
   - This is likely a navigation issue, not a missing-content issue.

6. **Closed-chain kinematics**
   - Explicitly marked optional in `content/04-robotics/index.md`.
   - Confirm that omission is acceptable for the stated open-chain, mobile and field
     robotics emphasis. Note that parallel mechanisms, linkages or construction
     equipment may later make it relevant.

### P3 — usability and wording

7. Assess the cognitive load of long bilingual pages. Some pages contain 9,000–12,000
   words across English and Korean. Determine whether first-pass routes and depth
   labels sufficiently prevent readers from becoming trapped in Foundations.

8. Verify or flag these two over-absolute control statements:
   - `content/04-robotics/control-theory-ce397.md`: “Every real implementation has
     anti-windup.”
   - Same page: observer poles “2–5× faster” presented without a clear heuristic
     qualifier.
   - Similar anti-windup language appears in
     `content/04-robotics/modern-robotics/ch11-robot-control.md`.

Recommended interpretation:

- anti-windup is commonly needed when integral action and saturation coexist, not a
  universal property of every implementation;
- 2–5× faster observer dynamics is a rule of thumb whose suitability depends on
  noise, unmodeled dynamics, sampling and actuator/estimator constraints.

## Important intentional omissions

Do not import the entire private curriculum simply because it appears frequently.

- Martingales and advanced random-process theory are not required for the target.
- Global/MIP optimization is optional for scheduling, contact modes and advanced
  TAMP, not a general prerequisite.
- Robust/H-infinity, adaptive and nonlinear control are specialization topics unless
  the thesis contribution depends on them.
- The wiki's goal is research literacy, not uniform technical mastery.

## Expected final deliverable

Return an evidence-backed evaluation, not a list of speculative additions. Separate:

1. **Blocking omissions** for the stated reader and goal;
2. **High-value improvements** that strengthen the bridge;
3. **Optional specialization material** that should stay external;
4. **Independent usability** of Foundations and Robotics;
5. **Integration quality** between them;
6. **Limits of the audit** and what was not independently fact-checked.

A defensible final conclusion should answer explicitly:

- Can the target reader start studying now?
- Where must they follow an external textbook or course?
- Is any missing topic serious enough to interrupt the prescribed path?

Do not use a numerical score unless the rubric is defined. Do not equate source
frequency with curricular importance. Do not edit or deploy anything during the
evaluation phase.

## Useful commands

```bash
cd /Users/jiseopbyeon/Downloads/phd
git status --short
git rev-parse --short HEAD
rg --files content/02-foundations content/04-robotics
rg -n -i "system identification|law of large|central limit|Markov chain|zero-order hold|task-and-motion|closed-chain" content/02-foundations content/04-robotics
python scripts/verify_content.py
python scripts/audit_parity.py
```

Before running any named script, confirm that its current path and CLI still match
the repository. Keep generated reports outside `content/` unless the user explicitly
asks to publish them.
