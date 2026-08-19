---
title: 0. How to Read Papers
tags: [reference]
study-depth: Literacy
depth-goal: "Use this map or guide to choose reading order, reading volume, and evidence checks."
mastery-when: "Working and Mastery are assigned on the individual concept or paper pages."
---

## English

The notes in this wiki exist for one purpose: making the vocabulary, sentence patterns,
and equations of papers familiar enough that the originals read smoothly. This page is the
method — how deep to read each paper, how to decode paper sentences and equations, and how
to check that a note actually landed.

This page governs **paper-reading behavior**. The separate
[[00-study-depth-guide|Study Depth Guide]] assigns Literacy / Working / Mastery targets to
foundations, concepts, robotics tools, construction topics, and individual papers.

### 1. Four reading depths — not every paper deserves the same

| Depth | What it means | Enough for |
|---|---|---|
| Recognition | the term is no longer foreign | everything else |
| **Literacy** | can restate problem, method I/O, and results in your own words | all adjacent fields — the default target of this wiki |
| Working | can follow the code, tensor shapes, and key hyperparameters | methods you use in your own experiments |
| Mastery | can critique assumptions and design variants | your thesis contribution area only |

The [[01-canonical-papers/canonical-list|canonical list]] marks a recommended engagement
level per paper: **★ read the original in full** (method and experiments), **◐ read the
note, then skim the original**, **○ the note is enough** (lineage understanding).
No one masters every field; a good researcher knows *which* depth each paper deserves.

> [!note] Same words, two axes
> This table describes how deeply to read *one paper*. The [[00-study-depth-guide|study-depth guide]] reuses Literacy/Working/Mastery for a different axis — how well you should eventually *use a topic*. ★◐○ and this table govern reading; `study-depth` governs usage; a ○-paper can live inside a Working-topic and vice versa.

### 2. The grammar of paper sentences

What common phrases imply — and what they do **not** guarantee:

| Phrase | Implies | Does not guarantee |
|---|---|---|
| "we formulate X as Y" | X is being translated into framework Y | that Y's assumptions hold for X |
| "conditioned on Z" | Z shapes the model's output distribution | when Z is provided (train only? inference? dropped for CFG?) — check per paper; or that the model uses Z well |
| "end-to-end" | trainable components are jointly optimized under one task objective | that nothing is frozen — frozen modules can sit inside the pipeline |
| "frozen" | weights fixed, no gradient | that the module is unimportant |
| "outperforms baselines" | better on the reported setup | that baselines were tuned, or the comparison is compute-matched |
| "state-of-the-art" | best on a specific benchmark at a specific time | general superiority |
| "ablation" | one factor (component, objective, data, hyperparameter) was changed to show it matters | that interactions between factors were tested |
| "zero-shot / few-shot" | no / few examples of the target task, class, or domain (inference-time demos in LLM/VLM usage; training examples in other fields) | that the task never appeared in pretraining data |
| "emergent" | absent at small scale, present at large | an agreed definition — read the evaluation closely |
| "real-world / in the wild" | outside a controlled lab setup | the operating range you care about |
| "orthogonal to" | combinable, independent improvement | that combining was actually tried |
| "we leave X to future work" | X was not done | X is easy |

### 3. How to read an equation

Ask five questions of every equation before trying to "understand" it:

1. **What is known?** (data, fixed models, hyperparameters)
2. **What is learned?** (the parameters — usually $\theta$, $\phi$)
3. **The expectation is over what?** (which distribution is being averaged)
4. **What is minimized or maximized?**
5. **Train vs. inference** — does this expression run during training, inference, or both?

Worked example — the behavior-cloning objective that appears across
[[01-canonical-papers/notes/4-vla/rt-1|VLA]] papers:

$$\mathcal{L}(\theta) = -\,E_{(o,a)\sim\mathcal{D}}\big[\log \pi_\theta(a \mid o)\big]$$

Known: the demo dataset $\mathcal{D}$. Learned: policy parameters $\theta$. Expectation:
over observation–action pairs sampled from the demos. Minimized: negative log-probability
of the expert's action — i.e., maximize the likelihood of expert actions
([[02-foundations/probability|MLE]]). Train vs. inference: this runs only in training;
at inference the policy just outputs $a \sim \pi_\theta(\cdot \mid o)$.

Notation habits worth internalizing: $\hat{x}$ = estimate of $x$; $\bar{x}$ = average or
target copy; $\theta$/$\phi$ = learnable parameters of different modules;
$\text{sg}[\cdot]$ = stop-gradient ([[02-foundations/calculus-backprop|calculus §5]]);
subscripts index time or samples, superscripts usually name a version or frame.

