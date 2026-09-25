---
title: 8. 3D Geometry & SE(3)
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §4]] (matrix multiplication, transpose) · [[02-foundations/linear-algebra|1. Linear Algebra §1]] (norms) · [[02-foundations/linear-algebra|1. Linear Algebra §4]] (orthogonal matrices — columns unit-length and mutually orthogonal, which is what $R^\top R = I$ says). Trigonometry is enough; no group theory is assumed.
> [[02-foundations/engineering-math|0.5 §4]](행렬곱·전치) · [[02-foundations/linear-algebra|1. 선형대수 §1]](노름) · [[02-foundations/linear-algebra|1. 선형대수 §4]](직교행렬 — 열이 단위길이이고 서로 직교, 즉 $R^\top R = I$가 말하는 것). 삼각함수면 충분하고 군론은 전제하지 않는다.
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/linear-algebra|1. Linear Algebra]] alone — it owes nothing to RL or signal processing. It is here because the robotics
track and the VLA papers (vision–language–action models, which turn an instruction and camera images into robot motion) need it next: the space a robot's states and actions are actually written in.*

Every robot action, camera pose, and 3D reconstruction in this wiki lives in SE(3) — the
space of rigid-body poses. This page is the working set for reading VLA action spaces and
3D vision papers; the full treatment (screws, exponential coordinates) lives in
[[04-robotics/modern-robotics-book|Modern Robotics ch. 3]].

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]], SE(3) is part of the mathematics floor under the perception, grasping, motion-planning and manipulation layers — every camera pose, grasp pose and tool pose is one of its elements — and in *"install that panel on the frame"* it serves three steps: *identify panel and frame*, *plan a grasp* and *move the component* (its chip sits on the mathematics floor of the [[physical-ai-map|Physical AI Map]]). Most integration bugs are frame bugs: add a camera's offset to its base's position without first rotating the offset into the world, and the camera lands $1.41\,\mathrm m$ from where it really is (§3's worked composition). Later pages build on this one section by section — [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]] its camera extrinsics (the camera's pose on the robot) on this page's §1–§3, [[04-robotics/state-estimation-slam|3. State Estimation]] its pose graphs (poses linked by measurements) on §2–§3, [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]] its twists and adjoints on §1, §3 and §4, [[04-robotics/grasping|15. Grasping]] its grasp-quality measure on §1's cross product, and [[05-construction-robotics/assembly-fabrication|4. Robotic Assembly & Fabrication]] its hole alignment on §4's small rotations — and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) it is tested by question 13 of block 1's [[02-foundations/overview#Gate check — are the foundations done?|foundations gate]] and used from block 2, the robotics common track, onward. After it you can build and check a rotation, compose and invert $4\times4$ poses with their subscripts cancelling, and say in which frame a velocity is written.

> [!note] First pass · 처음이라면
> About two sessions of 60–90 minutes. **Session 1:** the Running object and the picture, then §1 through the rotation check and the cross product's right-hand test — the 2D rotation, the order example and its figure come first. **Session 2:** §3, where poses compose by matrix product and a motion multiplies on the right or on the left; skim §2's table and §5; then self-checks 1, 3 and 4, question 13 of the [[02-foundations/overview#Gate check — are the foundations done?|gate check]], and problem 1, the Draw item. The rest of §2, all of §4 and every collapsed *Deeper* note are the second pass; read §4 before problem-set item 3, or when you reach Modern Robotics.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], one of the wiki's six frozen *plants* (control's word for the system being controlled): a planar arm of two $1\,\mathrm m$ links, its joint angles measured from the $x$-axis and the elbow's relative to the first link. At the catalog pose $\theta=(0^\circ,90^\circ)$ the elbow sits at $(1,0)$ and the tip at $(1,1)\,\mathrm m$. This page ignores the arm's masses and draws it as two **frames**. A frame here is a coordinate system attached to a body — an origin and three perpendicular unit axes, right-handed — and not a structural frame. Two frames carry the whole page, under Modern Robotics' letters: **$\{s\}$**, the *space* frame, fixed to the base at the shoulder, and **$\{b\}$**, the *body* frame, fixed to the tool at the tip. So $b$ means *body*, not base; §3's worked composition adds a world $A$, a base $B$ and a camera $C$, in capitals.

*Scope: this page teaches rotations and their four common representations, poses as $4\times4$ matrices, and a rigid body's six-number velocity, all on P2. It does not teach screw theory, exponential coordinates or the forward kinematics of a general arm, which are [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]] and [[04-robotics/modern-robotics/ch04-forward-kinematics|MR ch.4]], nor camera models, which are [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 490" style="max-width:100%;height:auto" role="img" aria-label="plant P2 at theta = (0°, 90°) drawn as two frames: base axes at the origin, tool axes at the tip (1, 1) turned 90°, the position arrow p, a point 0.1 m along the tool x-axis and the tool x-direction, the matrices R and T read off the drawing, and a margin box with the base origin seen from the tool">
  <defs><marker id="arSe" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="7" stroke-opacity="0.13" stroke-linecap="round" fill="none"><line x1="80.0" y1="300.0" x2="230.0" y2="300.0"/><line x1="230.0" y1="300.0" x2="230.0" y2="150.0"/></g>
  <circle cx="230.0" cy="300.0" r="4" fill="none" stroke="currentColor" stroke-opacity="0.3"/>
  <text x="240.0" y="320.0" fill="currentColor" opacity="0.6">elbow (1, 0)</text>
  <line x1="87.0" y1="300.0" x2="155.0" y2="300.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSe)"/>
  <line x1="80.0" y1="293.0" x2="80.0" y2="225.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSe)"/>
  <circle cx="80.0" cy="300.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="80.0" cy="300.0" r="2" fill="currentColor"/>
  <text x="160.0" y="304.0" fill="currentColor" font-size="13">x<tspan dy="3" font-size="11">s</tspan></text>
  <text x="74.0" y="231.0" fill="currentColor" font-size="13" text-anchor="end">y<tspan dy="3" font-size="11">s</tspan></text>
  <text x="70.0" y="320.0" fill="currentColor" font-size="13" text-anchor="end">z<tspan dy="3" font-size="11">s</tspan></text>
  <text x="90.0" y="320.0" fill="currentColor" opacity="0.9">base (0, 0)</text>
  <line x1="230.0" y1="143.0" x2="230.0" y2="75.0" stroke="currentColor" stroke-width="2.4" marker-end="url(#arSe)"/>
  <line x1="223.0" y1="150.0" x2="155.0" y2="150.0" stroke="currentColor" stroke-width="2.4" marker-end="url(#arSe)"/>
  <circle cx="230.0" cy="150.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="230.0" cy="150.0" r="2" fill="currentColor"/>
  <text x="236.0" y="80.0" fill="currentColor" font-size="13">x<tspan dy="3" font-size="11">b</tspan></text>
  <text x="150.0" y="155.0" fill="currentColor" font-size="13" text-anchor="end">y<tspan dy="3" font-size="11">b</tspan></text>
  <text x="240.0" y="170.0" fill="currentColor" font-size="13">z<tspan dy="3" font-size="11">b</tspan></text>
  <text x="240.0" y="185.0" fill="currentColor" opacity="0.9">tip (1, 1)</text>
  <line x1="86.4" y1="293.6" x2="223.6" y2="156.4" stroke="currentColor" stroke-width="1.4" marker-end="url(#arSe)" stroke-dasharray="6 4" stroke-opacity="0.8"/>
  <text x="150.0" y="262.0" fill="currentColor">p = (1, 1, 0)</text>
  <circle cx="230.0" cy="135.0" r="3.4" fill="currentColor"/>
  <line x1="226.0" y1="132.0" x2="214.0" y2="117.0" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="212.0" y="104.0" fill="currentColor" text-anchor="end">point: tool (0.1, 0, 0)</text>
  <text x="212.0" y="118.0" fill="currentColor" text-anchor="end">= base (1, 1.1, 0)</text>
  <line x1="258.0" y1="150.0" x2="258.0" y2="112.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSe)"/>
  <text x="266.0" y="126.0" fill="currentColor">direction</text>
  <text x="266.0" y="140.0" fill="currentColor">(0, 1, 0)</text>
  <text x="14.0" y="24.0" fill="currentColor">• point, 4th entry 1: rotated and shifted</text>
  <text x="14.0" y="38.0" fill="currentColor">↑ direction, 4th entry 0: rotated only</text>
  <text x="14.0" y="344.0" fill="currentColor" opacity="0.85">⊙ = z, out of the page (right-handed)</text>
  <text x="346.0" y="300.0" fill="currentColor" font-size="12">s = space frame, fixed to the base</text>
  <text x="346.0" y="316.0" fill="currentColor" font-size="12">b = body frame, fixed to the tool</text>
  <rect x="340" y="60" width="212" height="192" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="350.0" y="80.0" fill="currentColor">inverse: the same picture</text>
  <text x="350.0" y="94.0" fill="currentColor" opacity="0.9">read backwards</text>
  <line x1="500.0" y1="129.0" x2="500.0" y2="105.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSe)"/>
  <line x1="493.0" y1="136.0" x2="469.0" y2="136.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSe)"/>
  <circle cx="500.0" cy="136.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="500.0" cy="136.0" r="2" fill="currentColor"/>
  <text x="506.0" y="110.0" fill="currentColor" font-size="13">x<tspan dy="3" font-size="11">b</tspan></text>
  <text x="464.0" y="141.0" fill="currentColor" font-size="13" text-anchor="end">y<tspan dy="3" font-size="11">b</tspan></text>
  <path d="M500.0 136.0 L500.0 186.0 L450.0 186.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="2 3"/>
  <line x1="500.0" y1="136.0" x2="450.0" y2="186.0" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 3"/>
  <circle cx="450.0" cy="186.0" r="3.4" fill="currentColor"/>
  <text x="506.0" y="165.0" fill="currentColor" opacity="0.8">1</text>
  <text x="475.0" y="200.0" fill="currentColor" text-anchor="middle" opacity="0.8">1</text>
  <text x="467.0" y="159.0" fill="currentColor" text-anchor="end">√2</text>
  <text x="442.0" y="190.0" fill="currentColor" text-anchor="end">base origin</text>
  <text x="350.0" y="214.0" fill="currentColor">base origin in tool coords:</text>
  <text x="350.0" y="228.0" fill="currentColor">(−1, 1, 0) = −R<tspan dy="-4" font-size="11">T</tspan><tspan dy="4">p,</tspan></text>
  <text x="350.0" y="242.0" fill="currentColor">still √2 from the tip</text>
  <text x="14.0" y="372.0" fill="currentColor">R: each column read off a tip axis</text>
  <text x="84.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">x<tspan dy="3" font-size="11">b</tspan></text>
  <text x="114.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">y<tspan dy="3" font-size="11">b</tspan></text>
  <text x="144.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">z<tspan dy="3" font-size="11">b</tspan></text>
  <text x="84.0" y="410.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="114.0" y="410.0" fill="currentColor" font-size="12" text-anchor="middle">−1</text>
  <text x="144.0" y="410.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="84.0" y="426.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="114.0" y="426.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="144.0" y="426.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="84.0" y="442.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="114.0" y="442.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="144.0" y="442.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <path d="M71 398 L66 398 L66 447 L71 447" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M157 398 L162 398 L162 447 L157 447" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="24.0" y="426.0" fill="currentColor" font-size="12">R =</text>
  <text x="172.0" y="426.0" fill="currentColor" font-size="12">= R<tspan dy="3" font-size="11">z</tspan><tspan dy="-3">(90°)</tspan></text>
  <text x="14.0" y="466.0" fill="currentColor">columns unit, mutually ⟂: R<tspan dy="-4" font-size="11">T</tspan><tspan dy="4">R = I</tspan></text>
  <text x="14.0" y="480.0" fill="currentColor">x<tspan dy="3" font-size="11">b</tspan><tspan dx="3.3" dy="-3">× y</tspan><tspan dy="3" font-size="11">b</tspan><tspan dx="3.3" dy="-3">= +z</tspan><tspan dy="3" font-size="11">b</tspan><tspan dy="-3">: det R = +1</tspan></text>
  <text x="268.0" y="372.0" fill="currentColor">T: R in the corner, p in the last column</text>
  <text x="312.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="338.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">−1</text>
  <text x="364.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="390.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="312.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="338.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="364.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="390.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="312.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="338.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="364.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="390.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="312.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="338.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="364.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="390.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <path d="M301 380 L296 380 L296 445 L301 445" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M401 380 L406 380 L406 445 L401 445" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="268.0" y="420.0" fill="currentColor" font-size="12">T =</text>
  <rect x="300" y="381" width="77" height="47" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <rect x="378" y="381" width="24" height="47" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <rect x="300" y="429" width="102" height="15" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="414.0" y="408.0" fill="currentColor">← p = (1, 1, 0)</text>
  <text x="414.0" y="440.0" fill="currentColor">← fixed (0, 0, 0, 1)</text>
  <text x="268.0" y="466.0" fill="currentColor" opacity="0.9">the bottom row is not decoration (§3)</text>
</svg>

**P2** at $\theta=(0^\circ,90^\circ)$, drawn as its two frames rather than as an arm: the body frame $\{b\}$ sits at the tip $p=(1,1,0)$ with $x_b$ up the page and $y_b$ to the left, so its axes, read off in the coordinates of the space frame $\{s\}$ at the base, are the columns of $R=R_z(90^\circ)$, and $T$ holds $R$ in the corner, $p$ in the last column and $(0,0,0,1)$ below. A point $0.1\,\mathrm{m}$ out along the tool's $x$-axis lands at base $(1,\ 1.1,\ 0)$, rotated and shifted, while the tool's $x$-direction becomes $(0,1,0)$, rotated only. The margin box reads the same picture backwards: the base origin sits at $(-1,\ 1,\ 0)=-R^\top p$ in tool coordinates, still $\sqrt2$ from the tip.

### 1. Rotations are matrices with rules

A robot has to say how every part is turned — the tool relative to the base, the camera relative to the tool — and turns do not add like numbers: the same two turns in the other order leave the tool pointing somewhere else. This section gives the two rules a rotation matrix obeys, so that you can build one, check one and compose two. You have met the object before if you have analysed a plane frame or truss: the matrix that carries a member's local axes into the structure's global axes is a rotation matrix.

- A 3D rotation is a matrix $R \in \mathbb{R}^{3\times 3}$ with $R^\top R = I$ and
  $\det R = +1$ — the set of all such matrices is the **group SO(3)**.
  "Group" is the algebraic word for a set closed under composition where every element has an inverse.
  Here that means a rotation times a rotation is a rotation, and every rotation can be undone.
  That is all the word carries here; its four axioms are in the *Deeper* note at the end of this section.
  - **The two defining conditions, each named.** Written as a set,
    $$SO(3)=\{R\in\mathbb{R}^{3\times3} : R^\top R=I,\ \det R=+1\}$$
    so a matrix belongs exactly when it passes both tests. (1) **Orthogonality**, $R^\top R=I$: it preserves lengths and angles, since $(Rx)^\top(Ry)=x^\top R^\top R\,y=x^\top y$. (2) **Orientation preservation**, $\det R=+1$: it keeps a right-handed frame right-handed. Orthogonality alone already forces $\det R=\pm1$, and the second condition throws out the $-1$ half, the reflections. "S" is for *special* ($\det=+1$), "O" for *orthogonal*, and $3$ for the dimension.
  - **Non-example.** $S=\text{diag}(2,1,1)$ is not a rotation: $S^\top S=\text{diag}(4,1,1)\ne I$, it stretches the $x$-axis.
- Consequences: columns are an orthonormal frame (the rotated x/y/z axes);
  $R^{-1} = R^\top$ (undoing a rotation is free); rotations compose by multiplication,
  and **order matters** ($R_1 R_2 \ne R_2 R_1$ — rotate your phone about two axes in both
  orders to feel it).
- 2D worked example: $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$
  — check $R(90°)\,(1,0)^\top = (0,1)^\top$. All of SO(3) is this idea, three axes at once.
- **Order matters — with numbers, so you never have to trust the phone demo.** Take the two axis rotations — each comes from the 2D rotation above, placed in the plane perpendicular to its axis:
  $$R_z(90°) = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}, \qquad R_x(90°) = \begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$$
  and track the point $p = (1,0,0)$ — the tip of the x-axis.
  - $R_z$ **first**, then $R_x$: $R_z p = (0,1,0)$, and $R_x(0,1,0) = (0,0,1)$. The point
    ends up on the **z**-axis.
  - $R_x$ **first**, then $R_z$: $R_x p = (1,0,0)$ (a rotation about x does nothing to a
    point *on* x), and $R_z(1,0,0) = (0,1,0)$. The point ends up on the **y**-axis.

  Same two rotations, two completely different places. Nothing subtle is happening: the
  second rotation acts on wherever the first one *left* you. This is why a paper writing
  $R_{world}R_{body}$ versus $R_{body}R_{world}$ is describing different motions, and why
  every convention mismatch in robotics is ultimately this.

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="the point (1,0,0) rotated by R_z then R_x ends on the z-axis; rotated by R_x then R_z it ends on the y-axis">
  <defs><marker id="seOrd" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5" fill="none"><line x1="140.0" y1="132.0" x2="202.4" y2="168.0"/><line x1="140.0" y1="132.0" x2="77.6" y2="168.0"/><line x1="140.0" y1="132.0" x2="140.0" y2="60.0"/></g>
  <g font-size="12" fill="currentColor" fill-opacity="0.8"><text x="210.4" y="180.0">y</text><text x="61.6" y="180.0">x</text><text x="136.0" y="52.0">z</text></g>
  <circle cx="140.0" cy="132.0" r="2.5" fill="currentColor" fill-opacity="0.6"/>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="5 4" marker-end="url(#seOrd)">
    <path d="M81.6,171.0 Q140.0,197.8 196.4,172.0"/>
    <path d="M204.4,162.0 Q197.0,99.1 143.0,67.0"/>
  </g>
  <circle cx="77.6" cy="168.0" r="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="140.0" cy="60.0" r="4.5" fill="currentColor"/>
  <text x="140.0" y="199.8" font-size="12" fill="currentColor" text-anchor="middle">1: R<tspan dy="3" font-size="10">z</tspan><tspan dy="-3"> (90°)</tspan></text>
  <text x="205.0" y="95.1" font-size="12" fill="currentColor">2: R<tspan dy="3" font-size="10">x</tspan><tspan dy="-3"> (90°)</tspan></text>
  <text x="140.0" y="30" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600"><tspan>R</tspan><tspan dy="3" font-size="10">z</tspan><tspan dx="4" dy="-3">first, then R</tspan><tspan dy="3" font-size="10">x</tspan></text>
  <text x="140.0" y="218" font-size="12" fill="currentColor" text-anchor="middle">(1,0,0) → (0,1,0) → (0,0,1)</text>
  <text x="140.0" y="236" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">ends on z</text>
  <g stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5" fill="none"><line x1="400.0" y1="132.0" x2="462.4" y2="168.0"/><line x1="400.0" y1="132.0" x2="337.6" y2="168.0"/><line x1="400.0" y1="132.0" x2="400.0" y2="60.0"/></g>
  <g font-size="12" fill="currentColor" fill-opacity="0.8"><text x="470.4" y="180.0">y</text><text x="321.6" y="180.0">x</text><text x="396.0" y="52.0">z</text></g>
  <circle cx="400.0" cy="132.0" r="2.5" fill="currentColor" fill-opacity="0.6"/>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="5 4" marker-end="url(#seOrd)">
    <path d="M341.6,171.0 Q400.0,197.8 456.4,172.0"/>
  </g>
  <circle cx="337.6" cy="168.0" r="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="462.4" cy="168.0" r="4.5" fill="currentColor"/>
  <text x="329.6" y="144.0" font-size="12" fill="currentColor" text-anchor="end">1: R<tspan dy="3" font-size="10">x</tspan><tspan dy="-3">(90°)</tspan></text>
  <text x="329.6" y="159.0" font-size="12" fill="currentColor" text-anchor="end">stays put</text>
  <text x="400.0" y="199.8" font-size="12" fill="currentColor" text-anchor="middle">2: R<tspan dy="3" font-size="10">z</tspan><tspan dy="-3"> (90°)</tspan></text>
  <text x="400.0" y="30" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600"><tspan>R</tspan><tspan dy="3" font-size="10">x</tspan><tspan dx="4" dy="-3">first, then R</tspan><tspan dy="3" font-size="10">z</tspan></text>
  <text x="400.0" y="218" font-size="12" fill="currentColor" text-anchor="middle">(1,0,0) → (1,0,0) → (0,1,0)</text>
  <text x="400.0" y="236" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">ends on y</text>
</svg>

The point $(1,0,0)$, the tip of the $x$-axis, under the same two $90^\circ$ rotations in both orders. $R_z$ first carries it to $(0,1,0)$ and $R_x$ then lifts it to $(0,0,1)$; $R_x$ first leaves it where it is, since it lies on the $x$-axis, and $R_z$ then carries it to $(0,1,0)$ — so $R_xR_z\ne R_zR_x$.

- **The elementary rotations, for any angle.** The two matrices above are the $\theta=90°$ cases of the three rotations about the coordinate axes:
  $$R_x(\theta)=\begin{pmatrix}1&0&0\\0&c&-s\\0&s&c\end{pmatrix},\quad R_y(\theta)=\begin{pmatrix}c&0&s\\0&1&0\\-s&0&c\end{pmatrix},\quad R_z(\theta)=\begin{pmatrix}c&-s&0\\s&c&0\\0&0&1\end{pmatrix}$$
  with $c=\cos\theta$ and $s=\sin\theta$, so each leaves its own axis fixed and applies the 2D rotation to the other two coordinates. $R_y$'s signs look flipped because the right-hand rule orders that plane as $z$ then $x$. A positive $\theta$ turns counterclockwise when you look from the positive axis back toward the origin.
- **Checking a matrix is a rotation**, which you should do whenever you build one: columns
  must have length 1, be mutually perpendicular, and $\det = +1$. For $R_z(90°)$: columns are
  $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ — unit length ✓, pairwise dot products all 0 ✓, and
  $\det = +1$ ✓. A $\det$ of $-1$ means you built a **reflection**, which mirrors the robot
  rather than turning it — a real and common bug when converting conventions.
- **The cross product and its matrix, stated completely.** The cross product is an operation that takes two vectors in $\mathbb{R}^3$ and returns a third; it exists only in three dimensions. For $a=(a_1,a_2,a_3)$ and $b=(b_1,b_2,b_3)$,
  $$a\times b=\big(a_2b_3-a_3b_2,\ \ a_3b_1-a_1b_3,\ \ a_1b_2-a_2b_1\big)$$
  so the result has three defining properties: it is perpendicular to both inputs, $a^\top(a\times b)=b^\top(a\times b)=0$; its length is $\lVert a\rVert\lVert b\rVert\sin\varphi$, with $\varphi$ the angle between them, which is the area of the parallelogram they span; and its direction follows the right-hand rule (curl the fingers from $a$ toward $b$ and the thumb points along $a\times b$). Two rules follow from the formula. It is **anticommutative**, $b\times a=-a\times b$, so $a\times a=0$; and it is **not associative**. Because every component is linear in $b$, "cross with $a$" is a matrix, the **skew-symmetric matrix** of $a$:
  $$[a]_\times=\begin{pmatrix}0&-a_3&a_2\\a_3&0&-a_1\\-a_2&a_1&0\end{pmatrix},\qquad a\times b=[a]_\times b$$
  so $[a]_\times^\top=-[a]_\times$ (that is what skew-symmetric means): zeros on the diagonal and exactly three free entries, the components of $a$. Example: $a=(1,2,3)$ and $b=(4,5,6)$ give $a\times b=(-3,6,-3)$, and both checks vanish, $a^\top(a\times b)=-3+12-9=0$ and $b^\top(a\times b)=-12+30-18=0$; for the axes, $x\times y=z$, $y\times z=x$ and $z\times x=y$. Non-example: associativity fails, since $(x\times x)\times y=0$ while $x\times(x\times y)=x\times z=-y$. **Why it matters here:** for a matrix with orthonormal columns $r_1,r_2,r_3$, $\det R=(r_1\times r_2)^\top r_3$, which is $+1$ exactly when $r_3=r_1\times r_2$. That is the right-handedness test the picture writes as $x_b\times y_b=+z_b$. The same product builds the third column of the 6D representation (§2), and $[\cdot]_\times$ carries Rodrigues' formula (§2) and angular velocity (§4).

> [!note]- Deeper · 더 깊이
> **The group axioms, each named.** A **group** is a set with an operation satisfying four conditions. (1) **Closure**: combining two elements gives an element, $R_1,R_2\in SO(3)\Rightarrow R_1R_2\in SO(3)$, because $(R_1R_2)^\top R_1R_2=R_2^\top R_2=I$ and $\det(R_1R_2)=1\cdot1$. (2) **Associativity**: $(R_1R_2)R_3=R_1(R_2R_3)$, inherited from matrix multiplication. (3) **Identity**: $I$ is a rotation and $IR=RI=R$. (4) **Inverse**: $R^{-1}=R^\top$ is again a rotation. Commutativity is *not* an axiom, which is why the order result above is possible. **Non-example:** the set of rotations about $x$ by angles in $[0°,90°]$ is not a group: $60°$ followed by $60°$ gives $120°$, outside the set, so closure fails.

### 2. The four ways papers write rotations

The same orientation can be stored in four ways, and the choice decides what goes wrong: a logged yaw can jump from $179^\circ$ to $-179^\circ$ while the gripper barely turns, and a network regressing that angle is punished for a correct answer. The table and the definitions below say what each representation stores and where it breaks. Two habits follow. When a logged angle jumps while the object moves smoothly, check the wrapping and the rotation order before you diagnose a mechanical jump; and in a learning target, tell a discontinuity of the coordinates from a discontinuity of the motion — a representation changes the coordinates, never the physical orientation.

| Representation | Numbers | Strengths | The catch |
|---|---|---|---|
| Rotation matrix | 9 | composition, no singularities | redundant (6 constraints) |
| Euler angles (roll-pitch-yaw) | 3 | human-readable | **gimbal lock**; order conventions bite |
| Axis-angle $(\hat\omega, \theta)$ | 3 | minimal, geometric | composition is awkward |
| **Quaternion** $(w, x, y, z)$ | 4 | no singularities, cheap composition, interpolation (slerp) | double cover: $q$ and $-q$ are the same rotation |

- Learning-specific fact worth knowing: if a regression target must be globally single-valued
  and continuous in a Euclidean output space, low-dimensional coordinates for $SO(3)$ face
  topological obstructions — the same reason every flat world map must cut the globe
  somewhere (longitude jumps from 180° to −180°): some pair of nearby rotations always gets
  far-apart coordinates. Many robot-learning papers therefore use a **6D representation**
  (first two columns of $R$, then Gram-Schmidt) to avoid the relevant discontinuities.
  - **6D representation, stated completely** (Zhou et al., CVPR 2019). The network outputs two unconstrained 3-vectors $a_1,a_2$, and three steps turn them into a rotation: normalise the first, remove from the second its component along the first and normalise, then complete the frame with the cross product.
    $$b_1=\frac{a_1}{\lVert a_1\rVert},\qquad b_2=\frac{a_2-(b_1^\top a_2)\,b_1}{\lVert a_2-(b_1^\top a_2)\,b_1\rVert},\qquad b_3=b_1\times b_2,\qquad R=[\,b_1\ b_2\ b_3\,]$$
    so the columns are unit length, mutually perpendicular and right-handed by construction, and small changes in $(a_1,a_2)$ give small changes in $R$. Example: $a_1=(1,1,0)$, $a_2=(0,1,0)$ give $b_1=(0.707,\,0.707,\,0)$; removing the overlap leaves $(-0.5,\,0.5,\,0)$, so $b_2=(-0.707,\,0.707,\,0)$ and $b_3=(0,0,1)$. That $R$ is exactly $R_z(45°)$. The map fails only when $a_1=0$ or $a_2$ is parallel to $a_1$.

**The three minimal-or-compact representations, each defined with its formula.**
- **Euler angles (roll-pitch-yaw).** Three angles for a fixed, ordered product of elementary rotations. The common ZYX convention, with yaw $\psi$, pitch $\theta$ and roll $\phi$, is
  $$R=R_z(\psi)\,R_y(\theta)\,R_x(\phi)$$
  so the definition has three parts: the three angles, the three axes, and their order. Read left to right it is yaw, then pitch about the *new* $y$, then roll about the *newest* $x$ (intrinsic); read right to left it is roll, pitch, yaw about the *fixed* world axes (extrinsic). Both readings give the same matrix, which is why papers must say which convention they use. Gimbal lock is what happens when the middle rotation reaches $\pm90^\circ$ (pitch, for roll-pitch-yaw): the first and third rotation axes line up, so two of the three angles turn about the same axis and one direction of rotation has no angle left to describe it — a property of the Euler coordinates, not a physical loss of the object's ability to turn. **Gimbal lock, with numbers:** at $\theta=90°$ the product depends only on $\psi-\phi$. $(\psi,\theta,\phi)=(30°,90°,10°)$ and $(50°,90°,30°)$ both give $\begin{pmatrix}0&-0.342&0.940\\0&0.940&0.342\\-1&0&0\end{pmatrix}$, so one of the three angles has stopped doing anything.
- **Axis-angle.** A unit axis $\hat\omega$ and an angle $\theta$, often stored as the **rotation vector** $r=\theta\hat\omega$ (three numbers). The matrix is given by Rodrigues' formula,
  $$R=I+\sin\theta\,[\hat\omega]_\times+(1-\cos\theta)\,[\hat\omega]_\times^2$$
  where $[\hat\omega]_\times$ is the skew-symmetric matrix of §1, so the rotation is built from the identity plus two terms that act only perpendicular to the axis. Example: $\hat\omega=(0,0,1)$, $\theta=90°$ gives exactly $R_z(90°)$. It is derived in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §2]].
- **Unit quaternion.** Four numbers $q=(w,x,y,z)$ with one constraint, $w^2+x^2+y^2+z^2=1$. The rotation by $\theta$ about $\hat\omega$ is
  $$q=\big(\cos\tfrac{\theta}{2},\ \sin\tfrac{\theta}{2}\,\hat\omega\big)$$
  and it acts on a vector $v$ by the quaternion product $q\otimes(0,v)\otimes q^{*}$ (the Hamilton product $\otimes$, stated in full in the next item), where $q^{*}=(w,-x,-y,-z)$ is the conjugate; composing rotations is multiplying quaternions. The half angle is the source of the **double cover**: $\theta+360°$ describes the same rotation but gives $-q$. Example: $R_z(90°)$ is $q=(0.707,\,0,\,0,\,0.707)$, and both $q$ and $-q$ send $(1,0,0)$ to $(0,1,0)$, although $\lVert q-(-q)\rVert=2$. The correct rotation distance ignores the sign: $\text{angle}(q_1,q_2)=2\arccos\lvert q_1^\top q_2\rvert$, which for the identity $(1,0,0,0)$ and this $q$ is $2\arccos0.707=90°$. Converting a rotation matrix to a quaternion has its own trap: the textbook formula divides by $4w$, which vanishes near $180^\circ$, and [[02-foundations/algorithms/robotics-ai-problems|11.8 §8]] codes the stable version.
  - **The quaternion (Hamilton) product, stated completely.** Write a quaternion as a scalar and a 3-vector, $q=(w,\mathbf{v})$, meaning $w+xi+yj+zk$ with Hamilton's rules $i^2=j^2=k^2=ijk=-1$ (so $ij=k=-ji$, $jk=i=-kj$, $ki=j=-ik$). Multiplying two of them out and collecting terms gives
    $$q_1\otimes q_2=\big(w_1w_2-\mathbf{v}_1^\top\mathbf{v}_2,\ \ w_1\mathbf{v}_2+w_2\mathbf{v}_1+\mathbf{v}_1\times\mathbf{v}_2\big)$$
    with the cross product of §1 in the vector part. In components the scalar part is $w_1w_2-x_1x_2-y_1y_2-z_1z_2$ and the $x$ part is $w_1x_2+x_1w_2+y_1z_2-z_1y_2$; the $y$ and $z$ parts follow by cycling $x\to y\to z\to x$. Its conditions: it is associative, the product of two unit quaternions is again a unit quaternion, and it is **not commutative**, because the cross-product term changes sign when the factors swap. $q_1\otimes q_2$ is the rotation $q_2$ followed by $q_1$, matching $R(q_1)R(q_2)$. Worked, on the example above with $q=(c,0,0,s)$, $c=s=0.707$ and $v=(1,0,0)$: first $q\otimes(0,v)=\big(-(0,0,s)^\top(1,0,0),\ c\,(1,0,0)+(0,0,s)\times(1,0,0)\big)=(0,\ c,\ s,\ 0)$; then multiplying by $q^{*}=(c,0,0,-s)$ gives $(0,\ c^2-s^2,\ 2cs,\ 0)=(0,\ 0,\ 1,\ 0)$, the vector $(0,1,0)$. With $-q$ both outer factors flip sign and the two signs cancel, which is the double cover in one line. Composition: $q\otimes q=(c^2-s^2,\ 0,\ 0,\ 2cs)=(0,0,0,1)$, the $180°$ turn about $z$. Non-example: the entry-by-entry product $(c^2,0,0,s^2)=(0.5,0,0,0.5)$ has norm $0.707$, so it is not even a unit quaternion. Order matters exactly as in §1: $R_z$ first, then $R_x$, is $q_x\otimes q_z=(0.5,\ 0.5,\ -0.5,\ 0.5)$ with $q_x=(c,s,0,0)$, and it sends $(1,0,0)$ to $(0,0,1)$, while $q_z\otimes q_x=(0.5,\ 0.5,\ 0.5,\ 0.5)$ sends it to $(0,1,0)$.
- **Slerp** (spherical linear interpolation). Between unit quaternions $q_0,q_1$ with $\cos\Omega=q_0^\top q_1$, for $t\in[0,1]$:
  $$\text{slerp}(q_0,q_1;t)=\frac{\sin\big((1-t)\Omega\big)}{\sin\Omega}\,q_0+\frac{\sin(t\Omega)}{\sin\Omega}\,q_1$$
  so the result stays on the unit sphere and the rotation angle grows at constant rate. Example: from the identity to $R_z(90°)$ ($\Omega=45°$) at $t=0.5$ it gives $(0.924,\,0,\,0,\,0.383)$, which is $R_z(45°)$. The plain average $(0.854,\,0,\,0,\,0.354)$ has norm $0.924$, so it is not a unit quaternion until renormalised. (Flip $q_1$ to $-q_1$ first if $q_0^\top q_1<0$, so the interpolation takes the short way round.)

### 3. Poses: SE(3) and homogeneous transforms

A robot chains poses all day — the panel seen by the camera, the camera bolted to the base, the base parked on the site — and the step people forget when they chain two poses by hand is rotating an offset into the frame it is added in. A pose written as one $4\times4$ matrix makes that rotation happen every time you multiply, which is the whole reason poses are written this way rather than as an $(R,p)$ pair combined by hand; the worked composition below prices the forgotten rotation at $1.41\,\mathrm m$.

- A **pose** = rotation + position, packaged as
  $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$ (a $4\times4$ matrix).
- Composition is matrix multiplication: $T_{AC} = T_{AB}\,T_{BC}$ — read subscripts like
  units and they cancel. Inverse: $T^{-1} = \begin{pmatrix} R^\top & -R^\top p \\ 0 & 1 \end{pmatrix}$.
  - **The components, each named.** As a set,
    $$SE(3)=\Big\{T=\begin{pmatrix}R&p\\0&1\end{pmatrix} : R\in SO(3),\ p\in\mathbb{R}^3\Big\}$$
    so a pose has exactly three parts: a **rotation block** $R$ that must pass both SO(3) tests of §1, a **translation** $p$ with no constraint, and a fixed **bottom row** $(0,0,0,1)$. "E" is for *Euclidean*: these are the motions that preserve distances and handedness. It is a group, because the product $\begin{pmatrix}R_1&p_1\\0&1\end{pmatrix}\begin{pmatrix}R_2&p_2\\0&1\end{pmatrix}=\begin{pmatrix}R_1R_2&R_1p_2+p_1\\0&1\end{pmatrix}$ is again of this form, $I_4$ is the identity, and the inverse above exists. Non-examples: a $4\times4$ matrix whose upper-left block has $\det=-1$, or whose bottom row is not $(0,0,0,1)$ (that is a projective transform, as in a camera projection).
  - **Homogeneous coordinates.** To let one matrix both rotate and translate, a point $x\in\mathbb{R}^3$ is written with a fourth entry $1$, and a free direction (a velocity, an axis) with a fourth entry $0$:
    $$T\begin{pmatrix}x\\1\end{pmatrix}=\begin{pmatrix}Rx+p\\1\end{pmatrix},\qquad T\begin{pmatrix}d\\0\end{pmatrix}=\begin{pmatrix}Rd\\0\end{pmatrix}$$
    so points are rotated and shifted, while directions are only rotated. With $R=R_z(90°)$, $p=(2,0,0)$: the point $(1,0,0)$ goes to $(2,1,0)$, the direction $(1,0,0)$ goes to $(0,1,0)$. The inverse checks out on the same $T$: $-R^\top p=(0,2,0)$, and $T^{-1}$ sends the point $(2,0,0)$ back to the origin, as it should, since that is where $T$ put the origin.
  - **Worked: $T$ of plant P2.** Catalog pose $\theta=(0^\circ,90^\circ)$, tip at $(1,1)$ ([[02-foundations/lab-plants|0.6]]). The second link is vertical, so the tip $x$-axis is along $+y_s$. Then $R=R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$, $p=(1,1,0)$, and
    $$T=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$
    §4 builds from this same $T$ the $6\times6$ adjoint $\mathrm{Ad}_T$, which rewrites a velocity from tool coordinates into base coordinates, and problem-set item 2 uses it to place a camera on the tool and to turn the tool.
  - **What the subscripts mean.** $T_{AB}$ is the pose of frame $B$ expressed in frame $A$: its $R$ columns are $B$'s axes written in $A$'s coordinates, and its $p$ is $B$'s origin in $A$'s coordinates. Used as a map it converts coordinates, $x_A=T_{AB}\,x_B$, which is why inner subscripts must match to multiply. $T_{world\leftarrow cam}$ below is the same object written with an arrow.
  - **Right or left: a motion in the tool's frame or in the base's.** A motion $\Delta T$ can multiply the current pose from either side, and the side decides the frame in which $\Delta T$'s numbers are read. On the **right**, $T\,\Delta T$ applies $\Delta T$ in the body frame $\{b\}$, because $\Delta T$ acts on body coordinates before $T$ carries them to the base; on the **left**, $\Delta T\,T$ applies it in the space frame $\{s\}$, because it acts on coordinates that $T$ has already turned into base ones. For a pure shift $\Delta T=\mathrm{Trans}(d)$, with rotation $I$ and offset $d$,
    $$T\,\mathrm{Trans}(d)=\begin{pmatrix}R&R\,d+p\\0&1\end{pmatrix},\qquad \mathrm{Trans}(d)\,T=\begin{pmatrix}R&p+d\\0&1\end{pmatrix}$$
    so on the right the shift is first turned by $R$ into the tool's direction, and on the left it is added as it stands. On P2's $T$ with $d=(0.1,0,0)$: $T\,\mathrm{Trans}(d)$ puts the tip at $(1,\ 1.1,\ 0)$, $0.1\,\mathrm m$ along the tool's own $x$-axis, straight up the page, while $\mathrm{Trans}(d)\,T$ puts it at $(1.1,\ 1,\ 0)$, along the base's $x$-axis, to the right. The orientation stays $R$ in both, because a shift turns nothing. A gripper command "move 5 cm along your own $z$" is therefore a right multiplication, and "move 5 cm along the world's $z$" a left one.

- **Worked composition, with numbers.** Let a robot base, frame $B$ (a capital: a new frame, not the body frame $\{b\}$), sit $2$ m along the $x$-axis of the world frame $A$ and be turned
  $90°$ about $z$: $T_{AB}$ has $R = R_z(90°)$ and $p = (2,0,0)$. Let the camera sit $1$ m
  straight up from the base with no extra rotation: $T_{BC}$ has $R = I$, $p = (0,0,1)$.
  Multiplying, the rotation part is $R_z(90°)\,I = R_z(90°)$ and the translation part is
  $R_z(90°)(0,0,1) + (2,0,0) = (0,0,1) + (2,0,0) = (2,0,1)$. So the camera is at
  $(2, 0, 1)$ in world coordinates, still turned $90°$.
  Note *why* the translation worked out that way: $T_{BC}$'s offset was expressed in the
  **base** frame, so it had to be rotated into world before adding. In *this* example the
  rotation happens to change nothing — $(0,0,1)$ lies along the $z$ axis it is being turned
  about — so move the camera to the base's own $x$ axis, $p_{BC} = (1,0,0)$, and the step
  becomes visible: $R_z(90°)(1,0,0) + (2,0,0) = (0,1,0) + (2,0,0) = (2,1,0)$, whereas adding
  the offset *without* rotating gives $(3,0,0)$ — about 1.4 m ($\sqrt 2$) away, in the wrong direction.
  That rotation of the offset is the step the opening of this section warned about, and the matrix product does it for you.

<svg viewBox="0 0 560 270" style="max-width:100%;height:auto" role="img" aria-label="top view to scale: world frame A at the origin, base B at (2,0,0) turned 90 degrees, the camera offset (1,0,0) expressed in B rotated into the world lands the camera at (2,1,0), while adding it unrotated gives (3,0,0), 1.41 m away">
  <defs><marker id="seCmp" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.45"><line x1="60.0" y1="187.0" x2="60.0" y2="193.0"/><line x1="165.0" y1="187.0" x2="165.0" y2="193.0"/><line x1="270.0" y1="187.0" x2="270.0" y2="193.0"/><line x1="375.0" y1="187.0" x2="375.0" y2="193.0"/></g>
  <text x="60.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">0</text>
  <text x="165.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">1</text>
  <text x="270.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">2</text>
  <text x="375.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">3</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.35"><line x1="60.0" y1="190.0" x2="432.8" y2="190.0"/><line x1="60.0" y1="190.0" x2="60.0" y2="27.2"/></g>
  <text x="438.8" y="194.0" font-size="11" fill="currentColor" fill-opacity="0.75">x (m)</text>
  <text x="54.0" y="25.2" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="end">y</text>
  <g stroke="currentColor" stroke-width="2.2" marker-end="url(#seCmp)"><line x1="60.0" y1="190.0" x2="107.2" y2="190.0"/><line x1="60.0" y1="190.0" x2="60.0" y2="142.8"/></g>
  <circle cx="60.0" cy="190.0" r="3.2" fill="currentColor"/>
  <text x="113.2" y="194.0" font-size="12" fill="currentColor">x<tspan dy="3" font-size="10">A</tspan></text>
  <text x="54.0" y="148.0" font-size="12" fill="currentColor" text-anchor="end">y<tspan dy="3" font-size="10">A</tspan></text>
  <g stroke="currentColor" stroke-width="2.2" marker-end="url(#seCmp)"><line x1="270.0" y1="190.0" x2="270.0" y2="142.8"/><line x1="270.0" y1="190.0" x2="222.8" y2="190.0"/></g>
  <circle cx="270.0" cy="190.0" r="3.2" fill="currentColor"/>
  <text x="274.0" y="140.8" font-size="12" fill="currentColor">x<tspan dy="3" font-size="10">B</tspan></text>
  <text x="218.0" y="182.0" font-size="12" fill="currentColor" text-anchor="end">y<tspan dy="3" font-size="10">B</tspan></text>
  <g stroke="currentColor" stroke-width="1.4" marker-end="url(#seCmp)"><line x1="270.0" y1="85.0" x2="270.0" y2="37.8"/><line x1="270.0" y1="85.0" x2="222.8" y2="85.0"/></g>
  <circle cx="270.0" cy="85.0" r="3.2" fill="currentColor"/>
  <text x="274.0" y="35.8" font-size="12" fill="currentColor">x<tspan dy="3" font-size="10">C</tspan></text>
  <text x="202.8" y="89.0" font-size="12" fill="currentColor">y<tspan dy="3" font-size="10">C</tspan></text>
  <line x1="68.4" y1="221.5" x2="261.6" y2="221.5" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3" marker-end="url(#seCmp)"/>
  <text x="165.0" y="238.5" font-size="12" fill="currentColor" text-anchor="middle">T<tspan dy="3" font-size="10">AB</tspan></text>
  <line x1="256.4" y1="183.7" x2="256.4" y2="91.3" stroke="currentColor" stroke-width="1.6" marker-end="url(#seCmp)"/>
  <text x="248.4" y="131.5" font-size="12" fill="currentColor" text-anchor="end">T<tspan dy="3" font-size="10">BC</tspan><tspan dy="-3">: offset (1, 0, 0) in B</tspan></text>
  <text x="248.4" y="147.5" font-size="12" fill="currentColor" text-anchor="end">rotated into A: (0, 1, 0)</text>
  <line x1="276.3" y1="196.3" x2="368.7" y2="196.3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5" stroke-dasharray="2 3" marker-end="url(#seCmp)"/>
  <circle cx="375.0" cy="190.0" r="5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="2 2"/>
  <text x="383.0" y="180.0" font-size="12" fill="currentColor" fill-opacity="0.8">unrotated sum (3, 0, 0)</text>
  <line x1="371.0" y1="186.0" x2="274.0" y2="89.0" stroke="currentColor" stroke-width="1" stroke-dasharray="1 3"/>
  <text x="306.0" y="107.0" font-size="12" fill="currentColor" font-weight="600">√2 = 1.41 m off</text>
  <text x="54.0" y="207.0" font-size="12" fill="currentColor" text-anchor="end">world A</text>
  <text x="282.0" y="222.0" font-size="12" fill="currentColor">base B at (2, 0, 0), turned 90°</text>
  <text x="260.0" y="41.0" font-size="12" fill="currentColor" text-anchor="end">camera C at (2, 1, 0)</text>
  <text x="548" y="262" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="end">top view, to scale: 1 m per tick</text>
  <text x="548" y="22" font-size="12" fill="currentColor" text-anchor="end">T<tspan dy="3" font-size="10">AC</tspan><tspan dx="4" dy="-3">= T</tspan><tspan dy="3" font-size="10">AB</tspan><tspan dx="3" dy="-3">T</tspan><tspan dy="3" font-size="10">BC</tspan><tspan dy="-3">: rotate the offset, then add</tspan></text>
</svg>

The worked composition drawn to scale from above: base $B$ sits at $(2,0,0)$ turned $90^\circ$, so the camera offset $(1,0,0)$, written in $B$'s coordinates, points along the world's $+y$ once $R_z(90^\circ)$ turns it, and the camera lands at $(2,1,0)$. Adding the offset unrotated would put it at $(3,0,0)$, $\sqrt2=1.41\,\mathrm m$ away in the wrong direction — the step the product $T_{AB}\,T_{BC}$ never forgets.

- **Frames discipline** is 90% of not making sign errors: every quantity has a frame
  (world, base, camera, end-effector); write it down. "Where is the camera?" = $T_{world \leftarrow cam}$.

### 4. Velocity and small motions (the on-ramp to Modern Robotics)

A pose says where a frame is; a controller also needs how fast the frame is moving and turning, and that velocity is six numbers whose meaning depends on the frame they are written in — the same spinning tool has a zero linear velocity in one frame and $(1,-1,0)$ in another, as the adjoint example below shows. Finite rotations compose by multiplication and cannot be added entry by entry, but small motions can: the small-rotation approximation at the end of this section is the local linear language in which differentiation, and so every Jacobian, becomes possible.

- Angular velocity $\omega$ is a vector (axis × speed); rigid-body velocity = **twist**
  $(\omega, v)$ — six numbers, and the reason end-effector velocity commands are 6-DoF.
  - **Angular velocity, stated completely.** A vector $\omega\in\mathbb{R}^3$ with two parts: its **direction** is the instantaneous rotation axis, oriented by the right-hand rule (curl the fingers with the motion, the thumb points along $\omega$), and its **magnitude** $\lVert\omega\rVert$ is the turning rate in rad/s. For a body spinning about an axis through the origin, a body point at position $p$ moves with
    $$\dot p=\omega\times p$$
    so points on the axis stay still and speed grows with distance from it. Example: $\omega=(0,0,2)$ rad/s and $p=(1,0,0)$ m give $\dot p=(0,2,0)$ m/s: perpendicular to both the axis and the point's offset.
  - **The skew-symmetric matrix $[\omega]_\times$** is §1's cross-product matrix written for the angular velocity, the $3\times3$ matrix that performs "cross with $\omega$":
    $$[\omega]_\times=\begin{pmatrix}0&-\omega_3&\omega_2\\\omega_3&0&-\omega_1\\-\omega_2&\omega_1&0\end{pmatrix},\qquad [\omega]_\times v=\omega\times v$$
    so it is **skew-symmetric**, $[\omega]_\times^\top=-[\omega]_\times$, with zeros on the diagonal and exactly three free entries, the components of $\omega$. Example: $\omega=(0,0,1)$ gives $[\omega]_\times(1,0,0)=(0,1,0)$, the same as $\omega\times(1,0,0)$. Its sign pattern is developed in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §1]].
  - **Twist, stated completely.** A six-vector $\mathcal{V}=(\omega,v)$ with two parts: the angular velocity $\omega$, and a linear part $v$ that is the velocity of the body point *currently at the frame's origin* (whether or not the body actually occupies that point). Every body point $p$ then moves with
    $$\dot p=v+\omega\times p$$
    because a rigid velocity is the origin point's velocity plus the rotation about it. Example: a joint about the $\hat z$ axis through $q=(1,0,0)$ turning at $\omega=(0,0,1)$ has $v=-\omega\times q=(0,-1,0)$. The point on the axis gets $(0,-1,0)+(0,1,0)=0$ and stays still, as it must; the point $(2,0,0)$ gets $(0,1,0)$. Non-example: reading $v$ as the tool-tip velocity, which is only true when the tip sits at the frame origin. Which origin that is, space or body, is worked through in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §3]], and the two descriptions of one motion in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §4]].
  - **The adjoint map $\mathrm{Ad}_T$, stated completely.** A twist's six numbers depend on the frame they are written in, and the adjoint of a pose $T=(R,p)$ is the $6\times6$ matrix that converts them. If $\mathcal{V}_b=(\omega_b,v_b)$ is a twist written in frame $\{b\}$ and $T=T_{sb}$ is the pose of $\{b\}$ in $\{s\}$, the same motion written in $\{s\}$ is
    $$\mathcal{V}_s=\mathrm{Ad}_T\,\mathcal{V}_b,\qquad \mathrm{Ad}_T=\begin{pmatrix}R&0\\ {[p]_\times}R&R\end{pmatrix}$$
    and three steps give it. A body point at $x_b$ in $\{b\}$ sits at $x_s=Rx_b+p$ in $\{s\}$, and its velocity, being a direction, is only rotated (§3): $\dot x_s=R(v_b+\omega_b\times x_b)$. A rotation preserves the cross product, $R(a\times b)=(Ra)\times(Rb)$, so $\dot x_s=Rv_b+(R\omega_b)\times(x_s-p)$. Rearranged, $\dot x_s=\big(Rv_b+p\times R\omega_b\big)+(R\omega_b)\times x_s$, which has the twist form $v_s+\omega_s\times x_s$ with $\omega_s=R\omega_b$ and $v_s=Rv_b+[p]_\times R\,\omega_b$. Its conditions: it is linear, it is invertible with $\mathrm{Ad}_T^{-1}=\mathrm{Ad}_{T^{-1}}$, and it composes like the poses, $\mathrm{Ad}_{T_1T_2}=\mathrm{Ad}_{T_1}\mathrm{Ad}_{T_2}$. **Worked on P2's pose** ($R=R_z(90°)$ and $p=(1,1,0)$ from §3): $[p]_\times R=\begin{pmatrix}0&0&1\\0&0&-1\\1&1&0\end{pmatrix}$. The tool spinning about its own $z$-axis at $1$ rad/s is $\mathcal{V}_b=(0,0,1,\ 0,0,0)$, and $\mathrm{Ad}_T$ turns it into $\mathcal{V}_s=(0,0,1,\ 1,-1,0)$: the same spin, but with a linear part $(1,-1,0)$, because $v_s$ is the velocity of the body point at the *base* origin, $\sqrt2$ from the spin axis, and $\omega\times(0-p)=(1,-1,0)$. The tip itself gets $v_s+\omega_s\times p=(1,-1,0)+(-1,1,0)=0$, as a point on the axis must. Sliding along the tool's $x$-axis at $1$ m/s, $\mathcal{V}_b=(0,0,0,\ 1,0,0)$, becomes $(0,0,0,\ 0,1,0)$: straight up the page, as the picture's $x_b$ arrow says. Non-example: $\mathrm{Ad}_T$ is not $T$ applied to the six numbers, and it is not $\mathrm{diag}(R,R)$. Dropping the $[p]_\times R$ block gives the spin a zero linear part in the base frame, which is the tool-tip misreading of the twist non-example above.
  - **Why it matters: $\mathrm{Ad}_T$ and the Jacobian are different maps.** A manipulator Jacobian $J$ stacks one twist per joint, the twist the body gets when that joint turns at unit speed, so $\mathcal{V}=J\dot\theta$. For P2 at this pose, in base coordinates, joint 1 is the axis through the origin, $(0,0,1,\ 0,0,0)$, and joint 2 is the axis through the elbow $q=(1,0,0)$ worked in the twist item above, $(0,0,1,\ 0,-1,0)$. To write them in the tool frame instead, multiply each column by $\mathrm{Ad}_{T^{-1}}$ ($T^{-1}$ has $R^\top$ and $-R^\top p=(-1,1,0)$, the picture's margin box), which gives $(0,0,1,\ 1,1,0)$ and $(0,0,1,\ 0,1,0)$. So $\mathrm{Ad}$ is a fixed change of coordinates applied to $J$'s columns, while $J$ itself changes with $\theta$. The two views agree on the physics: the tip velocity from the base-frame columns, $v_s+\omega_s\times p$, is $(-1,1,0)$ and $(-1,0,0)$, the catalog's $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$, and $R$ times the tool-frame linear parts $(1,1,0)$ and $(0,1,0)$ gives the same two vectors.
- Small rotation ≈ $I + [\hat\omega\theta]_\times$. Why skew-symmetric? A rotation keeps
  lengths fixed, so $R^\top R = I$; differentiating at $R=I$ gives $\dot R + \dot R^\top = 0$,
  i.e. the generator $\dot R$ *must* be skew — its off-diagonal $\pm$ entries are exactly the
  components of the rotation axis $\omega$ (that is what $[\cdot]_\times$ packs). Rotations are
  thus *locally linear*, which is what lets Jacobians ([[02-foundations/calculus-backprop|2. Calculus]])
  map joint rates to end-effector twists, and what the exponential map formalizes
  ([[04-robotics/modern-robotics-book|MR ch. 3]]).
  - **The approximation, with its error.** For a rotation by a small angle $\theta$ about unit axis $\hat\omega$, keeping the first-order term of Rodrigues' formula (§2) gives
    $$R\approx I+\theta\,[\hat\omega]_\times$$
    since $\sin\theta\approx\theta$ and $1-\cos\theta\approx\theta^2/2$ is dropped. The error is second order in $\theta$. At $\theta=0.01$ rad about $z$ the largest entry error is $5.0\times10^{-5}$, and the approximation fails orthogonality by $\theta^2=10^{-4}$ (the diagonal of $R^\top R-I$). Non-example: at $\theta=90°$ the same formula gives columns of length $1.86$ and $\det=3.47$, nothing like a rotation, which is why the small-angle form is a derivative and not a way to build finite rotations.
  - **Why it matters.** Linearising here is what turns rotation estimation into least squares: an update $R\leftarrow R\,(I+[\delta\omega]_\times)$, or its exact exponential version, has three free numbers, which is how pose-graph and calibration solvers ([[02-foundations/optimization|4. Optimization §3.5]]) parameterise a rotation step.

> [!note]- Deeper · 더 깊이
> **From an axis to $T$, and back — the exponential map of [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].** Four symbols here are defined in that chapter, not on this page: $[S]$ is the $4\times4$ matrix that packs a twist, $e^{[S]\theta}$ the matrix exponential that turns a twist held through a joint angle $\theta$ into a pose, and $\log$ and the *vee* operator undo it.
> Let a revolute joint rotate about an axis parallel to world $z$ through the point
> $q=(1,0,0)$, with $\omega=(0,0,1)$. Its screw axis is
> $S=(\omega,v)$ with $v=-\omega\times q=(0,-1,0)$ — the velocity of the body point currently
> at the origin when the joint turns at unit speed, since that point sits at $-q$ from the axis — and
> $[S]=\begin{pmatrix}[\omega]_\times&v\\0&0\end{pmatrix}$.
> At $\theta=\pi/2$,
> $e^{[S]\theta}=\begin{pmatrix}R_z(90°)&(I-R_z)q\\0&1\end{pmatrix}$,
> whose translation is $(1,-1,0)$. The motion is rotation about a line displaced from the
> origin, not rotation plus an arbitrary translation. Conversely, away from branch
> ambiguities such as rotations near $\pi$, $\log T=[S]\theta$; the vee operator reads its
> six coordinates. This is the exact bridge used by product-of-exponentials (PoE) forward kinematics
> ([[04-robotics/modern-robotics/ch04-forward-kinematics|Forward Kinematics]]) and pose-error inverse kinematics.

**The reading this gives you.** A twist's linear part is the velocity of whichever body point sits at the frame's origin, so its numbers change with the frame and the origin while the physical motion does not: before reading the last three numbers as the tool tip's velocity, find out which frame and which origin they use. A velocity sent without its frame is an incomplete robot interface; [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions]] develops the distinction.

### 5. Where this appears in the wiki

- **VLA action spaces**: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]'s arm action is 7-D = end-effector
  position (3) + rotation (3) + gripper (1), inside an 11-D action that also carries base motion (3) and a mode switch (1); [[01-canonical-papers/notes/4-vla/pi0|π0]] outputs
  joint-space chunks — reading these requires exactly this page. Turning an end-effector
  pose back into joint commands is inverse kinematics
  ([[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]), whose many-solutions
  structure is the classical face of the same multimodality generative policies handle.
- **3D vision**: camera pose in [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]
  is $T \in SE(3)$. Pose estimation is the task of estimating this transform; a method may
  regress a matrix or rotation representation directly, or recover it through correspondences,
  geometric optimization, filtering, or a distributional estimate.
- **Sim & digital twins**: every simulator state and BIM-robot registration is a stack of
  $T$'s ([[05-construction-robotics/index|construction]]).

> [!tip] Going deeper · 더 깊이
> Lynch & Park's [*Modern Robotics*](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (Cambridge, free PDF) ch.3 is the full treatment of everything on this page, and the wiki's own [[04-robotics/modern-robotics/index|MR chapter notes]] are the guided path through it. Read ch.3 rather than a general geometry text: it develops $SO(3)$ and $SE(3)$ in the order a robotics reader needs them, with screws and twists arriving as the answer to a question rather than as machinery. §4 of this page is deliberately the on-ramp to that chapter and stops where it begins.

### Self-check

1. Verify $R(\theta)R(-\theta) = I$ in 2D, and explain why $R^{-1} = R^\top$ in general.
2. Why does regressing Euler angles with MSE misbehave near $\pm180°$? What do quaternions'
   double cover do to naive MSE?
3. Given $T_{base \leftarrow cam}$ and a point $p_{cam}$, write the point in base frame.
4. A gripper command is "move 5 cm along the *gripper's own* z-axis." Is that a left- or
   right-multiplication of the current pose? Why?

> [!tip]- Answers
> 1. Expanding the product gives $\cos^2\theta + \sin^2\theta = 1$ terms → $I$. In general $R$'s columns are orthonormal, so $R^\top R = I \Rightarrow R^{-1} = R^\top$.
> 2. Angle values jump at the $\pm180°$ boundary ($179° \to -179°$, not $-181°$) — neighboring rotations become distant targets and MSE explodes. Quaternions' double cover means $q$ and $-q$ are the same rotation, so a sign-flipped target gives a large loss (wrong gradient) for a correct answer.
> 3. $p_{base} = T_{base \leftarrow cam}\,[p_{cam}; 1]$ (append 1 for homogeneous coordinates, then multiply).
> 4. Right-multiplication $T \cdot \Delta T$ — motion in the body (gripper) frame multiplies on the right; world-frame motion on the left.

### Problem set · 과제

Tier B. **P2** at $\theta=(0^\circ,90^\circ)$, and at the other elbow $\theta=(90^\circ,-90^\circ)$ in items 1 and 3. This page §3–4. Planar, so $R=R_z(\theta_1+\theta_2)$.

1. **Draw.** The picture above for the other elbow, $\theta=(90^\circ,-90^\circ)$: base frame at the origin, elbow at $(0,1)$, and the tip frame at the same point $(1,1)$ with the forearm now horizontal. Label both origins, write $R$ read off the drawing, and mark the point $0.1\,\mathrm{m}$ out along the tool's $x$-axis. What does this tip frame share with the picture above, and what not?
2. **Derive.** (a) At the catalog pose a camera is fixed on the tool, $0.2\,\mathrm m$ along the tool's $y$-axis. Use $T$ to find its position in base coordinates, and say how far off the unrotated sum $p+(0,0.2,0)$ is. (b) The tool then turns $90^\circ$ about its own $z$-axis, $T\,\mathrm{Rot}_z(90^\circ)$, where $\mathrm{Rot}_z(90^\circ)$ is the pose with $R=R_z(90^\circ)$ and no shift. Give the new $R$ and $p$ and the camera's base position. Then multiply the same $\mathrm{Rot}_z(90^\circ)$ on the left instead, and say where the tool and the camera go.
3. **Interpret.** At the other elbow, $\theta=(90^\circ,-90^\circ)$, the elbow sits at $(0,1)$. Write joint 2's twist column in base coordinates and, with $\mathrm{Ad}_{T^{-1}}$, in tool coordinates. Which of the two columns differs from the catalog pose's (§4), and why? What does that say about $\mathrm{Ad}$ against $J$?

> [!note]- How to draw it · 그리는 법
> - The base frame at the origin as a right-handed triad: $x_s$ along $+x$, $y_s$ along $+y$, and $z_s$ out of the page drawn as a circled dot, so the page carries three axes and not two arrows.
> - The arm only faintly, elbow $(0,1)$ and tip $(1,1)$: the object is the frames, and the links are scaffolding.
> - The tip frame, with the forearm along $+x_s$: $x_b$ along $+x_s$, $y_b$ along $+y_s$, $z_b$ out of the page. This time the tip axes *are* parallel to the base axes, and correctly so, because $\theta_1+\theta_2=0$; in the picture above the same drawing would have lost the whole of $R$.
> - $R$ read off the drawing rather than computed: each column is one tip axis in base coordinates, $x_b=(1,0,0)$, $y_b=(0,1,0)$, $z_b=(0,0,1)$, so $R=I$. Check it against §1's two tests: orthonormal columns and $x_b\times y_b=z_b$.
> - The arrow from base origin to tip origin labelled $p=(1,1,0)$, the picture's own $p$, and $T$ with $R$ in the corner, $p$ in the last column and the bottom row $(0,0,0,1)$ written in.
> - A dot $0.1\,\mathrm{m}$ out along the *tool's* $x$-axis, at base $(1.1,\ 1,\ 0)$, to the right of the tip this time, beside the tool's $x$-*direction* as a short arrow labelled $(1,0,0)$: the point is rotated *and* shifted, the direction only rotated.
> - The inverse in a margin box: the base origin seen from the tool frame, $-R^\top p=(-1,\ -1,\ 0)$, still $\sqrt2$ from the tip because a rigid motion cannot change a distance.

> [!tip]- Solutions
> 1. Elbow at $(0,1)$, tip at $(1,1)$, with $x_b$ along $+x_s$ and $y_b$ along $+y_s$. Here $\theta_1+\theta_2=0$, so $R=R_z(0)=I$ and the tip axes are parallel to the base axes, correctly, because this forearm points along $+x$. The origin $p=(1,1,0)$ is the picture's; the orientation is not, so $T=\begin{pmatrix}1&0&0&1\\0&1&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$ differs from the picture's only in its $3\times3$ corner. The tool point lands at base $(1.1,\ 1,\ 0)$, to the right of the tip rather than above it, and the base origin seen from the tool is $(-1,\ -1,\ 0)$, still $\sqrt2$ away. A position alone does not fix a pose.
> 2. (a) $T\,(0,\ 0.2,\ 0,\ 1)^\top$: $R\,(0,0.2,0)=(-0.2,0,0)$, plus $p$, gives $(0.8,\ 1,\ 0)$ — $0.2\,\mathrm m$ to the left of the tip, because the tool's $y$-axis points along $-x_s$ in the picture. The unrotated sum $(1,\ 1.2,\ 0)$ is $0.2\sqrt2=0.283\,\mathrm m$ away. (b) On the right: $R=R_z(90^\circ)R_z(90^\circ)=R_z(180^\circ)$ and $p=(1,1,0)$ unchanged — the tool spins in place — and the camera moves to $R_z(180^\circ)(0,0.2,0)+p=(1,\ 0.8,\ 0)$, below the tip. On the left: $R=R_z(180^\circ)$ again, but $p=R_z(90^\circ)(1,1,0)=(-1,\ 1,\ 0)$: the whole tool swings $90^\circ$ about the base's $z$-axis through the base origin, and the camera lands at $(-1,\ 0.8,\ 0)$. The same rotation gives the same final orientation in two different places, because the side of the product says in which frame the rotation's axis is fixed.
> 3. Joint 2 turns about the $\hat z$ axis through the elbow $q=(0,1,0)$, so in base coordinates its column is $(0,0,1,\ -\omega\times q)=(0,0,1,\ 1,0,0)$, against $(0,0,1,\ 0,-1,0)$ at the catalog pose: it changed, because the elbow moved. At this pose $T$ has $R=I$ and $p=(1,1,0)$, so $\mathrm{Ad}_{T^{-1}}$ keeps $\omega$ and adds $(-p)\times\omega=(-1,1,0)$ to the linear part, giving the tool column $(0,0,1,\ 0,1,0)$ — the same as at the catalog pose, because in the tool frame the elbow always sits $1\,\mathrm m$ behind the tip, at $(-1,0,0)$. So $\mathrm{Ad}$ is a change of coordinates at one pose, while $J$, written in base coordinates, changes with $\theta$: its second column here is the tip velocity $v_s+\omega_s\times p=(1,0,0)+(-1,1,0)=(0,1,0)$, against $(-1,0,0)$ at the catalog pose. Changing the velocity frame left-multiplies $J$'s columns by $\mathrm{Ad}$; it does not replace $J$.

### Robotics bridge

This notation is used verbatim throughout the [[04-robotics/modern-robotics/index|Modern Robotics summary]] and the extrinsics of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]]; it becomes operational in [[04-robotics/state-estimation-slam|SLAM and localization]] and the time-indexed TF trees of [[04-robotics/robot-systems-deployment|Robot Systems]].

