---
title: 1. Research Questions & Claims
tags: [research, claims, methodology]
study-depth: Working
depth-goal: "Apply the procedure when forming claims, running experiments, analyzing failure, and writing."
mastery-when: "Mastery means consistently producing defensible work, not memorizing the page."
---

## English

A topic names an area; a research question specifies an uncertain relationship that evidence can resolve. “Apply VLA to construction” is a direction. A useful question identifies the intervention, comparator, outcome, conditions, and scope.

> [!info] Depth target
> Turn a broad interest into a falsifiable question; separate research gaps from missing implementations; and align contribution and claim strength with evidence.

> [!note] Prerequisites
> [[01-canonical-papers/how-to-read|How to Read Papers]] · [[02-foundations/ml-practice|ML Practice & Evaluation]]

### 1. Topic → problem → question

| Level | Example |
|---|---|
| Topic | VLA for construction manipulation |
| Problem | scarce demonstrations limit adaptation to new material layouts |
| Question | Under a fixed demonstration budget, does action-chunk fine-tuning of a pretrained VLA improve closed-loop success on held-out layouts over vision-only behavior cloning? |

The final question states a condition, intervention, comparator, outcome, and test distribution. It can be answered negatively.

**Before:** “We study construction manipulation.” **Problem:** an area does not identify an assumption that can fail. **After:** “Factory grasp planners often rely on an assumed friction coefficient μ; wet or dusty site surfaces can violate that assumption.” This turns a topic into a specific mismatch between a model and its operating conditions.

**Before:** “We will add touch to solve the mismatch.” **Problem:** installing a sensor is an intervention, not an answerable question. **After:** “When the assumed μ is wrong, how much does estimating friction from touch during contact recover lost grasp success, compared with the same planner using fixed μ?”

**The reading this gives you.** Follow the chain from surface condition to model error to a measurable outcome. Define how friction mismatch is established and keep the grasp planner comparable. A negative answer is informative: it could show that the available contact observations do not arrive early enough to change the grasp decision.

### 2. A gap is not merely “nobody has done this”

A defensible gap may be an unexplained failure, incompatible assumptions, missing evidence, poor generalization, unrealistic evaluation, or a theoretically/operationally important trade-off. Adding a model to a new dataset is an engineering activity unless it tests a consequential question.

A gap needs a reason why the missing evidence matters. “Nobody has attached a VLA to this excavator” could reflect an uninteresting port, unavailable hardware, or a difficult unsolved assumption. Those possibilities imply very different research projects, even though the novelty sentence sounds identical.

For example, a policy trained on visual demonstrations may not observe changing material resistance before the bucket commits to a motion. The consequential gap is whether the available observations support timely adaptation under that hidden variation. Testing a VLA on the machine becomes useful when the experiment can distinguish this information limitation from an implementation failure or a poor action interface.

**The reading this gives you.** Look for the bridge between missing work and a predicted failure mechanism. Ask what the existing method assumes, which site condition breaks it, and what observation would resolve the uncertainty. A credible gap survives even if another group has already built a superficially similar system.

### 3. Hypotheses and contributions

- **Hypothesis:** expected relationship that can be tested.
- **Engineering objective:** system capability to build.
- **Scientific contribution:** new knowledge supported by evidence.
- **System contribution:** integration or capability whose novelty may lie in architecture, deployment, or evaluation.
- **Artifact contribution:** useful code, dataset, benchmark, or platform.

A project can contribute a system without inventing a new algorithm, but must identify what knowledge or capability the system establishes beyond assembly effort.

**Before:** “Our contribution is a tactile sensor.” **Problem:** a component name does not specify what knowledge or capability was established. **After:** “We provide a contact-state estimation interface and evaluate whether its updates recover grasp performance under friction mismatch.” The artifact and its scientific question now have separate jobs.

