---
title: 2. Calculus & Backpropagation
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §1–2]] (derivatives, chain rule, Taylor) · [[02-foundations/linear-algebra|1. Linear Algebra §1]] (matrix shapes and transpose) · [[02-foundations/neural-network-basics|0.7]] (what a layer and a loss are)
> [[02-foundations/engineering-math|0.5 §1–2]](미분·연쇄 법칙·테일러) · [[02-foundations/linear-algebra|1. 선형대수 §1]](행렬 모양과 전치) · [[02-foundations/neural-network-basics|0.7]](층과 손실이 무엇인지)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

The one algorithm every deep learning paper assumes silently: reverse-mode automatic
differentiation. Course-depth treatment: from Taylor expansion to a fully worked backprop
example, plus the gradient pathologies that shaped architecture history.

### 1. Derivatives as local linear models

- **Taylor expansion** is the foundation of all of optimization:
  $$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12 \delta^\top H \delta$$
  ($H$ is the **Hessian** — the matrix of second derivatives $H_{ij}=\partial^2 f/\partial x_i \partial x_j$,
  the multivariable version of $f''$.) Gradient descent trusts the first-order term;
  Newton's method trusts the second ([[02-foundations/optimization|optimization]]).
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
  **Two things in that line deserve a sentence.** The trailing $1$ is $\partial L/\partial L$ —
  the loss's sensitivity to itself, where every backward pass starts; frameworks literally
  call `backward()` on a scalar and seed it with 1. The **transposes** are there because a
  Jacobian $J$ maps input perturbations *forward* into output perturbations, while here we
  are carrying sensitivities *backward* from the output — $J^\top$ is that same map run the
  other way. Shape-check it: if $f_1: \mathbb{R}^n \to \mathbb{R}^m$ then $J_1$ is $m\times n$,
  so only $J_1^\top$ ($n\times m$) can produce something the size of $x$.
- Two evaluation orders for that product:
  - **Forward mode**: propagate $\partial/\partial x_i$ input-side first — one pass *per input*.
  - **Reverse mode**: propagate $\partial L/\partial(\cdot)$ output-side first — one pass *per output*.
- Losses are scalar: one output, millions of inputs ⇒ reverse mode computes *every*
  parameter gradient in a single backward pass. **Backprop is exactly this choice.**
  **Put numbers on it.** A modest network with $10^7$ parameters and one scalar loss:
  forward mode would need one pass *per parameter*, so $10^7$ passes; reverse mode needs
  **one**. At roughly 2–3× the cost of a forward pass, that is a speedup of about seven
  orders of magnitude — and it is the only reason training large models is possible at all.
  The asymmetry is not a clever trick; it falls straight out of the shape of the problem
  (many inputs, one output), and it would reverse if you ever needed the sensitivity of many
  outputs to *one* input.
- Autodiff mechanics: each primitive supplies a **VJP** (vector-Jacobian product)
  $v \mapsto J^\top v$; the framework composes them along the recorded graph.
  Cost ≈ 2–3× a forward pass; memory ≈ stored activations (hence gradient checkpointing:
  recompute instead of store).

### 3. Worked example — a 2-layer network, by hand

Network: $z = W_1 x$, $h = \text{ReLU}(z)$, $\hat y = W_2 h$, loss
$L = \tfrac12\|\hat y - y\|^2$. Backward pass, output to input:

1. $\dfrac{\partial L}{\partial \hat y} = \hat y - y \quad$ (call it $\delta_2$)
2. $\dfrac{\partial L}{\partial W_2} = \delta_2\, h^\top$ — **error × input**, an *outer product*
   (a column times a row, which produces a whole matrix — the same shape as $W_2$)
3. $\dfrac{\partial L}{\partial h} = W_2^\top \delta_2$ — the error, mapped backwards
4. $\dfrac{\partial L}{\partial z} = W_2^\top \delta_2 \odot \mathbb{1}[z > 0]$ — ReLU's
   gradient is a mask (call it $\delta_1$)
5. $\dfrac{\partial L}{\partial W_1} = \delta_1\, x^\top$

