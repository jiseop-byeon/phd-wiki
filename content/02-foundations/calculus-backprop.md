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

*Stands on [[02-foundations/linear-algebra|1. Linear Algebra]]. Differentiating a stack of those maps is the whole of backpropagation.
Optimization and RL Basics both come back here for their gradients.*

The one algorithm every deep learning paper assumes silently: reverse-mode automatic
differentiation. Course-depth treatment: from Taylor expansion to a fully worked backprop
example, plus the gradient pathologies that shaped architecture history.

> [!note] First pass · 처음이라면
> Read §1, then §3 — do the two-layer example by hand, it is the whole page in one calculation — then §6. §4 and §5 are for when you are reading an architecture paper and want to know why it is shaped that way.

### 1. Derivatives as local linear models

- **Taylor expansion** is the foundation of all of optimization:
  $$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12 \delta^\top H \delta$$
  ($H$ is the **Hessian** — the matrix of second derivatives $H_{ij}=\partial^2 f/\partial x_i \partial x_j$,
  the multivariable version of $f''$.) Gradient descent trusts the first-order term;
  Newton's method trusts the second ([[02-foundations/optimization|optimization]]).
  - **What kind of thing it is.** A polynomial model of a smooth function $f:\mathbb{R}^n\to\mathbb{R}$, built at one point and trusted only for small steps. Here $x\in\mathbb{R}^n$ is the current point, $\delta\in\mathbb{R}^n$ the proposed step, and $^\top$ turns the column $\nabla f(x)$ into a row so that the product is a single number.
  - **Its three terms, each named.** The **value** $f(x)$ is zeroth order. The **slope term** $\nabla f(x)^\top\delta$ is first order: linear in $\delta$. The **curvature term** $\tfrac12\delta^\top H\delta$ is second order: quadratic in $\delta$. Every omitted term shrinks at least like $\lVert\delta\rVert^3$, so the model is accurate only while the step is small.
  - **Worked, with numbers.** Take $f(x_1,x_2)=x_1^2x_2$ at $x=(1,2)$ with step $\delta=(0.1,\,0.1)$. Then $f(x)=2$, $\nabla f=(2x_1x_2,\;x_1^2)=(4,1)$ and $H=\begin{pmatrix}2x_2&2x_1\\2x_1&0\end{pmatrix}=\begin{pmatrix}4&2\\2&0\end{pmatrix}$. First order gives $2+0.4+0.1=2.5$. The curvature term adds $\tfrac12(0.04+0.04+0)=0.04$, giving $2.54$. The true value is $f(1.1,\,2.1)=2.541$, and the missing $0.001$ is exactly the third-order term $\delta_1^2\delta_2$.
