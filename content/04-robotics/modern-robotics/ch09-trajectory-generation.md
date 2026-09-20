---
title: "MR Ch.09 — Trajectory Generation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P2, time one named joint move with a trapezoidal and a cubic scaling, say which actuator limit binds each, and predict how the answer moves when the gearing changes."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.9** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> Differentiating polynomials ([[02-foundations/engineering-math|0.5 §1]]) and the idea of separating path from timing are all you need — the lightest chapter in the track. Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] carries the worked move.
> 다항식 미분([[02-foundations/engineering-math|0.5 §1]])과 경로/시간의 분리라는 아이디어만 있으면 된다 — 이 장은 트랙에서 가장 가벼운 장이다. 계산은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**로 한다.

## English

**Core question**: how do we turn "go from A to B" into a smooth, executable function of time?

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], and one named move on it: the **elbow flip** between the two configurations that put the tip on the panel target $(1,1)$, derived in [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]].

$$\theta^{\text{start}} = (0°,\ 90°) \ \longrightarrow\ \theta^{\text{goal}} = (90°,\ -90°), \qquad \Delta\theta_1 = +\tfrac{\pi}{2} = 1.5708\ \mathrm{rad}, \quad \Delta\theta_2 = -\pi = -3.1416\ \mathrm{rad}$$

so the elbow travels exactly twice as far as the shoulder, which is the fact the whole page turns on. The **path** is the straight line between those two points of joint space, $\theta(s) = \theta^{\text{start}} + s\,\Delta\theta$ with $s \in [0,1]$; this page only chooses $s(t)$.

**Actuator limits, frozen here** (0.6 gives P2 geometry, not motors, so this page defines them and never changes them): every joint of P2 obeys

$$|\dot\theta_i| \le v_{\max} = 0.8\ \mathrm{rad/s}, \qquad |\ddot\theta_i| \le a_{\max} = 2\ \mathrm{rad/s^2}$$

which are the same two numbers the generic example in §1 already uses, now attached to the plant.

> [!warning] A time scaling is not a collision check · 시간 스케일링은 충돌 검사가 아니다
> This straight joint-space path is *not* collision-free against the panel: [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] shows it drives the arm $\sqrt{2}-1 = 0.414\,\mathrm{m}$ into the wall at its midpoint. Timing a path and clearing a path are different questions, and this chapter answers only the first.
> 이 직선 관절 경로는 패널에 대해 충돌이 없지 *않다*. [[04-robotics/modern-robotics/ch10-motion-planning|10장]]이 중간점에서 팔이 벽 안으로 $\sqrt{2}-1 = 0.414\,\mathrm{m}$ 들어감을 보인다. 경로에 시간을 입히는 것과 경로를 비우는 것은 다른 질문이고, 이 장은 앞의 것만 답한다.

### Homework diagram · 과제가 그릴 그림

One figure, three stacked panels sharing a horizontal time axis that runs from $0$ to $6\,\mathrm{s}$. Plot the **elbow** only.

- **Top, $\theta_2(t)$.** Two curves from $90°$ down to $-90°$: the trapezoid's (straight in the middle, parabolic at both ends) and the cubic's (an S-curve). Mark where each one arrives.
- **Middle, $\dot\theta_2(t)$.** Draw the limit $v_{\max} = 0.8\,\mathrm{rad/s}$ as a horizontal dashed line. The trapezoid is a trapezoid: a $0.4\,\mathrm{s}$ ramp up, a flat top *on* the dashed line, a $0.4\,\mathrm{s}$ ramp down. The cubic is a single parabola that just kisses the dashed line at its midpoint. Shade the trapezoid's flat top and label it with its duration.
- **Bottom, $\ddot\theta_2(t)$.** Draw $a_{\max} = 2\,\mathrm{rad/s^2}$ as a dashed line. The trapezoid is two rectangles, $+a_{\max}$ then $-a_{\max}$, with zero between — and it *touches* the dashed line. The cubic is a straight line falling from a small positive value through zero to its negative, nowhere near the dashed line. Write the cubic's peak next to it.

The figure's whole message is which dashed line each profile touches. The problem set asks for the same three panels after the joint is re-geared, and the answer changes which line is touched.

### Worked on the plant · 장치로 한 번 끝까지

Both joints ride one scaling $s(t)$, so joint $i$ has $\dot\theta_i = \Delta\theta_i\,\dot s$ and $\ddot\theta_i = \Delta\theta_i\,\ddot s$. Every peak is therefore proportional to $|\Delta\theta_i|$, and the joint with the largest $|\Delta\theta_i|$ hits its limit first. Here that is the elbow, at $|\Delta\theta_2| = \pi = 3.1416\,\mathrm{rad}$, exactly twice the shoulder. **Design the scaling for the elbow and the shoulder follows for free.**

**A — the trapezoid.** First decide whether a cruise phase exists at all. Ramping to $v_{\max}$ and straight back down covers $2 \cdot \tfrac12 a_{\max}t_a^2$ with $t_a = v_{\max}/a_{\max}$, i.e.

