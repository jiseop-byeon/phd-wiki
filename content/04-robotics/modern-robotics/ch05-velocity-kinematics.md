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
> Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled; P2 is the catalog's planar two-link arm). Its $2\times2$ Jacobian and $\tau = J^\top F$ were derived in [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §1]] and its singular values in [[02-foundations/linear-algebra|1. Linear Algebra §4.5.2]]; this page recalls them and adds the frames, the loop and the singularities. FK from [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]]; twists and the adjoint from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3–4]] and the wrench from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §6]]; partial derivatives and Jacobians ([[02-foundations/calculus-backprop|2. Calculus]]), and what matrix rank means ([[02-foundations/linear-algebra|1. Linear Algebra §2]]); the free-body diagram of the picture's press ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §2]]). How to step a loop: [[02-foundations/lab-kernel|0.7 Lab Kernel]], and [[02-foundations/tools/python-research-code|12.3 Python for Research Code]] first if Python is new.
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**(장치(plant)는 제어 공학에서 제어 대상 시스템을 부르는 말이고, P2는 카탈로그의 평면 2링크 팔이다). 그 $2\times2$ 야코비안과 $\tau = J^\top F$는 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §1]]에서, 특이값은 [[02-foundations/linear-algebra|1. 선형대수 §4.5.2]]에서 이미 유도했다. 이 페이지는 그것을 되짚고 프레임, 루프, 특이점을 더한다. [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 FK, [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3–4]]의 트위스트와 수반(adjoint), [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §6]]의 렌치, 편미분과 야코비안([[02-foundations/calculus-backprop|2. 미적분]]), 행렬의 랭크([[02-foundations/linear-algebra|1. 선형대수 §2]]), 그림 속 누르기의 자유물체도([[02-foundations/basic-mechanics|0.6.1 기초 역학 §2]]). 루프 전진은 [[02-foundations/lab-kernel|0.7 Lab Kernel]]이고, 파이썬이 처음이면 [[02-foundations/tools/python-research-code|12.3]]을 먼저 본다.

## English

**Core question**: how do joint velocities map to end-effector velocity — and forces back?

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] the Jacobian is the manipulation layer's local map, and through its transpose the first step into the contact-and-force layer; in *"install that panel on the frame"* it serves *move the component* (joint rates for a commanded tip velocity), *detect contact* (tip force read back from joint torques) and *perform the fitting* (the torque a press costs) — its chip sits in the manipulation band of the [[physical-ai-map|Physical AI Map]]. Without it motion and force both go wrong quietly: freeze $J$ at the start of a $0.5\,\mathrm{m}$ downward move of **P2**, the catalog's planar two-link arm ([[02-foundations/lab-plants|0.6]]), and the tip ends $12\,\mathrm{cm}$ off in $x$ (§2); multiply a wrist sensor's $\mathcal{F}_b$ by $J_s^\top$ and the $10\,\mathrm{N}$ press seems to load no joint (§3); and near the straight arm a $0.1\,\mathrm{N{\cdot}m}$ torque error hides $2.6\,\mathrm{N}$ of force along the arm, against $0.16\,\mathrm{N}$ at the catalog pose (§3). Later pages build on it section by section — [[04-robotics/force-compliance-control|13. Force & Compliance Control]] its Worked case, §3 and §4 on $\tau = J^\top\mathcal{F}$, [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation §1–§3]] reachability and base placement on §4's ellipsoids, [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration §5]] retargeting on §4, [[04-robotics/modern-robotics/ch11-robot-control|MR ch.11]] its Worked case on §3, and [[04-robotics/capstone-panel-contact|26. Capstone]] steps 3 and 5 of its Worked case — in block 2 of the dissertation path ([[07-research-program/index|7. Research Program §8]], robotics sessions 12–15). After it you can draw P2's Jacobian columns as tip velocities, compute joint rates and holding torques, recognise a singularity and judge a pressing pose by its force ellipsoid, and run a resolved-rate loop.

> [!note] First pass · 처음이라면
> About four 60–90-minute sessions, robotics 12–15. **Session 1:** the Running object, the picture and the Worked case by hand — $J$ from the two arrows at the tip, $J^{-1}$, the joint rates for $v = (0,-0.25)\,\mathrm{m/s}$ and the torque of the $10\,\mathrm{N}$ press — then §2, where $J$ becomes a function of $\theta$ and the resolved-rate run shows why it must be recomputed. End by redoing the Worked case with its answers covered. **Session 2:** §1 (the frame written down: $J_s$, $J_b$ and how the $2\times2$ sits inside them), §3 with its six-vector check and the force-sensing number, and §4's singularity and ellipsoids. **Session 3:** the self-check and problems 1–2. **Session 4:** problem 3, the lab. The collapsed *Deeper* notes are second pass.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's planar two-link arm: unit links, the shoulder at the origin, $\theta_1$ measured from the $+x$ axis and the elbow angle $\theta_2$ relative to link 1 — a "2R" arm, two revolute (rotating) joints. It stands at the catalog pose $\theta = (0^\circ, 90^\circ)$: elbow $(1,0)$, forearm straight up, tip $(1,1)$. The frames are ch.3's and ch.4's: $\{s\}$ at the shoulder, $\{b\}$ at the tip with $x_b$ along the forearm.

**The press.** The tool pushes $F = (0,-10)\,\mathrm{N}$ straight down on a panel lying flat under the tip (the forearm passes in front of the panel, out of the drawing plane, so only the tip touches it) — the orientation [[02-foundations/manipulator-kinematics-dynamics|10]] and [[04-robotics/force-compliance-control|13]] use; ch.2's upright panel, face $x = 1$, is the same panel turned through a right angle, and problem 2 presses it. $F$ is the force the tool applies to the panel; the panel pushes the tool back with $(0, +10)\,\mathrm{N}$.

*Scope: this page teaches the velocity Jacobian in the plane and as a six-vector map, the statics that shares its matrix, and singularities with the two ellipsoids, on P2. The arm's own mass is [[02-foundations/manipulator-kinematics-dynamics|10]] and [[04-robotics/modern-robotics/ch08-dynamics|ch.8]]; inverse kinematics is [[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 314" style="max-width:100%;height:auto" role="img" aria-label="P2 at the catalog pose with, at the tip, the two Jacobian columns (−1, 1) and (−1, 0) m/s, the commanded velocity (0, −0.25) m/s and the manipulability ellipse with semi-axes 1.618 and 0.618; beside it the press drawn apart: the tool pushes the panel with (0, −10) N and the panel pushes the tool back with (0, +10) N.">
  <defs><marker id="mr05hdE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker><marker id="mr05hdvE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <path d="M78 34 L74.3 34.1 L70.7 34.3 L67.3 34.6 L64 35.1 L60.9 35.6 L57.9 36.4 L55.1 37.2 L52.4 38.2 L49.9 39.3 L47.6 40.5 L45.4 41.9 L43.4 43.3 L41.6 44.9 L39.9 46.6 L38.5 48.5 L37.2 50.4 L36.1 52.5 L35.1 54.6 L34.4 56.9 L33.8 59.3 L33.5 61.7 L33.3 64.3 L33.3 67 L33.5 69.7 L33.8 72.6 L34.4 75.5 L35.1 78.5 L36.1 81.6 L37.2 84.8 L38.5 88 L39.9 91.3 L41.6 94.7 L43.4 98.1 L45.4 101.5 L47.6 105.1 L49.9 108.6 L52.4 112.2 L55.1 115.9 L57.9 119.5 L60.9 123.2 L64 127 L67.3 130.7 L70.7 134.5 L74.3 138.2 L78 142 L81.8 145.8 L85.8 149.5 L89.9 153.3 L94.1 157 L98.4 160.8 L102.8 164.5 L107.3 168.1 L112 171.8 L116.7 175.4 L121.5 178.9 L126.3 182.5 L131.3 185.9 L136.3 189.3 L141.3 192.7 L146.5 196 L151.6 199.2 L156.9 202.4 L162.1 205.5 L167.4 208.5 L172.7 211.4 L178 214.3 L183.3 217 L188.7 219.7 L194 222.3 L199.3 224.7 L204.6 227.1 L209.9 229.4 L215.1 231.5 L220.4 233.6 L225.5 235.5 L230.7 237.4 L235.7 239.1 L240.7 240.7 L245.7 242.1 L250.5 243.5 L255.3 244.7 L260 245.8 L264.7 246.8 L269.2 247.6 L273.6 248.4 L277.9 248.9 L282.1 249.4 L286.2 249.7 L290.2 249.9 L294 250 L297.7 249.9 L301.3 249.7 L304.7 249.4 L308 248.9 L311.1 248.4 L314.1 247.6 L316.9 246.8 L319.6 245.8 L322.1 244.7 L324.4 243.5 L326.6 242.1 L328.6 240.7 L330.4 239.1 L332.1 237.4 L333.5 235.5 L334.8 233.6 L335.9 231.5 L336.9 229.4 L337.6 227.1 L338.2 224.7 L338.5 222.3 L338.7 219.7 L338.7 217 L338.5 214.3 L338.2 211.4 L337.6 208.5 L336.9 205.5 L335.9 202.4 L334.8 199.2 L333.5 196 L332.1 192.7 L330.4 189.3 L328.6 185.9 L326.6 182.5 L324.4 178.9 L322.1 175.4 L319.6 171.8 L316.9 168.1 L314.1 164.5 L311.1 160.8 L308 157 L304.7 153.3 L301.3 149.5 L297.7 145.8 L294 142 L290.2 138.2 L286.2 134.5 L282.1 130.7 L277.9 127 L273.6 123.2 L269.2 119.5 L264.7 115.9 L260 112.2 L255.3 108.6 L250.5 105.1 L245.7 101.5 L240.7 98.1 L235.7 94.7 L230.7 91.3 L225.5 88 L220.4 84.8 L215.1 81.6 L209.9 78.5 L204.6 75.5 L199.3 72.6 L194 69.7 L188.7 67 L183.3 64.3 L178 61.7 L172.7 59.3 L167.4 56.9 L162.1 54.6 L156.9 52.5 L151.6 50.4 L146.5 48.5 L141.3 46.6 L136.3 44.9 L131.3 43.3 L126.3 41.9 L121.5 40.5 L116.7 39.3 L112 38.2 L107.3 37.2 L102.8 36.4 L98.4 35.6 L94.1 35.1 L89.9 34.6 L85.8 34.3 L81.8 34.1 Z" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="2 3" opacity="0.75"><line x1="186" y1="142" x2="37.4" y2="50.1"/><line x1="186" y1="142" x2="221.1" y2="85.2"/></g>
  <polyline points="78,250 186,250 186,142" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.3"/>
  <circle cx="78" cy="250" r="4.5" fill="currentColor" fill-opacity="0.6"/>
  <circle cx="186" cy="250" r="3.5" fill="currentColor" fill-opacity="0.6"/>
  <g stroke="currentColor" stroke-width="2.4" marker-end="url(#mr05hdE)"><line x1="186" y1="142" x2="78" y2="34"/><line x1="186" y1="142" x2="78" y2="142"/></g>
  <line x1="186" y1="142" x2="186" y2="169" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr05hdvE)"/>
  <circle cx="186" cy="142" r="4" fill="currentColor"/>
  <line x1="350" y1="14" x2="350" y2="290" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <circle cx="382" cy="220" r="4" fill="currentColor"/>
  <line x1="360" y1="266" x2="408" y2="266" stroke="currentColor" stroke-width="1.6"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="366" y1="266" x2="360" y2="273"/> <line x1="374" y1="266" x2="368" y2="273"/> <line x1="382" y1="266" x2="376" y2="273"/> <line x1="390" y1="266" x2="384" y2="273"/> <line x1="398" y1="266" x2="392" y2="273"/></g>
  <path d="M373 227 L379 227 L379 254 L383.5 254 L376 265 L368.5 254 L373 254 Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <line x1="391" y1="264" x2="391" y2="226" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr05hdvE)"/>
  <g font-size="11" fill="currentColor">
    <text x="78" y="25" text-anchor="middle">col 1 = (−1, 1)</text>
    <text x="142" y="158" text-anchor="middle">col 2 = (−1, 0)</text>
    <text x="196" y="169">v = (0, −0.25)</text>
    <text x="196" y="184">θ̇ = (−0.25, 0.25) rad/s</text>
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
    <text x="362" y="203" font-size="12">The press, drawn apart</text>
    <text x="414" y="224">F = (0, −10) N</text>
    <text x="414" y="238" opacity="0.85">tool on panel (outlined)</text>
    <text x="414" y="256">(0, +10) N</text>
    <text x="414" y="270" opacity="0.85">panel on tool (thin)</text>
    <text x="414" y="288">τ = JᵀF = (−10, 0) N·m</text>
    <text x="12" y="304" opacity="0.85">Arrows at the tip are velocities, 1 m/s drawn as 1 m; the press and its reaction are drawn apart, right.</text>
  </g>
</svg>

Plant **P2** at the catalog pose $\theta = (0^\circ, 90^\circ)$, drawn to scale with the velocities anchored at the tip $(1,1)$: the Jacobian columns $(-1,1)$ and $(-1,0)\,\mathrm{m/s}$, the tip velocities when only the shoulder or only the elbow turns at $1\,\mathrm{rad/s}$; the thin commanded velocity $v = (0,-0.25)\,\mathrm{m/s}$, which needs $\dot\theta = J^{-1}v = (-0.25,\ 0.25)\,\mathrm{rad/s}$; and the manipulability ellipse, the image of the unit circle of joint rates, with semi-axes $1.618$ and $0.618$. On the right the press is drawn apart, as a free-body diagram draws it ([[02-foundations/basic-mechanics|0.6.1 §2]]): the tool pushes the panel with $F = (0,-10)\,\mathrm{N}$, the force $\tau = J^\top F$ takes, the panel pushes the tool back with $(0,+10)\,\mathrm{N}$, and the same $J$ maps $F$ to $\tau = (-10,\ 0)\,\mathrm{N{\cdot}m}$.

### Worked case · 대상으로 한 번 끝까지

Everything here was met once already on this pose — the Jacobian and $\tau = J^\top F$ in [[02-foundations/manipulator-kinematics-dynamics|10. §1]], the singular values in [[02-foundations/linear-algebra|1. Linear Algebra §4.5.2]] — so this is a recall, done the way this chapter reads it: as arrows at the tip. What the chapter adds comes after it: the frames (§1), $J$ as a function of $\theta$ and why it must be recomputed (§2), the statics as a six-vector map (§3), and the singular poses (§4).

