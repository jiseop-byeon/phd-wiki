---
title: Calculus & Backpropagation
tags: [foundations]
---

## English

The one algorithm every deep learning paper assumes silently: reverse-mode automatic
differentiation. This page builds it from the chain rule up, plus the gradient phenomena
(vanishing, exploding, stopping) that architectural history keeps responding to.

### 1. Derivatives as sensitivities

- $\frac{\partial L}{\partial w}$ answers: "if I nudge $w$, how much does the loss move?"
  Training is nothing but computing millions of these sensitivities and stepping against them.
- **Gradient** $\nabla_w L$: the vector of all sensitivities; points uphill; its negative is
  the locally steepest descent direction ([[50-foundations/optimization|optimization]]).
- **Jacobian** $J_{ij} = \partial y_i / \partial x_j$: sensitivities of a vector function —
  the object that chains when functions compose. (In robotics the *same* Jacobian maps joint
  velocities to end-effector velocities — [[20-robotics/index|Modern Robotics]].)

### 2. The chain rule, then backprop

- Composition: $L = f_3(f_2(f_1(x)))$ ⇒ $\frac{\partial L}{\partial x} = J_1^\top J_2^\top J_3^\top \cdot 1$.
- Two evaluation orders: forward-mode (input-side first) costs one pass *per input*;
  **reverse-mode** (output-side first) costs one pass *per output*. Losses are scalar
  (one output, millions of inputs) ⇒ reverse-mode wins — **backprop is exactly this choice**.
- Mechanics: forward pass caches intermediate activations; backward pass sweeps once,
  multiplying local Jacobians — total cost ≈ 2–3× a forward pass, memory ≈ storing activations
  (hence gradient checkpointing in large-model training).

### 3. Gradients through the classic layers

- Linear $y = Wx$: $\partial L/\partial W = (\partial L/\partial y)\,x^\top$ — outer product;
  weight gradients are "error × input."
- ReLU: gradient is a mask (1 where active, 0 where dead) — cheap, and the reason ReLU beat
  sigmoid ([[canonical-papers/notes/alexnet|AlexNet]]): no saturation region killing gradients.
- Softmax + cross-entropy: gradients simplify to $q - p$ (prediction minus target) — one of
  the tidiest results in the field; numerically stable via log-sum-exp.

### 4. The pathologies that shaped architecture history

- **Vanishing gradients**: products of many Jacobians with norms < 1 shrink exponentially —
  the disease of deep/recurrent nets. Treatments, in historical order:
  [[canonical-papers/notes/lstm|LSTM]]'s constant-error carousel,
  [[canonical-papers/notes/batch-norm|BatchNorm]]'s conditioning,
  [[canonical-papers/notes/resnet|ResNet]]'s identity paths ($\partial(x + F(x))/\partial x = I + \ldots$
  — the gradient always has a highway home).
- **Exploding gradients**: norms > 1 — treated with gradient clipping (standard in RNN/LLM training).
- **Stop-gradient**: deliberately cutting the graph ($\text{sg}[\cdot]$) — reparameterization
  ([[canonical-papers/notes/vae|VAE]]), target networks in RL, EMA teachers (DINO) all
  manipulate *where* gradients may flow. When a paper draws a dashed arrow, it's this.

### 5. Reading equations like an implementer

- Every $E[\cdot]$ in a loss becomes a mini-batch mean in code; every expectation over a
  distribution you can't sample becomes a bound ([[50-foundations/information-theory|ELBO]])
  or a trick (reparameterization, policy gradients — [[50-foundations/rl-basics|RL basics]]).
- Dimensional sanity: gradients always have the *same shape as the thing they differentiate
  with respect to* — the fastest error-check in existence.

## 한국어

모든 딥러닝 논문이 말없이 전제하는 단 하나의 알고리즘: 역방향 자동 미분. 이 페이지는
연쇄 법칙에서부터 그것을 쌓아 올리고, 구조 설계의 역사가 반복해서 응답해 온 그래디언트
현상들(소실, 폭발, 차단)을 정리한다.

### 1. 민감도로서의 미분

