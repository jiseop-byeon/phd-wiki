---
title: 2. Calculus & Backpropagation
tags: [foundations]
---

> [[02-foundations/overview|0. Overview]] — 이 페이지에 필요한 사전 수학과 다른 지식과의 연결 지도 · prerequisites & connection map

## English

The one algorithm every deep learning paper assumes silently: reverse-mode automatic
differentiation. Course-depth treatment: from Taylor expansion to a fully worked backprop
example, plus the gradient pathologies that shaped architecture history.

### 1. Derivatives as local linear models

- **Taylor expansion** is the foundation of all of optimization:
  $$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12 \delta^\top H \delta$$
  Gradient descent trusts the first-order term; Newton's method trusts the second
  ([[02-foundations/optimization|optimization]]).
- $\partial L/\partial w$ answers: "nudge $w$, how much does $L$ move?" Training =
  computing millions of these sensitivities and stepping against them.
- **Gradient** $\nabla_w L$: vector of all sensitivities; points uphill; perpendicular to
  level sets. **Jacobian** $J_{ij} = \partial y_i/\partial x_j$: the sensitivity matrix of
  a vector function — the object that *chains* under composition. (Robotics uses the same
  word for the same object: joint velocities → end-effector velocities,
  [[04-robotics/index|Modern Robotics]].)

### 2. The chain rule, and why backprop runs backwards

- Composition $L = f_3(f_2(f_1(x)))$:
  $\dfrac{\partial L}{\partial x} = J_1^\top J_2^\top J_3^\top \cdot 1$.
- Two evaluation orders for that product:
  - **Forward mode**: propagate $\partial/\partial x_i$ input-side first — one pass *per input*.
  - **Reverse mode**: propagate $\partial L/\partial(\cdot)$ output-side first — one pass *per output*.
- Losses are scalar: one output, millions of inputs ⇒ reverse mode computes *every*
  parameter gradient in a single backward pass. **Backprop is exactly this choice.**
- Autodiff mechanics: each primitive supplies a **VJP** (vector-Jacobian product)
  $v \mapsto J^\top v$; the framework composes them along the recorded graph.
  Cost ≈ 2–3× a forward pass; memory ≈ stored activations (hence gradient checkpointing:
  recompute instead of store).

### 3. Worked example — a 2-layer network, by hand

Network: $z = W_1 x$, $h = \text{ReLU}(z)$, $\hat y = W_2 h$, loss
$L = \tfrac12\|\hat y - y\|^2$. Backward pass, output to input:

1. $\dfrac{\partial L}{\partial \hat y} = \hat y - y \quad$ (call it $\delta_2$)
2. $\dfrac{\partial L}{\partial W_2} = \delta_2\, h^\top$ — **error × input**, an outer product
3. $\dfrac{\partial L}{\partial h} = W_2^\top \delta_2$ — the error, mapped backwards
4. $\dfrac{\partial L}{\partial z} = W_2^\top \delta_2 \odot \mathbb{1}[z > 0]$ — ReLU's
   gradient is a mask (call it $\delta_1$)
5. $\dfrac{\partial L}{\partial W_1} = \delta_1\, x^\top$

Every deep network's backward pass is this pattern iterated: *deltas flow backward through
transposes, weight gradients are outer products of deltas with cached activations.*
Dimensional sanity check: each gradient has the same shape as its variable — the fastest
bug detector in existence.

### 4. Gradients through the classic layers

- **Softmax + cross-entropy** — the tidiest result in the field. With logits $z$,
  $p = \text{softmax}(z)$, one-hot target $y$: $\dfrac{\partial L}{\partial z} = p - y$.
  (Derivation: $L = -\log p_c$; $\partial \log p_c/\partial z_j = \mathbb{1}[j=c] - p_j$.)
  Numerically stabilized via log-sum-exp.
- **ReLU**: mask gradient — cheap, non-saturating; the reason it beat sigmoid
  ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]). Dead units = permanently zero mask.
- **Sigmoid** $\sigma' = \sigma(1-\sigma) \le 1/4$: every saturating layer multiplies the
  backward signal by ≤ 0.25 — stack ten and gradients shrink a million-fold. This single
  inequality explains a decade of architecture history.

### 5. The pathologies that shaped architectures

- **Vanishing gradients**: products of Jacobians with norms < 1 decay exponentially with
  depth/time. Treatments, in historical order:
  - [[01-canonical-papers/notes/1-foundations/lstm|LSTM]]: a self-connection of weight exactly 1.0 — the
    error carousel where the product stops shrinking.
  - [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]: renormalize activations so Jacobians
    stay well-scaled (better conditioning).
  - [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]: $\partial(x + F(x))/\partial x = I + \partial F/\partial x$
    — the identity term guarantees the gradient always has an un-attenuated path home.
