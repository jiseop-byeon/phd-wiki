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

An argument is a sequence of dependencies because later claims only make sense after earlier assumptions are visible. For example, [[04-robotics/grasping|Grasping]] moves from closure to grasp quality and then to learning: resisting a wrench is one question, margin against uncertainty is another, and predicting a useful grasp from observations is another. A learned score cannot silently inherit every guarantee of the mechanical model.

**The reading this gives you.** Read a draft by tracing the same chain. Does the problem motivate the chosen model, does the experiment test that model's promised advantage, and does the conclusion stay within those observations? A section can be individually clear while the argument between sections is still missing.

### 2. Claim–method–evidence sentences

Prefer: “Under held-out material layouts, our policy improved closed-loop success from X to Y over matched BC, with Z trials per condition.”

Avoid: “Our intelligent framework significantly revolutionizes robust construction autonomy.” The second sentence lacks an operational claim, comparator, scope, and evidence.

These are hypothetical sentence templates; fill numerical results only from the actual experiment.

**Before:** “Our method robustly handles diverse objects.” **Problem:** diverse and robust have no test boundary. **After:** “On the held-out object set, we report grasp success against a matched baseline, with attempts and failures separated by material.”

**Before:** “Our architecture improves data efficiency.” **Problem:** an advantage at one training budget does not describe a learning curve. **After:** “We compare the methods across predeclared demonstration budgets with the same evaluation protocol and report uncertainty for each budget.”

**Before:** “The robot autonomously completes the task.” **Problem:** assistance can be hidden inside completion. **After:** “We distinguish autonomous completion from completion after an operator stop or reset, retaining every initiated attempt.”

**The reading this gives you.** A useful sentence gives the reader somewhere to check its nouns and verbs: the split, comparator, metric, and accounting rule. Replace the reporting templates with actual outcomes only when those records exist.

### 3. Related work as a taxonomy

Group papers by problem assumption, representation, supervision, planning/control interface, or evaluation regime. End each group by stating the unresolved distinction your work tests. Chronological lists are useful only when history itself explains the research gap.

**Before:** “Paper A used vision. Paper B added touch. Paper C proposed a new planner. Our system combines their advantages.” **Problem:** the reader learns an inventory but cannot locate an unresolved comparison. The final sentence also promises benefits that combining components alone does not establish.

**After:** “We organize grasping methods by when they obtain contact information. Methods that commit from a pre-contact image depend on assumptions about friction and geometry. Methods that update after contact can react to slip, but their value depends on whether sensing and control respond before failure. Our comparison holds the planner fixed and tests that timing boundary.”

This rewrite uses an assumption and an interface as the organizing axes. Actual papers and citations must then be placed in the appropriate groups. **The reading this gives you.** Ask whether each group changes the experiment you would design. If removing the related-work paragraph leaves the claimed gap unchanged, the paragraph may still be a bibliography in prose.

### 4. Figures and tables

A system figure should show runtime information flow, trained/frozen components, frames or rates when relevant, and train/inference differences. A result table needs units, direction of improvement, uncertainty, trial count, and clear best-value conventions. Captions should be understandable without searching the body for basic definitions.

A visual comparison is persuasive because readers perceive height and separation before inspecting a protocol. That makes missing denominators especially consequential. A success-rate bar from a small sample can look just as precise as a bar supported by much more independent exposure.

For example, show the same grasping result first as a bar and then with trial counts, uncertainty intervals, and individual condition labels. The bar invites a ranking. The expanded display lets a reader see whether the apparent lead is uncertain, whether one material dominates the average, and whether repeated runs share the same objects. Neither display changes the data; the second changes which conclusions are visibly defensible.

**The reading this gives you.** Check the unit behind each dot, bar, or interval. A caption should identify the aggregation, interval procedure, and exclusions. If the plot claims generalization, its condition labels should expose the shift rather than hide it in an overall mean.

### 5. Results versus discussion

Results report measured outcomes. Discussion interprets causes, limitations, and transfer. “Method A had fewer failures” is a result; “tactile feedback enabled earlier slip recovery” is a mechanistic interpretation requiring diagnostic evidence.

**Before:** “The tactile system had fewer failures because it understood contact.” **Problem:** the first clause describes an outcome, while the second invents a mechanism without identifying a measurement. **After, results:** “The tactile condition had fewer observed failures under the matched protocol.” **After, discussion:** “Earlier slip detection is a candidate explanation; synchronized sensing and recovery logs are needed to test it.”

**Before:** “The model generalized, proving it learned transferable physical knowledge.” **Problem:** success on a held-out set does not identify the representation responsible. **After, results:** “The model completed tasks on the declared held-out layouts.” **After, discussion:** “This supports transfer across those layouts; transfer to different materials remains untested.”

