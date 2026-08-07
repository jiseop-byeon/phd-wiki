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

Deep learning *is* linear algebra with nonlinearities between the matrix multiplies.
This page is a course-depth treatment: definitions, derivations, worked examples, and
where each concept appears in the papers of this wiki.

### 1. Vectors, matrices, and what multiplication means

- A matrix $W \in \mathbb{R}^{m\times n}$ is a **linear map** $\mathbb{R}^n \to \mathbb{R}^m$:
  it satisfies $W(ax + by) = aWx + bWy$. Every linear layer, attention projection
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
- **Dot product and angle**: $\langle a,b\rangle = \|a\|\|b\|\cos\theta$. Cosine similarity
  $= \langle a,b\rangle / (\|a\|\|b\|)$ — the retrieval metric of
  [[01-canonical-papers/notes/3-vlm/clip|CLIP]].
- Norms: $\|x\|_2 = \sqrt{\sum x_i^2}$ (length, energy), $\|x\|_1 = \sum |x_i|$
  (sparsity-inducing — its "corners" touch axes first), $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$.

### 2. Linear systems, rank, column space and null space

- $Ax = b$ solvable ⟺ $b \in \text{col}(A)$ — the **column space**, i.e. everything you can
  reach by scaling $A$'s columns and adding them up. ("Everything reachable from a set of
  vectors this way" is their **span**; the column space is the span of the columns.) Gaussian elimination = row
  operations to triangular form; LU factorization is elimination *recorded* so multiple
  right-hand sides are cheap.
- **Rank** = number of independent columns = number of independent rows = dimension of
  what the map can express. Rank-deficient ⇒ information is destroyed
  (null space $\{x: Ax = 0\}$ is nontrivial).
- **Least squares** — the most-used derivation in applied math. Overdetermined $Ax \approx b$:
  minimize $\|Ax - b\|^2$. Setting the gradient to zero:
  $$\nabla_x \|Ax-b\|^2 = 2A^\top(Ax - b) = 0 \;\Rightarrow\; A^\top A\, \hat{x} = A^\top b$$
  (the **normal equations**). Geometrically: $A\hat{x}$ is the orthogonal projection of $b$
  onto $\text{col}(A)$, and the residual is perpendicular to it. Linear regression,
  calibration, and the Kalman filter's update all live here.
- Low-rank structure recurs everywhere: [[01-canonical-papers/notes/1-foundations/lora|LoRA]] assumes weight
  *updates* have low intrinsic rank ($\Delta W = BA$ with $r \ll d$).

### 3. Eigendecomposition — directions a map only stretches

- $Av = \lambda v$: along eigenvector $v$, the map is pure scaling by $\lambda$. For
  symmetric $A$: real eigenvalues, orthogonal eigenvectors, $A = Q\Lambda Q^\top$
  (spectral theorem).
