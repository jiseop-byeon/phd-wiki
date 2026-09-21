---
title: "7. MPC"
tags: [robotics, control]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Key reference** — Mayne, Rawlings, Rao & Scokaert, *Constrained model predictive control: Stability and optimality*, Automatica 2000 · [DOI](https://doi.org/10.1016/S0005-1098(99)00214-9)

## English

*Group D. Stands on [[04-robotics/control-theory-ce397|5]] and [[04-robotics/lqr-lqg|6]]. Handling input and state constraints natively is its whole reason for existing
next to LQR, and [[04-robotics/convex-mpc-legged|8. Convex MPC]] is the application that made it standard on legged robots.*

> [!info] Depth target · 깊이 목표
> Read an MPC formulation (cost, horizon, constraints), identify what is solved online at each step, judge feasibility/stability claims, and recognize the standard failure modes. Solver internals are optional.
> MPC 정식화(비용·지평·제약)를 읽고, 매 스텝 온라인으로 무엇이 풀리는지 짚고, feasibility/안정성 주장을 판단하고, 표준 실패 모드를 알아볼 수 있으면 된다. 솔버 내부는 선택이다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/control-theory-ce397|5. Control Theory]] (state space, stability, and *why saturation breaks every linear guarantee* — the gap MPC exists to close) · [[04-robotics/lqr-lqg|6. LQR/LQG]] (its Riccati $P$ is MPC's usual terminal cost) · [[02-foundations/optimization|4. Optimization §2–5]] (convexity, KKT, and the MPC-as-QP example written out there)
> [[04-robotics/control-theory-ce397|5. 제어 이론]] (상태공간, 안정성, 그리고 *포화가 모든 선형 보장을 왜 깨는가* — MPC가 메우려는 그 간극) · [[04-robotics/lqr-lqg|6. LQR/LQG]] (그 리카티 $P$가 MPC의 표준 종단 비용) · [[02-foundations/optimization|4. 최적화 §2–5]] (볼록성, KKT, 거기 써 놓은 MPC-QP 예제)

**What it is**: **Model Predictive Control** solves, at every control step, a finite-horizon
optimal control problem from the current state, applies only the first input, and re-solves
at the next step (receding horizon). Written out, at time $t$, with measured (or estimated) state
$x(t)$, it solves

$$\min_{u_0,\ldots,u_{N-1}} \sum_{k=0}^{N-1} \ell(x_k, u_k) + V_f(x_N) \quad \text{s.t.} \quad x_{k+1} = f(x_k, u_k),\;\; x_k \in \mathcal X,\;\; u_k \in \mathcal U,\;\; x_N \in \mathcal X_f,\;\; x_0 = x(t)$$

and applies $u(t) = u_0^\star$, because only the first input is used before the next measurement
arrives and the whole problem is solved again. Its named components are the **prediction model**
$f$ (for linear MPC $f(x,u) = Ax + Bu$); the **horizon** $N$, the number of steps looked ahead;
the **stage cost** $\ell$ (for linear MPC $x^\top Q x + u^\top R u$); the **terminal cost** $V_f$,
which stands in for everything after step $N$ (typically $x^\top P x$ with the LQR $P$); the
**constraint sets** $\mathcal X$ and $\mathcal U$ for states and inputs; and the **terminal set**
$\mathcal X_f$ in which the prediction must end. *Non-example:* solving this once and executing the
whole sequence $u_0, \ldots, u_{N-1}$ is open-loop optimal control, not MPC; the re-solve from a new
measurement is what supplies the feedback. With linear dynamics, positive-semidefinite quadratic
state/terminal costs, a positive-definite input cost, and affine equality plus linear
inequality constraints, it is a convex QP — written out fully in
[[02-foundations/optimization|4. Optimization §5]]. More general convex constraints can
produce a convex program that is not a QP —
and constraints on inputs and states are handled *natively*, which is
MPC's whole advantage over [[04-robotics/lqr-lqg|LQR]].

**Worked: P4 with $|u|\le 1$.** The leaky heater $\dot x=-x+u+d$ ([[02-foundations/lab-plants|0.6]]). Unconstrained $100\times$ rejection wants $K=99$ (CE397 Self-check 1). At $x=0.5$ that law asks $u=-49.5$, which the rail $|u|\le 1$ forbids. Steady state $0=-x+u+d$ with $d=1$ and $|u|\le 1$ forces $x_\mathrm{ss}=u+1\in[0,2]$. Sitting at $d/(1+99)=0.01$ would need $u=-0.99$ *and* a transient that never asked for $|u|>1$, which $u=-99x$ does as soon as $|x|>1/99$. A receding horizon of length 3 on this plant, with only $u_0$ applied, exists *because* of that rail. LQR $K=99$ is not “almost MPC with a short horizon.” The problem set repeats the same arithmetic at $x=1$.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="receding horizon: plan over the horizon, execute one step, re-plan">
  <g stroke="currentColor" stroke-width="1" opacity="0.3">
    <line x1="30" y1="170" x2="440" y2="170"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.25" stroke-dasharray="2 4">
    <line x1="60" y1="20" x2="60" y2="170"/><line x1="100" y1="20" x2="100" y2="170"/><line x1="140" y1="20" x2="140" y2="170"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.45" stroke-dasharray="5 3">
    <path d="M60,120 C110,96 170,88 260,84"/>
    <path d="M100,110 C150,88 210,80 300,78"/>
    <path d="M140,100 C190,80 250,74 340,72"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="2.4">
    <path d="M60,120 L100,110"/><path d="M100,110 L140,100"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="120" r="3.5"/><circle cx="100" cy="110" r="3.5"/><circle cx="140" cy="100" r="3.5"/></g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="186">t</text><text x="90" y="186">t+1</text><text x="130" y="186">t+2</text>
    <text x="268" y="88" opacity="0.8">planned horizon (thrown away)</text>
    <text x="150" y="130">actually executed</text>
    <text x="30" y="16" opacity="0.9">each step: solve the whole horizon, keep only the first input, shift, solve again</text>
  </g>
</svg>



**The Mayne et al. 2000 survey** is the field's canonical reference: it settled *when MPC
is stable* — the roles of the terminal cost, terminal constraint set, and horizon length —
turning a practical heuristic into a theory. The mechanism has two parts, plus fine print:

- **(a) Recursive feasibility.** Suppose the horizon ends inside a **terminal set** that is
  *invariant* under a known local controller (invariant = once the state is inside that set,
  the controller keeps it inside forever, and the set lies inside the state constraints while
  that appended control stays inside the input constraints). In symbols, with $\kappa_f$ the local
  controller (usually the LQR law $-Kx$),
  $$x \in \mathcal X_f \implies f\big(x, \kappa_f(x)\big) \in \mathcal X_f, \qquad \mathcal X_f \subseteq \mathcal X, \qquad \kappa_f(x) \in \mathcal U \ \text{ for all } x \in \mathcal X_f$$
  so the three conditions say that the state stays in the set, the set respects the state
  constraints, and the local control respects the input constraints. Then a feasible plan today implies
  a feasible plan tomorrow: drop the first step and append one step of that controller. This
  is **recursive feasibility**, the property MPC papers invoke by name.
- **(b) Stability from a cost decrease.** Suppose also that the terminal cost decreases by
  **at least the stage cost** under that controller, so that
  $V_f(f(x,u)) - V_f(x) \le -\ell(x,u)$ with $u = \kappa_f(x)$, for every $x \in \mathcal X_f$
  (here $f$ is the prediction model, $\ell$ the stage cost and $V_f$ the terminal cost). Then the
  optimal cost becomes a Lyapunov function
  (a positive "energy" that strictly decreases along the closed loop, so the state must settle
  at the origin; the three defining conditions are in [[04-robotics/control-theory-ce397|5. Control Theory §4]]) and the origin is
  **asymptotically** stable, with the feasible set as its domain of attraction. The **feasible
  set** is the set of initial states for which at least one input sequence satisfies every
  constraint, and a **domain of attraction** is a set of initial states from which the closed loop
  converges to the origin. Merely
  decreasing is not enough; the decrease has to dominate the stage cost, and the conclusion
  holds only from states that were feasible to begin with.
- **Fine print.** That inequality is one assumption of four, not the whole hypothesis:
  Borrelli's Theorem 12.2 also requires the stage and terminal costs to be continuous and
  positive definite, the sets to be closed and to contain the origin in their interior, and
  the terminal set to be control invariant inside the state constraints. Rawlings adds a lower
  bound on the stage cost and a weak-controllability condition.

**Worked, on one scalar system.** Take $x_{k+1} = x_k + u_k$ with $|u_k| \le 1$, stage cost
$\ell = x^2 + u^2$, and the discrete LQR solution of [[04-robotics/lqr-lqg|6. LQR / LQG §1]]:
$V_f = 1.618\,x^2$ and $\kappa_f(x) = -0.618\,x$.
- *Terminal set.* $|\kappa_f(x)| \le 1$ exactly when $|x| \le 1.618$, and the next state
  $0.382\,x$ stays in that interval, so $\mathcal X_f = [-1.618,\ 1.618]$ is invariant.
- *Cost decrease.* $V_f(0.382x) - V_f(x) = -1.382\,x^2$ and $\ell(x, \kappa_f(x)) = x^2 + 0.382\,x^2 = 1.382\,x^2$,
  so condition (b) holds with equality, as it must when $V_f$ is the exact LQR cost-to-go.
- *Feasible set.* Each step moves the state by at most $1$, so with $N = 2$ the feasible set is
  $|x| \le 2 + 1.618 = 3.618$. From $x = 4$ the problem has no solution.
- *One step.* From $x = 3$, unconstrained LQR would command $-1.854$, which violates $|u| \le 1$.
  The MPC problem returns $u_0 = u_1 = -1$ (predicted $x_2 = 1 \in \mathcal X_f$, cost $16.62$),
  the plant receives $-1$, and the next problem starts from $x = 2$. The shifted plan
  $(-1,\ \kappa_f(1) = -0.618)$ ends at $0.382 \in \mathcal X_f$, so it is feasible, exactly as (a)
  promised.

Read the survey after the optimization page's example; skim its
formulation and stability sections rather than every proof.

> [!note] First pass · 처음이라면
> Read §1 (when the QP is actually convex), §3 (the failure modes papers gloss), §4. §2 — stacked versus condensed — is for when you implement or when a paper reports solve times.

### Homework diagram · 과제가 그릴 그림

The figure above draws receding horizon in the abstract. This is the version you must be able to
draw on **P4** from [[02-foundations/lab-plants|0.6 Lab Plants]], and the problem set asks for the
same one.

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="Receding horizon of length 3 on the leaky heater at x(t) = 0.5: predicted states above a time axis, three planned inputs pinned at the rail u = -1 inside the band from -1 to +1, the K = 99 demand of -49.5 far below it, d = 1 entering the plant unmeasured, the horizon re-planned from the new measurement, and the steady states [0, 2] the rails permit with 0.01 marked.">
  <defs><marker id="aMPC" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <rect x="24" y="30" width="120" height="34" rx="3"/>
    <circle cx="206" cy="47" r="10"/>
    <rect x="252" y="30" width="150" height="34" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" marker-end="url(#aMPC)">
    <line x1="144" y1="47" x2="194" y2="47"/>
    <line x1="206" y1="12" x2="206" y2="35"/>
    <line x1="216" y1="47" x2="250" y2="47"/>
    <polyline points="402,47 470,47 470,80 84,80 84,66"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="56" y1="210" x2="268" y2="210"/>
    <line x1="64" y1="206" x2="64" y2="214"/>
    <line x1="128" y1="206" x2="128" y2="214"/>
    <line x1="192" y1="206" x2="192" y2="214"/>
    <line x1="256" y1="206" x2="256" y2="214"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.45">
    <line x1="268" y1="210" x2="328" y2="210"/>
    <line x1="320" y1="206" x2="320" y2="214"/>
    <line x1="64" y1="200" x2="320" y2="200" stroke-dasharray="1 3"/>
  </g>
  <rect x="64" y="238" width="192" height="50" fill="currentColor" fill-opacity="0.10"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.7">
    <line x1="64" y1="238" x2="256" y2="238"/>
    <line x1="64" y1="288" x2="256" y2="288"/>
    <line x1="64" y1="263" x2="256" y2="263" stroke-dasharray="1 3"/>
  </g>
  <rect x="78" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="142" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="206" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <ellipse cx="96" cy="275.5" rx="27" ry="16" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <line x1="96" y1="291" x2="96" y2="302"/>
    <path d="M90 305 L102 301 M90 310 L102 306"/>
    <line x1="96" y1="309" x2="96" y2="356" marker-end="url(#aMPC)"/>
  </g>
  <polyline points="64,105 128,132.1 192,156.7 256,178.9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="128,114 192,140.3 256,164.1 320,185.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" stroke-opacity="0.45"/>
  <circle cx="64" cy="105" r="4" fill="currentColor"/>
  <circle cx="128" cy="132.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="156.7" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="256" cy="178.9" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="140.3" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="256" cy="164.1" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="320" cy="185.6" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="128" cy="114" r="4" fill="currentColor"/>
  <path d="M134 114 H137 V132.1 H134" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <line x1="137" y1="123.1" x2="196" y2="112" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <rect x="352" y="284" width="120" height="16" fill="currentColor" fill-opacity="0.22"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="338" y1="292" x2="492" y2="292"/>
    <line x1="352" y1="281" x2="352" y2="303"/>
    <line x1="412" y1="281" x2="412" y2="303"/>
    <line x1="472" y1="281" x2="472" y2="303"/>
  </g>
  <path d="M352.6 301 l-5 9 h10 z" fill="currentColor"/>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="84" y="44">MPC</text>
    <text x="84" y="58">N = 3, |u| ≤ 1</text>
    <text x="327" y="52" font-size="12">ẋ = −x + u + d</text>
    <text x="64" y="226">t</text>
    <text x="128" y="226">t+1</text>
    <text x="192" y="226">t+2</text>
    <text x="256" y="226">t+3</text>
    <text x="320" y="226" opacity="0.5">t+4</text>
    <text x="96" y="255">u₀</text>
    <text x="160" y="255">u₁</text>
    <text x="224" y="255">u₂</text>
    <text x="352" y="276">0</text>
    <text x="412" y="276">1</text>
    <text x="472" y="276">2</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="160" y="41">u₀</text>
    <text x="214" y="22">d = 1, not measured</text>
    <text x="462" y="76" text-anchor="end" opacity="0.85">measured x</text>
    <text x="58" y="95">x(t) = 0.5, measured</text>
    <text x="200" y="110">new measurement at t+1, above the predicted x₁:</text>
    <text x="200" y="124">that gap is the feedback (d = 1 is not in the model)</text>
    <text x="336" y="150" opacity="0.9">dashed: the plan, only step one runs</text>
    <text x="336" y="164" opacity="0.6">lighter: re-planned from the new x</text>
    <text x="58" y="242" text-anchor="end">u = +1</text>
    <text x="58" y="292" text-anchor="end">u = −1</text>
    <text x="58" y="204" text-anchor="end" opacity="0.7">x = 0</text>
    <text x="140" y="306" opacity="0.85">only u₀ reaches the plant</text>
    <text x="108" y="338">K = 99 asks u = −Kx = −49.5</text>
    <text x="108" y="352" opacity="0.85">far below the band (off scale)</text>
    <text x="318" y="248">steady states the rails permit</text>
    <text x="318" y="262">0 = −x + u + d ⇒ x<tspan font-size="9.5" dy="3">ss</tspan><tspan dy="-3" dx="1.5"> = u + 1 ∈ [0, 2]</tspan></text>
    <text x="318" y="326">0.01 = d/(1 + 99): reachable as a</text>
    <text x="318" y="340">steady state, not by u = −99x's transient</text>
    <text x="318" y="359" opacity="0.7" font-size="11">one step = 0.1 s (P4's catalog sampling)</text>
  </g>
</svg>

The figure is the worked case at the top of this page, $x(t)=0.5$, where the $K=99$ law asks $u=-49.5$, with the predicted dots stepped at P4's catalog sampling $T=0.1$ s; the paragraphs below and the problem set use $x=1$, where the arrow reaches $u=-99$.

**The axis and the prediction.** A time axis with four ticks, $t$ through $t+3$, so the $N=3$
horizon fits. Above it, the state: the measured $x(t)$ as a filled dot on the first tick, the
predicted $x_1,x_2,x_3$ as open dots, and a dashed curve through them — dashed, because only the
first segment is ever executed.

**The rail band.** Below the axis, the input: a shaded horizontal strip between $u=-1$ and $u=+1$
with both edges labelled. Draw the three planned inputs $u_0,u_1,u_2$ as bars inside that strip,
and circle $u_0$, the only one that reaches the plant. Then draw what the unconstrained gain asks
for as an arrow leaving the strip: at $x=1$ the law $u=-Kx$ with $K=99$ wants $u=-99$, far below
the band. That arrow is the whole reason this figure is not LQR's.

**The disturbance, and the steady states the rails leave.** Put $d=1$ on its own arrow into the
summing junction ahead of the plant box, never through the controller — the controller does not
measure it. Beside the figure draw a short $x$-axis and shade $[0,2]$ on it: with $|u|\le1$ and
$d=1$, setting $0=-x+u+d$ gives $x_\mathrm{ss}=u+1$, so that interval is every steady state the
rails permit. Mark $0.01$ inside it, the point the $K=99$ design was aiming at, and write the
distinction the problem set turns on beside the mark — reachable as a steady state, not reachable
by that law's transient.

**The shift.** Redraw the whole horizon one tick to the right in a lighter line, and start it from
the *new measurement* rather than from the $x_1$ you predicted. The gap between those two dots is
the feedback. A drawing in which they coincide has drawn open-loop optimal control, which is the
non-example at the top of this page.

### 1. When is the QP actually convex?

The "it's just a QP" claim carries conditions worth checking in any paper:

- **Cost**: $Q \succeq 0$, $R \succ 0$, terminal $P \succeq 0$ — the quadratic must be
  (semi)definite ([[02-foundations/linear-algebra|SPD, page 1 §3]]). An indefinite $Q$
  (e.g., from a learned cost) breaks convexity silently.
- **Dynamics**: linear (or linearized — then the QP is only an approximation whose quality
  decays away from the linearization point).
- **Constraints**: input/state sets must be convex (boxes, polytopes). **Obstacle-avoidance
  constraints are non-convex** — which is why collision-aware MPC papers either convexify
  locally (safe corridors) or leave the QP world entirely. A set is convex when the segment
  between any two of its points stays inside it (the definition, and the conditions for a convex
  problem, are in [[02-foundations/optimization|4. Optimization §2]]). The free space outside a
  unit-radius obstacle at the origin, $\lVert p\rVert \ge 1$, contains $(-1.5, 0)$ and $(1.5, 0)$
  but not their midpoint $(0, 0)$, so it fails that test.

### 2. What the solver actually sees

Two standard ways to write the same problem — papers assume you know which one they use:

- **Stacked (sparse) form**: keep all states $x_{0:N}$ and inputs $u_{0:N-1}$ as
  variables and add dynamics as equality constraints — a large, *sparse, banded* problem
  that interior-point solvers exploit; cost matrices sit in blocks along the diagonal.
- **Condensed form**: eliminate the states using $x_k = A^k x_0 + \sum_j A^{k-1-j}Bu_j$,
  leaving only $u_{0:N-1}$ — a smaller but *dense* QP whose conditioning can worsen with
  horizon length (powers of $A$, cost weights and input directions).

**Size it, so "large" and "small" stop being adjectives.** Take a quadruped centroidal MPC
of the kind [[04-robotics/convex-mpc-legged|convex MPC papers]] run: state $n_x = 13$
(position, orientation, their velocities, plus gravity), input $n_u = 12$ (a 3-vector force
at each of 4 feet), horizon $N = 10$.

| | variables | equality constraints | Hessian |
|---|---|---|---|
| **Stacked** | $(N{+}1)n_x + Nn_u = 143 + 120 = 263$ | $Nn_x+n_x = 130+13 = 143$ | $263\times263$, **banded** — mostly zeros |
| **Condensed** | $Nn_u = 120$ | none (dynamics substituted in) | $120\times120$, **generally dense** — up to 14,400 entries |

Condensed has under half the variables, which sounds decisive until you notice its Hessian is
dense: $120^2 = 14{,}400$ stored entries in a dense representation, against a stacked matrix whose nonzero count grows only
linearly in $N$. Doubling the horizon roughly doubles stacked storage at fixed state/input dimensions; it *quadruples* the
condensed Hessian's entry count and, because generic dense Cholesky factorization is cubic in the variable
count, multiplies that factorization work by about eight. The cubic growth is not forced by the
dense form: Axehill & Morari (*Systems & Control Letters* 61, 2012, Theorem 3) build a Cholesky
factor of the condensed Hessian from the Riccati recursion's quantities in $O(N^2)$, and note that
adding the eliminated states back as variables recovers the classical $O(N)$ Riccati solve. Rawlings, Mayne & Diehl §8.8.4 surveys condensing methods with this quadratic horizon dependence. And at 50 Hz the entire solve must finish inside **20 ms**, minus whatever state
estimation already spent — which is why this choice is a real engineering decision rather
than a stylistic one.

Rule of thumb when reading: long horizons and state constraints → stacked; short horizons,
input constraints only → condensed. (Large powers of $A$ can worsen conditioning. Stable dynamics help, but do not alone guarantee good conditioning: weights, controllability and scaling also matter. Storage and dense factorization counts are not guarantees about total solver runtime.)

**Count the initial state explicitly.** In the table, $x_0$ is retained as a variable, so its measured value requires another $n_x=13$ equality constraints in addition to the 130 dynamics equations. If you substitute the measured $x_0$ before forming the QP, remove both its 13 variables and those 13 constraints: the equivalent stacked formulation has 250 variables and 130 dynamics equalities. This bookkeeping changes the matrix dimensions, not the control problem.

**Follow one control step.** Read the current estimate, solve for the full sequence, apply only its first input, and measure again. The rest of the previous sequence is a prediction and perhaps a warm start; it is not a commitment to act open-loop for the whole horizon. A better plan from yesterday's state can be less useful than a modest plan from the current state. That is why timing belongs in the formulation rather than only in a runtime footnote.

### 3. The failure modes papers gloss over

- **Infeasibility**: a disturbance pushes the state where *no* input sequence satisfies
  the constraints — the solver returns nothing, and the controller must do *something*.
  Standard fix: **constraint softening** — replace hard state constraints with penalized
  slack variables $\sigma \ge 0$ (cost $+\rho\|\sigma\|$), allowing violations of the relaxed constraints at a cost. For a state bound $x_k \le x_{max}$ it reads
  $$x_k \le x_{max} + \sigma_k, \qquad \sigma_k \ge 0, \qquad \text{cost} = \textstyle\sum_k \ell(x_k, u_k) + V_f(x_N) + \rho \sum_k \sigma_k$$
  so a violation of size $\sigma_k$ is permitted but costs $\rho\,\sigma_k$; with this linear ($\ell_1$) penalty and $\rho$ larger than the constraint's Lagrange multiplier, the softened problem returns the hard-constrained solution whenever that one exists (an *exact penalty*). This does not guarantee feasibility if the remaining hard constraints conflict. Input (actuator) constraints stay hard, and the controller needs a defined fallback when no usable solution is available.
- **Model mismatch**: MPC optimizes the *model's* future; bias between model and plant
  turns "optimal" plans into repeated small errors that feedback (the re-solving itself)
  must absorb. Watch for papers quantifying this vs assuming it away.
- **Latency and rate**: the plan is computed from a state estimate that is stale by the
  solve time ([[04-robotics/robot-systems-deployment|systems page §3]]). **Warm starting**
  — initializing the solver from the previous solution shifted one step — is what makes
  high-rate MPC possible; cold-started NMPC at 100 Hz is a red flag.
- **Estimator coupling**: MPC consumes $\hat{x}$, not $x$
  ([[04-robotics/state-estimation-slam|estimation page]]) — estimator bias becomes
  systematic constraint violation.

### 4. Linear vs nonlinear vs contact

- **Linear MPC**: convex QP; solve times from microseconds to milliseconds *for
  small-to-moderate problems on modern CPUs* — always condition speed claims on problem
  size, solver, and hardware.
- **Nonlinear MPC (NMPC)**: sequential quadratic programming (SQP: solve a QP model of the problem at the current iterate, step, repeat, [[02-foundations/optimization|4. Optimization §4]]) or DDP-style solvers (differential dynamic programming: a second-order trajectory optimizer that alternates an LQR-like backward pass around the current trajectory with a forward rollout);
  local optima and initialization sensitivity return
  ([[04-robotics/planning-decision-making|planning §6]]).
- **Contact-implicit MPC**: contact mode switches make the problem non-smooth
  ([[04-robotics/contact-force-tactile|contact §1]]); the
  [[04-robotics/convex-mpc-legged|legged convex-MPC]] trick is to *pre-specify* the
  contact schedule so the remaining problem is convex — read that page as the
  representative escape route.

**Where it meets learning** (this wiki's angle):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]] is MPC with a *learned* model and CEM solver;
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]'s receding-horizon action
chunks borrow MPC's structure; learned-dynamics MPC for excavators is an active
construction-robotics direction ([[05-construction-robotics/earthmoving-heavy-machinery|stream 3]]).

> [!tip] Going deeper · 더 깊이
> Two free books, and they answer different questions. Rawlings, Mayne & Diehl, [*Model Predictive Control: Theory, Computation, and Design*](https://sites.engineering.ucsb.edu/~jbraw/mpc/) is where the stability and feasibility guarantees are proved in the most general setting — read it when a paper claims recursive feasibility and you want to know what it had to assume. Borrelli, Bemporad & Morari, [*Predictive Control for Linear and Hybrid Systems*](http://cse.lab.imtlucca.it/~bemporad/publications/papers/BBMbook.pdf) proves the same guarantees more compactly for the linear polytopic case this page uses (persistent feasibility in §12.3.1, asymptotic stability in §12.3.2, Theorem 12.2 on four assumptions), and the same book is also the computational reference: explicit MPC, the QP structure of §2, and hybrid formulations, which is the half that matters for §4's contact case.

### Self-check

1. You plug a learned cost matrix $Q$ into an MPC and the solver misbehaves. First thing to check?
2. Horizon $N=50$ with many state constraints — expect stacked or condensed? Why?
3. A disturbance pushes the state outside the constraint set. What happens under hard-constrained vs softened MPC?
4. A paper claims "our NMPC runs at 200 Hz." Name three things to check.

> [!tip]- Answers
> 1. Whether $Q \succeq 0$ — if indefinite, the QP is non-convex and solver behavior is undefined.
> 2. Stacked — its structured (Riccati or sparse) solve grows linearly in $N$, while generic dense factorization of the condensed form grows as $N^3$ (or $N^2$ with Axehill–Morari); the condensed Hessian is dense at every horizon and its conditioning can degrade through powers of $A$; and state constraints stay sparse in the stacked form.
> 3. Hard: infeasible — the solver returns no usable command and a separate fallback must act. Soft: slacks can return a penalized violation **if the remaining hard constraints are feasible**; softening selected constraints does not guarantee that control can continue.
> 4. ① Warm-started or cold? ② Problem size (horizon, state dimension) and solver? ③ Is 200 Hz solve time or end-to-end latency ([[04-robotics/robot-systems-deployment|frequency ≠ latency]])?

### Problem set · 과제

Tier B. **P4** from [[02-foundations/lab-plants|0.6]], horizon $N=3$, $|u|\le1$, $d=1$. No simulator.

1. **Draw.** Receding horizon of length 3 on the leaky heater. Mark the rails $|u|\le1$ and $d=1$ entering the plant.
2. **Derive.** Unconstrained $100\times$ rejection wants $K=99$ (CE397 Self-check 1). At $x=1$, what is $u=-Kx$? Why is that illegal here? Under $|u|\le1$ and $d=1$, what interval can $x_\mathrm{ss}$ sit in?
3. **Interpret.** Why LQR $K=99$ is not "almost MPC with a short horizon" on this plant.

> [!tip]- Solutions
> 1. Three predicted steps, only $u_0$ applied, rails at $\pm1$.
> 2. $u=-99$. The constraint $|u|\le1$ forbids it. Steady state $0=-x+u+d\Rightarrow x=u+1\in[0,2]$. Sitting at $d/(1+99)=0.01$ would need $u=-0.99$ *and* a transient that never asked for $|u|>1$, which $u=-99x$ does as soon as $|x|>1/99$.
> 3. MPC exists next to LQR *because* of the constraint. A huge unconstrained gain is not a feasible plan of any horizon.

### Continue beyond this guide

See [[04-robotics/planning-decision-making|Planning & Decision-Making]] for trajectory optimization, replanning, task planning, and planning under uncertainty.

### Connections

- Foundations: [[02-foundations/optimization|Optimization]] (QP, KKT), [[02-foundations/linear-algebra|Linear Algebra]]
- Previous: [[04-robotics/lqr-lqg|LQR/LQG]] · Next: [[04-robotics/convex-mpc-legged|Convex MPC for legged robots]]

### After reading

- [ ] Describe the receding-horizon procedure (solve → apply the first input → re-solve)
- [ ] State the conditions for a convex QP ($Q,R,P$ definiteness and affine/polyhedral constraints), distinguish it from a general convex program, and say where obstacle constraints break convexity
- [ ] Explain the stacked vs condensed trade-off, and infeasibility, constraint softening, and warm starting
- [ ] Name Mayne 2000's stability ingredients (terminal cost, terminal set, horizon) and where PlaNet and Diffusion Policy borrow MPC's structure

## 한국어

*[[04-robotics/control-theory-ce397|5]]·[[04-robotics/lqr-lqg|6]]번 위에 선다. D군이다. 입력·상태 제약을 태생적으로 다루는 것이 LQR 옆에 존재하는 이유이고,
[[04-robotics/convex-mpc-legged|8. Convex MPC]]가 이것을 보행 로봇의 표준으로 만든 응용이다.*

**무엇인가**: **모델 예측 제어**는 매 제어 주기마다 현재 상태에서 유한 지평 최적 제어
문제를 풀고, 첫 입력만 적용한 뒤, 다음 주기에 다시 푼다(receding horizon). 식으로 쓰면, 시각 $t$에서
측정한(또는 추정한) 상태 $x(t)$로부터 다음을 푼다.

$$\min_{u_0,\ldots,u_{N-1}} \sum_{k=0}^{N-1} \ell(x_k, u_k) + V_f(x_N) \quad \text{s.t.} \quad x_{k+1} = f(x_k, u_k),\;\; x_k \in \mathcal X,\;\; u_k \in \mathcal U,\;\; x_N \in \mathcal X_f,\;\; x_0 = x(t)$$

그리고 $u(t) = u_0^\star$를 적용한다. 다음 측정이 오기 전까지 쓰이는 것은 첫 입력뿐이고 문제 전체를
다시 풀기 때문이다. 이름 붙은 구성 요소는 **예측 모델** $f$(선형 MPC에서는 $f(x,u) = Ax + Bu$),
앞을 내다보는 스텝 수인 **지평** $N$, **단계 비용** $\ell$(선형 MPC에서는 $x^\top Q x + u^\top R u$),
$N$스텝 이후 전부를 대신하는 **종단 비용** $V_f$(보통 LQR의 $P$로 $x^\top P x$), 상태와 입력의
**제약 집합** $\mathcal X$와 $\mathcal U$, 그리고 예측이 끝나야 하는 **종단 집합** $\mathcal X_f$다.
*반례:* 이 문제를 한 번 풀고 시퀀스 $u_0, \ldots, u_{N-1}$ 전체를 실행하는 것은 MPC가 아니라 개루프
최적 제어다. 피드백을 공급하는 것은 새 측정에서 다시 푸는 일이다. 선형 동역학,
양의 준정부호 상태·종단 비용, 양의 정부호 입력 비용, 아핀 등식과 선형 부등식 제약이면 볼록
QP가 된다 — [[02-foundations/optimization|4. 최적화 §5]]에 완전히 써 놓았다. 더 일반적인 볼록
제약은 볼록 최적화 문제를 만들 수 있지만 반드시 QP인 것은 아니다. 입력·상태 제약을 *태생적으로* 다루는 것이
[[04-robotics/lqr-lqg|LQR]] 대비 MPC의 존재 이유다.

**계산: $|u|\le 1$인 P4.** 새는 히터 $\dot x=-x+u+d$([[02-foundations/lab-plants|0.6]]). 제약 없는 $100$배 억제는 $K=99$(CE397 스스로 점검 1). $x=0.5$에서 그 법칙은 $u=-49.5$를 요구하고 레일 $|u|\le 1$이 금지한다. 정상상태 $0=-x+u+d$, $d=1$, $|u|\le 1$이면 $x_\mathrm{ss}=u+1\in[0,2]$. $d/(1+99)=0.01$에 앉으려면 $u=-0.99$이면서 과도에서 $|u|>1$을 한 번도 안 물어야 하는데, $u=-99x$는 $|x|>1/99$이면 바로 묻는다. 이 플랜트에서 길이 3의 후퇴 지평이 있는 이유가 그 레일이다. LQR $K=99$는 “짧은 지평의 거의 MPC”가 아니다. 과제는 같은 산수를 $x=1$에서 반복한다.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="receding horizon: 지평 전체를 계획하고 한 스텝만 실행한 뒤 다시 계획">
  <g stroke="currentColor" stroke-width="1" opacity="0.3">
    <line x1="30" y1="170" x2="440" y2="170"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.25" stroke-dasharray="2 4">
    <line x1="60" y1="20" x2="60" y2="170"/><line x1="100" y1="20" x2="100" y2="170"/><line x1="140" y1="20" x2="140" y2="170"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.45" stroke-dasharray="5 3">
    <path d="M60,120 C110,96 170,88 260,84"/>
    <path d="M100,110 C150,88 210,80 300,78"/>
    <path d="M140,100 C190,80 250,74 340,72"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="2.4">
    <path d="M60,120 L100,110"/><path d="M100,110 L140,100"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="120" r="3.5"/><circle cx="100" cy="110" r="3.5"/><circle cx="140" cy="100" r="3.5"/></g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="186">t</text><text x="90" y="186">t+1</text><text x="130" y="186">t+2</text>
    <text x="268" y="88" opacity="0.8">계획된 지평(버려진다)</text>
    <text x="150" y="130">실제로 실행된 부분</text>
    <text x="30" y="16" opacity="0.9">매 주기: 지평 전체를 풀고, 첫 입력만 남기고, 한 칸 밀어 다시 푼다</text>
  </g>
</svg>



**Mayne et al. 2000 서베이**는 이 분야의 정본이다: *MPC가 언제 안정한가* — 종단 비용,
종단 제약 집합, 지평 길이의 역할 — 를 정리해 실용적 휴리스틱을 이론으로 만들었다.
메커니즘은 두 부분과 작은 글씨로 이루어진다:

- **(a) Recursive feasibility.** 지평의 끝이 알려진 국소 제어기 아래 *불변*인 **종단 집합**
  안에 떨어진다고 하자(불변 = 일단 상태가 그 집합 안에 들어오면 그 제어기가 영원히 그 안에
  잡아두고, 그 집합이 상태 제약 안에 있으며 이어 붙이는 입력도 입력 제약 안에 있다는 뜻).
  기호로는 국소 제어기를 $\kappa_f$(보통 LQR 법칙 $-Kx$)라 할 때
  $$x \in \mathcal X_f \implies f\big(x, \kappa_f(x)\big) \in \mathcal X_f, \qquad \mathcal X_f \subseteq \mathcal X, \qquad \kappa_f(x) \in \mathcal U \ \text{ for all } x \in \mathcal X_f$$
  이다. 세 조건은 차례로 상태가 집합 안에 머물고, 집합이 상태 제약을 지키고, 국소 제어가 입력 제약을
  지킨다는 말이다. 그러면 오늘의 실행 가능한 계획이 내일의 실행 가능한 계획을 함의한다: 첫 스텝을 떼어 내고
  그 제어기 한 스텝을 이어 붙이면 된다. 이것이 MPC 논문들이 이름으로 부르는
  성질(**recursive feasibility**)이다.
- **(b) 비용 감소에서 오는 안정성.** 또 종단 비용이 그 제어기 아래 **최소한 단계 비용만큼**
  감소한다고 하자, 즉 모든 $x \in \mathcal X_f$에서 $u = \kappa_f(x)$일 때
  $V_f(f(x,u)) - V_f(x) \le -\ell(x,u)$($f$는 예측 모델, $\ell$은 단계 비용, $V_f$는 종단 비용). 그러면 최적 비용이 리아푸노프
  함수(폐루프를 따라 계속 줄어드는 양의 "에너지"라서 상태가 원점에 자리 잡을 수밖에 없게
  만드는 함수; 세 정의 조건은 [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]에 있다)가 되고 원점이
  **점근적으로** 안정해진다. 그 흡인 영역은 실행 가능 집합이다. **실행 가능 집합**은 모든 제약을
  만족하는 입력 시퀀스가 하나라도 있는 초기 상태들의 집합이고, **흡인 영역**은 폐루프가 원점으로
  수렴하는 초기 상태들의 집합이다. 그냥 감소하는 것으로는
  부족하고 감소가 단계 비용을 압도해야 하며, 결론은 애초에 실행 가능했던 상태에서만 성립한다.
- **작은 글씨.** 그 부등식은 가정 넷 중 하나일 뿐이다. Borrelli의 정리 12.2는 단계 비용과
  종단 비용이 연속이고 양정부호일 것, 집합들이 닫혀 있고 원점을 내부에 포함할 것, 종단 집합이
  상태 제약 안에서 제어 불변일 것도 함께 요구하고, Rawlings는 단계 비용의 하한과 약한
  제어가능성 조건을 더한다.

**계산 예제, 스칼라 시스템 하나로.** $x_{k+1} = x_k + u_k$, $|u_k| \le 1$, 단계 비용 $\ell = x^2 + u^2$,
그리고 [[04-robotics/lqr-lqg|6. LQR / LQG §1]]의 이산 LQR 해 $V_f = 1.618\,x^2$, $\kappa_f(x) = -0.618\,x$를 쓰자.
- *종단 집합.* $|\kappa_f(x)| \le 1$은 정확히 $|x| \le 1.618$일 때이고 다음 상태 $0.382\,x$도 그 구간에
  머물므로, $\mathcal X_f = [-1.618,\ 1.618]$은 불변이다.
- *비용 감소.* $V_f(0.382x) - V_f(x) = -1.382\,x^2$이고 $\ell(x, \kappa_f(x)) = x^2 + 0.382\,x^2 = 1.382\,x^2$이므로
  조건 (b)가 등호로 성립한다. $V_f$가 정확한 LQR cost-to-go이면 그래야 한다.
- *실행 가능 집합.* 한 스텝에 상태가 최대 $1$만큼 움직이므로 $N = 2$면 실행 가능 집합은
  $|x| \le 2 + 1.618 = 3.618$이다. $x = 4$에서는 해가 없다.
- *한 스텝.* $x = 3$에서 제약 없는 LQR은 $|u| \le 1$을 어기는 $-1.854$를 명령한다. MPC 문제는
  $u_0 = u_1 = -1$을 돌려주고(예측 $x_2 = 1 \in \mathcal X_f$, 비용 $16.62$), 플랜트는 $-1$을 받으며,
  다음 문제는 $x = 2$에서 시작한다. 한 칸 민 계획 $(-1,\ \kappa_f(1) = -0.618)$은 $0.382 \in \mathcal X_f$에서
  끝나므로 실행 가능하다. (a)가 약속한 그대로다.

서베이는 최적화 페이지의 예제를 본 뒤에 읽되, 모든 증명보다는
정식화와 안정성 조건을 다룬 절들을 훑는 것을 권한다.

> [!note] 처음이라면 · First pass
> 먼저 §1(QP가 실제로 볼록한 조건), §3(논문이 얼버무리는 실패 모드), §4. §2의 stacked/condensed는 직접 구현하거나 논문이 풀이 시간을 보고할 때 읽어라.

### 과제가 그릴 그림 · Homework diagram

위 그림은 receding horizon을 추상적으로 그린 것이다. 여기 있는 것은
[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P4** 위에서 직접 그릴 수 있어야 하는 판이고,
과제가 요구하는 것도 같은 그림이다.

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="x(t) = 0.5인 새는 히터 위의 길이 3 후퇴 지평: 시간 축 위의 예측 상태, -1과 +1 사이 띠 안에서 레일 u = -1에 붙은 계획 입력 셋, 그 한참 아래의 K = 99 요구값 -49.5, 측정되지 않은 채 플랜트로 들어가는 d = 1, 새 측정값에서 다시 세운 지평, 레일이 허용하는 정상상태 [0, 2]와 0.01의 표시.">
  <defs><marker id="aMPCk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <rect x="24" y="30" width="120" height="34" rx="3"/>
    <circle cx="206" cy="47" r="10"/>
    <rect x="252" y="30" width="150" height="34" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" marker-end="url(#aMPCk)">
    <line x1="144" y1="47" x2="194" y2="47"/>
    <line x1="206" y1="12" x2="206" y2="35"/>
    <line x1="216" y1="47" x2="250" y2="47"/>
    <polyline points="402,47 470,47 470,80 84,80 84,66"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="56" y1="210" x2="268" y2="210"/>
    <line x1="64" y1="206" x2="64" y2="214"/>
    <line x1="128" y1="206" x2="128" y2="214"/>
    <line x1="192" y1="206" x2="192" y2="214"/>
    <line x1="256" y1="206" x2="256" y2="214"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.45">
    <line x1="268" y1="210" x2="328" y2="210"/>
    <line x1="320" y1="206" x2="320" y2="214"/>
    <line x1="64" y1="200" x2="320" y2="200" stroke-dasharray="1 3"/>
  </g>
  <rect x="64" y="238" width="192" height="50" fill="currentColor" fill-opacity="0.10"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.7">
    <line x1="64" y1="238" x2="256" y2="238"/>
    <line x1="64" y1="288" x2="256" y2="288"/>
    <line x1="64" y1="263" x2="256" y2="263" stroke-dasharray="1 3"/>
  </g>
  <rect x="78" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="142" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="206" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <ellipse cx="96" cy="275.5" rx="27" ry="16" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <line x1="96" y1="291" x2="96" y2="302"/>
    <path d="M90 305 L102 301 M90 310 L102 306"/>
    <line x1="96" y1="309" x2="96" y2="356" marker-end="url(#aMPCk)"/>
  </g>
  <polyline points="64,105 128,132.1 192,156.7 256,178.9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="128,114 192,140.3 256,164.1 320,185.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" stroke-opacity="0.45"/>
  <circle cx="64" cy="105" r="4" fill="currentColor"/>
  <circle cx="128" cy="132.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="156.7" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="256" cy="178.9" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="140.3" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="256" cy="164.1" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="320" cy="185.6" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="128" cy="114" r="4" fill="currentColor"/>
  <path d="M134 114 H137 V132.1 H134" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <line x1="137" y1="123.1" x2="196" y2="112" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <rect x="352" y="284" width="120" height="16" fill="currentColor" fill-opacity="0.22"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="338" y1="292" x2="492" y2="292"/>
    <line x1="352" y1="281" x2="352" y2="303"/>
    <line x1="412" y1="281" x2="412" y2="303"/>
    <line x1="472" y1="281" x2="472" y2="303"/>
  </g>
  <path d="M352.6 301 l-5 9 h10 z" fill="currentColor"/>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="84" y="44">MPC</text>
    <text x="84" y="58">N = 3, |u| ≤ 1</text>
    <text x="327" y="52" font-size="12">ẋ = −x + u + d</text>
    <text x="64" y="226">t</text>
    <text x="128" y="226">t+1</text>
    <text x="192" y="226">t+2</text>
    <text x="256" y="226">t+3</text>
    <text x="320" y="226" opacity="0.5">t+4</text>
    <text x="96" y="255">u₀</text>
    <text x="160" y="255">u₁</text>
    <text x="224" y="255">u₂</text>
    <text x="352" y="276">0</text>
    <text x="412" y="276">1</text>
    <text x="472" y="276">2</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="160" y="41">u₀</text>
    <text x="214" y="22">d = 1, 측정 안 됨</text>
    <text x="462" y="76" text-anchor="end" opacity="0.85">측정한 x</text>
    <text x="58" y="95">x(t) = 0.5, 측정값</text>
    <text x="200" y="110">t+1의 새 측정값은 예측한 x₁보다 위에 있다:</text>
    <text x="200" y="124">그 간격이 피드백이다 (모델에는 d = 1이 없다)</text>
    <text x="336" y="150" opacity="0.9">파선: 계획, 실행되는 것은 첫 스텝뿐</text>
    <text x="336" y="164" opacity="0.6">옅은 선: 새 x에서 다시 세운 계획</text>
    <text x="58" y="242" text-anchor="end">u = +1</text>
    <text x="58" y="292" text-anchor="end">u = −1</text>
    <text x="58" y="204" text-anchor="end" opacity="0.7">x = 0</text>
    <text x="140" y="306" opacity="0.85">플랜트에 닿는 것은 u₀뿐</text>
    <text x="108" y="338">K = 99는 u = −Kx = −49.5를 요구</text>
    <text x="108" y="352" opacity="0.85">띠보다 한참 아래 (축척 밖)</text>
    <text x="318" y="248">레일이 허용하는 정상상태</text>
    <text x="318" y="262">0 = −x + u + d ⇒ x<tspan font-size="9.5" dy="3">ss</tspan><tspan dy="-3" dx="1.5"> = u + 1 ∈ [0, 2]</tspan></text>
    <text x="318" y="326">0.01 = d/(1 + 99): 정상상태로는</text>
    <text x="318" y="340">도달 가능, u = −99x의 과도 구간으로는 불가</text>
    <text x="318" y="359" opacity="0.7" font-size="11">한 스텝 = 0.1초 (P4 카탈로그 샘플링)</text>
  </g>
</svg>

그림은 이 페이지 첫머리의 계산 $x(t)=0.5$를 그린 것이다. 거기서 $K=99$ 법칙은 $u=-49.5$를 요구하고, 예측 점은 P4 카탈로그의 샘플링 $T=0.1$초 간격으로 찍었다. 아래 문단과 과제는 $x=1$을 쓰며, 그때 화살표는 $u=-99$에 닿는다.

**축과 예측.** 눈금이 넷($t$부터 $t+3$까지)인 시간 축을 그어 $N=3$ 지평이 들어가게 한다. 축
위쪽에는 상태를 그린다. 첫 눈금에 측정값 $x(t)$를 채운 점으로, 예측값 $x_1,x_2,x_3$를 빈 점으로,
그리고 그 점들을 지나는 파선. 파선인 이유는 실제로 실행되는 것이 첫 구간뿐이기 때문이다.

**레일 띠.** 축 아래쪽에는 입력을 그린다. $u=-1$과 $u=+1$ 사이를 칠한 수평 띠를 놓고 양쪽 가장자리에
값을 적는다. 계획된 입력 $u_0,u_1,u_2$를 그 띠 안의 막대로 그리고, 플랜트에 실제로 닿는 $u_0$에
동그라미를 친다. 그다음 제약 없는 이득이 요구하는 값을 띠 밖으로 나가는 화살표로 그린다. $x=1$에서
$K=99$인 $u=-Kx$는 $u=-99$를 원하고, 이는 띠보다 한참 아래다. 그 화살표가 이 그림이 LQR의 그림이
아닌 이유 전부다.

**외란, 그리고 레일이 남겨 주는 정상상태.** $d=1$은 제어기를 거치지 않고 플랜트 상자 앞 합산점으로
바로 들어가는 별도 화살표로 그린다 — 제어기는 그것을 측정하지 않는다. 그림 옆에는 짧은 $x$축을 긋고
$[0,2]$를 칠한다. $|u|\le1$, $d=1$에서 $0=-x+u+d$이면 $x_\mathrm{ss}=u+1$이므로, 그 구간이 레일이
허용하는 모든 정상상태다. 그 안에 $K=99$ 설계가 노리던 점 $0.01$을 찍고, 과제가 갈라 보는 구분을
옆에 적는다 — 정상상태로는 도달 가능하지만 그 법칙의 과도 구간으로는 도달할 수 없다.

**한 칸 밀기.** 마지막으로 지평 전체를 한 눈금 오른쪽에 옅은 선으로 다시 그리되, 예측했던 $x_1$이
아니라 *새 측정값*에서 출발시킨다. 두 점 사이의 간격이 곧 피드백이다. 그 둘이 겹치게 그린 그림은
개루프 최적 제어를 그린 것이며, 그것이 이 페이지 첫머리의 반례다.

### 1. QP는 언제 실제로 볼록한가?

"그냥 QP다"라는 주장에는 논문에서 확인할 조건들이 붙어 있다:

- **비용**: $Q \succeq 0$, $R \succ 0$, 종단 $P \succeq 0$ — 이차형식이 (준)정부호여야
  한다 ([[02-foundations/linear-algebra|SPD, 1페이지 §3]]). (학습된 비용 등에서 나온)
  부정부호 $Q$는 볼록성을 조용히 깨뜨린다.
- **동역학**: 선형(또는 선형화 — 이 경우 QP는 선형화 지점에서 멀어질수록 품질이 떨어지는
  근사일 뿐이다).
- **제약**: 입력/상태 집합이 볼록해야 한다(박스, 폴리토프). **장애물 회피 제약은
  비볼록이다** — 충돌 인지 MPC 논문들이 국소 볼록화(안전 통로)를 하거나 아예 QP 세계를
  떠나는 이유다. 집합은 그 안의 두 점을 잇는 선분이 집합 안에 머물 때 볼록하다(정의와 볼록 문제의
  조건은 [[02-foundations/optimization|4. 최적화 §2]]). 원점에 있는 반지름 1 장애물 바깥의 자유 공간
  $\lVert p\rVert \ge 1$은 $(-1.5, 0)$과 $(1.5, 0)$을 담지만 그 중점 $(0, 0)$은 담지 않으므로 이 검사에
  실패한다.

### 2. 솔버가 실제로 보는 것

같은 문제를 쓰는 표준적인 두 방식 — 논문은 독자가 어느 쪽인지 안다고 가정한다:

- **Stacked (희소) 형태**: 모든 상태 $x_{0:N}$과 입력 $u_{0:N-1}$을 변수로 두고 동역학을
  등식 제약으로 추가 — 크지만 *희소·띠 구조*라 내부점 솔버가 활용한다; 비용 행렬이
  대각 블록으로 놓인다.
- **Condensed (축약) 형태**: $x_k = A^k x_0 + \sum_j A^{k-1-j}Bu_j$로 상태를 소거해
  $u_{0:N-1}$만 남긴다 — 작지만 *조밀*하고, 지평이 길어지며($A$의 거듭제곱, 비용 가중치, 입력 방향) 조건수가
  나빠질 수 있다.

**크기를 재 보자 — 그래야 "크다"와 "작다"가 형용사에서 벗어난다.**
[[04-robotics/convex-mpc-legged|convex MPC 논문]]들이 돌리는 사족보행 centroidal MPC로 예를
들면: 상태 $n_x = 13$(위치, 자세, 그 속도들, 그리고 중력), 입력 $n_u = 12$(발 4개 각각의
3차원 힘), 지평 $N = 10$.

| | 변수 | 등식 제약 | 헤시안 |
|---|---|---|---|
| **Stacked** | $(N{+}1)n_x + Nn_u = 143 + 120 = 263$ | $Nn_x+n_x = 130+13 = 143$ | $263\times263$, **띠 구조** — 대부분 0 |
| **Condensed** | $Nn_u = 120$ | 없음(동역학을 대입해 소거) | $120\times120$, **일반적으로 밀집** — 최대 14,400개 성분 |

Condensed는 변수가 절반 이하라 결정적으로 보이지만, 헤시안이 밀집이라는 점을 보면 달라진다:
조밀하게 저장하면 원소가 $120^2 = 14{,}400$개인 반면 stacked의 비영 성분은 $N$에 대해 선형으로만 늘어난다.
고정 상태·입력 차원에서 지평을 두 배로 하면 stacked 저장량은 대략 두 배가 되고, condensed는 헤시안 *원소 수*가 네 배가 되며, 조밀 분해가 변수 수의 3제곱이므로 조밀 분해 연산량은 약 여덟 배가 된다. 다만 3제곱은 범용 Cholesky 분해의 경우이고, 조밀 형태가 강제하는 것은 아니다: Axehill과 Morari(*Systems & Control Letters* 61, 2012, 정리 3)는 Riccati 재귀의 양들로 condensed 헤시안의 Cholesky 인자를 $O(N^2)$에 만들고, 소거한 상태를 다시 변수로 넣으면 고전적인 $O(N)$ Riccati 풀이로 돌아간다고 적는다. Rawlings, Mayne, Diehl §8.8.4도 이런 이차 지평 의존도의 condensing 방법들을 정리한다. 그리고 50 Hz라면
이 풀이 전체가 **20 ms** 안에 끝나야 하고, 거기서 상태 추정이 이미 쓴 시간을 빼야 한다 —
이 선택이 취향이 아니라 실제 엔지니어링 결정인 이유다.

읽을 때의 어림 규칙: 긴 지평 + 상태 제약 → stacked; 짧은 지평 + 입력 제약만 → condensed.
($A$의 큰 거듭제곱은 조건수를 나쁘게 만들 수 있다. 안정 동역학은 유리하지만 가중치·제어 가능성·스케일도 중요하므로 그것만으로 좋은 조건수를 보장하지는 않는다. 저장량과 조밀 분해 연산량은 전체 솔버 시간의 보장이 아니다.)

**초기 상태를 명시적으로 센다.** 표에서는 $x_0$도 변수이므로 측정값에 고정하는 $n_x=13$개 등식이 동역학 130개 외에 필요하다. QP를 만들기 전에 측정한 $x_0$를 대입하면 변수 13개와 고정 등식 13개를 함께 뺀다. 같은 문제를 변수 250개, 동역학 등식 130개로 쓸 수 있다. 행렬 크기의 장부가 달라질 뿐 제어 문제는 같다.

**한 제어 주기를 따라간다.** 현재 추정값을 읽고, 전체 입력 시퀀스를 풀고, 첫 입력만 적용한 뒤 다시 측정한다. 이전 시퀀스의 나머지는 예측이자 warm start 후보이며, 전체 지평 동안 그대로 실행하겠다는 약속이 아니다. 오래된 상태의 훌륭한 계획보다 현재 상태의 평범한 계획이 유용할 수 있다. 시간이 부록의 실행 속도 수치가 아니라 문제 구성에 들어가는 이유다.

### 3. 논문이 얼버무리는 실패 모드

- **Infeasibility**: 외란이 상태를 *어떤* 입력 시퀀스로도 제약을 만족할 수 없는 곳으로
  밀면 — 솔버는 아무것도 돌려주지 않고, 제어기는 *뭐라도* 해야 한다. 표준 처방:
  **제약 연화(constraint softening)** — 딱딱한 상태 제약을 벌점 붙은 슬랙 변수
  $\sigma \ge 0$(비용 $+\rho\|\sigma\|$)로 바꿔, 연화한 제약을 비용을 치르고 위반하도록 허용한다. 상태 한계 $x_k \le x_{max}$라면
  $$x_k \le x_{max} + \sigma_k, \qquad \sigma_k \ge 0, \qquad \text{cost} = \textstyle\sum_k \ell(x_k, u_k) + V_f(x_N) + \rho \sum_k \sigma_k$$
  이다. 크기 $\sigma_k$의 위반이 허용되지만 $\rho\,\sigma_k$만큼 비용이 붙는다. 이 선형($\ell_1$) 벌점에서 $\rho$가 그 제약의 라그랑주 승수보다 크면, 경성 제약 해가 존재할 때 연화한 문제도 그 해를 돌려준다(*정확한 벌점*). 남은 경성 제약이 충돌하면 여전히 해가 없을 수 있다. 입력(액추에이터) 제약은 경성으로 유지하며, 쓸 수 있는 해가 없을 때의 대체 동작도 정해야 한다.
- **모델 불일치**: MPC는 *모델의* 미래를 최적화한다; 모델과 플랜트의 편차는 "최적" 계획을
  피드백(재풀이 자체)이 흡수해야 하는 반복적 소오차로 바꾼다. 이를 정량화하는 논문과
  가정으로 치우는 논문을 구분하라.
- **지연과 주기**: 계획은 풀이 시간만큼 낡은 상태 추정에서 계산된다
  ([[04-robotics/robot-systems-deployment|시스템 페이지 §3]]). **Warm start** — 이전 해를
  한 스텝 밀어 솔버를 초기화 — 가 고주기 MPC를 가능하게 하는 것이다; 100 Hz의 cold-start
  NMPC는 적신호다.
- **추정기 결합**: MPC는 $x$가 아니라 $\hat{x}$를 소비한다
  ([[04-robotics/state-estimation-slam|추정 페이지]]) — 추정기 편향은 계통적 제약 위반이
  된다.

### 4. 선형 vs 비선형 vs 접촉

- **선형 MPC**: 볼록 QP; *현대 CPU에서 중소 규모 문제라면* 마이크로초~밀리초의 풀이
  시간 — 속도 주장은 항상 문제 크기·솔버·하드웨어를 조건으로 달아 읽어라.
- **비선형 MPC (NMPC)**: SQP(현재 반복점에서 문제의 QP 모델을 풀고, 한 스텝 가고, 반복한다, [[02-foundations/optimization|4. 최적화 §4]]) 또는 DDP류 솔버(differential dynamic programming: 현재 궤적 주위에서 LQR 같은 역방향 패스와 순방향 롤아웃을 번갈아 도는 2차 궤적 최적화기); 국소 최적과 초기화 민감성이 돌아온다
  ([[04-robotics/planning-decision-making|계획 §6]]).
- **접촉 내재 MPC**: 접촉 모드 전환이 문제를 비매끄럽게 만든다
  ([[04-robotics/contact-force-tactile|접촉 §1]]);
  [[04-robotics/convex-mpc-legged|보행 convex MPC]]의 트릭은 접촉 스케줄을 *미리 지정*해
  남는 문제를 볼록하게 만드는 것 — 대표적 탈출로로 그 페이지를 읽어라.

**학습과 만나는 지점** (이 위키의 관심사):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]]은 *학습된* 모델과 CEM 솔버의 MPC이고,
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]의 receding-horizon 행동
청크는 MPC의 구조를 빌린 것이며, 굴착기의 학습 동역학 MPC는 건설로봇의 활발한 연구
방향이다 ([[05-construction-robotics/earthmoving-heavy-machinery|스트림 3]]).

### 연결

- 기초: [[02-foundations/optimization|최적화]] (QP, KKT), [[02-foundations/linear-algebra|선형대수]]
- 이전: [[04-robotics/lqr-lqg|LQR/LQG]] · 다음: [[04-robotics/convex-mpc-legged|보행 로봇의 convex MPC]]

### 이 안내 너머로

궤적 최적화, 재계획, 과제 계획, 불확실성 하의 계획은 [[04-robotics/planning-decision-making|계획과 의사결정]]에서 다룬다.

> [!tip] 더 깊이 · Going deeper
> 무료 책이 둘이고, 서로 다른 질문에 답한다. Rawlings, Mayne, Diehl의 [*Model Predictive Control: Theory, Computation, and Design*](https://sites.engineering.ucsb.edu/~jbraw/mpc/)은 안정성과 실현가능성 보장이 가장 일반적인 설정에서 증명되는 곳이다 — 논문이 재귀적 실현가능성을 주장할 때 그것이 무엇을 가정해야 했는지 알고 싶다면 이 책이다. Borrelli, Bemporad, Morari의 [*Predictive Control for Linear and Hybrid Systems*](http://cse.lab.imtlucca.it/~bemporad/publications/papers/BBMbook.pdf)는 이 페이지가 쓰는 선형 폴리토프 경우에 같은 보장을 더 짧게 증명하고(지속 실현가능성 §12.3.1, 점근 안정성 §12.3.2, 가정 네 개의 정리 12.2), 같은 책이 계산 쪽 참고서이기도 하다: explicit MPC, §2의 QP 구조, 그리고 하이브리드 정식화 — §4의 접촉 사례에 중요한 절반이 그쪽이다.

### 스스로 점검 · Self-check

1. 학습된 비용 행렬 $Q$를 MPC에 꽂았더니 솔버가 이상하게 군다. 가장 먼저 확인할 것은?
2. 지평 $N=50$, 상태 제약이 많은 문제 — stacked와 condensed 중 무엇을 기대해야 하나? 왜?
3. 외란으로 상태가 제약 밖으로 밀렸다. 하드 제약 MPC와 소프트 제약 MPC는 각각 어떻게 되나?
4. "우리 NMPC는 200 Hz로 돈다"라는 주장에서 확인할 세 가지는?

> [!tip]- 정답 · Answers
> 1. $Q \succeq 0$인지 — 부정부호면 QP가 비볼록이 되어 솔버 거동이 정의되지 않는다.
> 2. Stacked — 구조화된(리카티 또는 희소) 풀이는 $N$에 선형으로 늘지만, condensed 형태의 범용 조밀 분해는 $N^3$(Axehill–Morari를 쓰면 $N^2$)으로 는다. condensed 헤시안은 지평과 무관하게 조밀하고, $A$의 거듭제곱 때문에 조건수가 나빠질 수 있으며, 상태 제약은 stacked에서 희소하게 남는다.
> 3. 하드: infeasible — 솔버가 쓸 수 있는 명령을 반환하지 않아 별도의 폴백이 필요. 소프트: **남은 하드 제약이 feasible할 때** 슬랙으로 벌점 있는 위반 해를 반환할 수 있다. 일부 제약을 연화한다고 제어 지속이 보장되지는 않는다.
> 4. ① warm start 여부 ② 문제 크기(지평·상태 차원)와 솔버 ③ 그 200 Hz가 풀이 시간인지 끝-끝 지연인지 ([[04-robotics/robot-systems-deployment|주파수 ≠ 지연]]).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P4**, 지평 $N=3$, $|u|\le1$, $d=1$. 시뮬레이터 없음.

1. **그리기.** 새는 히터의 길이 3 receding horizon. 레일 $|u|\le1$과 플랜트로 들어가는 $d=1$.
2. **유도.** 제약 없는 $100$배 억제는 $K=99$(CE397 스스로 점검 1). $x=1$에서 $u=-Kx$는? 여기서 왜 불법인가? $|u|\le1$, $d=1$이면 $x_\mathrm{ss}$가 앉을 수 있는 구간은?
3. **해석.** 이 플랜트에서 LQR $K=99$가 "짧은 지평 MPC와 거의 같다"가 아닌 이유.

> [!tip]- 정답 · Solutions
> 1. 예측 세 스텝, 적용은 $u_0$만, 레일 $\pm1$.
> 2. $u=-99$. $|u|\le1$이 금지. 정상상태 $x=u+1\in[0,2]$. $0.01$에 앉으려면 $u=-0.99$이고 과도에서 $|u|>1$을 한 번도 안 물어야 하는데, $u=-99x$는 $|x|>1/99$이면 바로 위반한다.
> 3. MPC가 LQR 옆에 있는 이유가 제약이다. 거대한 무제약 이득은 어떤 지평의 가능 계획도 아니다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] receding horizon 절차(풀고 → 첫 입력만 적용하고 → 다시 푼다)를 말할 수 있다
- [ ] 볼록 QP의 조건($Q,R,P$의 정부호성과 아핀·다면체 제약)과 일반 볼록 최적화의 차이, 장애물 제약이 볼록성을 깨뜨리는 지점을 말할 수 있다
- [ ] stacked/condensed 정식화의 트레이드오프와 infeasibility·softening·warm start를 설명할 수 있다
- [ ] Mayne 2000의 안정성 재료(종단 비용·종단 집합·지평)와 PlaNet·Diffusion Policy가 MPC 구조를 빌린 지점을 말할 수 있다
