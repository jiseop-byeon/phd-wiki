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
> You need the Jacobian from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]], least squares ([[02-foundations/linear-algebra|1. Linear Algebra §2]]) and the pseudoinverse ([[02-foundations/linear-algebra|§4.5]]), and Newton's method ([[02-foundations/optimization|4. Optimization §3]]).
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안과 [[02-foundations/linear-algebra|최소제곱/유사역행렬]], [[02-foundations/optimization|뉴턴법]]을 알고 있어야 한다.

## English

**Core question**: given a desired end-effector pose, what joint angles achieve it?

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

**Step 2 — the shoulder angle, one per branch.** With $\theta_2$ chosen, the arm becomes a rigid triangle and the tip's bearing from the base splits into two pieces — where the target lies, minus how far the folded forearm swings the tip off link 1's own direction:

$$\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2)$$

and the second term flips sign with $\theta_2$, so the two elbow choices give two different shoulder angles rather than one. For $\theta_2 = +90^\circ$: $\operatorname{atan2}(1,1) - \operatorname{atan2}(1, 1) = 45^\circ - 45^\circ = 0^\circ$, giving $\theta = (0^\circ, 90^\circ)$. For $\theta_2 = -90^\circ$: $45^\circ - \operatorname{atan2}(-1, 1) = 45^\circ - (-45^\circ) = 90^\circ$, giving $\theta = (90^\circ, -90^\circ)$. Both check against FK: $(\cos 0^\circ + \cos 90^\circ,\ \sin 0^\circ + \sin 90^\circ) = (1,1)$ and $(\cos 90^\circ + \cos 0^\circ,\ \sin 90^\circ + \sin 0^\circ) = (1,1)$. The first is the catalog frozen pose; nothing on this page chose it over the other, the catalog did.

**Step 3 — why the average is not an answer, in numbers.** The componentwise mean is $(45^\circ, 0^\circ)$, a straight arm, tip at $(\sqrt2, \sqrt2)$, a miss of $\sqrt{2(\sqrt2 - 1)^2} = 0.5858\,\mathrm{m}$ on a target $1.414\,\mathrm{m}$ from the base — a $41\,\%$ overshoot, not a rounding error. The set of IK solutions is not convex, and averaging is exactly the operation that assumes it is.

**Step 4 — hand the mean configuration to a numerical solver and watch nothing happen.** Seed Newton IK at $\theta^{(0)} = (45^\circ, 0^\circ)$. With $s_1 = c_1 = s_{12} = c_{12} = 0.7071$ the ch.5 formula gives

$$J = \begin{pmatrix}-1.4142 & -0.7071\\ 1.4142 & 0.7071\end{pmatrix}, \qquad \det J = L_1L_2\sin\theta_2 = 0, \qquad \sigma = (2.2361,\ 0)$$

so the map has rank 1: its one reachable direction is $(-0.7071, 0.7071)$, perpendicular to the arm. The error is $e = (1,1) - (\sqrt2,\sqrt2) = (-0.4142, -0.4142)$, which points straight back *along* the arm. Then

$$J^\top e = \begin{pmatrix}-1.4142 & 1.4142\\ -0.7071 & 0.7071\end{pmatrix}\begin{pmatrix}-0.4142\\ -0.4142\end{pmatrix} = \begin{pmatrix}0.5858 - 0.5858\\ 0.2929 - 0.2929\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}$$

and every update built on $J^\top$ inherits that zero: the pseudoinverse step is $0$, and so is the damped step $J^\top(JJ^\top + \lambda^2 I)^{-1}e$ for **every** $\lambda$, because the damping only changes what multiplies a vector that is already zero. The solver terminates on "no progress" while standing $58.6\,\mathrm{cm}$ from a target that has two exact solutions. Damping is the wrong medicine here; a different seed is the only cure.

**Step 5 — one degree off the singularity is a different failure.** Move the seed to $(45^\circ, 10^\circ)$ so the arm is merely *nearly* straight: now $\det J = \sin 10^\circ = 0.1736$ and $\sigma = (2.2279,\ 0.0779)$. The error $\|e\| = 0.5964$ divided by that smallest singular value is what sets the step size, and the undamped update is a joint move of $\|\Delta\theta\| = 7.51\,\mathrm{rad}$ — it hurls the tip to $(-1.32, -1.39)$ and drives $\|e\|$ from $0.596$ up to $3.33$. Damping at $\lambda = 0.3$ instead steps to $(30.3^\circ, 33.1^\circ)$ and brings $\|e\|$ down to $0.506$: smaller than the exact least-squares step, and in the right direction. **Exactly singular means no step; nearly singular means a wild one.** They look alike on a plot of $\|e\|$ and need opposite fixes.

