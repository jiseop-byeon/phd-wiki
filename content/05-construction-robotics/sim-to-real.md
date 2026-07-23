---
title: Sim-to-Real for Field Robots
tags: [construction, sim-to-real, robotics, learning]
study-depth: Working
depth-goal: "Use the task taxonomy, system assumptions, and evaluation criteria to formulate construction-robotics research."
mastery-when: "Raise to Mastery when this task stream or deployment layer is the thesis contribution."
---

## English

Simulation makes dangerous, slow, and expensive robot experience cheap. It does not make
that experience real. **Sim-to-real** is the set of modeling, training, adaptation, and
evaluation practices used to keep a policy useful when its simulator assumptions fail.

> [!note] Prerequisites
> [[02-foundations/probability|Probability]] · [[02-foundations/rl-basics|RL Basics]] ·
> [[04-robotics/robot-systems-deployment|Robot Systems]] ·
> [[04-robotics/contact-force-tactile|Contact]]

### 1. Where the reality gap comes from

| Gap | Examples in field robots | Typical response |
|---|---|---|
| Dynamics | mass, friction, hydraulic delay, backlash | system identification, parameter randomization, residual models |
| Contact/material | soil, rubble, tire slip, cutting resistance | randomized terrain, learned contact models, online adaptation |
| Sensing | dust, glare, vibration, latency, missing returns | sensor noise/latency models, augmentation, robust estimation |
| Task distribution | unseen sites, geometry, weather, operators | diverse procedural scenes, curriculum, real-data fine-tuning |
| Software/hardware | control rate, saturation, dropped messages | hardware-in-the-loop, action delay and limit randomization |

The important question is not “Was simulation photorealistic?” but **which variables
that affect the policy were represented, varied, or adapted**.

### 2. Main strategies

- **System identification** fits simulator parameters to measured trajectories. It makes
  one simulator more faithful but can overfit one machine and one operating condition.
- **Domain randomization** trains across a distribution of dynamics, sensing, and scene
  parameters. Success depends on whether the real system lies inside a useful training
  distribution; “more random” is not automatically better.
- **Teacher–student / privileged learning** lets a teacher observe simulator-only state
  (terrain parameters, perfect pose) and distills behavior into a student using deployable
  observations. Always check what information exists at test time.
- **Residual learning** keeps a model-based controller and learns a correction. This can
  reduce the search space, but safety still depends on how the residual is bounded.
- **Real-data adaptation** fine-tunes representations, dynamics, or policies using a
  small real dataset. Report how much real machine time and human intervention it costs.
- **Parallel simulation** creates experience quickly; it improves sample throughput, not
  simulator validity. Thousands of environments can repeat the same wrong physics.

### 3. A deployment ladder

1. Simulator-only evaluation with held-out parameters.
2. Hardware-in-the-loop and timing/saturation tests.
3. Slow, supervised real trials inside a safety envelope.
4. Adaptation without changing the evaluation cases.
5. Repeated operation across materials, machines, sites, and days.

Zero-shot transfer means no target-domain training update before deployment; it does not
mean no real-system knowledge was used to build or tune the simulator.

### 4. Reading the evidence

> [!warning] Reading the claim
> “Successful sim-to-real transfer” proves transfer only for the reported machine,
> operating range, and intervention protocol. Find the randomized variables, real-data
> budget, safety controller, failed trials, and whether evaluation conditions were used
> while tuning. A video is evidence of possibility, not a transfer distribution.

Useful measures include real/sim performance ratio, interventions per hour, constraint
violations, performance across parameter shifts, adaptation data/time, and degradation
outside the training range.

### After reading

- Separate dynamics, contact, sensing, task, and implementation gaps.
- Explain system identification, domain randomization, privileged learning, residuals,
  and real-data adaptation without treating them as interchangeable.
- Identify simulator-only information and the real-data budget in a paper.
- State what evidence would support generalization beyond one machine and one soil bin.

### Sources