**Now with actual numbers** — the *same* network as
[[02-foundations/neural-network-basics|0.7 §2]], so nothing new has to be set up:
$W_1 = \begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$,
$W_2 = \begin{pmatrix}1&-1&0.5\end{pmatrix}$, $x = (1,2)$. Forward, from that page:
$z = (1,2,3)$, $h = (1,2,3)$, $\hat y = 0.5$. Suppose the target is $y = 1$, so
$L = \tfrac12(0.5-1)^2 = 0.125$. Backward, one line per step above:

| Step | Formula | Numbers |
|---|---|---|
| 1 | $\delta_2 = \hat y - y$ | $0.5 - 1 = -0.5$ |
| 2 | $\partial L/\partial W_2 = \delta_2 h^\top$ | $-0.5\,(1,2,3) = (-0.5,\,-1,\,-1.5)$ |
| 3 | $\partial L/\partial h = W_2^\top\delta_2$ | $-0.5\,(1,-1,0.5) = (-0.5,\,0.5,\,-0.25)$ |
| 4 | $\delta_1 = \partial L/\partial h \odot \mathbb{1}[z>0]$ | mask is $(1,1,1)$ since $z>0$, so $\delta_1 = (-0.5,\,0.5,\,-0.25)$ |
| 5 | $\partial L/\partial W_1 = \delta_1 x^\top$ | $\begin{pmatrix}-0.5&-1\\0.5&1\\-0.25&-0.5\end{pmatrix}$ |

Three things to notice, and they generalize to every network you will read about:
- **The sign says what to do.** $\delta_2 = -0.5$ is negative because the prediction was
  *too low*; gradient descent subtracts the gradient, so every weight feeding a positive
  activation goes **up**. The arithmetic is doing the obvious thing.
- **Bigger activation, bigger gradient.** In step 2 the third weight gets $-1.5$ while the
  first gets $-0.5$, purely because $h_3 = 3$ was the loudest input. Credit is assigned in
  proportion to who spoke.
- **Shapes match their variables.** $\partial L/\partial W_1$ came out $3\times2$, exactly
  $W_1$'s shape. If yours does not, you have a bug — no exceptions.

Each step above *is* one VJP: step 3, $W_2^\top\delta_2$, is the layer's Jacobian-transpose
applied to the incoming $\delta$ — you just did by hand what §2 described abstractly. Every
deep network's backward pass is this pattern iterated: *deltas flow backward through
transposes, weight gradients are outer products of deltas with cached activations.*
Dimensional sanity check: each gradient has the same shape as its variable — the fastest
bug detector in existence.

<svg viewBox="0 0 560 175" style="max-width:100%;height:auto" role="img" aria-label="forward and backward pass through a two-layer network">
  <defs><marker id="bpF" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="20" y="52" width="62" height="34" rx="4"/><rect x="140" y="52" width="62" height="34" rx="4"/>
    <rect x="260" y="52" width="72" height="34" rx="4"/><rect x="380" y="52" width="62" height="34" rx="4"/>
    <rect x="490" y="52" width="52" height="34" rx="4"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="51" y="74">x</text><text x="171" y="74">z = W₁x</text><text x="296" y="74">h = ReLU(z)</text><text x="411" y="74">ŷ = W₂h</text><text x="516" y="74">L</text>
  </g>
  <g stroke="currentColor" stroke-width="1.5" marker-end="url(#bpF)">
    <line x1="82" y1="62" x2="138" y2="62"/><line x1="202" y1="62" x2="258" y2="62"/>
    <line x1="332" y1="62" x2="378" y2="62"/><line x1="442" y1="62" x2="488" y2="62"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" marker-end="url(#bpF)" stroke-dasharray="5 3" opacity="0.85">
    <line x1="488" y1="78" x2="444" y2="78"/><line x1="378" y1="78" x2="334" y2="78"/>
    <line x1="258" y1="78" x2="204" y2="78"/><line x1="138" y1="78" x2="84" y2="78"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">
    <text x="466" y="102">δ₂ = ŷ − y</text><text x="356" y="102">W₂ᵀδ₂</text><text x="231" y="102">⊙ 1[z&gt;0] = δ₁</text><text x="111" y="102">W₁ᵀδ₁</text>
    <text x="411" y="128">∂L/∂W₂ = δ₂hᵀ</text><text x="171" y="128">∂L/∂W₁ = δ₁xᵀ</text>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="20" y="34">forward →</text><text x="20" y="160" opacity="0.85">← backward (dashed): deltas travel through transposes, weight gradients are outer products</text>
  </g>
</svg>



### 4. Gradients through the classic layers

- **Softmax + cross-entropy** — the tidiest result in the field, and *not* a legacy topic:
  it is still how every LLM is trained (next-token prediction is one softmax over the
  vocabulary, scored by cross-entropy), how every classification head works, and softmax is
  the operation inside attention itself
  ([[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]). Even robot
  policies use it when actions are discretized into tokens
  ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]] bins each action dimension into 256 values, making
  control a classification problem). The main exception worth knowing: policies with
  continuous-valued outputs — regression heads, and
  [[01-canonical-papers/notes/4-vla/diffusion-policy|diffusion]]/flow-matching policies — are
  trained with squared error instead.
  With logits $z$, $p = \text{softmax}(z)$, one-hot target $y$:
  $\dfrac{\partial L}{\partial z} = p - y$ — *predicted minus true*, and nothing else.
  (Derivation: $L = -\log p_c$; $\partial \log p_c/\partial z_j = \mathbb{1}[j=c] - p_j$.)
  Computed in practice through log-sum-exp so the exponentials cannot overflow — derived in
  [[02-foundations/engineering-math|0.5 §6]].
