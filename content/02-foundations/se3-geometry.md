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
track and the VLA papers need it next: the space a robot's states and actions are actually written in.*

Every robot action, camera pose, and 3D reconstruction in this wiki lives in SE(3) — the
space of rigid-body poses. This page is the working set for reading VLA action spaces and
3D vision papers; the full treatment (screws, exponential coordinates) lives in
[[04-robotics/modern-robotics-book|Modern Robotics ch. 3]].

> [!note] First pass · 처음이라면
> Read §1 (rotation order, with the coordinates), §3 (poses compose by matrix product), §5 (where this shows up). §2 is a table to consult, and §4 is the on-ramp to Modern Robotics — read it when you get there.

### Homework diagram · 과제가 그릴 그림

The object is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at $\theta=(0^\circ,90^\circ)$, drawn as two frames rather than as an arm. The problem set asks for this drawing.

**Two frames, axes first.** Draw the base frame at the origin: $x_s$ along $+x$, $y_s$ along $+y$, $z_s$ out of the page, drawn as a circled dot so the page has a right-handed triad and not two arrows. Sketch the arm faintly behind it — elbow $(1,0)$, tip $(1,1)$ — but draw it faintly, because this page's object is the frames and the links are only scaffolding. At the tip, draw the second frame. The forearm is vertical, so the tool's own $x$-axis points along $+y_s$ (straight up the page) and its $y$-axis along $-x_s$ (to the left); $z$ stays out of the page. Label the tip axes $x_b$, $y_b$, $z_b$ and *do not* draw them parallel to the base axes — the entire content of $R$ is that they are not.

**The matrix, read off the drawing rather than computed.** Beside the figure write a $3\times3$ box and fill each column by reading the corresponding tip axis off the page in base coordinates: $x_b=(0,1,0)$, $y_b=(-1,0,0)$, $z_b=(0,0,1)$. That is $R_z(90^\circ)$, obtained without a trigonometric identity. Under the box write the two membership tests of §1 as checks you can do on those three columns: they are unit length and mutually perpendicular ($R^\top R=I$), and $x_b\times y_b=z_b$ rather than $-z_b$ ($\det R=+1$). Then draw the arrow from base origin to tip origin and label it $p=(1,1,0)$, and assemble $T$ with $R$ in the corner, $p$ in the last column, and the bottom row $(0,0,0,1)$ written in — that row is not decoration, and §3 says what goes wrong without it.

**One point and one direction, to separate them.** Mark a small dot $0.1\,\mathrm{m}$ out along the *tool's* $x$-axis. In tool coordinates it is $(0.1,0,0)$; on the page it sits at $(1,\ 1.1,\ 0)$ in base coordinates, so draw it above the tip, not to the right of it. Beside it draw the tool's $x$-*direction* as a short arrow and label it $(0,1,0)$ in base coordinates. Write the difference next to the two marks: the point carried the fourth entry $1$ and so was rotated *and* shifted; the direction carried $0$ and was only rotated. Nearly every frame bug in the robotics track is this distinction.

**The inverse, drawn as the same picture read backwards.** In a margin box, draw the base origin as seen from the tool frame: it lies at $(-1,\ 1,\ 0)$ in tool coordinates, which is $-R^\top p$. Draw it at the correct place relative to the tool axes — one unit against $x_b$ (down the page), one unit along $y_b$ (to the left) — and check on the page that its distance from the tip is still $\sqrt2$, since a rigid motion cannot change a distance. The problem set asks for $T$; this box is how you check the $T$ you wrote without multiplying anything.

### 1. Rotations are matrices with rules

- A 3D rotation is a matrix $R \in \mathbb{R}^{3\times 3}$ with $R^\top R = I$ and
  $\det R = +1$ — the set of all such matrices is the **group SO(3)**.
  "Group" is the algebraic word for a set closed under composition where every element has an inverse.
  Here that means a rotation times a rotation is a rotation, and every rotation can be undone.
  That is all the word carries here.
  - **The two defining conditions, each named.** Written as a set,
    $$SO(3)=\{R\in\mathbb{R}^{3\times3} : R^\top R=I,\ \det R=+1\}$$
    so a matrix belongs exactly when it passes both tests. (1) **Orthogonality**, $R^\top R=I$: it preserves lengths and angles, since $(Rx)^\top(Ry)=x^\top R^\top R\,y=x^\top y$. (2) **Orientation preservation**, $\det R=+1$: it keeps a right-handed frame right-handed. Orthogonality alone already forces $\det R=\pm1$, and the second condition throws out the $-1$ half, the reflections. "S" is for *special* ($\det=+1$), "O" for *orthogonal*, and $3$ for the dimension.
  - **The group axioms, each named.** A **group** is a set with an operation satisfying four conditions. (1) **Closure**: combining two elements gives an element, $R_1,R_2\in SO(3)\Rightarrow R_1R_2\in SO(3)$, because $(R_1R_2)^\top R_1R_2=R_2^\top R_2=I$ and $\det(R_1R_2)=1\cdot1$. (2) **Associativity**: $(R_1R_2)R_3=R_1(R_2R_3)$, inherited from matrix multiplication. (3) **Identity**: $I$ is a rotation and $IR=RI=R$. (4) **Inverse**: $R^{-1}=R^\top$ is again a rotation. Commutativity is *not* an axiom, which is why the order result below is possible.
  - **Non-examples.** $S=\text{diag}(2,1,1)$ is not a rotation: $S^\top S=\text{diag}(4,1,1)\ne I$, it stretches the $x$-axis. The set of rotations about $x$ by angles in $[0°,90°]$ is not a group: $60°$ followed by $60°$ gives $120°$, outside the set, so closure fails.
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
- **The elementary rotations, for any angle.** The two matrices above are the $\theta=90°$ cases of the three rotations about the coordinate axes:
  $$R_x(\theta)=\begin{pmatrix}1&0&0\\0&c&-s\\0&s&c\end{pmatrix},\quad R_y(\theta)=\begin{pmatrix}c&0&s\\0&1&0\\-s&0&c\end{pmatrix},\quad R_z(\theta)=\begin{pmatrix}c&-s&0\\s&c&0\\0&0&1\end{pmatrix}$$
  with $c=\cos\theta$ and $s=\sin\theta$, so each leaves its own axis fixed and applies the 2D rotation to the other two coordinates. $R_y$'s signs look flipped because the right-hand rule orders that plane as $z$ then $x$. A positive $\theta$ turns counterclockwise when you look from the positive axis back toward the origin.
