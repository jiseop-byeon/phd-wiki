---
title: "MR Ch.13 — Wheeled Mobile Robots"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On the P6 cart, write the unicycle and differential-drive kinematics, turn a pair of encoder counts into a pose by hand, and rank quantization against slip as error sources."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.13** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> Nonholonomic constraints from [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]] and trigonometry are enough. The object is the cart of **P6** in [[02-foundations/lab-plants|0.6 Lab Plants]], given two wheels below.
> [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 비홀로노믹 제약과 삼각함수면 충분하다. 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6** 카트이고, 아래에서 바퀴 두 개를 달아 준다.

## English

**Core question**: how do wheeled bases move, and why is "can't slide sideways" not the same as "can't get there"?

### Running plant · 이 페이지의 장치

**P6** in [[02-foundations/lab-plants|0.6 Lab Plants]] is a cart on a line with an encoder at $2048$ counts per metre and a clock: vision at $50\,\mathrm{Hz}$, control at $200\,\mathrm{Hz}$, $70\,\mathrm{ms}$ from mid-exposure to applied force. This page lifts it into the plane by giving it two independently driven wheels. Call the result **P6-D**, and freeze it here.

| quantity | value | where it comes from |
|---|---:|---|
| encoder, per wheel | $2048$ counts per metre of wheel travel | **P6** |
| counts per wheel revolution | $1024$, quadrature after decode | defined here |
| wheel circumference | $1024/2048 = 0.500\ \mathrm{m}$ | forced by the two rows above |
| **wheel radius $r$** | $0.500/2\pi = 1/(4\pi) = 0.079577\ \mathrm{m}$ | derived; a $159.2\,\mathrm{mm}$ wheel |
| **half-track $d$** | $0.200\ \mathrm{m}$, so the track is $0.400\ \mathrm{m}$ | defined here, matching §1's worked drive |
| distance per count | $1/2048 = 0.48828\ \mathrm{mm}$ | derived |
| control period | $5\ \mathrm{ms}$ ($200\,\mathrm{Hz}$) | **P6** |
| vision period | $20\ \mathrm{ms}$ ($50\,\mathrm{Hz}$) | **P6** |
| sense-to-act budget | $70\ \mathrm{ms}$ | **P6** |
| nominal speed | $0.500\ \mathrm{m/s}$ | defined here |

The radius is not a free choice: a $1024$-count wheel that must resolve $2048$ counts per metre has to roll exactly $0.5\,\mathrm{m}$ per turn, which fixes $r = 1/(4\pi)$. Pose is $(x, y, \theta)$ with $\theta$ the heading from $+x$.

### Homework diagram · 과제가 그릴 그림

Two panels.

**Left — the geometry.** The cart as a rectangle with its body frame at the wheel-axle midpoint: body $x$ forward, body $y$ to the left. Draw both wheels on the axle at $\pm d$ and label $d = 0.200\,\mathrm{m}$. Extend the axle line to the left until it reaches the **instantaneous centre of rotation** and mark that distance $R = v/\omega$; draw the arc the body frame follows around it. On the arc, write $\Delta s_R$ along the outer wheel's track and $\Delta s_L$ along the inner one. Put a crossed-out sideways arrow on the body $y$ axis: that is the nonholonomic constraint, and it is the one arrow the cart cannot draw.

**Right — the clock.** A time axis with three rows of ticks: control at every $5\,\mathrm{ms}$, vision at every $20\,\mathrm{ms}$, and a single bracket $70\,\mathrm{ms}$ long from a camera mid-exposure mark to the instant force is applied. Under the bracket write how far the cart has travelled at $0.5\,\mathrm{m/s}$. Under one $5\,\mathrm{ms}$ interval write how many counts arrive in it.

The problem set asks for the left panel redrawn for a turn in place, where $R = 0$ and the arc collapses to the axle midpoint.

### Worked on the plant · 장치로 한 번 끝까지

**Step 1 — from the rolling constraint to the unicycle.** A wheel that rolls without slipping has no velocity along its own axle, so the body's velocity is along body $x$ only. Writing that in world coordinates with speed $v$ and turn rate $\omega$:

$$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega$$

because the body $x$ axis points at angle $\theta$. Two inputs, three state variables: the deficit *is* the nonholonomic constraint, and in the form $A(\theta)\dot\theta = 0$ it reads $\dot x\sin\theta - \dot y\cos\theta = 0$.

**Step 2 — from two wheels to $(v,\omega)$.** Each wheel's contact point moves at its own ground speed $\dot s_R$ and $\dot s_L$. The body-frame midpoint is their average and the turn rate is their difference over the track:

$$v = \frac{\dot s_R + \dot s_L}{2} = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{\dot s_R - \dot s_L}{2d} = \frac{r(\omega_R - \omega_L)}{2d}$$

since a rigid body rotating at $\omega$ makes the two points $2d$ apart differ in speed by exactly $2d\,\omega$. The instantaneous turn radius follows as $R = v/\omega = d(\dot s_R + \dot s_L)/(\dot s_R - \dot s_L)$.

**Step 3 — counts to pose, as an algorithm.** This is what the odometry node runs every $5\,\mathrm{ms}$ on the two count differences $\Delta n_R, \Delta n_L$:

1. $\Delta s_R = \Delta n_R/2048$, $\Delta s_L = \Delta n_L/2048$ (metres);
2. $\Delta s = (\Delta s_R + \Delta s_L)/2$ and $\Delta\theta = (\Delta s_R - \Delta s_L)/(2d) = (\Delta s_R - \Delta s_L)/0.4$;
3. $x \mathrel{+}= \Delta s\cos(\theta + \Delta\theta/2)$, $y \mathrel{+}= \Delta s\sin(\theta + \Delta\theta/2)$, $\theta \mathrel{+}= \Delta\theta$.

Step 3 uses the *midpoint* heading rather than the heading at the start of the interval, which is second-order accurate because the true displacement of a constant-curvature arc points along exactly that midpoint direction. What it still gets wrong is the magnitude — the arc's chord is $2R\sin(\Delta\theta/2)$, shorter than the arc $\Delta s$ — and Step 5 sizes that.

**Step 4 — one worked manoeuvre.** Drive a quarter circle of radius $R = 1.000\,\mathrm{m}$ that carries the cart from $(0,0,0°)$ to $(1,1,90°)$, so the body-frame arc is $s = R\,\pi/2 = 1.570796\,\mathrm{m}$. Commanded wheel arcs:

$$\Delta s_R = s\,\frac{R+d}{R} = 1.5708 \times 1.2 = 1.884956\ \mathrm{m}, \qquad \Delta s_L = s\,\frac{R-d}{R} = 1.5708 \times 0.8 = 1.256637\ \mathrm{m}$$

because the outer wheel runs on a circle of radius $R+d$ and the inner on $R-d$ about the same centre. In counts those are $1.884956 \times 2048 = 3860.39$ and $1.256637 \times 2048 = 2573.59$ — and an encoder reports whole counts, so what the odometry actually sees is $\Delta n_R = 3860$, $\Delta n_L = 2573$. Run the algorithm on those integers:

- $\Delta s_R = 3860/2048 = 1.884766\,\mathrm{m}$, $\Delta s_L = 2573/2048 = 1.256348\,\mathrm{m}$;
- $\Delta s = 1.570557\,\mathrm{m}$, short of the commanded $1.570796$ by $0.240\,\mathrm{mm}$;
- $\Delta\theta = 0.628418/0.4 = 1.571045\,\mathrm{rad} = 90.0142°$, over by $0.0142°$;
- reconstructed radius $R' = \Delta s/\Delta\theta = 0.999689\,\mathrm{m}$, giving a final position $(R'\sin\Delta\theta,\ R'(1-\cos\Delta\theta)) = (0.999689,\ 0.999938)\,\mathrm{m}$.

**The whole manoeuvre lands $0.317\,\mathrm{mm}$ from the target**, which is $0.02\,\%$ of the metre travelled, and every bit of it comes from the two truncated counts. That last line is the *exact* constant-curvature integration — the closed form MR's odometry section uses — and it is legitimate here only because the whole manoeuvre genuinely is one arc. Step 3's midpoint rule is the cheap per-tick approximation to it, and Step 5 measures what the approximation costs.

**Step 5 — why the loop runs at $200\,\mathrm{Hz}$ and not once per manoeuvre.** Apply step 3 *once* over the whole $90°$ turn and it reports a displacement of magnitude $\Delta s = 1.5708\,\mathrm{m}$ in the $45°$ direction, when the true chord is $2R\sin 45° = 1.4142\,\mathrm{m}$: an error of $156.6\,\mathrm{mm}$. Split the same turn across the $628$ control ticks the manoeuvre actually takes at $0.5\,\mathrm{m/s}$, so that $\Delta\theta = 2.5\,\mathrm{mrad}$ per tick, and the per-step magnitude error is

$$\Delta s\left(1 - \frac{\sin(\Delta\theta/2)}{\Delta\theta/2}\right) \approx \frac{\Delta s\,\Delta\theta^2}{24} = \frac{0.0025 \times (0.0025)^2}{24} = 6.5 \times 10^{-10}\ \mathrm{m}$$

because $\sin u/u \approx 1 - u^2/6$, so over $628$ ticks the total discretization error is $0.41\ \mu\mathrm{m}$ — six orders of magnitude below the quantization error of Step 4. **The integrator is never the problem at $200\,\mathrm{Hz}$; the encoder and the tyres are.**

**Step 6 — rank the two error sources.** Quantization first. Counts are exact events, so the residual is bounded rather than accumulating: at any instant each wheel's distance is known to within half a count, and the worst-case heading error is

$$\delta\theta = \frac{2 \times \tfrac12 (1/2048)}{2d} = \frac{1/2048}{0.4} = 0.0012207\ \mathrm{rad} = 0.0699°$$

which is also the smallest heading change one count can express. It does not grow — but it *rotates everything that comes after it*, so after another $10\,\mathrm{m}$ of straight driving it has become a $12.2\,\mathrm{mm}$ lateral error. Now slip. Let the right wheel slip $1\,\%$ more than the left over the same quarter turn: $\Delta s_R$ is wrong by $0.01 \times 1.885 = 18.85\,\mathrm{mm}$, so the heading is wrong by $0.01885/0.4 = 0.0471\,\mathrm{rad} = 2.70°$, and over a further $10\,\mathrm{m}$ that is $471\,\mathrm{mm}$.

| source | heading error, one quarter turn | after another $10\,\mathrm{m}$ |
|---|---:|---:|
| encoder quantization | $0.0699°$ | $12.2\ \mathrm{mm}$ |
| $1\,\%$ differential slip | $2.700°$ | $471\ \mathrm{mm}$ |

Slip beats quantization by a factor of $38.6$, so **odometry decay is a tyre budget, not an encoder budget** — buying a finer encoder buys nothing here, and this is the quantitative form of the "fuse with external sensing" claim in §1.

**Step 7 — what the clock does to all of this.** At $0.5\,\mathrm{m/s}$ the cart moves $10\,\mathrm{mm}$ between two vision frames and $35\,\mathrm{mm}$ inside P6's $70\,\mathrm{ms}$ sense-to-act budget, so a goal computed from an image is always at least $35\,\mathrm{mm}$ stale. And a single control tick carries only $0.5/200 \times 2048 = 5.12$ counts, so differencing one tick gives a velocity quantized to $200/2048 = 0.0977\,\mathrm{m/s}$, which is $19.5\,\%$ of the nominal speed. A usable velocity needs a window of ticks or a filter; one tick of an encoder is a position sensor, not a speedometer.

### 1. The chapter in one list

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
  car), the velocity constraints restrict *paths*, not the reachable set. The deep consequence (Brockett): no **continuous** time-invariant feedback can stabilize
  such systems to a point — why practical controllers track *trajectories* instead. Planning
  has the matching consequence: search edges must be drivable curves — Reeds–Shepp shots,
  state lattices, Hybrid A\* ([[04-robotics/planning-decision-making|4. Planning §5.5]]). A base putting P2's origin in front of the panel therefore cannot use a sideways shuffle as a legal edge, and still reaches the pose.