- **Hessian**, stated completely. For a twice-differentiable $f:\mathbb{R}^n\to\mathbb{R}$ it is the $n\times n$ matrix of every second partial derivative:
  $$H(x)_{ij} = \frac{\partial^2 f}{\partial x_i\,\partial x_j}(x)$$
  so entry $(i,j)$ says how the slope along $x_i$ changes as you move along $x_j$. Two properties carry all its uses. It is **symmetric**, $H_{ij}=H_{ji}$, whenever those second partials are continuous (Schwarz's theorem); in the example $H_{12}=H_{21}=2$. And $\delta^\top H\delta$ is the **curvature along the direction $\delta$**: positive means the surface bends up that way. Why it matters: the signs of its eigenvalues ([[02-foundations/linear-algebra|1. Linear Algebra §3]]) separate minima from saddles, and $H\succeq0$ everywhere is exactly convexity ([[02-foundations/optimization|4. Optimization §2]]).
- $\partial L/\partial w$ answers: "nudge $w$, how much does $L$ move?" Training =
  computing millions of these sensitivities and stepping against them. (The partial derivative itself is defined in [[02-foundations/engineering-math|0.5 §1]].)
- **Gradient** $\nabla_w L$: vector of all sensitivities; points uphill; perpendicular to
  level sets. Stated completely, for $f:\mathbb{R}^n\to\mathbb{R}$ it is the column vector of the $n$ partial derivatives,
  $$\nabla f(x) = \Big(\frac{\partial f}{\partial x_1},\ \ldots,\ \frac{\partial f}{\partial x_n}\Big)^\top$$
  Because it collects every partial, it answers the **directional derivative**: the rate of change along a unit vector $u$ is $\nabla f(x)^\top u$. Both geometric facts follow from that one product.
  - **Points uphill.** $\nabla f^\top u = \lVert\nabla f\rVert\cos\theta$ is largest when $u$ is parallel to $\nabla f$, so the gradient is the steepest-ascent direction and its length $\lVert\nabla f\rVert$ is that steepest rate. In the Taylor example, moving along $x_1$ changes $f$ at rate $4$, while moving along $\nabla f=(4,1)$ changes it at rate $\sqrt{17}\approx4.12$.
  - **Perpendicular to level sets.** Along a level set $f$ does not change, so every tangent direction $u$ has $\nabla f^\top u=0$. For $f=x_1^2+x_2^2$ at $(3,4)$ the gradient is $(6,8)$, the circle's tangent is $(-4,3)$, and $6(-4)+8(3)=0$ ✓.
- **Jacobian** $J_{ij} = \partial y_i/\partial x_j$: the sensitivity matrix of
  a vector function — the object that *chains* under composition. (Robotics uses the same
  word for the same object: joint velocities → end-effector velocities,
  [[04-robotics/index|Modern Robotics]].) Stated completely, for $y=f(x)$ with $f:\mathbb{R}^n\to\mathbb{R}^m$ it is the $m\times n$ matrix
  $$J(x) = \begin{pmatrix}\partial y_1/\partial x_1 & \cdots & \partial y_1/\partial x_n\\ \vdots & & \vdots\\ \partial y_m/\partial x_1 & \cdots & \partial y_m/\partial x_n\end{pmatrix}$$
  so it has one row per output and one column per input, and its defining property is the first-order model $f(x+\delta)\approx f(x)+J(x)\,\delta$.
  - **Row $i$** is the gradient of output $y_i$, laid on its side. **Column $j$** is how every output responds to input $x_j$ alone. For a scalar function ($m=1$) the Jacobian is the single row $\nabla f^\top$.
  - **Worked.** $f(x_1,x_2)=(x_1x_2,\; x_1+x_2^2)$ at $x=(1,2)$ gives $f=(2,5)$ and $J=\begin{pmatrix}x_2&x_1\\1&2x_2\end{pmatrix}=\begin{pmatrix}2&1\\1&4\end{pmatrix}$. Nudge $x_1$ by $0.01$: the outputs move by $(0.02,\,0.01)$, which is $0.01$ times the first column, as the model predicts.

**A derivative predicts a change; it is not the changed value.** In the Taylor expression, f(x) is the current output, δ is the proposed input change, the gradient term predicts its first-order effect, and the Hessian term corrects for curvature. If δ is too large, omitted terms can matter. That is why knowing a downhill direction does not tell you how far to step.

For a vector output, read the Jacobian one column at a time: perturb one input while holding the rest fixed, then collect how every output responds. For a scalar loss, collect one sensitivity per parameter into the gradient. The symbols are different shapes of the same local question. A derivative can be negative even when the loss itself is positive; the sign describes direction of change, not the value's sign.

> [!question] Pause and explain · 잠깐 설명해 보기
> If a parameter's derivative is positive, which small change does gradient descent propose? Decrease the parameter, because the local model predicts that increasing it would raise the loss. This is a local prediction; the step size and curvature determine whether the actual update behaves as predicted.

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
- **The multivariable chain rule, stated completely.** The scalar rule of [[02-foundations/engineering-math|0.5 §1]] generalises in two equivalent forms. For a composition $h(x)=g(f(x))$ with $f:\mathbb{R}^n\to\mathbb{R}^m$ and $g:\mathbb{R}^m\to\mathbb{R}^k$, the Jacobians multiply:
  $$J_{g\circ f}(x) = J_g\big(f(x)\big)\,J_f(x)$$
  so the $k\times m$ matrix of the outer map, evaluated where the inner map landed, times the $m\times n$ matrix of the inner map gives the $k\times n$ Jacobian of the whole. Written entry by entry for a scalar $L$ that depends on $x_j$ through intermediates $y_1,\ldots,y_m$, the same rule is a **sum over every path**:
  $$\frac{\partial L}{\partial x_j} = \sum_{i=1}^{m}\frac{\partial L}{\partial y_i}\,\frac{\partial y_i}{\partial x_j}$$
  because a nudge to $x_j$ reaches $L$ through each $y_i$ separately and the first-order effects add. Stacking that sum over $j$ is exactly $\nabla_x L = J^\top\,\nabla_y L$.
  - **Worked.** Use the Jacobian example from §1, $y=(x_1x_2,\;x_1+x_2^2)$ at $x=(1,2)$, so $y=(2,5)$, and let $L=y_1y_2$. Then $\nabla_y L=(y_2,\,y_1)=(5,2)$ and $\nabla_x L=J^\top(5,2)=\begin{pmatrix}2&1\\1&4\end{pmatrix}(5,2)=(12,\,13)$. A central finite difference on $L=x_1x_2(x_1+x_2^2)$ returns $(12.000,\,13.000)$ ✓.
- Two evaluation orders for that product:
  - **Forward mode**: propagate $\partial/\partial x_i$ input-side first — one pass *per input*.
  - **Reverse mode**: propagate $\partial L/\partial(\cdot)$ output-side first — one pass *per output*.
  - **Stated as formulas.** Forward mode carries a **tangent** $\dot x$ (a chosen input direction) through each primitive $y=f(x)$ by the **Jacobian-vector product** $\dot y = J\dot x$. Seeding $\dot x=e_j$, the $j$-th unit vector, returns column $j$ of the Jacobian, so a full $n$-input Jacobian needs $n$ passes. Reverse mode carries an **adjoint** $\bar y=\partial L/\partial y$ backward by the **vector-Jacobian product** $\bar x = J^\top\bar y$. Seeding $\bar y=e_i$ returns row $i$, so an $m$-output Jacobian needs $m$ passes. With the §1 Jacobian: forward with $\dot x=(1,0)$ gives $(2,1)$, the first column; reverse with $\bar y=(0,1)$ gives $(1,4)$, the second row.
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
<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="forward mode sweeping left to right once per parameter against reverse mode sweeping right to left once for the single loss">
  <defs><marker id="cbA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1">
    <rect x="70" y="38" width="52" height="26" rx="3"/><rect x="160" y="38" width="52" height="26" rx="3"/><rect x="250" y="38" width="52" height="26" rx="3"/><rect x="340" y="38" width="52" height="26" rx="3"/><circle cx="446" cy="51" r="14"/>
  </g>
  <g fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1">
    <rect x="70" y="108" width="52" height="26" rx="3"/><rect x="160" y="108" width="52" height="26" rx="3"/><rect x="250" y="108" width="52" height="26" rx="3"/><rect x="340" y="108" width="52" height="26" rx="3"/><circle cx="446" cy="121" r="14"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#cbA)" opacity="0.85">
    <line x1="124" y1="51" x2="158" y2="51"/><line x1="214" y1="51" x2="248" y2="51"/><line x1="304" y1="51" x2="338" y2="51"/><line x1="394" y1="51" x2="428" y2="51"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#cbA)" opacity="0.85">
    <line x1="160" y1="121" x2="124" y2="121"/><line x1="250" y1="121" x2="214" y2="121"/><line x1="340" y1="121" x2="304" y2="121"/><line x1="430" y1="121" x2="394" y2="121"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="24" y="30">forward mode</text>
    <text x="24" y="100">reverse mode</text>
    <text x="470" y="56">&#215; 10&#8311; sweeps</text>
    <text x="470" y="126">&#215; 1 sweep</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8">
    <text x="104" y="30">push &#8706;/&#8706;&#952;&#7522; from the inputs &#8212; one sweep per parameter</text>
    <text x="104" y="100">pull &#8706;L/&#8706;(&#183;) from the output &#8212; one sweep per output</text>
    <text x="70" y="84">10&#8311; parameters</text>
    <text x="470" y="154">1 scalar loss</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="190">The asymmetry is not a trick; it falls out of the shape of the problem &#8212; many inputs, one</text>
    <text x="24" y="206">output. A backward pass costs two to three forward passes, so the real gap is about seven</text>
    <text x="24" y="222">orders of magnitude, and training large models is possible for that reason alone. Need the</text>
    <text x="24" y="238">sensitivity of many outputs to one input and the ordering flips.</text>
  </g>
</svg>

  $v \mapsto J^\top v$; the framework composes them along the recorded graph.
  Cost ≈ 2–3× a forward pass; memory ≈ stored activations (hence gradient checkpointing:
  recompute instead of store).
  - **VJP, stated completely.** For a primitive $y=f(x)$ with Jacobian $J$, its VJP is the linear map from an output-sized sensitivity $v=\partial L/\partial y$ to the input-sized sensitivity $J^\top v=\partial L/\partial x$. A primitive supplies it as a rule and never builds $J$, which for a layer with $10^7$ inputs and outputs would have $10^{14}$ entries. Two rules you already use in §3: for a linear layer $y=Wx$ the VJP is $v\mapsto W^\top v$, and for an elementwise ReLU it is $v\mapsto v\odot\mathbb{1}[z>0]$.
  - **Gradient checkpointing, stated completely.** A memory-for-compute trade with two parts: during the forward pass store activations only at chosen **checkpoints**, and during the backward pass **recompute** each segment's activations from its checkpoint just before that segment's VJPs need them. The cost is roughly one extra forward pass; with checkpoints every $\sqrt{n}$ layers of an $n$-layer network, activation memory falls from $O(n)$ to $O(\sqrt{n})$ (Chen et al., "Training Deep Nets with Sublinear Memory Cost," 2016).

**Backward does not mean undoing the forward pass.** The forward pass carries values; the backward pass carries sensitivity of the final loss to those values. At each operation, multiply the arriving sensitivity by that operation's local derivative. If a value affects the loss through several branches, add the contributions from those branches. Shared use creates a sum of effects, not permission to count only the last branch visited.

The transpose in Jᵀv is therefore not an inverse. You can backpropagate through a rectangular or information-losing map because you are asking how its output loss would change with its input, not reconstructing the input from the output. Keeping this distinction clear connects backpropagation to the Jacobian's mechanical use without confusing either with inverse kinematics.

**Try the existing forward-pass example again.** Label each intermediate with its shape, then place one loss-sensitivity variable beside it. Walk backward and check that each sensitivity has the same shape as the value it belongs to. A shape mismatch catches many mistakes before any numerical calculation is needed.

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

**Three pieces of notation in those steps, each defined.** (The loss $L=\tfrac12\|\hat y-y\|^2$ is the squared-error loss of [[02-foundations/neural-network-basics|0.7 §3]].)
- **Outer product.** For a column $u\in\mathbb{R}^m$ and a column $v\in\mathbb{R}^n$ it is the $m\times n$ matrix
  $$(uv^\top)_{ij} = u_i\,v_j$$
  so every entry is one component of $u$ times one component of $v$. It has rank 1 (every row is a multiple of $v^\top$). Example: $u=(1,2)$, $v=(3,4,5)$ gives $\begin{pmatrix}3&4&5\\6&8&10\end{pmatrix}$. Contrast the **inner product** $u^\top v$, a single number that needs equal lengths. Why it appears: $\partial L/\partial W_{ij}=\delta_i\,h_j$, because weight $W_{ij}$ multiplies input $h_j$ on its way to output $i$.
- **Hadamard (elementwise) product** $\odot$. For two vectors or matrices of the same shape,
  $$(a\odot b)_i = a_i\,b_i$$
  so it multiplies matching entries and keeps the shape. Example: $(-0.5,\,0.5,\,-0.25)\odot(1,0,1)=(-0.5,\,0,\,-0.25)$. It is not the matrix product: $a\odot b$ needs equal shapes, $ab$ needs matching inner dimensions.
- **Indicator** $\mathbb{1}[\cdot]$. It returns $1$ when the condition inside is true and $0$ otherwise, applied entry by entry to a vector. $\mathbb{1}[z>0]$ is ReLU's derivative: slope $1$ where $z>0$, slope $0$ where $z<0$. At exactly $z=0$ ReLU has no derivative, and frameworks such as PyTorch simply use $0$ there.

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
- **The sign says what to do — locally.** $\delta_2 = -0.5$ is negative because the
  prediction was *too low*, so all three output weights in step 2 increase under gradient
  descent. Earlier layers also inherit downstream signs: the second row of $W_1$ decreases
  here because its path through $W_2$ is negative. A low prediction does not mean every
  weight in the network must increase.
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
  vocabulary, scored by cross-entropy — the loss $-\log p_{\text{true}}$, derived in [[02-foundations/information-theory|5. Information Theory §2]]), how every classification head works, and softmax is
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
  - **The four objects, each defined.** **Logits** $z\in\mathbb{R}^K$ are the network's raw, unnormalised scores, one per class, any real numbers. **Softmax** is the map from $\mathbb{R}^K$ to probability vectors,
    $$p_j = \text{softmax}(z)_j = \frac{e^{z_j}}{\sum_{k=1}^{K} e^{z_k}}$$
    so every $p_j$ is positive (an exponential is), the $p_j$ sum to $1$ (the denominator is their common total), and the order of the scores is kept. Adding one constant to every logit changes nothing, since the factor $e^{c}$ cancels. A **one-hot** target $y$ has $y_c=1$ at the true class $c$ and $0$ elsewhere. **Cross-entropy** against it is $L=-\sum_j y_j\log p_j=-\log p_c$, the general definition being in [[02-foundations/information-theory|5. Information Theory §2]].
  - **Worked.** $z=(2,1,0)$ with true class $c=1$ (the first). Softmax gives $p=(0.665,\,0.245,\,0.090)$; $z+10=(12,11,10)$ gives the same $p$. The loss is $-\log 0.665=0.408$, and the gradient is $p-y=(-0.335,\,0.245,\,0.090)$: push the true logit up, the other two down, each in proportion to the probability it wrongly holds.
  Computed in practice through log-sum-exp so the exponentials cannot overflow — derived in
  [[02-foundations/engineering-math|0.5 §6]]. The same loss coded in NumPy, with the $1/N$ of a
  mean loss and a finite-difference gradient check, is [[02-foundations/algorithms/robotics-ai-problems|11.8 §9]].