### Sources

- K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — ch.3 for rotations, homogeneous transforms, twists, the adjoint and the exponential map, and ch.4 for product-of-exponentials kinematics; the authors' [official page](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) and the wiki's [[04-robotics/modern-robotics/index|MR chapter notes]].
- Y. Zhou, C. Barnes, J. Lu, J. Yang and H. Li, "On the Continuity of Rotation Representations in Neural Networks," CVPR 2019 — the 6D representation of §2.
- The numeric examples on this page were computed here from P2's catalog numbers and the poses stated; recompute them rather than trusting them.

## 한국어

*[[02-foundations/linear-algebra|1. 선형대수]] 하나 위에 선다 — RL이나 신호처리에는 빚진 것이 없다. 여기 놓인 이유는 로보틱스 트랙과
VLA(시각–언어–행동 모델: 지시문과 카메라 영상을 로봇의 동작으로 바꾸는 모델) 논문이 다음으로 이것을 요구하기 때문이다: 로봇의 상태와 행동이 실제로 적히는 공간.*

이 위키의 모든 로봇 행동, 카메라 자세, 3D 재구성은 SE(3) — 강체 자세의 공간 — 에 산다.
이 페이지는 VLA 행동 공간과 3D 비전 논문을 읽기 위한 작업 세트다; 완전한 전개(스크류,
지수 좌표)는 [[04-robotics/modern-robotics-book|Modern Robotics 3장]]의 몫이다.

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 SE(3)는 인식, 파지, 모션 계획, 조작 층 밑에 깔린 수학 바닥의 한 부분이다([[physical-ai-map|피지컬 AI 지도]]의 수학 바닥에 이 페이지의 자리가 있다). 카메라 자세도, 파지 자세도, 공구 자세도 모두 SE(3)의 원소이고, "*저 패널을 프레임에 설치해*"에서는 *패널과 프레임을 식별하고*, *파지를 계획하고*, *부재를 옮기는* 세 단계를 받친다. 로봇을 통합할 때 나는 버그의 대부분은 프레임 버그다. 카메라 오프셋을 월드 좌표로 돌려 놓지 않은 채 베이스 위치에 그냥 더하면, 카메라가 실제 자리에서 $1.41\,\mathrm m$ 떨어진 곳에 찍힌다(§3의 합성 계산). 뒤 페이지들은 이 페이지를 절 단위로 가져다 쓴다. [[04-robotics/geometric-perception-calibration|3.5 기하 인식·보정]]은 카메라 외부 파라미터(로봇에 달린 카메라의 자세)를 이 페이지의 §1–§3 위에, [[04-robotics/state-estimation-slam|3. 상태 추정]]은 포즈 그래프(측정으로 서로 이어진 자세들)를 §2–§3 위에, [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장]]은 트위스트와 수반 사상을 §1, §3, §4 위에 세우고, [[04-robotics/grasping|15. 파지]]는 파지 품질 척도에 §1의 외적을, [[05-construction-robotics/assembly-fabrication|4. 로봇 조립·제작]]은 구멍 맞추기에 §4의 작은 회전을 쓴다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 1 [[02-foundations/overview#통과 점검 — 기초는 끝났는가|기초 통과 점검]]의 13번 문제가 이 페이지를 검사하고, 블록 2 로보틱스 공통 트랙부터 줄곧 쓰인다. 이 페이지를 마치면 회전을 만들고 검사하며, 아래 첨자가 약분되도록 $4\times4$ 자세를 합성하고 뒤집고, 속도가 어느 프레임으로 적혔는지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 두 번쯤 든다. **첫 회차:** 이 페이지의 대상과 그림을 본 뒤, §1을 2D 회전, 순서 예제와 그 그림부터 시작해 행렬이 회전인지 확인하는 법과 오른손 좌표계인지 검사하는 외적까지 읽는다. **둘째 회차:** 자세가 행렬곱으로 합성되고 운동을 오른쪽에 곱하느냐 왼쪽에 곱하느냐가 갈리는 §3을 읽고, §2의 표와 §5는 훑어만 본 뒤, 스스로 점검 1, 3, 4번, [[02-foundations/overview#통과 점검 — 기초는 끝났는가|통과 점검]] 13번, 그리고 과제 1번(그리기)을 푼다. §2의 나머지, §4 전체, 접힌 *더 깊이* 메모는 두 번째 읽기로 미루되, §4는 과제 3번 전이나 Modern Robotics에 들어설 때 읽는다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**다. 이 위키가 숫자를 고정해 둔 *장치*(plant, 제어에서 제어 대상인 시스템을 부르는 말) 여섯 가운데 하나로, 길이 $1\,\mathrm m$인 링크 둘로 된 평면 팔이다. 관절각은 $x$축에서 재고, 엘보 각은 첫 링크에 대해 잰다. 카탈로그 자세 $\theta=(0^\circ,90^\circ)$에서 엘보는 $(1,0)$, 말단은 $(1,1)\,\mathrm m$에 있다. 이 페이지는 팔의 질량을 무시하고 팔을 **프레임** 둘로 그린다. 여기서 프레임은 물체에 붙은 좌표계, 곧 원점 하나와 서로 수직인 단위 축 셋(오른손 좌표계)이며, 구조물의 골조를 가리키는 말이 아니다. 두 프레임이 페이지 전체를 끌고 가고, 글자는 Modern Robotics를 따른다. 어깨의 베이스에 고정된 **공간 프레임**(space frame) $\{s\}$와, 말단의 공구에 고정된 **물체 프레임**(body frame) $\{b\}$다. 그러니 $b$는 베이스가 아니라 물체(body)의 b다. §3의 합성 예제는 월드 $A$, 베이스 $B$, 카메라 $C$를 대문자로 더한다.

*범위: 이 페이지는 회전과 그 흔한 표현 네 가지, $4\times4$ 행렬로서의 자세, 강체의 여섯 숫자 속도를 모두 P2 위에서 가르친다. 스크류 이론, 지수 좌표, 일반적인 팔의 순기구학은 가르치지 않으며 그것은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장]]과 [[04-robotics/modern-robotics/ch04-forward-kinematics|MR 4장]]의 몫이고, 카메라 모델은 [[04-robotics/geometric-perception-calibration|3.5 기하 인식·보정]]의 몫이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 490" style="max-width:100%;height:auto" role="img" aria-label="θ = (0°, 90°)의 장치 P2를 프레임 둘로 그린 그림: 원점의 베이스 축, 90° 돌아간 말단 (1, 1)의 도구 축, 위치 화살표 p, 도구 x축으로 0.1 m 나간 점과 도구 x 방향, 그림에서 읽은 행렬 R과 T, 도구에서 본 베이스 원점을 그린 여백 상자">
  <defs><marker id="arSek" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="7" stroke-opacity="0.13" stroke-linecap="round" fill="none"><line x1="80.0" y1="300.0" x2="230.0" y2="300.0"/><line x1="230.0" y1="300.0" x2="230.0" y2="150.0"/></g>
  <circle cx="230.0" cy="300.0" r="4" fill="none" stroke="currentColor" stroke-opacity="0.3"/>
  <text x="240.0" y="320.0" fill="currentColor" opacity="0.6">엘보 (1, 0)</text>
  <line x1="87.0" y1="300.0" x2="155.0" y2="300.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSek)"/>
  <line x1="80.0" y1="293.0" x2="80.0" y2="225.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSek)"/>
  <circle cx="80.0" cy="300.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="80.0" cy="300.0" r="2" fill="currentColor"/>
  <text x="160.0" y="304.0" fill="currentColor" font-size="13">x<tspan dy="3" font-size="11">s</tspan></text>
  <text x="74.0" y="231.0" fill="currentColor" font-size="13" text-anchor="end">y<tspan dy="3" font-size="11">s</tspan></text>
  <text x="70.0" y="320.0" fill="currentColor" font-size="13" text-anchor="end">z<tspan dy="3" font-size="11">s</tspan></text>
  <text x="90.0" y="320.0" fill="currentColor" opacity="0.9">베이스 (0, 0)</text>
  <line x1="230.0" y1="143.0" x2="230.0" y2="75.0" stroke="currentColor" stroke-width="2.4" marker-end="url(#arSek)"/>
  <line x1="223.0" y1="150.0" x2="155.0" y2="150.0" stroke="currentColor" stroke-width="2.4" marker-end="url(#arSek)"/>
  <circle cx="230.0" cy="150.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="230.0" cy="150.0" r="2" fill="currentColor"/>
  <text x="236.0" y="80.0" fill="currentColor" font-size="13">x<tspan dy="3" font-size="11">b</tspan></text>
  <text x="150.0" y="155.0" fill="currentColor" font-size="13" text-anchor="end">y<tspan dy="3" font-size="11">b</tspan></text>
  <text x="240.0" y="170.0" fill="currentColor" font-size="13">z<tspan dy="3" font-size="11">b</tspan></text>
  <text x="240.0" y="185.0" fill="currentColor" opacity="0.9">말단 (1, 1)</text>
  <line x1="86.4" y1="293.6" x2="223.6" y2="156.4" stroke="currentColor" stroke-width="1.4" marker-end="url(#arSek)" stroke-dasharray="6 4" stroke-opacity="0.8"/>
  <text x="150.0" y="262.0" fill="currentColor">p = (1, 1, 0)</text>
  <circle cx="230.0" cy="135.0" r="3.4" fill="currentColor"/>
  <line x1="226.0" y1="132.0" x2="214.0" y2="117.0" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="212.0" y="104.0" fill="currentColor" text-anchor="end">점: 도구 좌표 (0.1, 0, 0)</text>
  <text x="212.0" y="118.0" fill="currentColor" text-anchor="end">= 베이스 (1, 1.1, 0)</text>
  <line x1="258.0" y1="150.0" x2="258.0" y2="112.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSek)"/>
  <text x="266.0" y="126.0" fill="currentColor">방향</text>
  <text x="266.0" y="140.0" fill="currentColor">(0, 1, 0)</text>
  <text x="14.0" y="24.0" fill="currentColor">• 점, 넷째 성분 1: 회전하고 평행이동</text>
  <text x="14.0" y="38.0" fill="currentColor">↑ 방향, 넷째 성분 0: 회전만</text>
  <text x="14.0" y="344.0" fill="currentColor" opacity="0.85">⊙ = 지면 밖으로 나오는 z (오른손 좌표계)</text>
  <text x="346.0" y="300.0" fill="currentColor" font-size="12">s = 공간 프레임, 베이스에 고정</text>
  <text x="346.0" y="316.0" fill="currentColor" font-size="12">b = 물체 프레임, 공구에 고정</text>
  <rect x="340" y="60" width="212" height="192" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="350.0" y="80.0" fill="currentColor">역행렬: 같은 그림을</text>
  <text x="350.0" y="94.0" fill="currentColor" opacity="0.9">거꾸로 읽은 것</text>
  <line x1="500.0" y1="129.0" x2="500.0" y2="105.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSek)"/>
  <line x1="493.0" y1="136.0" x2="469.0" y2="136.0" stroke="currentColor" stroke-width="2.0" marker-end="url(#arSek)"/>
  <circle cx="500.0" cy="136.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="500.0" cy="136.0" r="2" fill="currentColor"/>
  <text x="506.0" y="110.0" fill="currentColor" font-size="13">x<tspan dy="3" font-size="11">b</tspan></text>
  <text x="464.0" y="141.0" fill="currentColor" font-size="13" text-anchor="end">y<tspan dy="3" font-size="11">b</tspan></text>
  <path d="M500.0 136.0 L500.0 186.0 L450.0 186.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="2 3"/>
  <line x1="500.0" y1="136.0" x2="450.0" y2="186.0" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 3"/>
  <circle cx="450.0" cy="186.0" r="3.4" fill="currentColor"/>
  <text x="506.0" y="165.0" fill="currentColor" opacity="0.8">1</text>
  <text x="475.0" y="200.0" fill="currentColor" text-anchor="middle" opacity="0.8">1</text>
  <text x="467.0" y="159.0" fill="currentColor" text-anchor="end">√2</text>
  <text x="442.0" y="190.0" fill="currentColor" text-anchor="end">베이스 원점</text>
  <text x="350.0" y="214.0" fill="currentColor">도구 좌표로 본 베이스 원점:</text>
  <text x="350.0" y="228.0" fill="currentColor">(−1, 1, 0) = −R<tspan dy="-4" font-size="11">T</tspan><tspan dy="4">p,</tspan></text>
  <text x="350.0" y="242.0" fill="currentColor">말단에서 여전히 √2</text>
  <text x="14.0" y="372.0" fill="currentColor">R: 각 열을 말단 축에서 읽는다</text>
  <text x="84.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">x<tspan dy="3" font-size="11">b</tspan></text>
  <text x="114.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">y<tspan dy="3" font-size="11">b</tspan></text>
  <text x="144.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">z<tspan dy="3" font-size="11">b</tspan></text>
  <text x="84.0" y="410.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="114.0" y="410.0" fill="currentColor" font-size="12" text-anchor="middle">−1</text>
  <text x="144.0" y="410.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="84.0" y="426.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="114.0" y="426.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="144.0" y="426.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="84.0" y="442.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="114.0" y="442.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="144.0" y="442.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <path d="M71 398 L66 398 L66 447 L71 447" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M157 398 L162 398 L162 447 L157 447" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="24.0" y="426.0" fill="currentColor" font-size="12">R =</text>
  <text x="172.0" y="426.0" fill="currentColor" font-size="12">= R<tspan dy="3" font-size="11">z</tspan><tspan dy="-3">(90°)</tspan></text>
  <text x="14.0" y="466.0" fill="currentColor">열은 단위 길이, 서로 ⟂: R<tspan dy="-4" font-size="11">T</tspan><tspan dy="4">R = I</tspan></text>
  <text x="14.0" y="480.0" fill="currentColor">x<tspan dy="3" font-size="11">b</tspan><tspan dx="3.3" dy="-3">× y</tspan><tspan dy="3" font-size="11">b</tspan><tspan dx="3.3" dy="-3">= +z</tspan><tspan dy="3" font-size="11">b</tspan><tspan dy="-3">: det R = +1</tspan></text>
  <text x="268.0" y="372.0" fill="currentColor">T: 구석에 R, 마지막 열에 p</text>
  <text x="312.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="338.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">−1</text>
  <text x="364.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="390.0" y="392.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="312.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="338.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="364.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="390.0" y="408.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="312.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="338.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="364.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <text x="390.0" y="424.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="312.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="338.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="364.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">0</text>
  <text x="390.0" y="440.0" fill="currentColor" font-size="12" text-anchor="middle">1</text>
  <path d="M301 380 L296 380 L296 445 L301 445" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M401 380 L406 380 L406 445 L401 445" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="268.0" y="420.0" fill="currentColor" font-size="12">T =</text>
  <rect x="300" y="381" width="77" height="47" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <rect x="378" y="381" width="24" height="47" rx="2" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <rect x="300" y="429" width="102" height="15" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="414.0" y="408.0" fill="currentColor">← p = (1, 1, 0)</text>
  <text x="414.0" y="440.0" fill="currentColor">← 늘 (0, 0, 0, 1)</text>
  <text x="268.0" y="466.0" fill="currentColor" opacity="0.9">아래 행은 장식이 아니다 (§3)</text>
