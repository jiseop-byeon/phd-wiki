---
title: 1. Learning Systems
tags: [deep-learning, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Trace one model from tensors and loss through an optimizer update, validation, and a defensible training claim."
mastery-when: "Raise when architecture, objective, optimization, or scaling is part of the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/neural-network-basics|0.7 Neural Networks]], [[02-foundations/calculus-backprop|2. Calculus & Backprop]], [[02-foundations/optimization|4. Optimization]], and [[02-foundations/ml-practice|9. ML Practice]]. Object **D1** from [[03-deep-learning/lab-objects|0. Lab Objects]]; the Tier A lab in §6 needs NumPy and nothing else.
> [[02-foundations/neural-network-basics|0.7 신경망]], [[02-foundations/calculus-backprop|2. 미적분과 역전파]], [[02-foundations/optimization|4. 최적화]], [[02-foundations/ml-practice|9. ML 실무]]. 대상은 [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D1**이고, §6의 Tier A 실습에는 NumPy만 있으면 된다.

## English

> [!note] First pass
> Read §§1–4 and do questions 1–2. Work the Worked case by hand before you open §6 — the lab checks your arithmetic, it does not replace it. Return to §5 when comparing training sections in papers.

### Running object: D1

Use **D1** from [[03-deep-learning/lab-objects|0. Lab Objects]], biases zero:

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}.$$

Forward: $W_1x=(1,2,1)$, $h=\operatorname{ReLU}(W_1x)=(1,2,1)$, $s=W_2h=(2,1)$. The prediction is $p=\operatorname{softmax}(s)$. A diagram must show shapes $2\rightarrow3\rightarrow2$. This is not **P1** ($2\to3\to1$ MSE).

The target is class 1 throughout this page, so $y=(1,0)$, and every number below follows from those five objects and nothing else.

*Scope: this page teaches the typed pipeline from one input to one parameter update — shapes, softmax, cross-entropy, the backward pass, one SGD step, and the step size that update has to respect — and the evidence a training claim owes. It does not teach where the derivatives come from, which is [[02-foundations/calculus-backprop|2. Calculus & Backprop §2]]; nor the optimizers themselves (momentum, Adam, schedules), which are [[02-foundations/optimization|4. Optimization §3]]; nor the experimental protocol that turns a number into a result, which is [[02-foundations/ml-practice|9. ML Practice §4]]; nor any architecture beyond a two-layer MLP — convolutions and patch tokens are [[03-deep-learning/computer-vision/index|2. Computer Vision]], and attention is [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]] and the [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer note]].*

### Homework diagram

One diagram, and the problem set asks for exactly this one. Draw both directions on the same picture. The figure is the worked case below, on the catalog numbers; problem 1 asks for the same drawing with batch shapes for $B=4$.

<svg viewBox="0 0 560 518" style="max-width:100%;height:auto" role="img" aria-label="D1's forward pass down the left with every tensor's shape and value, its weights and zero biases in the middle, and the backward pass up the right with every gradient's value">
  <defs><marker id="aD1e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="22" font-size="12" fill="currentColor">D1 · target class 1, y = (1, 0) · solid: forward · dashed: backward</text>
  <text x="75" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">forward · activations</text>
  <text x="265" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">parameters · biases present, zero</text>
  <text x="469" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">backward · gradients</text>
  <line x1="144" y1="34" x2="144" y2="390" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 4"/>
  <line x1="385" y1="34" x2="385" y2="390" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 4"/>
  <rect x="12" y="49" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="63" font-size="11" fill="currentColor" text-anchor="middle">x · 2</text>
  <text x="75" y="78" font-size="11" fill="currentColor" text-anchor="middle">(1, 2)</text>
  <rect x="12" y="153" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="167" font-size="11" fill="currentColor" text-anchor="middle">z · 3</text>
  <text x="75" y="182" font-size="11" fill="currentColor" text-anchor="middle">(1, 2, 1)</text>
  <rect x="12" y="241" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="255" font-size="11" fill="currentColor" text-anchor="middle">h · 3</text>
  <text x="75" y="270" font-size="11" fill="currentColor" text-anchor="middle">(1, 2, 1)</text>
  <rect x="12" y="349" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="363" font-size="11" fill="currentColor" text-anchor="middle">s · 2</text>
  <text x="75" y="378" font-size="11" fill="currentColor" text-anchor="middle">(2, 1)</text>
  <line x1="75" y1="83" x2="75" y2="107" stroke="currentColor" stroke-width="1.4"/>
  <line x1="75" y1="129" x2="75" y2="152" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1e)"/>
  <line x1="75" y1="275" x2="75" y2="301" stroke="currentColor" stroke-width="1.4"/>
  <line x1="75" y1="323" x2="75" y2="348" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1e)"/>
  <rect x="31" y="107" width="88" height="22" rx="11" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="122" font-size="11" fill="currentColor" text-anchor="middle">W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">x + b</tspan><tspan dy="3" font-size="10">1</tspan></text>
  <rect x="31" y="301" width="88" height="22" rx="11" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="316" font-size="11" fill="currentColor" text-anchor="middle">W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3">h + b</tspan><tspan dy="3" font-size="10">2</tspan></text>
  <line x1="75" y1="187" x2="75" y2="205" stroke="currentColor" stroke-width="1.4"/>
  <rect x="35" y="205" width="80" height="18" stroke="currentColor" stroke-width="1.6" fill="currentColor" fill-opacity="0.1"/>
  <text x="75" y="218" font-size="11" fill="currentColor" text-anchor="middle">ReLU gate</text>
  <line x1="75" y1="223" x2="75" y2="240" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1e)"/>
  <line x1="75" y1="383" x2="75" y2="397" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1e)"/>
  <rect x="12" y="397" width="536" height="26" rx="5" stroke="currentColor" stroke-width="1.6" fill="currentColor" fill-opacity="0.07"/>
  <text x="265" y="414" font-size="11.5" fill="currentColor" text-anchor="middle">softmax + cross-entropy · one block</text>
  <line x1="75" y1="423" x2="75" y2="433" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1e)"/>
  <rect x="12" y="434" width="126" height="54" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="449" font-size="11" fill="currentColor" text-anchor="middle">p · 2</text>
  <text x="75" y="465" font-size="11" fill="currentColor" text-anchor="middle">p<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= 0.731059</tspan></text>
  <text x="75" y="481" font-size="11" fill="currentColor" text-anchor="middle">p<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= 0.268941</tspan></text>
  <line x1="265" y1="423" x2="265" y2="444" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1e)"/>
  <rect x="177" y="445" width="176" height="24" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="265" y="461" font-size="11" fill="currentColor" text-anchor="middle">L · scalar = 0.313262 nats</text>
  <text x="152" y="70" font-size="11" fill="currentColor">W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">· 3×2</tspan></text>
  <text x="176" y="87" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="196" y="87" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="176" y="101" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="196" y="101" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="176" y="115" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="196" y="115" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M158 76 L154 76 L154 119 L158 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M196 76 L200 76 L200 119 L196 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="220" y="70" font-size="11" fill="currentColor">b<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">· 3 = 0</tspan></text>
  <text x="242" y="87" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="242" y="101" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="242" y="115" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M224 76 L220 76 L220 119 L224 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M242 76 L246 76 L246 119 L242 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="152" y="142" font-size="11" fill="currentColor">∂L/∂W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= (∂L/∂z) x</tspan><tspan dy="-4" font-size="10">T</tspan><tspan dy="4" dx="3.5">· 3×2</tspan></text>
  <text x="224" y="159" font-size="11" fill="currentColor" text-anchor="end">0.268941</text>
  <text x="292" y="159" font-size="11" fill="currentColor" text-anchor="end">0.537883</text>
  <text x="224" y="173" font-size="11" fill="currentColor" text-anchor="end">−0.268941</text>
  <text x="292" y="173" font-size="11" fill="currentColor" text-anchor="end">−0.537883</text>
  <text x="224" y="187" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="292" y="187" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M158 148 L154 148 L154 191 L158 191" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M292 148 L296 148 L296 191 L292 191" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <line x1="151" y1="97" x2="121" y2="116" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD1e)"/>
  <text x="152" y="258" font-size="11" fill="currentColor">W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">· 2×3</tspan></text>
  <text x="176" y="275" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="196" y="275" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="216" y="275" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="176" y="289" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="196" y="289" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="216" y="289" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M158 264 L154 264 L154 293 L158 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M216 264 L220 264 L220 293 L216 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="240" y="258" font-size="11" fill="currentColor">b<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">· 2 = 0</tspan></text>
  <text x="262" y="275" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="262" y="289" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M244 264 L240 264 L240 293 L244 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M262 264 L266 264 L266 293 L262 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="152" y="318" font-size="11" fill="currentColor">∂L/∂W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= (p − y) h</tspan><tspan dy="-4" font-size="10">T</tspan><tspan dy="4" dx="3.5">· 2×3</tspan></text>
  <text x="224" y="335" font-size="11" fill="currentColor" text-anchor="end">−0.268941</text>
  <text x="292" y="335" font-size="11" fill="currentColor" text-anchor="end">−0.537883</text>
  <text x="360" y="335" font-size="11" fill="currentColor" text-anchor="end">−0.268941</text>
  <text x="224" y="349" font-size="11" fill="currentColor" text-anchor="end">0.268941</text>
  <text x="292" y="349" font-size="11" fill="currentColor" text-anchor="end">0.537883</text>
  <text x="360" y="349" font-size="11" fill="currentColor" text-anchor="end">0.268941</text>
  <path d="M158 324 L154 324 L154 353 L158 353" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M360 324 L364 324 L364 353 L360 353" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <line x1="151" y1="279" x2="121" y2="310" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD1e)"/>
  <rect x="390" y="349" width="158" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="363" font-size="11" fill="currentColor" text-anchor="middle">∂L/∂s = p − y · 2</text>
  <text x="469" y="378" font-size="11" fill="currentColor" text-anchor="middle">(−0.268941, 0.268941)</text>
  <rect x="390" y="241" width="158" height="52" rx="4" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="255" font-size="11" fill="currentColor" text-anchor="middle">∂L/∂h = W<tspan dy="3" font-size="10">2</tspan><tspan dy="-7" font-size="10">T</tspan><tspan dy="4">(p − y) · 3</tspan></text>
  <text x="469" y="270" font-size="11" fill="currentColor" text-anchor="middle">(0.268941, −0.268941, 0)</text>
  <text x="469" y="286" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">0: column 3 of W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">is (0, 0)</tspan></text>
  <rect x="390" y="153" width="158" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="167" font-size="11" fill="currentColor" text-anchor="middle">∂L/∂z · 3</text>
  <text x="469" y="182" font-size="11" fill="currentColor" text-anchor="middle">(0.268941, −0.268941, 0)</text>
  <line x1="469" y1="397" x2="469" y2="384" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#aD1e)"/>
  <line x1="469" y1="349" x2="469" y2="294" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#aD1e)"/>
  <text x="475" y="326" font-size="11" fill="currentColor" fill-opacity="0.85">× W<tspan dy="3" font-size="10">2</tspan><tspan dy="-7" font-size="10">T</tspan></text>
  <line x1="389" y1="358" x2="369" y2="342" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#aD1e)"/>
  <line x1="469" y1="241" x2="469" y2="223" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>
  <rect x="415" y="205" width="108" height="18" rx="9" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="218" font-size="11" fill="currentColor" text-anchor="middle">⊙ mask (1, 1, 1)</text>
  <line x1="469" y1="205" x2="469" y2="188" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#aD1e)"/>
  <line x1="117" y1="214" x2="413" y2="214" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="1 3"/>
  <text x="265" y="210" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.9">mask 1[z &gt; 0] = (1, 1, 1)</text>
  <text x="265" y="227" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">read off z, fixed before backward</text>
  <line x1="389" y1="166" x2="301" y2="168" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#aD1e)"/>
  <text x="12" y="502" font-size="11" fill="currentColor" fill-opacity="0.9">No arrow runs from L to W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">: its gradient arrives only through W</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">and the mask.</tspan></text>
