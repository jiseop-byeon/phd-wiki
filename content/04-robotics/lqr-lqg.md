---
title: "6. LQR / LQG"
tags: [robotics, control]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Study links** — [Underactuated Robotics, LQR chapter (Tedrake, MIT)](https://underactuated.csail.mit.edu/lqr.html) · [Stanford EE363 lecture slides](https://web.stanford.edu/class/ee363/)

## English

*Group D. Stands on [[04-robotics/control-theory-ce397|5. Control Theory]] plus probability and optimization. Instead of placing poles by hand you
let a cost place them, and the separation principle says when estimator and controller may be designed apart.*

> [!info] Depth target · 깊이 목표
> State the LQR problem, the role of the Riccati equation, the conditions under which the solution exists and stabilizes, and LQG's estimator–controller separation with its caveat. Deriving or implementing Riccati solvers is optional.
> LQR 문제, 리카티 방정식의 역할, 해가 존재하고 안정화하는 조건, LQG의 추정기–제어기 분리와 그 단서를 말할 수 있으면 된다. 리카티 해법의 유도·구현은 선택이다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/control-theory-ce397|5. Control Theory]] (state space, eigenvalue stability, controllability/observability, pole placement — this page is *"choose $K$ by optimization instead of by hand"*) · [[02-foundations/optimization|4. Optimization]] (quadratic objectives) · [[02-foundations/probability|3. Probability]] (the Kalman filter, for the LQG half)
> [[04-robotics/control-theory-ce397|5. 제어 이론]] (상태공간, 고유값 안정성, 가제어성/가관측성, 극점 배치 — 이 페이지는 *"$K$를 손이 아니라 최적화로 고르기"*다) · [[02-foundations/optimization|4. 최적화]] (이차 목적함수) · [[02-foundations/probability|3. 확률]] (LQG 절반을 위한 칼만 필터)

**What it is**: the **Linear Quadratic Regulator** is the exactly-solvable heart of optimal
control. For linear dynamics $\dot x = Ax + Bu$ and quadratic cost
$\int (x^\top Q x + u^\top R u)\,dt$ with $Q \succeq 0$ and $R \succ 0$ (so $R^{-1}$ exists), the optimal controller is a constant linear feedback
$u = -Kx$, with $K = R^{-1}B^\top P$ where $P$ solves the **algebraic Riccati equation** —
no iteration at runtime.
Written out, the infinite-horizon LQR problem is

$$\min_{u(\cdot)}\; J = \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt \quad \text{subject to} \quad \dot x = Ax + Bu,\;\; x(0) = x_0$$

with four named ingredients: the linear model $(A, B)$; the **state weight** $Q$, positive
semidefinite ($x^\top Q x \ge 0$ for every $x$), which prices deviation from the origin; the
**input weight** $R$, positive definite ($u^\top R u > 0$ for every $u \ne 0$), which prices
effort and must be strictly positive so that no input is free; and the infinite horizon, which is
why the optimal gain is constant rather than time-varying. (Definiteness is defined in
[[02-foundations/linear-algebra|1. Linear Algebra §3]].) Tracking a reference is the same problem
written in error coordinates $x - x_{ref}$.
**LQG** adds Gaussian noise and partial observation: the optimal solution is a
[[02-foundations/probability|Kalman filter]] feeding an LQR (the **separation principle**:
estimate optimally, then control the estimate optimally, and it is jointly optimal).

> [!note] First pass · 처음이라면
> A short page; read it through. If you only have ten minutes, §2 is the one that changes how you read papers — "LQR guarantees stability" has two conditions attached, and papers linearising a nonlinear system inherit them only at the linearisation point.

### Homework diagram · 과제가 그릴 그림

Draw it once here; the problem set asks for the same figure with one weight changed. The object is
**P4** from [[02-foundations/lab-plants|0.6 Lab Plants]], the leaky heater $\dot x=-x+u+d$ of
[[04-robotics/control-theory-ce397|5. Control Theory §1]] — the same machine, with the gain now
chosen by a cost instead of by hand.

<svg viewBox="0 0 560 376" style="max-width:100%;height:auto" role="img" aria-label="Top: the leaky heater's feedback loop with the disturbance entering at the summing junction, and a dashed ledger that prices x with Q and u with R into J. Bottom: the real axis with the open-loop pole at -1 and the closed-loop poles at -1.414 for Q = 1 and -2.236 for Q = 4.">
  <defs><marker id="aLQR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <circle cx="96" cy="80" r="11"/>
    <rect x="160" y="60" width="160" height="40" rx="3"/>
    <rect x="238" y="138" width="60" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aLQR)">
    <line x1="96" y1="26" x2="96" y2="68"/>
    <line x1="107" y1="80" x2="158" y2="80"/>
    <line x1="320" y1="80" x2="424" y2="80"/>
    <polyline points="380,80 380,152 300,152"/>
    <polyline points="238,152 96,152 96,92"/>
  </g>
  <circle cx="380" cy="80" r="3" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-dasharray="4 3" stroke-opacity="0.75">
    <polyline points="424,80 452,80"/>
    <polyline points="472,94 472,204"/>
    <polyline points="140,152 140,204"/>
    <polyline points="160,218 300,218"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.75">
    <rect x="452" y="66" width="40" height="28" rx="3"/>
    <rect x="120" y="204" width="40" height="28" rx="3"/>
    <rect x="300" y="204" width="240" height="28" rx="3"/>
  </g>
  <circle cx="140" cy="152" r="2.6" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="50" y1="306.0" x2="519.5" y2="306.0"/>
    <line x1="470" y1="301.0" x2="470" y2="311.0"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.45">
    <line x1="170" y1="303.0" x2="170" y2="309.0"/>
    <line x1="320" y1="303.0" x2="320" y2="309.0"/>
  </g>
  <g stroke="currentColor" fill="none">
    <path d="M314.5 300.5 L325.5 311.5 M314.5 311.5 L325.5 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M252.4 300.5 L263.4 311.5 M252.4 311.5 L263.4 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M129.1 300.5 L140.1 311.5 M129.1 311.5 L140.1 300.5" stroke-width="2.4" stroke-opacity="1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aLQR)">
    <line x1="320" y1="290.0" x2="138.6" y2="290.0"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="96" y="84">Σ</text>
    <text x="240" y="85">ẋ = −x + u + d</text>
    <text x="268" y="157">−K</text>
    <text x="472" y="85">Q</text>
    <text x="140" y="223">R</text>
    <text x="420" y="223">J = ∫<tspan font-size="9.5" dy="4">0</tspan><tspan font-size="9.5" dy="-10">∞</tspan><tspan dy="6"> (Qx² + Ru²) dt</tspan></text>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="104" y="38">d</text>
    <text x="360" y="73">x</text>
    <text x="182" y="146">u</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="240" y="52" text-anchor="middle" opacity="0.85">P4, the leaky heater</text>
    <text x="268" y="184" text-anchor="middle">(Q, R) → P → K: offline, once</text>
    <text x="268" y="198" text-anchor="middle" opacity="0.85">Q = 4, R = 1 gives P = K = 1.236</text>
    <text x="540" y="250" text-anchor="end" opacity="0.8">ledger: an accounting path, it never touches the plant</text>
    <text x="227.3" y="283.0" text-anchor="middle">raise Q/R: the closed-loop pole slides left</text>
    <text x="328" y="326.0">−1</text>
    <text x="328" y="340.0" opacity="0.85">open loop</text>
    <text x="257.9" y="326.0" text-anchor="middle" opacity="0.85">−√2 = −1.414</text>
    <text x="257.9" y="340.0" text-anchor="middle" opacity="0.85">Q = 1, problem set</text>
    <text x="134.6" y="326.0" text-anchor="middle">−√5 = −2.236</text>
    <text x="134.6" y="340.0" text-anchor="middle">Q = 4, worked in §1</text>
    <text x="470" y="326.0" text-anchor="middle">0</text>
    <text x="523.5" y="310.0">Re s</text>
    <text x="12" y="363" opacity="0.9">closed-loop pole −(1 + K) = −√(1 + Q) at R = 1; nothing else in the figure moves</text>
  </g>
</svg>

**The loop.** A summing junction; the plant box $\dot x=-x+u+d$ after it; the disturbance $d$
entering at that junction beside $u$; the state $x$ leaving the box; and a feedback path from $x$
through a gain block $-K$ back into the junction. That much is the control page's picture, and
nothing on it has changed.

**The ledger, which is what LQR adds.** Tap both signals and draw where their prices are paid: a
branch from $x$ into a box $Q$, a branch from $u$ into a box $R$, and both into an accumulator
labelled $J=\int_0^\infty (Qx^2+Ru^2)\,dt$. Draw this branch with a different line weight, because
it never touches the plant — it is an accounting path, not a control path, and keeping it visually
separate is how $Q$ and $R$ stay distinct from the noise covariances $W$ and $V$ that enter the
same loop in §4. Beside the $-K$ block write the single arrow the Riccati equation is,
$(Q,R)\rightarrow P\rightarrow K$, and label it *offline, once*.

**The pole axis.** Under the loop draw a real axis. Mark the open-loop pole at $-1$, where the
uncontrolled heater already sits, and the closed-loop pole at $-(1+K)$. On this plant the
stabilizing Riccati solution at $R=1$ is $P=K=-1+\sqrt{1+Q}$, so the closed-loop pole lands at
exactly $-\sqrt{1+Q}$: mark $-\sqrt5=-2.236$ for the $Q=4$ case worked in §1, and
$-\sqrt2=-1.414$ for the problem set's $Q=1$. The arrow worth drawing is the one that matters
when reading a paper — raising $Q/R$ slides that pole left, and nothing else in the figure moves.

