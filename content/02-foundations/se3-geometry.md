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

*[[02-foundations/rl-basics|7. RL Basics]] gave you the grammar of states and actions. This page gives the space a robot's states and
actions are written in. Then [[02-foundations/ml-practice|9. ML Practice]] is how to read a claim that such a policy works.*

Every robot action, camera pose, and 3D reconstruction in this wiki lives in SE(3) — the
space of rigid-body poses. This page is the working set for reading VLA action spaces and
3D vision papers; the full treatment (screws, exponential coordinates) lives in
[[04-robotics/modern-robotics-book|Modern Robotics ch. 3]].

### 1. Rotations are matrices with rules

- A 3D rotation is a matrix $R \in \mathbb{R}^{3\times 3}$ with $R^\top R = I$ and
  $\det R = +1$ — the set of all such matrices is the **group SO(3)**. ("Group" is the
  algebraic word for a set closed under composition where every element has an inverse:
  a rotation times a rotation is a rotation, and every rotation can be undone. That is all
  the word carries here.)
- Consequences: columns are an orthonormal frame (the rotated x/y/z axes);
  $R^{-1} = R^\top$ (undoing a rotation is free); rotations compose by multiplication,
  and **order matters** ($R_1 R_2 \ne R_2 R_1$ — rotate your phone about two axes in both
  orders to feel it).
- 2D worked example: $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$
  — check $R(90°)\,(1,0)^\top = (0,1)^\top$. All of SO(3) is this idea, three axes at once.
- **Order matters — with numbers, so you never have to trust the phone demo.** Let
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
- **Checking a matrix is a rotation**, which you should do whenever you build one: columns
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

  must have length 1, be mutually perpendicular, and $\det = +1$. For $R_z(90°)$: columns are
  $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ — unit length ✓, pairwise dot products all 0 ✓, and
  $\det = +1$ ✓. A $\det$ of $-1$ means you built a **reflection**, which mirrors the robot
  rather than turning it — a real and common bug when converting conventions.

### 2. The four ways papers write rotations

| Representation | Numbers | Strengths | The catch |
|---|---|---|---|
| Rotation matrix | 9 | composition, no singularities | redundant (6 constraints) |
| Euler angles (roll-pitch-yaw) | 3 | human-readable | **gimbal lock**; order conventions bite |
| Axis-angle $(\hat\omega, \theta)$ | 3 | minimal, geometric | composition is awkward |
| **Quaternion** $(w, x, y, z)$ | 4 | no singularities, cheap composition, interpolation (slerp) | double cover: $q$ and $-q$ are the same rotation |

- Learning-specific fact worth knowing: all 3- and 4-number representations are
  *discontinuous* as targets for neural networks — which is why many robot-learning papers
  regress a **6D representation** (first two columns of $R$, then Gram-Schmidt) instead.

### 3. Poses: SE(3) and homogeneous transforms

- A **pose** = rotation + position, packaged as
  $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$ (a $4\times4$ matrix).
- Composition is matrix multiplication: $T_{AC} = T_{AB}\,T_{BC}$ — read subscripts like
  units and they cancel. Inverse: $T^{-1} = \begin{pmatrix} R^\top & -R^\top p \\ 0 & 1 \end{pmatrix}$.

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
  the offset *without* rotating gives $(3,0,0)$ — a metre away, in the wrong direction.
  That rotation of the offset is the step people forget, and it is exactly what the matrix
  form does for you automatically — which is the entire reason poses are written as $4\times4$ matrices instead
  of an $(R, p)$ pair you combine by hand.
- **Frames discipline** is 90% of not making sign errors: every quantity has a frame
  (world, base, camera, end-effector); write it down. "Where is the camera?" = $T_{world \leftarrow cam}$.

### 4. Velocity and small motions (the on-ramp to Modern Robotics)

- Angular velocity $\omega$ is a vector (axis × speed); rigid-body velocity = **twist**
  $(\omega, v)$ — six numbers, and the reason end-effector velocity commands are 6-DoF.
- Small rotation ≈ $I + [\hat\omega\theta]_\times$. Why skew-symmetric? A rotation keeps
  lengths fixed, so $R^\top R = I$; differentiating at $R=I$ gives $\dot R + \dot R^\top = 0$,
  i.e. the generator $\dot R$ *must* be skew — its off-diagonal $\pm$ entries are exactly the
  components of the rotation axis $\omega$ (that is what $[\cdot]_\times$ packs). Rotations are
  thus *locally linear*, which is what lets Jacobians ([[02-foundations/calculus-backprop|2. Calculus]])
  map joint rates to end-effector twists, and what the exponential map formalizes
  ([[04-robotics/modern-robotics-book|MR ch. 3]]).