</svg>

$\theta=(0^\circ,90^\circ)$의 **P2**를 팔이 아니라 두 프레임으로 그리면, 물체 프레임 $\{b\}$는 말단 $p=(1,1,0)$에서 $x_b$가 지면 위쪽, $y_b$가 왼쪽을 향하므로 그 축들을 베이스에 있는 공간 프레임 $\{s\}$의 좌표로 읽은 것이 곧 $R=R_z(90^\circ)$의 열이 되고, $T$는 구석에 $R$, 마지막 열에 $p$, 아래에 $(0,0,0,1)$을 담는다. 도구 $x$축을 따라 $0.1\,\mathrm{m}$ 나간 점은 회전되고 평행이동해 베이스 $(1,\ 1.1,\ 0)$에 놓이지만, 도구의 $x$-방향은 회전만 되어 $(0,1,0)$이 된다. 여백 상자는 같은 그림을 거꾸로 읽은 것으로, 베이스 원점은 도구 좌표로 $(-1,\ 1,\ 0)=-R^\top p$에 있고 말단에서 여전히 $\sqrt2$ 떨어져 있다.

### 1. 회전은 규칙 있는 행렬이다

로봇은 모든 부품이 어떻게 돌아가 있는지 말할 수 있어야 한다. 베이스에 대해 공구가, 공구에 대해 카메라가 얼마나 돌아가 있는지다. 그런데 회전은 숫자처럼 더해지지 않는다. 같은 두 회전도 순서를 바꾸면 공구가 다른 곳을 향한다. 이 절은 회전 행렬이 지키는 규칙 둘을 세워, 회전을 만들고 검사하고 둘을 합성할 수 있게 한다. 평면 골조나 트러스를 해석해 본 적이 있다면 이 대상을 이미 만났다. 부재의 국부 좌표축을 구조물의 전체 좌표축으로 옮기는 좌표 변환 행렬이 바로 회전 행렬이다.