- **ReLU**: mask gradient — cheap, non-saturating; the reason it displaced saturating units
  ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] compared it against tanh and reported several-times-faster training). Dead units = permanently zero mask.
  Stated with its formula: $\text{ReLU}(z)=\max(0,z)$, whose derivative is $\mathbb{1}[z>0]$ (§3). It is **non-saturating** because the slope stays exactly $1$ for every positive input, however large. A **dead unit** is one whose pre-activation $z=w^\top x+b$ is negative for every input in the data: its mask is always $0$, so $w$ and $b$ receive zero gradient and can never move back. Example: $w=1$, $b=-10$ and inputs $x\in[0,1]$ give $z\le-9$ on every example.
- **Sigmoid** $\sigma' = \sigma(1-\sigma) \le 1/4$: stacked sigmoids shrink the gradient geometrically.
  Stated with its formula, the sigmoid squashes any real $z$ into $(0,1)$:
  $$\sigma(z) = \frac{1}{1+e^{-z}}$$
  so $\sigma(0)=0.5$, $\sigma(4)=0.982$ and $\sigma(-4)=0.018$. Differentiating gives $\sigma'(z)=e^{-z}/(1+e^{-z})^2$, and splitting that fraction as $\frac{1}{1+e^{-z}}\cdot\frac{e^{-z}}{1+e^{-z}}$ shows it equals $\sigma(1-\sigma)$. A unit is **saturated** when $|z|$ is large enough that $\sigma$ sits near $0$ or $1$, which makes $\sigma'$ near $0$.
  The bound holds because $\sigma(1-\sigma)$ is a downward parabola in $\sigma\in(0,1)$, highest at $\sigma=1/2$ (that is, $z=0$), where it equals $1/2\cdot1/2=1/4$.
  Every sigmoid layer multiplies the backward signal by at most 0.25, and 0.25 is the *best* case, at $z=0$.
  From the sigmoid derivatives alone, ten layers attenuate gradients at least a million-fold: $0.25^{10} \approx 9.5\times10^{-7}$.
  Once units saturate it is far worse, since $\sigma'(4) \approx 0.018$. The full gradient also carries weight Jacobians. This single inequality explains a decade of architecture history.

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
  - **Stated with the formula.** For a chain of $T$ layers or time steps $h_t=f_t(h_{t-1})$ with Jacobians $J_t=\partial h_t/\partial h_{t-1}$, the chain rule of §2 gives
    $$\frac{\partial L}{\partial h_0} = J_1^\top J_2^\top\cdots J_T^\top\,\frac{\partial L}{\partial h_T}$$
    so the signal reaching the first layer has passed through $T$ matrices, and its size is bounded by $\big\lVert\partial L/\partial h_0\big\rVert\le\prod_t\lVert J_t\rVert\,\big\lVert\partial L/\partial h_T\big\rVert$. **Vanishing** is the case where every $\lVert J_t\rVert\le\rho<1$, which forces decay at least as fast as $\rho^{T}$. With scalar Jacobians of $0.9$ over $50$ steps the gradient is multiplied by $0.9^{50}=0.0052$. Consequence: early layers, or early time steps, stop learning while later ones still do.
- **Exploding gradients**: norms > 1 — treated with gradient clipping (rescale $\|g\|$ to a
  ceiling), standard in RNN/LLM training.
  - **Stated with the formula.** The same product with factors larger than $1$ can grow like $\rho^{T}$: scalar Jacobians of $1.1$ over $50$ steps multiply the gradient by $1.1^{50}=117$, and one such step can throw the weights far outside the region where the loss was sensible. **Clipping by norm**, with ceiling $c$, rescales the gradient $g$ as
    $$g \leftarrow g\cdot\min\!\Big(1,\ \frac{c}{\lVert g\rVert}\Big)$$
    so a gradient already shorter than $c$ is untouched and a longer one keeps its direction but is shortened to length exactly $c$. Example: $g=(3,4)$ has length $5$; with $c=1$ it becomes $(0.6,\,0.8)$.
- **Stop-gradient** $\text{sg}[\cdot]$: deliberately cut the graph. Reparameterization
  ([[01-canonical-papers/notes/6-diffusion/vae|VAE]]) moves sampling *outside* the differentiated path;
  EMA teachers ([[01-canonical-papers/notes/2-computer-vision/dino|DINO]]; EMA = exponential moving average — the teacher's weights are a slowly updated running average of the student's) and RL target networks receive no
  gradient by design. A dashed arrow in a paper figure *often* denotes stop-gradient —
  but it can also mean an auxiliary or inference-only path, so always check the legend.
  - **Stop-gradient, stated completely.** An operator with two rules: in the forward pass it is the identity, $\text{sg}[a]=a$; in the backward pass its derivative is declared zero, $\partial\,\text{sg}[a]/\partial a=0$. So the value is used but no sensitivity flows back through it (`detach()` in PyTorch, `stop_gradient` in JAX). Example: $L=(\text{sg}[a]-b)^2$ at $a=3$, $b=1$ has $L=4$, $\partial L/\partial b=-2(a-b)=-4$, and $\partial L/\partial a=0$, where without the operator it would be $+4$.
  - **Reparameterization, stated completely.** Replace a sample $z\sim\mathcal{N}(\mu,\sigma^2)$ by a deterministic function of the parameters and external noise:
    $$z = \mu + \sigma\,\epsilon,\qquad \epsilon\sim\mathcal{N}(0,1)$$
    because this $z$ has exactly the same distribution, while now $\partial z/\partial\mu=1$ and $\partial z/\partial\sigma=\epsilon$ are ordinary derivatives. Example: $\mu=1$, $\sigma=2$ and a drawn $\epsilon=0.5$ give $z=2$ and $\partial z/\partial\sigma=0.5$. Drawing $z$ directly from $\mathcal{N}(\mu,\sigma^2)$ is the non-example: the draw is not a function of $\mu$ you can differentiate.
  - **EMA teacher, stated completely.** After each student update the teacher's parameters $\theta_T$ move a fraction of the way toward the student's $\theta_S$, with a decay $\tau$ just below $1$:
    $$\theta_T \leftarrow \tau\,\theta_T + (1-\tau)\,\theta_S$$
    so a student value from $k$ steps ago keeps weight $\propto\tau^{k}$, and the teacher gets its values only through this rule, never through a gradient. With $\tau=0.99$ that weight halves every $\ln 0.5/\ln 0.99\approx69$ steps; DINO's schedule starts at $\tau=0.996$, a half-life of about $173$ steps.

### 6. Reading equations like an implementer

- Expectations over training data are commonly estimated by minibatch means; finite sums,
  analytic expectations and dynamic programs can sometimes be evaluated directly. In deep
  learning, intractable or non-reparameterizable expectations are often handled with a bound
  ([[02-foundations/information-theory|ELBO]]), a Monte Carlo estimator, or a gradient-estimation technique
  (reparameterization; likelihood-ratio/policy gradients — [[02-foundations/rl-basics|RL basics]]).
  - **Minibatch estimate, stated completely.** For a training loss that averages per-example losses $\ell_i$ over $N$ examples, the minibatch gradient over a random subset $B$ of size $|B|$ is
    $$\hat g = \frac{1}{|B|}\sum_{i\in B}\nabla\ell_i(\theta)\ \approx\ \frac{1}{N}\sum_{i=1}^{N}\nabla\ell_i(\theta)$$
    and it is **unbiased**: averaged over all possible batches it equals the full gradient, so it is right on average while each draw is noisy. A worked version is in [[02-foundations/optimization|4. Optimization §3]].