### 5. Where this appears in the wiki

- **VLA action spaces**: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]'s 7-DoF action = end-effector
  position (3) + rotation (3) + gripper (1); [[01-canonical-papers/notes/4-vla/pi0|π0]] outputs
  joint-space chunks — reading these requires exactly this page. Turning an end-effector
  pose back into joint commands is inverse kinematics
  ([[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]), whose many-solutions
  structure is the classical face of the same multimodality generative policies handle.
- **3D vision**: camera pose in [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]
  is $T \in SE(3)$; "pose estimation" = regressing this matrix.
- **Sim & digital twins**: every simulator state and BIM-robot registration is a stack of
  $T$'s ([[05-construction-robotics/index|construction]]).

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

### Robotics bridge

This notation is used verbatim throughout the [[04-robotics/modern-robotics/index|Modern Robotics summary]] and the extrinsics of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]]; it becomes operational in [[04-robotics/state-estimation-slam|SLAM and localization]] and the time-indexed TF trees of [[04-robotics/robot-systems-deployment|Robot Systems]].

## 한국어

*[[02-foundations/rl-basics|7. RL 기초]]가 상태와 행동의 문법을 줬다. 이 페이지는 로봇의 상태와 행동이 적히는 공간을 준다.
그다음 [[02-foundations/ml-practice|9. ML 실무]]는 그런 정책이 작동한다는 주장을 어떻게 읽을 것인가다.*

이 위키의 모든 로봇 행동, 카메라 자세, 3D 재구성은 SE(3) — 강체 자세의 공간 — 에 산다.
이 페이지는 VLA 행동 공간과 3D 비전 논문을 읽기 위한 작업 세트다; 완전한 전개(스크류,
지수 좌표)는 [[04-robotics/modern-robotics-book|Modern Robotics 3장]]의 몫이다.

### 1. 회전은 규칙 있는 행렬이다

- 3D 회전은 $R^\top R = I$이고 $\det R = +1$인 행렬 $R \in \mathbb{R}^{3\times 3}$ —
  이런 행렬 전체의 집합을 **군**(group) SO(3)라고 부른다. ("군"은 합성에 대해 닫혀 있고 모든
  원소에 역원이 있는 집합을 가리키는 대수학 용어다: 회전 × 회전 = 회전이고, 모든 회전은
  되돌릴 수 있다. 여기서 이 단어가 담는 뜻은 그것이 전부다.)
- 따름정리: 열들은 정규직교 프레임(회전된 x/y/z 축)이다; $R^{-1} = R^\top$(회전 되돌리기는
  공짜); 회전은 곱셈으로 합성되고 **순서가 중요하다** ($R_1 R_2 \ne R_2 R_1$ — 폰을 두 축으로
  순서 바꿔 돌려보면 몸으로 느껴진다).
- 2D 계산 예제: $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$
  — $R(90°)\,(1,0)^\top = (0,1)^\top$ 검산. SO(3) 전체가 이 아이디어를 세 축으로 한 것이다.
- **순서가 중요하다 — 숫자로, 폰 시연을 믿지 않아도 되게.**
  $$R_z(90°) = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}, \qquad R_x(90°) = \begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$$
  로 두고, 점 $p = (1,0,0)$ — x축의 끝 — 을 따라가 보자.
  - $R_z$를 **먼저**, 그다음 $R_x$: $R_z p = (0,1,0)$, 그리고 $R_x(0,1,0) = (0,0,1)$.
    점이 **z**축 위에 도착한다.
  - $R_x$를 **먼저**, 그다음 $R_z$: $R_x p = (1,0,0)$(x축 *위의* 점은 x축 회전으로 움직이지
    않는다), 그리고 $R_z(1,0,0) = (0,1,0)$. 점이 **y**축 위에 도착한다.

  같은 회전 둘, 전혀 다른 두 위치. 미묘한 일은 하나도 없다: 두 번째 회전은 첫 번째 회전이
  *남겨둔* 자리에 작용한다. 논문의 $R_{world}R_{body}$와 $R_{body}R_{world}$가 서로 다른 운동을
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

  기술하는 이유이고, 로보틱스의 모든 규약 불일치가 결국 이것인 이유다.
- **어떤 행렬이 회전인지 확인하기** — 회전 행렬을 만들 때마다 해야 한다: 열의 길이가 1이고,
  서로 수직이며, $\det = +1$이어야 한다. $R_z(90°)$라면 열이 $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ —
  길이 1 ✓, 서로의 내적이 모두 0 ✓, $\det = +1$ ✓. $\det$가 $-1$이면 **반사**를 만든 것이고,
  로봇을 돌리는 대신 거울에 비춘 셈이다 — 규약 변환에서 실제로 자주 나는 버그다.