### 4. Claims vs. evidence — the skeptic's checklist

- **Problem**: what exactly is being solved, and is the claimed gap in prior work *demonstrated* or just asserted?
- **Method**: inputs and outputs; which parts are learned vs. frozen; what each loss term does; what happens step-by-step at inference; which assumptions are load-bearing.
- **Experiments**: how are train/test split ([[02-foundations/ml-practice|ML practice §1]])? are baselines tuned and compute-matched? does the metric actually measure the claim? what does each ablation prove? is the improvement larger than seed variance?
- **Limitations**: what did the authors admit, what did they omit, and which assumption breaks first in your setting?

### 4.5 The whole method on one paper — a worked pass

Sections 2–4 are tools; this section runs all three on a single paper, in order, so you
can see what they actually produce. The paper is [[01-canonical-papers/notes/4-vla/rt-1|RT-1]],
chosen because its claim, its equation, and its results table are all typical of this field.

**Step 1 — decode the abstract's sentences (§2).** RT-1's abstract claims, in substance,
that one Transformer trained on a large and diverse real-robot dataset performs many tasks
and generalizes to new instructions, objects, and environments. Put each clause through
§2's table *before* reading anything else:

| Clause | §2 says it implies | §2 says it does not guarantee | So ask |
|---|---|---|---|
| "large, diverse dataset" | scale | what the *unit* of diversity is | 700+ instructions — but how many objects? how many kitchens? |
| "generalizes to new instructions" | no examples of that instruction | that the *skill* or *object* was unseen | is a "new instruction" a new phrasing of a seen skill? |
| "outperforms prior methods" | better on the reported setup | tuned, compute-matched baselines | which baselines, at what parameter count? |

Three questions, no equations yet — and all three turn out to be exactly the axes the
paper's own results table is organized by. That is the normal outcome: the sentence grammar
tells you what the experiments will have to answer.

**Step 2 — read the one equation (§3).** RT-1 discretizes each of 11 action dimensions into
256 bins, so its training objective is cross-entropy over those bins:

$$\mathcal{L}(\theta) = -\,E_{(o,a)\sim\mathcal{D}}\Big[\sum_{d=1}^{11}\log \pi_\theta(a_d \mid o)\Big]$$

Run the five questions:

1. **Known**: the demonstration dataset $\mathcal{D}$ — 130k teleoperated episodes.
2. **Learned**: $\theta$, the 35M Transformer parameters.
3. **Expectation over**: observation–action pairs drawn from *the demonstrations* — not
   from states the policy itself visits.
4. **Minimized**: the negative log-probability of the expert's bin, summed over 11 dimensions.
5. **Train vs inference**: training only; at inference the policy picks a bin per dimension.

Question 3 just paid for itself. "The expectation is over the demonstrator's states" *is*
the compounding-error problem ([[02-foundations/rl-basics|7. RL Basics §6]]): the moment the
policy drifts off the demonstrated states, the loss it was trained on says nothing about
where it now is. You did not need the paper to tell you that; the equation did.

**Step 3 — claims vs evidence (§4).** Now the checklist has something to bite on:

- *Problem* — is the gap demonstrated or asserted? Demonstrated: the paper shows
  one-model-per-task baselines failing under distribution shift.
- *Method* — what is learned vs frozen? Everything is trained here; the interesting
  interface question is the 256-bin discretization, which converts control into
  classification and therefore caps action resolution.
- *Experiments* — the key numbers are **97% on seen instructions and 76% on unseen**. That
  gap is the honest content of the generalization claim, and it exists only because the
  paper reports the two splits separately ([[02-foundations/ml-practice|9. ML Practice §1]]).
  A paper reporting one blended number would have hidden it.
- *Limitations* — the authors' own: performance tracks data *diversity* more than quantity,
  which is a statement about what would be needed to extend the result, not just a caveat.

**Step 4 — the exit test (§5).** Close the note and say the five items aloud. If you can
state the seen/unseen gap and why the expectation in step 2 matters, the paper landed.

> [!tip] Do this once yourself
> Pick a paper you have already read and run these four steps on it in writing. The first
> pass takes an hour; after that it takes about ten minutes and becomes the way you read.

### 5. Before you close a note

Every note in this wiki supports the same exit test. Without looking back, say:

1. the one-line summary in your own words,
2. the inputs and outputs of the method,
3. what one key equation, diagram, or algorithmic step does,
4. one predecessor and one successor paper, and
5. one limitation.

