---
title: "MR Ch.04 — Forward Kinematics"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.4** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need screw axes and the adjoint from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3–4]] and the closed form of $e^{[\mathcal{S}]\theta}$ from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]], plus multiplying 4×4 homogeneous transforms ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §3]]); P2's forward kinematics by plain geometry ([[02-foundations/manipulator-kinematics-dynamics|10 §1]]) is the check this page's formula must reproduce. The object is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled).
> [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3–4]]의 스크류 축과 수반(adjoint), [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §5]]의 $e^{[\mathcal{S}]\theta}$ 닫힌 형태, 그리고 4×4 동차 변환의 곱([[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §3]])을 쓸 수 있어야 한다. 순수 기하로 구한 P2의 순기구학([[02-foundations/manipulator-kinematics-dynamics|10 §1]])이 이 페이지의 공식이 재현해야 할 검산이다. 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치(plant, 제어에서 제어 대상인 시스템을 부르는 말) **P2**다.

## English

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] forward kinematics (FK) is the manipulation layer's first computation — joint angles in, tool pose out — and in *"install that panel on the frame"* it serves *move the component*: every control tick, collision check and inverse-kinematics (IK) iteration asks where the tool is at the current $\theta$ (its chip sits in the manipulation band of the [[physical-ai-map|Physical AI Map]]). A wrong FK gives no warning sign: read the elbow's screw where the arm stands at $(90°, 90°)$ instead of at home and the product puts the tip at $(-3, 1)$, $2\,\mathrm m$ from the true $(-1, 1)$, with the orientation still exactly right; swap the two exponentials and it lands at $(-1, -1)$, again with the right orientation (§1's box and the Worked case, both drawn in §2's figure). Later pages call it constantly — [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §1]] turns its screws into Jacobian columns, [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6 §2]] evaluates it at every Newton step and builds its pose error from $M$ and the body screws, [[04-robotics/ros2/describing-a-robot|25.6 §2]] stores the same chain as the link frames of a URDF, the robot-description file that ROS reads, and [[04-robotics/capstone-panel-contact|26. Capstone §6]] calls it at every step of its loop, for the collision margin and for the tip that presses — all in block 2 of the dissertation path ([[07-research-program/index|7 §8]]), where this page takes robotics sessions 10–11. After it you can read an arm's home configuration and screw axes, evaluate $T(\theta)$ in space and body form, and check the result against geometry.

> [!note] First pass · 처음이라면
> One session, robotics session 10: the Running object, the picture, §1 with its three boxes, §2's worked example with its figure, and the Worked case — take Step 3's matrix as given from ch.3 §5, and leave Step 5's body form for later. End it by checking, page closed, that the product of exponentials (PoE) and geometry agree on the tip at $(0°, 90°)$ and at $(90°, 90°)$, by saying why the swapped order moves the tip $2\,\mathrm m$ without changing $R$, and with self-check 1. Session 11 is the rest of the self-check and the problem set; the collapsed *Deeper* notes — D-H and URDF in §1, the body form in the Worked case — are the second pass.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], one of the wiki's six frozen *plants* (control's word for the system being controlled): the planar 2R arm — two revolute joints — with $L_1 = L_2 = 1\,\mathrm m$, $\theta_1$ measured from the $+x$ axis and $\theta_2$ relative to link 1, and the catalog pose $\theta = (0°, 90°)$ with the tip at $(1, 1)$. Its forward kinematics by plain geometry — the elbow plus the forearm — is already derived in [[02-foundations/manipulator-kinematics-dynamics|10 §1]]; this page writes the same map as a product of exponentials, the form that carries over unchanged to a six-joint arm. The frames are those of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3]]: the space frame $\{s\}$ at the shoulder, and the body frame $\{b\}$ on the tool at the tip, with $\hat x_b$ along the forearm. $M$ below is MR's letter for the tool's pose at $\theta = 0$, unrelated to the mass matrix $M(\theta)$ of 10.

*Scope: this page teaches the forward kinematics of an open chain as a product of exponentials, in space and body form, on P2. It does not teach inverse kinematics ([[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6]]), velocities and Jacobians ([[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]]), or the Denavit–Hartenberg convention, which §1's Deeper note only places.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 322" style="max-width:100%;height:auto" role="img" aria-label="P2 drawn twice: the home pose dashed with its two screw axes at q1 and q2, and the pose (0°, 90°) solid, sharing link 1; frames at the base, at q2 and at the tool tip; beside it the matrix route and the geometric route both give the tip (1, 1).">
  <defs><marker id="mr04hdE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <line x1="28.7" y1="196" x2="341.4" y2="196" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="70,196 188,196 306,196" fill="none" stroke="currentColor" stroke-width="2.6" stroke-dasharray="7 5" opacity="0.45"/>
  <polyline points="70,196 188,196 188,78" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.5"/>
  <circle cx="306" cy="196" r="4" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="188" cy="78" r="4.5" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1.7" marker-end="url(#mr04hdE)"><line x1="78" y1="196" x2="105.4" y2="196"/><line x1="70" y1="188" x2="70" y2="160.6"/><line x1="196" y1="196" x2="223.4" y2="196"/><line x1="188" y1="188" x2="188" y2="160.6"/><line x1="188" y1="73" x2="188" y2="42.6"/><line x1="183" y1="78" x2="152.6" y2="78"/></g>
  <circle cx="70" cy="196" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="70" cy="196" r="2" fill="currentColor"/>
  <circle cx="188" cy="196" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="188" cy="196" r="2" fill="currentColor"/>
  <line x1="352" y1="14" x2="352" y2="274" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="103.4" y="189" text-anchor="middle">x̂<tspan dy="3.5">s</tspan></text>
    <text x="62" y="166.6" text-anchor="end">ŷ<tspan dy="3.5">s</tspan></text>
    <text x="58" y="187" text-anchor="end" font-size="12">{s}</text>
    <text x="220.4" y="211" text-anchor="middle">x</text>
    <text x="181" y="165.6" text-anchor="end">y</text>
    <text x="201" y="180" font-size="12">{q<tspan dy="3.5">2</tspan><tspan dy="-3.5">}</tspan></text>
    <text x="195" y="50.6">x̂<tspan dy="3.5">b</tspan></text>
    <text x="148.6" y="71" text-anchor="end">ŷ<tspan dy="3.5">b</tspan></text>
    <text x="197" y="94" font-size="12">tool {b}</text>
    <text x="306" y="166" text-anchor="middle" opacity="0.8">home, θ = 0</text>
    <text x="306" y="181" text-anchor="middle" opacity="0.8">tip (2, 0) → M</text>
    <text x="197" y="124">θ = (0°, 90°), solid</text>
    <text x="197" y="139">tip (1, 1)</text>
    <text x="70" y="226" text-anchor="middle">S<tspan dy="3.5">1</tspan><tspan dy="-3.5">: q</tspan><tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="70" y="242" text-anchor="middle">ω̂<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1)</tspan></text>
    <text x="70" y="258" text-anchor="middle">v<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="188" y="226" text-anchor="middle">S<tspan dy="3.5">2</tspan><tspan dy="-3.5">: q</tspan><tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="188" y="242" text-anchor="middle">ω̂<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1)</tspan></text>
    <text x="188" y="258" text-anchor="middle">v<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (0, −1, 0)</tspan></text>
    <text x="12" y="290" opacity="0.85">Dashed = home pose, where M and the screw axes S<tspan dy="3.5">1</tspan><tspan dy="-3.5">, S</tspan><tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">are read (they stay there).</tspan></text>
    <text x="12" y="306" opacity="0.85">Solid = the pose being evaluated. θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 0, so the two arms share link 1.</tspan></text>
    <text x="364" y="26" font-size="12">Two routes, one tip</text>
    <text x="364" y="52">Matrix route (PoE)</text>
    <text x="372" y="69">T = exp([S<tspan dy="3.5">1</tspan><tspan dy="-3.5">]θ</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">) exp([S</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">]θ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">) M</tspan></text>
    <text x="372" y="86">θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 0, so exp([S</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">]·0) = I</tspan></text>
    <text x="372" y="103">T = exp([S<tspan dy="3.5">2</tspan><tspan dy="-3.5">]·π/2) M</tspan></text>
    <text x="372" y="120">→ p = (1, 1, 0), R = R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(90°)</tspan></text>
    <text x="364" y="148">Geometric route</text>
    <text x="372" y="165">elbow + forearm</text>
    <text x="372" y="182">= (1, 0) + (0, 1) = (1, 1)</text>
    <text x="364" y="210">The two lines must agree.</text>
  </g>
</svg>

Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] twice on one set of axes: dashed at home, both links along $+\hat x$ and the tip at $(2,0)$, where $M$ and the screw axes are read; solid at the evaluated pose $\theta = (0^\circ, 90^\circ)$, sharing link 1 with the home arm because $\theta_1 = 0$. The screw axes sit on the home arm only — $\mathcal{S}_1$ through $q_1 = (0,0,0)$ with $v_1 = (0,0,0)$, $\mathcal{S}_2$ through $q_2 = (1,0,0)$ with $v_2 = (0,-1,0)$ — and frames sit at the base, at $q_2$ and at the tool tip. Beside the arms, the matrix route $T = e^{[\mathcal{S}_2]\pi/2}M$ and the geometric route, elbow $+$ forearm $= (1,0) + (0,1)$, agree on the tip $(1,1)$ with $R = R_z(90^\circ)$.

### 1. The product of exponentials

Every control tick the encoders report $\theta$, and the controller, the collision checker and the IK loop all ask the same question: given the joint angles, where is the tool? This section answers it with one formula built from two ingredients that are read once, at home.

$$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$

Read it right-to-left, because the factor next to $M$ acts first: start at the home pose $M$ (all joints zero), then each joint screws everything downstream of it. Two ingredients only: the home pose, and one screw axis per joint *written in the fixed frame at the home position*. No intermediate link frames are needed; the classical convention that does use them, and the robot-description files that still chain them, are placed in the Deeper note below.

**Why axes read once at home serve every $\theta$.** Read the product from the right. $e^{[\mathcal{S}_2]\theta_2}$ acts first and turns the forearm about the elbow axis through $(1, 0, 0)$ while joint 1 has not yet acted, so the elbow still stands exactly where the home axis says; then $e^{[\mathcal{S}_1]\theta_1}$ carries the whole bent arm, elbow axis included, about the base. At $(90°, 90°)$ the tip goes $(2,0) \to (1,1) \to (-1,1)$, the three panels of §2's figure. (The **body form** $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots$ expresses the same map with the axes written in the end-effector frame.)

> [!note]- Deeper · 더 깊이
> **D-H parameters and URDF.** Needing no intermediate link frames is the advantage over Denavit–Hartenberg (D-H), the classical convention that attaches a frame to every link and describes each joint by four numbers relative to the previous link's frame — link length, link twist (an angle between neighbouring joint axes, not ch.3's twist), offset and joint angle; MR Appendix C, and no wiki page covers it — and it is why MR's software library uses PoE. Mainstream robot formats still chain parent-to-child link frames: URDF, the XML robot description that ROS reads, stores an arm as a tree of link frames joined by joints ([[04-robotics/ros2/describing-a-robot|25.6 §2]]).