$$\Delta\theta^{*} = \frac{v_{\max}^2}{a_{\max}} = \frac{0.8^2}{2} = 0.32\ \mathrm{rad}$$

and since our $3.1416\,\mathrm{rad}$ is far above that, the profile is a true trapezoid rather than a triangle. Then:

- ramp time $t_a = v_{\max}/a_{\max} = 0.8/2 = 0.4\ \mathrm{s}$, covering $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16\ \mathrm{rad}$ on the way up and $0.16\,\mathrm{rad}$ on the way down;
- cruise distance $3.1416 - 0.32 = 2.8216\ \mathrm{rad}$, at $0.8\,\mathrm{rad/s}$, taking $2.8216/0.8 = 3.5270\ \mathrm{s}$;
- total $T_{\text{trap}} = 0.4 + 3.5270 + 0.4 = \mathbf{4.327\ s}$, of which the cruise is $3.5270/4.327 = 81.5\,\%$.

Check the shoulder, which rides the same $s(t)$ at half the amplitude: peak velocity $0.5 \times 0.8 = 0.4\,\mathrm{rad/s}$ and peak acceleration $0.5 \times 2 = 1\,\mathrm{rad/s^2}$. Both are at half their limits, so the shoulder is idle in the binding sense — it never constrains anything.

**B — the cubic, on the same move.** For $s(t) = 3t^2/T^2 - 2t^3/T^3$ the unit-move peaks are $\dot s_{\max} = 1.5/T$ at $t = T/2$ and $|\ddot s|_{\max} = 6/T^2$ at the two ends, so the elbow's peaks are $1.5\,\Delta\theta/T$ and $6\,\Delta\theta/T^2$. Invert each limit separately for the shortest admissible duration:

$$T_v = \frac{1.5\,\Delta\theta}{v_{\max}} = \frac{1.5 \times 3.1416}{0.8} = 5.8905\ \mathrm{s}, \qquad T_a = \sqrt{\frac{6\,\Delta\theta}{a_{\max}}} = \sqrt{\frac{6 \times 3.1416}{2}} = 3.0700\ \mathrm{s}$$

because a longer $T$ lowers both peaks, so each limit sets a floor and the move must satisfy the larger of the two. Here $T_v > T_a$, so $T_{\text{cubic}} = \mathbf{5.891\ s}$ and **velocity is the binding limit**. Confirm by back-substitution: at that duration the peak acceleration is $6 \times 3.1416/5.8905^2 = 0.543\,\mathrm{rad/s^2}$, only $27\,\%$ of $a_{\max}$ — the motor's torque is almost entirely unused.

**C — read the two against each other.** Force the cubic into the trapezoid's duration and it asks for $1.5 \times 3.1416/4.327 = 1.089\,\mathrm{rad/s}$, which is $36\,\%$ over $v_{\max}$: at $T = 4.327\,\mathrm{s}$ the cubic is simply not executable on this joint. Compare the two admissible durations instead:

$$\frac{T_{\text{cubic}}}{T_{\text{trap}}} = \frac{5.8905}{4.3270} = 1.361 \quad\Longrightarrow\quad \text{the trapezoid finishes } 26.5\,\% \text{ sooner}$$

and the reason is visible in the middle panel of the diagram: the trapezoid sits *at* $v_{\max}$ for $81.5\,\%$ of the move, while the cubic reaches $v_{\max}$ at one instant and is below it everywhere else. Spending the whole move at the limit is the entire advantage, and it is paid for with a discontinuous acceleration at the two corners.

**D — which limit binds, in general.** Setting $T_v = T_a$ and solving gives the crossover for a cubic:

$$\Delta\theta^{\dagger} = \frac{8}{3}\cdot\frac{v_{\max}^2}{a_{\max}} = \frac{8}{3}\cdot\frac{0.64}{2} = 0.853\ \mathrm{rad}$$

because $1.5\Delta\theta/v_{\max} = \sqrt{6\Delta\theta/a_{\max}}$ squares to $2.25\Delta\theta^2/v_{\max}^2 = 6\Delta\theta/a_{\max}$. Above $0.853\,\mathrm{rad}$ velocity binds; below it acceleration binds. Both moves on this page — the elbow's $3.1416$ and §1's $1.2$ — are above it, which is why both are velocity-bound. The problem set moves the plant to the other side of this line without changing $\Delta\theta$ at all.

### 1. The chapter in one list

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
> The claim of infeasibility *is* $0.9>0.8$. A cubic on P2 that ignores contact still does not bound $F_n$ on a P3-stiffness wall.

### 2. Time scaling, defined

A **time scaling** is a *function* $s: [0,T] \to [0,1]$, not a path and not a trajectory. It has three defining conditions, and dropping any one of them breaks something specific:

- **Endpoints**: $s(0) = 0$ and $s(T) = 1$, so the move starts at the start and finishes at the goal.
- **Monotonicity**: $\dot s(t) \ge 0$, so the robot never retraces the path. A scaling that dips backwards is a different path, not a different timing.
- **Smoothness to the order the hardware needs**: at least $C^1$ so velocity is continuous; $C^2$ if torque must be continuous.