- 3D 회전은 $R^\top R = I$이고 $\det R = +1$인 행렬 $R \in \mathbb{R}^{3\times 3}$ —
  이런 행렬 전체의 집합을 **군**(group) SO(3)라고 부른다.
  "군"은 합성에 대해 닫혀 있고 모든 원소에 역원이 있는 집합을 가리키는 대수학 용어다.
  여기서는 회전 × 회전 = 회전이고, 모든 회전은 되돌릴 수 있다는 뜻이다.
  이 단어가 담는 뜻은 그것이 전부이고, 군의 공리 넷은 이 절 끝의 *더 깊이* 메모에 있다.
  - **두 정의 조건, 각각의 이름.** 집합으로 쓰면
    $$SO(3)=\{R\in\mathbb{R}^{3\times3} : R^\top R=I,\ \det R=+1\}$$
    이므로, 행렬은 두 검사를 모두 통과할 때 정확히 여기에 속한다. (1) **직교성** $R^\top R=I$: $(Rx)^\top(Ry)=x^\top R^\top R\,y=x^\top y$이므로 길이와 각도를 보존한다. (2) **방향 보존** $\det R=+1$: 오른손 좌표계를 오른손 좌표계로 유지한다. 직교성만으로도 $\det R=\pm1$이 강제되고, 둘째 조건이 $-1$ 쪽, 곧 반사를 걸러낸다. "S"는 *special*($\det=+1$), "O"는 *orthogonal*(직교), $3$은 차원이다.
  - **반례.** $S=\text{diag}(2,1,1)$은 회전이 아니다. $S^\top S=\text{diag}(4,1,1)\ne I$이고 $x$축을 늘린다.
