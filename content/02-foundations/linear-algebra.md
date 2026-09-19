---
title: 1. Linear Algebra
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §4]] (matrix multiplication, transpose, inverse) · [[02-foundations/engineering-math|0.5 §10]] (Σ, argmax, norm notation) · [[02-foundations/neural-network-basics|0.7]] for the machine-learning words the examples use (layer, token, embedding)
> [[02-foundations/engineering-math|0.5 §4]](행렬곱·전치·역행렬) · [[02-foundations/engineering-math|0.5 §10]](Σ·argmax·노름 표기) · 예제에 쓰이는 기계학습 어휘(층·토큰·임베딩)는 [[02-foundations/neural-network-basics|0.7]]
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/engineering-math|0.5]] and [[02-foundations/neural-network-basics|0.7]]. First corner of the core triangle: a matrix is a map, with a rank,
eigenvalues and an SVD. Four later pages name this one as a prerequisite — calculus, probability, optimization and SE(3).*

Deep learning *is* linear algebra with nonlinearities between the matrix multiplies.
This page is a course-depth treatment: definitions, derivations, worked examples, and
where each concept appears in the papers of this wiki.

> [!note] First pass · 처음이라면
> Read §1 for what a matrix is, then the 2×2 worked example in §3, then §6 for the high-dimensional intuition papers assume. Come back for §4 (SVD) when a paper factorises something, §4.5 the first time you meet $J^\dagger$ on the robotics track, and §5 when you reach the control track.

### 1. Vectors, matrices, and what multiplication means

The first three bullets set up the vocabulary — what a matrix is and two ways to read $Wx$ — and the worked shape computation for an attention head follows right after.

- A matrix $W \in \mathbb{R}^{m\times n}$ is a **linear map** $\mathbb{R}^n \to \mathbb{R}^m$:
  it satisfies $W(ax + by) = aWx + bWy$, which is additivity and homogeneity at once (the
  complete definition, with non-examples, is [[02-foundations/engineering-math|0.5 §4.5]]).
  The converse also holds: every linear map $\mathbb{R}^n \to \mathbb{R}^m$ is a matrix, whose
  column $j$ is the image of the unit vector $e_j$, since any $x = \sum_j x_j e_j$ is then sent
  to $\sum_j x_j W e_j$. For $W = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $We_1 = (1,3)$ is the
  first column. Non-example: $x \mapsto Wx + b$ with $b \ne 0$ is affine, not linear, because it
  sends $0$ to $b$. Every linear layer (strictly, its $W$), attention projection
  ($W_Q, W_K, W_V$), and embedding lookup is one.
- Two readings of $y = Wx$:
  - **Row picture**: $y_i = \langle w_{i,:}, x\rangle$ — each output is a dot-product
    similarity between the input and a learned pattern (row).
  - **Column picture**: $y = \sum_j x_j\, w_{:,j}$ — the output is a mix of learned
    directions (columns) weighted by the input.
- Shape discipline: $(m\times n)(n\times 1) = (m \times 1)$. Reading shapes is how you read
  architectures. Worked example — one attention head with $d_{model}=512$, $d_k=64$, where $X$ is the
  input matrix of $T$ token embeddings (one 512-dim row per token in the sequence):
  $Q = XW_Q$ is $(T\times 512)(512\times 64) = T\times 64$; scores $QK^\top$ are $T\times T$;
  output $\text{softmax}(QK^\top/\sqrt{64})\,V$ is $T\times 64$ (softmax turns scores
  into probabilities — defined in [[02-foundations/engineering-math|0.5 §10]]). The whole
  [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] type-checks in one line.
- **Dot product and angle**: the dot (inner) product takes two vectors of the same length and
  returns one number,
  $$\langle a,b\rangle = a^\top b = \sum_{i=1}^{n} a_i b_i = \|a\|\,\|b\|\cos\theta$$
  where $\theta$ is the angle between them; the last equality is the law of cosines, so the
  product measures how much of one vector lies along the other. Example: $a = (1,2,2)$,
  $b = (2,0,1)$ give $\langle a,b\rangle = 2 + 0 + 2 = 4$, $\|a\| = 3$, $\|b\| = \sqrt5 = 2.236$,
  so $\cos\theta = 0.596$ and $\theta = 53.4°$. Two vectors are **orthogonal** when
  $\langle a,b\rangle = 0$, like $(1,0)$ and $(0,1)$. Cosine similarity
  $= \langle a,b\rangle / (\|a\|\|b\|)$ lies in $[-1, 1]$ ($1$ same direction, $0$ orthogonal,
  $-1$ opposite; $0.596$ here) and ignores lengths — the retrieval metric of
  [[01-canonical-papers/notes/3-vlm/clip|CLIP]].
- A **norm** $\|\cdot\|$ assigns a length to each vector. It is any function satisfying three
  axioms, for all vectors $x, y$ and scalars $c$ — positive definiteness, absolute homogeneity
  and the triangle inequality:
  $$\|x\| \ge 0 \text{ with } \|x\| = 0 \iff x = 0, \qquad \|c\,x\| = |c|\,\|x\|, \qquad \|x + y\| \le \|x\| + \|y\|$$
  so lengths behave the way distances must (no detour is shorter than the direct path).
  Norms: $\|x\|_2 = \sqrt{\sum x_i^2}$ (length, energy), $\|x\|_1 = \sum |x_i|$
  (sparsity-inducing — its "corners" touch axes first), $\|x\|_\infty = \max_i |x_i|$, and for
  matrices $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$. Example: $x = (3,-4)$ has $\|x\|_2 = 5$,
  $\|x\|_1 = 7$, $\|x\|_\infty = 4$; $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$ has
  $\|A\|_F = \sqrt{30} = 5.477$; and $u = (3,0)$, $v = (0,4)$ satisfy the triangle inequality as
  $\|u+v\|_2 = 5 \le 3 + 4$. Non-example: the so-called "$L_0$ norm", the count of nonzero
  entries, is not a norm, since doubling $x$ leaves the count unchanged instead of doubling it.

**Follow one input through the map.** Before calculating, say what each axis means. In a robot velocity map, the input entries may be joint speeds and the output entries tip-velocity components. In a neural layer, they are feature coordinates. The arithmetic is the same, but units and interpretation come from the application. A row asks which combination of inputs creates one output; a column asks what happens if only one input changes. Neither view requires imagining the whole matrix at once.

In the attention example above, select one row of the score matrix. That row contains one query's comparison with every key. Softmax normalizes across those keys, and multiplying by V combines their value vectors into one output row. Repeat for the other queries. This explains why the score matrix is token-by-token while the result is token-by-feature: the operation mixes information between tokens without turning the token index into a feature coordinate.

> [!question] Pause and explain · 잠깐 설명해 보기
> If you double one input coordinate while holding the others fixed, which column controls the change? The corresponding column of the matrix. It describes that input's contribution; the other columns' contributions remain unchanged. Use this test whenever a matrix looks like an opaque block of numbers.

### 2. Linear systems, rank, column space and null space

- $Ax = b$ solvable ⟺ $b \in \text{col}(A)$ — the **column space**, i.e. everything you can
  reach by scaling $A$'s columns and adding them up. ("Everything reachable from a set of
  vectors this way" is their **span**; the column space is the span of the columns.) As sets,
  $$\text{span}(v_1, \ldots, v_k) = \{c_1 v_1 + \cdots + c_k v_k : c_i \in \mathbb{R}\}, \qquad \text{col}(A) = \{Ax : x \in \mathbb{R}^n\}$$
  and the two descriptions of $\text{col}(A)$ agree because $Ax$ is exactly the combination of
  columns weighted by $x$ (§1's column picture). Example: $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$
  has $\text{col}(C)$ = the line through $(1,2)$, so $Cx = (1,2)$ is solvable and $Cx = (1,0)$
  is not.
- **Linear independence**: vectors $v_1, \ldots, v_k$ are linearly independent when the only
  combination that gives zero is the trivial one,
  $$c_1 v_1 + \cdots + c_k v_k = 0 \implies c_1 = \cdots = c_k = 0$$
  so no vector is a combination of the others and each one adds a new direction. Example:
  $(1,0,1)$ and $(0,1,1)$ are independent; adding $(1,1,2)$, their sum, makes the set dependent
  ($1\cdot v_1 + 1\cdot v_2 - 1\cdot v_3 = 0$), and the span stays a plane.
- Gaussian elimination = row
  operations to triangular form; LU factorization is elimination *recorded* so multiple
  right-hand sides are cheap. Written out, $A = LU$ with $L$ lower-triangular (ones on the
  diagonal, the elimination multipliers below) and $U$ upper-triangular (what elimination
  leaves), so $Ax = b$ becomes two triangular solves, $Ly = b$ then $Ux = y$. Example:
  $\begin{pmatrix}2&1\\4&3\end{pmatrix} = \begin{pmatrix}1&0\\2&1\end{pmatrix}\begin{pmatrix}2&1\\0&1\end{pmatrix}$
  (the multiplier is $4/2 = 2$); for $b = (3,7)$, $Ly = b$ gives $y = (3,1)$ and $Ux = y$ gives
  $x = (1,1)$.
- **Rank** = number of independent columns = number of independent rows = dimension of
  what the map can express, $\text{rank}(A) = \dim \text{col}(A)$, where the dimension counts
  the vectors in a largest independent set. The **null space**
  $\text{null}(A) = \{x : Ax = 0\}$ is every input the map sends to zero; it always contains
  $x = 0$, and is *nontrivial* when it contains more. The two are tied by rank–nullity, for
  $A$ with $n$ columns:
  $$\text{rank}(A) + \dim \text{null}(A) = n$$
  since every input direction is either expressed in the output or destroyed. Rank-deficient ⇒ information is destroyed
  (null space $\{x: Ax = 0\}$ is nontrivial). Example: $C$ above has rank $1$ and null space
  spanned by $(2,-1)$, dimension $1$, and $1 + 1 = 2$ ✓. The consequence for solving: if $x_0$
  solves $Ax = b$, then so does $x_0 + z$ for every $z$ in the null space, so the solution is
  unique exactly when the null space is trivial.
- **Least squares** — the most-used derivation in applied math. Overdetermined $Ax \approx b$:
  minimize $\|Ax - b\|^2$. Setting the gradient to zero:
  $$\nabla_x \|Ax-b\|^2 = 2A^\top(Ax - b) = 0 \;\Rightarrow\; A^\top A\, \hat{x} = A^\top b$$
  (the **normal equations**), unique when $A$'s columns are linearly independent — VMLS (Boyd & Vandenberghe's *Introduction to Applied Linear Algebra*, see Going deeper below) makes that
  assumption explicitly, and it is what makes $A^\top A$ invertible. Geometrically: $A\hat{x}$ is the orthogonal projection of $b$
  onto $\text{col}(A)$, and the residual is perpendicular to it. That projection is itself a
  matrix,
  $$P = A(A^\top A)^{-1}A^\top, \qquad P^2 = P, \qquad P^\top = P$$
  where $P^2 = P$ holds since projecting twice changes nothing and $P^\top = P$ since the discarded
  part is perpendicular; in the example below $Pb = (7/6,\ 8/3,\ 25/6)$. Linear regression,
  calibration, and the Kalman filter's update all live here.
  **Worked, three points and a line.** Fit $y = c + mx$ to $(1,1), (2,3), (3,4)$ — three
  equations, two unknowns, no exact solution. Stack them:
  $A = \begin{pmatrix}1&1\\1&2\\1&3\end{pmatrix}$, $b = (1,3,4)$. Then
  $A^\top A = \begin{pmatrix}3&6\\6&14\end{pmatrix}$ and $A^\top b = (8, 19)$, so
  $\hat x = (c, m) = (-\tfrac13, \tfrac32)$. The residual is
  $b - A\hat x = (-\tfrac16, \tfrac13, -\tfrac16)$ — and check the geometry claim directly:
  its sum is $0$ and its dot product with $(1,2,3)$ is $-\tfrac16 + \tfrac23 - \tfrac12 = 0$.
  The residual really is perpendicular to both columns of $A$, which is exactly what
  "orthogonal projection" asserts. That check costs ten seconds and catches most sign errors.