If any of the five fails, reread that section — not the whole note.

### Connections

- Confusable-pair comparisons in the [[glossary|glossary]] · [[02-foundations/ml-practice|9. ML Practice & Evaluation]] (reading results tables) · [[01-canonical-papers/canonical-list|Canonical Paper List]]

## 한국어

이 위키의 노트들은 하나의 목적을 위해 존재한다: 논문의 어휘, 문장 패턴, 수식을 충분히
친숙하게 만들어 원문이 술술 읽히게 하는 것. 이 페이지는 그 방법론이다 — 논문마다 얼마나
깊게 읽을지, 논문 문장과 수식을 어떻게 해독할지, 노트가 실제로 흡수됐는지 어떻게
점검할지.

이 페이지는 **논문을 읽는 행동**을 다룬다. Foundations·개념·로보틱스 도구·건설 주제·
개별 논문을 어느 수준까지 사용할지는 [[00-study-depth-guide|Study Depth Guide]]와 각
페이지 상단의 `study-depth`가 안내한다.

### 1. 네 가지 읽기 깊이 — 모든 논문이 같은 깊이를 요구하지 않는다

| 깊이 | 의미 | 충분한 범위 |
|---|---|---|
| 인지 | 용어가 더 이상 낯설지 않다 | 그 외 전부 |
| **독해** | 문제·방법의 입출력·결과를 내 말로 다시 말할 수 있다 | 모든 인접 분야 — 이 위키의 기본 목표 |
| 실무 | 코드, 텐서 모양, 핵심 하이퍼파라미터를 따라갈 수 있다 | 내 실험에서 직접 쓰는 방법들 |
| 숙달 | 가정을 비판하고 변형을 설계할 수 있다 | 내 논문의 기여 영역 하나 |

[[01-canonical-papers/canonical-list|핵심 논문 리스트]]는 논문마다 권장 수준을 표시한다:
**★ 원문 정독**(방법·실험까지), **◐ 노트 후 원문 훑기**, **○ 노트로 충분**(계보 이해).
모든 분야를 숙달하는 사람은 없다 — 좋은 연구자는 *어느* 논문이 어느 깊이를 요구하는지
아는 사람이다.

> [!note] 같은 단어, 두 개의 축
> 이 표는 *논문 한 편*을 얼마나 깊게 읽을지의 축이다. [[00-study-depth-guide|깊이 가이드]]는 Literacy/Working/Mastery를 다른 축 — 주제를 결국 얼마나 잘 *사용*해야 하는가 — 에 재사용한다. ★◐○과 이 표는 읽기를, `study-depth`는 사용을 다룬다; ○ 논문이 Working 주제 안에 있을 수 있고 그 반대도 가능하다.

### 2. 논문 문장의 문법

자주 나오는 표현이 무엇을 암시하고 — 무엇을 **보장하지 않는지**:

| 표현 | 암시하는 것 | 보장하지 않는 것 |
|---|---|---|
| "we formulate X as Y" | X를 틀 Y로 번역하고 있다 | Y의 가정이 X에서 성립한다는 것 |
| "conditioned on Z" | Z가 모델의 출력 분포를 규정한다 | Z가 언제 주어지는지(학습만? 추론? CFG처럼 제거되기도?) — 논문별 확인; 모델이 Z를 잘 쓴다는 것 |
| "end-to-end" | 학습 가능한 구성요소들이 하나의 과제 목적함수로 공동 최적화된다 | 아무것도 얼리지 않았다는 것 — frozen 모듈이 파이프라인 안에 있을 수 있다 |
| "frozen" | 가중치 고정, 그래디언트 없음 | 그 모듈이 안 중요하다는 것 |
| "outperforms baselines" | 보고된 설정에서 더 좋다 | 베이스라인이 튜닝됐다는 것, 연산량이 같다는 것 |
| "state-of-the-art" | 특정 벤치마크·특정 시점의 1위 | 일반적 우월성 |
| "ablation" | 한 요인(구성요소·목적함수·데이터·하이퍼파라미터)을 바꿔 중요함을 보였다 | 요인 간 상호작용까지 검증했다는 것 |
| "zero-shot / few-shot" | 대상 과제·클래스·도메인의 예시가 없음/소수 (LLM/VLM에서는 추론 시 데모, 다른 분야에서는 학습 예시) | 사전학습 데이터에 그 과제가 없었다는 것 |
| "emergent" | 작은 규모에 없다가 큰 규모에 나타남 | 합의된 정의 — 평가 방식을 꼼꼼히 봐야 한다 |
| "real-world / in the wild" | 통제된 실험실 밖 | 당신이 신경 쓰는 운용 범위 |
| "orthogonal to" | 결합 가능한 독립적 개선 | 실제로 결합해 봤다는 것 |
| "we leave X to future work" | X를 안 했다 | X가 쉽다는 것 |