- **ReLU**: mask gradient — cheap, non-saturating; the reason it beat sigmoid
  ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]). Dead units = permanently zero mask.
- **Sigmoid** $\sigma' = \sigma(1-\sigma) \le 1/4$: every saturating layer multiplies the
  backward signal by ≤ 0.25 — from the sigmoid derivatives alone, ten saturated layers
  attenuate gradients roughly a million-fold (the full gradient also carries weight
  Jacobians). This single inequality explains a decade of architecture history.

### 5. The pathologies that shaped architectures

- **Vanishing gradients**: products of Jacobians with norms < 1 decay exponentially with
  depth/time. Treatments, in historical order:
  - [[01-canonical-papers/notes/1-foundations/lstm|LSTM]]: a self-connection of weight exactly 1.0 — the
    error carousel where the product stops shrinking.
  - [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]: renormalize activations so Jacobians
    stay well-scaled (better conditioning) — one of several proposed explanations; *why*
    BatchNorm works is still debated (see the note).
  - [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]: $\partial(x + F(x))/\partial x = I + \partial F/\partial x$
    — the identity term gives the gradient a direct, unattenuated path — it *mitigates*
    vanishing (a path exists) rather than guaranteeing the total gradient never decays.
- **Exploding gradients**: norms > 1 — treated with gradient clipping (rescale $\|g\|$ to a
  ceiling), standard in RNN/LLM training.
- **Stop-gradient** $\text{sg}[\cdot]$: deliberately cut the graph. Reparameterization
  ([[01-canonical-papers/notes/6-diffusion/vae|VAE]]) moves sampling *outside* the differentiated path;
  EMA teachers ([[01-canonical-papers/notes/2-computer-vision/dino|DINO]]) and RL target networks receive no
  gradient by design. A dashed arrow in a paper figure *often* denotes stop-gradient —
  but it can also mean an auxiliary or inference-only path, so always check the legend.

### 6. Reading equations like an implementer

- Every $E[\cdot]$ in a loss becomes a minibatch mean. In deep learning, expectations you
  cannot differentiate through are typically handled with a bound ([[02-foundations/information-theory|ELBO]]),
  a Monte Carlo estimator, or a trick
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