**Before:** “We hypothesize that our system is novel and useful.” **Problem:** novelty is a relation to prior work, and usefulness has no defined outcome here. **After:** “We predict that contact-time friction updates reduce failures associated with incorrect assumed μ, under a matched grasping protocol.”

These are proposed statements, not results. The contribution sentence must eventually say what the evidence supports, including a narrower outcome if the prediction fails. **The reading this gives you.** Check whether the claimed contribution is an artifact, an observed relationship, or a capability, and whether the paper supplies the corresponding evidence.

### 4. Claim types

| Claim | Required caution |
|---|---|
| Descriptive | claims must stay within the studied sample |
| Comparative | performance relative to a defined baseline and setting |
| Causal | alternative explanations must be controlled or modeled |
| Generalization | target distribution and shift must be defined |
| Mechanistic | evidence must isolate why the method works |
| Safety/reliability | exposure, severity, rare failures, and system boundaries matter |

“Performance drops when component X is removed” supports a scoped dependency; it does not prove the author's complete causal story.

**Before:** “Touch explains the improvement because the full system scored higher.” **Problem:** a comparative result does not isolate a mechanism when training data or control logic also changed. **After:** “The complete system outperformed the baseline in the tested conditions; a matched tactile ablation is needed to attribute the difference to touch.”

**Before:** “The robot is safe because no collision occurred.” **Problem:** a sample outcome omits exposure and the role of supervision. **After:** “No collision was observed under the stated trial and intervention protocol; this supports a bounded observation about the tested system.”

These hypothetical rewrites preserve the observation while reducing the inferred claim. **The reading this gives you.** Underline the verb: describes, exceeds, causes, transfers, or prevents. Then ask whether the comparison and sampling procedure can actually support that kind of statement.

### 5. Scope and assumptions

Write the population, environment, embodiment, sensors, data regime, task, intervention policy, and evaluation horizon. Assumptions are not weaknesses by default; hidden assumptions are.

Scope makes the experiment interpretable because the same intervention can answer different questions under different conditions. A friction estimator evaluated on familiar dry objects tests adaptation within a known regime. Evaluation on held-out wet surfaces tests a different boundary, even if the task and success metric keep the same names.

For the tactile grasping question, record material preparation, how friction mismatch is induced or verified, the contact observations available before action, and what the operator may change. Also state whether grasp geometry and object identity appeared in training. A policy can exploit those cues without estimating friction, so an apparently successful test may support a narrower explanation than intended.

**The reading this gives you.** Try completing the sentence “This result applies when…”. Each missing condition is a question for the methods section. Separate an explicit simplification from an untested transfer claim; knowing the model's boundary is what lets a later study deliberately move it.

### 6. Worked rewrite

Weak: **Can world models improve construction robots?**

Stronger: **For autonomous excavation in variable soil, does a learned latent dynamics model reduce bucket-path tracking error and recovery interventions relative to model-free behavior cloning when both use the same demonstrations and MPC safety constraints?**

This still needs operational definitions for soil variation, intervention, and the world-model planning procedure.

**Before, as a proposed abstract:** “Construction robots need robust manipulation. We introduce a tactile intelligence framework for reliable grasping in challenging environments.” It names a motivation and a tool, but a reader cannot identify the assumption being tested or imagine a result that would contradict the promise.

**After, as a proposed abstract:** “Grasp planners that assume known friction may lose success when site surfaces become wet or dusty. We ask whether estimating μ from tactile observations during contact recovers this loss relative to the same planner using fixed μ. We compare the conditions under matched objects, sensing opportunities, and intervention rules, with held-out surface conditions. We report grasp success, recovery behavior, and estimation timing. The experiment tests whether the observed contact information is useful before the grasp decision; it does not establish general construction autonomy.”

This is a study proposal, so it intentionally contains no invented result. After testing, replace the reporting intention with the measured outcome and uncertainty. The strongest final sentence must follow that outcome, including a negative one.

### 7. Claim–evidence table