The trajectory is then the composition $\theta(t) = \theta(s(t))$, and differentiating it once and twice gives the two identities every calculation on this page uses:

$$\dot\theta(t) = \frac{d\theta}{ds}\,\dot s, \qquad \ddot\theta(t) = \frac{d\theta}{ds}\,\ddot s + \frac{d^2\theta}{ds^2}\,\dot s^2$$

where the second term vanishes for a straight-line path in joint space, because $d^2\theta/ds^2 = 0$ there, which is why P2's elbow flip reduces to $\ddot\theta_i = \Delta\theta_i\,\ddot s$.

- **Example**: the cubic $s = 3t^2/T^2 - 2t^3/T^3$. Check the conditions: $s(0)=0$, $s(T)=1$, $\dot s = 6t/T^2 - 6t^2/T^3 = (6t/T^2)(1 - t/T) \ge 0$ on $[0,T]$, and $\dot s(0) = \dot s(T) = 0$.
- **Non-example**: $s(t) = \sin(2\pi t/T)$. It is smooth and it starts at $0$, but it is not monotone and $s(T) = 0 \neq 1$ — it returns to the start, so it is not a point-to-point scaling at all.
- **Why it matters**: because the scaling is a separate object, an actuator-limit question ("can this motor do it?") never touches the geometry, and a clearance question ("does this path hit the panel?") never touches the timing. Mixing them is how a planner gets blamed for a motor's limits.

### 3. The trapezoidal profile, defined

A **trapezoidal velocity profile** is the time scaling whose *velocity* $\dot s$ is piecewise linear with three phases — constant acceleration $+a_{\max}$, constant velocity $v_{\max}$, constant deceleration $-a_{\max}$ — so that both actuator limits are attained rather than approached. Applied to a joint move of size $\Delta\theta$, its duration is

$$T_{\text{trap}} = \frac{\Delta\theta}{v_{\max}} + \frac{v_{\max}}{a_{\max}} \qquad \text{when } \Delta\theta \ge \frac{v_{\max}^2}{a_{\max}}$$

because the cruise covers $\Delta\theta - v_{\max}^2/a_{\max}$ at speed $v_{\max}$ while the two ramps take $v_{\max}/a_{\max}$ between them. Check it on the elbow: $3.1416/0.8 + 0.8/2 = 3.9270 + 0.4 = 4.327\,\mathrm{s}$, the number derived the long way above.

- **Example**: P2's elbow flip, $T_{\text{trap}} = 4.327\,\mathrm{s}$ with an $81.5\,\%$ cruise.
- **Degenerate case, not a non-example**: when $\Delta\theta < v_{\max}^2/a_{\max}$ the cruise phase has negative length, the profile collapses to a **triangle**, and the duration is $T_{\text{tri}} = 2\sqrt{\Delta\theta/a_{\max}}$ with a peak velocity $a_{\max}T/2$ that never reaches $v_{\max}$. Using the trapezoid formula there returns a *shorter* time than physics allows, which is the standard way this calculation is got wrong.
- **Non-example**: a velocity profile that is trapezoidal in *shape* but whose top is at $0.6\,v_{\max}$. It is a perfectly legal time scaling and it is not the trapezoidal profile, because the defining property is saturation of both limits, not the silhouette.
- **Why it matters**: its two parameters *are* the machine's two spec numbers, so a datasheet maps onto it without solving anything. That is why industrial controllers run it and why it is the baseline any fancier scaling has to beat.

**Wiki connections**: [[01-canonical-papers/notes/4-vla/act|action chunks]] and
[[01-canonical-papers/notes/4-vla/diffusion-policy|denoised trajectories]] are *learned*
replacements for exactly this chapter; classical time scaling still wraps learned outputs
on real hardware for safety/limits.

### Self-check

1. For the cubic scaling $s(t) = 3t^2/T^2 - 2t^3/T^3$, compute $s(0), s(T), \dot s(0), \dot s(T)$ and confirm the boundary conditions.
2. What does quintic scaling buy over cubic, and what does it cost?
3. Why is the trapezoidal velocity profile the industrial default?
4. P2's shoulder alone must move $\Delta\theta_1 = \pi/2$ with the catalog limits. Which limit binds, and what is the trapezoid's duration?

> [!tip]- Answers
> 1. $s(0)=0$, $s(T)=1$; $\dot s = 6t/T^2 - 6t^2/T^3$, so $\dot s(0) = \dot s(T) = 0$ — it starts and ends at rest, which is exactly the point-to-point requirement.
> 2. Quintic also zeroes the endpoint *accelerations*, so torque is continuous at the ends (no jolt). The cost is a higher peak velocity for the same duration ($1.875/T$ vs $1.5/T$) — note the peak *acceleration* is actually lower than cubic's ($5.77/T^2$ vs $6/T^2$), so it is speed, not torque, that you pay.
> 3. Its parameters *are* the actuator limits: maximum velocity and maximum acceleration appear directly in the profile, so a machine spec maps onto it one-to-one without solving anything.
> 4. $\Delta\theta_1 = 1.5708 > \Delta\theta^{*} = 0.32$, so it is still a true trapezoid, and $1.5708 > \Delta\theta^{\dagger} = 0.853$, so velocity binds. $T_{\text{trap}} = 1.5708/0.8 + 0.4 = 1.963 + 0.4 = 2.363\,\mathrm{s}$ — the $\Delta\theta/v_{\max}$ term is exactly half the elbow's, while the $v_{\max}/a_{\max}$ ramp term does not scale with the move at all.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same plant **P2** and the same elbow flip, $|\Delta\theta_2| = \pi\,\mathrm{rad}$, but the joint is re-geared: a taller gear ratio raises the top speed and cuts the torque, giving $v_{\max} = 1.6\,\mathrm{rad/s}$ and $a_{\max} = 0.5\,\mathrm{rad/s^2}$.