- $\arg\max$ is not differentiable; softmax is its smooth stand-in (temperature controls
  the sharpness). Sampling is not differentiable; Gumbel-softmax / straight-through
  estimators fake it. Gumbel-softmax replaces the discrete sample with a smooth, temperature-controlled softmax of noise-perturbed logits; straight-through uses the hard sample in the forward pass but passes the smooth version's gradient backward.
  - **Softmax with temperature.** With temperature $\tau>0$,
    $$p_j = \frac{e^{z_j/\tau}}{\sum_k e^{z_k/\tau}}$$
    so $\tau=1$ is ordinary softmax, a small $\tau$ sharpens toward the one-hot vector of $\arg\max$, and a large $\tau$ flattens toward uniform. For $z=(2,1,0)$: $\tau=1$ gives $(0.665,\,0.245,\,0.090)$, $\tau=0.5$ gives $(0.867,\,0.117,\,0.016)$, and $\tau=0.1$ gives $(0.99995,\,0.00005,\,0.00000)$. $\arg\max$ itself is the non-example: its output jumps between one-hot vectors, so its derivative is zero almost everywhere.
  - **Gumbel-softmax, stated completely.** Three steps. Draw $u_j$ uniformly from $(0,1)$ and form Gumbel noise $g_j=-\log(-\log u_j)$. Then $\arg\max_j(z_j+g_j)$ is an exact sample from $\text{softmax}(z)$ (the Gumbel-max trick). Finally replace that $\arg\max$ by a temperature softmax:
    $$y_j = \frac{e^{(z_j+g_j)/\tau}}{\sum_k e^{(z_k+g_k)/\tau}}$$
    since $y$ is smooth in $z$ and approaches the one-hot sample as $\tau\to0$. Example: $z=(2,1,0)$ with $u=(0.1,\,0.9,\,0.5)$ gives $g=(-0.834,\,2.250,\,0.367)$ and $z+g=(1.166,\,3.250,\,0.367)$, so this draw picks class 2 although class 1 has the larger logit, which is what sampling should sometimes do. At $\tau=1$, $y=(0.105,\,0.847,\,0.047)$; at $\tau=0.5$, $y=(0.015,\,0.982,\,0.003)$.
  - **Straight-through, stated completely.** Use the hard one-hot $y_{\text{hard}}$ in the forward pass and the soft $y$'s gradient in the backward pass, written with the stop-gradient of §5 as
    $$y_{\text{ST}} = y_{\text{hard}} - \text{sg}[y] + y$$
    because the forward value is $y_{\text{hard}}-y+y=y_{\text{hard}}$, while the backward pass sees $\partial y_{\text{ST}}/\partial z=\partial y/\partial z$, the two hard terms contributing nothing. The gradient is therefore biased: it is the gradient of a slightly different, smooth computation.
- Frameworks differentiate *programs*, not formulas: control flow, loops, and in-place ops
  all have gradient semantics — most "my loss doesn't decrease" bugs are graph bugs.