These hypothetical examples show why keeping interpretation separate is useful even when both parts are eventually supported. **The reading this gives you.** Ask what could be copied directly from a measurement record and what requires an additional argument. Put the extra argument beside its supporting analysis, with alternatives visible.

### 6. Limitations

State untested environments, data and compute dependencies, hardware assumptions, intervention/reset, failure modes, safety boundaries, and likely distribution shifts. A limitation section does not weaken a paper; it prevents unsupported generalization.

**Before:** “Future work will address more challenging conditions.” **Problem:** the reader cannot tell whether a relevant condition failed or was never tested. **After:** “Wet surfaces were not included in evaluation; the present evidence does not establish transfer when contact friction changes.”

**Before:** “The system occasionally needs human assistance.” **Problem:** the phrase hides the trigger and its effect on the autonomy claim. **After:** “The operator resets the robot after loss of localization. These episodes are retained as failed autonomous attempts, and assisted completion is reported separately.”

These are hypothetical boundaries that a real limitation section should replace with documented conditions. Explain whether the boundary is in sensing, training coverage, control, or evaluation. A reader can then decide which change would be needed to use the method elsewhere.

**The reading this gives you.** A limitation should predict where the claim may stop holding. A future-work promise is useful only after the existing failure or missing evidence is explicit; it cannot substitute for that description.

### 7. Peer review

Decompose each comment into factual correction, clarity request, missing evidence, scope dispute, or preference. Respond with:

- **Agree:** acknowledge and revise.
- **Clarify:** explain the misunderstanding and improve the paper so others do not share it.
- **Revise:** add analysis, experiment, citation, or limitation.
- **Rebut:** respectfully show why the requested conclusion does not follow, using evidence and scope.

State exactly where the manuscript changed. Do not claim a new experiment proves more than it measures.

For example, “novelty is unclear” can point to different defects. Check whether the nearest prior method is accurately described, whether the manuscript states a concrete difference from it, and whether the experiment establishes why that difference matters. A system contribution can be legitimate even if no network component is new, but integration effort alone does not answer these questions.

A useful response might explain that the difference is the contact-time state update, add the missing comparison to the taxonomy, and narrow the contribution if the experiment only supports the integrated system. **The reading this gives you.** Treat the comment as a request to locate a missing link in the argument. More adjectives about novelty do not supply that link; a traceable assumption, interface, or evaluation difference does.

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

Alignment matters because individually valid artifacts can describe different experiments. A table may use a checkpoint selected before a controller change, while the released configuration and demonstration video use the later controller. The reader can run the code successfully and still fail to reproduce the reported result.

For example, give each grasping run an identifier that links its configuration, checkpoint, calibration, raw log, and analysis output. Connect every table entry to the included run identifiers and document exclusions. Preserve failed runs too. If a video illustrates a different configuration, label that difference instead of presenting it as the source of the table.

**The reading this gives you.** Trace a result backward from figure to analysis to raw attempt. Ask whether the path ends at the same software and hardware settings that the method describes. Reproducible artifacts are an inspectable chain of evidence, not simply a repository containing files with plausible names.

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

논증은 의존 관계의 순서다. 뒤의 주장을 이해하려면 앞의 가정이 보여야 한다. 예를 들어 [[04-robotics/grasping|파지]]는 닫힘에서 파지 품질을 거쳐 학습으로 이동한다. 렌치를 버티는가, 불확실성에 대한 여유가 있는가, 관측에서 쓸 만한 파지를 예측하는가는 서로 다른 질문이다. 학습 점수가 역학 모델의 보장을 자동으로 물려받지는 않는다.

**여기서 얻는 독법.** 초안에서도 같은 사슬을 찾는다. 문제가 선택한 모델을 필요로 하는가, 실험은 모델이 약속한 이점을 시험하는가, 결론은 관찰 범위에 머무는가를 본다. 각 절이 명료해도 절 사이의 논증은 빠져 있을 수 있다.

### 2. 주장–방법–증거 문장

권장: "Held-out 자재 배치에서, 우리 정책은 짝지은 BC 대비 폐루프 성공률을 X에서 Y로
높였다 (조건당 Z회 시행)."

피하라: "우리의 지능적 프레임워크는 강건한 건설 자율성을 혁신한다." 두 번째 문장에는
조작적 주장, 비교 대상, 범위, 증거가 없다.

다음은 가상 문장 틀이다. 수치 결과는 실제 실험에서 얻은 것만 채운다.

**수정 전:** “다양한 물체를 강건하게 다룬다.” **문제:** 다양성과 강건성의 시험 경계가 없다. **수정 후:** “보지 못한 물체 집합에서 짝지은 베이스라인 대비 파지 성공을 보고하고, 재료별 시도와 실패를 구분한다.”