- 따름정리: 열들은 정규직교 프레임(회전된 x/y/z 축)이다; $R^{-1} = R^\top$(회전 되돌리기는
  공짜); 회전은 곱셈으로 합성되고 **순서가 중요하다** ($R_1 R_2 \ne R_2 R_1$ — 폰을 두 축으로
  순서 바꿔 돌려보면 몸으로 느껴진다).
- 2D 계산 예제: $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$
  — $R(90°)\,(1,0)^\top = (0,1)^\top$ 검산. SO(3) 전체가 이 아이디어를 세 축으로 한 것이다.
- **순서가 중요하다 — 숫자로, 폰 시연을 믿지 않아도 되게.** 두 축 회전을 잡자 — 각각 위의 2D 회전을 그 축에 수직인 평면에 놓은 것이다:
  $$R_z(90°) = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}, \qquad R_x(90°) = \begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$$
  로 두고, 점 $p = (1,0,0)$ — x축의 끝 — 을 따라가 보자.
  - $R_z$를 **먼저**, 그다음 $R_x$: $R_z p = (0,1,0)$, 그리고 $R_x(0,1,0) = (0,0,1)$.
    점이 **z**축 위에 도착한다.
  - $R_x$를 **먼저**, 그다음 $R_z$: $R_x p = (1,0,0)$(x축 *위의* 점은 x축 회전으로 움직이지
    않는다), 그리고 $R_z(1,0,0) = (0,1,0)$. 점이 **y**축 위에 도착한다.

  같은 회전 둘, 전혀 다른 두 위치. 미묘한 일은 하나도 없다: 두 번째 회전은 첫 번째 회전이
  *남겨둔* 자리에 작용한다. 논문의 $R_{world}R_{body}$와 $R_{body}R_{world}$가 서로 다른 운동을
  기술하는 이유이고, 로보틱스의 모든 규약 불일치가 결국 이것인 이유다.

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="점 (1,0,0)을 R_z 다음 R_x로 돌리면 z축에, R_x 다음 R_z로 돌리면 y축에 도착한다">
  <defs><marker id="seOrdk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5" fill="none"><line x1="140.0" y1="132.0" x2="202.4" y2="168.0"/><line x1="140.0" y1="132.0" x2="77.6" y2="168.0"/><line x1="140.0" y1="132.0" x2="140.0" y2="60.0"/></g>
  <g font-size="12" fill="currentColor" fill-opacity="0.8"><text x="210.4" y="180.0">y</text><text x="61.6" y="180.0">x</text><text x="136.0" y="52.0">z</text></g>
  <circle cx="140.0" cy="132.0" r="2.5" fill="currentColor" fill-opacity="0.6"/>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="5 4" marker-end="url(#seOrdk)">
    <path d="M81.6,171.0 Q140.0,197.8 196.4,172.0"/>
    <path d="M204.4,162.0 Q197.0,99.1 143.0,67.0"/>
  </g>
  <circle cx="77.6" cy="168.0" r="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="140.0" cy="60.0" r="4.5" fill="currentColor"/>
  <text x="140.0" y="199.8" font-size="12" fill="currentColor" text-anchor="middle">1: R<tspan dy="3" font-size="10">z</tspan><tspan dy="-3"> (90°)</tspan></text>
  <text x="205.0" y="95.1" font-size="12" fill="currentColor">2: R<tspan dy="3" font-size="10">x</tspan><tspan dy="-3"> (90°)</tspan></text>
  <text x="140.0" y="30" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600"><tspan>R</tspan><tspan dy="3" font-size="10">z</tspan><tspan dx="4" dy="-3">먼저, 그다음 R</tspan><tspan dy="3" font-size="10">x</tspan></text>
  <text x="140.0" y="218" font-size="12" fill="currentColor" text-anchor="middle">(1,0,0) → (0,1,0) → (0,0,1)</text>
  <text x="140.0" y="236" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">z축에 도착</text>
  <g stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5" fill="none"><line x1="400.0" y1="132.0" x2="462.4" y2="168.0"/><line x1="400.0" y1="132.0" x2="337.6" y2="168.0"/><line x1="400.0" y1="132.0" x2="400.0" y2="60.0"/></g>
  <g font-size="12" fill="currentColor" fill-opacity="0.8"><text x="470.4" y="180.0">y</text><text x="321.6" y="180.0">x</text><text x="396.0" y="52.0">z</text></g>
  <circle cx="400.0" cy="132.0" r="2.5" fill="currentColor" fill-opacity="0.6"/>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="5 4" marker-end="url(#seOrdk)">
    <path d="M341.6,171.0 Q400.0,197.8 456.4,172.0"/>
  </g>
  <circle cx="337.6" cy="168.0" r="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="462.4" cy="168.0" r="4.5" fill="currentColor"/>
  <text x="329.6" y="144.0" font-size="12" fill="currentColor" text-anchor="end">1: R<tspan dy="3" font-size="10">x</tspan><tspan dy="-3">(90°)</tspan></text>
  <text x="329.6" y="159.0" font-size="12" fill="currentColor" text-anchor="end">그대로</text>
  <text x="400.0" y="199.8" font-size="12" fill="currentColor" text-anchor="middle">2: R<tspan dy="3" font-size="10">z</tspan><tspan dy="-3"> (90°)</tspan></text>
  <text x="400.0" y="30" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600"><tspan>R</tspan><tspan dy="3" font-size="10">x</tspan><tspan dx="4" dy="-3">먼저, 그다음 R</tspan><tspan dy="3" font-size="10">z</tspan></text>
  <text x="400.0" y="218" font-size="12" fill="currentColor" text-anchor="middle">(1,0,0) → (1,0,0) → (0,1,0)</text>
  <text x="400.0" y="236" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">y축에 도착</text>
</svg>

$x$축의 끝점 $(1,0,0)$에 같은 두 $90^\circ$ 회전을 두 순서로 적용한 그림이다. $R_z$를 먼저 하면 $(0,1,0)$으로 갔다가 $R_x$가 $(0,0,1)$로 들어 올리고, $R_x$를 먼저 하면 점이 $x$축 위에 있어 제자리에 머물다가 $R_z$가 $(0,1,0)$으로 옮긴다. 그래서 $R_xR_z\ne R_zR_x$다.

- **임의 각도의 기본 회전.** 위의 두 행렬은 좌표축 둘레 세 회전의 $\theta=90°$ 경우다.
  $$R_x(\theta)=\begin{pmatrix}1&0&0\\0&c&-s\\0&s&c\end{pmatrix},\quad R_y(\theta)=\begin{pmatrix}c&0&s\\0&1&0\\-s&0&c\end{pmatrix},\quad R_z(\theta)=\begin{pmatrix}c&-s&0\\s&c&0\\0&0&1\end{pmatrix}$$
  $c=\cos\theta$, $s=\sin\theta$이므로, 각 회전은 자기 축을 고정하고 나머지 두 좌표에 2D 회전을 적용한다. $R_y$의 부호가 뒤집혀 보이는 것은 오른손 법칙이 그 평면을 $z$ 다음 $x$ 순서로 잡기 때문이다. 양의 $\theta$는 양의 축 쪽에서 원점을 내려다볼 때 반시계 방향으로 돈다.
- **어떤 행렬이 회전인지 확인하기** — 회전 행렬을 만들 때마다 해야 한다: 열의 길이가 1이고,
  서로 수직이며, $\det = +1$이어야 한다. $R_z(90°)$라면 열이 $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ —
  길이 1 ✓, 서로의 내적이 모두 0 ✓, $\det = +1$ ✓. $\det$가 $-1$이면 **반사**를 만든 것이고,
  로봇을 돌리는 대신 거울에 비춘 셈이다 — 규약 변환에서 실제로 자주 나는 버그다.