### 3. 수식 읽는 법

수식을 "이해"하려 들기 전에 다섯 가지를 물어라:

1. **무엇이 주어져 있는가?** (데이터, 고정된 모델, 하이퍼파라미터)
2. **무엇이 학습되는가?** (파라미터 — 보통 $\theta$, $\phi$)
3. **기댓값은 무엇에 대한 것인가?** (어느 분포 위에서 평균하는가)
4. **무엇을 최소화/최대화하는가?**
5. **학습 vs 추론** — 이 식은 학습 때 도는가, 추론 때 도는가, 둘 다인가?

예제 — [[01-canonical-papers/notes/4-vla/rt-1|VLA]] 논문들에 두루 등장하는
행동 복제 목적함수:

$$\mathcal{L}(\theta) = -\,E_{(o,a)\sim\mathcal{D}}\big[\log \pi_\theta(a \mid o)\big]$$

주어진 것: 시연 데이터셋 $\mathcal{D}$. 학습되는 것: 정책 파라미터 $\theta$. 기댓값:
시연에서 샘플링한 관측–행동 쌍에 대해. 최소화하는 것: 전문가 행동의 음의 로그 확률 —
즉 전문가 행동의 우도를 최대화한다([[02-foundations/probability|MLE]]). 학습 vs 추론:
이 식은 학습에서만 돌고, 추론에서는 그냥 $a \sim \pi_\theta(\cdot \mid o)$로 행동을 낸다.

몸에 익힐 표기 습관: $\hat{x}$ = $x$의 추정치; $\bar{x}$ = 평균 또는 타깃 복사본;
$\theta$/$\phi$ = 서로 다른 모듈의 학습 파라미터;
$\text{sg}[\cdot]$ = stop-gradient ([[02-foundations/calculus-backprop|미적분 §5]]);
아래 첨자는 시간·샘플 인덱스, 위 첨자는 보통 버전이나 프레임 이름.

### 4. 주장 vs 증거 — 회의주의자의 체크리스트

- **문제**: 정확히 무엇을 푸는가, 기존 연구의 공백이라는 주장은 *입증*됐는가 단언됐는가?
- **방법**: 입력과 출력; 학습되는 부분 vs 얼린 부분; 각 손실 항의 역할; 추론이 단계별로
  어떻게 진행되는가; 어떤 가정이 하중을 받치는가.
- **실험**: train/test 분할은([[02-foundations/ml-practice|ML 실무 §1]])? 베이스라인은
  튜닝·연산량 대등한가? 지표가 주장을 실제로 재는가? 각 절제 실험이 무엇을 증명하는가?
  개선폭이 시드 분산보다 큰가?
- **한계**: 저자가 인정한 것, 생략한 것, 그리고 당신의 환경에서 가장 먼저 깨질 가정은?

### 4.5 방법 전체를 한 논문에 적용해 보기 — 시범

2~4절은 도구다. 이 절은 그 셋을 논문 하나에 순서대로 실제로 돌려, 도구가 무엇을 만들어내는지
보여준다. 대상은 [[01-canonical-papers/notes/4-vla/rt-1|RT-1]] — 주장도, 수식도, 결과 표도
이 분야의 전형이라서 골랐다.

**1단계 — 초록의 문장을 해독한다 (§2).** RT-1의 초록은 요지상, 크고 다양한 실기계 데이터로
학습한 Transformer 하나가 많은 과제를 수행하고 새로운 지시·물체·환경으로 일반화한다고
주장한다. *다른 것을 읽기 전에* 각 절을 2절의 표에 통과시켜 보자:

| 절 | 2절이 말하는 함의 | 2절이 말하는 비보장 | 그래서 물어야 할 것 |
|---|---|---|---|
| "크고 다양한 데이터" | 규모 | 다양성의 *단위*가 무엇인지 | 지시 700개 — 그런데 물체는 몇 개? 주방은 몇 개? |
| "새로운 지시로 일반화" | 그 지시의 예시가 없었음 | *스킬*이나 *물체*가 처음이라는 것 | "새 지시"가 본 적 있는 스킬의 새 표현은 아닌가? |
| "기존 방법을 능가" | 보고된 설정에서 더 낫다 | 베이스라인이 튜닝·연산량 정합되었다는 것 | 어떤 베이스라인을, 파라미터 몇 개로? |