- **Checking a matrix is a rotation**, which you should do whenever you build one: columns

  must have length 1, be mutually perpendicular, and $\det = +1$. For $R_z(90°)$: columns are
  $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ — unit length ✓, pairwise dot products all 0 ✓, and
  $\det = +1$ ✓. A $\det$ of $-1$ means you built a **reflection**, which mirrors the robot
  rather than turning it — a real and common bug when converting conventions.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="the same point rotated by z then x lands on the z axis, and by x then z lands on the y axis">
  <defs><marker id="seA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <line x1="150" y1="110" x2="197.6" y2="137.5"/>
    <line x1="150" y1="110" x2="102.4" y2="137.5"/>
    <line x1="150" y1="110" x2="150" y2="55"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.7">
    <text x="201.6" y="147.5">x</text><text x="90.4" y="147.5">y</text><text x="146" y="49">z</text>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" stroke-dasharray="5 4" opacity="0.85" marker-end="url(#seA)">
    <path d="M197.6,137.5 Q150.0,115.5 102.4,137.5"/>
    <path d="M102.4,137.5 Q126.2,33 150,55"/>
  </g>
  <g fill="currentColor"><circle cx="150" cy="110" r="3"/><circle cx="197.6" cy="137.5" r="3.4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="86" y="36">R&#7526; first, then R&#8339;</text></g>
  <g font-size="9.5" fill="currentColor" opacity="0.85"><text x="86" y="172">(1,0,0) &#8594; (0,1,0) &#8594; (0,0,1)</text></g>
  <g font-size="9.5" fill="currentColor"><text x="86" y="188">ends on z</text></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <line x1="410" y1="110" x2="457.6" y2="137.5"/>
    <line x1="410" y1="110" x2="362.4" y2="137.5"/>
    <line x1="410" y1="110" x2="410" y2="55"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.7">
    <text x="461.6" y="147.5">x</text><text x="350.4" y="147.5">y</text><text x="406" y="49">z</text>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" stroke-dasharray="5 4" opacity="0.85" marker-end="url(#seA)">
    <path d="M457.6,137.5 Q410.0,115.5 362.4,137.5"/>
  </g>
  <g fill="currentColor"><circle cx="410" cy="110" r="3"/><circle cx="457.6" cy="137.5" r="3.4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="346" y="36">R&#8339; first, then R&#7526;</text></g>
  <g font-size="9.5" fill="currentColor" opacity="0.85"><text x="346" y="172">(1,0,0) &#8594; (1,0,0) &#8594; (0,1,0)</text></g>
  <g font-size="9.5" fill="currentColor"><text x="346" y="188">ends on y</text></g>
  <g font-size="9" fill="currentColor" opacity="0.75"><text x="346" y="204">R&#8339; leaves a point on the x axis alone</text></g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="224">Same two rotations, different order, different place. The second rotation acts on wherever the</text>
    <text x="24" y="240">first one left you &#8212; nothing subtler than that is going on. It is why R&#8377;&#8338;&#8341;&#8343;&#8342;R&#8341;&#8338;&#8340;&#8342; and R&#8341;&#8338;&#8340;&#8342;R&#8377;&#8338;&#8341;&#8343;&#8342; describe</text>
    <text x="24" y="256">different motions, and why every convention mismatch in robotics is ultimately this one.</text>
  </g>
</svg>

### 2. The four ways papers write rotations

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

**Representation changes coordinates, not the physical orientation.** A rotation matrix stores how the local axes point in the reference frame. Euler angles describe an ordered sequence of rotations, so their order is part of the definition. Axis-angle describes an axis and a turn about it; the table's minimal count refers to its independent degrees of freedom, often stored as a rotation vector. An explicit unit axis plus angle uses redundant stored components.

A unit quaternion is another constrained coordinate system. Its sign ambiguity means q and −q can encode exactly the same orientation, so a raw Euclidean difference between their entries is a poor rotation-error measure. Converting a rotation matrix to a quaternion has its own trap — the textbook formula divides by $4w$, which vanishes near 180° — and [[02-foundations/algorithms/robotics-ai-problems|11.8 §8]] codes the stable version. Gimbal lock is what happens when the middle Euler rotation reaches ±90° (pitch, for roll-pitch-yaw): the first and third rotation axes line up, so two of the three angles now turn about the same axis and one direction of rotation has no angle left to describe it. It likewise belongs to an Euler coordinate chart, not a physical loss of the object's ability to rotate.

**The three minimal-or-compact representations, each defined with its formula.**
- **Euler angles (roll-pitch-yaw).** Three angles for a fixed, ordered product of elementary rotations. The common ZYX convention, with yaw $\psi$, pitch $\theta$ and roll $\phi$, is
  $$R=R_z(\psi)\,R_y(\theta)\,R_x(\phi)$$
  so the definition has three parts: the three angles, the three axes, and their order. Read left to right it is yaw, then pitch about the *new* $y$, then roll about the *newest* $x$ (intrinsic); read right to left it is roll, pitch, yaw about the *fixed* world axes (extrinsic). Both readings give the same matrix, which is why papers must say which convention they use. **Gimbal lock, with numbers:** at $\theta=90°$ the product depends only on $\psi-\phi$. $(\psi,\theta,\phi)=(30°,90°,10°)$ and $(50°,90°,30°)$ both give $\begin{pmatrix}0&-0.342&0.940\\0&0.940&0.342\\-1&0&0\end{pmatrix}$, so one of the three angles has stopped doing anything.
- **Axis-angle.** A unit axis $\hat\omega$ and an angle $\theta$, often stored as the **rotation vector** $r=\theta\hat\omega$ (three numbers). The matrix is given by Rodrigues' formula,
  $$R=I+\sin\theta\,[\hat\omega]_\times+(1-\cos\theta)\,[\hat\omega]_\times^2$$
  where $[\hat\omega]_\times$ is the skew-symmetric matrix of §4, so the rotation is built from the identity plus two terms that act only perpendicular to the axis. Example: $\hat\omega=(0,0,1)$, $\theta=90°$ gives exactly $R_z(90°)$. It is derived in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §2]].