1. **Draw.** The same three stacked panels for the elbow under the new limits. Before drawing, decide which of the two dashed lines each profile touches now — the shapes change, and one of them loses a phase entirely.
2. **Derive.** (a) The trapezoid: evaluate $v_{\max}^2/a_{\max}$ first and say what kind of profile results, then give its duration and its peak velocity. (b) The cubic: compute $T_v$ and $T_a$, state $T_{\text{cubic}}$ and which limit binds. (c) The ratio $T_{\text{cubic}}/T_{\text{trap}}$, and show that under these conditions the ratio does not depend on $\Delta\theta$ or on $a_{\max}$ at all.
3. **Interpret.** The re-gearing doubled the top speed and quartered the acceleration. Did the elbow flip get faster or slower, and by how much against the catalog numbers? Which of the two limits is worth buying, and what does the crossover $\Delta\theta^{\dagger}$ say about when that answer flips?

> [!tip]- Solutions
> 1. Velocity: the trapezoid's flat top disappears, so the middle panel shows a triangle peaking at $1.2533\,\mathrm{rad/s}$, below the new $v_{\max}$ dashed line at $1.6$. Acceleration: both profiles now press against the $a_{\max}$ line — the triangle touches it over both halves, and the cubic touches it at the two endpoints.
> 2. (a) $v_{\max}^2/a_{\max} = 2.56/0.5 = 5.12\,\mathrm{rad} > \pi$, so the move is too short to reach top speed and the profile is a **triangle**: $T_{\text{tri}} = 2\sqrt{\pi/0.5} = 2 \times 2.5066 = 5.013\,\mathrm{s}$, peak velocity $a_{\max}T/2 = 0.5 \times 2.5066 = 1.2533\,\mathrm{rad/s}$, comfortably under $1.6$. (b) $T_v = 1.5\pi/1.6 = 2.945\,\mathrm{s}$, $T_a = \sqrt{6\pi/0.5} = 6.140\,\mathrm{s}$, so $T_{\text{cubic}} = 6.140\,\mathrm{s}$ and **acceleration** binds — the limit has swapped. (c) $6.140/5.013 = 1.2247$. When both profiles are acceleration-bound the durations are $2\sqrt{\Delta\theta/a_{\max}}$ and $\sqrt{6\Delta\theta/a_{\max}}$, whose ratio is $\sqrt{6}/2 = \sqrt{3/2} = 1.2247$ with $\Delta\theta$ and $a_{\max}$ cancelling.
> 3. Slower, in both cases: $5.013$ against $4.327\,\mathrm{s}$ for the trapezoid ($+15.9\,\%$) and $6.140$ against $5.891\,\mathrm{s}$ for the cubic ($+4.2\,\%$). Buying top speed was worthless here because the move never reaches it; the acceleration is what was worth keeping. The crossover says when: $\Delta\theta^{\dagger} = \tfrac83 v_{\max}^2/a_{\max}$ rises from $0.853$ to $13.65\,\mathrm{rad}$, so under the new gearing every move shorter than $13.65\,\mathrm{rad}$ is acceleration-bound. Top speed only starts paying above that, and P2's joints never travel that far in one move.

## 한국어

**핵심 질문**: "A에서 B로 가라"를 매끄럽고 실행 가능한 시간 함수로 어떻게 바꾸는가?

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 그리고 그 위의 이름 붙은 이동 하나. 말단을 패널 목표 $(1,1)$에 두는 두 자세 사이의 **엘보 뒤집기**이며, 두 자세는 [[04-robotics/modern-robotics/ch02-configuration-space|2장]]에서 유도했다.

$$\theta^{\text{start}} = (0°,\ 90°) \ \longrightarrow\ \theta^{\text{goal}} = (90°,\ -90°), \qquad \Delta\theta_1 = +\tfrac{\pi}{2} = 1.5708\ \mathrm{rad}, \quad \Delta\theta_2 = -\pi = -3.1416\ \mathrm{rad}$$

이므로 엘보가 어깨보다 정확히 두 배 멀리 간다. 이 페이지 전체가 이 사실 위에서 돈다. **경로**는 관절 공간의 두 점을 잇는 직선 $\theta(s) = \theta^{\text{start}} + s\,\Delta\theta$, $s \in [0,1]$이고, 이 페이지는 $s(t)$만 고른다.

**여기서 고정하는 액추에이터 한계**(0.6은 P2의 기하를 주지 기구동을 주지 않으므로, 이 페이지가 정의하고 다시 바꾸지 않는다): P2의 모든 관절은

