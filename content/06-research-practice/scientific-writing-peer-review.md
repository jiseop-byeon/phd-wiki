---
title: 4. Scientific Writing & Peer Review
tags: [research, writing, peer-review]
---

## English

Scientific writing aligns a claim with evidence and makes its boundary inspectable. Clarity is not decoration: ambiguous scope, hidden assumptions, and missing protocol prevent readers from evaluating the work.

### 1. Paper-level argument

| Section | Primary job |
|---|---|
| Abstract | problem, method, strongest scoped evidence, implication |
| Introduction | importance, precise gap, approach, contributions |
| Related work | taxonomy and difference, not a citation inventory |
| Method | variables, assumptions, algorithm/system, reproducible detail |
| Experiments | questions, protocol, baselines, metrics, results |
| Discussion | interpretation, mechanisms, generalization, trade-offs |
| Limitations | boundary of validity and unresolved risks |

Do not let the introduction promise general capability while experiments test one narrow condition.

### 2. Claim–method–evidence sentences

Prefer: “Under held-out material layouts, our policy improved closed-loop success from X to Y over matched BC, with Z trials per condition.”

Avoid: “Our intelligent framework significantly revolutionizes robust construction autonomy.” The second sentence lacks an operational claim, comparator, scope, and evidence.

### 3. Related work as a taxonomy

Group papers by problem assumption, representation, supervision, planning/control interface, or evaluation regime. End each group by stating the unresolved distinction your work tests. Chronological lists are useful only when history itself explains the research gap.

### 4. Figures and tables

A system figure should show runtime information flow, trained/frozen components, frames or rates when relevant, and train/inference differences. A result table needs units, direction of improvement, uncertainty, trial count, and clear best-value conventions. Captions should be understandable without searching the body for basic definitions.

### 5. Results versus discussion

Results report measured outcomes. Discussion interprets causes, limitations, and transfer. “Method A had fewer failures” is a result; “tactile feedback enabled earlier slip recovery” is a mechanistic interpretation requiring diagnostic evidence.

### 6. Limitations

State untested environments, data and compute dependencies, hardware assumptions, intervention/reset, failure modes, safety boundaries, and likely distribution shifts. A limitation section does not weaken a paper; it prevents unsupported generalization.

### 7. Peer review

Decompose each comment into factual correction, clarity request, missing evidence, scope dispute, or preference. Respond with:

- **Agree:** acknowledge and revise.
- **Clarify:** explain the misunderstanding and improve the paper so others do not share it.
- **Revise:** add analysis, experiment, citation, or limitation.
- **Rebut:** respectfully show why the requested conclusion does not follow, using evidence and scope.

State exactly where the manuscript changed. Do not claim a new experiment proves more than it measures.

### 8. Artifact alignment

Paper, appendix, code, data, model, configuration, logs, and video should refer to compatible versions and identifiers. Videos illustrate behavior but do not replace trial distributions and failure counts.

### After reading

- Write a scoped claim–method–evidence sentence.
- Explain each paper section's distinct job.
- Organize related work as a useful taxonomy.
- Separate measured results from mechanistic interpretation.
- Write limitations as validity boundaries.
- Classify and answer reviewer comments with traceable revisions.

### Self-check

1. What is missing from “our method is robust in the real world”?
2. Why should results and discussion be separated?
3. What makes a response letter easy to verify?
4. Why is a polished demonstration video insufficient evidence?

> [!tip]- Answers
> 1. Method, comparator, operational definition of robustness/real world, conditions, trials, metrics, uncertainty, and failures. 2. It distinguishes observations from causal or generalizing interpretation. 3. Quote/decompose the concern, answer directly, describe evidence/revision, and give exact locations. 4. Selection bias, omitted failures/resets, unknown exposure, and missing matched baselines.

## 한국어

Scientific writing은 claim을 evidence와 맞추고 validity boundary를 독자가 검사하게 만드는 일이다. Abstract는 problem–method–scoped evidence, Introduction은 importance–gap–approach–contribution, Related work는 taxonomy와 차이, Method는 가정·변수·시스템, Experiments는 질문·protocol·baseline·metric, Discussion은 해석, Limitations는 유효 범위를 담당한다.

Results에서 측정된 사실과 Discussion의 기전·일반화 해석을 구분한다. 좋은 limitation은 논문을 약하게 만드는 것이 아니라 unsupported generalization을 막는다. Reviewer comment는 factual correction, clarity, missing evidence, scope dispute와 preference로 분해하고 agree·clarify·revise·rebut 중 적절한 방식으로 답하며 수정 위치를 명시한다.

Paper, appendix, code, data, configuration, log와 video의 version을 맞춘다. Demo video는 행동을 보여주지만 trial distribution, failure count와 baseline을 대신하지 않는다.
