---
title: "MR Ch.06 — Inverse Kinematics"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.6** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the Jacobian and its resolved-rate loop from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]], least squares ([[02-foundations/linear-algebra|1. Linear Algebra §2]]) and the pseudoinverse with its damped form ([[02-foundations/linear-algebra|1. Linear Algebra §4.5]]), and Newton's method ([[02-foundations/optimization|4. Optimization §3]]); §2's full-pose error uses the matrix logarithm of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]] and the home configuration and body screws of [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]]. The object is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled; P2 is the catalog's planar two-link arm).
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안과 분해 속도 루프, 최소제곱([[02-foundations/linear-algebra|1. 선형대수 §2]]), 유사역행렬과 그 감쇠 형태([[02-foundations/linear-algebra|1. 선형대수 §4.5]]), 뉴턴법([[02-foundations/optimization|4. 최적화 §3]])을 알고 있어야 한다. §2의 자세 전체 오차는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §5]]의 행렬 로그와 [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 홈 컨피규레이션과 물체 스크류를 쓴다. 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**다(장치(plant)는 제어 공학에서 제어 대상 시스템을 부르는 말이고, P2는 카탈로그의 평면 2링크 팔이다).

## English

**Core question**: given a desired end-effector pose, what joint angles achieve it?

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] inverse kinematics turns a tool target into joint angles in the manipulation layer, and in *"install that panel on the frame"* it serves *move the component*, the step the [[physical-ai-map|Physical AI Map]] already files it under (its chip sits in the manipulation band): the panel point is given in the task space, but the motors need a $\theta$. Without it a solver fails in ways that look alike: average the two exact solutions that put **P2**, the catalog's planar two-link arm ([[02-foundations/lab-plants|0.6]]), on the panel point $(1,1)$, and the arm straightens to $(45^\circ, 0^\circ)$, $0.586\,\mathrm{m}$ past the target on a singularity where no step, damped or not, moves it; ten degrees off that seed the undamped step throws the joints $7.51\,\mathrm{rad}$ and the error grows from $0.596$ to $3.33\,\mathrm{m}$ (Worked case, Steps 3–5). Later pages depend on it — [[04-robotics/ros2/manipulation-moveit2|25.8 MoveIt 2 §1 and §7]] calls IK solvers and builds Cartesian paths on this loop, [[04-robotics/robot-systems-deployment|10. Robot Systems §2]] routes end-effector actions through it, [[04-robotics/planning-decision-making|4. Planning & Decision-Making §1]] places it between path and controller, and the [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] note meets Step 3's failure again in demonstrations, where averaging two valid modes gives an invalid action — in block 2 of the dissertation path ([[07-research-program/index|7. Research Program §8]], robotics sessions 16–18). After it you can list every IK branch of P2 analytically, run and diagnose a Newton–Raphson IK, and choose damping or a new seed when it stalls or jumps.

> [!note] First pass · 처음이라면
> About three 60–90-minute sessions, robotics 16–18. **Session 1:** the Running object, the picture and the whole Worked case by hand — the two analytic branches, why their mean is not a solution, and what a solver does seeded on the singularity (Step 4) and ten degrees off it (Step 5), using the damped step whose formula Step 4 writes down. End by explaining, page closed, why the seed $(45^\circ, 0^\circ)$ gets no step for any damping $\lambda$ while $(45^\circ, 10^\circ)$ gets a wild one: two failures that look alike and need opposite fixes. **Session 2:** §1–§4 — the problem and analytic IK defined, Newton–Raphson with its full-pose error, §3's iteration by hand, and §4's damped least squares, whose example is Step 5's numbers again. **Session 3:** the self-check and the problem set. The collapsed *Deeper* notes are second pass.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's planar two-link arm — unit links, $\theta_1$ from the $+x$ axis, the elbow angle $\theta_2$ relative to link 1, a "2R" arm with two revolute (rotating) joints — and its catalog target, the tip at $(1,1)$: the point on the face $x = 1$ of ch.2's panel where the running task makes contact. The catalog's frozen pose $(0^\circ, 90^\circ)$ is one IK solution of that target; this page finds all of them and asks what a numerical solver does from a bad seed.

*Scope: this page teaches IK on P2 — the analytic branches, Newton–Raphson on the tip error and on the full pose, and damped least squares. Whether the way to the target is free is [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]]; the joint rates for a moving target are [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §2]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 292" style="max-width:100%;height:auto" role="img" aria-label="P2 reaching the target (1, 1) with two IK branches, elbow at (1, 0) and at (0, 1); their joint-space mean is a straight arm whose tip (1.414, 1.414) overshoots by 0.586 m, where the only reachable direction is perpendicular to the wanted one.">
  <defs><marker id="mr06hdE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="0.8" opacity="0.25"><line x1="38.8" y1="256" x2="307.5" y2="256"/><line x1="70" y1="268.5" x2="70" y2="37.2"/></g>
  <polyline points="70,256 70,131 195,131" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round" opacity="0.42"/>
  <polyline points="70,256 195,256 195,131" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>
  <polyline points="70,256 158.4,167.6 238.3,87.7" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4" opacity="0.75"/>
  <circle cx="70" cy="256" r="4.8" fill="currentColor"/>
  <circle cx="195" cy="256" r="3.8" fill="currentColor"/>
  <circle cx="70" cy="131" r="3.8" fill="currentColor" fill-opacity="0.42"/>
  <circle cx="158.4" cy="167.6" r="3" fill="currentColor" fill-opacity="0.75"/>
  <circle cx="195" cy="131" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <g stroke="currentColor" stroke-width="2.2"><line x1="242.6" y1="75" x2="251" y2="83.4"/><line x1="242.6" y1="83.4" x2="251" y2="75"/></g>
  <g stroke="currentColor" stroke-width="1.8" marker-end="url(#mr06hdE)"><line x1="238.3" y1="70.7" x2="220.3" y2="52.7"/><line x1="255.3" y1="87.7" x2="273.3" y2="105.7"/></g>
  <line x1="223.4" y1="91.2" x2="194.6" y2="120" stroke="currentColor" stroke-width="2.4" marker-end="url(#mr06hdE)"/>
  <polyline points="236.9,89.1 227,79.2 236.9,69.3" fill="none" stroke="currentColor" stroke-width="1" opacity="0.85"/>
  <line x1="340" y1="14" x2="340" y2="276" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="215.3" y="46.7" text-anchor="end">reachable</text>
    <text x="205.9" y="92.1" text-anchor="end">wanted</text>
    <text x="226.9" y="126.1">miss 0.586 m</text>
    <text x="257.8" y="76.2">(1.414, 1.414)</text>
    <text x="206" y="153">target (1, 1)</text>
    <text x="195" y="274" text-anchor="middle">elbow A (1, 0)</text>
    <text x="61" y="135" text-anchor="end" opacity="0.75">(0, 1)</text>
    <text x="61" y="149" text-anchor="end" opacity="0.75">elbow B</text>
    <text x="132.5" y="122" text-anchor="middle" opacity="0.75">B (90°, −90°)</text>
    <text x="204" y="223.5">A (0°, 90°)</text>
    <text x="145" y="241" text-anchor="middle" opacity="0.85">mean (45°, 0°)</text>
    <text x="70" y="274" text-anchor="middle" opacity="0.8">base</text>
    <text x="352" y="26" font-size="12">Two exact IK solutions</text>
    <text x="358" y="45">A = (0°, 90°), elbow (1, 0)</text>
    <text x="358" y="62">B = (90°, −90°), elbow (0, 1)</text>
    <text x="352" y="91" font-size="12">Their mean (45°, 0°) is not one</text>
    <text x="358" y="110">tip (√2, √2), miss 0.5858 m</text>
    <text x="358" y="127">= 41 % of the target's 1.414 m</text>
    <text x="352" y="156" font-size="12">At the mean, J has rank 1</text>
    <text x="358" y="175">σ = (2.2361, 0)</text>
    <text x="358" y="192">reachable (−0.7071, 0.7071)</text>
    <text x="358" y="209">wanted e = (−0.4142, −0.4142)</text>
    <text x="358" y="226">Jᵀe = (0, 0): no step, for every λ</text>
  </g>
</svg>

Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] reaching the catalog target $(1,1)$, the point on the panel face, on two exact IK branches: A, $(0^\circ, 90^\circ)$, with its elbow at $(1,0)$, and B, $(90^\circ, -90^\circ)$, with its elbow at $(0,1)$ — same tip, two different arms. Their componentwise mean $(45^\circ, 0^\circ)$ is the dashed straight arm, whose tip $(\sqrt2, \sqrt2) = (1.414, 1.414)$ overshoots by $0.586\,\mathrm{m}$, $41\,\%$ of the target's distance. At that tip $J$ has rank 1, $\sigma = (2.2361,\ 0)$: the only reachable direction is perpendicular to the arm while the wanted one runs back along it, so $J^\top e = (0,0)$ and there is no step at all, for every damping $\lambda$.

### Worked case · 대상으로 한 번 끝까지

Analytic IK on **P2** for the catalog target, then one numerical step from the worst possible seed. Every number here is exact.

**Step 1 — the elbow angle, from the law of cosines.** Squaring and adding the two FK equations kills $\theta_1$ and leaves $x^2 + y^2 = L_1^2 + L_2^2 + 2L_1L_2\cos\theta_2$, because the cross terms collapse by $\cos\theta_1\cos(\theta_1{+}\theta_2) + \sin\theta_1\sin(\theta_1{+}\theta_2) = \cos\theta_2$. Solving for the elbow:

$$\cos\theta_2 = \frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2} = \frac{1 + 1 - 1 - 1}{2} = 0 \quad\Longrightarrow\quad \theta_2 = \pm 90^\circ$$

and the $\pm$ is where multiple solutions come from: the equation fixes $\cos\theta_2$, never $\theta_2$ itself. The target is reachable exactly when this cosine lands in $[-1, 1]$, which is the clean test for "no solution".

**Step 2 — the shoulder angle, one per branch.** With $\theta_2$ chosen, the arm becomes a rigid triangle and the tip's bearing from the base splits into two pieces — where the target lies, minus how far the folded forearm swings the tip off link 1's own direction. Both pieces are angles of points, which is why they use $\operatorname{atan2}(y, x)$, the two-argument arctangent: the angle of the point $(x, y)$ over the full circle, which keeps both signs and so never confuses opposite quadrants:

$$\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2)$$

and the second term flips sign with $\theta_2$, so the two elbow choices give two different shoulder angles rather than one. For $\theta_2 = +90^\circ$: $\operatorname{atan2}(1,1) - \operatorname{atan2}(1, 1) = 45^\circ - 45^\circ = 0^\circ$, giving $\theta = (0^\circ, 90^\circ)$. For $\theta_2 = -90^\circ$: $45^\circ - \operatorname{atan2}(-1, 1) = 45^\circ - (-45^\circ) = 90^\circ$, giving $\theta = (90^\circ, -90^\circ)$. Both check against FK: $(\cos 0^\circ + \cos 90^\circ,\ \sin 0^\circ + \sin 90^\circ) = (1,1)$ and $(\cos 90^\circ + \cos 0^\circ,\ \sin 90^\circ + \sin 0^\circ) = (1,1)$. The first is the catalog frozen pose; nothing on this page chose it over the other, the catalog did.

**Step 3 — why the average is not an answer, in numbers.** The componentwise mean is $(45^\circ, 0^\circ)$, a straight arm, tip at $(\sqrt2, \sqrt2)$, a miss of $\sqrt{2(\sqrt2 - 1)^2} = 0.5858\,\mathrm{m}$ on a target $1.414\,\mathrm{m}$ from the base — a $41\,\%$ overshoot, not a rounding error. The set of IK solutions is not convex, and averaging is exactly the operation that assumes it is.

**Step 4 — hand the mean configuration to a numerical solver and watch nothing happen.** Seed Newton IK — repeat the step $\Delta\theta = J^\dagger e$ on the tip error $e$, derived in §2 — at $\theta^{(0)} = (45^\circ, 0^\circ)$. With $s_1 = c_1 = s_{12} = c_{12} = 0.7071$ the ch.5 formula gives

$$J = \begin{pmatrix}-1.4142 & -0.7071\\ 1.4142 & 0.7071\end{pmatrix}, \qquad \det J = L_1L_2\sin\theta_2 = 0, \qquad \sigma = (2.2361,\ 0)$$

so the map has rank 1, because its two columns are parallel: its one reachable direction is $(-0.7071, 0.7071)$, perpendicular to the arm. The error is $e = (1,1) - (\sqrt2,\sqrt2) = (-0.4142, -0.4142)$, which points straight back *along* the arm. Then

$$J^\top e = \begin{pmatrix}-1.4142 & 1.4142\\ -0.7071 & 0.7071\end{pmatrix}\begin{pmatrix}-0.4142\\ -0.4142\end{pmatrix} = \begin{pmatrix}0.5858 - 0.5858\\ 0.2929 - 0.2929\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}$$

and every update built on $J^\top$ inherits that zero: the pseudoinverse step is $0$, and so is the damped step $J^\top(JJ^\top + \lambda^2 I)^{-1}e$ (damped least squares, the singularity fix of §4) for **every** $\lambda$, because the damping only changes what multiplies a vector that is already zero. The solver terminates on "no progress" while standing $58.6\,\mathrm{cm}$ from a target that has two exact solutions. Damping is the wrong medicine here; a different seed is the only cure.

**Step 5 — ten degrees off the singularity is a different failure.** Move the seed to $(45^\circ, 10^\circ)$ so the arm is merely *nearly* straight: now $\det J = \sin 10^\circ = 0.1736$ and $\sigma = (2.2279,\ 0.0779)$. The error $\|e\| = 0.5964$ divided by that smallest singular value is what sets the step size, and the undamped update is a joint move of $\|\Delta\theta\| = 7.51\,\mathrm{rad}$ — it hurls the tip to $(-1.32, -1.39)$ and drives $\|e\|$ from $0.596$ up to $3.33$. Damping at $\lambda = 0.3$ instead steps to $(30.3^\circ, 33.1^\circ)$ and brings $\|e\|$ down to $0.506$: smaller than the exact least-squares step, and in the right direction. **Exactly singular means no step; nearly singular means a wild one.** They look alike on a plot of $\|e\|$ and need opposite fixes.

