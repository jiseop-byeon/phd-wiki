---
title: "MR Ch.05 — Velocity Kinematics & Statics"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P2, draw the Jacobian columns, compute τ = JᵀF, run resolved-rate Euler with a live versus frozen J, and say what a near-singularity does to a straight-line task."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.5** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]]. FK from [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]], partial derivatives and Jacobians ([[02-foundations/calculus-backprop|2. Calculus]]), and what matrix rank means ([[02-foundations/linear-algebra|1. Linear Algebra §2]]). How to step a loop: [[02-foundations/lab-kernel|0.65 Lab Kernel]].
> [[02-foundations/lab-plants|0.6]]의 장치 **P2**. [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 FK, [[02-foundations/calculus-backprop|편미분·야코비안]], [[02-foundations/linear-algebra|선형대수 §2]]의 랭크. 루프 전진: [[02-foundations/lab-kernel|0.65]].

## English

**Core question**: how do joint velocities map to end-effector velocity — and forces back?

### 1. The Jacobian — with its frame written down

$$\mathcal{V}_s = J_s(\theta)\,\dot\theta \qquad \text{or} \qquad \mathcal{V}_b = J_b(\theta)\,\dot\theta$$

Column $i$ = the end-effector twist produced by unit velocity of joint $i$ alone. The
subscript is part of the object: $J_s$ gives space-frame twists, $J_b$ body-frame twists,
related by $J_s = [\text{Ad}_{T}]\,J_b$ ([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §4]]).
This is the same Jacobian as in [[02-foundations/calculus-backprop|calculus]] — here its
columns happen to be transformed screw axes.

**Build the idea column by column.** Freeze the current configuration and imagine moving only one joint. Record the instantaneous rigid-body motion of the tool in the declared frame. That response is one Jacobian column. Do the same for each joint; simultaneous joint motion is the weighted sum of those columns because this velocity relationship is linear at the fixed configuration.

The qualification “at the fixed configuration” matters. Once the joints move, their axes and lever arms relative to the tool may change, so the Jacobian must be recomputed. A constant Jacobian can predict a small local displacement but is not generally a finite-motion map. Forward kinematics updates the pose; the Jacobian describes its local sensitivity.

**Check your understanding.** If joint rates have n entries and the chosen task velocity has m entries, J has m rows and n columns. A full rigid-body twist uses the spatial or body Jacobian, while a position-only task may use a different reduced Jacobian. Never remove angular rows blindly without checking which point the remaining linear components describe.

### 2. Worked example — the planar 2R arm's tip Jacobian

For the tip position (planar case, so a 2×2 suffices), differentiate the FK:
$$x = L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2), \qquad y = L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2)$$
Each entry is one partial derivative. The chain rule on the second term of $x$ gives $\partial\cos(\theta_1{+}\theta_2)/\partial\theta_1 = -\sin(\theta_1{+}\theta_2)\cdot 1$, so $\partial x/\partial\theta_1 = -L_1\sin\theta_1 - L_2\sin(\theta_1{+}\theta_2)$, while $\theta_2$ appears only in that term, so $\partial x/\partial\theta_2 = -L_2\sin(\theta_1{+}\theta_2)$. The $y$ row is the same with $\sin \to \cos$. Stacking rows $(x, y)$ against columns $(\theta_1, \theta_2)$:
$$J(\theta) = \begin{pmatrix} -L_1 s_1 - L_2 s_{12} & -L_2 s_{12} \\ L_1 c_1 + L_2 c_{12} & L_2 c_{12} \end{pmatrix}$$
with $s_{12} = \sin(\theta_1{+}\theta_2)$ etc. At $L_1 = L_2 = 1$, $\theta = (0°, 90°)$:
$s_1 = 0, c_1 = 1, s_{12} = 1, c_{12} = 0$, so
$$J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}, \qquad \det J = 1.$$
Full rank — every tip velocity is reachable. In general
$\det J = L_1 L_2 \sin\theta_2$: **the arm is singular exactly when straight or folded**
($\theta_2 = 0°$ or $180°$) — geometrically obvious once the math says where to look.

### 3. Statics duality — derived in three lines

