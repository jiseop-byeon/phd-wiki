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
> You need screw axes and the adjoint from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3–4]] and the closed form of $e^{[\mathcal{S}]\theta}$ from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]], plus multiplying 4×4 homogeneous transforms ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §3]]). The object is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]].
> [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3–4]]의 스크류 축과 adjoint, [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §5]]의 $e^{[\mathcal{S}]\theta}$ 닫힌 형태, 그리고 4×4 동차 변환의 곱([[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §3]])을 쓸 수 있어야 한다. 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**다.

## English

**Core question**: given joint angles $\theta$, where is the end-effector?

> [!note] First pass · 처음이라면
> Read the picture, the product-of-exponentials formula, and Steps 1–5 of the worked example (home pose, two screws, one evaluation, one geometric check) — that is the whole recipe. Then the Worked case's Steps 1, 2, 4 and 6: the catalog pose, and the wrong multiplication order that no orientation error warns you about. Step 3's closed-form exponential (from ch.3 §5) and Step 5's body form are second pass, and so is the D-H aside.

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

### The Product of Exponentials — one formula

$$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$

Read right-to-left: start at the home pose $M$ (all joints zero), then each joint screws
everything downstream of it. Two ingredients only: the home pose, and one screw axis per
joint *written in the fixed frame at the home position*. No intermediate link frames —
which is the advantage over Denavit-Hartenberg (D-H), the classical convention that attaches a frame to every link and describes each joint by four numbers relative to the previous link's frame (link length, twist, offset, joint angle; MR Appendix C; no wiki page covers it), and why MR's software library uses PoE (mainstream robot formats such as URDF still chain parent-to-child link frames).
(The **body form** $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots$ expresses the same thing
with axes in the end-effector frame.)

### Worked example, start to finish — planar 2R arm

Links $L_1 = L_2 = 1$, both stretched along $+\hat x$ at home. The general recipe, then
the numbers:

**Step 1 — home pose $M$.** End-effector at $(2, 0, 0)$, aligned with the base:
$$M = \begin{pmatrix} 1&0&0&2\\ 0&1&0&0\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**Step 2 — screw axis of joint 1.** Axis direction $\hat\omega_1 = (0,0,1)$; a point on
the axis $q_1 = (0,0,0)$; linear part $v_1 = -\hat\omega_1 \times q_1 = (0,0,0)$.
So $\mathcal{S}_1 = (0,0,1;\; 0,0,0)$.

**Step 3 — screw axis of joint 2.** $\hat\omega_2 = (0,0,1)$; $q_2 = (1,0,0)$;
$v_2 = -\hat\omega_2 \times q_2 = -(0,1,0) = (0,-1,0)$.
So $\mathcal{S}_2 = (0,0,1;\; 0,-1,0)$.

**Step 4 — evaluate at $\theta_1 = \theta_2 = 90°$.**
$e^{[\mathcal{S}_2]\,90°}$ rotates everything by 90° about the vertical axis through
$q_2 = (1,0,0)$. Apply it to $M$: the end-effector sits at $p - q_2 = (1,0,0)$ relative to
the axis; rotated 90° it becomes $(0,1,0)$; adding $q_2$ back gives $(1,1,0)$, with
orientation $R_z(90°)$. Then $e^{[\mathcal{S}_1]\,90°}$ rotates that result 90° about the
origin: $(1,1,0) \to (-1,1,0)$, orientation $R_z(180°)$:
$$T(90°, 90°) = \begin{pmatrix} -1&0&0&-1\\ 0&-1&0&1\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**Step 5 — sanity check against plain geometry.** $\theta_1 = 90°$ points link 1 along
$+\hat y$ (elbow at $(0,1)$); $\theta_2 = 90°$ adds another 90°, pointing link 2 along
$-\hat x$; tip $= (0,1) + (-1,0) = (-1, 1)$, total orientation $180°$. **Same answer.**
Do this double-check on every robot you model — geometric FK and PoE FK must agree.

