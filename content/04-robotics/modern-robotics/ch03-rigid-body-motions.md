---
title: "MR Ch.03 — Rigid-Body Motions"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.3** — [[04-robotics/modern-robotics-book|book guide & free PDF]] · prerequisite: [[02-foundations/se3-geometry|8. SE(3)]]

> [!note] Prerequisites · 선수 지식
> You should be able to: ① multiply rotation matrices and use $R^{-1} = R^\top$ ([[02-foundations/se3-geometry|SE(3) §1]]) ② compute a cross product $\omega \times v$ ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §1]]) ③ solve $\dot x = ax \Rightarrow x = e^{at}x_0$ ([[02-foundations/engineering-math|0.5 §8]]) ④ read a twist $(\omega, v)$ and the adjoint $\mathrm{Ad}_T$ as [[02-foundations/se3-geometry|8. SE(3) §4]] writes them — §1, §3 and §4 recall them before adding to them. If any of the four is shaky, read that page first. The object throughout is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled).
> 다음을 할 수 있어야 한다: ① 회전 행렬 곱셈과 $R^{-1} = R^\top$ ([[02-foundations/se3-geometry|SE(3) §1]]) ② 외적 $\omega \times v$ 계산 ([[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §1]]) ③ $\dot x = ax \Rightarrow x = e^{at}x_0$ ([[02-foundations/engineering-math|0.5 공업수학 §8]]) ④ [[02-foundations/se3-geometry|8. SE(3) §4]]가 쓰는 트위스트 $(\omega, v)$와 수반(adjoint) $\mathrm{Ad}_T$를 읽을 수 있어야 한다 — §1, §3, §4가 먼저 되짚은 뒤에 보탠다. 넷 중 하나라도 흔들리면 해당 페이지를 먼저 읽어라. 전체에서 쓰는 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**다.

## English

**Core question**: how do we represent and compose rotations, poses, and velocities of rigid bodies — without singularities?

This is the longest-feeling chapter of the book, and it takes five of the seventeen robotics sessions that ch.2–6 fill (sessions 5–9): every later chapter is this machinery applied. Take it in four steps (§1–§4), then two more that later chapters call on (§5–§6).

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this page is the manipulation layer's language — the rotations and poses of [[02-foundations/se3-geometry|8. SE(3)]] on the mathematics floor, carried into screws, twists and wrenches — and in *"install that panel on the frame"* it serves *move the component*, where every velocity command is a twist in a named frame, and *detect contact*, where a wrist force–torque sensor's wrench must be moved into the tool frame (its chip sits in the manipulation band of the [[physical-ai-map|Physical AI Map]]). Without it frames lie silently: read a space twist's linear part as the tip velocity and P2's shoulder turning at $1\,\mathrm{rad/s}$ seems to leave the tip still ($v_s = 0$) while it moves at $(-1, 1, 0)\,\mathrm{m/s}$ (§3), and drop a wrench's moment and the shoulder appears to hold $10\,\mathrm N$ on a $1\,\mathrm m$ lever for $0\,\mathrm W$ (§6). Later pages use it section by section — [[04-robotics/modern-robotics/ch04-forward-kinematics|MR ch.4]] multiplies §5's exponentials into forward kinematics, [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §1 and §3]] builds the space Jacobian from the body Jacobian with §4's adjoint and derives $\tau = J^\top\mathcal{F}$ from §6's power pairing, [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6 §2]] takes §5's logarithm as its pose error, [[04-robotics/contact-force-tactile|9. Contact §4]] writes contacts as §6's wrenches, and [[04-robotics/geometric-perception-calibration|3.5 §7.5]] servos a camera on §3 and §5 — all in block 2 of the dissertation path ([[07-research-program/index|7 §8]]), where this page takes robotics sessions 5–9. After it you can write P2's $T_{sb}$, turn a joint axis into a screw and back with exp and log, move a twist or a wrench between $\{s\}$ and $\{b\}$, and say which point a velocity's linear part belongs to.

> [!note] First pass · 처음이라면
> One session, robotics session 5: the Running object, the picture and the Worked case by hand, then §1 and §2. End it by writing $T_{sb}$ with the page closed, reading $\omega$ from $\dot R = \mathrm{diag}(0.2,\ 0.2,\ 0)$, and doing self-check 1. The rest takes sessions 6–9: §3–§4 (twists in two frames and the adjoint), §5 with its listing, §6 (wrenches), then the rest of the self-check and the problem set. The collapsed *Deeper* notes of §1 and §3 are for the second pass.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], one of the wiki's six frozen *plants* (control's word for the system being controlled): a planar arm of two $1\,\mathrm m$ links, $\theta_1$ measured from the $x$-axis and $\theta_2$ relative to link 1, at the catalog pose $\theta = (0°, 90°)$ with the elbow at $(1, 0)$ and the tip at $(1, 1)\,\mathrm m$. Two frames carry the page, as in [[02-foundations/se3-geometry|8. SE(3)]]: the **space frame** $\{s\}$, fixed at the shoulder, and the **body frame** $\{b\}$, fixed to the tool at the tip with $\hat x_b$ along the forearm; both have $\hat z$ out of the page. The arm's masses play no part here.

*Scope: this page teaches the exponential and logarithm of rotations and poses, twists and wrenches in the two frames, and the adjoint that moves them between frames, all on P2. It does not teach the forward kinematics of a chain ([[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]]) or Jacobians ([[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]]), which are built from them.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 324" style="max-width:100%;height:auto" role="img" aria-label="P2 at the catalog pose with the space frame at the base, the body frame at the tip, the dashed offset p = (1, 1, 0), and two rotation axes through the origin and the elbow; the four velocity numbers are written beside the drawing.">
  <defs><marker id="mr03hdE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="120,222 260,222 260,82" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.28"/>
  <line x1="126.4" y1="215.6" x2="253.6" y2="88.4" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#mr03hdE)"/>
  <g stroke="currentColor" stroke-width="1.8" marker-end="url(#mr03hdE)"><line x1="127" y1="222" x2="176" y2="222"/><line x1="120" y1="215" x2="120" y2="166"/><line x1="260" y1="76" x2="260" y2="26"/><line x1="254" y1="82" x2="204" y2="82"/></g>
  <g><circle cx="120" cy="222" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="120" cy="222" r="2" fill="currentColor"/></g>
  <g><circle cx="260" cy="222" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="260" cy="222" r="2" fill="currentColor"/></g>
  <g><circle cx="260" cy="82" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="260" cy="82" r="2" fill="currentColor"/></g>
  <path d="M115.1 203.6 L113.5 204.1 L112 204.8 L110.5 205.5 L109.1 206.4 L107.8 207.4 L106.6 208.6 L105.4 209.8 L104.4 211.1 L103.5 212.5 L102.8 214 L102.1 215.5 L101.6 217.1 L101.3 218.7 L101.1 220.3 L101 222 L101.1 223.7 L101.3 225.3 L101.6 226.9 L102.1 228.5 L102.8 230 L103.5 231.5 L104.4 232.9 L105.4 234.2 L106.6 235.4 L107.8 236.6 L109.1 237.6 L110.5 238.5 L112 239.2 L113.5 239.9 L115.1 240.4 L116.7 240.7 L118.3 240.9 L120 241 L121.7 240.9 L123.3 240.7 L124.9 240.4 L126.5 239.9 L128 239.2 L129.5 238.5 L130.9 237.6 L132.2 236.6 L133.4 235.4 L134.6 234.2 L135.6 232.9 L136.5 231.5 L137.2 230 L137.9 228.5 L138.4 226.9" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr03hdE)"/>
  <path d="M241.6 226.9 L242.1 228.4 L242.7 229.8 L243.4 231.2 L244.2 232.6 L245.1 233.8 L246.1 235 L247.2 236.1 L248.4 237.1 L249.7 238 L251 238.8 L252.4 239.4 L253.9 240 L255.4 240.4 L256.9 240.7 L258.4 240.9 L260 241 L261.6 240.9 L263.1 240.7 L264.6 240.4 L266.1 240 L267.6 239.4 L269 238.8 L270.3 238 L271.6 237.1 L272.8 236.1 L273.9 235 L274.9 233.8 L275.8 232.6 L276.6 231.2 L277.3 229.8 L277.9 228.4 L278.4 226.9 L278.7 225.4 L278.9 223.9 L279 222.3 L279 220.8 L278.8 219.2 L278.5 217.7 L278.1 216.2 L277.6 214.7 L276.9 213.3 L276.1 212 L275.3 210.7 L274.3 209.5 L273.2 208.3 L272.1 207.3 L270.8 206.4 L269.5 205.5" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr03hdE)"/>
  <line x1="318" y1="14" x2="318" y2="290" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="176" y="241" text-anchor="middle">x̂<tspan dy="3.5">s</tspan></text>
    <text x="112" y="171" text-anchor="end">ŷ<tspan dy="3.5">s</tspan></text>
    <text x="94" y="208" text-anchor="end" font-size="12">{s}</text>
    <text x="94" y="226" text-anchor="end">ẑ<tspan dy="3.5">s</tspan></text>
    <text x="268" y="36">x̂<tspan dy="3.5">b</tspan></text>
    <text x="200" y="74" text-anchor="end">ŷ<tspan dy="3.5">b</tspan></text>
    <text x="270" y="98" font-size="12">{b}</text>
    <text x="270" y="112">ẑ<tspan dy="3.5">b</tspan></text>
    <text x="180" y="144" text-anchor="end">p = (1, 1, 0)</text>
    <text x="120" y="260" text-anchor="middle">q<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="120" y="276" text-anchor="middle">ω̂ = (0, 0, 1)</text>
    <text x="120" y="292" text-anchor="middle">θ̇ = 1 rad/s</text>
    <text x="260" y="260" text-anchor="middle">q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="260" y="276" text-anchor="middle">ω̂ = (0, 0, 1)</text>
    <text x="260" y="292" text-anchor="middle">θ̇ = 1 rad/s</text>
    <text x="12" y="312" opacity="0.85">⊙ = a z axis out of the page · curved arrow = turning about it at 1 rad/s</text>
    <text x="332" y="26" font-size="12">Written beside the figure</text>
    <text x="332" y="48">T<tspan dy="3.5">sb</tspan><tspan dy="-3.5">: R</tspan><tspan dy="3.5">sb</tspan><tspan dx="3.1" dy="-3.5">= R</tspan><tspan dy="3.5">z</tspan><tspan dy="-3.5">(90°), p = (1, 1, 0)</tspan></text>
    <text x="332" y="78">Axis 1, through q<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="340" y="96" opacity="0.85">tip:</text>
    <text x="380" y="96">ω̂ × p = (−1, 1, 0) m/s</text>
    <text x="340" y="114" opacity="0.85">v<tspan dy="3.5">s</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="380" y="114">−ω̂ × q<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="332" y="144">Axis 2, through q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="340" y="162" opacity="0.85">tip:</text>
    <text x="380" y="162">ω̂ × (p − q<tspan dy="3.5">2</tspan><tspan dy="-3.5">) = (−1, 0, 0) m/s</tspan></text>
    <text x="340" y="180" opacity="0.85">v<tspan dy="3.5">s</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="380" y="180">−ω̂ × q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (0, −1, 0)</tspan></text>
    <text x="332" y="212">Neither v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">is the tip velocity:</tspan></text>
    <text x="332" y="228">v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= ṗ − ω</tspan><tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">× p, not ṗ.</tspan></text>
  </g>
</svg>

Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at the catalog pose $\theta = (0^\circ, 90^\circ)$, with the space frame $\{s\}$ at the base, the body frame $\{b\}$ at the tip with $\hat x_b$ along the forearm, and the dashed offset $p = (1,1,0)$. $R_{sb} = R_z(90^\circ)$ and $p$ are the whole of $T_{sb}$, and each circled dot is a $z$ axis pointing out of the page. Two candidate axes, both $\hat\omega = (0,0,1)$ at $1\,\mathrm{rad/s}$, pass through the origin $q_1$ and the elbow $q_2 = (1,0,0)$ and move the tip at $(-1,1,0)$ and $(-1,0,0)\,\mathrm{m/s}$, while the space twist's linear parts are $v_s = (0,0,0)$ and $(0,-1,0)$ — neither is the tip velocity, because $v_s = \dot p - \omega_s \times p$, not $\dot p$.

### Worked case · 대상으로 한 번 끝까지

Three numbers derived by hand: the picture's $T_{sb}$ and its tip velocity for the shoulder, then the angular velocity of the forearm when the elbow turns. Each uses one object recalled from [[02-foundations/se3-geometry|8. SE(3)]] or defined in §1–§2 below; the pointers say where.

**Step 1 — the tool pose $T_{sb}$** (a recall of [[02-foundations/se3-geometry|8 §3]]). At the catalog pose the forearm points along $+\hat y_s$, so $\hat x_b = \hat y_s$, and a right-handed frame with $\hat z_b$ out of the page then has $\hat y_b = -\hat x_s$. The columns of $R_{sb}$ are $\{b\}$'s axes written in $\{s\}$, and $p$ is the tip:

$$R_{sb}=R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},\qquad p=(1,1,0),\qquad T_{sb}=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

since a pose stacks the rotation block and the position column over the row $(0,0,0,1)$.

**Step 2 — the tip velocity for the shoulder at $1\,\mathrm{rad/s}$, as a matrix product.** The shoulder spins the whole arm about $\hat z = (0,0,1)$ through the origin, so the tip moves at $\hat z \times p$. §1's bracket writes "cross with $\hat z$" as a matrix, the $[\hat z]_\times$ of 8 §1:

$$[\hat z]\,p = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}\begin{pmatrix}1\\1\\0\end{pmatrix} = \begin{pmatrix}-1\\1\\0\end{pmatrix}\ \mathrm{m/s}$$

because row $i$ of the bracket reproduces component $i$ of the cross product. The velocity is perpendicular to the line from the base to the tip, and its speed $\sqrt2 = 1.414\,\mathrm{m/s}$ is the tip's distance from the axis times $1\,\mathrm{rad/s}$; ch.5's Worked case, Step 1, calls this vector column 1 of the Jacobian.

**Step 3 — an angular velocity read from $\dot R$.** Turn the elbow at $-0.2\,\mathrm{rad/s}$. The forearm's absolute angle is $\varphi = \theta_1 + \theta_2$, so $R = R_z(\varphi)$, and differentiating each entry by the chain rule gives $\dot R = \dot\varphi\,\mathrm{d}R_z/\mathrm{d}\varphi$ with $\mathrm{d}R_z/\mathrm{d}\varphi = \begin{pmatrix}-\sin\varphi&-\cos\varphi&0\\ \cos\varphi&-\sin\varphi&0\\ 0&0&0\end{pmatrix}$. At $\varphi = 90°$ that matrix is $\mathrm{diag}(-1,\ -1,\ 0)$, so with $\dot\varphi = -0.2\,\mathrm{rad/s}$, $\dot R = \mathrm{diag}(0.2,\ 0.2,\ 0)$. That matrix is symmetric, so read directly as a bracket it would report $\omega = 0$ for a turning forearm; the angular velocity is read from $\dot RR^\top$ instead (§2's box):

$$\dot RR^\top = \begin{pmatrix}0.2&0&0\\0&0.2&0\\0&0&0\end{pmatrix}\begin{pmatrix}0&1&0\\-1&0&0\\0&0&1\end{pmatrix} = \begin{pmatrix}0&0.2&0\\-0.2&0&0\\0&0&0\end{pmatrix} = [(0,\ 0,\ -0.2)]$$

so $\omega = (0, 0, -0.2)\,\mathrm{rad/s}$, a clockwise turn about $\hat z$, as the elbow's sign says.

These three steps are what the rest of the page generalizes: §1 names the bracket, §2 the angular velocity and its exponential, §3–§4 the six-number velocity in each frame, and §5–§6 the pose exponential and the wrench.

### 1. The skew-symmetric bridge: cross products become matrices

Rotation is full of cross products — a point at $r$ on a body turning at $\omega$ moves at $\omega \times r$ — and a cross product cannot be multiplied, inverted or exponentiated the way a matrix can; written as a matrix it can, and *linear algebra applies to rotation dynamics*, including §2's matrix exponential. A sign slip in that matrix costs nothing on paper and surfaces only on the robot, as the box's non-example shows. Recall from [[02-foundations/se3-geometry|8. SE(3) §1]] that "cross with $a$" is the skew-symmetric matrix $[a]_\times$; this chapter adds the name $\mathfrak{so}(3)$ for the set of such matrices and uses them as the generators of rotation in §2. **Notation:** 8 writes this matrix $[\omega]_\times$ and the adjoint $\mathrm{Ad}_T$; MR and ch.3–5 write $[\omega]$ and $[\mathrm{Ad}_T]$ — the same objects.

For $\omega = (\omega_1, \omega_2, \omega_3)$, define
$$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}, \qquad [\omega]\,v = \omega \times v.$$
Check one entry yourself: the first row of $[\omega]v$ is $-\omega_3 v_2 + \omega_2 v_3$ —
exactly the first component of $\omega \times v$.

> **The bracket and $\mathfrak{so}(3)$, defined.** $\mathfrak{so}(3)$ is *a set*: the $3\times3$ real matrices that are **skew-symmetric**, $A^\top = -A$, a condition that forces a zero diagonal and leaves three free entries. The **bracket** $[\cdot]$ is *a linear map* from $\mathbb{R}^3$ onto $\mathfrak{so}(3)$, fixed by one rule: $[\omega]$ **performs the cross product**, $[\omega]v = \omega\times v$ for every $v$. Its output is skew-symmetric because $v^\top(\omega\times v) = 0$ for every $v$, and the map is one-to-one, so each element of $\mathfrak{so}(3)$ is $[\omega]$ for exactly one $\omega$ (MR §3.2.2; the cross product itself is in [[02-foundations/se3-geometry|8. SE(3) §1]]).
>
> $$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix} = -[\omega]^\top, \qquad [\omega]\,v = \omega\times v$$
>
> where $\omega = (\omega_1, \omega_2, \omega_3)$; the entries sit where they do so that row $i$ of $[\omega]v$ reproduces component $i$ of $\omega\times v$.
>
> - **Example**: P2's shoulder axis $\hat z = (0,0,1)$ and its tip $p = (1,1,0)$: $[\hat z]p = (-1,1,0)$, the tip velocity for $1\,\mathrm{rad/s}$ at the shoulder, column 1 of the $J$ of [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §2]].
> - **Non-example**: $[p]\hat z = (1,-1,0)$, the operands swapped. $[p]$ is a perfectly good element of $\mathfrak{so}(3)$, but of the wrong vector: the velocity reverses and sends the tip toward $+x$, into the panel. Nothing crashes, so the sign error surfaces only on the robot.

The bracket in words, its sign pattern read physically, and the operand-order check are folded below for the second pass.

> [!note]- Deeper · 더 깊이
> **What the bracket operation does.** The vector $\omega$ holds the angular-velocity coordinates, and the bracket packages those same three numbers into a matrix that performs "cross with $\omega$" on any input vector. The matrix is not an extra physical object and its entries are not independent parameters; its signs encode the right-hand rule of the cross product.
>
> For a point displaced from a rotation axis, the cross product gives the part of its velocity perpendicular to both the axis and the displacement. A point on the axis has no such velocity; a point farther from the axis has a larger one at the same angular speed. This physical picture lets you rebuild the sign pattern instead of memorizing it.
>
> **Check your understanding.** Swapping the operands reverses the cross product, so $[\omega]v$ and $[v]\omega$ are negatives of each other. Matrix notation makes composition easier, but it does not make cross products commutative: check operand order when you turn a geometric formula into code.