$$|\dot\theta_i| \le v_{\max} = 0.8\ \mathrm{rad/s}, \qquad |\ddot\theta_i| \le a_{\max} = 2\ \mathrm{rad/s^2}$$

를 지킨다. §1의 일반 예제가 이미 쓰던 그 두 숫자를 이제 장치에 붙인 것이다.

### 과제가 그릴 그림 · Homework diagram

그림 하나, 가로 시간축($0$부터 $6\,\mathrm{s}$)을 공유하는 세 단. **엘보**만 그린다.

- **위, $\theta_2(t)$.** $90°$에서 $-90°$로 내려가는 곡선 둘: 사다리꼴(가운데가 직선, 양 끝이 포물선)과 3차(S자). 각각 언제 도착하는지 표시한다.
- **가운데, $\dot\theta_2(t)$.** 한계 $v_{\max} = 0.8\,\mathrm{rad/s}$를 가로 점선으로 긋는다. 사다리꼴은 말 그대로 사다리꼴이다. $0.4\,\mathrm{s}$ 상승, 점선 *위에* 붙은 평평한 꼭대기, $0.4\,\mathrm{s}$ 하강. 3차는 중간에서 점선을 살짝 스치는 포물선 하나다. 사다리꼴의 평평한 부분을 칠하고 그 길이를 적는다.
- **아래, $\ddot\theta_2(t)$.** $a_{\max} = 2\,\mathrm{rad/s^2}$를 점선으로 긋는다. 사다리꼴은 직사각형 둘, $+a_{\max}$ 다음 $-a_{\max}$, 사이는 0이며 점선에 *닿는다*. 3차는 작은 양수에서 0을 지나 음수로 내려가는 직선이고 점선 근처에도 못 간다. 3차의 최댓값을 옆에 적는다.

이 그림이 말하려는 전부는 각 프로파일이 어느 점선에 닿느냐다. 과제는 관절의 기어비를 바꾼 뒤 같은 세 단을 요구하고, 답에서 닿는 점선이 바뀐다.

### 장치로 한 번 끝까지 · Worked on the plant

두 관절이 하나의 스케일링 $s(t)$를 타므로 관절 $i$는 $\dot\theta_i = \Delta\theta_i\,\dot s$, $\ddot\theta_i = \Delta\theta_i\,\ddot s$다. 따라서 모든 최댓값이 $|\Delta\theta_i|$에 비례하고, $|\Delta\theta_i|$가 가장 큰 관절이 먼저 한계에 닿는다. 여기서는 엘보이며 $|\Delta\theta_2| = \pi = 3.1416\,\mathrm{rad}$, 어깨의 정확히 두 배다. **엘보에 맞춰 스케일링을 설계하면 어깨는 저절로 따라온다.**

**A — 사다리꼴.** 먼저 순항 구간이 존재하는지부터 정한다. $v_{\max}$까지 올렸다가 곧바로 내리면 $t_a = v_{\max}/a_{\max}$일 때 $2 \cdot \tfrac12 a_{\max}t_a^2$를 이동하므로

$$\Delta\theta^{*} = \frac{v_{\max}^2}{a_{\max}} = \frac{0.8^2}{2} = 0.32\ \mathrm{rad}$$

이고, 우리의 $3.1416\,\mathrm{rad}$이 그보다 훨씬 크므로 삼각형이 아니라 진짜 사다리꼴이다. 그다음:

- 상승 시간 $t_a = v_{\max}/a_{\max} = 0.8/2 = 0.4\ \mathrm{s}$, 올라가며 $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16\ \mathrm{rad}$, 내려가며 $0.16\,\mathrm{rad}$;
- 순항 거리 $3.1416 - 0.32 = 2.8216\ \mathrm{rad}$, $0.8\,\mathrm{rad/s}$로 $2.8216/0.8 = 3.5270\ \mathrm{s}$;
- 합계 $T_{\text{trap}} = 0.4 + 3.5270 + 0.4 = \mathbf{4.327\ s}$, 그중 순항이 $3.5270/4.327 = 81.5\,\%$.

같은 $s(t)$를 절반 진폭으로 타는 어깨를 확인한다. 최대 속도 $0.5 \times 0.8 = 0.4\,\mathrm{rad/s}$, 최대 가속도 $0.5 \times 2 = 1\,\mathrm{rad/s^2}$. 둘 다 한계의 절반이라 어깨는 아무것도 구속하지 않는다.

**B — 같은 이동의 3차.** $s(t) = 3t^2/T^2 - 2t^3/T^3$의 단위 이동 최댓값은 $t = T/2$에서 $\dot s_{\max} = 1.5/T$, 양 끝에서 $|\ddot s|_{\max} = 6/T^2$이므로 엘보의 최댓값은 $1.5\,\Delta\theta/T$와 $6\,\Delta\theta/T^2$다. 두 한계를 각각 뒤집어 최소 허용 시간을 구한다:

$$T_v = \frac{1.5\,\Delta\theta}{v_{\max}} = \frac{1.5 \times 3.1416}{0.8} = 5.8905\ \mathrm{s}, \qquad T_a = \sqrt{\frac{6\,\Delta\theta}{a_{\max}}} = \sqrt{\frac{6 \times 3.1416}{2}} = 3.0700\ \mathrm{s}$$

$T$가 길어지면 두 최댓값이 모두 내려가므로 각 한계가 하한을 하나씩 주고 이동은 둘 중 큰 쪽을 만족해야 한다. 여기서는 $T_v > T_a$이므로 $T_{\text{cubic}} = \mathbf{5.891\ s}$, **속도가 걸리는 한계**다. 되대입해 확인하면 그 시간에서 최대 가속도는 $6 \times 3.1416/5.8905^2 = 0.543\,\mathrm{rad/s^2}$, $a_{\max}$의 $27\,\%$에 불과하다. 모터의 토크를 거의 쓰지 않는다.

**C — 둘을 맞대어 읽기.** 3차를 사다리꼴의 시간에 억지로 밀어 넣으면 $1.5 \times 3.1416/4.327 = 1.089\,\mathrm{rad/s}$를 요구하는데 이는 $v_{\max}$의 $36\,\%$ 초과다. $T = 4.327\,\mathrm{s}$에서 3차는 이 관절로 실행 자체가 불가능하다. 대신 각자 허용되는 시간끼리 비교한다:

$$\frac{T_{\text{cubic}}}{T_{\text{trap}}} = \frac{5.8905}{4.3270} = 1.361 \quad\Longrightarrow\quad \text{사다리꼴이 } 26.5\,\% \text{ 먼저 끝난다}$$

이유는 그림 가운데 단에 보인다. 사다리꼴은 이동의 $81.5\,\%$ 동안 $v_{\max}$에 *붙어* 있고, 3차는 한순간만 $v_{\max}$에 닿고 나머지는 그 아래다. 이동 내내 한계에 붙어 있는 것이 이득의 전부이며, 그 대가는 양 모서리의 불연속 가속도다.

**D — 일반적으로 어느 한계가 걸리는가.** $T_v = T_a$로 놓고 풀면 3차의 교차점이 나온다:

$$\Delta\theta^{\dagger} = \frac{8}{3}\cdot\frac{v_{\max}^2}{a_{\max}} = \frac{8}{3}\cdot\frac{0.64}{2} = 0.853\ \mathrm{rad}$$

$1.5\Delta\theta/v_{\max} = \sqrt{6\Delta\theta/a_{\max}}$를 제곱하면 $2.25\Delta\theta^2/v_{\max}^2 = 6\Delta\theta/a_{\max}$가 되기 때문이다. $0.853\,\mathrm{rad}$ 위에서는 속도가, 아래에서는 가속도가 걸린다. 이 페이지의 두 이동 — 엘보의 $3.1416$과 §1의 $1.2$ — 은 모두 그 위이고, 그래서 둘 다 속도 구속이다. 과제는 $\Delta\theta$를 전혀 건드리지 않고 장치를 이 선의 반대편으로 옮긴다.

### 1. 이 장을 목록 하나로

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
>
> 실행 불가 주장은 곧 $0.9>0.8$이다. 접촉을 무시한 P2 3차는 P3 강성 벽의 $F_n$을 여전히 묶지 못한다.

### 2. 시간 스케일링의 정의

**시간 스케일링**은 *함수* $s: [0,T] \to [0,1]$이다. 경로도 궤적도 아니다. 정의 조건이 셋이고, 하나씩 빠질 때마다 구체적으로 무언가가 깨진다:

- **양 끝**: $s(0) = 0$, $s(T) = 1$. 출발점에서 출발해 목표에서 끝난다.
- **단조성**: $\dot s(t) \ge 0$. 로봇이 경로를 되짚지 않는다. 거꾸로 내려가는 스케일링은 다른 타이밍이 아니라 다른 경로다.
- **하드웨어가 요구하는 차수까지의 매끄러움**: 속도가 연속이려면 최소 $C^1$, 토크가 연속이어야 하면 $C^2$.

궤적은 합성 $\theta(t) = \theta(s(t))$이고, 한 번·두 번 미분하면 이 페이지의 모든 계산이 쓰는 항등식 둘이 나온다:

$$\dot\theta(t) = \frac{d\theta}{ds}\,\dot s, \qquad \ddot\theta(t) = \frac{d\theta}{ds}\,\ddot s + \frac{d^2\theta}{ds^2}\,\dot s^2$$

관절 공간의 직선 경로에서는 $d^2\theta/ds^2 = 0$이라 둘째 항이 사라지고, 그래서 P2의 엘보 뒤집기가 $\ddot\theta_i = \Delta\theta_i\,\ddot s$로 줄어든다.