- **Exploding gradients**: norms > 1 — treated with gradient clipping (rescale $\|g\|$ to a
  ceiling), standard in RNN/LLM training.
- **Stop-gradient** $\text{sg}[\cdot]$: deliberately cut the graph. Reparameterization
  ([[01-canonical-papers/notes/6-diffusion/vae|VAE]]) moves sampling *outside* the differentiated path;
  EMA teachers ([[01-canonical-papers/notes/2-computer-vision/dino|DINO]]) and RL target networks receive no
  gradient by design. When a paper draws a dashed arrow, it means this.

### 6. Reading equations like an implementer

- Every $E[\cdot]$ in a loss becomes a minibatch mean. Every expectation you cannot sample
  through becomes a bound ([[02-foundations/information-theory|ELBO]]) or a trick
  (reparameterization; likelihood-ratio/policy gradients — [[02-foundations/rl-basics|RL basics]]).
- $\arg\max$ is not differentiable; softmax is its smooth stand-in (temperature controls
  the sharpness). Sampling is not differentiable; Gumbel-softmax / straight-through
  estimators fake it.
- Frameworks differentiate *programs*, not formulas: control flow, loops, and in-place ops
  all have gradient semantics — most "my loss doesn't decrease" bugs are graph bugs.

### Self-check

1. Redo the worked example with an MSE loss replaced by softmax-CE. What changes in step 1?
2. Show $\partial(x + F(x))/\partial x = I + J_F$ and explain why depth stops hurting.
3. Why does forward-mode autodiff cost one pass *per input parameter*, and why is that
   fatal for a 7B-parameter model?
4. In the [[01-canonical-papers/notes/6-diffusion/vae|VAE]], why can't you backprop through
   $z \sim \mathcal{N}(\mu, \sigma^2)$ directly, and how does $z = \mu + \sigma\epsilon$ fix it?

## 한국어

모든 딥러닝 논문이 말없이 전제하는 단 하나의 알고리즘: 역방향 자동 미분. 교재 수준의
서술: 테일러 전개에서 손으로 푸는 역전파 예제까지, 그리고 구조 설계의 역사를 만든
그래디언트 병리들.

### 1. 국소 선형 모델로서의 미분

- **테일러 전개**가 최적화 전체의 토대다:
  $$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12 \delta^\top H \delta$$
  경사 하강은 1차 항을, 뉴턴법은 2차 항까지 믿는다
  ([[02-foundations/optimization|최적화]]).
- $\partial L/\partial w$의 질문: "$w$를 살짝 밀면 $L$이 얼마나 움직이는가?" 학습 = 이
  민감도 수백만 개를 계산해 반대로 내딛는 일.
- **그래디언트** $\nabla_w L$: 민감도 전체의 벡터; 오르막을 가리키고 등고선에 수직이다.
  **야코비안** $J_{ij} = \partial y_i/\partial x_j$: 벡터 함수의 민감도 행렬 — 합성에서
  *연쇄되는* 대상. (로보틱스도 같은 대상에 같은 이름을 쓴다: 관절 속도 → 말단 속도,
  [[04-robotics/index|Modern Robotics]].)

### 2. 연쇄 법칙, 그리고 역전파가 뒤로 도는 이유

- 합성 $L = f_3(f_2(f_1(x)))$:
  $\dfrac{\partial L}{\partial x} = J_1^\top J_2^\top J_3^\top \cdot 1$
- 이 곱의 두 가지 계산 순서:
  - **순방향 모드**: $\partial/\partial x_i$를 입력 쪽부터 전파 — *입력마다* 한 패스.
  - **역방향 모드**: $\partial L/\partial(\cdot)$를 출력 쪽부터 전파 — *출력마다* 한 패스.
- 손실은 스칼라다: 출력 1개, 입력 수백만 개 ⇒ 역방향 모드가 backward 한 번으로 *모든*
  파라미터의 그래디언트를 계산한다. **역전파는 정확히 이 선택이다.**
- 자동 미분의 동작: 각 기본 연산이 **VJP**(벡터-야코비안 곱) $v \mapsto J^\top v$를
  제공하고, 프레임워크가 기록된 그래프를 따라 이를 합성한다.
  비용 ≈ 순방향의 2~3배; 메모리 ≈ 저장된 활성값 (gradient checkpointing: 저장 대신 재계산).

### 3. 계산 예제 — 2층 네트워크를 손으로

네트워크: $z = W_1 x$, $h = \text{ReLU}(z)$, $\hat y = W_2 h$, 손실
$L = \tfrac12\|\hat y - y\|^2$. 출력에서 입력으로 backward:

1. $\dfrac{\partial L}{\partial \hat y} = \hat y - y \quad$ (이것을 $\delta_2$라 하자)
2. $\dfrac{\partial L}{\partial W_2} = \delta_2\, h^\top$ — **오차 × 입력**, 외적이다
3. $\dfrac{\partial L}{\partial h} = W_2^\top \delta_2$ — 오차를 거꾸로 사상한 것
4. $\dfrac{\partial L}{\partial z} = W_2^\top \delta_2 \odot \mathbb{1}[z > 0]$ — ReLU의
   그래디언트는 마스크 (이것이 $\delta_1$)
5. $\dfrac{\partial L}{\partial W_1} = \delta_1\, x^\top$

모든 깊은 네트워크의 backward가 이 패턴의 반복이다: *델타는 전치를 타고 뒤로 흐르고,
가중치 그래디언트는 델타와 캐시된 활성값의 외적이다.* 차원 검산: 각 그래디언트는 그
변수와 같은 모양이다 — 세상에서 가장 빠른 버그 검출기.

### 4. 고전 층들의 그래디언트

- **Softmax + 교차 엔트로피** — 이 분야에서 가장 깔끔한 결과. 로짓 $z$,
  $p = \text{softmax}(z)$, 원-핫 정답 $y$일 때: $\dfrac{\partial L}{\partial z} = p - y$.
  (유도: $L = -\log p_c$; $\partial \log p_c/\partial z_j = \mathbb{1}[j=c] - p_j$.)
  log-sum-exp로 수치 안정화.
- **ReLU**: 마스크 그래디언트 — 싸고, 포화하지 않는다; 시그모이드를 이긴 이유다
  ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]). 죽은 유닛 = 영원히 0인 마스크.
- **시그모이드** $\sigma' = \sigma(1-\sigma) \le 1/4$: 포화 층 하나가 역방향 신호에 0.25
  이하를 곱한다 — 열 개를 쌓으면 그래디언트가 백만 배 준다. 이 부등식 하나가 구조
  설계사(史) 10년을 설명한다.

### 5. 구조를 만든 병리들

- **그래디언트 소실**: 노름 < 1인 야코비안들의 곱은 깊이/시간에 지수적으로 붕괴.
  역사 순서의 처방:
  - [[01-canonical-papers/notes/1-foundations/lstm|LSTM]]: 가중치가 정확히 1.0인 자기 연결 — 곱이 더는
    줄지 않는 오차 회전목마.
  - [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]: 활성값을 재정규화해 야코비안의
    스케일을 유지 (조건수 개선).
  - [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]:
    $\partial(x + F(x))/\partial x = I + \partial F/\partial x$ — 항등 항이 감쇠 없는
    귀갓길을 보장한다.
- **그래디언트 폭발**: 노름 > 1 — gradient clipping($\|g\|$를 상한으로 재스케일)으로
  처치, RNN/LLM 학습의 표준.
- **Stop-gradient** $\text{sg}[\cdot]$: 그래프를 의도적으로 자르기. reparameterization
  ([[01-canonical-papers/notes/6-diffusion/vae|VAE]])은 샘플링을 미분 경로 *밖으로* 옮기고, EMA
  교사([[01-canonical-papers/notes/2-computer-vision/dino|DINO]])와 RL 타깃 네트워크는 설계상 그래디언트를 받지
  않는다. 논문의 점선 화살표가 이것이다.

### 6. 구현자의 눈으로 수식 읽기

- 손실의 모든 $E[\cdot]$는 미니배치 평균이 된다. 통과해서 샘플링할 수 없는 기댓값은
  하한([[02-foundations/information-theory|ELBO]])이나 트릭(reparameterization;
  우도비/정책 그래디언트 — [[02-foundations/rl-basics|RL 기초]])이 된다.
- $\arg\max$는 미분 불가능하다; softmax가 그 매끄러운 대역이다(온도가 날카로움을 조절).
  샘플링도 미분 불가능하다; Gumbel-softmax / straight-through 추정기가 흉내 낸다.
- 프레임워크는 수식이 아니라 *프로그램*을 미분한다: 제어 흐름, 루프, in-place 연산에 전부
  그래디언트 의미론이 있다 — "손실이 안 줄어요" 버그의 대부분은 그래프 버그다.

### 스스로 점검

1. 계산 예제의 MSE를 softmax-CE로 바꾸면 1번 단계가 어떻게 바뀌는가?
2. $\partial(x + F(x))/\partial x = I + J_F$를 보이고, 깊이가 더는 해가 안 되는 이유를
   설명하라.
3. 순방향 모드 자동 미분은 왜 *입력 파라미터마다* 한 패스가 들고, 그것이 7B 모델에 왜
   치명적인가?
4. [[01-canonical-papers/notes/6-diffusion/vae|VAE]]에서 $z \sim \mathcal{N}(\mu, \sigma^2)$를 직접
   역전파할 수 없는 이유는, 그리고 $z = \mu + \sigma\epsilon$이 이를 고치는 방식은?
