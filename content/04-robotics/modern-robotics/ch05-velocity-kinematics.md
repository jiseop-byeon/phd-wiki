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
> Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]]. FK from [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]]; twists and the adjoint from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3–4]] and the wrench from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §6]]; partial derivatives and Jacobians ([[02-foundations/calculus-backprop|2. Calculus]]), and what matrix rank means ([[02-foundations/linear-algebra|1. Linear Algebra §2]]). How to step a loop: [[02-foundations/lab-kernel|0.7 Lab Kernel]].
> [[02-foundations/lab-plants|0.6]]의 장치 **P2**. [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 FK, [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3–4]]의 twist와 adjoint, [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §6]]의 렌치, [[02-foundations/calculus-backprop|편미분·야코비안]], [[02-foundations/linear-algebra|선형대수 §2]]의 랭크. 루프 전진: [[02-foundations/lab-kernel|0.7]].

## English

**Core question**: how do joint velocities map to end-effector velocity — and forces back?

> [!note] First pass · 처음이라면
> Read the picture and §1's opening definition (column $i$ is the tool's motion when joint $i$ alone turns), then §2 through the two arrows at the tip and the resolved-rate run — the Jacobian as two velocity arrows and why it must be recomputed — and §3's three-line derivation of $\tau = J^\top\mathcal{F}$ with its P2 number. The rest of §1's frame bookkeeping, the six-vector check and the accounting paragraphs after §3's derivation, and §4's ellipsoids are second pass; the six-vector check needs the wrench of ch.3 §6.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 306" style="max-width:100%;height:auto" role="img" aria-label="P2 at the catalog pose with, at the tip, the two Jacobian columns (−1, 1) and (−1, 0) m/s, the commanded velocity (0, −0.25) m/s, the manipulability ellipse with semi-axes 1.618 and 0.618, and the outlined force (0, −10) N pointing into the tip.">
  <defs><marker id="mr05hdE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker><marker id="mr05hdvE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <path d="M78 34 L74.3 34.1 L70.7 34.3 L67.3 34.6 L64 35.1 L60.9 35.6 L57.9 36.4 L55.1 37.2 L52.4 38.2 L49.9 39.3 L47.6 40.5 L45.4 41.9 L43.4 43.3 L41.6 44.9 L39.9 46.6 L38.5 48.5 L37.2 50.4 L36.1 52.5 L35.1 54.6 L34.4 56.9 L33.8 59.3 L33.5 61.7 L33.3 64.3 L33.3 67 L33.5 69.7 L33.8 72.6 L34.4 75.5 L35.1 78.5 L36.1 81.6 L37.2 84.8 L38.5 88 L39.9 91.3 L41.6 94.7 L43.4 98.1 L45.4 101.5 L47.6 105.1 L49.9 108.6 L52.4 112.2 L55.1 115.9 L57.9 119.5 L60.9 123.2 L64 127 L67.3 130.7 L70.7 134.5 L74.3 138.2 L78 142 L81.8 145.8 L85.8 149.5 L89.9 153.3 L94.1 157 L98.4 160.8 L102.8 164.5 L107.3 168.1 L112 171.8 L116.7 175.4 L121.5 178.9 L126.3 182.5 L131.3 185.9 L136.3 189.3 L141.3 192.7 L146.5 196 L151.6 199.2 L156.9 202.4 L162.1 205.5 L167.4 208.5 L172.7 211.4 L178 214.3 L183.3 217 L188.7 219.7 L194 222.3 L199.3 224.7 L204.6 227.1 L209.9 229.4 L215.1 231.5 L220.4 233.6 L225.5 235.5 L230.7 237.4 L235.7 239.1 L240.7 240.7 L245.7 242.1 L250.5 243.5 L255.3 244.7 L260 245.8 L264.7 246.8 L269.2 247.6 L273.6 248.4 L277.9 248.9 L282.1 249.4 L286.2 249.7 L290.2 249.9 L294 250 L297.7 249.9 L301.3 249.7 L304.7 249.4 L308 248.9 L311.1 248.4 L314.1 247.6 L316.9 246.8 L319.6 245.8 L322.1 244.7 L324.4 243.5 L326.6 242.1 L328.6 240.7 L330.4 239.1 L332.1 237.4 L333.5 235.5 L334.8 233.6 L335.9 231.5 L336.9 229.4 L337.6 227.1 L338.2 224.7 L338.5 222.3 L338.7 219.7 L338.7 217 L338.5 214.3 L338.2 211.4 L337.6 208.5 L336.9 205.5 L335.9 202.4 L334.8 199.2 L333.5 196 L332.1 192.7 L330.4 189.3 L328.6 185.9 L326.6 182.5 L324.4 178.9 L322.1 175.4 L319.6 171.8 L316.9 168.1 L314.1 164.5 L311.1 160.8 L308 157 L304.7 153.3 L301.3 149.5 L297.7 145.8 L294 142 L290.2 138.2 L286.2 134.5 L282.1 130.7 L277.9 127 L273.6 123.2 L269.2 119.5 L264.7 115.9 L260 112.2 L255.3 108.6 L250.5 105.1 L245.7 101.5 L240.7 98.1 L235.7 94.7 L230.7 91.3 L225.5 88 L220.4 84.8 L215.1 81.6 L209.9 78.5 L204.6 75.5 L199.3 72.6 L194 69.7 L188.7 67 L183.3 64.3 L178 61.7 L172.7 59.3 L167.4 56.9 L162.1 54.6 L156.9 52.5 L151.6 50.4 L146.5 48.5 L141.3 46.6 L136.3 44.9 L131.3 43.3 L126.3 41.9 L121.5 40.5 L116.7 39.3 L112 38.2 L107.3 37.2 L102.8 36.4 L98.4 35.6 L94.1 35.1 L89.9 34.6 L85.8 34.3 L81.8 34.1 Z" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="2 3" opacity="0.75"><line x1="186" y1="142" x2="37.4" y2="50.1"/><line x1="186" y1="142" x2="221.1" y2="85.2"/></g>
  <polyline points="78,250 186,250 186,142" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.3"/>
  <circle cx="78" cy="250" r="4.5" fill="currentColor" fill-opacity="0.6"/>
  <circle cx="186" cy="250" r="3.5" fill="currentColor" fill-opacity="0.6"/>
  <path d="M183 34 L189 34 L189 124 L193.5 124 L186 137 L178.5 124 L183 124 Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <g stroke="currentColor" stroke-width="2.4" marker-end="url(#mr05hdE)"><line x1="186" y1="142" x2="78" y2="34"/><line x1="186" y1="142" x2="78" y2="142"/></g>
  <line x1="186" y1="142" x2="186" y2="169" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr05hdvE)"/>
  <circle cx="186" cy="142" r="4" fill="currentColor"/>
  <line x1="350" y1="14" x2="350" y2="270" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="78" y="25" text-anchor="middle">col 1 = (−1, 1)</text>
    <text x="142" y="158" text-anchor="middle">col 2 = (−1, 0)</text>
    <text x="196" y="169">v = (0, −0.25)</text>
    <text x="196" y="184">θ̇ = (−0.25, 0.25) rad/s</text>
    <text x="198" y="43">F = (0, −10) N</text>
    <text x="198" y="58">τ = Jᵀ F = (−10, 0) N·m</text>
    <text x="24.4" y="44.1" text-anchor="middle">σ<tspan dy="3.5">1</tspan></text>
    <text x="227.1" y="77.2">σ<tspan dy="3.5">2</tspan></text>
    <text x="78" y="267" text-anchor="middle" opacity="0.8">base (0, 0)</text>
    <text x="186" y="267" text-anchor="middle" opacity="0.8">elbow (1, 0)</text>
    <text x="196" y="150" opacity="0.8">tip (1, 1)</text>
    <text x="362" y="26" font-size="12">Velocities out of the tip</text>
    <text x="368" y="45">col 1 = (−1, 1) m/s, θ̇ = (1, 0)</text>
    <text x="368" y="62">col 1 ⟂ base–tip line, length √2</text>
    <text x="368" y="79">col 2 = (−1, 0) m/s, θ̇ = (0, 1)</text>
    <text x="368" y="102">v = (0, −0.25) m/s (thin)</text>
    <text x="368" y="119">θ̇ = J⁻¹v = (−0.25, 0.25) rad/s</text>
    <text x="362" y="146" font-size="12">Ellipse = J · (unit circle)</text>
    <text x="368" y="165">σ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 1.618 (long, easy)</tspan></text>
    <text x="368" y="182">σ<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= 0.618, ratio 2.6</tspan></text>
    <text x="362" y="209" font-size="12">Force into the tip (outlined)</text>
    <text x="368" y="228">F = (0, −10) N</text>
    <text x="368" y="245">τ = Jᵀ F = (−10, 0) N·m</text>
    <text x="12" y="296" opacity="0.85">Arrows out of the tip are velocities (1 m/s drawn as 1 m); the outlined arrow into the tip is a force.</text>
  </g>
