---
title: "MR Ch.08 — Dynamics of Open Chains"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.8** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] 시작 전 점검 · Before you start
> You need the Jacobian from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]], positive-definite matrices ([[02-foundations/linear-algebra|1. Linear Algebra §3]]), and mechanics at the level of Newton's second law.
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안, [[02-foundations/linear-algebra|PSD 행렬]], 그리고 뉴턴 제2법칙 수준의 역학이 필요하다.

## English

**Core question**: what torques produce what accelerations?

- **The equation of motion** — everything in one line:
  $$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$
  mass matrix (configuration-dependent inertia), Coriolis/centripetal terms (velocity
  products), gravity. $M(\theta)$ is symmetric positive-definite
  ([[02-foundations/linear-algebra|PSD]]) — kinetic energy $\tfrac12\dot\theta^\top M \dot\theta$
  is a genuine square.
- **Where the three terms come from, on one link**: a pendulum (mass $m$, length $l$,
  angle $\theta$ from vertical) has $\tau = \underbrace{ml^2}_{M}\,\ddot\theta +
  \underbrace{mgl\sin\theta}_{g(\theta)}$ — here $M=ml^2$ is the (constant) inertia and
  $g(\theta)=mgl\sin\theta$ is the configuration-dependent gravity torque; the Coriolis
  term $c$ is *zero* because a single link has no velocity-coupling between joints. Add a
  second link and $M$ becomes $\theta$-dependent and $c$ turns on — that is the whole jump
  from "one equation" to "why multi-link dynamics are hard.
- Two derivations, one answer: **Lagrangian** (energy-based, clean for analysis) vs
  **recursive Newton-Euler** (force-balance, $O(n)$, what simulators and controllers
  actually compute).
- **Forward dynamics** ($\tau \to \ddot\theta$): what a simulator integrates each step —
  every physics engine (Isaac, MuJoCo) is this equation plus contacts.
  **Inverse dynamics** ($\ddot\theta \to \tau$): what a controller feeds forward
  ([[04-robotics/modern-robotics/ch11-robot-control|ch.11]]).
- Task-space version: the same structure expressed at the end-effector — the bridge to
  operational-space and impedance control.

**Wiki connections**: sim-to-real gaps live in the mismatch of this equation's parameters;
[[01-canonical-papers/notes/5-world-models/dreamer|world models]] *learn* an implicit version of it;
[[04-robotics/convex-mpc-legged|convex MPC]] deliberately simplifies it (single rigid body)
to buy solvability.

## 한국어

**핵심 질문**: 어떤 토크가 어떤 가속도를 만드는가?

- **운동 방정식** — 전부가 한 줄에:
  $$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$
  질량 행렬(자세 의존 관성), 코리올리/원심 항(속도 곱), 중력. $M(\theta)$는 대칭
  양정부호([[02-foundations/linear-algebra|PSD]]) — 운동 에너지
  $\tfrac12\dot\theta^\top M \dot\theta$가 진짜 제곱량이라는 뜻.
- **세 항이 어디서 오는지, 1링크로**: 진자(질량 $m$, 길이 $l$, 연직에서의 각 $\theta$)는
  $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$ —
  여기서 $M=ml^2$가 (상수) 관성, $g(\theta)=mgl\sin\theta$가 자세 의존 중력 토크다;
  코리올리 항 $c$는 *0*인데 단일 링크는 관절 간 속도 결합이 없기 때문이다. 링크를 하나
  더 붙이면 $M$이 $\theta$ 의존이 되고 $c$가 켜진다 — 그것이 "한 방정식"에서 "다링크
  동역학이 왜 어려운가"로 가는 도약 전부다.
- 유도는 둘, 답은 하나: **라그랑주**(에너지 기반, 해석에 깔끔) vs **재귀
  뉴턴-오일러**(힘 평형, $O(n)$, 시뮬레이터·제어기가 실제로 계산하는 것).
- **순동역학** ($\tau \to \ddot\theta$): 시뮬레이터가 매 스텝 적분하는 것 — 모든 물리
  엔진(Isaac, MuJoCo)이 이 방정식 + 접촉이다.
  **역동역학** ($\ddot\theta \to \tau$): 제어기가 피드포워드로 공급하는 것
  ([[04-robotics/modern-robotics/ch11-robot-control|11장]]).
- 작업 공간 버전: 같은 구조를 말단에서 표현 — operational-space·임피던스 제어로 가는 다리.

**위키 연결**: sim-to-real 격차는 이 방정식의 파라미터 불일치에 살고,
[[01-canonical-papers/notes/5-world-models/dreamer|월드모델]]은 이것의 암시적 버전을 *학습*하며,
[[04-robotics/convex-mpc-legged|convex MPC]]는 풀림성을 사려고 이를 의도적으로
단순화(단일 강체)한다.

### Self-check · 스스로 점검

1. Explain why the mass matrix $M(\theta)$ depends on configuration, using an extended vs folded arm. · 질량 행렬 $M(\theta)$가 자세에 의존하는 이유를 팔을 뻗은/접은 상태의 관성으로 설명하라.
2. Which of forward and inverse dynamics does a simulator integrate, and which does a controller feed forward? · 순동역학과 역동역학 중 시뮬레이터가 적분하는 것은 어느 쪽이고, 제어기가 피드포워드로 쓰는 것은 어느 쪽인가?
3. Why is the Coriolis term $c(\theta,\dot\theta)$ quadratic in velocity? · 코리올리 항 $c(\theta, \dot\theta)$는 왜 속도의 이차식인가?

> [!tip]- Answers · 정답
> 1. Rotational inertia depends on how far mass sits from the axis. Extended, the distal links are far out and the same joint acceleration needs much more torque; folded, they are close and it needs less. Inertia is a function of geometry, and geometry is $\theta$. · 같은 관절 가속도라도 팔을 뻗으면 말단 질량이 축에서 멀어 회전 관성이 커진다 — 관성이 기하(자세)의 함수이기 때문.
> 2. Simulator = forward dynamics ($\tau \to \ddot\theta$), integrated each step; controller feedforward = inverse dynamics ($\ddot\theta \to \tau$). · 시뮬레이터 = 순동역학; 제어기 피드포워드 = 역동역학.
> 3. Substituting the kinetic energy $\tfrac12\dot\theta^\top M(\theta)\dot\theta$ into the Lagrange equation differentiates $M$ with respect to $\theta$, and the chain rule turns $\partial M/\partial\theta$ into products $\dot\theta_i\dot\theta_j$ — velocity times velocity. · 운동 에너지를 라그랑주 방정식에 넣으면 $M$의 $\theta$ 의존성에서 $\dot\theta_i\dot\theta_j$ 곱 항이 나오기 때문.
