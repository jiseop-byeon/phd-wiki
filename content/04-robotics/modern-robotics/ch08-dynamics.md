---
title: "MR Ch.08 — Dynamics of Open Chains"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.8** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the Jacobian from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]], positive-definite matrices ([[02-foundations/linear-algebra|1. Linear Algebra §3]]), and mechanics at the level of Newton's second law.
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안, [[02-foundations/linear-algebra|PSD 행렬]], 그리고 뉴턴 제2법칙 수준의 역학이 필요하다.

## English

**Core question**: what torques produce what accelerations?

- **The equation of motion** — everything in one line:
  $$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$
  mass matrix (configuration-dependent inertia), Coriolis/centripetal terms (velocity
  products), gravity. $M(\theta)$ is symmetric positive-definite
  ([[02-foundations/linear-algebra|PSD]]) — kinetic energy $\tfrac12\dot\theta^\top M \dot\theta$
  behaves like $x^2$: $\dot\theta^\top M\dot\theta > 0$ for every nonzero joint velocity, matching
  the fact that a moving arm's kinetic energy can never be negative.
- **Where the three terms come from, on one link**: a pendulum has only two of them.
  With mass $m$, length $l$ and angle $\theta$ from vertical,
  $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$.
  - $M=ml^2$ is the inertia, and it is constant.
  - $g(\theta)=mgl\sin\theta$ is the gravity torque, and it depends on configuration.
  - The Coriolis term $c$ is *zero* because $M$ does not depend on $\theta$. (A one-joint
    system with configuration-dependent inertia would still have $c = \tfrac12 M'(\theta)\dot\theta^2$.)

  Add a second link and $M$ becomes $\theta$-dependent and $c$ turns on — that is the whole
  jump from "one equation" to "why multi-link dynamics are hard."

> [!example] Worked example · 계산 예제
> **Two links: $M$ changes with the elbow.** Take the planar 2R arm with point masses at the link ends, $m_1=m_2=1$ kg, $L_1=L_2=1$ m (full derivation in [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] §3–§5). Then
> $$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$
> - $\theta_2 = 0°$ (straight out): $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$.
> - $\theta_2 = 90°$ (elbow square): $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$.
>
> **What it means physically.** $M_{11}$ drops from 5 to 3 kg·m² because the forearm mass moves closer to the shoulder axis: the same shoulder acceleration needs 40% less torque. The off-diagonal term (2, then 1) is coupling — accelerating one joint pushes on the other. The pendulum had neither effect.
>
> **Gravity at one pose.** With $g = 9.81$ m/s² in the vertical plane, at $\theta = (0°, 90°)$ the forearm points straight up. Both masses sit 1 m horizontally from the shoulder, so $g_1 = 2 \times 9.81 \times 1 = 19.62$ N·m. The forearm mass is directly above the elbow, so $g_2 = 0$.
- Two derivations, one answer: **Lagrangian** (energy-based, clean for analysis) vs
  **recursive Newton-Euler** (force-balance, $O(n)$, what simulators and controllers
  actually compute).
- **Forward dynamics** ($\tau \to \ddot\theta$): what a simulator integrates each step —
  every physics engine (Isaac, MuJoCo) is this equation plus contacts.
  **Inverse dynamics** ($\ddot\theta \to \tau$): what a controller feeds forward
  ([[04-robotics/modern-robotics/ch11-robot-control|ch.11]]).
- Task-space version: the same structure expressed at the end-effector — the bridge to
  operational-space control ([[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §6]]) and
  impedance control ([[04-robotics/force-compliance-control|Force & Compliance Control §2]]).

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
  $\tfrac12\dot\theta^\top M \dot\theta$가 $x^2$처럼 행동한다는 뜻이다: 0이 아닌 모든 관절 속도에서
  $\dot\theta^\top M\dot\theta > 0$이고, 움직이는 팔의 운동 에너지가 음수일 수 없다는 사실과 맞아떨어진다.
- **세 항이 어디서 오는지, 1링크로**: 진자에는 세 항 중 두 개만 있다.
  질량 $m$, 길이 $l$, 연직에서의 각 $\theta$이면
  $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$이다.
  - $M=ml^2$는 관성이고, 상수다.
  - $g(\theta)=mgl\sin\theta$는 중력 토크이고, 자세에 의존한다.
  - 코리올리 항 $c$는 *0*이다. $M$이 $\theta$에 의존하지 않기 때문이다. (관성이 자세에
    의존하는 1관절 계라면 $c = \tfrac12 M'(\theta)\dot\theta^2$가 남는다.)

  링크를 하나 더 붙이면 $M$이 $\theta$ 의존이 되고 $c$가 켜진다 — 그것이 "한 방정식"에서
  "다링크 동역학이 왜 어려운가"로 가는 도약 전부다.

> [!example] 계산 예제 · Worked example
> **2링크: 팔꿈치에 따라 $M$이 바뀐다.** 링크 끝에 점질량이 있는 평면 2R 팔, $m_1=m_2=1$ kg, $L_1=L_2=1$ m를 잡자(전체 유도는 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학]] §3–§5). 그러면
> $$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$
> - $\theta_2 = 0°$ (쭉 뻗음): $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$.
> - $\theta_2 = 90°$ (팔꿈치 직각): $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$.
>
> **물리적 의미.** 전완 질량이 어깨 축에 가까워지므로 $M_{11}$이 5에서 3 kg·m²로 줄어든다: 같은 어깨 가속도에 토크가 40% 덜 든다. 비대각 항(2, 그다음 1)은 결합이다 — 한 관절을 가속하면 다른 관절이 밀린다. 진자에는 둘 다 없었다.
>
> **한 자세의 중력.** 연직 평면에서 $g = 9.81$ m/s²로 두고 $\theta = (0°, 90°)$이면 전완이 똑바로 위를 향한다. 두 질량 모두 어깨에서 수평으로 1 m 떨어져 있으므로 $g_1 = 2 \times 9.81 \times 1 = 19.62$ N·m. 전완 질량은 팔꿈치 바로 위에 있으므로 $g_2 = 0$.
- 유도는 둘, 답은 하나: **라그랑주**(에너지 기반, 해석에 깔끔) vs **재귀
  뉴턴-오일러**(힘 평형, $O(n)$, 시뮬레이터·제어기가 실제로 계산하는 것).
- **순동역학** ($\tau \to \ddot\theta$): 시뮬레이터가 매 스텝 적분하는 것 — 모든 물리
  엔진(Isaac, MuJoCo)이 이 방정식 + 접촉이다.
  **역동역학** ($\ddot\theta \to \tau$): 제어기가 피드포워드로 공급하는 것
  ([[04-robotics/modern-robotics/ch11-robot-control|11장]]).
- 작업 공간 버전: 같은 구조를 말단에서 표현 — operational-space 제어([[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §6]])와
  임피던스 제어([[04-robotics/force-compliance-control|힘·컴플라이언스 제어 §2]])로 가는 다리.

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
