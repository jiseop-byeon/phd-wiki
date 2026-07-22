---
title: "MR Ch.8 — Dynamics of Open Chains"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.8** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

## English

**Core question**: what torques produce what accelerations?

- **The equation of motion** — everything in one line:
  $$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$
  mass matrix (configuration-dependent inertia), Coriolis/centripetal terms (velocity
  products), gravity. $M(\theta)$ is symmetric positive-definite
  ([[02-foundations/linear-algebra|PSD]]) — kinetic energy $\tfrac12\dot\theta^\top M \dot\theta$
  is a genuine square.
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