- **Odometry and its decay**: integrating wheel encoders gives pose, but slip and
  quantization make the error grow without bound — the concrete reason mobile robots fuse
  odometry with external sensing via the
  [[02-foundations/probability|Kalman-filter machinery]] (and, at scale, SLAM). The worked section puts numbers on which of the two dominates.
- **Omni/mecanum wheels** buy back the sideways direction at the cost of payload and
  outdoor robustness — why warehouse robots use them and site robots usually don't.

### 2. Odometry, defined

**Odometry** is *dead reckoning from proprioceptive sensors*: an estimate of pose built by integrating measured motion, with no external reference. Three conditions make it what it is, and each one names a failure:

- it integrates **measured** increments, so every measurement error enters the state and stays;
- it uses a **kinematic model** — here the differential drive — so every modelling error (a mis-measured $d$, a worn wheel with the wrong $r$) enters as a systematic bias;
- it has **no absolute reference**, so nothing ever corrects it.

$$\hat q_{k+1} = \hat q_k \oplus f(\Delta n_{R,k}, \Delta n_{L,k})$$

where $\oplus$ is the pose update of Step 3, so the estimate is a running sum and errors compose rather than average out.

- **Example**: the quarter turn of Step 4 — $0.317\,\mathrm{mm}$ of position error out of $1.57\,\mathrm{m}$ from quantization alone, with no external sensor consulted.
- **Non-example**: a wheel-encoder estimate that a GNSS fix has corrected. That is *fusion*, and it is a different object with a different error behaviour: bounded rather than growing ([[04-robotics/state-estimation-slam|State Estimation §8]]).
- **Why it matters**: odometry's error is unbounded *in the long run* and excellent *in the short run*, which is exactly the opposite of a global sensor. Fusion exists because those two profiles are complementary, not because either is bad.