### 2. Why an exponential? Rotation is a linear ODE

A gyro or a joint encoder reports an angular velocity, and the orientation has to be integrated from it; the obvious step, $R \leftarrow (I + [\omega]\Delta t)R$, leaves the rotation group — with P2's elbow at $-0.2\,\mathrm{rad/s}$ one $1\,\mathrm s$ step stretches the two columns of $R$ in the plane of rotation by $\sqrt{1+0.2^2} = 1.019804$, a $2\%$ error, and $100$ steps of $0.01\,\mathrm s$ still leave $1.000200$, which $100\,\mathrm s$ of such steps grow back to $2\%$. This section shows that rotation obeys a linear ODE whose exact solution, a matrix exponential, is a rotation at any step size, which is why the gyroscope readings of an IMU (inertial measurement unit) are integrated as a product of exponentials ([[04-robotics/state-estimation-slam|3. State Estimation §7.2]]).

> **Angular velocity, defined.** The **angular velocity** of a turning frame is *a vector*: its direction is the **instantaneous axis of rotation**, oriented by the right-hand rule, and its length is the **turning rate** in rad/s (MR §3.2.2). To have coordinates it needs a frame, and $R(t)$, the orientation of $\{b\}$ in $\{s\}$, gives both natural ones: $\dot RR^\top$ and $R^\top\dot R$ are always **skew-symmetric** (differentiate $RR^\top = R^\top R = I$), so each is the bracket of exactly one vector.
>
> $$[\omega_s] = \dot R\,R^\top, \qquad [\omega_b] = R^\top\dot R, \qquad \omega_s = R\,\omega_b$$
>
> where $\omega_s$ is the angular velocity written in the fixed frame $\{s\}$ and $\omega_b$ the same vector written in $\{b\}$; the third identity is the change of frame, so the two forms of the ODE below agree.
>
> - **Example**: P2 at the catalog pose, elbow turning at $-0.2\,\mathrm{rad/s}$: $R = R_z(90°)$ and $\dot R = \mathrm{diag}(0.2,\ 0.2,\ 0)$, so $\dot RR^\top = R^\top\dot R = [(0,0,-0.2)]$ and $\omega_s = \omega_b = (0,0,-0.2)\,\mathrm{rad/s}$, equal because $R$ turns about $\hat z$ and leaves it fixed.
> - **Non-example**: that $\dot R$ read directly as $[\omega]$. It is symmetric, so its off-diagonal entries report $\omega = 0$ for a forearm that is turning; $\dot R = [\omega]$ holds only at $R = I$. Code that differentiates logged orientations has to multiply by $R^\top$ before it reads an axis.

Multiply the box's first identity on the right by $R$ and use $R^\top R = I$: a frame spinning at constant angular velocity obeys $\dot R = [\omega_s]\,R$ with $\omega_s$ expressed in the space frame, and likewise $\dot R = R\,[\omega_b]$ in the body frame (MR §3.2.2). The two forms agree because $\omega_s = R\,\omega_b$ and rotating a bracket gives $[R\,\omega_b] = R\,[\omega_b]\,R^\top$, so $[\omega_s]\,R = R\,[\omega_b]\,R^\top R = R\,[\omega_b]$.
This is the matrix version of $\dot x = ax$ — so its solution is the matrix version of
$e^{at}$: rotating about unit axis $\hat\omega$ for "time" $\theta$ gives
$$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2 \quad \text{(Rodrigues' formula)}.$$
The infinite series collapses to three terms because $[\hat\omega]^3 = -[\hat\omega]$.

**Worked check** — rotate about $\hat z = (0,0,1)$ by $\theta = 90°$:
$[\hat z] = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}$,
$[\hat z]^2 = \begin{pmatrix}-1&0&0\\0&-1&0\\0&0&0\end{pmatrix}$, so
$$R = I + (1)[\hat z] + (1)[\hat z]^2 = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},$$
which is exactly $R_z(90°)$ — it sends $\hat x \to \hat y$. Every rotation is *one*
axis-angle exponential (Euler's theorem); $\log$ recovers $(\hat\omega, \theta)$ from $R$ (the formula is in §5.3).
This exp/log pair is the door between the Lie group (rotations) and the Lie algebra
(angular velocities) — and the reason poses can be interpolated and averaged correctly.

> **Exponential coordinates of a rotation, defined.** The **exponential coordinates** of a rotation $R \in SO(3)$ — a matrix with $R^\top R = I$ and $\det R = +1$ ([[02-foundations/se3-geometry|8. SE(3) §1]]) — are *three numbers*, $\hat\omega\theta \in \mathbb{R}^3$, under three conditions: the **axis is a unit vector**, $\|\hat\omega\| = 1$; the **angle** $\theta$ is measured about it by the right-hand rule; and **exponentiating returns $R$**, $e^{[\hat\omega]\theta} = R$, so a frame starting at $\{s\}$ and turning about $\hat\omega$ at $1\,\mathrm{rad/s}$ for $\theta$ seconds ends at $R$. Every rotation has them; the matrix logarithm, whose formula is in §5.3, returns the ones with $\theta \in [0, \pi]$, unique when $0 < \theta < \pi$ (MR §3.2.3).
>
> $$e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2, \qquad \theta = \arccos\frac{\operatorname{tr}R - 1}{2}$$
>
> where the three-term form needs the unit axis, since it rests on $[\hat\omega]^3 = -[\hat\omega]$, while a general $\omega$ has $[\omega]^3 = -\|\omega\|^2[\omega]$.
>
> - **Example**: P2's forearm at the catalog pose, $R_z(90°)$: $\operatorname{tr}R = 1$ gives $\theta = 1.5708$, so $\hat\omega\theta = (0,0,1.5708)$; after the elbow's $-0.2\,\mathrm{rad}$ turn below, $(0,0,1.3708)$.
> - **Non-example**: the elbow's angular velocity $(0,0,-0.2)\,\mathrm{rad/s}$ used as the axis with $\theta = 1\,\mathrm{s}$. It is not a unit vector, and the formula returns columns of length $0.995934$, not a rotation; normalized, $\hat\omega = (0,0,-1)$ and $\theta = 0.2$ give $R_z(-11.46°)$ exactly. A gyro reports $\omega$ in rad/s: split it into axis and angle before Rodrigues' formula.

**On P2.** The worked check is P2's forearm. At the catalog pose $\theta_1+\theta_2=90^\circ$, so the forearm frame's orientation is exactly this $R_z(90^\circ)$, the $R_{sb}$ of the Worked case. Every rotation of a planar arm is about the one $z$-axis, and rotations about one axis commute, so for P2 the space and body forms of the ODE coincide, $\omega_s=\omega_b$. Turn the elbow at the $-0.2$ rad/s of the book guide's worked case ([[04-robotics/modern-robotics-book|1. Modern Robotics]]) and after $1$ s the forearm has turned $-0.2$ rad: Rodrigues' formula with $\sin(-0.2)=-0.198669$ and $1-\cos0.2=0.019933$ gives $R_z(78.54^\circ)$, still exactly orthonormal — the exact answer that the opening's Euler step misses by $2\%$.

### 3. Twists: body velocity is six numbers — but read $v$ carefully

When P2's shoulder turns at $1\,\mathrm{rad/s}$ the tip moves at $(-1, 1, 0)\,\mathrm{m/s}$, yet the space twist of that motion has linear part $v_s = 0$ (the picture): the six numbers of a rigid-body velocity carry the frame they are written in and the point their $v$ belongs to, and reading them as "the tip's velocity" is the most common frame error there is. Recall from [[02-foundations/se3-geometry|8. SE(3) §4]] the twist $(\omega, v)$, whose $v$ is the velocity of the body point at the frame's origin — for the joint through $(1, 0, 0)$, $v = (0, -1, 0)$; this section adds the twists of the two standard frames, $\dot TT^{-1}$ and $T^{-1}\dot T$, and the screw with its pitch.

A moving body's velocity is a **twist** $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$.
Written as the $4\times4$ matrix $[\mathcal{V}] = \begin{pmatrix}[\omega] & v\\ 0 & 0\end{pmatrix}$ it is an element of $\mathfrak{se}(3)$, the Lie algebra of SE(3) — the pose counterpart of §2's angular velocities — and its six coordinates are $(\omega_x, \omega_y, \omega_z, v_x, v_y, v_z)$.
**The meaning of $v$ depends on the reference frame and origin.** A space twist describes a velocity field relative to the fixed space origin; a body twist uses the moving body origin. Do not identify their linear components without specifying those choices. Every nonzero twist is a
**screw**: rotate about an axis while translating along it. The **pitch** $h$ is how far the
body advances along the axis per radian it turns about it, in metres per radian, so a screw
with $h = 0.01$ m/rad moves 1 cm along its axis for every radian of rotation — the same
quantity a machinist means by the pitch of a thread. Reading it that way makes the two limits
obvious: pure translation is the **infinite**-pitch case (turn nothing, still advance) and
pure rotation is the zero-pitch case (MR Def. 3.24: $h = 0$ for a pure rotation; $h \to \infty$ when $\omega = 0$).

> **Space and body twists, defined.** A **twist** is *a six-vector attached to one frame*, $\mathcal{V} = (\omega, v)$, or its $4\times4$ matrix $[\mathcal{V}] \in \mathfrak{se}(3)$ ([[02-foundations/se3-geometry|8. SE(3) §4]] defines it for one frame). Two conditions make it a space or a body twist (MR §3.3.2). **One frame for both halves**: $\omega$ and $v$ are written in the same frame, $\{s\}$ or $\{b\}$. **$v$ belongs to that frame's origin**: it is the velocity of the body point, real or imagined, passing through the origin of the frame the twist is written in.
>
> $$[\mathcal{V}_s] = \dot T\,T^{-1} = \begin{pmatrix}[\omega_s] & \dot p - \omega_s\times p\\ 0 & 0\end{pmatrix}, \qquad [\mathcal{V}_b] = T^{-1}\dot T = \begin{pmatrix}[\omega_b] & R^\top\dot p\\ 0 & 0\end{pmatrix}$$
>
> where $T = T_{sb} = (R, p)$ is the pose of $\{b\}$ and $\dot p$ the velocity of $\{b\}$'s origin in $\{s\}$ coordinates; the blocks take this form because multiplying $\dot T$ by $T^{-1}$ on the right or the left is §2's $\dot RR^\top$ and $R^\top\dot R$ one size up.
>
> - **Example**: P2 at the catalog pose, shoulder at $1\,\mathrm{rad/s}$, $\{b\}$ at the tip. The tip moves at $\dot p = (-1,1,0)$, so $\mathcal{V}_s = (0,0,1;\ 0,0,0)$ and $\mathcal{V}_b = (0,0,1;\ 1,1,0)$, the tip's velocity written in the tip frame.
> - **Non-example**: $(\omega_s, \dot p) = (0,0,1;\ -1,1,0)$, spin and tip velocity stacked. In $\{s\}$ it fails the second condition, since $\dot p$ belongs to the tip, not to the origin; as a body twist it fails the first, since it is written in $\{s\}$. Fed to §4's adjoint or the Jacobian of [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §1]], it describes a motion the arm is not making.

The same bookkeeping in words — which origin, which axes — is folded below for the second pass.

> [!note]- Deeper · 더 깊이
> **Distinguish the body origin from the space origin.** Let $p$ locate the body origin in space coordinates. The space twist's linear part is $v_s = \dot p - \omega_s \times p$, so recovering the velocity of the body origin means adding the rotational term back. The body twist's linear part is $v_b = R^\top\dot p$: the velocity of the body origin, written in body axes. So "$v$ is not the tool-tip velocity" needs its frame: when the body origin sits at the tool tip, $v_b$ is exactly the tip's velocity, in the tip's own axes.
>
> Imagine a tool rotating about its own fixed tip. The tip does not translate, while points farther along the tool move. A description from the space origin must carry enough to rebuild that whole velocity field, not just the tip's path, and moving the origin changes the linear part needed to describe the same motion.
>
> **Check your understanding.** Always name both the frame the numbers are written in and the point whose velocity you want. The [official twist explanation](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-2-twists-part-1-of-2/) develops this distinction. A mismatch here can make a numerically correct Jacobian appear to command the wrong translation.

### 4. One motion, two descriptions: space frame vs body frame

Every offset frame — a tool, a camera, a force sensor — sees the same motion with different numbers, and the conversion needs the frame's position as well as its rotation: drop the position and every offset frame gets the wrong linear velocity. Recall from [[02-foundations/se3-geometry|8. SE(3) §4]] the adjoint $\mathrm{Ad}_T$ of a pose $T = (R, p)$, worked there on this very $T_{sb}$ (the Worked case's Step 1); this section derives its corner from §3's formula, adds its conjugation form $T[\mathcal{V}]T^{-1}$ (8 already gives its composition rule), and names what later chapters use it for: turning the body Jacobian into the space Jacobian ([[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §1]]) and, transposed, moving wrenches (§6).

The same physical motion can be written in the fixed frame ($\mathcal{V}_s$) or the moving
body frame ($\mathcal{V}_b$). They are related by the **adjoint** of the current pose
$T = (R, p)$:
$$\mathcal{V}_s = [\text{Ad}_T]\,\mathcal{V}_b, \qquad [\text{Ad}_T] = \begin{pmatrix} R & 0 \\ [p]R & R\end{pmatrix}.$$
The top row says $\omega_s = R\,\omega_b$. The corner $[p]R$ comes from §3's space-twist formula $v_s = \dot p - \omega_s \times p$: the body origin's velocity is $\dot p = R\,v_b$, so $v_s = R\,v_b + p \times \omega_s = R\,v_b + [p]R\,\omega_b$. In words, $v_s$ describes the imaginary body point sitting at the space origin, offset by $-p$ from the body origin, and spinning about the body origin sweeps that point sideways by $p \times \omega_s$.
A special case worth memorizing: if $p = 0$ (pure rotation), this is just "rotate both
halves": $\omega_s = R\,\omega_b$, $v_s = R\,v_b$. **Frame subscripts are not decoration**
— most sign errors in later chapters are $s$/$b$ confusions, so write the subscript every
time. The pose exponential works like the rotation one:
$T = e^{[\mathcal{S}]\theta}$ means "follow screw $\mathcal{S}$ for angle $\theta$," and §5 computes it.

> **Adjoint map, defined.** The **adjoint** of a pose $T = (R, p) \in SE(3)$ ([[02-foundations/se3-geometry|8. SE(3) §3]]) is *a $6\times6$ matrix* $[\mathrm{Ad}_T]$, defined by one requirement: for $T = T_{ab}$ it turns a twist written in $\{b\}$ into the same motion written in $\{a\}$, $[\mathrm{Ad}_T\mathcal{V}] = T[\mathcal{V}]T^{-1}$ (MR Def. 3.20). Three properties follow. It is **linear in the twist** at a fixed $T$. It **needs both halves of the pose**: $R$ turns both vectors, and $p$ enters through the corner $[p]R$. And it **composes like the poses**, $[\mathrm{Ad}_{T_1}][\mathrm{Ad}_{T_2}] = [\mathrm{Ad}_{T_1T_2}]$, so its inverse is $[\mathrm{Ad}_{T^{-1}}]$, not its transpose, which moves wrenches (§6).
>
> $$[\mathrm{Ad}_T] = \begin{pmatrix}R & 0\\ [p]R & R\end{pmatrix}, \qquad [\mathrm{Ad}_T\mathcal{V}] = T\,[\mathcal{V}]\,T^{-1}, \qquad \mathcal{V}_s = [\mathrm{Ad}_{T_{sb}}]\,\mathcal{V}_b$$
>
> where $[\mathcal{V}]$ is the $4\times4$ matrix of §3; conjugation by $T$ is the change of frame itself, so writing it out block by block gives the $6\times6$ form.
>
> - **Example**: P2's $T_{sb}$ at the catalog pose (the Worked case's Step 1) sends the body twists of the two joints, $(0,0,1;\ 1,1,0)$ and $(0,0,1;\ 0,1,0)$, to $(0,0,1;\ 0,0,0)$ and $(0,0,1;\ 0,-1,0)$ — the twists of each joint turning alone at unit rate, which ch.4 names the screw axes $\mathcal{S}_1$ and $\mathcal{S}_2$ and ch.5 stacks as the columns of its Jacobians, $J_b$ before the adjoint and $J_s$ after.
> - **Non-example**: $\mathrm{diag}(R, R)$, "rotate both halves" used with $p \ne 0$. On the shoulder's body twist it returns $(0,0,1;\ -1,1,0)$, the tip's velocity instead of the space twist, whose $v_s$ is $0$. It is right only when $p = 0$, so every offset frame — a tool, a camera — needs the corner.

The figure draws one motion with both descriptions: the elbow turning at $1\,\mathrm{rad/s}$, at the pose of the Worked case.