- Why you care, concretely:
  - **Powers**: $A^k = Q\Lambda^k Q^\top$ — long-run behavior is governed by the largest
    $|\lambda|$. Stability of $x_{t+1} = Ax_t$ ⟺ all $|\lambda_i| < 1$
    (continuous time $\dot x = Ax$: all $\text{Re}(\lambda_i) < 0$).
  - **Optimization landscapes**: for quadratic loss $\frac12 x^\top H x$, gradient descent
    converges per-eigendirection at rate $(1 - \alpha\lambda_i)$; the usable step size is
    set by $\lambda_{max}$, the slowest progress by $\lambda_{min}$. The
    **condition number** $\kappa = \lambda_{max}/\lambda_{min}$ (for this SPD — symmetric positive-definite, defined below — Hessian; for a
    general matrix the 2-norm condition number is the singular-value ratio
    $\kappa_2 = \sigma_{max}/\sigma_{min}$) *is* the difficulty of the problem — and poor conditioning is one useful lens on why
    adaptive optimization ([[01-canonical-papers/notes/1-foundations/adam|Adam]]) and normalization
    ([[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]) help.
- **Positive (semi-)definite**: symmetric $A$ with all $\lambda_i > 0$ ($\ge 0$);
  equivalently $x^\top A x > 0$ for all $x \ne 0$. Covariance matrices, Hessians at minima,
  and Gram/kernel matrices are PSD — "PSD" in a paper means "behaves like a squared quantity."

### 4. SVD — a universal factorization, available for every matrix

- **Every** matrix (any shape, any rank): $A = U\Sigma V^\top$ with **orthogonal** $U, V$ (columns unit-length and mutually
  perpendicular, so multiplying by one is a pure rotation/reflection — it stretches nothing) and
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$. Reading: rotate (input
  basis $V$) → scale (singular values) → rotate (output basis $U$).

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

- Connections: $\sigma_i^2$ = eigenvalues of $A^\top A$; rank = number of nonzero $\sigma_i$;
  $\|A\|_2 = \sigma_1$.
- **Eckart–Young**: the best rank-$k$ approximation (in $\|\cdot\|_F$ or $\|\cdot\|_2$) is
  truncated SVD $\sum_{i\le k}\sigma_i u_i v_i^\top$. This is the mathematical license for
  model compression and PCA. ([[01-canonical-papers/notes/1-foundations/lora|LoRA]] is related but
  different: it does not SVD-approximate a finished update — it *parameterizes* the update
  as low-rank from the start, an empirical design choice.)
- **PCA in four lines**: center data $X$; covariance $C = \frac1n X^\top X$; its top
  eigenvectors = directions of maximal variance = right singular vectors of $X$; project.
  A classical ancestor of learned representations.

### 5. The control-theory connection

Linear algebra *is* the language of control ([[04-robotics/index|control track]]):

- **State-space model** $\dot{x} = Ax + Bu$, $y = Cx$: the system is a matrix; simulating
  is repeated matrix multiplication; the matrix exponential $e^{At}$ solves it exactly.
- **Stability = eigenvalues of $A$** (poles): continuous-time stable iff all
  $\text{Re}(\lambda_i) < 0$; discrete-time iff all $|\lambda_i| < 1$.
- **Controllability**: which directions can the input actually push the state? One step
  of input moves you along the columns of $B$; the dynamics then rotate that reach into
  $AB$, then $A^2B$, and so on. Stack those reachable directions —
  $[B, AB, \ldots, A^{n-1}B]$ — and if together they span all $n$ dimensions
  ($\text{rank} = n$), *every* state is reachable; if they miss a direction, no input
  sequence ever drives the state there. 
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
- LQR gains, Kalman filters, and MPC condensing all reduce to solving structured linear
  systems (Riccati equations) — numerical linear algebra is the control engineer's daily tool.

### 6. Geometry of high dimensions (paper-reading intuition)

- Random high-dim vectors are nearly orthogonal ($E[\cos\theta] \to 0$) — one reason
  dot-product retrieval over millions of embeddings is *possible*: unrelated items score
  near zero. (That relevant pairs score high is a property of the *learned* embedding, not
  of geometry.)
- Distances concentrate: nearest and farthest neighbors differ by little — why cosine
  similarity and *learned* metrics replace raw Euclidean distance.
- Manifold hypothesis: real data occupies a low-dimensional surface inside pixel space —
  the implicit justification for latent spaces ([[01-canonical-papers/notes/6-diffusion/vae|VAE]],
  [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]]).

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

## 한국어

딥러닝은 행렬곱 사이에 비선형성을 끼운 선형대수 *그 자체*다. 이 페이지는 교재 수준의
서술이다: 정의, 유도, 계산 예시, 그리고 각 개념이 이 위키의 논문들 어디에서 나타나는지.

### 1. 벡터, 행렬, 그리고 곱셈의 의미