<svg viewBox="0 0 560 348" style="max-width:100%;height:auto" role="img" aria-label="P2 drawn to scale for one step from the nearly straight seed (45°, 10°) toward the target (1, 1): the undamped step moves the joints 7.51 rad and throws the tip to (−1.32, −1.39); the damped step at λ = 0.3 goes to (30.3°, 33.1°) with error 0.506 m. Right: the gain along a singular direction σ, 1/σ against σ/(σ² + λ²).">
  <defs><marker id="mr06s5e" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <circle cx="150.0" cy="160.0" r="128.0" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.45"/>
  <g stroke="currentColor" stroke-width="0.8" opacity="0.25"><line x1="15.6" y1="160.0" x2="284.4" y2="160.0"/><line x1="150.0" y1="294.4" x2="150.0" y2="25.6"/></g>
  <polyline points="150.0,160.0 195.3,114.7 232.0,62.3" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" opacity="0.4"/>
  <polyline points="150.0,160.0 94.4,191.7 65.6,248.8" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4" stroke-linejoin="round"/>
  <polyline points="150.0,160.0 205.3,127.7 234.0,70.6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="195.3" cy="114.7" r="3" fill="currentColor" fill-opacity="0.4"/>
  <circle cx="94.4" cy="191.7" r="3" fill="currentColor" fill-opacity="1"/>
  <circle cx="205.3" cy="127.7" r="3" fill="currentColor" fill-opacity="1"/>
  <circle cx="150.0" cy="160.0" r="4.5" fill="currentColor"/>
  <circle cx="214.0" cy="96.0" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <g stroke="currentColor" stroke-width="2"><line x1="61.6" y1="244.8" x2="69.6" y2="252.8"/><line x1="61.6" y1="252.8" x2="69.6" y2="244.8"/></g>
  <g font-size="11" fill="currentColor">
    <text x="224.0" y="112.0">target (1, 1)</text>
    <text x="74.6" y="252.8">(−1.32, −1.39)</text>
    <text x="143.0" y="153.0" text-anchor="end" opacity="0.8">base</text>
    <text x="220.0" y="278.8" opacity="0.6">reach 2 m</text>
  </g>
  <g stroke="currentColor">
    <line x1="14" y1="302" x2="38" y2="302" stroke-width="2.6" opacity="0.4"/>
    <line x1="14" y1="320" x2="38" y2="320" stroke-width="2" stroke-dasharray="6 4"/>
    <line x1="14" y1="338" x2="38" y2="338" stroke-width="2.6"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="46" y="306">seed (45°, 10°): ‖e‖ = 0.596</text>
    <text x="46" y="324">undamped: joints move 7.51 rad, ‖e‖ = 3.33</text>
    <text x="46" y="342">damped, λ = 0.3: (30.3°, 33.1°), ‖e‖ = 0.506</text>
  </g>
  <line x1="322" y1="14" x2="322" y2="296" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.6"><line x1="346" y1="214" x2="542" y2="214"/><line x1="346" y1="214" x2="346" y2="64"/></g>
  <polyline points="386.8,64.0 388.8,70.9 390.8,77.2 392.7,82.9 394.7,88.2 396.7,93.1 398.6,97.6 400.6,101.8 402.5,105.7 404.5,109.3 406.5,112.7 408.4,115.9 410.4,118.9 412.4,121.7 414.3,124.4 416.3,126.9 418.3,129.2 420.2,131.5 422.2,133.6 424.2,135.6 426.1,137.5 428.1,139.4 430.0,141.1 432.0,142.8 434.0,144.4 435.9,145.9 437.9,147.4 439.9,148.7 441.8,150.1 443.8,151.4 445.8,152.6 447.7,153.8 449.7,154.9 451.6,156.0 453.6,157.1 455.6,158.1 457.5,159.1 459.5,160.0 461.5,161.0 463.4,161.8 465.4,162.7 467.4,163.5 469.3,164.3 471.3,165.1 473.3,165.9 475.2,166.6 477.2,167.3 479.1,168.0 481.1,168.7 483.1,169.3 485.0,169.9 487.0,170.6 489.0,171.2 490.9,171.7 492.9,172.3 494.9,172.9 496.8,173.4 498.8,173.9 500.8,174.4 502.7,174.9 504.7,175.4 506.6,175.9 508.6,176.3 510.6,176.8 512.5,177.2 514.5,177.7 516.5,178.1 518.4,178.5 520.4,178.9 522.4,179.3 524.3,179.7 526.3,180.0 528.3,180.4 530.2,180.8 532.2,181.1 534.1,181.4 536.1,181.8 538.1,182.1 540.0,182.4 542.0,182.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="346.0,214.0 347.6,209.8 349.3,205.7 350.9,201.6 352.5,197.6 354.2,193.7 355.8,190.0 357.4,186.3 359.1,182.9 360.7,179.6 362.3,176.5 364.0,173.6 365.6,170.9 367.2,168.4 368.9,166.1 370.5,164.0 372.1,162.1 373.8,160.4 375.4,158.9 377.0,157.5 378.7,156.3 380.3,155.3 381.9,154.4 383.6,153.6 385.2,153.0 386.8,152.5 388.5,152.1 390.1,151.8 391.7,151.6 393.4,151.5 395.0,151.5 396.6,151.5 398.3,151.6 399.9,151.8 401.5,152.0 403.2,152.2 404.8,152.5 406.4,152.8 408.1,153.2 409.7,153.6 411.3,154.0 413.0,154.4 414.6,154.9 416.2,155.3 417.9,155.8 419.5,156.3 421.1,156.8 422.8,157.3 424.4,157.8 426.0,158.3 427.7,158.9 429.3,159.4 430.9,159.9 432.6,160.4 434.2,160.9 435.8,161.5 437.5,162.0 439.1,162.5 440.7,163.0 442.4,163.5 444.0,164.0 445.6,164.5 447.3,165.0 448.9,165.5 450.5,166.0 452.2,166.4 453.8,166.9 455.4,167.4 457.1,167.8 458.7,168.3 460.3,168.7 462.0,169.2 463.6,169.6 465.2,170.1 466.9,170.5 468.5,170.9 470.1,171.3 471.8,171.7 473.4,172.1 475.0,172.5 476.7,172.9 478.3,173.3 479.9,173.7 481.6,174.0 483.2,174.4 484.8,174.8 486.5,175.1 488.1,175.5 489.7,175.8 491.4,176.2 493.0,176.5 494.6,176.8 496.3,177.2 497.9,177.5 499.5,177.8 501.2,178.1 502.8,178.4 504.4,178.7 506.1,179.0 507.7,179.3 509.3,179.6 511.0,179.9 512.6,180.2 514.2,180.4 515.9,180.7 517.5,181.0 519.1,181.2 520.8,181.5 522.4,181.8 524.0,182.0 525.7,182.3 527.3,182.5 528.9,182.8 530.6,183.0 532.2,183.2 533.8,183.5 535.5,183.7 537.1,183.9 538.7,184.1 540.4,184.4 542.0,184.6" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="395.0" cy="151.5" r="3" fill="currentColor"/>
  <line x1="358.7" y1="214" x2="358.7" y2="74" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>
  <circle cx="358.7" cy="183.6" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="358.7" y1="76" x2="358.7" y2="60" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr06s5e)"/>
  <g font-size="11" fill="currentColor">
    <text x="332" y="28" font-size="12">gain along a direction with singular value σ</text>
    <text x="341" y="180.5" text-anchor="end" font-size="10">1</text>
    <text x="341" y="143.0" text-anchor="end" font-size="10">2</text>
    <text x="341" y="105.5" text-anchor="end" font-size="10">3</text>
    <text x="341" y="68.0" text-anchor="end" font-size="10">4</text>
    <text x="395.0" y="228" text-anchor="middle" font-size="10">0.3</text>
    <text x="444.0" y="228" text-anchor="middle" font-size="10">0.6</text>
    <text x="493.0" y="228" text-anchor="middle" font-size="10">0.9</text>
    <text x="542.0" y="228" text-anchor="middle" font-size="10">1.2</text>
    <text x="542" y="242" text-anchor="end">σ</text>
    <text x="430.9" y="124.0">1/σ, undamped</text>
    <text x="440.7" y="193.4">damped, λ = 0.3</text>
    <text x="390.0" y="145.5" text-anchor="end" font-size="10">1.67</text>
    <text x="364.7" y="187.6" font-size="10">0.81</text>
    <text x="364.7" y="66" font-size="10">12.8</text>
    <text x="332" y="258">peak 1/(2λ) = 1.67, at σ = λ</text>
    <text x="332" y="274">at σmin = 0.0779: 12.8 undamped,</text>
    <text x="332" y="290">0.81 damped</text>
  </g>
</svg>

Step 5 on P2, drawn to scale. From the nearly straight seed $(45^\circ, 10^\circ)$, whose tip sits at $(1.281,\ 1.526)$, $0.596\,\mathrm{m}$ from the target $(1,1)$, the undamped step divides the error by $\sigma_{\min} = 0.0779$, turns the joints $7.51\,\mathrm{rad}$ and throws the tip to $(-1.32,\ -1.39)$, $3.33\,\mathrm{m}$ off, while the damped step at $\lambda = 0.3$ turns them $0.478\,\mathrm{rad}$ to $(30.3^\circ,\ 33.1^\circ)$, $0.506\,\mathrm{m}$ off. On the right, the gain a step applies to the error along a direction with singular value $\sigma$: $1/\sigma$ undamped against $\sigma/(\sigma^2 + \lambda^2)$ damped, which never exceeds $1/(2\lambda) = 1.67$ and is $0.81$ at $\sigma_{\min}$, where the undamped gain is $12.8$.

### 1. IK is structurally harder than FK

Unlike FK, IK has **zero, one, several, or infinitely many** solutions (elbow-up vs
elbow-down; a 7-dof arm has a continuum). This multimodality is a useful analogy for why
[[01-canonical-papers/notes/4-vla/diffusion-policy|generative policies]] represent alternative actions: averaging distinct valid solutions may give an invalid one. It does not establish that a particular learned policy performs better. **Analytic IK**
(closed-form, e.g. a 6R arm — six revolute joints — whose last three axes meet in one point, a spherical wrist) enumerates all branches exactly; when geometry
doesn't permit it, go numerical.

> **Inverse kinematics problem, defined.** The **inverse kinematics problem** is *an equation to be solved for the joints*: given a target, find joint vectors that forward kinematics sends onto it. Three conditions define it. **The target is fixed**: a pose $X \in SE(3)$, or task coordinates $x_d$ for a position task (the task space of [[04-robotics/modern-robotics/ch02-configuration-space|ch.2 §1.5]]), together with the FK map of ch.4. **The equation is exact**: $\theta$ solves it when $T(\theta) = X$, and a numerical solver meets that only to a tolerance it must state. And **its solution set is part of the problem**: $\Theta(X)$ can be empty (outside the workspace), finite (several branches) or a continuum (a redundant arm), and a solver that returns one $\theta$ has solved the problem without describing the set (MR ch.6).
>
> $$\Theta(X) = \{\theta \in \mathbb{R}^n :\ T(\theta) = X\} = T^{-1}(X)$$
>
> where $T^{-1}$ means the preimage, not an inverse function, because FK is single-valued but many joint vectors can share one pose, so a preimage need not be a single point.
>
> - **Example**: P2's tip target $(1,1)$ has $\Theta = \{(0^\circ, 90^\circ),\ (90^\circ, -90^\circ)\}$, angles mod $360^\circ$. The target $(2.5, 0)$ has $\Theta = \emptyset$, since it would need $\cos\theta_2 = 2.125$.
> - **Non-example**: a reachable point taken for a reachable pose. Add the tool's direction $\phi = 45^\circ$ to the target $(1,1)$: each branch fixes $\phi = \theta_1 + \theta_2$, $90^\circ$ on one and $0^\circ$ on the other, so $\Theta = \emptyset$ although both branches reach the point. A position-only solver reports success on a pose task that P2 cannot do.

> **Analytic IK, defined.** **Analytic inverse kinematics** is *a closed-form solution method*: explicit formulas that list the solution set. Three conditions define it. **Closed form**: a finite sequence of algebraic and trigonometric steps, such as the law of cosines and $\operatorname{atan2}$, with no iteration and no initial guess. **Complete**: one formula per branch, so every element of a finite $\Theta(X)$ comes out. **It decides existence**: the same formulas say when $\Theta(X) = \emptyset$. Only special geometries admit one, such as the planar 2R arm of MR's ch.6 introduction and the PUMA- and Stanford-type arms with a spherical wrist of MR §6.1.
>
> $$\theta_2 = \pm\arccos\frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2}, \qquad \theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}\bigl(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2\bigr)$$
>
> where $(x, y)$ is the target and the $\pm$ gives the two branches, since the law of cosines fixes $\cos\theta_2$ and leaves the sign of $\theta_2$ open; the $\arccos$ exists exactly when its argument lies in $[-1, 1]$, which is the existence test. Steps 1–2 of the worked case derive both lines.
>
> - **Example**: at $(1,1)$ the argument is $0$, so $\theta_2 = \pm 90^\circ$ and $\theta_1 = 0^\circ$ or $90^\circ$: both branches, with no seed.
> - **Non-example**: the same formula coded with $\theta_2 = \arccos(\cdot)$ and no $\pm$. It is closed-form but not complete: $\arccos$ returns values in $[0, \pi]$, so it finds $(0^\circ, 90^\circ)$ and never $(90^\circ, -90^\circ)$, and a planner that needs the other elbow to clear an obstacle is told that none exists.

