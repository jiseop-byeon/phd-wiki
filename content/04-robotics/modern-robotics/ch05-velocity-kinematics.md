---
title: "MR Ch.05 — Velocity Kinematics & Statics"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.5** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] 시작 전 점검 · Before you start
> You need FK from [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]], partial derivatives and Jacobians ([[02-foundations/calculus-backprop|2. Calculus]]), and what matrix rank means ([[02-foundations/linear-algebra|1. Linear Algebra §2]]).
> [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 FK와 [[02-foundations/calculus-backprop|편미분·야코비안]], 그리고 행렬 랭크의 의미([[02-foundations/linear-algebra|선형대수 §2]])를 알고 있어야 한다.

## English

**Core question**: how do joint velocities map to end-effector velocity — and forces back?

### 1. The Jacobian — with its frame written down

$$\mathcal{V}_s = J_s(\theta)\,\dot\theta \qquad \text{or} \qquad \mathcal{V}_b = J_b(\theta)\,\dot\theta$$

Column $i$ = the end-effector twist produced by unit velocity of joint $i$ alone. The
subscript is part of the object: $J_s$ gives space-frame twists, $J_b$ body-frame twists,
related by $J_s = [\text{Ad}_{T}]\,J_b$ ([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §4]]).
This is the same Jacobian as in [[02-foundations/calculus-backprop|calculus]] — here its
columns happen to be transformed screw axes.

### 2. Worked example — the planar 2R arm's tip Jacobian

For the tip position (planar case, so a 2×2 suffices), differentiate the FK:
$$x = L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2), \qquad y = L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2)$$
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

### 4. Singularities and the manipulability ellipsoid

- Near a singularity, small task-space motions demand huge joint velocities —
  $J^{-1}$ blows up. The 2R example: as $\theta_2 \to 0$, $\det J \to 0$.
- The **manipulability ellipsoid** is the image of the unit ball of joint velocities under
  $J$; its axes are the singular values ([[02-foundations/linear-algebra|SVD]]). Long axis
  = easy direction, short axis = hard; at a singularity one axis collapses to zero.
  The force ellipsoid is its reciprocal twin — directions that are hard to move are easy
  to hold force against, and vice versa.

<svg viewBox="0 0 560 220" style="max-width:100%;height:auto" role="img" aria-label="the 2R arm's manipulability ellipse well away from and close to a singularity">
  <ellipse cx="103.0" cy="92.0" rx="37.5" ry="14.3" transform="rotate(-31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="51.1" ry="3.6" transform="rotate(-80.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;&#8322; = 90&#176; &#8212; well conditioned</text><text x="355" y="26">&#952;&#8322; = 20&#176; &#8212; nearing a singularity</text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; ratio 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; ratio 14</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="20" y="196" opacity="0.9">The ellipse is the set of tip velocities reachable with unit joint speed. As the arm straightens it</text>
    <text x="20" y="211" opacity="0.9">flattens: one direction stays easy, the other needs ever larger joint rates. At 0&#176; it collapses to a line.</text>
  </g>
</svg>



<svg viewBox="0 0 560 220" style="max-width:100%;height:auto" role="img" aria-label="the 2R arm's manipulability ellipse well away from and close to a singularity">
  <ellipse cx="103.0" cy="92.0" rx="39.4" ry="15.1" transform="rotate(-31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="53.7" ry="3.8" transform="rotate(-80.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;&#8322; = 90&#176; &#8212; well conditioned</text><text x="355" y="26">&#952;&#8322; = 20&#176; &#8212; nearing a singularity</text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; ratio 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; ratio 14</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="20" y="196" opacity="0.9">The ellipse is the set of tip velocities reachable with unit joint speed. As the arm straightens</text>
    <text x="20" y="211" opacity="0.9">it flattens: one direction stays easy, the other needs ever larger joint rates. At 0&#176; it is a line.</text>
  </g>
</svg>



**Wiki connections**: teleoperation ([[01-canonical-papers/notes/4-vla/act|ALOHA]]) and
compliant control live on $\tau = J^\top \mathcal{F}$; singularity awareness is why raw
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

### 2. 계산 예제 — 평면 2R 팔의 끝점 야코비안

끝점 위치(평면이므로 2×2면 충분)에 대해 FK를 미분하면:
$$x = L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2), \qquad y = L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2)$$
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

### 4. 특이점과 가조작성 타원체

- 특이점 근처에서는 작은 작업 공간 운동이 거대한 관절 속도를 요구한다 — $J^{-1}$이
  폭발한다. 2R 예제에서 $\theta_2 \to 0$이면 $\det J \to 0$.
- **가조작성 타원체**는 관절 속도 단위 공이 $J$를 통과한 상이고, 그 축들이
  특이값([[02-foundations/linear-algebra|SVD]])이다. 긴 축 = 쉬운 방향, 짧은 축 = 어려운
  방향; 특이점에서는 한 축이 0으로 붕괴한다. 힘 타원체는 그 역수 쌍둥이다 — 움직이기
  어려운 방향일수록 힘을 버티기는 쉽고, 그 반대도 성립한다.

<svg viewBox="0 0 560 220" style="max-width:100%;height:auto" role="img" aria-label="특이점에서 멀 때와 가까울 때의 2R 팔 가조작성 타원">
  <ellipse cx="103.0" cy="92.0" rx="37.5" ry="14.3" transform="rotate(-31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="51.1" ry="3.6" transform="rotate(-80.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;&#8322; = 90&#176; &#8212; 조건이 좋다</text><text x="355" y="26">&#952;&#8322; = 20&#176; &#8212; 특이점에 접근</text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; 비 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; 비 14</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="20" y="196" opacity="0.9">타원은 관절 속도 크기 1로 낼 수 있는 끝점 속도의 집합이다. 팔이 펴질수록 납작해진다:</text>
    <text x="20" y="211" opacity="0.9">한 방향은 계속 쉽고, 다른 방향은 갈수록 큰 관절 속도를 요구한다. 0&#176;에서는 직선으로 붕괴한다.</text>
  </g>
</svg>



**위키 연결**: 원격조작([[01-canonical-papers/notes/4-vla/act|ALOHA]])과 유연 제어가
$\tau = J^\top \mathcal{F}$ 위에 살고, 특이점 인지가 실제 팔에서 VLA 원출력에 안전
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
> 3. 축 방향은 거의 특이 방향이라 거대한 관절 속도가 필요; 수직 방향은 정상 동작.
> 4. 속도는 특이값 $\sigma$배로 증폭되고, 같은 방향의 힘은 $\tau = J^\top \mathcal{F}$에 의해 $1/\sigma$로 스케일되기 때문.