- Low-rank structure recurs everywhere: [[01-canonical-papers/notes/1-foundations/lora|LoRA]] assumes weight
<svg viewBox="0 0 560 242" style="max-width:100%;height:auto" role="img" aria-label="a vector b above the plane spanned by the columns of A, its projection inside the plane, and the residual meeting the plane at a right angle">
  <g fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.65">
    <polygon points="40,150 232,106 344,146 152,190"/>
  </g>
  <defs><marker id="laA" markerWidth="8" markerHeight="8" refX="7" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#laA)">
    <line x1="112" y1="164" x2="236" y2="58"/>
    <line x1="112" y1="164" x2="238" y2="140"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" stroke-dasharray="5 4" opacity="0.85">
    <line x1="244" y1="142" x2="244" y2="62"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <polyline points="232,142 232,130 244,130"/>
  </g>
  <g fill="currentColor"><circle cx="112" cy="164" r="3.5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="46" y="182" opacity="0.85">col(A) &#8212; everything A can reach</text>
    <text x="200" y="48">b (the data)</text>
    <text x="184" y="158">A x&#770; (the projection)</text>
    <text x="254" y="96">residual b &#8722; A x&#770;</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.8">
    <text x="254" y="110">&#8869; to the plane</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="388" y="40">the worked example</text>
    <text x="388" y="58">b = (1, 3, 4)</text>
    <text x="388" y="74">A x&#770; = (7/6, 8/3, 25/6)</text>
    <text x="388" y="90">residual = (&#8722;1/6, 1/3, &#8722;1/6)</text>
    <text x="400" y="108">&#183; (1,1,1) = 0</text>
    <text x="400" y="124">&#183; (1,2,3) = 0</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="204">The normal equations A&#7488;A x&#770; = A&#7488;b are this picture written as algebra: A&#7488;(b &#8722; A x&#770;) = 0 says</text>
    <text x="24" y="220">the residual is perpendicular to every column of A. That is also why least squares is least &#8212;</text>
    <text x="24" y="236">any other point of the plane is further from b, by Pythagoras on the right angle drawn here.</text>
  </g>
</svg>

  *updates* have low intrinsic rank ($\Delta W = BA$ with $r \ll d$).

**Separate three questions before reaching for an inverse.** Can the columns produce the requested b at all? If yes, is there only one input that does so? If not, what criterion chooses among approximations? These are existence, uniqueness, and selection. A rectangular matrix is not automatically a failed problem: it may describe more measurements than unknowns, or more available controls than the task needs.

For the line-fitting example, the first column says how changing the intercept moves every prediction together; the second says how changing the slope moves predictions in proportion to their x-coordinate. The observed data do not lie in the plane of predictions those columns can generate. Least squares chooses a point in that plane. At the optimum, the remaining residual is perpendicular to both available directions, so neither an intercept nudge nor a slope nudge can reduce squared error to first order.

**Check your understanding.** A zero residual means the chosen model fits these observations exactly. It does not mean the data are noiseless, the parameters are unique, or future predictions are correct. Conversely, a nonzero residual may simply reflect measurement noise in an overdetermined problem. This is why rank and residual answer different questions.

### 3. Eigendecomposition — directions a map only stretches

- An **eigenvector** of a square matrix $A$ is a *nonzero* vector $v$ that $A$ only scales,
  and the scale factor $\lambda$ is its **eigenvalue**:
  $$Av = \lambda v, \qquad v \ne 0$$
  so along eigenvector $v$, the map is pure scaling by $\lambda$ ($v = 0$ is excluded because
  $A0 = \lambda 0$ for every $\lambda$). The eigenvalues are the roots of
  $\det(A - \lambda I) = 0$, since $(A - \lambda I)v = 0$ has a nonzero solution only when
  $A - \lambda I$ is singular. Non-example: the $90°$ rotation
  $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ turns every nonzero vector, so it has no real
  eigenvector; its eigenvalues are $\pm j$.
- **Eigendecomposition**: when $A$ has $n$ independent eigenvectors, stack them as the columns
  of $V$ and the eigenvalues on the diagonal of $\Lambda$; then $A = V\Lambda V^{-1}$. Example:
  $\begin{pmatrix}1&1\\0&2\end{pmatrix}$ has $\lambda = 1, 2$ with eigenvectors $(1,0)$ and
  $(1,1)$. Not every matrix has one: the shear $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ has
  $\lambda = 1$ twice but only the single eigenvector direction $(1,0)$.
- **Spectral theorem.** For
  symmetric $A$ ($A^\top = A$): real eigenvalues, orthogonal eigenvectors, $A = Q\Lambda Q^\top$
  with $Q$ orthogonal ($Q^\top Q = I$, §4), so $Q^{-1} = Q^\top$.
- **Worked $2\times2$, start to finish.** Take $A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$.
  Eigenvalues solve $\det(A - \lambda I) = 0$:
  $$(2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0 \quad\Rightarrow\quad \lambda = 3,\ 1$$
  For $\lambda = 3$, solve $(A - 3I)v = 0$: the matrix
  $\begin{pmatrix}-1&1\\1&-1\end{pmatrix}$ says $v_1 = v_2$, so $v = (1,1)$.
  Check: $A(1,1) = (3,3) = 3(1,1)$ ✓. For $\lambda = 1$ the same steps give $v = (1,-1)$,
  and $A(1,-1) = (1,-1)$ ✓. The two eigenvectors came out perpendicular — that is the
  spectral theorem at work, not luck, and it happened because $A$ is symmetric. Normalized to
  length 1 they form $Q = \tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$, and
  $Q\,\text{diag}(3,1)\,Q^\top$ multiplies back to $A$ ✓.
  *Reading it aloud:* this matrix stretches everything along the $45°$ diagonal by $3\times$
  and leaves the anti-diagonal untouched. Every symmetric matrix is a version of that sentence.
- Why you care, concretely:
  - **Powers**: $A^k = Q\Lambda^k Q^\top$ — long-run behavior is governed by the largest
    $|\lambda|$. Stability of $x_{t+1} = Ax_t$ ⟺ all $|\lambda_i| < 1$
    (continuous time $\dot x = Ax$: all $\text{Re}(\lambda_i) < 0$).
  - **Optimization landscapes**: for quadratic loss $\frac12 x^\top H x$ ($H$ = the **Hessian**,
    the matrix of second derivatives — defined properly in
    [[02-foundations/calculus-backprop|2. Calculus §1]]; here just "the curvature matrix"), gradient descent
    converges per-eigendirection at rate $(1 - \alpha\lambda_i)$; the usable step size is
    set by $\lambda_{max}$, the slowest progress by $\lambda_{min}$. The
    **condition number** $\kappa = \lambda_{max}/\lambda_{min}$ (for this SPD — symmetric positive-definite, defined below — Hessian; for a
    general matrix the 2-norm condition number is the singular-value ratio
    $\kappa_2 = \sigma_{max}/\sigma_{min}$, e.g. $\begin{pmatrix}1&2\\3&4\end{pmatrix}$ has
    $\sigma = 5.465,\ 0.366$ and $\kappa_2 = 14.93$; a singular matrix has $\kappa = \infty$) *is* the difficulty of the problem — and poor conditioning is one useful lens on why
    adaptive optimization ([[01-canonical-papers/notes/1-foundations/adam|Adam]]) and normalization
    ([[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]) help.

    **What $\kappa$ costs you, in numbers.** Let $H = \text{diag}(10, 1)$, so
    $\lambda_{max} = 10$, $\lambda_{min} = 1$, $\kappa = 10$. Gradient descent multiplies
    coordinate $i$ by $(1 - \alpha\lambda_i)$ each step. Stability needs
    $\alpha < 2/\lambda_{max} = 0.2$, so take $\alpha = 0.18$. The steep direction then
    shrinks by $|1 - 1.8| = 0.8$ per step — fine — but the flat direction shrinks by only
    $1 - 0.18 = 0.82$ per step. Starting from $x_0 = (1,1)$, after 20 steps you are at about
    $(0.012,\ 0.019)$: the flat coordinate is what holds you back, and always will. Raise
    $\kappa$ to 1000 and the flat direction needs roughly 100× more steps. *That* is why
    people say "the problem is ill-conditioned" rather than "the learning rate is wrong" —
    no single $\alpha$ can serve both directions, which is exactly the gap per-coordinate
    methods try to close.
<svg viewBox="0 0 560 260" style="max-width:100%;height:auto" role="img" aria-label="gradient descent bouncing across a narrow valley while creeping along its floor">
  <g stroke="currentColor" stroke-width="1" opacity="0.3" fill="none">
    <line x1="40" y1="128" x2="240" y2="128"/><line x1="138" y1="24" x2="138" y2="196"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <ellipse cx="138" cy="128" rx="19.0" ry="60.1"/>
    <ellipse cx="138" cy="128" rx="11.4" ry="36.1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" opacity="0.9">
    <polyline points="223.0,43.0 70.0,58.3 192.4,70.8 94.5,81.1 172.8,89.6 110.1,96.5 160.3,102.2 120.2,106.8 152.3,110.6"/>
  </g>
  <g fill="currentColor" opacity="0.9"><circle cx="223.0" cy="43.0" r="2.6"/><circle cx="70.0" cy="58.3" r="2.6"/><circle cx="192.4" cy="70.8" r="2.6"/><circle cx="94.5" cy="81.1" r="2.6"/><circle cx="172.8" cy="89.6" r="2.6"/><circle cx="110.1" cy="96.5" r="2.6"/><circle cx="160.3" cy="102.2" r="2.6"/><circle cx="120.2" cy="106.8" r="2.6"/><circle cx="152.3" cy="110.6" r="2.6"/></g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="230" y="36">x&#8320; = (1, 1)</text>
    <text x="256" y="120">steep direction x&#8321;</text>
    <text x="256" y="134">&#215;0.8 per step, sign flipping</text>
    <text x="256" y="158">flat direction x&#8322;</text>
    <text x="256" y="172">&#215;0.82 per step</text>
    <text x="256" y="190">after 20 steps: (0.012, 0.019)</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="206">H = diag(10, 1) and &#945; = 0.18, just under the stability limit. The steep coordinate shrinks slightly</text>
    <text x="24" y="222">faster but flips sign each step, so the iterates bounce across the valley; the flat coordinate is</text>
    <text x="24" y="238">the one still holding you back at step 20. Raise &#954; to 1000 and the flat direction needs roughly</text>
    <text x="24" y="254">100&#215; more steps &#8212; no single &#945; serves both, which is what &#8220;ill-conditioned&#8221; names.</text>
  </g>
</svg>

- **Positive (semi-)definite**: symmetric $A$ with all $\lambda_i > 0$ ($\ge 0$);
  equivalently $x^\top A x > 0$ for all $x \ne 0$. Covariance matrices, Hessians at minima,
  and Gram/kernel matrices are PSD — "PSD" in a paper means "behaves like a squared quantity."
- **Reading $x^\top A x$ — it really is $ax^2$ with more indices.** The transposes are
  bookkeeping, not content. $x$ is a column ($n\times1$), so $x^\top$ is $1\times n$, and
  $(1\times n)(n\times n)(n\times 1) = 1\times 1$: you need an $x$ on *each* side or the
  answer would not be a number. Expand the product and every term is a coefficient times two coordinates:
  $$x^\top A x = \sum_i\sum_j A_{ij}\,x_i x_j$$
  — which is exactly what "quadratic" means. In one dimension it collapses to $a x^2$, as you would hope.
  - *Diagonal $A$ = independent parabolas.* $A = \begin{pmatrix}2&0\\0&3\end{pmatrix}$ gives
    $x^\top A x = 2x_1^2 + 3x_2^2$ — a bowl, steeper along $x_2$.
  - *Off-diagonal entries are the cross-terms that tilt it.*
    $A = \begin{pmatrix}1&1\\1&1\end{pmatrix}$ gives
    $x_1^2 + 2x_1x_2 + x_2^2 = (x_1+x_2)^2$ — still never negative, but flat along the whole
    line $x_1 = -x_2$, where it is exactly zero. That is *semi*-definite: a valley with a
    flat floor rather than a single lowest point.
  - *Not PSD looks like this.* $A = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$ gives
    $x_1^2 - x_2^2$, which is $+1$ at $x=(1,0)$ and $-1$ at $x=(0,1)$ — up one way, down the
    other. A saddle, not a bowl.
- **Why the two definitions are the same statement.** Substitute $A = Q\Lambda Q^\top$ and
  let $y = Q^\top x$ (just $x$ read in the eigenvector coordinate system):
  $$x^\top A x = x^\top Q\Lambda Q^\top x = y^\top \Lambda y = \sum_i \lambda_i\, y_i^2$$
  A weighted sum of squares, with the eigenvalues as the weights. Squares are never negative,
  so the whole thing is $\ge 0$ for every $x$ **exactly when** every $\lambda_i \ge 0$. The
  eigenvalue test and the $x^\top A x$ test are one fact seen twice.
- **Where you will actually meet it.** Two places, and both make the abstraction concrete:
  - *Taylor's second-order term* ([[02-foundations/engineering-math|0.5 §2]]) is
    $\tfrac12\,\delta^\top H \delta$ — the curvature you feel when stepping $\delta$ away
    from a point. At a stationary point, $H \succ 0$ is sufficient for a strict local
    minimum; $H \succeq 0$ is necessary but not sufficient. For example,
    $f(x,y)=x^4-y^4$ has zero gradient and the zero (hence PSD) Hessian at the origin, but
    the origin is a saddle. See [[02-foundations/optimization|4. Optimization §3]].
  - *Variance of any linear readout*: for a random vector $x$ with covariance $\Sigma$,
    $\text{Var}(w^\top x) = w^\top \Sigma w$. A variance cannot be negative — and that,
    with no further argument, is **why every covariance matrix is PSD**. When a paper says
    "$\Sigma \succeq 0$", it is asserting nothing more exotic than that.

<svg viewBox="0 0 470 214" style="max-width:100%;height:auto" role="img" aria-label="three quadratic forms: a bowl, a flat-floored valley, and a saddle">
  <g stroke="currentColor" stroke-width="1" opacity="0.3">
    <line x1="15" y1="118" x2="125" y2="118"/><line x1="180" y1="118" x2="290" y2="118"/><line x1="345" y1="118" x2="455" y2="118"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.9"><path d="M15.0 72.0L16.8 75.0L18.7 77.9L20.5 80.7L22.3 83.4L24.2 86.1L26.0 88.6L27.8 91.0L29.7 93.3L31.5 95.5L33.3 97.6L35.2 99.5L37.0 101.4L38.8 103.2L40.7 104.9L42.5 106.5L44.3 108.0L46.2 109.4L48.0 110.6L49.8 111.8L51.7 112.9L53.5 113.9L55.3 114.7L57.2 115.5L59.0 116.2L60.8 116.7L62.7 117.2L64.5 117.5L66.3 117.8L68.2 117.9L70.0 118.0L71.8 117.9L73.7 117.8L75.5 117.5L77.3 117.2L79.2 116.7L81.0 116.2L82.8 115.5L84.7 114.7L86.5 113.9L88.3 112.9L90.2 111.8L92.0 110.6L93.8 109.4L95.7 108.0L97.5 106.5L99.3 104.9L101.2 103.2L103.0 101.4L104.8 99.5L106.7 97.6L108.5 95.5L110.3 93.3L112.2 91.0L114.0 88.6L115.8 86.1L117.7 83.4L119.5 80.7L121.3 77.9L123.2 75.0L125.0 72.0"/><path d="M180.0 87.3L181.8 89.3L183.7 91.3L185.5 93.2L187.3 95.0L189.2 96.7L191.0 98.4L192.8 100.0L194.7 101.5L196.5 103.0L198.3 104.4L200.2 105.7L202.0 107.0L203.8 108.2L205.7 109.3L207.5 110.3L209.3 111.3L211.2 112.2L213.0 113.1L214.8 113.9L216.7 114.6L218.5 115.2L220.3 115.8L222.2 116.3L224.0 116.8L225.8 117.1L227.7 117.5L229.5 117.7L231.3 117.9L233.2 118.0L235.0 118.0L236.8 118.0L238.7 117.9L240.5 117.7L242.3 117.5L244.2 117.1L246.0 116.8L247.8 116.3L249.7 115.8L251.5 115.2L253.3 114.6L255.2 113.9L257.0 113.1L258.8 112.2L260.7 111.3L262.5 110.3L264.3 109.3L266.2 108.2L268.0 107.0L269.8 105.7L271.7 104.4L273.5 103.0L275.3 101.5L277.2 100.0L279.0 98.4L280.8 96.7L282.7 95.0L284.5 93.2L286.3 91.3L288.2 89.3L290.0 87.3"/><path d="M345.0 87.3L346.8 89.3L348.7 91.3L350.5 93.2L352.3 95.0L354.2 96.7L356.0 98.4L357.8 100.0L359.7 101.5L361.5 103.0L363.3 104.4L365.2 105.7L367.0 107.0L368.8 108.2L370.7 109.3L372.5 110.3L374.3 111.3L376.2 112.2L378.0 113.1L379.8 113.9L381.7 114.6L383.5 115.2L385.3 115.8L387.2 116.3L389.0 116.8L390.8 117.1L392.7 117.5L394.5 117.7L396.3 117.9L398.2 118.0L400.0 118.0L401.8 118.0L403.7 117.9L405.5 117.7L407.3 117.5L409.2 117.1L411.0 116.8L412.8 116.3L414.7 115.8L416.5 115.2L418.3 114.6L420.2 113.9L422.0 113.1L423.8 112.2L425.7 111.3L427.5 110.3L429.3 109.3L431.2 108.2L433.0 107.0L434.8 105.7L436.7 104.4L438.5 103.0L440.3 101.5L442.2 100.0L444.0 98.4L445.8 96.7L447.7 95.0L449.5 93.2L451.3 91.3L453.2 89.3L455.0 87.3"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.9" opacity="0.55" stroke-dasharray="5 3"><path d="M15.0 87.3L16.8 89.3L18.7 91.3L20.5 93.2L22.3 95.0L24.2 96.7L26.0 98.4L27.8 100.0L29.7 101.5L31.5 103.0L33.3 104.4L35.2 105.7L37.0 107.0L38.8 108.2L40.7 109.3L42.5 110.3L44.3 111.3L46.2 112.2L48.0 113.1L49.8 113.9L51.7 114.6L53.5 115.2L55.3 115.8L57.2 116.3L59.0 116.8L60.8 117.1L62.7 117.5L64.5 117.7L66.3 117.9L68.2 118.0L70.0 118.0L71.8 118.0L73.7 117.9L75.5 117.7L77.3 117.5L79.2 117.1L81.0 116.8L82.8 116.3L84.7 115.8L86.5 115.2L88.3 114.6L90.2 113.9L92.0 113.1L93.8 112.2L95.7 111.3L97.5 110.3L99.3 109.3L101.2 108.2L103.0 107.0L104.8 105.7L106.7 104.4L108.5 103.0L110.3 101.5L112.2 100.0L114.0 98.4L115.8 96.7L117.7 95.0L119.5 93.2L121.3 91.3L123.2 89.3L125.0 87.3"/><path d="M180.0 118.0L181.8 118.0L183.7 118.0L185.5 118.0L187.3 118.0L189.2 118.0L191.0 118.0L192.8 118.0L194.7 118.0L196.5 118.0L198.3 118.0L200.2 118.0L202.0 118.0L203.8 118.0L205.7 118.0L207.5 118.0L209.3 118.0L211.2 118.0L213.0 118.0L214.8 118.0L216.7 118.0L218.5 118.0L220.3 118.0L222.2 118.0L224.0 118.0L225.8 118.0L227.7 118.0L229.5 118.0L231.3 118.0L233.2 118.0L235.0 118.0L236.8 118.0L238.7 118.0L240.5 118.0L242.3 118.0L244.2 118.0L246.0 118.0L247.8 118.0L249.7 118.0L251.5 118.0L253.3 118.0L255.2 118.0L257.0 118.0L258.8 118.0L260.7 118.0L262.5 118.0L264.3 118.0L266.2 118.0L268.0 118.0L269.8 118.0L271.7 118.0L273.5 118.0L275.3 118.0L277.2 118.0L279.0 118.0L280.8 118.0L282.7 118.0L284.5 118.0L286.3 118.0L288.2 118.0L290.0 118.0"/><path d="M345.0 148.7L346.8 146.7L348.7 144.7L350.5 142.8L352.3 141.0L354.2 139.3L356.0 137.6L357.8 136.0L359.7 134.5L361.5 133.0L363.3 131.6L365.2 130.3L367.0 129.0L368.8 127.8L370.7 126.7L372.5 125.7L374.3 124.7L376.2 123.8L378.0 122.9L379.8 122.1L381.7 121.4L383.5 120.8L385.3 120.2L387.2 119.7L389.0 119.2L390.8 118.9L392.7 118.5L394.5 118.3L396.3 118.1L398.2 118.0L400.0 118.0L401.8 118.0L403.7 118.1L405.5 118.3L407.3 118.5L409.2 118.9L411.0 119.2L412.8 119.7L414.7 120.2L416.5 120.8L418.3 121.4L420.2 122.1L422.0 122.9L423.8 123.8L425.7 124.7L427.5 125.7L429.3 126.7L431.2 127.8L433.0 129.0L434.8 130.3L436.7 131.6L438.5 133.0L440.3 134.5L442.2 136.0L444.0 137.6L445.8 139.3L447.7 141.0L449.5 142.8L451.3 144.7L453.2 146.7L455.0 148.7"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="70" y="22">positive definite</text><text x="235" y="22">positive semidefinite</text><text x="400" y="22">indefinite</text>
    <text x="70" y="40" font-size="10" opacity="0.8">2x&#8321;&#178; + 3x&#8322;&#178;</text><text x="235" y="40" font-size="10" opacity="0.8">(x&#8321; + x&#8322;)&#178;</text><text x="400" y="40" font-size="10" opacity="0.8">x&#8321;&#178; &#8722; x&#8322;&#178;</text>
    <text x="70" y="176">up in every direction</text><text x="235" y="176">up, but flat along a line</text><text x="400" y="176">one way up, one way down</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="15" y="196" opacity="0.85">Each panel plots x&#7488;Ax along two directions through the origin (solid and dashed).</text>
    <text x="15" y="209" opacity="0.85">Positive semidefinite means no direction ever dips below the axis.</text>
  </g>
</svg>



### 4. SVD — a universal factorization, available for every matrix

- **Every** matrix (any shape, any rank): $A = U\Sigma V^\top$ with **orthogonal** $U, V$ (columns unit-length and mutually
  perpendicular, so multiplying by one is a pure rotation/reflection — it stretches nothing) and
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$. Reading: rotate (input
  basis $V$) → scale (singular values) → rotate (output basis $U$).
- **The pieces, named.** For $A \in \mathbb{R}^{m\times n}$, $U$ is $m\times m$, $\Sigma$ is
  $m\times n$ with zeros off the diagonal, and $V$ is $n\times n$. A square matrix $Q$ is
  **orthogonal** when $Q^\top Q = I$, which is why it preserves lengths:
  $\|Qx\|^2 = x^\top Q^\top Q x = \|x\|^2$. A $30°$ rotation keeps $\|(3,4)\| = 5$; the
  non-example $\text{diag}(2,1)$ has $\text{diag}(2,1)^\top\text{diag}(2,1) = \text{diag}(4,1) \ne I$
  and stretches. Read column by column, the SVD says
  $$A v_i = \sigma_i u_i, \qquad A^\top u_i = \sigma_i v_i$$
  where the columns $v_i$ of $V$ are the **right singular vectors**, the columns $u_i$ of $U$
  the **left singular vectors**, and $\sigma_i \ge 0$ the **singular values**, so input direction
  $v_i$ goes to output direction $u_i$, stretched by $\sigma_i$.

<svg viewBox="0 0 520 150" style="max-width:100%;height:auto" role="img" aria-label="SVD as rotate, scale, rotate">
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <circle cx="60" cy="75" r="38"/>
    <circle cx="205" cy="75" r="38"/>
    <ellipse cx="350" cy="75" rx="42" ry="17"/>
    <ellipse cx="475" cy="75" rx="17" ry="42" transform="rotate(-30 475 75)"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.6">
    <line x1="60" y1="75" x2="98" y2="75"/><line x1="60" y1="75" x2="60" y2="37"/>
    <line x1="205" y1="75" x2="232" y2="48"/><line x1="205" y1="75" x2="178" y2="48"/>
    <line x1="350" y1="75" x2="392" y2="75"/><line x1="350" y1="75" x2="350" y2="58"/>
  </g>
  <defs><marker id="svdArrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.4" marker-end="url(#svdArrow)" opacity="0.8">
    <line x1="108" y1="75" x2="152" y2="75"/><line x1="253" y1="75" x2="297" y2="75"/><line x1="400" y1="75" x2="428" y2="75"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="60" y="138">unit ball</text>
    <text x="130" y="66">Vᵀ</text><text x="275" y="66">Σ</text><text x="414" y="66">U</text>
    <text x="205" y="138">rotate</text><text x="350" y="138">scale σ₁, σ₂</text><text x="475" y="138">rotate</text>
  </g>
</svg>

*Every matrix does exactly this to a sphere: rotate, stretch along axes, rotate again. The $\sigma_i$ are the stretch factors, and a zero $\sigma_i$ is a direction the map destroys.*

- **Worked, on the singular matrix from [[02-foundations/engineering-math|0.5 §4]].** $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$.
  Compute $C^\top C = \begin{pmatrix}5&10\\10&20\end{pmatrix}$, whose eigenvalues solve
  $\lambda^2 - 25\lambda = 0$, giving $\lambda = 25, 0$. So $\sigma_1 = \sqrt{25} = 5$ and
  $\sigma_2 = 0$. Read that off: **one** nonzero singular value means rank 1, so $C$ collapses
  the plane onto a line, and $\|C\|_2 = \sigma_1 = 5$ is the most it can stretch anything. The
  direction it destroys is the right singular vector belonging to $\sigma_2 = 0$, here
  $(2,-1)/\sqrt5$ — check: $C(2,-1) = (0,0)$ ✓. That is §2's null space, found by a different
  route.
- Connections: $\sigma_i^2$ = eigenvalues of $A^\top A$; rank = number of nonzero $\sigma_i$;
  $\|A\|_2 = \sigma_1$. That last one is the definition of the **spectral norm** (the matrix
  2-norm) as the largest stretch,
  $$\|A\|_2 = \max_{x \ne 0} \frac{\|Ax\|_2}{\|x\|_2} = \sigma_1$$
  since the best input is $v_1$. For $C$ above, the input $(1,2)$ becomes $(5,10)$, stretched by
  exactly $5$.
- **Eckart–Young**: the best rank-$k$ approximation (in $\|\cdot\|_F$ or $\|\cdot\|_2$) is
  truncated SVD $A_k = \sum_{i\le k}\sigma_i u_i v_i^\top$, and its error is exactly what was
  thrown away,
  $$\|A - A_k\|_2 = \sigma_{k+1}, \qquad \|A - A_k\|_F = \sqrt{\textstyle\sum_{i>k}\sigma_i^2}$$
  so no rank-$k$ matrix can do better. Example: $A = \text{diag}(3,2,1)$ with $k = 1$ keeps
  $\text{diag}(3,0,0)$, with error $2$ in the 2-norm and $\sqrt5 = 2.236$ in Frobenius. This is the mathematical license for
  model compression and PCA. ([[01-canonical-papers/notes/1-foundations/lora|LoRA]] is related but
  different: it does not SVD-approximate a finished update — it *parameterizes* the update
  as low-rank from the start, an empirical design choice.)
- **PCA in four lines**: center data $X$; covariance $C = \frac1n X^\top X$; its top
  eigenvectors = directions of maximal variance = right singular vectors of $X$; project.
  A classical ancestor of learned representations. PCA (principal component analysis) is thus
  a linear dimensionality reduction. With $X$ holding $n$ centered samples as rows, the variance
  along a unit direction $w$ is $w^\top C w$, so the directions of maximal variance are the
  eigenvectors of $C$:
  $$C\,w_i = \lambda_i\,w_i, \qquad z = W_k^\top x$$
  where $w_i$ is the $i$-th principal direction, $\lambda_i$ the variance of the data along it,
  $W_k$ the matrix of the top $k$ directions and $z$ the $k$ new coordinates of a sample $x$; the
  share of variance kept is $\sum_{i \le k}\lambda_i / \sum_i \lambda_i$. Example: the points
  $(2,0), (0,1), (-2,0), (0,-1)$ already have mean zero, $C = \text{diag}(2,\ 0.5)$, the first
  component is $(1,0)$ with $2/2.5 = 80\%$ of the variance, and the one-number codes are
  $2, 0, -2, 0$.

**Read the multiplication from right to left.** Vᵀ first expresses an input in special input directions. Σ stretches or suppresses each of those coordinates. U then expresses the result in the output frame. The input and output spaces can have different dimensions, which is why SVD applies even when an eigenvector interpretation of A itself is unavailable.

Return to the singular example above. Its zero singular value means a component along the destroyed direction leaves no trace in the output. No inverse can recover information that never appears there. A very small nonzero singular value creates a related problem: recovering that input component requires dividing by a small number, amplifying measurement error as well as signal. This is the reason to care about conditioning before solving an inverse problem.

**Check your understanding.** When truncated SVD discards a weak direction, it accepts reconstruction error in exchange for a simpler or more stable representation. It does not prove that the discarded direction is unimportant for your task. A low-variance feature can still carry the distinction a classifier or robot needs; the matrix approximation objective and the downstream objective must be kept separate.

### 4.5 The pseudo-inverse — what $J^\dagger$ means

The symbol $A^\dagger$ appears all over the robotics track — $J^\dagger$ for inverse
kinematics, $J^\dagger$ again in operational-space control — and it is the object that
connects the SVD above to every solver in this wiki. It exists because most matrices you
meet are not square, so $A^{-1}$ is not available.

**When is there anything to invert?** $A^\top A$ is invertible exactly when $A$'s columns
are linearly independent. One line shows it: if $A^\top A x = 0$ then
$x^\top A^\top A x = \lVert Ax \rVert^2 = 0$, so $Ax = 0$, so $x = 0$ by independence.

**Two formulas, and which one you get depends on the shape.**

| Shape | Pseudo-inverse | It is a | What it computes |
|---|---|---|---|
| Tall, independent columns ($m > n$) | $A^\dagger = (A^\top A)^{-1}A^\top$ | left inverse, $A^\dagger A = I$ | the least-squares solution of an *overdetermined* system |
| Wide, independent rows ($m < n$) | $A^\dagger = A^\top (AA^\top)^{-1}$ | right inverse, $AA^\dagger = I$ | the *minimum-norm* solution of an *underdetermined* system |
| Square and invertible | both | the inverse | $A^{-1}$ — the two formulas collapse to it |

Those two rows are two different robotics situations. Tall is more measurements than
unknowns: calibration, bundle adjustment, fitting a plane to a point cloud. Wide is more
joints than task dimensions: a redundant arm, where infinitely many joint velocities produce
the tool motion you asked for and you need a rule to pick one.

**Worked — the minimum-norm rule, on a redundant arm.** Take a 3-link planar arm with unit
links at $\theta = (0°, 90°, 0°)$. Its Jacobian mapping joint rates to tool velocity comes from the column rule (MR ch.5) — each column is the tip velocity produced by unit rate at that joint alone — and it is
$2 \times 3$ — wide, hence redundant:

$$J = \begin{bmatrix} -2 & -2 & -1 \\ 1 & 0 & 0 \end{bmatrix}, \qquad JJ^\top = \begin{bmatrix} 9 & -2 \\ -2 & 1 \end{bmatrix}, \qquad \det JJ^\top = 5$$

The minimum-norm rule follows from minimising $\lVert\dot\theta\rVert$ subject to $J\dot\theta = v$, and the answer is the right pseudoinverse:

$$J^\dagger = J^\top (JJ^\top)^{-1} = \begin{bmatrix} 0 & 1 \\ -0.4 & -0.8 \\ -0.2 & -0.4 \end{bmatrix}$$

Ask the tool to move straight up at 1 m/s, $v = (0, 1)$. Then
$\dot\theta = J^\dagger v = (1,\, -0.8,\, -0.4)$, with $\lVert\dot\theta\rVert = 1.342$.

Now find the redundancy. $J$'s null space is spanned by $n = (0,\, 0.447,\, -0.894)$ — check
$Jn = 0$. So $\dot\theta + \alpha n$ produces **exactly the same tool velocity** for any
$\alpha$, and its norm is $\sqrt{1.8 + \alpha^2}$: at $\alpha = 1$ it is 1.673, at
$\alpha = -1$ also 1.673. Every alternative is longer. That is the whole content of
"pseudo-inverse": among the infinitely many joint motions that do the job, it returns the
shortest one, and the null space is the freedom left over — which
[[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] spends on joint limits and
obstacle avoidance.

**Worked: plant P2, the square case the problem set uses.** Catalog pose $\theta=(0^\circ,90^\circ)$ ([[02-foundations/lab-plants|0.6]]):

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}.$$

Draw the columns at the tip $(1,1)$: column 1 is the tip velocity for $\dot\theta=(1,0)$, which is $(-1,1)$; column 2 is $(-1,0)$. The $2\times 2$ inverse formula with $\det J=1$ gives $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. Square and invertible, so the table's last row says $J^\dagger=J^{-1}$. Check: $J J^{-1}=I$. The problem set asks you to write those two matrices and to say they match — you have just done it. The 3-link arm above needed a pseudoinverse because it was wide; P2 does not. What P2 *does* need the SVD story for is the next sentence: send $\theta_2\to 0$ and the two columns become parallel, $\det J\to 0$, $\kappa_2(J)\to\infty$, and a sideways tip motion is lost. $J^\dagger$ then explodes in the lost direction exactly as $\Sigma^\dagger$ below predicts.

**The SVD view, and why $J^\dagger$ explodes.** Writing $A = U\Sigma V^\top$ from §4, the
pseudo-inverse is

$$A^\dagger = V\Sigma^\dagger U^\top, \qquad \Sigma^\dagger = \operatorname{diag}(1/\sigma_1,\, \ldots,\, 1/\sigma_r,\, 0,\, \ldots)$$

— invert the nonzero singular values, leave the zeros alone. This is the definition that
works for *every* matrix, including rank-deficient ones, and the two formulas above are
special cases of it. It also explains the failure mode: near a singular configuration one
$\sigma_i \to 0$, so $1/\sigma_i \to \infty$ and the returned joint velocity grows without bound in
that one direction as the arm approaches the singularity. The arm is being asked to move in a direction it cannot move; at the singular pose itself the pseudo-inverse leaves that zero alone, so the answer jumps discontinuously when the rank actually drops.

**The definition behind both formulas.** The (Moore–Penrose) pseudo-inverse of any
$m\times n$ matrix $A$ is the unique $n\times m$ matrix $A^\dagger$ satisfying four conditions:

$$AA^\dagger A = A, \qquad A^\dagger A A^\dagger = A^\dagger, \qquad (AA^\dagger)^\top = AA^\dagger, \qquad (A^\dagger A)^\top = A^\dagger A$$

The first two say $A^\dagger$ undoes $A$ wherever undoing is possible, and the last two say the
products $AA^\dagger$ and $A^\dagger A$ are orthogonal projections, so what cannot be undone is
discarded perpendicularly rather than arbitrarily. The SVD formula satisfies all four, which is
why it is the general definition. The $J^\dagger$ above passes all four numerically (to about
$10^{-16}$), and $J^\dagger J$ is not $I$ but the projection with rows $(1,0,0)$,
$(0, 0.8, 0.4)$, $(0, 0.4, 0.2)$: it removes exactly the null-space direction $n$, because the
arm is redundant.

The fix is to stop inverting the small singular values exactly — replace $1/\sigma$ with
$\sigma/(\sigma^2 + \lambda)$, which is bounded for every $\sigma$ and equals $1/\sigma$
when $\sigma^2 \gg \lambda$. That is **damped least squares**: instead of the exact
minimum-norm solution, it minimizes $\lVert J\dot\theta - v\rVert^2 + \lambda\lVert\dot\theta\rVert^2$,
a trade between tracking error and joint speed, whose solution is

$$J^\dagger_\lambda = J^\top (JJ^\top + \lambda I)^{-1}$$

where $\lambda > 0$ is the damping; adding $\lambda I$ keeps the matrix invertible even at a
singularity, so the inverse can never blow up. In numbers: with $\lambda = 0.01$, a healthy
$\sigma = 1$ is inverted to $0.990$ instead of $1$, but a near-singular $\sigma = 0.01$ gives
$0.990$ instead of $100$. On the arm above, the same $\lambda$ turns the command $v = (0,1)$ into
$\dot\theta = (0.982,\ -0.784,\ -0.392)$ instead of $(1,\ -0.8,\ -0.4)$ — slightly less
tracking, bounded speeds. It is the same $\lambda$
as the trust parameter you will meet on [[02-foundations/optimization|4. Optimization §3.5]] —
a forward pointer, not something this page depends on. So the chain
runs: singular values → pseudo-inverse → what happens when one of them vanishes → damping →
Levenberg–Marquardt. Four names, one idea.

### 5. The control-theory connection

Linear algebra *is* the language of control ([[04-robotics/index|control track]]):

- **State-space model** $\dot{x} = Ax + Bu$, $y = Cx$: the system is a matrix; simulating
  is repeated matrix multiplication; the matrix exponential $e^{At}$ solves the unforced system exactly, and with the convolution $x(t) = e^{At}x_0 + \int_0^t e^{A(t-s)}Bu(s)\,ds$ the forced one.
  The symbols: $x \in \mathbb{R}^n$ is the **state** (the numbers that, with future inputs,
  determine the future), $u \in \mathbb{R}^m$ the input, $y \in \mathbb{R}^p$ the measured
  output, and $A$ ($n\times n$), $B$ ($n\times m$), $C$ ($p\times n$) the internal dynamics, how
  the input enters, and what the sensor sees (full treatment in
  [[04-robotics/control-theory-ce397|5. Control Theory §2]]). The **matrix exponential** is
  defined by the same power series as $e^{at}$,
  $$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + \cdots$$
  so that $\frac{d}{dt}e^{At} = Ae^{At}$ and $x(t) = e^{At}x_0$ solves $\dot x = Ax$. Example: a
  unit mass pushed by a force $u$, with state (position, velocity), has
  $A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$ and $B = (0, 1)$. Here $A^2 = 0$, so the series
  stops: $e^{At} = \begin{pmatrix}1&t\\0&1\end{pmatrix}$, and starting at position $0$ with
  velocity $1$, after $t = 2$ the state is $(2, 1)$.
- **Stability = eigenvalues of $A$** (poles): continuous-time stable iff all
  $\text{Re}(\lambda_i) < 0$; discrete-time iff all $|\lambda_i| < 1$.
- **Controllability**: which directions can the input actually push the state? One step
  of input moves you along the columns of $B$; the dynamics then rotate that reach into
  $AB$, then $A^2B$, and so on. Stack those reachable directions —
  $[B, AB, \ldots, A^{n-1}B]$ — and if together they span all $n$ dimensions
  ($\text{rank} = n$), *every* state is reachable; if they miss a direction, no input
  sequence ever drives the state there. As a test,
  $$\mathcal{C} = [\,B \;\; AB \;\; \cdots \;\; A^{n-1}B\,], \qquad \text{controllable} \iff \text{rank}\,\mathcal{C} = n$$
  where $\mathcal{C}$ is the $n \times nm$ controllability matrix; the stack stops at
  $A^{n-1}B$ because later powers add no new direction (the Cayley–Hamilton argument in
  [[04-robotics/control-theory-ce397|5. Control Theory §6]]). Example: the pushed mass above has
  $AB = (1, 0)$, so $\mathcal{C} = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ with rank 2 — a force
  alone steers both position and velocity. Non-example: $A = \text{diag}(1, 2)$ with
  $B = (1, 0)$ gives $\mathcal{C} = \begin{pmatrix}1&1\\0&0\end{pmatrix}$, rank 1, so the second,
  unstable mode can never be influenced.
<svg viewBox="0 0 470 160" style="max-width:100%;height:auto" role="img" aria-label="controllable versus uncontrollable reachable directions">
  <g fill="currentColor" opacity="0.10"><polygon points="30,120 30,55 105,55 105,120"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35">
    <line x1="30" y1="120" x2="190" y2="120"/><line x1="30" y1="120" x2="30" y2="20"/>
    <line x1="280" y1="120" x2="440" y2="120"/><line x1="280" y1="120" x2="280" y2="20"/>
  </g>
  <defs><marker id="cArrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="2" marker-end="url(#cArrow)">
    <line x1="30" y1="120" x2="30" y2="58"/>
    <line x1="30" y1="120" x2="102" y2="58"/>
    <line x1="280" y1="120" x2="362" y2="120"/>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="36" y="52">B</text><text x="108" y="52">AB</text>
    <text x="368" y="116">B</text><text x="330" y="140">AB is on the same line</text>
    <text x="14" y="156" font-size="12">rank 2 → every state reachable</text>
    <text x="264" y="156" font-size="12">rank 1 → one direction unreachable</text>
  </g>
</svg>

*Left: $B$ and $AB$ point in different directions, so together they span the plane. Right: the dynamics only ever rotate $B$ back onto itself — a whole direction of the state space is out of reach, whatever you do with $u$.*

  Observability is the transpose twin — can the
  output $y$ eventually reveal every state? — with matrix $[C^\top, A^\top C^\top, \ldots]$.
  Stacked the usual way,
  $$\mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix}, \qquad \text{observable} \iff \text{rank}\,\mathcal{O} = n$$
  which is the transpose of that matrix and has the same rank, because $y, \dot y, \ddot y, \ldots$
  equal $Cx, CAx, CA^2x, \ldots$ when $u = 0$, and $x$ can be solved for exactly when this stack
  has full rank. Example: measuring the pushed mass's position, $C = (1, 0)$, gives
  $\mathcal{O} = I$, rank 2, observable. Non-example: measuring only its velocity, $C = (0, 1)$,
  gives rows $(0,1)$ and $(0,0)$, rank 1 — no amount of speed data reveals where the mass
  started.
- LQR gains ([[04-robotics/lqr-lqg|6. LQR/LQG]]), Kalman filters ([[02-foundations/probability|3. Probability §5]]), and MPC ([[04-robotics/mpc|7. MPC]]) all reduce to structured matrix computations — Riccati recursions (one linear solve per step) for LQR and Kalman, and a dense QP (quadratic program: a quadratic cost under linear constraints) after MPC condensing (eliminating the states so only the inputs remain as variables, [[04-robotics/mpc|7. MPC §2]]) — numerical linear algebra is the control engineer's daily tool.

### 6. Geometry of high dimensions (paper-reading intuition)

- Random zero-mean (isotropic) high-dim vectors are nearly orthogonal: $\cos\theta$ concentrates around 0 with spread $\approx 1/\sqrt d$ (its mean is already 0 in any dimension; vectors with a non-zero mean do not become orthogonal) — one reason
  dot-product retrieval over millions of embeddings is *possible*: unrelated items score
  near zero. (That relevant pairs score high is a property of the *learned* embedding, not
  of geometry.)
- Distances concentrate: nearest and farthest neighbors differ by little — one reason *learned* embeddings and metrics replace raw distances on raw features. (Cosine similarity does not escape concentration: for unit vectors $\|a-b\|^2 = 2 - 2\cos\theta$, so it ranks neighbours exactly as Euclidean distance does; what it adds is ignoring vector norms.)
- Manifold hypothesis: real data occupies a low-dimensional surface inside pixel space —
  the implicit justification for latent spaces ([[01-canonical-papers/notes/6-diffusion/vae|VAE]],
  [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]]).

> [!tip] Going deeper · 더 깊이
> This page is a working set, not a course. If it moves too fast, Boyd and Vandenberghe's free [*Introduction to Applied Linear Algebra*](https://web.stanford.edu/~boyd/vmls/) covers §1 and the least-squares half of §2 at a gentler pace — it builds everything from linear independence and QR, and never uses the words rank, column space or null space, and Strang's *Introduction to Linear Algebra* is the standard first course for the eigenvalue and SVD half. Come back here for where each idea shows up in the papers.

### Self-check

1. Why do two stacked linear layers (no nonlinearity) collapse to one? What rank can the
   composition have?
2. Derive the normal equations and explain why the residual is orthogonal to $\text{col}(A)$.
3. A discrete system $x_{t+1} = Ax_t$ has eigenvalues $0.9, 1.02$. What happens, and along
   which direction?
4. Why does [[01-canonical-papers/notes/1-foundations/lora|LoRA]] initialize $B = 0$? (What map does
   $W_0 + BA$ equal at step 0?)

> [!tip]- Answers
> 1. $W_2(W_1x) = (W_2W_1)x$ — the product *is* a single linear map, so the composition collapses. Its rank is at most $\min(\text{rank}\,W_1, \text{rank}\,W_2)$: stacking cannot create expressive power that neither factor had.
> 2. Setting $\nabla\|Ax-b\|^2 = 2A^\top(Ax-b) = 0$ gives $A^\top A\hat x = A^\top b$. The residual $r = b - A\hat x$ then satisfies $A^\top r = 0$, i.e. $r$ is orthogonal to every column of $A$ — which is exactly the statement that $A\hat x$ is the orthogonal projection of $b$ onto $\text{col}(A)$.
> 3. The component along the $0.9$ eigenvector decays; the component along the $1.02$ eigenvector grows 2% per step. The state therefore diverges, asymptotically aligned with the $1.02$ eigenvector — a single unstable mode dominates the long run no matter how small it starts.
> 4. With $B = 0$ the update is $\Delta W = BA = 0$, so $W_0 + BA = W_0$ at step 0: training starts *exactly* at the pretrained model (a no-op initialization) instead of perturbing it randomly.

### Problem set · 과제

Tier B. **P2** from [[02-foundations/lab-plants|0.6]] at $\theta=(0^\circ,90^\circ)$. This page §4.5. No time-stepper.

1. **Draw.** Arm in the plane: base at the origin, elbow $(1,0)$, tip $(1,1)$. Draw $J$'s two columns as arrows at the tip (tip velocity for each unit joint rate).
2. **Derive.** From $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$, compute $J^{-1}$ by the $2\times 2$ formula. Then $J^\dagger$ from the square-invertible row of the §4.5 table. Confirm they match.
3. **Interpret.** Send $\theta_2\to 0$ with $\theta_1$ fixed. What happens to the two column arrows, to $\det J$, and to $\kappa_2(J)$? What tool motion becomes impossible?

> [!tip]- Solutions
> 1. Column 1 is $(-1,1)$ (whole arm about the base). Column 2 is $(-1,0)$ (forearm about the elbow).
> 2. $\det J=1$, so $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. Square and invertible $\Rightarrow J^\dagger=J^{-1}$.
> 3. The columns become parallel (both along $\pm y$ at $\theta=(0^\circ,0^\circ)$), $\det J\to 0$, $\kappa_2\to\infty$. Sideways ($x$) tip motion is lost: a stretched arm cannot do it at finite joint speed.

## 한국어

*[[02-foundations/engineering-math|0.5]]와 [[02-foundations/neural-network-basics|0.7]] 위에 선다. 핵심 삼각형의 첫 꼭짓점이다: 행렬은 랭크와 고윳값과 SVD를 가진
사상이다. 뒤의 네 페이지 — 미적분, 확률, 최적화, SE(3) — 가 이 페이지를 선수로 지목한다.*

딥러닝은 행렬곱 사이에 비선형성을 끼운 선형대수 *그 자체*다. 이 페이지는 교재 수준의
서술이다: 정의, 유도, 계산 예시, 그리고 각 개념이 이 위키의 논문들 어디에서 나타나는지.

> [!note] 처음이라면 · First pass
> 먼저 §1로 행렬이 무엇인지, 그다음 §3의 2×2 계산 예제, 그다음 §6의 고차원 직관. §4(SVD)는 논문이 무언가를 분해할 때, §4.5는 로보틱스 트랙에서 $J^\dagger$를 처음 만날 때, §5는 제어 트랙에 닿았을 때 돌아오라.

### 1. 벡터, 행렬, 그리고 곱셈의 의미

처음 세 항목은 어휘를 세운다 — 행렬이 무엇인지, $Wx$를 읽는 두 방법 — 그리고 바로 뒤에 어텐션 헤드의 모양을 따지는 계산 예시가 이어진다.

- 행렬 $W \in \mathbb{R}^{m\times n}$은 **선형 사상** $\mathbb{R}^n \to \mathbb{R}^m$이다:
  $W(ax + by) = aWx + bWy$를 만족한다. 가법성과 동차성을 한꺼번에 쓴 것이다(비예시까지 담은
  완전한 정의는 [[02-foundations/engineering-math|0.5 §4.5]]). 역도 성립한다. $\mathbb{R}^n \to \mathbb{R}^m$인
  모든 선형 사상은 행렬이고, 그 $j$번째 열은 단위벡터 $e_j$의 상이다. 임의의 $x = \sum_j x_j e_j$가
  $\sum_j x_j W e_j$로 가기 때문이다. $W = \begin{pmatrix}1&2\\3&4\end{pmatrix}$라면
  $We_1 = (1,3)$이 첫 열이다. 비예시: $b \ne 0$인 $x \mapsto Wx + b$는 $0$을 $b$로 보내므로
  선형이 아니라 아핀이다. 모든 선형층(엄밀히는 그 $W$), 어텐션 투영($W_Q, W_K, W_V$), 임베딩
  조회가 이것이다.
- $y = Wx$의 두 가지 독해:
  - **행 관점**: $y_i = \langle w_{i,:}, x\rangle$ — 각 출력은 입력과 학습된 패턴(행)
    사이의 내적 유사도다.
  - **열 관점**: $y = \sum_j x_j\, w_{:,j}$ — 출력은 학습된 방향들(열)을 입력이 가중한
    혼합이다.
- 모양의 규율: $(m\times n)(n\times 1) = (m \times 1)$. 모양 읽기가 구조 읽기다.
  계산 예시 — $d_{model}=512$, $d_k=64$인 어텐션 헤드 하나, $X$는 시퀀스의 토큰 $T$개를
  512차원 행으로 쌓은 입력 행렬:
  $Q = XW_Q$는 $(T\times 512)(512\times 64) = T\times 64$; 점수 $QK^\top$는 $T\times T$;
  출력 $\text{softmax}(QK^\top/\sqrt{64})\,V$는 $T\times 64$ (softmax는 점수를 확률로
  바꾼다 — [[02-foundations/engineering-math|0.5 §10]]에 정의).
  [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] 전체가 한 줄로 타입
  검사된다.
- **내적과 각도**: 내적은 길이가 같은 두 벡터를 받아 숫자 하나를 돌려준다.
  $$\langle a,b\rangle = a^\top b = \sum_{i=1}^{n} a_i b_i = \|a\|\,\|b\|\cos\theta$$
  $\theta$는 두 벡터 사이의 각이다. 마지막 등식은 코사인 법칙이고, 그래서 내적은 한 벡터가 다른
  벡터 방향으로 얼마나 누워 있는지를 잰다. 예: $a = (1,2,2)$, $b = (2,0,1)$이면
  $\langle a,b\rangle = 2 + 0 + 2 = 4$, $\|a\| = 3$, $\|b\| = \sqrt5 = 2.236$이므로
  $\cos\theta = 0.596$, $\theta = 53.4°$다. $\langle a,b\rangle = 0$이면 두 벡터가 **직교**한다.
  $(1,0)$과 $(0,1)$이 그렇다. 코사인 유사도 $= \langle a,b\rangle / (\|a\|\|b\|)$는 $[-1, 1]$에
  있고($1$은 같은 방향, $0$은 직교, $-1$은 반대 방향, 여기서는 $0.596$) 길이를 무시한다 —
  [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 검색 지표.
- **노름** $\|\cdot\|$은 각 벡터에 길이를 준다. 모든 벡터 $x, y$와 스칼라 $c$에 대해 세 공리
  — 양의 정부호성, 절대 동차성, 삼각 부등식 — 를 만족하는 함수면 무엇이든 노름이다.
  $$\|x\| \ge 0 \text{ with } \|x\| = 0 \iff x = 0, \qquad \|c\,x\| = |c|\,\|x\|, \qquad \|x + y\| \le \|x\| + \|y\|$$
  그래서 길이가 거리처럼 행동한다(돌아가는 길이 곧은 길보다 짧을 수 없다).
  노름: $\|x\|_2 = \sqrt{\sum x_i^2}$(길이, 에너지), $\|x\|_1 = \sum |x_i|$(희소성 유도 —
  "모서리"가 축에 먼저 닿는다), $\|x\|_\infty = \max_i |x_i|$, 행렬에는
  $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$. 예: $x = (3,-4)$는 $\|x\|_2 = 5$, $\|x\|_1 = 7$,
  $\|x\|_\infty = 4$이고, $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$는
  $\|A\|_F = \sqrt{30} = 5.477$이며, $u = (3,0)$, $v = (0,4)$는 $\|u+v\|_2 = 5 \le 3 + 4$로
  삼각 부등식을 만족한다. 비예시: 0이 아닌 성분의 개수인 이른바 "$L_0$ 노름"은 노름이 아니다.
  $x$를 두 배로 해도 개수가 두 배가 되지 않고 그대로이기 때문이다.

**입력 하나를 사상 끝까지 따라간다.** 계산 전에 각 축의 뜻을 말해 본다. 로봇 속도 사상에서는 입력이 관절 속도이고 출력이 말단 속도 성분일 수 있다. 신경망 층에서는 특징 좌표다. 계산은 같지만 단위와 해석은 응용이 정한다. 행은 한 출력을 만드는 입력 조합을 묻는다. 열은 입력 하나만 바뀌면 무슨 일이 생기는지 묻는다. 행렬 전체를 한꺼번에 상상할 필요가 없다.

위 어텐션 예제에서는 점수 행렬의 행 하나를 고른다. 한 쿼리를 모든 키와 비교한 값이다. Softmax는 그 키들에 걸쳐 정규화하고, V를 곱하면 키에 대응하는 값 벡터를 섞어 출력 행 하나를 만든다. 나머지 쿼리에서도 반복한다. 그래서 점수는 토큰×토큰이지만 결과는 토큰×특징이다. 토큰 사이의 정보를 섞지, 토큰 번호를 특징 좌표로 바꾸는 것이 아니다.

> [!question] 잠깐 설명해 보기 · Pause and explain
> 다른 입력을 고정하고 입력 좌표 하나를 두 배로 만들면 어느 열이 변화를 결정하는가? 그 좌표에 대응하는 열이다. 그 입력의 기여가 바뀌고 다른 열의 기여는 그대로다. 행렬이 불투명한 숫자 덩어리처럼 보이면 이 질문부터 한다.

### 2. 선형계, 랭크, 열공간과 영공간

- $Ax = b$가 풀린다 ⟺ $b \in \text{col}(A)$ — **열공간(column space)**, 즉 $A$의 열들을
  스칼라배해 더해서 도달할 수 있는 점 전체다. ("어떤 벡터 집합에서 이렇게 도달할 수 있는
  것 전체"를 그 집합의 **span**(생성)이라 하고, 열공간은 열들의 span이다.) 집합으로 쓰면
  $$\text{span}(v_1, \ldots, v_k) = \{c_1 v_1 + \cdots + c_k v_k : c_i \in \mathbb{R}\}, \qquad \text{col}(A) = \{Ax : x \in \mathbb{R}^n\}$$
  이고, $Ax$가 정확히 $x$로 가중한 열들의 조합이므로(§1의 열 관점) $\text{col}(A)$의 두 설명이
  일치한다. 예: $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$의 $\text{col}(C)$는 $(1,2)$를 지나는
  직선이므로 $Cx = (1,2)$는 풀리고 $Cx = (1,0)$은 풀리지 않는다.
- **일차독립**: 영벡터를 만드는 조합이 자명한 것뿐이면 벡터 $v_1, \ldots, v_k$가 일차독립이다.
  $$c_1 v_1 + \cdots + c_k v_k = 0 \implies c_1 = \cdots = c_k = 0$$
  그래서 어떤 벡터도 나머지의 조합이 아니고, 하나하나가 새 방향을 더한다. 예: $(1,0,1)$과
  $(0,1,1)$은 독립이다. 둘의 합 $(1,1,2)$를 보태면 종속이 되고
  ($1\cdot v_1 + 1\cdot v_2 - 1\cdot v_3 = 0$), span은 여전히 평면이다.
- 가우스 소거 = 삼각형 꼴로 가는 행
  연산; LU 분해는 소거 과정을 *기록*해 우변이 여러 개일 때 재사용을 싸게 만든 것. 풀어 쓰면
  $A = LU$이고, $L$은 하삼각(대각선이 1, 그 아래가 소거 승수), $U$는 상삼각(소거가 남긴 것)이다.
  그래서 $Ax = b$가 삼각 풀이 두 번, $Ly = b$와 $Ux = y$가 된다. 예:
  $\begin{pmatrix}2&1\\4&3\end{pmatrix} = \begin{pmatrix}1&0\\2&1\end{pmatrix}\begin{pmatrix}2&1\\0&1\end{pmatrix}$
  (승수는 $4/2 = 2$)이고, $b = (3,7)$이면 $Ly = b$에서 $y = (3,1)$, $Ux = y$에서 $x = (1,1)$이다.
- **랭크** = 독립인 열의 수 = 독립인 행의 수 = 사상이 표현할 수 있는 것의 차원,
  $\text{rank}(A) = \dim \text{col}(A)$이다. 차원은 가장 큰 독립 집합의 벡터 수다. **영공간**
  $\text{null}(A) = \{x : Ax = 0\}$은 사상이 0으로 보내는 입력 전체다. 항상 $x = 0$을 포함하고,
  그보다 많이 포함하면 *자명하지 않다*고 한다. 열이 $n$개인 $A$에서 둘은 랭크–퇴화차수 정리로
  묶인다.
  $$\text{rank}(A) + \dim \text{null}(A) = n$$
  모든 입력 방향은 출력에 표현되거나 파괴되거나 둘 중 하나이기 때문이다.
  랭크 부족 ⇒ 정보가 파괴된다 (영공간 $\{x: Ax = 0\}$이 자명하지 않다). 예: 위의 $C$는 랭크
  $1$이고 영공간은 $(2,-1)$이 생성하는 1차원이며 $1 + 1 = 2$다 ✓. 풀이에 대한 결과: $x_0$가
  $Ax = b$의 해이면 영공간의 모든 $z$에 대해 $x_0 + z$도 해이므로, 해는 영공간이 자명할 때만
  유일하다.
- **최소제곱** — 응용수학에서 가장 많이 쓰는 유도. 과결정 $Ax \approx b$:
  $\|Ax - b\|^2$ 최소화. 그래디언트를 0으로 놓으면:
  $$\nabla_x \|Ax-b\|^2 = 2A^\top(Ax - b) = 0 \;\Rightarrow\; A^\top A\, \hat{x} = A^\top b$$
  (**정규방정식**). $A$의 열이 일차독립일 때 유일하다. VMLS(Boyd·Vandenberghe의 *Introduction to Applied Linear Algebra*, 아래 더 깊이 참고)가 그 가정을 명시하고, 그것이 $A^\top A$를 가역으로 만든다. 기하적으로: $A\hat{x}$는 $b$를 $\text{col}(A)$에 직교 투영한 것이고,
  잔차는 거기에 수직이다. 그 투영 자체가 행렬이다.
  $$P = A(A^\top A)^{-1}A^\top, \qquad P^2 = P, \qquad P^\top = P$$
  $P^2 = P$는 두 번 투영해도 달라지지 않는다는 뜻이고, $P^\top = P$는 버려지는 부분이 수직이라는
  뜻이다. 아래 예제에서 $Pb = (7/6,\ 8/3,\ 25/6)$이다.
  선형 회귀, 캘리브레이션, 칼만 필터의 갱신이 모두 여기 산다.
  **계산 예제 — 점 셋에 직선 하나.** $(1,1), (2,3), (3,4)$에 $y = c + mx$를 맞춰 보자 —
  식 셋, 미지수 둘, 정확한 해는 없다. 쌓으면
  $A = \begin{pmatrix}1&1\\1&2\\1&3\end{pmatrix}$, $b = (1,3,4)$. 그러면
  $A^\top A = \begin{pmatrix}3&6\\6&14\end{pmatrix}$, $A^\top b = (8, 19)$이므로
  $\hat x = (c, m) = (-\tfrac13, \tfrac32)$. 잔차는 $b - A\hat x = (-\tfrac16, \tfrac13, -\tfrac16)$이고,
  기하 주장을 직접 검산해 보라: 합이 $0$이고 $(1,2,3)$과의 내적이
  $-\tfrac16 + \tfrac23 - \tfrac12 = 0$이다. 잔차가 정말로 $A$의 두 열 모두에 수직이고,
  그것이 "직교 투영"이 주장하는 바로 그것이다. 이 검산은 10초면 되고 부호 실수의 대부분을
  잡아낸다.
<svg viewBox="0 0 560 242" style="max-width:100%;height:auto" role="img" aria-label="A의 열들이 만드는 평면 위로 벡터 b가 떠 있고 그 투영이 평면 안에 있으며 잔차가 평면과 직각으로 만난다">
  <g fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.65">
    <polygon points="40,150 232,106 344,146 152,190"/>
  </g>
  <defs><marker id="laA" markerWidth="8" markerHeight="8" refX="7" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#laA)">
    <line x1="112" y1="164" x2="236" y2="58"/>
    <line x1="112" y1="164" x2="238" y2="140"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" stroke-dasharray="5 4" opacity="0.85">
    <line x1="244" y1="142" x2="244" y2="62"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <polyline points="232,142 232,130 244,130"/>
  </g>
  <g fill="currentColor"><circle cx="112" cy="164" r="3.5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="46" y="182" opacity="0.85">col(A) &#8212; A가 도달할 수 있는 전부</text>
    <text x="200" y="48">b (데이터)</text>
    <text x="184" y="158">A x&#770; (투영)</text>
    <text x="254" y="96">잔차 b &#8722; A x&#770;</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.8">
    <text x="254" y="110">평면에 &#8869;</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="388" y="40">예제의 숫자</text>
    <text x="388" y="58">b = (1, 3, 4)</text>
    <text x="388" y="74">A x&#770; = (7/6, 8/3, 25/6)</text>
    <text x="388" y="90">잔차 = (&#8722;1/6, 1/3, &#8722;1/6)</text>
    <text x="400" y="108">&#183; (1,1,1) = 0</text>
    <text x="400" y="124">&#183; (1,2,3) = 0</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="204">정규방정식 A&#7488;A x&#770; = A&#7488;b는 이 그림을 대수로 쓴 것이다. A&#7488;(b &#8722; A x&#770;) = 0이 곧 잔차가 A의</text>
    <text x="24" y="220">모든 열에 수직이라는 뜻이다. 최소제곱이 최소인 이유도 이것이다 &#8212; 여기 그린 직각에 피타고라스를</text>
    <text x="24" y="236">적용하면 평면 위의 다른 어떤 점도 b에서 더 멀다는 것이 바로 나온다.</text>
  </g>
</svg>

- 저랭크 구조는 도처에서 반복된다: [[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 가중치
  *업데이트*의 내재 랭크가 낮다고 가정한다($r \ll d$인 $\Delta W = BA$).

**역행렬을 찾기 전에 세 질문을 나눈다.** 열들로 원하는 b를 만들 수 있는가? 만들 수 있다면 입력이 하나뿐인가? 만들 수 없다면 어떤 기준으로 근사를 고르는가? 존재성, 유일성, 선택의 문제다. 직사각 행렬이라고 문제가 실패한 것은 아니다. 미지수보다 측정이 많거나, 과제가 요구하는 것보다 제어 수단이 많을 수 있다.

직선 적합 예제의 첫 열은 절편을 바꾸면 모든 예측이 함께 움직인다는 뜻이다. 둘째 열은 기울기를 바꾸면 x좌표에 비례해 움직인다는 뜻이다. 관측 자료는 두 열이 만드는 예측의 평면 안에 없다. 최소자승은 그 평면 위의 점을 고른다. 최적점에서는 남은 잔차가 두 방향 모두에 수직이므로 절편이나 기울기를 조금 바꿔도 제곱 오차를 일차적으로 줄이지 못한다.

**이해 확인.** 잔차가 0이면 선택한 모델이 이 관측을 정확히 맞춘다는 뜻이다. 잡음이 없거나 파라미터가 유일하거나 미래 예측이 맞는다는 뜻은 아니다. 반대로 과결정 문제의 0이 아닌 잔차는 측정 잡음 때문일 수 있다. 랭크와 잔차가 다른 질문에 답하는 이유다.

### 3. 고유분해 — 사상이 늘이기만 하는 방향

- 정방 행렬 $A$의 **고유벡터**는 $A$가 늘이거나 줄이기만 하는 *영이 아닌* 벡터 $v$이고, 그
  배율 $\lambda$가 **고유값**이다.
  $$Av = \lambda v, \qquad v \ne 0$$
  그래서 고유벡터 $v$ 방향에서 사상은 $\lambda$배 순수 스케일링이다(모든 $\lambda$에 대해
  $A0 = \lambda 0$이므로 $v = 0$은 뺀다). $(A - \lambda I)v = 0$이 영이 아닌 해를 가지려면
  $A - \lambda I$가 특이해야 하므로, 고유값은 $\det(A - \lambda I) = 0$의 근이다. 비예시:
  $90°$ 회전 $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$은 영이 아닌 모든 벡터를 돌려 버리므로 실수
  고유벡터가 없고, 고유값은 $\pm j$다.
- **고유분해**: $A$가 독립인 고유벡터 $n$개를 가지면 그것들을 $V$의 열로, 고유값을 $\Lambda$의
  대각선에 놓아 $A = V\Lambda V^{-1}$로 쓴다. 예: $\begin{pmatrix}1&1\\0&2\end{pmatrix}$는
  고유값 $1, 2$와 고유벡터 $(1,0)$, $(1,1)$을 가진다. 모든 행렬이 되는 것은 아니다. 층밀림
  $\begin{pmatrix}1&1\\0&1\end{pmatrix}$은 고유값 $1$이 두 번이지만 고유벡터 방향은 $(1,0)$
  하나뿐이다.
- **스펙트럼 정리.** 대칭 $A$($A^\top = A$): 실수 고유값, 직교 고유벡터, $A = Q\Lambda Q^\top$.
  $Q$는 직교행렬($Q^\top Q = I$, §4)이므로 $Q^{-1} = Q^\top$이다.
- **$2\times2$ 계산 예제, 처음부터 끝까지.** $A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$를 보자.
  고유값은 $\det(A - \lambda I) = 0$을 푼다:
  $$(2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0 \quad\Rightarrow\quad \lambda = 3,\ 1$$
  $\lambda = 3$이면 $(A - 3I)v = 0$을 푼다: 행렬
  $\begin{pmatrix}-1&1\\1&-1\end{pmatrix}$이 $v_1 = v_2$를 말하므로 $v = (1,1)$.
  검산: $A(1,1) = (3,3) = 3(1,1)$ ✓. $\lambda = 1$도 같은 절차로 $v = (1,-1)$,
  $A(1,-1) = (1,-1)$ ✓. 두 고유벡터가 서로 수직으로 나온 것은 운이 아니라 스펙트럼 정리가
  작동한 것이고, $A$가 대칭이기 때문이다. 길이 1로 정규화하면
  $Q = \tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$이고, $Q\,\text{diag}(3,1)\,Q^\top$를
  곱하면 다시 $A$가 된다 ✓.
  *소리 내어 읽으면:* 이 행렬은 $45°$ 대각선 방향으로 모든 것을 $3$배 늘이고 반대 대각선은
  건드리지 않는다. 모든 대칭 행렬이 이 문장의 어떤 판본이다.
- 구체적으로 왜 중요한가:
  - **거듭제곱**: $A^k = Q\Lambda^k Q^\top$ — 장기 거동은 가장 큰 $|\lambda|$가 지배한다.
    $x_{t+1} = Ax_t$의 안정성 ⟺ 모든 $|\lambda_i| < 1$
    (연속 시간 $\dot x = Ax$: 모든 $\text{Re}(\lambda_i) < 0$).
  - **최적화 지형**: 이차 손실 $\frac12 x^\top H x$($H$ = **헤시안**, 2차 도함수의 행렬 —
    정식 정의는 [[02-foundations/calculus-backprop|2. 미적분 §1]]; 여기서는 "곡률 행렬"로
    읽으면 된다)에서 경사 하강은 고유방향별로
    $(1 - \alpha\lambda_i)$ 비율로 수렴한다; 쓸 수 있는 스텝 크기는 $\lambda_{max}$가,
    가장 느린 진전은 $\lambda_{min}$이 정한다. **조건수**
    $\kappa = \lambda_{max}/\lambda_{min}$(이 SPD — 대칭 양정부호, 아래에 정의 — 헤시안 기준; 일반 행렬의 2-노름 조건수는
    특이값 비 $\kappa_2 = \sigma_{max}/\sigma_{min}$. 예를 들어 $\begin{pmatrix}1&2\\3&4\end{pmatrix}$는
    $\sigma = 5.465,\ 0.366$이고 $\kappa_2 = 14.93$이며, 특이 행렬은 $\kappa = \infty$)가 문제의 난이도 *그 자체*다 —
    나쁜 조건수는 적응형 최적화([[01-canonical-papers/notes/1-foundations/adam|Adam]])와
    정규화([[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]])가 왜 돕는지 이해하는
    유용한 관점 중 하나다.

    **$\kappa$가 치르게 하는 대가, 숫자로.** $H = \text{diag}(10, 1)$이면 $\lambda_{max} = 10$,
    $\lambda_{min} = 1$, $\kappa = 10$이다. 경사 하강은 매 스텝 좌표 $i$에
    $(1 - \alpha\lambda_i)$를 곱한다. 안정하려면 $\alpha < 2/\lambda_{max} = 0.2$여야 하니
    $\alpha = 0.18$로 두자. 그러면 가파른 방향은 스텝당 $|1 - 1.8| = 0.8$배로 줄어 괜찮지만,
    평평한 방향은 스텝당 $1 - 0.18 = 0.82$배밖에 줄지 않는다. $x_0 = (1,1)$에서 시작하면 20
    스텝 뒤 대략 $(0.012,\ 0.019)$ — 발목을 잡는 것은 평평한 좌표이고 앞으로도 계속 그렇다.
    $\kappa$를 1000으로 올리면 평평한 방향에 약 100배의 스텝이 더 필요하다. "학습률이
    잘못됐다"가 아니라 *"문제의 조건이 나쁘다"*고 말하는 이유가 이것이다 — 어떤 단일 $\alpha$도
    두 방향을 동시에 만족시킬 수 없고, 좌표별 방법들이 메우려는 격차가 정확히 이것이다.
- **양(준)정부호**: 모든 $\lambda_i > 0$($\ge 0$)인 대칭 $A$; 동치로 모든 $x \ne 0$에서
<svg viewBox="0 0 560 260" style="max-width:100%;height:auto" role="img" aria-label="좁은 골짜기를 가로질러 튀면서 바닥을 따라 천천히 나아가는 경사 하강">
  <g stroke="currentColor" stroke-width="1" opacity="0.3" fill="none">
    <line x1="40" y1="128" x2="240" y2="128"/><line x1="138" y1="24" x2="138" y2="196"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <ellipse cx="138" cy="128" rx="19.0" ry="60.1"/>
    <ellipse cx="138" cy="128" rx="11.4" ry="36.1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" opacity="0.9">
    <polyline points="223.0,43.0 70.0,58.3 192.4,70.8 94.5,81.1 172.8,89.6 110.1,96.5 160.3,102.2 120.2,106.8 152.3,110.6"/>
  </g>
  <g fill="currentColor" opacity="0.9"><circle cx="223.0" cy="43.0" r="2.6"/><circle cx="70.0" cy="58.3" r="2.6"/><circle cx="192.4" cy="70.8" r="2.6"/><circle cx="94.5" cy="81.1" r="2.6"/><circle cx="172.8" cy="89.6" r="2.6"/><circle cx="110.1" cy="96.5" r="2.6"/><circle cx="160.3" cy="102.2" r="2.6"/><circle cx="120.2" cy="106.8" r="2.6"/><circle cx="152.3" cy="110.6" r="2.6"/></g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="230" y="36">x&#8320; = (1, 1)</text>
    <text x="256" y="120">가파른 방향 x&#8321;</text>
    <text x="256" y="134">스텝당 &#215;0.8, 부호가 뒤집힌다</text>
    <text x="256" y="158">평평한 방향 x&#8322;</text>
    <text x="256" y="172">스텝당 &#215;0.82</text>
    <text x="256" y="190">20 스텝 뒤: (0.012, 0.019)</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="206">H = diag(10, 1), &#945; = 0.18 &#8212; 안정 한계 바로 아래다. 가파른 좌표가 조금 더 빨리 줄지만 매 스텝</text>
    <text x="24" y="222">부호가 뒤집혀서 반복점이 골짜기를 가로질러 튄다. 20 스텝째에도 발목을 잡고 있는 것은 평평한</text>
    <text x="24" y="238">좌표다. &#954;를 1000으로 올리면 평평한 방향에 약 100배의 스텝이 더 필요하다 &#8212; 어떤 단일 &#945;도</text>
    <text x="24" y="254">둘을 함께 만족시키지 못한다는 것, 그것이 &#8220;조건이 나쁘다&#8221;는 말의 뜻이다.</text>
  </g>
</svg>

  $x^\top A x > 0$. 공분산 행렬, 최솟값에서의 헤시안, 그람/커널 행렬이 PSD다 —
  논문의 "PSD"는 "제곱량처럼 행동한다"는 뜻.
- **$x^\top A x$ 읽는 법 — 정말로 인덱스가 늘어난 $ax^2$이다.** 전치는 내용이 아니라 부기다.
  $x$가 열벡터($n\times1$)이므로 $x^\top$은 $1\times n$이고,
  $(1\times n)(n\times n)(n\times 1) = 1\times 1$ — 즉 답이 숫자가 되려면 $x$가 *양쪽에*
  하나씩 있어야 한다. 곱을 전개하면 모든 항이 계수 곱하기 좌표 둘이다:
  $$x^\top A x = \sum_i\sum_j A_{ij}\,x_i x_j$$
  — 그것이 정확히 "이차"의 뜻이다. 1차원으로 줄이면
  기대대로 $a x^2$가 된다.
  - *대각 $A$ = 서로 독립인 포물선들.* $A = \begin{pmatrix}2&0\\0&3\end{pmatrix}$이면
    $x^\top A x = 2x_1^2 + 3x_2^2$ — 그릇 모양이고 $x_2$ 방향이 더 가파르다.
  - *비대각 성분이 그릇을 기울이는 교차항이다.*
    $A = \begin{pmatrix}1&1\\1&1\end{pmatrix}$이면
    $x_1^2 + 2x_1x_2 + x_2^2 = (x_1+x_2)^2$ — 여전히 음수가 되지 않지만, 직선 $x_1 = -x_2$
    전체에서 정확히 0으로 평평하다. 이것이 *준*정부호다: 최저점 하나가 아니라 바닥이 평평한
    골짜기.
  - *PSD가 아닌 경우는 이렇게 생겼다.* $A = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$이면
    $x_1^2 - x_2^2$이고, $x=(1,0)$에서 $+1$, $x=(0,1)$에서 $-1$ — 한 방향은 올라가고 다른
    방향은 내려간다. 그릇이 아니라 안장이다.
- **두 정의가 왜 같은 말인가.** $A = Q\Lambda Q^\top$을 대입하고 $y = Q^\top x$로 두면
  (그저 $x$를 고유벡터 좌표계에서 읽은 것):
  $$x^\top A x = x^\top Q\Lambda Q^\top x = y^\top \Lambda y = \sum_i \lambda_i\, y_i^2$$
  고유값을 가중치로 쓴 제곱들의 가중합이다. 제곱은 결코 음수가 아니므로, 이 전체가 모든 $x$에
  대해 $\ge 0$일 **필요충분조건**이 모든 $\lambda_i \ge 0$이다. 고유값 판정과 $x^\top A x$
  판정은 하나의 사실을 두 번 본 것이다.
- **실제로 만나게 되는 자리.** 두 곳이고, 둘 다 이 추상을 구체로 만든다:
  - *테일러의 2차 항*([[02-foundations/engineering-math|0.5 §2]])이
    $\tfrac12\,\delta^\top H \delta$다 — 어떤 점에서 $\delta$만큼 움직일 때 느끼는 곡률.
    정상점에서 $H \succ 0$이면 엄격한 지역 최솟값이라는 충분조건이고, $H \succeq 0$은
    필요하지만 충분하지 않다. 예를 들어 $f(x,y)=x^4-y^4$는 원점에서 그래디언트와 헤시안이
    모두 0(따라서 PSD)이지만 원점은 안장점이다
    ([[02-foundations/optimization|4. 최적화 §3]]).
  - *임의의 선형 판독값의 분산*: 공분산이 $\Sigma$인 확률벡터 $x$에 대해
    $\text{Var}(w^\top x) = w^\top \Sigma w$. 분산은 음수가 될 수 없고 — 더 이상의 논증 없이
    이것이 **모든 공분산 행렬이 PSD인 이유**다. 논문의 "$\Sigma \succeq 0$"은 그 이상 별난
    것을 주장하지 않는다.

<svg viewBox="0 0 470 214" style="max-width:100%;height:auto" role="img" aria-label="세 가지 이차형식: 그릇, 바닥이 평평한 골짜기, 안장">
  <g stroke="currentColor" stroke-width="1" opacity="0.3">
    <line x1="15" y1="118" x2="125" y2="118"/><line x1="180" y1="118" x2="290" y2="118"/><line x1="345" y1="118" x2="455" y2="118"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.9"><path d="M15.0 72.0L16.8 75.0L18.7 77.9L20.5 80.7L22.3 83.4L24.2 86.1L26.0 88.6L27.8 91.0L29.7 93.3L31.5 95.5L33.3 97.6L35.2 99.5L37.0 101.4L38.8 103.2L40.7 104.9L42.5 106.5L44.3 108.0L46.2 109.4L48.0 110.6L49.8 111.8L51.7 112.9L53.5 113.9L55.3 114.7L57.2 115.5L59.0 116.2L60.8 116.7L62.7 117.2L64.5 117.5L66.3 117.8L68.2 117.9L70.0 118.0L71.8 117.9L73.7 117.8L75.5 117.5L77.3 117.2L79.2 116.7L81.0 116.2L82.8 115.5L84.7 114.7L86.5 113.9L88.3 112.9L90.2 111.8L92.0 110.6L93.8 109.4L95.7 108.0L97.5 106.5L99.3 104.9L101.2 103.2L103.0 101.4L104.8 99.5L106.7 97.6L108.5 95.5L110.3 93.3L112.2 91.0L114.0 88.6L115.8 86.1L117.7 83.4L119.5 80.7L121.3 77.9L123.2 75.0L125.0 72.0"/><path d="M180.0 87.3L181.8 89.3L183.7 91.3L185.5 93.2L187.3 95.0L189.2 96.7L191.0 98.4L192.8 100.0L194.7 101.5L196.5 103.0L198.3 104.4L200.2 105.7L202.0 107.0L203.8 108.2L205.7 109.3L207.5 110.3L209.3 111.3L211.2 112.2L213.0 113.1L214.8 113.9L216.7 114.6L218.5 115.2L220.3 115.8L222.2 116.3L224.0 116.8L225.8 117.1L227.7 117.5L229.5 117.7L231.3 117.9L233.2 118.0L235.0 118.0L236.8 118.0L238.7 117.9L240.5 117.7L242.3 117.5L244.2 117.1L246.0 116.8L247.8 116.3L249.7 115.8L251.5 115.2L253.3 114.6L255.2 113.9L257.0 113.1L258.8 112.2L260.7 111.3L262.5 110.3L264.3 109.3L266.2 108.2L268.0 107.0L269.8 105.7L271.7 104.4L273.5 103.0L275.3 101.5L277.2 100.0L279.0 98.4L280.8 96.7L282.7 95.0L284.5 93.2L286.3 91.3L288.2 89.3L290.0 87.3"/><path d="M345.0 87.3L346.8 89.3L348.7 91.3L350.5 93.2L352.3 95.0L354.2 96.7L356.0 98.4L357.8 100.0L359.7 101.5L361.5 103.0L363.3 104.4L365.2 105.7L367.0 107.0L368.8 108.2L370.7 109.3L372.5 110.3L374.3 111.3L376.2 112.2L378.0 113.1L379.8 113.9L381.7 114.6L383.5 115.2L385.3 115.8L387.2 116.3L389.0 116.8L390.8 117.1L392.7 117.5L394.5 117.7L396.3 117.9L398.2 118.0L400.0 118.0L401.8 118.0L403.7 117.9L405.5 117.7L407.3 117.5L409.2 117.1L411.0 116.8L412.8 116.3L414.7 115.8L416.5 115.2L418.3 114.6L420.2 113.9L422.0 113.1L423.8 112.2L425.7 111.3L427.5 110.3L429.3 109.3L431.2 108.2L433.0 107.0L434.8 105.7L436.7 104.4L438.5 103.0L440.3 101.5L442.2 100.0L444.0 98.4L445.8 96.7L447.7 95.0L449.5 93.2L451.3 91.3L453.2 89.3L455.0 87.3"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.9" opacity="0.55" stroke-dasharray="5 3"><path d="M15.0 87.3L16.8 89.3L18.7 91.3L20.5 93.2L22.3 95.0L24.2 96.7L26.0 98.4L27.8 100.0L29.7 101.5L31.5 103.0L33.3 104.4L35.2 105.7L37.0 107.0L38.8 108.2L40.7 109.3L42.5 110.3L44.3 111.3L46.2 112.2L48.0 113.1L49.8 113.9L51.7 114.6L53.5 115.2L55.3 115.8L57.2 116.3L59.0 116.8L60.8 117.1L62.7 117.5L64.5 117.7L66.3 117.9L68.2 118.0L70.0 118.0L71.8 118.0L73.7 117.9L75.5 117.7L77.3 117.5L79.2 117.1L81.0 116.8L82.8 116.3L84.7 115.8L86.5 115.2L88.3 114.6L90.2 113.9L92.0 113.1L93.8 112.2L95.7 111.3L97.5 110.3L99.3 109.3L101.2 108.2L103.0 107.0L104.8 105.7L106.7 104.4L108.5 103.0L110.3 101.5L112.2 100.0L114.0 98.4L115.8 96.7L117.7 95.0L119.5 93.2L121.3 91.3L123.2 89.3L125.0 87.3"/><path d="M180.0 118.0L181.8 118.0L183.7 118.0L185.5 118.0L187.3 118.0L189.2 118.0L191.0 118.0L192.8 118.0L194.7 118.0L196.5 118.0L198.3 118.0L200.2 118.0L202.0 118.0L203.8 118.0L205.7 118.0L207.5 118.0L209.3 118.0L211.2 118.0L213.0 118.0L214.8 118.0L216.7 118.0L218.5 118.0L220.3 118.0L222.2 118.0L224.0 118.0L225.8 118.0L227.7 118.0L229.5 118.0L231.3 118.0L233.2 118.0L235.0 118.0L236.8 118.0L238.7 118.0L240.5 118.0L242.3 118.0L244.2 118.0L246.0 118.0L247.8 118.0L249.7 118.0L251.5 118.0L253.3 118.0L255.2 118.0L257.0 118.0L258.8 118.0L260.7 118.0L262.5 118.0L264.3 118.0L266.2 118.0L268.0 118.0L269.8 118.0L271.7 118.0L273.5 118.0L275.3 118.0L277.2 118.0L279.0 118.0L280.8 118.0L282.7 118.0L284.5 118.0L286.3 118.0L288.2 118.0L290.0 118.0"/><path d="M345.0 148.7L346.8 146.7L348.7 144.7L350.5 142.8L352.3 141.0L354.2 139.3L356.0 137.6L357.8 136.0L359.7 134.5L361.5 133.0L363.3 131.6L365.2 130.3L367.0 129.0L368.8 127.8L370.7 126.7L372.5 125.7L374.3 124.7L376.2 123.8L378.0 122.9L379.8 122.1L381.7 121.4L383.5 120.8L385.3 120.2L387.2 119.7L389.0 119.2L390.8 118.9L392.7 118.5L394.5 118.3L396.3 118.1L398.2 118.0L400.0 118.0L401.8 118.0L403.7 118.1L405.5 118.3L407.3 118.5L409.2 118.9L411.0 119.2L412.8 119.7L414.7 120.2L416.5 120.8L418.3 121.4L420.2 122.1L422.0 122.9L423.8 123.8L425.7 124.7L427.5 125.7L429.3 126.7L431.2 127.8L433.0 129.0L434.8 130.3L436.7 131.6L438.5 133.0L440.3 134.5L442.2 136.0L444.0 137.6L445.8 139.3L447.7 141.0L449.5 142.8L451.3 144.7L453.2 146.7L455.0 148.7"/></g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="70" y="22">양정부호</text><text x="235" y="22">양준정부호</text><text x="400" y="22">부정부호</text>
    <text x="70" y="40" font-size="10" opacity="0.8">2x&#8321;&#178; + 3x&#8322;&#178;</text><text x="235" y="40" font-size="10" opacity="0.8">(x&#8321; + x&#8322;)&#178;</text><text x="400" y="40" font-size="10" opacity="0.8">x&#8321;&#178; &#8722; x&#8322;&#178;</text>
    <text x="70" y="176">모든 방향에서 위로</text><text x="235" y="176">위로, 다만 한 직선에서 평평</text><text x="400" y="176">한쪽은 위, 다른 쪽은 아래</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="15" y="196" opacity="0.85">각 패널은 원점을 지나는 두 방향(실선·점선)을 따라 x&#7488;Ax 값을 그린 것이다.</text>
    <text x="15" y="209" opacity="0.85">양준정부호란 어느 방향으로도 축 아래로 내려가지 않는다는 뜻이다.</text>
  </g>
</svg>



### 4. SVD — 모든 행렬에 존재하는 보편적 분해

- **모든** 행렬(모양·랭크 불문): $A = U\Sigma V^\top$, $U, V$는 **직교행렬**(열들이 길이 1이고 서로 수직 — 그래서 곱하는
  것은 순수한 회전/반사이고 아무것도 늘이지 않는다),
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$.
  독해: 회전(입력 기저 $V$) → 스케일(특이값) → 회전(출력 기저 $U$).
- **조각들의 이름.** $A \in \mathbb{R}^{m\times n}$이면 $U$는 $m\times m$, $\Sigma$는 대각선
  밖이 0인 $m\times n$, $V$는 $n\times n$이다. 정방 행렬 $Q$가 $Q^\top Q = I$를 만족하면
  **직교행렬**이고, 그래서 길이를 보존한다: $\|Qx\|^2 = x^\top Q^\top Q x = \|x\|^2$. $30°$ 회전은
  $\|(3,4)\| = 5$를 그대로 두고, 비예시 $\text{diag}(2,1)$은
  $\text{diag}(2,1)^\top\text{diag}(2,1) = \text{diag}(4,1) \ne I$라서 늘인다. 열 하나씩 읽으면
  SVD는 이렇게 말한다.
  $$A v_i = \sigma_i u_i, \qquad A^\top u_i = \sigma_i v_i$$
  $V$의 열 $v_i$가 **오른쪽 특이벡터**, $U$의 열 $u_i$가 **왼쪽 특이벡터**, $\sigma_i \ge 0$이
  **특이값**이다. 입력 방향 $v_i$가 $\sigma_i$배 늘어나 출력 방향 $u_i$로 간다.

<svg viewBox="0 0 520 150" style="max-width:100%;height:auto" role="img" aria-label="SVD = 회전 → 스케일 → 회전">
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <circle cx="60" cy="75" r="38"/>
    <circle cx="205" cy="75" r="38"/>
    <ellipse cx="350" cy="75" rx="42" ry="17"/>
    <ellipse cx="475" cy="75" rx="17" ry="42" transform="rotate(-30 475 75)"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.6">
    <line x1="60" y1="75" x2="98" y2="75"/><line x1="60" y1="75" x2="60" y2="37"/>
    <line x1="205" y1="75" x2="232" y2="48"/><line x1="205" y1="75" x2="178" y2="48"/>
    <line x1="350" y1="75" x2="392" y2="75"/><line x1="350" y1="75" x2="350" y2="58"/>
  </g>
  <defs><marker id="svdArrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.4" marker-end="url(#svdArrow)" opacity="0.8">
    <line x1="108" y1="75" x2="152" y2="75"/><line x1="253" y1="75" x2="297" y2="75"/><line x1="400" y1="75" x2="428" y2="75"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="60" y="138">단위 원</text>
    <text x="130" y="66">Vᵀ</text><text x="275" y="66">Σ</text><text x="414" y="66">U</text>
    <text x="205" y="138">회전</text><text x="350" y="138">σ₁, σ₂ 배로 늘리기</text><text x="475" y="138">회전</text>
  </g>
</svg>

*모든 행렬이 구에 하는 일이 정확히 이것이다: 회전 → 축 방향으로 늘이기 → 다시 회전. $\sigma_i$가 늘이는 배율이고, $\sigma_i = 0$인 방향은 사상이 파괴하는 방향이다.*

- **[[02-foundations/engineering-math|0.5 §4]]의 특이 행렬로 계산해 보면.** $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$.
  $C^\top C = \begin{pmatrix}5&10\\10&20\end{pmatrix}$이고 그 고유값은
  $\lambda^2 - 25\lambda = 0$에서 $\lambda = 25, 0$. 따라서 $\sigma_1 = \sqrt{25} = 5$,
  $\sigma_2 = 0$이다. 그대로 읽으면: 0이 아닌 특이값이 **하나**이므로 랭크 1, 즉 $C$는 평면을
  직선 하나로 뭉갠다. 그리고 $\|C\|_2 = \sigma_1 = 5$가 이 행렬이 무언가를 늘일 수 있는
  최대치다. 파괴되는 방향은 $\sigma_2 = 0$에 대응하는 우특이벡터, 여기서는 $(2,-1)/\sqrt5$ —
  검산: $C(2,-1) = (0,0)$ ✓. 2절의 영공간을 다른 길로 찾은 것이다.
- 연결: $\sigma_i^2$ = $A^\top A$의 고유값; 랭크 = 0이 아닌 $\sigma_i$의 수;
  $\|A\|_2 = \sigma_1$. 마지막 것이 **스펙트럼 노름**(행렬 2-노름)을 가장 큰 늘임으로 정의한
  것이다.
  $$\|A\|_2 = \max_{x \ne 0} \frac{\|Ax\|_2}{\|x\|_2} = \sigma_1$$
  가장 좋은 입력이 $v_1$이기 때문이다. 위의 $C$에서 입력 $(1,2)$는 $(5,10)$이 되어 정확히 $5$배
  늘어난다.
- **Eckart–Young**: 최적 랭크-$k$ 근사($\|\cdot\|_F$·$\|\cdot\|_2$ 기준)는 절단 SVD
  $A_k = \sum_{i\le k}\sigma_i u_i v_i^\top$이고, 그 오차는 정확히 버린 것만큼이다.
  $$\|A - A_k\|_2 = \sigma_{k+1}, \qquad \|A - A_k\|_F = \sqrt{\textstyle\sum_{i>k}\sigma_i^2}$$
  그래서 어떤 랭크-$k$ 행렬도 더 잘할 수 없다. 예: $A = \text{diag}(3,2,1)$, $k = 1$이면
  $\text{diag}(3,0,0)$을 남기고 오차는 2-노름으로 $2$, 프로베니우스로 $\sqrt5 = 2.236$이다.
  모델 압축과 PCA의 수학적 면허장.
  ([[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 관련되지만 다르다: 완성된 업데이트를
  SVD로 근사하는 게 아니라 업데이트 자체를 처음부터 저랭크로 *매개화*하는 경험적 설계다.)
- **PCA 네 줄 요약**: 데이터 $X$를 중심화; 공분산 $C = \frac1n X^\top X$; 그 상위
  고유벡터들 = 분산 최대 방향 = $X$의 오른쪽 특이벡터; 투영. 학습된 표현의 고전적
  조상이다. 즉 PCA(주성분 분석)는 선형 차원 축소다. 중심화한 샘플 $n$개를 행으로 담은 $X$에서
  주성분은
  $$C\,w_i = \lambda_i\,w_i, \qquad z = W_k^\top x$$
  를 푼다. $w_i$는 $i$번째 주방향, $\lambda_i$는 그 방향의 데이터 분산, $W_k$는 상위 $k$개 방향을
  모은 행렬, $z$는 샘플 $x$의 새 좌표 $k$개다. 단위 방향 $w$를 따른 분산이 $w^\top C w$이므로 분산이 최대인 방향이 곧 $C$의 고유벡터다. 남기는 분산 비율은
  $\sum_{i \le k}\lambda_i / \sum_i \lambda_i$다. 예: 점 $(2,0), (0,1), (-2,0), (0,-1)$은 이미
  평균이 0이고 $C = \text{diag}(2,\ 0.5)$이므로, 첫 주성분은 $(1,0)$으로 분산의
  $2/2.5 = 80\%$를 담고, 숫자 하나짜리 코드는 $2, 0, -2, 0$이다.

**곱은 오른쪽에서 왼쪽으로 읽는다.** Vᵀ가 입력을 특별한 입력 방향들의 성분으로 바꾼다. Σ가 각 성분을 늘이거나 지운다. U가 결과를 출력 좌표로 표현한다. 입력·출력 공간의 차원이 달라도 된다. A 자체의 고유벡터 해석을 쓸 수 없는 경우에도 SVD가 가능한 이유다.

위 특이 행렬의 0인 특이값은 사라지는 방향의 성분이 출력에 흔적을 남기지 않는다는 뜻이다. 출력에 없는 정보는 역행렬로 복원할 수 없다. 0은 아니지만 아주 작은 특이값도 관련 문제를 만든다. 입력 성분을 복원하려면 작은 수로 나눠야 하므로 신호와 함께 측정 오차도 증폭한다. 역문제를 풀기 전에 조건수를 보는 이유다.

**이해 확인.** 절단 SVD가 약한 방향을 버리면 복원 오차를 받아들이는 대신 더 단순하거나 안정적인 표현을 얻는다. 버린 방향이 내 과제에 중요하지 않다는 증거는 아니다. 분산이 작은 특징도 분류기나 로봇이 필요한 구분을 담을 수 있다. 행렬 근사 목적과 후속 과제 목적을 나눠야 한다.

### 4.5 유사역행렬 — $J^\dagger$가 무슨 뜻인가

기호 $A^\dagger$는 로보틱스 트랙 곳곳에 나온다 — 역기구학의 $J^\dagger$, 작업공간 제어의
$J^\dagger$ — 그리고 위의 SVD와 이 위키의 모든 솔버를 잇는 대상이다. 마주치는 행렬 대부분이
정사각이 아니어서 $A^{-1}$을 쓸 수 없기 때문에 존재한다.

**애초에 뒤집을 것이 있기는 한가?** $A^\top A$는 정확히 $A$의 열이 선형독립일 때 역을 갖는다.
한 줄이면 보인다. $A^\top A x = 0$이면 $x^\top A^\top A x = \lVert Ax \rVert^2 = 0$이므로
$Ax = 0$이고, 독립성에 의해 $x = 0$이다.

**공식이 둘이고, 어느 쪽을 얻는지는 모양이 정한다.**

| 모양 | 유사역행렬 | 정체 | 무엇을 계산하는가 |
|---|---|---|---|
| 키 크고 열이 독립 ($m > n$) | $A^\dagger = (A^\top A)^{-1}A^\top$ | 왼쪽 역원, $A^\dagger A = I$ | *과결정* 계의 최소자승해 |
| 넓고 행이 독립 ($m < n$) | $A^\dagger = A^\top (AA^\top)^{-1}$ | 오른쪽 역원, $AA^\dagger = I$ | *부족결정* 계의 *최소 노름* 해 |
| 정사각이고 가역 | 둘 다 | 역행렬 | $A^{-1}$ — 두 공식이 여기로 무너진다 |

그 두 행이 서로 다른 두 로보틱스 상황이다. 키 큰 쪽은 미지수보다 측정이 많은 경우 — 보정,
번들 조정, 점군에 평면 맞추기. 넓은 쪽은 과제 차원보다 관절이 많은 경우 — 여유자유도 팔이고,
요청한 도구 운동을 만드는 관절 속도가 무한히 많으므로 하나를 고르는 규칙이 필요하다.

**계산 — 여유자유도 팔에서의 최소 노름 규칙.** 단위 길이 링크 셋짜리 평면 팔을
$\theta = (0°, 90°, 0°)$에 두자. 관절 속도를 도구 속도로 보내는 야코비는 열 규칙(MR 5장)에서 나온다 — 각 열은 그 관절만 단위 속도로 돌릴 때 생기는 말단 속도다 — 그리고 $2 \times 3$이다 —
넓고, 따라서 여유자유도가 있다.

$$J = \begin{bmatrix} -2 & -2 & -1 \\ 1 & 0 & 0 \end{bmatrix}, \qquad JJ^\top = \begin{bmatrix} 9 & -2 \\ -2 & 1 \end{bmatrix}, \qquad \det JJ^\top = 5$$

최소 노름 규칙은 $J\dot\theta = v$를 만족하면서 $\lVert\dot\theta\rVert$를 최소화하는 데서 따라 나온다. 답이 오른쪽 유사역행렬이다:

$$J^\dagger = J^\top (JJ^\top)^{-1} = \begin{bmatrix} 0 & 1 \\ -0.4 & -0.8 \\ -0.2 & -0.4 \end{bmatrix}$$

도구를 위로 1 m/s로 올리라고 하자, 즉 $v = (0, 1)$. 그러면
$\dot\theta = J^\dagger v = (1,\, -0.8,\, -0.4)$이고 $\lVert\dot\theta\rVert = 1.342$다.

이제 여유자유도를 찾자. $J$의 영공간은 $n = (0,\, 0.447,\, -0.894)$가 친다 — $Jn = 0$을
확인하라. 그러므로 $\dot\theta + \alpha n$은 어떤 $\alpha$에 대해서도 **정확히 같은 도구
속도**를 만들고, 그 노름은 $\sqrt{1.8 + \alpha^2}$다. $\alpha = 1$이면 1.673, $\alpha = -1$
이어도 1.673. 모든 대안이 더 길다. "유사역행렬"의 내용이 그것으로 전부다. 일을 해내는 무한히
많은 관절 운동 중 가장 짧은 것을 돌려주고, 영공간은 남은 자유다 —
[[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장]]이 그것을 관절 한계와 장애물
회피에 쓴다.

**계산: 장치 P2, 과제가 쓰는 정방 경우.** 카탈로그 자세 $\theta=(0^\circ,90^\circ)$([[02-foundations/lab-plants|0.6]]):

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}.$$

말단 $(1,1)$에서 열을 그려라. 열 1은 $\dot\theta=(1,0)$의 말단 속도 $(-1,1)$, 열 2는 $(-1,0)$. $\det J=1$인 $2\times 2$ 역행렬 공식은 $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. 정방·가역이므로 표의 마지막 행이 $J^\dagger=J^{-1}$이라고 말한다. $J J^{-1}=I$. 과제는 그 두 행렬을 쓰고 같다고 말하라고 한다 — 방금 한 일이다. 위의 3링크는 가로로 넓어서 유사역행렬이 필요했고, P2는 아니다. P2가 SVD 이야기를 필요로 하는 것은 다음 문장이다. $\theta_2\to 0$이면 두 열이 평행해지고 $\det J\to 0$, $\kappa_2(J)\to\infty$, 옆방향 말단 운동이 사라진다. $J^\dagger$는 잃어버린 방향에서 아래 $\Sigma^\dagger$가 예측하는 대로 폭발한다.

**SVD의 관점, 그리고 $J^\dagger$가 폭발하는 이유.** §4에서 $A = U\Sigma V^\top$로 쓰면
유사역행렬은

$$A^\dagger = V\Sigma^\dagger U^\top, \qquad \Sigma^\dagger = \operatorname{diag}(1/\sigma_1,\, \ldots,\, 1/\sigma_r,\, 0,\, \ldots)$$

이다 — 0이 아닌 특이값만 뒤집고 0은 그대로 둔다. 이것이 계수가 모자란 것을 포함해 *모든*
행렬에서 통하는 정의이고, 위의 두 공식은 그 특수한 경우다. 그리고 실패 방식도 설명한다.
특이 자세 근처에서는 어떤 $\sigma_i \to 0$이므로 $1/\sigma_i \to \infty$가 되고 돌려받는
관절 속도가 특이 자세에 다가갈수록 그 한 방향으로 한없이 커진다. 팔에게 움직일 수 없는 방향으로 움직이라고 요구한 것이다. 특이 자세 그 자체에서는 유사역행렬이 그 0을 건드리지 않으므로, 계수가 실제로 떨어지는 순간 답이 불연속으로 뛴다.

**두 공식 뒤에 있는 정의.** 임의의 $m\times n$ 행렬 $A$의 (무어–펜로즈) 유사역행렬은 네 조건을
만족하는 유일한 $n\times m$ 행렬 $A^\dagger$다.

$$AA^\dagger A = A, \qquad A^\dagger A A^\dagger = A^\dagger, \qquad (AA^\dagger)^\top = AA^\dagger, \qquad (A^\dagger A)^\top = A^\dagger A$$

앞의 둘은 되돌릴 수 있는 곳에서는 $A^\dagger$가 $A$를 되돌린다는 뜻이고, 뒤의 둘은 곱
$AA^\dagger$와 $A^\dagger A$가 직교 투영이라는 뜻이다. 그래서 되돌릴 수 없는 부분은 제멋대로가
아니라 수직으로 버려진다. SVD 공식이 넷을 모두 만족하므로 그것이 일반 정의다. 위의 $J^\dagger$도
넷을 수치적으로(약 $10^{-16}$까지) 통과하고, $J^\dagger J$는 $I$가 아니라 행이 $(1,0,0)$,
$(0, 0.8, 0.4)$, $(0, 0.4, 0.2)$인 투영이다. 팔이 여유자유도를 가지므로 영공간 방향 $n$을 정확히
지우는 것이다.

해법은 작은 특이값을 정확히 뒤집는 일을 그만두는 것이다 — $1/\sigma$를
$\sigma/(\sigma^2 + \lambda)$로 바꾸면 모든 $\sigma$에 대해 유계이고 $\sigma^2 \gg \lambda$일
때는 $1/\sigma$와 같다. 그것이 **감쇠 최소자승**이다. 정확한 최소 노름 해 대신
$\lVert J\dot\theta - v\rVert^2 + \lambda\lVert\dot\theta\rVert^2$, 즉 추종 오차와 관절 속도의
절충을 최소화하며, 그 해는

$$J^\dagger_\lambda = J^\top (JJ^\top + \lambda I)^{-1}$$

이다. $\lambda > 0$이 감쇠다. $\lambda I$를 더하면 특이 자세에서도 행렬이 가역으로 남으므로 역이
폭발할 수 없다. 숫자로: $\lambda = 0.01$일 때 멀쩡한 $\sigma = 1$은 $1$ 대신 $0.990$으로, 특이에
가까운 $\sigma = 0.01$은 $100$ 대신 $0.990$으로 뒤집힌다. 위의 팔에서 같은 $\lambda$는 명령
$v = (0,1)$을 $(1,\ -0.8,\ -0.4)$ 대신 $\dot\theta = (0.982,\ -0.784,\ -0.392)$로 바꾼다 — 추종은
조금 덜하고 속도는 유계다. 그리고 이것은
[[02-foundations/optimization|4. 최적화 §3.5]]에서 만나게 될 신뢰 파라미터와 같은 $\lambda$다 —
이 페이지가 기대는 것이 아니라 앞을 가리키는 표지다. 그러니 사슬은 이렇게 이어진다: 특이값 → 유사역행렬
→ 그중 하나가 사라지면 벌어지는 일 → 감쇠 → Levenberg–Marquardt. 이름 넷, 발상 하나.

### 5. 제어이론과의 연결

선형대수는 제어의 언어 *그 자체*다 ([[04-robotics/index|제어 트랙]]):

- **상태공간 모델** $\dot{x} = Ax + Bu$, $y = Cx$: 시스템이 곧 행렬이다; 시뮬레이션은
  반복된 행렬곱이고, 행렬 지수 $e^{At}$가 입력이 없는 시스템의 정확한 해를 주고, 입력이 있으면 합성곱 $x(t) = e^{At}x_0 + \int_0^t e^{A(t-s)}Bu(s)\,ds$가 해다.
  기호: $x \in \mathbb{R}^n$은 **상태**(미래 입력과 함께 미래를 결정하는 숫자들),
  $u \in \mathbb{R}^m$은 입력, $y \in \mathbb{R}^p$는 측정 출력이고, $A$($n\times n$), $B$($n\times m$),
  $C$($p\times n$)는 각각 내부 동역학, 입력이 들어오는 방식, 센서가 보는 것이다(자세한 서술은
  [[04-robotics/control-theory-ce397|5. 제어 이론 §2]]). **행렬 지수**는 $e^{at}$와 같은 거듭제곱
  급수로 정의한다.
  $$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + \cdots$$
  그래서 $\frac{d}{dt}e^{At} = Ae^{At}$이고 $x(t) = e^{At}x_0$가 $\dot x = Ax$를 푼다. 예: 힘
  $u$로 미는 단위 질량의 상태를 (위치, 속도)로 두면 $A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$,
  $B = (0, 1)$이다. $A^2 = 0$이라 급수가 멈추고 $e^{At} = \begin{pmatrix}1&t\\0&1\end{pmatrix}$이며,
  위치 $0$, 속도 $1$에서 출발하면 $t = 2$ 뒤 상태는 $(2, 1)$이다.
- **안정성 = $A$의 고유값** (극점): 연속 시간은 모든 $\text{Re}(\lambda_i) < 0$일 때,
  이산 시간은 모든 $|\lambda_i| < 1$일 때 안정.
- **가제어성**: 입력이 상태를 실제로 어느 방향으로 밀 수 있나? 입력 한 스텝은 $B$의 열
  방향으로 움직이고, 동역학이 그 도달 범위를 $AB$로, 다시 $A^2B$로 회전시킨다. 그 도달
  방향들을 쌓아 —$[B, AB, \ldots, A^{n-1}B]$— 함께 $n$차원 전체를 생성하면($\text{rank}=n$)
  *모든* 상태에 도달 가능하고, 한 방향이라도 빠지면 어떤 입력 시퀀스도 상태를 그리로
  몰지 못한다. 판정식으로 쓰면
  $$\mathcal{C} = [\,B \;\; AB \;\; \cdots \;\; A^{n-1}B\,], \qquad \text{controllable} \iff \text{rank}\,\mathcal{C} = n$$
  이고 $\mathcal{C}$는 $n \times nm$ 가제어성 행렬이다. 그 뒤의 거듭제곱은 새 방향을 더하지
  못하므로 $A^{n-1}B$에서 멈춘다(케일리–해밀턴 논증은 [[04-robotics/control-theory-ce397|5. 제어 이론 §6]]).
  예: 위의 밀리는 질량은 $AB = (1, 0)$이라 $\mathcal{C} = \begin{pmatrix}0&1\\1&0\end{pmatrix}$,
  랭크 2다 — 힘 하나로 위치와 속도를 모두 몬다. 비예시: $A = \text{diag}(1, 2)$,
  $B = (1, 0)$이면 $\mathcal{C} = \begin{pmatrix}1&1\\0&0\end{pmatrix}$, 랭크 1이라 둘째 모드,
  그것도 불안정한 모드에 결코 영향을 줄 수 없다.
<svg viewBox="0 0 470 160" style="max-width:100%;height:auto" role="img" aria-label="가제어 vs 비가제어: 도달 가능한 방향">
  <g fill="currentColor" opacity="0.10"><polygon points="30,120 30,55 105,55 105,120"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35">
    <line x1="30" y1="120" x2="190" y2="120"/><line x1="30" y1="120" x2="30" y2="20"/>
    <line x1="280" y1="120" x2="440" y2="120"/><line x1="280" y1="120" x2="280" y2="20"/>
  </g>
  <defs><marker id="cArrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="2" marker-end="url(#cArrow)">
    <line x1="30" y1="120" x2="30" y2="58"/>
    <line x1="30" y1="120" x2="102" y2="58"/>
    <line x1="280" y1="120" x2="362" y2="120"/>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="36" y="52">B</text><text x="108" y="52">AB</text>
    <text x="368" y="116">B</text><text x="330" y="140">AB가 같은 직선 위에 있다</text>
    <text x="14" y="156" font-size="12">rank 2 → 모든 상태에 도달 가능</text>
    <text x="264" y="156" font-size="12">rank 1 → 한 방향에 도달 불가</text>
  </g>
</svg>

*왼쪽: $B$와 $AB$가 다른 방향을 가리켜 둘이 평면을 생성한다. 오른쪽: 동역학이 $B$를 자기 자신 위로만 돌려놓아, $u$를 어떻게 써도 상태 공간의 한 방향 전체에 닿지 못한다.*

  가관측성은 전치 쌍둥이다 — 출력 $y$가 결국 모든 상태를 드러낼 수 있는가? — 행렬은 $[C^\top, A^\top C^\top, \ldots]$이다.
  보통 방식으로 쌓으면
  $$\mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix}, \qquad \text{observable} \iff \text{rank}\,\mathcal{O} = n$$
  이고, 앞의 행렬의 전치라 랭크가 같다. $u = 0$일 때 $y, \dot y, \ddot y, \ldots$가
  $Cx, CAx, CA^2x, \ldots$와 같으므로, 이 묶음이 풀랭크일 때 정확히 $x$를 풀어낼 수 있기
  때문이다. 예: 밀리는 질량의 위치를 재면 $C = (1, 0)$, $\mathcal{O} = I$, 랭크 2로 가관측이다.
  비예시: 속도만 재면 $C = (0, 1)$, 행이 $(0,1)$과 $(0,0)$이라 랭크 1 — 속도 자료를 아무리 모아도
  질량이 어디서 출발했는지 알 수 없다.
- LQR 이득([[04-robotics/lqr-lqg|6. LQR/LQG]]), 칼만 필터([[02-foundations/probability|3. 확률 §5]]), MPC([[04-robotics/mpc|7. MPC]])가 전부 구조화된 행렬 계산으로 환원된다 — LQR과 칼만은 리카티 재귀(단계마다 선형 풀이 한 번), MPC는 응축(condensing: 상태를 소거해 입력만 변수로 남기는 것, [[04-robotics/mpc|7. MPC §2]]) 뒤의 조밀한 QP(이차 계획: 선형 제약 아래 이차 비용 최소화) — 수치 선형대수가 제어 엔지니어의 일상 도구인 이유.

### 6. 고차원의 기하 (논문 읽기용 직관)

- 평균이 0인(등방) 무작위 고차원 벡터들은 거의 직교한다: $\cos\theta$가 0 근처에 퍼짐 $\approx 1/\sqrt d$로 모인다(평균은 어느 차원에서나 이미 0이고, 평균이 0이 아닌 벡터들은 직교해지지 않는다) — 수백만 임베딩에 대한
  내적 검색이 *가능한* 이유 중 하나다: 무관한 항목의 점수가 0 근처로 깔린다. (관련 쌍의
  점수가 높은 것은 기하가 아니라 *학습된* 임베딩의 성질이다.)
- 거리가 집중된다: 가장 가까운 이웃과 가장 먼 이웃의 차이가 작다 — 원시 특징 위의 거리 대신 *학습된* 임베딩과 거리를 쓰는 이유 중 하나다. (코사인 유사도도 집중을 피하지 못한다: 단위 벡터에서 $\|a-b\|^2 = 2 - 2\cos\theta$이므로 이웃 순위는 유클리드 거리와 똑같다. 코사인이 더하는 것은 벡터 크기를 무시하는 것이다.)
- 다양체 가설: 실제 데이터는 픽셀 공간 속 저차원 곡면 위에 산다 —
  잠재 공간([[01-canonical-papers/notes/6-diffusion/vae|VAE]],
  [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]])의 암묵적 정당화.

> [!tip] 더 깊이 · Going deeper
> 이 페이지는 강의가 아니라 작업 세트다. 너무 빠르면 Boyd·Vandenberghe의 무료 교재 [*Introduction to Applied Linear Algebra*](https://web.stanford.edu/~boyd/vmls/)가 §1과 §2의 최소제곱 쪽을 더 천천히 간다. 다만 그 책은 모든 것을 일차독립과 QR로 세우고 랭크·열공간·영공간이라는 말을 쓰지 않는다, 고윳값·SVD 쪽은 Strang의 *Introduction to Linear Algebra*가 표준 첫 강의다. 각 개념이 논문 어디에 나타나는지는 이 페이지로 돌아와 보라.

### 스스로 점검

1. 비선형성 없는 선형층 두 개는 왜 하나로 접히는가? 그 합성의 랭크는 최대 얼마인가?
2. 정규방정식을 유도하고, 잔차가 $\text{col}(A)$에 직교하는 이유를 설명하라.
3. 이산 시스템 $x_{t+1} = Ax_t$의 고유값이 $0.9, 1.02$다. 무슨 일이, 어느 방향으로
   일어나는가?
4. [[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 왜 $B = 0$으로 초기화하는가? (0스텝에서
   $W_0 + BA$는 어떤 사상과 같은가?)

> [!tip]- 스스로 점검 정답 · Answers
> 1. $W_2(W_1 x) = (W_2 W_1)x$ — 곱이 곧 하나의 선형 사상이라 접힌다; 랭크는 $\min(\text{rank}\,W_1, \text{rank}\,W_2)$ 이하.
> 2. $\nabla\|Ax-b\|^2 = 2A^\top(Ax-b) = 0 \Rightarrow A^\top A\hat{x} = A^\top b$; 잔차 $r = b - A\hat{x}$는 $A^\top r = 0$ — $A$의 모든 열과 직교한다.
> 3. 0.9 고유방향 성분은 감쇠하고 1.02 방향 성분은 매 스텝 2%씩 지수 성장 — 상태는 결국 1.02의 고유벡터 방향으로 발산한다.
> 4. $B=0$이면 $\Delta W = BA = 0$이라 시작 시점에 $W_0 + BA = W_0$ — 학습이 정확히 사전학습 모델에서 출발한다(no-op 초기화).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**, $\theta=(0^\circ,90^\circ)$. 이 페이지 §4.5. 시간 스테퍼 없음.

1. **그리기.** 평면 팔: 베이스 원점, 엘보 $(1,0)$, 말단 $(1,1)$. $J$의 두 열을 말단의 화살로 (각 관절 단위속도가 만드는 말단 속도).
2. **유도.** $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$에서 $2\times 2$ 공식으로 $J^{-1}$. 이어서 §4.5 표의 정방·가역 행으로 $J^\dagger$. 둘이 같은지 확인하라.
3. **해석.** $\theta_1$을 고정하고 $\theta_2\to 0$. 두 열 화살, $\det J$, $\kappa_2(J)$는? 어떤 말단 운동이 불가능해지는가?

> [!tip]- 정답 · Solutions
> 1. 1열은 $(-1,1)$ (베이스를 도는 팔 전체). 2열은 $(-1,0)$ (엘보를 도는 전완).
> 2. $\det J=1$이므로 $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. 정방·가역 $\Rightarrow J^\dagger=J^{-1}$.
> 3. 열이 평행해진다($\theta=(0^\circ,0^\circ)$에서 둘 다 $\pm y$), $\det J\to 0$, $\kappa_2\to\infty$. 옆($x$) 말단 운동이 사라진다: 곧게 뻗은 팔은 유한 관절속도로 그것을 못 한다.