The picture and Steps 1–3 are this section on P2: two exact branches for the panel point $(1,1)$, elbows at $(1,0)$ and $(0,1)$, and a mean $(45^\circ, 0^\circ)$ that is not a solution. A numerical solver follows the branch near its seed, so **one failed local search does not prove that the robot has no solution**: before concluding that a target is unreachable, rule out a poor seed, a singular local map, a violated joint limit and an expired iteration budget.

> [!note]- Deeper · 더 깊이
> **A pose target is not yet a motion plan.** Elbow-up and elbow-down solutions can reach the same tip pose through very different arm configurations, and a joint limit or an obstacle can invalidate one branch without the other. A solver returning a target configuration therefore answers a narrower question than a planner finding a collision-free route to it ([[04-robotics/modern-robotics/ch10-motion-planning|ch.10]]).
>
> **Seeds and continuity.** For successive nearby targets the previous solution is a useful seed because it encourages continuity; it does not guarantee continuity through singularities or a change of feasible branch. The analogy to multimodal learned actions is about representing alternatives; it is not a theorem that every generative policy outperforms regression.

### 2. Numerical IK = Newton-Raphson on the pose error

A general arm has no closed form: P2's law of cosines works because two links make a triangle, and a six-joint arm offers no such triangle unless it was built for one (the spherical wrist of §1), while a seven-joint arm has a continuum of answers. Numerical IK treats the target as a root to find instead. This is Newton's method of [[02-foundations/optimization|4. Optimization §3]] in vector form. For a scalar equation $f(x) = 0$, Newton steps $x \leftarrow x - f(x)/f'(x)$; here the equation is $\mathrm{FK}(\theta) - x_{goal} = 0$, so the derivative $f'$ becomes the Jacobian $J$, dividing by it becomes solving $J\,\Delta\theta = e$, and when $J$ is not square or not invertible, solving means least squares — hence $J^\dagger$, which is why the iteration reads
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(task-space error)}$$
where in the full SE(3) case $e$ is the six-vector error $[\log(T_{now}^{-1} T_{goal})]^\vee$ in body coordinates, paired with the body Jacobian
([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3 §5]]'s matrix logarithm; the "vee" $^\vee$ undoes ch.3's bracket operation, pulling the six numbers back out of the $4\times4$ matrix), and $J^\dagger$
is the pseudoinverse ([[02-foundations/linear-algebra|least squares]]).

> **Newton-Raphson IK, defined.** **Newton-Raphson inverse kinematics** is *an iterative root-finding algorithm*: it produces a sequence of joint vectors, not a formula. Three conditions define it. **It seeks a root of the task residual** $e(\theta) = x_d - f(\theta)$. **It re-linearizes every step**: $J$ is evaluated at the current iterate, never frozen. **It solves the linear model in least squares**: $\Delta\theta = J^\dagger e$, which is $J^{-1}e$ when $J$ is square and invertible. Two rules sit outside the definition (MR §6.2.2). The loop stops on the residual, $\|e\| \le \epsilon$, with separate bounds on $\|\omega_b\|$ and $\|v_b\|$ for a pose, since a step-size test would stop at Step 4's seed $0.586\,\mathrm{m}$ from the target. And it converges only from a seed inside a solution's basin of attraction — the set of seeds from which the iteration ends on that solution.
>
> $$\theta_{k+1} = \theta_k + J^\dagger(\theta_k)\,\bigl(x_d - f(\theta_k)\bigr), \qquad \text{stop when } \|x_d - f(\theta_k)\| \le \epsilon$$
>
> where $f$ is forward kinematics in task coordinates and $J = \partial f/\partial\theta$; the step zeroes the first-order Taylor model of $e$, so near a regular solution each error is roughly proportional to the square of the one before.
>
> - **Example**: P2, target $(1,1)$, seed $(20^\circ, 70^\circ)$: $\|e\| = 0.347,\ 0.066,\ 0.0021,\ 2\times10^{-6}\,\mathrm{m}$, landing on $(0^\circ, 90^\circ)$. Seeded at $(60^\circ, -60^\circ)$ the same loop lands on $(90^\circ, -90^\circ)$ instead.
> - **Non-example**: the same loop with $J$ frozen at the seed, a chord iteration. From $(20^\circ, 70^\circ)$ it still reaches $(0^\circ, 90^\circ)$, but after three steps $\|e\|$ is $1.2\times10^{-3}\,\mathrm{m}$ against Newton-Raphson's $2\times10^{-6}$, because each step now multiplies the error by a factor that settles near $0.06$ instead of squaring it. A solver that reuses one Jacobian to save time pays for it in iterations.

**The SE(3) error in numbers, on P2.** Seed at home, $\theta = (0, 0)$, so $T_{now} = M$, the home configuration of [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]] (MR's letter for it; not the mass matrix $M$ of [[02-foundations/manipulator-kinematics-dynamics|10]]), and ask for $T_{goal} = T_{sb}$, the catalog tool pose derived in Step 1 of [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3's Worked case]]. Then $M^{-1}T_{sb}$ has $R = R_z(90^\circ)$ and $p = (-1, 1, 0)$, and the logarithm of ch.3 §5 gives $e = (0, 0, \pi/2;\ 0, \pi/2, 0) = \mathcal{B}_2\cdot\frac{\pi}{2}$ — the elbow's body screw $\mathcal{B}_2 = (0,0,1;\ 0,1,0)$ of [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]], turned a quarter turn. At home the body Jacobian's columns are ch.4's body screws, $\mathcal{B}_1 = (0,0,1;\ 0,2,0)$ and $\mathcal{B}_2$, and $J_b^\dagger e = (0,\ \pi/2)$: one Newton step lands exactly on $(0^\circ, 90^\circ)$, because this error is itself one joint's screw. A general error is not, which is why the loop repeats, as §3 does by hand.

> [!note]- Deeper · 더 깊이
> **The full-pose error, carefully.** For the body-frame pose error above, the matrix logarithm is first a matrix in the Lie algebra; its six coordinates form the error vector, and they pair with the body Jacobian. Use separate rotation and translation stopping tolerances, because radians and lengths are different units, and enforce joint limits and check collision separately from numerical convergence.
>
> **What the pseudoinverse does and does not do.** It minimizes the local linear residual and picks the minimum-norm update when alternatives remain; it does not solve the whole nonlinear pose problem at once, which is why the loop repeats. The book's [official numerical IK walkthrough](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) steps through the same local approximation and update loop.

### 3. One full iteration, by hand — planar 2R arm

Every iteration of §2 makes the same four moves — compute the current tip by FK, form the error to the target, evaluate $J$ at the current joints, and solve $J\,\Delta\theta = e$ for the update — and then starts over, because $J$ describes only local change. Here they are once by hand, then the sequence they produce.

