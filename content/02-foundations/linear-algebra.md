---
title: 1. Linear Algebra
tags: [foundations]
---

> [[02-foundations/overview|0. Overview]] — 이 페이지에 필요한 사전 수학과 다른 지식과의 연결 지도 · prerequisites & connection map

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
  architectures. Worked example — one attention head with $d_{model}=512$, $d_k=64$:
  $Q = XW_Q$ is $(T\times 512)(512\times 64) = T\times 64$; scores $QK^\top$ are $T\times T$;
  output $\text{softmax}(QK^\top/\sqrt{64})\,V$ is $T\times 64$. The whole
  [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] type-checks in one line.
- **Dot product and angle**: $\langle a,b\rangle = \|a\|\|b\|\cos\theta$. Cosine similarity
  $= \langle a,b\rangle / (\|a\|\|b\|)$ — the retrieval metric of
  [[01-canonical-papers/notes/3-vlm/clip|CLIP]].
- Norms: $\|x\|_2 = \sqrt{\sum x_i^2}$ (length, energy), $\|x\|_1 = \sum |x_i|$
  (sparsity-inducing — its "corners" touch axes first), $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$.

### 2. Linear systems, rank, and the four subspaces

- $Ax = b$ solvable ⟺ $b \in \text{col}(A)$ (column space). Gaussian elimination = row
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
    **condition number** $\kappa = \lambda_{max}/\lambda_{min}$ (for this SPD Hessian; for a
    general matrix the 2-norm condition number is the singular-value ratio
    $\kappa_2 = \sigma_{max}/\sigma_{min}$) *is* the difficulty of the problem — the fact [[01-canonical-papers/notes/1-foundations/adam|Adam]] and
    [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]] exist to fight.
- **Positive (semi-)definite**: symmetric $A$ with all $\lambda_i > 0$ ($\ge 0$);
  equivalently $x^\top A x > 0$ for all $x \ne 0$. Covariance matrices, Hessians at minima,
  and Gram/kernel matrices are PSD — "PSD" in a paper means "behaves like a squared quantity."

### 4. SVD — the one factorization that always exists

- **Every** matrix (any shape, any rank): $A = U\Sigma V^\top$ with orthogonal $U, V$ and
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$. Reading: rotate (input
  basis $V$) → scale (singular values) → rotate (output basis $U$).
- Connections: $\sigma_i^2$ = eigenvalues of $A^\top A$; rank = number of nonzero $\sigma_i$;
  $\|A\|_2 = \sigma_1$.
- **Eckart–Young**: the best rank-$k$ approximation (in $\|\cdot\|_F$ or $\|\cdot\|_2$) is
  truncated SVD $\sum_{i\le k}\sigma_i u_i v_i^\top$. This is the mathematical license for
  [[01-canonical-papers/notes/1-foundations/lora|LoRA]], model compression, and PCA.
- **PCA in four lines**: center data $X$; covariance $C = \frac1n X^\top X$; its top
  eigenvectors = directions of maximal variance = right singular vectors of $X$; project.
  Classical ancestor of every learned representation.

### 5. The control-theory connection

Linear algebra *is* the language of control ([[04-robotics/index|control track]]):

- **State-space model** $\dot{x} = Ax + Bu$, $y = Cx$: the system is a matrix; simulating
  is repeated matrix multiplication; the matrix exponential $e^{At}$ solves it exactly.
- **Stability = eigenvalues of $A$** (poles): continuous-time stable iff all
  $\text{Re}(\lambda_i) < 0$; discrete-time iff all $|\lambda_i| < 1$.
- **Controllability**: $\text{rank}[B, AB, \ldots, A^{n-1}B] = n$ — a rank condition
  decides whether any state is reachable; observability is its transpose twin
  ($[C^\top, A^\top C^\top, \ldots]$).
- LQR gains, Kalman filters, and MPC condensing all reduce to solving structured linear
  systems (Riccati equations) — numerical linear algebra is the control engineer's daily tool.

### 6. Geometry of high dimensions (paper-reading intuition)

- Random high-dim vectors are nearly orthogonal ($E[\cos\theta] \to 0$) — why dot-product
  retrieval over millions of embeddings works.
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
  계산 예시 — $d_{model}=512$, $d_k=64$인 어텐션 헤드 하나:
  $Q = XW_Q$는 $(T\times 512)(512\times 64) = T\times 64$; 점수 $QK^\top$는 $T\times T$;
  출력 $\text{softmax}(QK^\top/\sqrt{64})\,V$는 $T\times 64$.
  [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] 전체가 한 줄로 타입
  검사된다.
