---
title: 0. How to Read Papers
tags: [reference]
---

## English

The notes in this wiki exist for one purpose: making the vocabulary, sentence patterns,
and equations of papers familiar enough that the originals read smoothly. This page is the
method — how deep to read each paper, how to decode paper sentences and equations, and how
to check that a note actually landed.

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