</svg>

Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at the catalog pose $\theta = (0^\circ, 90^\circ)$, drawn to scale with everything anchored at the tip $(1,1)$: the Jacobian columns $(-1,1)$ and $(-1,0)\,\mathrm{m/s}$, the tip velocities when only the shoulder or only the elbow turns at $1\,\mathrm{rad/s}$; the thin commanded velocity $v = (0,-0.25)\,\mathrm{m/s}$, which needs $\dot\theta = J^{-1}v = (-0.25,\ 0.25)\,\mathrm{rad/s}$; and the manipulability ellipse, the image of the unit circle of joint rates, with semi-axes $1.618$ and $0.618$. The outlined arrow is a force into the tip, $F = (0,-10)\,\mathrm{N}$, which the same $J$ maps back to $\tau = J^\top F = (-10,\ 0)\,\mathrm{N{\cdot}m}$ — arrows out of the tip are velocities, the arrow into it is a force.

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

**Those two columns are arrows at the tip.** Shoulder-only, $\dot\theta=(1,0)$: the tip sits at lever arm $\sqrt{2}$ from the base, velocity perpendicular to $(1,1)$, so column 1 $=(-1,1)$. Elbow-only, $\dot\theta=(0,1)$: the forearm is along $+y$, velocity perpendicular to it, so column 2 $=(-1,0)$. Stacking them recovers $J$. Inverse: $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. Command $v=(0,-0.25)\,\mathrm{m/s}$ at this pose:

$$\dot\theta=J^{-1}v=(-0.25,\ 0.25)\,\mathrm{rad/s}.$$

**Worked: resolved-rate Euler.** Same command for $2\,\mathrm{s}$, $T=0.01$, explicit Euler on $\theta$ ([[02-foundations/lab-kernel|0.7]]). Recompute $J(\theta)$ every step: the tip ends at $\approx(0.999,\ 0.500)$, $x$-drift $<1\,\mathrm{mm}$ on a commanded $\Delta y=-0.50\,\mathrm{m}$. Freeze $J$ at the start: the tip ends at $\approx(0.878,\ 0.521)$ — twelve centimetres of $x$ error. A constant Jacobian is a local map, not a finite-motion map. The problem set fills this loop; changing $T$ is the knob.

### 3. Statics duality — derived in three lines

Power must match at both ends of a lossless mechanism. Joint-side power is
$\dot\theta^\top \tau$; end-effector-side power is $\mathcal{V}^\top \mathcal{F}$, where the
wrench $\mathcal{F} = (m, f) \in \mathbb{R}^6$ stacks the moment and the force the tool applies, and its pairing with a twist, $\mathcal{V}^\top\mathcal{F} = \omega\cdot m + v\cdot f$, is a power in watts (defined with its frame rule in [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §6]]). Substitute $\mathcal{V} = J\dot\theta$:
$$\dot\theta^\top \tau = (J\dot\theta)^\top \mathcal{F} = \dot\theta^\top J^\top \mathcal{F} \quad \forall \dot\theta \;\;\Longrightarrow\;\; \boxed{\tau = J^\top(\theta)\,\mathcal{F}}$$
The *same* matrix maps velocities out and wrenches back in — gravity compensation, force
control, and contact reasoning all run on this one line. (Frames must match: $J_b$ pairs
with the body wrench $\mathcal{F}_b$, $J_s$ with $\mathcal{F}_s$.) On catalog P2, $F=(0,-10)\,\mathrm{N}$ (down on the panel) gives $\tau=J^\top F=(-10,0)\,\mathrm{N{\cdot}m}$: the shoulder carries the load, the elbow does not. The problem set uses a different $F$.

**The same number from the full six-vectors.** As a space wrench this force is $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$, its moment $p\times f$ taken about the base, and at this pose the space Jacobian's columns are the screws $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$ and $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$, since $\theta_1 = 0$ leaves $\mathcal{S}_2$ where it was at home. So $J_s^\top\mathcal{F}_s = (-10,\ 0)$ again, and [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §6]] repeats the check in the body frame. The $2\times2$ shortcut is exact because pairing the tip force with the tip velocity gives the same power as pairing the space wrench with the space twist.

**Read the equality as an accounting rule.** A wrench does work through the motion it acts on. The Jacobian tells how a joint motion appears at the tool, so the transpose tells how that same tool wrench loads each joint. For each column, ask how strongly the wrench acts along the motion that column produces. That dot product is the corresponding joint effort.