- **Unit quaternion.** Four numbers $q=(w,x,y,z)$ with one constraint, $w^2+x^2+y^2+z^2=1$. The rotation by $\theta$ about $\hat\omega$ is
  $$q=\big(\cos\tfrac{\theta}{2},\ \sin\tfrac{\theta}{2}\,\hat\omega\big)$$
  and it acts on a vector $v$ by the quaternion product $q\otimes(0,v)\otimes q^{*}$, where $q^{*}=(w,-x,-y,-z)$ is the conjugate; composing rotations is multiplying quaternions. The half angle is the source of the **double cover**: $\theta+360°$ describes the same rotation but gives $-q$. Example: $R_z(90°)$ is $q=(0.707,\,0,\,0,\,0.707)$, and both $q$ and $-q$ send $(1,0,0)$ to $(0,1,0)$, although $\lVert q-(-q)\rVert=2$. The correct rotation distance ignores the sign: $\text{angle}(q_1,q_2)=2\arccos\lvert q_1^\top q_2\rvert$, which for the identity $(1,0,0,0)$ and this $q$ is $2\arccos0.707=90°$.
- **Slerp** (spherical linear interpolation). Between unit quaternions $q_0,q_1$ with $\cos\Omega=q_0^\top q_1$, for $t\in[0,1]$:
  $$\text{slerp}(q_0,q_1;t)=\frac{\sin\big((1-t)\Omega\big)}{\sin\Omega}\,q_0+\frac{\sin(t\Omega)}{\sin\Omega}\,q_1$$
  so the result stays on the unit sphere and the rotation angle grows at constant rate. Example: from the identity to $R_z(90°)$ ($\Omega=45°$) at $t=0.5$ it gives $(0.924,\,0,\,0,\,0.383)$, which is $R_z(45°)$. The plain average $(0.854,\,0,\,0,\,0.354)$ has norm $0.924$, so it is not a unit quaternion until renormalised. (Flip $q_1$ to $-q_1$ first if $q_0^\top q_1<0$, so the interpolation takes the short way round.)

**Check your understanding.** If a robot's logged Euler angle jumps while the object moves smoothly, first check wrapping and the chosen rotation order. Do not immediately diagnose a mechanical jump. For a learning target, distinguish a discontinuity in coordinates from a discontinuity in the underlying motion.

### 3. Poses: SE(3) and homogeneous transforms

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
    $\mathrm{Ad}_T$ rewrites one twist in another frame; $J$ stacks joint screws at this pose. They are not the same map. Changing the velocity frame left-multiplies $J$'s columns by $\mathrm{Ad}$. The problem set asks you to write this $T$.
  - **What the subscripts mean.** $T_{AB}$ is the pose of frame $B$ expressed in frame $A$: its $R$ columns are $B$'s axes written in $A$'s coordinates, and its $p$ is $B$'s origin in $A$'s coordinates. Used as a map it converts coordinates, $x_A=T_{AB}\,x_B$, which is why inner subscripts must match to multiply. $T_{world\leftarrow cam}$ below is the same object written with an arrow.

<svg viewBox="0 0 470 190" style="max-width:100%;height:auto" role="img" aria-label="frame composition: world to base to camera">
  <defs><marker id="se3a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <path d="M40,140 L40,100"/><path d="M40,140 L80,140"/>
    <path d="M200,120 L188,86"/><path d="M200,120 L234,108"/>
    <path d="M360,70 L352,34"/><path d="M360,70 L396,64"/>
  </g>
  <g fill="currentColor"><circle cx="40" cy="140" r="3"/><circle cx="200" cy="120" r="3"/><circle cx="360" cy="70" r="3"/></g>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" opacity="0.8" fill="none">
    <path d="M46,138 L193,123" marker-end="url(#se3a)"/><path d="M206,118 L353,73" marker-end="url(#se3a)"/>
    <path d="M44,148 C140,184 272,142 356,80" marker-end="url(#se3a)"/>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="18" y="162">world A</text><text x="176" y="144">base B</text><text x="346" y="26">camera C</text>
    <text x="98" y="116" font-size="11">T_AB</text><text x="264" y="84" font-size="11">T_BC</text>
    <text x="150" y="176" font-size="11" opacity="0.85">T_AC = T_AB · T_BC &#8212; B cancels</text>
  </g>
</svg>


- **Worked composition, with numbers.** Let the base sit $2$ m along world-$x$ and be turned
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
  That rotation of the offset is the step people forget, and it is exactly what the matrix
  form does for you automatically — which is the entire reason poses are written as $4\times4$ matrices instead
  of an $(R, p)$ pair you combine by hand.
- **Frames discipline** is 90% of not making sign errors: every quantity has a frame
  (world, base, camera, end-effector); write it down. "Where is the camera?" = $T_{world \leftarrow cam}$.

### 4. Velocity and small motions (the on-ramp to Modern Robotics)

- Angular velocity $\omega$ is a vector (axis × speed); rigid-body velocity = **twist**
  $(\omega, v)$ — six numbers, and the reason end-effector velocity commands are 6-DoF.
  - **Angular velocity, stated completely.** A vector $\omega\in\mathbb{R}^3$ with two parts: its **direction** is the instantaneous rotation axis, oriented by the right-hand rule (curl the fingers with the motion, the thumb points along $\omega$), and its **magnitude** $\lVert\omega\rVert$ is the turning rate in rad/s. For a body spinning about an axis through the origin, a body point at position $p$ moves with
    $$\dot p=\omega\times p$$
    so points on the axis stay still and speed grows with distance from it. Example: $\omega=(0,0,2)$ rad/s and $p=(1,0,0)$ m give $\dot p=(0,2,0)$ m/s: perpendicular to both the axis and the point's offset.
  - **The skew-symmetric matrix $[\omega]_\times$, stated completely.** The $3\times3$ matrix that performs "cross with $\omega$":
    $$[\omega]_\times=\begin{pmatrix}0&-\omega_3&\omega_2\\\omega_3&0&-\omega_1\\-\omega_2&\omega_1&0\end{pmatrix},\qquad [\omega]_\times v=\omega\times v$$
    so it is **skew-symmetric**, $[\omega]_\times^\top=-[\omega]_\times$, with zeros on the diagonal and exactly three free entries, the components of $\omega$. Example: $\omega=(0,0,1)$ gives $[\omega]_\times(1,0,0)=(0,1,0)$, the same as $\omega\times(1,0,0)$. Its sign pattern is developed in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §1]].
  - **Twist, stated completely.** A six-vector $\mathcal{V}=(\omega,v)$ with two parts: the angular velocity $\omega$, and a linear part $v$ that is the velocity of the body point *currently at the frame's origin* (whether or not the body actually occupies that point). Every body point $p$ then moves with
    $$\dot p=v+\omega\times p$$
    because a rigid velocity is the origin point's velocity plus the rotation about it. Example: a joint about the vertical axis through $q=(1,0,0)$ turning at $\omega=(0,0,1)$ has $v=-\omega\times q=(0,-1,0)$. The point on the axis gets $(0,-1,0)+(0,1,0)=0$ and stays still, as it must; the point $(2,0,0)$ gets $(0,1,0)$. Non-example: reading $v$ as the tool-tip velocity, which is only true when the tip sits at the frame origin. Which origin that is, space or body, is worked through in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §3]], and the two descriptions of one motion in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions §4]].
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

