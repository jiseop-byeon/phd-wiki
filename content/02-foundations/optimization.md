---
title: 4. Optimization
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §1–2]] (gradients, Taylor) · [[02-foundations/linear-algebra|1. Linear Algebra §3]] (eigenvalues, SPD, condition number) · [[02-foundations/calculus-backprop|2. Calculus §1]] (the Hessian)
> [[02-foundations/engineering-math|0.5 §1–2]](그래디언트·테일러) · [[02-foundations/linear-algebra|1. 선형대수 §3]](고유값·SPD·조건수) · [[02-foundations/calculus-backprop|2. 미적분 §1]](헤시안)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*[[02-foundations/probability|3. Probability]] handed you an objective. This page minimizes it, constraints included, which is where
convexity and KKT earn their keep. Then [[02-foundations/information-theory|5. Information Theory]] says what those objectives measure.*

Optimization is the shared language of this wiki: training a network
([[01-canonical-papers/notes/1-foundations/adam|Adam]]), solving MPC, planning a trajectory, and allocating
construction tasks are all "minimize an objective subject to constraints." Course-depth
treatment: conditions, derivations, and a fully written MPC-as-QP example.

### 1. Anatomy of a problem

$$\min_{x \in \mathbb{R}^n} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; h_j(x) = 0$$

Decision variables, objective, inequality/equality constraints. Formulation is half the
work: *what is a variable, what is a constraint, what is the objective* — and often several
formulations of the same engineering problem differ wildly in solvability.

### 2. Convexity — the great divide

- A set is convex if it contains all line segments between its points; $f$ is convex if
  $f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda)f(y)$ — equivalently
  (twice-differentiable case) $H \succeq 0$ everywhere — read $\succeq 0$ as "positive
  semidefinite", the matrix version of $\ge 0$: $x^\top H x \ge 0$ for every direction $x$,
  i.e. the surface curves upward (or at worst is flat) whichever way you walk.
- Convex problem = convex $f$ over a convex feasible set ⇒ **every local minimum is
  global**, and polynomial-time reliable solvers exist.

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
  but not the second — and dominate high-dimensional landscapes.
- **Gradient descent** from Taylor: minimizing the first-order model within a step-size
  trust gives $x_{k+1} = x_k - \alpha\nabla f(x_k)$. On a quadratic with Hessian $H$, the
  per-eigendirection contraction is $|1 - \alpha\lambda_i|$; stability needs
  $\alpha < 2/\lambda_{max}$, so the slow direction converges like
  $(1 - \lambda_{min}/\lambda_{max})^k$ — **the condition number $\kappa$ is the pain**
  ([[02-foundations/linear-algebra|linear algebra]]).