### 3. The instantaneous centre of rotation, defined

The **instantaneous centre of rotation (ICR)** is the *point in the plane* whose velocity is zero at this instant, so the whole body appears to be turning about it. For a rigid planar body moving with body velocity $v$ along $x$ and turn rate $\omega \ne 0$, it lies on the body $y$ axis at signed distance

$$R = \frac{v}{\omega}$$

because a point at distance $R$ to the left of the frame has velocity $v - \omega R$ along body $x$, which vanishes exactly at $R = v/\omega$. For a differential drive it must also lie on the *axle line*, since both wheels roll, and that single geometric fact is the whole of Step 2.

- **Example**: the quarter turn, $R = 1.000\,\mathrm{m}$, ICR one metre to the left of the axle midpoint, outer wheel on a $1.2\,\mathrm{m}$ circle and inner on $0.8\,\mathrm{m}$.
- **Example at the boundary**: $\omega_R = -\omega_L$ gives $v = 0$ and $R = 0$ — the ICR sits at the axle midpoint and the cart spins in place.
- **Non-example**: $\omega_R = \omega_L$. Then $\omega = 0$ and $R$ is undefined, not infinite-and-therefore-fine: there is no point of zero velocity, and the motion is a pure translation. Code that computes $R = v/\omega$ without guarding this divides by zero on the commonest command a cart receives.
- **Why it matters**: every drivable edge a planner may propose for this base is an arc about some ICR on the axle line, which is why a straight C-space segment between two poses is usually not executable ([[04-robotics/modern-robotics/ch10-motion-planning|ch.10]]).

**Wiki connections**: site navigation for inspection robots
([[05-construction-robotics/index|construction]]) runs on exactly this stack: unicycle
kinematics + [[04-robotics/modern-robotics/ch10-motion-planning|kinodynamic planning]] +
fused localization.

### Self-check

1. For the worked diff-drive, what wheel speeds make the robot spin in place at 1 rad/s?
2. Why can't a smooth static feedback stabilize a car to a parking spot, in one sentence?
3. Odometry error grows without bound; GPS error doesn't. What does the fusion of the two
   give you that neither has alone?
4. P6-D reports $\Delta n_R = \Delta n_L = 5$ in one control tick. What are $\Delta s$, $\Delta\theta$, and the implied speed?

> [!tip]- Answers
> 1. Spinning in place means $v = 0$, i.e. $\omega_R = -\omega_L$. Then $\omega = r(2\omega_R)/(2d) = r\omega_R/d = 0.5\,\omega_R = 1$, so $\omega_R = 2$ and $\omega_L = -2$ rad/s.
> 2. Because the system has no sideways velocity, its reachable directions at a point are restricted, and Brockett's condition shows no *continuous* time-invariant feedback can asymptotically stabilize it to an arbitrary pose — continuous, not merely smooth, so no amount of relaxing differentiability rescues it — which is why practical controllers track *trajectories* instead of regulating to a point.
> 3. Short-term precision (odometry, smooth and high-rate but drifting) plus a drift-free absolute reference (GNSS — though on site, multipath and occlusion add bias, not just noise). Kalman fusion takes the strengths of both timescales: locally smooth *and* globally bounded, which neither has alone. See [[04-robotics/state-estimation-slam|State Estimation §8]].
> 4. $\Delta s_R = \Delta s_L = 5/2048 = 2.441\,\mathrm{mm}$, so $\Delta s = 2.441\,\mathrm{mm}$ and $\Delta\theta = 0$ — dead straight. The implied speed is $0.002441/0.005 = 0.488\,\mathrm{m/s}$, and the next admissible readings are $4$ and $6$ counts, i.e. $0.391$ and $0.586\,\mathrm{m/s}$: the quantization is coarser than most speed tolerances, which is Step 7's point.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same cart **P6-D**, same frozen numbers, but the manoeuvre changes: instead of the quarter-circle arc, the cart must **turn in place through exactly $90°$** to face the panel, at $\omega = 0.5\,\mathrm{rad/s}$.

