# Full-wiki read and evaluation

- Date: 2026-09-09
- Commit evaluated: `b9cf46b`; fixes applied in `19e27f5`
- Scope: every one of the 215 published pages in `content/`, both `## English` and `## 한국어` halves, ~470,000 words
- Method: eight parallel chapter-by-chapter reads, plus corpus-wide checks and independent verification of every P1 by the coordinator

## What was actually done

The corpus was divided into eight groups and each was read end to end — not sampled. Reported
coverage: 14 foundations pages, 24 robotics pages, 19 Modern Robotics and haptics pages, 23
construction/practice/program/radar pages, 40 deep-learning paper notes, 42 VLA/world-model/
diffusion/robotics notes, 45 construction and navigation notes, and the nine entry-layer and
chapter-3 files.

Four corpus-wide checks were run centrally because no single group could see them: wikilink
resolution across all 4,955 links, self-check answer coverage, frontmatter completeness, and
the ratio of Korean to English in every bilingual page.

**Every P1 in this report was independently confirmed by the coordinator** — by reading the
source passage, recomputing the arithmetic, or fetching the paper's abstract — before being
acted on. One reported P1 was **downgraded** on that check: see §5.

## 1. Verdict

The wiki is in good condition and its distinguishing habit is real. Across eight independent
readers the same observation recurs: the pages take a claim the field repeats, put numbers on
it, and then say what the numbers do *not* establish. Arithmetic survives recomputation
almost everywhere — one reader recomputed roughly forty worked numbers in the robotics track
and another every number in foundations, and both report essentially full reproduction.

Nine statements were found that teach something wrong. All nine are now fixed. That is nine
defects in ~470,000 words across 215 pages, and none of them was in the reasoning — they were
a stale translation, a mislabelled table row, a paper given an encoder it does not use.

## 2. What was wrong, by kind

**Bilingual drift — four of the nine.** This is the dominant failure mode and it has a
mechanism: a correction gets applied to one half and not the other. The clearest case is the
lineage page, where the September 7 audit fixed the English summary sentence from
"tokenization" to "attention-based sequence modeling", fixed the Korean diagram label, and
left the Korean summary sentence — the sentence stating the wiki's whole thesis — untouched.
The others follow the same shape: the Korean AdamW row taught the misconception AdamW exists
to correct; the Korean grasping bullet gave three-fingered hands 12–20 DoF when they are
underactuated at 4–7.

This matters more than the count suggests, because the wiki's own parity tool cannot see it.
`audit_parity.py` compares section *references* between halves and reports zero mismatches —
correctly, since the references do match. Content-level divergence ships silently.

**Attribution — three.** A paper given something it does not contain. Latent Diffusion was
credited with CLIP and T5 text encoders; the paper uses a transformer over a BERT tokenizer.
The AES note said "task variety is narrow (loading)" when that abstract names five task
classes.

**Internal contradiction — two.** Two pages disagreeing with themselves or with the page they
defer to. Force & Compliance §5 ran its impact model at a stiffness §1 says a control loop
never sees, which inverted the section's conclusion; the paper arc listed five candidate tasks
where the domain page's own five criteria clear three.

## 3. What is strong, specifically

- **Provenance discipline.** The habit of writing "the abstract reports no quantitative
  result" or "this is a body figure, not the abstract's" is applied across the paper notes and
  was verified correct in every case a reader checked against a live abstract — GelSight,
  UMI, GELLO, robomimic, Mobile ALOHA, BADGR, Lee 2020, RMA, SemExp, VLN-CE, VLFM,
  ConceptGraphs, NaVid, Uni-NaVid, ViNT/NoMaD among them.
- **Citation integrity.** Thirty-one DOIs, volumes and article numbers in the construction
  notes were resolved against Crossref. No mismatches.
- **Dated, scoped, rerunnable absence claims.** The construction manipulation count names its
  six keywords, two databases, search date, rerun date, named exceptions, an explicit
  exclusion, and two candidate papers deliberately not counted. "A count that is not dated
  cannot be disagreed with, and this one is meant to be."
- **Arithmetic that reproduces.** The LQR Riccati table, the Bode/X-29 derivation, the base-rate
  precision calculation, the binomial and rule-of-three failure regimes, the 2R mass matrix and
  operational-space inertia, the deadly-triad divergence — all recomputed by readers, all correct.