</svg>

Five things the drawing has to get right, each of which is a claim about the computation.
**Every tensor labelled with its shape** — $x$ (2), $z$ (3), $h$ (3), $s$ (2), $p$ (2), $L$ (scalar). An unlabelled arrow is where a shape error hides, and a shape error is the most common reason a re-implementation silently trains the wrong model.
**The ReLU drawn as a gate on $z$, not on $h$.** The mask is $\mathbf 1[z>0]$: it is read off the *pre-activation*, and it is fixed for this sample before any gradient flows. Drawing it after $h$ claims the backward pass can choose the mask, which it cannot.
**Softmax and cross-entropy drawn as one block.** Separately they each have an ugly Jacobian; together they emit $p-y$ (§2). The block's output arrow is the only place that expression appears.
**No arrow from $L$ straight to $W_1$.** The gradient reaches $W_1$ only through $W_2$ and then through the mask. That path is the whole of backpropagation, and a diagram with a shortcut is a diagram of a different algorithm.
**Biases marked and marked zero.** D1 freezes them at zero; the parameter count in problem 1 counts them anyway, and the difference between "absent" and "present and zero" is exactly the 5 numbers that separate 12 from 17.

### Worked case

This is the homework object. Do the three things the problem set asks — forward, backward, one step — here first, on the catalog numbers, so the set is a change of target and knob rather than a first derivation. Loss is in nats throughout, because every logarithm on this page is natural.

**Forward.** Symbols, then substitution, then number:

$$z=W_1x=(1,2,1),\qquad h=\operatorname{ReLU}(z)=(1,2,1),\qquad s=W_2h=(2,1).$$

All three pre-activations are positive, so the ReLU mask is $\mathbf 1[z>0]=(1,1,1)$ and nothing is clipped on this sample. The softmax and the loss:

$$p_1=\frac{e^2}{e^2+e^1}=0.731059,\qquad p_2=0.268941,\qquad L=-\log p_1=0.313262 \text{ nats}.$$

**Backward.** The one derivative worth memorising is $\partial L/\partial s=p-y$ (derived in §2), so

$$\frac{\partial L}{\partial s}=(0.731059-1,\ 0.268941-0)=(-0.268941,\ 0.268941).$$

That vector is pushed back through the two matrices. Because $\partial L/\partial W_2=(p-y)h^\top$ is an outer product,

$$\frac{\partial L}{\partial W_2}=\begin{pmatrix}-0.268941&-0.537883&-0.268941\\0.268941&0.537883&0.268941\end{pmatrix},$$

where the middle column is twice the others since $h_2=2$ — the hidden unit that was twice as active takes twice the blame. Continuing back,

$$\frac{\partial L}{\partial h}=W_2^\top(p-y)=(0.268941,\ -0.268941,\ 0),$$

and the third entry is exactly zero because $W_2$'s third column is $(0,0)$: hidden unit 3 is wired to nothing and therefore learns nothing on this sample, no matter how wrong the prediction is. Applying the mask (all ones here) and one more outer product with $x=(1,2)$:

$$\frac{\partial L}{\partial W_1}=\begin{pmatrix}0.268941&0.537883\\-0.268941&-0.537883\\0&0\end{pmatrix}.$$

**One SGD step.** The rule is $\theta\leftarrow\theta-\eta\,\partial L/\partial\theta$. At $\eta=0.1$ the logits move to $s=(2.299452,\ 0.700548)$ — symmetric, by $\pm0.299452$, because $p-y$ is antisymmetric for two classes — and

$$p=(0.831865,\ 0.168135),\qquad L=0.184085,\qquad \Delta L=-0.129177 \text{ nats}.$$

The first-order prediction is $-\eta\lVert g\rVert^2=-0.1\times1.591249=-0.159125$, so the step delivered $81\%$ of what the gradient promised. The gap is curvature, and §6 is about what happens when a larger $\eta$ makes that gap change sign.

### 1. A paper's model is a typed computation

Architecture prose becomes checkable only after attaching shapes. For a batch of $B$ samples, $X\in\mathbb R^{B\times2}$, $H\in\mathbb R^{B\times3}$, and $S\in\mathbb R^{B\times2}$. Parameters are learned; activations are sample-dependent; hyperparameters are chosen outside gradient descent. If these three are mixed, parameter counts and claims about efficiency become unreliable.

> **Parameter, activation, hyperparameter — the three-way split, defined.** All three are *numbers in the same program*, which is why they get confused; they differ in **what changes them**. A **parameter** is a number the optimizer writes: it has a gradient, it is counted in "model size", and it is saved in the checkpoint — D1's $W_1$ and $W_2$, 12 of them, or 17 with the zero biases. An **activation** is a number produced by running the model on an input: it has no gradient of its own to store, it changes with every sample, and it is what dominates training memory — D1's $z$, $h$, $s$, $p$. A **hyperparameter** is a number chosen outside gradient descent, by a human or a search: the learning rate $\eta$, the decay $\lambda$, the batch size, the number of hidden units.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta}\qquad\text{— }\theta\text{ is parameters, }\eta\text{ is a hyperparameter, and }L\text{ was computed from activations}$$
>
> so the update equation itself contains one of each, and reading it left to right is the fastest way to classify any number a paper mentions.
>
> - **Example**: D1's hidden width 3 is a hyperparameter; the resulting $h=(1,2,1)$ is an activation; the $W_1$ that produced it is parameters. Change the width and the parameter count changes; change the input and only the activation changes.
> - **Non-example**: the ReLU mask $\mathbf 1[z>0]=(1,1,1)$. It is an activation, not a parameter — nobody learns it — but it is also not a hyperparameter, because no one chose it. It is derived from the sample, which is why a paper that reports "sparsity" has to say sparsity *of what, on which data*.
> - **Non-example**: an Adam optimizer state. It is written by the optimizer and saved in a checkpoint, so it looks like a parameter, but it is not used in the forward pass and must not be counted in model size. Papers that quote "checkpoint size" instead of parameter count are quoting this.
> - **Why it matters**: "our model is 3× smaller" is a parameter claim, "it needs 3× less memory to train" is an activation claim, and "it is 3× cheaper to tune" is a hyperparameter claim. They are three different experiments and a paper that conflates them has not run any of them. The same split, written for reading experimental sections, is [[02-foundations/neural-network-basics|0.7 Neural Networks §5]].

Those logits $s=(2,1)$ are D1's forward pass, not a second example:

$$p_1=\frac{e^2}{e^2+e^1}=0.731,\qquad p_2=0.269.$$

With class 1 as the target, cross-entropy is $-\log p_1=0.313$. Adding the same constant to both logits changes neither probability: softmax represents relative evidence.

> **Softmax, defined.** The **softmax** is a *map from a vector of real logits to a point in the probability simplex* — a function, not a layer with parameters, and not a probability of being correct. Three defining conditions. Its outputs are **positive and sum to one**, which is what makes them usable as a distribution. It is **shift invariant**, $\operatorname{softmax}(s+c\mathbf 1)=\operatorname{softmax}(s)$, so only logit *differences* carry information. And it is **strictly monotone in each logit**, so the ranking of the logits is the ranking of the probabilities and the arg max never moves.
>
> $$p_i=\frac{e^{s_i}}{\sum_{j=1}^{C}e^{s_j}}$$
>
> where $s\in\mathbb R^{C}$ are the logits, $C$ the number of classes, and $p_i$ the predicted probability of class $i$ — and implementations subtract $\max_j s_j$ from every logit first, which changes nothing because of shift invariance but keeps $e^{s_j}$ from overflowing.
>
> - **Example**: D1's $s=(2,1)$ gives $p=(0.731059,0.268941)$, and $s=(102,101)$ gives exactly the same $p$, because only the difference $s_1-s_2=1$ entered.
> - **Non-example**: a max. Softmax does not return $\max_j s_j$ or a one-hot at the arg max; it returns a spread whose sharpness depends on the logit *gaps*, which is the whole subject of the temperature sweep on [[03-deep-learning/vlm/index|3. VLM]].
> - **Non-example**: a confidence that the answer is right. $p_1=0.731$ is the model's number, not a measured frequency; whether $73\%$ of such predictions are correct is calibration, measured separately ([[02-foundations/ml-practice|9. ML Practice §3]]).
> - **Why it matters**: shift invariance is why the $C$ logits have only $C-1$ degrees of freedom, why a "logit bias" column can be dropped without changing anything, and why two papers reporting different logits can describe the identical classifier.

> **Cross-entropy loss, defined.** The **cross-entropy loss** is a *scalar function of a predicted distribution and a target distribution* — it scores a distribution, not a decision, which is why it is not accuracy. Three defining conditions. It is the **negative log-likelihood of the target under the prediction**, so minimising it is maximum likelihood. It is **asymmetric** in its two arguments: $H(y,p)\ne H(p,y)$, and it is $p$ that is being trained. And it is **unbounded above** — a confident wrong answer costs arbitrarily much, while a confident right answer saves at most what it already had.
>
> $$L=-\sum_{i=1}^{C}y_i\log p_i\ \ \xrightarrow{\ y\text{ one-hot at }c\ }\ \ L=-\log p_c$$
>
> where $y$ is the target distribution (one-hot at the true class $c$ in every case on this page), $p$ the softmax output, and $C$ the number of classes — and the sum collapses to a single term **because** a one-hot $y$ zeroes every $i\ne c$.
>
> - **Example**: D1 with target class 1 costs $-\log 0.731059=0.313262$ nats. Base $e$ gives nats, base 2 gives bits, and $0.313262/\log 2=0.451941$ bits is the same number in the other unit.
> - **Non-example**: accuracy. D1's prediction is *correct* — class 1 has the larger probability — while its loss is a positive 0.313. Loss can rise while accuracy is unchanged, which is why a paper must report both and why early stopping on one is not early stopping on the other.
> - **Non-example**: the entropy of the prediction. $H(p)=0.582 \text{ nats}$ here, which is not the loss; entropy measures how spread the prediction is, cross-entropy measures how much of its mass sits on the truth. The full relation, $H(y,p)=H(y)+D_{\mathrm{KL}}(y\Vert p)$, is [[02-foundations/information-theory|5. Information Theory §2]].
> - **Why it matters**: the unboundedness above is the source of most training instability that is blamed on the optimizer. One mislabelled sample with a confident prediction can contribute more loss than a hundred correct ones, and $\lVert\partial L/\partial s\rVert$ is bounded by $\sqrt2$ only because of the softmax in front of it.