1. **Draw.** The left panel again for this manoeuvre: where the ICR now sits, what the two wheels do, and what the arc of the body-frame origin degenerates to. Add the wheel-track circles and their radii.
2. **Derive.** (a) The wheel arc each wheel must travel, and the exact count it corresponds to. (b) Turning in place forces $\Delta n_R = -\Delta n_L$; show that this makes $\Delta n_R - \Delta n_L$ even, list the two nearest achievable headings and their errors, and give the heading step between consecutive achievable values. (c) Now allow $\Delta n_R \ne -\Delta n_L$: find the count pair that lands nearest $90°$, and say what it costs in translation. (d) How long does the turn take, and how many counts arrive per $5\,\mathrm{ms}$ control tick?
3. **Interpret.** Compare (b)'s heading error with the $2.70°$ that a $1\,\%$ differential slip produced on the arc, and say which of the two a better encoder would fix. Then use (d) to explain why a velocity controller for this turn cannot be tuned on one-tick differences, and name the two standard ways out.

> [!tip]- Solutions
> 1. $v = 0$ and $R = v/\omega = 0$, so the ICR is at the axle midpoint; the body-frame origin does not move and its arc degenerates to a point. The two wheels counter-rotate on the same circle of radius $d = 0.200\,\mathrm{m}$ about that point, one forward and one backward.
> 2. (a) Each wheel travels $d\,\Delta\theta = 0.200 \times 1.570796 = 0.314159\,\mathrm{m}$, which is $0.314159 \times 2048 = 643.398$ counts. (b) With $\Delta n_L = -\Delta n_R$ the difference is $2\Delta n_R$, always even, while the exact requirement is $2d\,\Delta\theta \times 2048 = 1286.796$ counts — odd territory. The two nearest even values are $1286$ ($\Delta n_R = 643$), giving $1286/2048/0.4 = 1.569824\,\mathrm{rad} = 89.9443°$, error $-0.0557°$; and $1288$ ($\Delta n_R = 644$), giving $1.572266\,\mathrm{rad} = 90.0842°$, error $+0.0842°$. Consecutive achievable values are $2$ counts apart, i.e. $2/2048/0.4 = 0.0024414\,\mathrm{rad} = 0.1399°$ — twice the single-count quantum of $0.0699°$, because the symmetry throws away every other value. (c) Break the symmetry: $\Delta n_R = 644$, $\Delta n_L = -643$ gives a difference of $1287$ and a heading of $1.571045\,\mathrm{rad} = 90.0142°$, error $+0.0142°$, four times better. The cost is that $\Delta s = (644-643)/2048/2 = 0.244\,\mathrm{mm}$ of forward translation: the cart no longer turns exactly in place. (d) $\Delta\theta/\omega = 1.5708/0.5 = 3.142\,\mathrm{s}$, i.e. $628$ control ticks, and each wheel covers $d\,\omega\,\Delta t = 0.2 \times 0.5 \times 0.005 = 0.5\,\mathrm{mm}$ per tick, which is $1.024$ counts.
> 3. The turn-in-place heading error is $0.056°$–$0.084°$ against slip's $2.70°$, a factor of roughly $35$: a finer encoder would fix the smaller of the two and leave the larger untouched, so it is the wrong purchase. The tyres, or an external heading reference, are the right one. From (d), one tick carries about one count, so a one-tick velocity estimate is quantized to $\pm 100\,\%$ of the commanded wheel speed — the derivative is pure quantization noise. The two standard ways out are to difference over a longer window (accepting the lag it adds) or to run a state estimator that integrates the counts and models the speed, which is where this page hands off to [[04-robotics/state-estimation-slam|State Estimation §8]].

## 한국어

**핵심 질문**: 바퀴 달린 베이스는 어떻게 움직이고, "옆으로 못 미끄러진다"가 왜 "거기 못 간다"와 다른가?

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**은 직선 위의 카트로, 엔코더가 미터당 $2048$ 카운트이고 시계가 붙어 있다. 비전 $50\,\mathrm{Hz}$, 제어 $200\,\mathrm{Hz}$, 노출 중간부터 힘이 나갈 때까지 $70\,\mathrm{ms}$. 이 페이지는 독립 구동 바퀴 둘을 달아 그것을 평면으로 들어 올린다. 결과를 **P6-D**라 부르고 여기서 고정한다.

| 양 | 값 | 출처 |
|---|---:|---|
| 바퀴당 엔코더 | 바퀴 주행 미터당 $2048$ 카운트 | **P6** |
| 바퀴 1회전당 카운트 | 디코드 후 쿼드러처 $1024$ | 여기서 정의 |
| 바퀴 둘레 | $1024/2048 = 0.500\ \mathrm{m}$ | 위 두 행이 강제 |
| **바퀴 반지름 $r$** | $0.500/2\pi = 1/(4\pi) = 0.079577\ \mathrm{m}$ | 유도; 지름 $159.2\,\mathrm{mm}$ |
| **반축거 $d$** | $0.200\ \mathrm{m}$, 축거는 $0.400\ \mathrm{m}$ | 여기서 정의, §1 계산 예제와 일치 |
| 카운트당 거리 | $1/2048 = 0.48828\ \mathrm{mm}$ | 유도 |
| 제어 주기 | $5\ \mathrm{ms}$ ($200\,\mathrm{Hz}$) | **P6** |
| 비전 주기 | $20\ \mathrm{ms}$ ($50\,\mathrm{Hz}$) | **P6** |
| 감지-작용 예산 | $70\ \mathrm{ms}$ | **P6** |
| 기준 속도 | $0.500\ \mathrm{m/s}$ | 여기서 정의 |

반지름은 자유롭게 고른 값이 아니다. 미터당 $2048$ 카운트를 내야 하는 $1024$ 카운트 바퀴는 한 바퀴에 정확히 $0.5\,\mathrm{m}$를 굴러야 하고, 그것이 $r = 1/(4\pi)$를 못 박는다. 자세는 $(x, y, \theta)$이고 $\theta$는 $+x$에서 잰 방위다.

### 과제가 그릴 그림 · Homework diagram

그림 두 장.