> [!tip]- Answers
> 1. Only step 1 changes: $\delta_2$ becomes $p - y$ (the softmax + cross-entropy gradient) instead of $\hat y - y$. Steps 2–5 are identical — the backward pattern does not care which loss produced the incoming delta.
> 2. The derivative of a sum is the sum of derivatives: $\partial(x + F(x))/\partial x = I + \partial F/\partial x = I + J_F$. The identity term gives the backward signal one path that is never multiplied down, so depth stops *forcing* decay — it mitigates vanishing rather than guaranteeing the total gradient never shrinks.
> 3. Forward mode propagates sensitivities with respect to *one* input direction per pass, so covering 7B parameters would need 7B passes. Reverse mode propagates from a *scalar* loss, so a single backward pass yields every parameter gradient — the asymmetry is why training is possible at all.
> 4. Sampling is a stochastic branch with no derivative with respect to $\mu, \sigma$. Rewriting $z = \mu + \sigma\epsilon$ with $\epsilon \sim \mathcal{N}(0,1)$ pushes the randomness into an *external input*, leaving a deterministic, differentiable function of $\mu$ and $\sigma$ — gradients now flow to the encoder.

## 한국어

모든 딥러닝 논문이 말없이 전제하는 단 하나의 알고리즘: 역방향 자동 미분. 교재 수준의
서술: 테일러 전개에서 손으로 푸는 역전파 예제까지, 그리고 구조 설계의 역사를 만든
그래디언트 병리들.

### 1. 국소 선형 모델로서의 미분

- **테일러 전개**가 최적화 전체의 토대다:
  $$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12 \delta^\top H \delta$$
  ($H$는 **헤시안** — 2차 도함수의 행렬 $H_{ij}=\partial^2 f/\partial x_i \partial x_j$,
  $f''$의 다변수 버전이다.) 경사 하강은 1차 항을, 뉴턴법은 2차 항까지 믿는다
  ([[02-foundations/optimization|최적화]]).
- $\partial L/\partial w$의 질문: "$w$를 살짝 밀면 $L$이 얼마나 움직이는가?" 학습 = 이
  민감도 수백만 개를 계산해 반대로 내딛는 일.
- **그래디언트** $\nabla_w L$: 민감도 전체의 벡터; 오르막을 가리키고 등고선에 수직이다.
  **야코비안** $J_{ij} = \partial y_i/\partial x_j$: 벡터 함수의 민감도 행렬 — 합성에서
  *연쇄되는* 대상. (로보틱스도 같은 대상에 같은 이름을 쓴다: 관절 속도 → 말단 속도,
  [[04-robotics/index|Modern Robotics]].)

### 2. 연쇄 법칙, 그리고 역전파가 뒤로 도는 이유

- 합성 $L = f_3(f_2(f_1(x)))$:
  $\dfrac{\partial L}{\partial x} = J_1^\top J_2^\top J_3^\top \cdot 1$.
  **이 줄에서 두 가지는 한 문장씩 설명할 값이 있다.** 끝의 $1$은 $\partial L/\partial L$ —
  손실의 자기 자신에 대한 민감도이고 모든 역전파가 여기서 시작한다. 프레임워크가 스칼라에
  `backward()`를 부르며 1을 씨앗으로 놓는 것이 문자 그대로 이것이다. **전치**가 붙은 이유는,
  야코비안 $J$가 입력의 섭동을 *앞으로* 밀어 출력의 섭동으로 보내는 사상인데 여기서는
  민감도를 출력에서 *뒤로* 나르고 있기 때문이다 — $J^\top$이 그 사상을 반대 방향으로 돌린
  것이다. 모양으로 확인하면: $f_1: \mathbb{R}^n \to \mathbb{R}^m$이면 $J_1$이 $m\times n$이므로
  $x$ 크기의 결과를 낼 수 있는 것은 $J_1^\top$($n\times m$)뿐이다.
- 이 곱의 두 가지 계산 순서:
  - **순방향 모드**: $\partial/\partial x_i$를 입력 쪽부터 전파 — *입력마다* 한 패스.
  - **역방향 모드**: $\partial L/\partial(\cdot)$를 출력 쪽부터 전파 — *출력마다* 한 패스.