- **Gradient descent vs Newton, in one line of arithmetic.** Take $f(x) = 5x^2$, so
  $f'(x) = 10x$ and $f''(x) = 10$, starting at $x_0 = 1$. Gradient descent with
  $\alpha = 0.05$ gives $x_1 = 1 - 0.05(10) = 0.5$, then $0.25$, then $0.125$ — halving every
  step, so about 10 steps to reach $10^{-3}$. Newton divides by the curvature instead:
  $x_1 = 1 - \frac{f'(1)}{f''(1)} = 1 - \frac{10}{10} = 0$ — **exact, in a single step**,
  because a quadratic is precisely the model Newton assumes. Worth seeing once: Newton's
  speed is not magic, it is the payoff for owning the second derivative. On a non-quadratic
  you get that behavior only near the optimum, and you pay $O(n^3)$ per step to form and
  invert $H$ — which is why nobody runs it on a neural network.
- **Momentum** accumulates a velocity to average out oscillation across ill-conditioned
  valleys; **Newton** minimizes the *second*-order model,
  $x_{k+1} = x_k - H^{-1}\nabla f$ — quadratic convergence near the optimum, $O(n^3)$ per
  step; quasi-Newton (BFGS/L-BFGS) builds $H^{-1}$ estimates from gradient differences.
- Stochastic gradients: unbiased but noisy estimates from minibatches; noise ~ helps escape
  saddles, demands step-size decay or adaptivity — [[01-canonical-papers/notes/1-foundations/adam|Adam]] ≈
  momentum + per-coordinate curvature proxy.

### 4. Constrained optimization — Lagrange, KKT, duality

- **Why add the constraint to the objective at all?** At a constrained optimum, you can't
  descend $f$ without violating a constraint — the *descent* direction $-\nabla f$ points
  straight into the active constraint's forbidden side, so $\nabla f$ itself points back into
  the feasible region, anti-parallel to $\nabla g$: $\nabla f = -\lambda\nabla g$ for some
  $\lambda \ge 0$ (the two gradients are anti-parallel). Rearranged, that is
  $\nabla(f + \lambda g) = 0$ — so minimizing the combined **Lagrangian** finds exactly the
  points where no feasible descent direction remains.
- **Lagrangian**: $\mathcal{L}(x,\lambda,\nu) = f(x) + \sum_i \lambda_i g_i(x) + \sum_j \nu_j h_j(x)$, $\lambda_i \ge 0$.
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
- Algorithms: penalty/barrier methods bake constraints into the objective;
  **interior-point** follows the barrier central path (the LP/QP workhorse); **SQP**
  solves a QP model at each iterate (the nonlinear-MPC workhorse); projected gradient for
  simple sets.

### 5. Problem classes that matter for robotics

| Class | Form | Where it appears |
|---|---|---|
| LP | linear $f$, linear constraints | resource allocation, scheduling relaxations |
| QP | convex quadratic $f$, linear constraints | **linear MPC**, trajectory smoothing, inverse dynamics |
| NLP | nonlinear | nonlinear MPC, trajectory optimization, calibration |
| MIP | integer variables | task assignment, construction sequencing (branch & bound) |
| Global | non-convex, certified | rarely needed directly; underneath MIP solvers |

**MPC as a QP, written out** ([[04-robotics/index|control track]]): linear dynamics
$x_{t+1} = Ax_t + Bu_t$, horizon $N$, stage cost $x^\top Q x + u^\top R u$:

$$\min_{u_0..u_{N-1}} \sum_{t=0}^{N-1}\big(x_t^\top Q x_t + u_t^\top R u_t\big) + x_N^\top P x_N \quad \text{s.t. } x_{t+1} = Ax_t + Bu_t,\; u_{min}\le u_t \le u_{max},\; x_t \in \mathcal{X}$$

Substituting the dynamics (condensing) leaves a convex QP in the $u$'s — solved in
milliseconds by interior-point/active-set solvers, re-solved every control step with the
first input applied. *MPC = the projection example scaled up, a thousand times a second.*

### 6. Reading this wiki through optimization

- Network training = stochastic non-convex optimization
  ([[01-canonical-papers/notes/1-foundations/adam|Adam]]; [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]
  reshapes the landscape's conditioning — one proposed mechanism among several).
- [[01-canonical-papers/notes/1-foundations/lora|LoRA]] = restricting the update to a low-rank parameterization.
- [[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]]'s KL penalty = a soft trust-region constraint.
- Diffusion training = minimizing a variational bound; [[01-canonical-papers/notes/5-world-models/planet|PlaNet]]'s
  CEM planning = derivative-free optimization in latent space.

### Self-check

1. Show that the max of two convex functions is convex, and use it to argue hinge loss is convex.
2. For $f(x) = \tfrac12 x^\top H x$ with eigenvalues $\{1, 100\}$: what is the largest
   stable step size, and how many iterations to shrink the slow mode by 100×?
3. In the projection example, verify all four KKT conditions in the binding case.
4. Why is the MPC problem above convex, and what could make it non-convex in practice?
   (Hint: obstacle avoidance constraints.)

> [!tip]- Answers
> 1. The epigraph of $\max(f,g)$ is the intersection of two convex epigraphs, hence convex. Hinge loss $\max(0, 1-yx)$ is the max of two affine functions, so it is convex.
> 2. Stability needs $\alpha < 2/\lambda_{max} = 0.02$. Taking the usual half-of-the-limit $\alpha = 0.01$ (near the boundary the fast mode oscillates), the slow mode contracts as $(1-\alpha\lambda_{min})^k = 0.99^k$; $0.99^k = 0.01 \Rightarrow k = \ln 0.01/\ln 0.99 \approx 458$ iterations. The condition number $\kappa = 100$ *is* that cost.
> 3. Binding case: stationarity holds by construction, $x^* = p - \lambda a$; primal feasibility $a^\top x^* = b$ (active); dual feasibility $\lambda = (a^\top p - b)/\|a\|^2 > 0$ precisely because the constraint was violated at $p$; complementary slackness $\lambda g = \lambda\cdot 0 = 0$.
> 4. The objective is a convex quadratic and the constraints are linear (dynamics equalities plus input/state boxes) — a convex QP. It stops being convex when obstacle avoidance enters (the free space is a non-convex complement) or when discrete decisions such as task ordering or contact-mode selection are added.

### Robotics bridge

Constraints and nonlinear optimization become executable robot decisions in [[04-robotics/planning-decision-making|Planning & Decision-Making]] and [[04-robotics/mpc|MPC]].

## 한국어

*[[02-foundations/probability|3. 확률]]이 목적함수를 건넸다. 이 페이지는 그것을 최소화한다 — 제약이 붙은 경우까지, 볼록성과
KKT가 값을 하는 자리가 거기다. 그다음 [[02-foundations/information-theory|5. 정보이론]]이 그 목적함수들이 무엇을 재는지 말한다.*

최적화는 이 위키의 공용 언어다: 네트워크 학습([[01-canonical-papers/notes/1-foundations/adam|Adam]]),
MPC 풀기, 궤적 계획, 건설 작업 할당이 모두 "제약 아래 목적함수 최소화"다. 교재 수준의
서술: 조건, 유도, 그리고 완전히 써 내려간 MPC-QP 예제.

### 1. 문제의 구조

$$\min_{x \in \mathbb{R}^n} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; h_j(x) = 0$$

결정 변수, 목적함수, 부등식/등식 제약. 정식화가 일의 절반이다: *무엇이 변수이고, 무엇이
제약이고, 무엇이 목적인가* — 같은 공학 문제라도 정식화에 따라 풀림성이 극적으로 달라진다.

### 2. 볼록성 — 결정적 분기점

- 집합이 볼록 = 두 점 사이 선분을 모두 포함; $f$가 볼록 =
  $f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda)f(y)$ — (2차 미분 가능하면)
  모든 곳에서 $H \succeq 0$과 동치 — $\succeq 0$은 "양의 준정부호"로 읽고, $\ge 0$의 행렬판이다:
  모든 방향 $x$에 대해 $x^\top H x \ge 0$, 즉 어느 방향으로 걸어도 표면이 위로 휘거나
  (최악의 경우) 평평하다는 뜻.
- 볼록 문제 = 볼록 가능 영역 위의 볼록 $f$ ⇒ **모든 지역 최솟값이 전역**이고,
  다항 시간의 신뢰할 수 있는 솔버가 존재한다.

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
  지배한다.
- 테일러에서 나오는 **경사 하강**: 1차 모델을 신뢰 반경 안에서 최소화하면
  $x_{k+1} = x_k - \alpha\nabla f(x_k)$. 헤시안 $H$의 이차 함수에서 고유방향별 수축률은
  $|1 - \alpha\lambda_i|$; 안정성엔 $\alpha < 2/\lambda_{max}$가 필요해 느린 방향은
  $(1 - \lambda_{min}/\lambda_{max})^k$처럼 수렴한다 — **조건수 $\kappa$가 곧 고통이다**
  ([[02-foundations/linear-algebra|선형대수]]).
- **경사 하강 vs 뉴턴법, 산수 한 줄로.** $f(x) = 5x^2$이면 $f'(x) = 10x$, $f''(x) = 10$이다.
  $x_0 = 1$에서 $\alpha = 0.05$의 경사 하강을 하면 $x_1 = 1 - 0.05(10) = 0.5$, 다음 $0.25$,
  그다음 $0.125$ — 매 스텝 절반이 되므로 $10^{-3}$에 닿는 데 약 10 스텝이 든다. 뉴턴법은 대신
  곡률로 나눈다: $x_1 = 1 - \frac{f'(1)}{f''(1)} = 1 - \frac{10}{10} = 0$ — **단 한 스텝에
  정확히** 도착한다. 이차 함수가 곧 뉴턴법이 가정하는 모델 그 자체이기 때문이다. 한 번은 봐둘
  값어치가 있다: 뉴턴법의 속도는 마법이 아니라 2차 도함수를 가진 값이다. 이차가 아닌 함수에서는
  최적점 근처에서만 이 거동이 나오고, 매 스텝 $H$를 만들고 역행렬을 구하는 데 $O(n^3)$을 낸다 —
  아무도 신경망에 이걸 돌리지 않는 이유다.
- **모멘텀**은 속도를 누적해 나쁜 조건의 골짜기에서 진동을 상쇄한다; **뉴턴법**은 *2차*
  모델을 최소화, $x_{k+1} = x_k - H^{-1}\nabla f$ — 최적점 근처 이차 수렴, 스텝당
  $O(n^3)$; 준뉴턴(BFGS/L-BFGS)은 그래디언트 차분으로 $H^{-1}$ 추정을 쌓는다.
- 확률적 그래디언트: 미니배치의 불편이지만 시끄러운 추정; 노이즈는 안장 탈출을 돕는 대신
  스텝 감쇠나 적응성을 요구한다 — [[01-canonical-papers/notes/1-foundations/adam|Adam]] ≈ 모멘텀 +
  좌표별 곡률 대리.

### 4. 제약 최적화 — 라그랑주, KKT, 쌍대성

- **왜 제약을 목적함수에 더하나?** 제약 최적점에서는 제약을 어기지 않고는 $f$를 더 내릴
  수 없다 — *하강* 방향 $-\nabla f$가 활성 제약의 금지 영역 쪽을 정면으로 가리키므로,
  $\nabla f$ 자신은 실행 가능 영역 쪽을 향한다. 어떤
  $\lambda \ge 0$에 대해 $\nabla f = -\lambda\nabla g$(두 그래디언트가 반평행)가 된다.
  정리하면 $\nabla(f + \lambda g) = 0$ — 그래서 결합된 **라그랑지안**을 최소화하면 실행
  가능한 하강 방향이 남지 않는 점을 정확히 찾는다.
<svg viewBox="0 0 560 266" style="max-width:100%;height:auto" role="img" aria-label="제약 최적점에서 목적함수의 그래디언트와 제약의 그래디언트가 한 직선 위에서 서로 반대를 향한다">
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
- **KKT 조건** (제약이 있는 1차 최적성):
  1. 정상성: $\nabla_x \mathcal{L} = 0$
  2. 원 가능성: $g_i \le 0,\ h_j = 0$
  3. 쌍대 가능성: $\lambda_i \ge 0$
  4. **상보 여유성**: $\lambda_i\, g_i = 0$ — 제약은 구속되거나($g_i=0$, 가격
     $\lambda_i>0$) 놀거나($\lambda_i = 0$) 둘 중 하나다.
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
- 알고리즘: 페널티/배리어는 제약을 목적함수에 굽고; **내부점법**은 배리어의 중심 경로를
  따른다(LP/QP 주력); **SQP**는 반복점마다 QP 모델을 푼다(비선형 MPC 주력); 단순한
  집합에는 투영 경사법.

### 5. 로보틱스에 중요한 문제 부류

| 부류 | 형태 | 등장하는 곳 |
|---|---|---|
| LP | 선형 $f$, 선형 제약 | 자원 할당, 스케줄링 완화 |
| QP | 볼록 이차 $f$, 선형 제약 | **선형 MPC**, 궤적 평활화, 역동역학 |
| NLP | 비선형 | 비선형 MPC, 궤적 최적화, 캘리브레이션 |
| MIP | 정수 변수 | 작업 배정, 공정 순서 (branch & bound) |
| 전역 | 비볼록, 보증 | 직접 쓸 일은 드묾; MIP 솔버의 밑바닥 |

**MPC를 QP로 완전히 써보기** ([[04-robotics/index|제어 트랙]]): 선형 동역학
$x_{t+1} = Ax_t + Bu_t$, 지평 $N$, 단계 비용 $x^\top Q x + u^\top R u$:

$$\min_{u_0..u_{N-1}} \sum_{t=0}^{N-1}\big(x_t^\top Q x_t + u_t^\top R u_t\big) + x_N^\top P x_N \quad \text{s.t. } x_{t+1} = Ax_t + Bu_t,\; u_{min}\le u_t \le u_{max},\; x_t \in \mathcal{X}$$

동역학을 대입(응축)하면 $u$들에 대한 볼록 QP만 남는다 — 내부점/active-set 솔버가 수
밀리초에 풀고, 매 제어 주기 첫 입력만 적용하며 다시 푼다. *MPC = 위의 투영 예제를
초당 천 번 규모로 키운 것.*

### 6. 최적화의 눈으로 이 위키 읽기

- 네트워크 학습 = 확률적 비볼록 최적화 ([[01-canonical-papers/notes/1-foundations/adam|Adam]];
  [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]은 지형의 조건수를 다듬는다 — 여러 제안된 기제 중 하나).
- [[01-canonical-papers/notes/1-foundations/lora|LoRA]] = 업데이트를 저랭크 매개화로 제약.
- [[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]]의 KL 페널티 = 부드러운 신뢰 영역 제약.
- 디퓨전 학습 = 변분 하한 최소화; [[01-canonical-papers/notes/5-world-models/planet|PlaNet]]의 CEM 플래닝 =
  잠재 공간의 미분 불요 최적화.

### 스스로 점검

1. 두 볼록 함수의 max가 볼록임을 보이고, 이를 써서 힌지 손실이 볼록임을 논증하라.
2. 고유값 $\{1, 100\}$인 $f(x) = \tfrac12 x^\top H x$에서: 안정한 최대 스텝은? 느린
   모드를 100배 줄이는 데 몇 번의 반복이 필요한가?
3. 투영 예제의 구속 케이스에서 KKT 네 조건을 전부 검증하라.
4. 위 MPC 문제는 왜 볼록인가? 실전에서 무엇이 비볼록으로 만들 수 있는가?
   (힌트: 장애물 회피 제약.)

> [!tip]- 스스로 점검 정답 · Answers
> 1. $\max(f,g)$의 에피그래프는 두 볼록 에피그래프의 교집합 — 볼록. 힌지 $\max(0, 1-yx)$는 아핀 함수 둘의 max라 볼록이다.
> 2. 안정 조건 $\alpha < 2/\lambda_{max} = 0.02$. 실전 관례대로 한계의 절반 $\alpha = 0.01$을 잡으면(경계 근처는 빠른 모드가 진동한다) 느린 모드는 $(1-0.01)^k = 0.99^k$로 수축; $0.99^k = 0.01 \Rightarrow k = \ln 0.01/\ln 0.99 \approx 458$회.
> 3. 구속 케이스: 정상성은 $x^* = p - \lambda a$로 성립; $a^\top x^* = b$(원 가능·구속); $\lambda = (a^\top p - b)/\|a\|^2 > 0$(쌍대 가능); $\lambda g = \lambda \cdot 0 = 0$(상보 여유성).
> 4. 목적은 볼록 이차, 제약은 선형(동역학 등식 + 박스) — 볼록 QP. 장애물 회피(비볼록 여집합)나 정수 결정(작업 순서)이 들어오면 비볼록이 된다.

### 로보틱스 다리

제약 최적화와 QP는 [[04-robotics/mpc|7. MPC]]와 [[04-robotics/planning-decision-making|4. 계획]]의 궤적 최적화에서 그대로 다시 나온다.