- $\frac{\partial L}{\partial w}$의 질문: "$w$를 살짝 밀면 손실이 얼마나 움직이는가?"
  학습이란 이 민감도 수백만 개를 계산해 반대 방향으로 내딛는 일일 뿐이다.
- **그래디언트** $\nabla_w L$: 민감도 전체의 벡터; 오르막을 가리키고, 그 반대가 국소적으로
  가장 가파른 하강 방향이다 ([[50-foundations/optimization|최적화]]).
- **야코비안** $J_{ij} = \partial y_i / \partial x_j$: 벡터 함수의 민감도 — 함수가 합성될 때
  연쇄되는 대상. (로보틱스에서 관절 속도를 말단 속도로 보내는 것도 *같은* 야코비안이다 —
  [[20-robotics/index|Modern Robotics]].)

### 2. 연쇄 법칙, 그리고 역전파

- 합성: $L = f_3(f_2(f_1(x)))$ ⇒ $\frac{\partial L}{\partial x} = J_1^\top J_2^\top J_3^\top \cdot 1$
- 두 가지 계산 순서: 순방향 모드는 *입력마다* 한 번의 패스, **역방향 모드**는 *출력마다*
  한 번의 패스가 든다. 손실은 스칼라(출력 1개, 입력 수백만 개) ⇒ 역방향 모드의 승리 —
  **역전파는 정확히 이 선택이다**.
- 동작: 순방향 패스가 중간 활성값을 캐시하고, 역방향 패스가 국소 야코비안들을 곱하며 한 번
  쓸고 지나간다 — 총비용 ≈ 순방향의 2~3배, 메모리 ≈ 활성값 저장
  (대형 모델 학습의 gradient checkpointing이 여기서 나온다).

### 3. 고전 층들의 그래디언트

- 선형층 $y = Wx$: $\partial L/\partial W = (\partial L/\partial y)\,x^\top$ — 외적;
  가중치 그래디언트는 "오차 × 입력"이다.
- ReLU: 그래디언트가 마스크다(살아 있으면 1, 죽었으면 0) — 싸고, ReLU가 시그모이드를 이긴
  이유다 ([[canonical-papers/notes/alexnet|AlexNet]]): 그래디언트를 죽이는 포화 구간이 없다.
- Softmax + 교차 엔트로피: 그래디언트가 $q - p$(예측 빼기 정답)로 단순해진다 — 이 분야에서
  가장 깔끔한 결과 중 하나; log-sum-exp로 수치 안정화.

### 4. 구조 설계의 역사를 만든 병리들

- **그래디언트 소실**: 노름이 1보다 작은 야코비안들의 곱은 지수적으로 준다 — 깊은/순환
  네트워크의 질병. 역사 순서대로의 처방:
  [[canonical-papers/notes/lstm|LSTM]]의 constant error carousel,
  [[canonical-papers/notes/batch-norm|BatchNorm]]의 조건수 개선,
  [[canonical-papers/notes/resnet|ResNet]]의 항등 경로 ($\partial(x + F(x))/\partial x = I + \ldots$
  — 그래디언트에게 언제나 집으로 가는 고속도로가 있다).
- **그래디언트 폭발**: 노름 > 1 — gradient clipping으로 처치 (RNN/LLM 학습의 표준).
- **Stop-gradient**: 그래프를 의도적으로 자르기 ($\text{sg}[\cdot]$) — reparameterization
  ([[canonical-papers/notes/vae|VAE]]), RL의 타깃 네트워크, EMA 교사(DINO) 모두
  그래디언트가 *어디로 흐를 수 있는가*를 조작한다. 논문의 점선 화살표가 바로 이것이다.

### 5. 구현자의 눈으로 수식 읽기

- 손실의 모든 $E[\cdot]$는 코드에서 미니배치 평균이 된다; 샘플링할 수 없는 분포에 대한
  기댓값은 하한([[50-foundations/information-theory|ELBO]])이나 트릭(reparameterization,
  정책 그래디언트 — [[50-foundations/rl-basics|RL 기초]])이 된다.
- 차원 검산: 그래디언트는 언제나 *미분 대상과 같은 모양*이다 — 세상에서 가장 빠른 오류 검사.