> **Forward kinematics, defined.** **Forward kinematics** is a *map* from joint values to the pose of the tool, and three conditions make it one. Its **input is the joint vector alone**, $\theta \in \mathbb{R}^n$: no velocities, torques or history. Its **output is the tool frame's pose in a chosen task space** — MR calls it the tool's *configuration*, a word this wiki keeps for the whole robot's joint values ([[04-robotics/modern-robotics/ch02-configuration-space|ch.2 §1]]): in general the pose $T_{sb} \in SE(3)$ of the frame $\{b\}$ in a fixed frame $\{s\}$, or task coordinates $x = f(\theta)$ such as the tip position alone when only position matters, so the frames and the task coordinates belong to the definition. And **for an open chain it is single-valued**: each $\theta$ gives exactly one output, because rigid links at fixed joint values leave nothing free; a closed chain can have several (MR ch.7).
>
> $$\theta \mapsto T_{sb}(\theta) = \begin{pmatrix} R(\theta) & p(\theta) \\ 0 & 1 \end{pmatrix} \in SE(3), \qquad x = f(\theta) \in \mathbb{R}^m$$
>
> where $R(\theta)$ and $p(\theta)$ are the tool frame's orientation and origin in $\{s\}$ and $f$ writes the same pose in the task's $m$ coordinates; $SE(3)$ is the general case because a rigid tool has a direction as well as a location.
>
> - **Example**: P2 with $\{s\}$ at the shoulder and $\{b\}$ at the tip sends $(0^\circ, 90^\circ)$ to $p = (1,1,0)$, $R = R_z(90^\circ)$ and $(90^\circ, -90^\circ)$ to $p = (1,1,0)$, $R = I$; in the position task $f(\theta) = (x, y)$ both go to $(1,1)$.
> - **Non-example**: the reverse map, from the tip back to the joints. Kinematics is easily pictured as one invertible relation, but this map is not a function: $(1,1)$ has the two preimages above and $(2.5, 0)$ has none. That is ch.6's problem, and it is why FK can be called blindly at any $\theta$ while IK must choose among branches or report that none exists.

> **Home configuration, defined.** The **home configuration** $M$ is *one constant element of* $SE(3)$: the pose of the tool frame $\{b\}$ in the fixed frame $\{s\}$ with every joint at zero. Three conditions pin it down. **Every joint value is zero**, $\theta = 0$, with each joint's zero and positive direction declared first. It is **the tool frame seen from the fixed frame**, not a link frame. And it is **constant**: fixed once $\{s\}$, $\{b\}$ and the joint zeros are chosen, never updated as the robot moves.
>
> $$M = T_{sb}(0) = \begin{pmatrix} R_{sb}(0) & p_{sb}(0) \\ 0 & 1 \end{pmatrix} \in SE(3)$$
>
> where $R_{sb}(0)$ and $p_{sb}(0)$ are the tool frame's orientation and origin at the zero position; $M$ sits at the right end of the space form because every factor is a screw motion written in the fixed frame, and a motion written in $\{s\}$ multiplies from the left (MR §3.3.1); the body form's screws are written in $\{b\}$, which is why $M$ moves to their left.
>
> - **Example**: P2 has both links along $+\hat x$ at zero, so $R = I$ and $p = (2,0,0)$, the $M$ of Step 1.
> - **Non-example**: the catalog pose $T(0^\circ, 90^\circ)$, "where the robot usually is". Put in place of $M$ and evaluated at that same $\theta$, it lets the elbow turn the forearm a second time: the tip lands at $(0,0)$ with $R = R_z(180^\circ)$, $1.414\,\mathrm{m}$ from the true $(1,1)$. $M$ is read once, at zero; read it wherever the arm happens to stand and every later FK call inherits the mistake.

> **Product of exponentials, defined.** The **product-of-exponentials (PoE) formula** is a *representation of the forward-kinematics map*: one SE(3) exponential per joint, multiplied into $M$. Three conditions define it. Its ingredients are **the home configuration** $M$ and **one screw axis per joint, read at the zero position**: $\mathcal{S}_i$ in $\{s\}$ for the space form, $(\hat\omega_i,\ -\hat\omega_i \times q_i)$ for a revolute joint and $(0,\ \hat v_i)$ for a prismatic one with unit direction $\hat v_i$, and $\mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\mathcal{S}_i$ in $\{b\}$ for the body form. **The factors run in joint order**, $1$ to $n$ from left to right, in both forms. And **$M$ sits on the right in the space form and on the left in the body form**.
>
> $$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\cdots e^{[\mathcal{S}_n]\theta_n}M = M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}, \qquad \mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\,\mathcal{S}_i$$
>
> where each factor is the screw motion of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]]; axes read once at home serve every $\theta$, because in the space form each exponential acts before the joints nearer the base have carried its axis away (MR §4.1).
>
> - **Example**: P2's $\mathcal{S}_1 = (0,0,1;\,0,0,0)$, $\mathcal{S}_2 = (0,0,1;\,0,-1,0)$, $\mathcal{B}_1 = (0,0,1;\,0,2,0)$, $\mathcal{B}_2 = (0,0,1;\,0,1,0)$: both forms put the tip at $(-1,1)$ with $R_z(180^\circ)$ at $(90^\circ, 90^\circ)$.
> - **Non-example**: $\mathcal{S}_2$ read from the arm where it stands. At $(90^\circ, 90^\circ)$ the elbow is at $(0,1)$, giving $(0,0,1;\,1,0,0)$, and the product puts the tip at $(-3,1)$, $2\,\mathrm{m}$ from $(-1,1)$, with the orientation still exactly $R_z(180^\circ)$. On a planar arm every factor turns about $\hat z$, so the rotation block is $R_z(\theta_1 + \theta_2)$ whichever axes are used; only the position column can expose a misplaced screw.

### 2. Worked example at (90°, 90°)

A formula is trusted only once it has been checked against something independent, so this section runs the recipe on the 2R arm at a pose where both joints move, and checks the answer against plain geometry.

Links $L_1 = L_2 = 1$, both stretched along $+\hat x$ at home. The general recipe, then the numbers:

**Step 1 — home pose $M$.** End-effector at $(2, 0, 0)$, aligned with the base:
$$M = \begin{pmatrix} 1&0&0&2\\ 0&1&0&0\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**Step 2 — screw axis of joint 1.** Axis direction $\hat\omega_1 = (0,0,1)$; a point on
the axis $q_1 = (0,0,0)$; linear part $v_1 = -\hat\omega_1 \times q_1 = (0,0,0)$.
So $\mathcal{S}_1 = (0,0,1;\; 0,0,0)$.

**Step 3 — screw axis of joint 2.** $\hat\omega_2 = (0,0,1)$; $q_2 = (1,0,0)$;
$v_2 = -\hat\omega_2 \times q_2 = -(0,1,0) = (0,-1,0)$.
So $\mathcal{S}_2 = (0,0,1;\; 0,-1,0)$.

**Step 4 — evaluate at $\theta_1 = \theta_2 = 90°$.**
$e^{[\mathcal{S}_2]\,90°}$ rotates everything by 90° about the $\hat z$ axis through
$q_2 = (1,0,0)$. Apply it to $M$: the end-effector sits at $p - q_2 = (1,0,0)$ relative to
the axis; rotated 90° it becomes $(0,1,0)$; adding $q_2$ back gives $(1,1,0)$, with
orientation $R_z(90°)$. Then $e^{[\mathcal{S}_1]\,90°}$ rotates that result 90° about the
origin: $(1,1,0) \to (-1,1,0)$, orientation $R_z(180°)$:
$$T(90°, 90°) = \begin{pmatrix} -1&0&0&-1\\ 0&-1&0&1\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**Step 5 — sanity check against plain geometry.** $\theta_1 = 90°$ points link 1 along
$+\hat y$ (elbow at $(0,1)$); $\theta_2 = 90°$ adds another 90°, pointing link 2 along
$-\hat x$; tip $= (0,1) + (-1,0) = (-1, 1)$, total orientation $180°$. **Same answer.**
Do this double-check on every robot you model — geometric FK and PoE FK must agree.

The figure draws Steps 4–5 and, below them, two wrong products at the same $\theta$: the screw axis misread in §1's box, and the swapped order that Step 6 of the Worked case below comes back to.