<svg viewBox="0 0 560 284" style="max-width:100%;height:auto" role="img" aria-label="P2 at the catalog pose with the elbow turning at 1 rad/s: the tip's velocity (−1, 0, 0) and the velocity (0, −1, 0) of the body point at the space origin, both on the radius-1 m circle about the elbow axis; beside it the two six-vectors and the adjoint that relates them.">
  <defs><marker id="mr03avE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="192,80 185.7,80.2 179.5,80.7 173.2,81.5 167.1,82.6 160.9,84.1 154.9,85.9 149,88 143.2,90.4 137.5,93.1 132,96.1 126.6,99.4 121.5,102.9 116.5,106.7 111.7,110.8 107.1,115.1 102.8,119.7 98.7,124.5 94.9,129.5 91.4,134.6 88.1,140 85.1,145.5 82.4,151.2 80,157 77.9,162.9 76.1,168.9 74.6,175.1 73.5,181.2 72.7,187.5 72.2,193.7 72,200" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.55"/>
  <polyline points="72,200 192,200 192,80" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.28"/>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2" marker-end="url(#mr03avE)"><line x1="80" y1="200" x2="128" y2="200"/><line x1="72" y1="192" x2="72" y2="144"/><line x1="192" y1="73" x2="192" y2="28"/><line x1="185" y1="80" x2="104" y2="80"/></g>
  <g><circle cx="192" cy="200" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="192" cy="200" r="2" fill="currentColor"/></g>
  <circle cx="72" cy="200" r="3.6" fill="currentColor"/>
  <circle cx="192" cy="80" r="3.6" fill="currentColor"/>
  <polyline points="202.9,213 204,212 205,210.9 205.9,209.8 206.7,208.5 207.4,207.2 208,205.8 208.4,204.4 208.7,203 208.9,201.5 209,200 208.9,198.5 208.7,197 208.4,195.6 208,194.2 207.4,192.8 206.7,191.5 205.9,190.2 205,189.1 204,188 202.9,187 201.8,186.1 200.5,185.3 199.2,184.6 197.8,184 196.4,183.6 195,183.3 193.5,183.1 192,183 190.5,183.1 189,183.3 187.6,183.6 186.2,184 184.8,184.6 183.5,185.3 182.2,186.1 181.1,187 180,188 179,189.1 178.1,190.2 177.3,191.5 176.6,192.8 176,194.2 175.6,195.6 175.3,197 175.1,198.5 175,200 175.1,201.5 175.3,203 175.6,204.4" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#mr03avE)"/>
  <g stroke="currentColor" stroke-width="2.8" marker-end="url(#mr03avE)"><line x1="187" y1="80" x2="132" y2="80"/><line x1="72" y1="205" x2="72" y2="260"/></g>
  <g font-size="11" fill="currentColor">
    <text x="130" y="214">x̂<tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
    <text x="64" y="148" text-anchor="end">ŷ<tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
    <text x="62" y="194" text-anchor="end" font-size="12">{s}</text>
    <text x="200" y="36">x̂<tspan dy="3.5">b</tspan><tspan dy="-3.5"></tspan></text>
    <text x="100" y="84" text-anchor="end">ŷ<tspan dy="3.5">b</tspan><tspan dy="-3.5"></tspan></text>
    <text x="201" y="85" font-size="12">{b}</text>
    <text x="204" y="220">q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="214" y="190">1 rad/s</text>
    <text x="184" y="69" text-anchor="end">ṗ = (−1, 0, 0) m/s, along +ŷ<tspan dy="3.5">b</tspan><tspan dy="-3.5"></tspan></text>
    <text x="81" y="244">v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= (0, −1, 0)</tspan></text>
    <text x="81" y="259" opacity="0.85">body point at the origin</text>
    <text x="89.1" y="129.1" text-anchor="end" opacity="0.8">1 m from the axis</text>
    <text x="300" y="30" font-size="12">Elbow at 1 rad/s, catalog pose</text>
    <text x="300" y="57" opacity="0.85">Written in {b}, v at the tip:</text>
    <text x="312" y="74">V<tspan dy="3.5">b</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1; 0, 1, 0): ṗ in tip axes</tspan></text>
    <text x="300" y="95" opacity="0.85">Written in {s}, v at the origin:</text>
    <text x="312" y="112">V<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1; 0, −1, 0)</tspan></text>
    <text x="300" y="133" opacity="0.85">The adjoint relates them, T = T<tspan dy="3.5">sb</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="300" y="150">V<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= [Ad</tspan><tspan dy="3.5">T</tspan><tspan dy="-3.5">] V</tspan><tspan dy="3.5">b</tspan><tspan dy="-3.5">, and its corner:</tspan></text>
    <text x="300" y="167">v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= R v</tspan><tspan dy="3.5">b</tspan><tspan dx="3.1" dy="-3.5">+ p × ω</tspan><tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
    <text x="312" y="184">= (−1, 0, 0) + (1, −1, 0)</text>
    <text x="300" y="207" opacity="0.85">diag(R, R) drops the corner: (−1, 0, 0),</text>
    <text x="312" y="224" opacity="0.85">the tip's ṗ, not v<tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
  </g>
</svg>

P2's elbow turning at $1\,\mathrm{rad/s}$ about its axis, the $\hat z$ axis through $q_2 = (1, 0, 0)$, out of the page, at the catalog pose. The tip and the base origin both lie $1\,\mathrm m$ from that axis, so both move at $1\,\mathrm{m/s}$ along the dashed circle: the tip at $\dot p = (-1, 0, 0)$, which in tip axes is $v_b = (0, 1, 0)$, and the body point at the origin at $v_s = (0, -1, 0)$. One motion gives two six-vectors, $\mathcal{V}_b = (0,0,1;\ 0,1,0)$ and $\mathcal{V}_s = (0,0,1;\ 0,-1,0)$, and $[\mathrm{Ad}_{T_{sb}}]$ ties them by adding its corner, $p \times \omega_s = (1, -1, 0)$, to $Rv_b = (-1, 0, 0)$.

### 5. The pose exponential and logarithm on SE(3)

Ch.4 builds every pose of the arm out of joint motions, and ch.6 needs a pose *error* that a Jacobian can act on: the exponential gives the first — ch.4's product of exponentials is nothing else — and the logarithm the second, since numerical IK ([[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6 §2]]) iterates on $[\log(T_{now}^{-1}T_{goal})]^\vee$, where $^\vee$ reads the six coordinates back out of the $4\times4$ matrix.

*In one sentence:* a whole pose — rotation and position together — is reached by following one screw for one amount, so it is the exponential of a twist, and the logarithm reads that screw and that amount back from any pose.

*If you need only one thing from this section:* the translation column is $G(\theta)v$, not $v\theta$, because the rotation carries the linear velocity round as it goes — on P2's elbow screw at a quarter turn this puts the origin at $(1,-1,0)$, where the naive form puts it at $(0,-1.5708,0)$ (5.1's example and non-example).

§2 turned a rotation axis and an angle into a rotation matrix; this section does the same for a whole pose, then inverts it. Here a **screw axis** is a twist $\mathcal{S} = (\omega, v)$ of §3 normalized in one of two ways: either $\|\omega\| = 1$, and $\theta$ is an angle in radians turned about the axis, or $\omega = 0$ and $\|v\| = 1$, and $\theta$ is a distance in metres slid along $v$. Its bracket is the $4\times4$ element of $\mathfrak{se}(3)$ from §3,

$$[\mathcal{S}] = \begin{pmatrix}[\omega] & v\\ 0 & 0\end{pmatrix}$$

and following the screw for $\theta$ from the identity is the linear ODE $dT/d\theta = [\mathcal{S}]\,T$ with $T(0) = I$ — §2's $\dot R = [\omega_s]R$ one size up — so its solution is the matrix exponential $T = e^{[\mathcal{S}]\theta}$.

**The axis inside the screw.** With $\|\omega\| = 1$ the six numbers are a point $q$ on the axis and the pitch $h$ of §3, $\mathcal{S} = (\omega,\ -\omega\times q + h\,\omega)$ (MR Def. 3.24): P2's revolute joints have $h = 0$, so the elbow through $q_2 = (1,0,0)$ is $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$, and a joint turning at rate $\dot\theta$ has the twist $\mathcal{V} = \mathcal{S}\dot\theta$. *Non-example*: that twist at $\dot\theta = 2\,\mathrm{rad/s}$, $(0,0,2;\ 0,-2,0)$, is not a screw axis, since $\|\omega\| = 2$; fed to 5.1's closed form with $\theta = \pi/2$, it returns a rotation block whose columns have length $3.606$. The motion it stands for is $\mathcal{S}_2$ followed for $\theta = \pi$, a half turn about the elbow. Normalizing first is what lets ch.4 read each exponent's $\theta$ as a joint angle.

**5.1 The closed form.** Every power of $[\mathcal{S}]$ keeps the same pattern, $[\mathcal{S}]^k = \begin{pmatrix}[\omega]^k & [\omega]^{k-1}v\\ 0 & 0\end{pmatrix}$ for $k \ge 1$, so the series splits into a rotation block and a translation column:

$$e^{[\mathcal{S}]\theta} = \begin{pmatrix} e^{[\omega]\theta} & G(\theta)\,v \\ 0 & 1 \end{pmatrix}, \qquad G(\theta) = I\theta + [\omega]\frac{\theta^2}{2!} + [\omega]^2\frac{\theta^3}{3!} + [\omega]^3\frac{\theta^4}{4!} + \cdots$$

The rotation block is Rodrigues' formula of §2. For $G$, the same identity $[\omega]^3 = -[\omega]$ folds the series: the $[\omega]$ terms collect $\theta^2/2! - \theta^4/4! + \cdots = 1 - \cos\theta$ and the $[\omega]^2$ terms collect $\theta^3/3! - \theta^5/5! + \cdots = \theta - \sin\theta$, so

$$G(\theta) = I\theta + (1-\cos\theta)\,[\omega] + (\theta-\sin\theta)\,[\omega]^2 \qquad (\|\omega\| = 1)$$

which is MR Prop. 3.25. Read it physically: $G(\theta)v = \int_0^\theta e^{[\omega]\varphi}v\,d\varphi$ is the linear velocity $v$, carried round by the rotation accumulated so far and summed over the motion; integrating Rodrigues' formula term by term gives the same three coefficients.

- **Example, on P2.** The elbow screw $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$ through $q_2 = (1,0,0)$, at $\theta = \pi/2$. With $[\hat z]^2 = \mathrm{diag}(-1,-1,0)$, $1 - \cos\frac{\pi}{2} = 1$ and $\frac{\pi}{2} - \sin\frac{\pi}{2} = 0.5708$:

  $$G(\tfrac{\pi}{2}) = \begin{pmatrix}1&-1&0\\1&1&0\\0&0&\pi/2\end{pmatrix}, \qquad G v_2 = \begin{pmatrix}1\\-1\\0\end{pmatrix}, \qquad e^{[\mathcal{S}_2]\pi/2} = \begin{pmatrix}0&-1&0&1\\1&0&0&-1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

  since the first two diagonal entries of $G$ are $\frac{\pi}{2} - 0.5708 = 1$. The translation column is where the origin goes: it sits at $-q_2 = (-1,0)$ from the axis, a quarter turn takes that to $(0,-1)$, and adding $q_2$ back gives $(1,-1)$. The elbow itself, on the axis, stays put: $R_z(90^\circ)(1,0,0) + (1,-1,0) = (1,0,0)$.
- **Non-example.** $\begin{pmatrix} e^{[\omega]\theta} & v\theta \\ 0 & 1\end{pmatrix}$, rotating and translating as if the two were independent. For $\mathcal{S}_2$ it puts the origin at $(0,-1.5708,0)$ instead of $(1,-1,0)$ and moves the elbow to $(0,-0.5708,0)$ — a revolute joint whose own axis moves. The correction $G(\theta) - I\theta$ is exactly the rotation's effect on the translation.

**5.2 Pure translation.** When $\omega = 0$, $[\mathcal{S}]^2 = 0$ (the top-left block is zero, so the product has nothing left), and the series stops after its linear term:

$$e^{[\mathcal{S}]\theta} = \begin{pmatrix} I & v\,\theta \\ 0 & 1 \end{pmatrix} \qquad (\omega = 0,\ \|v\| = 1)$$

— the infinite-pitch screw of §3, a slide of $\theta$ metres along $v$ with no rotation. The rotational formula happens to give the same $G = I\theta$ when $[\omega] = 0$, but its $\theta$ is an angle and this one is a length, which is why the two cases are stated apart. *On P2*: the home pose $M$ of [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]], tip at $(2,0,0)$ with $R = I$, is exactly this with $v = (1,0,0)$ and $\theta = 2\,\mathrm{m}$.

**5.3 The matrix logarithm.** The inverse question: given $T = (R, p)$, find a screw $\mathcal{S}$ and $\theta$ with $e^{[\mathcal{S}]\theta} = T$. Such a pair always exists — every rigid displacement is a motion along one screw (the Chasles–Mozzi theorem) — and the closed form says how to read it off (MR §3.3.3.2):

1. If $R = I$, the motion is a pure translation: $\omega = 0$, $\theta = \|p\|$, $v = p/\|p\|$.
2. Otherwise take the rotation's logarithm first. The trace of Rodrigues' formula is $\operatorname{tr}R = 3 - 2(1-\cos\theta) = 1 + 2\cos\theta$, because $\operatorname{tr}[\omega] = 0$ and $\operatorname{tr}[\omega]^2 = -2\|\omega\|^2 = -2$; and $R - R^\top = 2\sin\theta\,[\omega]$, because $[\omega]$ is antisymmetric while $I$ and $[\omega]^2$ are symmetric. So, for $\theta \in (0, \pi)$,

$$\theta = \arccos\frac{\operatorname{tr}R - 1}{2}, \qquad [\omega] = \frac{R - R^\top}{2\sin\theta}, \qquad v = G^{-1}(\theta)\,p$$

with the inverse of 5.1's $G$,

$$G^{-1}(\theta) = \frac{1}{\theta}\,I - \frac{1}{2}\,[\omega] + \Bigl(\frac{1}{\theta} - \frac{1}{2}\cot\frac{\theta}{2}\Bigr)[\omega]^2$$

which you can confirm by multiplying out $G\,G^{-1}$ with $[\omega]^3 = -[\omega]$ and $[\omega]^4 = -[\omega]^2$. At $\theta = \pi$, where $\sin\theta = 0$, read the axis from $R = I + 2[\omega]^2 = 2\omega\omega^\top - I$ instead, i.e. $\omega\omega^\top = (R + I)/2$.

- **Example, on P2.** Three logarithms, one per case. (i) $e^{[\mathcal{S}_2]\pi/2}$ of 5.1: $\operatorname{tr}R = 1$ gives $\theta = \pi/2$, $(R - R^\top)/2 = [\hat z]$, and $G^{-1}(\frac{\pi}{2}) = \begin{pmatrix}0.5&0.5&0\\-0.5&0.5&0\\0&0&2/\pi\end{pmatrix}$ takes $p = (1,-1,0)$ to $v = (0,-1,0)$: $\mathcal{S}_2$ comes back. (ii) the Worked case's $T_{sb}$, same $R$ but $p = (1,1,0)$: $v = G^{-1}p = (1,0,0)$, and $v = -\omega\times q$ puts the axis through $q = (0,1,0)$. The tool frame is reached from $\{s\}$ by one quarter turn about the $\hat z$ axis through $(0,1)$, a point on neither link, which is why a logarithm's screw is a property of the displacement, not of the arm. (iii) $M$: $R = I$, so case 1 gives $\theta = 2$ and $v = (1,0,0)$, the slide of 5.2.
- **Non-example.** The screw read off as $v = p/\theta$, the rotation's logarithm with the position simply divided by the angle — 5.1's non-example run backwards. For the Worked case's $T_{sb}$ it gives $v = (0.6366,\ 0.6366,\ 0)$ instead of $(1,0,0)$, and following that screw for $\pi/2$ puts the tool at $(0,\ 1.2732)$, $1.04\,\mathrm{m}$ from where it is: only $G^{-1}$ undoes the rotation's sweep of the translation.

The block below checks every number of this section: the closed form against the raw power series, the pure translation, and the three logarithms with a round trip through the exponential.

```python
# Pose exponential and logarithm on SE(3), checked on P2's screws (§5).
import numpy as np

def bracket(w):
    x, y, z = w
    return np.array([(0, -z, y), (z, 0, -x), (-y, x, 0)], float)

def exp_screw(S, th):
    """e^{[S]th} by the closed form: 5.1 for a unit omega, 5.2 for omega = 0."""
    w, v = np.asarray(S[:3], float), np.asarray(S[3:], float)
    T = np.eye(4)
    if np.allclose(w, 0):
        T[:3, 3] = v * th
        return T
    W = bracket(w)
    T[:3, :3] = np.eye(3) + np.sin(th) * W + (1 - np.cos(th)) * W @ W
    G = np.eye(3) * th + (1 - np.cos(th)) * W + (th - np.sin(th)) * W @ W
    T[:3, 3] = G @ v
    return T

def exp_series(S, th, terms=40):
    """The same exponential by summing its power series, as an independent check."""
    X = np.zeros((4, 4))
    X[:3, :3], X[:3, 3] = bracket(S[:3]), S[3:]
    out, term = np.eye(4), np.eye(4)
    for k in range(1, terms):
        term = term @ (X * th) / k
        out = out + term
    return out

def log_pose(T):
    """(S, th) with e^{[S]th} = T, by 5.3; valid for R = I or th in (0, pi)."""
    R, p = T[:3, :3], T[:3, 3]
    if np.allclose(R, np.eye(3)):
        th = np.linalg.norm(p)
        return np.r_[0, 0, 0, p / th], th
    th = np.arccos((np.trace(R) - 1) / 2)
    W = (R - R.T) / (2 * np.sin(th))
    w = np.array([W[2, 1], W[0, 2], W[1, 0]])
    Ginv = np.eye(3) / th - W / 2 + (1 / th - 1 / (2 * np.tan(th / 2))) * W @ W
    return np.r_[w, Ginv @ p], th

S2 = np.array([0, 0, 1, 0, -1, 0.])     # elbow screw, axis through q2 = (1, 0, 0)
M = np.eye(4)
M[0, 3] = 2                              # P2's home pose: tip at (2, 0, 0), R = I
E2 = exp_screw(S2, np.pi / 2)
T_sb = E2 @ M                            # the tool pose of the Worked case
print("e^[S2]pi/2 =\n", E2.round(4) + 0.0)
print("closed form = series:", np.allclose(E2, exp_series(S2, np.pi / 2)))
print("M is a pure translation:", np.allclose(exp_screw([0, 0, 0, 1, 0, 0], 2.0), M))
for name, T in [("e^[S2]pi/2", E2), ("T_sb", T_sb), ("M", M)]:
    S, th = log_pose(T)
    print(f"log {name}: S = {S.round(4) + 0.0}, theta = {th:.4f},",
          "round trip:", np.allclose(exp_screw(S, th), T))
```

It prints $e^{[\mathcal{S}_2]\pi/2}$ as above, `closed form = series: True`, `M is a pure translation: True`, and the three logarithms $(0,0,1;\ 0,-1,0)$ at $\theta = 1.5708$, $(0,0,1;\ 1,0,0)$ at $1.5708$ and $(0,0,0;\ 1,0,0)$ at $2.0000$, each with a `True` round trip.

**Why learning people should care**: exp/log maps are how you interpolate poses, average
rotations, and define losses on SE(3) — the machinery under diffusion and flow action heads
that generate tool poses on SE(3). A joint-space head such as [[01-canonical-papers/notes/4-vla/pi0|π0]]'s,
which outputs joint chunks, needs ch.4's forward kinematics before its output is a pose.

### 6. Wrenches — the force dual of twists

A six-axis force–torque sensor at the wrist reports a force and a moment in its own frame, and ch.5 must turn a force at the tool into joint torques, $\tau = J^\top\mathcal{F}$ ([[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §3]]): both need the push written as one six-vector that changes frame correctly, and grasp analysis in [[04-robotics/modern-robotics/ch12-grasping|ch.12]] sums such six-vectors from every contact. A twist says how a body moves; a **wrench** says how it is pushed. It is the six-vector that collects a moment and a force acting on a rigid body, both written in one frame $\{a\}$:

$$\mathcal{F}_a = (m_a,\ f_a) \in \mathbb{R}^6, \qquad m_a = r_a \times f_a$$

where $f_a$ is the linear force in newtons, $r_a$ is any point on its line of action in $\{a\}$ coordinates, and $m_a$ is the moment, in N·m, that the force exerts about the origin of $\{a\}$ (the moment of a force, [[02-foundations/basic-mechanics|0.6.1 §7]]). The definition has three conditions: both halves are expressed in the same frame; the moment is taken about that frame's *origin*, so — exactly like a twist's $v$ in §3 — the moment half changes when the reference point moves even though the force does not; and wrenches acting on one body add componentwise only when written in the same frame. Sliding $r_a$ along the force's own line changes nothing, since the added part is parallel to $f_a$ and its cross product with $f_a$ vanishes. A wrench with $f = 0$ is a **pure moment**. The order, moment first, matches the twist's $(\omega, v)$ so that the two pair component by component.