**Pose and velocity answer different questions.** A pose says where a frame is now; a twist says how rigid-body motion changes instantaneously. A finite rotation cannot generally be obtained by simply adding its matrix entries or Euler angles, because successive rotations compose through multiplication and order matters. The small-motion approximation supplies a local linear language in which differentiation becomes possible.

> [!example] From an axis to $T$, and back
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
> ([[04-robotics/modern-robotics/ch04-forward-kinematics|Forward Kinematics]]) and pose-error IK.

The linear part of a twist also depends on the reference frame and its origin. The same rotating body gives different point velocities at different distances from its axis. Before treating the last components of a twist as tool-tip translation, determine whether the twist is expressed in a body frame or a space frame and where that frame's origin lies. The detailed distinction is developed in [[04-robotics/modern-robotics/ch03-rigid-body-motions|Rigid-Body Motions]].

**Check your understanding.** Changing the reference frame changes the coordinates of the twist without changing the physical motion. This is a coordinate conversion problem, not a new motion command. It is why a velocity vector without its frame is an incomplete robot interface.

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

Tier B. **P2** at $\theta=(0^\circ,90^\circ)$. This page §3–4. Planar, so $R=R_z(\theta_1+\theta_2)$.

1. **Draw.** Base frame at the origin and tip frame at $(1,1)$. The second link is vertical: tip $x$-axis along $+y$. Label both origins.
2. **Derive.** Write $T_{\mathrm{base}\leftarrow\mathrm{tip}}$ as a $4\times 4$ homogeneous matrix. Rotation of the second link is $90^\circ$ about $z$; translation is the tip $(1,1,0)$.
3. **Interpret.** $\mathrm{Ad}_T$ rewrites one twist in another frame. $J$ maps $\dot\theta$ to a twist at this pose. Same matrix? What would $\mathrm{Ad}_T$ do to a column of $J$ if you changed the velocity frame?

> [!tip]- Solutions
> 1. Base at $(0,0)$; elbow $(1,0)$; tip $(1,1)$ with $x_{\mathrm{tip}}$ up and $y_{\mathrm{tip}}$ left.
> 2. $R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$, $p=(1,1,0)$, so
>    $T=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$.
> 3. Not the same map. $J$ is pose-dependent and stacks joint screws; $\mathrm{Ad}_T$ is a change of frame for a single twist. Changing the velocity frame left-multiplies $J$'s columns by $\mathrm{Ad}$ — it does not replace $J$.

### Robotics bridge

This notation is used verbatim throughout the [[04-robotics/modern-robotics/index|Modern Robotics summary]] and the extrinsics of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]]; it becomes operational in [[04-robotics/state-estimation-slam|SLAM and localization]] and the time-indexed TF trees of [[04-robotics/robot-systems-deployment|Robot Systems]].

## 한국어

*[[02-foundations/linear-algebra|1. 선형대수]] 하나 위에 선다 — RL이나 신호처리에는 빚진 것이 없다. 여기 놓인 이유는 로보틱스 트랙과
VLA 논문이 다음으로 이것을 요구하기 때문이다: 로봇의 상태와 행동이 실제로 적히는 공간.*

이 위키의 모든 로봇 행동, 카메라 자세, 3D 재구성은 SE(3) — 강체 자세의 공간 — 에 산다.
이 페이지는 VLA 행동 공간과 3D 비전 논문을 읽기 위한 작업 세트다; 완전한 전개(스크류,
지수 좌표)는 [[04-robotics/modern-robotics-book|Modern Robotics 3장]]의 몫이다.

> [!note] 처음이라면 · First pass
> 먼저 §1(회전 순서, 좌표까지), §3(자세는 행렬곱으로 합성된다), §5(어디에 나타나는가). §2는 찾아보는 표이고, §4는 Modern Robotics로 가는 진입로다 — 거기 도착할 때 읽어라.

### 과제가 그릴 그림 · Homework diagram

대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**를 $\theta=(0^\circ,90^\circ)$에서 본 것이고, 팔이 아니라 프레임 둘로 그린다. 과제가 이 그림을 요구한다.

**프레임 둘, 축부터.** 원점에 베이스 프레임을 그린다. $x_s$는 $+x$, $y_s$는 $+y$, $z_s$는 지면 밖으로 나오므로 동그라미 안의 점으로 그린다. 화살표 둘이 아니라 오른손 삼각대가 지면 위에 있어야 하기 때문이다. 팔은 뒤에 흐리게 스케치한다 — 엘보 $(1,0)$, 말단 $(1,1)$ — 흐리게 그리는 이유는 이 페이지의 대상이 프레임이고 링크는 받침대일 뿐이기 때문이다. 말단에 둘째 프레임을 그린다. 전완이 수직이므로 도구 자신의 $x$축은 $+y_s$(지면 위쪽)를, $y$축은 $-x_s$(왼쪽)를 향하고 $z$는 지면 밖 그대로다. 말단 축에 $x_b$, $y_b$, $z_b$라 이름 붙이고 베이스 축과 평행하게 그리지 *않는다*. $R$의 내용 전부가 그 둘이 평행하지 않다는 것이다.