**Step 1 — the two columns are arrows at the tip.** Column $i$ of $J$ is the tip velocity when joint $i$ alone turns at $1\,\mathrm{rad/s}$. Turning a joint moves the tip on a circle about that joint, so the arrow is perpendicular to the line from the joint to the tip and as long as that line. Shoulder only, $\dot\theta = (1,0)$: the tip is $\sqrt2$ from the base along $(1,1)$, so column 1 is $(-1,1)$. Elbow only, $\dot\theta = (0,1)$: the forearm points along $+y$ with length 1, so column 2 is $(-1,0)$. Stacked side by side, because the joint rates weight the columns:

$$J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}, \qquad \det J = (-1)(0) - (-1)(1) = 1$$

**Step 2 — invert, and resolve a commanded velocity.** With $\det J = 1$ the $2\times2$ inverse (swap the diagonal, negate the off-diagonal, divide by the determinant) is $J^{-1} = \begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. Command the tip straight down at $v = (0,-0.25)\,\mathrm{m/s}$; since $v = J\dot\theta$, the joint rates are

$$\dot\theta = J^{-1}v = \begin{pmatrix}0&1\\-1&-1\end{pmatrix}\begin{pmatrix}0\\-0.25\end{pmatrix} = (-0.25,\ 0.25)\ \mathrm{rad/s}$$

so the shoulder turns clockwise and the elbow counterclockwise at the same rate: at this instant the forearm does not turn at all, and the tip moves exactly as the elbow does, straight down. Check it with the arrows: $-0.25\,(-1,1) + 0.25\,(-1,0) = (0,\ -0.25)$.

**Step 3 — the press, by power.** Leave the arm's own weight out — its holding torque is added separately (§3) — and let the arm creep through this pose. A weightless arm moving that slowly stores no energy, so the power the motors put in equals the power the tool delivers, $\tau^\top\dot\theta = F^\top v = F^\top J\dot\theta$, for every $\dot\theta$, and therefore $\tau = J^\top F$ (§3 states the conditions). For the press, because $J^\top$ has the columns of $J$ as its rows,

$$\tau = J^\top F = \begin{pmatrix}-1&1\\-1&0\end{pmatrix}\begin{pmatrix}0\\-10\end{pmatrix} = (-10,\ 0)\ \mathrm{N{\cdot}m}$$

The shoulder carries the whole press, $10\,\mathrm{N}$ on a $1\,\mathrm{m}$ lever, and the elbow carries nothing, because the push runs straight along the forearm through the elbow's axis. Read it off the arrows: column 2, the elbow's tip velocity $(-1,0)$, is perpendicular to $F$, so $F$ does no work on the elbow's motion — that zero dot product is the zero torque.

### 1. The Jacobian — with its frame written down

The Worked case's $J$ gives the tip's velocity in the plane. A controller that also turns the tool, or that reads a wrist sensor, needs the tool's whole rigid-body velocity — a twist, six numbers $(\omega, v)$ written in a named frame ([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3]]) — and the Jacobian that returns it, which says that every joint rate adds its own column of motion:

$$\mathcal{V}_s = J_s(\theta)\,\dot\theta \qquad \text{or} \qquad \mathcal{V}_b = J_b(\theta)\,\dot\theta$$

Column $i$ is the end-effector twist produced by unit velocity of joint $i$ alone, as in the Worked case, but now the frame is part of the object: $J_s$ gives space-frame twists, $J_b$ body-frame twists, and the two are related by $J_s = [\text{Ad}_{T_{sb}}]\,J_b$ ([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §4]]).

> **Space and body Jacobians, defined.** The **space Jacobian** $J_s(\theta)$ and the **body Jacobian** $J_b(\theta)$ are *matrix-valued functions of the configuration*, each $6\times n$: one object written in two frames. Three conditions define them. Each is **linear in the joint rates at a fixed $\theta$**: a combined motion is the weighted sum of the columns. **Column $i$ is joint $i$'s screw axis at the current configuration**, the twist produced by $\dot\theta_i = 1$ with every other rate zero. And **the frame is part of the object**: $J_s$ returns twists in $\{s\}$, $J_b$ in $\{b\}$ (MR §5.1).
>
> $$\mathcal{V}_s = J_s\dot\theta,\quad \mathcal{V}_b = J_b\dot\theta, \qquad J_{s,i}(\theta) = [\mathrm{Ad}_{e^{[\mathcal{S}_1]\theta_1}\cdots e^{[\mathcal{S}_{i-1}]\theta_{i-1}}}]\,\mathcal{S}_i, \qquad J_s = [\mathrm{Ad}_{T_{sb}}]\,J_b$$
>
> where $\mathcal{S}_i$ are ch.4's screws at home and the adjoint moves joint $i$'s axis to where joints $1$ to $i-1$ have carried it, which means that column $i$ of $J_s$ depends only on the joints before it.
>
> - **Example**: P2 at the catalog pose. $\theta_1 = 0$ leaves both axes at home, so the columns of $J_s$ are $(0,0,1;\,0,0,0)$ and $(0,0,1;\,0,-1,0)$; those of $J_b$ are $(0,0,1;\,1,1,0)$ and $(0,0,1;\,0,1,0)$, and $[\mathrm{Ad}_{T_{sb}}]J_b = J_s$.
> - **Example, with the adjoint at work**: P2 at $\theta = (90^\circ, 90^\circ)$. Joint 1 has carried the elbow's axis from $(1,0)$ to $(0,1)$, so column 2 of $J_s$ is $(0,0,1;\,1,0,0)$, the screw of an axis through $(0,1)$, not ch.4's home screw $\mathcal{S}_2 = (0,0,1;\,0,-1,0)$. [[04-robotics/modern-robotics/ch04-forward-kinematics|Ch.4 §1]]'s non-example feeds exactly this screw to the product of exponentials and puts the tip $2\,\mathrm{m}$ off; as a Jacobian column it is right, because the column is the axis carried there by the joint before it.
> - **Non-example**: the bottom rows of $J_s$ read as the tip's velocity. Column 1's linear part is $(0,0,0)$, yet the tip moves at $(-1,1)\,\mathrm{m/s}$ when the shoulder turns at $1\,\mathrm{rad/s}$, because a space twist's $v$ is the velocity of the body point at the origin of $\{s\}$ ([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3]]). The tip's velocity is $R_{sb}v_b$: $(-1,1)$ and $(-1,0)$, the columns of the Worked case's $J$. A resolved-rate loop built on those rows steers a point at the base, not the tool.

**How the $2\times2$ sits inside.** The Worked case's $J = \partial p/\partial\theta$ is the Jacobian of [[02-foundations/calculus-backprop|2. Calculus]]: the derivative of the tip's two coordinates. $J_s$ and $J_b$ are not the derivative of any six coordinates — their columns are screw axes — but they contain it: the tip's velocity is $\dot p = R_{sb}v_b = v_s + \omega_s \times p$, so rotating $J_b$'s linear rows into $\{s\}$ gives the Worked case's columns. At the catalog pose $R_{sb} = R_z(90^\circ)$ turns $(1,1,0)$ into $(-1,1,0)$ and $(0,1,0)$ into $(-1,0,0)$, the two arrows of Step 1.

> [!note]- Deeper · 더 깊이
> **Column by column, and why "at a fixed configuration".** Freeze the configuration and move one joint: the tool's instantaneous rigid-body motion in the declared frame is one column, and simultaneous joint motion is the weighted sum of the columns because the map is linear at that configuration. Once the joints move, their axes and lever arms relative to the tool change, so the Jacobian must be recomputed: a constant Jacobian predicts a small local displacement, not a finite motion (§2's frozen run shows the cost). Forward kinematics updates the pose; the Jacobian is its local sensitivity.
>
> **Rows and columns.** With $n$ joint rates and an $m$-number task velocity, $J$ is $m \times n$. A full twist uses $J_s$ or $J_b$, $6\times n$; a position-only task uses a reduced Jacobian such as the Worked case's $2\times2$. Never delete the angular rows of $J_s$ and read what is left as the tip's velocity: its linear part belongs to the point at the origin of $\{s\}$, as the non-example above shows.

### 2. Worked example — the planar 2R arm's tip Jacobian

The Worked case read $J$ off two arrows at one pose. The arm does not stay there, and a controller needs $J$ wherever the arm is, so differentiate the forward kinematics once, symbolically. For the tip position, where a $2\times2$ suffices because the arm is planar:
$$x = L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2), \qquad y = L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2)$$
Each entry is one partial derivative. The chain rule on the second term of $x$ gives $\partial\cos(\theta_1{+}\theta_2)/\partial\theta_1 = -\sin(\theta_1{+}\theta_2)\cdot 1$, so $\partial x/\partial\theta_1 = -L_1\sin\theta_1 - L_2\sin(\theta_1{+}\theta_2)$, while $\theta_2$ appears only in that term, so $\partial x/\partial\theta_2 = -L_2\sin(\theta_1{+}\theta_2)$. The $y$ row is the same with $\sin \to \cos$. Stacking rows $(x, y)$ against columns $(\theta_1, \theta_2)$, because each row is one coordinate and each column one joint:
$$J(\theta) = \begin{pmatrix} -L_1 s_1 - L_2 s_{12} & -L_2 s_{12} \\ L_1 c_1 + L_2 c_{12} & L_2 c_{12} \end{pmatrix}$$
with $s_1 = \sin\theta_1$, $c_1 = \cos\theta_1$, $s_{12} = \sin(\theta_1{+}\theta_2)$ and $c_{12} = \cos(\theta_1{+}\theta_2)$. At $L_1 = L_2 = 1$ and $\theta = (0°, 90°)$, $s_1 = 0$, $c_1 = 1$, $s_{12} = 1$ and $c_{12} = 0$ return the Worked case's $J$, whose columns were the two arrows. In general
$\det J = L_1 L_2 \sin\theta_2$: **the arm is singular exactly when straight or folded**
($\theta_2 = 0°$ or $180°$) — geometrically obvious once the math says where to look: straight or folded, the two arrows are parallel.

A formula for $J(\theta)$ is what lets a controller follow a commanded velocity for more than an instant.

> **Resolved-rate control, defined.** **Resolved-rate control** is *a loop that turns a commanded tool velocity into joint motion*, one control period at a time. Three conditions define it. **The command is a task velocity**, here the tip velocity $v$, not a joint target. **It is resolved at the current configuration**: each period solves $J(\theta_k)\,\dot\theta = v$ with $J$ evaluated at the joints the arm has now. **It integrates**: the joint rates are held for one period $T$ and added to the joint command.
>
> $$\dot\theta_k = J(\theta_k)^{-1}v, \qquad \theta_{k+1} = \theta_k + T\,\dot\theta_k$$
>
> where $J^{-1}$ exists away from singularities (§4) and becomes a pseudoinverse for a non-square $J$ (ch.6); the loop is explicit Euler on $\dot\theta = J(\theta)^{-1}v$ ([[02-foundations/lab-kernel|0.7]]), which means that its error has two sources, the step $T$ and a stale $J$.
>
> - **Example**: P2 from the catalog pose, $v = (0,-0.25)\,\mathrm{m/s}$ for $2\,\mathrm{s}$ at $T = 0.01\,\mathrm{s}$. The tip ends at $\approx(0.999,\ 0.500)$, under $1\,\mathrm{mm}$ of $x$-drift on a commanded $\Delta y = -0.50\,\mathrm{m}$, with the joints at $(-29.4^\circ,\ 112.1^\circ)$.
> - **Non-example**: the same loop with $J$ frozen at the start. The joint rates stay $(-0.25,\ 0.25)$ for the whole run, so $\theta_1 + \theta_2$ stays $90^\circ$: the forearm stays upright and the tip rides the elbow's circle raised $1\,\mathrm{m}$, $p = (\cos\theta_1,\ 1 + \sin\theta_1)$, to $\approx(0.878,\ 0.521)$ — twelve centimetres of $x$ error. A constant Jacobian is a local map, not a finite-motion map.
> - **Why it matters**: a teleoperation handle or a policy that outputs tool velocities reaches the motors through this loop, so it inherits both errors, and the stale-$J$ one does not shrink with a smaller $T$ (problem 3).