$L_1 = L_2 = 1$; target tip $(-1, 1)$ (true answer: $\theta^* = (90°, 90°)$, from
[[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4 §2]]'s worked example). Start at
$\theta^{(0)} = (45°, 90°)$.

- **FK**: tip $= (\cos 45° + \cos 135°,\; \sin 45° + \sin 135°)$ — compute:
  $(0.707 - 0.707,\; 0.707 + 0.707) = (0,\, 1.414)$.
- **Error**: $e = (-1, 1) - (0, 1.414) = (-1, -0.414)$; $\|e\| = 1.08$.
- **Jacobian** (ch.5 formula, $s_1 = c_1 = 0.707$, $s_{12} = 0.707$, $c_{12} = -0.707$), because the ch.5 $J(\theta)$ is evaluated at the current joints:
  $$J = \begin{pmatrix} -1.414 & -0.707 \\ 0 & -0.707 \end{pmatrix}, \quad \det J = 1.0$$
- **Update**: with $\det J = 1$, swapping the diagonal and negating the off-diagonal gives $J^{-1} = \begin{pmatrix} -0.707 & 0.707 \\ 0 & -1.414 \end{pmatrix}$, so $\Delta\theta = J^{-1} e = (0.707 - 0.293,\; 0.586) = (0.41,\; 0.59)$ rad $= (23.7°,\; 33.6°)$ and
  $\theta^{(1)} = (68.7°,\; 123.6°)$.
- **Check**: FK at $\theta^{(1)}$, where $\theta_1 + \theta_2 = 192.3°$, gives the tip $(0.363 - 0.977,\ 0.932 - 0.213) \approx (-0.61,\, 0.72)$;
  $\|e\| = 0.48$ — **the error halved in one step**, and the iterate is moving toward
  $(90°, 90°)$. The elbow has overshot, though: $123.6°$ against the answer's $90°$, because far from the answer the full Newton step trusts the linear model too far.

**The rest of the run.** Repeating the four moves gives $\|e\| = 1.08,\ 0.477,\ 0.0685,\ 0.0023,\ 2.7\times10^{-6}\,\mathrm{m}$, the joints passing $(68.7°, 123.6°)$, $(90.5°, 93.4°)$ and $(89.9°, 90.1°)$ before landing on $(90°, 90°)$. The first step only halves the error because the seed is $45°$ from the answer, where the linear model $J$ is a poor guide. Once the iterate is close, each error is about half the square of the one before — $0.0685^2/2 = 0.0023$, then $0.0023^2/2 = 2.7\times10^{-6}$ — which is the quadratic convergence of the Newton–Raphson box: the correct digits roughly double every step. Plotting $\|e\|$ against the iteration on a log axis is the standard sanity check for any IK implementation: a straight descent means a stale $J$ (the chord non-example), a stall means a singular seed (Step 4), and a sudden rise means a nearly singular one (Step 5).

### 4. The two practical complications

- **Singularities**: near them $J^\dagger$ explodes. The fix in plain words: add $\lambda^2 I$
  so the matrix to invert stays invertible even when $J$ loses rank, accepting a slightly
  wrong but bounded step instead of a huge one. That is **damped least squares**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$, which trades accuracy for stability — ridge regression in
  disguise, ridge regression being the statistics name for least squares with a penalty on the size of the answer. It is also, exactly, the **Levenberg–Marquardt** step for this residual: the
  identity $J^\top(JJ^\top + \lambda^2 I)^{-1} = (J^\top J + \lambda^2 I)^{-1}J^\top$, proved in the note below, makes the
  two expressions the same, so $\lambda$ is a trust parameter and damped IK is the same
  algorithm that SLAM (simultaneous localization and mapping) and calibration run ([[02-foundations/optimization|4. Optimization §3.5]]).
  One convention to carry between pages: [[02-foundations/linear-algebra|1. Linear Algebra §4.5]] and [[02-foundations/optimization|4. Optimization §3.5]] write the damping as $\lambda$ where this page writes $\lambda^2$, so this page's $\lambda = 0.3$ is $\lambda = 0.09$ there. MR itself stops at the plain pseudoinverse; the note below says where the damped form comes from.

> [!note]- Deeper · 더 깊이
> **The identity in one line.** $(J^\top J + \lambda^2 I)J^\top = J^\top JJ^\top + \lambda^2 J^\top = J^\top(JJ^\top + \lambda^2 I)$; multiply on the left by $(J^\top J + \lambda^2 I)^{-1}$ and on the right by $(JJ^\top + \lambda^2 I)^{-1}$, both invertible for $\lambda > 0$ because each matrix is then positive definite.
>
> **Where damped least squares comes from.** MR itself does not present it: at a singularity chapter 6 offers the bare pseudo-inverse and sends the damped and redundant-arm family to its notes and references, so do not go looking for it in the chapter. The $\lambda^2$ form written here is that outside literature's convention: $\lambda$ then has the units of a singular value, and the gain $\sigma/(\sigma^2 + \lambda^2)$ peaks exactly at $\sigma = \lambda$. For a two-link arm coded end to end — analytic IK with both elbow branches, then one damped step — see [[02-foundations/algorithms/robotics-ai-problems|11.8 §6]].

> **Damped least squares, defined.** **Damped least squares** (DLS) is *a regularized step rule for numerical IK*: the joint step that best reduces the linearized error while paying for its own length. Three conditions define it. **Damping $\lambda > 0$**: $JJ^\top + \lambda^2 I$ is then positive definite, so the inverse exists at every $\theta$, singular or not. **A trade-off objective**: the step minimizes the residual plus a penalty on its size. **Bounded gain**: along a singular direction with value $\sigma$ the error is scaled by $\sigma/(\sigma^2 + \lambda^2) \le 1/(2\lambda)$ instead of $1/\sigma$, and as $\lambda \to 0$ away from singularities the step returns to $J^\dagger e$.
>
> $$\Delta\theta = J^\top\bigl(JJ^\top + \lambda^2 I\bigr)^{-1}e = \arg\min_{\Delta\theta}\ \|J\Delta\theta - e\|^2 + \lambda^2\|\Delta\theta\|^2$$
>
> where $e$ is the task error and $\lambda$ the damping; the two sides agree because setting the cost's gradient to zero gives $(J^\top J + \lambda^2 I)\,\Delta\theta = J^\top e$, the Levenberg–Marquardt form above.
>
> - **Example**: Step 5's seed $(45^\circ, 10^\circ)$, where $\sigma_{\min} = 0.0779$. Undamped, the weak direction is amplified $12.8$ times and the step is $7.51\,\mathrm{rad}$; at $\lambda = 0.3$ its gain is $0.81$, no step can exceed $0.994\,\mathrm{rad}$, and the arm moves to $(30.3^\circ, 33.1^\circ)$ with $\|e\| = 0.506$.
> - **Non-example**: the plain pseudoinverse $J^\dagger$, which libraries return at every $\theta$ and which therefore looks safe. It is defined everywhere, but its gain $1/\sigma$ has no upper bound as $\sigma \to 0$, which is the $7.51\,\mathrm{rad}$ step above. A solver that swaps DLS for it gains accuracy far from singularities and loses control near them.

- **Redundancy** ($n > 6$): the null space of $J$ ([[02-foundations/linear-algebra|§2's null space]], this time of $J$: joint velocities with $J\dot\theta = 0$) moves joints without moving the tool —
  spend it on secondary objectives (joint limits, obstacles, singularity avoidance).

**Wiki connections**: end-effector-space teleop stacks and VLA (vision-language-action) policies run IK, or its velocity-level cousin, between policy output and motor commands; joint-space rigs such as [[01-canonical-papers/notes/4-vla/act|ALOHA]] skip it.

### Self-check

1. For the target $(-1,1)$ above, what is the *other* analytic solution besides
   $(90°, 90°)$?
2. Why does Newton IK need a *good initial guess*, and what typically supplies it in a
   control loop?
3. What goes wrong if you run the ch.5 arm's IK starting exactly at $\theta_2 = 0$?
4. Write the damped least squares update and say what $\lambda$ trades off.

> [!tip]- Answers
> 1. The elbow-down branch: $(180°, -90°)$. Check: link 1 points along $-\hat x$ to $(-1,0)$, then link 2 turns $-90°$ to point along $+\hat y$, giving tip $(-1,1)$. ✓ Two joint configurations, one task pose — that is IK's multimodality in a single example.
> 2. Newton's method converges only locally: far from a solution the linearization $J$ is a poor model and the step can diverge or land in a different branch. In a control loop the previous timestep's solution is the natural seed, since the target moves continuously — which also keeps the arm on one branch instead of flipping elbow configurations mid-motion.
> 3. $\theta_2 = 0$ is a singularity: $\det J = L_1L_2\sin\theta_2 = 0$, so $J^{-1}$ does not exist. The pseudoinverse still returns a step, but it cannot reduce error in the lost direction at all — the iteration stalls (or blows up numerically without damping).
> 4. $\Delta\theta = J^\top(JJ^\top + \lambda^2 I)^{-1}e$. Large $\lambda$ = stable near singularities but slower and biased (the step no longer solves the exact least-squares problem); small $\lambda$ = accurate away from singularities but explosive near them. It is ridge regression, and $\lambda$ is its ridge parameter.

### Problem set · 과제

Tier B. **P2** from [[02-foundations/lab-plants|0.6]], at the targets each item names. Analytic only — no Newton loop.

1. **Draw.** The picture above for a target on the $x$-axis, $(1.5,\ 0)$: both IK branches that put the tip there, with the two elbow points labelled and each branch's joint angles written beside it. Add the mean of the two joint vectors, dashed, with an $\times$ on its tip, and the miss back to the target.
2. **Derive.** The target $(1,\ 0.5)$ on the panel face, half a metre below the catalog target. (a) $\cos\theta_2$ and both branches, with their elbow points. (b) The componentwise mean of the two joint vectors: where does it put the tip, and how far from the target? Show that for P2's unit links the mean is always the straight arm along $\operatorname{atan2}(y, x)$, so it overshoots by $2 - r$, where $r$ is the target's distance from the base. (c) [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §2]]'s live resolved-rate run drove the tip from $(1,1)$ to $(0.999,\ 0.500)$ and ended with the joints at $(-29.45^\circ,\ 112.06^\circ)$. Which branch did it land on, and why that one?
3. **Interpret.** A joint limit $|\theta_2| \le 100^\circ$ is added to P2's elbow. Which branches of $(1,1)$ and of $(1,\ 0.5)$ survive? What region of the workspace does the limit remove, and how do the analytic formulas and a Newton loop each report a target inside it?

> [!note]- How to draw it · 그리는 법
> - Draw the target once, as a small circle at $(1.5,\ 0)$, and let every arm end on it or point at it.
> - Each branch is two links: link 1 from the base to its elbow, link 2 from the elbow to the target. Draw one branch solid and the other lighter; they are mirror images in the $x$-axis because the target lies on it.
> - Label both elbow points, $(0.75,\ -0.661)$ and $(0.75,\ 0.661)$, and write each branch's angles, $(-41.4^\circ,\ 82.8^\circ)$ and $(41.4^\circ,\ -82.8^\circ)$: same tip, two different arms.
> - The mean of the two joint vectors is $(0^\circ,\ 0^\circ)$: draw it dashed as one straight segment along $+x$, put an $\times$ on its tip at $(2,0)$, and mark the $0.5\,\mathrm{m}$ miss back to the target. It must land visibly past the target, not near it.
> - At the dashed tip, "reachable" is a double-headed arrow perpendicular to the straight arm and "wanted" points back along it toward the target. Draw them at right angles: the straight arm is singular again, and the whole error lies in the direction it cannot move.

> [!tip]- Solutions
> 1. With $\cos\theta_2=(1.5^2-2)/2=0.125$, $\theta_2=\pm82.8^\circ$, and $\theta_1=-\operatorname{atan2}(\sin\theta_2,\ 1+\cos\theta_2)=\mp41.4^\circ$: branches $(-41.4^\circ,\ 82.8^\circ)$ with the elbow at $(0.75,\ -0.661)$ and $(41.4^\circ,\ -82.8^\circ)$ with the elbow at $(0.75,\ 0.661)$, mirror images in the $x$-axis. Their mean is $(0^\circ,\ 0^\circ)$, the straight arm, with its tip at $(2,0)$: $0.5\,\mathrm{m}$ past the target, a third of its distance from the base, and exactly on the singularity, as in the picture above. The mean of two IK solutions is again not a solution.
> 2. (a) $\cos\theta_2=(1^2+0.5^2-2)/2=(1.25-2)/2=-0.375$, so $\theta_2=\pm112.0^\circ$. For $\theta_2=+112.0^\circ$, $\theta_1=\operatorname{atan2}(0.5,1)-\operatorname{atan2}(\sin112.0^\circ,\ 1+\cos112.0^\circ)=26.6^\circ-\operatorname{atan2}(0.927,\ 0.625)=26.6^\circ-56.0^\circ=-29.4^\circ$, elbow at $(\cos(-29.4^\circ),\ \sin(-29.4^\circ))=(0.871,\ -0.492)$. For $\theta_2=-112.0^\circ$, $\theta_1=26.6^\circ+56.0^\circ=82.6^\circ$, elbow at $(0.129,\ 0.992)$. FK checks both: the first has its forearm at $-29.4^\circ+112.0^\circ=82.6^\circ$, so the tip is $(0.871+0.129,\ -0.492+0.992)=(1.0,\ 0.5)$; the second swaps the two directions and gives the same tip. (b) The mean is $(26.6^\circ,\ 0^\circ)$, a straight arm along the target's bearing, tip at $2(\cos26.6^\circ,\ \sin26.6^\circ)=(1.789,\ 0.894)$, $0.882\,\mathrm{m}$ from the target. In general, for unit links $\operatorname{atan2}(\sin\beta,\ 1+\cos\beta)=\beta/2$, because $\sin\beta=2\sin\tfrac\beta2\cos\tfrac\beta2$ and $1+\cos\beta=2\cos^2\tfrac\beta2$; so with $\phi=\operatorname{atan2}(y,x)$ and $\beta=|\theta_2|$ the branches are $(\phi-\beta/2,\ \beta)$ and $(\phi+\beta/2,\ -\beta)$, whose mean is $(\phi,\ 0)$: the straight arm along $\phi$, tip at distance 2, overshooting a target at distance $r$ by $2-r$ — here $2-\sqrt{1.25}=0.882$, and $0.586$ for $(1,1)$ and $0.5$ for the Draw item's $(1.5,\ 0)$. (c) The first branch, $(-29.4^\circ,\ 112.0^\circ)$: the run started at $(0^\circ,\ 90^\circ)$ with $\theta_2>0$ and moved continuously, and reaching the other branch would have taken $\theta_2$ through $0^\circ$, the straight-arm singularity, where $J$ cannot be inverted. The $0.04^\circ$ difference in $\theta_2$ is the run's sub-millimetre drift.
> 3. The elbow now needs $|\theta_2|\le100^\circ$. $(1,1)$ needs $|\theta_2|=90^\circ$, so both branches survive; $(1,\ 0.5)$ needs $|\theta_2|=112.0^\circ$, so neither does, although it lies well inside the $2\,\mathrm{m}$ reach. Since $r^2=2+2\cos\theta_2$ for unit links, $|\theta_2|\le100^\circ$ means $r\ge\sqrt{2+2\cos100^\circ}=\sqrt{2-0.347}=1.286\,\mathrm{m}$: the limit opens a hole of radius $1.286\,\mathrm{m}$ around the base, where the unlimited arm reached every $r$ from 0 to 2. The analytic formulas decide it in one comparison, $\cos\theta_2=-0.375<\cos100^\circ=-0.174$, and report that no solution exists within the limit; a Newton loop clamped to the limit would only fail to converge, which cannot tell an unreachable target from a bad seed (§1).

## 한국어

**핵심 질문**: 원하는 말단 자세가 주어지면 어떤 관절 각이 그것을 달성하는가?

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 역기구학은 조작 층에서 도구의 목표를 관절 각으로 바꾸는 일이다. "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계를 받친다. 패널의 점은 과제 공간에서 주어지는데 모터에는 $\theta$가 필요하기 때문이다. [[physical-ai-map|피지컬 AI 지도]]도 이 페이지를 그 단계에 넣어 두었고, 칩은 조작 띠에 있다. 이것이 없으면 해법이 서로 비슷해 보이는 방식으로 실패한다. 카탈로그의 평면 2링크 팔 **P2**([[02-foundations/lab-plants|0.6]])를 패널의 점 $(1,1)$에 두는 정확한 해 둘을 평균하면 팔이 $(45^\circ, 0^\circ)$로 곧게 펴져 목표를 $0.586\,\mathrm{m}$ 지나치고, 그 자리는 감쇠가 있든 없든 어떤 스텝도 팔을 움직이지 못하는 특이점이다. 그 초기값에서 10도 벗어나면 감쇠 없는 스텝이 관절을 $7.51\,\mathrm{rad}$ 던지고 오차가 $0.596$에서 $3.33\,\mathrm{m}$로 커진다('대상으로 한 번 끝까지' 3–5단계). 뒤 페이지들이 여기에 기댄다. [[04-robotics/ros2/manipulation-moveit2|25.8 MoveIt 2 §1과 §7]]은 IK 해법을 부르고 이 루프 위에 직선 말단 경로를 세우며, [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §2]]는 말단 행동을 이것을 거쳐 모터로 보내고, [[04-robotics/planning-decision-making|4. 계획·의사결정 §1]]은 이것을 경로와 제어기 사이에 두며, [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] 노트는 3단계의 실패를 시연에서 다시 만난다. 유효한 두 모드를 평균하면 무효한 행동이 된다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 2, 로보틱스 16–18회차다. 이 페이지를 마치면 P2의 IK 가지를 해석적으로 모두 나열하고, 뉴턴–랩슨 IK를 돌리고 진단하며, 그것이 멈추거나 날뛸 때 감쇠와 새 초기값 가운데 무엇을 고를지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 세 번쯤, 로보틱스 16–18회차다. **첫 회차:** 이 페이지의 대상, 그림, '대상으로 한 번 끝까지' 전체를 손으로 한다. 해석적 가지 둘, 그 평균이 해가 아닌 이유, 그리고 특이점 위(4단계)와 거기서 10도 벗어난 곳(5단계)에서 시작한 해법이 하는 일이다. 감쇠 스텝은 4단계가 적어 둔 식을 쓴다. 끝으로 초기값 $(45^\circ, 0^\circ)$는 어떤 감쇠 $\lambda$에서도 스텝을 얻지 못하는데 $(45^\circ, 10^\circ)$는 날뛰는 스텝을 얻는 이유를 페이지를 덮고 설명한다. 비슷해 보이지만 처방이 정반대인 두 실패다. **둘째 회차:** §1–§4. 문제와 해석적 IK의 정의, 자세 전체 오차가 있는 뉴턴–랩슨, 손으로 하는 §3의 반복, 그리고 예가 다시 5단계의 숫자인 §4의 감쇠 최소제곱이다. **셋째 회차:** 스스로 점검과 과제. 접힌 *더 깊이* 메모는 두 번째 읽기다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그의 평면 2링크 팔(링크 길이 1, $\theta_1$은 $+x$축에서, 엘보 각 $\theta_2$는 링크 1에 대해 잰다. 회전 관절 둘인 "2R" 팔이다)과 그 카탈로그 목표인 말단 $(1,1)$이다. 이 점은 관통 과제가 접촉하는 자리, 곧 2장 패널의 면 $x = 1$ 위의 점이다. 카탈로그의 고정 자세 $(0^\circ, 90^\circ)$는 그 목표의 IK 해 가운데 하나이고, 이 페이지는 해를 모두 찾은 뒤 나쁜 초기값에서 수치 해법이 무엇을 하는지 묻는다.

*범위: 이 페이지는 P2 위에서 IK를 가르친다. 해석적 가지, 말단 오차와 자세 전체 오차에 대한 뉴턴–랩슨, 감쇠 최소제곱이다. 목표까지 가는 길이 비어 있는지는 [[04-robotics/modern-robotics/ch10-motion-planning|10장]], 움직이는 목표에 필요한 관절 속도는 [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §2]]에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 292" style="max-width:100%;height:auto" role="img" aria-label="목표 (1, 1)에 닿는 P2의 IK 가지 둘(엘보 (1, 0)과 (0, 1))과 그 관절 공간 평균인 곧은 팔을 그린 그림으로, 평균의 말단 (1.414, 1.414)은 0.586 m 지나치고 거기서 도달 가능한 유일한 방향은 원하는 방향과 직각이다.">
  <defs><marker id="mr06hdK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="0.8" opacity="0.25"><line x1="38.8" y1="256" x2="307.5" y2="256"/><line x1="70" y1="268.5" x2="70" y2="37.2"/></g>
  <polyline points="70,256 70,131 195,131" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round" opacity="0.42"/>
  <polyline points="70,256 195,256 195,131" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>
  <polyline points="70,256 158.4,167.6 238.3,87.7" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4" opacity="0.75"/>
  <circle cx="70" cy="256" r="4.8" fill="currentColor"/>
  <circle cx="195" cy="256" r="3.8" fill="currentColor"/>
  <circle cx="70" cy="131" r="3.8" fill="currentColor" fill-opacity="0.42"/>
  <circle cx="158.4" cy="167.6" r="3" fill="currentColor" fill-opacity="0.75"/>
  <circle cx="195" cy="131" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <g stroke="currentColor" stroke-width="2.2"><line x1="242.6" y1="75" x2="251" y2="83.4"/><line x1="242.6" y1="83.4" x2="251" y2="75"/></g>
  <g stroke="currentColor" stroke-width="1.8" marker-end="url(#mr06hdK)"><line x1="238.3" y1="70.7" x2="220.3" y2="52.7"/><line x1="255.3" y1="87.7" x2="273.3" y2="105.7"/></g>
  <line x1="223.4" y1="91.2" x2="194.6" y2="120" stroke="currentColor" stroke-width="2.4" marker-end="url(#mr06hdK)"/>
  <polyline points="236.9,89.1 227,79.2 236.9,69.3" fill="none" stroke="currentColor" stroke-width="1" opacity="0.85"/>
  <line x1="340" y1="14" x2="340" y2="276" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="215.3" y="46.7" text-anchor="end">도달 가능</text>
    <text x="205.9" y="92.1" text-anchor="end">원하는 방향</text>
    <text x="226.9" y="126.1">빗나감 0.586 m</text>
    <text x="257.8" y="76.2">(1.414, 1.414)</text>
    <text x="206" y="153">목표 (1, 1)</text>
    <text x="195" y="274" text-anchor="middle">엘보 A (1, 0)</text>
    <text x="61" y="135" text-anchor="end" opacity="0.75">(0, 1)</text>
    <text x="61" y="149" text-anchor="end" opacity="0.75">엘보 B</text>
    <text x="132.5" y="122" text-anchor="middle" opacity="0.75">B (90°, −90°)</text>
    <text x="204" y="223.5">A (0°, 90°)</text>
    <text x="145" y="241" text-anchor="middle" opacity="0.85">평균 (45°, 0°)</text>
    <text x="70" y="274" text-anchor="middle" opacity="0.8">베이스</text>
    <text x="352" y="26" font-size="12">정확한 IK 해 둘</text>
    <text x="358" y="45">A = (0°, 90°), 엘보 (1, 0)</text>
    <text x="358" y="62">B = (90°, −90°), 엘보 (0, 1)</text>
    <text x="352" y="91" font-size="12">평균 (45°, 0°)은 해가 아니다</text>
    <text x="358" y="110">말단 (√2, √2), 빗나감 0.5858 m</text>
    <text x="358" y="127">= 목표 거리 1.414 m의 41 %</text>
    <text x="352" y="156" font-size="12">평균에서 J의 랭크는 1</text>
    <text x="358" y="175">σ = (2.2361, 0)</text>
    <text x="358" y="192">도달 가능 (−0.7071, 0.7071)</text>
    <text x="358" y="209">원하는 방향 e = (−0.4142, −0.4142)</text>
    <text x="358" y="226">Jᵀe = (0, 0): 어떤 λ에도 스텝 0</text>
  </g>
</svg>

패널 면 위의 점인 카탈로그 목표 $(1,1)$에 정확한 IK 가지 둘로 닿는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2** — 가지 A $(0^\circ, 90^\circ)$는 엘보가 $(1,0)$, 가지 B $(90^\circ, -90^\circ)$는 엘보가 $(0,1)$에 있어 말단은 같고 팔이 둘이다. 두 가지의 성분별 평균 $(45^\circ, 0^\circ)$는 점선의 곧은 팔이고, 그 말단 $(\sqrt2, \sqrt2) = (1.414, 1.414)$는 목표를 $0.586\,\mathrm{m}$, 목표 거리의 $41\,\%$만큼 지나친다. 그 말단에서 $J$의 랭크는 1($\sigma = (2.2361,\ 0)$)이라 도달 가능한 유일한 방향은 팔에 수직인데 원하는 방향은 팔을 따라 되돌아가므로, $J^\top e = (0,0)$이고 어떤 감쇠 $\lambda$에서도 스텝이 전혀 없다.

### 대상으로 한 번 끝까지 · Worked case

카탈로그 목표에 대한 **P2**의 해석적 IK, 그다음 가장 나쁜 초기값에서의 수치 한 스텝. 여기 숫자는 전부 정확하다.

**1단계 — 엘보 각, 코사인 법칙에서.** FK 두 식을 제곱해 더하면 $\theta_1$이 사라지고 $x^2 + y^2 = L_1^2 + L_2^2 + 2L_1L_2\cos\theta_2$만 남는다. 교차항이 $\cos\theta_1\cos(\theta_1{+}\theta_2) + \sin\theta_1\sin(\theta_1{+}\theta_2) = \cos\theta_2$로 접히기 때문이다. 엘보에 대해 풀면

$$\cos\theta_2 = \frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2} = \frac{1 + 1 - 1 - 1}{2} = 0 \quad\Longrightarrow\quad \theta_2 = \pm 90^\circ$$

이고, 이 $\pm$가 해가 여럿인 이유다. 방정식이 정하는 것은 $\cos\theta_2$이지 $\theta_2$ 자체가 아니다. 목표에 도달 가능한 조건도 여기서 나온다. 이 코사인이 $[-1, 1]$에 들어와야 하고, 그것이 "해 없음"의 깔끔한 판정이다.

**2단계 — 어깨 각, 가지마다 하나씩.** $\theta_2$를 고르면 팔이 강체 삼각형이 되고, 베이스에서 본 말단의 방위각이 두 조각으로 갈라진다. 목표가 놓인 방향에서, 접힌 전완이 말단을 링크 1 자신의 방향에서 얼마나 밀어냈는지를 뺀 것이다. 두 조각 모두 점의 각이므로 인자가 둘인 아크탄젠트 $\operatorname{atan2}(y, x)$를 쓴다. 점 $(x, y)$의 각을 원 전체에 걸쳐 돌려주는 함수로, 두 부호를 모두 보존하므로 마주 보는 사분면을 헷갈리지 않는다:

$$\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2)$$

