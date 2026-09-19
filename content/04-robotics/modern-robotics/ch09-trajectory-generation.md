---
title: "MR Ch.09 — Trajectory Generation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.9** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> Differentiating polynomials ([[02-foundations/engineering-math|0.5 §1]]) and the idea of separating path from timing are all you need — the lightest chapter in the track.
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
  bang-bang structure (at every instant the path acceleration sits at its maximum or its
  minimum, never in between — typically full acceleration, then a switch to full deceleration).
- Smoothness matters physically: discontinuous acceleration = torque spikes = vibration
  (the torque is $\tau = M(\theta)\ddot\theta + c + g$ from ch.8, and $c$, $g$ vary smoothly
  with the state, so a jump in $\ddot\theta$ is a jump in commanded torque)
  ([[02-foundations/signal-processing|signal processing]]'s frequency lens applies).

> [!example] Worked example · 계산 예제
> One joint moves $\Delta\theta = 1.2$ rad in $T = 2$ s. Scale the unit-move peaks by $\Delta\theta$:
> - **Cubic**: peak velocity $1.5 \cdot 1.2/2 = 0.9$ rad/s; peak acceleration $6 \cdot 1.2/2^2 = 1.8$ rad/s².
> - **Quintic**: peak velocity $1.875 \cdot 1.2/2 = 1.125$ rad/s; peak acceleration $5.77 \cdot 1.2/2^2 \approx 1.73$ rad/s².
>
> Now suppose the actuator allows $v_{\max} = 0.8$ rad/s and $a_{\max} = 2$ rad/s², and run a **trapezoidal** profile instead:
> - Accelerate: $v_{\max}/a_{\max} = 0.4$ s, covering $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16$ rad. Decelerate: the same 0.4 s and 0.16 rad.
> - Cruise: the remaining $1.2 - 0.32 = 0.88$ rad at 0.8 rad/s takes $1.1$ s.
> - Total: $0.4 + 1.1 + 0.4 = 1.9$ s — faster than the 2 s polynomial moves.
>
> **Which limit binds**: velocity. Both polynomials stay under $a_{\max}$ (1.8 and 1.73 < 2) but exceed $v_{\max}$ (0.9 and 1.125 > 0.8), so at $T = 2$ s neither is executable on this joint; the trapezoid saturates $v_{\max}$ by construction.
>
> The homework's infeasibility claim *is* $0.9>0.8$. A cubic on P2 that ignores contact still does not bound $F_n$ on a P3-stiffness wall.

**Wiki connections**: [[01-canonical-papers/notes/4-vla/act|action chunks]] and
[[01-canonical-papers/notes/4-vla/diffusion-policy|denoised trajectories]] are *learned*
replacements for exactly this chapter; classical time scaling still wraps learned outputs
on real hardware for safety/limits.

### Problem set · 과제

Tier C. Claim-reading. Running task: time a **P2** move toward the panel ([[02-foundations/lab-plants|0.6]]).

1. **Claim.** Which number is the claim that the cubic at $T=2\,\mathrm{s}$ is infeasible on $v_{\max}=0.8\,\mathrm{rad/s}$?
2. **Falsify.** What actuator spec would falsify “the trapezoid is faster than the $2\,\mathrm{s}$ polynomials”?
3. **Task.** A cubic in P2's joints that ignores contact: what can it not promise at the panel?

> [!tip]- Solutions
> 1. Peak cubic velocity $0.9\,\mathrm{rad/s}>0.8$ — that comparison *is* the infeasibility claim (the example's “which limit binds”).
> 2. $v_{\max}\ge1.125\,\mathrm{rad/s}$ and a slower trapezoid (lower $a_{\max}$, or $v_{\max}$ so small the cruise disappears and total time exceeds $2\,\mathrm{s}$). Then the $2\,\mathrm{s}$ polynomials would be executable and could win on time.
> 3. Smooth $\theta(t)$ does not bound $F_n$ on a P3-stiffness wall. Discontinuous $\ddot\theta$ is a torque spike (ch.8); contact force is a different object.

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
  빠른 $s(t)$ 찾기 — 고전적 뱅뱅 구조(매 순간 경로 가속도가 최댓값이나 최솟값에 붙어 있고 그 사이 값은 쓰지 않는다 — 보통 최대 가속 후 최대 감속으로 전환)를 갖는 [[02-foundations/optimization|최적화]] 문제.
- 매끄러움은 물리적으로 중요하다: 불연속 가속도 = 토크 스파이크 = 진동
  (8장의 토크는 $\tau = M(\theta)\ddot\theta + c + g$이고 $c$, $g$는 상태에 따라 매끄럽게
  변하므로, $\ddot\theta$가 튀면 명령 토크도 튄다)
  ([[02-foundations/signal-processing|신호처리]]의 주파수 렌즈가 적용된다).

> [!example] 계산 예제 · Worked example
> 관절 하나가 $T = 2$ s 동안 $\Delta\theta = 1.2$ rad 움직인다. 단위 이동의 최댓값에 $\Delta\theta$를 곱한다:
> - **3차**: 최대 속도 $1.5 \cdot 1.2/2 = 0.9$ rad/s, 최대 가속도 $6 \cdot 1.2/2^2 = 1.8$ rad/s².
> - **5차**: 최대 속도 $1.875 \cdot 1.2/2 = 1.125$ rad/s, 최대 가속도 $5.77 \cdot 1.2/2^2 \approx 1.73$ rad/s².
>
> 이제 액추에이터 한계가 $v_{\max} = 0.8$ rad/s, $a_{\max} = 2$ rad/s²라 하고 **사다리꼴** 프로파일을 쓴다:
> - 가속: $v_{\max}/a_{\max} = 0.4$ s 동안 $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16$ rad 이동. 감속도 똑같이 0.4 s, 0.16 rad.
> - 순항: 남은 $1.2 - 0.32 = 0.88$ rad를 0.8 rad/s로 가는 데 $1.1$ s.
> - 합계: $0.4 + 1.1 + 0.4 = 1.9$ s — 2 s짜리 다항식 이동보다 빠르다.
>
> **어느 한계가 걸리는가**: 속도다. 두 다항식 모두 가속도는 $a_{\max}$ 아래지만(1.8, 1.73 < 2) 속도는 $v_{\max}$를 넘으므로(0.9, 1.125 > 0.8) $T = 2$ s로는 이 관절에서 실행할 수 없다. 사다리꼴은 구성상 $v_{\max}$에 딱 맞춘다.

**위키 연결**: [[01-canonical-papers/notes/4-vla/act|행동 청크]]와
[[01-canonical-papers/notes/4-vla/diffusion-policy|노이즈 제거된 궤적]]은 정확히 이 장의 *학습된*
대체물이고, 실제 하드웨어에서는 안전/한계를 위해 고전적 시간 스케일링이 학습 출력을 여전히
감싼다.

### Self-check · 스스로 점검

1. For the cubic scaling $s(t) = 3t^2/T^2 - 2t^3/T^3$, compute $s(0), s(T), \dot s(0), \dot s(T)$ and confirm the boundary conditions. · 3차 시간 스케일링에서 $s(0), s(T), \dot s(0), \dot s(T)$를 계산해 경계 조건을 확인하라.
2. What does quintic scaling buy over cubic, and what does it cost? · 5차 스케일링이 3차보다 나은 점은 무엇이고, 그 대가는?
3. Why is the trapezoidal velocity profile the industrial default? · 사다리꼴 속도 프로파일이 산업 제어기의 기본값인 실용적 이유는?

> [!tip]- Answers · 정답
> 1. $s(0)=0$, $s(T)=1$; $\dot s = 6t/T^2 - 6t^2/T^3$, so $\dot s(0) = \dot s(T) = 0$ — it starts and ends at rest, which is exactly the point-to-point requirement. · 양 끝에서 정지한다.
> 2. Quintic also zeroes the endpoint *accelerations*, so torque is continuous at the ends (no jolt). The cost is a higher peak velocity for the same duration ($1.875/T$ vs $1.5/T$) — note the peak *acceleration* is actually lower than cubic's ($5.77/T^2$ vs $6/T^2$), so it is speed, not torque, that you pay. · 양 끝 가속도까지 0이라 토크가 매끄럽다; 대가는 같은 시간에서 최대 속도가 커지는 것이다($1.875/T$ vs $1.5/T$). 최대 가속도는 오히려 작다($5.77/T^2$ vs $6/T^2$). 치르는 것은 토크가 아니라 속도다.
> 3. Its parameters *are* the actuator limits: maximum velocity and maximum acceleration appear directly in the profile, so a machine spec maps onto it one-to-one without solving anything. · 최대 속도·가속도 한계를 직접 파라미터로 가져 액추에이터 스펙과 1:1로 대응되기 때문.

### 과제 · Problem set

Tier C. 주장 읽기. 관통 과제: [[02-foundations/lab-plants|0.6]]의 **P2**를 패널까지 시간으로 스케일.

1. **주장.** $T=2\,\mathrm{s}$ 3차가 $v_{\max}=0.8\,\mathrm{rad/s}$에서 실행 불가라는 주장은 어느 숫자인가?
2. **반증.** “사다리꼴이 $2\,\mathrm{s}$ 다항식보다 빠르다”를 깨는 액추에이터 스펙은?
3. **과제.** 접촉을 무시한 P2 관절 3차가 패널에서 약속하지 못하는 것은?

> [!tip]- 정답 · Solutions
> 1. 3차 최대 속도 $0.9>0.8$ — 그 비교가 곧 실행 불가 주장이다.
> 2. $v_{\max}\ge1.125$이고 사다리꼴이 더 느린 경우(낮은 $a_{\max}$, 또는 순항이 사라져 총 시간이 $2\,\mathrm{s}$를 넘는 $v_{\max}$). 그때 $2\,\mathrm{s}$ 다항식이 실행 가능하고 시간에서 이길 수 있다.
> 3. 매끄러운 $\theta(t)$는 P3 강성 벽의 $F_n$을 묶지 않는다. $\ddot\theta$의 불연속은 토크 스파이크(8장)이고, 접촉력은 다른 대상이다.