<svg viewBox="0 0 560 320" style="max-width:100%;height:auto" role="img" aria-label="P2 following the command v = (0, −0.25) m/s for 2 s from the catalog pose: with J recomputed every step the tip goes straight down to (0.999, 0.500); with the start J frozen it rides the elbow circle raised 1 m and ends at (0.878, 0.521), 12 cm off in x.">
  <defs><marker id="mr05rre" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="0.8" opacity="0.25"><line x1="36.0" y1="226" x2="268.0" y2="226"/><line x1="60" y1="314.0" x2="60" y2="34.0"/></g>
  <polyline points="178.9,173.1 180.8,171.0 182.6,168.8 184.3,166.7 186.1,164.5 187.8,162.3 189.4,160.0 191.1,157.8 192.6,155.5 194.2,153.1 195.7,150.8 197.1,148.4 198.6,146.0 199.9,143.6 201.3,141.1 202.6,138.6 203.8,136.1 205.0,133.6 206.2,131.1 207.3,128.5 208.3,125.9 209.4,123.3 210.4,120.7 211.3,118.1 212.2,115.4 213.0,112.8 213.8,110.1 214.5,107.4 215.2,104.7 215.9,102.0 216.5,99.3 217.1,96.5 217.6,93.8 218.0,91.0 218.4,88.3 218.8,85.5 219.1,82.7 219.4,79.9 219.6,77.2 219.8,74.4 219.9,71.6 220.0,68.8 220.0,66.0 220.0,63.2 219.9,60.4 219.8,57.6 219.6,54.8 219.4,52.1 219.1,49.3 218.8,46.5 218.4,43.7" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
  <polyline points="60.0,226.0 220.0,226.0 220.0,66.0" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" opacity="0.18"/>
  <line x1="60.0" y1="66.0" x2="200.4" y2="142.7" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
  <circle cx="60.0" cy="66.0" r="3" fill="currentColor" fill-opacity="0.6"/>
  <polyline points="60.0,226.0 200.4,302.7 200.4,142.7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 4" stroke-linejoin="round" opacity="0.7"/>
  <polyline points="60.0,226.0 199.3,304.7 219.9,146.0" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
  <polyline points="220.0,66.0 220.0,70.0 220.0,74.0 220.0,78.0 220.0,82.0 220.0,86.0 220.0,90.0 220.0,94.0 220.0,98.0 220.0,102.0 219.9,106.0 219.9,110.0 219.9,114.0 219.9,118.0 219.9,122.0 219.9,126.0 219.9,130.0 219.9,134.0 219.9,138.0 219.9,142.0 219.9,146.0 219.9,146.0" fill="none" stroke="currentColor" stroke-width="1.8" marker-end="url(#mr05rre)"/>
  <polyline points="220.0,66.0 220.0,70.0 219.8,74.0 219.6,78.0 219.2,82.0 218.8,85.9 218.2,89.9 217.6,93.9 216.8,97.8 216.0,101.7 215.0,105.6 214.0,109.4 212.9,113.3 211.6,117.1 210.3,120.9 208.9,124.6 207.4,128.3 205.8,132.0 204.1,135.6 202.3,139.2 200.4,142.7 200.4,142.7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#mr05rre)"/>
  <circle cx="60.0" cy="226.0" r="4.5" fill="currentColor" fill-opacity="1"/>
  <circle cx="220.0" cy="226.0" r="3" fill="currentColor" fill-opacity="0.3"/>
  <circle cx="199.3" cy="304.7" r="3.5" fill="currentColor" fill-opacity="1"/>
  <circle cx="200.4" cy="302.7" r="3.5" fill="currentColor" fill-opacity="0.7"/>
  <circle cx="220.0" cy="146.0" r="5.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.8"><line x1="200.4" y1="160.0" x2="219.9" y2="160.0"/><line x1="200.4" y1="156.0" x2="200.4" y2="164.0"/><line x1="219.9" y1="156.0" x2="219.9" y2="164.0"/></g>
  <g font-size="11" fill="currentColor">
    <text x="230.0" y="70.0">start (0°, 90°)</text>
    <text x="229.9" y="146.0">target (1, 0.5)</text>
    <text x="225.9" y="164.0">12 cm</text>
    <text x="52" y="242" text-anchor="end" opacity="0.8">base</text>
    <text x="174.9" y="185.1" text-anchor="end" opacity="0.75">elbow circle raised 1 m</text>
    <text x="68" y="62" opacity="0.75">centre (0, 1)</text>
    <text x="312" y="240" opacity="0.8">drawn to scale; the light arm is the start</text>
  </g>
  <line x1="300" y1="14" x2="300" y2="300" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="312" y="28" font-size="12">One command, v = (0, −0.25) m/s for 2 s</text>
    <line x1="314" y1="52" x2="340" y2="52" stroke="currentColor" stroke-width="2.6"/>
    <text x="348" y="56">live J, recomputed each step</text>
    <text x="348" y="74">tip ends at (0.999, 0.500)</text>
    <text x="348" y="92">θ = (−29.4°, 112.1°)</text>
    <line x1="314" y1="124" x2="340" y2="124" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 4" opacity="0.7"/>
    <text x="348" y="128">frozen J, the start's</text>
    <text x="348" y="146">joint rates stay (−0.25, 0.25) rad/s</text>
    <text x="348" y="164">θ₁ + θ₂ = 90°: forearm upright</text>
    <text x="348" y="182">tip rides the elbow circle raised 1 m</text>
    <text x="348" y="200">ends at (0.878, 0.521): 12 cm off in x</text>
  </g>
</svg>

The two runs of the box, drawn to scale from the catalog pose: recomputing $J$ every step takes the tip straight down to $(0.999,\ 0.500)$, while the frozen $J$ keeps the forearm upright and lets the tip ride the elbow's circle raised $1\,\mathrm{m}$, about $(0,1)$, to $(0.878,\ 0.521)$, $12\,\mathrm{cm}$ short in $x$ — the dotted radius from $(0,1)$ to that tip stays parallel to link 1, since the frozen tip is always the elbow moved straight up $1\,\mathrm{m}$. The two elbows end within $1.4\,\mathrm{cm}$ of each other, near $(0.87,\ -0.49)$; the whole difference is in how the forearm turned. The problem set fills this loop; changing $T$ is the knob.

### 3. Statics duality — derived in three lines

Pressing the panel with $10\,\mathrm{N}$ costs the shoulder $10\,\mathrm{N{\cdot}m}$ and the elbow nothing (Worked case, Step 3). A force controller needs that map at every pose and for every wrench, and a contact detector needs it backwards, from measured torques to the force at the tool. [[02-foundations/manipulator-kinematics-dynamics|10. §1]] derived it for P2's $2\times2$ case; here it is for the six-vector wrench, with the conditions it needs.

Power must match at both ends of a lossless mechanism. Joint-side power is
$\dot\theta^\top \tau$; end-effector-side power is $\mathcal{V}^\top \mathcal{F}$, where the
wrench $\mathcal{F} = (m, f) \in \mathbb{R}^6$ stacks the moment and the force the tool applies, and its pairing with a twist, $\mathcal{V}^\top\mathcal{F} = \omega\cdot m + v\cdot f$, is a power in watts (defined with its frame rule in [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §6]]). Substitute $\mathcal{V} = J\dot\theta$, because the tool's twist is what the joints produce:
$$\dot\theta^\top \tau = (J\dot\theta)^\top \mathcal{F} = \dot\theta^\top J^\top \mathcal{F} \quad \forall \dot\theta \;\;\Longrightarrow\;\; \boxed{\tau = J^\top(\theta)\,\mathcal{F}}$$
The *same* matrix maps velocities out and wrenches back in — gravity compensation, force
control, and contact reasoning all run on this one line. (Frames must match: $J_b$ pairs
with the body wrench $\mathcal{F}_b$, $J_s$ with $\mathcal{F}_s$.)

**The same number from the full six-vectors.** As a space wrench this force is $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$, its moment $p\times f$ taken about the base, and at this pose the space Jacobian's columns are the screws $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$ and $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$, since $\theta_1 = 0$ leaves $\mathcal{S}_2$ where it was at home. So $J_s^\top\mathcal{F}_s = (-10,\ 0)$ again, and [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §6]] repeats the check in the body frame. The $2\times2$ shortcut is exact because pairing the tip force with the tip velocity gives the same power as pairing the space wrench with the space twist.