<svg viewBox="0 0 540 210" style="max-width:100%;height:auto" role="img" aria-label="the planar 2R arm at home and at 90/90, with the tip reached by both routes">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="30" y1="150" x2="440" y2="150"/><line x1="70" y1="30" x2="70" y2="180"/></g>
  <g stroke="currentColor" stroke-width="2.2" fill="none" opacity="0.45" stroke-dasharray="6 4">
    <line x1="70" y1="150" x2="130" y2="150"/><line x1="130" y1="150" x2="190" y2="150"/>
  </g>
  <g fill="currentColor" opacity="0.5"><circle cx="130" cy="150" r="3.5"/><circle cx="190" cy="150" r="3.5"/></g>
  <g stroke="currentColor" stroke-width="2.6" fill="none">
    <line x1="70" y1="150" x2="70" y2="90"/><line x1="70" y1="90" x2="12" y2="90"/>
  </g>
  <g fill="currentColor"><circle cx="70" cy="150" r="4.5"/><circle cx="70" cy="90" r="4.5"/><circle cx="12" cy="90" r="4"/></g>
  <g font-size="11" fill="currentColor">
    <text x="112" y="186" opacity="0.7">home: both links along +x, tip at (2, 0)</text>
    <text x="80" y="124">link 1</text><text x="18" y="80">link 2</text>
    <text x="40" y="168">q<tspan dy="3.5">1</tspan><tspan dy="-3.5">=(0,0)</tspan></text><text x="112" y="168" opacity="0.7">q<tspan dy="3.5">2</tspan><tspan dy="-3.5">=(1,0)</tspan></text>
    <text x="232" y="52">at &#952;<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = &#952;</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90&#176;:</tspan></text>
    <text x="232" y="72">PoE:  tip &#8594; (1,1) &#8594; (&#8722;1, 1),  R = R_z(180&#176;)</text>
    <text x="232" y="92">geometry:  elbow (0,1), link 2 along &#8722;x</text>
    <text x="232" y="112">&#8594; tip (0,1) + (&#8722;1,0) = (&#8722;1, 1)  &#8212; same</text>
    <text x="232" y="138">dashed = home pose &#183; solid = &#952; = (90&#176;, 90&#176;)</text>
    <text x="20" y="206" opacity="0.85">Two routes, one tip. If they disagree, the screw axes or the home pose are wrong &#8212; check q first.</text>
  </g>
</svg>

### Worked case · 대상으로 한 번 끝까지

The same recipe on the catalog object, at the pose every later chapter quotes: plant **P2** at $\theta = (0^\circ, 90^\circ)$ ([[02-foundations/lab-plants|0.6]]). Nothing here is new machinery; the point is to produce the one $4\times4$ that the rest of the track means by "the frozen pose".

**Step 1 — the ingredients do not move.** $M$ and the screw axes were measured at the home pose, so the worked example's numbers (its Steps 1–3) carry over unchanged no matter what $\theta$ is asked for:

$$\mathcal{S}_1 = (0,0,1;\ 0,0,0), \qquad \mathcal{S}_2 = (0,0,1;\ 0,-1,0), \qquad M = \begin{pmatrix}1&0&0&2\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

because a screw axis is a property of the mechanism at home, not of the configuration being evaluated. Only $\theta$ changes between one FK call and the next.

**Step 2 — the first factor is the identity.** $\theta_1 = 0$, and $e^{[\mathcal{S}]\cdot 0} = I$ for every screw $\mathcal{S}$, so $T(0^\circ, 90^\circ) = e^{[\mathcal{S}_2](\pi/2)}M$. The shoulder contributes nothing and the elbow does all the work. This is a fact about this pose only, and step 6 shows what it costs to forget that.

**Step 3 — the elbow exponential, as a matrix.** For a screw with unit $\hat\omega$, the closed form is $e^{[\mathcal{S}]\theta} = \begin{pmatrix} e^{[\hat\omega]\theta} & G(\theta)v \\ 0 & 1\end{pmatrix}$ with $G(\theta) = I\theta + (1-\cos\theta)[\hat\omega] + (\theta - \sin\theta)[\hat\omega]^2$, the translation integrated along the screw — derived from the power series in [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]] (MR Prop. 3.25), which checks this very matrix. With $\hat\omega = \hat z$, $\theta = \pi/2$, $[\hat z]^2 = \mathrm{diag}(-1,-1,0)$ and the coefficients $1 - \cos(\pi/2) = 1$, $\pi/2 - \sin(\pi/2) = 0.5708$:

$$G = \begin{pmatrix}1&-1&0\\1&1&0\\0&0&\pi/2\end{pmatrix}, \qquad G\,v_2 = G\begin{pmatrix}0\\-1\\0\end{pmatrix} = \begin{pmatrix}1\\-1\\0\end{pmatrix}$$

since the first two diagonal entries are $\pi/2 - 0.5708 = 1$. Rodrigues supplies the rotation block, $e^{[\hat z](\pi/2)} = R_z(90^\circ)$, so

$$e^{[\mathcal{S}_2](\pi/2)} = \begin{pmatrix}0&-1&0&1\\1&0&0&-1\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$

**Step 4 — multiply by $M$.** Rotation: $R_z(90^\circ)\cdot I = R_z(90^\circ)$. Translation: $R_z(90^\circ)(2,0,0)^\top + (1,-1,0)^\top = (0,2,0)^\top + (1,-1,0)^\top = (1,1,0)^\top$. So

$$T(0^\circ, 90^\circ) = \begin{pmatrix}0&-1&0&1\\1&0&0&1\\0&0&1&0\\0&0&0&1\end{pmatrix}$$

where the translation column is the catalog tip $(1,1)$ and the rotation block carries the tool's $x$-axis onto $+\hat y_s$, because the elbow exponential turned the whole downstream link a quarter turn about the vertical through $q_2$. Geometry agrees in one line: elbow $(\cos 0^\circ, \sin 0^\circ) = (1,0)$, plus a unit forearm at absolute angle $\theta_1 + \theta_2 = 90^\circ$, giving $(1,0) + (0,1) = (1,1)$.

**Step 5 — the body form, as an independent check.** The body axes are the same screws measured from the tool frame at home, $\mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\mathcal{S}_i$ (the adjoint of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §4]]), which here gives $\mathcal{B}_1 = (0,0,1;\ 0,2,0)$ and $\mathcal{B}_2 = (0,0,1;\ 0,1,0)$ — the linear parts are literally the distances $2\,\mathrm{m}$ and $1\,\mathrm{m}$ from the tool back to each axis. Then $T = M\,e^{[\mathcal{B}_1]\theta_1}e^{[\mathcal{B}_2]\theta_2}$ multiplies out to the identical $4\times4$. Two formulations, one pose.

**Step 6 — what the identity was hiding.** Take the *other* worked pose, $\theta = (90^\circ, 90^\circ)$, where neither factor is $I$, and multiply the two exponentials in the wrong order. The correct product puts the tip at $(-1, 1)$; the swapped product $e^{[\mathcal{S}_2]\theta_2}e^{[\mathcal{S}_1]\theta_1}M$ puts it at $(-1, -1)$, with the *same* orientation $R_z(180^\circ)$. Two metres of position error and no orientation error to warn you — which is why the order is part of the formula, and why the catalog pose is a poor place to test a new FK implementation.

The recipe generalizes verbatim: home pose → per-joint $(\hat\omega_i, q_i)$ →
$v_i = -\hat\omega_i \times q_i$ → exponentials → multiply. For code, the Modern Robotics
Python library implements `FKinSpace(M, Slist, thetalist)` — verify your hand computation
against it once per mechanism.

**Wiki connections**: FK is the deterministic core inside every simulator and digital
twin ([[05-construction-robotics/index|construction]]); VLAs that output joint chunks
([[01-canonical-papers/notes/4-vla/pi0|π0]]) rely on FK to interpret them in task space.

### Self-check

1. For the same arm, compute $T(0°, 90°)$ — elbow position, tip position, orientation.
2. Why is $v_i = -\hat\omega_i \times q_i$? (What is the velocity of the origin-coincident
   point when the body rotates about the axis through $q_i$?)
