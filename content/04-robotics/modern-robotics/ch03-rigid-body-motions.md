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
> You should be able to: ① multiply rotation matrices and use $R^{-1} = R^\top$ ([[02-foundations/se3-geometry|SE(3) §1]]) ② compute a cross product $\omega \times v$ ③ solve $\dot x = ax \Rightarrow x = e^{at}x_0$ ([[02-foundations/engineering-math|0.5 §8]]). If any of the three is shaky, read that page first.
> 다음을 할 수 있어야 한다: ① 회전 행렬 곱셈과 $R^{-1} = R^\top$ ([[02-foundations/se3-geometry|SE(3) §1]]) ② 외적 $\omega \times v$ 계산 ③ $\dot x = ax \Rightarrow x = e^{at}x_0$ ([[02-foundations/engineering-math|0.5 공업수학 §8]]). 셋 중 하나라도 흔들리면 해당 페이지를 먼저 읽어라.

## English

**Core question**: how do we represent and compose rotations, poses, and velocities of rigid bodies — without singularities?

This is the longest-feeling chapter of the book, and the one worth ~30% of your total
study time: every later chapter is this machinery applied. Take it in four steps.

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

### 1. The skew-symmetric bridge: cross products become matrices

For $\omega = (\omega_1, \omega_2, \omega_3)$, define
$$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}, \qquad [\omega]\,v = \omega \times v.$$
Check one entry yourself: the first row of $[\omega]v$ is $-\omega_3 v_2 + \omega_2 v_3$ —
exactly the first component of $\omega \times v$. Why bother? Because once cross products
are matrices, *linear algebra applies to rotation dynamics* — including the matrix
exponential below.

**What the bracket operation does.** The vector ω contains the angular-velocity coordinates. The brackets package those same coordinates into a matrix that performs “cross with ω” on any input vector. The matrix is not an extra physical object and its entries are not independent parameters. Its signs encode the right-hand-rule orientation of the cross product.

For a point displaced from a rotation axis, the cross product gives the part of its velocity perpendicular to both the angular-velocity axis and the displacement. A point on the axis has no such rotational velocity; a point farther from the axis has a larger one at the same angular speed. This physical picture helps you reconstruct the sign pattern rather than memorizing it without meaning.

**Check your understanding.** Swapping the operands reverses the cross product, so [ω]v and [v]ω are generally opposites. Matrix notation makes composition easier, but it does not make cross products commutative. Check operand order when converting a geometric formula into code.

### 2. Why an exponential? Rotation is a linear ODE