> [!tip] Going deeper · 더 깊이
> For the machinery underneath: Baydin, Pearlmutter, Radul and Siskind, "Automatic Differentiation in Machine Learning: a Survey," *JMLR* 18(153), 2018 — the paper that separates forward and reverse mode carefully. The [*Deep Learning* book](https://www.deeplearningbook.org/) ch.6 treats backprop as an algorithm.

### Self-check

1. Redo the worked example with a $K$-class output ($W_2 \in \mathbb{R}^{K\times 3}$) and softmax-CE in place of MSE. What changes? (Softmax over the example's single scalar output is always 1, so a one-output softmax would give zero gradient.)
2. Show $\partial(x + F(x))/\partial x = I + J_F$ and explain why depth no longer forces the gradient to decay.
3. Why does forward-mode autodiff cost one pass *per input parameter*, and why is that
   fatal for a 7B-parameter model?
4. In the [[01-canonical-papers/notes/6-diffusion/vae|VAE]], why can't you backprop through
   $z \sim \mathcal{N}(\mu, \sigma^2)$ directly, and how does $z = \mu + \sigma\epsilon$ fix it?

> [!tip]- Answers
> 1. $\delta_2$ becomes $p - y$, a $K$-vector (the softmax + cross-entropy gradient), instead of the scalar $\hat y - y$. Steps 2–5 keep the same formulas with $W_2$ now $K\times 3$ — the backward pattern does not care which loss produced the incoming delta.
> 2. The derivative of a sum is the sum of derivatives: $\partial(x + F(x))/\partial x = I + \partial F/\partial x = I + J_F$. The identity term gives the backward signal one path that is never multiplied down, so depth stops *forcing* decay — it mitigates vanishing rather than guaranteeing the total gradient never shrinks.
> 3. Forward mode propagates sensitivities with respect to *one* input direction per pass, so covering 7B parameters would need 7B passes. Reverse mode propagates from a *scalar* loss, so a single backward pass yields every parameter gradient — the asymmetry is why training is possible at all.
> 4. Sampling is a stochastic branch with no derivative with respect to $\mu, \sigma$. Rewriting $z = \mu + \sigma\epsilon$ with $\epsilon \sim \mathcal{N}(0,1)$ pushes the randomness into an *external input*, leaving a deterministic, differentiable function of $\mu$ and $\sigma$ — gradients now flow to the encoder.

## 한국어

*[[02-foundations/linear-algebra|1. 선형대수]] 위에 선다. 그 사상들의 적층을 미분하는 것이 역전파의 전부다.
최적화와 RL 기초가 그래디언트를 가지러 이 페이지로 돌아온다.*

모든 딥러닝 논문이 말없이 전제하는 단 하나의 알고리즘: 역방향 자동 미분. 교재 수준의
서술: 테일러 전개에서 손으로 푸는 역전파 예제까지, 그리고 구조 설계의 역사를 만든
그래디언트 병리들.

> [!note] 처음이라면 · First pass
> 먼저 §1 다음 §3 — 2층 예제를 손으로 풀어라, 그 계산 하나가 이 페이지의 전부다 — 그다음 §6. §4·§5는 구조 논문을 읽으며 왜 그 모양인지 알고 싶어질 때다.

### 1. 국소 선형 모델로서의 미분

- **테일러 전개**가 최적화 전체의 토대다:
  $$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12 \delta^\top H \delta$$
  ($H$는 **헤시안** — 2차 도함수의 행렬 $H_{ij}=\partial^2 f/\partial x_i \partial x_j$,
  $f''$의 다변수 버전이다.) 경사 하강은 1차 항을, 뉴턴법은 2차 항까지 믿는다
  ([[02-foundations/optimization|최적화]]).
  - **어떤 종류의 대상인가.** 매끄러운 함수 $f:\mathbb{R}^n\to\mathbb{R}$를 한 점에서 만든 다항식 모델이고, 작은 스텝에서만 믿는다. $x\in\mathbb{R}^n$은 현재 점, $\delta\in\mathbb{R}^n$은 제안한 스텝, $^\top$은 열벡터 $\nabla f(x)$를 행벡터로 눕혀 곱이 숫자 하나가 되게 한다.
  - **세 항, 각각의 이름.** **값** $f(x)$는 0차 항이다. **기울기 항** $\nabla f(x)^\top\delta$는 1차 항으로 $\delta$에 선형이다. **곡률 항** $\tfrac12\delta^\top H\delta$는 2차 항으로 $\delta$에 이차다. 생략한 항은 모두 적어도 $\lVert\delta\rVert^3$처럼 줄어들므로, 모델은 스텝이 작을 때만 정확하다.
  - **숫자로 계산.** $f(x_1,x_2)=x_1^2x_2$를 $x=(1,2)$에서 스텝 $\delta=(0.1,\,0.1)$로 본다. $f(x)=2$, $\nabla f=(2x_1x_2,\;x_1^2)=(4,1)$, $H=\begin{pmatrix}2x_2&2x_1\\2x_1&0\end{pmatrix}=\begin{pmatrix}4&2\\2&0\end{pmatrix}$이다. 1차까지는 $2+0.4+0.1=2.5$. 곡률 항이 $\tfrac12(0.04+0.04+0)=0.04$를 더해 $2.54$가 된다. 참값은 $f(1.1,\,2.1)=2.541$이고, 남은 $0.001$은 정확히 3차 항 $\delta_1^2\delta_2$다.
- **헤시안**의 완전한 정의. 두 번 미분 가능한 $f:\mathbb{R}^n\to\mathbb{R}$에 대해, 모든 2계 편미분을 모은 $n\times n$ 행렬이다:
  $$H(x)_{ij} = \frac{\partial^2 f}{\partial x_i\,\partial x_j}(x)$$
  즉 $(i,j)$ 성분은 $x_j$ 방향으로 움직일 때 $x_i$ 방향 기울기가 얼마나 변하는지다. 쓰임은 두 성질에서 나온다. 2계 편미분이 연속이면 **대칭**이다, $H_{ij}=H_{ji}$(슈바르츠 정리). 위 예제에서도 $H_{12}=H_{21}=2$다. 그리고 $\delta^\top H\delta$는 **방향 $\delta$로의 곡률**이다. 양수면 그 방향으로 표면이 위로 휜다. 중요한 이유: 고유값의 부호([[02-foundations/linear-algebra|1. 선형대수 §3]])가 최소점과 안장점을 가르고, 모든 곳에서 $H\succeq0$인 것이 곧 볼록성이다([[02-foundations/optimization|4. 최적화 §2]]).
- $\partial L/\partial w$의 질문: "$w$를 살짝 밀면 $L$이 얼마나 움직이는가?" 학습 = 이
  민감도 수백만 개를 계산해 반대로 내딛는 일. (편미분 자체의 정의는 [[02-foundations/engineering-math|0.5 §1]].)
- **그래디언트** $\nabla_w L$: 민감도 전체의 벡터; 오르막을 가리키고 등고선에 수직이다.
  완전히 쓰면, $f:\mathbb{R}^n\to\mathbb{R}$의 편미분 $n$개를 세운 열벡터다.
  $$\nabla f(x) = \Big(\frac{\partial f}{\partial x_1},\ \ldots,\ \frac{\partial f}{\partial x_n}\Big)^\top$$
  모든 편미분을 모았기 때문에 **방향 미분**에 답한다: 단위벡터 $u$ 방향의 변화율은 $\nabla f(x)^\top u$다. 두 기하적 사실이 모두 이 곱 하나에서 나온다.
  - **오르막을 가리킨다.** $\nabla f^\top u = \lVert\nabla f\rVert\cos\theta$는 $u$가 $\nabla f$와 평행할 때 가장 크므로, 그래디언트는 가장 가파른 오르막 방향이고 길이 $\lVert\nabla f\rVert$가 그 최대 변화율이다. 테일러 예제에서 $x_1$ 방향 변화율은 $4$, $\nabla f=(4,1)$ 방향 변화율은 $\sqrt{17}\approx4.12$다.
  - **등고선에 수직이다.** 등고선을 따라가면 $f$가 변하지 않으므로 모든 접선 방향 $u$에서 $\nabla f^\top u=0$이다. $f=x_1^2+x_2^2$의 $(3,4)$에서 그래디언트는 $(6,8)$, 원의 접선은 $(-4,3)$이고 $6(-4)+8(3)=0$ ✓.
- **야코비안** $J_{ij} = \partial y_i/\partial x_j$: 벡터 함수의 민감도 행렬 — 합성에서
  *연쇄되는* 대상. (로보틱스도 같은 대상에 같은 이름을 쓴다: 관절 속도 → 말단 속도,
  [[04-robotics/index|Modern Robotics]].) 완전히 쓰면, $f:\mathbb{R}^n\to\mathbb{R}^m$인 $y=f(x)$에 대한 $m\times n$ 행렬이다.
  $$J(x) = \begin{pmatrix}\partial y_1/\partial x_1 & \cdots & \partial y_1/\partial x_n\\ \vdots & & \vdots\\ \partial y_m/\partial x_1 & \cdots & \partial y_m/\partial x_n\end{pmatrix}$$
  그래서 출력마다 행 하나, 입력마다 열 하나이고, 정의하는 성질은 1차 모델 $f(x+\delta)\approx f(x)+J(x)\,\delta$다.
  - **$i$번째 행**은 출력 $y_i$의 그래디언트를 눕힌 것이다. **$j$번째 열**은 입력 $x_j$ 하나에 모든 출력이 어떻게 반응하는지다. 스칼라 함수($m=1$)라면 야코비안은 행 하나 $\nabla f^\top$이다.
  - **계산.** $f(x_1,x_2)=(x_1x_2,\; x_1+x_2^2)$를 $x=(1,2)$에서 보면 $f=(2,5)$이고 $J=\begin{pmatrix}x_2&x_1\\1&2x_2\end{pmatrix}=\begin{pmatrix}2&1\\1&4\end{pmatrix}$다. $x_1$을 $0.01$ 밀면 출력이 $(0.02,\,0.01)$ 움직이는데, 모델이 예측하는 대로 첫 열의 $0.01$배다.

**미분은 변화량을 예측하지 바뀐 값 자체가 아니다.** 테일러 식에서 f(x)는 현재 출력, δ는 제안한 입력 변화, 기울기 항은 그 일차 효과, 헤시안 항은 곡률 보정이다. δ가 크면 생략한 항이 중요해진다. 내려가는 방향을 안다고 얼마나 움직일지까지 아는 것은 아니다.

벡터 출력의 야코비안은 열 하나씩 읽는다. 나머지를 고정하고 입력 하나를 조금 바꾼 뒤 모든 출력의 반응을 모은다. 스칼라 손실에서는 파라미터별 민감도를 기울기 벡터로 모은다. 서로 다른 모양으로 같은 국소 질문을 하는 것이다. 손실이 양수여도 미분은 음수일 수 있다. 미분의 부호는 값의 부호가 아니라 변화 방향이다.

> [!question] 잠깐 설명해 보기 · Pause and explain
> 파라미터의 미분이 양수면 경사하강은 어느 쪽의 작은 변화를 제안하는가? 파라미터를 줄인다. 국소 모델상 늘리면 손실이 올라가기 때문이다. 이는 국소 예측이다. 실제 갱신이 예측대로 움직일지는 보폭과 곡률에 달려 있다.

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
- **다변수 연쇄 법칙의 완전한 형태.** [[02-foundations/engineering-math|0.5 §1]]의 스칼라 법칙은 동치인 두 형태로 일반화된다. $f:\mathbb{R}^n\to\mathbb{R}^m$, $g:\mathbb{R}^m\to\mathbb{R}^k$의 합성 $h(x)=g(f(x))$에서는 야코비안이 곱해진다.
  $$J_{g\circ f}(x) = J_g\big(f(x)\big)\,J_f(x)$$
  즉 안쪽 사상이 도착한 점에서 계산한 바깥 사상의 $k\times m$ 행렬에 안쪽 사상의 $m\times n$ 행렬을 곱하면 전체의 $k\times n$ 야코비안이 된다. 스칼라 $L$이 중간값 $y_1,\ldots,y_m$을 거쳐 $x_j$에 의존할 때 성분별로 쓰면, 같은 법칙이 **모든 경로에 대한 합**이다.
  $$\frac{\partial L}{\partial x_j} = \sum_{i=1}^{m}\frac{\partial L}{\partial y_i}\,\frac{\partial y_i}{\partial x_j}$$
  $x_j$를 미는 효과가 각 $y_i$를 따로 거쳐 $L$에 닿고 1차 효과는 더해지기 때문이다. 이 합을 $j$에 대해 쌓으면 정확히 $\nabla_x L = J^\top\,\nabla_y L$이다.
  - **계산.** §1의 야코비안 예제 $y=(x_1x_2,\;x_1+x_2^2)$를 $x=(1,2)$에서 쓰면 $y=(2,5)$이고, $L=y_1y_2$로 두자. $\nabla_y L=(y_2,\,y_1)=(5,2)$이고 $\nabla_x L=J^\top(5,2)=\begin{pmatrix}2&1\\1&4\end{pmatrix}(5,2)=(12,\,13)$이다. $L=x_1x_2(x_1+x_2^2)$에 중앙 유한 차분을 걸면 $(12.000,\,13.000)$ ✓.
- 이 곱의 두 가지 계산 순서:
  - **순방향 모드**: $\partial/\partial x_i$를 입력 쪽부터 전파 — *입력마다* 한 패스.
  - **역방향 모드**: $\partial L/\partial(\cdot)$를 출력 쪽부터 전파 — *출력마다* 한 패스.
  - **식으로 쓰면.** 순방향 모드는 **탄젠트** $\dot x$(고른 입력 방향)를 각 기본 연산 $y=f(x)$에 **야코비안-벡터 곱** $\dot y = J\dot x$로 통과시킨다. $\dot x=e_j$($j$번째 단위벡터)를 씨앗으로 넣으면 야코비안의 $j$번째 열이 나오므로, 입력이 $n$개인 야코비안 전체에는 패스 $n$번이 든다. 역방향 모드는 **수반(adjoint)** $\bar y=\partial L/\partial y$를 **벡터-야코비안 곱** $\bar x = J^\top\bar y$로 뒤로 나른다. $\bar y=e_i$를 넣으면 $i$번째 행이 나오므로, 출력이 $m$개인 야코비안에는 패스 $m$번이 든다. §1의 야코비안으로: 순방향에 $\dot x=(1,0)$을 넣으면 첫 열 $(2,1)$, 역방향에 $\bar y=(0,1)$을 넣으면 둘째 행 $(1,4)$가 나온다.
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
  - **VJP의 완전한 정의.** 야코비안이 $J$인 기본 연산 $y=f(x)$의 VJP는 출력 크기의 민감도 $v=\partial L/\partial y$를 입력 크기의 민감도 $J^\top v=\partial L/\partial x$로 보내는 선형 사상이다. 기본 연산은 이것을 규칙으로 제공하고 $J$를 만들지 않는다. 입출력이 $10^7$개인 층이라면 $J$의 성분이 $10^{14}$개이기 때문이다. §3에서 이미 쓰는 규칙 둘: 선형층 $y=Wx$의 VJP는 $v\mapsto W^\top v$, 원소별 ReLU의 VJP는 $v\mapsto v\odot\mathbb{1}[z>0]$이다.
  - **gradient checkpointing의 완전한 정의.** 메모리와 계산을 맞바꾸는 방법이고 두 부분으로 된다. 순전파에서는 고른 **체크포인트**에서만 활성값을 저장하고, 역전파에서는 각 구간의 VJP가 필요로 하기 직전에 그 구간의 활성값을 체크포인트부터 **재계산**한다. 비용은 대략 순전파 한 번 추가다. $n$층 네트워크에서 $\sqrt{n}$층마다 체크포인트를 두면 활성값 메모리가 $O(n)$에서 $O(\sqrt{n})$으로 준다(Chen et al., "Training Deep Nets with Sublinear Memory Cost," 2016).
<svg viewBox="0 0 560 228" style="max-width:100%;height:auto" role="img" aria-label="파라미터마다 한 번 왼쪽에서 오른쪽으로 쓸어가는 순방향 모드와, 손실 하나에 대해 한 번 오른쪽에서 왼쪽으로 쓸어오는 역방향 모드">
  <defs><marker id="cbA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1">
    <rect x="70" y="38" width="52" height="26" rx="3"/><rect x="160" y="38" width="52" height="26" rx="3"/><rect x="250" y="38" width="52" height="26" rx="3"/><rect x="340" y="38" width="52" height="26" rx="3"/><circle cx="446" cy="51" r="14"/>
  </g>
  <g fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1">
    <rect x="70" y="108" width="52" height="26" rx="3"/><rect x="160" y="108" width="52" height="26" rx="3"/><rect x="250" y="108" width="52" height="26" rx="3"/><rect x="340" y="108" width="52" height="26" rx="3"/><circle cx="446" cy="121" r="14"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#cbA)" opacity="0.85">
    <line x1="124" y1="51" x2="158" y2="51"/><line x1="214" y1="51" x2="248" y2="51"/><line x1="304" y1="51" x2="338" y2="51"/><line x1="394" y1="51" x2="428" y2="51"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#cbA)" opacity="0.85">
    <line x1="160" y1="121" x2="124" y2="121"/><line x1="250" y1="121" x2="214" y2="121"/><line x1="340" y1="121" x2="304" y2="121"/><line x1="430" y1="121" x2="394" y2="121"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="24" y="30">순방향 모드</text>
    <text x="24" y="100">역방향 모드</text>
    <text x="470" y="56">&#215; 10&#8311;회</text>
    <text x="470" y="126">&#215; 1회</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8">
    <text x="104" y="30">&#8706;/&#8706;&#952;&#7522;를 입력 쪽부터 민다 &#8212; 파라미터마다 한 번</text>
    <text x="104" y="100">&#8706;L/&#8706;(&#183;)를 출력에서 끌어온다 &#8212; 출력마다 한 번</text>
    <text x="70" y="84">파라미터 10&#8311;개</text>
    <text x="470" y="154">스칼라 손실 1개</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="190">이 비대칭은 요령이 아니라 문제의 모양에서 곧장 나온다 &#8212; 입력이 많고 출력이 하나다. 역방향</text>
    <text x="24" y="206">패스가 순방향의 2~3배 비용이므로 실제 차이는 약 7자릿수이고, 대형 모델 학습이 가능한 이유가</text>
    <text x="24" y="222">오직 이것이다. 만약 하나의 입력에 대한 다수 출력의 민감도가 필요했다면 우열이 뒤집힌다.</text>
  </g>
</svg>

**뒤로 간다는 것은 순전파를 되돌린다는 뜻이 아니다.** 순전파는 값을 전달한다. 역전파는 그 값에 대한 최종 손실의 민감도를 전달한다. 연산마다 도착한 민감도에 국소 미분을 곱한다. 값 하나가 여러 분기를 통해 손실에 영향을 주면 분기별 기여를 더한다. 공유 사용의 효과를 합해야지 마지막 분기만 세면 안 된다.

따라서 Jᵀv의 전치는 역행렬이 아니다. 출력에서 입력을 복원하는 것이 아니라 입력 변화가 출력 손실에 미칠 영향을 묻는다. 직사각 사상이나 정보를 잃는 사상도 역전파할 수 있는 이유다. 이 구분이 있어야 야코비안의 역학적 쓰임과 연결하면서 역기구학과 혼동하지 않는다.

**기존 순전파 예제를 다시 해 본다.** 중간값마다 모양을 적고 그 옆에 손실 민감도 변수를 둔다. 뒤로 걸으며 민감도의 모양이 해당 값과 같은지 확인한다. 숫자를 계산하기 전에도 많은 오류를 잡을 수 있다.

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

**위 단계에 나온 표기 셋, 각각의 정의.** (손실 $L=\tfrac12\|\hat y-y\|^2$는 [[02-foundations/neural-network-basics|0.7 §3]]의 제곱 오차 손실이다.)
- **외적(outer product).** 열벡터 $u\in\mathbb{R}^m$과 열벡터 $v\in\mathbb{R}^n$의 외적은 $m\times n$ 행렬이다.
  $$(uv^\top)_{ij} = u_i\,v_j$$
  즉 모든 성분이 $u$의 성분 하나와 $v$의 성분 하나의 곱이다. 계수는 1이다(모든 행이 $v^\top$의 배수). 예: $u=(1,2)$, $v=(3,4,5)$이면 $\begin{pmatrix}3&4&5\\6&8&10\end{pmatrix}$. 대조되는 **내적** $u^\top v$는 숫자 하나이고 길이가 같아야 한다. 여기 나오는 이유: 가중치 $W_{ij}$가 입력 $h_j$를 출력 $i$로 보내며 곱해지기 때문에 $\partial L/\partial W_{ij}=\delta_i\,h_j$다.
- **아다마르(원소별) 곱** $\odot$. 모양이 같은 두 벡터나 행렬에 대해
  $$(a\odot b)_i = a_i\,b_i$$
  즉 같은 자리 성분끼리 곱하고 모양을 유지한다. 예: $(-0.5,\,0.5,\,-0.25)\odot(1,0,1)=(-0.5,\,0,\,-0.25)$. 행렬곱이 아니다. $a\odot b$는 모양이 같아야 하고, $ab$는 안쪽 차원이 맞아야 한다.
- **지시 함수** $\mathbb{1}[\cdot]$. 안의 조건이 참이면 $1$, 거짓이면 $0$을 돌려주고, 벡터에는 성분별로 적용한다. $\mathbb{1}[z>0]$이 ReLU의 도함수다. $z>0$에서 기울기 $1$, $z<0$에서 기울기 $0$이다. 정확히 $z=0$에서 ReLU는 미분 불가능하고, PyTorch 같은 프레임워크는 그냥 $0$을 쓴다.

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
- **부호는 국소적으로 무엇을 할지 말해준다.** $\delta_2 = -0.5$가 음수인 이유는 예측이
  *너무 낮았기* 때문이며, 경사 하강에서 2단계의 출력층 가중치 셋은 모두 증가한다. 앞쪽 층은
  뒤쪽 가중치의 부호도 물려받는다. 여기서는 $W_2$의 음수 경로 때문에 $W_1$의 두 번째 행이
  감소한다. 예측이 낮다고 네트워크의 모든 가중치가 증가하는 것은 아니다.
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
  교차 엔트로피 — 손실 $-\log p_{\text{정답}}$, 유도는 [[02-foundations/information-theory|5. 정보이론 §2]] — 로 채점하는 것). 모든 분류 헤드가 이것이고, softmax는 어텐션 내부의 연산
  그 자체다([[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]).
  로봇 정책도 행동을 토큰으로 이산화하면 이것을 쓴다
  ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]]은 각 행동 차원을 256개 구간으로 나눠 제어를
  분류 문제로 만든다). 알아둘 예외: 출력이 연속값인 정책 — 회귀 헤드와
  [[01-canonical-papers/notes/4-vla/diffusion-policy|디퓨전]]·플로우 매칭 정책 — 은 대신
  제곱 오차로 학습한다.
  로짓 $z$, $p = \text{softmax}(z)$, 원-핫 정답 $y$일 때:
  $\dfrac{\partial L}{\partial z} = p - y$ — *예측에서 정답을 뺀 것*, 그게 전부다.
  (유도: $L = -\log p_c$; $\partial \log p_c/\partial z_j = \mathbb{1}[j=c] - p_j$.)
  - **네 대상, 각각의 정의.** **로짓** $z\in\mathbb{R}^K$는 네트워크가 내는 정규화 전 점수로, 클래스마다 하나씩이고 아무 실수나 될 수 있다. **softmax**는 $\mathbb{R}^K$에서 확률 벡터로 가는 사상이다.
    $$p_j = \text{softmax}(z)_j = \frac{e^{z_j}}{\sum_{k=1}^{K} e^{z_k}}$$
    그래서 모든 $p_j$가 양수이고(지수 함수이므로), 합이 $1$이며(분모가 공통 합계이므로), 점수의 순서가 유지된다. 모든 로짓에 같은 상수를 더해도 인수 $e^{c}$가 약분되므로 아무것도 바뀌지 않는다. **원-핫** 정답 $y$는 정답 클래스 $c$에서 $y_c=1$, 나머지는 $0$이다. 이에 대한 **교차 엔트로피**는 $L=-\sum_j y_j\log p_j=-\log p_c$이고, 일반 정의는 [[02-foundations/information-theory|5. 정보이론 §2]]에 있다.
  - **계산.** $z=(2,1,0)$, 정답 클래스 $c=1$(첫째). softmax는 $p=(0.665,\,0.245,\,0.090)$이고, $z+10=(12,11,10)$도 같은 $p$를 준다. 손실은 $-\log 0.665=0.408$, 그래디언트는 $p-y=(-0.335,\,0.245,\,0.090)$이다. 정답 로짓은 올리고 나머지 둘은 내리되, 각자 잘못 가져간 확률에 비례해 움직인다.
  실무에서는 지수가 넘치지 않도록 log-sum-exp를 거쳐 계산한다 —
  [[02-foundations/engineering-math|0.5 §6]]에 유도해 두었다. 같은 손실을 평균 손실의 $1/N$과
  유한 차분 그래디언트 검사까지 넣어 NumPy로 짠 것은 [[02-foundations/algorithms/robotics-ai-problems|11.8 §9]]에 있다.
