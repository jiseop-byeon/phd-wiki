---
title: 4. Optimization
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> Plant **P1** from [[02-foundations/lab-plants|0.6 Lab Plants]] · [[02-foundations/engineering-math|0.5 §1–2]] (gradients, Taylor) · [[02-foundations/linear-algebra|1. Linear Algebra §3]] (eigenvalues, SPD, condition number) · [[02-foundations/calculus-backprop|2. Calculus §1]] (the Hessian) · [[02-foundations/probability|3. Probability §2]] (expectation, for §3's stochastic gradients)
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P1** · [[02-foundations/engineering-math|0.5 §1–2]](그래디언트·테일러) · [[02-foundations/linear-algebra|1. 선형대수 §3]](고유값·SPD·조건수) · [[02-foundations/calculus-backprop|2. 미적분 §1]](헤시안) · [[02-foundations/probability|3. 확률 §2]](기댓값, §3의 확률적 그래디언트용)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/calculus-backprop|2. Calculus]] — gradients and Taylor. First of the two applied pillars: it minimizes the objective,
constraints included, and it is where network training, MPC, trajectory planning and task allocation become one sentence.*

Optimization is the shared language of this wiki: training a network
([[01-canonical-papers/notes/1-foundations/adam|Adam]]), solving MPC, planning a trajectory, and allocating
construction tasks are all "minimize an objective subject to constraints." Course-depth
treatment: conditions, derivations, and a fully written MPC-as-QP example.

> [!note] First pass · 처음이라면
> Read the picture, §1, then §2 — convexity is the fork everything else hangs on — then §3, whose P1 step is the picture's arithmetic. Open §4 the first time a paper says "subject to"; KKT reads much better with a concrete constraint in front of you. §3.5 is for when a SLAM, calibration or IK paper says "we optimize" — read it with such a paper in hand. §5 is a table of problem classes to look things up in, and §6 is a one-screen map of where this page reappears in the wiki; skim both.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 482" style="max-width:100%;height:auto" role="img" aria-label="Loss against the single weight W2,1: a parabola with vertex at 1.5; the catalog point at 1 with height 0.125 and slope -0.5; the eta = 0.1 step to 1.05 drawn to scale beside the 0.5 still to go; step sizes 1 and 2 marked on the axis; below, the eta = 10 step to 6 on a broken axis, with 2415.1 for the full step">
  <defs><marker id="aOp" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <line x1="60" y1="214" x2="530" y2="214" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="60" y1="214" x2="60" y2="30" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="548" y="230" font-size="11" fill="currentColor" text-anchor="end">W<tspan dy="3" font-size="9.5">2,1</tspan></text>
  <text x="53" y="24" font-size="11" fill="currentColor" text-anchor="end">L</text>
  <line x1="85.6" y1="214" x2="85.6" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="85.6" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="213.3" y1="214" x2="213.3" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="213.3" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="341.1" y1="214" x2="341.1" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="341.1" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.5</text>
  <line x1="468.9" y1="214" x2="468.9" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="468.9" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2</text>
  <line x1="56" y1="154" x2="60" y2="154" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="158" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.2</text>
  <line x1="56" y1="94" x2="60" y2="94" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="98" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.4</text>
  <line x1="56" y1="34" x2="60" y2="34" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="38" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.6</text>
  <text x="53" y="218" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <path d="M60 32.5 L63.8 37.4 L67.7 42.3 L71.5 47 L75.3 51.8 L79.2 56.4 L83 61 L86.8 65.5 L90.7 69.9 L94.5 74.3 L98.3 78.6 L102.2 82.9 L106 87 L109.8 91.1 L113.7 95.2 L117.5 99.2 L121.3 103.1 L125.2 106.9 L129 110.7 L132.8 114.4 L136.7 118 L140.5 121.6 L144.3 125.1 L148.2 128.5 L152 131.9 L155.8 135.2 L159.7 138.4 L163.5 141.5 L167.3 144.6 L171.2 147.7 L175 150.6 L178.8 153.5 L182.7 156.3 L186.5 159.1 L190.3 161.8 L194.2 164.4 L198 167 L201.8 169.4 L205.7 171.9 L209.5 174.2 L213.3 176.5 L217.2 178.7 L221 180.9 L224.8 182.9 L228.7 185 L232.5 186.9 L236.3 188.8 L240.2 190.6 L244 192.3 L247.8 194 L251.7 195.6 L255.5 197.2 L259.3 198.6 L263.2 200 L267 201.4 L270.8 202.7 L274.7 203.9 L278.5 205 L282.3 206.1 L286.2 207.1 L290 208 L293.8 208.9 L297.7 209.7 L301.5 210.4 L305.3 211.1 L309.2 211.7 L313 212.2 L316.8 212.6 L320.7 213 L324.5 213.4 L328.3 213.6 L332.2 213.8 L336 213.9 L339.8 214 L343.7 214 L347.5 213.9 L351.3 213.8 L355.2 213.5 L359 213.3 L362.8 212.9 L366.7 212.5 L370.5 212 L374.3 211.5 L378.2 210.8 L382 210.2 L385.8 209.4 L389.7 208.6 L393.5 207.7 L397.3 206.7 L401.2 205.7 L405 204.6 L408.8 203.5 L412.7 202.2 L416.5 200.9 L420.3 199.6 L424.2 198.2 L428 196.7 L431.8 195.1 L435.7 193.5 L439.5 191.8 L443.3 190 L447.2 188.2 L451 186.3 L454.8 184.3 L458.7 182.3 L462.5 180.2 L466.3 178 L470.2 175.7 L474 173.4 L477.8 171.1 L481.7 168.6 L485.5 166.1 L489.3 163.5 L493.2 160.9 L497 158.2 L500.8 155.4 L504.7 152.6 L508.5 149.6 L512.3 146.7 L516.2 143.6 L520 140.5" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <circle cx="341.1" cy="214" r="3.5" stroke="none" fill="currentColor"/>
  <text x="347.1" y="192" font-size="11" fill="currentColor" fill-opacity="0.85">vertex (1.5, 0)</text>
  <line x1="141.8" y1="134.5" x2="277.2" y2="214" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" stroke-dasharray="5 3"/>
  <text x="74" y="160" font-size="11" fill="currentColor">tangent slope</text>
  <text x="74" y="175" font-size="11" fill="currentColor">1 − 1.5 = −0.5</text>
  <line x1="213.3" y1="176.5" x2="226.6" y2="176.5" stroke="currentColor" stroke-width="1.3" marker-end="url(#aOp)"/>
  <circle cx="213.3" cy="176.5" r="4.5" stroke="none" fill="currentColor"/>
  <circle cx="226.1" cy="183.6" r="3" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.0"/>
  <text x="204.3" y="194.5" font-size="11" fill="currentColor" text-anchor="end">(1, 0.125)</text>
  <text x="233.1" y="180.5" font-size="11" fill="currentColor">0.05</text>
  <line x1="213.3" y1="156.5" x2="341.1" y2="156.5" stroke="currentColor" stroke-width="1.1"/>
  <line x1="213.3" y1="152.5" x2="213.3" y2="160.5" stroke="currentColor" stroke-width="1.1"/>
  <line x1="341.1" y1="152.5" x2="341.1" y2="160.5" stroke="currentColor" stroke-width="1.1"/>
  <line x1="213.3" y1="161.5" x2="213.3" y2="170.5" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" stroke-dasharray="1 2"/>
  <line x1="341.1" y1="161.5" x2="341.1" y2="208" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" stroke-dasharray="1 2"/>
  <text x="277.2" y="151.5" font-size="11" fill="currentColor" text-anchor="middle">0.5 still to the vertex</text>
  <path d="M336.6 238 L341.1 233 L345.6 238 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="341.1" y="251" font-size="11" fill="currentColor" text-anchor="middle">η = 1</text>
  <path d="M464.4 238 L468.9 233 L473.4 238 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="468.9" y="251" font-size="11" fill="currentColor" text-anchor="middle">η = 2</text>
  <line x1="489.3" y1="247" x2="509.3" y2="247" stroke="currentColor" stroke-width="1.2" marker-end="url(#aOp)"/>
  <text x="513.3" y="251" font-size="11" fill="currentColor">η &gt; 2</text>
  <text x="208" y="30" font-size="11" fill="currentColor" fill-opacity="1.0">η = 0.1: W<tspan dy="3" font-size="9.5">2,1</tspan><tspan dy="-3" dx="3.5">1 → 1.05, L 0.125 → 0.101</tspan></text>
  <text x="208" y="46" font-size="11" fill="currentColor" fill-opacity="1.0">curvature 1 here: one step lands at 1 + 0.5η;</text>
  <text x="208" y="62" font-size="11" fill="currentColor" fill-opacity="1.0">η = 1 hits the vertex, η &lt; 2 converges, η &gt; 2 walks away</text>
  <text x="208" y="84" font-size="11" fill="currentColor" fill-opacity="0.85">the real step moves all three weights; along</text>
  <text x="208" y="100" font-size="11" fill="currentColor" fill-opacity="0.85">its gradient the curvature is ‖h‖² = 14: exact</text>
  <text x="208" y="116" font-size="11" fill="currentColor" fill-opacity="0.85">η = 1/14 ≈ 0.071, divergence past 2/14 ≈ 0.143,</text>
  <text x="208" y="132" font-size="11" fill="currentColor" fill-opacity="0.85">so η = 0.1 overshoots to ŷ = 1.20, not 1</text>
  <text x="12" y="280" font-size="12" fill="currentColor">the variant: η = 10, broken vertical axis</text>
  <line x1="60" y1="424" x2="530" y2="424" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="60" y1="424" x2="60" y2="364" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="60" y1="350" x2="60" y2="306" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="54" y1="364" x2="66" y2="358" stroke="currentColor" stroke-width="1.3"/>
  <line x1="54" y1="356" x2="66" y2="350" stroke="currentColor" stroke-width="1.3"/>
  <text x="548" y="440" font-size="11" fill="currentColor" text-anchor="end">W<tspan dy="3" font-size="9.5">2,1</tspan></text>
  <text x="68" y="312" font-size="11" fill="currentColor">L</text>
  <line x1="104.5" y1="424" x2="104.5" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="104.5" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="178.7" y1="424" x2="178.7" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="178.7" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2</text>
  <line x1="252.9" y1="424" x2="252.9" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="252.9" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">3</text>
  <line x1="327.1" y1="424" x2="327.1" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="327.1" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">4</text>
  <line x1="401.3" y1="424" x2="401.3" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="401.3" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">5</text>
  <line x1="475.5" y1="424" x2="475.5" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="475.5" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">6</text>
  <line x1="56" y1="424" x2="60" y2="424" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="428" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <line x1="56" y1="374" x2="60" y2="374" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="378" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.5</text>
  <line x1="56" y1="340" x2="60" y2="340" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="344" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">10</text>
  <path d="M60.3 364 L62.4 367 L64.4 369.9 L66.4 372.7 L68.5 375.4 L70.5 378.1 L72.5 380.6 L74.6 383.2 L76.6 385.6 L78.6 388 L80.7 390.2 L82.7 392.5 L84.7 394.6 L86.8 396.7 L88.8 398.7 L90.8 400.6 L92.8 402.4 L94.9 404.2 L96.9 405.9 L98.9 407.5 L101 409 L103 410.5 L105 411.9 L107.1 413.2 L109.1 414.4 L111.1 415.6 L113.2 416.6 L115.2 417.7 L117.2 418.6 L119.3 419.5 L121.3 420.2 L123.3 421 L125.4 421.6 L127.4 422.2 L129.4 422.6 L131.5 423.1 L133.5 423.4 L135.5 423.7 L137.5 423.9 L139.6 424 L141.6 424 L143.6 424 L145.7 423.9 L147.7 423.7 L149.7 423.4 L151.8 423.1 L153.8 422.6 L155.8 422.2 L157.9 421.6 L159.9 421 L161.9 420.2 L164 419.5 L166 418.6 L168 417.7 L170.1 416.7 L172.1 415.6 L174.1 414.4 L176.2 413.2 L178.2 411.9 L180.2 410.5 L182.3 409 L184.3 407.5 L186.3 405.9 L188.3 404.2 L190.4 402.4 L192.4 400.6 L194.4 398.6 L196.5 396.7 L198.5 394.6 L200.5 392.5 L202.6 390.2 L204.6 388 L206.6 385.6 L208.7 383.2 L210.7 380.6 L212.7 378.1 L214.8 375.4 L216.8 372.7 L218.8 369.9 L220.9 367 L222.9 364" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <path d="M471.8 350 L472.4 346 L473.1 342.1 L473.7 338.1 L474.4 334.1 L475.1 330.1 L475.7 326.1 L476.4 322.1 L477 318.1 L477.7 314 L478.4 310" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <line x1="104.5" y1="411.5" x2="475.5" y2="411.5" stroke="currentColor" stroke-width="1.5" marker-end="url(#aOp)"/>
  <circle cx="104.5" cy="411.5" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="475.5" y1="405.5" x2="475.5" y2="366" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 3"/>
  <line x1="475.5" y1="348" x2="475.5" y2="332.5" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 3"/>
  <circle cx="475.5" cy="327.5" r="4" stroke="none" fill="currentColor"/>
  <text x="290" y="403.5" font-size="11" fill="currentColor" text-anchor="middle">η = 10: W<tspan dy="3" font-size="9.5">2,1</tspan><tspan dy="-3" dx="3.5">1 → 6</tspan></text>
  <text x="463.5" y="331.5" font-size="11" fill="currentColor" text-anchor="end">L = 10.125 on the slice</text>
  <text x="80" y="300" font-size="11" fill="currentColor" fill-opacity="0.9">full three-weight step: ŷ = 70.5, L = 2415.1, far above this axis</text>
  <text x="12" y="470" font-size="11" fill="currentColor" fill-opacity="0.85">One picture, two step sizes: the only difference between training and divergence.</text>
</svg>

Plant **P1** from [[02-foundations/lab-plants|0.6 Lab Plants]], cut down to the one weight $W_{2,1}$: the loss is the parabola $L=\tfrac12(W_{2,1}-1.5)^2$, its slope at the catalog point $(1,\ 0.125)$ is $-0.5$, and the step $\eta=0.1$ moves the weight $0.05$, to $1.05$ ($L=0.101$), beside the $0.5$ still left to the vertex. On this slice the curvature is $1$, so $\eta=1$ lands on the vertex and $\eta>2$ diverges (on a parabola of curvature $c$ a step multiplies the distance to the vertex by $1-\eta c$; §3). Along the real three-weight gradient the curvature is $\lVert h\rVert^2=14$, the one nonzero eigenvalue of the Hessian $hh^\top$ (derived in §3's P1 step), which moves the exact step to $1/14\approx0.071$ and the divergence threshold to $2/14\approx0.143$. The lower panel is $\eta=10$: the weight jumps to $6$ ($L=10.125$ on the slice), and the full three-weight step reaches $\hat y=70.5$, $L=2415.1$.

### 1. Anatomy of a problem

$$\min_{x \in \mathbb{R}^n} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; h_j(x) = 0$$

Decision variables, objective, inequality/equality constraints. Formulation is half the
work: *what is a variable, what is a constraint, what is the objective* — and often several
formulations of the same engineering problem differ wildly in solvability.

**The parts of that line, each named.**
- **Decision variable** $x\in\mathbb{R}^n$: the $n$ numbers the solver may choose.
- **Objective** $f:\mathbb{R}^n\to\mathbb{R}$: the single number to make small. A maximisation of $u(x)$ is written as minimising $f=-u$.
- **Inequality constraints** $g_i(x)\le0$, $i=1,\ldots,m$, and **equality constraints** $h_j(x)=0$, $j=1,\ldots,p$: requirements every admissible $x$ must meet. "s.t." reads "subject to". Any requirement can be put in this form, for example $x_1\ge2$ becomes $2-x_1\le0$.
- **Feasible set** $\mathcal{F}=\{x : g_i(x)\le0 \text{ for all } i,\ h_j(x)=0 \text{ for all } j\}$: the admissible points. An $x$ outside it is **infeasible**, however small $f(x)$ is.
- **Optimal value** $p^\star=\inf_{x\in\mathcal{F}}f(x)$ and **minimiser** $x^\star$, a feasible point with $f(x^\star)=p^\star$ (the infimum $\inf$ is the greatest lower bound, which a minimiser attains when one exists).

**Local and global minimum, defined.** A feasible $x^\star$ is a **global minimum** when no feasible point does better,
$$f(x^\star)\le f(x)\quad\text{for every } x\in\mathcal{F}$$
and a **local minimum** when that holds only nearby, for every feasible $x$ with $\lVert x-x^\star\rVert<r$ for some radius $r>0$, so a local minimum only has to beat its neighbours. Every global minimum is local; the converse is the question §2 answers. A **strict** local minimum has $<$ in place of $\le$ for $x\ne x^\star$.

> [!example] Worked example · 계산 예제
> Minimise $f(x)=(x-3)^2$ subject to $x\le1$, written as $g(x)=x-1\le0$. The feasible set is $(-\infty,1]$. Without the constraint the answer would be $x=3$, which is infeasible. On the feasible set $f$ keeps falling as $x$ rises toward $1$, so $x^\star=1$ and $p^\star=(1-3)^2=4$. The constraint changed the answer, which is exactly what it means for it to be **active** at the optimum, $g(x^\star)=0$.

The formulation is needed because a preference and a requirement play different roles. For example, a robot may prefer a short path while being required to respect a workspace boundary. Put path cost in the objective and admissibility in constraints, then decide whether the chosen model can represent the actual obstacle and actuation limits. **The reading this gives you.** Before studying a solver, name what it may change and what it must satisfy. A smaller objective value does not establish feasibility, and feasibility in an approximate model does not prove that the physical system meets every requirement.

### 2. Convexity — the great divide

- A set is convex if it contains all line segments between its points; $f$ is convex if
  $f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda)f(y)$ — equivalently
  (twice-differentiable case) $H \succeq 0$ everywhere — read $\succeq 0$ as "positive
  semidefinite", the matrix version of $\ge 0$: $x^\top H x \ge 0$ for every direction $x$,
  i.e. the surface curves upward (or at worst is flat) whichever way you walk.
  (The eigenvalue test for $\succeq0$, all eigenvalues $\ge0$, is in [[02-foundations/linear-algebra|1. Linear Algebra §3]].)
- **Convex set, stated completely.** A set $C\subseteq\mathbb{R}^n$ is convex when, for every two points in it and every mixing weight between $0$ and $1$, the mixed point is also in it:
  $$x\in C,\ y\in C,\ \lambda\in[0,1]\ \implies\ \lambda x+(1-\lambda)y\in C$$
  so the whole segment from $x$ ($\lambda=1$) to $y$ ($\lambda=0$) stays inside. Examples: a half-space $\{x : a^\top x\le b\}$, a ball $\{x : \lVert x-c\rVert\le r\}$, and any intersection of convex sets, which is why a polyhedron $\{x : Hx\le h\}$ is convex. **Non-example:** the ring $\{x : 0.5\le\lVert x\rVert\le1\}$ contains $(1,0)$ and $(-1,0)$ but not their midpoint $(0,0)$. The free space around an obstacle fails for the same reason.
- **Convex function, stated completely.** $f$ is convex when its domain is a convex set and the chord between any two points of its graph lies on or above the graph:
  $$f(\lambda x+(1-\lambda)y)\le\lambda f(x)+(1-\lambda)f(y)\quad\text{for all } x,y,\ \lambda\in[0,1]$$
  because the left side is $f$ at the mixed point and the right side is the same mix of the two function values. Two equivalent tests hold when $f$ is smooth enough. **First order:** every tangent plane lies below the graph, $f(y)\ge f(x)+\nabla f(x)^\top(y-x)$. **Second order:** $H(x)\succeq0$ everywhere, the condition above.
  - **Example.** $f(x)=x^2$ with $x=-1$, $y=3$, $\lambda=0.5$: $f(1)=1\le0.5(1)+0.5(9)=5$ ✓, and $f''=2\ge0$ everywhere.
  - **Non-example.** $f(x)=x^4-2x^2$ with $x=-1$, $y=1$, $\lambda=0.5$: $f(0)=0$ but $0.5f(-1)+0.5f(1)=-1$, so the graph rises above the chord. Its $f''(0)=-4<0$ says the same.
  - **Strict and strong.** $f$ is **strictly convex** when the inequality is strict for $x\ne y$ and $0<\lambda<1$, and **strongly convex** with modulus $m>0$ when $H(x)\succeq mI$ everywhere, curvature at least $m$ in every direction. $x^2$ is strongly convex ($m=2$); $x^4$ is strictly but not strongly convex, since $f''(0)=0$. The Newton convergence claim in §3 needs the strong version.