<svg viewBox="0 0 560 318" style="max-width:100%;height:auto" role="img" aria-label="P2 in three panels: home, after the elbow exponential with the tip at (1, 1), and after the shoulder exponential with the tip at (−1, 1); below, the swapped product's tip (−1, −1) and the product with the elbow axis read where the arm stands, tip (−3, 1), beside the true tip, all three with orientation R_z(180°).">
  <defs><marker id="mr04peE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <line x1="12" y1="118" x2="180" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="71.8,118 115.8,118 159.8,118" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6"/>
  <circle cx="71.8" cy="118" r="3.4" fill="currentColor"/>
  <circle cx="115.8" cy="118" r="3" fill="currentColor"/>
  <circle cx="159.8" cy="118" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="164.8" y1="118" x2="183.8" y2="118" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr04peE)"/>
  <circle cx="71.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="115.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="196" y1="118" x2="364" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="255.8,118 299.8,118 343.8,118" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 4" opacity="0.45"/>
  <polyline points="255.8,118 299.8,118 299.8,74" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6"/>
  <circle cx="255.8" cy="118" r="3.4" fill="currentColor"/>
  <circle cx="299.8" cy="118" r="3" fill="currentColor"/>
  <circle cx="299.8" cy="74" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="299.8" y1="69" x2="299.8" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr04peE)"/>
  <circle cx="299.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="343.8,118 343.6,114.2 343.1,110.4 342.3,106.6 341.1,103 339.7,99.4 337.9,96 335.8,92.8 333.5,89.7 330.9,86.9 328.1,84.3 325,82 321.8,79.9 318.4,78.1 314.8,76.7 311.2,75.5 307.4,74.7 303.6,74.2 299.8,74" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr04peE)"/>
  <line x1="380" y1="118" x2="548" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="439.8,118 483.8,118 483.8,74" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 4" opacity="0.45"/>
  <polyline points="439.8,118 439.8,74 395.8,74" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6"/>
  <circle cx="439.8" cy="118" r="3.4" fill="currentColor"/>
  <circle cx="439.8" cy="74" r="3" fill="currentColor"/>
  <circle cx="395.8" cy="74" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="390.8" y1="74" x2="371.8" y2="74" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr04peE)"/>
  <circle cx="439.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="483.8,74 479.8,70.3 475.5,67 470.9,64.1 466.1,61.6 461.1,59.5 455.9,57.9 450.6,56.7 445.2,56 439.8,55.8 434.4,56 429,56.7 423.7,57.9 418.5,59.5 413.5,61.6 408.7,64.1 404.1,67 399.8,70.3 395.8,74" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr04peE)"/>
  <line x1="20" y1="245" x2="216" y2="245" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="160,245 160,205 120,205" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" opacity="0.55"/>
  <circle cx="160" cy="245" r="3.4" fill="currentColor"/>
  <circle cx="200" cy="245" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>
  <circle cx="160" cy="205" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 2"/>
  <circle cx="120" cy="205" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="115" y1="205" x2="98" y2="205" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr04peE)"/>
  <circle cx="120" cy="285" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 2"/>
  <line x1="115" y1="285" x2="98" y2="285" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr04peE)"/>
  <circle cx="40" cy="205" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 2"/>
  <line x1="35" y1="205" x2="18" y2="205" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr04peE)"/>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="1 3" opacity="0.8"><line x1="120" y1="211" x2="120" y2="279"/><line x1="94" y1="205" x2="46" y2="205"/></g>
  <g font-size="11" fill="currentColor">
    <text x="14" y="22" font-size="12">① home: M</text>
    <text x="14" y="135">tip (2, 0), R = I</text>
    <text x="14" y="150" opacity="0.8">axes S<tspan dy="3.5">1</tspan><tspan dy="-3.5">, S</tspan><tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">read here</tspan></text>
    <text x="198" y="22" font-size="12">② exp([S<tspan dy="3.5">2</tspan><tspan dy="-3.5">]·π/2) M</tspan></text>
    <text x="198" y="135">tip (1, 1), R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(90°)</tspan></text>
    <text x="198" y="150" opacity="0.8">elbow turns; joint 1 not yet</text>
    <text x="382" y="22" font-size="12">③ exp([S<tspan dy="3.5">1</tspan><tspan dy="-3.5">]·π/2) ②</tspan></text>
    <text x="382" y="135">tip (−1, 1), R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(180°)</tspan></text>
    <text x="382" y="150" opacity="0.8">the bent arm turns about the base</text>
    <text x="120" y="193" text-anchor="middle">true (−1, 1)</text>
    <text x="128" y="289">swapped order (−1, −1)</text>
    <text x="40" y="193" text-anchor="middle">(−3, 1)</text>
    <text x="14" y="225">S<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">read at (0, 1)</tspan></text>
    <text x="209" y="260" opacity="0.8">home axis q<tspan dy="3.5">2</tspan><tspan dy="-3.5"></tspan></text>
    <text x="125" y="237">2 m</text>
    <text x="76" y="200" text-anchor="middle">2 m</text>
    <text x="300" y="184" font-size="12">Two wrong products at (90°, 90°)</text>
    <text x="300" y="203">All three tool frames have R = R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(180°):</tspan></text>
    <text x="300" y="219">no orientation error, so only the</text>
    <text x="300" y="235">position column shows the mistake, 2 m each.</text>
    <text x="300" y="257">Swapped, the shoulder stands the arm up first</text>
    <text x="300" y="273">and the elbow factor turns it about (1, 0).</text>
    <text x="300" y="295">Read at (0, 1), the axis is carried by the</text>
    <text x="300" y="311">shoulder a second time.</text>
  </g>
</svg>

Top, the product at $(90°, 90°)$ read from the right: ① home, tip $(2, 0)$ with $R = I$; ② the elbow factor turns the forearm about $q_2 = (1, 0, 0)$ before joint 1 acts, tip $(1, 1)$ with $R_z(90°)$; ③ the shoulder factor turns the whole bent arm about the base, tip $(-1, 1)$ with $R_z(180°)$. Bottom, two wrong products at the same $\theta$: the swapped order puts the tip at $(-1, -1)$, and the elbow screw read where the elbow stands, through $(0, 1)$, puts it at $(-3, 1)$ — both $2\,\mathrm m$ off and both with the correct $R_z(180°)$, so only the position column shows the mistake.

### Worked case · 대상으로 한 번 끝까지

The same recipe on the catalog object, at the pose every later chapter quotes: plant **P2** at $\theta = (0^\circ, 90^\circ)$ ([[02-foundations/lab-plants|0.6]]). Nothing here is new machinery; the point is to produce the one $4\times4$ that the rest of the track means by "the frozen pose".

**Step 1 — the ingredients do not move.** $M$ and the screw axes were measured at the home pose, so the worked example's numbers (its Steps 1–3) carry over unchanged no matter what $\theta$ is asked for:

$$\mathcal{S}_1 = (0,0,1;\ 0,0,0), \qquad \mathcal{S}_2 = (0,0,1;\ 0,-1,0), \qquad M = \begin{pmatrix}1&0&0&2\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

because a screw axis is a property of the mechanism at home, not of the configuration being evaluated. Only $\theta$ changes between one FK call and the next.

**Step 2 — the first factor is the identity.** $\theta_1 = 0$, and $e^{[\mathcal{S}]\cdot 0} = I$ for every screw $\mathcal{S}$, so $T(0^\circ, 90^\circ) = e^{[\mathcal{S}_2](\pi/2)}M$. The shoulder contributes nothing and the elbow does all the work. This is a fact about this pose only, and Step 6 shows what it costs to forget that.

**Step 3 — the elbow exponential, as a matrix.** For a screw with unit $\hat\omega$, the closed form is $e^{[\mathcal{S}]\theta} = \begin{pmatrix} e^{[\hat\omega]\theta} & G(\theta)v \\ 0 & 1\end{pmatrix}$ with $G(\theta) = I\theta + (1-\cos\theta)[\hat\omega] + (\theta - \sin\theta)[\hat\omega]^2$, the translation integrated along the screw — derived from the power series in [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]] (MR Prop. 3.25), which checks this very matrix. With $\hat\omega = \hat z$, $\theta = \pi/2$, $[\hat z]^2 = \mathrm{diag}(-1,-1,0)$ and the coefficients $1 - \cos(\pi/2) = 1$, $\pi/2 - \sin(\pi/2) = 0.5708$:

$$G = \begin{pmatrix}1&-1&0\\1&1&0\\0&0&\pi/2\end{pmatrix}, \qquad G\,v_2 = G\begin{pmatrix}0\\-1\\0\end{pmatrix} = \begin{pmatrix}1\\-1\\0\end{pmatrix}$$

since the first two diagonal entries are $\pi/2 - 0.5708 = 1$. Rodrigues supplies the rotation block, $e^{[\hat z](\pi/2)} = R_z(90^\circ)$, so

$$e^{[\mathcal{S}_2](\pi/2)} = \begin{pmatrix}0&-1&0&1\\1&0&0&-1\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$

**Step 4 — multiply by $M$.** Rotation: $R_z(90^\circ)\cdot I = R_z(90^\circ)$. Translation: $R_z(90^\circ)(2,0,0)^\top + (1,-1,0)^\top = (0,2,0)^\top + (1,-1,0)^\top = (1,1,0)^\top$. So

$$T(0^\circ, 90^\circ) = \begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

where the translation column is the catalog tip $(1,1)$ and the rotation block carries the tool's $x$-axis onto $+\hat y_s$, because the elbow exponential turned the whole downstream link a quarter turn about the $\hat z$ axis through $q_2$. Geometry agrees in one line: elbow $(\cos 0^\circ, \sin 0^\circ) = (1,0)$, plus a unit forearm at absolute angle $\theta_1 + \theta_2 = 90^\circ$, giving $(1,0) + (0,1) = (1,1)$.

**Step 5 — the body form**, an independent check of Step 4, is folded below for the second pass.

> [!note]- Deeper · 더 깊이
> **Step 5 — the body form, as an independent check.** The body axes are the same screws measured from the tool frame at home, $\mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\mathcal{S}_i$ (the adjoint of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §4]]), which here gives $\mathcal{B}_1 = (0,0,1;\ 0,2,0)$ and $\mathcal{B}_2 = (0,0,1;\ 0,1,0)$ — the linear parts are literally the distances $2\,\mathrm{m}$ and $1\,\mathrm{m}$ from the tool back to each axis. Then $T = M\,e^{[\mathcal{B}_1]\theta_1}e^{[\mathcal{B}_2]\theta_2}$ multiplies out to the identical $4\times4$. Two formulations, one pose.

**Step 6 — what the identity was hiding.** Take the *other* worked pose, $\theta = (90^\circ, 90^\circ)$, where neither factor is $I$, and multiply the two exponentials in the wrong order. The correct product puts the tip at $(-1, 1)$; the swapped product $e^{[\mathcal{S}_2]\theta_2}e^{[\mathcal{S}_1]\theta_1}M$ puts it at $(-1, -1)$, with the *same* orientation $R_z(180^\circ)$. Two metres of position error and no orientation error to warn you — which is why the order is part of the formula, and why the catalog pose is a poor place to test a new FK implementation.

The recipe generalizes verbatim: home pose → per-joint $(\hat\omega_i, q_i)$ →
$v_i = -\hat\omega_i \times q_i$ → exponentials → multiply. For code, the Modern Robotics
Python library implements `FKinSpace(M, Slist, thetalist)` — verify your hand computation
against it once per mechanism.

**Wiki connections**: FK is the deterministic core inside every simulator and digital
twin ([[05-construction-robotics/index|construction]]); VLAs that output joint chunks
([[01-canonical-papers/notes/4-vla/pi0|π0]]) rely on FK to interpret them in task space.

### Self-check

1. For the same arm, compute $T(90°, 0°)$ — elbow position, tip position, orientation. Which factor of the product is the identity now?
2. Why is $v_i = -\hat\omega_i \times q_i$? (What is the velocity of the origin-coincident
   point when the body rotates about the axis through $q_i$?)
3. In the body form, which joint's exponential sits closest to $M$, and why?

> [!tip]- Answers
> 1. $\theta_2 = 0$, so $e^{[\mathcal{S}_2]\cdot 0} = I$ and $T = e^{[\mathcal{S}_1]\pi/2}M$: the whole straight arm turns a quarter turn about the base. Elbow $(0,1)$, tip $(0,2,0)$, orientation $R_z(90°)$ — as a matrix, the rotation columns $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$ and the translation $(0,2,0)$. Check geometrically: $(0,1) + (0,1) = (0,2)$. ✓ It mirrors the Worked case, where the shoulder factor was the identity.
> 2. Because the axis passes through $q_i$, the body point *currently coincident with the origin* sits at $-q_i$ relative to the axis, so its velocity is $\omega\times(0 - q_i) = -\omega\times q_i$ — literally the "what $v$ means" warning of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3]].
> 3. **Joint 1.** The body form is $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}$ (MR eq. 4.16), so $e^{[\mathcal{B}_1]\theta_1}$ sits against $M$. The joint order is **not** reversed — it runs $1 \ldots n$ in both forms; what changes is which side $M$ sits on (right in the space form, left in the body form) and that the axes are written in the end-effector frame.

### Problem set · 과제

Tier B. **P2** from [[02-foundations/lab-plants|0.6]]; home and screws as on this page. No simulator.