### 1. IK is structurally harder than FK

Unlike FK, IK has **zero, one, several, or infinitely many** solutions (elbow-up vs
elbow-down; a 7-dof arm has a continuum). This multimodality is a useful analogy for why
[[01-canonical-papers/notes/4-vla/diffusion-policy|generative policies]] represent alternative actions: averaging distinct valid solutions may give an invalid one. It does not establish that a particular learned policy performs better. **Analytic IK**
(closed-form, e.g. 6R with spherical wrist) enumerates all branches exactly; when geometry
doesn't permit it, go numerical.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="one target reached by two joint solutions, and the average of the two overshooting it">
  <g stroke="currentColor" stroke-width="1" opacity="0.25">
    <line x1="40" y1="190" x2="250" y2="190"/><line x1="60" y1="200" x2="60" y2="30"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.85">
    <polyline points="60,190 160,190 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.45">
    <polyline points="60,190 60,90 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.7">
    <polyline points="60,190 131,119 201,49"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="4.5"/>
    <circle cx="160" cy="190" r="3.5" opacity="0.85"/>
    <circle cx="60" cy="90" r="3.5" opacity="0.45"/>
    <circle cx="131" cy="119" r="3" opacity="0.7"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.8">
    <circle cx="160" cy="90" r="6"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.7">
    <line x1="196" y1="44" x2="206" y2="54"/>
    <line x1="196" y1="54" x2="206" y2="44"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="176" y="196">solution 1 &#183; (0&#176;, +90&#176;)</text>
    <text x="24" y="78" opacity="0.85">solution 2 &#183; (90&#176;, &#8722;90&#176;)</text>
    <text x="214" y="46" opacity="0.85">lands at (1.41, 1.41)</text>
    <text x="176" y="94">target (1, 1)</text>
    <text x="286" y="140" opacity="0.85">average &#183; (45&#176;, 0&#176;)</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5" fill="none">
    <line x1="283" y1="136" x2="140" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">Two joint pairs put the tip on the same target &#8212; that is what &#8220;several solutions&#8221; means.</text>
    <text x="24" y="226">Average them and the arm straightens to (1.41, 1.41), missing by 0.59. The mean of two</text>
    <text x="24" y="240">valid answers is not an answer, which is the classical picture of why multimodal action</text>
    <text x="24" y="254">prediction needs a representation that can hold alternatives.</text>
  </g>
</svg>

**Those two solutions are plant P2 at tip $(1,1)$.** Unit links: the elbow of $(0^\circ,90^\circ)$ sits at $(1,0)$ with the forearm along $+y$; the elbow of $(90^\circ,-90^\circ)$ sits at $(0,1)$ with the forearm along $+x$. Both tips are $(1,1)$. The catalog frozen pose ([[02-foundations/lab-plants|0.6]]) is the first of these. The dashed average in the figure is $(45^\circ,0^\circ)$, a straight arm whose tip is $(\sqrt{2},\sqrt{2})$ — not a solution. The problem set asks you to draw both branches and to say that; the figure has already done the geometry.

**A pose target is not yet a motion plan.** Elbow-up and elbow-down solutions can reach the same tip pose through very different arm configurations. Joint limits or an obstacle can invalidate one branch without invalidating the other. A solver returning a target configuration therefore answers a narrower question than a planner finding a collision-free route to it.

A numerical solver usually follows the branch near its initial guess. If it stops without success, distinguish an unreachable target from a poor initialization, a singular local map, a violated limit, or an iteration budget that expired. One unsuccessful local search does not prove that the robot has no solution.

**Check your understanding.** For successive nearby targets, the previous solution is often a useful starting point because it encourages continuity. It does not guarantee continuity through singularities or changes of feasible branch. The analogy to multimodal learned actions is about representing alternatives; it is not a theorem that every generative policy outperforms regression.

### 2. Numerical IK = Newton-Raphson on the pose error

Iterate:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(task-space error)}$$
where in the full SE(3) case $e$ is the six-vector error $[\log(T_{now}^{-1} T_{goal})]^\vee$ in body coordinates, paired with the body Jacobian
([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3]]'s log map; the "vee" $^\vee$ undoes ch.3's bracket operation, pulling the six numbers back out of the $4\times4$ matrix), and $J^\dagger$
is the pseudoinverse ([[02-foundations/linear-algebra|least squares]]).

**Follow one iteration.** Compute the current pose, express the goal error in a chosen frame, and evaluate the matching Jacobian at the current joints. Solve the local relation JΔθ ≈ e, update the joint guess, then recompute both pose and error. Repeating is necessary because the Jacobian describes only local change. A damping or step-size rule can keep the update from trusting that approximation too far.