수식은 아직 하나도 안 봤는데 질문이 셋 나왔고, 셋 다 결국 논문 자신의 결과 표가 조직된 축과
정확히 일치한다. 이것이 정상적인 결과다: 문장의 문법이 실험이 무엇에 답해야 하는지를 알려준다.

**2단계 — 수식 하나를 읽는다 (§3).** RT-1은 11개 행동 차원을 각각 256구간으로 이산화하므로,
학습 목적함수는 그 구간들에 대한 교차 엔트로피다:

$$\mathcal{L}(\theta) = -\,E_{(o,a)\sim\mathcal{D}}\Big[\sum_{d=1}^{11}\log \pi_\theta(a_d \mid o)\Big]$$

다섯 질문을 돌린다:

1. **아는 것**: 시연 데이터셋 $\mathcal{D}$ — 원격조작 에피소드 13만 개.
2. **배우는 것**: $\theta$, 3,500만 개의 Transformer 파라미터.
3. **기댓값의 대상**: *시연*에서 뽑은 관측–행동 쌍 — 정책 자신이 방문하는 상태가 아니다.
4. **최소화하는 것**: 전문가가 고른 구간의 음의 로그 확률을 11개 차원에 대해 합한 것.
5. **학습 vs 추론**: 학습에서만; 추론에서는 차원마다 구간을 하나 고른다.

3번 질문이 방금 값을 했다. "기댓값이 시연자의 상태 위에서 잡힌다"는 것이 곧 복합 오차
문제다([[02-foundations/rl-basics|7. RL 기초 §6]]): 정책이 시연된 상태에서 벗어나는 순간,
학습에 쓴 손실은 지금 있는 곳에 대해 아무 말도 해주지 않는다. 논문이 알려줄 필요가 없었다.
수식이 알려줬다.

**3단계 — 주장 vs 증거 (§4).** 이제 체크리스트가 물 곳이 생겼다:

- *문제* — 격차가 입증되었나 단정되었나? 입증됐다. 과제별 단일 모델 베이스라인이 분포
  이동에서 무너지는 것을 보여준다.
- *방법* — 무엇이 학습되고 무엇이 얼어 있나? 여기서는 전부 학습된다. 흥미로운 인터페이스
  질문은 256구간 이산화이고, 그것이 제어를 분류로 바꾸는 동시에 행동 해상도의 상한을 정한다.
- *실험* — 핵심 숫자는 **본 지시 97%, 못 본 지시 76%** 두 개다. 그 격차가 일반화 주장의 정직한
  내용이고, 논문이 두 분할을 따로 보고했기 때문에만 존재한다([[02-foundations/ml-practice|9. ML 실무 §1]]).
  하나로 섞은 숫자를 보고했다면 가려졌을 것이다.
- *한계* — 저자들 자신의 말: 성능이 데이터 양보다 *다양성*을 따라간다. 이것은 단순한 단서가
  아니라 이 결과를 확장하려면 무엇이 필요한지에 대한 진술이다.

**4단계 — 종료 시험 (§5).** 노트를 덮고 다섯 항목을 소리 내어 말해 보라. seen/unseen 격차와
2단계 기댓값이 왜 중요한지를 말할 수 있으면 그 논문은 안착한 것이다.

> [!tip] 직접 한 번 해 보라
> 이미 읽은 논문 하나를 골라 이 네 단계를 글로 써서 돌려 보라. 첫 번째는 한 시간쯤 걸리고,
> 그 뒤로는 10분이면 되며, 그때부터는 그것이 당신이 논문을 읽는 방식이 된다.

### 5. 노트를 닫기 전에

이 위키의 모든 노트는 같은 퇴장 시험을 지원한다. 노트를 다시 보지 않고 말해 보라:

1. 한 줄 요약을 내 말로,
2. 방법의 입력과 출력,
3. 핵심 식·도식·절차 중 하나가 하는 일,
4. 이전 논문 하나와 이후 논문 하나,
5. 한계 하나.

다섯 중 하나라도 막히면 그 섹션만 다시 읽어라 — 노트 전체가 아니라.

### 연결

- [[glossary|용어집]]의 혼동 쌍 비교 · [[02-foundations/ml-practice|9. ML 실무와 평가]] (결과 표 읽기) · [[01-canonical-papers/canonical-list|핵심 논문 리스트]]