- **예**: 3차 $s = 3t^2/T^2 - 2t^3/T^3$. 조건을 확인하면 $s(0)=0$, $s(T)=1$, $\dot s = 6t/T^2 - 6t^2/T^3 = (6t/T^2)(1 - t/T) \ge 0$($[0,T]$ 위에서), 그리고 $\dot s(0) = \dot s(T) = 0$.
- **반례**: $s(t) = \sin(2\pi t/T)$. 매끄럽고 $0$에서 시작하지만 단조가 아니고 $s(T) = 0 \neq 1$이다. 출발점으로 돌아오므로 애초에 점대점 스케일링이 아니다.
- **왜 중요한가**: 스케일링이 별개의 대상이라서, 액추에이터 한계 질문("이 모터가 할 수 있나?")이 기하를 건드리지 않고, 여유 공간 질문("이 경로가 패널에 부딪히나?")이 타이밍을 건드리지 않는다. 둘을 섞는 것이 모터의 한계를 계획기 탓으로 돌리는 방식이다.

### 3. 사다리꼴 프로파일의 정의

**사다리꼴 속도 프로파일**은 *속도* $\dot s$가 구간별 일차인 시간 스케일링이다. 구간은 셋 — 일정 가속 $+a_{\max}$, 일정 속도 $v_{\max}$, 일정 감속 $-a_{\max}$ — 이고, 두 액추에이터 한계에 접근하는 것이 아니라 실제로 도달한다. 크기 $\Delta\theta$인 관절 이동에 적용하면 소요 시간은

$$T_{\text{trap}} = \frac{\Delta\theta}{v_{\max}} + \frac{v_{\max}}{a_{\max}} \qquad (\Delta\theta \ge \frac{v_{\max}^2}{a_{\max}}\text{일 때})$$

이다. 순항이 $\Delta\theta - v_{\max}^2/a_{\max}$를 속도 $v_{\max}$로 덮고 두 램프가 합쳐서 $v_{\max}/a_{\max}$를 쓰기 때문이다. 엘보로 확인하면 $3.1416/0.8 + 0.8/2 = 3.9270 + 0.4 = 4.327\,\mathrm{s}$, 위에서 길게 유도한 그 숫자다.

- **예**: P2의 엘보 뒤집기, $T_{\text{trap}} = 4.327\,\mathrm{s}$, 순항 $81.5\,\%$.
- **축퇴하는 경우이지 반례는 아닌 것**: $\Delta\theta < v_{\max}^2/a_{\max}$이면 순항 구간의 길이가 음수가 되어 프로파일이 **삼각형**으로 무너지고, 소요 시간은 $T_{\text{tri}} = 2\sqrt{\Delta\theta/a_{\max}}$, 최대 속도는 $v_{\max}$에 닿지 못하는 $a_{\max}T/2$다. 거기에 사다리꼴 공식을 쓰면 물리가 허용하는 것보다 *짧은* 시간이 나오고, 이 계산이 틀리는 표준적인 방식이 그것이다.
- **반례**: 모양은 사다리꼴인데 꼭대기가 $0.6\,v_{\max}$인 속도 프로파일. 완전히 합법적인 시간 스케일링이지만 사다리꼴 프로파일은 아니다. 정의하는 성질은 실루엣이 아니라 두 한계의 포화이기 때문이다.
- **왜 중요한가**: 파라미터 둘이 곧 기계 사양의 숫자 둘이라, 데이터시트가 아무것도 풀지 않고 그대로 대응된다. 산업 제어기가 이것을 돌리는 이유이자, 더 정교한 스케일링이 이겨야 하는 기준선인 이유다.

**위키 연결**: [[01-canonical-papers/notes/4-vla/act|행동 청크]]와
[[01-canonical-papers/notes/4-vla/diffusion-policy|노이즈 제거된 궤적]]은 정확히 이 장의 *학습된*
대체물이고, 실제 하드웨어에서는 안전/한계를 위해 고전적 시간 스케일링이 학습 출력을 여전히
감싼다.

### 스스로 점검

1. 3차 스케일링 $s(t) = 3t^2/T^2 - 2t^3/T^3$에서 $s(0), s(T), \dot s(0), \dot s(T)$를 계산해 경계 조건을 확인하라.
2. 5차 스케일링이 3차보다 나은 점은 무엇이고, 그 대가는 무엇인가?
3. 사다리꼴 속도 프로파일이 산업 제어기의 기본값인 실용적 이유는?
4. P2 어깨만 카탈로그 한계로 $\Delta\theta_1 = \pi/2$ 움직인다. 어느 한계가 걸리고, 사다리꼴 소요 시간은 얼마인가?