### 1. The Riccati equation, read structurally

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

This is the **algebraic Riccati equation (ARE)**: a matrix equation, quadratic in the unknown
symmetric $n \times n$ matrix $P$, whose data are the model $A, B$ and the weights $Q, R$. $P$ is
the matrix of the optimal **cost-to-go** (value function), the least cost achievable from a
given starting state:

$$V(x_0) = \min_{u(\cdot)} \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt = x_0^\top P x_0$$

so $P$ answers "how expensive is it to be at $x_0$" for every $x_0$ at once.

**Where it comes from, in four steps.** Guess that the optimal cost-to-go is quadratic,
$V(x) = x^\top P x$ — a guess justified afterwards by the fact that it closes. Substitute it
into the optimality condition (the continuous-time Bellman equation, or HJB — the Bellman equation is introduced in discrete time in [[02-foundations/rl-basics|7. RL Basics §2]]), which says the
instantaneous cost plus the rate of change of the cost-to-go is zero at the optimum:
$0 = \min_u\,[\,x^\top Q x + u^\top R u + \nabla V^\top(Ax + Bu)\,]$, with $\nabla V = 2Px$.
Third, minimise over $u$ — now an ordinary quadratic: setting the derivative to zero gives
$2Ru + 2B^\top P x = 0$, so $u^\star = -R^{-1}B^\top P x$. **That is where the LQR gain
$K = R^{-1}B^\top P$ comes from; it falls out rather than being designed.** Fourth, put
$u^\star$ back in. Every term carries an $x$ on each side, and what is left between them is
exactly the equation above.

Reading it that way makes the strange middle term ordinary. $-PBR^{-1}B^\top P$ is not an
extra modelling choice — it is the optimal feedback substituted back into the cost, which is
why it is quadratic in $P$ and why it is subtracted: it is the cost the controller *avoids*
by acting.

**Worked, scalar.** Take the unstable $\dot x = x + u$ ($A = B = 1$) with $Q = R = 1$. The ARE
becomes $2P - P^2 + 1 = 0$, which has **two** roots, $P = 1 + \sqrt2 = 2.414$ and
$P = 1 - \sqrt2 = -0.414$. The **stabilizing solution** is the one whose gain makes $A - BK$
stable: $P = 2.414$ gives $K = 2.414$ and the closed loop $\dot x = -1.414\,x$, while
$P = -0.414$ gives $\dot x = +1.414\,x$. A Riccati equation generally has several solutions, and
"the" solution in any paper means the stabilizing one. Check the cost-to-go: from $x_0 = 1$ the
closed loop gives $x = e^{-1.414t}$ and $u = -2.414\,x$, so
$J = \int_0^\infty (1 + 2.414^2)\,e^{-2.828t}\,dt = 2.414 = P$.

**Worked: plant P4, already stable.** The leaky heater $\dot x=-x+u$ has $A=-1$, $B=1$ ([[02-foundations/lab-plants|0.6]]). With $Q=4$, $R=1$ the ARE is $-2P-P^2+4=0$, so $P=-1+\sqrt5\approx 1.236$ (the positive root). Then $K=P\approx 1.236$, the closed-loop pole is $-(1+K)\approx-2.24$, and a constant $d=1$ sits at $x_\mathrm{ss}=d/(1+K)\approx 0.45$. Compare a CE397-style hand gain $K=4$: pole $-5$, $x_\mathrm{ss}=0.2$. $Q=4$ already prices state more than effort, so LQR acts, but not as hard as the hand gain that bought $5\times$ rejection. The problem set repeats the ARE at $Q=R=1$, where the optimizer barely acts ($K\approx 0.414$) because the plant is already stable and state and effort are priced equally. Raising $Q/R$ is the $(1+K)$ trade of CE397 §1: smaller $x_\mathrm{ss}$, more effort and noise.

(Robotics papers usually use the **discrete-time twin** — the DARE, with gain $K=(R+B^\top P B)^{-1}B^\top P A$ — same structure, same reading.) For $x_{k+1} = Ax_k + Bu_k$ and cost $\sum_k (x_k^\top Q x_k + u_k^\top R u_k)$ it reads

$$P = A^\top P A - A^\top P B\,(R + B^\top P B)^{-1} B^\top P A + Q$$

so each step's cost-to-go is the stage cost plus the next step's cost-to-go under the best input.
For $x_{k+1} = x_k + u_k$ with $Q = R = 1$ it reduces to $P^2 - P - 1 = 0$, so $P = 1.618$,
$K = P/(1+P) = 0.618$, and the closed loop $x_{k+1} = 0.382\,x_k$ is inside the unit circle
([[04-robotics/mpc|7. MPC]] reuses these numbers). You never solve this by hand — but reading it structurally pays: $Q$ injects state cost,
the quadratic $-PBR^{-1}B^\top P$ term is *feedback eating cost through control*, and the
stabilizing solution $P$ — positive definite when $(A,Q^{1/2})$ is observable — is what makes $V(x)=x^\top P x$ a Lyapunov function for
the closed loop. (A **Lyapunov function** is a scalar "energy" of the state that is positive everywhere except at $x=0$ and decreases along every closed-loop trajectory; if one exists, the state has nowhere to go but $0$, so its existence proves stability; the three conditions and a worked example are in [[04-robotics/control-theory-ce397|5. Control Theory §4]]. Here the HJB condition gives $\dot V = -(x^\top Q x + u^{\star\top} R u^\star)$, minus the running cost.) Under detectability alone $P \succeq 0$, and the argument needs a LaSalle-type step — LaSalle's invariance principle, which still proves convergence when $\dot V$ is only $\le 0$, provided no trajectory can stay forever where $\dot V = 0$ except at the origin. When a paper says "we solve a Riccati equation," it means this constant
$P$, computed once offline (or once per linearization in iterative/time-varying LQR).

### 2. When does this actually work? Two conditions