3. In the body form, which joint's exponential sits closest to $M$, and why?

> [!tip]- Answers
> 1. Joint 1 is at zero, so the elbow stays at $(1,0)$; joint 2 rotates link 2 by 90° about the axis through $q_2$, pointing it along $+\hat y$. Tip $= (1,1,0)$, orientation $R_z(90°)$. Check geometrically: $(1,0) + (0,1) = (1,1)$. ✓
> 2. Because the axis passes through $q_i$, the body point *currently coincident with the origin* sits at $-q_i$ relative to the axis, so its velocity is $\omega\times(0 - q_i) = -\omega\times q_i$ — literally the "what $v$ means" warning of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §3]].
> 3. **Joint 1.** The body form is $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}$ (MR eq. 4.16), so $e^{[\mathcal{B}_1]\theta_1}$ sits against $M$. The joint order is **not** reversed — it runs $1 \ldots n$ in both forms; what changes is which side $M$ sits on (right in the space form, left in the body form) and that the axes are written in the end-effector frame.

### Problem set · 과제

Tier B. **P2** at the frozen pose of [[02-foundations/lab-plants|0.6]]. Home and screws as on this page. No simulator.

1. **Draw.** The picture above for $\theta=(45^\circ,45^\circ)$, the pose where the shoulder moves too: dashed home (both links along $+x$, tip at $(2,0)$) and the solid evaluated arm, with the screw axes and the frames at the base, at $q_2=(1,0,0)$ and at the tip. Beside the arms, the matrix route and the geometric route to the tip. Where would the tip land if you skipped the first exponential?
2. **Derive.** Write $\mathcal{S}_1$, $\mathcal{S}_2$, and $M$. From geometry: elbow, tip, $R$ at $\theta=(0^\circ,90^\circ)$. Why is $e^{[\mathcal{S}_1]\theta_1}=I$ here, and what is $T$?
3. **Interpret.** When does skipping the first exponential fail, and what must still match PoE if it does?

> [!note]- How to draw it · 그리는 법
> - The home arm dashed: both links along $+\hat x$, elbow at $(1,0)$, tip at $(2,0)$. This is where $M$ is read — a fact about the model, not about where the robot is now.
> - The evaluated arm solid: elbow at $(\cos45^\circ,\ \sin45^\circ)=(0.707,\ 0.707)$, tip one more unit along the absolute angle $90^\circ$, at $(0.707,\ 1.707)$. Now $\theta_1\ne0$, so the two arms no longer share link 1: draw them apart.
> - The screw axes on the home drawing and nowhere else: a circled dot at each $q_i$, labelled with $\hat\omega_i=(0,0,1)$ and its linear part $v_i=-\hat\omega_i\times q_i$. The solid elbow is at $(0.707,\ 0.707)$, not at $q_2$; marking $\mathcal{S}_2$ there is the most common way this figure goes wrong.
> - Three frames as small pairs of labelled arrows: $\{s\}$ at the base, one at $q_2$ on the home arm, and the tool frame at the solid tip with its $x$-axis along the forearm, straight up.
> - Beside the figure, two independent lines that must agree: the matrix route $T=e^{[\mathcal{S}_1]\theta_1}e^{[\mathcal{S}_2]\theta_2}M$ and the geometric route, elbow $+$ forearm.
> - A faint third arm for the shortcut that skips $e^{[\mathcal{S}_1]\theta_1}$: $e^{[\mathcal{S}_2]\theta_2}M$ alone puts the tip at $(1.707,\ 0.707)$ with $R=R_z(45^\circ)$, $1.414\,\mathrm{m}$ from the true tip. That gap is item 3's answer, drawn.