### 2. One update is not a training result

For one-hot target $y$, softmax plus cross-entropy gives the useful derivative

$$\frac{\partial L}{\partial s}=p-y.$$

Here it is $(-0.269,0.269)$: raise the correct logit and lower the other. Backpropagating this vector computes gradients; the optimizer converts them into an update. SGD, momentum, and Adam therefore change the *update rule*, not the model's forward definition. The chain that carries $p-y$ back to $W_1$ is worked in full in the Worked case above, and the general machinery is [[02-foundations/calculus-backprop|2. Calculus & Backprop §3]].

Why that derivative is so clean is worth one line, because it is the reason the two blocks are drawn as one. The softmax Jacobian is $\partial p_i/\partial s_j=p_i(\delta_{ij}-p_j)$ and the loss derivative is $\partial L/\partial p_i=-y_i/p_i$; multiplying them makes every $p_i$ cancel and leaves $p-y$. Neither factor is pleasant on its own and their product is a subtraction, which is why implementations fuse the two and why a framework that lets you apply softmax twice by accident will train, slowly and wrongly, without ever raising an error.

> **The SGD step and its learning rate, defined.** A **gradient-descent step** is an *update rule applied to the parameter vector* — a map $\theta\mapsto\theta'$, not a loss and not a direction. Three defining conditions. It moves **against the gradient of the loss it was given**, so what it descends is whatever objective the gradient came from (with weight decay, not the cross-entropy). It has a **step size $\eta$ chosen outside the derivative**, which is what makes $\eta$ a hyperparameter. And it is **a local statement only**: the guarantee $L(\theta')<L(\theta)$ holds for small enough $\eta$ and for no particular $\eta$ you happen to choose.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta},\qquad L(\theta')\approx L(\theta)-\eta\lVert g\rVert^2+\tfrac{\eta^2}{2}g^\top Hg$$
>
> where $g=\partial L/\partial\theta$, $H$ is the Hessian at $\theta$, and the second-order term is why the descent stops being descent: on a quadratic, the step reduces the loss only while $\eta<2/\lambda_{\max}(H)$, since above that the $\eta^2$ term outgrows the $\eta$ term.
>
> - **Example**: D1 at $\eta=0.1$ predicts $\Delta L\approx-\eta\lVert g\rVert^2=-0.159125$ and delivers $-0.129177$. The shortfall is the $\eta^2$ term, still small.
> - **Non-example**: "SGD" with the full dataset in one batch, which is what this page runs. Stochastic gradient descent means the gradient is a *sample estimate*; D1 has one sample, so every gradient here is exact and none of the noise arguments about SGD apply. A paper calling full-batch descent "SGD" is not wrong in code and is wrong in its analysis.
> - **Non-example**: Adam. It is not this rule with a different $\eta$ — it rescales each coordinate by a running second moment, so its effective per-coordinate step is not $\eta$ and the $2/\lambda_{\max}$ bound does not transfer. Comparing "the same learning rate" across optimizers compares nothing.
> - **Why it matters**: $2/\lambda_{\max}(H)$ is a *measurable* number, not a rule of thumb, and §6 measures it on D1 and finds it to four significant figures. The optimizer families are [[02-foundations/optimization|4. Optimization §3]].

### 3. Training, validation, and test answer different questions

- training loss: can the parameters fit sampled training batches?
- validation metric: which checkpoint or hyperparameter should be selected?
- test metric: how did the already frozen decision perform on held-out data?

Repeated test-guided tuning leaks test information. A paper that reports its best seed without a predeclared selection rule estimates luck as well as method quality. The split discipline itself, including what counts as a leak, is [[02-foundations/ml-practice|9. ML Practice §1]].

### 4. Regularization and scaling are claims with controls

Weight decay, augmentation, dropout, early stopping, more data, and more compute can all improve a result through different mechanisms. A scaling claim needs axes—parameters, data, compute—and a controlled comparison. “Our larger model is better” does not identify which axis caused the gain.

Of those, weight decay is the one §6 needs, so it gets a definition rather than a name in a list.

> **Weight decay, defined.** **Weight decay** is a *term added to the objective* — it changes what is being minimised, so it is not a trick applied to the update afterwards. Three defining conditions. It penalises the **squared norm of the parameters**, which is a choice: it prefers many small weights to one large one, and it has no opinion about the data. It is applied to **parameters, not activations**, so it shrinks $W_1$ and $W_2$ and never touches $h$. And it is **scaled by a coefficient $\lambda$ chosen outside gradient descent**, so a paper reporting "weight decay" without $\lambda$ has reported nothing.
>
> $$L_{\lambda}(\theta)=L(\theta)+\frac{\lambda}{2}\lVert\theta\rVert^2,\qquad \frac{\partial L_\lambda}{\partial\theta}=\frac{\partial L}{\partial\theta}+\lambda\theta$$
>
> where $\lVert\theta\rVert^2$ sums the squares of all 12 of D1's weights and $\lambda\ge0$ is the coefficient — so the gradient gains a term pointing straight at the origin, and every step multiplies the parameters by $(1-\eta\lambda)$ before the data has any say.
>
> - **Example**: D1 at $\lambda=0.1$ starts from $L_\lambda=0.313262+\tfrac{0.1}{2}\cdot5=0.563262$, since $\lVert W_1\rVert^2=3$ and $\lVert W_2\rVert^2=2$.
> - **Non-example**: the $(1-\eta\lambda)$ multiplier applied *after* an Adam update ("decoupled" weight decay). That is a different algorithm with a different minimiser, not an implementation detail, which is why the two are named differently in the literature.
> - **Non-example**: early stopping. Both shrink the effective capacity, but early stopping changes *when you stop*, leaving the objective alone; weight decay changes *what you are minimising*, so it moves the minimum itself. §6 uses that: it is the decay that gives D1 a minimum to overshoot.
> - **Why it matters**: cross-entropy on one separable point has **no** minimiser — the loss falls monotonically as the logits run to infinity — so no learning rate can be "too large" for it and a step-size sweep on it measures nothing. Adding $\lambda$ gives the objective a floor at a finite $\theta^\ast$, and only then does a stability boundary exist. Regularization as an umbrella term is [[02-foundations/ml-practice|9. ML Practice §2]].

### 5. How to read a training recipe

Extract: data mixture and split; preprocessing; initialization; objective and coefficients; optimizer and schedule; batch size and number of updates; precision and hardware; checkpoint selection; seeds and uncertainty. Then ask which choices are essential by reading ablations. This is the operational bridge to [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]], and [[01-canonical-papers/notes/1-foundations/adam|Adam]].

### 6. The lab: the step size has a boundary, and it is measurable

Everything above is one step. The question a hand calculation cannot answer is which step sizes can be repeated, so this section runs the same D1 in a loop. Part 1 of the listing reproduces the Worked case exactly — if your arithmetic disagrees with it, fix that before reading the table. Part 2 adds the $\lambda=0.1$ decay of §4, because without it the objective has no minimum and every step size looks equally good. Part 3 asks where the boundary in the table comes from.

```python
# D1: forward, backward, one SGD step, then the step-size sweep. NumPy only.
import numpy as np

W1 = np.array(((1., 0.), (0., 1.), (1., 0.)))      # 3x2
W2 = np.array(((0., 1., 0.), (1., 0., 0.)))        # 2x3
x, y = np.array((1., 2.)), np.array((1., 0.))      # input, one-hot target (class 1)

def forward(A, B):
    z = A @ x                                      # pre-activation
    h = np.maximum(z, 0.0)                         # ReLU
    s = B @ h                                      # logits
    e = np.exp(s - s.max())                        # shift-stabilised softmax
    return z, h, s, e / e.sum()

def loss_grads(A, B, lam):
    z, h, s, p = forward(A, B)
    gs  = p - y                                    # dL/ds, softmax + cross-entropy
    gW2 = np.outer(gs, h) + lam * B
    gz  = (B.T @ gs) * (z > 0)                     # back through W2, then the ReLU mask
    gW1 = np.outer(gz, x) + lam * A
    ce  = -np.log(np.clip(p[y.argmax()], 1e-300, None))
    return ce + 0.5*lam*((A**2).sum() + (B**2).sum()), gW1, gW2, (z, h, s, p, gs, gz, ce)

# --- 1. the worked case: forward, backward, one step, no weight decay -------
L0, gW1, gW2, (z, h, s, p, gs, gz, ce0) = loss_grads(W1, W2, 0.0)
print("z", z, " h", h, " s", s, " p", np.round(p, 6), " L", round(ce0, 6))
print("dL/ds", np.round(gs, 6), "  dL/dz", np.round(gz, 6))
print("dL/dW1\n", np.round(gW1, 6), "\ndL/dW2\n", np.round(gW2, 6))
A, B = W1 - 0.1*gW1, W2 - 0.1*gW2
print("after one step at eta=0.1:  s", np.round(forward(A, B)[2], 6),
      " p", np.round(forward(A, B)[3], 6), " L", round(loss_grads(A, B, 0.0)[0], 6))
print("first-order prediction -eta*||g||^2 =",
      round(-0.1*((gW1**2).sum() + (gW2**2).sum()), 6))

# --- 2. the sweep, with the weight decay of section 4 (lam = 0.1) ----------
def run(eta, steps=200, lam=0.1):
    A, B = W1.copy(), W2.copy()
    for k in range(steps):
        L, gA, gB, _ = loss_grads(A, B, lam)
        if not np.isfinite(L) or L > 1e12:
            return None, k                                     # diverged
        A, B = A - eta*gA, B - eta*gB
    L, _, _, (_, h, _, p, _, _, _) = loss_grads(A, B, lam)
    return (L, float(p[0]), int((h <= 0).sum())), None

for eta in (0.01, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0, 12.0, 20.0):
    out, blew = run(eta)
    print("eta=%-5g" % eta, "diverged at step %d" % blew if out is None
          else "L=%.6f  p1=%.4f  dead units=%d" % out)

# --- 3. where the sharp boundary comes from, and where there is none -------
t = np.concatenate([W1.ravel(), W2.ravel()])
def g(t): return np.concatenate([q.ravel() for q in loss_grads(t[:6].reshape(3, 2), t[6:].reshape(2, 3), 0.1)[1:3]])
for _ in range(200000): t = t - 0.02*g(t)                      # walk to the minimum
H = np.array([(g(t + 1e-5*e) - g(t - 1e-5*e))/2e-5 for e in np.eye(12)])
lmax = np.linalg.eigvalsh(0.5*(H + H.T))[-1]
print("L* = %.6f   lambda_max = %.4f   2/lambda_max = %.4f"
      % (loss_grads(t[:6].reshape(3, 2), t[6:].reshape(2, 3), 0.1)[0], lmax, 2/lmax))
grid = np.arange(10.40, 10.61, 0.0005)
flag = [run(e)[1] is not None for e in grid]
print("first eta that diverges: %.4f ; of the %d grid points above it, %d still survive"
      % (grid[flag.index(True)], len(flag) - flag.index(True), sum(not f for f in flag[flag.index(True):])))
```