- 손실은 스칼라다: 출력 1개, 입력 수백만 개 ⇒ 역방향 모드가 backward 한 번으로 *모든*
  파라미터의 그래디언트를 계산한다. **역전파는 정확히 이 선택이다.**
  **숫자를 붙여 보자.** 파라미터 $10^7$개에 스칼라 손실 하나인 평범한 신경망이라면, 순방향
  모드는 *파라미터마다* 한 패스가 필요하니 $10^7$번, 역방향 모드는 **한 번**이다. 역방향
  패스가 순방향의 2~3배 비용이므로 대략 7자릿수의 차이이고, 대형 모델 학습이 가능한 이유가
  오직 이것이다. 이 비대칭은 영리한 요령이 아니라 문제의 모양(입력 다수, 출력 하나)에서 곧장
  나오는 것이고, 만약 *하나의* 입력에 대한 다수 출력의 민감도가 필요했다면 우열이 뒤집힌다.
- 자동 미분의 동작: 각 기본 연산이 **VJP**(벡터-야코비안 곱) $v \mapsto J^\top v$를
  제공하고, 프레임워크가 기록된 그래프를 따라 이를 합성한다.
  비용 ≈ 순방향의 2~3배; 메모리 ≈ 저장된 활성값 (gradient checkpointing: 저장 대신 재계산).

### 3. 계산 예제 — 2층 네트워크를 손으로

네트워크: $z = W_1 x$, $h = \text{ReLU}(z)$, $\hat y = W_2 h$, 손실
$L = \tfrac12\|\hat y - y\|^2$. 출력에서 입력으로 backward:

1. $\dfrac{\partial L}{\partial \hat y} = \hat y - y \quad$ (이것을 $\delta_2$라 하자)
2. $\dfrac{\partial L}{\partial W_2} = \delta_2\, h^\top$ — **오차 × 입력**, *외적(outer product)*이다
   (열벡터 × 행벡터 → 행렬 하나가 나온다 — $W_2$와 같은 모양)
3. $\dfrac{\partial L}{\partial h} = W_2^\top \delta_2$ — 오차를 거꾸로 사상한 것
4. $\dfrac{\partial L}{\partial z} = W_2^\top \delta_2 \odot \mathbb{1}[z > 0]$ — ReLU의
   그래디언트는 마스크 (이것이 $\delta_1$)
5. $\dfrac{\partial L}{\partial W_1} = \delta_1\, x^\top$

**이제 실제 숫자로** — [[02-foundations/neural-network-basics|0.7 §2]]와 *같은* 신경망이라
새로 세팅할 것이 없다: $W_1 = \begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$,
$W_2 = \begin{pmatrix}1&-1&0.5\end{pmatrix}$, $x = (1,2)$. 그 페이지의 순전파 결과가
$z = (1,2,3)$, $h = (1,2,3)$, $\hat y = 0.5$였다. 정답이 $y = 1$이라 하면
$L = \tfrac12(0.5-1)^2 = 0.125$. 역전파는 위 단계마다 한 줄씩:

| 단계 | 식 | 숫자 |
|---|---|---|
| 1 | $\delta_2 = \hat y - y$ | $0.5 - 1 = -0.5$ |
| 2 | $\partial L/\partial W_2 = \delta_2 h^\top$ | $-0.5\,(1,2,3) = (-0.5,\,-1,\,-1.5)$ |
| 3 | $\partial L/\partial h = W_2^\top\delta_2$ | $-0.5\,(1,-1,0.5) = (-0.5,\,0.5,\,-0.25)$ |
| 4 | $\delta_1 = \partial L/\partial h \odot \mathbb{1}[z>0]$ | $z>0$이라 마스크가 $(1,1,1)$, 따라서 $\delta_1 = (-0.5,\,0.5,\,-0.25)$ |
| 5 | $\partial L/\partial W_1 = \delta_1 x^\top$ | $\begin{pmatrix}-0.5&-1\\0.5&1\\-0.25&-0.5\end{pmatrix}$ |

눈여겨볼 것 셋, 그리고 이 셋은 앞으로 읽을 모든 신경망에 그대로 적용된다:
- **부호가 무엇을 할지 말해준다.** $\delta_2 = -0.5$가 음수인 이유는 예측이 *너무 낮았기*
  때문이다. 경사 하강은 그래디언트를 빼므로, 양의 활성값을 받는 가중치는 전부 **올라간다**.
  산수가 당연한 일을 하고 있다.