> [!tip]- Solutions
> 1. Home stretched along $+x$. Evaluated arm: elbow $(0.707,\ 0.707)$, tip $(0.707,\ 1.707)$, forearm along $+y$, so $R=R_z(90^\circ)$. Matrix route: $e^{[\mathcal{S}_2]\pi/4}M$ turns $M$ about $q_2$ to tip $(1.707,\ 0.707)$ with $R=R_z(45^\circ)$; $e^{[\mathcal{S}_1]\pi/4}$ then turns that about the origin to tip $(0.707,\ 1.707)$ with $R=R_z(90^\circ)$ — the geometric route's answer. Skipping the first exponential leaves the tip at $(1.707,\ 0.707)$, $\sqrt2=1.414\,\mathrm{m}$ off: the shortcut of item 2 holds only because $\theta_1=0$ at the frozen pose.
> 2. $\mathcal{S}_1=(0,0,1;\,0,0,0)$, $\mathcal{S}_2=(0,0,1;\,0,-1,0)$, $M$ has $p=(2,0,0)$ and $R=I$. $\theta_1=0$ so the first factor is $I$. Joint 2 rotates $M$ about $q_2$: tip $(1,1)$, $R=R_z(90^\circ)$. Same $T$ as Self-check 1 — now named **P2**.
> 3. The shortcut fails as soon as the shoulder moves; then the product order matters. Geometric FK and PoE must still agree.

## 한국어

**핵심 질문**: 관절 각 $\theta$가 주어지면 말단은 어디에 있는가?

> [!note] 처음이라면 · First pass
> 그림, 지수 곱 공식, 그리고 계산 예제의 1–5단계(홈 자세, 스크류 둘, 한 번의 평가, 기하 검산 하나)를 읽어라. 레시피 전부가 거기 있다. 그다음 '대상으로 한 번 끝까지'의 1·2·4·6단계를 읽는다. 카탈로그 자세, 그리고 어떤 방향 오차도 경고해 주지 않는 잘못된 곱 순서다. 3단계의 닫힌 형태 지수(3장 §5에서 온다)와 5단계의 바디 형식은 두 번째 읽기이고, D-H 여담도 그렇다.

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

### 지수 곱 공식 — 단 하나의 공식

$$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$

오른쪽에서 왼쪽으로 읽어라: 홈 자세 $M$(모든 관절 0)에서 시작해, 각 관절이 자기 하류
전체를 스크류로 돌린다. 재료는 둘뿐이다: 홈 자세, 그리고 관절마다 *홈 위치에서 고정
프레임 기준으로 쓴* 스크류 축 하나. 중간 링크 프레임이 필요 없다 — 이것이 D-H(Denavit-Hartenberg) 대비
장점이고(D-H는 링크마다 프레임을 붙이고 각 관절을 이전 링크 프레임에 대한 네 숫자 — 링크 길이, 비틀림, 오프셋, 관절각 — 로 기술하는 고전 규약이다; MR 부록 C, 위키에는 별도 페이지가 없다) MR의 소프트웨어 라이브러리가 PoE를 쓰는 이유다(URDF 같은 주류 로봇 형식은 여전히 부모–자식 링크 프레임을 잇는다). (**바디 형식**
$T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots$은 축을 말단 프레임에서 쓴 같은 내용이다.)

### 처음부터 끝까지 계산 예제 — 평면 2R 팔

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
$e^{[\mathcal{S}_2]\,90°}$는 $q_2 = (1,0,0)$를 지나는 수직축 둘레로 모든 것을 90° 돌린다.
$M$에 적용하면: 말단은 축 기준 $p - q_2 = (1,0,0)$에 있고, 90° 돌리면 $(0,1,0)$, $q_2$를
되더하면 $(1,1,0)$, 방향은 $R_z(90°)$. 그다음 $e^{[\mathcal{S}_1]\,90°}$가 그 결과를 원점
둘레로 90° 돌린다: $(1,1,0) \to (-1,1,0)$, 방향 $R_z(180°)$:
$$T(90°, 90°) = \begin{pmatrix} -1&0&0&-1\\ 0&-1&0&1\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**5단계 — 순수 기하로 검산.** $\theta_1 = 90°$면 링크 1이 $+\hat y$ 방향(팔꿈치
$(0,1)$); $\theta_2 = 90°$가 90°를 더해 링크 2는 $-\hat x$ 방향; 끝점 $= (0,1) + (-1,0)
= (-1, 1)$, 총 방향 $180°$. **같은 답이다.** 모델링하는 모든 로봇에서 이 이중 검산을
하라 — 기하 FK와 PoE FK는 반드시 일치해야 한다.