A frame spinning at constant angular velocity obeys $\dot R = [\omega_s]\,R$ with $\omega_s$ expressed in the space frame (equivalently $\dot R = R\,[\omega_b]$ in the body frame; MR §3.2.2). The two forms agree because $\omega_s = R\,\omega_b$ and rotating a bracket gives $[R\,\omega_b] = R\,[\omega_b]\,R^\top$, so $[\omega_s]\,R = R\,[\omega_b]\,R^\top R = R\,[\omega_b]$.
This is the matrix version of $\dot x = ax$ — so its solution is the matrix version of
$e^{at}$: rotating about unit axis $\hat\omega$ for "time" $\theta$ gives
$$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2 \quad \text{(Rodrigues' formula)}.$$
The infinite series collapses to three terms because $[\hat\omega]^3 = -[\hat\omega]$.

**Worked check** — rotate about $\hat z = (0,0,1)$ by $\theta = 90°$:
$[\hat z] = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}$,
$[\hat z]^2 = \begin{pmatrix}-1&0&0\\0&-1&0\\0&0&0\end{pmatrix}$, so
$$R = I + (1)[\hat z] + (1)[\hat z]^2 = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},$$
which is exactly $R_z(90°)$ — it sends $\hat x \to \hat y$. Every rotation is *one*
axis-angle exponential (Euler's theorem); $\log$ recovers $(\hat\omega, \theta)$ from $R$.
This exp/log pair is the door between the Lie group (rotations) and the Lie algebra
(angular velocities) — and the reason poses can be interpolated and averaged correctly.

### 3. Twists: body velocity is six numbers — but read $v$ carefully

A moving body's velocity is a **twist** $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$.
**The meaning of $v$ depends on the reference frame and origin.** A space twist describes a velocity field relative to the fixed space origin; a body twist uses the moving body origin. Do not identify their linear components without specifying those choices. Every nonzero twist is a
**screw**: rotate about an axis while translating along it. The **pitch** $h$ is how far the
body advances along the axis per radian it turns about it, in metres per radian, so a screw
with $h = 0.01$ m/rad moves 1 cm along its axis for every radian of rotation — the same
quantity a machinist means by the pitch of a thread. Reading it that way makes the two limits
obvious: pure translation is the **infinite**-pitch case (turn nothing, still advance) and
pure rotation is the zero-pitch case (MR Def. 3.24: $h = 0$ for a pure rotation; $h \to \infty$ when $\omega = 0$).

**Distinguish the body origin from the space origin.** Let p locate the body origin in space coordinates. The space-twist linear component is v_s = ṗ − ω_s × p; recovering the velocity of the body origin therefore requires adding the rotational term. The body-twist linear component is v_b = Rᵀṗ: it is the velocity of the body origin expressed in body coordinates. Thus “v is not the tool-tip velocity” needs the frame qualification; it can be exactly that point velocity when the body origin is chosen at the tool tip.

Imagine a tool rotating about its own fixed tip. That tip has no translational motion, while points farther along the tool move. A space-origin description must encode enough information to reproduce that whole velocity field, not just the tip's trajectory. Changing origins changes the linear component required to describe the same motion.

**Check your understanding.** Always name both the expression frame and the point whose velocity you want. The [official twist explanation](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-2-twists-part-1-of-2/) develops this distinction. A mismatch here can make a numerically correct Jacobian appear to command the wrong translation.

### 4. One motion, two descriptions: space frame vs body frame

The same physical motion can be written in the fixed frame ($\mathcal{V}_s$) or the moving
body frame ($\mathcal{V}_b$). They are related by the **adjoint** of the current pose
$T = (R, p)$:
$$\mathcal{V}_s = [\text{Ad}_T]\,\mathcal{V}_b, \qquad [\text{Ad}_T] = \begin{pmatrix} R & 0 \\ [p]R & R\end{pmatrix}.$$
The top row says $\omega_s = R\,\omega_b$. The corner $[p]R$ comes from §3's space-twist formula $v_s = \dot p - \omega_s \times p$: the body origin's velocity is $\dot p = R\,v_b$, so $v_s = R\,v_b + p \times \omega_s = R\,v_b + [p]R\,\omega_b$. In words, $v_s$ describes the imaginary body point sitting at the space origin, offset by $-p$ from the body origin, and spinning about the body origin sweeps that point sideways by $p \times \omega_s$.
A special case worth memorizing: if $p = 0$ (pure rotation), this is just "rotate both
halves": $\omega_s = R\,\omega_b$, $v_s = R\,v_b$. **Frame subscripts are not decoration**
— most sign errors in later chapters are $s$/$b$ confusions, so write the subscript every
time. The pose exponential works like the rotation one:
$T = e^{[\mathcal{S}]\theta}$ means "follow screw $\mathcal{S}$ for angle $\theta$."

**Worked: $T_{sb}$ of plant P2.** Catalog pose $\theta=(0^\circ,90^\circ)$, tip at $(1,1)$ ([[02-foundations/lab-plants|0.6]]). Put $\{b\}$ at the tip with its $x$-axis along the forearm, so along $+\hat y_s$. A right-handed frame with $z$ out of the page then has $y_b=-\hat x_s$, and

$$R_{sb}=R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},\qquad p=(1,1,0),\qquad T_{sb}=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$