**행렬, 계산이 아니라 그림에서 읽어 내기.** 그림 옆에 $3\times3$ 상자를 그리고, 각 열을 해당 말단 축을 베이스 좌표로 읽어 채운다. $x_b=(0,1,0)$, $y_b=(-1,0,0)$, $z_b=(0,0,1)$. 삼각함수 항등식 없이 얻은 $R_z(90^\circ)$다. 상자 아래에는 §1의 소속 검사 둘을, 그 세 열로 직접 할 수 있는 확인으로 적는다. 길이가 1이고 서로 수직이며($R^\top R=I$), $x_b\times y_b$가 $-z_b$가 아니라 $z_b$다($\det R=+1$). 그다음 베이스 원점에서 말단 원점으로 화살표를 긋고 $p=(1,1,0)$이라 쓴 뒤, 구석에 $R$, 마지막 열에 $p$, 아래 행에 $(0,0,0,1)$을 적어 $T$를 조립한다. 그 아래 행은 장식이 아니고, 없으면 무엇이 깨지는지는 §3이 말한다.

**점 하나와 방향 하나, 둘을 가르기 위해.** *도구* $x$축을 따라 $0.1\,\mathrm{m}$ 나간 자리에 작은 점을 찍는다. 도구 좌표로는 $(0.1,0,0)$이고, 지면 위 베이스 좌표로는 $(1,\ 1.1,\ 0)$이므로 말단의 오른쪽이 아니라 위에 찍힌다. 그 옆에 도구의 $x$-*방향*을 짧은 화살표로 그리고 베이스 좌표 $(0,1,0)$이라 적는다. 두 표시 옆에 차이를 적는다. 점은 넷째 성분 $1$을 지녀 회전되고 *또* 평행이동했고, 방향은 $0$을 지녀 회전만 되었다. 로보틱스 트랙의 프레임 버그는 거의 전부 이 구분이다.

**역행렬, 같은 그림을 거꾸로 읽은 것.** 여백 상자에 도구 프레임에서 본 베이스 원점을 그린다. 도구 좌표로 $(-1,\ 1,\ 0)$이고, 이것이 $-R^\top p$다. 도구 축에 대해 올바른 자리에 — $x_b$ 반대쪽으로 한 칸(지면 아래), $y_b$ 쪽으로 한 칸(왼쪽) — 찍고, 말단에서의 거리가 여전히 $\sqrt2$인지 지면 위에서 확인한다. 강체 운동은 거리를 바꿀 수 없기 때문이다. 과제가 요구하는 것은 $T$이고, 이 상자는 아무것도 곱하지 않고 그 $T$를 검산하는 방법이다.

### 1. 회전은 규칙 있는 행렬이다

- 3D 회전은 $R^\top R = I$이고 $\det R = +1$인 행렬 $R \in \mathbb{R}^{3\times 3}$ —
  이런 행렬 전체의 집합을 **군**(group) SO(3)라고 부른다.
  "군"은 합성에 대해 닫혀 있고 모든 원소에 역원이 있는 집합을 가리키는 대수학 용어다.
  여기서는 회전 × 회전 = 회전이고, 모든 회전은 되돌릴 수 있다는 뜻이다.
  이 단어가 담는 뜻은 그것이 전부다.
  - **두 정의 조건, 각각의 이름.** 집합으로 쓰면
    $$SO(3)=\{R\in\mathbb{R}^{3\times3} : R^\top R=I,\ \det R=+1\}$$
    이므로, 행렬은 두 검사를 모두 통과할 때 정확히 여기에 속한다. (1) **직교성** $R^\top R=I$: $(Rx)^\top(Ry)=x^\top R^\top R\,y=x^\top y$이므로 길이와 각도를 보존한다. (2) **방향 보존** $\det R=+1$: 오른손 좌표계를 오른손 좌표계로 유지한다. 직교성만으로도 $\det R=\pm1$이 강제되고, 둘째 조건이 $-1$ 쪽, 곧 반사를 걸러낸다. "S"는 *special*($\det=+1$), "O"는 *orthogonal*(직교), $3$은 차원이다.
  - **군의 공리, 각각의 이름.** **군**은 연산이 붙은 집합으로 네 조건을 만족한다. (1) **닫힘**: 두 원소를 결합하면 원소가 된다, $R_1,R_2\in SO(3)\Rightarrow R_1R_2\in SO(3)$. $(R_1R_2)^\top R_1R_2=R_2^\top R_2=I$이고 $\det(R_1R_2)=1\cdot1$이기 때문이다. (2) **결합법칙**: $(R_1R_2)R_3=R_1(R_2R_3)$, 행렬곱에서 물려받는다. (3) **항등원**: $I$는 회전이고 $IR=RI=R$. (4) **역원**: $R^{-1}=R^\top$도 회전이다. 교환법칙은 공리가 *아니며*, 그래서 아래의 순서 결과가 가능하다.
  - **반례.** $S=\text{diag}(2,1,1)$은 회전이 아니다. $S^\top S=\text{diag}(4,1,1)\ne I$이고 $x$축을 늘린다. $x$축 둘레로 $[0°,90°]$ 범위의 각만큼 도는 회전들의 집합은 군이 아니다. $60°$ 다음 $60°$는 집합 밖의 $120°$이므로 닫힘이 깨진다.
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
- **임의 각도의 기본 회전.** 위의 두 행렬은 좌표축 둘레 세 회전의 $\theta=90°$ 경우다.
  $$R_x(\theta)=\begin{pmatrix}1&0&0\\0&c&-s\\0&s&c\end{pmatrix},\quad R_y(\theta)=\begin{pmatrix}c&0&s\\0&1&0\\-s&0&c\end{pmatrix},\quad R_z(\theta)=\begin{pmatrix}c&-s&0\\s&c&0\\0&0&1\end{pmatrix}$$
  $c=\cos\theta$, $s=\sin\theta$이므로, 각 회전은 자기 축을 고정하고 나머지 두 좌표에 2D 회전을 적용한다. $R_y$의 부호가 뒤집혀 보이는 것은 오른손 법칙이 그 평면을 $z$ 다음 $x$ 순서로 잡기 때문이다. 양의 $\theta$는 양의 축 쪽에서 원점을 내려다볼 때 반시계 방향으로 돈다.