> **Statics duality, defined.** The **statics duality** is *a linear map from end-effector wrenches to joint torques*, the transpose of the velocity Jacobian at the same $\theta$, and it holds under three conditions. **Static equilibrium**: the arm is at rest, $\dot\theta = 0$ and $\ddot\theta = 0$ (MR reads the power balance in the limit $\dot\theta \to 0$), so no power goes into moving the arm and the power at the joints equals the power at the tool. **One frame for both**: $J_b$ pairs with the body wrench $\mathcal{F}_b$, $J_s$ with $\mathcal{F}_s$. And **$\mathcal{F}$ is the wrench the tool applies**; the torques that hold up the arm's own weight are added separately (MR §5.2).
>
> $$\tau = J^\top(\theta)\,\mathcal{F} \quad\Longleftrightarrow\quad \tau^\top\dot\theta = \mathcal{F}^\top J(\theta)\,\dot\theta \ \ \text{for every } \dot\theta$$
>
> where $\tau \in \mathbb{R}^n$ is the joint-torque vector, $\mathcal{F}$ the wrench (the tip force alone when paired with the Worked case's $J$) and $J$ the Jacobian in the same frame; the transpose appears because power is a dot product, so the matrix that sends $\dot\theta$ out must send $\mathcal{F}$ back.
>
> - **Example**: the $10\,\mathrm{N}$ press. $\mathcal{F}_s$ with $J_s$ gives $\tau = (-10,\ 0)\,\mathrm{N\,m}$, and so does the same force in the tool frame, $\mathcal{F}_b = (0,0,0;\,-10,0,0)$, with $J_b$.
> - **Non-example**: a wrist sensor's $\mathcal{F}_b$ multiplied by $J_s^\top$. It returns $(0,\ 0)$, as if the contact loaded no joint: the shoulder's real $10\,\mathrm{N\,m}$ vanishes because the frames were mixed.

**Reading torques back into a force is the hard direction.** Mapping a known wrench to joint loads needs no inverse, and the map stays meaningful at a singularity. Solving backwards for an unknown wrench from measured torques may be ambiguous or noise-sensitive. In numbers: at $\theta = (0^\circ, 5^\circ)$ the smallest singular value of $J$ is $0.039$, and its force direction, $(0.999,\ 0.052)$, lies almost exactly along the arm. A $10\,\mathrm{N}$ push that way produces a joint-torque vector of norm only $0.39\,\mathrm{N\,m}$, so a $0.1\,\mathrm{N\,m}$ error in the measured torques can hide up to $0.1/0.039 = 2.6\,\mathrm{N}$ of force along the arm, against $0.1/0.618 = 0.16\,\mathrm{N}$ at the catalog pose. It also requires separating contact loads from gravity, inertia, friction, and other contributions to measured effort.

> [!note]- Deeper · 더 깊이
> **The equality as an accounting rule.** A wrench does work through the motion it acts on. The Jacobian tells how a joint motion appears at the tool, so its transpose tells how the same tool wrench loads each joint: for each column, the dot product of the wrench with the motion that column produces is that joint's torque, its generalized force. In the Worked case the press is perpendicular to column 2, so the elbow's torque is zero.
>
> **Zero torque is not zero force.** If a force does no work along a joint's permitted instantaneous motion, its contribution to that joint's torque is zero, but the force is still there, carried as a reaction in the constrained directions: the elbow's bearing carries the whole $10\,\mathrm{N}$ press while its motor carries nothing. Match wrench and twist conventions, units and frames before using the power identity.

### 4. Singularities and the manipulability ellipsoid

Straighten P2 to $\theta = (0^\circ, 5^\circ)$ and moving the tip $0.1\,\mathrm{m/s}$ straight out costs $2.56\,\mathrm{rad/s}$ of joint rate, $16$ times what the catalog pose needs: near a singularity small task motions demand huge joint velocities, because $J^{-1}$ blows up as $\det J = \sin\theta_2 \to 0$. This section says exactly when a pose is singular, and how to measure how close it is.

> **Kinematic singularity, defined.** A **kinematic singularity** is *a property of a configuration* $\theta$, judged through a chosen task Jacobian $J(\theta)$. Three conditions define it. **Rank drop**: $\operatorname{rank}J(\theta)$ falls below the largest rank $J$ reaches anywhere; for a square $J$, $\det J(\theta) = 0$. **Frame independence**: $\operatorname{rank}J_s = \operatorname{rank}J_b$ because $[\mathrm{Ad}_{T_{sb}}]$ is invertible, so the frame in which the twist is written cannot create or remove one. **Task relativity**: the rows of $J$ name the task, which point and which coordinates, and a different task has its own singular poses. At such a $\theta$ the tool cannot move instantaneously in some direction, and it holds a wrench along that direction with zero joint torque (MR §5.3).
>
> $$\operatorname{rank}J(\theta) < \max_{\theta'}\,\operatorname{rank}J(\theta'), \qquad \text{P2's tip: } \det J(\theta) = L_1L_2\sin\theta_2 = 0$$
>
> where the maximum runs over all configurations, so the test compares a pose with the arm's own best, not with the number of task rows.
>
> - **Example**: P2 straight, $\theta = (0^\circ, 0^\circ)$: $J = \begin{pmatrix}0&0\\2&1\end{pmatrix}$ has rank 1, the lost direction runs along the arm, and a $10\,\mathrm{N}$ force along it needs $J^\top(10, 0) = (0, 0)$. P2's $6\times2$ $J_s$ keeps rank 2 at every $\theta$, and a tool point $0.5\,\mathrm{m}$ from the tip along $+y_b$, square to the forearm (toward $-x$ at the catalog pose), is singular at $\theta_2 = -26.6^\circ$ and $153.4^\circ$ instead: this singularity belongs to the tip-position task.
> - **Non-example**: $\theta = (0^\circ, 5^\circ)$, nearly straight. $\det J = 0.087$ and the rank is 2, so it is not singular, yet moving the tip $0.1\,\mathrm{m/s}$ straight out costs $2.56\,\mathrm{rad/s}$ of joint rate, $16$ times the $0.158$ the catalog pose needs. Singularity is yes or no; how close a pose comes is what the ellipsoid below measures.

- The **manipulability ellipsoid** is the image of the unit ball of joint velocities under
  $J$; its axes are the singular values ([[02-foundations/linear-algebra|SVD]]). Long axis
  = easy direction, short axis = hard; at a singularity one axis collapses to zero.
  The force ellipsoid is its reciprocal twin — directions that are hard to move are easy
  to hold force against, and vice versa.

> **Manipulability ellipsoid, defined.** The **manipulability ellipsoid** is *a set of tool velocities attached to one configuration*: the image under $J(\theta)$ of every joint-rate vector of unit length. Two conditions define it. **Unit joint rates**: $\|\dot\theta\| = 1$ in the Euclidean norm, which weighs every joint alike, so changing one joint's units reshapes it. **One configuration**: $J$ is frozen at the $\theta$ being judged. When $J$ has full rank $m$ the image is the ellipsoid written below; at a singularity it degenerates, into a segment for P2 (MR §5.4).
>
> $$\bigl\{v :\ v^\top (JJ^\top)^{-1}v = 1\bigr\}, \qquad \text{semi-axes } \sigma_i(J) = \sqrt{\lambda_i(JJ^\top)}, \qquad \mu_1 = \sigma_{\max}/\sigma_{\min}$$
>
> where $v$ is the task velocity and $\lambda_i$ are the eigenvalues of $JJ^\top$; the set has this form because, for a square invertible $J$ like P2's, $v = J\dot\theta$ turns $\dot\theta^\top\dot\theta = 1$ into $v^\top (JJ^\top)^{-1}v = 1$, so the axes point along the eigenvectors of $JJ^\top$. $\mu_1 \ge 1$ is MR's isotropy measure, infinite at a singularity; its square is the condition number of $JJ^\top$, and $\mu_1$ itself is the condition number $\kappa_2(J) = \sigma_{\max}/\sigma_{\min}$ of [[02-foundations/linear-algebra|1. Linear Algebra §3]], which §4.5.2 there evaluates at $2.618$ on this same pose. This page writes $\mu_1$ throughout.
>
> - **Example**: P2 at the catalog pose: semi-axes $1.618$ and $0.618$, $\mu_1 = 2.618$. Nearer straight, $\mu_1 = 14.2$ at $(0^\circ, 20^\circ)$ and $57.3$ at $(0^\circ, 5^\circ)$.
> - **Non-example**: the force ellipsoid, $\{f :\ \|J^\top f\| = 1\}$. It has the same axes and reciprocal semi-axes, $0.618$ along the long velocity axis and $1.618$ along the short one, so reading the long velocity axis as the strong direction swaps the two. A pose chosen for pressing on the panel should be judged by the force ellipsoid.

<svg viewBox="0 0 560 190" style="max-width:100%;height:auto" role="img" aria-label="P2's manipulability ellipse at θ2 = 90° (semi-axes 1.62 and 0.62) and at θ2 = 20° (2.20 and 0.16), drawn at 0.4 of the arm's scale">
  <ellipse cx="103.0" cy="92.0" rx="37.5" ry="14.3" transform="rotate(31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="51.1" ry="3.6" transform="rotate(78.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90&#176; &#8212; well conditioned</tspan></text><text x="355" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 20&#176; &#8212; nearing a singularity</tspan></text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; ratio 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; ratio 14</text>
  </g>
</svg>

The manipulability ellipse of P2 at the catalog pose and with the elbow closed to $\theta_2 = 20^\circ$, drawn centred on the tip at $0.4$ of the arm's scale: $\sigma = 1.62$ and $0.62$ ($\mu_1 = 2.6$) against $2.20$ and $0.16$ ($\mu_1 = 14$). As the arm straightens the ellipse flattens, one direction staying easy while the other needs ever larger joint rates, and at $\theta_2 = 0^\circ$ it collapses to a segment.

**Wiki connections**: force-feedback teleoperation, gravity compensation and
compliant control live on $\tau = J^\top \mathcal{F}$ ([[01-canonical-papers/notes/4-vla/act|ALOHA]] itself mirrors leader joints to follower joints directly); singularity awareness is why the raw
outputs of VLA (vision-language-action) policies pass through safety filters on real arms.

### Self-check

1. Compute $J$ at $\theta = (90°, 90°)$ and its determinant.
2. Derive $\tau = J^\top \mathcal{F}$ again from power conservation without looking.
3. The 2R arm is at $\theta_2 = 5°$. Qualitatively, what happens if the task demands tip
   motion along the arm's axis? Perpendicular to it?
4. Why do the manipulability and force ellipsoids have reciprocal axes?

> [!tip]- Answers
> 1. $s_1 = 1, c_1 = 0, s_{12} = \sin 180° = 0, c_{12} = -1$, so $J = \begin{pmatrix}-1 & 0\\ -1 & -1\end{pmatrix}$ and $\det J = 1$. Still nonsingular — consistent with $\det J = L_1L_2\sin\theta_2 = \sin 90° = 1$.
> 2. Power must match at both ends: $\dot\theta^\top\tau = \mathcal{V}^\top\mathcal{F}$. Substituting $\mathcal{V} = J\dot\theta$ gives $\dot\theta^\top\tau = \dot\theta^\top J^\top\mathcal{F}$ for *all* $\dot\theta$, hence $\tau = J^\top\mathcal{F}$.
> 3. Motion along the arm's own axis is the nearly-singular direction: $\det J = \sin 5° \approx 0.087$ and the smallest singular value is $\approx 0.04$, so producing that tip velocity demands more than an order of magnitude more joint speed than at the catalog pose ($2.56$ against $0.158\,\mathrm{rad/s}$ for $0.1\,\mathrm{m/s}$) — often beyond joint limits. Perpendicular motion is unaffected and behaves normally.
> 4. Velocities are amplified by the singular value $\sigma$ in each principal direction; by $\tau = J^\top\mathcal{F}$ the force transmitted in that same direction scales as $1/\sigma$. Directions that are easy to move are therefore hard to hold force in, and vice versa — the two ellipsoids are reciprocal.

### Problem set · 과제

Tier A. Using **P2** from [[02-foundations/lab-plants|0.6]], at the catalog pose $\theta=(0^\circ,90^\circ)$ and the other pose each item names. The arm's mass and $\Lambda$ are [[02-foundations/manipulator-kinematics-dynamics|10]]'s, already read; this page is velocity and statics.

1. **Draw.** The picture above with the elbow closed to $\theta=(0^\circ,30^\circ)$, nearer the straight arm: base at the origin, elbow at $(1,0)$, tip at $(1.866,\ 0.5)$. Draw Jacobian column 1 as the tip velocity for $\dot\theta=(1,0)$ and column 2 as the tip velocity for $\dot\theta=(0,1)$, both as arrows at the tip, the manipulability ellipse, and a commanded tip velocity of $0.25\,\mathrm{m/s}$ straight away from the base with the joint rates it needs. Write the two columns as vectors.
2. **Derive.** The other elbow of the same tip, branch B $=(90^\circ,-90^\circ)$ of [[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6]]: elbow at $(0,1)$, forearm along $+x$. (a) $J$ from the two arrows at the tip, and $\det J$. (b) $J^{-1}$, compared with $J$. (c) The joint rates for $v=(0,-0.25)\,\mathrm{m/s}$: which joint moves? (d) $\tau=J^\top F$ for the $10\,\mathrm{N}$ press $F=(0,-10)\,\mathrm{N}$ and for $F=(2,-5)\,\mathrm{N}$, against $(-10,0)$ and $(-7,-2)$ at the catalog pose. (e) Back at the catalog pose, press ch.2's upright face instead: the tool pushes $F=(10,0)\,\mathrm{N}$ into it. Give $\tau$ and say why the elbow now carries load.
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
> - Draw P2 to scale first: base at the origin, elbow at $(1,0)$, forearm at $30^\circ$ to the tip at $(1.866,\ 0.5)$.
> - Column $i$ is the tip velocity when only joint $i$ turns at $1\,\mathrm{rad/s}$: an arrow perpendicular to the line from joint $i$ to the tip and as long as that line — $1.932$ from the base for column 1, the unit forearm for column 2. Label each arrow with its vector.
> - Anchor both columns at the tip. Drawing a column from the base is the standard way this figure goes wrong: a Jacobian column is a velocity of the tip.
> - The manipulability ellipse centred on the tip, the image of the unit circle of joint rates, with semi-axes equal to the singular values, $2.163$ and $0.231$ here against $1.618$ and $0.618$ in the picture above. Draw it thin: $\mu_1=9.36$.
> - Mark the base-to-tip line through the tip: the ellipse's short axis lies within a few degrees of it, so the radial direction is the one the arm moves in worst.
> - The commanded velocity as its own arrow out of the tip along that line, in a different line weight from the columns, with $\dot\theta=J^{-1}v$ written beside it.

> [!tip]- Solutions
> 1. Column 1 is the shoulder-only velocity: perpendicular to the base-to-tip line and as long as it, $(-0.5,\ 1.866)$, length $1.932$. Column 2 is the elbow-only velocity, perpendicular to the forearm at $30^\circ$: $(-0.5,\ 0.866)$, unit length. $\det J=\sin30^\circ=0.5$. The ellipse has semi-axes $2.163$ and $0.231$, $\mu_1=9.36$ against $2.618$ at the catalog pose; its long axis points at $108^\circ$, its short axis at $18^\circ$, close to the base-to-tip line at $15^\circ$. Moving the tip $0.25\,\mathrm{m/s}$ straight out, along $(0.966,\ 0.259)$, needs $\dot\theta=J^{-1}v=(0.483,\ -0.966)\,\mathrm{rad/s}$, $2.7$ times the $(0.177,\ -0.354)$ the same request needs at the catalog pose: closer to straight, the radial direction is the expensive one.
> 2. (a) Shoulder only: the tip $(1,1)$ is still $\sqrt2$ from the base, so column 1 is $(-1,1)$ as at the catalog pose — column 1 depends only on where the tip is. Elbow only: the forearm now points along $+x$ from $(0,1)$, so the tip moves perpendicular to it, column 2 $=(0,1)$. $J=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$ and $\det J=(-1)(1)-(0)(1)=-1$: the same size as at the catalog pose and the opposite sign, because the elbow is bent the other way ($\sin\theta_2=-1$). (b) $J^{-1}=\frac{1}{-1}\begin{pmatrix}1&0\\-1&-1\end{pmatrix}=\begin{pmatrix}-1&0\\1&1\end{pmatrix}=J$: this $J$ is its own inverse, $J^2=I$. (c) $\dot\theta=J^{-1}v=(0,\ -0.25)\,\mathrm{rad/s}$: only the elbow turns, because with the forearm horizontal the elbow alone moves the tip straight down; the catalog pose needed both joints for the same $v$. (d) $J^\top=\begin{pmatrix}-1&1\\0&1\end{pmatrix}$. The press gives $\tau=(-10,\ -10)\,\mathrm{N{\cdot}m}$: both joints load, where at the catalog pose only the shoulder did, because the push is now perpendicular to the forearm, $1\,\mathrm{m}$ from the elbow. $F=(2,-5)$ gives $\tau=(-2-5,\ -5)=(-7,\ -5)\,\mathrm{N{\cdot}m}$: the shoulder's $-7$ is the catalog pose's again, since it depends only on column 1. (e) With the catalog $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$, $\tau=J^\top(10,0)=(-10,\ -10)\,\mathrm{N{\cdot}m}$. The push is horizontal, perpendicular to the upright forearm at $1\,\mathrm{m}$ from the elbow, so the elbow carries $10\,\mathrm{N{\cdot}m}$; about the shoulder its lever is the tip's height, $1\,\mathrm{m}$, so the shoulder carries $10\,\mathrm{N{\cdot}m}$ as well.
> 3. $J$ blanks: `((-s1-s12, -s12), (c1+c12, c12))`. Inverse: `th1d = (J[1][1]*0 - J[0][1]*vy)/det`, `th2d = (-J[1][0]*0 + J[0][0]*vy)/det`. Lecture pair: live $\approx(0.999,\ 0.500)$, frozen $\approx(0.878,\ 0.521)$. Live at $T=0.05$: $\approx(0.997,\ 0.501)$ — still millimetre-scale. Integrator class. Frozen error is independent of $T$ (joint rates are constant), so it is not a step-size artefact.

## 한국어

**핵심 질문**: 관절 속도는 말단 속도로, 힘은 그 반대로 어떻게 옮겨지는가?

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 야코비안은 조작 층의 국소 지도이고, 그 전치를 통해 접촉·힘 층으로 들어가는 첫걸음이다. "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계(명령한 말단 속도에 필요한 관절 속도), *접촉을 감지하는* 단계(관절 토크에서 거꾸로 읽는 말단 힘), *끼움을 수행하는* 단계(누르기에 드는 토크)를 받친다. 이 페이지의 칩은 [[physical-ai-map|피지컬 AI 지도]]의 조작 띠에 있다. 이것이 없으면 운동도 힘도 소리 없이 틀린다. 카탈로그의 평면 2링크 팔 **P2**([[02-foundations/lab-plants|0.6]])를 $0.5\,\mathrm{m}$ 아래로 옮길 때 시작의 $J$를 고정하면 말단이 $x$로 $12\,\mathrm{cm}$ 벗어나 끝나고(§2), 손목 센서의 $\mathcal{F}_b$에 $J_s^\top$를 곱하면 $10\,\mathrm{N}$ 누르기가 어느 관절에도 부하를 주지 않는 것처럼 나오며(§3), 곧게 편 팔 근처에서는 $0.1\,\mathrm{N{\cdot}m}$의 토크 오차가 팔 방향 힘 $2.6\,\mathrm{N}$을 숨긴다. 카탈로그 자세라면 $0.16\,\mathrm{N}$이다(§3). 뒤 페이지들이 절 단위로 이 위에 선다. [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]는 '대상으로 한 번 끝까지', §3, §4를 $\tau = J^\top\mathcal{F}$ 위에, [[04-robotics/navigation-mobile-manipulation|16. 내비게이션·모바일 매니퓰레이션 §1–§3]]은 도달성과 베이스 배치를 §4의 타원체 위에, [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 §5]]는 리타기팅을 §4 위에, [[04-robotics/modern-robotics/ch11-robot-control|MR 11장]]은 '대상으로 한 번 끝까지'를 §3 위에 세우고, [[04-robotics/capstone-panel-contact|26. 캡스톤]]은 '대상으로 한 번 끝까지'의 3단계와 5단계에서 쓴다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 2, 로보틱스 12–15회차다. 이 페이지를 마치면 P2의 야코비안 열을 말단 속도로 그리고, 관절 속도와 유지 토크를 계산하고, 특이점을 알아보고 누르는 자세를 힘 타원체로 판정하고, 분해 속도 루프를 돌릴 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 네 번쯤, 로보틱스 12–15회차다. **첫 회차:** 이 페이지의 대상, 그림, '대상으로 한 번 끝까지'를 손으로 한다. 말단의 두 화살표에서 읽는 $J$, $J^{-1}$, $v = (0,-0.25)\,\mathrm{m/s}$에 필요한 관절 속도, $10\,\mathrm{N}$ 누르기의 토크다. 이어서 $J$가 $\theta$의 함수가 되고, 분해 속도 실행이 왜 $J$를 다시 계산해야 하는지 보여 주는 §2를 읽는다. 끝으로 '대상으로 한 번 끝까지'를 답을 가리고 다시 한다. **둘째 회차:** §1(프레임을 명시한 $J_s$, $J_b$, 그리고 $2\times2$가 그 안에 들어 있는 방식), 6차원 검산과 힘 감지 숫자가 있는 §3, §4의 특이점과 타원체. **셋째 회차:** 스스로 점검과 과제 1–2. **넷째 회차:** 과제 3, 실습. 접힌 *더 깊이* 메모는 두 번째 읽기다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그의 평면 2링크 팔이다. 링크 길이는 1, 어깨는 원점에 있고, $\theta_1$은 $+x$축에서 재며 엘보 각 $\theta_2$는 링크 1에 대해 잰다. 회전 관절 둘인 "2R" 팔이다. 팔은 카탈로그 자세 $\theta = (0^\circ, 90^\circ)$에 서 있다. 엘보는 $(1,0)$, 전완은 곧장 위, 말단은 $(1,1)$이다. 프레임은 3장과 4장의 것이다. 공간 프레임 $\{s\}$는 어깨에, 물체 프레임 $\{b\}$는 말단에 있고 $x_b$는 전완 방향이다.

**누르기.** 도구가 말단 아래에 평평하게 놓인 패널을 $F = (0,-10)\,\mathrm{N}$으로 곧장 아래로 누른다(전완은 그림 평면 바깥, 패널 앞쪽으로 지나가므로 패널에 닿는 것은 말단뿐이다). [[02-foundations/manipulator-kinematics-dynamics|10]]과 [[04-robotics/force-compliance-control|13]]이 쓰는 방향이다. 2장의 수직 패널(면 $x = 1$)은 같은 패널을 직각으로 돌린 것이고, 과제 2가 그 면을 누른다. $F$는 도구가 패널에 가하는 힘이고, 패널은 도구를 $(0, +10)\,\mathrm{N}$으로 되민다.

*범위: 이 페이지는 평면에서의 속도 야코비안과 6차원 사상으로서의 속도 야코비안, 같은 행렬을 쓰는 정역학, 특이점과 두 타원체를 P2 위에서 가르친다. 팔 자신의 질량은 [[02-foundations/manipulator-kinematics-dynamics|10]]과 [[04-robotics/modern-robotics/ch08-dynamics|8장]], 역기구학은 [[04-robotics/modern-robotics/ch06-inverse-kinematics|6장]]에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 314" style="max-width:100%;height:auto" role="img" aria-label="카탈로그 자세의 P2 말단에 야코비안의 두 열 (−1, 1)과 (−1, 0) m/s, 명령 속도 (0, −0.25) m/s, 반축이 1.618과 0.618인 가조작성 타원을 그리고, 오른쪽에 누르기를 떼어 그린 그림: 도구가 패널을 (0, −10) N으로 누르고 패널이 도구를 (0, +10) N으로 되민다.">
  <defs><marker id="mr05hdK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker><marker id="mr05hdvK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <path d="M78 34 L74.3 34.1 L70.7 34.3 L67.3 34.6 L64 35.1 L60.9 35.6 L57.9 36.4 L55.1 37.2 L52.4 38.2 L49.9 39.3 L47.6 40.5 L45.4 41.9 L43.4 43.3 L41.6 44.9 L39.9 46.6 L38.5 48.5 L37.2 50.4 L36.1 52.5 L35.1 54.6 L34.4 56.9 L33.8 59.3 L33.5 61.7 L33.3 64.3 L33.3 67 L33.5 69.7 L33.8 72.6 L34.4 75.5 L35.1 78.5 L36.1 81.6 L37.2 84.8 L38.5 88 L39.9 91.3 L41.6 94.7 L43.4 98.1 L45.4 101.5 L47.6 105.1 L49.9 108.6 L52.4 112.2 L55.1 115.9 L57.9 119.5 L60.9 123.2 L64 127 L67.3 130.7 L70.7 134.5 L74.3 138.2 L78 142 L81.8 145.8 L85.8 149.5 L89.9 153.3 L94.1 157 L98.4 160.8 L102.8 164.5 L107.3 168.1 L112 171.8 L116.7 175.4 L121.5 178.9 L126.3 182.5 L131.3 185.9 L136.3 189.3 L141.3 192.7 L146.5 196 L151.6 199.2 L156.9 202.4 L162.1 205.5 L167.4 208.5 L172.7 211.4 L178 214.3 L183.3 217 L188.7 219.7 L194 222.3 L199.3 224.7 L204.6 227.1 L209.9 229.4 L215.1 231.5 L220.4 233.6 L225.5 235.5 L230.7 237.4 L235.7 239.1 L240.7 240.7 L245.7 242.1 L250.5 243.5 L255.3 244.7 L260 245.8 L264.7 246.8 L269.2 247.6 L273.6 248.4 L277.9 248.9 L282.1 249.4 L286.2 249.7 L290.2 249.9 L294 250 L297.7 249.9 L301.3 249.7 L304.7 249.4 L308 248.9 L311.1 248.4 L314.1 247.6 L316.9 246.8 L319.6 245.8 L322.1 244.7 L324.4 243.5 L326.6 242.1 L328.6 240.7 L330.4 239.1 L332.1 237.4 L333.5 235.5 L334.8 233.6 L335.9 231.5 L336.9 229.4 L337.6 227.1 L338.2 224.7 L338.5 222.3 L338.7 219.7 L338.7 217 L338.5 214.3 L338.2 211.4 L337.6 208.5 L336.9 205.5 L335.9 202.4 L334.8 199.2 L333.5 196 L332.1 192.7 L330.4 189.3 L328.6 185.9 L326.6 182.5 L324.4 178.9 L322.1 175.4 L319.6 171.8 L316.9 168.1 L314.1 164.5 L311.1 160.8 L308 157 L304.7 153.3 L301.3 149.5 L297.7 145.8 L294 142 L290.2 138.2 L286.2 134.5 L282.1 130.7 L277.9 127 L273.6 123.2 L269.2 119.5 L264.7 115.9 L260 112.2 L255.3 108.6 L250.5 105.1 L245.7 101.5 L240.7 98.1 L235.7 94.7 L230.7 91.3 L225.5 88 L220.4 84.8 L215.1 81.6 L209.9 78.5 L204.6 75.5 L199.3 72.6 L194 69.7 L188.7 67 L183.3 64.3 L178 61.7 L172.7 59.3 L167.4 56.9 L162.1 54.6 L156.9 52.5 L151.6 50.4 L146.5 48.5 L141.3 46.6 L136.3 44.9 L131.3 43.3 L126.3 41.9 L121.5 40.5 L116.7 39.3 L112 38.2 L107.3 37.2 L102.8 36.4 L98.4 35.6 L94.1 35.1 L89.9 34.6 L85.8 34.3 L81.8 34.1 Z" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="2 3" opacity="0.75"><line x1="186" y1="142" x2="37.4" y2="50.1"/><line x1="186" y1="142" x2="221.1" y2="85.2"/></g>
  <polyline points="78,250 186,250 186,142" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.3"/>
  <circle cx="78" cy="250" r="4.5" fill="currentColor" fill-opacity="0.6"/>
  <circle cx="186" cy="250" r="3.5" fill="currentColor" fill-opacity="0.6"/>
  <g stroke="currentColor" stroke-width="2.4" marker-end="url(#mr05hdK)"><line x1="186" y1="142" x2="78" y2="34"/><line x1="186" y1="142" x2="78" y2="142"/></g>
  <line x1="186" y1="142" x2="186" y2="169" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr05hdvK)"/>
  <circle cx="186" cy="142" r="4" fill="currentColor"/>
  <line x1="350" y1="14" x2="350" y2="290" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <circle cx="382" cy="220" r="4" fill="currentColor"/>
  <line x1="360" y1="266" x2="408" y2="266" stroke="currentColor" stroke-width="1.6"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="366" y1="266" x2="360" y2="273"/> <line x1="374" y1="266" x2="368" y2="273"/> <line x1="382" y1="266" x2="376" y2="273"/> <line x1="390" y1="266" x2="384" y2="273"/> <line x1="398" y1="266" x2="392" y2="273"/></g>
  <path d="M373 227 L379 227 L379 254 L383.5 254 L376 265 L368.5 254 L373 254 Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <line x1="391" y1="264" x2="391" y2="226" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr05hdvK)"/>
  <g font-size="11" fill="currentColor">
    <text x="78" y="25" text-anchor="middle">열 1 = (−1, 1)</text>
    <text x="142" y="158" text-anchor="middle">열 2 = (−1, 0)</text>
    <text x="196" y="169">v = (0, −0.25)</text>
    <text x="196" y="184">θ̇ = (−0.25, 0.25) rad/s</text>
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
    <text x="362" y="203" font-size="12">누르기, 떼어 그림</text>
    <text x="414" y="224">F = (0, −10) N</text>
    <text x="414" y="238" opacity="0.85">도구가 패널에 (윤곽선)</text>
    <text x="414" y="256">(0, +10) N</text>
    <text x="414" y="270" opacity="0.85">패널이 도구에 (가는 선)</text>
    <text x="414" y="288">τ = JᵀF = (−10, 0) N·m</text>
    <text x="12" y="304" opacity="0.85">말단의 화살표는 속도다(1 m/s를 1 m로). 누르는 힘과 그 반작용은 오른쪽에 떼어 그렸다.</text>
  </g>
</svg>

카탈로그 자세 $\theta = (0^\circ, 90^\circ)$의 장치 **P2**를 축척대로 그리고 속도를 모두 말단 $(1,1)$에 붙였다. 야코비안의 두 열 $(-1,1)$과 $(-1,0)\,\mathrm{m/s}$는 어깨만, 또는 엘보만 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도이고, 가는 화살표인 명령 속도 $v = (0,-0.25)\,\mathrm{m/s}$에는 $\dot\theta = J^{-1}v = (-0.25,\ 0.25)\,\mathrm{rad/s}$가 필요하며, 가조작성 타원은 관절 속도 단위원의 상으로 반축이 $1.618$과 $0.618$이다. 오른쪽에는 자유물체도처럼([[02-foundations/basic-mechanics|0.6.1 §2]]) 누르기를 떼어 그렸다. 도구가 패널을 $F = (0,-10)\,\mathrm{N}$으로 누르고(이것이 $\tau = J^\top F$가 받는 힘이다), 패널이 도구를 $(0,+10)\,\mathrm{N}$으로 되밀며, 같은 $J$가 $F$를 $\tau = (-10,\ 0)\,\mathrm{N{\cdot}m}$로 보낸다.

### 대상으로 한 번 끝까지 · Worked case

여기 나오는 것은 모두 이 자세에서 한 번 만난 것이다. 야코비안과 $\tau = J^\top F$는 [[02-foundations/manipulator-kinematics-dynamics|10. §1]]에서, 특이값은 [[02-foundations/linear-algebra|1. 선형대수 §4.5.2]]에서 구했다. 그래서 이것은 되짚기이고, 이 장이 읽는 방식, 곧 말단의 화살표로 다시 한다. 이 장이 더하는 것은 그 뒤에 온다. 프레임(§1), $\theta$의 함수로서의 $J$와 그것을 다시 계산해야 하는 이유(§2), 6차원 사상으로서의 정역학(§3), 특이 자세(§4)다.

**1단계 — 두 열은 말단의 화살표다.** $J$의 열 $i$는 관절 $i$만 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도다. 관절 하나를 돌리면 말단은 그 관절을 중심으로 원을 그리므로, 화살표는 관절에서 말단까지의 선에 수직이고 그 선만큼 길다. 어깨만, $\dot\theta = (1,0)$: 말단이 베이스에서 $(1,1)$ 방향으로 $\sqrt2$ 떨어져 있으므로 열 1은 $(-1,1)$이다. 엘보만, $\dot\theta = (0,1)$: 전완이 길이 1로 $+y$를 가리키므로 열 2는 $(-1,0)$이다. 관절 속도가 열에 가중치를 주므로 둘을 나란히 세우면

$$J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}, \qquad \det J = (-1)(0) - (-1)(1) = 1$$

**2단계 — 뒤집어서 명령 속도를 푼다.** $\det J = 1$이므로 $2\times2$ 역행렬(대각을 맞바꾸고, 비대각의 부호를 바꾸고, 행렬식으로 나눈다)은 $J^{-1} = \begin{pmatrix}0&1\\-1&-1\end{pmatrix}$이다. 말단을 $v = (0,-0.25)\,\mathrm{m/s}$로 곧장 내리라고 명령하면, $v = J\dot\theta$이므로 관절 속도는

$$\dot\theta = J^{-1}v = \begin{pmatrix}0&1\\-1&-1\end{pmatrix}\begin{pmatrix}0\\-0.25\end{pmatrix} = (-0.25,\ 0.25)\ \mathrm{rad/s}$$

이다. 어깨는 시계 방향으로, 엘보는 반시계 방향으로 같은 빠르기로 돈다. 이 순간 전완은 전혀 돌지 않고, 말단은 엘보와 똑같이 곧장 아래로 움직인다. 화살표로 검산하면 $-0.25\,(-1,1) + 0.25\,(-1,0) = (0,\ -0.25)$다.

**3단계 — 누르기, 일률로.** 팔 자신의 무게는 빼 두고(그 유지 토크는 따로 더한다, §3) 팔이 이 자세를 아주 천천히 지나간다고 하자. 무게를 뺀 팔이 그렇게 천천히 움직이면 에너지를 저장하지 않으므로, 모터가 넣는 일률이 도구가 내는 일률과 같다. 모든 $\dot\theta$에 대해 $\tau^\top\dot\theta = F^\top v = F^\top J\dot\theta$이고, 따라서 $\tau = J^\top F$다(조건은 §3이 밝힌다). $J^\top$의 행이 $J$의 열이므로 누르기에 대해

$$\tau = J^\top F = \begin{pmatrix}-1&1\\-1&0\end{pmatrix}\begin{pmatrix}0\\-10\end{pmatrix} = (-10,\ 0)\ \mathrm{N{\cdot}m}$$

이다. 어깨가 누르기 전체를 $1\,\mathrm{m}$ 지렛대로 지고, 엘보는 아무것도 지지 않는다. 미는 힘이 전완을 따라 엘보 축을 곧장 지나가기 때문이다. 화살표로 읽으면, 엘보의 말단 속도인 열 2 $(-1,0)$이 $F$와 수직이므로 $F$는 엘보의 운동에 일을 하지 않는다. 그 내적 0이 토크 0이다.

### 1. 야코비안 — 프레임을 명시해서

'대상으로 한 번 끝까지'의 $J$는 평면에서의 말단 속도를 준다. 도구의 방향까지 돌리거나 손목 센서를 읽는 제어기에는 더 많은 것이 필요하다. 도구의 강체 속도 전체, 곧 이름 붙은 프레임에서 쓴 여섯 수 $(\omega, v)$인 트위스트([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3]])와, 그것을 돌려주는 야코비안이다. 야코비안은 관절 속도마다 제 몫의 운동 열을 하나씩 더한다고 말한다.