둘째 항은 $\theta_2$와 함께 부호가 뒤집히므로, 엘보 선택 둘이 어깨 각 하나가 아니라 둘을 준다. $\theta_2 = +90^\circ$: $\operatorname{atan2}(1,1) - \operatorname{atan2}(1, 1) = 45^\circ - 45^\circ = 0^\circ$이므로 $\theta = (0^\circ, 90^\circ)$. $\theta_2 = -90^\circ$: $45^\circ - \operatorname{atan2}(-1, 1) = 45^\circ - (-45^\circ) = 90^\circ$이므로 $\theta = (90^\circ, -90^\circ)$. 둘 다 FK로 검산된다. $(\cos 0^\circ + \cos 90^\circ,\ \sin 0^\circ + \sin 90^\circ) = (1,1)$이고 $(\cos 90^\circ + \cos 0^\circ,\ \sin 90^\circ + \sin 0^\circ) = (1,1)$이다. 앞의 것이 카탈로그 고정 자세인데, 이 페이지가 그렇게 고른 것이 아니라 카탈로그가 고른 것이다.

**3단계 — 평균이 왜 해가 아닌지, 숫자로.** 성분별 평균은 $(45^\circ, 0^\circ)$, 곧게 편 팔이고 말단은 $(\sqrt2, \sqrt2)$다. 빗나간 거리는 $\sqrt{2(\sqrt2 - 1)^2} = 0.5858\,\mathrm{m}$인데, 베이스에서 $1.414\,\mathrm{m}$ 떨어진 목표에 대해 $41\,\%$를 지나친 것이지 반올림 오차가 아니다. IK 해의 집합은 볼록하지 않고, 평균은 정확히 그것이 볼록하다고 가정하는 연산이다.

**4단계 — 그 평균 컨피규레이션을 수치 해법에 주고 아무 일도 안 일어나는 것을 본다.** $\theta^{(0)} = (45^\circ, 0^\circ)$에서 뉴턴 IK — 말단 오차 $e$에 대해 스텝 $\Delta\theta = J^\dagger e$를 반복하는 것, §2에서 유도 — 를 시작한다. $s_1 = c_1 = s_{12} = c_{12} = 0.7071$이므로 5장 공식이

$$J = \begin{pmatrix}-1.4142 & -0.7071\\ 1.4142 & 0.7071\end{pmatrix}, \qquad \det J = L_1L_2\sin\theta_2 = 0, \qquad \sigma = (2.2361,\ 0)$$

을 준다. 두 열이 평행하므로 랭크가 1이고, 도달 가능한 단 하나의 방향은 팔에 수직인 $(-0.7071, 0.7071)$이다. 오차는 $e = (1,1) - (\sqrt2,\sqrt2) = (-0.4142, -0.4142)$로 팔을 *따라* 곧장 되돌아가는 방향이다. 그러면

$$J^\top e = \begin{pmatrix}-1.4142 & 1.4142\\ -0.7071 & 0.7071\end{pmatrix}\begin{pmatrix}-0.4142\\ -0.4142\end{pmatrix} = \begin{pmatrix}0.5858 - 0.5858\\ 0.2929 - 0.2929\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}$$

이고, $J^\top$ 위에 세운 모든 갱신이 이 0을 물려받는다. 유사역행렬 스텝이 $0$이고, 감쇠 스텝 $J^\top(JJ^\top + \lambda^2 I)^{-1}e$(감쇠 최소제곱, §4의 특이점 처방)도 **모든** $\lambda$에 대해 $0$이다. 감쇠는 이미 0인 벡터에 곱해지는 것만 바꾸기 때문이다. 해법은 정확한 해가 둘이나 있는 목표에서 $58.6\,\mathrm{cm}$ 떨어진 채 "진전 없음"으로 멈춘다. 여기서 감쇠는 잘못된 처방이고, 유일한 처방은 다른 초기값이다.

**5단계 — 특이점에서 10도 벗어나면 실패의 종류가 바뀐다.** 초기값을 $(45^\circ, 10^\circ)$로 옮겨 팔이 *거의* 곧게 편 상태만 되게 하자. 이제 $\det J = \sin 10^\circ = 0.1736$, $\sigma = (2.2279,\ 0.0779)$다. 스텝 크기를 정하는 것은 $\|e\| = 0.5964$를 그 가장 작은 특이값으로 나눈 값이고, 감쇠 없는 갱신은 관절이 $\|\Delta\theta\| = 7.51\,\mathrm{rad}$만큼 움직이는 것이다. 말단은 $(-1.32, -1.39)$로 내던져지고 $\|e\|$는 $0.596$에서 $3.33$으로 커진다. $\lambda = 0.3$의 감쇠는 대신 $(30.3^\circ, 33.1^\circ)$로 가서 $\|e\|$를 $0.506$까지 내린다. 정확한 최소제곱 스텝보다 작고, 방향은 옳다. **정확히 특이점이면 스텝이 없고, 거의 특이점이면 스텝이 날뛴다.** $\|e\|$ 그래프에서는 비슷해 보이지만 처방이 정반대다.