**왼쪽 — 기하.** 카트를 직사각형으로 그리고 바디 좌표계를 차축 중점에 둔다. 바디 $x$가 앞, 바디 $y$가 왼쪽. 차축 위 $\pm d$에 바퀴 둘을 그리고 $d = 0.200\,\mathrm{m}$을 적는다. 차축 직선을 왼쪽으로 연장해 **순간 회전 중심**까지 긋고 그 거리를 $R = v/\omega$로 표시한 뒤, 바디 좌표계가 그 둘레로 따라가는 호를 그린다. 호 위에 바깥 바퀴 자취를 따라 $\Delta s_R$, 안쪽을 따라 $\Delta s_L$을 쓴다. 바디 $y$축에 가위표 친 옆 방향 화살표를 그린다. 그것이 비홀로노믹 제약이고, 카트가 그릴 수 없는 유일한 화살표다.

**오른쪽 — 시계.** 시간축에 눈금 세 줄: $5\,\mathrm{ms}$마다 제어, $20\,\mathrm{ms}$마다 비전, 그리고 카메라 노출 중간 표시에서 힘이 나가는 순간까지 $70\,\mathrm{ms}$짜리 괄호 하나. 괄호 아래에 $0.5\,\mathrm{m/s}$에서 카트가 간 거리를 적는다. $5\,\mathrm{ms}$ 구간 하나 아래에 그 안에 도착하는 카운트 수를 적는다.

과제는 제자리 회전에 대해 왼쪽 그림을 다시 그리라고 하며, 그때 $R = 0$이고 호는 차축 중점으로 주저앉는다.

### 장치로 한 번 끝까지 · Worked on the plant

**1단계 — 구름 제약에서 외바퀴 모델로.** 미끄러지지 않고 구르는 바퀴는 자기 차축 방향 속도가 0이므로 몸체 속도는 바디 $x$ 방향뿐이다. 속력 $v$와 회전율 $\omega$로 세계 좌표에 쓰면:

$$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega$$

바디 $x$축이 각 $\theta$를 향하기 때문이다. 입력 둘, 상태 셋. 이 부족분이 *곧* 비홀로노믹 제약이고, $A(\theta)\dot\theta = 0$ 꼴로 쓰면 $\dot x\sin\theta - \dot y\cos\theta = 0$이다.

**2단계 — 바퀴 둘에서 $(v,\omega)$로.** 각 바퀴의 접지점은 자기 지면 속력 $\dot s_R$, $\dot s_L$로 움직인다. 바디 좌표계 중점은 그 평균이고 회전율은 차이를 축거로 나눈 것이다:

$$v = \frac{\dot s_R + \dot s_L}{2} = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{\dot s_R - \dot s_L}{2d} = \frac{r(\omega_R - \omega_L)}{2d}$$

$\omega$로 도는 강체에서 $2d$ 떨어진 두 점의 속력 차가 정확히 $2d\,\omega$이기 때문이다. 순간 회전 반지름은 $R = v/\omega = d(\dot s_R + \dot s_L)/(\dot s_R - \dot s_L)$로 따라 나온다.

**3단계 — 카운트에서 자세로, 알고리즘으로.** 오도메트리 노드가 카운트 차 $\Delta n_R, \Delta n_L$에 대해 $5\,\mathrm{ms}$마다 도는 것이 이것이다:

1. $\Delta s_R = \Delta n_R/2048$, $\Delta s_L = \Delta n_L/2048$ (미터);
2. $\Delta s = (\Delta s_R + \Delta s_L)/2$, $\Delta\theta = (\Delta s_R - \Delta s_L)/(2d) = (\Delta s_R - \Delta s_L)/0.4$;
3. $x \mathrel{+}= \Delta s\cos(\theta + \Delta\theta/2)$, $y \mathrel{+}= \Delta s\sin(\theta + \Delta\theta/2)$, $\theta \mathrel{+}= \Delta\theta$.

3번은 구간 시작의 방위가 아니라 *중간점* 방위를 쓰는데, 일정 곡률 호의 실제 변위가 정확히 그 중간점 방향을 향하므로 2차 정확도다. 그래도 크기는 틀린다. 호의 현은 $2R\sin(\Delta\theta/2)$로 호 $\Delta s$보다 짧고, 그 크기를 5단계가 잰다.

**4단계 — 기동 하나를 끝까지.** 반지름 $R = 1.000\,\mathrm{m}$의 1/4원을 돌아 카트를 $(0,0,0°)$에서 $(1,1,90°)$로 옮긴다. 바디 좌표계의 호는 $s = R\,\pi/2 = 1.570796\,\mathrm{m}$다. 명령된 바퀴 호는

$$\Delta s_R = s\,\frac{R+d}{R} = 1.5708 \times 1.2 = 1.884956\ \mathrm{m}, \qquad \Delta s_L = s\,\frac{R-d}{R} = 1.5708 \times 0.8 = 1.256637\ \mathrm{m}$$

이다. 바깥 바퀴가 같은 중심에 대해 반지름 $R+d$의 원을, 안쪽이 $R-d$의 원을 달리기 때문이다. 카운트로는 $1.884956 \times 2048 = 3860.39$와 $1.256637 \times 2048 = 2573.59$인데, 엔코더는 정수 카운트만 보고하므로 오도메트리가 실제로 보는 것은 $\Delta n_R = 3860$, $\Delta n_L = 2573$이다. 그 정수로 알고리즘을 돌린다:

- $\Delta s_R = 3860/2048 = 1.884766\,\mathrm{m}$, $\Delta s_L = 2573/2048 = 1.256348\,\mathrm{m}$;
- $\Delta s = 1.570557\,\mathrm{m}$, 명령된 $1.570796$보다 $0.240\,\mathrm{mm}$ 모자란다;
- $\Delta\theta = 0.628418/0.4 = 1.571045\,\mathrm{rad} = 90.0142°$, $0.0142°$ 초과;
- 복원된 반지름 $R' = \Delta s/\Delta\theta = 0.999689\,\mathrm{m}$, 최종 위치 $(R'\sin\Delta\theta,\ R'(1-\cos\Delta\theta)) = (0.999689,\ 0.999938)\,\mathrm{m}$.