1. **Draw.** The picture above for $\theta=(45^\circ,45^\circ)$, the pose where the shoulder moves too: dashed home (both links along $+x$, tip at $(2,0)$) and the solid evaluated arm, with the screw axes and the frames at the base, at $q_2=(1,0,0)$ and at the tip. Beside the arms, the matrix route and the geometric route to the tip. Where would the tip land if you skipped the first exponential?
2. **Derive.** The other arm that reaches the catalog target: $\theta = (90^\circ, -90^\circ)$, contact B of [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]] and the second IK branch of [[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6]]. Evaluate $T$ by the product of exponentials, factor by factor from the right — first $e^{[\mathcal{S}_2](-\pi/2)}M$, then $e^{[\mathcal{S}_1](\pi/2)}$ — and check it by geometry. What does it share with the Worked case's $T(0^\circ, 90^\circ)$, and what differs? Where would the tip land if you dropped the first factor?
3. **Interpret.** A $0.2\,\mathrm m$ tool is bolted to the tip along the forearm, and the tool frame $\{b\}$ moves to its end. Which of the ingredients $M$, $\mathcal{S}_1$, $\mathcal{S}_2$ change, and why does a new tool never change the space screw axes? Where does $T(0^\circ, 90^\circ)$ now put the tool point, and does its orientation change?

> [!note]- How to draw it · 그리는 법
> - The home arm dashed: both links along $+\hat x$, elbow at $(1,0)$, tip at $(2,0)$. This is where $M$ is read — a fact about the model, not about where the robot is now.
> - The evaluated arm solid: elbow at $(\cos45^\circ,\ \sin45^\circ)=(0.707,\ 0.707)$, tip one more unit along the absolute angle $90^\circ$, at $(0.707,\ 1.707)$. Now $\theta_1\ne0$, so the two arms no longer share link 1: draw them apart.
> - The screw axes on the home drawing and nowhere else: a circled dot at each $q_i$, labelled with $\hat\omega_i=(0,0,1)$ and its linear part $v_i=-\hat\omega_i\times q_i$. The solid elbow is at $(0.707,\ 0.707)$, not at $q_2$; marking $\mathcal{S}_2$ there is the most common way this figure goes wrong.
> - Three frames as small pairs of labelled arrows: $\{s\}$ at the base, one at $q_2$ on the home arm, and the tool frame at the solid tip with its $x$-axis along the forearm, straight up.
> - Beside the figure, two independent lines that must agree: the matrix route $T=e^{[\mathcal{S}_1]\theta_1}e^{[\mathcal{S}_2]\theta_2}M$ and the geometric route, elbow $+$ forearm.
> - A faint third arm for the shortcut that skips $e^{[\mathcal{S}_1]\theta_1}$: $e^{[\mathcal{S}_2]\theta_2}M$ alone puts the tip at $(1.707,\ 0.707)$ with $R=R_z(45^\circ)$, $1.414\,\mathrm{m}$ from the true tip. That gap is the answer to the item's last question, drawn.

> [!tip]- Solutions
> 1. Home stretched along $+x$. Evaluated arm: elbow $(0.707,\ 0.707)$, tip $(0.707,\ 1.707)$, forearm along $+y$, so $R=R_z(90^\circ)$. Matrix route: $e^{[\mathcal{S}_2]\pi/4}M$ turns $M$ about $q_2$ to tip $(1.707,\ 0.707)$ with $R=R_z(45^\circ)$; $e^{[\mathcal{S}_1]\pi/4}$ then turns that about the origin to tip $(0.707,\ 1.707)$ with $R=R_z(90^\circ)$ — the geometric route's answer. Skipping the first exponential leaves the tip at $(1.707,\ 0.707)$, $\sqrt2=1.414\,\mathrm{m}$ off: the Worked case's shortcut (Step 2) holds only because $\theta_1=0$ at the catalog pose.
> 2. Read from the right. $e^{[\mathcal{S}_2](-\pi/2)}$ turns $M$ a quarter turn clockwise about $q_2 = (1,0,0)$: the tip, $(1,0)$ from the axis, goes to $(0,-1)$ from it, so to $(1,-1)$, with $R = R_z(-90^\circ)$. Then $e^{[\mathcal{S}_1](\pi/2)}$ turns that a quarter turn counterclockwise about the origin: $(1,-1) \to (1,1)$ and $R = R_z(90^\circ)R_z(-90^\circ) = I$. So $T(90^\circ,-90^\circ)$ has $R = I$ and $p = (1,1,0)$: rows $(1,0,0,1)$, $(0,1,0,1)$, $(0,0,1,0)$, $(0,0,0,1)$. Geometry agrees: elbow $(\cos 90^\circ, \sin 90^\circ) = (0,1)$, forearm at the absolute angle $90^\circ - 90^\circ = 0^\circ$, tip $(0,1) + (1,0) = (1,1)$, heading $0^\circ$. It shares the tip with the Worked case's $T(0^\circ,90^\circ)$ and differs in orientation, $I$ against $R_z(90^\circ)$: FK gives one pose per $\theta$, but two $\theta$ reach one tip, which is why a tip position is not a configuration (ch.2 §1). Dropping the first factor leaves the tip at $(1,-1)$, $2\,\mathrm m$ from the true tip.
> 3. Only $M$ changes: at zero the tool point is at $(2.2, 0, 0)$, so $M$ gets $p = (2.2, 0, 0)$ and keeps $R = I$. $\mathcal{S}_1$ and $\mathcal{S}_2$ stay as they are, because a space screw axis is a joint's axis written in $\{s\}$ at home, and bolting on a tool moves no joint. At $(0^\circ, 90^\circ)$, $e^{[\mathcal{S}_2]\pi/2}$ turns the tool point, $1.2\,\mathrm m$ from the elbow axis, a quarter turn about $q_2$: it lands at $(1, 1.2)$, with $R = R_z(90^\circ)$ as before — $0.2\,\mathrm m$ farther up the panel face $x = 1$. The body screws, measured from the tool frame, do change, to $\mathcal{B}_1 = (0,0,1;\ 0,2.2,0)$ and $\mathcal{B}_2 = (0,0,1;\ 0,1.2,0)$ (Step 5's Deeper note): a tool change is one new $M$ in the space form but a new $\mathcal{B}_i$ for every joint in the body form.

### Sources

- K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — ch.4, §4.1 (the product of exponentials in space and body form), and Appendix C (Denavit–Hartenberg parameters); the book's companion software implements `FKinSpace`, and the [[04-robotics/modern-robotics-book|book guide]] links the free PDF.
- The poses and matrices on this page were computed here from P2's catalog numbers; recompute them rather than trusting them.

## 한국어

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 순기구학(FK)은 조작 층의 첫 계산이다. 관절각을 넣으면 도구 자세가 나온다. "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계를 받치는데, 제어 주기마다, 충돌 검사마다, 역기구학(IK) 반복마다 지금의 $\theta$에서 도구가 어디 있는지를 묻기 때문이다([[physical-ai-map|피지컬 AI 지도]]의 조작 띠에 이 페이지의 자리가 있다). 틀린 FK는 아무 경고도 주지 않는다. 엘보의 스크류 축을 홈이 아니라 $(90°, 90°)$에서 팔이 서 있는 자리에서 읽으면 곱이 말단을 참값 $(-1, 1)$에서 $2\,\mathrm m$ 떨어진 $(-3, 1)$에 놓는데, 방향은 여전히 정확하다. 두 지수의 순서를 바꾸면 말단은 $(-1, -1)$에 떨어지고, 이번에도 방향은 맞다(§1의 상자와 '대상으로 한 번 끝까지', 둘 다 §2의 그림에 그렸다). 뒤 페이지들은 이것을 끊임없이 부른다. [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §1]]은 그 스크류 축을 야코비안의 열로 바꾸고, [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장 §2]]는 뉴턴 반복마다 FK를 계산하며 $M$과 물체 스크류 축으로 자세 오차를 만들고, [[04-robotics/ros2/describing-a-robot|25.6 §2]]는 같은 사슬을 ROS가 읽는 로봇 기술 파일인 URDF의 링크 프레임으로 저장하며, [[04-robotics/capstone-panel-contact|26. 캡스톤 §6]]은 루프의 매 스텝에서 충돌 여유와 누르는 말단을 구하려고 FK를 부른다. 모두 학위논문 경로([[07-research-program/index|7 §8]])의 블록 2에 있고, 이 페이지는 그중 로보틱스 회차 10–11이다. 이 페이지를 마치면 팔의 홈 자세와 스크류 축을 읽고, $T(\theta)$를 공간 형식과 물체 형식으로 계산하고, 그 결과를 기하로 검산할 수 있다.

> [!note] 처음이라면 · First pass
> 한 회차, 로보틱스 회차 10이다. '이 페이지의 대상', 그림, 세 상자가 있는 §1, 그림이 딸린 §2의 계산 예제, 그리고 '대상으로 한 번 끝까지'를 읽되, 3단계의 행렬은 3장 §5에서 온 것으로 받아들이고 5단계의 물체 형식은 뒤로 미룬다. 회차는 페이지를 덮고 $(0°, 90°)$와 $(90°, 90°)$에서 지수 곱(PoE)과 기하가 말단에 대해 일치하는지 확인하고, 순서를 바꾼 곱이 왜 $R$은 그대로 둔 채 말단을 $2\,\mathrm m$ 옮기는지 말하고, 스스로 점검 1번을 풀며 끝낸다. 회차 11은 나머지 스스로 점검과 과제다. 접힌 *더 깊이* 메모 — §1의 D-H와 URDF, '대상으로 한 번 끝까지'의 물체 형식 — 는 두 번째 읽기다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**다. 이 위키가 숫자를 고정해 둔 *장치*(plant, 제어에서 제어 대상인 시스템을 부르는 말) 여섯 가운데 하나인 평면 2R 팔, 곧 회전 관절 둘로 된 팔이고, $L_1 = L_2 = 1\,\mathrm m$, $\theta_1$은 $+x$축에서, $\theta_2$는 링크 1에 대해 재며, 카탈로그 자세 $\theta = (0°, 90°)$에서 말단은 $(1, 1)$에 있다. 순수 기하로 구한 순기구학 — 엘보 더하기 전완 — 은 이미 [[02-foundations/manipulator-kinematics-dynamics|10 §1]]에서 유도했다. 이 페이지는 같은 사상을 지수 곱으로 쓴다. 관절이 여섯인 팔에도 그대로 옮겨 가는 꼴이다. 프레임은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장]]과 같다. 어깨의 공간 프레임 $\{s\}$, 그리고 $\hat x_b$가 전완을 따라가는 말단 도구의 물체 프레임 $\{b\}$다. 아래의 $M$은 $\theta = 0$에서의 도구 자세를 가리키는 MR의 글자이고, 10의 질량 행렬 $M(\theta)$와는 관계가 없다.