- **ReLU**: 마스크 그래디언트 — 싸고, 포화하지 않는다; 포화 활성함수를 밀어낸 이유다
  ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]은 tanh와 비교해 몇 배 빠른 학습을 보고했다). 죽은 유닛 = 영원히 0인 마스크.
  식으로 쓰면 $\text{ReLU}(z)=\max(0,z)$이고 도함수는 $\mathbb{1}[z>0]$(§3)이다. 양수 입력이 아무리 커도 기울기가 정확히 $1$이므로 **포화하지 않는다**. **죽은 유닛**은 사전 활성값 $z=w^\top x+b$가 데이터의 모든 입력에서 음수인 유닛이다. 마스크가 항상 $0$이라 $w$와 $b$가 그래디언트 0을 받고, 다시는 돌아오지 못한다. 예: $w=1$, $b=-10$, 입력 $x\in[0,1]$이면 모든 예제에서 $z\le-9$다.
- **시그모이드** $\sigma' = \sigma(1-\sigma) \le 1/4$: 시그모이드를 쌓으면 그래디언트가 기하급수적으로 줄어든다.
  식으로 쓰면, 시그모이드는 임의의 실수 $z$를 $(0,1)$로 눌러 넣는다.
  $$\sigma(z) = \frac{1}{1+e^{-z}}$$
  그래서 $\sigma(0)=0.5$, $\sigma(4)=0.982$, $\sigma(-4)=0.018$이다. 미분하면 $\sigma'(z)=e^{-z}/(1+e^{-z})^2$이고, 이 분수를 $\frac{1}{1+e^{-z}}\cdot\frac{e^{-z}}{1+e^{-z}}$로 쪼개면 $\sigma(1-\sigma)$와 같음이 보인다. $|z|$가 커서 $\sigma$가 $0$이나 $1$ 근처에 붙어 $\sigma'$가 거의 $0$인 유닛을 **포화**했다고 한다.
  이 상한이 성립하는 이유는 $\sigma(1-\sigma)$가 $\sigma\in(0,1)$에서 위로 볼록한(아래로 열린) 포물선이라 $\sigma=1/2$(즉 $z=0$)에서 가장 크고, 그 값이 $1/2\cdot1/2=1/4$이기 때문이다.
  시그모이드 층 하나가 역방향 신호에 많아야 0.25를 곱하고, 0.25는 $z=0$에서의 *최선*이다.
  시그모이드 도함수만 따져도 층 열 개면 그래디언트가 최소 백만 배 준다: $0.25^{10} \approx 9.5\times10^{-7}$.
  유닛이 포화하면 훨씬 더 준다. $\sigma'(4) \approx 0.018$이기 때문이다. 실제 그래디언트에는 가중치 야코비안도 함께 곱해진다. 이 부등식 하나가 구조
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
  - **식으로 쓰면.** 야코비안이 $J_t=\partial h_t/\partial h_{t-1}$인 $T$개의 층 또는 시간 스텝 $h_t=f_t(h_{t-1})$에 §2의 연쇄 법칙을 적용하면
    $$\frac{\partial L}{\partial h_0} = J_1^\top J_2^\top\cdots J_T^\top\,\frac{\partial L}{\partial h_T}$$
    즉 첫 층에 닿는 신호는 행렬 $T$개를 통과했고, 크기는 $\big\lVert\partial L/\partial h_0\big\rVert\le\prod_t\lVert J_t\rVert\,\big\lVert\partial L/\partial h_T\big\rVert$로 묶인다. **소실**은 모든 $\lVert J_t\rVert\le\rho<1$인 경우이고, 적어도 $\rho^{T}$만큼 빠른 감쇠를 강제한다. 스칼라 야코비안 $0.9$가 $50$스텝 이어지면 그래디언트에 $0.9^{50}=0.0052$가 곱해진다. 결과: 뒤쪽 층은 여전히 배우는데 앞쪽 층이나 앞쪽 시간 스텝은 배우기를 멈춘다.