<svg viewBox="0 0 560 348" style="max-width:100%;height:auto" role="img" aria-label="거의 곧게 편 초기값 (45°, 10°)에서 목표 (1, 1)로 가는 스텝 하나를 축척대로 그린 P2: 감쇠 없는 스텝은 관절을 7.51 rad 움직여 말단을 (−1.32, −1.39)로 던지고, λ = 0.3의 감쇠 스텝은 (30.3°, 33.1°)로 가서 오차를 0.506 m로 줄인다. 오른쪽은 특이값 σ 방향의 이득 1/σ와 σ/(σ² + λ²).">
  <defs><marker id="mr06s5k" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <circle cx="150.0" cy="160.0" r="128.0" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.45"/>
  <g stroke="currentColor" stroke-width="0.8" opacity="0.25"><line x1="15.6" y1="160.0" x2="284.4" y2="160.0"/><line x1="150.0" y1="294.4" x2="150.0" y2="25.6"/></g>
  <polyline points="150.0,160.0 195.3,114.7 232.0,62.3" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" opacity="0.4"/>
  <polyline points="150.0,160.0 94.4,191.7 65.6,248.8" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4" stroke-linejoin="round"/>
  <polyline points="150.0,160.0 205.3,127.7 234.0,70.6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="195.3" cy="114.7" r="3" fill="currentColor" fill-opacity="0.4"/>
  <circle cx="94.4" cy="191.7" r="3" fill="currentColor" fill-opacity="1"/>
  <circle cx="205.3" cy="127.7" r="3" fill="currentColor" fill-opacity="1"/>
  <circle cx="150.0" cy="160.0" r="4.5" fill="currentColor"/>
  <circle cx="214.0" cy="96.0" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <g stroke="currentColor" stroke-width="2"><line x1="61.6" y1="244.8" x2="69.6" y2="252.8"/><line x1="61.6" y1="252.8" x2="69.6" y2="244.8"/></g>
  <g font-size="11" fill="currentColor">
    <text x="224.0" y="112.0">목표 (1, 1)</text>
    <text x="74.6" y="252.8">(−1.32, −1.39)</text>
    <text x="143.0" y="153.0" text-anchor="end" opacity="0.8">베이스</text>
    <text x="220.0" y="278.8" opacity="0.6">도달 한계 2 m</text>
  </g>
  <g stroke="currentColor">
    <line x1="14" y1="302" x2="38" y2="302" stroke-width="2.6" opacity="0.4"/>
    <line x1="14" y1="320" x2="38" y2="320" stroke-width="2" stroke-dasharray="6 4"/>
    <line x1="14" y1="338" x2="38" y2="338" stroke-width="2.6"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="46" y="306">초기값 (45°, 10°): ‖e‖ = 0.596</text>
    <text x="46" y="324">감쇠 없음: 관절 7.51 rad, ‖e‖ = 3.33</text>
    <text x="46" y="342">감쇠 λ = 0.3: (30.3°, 33.1°), ‖e‖ = 0.506</text>
  </g>
  <line x1="322" y1="14" x2="322" y2="296" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.6"><line x1="346" y1="214" x2="542" y2="214"/><line x1="346" y1="214" x2="346" y2="64"/></g>
  <polyline points="386.8,64.0 388.8,70.9 390.8,77.2 392.7,82.9 394.7,88.2 396.7,93.1 398.6,97.6 400.6,101.8 402.5,105.7 404.5,109.3 406.5,112.7 408.4,115.9 410.4,118.9 412.4,121.7 414.3,124.4 416.3,126.9 418.3,129.2 420.2,131.5 422.2,133.6 424.2,135.6 426.1,137.5 428.1,139.4 430.0,141.1 432.0,142.8 434.0,144.4 435.9,145.9 437.9,147.4 439.9,148.7 441.8,150.1 443.8,151.4 445.8,152.6 447.7,153.8 449.7,154.9 451.6,156.0 453.6,157.1 455.6,158.1 457.5,159.1 459.5,160.0 461.5,161.0 463.4,161.8 465.4,162.7 467.4,163.5 469.3,164.3 471.3,165.1 473.3,165.9 475.2,166.6 477.2,167.3 479.1,168.0 481.1,168.7 483.1,169.3 485.0,169.9 487.0,170.6 489.0,171.2 490.9,171.7 492.9,172.3 494.9,172.9 496.8,173.4 498.8,173.9 500.8,174.4 502.7,174.9 504.7,175.4 506.6,175.9 508.6,176.3 510.6,176.8 512.5,177.2 514.5,177.7 516.5,178.1 518.4,178.5 520.4,178.9 522.4,179.3 524.3,179.7 526.3,180.0 528.3,180.4 530.2,180.8 532.2,181.1 534.1,181.4 536.1,181.8 538.1,182.1 540.0,182.4 542.0,182.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="346.0,214.0 347.6,209.8 349.3,205.7 350.9,201.6 352.5,197.6 354.2,193.7 355.8,190.0 357.4,186.3 359.1,182.9 360.7,179.6 362.3,176.5 364.0,173.6 365.6,170.9 367.2,168.4 368.9,166.1 370.5,164.0 372.1,162.1 373.8,160.4 375.4,158.9 377.0,157.5 378.7,156.3 380.3,155.3 381.9,154.4 383.6,153.6 385.2,153.0 386.8,152.5 388.5,152.1 390.1,151.8 391.7,151.6 393.4,151.5 395.0,151.5 396.6,151.5 398.3,151.6 399.9,151.8 401.5,152.0 403.2,152.2 404.8,152.5 406.4,152.8 408.1,153.2 409.7,153.6 411.3,154.0 413.0,154.4 414.6,154.9 416.2,155.3 417.9,155.8 419.5,156.3 421.1,156.8 422.8,157.3 424.4,157.8 426.0,158.3 427.7,158.9 429.3,159.4 430.9,159.9 432.6,160.4 434.2,160.9 435.8,161.5 437.5,162.0 439.1,162.5 440.7,163.0 442.4,163.5 444.0,164.0 445.6,164.5 447.3,165.0 448.9,165.5 450.5,166.0 452.2,166.4 453.8,166.9 455.4,167.4 457.1,167.8 458.7,168.3 460.3,168.7 462.0,169.2 463.6,169.6 465.2,170.1 466.9,170.5 468.5,170.9 470.1,171.3 471.8,171.7 473.4,172.1 475.0,172.5 476.7,172.9 478.3,173.3 479.9,173.7 481.6,174.0 483.2,174.4 484.8,174.8 486.5,175.1 488.1,175.5 489.7,175.8 491.4,176.2 493.0,176.5 494.6,176.8 496.3,177.2 497.9,177.5 499.5,177.8 501.2,178.1 502.8,178.4 504.4,178.7 506.1,179.0 507.7,179.3 509.3,179.6 511.0,179.9 512.6,180.2 514.2,180.4 515.9,180.7 517.5,181.0 519.1,181.2 520.8,181.5 522.4,181.8 524.0,182.0 525.7,182.3 527.3,182.5 528.9,182.8 530.6,183.0 532.2,183.2 533.8,183.5 535.5,183.7 537.1,183.9 538.7,184.1 540.4,184.4 542.0,184.6" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="395.0" cy="151.5" r="3" fill="currentColor"/>
  <line x1="358.7" y1="214" x2="358.7" y2="74" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>
  <circle cx="358.7" cy="183.6" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <line x1="358.7" y1="76" x2="358.7" y2="60" stroke="currentColor" stroke-width="1.3" marker-end="url(#mr06s5k)"/>
  <g font-size="11" fill="currentColor">
    <text x="332" y="28" font-size="12">특이값 σ 방향의 이득</text>
    <text x="341" y="180.5" text-anchor="end" font-size="10">1</text>
    <text x="341" y="143.0" text-anchor="end" font-size="10">2</text>
    <text x="341" y="105.5" text-anchor="end" font-size="10">3</text>
    <text x="341" y="68.0" text-anchor="end" font-size="10">4</text>
    <text x="395.0" y="228" text-anchor="middle" font-size="10">0.3</text>
    <text x="444.0" y="228" text-anchor="middle" font-size="10">0.6</text>
    <text x="493.0" y="228" text-anchor="middle" font-size="10">0.9</text>
    <text x="542.0" y="228" text-anchor="middle" font-size="10">1.2</text>
    <text x="542" y="242" text-anchor="end">σ</text>
    <text x="430.9" y="124.0">1/σ, 감쇠 없음</text>
    <text x="440.7" y="193.4">감쇠, λ = 0.3</text>
    <text x="390.0" y="145.5" text-anchor="end" font-size="10">1.67</text>
    <text x="364.7" y="187.6" font-size="10">0.81</text>
    <text x="364.7" y="66" font-size="10">12.8</text>
    <text x="332" y="258">최대 1/(2λ) = 1.67, σ = λ에서</text>
    <text x="332" y="274">σmin = 0.0779에서 감쇠 없이 12.8,</text>
    <text x="332" y="290">감쇠하면 0.81</text>
  </g>
</svg>

5단계를 P2 위에 축척대로 그렸다. 거의 곧게 편 초기값 $(45^\circ, 10^\circ)$의 말단은 $(1.281,\ 1.526)$으로 목표 $(1,1)$에서 $0.596\,\mathrm{m}$ 떨어져 있다. 감쇠 없는 스텝은 오차를 $\sigma_{\min} = 0.0779$로 나눠 관절을 $7.51\,\mathrm{rad}$ 돌리고 말단을 $3.33\,\mathrm{m}$ 떨어진 $(-1.32,\ -1.39)$로 던지며, $\lambda = 0.3$의 감쇠 스텝은 관절을 $0.478\,\mathrm{rad}$ 돌려 $0.506\,\mathrm{m}$ 떨어진 $(30.3^\circ,\ 33.1^\circ)$로 간다. 오른쪽은 특이값 $\sigma$인 방향의 오차에 스텝이 곱하는 이득이다. 감쇠가 없으면 $1/\sigma$, 감쇠하면 $\sigma/(\sigma^2 + \lambda^2)$이고, 뒤의 것은 $1/(2\lambda) = 1.67$을 넘지 않으며 $\sigma_{\min}$에서 $0.81$이다. 같은 자리에서 감쇠 없는 이득은 $12.8$이다.

### 1. IK는 구조적으로 FK보다 어렵다

FK와 달리 IK의 해는 **0개, 1개, 여러 개, 무한히 많을 수** 있다(엘보 위/아래; 7자유도
팔은 연속체). 이 다봉성은
[[01-canonical-papers/notes/4-vla/diffusion-policy|생성형 정책]]이 대안 행동을 표현하는 이유에 대한 비유다. 서로 다른 유효 해를 평균하면 무효 해가 될 수 있다. 특정 학습 정책의 성능 우위를 증명하는 것은 아니다. **해석적 IK**(닫힌 형태, 예: 회전 관절 여섯 가운데 마지막 세 축이 한 점에서 만나는 구면
손목을 가진 6R 팔)는 모든 가지를 정확히 열거한다; 기하가 허락하지 않으면 수치로 간다.

> **역기구학 문제의 정의.** **역기구학 문제**(inverse kinematics problem)는 *관절에 대해 푸는 방정식*이다. 목표가 주어지면 순기구학이 그 목표로 보내는 관절 벡터를 찾는다. 정의 조건 셋. **목표가 고정되어 있다**: 자세 $X \in SE(3)$, 위치 과제라면 과제 좌표 $x_d$([[04-robotics/modern-robotics/ch02-configuration-space|2장 §1.5]]의 과제 공간)이고, 4장의 FK 사상도 함께 고정이다. **등식이 정확하다**: $T(\theta) = X$일 때 $\theta$가 해이고, 수치 해법은 스스로 밝혀야 할 허용오차 안에서만 그것을 만족한다. 그리고 **해 집합이 문제의 일부다**: $\Theta(X)$는 비어 있을 수도(작업 영역 밖), 유한할 수도(가지 여럿), 연속체일 수도(여유자유도 팔) 있고, $\theta$ 하나를 돌려준 해법은 문제를 풀었지만 집합을 기술하지는 않은 것이다(MR 6장).
>
> $$\Theta(X) = \{\theta \in \mathbb{R}^n :\ T(\theta) = X\} = T^{-1}(X)$$
>
> 여기서 $T^{-1}$은 역함수가 아니라 역상을 뜻한다. FK는 값이 하나로 정해지지만 여러 관절 벡터가 한 자세를 나눠 가질 수 있으므로, 그 역상은 원소가 하나라는 보장이 없다.
>
> - **예**: P2의 말단 목표 $(1,1)$은 $\Theta = \{(0^\circ, 90^\circ),\ (90^\circ, -90^\circ)\}$다(각은 $360^\circ$를 법으로). 목표 $(2.5, 0)$은 $\cos\theta_2 = 2.125$가 필요하므로 $\Theta = \emptyset$이다.
> - **비예**: 도달 가능한 점을 도달 가능한 자세로 착각하는 것. 목표 $(1,1)$에 도구 방향 $\phi = 45^\circ$를 더해 보자. 가지마다 $\phi = \theta_1 + \theta_2$가 정해져 한쪽은 $90^\circ$, 다른 쪽은 $0^\circ$이므로, 두 가지 모두 그 점에 닿는데도 $\Theta = \emptyset$이다. 위치만 푸는 해법은 P2가 할 수 없는 자세 과제에 성공을 보고한다.

> **해석적 IK의 정의.** **해석적 역기구학**(analytic inverse kinematics)은 *닫힌 형태의 풀이법*이다. 해 집합을 나열하는 명시적 공식이다. 정의 조건 셋. **닫힌 형태**: 코사인 법칙과 $\operatorname{atan2}$ 같은 대수·삼각 연산을 유한 번 거칠 뿐이고, 반복도 초기값도 없다. **완전하다**: 가지마다 공식이 하나씩 있어 유한한 $\Theta(X)$의 원소가 모두 나온다. **존재를 판정한다**: 같은 공식이 $\Theta(X) = \emptyset$인 때를 말해 준다. MR 6장 도입부의 평면 2R 팔, 그리고 MR §6.1의 구면 손목을 가진 PUMA형·Stanford형 팔처럼 특별한 기하만 이것을 허락한다.
>
> $$\theta_2 = \pm\arccos\frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2}, \qquad \theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}\bigl(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2\bigr)$$
>
> 여기서 $(x, y)$는 목표다. 코사인 법칙이 정하는 것은 $\cos\theta_2$뿐이고 $\theta_2$의 부호는 열려 있으므로 $\pm$가 두 가지를 준다. $\arccos$는 인수가 $[-1, 1]$에 들 때만 존재하므로 그것이 존재 판정이다. 두 줄 모두 '대상으로 한 번 끝까지'의 1–2단계가 유도한다.
>
> - **예**: $(1,1)$에서 인수가 $0$이므로 $\theta_2 = \pm 90^\circ$, $\theta_1 = 0^\circ$ 또는 $90^\circ$다. 초기값 없이 두 가지가 다 나온다.
> - **비예**: 같은 공식을 $\pm$ 없이 $\theta_2 = \arccos(\cdot)$로 짠 코드. 닫힌 형태이지만 완전하지 않다. $\arccos$는 $[0, \pi]$의 값만 돌려주므로 $(0^\circ, 90^\circ)$만 찾고 $(90^\circ, -90^\circ)$는 끝내 찾지 못한다. 장애물을 피하려고 다른 엘보가 필요한 계획기는 그런 해가 없다는 답을 받는다.

그림과 1–3단계가 이 절을 P2 위에서 한 것이다. 패널의 점 $(1,1)$에 대한 정확한 가지 둘(엘보는 $(1,0)$과 $(0,1)$), 그리고 해가 아닌 평균 $(45^\circ, 0^\circ)$다. 수치 해법은 초기값 근처의 가지를 따라가므로, **국소 탐색 한 번의 실패가 로봇에 해가 없다는 증거는 아니다**. 목표에 도달할 수 없다고 결론짓기 전에 나쁜 초기값, 특이한 국소 사상, 관절 한계 위반, 반복 예산 소진을 먼저 배제한다.

> [!note]- 더 깊이 · Deeper
> **목표 자세는 아직 운동 계획이 아니다.** 엘보가 위인 해와 아래인 해는 말단 자세가 같아도 팔의 컨피규레이션이 크게 다를 수 있고, 관절 한계나 장애물이 한 가지만 불가능하게 만들 수 있다. 그래서 목표 컨피규레이션을 돌려주는 해법은 그곳까지 충돌 없는 경로를 찾는 계획기([[04-robotics/modern-robotics/ch10-motion-planning|10장]])보다 좁은 질문에 답한다.
>
> **초기값과 연속성.** 가까운 목표를 연이어 풀 때 직전 해는 연속성을 유도하므로 좋은 초기값이다. 그렇다고 특이점을 지나거나 가능한 가지가 바뀔 때까지 연속성을 보장하지는 않는다. 다봉적 학습 행동과의 비유는 대안을 표현하는 문제일 뿐, 모든 생성 정책이 회귀보다 낫다는 정리가 아니다.

### 2. 수치 IK = 자세 오차에 대한 뉴턴-랩슨