*범위: 이 페이지는 열린 사슬의 순기구학을 지수 곱으로, 공간 형식과 물체 형식 모두 P2 위에서 가르친다. 역기구학([[04-robotics/modern-robotics/ch06-inverse-kinematics|6장]]), 속도와 야코비안([[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]), Denavit–Hartenberg 규약은 가르치지 않으며, 마지막 것은 §1의 '더 깊이' 메모가 자리만 잡아 준다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 322" style="max-width:100%;height:auto" role="img" aria-label="q1과 q2의 스크류 축을 표시한 점선 홈 자세와 링크 1을 공유하는 실선 (0°, 90°) 자세로 P2를 두 번 그리고 베이스, q2, 도구 말단에 프레임을 둔 그림으로, 옆에 적은 행렬 경로와 기하 경로가 모두 말단 (1, 1)을 준다.">
  <defs><marker id="mr04hdK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <line x1="28.7" y1="196" x2="341.4" y2="196" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="70,196 188,196 306,196" fill="none" stroke="currentColor" stroke-width="2.6" stroke-dasharray="7 5" opacity="0.45"/>
  <polyline points="70,196 188,196 188,78" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.5"/>
  <circle cx="306" cy="196" r="4" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="188" cy="78" r="4.5" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1.7" marker-end="url(#mr04hdK)"><line x1="78" y1="196" x2="105.4" y2="196"/><line x1="70" y1="188" x2="70" y2="160.6"/><line x1="196" y1="196" x2="223.4" y2="196"/><line x1="188" y1="188" x2="188" y2="160.6"/><line x1="188" y1="73" x2="188" y2="42.6"/><line x1="183" y1="78" x2="152.6" y2="78"/></g>
  <circle cx="70" cy="196" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="70" cy="196" r="2" fill="currentColor"/>
  <circle cx="188" cy="196" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="188" cy="196" r="2" fill="currentColor"/>
  <line x1="352" y1="14" x2="352" y2="274" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="103.4" y="189" text-anchor="middle">x̂<tspan dy="3.5">s</tspan></text>
    <text x="62" y="166.6" text-anchor="end">ŷ<tspan dy="3.5">s</tspan></text>
    <text x="58" y="187" text-anchor="end" font-size="12">{s}</text>
    <text x="220.4" y="211" text-anchor="middle">x</text>
    <text x="181" y="165.6" text-anchor="end">y</text>
    <text x="201" y="180" font-size="12">{q<tspan dy="3.5">2</tspan><tspan dy="-3.5">}</tspan></text>
    <text x="195" y="50.6">x̂<tspan dy="3.5">b</tspan></text>
    <text x="148.6" y="71" text-anchor="end">ŷ<tspan dy="3.5">b</tspan></text>
    <text x="197" y="94" font-size="12">도구 {b}</text>
    <text x="306" y="166" text-anchor="middle" opacity="0.8">홈, θ = 0</text>
    <text x="306" y="181" text-anchor="middle" opacity="0.8">말단 (2, 0) → M</text>
    <text x="197" y="124">θ = (0°, 90°), 실선</text>
    <text x="197" y="139">말단 (1, 1)</text>
    <text x="70" y="226" text-anchor="middle">S<tspan dy="3.5">1</tspan><tspan dy="-3.5">: q</tspan><tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="70" y="242" text-anchor="middle">ω̂<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1)</tspan></text>
    <text x="70" y="258" text-anchor="middle">v<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 0)</tspan></text>
    <text x="188" y="226" text-anchor="middle">S<tspan dy="3.5">2</tspan><tspan dy="-3.5">: q</tspan><tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (1, 0, 0)</tspan></text>
    <text x="188" y="242" text-anchor="middle">ω̂<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (0, 0, 1)</tspan></text>
    <text x="188" y="258" text-anchor="middle">v<tspan dy="3.5">2</tspan><tspan dx="3.1" dy="-3.5">= (0, −1, 0)</tspan></text>
    <text x="12" y="290" opacity="0.85">점선 = 홈 자세. M과 스크류 축 S<tspan dy="3.5">1</tspan><tspan dy="-3.5">, S</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">를 여기서 읽고, 축은 거기 머문다.</tspan></text>
    <text x="12" y="306" opacity="0.85">실선 = 평가하는 자세. θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 0이라 두 팔이 링크 1을 공유한다.</tspan></text>
    <text x="364" y="26" font-size="12">두 경로, 하나의 말단</text>
    <text x="364" y="52">행렬 경로 (PoE)</text>
    <text x="372" y="69">T = exp([S<tspan dy="3.5">1</tspan><tspan dy="-3.5">]θ</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">) exp([S</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">]θ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">) M</tspan></text>
    <text x="372" y="86">θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 0이라 exp([S</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">]·0) = I</tspan></text>
    <text x="372" y="103">T = exp([S<tspan dy="3.5">2</tspan><tspan dy="-3.5">]·π/2) M</tspan></text>
    <text x="372" y="120">→ p = (1, 1, 0), R = R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(90°)</tspan></text>
    <text x="364" y="148">기하 경로</text>
    <text x="372" y="165">엘보 + 전완</text>
    <text x="372" y="182">= (1, 0) + (0, 1) = (1, 1)</text>
    <text x="364" y="210">두 줄은 반드시 같아야 한다.</text>
  </g>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**, 한 좌표축 위에 두 번: 점선은 두 링크가 모두 $+\hat x$로 뻗어 말단이 $(2,0)$인 홈 자세로 $M$과 스크류 축을 읽는 곳이고, 실선은 평가하는 자세 $\theta = (0^\circ, 90^\circ)$로 $\theta_1 = 0$이라 링크 1을 홈 팔과 공유한다. 스크류 축은 홈 팔에만 있고($q_1 = (0,0,0)$을 지나는 $\mathcal{S}_1$은 $v_1 = (0,0,0)$, $q_2 = (1,0,0)$을 지나는 $\mathcal{S}_2$는 $v_2 = (0,-1,0)$), 프레임은 베이스, $q_2$, 도구 말단에 있다. 옆에 적은 행렬 경로 $T = e^{[\mathcal{S}_2]\pi/2}M$과 기하 경로 엘보 $+$ 전완 $= (1,0) + (0,1)$이 말단 $(1,1)$, $R = R_z(90^\circ)$에서 일치한다.

### 1. 지수 곱 공식

제어 주기마다 엔코더가 $\theta$를 보고하면 제어기도, 충돌 검사기도, IK 루프도 같은 질문을 한다. 관절각이 주어지면 도구는 어디 있는가? 이 절은 홈에서 한 번 읽는 재료 둘로 만든 공식 하나로 답한다.

$$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$

오른쪽에서 왼쪽으로 읽어라. $M$ 바로 옆의 인자가 먼저 작용하기 때문이다. 홈 자세 $M$(모든 관절 0)에서 시작해, 각 관절이 자기 하류 전체를 스크류로 돌린다. 재료는 둘뿐이다. 홈 자세, 그리고 관절마다 *홈 위치에서 고정 프레임 기준으로 쓴* 스크류 축 하나다. 중간 링크 프레임은 필요 없다. 그것을 쓰는 고전 규약과 아직도 링크 프레임을 잇는 로봇 기술 파일은 아래 '더 깊이' 메모에 자리를 잡아 둔다.

**홈에서 한 번 읽은 축이 모든 $\theta$에 통하는 이유.** 곱을 오른쪽부터 읽는다. $e^{[\mathcal{S}_2]\theta_2}$가 먼저 작용해 관절 1이 아직 움직이지 않은 채로 전완을 $(1, 0, 0)$을 지나는 엘보 축 둘레로 돌리므로, 엘보는 홈 축이 말하는 바로 그 자리에 서 있다. 그다음 $e^{[\mathcal{S}_1]\theta_1}$이 엘보 축까지 포함해 굽은 팔 전체를 베이스 둘레로 옮긴다. $(90°, 90°)$에서 말단은 $(2,0) \to (1,1) \to (-1,1)$로 가고, 이것이 §2 그림의 세 칸이다. (**물체 형식**(body form) $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots$은 축을 말단 프레임에서 쓴 같은 사상이다.)

> [!note]- 더 깊이 · Deeper
> **D-H 파라미터와 URDF.** 중간 링크 프레임이 필요 없다는 것이 Denavit–Hartenberg(D-H) 대비 장점이다. D-H는 링크마다 프레임을 붙이고 각 관절을 이전 링크 프레임에 대한 네 숫자 — 링크 길이, 링크 비틀림(이웃한 관절 축 사이의 각으로, 3장의 트위스트가 아니다), 오프셋, 관절각 — 로 기술하는 고전 규약이다(MR 부록 C, 위키에는 별도 페이지가 없다). MR의 소프트웨어 라이브러리가 PoE를 쓰는 이유가 이것이다. 주류 로봇 형식은 여전히 부모–자식 링크 프레임을 잇는다. ROS가 읽는 XML 로봇 기술인 URDF는 팔을 관절로 이어진 링크 프레임의 트리로 저장한다([[04-robotics/ros2/describing-a-robot|25.6 §2]]).

> **순기구학의 정의.** **순기구학**(forward kinematics)은 관절 값에서 도구의 자세로 가는 *사상*이고, 세 조건이 그것을 사상으로 만든다. **입력은 관절 벡터 하나뿐**이다. $\theta \in \mathbb{R}^n$만 들어가고 속도도 토크도 이력도 들어가지 않는다. **출력은 고른 과제 공간에서 본 도구 프레임의 자세**다. MR은 이것을 도구의 *컨피규레이션*이라 부르지만, 이 위키는 그 말을 로봇 전체의 관절 값에 남겨 둔다([[04-robotics/modern-robotics/ch02-configuration-space|2장 §1]]). 일반적으로는 고정 프레임 $\{s\}$에서 본 프레임 $\{b\}$의 자세 $T_{sb} \in SE(3)$이고, 위치만 중요할 때의 말단 위치처럼 과제 좌표 $x = f(\theta)$일 수도 있다. 그래서 프레임과 과제 좌표가 정의에 들어 있다. 그리고 **열린 사슬에서는 값이 하나로 정해진다**. 링크가 강체이고 관절 값이 고정되면 남는 자유가 없으므로 $\theta$ 하나에 출력이 정확히 하나다. 닫힌 사슬은 여럿일 수 있다(MR 7장).
>
> $$\theta \mapsto T_{sb}(\theta) = \begin{pmatrix} R(\theta) & p(\theta) \\ 0 & 1 \end{pmatrix} \in SE(3), \qquad x = f(\theta) \in \mathbb{R}^m$$
>
> 여기서 $R(\theta)$와 $p(\theta)$는 $\{s\}$에서 쓴 도구 프레임의 방향과 원점이고, $f$는 같은 자세를 과제의 좌표 $m$개로 쓴 것이다. $SE(3)$가 일반적인 경우인 것은 강체 도구에 위치뿐 아니라 방향도 있기 때문이다.
>
> - **예**: 어깨에 $\{s\}$, 말단에 $\{b\}$를 둔 P2는 $(0^\circ, 90^\circ)$를 $p = (1,1,0)$, $R = R_z(90^\circ)$로, $(90^\circ, -90^\circ)$를 $p = (1,1,0)$, $R = I$로 보낸다. 위치 과제 $f(\theta) = (x, y)$에서는 둘 다 $(1,1)$로 간다.
> - **비예**: 거꾸로 가는 사상, 곧 말단에서 관절로 되돌아가는 사상. 기구학을 뒤집을 수 있는 관계 하나로 그리기 쉽지만, 이 사상은 함수가 아니다. $(1,1)$에는 위의 역상이 둘 있고 $(2.5, 0)$에는 하나도 없다. 그것은 6장의 문제이고, FK는 어떤 $\theta$에서든 그냥 부를 수 있는데 IK는 가지 가운데 고르거나 해가 없다고 보고해야 하는 이유다.

> **홈 자세의 정의.** **홈 자세**(home configuration) $M$은 $SE(3)$의 *상수 원소 하나*다. 모든 관절이 0일 때 고정 프레임 $\{s\}$에서 본 도구 프레임 $\{b\}$의 자세다. 세 조건이 그것을 정한다. **모든 관절 값이 0이다**. 곧 $\theta = 0$이고, 각 관절의 0과 양의 방향은 먼저 선언해 둔다. **고정 프레임에서 본 도구 프레임이다.** 링크 프레임이 아니다. 그리고 **상수다.** $\{s\}$, $\{b\}$, 관절의 0을 고르면 한 번 정해지고, 로봇이 움직여도 갱신하지 않는다.
>
> $$M = T_{sb}(0) = \begin{pmatrix} R_{sb}(0) & p_{sb}(0) \\ 0 & 1 \end{pmatrix} \in SE(3)$$
>
> 여기서 $R_{sb}(0)$와 $p_{sb}(0)$는 영 자세에서 도구 프레임의 방향과 원점이다. 공간 형식에서 $M$이 오른쪽 끝에 오는 것은 모든 인자가 고정 프레임에서 쓴 스크류 운동이고, $\{s\}$에서 쓴 운동은 왼쪽에서 곱해지기 때문이다(MR §3.3.1). 물체 형식의 스크류 축은 $\{b\}$에서 쓰므로 $M$이 그 왼쪽으로 간다.
>
> - **예**: P2는 영 자세에서 두 링크가 모두 $+\hat x$를 향하므로 $R = I$, $p = (2,0,0)$이다. 1단계의 $M$이다.
> - **비예**: "로봇이 보통 있는 곳"인 카탈로그 자세 $T(0^\circ, 90^\circ)$. $M$ 자리에 넣고 같은 $\theta$에서 계산하면 엘보가 전완을 한 번 더 돌려, 말단이 $(0,0)$, $R = R_z(180^\circ)$에 떨어지고 참값 $(1,1)$에서 $1.414\,\mathrm{m}$ 벗어난다. $M$은 영 자세에서 한 번 읽는다. 팔이 마침 서 있는 곳에서 읽으면 그 뒤의 모든 FK 호출이 그 실수를 물려받는다.

> **지수 곱 공식의 정의.** **지수 곱 공식**(product of exponentials, PoE)은 *순기구학 사상을 나타내는 한 방식*이다. 관절마다 SE(3) 지수 하나를 $M$에 곱한다. 정의 조건 셋. 재료는 **홈 자세** $M$과 **영 자세에서 읽은 관절별 스크류 축 하나**다. 공간 형식이면 $\{s\}$에서 쓴 $\mathcal{S}_i$로, 회전 관절은 $(\hat\omega_i,\ -\hat\omega_i \times q_i)$, 단위 방향이 $\hat v_i$인 직동 관절은 $(0,\ \hat v_i)$다. 물체 형식이면 $\{b\}$에서 쓴 $\mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\mathcal{S}_i$다. **인자는 관절 순서대로 놓인다.** 두 형식 모두 왼쪽에서 오른쪽으로 $1$부터 $n$까지다. 그리고 **$M$은 공간 형식에서는 오른쪽, 물체 형식에서는 왼쪽에 온다.**
>
> $$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\cdots e^{[\mathcal{S}_n]\theta_n}M = M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}, \qquad \mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\,\mathcal{S}_i$$
>
> 여기서 각 인자는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §5]]의 스크류 운동이다. 홈에서 한 번 읽은 축이 모든 $\theta$에 통하는 것은, 공간 형식에서 각 지수가 베이스 쪽 관절들이 그 축을 옮겨 놓기 전에 작용하기 때문이다(MR §4.1).
>
> - **예**: P2의 $\mathcal{S}_1 = (0,0,1;\,0,0,0)$, $\mathcal{S}_2 = (0,0,1;\,0,-1,0)$, $\mathcal{B}_1 = (0,0,1;\,0,2,0)$, $\mathcal{B}_2 = (0,0,1;\,0,1,0)$. 두 형식 모두 $(90^\circ, 90^\circ)$에서 말단을 $(-1,1)$, $R_z(180^\circ)$에 놓는다.
> - **비예**: 팔이 지금 서 있는 자리에서 읽은 $\mathcal{S}_2$. $(90^\circ, 90^\circ)$에서 엘보는 $(0,1)$에 있고, 거기서 읽으면 $(0,0,1;\,1,0,0)$이 되어 곱이 말단을 $(-3,1)$에 놓는다. $(-1,1)$에서 $2\,\mathrm{m}$ 벗어났는데 방향은 여전히 정확히 $R_z(180^\circ)$다. 평면 팔에서는 모든 인자가 $\hat z$ 둘레로 돌기 때문에 어떤 축을 쓰든 회전 블록이 $R_z(\theta_1 + \theta_2)$이고, 잘못 놓인 스크류를 드러낼 수 있는 것은 위치 열뿐이다.