**Power.** A body point at $r_a$ moves at $v_a + \omega_a \times r_a$ (the velocity field of §3), so a force $f_a$ applied there delivers $f_a\cdot(v_a + \omega_a\times r_a) = v_a\cdot f_a + \omega_a\cdot(r_a\times f_a)$, the last step by the cyclic rule of the scalar triple product, $a\cdot(b\times c) = b\cdot(c\times a) = c\cdot(a\times b)$. Hence

$$P = \mathcal{V}_a^\top\mathcal{F}_a = \omega_a\cdot m_a + v_a\cdot f_a$$

in watts: rotation against moment plus translation against force. This pairing is why the moment goes with $\omega$ and the force with $v$.

**Frame change.** Power is physical, so it cannot depend on the frame it is written in: $\mathcal{V}_b^\top\mathcal{F}_b = \mathcal{V}_a^\top\mathcal{F}_a$ for every motion. Substituting §4's $\mathcal{V}_a = [\mathrm{Ad}_{T_{ab}}]\mathcal{V}_b$ gives $\mathcal{V}_b^\top\mathcal{F}_b = \mathcal{V}_b^\top[\mathrm{Ad}_{T_{ab}}]^\top\mathcal{F}_a$ for every $\mathcal{V}_b$, so

$$\mathcal{F}_b = [\mathrm{Ad}_{T_{ab}}]^\top\,\mathcal{F}_a$$

(MR Prop. 3.27): twists change frame through the adjoint and wrenches through its transpose. Written out with the block form of §4, $f_b = R^\top f_a$ and $m_b = R^\top(m_a - p\times f_a)$ — rotate the force, and move the moment's reference point from $\{a\}$'s origin to $\{b\}$'s origin at $p$.

- **Example, on P2.** The force of [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]]'s statics, $f = (0,-10,0)\,\mathrm{N}$ applied by the tool at the tip $p = (1,1,0)$, with $T_{sb}$ from the Worked case. In $\{s\}$ the moment is $p\times f = (0,0,-10)\,\mathrm{N\,m}$, so $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$. In $\{b\}$, $\mathcal{F}_b = [\mathrm{Ad}_{T_{sb}}]^\top\mathcal{F}_s = (0,0,0;\ -10,0,0)$: no moment, because the force acts at $\{b\}$'s own origin, and a force along $-\hat x_b$, straight back down the forearm. Power checks the pair. Turning joint 1 at $1\,\mathrm{rad/s}$ is the space twist $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$, and $\mathcal{S}_1^\top\mathcal{F}_s = -10\,\mathrm{W}$; the same motion written in $\{b\}$ is $(0,0,1;\ 1,1,0)$, and pairing it with $\mathcal{F}_b$ gives $1\cdot(-10) = -10\,\mathrm{W}$ again. With joint 2's screw $\mathcal{S}_2$ the pairing is $1\cdot(-10) + (-1)(-10) = 0$. Those two numbers are the joint torques $\tau = (-10, 0)\,\mathrm{N\,m}$ of [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §3]], because a joint torque is the power delivered per unit joint rate.
- **Non-example.** $\mathcal{F}_s = (0,0,0;\ 0,-10,0)$, the force with its moment dropped as if it acted at the base. Paired with $\mathcal{S}_1$ it gives $0\,\mathrm{W}$: it claims the shoulder holds a $10\,\mathrm{N}$ load on a $1\,\mathrm{m}$ lever arm for free. A wrench's moment belongs to a reference point, and forgetting it is §3's $v_s$-versus-$\dot p$ error in force form.

```python
# The 10 N tip force of ch.5 as a wrench, in {s} and in {b}, and its power (§6).
def adjoint(T):
    R, p = T[:3, :3], T[:3, 3]
    A = np.zeros((6, 6))
    A[:3, :3], A[3:, 3:], A[3:, :3] = R, R, bracket(p) @ R
    return A

p, f = T_sb[:3, 3], np.array([0, -10, 0.])
F_s = np.r_[np.cross(p, f), f]                  # (m_s, f_s): moment about the base
F_b = adjoint(T_sb).T @ F_s                      # frame change by the adjoint transpose
S1 = np.array([0, 0, 1, 0, 0, 0.])              # shoulder screw
V1_b = adjoint(np.linalg.inv(T_sb)) @ S1         # joint 1 at 1 rad/s, written in {b}
print("F_s =", F_s + 0.0, " F_b =", F_b.round(4) + 0.0)
print("power of joint 1 in {s}:", float(S1 @ F_s), " in {b}:", round(float(V1_b @ F_b), 4))
print("tau = (S1.F_s, S2.F_s) =", (float(S1 @ F_s), float(S2 @ F_s)))
```

It prints $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$ and $\mathcal{F}_b = (0,0,0;\ -10,0,0)$, the power $-10$ in both frames, and $\tau = (-10, 0)$.

### Self-check

1. Verify Rodrigues for $\theta = 180°$ about $\hat z$. What matrix do you get?
2. A body rotates about an axis through the point $(0, 2, 0)$ (axis direction $\hat z$,
   speed 1 rad/s). What is its space twist $\mathcal{V}_s = (\omega_s, v_s)$?
3. Why does $[\hat\omega]^3 = -[\hat\omega]$ terminate the exponential series?
4. If $T$ is a pure translation by $p$, what does $[\text{Ad}_T]$ do to a twist?
5. What is $e^{[\mathcal{S}_1]\pi/2}$ for P2's shoulder screw $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$, and why is its translation column zero?
6. The tip force is $f = (10, 0, 0)\,\mathrm{N}$ instead, still at $p = (1,1,0)$. Write $\mathcal{F}_s$ and the two joint torques $\mathcal{S}_i^\top\mathcal{F}_s$.

> [!tip]- Answers
> 1. $\sin 180° = 0$ and $1-\cos 180° = 2$, so $R = I + 0 + 2[\hat z]^2 = \text{diag}(-1,-1,1)$ — the x and y axes flip, z is untouched.
> 2. $\omega_s = (0,0,1)$; the space-frame linear part is $v_s = -\omega \times q = -(0,0,1)\times(0,2,0) = (2,0,0)$ — the body point currently at the origin moves at 2 m/s in $+x$, even though the axis itself is stationary. This is §3's warning made numerical.
> 3. Because powers of a $3\times3$ skew-symmetric matrix cycle back to multiples of itself ($[\hat\omega]^3 = -[\hat\omega]$), every term of the infinite series collapses into a coefficient on $[\hat\omega]$ or $[\hat\omega]^2$ — leaving Rodrigues' three terms.
> 4. It leaves $\omega$ unchanged and maps $v \mapsto v + p\times\omega$ — the linear velocity is corrected by exactly the offset of the axis, which is why frame subscripts must be written every time.
> 5. $v_1 = 0$, so $G(\theta)v_1 = 0$ and $e^{[\mathcal{S}_1]\pi/2} = \begin{pmatrix}R_z(90^\circ) & 0\\ 0 & 1\end{pmatrix}$: the axis passes through the origin, so the origin does not move (§5.1).
> 6. $m_s = p\times f = (0,0,-10)$, so $\mathcal{F}_s = (0,0,-10;\ 10,0,0)$. Then $\tau_1 = \mathcal{S}_1^\top\mathcal{F}_s = -10$ and $\tau_2 = \mathcal{S}_2^\top\mathcal{F}_s = 1\cdot(-10) + (-1)\cdot 0 = -10\,\mathrm{N\,m}$ — the same $(-10,-10)$ that ch.5's $J^\top(10, 0)$ gives (§6).

### Problem set · 과제

Tier B. Using **P2** from [[02-foundations/lab-plants|0.6]], at the catalog pose $\theta=(0^\circ,90^\circ)$ and at the raised pose $\theta=(90^\circ,0^\circ)$. No simulator.

1. **Draw.** The picture above for the arm raised straight up, $\theta=(90^\circ,0^\circ)$: base frame $\{s\}$ at the origin, elbow at $(0,1)$, tip at $(0,2)$, and the tool frame $\{b\}$ at the tip with its $x$-axis along the forearm. Add the axis through the elbow, $\hat\omega=(0,0,1)$ at $1\,\mathrm{rad/s}$, and write beside the figure the tip's velocity and the space twist's linear part. Which way does each point?
2. **Derive.** At the raised pose $\theta=(90^\circ,0^\circ)$: (a) write $T_{sb}$; (b) turn the shoulder at $1\,\mathrm{rad/s}$ and write the space twist $\mathcal{V}_s$ and the body twist $\mathcal{V}_b$ of that motion, then check $\mathcal{V}_s=[\mathrm{Ad}_{T_{sb}}]\mathcal{V}_b$; (c) at the catalog pose the same motion had $\mathcal{V}_s=(0,0,1;\ 0,0,0)$ and $\mathcal{V}_b=(0,0,1;\ 1,1,0)$ (§3's box) — which of the two six-vectors changed with the pose, and why? (d) Give the tip's velocity in $\{s\}$ and in $\{b\}$ axes.
3. **Interpret.** (a) Why are $\omega_x$, $\omega_y$ and $v_z$ zero in every twist of P2, at every pose and joint rate? (b) The tool's poses live in SE(2), the planar poses — $x$, $y$ and one heading angle, three numbers — yet P2's configuration space is [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]]'s torus, two numbers. Why is SE(2) the space of the tool's poses but not P2's configuration space? (c) Which tool headings can P2 hold with its tip on the catalog target $(1,1)$? Show that $(1, 1, 45^\circ)$ is not one of them.

> [!note]- How to draw it · 그리는 법
> - Draw the arm first: base at the origin, link 1 straight up to the elbow at $(0,1)$, link 2 straight on up to the tip at $(0,2)$.
> - The space frame $\{s\}$ at the origin: $\hat x_s$ right, $\hat y_s$ up, and $\hat z_s$ as a circled dot meaning out of the page. Draw the dot — a planar figure that does not declare which way $z$ points makes every sign in this chapter a coin flip.
> - The body frame $\{b\}$ at the tip, with $\hat x_b$ along the forearm, i.e. along $+\hat y_s$ — the same $R_{sb}$ as in the picture above. Right-handedness then puts $\hat y_b$ along $-\hat x_s$ and $\hat z_b$ out of the page again.
> - The offset $p=(0,2,0)$ as a dashed arrow from the origin to the tip. $R_{sb}$ and $p$ are the whole of $T_{sb}$, and only $p$ changed.
> - The rotation axis as a circled dot with a curved arrow around it at the elbow, $q=(0,1,0)$, labelled with $\hat\omega$ and $\dot\theta=1\,\mathrm{rad/s}$.
> - Write velocities beside the figure, not inside it: the tip's actual velocity $\hat\omega\times(p-q)$ next to the twist's linear part $v_s=-\hat\omega\times q$, each as a short arrow. The tip sits one metre above the axis and the space origin one metre below it, so the two arrows point opposite ways; if yours agree, you wrote $\dot p$ where the twist wants $v_s$.

> [!tip]- Solutions
> 1. The forearm points along $+\hat y_s$, so again $\hat x_b=\hat y_s$, $\hat y_b=-\hat x_s$ and $\hat z_b$ out of the page: $R_{sb}=R_z(90^\circ)$ as in the picture, but $p=(0,2,0)$. The elbow axis passes through $q=(0,1,0)$ with $\hat\omega=(0,0,1)$. The tip moves at $\hat\omega\times(p-q)=(0,0,1)\times(0,1,0)=(-1,0,0)\,\mathrm{m/s}$, to the left; the twist's linear part is $v_s=-\hat\omega\times q=(1,0,0)$, to the right. They are equal and opposite: $v_s$ is the velocity of the body point passing through the space origin, one metre below the axis, and the tip is one metre above it.
> 2. (a) The forearm again points along $+\hat y_s$, so $R_{sb}=R_z(90^\circ)$ as in the Worked case, and only $p$ changed: $p=(0,2,0)$, so $T_{sb}$ has the rotation columns $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ and the translation $(0,2,0)$. (b) The shoulder axis passes through the origin, so $\mathcal{V}_s=(0,0,1;\ 0,0,0)$, exactly as at the catalog pose. In $\{b\}$, $\omega_b=R^\top(0,0,1)=(0,0,1)$ and $v_b=R^\top\dot p$ with $\dot p=\hat z\times p=(-2,0,0)$, so $v_b=(0,2,0)$ and $\mathcal{V}_b=(0,0,1;\ 0,2,0)$. Check: $v_s=Rv_b+p\times\omega_s=(-2,0,0)+(2,0,0)=0$. (c) The space twist did not change and the body twist did. $v_s$ belongs to the body point at the base origin, which lies on the shoulder axis at every pose, so it stays $0$; $v_b$ belongs to the tip, now $2\,\mathrm m$ from the axis instead of $\sqrt2$, so it changes whenever the tip moves relative to the axis. (d) $\dot p=(-2,0,0)\,\mathrm{m/s}$ in $\{s\}$, to the left; in tip axes that is $(0,2,0)$, along $+\hat y_b$, which points along $-\hat x_s$.
> 3. (a) Both joint axes are parallel to $\hat z$ and pass through points $q_i$ of the plane $z=0$, so every twist of P2 is a combination of $(0,0,1;\ -\hat z\times q_i)$: $\omega$ lies along $\hat z$, and $-\hat z\times q_i$ lies in the plane, so $\omega_x=\omega_y=v_z=0$. Only three of the six numbers ever move, which is why the tool's motion fits in SE(2). (b) A configuration is a point of the torus $T^2$, two joint angles, and forward kinematics sends it to one tool pose; those images form a two-dimensional surface inside the three-dimensional SE(2), so most planar poses are nobody's image. SE(2) is where a task writes the tool's goals — the task space of [[04-robotics/modern-robotics/ch02-configuration-space|ch.2 §1.5]] — not where the robot lives. (c) The elbow must be $1\,\mathrm m$ from the base and $1\,\mathrm m$ from the tip, so a heading $\varphi$ is possible only if $(1-\cos\varphi)^2+(1-\sin\varphi)^2=1$, i.e. $\cos\varphi+\sin\varphi=1$, which holds only at $\varphi=0^\circ$ (contact B of ch.2, $\theta=(90^\circ,-90^\circ)$) and $90^\circ$ (contact A, the catalog pose). At $45^\circ$ the elbow would sit at $(1,1)-(\cos45^\circ,\sin45^\circ)=(0.293,\ 0.293)$, $0.414\,\mathrm m$ from the base.

### Sources

- K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — ch.3: §3.2 for rotations, angular velocity and exponential coordinates, §3.3 for twists, the adjoint, screws and the matrix logarithm, §3.4 for wrenches; the [[04-robotics/modern-robotics-book|book guide]] links the free PDF.
- The numbers on this page and its two listings were computed here from P2's catalog pose; recompute them rather than trusting them.

## 한국어

**핵심 질문**: 강체의 회전·자세·속도를 특이점 없이 어떻게 표현하고 합성하는가?

책에서 가장 길게 느껴지는 장이고, 2–6장이 채우는 로보틱스 회차 열일곱 가운데 다섯(회차 5–9)을 쓴다. 이후의 모든 장이 이 기계장치의 응용이기 때문이다. 네 단계(§1–§4)로 나눠 잡고, 이후 장들이 불러 쓰는 두 단계(§5–§6)를 더하라.

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 조작 층의 언어다. 수학 바닥에 있는 [[02-foundations/se3-geometry|8. SE(3)]]의 회전과 자세를 스크류, 트위스트, 렌치로 이어 가기 때문이다. "*저 패널을 프레임에 설치해*"에서는 두 단계를 받친다. *부재를 옮길* 때는 모든 속도 명령이 이름 붙은 프레임에서 쓴 트위스트이고, *접촉을 감지할* 때는 손목 힘-토크 센서의 렌치를 도구 프레임으로 옮겨야 한다([[physical-ai-map|피지컬 AI 지도]]의 조작 띠에 이 페이지의 자리가 있다). 이것이 없으면 프레임이 소리 없이 속인다. 공간 트위스트의 선형 성분을 말단 속도로 읽으면, P2([[02-foundations/lab-plants|0.6]]의 두 링크 평면 팔)의 어깨가 $1\,\mathrm{rad/s}$로 돌 때 말단은 $(-1, 1, 0)\,\mathrm{m/s}$로 움직이는데도 가만히 있는 것처럼 보인다($v_s = 0$, §3). 렌치의 모멘트를 빼 버리면 어깨가 $1\,\mathrm m$ 지렛대 끝의 $10\,\mathrm N$을 $0\,\mathrm W$로 드는 것처럼 보인다(§6). 뒤 페이지들은 이 페이지를 절 단위로 쓴다. [[04-robotics/modern-robotics/ch04-forward-kinematics|MR 4장]]은 §5의 지수들을 곱해 순기구학을 만들고, [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §1과 §3]]은 §4의 수반(adjoint)으로 물체 야코비안에서 공간 야코비안을 만들고 §6의 일률 짝짓기로 $\tau = J^\top\mathcal{F}$를 유도하며, [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장 §2]]는 §5의 로그를 자세 오차로 쓰고, [[04-robotics/contact-force-tactile|9. 접촉 §4]]는 접촉을 §6의 렌치로 쓰며, [[04-robotics/geometric-perception-calibration|3.5 §7.5]]는 §3과 §5로 카메라를 서보한다. 모두 학위논문 경로([[07-research-program/index|7 §8]])의 블록 2에 있고, 이 페이지는 그중 로보틱스 회차 5–9다. 이 페이지를 마치면 P2의 $T_{sb}$를 쓰고, 관절 축을 exp와 log로 스크류로 바꿨다 되돌리고, 트위스트나 렌치를 $\{s\}$와 $\{b\}$ 사이에서 옮기고, 속도의 선형 성분이 어느 점의 것인지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 한 회차, 로보틱스 회차 5다. '이 페이지의 대상', 그림, '대상으로 한 번 끝까지'를 손으로 풀고, 이어서 §1과 §2를 읽는다. 회차는 페이지를 덮고 $T_{sb}$를 쓰고, $\dot R = \mathrm{diag}(0.2,\ 0.2,\ 0)$에서 $\omega$를 읽어 내고, 스스로 점검 1번을 풀며 끝낸다. 나머지는 회차 6–9다. §3–§4(두 프레임의 트위스트와 수반), 목록이 있는 §5, §6(렌치), 그리고 나머지 스스로 점검과 과제다. §1과 §3의 접힌 *더 깊이* 메모는 두 번째 읽기다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**다. 이 위키가 숫자를 고정해 둔 *장치*(plant, 제어에서 제어 대상인 시스템을 부르는 말) 여섯 가운데 하나로, 길이 $1\,\mathrm m$인 링크 둘로 된 평면 팔이다. $\theta_1$은 $x$축에서, $\theta_2$는 링크 1에 대해 재고, 카탈로그 자세 $\theta = (0°, 90°)$에서 엘보는 $(1, 0)$, 말단은 $(1, 1)\,\mathrm m$에 있다. [[02-foundations/se3-geometry|8. SE(3)]]에서처럼 프레임 둘이 페이지를 끌고 간다. 어깨에 고정된 **공간 프레임**(space frame) $\{s\}$와, 말단의 도구에 고정되고 $\hat x_b$가 전완을 따라가는 **물체 프레임**(body frame) $\{b\}$이며, 둘 다 $\hat z$가 지면 밖을 향한다. 팔의 질량은 여기서 쓰지 않는다.