A pure $z$-rotation of the *whole arm about the origin* has space twist $\mathcal{V}_s=((0,0,1),(0,0,0))$: the axis through the origin gives $v_s=-\omega\times 0=0$. The tip still moves; $v_s$ is not the tip velocity. At this $p$, $\omega_s\times p=(-1,1,0)$, which is exactly the tip velocity for $1\,\mathrm{rad/s}$, and $v_s=\dot p-\omega_s\times p$ recovers the distinction of §3. Planar P2 always has $\omega_x=\omega_y=v_z=0$, so SE(2) is enough — until a paper treats $v_s$ as $\dot p$. The problem set keeps this $T_{sb}$ and asks the twist about the *elbow* instead.

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="one physical motion described from the fixed frame and from the body frame">
  <defs><marker id="mr3a" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <line x1="45" y1="150" x2="45" y2="100"/><line x1="45" y1="150" x2="95" y2="150"/>
  </g>
  <g fill="currentColor"><circle cx="45" cy="150" r="3.5"/></g>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <line x1="250" y1="95" x2="216" y2="60"/><line x1="250" y1="95" x2="285" y2="61"/>
  </g>
  <g fill="currentColor"><circle cx="250" cy="95" r="3.5"/></g>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.5" stroke-dasharray="4 3"><line x1="45" y1="150" x2="250" y2="95"/></g>
  <g stroke="currentColor" stroke-width="2.4" fill="none" opacity="0.85">
    <path d="M250,95 C300,70 340,80 372,110" marker-end="url(#mr3a)"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="26" y="172">space frame {s}</text><text x="234" y="120">body frame {b}</text>
    <text x="130" y="112" font-size="10.5" opacity="0.8">p, R</text>
    <text x="300" y="66">one motion</text>
    <text x="20" y="30">Same arrow, two sets of numbers</text>
    <text x="20" y="188" opacity="0.9">Nothing about the motion changes &#8212; only which frame you write it in. [Ad_T] converts between them,</text>
    <text x="20" y="204" opacity="0.9">and it needs BOTH R and p: rotating the frame is not enough when the frames are also offset.</text>
  </g>
</svg>



**Why learning people should care**: exp/log maps are how you interpolate poses, average
rotations, and define losses on SE(3) — the machinery under SE(3) diffusion/flow action
heads ([[01-canonical-papers/notes/4-vla/pi0|π0]]-style).

### Self-check

1. Verify Rodrigues for $\theta = 180°$ about $\hat z$. What matrix do you get?
2. A body rotates about an axis through the point $(0, 2, 0)$ (axis direction $\hat z$,
   speed 1 rad/s). What is its space twist $\mathcal{V}_s = (\omega_s, v_s)$?
3. Why does $[\hat\omega]^3 = -[\hat\omega]$ terminate the exponential series?
4. If $T$ is a pure translation by $p$, what does $[\text{Ad}_T]$ do to a twist?

> [!tip]- Answers
> 1. $\sin 180° = 0$ and $1-\cos 180° = 2$, so $R = I + 0 + 2[\hat z]^2 = \text{diag}(-1,-1,1)$ — the x and y axes flip, z is untouched.
> 2. $\omega_s = (0,0,1)$; the space-frame linear part is $v_s = -\omega \times q = -(0,0,1)\times(0,2,0) = (2,0,0)$ — the body point currently at the origin moves at 2 m/s in $+x$, even though the axis itself is stationary. This is §3's warning made numerical.
> 3. Because powers of a $3\times3$ skew-symmetric matrix cycle back to multiples of itself ($[\hat\omega]^3 = -[\hat\omega]$), every term of the infinite series collapses into a coefficient on $[\hat\omega]$ or $[\hat\omega]^2$ — leaving Rodrigues' three terms.
> 4. It leaves $\omega$ unchanged and maps $v \mapsto v + p\times\omega$ — the linear velocity is corrected by exactly the offset of the axis, which is why frame subscripts must be written every time.

### Problem set · 과제

Tier B. Using **P2** at $\theta=(0^\circ,90^\circ)$ from [[02-foundations/lab-plants|0.6]]. No simulator.