- **그래디언트 폭발**: 노름 > 1 — gradient clipping($\|g\|$를 상한으로 재스케일)으로
  처치, RNN/LLM 학습의 표준.
  - **식으로 쓰면.** 같은 곱의 인수가 $1$보다 크면 $\rho^{T}$처럼 커질 수 있다. 스칼라 야코비안 $1.1$이 $50$스텝이면 그래디언트에 $1.1^{50}=117$이 곱해지고, 그런 스텝 한 번이 가중치를 손실이 말이 되던 영역 밖으로 던질 수 있다. 상한 $c$의 **노름 클리핑**은 그래디언트 $g$를 이렇게 재스케일한다.
    $$g \leftarrow g\cdot\min\!\Big(1,\ \frac{c}{\lVert g\rVert}\Big)$$
    그래서 이미 $c$보다 짧은 그래디언트는 그대로이고, 긴 것은 방향을 유지한 채 길이가 정확히 $c$로 줄어든다. 예: $g=(3,4)$는 길이 $5$이고, $c=1$이면 $(0.6,\,0.8)$이 된다.
- **Stop-gradient** $\text{sg}[\cdot]$: 그래프를 의도적으로 자르기. reparameterization
  ([[01-canonical-papers/notes/6-diffusion/vae|VAE]])은 샘플링을 미분 경로 *밖으로* 옮기고, EMA
  교사(지수 이동 평균 — 교사 가중치가 학생 가중치를 천천히 따라가는 이동 평균이다; [[01-canonical-papers/notes/2-computer-vision/dino|DINO]])와 RL 타깃 네트워크는 설계상 그래디언트를 받지
  않는다. 논문 그림의 점선 화살표는 *대개* stop-gradient지만, 보조 경로나 추론 전용
  경로를 뜻하기도 하므로 반드시 범례를 확인하라.
  - **stop-gradient의 완전한 정의.** 규칙 두 개를 가진 연산자다. 순전파에서는 항등, $\text{sg}[a]=a$이고, 역전파에서는 도함수를 0으로 선언한다, $\partial\,\text{sg}[a]/\partial a=0$. 그래서 값은 쓰이지만 그것을 거쳐 민감도가 뒤로 흐르지 않는다(PyTorch의 `detach()`, JAX의 `stop_gradient`). 예: $L=(\text{sg}[a]-b)^2$을 $a=3$, $b=1$에서 보면 $L=4$, $\partial L/\partial b=-2(a-b)=-4$, $\partial L/\partial a=0$이다. 연산자가 없었다면 $+4$였다.
  - **reparameterization의 완전한 정의.** 샘플 $z\sim\mathcal{N}(\mu,\sigma^2)$를 파라미터와 외부 잡음의 결정적 함수로 바꾼다.
    $$z = \mu + \sigma\,\epsilon,\qquad \epsilon\sim\mathcal{N}(0,1)$$
    이 $z$의 분포가 정확히 같으면서 이제 $\partial z/\partial\mu=1$, $\partial z/\partial\sigma=\epsilon$이 평범한 도함수이기 때문이다. 예: $\mu=1$, $\sigma=2$, 뽑힌 $\epsilon=0.5$이면 $z=2$이고 $\partial z/\partial\sigma=0.5$다. $\mathcal{N}(\mu,\sigma^2)$에서 $z$를 직접 뽑는 것이 반례다. 그 추출은 미분할 수 있는 $\mu$의 함수가 아니다.
  - **EMA 교사의 완전한 정의.** 학생이 갱신될 때마다 교사 파라미터 $\theta_T$가 학생 파라미터 $\theta_S$ 쪽으로 일정 비율만큼 움직이고, 감쇠 $\tau$는 $1$보다 조금 작다.
    $$\theta_T \leftarrow \tau\,\theta_T + (1-\tau)\,\theta_S$$
    그래서 $k$스텝 전 학생 값은 $\tau^{k}$에 비례하는 가중치를 유지하고, 교사는 그래디언트가 아니라 오직 이 규칙으로만 값을 얻는다. $\tau=0.99$이면 그 가중치가 $\ln 0.5/\ln 0.99\approx69$스텝마다 절반이 된다. DINO의 스케줄은 $\tau=0.996$에서 시작하며, 반감기는 약 $173$스텝이다.