*범위: 이 페이지는 회전과 자세의 지수와 로그, 두 프레임에서의 트위스트와 렌치, 그리고 그것들을 프레임 사이에서 옮기는 수반을 모두 P2 위에서 가르친다. 사슬의 순기구학([[04-robotics/modern-robotics/ch04-forward-kinematics|4장]])과 야코비안([[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]])은 가르치지 않으며, 그것들은 이 페이지 위에 세워진다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 324" style="max-width:100%;height:auto" role="img" aria-label="카탈로그 자세의 P2에 베이스의 공간 프레임, 말단의 물체 프레임, 점선 오프셋 p = (1, 1, 0), 원점과 엘보를 지나는 회전축 둘을 그리고, 속도 숫자 넷을 옆에 적은 그림.">
  <defs><marker id="mr03hdK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="120,222 260,222 260,82" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.28"/>
  <line x1="126.4" y1="215.6" x2="253.6" y2="88.4" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#mr03hdK)"/>
  <g stroke="currentColor" stroke-width="1.8" marker-end="url(#mr03hdK)"><line x1="127" y1="222" x2="176" y2="222"/><line x1="120" y1="215" x2="120" y2="166"/><line x1="260" y1="76" x2="260" y2="26"/><line x1="254" y1="82" x2="204" y2="82"/></g>
  <g><circle cx="120" cy="222" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="120" cy="222" r="2" fill="currentColor"/></g>
  <g><circle cx="260" cy="222" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="260" cy="222" r="2" fill="currentColor"/></g>
  <g><circle cx="260" cy="82" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="260" cy="82" r="2" fill="currentColor"/></g>
  <path d="M115.1 203.6 L113.5 204.1 L112 204.8 L110.5 205.5 L109.1 206.4 L107.8 207.4 L106.6 208.6 L105.4 209.8 L104.4 211.1 L103.5 212.5 L102.8 214 L102.1 215.5 L101.6 217.1 L101.3 218.7 L101.1 220.3 L101 222 L101.1 223.7 L101.3 225.3 L101.6 226.9 L102.1 228.5 L102.8 230 L103.5 231.5 L104.4 232.9 L105.4 234.2 L106.6 235.4 L107.8 236.6 L109.1 237.6 L110.5 238.5 L112 239.2 L113.5 239.9 L115.1 240.4 L116.7 240.7 L118.3 240.9 L120 241 L121.7 240.9 L123.3 240.7 L124.9 240.4 L126.5 239.9 L128 239.2 L129.5 238.5 L130.9 237.6 L132.2 236.6 L133.4 235.4 L134.6 234.2 L135.6 232.9 L136.5 231.5 L137.2 230 L137.9 228.5 L138.4 226.9" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr03hdK)"/>
  <path d="M241.6 226.9 L242.1 228.4 L242.7 229.8 L243.4 231.2 L244.2 232.6 L245.1 233.8 L246.1 235 L247.2 236.1 L248.4 237.1 L249.7 238 L251 238.8 L252.4 239.4 L253.9 240 L255.4 240.4 L256.9 240.7 L258.4 240.9 L260 241 L261.6 240.9 L263.1 240.7 L264.6 240.4 L266.1 240 L267.6 239.4 L269 238.8 L270.3 238 L271.6 237.1 L272.8 236.1 L273.9 235 L274.9 233.8 L275.8 232.6 L276.6 231.2 L277.3 229.8 L277.9 228.4 L278.4 226.9 L278.7 225.4 L278.9 223.9 L279 222.3 L279 220.8 L278.8 219.2 L278.5 217.7 L278.1 216.2 L277.6 214.7 L276.9 213.3 L276.1 212 L275.3 210.7 L274.3 209.5 L273.2 208.3 L272.1 207.3 L270.8 206.4 L269.5 205.5" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr03hdK)"/>
  <line x1="318" y1="14" x2="318" y2="290" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="176" y="241" text-anchor="middle">x̂<tspan dy="3.5">s</tspan></text>
    <text x="112" y="171" text-anchor="end">ŷ<tspan dy="3.5">s</tspan></text>
    <text x="94" y="208" text-anchor="end" font-size="12">{s}</text>
    <text x="94" y="226" text-anchor="end">ẑ<tspan dy="3.5">s</tspan></text>
    <text x="268" y="36">x̂<tspan dy="3.5">b</tspan></text>
    <text x="200" y="74" text-anchor="end">ŷ<tspan dy="3.5">b</tspan></text>
    <text x="270" y="98" font-size="12">{b}</text>
    <text x="270" y="112">ẑ<tspan dy="3.5">b</tspan></text>
    <text x="180" y="144" text-anchor="end">p = (1, 1, 0)</text>
    <text x="120" y="260" text-anchor="middle">q<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="120" y="276" text-anchor="middle">ω̂ = (0, 0, 1)</text>
    <text x="120" y="292" text-anchor="middle">θ̇ = 1 rad/s</text>
    <text x="260" y="260" text-anchor="middle">q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="260" y="276" text-anchor="middle">ω̂ = (0, 0, 1)</text>
    <text x="260" y="292" text-anchor="middle">θ̇ = 1 rad/s</text>
    <text x="12" y="312" opacity="0.85">⊙ = 지면 밖을 향하는 z축 · 굽은 화살표 = 그 축 둘레로 1 rad/s 회전</text>
    <text x="332" y="26" font-size="12">그림 옆에 적는 것</text>
    <text x="332" y="48">T<tspan dy="3.5">sb</tspan><tspan dy="-3.5">: R</tspan><tspan dy="3.5">sb</tspan><tspan dx="3.1" dy="-3.5">= R</tspan><tspan dy="3.5">z</tspan><tspan dy="-3.5">(90°), p = (1, 1, 0)</tspan></text>
    <text x="332" y="78">축 1, q<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)을 지남</tspan></text>
    <text x="340" y="96" opacity="0.85">말단:</text>
    <text x="380" y="96">ω̂ × p = (−1, 1, 0) m/s</text>
    <text x="340" y="114" opacity="0.85">v<tspan dy="3.5">s</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="380" y="114">−ω̂ × q<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="332" y="144">축 2, q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)을 지남</tspan></text>
    <text x="340" y="162" opacity="0.85">말단:</text>
    <text x="380" y="162">ω̂ × (p − q<tspan dy="3.5">2</tspan><tspan dy="-3.5">) = (−1, 0, 0) m/s</tspan></text>
    <text x="340" y="180" opacity="0.85">v<tspan dy="3.5">s</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="380" y="180">−ω̂ × q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (0, −1, 0)</tspan></text>
    <text x="332" y="212">어느 쪽 v<tspan dy="3.5">s</tspan><tspan dy="-3.5">도 말단 속도가 아니다:</tspan></text>
    <text x="332" y="228">v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= ṗ − ω</tspan><tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">× p이지 ṗ가 아니다.</tspan></text>
  </g>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**, 카탈로그 자세 $\theta = (0^\circ, 90^\circ)$에 베이스의 공간 프레임 $\{s\}$, $\hat x_b$가 전완 방향인 말단의 물체 프레임 $\{b\}$, 점선 오프셋 $p = (1,1,0)$을 그렸다. $R_{sb} = R_z(90^\circ)$와 $p$가 $T_{sb}$의 전부이고, 동그라미 친 점은 지면 밖을 향하는 $z$축이다. 회전축 후보 둘은 모두 $\hat\omega = (0,0,1)$, $1\,\mathrm{rad/s}$로 원점 $q_1$과 엘보 $q_2 = (1,0,0)$을 지나며 말단을 $(-1,1,0)$과 $(-1,0,0)\,\mathrm{m/s}$로 움직이지만, 공간 트위스트의 선형 성분은 $v_s = (0,0,0)$과 $(0,-1,0)$이다 — $v_s = \dot p - \omega_s \times p$이지 $\dot p$가 아니므로 어느 쪽도 말단 속도가 아니다.

### 대상으로 한 번 끝까지 · Worked case

숫자 셋을 손으로 유도한다. 그림의 $T_{sb}$와 어깨가 돌 때의 말단 속도, 그리고 엘보가 돌 때 전완의 각속도다. 각각 [[02-foundations/se3-geometry|8. SE(3)]]에서 되짚는 대상이나 아래 §1–§2가 정의하는 대상을 하나씩 쓰고, 어디서 오는지 함께 적어 둔다.

**1단계 — 도구 자세 $T_{sb}$**([[02-foundations/se3-geometry|8 §3]]을 되짚는다). 카탈로그 자세에서 전완은 $+\hat y_s$를 향하므로 $\hat x_b = \hat y_s$이고, $\hat z_b$가 지면 밖인 오른손 프레임이면 $\hat y_b = -\hat x_s$다. $R_{sb}$의 열은 $\{s\}$로 쓴 $\{b\}$의 축이고, $p$는 말단이다:

$$R_{sb}=R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},\qquad p=(1,1,0),\qquad T_{sb}=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

자세는 회전 블록과 위치 열을 행 $(0,0,0,1)$ 위에 쌓은 것이기 때문이다.

**2단계 — 어깨가 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도를 행렬 곱으로.** 어깨는 원점을 지나는 $\hat z = (0,0,1)$ 둘레로 팔 전체를 돌리므로 말단은 $\hat z \times p$로 움직인다. §1의 대괄호는 "$\hat z$와 외적하기"를 행렬, 곧 8 §1의 $[\hat z]_\times$로 쓴다:

$$[\hat z]\,p = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}\begin{pmatrix}1\\1\\0\end{pmatrix} = \begin{pmatrix}-1\\1\\0\end{pmatrix}\ \mathrm{m/s}$$

대괄호의 $i$번째 행이 외적의 $i$번째 성분을 재현하기 때문이다. 이 속도는 베이스에서 말단으로 가는 선에 수직이고, 그 크기 $\sqrt2 = 1.414\,\mathrm{m/s}$는 축에서 말단까지의 거리 곱하기 $1\,\mathrm{rad/s}$다. 5장의 '대상으로 한 번 끝까지' 1단계는 이 벡터를 야코비안의 열 1이라 부른다.

**3단계 — $\dot R$에서 읽는 각속도.** 엘보를 $-0.2\,\mathrm{rad/s}$로 돌린다. 전완의 절대각은 $\varphi = \theta_1 + \theta_2$라 $R = R_z(\varphi)$이고, 성분마다 연쇄 법칙으로 미분하면 $\dot R = \dot\varphi\,\mathrm{d}R_z/\mathrm{d}\varphi$, $\mathrm{d}R_z/\mathrm{d}\varphi = \begin{pmatrix}-\sin\varphi&-\cos\varphi&0\\ \cos\varphi&-\sin\varphi&0\\ 0&0&0\end{pmatrix}$이다. $\varphi = 90°$에서 이 행렬은 $\mathrm{diag}(-1,\ -1,\ 0)$이므로, $\dot\varphi = -0.2\,\mathrm{rad/s}$이면 $\dot R = \mathrm{diag}(0.2,\ 0.2,\ 0)$이다. 이 행렬은 대칭이라 곧바로 대괄호로 읽으면 도는 전완에 대해 $\omega = 0$을 보고한다. 각속도는 대신 $\dot RR^\top$에서 읽는다(§2의 상자):

$$\dot RR^\top = \begin{pmatrix}0.2&0&0\\0&0.2&0\\0&0&0\end{pmatrix}\begin{pmatrix}0&1&0\\-1&0&0\\0&0&1\end{pmatrix} = \begin{pmatrix}0&0.2&0\\-0.2&0&0\\0&0&0\end{pmatrix} = [(0,\ 0,\ -0.2)]$$

따라서 $\omega = (0, 0, -0.2)\,\mathrm{rad/s}$, 엘보 속도의 부호대로 $\hat z$ 둘레 시계 방향 회전이다.

이 세 단계를 나머지 페이지가 일반화한다. §1은 대괄호에, §2는 각속도와 그 지수에, §3–§4는 프레임마다의 여섯 숫자 속도에, §5–§6은 자세의 지수와 렌치에 이름을 붙인다.

### 1. 반대칭 다리: 외적이 행렬이 된다

회전은 외적투성이다 — $\omega$로 도는 물체의 $r$에 있는 점은 $\omega \times r$로 움직인다. 그런데 외적은 행렬처럼 곱하거나 뒤집거나 지수를 취할 수 없고, 행렬로 쓰면 그럴 수 있다. 그 순간 *회전 동역학에 선형대수가 통째로 적용*되고, §2의 행렬 지수도 여기서 나온다. 이 행렬의 부호 실수는 종이 위에서는 아무 대가가 없고 로봇 위에서야 드러난다. 상자의 비예가 그것을 보인다. [[02-foundations/se3-geometry|8. SE(3) §1]]에서 "$a$와 외적하기"는 반대칭 행렬 $[a]_\times$였음을 되짚자. 이 장은 그런 행렬들의 집합에 $\mathfrak{so}(3)$라는 이름을 붙이고, §2에서 그것들을 회전의 생성자로 쓴다. **표기:** 8은 이 행렬을 $[\omega]_\times$, 수반을 $\mathrm{Ad}_T$로 쓰고, MR과 3–5장은 $[\omega]$와 $[\mathrm{Ad}_T]$로 쓴다. 같은 대상이다.

$\omega = (\omega_1, \omega_2, \omega_3)$에 대해
$$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}, \qquad [\omega]\,v = \omega \times v.$$
한 성분을 직접 검산하라: $[\omega]v$의 첫 행은 $-\omega_3 v_2 + \omega_2 v_3$ —
정확히 $\omega \times v$의 첫 성분이다.

> **대괄호와 $\mathfrak{so}(3)$의 정의.** $\mathfrak{so}(3)$는 *집합*이다. **반대칭**, 곧 $A^\top = -A$인 $3\times3$ 실수 행렬을 모두 모은 것이고, 이 조건 하나가 대각을 0으로 만들고 자유로운 성분 셋을 남긴다. **대괄호**(bracket) $[\cdot]$는 $\mathbb{R}^3$에서 $\mathfrak{so}(3)$로 가는 *선형 사상*이고, 규칙 하나로 정해진다. $[\omega]$는 **외적을 수행한다**. 모든 $v$에 대해 $[\omega]v = \omega\times v$다. 모든 $v$에서 $v^\top(\omega\times v) = 0$이므로 결과는 반대칭이고, 사상이 일대일이라 $\mathfrak{so}(3)$의 원소는 저마다 정확히 한 $\omega$의 $[\omega]$다(MR §3.2.2. 외적 자체는 [[02-foundations/se3-geometry|8. SE(3) §1]]).
>
> $$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix} = -[\omega]^\top, \qquad [\omega]\,v = \omega\times v$$
>
> 여기서 $\omega = (\omega_1, \omega_2, \omega_3)$이고, 각 성분은 $[\omega]v$의 $i$번째 행이 $\omega\times v$의 $i$번째 성분을 재현하도록 그 자리에 놓인다.
>
> - **예**: P2의 어깨 축 $\hat z = (0,0,1)$과 말단 $p = (1,1,0)$. $[\hat z]p = (-1,1,0)$은 어깨가 $1\,\mathrm{rad/s}$로 돌 때의 말단 속도이고, [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §2]]의 $J$의 열 1이다.
> - **비예**: 피연산자를 바꾼 $[p]\hat z = (1,-1,0)$. $[p]$도 멀쩡한 $\mathfrak{so}(3)$의 원소지만 엉뚱한 벡터의 것이다. 속도가 뒤집혀 말단을 $+x$ 쪽, 곧 패널 안으로 보낸다. 아무것도 멈추지 않으므로 이 부호 오류는 로봇 위에서야 드러난다.

말로 한 대괄호, 물리적으로 읽는 부호 배열, 피연산자 순서 점검은 아래에 두 번째 읽기로 접어 둔다.

> [!note]- 더 깊이 · Deeper
> **대괄호가 하는 일.** 벡터 $\omega$에는 각속도 좌표 셋이 있고, 대괄호는 바로 그 세 숫자를 어떤 입력 벡터에든 "$\omega$와 외적하기"를 수행하는 행렬로 포장한다. 새로운 물리 대상도 아니고 성분들이 독립 파라미터도 아니다. 부호는 외적의 오른손 규칙을 담는다.
>
> 회전축에서 떨어진 점에서는 외적이 축과 변위 모두에 수직인 속도 성분을 준다. 축 위의 점에는 그런 속도가 없고, 같은 각속도라면 축에서 먼 점이 더 빠르다. 이 그림을 떠올리면 부호 배열을 외우는 대신 다시 세울 수 있다.
>
> **이해 확인.** 피연산자를 바꾸면 외적 부호가 반대가 되므로 $[\omega]v$와 $[v]\omega$는 서로의 음수다. 행렬 표기는 합성을 쉽게 만들지만 외적을 교환 가능하게 만들지는 않는다. 기하 식을 코드로 옮길 때 순서를 확인한다.

### 2. 왜 지수함수인가? 회전은 선형 미분방정식이다

자이로나 관절 엔코더는 각속도를 보고하고, 방향은 그것을 적분해 얻어야 한다. 그런데 뻔한 한 스텝 $R \leftarrow (I + [\omega]\Delta t)R$은 회전군을 벗어난다. P2의 엘보가 $-0.2\,\mathrm{rad/s}$로 돌 때 $1\,\mathrm s$짜리 한 스텝은 회전 평면에 놓인 $R$의 두 열을 $\sqrt{1+0.2^2} = 1.019804$배로 늘려 $2\%$ 오차를 내고, $0.01\,\mathrm s$ 스텝 $100$번이면 $1.000200$이 남는데 그런 스텝으로 $100\,\mathrm s$를 가면 다시 $2\%$로 자란다. 이 절은 회전이 선형 미분방정식을 따르고 그 정확한 해인 행렬 지수가 어떤 스텝 크기에서도 회전임을 보인다. IMU(관성 측정 장치)의 자이로 측정을 지수들의 곱으로 적분하는 이유가 이것이다([[04-robotics/state-estimation-slam|3. 상태 추정 §7.2]]).

> **각속도의 정의.** 도는 프레임의 **각속도**(angular velocity)는 *벡터*다. 방향은 오른손 규칙으로 향을 정한 **순간 회전축**이고, 길이는 rad/s 단위의 **회전 속도**다(MR §3.2.2). 좌표로 쓰려면 프레임이 필요한데, $\{s\}$에서 본 $\{b\}$의 방향 $R(t)$가 자연스러운 두 프레임을 모두 준다. $\dot RR^\top$와 $R^\top\dot R$는 언제나 **반대칭**이므로($RR^\top = R^\top R = I$를 미분하면 된다) 저마다 정확히 한 벡터의 대괄호다.
>
> $$[\omega_s] = \dot R\,R^\top, \qquad [\omega_b] = R^\top\dot R, \qquad \omega_s = R\,\omega_b$$
>
> 여기서 $\omega_s$는 공간 프레임 $\{s\}$로 쓴 각속도, $\omega_b$는 같은 벡터를 $\{b\}$로 쓴 것이다. 셋째 항등식이 프레임 변환이고, 그래서 아래 미분방정식의 두 형태가 일치한다.
>
> - **예**: 카탈로그 자세의 P2에서 엘보가 $-0.2\,\mathrm{rad/s}$로 돈다. $R = R_z(90°)$, $\dot R = \mathrm{diag}(0.2,\ 0.2,\ 0)$이므로 $\dot RR^\top = R^\top\dot R = [(0,0,-0.2)]$이고 $\omega_s = \omega_b = (0,0,-0.2)\,\mathrm{rad/s}$다. $R$이 $\hat z$ 둘레로 돌아 $\hat z$를 그대로 두므로 둘이 같다.
> - **비예**: 그 $\dot R$를 곧바로 $[\omega]$로 읽는 것. $\dot R$는 대칭이라 비대각 성분이 도는 전완에 대해 $\omega = 0$을 보고한다. $\dot R = [\omega]$는 $R = I$에서만 성립한다. 기록된 자세를 미분하는 코드는 축을 읽기 전에 $R^\top$를 곱해야 한다.