**The sweep.** Two hundred full-batch steps from the catalog $W_1,W_2$, objective $L_\lambda=$ cross-entropy $+\ 0.05\lVert\theta\rVert^2$, which starts at $L_\lambda=0.563262$. "Dead units" counts hidden units with $h_i=0$ at the end, out of 3.

| $\eta$ | $L_\lambda$ after 200 steps | $p_1$ | dead units | what happened |
|---:|---:|---:|---:|---|
| $0.01$ | $0.255664$ | $0.9657$ | 0 | still descending; 200 steps was not enough |
| $0.1$ | $0.143118$ | $0.9684$ | 1 | nearly there |
| $0.5$ | $0.140339$ | $0.9684$ | 1 | at the minimum |
| $1$ | $0.140339$ | $0.9684$ | 1 | at the minimum |
| $2$ | $0.140339$ | $0.9684$ | 1 | at the minimum |
| $3$ | $0.140345$ | $0.9678$ | 1 | at the edge, $2/\lambda_{\max}=3.0179$ |
| $5$ | $0.149517$ | $0.9867$ | 1 | oscillating above the minimum |
| $8$ | $0.599431$ | $1.0000$ | 1 | cross-entropy 0, norm large: bouncing |
| $10$ | $0.693147$ | $0.5000$ | 3 | collapsed; $\log 2$ is the give-up loss |
| $12$ | diverged at step 15 | — | — | overflow |
| $20$ | diverged at step 9 | — | — | overflow |

**Reading the sweep.** Four things the hand derivation could not have told you.

- **The useful boundary is the settling boundary, and it is exactly $2/\lambda_{\max}$.** Rows $0.5$ through $2$ land on $L^\ast=0.140339$ to six figures; row $3$ misses it in the sixth. Part 3 of the listing walks to $\theta^\ast$, builds the $12\times12$ Hessian by finite differences and reports $\lambda_{\max}=0.6627$, hence $2/\lambda_{\max}=3.0179$. Bisecting the loop for the largest $\eta$ that still settles gives $3.0180$. The textbook condition is not an approximation here; it is the measurement, to four significant figures.
- **Above that boundary the failure is silent before it is loud.** At $\eta=8$ the cross-entropy is zero — the model is *perfect* on its one training point — while $L_\lambda=0.599431$, four times the minimum, because the weights have been thrown far from the origin. A run monitored on accuracy alone shows nothing wrong. At $\eta=10$ all three hidden units are dead, $p=(0.5,0.5)$, and the loss sits at exactly $\log 2=0.693147$: every weight has been decayed to zero and the network predicts the prior. That number is worth recognising on sight, because a two-class run stuck at $0.693$ has not converged, it has given up.
- **One unit dies on purpose, and that is not the bug.** Every row from $\eta=0.1$ to $\eta=8$ ends with one dead unit, and so does the minimum itself: $\theta^\ast$ has $W_1$'s first row and $W_2$'s first column at zero. The backward pass wanted to push hidden unit 1 down ($\partial L/\partial z_1=+0.268941$) and the decay finished the job. Weight decay prunes; three dead units is collapse, one is the objective doing what it was asked.
- **The overflow boundary is not a boundary at all.** It is tempting to report the divergence threshold the way the settling threshold was reported. Part 3 scans $\eta$ from $10.40$ to $10.6095$ in steps of $0.0005$: the first divergence is at $\eta=10.4015$, and of the 417 grid points at or above it, 285 still survive 200 steps. Past the stability limit the iterate bounces across the ReLU kinks and whether it escapes is not monotone in $\eta$. A paper quoting "training diverges above $\eta=10.4$" on a plot of this kind is quoting one grid.

### Self-check

1. Which of $W_2$, $h$, $\eta$, $\lambda$, and the ReLU mask are parameters, which activations, which hyperparameters?
2. Why do implementations fuse softmax and cross-entropy into one block?
3. D1's $\partial L/\partial h$ has a zero third entry. Which number in the object caused it, and does a better prediction change it?
4. A two-class training run flatlines at loss $0.693$. What is the single most likely diagnosis, and what would confirm it?
5. Why does a learning-rate sweep on plain cross-entropy over one separable sample teach nothing about stability?

> [!tip]- Answers
> 1. Parameters: $W_2$ (and $W_1$). Activation: $h$. Hyperparameters: $\eta$ and $\lambda$. The ReLU mask is none of them — it is derived from the sample, so it is an activation in the memory sense and a *choice of nobody*.
> 2. Their Jacobians are ugly separately — $p_i(\delta_{ij}-p_j)$ and $-y_i/p_i$ — and their product cancels to $p-y$. Fusing also avoids taking $\log$ of an underflowed probability.
> 3. $W_2$'s third column is $(0,0)$, so hidden unit 3 feeds nothing. It stays zero for every prediction, right or wrong: the gradient is a property of the wiring, not of the error.
> 4. The model is predicting the class prior and learning nothing: $\log 2=0.693147$ is the loss of $p=(0.5,0.5)$. Confirm by printing the logits — if $s_1\approx s_2$ with tiny weights, the step size collapsed the network (the $\eta=10$ row); if the weights are large and $s$ is still flat, the wiring is broken.
> 5. That objective has no minimiser: the logits can run to infinity and the loss falls monotonically for every $\eta$ in the table. There is no minimum to overshoot, so nothing in the sweep can be unstable. Weight decay supplies the floor (§4).

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and [[03-deep-learning/lab-objects|0. Lab Objects]]. The object is D1 throughout; questions 2 and 4 change the target class, so none of the page's numbers can be copied.

1. **Draw.** Draw D1 with batch shapes for $B=4$ and count weights including biases. Add the backward arrows of the Homework diagram and mark which one is blocked by the ReLU mask and which one is blocked by a zero column of $W_2$.
2. **Derive.** For logits $(0,\log 3)$ and target class 1, compute probabilities, loss, and $p-y$.
3. **Interpret.** Validation improves while test performance is repeatedly inspected and used to alter augmentation. Which boundary was crossed?
4. **Do.** Fill the `?` blanks, then re-run the lab with the target changed to **class 2** ($y=(0,1)$, so the catalog model starts *wrong*) and the decay raised to $\lambda=0.2$. Report (a) the starting $L_\lambda$; (b) the sweep over $\eta\in\{0.05,0.5,2,5,20\}$ at 200 steps, as a table of $L_\lambda$, dead units, and any divergence step; (c) the largest $\eta$ that still settles at the minimum, by bisection. Then say in one sentence why that boundary moved relative to the $\lambda=0.1$ run in §6.

```python
# D1 with the target flipped to class 2 and a heavier decay. Fill ?.
import numpy as np
W1 = np.array(((1., 0.), (0., 1.), (1., 0.)))
W2 = np.array(((0., 1., 0.), (1., 0., 0.)))
x   = np.array((1., 2.))
y   = ?                                     # one-hot target for class 2
lam = ?                                     # 0.2

def loss_grads(A, B):
    z = A @ x
    h = ?                                   # ReLU of z
    s = B @ h
    e = np.exp(s - s.max()); p = e / e.sum()
    gs  = ?                                 # dL/ds for softmax + cross-entropy
    gW2 = np.outer(gs, h) + lam * B
    gz  = ?                                 # (B.T @ gs) masked by the pre-activation sign
    gW1 = np.outer(gz, x) + lam * A
    ce  = -np.log(np.clip(p[y.argmax()], 1e-300, None))
    return ce + 0.5*lam*((A**2).sum() + (B**2).sum()), gW1, gW2, h, p

print("L at step 0:", round(loss_grads(W1, W2)[0], 6))
def run(eta, steps=200):
    A, B = W1.copy(), W2.copy()
    for k in range(steps):
        L, gA, gB, _, _ = loss_grads(A, B)
        if not np.isfinite(L) or L > 1e12:
            return None, k
        A, B = A - eta*gA, B - eta*gB
    L, _, _, h, p = loss_grads(A, B)
    return (L, int((h <= 0).sum())), None
for eta in (0.05, 0.5, 2.0, 5.0, 20.0):
    out, blew = run(eta)
    print("eta=%-5g" % eta, "diverged at step %d" % blew if out is None
          else "L=%.6f  dead units=%d" % out)
lo, hi = 0.1, 30.0                          # bisection for the settling boundary
for _ in range(60):
    mid = 0.5*(lo + hi)
    out, _ = run(mid, 4000)
    ok = out is not None and abs(out[0] - ?) < 1e-5      # the minimum from the eta=0.5 row
    lo, hi = (mid, hi) if ok else (lo, mid)
print("largest eta that settles: %.4f" % hi)
```

> [!tip]- Solutions
> 1. $X:4\times2$, $H:4\times3$, $S:4\times2$; parameters $(2\cdot3+3)+(3\cdot2+2)=17$. On the backward arrows: $\partial L/\partial z=\partial L/\partial h\odot\mathbf 1[z>0]$ is the masked one, and $\partial L/\partial h_3=0$ is blocked by $W_2$'s zero third column — a different mechanism, permanent rather than sample-dependent.
> 2. $p=(1/4,3/4)$, $L=-\log(1/4)=1.386$, $p-y=(-3/4,3/4)$.
> 3. The test set became part of model selection; the reported test result is no longer an untouched estimate.
> 4. Blanks: `y = np.array((0., 1.))`, `lam = 0.2`, `h = np.maximum(z, 0.0)`, `gs = p - y`, `gz = (B.T @ gs) * (z > 0)`, and `abs(out[0] - 0.235806)`. (a) $L_\lambda=1.313262+0.5\cdot0.2\cdot5=1.813262$, since the catalog model puts only $p_2=0.268941$ on the new target. (b) The sweep:
>
>    | $\eta$ | $L_\lambda$ after 200 | dead units |
>    |---:|---:|---:|
>    | $0.05$ | $0.240870$ | 0 |
>    | $0.5$ | $0.235806$ | 1 |
>    | $2$ | $0.238924$ | 1 |
>    | $5$ | $0.693147$ | 3 |
>    | $20$ | diverged at step 6 | — |
>
>    (c) Bisection gives $1.9801$, and $L^\ast=0.235806$. It moved **down** from $3.0180$: doubling $\lambda$ adds $\lambda$ to the curvature in every direction, so $\lambda_{\max}$ of the Hessian at the new minimum is larger and $2/\lambda_{\max}$ is smaller. Heavier regularization is not a free way to stabilise training — it buys a floor for the loss and pays for it with a tighter step-size ceiling. The $\eta=5$ row is the same $\log 2$ collapse as §6, reached sooner.

## 한국어

> [!note] 처음이라면
> §1–4와 문제 1–2를 먼저 한다. §6을 열기 전에 계산 절을 손으로 끝낸다. 실습은 손계산을 검산하는 것이지 대신하는 것이 아니다. 논문의 학습 절을 비교할 때 §5로 돌아온다.

### 계속 쓰는 대상: D1

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D1**을 쓴다. bias는 0이다.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}.$$