- [Tobin et al., *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World*](https://arxiv.org/abs/1703.06907)
- [Peng et al., *Sim-to-Real Transfer of Robotic Control with Dynamics Randomization*](https://arxiv.org/abs/1710.06537)
- [Lee et al., *Learning Quadrupedal Locomotion over Challenging Terrain*](https://www.science.org/doi/10.1126/scirobotics.abc5986) — privileged learning example

## 한국어

시뮬레이션은 위험하고 느리며 비싼 로봇 경험을 싸게 만든다. 그 경험을 현실로 만들어 주지는
않는다. **Sim-to-real**은 시뮬레이터의 가정이 깨져도 정책이 쓸모 있도록 만드는 모델링·학습·
적응·평가 방법의 묶음이다.

> [!note] 선수지식
> [[02-foundations/probability|확률]] · [[02-foundations/rl-basics|RL 기초]] ·
> [[04-robotics/robot-systems-deployment|로봇 시스템]] · [[04-robotics/contact-force-tactile|접촉]]

### 1. Reality gap은 어디서 생기나

| 격차 | 필드 로봇의 예 | 대표 대응 |
|---|---|---|
| 동역학 | 질량·마찰·유압 지연·백래시 | 시스템 식별, 파라미터 랜덤화, 잔차 모델 |
| 접촉·재료 | 흙·잔해·타이어 슬립·절삭 저항 | 지형 랜덤화, 학습 접촉 모델, 온라인 적응 |
| 센싱 | 먼지·눈부심·진동·지연·LiDAR 누락 | 노이즈/지연 모델, 증강, 강건 추정 |
| 과제 분포 | 새로운 현장·형상·날씨·작업자 | 절차적 장면, 커리큘럼, 실제 데이터 파인튜닝 |
| 구현 | 제어 주기·포화·메시지 손실 | hardware-in-the-loop, 지연·한계 랜덤화 |

핵심 질문은 “그래픽이 사실적인가?”가 아니라 **정책에 영향을 주는 변수를 무엇까지 표현·
변동·적응했는가**다.

### 2. 주요 전략

- **시스템 식별**은 측정 궤적에 시뮬레이터 파라미터를 맞춘다. 한 조건에는 정확해지지만 한
  기계에 과적합할 수 있다.
- **도메인 랜덤화**는 동역학·센싱·장면 파라미터의 분포에서 학습한다. 현실이 유용한 학습
  분포 안에 있어야 하며, 무조건 더 많이 흔든다고 좋아지지 않는다.
- **교사–학생/privileged learning**은 교사가 완벽한 자세나 지반 파라미터 같은 시뮬레이터
  전용 상태를 보고, 배치 가능한 관측만 쓰는 학생에게 행동을 증류한다. 시험 때 가능한
  정보를 반드시 확인하라.
- **잔차 학습**은 모델 기반 제어기를 유지하고 보정량만 학습한다. 탐색 공간을 줄이지만 잔차
  한계와 안전 보장은 별개다.
- **실데이터 적응**은 소량의 실제 데이터로 표현·동역학·정책을 조정한다. 실제 장비 시간과
  인간 개입 비용을 보고해야 한다.
- **병렬 시뮬레이션**은 경험 생산량을 늘릴 뿐 물리의 타당성을 보장하지 않는다.

### 3. 배치 사다리

1. 보지 않은 파라미터에서 시뮬레이터 평가
2. hardware-in-the-loop와 지연·포화 시험
3. 안전 영역 안의 저속·감독 실제 시험
4. 평가 사례를 보며 튜닝하지 않는 적응
5. 재료·기계·현장·날짜를 바꾼 반복 운용

Zero-shot transfer는 배치 전에 목표 도메인 학습 업데이트가 없다는 뜻이지, 시뮬레이터를
만드는 데 실제 시스템 지식을 전혀 쓰지 않았다는 뜻이 아니다.

### 4. 증거 읽기

> [!warning] 주장 읽기
> “성공적인 sim-to-real”은 보고된 기계·운용 범위·개입 규약에서만 전이를 증명한다. 랜덤화한
> 변수, 실데이터 예산, 안전 제어기, 실패 시행, 평가 조건을 튜닝에 썼는지 확인하라. 영상은
> 가능성의 증거이지 전이 분포의 증거가 아니다.

유용한 측정값은 현실/시뮬 성능 비율, 시간당 개입, 제약 위반, 파라미터 변화별 성능, 적응
데이터·시간, 학습 범위 밖의 성능 저하다.

### 읽고 나면 말할 수 있어야 하는 것

- 동역학·접촉·센싱·과제·구현 격차를 구분한다.
- 시스템 식별, 도메인 랜덤화, privileged learning, 잔차, 실데이터 적응을 구별한다.
- 논문의 시뮬레이터 전용 정보와 실데이터 예산을 찾는다.
- 한 기계·한 토조를 넘어선 일반화를 지지할 증거를 말한다.

### 출처

- [Tobin et al., Domain Randomization](https://arxiv.org/abs/1703.06907)
- [Peng et al., Dynamics Randomization](https://arxiv.org/abs/1710.06537)
- [Lee et al., challenging-terrain locomotion](https://www.science.org/doi/10.1126/scirobotics.abc5986)