상자의 첫 항등식 오른쪽에 $R$을 곱하고 $R^\top R = I$를 쓰면, 일정한 각속도로 도는 프레임은 공간 프레임에서 표현한 $\omega_s$로 $\dot R = [\omega_s]\,R$을 따르고, 물체 프레임으로는 마찬가지로 $\dot R = R\,[\omega_b]$를 따른다(MR §3.2.2). 두 형태가 같은 이유는 $\omega_s = R\,\omega_b$이고 괄호 행렬을 회전하면 $[R\,\omega_b] = R\,[\omega_b]\,R^\top$이 되어, $[\omega_s]\,R = R\,[\omega_b]\,R^\top R = R\,[\omega_b]$이기 때문이다.
$\dot x = ax$의 행렬판이다 — 그러므로 해도 $e^{at}$의 행렬판이다: 단위축 $\hat\omega$
둘레로 "시간" $\theta$만큼 돌면
$$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2 \quad \text{(로드리게스 공식)}.$$
무한급수가 세 항으로 접히는 이유는 $[\hat\omega]^3 = -[\hat\omega]$이기 때문이다.

**검산 예제** — $\hat z = (0,0,1)$ 둘레 $\theta = 90°$ 회전:
$[\hat z] = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}$, $[\hat z]^2 = \begin{pmatrix}-1&0&0\\0&-1&0\\0&0&0\end{pmatrix}$을 대입하면
$$R = I + (1)[\hat z] + (1)[\hat z]^2 = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$$
— 정확히 $R_z(90°)$이고, $\hat x$를 $\hat y$로 보낸다. 모든 회전은 *하나의* 축-각
지수다(오일러 정리); $\log$가 $R$에서 $(\hat\omega, \theta)$를 복원한다(식은 §5.3). 이 exp/log 쌍이
리 군(회전)과 리 대수(각속도) 사이의 문이고 — 자세를 올바르게 보간하고 평균할 수 있는
이유다.

> **회전의 지수 좌표의 정의.** **지수 좌표**(exponential coordinates)는 회전 $R \in SO(3)$, 곧 $R^\top R = I$이고 $\det R = +1$인 행렬([[02-foundations/se3-geometry|8. SE(3) §1]])을 나타내는 *숫자 셋* $\hat\omega\theta \in \mathbb{R}^3$이고, 세 조건이 이것을 정한다. **축은 단위 벡터**, $\|\hat\omega\| = 1$이다. **각** $\theta$는 그 축 둘레로 오른손 규칙에 따라 잰다. 그리고 **지수를 취하면 $R$로 돌아온다**. $e^{[\hat\omega]\theta} = R$, 곧 $\{s\}$에서 출발해 $\hat\omega$ 둘레로 $1\,\mathrm{rad/s}$로 $\theta$초 도는 프레임이 $R$에서 멈춘다. 모든 회전에 지수 좌표가 있고, 행렬 로그(식은 §5.3)는 $\theta \in [0, \pi]$인 것을 돌려주며 $0 < \theta < \pi$이면 그것이 유일하다(MR §3.2.3).
>
> $$e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2, \qquad \theta = \arccos\frac{\operatorname{tr}R - 1}{2}$$
>
> 여기서 세 항 꼴은 단위 축이 있어야 성립한다. $[\hat\omega]^3 = -[\hat\omega]$에 기대기 때문이고, 일반 $\omega$라면 $[\omega]^3 = -\|\omega\|^2[\omega]$다.
>
> - **예**: 카탈로그 자세에서 P2의 전완 $R_z(90°)$. $\operatorname{tr}R = 1$에서 $\theta = 1.5708$이므로 $\hat\omega\theta = (0,0,1.5708)$이고, 아래에서 엘보가 $-0.2\,\mathrm{rad}$ 돈 뒤에는 $(0,0,1.3708)$이다.
> - **비예**: 엘보의 각속도 $(0,0,-0.2)\,\mathrm{rad/s}$를 축으로, $\theta = 1\,\mathrm{s}$로 넣는 것. 단위 벡터가 아니라서 공식이 길이 $0.995934$인 열을 돌려주고, 그것은 회전이 아니다. 정규화하면 $\hat\omega = (0,0,-1)$, $\theta = 0.2$가 정확히 $R_z(-11.46°)$를 준다. 자이로는 $\omega$를 rad/s로 보고하니, 로드리게스 공식에 넣기 전에 축과 각으로 나눠야 한다.

**P2에서.** 검산 예제는 P2의 전완이다. 카탈로그 자세에서 $\theta_1+\theta_2=90^\circ$이므로 전완 프레임의 방향이 정확히 이 $R_z(90^\circ)$, 곧 '대상으로 한 번 끝까지'의 $R_{sb}$다. 평면 팔의 회전은 모두 하나뿐인 $z$축 둘레이고 한 축 둘레의 회전끼리는 교환되므로, P2에서는 미분방정식의 공간 형태와 물체 형태가 일치해 $\omega_s=\omega_b$다. 책 안내 페이지의 계산 예제([[04-robotics/modern-robotics-book|1. Modern Robotics]])처럼 엘보를 $-0.2$ rad/s로 돌리면 $1$ s 뒤 전완은 $-0.2$ rad 돌아 있다. $\sin(-0.2)=-0.198669$와 $1-\cos0.2=0.019933$을 넣은 로드리게스 공식이 $R_z(78.54^\circ)$를 주고, 이것은 여전히 정확히 정규직교다. 이 절 첫머리의 오일러 스텝이 $2\%$ 놓치는 정확한 답이다.

### 3. 트위스트: 강체의 속도는 여섯 숫자 — 단, $v$를 조심해서 읽어라

P2의 어깨가 $1\,\mathrm{rad/s}$로 돌면 말단은 $(-1, 1, 0)\,\mathrm{m/s}$로 움직이는데, 그 운동의 공간 트위스트는 선형 성분이 $v_s = 0$이다(그림). 강체 속도의 여섯 숫자에는 어느 프레임으로 썼는지, 그 $v$가 어느 점의 것인지가 들어 있고, 그것을 "말단의 속도"로 읽는 것이 가장 흔한 프레임 실수다. [[02-foundations/se3-geometry|8. SE(3) §4]]의 트위스트 $(\omega, v)$를 되짚자. $v$는 프레임 원점에 있는 물체 점의 속도이고, $(1, 0, 0)$을 지나는 관절이면 $v = (0, -1, 0)$이다. 이 절은 두 표준 프레임의 트위스트 $\dot TT^{-1}$와 $T^{-1}\dot T$, 그리고 피치를 가진 스크류를 보탠다.

움직이는 강체의 속도는 **트위스트**(twist) $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$이다.
$4\times4$ 행렬 $[\mathcal{V}] = \begin{pmatrix}[\omega] & v\\ 0 & 0\end{pmatrix}$로 쓰면 SE(3)의 리 대수 $\mathfrak{se}(3)$의 원소이고(§2 각속도의 자세판이다), 여섯 좌표는 $(\omega_x, \omega_y, \omega_z, v_x, v_y, v_z)$다.
**$v$의 뜻은 기준 프레임과 원점에 달렸다.** 공간 트위스트는 고정된 공간 원점을 기준으로 속도장을 나타내고, 물체 트위스트는 움직이는 물체 원점을 쓴다. 이 선택 없이 두 선형 성분을 같은 것으로 읽으면 안 된다. 0이 아닌 모든 트위스트는
**스크류**다: 축 둘레로 돌면서 그 축 방향으로 나아가는 운동이다. **피치** $h$는 축 둘레로
1라디안 도는 동안 그 축 방향으로 얼마나 나아가는가이고 단위는 m/rad다. 즉 $h = 0.01$ m/rad인
스크류는 1라디안 회전마다 축 방향으로 1 cm 나아간다. 나사산의 피치와 같은 뜻이다. 이렇게 읽으면
두 극한이 바로 보인다. 순수 병진은 피치가 **무한대**인 경우이고(돌지 않는데도 나아간다), 순수
회전이 피치 0인 경우다(MR 정의 3.24: 순수 회전이면 $h = 0$, $\omega = 0$이면 $h \to \infty$).

> **공간 트위스트와 물체 트위스트의 정의.** **트위스트**(twist)는 *한 프레임에 붙은 6차원 벡터* $\mathcal{V} = (\omega, v)$, 또는 그 $4\times4$ 행렬 $[\mathcal{V}] \in \mathfrak{se}(3)$이다([[02-foundations/se3-geometry|8. SE(3) §4]]가 프레임 하나에서 정의한다). 두 조건이 그것을 공간 트위스트나 물체 트위스트로 만든다(MR §3.3.2). **두 절반이 한 프레임**: $\omega$와 $v$를 같은 프레임, $\{s\}$나 $\{b\}$로 쓴다. **$v$는 그 프레임 원점의 것**: 트위스트를 쓰는 프레임의 원점을 지나가는 물체 점(실제든 가상이든)의 속도다.
>
> $$[\mathcal{V}_s] = \dot T\,T^{-1} = \begin{pmatrix}[\omega_s] & \dot p - \omega_s\times p\\ 0 & 0\end{pmatrix}, \qquad [\mathcal{V}_b] = T^{-1}\dot T = \begin{pmatrix}[\omega_b] & R^\top\dot p\\ 0 & 0\end{pmatrix}$$
>
> 여기서 $T = T_{sb} = (R, p)$는 $\{b\}$의 자세, $\dot p$는 $\{b\}$ 원점의 속도를 $\{s\}$ 좌표로 쓴 것이다. $\dot T$에 $T^{-1}$를 오른쪽이나 왼쪽에서 곱하는 것이 §2의 $\dot RR^\top$와 $R^\top\dot R$를 한 치수 키운 것이기 때문에 블록이 이런 꼴이 된다.
>
> - **예**: 카탈로그 자세의 P2, 어깨가 $1\,\mathrm{rad/s}$, $\{b\}$는 말단. 말단이 $\dot p = (-1,1,0)$으로 움직이므로 $\mathcal{V}_s = (0,0,1;\ 0,0,0)$, $\mathcal{V}_b = (0,0,1;\ 1,1,0)$이고, 뒤의 것은 말단 속도를 말단 프레임으로 쓴 것이다.
> - **비예**: 회전과 말단 속도를 쌓은 $(\omega_s, \dot p) = (0,0,1;\ -1,1,0)$. $\{s\}$에서는 둘째 조건을 어긴다. $\dot p$는 원점이 아니라 말단의 것이다. 물체 트위스트로는 첫째 조건을 어긴다. $\{s\}$로 쓰였기 때문이다. §4의 수반이나 [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §1]]의 야코비안에 넣으면 팔이 하지 않는 운동을 기술하게 된다.

같은 장부 정리를 말로 — 어느 원점, 어느 축 — 한 것은 아래에 두 번째 읽기로 접어 둔다.

> [!note]- 더 깊이 · Deeper
> **물체 원점과 공간 원점을 나눈다.** $p$가 공간 좌표로 쓴 물체 원점의 위치라 하자. 공간 트위스트의 선형 성분은 $v_s = \dot p - \omega_s \times p$이므로 물체 원점의 속도를 얻으려면 회전 항을 다시 더해야 한다. 물체 트위스트의 선형 성분은 $v_b = R^\top\dot p$로, 물체 원점의 속도를 물체 축으로 쓴 것이다. 따라서 "$v$는 도구 끝 속도가 아니다"에는 프레임이 붙어야 한다. 물체 원점이 도구 끝, 곧 말단에 있으면 $v_b$는 바로 그 말단의 속도를 말단 자신의 축으로 쓴 것이다.
>
> 고정된 자기 말단을 축으로 도는 도구를 상상한다. 말단은 병진하지 않아도 도구의 다른 점들은 움직인다. 공간 원점에서 본 기술은 말단의 경로만이 아니라 속도장 전체를 되살릴 정보를 담아야 하고, 원점을 옮기면 같은 운동을 기술하는 데 필요한 선형 성분이 바뀐다.
>
> **이해 확인.** 숫자를 쓴 프레임과 속도를 알고 싶은 점을 모두 말한다. [공식 트위스트 설명](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-2-twists-part-1-of-2/)이 이 차이를 다룬다. 이를 섞으면 수치적으로 올바른 야코비안도 잘못된 병진을 명령하는 것처럼 보인다.

### 4. 하나의 운동, 두 개의 기술: 공간 프레임 vs 물체 프레임

떨어져 있는 프레임 — 도구, 카메라, 힘 센서 — 은 모두 같은 운동을 다른 숫자로 보고, 그 숫자를 바꾸려면 프레임의 회전뿐 아니라 위치도 있어야 한다. 위치를 빼면 떨어진 프레임마다 선속도가 틀린다. [[02-foundations/se3-geometry|8. SE(3) §4]]의 자세 $T = (R, p)$의 수반 $\mathrm{Ad}_T$를 되짚자. 거기서도 바로 이 $T_{sb}$('대상으로 한 번 끝까지'의 1단계)로 계산했다. 이 절은 그 모서리를 §3의 식에서 유도하고, 켤레 꼴 $T[\mathcal{V}]T^{-1}$을 보태고(합성 규칙은 8이 이미 준다), 뒤 장들이 그것을 어디에 쓰는지 밝힌다. 물체 야코비안을 공간 야코비안으로 바꾸는 데([[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §1]]), 그리고 전치해서 렌치를 옮기는 데(§6)다.

같은 물리적 운동을 공간 프레임에서 쓰면 $\mathcal{V}_s$, 움직이는 물체 프레임에서 쓰면
$\mathcal{V}_b$다. 둘은 현재 자세 $T = (R, p)$의 **수반**(adjoint)으로 연결된다:
$$\mathcal{V}_s = [\text{Ad}_T]\,\mathcal{V}_b, \qquad [\text{Ad}_T] = \begin{pmatrix} R & 0 \\ [p]R & R\end{pmatrix}.$$
윗줄은 $\omega_s = R\,\omega_b$라는 뜻이다. 모서리의 $[p]R$은 §3의 공간 트위스트 식 $v_s = \dot p - \omega_s \times p$에서 나온다: 물체 원점의 속도가 $\dot p = R\,v_b$이므로 $v_s = R\,v_b + p \times \omega_s = R\,v_b + [p]R\,\omega_b$다. 말로 하면, $v_s$는 공간 원점에 놓인 가상의 물체 점(물체 원점에서 $-p$만큼 떨어진 점)을 기술하고, 물체 원점을 중심으로 도는 회전이 그 점을 $p \times \omega_s$만큼 옆으로 쓸고 간다.
외울 가치가 있는 특수 사례: $p = 0$(순수 회전)이면 그냥 "양쪽을 회전"이다:
$\omega_s = R\,\omega_b$, $v_s = R\,v_b$. **프레임 아래 첨자는 장식이 아니다** — 이후
장들의 부호 실수 대부분이 $s$/$b$ 혼동이므로, 매번 아래 첨자를 써라. 자세의 지수도
회전과 같다: $T = e^{[\mathcal{S}]\theta}$ = "스크류 $\mathcal{S}$를 $\theta$만큼
따라가라." 그것을 계산하는 것이 §5다.

> **수반 사상의 정의.** 자세 $T = (R, p) \in SE(3)$([[02-foundations/se3-geometry|8. SE(3) §3]])의 **수반**(adjoint)은 *$6\times6$ 행렬* $[\mathrm{Ad}_T]$이고, 요구 하나로 정해진다. $T = T_{ab}$이면 $\{b\}$로 쓴 트위스트를 같은 운동을 $\{a\}$로 쓴 트위스트로 바꾼다. $[\mathrm{Ad}_T\mathcal{V}] = T[\mathcal{V}]T^{-1}$다(MR 정의 3.20). 여기서 세 성질이 나온다. 고정된 $T$에서 **트위스트에 선형**이다. **자세의 두 절반이 다 필요하다**. $R$은 두 벡터를 모두 돌리고, $p$는 모서리 $[p]R$로 들어온다. 그리고 **자세처럼 합성된다**. $[\mathrm{Ad}_{T_1}][\mathrm{Ad}_{T_2}] = [\mathrm{Ad}_{T_1T_2}]$이므로 역행렬은 전치가 아니라 $[\mathrm{Ad}_{T^{-1}}]$다. 전치는 렌치를 옮긴다(§6).
>
> $$[\mathrm{Ad}_T] = \begin{pmatrix}R & 0\\ [p]R & R\end{pmatrix}, \qquad [\mathrm{Ad}_T\mathcal{V}] = T\,[\mathcal{V}]\,T^{-1}, \qquad \mathcal{V}_s = [\mathrm{Ad}_{T_{sb}}]\,\mathcal{V}_b$$
>
> 여기서 $[\mathcal{V}]$는 §3의 $4\times4$ 행렬이다. $T$로 켤레를 취하는 것이 곧 프레임 변환이므로, 그것을 블록별로 풀어 쓰면 $6\times6$ 꼴이 나온다.
>
> - **예**: 카탈로그 자세의 P2의 $T_{sb}$('대상으로 한 번 끝까지'의 1단계)는 두 관절의 물체 트위스트 $(0,0,1;\ 1,1,0)$과 $(0,0,1;\ 0,1,0)$을 $(0,0,1;\ 0,0,0)$과 $(0,0,1;\ 0,-1,0)$으로 보낸다. 각 관절이 홀로 단위 속도로 돌 때의 트위스트이고, 4장은 이것을 스크류 축 $\mathcal{S}_1$과 $\mathcal{S}_2$라 부르며, 5장은 이것들을 야코비안의 열로 쌓는다. 수반 앞은 $J_b$, 뒤는 $J_s$다.
> - **비예**: $p \ne 0$인데 "양쪽을 회전"을 쓴 $\mathrm{diag}(R, R)$. 어깨의 물체 트위스트에 적용하면 $(0,0,1;\ -1,1,0)$이 나온다. $v_s$가 $0$인 공간 트위스트가 아니라 말단의 속도다. $p = 0$일 때만 맞으므로, 떨어져 있는 프레임 — 도구, 카메라 — 에는 모두 모서리가 필요하다.

아래 그림은 한 운동을 두 기술로 그린다. '대상으로 한 번 끝까지'의 자세에서 엘보가 $1\,\mathrm{rad/s}$로 돈다.