1. **Draw.** Base frame $\{s\}$ at the origin, elbow at $(1,0)$, tip at $(1,1)$. Put the tool frame $\{b\}$ at the tip with its $x$-axis along the forearm.
2. **Derive.** Write $T_{sb}$ of that tip (the lecture's $4\times4$). Then a pure $z$-rotation of the whole arm about the *elbow* $q_2=(1,0,0)$: space twist $\mathcal{V}_s=(\omega,v)$. Which three of the six $\mathfrak{se}(3)$ coordinates are still identically zero?
3. **Interpret.** Why is SE(2) enough here, and what goes wrong if a paper treats the space-twist linear part $v_s$ as the tip velocity at this pose?

> [!note]- How to draw it · 그리는 법
> - Draw the arm first: base at the origin, link 1 along $+x$ to the elbow at $(1,0)$, link 2 straight up to the tip at $(1,1)$.
> - The space frame $\{s\}$ at the origin: $\hat x_s$ right, $\hat y_s$ up, and $\hat z_s$ as a circled dot meaning out of the page. Draw the dot — a planar figure that does not declare which way $z$ points makes every sign in this chapter a coin flip.
> - The body frame $\{b\}$ at the tip, with $\hat x_b$ along the forearm, i.e. along $+\hat y_s$. Right-handedness then puts $\hat y_b$ along $-\hat x_s$ and $\hat z_b$ out of the page again.
> - The offset $p$ as a dashed arrow from the origin to the tip. $R_{sb}$ and $p$ are the whole of $T_{sb}$.
> - For item 2's twist, draw the rotation axis as a circled dot with a curved arrow around it, at the point $q$ it passes through, labelled with $\hat\omega$ and $\dot\theta$.
> - Write velocities beside the figure, not inside it: the tip's actual velocity $\hat\omega \times (p - q)$ next to the twist's linear part $v_s = -\hat\omega \times q$. The two must disagree whenever $p \ne 0$; if yours agree, you wrote $\dot p$ where the twist wants $v_s$.

> [!tip]- Solutions
> 1. Forearm along $+y_s$, so $x_b=\hat y_s$ and $y_b=-\hat x_s$ (right-handed, $z$ out).
> 2. $T_{sb}$ as in §4. Elbow axis: $\omega_s=(0,0,1)$, $v_s=-\omega\times q_2=(0,-1,0)$. Still $\omega_x=\omega_y=v_z=0$; $v_s$ is no longer $0$.
> 3. Motion stays in the plane, so SE(2) is the configuration group. At this pose $v_s=\dot p-\omega_s\times p$: a $1\,\mathrm{rad/s}$ spin about $z$ gives $\omega_s\times p=(-1,1,0)$, so $v_s$ is *not* the tip velocity unless $p=0$. Use the adjoint of §4.

## 한국어

**핵심 질문**: 강체의 회전·자세·속도를 특이점 없이 어떻게 표현하고 합성하는가?

책에서 가장 길게 느껴지는 장이고, 전체 공부 시간의 약 30%를 써도 되는 장이다 —
이후의 모든 장이 이 기계장치의 응용이기 때문이다. 네 단계로 나눠 잡아라.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 324" style="max-width:100%;height:auto" role="img" aria-label="카탈로그 자세의 P2에 베이스의 space 프레임, 말단의 body 프레임, 점선 오프셋 p = (1, 1, 0), 원점과 엘보를 지나는 회전축 둘을 그리고, 속도 숫자 넷을 옆에 적은 그림.">
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

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**, 카탈로그 자세 $\theta = (0^\circ, 90^\circ)$에 베이스의 space 프레임 $\{s\}$, $\hat x_b$가 전완 방향인 말단의 body 프레임 $\{b\}$, 점선 오프셋 $p = (1,1,0)$을 그렸다. $R_{sb} = R_z(90^\circ)$와 $p$가 $T_{sb}$의 전부이고, 동그라미 친 점은 지면 밖을 향하는 $z$축이다. 회전축 후보 둘은 모두 $\hat\omega = (0,0,1)$, $1\,\mathrm{rad/s}$로 원점 $q_1$과 엘보 $q_2 = (1,0,0)$을 지나며 말단을 $(-1,1,0)$과 $(-1,0,0)\,\mathrm{m/s}$로 움직이지만, 공간 트위스트의 선형 성분은 $v_s = (0,0,0)$과 $(0,-1,0)$이다 — $v_s = \dot p - \omega_s \times p$이지 $\dot p$가 아니므로 어느 쪽도 말단 속도가 아니다.

### 1. 반대칭 다리: 외적이 행렬이 된다

$\omega = (\omega_1, \omega_2, \omega_3)$에 대해
$$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}, \qquad [\omega]\,v = \omega \times v.$$
한 성분을 직접 검산하라: $[\omega]v$의 첫 행은 $-\omega_3 v_2 + \omega_2 v_3$ —
정확히 $\omega \times v$의 첫 성분이다. 왜 이렇게 하나? 외적이 행렬이 되는 순간
*회전 동역학에 선형대수가 통째로 적용*되기 때문이다 — 아래의 행렬 지수를 포함해서.