- **어떤 행렬이 회전인지 확인하기** — 회전 행렬을 만들 때마다 해야 한다: 열의 길이가 1이고,
  서로 수직이며, $\det = +1$이어야 한다. $R_z(90°)$라면 열이 $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ —
  길이 1 ✓, 서로의 내적이 모두 0 ✓, $\det = +1$ ✓. $\det$가 $-1$이면 **반사**를 만든 것이고,
  로봇을 돌리는 대신 거울에 비춘 셈이다 — 규약 변환에서 실제로 자주 나는 버그다.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="같은 점을 z 다음 x로 돌리면 z축에 도착하고 x 다음 z로 돌리면 y축에 도착한다">
  <defs><marker id="seA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <line x1="150" y1="110" x2="197.6" y2="137.5"/>
    <line x1="150" y1="110" x2="102.4" y2="137.5"/>
    <line x1="150" y1="110" x2="150" y2="55"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.7">
    <text x="201.6" y="147.5">x</text><text x="90.4" y="147.5">y</text><text x="146" y="49">z</text>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" stroke-dasharray="5 4" opacity="0.85" marker-end="url(#seA)">
    <path d="M197.6,137.5 Q150.0,115.5 102.4,137.5"/>
    <path d="M102.4,137.5 Q126.2,33 150,55"/>
  </g>
  <g fill="currentColor"><circle cx="150" cy="110" r="3"/><circle cx="197.6" cy="137.5" r="3.4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="86" y="36">R&#7526; 먼저, 그다음 R&#8339;</text></g>
  <g font-size="9.5" fill="currentColor" opacity="0.85"><text x="86" y="172">(1,0,0) &#8594; (0,1,0) &#8594; (0,0,1)</text></g>
  <g font-size="9.5" fill="currentColor"><text x="86" y="188">z축에 도착</text></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <line x1="410" y1="110" x2="457.6" y2="137.5"/>
    <line x1="410" y1="110" x2="362.4" y2="137.5"/>
    <line x1="410" y1="110" x2="410" y2="55"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.7">
    <text x="461.6" y="147.5">x</text><text x="350.4" y="147.5">y</text><text x="406" y="49">z</text>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" stroke-dasharray="5 4" opacity="0.85" marker-end="url(#seA)">
    <path d="M457.6,137.5 Q410.0,115.5 362.4,137.5"/>
  </g>
  <g fill="currentColor"><circle cx="410" cy="110" r="3"/><circle cx="457.6" cy="137.5" r="3.4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="346" y="36">R&#8339; 먼저, 그다음 R&#7526;</text></g>
  <g font-size="9.5" fill="currentColor" opacity="0.85"><text x="346" y="172">(1,0,0) &#8594; (1,0,0) &#8594; (0,1,0)</text></g>
  <g font-size="9.5" fill="currentColor"><text x="346" y="188">y축에 도착</text></g>
  <g font-size="9" fill="currentColor" opacity="0.75"><text x="346" y="204">R&#8339;는 x축 위의 점을 움직이지 않는다</text></g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="224">같은 회전 둘, 다른 순서, 다른 자리. 두 번째 회전은 첫 번째가 남겨둔 자리에 작용한다 &#8212; 그보다</text>
    <text x="24" y="240">미묘한 일은 하나도 일어나지 않는다. 논문의 R&#8377;&#8338;&#8341;&#8343;&#8342;R&#8341;&#8338;&#8340;&#8342;와 R&#8341;&#8338;&#8340;&#8342;R&#8377;&#8338;&#8341;&#8343;&#8342;가 서로 다른 운동을 기술하는</text>
    <text x="24" y="256">이유이고, 로보틱스의 규약 불일치가 결국 전부 이것인 이유다.</text>
  </g>
</svg>

### 2. 논문이 회전을 쓰는 네 가지 방법

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

**표현은 좌표를 바꾸지 물리적 방향을 바꾸지 않는다.** 회전행렬은 로컬 축이 기준 좌표에서 향하는 방향을 저장한다. 오일러 각은 순서 있는 회전의 연속이라 순서도 정의의 일부다. 축–각은 축과 그 둘레의 회전을 나타낸다. 표의 최소 개수는 독립 자유도이며 흔히 회전벡터로 저장한다. 단위축과 각도를 따로 저장하면 중복 성분이 생긴다.

단위 쿼터니언도 제약이 있는 좌표다. q와 −q가 정확히 같은 방향을 나타내므로 성분의 단순 유클리드 차이는 회전 오차로 부적절하다. 회전 행렬을 쿼터니언으로 바꾸는 데도 함정이 있다 — 교과서 식은 $4w$로 나누는데 180° 근처에서 이 값이 0으로 간다 — [[02-foundations/algorithms/robotics-ai-problems|11.8 §8]]이 안정적인 버전을 코드로 보인다. 짐벌락은 가운데 오일러 회전이 ±90°에 이를 때(roll-pitch-yaw라면 pitch) 첫째와 셋째 회전축이 한 줄로 겹쳐, 세 각 중 둘이 같은 축을 돌리게 되고 한 회전 방향을 나타낼 각이 남지 않는 현상이다. 이것도 오일러 좌표 표현의 문제이지 물체가 회전 능력을 물리적으로 잃는 것은 아니다.

**최소 또는 간결한 세 표현, 각각의 식과 정의.**
- **오일러 각(roll-pitch-yaw).** 정해진 순서의 기본 회전 곱을 나타내는 각 세 개다. 흔한 ZYX 규약에서 yaw $\psi$, pitch $\theta$, roll $\phi$로
  $$R=R_z(\psi)\,R_y(\theta)\,R_x(\phi)$$
  이므로 정의에는 세 부분이 있다. 세 각, 세 축, 그리고 그 순서다. 왼쪽부터 읽으면 yaw, 그다음 *새* $y$축 둘레 pitch, 그다음 *가장 새로운* $x$축 둘레 roll(내재적)이고, 오른쪽부터 읽으면 *고정된* 월드 축 둘레로 roll, pitch, yaw(외재적)다. 두 독법이 같은 행렬을 주므로 논문은 어느 규약인지 밝혀야 한다. **숫자로 본 짐벌 락:** $\theta=90°$에서 곱은 $\psi-\phi$에만 의존한다. $(\psi,\theta,\phi)=(30°,90°,10°)$와 $(50°,90°,30°)$가 모두 $\begin{pmatrix}0&-0.342&0.940\\0&0.940&0.342\\-1&0&0\end{pmatrix}$를 주므로, 세 각 중 하나는 아무 일도 하지 않게 된다.
- **축-각.** 단위 축 $\hat\omega$와 각 $\theta$이고, 흔히 **회전 벡터** $r=\theta\hat\omega$(숫자 셋)로 저장한다. 행렬은 로드리게스 공식으로 주어진다.
  $$R=I+\sin\theta\,[\hat\omega]_\times+(1-\cos\theta)\,[\hat\omega]_\times^2$$
  $[\hat\omega]_\times$는 §4의 반대칭 행렬이므로, 회전은 항등행렬에 축에 수직인 방향에만 작용하는 두 항을 더해 만들어진다. 예: $\hat\omega=(0,0,1)$, $\theta=90°$이면 정확히 $R_z(90°)$다. 유도는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §2]]에 있다.