<svg viewBox="0 0 560 284" style="max-width:100%;height:auto" role="img" aria-label="카탈로그 자세의 P2에서 엘보가 1 rad/s로 돌 때, 말단의 속도 (−1, 0, 0)과 공간 원점에 있는 물체 점의 속도 (0, −1, 0)을 엘보 축 둘레 반지름 1 m 원 위에 그리고, 옆에 두 여섯 숫자 벡터와 수반 관계를 적은 그림.">
  <defs><marker id="mr03avK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="192,80 185.7,80.2 179.5,80.7 173.2,81.5 167.1,82.6 160.9,84.1 154.9,85.9 149,88 143.2,90.4 137.5,93.1 132,96.1 126.6,99.4 121.5,102.9 116.5,106.7 111.7,110.8 107.1,115.1 102.8,119.7 98.7,124.5 94.9,129.5 91.4,134.6 88.1,140 85.1,145.5 82.4,151.2 80,157 77.9,162.9 76.1,168.9 74.6,175.1 73.5,181.2 72.7,187.5 72.2,193.7 72,200" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.55"/>
  <polyline points="72,200 192,200 192,80" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.28"/>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2" marker-end="url(#mr03avK)"><line x1="80" y1="200" x2="128" y2="200"/><line x1="72" y1="192" x2="72" y2="144"/><line x1="192" y1="73" x2="192" y2="28"/><line x1="185" y1="80" x2="104" y2="80"/></g>
  <g><circle cx="192" cy="200" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="192" cy="200" r="2" fill="currentColor"/></g>
  <circle cx="72" cy="200" r="3.6" fill="currentColor"/>
  <circle cx="192" cy="80" r="3.6" fill="currentColor"/>
  <polyline points="202.9,213 204,212 205,210.9 205.9,209.8 206.7,208.5 207.4,207.2 208,205.8 208.4,204.4 208.7,203 208.9,201.5 209,200 208.9,198.5 208.7,197 208.4,195.6 208,194.2 207.4,192.8 206.7,191.5 205.9,190.2 205,189.1 204,188 202.9,187 201.8,186.1 200.5,185.3 199.2,184.6 197.8,184 196.4,183.6 195,183.3 193.5,183.1 192,183 190.5,183.1 189,183.3 187.6,183.6 186.2,184 184.8,184.6 183.5,185.3 182.2,186.1 181.1,187 180,188 179,189.1 178.1,190.2 177.3,191.5 176.6,192.8 176,194.2 175.6,195.6 175.3,197 175.1,198.5 175,200 175.1,201.5 175.3,203 175.6,204.4" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#mr03avK)"/>
  <g stroke="currentColor" stroke-width="2.8" marker-end="url(#mr03avK)"><line x1="187" y1="80" x2="132" y2="80"/><line x1="72" y1="205" x2="72" y2="260"/></g>
  <g font-size="11" fill="currentColor">
    <text x="130" y="214">x̂<tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
    <text x="64" y="148" text-anchor="end">ŷ<tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
    <text x="62" y="194" text-anchor="end" font-size="12">{s}</text>
    <text x="200" y="36">x̂<tspan dy="3.5">b</tspan><tspan dy="-3.5"></tspan></text>
    <text x="100" y="84" text-anchor="end">ŷ<tspan dy="3.5">b</tspan><tspan dy="-3.5"></tspan></text>
    <text x="201" y="85" font-size="12">{b}</text>
    <text x="204" y="220">q<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="214" y="190">1 rad/s</text>
    <text x="184" y="69" text-anchor="end">ṗ = (−1, 0, 0) m/s, +ŷ<tspan dy="3.5">b</tspan><tspan dx="3.1" dy="-3.5">방향</tspan></text>
    <text x="81" y="244">v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= (0, −1, 0)</tspan></text>
    <text x="81" y="259" opacity="0.85">원점의 물체 점</text>
    <text x="89.1" y="129.1" text-anchor="end" opacity="0.8">축에서 1 m</text>
    <text x="300" y="30" font-size="12">엘보 1 rad/s, 카탈로그 자세</text>
    <text x="300" y="57" opacity="0.85">{b}로 쓰고 v는 말단의 것:</text>
    <text x="312" y="74">V<tspan dy="3.5">b</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1; 0, 1, 0): 말단 축으로 쓴 ṗ</tspan></text>
    <text x="300" y="95" opacity="0.85">{s}로 쓰고 v는 원점의 것:</text>
    <text x="312" y="112">V<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1; 0, −1, 0)</tspan></text>
    <text x="300" y="133" opacity="0.85">수반 사상이 잇는다, T = T<tspan dy="3.5">sb</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="300" y="150">V<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= [Ad</tspan><tspan dy="3.5">T</tspan><tspan dy="-3.5">] V</tspan><tspan dy="3.5">b</tspan><tspan dy="-3.5">, 그 모서리가:</tspan></text>
    <text x="300" y="167">v<tspan dy="3.5">s</tspan><tspan dx="3.1" dy="-3.5">= R v</tspan><tspan dy="3.5">b</tspan><tspan dx="3.1" dy="-3.5">+ p × ω</tspan><tspan dy="3.5">s</tspan><tspan dy="-3.5"></tspan></text>
    <text x="312" y="184">= (−1, 0, 0) + (1, −1, 0)</text>
    <text x="300" y="207" opacity="0.85">diag(R, R)는 모서리를 버려 (−1, 0, 0):</text>
    <text x="312" y="224" opacity="0.85">말단의 ṗ이지 v<tspan dy="3.5">s</tspan><tspan dy="-3.5">가 아니다</tspan></text>
  </g>
</svg>

카탈로그 자세의 P2에서 엘보가 자기 축, 곧 $q_2 = (1, 0, 0)$을 지나 지면 밖을 향하는 $\hat z$축 둘레로 $1\,\mathrm{rad/s}$로 돈다. 말단과 베이스 원점은 둘 다 그 축에서 $1\,\mathrm m$ 떨어져 있어 점선 원을 따라 $1\,\mathrm{m/s}$로 움직인다. 말단은 $\dot p = (-1, 0, 0)$, 말단 축으로 쓰면 $v_b = (0, 1, 0)$이고, 원점의 물체 점은 $v_s = (0, -1, 0)$이다. 한 운동이 여섯 숫자 벡터 둘, $\mathcal{V}_b = (0,0,1;\ 0,1,0)$과 $\mathcal{V}_s = (0,0,1;\ 0,-1,0)$을 주고, $[\mathrm{Ad}_{T_{sb}}]$가 $Rv_b = (-1, 0, 0)$에 모서리 $p \times \omega_s = (1, -1, 0)$을 더해 둘을 잇는다.

### 5. SE(3)의 자세 지수와 로그

4장은 팔의 모든 자세를 관절 운동으로 만들고, 6장은 야코비안이 다룰 수 있는 자세 *오차*가 필요하다. 지수가 앞의 것을 준다 — 4장의 지수 곱이 바로 그것이다. 로그가 뒤의 것을 준다. 수치 IK([[04-robotics/modern-robotics/ch06-inverse-kinematics|6장 §2]])는 $[\log(T_{now}^{-1}T_{goal})]^\vee$ 위에서 반복하고, $^\vee$는 $4\times4$ 행렬에서 여섯 좌표를 다시 읽어 낸다.

*한 문장으로:* 자세 전체 — 회전과 위치를 함께 — 는 스크류 하나를 한 양만큼 따라가서 도달하므로 트위스트의 지수이고, 로그는 어떤 자세에서든 그 스크류와 양을 다시 읽어 낸다.

*이 절에서 하나만 가져간다면:* 병진 열은 $v\theta$가 아니라 $G(\theta)v$다. 회전이 진행하면서 선속도를 함께 돌려 놓기 때문이다. P2의 엘보 스크류로 4분의 1바퀴를 돌면 원점은 $(1,-1,0)$에 가고, 순진한 형태는 그것을 $(0,-1.5708,0)$에 둔다(5.1의 예와 비예).

§2는 회전축과 각을 회전 행렬로 바꿨다. 이 절은 자세 전체에 대해 같은 일을 하고, 그 역을 구한다. 여기서 **스크류 축**은 §3의 트위스트 $\mathcal{S} = (\omega, v)$를 두 방식 중 하나로 정규화한 것이다. $\|\omega\| = 1$이면 $\theta$는 축 둘레로 도는 각(라디안)이고, $\omega = 0$이고 $\|v\| = 1$이면 $\theta$는 $v$ 방향으로 미끄러지는 거리(미터)다. 그 괄호는 §3의 $\mathfrak{se}(3)$ 원소인 $4\times4$ 행렬

$$[\mathcal{S}] = \begin{pmatrix}[\omega] & v\\ 0 & 0\end{pmatrix}$$

이고, 항등에서 출발해 스크류를 $\theta$만큼 따라가는 것은 $T(0) = I$인 선형 미분방정식 $dT/d\theta = [\mathcal{S}]\,T$(§2의 $\dot R = [\omega_s]R$를 한 치수 키운 것)이므로, 해는 행렬 지수 $T = e^{[\mathcal{S}]\theta}$다.

**스크류 안의 축.** $\|\omega\| = 1$이면 여섯 숫자는 축 위의 점 $q$와 §3의 피치 $h$로 정해진다. $\mathcal{S} = (\omega,\ -\omega\times q + h\,\omega)$다(MR 정의 3.24). P2의 회전 관절은 $h = 0$이므로 $q_2 = (1,0,0)$을 지나는 엘보는 $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$이고, 속도 $\dot\theta$로 도는 관절의 트위스트는 $\mathcal{V} = \mathcal{S}\dot\theta$다. *비예*: $\dot\theta = 2\,\mathrm{rad/s}$인 그 트위스트 $(0,0,2;\ 0,-2,0)$은 $\|\omega\| = 2$라 스크류 축이 아니다. 5.1의 닫힌 형태에 $\theta = \pi/2$와 함께 넣으면 열의 길이가 $3.606$인 회전 블록이 나온다. 그것이 나타내는 운동은 $\mathcal{S}_2$를 $\theta = \pi$만큼 따라간 것, 곧 엘보 둘레의 반 바퀴다. 먼저 정규화해야 4장이 각 지수의 $\theta$를 관절각으로 읽을 수 있다.

**5.1 닫힌 형태.** $[\mathcal{S}]$의 거듭제곱은 모두 같은 꼴을 유지한다. $k \ge 1$이면 $[\mathcal{S}]^k = \begin{pmatrix}[\omega]^k & [\omega]^{k-1}v\\ 0 & 0\end{pmatrix}$이므로 급수가 회전 블록과 병진 열로 갈라진다:

$$e^{[\mathcal{S}]\theta} = \begin{pmatrix} e^{[\omega]\theta} & G(\theta)\,v \\ 0 & 1 \end{pmatrix}, \qquad G(\theta) = I\theta + [\omega]\frac{\theta^2}{2!} + [\omega]^2\frac{\theta^3}{3!} + [\omega]^3\frac{\theta^4}{4!} + \cdots$$

회전 블록은 §2의 로드리게스 공식이다. $G$에서는 같은 항등식 $[\omega]^3 = -[\omega]$가 급수를 접는다. $[\omega]$ 항은 $\theta^2/2! - \theta^4/4! + \cdots = 1 - \cos\theta$로, $[\omega]^2$ 항은 $\theta^3/3! - \theta^5/5! + \cdots = \theta - \sin\theta$로 모이므로

$$G(\theta) = I\theta + (1-\cos\theta)\,[\omega] + (\theta-\sin\theta)\,[\omega]^2 \qquad (\|\omega\| = 1)$$

이고, 이것이 MR 명제 3.25다. 물리적으로 읽으면 $G(\theta)v = \int_0^\theta e^{[\omega]\varphi}v\,d\varphi$는 선속도 $v$를 지금까지 쌓인 회전으로 돌려 가며 운동 전체에 걸쳐 더한 것이다. 로드리게스 공식을 항별로 적분해도 같은 세 계수가 나온다.

- **예, P2에서.** $q_2 = (1,0,0)$을 지나는 엘보 스크류 $\mathcal{S}_2 = (0,0,1;\ 0,-1,0)$, $\theta = \pi/2$. $[\hat z]^2 = \mathrm{diag}(-1,-1,0)$, $1 - \cos\frac{\pi}{2} = 1$, $\frac{\pi}{2} - \sin\frac{\pi}{2} = 0.5708$이므로

  $$G(\tfrac{\pi}{2}) = \begin{pmatrix}1&-1&0\\1&1&0\\0&0&\pi/2\end{pmatrix}, \qquad G v_2 = \begin{pmatrix}1\\-1\\0\end{pmatrix}, \qquad e^{[\mathcal{S}_2]\pi/2} = \begin{pmatrix}0&-1&0&1\\1&0&0&-1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

  이다. $G$의 앞 두 대각 성분이 $\frac{\pi}{2} - 0.5708 = 1$이기 때문이다. 병진 열은 원점이 가는 곳이다. 원점은 축에서 $-q_2 = (-1,0)$에 있고, 4분의 1바퀴 돌면 $(0,-1)$, $q_2$를 되더하면 $(1,-1)$이다. 축 위의 엘보는 제자리에 있다: $R_z(90^\circ)(1,0,0) + (1,-1,0) = (1,0,0)$.
- **비예.** 회전과 병진이 서로 독립인 것처럼 돌리고 옮기는 $\begin{pmatrix} e^{[\omega]\theta} & v\theta \\ 0 & 1\end{pmatrix}$. $\mathcal{S}_2$에서는 원점을 $(1,-1,0)$이 아니라 $(0,-1.5708,0)$에 놓고 엘보를 $(0,-0.5708,0)$으로 옮긴다. 자기 축이 움직이는 회전 관절이다. 보정 $G(\theta) - I\theta$가 정확히 회전이 병진에 미치는 효과다.

**5.2 순수 병진.** $\omega = 0$이면 $[\mathcal{S}]^2 = 0$이고(왼쪽 위 블록이 0이라 곱에 남는 것이 없다) 급수는 일차 항 뒤에서 멈춘다:

$$e^{[\mathcal{S}]\theta} = \begin{pmatrix} I & v\,\theta \\ 0 & 1 \end{pmatrix} \qquad (\omega = 0,\ \|v\| = 1)$$

