---
title: 4. Scientific Writing & Peer Review
tags: [research, writing, peer-review]
study-depth: Working
depth-goal: "Apply the procedure when forming claims, running experiments, analyzing failure, and writing."
mastery-when: "Mastery means consistently producing defensible work, not memorizing the page."
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

<svg viewBox="0 0 560 226" style="max-width:100%;height:auto" role="img" aria-label="a claim box drawn inside an evidence box, and the same two boxes with the claim spilling outside the evidence">
  <g font-size="11" fill="currentColor">
    <text x="40" y="16">defensible</text><text x="310" y="16">the common failure</text>
  </g>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.7">
    <rect x="40" y="30" width="210" height="104" rx="4"/>
    <rect x="310" y="46" width="150" height="72" rx="4"/>
  </g>
  <g fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.4">
    <rect x="70" y="52" width="150" height="60" rx="3"/>
    <rect x="340" y="30" width="200" height="104" rx="3" fill-opacity="0.16"/>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="145" y="46">what the evidence covers</text>
    <text x="145" y="86">what the paper claims</text>
    <text x="385" y="86">what the evidence covers</text>
    <text x="440" y="152">what the paper claims</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none">
    <line x1="440" y1="144" x2="440" y2="136"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="310" y="170">this overhang is exactly what gets attacked</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="188">A reviewer is not measuring how large the result is. They are measuring whether one box sits</text>
    <text x="24" y="204">inside the other. Every &#8220;the claim is too strong&#8221; review is a report of the shaded band, and the</text>
    <text x="24" y="220">cheapest fix is almost never a new experiment &#8212; it is narrowing the sentence until it fits.</text>
  </g>
</svg>

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

### 8. Worked example: one review comment, one compliant response

**Reviewer**: "The 85% success rate is unconvincing — only one scene was tested, and the
baseline appears untuned."

**Response (Agree + Revise + Clarify)**: "We agree the single-scene evaluation limited the claim.
We added two held-out scenes with randomized object layouts (§5.2, Table 3): success is
85%, 80%, 80% (17/20, 16/20, 16/20 per scene; binomial SE ≈ 8 %p at this n, so the spread between scenes is inside the noise). On tuning: the BC baseline used the
same demonstrations, encoder, and a 12-configuration hyperparameter sweep identical to
ours (App. C); we now state this in §5.1. We have narrowed the abstract's claim from
'robust manipulation' to 'consistent success across three tabletop scenes.'"

Every element is traceable: the concern is restated, the evidence is located, the
comparison protocol is specified, and the claim is renegotiated to match the data.

### 9. Artifact alignment

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

### Sources

- [Simon Peyton Jones — *How to Write a Great Research Paper* (Microsoft Research)](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/) — the classic talk on claim-first writing
- [IEEE T-RO — Information for Reviewers](https://www.ieee-ras.org/publications/t-ro/t-ro-information-for-reviewers/) — what reviewers at a flagship robotics journal are asked to check

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

<svg viewBox="0 0 560 226" style="max-width:100%;height:auto" role="img" aria-label="증거 상자 안에 들어 있는 주장 상자와, 주장이 증거 밖으로 삐져나온 같은 두 상자">
  <g font-size="11" fill="currentColor">
    <text x="40" y="16">방어 가능한 경우</text><text x="310" y="16">흔한 실패</text>
  </g>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.7">
    <rect x="40" y="30" width="210" height="104" rx="4"/>
    <rect x="310" y="46" width="150" height="72" rx="4"/>
  </g>
  <g fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.4">
    <rect x="70" y="52" width="150" height="60" rx="3"/>
    <rect x="340" y="30" width="200" height="104" rx="3" fill-opacity="0.16"/>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="145" y="46">증거가 덮는 범위</text>
    <text x="145" y="86">논문이 하는 주장</text>
    <text x="385" y="86">증거가 덮는 범위</text>
    <text x="440" y="152">논문이 하는 주장</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none">
    <line x1="440" y1="144" x2="440" y2="136"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="310" y="170">이 삐져나온 폭이 정확히 공격받는 지점이다</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="188">심사자가 재는 것은 결과가 얼마나 큰가가 아니다. 두 상자 중 하나가 다른 하나 안에 들어가는가다.</text>
    <text x="24" y="204">&#8220;주장이 과하다&#8221;는 모든 심사평은 저 음영 띠에 대한 보고이고, 가장 싼 교정은 새 실험이</text>
    <text x="24" y="220">거의 아니다 &#8212; 문장이 맞을 때까지 좁히는 것이다.</text>
  </g>
</svg>

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

### 8. 예제: 리뷰 코멘트 하나, 규범적 응답 하나

**리뷰어**: "85% 성공률은 설득력이 없다 — 장면 하나에서만 시험됐고 베이스라인이 튜닝되지
않은 것으로 보인다."

**응답 (Agree + Revise + Clarify)**: "단일 장면 평가가 주장을 제한한다는 데 동의합니다. 물체
배치를 무작위화한 held-out 장면 2개를 추가했습니다(§5.2, 표 3): 성공률 85%, 80%, 80%(장면당 17/20, 16/20, 16/20. 이 $n$에서 이항 표준오차가 약 8%p이므로 장면 간 차이는 잡음 안이다)
(각 20회, 시드 3개 ±1 std). 튜닝에 대해: BC 베이스라인은 같은 시연·인코더와, 저희와
동일한 12개 구성 하이퍼파라미터 탐색을 사용했습니다(부록 C); §5.1에 명시했습니다.
초록의 주장을 'robust manipulation'에서 '세 탁상 장면에 걸친 일관된 성공'으로
좁혔습니다."

모든 요소가 추적 가능하다: 우려를 재진술하고, 증거의 위치를 밝히고, 비교 프로토콜을
명시하고, 주장을 데이터에 맞게 재협상했다.

### 9. 산출물 정렬

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

### 출처

- [Simon Peyton Jones — *How to Write a Great Research Paper* (Microsoft Research)](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/) — 주장 우선 글쓰기의 고전 강연
- [IEEE T-RO — Information for Reviewers](https://www.ieee-ras.org/publications/t-ro/t-ro-information-for-reviewers/) — 대표 로보틱스 저널의 리뷰어 점검 항목