**대괄호가 하는 일.** 벡터 ω에는 각속도 좌표가 있다. 대괄호는 같은 좌표를 “ω와 외적하기” 연산을 수행하는 행렬로 포장한다. 새로운 물리 물체도 아니고 성분들이 독립 파라미터도 아니다. 부호는 외적의 오른손 법칙 방향을 담는다.

회전축에서 떨어진 점에서는 외적이 각속도 축과 변위 모두에 수직인 속도 성분을 준다. 축 위의 점에는 이 회전 속도가 없다. 같은 각속도라면 축에서 먼 점이 더 빠르다. 이 그림을 떠올리면 뜻 없이 외우는 대신 부호 배열을 복원할 수 있다.

**이해 확인.** 피연산자를 바꾸면 외적 부호가 반대가 되므로 [ω]v와 [v]ω는 일반적으로 서로 반대다. 행렬 표기는 합성을 쉽게 만들지만 외적을 교환 가능하게 만들지는 않는다. 기하 식을 코드로 옮길 때 순서를 확인한다.

### 2. 왜 지수함수인가? 회전은 선형 미분방정식이다

일정한 각속도로 도는 프레임은 공간 프레임에서 표현한 $\omega_s$로 $\dot R = [\omega_s]\,R$을 따른다(바디 프레임으로는 $\dot R = R\,[\omega_b]$; MR §3.2.2). 두 형태가 같은 이유는 $\omega_s = R\,\omega_b$이고 괄호 행렬을 회전하면 $[R\,\omega_b] = R\,[\omega_b]\,R^\top$이 되어, $[\omega_s]\,R = R\,[\omega_b]\,R^\top R = R\,[\omega_b]$이기 때문이다.
$\dot x = ax$의 행렬판이다 — 그러므로 해도 $e^{at}$의 행렬판이다: 단위축 $\hat\omega$
둘레로 "시간" $\theta$만큼 돌면
$$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2 \quad \text{(로드리게스 공식)}.$$
무한급수가 세 항으로 접히는 이유는 $[\hat\omega]^3 = -[\hat\omega]$이기 때문이다.

**검산 예제** — $\hat z = (0,0,1)$ 둘레 $\theta = 90°$ 회전:
$[\hat z] = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}$, $[\hat z]^2 = \begin{pmatrix}-1&0&0\\0&-1&0\\0&0&0\end{pmatrix}$을 대입하면
$$R = I + (1)[\hat z] + (1)[\hat z]^2 = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$$
— 정확히 $R_z(90°)$이고, $\hat x$를 $\hat y$로 보낸다. 모든 회전은 *하나의* 축-각
지수다(오일러 정리); $\log$가 $R$에서 $(\hat\omega, \theta)$를 복원한다. 이 exp/log 쌍이
리 군(회전)과 리 대수(각속도) 사이의 문이고 — 자세를 올바르게 보간하고 평균할 수 있는
이유다.

### 3. Twist: 강체의 속도는 여섯 숫자 — 단, $v$를 조심해서 읽어라