§3의 피치 무한대 스크류, 곧 회전 없이 $v$ 방향으로 $\theta$미터 미끄러지는 운동이다. $[\omega] = 0$이면 회전용 공식도 우연히 같은 $G = I\theta$를 주지만, 그쪽의 $\theta$는 각이고 이쪽은 길이라서 두 경우를 따로 쓴다. *P2에서*: [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 홈 자세 $M$(말단 $(2,0,0)$, $R = I$)이 정확히 $v = (1,0,0)$, $\theta = 2\,\mathrm{m}$인 이 경우다.

**5.3 행렬 로그.** 거꾸로 묻는다. $T = (R, p)$가 주어지면 $e^{[\mathcal{S}]\theta} = T$인 스크류 $\mathcal{S}$와 $\theta$를 찾는다. 그런 쌍은 항상 있고(모든 강체 변위는 스크류 하나를 따르는 운동이다 — 샬–모치 정리), 닫힌 형태가 그것을 읽어 내는 법을 알려 준다(MR §3.3.3.2):

1. $R = I$이면 순수 병진이다: $\omega = 0$, $\theta = \|p\|$, $v = p/\|p\|$.
2. 아니면 회전의 로그부터 구한다. $\operatorname{tr}[\omega] = 0$이고 $\operatorname{tr}[\omega]^2 = -2\|\omega\|^2 = -2$이므로 로드리게스 공식의 대각합은 $\operatorname{tr}R = 3 - 2(1-\cos\theta) = 1 + 2\cos\theta$이고, $[\omega]$는 반대칭이며 $I$와 $[\omega]^2$는 대칭이므로 $R - R^\top = 2\sin\theta\,[\omega]$다. 따라서 $\theta \in (0, \pi)$에서

$$\theta = \arccos\frac{\operatorname{tr}R - 1}{2}, \qquad [\omega] = \frac{R - R^\top}{2\sin\theta}, \qquad v = G^{-1}(\theta)\,p$$

이고, 5.1의 $G$의 역은

$$G^{-1}(\theta) = \frac{1}{\theta}\,I - \frac{1}{2}\,[\omega] + \Bigl(\frac{1}{\theta} - \frac{1}{2}\cot\frac{\theta}{2}\Bigr)[\omega]^2$$

이다. $[\omega]^3 = -[\omega]$와 $[\omega]^4 = -[\omega]^2$로 $G\,G^{-1}$을 곱해 펼치면 확인된다. $\sin\theta = 0$인 $\theta = \pi$에서는 대신 $R = I + 2[\omega]^2 = 2\omega\omega^\top - I$, 곧 $\omega\omega^\top = (R + I)/2$에서 축을 읽는다.

- **예, P2에서.** 경우마다 로그 하나씩, 셋. (i) 5.1의 $e^{[\mathcal{S}_2]\pi/2}$: $\operatorname{tr}R = 1$에서 $\theta = \pi/2$, $(R - R^\top)/2 = [\hat z]$이고, $G^{-1}(\frac{\pi}{2}) = \begin{pmatrix}0.5&0.5&0\\-0.5&0.5&0\\0&0&2/\pi\end{pmatrix}$가 $p = (1,-1,0)$을 $v = (0,-1,0)$으로 보낸다. $\mathcal{S}_2$가 돌아온다. (ii) '대상으로 한 번 끝까지'의 $T_{sb}$: $R$은 같고 $p = (1,1,0)$이라 $v = G^{-1}p = (1,0,0)$이고, $v = -\omega\times q$가 축을 $q = (0,1,0)$에 둔다. 도구 프레임은 $\{s\}$에서 $(0,1)$을 지나는 $\hat z$축 둘레로 4분의 1바퀴 한 번에 닿는다. 어느 링크 위에도 없는 점이고, 로그의 스크류가 팔이 아니라 변위의 성질인 이유다. (iii) $M$: $R = I$라 경우 1이 $\theta = 2$, $v = (1,0,0)$을 준다. 5.2의 미끄러짐이다.
- **비예.** $v = p/\theta$로 읽은 스크류, 곧 회전의 로그에 위치를 각으로 나눠 붙인 것 — 5.1의 비예를 거꾸로 돌린 것이다. '대상으로 한 번 끝까지'의 $T_{sb}$에서 이것은 $(1,0,0)$ 대신 $v = (0.6366,\ 0.6366,\ 0)$을 주고, 그 스크류를 $\pi/2$만큼 따라가면 도구가 제자리에서 $1.04\,\mathrm{m}$ 떨어진 $(0,\ 1.2732)$에 간다. 회전이 병진을 쓸고 간 몫은 $G^{-1}$만이 되돌린다.

이 절의 모든 숫자는 영어 절반의 첫째 파이썬 블록이 확인한다. 닫힌 형태를 거듭제곱 급수 자체와 대조하고, 순수 병진을 확인하고, 세 로그를 지수로 되돌려 본다. 출력은 위의 $e^{[\mathcal{S}_2]\pi/2}$, 급수와의 일치 `True`, $M$이 순수 병진이라는 `True`, 그리고 세 로그 $(0,0,1;\ 0,-1,0)$·$\theta = 1.5708$, $(0,0,1;\ 1,0,0)$·$1.5708$, $(0,0,0;\ 1,0,0)$·$2.0000$이며 되돌림은 모두 `True`다.

**학습 쪽에서 중요한 이유**: exp/log 사상이 자세 보간, 회전 평균, SE(3) 위의 손실 정의의
방법이고 — SE(3) 위에서 도구 자세를 디퓨전이나 flow로 생성하는 행동 헤드의 밑바닥 기계장치다.
관절 청크를 내는 [[01-canonical-papers/notes/4-vla/pi0|π0]]의 헤드 같은 관절 공간 헤드는
4장의 순기구학을 거쳐야 그 출력이 자세가 된다.

### 6. 렌치 — 트위스트의 힘 쌍대

손목의 6축 힘-토크 센서는 힘과 모멘트를 자기 프레임으로 보고하고, 5장은 도구에 걸린 힘을 관절 토크 $\tau = J^\top\mathcal{F}$로 바꿔야 한다([[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §3]]). 둘 다 밀기를 프레임을 올바르게 바꾸는 여섯 숫자 벡터 하나로 써야 하고, [[04-robotics/modern-robotics/ch12-grasping|12장]]의 파지 해석은 접촉마다의 그런 벡터를 더한다. 트위스트가 강체가 어떻게 움직이는지를 말한다면 **렌치**(wrench)는 어떻게 밀리는지를 말한다. 강체에 작용하는 모멘트와 힘을 한 프레임 $\{a\}$에서 함께 쓴 6차원 벡터다:

$$\mathcal{F}_a = (m_a,\ f_a) \in \mathbb{R}^6, \qquad m_a = r_a \times f_a$$

여기서 $f_a$는 선형 힘(N), $r_a$는 그 작용선 위의 아무 점($\{a\}$ 좌표, m), $m_a$는 그 힘이 $\{a\}$의 원점에 대해 만드는 모멘트(N·m, 힘의 모멘트는 [[02-foundations/basic-mechanics|0.6.1 §7]])다. 정의 조건은 셋이다. 두 절반은 같은 프레임으로 쓴다. 모멘트는 그 프레임의 *원점*에 대해 잡으므로, §3에서 트위스트의 $v$가 그랬듯 힘이 그대로여도 기준점이 옮겨 가면 모멘트 절반이 바뀐다. 한 강체에 작용하는 렌치들은 같은 프레임으로 썼을 때에만 성분별로 더해진다. $r_a$를 힘 자신의 작용선을 따라 옮겨도 아무것도 바뀌지 않는다. 더해지는 부분이 $f_a$에 평행해 $f_a$와의 외적이 0이기 때문이다. $f = 0$인 렌치는 **순수 모멘트**다. 모멘트를 앞에 두는 순서는 트위스트의 $(\omega, v)$와 맞춰 성분끼리 짝짓기 위한 것이다.

**일률.** $r_a$에 있는 물체 점은 $v_a + \omega_a \times r_a$로 움직이므로(§3의 속도장), 거기 걸린 힘 $f_a$가 내는 일률은 $f_a\cdot(v_a + \omega_a\times r_a) = v_a\cdot f_a + \omega_a\cdot(r_a\times f_a)$다. 마지막 단계는 스칼라 삼중곱의 순환 규칙 $a\cdot(b\times c) = b\cdot(c\times a) = c\cdot(a\times b)$다. 따라서

$$P = \mathcal{V}_a^\top\mathcal{F}_a = \omega_a\cdot m_a + v_a\cdot f_a$$

이고 단위는 와트다. 회전 곱하기 모멘트 더하기 병진 곱하기 힘이다. 모멘트가 $\omega$와, 힘이 $v$와 짝을 이루는 이유가 이 짝짓기다.

**프레임 변환.** 일률은 물리량이라 어느 프레임으로 쓰느냐에 달릴 수 없다. 모든 운동에 대해 $\mathcal{V}_b^\top\mathcal{F}_b = \mathcal{V}_a^\top\mathcal{F}_a$다. §4의 $\mathcal{V}_a = [\mathrm{Ad}_{T_{ab}}]\mathcal{V}_b$를 대입하면 모든 $\mathcal{V}_b$에 대해 $\mathcal{V}_b^\top\mathcal{F}_b = \mathcal{V}_b^\top[\mathrm{Ad}_{T_{ab}}]^\top\mathcal{F}_a$이므로

$$\mathcal{F}_b = [\mathrm{Ad}_{T_{ab}}]^\top\,\mathcal{F}_a$$

이다(MR 명제 3.27). 트위스트는 수반으로, 렌치는 그 전치로 프레임을 바꾼다. §4의 블록 형태로 풀어 쓰면 $f_b = R^\top f_a$, $m_b = R^\top(m_a - p\times f_a)$다. 힘은 회전시키고, 모멘트의 기준점은 $\{a\}$의 원점에서 $p$에 있는 $\{b\}$의 원점으로 옮긴다.

- **예, P2에서.** [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]] 정역학의 힘, 곧 도구가 말단 $p = (1,1,0)$에서 가하는 $f = (0,-10,0)\,\mathrm{N}$과 '대상으로 한 번 끝까지'의 $T_{sb}$. $\{s\}$에서 모멘트는 $p\times f = (0,0,-10)\,\mathrm{N\,m}$이므로 $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$이다. $\{b\}$에서는 $\mathcal{F}_b = [\mathrm{Ad}_{T_{sb}}]^\top\mathcal{F}_s = (0,0,0;\ -10,0,0)$이다. 힘이 $\{b\}$ 자신의 원점에 걸리므로 모멘트가 없고, 힘은 $-\hat x_b$ 방향, 곧 전완을 따라 곧장 되돌아가는 방향이다. 일률이 이 쌍을 검산한다. 관절 1을 $1\,\mathrm{rad/s}$로 돌리는 것은 공간 트위스트 $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$이고 $\mathcal{S}_1^\top\mathcal{F}_s = -10\,\mathrm{W}$다. 같은 운동을 $\{b\}$로 쓰면 $(0,0,1;\ 1,1,0)$이고, $\mathcal{F}_b$와 짝지으면 다시 $1\cdot(-10) = -10\,\mathrm{W}$다. 관절 2의 스크류 $\mathcal{S}_2$와는 $1\cdot(-10) + (-1)(-10) = 0$이다. 이 두 숫자가 [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §3]]의 관절 토크 $\tau = (-10, 0)\,\mathrm{N\,m}$다. 관절 토크는 관절 속도 단위당 전달되는 일률이기 때문이다.
- **비예.** 모멘트를 빼 버리고 힘이 베이스에 걸린 것처럼 쓴 $\mathcal{F}_s = (0,0,0;\ 0,-10,0)$. $\mathcal{S}_1$과 짝지으면 $0\,\mathrm{W}$가 나온다. 어깨가 $1\,\mathrm{m}$ 지렛대 끝의 $10\,\mathrm{N}$ 하중을 공짜로 든다는 주장이다. 렌치의 모멘트는 기준점에 속하고, 그것을 잊는 것은 §3의 $v_s$ 대 $\dot p$ 실수를 힘으로 옮긴 것이다.

위 숫자는 영어 절반의 둘째 파이썬 블록이 확인한다. 출력은 $\mathcal{F}_s = (0,0,-10;\ 0,-10,0)$, $\mathcal{F}_b = (0,0,0;\ -10,0,0)$, 두 프레임 모두 일률 $-10$, 그리고 $\tau = (-10, 0)$이다.

### 스스로 점검

1. $\hat z$ 둘레 $\theta = 180°$에 대해 로드리게스를 검산하라. 어떤 행렬이 나오는가?
2. 물체가 점 $(0, 2, 0)$을 지나는 축($\hat z$ 방향, 1 rad/s) 둘레로 돈다.
   공간 트위스트 $\mathcal{V}_s = (\omega_s, v_s)$는?
3. $[\hat\omega]^3 = -[\hat\omega]$가 지수 급수를 세 항으로 끝내는 이유는?
4. $T$가 $p$만큼의 순수 병진이면 $[\text{Ad}_T]$는 트위스트에 무슨 일을 하는가?
5. P2의 어깨 스크류 $\mathcal{S}_1 = (0,0,1;\ 0,0,0)$에 대해 $e^{[\mathcal{S}_1]\pi/2}$는 무엇이고, 병진 열이 왜 0인가?
6. 말단 힘이 대신 $f = (10, 0, 0)\,\mathrm{N}$이고 여전히 $p = (1,1,0)$에 걸린다. $\mathcal{F}_s$와 두 관절 토크 $\mathcal{S}_i^\top\mathcal{F}_s$를 써라.

> [!tip]- 정답 · Answers
> 1. $\sin 180° = 0$, $1-\cos 180° = 2$이므로 $R = I + 0 + 2[\hat z]^2 = \text{diag}(-1, -1, 1)$ — x·y축이 뒤집히고 z는 그대로다.
> 2. $\omega_s = (0,0,1)$; 공간 프레임의 선형 성분은 $v_s = -\omega \times q = -(0,0,1)\times(0,2,0) = (2,0,0)$ — 지금 원점에 있는 물체 위의 점이 $+x$로 2 m/s로 움직인다는 뜻이고, 축 자체는 정지해 있다. §3의 경고를 수치로 옮긴 것이다.
> 3. 3×3 반대칭 행렬의 거듭제곱이 자기 자신의 배수로 되돌아오기 때문이다($[\hat\omega]^3 = -[\hat\omega]$). 급수의 모든 항이 $[\hat\omega]$, $[\hat\omega]^2$의 계수로 흡수되어 로드리게스의 세 항만 남는다.
> 4. $\omega$는 그대로 두고 $v \mapsto v + p \times \omega$로 보낸다. 선속도가 정확히 축의 오프셋만큼 보정되는 것이고, 그래서 프레임 아래 첨자를 매번 써야 한다.
> 5. $v_1 = 0$이므로 $G(\theta)v_1 = 0$이고 $e^{[\mathcal{S}_1]\pi/2} = \begin{pmatrix}R_z(90^\circ) & 0\\ 0 & 1\end{pmatrix}$다. 축이 원점을 지나므로 원점이 움직이지 않는다(§5.1).
> 6. $m_s = p\times f = (0,0,-10)$이므로 $\mathcal{F}_s = (0,0,-10;\ 10,0,0)$. 그러면 $\tau_1 = \mathcal{S}_1^\top\mathcal{F}_s = -10$, $\tau_2 = \mathcal{S}_2^\top\mathcal{F}_s = 1\cdot(-10) + (-1)\cdot 0 = -10\,\mathrm{N\,m}$로, 5장의 $J^\top(10, 0)$이 주는 $(-10,-10)$과 같다(§6).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**, 카탈로그 자세 $\theta=(0^\circ,90^\circ)$와 세운 자세 $\theta=(90^\circ,0^\circ)$. 시뮬레이터 없음.

1. **그리기.** 팔을 곧장 위로 세운 $\theta=(90^\circ,0^\circ)$에 대한 위의 그림: 원점의 베이스 프레임 $\{s\}$, 엘보 $(0,1)$, 말단 $(0,2)$, 그리고 말단에서 $x$축이 전완 방향인 도구 프레임 $\{b\}$. 엘보를 지나는 축 $\hat\omega=(0,0,1)$, $1\,\mathrm{rad/s}$를 더하고, 그림 옆에 말단의 속도와 공간 트위스트의 선형 성분을 적어라. 각각 어느 쪽을 가리키는가?
2. **유도.** 세운 자세 $\theta=(90^\circ,0^\circ)$에서: (a) $T_{sb}$를 써라. (b) 어깨를 $1\,\mathrm{rad/s}$로 돌리고 그 운동의 공간 트위스트 $\mathcal{V}_s$와 물체 트위스트 $\mathcal{V}_b$를 쓴 뒤 $\mathcal{V}_s=[\mathrm{Ad}_{T_{sb}}]\mathcal{V}_b$를 확인하라. (c) 카탈로그 자세에서 같은 운동은 $\mathcal{V}_s=(0,0,1;\ 0,0,0)$, $\mathcal{V}_b=(0,0,1;\ 1,1,0)$이었다(§3의 상자). 두 여섯 숫자 벡터 중 자세와 함께 바뀐 것은 어느 쪽이고, 왜인가? (d) 말단의 속도를 $\{s\}$와 $\{b\}$의 축으로 각각 써라.
3. **해석.** (a) P2의 트위스트에서는 어떤 자세, 어떤 관절 속도에서든 왜 $\omega_x$, $\omega_y$, $v_z$가 0인가? (b) 도구의 자세는 SE(2), 곧 평면 자세 — $x$, $y$, 방향각 하나, 숫자 셋 — 에 사는데, P2의 컨피규레이션 공간은 [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 원환면, 숫자 둘이다. SE(2)가 왜 도구 자세의 공간이면서 P2의 컨피규레이션 공간은 아닌가? (c) 말단을 카탈로그 목표 $(1,1)$에 둔 채 P2가 가질 수 있는 도구 방향은 무엇인가? $(1, 1, 45^\circ)$가 그중 하나가 아님을 보여라.

> [!note]- 그리는 법 · How to draw it
> - 팔부터 그린다. 베이스는 원점, 링크 1은 곧장 위로 엘보 $(0,1)$까지, 링크 2는 그대로 위로 말단 $(0,2)$까지.
> - 원점의 공간 프레임 $\{s\}$: $\hat x_s$는 오른쪽, $\hat y_s$는 위, $\hat z_s$는 지면 밖을 뜻하는 동그라미 친 점. 점을 반드시 그린다. 셋째 축이 어디를 향하는지 말하지 않는 평면 그림에서는 이 장의 모든 부호가 동전 던지기가 된다.
> - 말단의 물체 프레임 $\{b\}$는 $\hat x_b$를 전완 방향, 곧 $+\hat y_s$ 방향에 둔다 — 위 그림과 같은 $R_{sb}$다. 그러면 오른손 규칙에 따라 $\hat y_b$는 $-\hat x_s$ 방향이고 $\hat z_b$도 다시 지면 밖이다.
> - 오프셋 $p=(0,2,0)$은 원점에서 말단까지의 점선 화살표로. $R_{sb}$와 $p$가 $T_{sb}$의 전부이고, 바뀐 것은 $p$뿐이다.
> - 회전축은 엘보 $q=(0,1,0)$에 동그라미 친 점과 그 둘레의 굽은 화살표로 그리고, $\hat\omega$와 $\dot\theta=1\,\mathrm{rad/s}$를 적는다.
> - 속도는 그림 안이 아니라 옆에 짧은 화살표로 적는다. 말단의 실제 속도 $\hat\omega\times(p-q)$와 트위스트의 선형 성분 $v_s=-\hat\omega\times q$를 나란히 둔다. 말단은 축 위 1 m, 공간 원점은 축 아래 1 m에 있으므로 두 화살표는 서로 반대를 가리킨다. 같게 나왔다면 트위스트가 $v_s$를 원하는 자리에 $\dot p$를 쓴 것이다.

> [!tip]- 정답 · Solutions
> 1. 전완이 $+\hat y_s$를 가리키므로 다시 $\hat x_b=\hat y_s$, $\hat y_b=-\hat x_s$, $\hat z_b$는 지면 밖이다. $R_{sb}=R_z(90^\circ)$는 위 그림과 같고 $p=(0,2,0)$만 다르다. 엘보 축은 $q=(0,1,0)$을 지나고 $\hat\omega=(0,0,1)$이다. 말단은 $\hat\omega\times(p-q)=(0,0,1)\times(0,1,0)=(-1,0,0)\,\mathrm{m/s}$로 왼쪽으로 움직이고, 트위스트의 선형 성분은 $v_s=-\hat\omega\times q=(1,0,0)$으로 오른쪽이다. 크기는 같고 방향은 반대다. $v_s$는 축 아래 1 m, 공간 원점을 지나는 강체 점의 속도이고, 말단은 축 위 1 m에 있다.
> 2. (a) 전완이 다시 $+\hat y_s$를 향하므로 $R_{sb}=R_z(90^\circ)$는 '대상으로 한 번 끝까지'와 같고 $p$만 바뀐다. $p=(0,2,0)$이므로 $T_{sb}$의 회전 열은 $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$이고 병진은 $(0,2,0)$이다. (b) 어깨 축은 원점을 지나므로 $\mathcal{V}_s=(0,0,1;\ 0,0,0)$으로, 카탈로그 자세와 똑같다. $\{b\}$에서는 $\omega_b=R^\top(0,0,1)=(0,0,1)$이고, $\dot p=\hat z\times p=(-2,0,0)$이라 $v_b=R^\top\dot p=(0,2,0)$, 곧 $\mathcal{V}_b=(0,0,1;\ 0,2,0)$이다. 확인: $v_s=Rv_b+p\times\omega_s=(-2,0,0)+(2,0,0)=0$. (c) 공간 트위스트는 그대로이고 물체 트위스트가 바뀌었다. $v_s$는 베이스 원점에 있는 물체 점의 것이고 그 점은 어느 자세에서든 어깨 축 위에 있으니 늘 $0$이다. $v_b$는 말단의 것이고 말단이 이제 축에서 $\sqrt2$가 아니라 $2\,\mathrm m$ 떨어져 있으니, 말단이 축에 대해 움직일 때마다 바뀐다. (d) $\{s\}$에서 $\dot p=(-2,0,0)\,\mathrm{m/s}$로 왼쪽이고, 말단 축으로는 $(0,2,0)$, 곧 $-\hat x_s$를 가리키는 $+\hat y_b$ 방향이다.
> 3. (a) 두 관절 축은 모두 $\hat z$에 평행하고 평면 $z=0$의 점 $q_i$를 지나므로, P2의 모든 트위스트는 $(0,0,1;\ -\hat z\times q_i)$들의 조합이다. $\omega$는 $\hat z$ 방향이고 $-\hat z\times q_i$는 평면 안에 있으니 $\omega_x=\omega_y=v_z=0$이다. 여섯 숫자 가운데 셋만 움직이고, 그래서 도구의 운동이 SE(2)에 들어맞는다. (b) 컨피규레이션은 원환면 $T^2$의 점, 곧 관절각 둘이고, 순기구학이 그것을 도구 자세 하나로 보낸다. 그 상들은 3차원 SE(2) 안의 2차원 곡면을 이루므로 대부분의 평면 자세는 어느 컨피규레이션의 상도 아니다. SE(2)는 과제가 도구의 목표를 쓰는 곳 — [[04-robotics/modern-robotics/ch02-configuration-space|2장 §1.5]]의 작업 공간 — 이지 로봇이 사는 곳이 아니다. (c) 엘보는 베이스에서 $1\,\mathrm m$, 말단에서 $1\,\mathrm m$ 떨어져야 하므로 방향 $\varphi$는 $(1-\cos\varphi)^2+(1-\sin\varphi)^2=1$, 곧 $\cos\varphi+\sin\varphi=1$일 때만 가능하고, 이것은 $\varphi=0^\circ$(2장의 접촉 B, $\theta=(90^\circ,-90^\circ)$)와 $90^\circ$(접촉 A, 카탈로그 자세)에서만 성립한다. $45^\circ$라면 엘보가 $(1,1)-(\cos45^\circ,\sin45^\circ)=(0.293,\ 0.293)$, 베이스에서 $0.414\,\mathrm m$에 놓여야 한다.

### 출처 · Sources

- K. M. Lynch, F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — 3장. 회전, 각속도, 지수 좌표는 §3.2, 트위스트, 수반, 스크류, 행렬 로그는 §3.3, 렌치는 §3.4. 무료 PDF는 [[04-robotics/modern-robotics-book|책 안내]]에 있다.
- 이 페이지의 숫자와 두 목록은 P2의 카탈로그 자세로 여기서 직접 계산한 것이다. 믿지 말고 다시 계산하라.