$$\mathcal{V}_s = J_s(\theta)\,\dot\theta \qquad \text{또는} \qquad \mathcal{V}_b = J_b(\theta)\,\dot\theta$$

열 $i$는 '대상으로 한 번 끝까지'에서처럼 관절 $i$만 단위 속도로 움직일 때의 말단 트위스트다. 다만 이제는 프레임이 대상의 일부다. $J_s$는 공간 프레임의 트위스트를, $J_b$는 물체 프레임의 트위스트를 주고, 둘은 $J_s = [\text{Ad}_{T_{sb}}]\,J_b$로 이어진다([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §4]]).

> **공간 야코비안과 물체 야코비안의 정의.** **공간 야코비안**(space Jacobian) $J_s(\theta)$와 **물체 야코비안**(body Jacobian) $J_b(\theta)$는 *컨피규레이션의 함수인 행렬*이고 크기는 $6\times n$이다. 한 대상을 두 프레임으로 쓴 것이다. 정의 조건 셋. 둘 다 **고정된 $\theta$에서 관절 속도에 선형**이다. 여러 관절이 함께 움직이면 열들의 가중합이 된다. **$i$번째 열은 현재 컨피규레이션에서 관절 $i$의 스크류 축**이다. $\dot\theta_i = 1$이고 나머지 속도가 모두 0일 때 생기는 트위스트다. 그리고 **프레임이 대상의 일부**다. $J_s$는 $\{s\}$의 트위스트를, $J_b$는 $\{b\}$의 트위스트를 준다(MR §5.1).
>
> $$\mathcal{V}_s = J_s\dot\theta,\quad \mathcal{V}_b = J_b\dot\theta, \qquad J_{s,i}(\theta) = [\mathrm{Ad}_{e^{[\mathcal{S}_1]\theta_1}\cdots e^{[\mathcal{S}_{i-1}]\theta_{i-1}}}]\,\mathcal{S}_i, \qquad J_s = [\mathrm{Ad}_{T_{sb}}]\,J_b$$
>
> 여기서 $\mathcal{S}_i$는 4장의 홈 스크류이고, 수반 사상이 관절 $i$의 축을 관절 $1$부터 $i-1$까지가 옮겨 놓은 자리로 데려간다. 그래서 $J_s$의 $i$번째 열은 그 앞의 관절에만 의존한다.
>
> - **예**: 카탈로그 자세의 P2. $\theta_1 = 0$이라 두 축이 홈의 자리에 그대로 있으므로 $J_s$의 열은 $(0,0,1;\,0,0,0)$과 $(0,0,1;\,0,-1,0)$이다. $J_b$의 열은 $(0,0,1;\,1,1,0)$과 $(0,0,1;\,0,1,0)$이고, $[\mathrm{Ad}_{T_{sb}}]J_b = J_s$다.
> - **예, 수반 사상이 실제로 쓰이는 경우**: $\theta = (90^\circ, 90^\circ)$의 P2. 관절 1이 엘보 축을 $(1,0)$에서 $(0,1)$로 옮겼으므로 $J_s$의 열 2는 $(0,1)$을 지나는 축의 스크류 $(0,0,1;\,1,0,0)$이고, 4장의 홈 스크류 $\mathcal{S}_2 = (0,0,1;\,0,-1,0)$이 아니다. [[04-robotics/modern-robotics/ch04-forward-kinematics|4장 §1]]의 비예는 바로 이 스크류를 지수 곱 공식에 넣어 말단을 $2\,\mathrm{m}$ 벗어나게 한다. 야코비안의 열로서는 이것이 맞다. 열은 앞 관절이 그 자리로 옮겨 놓은 축이기 때문이다.
> - **비예**: $J_s$의 아래 세 행을 말단 속도로 읽는 것. 열 1의 선형부는 $(0,0,0)$인데, 어깨가 $1\,\mathrm{rad/s}$로 돌면 말단은 $(-1,1)\,\mathrm{m/s}$로 움직인다. 공간 트위스트의 $v$는 $\{s\}$ 원점에 있는 물체 점의 속도이기 때문이다([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3]]). 말단 속도는 $R_{sb}v_b$이고, 그것이 $(-1,1)$과 $(-1,0)$, 곧 '대상으로 한 번 끝까지'의 $J$의 열이다. 그 행들 위에 세운 분해 속도 루프는 도구가 아니라 베이스에 있는 점을 조종한다.