순전파: $W_1x=(1,2,1)$, $h=\operatorname{ReLU}(W_1x)=(1,2,1)$, $s=W_2h=(2,1)$, $p=\operatorname{softmax}(s)$. 그림에 $2\rightarrow3\rightarrow2$ shape를 적는다. **P1**($2\to3\to1$ MSE)과 다른 장치다.

이 페이지에서 정답은 항상 1번 클래스이므로 $y=(1,0)$이고, 아래의 모든 숫자는 이 다섯 개의 대상만으로 나온다.

*범위: 이 페이지는 입력 하나에서 파라미터 갱신 하나까지의 형식 붙은 경로 — shape, softmax, cross-entropy, 역전파, SGD 한 스텝, 그리고 그 스텝이 지켜야 하는 보폭 — 와 학습 주장이 갖춰야 할 증거를 가르친다. 미분이 어디서 오는지는 가르치지 않는다. 그것은 [[02-foundations/calculus-backprop|2. 미적분과 역전파 §2]]다. optimizer 자체(momentum, Adam, schedule)도 아니다. 그것은 [[02-foundations/optimization|4. 최적화 §3]]다. 숫자를 결과로 바꾸는 실험 절차도 아니다. 그것은 [[02-foundations/ml-practice|9. ML 실무 §4]]다. 2층 MLP 너머의 구조도 아니다. convolution과 patch token은 [[03-deep-learning/computer-vision/index|2. 컴퓨터비전]], attention은 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]]와 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]다.*

### 과제가 그릴 그림

그림 하나이고, 과제가 요구하는 것이 정확히 이 그림이다. 순방향과 역방향을 한 장에 함께 그린다. 그림은 아래 계산 절을 카탈로그 숫자로 그린 것이고, 문제 1은 같은 그림을 $B=4$의 배치 shape로 요구한다.

<svg viewBox="0 0 560 518" style="max-width:100%;height:auto" role="img" aria-label="D1의 순전파를 왼쪽 열에 텐서마다 shape와 값을 달아 내려 그리고, 가운데에 가중치와 0인 bias를, 오른쪽 열에 gradient 값을 단 역전파를 올려 그린 그림">
  <defs><marker id="aD1k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="22" font-size="12" fill="currentColor">D1 · 정답 1번 클래스, y = (1, 0) · 실선: 순전파 · 점선: 역전파</text>
  <text x="75" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">순전파 · activation</text>
  <text x="265" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">파라미터 · bias는 있고 0</text>
  <text x="469" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">역전파 · gradient</text>
  <line x1="144" y1="34" x2="144" y2="390" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 4"/>
  <line x1="385" y1="34" x2="385" y2="390" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 4"/>
  <rect x="12" y="49" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="63" font-size="11" fill="currentColor" text-anchor="middle">x · 2</text>
  <text x="75" y="78" font-size="11" fill="currentColor" text-anchor="middle">(1, 2)</text>
  <rect x="12" y="153" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="167" font-size="11" fill="currentColor" text-anchor="middle">z · 3</text>
  <text x="75" y="182" font-size="11" fill="currentColor" text-anchor="middle">(1, 2, 1)</text>
  <rect x="12" y="241" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="255" font-size="11" fill="currentColor" text-anchor="middle">h · 3</text>
  <text x="75" y="270" font-size="11" fill="currentColor" text-anchor="middle">(1, 2, 1)</text>
  <rect x="12" y="349" width="126" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="363" font-size="11" fill="currentColor" text-anchor="middle">s · 2</text>
  <text x="75" y="378" font-size="11" fill="currentColor" text-anchor="middle">(2, 1)</text>
  <line x1="75" y1="83" x2="75" y2="107" stroke="currentColor" stroke-width="1.4"/>
  <line x1="75" y1="129" x2="75" y2="152" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1k)"/>
  <line x1="75" y1="275" x2="75" y2="301" stroke="currentColor" stroke-width="1.4"/>
  <line x1="75" y1="323" x2="75" y2="348" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1k)"/>
  <rect x="31" y="107" width="88" height="22" rx="11" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="122" font-size="11" fill="currentColor" text-anchor="middle">W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">x + b</tspan><tspan dy="3" font-size="10">1</tspan></text>
  <rect x="31" y="301" width="88" height="22" rx="11" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="316" font-size="11" fill="currentColor" text-anchor="middle">W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3">h + b</tspan><tspan dy="3" font-size="10">2</tspan></text>
  <line x1="75" y1="187" x2="75" y2="205" stroke="currentColor" stroke-width="1.4"/>
  <rect x="35" y="205" width="80" height="18" stroke="currentColor" stroke-width="1.6" fill="currentColor" fill-opacity="0.1"/>
  <text x="75" y="218" font-size="11" fill="currentColor" text-anchor="middle">ReLU 게이트</text>
  <line x1="75" y1="223" x2="75" y2="240" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1k)"/>
  <line x1="75" y1="383" x2="75" y2="397" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1k)"/>
  <rect x="12" y="397" width="536" height="26" rx="5" stroke="currentColor" stroke-width="1.6" fill="currentColor" fill-opacity="0.07"/>
  <text x="265" y="414" font-size="11.5" fill="currentColor" text-anchor="middle">softmax + cross-entropy · 한 블록</text>
  <line x1="75" y1="423" x2="75" y2="433" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1k)"/>
  <rect x="12" y="434" width="126" height="54" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="75" y="449" font-size="11" fill="currentColor" text-anchor="middle">p · 2</text>
  <text x="75" y="465" font-size="11" fill="currentColor" text-anchor="middle">p<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= 0.731059</tspan></text>
  <text x="75" y="481" font-size="11" fill="currentColor" text-anchor="middle">p<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= 0.268941</tspan></text>
  <line x1="265" y1="423" x2="265" y2="444" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD1k)"/>
  <rect x="177" y="445" width="176" height="24" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="265" y="461" font-size="11" fill="currentColor" text-anchor="middle">L · 스칼라 = 0.313262 nat</text>
  <text x="152" y="70" font-size="11" fill="currentColor">W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">· 3×2</tspan></text>
  <text x="176" y="87" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="196" y="87" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="176" y="101" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="196" y="101" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="176" y="115" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="196" y="115" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M158 76 L154 76 L154 119 L158 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M196 76 L200 76 L200 119 L196 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="220" y="70" font-size="11" fill="currentColor">b<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">· 3 = 0</tspan></text>
  <text x="242" y="87" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="242" y="101" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="242" y="115" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M224 76 L220 76 L220 119 L224 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M242 76 L246 76 L246 119 L242 119" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="152" y="142" font-size="11" fill="currentColor">∂L/∂W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= (∂L/∂z) x</tspan><tspan dy="-4" font-size="10">T</tspan><tspan dy="4" dx="3.5">· 3×2</tspan></text>
  <text x="224" y="159" font-size="11" fill="currentColor" text-anchor="end">0.268941</text>
  <text x="292" y="159" font-size="11" fill="currentColor" text-anchor="end">0.537883</text>
  <text x="224" y="173" font-size="11" fill="currentColor" text-anchor="end">−0.268941</text>
  <text x="292" y="173" font-size="11" fill="currentColor" text-anchor="end">−0.537883</text>
  <text x="224" y="187" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="292" y="187" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M158 148 L154 148 L154 191 L158 191" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M292 148 L296 148 L296 191 L292 191" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <line x1="151" y1="97" x2="121" y2="116" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD1k)"/>
  <text x="152" y="258" font-size="11" fill="currentColor">W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">· 2×3</tspan></text>
  <text x="176" y="275" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="196" y="275" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="216" y="275" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="176" y="289" font-size="11" fill="currentColor" text-anchor="end">1</text>
  <text x="196" y="289" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="216" y="289" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M158 264 L154 264 L154 293 L158 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M216 264 L220 264 L220 293 L216 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="240" y="258" font-size="11" fill="currentColor">b<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">· 2 = 0</tspan></text>
  <text x="262" y="275" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <text x="262" y="289" font-size="11" fill="currentColor" text-anchor="end">0</text>
  <path d="M244 264 L240 264 L240 293 L244 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M262 264 L266 264 L266 293 L262 293" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <text x="152" y="318" font-size="11" fill="currentColor">∂L/∂W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= (p − y) h</tspan><tspan dy="-4" font-size="10">T</tspan><tspan dy="4" dx="3.5">· 2×3</tspan></text>
  <text x="224" y="335" font-size="11" fill="currentColor" text-anchor="end">−0.268941</text>
  <text x="292" y="335" font-size="11" fill="currentColor" text-anchor="end">−0.537883</text>
  <text x="360" y="335" font-size="11" fill="currentColor" text-anchor="end">−0.268941</text>
  <text x="224" y="349" font-size="11" fill="currentColor" text-anchor="end">0.268941</text>
  <text x="292" y="349" font-size="11" fill="currentColor" text-anchor="end">0.537883</text>
  <text x="360" y="349" font-size="11" fill="currentColor" text-anchor="end">0.268941</text>
  <path d="M158 324 L154 324 L154 353 L158 353" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <path d="M360 324 L364 324 L364 353 L360 353" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.8" stroke-linejoin="round"/>
  <line x1="151" y1="279" x2="121" y2="310" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD1k)"/>
  <rect x="390" y="349" width="158" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="363" font-size="11" fill="currentColor" text-anchor="middle">∂L/∂s = p − y · 2</text>
  <text x="469" y="378" font-size="11" fill="currentColor" text-anchor="middle">(−0.268941, 0.268941)</text>
  <rect x="390" y="241" width="158" height="52" rx="4" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="255" font-size="11" fill="currentColor" text-anchor="middle">∂L/∂h = W<tspan dy="3" font-size="10">2</tspan><tspan dy="-7" font-size="10">T</tspan><tspan dy="4">(p − y) · 3</tspan></text>
  <text x="469" y="270" font-size="11" fill="currentColor" text-anchor="middle">(0.268941, −0.268941, 0)</text>
  <text x="469" y="286" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">0: W<tspan dy="3" font-size="10">2</tspan><tspan dy="-3">의 3열이 (0, 0)</tspan></text>
  <rect x="390" y="153" width="158" height="34" rx="4" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="167" font-size="11" fill="currentColor" text-anchor="middle">∂L/∂z · 3</text>
  <text x="469" y="182" font-size="11" fill="currentColor" text-anchor="middle">(0.268941, −0.268941, 0)</text>
  <line x1="469" y1="397" x2="469" y2="384" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#aD1k)"/>
  <line x1="469" y1="349" x2="469" y2="294" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#aD1k)"/>
  <text x="475" y="326" font-size="11" fill="currentColor" fill-opacity="0.85">× W<tspan dy="3" font-size="10">2</tspan><tspan dy="-7" font-size="10">T</tspan></text>
  <line x1="389" y1="358" x2="369" y2="342" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#aD1k)"/>
  <line x1="469" y1="241" x2="469" y2="223" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>
  <rect x="415" y="205" width="108" height="18" rx="9" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3"/>
  <text x="469" y="218" font-size="11" fill="currentColor" text-anchor="middle">⊙ mask (1, 1, 1)</text>
  <line x1="469" y1="205" x2="469" y2="188" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#aD1k)"/>
  <line x1="117" y1="214" x2="413" y2="214" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="1 3"/>
  <text x="265" y="210" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.9">mask 1[z &gt; 0] = (1, 1, 1)</text>
  <text x="265" y="227" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">z에서 읽고 역전파 전에 고정</text>
  <line x1="389" y1="166" x2="301" y2="168" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#aD1k)"/>
  <text x="12" y="502" font-size="11" fill="currentColor" fill-opacity="0.9">L에서 W<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">으로 가는 화살표는 없다. gradient는 W</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">와 mask를 지나야만 닿는다.</tspan></text>