일반적인 팔에는 닫힌 형태가 없다. P2의 코사인 법칙은 링크 둘이 삼각형을 이루기 때문에 통하는데, 6관절 팔은 그렇게 만들어지지 않은 한(§1의 구면 손목) 그런 삼각형이 없고, 7관절 팔은 답이 연속체를 이룬다. 그래서 수치 IK는 목표를 찾아야 할 근으로 다룬다. 이것은 [[02-foundations/optimization|4. 최적화 §3]]의 뉴턴법을 벡터로 쓴 것이다. 스칼라 방정식 $f(x) = 0$에서 뉴턴 스텝은 $x \leftarrow x - f(x)/f'(x)$다. 여기서는 방정식이 $\mathrm{FK}(\theta) - x_{goal} = 0$이므로 도함수 $f'$가 야코비안 $J$가 되고, 그것으로 나누는 일은 $J\,\Delta\theta = e$를 푸는 일이 되며, $J$가 정사각이 아니거나 가역이 아니면 푸는 것은 최소제곱을 뜻한다. 그래서 $J^\dagger$다. 반복:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(작업 공간 오차)}$$
완전한 SE(3)의 경우 $e$는 물체 좌표로 쓴 6차원 오차 $[\log(T_{now}^{-1} T_{goal})]^\vee$이고 물체 야코비안과 짝지어 쓴다. 로그는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §5]]의 행렬 로그이고, "vee" $^\vee$는 3장의 대괄호 연산을 되돌려 $4\times4$ 행렬에서 여섯 개의 수를 다시 꺼낸다. $J^\dagger$는 유사역행렬([[02-foundations/linear-algebra|최소제곱]])이다.

> **뉴턴-랩슨 IK의 정의.** **뉴턴-랩슨 역기구학**(Newton-Raphson inverse kinematics)은 *반복 근 찾기 알고리즘*이다. 공식이 아니라 관절 벡터의 수열을 만든다. 정의 조건 셋. **과제 잔차의 근을 찾는다**: $e(\theta) = x_d - f(\theta) = 0$을 푼다. **매 스텝 다시 선형화한다**: $J$는 현재 반복점에서 계산하고, 고정하지 않는다. **선형 모형을 최소제곱으로 푼다**: $\Delta\theta = J^\dagger e$이고, $J$가 정사각이고 가역이면 $J^{-1}e$다. 정의 밖의 규칙이 둘 있다(MR §6.2.2). 루프는 잔차로 멈춘다. 곧 $\|e\| \le \epsilon$이고, 자세라면 $\|\omega_b\|$와 $\|v_b\|$에 따로 한계를 둔다. 스텝 크기로 판정하면 4단계의 초기값에서 목표와 $0.586\,\mathrm{m}$ 떨어진 채 멈추기 때문이다. 그리고 해의 끌림 영역, 곧 반복이 그 해에서 끝나는 초기값들의 집합 안에 있는 초기값에서만 수렴한다.
>
> $$\theta_{k+1} = \theta_k + J^\dagger(\theta_k)\,\bigl(x_d - f(\theta_k)\bigr), \qquad \text{stop when } \|x_d - f(\theta_k)\| \le \epsilon$$
>
> 여기서 $f$는 과제 좌표로 쓴 순기구학, $J = \partial f/\partial\theta$다. 스텝은 $e$의 1차 테일러 모형을 0으로 만들므로, 정칙인 해 근처에서는 각 오차가 대략 직전 오차의 제곱에 비례한다.
>
> - **예**: P2, 목표 $(1,1)$, 초기값 $(20^\circ, 70^\circ)$. $\|e\| = 0.347,\ 0.066,\ 0.0021,\ 2\times10^{-6}\,\mathrm{m}$로 줄며 $(0^\circ, 90^\circ)$에 내려앉는다. $(60^\circ, -60^\circ)$에서 시작하면 같은 루프가 대신 $(90^\circ, -90^\circ)$에 내려앉는다.
> - **비예**: 초기값에서 $J$를 고정한 같은 루프, 곧 현(chord) 반복. $(20^\circ, 70^\circ)$에서 시작해도 $(0^\circ, 90^\circ)$에 닿기는 하지만, 세 스텝 뒤의 $\|e\|$가 뉴턴-랩슨의 $2\times10^{-6}$에 비해 $1.2\times10^{-3}\,\mathrm{m}$다. 매 스텝 오차를 제곱하는 대신 $0.06$ 근처로 모이는 비율을 곱할 뿐이기 때문이다. 시간을 아끼려고 야코비안 하나를 재사용한 해법은 그 값을 반복 횟수로 치른다.

**SE(3) 오차를 숫자로, P2에서.** 홈 $\theta = (0, 0)$에서 시작하므로 $T_{now} = M$, 곧 [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 홈 컨피규레이션이다(MR이 쓰는 글자이고, [[02-foundations/manipulator-kinematics-dynamics|10]]의 질량 행렬 $M$이 아니다). 그리고 목표는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장의 '대상으로 한 번 끝까지']] 1단계에서 유도한 카탈로그 도구 자세 $T_{goal} = T_{sb}$다. 그러면 $M^{-1}T_{sb}$는 $R = R_z(90^\circ)$, $p = (-1, 1, 0)$이고, 3장 §5의 로그가 $e = (0, 0, \pi/2;\ 0, \pi/2, 0) = \mathcal{B}_2\cdot\frac{\pi}{2}$를 준다. [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 엘보 물체 스크류 $\mathcal{B}_2 = (0,0,1;\ 0,1,0)$을 4분의 1바퀴 돌린 것이다. 홈에서 물체 야코비안의 열은 4장의 물체 스크류 $\mathcal{B}_1 = (0,0,1;\ 0,2,0)$과 $\mathcal{B}_2$이고 $J_b^\dagger e = (0,\ \pi/2)$다. 뉴턴 한 스텝이 정확히 $(0^\circ, 90^\circ)$에 떨어진다. 이 오차 자체가 관절 하나의 스크류이기 때문이다. 일반적인 오차는 그렇지 않으므로 루프가 반복하고, §3이 그것을 손으로 한다.

> [!note]- 더 깊이 · Deeper
> **자세 전체 오차를 조심스럽게.** 위의 물체 프레임 자세 오차에서 행렬 로그의 결과는 먼저 리 대수의 행렬이다. 그 여섯 좌표가 오차 벡터이고, 물체 야코비안과 짝을 이룬다. 라디안과 길이는 단위가 다르므로 회전과 병진의 정지 허용오차를 따로 두고, 관절 한계와 충돌은 수치 수렴과 별개로 검사한다.
>
> **유사역행렬이 하는 일과 하지 않는 일.** 유사역행렬은 국소 선형 잔차를 최소화하고, 대안이 남으면 노름이 가장 작은 갱신을 고른다. 비선형 자세 문제 전체를 한 번에 풀지는 않으므로 루프가 반복한다. 책의 [공식 수치 IK 설명](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)이 같은 국소 근사와 갱신 루프를 따라간다.

### 3. 한 반복을 손으로 끝까지 — 평면 2R 팔

§2의 반복은 매번 같은 네 가지를 한다. FK로 지금의 말단을 계산하고, 목표까지의 오차를 만들고, 지금의 관절에서 $J$를 구하고, $J\,\Delta\theta = e$를 풀어 갱신한다. 그리고 $J$가 국소 변화만 말해 주므로 처음부터 다시 한다. 여기서 그 넷을 손으로 한 번 한 뒤, 그것이 만드는 수열을 본다.

$L_1 = L_2 = 1$; 목표 말단 $(-1, 1)$ (참값: $\theta^* = (90°, 90°)$ —
[[04-robotics/modern-robotics/ch04-forward-kinematics|4장 §2]]의 계산 예제에서). 초기값
$\theta^{(0)} = (45°, 90°)$에서 시작.

- **FK**: 말단 $= (\cos 45° + \cos 135°,\; \sin 45° + \sin 135°)$ — 계산하면
  $(0.707 - 0.707,\; 0.707 + 0.707) = (0,\, 1.414)$.
- **오차**: $e = (-1, 1) - (0, 1.414) = (-1, -0.414)$; $\|e\| = 1.08$.
- **야코비안** (5장 공식, $s_1 = c_1 = 0.707$, $s_{12} = 0.707$, $c_{12} = -0.707$). 5장의 $J(\theta)$를 지금의 관절에서 계산하기 때문이다:
  $$J = \begin{pmatrix} -1.414 & -0.707 \\ 0 & -0.707 \end{pmatrix}, \quad \det J = 1.0$$
- **갱신**: $\det J = 1$이므로 대각을 맞바꾸고 비대각의 부호를 바꾸면 $J^{-1} = \begin{pmatrix} -0.707 & 0.707 \\ 0 & -1.414 \end{pmatrix}$이고, $\Delta\theta = J^{-1} e = (0.707 - 0.293,\; 0.586) = (0.41,\; 0.59)$ rad $= (23.7°,\; 33.6°)$, 따라서
  $\theta^{(1)} = (68.7°,\; 123.6°)$.
- **확인**: $\theta_1 + \theta_2 = 192.3°$인 $\theta^{(1)}$에서 FK 말단은 $(0.363 - 0.977,\ 0.932 - 0.213) \approx (-0.61,\, 0.72)$;
  $\|e\| = 0.48$ — **한 스텝에 오차가 절반**이 됐고, 반복점은 $(90°, 90°)$ 쪽으로
  움직이고 있다. 다만 엘보는 답의 $90°$를 지나 $123.6°$까지 넘어갔다. 답에서 멀 때 뉴턴의 전체 스텝은 선형 모형을 너무 멀리까지 믿기 때문이다.

**나머지 실행.** 네 가지를 되풀이하면 $\|e\| = 1.08,\ 0.477,\ 0.0685,\ 0.0023,\ 2.7\times10^{-6}\,\mathrm{m}$이고, 관절은 $(68.7°, 123.6°)$, $(90.5°, 93.4°)$, $(89.9°, 90.1°)$를 거쳐 $(90°, 90°)$에 내려앉는다. 첫 스텝이 오차를 절반으로만 줄이는 것은 초기값이 답에서 $45°$ 떨어져 있어 선형 모형 $J$가 좋은 길잡이가 못 되기 때문이다. 반복점이 가까워지면 각 오차가 직전 오차 제곱의 절반쯤이 된다. $0.0685^2/2 = 0.0023$, 이어서 $0.0023^2/2 = 2.7\times10^{-6}$이다. 이것이 뉴턴-랩슨 상자의 이차 수렴이고, 맞는 자릿수가 스텝마다 대략 두 배가 된다. 반복 횟수에 대한 $\|e\|$를 로그 축에 그리는 것이 모든 IK 구현의 표준 검산이다. 곧게 내려가는 직선은 낡은 $J$(현 반복 비예), 멈춤은 특이한 초기값(4단계), 갑작스러운 상승은 거의 특이한 초기값(5단계)을 뜻한다.

### 4. 실전의 두 가지 복잡성

- **특이점**: 근처에서 $J^\dagger$가 폭발한다. 쉬운 말로 된 해법: $\lambda^2 I$를 더해
  $J$가 랭크를 잃어도 역행렬을 구할 행렬이 계속 가역이 되게 하고, 거대한 스텝 대신 약간
  틀리지만 크기가 유한한 스텝을 받아들인다. 그것이 **감쇠 최소제곱**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$이며, 정확도를 안정성과 맞바꾼다. 변장한 릿지 회귀인데, 릿지 회귀는 답의 크기에 벌점을 주는 최소제곱을 통계에서 부르는 이름이다.
  그리고 정확히 이 잔차에 대한 **Levenberg–Marquardt** 스텝이기도 하다. 아래 메모에서 증명하는 항등식
  $J^\top(JJ^\top + \lambda^2 I)^{-1} = (J^\top J + \lambda^2 I)^{-1}J^\top$가 두 식을 같게
  만들므로 $\lambda$는 신뢰 파라미터이고, 감쇠 IK는 SLAM(동시적 위치 추정 및 지도 작성)과 보정이 돌리는 바로 그 알고리즘이다
  ([[02-foundations/optimization|4. 최적화 §3.5]]).
  페이지를 오갈 때 챙길 관례가 하나 있다. [[02-foundations/linear-algebra|1. 선형대수 §4.5]]와 [[02-foundations/optimization|4. 최적화 §3.5]]는 이 페이지가 $\lambda^2$로 쓰는 감쇠를 $\lambda$로 쓴다. 그래서 이 페이지의 $\lambda = 0.3$은 거기서 $\lambda = 0.09$다. MR 자체는 그냥 유사역행렬에서 멈추고, 감쇠 형태가 어디서 왔는지는 아래 메모가 말한다.

> [!note]- 더 깊이 · Deeper
> **항등식을 한 줄로.** $(J^\top J + \lambda^2 I)J^\top = J^\top JJ^\top + \lambda^2 J^\top = J^\top(JJ^\top + \lambda^2 I)$의 왼쪽에 $(J^\top J + \lambda^2 I)^{-1}$을, 오른쪽에 $(JJ^\top + \lambda^2 I)^{-1}$을 곱한다. $\lambda > 0$이면 두 행렬 모두 양정부호라 가역이다.
>
> **감쇠 최소제곱의 출처.** MR 자체는 이것을 다루지 않는다. 6장은 특이점에서 그냥 유사역행렬을 주고, 감쇠와 여유자유도 계열은 주석과 참고문헌으로 넘기므로 6장에서 찾지 마라. 여기 쓴 $\lambda^2$ 표기는 그 바깥 문헌의 관례다. 그러면 $\lambda$가 특이값과 같은 단위를 갖고, 이득 $\sigma/(\sigma^2 + \lambda^2)$은 정확히 $\sigma = \lambda$에서 최대가 된다. 2링크 팔을 처음부터 끝까지 코드로 옮긴 것 — 두 엘보 해를 모두 주는 해석적 IK와 감쇠 스텝 한 번 — 은 [[02-foundations/algorithms/robotics-ai-problems|11.8 §6]]에 있다.

> **감쇠 최소제곱의 정의.** **감쇠 최소제곱**(damped least squares, DLS)은 *수치 IK를 위한 정칙화된 스텝 규칙*이다. 선형화한 오차를 가장 잘 줄이면서 스텝 자신의 길이에 값을 치르는 관절 스텝이다. 정의 조건 셋. **감쇠 $\lambda > 0$**: 그러면 $JJ^\top + \lambda^2 I$가 양정부호라서 특이하든 아니든 모든 $\theta$에서 역행렬이 있다. **맞바꿈 목적함수**: 스텝은 잔차에 스텝 크기의 벌점을 더한 값을 최소화한다. **이득에 상한이 있다**: 특이값 $\sigma$인 방향의 오차에는 $1/\sigma$ 대신 $\sigma/(\sigma^2 + \lambda^2) \le 1/(2\lambda)$가 곱해지고, 특이점에서 멀 때 $\lambda \to 0$이면 스텝은 $J^\dagger e$로 돌아간다.
>
> $$\Delta\theta = J^\top\bigl(JJ^\top + \lambda^2 I\bigr)^{-1}e = \arg\min_{\Delta\theta}\ \|J\Delta\theta - e\|^2 + \lambda^2\|\Delta\theta\|^2$$
>
> 여기서 $e$는 과제 오차, $\lambda$는 감쇠다. 두 변이 같은 것은 목적함수의 기울기를 0으로 두면 위의 Levenberg–Marquardt 형태 $(J^\top J + \lambda^2 I)\,\Delta\theta = J^\top e$가 나오기 때문이다.
>
> - **예**: 5단계의 초기값 $(45^\circ, 10^\circ)$, $\sigma_{\min} = 0.0779$. 감쇠가 없으면 약한 방향이 $12.8$배로 증폭되어 스텝이 $7.51\,\mathrm{rad}$다. $\lambda = 0.3$이면 그 방향의 이득은 $0.81$이고, 어떤 스텝도 $0.994\,\mathrm{rad}$를 넘지 못하며, 팔은 $(30.3^\circ, 33.1^\circ)$로 가서 $\|e\| = 0.506$이 된다.
> - **비예**: 그냥 유사역행렬 $J^\dagger$. 라이브러리가 모든 $\theta$에서 돌려주니 안전해 보인다. 어디서나 정의되지만 이득에 상한이 없다. $\sigma \to 0$이면 $1/\sigma$가 끝없이 커지고, 그것이 위의 $7.51\,\mathrm{rad}$ 스텝이다. DLS를 이것으로 바꾼 해법은 특이점에서 먼 곳의 정확도를 얻는 대신 특이점 근처의 통제를 잃는다.

- **여유자유도** ($n > 6$): $J$의 영공간([[02-foundations/linear-algebra|§2의 영공간]]을 이번엔 $J$에 적용한 것: $J\dot\theta = 0$인 관절 속도들)은 도구를 움직이지 않고 관절만 움직인다 — 이를
  2차 목표(관절 한계, 장애물, 특이점 회피)에 쓴다.

**위키 연결**: 말단 공간 원격조작 스택과 말단 공간 VLA(시각·언어 입력에서 행동을 내는 정책)는 정책 출력과 모터 명령 사이에서 IK(또는 그 속도 수준 사촌)를 돌린다. [[01-canonical-papers/notes/4-vla/act|ALOHA]] 같은 관절 공간 장비는 이것을 건너뛴다.

### 스스로 점검

1. 위의 목표 $(-1,1)$에 대해 $(90°, 90°)$ 말고 *다른* 해석해는 무엇인가?
2. 뉴턴 IK에 *좋은 초기값*이 필요한 이유는, 그리고 제어 루프에서는 보통 무엇이 그것을
   제공하는가?
3. $\theta_2 = 0$에서 정확히 시작해 IK를 돌리면 무엇이 잘못되는가?
4. 감쇠 최소제곱 갱신식을 쓰고, $\lambda$가 무엇을 맞바꾸는지 말하라.

> [!tip]- 정답 · Answers
> 1. 엘보가 아래인 가지 $(180°, -90°)$. 확인: 링크 1이 $-\hat x$ 방향으로 $(-1,0)$까지 가고, 링크 2가 $-90°$ 돌아 $+\hat y$를 향하므로 말단은 $(-1,1)$이다. ✓ 관절 컨피규레이션 둘에 과제 자세 하나 — 한 예제 안에 담긴 IK의 다봉성이다.
> 2. 뉴턴법은 국소적으로만 수렴한다. 해에서 멀면 선형화 $J$가 나쁜 모델이어서 스텝이 발산하거나 다른 가지에 떨어질 수 있다. 제어 루프에서는 목표가 연속적으로 움직이므로 직전 시점의 해가 자연스러운 초기값이고, 덕분에 팔이 운동 도중 엘보 컨피규레이션을 뒤집지 않고 한 가지에 머문다.
> 3. $\theta_2 = 0$은 특이점이다: $\det J = L_1L_2\sin\theta_2 = 0$이므로 $J^{-1}$가 존재하지 않는다. 유사역행렬은 그래도 스텝을 하나 돌려주지만 잃어버린 방향의 오차는 전혀 줄이지 못한다. 반복은 정체하거나, 감쇠가 없으면 수치적으로 폭주한다.
> 4. $\Delta\theta = J^\top(JJ^\top + \lambda^2 I)^{-1}e$. 큰 $\lambda$는 특이점 근처에서 안정하지만 느리고 편향된다. 여기서 편향이란 스텝이 더 이상 정확한 최소제곱 문제를 풀지 않는다는 뜻이다. 작은 $\lambda$는 특이점에서 멀 때 정확하지만 가까이서는 폭주한다. 이것은 릿지 회귀이고, $\lambda$가 그 릿지 파라미터다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**, 각 문항이 정하는 목표. 해석해만 — 뉴턴 루프 없음.

1. **그리기.** $x$축 위의 목표 $(1.5,\ 0)$에 대한 위의 그림: 말단을 거기 두는 IK 가지 둘, 두 엘보 점의 이름, 그리고 가지마다 옆에 적은 관절 각. 두 관절 벡터의 평균을 점선으로 더하고, 그 말단에 $\times$를 치고, 목표까지 되돌아오는 빗나감을 표시하라.
2. **유도.** 카탈로그 목표보다 반 미터 아래, 패널 면 위의 목표 $(1,\ 0.5)$. (a) $\cos\theta_2$와 두 가지, 그리고 각 엘보 점. (b) 두 관절 벡터의 성분별 평균은 말단을 어디에 두고, 목표에서 얼마나 떨어져 있는가? P2의 단위 링크에서 평균은 언제나 $\operatorname{atan2}(y, x)$ 방향으로 곧게 편 팔이고, 따라서 $2 - r$만큼 지나침을 보여라. $r$은 목표의 베이스에서의 거리다. (c) [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §2]]의 매 스텝 갱신한 분해 속도 실행은 말단을 $(1,1)$에서 $(0.999,\ 0.500)$까지 옮기고 관절이 $(-29.45^\circ,\ 112.06^\circ)$에서 끝났다. 어느 가지에 내려앉았고, 왜 그 가지인가?
3. **해석.** P2의 엘보에 관절 한계 $|\theta_2| \le 100^\circ$를 더한다. $(1,1)$과 $(1,\ 0.5)$의 가지 가운데 무엇이 살아남는가? 이 한계는 작업 영역의 어느 부분을 없애고, 그 안의 목표를 해석적 공식과 뉴턴 루프는 각각 어떻게 보고하는가?

