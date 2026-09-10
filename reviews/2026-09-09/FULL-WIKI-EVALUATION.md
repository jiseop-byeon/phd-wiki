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

### 4.1 Actions taken (2026-09-09)

All four weaknesses above were addressed after this report was written.

| # | Weakness | Action |
|---|---|---|
| 1 | Korean half thinner | Seven haptics pages rewritten. Restored display equations the Korean text referred to as "위 식" without showing, two Mermaid diagrams, the prerequisite and reading tables collapsed into prose, the seven-item annotated reading list with its DOIs, and the missing zero-order-hold caveat in 24.4 §3. Track ratios now 0.69–0.90, previously 0.32–0.49. |
| 2 | Depth drift | The research-program §7 claim replaced in both halves with the measured distribution (136 Working / 72 Literacy / 7 Mastery), the note that 52 of the 72 Literacy pages are paper notes, and the instruction to read the counts as an instrument rather than a target. |
| 3 | Untraceable numbers | Scaling law identified as Lin et al., arXiv:2410.18647, with its abstract wording checked. ConRFT (arXiv:2502.05450) and RECAP (arXiv:2511.14759) cited. HIL-SERL's 27%/18%/100% marked body figures, since its abstract carries only the 1–2.5 h and 2x claims. The π0 UPenn figures could not be traced through arXiv search and are now marked "source not located, do not cite from here" in both halves. |
| 4 | Volatile page undated | `physical-ai-ecosystem` given `last_verified: 2026-09-09` and a bilingual staleness warning. |

### 4.2 Full bilingual parity audit (2026-09-09)

Weakness 1 was then re-opened and settled across the whole wiki. Two corrections to §4 first.

**The "91 of 201" census does not reproduce.** By word ratio, 23 of 208 bilingual pages fall
below 0.75. The figure near 91 appears only when Korean is measured by character count, which
returns 136 — and character count is not a defect signal, because Korean says the same thing
in fewer characters. Word ratio is a weak proxy too. The instrument that actually works is a
section-by-section comparison of the two halves.

**Method.** Eight readers compared both halves of all 208 bilingual pages in full, looking for
five defect classes: a Korean sentence pointing at an equation or table that exists only in
English, a missing artifact, a table or list collapsed into prose, a lost caveat, and a
contradiction between the halves. A mechanical pass counted artifacts per half beforehand.

**Result: 22 defects across 19 files, all repaired.** The commonest were dropped citations
(GAE's arXiv id, four article titles in the legged-locomotion source list, the authors of the
Nature aerial-manufacturing paper) and self-check answers reduced to the bare result, losing
the verification step the answer exists to teach. Two were contradictions. The navigation note
told Korean readers not to extrapolate a 23% figure while the English half told them to assume
it until shown otherwise. The PlaNet note's Korean topic marker reversed which system leads.
One repair went the other way: the Apolinarska note asserted in English that the platform's
control mode is in the paper's appendix, while the Korean half said, more carefully, that the
sources consulted do not name it. The Korean statement is now used in both.

**A larger defect surfaced underneath.** Bilingual callouts are authored once, in the English
half, so the language toggle hid them from every Korean-mode reader. That affected 145 pages,
including prerequisite lists and depth targets. It also hid the research radar dashboard.
Fixed in the toggle rather than in the content: an English-half block containing Hangul, or an
embedded widget, is now tagged so neither filter hides it. Verified in a browser with no
leakage in either direction.



### 4.3 The depth-drift finding, settled (2026-09-09)

Weakness 2 was recorded as a measurement and left as a judgement call. It is now decided,
and the judgement in §4 was **wrong in its conclusion though right in its numbers**.

"Working has become the default, which blunts the filter" compares the distribution against
the research program's rhetoric. The operative instrument is the study guide, and its own
area table prescribes Working in **nine of twelve rows**. Applying the guide honestly
produces a Working majority; the majority is therefore not evidence of anything.

The decidable question is narrower: does any page sit *deeper* than its area allows? Mapping
all 204 pages that fall under a guide row against both the generic area table and the sharper
construction-manipulation profile gives **one** such page — the Dreamer note, still at Working
after the paper was re-marked ◐, and its own `wiki-support` already read Literacy. Demoted.
The other **40** deviations all run the opposite way: Literacy where the guide would permit
Working, mostly historical foundations notes (AlexNet, VGG, LSTM, BERT, GPT-3) and index
pages. The filter is conservative, not blunt.

Made standing rather than reported. `scripts/audit_depth.py` is check 14: it reads both
tables out of the guide and fails on any page deeper than its area allows, on a documented
promotion set for the eight methods the guide's own "directly used methods at Working" clause
covers, and on a wording change to either table — so the check cannot be silently retired.
Check 12 now also verifies the four self-counts the research program states (135 / 73 / 7,
and 53 of the 73 in chapter 01). Seven regressions were re-introduced and caught.

### 4.4 The undefined-term detector, run and triaged (2026-09-10)

§7 lists this detector as not run. Run: **172 concepts used but not taught, 0 indexed by two
or more books**, which is the only signal the detector printed, so the headline number was
unreadable. All 172 were classified by hand against the wiki's own admission rule — frequency
of encounter.

The list was almost entirely artifacts. The four most frequent hits (`critic`, `statistic`,
`dream`, `adopt`) are morphology and ordinary English; the wiki teaches *critics* and
*statistics* and the detector compared surface forms. Below them sat place names, one-off
paper vocabulary, and generic phrases (`design of`, `advantages of`, `in psychology`).

**One term survived**: `encoder-decoder`, used in six files — the lineage page and the
seq2seq, Transformer, MAE, U-Net and DETR notes — and taught in neither study chapter nor
the glossary. Added as a glossary entry, one clause, per the standing rule that glossing a
term the wiki's own prose already uses is always in scope.

Rather than record the triage as prose, the detector now performs it. Inflections are folded
to a stem to a fixpoint, and hits are ranked by how many files use the phrase and cut at
`FREQ_FLOOR = 5` — the admission rule made mechanical. The report is now 149 raw hits, 0 above
the floor, and reading it takes seconds.

**A second finding, from the same work.** Inserting one glossary entry required knowing the
sort order, and measuring it showed the convention is case-insensitive with punctuation *and*
spaces ignored. Under that key two entries had slipped — `Spatial memory` before `SNR · dB`,
and `Visuotactile` before `Virtual coupling`. Fixed, and the ordering is now check 15, since
the wiki had held this rule by hand across 229 entries with nothing enforcing it.

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