Power must match at both ends of a lossless mechanism. Joint-side power is
$\dot\theta^\top \tau$; end-effector-side power is $\mathcal{V}^\top \mathcal{F}$
(wrench $\mathcal{F}$ = moment + force). Substitute $\mathcal{V} = J\dot\theta$:
$$\dot\theta^\top \tau = (J\dot\theta)^\top \mathcal{F} = \dot\theta^\top J^\top \mathcal{F} \quad \forall \dot\theta \;\;\Longrightarrow\;\; \boxed{\tau = J^\top(\theta)\,\mathcal{F}}$$
The *same* matrix maps velocities out and wrenches back in — gravity compensation, force
control, and contact reasoning all run on this one line. (Frames must match: $J_b$ pairs
with the body wrench $\mathcal{F}_b$, $J_s$ with $\mathcal{F}_s$.)

**Read the equality as an accounting rule.** A wrench does work through the motion it acts on. The Jacobian tells how a joint motion appears at the tool, so the transpose tells how that same tool wrench loads each joint. For each column, ask how strongly the wrench acts along the motion that column produces. That dot product is the corresponding joint effort.

This is different from inverting a velocity equation. No inverse is needed to map a known wrench to joint loads, and the map remains meaningful at a singularity. However, solving backward for an unknown wrench from measured torques may be ambiguous or noise-sensitive. It also requires separating contact loads from gravity, inertia, friction, and other contributions to measured effort.

**Check your understanding.** If a force produces no work along a joint's permitted instantaneous motion, its contribution to that joint's generalized effort is zero. That does not mean the force is absent: the mechanism can carry reaction loads in constrained directions. Match wrench and twist conventions, units, and frames before using the power identity.

### 4. Singularities and the manipulability ellipsoid

- Near a singularity, small task-space motions demand huge joint velocities —
  $J^{-1}$ blows up. The 2R example: as $\theta_2 \to 0$, $\det J \to 0$.
- The **manipulability ellipsoid** is the image of the unit ball of joint velocities under
  $J$; its axes are the singular values ([[02-foundations/linear-algebra|SVD]]). Long axis
  = easy direction, short axis = hard; at a singularity one axis collapses to zero.
  The force ellipsoid is its reciprocal twin — directions that are hard to move are easy
  to hold force against, and vice versa.