- 행렬 $W \in \mathbb{R}^{m\times n}$은 **선형 사상** $\mathbb{R}^n \to \mathbb{R}^m$이다:
  $W(ax + by) = aWx + bWy$를 만족한다. 모든 선형층, 어텐션 투영($W_Q, W_K, W_V$), 임베딩
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
- **내적과 각도**: $\langle a,b\rangle = \|a\|\|b\|\cos\theta$. 코사인 유사도
  $= \langle a,b\rangle / (\|a\|\|b\|)$ — [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 검색 지표.
- 노름: $\|x\|_2 = \sqrt{\sum x_i^2}$(길이, 에너지), $\|x\|_1 = \sum |x_i|$(희소성 유도 —
  "모서리"가 축에 먼저 닿는다), $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$.

### 2. 선형계, 랭크, 열공간과 영공간

- $Ax = b$가 풀린다 ⟺ $b \in \text{col}(A)$ — **열공간(column space)**, 즉 $A$의 열들을
  스칼라배해 더해서 도달할 수 있는 점 전체다. ("어떤 벡터 집합에서 이렇게 도달할 수 있는
  것 전체"를 그 집합의 **span**(생성)이라 하고, 열공간은 열들의 span이다.) 가우스 소거 = 삼각형 꼴로 가는 행
  연산; LU 분해는 소거 과정을 *기록*해 우변이 여러 개일 때 재사용을 싸게 만든 것.
- **랭크** = 독립인 열의 수 = 독립인 행의 수 = 사상이 표현할 수 있는 것의 차원.
  랭크 부족 ⇒ 정보가 파괴된다 (영공간 $\{x: Ax = 0\}$이 자명하지 않다).
- **최소제곱** — 응용수학에서 가장 많이 쓰는 유도. 과결정 $Ax \approx b$:
  $\|Ax - b\|^2$ 최소화. 그래디언트를 0으로 놓으면:
  $$\nabla_x \|Ax-b\|^2 = 2A^\top(Ax - b) = 0 \;\Rightarrow\; A^\top A\, \hat{x} = A^\top b$$
  (**정규방정식**). 기하적으로: $A\hat{x}$는 $b$를 $\text{col}(A)$에 직교 투영한 것이고,
  잔차는 거기에 수직이다. 선형 회귀, 캘리브레이션, 칼만 필터의 갱신이 모두 여기 산다.
- 저랭크 구조는 도처에서 반복된다: [[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 가중치
  *업데이트*의 내재 랭크가 낮다고 가정한다($r \ll d$인 $\Delta W = BA$).

### 3. 고유분해 — 사상이 늘이기만 하는 방향

- $Av = \lambda v$: 고유벡터 $v$ 방향에서 사상은 $\lambda$배 순수 스케일링이다.
  대칭 $A$: 실수 고유값, 직교 고유벡터, $A = Q\Lambda Q^\top$ (스펙트럼 정리).
- 구체적으로 왜 중요한가:
  - **거듭제곱**: $A^k = Q\Lambda^k Q^\top$ — 장기 거동은 가장 큰 $|\lambda|$가 지배한다.
    $x_{t+1} = Ax_t$의 안정성 ⟺ 모든 $|\lambda_i| < 1$
    (연속 시간 $\dot x = Ax$: 모든 $\text{Re}(\lambda_i) < 0$).
  - **최적화 지형**: 이차 손실 $\frac12 x^\top H x$에서 경사 하강은 고유방향별로
    $(1 - \alpha\lambda_i)$ 비율로 수렴한다; 쓸 수 있는 스텝 크기는 $\lambda_{max}$가,
    가장 느린 진전은 $\lambda_{min}$이 정한다. **조건수**
    $\kappa = \lambda_{max}/\lambda_{min}$(이 SPD — 대칭 양정부호, 아래에 정의 — 헤시안 기준; 일반 행렬의 2-노름 조건수는
    특이값 비 $\kappa_2 = \sigma_{max}/\sigma_{min}$)가 문제의 난이도 *그 자체*다 —
    나쁜 조건수는 적응형 최적화([[01-canonical-papers/notes/1-foundations/adam|Adam]])와
    정규화([[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]])가 왜 돕는지 이해하는
    유용한 관점 중 하나다.
- **양(준)정부호**: 모든 $\lambda_i > 0$($\ge 0$)인 대칭 $A$; 동치로 모든 $x \ne 0$에서
  $x^\top A x > 0$. 공분산 행렬, 최솟값에서의 헤시안, 그람/커널 행렬이 PSD다 —
  논문의 "PSD"는 "제곱량처럼 행동한다"는 뜻.

### 4. SVD — 모든 행렬에 존재하는 보편적 분해

- **모든** 행렬(모양·랭크 불문): $A = U\Sigma V^\top$, $U, V$는 **직교행렬**(열들이 길이 1이고 서로 수직 — 그래서 곱하는
  것은 순수한 회전/반사이고 아무것도 늘이지 않는다),
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$.
  독해: 회전(입력 기저 $V$) → 스케일(특이값) → 회전(출력 기저 $U$).

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

- 연결: $\sigma_i^2$ = $A^\top A$의 고유값; 랭크 = 0이 아닌 $\sigma_i$의 수;
  $\|A\|_2 = \sigma_1$.
- **Eckart–Young**: 최적 랭크-$k$ 근사($\|\cdot\|_F$·$\|\cdot\|_2$ 기준)는 절단 SVD
  $\sum_{i\le k}\sigma_i u_i v_i^\top$이다. 모델 압축과 PCA의 수학적 면허장.
  ([[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 관련되지만 다르다: 완성된 업데이트를
  SVD로 근사하는 게 아니라 업데이트 자체를 처음부터 저랭크로 *매개화*하는 경험적 설계다.)
- **PCA 네 줄 요약**: 데이터 $X$를 중심화; 공분산 $C = \frac1n X^\top X$; 그 상위
  고유벡터들 = 분산 최대 방향 = $X$의 오른쪽 특이벡터; 투영. 학습된 표현의 고전적
  조상이다.

### 5. 제어이론과의 연결

선형대수는 제어의 언어 *그 자체*다 ([[04-robotics/index|제어 트랙]]):

- **상태공간 모델** $\dot{x} = Ax + Bu$, $y = Cx$: 시스템이 곧 행렬이다; 시뮬레이션은
  반복된 행렬곱이고, 행렬 지수 $e^{At}$가 정확한 해를 준다.
- **안정성 = $A$의 고유값** (극점): 연속 시간은 모든 $\text{Re}(\lambda_i) < 0$일 때,
  이산 시간은 모든 $|\lambda_i| < 1$일 때 안정.
- **가제어성**: 입력이 상태를 실제로 어느 방향으로 밀 수 있나? 입력 한 스텝은 $B$의 열
  방향으로 움직이고, 동역학이 그 도달 범위를 $AB$로, 다시 $A^2B$로 회전시킨다. 그 도달
  방향들을 쌓아 —$[B, AB, \ldots, A^{n-1}B]$— 함께 $n$차원 전체를 생성하면($\text{rank}=n$)
  *모든* 상태에 도달 가능하고, 한 방향이라도 빠지면 어떤 입력 시퀀스도 상태를 그리로
  몰지 못한다. 
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

  가관측성은 전치 쌍둥이($[C^\top, A^\top C^\top, \ldots]$).
- LQR 이득, 칼만 필터, MPC의 응축(condensing)이 전부 구조화된 선형계(리카티 방정식)
  풀이로 환원된다 — 수치 선형대수가 제어 엔지니어의 일상 도구인 이유.

### 6. 고차원의 기하 (논문 읽기용 직관)

- 무작위 고차원 벡터들은 거의 직교한다($E[\cos\theta] \to 0$) — 수백만 임베딩에 대한
  내적 검색이 *가능한* 이유 중 하나다: 무관한 항목의 점수가 0 근처로 깔린다. (관련 쌍의
  점수가 높은 것은 기하가 아니라 *학습된* 임베딩의 성질이다.)
- 거리가 집중된다: 가장 가까운 이웃과 가장 먼 이웃의 차이가 작다 — 코사인 유사도와
  *학습된* 거리가 유클리드 거리를 대체하는 이유.
- 다양체 가설: 실제 데이터는 픽셀 공간 속 저차원 곡면 위에 산다 —
  잠재 공간([[01-canonical-papers/notes/6-diffusion/vae|VAE]],
  [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]])의 암묵적 정당화.

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