- **단위 쿼터니언.** 제약 하나 $w^2+x^2+y^2+z^2=1$이 붙은 숫자 넷 $q=(w,x,y,z)$다. $\hat\omega$ 둘레 $\theta$ 회전은
  $$q=\big(\cos\tfrac{\theta}{2},\ \sin\tfrac{\theta}{2}\,\hat\omega\big)$$
  이고 벡터 $v$에는 쿼터니언 곱 $q\otimes(0,v)\otimes q^{*}$로 작용한다. $q^{*}=(w,-x,-y,-z)$는 켤레다. 회전 합성은 쿼터니언 곱이다. 반각이 **이중 덮개**의 원인이다. $\theta+360°$는 같은 회전인데 $-q$를 준다. 예: $R_z(90°)$는 $q=(0.707,\,0,\,0,\,0.707)$이고, $q$와 $-q$ 모두 $(1,0,0)$을 $(0,1,0)$으로 보내지만 $\lVert q-(-q)\rVert=2$다. 올바른 회전 거리는 부호를 무시한다. $\text{angle}(q_1,q_2)=2\arccos\lvert q_1^\top q_2\rvert$이고, 항등 $(1,0,0,0)$과 이 $q$ 사이에서는 $2\arccos0.707=90°$다.
- **slerp**(구면 선형 보간). $\cos\Omega=q_0^\top q_1$인 단위 쿼터니언 $q_0,q_1$ 사이에서 $t\in[0,1]$에 대해
  $$\text{slerp}(q_0,q_1;t)=\frac{\sin\big((1-t)\Omega\big)}{\sin\Omega}\,q_0+\frac{\sin(t\Omega)}{\sin\Omega}\,q_1$$
  그래서 결과가 단위 구면 위에 머물고 회전각이 일정한 속도로 커진다. 예: 항등에서 $R_z(90°)$로($\Omega=45°$) $t=0.5$에서 $(0.924,\,0,\,0,\,0.383)$, 곧 $R_z(45°)$를 준다. 단순 평균 $(0.854,\,0,\,0,\,0.354)$는 노름이 $0.924$라 다시 정규화하기 전까지 단위 쿼터니언이 아니다. ($q_0^\top q_1<0$이면 먼저 $q_1$을 $-q_1$로 뒤집어 짧은 쪽으로 보간한다.)

**이해 확인.** 물체는 부드럽게 움직이는데 로그의 오일러 각이 튀면 먼저 각도 감기와 회전 순서를 본다. 곧바로 기계적 점프를 진단하지 않는다. 학습 목표에서도 좌표의 불연속과 실제 동작의 불연속을 구분한다.

### 3. 자세: SE(3)와 동차 변환

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
    $\mathrm{Ad}_T$는 트위스트 하나의 프레임 변환이고 $J$는 이 자세의 관절 스크류 묶음이다. 같은 사상이 아니다. 과제는 이 $T$를 쓰라고 한다.
  - **아래 첨자의 뜻.** $T_{AB}$는 프레임 $A$에서 표현한 프레임 $B$의 자세다. $R$의 열은 $A$ 좌표로 쓴 $B$의 축이고, $p$는 $A$ 좌표로 쓴 $B$의 원점이다. 사상으로 쓰면 좌표를 변환한다, $x_A=T_{AB}\,x_B$. 곱하려면 안쪽 첨자가 맞아야 하는 이유다. 아래의 $T_{world\leftarrow cam}$은 같은 대상을 화살표로 쓴 것이다.

<svg viewBox="0 0 470 190" style="max-width:100%;height:auto" role="img" aria-label="프레임 합성: 월드에서 베이스, 베이스에서 카메라">
  <defs><marker id="se3a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <path d="M40,140 L40,100"/><path d="M40,140 L80,140"/>
    <path d="M200,120 L188,86"/><path d="M200,120 L234,108"/>
    <path d="M360,70 L352,34"/><path d="M360,70 L396,64"/>
  </g>
  <g fill="currentColor"><circle cx="40" cy="140" r="3"/><circle cx="200" cy="120" r="3"/><circle cx="360" cy="70" r="3"/></g>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" opacity="0.8" fill="none">
    <path d="M46,138 L193,123" marker-end="url(#se3a)"/><path d="M206,118 L353,73" marker-end="url(#se3a)"/>
    <path d="M44,148 C140,184 272,142 356,80" marker-end="url(#se3a)"/>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="18" y="162">월드 A</text><text x="176" y="144">베이스 B</text><text x="346" y="26">카메라 C</text>
    <text x="98" y="116" font-size="11">T_AB</text><text x="264" y="84" font-size="11">T_BC</text>
    <text x="150" y="176" font-size="11" opacity="0.85">T_AC = T_AB · T_BC &#8212; B가 약분된다</text>
  </g>
</svg>


- **합성 계산 예제, 숫자와 함께.** 베이스가 월드 $x$축으로 $2$ m 떨어져 있고 $z$축으로
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
  $(3,0,0)$ — 약 1.4 m($\sqrt 2$) 떨어진, 방향이 틀린 자리다. 사람들이 빼먹는 단계가 바로 그 오프셋 회전이고,
  행렬 형태가 자동으로 해주는 일이 정확히 그것이다 — pose를 $(R, p)$ 쌍으로 들고 손으로
  합치는 대신 $4\times4$ 행렬로 쓰는 이유 전부가 이것이다.
- **프레임 규율**이 부호 실수 안 하기의 90%다: 모든 양에는 프레임(월드, 베이스, 카메라,
  말단)이 있다; 항상 적어라. "카메라가 어디 있나?" = $T_{world \leftarrow cam}$.

### 4. 속도와 미소 운동 (Modern Robotics로 가는 진입로)