**수정 전:** “구조가 데이터 효율을 높인다.” **문제:** 한 학습 예산에서의 이점은 학습 곡선이 아니다. **수정 후:** “미리 정한 시연 예산별로 같은 평가 절차에서 비교하고 각 예산의 불확실성을 보고한다.”

**수정 전:** “로봇이 자율적으로 과제를 마친다.” **문제:** 완료 안에 보조가 숨을 수 있다. **수정 후:** “자율 완료와 운전자 정지·리셋 뒤 완료를 구분하고 시작한 모든 시도를 유지한다.”

**여기서 얻는 독법.** 좋은 문장은 분할, 비교 대상, 지표, 집계 규칙을 확인할 위치를 준다. 실제 기록이 있을 때만 보고 계획의 틀을 결과 문장으로 바꾼다.

### 3. Related work는 분류 체계다

문제 가정, 표현, 지도 방식, 계획/제어 인터페이스, 평가 체제로 논문들을 묶어라. 각 묶음의
끝에 당신의 연구가 시험하는 미해결 차이를 적어라. 연대순 나열은 역사 자체가 gap을
설명할 때만 유용하다.

**수정 전:** “논문 A는 시각을 썼다. B는 촉각을 추가했다. C는 새 계획기를 제안했다. 우리 시스템은 장점을 결합한다.” **문제:** 독자는 목록만 얻고 미해결 비교를 찾지 못한다. 부품 결합만으로 입증되지 않은 이점도 약속한다.

**수정 후:** “파지 방법을 접촉 정보를 얻는 시점으로 나눈다. 접촉 전 영상으로 결정을 끝내는 방법은 마찰과 형상 가정에 의존한다. 접촉 뒤 갱신하는 방법은 미끄러짐에 반응할 수 있지만, 실패 전에 센싱과 제어가 반응해야 유용하다. 본 비교는 계획기를 고정하고 이 시간 경계를 시험한다.”

가정과 인터페이스가 분류축이 됐다. 실제 논문과 인용은 해당 집단에 배치한다. **여기서 얻는 독법.** 각 집단이 설계할 실험을 바꾸는지 묻는다. 관련연구 문단을 지워도 주장한 gap이 그대로라면 아직 문장으로 쓴 참고문헌 목록일 수 있다.

### 4. 그림과 표

시스템 그림은 런타임 정보 흐름, 학습/동결 구성요소, 필요하면 프레임·주기, 학습/추론
차이를 보여야 한다. 결과 표에는 단위, 개선 방향, 불확실성, 시행 수, 명확한 최고값 표기가
필요하다. 캡션은 본문을 뒤지지 않고도 이해돼야 한다.

독자는 절차보다 높이와 간격을 먼저 보기 때문에 그림은 설득력이 강하다. 그래서 분모 누락이 중요하다. 작은 표본의 성공률 막대도 훨씬 많은 독립 노출로 얻은 막대처럼 정밀해 보일 수 있다.

같은 파지 결과를 먼저 막대로, 다음에는 시행 수·불확실성 구간·조건 이름과 함께 그려 보자. 막대는 순위를 보게 한다. 보강한 그림은 우위가 불확실한지, 특정 재료가 평균을 좌우하는지, 반복 시행이 같은 물체를 공유하는지 보게 한다. 데이터는 같지만 방어 가능한 결론이 드러나는 정도가 달라진다.

**여기서 얻는 독법.** 점·막대·구간 뒤의 단위를 확인한다. 캡션에는 집계, 구간 계산 방식, 제외 규칙이 있어야 한다. 일반화를 주장한다면 조건 이름이 분포 이동을 드러내야 한다. 전체 평균 속에 감추면 안 된다.

### 5. Results와 Discussion

Results는 측정된 결과를 보고한다. Discussion은 원인, 한계, 이전 가능성을 해석한다.
"방법 A의 실패가 적었다"는 result다; "촉각 피드백이 더 이른 미끄럼 회복을 가능하게 했다"
는 진단 증거를 요구하는 기전적 해석이다.

**수정 전:** “촉각 시스템은 접촉을 이해했기 때문에 실패가 적었다.” **문제:** 앞은 결과이고 뒤는 측정 대상을 밝히지 않은 기전이다. **결과로 분리:** “짝지은 절차에서 촉각 조건의 관찰 실패가 적었다.” **논의로 분리:** “더 이른 미끄러짐 감지가 후보 설명이다. 이를 시험하려면 동기화된 센싱·회복 로그가 필요하다.”

**수정 전:** “모델이 일반화했으므로 전이 가능한 물리 지식을 배웠다.” **문제:** 보지 못한 집합의 성공만으로 원인 표현을 알 수 없다. **결과로 분리:** “선언한 미관측 배치에서 과제를 완료했다.” **논의로 분리:** “해당 배치 사이의 전이를 지지한다. 다른 재료로의 전이는 시험하지 않았다.”

