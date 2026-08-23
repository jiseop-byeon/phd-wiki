---
title: "BADGR — An Autonomous Self-Supervised Learning-Based Navigation System"
authors: Gregory Kahn, Pieter Abbeel, Sergey Levine
affiliation: UC Berkeley
venue: IEEE RA-L
year: 2021
journal-ref: "IEEE Robotics and Automation Letters 6(2), 1312–1319, 2021"
arxiv: https://arxiv.org/abs/2002.05700
project: https://sites.google.com/view/badgr
tags: [paper, navigation, traversability, self-supervised]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if self-supervised traversability labelling becomes part of the thesis contribution."
---

**Kahn, Abbeel & Levine, RA-L 2021** — [arXiv:2002.05700](https://arxiv.org/abs/2002.05700) · [Project](https://sites.google.com/view/badgr)

> [!note] Math on-ramp · 수학 준비물
> Only the idea of a *learned* predictive model over future events, plus sampling-based action selection ([[04-robotics/planning-decision-making|4. §5–§6]]). The traversability vocabulary it depends on is [[04-robotics/traversability-off-road|17. §1–§2]].
> 미래 사건에 대한 *학습된* 예측 모델과 표본 기반 행동 선택([[04-robotics/planning-decision-making|4. §5–§6]])만 있으면 된다. 전제되는 traversability 어휘는 [[04-robotics/traversability-off-road|17. §1~§2]].

## English

**One-line summary**: A mobile robot drives itself around, records what actually happened when it took each action, and learns to predict navigational *events* — collision, bumpiness, position — instead of geometry, so tall grass stops looking like a wall.

### Context

The classical navigation stack treats the world as geometry: build an occupancy map from depth, plan a collision-free path. This is exactly the failure mode [[04-robotics/traversability-off-road|17. §1]] names — the geometric reading of a field of tall grass is "untraversable", and the robot never reaches its goal even though driving through the grass is trivially fine.

### Method

> [!tip] Key intuition
> Do not label the terrain. Label the **consequence**. Drive, record whether the bumper fired and how much the IMU shook, and let those become the supervision signal — no human annotation, no simulator.

The system is trained on **self-supervised off-policy data gathered in the real world**, with no simulation and no human supervision. The learned model predicts future navigational events conditioned on a candidate action sequence; the planner then picks the sequence whose predicted events are best under a user-specified preference. That preference channel is what lets the same model express "prefer pavement" or "grass is fine".

### Results

The abstract's claims are capability claims: it navigates real urban and off-road environments containing *geometrically distracting obstacles*, incorporates terrain preferences, generalises to novel environments, and keeps improving by collecting more data.

> [!warning] Reading the claims · 주장 읽는 법
> **The abstract contains no numbers** — no success rates, no dataset hours, no baseline margins. Every BADGR figure in circulation comes from the body or the project page. It is also worth naming what "self-supervised" means here: the labels are free, but the *data* costs real driving time on real hardware, and the robot must survive collecting it.
> **초록에 숫자가 하나도 없다** — 성공률도, 데이터 시간도, 베이스라인 대비 폭도 없다. 떠도는 BADGR 수치는 전부 본문이나 프로젝트 페이지에서 온 것이다. "self-supervised"의 의미도 짚어야 한다: 레이블은 공짜지만 *데이터*는 실제 하드웨어의 실제 주행 시간이고, 로봇이 그것을 수집하면서 살아남아야 한다.

### Limitations & critique

- **Learning by colliding.** The collision label exists because the robot collided. That is acceptable on a research rover in a field, and unacceptable on a construction site next to people or finished work.
- **The event vocabulary is the ceiling.** The model predicts the events you instrumented. Anything not sensed — sinking into mud, tipping risk, damaging what you drove over — is invisible to it.
- **Off-policy data drifts.** As the policy improves, the distribution of what it experiences changes, and old data describes a robot that no longer exists.
- Single platform, single scale. Nothing in the paper says the learned affordances transfer to a heavier or differently-actuated vehicle.

### Impact & follow-ups

BADGR is the clean statement of the reframing that [[04-robotics/traversability-off-road|17]] is built around: traversability is a *learned affordance of a specific robot*, not a property of the terrain. [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]] answers the "learning by colliding" objection by taking the supervision from a human demonstration instead of a bumper hit.

**For construction**: the preference channel is the transferable idea. A site has surfaces a robot *can* cross but *must not* — fresh screed, membrane, laid rebar. That is a preference, not a geometric obstacle, and geometry-only stacks have no way to express it.

### Connections

- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — the concept page this paper anchors
- [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]] — the same problem with demonstration instead of collision as the label source
- [[02-foundations/rl-basics|RL Basics §6]] — why interactive data collection beats a fixed offline set

### After reading

- [ ] State what BADGR predicts, and why predicting that instead of geometry solves the tall-grass failure.
- [ ] Name where the training labels come from and what they cost.
- [ ] Say what the preference channel buys you that a cost map does not.
- [ ] Say where a BADGR success rate you want to quote actually comes from.

## 한국어