**기동 전체가 목표에서 $0.317\,\mathrm{mm}$ 떨어진 곳에 내린다.** 1미터 남짓 이동한 것의 $0.02\,\%$이고, 전부가 잘려 나간 카운트 둘에서 나온다. 마지막 줄은 *정확한* 일정 곡률 적분, 즉 MR의 오도메트리 절이 쓰는 닫힌 형태다. 여기서 그것이 정당한 이유는 기동 전체가 실제로 호 하나이기 때문뿐이다. 3단계의 중간점 규칙은 그것의 값싼 틱 단위 근사이고, 그 근사의 대가를 5단계가 잰다.

**5단계 — 루프가 기동당 한 번이 아니라 $200\,\mathrm{Hz}$로 도는 이유.** 3번을 $90°$ 회전 전체에 *한 번* 적용하면 $45°$ 방향으로 크기 $\Delta s = 1.5708\,\mathrm{m}$의 변위를 보고하는데, 실제 현은 $2R\sin 45° = 1.4142\,\mathrm{m}$다. 오차 $156.6\,\mathrm{mm}$. 같은 회전을 $0.5\,\mathrm{m/s}$에서 실제로 걸리는 $628$개의 제어 틱에 나누면 틱당 $\Delta\theta = 2.5\,\mathrm{mrad}$이고 스텝당 크기 오차는

$$\Delta s\left(1 - \frac{\sin(\Delta\theta/2)}{\Delta\theta/2}\right) \approx \frac{\Delta s\,\Delta\theta^2}{24} = \frac{0.0025 \times (0.0025)^2}{24} = 6.5 \times 10^{-10}\ \mathrm{m}$$

다. $\sin u/u \approx 1 - u^2/6$이기 때문이다. $628$틱을 합쳐도 이산화 오차 총합은 $0.41\ \mu\mathrm{m}$, 4단계의 양자화 오차보다 여섯 자릿수 아래다. **$200\,\mathrm{Hz}$에서 적분기는 결코 문제가 아니다. 문제는 엔코더와 타이어다.**

**6단계 — 두 오차원의 순위.** 양자화부터. 카운트는 정확한 사건이라 잔차가 쌓이지 않고 유계다. 어느 순간에도 각 바퀴의 거리는 반 카운트 이내로 알려져 있고, 최악의 방위 오차는

$$\delta\theta = \frac{2 \times \tfrac12 (1/2048)}{2d} = \frac{1/2048}{0.4} = 0.0012207\ \mathrm{rad} = 0.0699°$$

이며, 이는 카운트 하나가 표현할 수 있는 최소 방위 변화이기도 하다. 자라지는 않는다 — 다만 *그 뒤의 모든 주행을 회전시킨다*. 그래서 직진 $10\,\mathrm{m}$을 더 가면 $12.2\,\mathrm{mm}$의 횡오차가 된다. 이제 미끄럼. 같은 1/4 회전 동안 오른 바퀴가 왼 바퀴보다 $1\,\%$ 더 미끄러지면 $\Delta s_R$이 $0.01 \times 1.885 = 18.85\,\mathrm{mm}$ 틀리므로 방위가 $0.01885/0.4 = 0.0471\,\mathrm{rad} = 2.70°$ 틀리고, $10\,\mathrm{m}$을 더 가면 $471\,\mathrm{mm}$이다.

| 원인 | 1/4 회전 한 번의 방위 오차 | 이후 $10\,\mathrm{m}$ |
|---|---:|---:|
| 엔코더 양자화 | $0.0699°$ | $12.2\ \mathrm{mm}$ |
| $1\,\%$ 차동 미끄럼 | $2.700°$ | $471\ \mathrm{mm}$ |

미끄럼이 양자화를 $38.6$배로 이긴다. 즉 **오도메트리의 붕괴는 엔코더 예산이 아니라 타이어 예산이다.** 더 고해상도 엔코더를 사도 여기서는 아무것도 사지 못하며, 이것이 §1의 "외부 센싱과 융합하라"는 주장의 정량적 형태다.

**7단계 — 시계가 이 모든 것에 하는 일.** $0.5\,\mathrm{m/s}$에서 카트는 비전 프레임 사이에 $10\,\mathrm{mm}$, P6의 $70\,\mathrm{ms}$ 감지-작용 예산 안에서 $35\,\mathrm{mm}$를 간다. 그래서 영상에서 계산된 목표는 언제나 최소 $35\,\mathrm{mm}$ 묵은 것이다. 그리고 제어 틱 하나에는 $0.5/200 \times 2048 = 5.12$ 카운트밖에 오지 않으므로 한 틱을 차분한 속도는 $200/2048 = 0.0977\,\mathrm{m/s}$로 양자화되고, 이는 기준 속도의 $19.5\,\%$다. 쓸 만한 속도에는 여러 틱의 창이나 필터가 필요하다. 엔코더 한 틱은 위치 센서이지 속도계가 아니다.

### 1. 이 장을 목록 하나로

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
  귀결(Brockett): 이런 시스템은 **연속** 시불변 피드백으로 점에 안정화할 수 없다 —
  실전 제어기가 점이 아니라 *궤적*을 추종하는 이유다. 계획 쪽의 짝이 되는 귀결은, 탐색의
  간선이 주행 가능한 곡선이어야 한다는 것이다 — Reeds–Shepp 연결, 상태 격자, Hybrid A\*
  ([[04-robotics/planning-decision-making|4. 계획 §5.5]]). 그래서 P2의 원점을 패널 앞에 두는 베이스도 옆으로 미끄러지는 간선은 쓸 수 없고, 그래도 그 자세에는 도달한다.
- **오도메트리와 그 붕괴**: 바퀴 엔코더 적분으로 자세를 얻지만, 미끄럼과 양자화로 오차가
  무한정 자란다 — 모바일 로봇이 오도메트리를 외부 센싱과
  [[02-foundations/probability|칼만 필터 기계장치]]로 융합하는(그리고 규모가 커지면 SLAM으로
  가는) 구체적 이유다. 둘 중 무엇이 지배하는지는 위의 계산 절이 숫자로 답한다.