- **내적과 각도**: $\langle a,b\rangle = \|a\|\|b\|\cos\theta$. 코사인 유사도
  $= \langle a,b\rangle / (\|a\|\|b\|)$ — [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 검색 지표.
- 노름: $\|x\|_2 = \sqrt{\sum x_i^2}$(길이, 에너지), $\|x\|_1 = \sum |x_i|$(희소성 유도 —
  "모서리"가 축에 먼저 닿는다), $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$.

### 2. 선형계, 랭크, 그리고 네 개의 부분공간

- $Ax = b$가 풀린다 ⟺ $b \in \text{col}(A)$(열공간). 가우스 소거 = 삼각형 꼴로 가는 행
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
    $\kappa = \lambda_{max}/\lambda_{min}$(이 SPD 헤시안 기준; 일반 행렬의 2-노름 조건수는
    특이값 비 $\kappa_2 = \sigma_{max}/\sigma_{min}$)가 문제의 난이도 *그 자체*다 —
    [[01-canonical-papers/notes/1-foundations/adam|Adam]]과 [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]이
    존재하는 이유가 이것과의 싸움이다.
- **양(준)정부호**: 모든 $\lambda_i > 0$($\ge 0$)인 대칭 $A$; 동치로 모든 $x \ne 0$에서
  $x^\top A x > 0$. 공분산 행렬, 최솟값에서의 헤시안, 그람/커널 행렬이 PSD다 —
  논문의 "PSD"는 "제곱량처럼 행동한다"는 뜻.

### 4. SVD — 언제나 존재하는 유일한 분해

- **모든** 행렬(모양·랭크 불문): $A = U\Sigma V^\top$, $U, V$는 직교,
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$.
  독해: 회전(입력 기저 $V$) → 스케일(특이값) → 회전(출력 기저 $U$).
- 연결: $\sigma_i^2$ = $A^\top A$의 고유값; 랭크 = 0이 아닌 $\sigma_i$의 수;
  $\|A\|_2 = \sigma_1$.
- **Eckart–Young**: 최적 랭크-$k$ 근사($\|\cdot\|_F$·$\|\cdot\|_2$ 기준)는 절단 SVD
  $\sum_{i\le k}\sigma_i u_i v_i^\top$이다. [[01-canonical-papers/notes/1-foundations/lora|LoRA]], 모델 압축,
  PCA의 수학적 면허장.
- **PCA 네 줄 요약**: 데이터 $X$를 중심화; 공분산 $C = \frac1n X^\top X$; 그 상위
  고유벡터들 = 분산 최대 방향 = $X$의 오른쪽 특이벡터; 투영. 모든 학습된 표현의 고전적
  조상이다.

### 5. 제어이론과의 연결

선형대수는 제어의 언어 *그 자체*다 ([[04-robotics/index|제어 트랙]]):

- **상태공간 모델** $\dot{x} = Ax + Bu$, $y = Cx$: 시스템이 곧 행렬이다; 시뮬레이션은
  반복된 행렬곱이고, 행렬 지수 $e^{At}$가 정확한 해를 준다.
- **안정성 = $A$의 고유값** (극점): 연속 시간은 모든 $\text{Re}(\lambda_i) < 0$일 때,
  이산 시간은 모든 $|\lambda_i| < 1$일 때 안정.
- **가제어성**: $\text{rank}[B, AB, \ldots, A^{n-1}B] = n$ — 어떤 상태든 도달 가능한지를
  랭크 조건이 결정한다; 가관측성은 그 전치 쌍둥이($[C^\top, A^\top C^\top, \ldots]$).
- LQR 이득, 칼만 필터, MPC의 응축(condensing)이 전부 구조화된 선형계(리카티 방정식)
  풀이로 환원된다 — 수치 선형대수가 제어 엔지니어의 일상 도구인 이유.

### 6. 고차원의 기하 (논문 읽기용 직관)

- 무작위 고차원 벡터들은 거의 직교한다($E[\cos\theta] \to 0$) — 수백만 임베딩에 대한
  내적 검색이 통하는 이유.
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