- **외적과 그 행렬의 완전한 정의.** 외적은 $\mathbb{R}^3$의 벡터 둘을 받아 셋째 벡터를 돌려주는 연산이고, 3차원에서만 정의된다. $a=(a_1,a_2,a_3)$와 $b=(b_1,b_2,b_3)$에 대해
  $$a\times b=\big(a_2b_3-a_3b_2,\ \ a_3b_1-a_1b_3,\ \ a_1b_2-a_2b_1\big)$$
  이므로 결과에는 정의 성질이 셋 있다. 두 입력 모두에 수직이고($a^\top(a\times b)=b^\top(a\times b)=0$), 길이는 두 벡터 사이 각을 $\varphi$라 할 때 $\lVert a\rVert\lVert b\rVert\sin\varphi$로 둘이 펼치는 평행사변형의 넓이이며, 방향은 오른손 법칙을 따른다(손가락을 $a$에서 $b$ 쪽으로 감으면 엄지가 $a\times b$를 가리킨다). 식에서 규칙 둘이 따라 나온다. 순서를 바꾸면 부호가 바뀌는 **반교환** 연산이어서 $b\times a=-a\times b$, 따라서 $a\times a=0$이고, 결합법칙은 **성립하지 않는다**. 모든 성분이 $b$에 선형이므로 "$a$와 외적"은 행렬이 되고, 그것이 $a$의 **반대칭 행렬** $[a]_\times$다.
  $$[a]_\times=\begin{pmatrix}0&-a_3&a_2\\a_3&0&-a_1\\-a_2&a_1&0\end{pmatrix},\qquad a\times b=[a]_\times b$$
  그래서 $[a]_\times^\top=-[a]_\times$(반대칭의 뜻)이고, 대각이 0이며 자유 성분은 정확히 셋, $a$의 성분이다. 예: $a=(1,2,3)$, $b=(4,5,6)$이면 $a\times b=(-3,6,-3)$이고, 두 검산 $a^\top(a\times b)=-3+12-9=0$과 $b^\top(a\times b)=-12+30-18=0$이 모두 성립한다. 좌표축끼리는 $x\times y=z$, $y\times z=x$, $z\times x=y$다. 반례: 결합법칙은 깨진다. $(x\times x)\times y=0$인데 $x\times(x\times y)=x\times z=-y$다. **여기서 중요한 이유:** 열 $r_1,r_2,r_3$이 정규직교인 행렬에서 $\det R=(r_1\times r_2)^\top r_3$이고, 이 값은 $r_3=r_1\times r_2$일 때 정확히 $+1$이다. 그림이 $x_b\times y_b=+z_b$로 적은 오른손 검사가 이것이다. 같은 곱이 6D 표현의 셋째 열을 만들고(§2), $[\cdot]_\times$가 로드리게스 공식(§2)과 각속도(§4)를 나른다.

> [!note]- 더 깊이 · Deeper
> **군의 공리, 각각의 이름.** **군**은 연산이 붙은 집합으로 네 조건을 만족한다. (1) **닫힘**: 두 원소를 결합하면 원소가 된다, $R_1,R_2\in SO(3)\Rightarrow R_1R_2\in SO(3)$. $(R_1R_2)^\top R_1R_2=R_2^\top R_2=I$이고 $\det(R_1R_2)=1\cdot1$이기 때문이다. (2) **결합법칙**: $(R_1R_2)R_3=R_1(R_2R_3)$, 행렬곱에서 물려받는다. (3) **항등원**: $I$는 회전이고 $IR=RI=R$. (4) **역원**: $R^{-1}=R^\top$도 회전이다. 교환법칙은 공리가 *아니며*, 그래서 위의 순서 결과가 가능하다. **반례:** $x$축 둘레로 $[0°,90°]$ 범위의 각만큼 도는 회전들의 집합은 군이 아니다. $60°$ 다음 $60°$는 집합 밖의 $120°$이므로 닫힘이 깨진다.

### 2. 논문이 회전을 쓰는 네 가지 방법

같은 방향도 네 가지로 저장할 수 있고, 어느 것을 고르느냐가 무엇이 틀어질지를 정한다. 그리퍼는 거의 돌지 않았는데 기록된 yaw가 $179^\circ$에서 $-179^\circ$로 뛸 수 있고, 그 각을 회귀하는 신경망은 옳은 답에 벌점을 받는다. 아래의 표와 정의는 각 표현이 무엇을 저장하고 어디서 깨지는지를 말한다. 거기서 습관 둘이 나온다. 물체는 부드럽게 움직이는데 로그의 각이 튀면, 기계적인 점프를 진단하기 전에 각도 감기(wrapping)와 회전 순서부터 확인한다. 그리고 학습 목표에서는 좌표의 불연속과 운동의 불연속을 구분한다. 표현은 좌표를 바꿀 뿐 물리적 방향은 바꾸지 않는다.

| 표현 | 숫자 | 강점 | 함정 |
|---|---|---|---|
| 회전 행렬 | 9 | 합성 쉬움, 특이점 없음 | 중복 (제약 6개) |
| 오일러 각 (roll-pitch-yaw) | 3 | 사람이 읽기 쉬움 | **짐벌 락**; 순서 규약이 문다 |
| 축-각 $(\hat\omega, \theta)$ | 3 | 최소, 기하적 | 합성이 어색 |
| **쿼터니언** $(w, x, y, z)$ | 4 | 특이점 없음, 싼 합성, 보간(slerp) | 이중 덮개: $q$와 $-q$가 같은 회전 |

- 학습 특화 상식: 유클리드 출력공간에서 전역 단일값·연속 회귀 타깃을 요구하면 $SO(3)$의
  저차원 좌표에는 위상적 장애가 있다 — 평평한 세계지도가 지구를 어딘가에서 잘라야 하는(경도가
  180°에서 −180°로 뛰는) 것과 같은 이유로, 가까운 두 회전이 멀리 떨어진 좌표를 받는 곳이 반드시
  생긴다. 많은 로봇 학습 논문은 관련 불연속을 피하려고
  **6D 표현**($R$의 앞 두 열 + Gram-Schmidt)을 쓴다.
  - **6D 표현의 완전한 정의**(Zhou et al., CVPR 2019). 네트워크가 제약 없는 3차원 벡터 둘 $a_1,a_2$를 내고, 세 단계로 회전을 만든다. 첫째를 정규화하고, 둘째에서 첫째 방향 성분을 빼고 정규화한 뒤, 외적으로 좌표계를 완성한다.
    $$b_1=\frac{a_1}{\lVert a_1\rVert},\qquad b_2=\frac{a_2-(b_1^\top a_2)\,b_1}{\lVert a_2-(b_1^\top a_2)\,b_1\rVert},\qquad b_3=b_1\times b_2,\qquad R=[\,b_1\ b_2\ b_3\,]$$
    그래서 열들이 구성상 단위 길이이고 서로 수직이며 오른손 좌표계이고, $(a_1,a_2)$의 작은 변화가 $R$의 작은 변화를 준다. 예: $a_1=(1,1,0)$, $a_2=(0,1,0)$이면 $b_1=(0.707,\,0.707,\,0)$이고, 겹치는 성분을 빼면 $(-0.5,\,0.5,\,0)$이 남아 $b_2=(-0.707,\,0.707,\,0)$, $b_3=(0,0,1)$이다. 이 $R$은 정확히 $R_z(45°)$다. 이 사상은 $a_1=0$이거나 $a_2$가 $a_1$과 평행할 때만 실패한다.

**최소 또는 간결한 세 표현, 각각의 식과 정의.**
- **오일러 각(roll-pitch-yaw).** 정해진 순서의 기본 회전 곱을 나타내는 각 세 개다. 흔한 ZYX 규약에서 yaw $\psi$, pitch $\theta$, roll $\phi$로
  $$R=R_z(\psi)\,R_y(\theta)\,R_x(\phi)$$
  이므로 정의에는 세 부분이 있다. 세 각, 세 축, 그리고 그 순서다. 왼쪽부터 읽으면 yaw, 그다음 *새* $y$축 둘레 pitch, 그다음 *가장 새로운* $x$축 둘레 roll(내재적)이고, 오른쪽부터 읽으면 *고정된* 월드 축 둘레로 roll, pitch, yaw(외재적)다. 두 독법이 같은 행렬을 주므로 논문은 어느 규약인지 밝혀야 한다. 짐벌 락은 가운데 회전이 $\pm90^\circ$에 이를 때(roll-pitch-yaw라면 pitch) 첫째와 셋째 회전축이 한 줄로 겹쳐, 세 각 중 둘이 같은 축을 돌리게 되고 한 회전 방향을 나타낼 각이 남지 않는 현상이다. 오일러 좌표의 성질이지, 물체가 돌 수 있는 능력을 물리적으로 잃는 것이 아니다. **숫자로 본 짐벌 락:** $\theta=90°$에서 곱은 $\psi-\phi$에만 의존한다. $(\psi,\theta,\phi)=(30°,90°,10°)$와 $(50°,90°,30°)$가 모두 $\begin{pmatrix}0&-0.342&0.940\\0&0.940&0.342\\-1&0&0\end{pmatrix}$를 주므로, 세 각 중 하나는 아무 일도 하지 않게 된다.
- **축-각.** 단위 축 $\hat\omega$와 각 $\theta$이고, 흔히 **회전 벡터** $r=\theta\hat\omega$(숫자 셋)로 저장한다. 행렬은 로드리게스 공식으로 주어진다.
  $$R=I+\sin\theta\,[\hat\omega]_\times+(1-\cos\theta)\,[\hat\omega]_\times^2$$
  $[\hat\omega]_\times$는 §1의 반대칭 행렬이므로, 회전은 항등행렬에 축에 수직인 방향에만 작용하는 두 항을 더해 만들어진다. 예: $\hat\omega=(0,0,1)$, $\theta=90°$이면 정확히 $R_z(90°)$다. 유도는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §2]]에 있다.
- **단위 쿼터니언.** 제약 하나 $w^2+x^2+y^2+z^2=1$이 붙은 숫자 넷 $q=(w,x,y,z)$다. $\hat\omega$ 둘레 $\theta$ 회전은
  $$q=\big(\cos\tfrac{\theta}{2},\ \sin\tfrac{\theta}{2}\,\hat\omega\big)$$
  이고 벡터 $v$에는 쿼터니언 곱 $q\otimes(0,v)\otimes q^{*}$로 작용한다(해밀턴 곱 $\otimes$는 바로 다음 항목에서 완전히 정의한다). $q^{*}=(w,-x,-y,-z)$는 켤레다. 회전 합성은 쿼터니언 곱이다. 반각이 **이중 덮개**의 원인이다. $\theta+360°$는 같은 회전인데 $-q$를 준다. 예: $R_z(90°)$는 $q=(0.707,\,0,\,0,\,0.707)$이고, $q$와 $-q$ 모두 $(1,0,0)$을 $(0,1,0)$으로 보내지만 $\lVert q-(-q)\rVert=2$다. 올바른 회전 거리는 부호를 무시한다. $\text{angle}(q_1,q_2)=2\arccos\lvert q_1^\top q_2\rvert$이고, 항등 $(1,0,0,0)$과 이 $q$ 사이에서는 $2\arccos0.707=90°$다. 회전 행렬을 쿼터니언으로 바꾸는 데도 함정이 있다. 교과서 식은 $4w$로 나누는데 $180^\circ$ 근처에서 이 값이 0으로 가고, [[02-foundations/algorithms/robotics-ai-problems|11.8 §8]]이 안정적인 버전을 코드로 보인다.
  - **쿼터니언(해밀턴) 곱의 완전한 정의.** 쿼터니언을 스칼라와 3차원 벡터로 쓰자, $q=(w,\mathbf{v})$. 곧 $w+xi+yj+zk$이고 해밀턴 규칙 $i^2=j^2=k^2=ijk=-1$을 따른다($ij=k=-ji$, $jk=i=-kj$, $ki=j=-ik$). 둘을 곱해 전개하고 항을 모으면
    $$q_1\otimes q_2=\big(w_1w_2-\mathbf{v}_1^\top\mathbf{v}_2,\ \ w_1\mathbf{v}_2+w_2\mathbf{v}_1+\mathbf{v}_1\times\mathbf{v}_2\big)$$
    이고, 벡터 부분에 §1의 외적이 들어 있다. 성분으로 쓰면 스칼라 부분은 $w_1w_2-x_1x_2-y_1y_2-z_1z_2$, $x$ 부분은 $w_1x_2+x_1w_2+y_1z_2-z_1y_2$이고, $y$와 $z$ 부분은 $x\to y\to z\to x$로 돌려 얻는다. 조건: 결합법칙이 성립하고, 단위 쿼터니언 둘의 곱은 다시 단위 쿼터니언이며, 인수를 맞바꾸면 외적 항의 부호가 바뀌므로 교환법칙은 **성립하지 않는다**. $q_1\otimes q_2$는 $q_2$ 다음 $q_1$을 한 회전으로, $R(q_1)R(q_2)$와 맞는다. 계산: 위 예의 $q=(c,0,0,s)$, $c=s=0.707$, $v=(1,0,0)$에서 먼저 $q\otimes(0,v)=\big(-(0,0,s)^\top(1,0,0),\ c\,(1,0,0)+(0,0,s)\times(1,0,0)\big)=(0,\ c,\ s,\ 0)$이고, 여기에 $q^{*}=(c,0,0,-s)$를 곱하면 $(0,\ c^2-s^2,\ 2cs,\ 0)=(0,\ 0,\ 1,\ 0)$, 곧 벡터 $(0,1,0)$이다. $-q$를 쓰면 바깥 두 인수의 부호가 모두 뒤집혀 서로 상쇄되니, 이것이 이중 덮개를 한 줄로 보인 것이다. 합성: $q\otimes q=(c^2-s^2,\ 0,\ 0,\ 2cs)=(0,0,0,1)$, $z$ 둘레 $180°$ 회전이다. 반례: 성분끼리 곱한 $(c^2,0,0,s^2)=(0.5,0,0,0.5)$는 노름이 $0.707$이라 단위 쿼터니언조차 아니다. 순서는 §1과 똑같이 중요하다. $R_z$ 먼저 그다음 $R_x$는 $q_x=(c,s,0,0)$으로 $q_x\otimes q_z=(0.5,\ 0.5,\ -0.5,\ 0.5)$이고 $(1,0,0)$을 $(0,0,1)$로 보내지만, $q_z\otimes q_x=(0.5,\ 0.5,\ 0.5,\ 0.5)$는 $(0,1,0)$으로 보낸다.
- **slerp**(구면 선형 보간). $\cos\Omega=q_0^\top q_1$인 단위 쿼터니언 $q_0,q_1$ 사이에서 $t\in[0,1]$에 대해
  $$\text{slerp}(q_0,q_1;t)=\frac{\sin\big((1-t)\Omega\big)}{\sin\Omega}\,q_0+\frac{\sin(t\Omega)}{\sin\Omega}\,q_1$$
  그래서 결과가 단위 구면 위에 머물고 회전각이 일정한 속도로 커진다. 예: 항등에서 $R_z(90°)$로($\Omega=45°$) $t=0.5$에서 $(0.924,\,0,\,0,\,0.383)$, 곧 $R_z(45°)$를 준다. 단순 평균 $(0.854,\,0,\,0,\,0.354)$는 노름이 $0.924$라 다시 정규화하기 전까지 단위 쿼터니언이 아니다. ($q_0^\top q_1<0$이면 먼저 $q_1$을 $-q_1$로 뒤집어 짧은 쪽으로 보간한다.)

### 3. 자세: SE(3)와 동차 변환

로봇은 하루 종일 자세를 잇는다. 카메라가 본 패널, 베이스에 볼트로 고정한 카메라, 현장에 세워 둔 베이스다. 두 자세를 손으로 이을 때 사람들이 빼먹는 단계는 오프셋을, 그것을 더할 프레임으로 먼저 돌려 놓는 일이다. 자세를 $4\times4$ 행렬 하나로 쓰면 곱할 때마다 그 회전이 저절로 일어나고, 자세를 손으로 합치는 $(R,p)$ 쌍 대신 이렇게 쓰는 이유가 바로 그것이다. 아래 합성 계산이 빠뜨린 회전의 대가를 $1.41\,\mathrm m$로 매긴다.

- **자세** = 회전 + 위치를 하나로 포장:
  $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$ ($4\times4$ 행렬).