<svg viewBox="0 0 540 210" style="max-width:100%;height:auto" role="img" aria-label="home 자세와 90/90에서의 평면 2R 팔, 두 경로로 도달한 끝점">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="30" y1="150" x2="440" y2="150"/><line x1="70" y1="30" x2="70" y2="180"/></g>
  <g stroke="currentColor" stroke-width="2.2" fill="none" opacity="0.45" stroke-dasharray="6 4">
    <line x1="70" y1="150" x2="130" y2="150"/><line x1="130" y1="150" x2="190" y2="150"/>
  </g>
  <g fill="currentColor" opacity="0.5"><circle cx="130" cy="150" r="3.5"/><circle cx="190" cy="150" r="3.5"/></g>
  <g stroke="currentColor" stroke-width="2.6" fill="none">
    <line x1="70" y1="150" x2="70" y2="90"/><line x1="70" y1="90" x2="12" y2="90"/>
  </g>
  <g fill="currentColor"><circle cx="70" cy="150" r="4.5"/><circle cx="70" cy="90" r="4.5"/><circle cx="12" cy="90" r="4"/></g>
  <g font-size="11" fill="currentColor">
    <text x="112" y="186" opacity="0.7">home: 두 링크 모두 +x, 끝점 (2, 0)</text>
    <text x="80" y="124">링크 1</text><text x="18" y="80">링크 2</text>
    <text x="40" y="168">q<tspan dy="3.5">1</tspan><tspan dy="-3.5">=(0,0)</tspan></text><text x="112" y="168" opacity="0.7">q<tspan dy="3.5">2</tspan><tspan dy="-3.5">=(1,0)</tspan></text>
    <text x="232" y="52">&#952;<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = &#952;</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90&#176;일 때:</tspan></text>
    <text x="232" y="72">PoE:  끝점 &#8594; (1,1) &#8594; (&#8722;1, 1),  R = R_z(180&#176;)</text>
    <text x="232" y="92">기하:  팔꿈치 (0,1), 링크 2는 &#8722;x 방향</text>
    <text x="232" y="112">&#8594; 끝점 (0,1) + (&#8722;1,0) = (&#8722;1, 1)  &#8212; 같다</text>
    <text x="232" y="138">점선 = home 자세 &#183; 실선 = &#952; = (90&#176;, 90&#176;)</text>
    <text x="20" y="206" opacity="0.85">두 경로, 하나의 끝점. 어긋나면 스크류 축이나 home 자세가 틀린 것이다 &#8212; q부터 확인하라.</text>
  </g>
</svg>



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

이다. 병진 열이 카탈로그 말단 $(1,1)$이고 회전 블록이 도구의 $x$축을 $+\hat y_s$로 옮기는데, 엘보 지수가 $q_2$를 지나는 연직축 둘레로 하류 링크 전체를 4분의 1바퀴 돌렸기 때문이다. 기하도 한 줄이다. 엘보 $(\cos 0^\circ, \sin 0^\circ) = (1,0)$에 절대각 $\theta_1 + \theta_2 = 90^\circ$인 단위 전완을 더해 $(1,0) + (0,1) = (1,1)$.

**5단계 — 바디 형식으로 독립 검산.** 바디 축은 같은 스크류를 홈에서 도구 프레임 기준으로 잰 것, 곧 $\mathcal{B}_i = [\mathrm{Ad}_{M^{-1}}]\mathcal{S}_i$다([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §4]]의 adjoint). 여기서는 $\mathcal{B}_1 = (0,0,1;\ 0,2,0)$, $\mathcal{B}_2 = (0,0,1;\ 0,1,0)$이고, 선형부가 말 그대로 도구에서 각 축까지의 거리 $2\,\mathrm{m}$와 $1\,\mathrm{m}$다. $T = M\,e^{[\mathcal{B}_1]\theta_1}e^{[\mathcal{B}_2]\theta_2}$를 곱하면 같은 $4\times4$가 나온다. 정식화 둘, 자세 하나.