### 2. (90°, 90°)에서의 계산 예제

공식은 독립된 무언가와 맞춰 본 뒤에야 믿을 수 있다. 그래서 이 절은 두 관절이 모두 움직이는 자세에서 2R 팔에 레시피를 돌리고, 답을 순수 기하와 맞춰 본다.

링크 $L_1 = L_2 = 1$, 홈에서 둘 다 $+\hat x$ 방향으로 뻗어 있다. 일반 레시피와 숫자를
함께 따라가라:

**1단계 — 홈 자세 $M$.** 말단이 $(2, 0, 0)$, 베이스와 같은 방향:
$$M = \begin{pmatrix} 1&0&0&2\\ 0&1&0&0\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**2단계 — 관절 1의 스크류 축.** 축 방향 $\hat\omega_1 = (0,0,1)$; 축 위의 점
$q_1 = (0,0,0)$; 선형부 $v_1 = -\hat\omega_1 \times q_1 = (0,0,0)$.
따라서 $\mathcal{S}_1 = (0,0,1;\; 0,0,0)$.

**3단계 — 관절 2의 스크류 축.** $\hat\omega_2 = (0,0,1)$; $q_2 = (1,0,0)$;
$v_2 = -\hat\omega_2 \times q_2 = -(0,1,0) = (0,-1,0)$.
따라서 $\mathcal{S}_2 = (0,0,1;\; 0,-1,0)$.

**4단계 — $\theta_1 = \theta_2 = 90°$에서 평가.**
$e^{[\mathcal{S}_2]\,90°}$는 $q_2 = (1,0,0)$을 지나는 $\hat z$축 둘레로 모든 것을 90° 돌린다.
$M$에 적용하면: 말단은 축 기준 $p - q_2 = (1,0,0)$에 있고, 90° 돌리면 $(0,1,0)$, $q_2$를
되더하면 $(1,1,0)$, 방향은 $R_z(90°)$. 그다음 $e^{[\mathcal{S}_1]\,90°}$가 그 결과를 원점
둘레로 90° 돌린다: $(1,1,0) \to (-1,1,0)$, 방향 $R_z(180°)$:
$$T(90°, 90°) = \begin{pmatrix} -1&0&0&-1\\ 0&-1&0&1\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**5단계 — 순수 기하로 검산.** $\theta_1 = 90°$면 링크 1이 $+\hat y$ 방향(엘보
$(0,1)$); $\theta_2 = 90°$가 90°를 더해 링크 2는 $-\hat x$ 방향; 말단 $= (0,1) + (-1,0)
= (-1, 1)$, 총 방향 $180°$. **같은 답이다.** 모델링하는 모든 로봇에서 이 이중 검산을
하라 — 기하 FK와 PoE FK는 반드시 일치해야 한다.

아래 그림은 4–5단계를 그리고, 그 아래에 같은 $\theta$에서의 틀린 곱 둘을 그린다. §1의 상자에서 잘못 읽은 스크류 축, 그리고 뒤의 '대상으로 한 번 끝까지' 6단계가 다시 다루는 순서를 바꾼 곱이다.