> [!tip]- 정답
> 1. $s(0)=0$, $s(T)=1$이고 $\dot s = 6t/T^2 - 6t^2/T^3$이므로 $\dot s(0) = \dot s(T) = 0$이다. 양 끝에서 정지하며, 이것이 점대점 이동이 요구하는 조건 그대로다.
> 2. 5차는 양 끝의 *가속도*까지 0으로 만들어 끝에서 토크가 연속이다(덜컥거림이 없다). 대가는 같은 소요 시간에서 최대 속도가 커지는 것이다($1.875/T$ 대 $1.5/T$). 최대 *가속도*는 오히려 3차보다 작으므로($5.77/T^2$ 대 $6/T^2$) 치르는 것은 토크가 아니라 속도다.
> 3. 파라미터가 곧 액추에이터 한계이기 때문이다. 최대 속도와 최대 가속도가 프로파일에 그대로 들어가므로 기계 사양이 아무것도 풀지 않고 1:1로 대응된다.
> 4. $\Delta\theta_1 = 1.5708$은 $\Delta\theta^{*} = 0.32$보다 크므로 여전히 진짜 사다리꼴이고, $\Delta\theta^{\dagger} = 0.853$보다도 크므로 속도가 걸린다. $T_{\text{trap}} = 1.5708/0.8 + 0.4 = 1.963 + 0.4 = 2.363\,\mathrm{s}$다. $\Delta\theta/v_{\max}$ 항만 엘보의 절반이고, 램프 항 $v_{\max}/a_{\max}$는 이동 크기와 아예 무관하다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 장치는 같은 **P2**, 이동도 같은 엘보 뒤집기 $|\Delta\theta_2| = \pi\,\mathrm{rad}$이지만 관절의 기어비를 바꾼다. 감속비를 낮춰 최고 속도를 올리고 토크를 깎아 $v_{\max} = 1.6\,\mathrm{rad/s}$, $a_{\max} = 0.5\,\mathrm{rad/s^2}$.

1. **그리기.** 새 한계에서 엘보의 같은 세 단. 그리기 전에 두 프로파일이 각각 어느 점선에 닿는지부터 정하라. 모양이 바뀌고, 한쪽은 구간 하나를 통째로 잃는다.
2. **유도.** (a) 사다리꼴: 먼저 $v_{\max}^2/a_{\max}$를 계산해 어떤 프로파일이 되는지 말하고, 소요 시간과 최대 속도를 구하라. (b) 3차: $T_v$와 $T_a$를 계산해 $T_{\text{cubic}}$과 걸리는 한계를 말하라. (c) 비 $T_{\text{cubic}}/T_{\text{trap}}$를 구하고, 이 조건에서 그 비가 $\Delta\theta$에도 $a_{\max}$에도 의존하지 않음을 보여라.
3. **해석.** 기어비 변경이 최고 속도를 두 배로, 가속도를 1/4로 만들었다. 엘보 뒤집기는 빨라졌는가 느려졌는가, 카탈로그 숫자 대비 얼마인가? 둘 중 어느 한계를 사는 것이 값어치가 있고, 교차점 $\Delta\theta^{\dagger}$는 그 답이 언제 뒤집히는지에 대해 무엇을 말하는가?

> [!tip]- 정답 · Solutions
> 1. 속도: 사다리꼴의 평평한 꼭대기가 사라지므로 가운데 단은 $1.2533\,\mathrm{rad/s}$에서 꼭짓점을 찍는 삼각형이고, 새 $v_{\max}$ 점선 $1.6$보다 아래다. 가속도: 이제 두 프로파일 모두 $a_{\max}$ 선에 붙는다. 삼각형은 양쪽 절반 내내 닿아 있고 3차는 양 끝점에서 닿는다.
> 2. (a) $v_{\max}^2/a_{\max} = 2.56/0.5 = 5.12\,\mathrm{rad} > \pi$이므로 최고 속도에 도달하기에는 이동이 짧고 프로파일은 **삼각형**이다. $T_{\text{tri}} = 2\sqrt{\pi/0.5} = 2 \times 2.5066 = 5.013\,\mathrm{s}$, 최대 속도 $a_{\max}T/2 = 0.5 \times 2.5066 = 1.2533\,\mathrm{rad/s}$로 $1.6$보다 여유 있게 아래다. (b) $T_v = 1.5\pi/1.6 = 2.945\,\mathrm{s}$, $T_a = \sqrt{6\pi/0.5} = 6.140\,\mathrm{s}$이므로 $T_{\text{cubic}} = 6.140\,\mathrm{s}$, **가속도**가 걸린다. 한계가 뒤바뀌었다. (c) $6.140/5.013 = 1.2247$. 두 프로파일이 모두 가속도 구속이면 소요 시간이 $2\sqrt{\Delta\theta/a_{\max}}$와 $\sqrt{6\Delta\theta/a_{\max}}$이고, 비는 $\sqrt{6}/2 = \sqrt{3/2} = 1.2247$로 $\Delta\theta$와 $a_{\max}$가 약분된다.
> 3. 둘 다 느려졌다. 사다리꼴은 $4.327$에서 $5.013\,\mathrm{s}$로 $+15.9\,\%$, 3차는 $5.891$에서 $6.140\,\mathrm{s}$로 $+4.2\,\%$. 여기서 최고 속도를 산 것은 소용이 없었다. 이동이 거기에 닿지 못하기 때문이다. 지킬 값어치가 있었던 것은 가속도다. 교차점이 그 시점을 말한다. $\Delta\theta^{\dagger} = \tfrac83 v_{\max}^2/a_{\max}$가 $0.853$에서 $13.65\,\mathrm{rad}$으로 올라가므로, 새 기어비에서는 $13.65\,\mathrm{rad}$보다 짧은 모든 이동이 가속도 구속이다. 최고 속도는 그 위에서야 값을 하기 시작하고, P2의 관절은 한 번의 이동으로 그만큼 가지 않는다.