<svg viewBox="0 0 560 220" style="max-width:100%;height:auto" role="img" aria-label="the 2R arm's manipulability ellipse well away from and close to a singularity">
  <ellipse cx="103.0" cy="92.0" rx="37.5" ry="14.3" transform="rotate(31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="51.1" ry="3.6" transform="rotate(78.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;&#8322; = 90&#176; &#8212; well conditioned</text><text x="355" y="26">&#952;&#8322; = 20&#176; &#8212; nearing a singularity</text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; ratio 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; ratio 14</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="20" y="196" opacity="0.9">The ellipse is the set of tip velocities reachable with unit joint speed. As the arm straightens it</text>
    <text x="20" y="211" opacity="0.9">flattens: one direction stays easy, the other needs ever larger joint rates. At 0&#176; it collapses to a line.</text>
  </g>
</svg>

**Wiki connections**: force-feedback teleoperation, gravity compensation and
compliant control live on $\tau = J^\top \mathcal{F}$ ([[01-canonical-papers/notes/4-vla/act|ALOHA]] itself mirrors leader joints to follower joints directly); singularity awareness is why raw
VLA outputs pass through safety filters on real arms.

### Self-check

1. Compute $J$ at $\theta = (90°, 90°)$ and its determinant.
2. Derive $\tau = J^\top \mathcal{F}$ again from power conservation without looking.
3. The 2R arm is at $\theta_2 = 5°$. Qualitatively, what happens if the task demands tip
   motion along the arm's axis? Perpendicular to it?
4. Why do the manipulability and force ellipsoids have reciprocal axes?

> [!tip]- Answers
> 1. $s_1 = 1, c_1 = 0, s_{12} = \sin 180° = 0, c_{12} = -1$, so $J = \begin{pmatrix}-1 & 0\\ -1 & -1\end{pmatrix}$ and $\det J = 1$. Still nonsingular — consistent with $\det J = L_1L_2\sin\theta_2 = \sin 90° = 1$.
> 2. Power must match at both ends: $\dot\theta^\top\tau = \mathcal{V}^\top\mathcal{F}$. Substituting $\mathcal{V} = J\dot\theta$ gives $\dot\theta^\top\tau = \dot\theta^\top J^\top\mathcal{F}$ for *all* $\dot\theta$, hence $\tau = J^\top\mathcal{F}$.
> 3. Motion along the arm's own axis is the nearly-singular direction: $\det J = \sin 5° \approx 0.087$, so producing that tip velocity demands roughly an order of magnitude more joint speed than normal — often beyond joint limits. Perpendicular motion is unaffected and behaves normally.
> 4. Velocities are amplified by the singular value $\sigma$ in each principal direction; by $\tau = J^\top\mathcal{F}$ the force transmitted in that same direction scales as $1/\sigma$. Directions that are easy to move are therefore hard to hold force in, and vice versa — the two ellipsoids are reciprocal.

### Problem set · 과제

Tier A. Using **P2** at $\theta=(0^\circ,90^\circ)$ from [[02-foundations/lab-plants|0.6]]. Mass and $\Lambda$ wait until [[02-foundations/manipulator-kinematics-dynamics|10]]; this page is velocity and statics.

1. **Draw.** P2 at the frozen pose: base at the origin, elbow at $(1,0)$, tip at $(1,1)$. Draw Jacobian column 1 as the tip velocity for $\dot\theta=(1,0)$, and column 2 as the tip velocity for $\dot\theta=(0,1)$. Both are arrows at the tip. Write the two arrows as vectors.
2. **Derive.** (a) Confirm $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ from the arrows (or from §2). (b) $J^{-1}$. (c) Joint rates that produce $v=(0,-0.25)\,\mathrm{m/s}$. (d) $\tau=J^\top F$ for $F=(2,-5)\,\mathrm{N}$. (e) Same $F$ at $\theta_2=5^\circ$ is *not* asked as a number — say which joint torque blows up if you instead asked for a tip velocity *along the arm*, and why $J^\top F$ itself does not blow up.
3. **Do.** Resolved-rate: command $v=(0,-0.25)$ for $2\,\mathrm{s}$ from the frozen pose, $T=0.01$, explicit Euler on $\theta$ ([[02-foundations/lab-kernel|0.65]]). Fill `?`. Run twice: recompute $J(\theta)$ every step, then freeze $J$ at the start. Plot tip $x(t),y(t)$. Report final tip and the $x$-drift of the frozen-$J$ run.

```python
# P2 resolved-rate. Fill ?.
import math
T, t1, vy = 0.01, 2.0, -0.25
n = int(round(t1 / T))
th1, th2 = 0.0, math.pi / 2
xs, ys = [], []
freeze = False                       # True on the second run
J0 = None
for k in range(n):
    s1, c1 = math.sin(th1), math.cos(th1)
    s12, c12 = math.sin(th1 + th2), math.cos(th1 + th2)
    J = ((?, ?), (?, ?))             # ((-s1-s12, -s12), (c1+c12, c12))
    if freeze:
        if J0 is None:
            J0 = J
        J = J0
    det = J[0][0]*J[1][1] - J[0][1]*J[1][0]
    # inverse of 2x2, then thdot = Jinv @ [0, vy]
    th1d, th2d = ?, ?
    th1, th2 = th1 + T*th1d, th2 + T*th2d
    xs.append(c1 + math.cos(th1 + th2))
    ys.append(math.sin(th1) + math.sin(th1 + th2))
# plot xs, ys; caption "P2, explicit Euler on theta, T=0.01"
```

> [!tip]- Solutions
> 1. Shoulder-only: the tip is at lever arm $\sqrt{2}$ from the base, velocity perpendicular to $(1,1)$, i.e. parallel to $(-1,1)$. Unit $\dot\theta_1$ gives $|v|=L_\text{tip}=\sqrt{2}$, so column 1 $=(-1,1)$. Elbow-only: forearm is along $+y$ from $(1,0)$ to $(1,1)$, unit $\dot\theta_2$ gives $v$ perpendicular to the forearm, column 2 $=(-1,0)$.
> 2. (a) Columns of $J$ are those arrows. (b) $\det J=1$, $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. (c) $\dot\theta=J^{-1}(0,-0.25)=(-0.25,\ 0.25)\,\mathrm{rad/s}$. (d) $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$, $\tau=J^\top(2,-5)=(-7,-2)\,\mathrm{N{\cdot}m}$. (e) Along-the-arm velocity hits the lost singular direction; $\dot\theta\sim 1/\sigma_\min$ blows up. $J^\top F$ is a static map and stays finite — the structure carries the force, the motors need not.
> 3. $J$ blanks: `((-s1-s12, -s12), (c1+c12, c12))`. Inverse: `th1d = (J[1][1]*0 - J[0][1]*vy)/det`, `th2d = (-J[1][0]*0 + J[0][0]*vy)/det`. Live $J$: tip ends at $\approx(1.00,\ 0.50)$, $x$-drift $<1\,\mathrm{mm}$ (commanded $\Delta y=-0.50$). Frozen $J$: tip ends at $\approx(0.88,\ 0.52)$ — a centimetre-scale $x$ error on a half-metre task, from using a local map as a finite-motion map.

## 한국어

**핵심 질문**: 관절 속도는 말단 속도로, 힘은 그 반대로 어떻게 사상되는가?

### 1. 야코비안 — 프레임을 명시해서

$$\mathcal{V}_s = J_s(\theta)\,\dot\theta \qquad \text{또는} \qquad \mathcal{V}_b = J_b(\theta)\,\dot\theta$$

$i$번째 열 = 관절 $i$만 단위 속도로 움직일 때의 말단 twist. 아래 첨자는 대상의 일부다:
$J_s$는 space 프레임 twist를, $J_b$는 body 프레임 twist를 주고, 둘은
$J_s = [\text{Ad}_{T}]\,J_b$로 연결된다
([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §4]]).
[[02-foundations/calculus-backprop|미적분]]의 야코비안과 같은 대상이며 — 여기서는 그
열들이 변환된 스크류 축일 뿐이다.