For the body-frame pose error written above, the matrix logarithm is first a matrix in the Lie algebra; its six coordinates form the error vector. Pair those coordinates with the body Jacobian. Use separate rotation and translation stopping tolerances because radians and length are different units. Also enforce joint limits and check collision separately from numerical convergence.

**Check your understanding.** The pseudoinverse minimizes the local linear residual and selects a minimum-norm update when alternatives remain. It does not directly solve the entire nonlinear pose problem. See the [official numerical IK walkthrough](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) for the local approximation and update loop.

### 3. One full iteration, by hand — planar 2R arm

$L_1 = L_2 = 1$; target tip $(-1, 1)$ (true answer: $\theta^* = (90°, 90°)$, from
[[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]]'s example). Start at
$\theta^{(0)} = (45°, 90°)$.

- **FK**: tip $= (\cos 45° + \cos 135°,\; \sin 45° + \sin 135°)$ — compute:
  $(0.707 - 0.707,\; 0.707 + 0.707) = (0,\, 1.414)$.
- **Error**: $e = (-1, 1) - (0, 1.414) = (-1, -0.414)$; $\|e\| = 1.08$.
- **Jacobian** (ch.5 formula, $s_1 = c_1 = 0.707$, $s_{12} = 0.707$, $c_{12} = -0.707$):
  $$J = \begin{pmatrix} -1.414 & -0.707 \\ 0 & -0.707 \end{pmatrix}, \quad \det J = 1.0$$
- **Update**: $\Delta\theta = J^{-1} e = (0.41,\; 0.59)$ rad $= (23.7°,\; 33.6°)$, so
  $\theta^{(1)} = (68.7°,\; 123.6°)$.
- **Check**: FK at $\theta^{(1)}$ gives tip $\approx (-0.61,\, 0.72)$;
  $\|e\| = 0.48$ — **the error halved in one step**, and the iterate is moving toward
  $(90°, 90°)$. A few more iterations converge; that plot of $\|e\|$ vs iteration is the
  standard sanity check for any IK implementation.

### 4. The two practical complications

- **Singularities**: near them $J^\dagger$ explodes. The fix in plain words: add $\lambda^2 I$
  so the matrix to invert stays invertible even when $J$ loses rank, accepting a slightly
  wrong but bounded step instead of a huge one. That is **damped least squares**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$, which trades accuracy for stability — ridge regression in
  disguise. It is also, exactly, the **Levenberg–Marquardt** step for this residual: the
  identity $J^\top(JJ^\top + \lambda I)^{-1} = (J^\top J + \lambda I)^{-1}J^\top$ makes the
  two expressions the same, so $\lambda$ is a trust parameter and damped IK is the same
  algorithm SLAM and calibration run ([[02-foundations/optimization|4. Optimization §3.5]]).

  Note where this comes from: **MR itself does not present damped least squares.** At a
  singularity chapter 6 offers the bare pseudo-inverse and sends the damped and redundant-arm
  family to its notes and references. The $\lambda^2$ form written here is the convention of
  that outside literature, chosen so that $\lambda$ carries units; the optimization page
  writes $\lambda$. Do not go looking for it in the chapter. For a two-link arm coded end to
  end — analytic IK with both elbow branches, then one damped step — see [[02-foundations/algorithms/robotics-ai-problems|11.8 §6]].
- **Redundancy** ($n > 6$): the null space of $J$ ([[02-foundations/linear-algebra|§2's null space]], this time of $J$: joint velocities with $J\dot\theta = 0$) moves joints without moving the tool —
  spend it on secondary objectives (joint limits, obstacles, singularity avoidance).

**Wiki connections**: end-effector-space teleop stacks and VLAs run IK (joint-space rigs such as [[01-canonical-papers/notes/4-vla/act|ALOHA]] skip it) (or its velocity-level cousin) between policy output
and motor commands.

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
> 4. $\Delta\theta = J^\top(JJ^\top + \lambda^2 I)^{-1}e$. Large $\lambda$ = stable near singularities but slower and biased (the step no longer solves the exact least-squares problem); small $\lambda$ = accurate away from singularities but explosive near them. It is ridge regression, and $\lambda$ is the ridge.

### Problem set · 과제

Tier B. Tip target $(1,1)$ on **P2** from [[02-foundations/lab-plants|0.6]]. Analytic only — no Newton loop.

1. **Draw.** Both IK branches that put the tip at $(1,1)$. Label the two elbow points.
2. **Derive.** The two joint pairs. Which is the frozen pose of 0.6? Average the two joint vectors; where does that mean configuration put the tip?
3. **Interpret.** A numerical IK seeded at $(45^\circ,0^\circ)$ cannot jump branches without crossing $\theta_2=0$. What does that mean for moving the tool to the panel?

> [!note]- How to draw it · 그리는 법
> - Draw the target once, as a small circle, and let every arm end on it or point at it.
> - Each branch is two links: link 1 from the base to its elbow, link 2 from the elbow to the target. Draw one branch solid and the other lighter.
> - Label both elbow points. The two elbows are the whole content of "elbow-up versus elbow-down": same tip, two different arms.
> - If you add the mean of the two joint vectors, draw it dashed from its own joint angles (in the picture above, $(45^\circ, 0^\circ)$, one straight segment), put an $\times$ on its tip, and mark the miss back to the target. It must land visibly past the target, not near it.
> - At the dashed tip, "reachable" is a double-headed arrow perpendicular to the straight arm and "wanted" points back along it toward the target. Draw them at right angles: every tip velocity the straight arm can produce lies on the first, and the whole error on the second.

> [!tip]- Solutions
> 1. Elbow-right: elbow at $(1,0)$, forearm up. Elbow-up: elbow at $(0,1)$, forearm to the right.
> 2. $(0^\circ,90^\circ)$ and $(90^\circ,-90^\circ)$. Frozen pose is $(0^\circ,90^\circ)$. Mean $(45^\circ,0^\circ)$: tip $(\sqrt2,\sqrt2)\approx(1.41,1.41)$ — not a solution. The mean of two IKs is not an IK (the figure in §1).
> 3. $\det J=L_1L_2\sin\theta_2$ vanishes on the straight arm between branches, and $(45^\circ,0^\circ)$ lies on it: seeded exactly there the solver does not move at all (Worked case, Step 4), and once nudged off it a local solver stays on that side; switching elbows loses the panel-normal velocity at the singularity.

## 한국어

**핵심 질문**: 원하는 말단 자세가 주어지면 어떤 관절 각이 그것을 달성하는가?

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

**2단계 — 어깨 각, 분기마다 하나씩.** $\theta_2$를 고르면 팔이 강체 삼각형이 되고, 베이스에서 본 말단의 방위각이 두 조각으로 갈라진다. 목표가 놓인 방향에서, 접힌 전완이 말단을 링크 1 자신의 방향에서 얼마나 밀어냈는지를 뺀 것이다:

$$\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2)$$

둘째 항은 $\theta_2$와 함께 부호가 뒤집히므로, 엘보 선택 둘이 어깨 각 하나가 아니라 둘을 준다. $\theta_2 = +90^\circ$: $\operatorname{atan2}(1,1) - \operatorname{atan2}(1, 1) = 45^\circ - 45^\circ = 0^\circ$이므로 $\theta = (0^\circ, 90^\circ)$. $\theta_2 = -90^\circ$: $45^\circ - \operatorname{atan2}(-1, 1) = 45^\circ - (-45^\circ) = 90^\circ$이므로 $\theta = (90^\circ, -90^\circ)$. 둘 다 FK로 검산된다. $(\cos 0^\circ + \cos 90^\circ,\ \sin 0^\circ + \sin 90^\circ) = (1,1)$이고 $(\cos 90^\circ + \cos 0^\circ,\ \sin 90^\circ + \sin 0^\circ) = (1,1)$이다. 앞의 것이 카탈로그 고정 자세인데, 이 페이지가 그렇게 고른 것이 아니라 카탈로그가 고른 것이다.

**3단계 — 평균이 왜 해가 아닌지, 숫자로.** 성분별 평균은 $(45^\circ, 0^\circ)$, 곧게 편 팔이고 말단은 $(\sqrt2, \sqrt2)$다. 빗나간 거리는 $\sqrt{2(\sqrt2 - 1)^2} = 0.5858\,\mathrm{m}$인데, 베이스에서 $1.414\,\mathrm{m}$ 떨어진 목표에 대해 $41\,\%$를 지나친 것이지 반올림 오차가 아니다. IK 해의 집합은 볼록하지 않고, 평균은 정확히 그것이 볼록하다고 가정하는 연산이다.

**4단계 — 그 평균 자세를 수치 해법에 주고 아무 일도 안 일어나는 것을 본다.** $\theta^{(0)} = (45^\circ, 0^\circ)$에서 뉴턴 IK를 시작한다. $s_1 = c_1 = s_{12} = c_{12} = 0.7071$이므로 5장 공식이

$$J = \begin{pmatrix}-1.4142 & -0.7071\\ 1.4142 & 0.7071\end{pmatrix}, \qquad \det J = L_1L_2\sin\theta_2 = 0, \qquad \sigma = (2.2361,\ 0)$$

을 준다. 랭크가 1이고, 도달 가능한 단 하나의 방향은 팔에 수직인 $(-0.7071, 0.7071)$이다. 오차는 $e = (1,1) - (\sqrt2,\sqrt2) = (-0.4142, -0.4142)$로 팔을 *따라* 곧장 되돌아가는 방향이다. 그러면

$$J^\top e = \begin{pmatrix}-1.4142 & 1.4142\\ -0.7071 & 0.7071\end{pmatrix}\begin{pmatrix}-0.4142\\ -0.4142\end{pmatrix} = \begin{pmatrix}0.5858 - 0.5858\\ 0.2929 - 0.2929\end{pmatrix} = \begin{pmatrix}0\\0\end{pmatrix}$$

이고, $J^\top$ 위에 세운 모든 갱신이 이 0을 물려받는다. 유사역행렬 스텝이 $0$이고, 감쇠 스텝 $J^\top(JJ^\top + \lambda^2 I)^{-1}e$도 **모든** $\lambda$에 대해 $0$이다. 감쇠는 이미 0인 벡터에 곱해지는 것만 바꾸기 때문이다. 해법은 정확한 해가 둘이나 있는 목표에서 $58.6\,\mathrm{cm}$ 떨어진 채 "진전 없음"으로 멈춘다. 여기서 감쇠는 잘못된 처방이고, 유일한 처방은 다른 초기값이다.

**5단계 — 특이점에서 조금 떨어지면 실패의 종류가 바뀐다.** 초기값을 $(45^\circ, 10^\circ)$로 옮겨 팔이 *거의* 곧게 편 상태만 되게 하자. 이제 $\det J = \sin 10^\circ = 0.1736$, $\sigma = (2.2279,\ 0.0779)$다. 스텝 크기를 정하는 것은 $\|e\| = 0.5964$를 그 가장 작은 특이값으로 나눈 값이고, 감쇠 없는 갱신은 관절이 $\|\Delta\theta\| = 7.51\,\mathrm{rad}$만큼 움직이는 것이다. 말단은 $(-1.32, -1.39)$로 내던져지고 $\|e\|$는 $0.596$에서 $3.33$으로 커진다. $\lambda = 0.3$의 감쇠는 대신 $(30.3^\circ, 33.1^\circ)$로 가서 $\|e\|$를 $0.506$까지 내린다. 정확한 최소제곱 스텝보다 작고, 방향은 옳다. **정확히 특이점이면 스텝이 없고, 거의 특이점이면 스텝이 날뛴다.** $\|e\|$ 그래프에서는 비슷해 보이지만 처방이 정반대다.

### 1. IK는 구조적으로 FK보다 어렵다

FK와 달리 IK의 해는 **0개, 1개, 여러 개, 무한히 많을 수** 있다(팔꿈치 위/아래; 7자유도
팔은 연속체). 이 다봉성은
[[01-canonical-papers/notes/4-vla/diffusion-policy|생성형 정책]]이 대안 행동을 표현하는 이유에 대한 비유다. 서로 다른 유효 해를 평균하면 무효 해가 될 수 있다. 특정 학습 정책의 성능 우위를 증명하는 것은 아니다. **해석적 IK**(닫힌 형태, 예: 구면
손목의 6R)는 모든 가지를 정확히 열거한다; 기하가 허락하지 않으면 수치로 간다.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="같은 목표에 도달하는 두 관절 해와, 그 평균이 목표를 지나쳐 버리는 것">
  <g stroke="currentColor" stroke-width="1" opacity="0.25">
    <line x1="40" y1="190" x2="250" y2="190"/><line x1="60" y1="200" x2="60" y2="30"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.85">
    <polyline points="60,190 160,190 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.45">
    <polyline points="60,190 60,90 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.7">
    <polyline points="60,190 131,119 201,49"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="4.5"/>
    <circle cx="160" cy="190" r="3.5" opacity="0.85"/>
    <circle cx="60" cy="90" r="3.5" opacity="0.45"/>
    <circle cx="131" cy="119" r="3" opacity="0.7"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.8">
    <circle cx="160" cy="90" r="6"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.7">
    <line x1="196" y1="44" x2="206" y2="54"/>
    <line x1="196" y1="54" x2="206" y2="44"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="176" y="196">해 1 &#183; (0&#176;, +90&#176;)</text>
    <text x="24" y="78" opacity="0.85">해 2 &#183; (90&#176;, &#8722;90&#176;)</text>
    <text x="214" y="46" opacity="0.85">(1.41, 1.41)에 도착</text>
    <text x="176" y="94">목표 (1, 1)</text>
    <text x="286" y="140" opacity="0.85">두 해의 평균 &#183; (45&#176;, 0&#176;)</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5" fill="none">
    <line x1="283" y1="136" x2="140" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">관절 각 두 쌍이 끝점을 같은 목표에 놓는다 &#8212; &#8220;해가 여러 개&#8221;라는 말의 뜻이 이것이다.</text>
    <text x="24" y="226">평균을 내면 팔이 펴져 (1.41, 1.41)에 가고 0.59만큼 빗나간다. 유효한 두 답의 평균은</text>
    <text x="24" y="240">답이 아니다. 다봉적 행동 예측에 대안을 담을 수 있는 표현이 필요한 이유의</text>
    <text x="24" y="254">고전적 그림이 바로 이것이다.</text>
  </g>
</svg>

**그 두 해가 끝점 $(1,1)$의 장치 P2다.** 단위 링크: $(0^\circ,90^\circ)$의 엘보는 $(1,0)$에 있고 전완은 $+y$; $(90^\circ,-90^\circ)$의 엘보는 $(0,1)$에 있고 전완은 $+x$. 끝점은 둘 다 $(1,1)$. 카탈로그 고정 자세([[02-foundations/lab-plants|0.6]])는 전자다. 그림의 점선 평균은 $(45^\circ,0^\circ)$, 곧은 팔의 끝점 $(\sqrt{2},\sqrt{2})$ — 해가 아니다. 과제는 두 분기를 그리고 그것을 말하라고 한다. 그림이 이미 기하를 했다.

**목표 자세는 아직 운동 계획이 아니다.** 팔꿈치가 위·아래인 해는 말단 자세가 같아도 팔 구성은 크게 다를 수 있다. 관절 한계나 장애물 때문에 한 분기만 불가능할 수 있다. 목표 구성을 반환하는 해법과 그곳까지 충돌 없는 경로를 찾는 계획기는 다른 질문에 답한다.

수치 해법은 대개 초기 추정 근처의 분기를 따라간다. 성공하지 못하면 도달 불가, 나쁜 초기값, 특이한 국소 사상, 한계 위반, 반복 예산 소진을 나눈다. 국소 탐색 한 번의 실패가 로봇에 해가 없다는 증거는 아니다.

**이해 확인.** 가까운 목표를 연속으로 풀 때 이전 해는 연속성을 유도하는 좋은 초기값일 수 있다. 특이점이나 가능 분기 변경을 지나도 연속성을 보장하지는 않는다. 다중모드 학습 행동과의 비유는 대안을 표현하는 문제다. 모든 생성 정책이 회귀보다 낫다는 정리가 아니다.

### 2. 수치 IK = 자세 오차에 대한 뉴턴-랩슨

반복:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(작업 공간 오차)}$$
완전한 SE(3)의 경우 $e$는 바디 좌표의 6차원 오차 $[\log(T_{now}^{-1} T_{goal})]^\vee$이며 바디 자코비안과 짝지어 쓴다
([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장]]의 로그 사상; "vee" $^\vee$는 3장의 대괄호 연산을 되돌려 $4\times4$ 행렬에서 여섯 개의 수를 다시 꺼낸다)이고,
$J^\dagger$는 유사역행렬([[02-foundations/linear-algebra|최소제곱]])이다.

**반복 한 번을 따라간다.** 현재 자세를 계산하고 목표 오차를 정한 프레임으로 표현한다. 현재 관절에서 그 프레임의 야코비안을 구한다. 국소 관계 JΔθ ≈ e를 풀고 관절 추정을 갱신한 뒤 자세와 오차를 다시 계산한다. 야코비안이 국소 변화만 설명하므로 반복이 필요하다. 감쇠나 보폭 규칙은 근사를 너무 멀리 믿지 않게 한다.

위 바디 프레임 자세 오차에서 행렬 로그의 결과는 먼저 리 대수의 행렬이다. 그 여섯 좌표를 오차 벡터로 뽑아 바디 야코비안과 짝짓는다. 라디안과 길이는 단위가 달라 회전·병진 정지 허용오차를 따로 쓴다. 수치 수렴과 별개로 관절 한계와 충돌도 검사한다.

**이해 확인.** 유사역행렬은 국소 선형 잔차를 최소화하고 대안이 남으면 최소 노름 갱신을 고른다. 전체 비선형 자세 문제를 곧바로 푸는 것은 아니다. 국소 근사와 갱신 루프는 [공식 수치 IK 설명](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)에서도 따라갈 수 있다.

### 3. 한 반복을 손으로 끝까지 — 평면 2R 팔

$L_1 = L_2 = 1$; 목표 끝점 $(-1, 1)$ (참값: $\theta^* = (90°, 90°)$ —
[[04-robotics/modern-robotics/ch04-forward-kinematics|4장]] 예제에서). 초기값
$\theta^{(0)} = (45°, 90°)$에서 시작.

- **FK**: 끝점 $= (0.707 - 0.707,\; 0.707 + 0.707) = (0,\, 1.414)$.
- **오차**: $e = (-1, 1) - (0, 1.414) = (-1, -0.414)$; $\|e\| = 1.08$.
- **야코비안** (5장 공식, $s_1 = c_1 = 0.707$, $s_{12} = 0.707$, $c_{12} = -0.707$):
  $$J = \begin{pmatrix} -1.414 & -0.707 \\ 0 & -0.707 \end{pmatrix}, \quad \det J = 1.0$$
- **갱신**: $\Delta\theta = J^{-1} e = (0.41,\; 0.59)$ rad $= (23.7°,\; 33.6°)$, 따라서
  $\theta^{(1)} = (68.7°,\; 123.6°)$.
- **확인**: $\theta^{(1)}$에서 FK 끝점 $\approx (-0.61,\, 0.72)$;
  $\|e\| = 0.48$ — **한 스텝에 오차가 절반**이 됐고, 반복점은 $(90°, 90°)$ 쪽으로
  움직이고 있다. 몇 번 더 반복하면 수렴한다; 반복 대비 $\|e\|$ 그래프가 모든 IK 구현의
  표준 검산이다.

### 4. 실전의 두 가지 복잡성

- **특이점**: 근처에서 $J^\dagger$가 폭발한다. 쉬운 말로 된 해법: $\lambda^2 I$를 더해
  $J$가 랭크를 잃어도 역행렬을 구할 행렬이 계속 가역이 되게 하고, 거대한 스텝 대신 약간
  틀리지만 크기가 유한한 스텝을 받아들인다. 그것이 **감쇠 최소제곱**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$이며, 정확도를 안정성과 맞바꾼다 — 변장한 릿지 회귀.
  그리고 정확히 이 잔차에 대한 **Levenberg–Marquardt** 스텝이기도 하다. 항등식
  $J^\top(JJ^\top + \lambda I)^{-1} = (J^\top J + \lambda I)^{-1}J^\top$가 두 식을 같게
  만들므로 $\lambda$는 신뢰 파라미터이고, 감쇠 IK는 SLAM과 보정이 돌리는 바로 그 알고리즘이다
  ([[02-foundations/optimization|4. 최적화 §3.5]]).

  출처를 분명히 해 두자. **MR 자체는
  damped least squares를 다루지 않는다.** 6장은 특이점에서 그냥 유사역행렬을 주고, 감쇠와
  여유자유도 계열은 참고문헌으로 넘긴다. 여기 쓴 $\lambda^2$ 표기는 그 바깥 문헌의 관례이고,
  $\lambda$가 단위를 갖게 하려는 것이다. 최적화 페이지는 $\lambda$로 쓴다. 6장에서 이
  표기를 찾지 마라. 2링크 팔을 처음부터 끝까지 코드로 옮긴 것 — 두 팔꿈치 해를 모두 주는
  해석적 IK와 감쇠 스텝 한 번 — 은 [[02-foundations/algorithms/robotics-ai-problems|11.8 §6]]에 있다.
- **여유자유도** ($n > 6$): $J$의 영공간([[02-foundations/linear-algebra|§2의 영공간]]을 이번엔 $J$에 적용한 것: $J\dot\theta = 0$인 관절 속도들)은 도구를 움직이지 않고 관절만 움직인다 — 이를
  2차 목표(관절 한계, 장애물, 특이점 회피)에 쓴다.

**위키 연결**: 말단 공간 원격조작 스택과 말단 공간 VLA가([[01-canonical-papers/notes/4-vla/act|ALOHA]] 같은 관절 공간 장비는 건너뛴다) 정책 출력과 모터 명령 사이에서 IK(또는 그 속도 수준 사촌)를 돌린다.

### 스스로 점검

1. 위의 목표 $(-1,1)$에 대해 $(90°, 90°)$ 말고 *다른* 해석해는 무엇인가?
2. 뉴턴 IK에 *좋은 초기값*이 필요한 이유는, 그리고 제어 루프에서는 보통 무엇이 그것을
   제공하는가?
3. $\theta_2 = 0$에서 정확히 시작해 IK를 돌리면 무엇이 잘못되는가?
4. 감쇠 최소제곱 갱신식을 쓰고, $\lambda$가 무엇을 맞바꾸는지 말하라.

> [!tip]- 정답 · Answers
> 1. elbow-down 가지인 $(180°, -90°)$. 확인: 링크 1이 $-\hat x$ 방향으로 $(-1,0)$까지 가고, 링크 2가 $-90°$ 돌아 $+\hat y$를 향하므로 끝점은 $(-1,1)$이다. ✓ 관절 컨피규레이션 둘에 과제 pose 하나 — 한 예제 안에 담긴 IK의 다봉성이다.
> 2. 뉴턴법은 국소적으로만 수렴한다. 해에서 멀면 선형화 $J$가 나쁜 모델이어서 스텝이 발산하거나 다른 가지에 떨어질 수 있다. 제어 루프에서는 목표가 연속적으로 움직이므로 직전 시점의 해가 자연스러운 초기값이고, 덕분에 팔이 운동 도중 elbow 컨피규레이션을 뒤집지 않고 한 가지에 머문다.
> 3. $\theta_2 = 0$은 특이점이다: $\det J = L_1L_2\sin\theta_2 = 0$이므로 $J^{-1}$가 존재하지 않는다. 유사역행렬은 그래도 스텝을 하나 돌려주지만 잃어버린 방향의 오차는 전혀 줄이지 못한다. 반복은 정체하거나, 감쇠가 없으면 수치적으로 폭주한다.
> 4. $\Delta\theta = J^\top(JJ^\top + \lambda^2 I)^{-1}e$. 큰 $\lambda$는 특이점 근처에서 안정하지만 느리고 편향된다. 여기서 편향이란 스텝이 더 이상 정확한 최소제곱 문제를 풀지 않는다는 뜻이다. 작은 $\lambda$는 특이점에서 멀 때 정확하지만 가까이서는 폭주한다. 이것은 능형회귀이고 $\lambda$가 그 능선이다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**, 말단 목표 $(1,1)$. 해석해만 — 뉴턴 루프 없음.

1. **그리기.** 말단을 $(1,1)$에 두는 IK 가지 둘. 엘보 두 점을 표시.
2. **유도.** 관절 각 두 쌍. 0.6의 고정 자세는 어느 쪽인가? 두 관절 벡터의 평균은 말단을 어디에 두는가?
3. **해석.** $(45^\circ,0^\circ)$에서 시작한 수치 IK는 $\theta_2=0$을 건너지 않고는 가지를 못 바꾼다. 도구를 패널로 옮길 때 뜻은?

> [!note]- 그리는 법 · How to draw it
> - 목표는 작은 원 하나로 한 번만 그리고, 모든 팔이 거기서 끝나거나 그것을 가리키게 둔다.
> - 가지마다 링크 둘이다. 링크 1은 베이스에서 그 엘보까지, 링크 2는 엘보에서 목표까지. 한 가지는 실선, 다른 가지는 더 얇게 그린다.
> - 엘보 두 점에 이름을 붙인다. 두 엘보가 "팔꿈치 위/아래"의 내용 전부다. 말단은 같고 팔이 둘이다.
> - 두 관절 벡터의 평균을 더한다면 그 자신의 관절 각으로 점선을 그리고(위의 그림에서는 $(45^\circ, 0^\circ)$, 곧은 선분 하나), 말단에 $\times$를 친 뒤 목표까지 되돌아오는 빗나감을 표시한다. 목표 근처가 아니라 눈에 띄게 지나쳐 있어야 한다.
> - 점선 말단에서 "도달 가능"은 곧은 팔에 수직인 양방향 화살표, "원하는 방향"은 팔을 따라 목표 쪽으로 되돌아가는 화살표다. 둘을 직각으로 그린다. 곧은 팔이 만들 수 있는 말단 속도는 전부 앞쪽에 있고, 오차는 전부 뒤쪽에 있다.

> [!tip]- 정답 · Solutions
> 1. 엘보-오른쪽: 엘보 $(1,0)$, 전완 위. 엘보-위: 엘보 $(0,1)$, 전완 오른쪽.
> 2. $(0^\circ,90^\circ)$와 $(90^\circ,-90^\circ)$. 고정 자세는 $(0^\circ,90^\circ)$. 평균 $(45^\circ,0^\circ)$: 말단 $(\sqrt2,\sqrt2)\approx(1.41,1.41)$ — 해가 아니다. 두 IK의 평균은 IK가 아니다(§1 그림).
> 3. 가지 사이의 직선 팔에서 $\det J=0$이고, $(45^\circ,0^\circ)$는 바로 그 위에 있다. 정확히 거기서 시작하면 해법은 전혀 움직이지 않고(위 계산의 4단계), 거기서 조금 벗어난 뒤에는 국소 해법이 그쪽에 남는다. 엘보를 바꾸면 특이점에서 패널 법선 속도를 잃는다.
