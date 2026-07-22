---
title: Linear Algebra
tags: [foundations]
---

## English

Deep learning *is* linear algebra with nonlinearities between the matrix multiplies.
This page covers the working set for reading papers — what each concept *means* when it
shows up in a model.

### 1. Vectors, matrices, and what multiplication means

- A matrix is a **linear map**: $Wx$ rotates/scales/projects $x$ into a new space. Every
  linear layer, attention projection ($W_Q, W_K, W_V$), and embedding table is one.
- Matrix shapes as type-checking: $(d_{out} \times d_{in})(d_{in} \times 1)$ — reading
  shapes is how you read architectures.
- **Dot product** = similarity (up to norms): the core of attention scores $QK^\top$ and
  [[canonical-papers/notes/clip|CLIP]]'s cosine similarity.
- Norms: $\|x\|_2$ (length), $\|x\|_1$ (sparsity-inducing), Frobenius for matrices.

### 2. Rank, span, and subspaces

- **Rank** = dimensionality of the output space actually reachable — the number of
  independent directions a map preserves.
- Low-rank structure is a recurring theme: [[canonical-papers/notes/lora|LoRA]] assumes
  weight *updates* have low intrinsic rank ($\Delta W = BA$); bottleneck layers, projections,
  and compression all live here.
- Column space / null space: what a map can express / what it destroys.

### 3. Eigendecomposition & SVD

- Eigenvectors: directions a map only stretches, $Av = \lambda v$. Governs stability
  (power iteration, spectral radius) and optimization landscapes (Hessian eigenvalues =
  curvature; the condition number $\lambda_{max}/\lambda_{min}$ decides how painful
  gradient descent is — see [[50-foundations/optimization|optimization]]).
- **SVD** $A = U\Sigma V^\top$: *any* matrix = rotate → scale → rotate. Best rank-$k$
  approximation = keep top-$k$ singular values (Eckart–Young) — the mathematical license
  behind [[canonical-papers/notes/lora|LoRA]] and model compression.
- PCA = eigendecomposition of the covariance matrix — the classical ancestor of learned
  representations.

### 4. Matrix identities you'll actually meet

- $(AB)^\top = B^\top A^\top$; $(AB)^{-1} = B^{-1}A^{-1}$ (when invertible).
- Trace tricks: $\text{tr}(ABC) = \text{tr}(CAB)$ — appears in Gaussian KL formulas.
- Positive (semi-)definite matrices: covariances, Hessians at minima, kernel/Gram matrices —
  "PSD" in a paper means "this behaves like a squared quantity."
- Softmax$(QK^\top/\sqrt{d_k})V$ is three matrix multiplies and one normalization —
  the [[canonical-papers/notes/attention-is-all-you-need|Transformer]] in one line.

### 5. Geometry of high dimensions (paper-reading intuition)

- Random high-dim vectors are nearly orthogonal — why dot-product retrieval works at scale.
- Distances concentrate: "nearest" neighbors are barely nearer — why cosine similarity and
  learned metrics replace raw Euclidean distance.
- Manifold hypothesis: real data occupies a low-dimensional surface inside pixel space —
  the implicit justification for latent spaces ([[canonical-papers/notes/vae|VAE]], latent diffusion).

## 한국어

딥러닝은 행렬곱 사이에 비선형성을 끼운 선형대수 *그 자체*다. 이 페이지는 논문을 읽을 때
각 개념이 모델 안에서 *무엇을 의미하는지*를 중심으로 실전 세트를 담았다.

### 1. 벡터, 행렬, 그리고 곱셈의 의미

- 행렬은 **선형 사상**이다: $Wx$는 $x$를 회전/스케일/투영해 새 공간으로 보낸다. 모든 선형층,
  어텐션 투영($W_Q, W_K, W_V$), 임베딩 테이블이 이것이다.
- 행렬 모양은 타입 검사다: $(d_{out} \times d_{in})(d_{in} \times 1)$ — 모양을 읽는 것이
  구조를 읽는 방법이다.
- **내적** = (노름을 무시하면) 유사도: 어텐션 점수 $QK^\top$와
  [[canonical-papers/notes/clip|CLIP]] 코사인 유사도의 핵심.
- 노름: $\|x\|_2$(길이), $\|x\|_1$(희소성 유도), 행렬에는 프로베니우스.

### 2. 랭크, 생성 공간, 부분공간

- **랭크** = 사상이 실제로 도달할 수 있는 출력 공간의 차원 — 보존되는 독립 방향의 개수.
- 저랭크 구조는 반복되는 주제다: [[canonical-papers/notes/lora|LoRA]]는 가중치 *업데이트*의
  내재 랭크가 낮다고 가정한다($\Delta W = BA$); 병목층, 투영, 압축이 전부 여기 산다.
- 열공간 / 영공간: 사상이 표현할 수 있는 것 / 파괴하는 것.

### 3. 고유분해와 SVD

- 고유벡터: 사상이 늘이기만 하는 방향, $Av = \lambda v$. 안정성(거듭제곱 반복, 스펙트럼
  반지름)과 최적화 지형(헤시안 고유값 = 곡률; 조건수 $\lambda_{max}/\lambda_{min}$이
  경사 하강의 고통을 결정 — [[50-foundations/optimization|최적화]] 참고)을 지배한다.
- **SVD** $A = U\Sigma V^\top$: *모든* 행렬 = 회전 → 스케일 → 회전. 최적 랭크-$k$ 근사 =
  상위 $k$개 특이값만 남기기(Eckart–Young) — [[canonical-papers/notes/lora|LoRA]]와 모델
  압축의 수학적 면허장.
- PCA = 공분산 행렬의 고유분해 — 학습된 표현의 고전적 조상.

### 4. 실제로 만나게 될 행렬 항등식

- $(AB)^\top = B^\top A^\top$; $(AB)^{-1} = B^{-1}A^{-1}$ (가역일 때).
- 트레이스 트릭: $\text{tr}(ABC) = \text{tr}(CAB)$ — 가우시안 KL 공식에 등장.
- 양(준)정부호 행렬: 공분산, 최솟값에서의 헤시안, 커널/그람 행렬 — 논문의 "PSD"는
  "제곱량처럼 행동한다"는 뜻이다.
- Softmax$(QK^\top/\sqrt{d_k})V$는 행렬곱 세 번과 정규화 한 번 —
  [[canonical-papers/notes/attention-is-all-you-need|Transformer]]를 한 줄로 쓴 것.

### 5. 고차원의 기하 (논문 읽기용 직관)

- 무작위 고차원 벡터들은 거의 직교한다 — 내적 기반 검색이 대규모에서 통하는 이유.
- 거리가 집중된다: "가장 가까운" 이웃도 간신히 더 가깝다 — 코사인 유사도와 학습된 거리가
  유클리드 거리를 대체하는 이유.
- 다양체 가설: 실제 데이터는 픽셀 공간 속 저차원 곡면 위에 산다 — 잠재 공간
  ([[canonical-papers/notes/vae|VAE]], latent diffusion)의 암묵적 정당화.