- 합성은 행렬곱: $T_{AC} = T_{AB}\,T_{BC}$ — 아래 첨자를 단위처럼 읽으면 약분된다.
  역: $T^{-1} = \begin{pmatrix} R^\top & -R^\top p \\ 0 & 1 \end{pmatrix}$
  - **구성 요소, 각각의 이름.** 집합으로 쓰면
    $$SE(3)=\Big\{T=\begin{pmatrix}R&p\\0&1\end{pmatrix} : R\in SO(3),\ p\in\mathbb{R}^3\Big\}$$
    이므로 자세는 정확히 세 부분으로 된다. §1의 SO(3) 검사 둘을 통과해야 하는 **회전 블록** $R$, 제약 없는 **병진** $p$, 그리고 고정된 **맨 아래 행** $(0,0,0,1)$. "E"는 *Euclidean*으로, 거리와 좌우 방향을 보존하는 운동이라는 뜻이다. 곱 $\begin{pmatrix}R_1&p_1\\0&1\end{pmatrix}\begin{pmatrix}R_2&p_2\\0&1\end{pmatrix}=\begin{pmatrix}R_1R_2&R_1p_2+p_1\\0&1\end{pmatrix}$이 다시 이 형태이고, $I_4$가 항등원이며, 위의 역이 존재하므로 군이다. 반례: 왼쪽 위 블록의 $\det=-1$인 $4\times4$ 행렬, 또는 맨 아래 행이 $(0,0,0,1)$이 아닌 행렬(카메라 투영 같은 사영 변환이다).
  - **동차 좌표.** 행렬 하나가 회전과 병진을 함께 하도록, 점 $x\in\mathbb{R}^3$에는 넷째 성분 $1$을, 자유 방향(속도, 축)에는 넷째 성분 $0$을 붙인다.
    $$T\begin{pmatrix}x\\1\end{pmatrix}=\begin{pmatrix}Rx+p\\1\end{pmatrix},\qquad T\begin{pmatrix}d\\0\end{pmatrix}=\begin{pmatrix}Rd\\0\end{pmatrix}$$
    그래서 점은 회전하고 이동하지만 방향은 회전만 한다. $R=R_z(90°)$, $p=(2,0,0)$이면 점 $(1,0,0)$은 $(2,1,0)$으로, 방향 $(1,0,0)$은 $(0,1,0)$으로 간다. 같은 $T$로 역도 확인된다. $-R^\top p=(0,2,0)$이고, $T^{-1}$은 점 $(2,0,0)$을 원점으로 되돌린다. $T$가 원점을 그 자리에 놓았으므로 당연하다.
  - **계산: 장치 P2의 $T$.** 카탈로그 자세 $\theta=(0^\circ,90^\circ)$, 말단 $(1,1)$([[02-foundations/lab-plants|0.6]]). 둘째 링크가 수직이므로 말단 $x$축은 $+y_s$. $R=R_z(90^\circ)$, $p=(1,1,0)$,
    $$T=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$
    §4는 바로 이 $T$로, 속도를 도구 좌표에서 베이스 좌표로 다시 쓰는 $6\times6$ 수반 행렬 $\mathrm{Ad}_T$를 만들고, 과제 2번은 이 $T$로 공구에 카메라를 달고 공구를 돌린다.
  - **아래 첨자의 뜻.** $T_{AB}$는 프레임 $A$에서 표현한 프레임 $B$의 자세다. $R$의 열은 $A$ 좌표로 쓴 $B$의 축이고, $p$는 $A$ 좌표로 쓴 $B$의 원점이다. 사상으로 쓰면 좌표를 변환한다, $x_A=T_{AB}\,x_B$. 곱하려면 안쪽 첨자가 맞아야 하는 이유다. 아래의 $T_{world\leftarrow cam}$은 같은 대상을 화살표로 쓴 것이다.
  - **오른쪽이냐 왼쪽이냐: 공구의 프레임에서 한 운동과 베이스의 프레임에서 한 운동.** 운동 $\Delta T$는 현재 자세에 어느 쪽에서든 곱할 수 있고, 곱하는 쪽이 $\Delta T$의 숫자를 어느 프레임으로 읽을지 정한다. **오른쪽**에 곱한 $T\,\Delta T$는 $\Delta T$를 물체 프레임 $\{b\}$에서 적용한다. $T$가 물체 좌표를 베이스 좌표로 옮기기 전에 $\Delta T$가 물체 좌표에 먼저 작용하기 때문이다. **왼쪽**에 곱한 $\Delta T\,T$는 공간 프레임 $\{s\}$에서 적용한다. $T$가 이미 베이스 좌표로 바꿔 놓은 것에 작용하기 때문이다. 회전이 $I$이고 오프셋이 $d$인 순수 이동 $\Delta T=\mathrm{Trans}(d)$라면
    $$T\,\mathrm{Trans}(d)=\begin{pmatrix}R&R\,d+p\\0&1\end{pmatrix},\qquad \mathrm{Trans}(d)\,T=\begin{pmatrix}R&p+d\\0&1\end{pmatrix}$$
    이므로, 오른쪽에서는 이동이 먼저 $R$로 돌려져 공구의 방향이 되고, 왼쪽에서는 그대로 더해진다. P2의 $T$에 $d=(0.1,0,0)$을 쓰면, $T\,\mathrm{Trans}(d)$는 말단을 공구 자신의 $x$축을 따라 $0.1\,\mathrm m$, 곧 지면 위쪽으로 옮겨 $(1,\ 1.1,\ 0)$에 두고, $\mathrm{Trans}(d)\,T$는 베이스의 $x$축을 따라 오른쪽으로 옮겨 $(1.1,\ 1,\ 0)$에 둔다. 이동은 아무것도 돌리지 않으므로 방향은 두 경우 모두 $R$ 그대로다. 그래서 그리퍼 명령 "네 $z$축을 따라 5 cm"는 오른쪽 곱이고, "월드의 $z$축을 따라 5 cm"는 왼쪽 곱이다.

- **합성 계산 예제, 숫자와 함께.** 로봇 베이스, 곧 프레임 $B$(대문자다. 물체 프레임 $\{b\}$가 아닌 새 프레임이다)가 월드 프레임 $A$의 $x$축으로 $2$ m 떨어져 있고 $z$축으로
  $90°$ 돌아가 있다고 하자: $T_{AB}$는 $R = R_z(90°)$, $p = (2,0,0)$. 카메라는 베이스에서
  똑바로 위로 $1$ m, 추가 회전은 없다: $T_{BC}$는 $R = I$, $p = (0,0,1)$.
  곱하면 회전부는 $R_z(90°)\,I = R_z(90°)$이고, 병진부는
  $R_z(90°)(0,0,1) + (2,0,0) = (0,0,1) + (2,0,0) = (2,0,1)$이다. 즉 카메라는 월드 좌표로
  $(2, 0, 1)$에 있고 여전히 $90°$ 돌아가 있다.
  병진이 *왜* 그렇게 나왔는지에 주목하라: $T_{BC}$의 오프셋은 **베이스** 프레임에서 표현된
  것이므로, 더하기 전에 월드로 회전시켜야 했다. 다만 *이* 예제에서는 회전이 아무것도 바꾸지
  않는다 — $(0,0,1)$이 회전축인 $z$와 나란하기 때문이다. 그러니 카메라를 베이스 자신의 $x$
  축으로 옮겨 $p_{BC} = (1,0,0)$으로 두면 그 단계가 눈에 보인다:
  $R_z(90°)(1,0,0) + (2,0,0) = (0,1,0) + (2,0,0) = (2,1,0)$인데, 회전 없이 그냥 더하면
  $(3,0,0)$ — 약 1.4 m($\sqrt 2$) 떨어진, 방향이 틀린 자리다. 이 절의 첫머리가 경고한 단계가 바로 그 오프셋 회전이고, 행렬곱은 그 일을 대신 해 준다.

<svg viewBox="0 0 560 270" style="max-width:100%;height:auto" role="img" aria-label="실제 비율의 위에서 본 그림: 원점의 월드 프레임 A, (2,0,0)에서 90도 돌아간 베이스 B, B 좌표의 카메라 오프셋 (1,0,0)을 월드로 돌리면 카메라는 (2,1,0)에 놓이고 돌리지 않고 더하면 1.41 m 떨어진 (3,0,0)이 된다">
  <defs><marker id="seCmpk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.45"><line x1="60.0" y1="187.0" x2="60.0" y2="193.0"/><line x1="165.0" y1="187.0" x2="165.0" y2="193.0"/><line x1="270.0" y1="187.0" x2="270.0" y2="193.0"/><line x1="375.0" y1="187.0" x2="375.0" y2="193.0"/></g>
  <text x="60.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">0</text>
  <text x="165.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">1</text>
  <text x="270.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">2</text>
  <text x="375.0" y="205.0" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="middle">3</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.35"><line x1="60.0" y1="190.0" x2="432.8" y2="190.0"/><line x1="60.0" y1="190.0" x2="60.0" y2="27.2"/></g>
  <text x="438.8" y="194.0" font-size="11" fill="currentColor" fill-opacity="0.75">x (m)</text>
  <text x="54.0" y="25.2" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="end">y</text>
  <g stroke="currentColor" stroke-width="2.2" marker-end="url(#seCmpk)"><line x1="60.0" y1="190.0" x2="107.2" y2="190.0"/><line x1="60.0" y1="190.0" x2="60.0" y2="142.8"/></g>
  <circle cx="60.0" cy="190.0" r="3.2" fill="currentColor"/>
  <text x="113.2" y="194.0" font-size="12" fill="currentColor">x<tspan dy="3" font-size="10">A</tspan></text>
  <text x="54.0" y="148.0" font-size="12" fill="currentColor" text-anchor="end">y<tspan dy="3" font-size="10">A</tspan></text>
  <g stroke="currentColor" stroke-width="2.2" marker-end="url(#seCmpk)"><line x1="270.0" y1="190.0" x2="270.0" y2="142.8"/><line x1="270.0" y1="190.0" x2="222.8" y2="190.0"/></g>
  <circle cx="270.0" cy="190.0" r="3.2" fill="currentColor"/>
  <text x="274.0" y="140.8" font-size="12" fill="currentColor">x<tspan dy="3" font-size="10">B</tspan></text>
  <text x="218.0" y="182.0" font-size="12" fill="currentColor" text-anchor="end">y<tspan dy="3" font-size="10">B</tspan></text>
  <g stroke="currentColor" stroke-width="1.4" marker-end="url(#seCmpk)"><line x1="270.0" y1="85.0" x2="270.0" y2="37.8"/><line x1="270.0" y1="85.0" x2="222.8" y2="85.0"/></g>
  <circle cx="270.0" cy="85.0" r="3.2" fill="currentColor"/>
  <text x="274.0" y="35.8" font-size="12" fill="currentColor">x<tspan dy="3" font-size="10">C</tspan></text>
  <text x="202.8" y="89.0" font-size="12" fill="currentColor">y<tspan dy="3" font-size="10">C</tspan></text>
  <line x1="68.4" y1="221.5" x2="261.6" y2="221.5" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3" marker-end="url(#seCmpk)"/>
  <text x="165.0" y="238.5" font-size="12" fill="currentColor" text-anchor="middle">T<tspan dy="3" font-size="10">AB</tspan></text>
  <line x1="256.4" y1="183.7" x2="256.4" y2="91.3" stroke="currentColor" stroke-width="1.6" marker-end="url(#seCmpk)"/>
  <text x="248.4" y="131.5" font-size="12" fill="currentColor" text-anchor="end">T<tspan dy="3" font-size="10">BC</tspan><tspan dy="-3">: B 좌표의 오프셋 (1, 0, 0)</tspan></text>
  <text x="248.4" y="147.5" font-size="12" fill="currentColor" text-anchor="end">A로 돌리면 (0, 1, 0)</text>
  <line x1="276.3" y1="196.3" x2="368.7" y2="196.3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5" stroke-dasharray="2 3" marker-end="url(#seCmpk)"/>
  <circle cx="375.0" cy="190.0" r="5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="2 2"/>
  <text x="383.0" y="180.0" font-size="12" fill="currentColor" fill-opacity="0.8">회전 없는 합 (3, 0, 0)</text>
  <line x1="371.0" y1="186.0" x2="274.0" y2="89.0" stroke="currentColor" stroke-width="1" stroke-dasharray="1 3"/>
  <text x="306.0" y="107.0" font-size="12" fill="currentColor" font-weight="600">√2 = 1.41 m 어긋남</text>
  <text x="54.0" y="207.0" font-size="12" fill="currentColor" text-anchor="end">월드 A</text>
  <text x="282.0" y="222.0" font-size="12" fill="currentColor">베이스 B: (2, 0, 0), 90° 회전</text>
  <text x="260.0" y="41.0" font-size="12" fill="currentColor" text-anchor="end">카메라 C: (2, 1, 0)</text>
  <text x="548" y="262" font-size="11" fill="currentColor" fill-opacity="0.75" text-anchor="end">위에서 본 그림, 실제 비율: 눈금 한 칸이 1 m</text>
  <text x="548" y="22" font-size="12" fill="currentColor" text-anchor="end">T<tspan dy="3" font-size="10">AC</tspan><tspan dx="4" dy="-3">= T</tspan><tspan dy="3" font-size="10">AB</tspan><tspan dx="3" dy="-3">T</tspan><tspan dy="3" font-size="10">BC</tspan><tspan dy="-3">: 오프셋을 돌린 뒤 더한다</tspan></text>
</svg>

위의 합성 계산을 실제 비율로 위에서 본 그림이다. 베이스 $B$는 $(2,0,0)$에서 $90^\circ$ 돌아가 있으므로, $B$의 좌표로 적은 카메라 오프셋 $(1,0,0)$은 $R_z(90^\circ)$로 돌리면 월드의 $+y$ 방향이 되고 카메라는 $(2,1,0)$에 놓인다. 오프셋을 돌리지 않고 더하면 $\sqrt2=1.41\,\mathrm m$ 떨어진 엉뚱한 방향의 $(3,0,0)$이 되며, 곱 $T_{AB}\,T_{BC}$는 이 단계를 결코 빠뜨리지 않는다.

- **프레임 규율**이 부호 실수 안 하기의 90%다: 모든 양에는 프레임(월드, 베이스, 카메라,
  말단)이 있다; 항상 적어라. "카메라가 어디 있나?" = $T_{world \leftarrow cam}$.

### 4. 속도와 미소 운동 (Modern Robotics로 가는 진입로)

자세는 프레임이 어디 있는지를 말한다. 제어기에는 그 프레임이 얼마나 빨리 움직이고 도는지도 필요한데, 그 속도는 여섯 숫자이고 그 뜻은 어느 프레임으로 적었느냐에 달려 있다. 아래 수반 사상 예제가 보이듯, 같은 회전하는 공구도 한 프레임에서는 선속도가 0이고 다른 프레임에서는 $(1,-1,0)$이다. 유한 회전은 곱으로 합성되며 성분끼리 더할 수 없지만, 작은 운동은 더할 수 있다. 이 절 끝의 미소 회전 근사가 미분, 그리고 모든 야코비안을 가능하게 하는 국소 선형 언어다.

- 각속도 $\omega$는 벡터(축 × 속력); 강체 속도 = **twist** $(\omega, v)$ — 여섯 숫자이고,
  말단 속도 명령이 6자유도인 이유다.
  - **각속도의 완전한 정의.** 두 부분을 가진 벡터 $\omega\in\mathbb{R}^3$다. **방향**은 순간 회전축이고 오른손 법칙으로 향한다(손가락을 운동 방향으로 감으면 엄지가 $\omega$를 가리킨다). **크기** $\lVert\omega\rVert$는 rad/s 단위의 회전 속도다. 원점을 지나는 축 둘레로 도는 물체에서 위치 $p$의 물체 점은
    $$\dot p=\omega\times p$$
    로 움직이므로, 축 위의 점은 가만히 있고 축에서 멀수록 빠르다. 예: $\omega=(0,0,2)$ rad/s, $p=(1,0,0)$ m이면 $\dot p=(0,2,0)$ m/s로, 축과 점의 오프셋 모두에 수직이다.
  - **반대칭 행렬 $[\omega]_\times$.** §1의 외적 행렬을 각속도에 대해 쓴 것으로, "$\omega$와 외적"을 수행하는 $3\times3$ 행렬이다.
    $$[\omega]_\times=\begin{pmatrix}0&-\omega_3&\omega_2\\\omega_3&0&-\omega_1\\-\omega_2&\omega_1&0\end{pmatrix},\qquad [\omega]_\times v=\omega\times v$$
    그래서 **반대칭**, $[\omega]_\times^\top=-[\omega]_\times$이고, 대각이 0이며 자유 성분은 정확히 셋, $\omega$의 성분이다. 예: $\omega=(0,0,1)$이면 $[\omega]_\times(1,0,0)=(0,1,0)$으로 $\omega\times(1,0,0)$과 같다. 부호 패턴은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §1]]에서 전개한다.
  - **트위스트의 완전한 정의.** 두 부분을 가진 6차원 벡터 $\mathcal{V}=(\omega,v)$다. 각속도 $\omega$, 그리고 *지금 프레임 원점에 있는* 물체 점의 속도인 선형 부분 $v$(물체가 실제로 그 점을 차지하든 아니든). 그러면 모든 물체 점 $p$는
    $$\dot p=v+\omega\times p$$
    로 움직인다. 강체 속도는 원점 점의 속도에 그 둘레의 회전을 더한 것이기 때문이다. 예: $q=(1,0,0)$을 지나는 $\hat z$축 둘레로 $\omega=(0,0,1)$로 도는 관절은 $v=-\omega\times q=(0,-1,0)$이다. 축 위의 점은 $(0,-1,0)+(0,1,0)=0$을 받아 당연히 가만히 있고, 점 $(2,0,0)$은 $(0,1,0)$을 받는다. 반례: $v$를 도구 끝 속도로 읽는 것. 끝이 프레임 원점에 있을 때만 참이다. 그 원점이 공간 원점인지 바디 원점인지는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §3]]에서, 한 운동의 두 기술은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §4]]에서 다룬다.
  - **수반 사상(adjoint map) $\mathrm{Ad}_T$의 완전한 정의.** 트위스트의 여섯 숫자는 어느 프레임으로 쓰느냐에 달려 있고, 자세 $T=(R,p)$의 수반 행렬은 그 숫자들을 변환하는 $6\times6$ 행렬이다. $\mathcal{V}_b=(\omega_b,v_b)$가 프레임 $\{b\}$로 쓴 트위스트이고 $T=T_{sb}$가 $\{s\}$에서 본 $\{b\}$의 자세라면, 같은 운동을 $\{s\}$로 쓴 것은
    $$\mathcal{V}_s=\mathrm{Ad}_T\,\mathcal{V}_b,\qquad \mathrm{Ad}_T=\begin{pmatrix}R&0\\ {[p]_\times}R&R\end{pmatrix}$$
    이고, 세 단계로 나온다. $\{b\}$에서 $x_b$에 있는 물체 점은 $\{s\}$에서 $x_s=Rx_b+p$에 있고, 그 속도는 방향이므로 회전만 된다(§3), $\dot x_s=R(v_b+\omega_b\times x_b)$. 회전은 외적을 보존하므로($R(a\times b)=(Ra)\times(Rb)$) $\dot x_s=Rv_b+(R\omega_b)\times(x_s-p)$다. 정리하면 $\dot x_s=\big(Rv_b+p\times R\omega_b\big)+(R\omega_b)\times x_s$로 트위스트 꼴 $v_s+\omega_s\times x_s$이고, $\omega_s=R\omega_b$, $v_s=Rv_b+[p]_\times R\,\omega_b$다. 조건: 선형이고, 역이 $\mathrm{Ad}_T^{-1}=\mathrm{Ad}_{T^{-1}}$로 존재하며, 자세처럼 합성된다, $\mathrm{Ad}_{T_1T_2}=\mathrm{Ad}_{T_1}\mathrm{Ad}_{T_2}$. **P2의 자세에서 계산**(§3의 $R=R_z(90°)$, $p=(1,1,0)$): $[p]_\times R=\begin{pmatrix}0&0&1\\0&0&-1\\1&1&0\end{pmatrix}$. 도구가 자기 $z$축 둘레로 $1$ rad/s로 도는 $\mathcal{V}_b=(0,0,1,\ 0,0,0)$에 $\mathrm{Ad}_T$를 곱하면 $\mathcal{V}_s=(0,0,1,\ 1,-1,0)$이다. 회전은 같은데 선형 부분이 $(1,-1,0)$인 것은, $v_s$가 회전축에서 $\sqrt2$ 떨어진 *베이스* 원점에 있는 물체 점의 속도이고 $\omega\times(0-p)=(1,-1,0)$이기 때문이다. 말단 자신은 $v_s+\omega_s\times p=(1,-1,0)+(-1,1,0)=0$을 받는다. 축 위의 점이니 당연하다. 도구 $x$축을 따라 $1$ m/s로 미끄러지는 $\mathcal{V}_b=(0,0,0,\ 1,0,0)$은 $(0,0,0,\ 0,1,0)$, 곧 그림의 $x_b$ 화살표대로 지면 위쪽이 된다. 반례: $\mathrm{Ad}_T$는 여섯 숫자에 $T$를 적용한 것이 아니고, $\mathrm{diag}(R,R)$도 아니다. $[p]_\times R$ 블록을 빼면 회전의 베이스 프레임 선형 부분이 0이 되는데, 이것이 위 트위스트 반례의 도구 끝 속도 오독이다.
  - **중요한 이유: $\mathrm{Ad}_T$와 야코비안은 다른 사상이다.** 매니퓰레이터 야코비안 $J$는 관절마다 트위스트 하나, 곧 그 관절이 단위 속도로 돌 때 물체가 받는 트위스트를 쌓은 것이라 $\mathcal{V}=J\dot\theta$다. 이 자세의 P2를 베이스 좌표로 쓰면 관절 1은 원점을 지나는 축 $(0,0,1,\ 0,0,0)$이고, 관절 2는 위 트위스트 항목에서 계산한 엘보 $q=(1,0,0)$을 지나는 축 $(0,0,1,\ 0,-1,0)$이다. 이것을 도구 프레임으로 쓰려면 각 열에 $\mathrm{Ad}_{T^{-1}}$을 곱한다($T^{-1}$은 $R^\top$과 $-R^\top p=(-1,1,0)$, 곧 그림의 여백 상자다). 결과는 $(0,0,1,\ 1,1,0)$과 $(0,0,1,\ 0,1,0)$이다. 그러니 $\mathrm{Ad}$는 $J$의 열에 적용하는 고정된 좌표 변환이고, $J$ 자체는 $\theta$에 따라 바뀐다. 두 관점은 물리에서 일치한다. 베이스 프레임 열로 구한 말단 속도 $v_s+\omega_s\times p$는 $(-1,1,0)$과 $(-1,0,0)$, 곧 카탈로그의 $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$이고, 도구 프레임 선형 부분 $(1,1,0)$과 $(0,1,0)$에 $R$을 곱해도 같은 두 벡터가 나온다.