</svg>

그림이 맞혀야 할 것이 다섯이고, 각각이 계산에 대한 주장이다.
**모든 텐서에 shape를 적는다** — $x$(2), $z$(3), $h$(3), $s$(2), $p$(2), $L$(스칼라). 이름 없는 화살표가 shape 오류가 숨는 자리이고, shape 오류는 재구현이 조용히 다른 모델을 학습시키는 가장 흔한 이유다.
**ReLU는 $h$가 아니라 $z$에 걸린 게이트로 그린다.** mask는 $\mathbf 1[z>0]$이다. 활성화 *이전* 값에서 읽고, 이 샘플에 대해 gradient가 흐르기 전에 이미 고정된다. $h$ 뒤에 그리면 역전파가 mask를 고를 수 있다는 주장이 되는데 그렇지 않다.
**softmax와 cross-entropy는 한 블록으로 그린다.** 따로 두면 각각의 Jacobian이 지저분하지만 합치면 $p-y$만 남는다(§2). 그 식이 나타나는 자리는 이 블록의 출력 화살표뿐이다.
**$L$에서 $W_1$으로 바로 가는 화살표는 없다.** gradient는 $W_2$를 지나고 mask를 지나야만 $W_1$에 닿는다. 그 경로가 역전파의 전부이고, 지름길이 있는 그림은 다른 알고리즘의 그림이다.
**bias를 그리고 0이라고 적는다.** D1은 bias를 0으로 고정한다. 문제 1의 파라미터 수는 그래도 bias를 센다. "없다"와 "있는데 0이다"의 차이가 정확히 12와 17을 가르는 다섯 개의 숫자다.

### 대상으로 한 번 끝까지

이것이 과제의 대상이다. 과제가 요구하는 세 가지 — 순전파, 역전파, 한 스텝 — 를 카탈로그 숫자로 여기서 먼저 한다. 그러면 과제는 정답 클래스와 손잡이를 바꾸는 일이지 첫 유도가 아니다. 이 페이지의 로그는 전부 자연로그이므로 loss의 단위는 nat이다.

**순전파.** 기호, 대입, 숫자 순으로:

$$z=W_1x=(1,2,1),\qquad h=\operatorname{ReLU}(z)=(1,2,1),\qquad s=W_2h=(2,1).$$

세 pre-activation이 모두 양수이므로 ReLU mask는 $\mathbf 1[z>0]=(1,1,1)$이고 이 샘플에서는 잘리는 값이 없다. softmax와 loss는

$$p_1=\frac{e^2}{e^2+e^1}=0.731059,\qquad p_2=0.268941,\qquad L=-\log p_1=0.313262\ \text{nat}.$$

**역전파.** 외울 가치가 있는 미분은 $\partial L/\partial s=p-y$ 하나다(§2의 유도). 그러므로

$$\frac{\partial L}{\partial s}=(0.731059-1,\ 0.268941-0)=(-0.268941,\ 0.268941).$$

이 벡터를 두 행렬로 되돌린다. $\partial L/\partial W_2=(p-y)h^\top$이 외적이므로

$$\frac{\partial L}{\partial W_2}=\begin{pmatrix}-0.268941&-0.537883&-0.268941\\0.268941&0.537883&0.268941\end{pmatrix},$$

가운데 열이 나머지의 두 배인데 $h_2=2$이기 때문이다. 두 배로 활성화된 은닉 유닛이 두 배의 책임을 진다. 계속 되돌리면

$$\frac{\partial L}{\partial h}=W_2^\top(p-y)=(0.268941,\ -0.268941,\ 0),$$

세 번째 성분이 정확히 0인데 $W_2$의 세 번째 열이 $(0,0)$이기 때문이다. 은닉 유닛 3은 아무 데도 연결되어 있지 않아서, 예측이 아무리 틀려도 이 샘플에서 아무것도 배우지 않는다. mask(여기서는 전부 1)를 걸고 $x=(1,2)$와 한 번 더 외적하면

$$\frac{\partial L}{\partial W_1}=\begin{pmatrix}0.268941&0.537883\\-0.268941&-0.537883\\0&0\end{pmatrix}.$$

**SGD 한 스텝.** 규칙은 $\theta\leftarrow\theta-\eta\,\partial L/\partial\theta$다. $\eta=0.1$이면 logit이 $s=(2.299452,\ 0.700548)$로 옮겨 가는데, $\pm0.299452$로 대칭인 이유는 두 클래스에서 $p-y$가 반대칭이기 때문이다. 그리고

$$p=(0.831865,\ 0.168135),\qquad L=0.184085,\qquad \Delta L=-0.129177\ \text{nat}.$$

1차 예측값은 $-\eta\lVert g\rVert^2=-0.1\times1.591249=-0.159125$이므로 이 스텝은 gradient가 약속한 값의 $81\%$를 실제로 냈다. 그 차이가 곡률이고, $\eta$를 더 키우면 그 차이의 부호가 바뀌는데 그 이야기가 §6이다.

### 1. 모델은 형식이 붙은 계산이다

배치 크기 $B$이면 $X\in\mathbb R^{B\times2}$, $H\in\mathbb R^{B\times3}$, $S\in\mathbb R^{B\times2}$. 파라미터는 학습되고, activation은 샘플마다 달라지며, 하이퍼파라미터는 경사하강 밖에서 고른다.

> **파라미터·activation·하이퍼파라미터, 세 갈래의 정의.** 셋 다 *같은 프로그램 안의 숫자*라서 헷갈린다. 구분은 **무엇이 그 값을 바꾸는가**다. **파라미터**는 optimizer가 쓰는 숫자다. gradient가 있고, "모델 크기"에 세어지고, checkpoint에 저장된다. D1에서는 $W_1$과 $W_2$의 12개, bias 0까지 세면 17개다. **activation**은 입력을 흘려서 만들어지는 숫자다. 자기 gradient를 저장하지 않고, 샘플마다 바뀌며, 학습 메모리를 지배한다. D1의 $z$, $h$, $s$, $p$가 그것이다. **하이퍼파라미터**는 경사하강 밖에서 사람이나 탐색이 고르는 숫자다. learning rate $\eta$, decay $\lambda$, batch 크기, 은닉 유닛 수.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta}\qquad\text{— }\theta\text{는 파라미터, }\eta\text{는 하이퍼파라미터, }L\text{은 activation에서 나왔다}$$
>
> 갱신식 하나에 셋이 모두 들어 있으므로, 이 식을 왼쪽부터 읽는 것이 논문에 나온 임의의 숫자를 분류하는 가장 빠른 방법이다.
>
> - **예**: D1의 은닉 폭 3은 하이퍼파라미터, 거기서 나온 $h=(1,2,1)$은 activation, 그것을 만든 $W_1$은 파라미터다. 폭을 바꾸면 파라미터 수가 바뀌고, 입력을 바꾸면 activation만 바뀐다.
> - **비예**: ReLU mask $\mathbf 1[z>0]=(1,1,1)$. 아무도 학습하지 않으니 파라미터가 아니고, 아무도 고르지 않았으니 하이퍼파라미터도 아니다. 샘플에서 유도된 값이다. 그래서 "sparsity"를 보고하는 논문은 *무엇의*, *어떤 데이터에서의* sparsity인지 말해야 한다.
> - **비예**: Adam의 optimizer state. optimizer가 쓰고 checkpoint에 저장되니 파라미터처럼 보이지만 순전파에 쓰이지 않으므로 모델 크기에 세면 안 된다. 파라미터 수 대신 "checkpoint 크기"를 인용하는 논문이 세고 있는 것이 이것이다.
> - **왜 중요한가**: "우리 모델이 3배 작다"는 파라미터 주장, "학습 메모리가 3배 적다"는 activation 주장, "튜닝이 3배 싸다"는 하이퍼파라미터 주장이다. 서로 다른 세 실험이고, 이를 뭉뚱그린 논문은 셋 중 어느 것도 하지 않은 것이다. 실험 절을 읽기 위한 같은 구분은 [[02-foundations/neural-network-basics|0.7 신경망 §5]]에 있다.

이 $s=(2,1)$은 D1 순전파 결과다. $p=(0.731,0.269)$이고 정답이 1번일 때 cross-entropy는 $0.313$이다. 두 logit에 같은 상수를 더해도 확률은 같다. softmax는 상대적 증거를 표현한다.

> **Softmax의 정의.** **Softmax**는 *실수 logit 벡터를 확률 단체(simplex) 위의 한 점으로 보내는 사상*이다. 파라미터가 있는 층이 아니고, 맞을 확률도 아니다. 정의 조건 셋. 출력이 **양수이고 합이 1**이라서 분포로 쓸 수 있다. **평행이동 불변**이라 $\operatorname{softmax}(s+c\mathbf 1)=\operatorname{softmax}(s)$이고, 따라서 logit의 *차이*만 정보를 나른다. 그리고 각 logit에 대해 **순증가**라서 logit의 순위가 곧 확률의 순위이고 arg max는 움직이지 않는다.
>
> $$p_i=\frac{e^{s_i}}{\sum_{j=1}^{C}e^{s_j}}$$
>
> $s\in\mathbb R^{C}$는 logit, $C$는 클래스 수, $p_i$는 클래스 $i$의 예측 확률이다. 구현은 먼저 모든 logit에서 $\max_j s_j$를 빼는데, 평행이동 불변이라 값은 그대로이면서 $e^{s_j}$의 overflow를 막기 때문이다.
>
> - **예**: D1의 $s=(2,1)$은 $p=(0.731059,0.268941)$을 주고, $s=(102,101)$도 정확히 같은 $p$를 준다. 들어간 것은 차이 $s_1-s_2=1$뿐이다.
> - **비예**: max. softmax는 $\max_j s_j$나 arg max의 one-hot을 돌려주지 않는다. logit *간격*이 정하는 날카로움을 가진 분포를 돌려준다. 그 간격을 다루는 것이 [[03-deep-learning/vlm/index|3. VLM]]의 temperature sweep이다.
> - **비예**: 답이 맞을 신뢰도. $p_1=0.731$은 모델이 낸 숫자이지 측정된 빈도가 아니다. 그런 예측의 $73\%$가 실제로 맞는지는 calibration이고 따로 측정한다([[02-foundations/ml-practice|9. ML 실무 §3]]).
> - **왜 중요한가**: 평행이동 불변 때문에 $C$개의 logit이 자유도 $C-1$만 가지고, "logit bias" 한 열을 지워도 아무 변화가 없으며, 서로 다른 logit을 보고한 두 논문이 동일한 분류기를 말하고 있을 수 있다.

