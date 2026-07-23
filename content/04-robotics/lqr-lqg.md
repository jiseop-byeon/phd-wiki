---
title: "6. LQR / LQG"
tags: [robotics, control, resource]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Study links** — [Underactuated Robotics, LQR chapter (Tedrake, MIT)](https://underactuated.csail.mit.edu/lqr.html) · [Stanford EE363 lecture notes (Boyd)](https://web.stanford.edu/class/ee363/)

## English

> [!info] Depth target · 깊이 목표
> State the LQR problem, the role of the Riccati equation, and LQG's estimator–controller separation. Deriving or implementing Riccati solvers is optional.
> LQR 문제와 리카티 방정식의 역할, LQG의 추정기–제어기 분리를 말할 수 있으면 된다. 리카티 해법의 유도·구현은 선택이다.

**What it is**: the **Linear Quadratic Regulator** is the exactly-solvable heart of optimal
control. For linear dynamics $\dot x = Ax + Bu$ and quadratic cost
$\int (x^\top Q x + u^\top R u)\,dt$, the optimal controller is a constant linear feedback
$u = -Kx$, with $K$ obtained from the **Riccati equation** — no iteration at runtime.
**LQG** adds Gaussian noise and partial observation: the optimal solution is a
[[02-foundations/probability|Kalman filter]] feeding an LQR (the **separation principle**:
estimate optimally, then control the estimate optimally, and it is jointly optimal).

**Why study it**: LQR is the reference point everything else is measured against —
[[04-robotics/mpc|MPC]] is "LQR + constraints, re-solved online"; RL policy evaluation on
linear-Gaussian problems recovers LQR; and the Riccati equation is where
[[02-foundations/linear-algebra|eigenvalues]] earn their keep in control.

**Suggested path**: EE363 notes 1–4 (LQR derivation via dynamic programming) →
Underactuated ch. (geometric intuition, code) → connect to the
[[02-foundations/optimization|MPC-as-QP example]].

### Continue beyond this guide

The estimator side of LQG is developed in [[04-robotics/state-estimation-slam|State Estimation, Localization & SLAM]].

## 한국어

**무엇인가**: **LQR**은 최적 제어에서 정확히 풀리는 심장부다. 선형 동역학
$\dot x = Ax + Bu$와 이차 비용 $\int (x^\top Q x + u^\top R u)\,dt$에 대해 최적 제어기는
상수 선형 피드백 $u = -Kx$이고, $K$는 **리카티 방정식**에서 나온다 — 실행 시 반복 계산이
없다. **LQG**는 가우시안 노이즈와 부분 관측을 더한 것: 최적해는
[[02-foundations/probability|칼만 필터]]가 LQR에 추정값을 공급하는 구조다
(**분리 원리**: 최적으로 추정하고, 그 추정값을 최적으로 제어하면, 그 결합이 전체 최적이다).

**왜 공부하나**: LQR은 다른 모든 것을 재는 기준점이다 — [[04-robotics/mpc|MPC]]는 "제약을
더해 온라인으로 다시 푸는 LQR"이고, 선형-가우시안 문제의 RL 정책 평가는 LQR을 복원하며,
리카티 방정식은 [[02-foundations/linear-algebra|고유값]]이 제어에서 제 몫을 하는 현장이다.

**권장 경로**: EE363 노트 1~4 (동적 계획법으로 LQR 유도) → Underactuated 해당 장(기하적
직관, 코드) → [[02-foundations/optimization|MPC-QP 예제]]로 연결.

### 연결

- 기초: [[02-foundations/linear-algebra|선형대수]] (리카티, 고유값), [[02-foundations/probability|확률]] (칼만), [[02-foundations/optimization|최적화]]
- 다음: [[04-robotics/mpc|MPC]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] LQR 문제 설정(선형 동역학 + 이차 비용)과 해의 형태($u = -Kx$)를 말할 수 있다
- [ ] $Q$와 $R$의 비율이 제어기 성격을 어떻게 바꾸는지 말할 수 있다
- [ ] 분리 원리 — 최적 추정(칼만) + 최적 제어(LQR)의 결합이 전체 최적 — 를 말할 수 있다
- [ ] LQR이 MPC·RL의 기준점으로 쓰이는 이유를 말할 수 있다