움직이는 강체의 속도는 **twist** $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$이다.
**$v$의 뜻은 기준 프레임과 원점에 달렸다.** 공간 트위스트는 고정 공간 원점을 기준으로 속도장을 나타내고, 바디 트위스트는 움직이는 바디 원점을 쓴다. 이 선택 없이 두 선형 성분을 같은 것으로 읽으면 안 된다. 0이 아닌 모든 twist는
**스크류**다: 축 둘레로 돌면서 그 축 방향으로 나아가는 운동이다. **피치** $h$는 축 둘레로
1라디안 도는 동안 그 축 방향으로 얼마나 나아가는가이고 단위는 m/rad다. 즉 $h = 0.01$ m/rad인
스크류는 1라디안 회전마다 축 방향으로 1 cm 나아간다. 나사산의 피치와 같은 뜻이다. 이렇게 읽으면
두 극한이 바로 보인다. 순수 병진은 피치가 **무한대**인 경우이고(돌지 않는데도 나아간다), 순수
회전이 피치 0인 경우다(MR 정의 3.24: 순수 회전이면 $h = 0$, $\omega = 0$이면 $h \to \infty$).

**바디 원점과 공간 원점을 나눈다.** p가 공간 좌표에서 바디 원점의 위치라 하자. 공간 트위스트의 선형 성분은 v_s = ṗ − ω_s × p다. 바디 원점의 속도를 얻으려면 회전 항을 다시 더해야 한다. 바디 트위스트의 선형 성분은 v_b = Rᵀṗ로, 바디 원점의 속도를 바디 좌표로 표현한 것이다. 따라서 “v는 도구 끝 속도가 아니다”에는 프레임 조건이 필요하다. 바디 원점이 도구 끝이면 바로 그 점의 속도일 수 있다.

고정된 자기 끝점을 축으로 도는 도구를 상상한다. 끝점은 병진하지 않아도 도구의 다른 점들은 움직인다. 공간 원점 기준 표현은 끝점 궤적뿐 아니라 전체 속도장을 복원할 정보를 담아야 한다. 원점을 옮기면 같은 운동을 설명하는 데 필요한 선형 성분도 바뀐다.

**이해 확인.** 표현 프레임과 속도를 알고 싶은 점을 모두 말한다. [공식 트위스트 설명](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-2-twists-part-1-of-2/)이 이 차이를 다룬다. 이를 섞으면 수치적으로 올바른 야코비안도 잘못된 병진을 명령하는 것처럼 보인다.

### 4. 하나의 운동, 두 개의 기술: space 프레임 vs body 프레임

같은 물리적 운동을 고정 프레임에서 쓰면 $\mathcal{V}_s$, 움직이는 몸체 프레임에서 쓰면
$\mathcal{V}_b$다. 둘은 현재 자세 $T = (R, p)$의 **adjoint**로 연결된다:
$$\mathcal{V}_s = [\text{Ad}_T]\,\mathcal{V}_b, \qquad [\text{Ad}_T] = \begin{pmatrix} R & 0 \\ [p]R & R\end{pmatrix}.$$
윗줄은 $\omega_s = R\,\omega_b$라는 뜻이다. 모서리의 $[p]R$은 §3의 공간 트위스트 식 $v_s = \dot p - \omega_s \times p$에서 나온다: 바디 원점의 속도가 $\dot p = R\,v_b$이므로 $v_s = R\,v_b + p \times \omega_s = R\,v_b + [p]R\,\omega_b$다. 말로 하면, $v_s$는 공간 원점에 놓인 가상의 물체 점(바디 원점에서 $-p$만큼 떨어진 점)을 기술하고, 바디 원점을 중심으로 도는 회전이 그 점을 $p \times \omega_s$만큼 옆으로 쓸고 간다.
외울 가치가 있는 특수 사례: $p = 0$(순수 회전)이면 그냥 "양쪽을 회전"이다:
$\omega_s = R\,\omega_b$, $v_s = R\,v_b$. **프레임 아래 첨자는 장식이 아니다** — 이후
장들의 부호 실수 대부분이 $s$/$b$ 혼동이므로, 매번 아래 첨자를 써라. 자세의 지수도
회전과 같다: $T = e^{[\mathcal{S}]\theta}$ = "스크류 $\mathcal{S}$를 $\theta$만큼
따라가라."

**계산: 장치 P2의 $T_{sb}$.** 카탈로그 자세 $\theta=(0^\circ,90^\circ)$, 말단 $(1,1)$([[02-foundations/lab-plants|0.6]]). $\{b\}$를 말단에 두고 $x$축을 전완, 곧 $+\hat y_s$에 둔다. 지면 밖으로 $z$인 오른손 프레임이면 $y_b=-\hat x_s$이고