**한 줄 요약**: 이동 로봇이 스스로 돌아다니며 각 행동에서 실제로 무슨 일이 일어났는지를 기록하고, 기하 대신 주행 *사건*(충돌, 흔들림, 위치)을 예측하도록 학습한다. 그러면 키 큰 풀이 더 이상 벽으로 보이지 않는다.

### 배경

고전적 내비게이션 스택은 세계를 기하로 다룬다: 깊이로 점유 격자를 만들고 충돌 없는 경로를 계획한다. 이것이 정확히 [[04-robotics/traversability-off-road|17. §1]]이 지목하는 실패 양상이다 — 키 큰 풀밭의 기하학적 독해는 "통과 불가"이고, 풀밭을 그냥 지나가면 아무 문제가 없는데도 로봇은 목표에 닿지 못한다.

### 방법

> [!tip] 핵심 직관
> 지형에 레이블을 붙이지 마라. **결과**에 붙여라. 주행하고, 범퍼가 눌렸는지와 IMU가 얼마나 흔들렸는지를 기록하고, 그것을 지도 신호로 삼아라 — 사람 주석도, 시뮬레이터도 없다.

시스템은 **실제 환경에서 모은 자기지도 off-policy 데이터**로 학습하며, 시뮬레이션도 사람 감독도 쓰지 않는다. 학습된 모델은 후보 행동열에 조건부로 미래 주행 사건을 예측하고, 계획기는 사용자가 지정한 선호 아래 예측 사건이 가장 좋은 행동열을 고른다. 그 선호 채널이 같은 모델로 "포장면 선호"와 "풀밭은 괜찮음"을 모두 표현하게 해준다.

### 결과

초록의 주장은 능력 주장이다: *기하학적으로 헷갈리게 하는 장애물*이 있는 실제 도시·오프로드 환경을 주행하고, 지형 선호를 반영하며, 새로운 환경으로 일반화하고, 데이터를 더 모아 계속 개선된다.

> [!warning] 주장 읽는 법 · Reading the claim
> **초록에 숫자가 하나도 없다** — 성공률도, 데이터 시간도, 베이스라인 대비 폭도 없다. 떠도는 BADGR 수치는 전부 본문이나 프로젝트 페이지에서 온 것이다. "자기지도"의 의미도 짚어야 한다: 레이블은 공짜지만 *데이터*는 실제 하드웨어의 실제 주행 시간이고, 로봇이 그것을 모으며 살아남아야 한다.
> The abstract contains no numbers at all; every BADGR figure in circulation comes from the body or the project page.

### 한계와 비판

- **부딪히며 배운다.** 충돌 레이블은 로봇이 충돌했기 때문에 존재한다. 들판의 연구용 로버에서는 받아들일 만하지만, 사람과 완성된 시공물 옆의 건설 현장에서는 아니다.
- **사건 어휘가 곧 천장이다.** 모델은 당신이 계측한 사건만 예측한다. 감지되지 않는 것 — 진흙에 빠짐, 전복 위험, 밟고 지나간 것의 손상 — 은 모델에게 보이지 않는다.
- **off-policy 데이터는 표류한다.** 정책이 좋아질수록 경험 분포가 바뀌고, 옛 데이터는 더 이상 존재하지 않는 로봇을 기술한다.
- 플랫폼 하나, 규모 하나. 학습된 어포던스가 더 무겁거나 구동 방식이 다른 차량으로 옮겨간다는 말은 논문에 없다.

### 영향과 후속 연구

BADGR은 [[04-robotics/traversability-off-road|17]]이 딛고 선 재프레이밍의 깔끔한 진술이다: traversability는 지형의 성질이 아니라 *특정 로봇의 학습된 어포던스*다. [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]]은 범퍼 충돌 대신 사람의 시연에서 지도 신호를 얻어 "부딪히며 배운다"는 반론에 답한다.

**건설의 경우**: 옮겨갈 만한 발상은 선호 채널이다. 현장에는 로봇이 지나갈 *수는* 있지만 지나가면 *안 되는* 표면이 있다 — 갓 친 방바닥, 방수 시트, 배근해 놓은 철근. 그것은 기하학적 장애물이 아니라 선호이고, 기하만 쓰는 스택에는 그것을 표현할 방법이 없다.

### 연결

- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율주행]] — 이 논문이 정박하는 개념 페이지
- [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]] — 충돌 대신 시연을 레이블 원천으로 삼은 같은 문제
- [[02-foundations/rl-basics|RL 기초 §6]] — 상호작용적 데이터 수집이 고정된 오프라인 집합을 이기는 이유

### 읽고 나면 말할 수 있어야 하는 것

- [ ] BADGR이 무엇을 예측하며, 기하 대신 그것을 예측하는 것이 왜 키 큰 풀 실패를 푸는지 말한다.
- [ ] 학습 레이블이 어디서 오고 무엇을 대가로 치르는지 댄다.
- [ ] 선호 채널이 비용 지도가 주지 못하는 무엇을 주는지 말한다.
- [ ] 인용하려는 BADGR 성공률이 실제로 어디서 왔는지 말한다.