Before experiments, make this table:

| Intended claim | Necessary comparison | Metric | Boundary |
|---|---|---|---|
| better data efficiency | same model/evaluation at several data budgets | learning curve and uncertainty | tested tasks/layouts only |
| better recovery | matched failure perturbations | recovery success/time | specified failure types |
| safer operation | comparable exposure and hazard definitions | violations, near misses, severity | not certification |

**Before:** “Claim: robust grasping; evidence: a successful video.” **Problem:** neither variation nor the denominator is visible. **After:** “Claim: improved recovery under specified surface shifts; evidence: matched attempts, failure records, and uncertainty for each held-out condition.”

**Before:** “Claim: tactile friction estimation is the cause; evidence: full model versus the old system.” **Problem:** the systems differ along uncontrolled axes. **After:** “Claim: benefit from contact-time updates; evidence: the same planner with updates enabled or disabled, matched sensing and compute, plus diagnostics linking updates to decisions.”

Use the table before data collection to discover evidence you cannot currently obtain. **The reading this gives you.** A missing comparison is a design decision: add it, narrow the claim, or leave that question explicitly unanswered. Filling the table after writing can hide this choice behind an attractive but irrelevant metric.

> [!tip] Fill this table before the experiments · 실험 전에 표를 채워라
> The reason to fill it early is stronger than tidiness. A study is largely decided before
> the first run, by three choices this table forces: which claim is worth making, which
> single comparison is hardest for a sceptic to escape, and where the work will be judged.
> Sun Tzu's version of the principle is that battle is won before it is fought; the research
> version is that one experiment a competing explanation cannot survive is worth more than
> ten that are merely consistent with your story.
>
> The third choice is the one people skip. Choosing where to be evaluated — which dataset,
> which failure conditions, which metric — is choosing the ground you fight on, and it is
> legitimate as long as you say plainly what that ground excludes. A strong problem statement
> makes this concrete by naming a *structural* reason existing methods fail, in the form
> "existing methods assume X → deployment violates X → the failure is therefore systematic",
> rather than the weaker "existing methods score lower". The first turns your work into a
> missing layer; the second turns it into an increment. Synthesised from Giseop Kim's essay
> [이기는 연구의 설계](https://gisbi-kim.github.io/notes/winning-research-design-sun-tzu/).

### After reading

- Convert a topic into a falsifiable question.
- Explain why absence of prior implementation is not automatically a research gap.
- Distinguish hypothesis, engineering objective, and contribution.
- Match claim type to the evidence it requires.
- State scope and assumptions before using words such as robust or general.

### Self-check

1. Rewrite “Does diffusion help robot planning?” as a testable question.
2. Why can a larger benchmark score fail to establish the claimed mechanism?
3. What would falsify a data-efficiency claim?

> [!tip]- Answers
> 1. Specify task/distribution, diffusion intervention, matched comparator, data budgets, metric, and closed-loop conditions. 2. Several components or data changes may differ; score alone does not isolate cause. 3. No advantage across predeclared low-data budgets under matched compute/model/evaluation, or an advantage explained by unequal data or tuning.

### Sources

- [DARPA — the Heilmeier Catechism](https://www.darpa.mil/about/heilmeier-catechism) — the classic checklist for stating what you are trying to do, what is new, and why it matters
- [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) — how a major venue operationalizes claim–evidence alignment

## 한국어

Topic은 영역의 이름이고, research question은 증거가 해소할 수 있는 불확실한 관계를
명시한다. "건설에 VLA 적용"은 방향이다. 쓸모 있는 질문은 개입(intervention), 비교
대상(comparator), 결과(outcome), 조건, 범위를 짚는다.

> [!info] 깊이 목표
> 넓은 관심을 반증 가능한 질문으로 바꾼다; research gap과 "아직 구현이 없음"을 구분한다;
> 기여와 주장 강도를 증거에 맞춘다.

> [!note] 선수 지식
> [[01-canonical-papers/how-to-read|How to Read Papers]] · [[02-foundations/ml-practice|ML 실무와 평가]]

### 1. Topic → problem → question

| 수준 | 예 |
|---|---|
| Topic | 건설 매니퓰레이션을 위한 VLA |
| Problem | 부족한 시연이 새로운 자재 배치에의 적응을 제한한다 |
| Question | 고정된 시연 예산 아래, 사전학습 VLA의 action-chunk 파인튜닝이 held-out 배치에서 vision-only 행동 복제보다 폐루프 성공률을 높이는가? |

최종 질문은 조건, 개입, 비교 대상, 결과, 시험 분포를 명시한다. **부정적으로도 답할 수
있어야 한다.**

**수정 전:** “건설 현장 조작을 연구한다.” **문제:** 영역 이름에는 실패할 가정이 없다. **수정 후:** “공장용 파지 계획기는 가정한 마찰계수 μ에 의존하는 경우가 많다. 젖거나 먼지가 묻은 현장 표면은 그 가정을 깨뜨릴 수 있다.” 주제가 모델과 운용 조건의 구체적 불일치로 바뀐다.

**수정 전:** “촉각을 추가해 이를 해결한다.” **문제:** 센서 설치는 개입이지 답할 수 있는 질문이 아니다. **수정 후:** “가정한 μ가 틀렸을 때, 접촉 중 촉각으로 마찰을 추정하면 고정 μ를 쓰는 같은 계획기 대비 잃어버린 파지 성공률을 얼마나 회복하는가?”

**여기서 얻는 독법.** 표면 조건에서 모델 오차를 거쳐 측정 결과로 이어지는 사슬을 찾는다. 마찰 오추정을 어떻게 확인할지 정하고 파지 계획기는 비교 가능하게 유지한다. 부정적 답도 유익하다. 접촉 관측이 파지 결정을 바꾸기에 너무 늦게 들어온다는 경계를 드러낼 수 있다.

### 2. Gap은 "아무도 안 했다"가 아니다

방어 가능한 gap은 설명되지 않은 실패, 양립 불가능한 가정, 빠진 증거, 나쁜 일반화,
비현실적 평가, 이론적·운용적으로 중요한 트레이드오프일 수 있다. 새 데이터셋에 모델을
얹는 것은 중대한 질문을 시험하지 않는 한 엔지니어링 활동이다.

빠진 증거가 왜 중요한지를 설명해야 gap이 된다. “아무도 이 굴착기에 VLA를 붙이지 않았다”는 말은 단순 이식, 장비 부재, 어려운 미해결 가정 중 어느 것이든 뜻할 수 있다. 신규성 문장은 같아 보여도 각각 다른 연구가 된다.

예를 들어 시각 시연으로 학습한 정책은 버킷 동작을 시작하기 전에 달라진 재료 저항을 보지 못할 수 있다. 중요한 gap은 숨은 변동 아래에서 주어진 관측으로 제때 적응할 수 있는가다. VLA를 기계에 올리는 실험은 이 정보 한계를 구현 실패나 부적절한 행동 인터페이스와 구별할 수 있을 때 유익하다.

**여기서 얻는 독법.** 빠진 연구와 예상 실패 기전을 연결하는 고리를 찾는다. 기존 방법은 무엇을 가정하고, 현장의 어떤 조건이 이를 깨며, 어떤 관찰로 불확실성을 해소할지 묻는다. 설득력 있는 gap은 다른 집단이 비슷하게 생긴 시스템을 이미 만들었더라도 남는다.

### 3. 가설과 기여

- **가설:** 시험 가능한 기대 관계.
- **엔지니어링 목표:** 구축할 시스템 능력.
- **과학적 기여:** 증거가 지지하는 새 지식.
- **시스템 기여:** 구조·배포·평가에 신규성이 있을 수 있는 통합·능력.
- **산출물 기여:** 유용한 코드, 데이터셋, 벤치마크, 플랫폼.

새 알고리즘 없이 시스템으로 기여할 수 있다 — 단 조립 노력 너머에 그 시스템이 어떤
지식·능력을 확립하는지 밝혀야 한다.

**수정 전:** “기여는 촉각 센서다.” **문제:** 부품 이름만으로는 어떤 지식이나 능력을 확립했는지 알 수 없다. **수정 후:** “접촉 상태 추정 인터페이스를 제공하고, 그 갱신이 마찰 오추정 아래 파지 성능을 회복하는지 평가한다.” 산출물과 과학적 질문의 역할이 나뉜다.

**수정 전:** “시스템이 새롭고 유용하다고 가설을 세운다.” **문제:** 신규성은 선행연구와의 관계이고 유용성에는 결과 정의가 없다. **수정 후:** “짝지은 파지 절차에서 접촉 중 마찰 갱신이 잘못 가정한 μ와 관련된 실패를 줄일 것으로 예측한다.”

이는 결과가 아니라 제안 단계의 문장이다. 최종 기여 문장은 예측이 실패했을 때의 더 좁은 결론까지 포함해 증거가 지지하는 것을 적어야 한다. **여기서 얻는 독법.** 기여가 산출물인지, 관찰된 관계인지, 능력인지 구별하고 그에 맞는 증거가 있는지 본다.

### 4. 주장의 유형

| 주장 | 요구되는 주의 |
|---|---|
| 기술적(descriptive) | 관찰된 표본을 넘어 일반화하지 말 것 |
| 비교적 | 정의된 베이스라인·설정 대비 성능 |
| 인과적 | 대안 설명이 통제·모델링돼야 함 |
| 일반화 | 대상 분포와 이동(shift)이 정의돼야 함 |
| 기전적(mechanistic) | 방법이 *왜* 통하는지 분리하는 증거 |
| 안전/신뢰성 | 노출, 심각도, 희귀 실패, 시스템 경계가 중요 |

"구성요소 X를 빼면 성능이 떨어진다"는 범위가 한정된 의존성을 지지할 뿐,
저자의 완전한 인과 이야기를 증명하지 않는다.

**수정 전:** “전체 시스템의 점수가 높으므로 촉각이 개선의 원인이다.” **문제:** 학습 데이터나 제어 논리도 달라졌다면 비교 결과로 기전을 분리할 수 없다. **수정 후:** “시험 조건에서 전체 시스템이 베이스라인보다 좋았다. 차이를 촉각에 귀속하려면 짝지은 촉각 절제가 필요하다.”

**수정 전:** “충돌이 없었으므로 로봇은 안전하다.” **문제:** 표본 결과에 노출량과 감독 역할이 빠져 있다. **수정 후:** “명시한 시행·개입 절차에서 충돌은 관찰되지 않았다. 이는 시험한 시스템에 한정된 관찰을 지지한다.”

가상의 고쳐 쓰기는 관찰을 보존하면서 추론 범위를 줄인다. **여기서 얻는 독법.** 기술한다, 앞선다, 유발한다, 전이한다, 방지한다 중 어느 동사를 쓰는지 본다. 비교와 표집 절차가 실제로 그 종류의 문장을 지지할 수 있는지 묻는다.

### 5. 범위와 가정

모집단, 환경, embodiment, 센서, 데이터 체제, 과제, 개입 정책, 평가 지평을 적어라.
가정은 그 자체로 약점이 아니다 — **숨긴 가정**이 약점이다.

범위가 있어야 실험을 해석할 수 있다. 같은 개입도 조건에 따라 다른 질문에 답한다. 익숙한 마른 물체에서 시험한 마찰 추정기는 알려진 조건 안의 적응을 다룬다. 보지 못한 젖은 표면에서의 평가는 과제와 성공 지표 이름이 같아도 다른 경계를 시험한다.

촉각 파지 질문에서는 재료 준비, 마찰 오추정의 유도·확인 방법, 행동 전에 이용 가능한 접촉 관측, 운전자가 바꿀 수 있는 것을 기록한다. 파지 형상과 물체 정체성이 학습에 있었는지도 밝힌다. 정책은 마찰을 추정하지 않고도 이런 단서를 쓸 수 있다. 성공한 시험이 의도보다 좁은 설명만 지지할 수 있는 이유다.

**여기서 얻는 독법.** “이 결과는 …일 때 적용된다”를 완성해 본다. 빠진 조건은 방법 절에 물어볼 질문이다. 명시한 단순화와 시험하지 않은 전이 주장을 구분한다. 모델의 경계를 알아야 후속 연구가 그 경계를 의도적으로 옮길 수 있다.

### 6. 고쳐 쓰기 예제

약함: **월드모델이 건설로봇을 개선할 수 있는가?**

더 강함: **가변 토질의 자율 굴착에서, 학습된 잠재 동역학 모델이 같은 시연과 MPC 안전
제약을 쓰는 model-free 행동 복제 대비 버킷 경로 추종 오차와 회복 개입을 줄이는가?**

이것도 토질 변동, 개입, 월드모델 계획 절차의 조작적 정의가 더 필요하다.

**수정 전, 제안 단계의 초록:** “건설로봇에는 강건한 조작이 필요하다. 어려운 환경에서 신뢰성 있는 파지를 위한 촉각 지능 프레임워크를 제안한다.” 동기와 도구는 있지만 시험할 가정이 없다. 독자는 약속에 반하는 결과를 상상하기 어렵다.

**수정 후, 제안 단계의 초록:** “마찰을 안다고 가정한 파지 계획기는 현장 표면이 젖거나 먼지가 묻으면 성공률이 떨어질 수 있다. 접촉 중 촉각으로 μ를 추정하면 고정 μ를 쓰는 같은 계획기 대비 이 손실을 회복하는지 묻는다. 물체, 센싱 기회, 개입 규칙을 맞추고 보지 못한 표면 조건에서 비교한다. 파지 성공, 회복 행동, 추정 시점을 보고한다. 이 실험은 관찰한 접촉 정보가 파지 결정 전에 유용한지 시험한다. 일반적인 건설 자율성을 확립하지는 않는다.”

연구 제안이므로 결과를 지어 넣지 않는다. 시험 뒤에는 보고 계획을 측정 결과와 불확실성으로 바꾼다. 최종 결론은 부정 결과까지 포함해 실제 관찰을 따라야 한다.

### 7. 주장–증거 표

실험 전에 이 표를 만들어라:

| 의도한 주장 | 필요한 비교 | 지표 | 경계 |
|---|---|---|---|
| 더 나은 데이터 효율 | 여러 데이터 예산에서 같은 모델/평가 | 학습 곡선과 불확실성 | 시험한 과제/배치에 한정 |
| 더 나은 회복 | 짝지은 실패 교란 | 회복 성공/시간 | 명시된 실패 유형 |
| 더 안전한 운용 | 대등한 노출과 hazard 정의 | 위반, near miss, 심각도 | 인증이 아님 |

**수정 전:** “주장: 강건한 파지. 증거: 성공 영상.” **문제:** 변동 조건과 분모가 보이지 않는다. **수정 후:** “주장: 명시한 표면 이동에서 회복 개선. 증거: 보지 못한 조건별 짝지은 시도, 실패 기록, 불확실성.”

**수정 전:** “주장: 촉각 마찰 추정이 원인. 증거: 전체 모델과 구형 시스템 비교.” **문제:** 통제하지 않은 축도 달라진다. **수정 후:** “주장: 접촉 중 갱신의 이점. 증거: 같은 계획기에서 갱신을 켜고 끈 비교, 대등한 센싱·연산, 갱신이 결정으로 이어지는 진단.”

수집 전에 표를 쓰면 지금 얻을 수 없는 증거가 드러난다. **여기서 얻는 독법.** 빠진 비교는 설계상의 선택이다. 비교를 추가하거나, 주장을 줄이거나, 답하지 못한 질문으로 남긴다. 글을 쓴 뒤 표를 채우면 보기 좋지만 무관한 지표가 이 선택을 가릴 수 있다.

> [!tip] 실험 전에 표를 채워라 · Fill this table before the experiments
> 일찍 채워야 할 이유는 정돈보다 강하다. 연구는 첫 실행 이전에 대체로 결정되며, 그 결정을 이 표가
> 강제하는 세 선택이 만든다. 어떤 주장을 할 값어치가 있는가, 회의적인 독자가 가장 빠져나가기
> 어려운 비교 하나는 무엇인가, 그리고 이 연구는 어디서 평가받을 것인가. 손자의 표현으로는 싸우기
> 전에 이겨 놓는 것이고, 연구의 표현으로는 경쟁 설명이 살아남을 수 없는 실험 하나가 당신의 서사와
> 그저 모순되지 않는 실험 열 개보다 값지다는 것이다.
>
> 사람들이 건너뛰는 것은 세 번째 선택이다. 어디서 평가받을지를 고르는 것 — 어느 데이터셋, 어떤
> 실패 조건, 어떤 지표 — 은 싸울 땅을 고르는 일이고, 그 땅이 무엇을 제외하는지 분명히 밝히는 한
> 정당하다. 강한 문제 정의는 기존 방법이 실패하는 *구조적* 이유를 대면서 이것을 구체화한다.
> "기존 방법은 X를 가정한다 → 배치 조건이 X를 위반한다 → 그러므로 실패는 체계적이다"의 꼴이지,
> "기존 방법은 점수가 낮다"의 꼴이 아니다. 앞의 형태는 연구를 빠져 있던 한 계층으로 만들고, 뒤의
> 형태는 증분으로 만든다. 김기섭의 에세이
> [이기는 연구의 설계](https://gisbi-kim.github.io/notes/winning-research-design-sun-tzu/)를
> 요약·재구성한 것이다.

### 읽고 나면 말할 수 있어야 하는 것

- topic을 반증 가능한 질문으로 변환할 수 있다
- 선행 구현의 부재가 자동으로 research gap이 아닌 이유를 설명할 수 있다
- 가설·엔지니어링 목표·기여를 구분할 수 있다
- 주장 유형을 그것이 요구하는 증거와 짝지을 수 있다
- robust·general 같은 단어를 쓰기 전에 범위와 가정을 명시할 수 있다

### 스스로 점검

1. "디퓨전이 로봇 계획에 도움이 되는가?"를 시험 가능한 질문으로 다시 써라.
2. 더 큰 벤치마크 점수가 주장한 기전을 확립하지 못할 수 있는 이유는?
3. 데이터 효율 주장을 반증하는 것은 무엇인가?

> [!tip]- 정답 · Answers
> 1. 과제/분포, 디퓨전 개입, 짝지은 비교 대상, 데이터 예산, 지표, 폐루프 조건을 명시한다.
> 2. 여러 구성요소나 데이터가 함께 달라졌을 수 있다 — 점수만으로는 원인을 분리하지 못한다.
> 3. 미리 선언한 저데이터 예산들에서 대등한 컴퓨트/모델/평가 아래 이점이 없거나, 이점이 불평등한 데이터·튜닝으로 설명되는 것.

### 출처

- [DARPA — Heilmeier Catechism](https://www.darpa.mil/about/heilmeier-catechism) — 무엇을 하려는지, 무엇이 새로운지, 왜 중요한지를 묻는 고전적 체크리스트
- [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) — 주요 학회가 주장–증거 정렬을 어떻게 운영화하는지