> **Cross-entropy loss의 정의.** **Cross-entropy loss**는 *예측 분포와 정답 분포의 스칼라 함수*다. 결정이 아니라 분포를 채점하므로 accuracy가 아니다. 정의 조건 셋. 예측 아래에서 정답의 **음의 로그가능도**이므로 이것을 최소화하는 것이 최대가능도 추정이다. 두 인자에 대해 **비대칭**이라 $H(y,p)\ne H(p,y)$이고, 학습되는 쪽은 $p$다. 그리고 **위로 유계가 아니다**. 확신에 찬 오답은 얼마든지 비쌀 수 있고, 확신에 찬 정답은 이미 가진 것보다 더 아끼지 못한다.
>
> $$L=-\sum_{i=1}^{C}y_i\log p_i\ \ \xrightarrow{\ y\text{가 }c\text{에서 one-hot}\ }\ \ L=-\log p_c$$
>
> $y$는 정답 분포(이 페이지에서는 항상 정답 클래스 $c$의 one-hot), $p$는 softmax 출력, $C$는 클래스 수다. 합이 한 항으로 줄어드는 이유는 one-hot $y$가 $i\ne c$를 전부 0으로 만들기 때문이다.
>
> - **예**: 정답이 1번인 D1은 $-\log 0.731059=0.313262$ nat이다. 밑이 $e$면 nat, 2면 bit이고, $0.313262/\log 2=0.451941$ bit는 단위만 바꾼 같은 숫자다.
> - **비예**: accuracy. D1의 예측은 *맞다* — 1번 클래스의 확률이 더 크다 — 그런데 loss는 양수 $0.313$이다. accuracy가 그대로인 채 loss가 오를 수 있으므로 논문은 둘 다 보고해야 하고, 한쪽 기준의 early stopping은 다른 쪽 기준의 early stopping이 아니다.
> - **비예**: 예측의 엔트로피. 여기서 $H(p)=0.582\ \text{nat}$인데 이것은 loss가 아니다. 엔트로피는 예측이 얼마나 퍼져 있는지를, cross-entropy는 그 질량이 정답 위에 얼마나 있는지를 잰다. 둘의 관계 $H(y,p)=H(y)+D_{\mathrm{KL}}(y\Vert p)$는 [[02-foundations/information-theory|5. 정보이론 §2]]에 있다.
> - **왜 중요한가**: 위로 유계가 아니라는 점이 optimizer 탓으로 돌려지는 학습 불안정의 주된 출처다. 확신에 찬 예측을 받은 오라벨 샘플 하나가 정답 백 개보다 큰 loss를 낼 수 있고, $\lVert\partial L/\partial s\rVert$가 $\sqrt2$로 묶이는 것은 앞에 softmax가 있기 때문일 뿐이다.

### 2. 한 번의 update는 학습 결과가 아니다

one-hot $y$에 대해 softmax와 cross-entropy를 합치면 $\partial L/\partial s=p-y$다. 여기서는 $(-0.269,0.269)$이므로 정답 logit은 올리고 다른 logit은 내린다. backprop은 gradient를 계산하고 optimizer가 update로 바꾼다. $p-y$가 $W_1$까지 되돌아가는 사슬은 위의 계산 절에 전부 적혀 있고, 일반 기계는 [[02-foundations/calculus-backprop|2. 미적분과 역전파 §3]]에 있다.

그 미분이 왜 그렇게 깨끗한지는 한 줄 적어 둘 만하다. 두 블록을 하나로 그리는 이유가 그것이기 때문이다. softmax의 Jacobian은 $\partial p_i/\partial s_j=p_i(\delta_{ij}-p_j)$이고 loss의 미분은 $\partial L/\partial p_i=-y_i/p_i$인데, 곱하면 $p_i$가 전부 약분되고 $p-y$만 남는다. 각각은 다루기 나쁘고 곱은 뺄셈 하나다. 구현이 둘을 융합하는 이유이고, softmax를 실수로 두 번 걸 수 있는 프레임워크가 오류 없이 느리고 틀리게 학습되는 이유이기도 하다.