- 미소 회전 ≈ $I + [\hat\omega\theta]_\times$. 왜 반대칭인가? 회전은 길이를 보존하므로
  $R^\top R = I$; $R=I$에서 미분하면 $\dot R + \dot R^\top = 0$, 즉 생성원 $\dot R$는 *반드시*
  반대칭이고, 그 비대각 $\pm$ 성분이 정확히 회전축 $\omega$의 성분이다($[\cdot]_\times$가
  담는 것). 그래서 회전은 *국소적으로 선형*이고,
  이것이 야코비안([[02-foundations/calculus-backprop|2. 미적분]])이 관절 속도를 말단
  twist로 사상할 수 있는 이유이자, 지수 사상이 정식화하는 내용이다
  ([[04-robotics/modern-robotics-book|MR 3장]]).
  - **근사와 그 오차.** 단위 축 $\hat\omega$ 둘레 작은 각 $\theta$의 회전에서 로드리게스 공식(§2)의 1차 항만 남기면
    $$R\approx I+\theta\,[\hat\omega]_\times$$
    $\sin\theta\approx\theta$이고 $1-\cos\theta\approx\theta^2/2$를 버리기 때문이다. 오차는 $\theta$에 대해 2차다. $z$축 둘레 $\theta=0.01$ rad에서 성분 오차의 최대는 $5.0\times10^{-5}$이고, 근사는 직교성을 $\theta^2=10^{-4}$만큼 어긴다($R^\top R-I$의 대각). 반례: $\theta=90°$에서 같은 식은 열 길이 $1.86$, $\det=3.47$을 주어 회전과 전혀 닮지 않았다. 작은 각 형태가 유한 회전을 만드는 방법이 아니라 미분인 이유다.
  - **중요한 이유.** 여기서 선형화하는 것이 회전 추정을 최소자승으로 바꾼다. 갱신 $R\leftarrow R\,(I+[\delta\omega]_\times)$, 또는 그 정확한 지수 판본은 자유 숫자가 셋이고, 포즈그래프·보정 솔버([[02-foundations/optimization|4. 최적화 §3.5]])가 회전 스텝을 매개화하는 방식이 이것이다.

> [!note]- 더 깊이 · Deeper
> **축에서 $T$로, 다시 축으로 — [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장]]의 지수 사상.** 여기 나오는 기호 넷은 이 페이지가 아니라 그 장에서 정의한다. $[S]$는 트위스트를 담는 $4\times4$ 행렬, $e^{[S]\theta}$는 관절각 $\theta$만큼 유지한 트위스트를 자세로 바꾸는 행렬 지수이고, $\log$와 *vee* 연산은 그것을 되돌린다.
> 월드 $z$축과 평행하고 $q=(1,0,0)$을 지나는 회전 관절을 잡자.
> $\omega=(0,0,1)$이면 screw axis는 $S=(\omega,v)$,
> $v=-\omega\times q=(0,-1,0)$이고(관절이 단위 속도로 돌 때 지금 원점에 있는 물체 점의 속도다 —
> 그 점은 축에서 $-q$만큼 떨어져 있으므로)
> $[S]=\begin{pmatrix}[\omega]_\times&v\\0&0\end{pmatrix}$다.
> $\theta=\pi/2$에서
> $e^{[S]\theta}=\begin{pmatrix}R_z(90°)&(I-R_z)q\\0&1\end{pmatrix}$이고 병진은
> $(1,-1,0)$이다. 원점에서 벗어난 선 둘레의 회전이지, 회전과 임의 병진을 따로 붙인 것이 아니다.
> 반대로 $\pi$ 근처 회전 같은 branch 모호성을 피하면 $\log T=[S]\theta$이고 vee 연산이 여섯
> 좌표를 읽는다. 이것이 지수 곱(PoE, product of exponentials) 순기구학
> ([[04-robotics/modern-robotics/ch04-forward-kinematics|순기구학]])과 자세 오차로 푸는 역기구학이 쓰는 정확한 다리다.

**여기서 얻는 독법.** 트위스트의 선형 부분은 프레임 원점에 있는 물체 점의 속도이므로, 그 숫자는 프레임과 원점에 따라 바뀌어도 물리적 운동은 바뀌지 않는다. 뒤쪽 세 숫자를 도구 끝의 속도로 읽기 전에 어느 프레임, 어느 원점으로 적었는지 확인한다. 프레임 없이 보낸 속도는 불완전한 로봇 인터페이스이고, 그 구분은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동]]에서 전개한다.

### 5. 이 위키에서 등장하는 곳

- **VLA 행동 공간**: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]의 팔 행동은 7차원 = 말단 위치(3) +
  회전(3) + 그리퍼(1)이고, 이것은 베이스 이동(3)과 모드 전환(1)까지 담은 11차원 행동의 일부다; [[01-canonical-papers/notes/4-vla/pi0|π0]]는 관절 공간 청크를 출력 —
  이들을 읽는 데 정확히 이 페이지가 필요하다. 말단 pose를 다시 관절 명령으로 바꾸는 것이
  [[04-robotics/modern-robotics/ch06-inverse-kinematics|역기구학(MR 6장)]]이고, 그 다해(多解)
  구조가 생성형 정책이 다루는 바로 그 다봉성의 고전적 얼굴이다.
- **3D 비전**: [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]의
  카메라 자세가 $T \in SE(3)$다. 자세 추정은 이 변환을 추정하는 과제이며, 행렬·회전 표현을
  직접 회귀할 수도 있고 대응점 풀이, 기하 최적화, 필터링, 분포 추정으로 얻을 수도 있다.
- **시뮬레이션과 디지털 트윈**: 모든 시뮬레이터 상태와 BIM-로봇 정합이 $T$들의 스택이다
  ([[05-construction-robotics/index|건설]]).

> [!tip] 더 깊이 · Going deeper
> Lynch & Park의 [*Modern Robotics*](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)(Cambridge, PDF 무료) 3장이 이 페이지 전체의 완전한 판본이고, 이 위키의 [[04-robotics/modern-robotics/index|MR 장별 노트]]가 그것을 통과하는 안내된 길이다. 일반 기하학 책이 아니라 3장을 읽어라. 로보틱스 독자가 필요로 하는 순서대로 $SO(3)$과 $SE(3)$을 전개하고, 스크류와 트위스트가 기계장치가 아니라 어떤 질문의 답으로 도착한다. 이 페이지의 §4는 의도적으로 그 장으로 가는 진입로이고, 그 장이 시작되는 곳에서 멈춘다.

### 스스로 점검

1. 2D에서 $R(\theta)R(-\theta) = I$를 검산하고, 일반적으로 $R^{-1} = R^\top$인 이유를
   설명하라.
2. 오일러 각을 MSE로 회귀하면 $\pm180°$ 근처에서 왜 이상해지는가? 쿼터니언의 이중 덮개는
   순진한 MSE에 무슨 짓을 하는가?
3. $T_{base \leftarrow cam}$과 점 $p_{cam}$이 주어졌을 때, 베이스 프레임의 점을 써라.
4. "그리퍼 *자신의* z축 방향으로 5 cm 이동" 명령은 현재 자세에 왼쪽 곱인가 오른쪽 곱인가?
   왜인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 곱을 전개하면 $\cos^2\theta + \sin^2\theta = 1$ 항등으로 $I$가 나온다. 일반적으로는 $R$의 열들이 정규직교라 $R^\top R = I \Rightarrow R^{-1} = R^\top$.
> 2. $\pm 180°$ 경계에서 각도 값이 점프한다($179° \to -181°$가 아니라 $-179°$) — 이웃한 회전이 먼 타깃이 되어 MSE가 폭발. 쿼터니언은 $q$와 $-q$가 같은 회전이라, 타깃과 부호가 반대면 옳은 답에 큰 손실을 주는 잘못된 그래디언트가 생긴다.
> 3. $p_{base} = T_{base \leftarrow cam}\,[p_{cam}; 1]$ (동차 좌표로 확장해 곱한다).
> 4. 오른쪽 곱 $T \cdot \Delta T$ — 자기(그리퍼) 프레임 기준 운동은 오른쪽에, 월드 프레임 기준 운동은 왼쪽에 곱한다.

### 과제 · Problem set

Tier B. **P2**, $\theta=(0^\circ,90^\circ)$, 그리고 1번과 3번에서는 반대쪽 엘보 $\theta=(90^\circ,-90^\circ)$. 이 페이지 §3–4. 평면이므로 $R=R_z(\theta_1+\theta_2)$.

1. **그리기.** 반대쪽 엘보 $\theta=(90^\circ,-90^\circ)$에 대한 위의 그림: 원점의 베이스 프레임, $(0,1)$의 엘보, 그리고 같은 점 $(1,1)$에 있되 전완이 이제 수평인 말단 프레임. 두 원점을 기입하고, 그림에서 읽은 $R$을 쓰고, 도구 $x$축을 따라 $0.1\,\mathrm{m}$ 나간 점을 표시하라. 이 말단 프레임은 위의 그림과 무엇을 공유하고 무엇을 공유하지 않는가?
2. **유도.** (가) 카탈로그 자세에서 카메라 하나가 공구의 $y$축을 따라 $0.2\,\mathrm m$ 떨어진 곳에 고정되어 있다. $T$로 그 위치를 베이스 좌표로 구하고, 돌리지 않고 더한 $p+(0,0.2,0)$이 얼마나 어긋나는지 말하라. (나) 이어서 공구가 자기 $z$축 둘레로 $90^\circ$ 돈다, $T\,\mathrm{Rot}_z(90^\circ)$. 여기서 $\mathrm{Rot}_z(90^\circ)$는 $R=R_z(90^\circ)$이고 이동이 없는 자세다. 새 $R$과 $p$, 카메라의 베이스 위치를 구하라. 그다음 같은 $\mathrm{Rot}_z(90^\circ)$를 대신 왼쪽에 곱하면 공구와 카메라가 어디로 가는지 말하라.
3. **해석.** 반대쪽 엘보 $\theta=(90^\circ,-90^\circ)$에서는 엘보가 $(0,1)$에 있다. 관절 2의 트위스트 열을 베이스 좌표로, 그리고 $\mathrm{Ad}_{T^{-1}}$로 도구 좌표로 써라. 두 열 가운데 카탈로그 자세(§4)의 것과 달라진 쪽은 어느 것이고 왜인가? 그것이 $\mathrm{Ad}$와 $J$의 차이에 대해 무엇을 말하는가?

> [!note]- 그리는 법 · How to draw it
> - 원점의 베이스 프레임을 오른손 삼각대로: $x_s$는 $+x$, $y_s$는 $+y$, $z_s$는 지면 밖으로 나오므로 동그라미 안의 점. 지면 위에 화살표 둘이 아니라 축 셋이 있어야 한다.
> - 팔은 흐리게만, 엘보 $(0,1)$과 말단 $(1,1)$. 대상은 프레임이고 링크는 받침대일 뿐이다.
> - 전완이 $+x_s$를 따라 놓인 말단 프레임: $x_b$는 $+x_s$, $y_b$는 $+y_s$, $z_b$는 지면 밖. 이번에는 말단 축이 베이스 축과 *정말로* 평행하고, $\theta_1+\theta_2=0$이므로 그게 맞다. 위 그림에서 같은 그림을 그렸다면 $R$의 내용 전부를 잃었을 것이다.
> - $R$을 계산이 아니라 그림에서 읽는다. 각 열이 말단 축 하나를 베이스 좌표로 쓴 것이다. $x_b=(1,0,0)$, $y_b=(0,1,0)$, $z_b=(0,0,1)$, 곧 $R=I$. §1의 검사 둘 — 정규직교인 열, $x_b\times y_b=z_b$ — 로 확인한다.
> - 베이스 원점에서 말단 원점으로 가는 화살표 $p=(1,1,0)$ — 위 그림과 같은 $p$ — 그리고 구석에 $R$, 마지막 열에 $p$, 아래 행에 $(0,0,0,1)$을 적은 $T$.
> - *도구* $x$축을 따라 $0.1\,\mathrm{m}$ 나간 점은 베이스 $(1.1,\ 1,\ 0)$, 이번에는 말단의 오른쪽에 찍고, 그 옆에 도구의 $x$-*방향*을 짧은 화살표 $(1,0,0)$으로 그린다. 점은 회전되고 *또* 평행이동하며, 방향은 회전만 된다.
> - 여백 상자의 역변환: 도구 프레임에서 본 베이스 원점 $-R^\top p=(-1,\ -1,\ 0)$. 강체 운동은 거리를 바꿀 수 없으므로 말단에서 여전히 $\sqrt2$다.

> [!tip]- 정답 · Solutions
> 1. 엘보 $(0,1)$, 말단 $(1,1)$이고 $x_b$는 $+x_s$, $y_b$는 $+y_s$를 따른다. 여기서는 $\theta_1+\theta_2=0$이라 $R=R_z(0)=I$이고, 이 전완이 $+x$를 가리키므로 말단 축이 베이스 축과 평행한 것이 맞다. 원점 $p=(1,1,0)$은 위 그림과 같고 방향은 다르다. 그래서 $T=\begin{pmatrix}1&0&0&1\\0&1&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$는 위 그림의 $T$와 $3\times3$ 구석만 다르다. 도구 점은 베이스 $(1.1,\ 1,\ 0)$, 곧 말단 위가 아니라 오른쪽에 찍히고, 도구에서 본 베이스 원점은 $(-1,\ -1,\ 0)$으로 여전히 $\sqrt2$ 떨어져 있다. 위치 하나로는 자세가 정해지지 않는다.
> 2. (가) $T\,(0,\ 0.2,\ 0,\ 1)^\top$: $R\,(0,0.2,0)=(-0.2,0,0)$에 $p$를 더하면 $(0.8,\ 1,\ 0)$이다. 그림에서 공구의 $y$축이 $-x_s$ 쪽을 향하므로 말단의 왼쪽 $0.2\,\mathrm m$다. 돌리지 않고 더한 $(1,\ 1.2,\ 0)$은 $0.2\sqrt2=0.283\,\mathrm m$ 떨어져 있다. (나) 오른쪽 곱: $R=R_z(90^\circ)R_z(90^\circ)=R_z(180^\circ)$이고 $p=(1,1,0)$은 그대로다. 공구가 제자리에서 돌고, 카메라는 $R_z(180^\circ)(0,0.2,0)+p=(1,\ 0.8,\ 0)$, 곧 말단 아래로 간다. 왼쪽 곱: $R=R_z(180^\circ)$은 같지만 $p=R_z(90^\circ)(1,1,0)=(-1,\ 1,\ 0)$이다. 공구 전체가 베이스 원점을 지나는 베이스 $z$축 둘레로 $90^\circ$ 휘돌아 가고, 카메라는 $(-1,\ 0.8,\ 0)$에 놓인다. 같은 회전이 같은 최종 방향을 주면서도 자리는 둘로 갈리는데, 곱하는 쪽이 회전축을 어느 프레임에 고정하는지 말하기 때문이다.
> 3. 관절 2는 엘보 $q=(0,1,0)$을 지나는 $\hat z$축 둘레로 돌므로 베이스 좌표의 열은 $(0,0,1,\ -\omega\times q)=(0,0,1,\ 1,0,0)$이고, 카탈로그 자세의 $(0,0,1,\ 0,-1,0)$과 다르다. 엘보가 움직였기 때문이다. 이 자세의 $T$는 $R=I$, $p=(1,1,0)$이므로 $\mathrm{Ad}_{T^{-1}}$은 $\omega$를 그대로 두고 선형 부분에 $(-p)\times\omega=(-1,1,0)$을 더해 도구 좌표의 열 $(0,0,1,\ 0,1,0)$을 준다. 카탈로그 자세와 같은 열이다. 도구 프레임에서 엘보는 언제나 말단 $1\,\mathrm m$ 뒤, $(-1,0,0)$에 있기 때문이다. 그러니 $\mathrm{Ad}$는 한 자세에서의 좌표 변환이고, 베이스 좌표로 쓴 $J$는 $\theta$에 따라 바뀐다. 여기서 $J$의 둘째 열은 말단 속도 $v_s+\omega_s\times p=(1,0,0)+(-1,1,0)=(0,1,0)$이고, 카탈로그 자세에서는 $(-1,0,0)$이었다. 속도 프레임을 바꾸면 $J$의 열에 $\mathrm{Ad}$를 왼쪽 곱할 뿐, $J$를 대체하지 않는다.

### 로보틱스 다리

여기서의 회전·변환 표기는 [[04-robotics/modern-robotics/index|Modern Robotics 요약]] 전체와 [[04-robotics/geometric-perception-calibration|3.5 기하 인식]]의 extrinsics가 그대로 사용하며, [[04-robotics/state-estimation-slam|SLAM·위치 추정]]과 [[04-robotics/robot-systems-deployment|로봇 시스템]]의 시간 인덱스 TF 트리에서 실전이 된다.

### 출처 · Sources

- K. M. Lynch, F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — 회전, 동차 변환, 트위스트, 수반 사상, 지수 사상은 3장, 지수 곱 기구학은 4장. 저자들의 [공식 페이지](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)와 이 위키의 [[04-robotics/modern-robotics/index|MR 장별 노트]].
- Y. Zhou, C. Barnes, J. Lu, J. Yang, H. Li, "On the Continuity of Rotation Representations in Neural Networks," CVPR 2019 — §2의 6D 표현.
- 이 페이지의 수치 예제는 P2의 카탈로그 숫자와 명시한 자세로 여기서 직접 계산한 것이다. 믿지 말고 다시 계산하라.