$$R_{sb}=R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},\qquad p=(1,1,0),\qquad T_{sb}=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$

원점 둘레로 팔 전체를 도는 순수 $z$ 회전의 공간 트위스트는 $\mathcal{V}_s=((0,0,1),(0,0,0))$: 원점을 지나는 축이라 $v_s=-\omega\times 0=0$. 말단은 움직인다. $v_s$는 말단 속도가 아니다. 이 $p$에서 $\omega_s\times p=(-1,1,0)$이 $1\,\mathrm{rad/s}$의 말단 속도이고, $v_s=\dot p-\omega_s\times p$가 §3의 구분을 되살린다. 평면 P2는 항상 $\omega_x=\omega_y=v_z=0$이라 SE(2)로 충분하다 — 논문이 $v_s$를 $\dot p$로 취급하기 전까지. 과제는 이 $T_{sb}$를 유지하고 *엘보* 둘레 twist를 묻는다.

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="하나의 물리적 운동을 고정 프레임에서, 그리고 몸체 프레임에서 기술한 것">
  <defs><marker id="mr3ak" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <line x1="45" y1="150" x2="45" y2="100"/><line x1="45" y1="150" x2="95" y2="150"/>
  </g>
  <g fill="currentColor"><circle cx="45" cy="150" r="3.5"/></g>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <line x1="250" y1="95" x2="216" y2="60"/><line x1="250" y1="95" x2="285" y2="61"/>
  </g>
  <g fill="currentColor"><circle cx="250" cy="95" r="3.5"/></g>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.5" stroke-dasharray="4 3"><line x1="45" y1="150" x2="250" y2="95"/></g>
  <g stroke="currentColor" stroke-width="2.4" fill="none" opacity="0.85">
    <path d="M250,95 C300,70 340,80 372,110" marker-end="url(#mr3ak)"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="26" y="172">space 프레임 {s}</text><text x="234" y="120">body 프레임 {b}</text>
    <text x="130" y="112" font-size="10.5" opacity="0.8">p, R</text>
    <text x="300" y="66">하나의 운동</text>
    <text x="20" y="30">같은 화살표, 두 벌의 숫자</text>
    <text x="20" y="188" opacity="0.9">운동 자체는 아무것도 바뀌지 않는다 &#8212; 어느 프레임에서 쓰느냐만 다르다. [Ad_T]가 둘을 변환하고,</text>
    <text x="20" y="204" opacity="0.9">R과 p가 둘 다 필요하다: 프레임이 떨어져 있으면 회전만으로는 부족하다.</text>
  </g>
</svg>



**학습 쪽에서 중요한 이유**: exp/log 사상이 자세 보간, 회전 평균, SE(3) 위의 손실 정의의
방법이고 — SE(3) 디퓨전/flow 행동 헤드([[01-canonical-papers/notes/4-vla/pi0|π0]]류)의
밑바닥 기계장치다.

### 스스로 점검

1. $\hat z$ 둘레 $\theta = 180°$에 대해 로드리게스를 검산하라. 어떤 행렬이 나오는가?
2. 몸체가 점 $(0, 2, 0)$을 지나는 축($\hat z$ 방향, 1 rad/s) 둘레로 돈다.
   space twist $\mathcal{V}_s = (\omega_s, v_s)$는?
3. $[\hat\omega]^3 = -[\hat\omega]$가 지수 급수를 세 항으로 끝내는 이유는?
4. $T$가 $p$만큼의 순수 병진이면 $[\text{Ad}_T]$는 twist에 무슨 일을 하는가?