**열 하나씩 개념을 만든다.** 현재 구성을 고정하고 관절 하나만 움직인다고 상상한다. 선언한 프레임에서 도구의 순간 강체 운동을 기록하면 야코비안의 열 하나다. 관절마다 반복한다. 고정 구성의 속도 관계는 선형이므로 여러 관절의 동시 운동은 열들의 가중합이다.

“고정 구성에서”가 중요하다. 관절이 움직이면 도구에 대한 축과 지레팔이 달라질 수 있어 야코비안을 다시 계산한다. 상수 야코비안은 작은 국소 변위를 예측하지만 일반적인 유한 운동 사상은 아니다. 순기구학은 자세를 갱신하고 야코비안은 국소 민감도를 말한다.

**이해 확인.** 관절 속도가 n성분이고 과제 속도가 m성분이면 J는 m행 n열이다. 전체 강체 트위스트에는 공간·바디 야코비안을 쓰고 위치만의 과제에는 다른 축소 야코비안을 쓸 수 있다. 남은 선형 성분이 어느 점을 설명하는지 확인하지 않고 각속도 행만 지우면 안 된다.

### 2. 계산 예제 — 평면 2R 팔의 끝점 야코비안

끝점 위치(평면이므로 2×2면 충분)에 대해 FK를 미분하면:
$$x = L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2), \qquad y = L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2)$$
각 성분은 편미분 하나다. $x$의 둘째 항에 연쇄법칙을 쓰면 $\partial\cos(\theta_1{+}\theta_2)/\partial\theta_1 = -\sin(\theta_1{+}\theta_2)\cdot 1$이므로 $\partial x/\partial\theta_1 = -L_1\sin\theta_1 - L_2\sin(\theta_1{+}\theta_2)$이고, $\theta_2$는 그 항에만 나오므로 $\partial x/\partial\theta_2 = -L_2\sin(\theta_1{+}\theta_2)$다. $y$ 행은 $\sin \to \cos$로 바꾼 같은 계산이다. 행 $(x, y)$, 열 $(\theta_1, \theta_2)$로 쌓으면:
$$J(\theta) = \begin{pmatrix} -L_1 s_1 - L_2 s_{12} & -L_2 s_{12} \\ L_1 c_1 + L_2 c_{12} & L_2 c_{12} \end{pmatrix}$$
($s_{12} = \sin(\theta_1{+}\theta_2)$ 등). $L_1 = L_2 = 1$, $\theta = (0°, 90°)$에서:
$s_1 = 0, c_1 = 1, s_{12} = 1, c_{12} = 0$이므로
$$J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}, \qquad \det J = 1.$$
풀랭크 — 모든 끝점 속도가 도달 가능하다. 일반적으로
$\det J = L_1 L_2 \sin\theta_2$: **팔이 완전히 뻗거나 접힐 때가 정확히 특이점이다**
($\theta_2 = 0°$ 또는 $180°$) — 수학이 어디를 보라고 알려주면 기하적으로도 자명해진다.

### 3. 정역학 쌍대성 — 세 줄 유도

