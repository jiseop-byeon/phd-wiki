---
title: "{{Course page}}"
tags: [curriculum]
study-depth: Working
depth-goal: "Complete the problem set of this page's tier from the wiki alone."
mastery-when: "Raise when the plant or method on this page carries the thesis contribution."
wiki-support: Working
---

<!--
Three-tier contract for every course page: 02-foundations, 04-robotics, and the
03-deep-learning modules. A haptics course is the bar: a specific object, then
draw / derive / run / change one knob.

The lecture, not the answer key, is the main product. Before the problem set, the page
must show the object in one picture, derive on the named object with the catalog numbers, and
work one numerical case in full. The problem set is a *variant* (a different pose, a
changed knob, an interpretation). A page that only appends problems to a summary has
not met the bar.

Reader depth may be Literacy; the note is still this course. Do not shorten the lecture
because the recommended study-depth is Literacy.

Tier A (Lab): named object + diagram + derivation + Python loop + parameter sweep.
Tier B (Derive): named object + diagram + hand derivation + hand problem set. No new simulator.
Tier C (Read): claim-reading homework only. Allowed only for a reading map or an index —
a page whose subject can be derived is Tier B, not Tier C.

1. OBJECT CATALOGS. Physical pages name a plant P1-P6 from 0.6 Lab Plants; deep-learning
pages name a tensor object D1-D6 from 3.0 Lab Objects. Reuse before inventing: add a new
catalog entry only when the page needs a different *kind* of object, and then say on the
page how it differs from the nearest existing one (D1 is 2->3->2 softmax, P1 is 2->3->1 MSE).
A page may freeze its own small object when no catalog entry fits (a 5-keypoint skeleton,
a 3x3 elevation patch); specify it completely once and never change its numbers later.

2. SCOPE HONESTY. A page titled with a whole field (computer vision, VLA, planning) must
say what it teaches and what it does not, and where the rest lives. If the field needs
more than one object, split it into sub-pages in the folder and keep index.md as the map.
One 50-line page does not become a course by declaring wiki-support: Working.

3. TIER A TRIGGER. If the subject *is* numerical computation - tensors, sampling, iteration,
stability boundaries, timing - a hand derivation alone is not the lecture: the page owes a
runnable loop and a sweep. Deep-learning modules are in this class.

4. DEFINITION COMPLETENESS. Every concept the page itself defines needs: what kind of thing
it is; every defining condition named (linearity is additivity AND homogeneity; LTI is
linearity AND time invariance); the formula on one $$ line with each symbol explained; an
example and, where readers go wrong, a non-example; why it matters. A metric used in a
table (IoU, mAP, ECE, MPJPE) is defined where it is first used or linked to the page that
defines it. Concepts defined elsewhere get a section link, never half a definition.
Reference: 0.5 Engineering Math §4.5 (linearity) and 6. Signal Processing §1 (LTI).

5. ONE SKELETON. Every course page carries the same headings in both halves, in this order:
Prerequisites callout, First pass callout, Running object, The picture, Worked case,
numbered lecture sections, then the wiki's standing tail - After reading (where the page has
one), Self-check (+ Answers), Problem set · 과제 (tier line, Draw / Derive / Do or Interpret,
Solutions), Sources. Do not invent per-track variants such as "Exit check".
The Worked case may sit right after The picture only if it reads at that position: every
term, symbol and formula it uses is defined in the Prerequisites, the Running object or the
picture, or glossed in one line with a pointer to the section that derives it. If it would
need more than three such glosses, it goes after the lecture sections it depends on (before
After reading) - a worked case that cites what the reader has not met yet does not teach.

10. HONEST PREREQUISITES. The Prerequisites callout lists every page the lecture actually
leans on, and none that comes later in study order (scripts/audit_prereqs.py reports both).
A concept the page uses must be taught on this page, on a listed prerequisite, or linked at
first use - never used as if known.

6. wiki-support: Working means the page's own problem set is completable from the page,
its prerequisites, and the object catalog - nothing else. If it is not, the honest value
is Literacy until the lecture is written.

7. CODE THAT RUNS. Every ```python block that is not a `?`-blank template or ROS code is
executed in CI by scripts/check_lab_code.py, NumPy and the standard library only. A page's
blocks run in order in one namespace, like a notebook, so a later block may use what an
earlier block defined. A published table must be the printed output of the published code.
An intentional fragment (a deliberate error, an excerpt of a larger program) starts with the
line `# not-run: <reason>`.

8. ONE RUNNING OBJECT PER TRACK. Foundations and Robotics reuse P1-P6, deep learning reuses
D1-D6, and research practice reuses the frozen study RS1 (06-research-practice/index.md).
The Robotics track ends in a capstone (26) that assembles the running task end to end; a
new stage page links the capstone step it owns.

9. THE PICTURE IS DRAWN. "The picture · 그림으로 먼저 보기" shows the page's one key figure
itself - the worked case's version, with its numbers and labels - in both halves (Korean
labels in the Korean half). Under it sits a caption of two or three sentences: what the
figure shows and its key numbers, nothing else. How to draw it yourself belongs to the
problem set, in a collapsed "How to draw it · 그리는 법" callout after the numbered items;
the Draw item asks for the variant.
Geometry, plots, timelines and phase portraits are inline SVG whose coordinates are computed
from the page's numbers (currentColor so the figure follows the light/dark theme; viewBox 560
wide so it scales to a phone; ids unique per figure). Graphs, pipelines and state machines
may be mermaid. A description of a figure without the figure does not meet the bar.

Do not copy any course's slides or assignments. Original problems. Python only.
Code once in the English half; Korean captions and interprets.
-->

> [!note] Prerequisites · 선수 지식
> [[02-foundations/lab-plants|0.6]] (plant id) or [[03-deep-learning/lab-objects|3.0]] (tensor object id) · [[02-foundations/lab-kernel|0.7]] if this page is Tier A
> [[02-foundations/lab-plants|0.6]](장치 id) 또는 [[03-deep-learning/lab-objects|3.0]](텐서 객체 id) · Tier A이면 [[02-foundations/lab-kernel|0.7]]

## English

*Stands on … First / later use of plant **P?** (or object **D?**).*

> [!note] First pass · 처음이라면
> …

### Running object · 이 페이지의 대상

**P?** from [[02-foundations/lab-plants|0.6 Lab Plants]] (or **D?** from [[03-deep-learning/lab-objects|3.0 Lab Objects]]), at the pose / numbers that page freezes. A page-local object is specified in full here instead.

*Scope: this page teaches … ; it does not teach … , which lives in … .*

### The picture · 그림으로 먼저 보기

(the page's one key figure, drawn with the worked case's numbers; a two- or three-sentence caption)

### Worked case · 대상으로 한 번 끝까지

(derive with catalog numbers; one fully worked numerical case)

### 1. …

(rest of the lecture)

### Problem set · 과제

Tier A / B / C. Using only this page, its prerequisites, and the object catalog. State the tier explicitly — a problem set with no tier line is incomplete.

1. **Draw.** …
2. **Derive.** …
3. **Do** (Tier A) / **Interpret** (Tier B/C). …

```python
# template with ? blanks — Tier A only
```

> [!note]- How to draw it · 그리는 법
> - (what a correct drawing must show, as a short checklist; it applies to the Draw item's variant)

> [!tip]- Solutions
> 1. …
> 2. …
> 3. …

### Self-check

…

> [!tip]- Answers
> …

## 한국어

(same sections, same numbering; Python listing is not repeated)