- **옴니/메카넘 휠**은 옆 방향을 되사는 대신 적재량과 야외 강건성을 지불한다 — 물류
  로봇은 쓰고 현장 로봇은 잘 안 쓰는 이유.

### 2. 오도메트리의 정의

**오도메트리**는 *고유 감각 센서로 하는 추측 항법*이다. 외부 기준 없이 측정된 운동을 적분해 만든 자세 추정이다. 그것을 그것이게 하는 조건이 셋이고, 하나하나가 실패 방식에 이름을 붙인다:

- **측정된** 증분을 적분하므로 모든 측정 오차가 상태에 들어와 남는다;
- **기구학 모델**을 쓰므로 — 여기서는 차동 구동 — 모든 모형 오차($d$를 잘못 쟀다, 닳은 바퀴의 $r$이 다르다)가 계통 편향으로 들어온다;
- **절대 기준이 없으므로** 아무것도 그것을 교정하지 않는다.

$$\hat q_{k+1} = \hat q_k \oplus f(\Delta n_{R,k}, \Delta n_{L,k})$$

여기서 $\oplus$는 3단계의 자세 갱신이므로 추정은 누적합이고, 오차는 평균으로 상쇄되지 않고 합성된다.

- **예**: 4단계의 1/4 회전 — 외부 센서를 한 번도 보지 않고 $1.57\,\mathrm{m}$ 중 $0.317\,\mathrm{mm}$의 위치 오차가 양자화만으로 나온다.
- **반례**: GNSS 픽스가 교정한 바퀴 엔코더 추정. 그것은 *융합*이고, 오차 거동이 다른 별개의 대상이다. 자라는 것이 아니라 유계다([[04-robotics/state-estimation-slam|상태 추정 §8]]).
- **왜 중요한가**: 오도메트리의 오차는 *장기적으로* 무계이고 *단기적으로* 훌륭하며, 이는 전역 센서와 정확히 반대다. 융합이 존재하는 이유는 어느 한쪽이 나빠서가 아니라 두 프로파일이 상보적이기 때문이다.

### 3. 순간 회전 중심의 정의

**순간 회전 중심**(ICR)은 이 순간 속도가 0인 *평면 위의 점*이라, 몸체 전체가 그 둘레를 도는 것처럼 보인다. 바디 속도 $v$가 $x$ 방향이고 회전율이 $\omega \ne 0$인 평면 강체에서 그것은 바디 $y$축 위 부호 있는 거리

$$R = \frac{v}{\omega}$$

에 있다. 좌표계에서 왼쪽으로 $R$만큼 떨어진 점의 바디 $x$ 방향 속도가 $v - \omega R$이고 그것이 정확히 $R = v/\omega$에서 사라지기 때문이다. 차동 구동에서는 두 바퀴가 모두 구르므로 ICR이 *차축 직선* 위에도 있어야 하고, 이 기하 사실 하나가 2단계의 전부다.

- **예**: 1/4 회전, $R = 1.000\,\mathrm{m}$, ICR은 차축 중점에서 왼쪽으로 1 m, 바깥 바퀴는 $1.2\,\mathrm{m}$ 원, 안쪽은 $0.8\,\mathrm{m}$ 원 위.
- **경계의 예**: $\omega_R = -\omega_L$이면 $v = 0$, $R = 0$. ICR이 차축 중점에 앉고 카트는 제자리에서 돈다.
- **반례**: $\omega_R = \omega_L$. 그러면 $\omega = 0$이고 $R$은 무한대라서 괜찮은 것이 아니라 정의되지 않는다. 속도가 0인 점이 아예 없고 운동은 순수 병진이다. 이것을 막지 않고 $R = v/\omega$를 계산하는 코드는 카트가 가장 흔히 받는 명령에서 0으로 나눈다.
- **왜 중요한가**: 이 베이스에 계획기가 제안할 수 있는 모든 주행 가능 간선은 차축 직선 위 어떤 ICR 둘레의 호다. 두 자세를 잇는 C-space 직선 선분이 대개 실행 불가능한 이유가 그것이다([[04-robotics/modern-robotics/ch10-motion-planning|10장]]).

**위키 연결**: 점검 로봇의 현장 항법([[05-construction-robotics/index|건설]])이 정확히 이
스택 위에서 돈다: 외바퀴 기구학 +
[[04-robotics/modern-robotics/ch10-motion-planning|키노다이나믹 계획]] + 융합 위치 추정.

### 스스로 점검

1. 위의 차동 구동에서 1 rad/s로 제자리 회전하려면 바퀴 속도는?
2. 매끄러운 정적 피드백이 자동차를 주차 지점에 안정화할 수 없는 이유를 한 문장으로.
3. 오도메트리 오차는 무한정 자라고 GPS 오차는 안 자란다. 둘의 융합은 각각이 못 주는
   무엇을 주는가?
4. P6-D가 제어 틱 하나에서 $\Delta n_R = \Delta n_L = 5$를 보고한다. $\Delta s$, $\Delta\theta$, 그리고 함의되는 속력은?