가상 예제지만 두 부분에 모두 증거가 생긴 뒤에도 이 구분은 유용하다. **여기서 얻는 독법.** 측정 기록에서 바로 옮길 수 있는 것과 추가 논증이 필요한 것을 구분한다. 추가 논증은 근거 분석 곁에 두고 대안 설명도 보이게 한다.

### 6. Limitations

시험하지 않은 환경, 데이터·컴퓨트 의존성, 하드웨어 가정, 개입/리셋, 실패 모드, 안전
경계, 가능성 높은 분포 이동을 명시하라. Limitations는 논문을 약하게 만드는 것이 아니라
근거 없는 일반화를 막는다.

**수정 전:** “더 어려운 조건은 향후 연구에서 다룬다.” **문제:** 관련 조건에서 실패했는지 아예 시험하지 않았는지 알 수 없다. **수정 후:** “젖은 표면은 평가에 포함하지 않았다. 현재 증거는 접촉 마찰이 바뀔 때의 전이를 확립하지 않는다.”

**수정 전:** “가끔 사람의 도움이 필요하다.” **문제:** 개입 원인과 자율성 주장에 미치는 영향이 숨는다. **수정 후:** “위치 추정이 끊기면 운전자가 로봇을 리셋한다. 해당 에피소드는 자율 시도의 실패로 남기고 보조 완료를 별도 보고한다.”

가상의 경계이므로 실제 한계 절에서는 기록된 조건으로 바꾼다. 경계가 센싱, 학습 범위, 제어, 평가 중 어디에 있는지 설명한다. 그래야 다른 곳에서 쓰려는 독자가 필요한 변경을 판단한다.

**여기서 얻는 독법.** 한계는 주장이 어디서 더 이상 성립하지 않을지 예측하게 해야 한다. 향후 연구의 약속은 기존 실패나 빠진 증거를 먼저 명시한 뒤에야 쓸모가 있다. 약속이 설명을 대신할 수는 없다.

### 7. Peer review

각 코멘트를 사실 정정, 명료화 요청, 증거 부족, 범위 이견, 선호로 분해하라. 응답 방식:

- **Agree:** 인정하고 수정한다.
- **Clarify:** 오해를 설명하고, 다른 독자가 같은 오해를 하지 않게 논문을 고친다.
- **Revise:** 분석·실험·인용·한계를 추가한다.
- **Rebut:** 증거와 범위로, 요구된 결론이 따라 나오지 않음을 정중히 보인다.

원고의 어디가 바뀌었는지 정확히 밝혀라. 새 실험이 측정한 것 이상을 증명한다고 주장하지
말라.

예를 들어 “novelty is unclear”는 서로 다른 결함을 가리킬 수 있다. 가장 가까운 선행 방법을 정확히 설명했는지, 원고가 구체적 차이를 밝혔는지, 실험이 그 차이가 중요한 이유를 보여 주는지 확인한다. 새 신경망 부품이 없어도 시스템 기여는 성립할 수 있다. 통합 노력만으로 이 질문에 답하지는 못한다.

접촉 중 상태 갱신이 차이라고 설명하고, 관련연구 분류에 빠진 비교를 넣고, 실험이 통합 시스템만 지지하면 기여 범위를 줄이는 답변이 가능하다. **여기서 얻는 독법.** 코멘트를 논증의 빠진 고리를 찾으라는 요청으로 읽는다. 신규성을 강조하는 형용사를 더해도 고리는 생기지 않는다. 확인 가능한 가정·인터페이스·평가의 차이가 필요하다.

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

각각 올바른 산출물도 서로 다른 실험을 설명할 수 있다. 표는 제어기를 바꾸기 전 체크포인트를 쓰고, 공개 설정과 시연 영상은 나중 제어기를 쓸 수 있다. 독자가 코드를 정상 실행해도 보고 결과를 재현하지 못하는 이유다.

파지 시행마다 설정, 체크포인트, 보정, 원본 로그, 분석 출력을 연결하는 식별자를 붙인다. 표의 각 항목을 포함한 시행 식별자로 연결하고 제외 규칙을 기록한다. 실패 시행도 보존한다. 다른 설정을 보여 주는 영상이면 차이를 표시하고 표의 출처인 것처럼 제시하지 않는다.

**여기서 얻는 독법.** 그림에서 분석을 거쳐 원본 시도까지 거슬러 간다. 방법 절의 소프트웨어·하드웨어 설정에서 경로가 끝나는지 본다. 재현 가능한 산출물은 그럴듯한 이름의 파일을 모은 저장소가 아니라 확인 가능한 증거 사슬이다.

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