손실 없는 기구의 양 끝에서 일률은 같아야 한다. 관절 쪽 일률은 $\dot\theta^\top \tau$,
말단 쪽 일률은 $\mathcal{V}^\top \mathcal{F}$(렌치 $\mathcal{F}$ = 모멘트 + 힘).
$\mathcal{V} = J\dot\theta$를 대입하면:
$$\dot\theta^\top \tau = (J\dot\theta)^\top \mathcal{F} = \dot\theta^\top J^\top \mathcal{F} \quad \forall \dot\theta \;\;\Longrightarrow\;\; \boxed{\tau = J^\top(\theta)\,\mathcal{F}}$$
*같은* 행렬이 속도를 내보내고 렌치를 되받는다 — 중력 보상, 힘 제어, 접촉 추론이 전부 이
한 줄 위에서 돈다. (프레임은 맞춰야 한다: $J_b$는 body 렌치 $\mathcal{F}_b$와, $J_s$는
$\mathcal{F}_s$와 짝이다.)

**등식을 일률의 회계 규칙으로 읽는다.** 렌치는 작용하는 운동을 통해 일을 한다. 야코비안이 관절 운동이 도구에서 어떻게 보이는지 알려 주므로 전치는 도구 렌치가 각 관절에 주는 부하를 알려 준다. 열마다 그 열이 만드는 운동에 렌치가 얼마나 작용하는지 묻는다. 그 내적이 해당 관절의 노력이다.

속도 식을 역으로 푸는 것과 다르다. 알려진 렌치를 관절 부하로 바꾸는 데 역행렬은 필요 없고 특이점에서도 뜻이 있다. 반면 측정 토크에서 모르는 렌치를 찾는 역문제는 모호하거나 잡음에 민감할 수 있다. 측정 노력에서 중력, 관성, 마찰 등도 분리해야 한다.

**이해 확인.** 힘이 관절의 허용된 순간 운동을 따라 일을 하지 않으면 그 관절의 일반화 힘 기여는 0이다. 힘이 없다는 뜻은 아니다. 기구는 구속 방향의 반력을 지탱할 수 있다. 일률 등식을 쓰기 전에 렌치·트위스트의 표기, 단위, 프레임을 맞춘다.

### 4. 특이점과 가조작성 타원체

- 특이점 근처에서는 작은 말단 운동이 거대한 관절 속도를 요구한다 — $J^{-1}$이
  폭발한다. 2R 예제에서 $\theta_2 \to 0$이면 $\det J \to 0$.
- **가조작성 타원체**는 관절 속도 단위 공이 $J$를 통과한 상이고, 그 축들이
  특이값([[02-foundations/linear-algebra|SVD]])이다. 긴 축 = 쉬운 방향, 짧은 축 = 어려운
  방향; 특이점에서는 한 축이 0으로 붕괴한다. 힘 타원체는 그 역수 쌍둥이다 — 움직이기
  어려운 방향일수록 힘을 버티기는 쉽고, 그 반대도 성립한다.

