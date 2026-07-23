---
title: "MR Ch.09 — Trajectory Generation"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.9** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] 시작 전 점검 · Before you start
> 다항식 미분([[02-foundations/engineering-math|0.5 §1]])과 경로/시간의 분리라는 아이디어만 있으면 된다 — 이 장은 트랙에서 가장 가벼운 장이다.

## English

**Core question**: how do we turn "go from A to B" into a smooth, executable function of time?

- **Path vs trajectory**: a path is geometry $\theta(s), s\in[0,1]$; a trajectory adds
  **time scaling** $s(t)$ — MR's clean separation that lets you design shape and timing
  independently.
- **Point-to-point time scalings**: cubic ($s = 3t^2/T^2 - 2t^3/T^3$: zero endpoint
  velocities) and quintic (zero endpoint accelerations too — smoother torques);
  **trapezoidal** velocity profiles (accelerate–cruise–decelerate) — what industrial
  controllers actually run.
- **Via points**: interpolate through waypoints with splines — watch for overshoot between
  close points.
- **Time-optimal time scaling**: given actuator limits and the
  [[04-robotics/modern-robotics/ch08-dynamics|dynamics]], find the fastest $s(t)$ along a
  fixed path — an [[02-foundations/optimization|optimization]] problem with a classic
  bang-bang structure.
- Smoothness matters physically: discontinuous acceleration = torque spikes = vibration
  ([[02-foundations/signal-processing|signal processing]]'s frequency lens applies).

**Wiki connections**: [[01-canonical-papers/notes/4-vla/act|action chunks]] and
[[01-canonical-papers/notes/4-vla/diffusion-policy|denoised trajectories]] are *learned*
replacements for exactly this chapter; classical time scaling still wraps learned outputs
on real hardware for safety/limits.

## 한국어

**핵심 질문**: "A에서 B로 가라"를 매끄럽고 실행 가능한 시간 함수로 어떻게 바꾸는가?

- **경로 vs 궤적**: 경로는 기하 $\theta(s), s\in[0,1]$; 궤적은 **시간 스케일링** $s(t)$를
  더한 것 — 모양과 타이밍을 독립적으로 설계하게 해주는 MR의 깔끔한 분리.
- **점대점 시간 스케일링**: 3차($s = 3t^2/T^2 - 2t^3/T^3$: 양 끝 속도 0)와 5차(양 끝
  가속도까지 0 — 토크가 더 매끄럽다); **사다리꼴** 속도 프로파일(가속–순항–감속) — 산업
  제어기가 실제로 도는 방식.
- **경유점**: 스플라인으로 웨이포인트들을 통과 — 가까운 점 사이의 오버슈트를 조심.
- **시간 최적 스케일링**: 액추에이터 한계와
  [[04-robotics/modern-robotics/ch08-dynamics|동역학]]이 주어졌을 때 고정 경로 위에서 가장
  빠른 $s(t)$ 찾기 — 고전적 뱅뱅 구조를 갖는 [[02-foundations/optimization|최적화]] 문제.
- 매끄러움은 물리적으로 중요하다: 불연속 가속도 = 토크 스파이크 = 진동
  ([[02-foundations/signal-processing|신호처리]]의 주파수 렌즈가 적용된다).

**위키 연결**: [[01-canonical-papers/notes/4-vla/act|행동 청크]]와
[[01-canonical-papers/notes/4-vla/diffusion-policy|노이즈 제거된 궤적]]은 정확히 이 장의 *학습된*
대체물이고, 실제 하드웨어에서는 안전/한계를 위해 고전적 시간 스케일링이 학습 출력을 여전히
감싼다.

### 스스로 점검 · Self-check

1. 3차 시간 스케일링 $s(t) = 3t^2/T^2 - 2t^3/T^3$에서 $s(0), s(T), \dot s(0), \dot s(T)$를 계산해 경계 조건을 확인하라.
2. 5차 스케일링이 3차보다 나은 점은 무엇이고, 그 대가는?
3. 사다리꼴 속도 프로파일이 산업 제어기의 기본값인 실용적 이유는?

> [!tip]- 정답 · Answers
> 1. $s(0)=0, s(T)=1$; $\dot s = 6t/T^2 - 6t^2/T^3$이므로 $\dot s(0)=\dot s(T)=0$ — 양 끝 정지.
> 2. 양 끝 가속도까지 0이라 토크가 매끄럽다; 대가는 같은 시간 내 최대 *속도*가 더 커짐(1.875/T vs 1.5/T — 최대 가속도는 오히려 큐빅보다 작다).
> 3. 최대 속도·가속도 한계를 직접 파라미터로 가져서 액추에이터 스펙과 1:1로 대응되기 때문.