- **Link integrity.** 4,955 wikilinks, one genuinely broken (fixed in `b9cf46b`), four
  intentional template placeholders.

## 4. Open weaknesses

**The Korean half is systematically thinner.** Median Korean-to-English word ratio is 0.76,
and 91 of 201 bilingual pages fall below 0.75. Korean is denser, so a ratio under 1.0 is
expected — but the haptics track at 0.32–0.49 is abridgement, not density. A concrete
instance: the sampling section of 24.4 drops "Conversely, finer resolution does not eliminate
zero-order-hold delay", the reverse half of the point it just made.

**The depth system has drifted from its own rule.** §7 of the research program says the
admission test sends anything that does not directly improve the construction manipulation
question to Literacy, and that "most of this wiki is deliberately Literacy". The actual
distribution is 136 Working, 72 Literacy, 7 Mastery. Chapter 4 has 4 Literacy pages out of 24,
with support-pillar and out-of-scope topics at Working. Mastery assignment is disciplined;
Working has become the default, which blunts the filter.

**Untraceable numbers in three places.** The π0 note's third-party evaluation gives five
figures attributed only to "a third-party study at UPenn" — no authors, no link. The
`rl-basics` 2024–26 callout cites an ICLR 2025 scaling law with no title or authors, and names
ConRFT and RECAP with no citation. These sit on pages that elsewhere insist numbers be
traceable.

**Volatile pages without check dates.** `physical-ai-ecosystem` is half of the home page's
"quick overview" route, lists companies and humanoid hardware, and carries no verification
date, while comparable pages carry a prominent one.

## 5. One reported finding downgraded

A reader flagged the earthmoving page's "24 h ... per human intervention" as a misattribution,
arguing it should read as continuous operation rather than mean time between interventions.
Fetching the Science Robotics abstract settles it: the paper's own sentence is "AES achieves 24
hours per intervention, i.e., the system can continuously operate for 24 hours without any
human intervention." The wiki's meaning was right. The real defect was narrower — the sentence
was broken across lines — and that is what was fixed, together with marking the compact-to-49-t
range as a body figure, since the abstract says only "compact and standard excavators".

## 6. What was fixed

All nine, in both halves, in `19e27f5`. Verified after the edit: `verify_content.py` 217 files
0 problems, `audit_parity.py` 0 mismatches, local build 215 files → 726 outputs, CI green.

| # | Page | Was | Now |
|---|---|---|---|
| 1 | `03-deep-learning/lineage` (KR) | "규모(2012)가 **토큰화**(2017)를 만나" | 어텐션 기반 시퀀스 모델링 |
| 2 | `02-foundations/ml-practice` (KR) | Gaussian-prior reading *is* plain Adam | L2 = decay for SGD; Adam's denominator distorts it |
| 3 | `04-robotics/grasping` (KR) | three-fingered hands 12–20 DoF | underactuated, 4–7; eigengrasps restored |
| 4 | `notes/1-foundations/mae` (both) | DINOv2 = frozen backbone of choice for VLMs | DINO-style when frozen; OpenVLA fuses it; VLMs run CLIP/SigLIP |
| 5 | `notes/6-diffusion/latent-diffusion` (both) | text via CLIP/T5 encoders | transformer over a BERT tokenizer; CLIP arrives with SD |
| 6 | `notes/8-construction/aes` (both) | "task variety is narrow (loading)" | five task classes named; only 24 h is loading |
| 7 | `05-construction/earthmoving` (both) | sentence broken across lines | repaired; 49 t marked a body figure |
| 8 | `04-robotics/force-compliance-control` (both) | impact run at 10⁷ | 10⁵ row added, 10⁷ labelled the idealisation |
| 9 | `07-research-program/paper-arc` (both) | five candidate tasks | defers to the §5 table, which clears three |

## 7. Limits of this evaluation

- Readers read the wiki, not the literature. Where a page attributes a number to a paper, that
  was checked against the paper only when a reader fetched it; roughly thirty abstracts were
  fetched across the eight groups, and each report lists which.
- No textbook was opened. Modern Robotics citations were checked against derivation and recall,
  not against the book.
- Paywalled sources were not read: HEAP's embankment error, Lasota & Shah's percentages,
  Apolinarska's algorithm details, ExT's body figures, among others.
- Rendering was not exercised for most findings. SVG defects are source-level readings.
- The undefined-term detector in `audit_gaps.py` was not run.