**6단계 — 항등이 가리고 있던 것.** 두 인자 중 어느 쪽도 $I$가 아닌 다른 계산 자세 $\theta = (90^\circ, 90^\circ)$에서 두 지수를 일부러 반대 순서로 곱해 보자. 올바른 곱은 말단을 $(-1, 1)$에 놓고, 뒤바꾼 곱 $e^{[\mathcal{S}_2]\theta_2}e^{[\mathcal{S}_1]\theta_1}M$은 $(-1, -1)$에 놓는다. 방향은 *둘 다* $R_z(180^\circ)$로 같다. 위치 오차 2 m에 경고가 될 방향 오차는 0이다. 순서가 공식의 일부인 이유이고, 새 FK 구현을 시험하기에 카탈로그 자세가 나쁜 자리인 이유다.

레시피는 그대로 일반화된다: 홈 자세 → 관절별 $(\hat\omega_i, q_i)$ →
$v_i = -\hat\omega_i \times q_i$ → 지수들 → 곱. 코드로는 Modern Robotics 파이썬
라이브러리의 `FKinSpace(M, Slist, thetalist)`가 이것을 구현한다 — 기구마다 한 번은
손계산과 라이브러리 결과를 대조하라.

**위키 연결**: FK는 모든 시뮬레이터·디지털 트윈([[05-construction-robotics/index|건설]])
안의 결정론적 핵심이고, 관절 청크를 출력하는 VLA([[01-canonical-papers/notes/4-vla/pi0|π0]])를
작업공간(operational space)에서 해석하는 데 쓰인다.

### 스스로 점검

1. 같은 팔에서 $T(0°, 90°)$를 계산하라 — 팔꿈치 위치, 끝점 위치, 방향.
2. 왜 $v_i = -\hat\omega_i \times q_i$인가? ($q_i$를 지나는 축 둘레로 돌 때, 원점과 겹친
   몸체 점의 속도는 무엇인가?)
3. 바디 형식에서는 어느 관절의 지수가 $M$에 가장 가까이 붙는가? 왜인가?

> [!tip]- 정답 · Answers
> 1. 관절 1이 0이라 팔꿈치는 $(1,0)$에 그대로; 관절 2가 $q_2$를 지나는 축 둘레로 링크 2를 90° 돌려 $+\hat y$ 방향 → 끝점 $(1,1,0)$; 방향 $R_z(90°)$. 기하로 검산: $(1,0) + (0,1) = (1,1)$. ✓
> 2. 원점과 겹친 몸체 점은 축에서 $-q_i$만큼 떨어져 있으므로 속도는 $\omega\times(0 - q_i) = -\omega\times q_i$ — [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3]]의 $v$ 정의 그대로.
> 3. **관절 1.** 바디 형식은 $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}$(MR 식 4.16)이므로 $e^{[\mathcal{B}_1]\theta_1}$이 $M$에 붙는다. 곱 순서는 **뒤집히지 않는다** — 두 형식 모두 $1 \ldots n$이고, 달라지는 것은 $M$이 어느 쪽에 오는지(공간 형식은 오른쪽, 바디 형식은 왼쪽)와 축을 말단 프레임에서 쓴다는 점이다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 고정 자세 **P2**. 홈과 스크류는 이 페이지. 시뮬레이터 없음.

1. **그리기.** 어깨도 움직이는 자세 $\theta=(45^\circ,45^\circ)$에 대한 위의 그림: 점선 홈(두 링크 $+x$, 말단 $(2,0)$)과 실선으로 그린 평가 자세의 팔, 스크류 축, 그리고 베이스·$q_2=(1,0,0)$·말단의 프레임. 팔 옆에 말단까지의 행렬 경로와 기하 경로를 적어라. 첫 지수를 건너뛰었다면 말단은 어디에 떨어졌겠는가?
2. **유도.** $\mathcal{S}_1$, $\mathcal{S}_2$, $M$. 기하로 $\theta=(0^\circ,90^\circ)$의 엘보·말단·$R$. 왜 $e^{[\mathcal{S}_1]\theta_1}=I$이고 $T$는?
3. **해석.** 첫 지수를 건너뛰는 지름길이 언제 깨지고, 그래도 PoE와 무엇이 맞아야 하는가?