> [!note]- 그리는 법 · How to draw it
> - 목표는 $(1.5,\ 0)$에 작은 원 하나로 한 번만 그리고, 모든 팔이 거기서 끝나거나 그것을 가리키게 둔다.
> - 가지마다 링크 둘이다. 링크 1은 베이스에서 그 엘보까지, 링크 2는 엘보에서 목표까지. 한 가지는 실선, 다른 가지는 더 얇게 그린다. 목표가 $x$축 위에 있으므로 두 가지는 $x$축에 대해 거울상이다.
> - 엘보 두 점 $(0.75,\ -0.661)$과 $(0.75,\ 0.661)$에 이름을 붙이고, 가지마다 각 $(-41.4^\circ,\ 82.8^\circ)$와 $(41.4^\circ,\ -82.8^\circ)$를 적는다. 말단은 같고 팔이 둘이다.
> - 두 관절 벡터의 평균은 $(0^\circ,\ 0^\circ)$이다. $+x$를 따라 곧은 선분 하나로 점선을 그리고, $(2,0)$의 말단에 $\times$를 친 뒤 목표까지 되돌아오는 $0.5\,\mathrm{m}$의 빗나감을 표시한다. 목표 근처가 아니라 눈에 띄게 지나쳐 있어야 한다.
> - 점선 말단에서 "도달 가능"은 곧은 팔에 수직인 양방향 화살표, "원하는 방향"은 팔을 따라 목표 쪽으로 되돌아가는 화살표다. 둘을 직각으로 그린다. 곧은 팔은 다시 특이하고, 오차는 전부 팔이 움직일 수 없는 방향에 있다.

> [!tip]- 정답 · Solutions
> 1. $\cos\theta_2=(1.5^2-2)/2=0.125$이므로 $\theta_2=\pm82.8^\circ$, $\theta_1=-\operatorname{atan2}(\sin\theta_2,\ 1+\cos\theta_2)=\mp41.4^\circ$다. 가지는 엘보가 $(0.75,\ -0.661)$인 $(-41.4^\circ,\ 82.8^\circ)$와 엘보가 $(0.75,\ 0.661)$인 $(41.4^\circ,\ -82.8^\circ)$로, $x$축에 대해 거울상이다. 평균은 $(0^\circ,\ 0^\circ)$, 곧 곧은 팔이고 말단은 $(2,0)$이다. 목표를 $0.5\,\mathrm{m}$, 베이스에서의 거리의 삼분의 일만큼 지나치고, 위 그림처럼 정확히 특이점 위에 있다. 두 IK 해의 평균은 이번에도 해가 아니다.
> 2. (a) $\cos\theta_2=(1^2+0.5^2-2)/2=(1.25-2)/2=-0.375$이므로 $\theta_2=\pm112.0^\circ$다. $\theta_2=+112.0^\circ$이면 $\theta_1=\operatorname{atan2}(0.5,1)-\operatorname{atan2}(\sin112.0^\circ,\ 1+\cos112.0^\circ)=26.6^\circ-\operatorname{atan2}(0.927,\ 0.625)=26.6^\circ-56.0^\circ=-29.4^\circ$이고 엘보는 $(\cos(-29.4^\circ),\ \sin(-29.4^\circ))=(0.871,\ -0.492)$다. $\theta_2=-112.0^\circ$이면 $\theta_1=26.6^\circ+56.0^\circ=82.6^\circ$, 엘보는 $(0.129,\ 0.992)$다. FK로 둘 다 검산된다. 앞의 것은 전완이 $-29.4^\circ+112.0^\circ=82.6^\circ$를 향하므로 말단이 $(0.871+0.129,\ -0.492+0.992)=(1.0,\ 0.5)$이고, 뒤의 것은 두 방향을 맞바꿔 같은 말단을 준다. (b) 평균은 $(26.6^\circ,\ 0^\circ)$, 목표 방향으로 곧게 편 팔이고 말단은 $2(\cos26.6^\circ,\ \sin26.6^\circ)=(1.789,\ 0.894)$, 목표에서 $0.882\,\mathrm{m}$ 떨어져 있다. 일반적으로 단위 링크에서는 $\operatorname{atan2}(\sin\beta,\ 1+\cos\beta)=\beta/2$다. $\sin\beta=2\sin\tfrac\beta2\cos\tfrac\beta2$, $1+\cos\beta=2\cos^2\tfrac\beta2$이기 때문이다. 그래서 $\phi=\operatorname{atan2}(y,x)$, $\beta=|\theta_2|$라 하면 가지는 $(\phi-\beta/2,\ \beta)$와 $(\phi+\beta/2,\ -\beta)$이고 평균은 $(\phi,\ 0)$, 곧 $\phi$ 방향으로 곧게 편 팔이다. 그 말단은 거리 2에 있으므로 거리 $r$의 목표를 $2-r$만큼 지나친다. 여기서는 $2-\sqrt{1.25}=0.882$, $(1,1)$에서는 $0.586$, 그리기 문항의 $(1.5,\ 0)$에서는 $0.5$다. (c) 첫째 가지 $(-29.4^\circ,\ 112.0^\circ)$다. 실행은 $\theta_2>0$인 $(0^\circ,\ 90^\circ)$에서 시작해 연속적으로 움직였고, 다른 가지로 가려면 $\theta_2$가 $J$를 뒤집을 수 없는 곧은 팔의 특이점 $0^\circ$를 지나야 했다. $\theta_2$의 $0.04^\circ$ 차이는 실행의 밀리미터 미만 드리프트다.
> 3. 엘보는 이제 $|\theta_2|\le100^\circ$여야 한다. $(1,1)$은 $|\theta_2|=90^\circ$가 필요하므로 두 가지가 모두 살아남고, $(1,\ 0.5)$는 $|\theta_2|=112.0^\circ$가 필요하므로 도달 범위 $2\,\mathrm{m}$ 안쪽 깊숙이 있는데도 하나도 살아남지 못한다. 단위 링크에서 $r^2=2+2\cos\theta_2$이므로 $|\theta_2|\le100^\circ$는 $r\ge\sqrt{2+2\cos100^\circ}=\sqrt{2-0.347}=1.286\,\mathrm{m}$를 뜻한다. 한계 없는 팔은 $0$부터 $2$까지 모든 $r$에 닿았는데, 이 한계가 베이스 둘레에 반지름 $1.286\,\mathrm{m}$의 구멍을 낸다. 해석적 공식은 비교 한 번, $\cos\theta_2=-0.375<\cos100^\circ=-0.174$로 판정하고 한계 안에 해가 없다고 보고한다. 한계에 묶인 뉴턴 루프는 수렴에 실패할 뿐이라, 도달할 수 없는 목표와 나쁜 초기값을 구별하지 못한다(§1).