This is different from inverting a velocity equation. No inverse is needed to map a known wrench to joint loads, and the map remains meaningful at a singularity. However, solving backward for an unknown wrench from measured torques may be ambiguous or noise-sensitive. In numbers: at $\theta = (0^\circ, 5^\circ)$ the smallest singular value of $J$ is $0.039$, and its force direction, $(0.999,\ 0.052)$, lies almost exactly along the arm. A $10\,\mathrm{N}$ push that way produces a joint-torque vector of norm only $0.39\,\mathrm{N\,m}$, so a $0.1\,\mathrm{N\,m}$ error in the measured torques can hide up to $0.1/0.039 = 2.6\,\mathrm{N}$ of force along the arm, against $0.1/0.618 = 0.16\,\mathrm{N}$ at the catalog pose. It also requires separating contact loads from gravity, inertia, friction, and other contributions to measured effort.

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
    <text x="115" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90&#176; &#8212; well conditioned</tspan></text><text x="355" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 20&#176; &#8212; nearing a singularity</tspan></text>
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
> 3. Motion along the arm's own axis is the nearly-singular direction: $\det J = \sin 5° \approx 0.087$ and the smallest singular value is $\approx 0.04$, so producing that tip velocity demands roughly an order of magnitude more joint speed than normal — often beyond joint limits. Perpendicular motion is unaffected and behaves normally.
> 4. Velocities are amplified by the singular value $\sigma$ in each principal direction; by $\tau = J^\top\mathcal{F}$ the force transmitted in that same direction scales as $1/\sigma$. Directions that are easy to move are therefore hard to hold force in, and vice versa — the two ellipsoids are reciprocal.

### Problem set · 과제

Tier A. Using **P2** at $\theta=(0^\circ,90^\circ)$ from [[02-foundations/lab-plants|0.6]]. Mass and $\Lambda$ wait until [[02-foundations/manipulator-kinematics-dynamics|10]]; this page is velocity and statics.

1. **Draw.** P2 at the frozen pose: base at the origin, elbow at $(1,0)$, tip at $(1,1)$. Draw Jacobian column 1 as the tip velocity for $\dot\theta=(1,0)$, and column 2 as the tip velocity for $\dot\theta=(0,1)$. Both are arrows at the tip. Write the two arrows as vectors.
2. **Derive.** (a) Confirm $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ from the arrows (or from §2). (b) $J^{-1}$. (c) Joint rates that produce $v=(0,-0.25)\,\mathrm{m/s}$. (d) $\tau=J^\top F$ for $F=(2,-5)\,\mathrm{N}$. (e) Same $F$ at $\theta_2=5^\circ$ is *not* asked as a number — say which joint rate blows up if you instead asked for a tip velocity *along the arm*, and why $J^\top F$ itself does not blow up.
3. **Do.** Fill the template and reproduce the lecture's $T=0.01$, $2\,\mathrm{s}$ pair (live vs frozen $J$). Then change *only* $T$ to $0.05$, live $J$, same $2\,\mathrm{s}$. Is the extra error frozen-$J$ class or integrator class?

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
    xs.append(math.cos(th1) + math.cos(th1 + th2))
    ys.append(math.sin(th1) + math.sin(th1 + th2))