### 2. 논문이 회전을 쓰는 네 가지 방법

| 표현 | 숫자 | 강점 | 함정 |
|---|---|---|---|
| 회전 행렬 | 9 | 합성 쉬움, 특이점 없음 | 중복 (제약 6개) |
| 오일러 각 (roll-pitch-yaw) | 3 | 사람이 읽기 쉬움 | **짐벌 락**; 순서 규약이 문다 |
| 축-각 $(\hat\omega, \theta)$ | 3 | 최소, 기하적 | 합성이 어색 |
| **쿼터니언** $(w, x, y, z)$ | 4 | 특이점 없음, 싼 합성, 보간(slerp) | 이중 덮개: $q$와 $-q$가 같은 회전 |

- 학습 특화 상식: 3·4개 숫자 표현은 모두 신경망의 회귀 타깃으로서 *불연속*이다 — 많은
  로봇 학습 논문이 대신 **6D 표현**($R$의 앞 두 열 + Gram-Schmidt)을 회귀하는 이유다.

### 3. 자세: SE(3)와 동차 변환

- **자세** = 회전 + 위치를 하나로 포장:
  $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$ ($4\times4$ 행렬).
- 합성은 행렬곱: $T_{AC} = T_{AB}\,T_{BC}$ — 아래 첨자를 단위처럼 읽으면 약분된다.
  역: $T^{-1} = \begin{pmatrix} R^\top & -R^\top p \\ 0 & 1 \end{pmatrix}$

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
  $(3,0,0)$ — 1 m 떨어진, 방향이 틀린 자리다. 사람들이 빼먹는 단계가 바로 그 오프셋 회전이고,
  행렬 형태가 자동으로 해주는 일이 정확히 그것이다 — pose를 $(R, p)$ 쌍으로 들고 손으로
  합치는 대신 $4\times4$ 행렬로 쓰는 이유 전부가 이것이다.
- **프레임 규율**이 부호 실수 안 하기의 90%다: 모든 양에는 프레임(월드, 베이스, 카메라,
  말단)이 있다; 항상 적어라. "카메라가 어디 있나?" = $T_{world \leftarrow cam}$.

### 4. 속도와 미소 운동 (Modern Robotics로 가는 진입로)

- 각속도 $\omega$는 벡터(축 × 속력); 강체 속도 = **twist** $(\omega, v)$ — 여섯 숫자이고,
  말단 속도 명령이 6자유도인 이유다.
- 미소 회전 ≈ $I + [\hat\omega\theta]_\times$. 왜 반대칭인가? 회전은 길이를 보존하므로
  $R^\top R = I$; $R=I$에서 미분하면 $\dot R + \dot R^\top = 0$, 즉 생성원 $\dot R$는 *반드시*
  반대칭이고, 그 비대각 $\pm$ 성분이 정확히 회전축 $\omega$의 성분이다($[\cdot]_\times$가
  담는 것). 그래서 회전은 *국소적으로 선형*이고,
  이것이 야코비안([[02-foundations/calculus-backprop|2. 미적분]])이 관절 속도를 말단
  twist로 사상할 수 있는 이유이자, 지수 사상이 정식화하는 내용이다
  ([[04-robotics/modern-robotics-book|MR 3장]]).

### 5. 이 위키에서 등장하는 곳

- **VLA 행동 공간**: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]의 7자유도 행동 = 말단 위치(3) +
  회전(3) + 그리퍼(1); [[01-canonical-papers/notes/4-vla/pi0|π0]]는 관절 공간 청크를 출력 —
  이들을 읽는 데 정확히 이 페이지가 필요하다. 말단 pose를 다시 관절 명령으로 바꾸는 것이
  [[04-robotics/modern-robotics/ch06-inverse-kinematics|역기구학(MR 6장)]]이고, 그 다해(多解)
  구조가 생성형 정책이 다루는 바로 그 다봉성의 고전적 얼굴이다.
- **3D 비전**: [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]의
  카메라 자세가 $T \in SE(3)$; "자세 추정" = 이 행렬의 회귀.
- **시뮬레이션과 디지털 트윈**: 모든 시뮬레이터 상태와 BIM-로봇 정합이 $T$들의 스택이다
  ([[05-construction-robotics/index|건설]]).

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

### 로보틱스 다리

여기서의 회전·변환 표기는 [[04-robotics/modern-robotics/index|Modern Robotics 요약]] 전체와 [[04-robotics/geometric-perception-calibration|3.5 기하 인식]]의 extrinsics가 그대로 사용하며, [[04-robotics/state-estimation-slam|SLAM·위치 추정]]과 [[04-robotics/robot-systems-deployment|로봇 시스템]]의 시간 인덱스 TF 트리에서 실전이 된다.