- 각속도 $\omega$는 벡터(축 × 속력); 강체 속도 = **twist** $(\omega, v)$ — 여섯 숫자이고,
  말단 속도 명령이 6자유도인 이유다.
  - **각속도의 완전한 정의.** 두 부분을 가진 벡터 $\omega\in\mathbb{R}^3$다. **방향**은 순간 회전축이고 오른손 법칙으로 향한다(손가락을 운동 방향으로 감으면 엄지가 $\omega$를 가리킨다). **크기** $\lVert\omega\rVert$는 rad/s 단위의 회전 속도다. 원점을 지나는 축 둘레로 도는 물체에서 위치 $p$의 물체 점은
    $$\dot p=\omega\times p$$
    로 움직이므로, 축 위의 점은 가만히 있고 축에서 멀수록 빠르다. 예: $\omega=(0,0,2)$ rad/s, $p=(1,0,0)$ m이면 $\dot p=(0,2,0)$ m/s로, 축과 점의 오프셋 모두에 수직이다.
  - **반대칭 행렬 $[\omega]_\times$의 완전한 정의.** "$\omega$와 외적"을 수행하는 $3\times3$ 행렬이다.
    $$[\omega]_\times=\begin{pmatrix}0&-\omega_3&\omega_2\\\omega_3&0&-\omega_1\\-\omega_2&\omega_1&0\end{pmatrix},\qquad [\omega]_\times v=\omega\times v$$
    그래서 **반대칭**, $[\omega]_\times^\top=-[\omega]_\times$이고, 대각이 0이며 자유 성분은 정확히 셋, $\omega$의 성분이다. 예: $\omega=(0,0,1)$이면 $[\omega]_\times(1,0,0)=(0,1,0)$으로 $\omega\times(1,0,0)$과 같다. 부호 패턴은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §1]]에서 전개한다.
  - **트위스트의 완전한 정의.** 두 부분을 가진 6차원 벡터 $\mathcal{V}=(\omega,v)$다. 각속도 $\omega$, 그리고 *지금 프레임 원점에 있는* 물체 점의 속도인 선형 부분 $v$(물체가 실제로 그 점을 차지하든 아니든). 그러면 모든 물체 점 $p$는
    $$\dot p=v+\omega\times p$$
    로 움직인다. 강체 속도는 원점 점의 속도에 그 둘레의 회전을 더한 것이기 때문이다. 예: $q=(1,0,0)$을 지나는 수직축 둘레로 $\omega=(0,0,1)$로 도는 관절은 $v=-\omega\times q=(0,-1,0)$이다. 축 위의 점은 $(0,-1,0)+(0,1,0)=0$을 받아 당연히 가만히 있고, 점 $(2,0,0)$은 $(0,1,0)$을 받는다. 반례: $v$를 도구 끝 속도로 읽는 것. 끝이 프레임 원점에 있을 때만 참이다. 그 원점이 공간 원점인지 바디 원점인지는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §3]]에서, 한 운동의 두 기술은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동 §4]]에서 다룬다.
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

**자세와 속도는 다른 질문이다.** 자세는 프레임이 지금 어디에 있는지, 트위스트는 강체 운동이 순간적으로 어떻게 변하는지 말한다. 유한 회전은 보통 행렬 성분이나 오일러 각을 더해 얻지 못한다. 회전은 곱으로 합성하고 순서가 중요하다. 미소 운동 근사는 미분할 수 있는 국소 선형 언어를 제공한다.

> [!example] 축에서 $T$로, 다시 축으로
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
> ([[04-robotics/modern-robotics/ch04-forward-kinematics|순기구학]])과 pose-error IK가 쓰는 정확한 다리다.

트위스트의 선형 성분도 기준 프레임과 원점에 달려 있다. 같은 회전체라도 축에서 떨어진 거리에 따라 점 속도가 다르다. 뒤쪽 성분을 도구 끝의 병진 속도로 읽기 전에 바디·공간 프레임 중 어디서 표현했고 원점이 어디인지 정한다. 자세한 구분은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|강체 운동]]에서 다룬다.

**이해 확인.** 기준 프레임을 바꾸면 물리 운동은 같고 트위스트 좌표가 바뀐다. 새 운동 명령이 아니라 좌표 변환이다. 프레임 없는 속도 벡터가 불완전한 로봇 인터페이스인 이유다.

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

Tier B. **P2**, $\theta=(0^\circ,90^\circ)$. 이 페이지 §3–4. 평면이므로 $R=R_z(\theta_1+\theta_2)$.

1. **그리기.** 원점의 베이스 프레임과 $(1,1)$의 말단 프레임. 둘째 링크는 수직: 말단 $x$축이 $+y$. 두 원점을 기입.
2. **유도.** $T_{\mathrm{base}\leftarrow\mathrm{tip}}$을 $4\times 4$ 동차행렬로. 둘째 링크의 회전은 $z$ 둘레 $90^\circ$, 평행이동은 말단 $(1,1,0)$.
3. **해석.** $\mathrm{Ad}_T$는 트위스트 하나를 다른 프레임으로 다시 쓴다. $J$는 이 자세에서 $\dot\theta$를 트위스트로 보낸다. 같은 행렬인가? 속도 프레임을 바꾸면 $\mathrm{Ad}_T$는 $J$의 한 열에 무엇을 하는가?

> [!tip]- 정답 · Solutions
> 1. 베이스 $(0,0)$, 엘보 $(1,0)$, 말단 $(1,1)$. $x_{\mathrm{tip}}$은 위, $y_{\mathrm{tip}}$은 왼쪽.
> 2. $R_z(90^\circ)=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$, $p=(1,1,0)$,
>    $T=\begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$.
> 3. 같은 사상이 아니다. $J$는 자세에 의존하며 관절 스크류를 쌓고, $\mathrm{Ad}_T$는 트위스트 하나의 프레임 변환이다. 속도 프레임을 바꾸면 $J$의 열에 $\mathrm{Ad}$를 왼쪽 곱할 뿐, $J$를 대체하지 않는다.

### 로보틱스 다리

여기서의 회전·변환 표기는 [[04-robotics/modern-robotics/index|Modern Robotics 요약]] 전체와 [[04-robotics/geometric-perception-calibration|3.5 기하 인식]]의 extrinsics가 그대로 사용하며, [[04-robotics/state-estimation-slam|SLAM·위치 추정]]과 [[04-robotics/robot-systems-deployment|로봇 시스템]]의 시간 인덱스 TF 트리에서 실전이 된다.