- **Stabilizability** of $(A,B)$: every mode of $A$ with $\text{Re}\,\lambda \ge 0$ — including the double integrator's modes at $\lambda = 0$ — must be influenceable by $u$ —
  the exact (necessary and sufficient) condition for a stabilizing feedback to exist,
  weaker than the full controllability rank test in
  [[02-foundations/linear-algebra|page 1's control section]]. Otherwise no feedback can
  stabilize, Riccati or not.
  Stated as a definition, $(A,B)$ is **stabilizable** when some gain $K$ makes every eigenvalue of
  $A - BK$ have negative real part. It is checked mode by mode with the PBH
  (Popov–Belevitch–Hautus) rank test,
  $$\text{rank}\,[\,A - \lambda I \;\; B\,] = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  because the rank drops below $n$ exactly at an eigenvalue whose mode the input cannot touch;
  demanding full rank at *every* eigenvalue is controllability itself. (In discrete time the
  unstable modes are those with $|\lambda| \ge 1$.) *Example:* the uncontrollable pair of
  [[04-robotics/control-theory-ce397|5. Control Theory §6]], $A = \text{diag}(-1,-2)$ with
  $B = (1, 0)^\top$, loses rank only at $\lambda = -2$, a mode that decays by itself, so it is
  stabilizable. *Non-example:* $A = \text{diag}(1, 2)$ with the same $B$ loses rank at
  $\lambda = 2$, an unstable mode, so no $K$ exists.
- **Detectability** of $(A,Q^{1/2})$: every mode with $\text{Re}\,\lambda \ge 0$ must show up in the cost —
  otherwise the optimizer can "not care" about a mode that is quietly diverging, and the
  optimal-cost controller is not stabilizing.
  Here $Q^{1/2}$ is any matrix with $(Q^{1/2})^\top Q^{1/2} = Q$, so that
  $x^\top Q x = \lVert Q^{1/2}x\rVert^2$ is the "output" the cost sees. Detectability is the dual
  of stabilizability, with the rows stacked instead of the columns:
  $$\text{rank}\begin{bmatrix} A - \lambda I \\ Q^{1/2} \end{bmatrix} = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  since a rank drop means some non-decaying mode $v$ has $Q^{1/2}v = 0$ and so costs nothing.
  *Example:* on the §3 double integrator, $Q = \text{diag}(q, 0)$ passes (rank 2 at $\lambda = 0$),
  because position is penalized and velocity changes position. *Non-example:* $Q = \text{diag}(0, 1)$,
  velocity only, with $R = 1$, has rank 1 at $\lambda = 0$. Its positive semidefinite Riccati
  solution is $P = \text{diag}(0, 1)$, so $K = (0\;\;1)$ and the closed-loop eigenvalues are
  $0$ and $-1$: started at position $1$ with velocity $1$, the cart stops at position $2$ and stays
  there, because the cost never asked it to come back.

These two are the fine print behind "LQR is guaranteed stable." Papers that linearize a
nonlinear system and run LQR inherit both conditions *at the linearization point only*.

### 3. What Q and R do to behavior — a worked reading

Double integrator (cart): $x = (p, v)$, $u$ = force, so
$A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$, $B = \begin{pmatrix}0\\1\end{pmatrix}$.
Choose $Q = \mathrm{diag}(q, 0)$ and $R = r$.

**This one you can actually solve by hand**, and the answer teaches more than any solver
output. Write $P = \begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$ and substitute
into the Riccati equation. Its three distinct entries give three scalar equations:

$$q - \frac{p_{12}^2}{r} = 0, \qquad p_{11} - \frac{p_{12}p_{22}}{r} = 0, \qquad 2p_{12} - \frac{p_{22}^2}{r} = 0$$

They are triangular, which is why you can solve for $p_{12}$ first and let the rest follow: $p_{12} = \sqrt{qr}$, then $p_{22} = \sqrt{2r\sqrt{qr}}$, then $p_{11}$
follows. The gain $K = R^{-1}B^\top P$ is the bottom row of $P$ divided by $r$:

$$k_1 = \sqrt{\rho}, \qquad k_2 = \sqrt{2}\,\rho^{1/4}, \qquad \text{where } \rho = q/r$$

Now read what that says — three separate facts fall out at once.

| $q$ | $r$ | $\rho = q/r$ | $K = (k_1, k_2)$ | $\omega_n$ | $\zeta$ | settling $\approx 4/\zeta\omega_n$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7 s |
| 100 | 1 | 100 | $(10.0,\ 4.47)$ | 3.16 | 0.707 | 1.8 s |
| 1 | 100 | 0.01 | $(0.10,\ 0.45)$ | 0.32 | 0.707 | 17.9 s |
| 10 | 10 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7 s |

- **A common scalar scale does not matter.** Rows 1 and 4 have identical gains: multiplying
  every entry of $Q$ and $R$ by the same positive scalar changes the cost scale, not its
  argmin. Relative weights within the matrices still matter.
- **For this position-only $Q=\operatorname{diag}(q,0)$, the damping is fixed.** Every row has $\zeta = 1/\sqrt2 = 0.707$. The
  closed-loop characteristic polynomial is
  $\lambda^2 + \sqrt2\rho^{1/4}\lambda + \sqrt\rho$, so $\omega_n = \rho^{1/4}$ and
  $2\zeta\omega_n = \sqrt2\rho^{1/4}$ force $\zeta = 0.707$ for any $q/r$ **under this special choice of $Q$**. Adding a velocity-state weight changes the Riccati solution and can change damping. Here the weights buy speed, not shape. This makes the claim "LQR picks the poles by optimization instead of by hand"
  made concrete — [[04-robotics/control-theory-ce397|control theory §7]] placed poles at
  $\zeta = 0.7$ by hand, and LQR arrived at essentially the same place without being told.
- **Speed is a fourth root, which is brutal.** $\omega_n = \rho^{1/4}$ means doubling the
  controller's bandwidth costs a **16×** increase in $q/r$; ten times faster costs $10^4$.
  When an experimental section says "we raised the state weight by two orders of magnitude",
  that bought a factor of $\sqrt{10} \approx 3.2$ in bandwidth — and, because
  $k_1 = \sqrt\rho$ grew 10×, roughly 10× the commanded force and 10× the amplified sensor
  noise along with it.

The qualitative vocabulary experimental sections use maps onto exactly this arithmetic:

- **Large $q/r$** ("state expensive, control cheap"): aggressive gains — fast recovery, large
  force spikes, more noise amplification, actuator saturation risk (which LQR itself does not
  model — that is [[04-robotics/mpc|MPC]]'s job).
- **Small $q/r$** ("control expensive"): gentle gains, slow recovery, smooth inputs.
- Weights on velocity vs position shape *damping* vs *stiffness* of the response — the knob
  vocabulary behind "we tuned Q/R for a settling time of…".

<svg viewBox="0 0 440 206" style="max-width:100%;height:auto" role="img" aria-label="LQR step responses at three Q/R ratios, all with the same damping">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="40" y1="50" x2="410" y2="50" stroke-dasharray="4 4"/><line x1="40" y1="140" x2="410" y2="140"/><line x1="40" y1="20" x2="40" y2="140"/></g>
  <path d="M40.0 140.0L42.6 132.6L45.1 116.5L47.7 98.1L50.3 81.3L52.9 67.7L55.4 58.0L58.0 51.6L60.6 48.0L63.1 46.4L65.7 46.1L68.3 46.5L70.9 47.3L73.4 48.0L76.0 48.8L78.6 49.3L81.1 49.7L83.7 50.0L86.3 50.1L88.9 50.2L91.4 50.2L94.0 50.1L96.6 50.1L99.1 50.1L101.7 50.0L104.3 50.0L106.9 50.0L109.4 50.0L112.0 50.0L114.6 50.0L117.1 50.0L119.7 50.0L122.3 50.0L124.9 50.0L127.4 50.0L130.0 50.0L132.6 50.0L135.1 50.0L137.7 50.0L140.3 50.0L142.9 50.0L145.4 50.0L148.0 50.0L150.6 50.0L153.1 50.0L155.7 50.0L158.3 50.0L160.9 50.0L163.4 50.0L166.0 50.0L168.6 50.0L171.1 50.0L173.7 50.0L176.3 50.0L178.9 50.0L181.4 50.0L184.0 50.0L186.6 50.0L189.1 50.0L191.7 50.0L194.3 50.0L196.9 50.0L199.4 50.0L202.0 50.0L204.6 50.0L207.1 50.0L209.7 50.0L212.3 50.0L214.9 50.0L217.4 50.0L220.0 50.0L222.6 50.0L225.1 50.0L227.7 50.0L230.3 50.0L232.9 50.0L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M40.0 140.0L42.6 139.1L45.1 136.8L47.7 133.3L50.3 128.9L52.9 123.8L55.4 118.3L58.0 112.6L60.6 106.7L63.1 100.9L65.7 95.2L68.3 89.7L70.9 84.5L73.4 79.6L76.0 75.0L78.6 70.8L81.1 67.0L83.7 63.6L86.3 60.6L88.9 57.9L91.4 55.6L94.0 53.6L96.6 51.8L99.1 50.4L101.7 49.2L104.3 48.3L106.9 47.5L109.4 47.0L112.0 46.6L114.6 46.3L117.1 46.2L119.7 46.1L122.3 46.1L124.9 46.2L127.4 46.4L130.0 46.6L132.6 46.8L135.1 47.0L137.7 47.3L140.3 47.5L142.9 47.8L145.4 48.0L148.0 48.3L150.6 48.5L153.1 48.7L155.7 48.9L158.3 49.1L160.9 49.2L163.4 49.4L166.0 49.5L168.6 49.6L171.1 49.8L173.7 49.8L176.3 49.9L178.9 50.0L181.4 50.0L184.0 50.1L186.6 50.1L189.1 50.1L191.7 50.1L194.3 50.2L196.9 50.2L199.4 50.2L202.0 50.2L204.6 50.2L207.1 50.2L209.7 50.1L212.3 50.1L214.9 50.1L217.4 50.1L220.0 50.1L222.6 50.1L225.1 50.1L227.7 50.1L230.3 50.1L232.9 50.1L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/>
  <path d="M40.0 140.0L42.6 139.9L45.1 139.6L47.7 139.2L50.3 138.7L52.9 137.9L55.4 137.1L58.0 136.1L60.6 135.1L63.1 133.9L65.7 132.6L68.3 131.3L70.9 129.8L73.4 128.3L76.0 126.8L78.6 125.2L81.1 123.5L83.7 121.8L86.3 120.0L88.9 118.3L91.4 116.5L94.0 114.7L96.6 112.8L99.1 111.0L101.7 109.1L104.3 107.3L106.9 105.4L109.4 103.6L112.0 101.7L114.6 99.9L117.1 98.1L119.7 96.3L122.3 94.5L124.9 92.8L127.4 91.0L130.0 89.3L132.6 87.7L135.1 86.0L137.7 84.4L140.3 82.8L142.9 81.3L145.4 79.7L148.0 78.3L150.6 76.8L153.1 75.4L155.7 74.0L158.3 72.7L160.9 71.4L163.4 70.1L166.0 68.9L168.6 67.7L171.1 66.6L173.7 65.5L176.3 64.4L178.9 63.4L181.4 62.4L184.0 61.4L186.6 60.5L189.1 59.6L191.7 58.8L194.3 58.0L196.9 57.2L199.4 56.4L202.0 55.7L204.6 55.1L207.1 54.4L209.7 53.8L212.3 53.2L214.9 52.7L217.4 52.1L220.0 51.6L222.6 51.2L225.1 50.7L227.7 50.3L230.3 49.9L232.9 49.5L235.4 49.2L238.0 48.9L240.6 48.6L243.1 48.3L245.7 48.0L248.3 47.8L250.9 47.6L253.4 47.4L256.0 47.2L258.6 47.0L261.1 46.9L263.7 46.8L266.3 46.6L268.9 46.5L271.4 46.4L274.0 46.4L276.6 46.3L279.1 46.2L281.7 46.2L284.3 46.2L286.9 46.1L289.4 46.1L292.0 46.1L294.6 46.1L297.1 46.1L299.7 46.1L302.3 46.2L304.9 46.2L307.4 46.2L310.0 46.3L312.6 46.3L315.1 46.4L317.7 46.4L320.3 46.5L322.9 46.5L325.4 46.6L328.0 46.7L330.6 46.7L333.1 46.8L335.7 46.9L338.3 46.9L340.9 47.0L343.4 47.1L346.0 47.2L348.6 47.3L351.1 47.3L353.7 47.4L356.3 47.5L358.9 47.6L361.4 47.7L364.0 47.7L366.6 47.8L369.1 47.9L371.7 48.0L374.3 48.0L376.9 48.1L379.4 48.2L382.0 48.3L384.6 48.3L387.1 48.4L389.7 48.5L392.3 48.6L394.9 48.6L397.4 48.7L400.0 48.8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/>
  <g stroke="currentColor"><line x1="40" y1="160" x2="70" y2="160" stroke-width="2"/><line x1="40" y1="176" x2="70" y2="176" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/><line x1="40" y1="192" x2="70" y2="192" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/></g>
  <g font-size="11" fill="currentColor">
    <text x="6" y="54">target</text><text x="6" y="144">0</text><text x="386" y="156">time (s)</text>
    <text x="78" y="164">q/r = 100 &#183; wn = 3.16 &#183; settles 1.8 s</text>
    <text x="78" y="180">q/r = 1 &#183; wn = 1.00 &#183; settles 5.7 s</text>
    <text x="78" y="196">q/r = 0.01 &#183; wn = 0.32 &#183; settles 17.9 s</text>
  </g>
</svg>



### 4. LQG's fine print

**The LQG problem, written out.** Both the dynamics and the sensor carry zero-mean Gaussian white
noise, independent of each other ([[02-foundations/probability|3. Probability §5]]):

$$x_{k+1} = Ax_k + Bu_k + w_k, \qquad y_k = Cx_k + v_k, \qquad w_k \sim \mathcal N(0, W), \quad v_k \sim \mathcal N(0, V)$$

Here $W$ and $V$ are the process and measurement noise covariances (the probability page calls them
$Q$ and $R$; they are renamed because $Q$ and $R$ are already the cost weights), and $u_k$ may use
only the measurements up to step $k$. The objective is the expected LQR cost per step,
$\lim_{T\to\infty}\tfrac1T E\big[\sum_{k<T} (x_k^\top Q x_k + u_k^\top R u_k)\big]$, since the noise
never lets the state settle. The solution has three named parts:
- a **Kalman filter** that produces $\hat x_k$, with a gain from a filter Riccati equation that
  involves only $A, C, W, V$;
- an **LQR gain** $K$ from the DARE of §1, which involves only $A, B, Q, R$;
- the **certainty-equivalent controller** $u_k = -K\hat x_k$, which treats the estimate as if it
  were the true state.

That the two gains can be computed separately and the combination is still optimal is the
**separation principle**; its pole version, closed-loop eigenvalues equal to those of $A - BK$
together with those of $A - LC$, is derived in
[[04-robotics/control-theory-ce397|5. Control Theory §8]]. Existence needs $(A, B)$ stabilizable and
$(A, Q^{1/2})$ detectable for the controller, and the dual pair of conditions for the filter.
*Example:* with $A = B = C = 1$ and $Q = R = W = V = 1$, both Riccati equations reduce to
$P^2 - P - 1 = 0$, so the LQR gain and the steady-state Kalman gain are both $0.618$, the duality
made literal.

The separation principle is exact for linear-Gaussian models — and famously fragile:
**LQG has no guaranteed robustness margins** (Doyle 1978's one-line abstract: "there are
none"; gain, phase and stability margins are defined in
[[04-robotics/control-theory-ce397|5. Control Theory §5.5]]). Estimator error and model error interact; real systems re-introduce margin checks
or robust variants. Read "we use LQG" as *nominal-optimal, robustness unverified unless
shown*.

**Why study it**: LQR is the reference point everything else is measured against —
[[04-robotics/mpc|MPC]] is "LQR + constraints, re-solved online" (its terminal cost $P$
is typically the LQR Riccati solution); RL policy iteration or policy optimization on
linear-quadratic problems recovers LQR (evaluation alone only prices a fixed gain); and time-varying LQR around a trajectory is the
standard tracking controller that learned planners hand their outputs to.

**Suggested path**: EE363's LQR lectures (discrete-time finite horizon, via Lagrange multipliers, infinite horizon, continuous time — lectures 16–19 in the Spring 2026 list) →
Underactuated ch. (geometric intuition, code) → connect to the
[[02-foundations/optimization|MPC-as-QP example]].

### Self-check

1. What happens to the Riccati approach if $(A,B)$ is not stabilizable?
2. On the double integrator, scale $Q$ by 10 and $R$ by 10 together — what happens to $K$?
3. In one sentence: why is "LQG is optimal, therefore robust" wrong?
4. Why use LQR's $P$ as the MPC terminal cost?

> [!tip]- Answers
> 1. No feedback can catch the unstable mode, so no stabilizing solution $P$ exists — the problem itself is ill-posed.
> 2. Unchanged — multiplying all of $Q$ and $R$ by the same positive scalar changes only the overall cost scale. Relative weights within matrix-valued $Q$ and $R$ still determine $K$.
> 3. Optimality is with respect to the nominal model, and LQG is proven to have no guaranteed margins against model error (Doyle 1978).
> 4. $x^\top P x$ is the exact cost-to-go inside a terminal set where the LQR law satisfies the constraints and keeps the state in the set. With that terminal constraint added, a short horizon still supports the stability argument — the terminal cost and terminal set together are the ingredients [[04-robotics/mpc|MPC §1]] lists (Borrelli Theorem 12.2).

### Problem set · 과제

Tier B. **P4** $\dot x=-x+u+d$ from [[02-foundations/lab-plants|0.6]], $Q=1$, $R=1$. No simulator.

1. **Draw.** The leaky heater with $u=-Kx$, boxes for $Q$ and $R$, disturbance $d$.
2. **Derive.** Scalar ARE. Stabilizing $P$ and $K$. Closed-loop pole and $x_\mathrm{ss}$ for $d=1$. Same two numbers at a CE397-style hand gain $K=4$.
3. **Interpret.** Why LQR's $K$ is smaller than $K=4$, and what raising $Q/R$ buys and costs (the $(1+K)$ trade of CE397 §1).

> [!tip]- Solutions
> 1. Plant pole already at $-1$; $Q$ prices $x$, $R$ prices $u$.
> 2. $-2P-P^2+1=0\Rightarrow P=-1+\sqrt2\approx0.414$, $K=P\approx0.414$. Pole $-(1+K)\approx-1.414$, $x_\mathrm{ss}=d/(1+K)\approx0.707$. At $K=4$: pole $-5$, $x_\mathrm{ss}=0.2$.
> 3. $Q=R=1$ prices state and effort equally on an already-stable plant, so the optimizer barely acts. $K=4$ is a hand choice (CE397 §1 used $K=9$ for $10\times$ rejection). Raising $Q/R$ increases $K$, buys smaller $x_\mathrm{ss}$, costs effort and noise.

### Continue beyond this guide

The estimator side of LQG is developed in [[04-robotics/state-estimation-slam|State Estimation, Localization & SLAM]].

### Connections

- Foundations: [[02-foundations/linear-algebra|Linear Algebra]] (Riccati, eigenvalues), [[02-foundations/probability|Probability]] (Kalman), [[02-foundations/optimization|Optimization]]
- Next: [[04-robotics/mpc|MPC]]

### After reading

- [ ] State the LQR problem and the form of its solution ($u=-Kx$, $K=R^{-1}B^\top P$)
- [ ] Say what stabilizability and detectability each guarantee, and what fails without them
- [ ] Explain with the worked example how the $Q/R$ ratio changes gains, response, and saturation risk
- [ ] State the separation principle and its fragility (LQG has no guaranteed margins), and why LQR is the reference point for MPC and RL

## 한국어

*[[04-robotics/control-theory-ce397|5. 제어 이론]]과 확률·최적화 위에 선다. D군이다. 극점을 손으로 고르는 대신 비용이 고르게 하고,
분리 원리가 추정기와 제어기를 따로 설계해도 되는 조건을 말해 준다.*

**무엇인가**: **LQR**은 최적 제어에서 정확히 풀리는 심장부다. 선형 동역학
$\dot x = Ax + Bu$와 이차 비용 $\int (x^\top Q x + u^\top R u)\,dt$($Q \succeq 0$, $R \succ 0$이라 $R^{-1}$이 존재)에 대해 최적 제어기는
상수 선형 피드백 $u = -Kx$이고, $K = R^{-1}B^\top P$에서 $P$는 **대수 리카티 방정식**의
해다 — 실행 시 반복 계산이 없다. 식으로 쓰면 무한 지평 LQR 문제는

$$\min_{u(\cdot)}\; J = \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt \quad \text{subject to} \quad \dot x = Ax + Bu,\;\; x(0) = x_0$$

이고 이름 붙은 재료가 넷이다. 선형 모델 $(A, B)$; 원점에서 벗어난 것에 값을 매기는 **상태 가중치**
$Q$, 양의 준정부호(모든 $x$에서 $x^\top Q x \ge 0$); 노력에 값을 매기는 **입력 가중치** $R$, 양의
정부호(모든 $u \ne 0$에서 $u^\top R u > 0$)이며 공짜 입력이 없도록 엄격히 양수여야 한다; 그리고 무한
지평, 이것 때문에 최적 이득이 시변이 아니라 상수다. (정부호성은 [[02-foundations/linear-algebra|1. 선형대수 §3]]에서
정의한다.) 기준 궤적 추종은 오차 좌표 $x - x_{ref}$로 쓴 같은 문제다. **LQG**는 가우시안 노이즈와 부분 관측을 더한 것: 최적해는
[[02-foundations/probability|칼만 필터]]가 LQR에 추정값을 공급하는 구조다
(**분리 원리**: 최적으로 추정하고, 그 추정값을 최적으로 제어하면, 그 결합이 전체 최적이다).

> [!note] 처음이라면 · First pass
> 짧은 페이지이니 통독하라. 10분뿐이라면 §2다 — "LQR은 안정성이 보장된다"에는 조건이 둘 붙어 있고, 비선형계를 선형화해 쓰는 논문은 그 조건을 선형화 지점에서만 물려받는다.

### 과제가 그릴 그림 · Homework diagram

여기서 한 번 그려 두면, 과제는 가중치 하나만 바꾼 같은 그림을 요구한다. 대상은
[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P4**, 곧
[[04-robotics/control-theory-ce397|5. 제어 이론 §1]]의 새는 히터 $\dot x=-x+u+d$다. 기계는
그대로이고, 이득을 손이 아니라 비용이 고른다는 점만 다르다.

<svg viewBox="0 0 560 376" style="max-width:100%;height:auto" role="img" aria-label="위: 외란이 합산점으로 들어오는 새는 히터의 피드백 루프와, x에는 Q로 u에는 R로 값을 매겨 J로 모으는 파선 장부. 아래: 개루프 극점 -1, Q = 1의 폐루프 극점 -1.414, Q = 4의 폐루프 극점 -2.236을 찍은 실수축.">
  <defs><marker id="aLQRk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <circle cx="96" cy="80" r="11"/>
    <rect x="160" y="60" width="160" height="40" rx="3"/>
    <rect x="238" y="138" width="60" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aLQRk)">
    <line x1="96" y1="26" x2="96" y2="68"/>
    <line x1="107" y1="80" x2="158" y2="80"/>
    <line x1="320" y1="80" x2="424" y2="80"/>
    <polyline points="380,80 380,152 300,152"/>
    <polyline points="238,152 96,152 96,92"/>
  </g>
  <circle cx="380" cy="80" r="3" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-dasharray="4 3" stroke-opacity="0.75">
    <polyline points="424,80 452,80"/>
    <polyline points="472,94 472,204"/>
    <polyline points="140,152 140,204"/>
    <polyline points="160,218 300,218"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.75">
    <rect x="452" y="66" width="40" height="28" rx="3"/>
    <rect x="120" y="204" width="40" height="28" rx="3"/>
    <rect x="300" y="204" width="240" height="28" rx="3"/>
  </g>
  <circle cx="140" cy="152" r="2.6" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="50" y1="306.0" x2="519.5" y2="306.0"/>
    <line x1="470" y1="301.0" x2="470" y2="311.0"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.45">
    <line x1="170" y1="303.0" x2="170" y2="309.0"/>
    <line x1="320" y1="303.0" x2="320" y2="309.0"/>
  </g>
  <g stroke="currentColor" fill="none">
    <path d="M314.5 300.5 L325.5 311.5 M314.5 311.5 L325.5 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M252.4 300.5 L263.4 311.5 M252.4 311.5 L263.4 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M129.1 300.5 L140.1 311.5 M129.1 311.5 L140.1 300.5" stroke-width="2.4" stroke-opacity="1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aLQRk)">
    <line x1="320" y1="290.0" x2="138.6" y2="290.0"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="96" y="84">Σ</text>
    <text x="240" y="85">ẋ = −x + u + d</text>
    <text x="268" y="157">−K</text>
    <text x="472" y="85">Q</text>
    <text x="140" y="223">R</text>
    <text x="420" y="223">J = ∫<tspan font-size="9.5" dy="4">0</tspan><tspan font-size="9.5" dy="-10">∞</tspan><tspan dy="6"> (Qx² + Ru²) dt</tspan></text>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="104" y="38">d</text>
    <text x="360" y="73">x</text>
    <text x="182" y="146">u</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="240" y="52" text-anchor="middle" opacity="0.85">P4, 새는 히터</text>
    <text x="268" y="184" text-anchor="middle">(Q, R) → P → K: 오프라인에서 한 번</text>
    <text x="268" y="198" text-anchor="middle" opacity="0.85">Q = 4, R = 1이면 P = K = 1.236</text>
    <text x="540" y="250" text-anchor="end" opacity="0.8">장부: 회계 경로이며 플랜트를 전혀 건드리지 않는다</text>
    <text x="227.3" y="283.0" text-anchor="middle">Q/R을 올리면 폐루프 극점이 왼쪽으로 미끄러진다</text>
    <text x="328" y="326.0">−1</text>
    <text x="328" y="340.0" opacity="0.85">개루프</text>
    <text x="257.9" y="326.0" text-anchor="middle" opacity="0.85">−√2 = −1.414</text>
    <text x="257.9" y="340.0" text-anchor="middle" opacity="0.85">Q = 1, 과제</text>
    <text x="134.6" y="326.0" text-anchor="middle">−√5 = −2.236</text>
    <text x="134.6" y="340.0" text-anchor="middle">Q = 4, §1의 계산</text>
    <text x="470" y="326.0" text-anchor="middle">0</text>
    <text x="523.5" y="310.0">Re s</text>
    <text x="12" y="363" opacity="0.9">R = 1에서 폐루프 극점 −(1 + K) = −√(1 + Q), 그림의 나머지는 움직이지 않는다</text>
  </g>
</svg>

**루프.** 합산점 하나, 그 뒤에 플랜트 상자 $\dot x=-x+u+d$, 그 합산점으로 $u$와 나란히 들어오는
외란 $d$, 상자에서 나오는 상태 $x$, 그리고 $x$에서 이득 상자 $-K$를 거쳐 합산점으로 돌아가는
피드백 경로. 여기까지는 제어 이론 페이지의 그림 그대로이고, 바뀐 것이 없다.

**LQR이 더하는 것 — 장부.** 두 신호를 각각 따서 값이 치러지는 곳을 그린다. $x$에서 상자 $Q$로
가는 가지, $u$에서 상자 $R$로 가는 가지, 그리고 둘이 함께 들어가는 누산기
$J=\int_0^\infty (Qx^2+Ru^2)\,dt$. 이 가지는 선 굵기를 달리해 그려라. 플랜트를 전혀 건드리지
않는 회계 경로이지 제어 경로가 아니며, 이렇게 시각적으로 갈라 두어야 $Q$·$R$이 §4에서 같은
루프로 들어오는 잡음 공분산 $W$·$V$와 섞이지 않는다. $-K$ 상자 옆에는 리카티 방정식이 곧
화살표 하나라는 것을 적는다: $(Q,R)\rightarrow P\rightarrow K$, 그리고 *오프라인에서 한 번*.

**극점 축.** 루프 아래에 실수축을 긋는다. 제어하지 않은 히터가 이미 앉아 있는 개루프 극점
$-1$과 폐루프 극점 $-(1+K)$를 표시한다. 이 플랜트에서 $R=1$일 때 안정화 리카티 해는
$P=K=-1+\sqrt{1+Q}$이므로 폐루프 극점은 정확히 $-\sqrt{1+Q}$에 놓인다. §1에서 푼 $Q=4$의
경우는 $-\sqrt5=-2.236$, 과제의 $Q=1$은 $-\sqrt2=-1.414$를 찍어라. 그릴 값이 있는 화살표는
논문을 읽을 때 쓰이는 그것이다 — $Q/R$을 올리면 그 극점이 왼쪽으로 미끄러지고, 그림의 나머지는
아무것도 움직이지 않는다.

### 1. 리카티 방정식, 구조로 읽기

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

이것이 **대수 리카티 방정식**(ARE)이다. 모르는 대칭 $n \times n$ 행렬 $P$에 대해 이차인 행렬
방정식이고, 자료는 모델 $A, B$와 가중치 $Q, R$이다. $P$는 최적 **cost-to-go**(가치 함수), 즉 주어진
출발 상태에서 달성할 수 있는 최소 비용의 행렬이다.

$$V(x_0) = \min_{u(\cdot)} \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt = x_0^\top P x_0$$

그래서 $P$는 모든 $x_0$에 대해 한꺼번에 "$x_0$에 있는 것이 얼마나 비싼가"에 답한다.

**어디서 오는가, 네 단계로.** 최적 cost-to-go가 이차형식이라고 추측한다,
$V(x) = x^\top P x$ — 맞아떨어지기 때문에 사후에 정당화되는 추측이다. 그것을 최적성
조건(연속 시간 벨만 방정식, 즉 HJB — 벨만 방정식은 [[02-foundations/rl-basics|7. RL 기초 §2]]에서 이산 시간으로 소개된다)에 대입한다. 최적에서는 순간 비용과 cost-to-go의 변화율의
합이 0이라는 조건이다: $0 = \min_u\,[\,x^\top Q x + u^\top R u + \nabla V^\top(Ax + Bu)\,]$,
그리고 $\nabla V = 2Px$다. 셋째, $u$에 대해 최소화하는데 이제 평범한 이차식이다. 미분을 0으로
두면 $2Ru + 2B^\top P x = 0$, 즉 $u^\star = -R^{-1}B^\top P x$다. **LQR 이득
$K = R^{-1}B^\top P$가 여기서 나온다. 설계된 것이 아니라 떨어져 나온다.** 넷째, $u^\star$를
도로 넣는다. 모든 항이 양옆에 $x$를 하나씩 달고 있고, 그 사이에 남는 것이 정확히 위의
방정식이다.

그렇게 읽으면 이상해 보이던 가운데 항이 평범해진다. $-PBR^{-1}B^\top P$는 덧붙인 모델링 선택이
아니라 *최적 피드백을 비용에 도로 대입한 것*이다. $P$에 대해 이차인 이유이고, 빼는 이유다 —
제어기가 행동함으로써 *치르지 않게 된* 비용이다.

**계산 예제, 스칼라.** 불안정한 $\dot x = x + u$($A = B = 1$)에 $Q = R = 1$을 쓰자. ARE는
$2P - P^2 + 1 = 0$이 되고 근이 **둘**, $P = 1 + \sqrt2 = 2.414$와 $P = 1 - \sqrt2 = -0.414$다.
**안정화 해**는 그 이득이 $A - BK$를 안정하게 만드는 해다. $P = 2.414$는 $K = 2.414$와 폐루프
$\dot x = -1.414\,x$를 주고, $P = -0.414$는 $\dot x = +1.414\,x$를 준다. 리카티 방정식은 일반적으로
해가 여럿이고, 논문의 "그" 해는 언제나 안정화 해를 뜻한다. cost-to-go를 검산하면, $x_0 = 1$에서
폐루프는 $x = e^{-1.414t}$, $u = -2.414\,x$이므로
$J = \int_0^\infty (1 + 2.414^2)\,e^{-2.828t}\,dt = 2.414 = P$다.

**계산: 이미 안정한 장치 P4.** 새는 히터 $\dot x=-x+u$는 $A=-1$, $B=1$([[02-foundations/lab-plants|0.6]]). $Q=4$, $R=1$이면 ARE는 $-2P-P^2+4=0$, $P=-1+\sqrt5\approx 1.236$(양근). $K\approx 1.236$, 폐루프 극점 $\approx-2.24$, 상수 $d=1$은 $x_\mathrm{ss}\approx 0.45$. 손 이득 $K=4$는 극점 $-5$, $x_\mathrm{ss}=0.2$. $Q=4$는 이미 상태 쪽을 더 사서 LQR이 움직이지만, $5$배 억제를 산 손 이득만큼은 아니다. 과제는 $Q=R=1$에서 ARE를 반복한다. 플랜트가 이미 안정하고 상태와 노력을 같게 매기므로 최적화기는 거의 안 움직인다($K\approx 0.414$). $Q/R$을 올리는 것이 CE397 §1의 $(1+K)$ 거래다.

(로봇 논문은 대개 **이산 시간 쌍둥이** — DARE, 이득 $K=(R+B^\top P B)^{-1}B^\top P A$ — 를 쓴다; 구조도 읽는 법도 같다.) $x_{k+1} = Ax_k + Bu_k$와 비용 $\sum_k (x_k^\top Q x_k + u_k^\top R u_k)$에 대해 식은

$$P = A^\top P A - A^\top P B\,(R + B^\top P B)^{-1} B^\top P A + Q$$

이다. 각 스텝의 cost-to-go가 단계 비용에 최선의 입력 아래 다음 스텝 cost-to-go를 더한 것이기 때문이다.
$x_{k+1} = x_k + u_k$, $Q = R = 1$이면 $P^2 - P - 1 = 0$으로 줄어 $P = 1.618$, $K = P/(1+P) = 0.618$이고,
폐루프 $x_{k+1} = 0.382\,x_k$는 단위원 안에 있다([[04-robotics/mpc|7. MPC]]가 이 숫자를 다시 쓴다). 손으로 푸는 일은 없다 — 하지만 구조로 읽으면 남는 게 있다: $Q$는 상태 비용을 주입하고,
이차 항 $-PBR^{-1}B^\top P$는 *피드백이 제어를 통해 비용을 깎아먹는* 항이며, 안정화 해
$P$가 — $(A,Q^{1/2})$가 가관측이면 양의 정부호 — $V(x)=x^\top P x$를 폐루프의 리아푸노프 함수로 만든다. (**리아푸노프 함수**(Lyapunov function)란 $x=0$을 뺀 모든 곳에서 양수이고 모든 폐루프 궤적을 따라 줄어드는 상태의 스칼라 "에너지"다. 그런 함수가 있으면 상태는 $0$ 말고 갈 곳이 없으므로, 그 존재가 곧 안정성의 증명이다. 세 조건과 계산 예제는 [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]에 있다. 여기서는 HJB 조건이 $\dot V = -(x^\top Q x + u^{\star\top} R u^\star)$, 즉 순간 비용에 음수를 붙인 값을 준다.) 검출 가능성만 있으면 $P \succeq 0$이고 LaSalle류 논증이 필요하다 — LaSalle 불변 원리는 $\dot V$가 $\le 0$에 그칠 때도, 원점 말고는 어떤 궤적도 $\dot V = 0$인 곳에 영원히 머물 수 없다면 수렴을 증명해 준다. 논문이 "리카티
방정식을 푼다"고 하면 이 상수 $P$를 오프라인에서 한 번(반복/시변 LQR에서는 선형화마다
한 번) 계산한다는 뜻이다.

### 2. 언제 실제로 통하는가? 두 조건

- **$(A,B)$의 안정화 가능성(stabilizability)**: $\text{Re}\,\lambda \ge 0$인 $A$의 모든 모드가 — 이중 적분기의 $\lambda = 0$ 모드도 포함해 — $u$의 영향을
  받아야 한다 — 안정화 피드백이 존재하기 위한 정확한(필요충분) 조건이며,
  [[02-foundations/linear-algebra|1페이지 제어 섹션]]의 완전한 가제어성 랭크 검정보다
  약하다. 아니면 리카티든 뭐든 어떤 피드백도 안정화할 수 없다.
  정의로 쓰면, 어떤 이득 $K$가 $A - BK$의 모든 고유값의 실수부를 음수로 만들 때 $(A,B)$가
  **안정화 가능**하다. 모드별로는 PBH(Popov–Belevitch–Hautus) 랭크 검정으로 확인한다.
  $$\text{rank}\,[\,A - \lambda I \;\; B\,] = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  입력이 건드릴 수 없는 모드의 고유값에서 정확히 랭크가 $n$ 아래로 떨어지기 때문이다. *모든*
  고유값에서 완전 랭크를 요구하면 그것이 가제어성 자체다. (이산 시간에서는 $|\lambda| \ge 1$인 모드가
  불안정 모드다.) *예:* [[04-robotics/control-theory-ce397|5. 제어 이론 §6]]의 불가제어 쌍
  $A = \text{diag}(-1,-2)$, $B = (1, 0)^\top$은 스스로 감쇠하는 모드인 $\lambda = -2$에서만 랭크를
  잃으므로 안정화 가능하다. *반례:* 같은 $B$에 $A = \text{diag}(1, 2)$이면 불안정 모드인
  $\lambda = 2$에서 랭크를 잃으므로 그런 $K$가 없다.
- **$(A,Q^{1/2})$의 검출 가능성(detectability)**: $\text{Re}\,\lambda \ge 0$인 모든 모드가 비용에 나타나야
  한다 — 아니면 최적화기가 조용히 발산하는 모드를 "신경 안 쓰는" 것이 허용되어, 최적
  비용의 제어기가 안정화 제어기가 아니게 된다.
  $Q^{1/2}$는 $(Q^{1/2})^\top Q^{1/2} = Q$인 아무 행렬이며, 그래서 $x^\top Q x = \lVert Q^{1/2}x\rVert^2$가
  비용이 보는 "출력"이 된다. 검출 가능성은 안정화 가능성의 쌍대로, 열 대신 행을 쌓는다.
  $$\text{rank}\begin{bmatrix} A - \lambda I \\ Q^{1/2} \end{bmatrix} = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  랭크가 떨어진다는 것은 감쇠하지 않는 어떤 모드 $v$가 $Q^{1/2}v = 0$이라 비용이 들지 않는다는 뜻이기
  때문이다. *예:* §3의 이중 적분기에서 $Q = \text{diag}(q, 0)$은 통과한다($\lambda = 0$에서 랭크 2).
  위치에 벌점이 붙고 속도가 위치를 바꾸기 때문이다. *반례:* 속도만 보는 $Q = \text{diag}(0, 1)$,
  $R = 1$은 $\lambda = 0$에서 랭크 1이다. 양의 준정부호 리카티 해는 $P = \text{diag}(0, 1)$이라
  $K = (0\;\;1)$이고 폐루프 고유값은 $0$과 $-1$이다. 위치 $1$, 속도 $1$에서 출발한 카트는 위치 $2$에서
  멈추고 거기 머문다. 비용이 돌아오라고 요구한 적이 없기 때문이다.

이 둘이 "LQR은 안정성이 보장된다"의 작은 글씨다. 비선형 시스템을 선형화해 LQR을 쓰는
논문은 두 조건을 *선형화 지점에서만* 상속한다.

### 3. Q와 R이 거동에 하는 일 — 읽기용 예제

이중 적분기(카트): $x = (p, v)$, $u$ = 힘이므로
$A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$, $B = \begin{pmatrix}0\\1\end{pmatrix}$.
$Q = \mathrm{diag}(q, 0)$, $R = r$로 두자.

**이 경우는 손으로 실제로 풀린다**, 그리고 그 답이 어떤 솔버 출력보다 많은 것을 가르쳐 준다.
$P = \begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$로 놓고 리카티 방정식에 대입하면
서로 다른 세 성분에서 스칼라 방정식 셋이 나온다:

$$q - \frac{p_{12}^2}{r} = 0, \qquad p_{11} - \frac{p_{12}p_{22}}{r} = 0, \qquad 2p_{12} - \frac{p_{22}^2}{r} = 0$$

세 식은 삼각 구조라 $p_{12}$부터 풀고 나머지를 따라오게 할 수 있다: $p_{12} = \sqrt{qr}$, 이어서 $p_{22} = \sqrt{2r\sqrt{qr}}$, 그리고 $p_{11}$이
따라 나온다. 이득 $K = R^{-1}B^\top P$는 $P$의 아랫줄을 $r$로 나눈 것이다:

$$k_1 = \sqrt{\rho}, \qquad k_2 = \sqrt{2}\,\rho^{1/4}, \qquad \rho = q/r$$

이제 이 식이 하는 말을 읽어보자 — 서로 다른 사실 셋이 한꺼번에 떨어진다.

| $q$ | $r$ | $\rho = q/r$ | $K = (k_1, k_2)$ | $\omega_n$ | $\zeta$ | 정착 시간 $\approx 4/\zeta\omega_n$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7초 |
| 100 | 1 | 100 | $(10.0,\ 4.47)$ | 3.16 | 0.707 | 1.8초 |
| 1 | 100 | 0.01 | $(0.10,\ 0.45)$ | 0.32 | 0.707 | 17.9초 |
| 10 | 10 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7초 |

- **공통 스칼라 배율은 의미가 없다.** 1행과 4행의 이득이 완전히 같다. $Q$와 $R$의 모든
  원소에 같은 양의 스칼라를 곱하면 비용의 크기만 바뀌고 argmin은 움직이지 않는다. 행렬 내부의
  상태·입력 사이 상대 가중치는 여전히 중요하다.
- **이 위치-only $Q=\operatorname{diag}(q,0)$에서는 감쇠가 고정된다.** 모든 행에서 $\zeta = 1/\sqrt2 = 0.707$이다. 폐루프
  특성 다항식이 $\lambda^2 + \sqrt2\rho^{1/4}\lambda + \sqrt\rho$이므로
  $\omega_n = \rho^{1/4}$, $2\zeta\omega_n = \sqrt2\rho^{1/4}$가 되어 **이 특수한 $Q$에서**
  어떤 $q/r$을 써도 $\zeta = 0.707$이다. 속도 상태 가중치를 추가하면 Riccati 해와 감쇠가
  달라질 수 있다. 이 예에서는 가중치가 사는 것이 속도이지 모양이 아니다. "LQR은 극점을 손이 아니라 최적화가 고른다"는
  일반론이 구체화된 것이다 — [[04-robotics/control-theory-ce397|제어 이론 §7]]은 손으로
  $\zeta = 0.7$에 놓았고, LQR은 시키지 않아도 사실상 같은 자리에 도착했다.
- **속도는 네제곱근이고, 이건 가혹하다.** $\omega_n = \rho^{1/4}$이므로 대역폭을 두 배로
  올리려면 $q/r$을 **16배**, 열 배로 올리려면 $10^4$배 키워야 한다. 실험 절에 "상태 가중치를
  두 자릿수 올렸다"고 쓰여 있으면 대역폭으로는 $\sqrt{10} \approx 3.2$배를 산 것이고,
  $k_1 = \sqrt\rho$가 10배 커졌으니 명령 힘도 대략 10배, 증폭되는 센서 잡음도 10배다.

실험 절이 쓰는 정성적 어휘가 정확히 이 산수에 대응한다:

- **큰 $q/r$**("상태가 비싸고 제어가 싸다"): 공격적 이득 — 빠른 회복, 큰 힘 스파이크, 잡음
  증폭 증가, 액추에이터 포화 위험(LQR 자신은 이를 모델링하지 않는다 —
  [[04-robotics/mpc|MPC]]의 몫이다).
- **작은 $q/r$**("제어가 비싸다"): 부드러운 이득, 느린 회복, 매끄러운 입력.
- 속도 vs 위치 가중치는 응답의 *감쇠* vs *강성*을 빚는다 — "정착 시간 …를 위해 Q/R을
  튜닝했다"는 문장 뒤의 손잡이 어휘다.

<svg viewBox="0 0 440 206" style="max-width:100%;height:auto" role="img" aria-label="세 가지 Q/R 비에서의 LQR 계단 응답 — 감쇠는 모두 같다">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="40" y1="50" x2="410" y2="50" stroke-dasharray="4 4"/><line x1="40" y1="140" x2="410" y2="140"/><line x1="40" y1="20" x2="40" y2="140"/></g>
  <path d="M40.0 140.0L42.6 132.6L45.1 116.5L47.7 98.1L50.3 81.3L52.9 67.7L55.4 58.0L58.0 51.6L60.6 48.0L63.1 46.4L65.7 46.1L68.3 46.5L70.9 47.3L73.4 48.0L76.0 48.8L78.6 49.3L81.1 49.7L83.7 50.0L86.3 50.1L88.9 50.2L91.4 50.2L94.0 50.1L96.6 50.1L99.1 50.1L101.7 50.0L104.3 50.0L106.9 50.0L109.4 50.0L112.0 50.0L114.6 50.0L117.1 50.0L119.7 50.0L122.3 50.0L124.9 50.0L127.4 50.0L130.0 50.0L132.6 50.0L135.1 50.0L137.7 50.0L140.3 50.0L142.9 50.0L145.4 50.0L148.0 50.0L150.6 50.0L153.1 50.0L155.7 50.0L158.3 50.0L160.9 50.0L163.4 50.0L166.0 50.0L168.6 50.0L171.1 50.0L173.7 50.0L176.3 50.0L178.9 50.0L181.4 50.0L184.0 50.0L186.6 50.0L189.1 50.0L191.7 50.0L194.3 50.0L196.9 50.0L199.4 50.0L202.0 50.0L204.6 50.0L207.1 50.0L209.7 50.0L212.3 50.0L214.9 50.0L217.4 50.0L220.0 50.0L222.6 50.0L225.1 50.0L227.7 50.0L230.3 50.0L232.9 50.0L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M40.0 140.0L42.6 139.1L45.1 136.8L47.7 133.3L50.3 128.9L52.9 123.8L55.4 118.3L58.0 112.6L60.6 106.7L63.1 100.9L65.7 95.2L68.3 89.7L70.9 84.5L73.4 79.6L76.0 75.0L78.6 70.8L81.1 67.0L83.7 63.6L86.3 60.6L88.9 57.9L91.4 55.6L94.0 53.6L96.6 51.8L99.1 50.4L101.7 49.2L104.3 48.3L106.9 47.5L109.4 47.0L112.0 46.6L114.6 46.3L117.1 46.2L119.7 46.1L122.3 46.1L124.9 46.2L127.4 46.4L130.0 46.6L132.6 46.8L135.1 47.0L137.7 47.3L140.3 47.5L142.9 47.8L145.4 48.0L148.0 48.3L150.6 48.5L153.1 48.7L155.7 48.9L158.3 49.1L160.9 49.2L163.4 49.4L166.0 49.5L168.6 49.6L171.1 49.8L173.7 49.8L176.3 49.9L178.9 50.0L181.4 50.0L184.0 50.1L186.6 50.1L189.1 50.1L191.7 50.1L194.3 50.2L196.9 50.2L199.4 50.2L202.0 50.2L204.6 50.2L207.1 50.2L209.7 50.1L212.3 50.1L214.9 50.1L217.4 50.1L220.0 50.1L222.6 50.1L225.1 50.1L227.7 50.1L230.3 50.1L232.9 50.1L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/>
  <path d="M40.0 140.0L42.6 139.9L45.1 139.6L47.7 139.2L50.3 138.7L52.9 137.9L55.4 137.1L58.0 136.1L60.6 135.1L63.1 133.9L65.7 132.6L68.3 131.3L70.9 129.8L73.4 128.3L76.0 126.8L78.6 125.2L81.1 123.5L83.7 121.8L86.3 120.0L88.9 118.3L91.4 116.5L94.0 114.7L96.6 112.8L99.1 111.0L101.7 109.1L104.3 107.3L106.9 105.4L109.4 103.6L112.0 101.7L114.6 99.9L117.1 98.1L119.7 96.3L122.3 94.5L124.9 92.8L127.4 91.0L130.0 89.3L132.6 87.7L135.1 86.0L137.7 84.4L140.3 82.8L142.9 81.3L145.4 79.7L148.0 78.3L150.6 76.8L153.1 75.4L155.7 74.0L158.3 72.7L160.9 71.4L163.4 70.1L166.0 68.9L168.6 67.7L171.1 66.6L173.7 65.5L176.3 64.4L178.9 63.4L181.4 62.4L184.0 61.4L186.6 60.5L189.1 59.6L191.7 58.8L194.3 58.0L196.9 57.2L199.4 56.4L202.0 55.7L204.6 55.1L207.1 54.4L209.7 53.8L212.3 53.2L214.9 52.7L217.4 52.1L220.0 51.6L222.6 51.2L225.1 50.7L227.7 50.3L230.3 49.9L232.9 49.5L235.4 49.2L238.0 48.9L240.6 48.6L243.1 48.3L245.7 48.0L248.3 47.8L250.9 47.6L253.4 47.4L256.0 47.2L258.6 47.0L261.1 46.9L263.7 46.8L266.3 46.6L268.9 46.5L271.4 46.4L274.0 46.4L276.6 46.3L279.1 46.2L281.7 46.2L284.3 46.2L286.9 46.1L289.4 46.1L292.0 46.1L294.6 46.1L297.1 46.1L299.7 46.1L302.3 46.2L304.9 46.2L307.4 46.2L310.0 46.3L312.6 46.3L315.1 46.4L317.7 46.4L320.3 46.5L322.9 46.5L325.4 46.6L328.0 46.7L330.6 46.7L333.1 46.8L335.7 46.9L338.3 46.9L340.9 47.0L343.4 47.1L346.0 47.2L348.6 47.3L351.1 47.3L353.7 47.4L356.3 47.5L358.9 47.6L361.4 47.7L364.0 47.7L366.6 47.8L369.1 47.9L371.7 48.0L374.3 48.0L376.9 48.1L379.4 48.2L382.0 48.3L384.6 48.3L387.1 48.4L389.7 48.5L392.3 48.6L394.9 48.6L397.4 48.7L400.0 48.8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/>
  <g stroke="currentColor"><line x1="40" y1="160" x2="70" y2="160" stroke-width="2"/><line x1="40" y1="176" x2="70" y2="176" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/><line x1="40" y1="192" x2="70" y2="192" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/></g>
  <g font-size="11" fill="currentColor">
    <text x="6" y="54">목표값</text><text x="6" y="144">0</text><text x="386" y="156">시간 (초)</text>
    <text x="78" y="164">q/r = 100 &#183; wn = 3.16 &#183; 정착 1.8초</text>
    <text x="78" y="180">q/r = 1 &#183; wn = 1.00 &#183; 정착 5.7초</text>
    <text x="78" y="196">q/r = 0.01 &#183; wn = 0.32 &#183; 정착 17.9초</text>
  </g>
</svg>



### 4. LQG의 작은 글씨

**LQG 문제를 식으로.** 동역학과 센서 모두에 서로 독립인 평균 0의 가우시안 백색 잡음이 붙는다
([[02-foundations/probability|3. 확률 §5]]).

$$x_{k+1} = Ax_k + Bu_k + w_k, \qquad y_k = Cx_k + v_k, \qquad w_k \sim \mathcal N(0, W), \quad v_k \sim \mathcal N(0, V)$$

$W$와 $V$는 공정 잡음과 측정 잡음의 공분산이다(확률 페이지는 $Q$와 $R$로 부르지만, 여기서는 $Q$와
$R$이 이미 비용 가중치라 이름을 바꿨다). $u_k$는 스텝 $k$까지의 측정만 쓸 수 있다. 잡음 때문에 상태가
결코 가라앉지 않으므로 목적은 스텝당 기대 LQR 비용
$\lim_{T\to\infty}\tfrac1T E\big[\sum_{k<T} (x_k^\top Q x_k + u_k^\top R u_k)\big]$이다. 해는 이름 붙은
세 부분으로 이루어진다.
- $\hat x_k$를 만드는 **칼만 필터**. 그 이득은 $A, C, W, V$만 들어가는 필터 리카티 방정식에서 나온다.
- §1의 DARE에서 나오는 **LQR 이득** $K$. $A, B, Q, R$만 들어간다.
- 추정값을 참 상태처럼 다루는 **확실성 등가 제어기** $u_k = -K\hat x_k$.

두 이득을 따로 계산해도 결합이 여전히 최적이라는 것이 **분리 원리**이고, 그 극점판(폐루프 고유값이
$A - BK$의 고유값과 $A - LC$의 고유값을 합친 것)은 [[04-robotics/control-theory-ce397|5. 제어 이론 §8]]에서
유도한다. 해가 존재하려면 제어기 쪽에 $(A, B)$ 안정화 가능과 $(A, Q^{1/2})$ 검출 가능이, 필터 쪽에
그 쌍대 조건들이 필요하다. *예:* $A = B = C = 1$, $Q = R = W = V = 1$이면 두 리카티 방정식이 모두
$P^2 - P - 1 = 0$으로 줄어 LQR 이득과 정상 상태 칼만 이득이 모두 $0.618$이다. 쌍대성이 글자 그대로
드러난다.

분리 원리는 선형-가우시안 모델에서 정확하다 — 그리고 유명하게 취약하다: **LQG에는
보장된 강건성 여유가 없다** (Doyle 1978의 한 줄 초록: "there are none"; 이득·위상·안정 여유는
[[04-robotics/control-theory-ce397|5. 제어 이론 §5.5]]에서 정의한다). 추정 오차와 모델
오차가 상호작용한다; 실제 시스템은 여유 검사나 강건 변형을 다시 도입한다. "LQG를 쓴다"는
*공칭 최적, 강건성은 보이기 전까지 미검증*으로 읽어라.

**왜 공부하나**: LQR은 다른 모든 것을 재는 기준점이다 — [[04-robotics/mpc|MPC]]는 "제약을
더해 온라인으로 다시 푸는 LQR"이고(그 종단 비용 $P$가 보통 LQR 리카티 해다),
선형-이차 문제의 RL 정책 반복이나 정책 최적화는 LQR을 복원하며(평가만으로는 고정된 이득의 값만 매긴다), 궤적 주변의 시변 LQR은 학습된
플래너가 출력을 넘기는 표준 추종 제어기다.

**권장 경로**: EE363의 LQR 강의(이산 유한 지평, 라그랑주 승수, 무한 지평, 연속 시간 — 2026년 봄 목록의 16~19강) → Underactuated 해당 장(기하적
직관, 코드) → [[02-foundations/optimization|MPC-QP 예제]]로 연결.

### 연결

- 기초: [[02-foundations/linear-algebra|선형대수]] (리카티, 고유값), [[02-foundations/probability|확률]] (칼만), [[02-foundations/optimization|최적화]]
- 다음: [[04-robotics/mpc|MPC]]

### 이 안내 너머로

LQG의 추정기 쪽은 [[04-robotics/state-estimation-slam|상태 추정, 위치 인식, SLAM]]에서 전개한다.

### 스스로 점검 · Self-check

1. $(A,B)$가 안정화 가능하지 않으면 리카티 접근에 무슨 일이 생기나?
2. 이중 적분기에서 $Q$를 10배, $R$을 10배 함께 키우면 $K$는 어떻게 되나?
3. "LQG는 최적이므로 강건하다"가 틀린 이유를 한 문장으로.
4. MPC의 종단 비용으로 LQR의 $P$를 쓰는 이유는?

> [!tip]- 정답 · Answers
> 1. 불안정 모드를 어떤 피드백도 못 잡으므로 안정화 해 $P$가 존재하지 않는다 — 문제 자체가 불량이다.
> 2. 불변 — $Q$와 $R$ 전체에 같은 양의 스칼라를 곱하면 비용 스케일만 바뀐다. 행렬형 $Q,R$ 내부의 상대 가중치는 여전히 $K$를 정한다.
> 3. 최적성은 공칭 모델에 대한 것이고, LQG는 모델 오차에 대한 보장된 여유가 없음이 증명되어 있다(Doyle 1978).
> 4. LQR 법칙이 제약을 지키고 상태를 그 안에 머물게 하는 종단 집합 안에서는 $x^\top P x$가 남은 비용을 정확히 준다. 그 종단 제약을 함께 두어야 짧은 지평으로도 안정성 논증이 성립한다 — 종단 비용과 종단 집합이 함께 [[04-robotics/mpc|MPC §1]]이 나열하는 재료다(Borrelli 정리 12.2).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P4** $\dot x=-x+u+d$, $Q=1$, $R=1$. 시뮬레이터 없음.

1. **그리기.** $u=-Kx$인 새는 히터, $Q$와 $R$ 상자, 외란 $d$.
2. **유도.** 스칼라 리카티. 안정화 $P$와 $K$. $d=1$의 폐루프 극점과 $x_\mathrm{ss}$. CE397식 손 이득 $K=4$에서 같은 두 숫자.
3. **해석.** LQR의 $K$가 $K=4$보다 작은 이유, $Q/R$을 올리면 사고 치는 것(CE397 §1의 $(1+K)$ 거래).

> [!tip]- 정답 · Solutions
> 1. 플랜트 극점은 이미 $-1$; $Q$는 $x$, $R$은 $u$에 값을 매긴다.
> 2. $-2P-P^2+1=0\Rightarrow P=-1+\sqrt2\approx0.414$, $K\approx0.414$. 극점 $\approx-1.414$, $x_\mathrm{ss}\approx0.707$. $K=4$면 극점 $-5$, $x_\mathrm{ss}=0.2$.
> 3. 이미 안정한 플랜트에서 $Q=R=1$은 거의 안 움직인다. $K=4$는 손 선택(CE397 §1은 $10$배 억제에 $K=9$). $Q/R$을 올리면 $K$가 커져 $x_\mathrm{ss}$는 줄고 노력·잡음은 는다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] LQR 문제 설정과 해의 형태($u=-Kx$, $K=R^{-1}B^\top P$)를 말할 수 있다
- [ ] 안정화 가능성·검출 가능성이 각각 무엇을 보장하는 조건인지 말할 수 있다
- [ ] $Q/R$ 비율이 이득·응답·포화 위험을 어떻게 바꾸는지 예제로 말할 수 있다
- [ ] 분리 원리와 그 취약성(LQG 무여유), LQR이 MPC·RL의 기준점인 이유를 말할 수 있다
