---
title: "RMA — Rapid Motor Adaptation for Legged Robots"
authors: Ashish Kumar, Zipeng Fu, Deepak Pathak, Jitendra Malik
affiliation: UC Berkeley, Carnegie Mellon University
venue: RSS
year: 2021
arxiv: https://arxiv.org/abs/2107.04034
project: https://ashish-kmr.github.io/rma-legged-robots/
tags: [paper, locomotion, legged, adaptation, sim-to-real]
status: note-complete
last_verified: 2026-08-22
study-depth: Literacy
wiki-support: Working
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if online adaptation to changing dynamics becomes part of the experimental design."
---

**Kumar, Fu, Pathak & Malik, RSS 2021** — [arXiv:2107.04034](https://arxiv.org/abs/2107.04034) · [Project](https://ashish-kmr.github.io/rma-legged-robots/)

> [!note] Math on-ramp · 수학 준비물
> The teacher–student idea from [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]], read as *system identification* rather than perception: the adaptation module estimates a latent that stands in for the environment's dynamics ([[04-robotics/legged-locomotion|18. §2]]).
> [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]의 teacher–student 발상을, 인지가 아니라 *시스템 식별*로 읽으면 된다: 적응 모듈이 환경 동역학을 대신하는 잠재 변수를 추정한다([[04-robotics/legged-locomotion|18. §2]]).

## English

**One-line summary**: Split the controller into a base policy and a small **adaptation module** that infers the environment's latent properties from recent proprioceptive history, so the robot re-tunes itself to a new terrain or payload in **fractions of a second**.

### Context

[[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] made the student infer terrain from proprioception. RMA asks a slightly different question: not *what is under me* but *what are the dynamics right now* — changing terrains, changing payloads, wear and tear. Those are things a single fixed policy cannot absorb, because they change what the same action does.

### Method

Two components. A **base policy** conditioned on a latent describing the environment's dynamics, and an **adaptation module** that estimates that latent online from the recent stream of proprioceptive signals. The two together let the robot adapt to novel situations in fractions of a second.

Notably, RMA is trained **entirely in simulation without any domain knowledge** — no reference trajectories, no predefined foot-trajectory generators — and is deployed on the A1 robot **without any fine-tuning**. The training uses a varied terrain generator with bioenergetics-inspired rewards.

### Results

Deployment across rocky, slippery and deformable surfaces, in environments with grass, long vegetation, concrete, pebbles, stairs, and sand. The abstract's summary claim is **state-of-the-art performance across diverse real-world and simulation experiments**.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> "State-of-the-art performance" appears in the abstract **with no accompanying number, baseline, or metric**. The concrete claims are the terrain list, the *fractions of a second* adaptation time, and the absence of fine-tuning. Cite those; treat the SOTA phrase as unquantified.
> "state-of-the-art performance"가 초록에 **어떤 숫자도, 베이스라인도, 지표도 없이** 등장한다. 구체적인 주장은 지형 목록, *1초의 몇 분의 일*이라는 적응 시간, 그리고 미세조정이 없다는 사실이다. 그것들을 인용하고, SOTA라는 표현은 정량화되지 않은 것으로 다뤄라.

### Limitations & critique

- **Adaptation is not perception.** RMA infers dynamics after the fact — it reacts to the terrain it is already standing on. It cannot plan ahead the way [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al.]] can, because it has no exteroception at all.
- **The latent is only as rich as the simulator's variation.** Whatever axis of dynamics the terrain generator did not vary is an axis the adaptation module has never learned to estimate.
- **A1-scale, A1-specific.** Nothing here establishes the recipe at construction-machine mass, where actuator saturation and inertia dominate differently.

### Impact & follow-ups

RMA established online latent system identification as a peer of privileged distillation rather than a competitor, and the "base policy plus small fast adapter" split is now common well outside legged control. It is also one of the cleanest demonstrations that pure-simulation training with no fine-tuning can transfer — which is the claim [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] treats most sceptically.

### Connections

- [[04-robotics/legged-locomotion|18. Legged Locomotion]] — the concept page
- [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] — distillation instead of online estimation
- [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] — why unknown dynamics parameters are the sim-to-real gap

### After reading