- Convex problem = convex $f$ over a convex feasible set ⇒ **every local minimum is
  global**. Many standard finite-dimensional convex problems have efficient solvers with
  global-solution guarantees under their stated assumptions.
  - **The conditions, each named.** In the §1 form a problem is **convex** when (1) the objective $f$ is convex, (2) every inequality function $g_i$ is convex, and (3) every equality function $h_j$ is affine, $h_j(x)=a_j^\top x-b_j$. Conditions (2) and (3) are what make the feasible set convex: $\{g_i\le0\}$ is a sublevel set of a convex function, and a nonlinear equality such as $x_1^2+x_2^2=1$ is a circle, which is not convex.
  - **Why local means global.** Suppose $x^\star$ is a local minimum and some feasible $y$ had $f(y)<f(x^\star)$. Points $\lambda x^\star+(1-\lambda)y$ with $\lambda$ just below $1$ are feasible and arbitrarily close to $x^\star$, and convexity gives them $f\le\lambda f(x^\star)+(1-\lambda)f(y)<f(x^\star)$, contradicting local optimality.
  - **Non-example with numbers.** $f(x)=x^4-2x^2+0.5x$ has two local minima, $x\approx-1.057$ with $f\approx-1.515$ and $x\approx0.930$ with $f\approx-0.517$, separated by a local maximum at $x\approx0.127$. Gradient descent with step $0.01$ started at $x=2$ settles at $0.930$, the worse one, and nothing local tells it so.

<svg viewBox="0 0 480 152" style="max-width:100%;height:auto" role="img" aria-label="convex versus non-convex landscape">
  <g fill="none" stroke="currentColor" stroke-width="1.8">
    <path d="M25,32 Q120,152 215,32"/>
    <path d="M265,50 C288,122 302,60 326,102 C349,142 366,50 396,98 C416,130 436,74 455,45"/>
  </g>
  <g fill="currentColor"><circle cx="120" cy="92" r="4"/><circle cx="292" cy="88" r="3.5"/><circle cx="409" cy="108" r="4"/></g>
  <g font-size="11.5" fill="currentColor" text-anchor="middle">
    <text x="120" y="126">the minimum</text>
    <text x="292" y="76" opacity="0.8">local</text><text x="409" y="132">another local</text>
    <text x="120" y="20">convex — every local min is global</text>
    <text x="360" y="20">non-convex — network training lives here</text>
  </g>
</svg>


- Recognizing/preserving convexity is the practical skill: norms, max of affine functions,
  and nonnegative sums of convex functions are convex; LP/QP and most MPC formulations are
  convex *by design*. Neural network training is deliberately non-convex — we trade
  guarantees for expressiveness and settle for good local minima.

### 3. Unconstrained optimization

- **Optimality conditions**: first-order $\nabla f(x^*) = 0$; second-order $H(x^*) \succeq 0$
  (necessary), $\succ 0$ (sufficient for strict local min). Saddle points satisfy the first
  but not the second — and dominate high-dimensional landscapes. The intuition: a minimum needs
  all $n$ Hessian eigenvalues positive, while a saddle only needs a mix of signs. If each sign were
  a coin flip, all $n$ positive would have probability $2^{-n}$ (about 0.001 for $n = 10$). Real
  Hessians are not coin flips, but Dauphin et al. (NeurIPS 2014) report evidence that critical
  points with high loss in neural networks are overwhelmingly saddles.
  - **The three conditions, each named.** For a twice-differentiable $f$ and a candidate $x^\star$: (1) **first-order necessary**, $\nabla f(x^\star)=0$, and a point satisfying it is a **stationary** (or **critical**) point; (2) **second-order necessary**, $H(x^\star)\succeq0$, true at every local minimum; (3) **second-order sufficient**, $\nabla f(x^\star)=0$ together with $H(x^\star)\succ0$, which guarantees a strict local minimum. A **saddle point** is a stationary point whose Hessian has at least one positive and one negative eigenvalue, so it is a minimum along some directions and a maximum along others.
  - **Examples at the boundaries.** $f(x,y)=x^2-y^2$ at the origin has $\nabla f=0$ and $H=\text{diag}(2,-2)$: a saddle. $f(x)=x^3$ at $0$ has $f'=0$ and $f''=0\ge0$, so it passes both necessary conditions, yet it is not a minimum since $f(-0.1)=-0.001<f(0)$. $f(x)=x^4$ at $0$ is a strict minimum with $f''(0)=0$, so condition (3) is sufficient but not necessary.
- **Gradient descent** from Taylor: minimizing the first-order model within a step-size
  trust gives $x_{k+1} = x_k - \alpha\nabla f(x_k)$. On a quadratic with Hessian $H$, the
  per-eigendirection contraction is $|1 - \alpha\lambda_i|$; stability needs
  $\alpha < 2/\lambda_{max}$; with the common choice $\alpha = 1/\lambda_{max}$ the slow direction converges like
  $(1 - \lambda_{min}/\lambda_{max})^k$ — **the condition number $\kappa$ is the pain**
  ([[02-foundations/linear-algebra|1. Linear Algebra §3]]).
  - **The update, with every symbol.** "The first-order model within a step-size trust" is this problem:
    $$x_{k+1}=\arg\min_x\Big[f(x_k)+\nabla f(x_k)^\top(x-x_k)+\frac{1}{2\alpha}\lVert x-x_k\rVert^2\Big]$$
    because setting its gradient $\nabla f(x_k)+(x-x_k)/\alpha$ to zero gives exactly $x_{k+1}=x_k-\alpha\nabla f(x_k)$. Here $k$ counts iterations, $x_k$ is the current iterate, and the **step size** (or **learning rate**) $\alpha>0$ sets how far the linear model is trusted. On $f=\tfrac12x^\top Hx$ the error obeys $x_{k+1}=(I-\alpha H)\,x_k$, which is where the per-eigendirection factor $1-\alpha\lambda_i$ comes from.
