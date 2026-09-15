---
title: "MR Ch.11 — Robot Control"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.11** — [[04-robotics/modern-robotics-book|book guide & free PDF]] · continues into [[04-robotics/lqr-lqg|LQR]] → [[04-robotics/mpc|MPC]]

> [!note] Prerequisites · 선수 지식
> You need the equation of motion from [[04-robotics/modern-robotics/ch08-dynamics|ch.8]] and second-order error dynamics ($\zeta, \omega_n$) from [[02-foundations/engineering-math|0.5 §8]]; [[04-robotics/control-theory-ce397|5. Control Theory]] develops the same ideas in state-space form.
> [[04-robotics/modern-robotics/ch08-dynamics|8장]]의 운동 방정식과 [[02-foundations/engineering-math|0.5 §8]]의 오차 미분방정식($\zeta, \omega_n$)이 필요하다; [[04-robotics/control-theory-ce397|5. 제어 이론]]이 같은 내용을 상태공간으로 전개한다.

## English

**Core question**: how do we make the robot actually follow the trajectory?

- **Error dynamics thinking**: design the controller so the *error* obeys a stable
  differential equation ([[02-foundations/engineering-math|0.5 §8]]) — e.g.,
  $\ddot e + K_d \dot e + K_p e = 0$ with gains picking damping/frequency.
- **Velocity-input regime (MR §11.3): P and PI swap the roles you expect.**
  - **P alone** gives *first-order* error dynamics, $\dot\theta_e + K_p\theta_e = c$. Here $c$
    is zero for a setpoint and nonzero for a constant-velocity target; that nonzero $c$ is the
    steady-state offset.
  - **Adding I** removes the offset. Differentiating once shows the cost:
    $\ddot\theta_e + K_p\dot\theta_e + K_i\theta_e = 0$. **PI in this same section is second
    order**, with $\omega_n=\sqrt{K_i}$ and $\zeta = K_p/(2\sqrt{K_i})$.
  - **Read the roles off those two expressions**: under velocity inputs $K_p$ is the *damping*
    and $K_i$ is the stiffness.
  - **Warning**: I also brings windup — hence anti-windup wherever the actuator can saturate.
- **Torque-input regime (MR §11.4): $K_p$ is the spring, $K_d$ the damper.**
  - With unit inertia, PD gives $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$, so
    $\omega_n=\sqrt{K_p}$ and $\zeta = K_d/(2\sqrt{K_p})$ — the opposite of the velocity-input
    roles. The same symbol does a different job in each regime, which is why gains do not
    transfer between them.
  - PID goes one order further still: its setpoint error dynamics are *third* order.
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

> [!example] Worked example · 계산 예제
> Torque-input PD with unit inertia: $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$, pick $K_p = 100$.
> - $\omega_n = \sqrt{K_p} = 10$ rad/s.
> - Critical damping: $K_d = 2\sqrt{K_p} = 20$, so $\zeta = 1$.
> - 2% settling time $\approx 4/(\zeta\omega_n) = 4/10 = 0.4$ s (MR §11.3 gives settling $\approx 4t$ with time constant $t = 1/(\zeta\omega_n)$).
> - Now halve the damper, $K_d = 10$: $\zeta = 10/(2\cdot 10) = 0.5$.
> - Overshoot $= e^{-\pi\zeta/\sqrt{1-\zeta^2}} \approx 16\%$ (MR lists 16% for $\zeta = 0.5$), and settling $\approx 4/(0.5\cdot 10) = 0.8$ s.
> - Halving $K_d$ bought no speed: $\zeta\omega_n$ halved, so settling doubled and the error now overshoots.

**Wiki connections**: VLA outputs ultimately pass through platform-specific position,
velocity, torque, or impedance interfaces and their low-level loops. Contact safety depends
on that whole stack — actuators, limits, passive compliance, speed, task setup, and control —
not on impedance control alone.

## 한국어

**핵심 질문**: 로봇이 궤적을 실제로 따르게 만드는 방법은?

- **오차 동역학 사고**: *오차*가 안정한 미분방정식([[02-foundations/engineering-math|0.5 §8]])을
  따르도록 제어기를 설계한다 — 예: $\ddot e + K_d \dot e + K_p e = 0$, 이득이 감쇠/주파수를
  고른다.
- **속도 입력 영역(MR §11.3): P와 PI에서는 이득의 역할이 예상과 뒤바뀐다.**
  - **P만** 쓰면 오차 동역학이 *1차*다($\dot\theta_e + K_p\theta_e = c$). $c$는 설정점
    추종이면 0이고 등속 목표면 0이 아니다. 그 0이 아닌 $c$가 곧 정상 상태 오프셋이다.
  - **I를 더하면** 오프셋이 사라진다. 한 번 미분해 보면 대가가 보인다:
    $\ddot\theta_e + K_p\dot\theta_e + K_i\theta_e = 0$. **같은 절의 PI가 이미 2차다.**
    $\omega_n=\sqrt{K_i}$, $\zeta = K_p/(2\sqrt{K_i})$다.
  - **이 두 식에서 역할을 그대로 읽어라**: 속도 입력에서는 $K_p$가 *감쇠*이고 $K_i$가 강성이다.
  - **주의**: I는 와인드업도 데려온다 — 액추에이터가 포화할 수 있는 곳이면 anti-windup이
    필요한 이유다.
