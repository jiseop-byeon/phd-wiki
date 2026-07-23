---
title: Do As I Can, Not As I Say — SayCan
authors: Michael Ahn et al.
venue: CoRL
year: 2022
pdf: https://arxiv.org/abs/2204.01691
tags: [paper, robotics, language, planning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Ahn et al., CoRL 2022** — [arXiv](https://arxiv.org/abs/2204.01691) · [PDF](https://arxiv.org/pdf/2204.01691)

## English

**One-line summary**: SayCan multiplies a language model's preference over high-level skills ("does this advance the instruction?") by a learned affordance/value estimate ("can the robot do it here and now?"), producing grounded skill sequences without making the LM a low-level controller.

### Context

By 2022, LLMs could decompose "I spilled my drink, can you help?" into sensible steps — but their plans floated free of any body: they would happily propose actions the robot cannot perform, on objects it cannot see, in states it is not in. Conversely, robot skill libraries could execute short behaviors reliably but had no idea which ones served a natural-language goal. SayCan's question: how do you let the LM plan while the robot's own experience vetoes what is infeasible?

### Method

> [!tip] Key intuition
> The LM knows what is *useful*; the robot's value functions know what is *possible*. Score every candidate skill by both and multiply — a product-of-experts where either side can veto a step.

- **Say**: score each skill's text description by the LM's likelihood of it as a continuation of the instruction (plus prompt-engineered few-shot context) — a preference over skills, not free-form generation.
- **Can**: each skill (pick, place, go-to; trained via behavior cloning or RL) carries a value function; its value at the current state is the affordance — the probability the skill succeeds from here.
- Select $\arg\max$ of (language score × affordance score), execute the skill, append it to the LM context, and repeat until the LM emits a termination step.
- Normalization and implementation details matter; this is a product-of-experts *intuition*, not a universal formula.

### Results

- Evaluated on 101 real-world instructions in a kitchen/office setting with a mobile manipulator over a library of pretrained skills — roughly 84% correct planning and 74% end-to-end execution.
- Affordance grounding is the differentiator: language-only ranking picks infeasible steps that affordances filter out, and planning quality scales with the underlying LM (the PaLM-SayCan upgrade improved both metrics).
- Handles long-horizon, temporally extended instructions ("bring the apple, then throw away the bag") by chaining scored skill selections.

### Limitations & critique

- The ceiling is the skill library: SayCan can only sequence what was pretrained, and adding a capability means training a new skill plus its value function.
- Open loop with respect to language: the LM does not see execution outcomes, so mid-plan failures go unnoticed (the direct motivation for Inner Monologue's feedback loop).
- The LM never perceives the scene — grounding is entirely delegated to value functions, whose calibration bounds the whole system.

### Impact & follow-ups

The canonical "LLM as planner over robot skills" architecture, and the bridge between language planning and robot learning before end-to-end VLA models. [[01-canonical-papers/notes/4-vla/rt-2|RT-2]] and [[01-canonical-papers/notes/4-vla/pi0|π0]] dissolve the boundary SayCan carefully maintains: perception, language, and action generation move into one learned model instead of a scored library. Reading SayCan first makes clear what VLA models absorbed and what they gave up (explicit feasibility estimates, modular skill upgrades).

> [!warning] Reading the claim
> Grounded language planning does not mean the LM learned new motor skills. Success is bounded by the skill library, the affordance estimator, perception, and the recovery executive — check which component failed before crediting or blaming the LM.

### Connections

- Next: [[01-canonical-papers/notes/4-vla/rt-2|RT-2]] (perception and action move into the model) · [[01-canonical-papers/notes/4-vla/pi0|π0]] (end-to-end generalist VLA)
- Construction parallel: [[01-canonical-papers/notes/8-construction/park-nl|Park NL instructions]] (natural-language tasking on site)

## 한국어

**한 줄 요약**: SayCan은 고수준 skill에 대한 언어모델의 선호("이게 지시를 진전시키는가?")와 학습된 affordance/value 추정("로봇이 지금 여기서 할 수 있는가?")을 곱해, 언어모델을 저수준 제어기로 만들지 않고도 접지된 skill 순서를 만든다.

### 배경

2022년쯤 LLM은 "음료를 쏟았는데 도와줄래?"를 그럴듯한 단계로 분해할 수 있었다 — 하지만 그 계획은 어떤 몸체와도 무관하게 떠 있었다: 로봇이 수행할 수 없는 행동을, 보이지 않는 물체에 대해, 지금 상태와 무관하게 태연히 제안했다. 반대로 로봇 skill library는 짧은 행동을 안정적으로 실행할 수 있었지만 어떤 skill이 자연어 목표에 복무하는지 알지 못했다. SayCan의 질문: LM이 계획하게 하되, 로봇 자신의 경험이 불가능한 것에 거부권을 행사하게 하려면?

### 방법

> [!tip] 핵심 직관
> LM은 무엇이 *유용한지* 알고, 로봇의 가치 함수는 무엇이 *가능한지* 안다. 모든 후보 skill을 양쪽으로 점수 매겨 곱하라 — 어느 쪽이든 한 단계를 거부할 수 있는 product-of-experts.

- **Say**: 각 skill의 텍스트 설명이 지시문의 연속으로 나올 LM 우도로 점수화(few-shot 프롬프트 문맥 포함) — 자유 생성이 아니라 skill들에 대한 선호다.
- **Can**: 각 skill(집기, 놓기, 이동; behavior cloning 또는 RL로 학습)은 가치 함수를 갖는다; 현재 상태에서의 그 값이 affordance — 여기서 그 skill이 성공할 확률이다.
- (언어 점수 × affordance 점수)의 $\arg\max$를 골라 실행하고, 실행한 skill을 LM 문맥에 덧붙인 뒤, LM이 종료 단계를 낼 때까지 반복한다.
- 정규화와 구현 세부가 중요하다; 이것은 product-of-experts *직관*이지 보편 공식이 아니다.

### 결과

- 주방/사무실 환경에서 모바일 매니퓰레이터와 사전학습 skill library로 실세계 지시 101개를 평가 — 계획 정확도 약 84%, 끝까지 실행 약 74%.
- 차별점은 affordance 접지다: 언어 점수만으로 순위를 매기면 불가능한 단계를 고르고, affordance가 이를 걸러낸다; 계획 품질은 기반 LM 규모에 따라 오른다(PaLM-SayCan 업그레이드가 두 지표 모두 개선).
- 점수화된 skill 선택을 연쇄해 장기·시간 확장 지시("사과 갖다주고, 그 다음 봉지를 버려")를 처리한다.

### 한계와 비판

- 천장은 skill library다: SayCan은 사전학습된 것만 배열할 수 있고, 능력 하나를 추가하려면 새 skill과 그 가치 함수를 학습해야 한다.
- 언어에 대해 open loop다: LM이 실행 결과를 보지 못하므로 계획 중간의 실패를 알아차리지 못한다(Inner Monologue의 피드백 루프가 나온 직접적 동기).
- LM은 장면을 전혀 지각하지 않는다 — 접지는 전적으로 가치 함수에 위임되고, 그 보정 품질이 시스템 전체의 상한이다.

### 영향과 후속 연구

"로봇 skill 위의 planner로서의 LLM"이라는 정전적 아키텍처이자, end-to-end VLA 이전에 언어 계획과 로봇 학습을 잇는 다리. [[01-canonical-papers/notes/4-vla/rt-2|RT-2]]와 [[01-canonical-papers/notes/4-vla/pi0|π0]]는 SayCan이 조심스럽게 유지한 경계를 녹인다: 지각·언어·행동 생성이 점수화된 library 대신 하나의 학습된 모델로 들어간다. SayCan을 먼저 읽으면 VLA가 무엇을 흡수했고 무엇을 포기했는지(명시적 실행가능성 추정, 모듈식 skill 업그레이드)가 선명해진다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 접지된 언어 계획이 LM이 새 운동 기술을 배웠다는 뜻은 아니다. 성공은 skill library, affordance 추정기, 지각, 회복 executive에 의해 제한된다 — LM을 칭찬하거나 탓하기 전에 어느 구성요소가 실패했는지 확인하라.

### 연결

- 다음: [[01-canonical-papers/notes/4-vla/rt-2|RT-2]] (지각과 행동이 모델 안으로) · [[01-canonical-papers/notes/4-vla/pi0|π0]] (end-to-end 범용 VLA)
- 건설 병렬: [[01-canonical-papers/notes/8-construction/park-nl|Park NL instructions]] (현장의 자연어 작업 지시)

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 언어 점수와 affordance 점수의 역할을 구분하고, 곱이 왜 product-of-experts인지 설명할 수 있다
- [ ] skill-library planner와 end-to-end VLA의 차이, 그리고 각각 무엇을 얻고 잃는지 말할 수 있다
- [ ] SayCan의 성공이 새 운동 기술 학습을 뜻하지 않는 이유와, 실패를 어느 구성요소에 귀속해야 하는지 설명할 수 있다