- **Gradient descent vs Newton, in one line of arithmetic.** Take $f(x) = 5x^2$, so
  $f'(x) = 10x$ and $f''(x) = 10$, starting at $x_0 = 1$. Gradient descent with
  $\alpha = 0.05$ gives $x_1 = 1 - 0.05(10) = 0.5$, then $0.25$, then $0.125$ — halving every
  step, so about 10 steps to reach $10^{-3}$. Newton divides by the curvature instead:
  $x_1 = 1 - \frac{f'(1)}{f''(1)} = 1 - \frac{10}{10} = 0$ — **exact, in a single step**,
  because a quadratic is precisely the model Newton assumes. Worth seeing once: Newton's
  speed is not magic, it is the payoff for owning the second derivative. On a non-quadratic
  you get that behavior only near the optimum, and you pay $O(n^3)$ per step to form and
  invert $H$ — which is why nobody runs it on a neural network.
- **Worked: one GD step on P1.** Catalog $W_2=(1,-1,0.5)$ and $\partial L/\partial W_2=(-0.5,-1,-1.5)$ from [[02-foundations/calculus-backprop|2]] ([[02-foundations/lab-plants|0.6]]). With $\eta=0.1$: $W_2\leftarrow(1.05,-0.9,0.65)$. Holding $h=(1,2,3)$, $L=\tfrac12(W_{2,1}-1.5)^2$ is a parabola in $W_{2,1}$ with minimum at $1.5$; the catalog sits on the left slope. $\eta=10$ jumps to $W_2=(6,9,15.5)$, $\hat y=70.5$, and $L$ explodes. The problem set is this step by hand.
  - **The curvature along the real step, derived.** With $h$ held fixed, $\hat y=W_2h$ is linear in $W_2$, so $L=\tfrac12(W_2h-y)^2$ has gradient $(\hat y-y)\,h$ and, differentiating once more, Hessian $hh^\top$ ([[02-foundations/calculus-backprop|2. Calculus §1]]). The curvature along a unit direction $u$ is $u^\top hh^\top u=(h^\top u)^2$. Along the single weight $W_{2,1}$, $u=e_1$ gives $h_1^2=1$, the slice in the picture. Along the gradient, $u=h/\lVert h\rVert$ gives $\lVert h\rVert^2=1+4+9=14$, the largest curvature in any direction, because $hh^\top$ has the single nonzero eigenvalue $\lVert h\rVert^2$ with eigenvector $h$. One step shows it directly. The step changes the output by $-\eta(\hat y-y)\lVert h\rVert^2$, so the residual becomes
    $$\hat y'-y=(\hat y-y)\big(1-\eta\lVert h\rVert^2\big)=-0.5\,(1-14\eta)$$
    which is the per-eigendirection factor $1-\alpha\lambda_i$ above with $\lambda=14$. So $\eta=1/14\approx0.071$ zeroes the residual in one step, any $\eta>2/14\approx0.143$ makes it grow, and $\eta=0.1$ overshoots to $-0.5(1-1.4)=+0.2$, i.e. $\hat y=1.20$ and $L=0.02$. $\eta=10$ multiplies the residual by $1-140=-139$: $\hat y-y=69.5$, $\hat y=70.5$ and $L=\tfrac12(69.5)^2=2415.1$.
- **Momentum** accumulates a velocity to average out oscillation across ill-conditioned
  valleys; **Newton** minimizes the *second*-order model,
  $x_{k+1} = x_k - H^{-1}\nabla f$ — quadratic convergence near the optimum for a strongly convex $f$ with Lipschitz Hessian (its curvature cannot change arbitrarily fast: $\lVert H(x) - H(y)\rVert \le L\lVert x - y\rVert$), $O(n^3)$ per
  step; quasi-Newton (BFGS/L-BFGS) builds $H^{-1}$ estimates from gradient differences.
  - **Momentum, stated completely.** The heavy-ball method keeps a **velocity** $v$ with a **momentum coefficient** $\beta\in[0,1)$ and steps along it:
    $$v_{k+1}=\beta v_k+\nabla f(x_k),\qquad x_{k+1}=x_k-\alpha\,v_{k+1}$$
    so $v$ is a decaying sum of past gradients, and $\beta=0$ recovers plain gradient descent. Its effect depends on whether gradients agree. With $\beta=0.9$ and a constant gradient $g$ (a valley floor), $v$ grows to $g/(1-\beta)=10g$, a tenfold longer step. With a gradient alternating $+g,-g$ (bouncing across the valley), $v$ settles to $\pm g/(1+\beta)=\pm0.53g$. The consistent direction is favoured about nineteen to one, which is the "average out oscillation" above.
  - **Newton, with every symbol.** $H=\nabla^2f(x_k)$ is the Hessian at the current iterate, and $-H^{-1}\nabla f(x_k)$ is the exact minimiser of the second-order Taylor model ([[02-foundations/calculus-backprop|2. Calculus §1]]). **Quadratic convergence** means the error obeys $\lVert x_{k+1}-x^\star\rVert\le C\lVert x_k-x^\star\rVert^2$ for some constant $C$, so the number of correct digits roughly doubles each step. On $f(x)=e^x-2x$ (minimiser $x^\star=\ln2$) from $x_0=1$, Newton's errors are $0.307,\ 0.0426,\ 8.95\times10^{-4},\ 4.0\times10^{-7},\ 8.0\times10^{-14}$.
  - **Quasi-Newton, stated completely.** Replace $H$ by a matrix $B_k$ built only from gradients. Its defining requirement is the **secant condition**, with step $s_k=x_{k+1}-x_k$ and gradient change $y_k=\nabla f(x_{k+1})-\nabla f(x_k)$:
    $$B_{k+1}\,s_k = y_k$$
    because along the step just taken, a correct Hessian must turn the change in position into the observed change in gradient. BFGS is the particular low-rank update of $B$ (or of its inverse) that satisfies this while staying symmetric positive definite; L-BFGS stores only the last few $(s_k,y_k)$ pairs instead of an $n\times n$ matrix. One-dimensional example: on $f=5x^2$, moving from $1$ to $0.5$ gives $s=-0.5$, $y=5-10=-5$, and $B=y/s=10$, the true curvature.
- Stochastic gradients: unbiased but noisy estimates from minibatches; noise ~ helps escape
  saddles, demands step-size decay or adaptivity — [[01-canonical-papers/notes/1-foundations/adam|Adam]] ≈
  momentum + per-coordinate curvature proxy.
  - **Stated completely.** For $f(x)=\frac1N\sum_{i=1}^N\ell_i(x)$, an average of per-example losses, a random batch $B$ of $|B|$ examples gives the estimate $\hat g=\frac{1}{|B|}\sum_{i\in B}\nabla\ell_i(x)$. **Unbiased** means $\mathbb{E}[\hat g]=\nabla f(x)$ over the random choice of batch; **noisy** means any single $\hat g$ can be far from it, with variance shrinking like $1/|B|$ for independently drawn examples.
  - **Worked.** Take $\ell_i=\tfrac12(x-a_i)^2$ with $a=(1,2,3,6)$, at $x=0$. The full gradient is $\frac14\sum(0-a_i)=-3$. The six batches of size 2 give $-1.5,\ -2,\ -3.5,\ -2.5,\ -4,\ -4.5$: no single one equals $-3$, and their average is exactly $-3$.

**Adaptive step sizes, in three steps.** These attack the condition-number problem above one coordinate at a time. A single $\alpha$ must be small enough for the steepest direction, which starves the flat ones. So each coordinate gets its own step size, set by how large its gradients have been: a steep coordinate with large gradients gets a small step, a flat one gets a large step. Because the scaling is per coordinate (a diagonal preconditioner), it fixes ill-conditioning aligned with the axes but not a valley tilted between them. The three methods share one update and differ only in the scale $s$:

$$x_{k+1,i} = x_{k,i} - \frac{\alpha}{\sqrt{s_{k,i}} + \epsilon}\, g_{k,i}$$

so a coordinate with a large $s$ takes small steps, because $\alpha/(\sqrt{s}+\epsilon)$ is its effective step size. The $\epsilon$ is a tiny constant (Adam's default is $10^{-8}$) that only keeps the division finite when a coordinate has seen almost no gradient.

- **AdaGrad** (Duchi, Hazan & Singer, JMLR 2011): $s_k = \sum_{t \le k} g_t^2$. Rarely-updated coordinates keep a small sum and so keep large steps. For example, the embedding of a rare word gets a nonzero gradient only in the few batches that contain that word, so AdaGrad lets it move far on each of those rare chances. But the sum only grows, so every step size decays and never recovers.
- **RMSProp** (Tieleman & Hinton 2012, unpublished lecture slides): $s_k = \beta s_{k-1} + (1-\beta) g_k^2$. The exponential average forgets old gradients, so the step can grow back.
- **Adam** adds momentum to the numerator and bias correction for the zero-initialized averages — see the [[01-canonical-papers/notes/1-foundations/adam|Adam note]].

> [!example] Worked example · 계산 예제
> One coordinate sees $g = [1.0, 0.1, 0.1, 0.1]$, with $\epsilon = 0$, $\beta = 0.9$, $s_0 = 0$.
> - **AdaGrad**: $s = 1, 1.01, 1.02, 1.03$, so the effective step is $1.000, 0.995, 0.990, 0.985$ times $\alpha$ — shrinking every step. One early spike has set the scale for good: by step 100 (99 gradients of 0.1) the update is $0.071\alpha$.
> - **RMSProp**: $s = 0.1, 0.091, 0.083, 0.076$, so the effective step is $3.16, 3.31, 3.47, 3.64$ times $\alpha$ — rising as the spike is forgotten; by step 100 the update is $1.00\alpha$.
> - That first RMSProp step of $3.16\alpha$ comes from $s_1 = 0.1$ underestimating $g_1^2 = 1$ tenfold — the zero-initialization bias Adam's correction removes ($0.1/(1-0.9) = 1$).

**AdamW — weight decay is not L2 under adaptive scaling** (Loshchilov & Hutter, ICLR 2019). For plain SGD, adding $\tfrac{\lambda}{2}\|w\|^2$ to the loss and shrinking $w \leftarrow w - \eta\lambda w$ give the same update. In Adam they differ: the L2 gradient $\lambda w$ is divided by $\sqrt{\hat v}$ along with the data gradient, so weights with a history of large gradients are decayed *less*. AdamW applies the shrink outside the adaptive step, so every weight decays at the same rate $\eta\lambda$. The paper reports that this decouples the best $\lambda$ from the learning rate and improves Adam's generalization, which is why most modern recipes — transformers, diffusion policies — use AdamW. Those recipes usually add **linear warmup then cosine decay** ([[02-foundations/ml-practice|9. ML Practice §6]]): early on $\hat v$ averages only a few squared gradients, so its scale is noisy and a full-size step can blow up, and the late decay lets minibatch noise settle.

**The two updates, written out.** With learning rate $\eta$, decay strength $\lambda$, and Adam's bias-corrected averages $\hat m_k$ (of gradients) and $\hat v_k$ (of squared gradients) from the [[01-canonical-papers/notes/1-foundations/adam|Adam note]]:
- **Adam + L2** adds $\lambda w_k$ to the gradient *before* the averages are formed, so the decay passes through the adaptive division: with $g_k=\nabla f(w_k)+\lambda w_k$, the step is $w_{k+1}=w_k-\eta\,\hat m_k/(\sqrt{\hat v_k}+\epsilon)$.
- **AdamW** keeps the gradient pure and applies the decay as a separate term:
$$w_{k+1}=w_k-\eta\Big(\frac{\hat m_k}{\sqrt{\hat v_k}+\epsilon}+\lambda\,w_k\Big)$$
so the shrink $\eta\lambda w_k$ is the same for every weight of the same size, whatever its gradient history. Example, looking at the decay part alone (no momentum, ignoring the small effect of $\lambda w$ on $\hat v$) for two weights equal to $1$ with $\eta=0.01$, $\lambda=0.1$ and $\sqrt{\hat v}=2$ versus $0.5$: under Adam + L2 they shrink by $\eta\lambda/\sqrt{\hat v}=5\times10^{-4}$ and $2\times10^{-3}$, under AdamW both shrink by $\eta\lambda=10^{-3}$.

### 3.5 Nonlinear least squares — the solver under half the robotics papers

Section 3 gave you gradient descent and Newton on a general objective. A large share of
robotics never uses either, because its problems all have the same special shape: a stack of
residuals to be driven toward zero.

$$\min_x \; \lVert f(x) \rVert^2, \qquad f(x) = \big(f_1(x),\, \ldots,\, f_m(x)\big)$$

Bundle adjustment, pose-graph SLAM, ICP registration, camera and hand–eye calibration,
inverse kinematics, and IMU–camera time alignment are all this problem with a different
$f$. You do not need to know any of them yet, only that each has this shape; the robotics track teaches them ([[04-robotics/state-estimation-slam|3. State Estimation & SLAM]] for pose graphs, [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]] for ICP and calibration, [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] for inverse kinematics). Knowing the two algorithms below tells you what those systems are actually doing when
a paper says "we optimize." So is output-error system identification, which fits a model's free run to the measured output instead of its one-step prediction ([[04-robotics/system-identification|5.5 System Identification §5]]).

**What the symbols are.** The unknown $x\in\mathbb{R}^n$ is what is being estimated (a pose, a set of landmark positions, calibration parameters). Each component $f_i:\mathbb{R}^n\to\mathbb{R}$ is a **residual**: what the model predicts for measurement $i$ at the guess $x$, minus what was actually measured. The vector $f(x)\in\mathbb{R}^m$ stacks all $m$ of them, and $\lVert f(x)\rVert^2=\sum_i f_i(x)^2$ is the total squared mismatch, zero only if every measurement is explained exactly. Many papers write $\tfrac12\lVert f\rVert^2$ or weight each residual by an inverse covariance, which changes the scale of the objective but not the method. For the beacon example below, $f_i(x)=\lVert x-a_i\rVert-\rho_i$: the predicted range to beacon $a_i$ minus the measured range $\rho_i$. At the guess $x=(12,4)$ with $\rho=(11.66,\,6.32,\,11.66)$ the residuals are $(0.989,\,-0.663,\,-2.716)$ and $\lVert f\rVert^2=8.79$; at the true $(10,6)$ they are below $0.005$, rounding error in the ranges.

**Gauss–Newton: linearize the residuals, not the objective.** At the current iterate,
replace $f$ by its first-order Taylor model $f(x_k) + J(x - x_k)$, where $J = Df(x_k)$ is
the Jacobian. That model is *affine*, so minimizing its squared norm is an ordinary linear
least squares problem — which you can already solve. Its solution is the next iterate:

$$x_{k+1} = x_k - (J^\top J)^{-1} J^\top f(x_k)$$

Two of the most useful ideas in applied mathematics meet here: calculus builds the affine
approximation, least squares solves it. Note what is *not* here — the second derivatives of
$f$. Full Newton would need them; Gauss–Newton gets its curvature for free out of
$J^\top J$, which is why it is used and Newton is not.

**Exactly what is dropped.** The objective $F(x)=\lVert f(x)\rVert^2$ has gradient $\nabla F=2J^\top f$ and Hessian
$$\nabla^2F = 2\Big(J^\top J+\sum_{i=1}^{m} f_i(x)\,\nabla^2 f_i(x)\Big)$$
so Newton's method on $F$ would need every residual's Hessian $\nabla^2f_i$. Gauss–Newton keeps only $J^\top J$. The dropped sum is weighted by the residuals $f_i$ themselves, so it is small when the model fits the data well near the solution, and then Gauss–Newton behaves almost like Newton. With large residuals at the solution (outliers, a wrong model) it can converge slowly. Setting the gradient of the linearised objective to zero gives the **normal equations** $J^\top J\,\Delta=-J^\top f(x_k)$ for the step $\Delta=x_{k+1}-x_k$, which is the update above.

**It has two representative failure modes that you will see.**

*It can diverge.* Each step reduces the residual of the **model**, but the model is only
trustworthy near $x_k$; the true residual can grow. On $f(x) = \tanh x$ (one residual, one
unknown, a single zero at the origin), Newton from $x_0 = 0.95$ gives
$0.95 \to -0.684 \to 0.234 \to -0.009$ and lands on the solution. From $x_0 = 1.15$ it gives
$1.15 \to -1.318 \to 2.156 \to -16.5$ and is gone. **A 0.2 change in initialization flips
convergence into divergence** — which is why every system above ships with an initializer,
and why "we use RANSAC/an IMU prior/a coarse alignment first" is load-bearing, not a detail.

*It stops outright when $J$ loses rank.* Take a site-localization problem: three beacons on
one wall at $a = (0,0), (8,0), (20,0)$, true position $(10, 6)$. Initialize the solver *on
the wall*, at $(12, 0)$. Each Jacobian row is $(x - a_i)/\lVert x - a_i\rVert$, so with
$y = 0$ every row's second entry is zero and

$$J = \begin{bmatrix} 1 & 0 \\ 1 & 0 \\ -1 & 0 \end{bmatrix}, \qquad J^\top J = \begin{bmatrix} 3 & 0 \\ 0 & 0 \end{bmatrix}, \qquad \det J^\top J = 0$$

Gauss–Newton asks for the inverse of a singular matrix and halts.

**Levenberg–Marquardt: distrust the model by a tunable amount.** A poor local model calls
for trust-region-style accept/reject and shorter steps; a rank-deficient Jacobian instead
signals an unobserved or degenerate direction. LM handles both with one knob $\lambda_k$; keep two facts in mind before the formulas:

1. **What $\lambda$ buys.** It charges for long steps, which keeps the solver where its affine model is trustworthy, and it makes the linear system invertible even when $J$ loses rank.
2. **How $\lambda$ is set.** By trial: shrink it after a step that truly lowered the residual, grow it after one that did not.

**Trust region, the idea LM is a version of.** A trust-region method has two named parts. (1) The **subproblem**: minimise the local model only inside a ball of radius $\Delta_k$ around the iterate,
$$\min_{\delta}\ \lVert f(x_k)+J\delta\rVert^2\quad\text{s.t.}\quad\lVert\delta\rVert\le\Delta_k$$
because the model is believed only that far. (2) The **gain ratio** that grades the step afterwards, $\varrho_k=\big(F(x_k)-F(x_k+\delta)\big)/\big(\text{model decrease}\big)$, actual decrease over predicted decrease. A common rule (Nocedal & Wright ch. 4) rejects the step when $\varrho_k\le0$, shrinks $\Delta$ when $\varrho_k<0.25$, and enlarges it when $\varrho_k>0.75$ and the step reached the boundary. Example: the model predicts a drop of $1.0$; an actual drop of $0.9$ gives $\varrho=0.9$ (trust more), $0.2$ gives $\varrho=0.2$ (keep the step, shrink $\Delta$), and a rise of $0.1$ gives $\varrho=-0.1$ (reject). LM's $\lambda_k$ is the Lagrange multiplier of that ball constraint (§4), which is why raising $\lambda$ acts like shrinking the radius.

Penalize distance from the current iterate — the divergence example above is the reason: the second term charges for leaving the neighbourhood where the affine model held, and $\lambda_k$ sets the price:

$$x_{k+1} = \arg\min_x \; \lVert f(x_k) + J(x - x_k) \rVert^2 + \lambda_k \lVert x - x_k \rVert^2$$

which is a regularized least squares problem. Its closed form follows from setting the gradient of that objective to zero — the Gauss–Newton normal equations with $\lambda_k I$ added to $J^\top J$:

$$x_{k+1} = x_k - (J^\top J + \lambda_k I)^{-1} J^\top f(x_k)$$

The $\lambda I$ makes the linear system invertible and limits explosive steps; it does not
restore information in an unobserved direction or guarantee convergence. In the beacon example it turns
$\det J^\top J = 0$ into $\det(J^\top J + I) = 4$ — the matrix is now invertible no matter
what $J$ does. And $\lambda$ interpolates: at $\lambda \to 0$ this is Gauss–Newton, at large
$\lambda$ it is a short step along the gradient.

Adapt it by trial: take the step, and if
the *true* residual fell, accept it and relax ($\lambda \leftarrow 0.8\lambda$); if it did
not, reject the step and distrust harder ($\lambda \leftarrow 2\lambda$). On the $\tanh$
problem from the same $x_0 = 1.15$ that destroyed Newton, starting from $\lambda_0 = 1$, this reaches $|x| < 10^{-3}$ in
eight steps (a smaller $\lambda_0$ is faster here, a larger one slower).

**Worked — what initialization is worth.** Same three beacons, ranges
$\rho = (11.66,\, 6.32,\, 11.66)$, solved by Gauss–Newton from two starts:

| Start | $k=1$ | $k=2$ | $k=3$ | Converged | $\kappa(J)$ at start |
|---|---|---|---|---|---|
| $(12,\, 0.5)$ — near the wall | $(10.3,\, \mathbf{32.3})$ | $(9.1,\, 8.1)$ | $(10.08,\, 6.14)$ | step 5 | 13.1 |
| $(12,\, 4)$ | $(10.2,\, 6.61)$ | $(9.99,\, 6.01)$ | $(10.0,\, 6.0)$ | step 3 | 1.8 |

Both reach the same answer, but the near-the-wall start throws the estimate to $y = 32.3$ —
five times the true value — before recovering. In a real deployment that excursion is a
robot commanded somewhere impossible, and it is why solvers are given step limits as well as
a trust parameter.

**Four things this buys you when reading.**

- **Damped least squares inverse kinematics *is* Levenberg–Marquardt.** The IK update
  $\Delta q = J^\top (JJ^\top + \lambda I)^{-1} e$ and the LM update
  $\Delta q = (J^\top J + \lambda I)^{-1} J^\top e$ are the same expression, identical to
  machine precision. The $\lambda$ that stops an arm exploding near a singularity
  ([[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]) is a trust parameter,
  not a hack.
- **Conditioning is squared.** For full-column-rank $J$ in the 2-norm,
  $\kappa(J^\top J) = \kappa(J)^2$, so a Jacobian with
  condition number 100 gives normal equations at $10^4$
  ([[02-foundations/linear-algebra|1. Linear Algebra §3]], where the singular-value ratio is defined). QR avoids explicitly squaring
  the condition number and is often the safer dense choice. Sparse normal-Cholesky methods
  do form the normal equations because they can be faster and exploit sparsity; their
  numerical tradeoff must be managed. When a paper reports trouble near singular
  configurations, this conditioning mechanism is one place to look.
- **It is a heuristic, and the papers know it.** Levenberg–Marquardt has no guarantee of
  reaching the global minimum — like $k$-means, it is used everywhere anyway. That is why
  this literature warm-starts from the previous solve, restarts from several
  initializations, and reports the best. When a SLAM or calibration paper says "we solve
  with Ceres / g2o / GTSAM," that only signals a nonlinear least-squares framework. Check
  the actual linearization, trust-region or line-search method, linear solver, and robust-loss
  settings; the library name alone identifies neither this algorithm nor a global optimum.
- **A filter is running this same step.** One Gauss–Newton iteration is algebraically the
  same update an iterated extended Kalman filter applies — the same weighted residual cost,
  written in information form rather than covariance form. So the familiar split between
  "optimisation-based" and "filter-based" state estimators is a choice about which variables
  to keep, not about which problem is being solved
  ([[04-robotics/state-estimation-slam|State Estimation & SLAM §5]]).

### 4. Constrained optimization — Lagrange, KKT, duality

- **Why add the constraint to the objective at all?** At a constrained optimum, you can't
  descend $f$ without violating a constraint — the *descent* direction $-\nabla f$ points
  straight into the active constraint's forbidden side, so $\nabla f$ itself points back into
  the feasible region, anti-parallel to $\nabla g$: $\nabla f = -\lambda\nabla g$ for some
  $\lambda \ge 0$ (the two gradients are anti-parallel). Rearranged, that is
  $\nabla(f + \lambda g) = 0$ — so setting the gradient of the combined **Lagrangian** to zero picks out exactly the
  candidate points where no feasible descent direction remains (on a non-convex problem such a point can be a saddle of the Lagrangian rather than its minimum).
- **Lagrangian**: $\mathcal{L}(x,\lambda,\nu) = f(x) + \sum_i \lambda_i g_i(x) + \sum_j \nu_j h_j(x)$, $\lambda_i \ge 0$.
  - **Its parts, each named.** A scalar function of the decision variable and of one **multiplier** per constraint: $\lambda_i$ for the inequality $g_i\le0$ and $\nu_j$ for the equality $h_j=0$. Inequality multipliers must be nonnegative, because $\lambda_i g_i$ has to act as a penalty for violation ($g_i>0$) and never as a reward. Equality multipliers may have either sign, since $h_j$ can be violated in either direction.
  - **Example.** For the half-space projection worked below, $\min\tfrac12\lVert x-p\rVert^2$ s.t. $a^\top x-b\le0$, the Lagrangian is $\mathcal{L}(x,\lambda)=\tfrac12\lVert x-p\rVert^2+\lambda(a^\top x-b)$, and $\nabla_x\mathcal{L}=x-p+\lambda a=0$ is the stationarity line used there.

<svg viewBox="0 0 560 266" style="max-width:100%;height:auto" role="img" aria-label="at a constrained optimum the gradient of the objective and the gradient of the constraint lie on one line pointing opposite ways">
  <defs><marker id="opA" markerWidth="8" markerHeight="8" refX="7" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" fill-opacity="0.07">
    <polygon points="60,180 360,80 360,190 60,190"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <line x1="60" y1="180" x2="360" y2="80"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.5">
    <circle cx="300" cy="60" r="18"/>
    <circle cx="300" cy="60" r="37.9"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.28" stroke-dasharray="4 3">
    <circle cx="300" cy="60" r="58"/>
  </g>
  <g stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#opA)">
    <line x1="312" y1="96" x2="329.4" y2="148.2"/>
    <line x1="312" y1="96" x2="294.6" y2="43.8"/>
  </g>
  <g fill="currentColor"><circle cx="312" cy="96" r="3.6"/><circle cx="300" cy="60" r="2.6" opacity="0.6"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="70" y="164">feasible region &#183; g(x) &#8804; 0</text>
    <text x="322" y="104">x&#8902;</text>
    <text x="336" y="152">&#8711;f</text>
    <text x="266" y="42">&#8711;g</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8">
    <text x="366" y="82">g(x) = 0</text>
    <text x="366" y="120">one line, opposite directions</text>
    <text x="366" y="58">where f would go if unconstrained</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">At a constrained optimum no feasible direction lowers f any further. That is the same as saying</text>
    <text x="24" y="228">&#8722;&#8711;f points straight out through the boundary, which is the same as saying &#8711;f and &#8711;g lie on one</text>
    <text x="24" y="244">line facing opposite ways. &#955; &#8805; 0 is the ratio of their lengths, and &#8711;(f + &#955;g) = 0 is this picture</text>
    <text x="24" y="260">written on one line &#8212; which is the whole reason the Lagrangian is worth forming.</text>
  </g>
</svg>

- **KKT conditions** (first-order optimality with constraints):
  1. Stationarity: $\nabla_x \mathcal{L} = 0$
  2. Primal feasibility: $g_i \le 0,\ h_j = 0$
  3. Dual feasibility: $\lambda_i \ge 0$
  4. **Complementary slackness**: $\lambda_i\, g_i = 0$ — a constraint either binds
     ($g_i=0$, price $\lambda_i>0$) or is free ($\lambda_i = 0$).

  Condition 1 written out in full, at a candidate $x^\star$ with multipliers $\lambda^\star,\nu^\star$:
  $$\nabla f(x^\star)+\sum_{i=1}^{m}\lambda_i^\star\nabla g_i(x^\star)+\sum_{j=1}^{p}\nu_j^\star\nabla h_j(x^\star)=0$$
  so the objective's gradient is balanced exactly by a nonnegative combination of the constraint gradients, the multi-constraint version of the picture above. A constraint is **active** at $x^\star$ when $g_i(x^\star)=0$ (the point sits on its boundary) and **inactive** when $g_i(x^\star)<0$; complementary slackness says only active constraints may carry a nonzero multiplier. Equality constraints are always active.

  In plain terms: KKT is the checklist a solver uses to recognise a candidate optimum; whether an optimum must pass it, and whether passing it proves optimality, depends on the problem.
  - **Necessary.** With differentiable functions they are **necessary** at any optimum where strong duality holds. For a convex problem, strong duality follows from a constraint qualification such as Slater's condition — some feasible point satisfies every inequality strictly, $g_i(x) < 0$ (Boyd & Vandenberghe §5.5.3).
    At a local minimum of a general, non-convex problem they are still necessary under a constraint qualification such as LICQ (linear independence constraint qualification: at that point, the gradients of the equality constraints and of the active inequality constraints are linearly independent). That is what SQP and interior-point NLP solvers rely on.
  - **Sufficient.** For a convex problem they are **also sufficient**. On a non-convex problem — nonlinear MPC, trajectory
    optimization, the classes §5 lists — a KKT point need not be a minimum at all.
  - **Constraint qualification, and what goes wrong without one.** A constraint qualification is a condition on the *geometry of the constraints alone* (not on $f$) that guarantees the constraint gradients describe the feasible set correctly near the point; Slater and LICQ above are two. Non-example: minimise $f(x)=x$ subject to $g(x)=x^2\le0$. The only feasible point is $x^\star=0$, so it is the minimum. But $\nabla f=1$ and $\nabla g(0)=2x^\star=0$, and stationarity $1+\lambda\cdot0=0$ has no solution for any $\lambda$. KKT fails at a true minimum, because no point satisfies $x^2<0$ (Slater fails) and the single active gradient is zero (LICQ fails).
- Worked example — project a point onto a half-space: $\min \tfrac12\|x - p\|^2$ s.t.
  $a^\top x \le b$. Stationarity: $x = p - \lambda a$. If $a^\top p \le b$: $\lambda = 0$,
  $x^* = p$ (constraint free). Else the constraint binds:
  $\lambda = (a^\top p - b)/\|a\|^2$, $x^* = p - \lambda a$ — exactly the projection formula.
  Complementary slackness *is* the case split.
  **With numbers**: $p = (3,4)$ and the constraint $x_1 + x_2 \le 5$, so $a = (1,1)$, $b = 5$.
  Check feasibility first: $a^\top p = 7 > 5$, so the constraint binds. Then
  $\lambda = (7-5)/2 = 1$ and $x^* = (3,4) - 1(1,1) = (2,3)$. Verify: $2+3 = 5$ ✓ (on the
  boundary), and the correction moved *perpendicular* to the constraint line — the shortest
  way out. Had the point been $p = (1,1)$, then $a^\top p = 2 \le 5$ gives $\lambda = 0$ and
  $x^* = p$: the constraint costs nothing, which is what a zero multiplier means.
- **Duality**: $q(\lambda,\nu) = \min_x \mathcal{L}$ lower-bounds the optimum (weak
  duality); under convexity + constraint qualification the bound is tight. Multipliers =
  **shadow prices**: sensitivity of the optimum to constraint relaxation — in scheduling,
  literally the marginal value of one more crane-hour.
  - **The pieces, each named.** The **dual function** is the Lagrangian minimised over $x$ with the multipliers held fixed,
    $$q(\lambda,\nu)=\inf_{x}\ \mathcal{L}(x,\lambda,\nu)$$
    so $q$ is always concave, whatever $f$ is, since it is a pointwise infimum of functions affine in $(\lambda,\nu)$. **Weak duality**: $q(\lambda,\nu)\le p^\star$ for every $\lambda\ge0$ and any $\nu$, because at any feasible $x$ the added terms satisfy $\lambda_ig_i\le0$ and $\nu_jh_j=0$. The **dual problem** is $d^\star=\max_{\lambda\ge0,\,\nu}q(\lambda,\nu)$, the best such bound. The **duality gap** is $p^\star-d^\star\ge0$, and **strong duality** means the gap is zero.
  - **Shadow price, as a formula.** Relax constraint $i$ to $g_i(x)\le u_i$ and let $p^\star(u)$ be the new optimal value. Under strong duality with a differentiable $p^\star$, $\partial p^\star/\partial u_i=-\lambda_i^\star$: loosening a constraint by a small $u_i$ lowers the optimum by about $\lambda_i^\star u_i$.
  - **Worked.** Minimise $x^2$ subject to $x\ge1$, i.e. $g(x)=1-x\le0$; clearly $x^\star=1$, $p^\star=1$. The Lagrangian $x^2+\lambda(1-x)$ is minimised at $x=\lambda/2$, so $q(\lambda)=\lambda-\lambda^2/4$. At $\lambda=1$ the bound is $q=0.75\le1$ (weak duality); its maximum is at $\lambda^\star=2$ with $d^\star=1=p^\star$ (strong duality). Tighten the constraint to $x\ge1.1$ ($u=-0.1$): the optimum becomes $1.21$, a rise of $0.21$, close to the predicted $\lambda^\star\cdot0.1=0.2$.
- Algorithms: penalty/barrier methods bake constraints into the objective;
  **interior-point** follows the barrier central path (the LP/QP workhorse); **SQP**
  solves a QP model at each iterate (the nonlinear-MPC workhorse); projected gradient for
  simple sets.
  - **Penalty method.** Solve a sequence of unconstrained problems $\min_x f(x)+\frac{\mu}{2}\sum_i\max(0,g_i(x))^2$ with growing weight $\mu$; iterates may be infeasible and approach feasibility as $\mu\to\infty$. On $\min x^2$ s.t. $x\ge1$ the minimiser is $\mu/(2+\mu)$: $0.333$, $0.833$, $0.998$ for $\mu=1,10,1000$, always slightly infeasible.
  - **Barrier and interior-point.** Keep iterates strictly feasible with a logarithmic barrier that blows up at the boundary, with barrier weight $t>0$:
    $$\min_x\ f(x)-t\sum_{i}\log\big(-g_i(x)\big)$$
    because $-\log(-g_i)\to\infty$ as $g_i\to0^-$. The minimisers $x^\star(t)$ trace the **central path**, which reaches the true optimum as $t\to0$; an interior-point method follows that path, taking Newton steps while shrinking $t$. On the same problem, $\min x^2-t\log(x-1)$ gives $x^\star(t)=\big(1+\sqrt{1+2t}\big)/2$: $1.366$, $1.005$, $1.00005$ for $t=1,\,0.01,\,0.0001$, always slightly feasible.
  - **SQP** (sequential quadratic programming). At iterate $x_k$, form a QP with a quadratic model of the Lagrangian as its objective and the constraints linearised, $g_i(x_k)+\nabla g_i(x_k)^\top\delta\le0$ and $h_j(x_k)+\nabla h_j(x_k)^\top\delta=0$; solve for the step $\delta$, update, repeat.
  - **Projected gradient.** Take a gradient step, then return to the feasible set $C$ with the Euclidean projection $\Pi_C(y)=\arg\min_{x\in C}\lVert x-y\rVert$: $x_{k+1}=\Pi_C\big(x_k-\alpha\nabla f(x_k)\big)$. It is practical only when $\Pi_C$ is cheap, as for a box, where it is clipping. Example: on $C=[0,1]$ from $x=0.8$ with gradient $-2$ and $\alpha=0.5$, the step reaches $1.8$ and projection returns $1$.

### 5. Problem classes that matter for robotics

| Class | Form | Where it appears |
|---|---|---|
| LP | linear $f$, linear constraints | resource allocation, scheduling relaxations |
| QP | convex quadratic $f$, linear constraints | **linear MPC**, trajectory smoothing, inverse dynamics |
| NLP | nonlinear | nonlinear MPC, trajectory optimization, calibration |
| MIP | integer variables | task assignment, construction sequencing (branch & bound) |
| Global | non-convex, certified | rarely needed directly; underneath MIP solvers |

**The classes in standard form, each defined.**
- **LP** (linear program): with cost vector $c\in\mathbb{R}^n$, constraint matrix $A\in\mathbb{R}^{m\times n}$ and bounds $b\in\mathbb{R}^m$,
  $$\min_x\ c^\top x\quad\text{s.t.}\quad Ax\le b$$
  so the objective and every constraint are affine, the feasible set is a polyhedron, and when an optimum exists one is found at a vertex. Example: $\min -x_1-2x_2$ s.t. $x_1+x_2\le4$, $x_2\le3$, $x\ge0$. The vertices $(0,0)$, $(4,0)$, $(1,3)$, $(0,3)$ give $0,\ -4,\ -7,\ -6$, so $x^\star=(1,3)$.
- **QP** (quadratic program): the LP constraints with a quadratic objective, $\min_x\tfrac12x^\top Px+q^\top x$ s.t. $Ax\le b$, and it is convex exactly when $P\succeq0$. A non-convex QP ($P$ with a negative eigenvalue) is NP-hard in general, which is why the table says *convex* quadratic.
- **NLP** (nonlinear program): the general §1 form where $f$, $g_i$ or $h_j$ is nonlinear; convex or not, it is solved by SQP or interior-point methods to a KKT point.
- **MIP** (mixed-integer program): any of the above with some variables restricted to integers, $x_i\in\mathbb{Z}$ (often $\{0,1\}$ for yes/no decisions). The integrality makes the feasible set non-convex. **Branch and bound** solves it by dropping integrality to get a lower bound (the *relaxation*), splitting on a fractional variable ($x_i\le\lfloor\cdot\rfloor$ or $x_i\ge\lceil\cdot\rceil$), and discarding any branch whose bound is already worse than the best integer solution found.

**MPC as a QP, written out** ([[04-robotics/index|control track]]): linear dynamics
$x_{t+1} = Ax_t + Bu_t$, horizon $N$, stage cost $x^\top Q x + u^\top R u$,
$Q,P\succeq0$, $R\succ0$, and a polyhedral state set
$\mathcal X=\{x:Hx\le h\}$:

$$\min_{u_0..u_{N-1}} \sum_{t=0}^{N-1}\big(x_t^\top Q x_t + u_t^\top R u_t\big) + x_N^\top P x_N \quad \text{s.t. } x_{t+1} = Ax_t + Bu_t,\; u_{min}\le u_t \le u_{max},\; x_t \in \mathcal{X}$$

Read it as the LQR cost with a finite horizon and hard constraints reattached. The dynamics enter as equality constraints; substitute them out (condensing) and what remains is a convex QP in the $u$'s alone. Small, structured
QPs can run at millisecond scale with an appropriate solver and implementation; report the
deadline and worst-case solve time. MPC re-solves each control step and applies the first input.

**Every symbol, and the loop that makes it MPC.** $x_t\in\mathbb{R}^{n}$ is the predicted state $t$ steps ahead, starting from the measured state $x_0$; $u_t\in\mathbb{R}^{p}$ is the input, the decision variable; $A$ and $B$ are the dynamics matrices (not the LP's $A$); $N$ is the **horizon**, the number of steps looked ahead. $Q$ weights state error, $R$ weights input effort ($R\succ0$ keeps the problem strictly convex in $u$), and $P$ is the **terminal cost** that stands in for everything after step $N$. $H$ and $h$ describe the allowed states (here $H$ is a constraint matrix, not a Hessian). **Model predictive control** is then three steps repeated each sampling period: (1) measure $x_0$, (2) solve the QP for $u_0,\ldots,u_{N-1}$, (3) apply only $u_0$ and discard the rest (the **receding horizon**).

> [!example] Worked example · 계산 예제
> Scalar system $x_{t+1}=x_t+u_t$, $N=1$, $Q=R=P=1$, measured $x_0=1$. The cost is $x_0^2+u_0^2+(x_0+u_0)^2=1+u_0^2+(1+u_0)^2$, minimised where $2u_0+2(1+u_0)=0$, so $u_0=-0.5$ and cost $1.5$. Add the input limit $|u_0|\le0.2$: the unconstrained answer is infeasible, the constraint becomes active, $u_0=-0.2$ and the cost rises to $1+0.04+0.64=1.68$. The full treatment is [[04-robotics/mpc|7. MPC]].

### 6. Reading this wiki through optimization

- Network training = stochastic non-convex optimization
  ([[01-canonical-papers/notes/1-foundations/adam|Adam]]; [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]
  reshapes the landscape's conditioning — one proposed mechanism among several).
- [[01-canonical-papers/notes/1-foundations/lora|LoRA]] = restricting the update to a low-rank parameterization.
- [[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]]'s KL penalty = a soft trust-region constraint.
- Diffusion training = minimizing a variational bound; [[01-canonical-papers/notes/5-world-models/planet|PlaNet]]'s
  CEM planning = derivative-free optimization in latent space.

> [!tip] Going deeper · 더 깊이
> The canonical next step is Boyd and Vandenberghe's [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/) — free, and the book every MPC paper is implicitly citing; ch.2–5 do convexity, duality and KKT properly. For the non-convex half, Nocedal and Wright's *Numerical Optimization*.

### Self-check

1. Show that the max of two convex functions is convex, and use it to argue hinge loss is convex.
2. For $f(x) = \tfrac12 x^\top H x$ with eigenvalues $\{1, 100\}$: what is the largest
   stable step size, and how many iterations to shrink the slow mode by 100×?
3. In the projection example, verify all four KKT conditions in the binding case.
4. Why is the MPC problem above convex, and what could make it non-convex in practice?
   (Hint: obstacle avoidance constraints.)
5. Two weights both equal 1, with $\sqrt{\hat v} = 10$ and $\sqrt{\hat v} = 0.1$. With
   $\eta = 10^{-3}$, $\lambda = 10^{-2}$ and no momentum, how much does each shrink per step
   under Adam + L2, and under AdamW?

> [!tip]- Answers
> 1. The epigraph of a function is the set of points on or above its graph, $\{(x,t) : t \ge f(x)\}$, and a function is convex exactly when its epigraph is a convex set. Since $t \ge \max(f,g)$ means $t \ge f$ and $t \ge g$, the epigraph of $\max(f,g)$ is the intersection of two convex epigraphs, hence convex. Hinge loss $\max(0, 1-yx)$ is the max of two affine functions, so it is convex.
> 2. Stability needs $\alpha < 2/\lambda_{max} = 0.02$. Taking the usual half-of-the-limit $\alpha = 0.01$ (near the boundary the fast mode oscillates), the slow mode contracts as $(1-\alpha\lambda_{min})^k = 0.99^k$; $0.99^k = 0.01 \Rightarrow k = \ln 0.01/\ln 0.99 \approx 458$ iterations. The condition number $\kappa = 100$ *is* that cost.
> 3. Binding case: stationarity holds by construction, $x^* = p - \lambda a$; primal feasibility $a^\top x^* = b$ (active); dual feasibility $\lambda = (a^\top p - b)/\|a\|^2 > 0$ precisely because the constraint was violated at $p$; complementary slackness $\lambda g = \lambda\cdot 0 = 0$.
> 4. The objective is a convex quadratic and the constraints are linear (dynamics equalities plus input/state boxes) — a convex QP. It stops being convex when obstacle avoidance enters (the free space is a non-convex complement) or when discrete decisions such as task ordering or contact-mode selection are added.
> 5. Adam + L2: the decay term $\eta\lambda w/\sqrt{\hat v}$ is $10^{-6}$ for the first weight and $10^{-4}$ for the second — a 100× spread set by gradient history (ignoring the small effect of $\lambda w$ on $\hat v$). AdamW: $\eta\lambda w = 10^{-5}$ for both.

### Problem set · 과제

Tier B. **P1** from [[02-foundations/lab-plants|0.6]]. One gradient step, by hand. The backprop that produced the given gradient lives on [[02-foundations/calculus-backprop|2]]; do not re-derive it here.

1. **Draw.** The picture above for the third weight instead of the first: $L=\tfrac12(\hat y-1)^2$ versus $W_{2,3}$ near $0.5$, holding $W_{2,1}=1$, $W_{2,2}=-1$ and $h=(1,2,3)$ fixed. Mark the catalog point, its tangent, the step $\eta=0.1$ along this weight alone, and the step sizes that land on the vertex and that diverge on this slice. Why is this parabola narrower than the one in the picture above?
2. **Derive.** One GD step $W_2\leftarrow W_2-\eta\,\partial L/\partial W_2$ with $\eta=0.1$ and $\partial L/\partial W_2=(-0.5,-1,-1.5)$, from catalog $W_2=(1,-1,0.5)$.
3. **Interpret.** Repeat with $\eta=10$. New $W_2$, and what happens to $L$?

> [!note]- How to draw it · 그리는 법
> - Axes $W_{2,3}$ (about $0.3$ to $1$) and $L$ ($0$ to about $0.6$). With $h=(1,2,3)$ and the other two weights at their catalog values, $\hat y=3W_{2,3}-1$, so the curve is the parabola $L=\tfrac12(3W_{2,3}-2)^2=\tfrac92(W_{2,3}-\tfrac23)^2$ with its vertex at $(0.667,\ 0)$.
> - The catalog point $W_{2,3}=0.5$ at height $L=0.125$, the same loss as in the picture above because both slices pass through the catalog state; a dot at any other height means the slice was taken wrong.
> - The tangent at that point, labelled with its slope $\partial L/\partial W_{2,3}=3(3\cdot0.5-2)=-1.5$ — the third entry of the gradient item 2 uses.
> - The step as a horizontal arrow *against* the slope, drawn to scale: $\eta=0.1$ moves this weight $0.15$, to $0.65$ ($L=0.00125$), just short of the vertex.
> - Three marks on the axis for what a step size does on this slice, where the curvature is $h_3^2=9$: $\eta=1/9=0.111$ lands exactly on the vertex, anything up to $2/9=0.222$ still converges, and past that the iterate walks away.
> - Draw the picture above's parabola faintly on the same scale, shifted so the two catalog points coincide: curvature $1$ against $9$. The same $\eta=0.1$ that crawls a tenth of the way along $W_{2,1}$ goes nine tenths of the way along $W_{2,3}$.
> - Items 2 and 3 move all three weights: keep their numbers off this slice, or write them in a corner box labelled "full step".

> [!tip]- Solutions
> 1. $\hat y=1-2+3W_{2,3}=3W_{2,3}-1$, so $L=\tfrac12(3W_{2,3}-2)^2=\tfrac92(W_{2,3}-\tfrac23)^2$, minimum at $0.667$. The catalog $W_{2,3}=0.5$ sits at $L=0.125$ on the left slope, with slope $-1.5$, the third entry of $\partial L/\partial W_2$. The curvature is $h_3^2=9$, nine times the first slice's $h_1^2=1$, which is why the parabola is narrower. A step of $\eta=0.1$ along this weight alone moves it $0.15$, to $0.65$ ($L=0.00125$), just short of the vertex; $\eta=1/9=0.111$ lands on it and $\eta>2/9=0.222$ diverges. The curvature along a weight is the square of the activation it multiplies, so one learning rate is a different fraction of the Newton step along each weight.
> 2. $W_2\leftarrow(1,-1,0.5)-0.1(-0.5,-1,-1.5)=(1.05,-0.9,0.65)$.
> 3. $W_2\leftarrow(1,-1,0.5)+(5,10,15)=(6,9,15.5)$. Then $\hat y=70.5$ and $L$ explodes. $\eta=10$ is far past a stable step on this scale.

### Robotics bridge

Constraints and nonlinear optimization become executable robot decisions in [[04-robotics/planning-decision-making|Planning & Decision-Making]] and [[04-robotics/mpc|MPC]].

## 한국어

*[[02-foundations/calculus-backprop|2. 미적분]]의 그래디언트와 테일러 위에 선다. 두 응용 기둥 중 첫째이고, 제약이 붙은 목적함수를
최소화한다 — 학습·MPC·궤적 계획·작업 할당이 한 문장이 되는 자리가 여기다.*

최적화는 이 위키의 공용 언어다: 네트워크 학습([[01-canonical-papers/notes/1-foundations/adam|Adam]]),
MPC 풀기, 궤적 계획, 건설 작업 할당이 모두 "제약 아래 목적함수 최소화"다. 교재 수준의
서술: 조건, 유도, 그리고 완전히 써 내려간 MPC-QP 예제.

> [!note] 처음이라면 · First pass
> 그림, §1, 그다음 §2 — 볼록성이 나머지 전부가 걸리는 분기점이다 — 그리고 §3을 읽어라. §3의 P1 스텝이 그림의 계산이다. §4는 논문이 처음 "subject to"라고 쓸 때 펴라. 눈앞에 구체적인 제약을 두고 읽으면 KKT가 훨씬 잘 읽힌다. §3.5는 SLAM·보정·IK 논문이 "최적화한다"고 쓸 때를 위한 것이니, 그런 논문을 손에 들고 읽어라. §5는 찾아보는 문제 부류 표이고 §6은 이 페이지가 위키 어디에 다시 나오는지 보여주는 한 화면짜리 지도이니, 둘 다 훑어보면 된다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 482" style="max-width:100%;height:auto" role="img" aria-label="가중치 하나 W2,1에 대한 손실: 꼭짓점 1.5의 포물선, 높이 0.125와 기울기 -0.5인 카탈로그 점 1, 남은 거리 0.5 옆에 같은 축척으로 그린 1.05까지의 eta = 0.1 스텝, 축 위의 스텝 크기 1과 2, 아래에는 끊은 축 위의 6까지의 eta = 10 스텝과 실제 스텝의 2415.1">
  <defs><marker id="aOpK" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <line x1="60" y1="214" x2="530" y2="214" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="60" y1="214" x2="60" y2="30" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="548" y="230" font-size="11" fill="currentColor" text-anchor="end">W<tspan dy="3" font-size="9.5">2,1</tspan></text>
  <text x="53" y="24" font-size="11" fill="currentColor" text-anchor="end">L</text>
  <line x1="85.6" y1="214" x2="85.6" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="85.6" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="213.3" y1="214" x2="213.3" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="213.3" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="341.1" y1="214" x2="341.1" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="341.1" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.5</text>
  <line x1="468.9" y1="214" x2="468.9" y2="218" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="468.9" y="230" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2</text>
  <line x1="56" y1="154" x2="60" y2="154" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="158" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.2</text>
  <line x1="56" y1="94" x2="60" y2="94" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="98" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.4</text>
  <line x1="56" y1="34" x2="60" y2="34" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="38" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.6</text>
  <text x="53" y="218" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <path d="M60 32.5 L63.8 37.4 L67.7 42.3 L71.5 47 L75.3 51.8 L79.2 56.4 L83 61 L86.8 65.5 L90.7 69.9 L94.5 74.3 L98.3 78.6 L102.2 82.9 L106 87 L109.8 91.1 L113.7 95.2 L117.5 99.2 L121.3 103.1 L125.2 106.9 L129 110.7 L132.8 114.4 L136.7 118 L140.5 121.6 L144.3 125.1 L148.2 128.5 L152 131.9 L155.8 135.2 L159.7 138.4 L163.5 141.5 L167.3 144.6 L171.2 147.7 L175 150.6 L178.8 153.5 L182.7 156.3 L186.5 159.1 L190.3 161.8 L194.2 164.4 L198 167 L201.8 169.4 L205.7 171.9 L209.5 174.2 L213.3 176.5 L217.2 178.7 L221 180.9 L224.8 182.9 L228.7 185 L232.5 186.9 L236.3 188.8 L240.2 190.6 L244 192.3 L247.8 194 L251.7 195.6 L255.5 197.2 L259.3 198.6 L263.2 200 L267 201.4 L270.8 202.7 L274.7 203.9 L278.5 205 L282.3 206.1 L286.2 207.1 L290 208 L293.8 208.9 L297.7 209.7 L301.5 210.4 L305.3 211.1 L309.2 211.7 L313 212.2 L316.8 212.6 L320.7 213 L324.5 213.4 L328.3 213.6 L332.2 213.8 L336 213.9 L339.8 214 L343.7 214 L347.5 213.9 L351.3 213.8 L355.2 213.5 L359 213.3 L362.8 212.9 L366.7 212.5 L370.5 212 L374.3 211.5 L378.2 210.8 L382 210.2 L385.8 209.4 L389.7 208.6 L393.5 207.7 L397.3 206.7 L401.2 205.7 L405 204.6 L408.8 203.5 L412.7 202.2 L416.5 200.9 L420.3 199.6 L424.2 198.2 L428 196.7 L431.8 195.1 L435.7 193.5 L439.5 191.8 L443.3 190 L447.2 188.2 L451 186.3 L454.8 184.3 L458.7 182.3 L462.5 180.2 L466.3 178 L470.2 175.7 L474 173.4 L477.8 171.1 L481.7 168.6 L485.5 166.1 L489.3 163.5 L493.2 160.9 L497 158.2 L500.8 155.4 L504.7 152.6 L508.5 149.6 L512.3 146.7 L516.2 143.6 L520 140.5" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <circle cx="341.1" cy="214" r="3.5" stroke="none" fill="currentColor"/>
  <text x="347.1" y="192" font-size="11" fill="currentColor" fill-opacity="0.85">꼭짓점 (1.5, 0)</text>
  <line x1="141.8" y1="134.5" x2="277.2" y2="214" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" stroke-dasharray="5 3"/>
  <text x="74" y="160" font-size="11" fill="currentColor">접선 기울기</text>
  <text x="74" y="175" font-size="11" fill="currentColor">1 − 1.5 = −0.5</text>
  <line x1="213.3" y1="176.5" x2="226.6" y2="176.5" stroke="currentColor" stroke-width="1.3" marker-end="url(#aOpK)"/>
  <circle cx="213.3" cy="176.5" r="4.5" stroke="none" fill="currentColor"/>
  <circle cx="226.1" cy="183.6" r="3" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.0"/>
  <text x="204.3" y="194.5" font-size="11" fill="currentColor" text-anchor="end">(1, 0.125)</text>
  <text x="233.1" y="180.5" font-size="11" fill="currentColor">0.05</text>
  <line x1="213.3" y1="156.5" x2="341.1" y2="156.5" stroke="currentColor" stroke-width="1.1"/>
  <line x1="213.3" y1="152.5" x2="213.3" y2="160.5" stroke="currentColor" stroke-width="1.1"/>
  <line x1="341.1" y1="152.5" x2="341.1" y2="160.5" stroke="currentColor" stroke-width="1.1"/>
  <line x1="213.3" y1="161.5" x2="213.3" y2="170.5" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" stroke-dasharray="1 2"/>
  <line x1="341.1" y1="161.5" x2="341.1" y2="208" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" stroke-dasharray="1 2"/>
  <text x="277.2" y="151.5" font-size="11" fill="currentColor" text-anchor="middle">꼭짓점까지 남은 0.5</text>
  <path d="M336.6 238 L341.1 233 L345.6 238 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="341.1" y="251" font-size="11" fill="currentColor" text-anchor="middle">η = 1</text>
  <path d="M464.4 238 L468.9 233 L473.4 238 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="468.9" y="251" font-size="11" fill="currentColor" text-anchor="middle">η = 2</text>
  <line x1="489.3" y1="247" x2="509.3" y2="247" stroke="currentColor" stroke-width="1.2" marker-end="url(#aOpK)"/>
  <text x="513.3" y="251" font-size="11" fill="currentColor">η &gt; 2</text>
  <text x="208" y="30" font-size="11" fill="currentColor" fill-opacity="1.0">η = 0.1: W<tspan dy="3" font-size="9.5">2,1</tspan><tspan dy="-3" dx="3.5">1 → 1.05, L 0.125 → 0.101</tspan></text>
  <text x="208" y="46" font-size="11" fill="currentColor" fill-opacity="1.0">여기 곡률은 1: 한 스텝이 1 + 0.5η에 내려앉는다.</text>
  <text x="208" y="62" font-size="11" fill="currentColor" fill-opacity="1.0">η = 1은 꼭짓점, η &lt; 2는 수렴, η &gt; 2는 걸어 나간다</text>
  <text x="208" y="84" font-size="11" fill="currentColor" fill-opacity="0.85">실제 스텝은 가중치 셋을 함께 움직이고, 그</text>
  <text x="208" y="100" font-size="11" fill="currentColor" fill-opacity="0.85">그래디언트 방향 곡률은 ‖h‖² = 14: 정확 스텝</text>
  <text x="208" y="116" font-size="11" fill="currentColor" fill-opacity="0.85">η = 1/14 ≈ 0.071, 발산 문턱 2/14 ≈ 0.143,</text>
  <text x="208" y="132" font-size="11" fill="currentColor" fill-opacity="0.85">그래서 η = 0.1은 1이 아니라 ŷ = 1.20까지 간다</text>
  <text x="12" y="280" font-size="12" fill="currentColor">변형: η = 10, 세로축을 끊어서</text>
  <line x1="60" y1="424" x2="530" y2="424" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="60" y1="424" x2="60" y2="364" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="60" y1="350" x2="60" y2="306" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="54" y1="364" x2="66" y2="358" stroke="currentColor" stroke-width="1.3"/>
  <line x1="54" y1="356" x2="66" y2="350" stroke="currentColor" stroke-width="1.3"/>
  <text x="548" y="440" font-size="11" fill="currentColor" text-anchor="end">W<tspan dy="3" font-size="9.5">2,1</tspan></text>
  <text x="68" y="312" font-size="11" fill="currentColor">L</text>
  <line x1="104.5" y1="424" x2="104.5" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="104.5" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="178.7" y1="424" x2="178.7" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="178.7" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2</text>
  <line x1="252.9" y1="424" x2="252.9" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="252.9" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">3</text>
  <line x1="327.1" y1="424" x2="327.1" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="327.1" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">4</text>
  <line x1="401.3" y1="424" x2="401.3" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="401.3" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">5</text>
  <line x1="475.5" y1="424" x2="475.5" y2="428" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="475.5" y="440" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">6</text>
  <line x1="56" y1="424" x2="60" y2="424" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="428" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <line x1="56" y1="374" x2="60" y2="374" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="378" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.5</text>
  <line x1="56" y1="340" x2="60" y2="340" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="53" y="344" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">10</text>
  <path d="M60.3 364 L62.4 367 L64.4 369.9 L66.4 372.7 L68.5 375.4 L70.5 378.1 L72.5 380.6 L74.6 383.2 L76.6 385.6 L78.6 388 L80.7 390.2 L82.7 392.5 L84.7 394.6 L86.8 396.7 L88.8 398.7 L90.8 400.6 L92.8 402.4 L94.9 404.2 L96.9 405.9 L98.9 407.5 L101 409 L103 410.5 L105 411.9 L107.1 413.2 L109.1 414.4 L111.1 415.6 L113.2 416.6 L115.2 417.7 L117.2 418.6 L119.3 419.5 L121.3 420.2 L123.3 421 L125.4 421.6 L127.4 422.2 L129.4 422.6 L131.5 423.1 L133.5 423.4 L135.5 423.7 L137.5 423.9 L139.6 424 L141.6 424 L143.6 424 L145.7 423.9 L147.7 423.7 L149.7 423.4 L151.8 423.1 L153.8 422.6 L155.8 422.2 L157.9 421.6 L159.9 421 L161.9 420.2 L164 419.5 L166 418.6 L168 417.7 L170.1 416.7 L172.1 415.6 L174.1 414.4 L176.2 413.2 L178.2 411.9 L180.2 410.5 L182.3 409 L184.3 407.5 L186.3 405.9 L188.3 404.2 L190.4 402.4 L192.4 400.6 L194.4 398.6 L196.5 396.7 L198.5 394.6 L200.5 392.5 L202.6 390.2 L204.6 388 L206.6 385.6 L208.7 383.2 L210.7 380.6 L212.7 378.1 L214.8 375.4 L216.8 372.7 L218.8 369.9 L220.9 367 L222.9 364" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <path d="M471.8 350 L472.4 346 L473.1 342.1 L473.7 338.1 L474.4 334.1 L475.1 330.1 L475.7 326.1 L476.4 322.1 L477 318.1 L477.7 314 L478.4 310" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <line x1="104.5" y1="411.5" x2="475.5" y2="411.5" stroke="currentColor" stroke-width="1.5" marker-end="url(#aOpK)"/>
  <circle cx="104.5" cy="411.5" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="475.5" y1="405.5" x2="475.5" y2="366" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 3"/>
  <line x1="475.5" y1="348" x2="475.5" y2="332.5" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 3"/>
  <circle cx="475.5" cy="327.5" r="4" stroke="none" fill="currentColor"/>
  <text x="290" y="403.5" font-size="11" fill="currentColor" text-anchor="middle">η = 10: W<tspan dy="3" font-size="9.5">2,1</tspan><tspan dy="-3" dx="3.5">1 → 6</tspan></text>
  <text x="463.5" y="331.5" font-size="11" fill="currentColor" text-anchor="end">단면에서 L = 10.125</text>
  <text x="80" y="300" font-size="11" fill="currentColor" fill-opacity="0.9">가중치 셋을 다 움직이는 실제 스텝: ŷ = 70.5, L = 2415.1, 이 축 훨씬 위</text>
  <text x="12" y="470" font-size="11" fill="currentColor" fill-opacity="0.85">그림 하나, 스텝 크기 둘. 학습과 발산을 가르는 유일한 차이다.</text>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P1**, 그 가중치 하나 $W_{2,1}$만 남긴 단면에서 손실은 포물선 $L=\tfrac12(W_{2,1}-1.5)^2$이고, 카탈로그 점 $(1,\ 0.125)$의 기울기는 $-0.5$이며, 스텝 $\eta=0.1$은 꼭짓점까지 남은 $0.5$ 옆에서 가중치를 $0.05$ 옮겨 $1.05$($L=0.101$)에 놓는다. 이 단면의 곡률은 $1$이라 $\eta=1$은 꼭짓점에 내려앉고 $\eta>2$는 발산한다(곡률 $c$인 포물선에서 스텝 하나는 꼭짓점까지의 거리에 $1-\eta c$를 곱한다; §3). 가중치 셋을 모두 움직이는 실제 그래디언트 방향의 곡률은 헤시안 $hh^\top$의 유일한 0 아닌 고윳값 $\lVert h\rVert^2=14$(§3의 P1 스텝에서 유도)라 정확 스텝은 $1/14\approx0.071$, 발산 문턱은 $2/14\approx0.143$으로 옮겨 간다. 아래 칸은 $\eta=10$으로, 가중치가 $6$으로 튀고(단면에서 $L=10.125$) 가중치 셋을 모두 움직이는 스텝은 $\hat y=70.5$, $L=2415.1$에 이른다.

### 1. 문제의 구조

$$\min_{x \in \mathbb{R}^n} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; h_j(x) = 0$$

결정 변수, 목적함수, 부등식/등식 제약. 정식화가 일의 절반이다: *무엇이 변수이고, 무엇이
제약이고, 무엇이 목적인가* — 같은 공학 문제라도 정식화에 따라 풀림성이 극적으로 달라진다.

**이 한 줄의 부분들, 각각의 이름.**
- **결정 변수** $x\in\mathbb{R}^n$: 솔버가 고를 수 있는 숫자 $n$개.
- **목적함수** $f:\mathbb{R}^n\to\mathbb{R}$: 작게 만들 숫자 하나. $u(x)$의 최대화는 $f=-u$의 최소화로 쓴다.
- **부등식 제약** $g_i(x)\le0$, $i=1,\ldots,m$과 **등식 제약** $h_j(x)=0$, $j=1,\ldots,p$: 허용되는 모든 $x$가 지켜야 할 요구 조건. "s.t."는 "subject to(다음 조건 아래)"로 읽는다. 어떤 요구든 이 형태로 쓸 수 있다. 예컨대 $x_1\ge2$는 $2-x_1\le0$이 된다.
- **실행 가능 집합** $\mathcal{F}=\{x : \text{모든 } i\text{에 대해 } g_i(x)\le0,\ \text{모든 } j\text{에 대해 } h_j(x)=0\}$: 허용되는 점들. 그 밖의 $x$는 $f(x)$가 아무리 작아도 **실행 불가능**하다.
- **최적값** $p^\star=\inf_{x\in\mathcal{F}}f(x)$와 **최소화점** $x^\star$, 즉 $f(x^\star)=p^\star$인 실행 가능한 점(하한 $\inf$는 가장 큰 하계이고, 최소화점이 있으면 그 점에서 도달한다).

**지역 최솟값과 전역 최솟값의 정의.** 실행 가능한 $x^\star$보다 나은 실행 가능한 점이 하나도 없으면 **전역 최솟값**이다.
$$f(x^\star)\le f(x)\quad\text{for every } x\in\mathcal{F}$$
이것이 가까운 곳에서만, 즉 어떤 반경 $r>0$에 대해 $\lVert x-x^\star\rVert<r$인 모든 실행 가능한 $x$에서만 성립하면 **지역 최솟값**이다. 그래서 지역 최솟값은 이웃만 이기면 된다. 전역 최솟값은 모두 지역 최솟값이고, 그 역이 언제 성립하느냐가 §2의 질문이다. **엄격한** 지역 최솟값은 $x\ne x^\star$에서 $\le$ 대신 $<$가 성립하는 것이다.

> [!example] 계산 예제 · Worked example
> $x\le1$, 즉 $g(x)=x-1\le0$ 아래에서 $f(x)=(x-3)^2$를 최소화한다. 실행 가능 집합은 $(-\infty,1]$이다. 제약이 없다면 답은 $x=3$이지만 실행 불가능하다. 실행 가능 집합 위에서 $f$는 $x$가 $1$로 갈수록 계속 줄어드므로 $x^\star=1$, $p^\star=(1-3)^2=4$다. 제약이 답을 바꿨다. 이것이 최적점에서 제약이 **활성**이라는 것, $g(x^\star)=0$의 뜻이다.

선호와 필수 조건의 역할이 달라 정식화가 필요하다. 로봇은 짧은 경로를 선호하면서 작업 공간 경계를 반드시 지켜야 할 수 있다. 경로 비용은 목적함수에, 허용 조건은 제약에 넣고 모델이 실제 장애물과 구동 한계를 표현하는지 판단한다. **여기서 얻는 독법.** 해법보다 먼저 바꿀 수 있는 것과 반드시 만족할 것을 적는다. 목적값 감소는 실행 가능성의 증거가 아니며 근사 모델의 가능성이 물리 시스템의 모든 요구 충족을 증명하지는 않는다.

### 2. 볼록성 — 결정적 분기점

- 집합이 볼록 = 두 점 사이 선분을 모두 포함; $f$가 볼록 =
  $f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda)f(y)$ — (2차 미분 가능하면)
  모든 곳에서 $H \succeq 0$과 동치 — $\succeq 0$은 "양의 준정부호"로 읽고, $\ge 0$의 행렬판이다:
  모든 방향 $x$에 대해 $x^\top H x \ge 0$, 즉 어느 방향으로 걸어도 표면이 위로 휘거나
  (최악의 경우) 평평하다는 뜻.
  ($\succeq0$의 고유값 판정, 즉 모든 고유값 $\ge0$은 [[02-foundations/linear-algebra|1. 선형대수 §3]]에 있다.)
- **볼록 집합의 완전한 정의.** 집합 $C\subseteq\mathbb{R}^n$ 안의 어떤 두 점과 $0$과 $1$ 사이의 어떤 섞음 비율에 대해서도 섞은 점이 역시 그 안에 있으면 볼록이다.
  $$x\in C,\ y\in C,\ \lambda\in[0,1]\ \implies\ \lambda x+(1-\lambda)y\in C$$
  그래서 $x$($\lambda=1$)에서 $y$($\lambda=0$)까지의 선분 전체가 안에 머문다. 예: 반공간 $\{x : a^\top x\le b\}$, 공 $\{x : \lVert x-c\rVert\le r\}$, 그리고 볼록 집합들의 교집합 — 다면체 $\{x : Hx\le h\}$가 볼록인 이유다. **반례:** 고리 $\{x : 0.5\le\lVert x\rVert\le1\}$은 $(1,0)$과 $(-1,0)$을 포함하지만 중점 $(0,0)$은 포함하지 않는다. 장애물 주변의 자유 공간이 볼록이 아닌 것도 같은 이유다.
- **볼록 함수의 완전한 정의.** 정의역이 볼록 집합이고, 그래프 위 두 점을 잇는 현이 그래프 위나 그 위쪽에 놓이면 $f$는 볼록이다.
  $$f(\lambda x+(1-\lambda)y)\le\lambda f(x)+(1-\lambda)f(y)\quad\text{for all } x,y,\ \lambda\in[0,1]$$
  좌변은 섞은 점에서의 $f$이고 우변은 두 함수값을 같은 비율로 섞은 것이기 때문이다. $f$가 충분히 매끄러우면 동치인 판정이 둘 있다. **1차:** 모든 접평면이 그래프 아래에 있다, $f(y)\ge f(x)+\nabla f(x)^\top(y-x)$. **2차:** 위에서 말한 모든 곳에서의 $H(x)\succeq0$.
  - **예.** $f(x)=x^2$, $x=-1$, $y=3$, $\lambda=0.5$: $f(1)=1\le0.5(1)+0.5(9)=5$ ✓이고, 모든 곳에서 $f''=2\ge0$.
  - **반례.** $f(x)=x^4-2x^2$, $x=-1$, $y=1$, $\lambda=0.5$: $f(0)=0$인데 $0.5f(-1)+0.5f(1)=-1$이라 그래프가 현 위로 솟는다. $f''(0)=-4<0$도 같은 말을 한다.
  - **엄격 볼록과 강볼록.** $x\ne y$, $0<\lambda<1$에서 부등식이 엄격하면 **엄격 볼록**, 모든 곳에서 $H(x)\succeq mI$($m>0$), 즉 모든 방향의 곡률이 적어도 $m$이면 계수 $m$의 **강볼록**이다. $x^2$은 강볼록($m=2$)이고, $x^4$은 $f''(0)=0$이므로 엄격 볼록이지만 강볼록은 아니다. §3의 뉴턴 수렴 주장에는 강볼록이 필요하다.
- 볼록 문제 = 볼록 가능 영역 위의 볼록 $f$ ⇒ **모든 지역 최솟값이 전역**이다. 많은 표준
  유한차원 볼록 문제에는 명시된 가정 아래 전역해 보장과 효율적인 솔버가 있다.
  - **조건들, 각각의 이름.** §1의 형태에서 (1) 목적함수 $f$가 볼록이고, (2) 모든 부등식 함수 $g_i$가 볼록이고, (3) 모든 등식 함수 $h_j$가 아핀, $h_j(x)=a_j^\top x-b_j$이면 문제가 **볼록**이다. (2)와 (3)이 실행 가능 집합을 볼록으로 만든다. $\{g_i\le0\}$은 볼록 함수의 하위 수준 집합이고, $x_1^2+x_2^2=1$ 같은 비선형 등식은 볼록이 아닌 원이기 때문이다.
  - **지역이 곧 전역인 이유.** $x^\star$가 지역 최솟값인데 어떤 실행 가능한 $y$가 $f(y)<f(x^\star)$라고 하자. $\lambda$가 $1$보다 조금 작은 점 $\lambda x^\star+(1-\lambda)y$는 실행 가능하고 $x^\star$에 얼마든지 가깝다. 볼록성에 의해 그 점들에서 $f\le\lambda f(x^\star)+(1-\lambda)f(y)<f(x^\star)$이므로 지역 최적성과 모순이다.
  - **숫자로 본 반례.** $f(x)=x^4-2x^2+0.5x$에는 지역 최솟값이 둘 있다. $x\approx-1.057$에서 $f\approx-1.515$, $x\approx0.930$에서 $f\approx-0.517$이고, 사이에 $x\approx0.127$의 지역 최댓값이 있다. $x=2$에서 스텝 $0.01$로 시작한 경사 하강은 더 나쁜 쪽인 $0.930$에 멈추고, 국소 정보는 그 사실을 알려주지 않는다.

<svg viewBox="0 0 480 152" style="max-width:100%;height:auto" role="img" aria-label="볼록 지형과 비볼록 지형">
  <g fill="none" stroke="currentColor" stroke-width="1.8">
    <path d="M25,32 Q120,152 215,32"/>
    <path d="M265,50 C288,122 302,60 326,102 C349,142 366,50 396,98 C416,130 436,74 455,45"/>
  </g>
  <g fill="currentColor"><circle cx="120" cy="92" r="4"/><circle cx="292" cy="88" r="3.5"/><circle cx="409" cy="108" r="4"/></g>
  <g font-size="11.5" fill="currentColor" text-anchor="middle">
    <text x="120" y="126">최솟값</text>
    <text x="292" y="76" opacity="0.8">지역 최솟값</text><text x="409" y="132">또 다른 지역 최솟값</text>
    <text x="120" y="20">볼록 — 모든 지역 최솟값이 전역이다</text>
    <text x="360" y="20">비볼록 — 신경망 학습이 사는 곳</text>
  </g>
</svg>


- 볼록성을 알아보고 보존하는 것이 실전 기술이다: 노름, 아핀 함수들의 max, 볼록 함수의
  비음수 합은 볼록; LP/QP와 대부분의 MPC 정식화는 *설계상* 볼록이다. 신경망 학습은
  의도적 비볼록 — 보장을 표현력과 맞바꾸고 좋은 지역 최솟값에 만족한다.

### 3. 무제약 최적화

- **최적성 조건**: 1차 $\nabla f(x^*) = 0$; 2차 $H(x^*) \succeq 0$(필요),
  $\succ 0$(엄격 지역 최소의 충분). 안장점은 1차만 만족한다 — 그리고 고차원 지형을
  지배한다. 직관은 이렇다: 최소점은 헤시안의 고유값 $n$개가 모두 양수여야 하지만, 안장점은
  부호가 섞이기만 하면 된다. 부호 하나하나가 동전 던지기라면 $n$개가 모두 양수일 확률은
  $2^{-n}$이다($n = 10$이면 약 0.001). 실제 헤시안이 동전 던지기는 아니지만, Dauphin 등(NeurIPS
  2014)은 신경망 손실에서 손실이 높은 임계점이 압도적으로 안장점이라는 증거를 보고한다.
  - **세 조건, 각각의 이름.** 두 번 미분 가능한 $f$와 후보 $x^\star$에 대해: (1) **1차 필요조건** $\nabla f(x^\star)=0$, 이를 만족하는 점이 **정상점**(또는 **임계점**)이다. (2) **2차 필요조건** $H(x^\star)\succeq0$, 모든 지역 최솟값에서 참이다. (3) **2차 충분조건** $\nabla f(x^\star)=0$이면서 $H(x^\star)\succ0$, 엄격한 지역 최솟값을 보장한다. **안장점**은 헤시안에 양의 고유값과 음의 고유값이 적어도 하나씩 있는 정상점이라, 어떤 방향으로는 최소이고 다른 방향으로는 최대다.
  - **경계에 있는 예.** $f(x,y)=x^2-y^2$의 원점은 $\nabla f=0$, $H=\text{diag}(2,-2)$인 안장점이다. $f(x)=x^3$의 $0$은 $f'=0$, $f''=0\ge0$이라 두 필요조건을 모두 통과하지만 $f(-0.1)=-0.001<f(0)$이므로 최솟값이 아니다. $f(x)=x^4$의 $0$은 $f''(0)=0$인 엄격한 최솟값이므로, 조건 (3)은 충분하지만 필요하지는 않다.
- 테일러에서 나오는 **경사 하강**: 1차 모델을 신뢰 반경 안에서 최소화하면
  $x_{k+1} = x_k - \alpha\nabla f(x_k)$. 헤시안 $H$의 이차 함수에서 고유방향별 수축률은
  $|1 - \alpha\lambda_i|$; 안정성엔 $\alpha < 2/\lambda_{max}$가 필요하고, 흔히 쓰는 $\alpha = 1/\lambda_{max}$를 고르면 느린 방향은
  $(1 - \lambda_{min}/\lambda_{max})^k$처럼 수렴한다 — **조건수 $\kappa$가 곧 고통이다**
  ([[02-foundations/linear-algebra|1. 선형대수 §3]]).
  - **갱신식, 모든 기호와 함께.** "1차 모델을 신뢰 반경 안에서 최소화"는 이 문제다.
    $$x_{k+1}=\arg\min_x\Big[f(x_k)+\nabla f(x_k)^\top(x-x_k)+\frac{1}{2\alpha}\lVert x-x_k\rVert^2\Big]$$
    그 그래디언트 $\nabla f(x_k)+(x-x_k)/\alpha$를 0으로 놓으면 정확히 $x_{k+1}=x_k-\alpha\nabla f(x_k)$가 나오기 때문이다. $k$는 반복 횟수, $x_k$는 현재 반복점, **스텝 크기**(또는 **학습률**) $\alpha>0$는 선형 모델을 얼마나 멀리까지 믿을지 정한다. $f=\tfrac12x^\top Hx$에서는 오차가 $x_{k+1}=(I-\alpha H)\,x_k$를 따르고, 고유방향별 인수 $1-\alpha\lambda_i$가 여기서 나온다.
- **경사 하강 vs 뉴턴법, 산수 한 줄로.** $f(x) = 5x^2$이면 $f'(x) = 10x$, $f''(x) = 10$이다.
  $x_0 = 1$에서 $\alpha = 0.05$의 경사 하강을 하면 $x_1 = 1 - 0.05(10) = 0.5$, 다음 $0.25$,
  그다음 $0.125$ — 매 스텝 절반이 되므로 $10^{-3}$에 닿는 데 약 10 스텝이 든다. 뉴턴법은 대신
  곡률로 나눈다: $x_1 = 1 - \frac{f'(1)}{f''(1)} = 1 - \frac{10}{10} = 0$ — **단 한 스텝에
  정확히** 도착한다. 이차 함수가 곧 뉴턴법이 가정하는 모델 그 자체이기 때문이다. 한 번은 봐둘
  값어치가 있다: 뉴턴법의 속도는 마법이 아니라 2차 도함수를 가진 값이다. 이차가 아닌 함수에서는
  최적점 근처에서만 이 거동이 나오고, 매 스텝 $H$를 만들고 역행렬을 구하는 데 $O(n^3)$을 낸다 —
  아무도 신경망에 이걸 돌리지 않는 이유다.
- **계산: P1에서 GD 한 스텝.** 카탈로그의 $W_2=(1,-1,0.5)$와 [[02-foundations/calculus-backprop|2]]에서 온 $\partial L/\partial W_2=(-0.5,-1,-1.5)$([[02-foundations/lab-plants|0.6]]). $\eta=0.1$이면 $W_2\leftarrow(1.05,-0.9,0.65)$. $h=(1,2,3)$을 고정하면 $L=\tfrac12(W_{2,1}-1.5)^2$은 $W_{2,1}$의 포물선이고 최솟값은 $1.5$에 있다. 카탈로그는 왼쪽 비탈에 앉아 있다. $\eta=10$은 $W_2=(6,9,15.5)$로 뛰어 $\hat y=70.5$가 되고 $L$이 폭발한다. 과제는 이 스텝을 손으로 하는 것이다.
  - **실제 스텝 방향의 곡률, 유도.** $h$를 고정하면 $\hat y=W_2h$는 $W_2$에 대해 선형이므로 $L=\tfrac12(W_2h-y)^2$의 그래디언트는 $(\hat y-y)\,h$이고, 한 번 더 미분하면 헤시안은 $hh^\top$이다([[02-foundations/calculus-backprop|2. 미적분 §1]]). 단위 방향 $u$를 따른 곡률은 $u^\top hh^\top u=(h^\top u)^2$다. 가중치 하나 $W_{2,1}$ 방향, 곧 $u=e_1$이면 $h_1^2=1$로 그림의 단면이다. 그래디언트 방향, 곧 $u=h/\lVert h\rVert$이면 $\lVert h\rVert^2=1+4+9=14$이고, $hh^\top$의 0 아닌 고윳값은 고유벡터 $h$를 가진 $\lVert h\rVert^2$ 하나뿐이므로 이것이 어느 방향보다 큰 곡률이다. 한 스텝이 이를 바로 보여준다. 스텝은 출력을 $-\eta(\hat y-y)\lVert h\rVert^2$만큼 바꾸므로 잔차는
    $$\hat y'-y=(\hat y-y)\big(1-\eta\lVert h\rVert^2\big)=-0.5\,(1-14\eta)$$
    가 되고, 이것이 위의 고유방향별 인자 $1-\alpha\lambda_i$에 $\lambda=14$를 넣은 것이다. 그래서 $\eta=1/14\approx0.071$은 한 스텝에 잔차를 0으로 만들고, $\eta>2/14\approx0.143$이면 잔차가 커지며, $\eta=0.1$은 $-0.5(1-1.4)=+0.2$로 넘어가 $\hat y=1.20$, $L=0.02$가 된다. $\eta=10$은 잔차에 $1-140=-139$를 곱한다: $\hat y-y=69.5$, $\hat y=70.5$, $L=\tfrac12(69.5)^2=2415.1$.
- **모멘텀**은 속도를 누적해 나쁜 조건의 골짜기에서 진동을 상쇄한다; **뉴턴법**은 *2차*
  모델을 최소화, $x_{k+1} = x_k - H^{-1}\nabla f$ — 강볼록이고 헤시안이 립시츠일 때(곡률이 임의로 빠르게 변할 수 없다는 뜻: $\lVert H(x) - H(y)\rVert \le L\lVert x - y\rVert$) 최적점 근처 이차 수렴, 스텝당
  $O(n^3)$; 준뉴턴(BFGS/L-BFGS)은 그래디언트 차분으로 $H^{-1}$ 추정을 쌓는다.
  - **모멘텀의 완전한 정의.** heavy-ball 방법은 **모멘텀 계수** $\beta\in[0,1)$로 **속도** $v$를 유지하고 그 방향으로 내딛는다.
    $$v_{k+1}=\beta v_k+\nabla f(x_k),\qquad x_{k+1}=x_k-\alpha\,v_{k+1}$$
    그래서 $v$는 과거 그래디언트의 감쇠 합이고, $\beta=0$이면 평범한 경사 하강이다. 효과는 그래디언트들이 일치하느냐에 달려 있다. $\beta=0.9$에서 그래디언트가 일정한 $g$면(골짜기 바닥) $v$가 $g/(1-\beta)=10g$로 자라 스텝이 열 배 길어진다. $+g,-g$로 번갈아 오면(골짜기를 가로질러 튐) $v$는 $\pm g/(1+\beta)=\pm0.53g$에 자리 잡는다. 일관된 방향이 약 19대 1로 우대받는 것이 위에서 말한 "진동 상쇄"다.
  - **뉴턴법, 모든 기호와 함께.** $H=\nabla^2f(x_k)$는 현재 반복점의 헤시안이고, $-H^{-1}\nabla f(x_k)$는 2차 테일러 모델([[02-foundations/calculus-backprop|2. 미적분 §1]])의 정확한 최소화점이다. **이차 수렴**은 어떤 상수 $C$에 대해 오차가 $\lVert x_{k+1}-x^\star\rVert\le C\lVert x_k-x^\star\rVert^2$를 따른다는 뜻이라, 맞는 자릿수가 스텝마다 대략 두 배가 된다. $f(x)=e^x-2x$(최소화점 $x^\star=\ln2$)를 $x_0=1$에서 풀면 뉴턴의 오차가 $0.307,\ 0.0426,\ 8.95\times10^{-4},\ 4.0\times10^{-7},\ 8.0\times10^{-14}$이다.
  - **준뉴턴의 완전한 정의.** $H$를 그래디언트만으로 만든 행렬 $B_k$로 바꾼다. 스텝 $s_k=x_{k+1}-x_k$와 그래디언트 변화 $y_k=\nabla f(x_{k+1})-\nabla f(x_k)$로 쓴 **할선 조건**이 정의하는 요구다.
    $$B_{k+1}\,s_k = y_k$$
    방금 밟은 스텝 방향에서는 올바른 헤시안이 위치 변화를 관측된 그래디언트 변화로 바꿔야 하기 때문이다. BFGS는 이를 만족하면서 대칭 양정부호를 유지하는 특정한 저랭크 갱신($B$나 그 역에 대한)이고, L-BFGS는 $n\times n$ 행렬 대신 최근 $(s_k,y_k)$ 쌍 몇 개만 저장한다. 1차원 예: $f=5x^2$에서 $1$에서 $0.5$로 가면 $s=-0.5$, $y=5-10=-5$, $B=y/s=10$으로 참 곡률이다.
- 확률적 그래디언트: 미니배치의 불편이지만 시끄러운 추정; 노이즈는 안장 탈출을 돕는 대신
  스텝 감쇠나 적응성을 요구한다 — [[01-canonical-papers/notes/1-foundations/adam|Adam]] ≈ 모멘텀 +
  좌표별 곡률 대리.
  - **완전한 정의.** 예제별 손실의 평균 $f(x)=\frac1N\sum_{i=1}^N\ell_i(x)$에 대해, 예제 $|B|$개의 무작위 배치 $B$가 추정 $\hat g=\frac{1}{|B|}\sum_{i\in B}\nabla\ell_i(x)$를 준다. **불편**은 배치의 무작위 선택에 대해 $\mathbb{E}[\hat g]=\nabla f(x)$라는 뜻이고, **시끄럽다**는 것은 한 번의 $\hat g$가 그것과 멀 수 있다는 뜻이다. 예제를 독립적으로 뽑으면 분산은 $1/|B|$처럼 준다.
  - **계산.** $\ell_i=\tfrac12(x-a_i)^2$, $a=(1,2,3,6)$, $x=0$으로 두자. 전체 그래디언트는 $\frac14\sum(0-a_i)=-3$이다. 크기 2인 배치 여섯 개는 $-1.5,\ -2,\ -3.5,\ -2.5,\ -4,\ -4.5$를 준다. 어느 하나도 $-3$이 아니지만 평균은 정확히 $-3$이다.

**적응형 스텝 크기, 세 단계로.** 위의 조건수 문제를 좌표 하나씩 공략하는 방법이다. $\alpha$ 하나는 가장 가파른 방향에 맞춰 작아야 하므로 평평한 방향은 거의 움직이지 못한다. 그래서 좌표마다 그동안 그래디언트가 얼마나 컸는지에 따라 자기만의 스텝 크기를 받는다: 그래디언트가 큰 가파른 좌표는 작은 스텝을, 평평한 좌표는 큰 스텝을 받는다. 스케일링이 좌표별(대각 전처리기)이므로 축에 정렬된 나쁜 조건은 고치지만, 축 사이로 비스듬히 놓인 골짜기는 고치지 못한다. 세 방법은 같은 업데이트를 공유하고 척도 $s$만 다르다:

$$x_{k+1,i} = x_{k,i} - \frac{\alpha}{\sqrt{s_{k,i}} + \epsilon}\, g_{k,i}$$

$\alpha/(\sqrt{s}+\epsilon)$가 그 좌표의 유효 스텝 크기이기 때문에, $s$가 큰 좌표는 작은 스텝을 밟는다. $\epsilon$은 아주 작은 상수(Adam의 기본값은 $10^{-8}$)로, 그래디언트를 거의 받지 못한 좌표에서 나눗셈이 발산하지 않게 할 뿐이다.

- **AdaGrad**(Duchi, Hazan & Singer, JMLR 2011): $s_k = \sum_{t \le k} g_t^2$. 드물게 갱신되는 좌표는 합이 작게 유지되므로 큰 스텝을 유지한다. 예를 들어 드문 단어의 임베딩은 그 단어가 들어 있는 몇 안 되는 배치에서만 0이 아닌 그래디언트를 받으므로, AdaGrad는 그 드문 기회마다 크게 움직이게 해 준다. 그러나 합은 커지기만 하므로 모든 스텝 크기가 줄어들고 다시 회복되지 않는다.
- **RMSProp**(Tieleman & Hinton 2012, 미출간 강의 슬라이드): $s_k = \beta s_{k-1} + (1-\beta) g_k^2$. 지수 평균은 오래된 그래디언트를 잊으므로 스텝이 다시 커질 수 있다.
- **Adam**은 분자에 모멘텀을, 0으로 초기화된 평균에 편향 보정을 더한다 — [[01-canonical-papers/notes/1-foundations/adam|Adam 노트]] 참고.

> [!example] 계산 예제 · Worked example
> 한 좌표가 $g = [1.0, 0.1, 0.1, 0.1]$을 받는다. $\epsilon = 0$, $\beta = 0.9$, $s_0 = 0$.
> - **AdaGrad**: $s = 1, 1.01, 1.02, 1.03$이므로 유효 스텝은 $\alpha$의 $1.000, 0.995, 0.990, 0.985$배 — 매 스텝 줄어든다. 초반의 스파이크 하나가 척도를 영영 정해 버린다: 100번째 스텝(0.1짜리 그래디언트 99개 뒤)의 업데이트는 $0.071\alpha$다.
> - **RMSProp**: $s = 0.1, 0.091, 0.083, 0.076$이므로 유효 스텝은 $\alpha$의 $3.16, 3.31, 3.47, 3.64$배 — 스파이크를 잊어 가며 커진다. 100번째 스텝의 업데이트는 $1.00\alpha$다.
> - RMSProp 첫 스텝이 $3.16\alpha$인 것은 $s_1 = 0.1$이 $g_1^2 = 1$을 열 배 과소추정하기 때문이다 — Adam의 보정이 없애는 바로 그 0-초기화 편향이다($0.1/(1-0.9) = 1$).

**AdamW — 적응 스케일링 아래서 weight decay는 L2가 아니다**(Loshchilov & Hutter, ICLR 2019). 평범한 SGD에서는 손실에 $\tfrac{\lambda}{2}\|w\|^2$를 더하는 것과 $w \leftarrow w - \eta\lambda w$로 줄이는 것이 같은 업데이트다. Adam에서는 다르다: L2 그래디언트 $\lambda w$가 데이터 그래디언트와 함께 $\sqrt{\hat v}$로 나뉘므로, 그래디언트가 컸던 이력이 있는 가중치일수록 *덜* 감쇠된다. AdamW는 줄이기를 적응 스텝 바깥에서 적용하므로 모든 가중치가 같은 비율 $\eta\lambda$로 감쇠한다. 논문은 이렇게 하면 최적 $\lambda$가 학습률과 분리되고 Adam의 일반화가 좋아진다고 보고하며, 그래서 트랜스포머·디퓨전 정책 등 대부분의 현대 학습 레시피가 AdamW를 쓴다. 이런 레시피는 보통 **선형 워밍업 후 코사인 감쇠**를 붙인다([[02-foundations/ml-practice|9. ML 실무 §6]]): 초반에는 $\hat v$가 제곱 그래디언트 몇 개만 평균하므로 척도가 시끄럽고 전체 크기 스텝이 폭주할 수 있으며, 후반의 감쇠는 미니배치 노이즈를 가라앉힌다.

**두 갱신식을 써 보면.** 학습률 $\eta$, 감쇠 강도 $\lambda$, 그리고 [[01-canonical-papers/notes/1-foundations/adam|Adam 노트]]의 편향 보정된 평균 $\hat m_k$(그래디언트)와 $\hat v_k$(제곱 그래디언트)로:
- **Adam + L2**는 평균을 만들기 *전에* 그래디언트에 $\lambda w_k$를 더하므로 감쇠가 적응 나눗셈을 통과한다. $g_k=\nabla f(w_k)+\lambda w_k$로 두고 스텝은 $w_{k+1}=w_k-\eta\,\hat m_k/(\sqrt{\hat v_k}+\epsilon)$이다.
- **AdamW**는 그래디언트를 순수하게 두고 감쇠를 별도 항으로 적용한다.
$$w_{k+1}=w_k-\eta\Big(\frac{\hat m_k}{\sqrt{\hat v_k}+\epsilon}+\lambda\,w_k\Big)$$
그래서 줄이는 양 $\eta\lambda w_k$는 그래디언트 이력과 상관없이 크기가 같은 모든 가중치에 같다. 예: 감쇠 부분만 보면(모멘텀 없음, $\lambda w$가 $\hat v$에 주는 작은 영향은 무시) $1$인 두 가중치에 $\eta=0.01$, $\lambda=0.1$, $\sqrt{\hat v}=2$와 $0.5$일 때, Adam + L2에서는 $\eta\lambda/\sqrt{\hat v}=5\times10^{-4}$와 $2\times10^{-3}$만큼, AdamW에서는 둘 다 $\eta\lambda=10^{-3}$만큼 준다.

### 3.5 비선형 최소자승 — 로보틱스 논문 절반 아래에 있는 풀이법

3절은 일반 목적함수에 대한 경사하강과 뉴턴을 주었다. 로보틱스의 큰 몫은 둘 중 어느 것도 쓰지
않는데, 그 문제들이 전부 같은 특별한 모양을 하고 있기 때문이다: 0으로 몰아야 할 잔차 더미.

$$\min_x \; \lVert f(x) \rVert^2, \qquad f(x) = \big(f_1(x),\, \ldots,\, f_m(x)\big)$$

번들 조정, 포즈그래프 SLAM, ICP 정합, 카메라·손눈 보정, 역기구학, IMU–카메라 시간 정렬이
전부 $f$만 다른 이 문제다. 이것들을 아직 알 필요는 없고, 모두 이 모양이라는 것만 알면 된다. 로보틱스 트랙이 가르친다(포즈그래프는 [[04-robotics/state-estimation-slam|3. 상태 추정과 SLAM]], ICP와 보정은 [[04-robotics/geometric-perception-calibration|3.5 기하 인식과 보정]], 역기구학은 [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장]]). 아래 두 알고리즘을 알면 논문이 "최적화한다"고 쓸 때 그 시스템들이
실제로 무엇을 하고 있는지 알 수 있다. 출력 오차 시스템 식별도 그렇다. 모델의 한 스텝 예측 대신 자유 주행을 측정 출력에 맞추기 때문이다([[04-robotics/system-identification|5.5 시스템 식별 §5]]).

**기호가 무엇인가.** 미지수 $x\in\mathbb{R}^n$은 추정할 대상이다(자세, 랜드마크 위치들, 보정 파라미터). 각 성분 $f_i:\mathbb{R}^n\to\mathbb{R}$는 **잔차**다. 추정값 $x$에서 모델이 측정 $i$에 대해 예측하는 값에서 실제 측정값을 뺀 것이다. 벡터 $f(x)\in\mathbb{R}^m$은 잔차 $m$개를 쌓은 것이고, $\lVert f(x)\rVert^2=\sum_i f_i(x)^2$은 전체 제곱 불일치로, 모든 측정이 정확히 설명될 때만 0이다. 많은 논문이 $\tfrac12\lVert f\rVert^2$로 쓰거나 잔차마다 역공분산 가중치를 주는데, 목적함수의 척도만 바뀌고 방법은 같다. 아래 비콘 예제에서는 $f_i(x)=\lVert x-a_i\rVert-\rho_i$, 즉 비콘 $a_i$까지의 예측 거리에서 측정 거리 $\rho_i$를 뺀 것이다. 추정값 $x=(12,4)$, $\rho=(11.66,\,6.32,\,11.66)$에서 잔차는 $(0.989,\,-0.663,\,-2.716)$이고 $\lVert f\rVert^2=8.79$다. 참 위치 $(10,6)$에서는 거리 반올림 오차 수준인 $0.005$ 미만이다.

**Gauss–Newton: 목적함수가 아니라 잔차를 선형화한다.** 현재 반복점에서 $f$를 1차 테일러 모델
$f(x_k) + J(x - x_k)$로 바꾼다. $J = Df(x_k)$는 야코비다. 이 모델은 *아핀*이므로 그 제곱
노름을 최소화하는 것은 평범한 선형 최소자승 문제이고, 그건 이미 풀 줄 안다. 그 해가 다음
반복점이다.

$$x_{k+1} = x_k - (J^\top J)^{-1} J^\top f(x_k)$$

응용수학에서 가장 쓸모 있는 두 발상이 여기서 만난다. 미적분이 아핀 근사를 만들고, 최소자승이
그것을 푼다. 여기에 *없는* 것에 주목하라 — $f$의 2차 도함수다. 완전한 뉴턴이라면 그것이
필요하다. Gauss–Newton은 곡률을 $J^\top J$에서 공짜로 얻고, 그래서 이것이 쓰이고 뉴턴은
쓰이지 않는다.

**정확히 무엇을 버리는가.** 목적함수 $F(x)=\lVert f(x)\rVert^2$의 그래디언트는 $\nabla F=2J^\top f$이고 헤시안은
$$\nabla^2F = 2\Big(J^\top J+\sum_{i=1}^{m} f_i(x)\,\nabla^2 f_i(x)\Big)$$
이므로 $F$에 뉴턴법을 쓰려면 잔차마다 헤시안 $\nabla^2f_i$가 필요하다. Gauss–Newton은 $J^\top J$만 남긴다. 버린 합은 잔차 $f_i$ 자체로 가중되므로, 해 근처에서 모델이 데이터에 잘 맞으면 작고 그때 Gauss–Newton은 거의 뉴턴처럼 움직인다. 해에서도 잔차가 크면(이상치, 틀린 모델) 느리게 수렴할 수 있다. 선형화된 목적함수의 그래디언트를 0으로 놓으면 스텝 $\Delta=x_{k+1}-x_k$에 대한 **정규방정식** $J^\top J\,\Delta=-J^\top f(x_k)$가 나오고, 이것이 위의 갱신식이다.

**대표적인 실패 방식 둘은 모두 자주 보게 된다.**

*발산할 수 있다.* 각 스텝은 **모델**의 잔차를 줄이지만, 모델은 $x_k$ 근처에서만 믿을 만하다.
참 잔차는 커질 수 있다. $f(x) = \tanh x$(잔차 하나, 미지수 하나, 원점에 유일한 영점)에서
뉴턴은 $x_0 = 0.95$부터 $0.95 \to -0.684 \to 0.234 \to -0.009$로 가서 해에 앉는다.
$x_0 = 1.15$부터는 $1.15 \to -1.318 \to 2.156 \to -16.5$로 가고 끝이다. **초기화의 0.2 차이가
수렴을 발산으로 뒤집는다** — 위의 모든 시스템이 초기화기를 함께 싣는 이유이고, "먼저
RANSAC을/IMU 사전값을/거친 정렬을 쓴다"가 사소한 세부가 아니라 하중을 지고 있는 이유다.

*$J$가 계수를 잃으면 아예 멈춘다.* 현장 위치 추정 문제를 보자. 한 벽면에 비콘 셋이
$a = (0,0), (8,0), (20,0)$에 있고 참 위치는 $(10, 6)$이다. 솔버를 *벽 위에서*, 즉 $(12, 0)$에서
초기화한다. 야코비의 각 행은 $(x - a_i)/\lVert x - a_i\rVert$이므로 $y = 0$에서는 모든 행의 둘째
성분이 0이고

$$J = \begin{bmatrix} 1 & 0 \\ 1 & 0 \\ -1 & 0 \end{bmatrix}, \qquad J^\top J = \begin{bmatrix} 3 & 0 \\ 0 & 0 \end{bmatrix}, \qquad \det J^\top J = 0$$

Gauss–Newton은 특이행렬의 역을 요구하고 멈춰 선다.

**Levenberg–Marquardt: 모델을 조절 가능한 만큼 불신한다.** 나쁜 국소모델에는 trust-region식
수락·거부와 짧은 스텝이 필요하지만, 랭크 결손 야코비안은 관측되지 않거나 퇴화한 방향을 뜻한다.
LM은 둘을 손잡이 하나 $\lambda_k$로 다룬다. 식을 보기 전에 두 가지를 기억해 두자:

1. **$\lambda$가 주는 것.** 긴 스텝에 값을 물려 아핀 모델을 믿을 수 있는 곳에 풀이를 붙잡아 두고, $J$가 랭크를 잃어도 선형계를 가역으로 만든다.
2. **$\lambda$를 정하는 법.** 시행으로 정한다: 참 잔차를 실제로 줄인 스텝 뒤에는 줄이고, 그렇지 못한 스텝 뒤에는 키운다.

**신뢰 영역 — LM이 그 한 판본인 발상.** 신뢰 영역 방법에는 이름 붙은 두 부분이 있다. (1) **부분 문제**: 반복점 주변 반경 $\Delta_k$의 공 안에서만 국소 모델을 최소화한다.
$$\min_{\delta}\ \lVert f(x_k)+J\delta\rVert^2\quad\text{s.t.}\quad\lVert\delta\rVert\le\Delta_k$$
모델을 그만큼까지만 믿기 때문이다. (2) 스텝을 사후에 채점하는 **이득 비** $\varrho_k=\big(F(x_k)-F(x_k+\delta)\big)/\big(\text{모델 감소량}\big)$, 즉 실제 감소를 예측 감소로 나눈 것. 흔한 규칙(Nocedal & Wright 4장)은 $\varrho_k\le0$이면 스텝을 거부하고, $\varrho_k<0.25$면 $\Delta$를 줄이며, $\varrho_k>0.75$이고 스텝이 경계에 닿았으면 키운다. 예: 모델이 $1.0$ 감소를 예측했을 때 실제 감소가 $0.9$면 $\varrho=0.9$(더 믿는다), $0.2$면 $\varrho=0.2$(스텝은 받되 $\Delta$를 줄인다), $0.1$만큼 오르면 $\varrho=-0.1$(거부)이다. LM의 $\lambda_k$는 그 공 제약의 라그랑주 승수(§4)이고, 그래서 $\lambda$를 키우는 것이 반경을 줄이는 것처럼 작동한다.

현재 반복점에서 멀어지는 것에 벌점을 매긴다. 위의 발산 예제가 그 이유다. 둘째 항이 아핀 모델이 유효하던 이웃을 벗어나는 데 값을 물리고, $\lambda_k$가 그 값을 정한다.

$$x_{k+1} = \arg\min_x \; \lVert f(x_k) + J(x - x_k) \rVert^2 + \lambda_k \lVert x - x_k \rVert^2$$

이것은 정규화된 최소자승 문제다. 닫힌 형태는 그 목적함수의 그래디언트를 0으로 놓으면 따라 나온다 — Gauss–Newton의 정규방정식에서 $J^\top J$에 $\lambda_k I$를 더한 것이다.

$$x_{k+1} = x_k - (J^\top J + \lambda_k I)^{-1} J^\top f(x_k)$$

$\lambda I$는 선형계를 가역으로 만들고 폭발적인 스텝을 제한하지만, 관측되지 않은 방향의
정보를 복원하거나 수렴을 보장하지는 않는다. 비콘 예제에서 그것은 $\det J^\top J = 0$을
$\det(J^\top J + I) = 4$로 바꾼다 — $J$가 무슨 짓을 하든 이제 행렬은 역을 갖는다. 그리고
$\lambda$는 보간한다. $\lambda \to 0$이면 Gauss–Newton이고, $\lambda$가 크면 그래디언트 방향의
짧은 한 걸음이다.

시행으로 조절한다. 스텝을 밟아 보고 *참* 잔차가 줄었으면 받아들이고
느슨하게 하며($\lambda \leftarrow 0.8\lambda$), 줄지 않았으면 스텝을 물리고 더 불신한다
($\lambda \leftarrow 2\lambda$). 뉴턴을 파괴했던 바로 그 $x_0 = 1.15$에서 $\tanh$ 문제를 이렇게
$\lambda_0 = 1$에서 시작해 풀면 여덟 스텝 만에 $|x| < 10^{-3}$에 닿는다(여기서는 $\lambda_0$가 작을수록 빠르고 클수록 느리다).

**계산 — 초기화의 값어치.** 같은 비콘 셋, 거리 $\rho = (11.66,\, 6.32,\, 11.66)$, 두 시작점에서
Gauss–Newton으로:

| 시작점 | $k=1$ | $k=2$ | $k=3$ | 수렴 | 시작점의 $\kappa(J)$ |
|---|---|---|---|---|---|
| $(12,\, 0.5)$ — 벽 근처 | $(10.3,\, \mathbf{32.3})$ | $(9.1,\, 8.1)$ | $(10.08,\, 6.14)$ | 5스텝 | 13.1 |
| $(12,\, 4)$ | $(10.2,\, 6.61)$ | $(9.99,\, 6.01)$ | $(10.0,\, 6.0)$ | 3스텝 | 1.8 |

둘 다 같은 답에 닿지만, 벽 근처에서 시작한 쪽은 회복하기 전에 추정치를 $y = 32.3$까지 —
참값의 다섯 배 — 던져 버린다. 실제 배포에서 그 이탈은 불가능한 곳으로 명령받은 로봇이고,
솔버에 신뢰 파라미터뿐 아니라 스텝 제한도 함께 주는 이유가 그것이다.

**읽을 때 이것이 사 주는 것 넷.**

- **감쇠 최소자승 역기구학이 *곧* Levenberg–Marquardt다.** IK 갱신식
  $\Delta q = J^\top (JJ^\top + \lambda I)^{-1} e$와 LM 갱신식
  $\Delta q = (J^\top J + \lambda I)^{-1} J^\top e$는 같은 식이고, 기계 정밀도까지 일치한다.
  특이 자세 근처에서 팔이 폭발하는 것을 막는 그 $\lambda$
  ([[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장]])는 임시방편이 아니라 신뢰
  파라미터다.
- **조건수가 제곱된다.** 열 랭크가 가득 찬 $J$의 2-노름에서는
  $\kappa(J^\top J) = \kappa(J)^2$이므로, 조건수 100인
  야코비는 정규방정식에서 $10^4$이 된다
  ([[02-foundations/linear-algebra|1. 선형대수 §3]]. 특이값 비로 정의하는 곳이다). QR은 조건수를 명시적으로 제곱하지 않아
  조밀 문제에서 흔히 더 안전하다. 반면 희소 normal-Cholesky는 $J^\top J$를 만들더라도
  희소성과 속도 때문에 실제 솔버에서 쓰이며, 수치적 대가를 관리해야 한다. 논문이 특이 자세
  근처의 수치 문제를 보고할 때 이 조건수 기전이 살펴볼 곳 중 하나다.
- **이것은 발견적 방법이고, 논문들도 안다.** Levenberg–Marquardt에는 전역 최솟값에 닿는다는
  보장이 없다 — $k$-평균과 마찬가지로, 그래도 어디서나 쓰인다. 이 문헌이 직전 해에서
  웜스타트하고, 여러 초기값에서 다시 돌리고, 그중 최선을 보고하는 이유다. SLAM이나 보정
  논문이 "Ceres / g2o / GTSAM으로 푼다"고 써도 비선형 최소자승 프레임워크를 썼다는 단서일
  뿐이다. 실제 선형화, trust-region/line-search 방법, 선형 솔버, 강건 손실 설정을 확인해야
  하며, 라이브러리 이름만으로 이 알고리즘이나 전역 최적해를 알 수는 없다.
- **필터도 이 같은 스텝을 돌리고 있다.** Gauss–Newton 한 번의 반복은 iterated 확장 칼만
  필터가 적용하는 갱신과 대수적으로 같다 — 같은 가중 잔차 비용을 공분산 형태가 아니라 정보
  형태로 적었을 뿐이다. 그러므로 "최적화 기반"과 "필터 기반" 상태 추정기의 익숙한 구분은
  어떤 변수를 남길 것인가의 선택이지, 서로 다른 문제를 푸는 것이 아니다
  ([[04-robotics/state-estimation-slam|상태 추정과 SLAM §5]]).

### 4. 제약 최적화 — 라그랑주, KKT, 쌍대성

- **왜 제약을 목적함수에 더하나?** 제약 최적점에서는 제약을 어기지 않고는 $f$를 더 내릴
  수 없다 — *하강* 방향 $-\nabla f$가 활성 제약의 금지 영역 쪽을 정면으로 가리키므로,
  $\nabla f$ 자신은 실행 가능 영역 쪽을 향한다. 어떤
  $\lambda \ge 0$에 대해 $\nabla f = -\lambda\nabla g$(두 그래디언트가 반평행)가 된다.
  정리하면 $\nabla(f + \lambda g) = 0$ — 그래서 결합된 **라그랑지안**의 그래디언트를 0으로 놓으면 실행
  가능한 하강 방향이 남지 않는 후보점을 정확히 찾는다(비볼록 문제에서는 그 점이 라그랑지안의 최소가 아니라 안장점일 수도 있다).

<svg viewBox="0 0 560 266" style="max-width:100%;height:auto" role="img" aria-label="제약 최적점에서 목적함수의 그래디언트와 제약의 그래디언트가 한 직선 위에서 서로 반대를 향한다">
  <defs><marker id="opAk" markerWidth="8" markerHeight="8" refX="7" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" fill-opacity="0.07">
    <polygon points="60,180 360,80 360,190 60,190"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <line x1="60" y1="180" x2="360" y2="80"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.5">
    <circle cx="300" cy="60" r="18"/>
    <circle cx="300" cy="60" r="37.9"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.28" stroke-dasharray="4 3">
    <circle cx="300" cy="60" r="58"/>
  </g>
  <g stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#opAk)">
    <line x1="312" y1="96" x2="329.4" y2="148.2"/>
    <line x1="312" y1="96" x2="294.6" y2="43.8"/>
  </g>
  <g fill="currentColor"><circle cx="312" cy="96" r="3.6"/><circle cx="300" cy="60" r="2.6" opacity="0.6"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="70" y="164">실행 가능 영역 &#183; g(x) &#8804; 0</text>
    <text x="322" y="104">x&#8902;</text>
    <text x="336" y="152">&#8711;f</text>
    <text x="266" y="42">&#8711;g</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8">
    <text x="366" y="82">g(x) = 0</text>
    <text x="366" y="120">한 직선 위, 반대 방향</text>
    <text x="366" y="58">제약이 없었다면 f가 갈 곳</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">제약 최적점에서는 실행 가능 영역 안으로 f를 더 내리는 방향이 남아 있지 않다. 그 말은 &#8722;&#8711;f가</text>
    <text x="24" y="228">경계를 똑바로 뚫고 나가려 한다는 뜻이고, 그것은 다시 &#8711;f와 &#8711;g가 한 직선 위에서 반대를 향한다는</text>
    <text x="24" y="244">뜻이다. &#955; &#8805; 0이 두 벡터의 길이 비이고, &#8711;(f + &#955;g) = 0은 이 그림을 한 줄로 적은 것이다 &#8212;</text>
    <text x="24" y="260">라그랑지안을 만들 값어치가 있는 이유가 그것이다.</text>
  </g>
</svg>

- **라그랑지안**: $\mathcal{L}(x,\lambda,\nu) = f(x) + \sum_i \lambda_i g_i(x) + \sum_j \nu_j h_j(x)$, $\lambda_i \ge 0$
  - **부분들, 각각의 이름.** 결정 변수와 제약마다 하나씩인 **승수**의 스칼라 함수다. 부등식 $g_i\le0$에는 $\lambda_i$, 등식 $h_j=0$에는 $\nu_j$가 붙는다. 부등식 승수는 음수일 수 없다. $\lambda_i g_i$가 위반($g_i>0$)에 대한 벌점으로만 작동하고 보상이 되면 안 되기 때문이다. 등식은 어느 쪽으로도 어길 수 있으므로 등식 승수의 부호는 자유다.
  - **예.** 아래의 반공간 투영 $\min\tfrac12\lVert x-p\rVert^2$ s.t. $a^\top x-b\le0$의 라그랑지안은 $\mathcal{L}(x,\lambda)=\tfrac12\lVert x-p\rVert^2+\lambda(a^\top x-b)$이고, $\nabla_x\mathcal{L}=x-p+\lambda a=0$이 거기서 쓰는 정상성 식이다.
- **KKT 조건** (제약이 있는 1차 최적성):
  1. 정상성: $\nabla_x \mathcal{L} = 0$
  2. 원 가능성: $g_i \le 0,\ h_j = 0$
  3. 쌍대 가능성: $\lambda_i \ge 0$
  4. **상보 여유성**: $\lambda_i\, g_i = 0$ — 제약은 구속되거나($g_i=0$, 가격
     $\lambda_i>0$) 놀거나($\lambda_i = 0$) 둘 중 하나다.

  조건 1을 후보 $x^\star$와 승수 $\lambda^\star,\nu^\star$에서 완전히 쓰면:
  $$\nabla f(x^\star)+\sum_{i=1}^{m}\lambda_i^\star\nabla g_i(x^\star)+\sum_{j=1}^{p}\nu_j^\star\nabla h_j(x^\star)=0$$
  즉 목적함수의 그래디언트가 제약 그래디언트들의 비음 결합과 정확히 균형을 이룬다. 위 그림의 다중 제약 판이다. $g_i(x^\star)=0$(점이 경계 위)이면 그 제약은 **활성**, $g_i(x^\star)<0$이면 **비활성**이다. 상보 여유성은 활성 제약만 0이 아닌 승수를 가질 수 있다고 말한다. 등식 제약은 항상 활성이다.

  쉽게 말해: KKT는 솔버가 최적 후보를 알아보는 점검표다. 최적점이 반드시 이 점검을 통과하는지, 통과하면 최적이 증명되는지는 문제에 따라 다르다.
  - **필요조건.** 함수가 미분 가능하면 이 조건들은 강쌍대성이 성립하는 모든 최적점에서 **필요하다**. 볼록 문제에서는 Slater 조건(모든 부등식을 엄격히, 곧 $g_i(x) < 0$으로 만족하는 실현 가능한 점이 하나 있다는 조건) 같은 제약 자격 조건이 강쌍대성을 준다(Boyd & Vandenberghe §5.5.3).
    일반 비볼록 문제의 국소 최소에서도 LICQ(선형 독립 제약 자격 조건: 그 점에서 등식 제약과 활성 부등식 제약의 그래디언트들이 선형 독립이라는 조건) 같은 제약 자격 조건 아래에서는 여전히 필요하다. SQP와 내점법 NLP 솔버가 기대는 것이 이것이다.
  - **충분조건.** 볼록 문제에서는 **충분조건이기도** 하다. 비볼록 문제 —
    비선형 MPC, 궤적 최적화, §5가 나열하는 부류 — 에서는 KKT 점이 최소점이 아닐 수도 있다.
  - **제약 자격 조건, 그리고 그것이 없을 때 생기는 일.** 제약 자격 조건은 ($f$가 아니라) *제약의 기하만*에 대한 조건으로, 그 점 근처에서 제약 그래디언트가 실행 가능 집합을 제대로 묘사함을 보장한다. 위의 Slater와 LICQ가 그 둘이다. 반례: $g(x)=x^2\le0$ 아래에서 $f(x)=x$를 최소화한다. 실행 가능한 점은 $x^\star=0$ 하나뿐이므로 그것이 최솟값이다. 그런데 $\nabla f=1$, $\nabla g(0)=2x^\star=0$이라 정상성 $1+\lambda\cdot0=0$을 만족하는 $\lambda$가 없다. 진짜 최솟값에서 KKT가 실패하는 것은 $x^2<0$을 만족하는 점이 없고(Slater 실패) 유일한 활성 그래디언트가 0이기(LICQ 실패) 때문이다.
- 계산 예제 — 반공간으로의 투영: $\min \tfrac12\|x - p\|^2$ s.t. $a^\top x \le b$.
  정상성: $x = p - \lambda a$. $a^\top p \le b$이면: $\lambda = 0$, $x^* = p$(제약이 논다).
  아니면 제약이 구속되어: $\lambda = (a^\top p - b)/\|a\|^2$, $x^* = p - \lambda a$ —
  정확히 투영 공식이다. 상보 여유성이 *곧* 이 경우 나누기다.
  **숫자로**: $p = (3,4)$, 제약 $x_1 + x_2 \le 5$이므로 $a = (1,1)$, $b = 5$. 실행 가능성부터
  확인하면 $a^\top p = 7 > 5$이라 제약이 활성이다. 그러면 $\lambda = (7-5)/2 = 1$,
  $x^* = (3,4) - 1(1,1) = (2,3)$. 검산: $2+3 = 5$ ✓(경계 위), 그리고 보정이 제약 직선에
  *수직*으로 움직였다 — 가장 짧게 빠져나오는 방향이다. 점이 $p = (1,1)$이었다면
  $a^\top p = 2 \le 5$이므로 $\lambda = 0$, $x^* = p$: 제약이 아무 대가도 요구하지 않는다는
  뜻이고, 그것이 승수 0의 의미다.
- **쌍대성**: $q(\lambda,\nu) = \min_x \mathcal{L}$은 최적값의 하한(약쌍대성); 볼록성 +
  제약 자격 조건에서 하한이 딱 맞는다. 승수 = **잠재 가격**: 제약을 풀어줄 때 최적값의
  민감도 — 스케줄링에서는 말 그대로 크레인 1시간 추가의 한계 가치다.
  - **부분들, 각각의 이름.** **쌍대 함수**는 승수를 고정한 채 라그랑지안을 $x$에 대해 최소화한 것이다.
    $$q(\lambda,\nu)=\inf_{x}\ \mathcal{L}(x,\lambda,\nu)$$
    $(\lambda,\nu)$에 아핀인 함수들의 점별 하한이므로 $f$가 무엇이든 $q$는 항상 오목하다. **약쌍대성**: 모든 $\lambda\ge0$과 임의의 $\nu$에서 $q(\lambda,\nu)\le p^\star$다. 실행 가능한 $x$에서는 더한 항이 $\lambda_ig_i\le0$, $\nu_jh_j=0$이기 때문이다. **쌍대 문제**는 그런 하한 중 최선인 $d^\star=\max_{\lambda\ge0,\,\nu}q(\lambda,\nu)$이다. **쌍대 간극**은 $p^\star-d^\star\ge0$이고, **강쌍대성**은 간극이 0이라는 뜻이다.
  - **잠재 가격을 식으로.** 제약 $i$를 $g_i(x)\le u_i$로 풀어 주고 새 최적값을 $p^\star(u)$라 하자. 강쌍대성이 성립하고 $p^\star$가 미분 가능하면 $\partial p^\star/\partial u_i=-\lambda_i^\star$이다. 작은 $u_i$만큼 제약을 느슨하게 하면 최적값이 약 $\lambda_i^\star u_i$만큼 내려간다.
  - **계산.** $x\ge1$, 즉 $g(x)=1-x\le0$ 아래에서 $x^2$을 최소화한다. 분명히 $x^\star=1$, $p^\star=1$이다. 라그랑지안 $x^2+\lambda(1-x)$는 $x=\lambda/2$에서 최소이므로 $q(\lambda)=\lambda-\lambda^2/4$다. $\lambda=1$이면 하한이 $q=0.75\le1$(약쌍대성)이고, 최댓값은 $\lambda^\star=2$에서 $d^\star=1=p^\star$(강쌍대성)이다. 제약을 $x\ge1.1$로 조이면($u=-0.1$) 최적값이 $1.21$로 $0.21$ 오르고, 예측값 $\lambda^\star\cdot0.1=0.2$에 가깝다.
- 알고리즘: 페널티/배리어는 제약을 목적함수에 굽고; **내부점법**은 배리어의 중심 경로를
  따른다(LP/QP 주력); **SQP**는 반복점마다 QP 모델을 푼다(비선형 MPC 주력); 단순한
  집합에는 투영 경사법.
  - **페널티법.** 가중치 $\mu$를 키워 가며 무제약 문제 $\min_x f(x)+\frac{\mu}{2}\sum_i\max(0,g_i(x))^2$를 차례로 푼다. 반복점은 실행 불가능할 수 있고 $\mu\to\infty$에서 실행 가능성에 다가간다. $x\ge1$ 아래 $\min x^2$에서는 최소화점이 $\mu/(2+\mu)$라 $\mu=1,10,1000$에서 $0.333$, $0.833$, $0.998$로 항상 약간 실행 불가능하다.
  - **배리어와 내부점법.** 경계에서 폭발하는 로그 배리어로 반복점을 엄격히 실행 가능하게 유지하며, 배리어 가중치는 $t>0$다.
    $$\min_x\ f(x)-t\sum_{i}\log\big(-g_i(x)\big)$$
    $g_i\to0^-$일 때 $-\log(-g_i)\to\infty$이기 때문이다. 최소화점 $x^\star(t)$들이 **중심 경로**를 그리고, $t\to0$에서 참 최적점에 닿는다. 내부점법은 $t$를 줄이면서 뉴턴 스텝으로 이 경로를 따라간다. 같은 문제에서 $\min x^2-t\log(x-1)$은 $x^\star(t)=\big(1+\sqrt{1+2t}\big)/2$를 주어 $t=1,\,0.01,\,0.0001$에서 $1.366$, $1.005$, $1.00005$로 항상 약간 실행 가능하다.
  - **SQP**(순차 이차 계획법). 반복점 $x_k$에서 라그랑지안의 이차 모델을 목적함수로, 선형화한 제약 $g_i(x_k)+\nabla g_i(x_k)^\top\delta\le0$, $h_j(x_k)+\nabla h_j(x_k)^\top\delta=0$을 제약으로 하는 QP를 만든다. 스텝 $\delta$를 풀고, 갱신하고, 반복한다.
  - **투영 경사법.** 경사 스텝을 밟은 뒤 유클리드 투영 $\Pi_C(y)=\arg\min_{x\in C}\lVert x-y\rVert$로 실행 가능 집합 $C$에 되돌린다: $x_{k+1}=\Pi_C\big(x_k-\alpha\nabla f(x_k)\big)$. $\Pi_C$가 쌀 때만 실용적이고, 박스라면 투영이 곧 잘라내기다. 예: $C=[0,1]$에서 $x=0.8$, 그래디언트 $-2$, $\alpha=0.5$면 스텝이 $1.8$에 닿고 투영이 $1$로 되돌린다.

### 5. 로보틱스에 중요한 문제 부류

| 부류 | 형태 | 등장하는 곳 |
|---|---|---|
| LP | 선형 $f$, 선형 제약 | 자원 할당, 스케줄링 완화 |
| QP | 볼록 이차 $f$, 선형 제약 | **선형 MPC**, 궤적 평활화, 역동역학 |
| NLP | 비선형 | 비선형 MPC, 궤적 최적화, 캘리브레이션 |
| MIP | 정수 변수 | 작업 배정, 공정 순서 (branch & bound) |
| 전역 | 비볼록, 보증 | 직접 쓸 일은 드묾; MIP 솔버의 밑바닥 |

**표준형으로 쓴 부류들, 각각의 정의.**
- **LP**(선형 계획): 비용 벡터 $c\in\mathbb{R}^n$, 제약 행렬 $A\in\mathbb{R}^{m\times n}$, 경계 $b\in\mathbb{R}^m$으로
  $$\min_x\ c^\top x\quad\text{s.t.}\quad Ax\le b$$
  그래서 목적함수와 모든 제약이 아핀이고, 실행 가능 집합은 다면체이며, 최적해가 있으면 꼭짓점에서 하나를 찾을 수 있다. 예: $\min -x_1-2x_2$ s.t. $x_1+x_2\le4$, $x_2\le3$, $x\ge0$. 꼭짓점 $(0,0)$, $(4,0)$, $(1,3)$, $(0,3)$이 $0,\ -4,\ -7,\ -6$을 주므로 $x^\star=(1,3)$이다.
- **QP**(이차 계획): LP의 제약에 이차 목적함수, $\min_x\tfrac12x^\top Px+q^\top x$ s.t. $Ax\le b$이고, 정확히 $P\succeq0$일 때 볼록이다. 비볼록 QP($P$에 음의 고유값)는 일반적으로 NP-난해이고, 표가 *볼록* 이차라고 쓴 이유다.
- **NLP**(비선형 계획): $f$, $g_i$, $h_j$ 중 하나라도 비선형인 §1의 일반형이다. 볼록이든 아니든 SQP나 내부점법으로 KKT 점까지 푼다.
- **MIP**(혼합 정수 계획): 위의 어느 것이든 일부 변수를 정수 $x_i\in\mathbb{Z}$(예/아니오 결정이면 흔히 $\{0,1\}$)로 제한한 것이다. 정수 조건이 실행 가능 집합을 비볼록으로 만든다. **분기 한정법**(branch and bound)은 정수 조건을 버려 하한을 얻고(*완화*), 분수값 변수에서 가지를 나누며($x_i\le\lfloor\cdot\rfloor$ 또는 $x_i\ge\lceil\cdot\rceil$), 하한이 이미 찾은 최선의 정수해보다 나쁜 가지를 버린다.

**MPC를 QP로 완전히 써보기** ([[04-robotics/index|제어 트랙]]): 선형 동역학
$x_{t+1} = Ax_t + Bu_t$, 지평 $N$, 단계 비용 $x^\top Q x + u^\top R u$,
$Q,P\succeq0$, $R\succ0$, 다면체 상태 집합 $\mathcal X=\{x:Hx\le h\}$:

$$\min_{u_0..u_{N-1}} \sum_{t=0}^{N-1}\big(x_t^\top Q x_t + u_t^\top R u_t\big) + x_N^\top P x_N \quad \text{s.t. } x_{t+1} = Ax_t + Bu_t,\; u_{min}\le u_t \le u_{max},\; x_t \in \mathcal{X}$$

유한 지평에 경성 제약을 다시 붙인 LQR 비용으로 읽어라. 동역학은 등식 제약으로 들어오고, 그것을 대입해 없애면(응축) $u$들에 대한 볼록 QP만 남는다. 작고 구조화된 QP는 적절한 솔버와
구현에서 ms급도 가능하므로 deadline과 최악 실행시간을 함께 보고해야 한다. MPC는 매 제어
주기에 다시 풀고 첫 입력만 적용한다.

**모든 기호, 그리고 이것을 MPC로 만드는 루프.** $x_t\in\mathbb{R}^{n}$은 측정한 상태 $x_0$에서 시작해 $t$스텝 뒤를 예측한 상태, $u_t\in\mathbb{R}^{p}$는 입력이자 결정 변수, $A$와 $B$는 동역학 행렬(LP의 $A$가 아니다), $N$은 앞을 내다보는 스텝 수인 **지평**이다. $Q$는 상태 오차, $R$은 입력 크기에 가중치를 주고($R\succ0$이 $u$에 대해 엄격 볼록을 유지한다), $P$는 $N$스텝 이후 전부를 대신하는 **종단 비용**이다. $H$와 $h$는 허용 상태를 기술한다(여기서 $H$는 제약 행렬이지 헤시안이 아니다). **모델 예측 제어**는 매 샘플링 주기에 반복하는 세 단계다. (1) $x_0$를 측정하고, (2) $u_0,\ldots,u_{N-1}$에 대한 QP를 풀고, (3) $u_0$만 적용하고 나머지는 버린다(**이동 지평**).

> [!example] 계산 예제 · Worked example
> 스칼라 시스템 $x_{t+1}=x_t+u_t$, $N=1$, $Q=R=P=1$, 측정값 $x_0=1$. 비용은 $x_0^2+u_0^2+(x_0+u_0)^2=1+u_0^2+(1+u_0)^2$이고 $2u_0+2(1+u_0)=0$에서 최소이므로 $u_0=-0.5$, 비용 $1.5$다. 입력 제한 $|u_0|\le0.2$를 더하면 무제약 답이 실행 불가능해져 제약이 활성이 되고, $u_0=-0.2$, 비용은 $1+0.04+0.64=1.68$로 오른다. 완전한 전개는 [[04-robotics/mpc|7. MPC]].

### 6. 최적화의 눈으로 이 위키 읽기

- 네트워크 학습 = 확률적 비볼록 최적화 ([[01-canonical-papers/notes/1-foundations/adam|Adam]];
  [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]은 지형의 조건수를 다듬는다 — 여러 제안된 기제 중 하나).
- [[01-canonical-papers/notes/1-foundations/lora|LoRA]] = 업데이트를 저랭크 매개화로 제약.
- [[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]]의 KL 페널티 = 부드러운 신뢰 영역 제약.
- 디퓨전 학습 = 변분 하한 최소화; [[01-canonical-papers/notes/5-world-models/planet|PlaNet]]의 CEM 플래닝 =
  잠재 공간의 미분 불요 최적화.

> [!tip] 더 깊이 · Going deeper
> 다음 단계의 정본은 Boyd·Vandenberghe의 [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/)이다 — 무료이고, MPC 논문들이 암묵적으로 인용하는 그 책이다. 2~5장이 볼록성·쌍대성·KKT를 제대로 다룬다. 비볼록 쪽은 Nocedal·Wright의 *Numerical Optimization*.

### 스스로 점검

1. 두 볼록 함수의 max가 볼록임을 보이고, 이를 써서 힌지 손실이 볼록임을 논증하라.
2. 고유값 $\{1, 100\}$인 $f(x) = \tfrac12 x^\top H x$에서: 안정한 최대 스텝은? 느린
   모드를 100배 줄이는 데 몇 번의 반복이 필요한가?
3. 투영 예제의 구속 케이스에서 KKT 네 조건을 전부 검증하라.
4. 위 MPC 문제는 왜 볼록인가? 실전에서 무엇이 비볼록으로 만들 수 있는가?
   (힌트: 장애물 회피 제약.)
5. 두 가중치가 모두 1이고 $\sqrt{\hat v} = 10$, $\sqrt{\hat v} = 0.1$이다. $\eta = 10^{-3}$,
   $\lambda = 10^{-2}$, 모멘텀 없음일 때, Adam + L2와 AdamW에서 각각 스텝당 얼마나 줄어드는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 함수의 에피그래프(epigraph)는 그래프 위 또는 그 위쪽 점들의 집합 $\{(x,t) : t \ge f(x)\}$이고, 함수가 볼록인 것은 에피그래프가 볼록 집합인 것과 정확히 같다. $t \ge \max(f,g)$는 $t \ge f$이면서 $t \ge g$라는 뜻이므로, $\max(f,g)$의 에피그래프는 두 볼록 에피그래프의 교집합 — 볼록. 힌지 $\max(0, 1-yx)$는 아핀 함수 둘의 max라 볼록이다.
> 2. 안정 조건 $\alpha < 2/\lambda_{max} = 0.02$. 실전 관례대로 한계의 절반 $\alpha = 0.01$을 잡으면(경계 근처는 빠른 모드가 진동한다) 느린 모드는 $(1-0.01)^k = 0.99^k$로 수축; $0.99^k = 0.01 \Rightarrow k = \ln 0.01/\ln 0.99 \approx 458$회. 조건수 $\kappa = 100$이 *곧* 그 대가다.
> 3. 구속 케이스: 정상성은 $x^* = p - \lambda a$로 성립; $a^\top x^* = b$(원 가능·구속); $\lambda = (a^\top p - b)/\|a\|^2 > 0$(쌍대 가능); $\lambda g = \lambda \cdot 0 = 0$(상보 여유성).
> 4. 목적은 볼록 이차, 제약은 선형(동역학 등식 + 박스) — 볼록 QP. 장애물 회피(비볼록 여집합)나 정수 결정(작업 순서, 접촉 모드 선택)이 들어오면 비볼록이 된다.
> 5. Adam + L2: 감쇠항 $\eta\lambda w/\sqrt{\hat v}$는 첫 가중치에서 $10^{-6}$, 둘째에서 $10^{-4}$ — 그래디언트 이력이 만든 100배 차이다($\lambda w$가 $\hat v$에 주는 작은 영향은 무시). AdamW: 둘 다 $\eta\lambda w = 10^{-5}$.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P1**. 경사 한 스텝, 손계산. 주어진 그래디언트의 역전파는 [[02-foundations/calculus-backprop|2]]에 있다. 여기서 다시 유도하지 마라.

1. **그리기.** 첫째가 아니라 셋째 가중치에 대한 위의 그림: $W_{2,1}=1$, $W_{2,2}=-1$, $h=(1,2,3)$을 고정하고 $L=\tfrac12(\hat y-1)^2$를 $0.5$ 근처의 $W_{2,3}$의 함수로 그린다. 카탈로그 점과 그 접선, 이 가중치만 움직이는 스텝 $\eta=0.1$, 그리고 이 단면에서 꼭짓점에 내려앉는 스텝 크기와 발산하는 스텝 크기를 표시하라. 이 포물선은 왜 위 그림의 것보다 좁은가?
2. **유도.** GD 한 스텝 $W_2\leftarrow W_2-\eta\,\partial L/\partial W_2$, $\eta=0.1$, $\partial L/\partial W_2=(-0.5,-1,-1.5)$, 출발 $W_2=(1,-1,0.5)$.
3. **해석.** $\eta=10$으로 반복. 새 $W_2$, $L$은?

> [!note]- 그리는 법 · How to draw it
> - 축은 $W_{2,3}$(대략 $0.3$부터 $1$)과 $L$($0$부터 약 $0.6$). $h=(1,2,3)$과 나머지 두 가중치를 카탈로그 값에 고정하면 $\hat y=3W_{2,3}-1$이므로, 곡선은 꼭짓점이 $(0.667,\ 0)$인 포물선 $L=\tfrac12(3W_{2,3}-2)^2=\tfrac92(W_{2,3}-\tfrac23)^2$이다.
> - 카탈로그 점 $W_{2,3}=0.5$는 높이 $L=0.125$에 찍는다. 두 단면이 모두 카탈로그 상태를 지나므로 위 그림과 같은 손실이고, 점이 다른 높이에 있으면 단면을 잘못 자른 것이다.
> - 그 점의 접선과 그 기울기 $\partial L/\partial W_{2,3}=3(3\cdot0.5-2)=-1.5$. 2번이 쓰는 그래디언트의 셋째 성분이다.
> - 스텝을 기울기 *반대* 방향 수평 화살표로, 같은 축척으로 그린다. $\eta=0.1$은 이 가중치를 $0.15$ 옮겨 $0.65$($L=0.00125$)에 놓고, 꼭짓점 바로 앞이다.
> - 곡률이 $h_3^2=9$인 이 단면에서 스텝 크기가 하는 일을 축 위 눈금 셋으로: $\eta=1/9=0.111$은 꼭짓점에 정확히 내려앉고, $2/9=0.222$까지는 그래도 수렴하며, 그것을 넘기면 반복점이 걸어 나간다.
> - 위 그림의 포물선을 같은 축척으로, 두 카탈로그 점이 겹치게 옮겨 흐리게 겹쳐 그린다. 곡률 $1$ 대 $9$다. $W_{2,1}$을 따라서는 꼭짓점까지의 십분의 일만 기어가는 같은 $\eta=0.1$이 $W_{2,3}$을 따라서는 십분의 구를 간다.
> - 2번과 3번은 가중치 셋을 다 움직인다. 그 숫자는 이 단면에 올리지 말거나, 구석 상자에 "전체 스텝"이라고 적어 따로 둔다.

> [!tip]- 정답 · Solutions
> 1. $\hat y=1-2+3W_{2,3}=3W_{2,3}-1$이므로 $L=\tfrac12(3W_{2,3}-2)^2=\tfrac92(W_{2,3}-\tfrac23)^2$, $0.667$에서 최소다. 카탈로그 $W_{2,3}=0.5$는 왼쪽 기울기 위 $L=0.125$에 있고, 기울기는 $\partial L/\partial W_2$의 셋째 성분인 $-1.5$다. 곡률은 $h_3^2=9$로 첫째 단면의 $h_1^2=1$의 아홉 배이고, 그래서 포물선이 좁다. 이 가중치만 $\eta=0.1$로 움직이면 $0.15$를 가서 $0.65$($L=0.00125$), 꼭짓점 바로 앞에 선다. $\eta=1/9=0.111$은 꼭짓점에 내려앉고 $\eta>2/9=0.222$는 발산한다. 한 가중치 방향의 곡률은 그 가중치가 곱하는 활성값의 제곱이므로, 학습률 하나가 가중치마다 뉴턴 스텝의 다른 몫이 된다.
> 2. $W_2\leftarrow(1,-1,0.5)-0.1(-0.5,-1,-1.5)=(1.05,-0.9,0.65)$.
> 3. $W_2\leftarrow(1,-1,0.5)+(5,10,15)=(6,9,15.5)$. $\hat y=70.5$, $L$이 폭발. $\eta=10$은 이 척도에서 안정 스텝을 한참 지난다.

### 로보틱스 다리

제약 최적화와 QP는 [[04-robotics/mpc|7. MPC]]와 [[04-robotics/planning-decision-making|4. 계획]]의 궤적 최적화에서 그대로 다시 나온다.