**$2\times2$가 그 안에 들어 있는 방식.** '대상으로 한 번 끝까지'의 $J = \partial p/\partial\theta$는 [[02-foundations/calculus-backprop|2. 미적분]]의 야코비안, 곧 말단의 두 좌표의 도함수다. $J_s$와 $J_b$는 어떤 여섯 좌표의 도함수도 아니지만(그 열은 스크류 축이다) 그것을 품고 있다. 말단 속도는 $\dot p = R_{sb}v_b = v_s + \omega_s \times p$이므로, $J_b$의 선형 행들을 $\{s\}$로 돌리면 '대상으로 한 번 끝까지'의 열이 나온다. 카탈로그 자세에서 $R_{sb} = R_z(90^\circ)$는 $(1,1,0)$을 $(-1,1,0)$으로, $(0,1,0)$을 $(-1,0,0)$으로 돌린다. 1단계의 두 화살표다.

> [!note]- 더 깊이 · Deeper
> **열 하나씩, 그리고 "고정된 컨피규레이션에서"인 이유.** 컨피규레이션을 고정하고 관절 하나만 움직이면, 선언한 프레임에서 도구의 순간 강체 운동이 열 하나다. 여러 관절이 동시에 움직이면 열들의 가중합이 되는데, 그 컨피규레이션에서 사상이 선형이기 때문이다. 관절이 움직이면 도구에 대한 축과 지렛대 팔이 달라지므로 야코비안을 다시 계산해야 한다. 상수 야코비안은 작은 국소 변위를 예측할 뿐 유한 운동을 예측하지 않는다(§2의 고정 실행이 그 값을 보여 준다). 순기구학은 자세를 갱신하고, 야코비안은 그 국소 민감도다.
>
> **행과 열.** 관절 속도가 $n$개이고 과제 속도가 $m$개의 수이면 $J$는 $m \times n$이다. 트위스트 전체에는 $6\times n$인 $J_s$나 $J_b$를 쓰고, 위치만의 과제에는 '대상으로 한 번 끝까지'의 $2\times2$ 같은 축소 야코비안을 쓴다. $J_s$의 각속도 행을 지우고 남은 것을 말단 속도로 읽으면 안 된다. 그 선형부는 $\{s\}$ 원점에 있는 점의 것이다. 위의 비예가 보여 준 그대로다.

### 2. 계산 예제 — 평면 2R 팔의 말단 야코비안

'대상으로 한 번 끝까지'는 한 자세에서 화살표 둘로 $J$를 읽었다. 팔은 거기 머물지 않고, 제어기는 팔이 어디 있든 $J$가 필요하다. 그래서 순기구학을 기호로 한 번 미분한다. 말단 위치(평면이므로 $2\times2$면 충분하다)는
$$x = L_1\cos\theta_1 + L_2\cos(\theta_1{+}\theta_2), \qquad y = L_1\sin\theta_1 + L_2\sin(\theta_1{+}\theta_2)$$
이고, 각 성분이 편미분 하나다. $x$의 둘째 항에 연쇄법칙을 쓰면 $\partial\cos(\theta_1{+}\theta_2)/\partial\theta_1 = -\sin(\theta_1{+}\theta_2)\cdot 1$이므로 $\partial x/\partial\theta_1 = -L_1\sin\theta_1 - L_2\sin(\theta_1{+}\theta_2)$이고, $\theta_2$는 그 항에만 나오므로 $\partial x/\partial\theta_2 = -L_2\sin(\theta_1{+}\theta_2)$다. $y$ 행은 $\sin \to \cos$로 바꾼 같은 계산이다. 각 행이 좌표 하나, 각 열이 관절 하나이므로 행 $(x, y)$, 열 $(\theta_1, \theta_2)$로 쌓으면:
$$J(\theta) = \begin{pmatrix} -L_1 s_1 - L_2 s_{12} & -L_2 s_{12} \\ L_1 c_1 + L_2 c_{12} & L_2 c_{12} \end{pmatrix}$$
여기서 $s_1 = \sin\theta_1$, $c_1 = \cos\theta_1$, $s_{12} = \sin(\theta_1{+}\theta_2)$, $c_{12} = \cos(\theta_1{+}\theta_2)$다. $L_1 = L_2 = 1$, $\theta = (0°, 90°)$에서는 $s_1 = 0$, $c_1 = 1$, $s_{12} = 1$, $c_{12} = 0$이 '대상으로 한 번 끝까지'의 $J$를 돌려준다. 그 열이 두 화살표였다. 일반적으로
$\det J = L_1 L_2 \sin\theta_2$: **팔이 완전히 뻗거나 접힐 때가 정확히 특이점이다**
($\theta_2 = 0°$ 또는 $180°$). 수학이 어디를 보라고 알려주면 기하적으로도 자명해진다. 뻗거나 접힌 팔에서는 두 화살표가 평행하다.

$J(\theta)$의 식이 있어야 제어기가 명령 속도를 한순간보다 오래 따라갈 수 있다.

> **분해 속도 제어의 정의.** **분해 속도 제어**(resolved-rate control)는 *명령한 도구 속도를 관절 운동으로 바꾸는 루프*이고, 한 번에 제어 주기 하나씩 돈다. 정의 조건 셋. **명령은 과제 속도다**: 여기서는 관절 목표가 아니라 말단 속도 $v$다. **현재 컨피규레이션에서 푼다**: 매 주기 팔이 지금 가진 관절에서 계산한 $J$로 $J(\theta_k)\,\dot\theta = v$를 푼다. **적분한다**: 관절 속도를 한 주기 $T$ 동안 유지해 관절 명령에 더한다.
>
> $$\dot\theta_k = J(\theta_k)^{-1}v, \qquad \theta_{k+1} = \theta_k + T\,\dot\theta_k$$
>
> 여기서 $J^{-1}$은 특이점(§4)에서 멀 때 존재하고, 정사각이 아닌 $J$에서는 유사역행렬이 된다(6장). 루프는 $\dot\theta = J(\theta)^{-1}v$에 대한 명시적 오일러([[02-foundations/lab-kernel|0.7]])이므로 오차의 원천이 둘, 스텝 $T$와 낡은 $J$다.
>
> - **예**: 카탈로그 자세의 P2에 $v = (0,-0.25)\,\mathrm{m/s}$를 $2\,\mathrm{s}$, $T = 0.01\,\mathrm{s}$로 준다. 말단은 $\approx(0.999,\ 0.500)$에서 끝나 명령한 $\Delta y = -0.50\,\mathrm{m}$에 대해 $x$ 드리프트가 $1\,\mathrm{mm}$ 미만이고, 관절은 $(-29.4^\circ,\ 112.1^\circ)$다.
> - **비예**: 시작의 $J$로 고정한 같은 루프. 관절 속도가 실행 내내 $(-0.25,\ 0.25)$에 머물러 $\theta_1 + \theta_2$가 $90^\circ$로 유지된다. 전완은 계속 서 있고, 말단은 $1\,\mathrm{m}$ 올린 엘보 원 $p = (\cos\theta_1,\ 1 + \sin\theta_1)$을 타고 $\approx(0.878,\ 0.521)$까지 간다. $x$ 오차 $12\,\mathrm{cm}$다. 상수 야코비안은 국소 사상이지 유한 운동 사상이 아니다.
> - **왜 중요한가**: 도구 속도를 내보내는 원격조작 핸들이나 정책은 이 루프를 거쳐 모터에 닿으므로 두 오차를 다 물려받는다. 낡은 $J$의 오차는 $T$를 줄여도 줄지 않는다(과제 3).

<svg viewBox="0 0 560 320" style="max-width:100%;height:auto" role="img" aria-label="P2가 카탈로그 자세에서 같은 명령 속도 (0, −0.25) m/s를 2 s 동안 따른 두 경로: 매 스텝 갱신한 J는 말단을 곧장 (0.999, 0.500)까지 내리고, 고정한 J는 1 m 올린 엘보 원을 따라 (0.878, 0.521)에서 끝나 x로 12 cm 벗어난다.">
  <defs><marker id="mr05rrk" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="0.8" opacity="0.25"><line x1="36.0" y1="226" x2="268.0" y2="226"/><line x1="60" y1="314.0" x2="60" y2="34.0"/></g>
  <polyline points="178.9,173.1 180.8,171.0 182.6,168.8 184.3,166.7 186.1,164.5 187.8,162.3 189.4,160.0 191.1,157.8 192.6,155.5 194.2,153.1 195.7,150.8 197.1,148.4 198.6,146.0 199.9,143.6 201.3,141.1 202.6,138.6 203.8,136.1 205.0,133.6 206.2,131.1 207.3,128.5 208.3,125.9 209.4,123.3 210.4,120.7 211.3,118.1 212.2,115.4 213.0,112.8 213.8,110.1 214.5,107.4 215.2,104.7 215.9,102.0 216.5,99.3 217.1,96.5 217.6,93.8 218.0,91.0 218.4,88.3 218.8,85.5 219.1,82.7 219.4,79.9 219.6,77.2 219.8,74.4 219.9,71.6 220.0,68.8 220.0,66.0 220.0,63.2 219.9,60.4 219.8,57.6 219.6,54.8 219.4,52.1 219.1,49.3 218.8,46.5 218.4,43.7" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
  <polyline points="60.0,226.0 220.0,226.0 220.0,66.0" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" opacity="0.18"/>
  <line x1="60.0" y1="66.0" x2="200.4" y2="142.7" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
  <circle cx="60.0" cy="66.0" r="3" fill="currentColor" fill-opacity="0.6"/>
  <polyline points="60.0,226.0 200.4,302.7 200.4,142.7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 4" stroke-linejoin="round" opacity="0.7"/>
  <polyline points="60.0,226.0 199.3,304.7 219.9,146.0" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
  <polyline points="220.0,66.0 220.0,70.0 220.0,74.0 220.0,78.0 220.0,82.0 220.0,86.0 220.0,90.0 220.0,94.0 220.0,98.0 220.0,102.0 219.9,106.0 219.9,110.0 219.9,114.0 219.9,118.0 219.9,122.0 219.9,126.0 219.9,130.0 219.9,134.0 219.9,138.0 219.9,142.0 219.9,146.0 219.9,146.0" fill="none" stroke="currentColor" stroke-width="1.8" marker-end="url(#mr05rrk)"/>
  <polyline points="220.0,66.0 220.0,70.0 219.8,74.0 219.6,78.0 219.2,82.0 218.8,85.9 218.2,89.9 217.6,93.9 216.8,97.8 216.0,101.7 215.0,105.6 214.0,109.4 212.9,113.3 211.6,117.1 210.3,120.9 208.9,124.6 207.4,128.3 205.8,132.0 204.1,135.6 202.3,139.2 200.4,142.7 200.4,142.7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#mr05rrk)"/>
  <circle cx="60.0" cy="226.0" r="4.5" fill="currentColor" fill-opacity="1"/>
  <circle cx="220.0" cy="226.0" r="3" fill="currentColor" fill-opacity="0.3"/>
  <circle cx="199.3" cy="304.7" r="3.5" fill="currentColor" fill-opacity="1"/>
  <circle cx="200.4" cy="302.7" r="3.5" fill="currentColor" fill-opacity="0.7"/>
  <circle cx="220.0" cy="146.0" r="5.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.8"><line x1="200.4" y1="160.0" x2="219.9" y2="160.0"/><line x1="200.4" y1="156.0" x2="200.4" y2="164.0"/><line x1="219.9" y1="156.0" x2="219.9" y2="164.0"/></g>
  <g font-size="11" fill="currentColor">
    <text x="230.0" y="70.0">시작 (0°, 90°)</text>
    <text x="229.9" y="146.0">목표 (1, 0.5)</text>
    <text x="225.9" y="164.0">12 cm</text>
    <text x="52" y="242" text-anchor="end" opacity="0.8">베이스</text>
    <text x="174.9" y="185.1" text-anchor="end" opacity="0.75">1 m 올린 엘보 원</text>
    <text x="68" y="62" opacity="0.75">중심 (0, 1)</text>
    <text x="312" y="240" opacity="0.8">축척대로, 옅은 팔은 시작 자세</text>
  </g>
  <line x1="300" y1="14" x2="300" y2="300" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="312" y="28" font-size="12">같은 명령, v = (0, −0.25) m/s로 2 s</text>
    <line x1="314" y1="52" x2="340" y2="52" stroke="currentColor" stroke-width="2.6"/>
    <text x="348" y="56">매 스텝 갱신한 J</text>
    <text x="348" y="74">말단 (0.999, 0.500)</text>
    <text x="348" y="92">θ = (−29.4°, 112.1°)</text>
    <line x1="314" y1="124" x2="340" y2="124" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 4" opacity="0.7"/>
    <text x="348" y="128">시작 자세의 J로 고정</text>
    <text x="348" y="146">관절 속도가 (−0.25, 0.25) rad/s로 고정</text>
    <text x="348" y="164">θ₁ + θ₂ = 90°: 전완이 서 있다</text>
    <text x="348" y="182">말단은 1 m 올린 엘보 원을 탄다</text>
    <text x="348" y="200">끝: (0.878, 0.521), x로 12 cm 벗어남</text>
  </g>