# plot xs, ys; caption "P2, explicit Euler on theta, T=0.01"
```

> [!note]- How to draw it · 그리는 법
> - Draw P2 to scale first: base at the origin, elbow at $(1,0)$, tip at $(1,1)$.
> - Column $i$ is the tip velocity when only joint $i$ turns at $1\,\mathrm{rad/s}$: an arrow perpendicular to the line from joint $i$ to the tip and as long as that line — $\sqrt2$ from the base for column 1, the unit forearm for column 2. Label each arrow with its vector.
> - Anchor both columns at the tip. Drawing a column from the base is the standard way this figure goes wrong: a Jacobian column is a velocity of the tip.
> - A commanded velocity is its own arrow out of the tip, in a different line weight from the columns, with the joint rates that produce it, $\dot\theta = J^{-1}v$, written beside it.
> - The manipulability ellipse is centred on the tip, the image of the unit circle of joint rates, with semi-axes equal to the singular values ($1.618$ and $0.618$ in the picture above). Draw it visibly elongated, long axis along the easy direction.
> - A force is an outlined arrow into the tip, never a solid one, so it cannot be read as a velocity; write $\tau = J^\top F$ beside it.

> [!tip]- Solutions
> 1. Shoulder-only: the tip is at lever arm $\sqrt{2}$ from the base, velocity perpendicular to $(1,1)$, i.e. parallel to $(-1,1)$. Unit $\dot\theta_1$ gives $|v|=L_\text{tip}=\sqrt{2}$, so column 1 $=(-1,1)$. Elbow-only: forearm is along $+y$ from $(1,0)$ to $(1,1)$, unit $\dot\theta_2$ gives $v$ perpendicular to the forearm, column 2 $=(-1,0)$.
> 2. (a) Columns of $J$ are those arrows. (b) $\det J=1$, $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. (c) $\dot\theta=J^{-1}(0,-0.25)=(-0.25,\ 0.25)\,\mathrm{rad/s}$. (d) $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$, $\tau=J^\top(2,-5)=(-7,-2)\,\mathrm{N{\cdot}m}$. (e) Along-the-arm velocity hits the lost singular direction; $\dot\theta\sim 1/\sigma_{\min}$ blows up. $J^\top F$ is a static map and stays finite — the structure carries the force, the motors need not.
> 3. $J$ blanks: `((-s1-s12, -s12), (c1+c12, c12))`. Inverse: `th1d = (J[1][1]*0 - J[0][1]*vy)/det`, `th2d = (-J[1][0]*0 + J[0][0]*vy)/det`. Lecture pair: live $\approx(0.999,\ 0.500)$, frozen $\approx(0.878,\ 0.521)$. Live at $T=0.05$: $\approx(0.997,\ 0.501)$ — still millimetre-scale. Integrator class. Frozen error is independent of $T$ (joint rates are constant), so it is not a step-size artefact.

## 한국어

**핵심 질문**: 관절 속도는 말단 속도로, 힘은 그 반대로 어떻게 사상되는가?

> [!note] 처음이라면 · First pass
> 그림과 §1 첫머리의 정의(열 $i$는 관절 $i$만 돌 때의 도구 운동)를 읽고, §2를 말단의 두 화살표와 resolved-rate 실행까지 읽어라. 야코비안이 속도 화살표 둘이라는 것과 왜 다시 계산해야 하는지가 거기 있다. 그다음 §3의 세 줄 유도 $\tau = J^\top\mathcal{F}$와 그 P2 숫자. §1의 나머지 프레임 관리, 6차원 검산과 §3 유도 뒤의 회계 문단들, §4의 타원체는 두 번째 읽기다. 6차원 검산에는 3장 §6의 렌치가 필요하다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 306" style="max-width:100%;height:auto" role="img" aria-label="카탈로그 자세의 P2 말단에 야코비안의 두 열 (−1, 1)과 (−1, 0) m/s, 명령 속도 (0, −0.25) m/s, 반축이 1.618과 0.618인 가조작성 타원, 말단으로 들어오는 윤곽선 힘 (0, −10) N을 그린 그림.">
  <defs><marker id="mr05hdK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker><marker id="mr05hdvK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <path d="M78 34 L74.3 34.1 L70.7 34.3 L67.3 34.6 L64 35.1 L60.9 35.6 L57.9 36.4 L55.1 37.2 L52.4 38.2 L49.9 39.3 L47.6 40.5 L45.4 41.9 L43.4 43.3 L41.6 44.9 L39.9 46.6 L38.5 48.5 L37.2 50.4 L36.1 52.5 L35.1 54.6 L34.4 56.9 L33.8 59.3 L33.5 61.7 L33.3 64.3 L33.3 67 L33.5 69.7 L33.8 72.6 L34.4 75.5 L35.1 78.5 L36.1 81.6 L37.2 84.8 L38.5 88 L39.9 91.3 L41.6 94.7 L43.4 98.1 L45.4 101.5 L47.6 105.1 L49.9 108.6 L52.4 112.2 L55.1 115.9 L57.9 119.5 L60.9 123.2 L64 127 L67.3 130.7 L70.7 134.5 L74.3 138.2 L78 142 L81.8 145.8 L85.8 149.5 L89.9 153.3 L94.1 157 L98.4 160.8 L102.8 164.5 L107.3 168.1 L112 171.8 L116.7 175.4 L121.5 178.9 L126.3 182.5 L131.3 185.9 L136.3 189.3 L141.3 192.7 L146.5 196 L151.6 199.2 L156.9 202.4 L162.1 205.5 L167.4 208.5 L172.7 211.4 L178 214.3 L183.3 217 L188.7 219.7 L194 222.3 L199.3 224.7 L204.6 227.1 L209.9 229.4 L215.1 231.5 L220.4 233.6 L225.5 235.5 L230.7 237.4 L235.7 239.1 L240.7 240.7 L245.7 242.1 L250.5 243.5 L255.3 244.7 L260 245.8 L264.7 246.8 L269.2 247.6 L273.6 248.4 L277.9 248.9 L282.1 249.4 L286.2 249.7 L290.2 249.9 L294 250 L297.7 249.9 L301.3 249.7 L304.7 249.4 L308 248.9 L311.1 248.4 L314.1 247.6 L316.9 246.8 L319.6 245.8 L322.1 244.7 L324.4 243.5 L326.6 242.1 L328.6 240.7 L330.4 239.1 L332.1 237.4 L333.5 235.5 L334.8 233.6 L335.9 231.5 L336.9 229.4 L337.6 227.1 L338.2 224.7 L338.5 222.3 L338.7 219.7 L338.7 217 L338.5 214.3 L338.2 211.4 L337.6 208.5 L336.9 205.5 L335.9 202.4 L334.8 199.2 L333.5 196 L332.1 192.7 L330.4 189.3 L328.6 185.9 L326.6 182.5 L324.4 178.9 L322.1 175.4 L319.6 171.8 L316.9 168.1 L314.1 164.5 L311.1 160.8 L308 157 L304.7 153.3 L301.3 149.5 L297.7 145.8 L294 142 L290.2 138.2 L286.2 134.5 L282.1 130.7 L277.9 127 L273.6 123.2 L269.2 119.5 L264.7 115.9 L260 112.2 L255.3 108.6 L250.5 105.1 L245.7 101.5 L240.7 98.1 L235.7 94.7 L230.7 91.3 L225.5 88 L220.4 84.8 L215.1 81.6 L209.9 78.5 L204.6 75.5 L199.3 72.6 L194 69.7 L188.7 67 L183.3 64.3 L178 61.7 L172.7 59.3 L167.4 56.9 L162.1 54.6 L156.9 52.5 L151.6 50.4 L146.5 48.5 L141.3 46.6 L136.3 44.9 L131.3 43.3 L126.3 41.9 L121.5 40.5 L116.7 39.3 L112 38.2 L107.3 37.2 L102.8 36.4 L98.4 35.6 L94.1 35.1 L89.9 34.6 L85.8 34.3 L81.8 34.1 Z" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="2 3" opacity="0.75"><line x1="186" y1="142" x2="37.4" y2="50.1"/><line x1="186" y1="142" x2="221.1" y2="85.2"/></g>
  <polyline points="78,250 186,250 186,142" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.3"/>
  <circle cx="78" cy="250" r="4.5" fill="currentColor" fill-opacity="0.6"/>
  <circle cx="186" cy="250" r="3.5" fill="currentColor" fill-opacity="0.6"/>
  <path d="M183 34 L189 34 L189 124 L193.5 124 L186 137 L178.5 124 L183 124 Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <g stroke="currentColor" stroke-width="2.4" marker-end="url(#mr05hdK)"><line x1="186" y1="142" x2="78" y2="34"/><line x1="186" y1="142" x2="78" y2="142"/></g>
  <line x1="186" y1="142" x2="186" y2="169" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr05hdvK)"/>
  <circle cx="186" cy="142" r="4" fill="currentColor"/>
  <line x1="350" y1="14" x2="350" y2="270" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="78" y="25" text-anchor="middle">열 1 = (−1, 1)</text>
    <text x="142" y="158" text-anchor="middle">열 2 = (−1, 0)</text>
    <text x="196" y="169">v = (0, −0.25)</text>
    <text x="196" y="184">θ̇ = (−0.25, 0.25) rad/s</text>
    <text x="198" y="43">F = (0, −10) N</text>
    <text x="198" y="58">τ = Jᵀ F = (−10, 0) N·m</text>
    <text x="24.4" y="44.1" text-anchor="middle">σ<tspan dy="3.5">1</tspan></text>
    <text x="227.1" y="77.2">σ<tspan dy="3.5">2</tspan></text>
    <text x="78" y="267" text-anchor="middle" opacity="0.8">베이스 (0, 0)</text>
    <text x="186" y="267" text-anchor="middle" opacity="0.8">엘보 (1, 0)</text>
    <text x="196" y="150" opacity="0.8">말단 (1, 1)</text>
    <text x="362" y="26" font-size="12">말단에서 나가는 속도</text>
    <text x="368" y="45">열 1 = (−1, 1) m/s, θ̇ = (1, 0)</text>
    <text x="368" y="62">열 1 ⟂ 베이스–말단 선, 길이 √2</text>
    <text x="368" y="79">열 2 = (−1, 0) m/s, θ̇ = (0, 1)</text>
    <text x="368" y="102">v = (0, −0.25) m/s (가는 선)</text>
    <text x="368" y="119">θ̇ = J⁻¹v = (−0.25, 0.25) rad/s</text>
    <text x="362" y="146" font-size="12">타원 = J · (단위원)</text>
    <text x="368" y="165">σ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 1.618 (긴 축, 쉬운 방향)</tspan></text>
    <text x="368" y="182">σ<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= 0.618, 축 비 2.6</tspan></text>
    <text x="362" y="209" font-size="12">말단으로 들어오는 힘 (윤곽선)</text>
    <text x="368" y="228">F = (0, −10) N</text>
    <text x="368" y="245">τ = Jᵀ F = (−10, 0) N·m</text>
    <text x="12" y="296" opacity="0.85">말단에서 나가는 화살표는 속도(1 m/s를 1 m로), 말단으로 들어오는 윤곽 화살표는 힘이다.</text>
  </g>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**, 카탈로그 자세 $\theta = (0^\circ, 90^\circ)$를 축척대로 그리고 모든 것을 말단 $(1,1)$에 붙였다. 야코비안의 두 열 $(-1,1)$과 $(-1,0)\,\mathrm{m/s}$는 어깨만, 또는 엘보만 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도이고, 가는 화살표인 명령 속도 $v = (0,-0.25)\,\mathrm{m/s}$에는 $\dot\theta = J^{-1}v = (-0.25,\ 0.25)\,\mathrm{rad/s}$가 필요하며, 가조작성 타원은 관절 속도 단위원의 상으로 반축이 $1.618$과 $0.618$이다. 윤곽선 화살표는 말단으로 들어오는 힘 $F = (0,-10)\,\mathrm{N}$이고 같은 $J$가 그것을 $\tau = J^\top F = (-10,\ 0)\,\mathrm{N{\cdot}m}$로 되돌린다 — 말단에서 나가는 화살표는 속도, 들어오는 화살표는 힘이다.

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

**그 두 열이 말단의 화살표다.** 어깨만 $\dot\theta=(1,0)$: 말단이 베이스에서 지렛대 $\sqrt{2}$, 속도는 $(1,1)$에 수직, 열 1 $=(-1,1)$. 엘보만 $\dot\theta=(0,1)$: 전완이 $+y$, 속도는 그에 수직, 열 2 $=(-1,0)$. 쌓으면 $J$가 나온다. 역행렬 $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. 이 자세에서 $v=(0,-0.25)\,\mathrm{m/s}$이면 $\dot\theta=(-0.25,\ 0.25)\,\mathrm{rad/s}$.

**계산: resolved-rate 오일러.** 같은 명령을 $2\,\mathrm{s}$, $T=0.01$, $\theta$에 명시적 오일러([[02-foundations/lab-kernel|0.7]]). $J(\theta)$를 매 스텝 재계산하면 말단 $\approx(0.999,\ 0.500)$, 명령 $\Delta y=-0.50\,\mathrm{m}$에서 $x$ 드리프트 $<1\,\mathrm{mm}$. 시작 $J$를 고정하면 $\approx(0.878,\ 0.521)$ — $x$ 오차 12 cm. 상수 야코비안은 국소 사상이지 유한 운동 사상이 아니다. 과제가 이 루프를 채우고, $T$를 바꾸는 것이 노브다.

### 3. 정역학 쌍대성 — 세 줄 유도

손실 없는 기구의 양 끝에서 일률은 같아야 한다. 관절 쪽 일률은 $\dot\theta^\top \tau$,
말단 쪽 일률은 $\mathcal{V}^\top \mathcal{F}$다. 렌치 $\mathcal{F} = (m, f) \in \mathbb{R}^6$은 도구가 가하는 모멘트와 힘을 쌓은 것이고, twist와의 짝 $\mathcal{V}^\top\mathcal{F} = \omega\cdot m + v\cdot f$가 와트 단위의 일률이다(프레임 규칙과 함께 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §6]]에서 정의).
$\mathcal{V} = J\dot\theta$를 대입하면:
$$\dot\theta^\top \tau = (J\dot\theta)^\top \mathcal{F} = \dot\theta^\top J^\top \mathcal{F} \quad \forall \dot\theta \;\;\Longrightarrow\;\; \boxed{\tau = J^\top(\theta)\,\mathcal{F}}$$
*같은* 행렬이 속도를 내보내고 렌치를 되받는다 — 중력 보상, 힘 제어, 접촉 추론이 전부 이
한 줄 위에서 돈다. (프레임은 맞춰야 한다: $J_b$는 body 렌치 $\mathcal{F}_b$와, $J_s$는
$\mathcal{F}_s$와 짝이다.) 카탈로그 P2에서 $F=(0,-10)\,\mathrm{N}$이면 $\tau=J^\top F=(-10,0)\,\mathrm{N{\cdot}m}$: 어깨가 지고 엘보는 안 진다. 과제는 다른 $F$를 쓴다.

**같은 숫자를 6차원 벡터로.** 이 힘을 공간 렌치로 쓰면 모멘트 $p\times f$를 베이스에 대해 잡은 $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$이고, 이 자세에서 공간 야코비안의 열은 스크류 $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$과 $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$이다. $\theta_1 = 0$이라 $\mathcal{S}_2$가 홈에서의 자리에 그대로 있기 때문이다. 따라서 $J_s^\top\mathcal{F}_s = (-10,\ 0)$이 다시 나오고, [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §6]]이 같은 검산을 바디 프레임에서 되풀이한다. $2\times2$ 지름길이 정확한 이유는 말단 힘과 말단 속도의 짝이 공간 렌치와 공간 twist의 짝과 같은 일률을 주기 때문이다.

**등식을 일률의 회계 규칙으로 읽는다.** 렌치는 작용하는 운동을 통해 일을 한다. 야코비안이 관절 운동이 도구에서 어떻게 보이는지 알려 주므로 전치는 도구 렌치가 각 관절에 주는 부하를 알려 준다. 열마다 그 열이 만드는 운동에 렌치가 얼마나 작용하는지 묻는다. 그 내적이 해당 관절의 노력이다.

속도 식을 역으로 푸는 것과 다르다. 알려진 렌치를 관절 부하로 바꾸는 데 역행렬은 필요 없고 특이점에서도 뜻이 있다. 반면 측정 토크에서 모르는 렌치를 찾는 역문제는 모호하거나 잡음에 민감할 수 있다. 숫자로 보면, $\theta = (0^\circ, 5^\circ)$에서 $J$의 가장 작은 특이값은 $0.039$이고 그 힘 방향 $(0.999,\ 0.052)$는 거의 정확히 팔을 따른다. 그쪽으로 $10\,\mathrm{N}$을 밀어도 관절 토크 벡터의 크기는 $0.39\,\mathrm{N\,m}$뿐이므로, 측정 토크의 $0.1\,\mathrm{N\,m}$ 오차가 팔 방향 힘을 최대 $0.1/0.039 = 2.6\,\mathrm{N}$까지 숨길 수 있다. 카탈로그 자세에서는 $0.1/0.618 = 0.16\,\mathrm{N}$이다. 측정 노력에서 중력, 관성, 마찰 등도 분리해야 한다.

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
    <text x="115" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90&#176; &#8212; 조건이 좋다</tspan></text><text x="355" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 20&#176; &#8212; 특이점에 접근</tspan></text>
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
3. **실행.** 템플릿을 채워 강의의 $T=0.01$, $2\,\mathrm{s}$ 쌍(산 $J$ 대 고정 $J$)을 재현한다. 그다음 $T$만 $0.05$로, 산 $J$, 같은 $2\,\mathrm{s}$. 추가 오차는 고정-$J$급인가 적분기급인가?

> [!note]- 그리는 법 · How to draw it
> - 먼저 P2를 축척대로 그린다. 베이스 원점, 엘보 $(1,0)$, 말단 $(1,1)$.
> - 열 $i$는 관절 $i$만 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도다. 관절 $i$에서 말단까지의 선에 수직이고 그 선만큼 긴 화살표로 그린다. 열 1은 베이스에서 $\sqrt2$, 열 2는 길이 1인 전완이다. 각 화살표에 벡터를 적는다.
> - 두 열 모두 말단에 붙인다. 베이스에서 그리는 것이 이 그림이 틀어지는 표준적인 방식이다. 야코비안의 열은 말단의 속도다.
> - 명령 속도는 말단에서 나가는 별도의 화살표로, 두 열과 다른 선 굵기로 그리고, 그것을 만드는 관절 속도 $\dot\theta = J^{-1}v$를 옆에 적는다.
> - 가조작성 타원은 말단 중심이고 관절 속도 단위원의 상이며, 반축은 특이값이다(위의 그림에서는 $1.618$과 $0.618$). 원이 아니라 눈에 띄게 길쭉하게, 긴 축을 쉬운 방향에 둔다.
> - 힘은 말단으로 들어오는 윤곽선 화살표로 그린다. 속을 채우지 않아야 속도로 읽히지 않는다. 옆에 $\tau = J^\top F$를 적는다.

> [!tip]- 정답 · Solutions
> 1. 어깨만: 말단이 베이스에서 지렛대 $\sqrt{2}$, 속도는 $(1,1)$에 수직 즉 $(-1,1)$ 방향. 단위 $\dot\theta_1$의 $|v|=\sqrt{2}$이므로 열 1 $=(-1,1)$. 엘보만: 전완이 $(1,0)\to(1,1)$의 $+y$, 단위 $\dot\theta_2$는 전완에 수직, 열 2 $=(-1,0)$.
> 2. (a) $J$의 열이 그 화살표. (b) $\det J=1$, $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. (c) $\dot\theta=(-0.25,\ 0.25)\,\mathrm{rad/s}$. (d) $\tau=(-7,-2)\,\mathrm{N{\cdot}m}$. (e) 팔 방향 속도는 잃어버린 특이 방향이라 $\dot\theta\sim 1/\sigma_{\min}$이 터진다. $J^\top F$는 정역학 사상이라 유한 — 구조가 힘을 지고 모터는 안 져도 된다.
> 3. 빈칸은 영어 해. 강의 쌍: 산 $\approx(0.999,\ 0.500)$, 고정 $\approx(0.878,\ 0.521)$. $T=0.05$ 산 $J$: $\approx(0.997,\ 0.501)$ — 여전히 밀리미터. 적분기급. 고정 오차는 $T$와 무관하다(관절 속도가 상수).