<svg viewBox="0 0 560 318" style="max-width:100%;height:auto" role="img" aria-label="P2를 세 칸에 그린 그림: 홈 자세, 엘보 지수 뒤 말단 (1, 1), 어깨 지수 뒤 말단 (−1, 1). 아래 칸은 순서를 바꾼 곱의 말단 (−1, −1)과 엘보 축을 서 있는 자리에서 읽은 곱의 말단 (−3, 1)을 참 말단과 함께 보이며, 셋 다 방향은 R_z(180°)다.">
  <defs><marker id="mr04peK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <line x1="12" y1="118" x2="180" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="71.8,118 115.8,118 159.8,118" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6"/>
  <circle cx="71.8" cy="118" r="3.4" fill="currentColor"/>
  <circle cx="115.8" cy="118" r="3" fill="currentColor"/>
  <circle cx="159.8" cy="118" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="164.8" y1="118" x2="183.8" y2="118" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr04peK)"/>
  <circle cx="71.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="115.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="196" y1="118" x2="364" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="255.8,118 299.8,118 343.8,118" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 4" opacity="0.45"/>
  <polyline points="255.8,118 299.8,118 299.8,74" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6"/>
  <circle cx="255.8" cy="118" r="3.4" fill="currentColor"/>
  <circle cx="299.8" cy="118" r="3" fill="currentColor"/>
  <circle cx="299.8" cy="74" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="299.8" y1="69" x2="299.8" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr04peK)"/>
  <circle cx="299.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="343.8,118 343.6,114.2 343.1,110.4 342.3,106.6 341.1,103 339.7,99.4 337.9,96 335.8,92.8 333.5,89.7 330.9,86.9 328.1,84.3 325,82 321.8,79.9 318.4,78.1 314.8,76.7 311.2,75.5 307.4,74.7 303.6,74.2 299.8,74" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr04peK)"/>
  <line x1="380" y1="118" x2="548" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="439.8,118 483.8,118 483.8,74" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 4" opacity="0.45"/>
  <polyline points="439.8,118 439.8,74 395.8,74" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round" opacity="0.6"/>
  <circle cx="439.8" cy="118" r="3.4" fill="currentColor"/>
  <circle cx="439.8" cy="74" r="3" fill="currentColor"/>
  <circle cx="395.8" cy="74" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="390.8" y1="74" x2="371.8" y2="74" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr04peK)"/>
  <circle cx="439.8" cy="118" r="6.5" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="483.8,74 479.8,70.3 475.5,67 470.9,64.1 466.1,61.6 461.1,59.5 455.9,57.9 450.6,56.7 445.2,56 439.8,55.8 434.4,56 429,56.7 423.7,57.9 418.5,59.5 413.5,61.6 408.7,64.1 404.1,67 399.8,70.3 395.8,74" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr04peK)"/>
  <line x1="20" y1="245" x2="216" y2="245" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <polyline points="160,245 160,205 120,205" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" opacity="0.55"/>
  <circle cx="160" cy="245" r="3.4" fill="currentColor"/>
  <circle cx="200" cy="245" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>
  <circle cx="160" cy="205" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 2"/>
  <circle cx="120" cy="205" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="115" y1="205" x2="98" y2="205" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr04peK)"/>
  <circle cx="120" cy="285" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 2"/>
  <line x1="115" y1="285" x2="98" y2="285" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr04peK)"/>
  <circle cx="40" cy="205" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 2"/>
  <line x1="35" y1="205" x2="18" y2="205" stroke="currentColor" stroke-width="1.5" marker-end="url(#mr04peK)"/>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="1 3" opacity="0.8"><line x1="120" y1="211" x2="120" y2="279"/><line x1="94" y1="205" x2="46" y2="205"/></g>
  <g font-size="11" fill="currentColor">
    <text x="14" y="22" font-size="12">① 홈: M</text>
    <text x="14" y="135">말단 (2, 0), R = I</text>
    <text x="14" y="150" opacity="0.8">축 S<tspan dy="3.5">1</tspan><tspan dy="-3.5">, S</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">는 여기서 읽는다</tspan></text>
    <text x="198" y="22" font-size="12">② exp([S<tspan dy="3.5">2</tspan><tspan dy="-3.5">]·π/2) M</tspan></text>
    <text x="198" y="135">말단 (1, 1), R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(90°)</tspan></text>
    <text x="198" y="150" opacity="0.8">엘보만 돈다, 관절 1은 아직</text>
    <text x="382" y="22" font-size="12">③ exp([S<tspan dy="3.5">1</tspan><tspan dy="-3.5">]·π/2) ②</tspan></text>
    <text x="382" y="135">말단 (−1, 1), R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(180°)</tspan></text>
    <text x="382" y="150" opacity="0.8">굽은 팔 전체가 베이스 둘레로</text>
    <text x="120" y="193" text-anchor="middle">참 (−1, 1)</text>
    <text x="128" y="289">순서를 바꾼 곱 (−1, −1)</text>
    <text x="40" y="193" text-anchor="middle">(−3, 1)</text>
    <text x="14" y="225">S<tspan dy="3.5">2</tspan><tspan dy="-3.5">를 (0, 1)에서 읽음</tspan></text>
    <text x="209" y="260" opacity="0.8">홈 축 q<tspan dy="3.5">2</tspan><tspan dy="-3.5"></tspan></text>
    <text x="125" y="237">2 m</text>
    <text x="76" y="200" text-anchor="middle">2 m</text>
    <text x="300" y="184" font-size="12">틀린 곱 둘, (90°, 90°)에서</text>
    <text x="300" y="203">세 도구 프레임 모두 R = R<tspan dy="3.5">z</tspan><tspan dy="-3.5">(180°):</tspan></text>
    <text x="300" y="219">방향 오차는 0이고, 위치 열만</text>
    <text x="300" y="235">잘못을 드러낸다 — 두 경우 모두 2 m.</text>
    <text x="300" y="257">순서를 바꾸면 어깨가 먼저 팔을 세우고,</text>
    <text x="300" y="273">엘보 지수는 그 팔을 홈 축 (1, 0) 둘레로 돌린다.</text>
    <text x="300" y="295">축을 (0, 1)에서 읽으면 어깨가 그 축을</text>
    <text x="300" y="311">한 번 더 옮겨 놓는다.</text>
  </g>
</svg>

위 칸은 $(90°, 90°)$의 곱을 오른쪽부터 읽은 것이다. ① 홈, 말단 $(2, 0)$, $R = I$. ② 엘보 인자가 관절 1보다 먼저 전완을 $q_2 = (1, 0, 0)$ 둘레로 돌려 말단 $(1, 1)$, $R_z(90°)$. ③ 어깨 인자가 굽은 팔 전체를 베이스 둘레로 돌려 말단 $(-1, 1)$, $R_z(180°)$. 아래 칸은 같은 $\theta$에서의 틀린 곱 둘이다. 순서를 바꾼 곱은 말단을 $(-1, -1)$에, 엘보가 서 있는 $(0, 1)$에서 읽은 엘보 스크류 축은 $(-3, 1)$에 놓는다. 둘 다 $2\,\mathrm m$ 벗어났고 둘 다 방향은 올바른 $R_z(180°)$이므로, 잘못을 드러내는 것은 위치 열뿐이다.

### 대상으로 한 번 끝까지 · Worked case

같은 레시피를 카탈로그 대상에, 이후 모든 장이 인용하는 그 자세에서 돌린다. [[02-foundations/lab-plants|0.6]]의 장치 **P2**, $\theta = (0^\circ, 90^\circ)$다. 새로운 기계장치는 없다. 목적은 트랙의 나머지가 "고정 자세"라고 부를 때 뜻하는 그 $4\times4$ 하나를 만들어 내는 것이다.

**1단계 — 재료는 움직이지 않는다.** $M$과 스크류 축은 홈 자세에서 쟀으므로, 어떤 $\theta$를 물어도 계산 예제의 숫자(그 1–3단계)가 그대로다:

$$\mathcal{S}_1 = (0,0,1;\ 0,0,0), \qquad \mathcal{S}_2 = (0,0,1;\ 0,-1,0), \qquad M = \begin{pmatrix}1&0&0&2\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

스크류 축은 평가하려는 자세가 아니라 홈에서의 기구에 대한 성질이기 때문이다. FK 호출 사이에서 바뀌는 것은 $\theta$뿐이다.

**2단계 — 첫 인자가 항등이다.** $\theta_1 = 0$이고 모든 스크류 $\mathcal{S}$에 대해 $e^{[\mathcal{S}]\cdot 0} = I$이므로 $T(0^\circ, 90^\circ) = e^{[\mathcal{S}_2](\pi/2)}M$이다. 어깨는 아무것도 하지 않고 엘보가 전부 한다. 이 자세에서만 성립하는 사실이고, 그것을 잊으면 얼마를 치르는지는 6단계가 보여 준다.

**3단계 — 엘보 지수를 행렬로.** 단위 $\hat\omega$의 스크류에 대한 닫힌 형태는 $e^{[\mathcal{S}]\theta} = \begin{pmatrix} e^{[\hat\omega]\theta} & G(\theta)v \\ 0 & 1\end{pmatrix}$이고, $G(\theta) = I\theta + (1-\cos\theta)[\hat\omega] + (\theta - \sin\theta)[\hat\omega]^2$는 스크류를 따라 적분한 병진이다. 거듭제곱 급수에서의 유도는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §5]]에 있고(MR 명제 3.25), 거기서 바로 이 행렬을 검산한다. $\hat\omega = \hat z$, $\theta = \pi/2$, $[\hat z]^2 = \mathrm{diag}(-1,-1,0)$이고 계수가 $1 - \cos(\pi/2) = 1$, $\pi/2 - \sin(\pi/2) = 0.5708$이므로

$$G = \begin{pmatrix}1&-1&0\\1&1&0\\0&0&\pi/2\end{pmatrix}, \qquad G\,v_2 = G\begin{pmatrix}0\\-1\\0\end{pmatrix} = \begin{pmatrix}1\\-1\\0\end{pmatrix}$$

다. 앞의 두 대각 성분이 $\pi/2 - 0.5708 = 1$이기 때문이다. 회전 블록은 로드리게스가 주므로 $e^{[\hat z](\pi/2)} = R_z(90^\circ)$이고,

$$e^{[\mathcal{S}_2](\pi/2)} = \begin{pmatrix}0&-1&0&1\\1&0&0&-1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

이다.

**4단계 — $M$을 곱한다.** 회전은 $R_z(90^\circ)\cdot I = R_z(90^\circ)$. 병진은 $R_z(90^\circ)(2,0,0)^\top + (1,-1,0)^\top = (0,2,0)^\top + (1,-1,0)^\top = (1,1,0)^\top$. 따라서

$$T(0^\circ, 90^\circ) = \begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

이다. 병진 열이 카탈로그 말단 $(1,1)$이고 회전 블록이 도구의 $x$축을 $+\hat y_s$로 옮기는데, 엘보 지수가 $q_2$를 지나는 $\hat z$축 둘레로 하류 링크 전체를 4분의 1바퀴 돌렸기 때문이다. 기하도 한 줄이다. 엘보 $(\cos 0^\circ, \sin 0^\circ) = (1,0)$에 절대각 $\theta_1 + \theta_2 = 90^\circ$인 단위 전완을 더해 $(1,0) + (0,1) = (1,1)$.

**5단계 — 물체 형식**, 4단계의 독립 검산은 아래에 두 번째 읽기로 접어 둔다.

> [!note]- 더 깊이 · Deeper
> **5단계 — 물체 형식으로 독립 검산.** 물체 축은 같은 스크류를 홈에서 도구 프레임 기준으로 잰 것, 곧 $\mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\mathcal{S}_i$다([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §4]]의 수반). 여기서는 $\mathcal{B}_1 = (0,0,1;\ 0,2,0)$, $\mathcal{B}_2 = (0,0,1;\ 0,1,0)$이고, 선형부가 말 그대로 도구에서 각 축까지의 거리 $2\,\mathrm{m}$와 $1\,\mathrm{m}$다. $T = M\,e^{[\mathcal{B}_1]\theta_1}e^{[\mathcal{B}_2]\theta_2}$를 곱하면 같은 $4\times4$가 나온다. 정식화 둘, 자세 하나.

**6단계 — 항등이 가리고 있던 것.** 두 인자 중 어느 쪽도 $I$가 아닌 다른 계산 자세 $\theta = (90^\circ, 90^\circ)$에서 두 지수를 일부러 반대 순서로 곱해 보자. 올바른 곱은 말단을 $(-1, 1)$에 놓고, 뒤바꾼 곱 $e^{[\mathcal{S}_2]\theta_2}e^{[\mathcal{S}_1]\theta_1}M$은 $(-1, -1)$에 놓는다. 방향은 *둘 다* $R_z(180^\circ)$로 같다. 위치 오차 2 m에 경고가 될 방향 오차는 0이다. 순서가 공식의 일부인 이유이고, 새 FK 구현을 시험하기에 카탈로그 자세가 나쁜 자리인 이유다.

레시피는 그대로 일반화된다: 홈 자세 → 관절별 $(\hat\omega_i, q_i)$ →
$v_i = -\hat\omega_i \times q_i$ → 지수들 → 곱. 코드로는 Modern Robotics 파이썬
라이브러리의 `FKinSpace(M, Slist, thetalist)`가 이것을 구현한다 — 기구마다 한 번은
손계산과 라이브러리 결과를 대조하라.