### 6. 구현자의 눈으로 수식 읽기

- 학습 데이터에 대한 기댓값은 흔히 미니배치 평균으로 추정하지만, 유한 합·해석적 기댓값·
  동적계획법으로 직접 계산할 수 있는 경우도 있다. 딥러닝에서는 계산하기 어렵거나
  reparameterize할 수 없는 기댓값을 흔히 하한([[02-foundations/information-theory|ELBO]]),
  몬테카를로 추정, 또는 그래디언트 추정 기법(reparameterization;
  우도비/정책 그래디언트 — [[02-foundations/rl-basics|RL 기초]])이 된다.
  - **미니배치 추정의 완전한 정의.** 학습 손실이 예제 $N$개의 손실 $\ell_i$의 평균일 때, 크기 $|B|$의 무작위 부분집합 $B$에 대한 미니배치 그래디언트는
    $$\hat g = \frac{1}{|B|}\sum_{i\in B}\nabla\ell_i(\theta)\ \approx\ \frac{1}{N}\sum_{i=1}^{N}\nabla\ell_i(\theta)$$
    이고 **불편**이다. 가능한 모든 배치에 대해 평균하면 전체 그래디언트와 같으므로, 한 번 뽑을 때마다 시끄럽지만 평균적으로는 맞다. 숫자로 푼 예는 [[02-foundations/optimization|4. 최적화 §3]]에 있다.
- $\arg\max$는 미분 불가능하다; softmax가 그 매끄러운 대역이다(온도가 날카로움을 조절).
  샘플링도 미분 불가능하다; Gumbel-softmax / straight-through 추정기가 흉내 낸다. Gumbel-softmax는 이산 샘플을 잡음을 더한 로짓의 매끄러운 softmax(온도로 날카로움 조절)로 바꾸고, straight-through는 순방향에서는 딱딱한 샘플을 쓰되 역방향에서는 매끄러운 쪽의 그래디언트를 흘려보낸다.
  - **온도가 있는 softmax.** 온도 $\tau>0$에서
    $$p_j = \frac{e^{z_j/\tau}}{\sum_k e^{z_k/\tau}}$$
    그래서 $\tau=1$이면 평범한 softmax, 작은 $\tau$는 $\arg\max$의 원-핫 벡터 쪽으로 날카로워지고, 큰 $\tau$는 균등 분포 쪽으로 평평해진다. $z=(2,1,0)$에서 $\tau=1$은 $(0.665,\,0.245,\,0.090)$, $\tau=0.5$는 $(0.867,\,0.117,\,0.016)$, $\tau=0.1$은 $(0.99995,\,0.00005,\,0.00000)$이다. $\arg\max$ 자체가 반례다. 출력이 원-핫 벡터 사이를 뛰어다니므로 도함수가 거의 모든 곳에서 0이다.
  - **Gumbel-softmax의 완전한 정의.** 세 단계다. $(0,1)$에서 균등하게 $u_j$를 뽑아 굼벨 잡음 $g_j=-\log(-\log u_j)$를 만든다. 그러면 $\arg\max_j(z_j+g_j)$가 $\text{softmax}(z)$의 정확한 샘플이다(굼벨-맥스 트릭). 마지막으로 그 $\arg\max$를 온도 softmax로 바꾼다.
    $$y_j = \frac{e^{(z_j+g_j)/\tau}}{\sum_k e^{(z_k+g_k)/\tau}}$$
    $y$는 $z$에 대해 매끄럽고 $\tau\to0$이면 원-핫 샘플에 다가가기 때문이다. 예: $z=(2,1,0)$, $u=(0.1,\,0.9,\,0.5)$이면 $g=(-0.834,\,2.250,\,0.367)$, $z+g=(1.166,\,3.250,\,0.367)$이라 이번 추출은 로짓이 더 큰 클래스 1이 아니라 클래스 2를 고른다. 샘플링이라면 가끔 그래야 한다. $\tau=1$에서 $y=(0.105,\,0.847,\,0.047)$, $\tau=0.5$에서 $y=(0.015,\,0.982,\,0.003)$이다.
  - **straight-through의 완전한 정의.** 순전파에서는 딱딱한 원-핫 $y_{\text{hard}}$를, 역전파에서는 부드러운 $y$의 그래디언트를 쓴다. §5의 stop-gradient로 쓰면
    $$y_{\text{ST}} = y_{\text{hard}} - \text{sg}[y] + y$$
    순전파 값은 $y_{\text{hard}}-y+y=y_{\text{hard}}$이고, 역전파는 딱딱한 두 항이 아무것도 보태지 않아 $\partial y_{\text{ST}}/\partial z=\partial y/\partial z$를 보기 때문이다. 그래서 그래디언트는 편향되어 있다. 조금 다른 매끄러운 계산의 그래디언트다.
- 프레임워크는 수식이 아니라 *프로그램*을 미분한다: 제어 흐름, 루프, in-place 연산에 전부
  그래디언트 의미론이 있다 — "손실이 안 줄어요" 버그의 대부분은 그래프 버그다.

> [!tip] 더 깊이 · Going deeper
> 아래 깔린 기계장치를 보려면: Baydin, Pearlmutter, Radul, Siskind, "Automatic Differentiation in Machine Learning: a Survey," *JMLR* 18(153), 2018 — 순방향과 역방향 모드를 정확히 가른 논문이다. 역전파를 알고리즘으로 다루는 것은 [*Deep Learning* 책](https://www.deeplearningbook.org/) 6장.

### 스스로 점검

1. 계산 예제를 $K$-클래스 출력($W_2 \in \mathbb{R}^{K\times 3}$)과 MSE 대신 softmax-CE로 바꾸면 무엇이 바뀌는가? (예제의 스칼라 출력 하나에 softmax를 걸면 항상 1이라 그래디언트가 0이 된다.)
2. $\partial(x + F(x))/\partial x = I + J_F$를 보이고, 깊이가 더는 감쇠를 강제하지 않는 이유를
   설명하라.
3. 순방향 모드 자동 미분은 왜 *입력 파라미터마다* 한 패스가 들고, 그것이 7B 모델에 왜
   치명적인가?
4. [[01-canonical-papers/notes/6-diffusion/vae|VAE]]에서 $z \sim \mathcal{N}(\mu, \sigma^2)$를 직접
   역전파할 수 없는 이유는, 그리고 $z = \mu + \sigma\epsilon$이 이를 고치는 방식은?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $\delta_2$가 스칼라 $\hat y - y$ 대신 $K$-벡터 $p - y$(softmax+CE의 결과)가 된다. 2~5단계는 $W_2$가 $K\times 3$이 된 채로 같은 공식을 쓴다.
> 2. 합의 미분 = 미분의 합: $I + \partial F/\partial x$ — 항등 항 덕분에 역방향 신호가 아무리 깊어도 곱해 줄어들지 않는 경로를 하나 갖는다. 즉 깊이가 감쇠를 *강제하지* 않게 될 뿐이고, 전체 gradient가 절대 줄지 않는다는 보장은 아니다.
> 3. 순방향 모드는 입력 방향 하나당 전체 패스 한 번 — 7B 파라미터면 패스 7B번이 필요해 불가능; 역방향은 스칼라 손실(출력 1개) 기준 한 번이면 된다.
> 4. 샘플링은 미분 불가능한 확률적 분기다; $z = \mu + \sigma\epsilon$으로 쓰면 무작위성이 외부 입력 $\epsilon$으로 밀려나 $\mu, \sigma$에 그래디언트가 흐른다.