</svg>

상자의 두 실행을 카탈로그 자세에서 축척대로 그렸다. 매 스텝 $J$를 다시 계산하면 말단이 곧장 $(0.999,\ 0.500)$까지 내려가고, 고정한 $J$는 전완을 세운 채 말단이 $(0,1)$을 중심으로 $1\,\mathrm{m}$ 올린 엘보 원을 타고 $(0.878,\ 0.521)$까지 가게 해 $x$로 $12\,\mathrm{cm}$ 모자란다. $(0,1)$에서 그 말단까지 그은 점선 반지름은 링크 1과 평행한데, 고정한 $J$의 말단은 언제나 엘보를 곧장 $1\,\mathrm{m}$ 위로 옮긴 점이기 때문이다. 두 엘보는 $(0.87,\ -0.49)$ 근처, 서로 $1.4\,\mathrm{cm}$ 안에서 끝나므로 차이는 전부 전완이 어떻게 돌았느냐에 있다. 과제가 이 루프를 채우고, $T$를 바꾸는 것이 노브다.

### 3. 정역학 쌍대성 — 세 줄 유도

패널을 $10\,\mathrm{N}$으로 누르면 어깨에 $10\,\mathrm{N{\cdot}m}$이 들고 엘보에는 아무것도 들지 않는다('대상으로 한 번 끝까지' 3단계). 힘 제어기에는 이 사상이 모든 자세, 모든 렌치에 대해 필요하고, 접촉 감지기에는 거꾸로, 측정한 토크에서 도구의 힘으로 가는 방향이 필요하다. [[02-foundations/manipulator-kinematics-dynamics|10. §1]]이 P2의 $2\times2$ 경우를 유도했고, 여기서는 6차원 렌치에 대해 필요한 조건과 함께 쓴다.

손실 없는 기구의 양 끝에서 일률은 같아야 한다. 관절 쪽 일률은 $\dot\theta^\top \tau$,
말단 쪽 일률은 $\mathcal{V}^\top \mathcal{F}$다. 렌치 $\mathcal{F} = (m, f) \in \mathbb{R}^6$은 도구가 가하는 모멘트와 힘을 쌓은 것이고, 트위스트와의 짝 $\mathcal{V}^\top\mathcal{F} = \omega\cdot m + v\cdot f$가 와트 단위의 일률이다(프레임 규칙과 함께 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §6]]에서 정의).
$\mathcal{V} = J\dot\theta$를 대입하면:
$$\dot\theta^\top \tau = (J\dot\theta)^\top \mathcal{F} = \dot\theta^\top J^\top \mathcal{F} \quad \forall \dot\theta \;\;\Longrightarrow\;\; \boxed{\tau = J^\top(\theta)\,\mathcal{F}}$$
*같은* 행렬이 속도를 내보내고 렌치를 되받는다. 중력 보상, 힘 제어, 접촉 추론이 전부 이 한 줄에 달려 있다. (프레임은 맞춰야 한다. $J_b$는 물체 렌치 $\mathcal{F}_b$와, $J_s$는 공간 렌치 $\mathcal{F}_s$와 짝이다.)

**같은 숫자를 6차원 벡터로.** 이 힘을 공간 렌치로 쓰면 모멘트 $p\times f$를 베이스에 대해 잡은 $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$이고, 이 자세에서 공간 야코비안의 열은 스크류 $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$과 $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$이다. $\theta_1 = 0$이라 $\mathcal{S}_2$가 홈에서의 자리에 그대로 있기 때문이다. 따라서 $J_s^\top\mathcal{F}_s = (-10,\ 0)$이 다시 나오고, [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §6]]이 같은 검산을 물체 프레임에서 되풀이한다. $2\times2$ 지름길이 정확한 이유는 말단 힘과 말단 속도의 짝이 공간 렌치와 공간 트위스트의 짝과 같은 일률을 주기 때문이다.

> **정역학 쌍대성의 정의.** **정역학 쌍대성**(statics duality)은 *말단 렌치를 관절 토크로 보내는 선형 사상*이다. 같은 $\theta$에서 속도 야코비안의 전치이고, 세 조건 아래에서 성립한다. **정적 평형**: 팔이 정지해 있다. $\dot\theta = 0$, $\ddot\theta = 0$이고(MR은 일률 균형을 $\dot\theta \to 0$의 극한으로 읽는다), 그래서 팔을 움직이는 데 드는 일률이 없고 관절 쪽 일률이 도구 쪽 일률과 같다. **둘에 같은 프레임**: $J_b$는 물체 렌치 $\mathcal{F}_b$와, $J_s$는 $\mathcal{F}_s$와 짝을 이룬다. 그리고 **$\mathcal{F}$는 도구가 가하는 렌치**다. 팔 자신의 무게를 버티는 토크는 따로 더한다(MR §5.2).
>
> $$\tau = J^\top(\theta)\,\mathcal{F} \quad\Longleftrightarrow\quad \tau^\top\dot\theta = \mathcal{F}^\top J(\theta)\,\dot\theta \ \ \text{for every } \dot\theta$$
>
> 여기서 $\tau \in \mathbb{R}^n$은 관절 토크, $\mathcal{F}$는 렌치('대상으로 한 번 끝까지'의 $J$와 짝지을 때는 말단 힘만), $J$는 같은 프레임의 야코비안이다. 전치가 나오는 것은 일률이 내적이기 때문이고, 그래서 $\dot\theta$를 내보내는 행렬이 $\mathcal{F}$를 되돌려야 한다.
>
> - **예**: $10\,\mathrm{N}$ 누르기. $\mathcal{F}_s$를 $J_s$와 짝지으면 $\tau = (-10,\ 0)\,\mathrm{N\,m}$이고, 같은 힘을 도구 프레임에서 쓴 $\mathcal{F}_b = (0,0,0;\,-10,0,0)$을 $J_b$와 짝지어도 같은 값이 나온다.
> - **비예**: 손목 센서가 준 $\mathcal{F}_b$에 $J_s^\top$를 곱하는 것. 결과는 $(0,\ 0)$으로, 접촉이 어느 관절에도 부하를 주지 않는다는 듯이 나온다. 프레임을 섞었기 때문에 어깨의 실제 $10\,\mathrm{N\,m}$이 사라진 것이다.

**토크에서 힘을 거꾸로 읽는 쪽이 어려운 방향이다.** 알려진 렌치를 관절 부하로 바꾸는 데는 역행렬이 필요 없고, 이 사상은 특이점에서도 뜻이 있다. 반면 측정 토크에서 모르는 렌치를 찾는 역문제는 모호하거나 잡음에 민감할 수 있다. 숫자로 보면, $\theta = (0^\circ, 5^\circ)$에서 $J$의 가장 작은 특이값은 $0.039$이고 그 힘 방향 $(0.999,\ 0.052)$는 거의 정확히 팔을 따른다. 그쪽으로 $10\,\mathrm{N}$을 밀어도 관절 토크 벡터의 크기는 $0.39\,\mathrm{N\,m}$뿐이므로, 측정 토크의 $0.1\,\mathrm{N\,m}$ 오차가 팔 방향 힘을 최대 $0.1/0.039 = 2.6\,\mathrm{N}$까지 숨길 수 있다. 카탈로그 자세에서는 $0.1/0.618 = 0.16\,\mathrm{N}$이다. 측정한 토크에서 중력, 관성, 마찰 등의 몫도 분리해야 한다.

> [!note]- 더 깊이 · Deeper
> **등식을 회계 규칙으로 읽기.** 렌치는 작용하는 운동을 통해 일을 한다. 야코비안이 관절 운동이 도구에서 어떻게 보이는지 알려 주므로, 그 전치는 같은 도구 렌치가 각 관절에 주는 부하를 알려 준다. 열마다 렌치와 그 열이 만드는 운동의 내적이 그 관절의 토크, 곧 일반화된 힘이다. '대상으로 한 번 끝까지'에서는 누르기가 열 2와 수직이므로 엘보 토크가 0이다.
>
> **토크 0은 힘 0이 아니다.** 힘이 관절의 허용된 순간 운동을 따라 일을 하지 않으면 그 관절의 토크 기여는 0이지만, 힘은 그대로 있고 구속 방향의 반력으로 전달된다. 엘보의 베어링은 $10\,\mathrm{N}$ 누르기 전체를 지는데 엘보 모터는 아무것도 지지 않는다. 일률 등식을 쓰기 전에 렌치와 트위스트의 표기, 단위, 프레임을 맞춘다.

### 4. 특이점과 가조작성 타원체

P2를 $\theta = (0^\circ, 5^\circ)$로 곧게 펴면 말단을 $0.1\,\mathrm{m/s}$로 곧장 밀어내는 데 관절 속도가 $2.56\,\mathrm{rad/s}$ 들고, 이는 카탈로그 자세에 드는 것의 $16$배다. 특이점 근처에서는 작은 과제 운동이 거대한 관절 속도를 요구한다. $\det J = \sin\theta_2 \to 0$일 때 $J^{-1}$이 폭발하기 때문이다. 이 절은 한 자세가 정확히 언제 특이한지, 그리고 얼마나 가까운지를 어떻게 재는지 말한다.