- **토크 입력 영역(MR §11.4): $K_p$가 스프링, $K_d$가 댐퍼다.**
  - 단위 관성에서 PD는 $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$이므로
    $\omega_n=\sqrt{K_p}$, $\zeta = K_d/(2\sqrt{K_p})$다 — 속도 입력의 역할과 정반대다. 같은
    기호가 영역마다 다른 일을 하므로 이득은 두 영역 사이에서 옮겨 쓸 수 없다.
  - PID는 한 차수 더 간다. 설정점 오차 동역학이 *3차*다.
- **계산 토크 / 피드백 선형화** — 이 장의 중심:
  $$\tau = M(\theta)\big(\ddot\theta_d + K_p e + K_d \dot e\big) + c(\theta,\dot\theta) + g(\theta)$$
  [[04-robotics/modern-robotics/ch08-dynamics|동역학 모델]]로 비선형성을 상쇄해, 마음대로
  배치할 수 있는 선형 오차 동역학만 남긴다. 모델 기반 제어의 가장 순수한 형태 — 그리고 그
  약점: $M, c, g$만큼만 좋다.
- **힘·임피던스 제어**: 접촉이 중요할 때는 위치만이 아니라 운동과 힘의 *관계*(가상
  스프링-댐퍼)를 제어한다 — 접촉이 많은 조작으로 들어가는 입구.
- 현대적 연속: 최적 피드백([[04-robotics/lqr-lqg|LQR]]) → 제약([[04-robotics/mpc|MPC]]) →
  학습된 정책([[02-foundations/rl-basics|RL]], [[01-canonical-papers/notes/4-vla/pi0|VLA]]) —
  층마다 모델링 부담을 더 흡수한다.

> [!example] 계산 예제 · Worked example
> 단위 관성의 토크 입력 PD: $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$, $K_p = 100$으로 잡는다.
> - $\omega_n = \sqrt{K_p} = 10$ rad/s.
> - 임계 감쇠: $K_d = 2\sqrt{K_p} = 20$, 즉 $\zeta = 1$.
> - 2% 정착 시간 $\approx 4/(\zeta\omega_n) = 4/10 = 0.4$ s (MR §11.3은 시정수 $t = 1/(\zeta\omega_n)$일 때 정착 $\approx 4t$로 준다).
> - 댐퍼를 절반으로, $K_d = 10$: $\zeta = 10/(2\cdot 10) = 0.5$.
> - 오버슈트 $= e^{-\pi\zeta/\sqrt{1-\zeta^2}} \approx 16\%$ (MR도 $\zeta = 0.5$에 16%를 든다), 정착 $\approx 4/(0.5\cdot 10) = 0.8$ s.
> - $K_d$를 절반으로 줄여도 빨라지지 않는다. $\zeta\omega_n$이 절반이 되어 정착 시간은 두 배가 되고 오차가 오버슈트한다.

**위키 연결**: VLA 출력은 플랫폼마다 위치·속도·토크·임피던스 인터페이스와 저수준 루프를
거친다. 접촉 안전은 임피던스 제어 하나가 아니라 액추에이터, 제한기, 수동 순응성, 속도,
과제 설정과 제어를 포함한 전체 스택이 결정한다.

### Self-check · 스스로 점검

1. In $\ddot e + K_d\dot e + K_p e = 0$, what relation between $K_d$ and $K_p$ gives critical damping? · 임계 감쇠가 되는 $K_d$와 $K_p$의 관계는?
2. What does "computed torque is only as good as the model" mean concretely — what is left when $M, c, g$ are wrong? · 계산 토크 제어가 "모델만큼만 좋다"는 말의 구체적 의미는?
3. Name two situations where impedance control beats position control. · 위치 제어 대신 임피던스 제어를 쓰는 대표적 상황 두 가지를 들어라.

> [!tip]- Answers · 정답
> 1. Matching $\ddot e + 2\zeta\omega_n\dot e + \omega_n^2 e = 0$ gives $\omega_n^2 = K_p$ and $2\zeta\omega_n = K_d$, so $\zeta = 1 \iff K_d = 2\sqrt{K_p}$ ([[02-foundations/engineering-math|0.5 §8]]). · $\zeta = 1 \Leftrightarrow K_d = 2\sqrt{K_p}$.
> 2. The cancellation is incomplete, so residual nonlinear terms remain inside the error dynamics — they act as a disturbance the PD gains must suppress. The error dynamics are no longer exactly linear, and both tracking performance and stability margin degrade as model error grows. · 상쇄가 불완전해 잔차 비선형 항이 남고, 모델 오차가 클수록 성능·안정 여유가 준다.
> 3. Contact tasks (polishing, insertion — where a small position error against a stiff surface produces a huge force) and human collaboration (compliance so a collision is survivable). Both are cases where the *force–motion relationship* matters more than positional accuracy. · 접촉 작업과 인간 협업 — 힘-운동 관계가 위치 정확도보다 중요한 경우.