- [ ] Say what the adaptation module estimates, and from what input.
- [ ] Explain why adaptation cannot substitute for exteroception.
- [ ] Name the part of the training setup that bounds what can be adapted to.
- [ ] State which of RMA's claims are quantified and which are not.

## 한국어

**한 줄 요약**: 제어기를 기본 정책과 작은 **적응 모듈**로 쪼갠다. 적응 모듈이 최근 고유수용 이력에서 환경의 잠재 속성을 추정하므로, 로봇이 새 지형이나 새 하중에 **1초의 몇 분의 일** 만에 스스로를 다시 맞춘다.

### 배경

[[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]은 학생이 고유수용 감각에서 지형을 추론하게 했다. RMA는 조금 다른 질문을 한다: *내 밑에 무엇이 있는가*가 아니라 *지금 동역학이 어떤가* — 바뀌는 지형, 바뀌는 하중, 마모. 이것들은 고정된 정책 하나가 흡수할 수 없는데, 같은 행동이 하는 일 자체를 바꿔놓기 때문이다.

### 방법

구성 요소는 둘이다. 환경 동역학을 기술하는 잠재 변수에 조건부인 **기본 정책**, 그리고 최근 고유수용 신호 흐름에서 그 잠재를 온라인으로 추정하는 **적응 모듈**. 둘이 합쳐져 로봇이 새로운 상황에 1초의 몇 분의 일 만에 적응한다.

특기할 점은 RMA가 **어떤 영역 지식도 없이 전부 시뮬레이션에서** 학습된다는 것이다 — 참조 궤적도, 미리 정의한 발 궤적 생성기도 없다 — 그리고 **미세조정 없이** A1 로봇에 배포된다. 학습에는 다양한 지형 생성기와 생체에너지학에서 착안한 보상을 쓴다.

### 결과

바위·미끄러운 면·변형 지반, 그리고 풀·긴 식생·콘크리트·자갈·계단·모래가 있는 환경에서의 배포. 초록의 요약 주장은 **다양한 실제 및 시뮬레이션 실험에서 state-of-the-art 성능**이다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "state-of-the-art performance"가 초록에 **어떤 숫자도, 베이스라인도, 지표도 없이** 등장한다. 구체적인 주장은 지형 목록, *1초의 몇 분의 일*이라는 적응 시간, 그리고 미세조정이 없다는 사실이다. 그것들을 인용하고, SOTA라는 표현은 정량화되지 않은 것으로 다뤄라.
> The SOTA phrase in the abstract carries no number, baseline, or metric.

### 한계와 비판

- **적응은 인지가 아니다.** RMA는 사후에 동역학을 추론한다 — 이미 올라선 지형에 반응하는 것이다. 외수용 감각이 아예 없으므로 [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등]]처럼 앞을 내다볼 수 없다.
- **잠재는 시뮬레이터가 준 변이만큼만 풍부하다.** 지형 생성기가 변화시키지 않은 동역학 축은, 적응 모듈이 추정하는 법을 배운 적 없는 축이다.
- **A1 규모, A1 특정.** 구동기 포화와 관성이 다르게 지배하는 건설 기계 질량에서 이 레시피가 성립한다는 근거는 여기에 없다.

### 영향과 후속 연구

RMA는 온라인 잠재 시스템 식별을 특권 증류의 경쟁자가 아니라 동급의 선택지로 자리잡게 했고, "기본 정책 + 작고 빠른 적응기" 분할은 이제 레그드 제어 바깥에서도 흔하다. 또한 미세조정 없는 순수 시뮬레이션 학습이 전이될 수 있음을 가장 깔끔하게 보인 사례이기도 한데, 그것이 [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]]이 가장 회의적으로 다루는 주장이다.

### 연결

- [[04-robotics/legged-locomotion|18. 레그드 로코모션]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]] — 온라인 추정 대신 증류
- [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학]] — 미지의 동역학 파라미터가 곧 sim-to-real 격차인 이유

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 적응 모듈이 무엇을 어떤 입력으로부터 추정하는지 말한다.
- [ ] 적응이 왜 외수용 감각을 대신할 수 없는지 설명한다.
- [ ] 적응 가능한 범위를 한정하는 학습 설정의 부분을 댄다.
- [ ] RMA의 주장 중 정량화된 것과 아닌 것을 가른다.