> [!tip]- 정답 · Answers
> 1. $v = 0$이 되도록 $\omega_R = -\omega_L$; $\omega = r\omega_R/d = 1$ ⇒ $\omega_R = 2, \omega_L = -2$ rad/s.
> 2. 옆 방향 속도가 없어 *연속* 시불변 피드백으로는 점 안정화가 불가능하다(Brockett). 매끄러운 것만이 아니라 연속인 것 전체가 안 되므로 미분가능성을 낮춰도 빠져나갈 수 없다 — 그래서 궤적 추종으로 우회한다.
> 3. 단기 정밀(오도메트리 — 부드럽고 빠르지만 드리프트한다)에 드리프트 없는 절대
>    기준(GNSS — 다만 현장에서는 멀티패스와 차폐가 잡음이 아니라 *편향*을 얹는다)을
>    더한다. 칼만 융합은 두 시간 척도의 장점을 각각 취한다: 국소적으로 부드럽고
>    *동시에* 전역적으로 유계 — 어느 쪽도 혼자서는 갖지 못하는 성질이다.
>    [[04-robotics/state-estimation-slam|상태 추정 §8]]을 보라.
> 4. $\Delta s_R = \Delta s_L = 5/2048 = 2.441\,\mathrm{mm}$이므로 $\Delta s = 2.441\,\mathrm{mm}$, $\Delta\theta = 0$. 완전 직진이다. 함의되는 속력은 $0.002441/0.005 = 0.488\,\mathrm{m/s}$이고, 바로 옆에 허용되는 읽기는 $4$와 $6$ 카운트, 즉 $0.391$과 $0.586\,\mathrm{m/s}$다. 양자화가 웬만한 속도 공차보다 거칠고, 그것이 7단계의 요점이다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 카트도 같은 **P6-D**, 고정 숫자도 같지만 기동이 바뀐다. 1/4원 호 대신 카트가 패널을 향하도록 $\omega = 0.5\,\mathrm{rad/s}$로 **제자리에서 정확히 $90°$ 회전**해야 한다.

1. **그리기.** 이 기동에 대해 왼쪽 그림을 다시 그린다. ICR이 이제 어디 있는지, 두 바퀴가 무엇을 하는지, 바디 좌표계 원점의 호가 무엇으로 주저앉는지. 바퀴 자취 원과 그 반지름을 더한다.
2. **유도.** (a) 각 바퀴가 가야 할 호와 그에 해당하는 정확한 카운트. (b) 제자리 회전은 $\Delta n_R = -\Delta n_L$을 강제한다. 그러면 $\Delta n_R - \Delta n_L$이 짝수가 됨을 보이고, 도달 가능한 가장 가까운 방위 둘과 그 오차, 그리고 연속한 도달 가능 값 사이의 방위 간격을 구하라. (c) 이제 $\Delta n_R \ne -\Delta n_L$을 허용한다. $90°$에 가장 가까이 내리는 카운트 쌍을 찾고, 그 대가가 병진으로 얼마인지 말하라. (d) 회전에 걸리는 시간과 $5\,\mathrm{ms}$ 제어 틱마다 도착하는 카운트 수는?
3. **해석.** (b)의 방위 오차를 호에서 $1\,\%$ 차동 미끄럼이 만든 $2.70°$와 비교하고, 더 좋은 엔코더가 둘 중 무엇을 고치는지 말하라. 그다음 (d)를 써서 이 회전의 속도 제어기를 한 틱 차분으로 튜닝할 수 없는 이유를 설명하고, 표준적인 두 가지 출구의 이름을 대라.

> [!tip]- 정답 · Solutions
> 1. $v = 0$, $R = v/\omega = 0$이므로 ICR은 차축 중점이고, 바디 좌표계 원점은 움직이지 않아 그 호가 점으로 주저앉는다. 두 바퀴는 그 점 둘레 반지름 $d = 0.200\,\mathrm{m}$의 같은 원 위에서 하나는 앞으로 하나는 뒤로 반대 방향으로 돈다.
> 2. (a) 각 바퀴는 $d\,\Delta\theta = 0.200 \times 1.570796 = 0.314159\,\mathrm{m}$, 즉 $0.314159 \times 2048 = 643.398$ 카운트를 간다. (b) $\Delta n_L = -\Delta n_R$이면 차가 $2\Delta n_R$이라 항상 짝수인데, 정확한 요구는 $2d\,\Delta\theta \times 2048 = 1286.796$ 카운트로 홀수 쪽이다. 가장 가까운 짝수 둘은 $1286$($\Delta n_R = 643$)로 $1286/2048/0.4 = 1.569824\,\mathrm{rad} = 89.9443°$, 오차 $-0.0557°$이고, $1288$($\Delta n_R = 644$)로 $1.572266\,\mathrm{rad} = 90.0842°$, 오차 $+0.0842°$다. 연속한 도달 가능 값은 $2$ 카운트 간격, 즉 $2/2048/0.4 = 0.0024414\,\mathrm{rad} = 0.1399°$로 한 카운트 양자 $0.0699°$의 두 배다. 대칭이 값을 하나 걸러 버리기 때문이다. (c) 대칭을 깬다. $\Delta n_R = 644$, $\Delta n_L = -643$이면 차가 $1287$, 방위가 $1.571045\,\mathrm{rad} = 90.0142°$, 오차 $+0.0142°$로 네 배 좋다. 대가는 $\Delta s = (644-643)/2048/2 = 0.244\,\mathrm{mm}$의 전진이다. 카트가 더는 정확히 제자리에서 돌지 않는다. (d) $\Delta\theta/\omega = 1.5708/0.5 = 3.142\,\mathrm{s}$, 즉 제어 틱 $628$개이고, 각 바퀴는 틱마다 $d\,\omega\,\Delta t = 0.2 \times 0.5 \times 0.005 = 0.5\,\mathrm{mm}$, 곧 $1.024$ 카운트를 간다.
> 3. 제자리 회전의 방위 오차는 $0.056°$–$0.084°$이고 미끄럼은 $2.70°$라 대략 $35$배다. 더 좋은 엔코더는 둘 중 작은 쪽을 고치고 큰 쪽은 건드리지 못하므로 잘못된 구매다. 옳은 구매는 타이어, 또는 외부 방위 기준이다. (d)에서 한 틱에 대략 카운트 하나가 오므로 한 틱 속도 추정은 명령 바퀴 속도의 $\pm 100\,\%$로 양자화된다. 미분이 순수한 양자화 잡음이다. 표준적인 출구는 둘이다. 더 긴 창으로 차분하거나(그만큼 지연을 받아들인다), 카운트를 적분하며 속력을 모형화하는 상태 추정기를 돌리는 것이다. 후자가 이 페이지가 [[04-robotics/state-estimation-slam|상태 추정 §8]]로 넘기는 지점이다.