> [!tip]- 정답 · Answers
> 1. $\sin 180° = 0$, $1-\cos 180° = 2$이므로 $R = I + 0 + 2[\hat z]^2 = \text{diag}(-1, -1, 1)$ — x·y축이 뒤집히고 z는 그대로다.
> 2. $\omega_s = (0,0,1)$; 공간 프레임의 선형 성분은 $v_s = -\omega \times q = -(0,0,1)\times(0,2,0) = (2,0,0)$ — 지금 원점에 있는 물체 위의 점이 $+x$로 2 m/s로 움직인다는 뜻이고, 축 자체는 정지해 있다. §3의 경고를 수치로 옮긴 것이다.
> 3. 3×3 반대칭 행렬의 거듭제곱이 자기 자신의 배수로 되돌아오기 때문 — 급수의 모든 항이 $[\hat\omega]$, $[\hat\omega]^2$의 계수로 흡수된다.
> 4. $\omega$는 그대로, $v \mapsto v + p \times \omega$.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**, $\theta=(0^\circ,90^\circ)$. 시뮬레이터 없음.

1. **그리기.** 원점의 베이스 $\{s\}$, 엘보 $(1,0)$, 말단 $(1,1)$. 말단에 도구 프레임 $\{b\}$, $x$축은 전완 방향.
2. **유도.** 그 말단의 $T_{sb}$(강의의 $4\times4$). 그다음 엘보 $q_2=(1,0,0)$ 둘레로 팔 전체를 도는 순수 $z$ 회전의 space twist $\mathcal{V}_s=(\omega,v)$. 여섯 $\mathfrak{se}(3)$ 좌표 중 여전히 0인 셋은?
3. **해석.** 왜 SE(2)면 충분한가? 이 자세에서 space twist의 $v_s$를 말단 속도로 읽으면 무엇이 틀리는가?

> [!note]- 그리는 법 · How to draw it
> - 팔부터 그린다. 베이스는 원점, 링크 1은 $+x$로 뻗어 엘보가 $(1,0)$, 링크 2는 곧장 위로 올라가 말단이 $(1,1)$.
> - 원점의 space 프레임 $\{s\}$: $\hat x_s$는 오른쪽, $\hat y_s$는 위, $\hat z_s$는 지면 밖을 뜻하는 동그라미 친 점. 점을 반드시 그린다. 셋째 축이 어디를 향하는지 말하지 않는 평면 그림에서는 이 장의 모든 부호가 동전 던지기가 된다.
> - 말단의 body 프레임 $\{b\}$는 $\hat x_b$를 전완 방향, 곧 $+\hat y_s$ 방향에 둔다. 그러면 오른손 규칙에 따라 $\hat y_b$는 $-\hat x_s$ 방향이고 $\hat z_b$도 다시 지면 밖이다.
> - 오프셋 $p$는 원점에서 말단까지의 점선 화살표로. $R_{sb}$와 $p$가 $T_{sb}$의 전부다.
> - 2번의 트위스트를 위해 회전축은 그 축이 지나는 점 $q$에 동그라미 친 점과 그 둘레의 굽은 화살표로 그리고, $\hat\omega$와 $\dot\theta$를 적는다.
> - 속도는 그림 안이 아니라 옆에 적는다. 말단의 실제 속도 $\hat\omega \times (p - q)$와 트위스트의 선형 성분 $v_s = -\hat\omega \times q$를 나란히 쓴다. $p \ne 0$이면 둘은 반드시 달라야 하고, 같게 나왔다면 트위스트가 $v_s$를 원하는 자리에 $\dot p$를 쓴 것이다.

> [!tip]- 정답 · Solutions
> 1. 전완이 $+y_s$이므로 $x_b=\hat y_s$, $y_b=-\hat x_s$(오른손 프레임, $z$는 지면 밖).
> 2. $T_{sb}$는 §4. 엘보 축: $\omega_s=(0,0,1)$, $v_s=-\omega\times q_2=(0,-1,0)$. 여전히 $\omega_x=\omega_y=v_z=0$; $v_s$는 이제 0이 아니다.
> 3. 운동이 평면에 남으므로 SE(2)가 컨피규레이션 군이다. 이 자세에서 $v_s=\dot p-\omega_s\times p$이고, $z$축 둘레 $1\,\mathrm{rad/s}$ 회전이면 $\omega_s\times p=(-1,1,0)$이므로 $p\neq0$이면 $v_s$는 말단 속도가 아니다. §4의 adjoint를 쓴다.
