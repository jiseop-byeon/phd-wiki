---
title: 4. Scientific Writing & Peer Review
tags: [research, writing, peer-review]
---

## English

Scientific writing aligns a claim with evidence and makes its boundary inspectable. Clarity is not decoration: ambiguous scope, hidden assumptions, and missing protocol prevent readers from evaluating the work.

> [!note] Prerequisites
> [[06-research-practice/research-questions-claims|Research Questions & Claims]] · [[06-research-practice/experimental-design-reproducibility|Experimental Design]] · [[06-research-practice/failure-analysis-system-evaluation|Failure Analysis]]

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

과학적 글쓰기는 주장을 증거와 정렬하고 그 경계를 검사 가능하게 만든다. 명료함은 장식이
아니다: 모호한 범위, 숨은 가정, 빠진 프로토콜은 독자의 평가 자체를 막는다.

> [!note] 선수 지식
> [[06-research-practice/research-questions-claims|연구 질문과 주장]] · [[06-research-practice/experimental-design-reproducibility|실험 설계]] · [[06-research-practice/failure-analysis-system-evaluation|실패 분석]]

### 1. 논문 수준의 논증

| 섹션 | 주된 역할 |
|---|---|
| Abstract | 문제, 방법, 범위가 한정된 가장 강한 증거, 함의 |
| Introduction | 중요성, 정확한 gap, 접근, 기여 |
| Related work | 분류 체계와 차이 — 인용 목록이 아니라 |
| Method | 변수, 가정, 알고리즘/시스템, 재현 가능한 세부 |
| Experiments | 질문, 프로토콜, 베이스라인, 지표, 결과 |
| Discussion | 해석, 기전, 일반화, 트레이드오프 |
| Limitations | 유효성의 경계와 미해결 위험 |

Introduction이 일반적 능력을 약속하고 실험은 좁은 조건 하나만 시험하게 두지 말라.

### 2. 주장–방법–증거 문장

권장: "Held-out 자재 배치에서, 우리 정책은 짝지은 BC 대비 폐루프 성공률을 X에서 Y로
높였다 (조건당 Z회 시행)."

피하라: "우리의 지능적 프레임워크는 강건한 건설 자율성을 혁신한다." 두 번째 문장에는
조작적 주장, 비교 대상, 범위, 증거가 없다.

### 3. Related work는 분류 체계다

문제 가정, 표현, 지도 방식, 계획/제어 인터페이스, 평가 체제로 논문들을 묶어라. 각 묶음의
끝에 당신의 연구가 시험하는 미해결 차이를 적어라. 연대순 나열은 역사 자체가 gap을
설명할 때만 유용하다.

### 4. 그림과 표

시스템 그림은 런타임 정보 흐름, 학습/동결 구성요소, 필요하면 프레임·주기, 학습/추론
차이를 보여야 한다. 결과 표에는 단위, 개선 방향, 불확실성, 시행 수, 명확한 최고값 표기가
필요하다. 캡션은 본문을 뒤지지 않고도 이해돼야 한다.

### 5. Results와 Discussion

Results는 측정된 결과를 보고한다. Discussion은 원인, 한계, 이전 가능성을 해석한다.
"방법 A의 실패가 적었다"는 result다; "촉각 피드백이 더 이른 미끄럼 회복을 가능하게 했다"
는 진단 증거를 요구하는 기전적 해석이다.

### 6. Limitations

시험하지 않은 환경, 데이터·컴퓨트 의존성, 하드웨어 가정, 개입/리셋, 실패 모드, 안전
경계, 가능성 높은 분포 이동을 명시하라. Limitations는 논문을 약하게 만드는 것이 아니라
근거 없는 일반화를 막는다.

### 7. Peer review

각 코멘트를 사실 정정, 명료화 요청, 증거 부족, 범위 이견, 선호로 분해하라. 응답 방식:

- **Agree:** 인정하고 수정한다.
- **Clarify:** 오해를 설명하고, 다른 독자가 같은 오해를 하지 않게 논문을 고친다.
- **Revise:** 분석·실험·인용·한계를 추가한다.
- **Rebut:** 증거와 범위로, 요구된 결론이 따라 나오지 않음을 정중히 보인다.

원고의 어디가 바뀌었는지 정확히 밝혀라. 새 실험이 측정한 것 이상을 증명한다고 주장하지
말라.

### 8. 산출물 정렬

논문, 부록, 코드, 데이터, 모델, 설정, 로그, 비디오는 호환되는 버전과 식별자를 참조해야
한다. 비디오는 행동을 보여 주지만 시행 분포와 실패 횟수를 대신하지 못한다.

### 읽고 나면 말할 수 있어야 하는 것

- 범위가 한정된 주장–방법–증거 문장을 쓸 수 있다
- 논문 각 섹션의 고유한 역할을 설명할 수 있다
- Related work를 유용한 분류 체계로 조직할 수 있다
- 측정된 결과와 기전적 해석을 분리할 수 있다
- Limitations를 유효성 경계로 쓸 수 있다
- 리뷰어 코멘트를 분류하고 추적 가능한 수정으로 답할 수 있다

### 스스로 점검

1. "우리 방법은 실세계에서 강건하다"에 빠진 것은?
2. Results와 Discussion을 분리해야 하는 이유는?
3. 검증하기 쉬운 응답 편지의 조건은?
4. 잘 다듬은 데모 비디오가 증거로 불충분한 이유는?

> [!tip]- 정답 · Answers
> 1. 방법, 비교 대상, 강건성/실세계의 조작적 정의, 조건, 시행 수, 지표, 불확실성, 실패.
> 2. 관찰과 인과적·일반화 해석을 구분하기 위해.
> 3. 우려를 인용·분해하고, 직접 답하고, 증거/수정을 기술하고, 정확한 위치를 준다.
> 4. 선택 편향, 생략된 실패/리셋, 알 수 없는 노출, 짝지은 베이스라인 부재.
