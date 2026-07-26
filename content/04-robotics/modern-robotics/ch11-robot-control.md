---
title: "MR Ch.11 — Robot Control"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.11** — [[04-robotics/modern-robotics-book|book guide & free PDF]] · continues into [[04-robotics/lqr-lqg|LQR]] → [[04-robotics/mpc|MPC]]

> [!note] 시작 전 점검 · Before you start
> You need the equation of motion from [[04-robotics/modern-robotics/ch08-dynamics|ch.8]] and second-order error dynamics ($\zeta, \omega_n$) from [[02-foundations/engineering-math|0.5 §8]]; [[04-robotics/control-theory-ce397|5. Control Theory]] develops the same ideas in state-space form.
> [[04-robotics/modern-robotics/ch08-dynamics|8장]]의 운동 방정식과 [[02-foundations/engineering-math|0.5 §8]]의 오차 미분방정식($\zeta, \omega_n$)이 필요하다; [[04-robotics/control-theory-ce397|5. 제어 이론]]이 같은 내용을 상태공간으로 전개한다.

## English

**Core question**: how do we make the robot actually follow the trajectory?

- **Error dynamics thinking**: design the controller so the *error* obeys a stable
  differential equation ([[02-foundations/engineering-math|0.5 §8]]) — e.g.,
  $\ddot e + K_d \dot e + K_p e = 0$ with gains picking damping/frequency.
- **PID** (velocity-input regime): the workhorse; P fights error, D adds damping, I kills
  steady-state offset (and brings windup — hence anti-windup in every real implementation).
- **Computed torque / feedback linearization** — the chapter's centerpiece:
  $$\tau = M(\theta)\big(\ddot\theta_d + K_p e + K_d \dot e\big) + c(\theta,\dot\theta) + g(\theta)$$
  Use the [[04-robotics/modern-robotics/ch08-dynamics|dynamics model]] to cancel the
  nonlinearity, leaving linear error dynamics you can place at will. Model-based control's
  purest form — and its weakness: it is only as good as $M, c, g$.
- **Force & impedance control**: when contact matters, control the *relationship* between
  motion and force (virtual spring-damper) rather than position alone — the entry point to
  contact-rich manipulation.
- The modern continuation: optimal feedback ([[04-robotics/lqr-lqg|LQR]]) → constraints
  ([[04-robotics/mpc|MPC]]) → learned policies ([[02-foundations/rl-basics|RL]],
  [[01-canonical-papers/notes/4-vla/pi0|VLA]]) — each layer absorbing more of the modeling burden.

**Wiki connections**: every VLA demo secretly rides on this chapter — policy outputs are
tracked by exactly these low-level loops; impedance control is why
[[01-canonical-papers/notes/4-vla/act|ALOHA]]-class contact tasks don't destroy their hardware.

## 한국어

**핵심 질문**: 로봇이 궤적을 실제로 따르게 만드는 방법은?

- **오차 동역학 사고**: *오차*가 안정한 미분방정식([[02-foundations/engineering-math|0.5 §8]])을
  따르도록 제어기를 설계한다 — 예: $\ddot e + K_d \dot e + K_p e = 0$, 이득이 감쇠/주파수를
  고른다.
- **PID** (속도 입력 영역): 주력 일꾼; P는 오차와 싸우고, D는 감쇠를 더하고, I는 정상 상태
  오프셋을 없앤다(그리고 와인드업을 데려온다 — 모든 실전 구현에 anti-windup이 있는 이유).
- **계산 토크 / 피드백 선형화** — 이 장의 중심:
  $$\tau = M(\theta)\big(\ddot\theta_d + K_p e + K_d \dot e\big) + c(\theta,\dot\theta) + g(\theta)$$
  [[04-robotics/modern-robotics/ch08-dynamics|동역학 모델]]로 비선형성을 상쇄해, 마음대로
  배치할 수 있는 선형 오차 동역학만 남긴다. 모델 기반 제어의 가장 순수한 형태 — 그리고 그
  약점: $M, c, g$만큼만 좋다.
- **힘·임피던스 제어**: 접촉이 중요할 때는 위치만이 아니라 운동과 힘의 *관계*(가상
  스프링-댐퍼)를 제어한다 — 접촉 많은 조작으로 들어가는 입구.
- 현대적 연속: 최적 피드백([[04-robotics/lqr-lqg|LQR]]) → 제약([[04-robotics/mpc|MPC]]) →
  학습된 정책([[02-foundations/rl-basics|RL]], [[01-canonical-papers/notes/4-vla/pi0|VLA]]) —
  층마다 모델링 부담을 더 흡수한다.

**위키 연결**: 모든 VLA 데모가 몰래 이 장 위에 올라타 있다 — 정책 출력은 정확히 이 저수준
루프들이 추종한다; 임피던스 제어는 [[01-canonical-papers/notes/4-vla/act|ALOHA]]급 접촉 과제가
하드웨어를 부수지 않는 이유다.

### Self-check · 스스로 점검

1. In $\ddot e + K_d\dot e + K_p e = 0$, what relation between $K_d$ and $K_p$ gives critical damping? · 임계 감쇠가 되는 $K_d$와 $K_p$의 관계는?
2. What does "computed torque is only as good as the model" mean concretely — what is left when $M, c, g$ are wrong? · 계산 토크 제어가 "모델만큼만 좋다"는 말의 구체적 의미는?
3. Name two situations where impedance control beats position control. · 위치 제어 대신 임피던스 제어를 쓰는 대표적 상황 두 가지를 들어라.

> [!tip]- Answers · 정답
> 1. Matching $\ddot e + 2\zeta\omega_n\dot e + \omega_n^2 e = 0$ gives $\omega_n^2 = K_p$ and $2\zeta\omega_n = K_d$, so $\zeta = 1 \iff K_d = 2\sqrt{K_p}$ ([[02-foundations/engineering-math|0.5 §8]]). · $\zeta = 1 \Leftrightarrow K_d = 2\sqrt{K_p}$.
> 2. The cancellation is incomplete, so residual nonlinear terms remain inside the error dynamics — they act as a disturbance the PD gains must suppress. The error dynamics are no longer exactly linear, and both tracking performance and stability margin degrade as model error grows. · 상쇄가 불완전해 잔차 비선형 항이 남고, 모델 오차가 클수록 성능·안정 여유가 준다.
> 3. Contact tasks (polishing, insertion — where a small position error against a stiff surface produces a huge force) and human collaboration (compliance so a collision is survivable). Both are cases where the *force–motion relationship* matters more than positional accuracy. · 접촉 작업과 인간 협업 — 힘-운동 관계가 위치 정확도보다 중요한 경우.