> **기구학적 특이점의 정의.** **기구학적 특이점**(kinematic singularity)은 *컨피규레이션의 성질*이고, 고른 과제 야코비안 $J(\theta)$로 판정한다. 정의 조건 셋. **랭크가 떨어진다**: $\operatorname{rank}J(\theta)$가 $J$가 어디서든 도달하는 가장 큰 랭크보다 작다. 정사각 $J$라면 $\det J(\theta) = 0$이다. **프레임과 무관하다**: $[\mathrm{Ad}_{T_{sb}}]$가 가역이므로 $\operatorname{rank}J_s = \operatorname{rank}J_b$이고, 트위스트를 어느 프레임에서 쓰느냐가 특이점을 만들거나 없애지 못한다. **과제에 상대적이다**: $J$의 행이 과제, 곧 어느 점의 어떤 좌표인지를 정하고, 과제가 다르면 특이 자세도 다르다. 이런 $\theta$에서 도구는 어떤 방향으로 순간적으로 움직일 수 없고, 그 방향의 렌치는 관절 토크 없이 버틴다(MR §5.3).
>
> $$\operatorname{rank}J(\theta) < \max_{\theta'}\,\operatorname{rank}J(\theta'), \qquad \text{P2's tip: } \det J(\theta) = L_1L_2\sin\theta_2 = 0$$
>
> 최댓값은 모든 컨피규레이션에 대해 잡는다. 그래서 이 판정은 한 자세를 과제 행의 개수가 아니라 그 팔이 낼 수 있는 최선과 견준다.
>
> - **예**: 곧게 편 P2, $\theta = (0^\circ, 0^\circ)$. $J = \begin{pmatrix}0&0\\2&1\end{pmatrix}$의 랭크는 1이고, 잃은 방향은 팔을 따르는 방향이며, 그 방향의 $10\,\mathrm{N}$ 힘에는 $J^\top(10, 0) = (0, 0)$만 있으면 된다. P2의 $6\times2$ $J_s$는 모든 $\theta$에서 랭크 2를 유지하고, 말단에서 $+y_b$ 방향으로 전완과 직각으로 $0.5\,\mathrm{m}$ 떨어진 도구 점(카탈로그 자세에서는 $-x$ 쪽)은 대신 $\theta_2 = -26.6^\circ$와 $153.4^\circ$에서 특이하다. 이 특이점은 말단 위치 과제의 것이다.
> - **비예**: 거의 곧은 $\theta = (0^\circ, 5^\circ)$. $\det J = 0.087$이고 랭크가 2이므로 특이점이 아니다. 그런데도 말단을 $0.1\,\mathrm{m/s}$로 곧장 밀어내려면 관절 속도가 $2.56\,\mathrm{rad/s}$ 들고, 이는 카탈로그 자세에 드는 $0.158$의 $16$배다. 특이점은 예·아니요로 답하는 질문이고, 얼마나 가까운지는 아래 타원체가 잰다.

- **가조작성 타원체**는 관절 속도 단위 공이 $J$를 통과한 상이고, 그 축들이
  특이값([[02-foundations/linear-algebra|SVD]])이다. 긴 축 = 쉬운 방향, 짧은 축 = 어려운
  방향; 특이점에서는 한 축이 0으로 붕괴한다. 힘 타원체는 그 역수 쌍둥이다 — 움직이기
  어려운 방향일수록 힘을 버티기는 쉽고, 그 반대도 성립한다.

> **가조작성 타원체의 정의.** **가조작성 타원체**(manipulability ellipsoid)는 *한 컨피규레이션에 붙은 도구 속도의 집합*이다. 길이가 1인 모든 관절 속도 벡터를 $J(\theta)$로 보낸 상이다. 정의 조건 둘. **단위 관절 속도**: 유클리드 노름으로 $\|\dot\theta\| = 1$이다. 이 노름은 모든 관절을 같게 치므로 한 관절의 단위를 바꾸면 모양이 바뀐다. **한 컨피규레이션**: $J$는 판정하는 $\theta$에서 고정한다. $J$의 랭크가 $m$으로 꽉 차 있으면 상은 아래에 쓴 타원체이고, 특이점에서는 납작해져 P2에서는 선분이 된다(MR §5.4).
>
> $$\bigl\{v :\ v^\top (JJ^\top)^{-1}v = 1\bigr\}, \qquad \text{semi-axes } \sigma_i(J) = \sqrt{\lambda_i(JJ^\top)}, \qquad \mu_1 = \sigma_{\max}/\sigma_{\min}$$
>
> 여기서 $v$는 과제 속도, $\lambda_i$는 $JJ^\top$의 고윳값이다. 집합이 이런 모양인 것은, P2처럼 $J$가 정사각이고 가역이면 $v = J\dot\theta$가 $\dot\theta^\top\dot\theta = 1$을 $v^\top (JJ^\top)^{-1}v = 1$로 바꾸기 때문이고, 그래서 축이 $JJ^\top$의 고유벡터 방향이다. $\mu_1 \ge 1$은 MR의 등방성 척도로 특이점에서 무한대가 되고, 그 제곱이 $JJ^\top$의 조건수다. $\mu_1$ 자체는 [[02-foundations/linear-algebra|1. 선형대수 §3]]의 조건수 $\kappa_2(J) = \sigma_{\max}/\sigma_{\min}$이고, 거기 §4.5.2가 바로 이 자세에서 $2.618$로 계산한다. 이 페이지는 내내 $\mu_1$로 쓴다.
>
> - **예**: 카탈로그 자세의 P2는 반축이 $1.618$과 $0.618$, $\mu_1 = 2.618$이다. 곧게 펼수록 커져서 $(0^\circ, 20^\circ)$에서 $14.2$, $(0^\circ, 5^\circ)$에서 $57.3$이다.
> - **비예**: 힘 타원체 $\{f :\ \|J^\top f\| = 1\}$. 축은 같고 반축은 역수라서, 속도의 긴 축 방향으로 $0.618$, 짧은 축 방향으로 $1.618$이다. 속도의 긴 축을 힘이 센 방향으로 읽으면 둘이 뒤바뀐다. 패널을 누를 자세는 힘 타원체로 판정해야 한다.

<svg viewBox="0 0 560 190" style="max-width:100%;height:auto" role="img" aria-label="θ2 = 90°(반축 1.62와 0.62)와 θ2 = 20°(2.20과 0.16)에서 P2의 가조작성 타원을 팔 축척의 0.4로 그린 그림">
  <ellipse cx="103.0" cy="92.0" rx="37.5" ry="14.3" transform="rotate(31.7 103.0 92.0)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="45.0" y1="150.0" x2="103.0" y2="150.0"/><line x1="103.0" y1="150.0" x2="103.0" y2="92.0"/></g><g fill="currentColor"><circle cx="45.0" cy="150.0" r="4"/><circle cx="103.0" cy="150.0" r="4"/><circle cx="103.0" cy="92.0" r="3.5"/></g>
  <ellipse cx="397.5" cy="130.2" rx="51.1" ry="3.6" transform="rotate(78.0 397.5 130.2)" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/><g stroke="currentColor" stroke-width="2.4" fill="none"><line x1="285.0" y1="150.0" x2="343.0" y2="150.0"/><line x1="343.0" y1="150.0" x2="397.5" y2="130.2"/></g><g fill="currentColor"><circle cx="285.0" cy="150.0" r="4"/><circle cx="343.0" cy="150.0" r="4"/><circle cx="397.5" cy="130.2" r="3.5"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90&#176; &#8212; 조건이 좋다</tspan></text><text x="355" y="26">&#952;<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 20&#176; &#8212; 특이점에 접근</tspan></text>
    <text x="115" y="42" font-size="10" opacity="0.8">det J = 1.00 &#183; &#963; = 1.62, 0.62 &#183; 비 2.6</text><text x="355" y="42" font-size="10" opacity="0.8">det J = 0.34 &#183; &#963; = 2.20, 0.16 &#183; 비 14</text>
  </g>
</svg>

카탈로그 자세와 엘보를 $\theta_2 = 20^\circ$로 편 자세에서 P2의 가조작성 타원을 말단 중심에 팔 축척의 $0.4$로 그렸다. $\sigma = 1.62$와 $0.62$($\mu_1 = 2.6$) 대 $2.20$과 $0.16$($\mu_1 = 14$)이다. 팔이 펴질수록 타원이 납작해져 한 방향은 계속 쉽고 다른 방향은 갈수록 큰 관절 속도를 요구하며, $\theta_2 = 0^\circ$에서는 선분으로 붕괴한다.

**위키 연결**: 힘 피드백 원격조작, 중력 보상, 유연 제어가
$\tau = J^\top \mathcal{F}$ 위에 서 있고([[01-canonical-papers/notes/4-vla/act|ALOHA]] 자체는 리더 관절을 팔로워 관절로 곧바로 옮긴다), 특이점 인지가 실제 팔에서 VLA(시각·언어 입력에서 행동을 내는 정책) 원출력에 안전
필터를 거는 이유다.

### 스스로 점검

1. $\theta = (90°, 90°)$에서 $J$와 행렬식을 계산하라.
2. 일률 보존에서 $\tau = J^\top \mathcal{F}$를 안 보고 다시 유도하라.
3. 2R 팔이 $\theta_2 = 5°$에 있다. 팔의 축 방향으로 말단을 움직이라는 과제가 오면
   정성적으로 무슨 일이 일어나는가? 수직 방향이면?
4. 가조작성 타원체와 힘 타원체의 축이 서로 역수인 이유는?

> [!tip]- 정답 · Answers
> 1. $s_1 = 1, c_1 = 0, s_{12} = \sin 180° = 0, c_{12} = -1$ → $J = \begin{pmatrix} -1 & 0 \\ -1 & -1 \end{pmatrix}$, $\det J = 1$. 여전히 특이하지 않고, $\det J = L_1L_2\sin\theta_2 = \sin 90° = 1$과 맞는다.
> 2. $\dot\theta^\top \tau = \mathcal{V}^\top \mathcal{F}$에 $\mathcal{V} = J\dot\theta$ 대입, 모든 $\dot\theta$에 대해 성립 ⇒ $\tau = J^\top \mathcal{F}$.
> 3. 팔 자신의 축 방향이 거의 특이 방향이다: $\det J = \sin 5° \approx 0.087$, 최소 특이값 ≈ 0.04라 카탈로그 자세보다 한 자릿수 넘게 큰 관절 속도가 필요하고($0.1\,\mathrm{m/s}$에 $2.56$ 대 $0.158\,\mathrm{rad/s}$) 관절 한계를 넘기 쉽다. 수직 방향은 정상 동작.
> 4. 속도는 특이값 $\sigma$배로 증폭되고, 같은 방향의 힘은 $\tau = J^\top \mathcal{F}$에 의해 $1/\sigma$로 스케일되기 때문. 움직이기 쉬운 방향은 힘을 버티기 어렵고, 그 반대도 성립한다.

### 과제 · Problem set

Tier A. [[02-foundations/lab-plants|0.6]]의 **P2**, 카탈로그 자세 $\theta=(0^\circ,90^\circ)$와 각 문항이 정하는 다른 자세. 팔의 질량과 $\Lambda$는 이미 읽은 [[02-foundations/manipulator-kinematics-dynamics|10]]의 것이고, 이 페이지는 속도와 정역학이다.

1. **그리기.** 엘보를 $\theta=(0^\circ,30^\circ)$로 접어 곧은 팔에 더 가까워진 위의 그림: 베이스 원점, 엘보 $(1,0)$, 말단 $(1.866,\ 0.5)$. $\dot\theta=(1,0)$의 말단 속도(열 1)와 $\dot\theta=(0,1)$의 말단 속도(열 2)를 말단에서 화살표로, 가조작성 타원, 그리고 베이스에서 곧장 멀어지는 $0.25\,\mathrm{m/s}$의 명령 말단 속도와 그것이 요구하는 관절 속도를 그려라. 두 열을 벡터로 써라.
2. **유도.** 같은 말단의 다른 엘보, [[04-robotics/modern-robotics/ch06-inverse-kinematics|6장]]의 가지 B $=(90^\circ,-90^\circ)$: 엘보는 $(0,1)$, 전완은 $+x$ 방향. (a) 말단의 두 화살표에서 $J$와 $\det J$. (b) $J^{-1}$을 $J$와 견주어라. (c) $v=(0,-0.25)\,\mathrm{m/s}$에 필요한 관절 속도: 어느 관절이 움직이는가? (d) $10\,\mathrm{N}$ 누르기 $F=(0,-10)\,\mathrm{N}$과 $F=(2,-5)\,\mathrm{N}$에 대한 $\tau=J^\top F$를 카탈로그 자세의 $(-10,0)$, $(-7,-2)$와 견주어라. (e) 카탈로그 자세로 돌아가 이번에는 2장의 수직 패널 면을 누른다. 도구가 그 면 안쪽으로 $F=(10,0)\,\mathrm{N}$을 민다. $\tau$를 구하고 왜 이제 엘보가 부하를 지는지 말하라.
3. **실행.** 템플릿을 채워 강의의 $T=0.01$, $2\,\mathrm{s}$ 쌍(매 스텝 갱신한 $J$ 대 고정한 $J$)을 재현한다. 그다음 $T$만 $0.05$로, 매 스텝 갱신한 $J$, 같은 $2\,\mathrm{s}$. 추가 오차는 고정-$J$급인가 적분기급인가?

> [!note]- 그리는 법 · How to draw it
> - 먼저 P2를 축척대로 그린다. 베이스 원점, 엘보 $(1,0)$, $30^\circ$로 놓인 전완 끝의 말단 $(1.866,\ 0.5)$.
> - 열 $i$는 관절 $i$만 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도다. 관절 $i$에서 말단까지의 선에 수직이고 그 선만큼 긴 화살표로 그린다. 열 1은 베이스에서 $1.932$, 열 2는 길이 1인 전완이다. 각 화살표에 벡터를 적는다.
> - 두 열 모두 말단에 붙인다. 베이스에서 그리는 것이 이 그림이 틀어지는 표준적인 방식이다. 야코비안의 열은 말단의 속도다.
> - 가조작성 타원은 말단 중심이고 관절 속도 단위원의 상이며, 반축은 특이값이다. 여기서는 $2.163$과 $0.231$로, 위 그림의 $1.618$과 $0.618$보다 훨씬 가늘다($\mu_1=9.36$).
> - 말단을 지나는 베이스-말단 선을 표시한다. 타원의 짧은 축이 그 선과 몇 도 차이밖에 나지 않으므로, 팔이 가장 못 움직이는 방향이 반지름 방향이다.
> - 명령 속도는 그 선을 따라 말단에서 나가는 별도의 화살표로, 두 열과 다른 선 굵기로 그리고, 옆에 $\dot\theta=J^{-1}v$를 적는다.

> [!tip]- 정답 · Solutions
> 1. 열 1은 어깨만 돌 때의 속도로, 베이스-말단 선에 수직이고 그만큼 길다. $(-0.5,\ 1.866)$, 길이 $1.932$. 열 2는 엘보만 돌 때의 속도로, $30^\circ$의 전완에 수직인 $(-0.5,\ 0.866)$, 길이 1. $\det J=\sin30^\circ=0.5$. 타원의 반축은 $2.163$과 $0.231$로 $\mu_1=9.36$(카탈로그 자세는 $2.618$)이고, 긴 축은 $108^\circ$, 짧은 축은 $18^\circ$ 방향이라 $15^\circ$인 베이스-말단 선에 가깝다. 말단을 $(0.966,\ 0.259)$ 방향으로 $0.25\,\mathrm{m/s}$ 곧장 밀어내려면 $\dot\theta=J^{-1}v=(0.483,\ -0.966)\,\mathrm{rad/s}$가 필요하고, 이는 카탈로그 자세에서 같은 요청에 드는 $(0.177,\ -0.354)$의 $2.7$배다. 곧은 팔에 가까울수록 비싼 것은 반지름 방향이다.
> 2. (a) 어깨만: 말단 $(1,1)$은 여전히 베이스에서 $\sqrt2$ 떨어져 있으므로 열 1은 카탈로그 자세와 같은 $(-1,1)$이다. 열 1은 말단이 어디 있느냐에만 달렸다. 엘보만: 전완이 이제 $(0,1)$에서 $+x$를 가리키므로 말단은 그에 수직으로 움직여 열 2 $=(0,1)$이다. $J=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$, $\det J=(-1)(1)-(0)(1)=-1$. 카탈로그 자세와 크기가 같고 부호가 반대인데, 엘보가 반대로 굽었기 때문이다($\sin\theta_2=-1$). (b) $J^{-1}=\frac{1}{-1}\begin{pmatrix}1&0\\-1&-1\end{pmatrix}=\begin{pmatrix}-1&0\\1&1\end{pmatrix}=J$. 이 $J$는 자기 자신의 역행렬이다($J^2=I$). (c) $\dot\theta=J^{-1}v=(0,\ -0.25)\,\mathrm{rad/s}$. 엘보만 돈다. 전완이 수평이라 엘보 혼자 말단을 곧장 내리기 때문이고, 카탈로그 자세에서는 같은 $v$에 두 관절이 다 필요했다. (d) $J^\top=\begin{pmatrix}-1&1\\0&1\end{pmatrix}$. 누르기는 $\tau=(-10,\ -10)\,\mathrm{N{\cdot}m}$를 준다. 카탈로그 자세에서는 어깨만 졌는데 이제 두 관절이 다 진다. 미는 힘이 엘보에서 $1\,\mathrm{m}$ 떨어진 곳에서 전완에 수직이기 때문이다. $F=(2,-5)$는 $\tau=(-2-5,\ -5)=(-7,\ -5)\,\mathrm{N{\cdot}m}$를 준다. 어깨의 $-7$은 카탈로그 자세와 같은데, 열 1에만 달렸기 때문이다. (e) 카탈로그 자세의 $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$로 $\tau=J^\top(10,0)=(-10,\ -10)\,\mathrm{N{\cdot}m}$. 미는 힘이 수평이라 엘보에서 $1\,\mathrm{m}$ 떨어진 곳에서 선 전완에 수직이므로 엘보가 $10\,\mathrm{N{\cdot}m}$를 지고, 어깨에 대해서는 지렛대가 말단의 높이 $1\,\mathrm{m}$이므로 어깨도 $10\,\mathrm{N{\cdot}m}$를 진다.
> 3. 빈칸: `((-s1-s12, -s12), (c1+c12, c12))`. 역행렬: `th1d = (J[1][1]*0 - J[0][1]*vy)/det`, `th2d = (-J[1][0]*0 + J[0][0]*vy)/det`. 강의 쌍: 매 스텝 갱신 $\approx(0.999,\ 0.500)$, 고정 $\approx(0.878,\ 0.521)$. $T=0.05$, 매 스텝 갱신: $\approx(0.997,\ 0.501)$ — 여전히 밀리미터. 적분기급이다. 고정 오차는 $T$와 무관하다(관절 속도가 상수이므로). 스텝 크기의 산물이 아니다.