- **활성값이 클수록 그래디언트가 크다.** 2단계에서 세 번째 가중치가 $-1.5$를 받고 첫 번째가
  $-0.5$를 받는 이유는 오직 $h_3 = 3$이 가장 크게 말했기 때문이다. 책임이 발언량에 비례해
  배분된다.
- **모양은 변수와 일치한다.** $\partial L/\partial W_1$이 $3\times2$로 나왔고, 이는 정확히
  $W_1$의 모양이다. 그렇지 않다면 버그다 — 예외 없다.

위의 각 단계가 곧 VJP 하나다: 3단계 $W_2^\top\delta_2$는 층의 야코비안-전치를 들어온
$\delta$에 적용한 것 — §2가 추상적으로 말한 것을 방금 손으로 한 셈이다. 모든 깊은
네트워크의 backward가 이 패턴의 반복이다: *델타는 전치를 타고 뒤로 흐르고, 가중치
그래디언트는 델타와 캐시된 활성값의 외적이다.* 차원 검산: 각 그래디언트는 그
변수와 같은 모양이다 — 세상에서 가장 빠른 버그 검출기.

<svg viewBox="0 0 560 175" style="max-width:100%;height:auto" role="img" aria-label="2층 신경망의 순전파와 역전파">
  <defs><marker id="bpF" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="20" y="52" width="62" height="34" rx="4"/><rect x="140" y="52" width="62" height="34" rx="4"/>
    <rect x="260" y="52" width="72" height="34" rx="4"/><rect x="380" y="52" width="62" height="34" rx="4"/>
    <rect x="490" y="52" width="52" height="34" rx="4"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="51" y="74">x</text><text x="171" y="74">z = W₁x</text><text x="296" y="74">h = ReLU(z)</text><text x="411" y="74">ŷ = W₂h</text><text x="516" y="74">L</text>
  </g>
  <g stroke="currentColor" stroke-width="1.5" marker-end="url(#bpF)">
    <line x1="82" y1="62" x2="138" y2="62"/><line x1="202" y1="62" x2="258" y2="62"/>
    <line x1="332" y1="62" x2="378" y2="62"/><line x1="442" y1="62" x2="488" y2="62"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" marker-end="url(#bpF)" stroke-dasharray="5 3" opacity="0.85">
    <line x1="488" y1="78" x2="444" y2="78"/><line x1="378" y1="78" x2="334" y2="78"/>
    <line x1="258" y1="78" x2="204" y2="78"/><line x1="138" y1="78" x2="84" y2="78"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">
    <text x="466" y="102">δ₂ = ŷ − y</text><text x="356" y="102">W₂ᵀδ₂</text><text x="231" y="102">⊙ 1[z&gt;0] = δ₁</text><text x="111" y="102">W₁ᵀδ₁</text>
    <text x="411" y="128">∂L/∂W₂ = δ₂hᵀ</text><text x="171" y="128">∂L/∂W₁ = δ₁xᵀ</text>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="20" y="34">순전파 →</text><text x="20" y="160" opacity="0.85">← 역전파(점선): 델타는 전치를 타고 흐르고, 가중치 그래디언트는 외적이다</text>
  </g>
</svg>



### 4. 고전 층들의 그래디언트

- **Softmax + 교차 엔트로피** — 이 분야에서 가장 깔끔한 결과이고, 지나간 주제가 *아니다*:
  지금도 모든 LLM이 이것으로 학습된다(다음 토큰 예측 = 어휘 전체에 대한 softmax 하나를
  교차 엔트로피로 채점하는 것). 모든 분류 헤드가 이것이고, softmax는 어텐션 내부의 연산
  그 자체다([[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]).
  로봇 정책도 행동을 토큰으로 이산화하면 이것을 쓴다
  ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]]은 각 행동 차원을 256개 구간으로 나눠 제어를
  분류 문제로 만든다). 알아둘 예외: 출력이 연속값인 정책 — 회귀 헤드와
  [[01-canonical-papers/notes/4-vla/diffusion-policy|디퓨전]]·플로우 매칭 정책 — 은 대신
  제곱 오차로 학습한다.
  로짓 $z$, $p = \text{softmax}(z)$, 원-핫 정답 $y$일 때:
  $\dfrac{\partial L}{\partial z} = p - y$ — *예측에서 정답을 뺀 것*, 그게 전부다.
  (유도: $L = -\log p_c$; $\partial \log p_c/\partial z_j = \mathbb{1}[j=c] - p_j$.)
  실무에서는 지수가 넘치지 않도록 log-sum-exp를 거쳐 계산한다 —
  [[02-foundations/engineering-math|0.5 §6]]에 유도해 두었다.