> **SGD 스텝과 learning rate의 정의.** **경사하강 스텝**은 *파라미터 벡터에 적용되는 갱신 규칙*, 즉 $\theta\mapsto\theta'$인 사상이다. loss도 방향도 아니다. 정의 조건 셋. **자기가 받은 loss의 gradient 반대 방향으로** 움직이므로, 내려가는 대상은 그 gradient가 나온 목적함수다(weight decay가 있으면 cross-entropy가 아니다). 미분 밖에서 고른 **보폭**을 $\eta$로 가지며, 그래서 $\eta$가 하이퍼파라미터다. 그리고 **국소적인 진술일 뿐**이다. $L(\theta')<L(\theta)$ 보장은 충분히 작은 $\eta$에 대해 성립하지, 당신이 고른 특정 $\eta$에 대해 성립하지 않는다.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta},\qquad L(\theta')\approx L(\theta)-\eta\lVert g\rVert^2+\tfrac{\eta^2}{2}g^\top Hg$$
>
> $g=\partial L/\partial\theta$, $H$는 $\theta$에서의 Hessian이다. 2차 항이 하강을 하강이 아니게 만드는 범인이다. 이차형식에서는 $\eta<2/\lambda_{\max}(H)$인 동안만 loss가 줄어드는데, 그 위에서는 $\eta^2$ 항이 $\eta$ 항을 앞지르기 때문이다.
>
> - **예**: $\eta=0.1$의 D1은 $\Delta L\approx-\eta\lVert g\rVert^2=-0.159125$를 예측하고 $-0.129177$을 낸다. 모자란 부분이 $\eta^2$ 항이고 아직은 작다.
> - **비예**: 전체 데이터를 한 배치로 넣은 "SGD" — 이 페이지가 돌리는 것이 바로 그것이다. stochastic gradient descent는 gradient가 *표본 추정치*라는 뜻인데, D1은 샘플이 하나라 모든 gradient가 정확하고 SGD의 잡음 논증은 하나도 적용되지 않는다. full-batch를 "SGD"라 부르는 논문은 코드에서는 틀리지 않고 해석에서는 틀린다.
> - **비예**: Adam. $\eta$만 다른 같은 규칙이 아니다. 좌표마다 2차 모멘트로 나누므로 실효 보폭이 $\eta$가 아니고 $2/\lambda_{\max}$ 경계도 그대로 옮겨 가지 않는다. optimizer를 바꾸며 "같은 learning rate"를 비교하는 것은 아무것도 비교하지 않는 것이다.
> - **왜 중요한가**: $2/\lambda_{\max}(H)$는 어림이 아니라 *측정 가능한* 숫자이고, §6이 D1에서 유효숫자 네 자리까지 측정한다. optimizer 계열은 [[02-foundations/optimization|4. 최적화 §3]]이다.

### 3. Train·validation·test의 질문은 다르다

- train loss: 학습 배치를 맞출 수 있는가.
- validation: checkpoint와 hyperparameter 중 무엇을 고를 것인가.
- test: 이미 고정한 결정을 미사용 자료에서 평가하면 어떤가.

test를 보며 계속 조정하면 test 정보가 학습 절차로 샌다. 분할 규율과 무엇이 유출인지는 [[02-foundations/ml-practice|9. ML 실무 §1]]에 있다.

### 4. 정규화와 scaling은 통제가 필요한 주장이다

weight decay, augmentation, dropout, early stopping, 데이터와 compute 증가는 서로 다른 기제로 결과를 바꾼다. scaling 주장은 parameter·data·compute 축을 분리해야 한다.

그중 §6이 필요로 하는 것은 weight decay이므로, 목록의 한 단어가 아니라 정의를 붙인다.

> **Weight decay의 정의.** **Weight decay**는 *목적함수에 더하는 항*이다. 최소화 대상 자체를 바꾸므로 나중에 갱신에 얹는 요령이 아니다. 정의 조건 셋. **파라미터의 제곱 norm**에 벌점을 주는데 이것은 선택이다. 큰 가중치 하나보다 작은 가중치 여럿을 선호하고, 데이터에 대해서는 아무 의견이 없다. **activation이 아니라 파라미터**에 적용되므로 $W_1$과 $W_2$를 줄이고 $h$는 건드리지 않는다. 그리고 경사하강 밖에서 고른 **계수 $\lambda$로 크기가 정해지므로**, $\lambda$ 없이 "weight decay를 썼다"고 적은 논문은 아무것도 적지 않은 것이다.
>
> $$L_{\lambda}(\theta)=L(\theta)+\frac{\lambda}{2}\lVert\theta\rVert^2,\qquad \frac{\partial L_\lambda}{\partial\theta}=\frac{\partial L}{\partial\theta}+\lambda\theta$$
>
> $\lVert\theta\rVert^2$은 D1의 가중치 12개의 제곱합이고 $\lambda\ge0$은 계수다. gradient에 원점을 바로 가리키는 항이 붙으므로, 데이터가 발언하기 전에 이미 매 스텝이 파라미터에 $(1-\eta\lambda)$를 곱한다.
>
> - **예**: $\lambda=0.1$의 D1은 $\lVert W_1\rVert^2=3$, $\lVert W_2\rVert^2=2$이므로 $L_\lambda=0.313262+\tfrac{0.1}{2}\cdot5=0.563262$에서 출발한다.
> - **비예**: Adam 갱신 *뒤에* $(1-\eta\lambda)$를 곱하는 방식(decoupled weight decay). 최소점이 다른 다른 알고리즘이지 구현 세부가 아니다. 문헌이 둘을 다른 이름으로 부르는 이유다.
> - **비예**: early stopping. 둘 다 실효 용량을 줄이지만 early stopping은 *언제 멈추는가*를 바꿀 뿐 목적함수는 그대로 둔다. weight decay는 *무엇을 최소화하는가*를 바꾸므로 최소점 자체가 옮겨 간다. §6이 쓰는 것이 이 성질이다. D1에 넘어설 최소점을 주는 것이 decay다.
> - **왜 중요한가**: 분리 가능한 점 하나에 대한 cross-entropy에는 최소점이 **없다**. logit이 무한으로 달아나면서 loss가 단조 감소하므로 어떤 learning rate도 "너무 크지" 않고, 거기서 한 보폭 sweep은 아무것도 재지 못한다. $\lambda$를 더하면 목적함수가 유한한 $\theta^\ast$에서 바닥을 얻고, 그제서야 안정성 경계가 존재한다. 정규화라는 우산 전체는 [[02-foundations/ml-practice|9. ML 실무 §2]]에 있다.

### 5. 학습 recipe 읽기

데이터 혼합·split, 전처리, 초기화, 목적함수, optimizer·schedule, batch와 update 수, precision·hardware, checkpoint 선택, seed와 불확실성을 뽑는다. 그다음 ablation에서 무엇이 필수인지 확인한다.

### 6. 실습: 보폭에는 경계가 있고, 그 경계는 측정된다

위의 전부는 한 스텝이다. 손계산이 답할 수 없는 질문은 *어떤 보폭을 반복할 수 있는가*이므로, 이 절은 같은 D1을 반복문에 넣는다. 영어 절 코드의 1부는 계산 절을 그대로 재현한다. 손계산이 그 출력과 다르면 표를 읽기 전에 손계산부터 고친다. 2부는 §4의 $\lambda=0.1$ decay를 더하는데, 그것이 없으면 목적함수에 최소점이 없어서 모든 보폭이 똑같이 좋아 보이기 때문이다. 3부는 표의 경계가 어디서 오는지 묻는다.

**Sweep.** 카탈로그 $W_1,W_2$에서 시작해 full-batch 200스텝, 목적함수는 cross-entropy $+\ 0.05\lVert\theta\rVert^2$이고 시작값은 $L_\lambda=0.563262$다. "죽은 유닛"은 끝에서 $h_i=0$인 은닉 유닛 수이고 전체는 3개다.

| $\eta$ | 200스텝 뒤 $L_\lambda$ | $p_1$ | 죽은 유닛 | 무슨 일이 일어났나 |
|---:|---:|---:|---:|---|
| $0.01$ | $0.255664$ | $0.9657$ | 0 | 아직 내려가는 중, 200스텝이 모자랐다 |
| $0.1$ | $0.143118$ | $0.9684$ | 1 | 거의 도착 |
| $0.5$ | $0.140339$ | $0.9684$ | 1 | 최소점 |
| $1$ | $0.140339$ | $0.9684$ | 1 | 최소점 |
| $2$ | $0.140339$ | $0.9684$ | 1 | 최소점 |
| $3$ | $0.140345$ | $0.9678$ | 1 | 경계 위, $2/\lambda_{\max}=3.0179$ |
| $5$ | $0.149517$ | $0.9867$ | 1 | 최소점 위에서 진동 |
| $8$ | $0.599431$ | $1.0000$ | 1 | cross-entropy는 0, norm은 큼: 튕기는 중 |
| $10$ | $0.693147$ | $0.5000$ | 3 | 붕괴, $\log 2$는 포기한 loss |
| $12$ | 15스텝에서 발산 | — | — | overflow |
| $20$ | 9스텝에서 발산 | — | — | overflow |

**Sweep 읽기.** 손 유도가 알려줄 수 없었던 것 넷.

- **쓸모 있는 경계는 정착 경계이고, 그것이 정확히 $2/\lambda_{\max}$다.** $0.5$부터 $2$까지의 행이 $L^\ast=0.140339$에 여섯 자리까지 내려앉고, $3$의 행은 여섯째 자리에서 어긋난다. 코드 3부는 $\theta^\ast$까지 내려가 유한차분으로 $12\times12$ Hessian을 만들고 $\lambda_{\max}=0.6627$, 즉 $2/\lambda_{\max}=3.0179$를 보고한다. 같은 반복문을 이분법으로 훑어 여전히 정착하는 최대 $\eta$를 찾으면 $3.0180$이다. 교과서의 조건이 여기서는 근사가 아니라 측정값이고, 유효숫자 네 자리까지 맞는다.
- **경계 위에서는 실패가 시끄러워지기 전에 조용하다.** $\eta=8$에서 cross-entropy는 0이다. 모델은 자기 학습점 하나에 대해 *완벽하다*. 그런데 $L_\lambda=0.599431$로 최소점의 네 배인데, 가중치가 원점에서 멀리 던져졌기 때문이다. accuracy만 보는 run은 아무 이상도 보지 못한다. $\eta=10$에서는 은닉 유닛 셋이 모두 죽고 $p=(0.5,0.5)$, loss는 정확히 $\log 2=0.693147$이다. 모든 가중치가 0으로 감쇠했고 신경망은 사전 확률을 예측한다. 이 숫자는 눈에 익혀 둘 가치가 있다. $0.693$에 멈춘 2클래스 run은 수렴한 것이 아니라 포기한 것이다.
- **유닛 하나가 죽는 것은 의도이고 버그가 아니다.** $\eta=0.1$부터 $\eta=8$까지의 모든 행이 죽은 유닛 하나로 끝나고, 최소점 자체가 그렇다. $\theta^\ast$에서 $W_1$의 첫 행과 $W_2$의 첫 열이 0이다. 역전파가 은닉 유닛 1을 내리려 했고($\partial L/\partial z_1=+0.268941$) decay가 마무리했다. weight decay는 가지치기를 한다. 죽은 유닛 셋은 붕괴이고, 하나는 목적함수가 시킨 대로 한 것이다.
- **Overflow 경계는 경계가 아니다.** 정착 경계처럼 발산 임계값을 보고하고 싶어진다. 코드 3부는 $\eta$를 $10.40$에서 $10.6095$까지 $0.0005$ 간격으로 훑는다. 첫 발산은 $\eta=10.4015$이고, 그 이상의 격자점 417개 중 285개가 여전히 200스텝을 살아남는다. 안정성 한계를 넘으면 반복이 ReLU의 꺾인 점들 위를 튕기고, 탈출 여부가 $\eta$에 대해 단조롭지 않다. 이런 그림에서 "$\eta=10.4$ 위에서 학습이 발산한다"고 적은 논문은 격자 하나를 인용하고 있는 것이다.

### 스스로 점검 · Self-check

1. $W_2$, $h$, $\eta$, $\lambda$, ReLU mask 중 무엇이 파라미터이고 activation이고 하이퍼파라미터인가.
2. 구현은 왜 softmax와 cross-entropy를 한 블록으로 융합하는가.
3. D1의 $\partial L/\partial h$는 세 번째 성분이 0이다. 대상의 어느 숫자가 그렇게 만들었고, 예측이 좋아지면 달라지는가.
4. 2클래스 학습이 loss $0.693$에서 평평해졌다. 가장 그럴듯한 진단 하나와 확인 방법은?
5. 분리 가능한 샘플 하나에 대한 순수 cross-entropy에서 learning rate sweep이 안정성에 대해 아무것도 가르치지 못하는 이유는?

> [!tip]- 정답 · Answers
> 1. 파라미터는 $W_2$(그리고 $W_1$), activation은 $h$, 하이퍼파라미터는 $\eta$와 $\lambda$다. ReLU mask는 셋 중 어느 것도 아니다. 샘플에서 유도되므로 메모리 관점에서는 activation이고, *아무도 고르지 않은* 값이다.
> 2. 따로 두면 Jacobian이 $p_i(\delta_{ij}-p_j)$와 $-y_i/p_i$로 지저분한데 곱하면 $p-y$로 약분된다. 융합하면 underflow된 확률에 $\log$를 거는 일도 피한다.
> 3. $W_2$의 세 번째 열이 $(0,0)$이라 은닉 유닛 3이 아무 데도 연결되어 있지 않다. 예측이 맞든 틀리든 0이다. gradient는 배선의 성질이지 오차의 성질이 아니다.
> 4. 모델이 클래스 사전 확률을 예측하고 아무것도 배우지 않는 상태다. $\log 2=0.693147$이 $p=(0.5,0.5)$의 loss다. logit을 찍어 확인한다. 가중치가 작으면서 $s_1\approx s_2$이면 보폭이 신경망을 붕괴시킨 것이고($\eta=10$의 행), 가중치가 큰데도 $s$가 평평하면 배선이 끊긴 것이다.
> 5. 그 목적함수에는 최소점이 없다. logit이 무한으로 갈 수 있어서 표의 모든 $\eta$에서 loss가 단조 감소한다. 넘어설 최소점이 없으므로 sweep 안의 어떤 것도 불안정할 수 없다. 바닥을 주는 것이 weight decay다(§4).

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[03-deep-learning/lab-objects|0. Lab Objects]]만 쓴다. 대상은 계속 D1이고, 문제 2와 4가 정답 클래스를 바꾸므로 페이지의 숫자를 그대로 옮길 수 없다.

1. **그리기.** $B=4$인 D1의 shape를 그리고 bias 포함 parameter 수를 센다. 과제가 그릴 그림의 역방향 화살표를 더하고, 어느 화살표가 ReLU mask에 막히고 어느 화살표가 $W_2$의 0인 열에 막히는지 표시한다.
2. **유도.** logit $(0,\log3)$, 정답 1번의 확률·loss·$p-y$를 구한다.
3. **해석.** test를 보며 augmentation을 바꿨다면 어떤 경계를 넘었는가.
4. **실행.** 영어 절 템플릿의 `?`를 채운 뒤, 정답을 **2번 클래스**로 바꾸고($y=(0,1)$, 즉 카탈로그 모델이 *틀린* 상태에서 출발한다) decay를 $\lambda=0.2$로 올려 다시 돌린다. (a) 시작 $L_\lambda$, (b) $\eta\in\{0.05,0.5,2,5,20\}$, 200스텝의 $L_\lambda$·죽은 유닛·발산 스텝 표, (c) 이분법으로 찾은, 여전히 최소점에 정착하는 최대 $\eta$를 보고한다. 그리고 그 경계가 §6의 $\lambda=0.1$ 대비 왜 움직였는지 한 문장으로 말한다.

> [!tip]- 정답 · Solutions
> 1. $4\times2\rightarrow4\times3\rightarrow4\times2$, 총 17개. 역방향에서 $\partial L/\partial z=\partial L/\partial h\odot\mathbf 1[z>0]$이 mask에 막히는 쪽이고, $\partial L/\partial h_3=0$은 $W_2$의 0인 세 번째 열에 막히는 쪽이다. 기제가 다르다. 후자는 샘플과 무관하게 영구적이다.
> 2. $p=(1/4,3/4)$, $L=1.386$, $p-y=(-3/4,3/4)$.
> 3. test가 모델 선택에 들어가 더 이상 독립 평가가 아니다.
> 4. 빈칸은 `y = np.array((0., 1.))`, `lam = 0.2`, `h = np.maximum(z, 0.0)`, `gs = p - y`, `gz = (B.T @ gs) * (z > 0)`, 그리고 `abs(out[0] - 0.235806)`이다. (a) 카탈로그 모델이 새 정답에 $p_2=0.268941$밖에 두지 않으므로 $L_\lambda=1.313262+0.5\cdot0.2\cdot5=1.813262$. (b) sweep은
>
>    | $\eta$ | 200스텝 뒤 $L_\lambda$ | 죽은 유닛 |
>    |---:|---:|---:|
>    | $0.05$ | $0.240870$ | 0 |
>    | $0.5$ | $0.235806$ | 1 |
>    | $2$ | $0.238924$ | 1 |
>    | $5$ | $0.693147$ | 3 |
>    | $20$ | 6스텝에서 발산 | — |
>
>    (c) 이분법은 $1.9801$을 주고 $L^\ast=0.235806$이다. $3.0180$에서 **내려갔다**. $\lambda$를 두 배로 하면 모든 방향의 곡률에 $\lambda$가 더해지므로 새 최소점에서 Hessian의 $\lambda_{\max}$가 커지고 $2/\lambda_{\max}$는 작아진다. 정규화를 세게 거는 것은 학습을 공짜로 안정시키는 방법이 아니다. loss의 바닥을 사고 보폭 천장을 좁혀 지불한다. $\eta=5$의 행은 §6과 같은 $\log 2$ 붕괴가 더 일찍 온 것이다.