> [!note]- 그리는 법 · How to draw it
> - 홈 자세의 팔은 점선. 두 링크 모두 $+\hat x$, 엘보 $(1,0)$, 말단 $(2,0)$. $M$을 읽는 곳이며, 로봇이 지금 어디 있는지가 아니라 모형에 대한 사실이다.
> - 평가할 자세의 팔은 실선. 엘보는 $(\cos45^\circ,\ \sin45^\circ)=(0.707,\ 0.707)$, 말단은 거기서 절대각 $90^\circ$ 방향으로 한 단위 더 간 $(0.707,\ 1.707)$. 이제 $\theta_1\ne0$이므로 두 팔은 링크 1을 공유하지 않는다. 떨어뜨려 그린다.
> - 스크류 축은 홈 그림에만 표시한다. 각 $q_i$에 동그라미 친 점을 찍고 $\hat\omega_i=(0,0,1)$과 선형부 $v_i=-\hat\omega_i\times q_i$를 적는다. 실선 엘보는 $q_2$가 아니라 $(0.707,\ 0.707)$에 있고, $\mathcal{S}_2$를 거기에 표시하는 것이 이 그림이 틀리는 가장 흔한 방식이다.
> - 프레임 셋을 이름 붙인 짧은 화살표 쌍으로. 베이스의 $\{s\}$, 홈 팔의 $q_2$에 하나, 그리고 실선 말단의 도구 프레임이고, 도구 프레임의 $x$축은 전완 방향, 곧 곧장 위다.
> - 그림 옆에는 서로 맞아야 하는 두 줄을 독립적으로 적는다. 행렬 경로 $T=e^{[\mathcal{S}_1]\theta_1}e^{[\mathcal{S}_2]\theta_2}M$과 기하 경로 엘보 $+$ 전완이다.
> - $e^{[\mathcal{S}_1]\theta_1}$을 건너뛰는 지름길의 셋째 팔을 흐리게: $e^{[\mathcal{S}_2]\theta_2}M$만으로는 말단이 $(1.707,\ 0.707)$, $R=R_z(45^\circ)$에 놓여 참 말단에서 $1.414\,\mathrm{m}$ 떨어진다. 그 간격이 3번의 답을 그린 것이다.

> [!tip]- 정답 · Solutions
> 1. 홈은 $+x$로 뻗음. 평가 자세: 엘보 $(0.707,\ 0.707)$, 말단 $(0.707,\ 1.707)$, 전완은 $+y$ 방향이라 $R=R_z(90^\circ)$. 행렬 경로: $e^{[\mathcal{S}_2]\pi/4}M$이 $M$을 $q_2$ 둘레로 돌려 말단을 $(1.707,\ 0.707)$, $R=R_z(45^\circ)$에 놓고, $e^{[\mathcal{S}_1]\pi/4}$가 그것을 원점 둘레로 돌려 말단 $(0.707,\ 1.707)$, $R=R_z(90^\circ)$ — 기하 경로의 답과 같다. 첫 지수를 건너뛰면 말단은 $(1.707,\ 0.707)$에 남아 $\sqrt2=1.414\,\mathrm{m}$ 어긋난다. 2번의 지름길은 고정 자세에서 $\theta_1=0$이기 때문에만 성립한다.
> 2. $\mathcal{S}_1=(0,0,1;\,0,0,0)$, $\mathcal{S}_2=(0,0,1;\,0,-1,0)$, $M$의 $p=(2,0,0)$, $R=I$. $\theta_1=0$이라 첫 인자는 $I$. 관절 2가 $M$을 $q_2$ 둘레로 돌려 말단 $(1,1)$, $R=R_z(90^\circ)$. 스스로 점검 1과 같은 $T$ — 이제 이름이 **P2**.
> 3. 어깨가 움직이는 순간 곱 순서가 필요하다. 기하 FK와 PoE는 여전히 같아야 한다.