**위키 연결**: FK는 모든 시뮬레이터·디지털 트윈([[05-construction-robotics/index|건설]])
안의 결정론적 핵심이고, VLA가 출력한 관절 청크([[01-canonical-papers/notes/4-vla/pi0|π0]])를
작업 공간에서 해석할 때 FK가 쓰인다.

### 스스로 점검

1. 같은 팔에서 $T(90°, 0°)$를 계산하라 — 엘보 위치, 말단 위치, 방향. 이번에는 곱의 어느 인자가 항등인가?
2. 왜 $v_i = -\hat\omega_i \times q_i$인가? ($q_i$를 지나는 축 둘레로 돌 때, 원점과 겹친
   물체 점의 속도는 무엇인가?)
3. 물체 형식에서는 어느 관절의 지수가 $M$에 가장 가까이 붙는가? 왜인가?

> [!tip]- 정답 · Answers
> 1. $\theta_2 = 0$이라 $e^{[\mathcal{S}_2]\cdot 0} = I$이고 $T = e^{[\mathcal{S}_1]\pi/2}M$이다. 곧게 편 팔 전체가 베이스 둘레로 4분의 1바퀴 돈다. 엘보 $(0,1)$, 말단 $(0,2,0)$, 방향 $R_z(90°)$이고, 행렬로는 회전 열 $(0,1,0)$, $(-1,0,0)$, $(0,0,1)$과 병진 $(0,2,0)$이다. 기하로 검산: $(0,1) + (0,1) = (0,2)$. ✓ 어깨 인자가 항등이던 '대상으로 한 번 끝까지'를 거울에 비춘 경우다.
> 2. 원점과 겹친 물체 점은 축에서 $-q_i$만큼 떨어져 있으므로 속도는 $\omega\times(0 - q_i) = -\omega\times q_i$ — [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3]]의 $v$ 정의 그대로.
> 3. **관절 1.** 물체 형식은 $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}$(MR 식 4.16)이므로 $e^{[\mathcal{B}_1]\theta_1}$이 $M$에 붙는다. 곱 순서는 **뒤집히지 않는다** — 두 형식 모두 $1 \ldots n$이고, 달라지는 것은 $M$이 어느 쪽에 오는지(공간 형식은 오른쪽, 물체 형식은 왼쪽)와 축을 말단 프레임에서 쓴다는 점이다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**. 홈과 스크류 축은 이 페이지의 것. 시뮬레이터 없음.

1. **그리기.** 어깨도 움직이는 자세 $\theta=(45^\circ,45^\circ)$에 대한 위의 그림: 점선 홈(두 링크 $+x$, 말단 $(2,0)$)과 실선으로 그린 평가 자세의 팔, 스크류 축, 그리고 베이스·$q_2=(1,0,0)$·말단의 프레임. 팔 옆에 말단까지의 행렬 경로와 기하 경로를 적어라. 첫 지수를 건너뛰었다면 말단은 어디에 떨어졌겠는가?
2. **유도.** 카탈로그 목표에 닿는 다른 팔, $\theta = (90^\circ, -90^\circ)$ — [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 접촉 B이자 [[04-robotics/modern-robotics/ch06-inverse-kinematics|6장]]의 두 번째 IK 가지. 지수 곱으로 $T$를 오른쪽 인자부터 — 먼저 $e^{[\mathcal{S}_2](-\pi/2)}M$, 그다음 $e^{[\mathcal{S}_1](\pi/2)}$ — 계산하고 기하로 검산하라. '대상으로 한 번 끝까지'의 $T(0^\circ, 90^\circ)$와 무엇이 같고 무엇이 다른가? 첫 인자를 빼면 말단은 어디에 떨어지는가?
3. **해석.** 전완을 따라 $0.2\,\mathrm m$짜리 도구를 말단에 붙이고, 도구 프레임 $\{b\}$를 그 끝으로 옮긴다. 재료 $M$, $\mathcal{S}_1$, $\mathcal{S}_2$ 가운데 무엇이 바뀌고, 새 도구가 공간 스크류 축을 왜 절대 바꾸지 않는가? $T(0^\circ, 90^\circ)$는 이제 도구 점을 어디에 놓고, 방향은 바뀌는가?

> [!note]- 그리는 법 · How to draw it
> - 홈 자세의 팔은 점선. 두 링크 모두 $+\hat x$, 엘보 $(1,0)$, 말단 $(2,0)$. $M$을 읽는 곳이며, 로봇이 지금 어디 있는지가 아니라 모형에 대한 사실이다.
> - 평가할 자세의 팔은 실선. 엘보는 $(\cos45^\circ,\ \sin45^\circ)=(0.707,\ 0.707)$, 말단은 거기서 절대각 $90^\circ$ 방향으로 한 단위 더 간 $(0.707,\ 1.707)$. 이제 $\theta_1\ne0$이므로 두 팔은 링크 1을 공유하지 않는다. 떨어뜨려 그린다.
> - 스크류 축은 홈 그림에만 표시한다. 각 $q_i$에 동그라미 친 점을 찍고 $\hat\omega_i=(0,0,1)$과 선형부 $v_i=-\hat\omega_i\times q_i$를 적는다. 실선 엘보는 $q_2$가 아니라 $(0.707,\ 0.707)$에 있고, $\mathcal{S}_2$를 거기에 표시하는 것이 이 그림이 틀리는 가장 흔한 방식이다.
> - 프레임 셋을 이름 붙인 짧은 화살표 쌍으로. 베이스의 $\{s\}$, 홈 팔의 $q_2$에 하나, 그리고 실선 말단의 도구 프레임이고, 도구 프레임의 $x$축은 전완 방향, 곧 곧장 위다.
> - 그림 옆에는 서로 맞아야 하는 두 줄을 독립적으로 적는다. 행렬 경로 $T=e^{[\mathcal{S}_1]\theta_1}e^{[\mathcal{S}_2]\theta_2}M$과 기하 경로 엘보 $+$ 전완이다.
> - $e^{[\mathcal{S}_1]\theta_1}$을 건너뛰는 지름길의 셋째 팔을 흐리게: $e^{[\mathcal{S}_2]\theta_2}M$만으로는 말단이 $(1.707,\ 0.707)$, $R=R_z(45^\circ)$에 놓여 참 말단에서 $1.414\,\mathrm{m}$ 떨어진다. 그 간격이 이 문항의 마지막 질문의 답을 그린 것이다.

> [!tip]- 정답 · Solutions
> 1. 홈은 $+x$로 뻗음. 평가 자세: 엘보 $(0.707,\ 0.707)$, 말단 $(0.707,\ 1.707)$, 전완은 $+y$ 방향이라 $R=R_z(90^\circ)$. 행렬 경로: $e^{[\mathcal{S}_2]\pi/4}M$이 $M$을 $q_2$ 둘레로 돌려 말단을 $(1.707,\ 0.707)$, $R=R_z(45^\circ)$에 놓고, $e^{[\mathcal{S}_1]\pi/4}$가 그것을 원점 둘레로 돌려 말단 $(0.707,\ 1.707)$, $R=R_z(90^\circ)$ — 기하 경로의 답과 같다. 첫 지수를 건너뛰면 말단은 $(1.707,\ 0.707)$에 남아 $\sqrt2=1.414\,\mathrm{m}$ 어긋난다. '대상으로 한 번 끝까지'의 지름길(2단계)은 카탈로그 자세에서 $\theta_1=0$이기 때문에만 성립한다.
> 2. 오른쪽부터 읽는다. $e^{[\mathcal{S}_2](-\pi/2)}$는 $M$을 $q_2 = (1,0,0)$ 둘레로 시계 방향 4분의 1바퀴 돌린다. 축에서 $(1,0)$에 있던 말단이 축에서 $(0,-1)$로, 곧 $(1,-1)$로 가고 $R = R_z(-90^\circ)$다. 그다음 $e^{[\mathcal{S}_1](\pi/2)}$가 그것을 원점 둘레로 반시계 방향 4분의 1바퀴 돌린다. $(1,-1) \to (1,1)$이고 $R = R_z(90^\circ)R_z(-90^\circ) = I$다. 따라서 $T(90^\circ,-90^\circ)$는 $R = I$, $p = (1,1,0)$, 곧 행 $(1,0,0,1)$, $(0,1,0,1)$, $(0,0,1,0)$, $(0,0,0,1)$이다. 기하도 같다. 엘보 $(\cos 90^\circ, \sin 90^\circ) = (0,1)$, 전완의 절대각 $90^\circ - 90^\circ = 0^\circ$, 말단 $(0,1) + (1,0) = (1,1)$, 방향 $0^\circ$. '대상으로 한 번 끝까지'의 $T(0^\circ,90^\circ)$와 말단은 같고 방향은 $I$ 대 $R_z(90^\circ)$로 다르다. FK는 $\theta$마다 자세를 하나 주지만 두 $\theta$가 한 말단에 닿고, 그래서 말단 위치는 컨피규레이션이 아니다(2장 §1). 첫 인자를 빼면 말단은 참 말단에서 $2\,\mathrm m$ 떨어진 $(1,-1)$에 남는다.
> 3. $M$만 바뀐다. 영 자세에서 도구 점은 $(2.2, 0, 0)$에 있으므로 $M$은 $p = (2.2, 0, 0)$이 되고 $R = I$는 그대로다. $\mathcal{S}_1$과 $\mathcal{S}_2$는 그대로다. 공간 스크류 축은 홈에서 $\{s\}$로 쓴 관절의 축이고, 도구를 붙인다고 관절이 움직이지는 않기 때문이다. $(0^\circ, 90^\circ)$에서 $e^{[\mathcal{S}_2]\pi/2}$는 엘보 축에서 $1.2\,\mathrm m$ 떨어진 도구 점을 $q_2$ 둘레로 4분의 1바퀴 돌려 $(1, 1.2)$에 놓고, $R = R_z(90^\circ)$는 전과 같다. 패널 면 $x = 1$을 따라 $0.2\,\mathrm m$ 더 위다. 도구 프레임에서 잰 물체 스크류 축은 바뀌어 $\mathcal{B}_1 = (0,0,1;\ 0,2.2,0)$, $\mathcal{B}_2 = (0,0,1;\ 0,1.2,0)$이 된다(5단계의 '더 깊이' 메모). 도구를 바꾸면 공간 형식에서는 $M$ 하나가 새로 생기지만, 물체 형식에서는 관절마다 $\mathcal{B}_i$가 새로 생긴다.

### 출처 · Sources

- K. M. Lynch, F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — 4장 §4.1(공간 형식과 물체 형식의 지수 곱), 그리고 부록 C(Denavit–Hartenberg 파라미터). 책의 동반 소프트웨어가 `FKinSpace`를 구현하고, 무료 PDF는 [[04-robotics/modern-robotics-book|책 안내]]에 있다.
- 이 페이지의 자세와 행렬은 P2의 카탈로그 숫자로 여기서 직접 계산한 것이다. 믿지 말고 다시 계산하라.
