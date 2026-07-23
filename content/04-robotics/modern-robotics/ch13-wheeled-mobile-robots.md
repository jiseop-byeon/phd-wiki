---
title: "MR Ch.13 — Wheeled Mobile Robots"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.13** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] 시작 전 점검 · Before you start
> [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 비홀로노믹 제약과 삼각함수면 충분하다.

## English

**Core question**: how do wheeled bases move, and why is "can't slide sideways" not the same as "can't get there"?

- **The unicycle model** — the essential kinematics of most mobile bases:
  $$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega$$
  Two inputs $(v, \omega)$, three configuration variables — the deficit *is* the
  nonholonomic constraint (no sideways velocity).
- **Differential drive, worked**: wheel radius $r$, half-axle $d$, wheel speeds
  $\omega_R, \omega_L$:
  $$v = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{r(\omega_R - \omega_L)}{2d}$$
  Numbers: $r = 0.1$ m, $d = 0.2$ m, $\omega_R = 10$, $\omega_L = 5$ rad/s
  → $v = 0.75$ m/s, $\omega = 1.25$ rad/s — a gentle left arc. Equal speeds → straight;
  opposite speeds → turn in place.
- **Nonholonomy ≠ unreachability**: a car cannot move sideways *instantaneously*, yet can
  parallel-park into any pose — for these ideal rolling models (unicycle, diff-drive,
  car), the velocity constraints restrict *paths*, not the reachable set. The deep consequence (Brockett): no smooth time-invariant feedback can stabilize
  such systems to a point — why practical controllers track *trajectories* instead.
- **Odometry and its decay**: integrating wheel encoders gives pose, but slip and
  quantization make the error grow without bound — the concrete reason mobile robots fuse
  odometry with external sensing via the
  [[02-foundations/probability|Kalman-filter machinery]] (and, at scale, SLAM).
- **Omni/mecanum wheels** buy back the sideways direction at the cost of payload and
  outdoor robustness — why warehouse robots use them and site robots usually don't.

**Wiki connections**: site navigation for inspection robots
([[05-construction-robotics/index|construction]]) runs on exactly this stack: unicycle
kinematics + [[04-robotics/modern-robotics/ch10-motion-planning|kinodynamic planning]] +
fused localization.

### Self-check

1. For the worked diff-drive, what wheel speeds make the robot spin in place at 1 rad/s?
2. Why can't a smooth static feedback stabilize a car to a parking spot, in one sentence?
3. Odometry error grows without bound; GPS error doesn't. What does the fusion of the two
   give you that neither has alone?

> [!tip]- 정답 · Answers
> 1. 제자리 회전은 $v = 0$, 즉 $\omega_R = -\omega_L$; $\omega = r\omega_R/d = 1$ ⇒ $\omega_R = 2, \omega_L = -2$ rad/s.
> 2. 옆 방향 속도가 없는 시스템은 최종 접근 방향이 제한되어, 연속 시불변 피드백으로는 임의 자세에 점근 안정화할 수 없다(Brockett) — 그래서 궤적 추종으로 우회한다.
> 3. 단기 정밀(오도메트리) + 드리프트 없는 절대 기준(GPS — 단 현장에서는 멀티패스·차폐로 편향이 생길 수 있다) — 칼만 융합이 두 시간 척도의 장점을 모두 취한다.

## 한국어

**핵심 질문**: 바퀴 달린 베이스는 어떻게 움직이고, "옆으로 못 미끄러진다"가 왜 "거기 못 간다"와 다른가?

- **외바퀴(unicycle) 모델** — 대부분의 모바일 베이스의 본질적 기구학:
  $$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega$$
  입력 둘 $(v, \omega)$에 컨피규레이션 변수 셋 — 이 부족분이 *곧* 비홀로노믹 제약이다
  (옆 방향 속도 없음).
- **차동 구동 계산 예제**: 바퀴 반지름 $r$, 반축거 $d$, 바퀴 속도 $\omega_R, \omega_L$:
  $$v = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{r(\omega_R - \omega_L)}{2d}$$
  숫자로: $r = 0.1$ m, $d = 0.2$ m, $\omega_R = 10$, $\omega_L = 5$ rad/s
  → $v = 0.75$ m/s, $\omega = 1.25$ rad/s — 완만한 좌회전 호. 같은 속도 → 직진;
  반대 속도 → 제자리 회전.
- **비홀로노미 ≠ 도달 불가**: 자동차는 *순간적으로* 옆으로 못 가지만 평행 주차로 어떤
  자세든 도달한다 — 이상적 구름 모델(외바퀴·차동 구동·자동차)에서 속도 제약은 *경로*를
  제한할 뿐 도달 집합을 제한하지 않는다. 깊은
  귀결(Brockett): 이런 시스템은 매끄러운 시불변 피드백으로 점에 안정화할 수 없다 —
  실전 제어기가 점이 아니라 *궤적*을 추종하는 이유다.
- **오도메트리와 그 붕괴**: 바퀴 엔코더 적분으로 자세를 얻지만, 미끄럼과 양자화로 오차가
  무한정 자란다 — 모바일 로봇이 오도메트리를 외부 센싱과
  [[02-foundations/probability|칼만 필터 기계장치]]로 융합하는(그리고 규모가 커지면 SLAM으로
  가는) 구체적 이유다.
- **옴니/메카넘 휠**은 옆 방향을 되사는 대신 적재량과 야외 강건성을 지불한다 — 물류
  로봇은 쓰고 현장 로봇은 잘 안 쓰는 이유.

**위키 연결**: 점검 로봇의 현장 항법([[05-construction-robotics/index|건설]])이 정확히 이
스택 위에서 돈다: 외바퀴 기구학 +
[[04-robotics/modern-robotics/ch10-motion-planning|키노다이나믹 계획]] + 융합 위치 추정.

### 스스로 점검

1. 위의 차동 구동에서 1 rad/s로 제자리 회전하려면 바퀴 속도는?
2. 매끄러운 정적 피드백이 자동차를 주차 지점에 안정화할 수 없는 이유를 한 문장으로.
3. 오도메트리 오차는 무한정 자라고 GPS 오차는 안 자란다. 둘의 융합은 각각이 못 주는
   무엇을 주는가?

> [!tip]- 정답 · Answers
> 1. $v = 0$이 되도록 $\omega_R = -\omega_L$; $\omega = r\omega_R/d = 1$ ⇒ $\omega_R = 2, \omega_L = -2$ rad/s.
> 2. 옆 방향 속도가 없어 연속 시불변 피드백으로는 점 안정화가 불가능하다(Brockett) — 궤적 추종으로 우회한다.
> 3. 단기 정밀(오도메트리) + 드리프트 없는 절대 기준(GPS — 현장에서는 멀티패스·차폐 편향 가능)을 동시에 — 칼만 융합이 두 시간 척도의 장점을 결합한다.