<svg viewBox="0 0 560 220" style="max-width:100%;height:auto" role="img" aria-label="특이점에서 멀 때와 가까울 때의 2R 팔 가조작성 타원">
  <ellipse cx="103.0" cy="92.0" rx="37.5" ry="14.3" transform="rotate(31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="51.1" ry="3.6" transform="rotate(78.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;&#8322; = 90&#176; &#8212; 조건이 좋다</text><text x="355" y="26">&#952;&#8322; = 20&#176; &#8212; 특이점에 접근</text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; 비 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; 비 14</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="20" y="196" opacity="0.9">타원은 관절 속도 크기 1로 낼 수 있는 끝점 속도의 집합이다. 팔이 펴질수록 납작해진다:</text>
    <text x="20" y="211" opacity="0.9">한 방향은 계속 쉽고, 다른 방향은 갈수록 큰 관절 속도를 요구한다. 0&#176;에서는 직선으로 붕괴한다.</text>
  </g>
</svg>



**위키 연결**: 힘 피드백 원격조작, 중력 보상, 유연 제어가
$\tau = J^\top \mathcal{F}$ 위에 살고([[01-canonical-papers/notes/4-vla/act|ALOHA]] 자체는 리더 관절을 팔로워 관절로 곧바로 옮긴다), 특이점 인지가 실제 팔에서 VLA 원출력에 안전
필터를 거는 이유다.

### 스스로 점검

1. $\theta = (90°, 90°)$에서 $J$와 행렬식을 계산하라.
2. 일률 보존에서 $\tau = J^\top \mathcal{F}$를 안 보고 다시 유도하라.
3. 2R 팔이 $\theta_2 = 5°$에 있다. 팔의 축 방향으로 끝점을 움직이라는 과제가 오면
   정성적으로 무슨 일이 일어나는가? 수직 방향이면?
4. 가조작성 타원체와 힘 타원체의 축이 서로 역수인 이유는?

> [!tip]- 정답 · Answers
> 1. $s_1 = 1, c_1 = 0, s_{12} = 0, c_{12} = -1$ → $J = \begin{pmatrix} -1 & 0 \\ -1 & -1 \end{pmatrix}$, $\det J = 1$.
> 2. $\dot\theta^\top \tau = \mathcal{V}^\top \mathcal{F}$에 $\mathcal{V} = J\dot\theta$ 대입, 모든 $\dot\theta$에 대해 성립 ⇒ $\tau = J^\top \mathcal{F}$.
> 3. 팔 자신의 축 방향이 거의 특이 방향이다: $\det J = \sin 5° \approx 0.087$, 최소 특이값 ≈ 0.04라 정상 자세보다 한 자릿수 이상 큰 관절 속도가 필요하고 관절 한계를 넘기 쉽다. 수직 방향은 정상 동작.
> 4. 속도는 특이값 $\sigma$배로 증폭되고, 같은 방향의 힘은 $\tau = J^\top \mathcal{F}$에 의해 $1/\sigma$로 스케일되기 때문.

### 과제 · Problem set

Tier A. [[02-foundations/lab-plants|0.6]]의 **P2**, $\theta=(0^\circ,90^\circ)$. 질량과 $\Lambda$는 [[02-foundations/manipulator-kinematics-dynamics|10]]까지 기다려라. 이 페이지는 속도와 정역학이다.

1. **그리기.** 고정 자세의 P2: 베이스 원점, 엘보 $(1,0)$, 말단 $(1,1)$. $\dot\theta=(1,0)$의 말단 속도(열 1)와 $\dot\theta=(0,1)$의 말단 속도(열 2)를 말단에서 화살표로 그려라. 두 벡터를 써라.
2. **유도.** (a) 화살표(또는 §2)에서 $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$. (b) $J^{-1}$. (c) $v=(0,-0.25)\,\mathrm{m/s}$를 만드는 관절 속도. (d) $F=(2,-5)\,\mathrm{N}$의 $\tau=J^\top F$. (e) $\theta_2=5^\circ$에서 같은 $F$의 숫자를 묻지 않는다. 대신 *팔을 따른* 말단 속도를 시키면 어느 관절 속도가 터지는지, 그리고 왜 $J^\top F$ 자체는 터지지 않는지.
3. **실행.** 영어 템플릿. $v=(0,-0.25)$를 $2\,\mathrm{s}$, $T=0.01$, $\theta$에 명시적 오일러. $J(\theta)$를 매 스텝 재계산한 런과 시작 $J$를 고정한 런. 말단 $x(t),y(t)$를 그리고 최종 말단과 고정-$J$의 $x$ 드리프트를 보고하라.

> [!tip]- 정답 · Solutions
> 1. 어깨만: 말단이 베이스에서 지렛대 $\sqrt{2}$, 속도는 $(1,1)$에 수직 즉 $(-1,1)$ 방향. 단위 $\dot\theta_1$의 $|v|=\sqrt{2}$이므로 열 1 $=(-1,1)$. 엘보만: 전완이 $(1,0)\to(1,1)$의 $+y$, 단위 $\dot\theta_2$는 전완에 수직, 열 2 $=(-1,0)$.
> 2. (a) $J$의 열이 그 화살표. (b) $\det J=1$, $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. (c) $\dot\theta=(-0.25,\ 0.25)\,\mathrm{rad/s}$. (d) $\tau=(-7,-2)\,\mathrm{N{\cdot}m}$. (e) 팔 방향 속도는 잃어버린 특이 방향이라 $\dot\theta\sim 1/\sigma_\min$이 터진다. $J^\top F$는 정역학 사상이라 유한 — 구조가 힘을 지고 모터는 안 져도 된다.
> 3. 빈칸은 영어 해. 산 $J$: 말단 $\approx(1.00,\ 0.50)$, $x$ 드리프트 $<1\,\mathrm{mm}$. 고정 $J$: $\approx(0.88,\ 0.52)$ — 0.5 m 과제에서 센티미터급 $x$ 오차. 국소 사상을 유한 운동 사상으로 쓴 대가.