- **ReLU**: 마스크 그래디언트 — 싸고, 포화하지 않는다; 시그모이드를 이긴 이유다
  ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]). 죽은 유닛 = 영원히 0인 마스크.
- **시그모이드** $\sigma' = \sigma(1-\sigma) \le 1/4$: 포화 층 하나가 역방향 신호에 0.25
  이하를 곱한다 — 시그모이드 도함수만 따져도 포화 층 열 개면 그래디언트가 대략 백만 배
  준다(실제 그래디언트에는 가중치 야코비안도 함께 곱해진다). 이 부등식 하나가 구조
  설계사(史) 10년을 설명한다.

### 5. 구조를 만든 병리들

- **그래디언트 소실**: 노름 < 1인 야코비안들의 곱은 깊이/시간에 지수적으로 붕괴.
  역사 순서의 처방:
  - [[01-canonical-papers/notes/1-foundations/lstm|LSTM]]: 가중치가 정확히 1.0인 자기 연결 — 곱이 더는
    줄지 않는 오차 회전목마.
  - [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]: 활성값을 재정규화해 야코비안의
    스케일을 유지 (조건수 개선) — 여러 제안된 설명 중 하나로, BatchNorm이 *왜* 통하는지는
    아직 논쟁 중이다 (노트 참고).
  - [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]:
    $\partial(x + F(x))/\partial x = I + \partial F/\partial x$ — 항등 항이 감쇠 없는
    직접 경로를 제공한다 — 소실을 *완화*하는 것이지(경로가 존재한다), 전체 그래디언트가
    절대 줄지 않음을 보장하는 것은 아니다.
- **그래디언트 폭발**: 노름 > 1 — gradient clipping($\|g\|$를 상한으로 재스케일)으로
  처치, RNN/LLM 학습의 표준.
- **Stop-gradient** $\text{sg}[\cdot]$: 그래프를 의도적으로 자르기. reparameterization
  ([[01-canonical-papers/notes/6-diffusion/vae|VAE]])은 샘플링을 미분 경로 *밖으로* 옮기고, EMA
  교사([[01-canonical-papers/notes/2-computer-vision/dino|DINO]])와 RL 타깃 네트워크는 설계상 그래디언트를 받지
  않는다. 논문 그림의 점선 화살표는 *대개* stop-gradient지만, 보조 경로나 추론 전용
  경로를 뜻하기도 하므로 반드시 범례를 확인하라.

### 6. 구현자의 눈으로 수식 읽기

- 손실의 모든 $E[\cdot]$는 미니배치 평균이 된다. 딥러닝에서는 통과해 미분할 수 없는
  기댓값을 대개 하한([[02-foundations/information-theory|ELBO]]), 몬테카를로 추정, 또는
  트릭(reparameterization;
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

> [!tip]- 스스로 점검 정답 · Answers
> 1. 1단계가 $\delta_2 = p - y$(softmax+CE의 결과)로 바뀌고 나머지 패턴은 동일하다.
> 2. 합의 미분 = 미분의 합: $I + \partial F/\partial x$ — 항등 항 덕분에 역방향 신호가 아무리 깊어도 감쇠 없는 경로를 하나 갖는다.
> 3. 순방향 모드는 입력 방향 하나당 전체 패스 한 번 — 7B 파라미터면 패스 7B번이 필요해 불가능; 역방향은 스칼라 손실(출력 1개) 기준 한 번이면 된다.
> 4. 샘플링은 미분 불가능한 확률적 분기다; $z = \mu + \sigma\epsilon$으로 쓰면 무작위성이 외부 입력 $\epsilon$으로 밀려나 $\mu, \sigma$에 그래디언트가 흐른다.
