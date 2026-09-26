---
title: 1. Learning Systems
tags: [deep-learning, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Trace one model from tensors and loss through an optimizer update, validation, and a defensible training claim."
mastery-when: "Raise when architecture, objective, optimization, or scaling is part of the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/neural-network-basics|0.8 Neural Networks]], [[02-foundations/calculus-backprop|2. Calculus & Backprop]], [[02-foundations/optimization|4. Optimization]], and [[02-foundations/ml-practice|9. ML Practice]]. Object **D1** from [[03-deep-learning/lab-objects|0. Lab Objects]]; the Tier A lab in §6 needs NumPy and nothing else. If NumPy is new, read [[02-foundations/tools/python-research-code|12.3 Python for Research Code §3–§4]] (arrays, shapes and vectorised loops) first.
> [[02-foundations/neural-network-basics|0.8 신경망]], [[02-foundations/calculus-backprop|2. 미적분과 역전파]], [[02-foundations/optimization|4. 최적화]], [[02-foundations/ml-practice|9. ML 실무]]. 대상은 [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D1**이고, §6의 Tier A 실습에는 NumPy만 있으면 된다. NumPy가 처음이면 [[02-foundations/tools/python-research-code|12.3 연구 코드를 위한 Python §3–§4]](배열, shape, 벡터화한 반복)를 먼저 읽는다.

## English

> [!note] Why this matters · 왜 배우는가
> This page opens the *learning and adaptation* layer of the physical-AI stack in [[07-research-program/index|7. Research Program §5]]: it is the training loop under every learned part of *"install that panel on the frame"*, from the detector that serves step 2, *identify panel and frame*, to the learned policy that serves step 7, *perform the fitting* (its chip sits in the learning-and-adaptation band of the [[physical-ai-map|Physical AI Map]]). A learned part's number is only as good as the loop behind it, and one step does not show the loop. On D1, the track's frozen two-layer classifier ([[03-deep-learning/lab-objects|0. Lab Objects]]), one step at $\eta=0.1$ delivers $81\%$ of the drop its gradient promised; below $2/\lambda_{\max}(H)=3.018$ every step size settles, given enough steps, on the same minimum; $\eta=8$ fits its one sample to a cross-entropy of $5.9\times10^{-9}$ while throwing its weights far from the origin; and $\eta=10$ gives up at $\log2=0.693$ (§6), none of which a loss quoted without its $\eta$, $\lambda$ and step count would show. The page's softmax, cross-entropy and $p-y$ return in [[03-deep-learning/vlm/index|3. VLM §2]], where each image picks its caption out of a batch, and its update trains the behaviour-cloning policies of [[03-deep-learning/vla/index|4. VLA §2]] and [[05-construction-robotics/imitating-contact|10. Imitating Contact §2]]; on the dissertation path ([[07-research-program/index|7. Research Program §8]]) it opens the deep-learning half of block 4, as deep-learning sessions 1–3, read after [[02-foundations/rl-robot-learning|7.5 RL §1 and §4]]. After it you can push one input forward and one update back through a network by hand, measure the step size a loop can repeat, and list what a training recipe must state before its number means anything.

> [!note] First pass · 처음이라면
> About three sessions of 60–90 minutes, rows 1–3 of the [[03-deep-learning/index|deep-learning schedule]]; the first two are the first pass. **Session 1:** the Running object, the picture and the Worked case, by hand with the solution covered: $L=0.313262$ nats, $p-y=(-0.268941,\,0.268941)$, and $\Delta L=-0.129177$ at $\eta=0.1$. **Session 2:** §1–§5 — open §1's collapsed recap only if softmax or cross-entropy has faded — then self-checks 1–3 and 5 and problems 1–3. **Session 3:** run §6's listing, read its figure and its four readings, and do problem 4. Finish by saying in your own words why $2/\lambda_{\max}(H)=3.018$ is the largest step size that settles, and — self-check 4, which needs §6 — why a two-class run stuck at $0.693$ has given up rather than converged.

### Running object: D1

Use **D1**, the deep-learning track's frozen two-layer classifier from [[03-deep-learning/lab-objects|0. Lab Objects]]:

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}.$$

Forward: $W_1x=(1,2,1)$, $h=\operatorname{ReLU}(W_1x)=(1,2,1)$, $s=W_2h=(2,1)$. The prediction is $p=\operatorname{softmax}(s)$. A diagram must show shapes $2\rightarrow3\rightarrow2$. This is not **P1**, the foundations track's two-layer test network of [[02-foundations/lab-plants|0.6 Lab Plants]] ($2\to3\to1$ MSE).

**The biases are held at zero.** The architecture has a bias vector in each layer, $b_1\in\mathbb R^3$ and $b_2\in\mathbb R^2$, and this page holds all five entries at zero: they are never updated and never decayed. So D1 trains $12$ parameters, the six entries of $W_1$ and the six of $W_2$, in an architecture with $17$ slots — the convention by which [[02-foundations/neural-network-basics|0.8 §2]] counts P1's $9$ weights of $13$ slots. A framework's linear layer trains its bias by default, and one step at $\eta=0.1$ with the biases trained lands elsewhere, at $s=(2.353964,\ 0.646036)$ with $\Delta L=-0.146696$: a different model with $17$ trained numbers, not an error in either calculation.

**Notation.** This page writes the logits $s$, the number of classes $C$, the step size $\eta$ and the weight decay $\lambda$. [[02-foundations/calculus-backprop|2. Calculus & Backprop §4.1]] and [[02-foundations/neural-network-basics|0.8 §6]] write the logits $z$ and the classes $K$ (here $z$ is the pre-activation, so 2 §4.1's $\partial L/\partial z=p-y$ is this page's $\partial L/\partial s$); 0.8 §3 and [[02-foundations/optimization|4. Optimization §3]] write the step size $\alpha$ in the general rule, though 4's worked step on P1 already uses $\eta$; and 4 writes a Hessian's eigenvalues $\lambda_i$ — so the curvature here is always $\lambda_{\max}(H)$, never a bare $\lambda$.

The target is class 1 throughout this page, so $y=(1,0)$, and every number below follows from $W_1$, $W_2$, $x$, $y$ and the zero biases, and nothing else.

*Scope: this page teaches the typed pipeline from one input to one parameter update — shapes, softmax, cross-entropy, the backward pass, one SGD step, and the step size that update has to respect — and the evidence a training claim owes. It does not teach where the derivatives come from, which is [[02-foundations/calculus-backprop|2. Calculus & Backprop §2]]; nor the optimizers themselves (momentum, Adam, schedules), which are [[02-foundations/optimization|4. Optimization §3]]; nor the experimental protocol that turns a number into a result, which is [[02-foundations/ml-practice|9. ML Practice §4]]; nor any architecture beyond a two-layer MLP — convolutions and patch tokens are [[03-deep-learning/computer-vision/index|2. Computer Vision]], and attention is [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]] and the [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer note]]. The module's four sub-lectures build on this page: [[03-deep-learning/foundations/sequence-models|1.1 Sequence Models]], [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]], [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale]] and [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing for Robot Learning]].*

### The picture

<svg viewBox="0 0 560 588" style="max-width:100%;height:auto" role="img" aria-label="D1's forward pass down the left with every tensor's shape and value, its weights and its biases held at zero in the middle, the backward pass up the right with every gradient's value, and a bottom strip with one SGD step on the 12 weights: predicted change -0.159125, delivered -0.129177">
  <defs><marker id="aD1e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="22" font-size="12" fill="currentColor">D1 · target class 1, y = (1, 0) · solid: forward · dashed: backward</text>
  <text x="75" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">forward · activations</text>
  <text x="265" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">parameters · biases held at zero</text>
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
  <line x1="12" y1="516" x2="548" y2="516" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <text x="12" y="534" font-size="11" fill="currentColor">One SGD step, η = 0.1, on the 12 weights: s → (2.299452, 0.700548), L → 0.184085</text>
  <text x="12" y="557" font-size="11" fill="currentColor">predicted, −η‖g‖²</text>
  <rect x="150" y="548" width="200" height="11" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="356" y="557" font-size="11" fill="currentColor">−0.159125</text>
  <text x="12" y="577" font-size="11" fill="currentColor">delivered, ΔL</text>
  <rect x="150" y="568" width="162.4" height="11" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="1"/>
  <text x="318.4" y="577" font-size="11" fill="currentColor">−0.129177, 81% of the prediction</text>
</svg>

D1's worked case on the catalog numbers, target class 1. The forward pass runs down the left, $x=(1,2)\to z=(1,2,1)\to h=(1,2,1)\to s=(2,1)$, into one softmax-and-cross-entropy block that gives $p_1=0.731059$ and $L=0.313262$ nats, with the weights and the biases, held at zero, in the middle. The backward pass runs up the right from $\partial L/\partial s=p-y=(-0.268941,0.268941)$ to $\partial L/\partial h=(0.268941,-0.268941,0)$, whose zero is $W_2$'s empty third column, and through the ReLU mask $\mathbf 1[z>0]=(1,1,1)$ to $\partial L/\partial W_1$ — no arrow runs from $L$ straight to $W_1$. The strip at the bottom is the Worked case's one step on the 12 weights at $\eta=0.1$: the loss falls by $0.129177$, $81\%$ of the $0.159125$ the gradient predicted.

### Worked case

This is the homework object. Do the three things the problem set asks — forward, backward, one step — here first, on the catalog numbers, so the set is a change of input, target and knob rather than a first derivation. Loss is in nats throughout, because every logarithm on this page is natural.

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

and the third entry is exactly zero because $W_2$'s third column is $(0,0)$: at these weights hidden unit 3 feeds nothing forward, so no error, however large, flows back into it, and $W_1$'s third row gets a zero gradient on this step. The block is not permanent. $W_2$'s third column has a gradient of its own, $(-0.268941,\ 0.268941)$ in the matrix above, because unit 3 is active ($h_3=1$), so one step writes $(0.026894,\ -0.026894)$ into it and the path back to unit 3 opens. Applying the mask (all ones here) and one more outer product with $x=(1,2)$:

$$\frac{\partial L}{\partial W_1}=\begin{pmatrix}0.268941&0.537883\\-0.268941&-0.537883\\0&0\end{pmatrix}.$$

**One SGD step.** The rule is $\theta\leftarrow\theta-\eta\,\partial L/\partial\theta$, applied to the 12 weights while the biases stay at zero. At $\eta=0.1$ the logits move to $s=(2.299452,\ 0.700548)$ — symmetric, by $\pm0.299452$, because $p-y$ is antisymmetric for two classes — and

$$p=(0.831865,\ 0.168135),\qquad L=0.184085,\qquad \Delta L=-0.129177 \text{ nats}.$$

The first-order prediction is $-\eta\lVert g\rVert^2=-0.1\times1.591249=-0.159125$, so the step delivered $81\%$ of what the gradient promised. The gap is curvature: §2's second-order term moves the prediction to $-0.1267$, only $0.0025$ from the delivered $-0.1292$. The curvature term grows as $\eta^2$ and the promised drop only as $\eta$, so a large enough step lets curvature win; §6 measures how large $\eta$ can grow before repeated steps stop settling.

### 1. A paper's model is a typed computation

*In one sentence:* a model described in words becomes checkable only once every tensor has a shape and every number is sorted into learned, computed or chosen — and on D1 that typing turns two logits into a probability and a loss in two lines.

*If you need only one thing from this section:* the three-way split — a parameter is written by the optimizer, an activation by the input, a hyperparameter by a person — because it decides whether "smaller", "cheaper to train" or "cheaper to tune" is being claimed.

Architecture prose becomes checkable only after attaching shapes. For a batch of $B$ samples, $X\in\mathbb R^{B\times2}$, $H\in\mathbb R^{B\times3}$, and $S\in\mathbb R^{B\times2}$. If the numbers inside them are not sorted into the three kinds below, parameter counts and claims about efficiency become unreliable.

> **Parameter, activation, hyperparameter — the three-way split, defined.** All three are *numbers in the same program*, which is why they get confused; they differ in **what changes them**. A **parameter** is a number the optimizer writes: it has a gradient, it is counted in "model size", and it is saved in the checkpoint — D1's $W_1$ and $W_2$, 12 of them; its five biases are held at zero and never written, so on this page they are slots of the architecture, not parameters. An **activation** is a number produced by running the model on an input: it has no gradient of its own to store, it changes with every sample, and it must be kept for the backward pass, so it is the part of training memory that grows with the batch and the context ([[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §5]]) — D1's $z$, $h$, $s$, $p$. A **hyperparameter** is a number chosen outside gradient descent, by a human or a search: the learning rate $\eta$, the decay $\lambda$, the batch size, the number of hidden units.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta}\qquad\text{— }\theta\text{ is parameters, }\eta\text{ is a hyperparameter, and }L\text{ was computed from activations}$$
>
> so the update equation itself contains one of each, and reading it left to right is the fastest way to classify any number a paper mentions.
>
> - **Example**: D1's hidden width 3 is a hyperparameter; the resulting $h=(1,2,1)$ is an activation; the $W_1$ that produced it is parameters. Change the width and the parameter count changes; change the input and only the activation changes.
> - **Non-example**: the ReLU mask $\mathbf 1[z>0]=(1,1,1)$. It is an activation, not a parameter — nobody learns it — but it is also not a hyperparameter, because no one chose it. It is derived from the sample, which is why a paper that reports "sparsity" has to say sparsity *of what, on which data*.
> - **Non-example**: an Adam optimizer state. It is written by the optimizer and saved in a checkpoint, so it looks like a parameter, but it is not used in the forward pass and must not be counted in model size. Papers that quote "checkpoint size" instead of parameter count are quoting this.
> - **Why it matters**: "our model is 3× smaller" is a parameter claim, "it needs 3× less memory to train" is an activation claim, and "it is 3× cheaper to tune" is a hyperparameter claim. They are three different experiments and a paper that conflates them has not run any of them. The same split, written for reading experimental sections, is [[02-foundations/neural-network-basics|0.8 Neural Networks §5]].

The Worked case turned D1's logits into $p$ and $L$ through softmax and cross-entropy, which the foundations pages define in full; the collapsed recap restates them, and the list after it keeps in view what this page adds.

> [!note]- Recap · 복습
> **Softmax** ([[02-foundations/calculus-backprop|2. Calculus & Backprop §4.1]], [[02-foundations/neural-network-basics|0.8 §6]]) maps real logits to a probability vector; it is a function, not a layer with parameters:
>
> $$p_i=\frac{e^{s_i}}{\sum_{j=1}^{C}e^{s_j}}$$
>
> with $s\in\mathbb R^{C}$ the logits and $C$ the number of classes. Its outputs are positive and sum to one. It is shift invariant, $\operatorname{softmax}(s+c\mathbf 1)=\operatorname{softmax}(s)$, so only logit differences carry information: $C$ logits have $C-1$ degrees of freedom, and implementations subtract $\max_j s_j$ first so that $e^{s_j}$ cannot overflow. And since every $p_i$ shares one denominator, the ranking of the logits is the ranking of the probabilities, so softmax never changes which class is on top. D1's $s=(2,1)$ and $s=(102,101)$ both give $p=(0.731059,\ 0.268941)$.
>
> **Cross-entropy** ([[02-foundations/neural-network-basics|0.8 §3]], [[02-foundations/information-theory|5. Information Theory §2]]) scores a predicted distribution $p$ against a target distribution $y$:
>
> $$L=-\sum_{i=1}^{C}y_i\log p_i\ \ \xrightarrow{\ y\text{ one-hot at }c\ }\ \ L=-\log p_c$$
>
> because a one-hot $y$ zeroes every term but the true class's. It is the negative log-likelihood of the target, so minimising it is maximum likelihood, and it is asymmetric, $H(y,p)\ne H(p,y)$, with $p$ the argument being trained. D1 costs $-\log0.731059=0.313262$ nats ($0.451941$ bits). The prediction's own entropy, $H(p)=0.582$ nats, is not the loss: it measures how spread the prediction is, not how much of its mass sits on the truth.

What this page adds to those definitions:

- **Softmax is not a confidence.** $p_1=0.731$ is the model's number, not a measured frequency. Whether $73\%$ of such predictions are right is *calibration* — a model is calibrated when, among the cases it scores $0.73$, the event happens $73\%$ of the time — measured separately, with a reliability diagram and its summary number, the expected calibration error ([[04-robotics/human-intent-prediction|23. Human Intent Prediction §4]]).
- **Cross-entropy is not accuracy.** D1's prediction is *correct* — class 1 has the larger probability — while its loss is a positive $0.313$. Loss can rise while accuracy stays put, which is why a paper must report both and why early stopping on one is not early stopping on the other.
- **Cross-entropy is unbounded above.** A confident wrong answer costs arbitrarily much, while a confident right answer saves at most what it already had, so one mislabelled sample with a confident prediction can contribute more loss than a hundred correct ones — the source of much of the training instability that is blamed on the optimizer. $\lVert\partial L/\partial s\rVert$ stays bounded, by $\sqrt2$, only because the softmax sits in front.

### 2. One update is not a training result

The Worked case took one step and the loss fell. That is not yet a training result, because training repeats the step hundreds of times, and whether the repetition settles depends on the step size against the curvature of the loss, which one step cannot show. On D1 with §4's decay, $\eta=5$ and $\eta=10$ both *raise* $L_\lambda$ on their first step, from $0.563262$ to $2.186$ and to $7.956$, and end in opposite places: $\eta=5$ near the minimum, $\eta=10$ collapsed at $\log2$ (§6). This section writes the gradient that starts every step, defines the step, and names the number that decides whether it can be repeated.

For one-hot target $y$, softmax plus cross-entropy gives the useful derivative

$$\frac{\partial L}{\partial s}=p-y.$$

Here it is $(-0.269,0.269)$: raise the correct logit and lower the other. Backpropagating this vector computes gradients; the optimizer converts them into an update. SGD, momentum, and Adam therefore change the *update rule*, not the model's forward definition. The chain that carries $p-y$ back to $W_1$ is worked in full in the Worked case above, and the general machinery is [[02-foundations/calculus-backprop|2. Calculus & Backprop §3]].

Why that derivative is so clean is worth one line, because it is the reason the two blocks are drawn as one. The softmax Jacobian is $\partial p_i/\partial s_j=p_i(\delta_{ij}-p_j)$ and the loss derivative is $\partial L/\partial p_i=-y_i/p_i$; multiplying them makes every $p_i$ cancel and leaves $p-y$. Neither factor is pleasant on its own and their product is a subtraction, which is why implementations fuse the two and why a framework that lets you apply softmax twice by accident will train, slowly and wrongly, without ever raising an error.

> **The SGD step and its learning rate, defined.** A **gradient-descent step** is an *update rule applied to the parameter vector* — a map $\theta\mapsto\theta'$, not a loss and not a direction. Three defining conditions. It moves **against the gradient of the loss it was given**, so what it descends is whatever objective the gradient came from (with weight decay, not the cross-entropy). It has a **step size $\eta$ chosen outside the derivative**, which is what makes $\eta$ a hyperparameter. And it is **a local statement only**: the guarantee $L(\theta')<L(\theta)$ holds for small enough $\eta$ and for no particular $\eta$ you happen to choose.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta},\qquad L(\theta')\approx L(\theta)-\eta\lVert g\rVert^2+\tfrac{\eta^2}{2}g^\top Hg$$
>
> where $g=\partial L/\partial\theta$, $H$ is the Hessian at $\theta$, and $\lambda_{\max}(H)$ is its largest eigenvalue — the curvature along the steepest direction. The second-order term is why descent can stop being descent. On a quadratic loss each step multiplies the error along every eigendirection of $H$ by $1-\eta\lambda_i$, so repeated steps converge only while $\lvert1-\eta\lambda_{\max}(H)\rvert<1$, that is, while $\eta<2/\lambda_{\max}(H)$ — the argument of [[02-foundations/optimization|4. Optimization §3]], written there with $\alpha$. Above that bound a single step can still lower the loss; what fails is repetition, since the error along the steepest direction grows by the factor $\lvert1-\eta\lambda_{\max}(H)\rvert>1$ at every step.
>
> - **Example**: D1 at $\eta=0.1$. The first-order term predicts $-\eta\lVert g\rVert^2=-0.159125$; the second-order term adds $\tfrac{\eta^2}{2}g^\top Hg=+0.0325$, with $H$ the cross-entropy's Hessian at the catalog weights, so the quadratic model predicts $-0.1267$ against the $-0.1292$ the step delivers. With the $\eta^2$ term the model misses by only $0.0025$; the rest is higher-order.
> - **Non-example**: "SGD" with the full dataset in one batch, which is what this page runs. Stochastic gradient descent means the gradient is a *sample estimate*; D1 has one sample, so every gradient here is exact and none of the noise arguments about SGD apply. A paper calling full-batch descent "SGD" is not wrong in code and is wrong in its analysis.
> - **Non-example**: Adam. It is not this rule with a different $\eta$ — it rescales each coordinate by a running second moment, so its effective per-coordinate step is not $\eta$ and the $2/\lambda_{\max}(H)$ bound does not transfer. Comparing "the same learning rate" across optimizers compares nothing.
> - **Why it matters**: $2/\lambda_{\max}(H)$ is a *measurable* number, not a rule of thumb, and §6 measures it on D1 and finds it to four significant figures. The optimizer families are [[02-foundations/optimization|4. Optimization §3]].

### 3. Training, validation, and test answer different questions

A number from a training run answers one of three questions, and D1 shows why they cannot be merged. It has one sample, so it has only a training loss, and §6's sweep ranks step sizes on that loss alone. Its row at $\eta=8$ has a cross-entropy of $5.9\times10^{-9}$, a perfect fit to the only data there is, while its regularised objective, $0.599431$, is four times the minimum, and nothing in the table can say whether the weights it reached would classify a second input. The three questions, and the data that answers each:

- training loss: can the parameters fit sampled training batches?
- validation metric: which checkpoint or hyperparameter should be selected?
- test metric: how did the already frozen decision perform on held-out data?

A validation set scores the candidates on data none of them was fit to, and the test set then scores only the one candidate that was picked. Repeated test-guided tuning leaks test information. A paper that reports its best seed without a predeclared selection rule estimates luck as well as method quality. The split discipline itself, including what counts as a leak, is [[02-foundations/ml-practice|9. ML Practice §1]].

The best-seed sentence has a size. If a method's score varies from seed to seed roughly normally with standard deviation $\sigma$, the best of $k$ seeds lands on average $1.163\sigma$ above the method's mean for $k=5$ and $1.539\sigma$ for $k=10$ — the expected maximum of $k$ standard normal draws. At $\sigma=0.5$ points the best of five reports about $0.58$ points that no rerun will reproduce, the size of many claimed gains. Report the mean and spread over all seeds, or declare the selection rule before looking; what seed-to-seed spread does to a small gain is [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §3]]. Robot results are usually success rates over a few trials, and there the spread comes from the trial count itself: $9$ successes in $10$ trials carries a Wilson interval of $[0.596,\ 0.982]$ ([[02-foundations/ml-practice|9. ML Practice]]'s worked case, part 4).

### 4. Regularization and scaling are claims with controls

Cross-entropy on one separable point has no minimiser: the loss falls monotonically as the logits run to infinity, so no step size can be too large for it, and a step-size sweep on it measures nothing (self-check 5). Something has to give the objective a floor at a finite $\theta^\ast$ before a stability boundary can exist, and on D1 that is weight decay, one of several ways to regularise. Weight decay, augmentation, dropout, early stopping, more data, and more compute can all improve a result through different mechanisms. A scaling claim needs axes—parameters, data, compute—and a controlled comparison. “Our larger model is better” does not identify which axis caused the gain. How compute is counted from the other two axes, $C\approx6ND$, and how a fixed budget is split between them are [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §6–§7]].

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
> - **Why it matters**: it is what gives D1 the finite minimum that §6's step sizes can overshoot, $L^\ast=0.140339$ at $\lambda=0.1$, and a larger $\lambda$ changes the curvature at that minimum, which problem 4 measures. Regularization as an umbrella term is [[02-foundations/ml-practice|9. ML Practice §2]].

### 5. How to read a training recipe

A reported number is the output of a whole recipe, and each item below is on the list because changing it alone changes that number. Extract: data mixture and split; preprocessing; initialization; objective and coefficients; optimizer and schedule; batch size and number of updates; precision and hardware; checkpoint selection; seeds and uncertainty. Then ask which choices are essential by reading ablations. This is the operational bridge to [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]], and [[01-canonical-papers/notes/1-foundations/adam|Adam]]. Three of those items are given numbers on the sub-lectures: initialization per layer in [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §1]], precision per parameter in [[03-deep-learning/foundations/training-at-scale|1.3 §4]], and hardware per operation in [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing §3]], with how to measure it before optimizing in [[03-deep-learning/foundations/gpu-computing|1.4 §7]].

D1 shows three of them. **Preprocessing**: feed the same weights $2x=(2,4)$ instead of $x$ and, because a ReLU network with zero biases is positively homogeneous, every logit doubles to $s=(4,2)$ and the loss falls from $0.313262$ to $0.126928$ with no weight changed — an input scaled one way in training and another at test time is a different model. **The objective's coefficients**: the same catalog weights score $0.563262$ at $\lambda=0.1$ (§4), so a loss quoted without its $\lambda$ cannot be compared with one that has it. **The optimizer and the number of updates**: after the same $200$ steps, $\eta=0.1$ still sits at $0.143118$ while $\eta=0.5$ has reached the minimum $0.140339$ (§6), so "trained for 200 steps" says little without the step size. Data, checkpoint selection and seeds are §3's questions, and the vocabulary a paper uses for the rest — warmup and cosine schedules, decoupled weight decay, gradient accumulation, weight averaging — is [[02-foundations/ml-practice|9. ML Practice §6]].

An ablation is how a reader learns which item carries the result: change one, hold the others and the training budget fixed, and report the difference with its spread ([[06-research-practice/experimental-design-reproducibility|2. Experimental Design §5]]). Each of the four notes above has such an item. AlexNet's recipe includes dropout of $0.5$ and heavy augmentation; ResNet puts batch normalization after every convolution and uses no dropout; the Transformer's post-norm layout depends on its learning-rate warmup, and removing the warmup cost most of the quality in Xiong et al.'s ablation, BLEU $8.45$ against about $34$ (why warmup protects that layout is [[03-deep-learning/foundations/training-at-scale|1.3 §9]]); and Adam's defaults, $\beta_1=0.9$ and $\beta_2=0.999$, are hyperparameters a recipe has to state even when it keeps them.

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
| $3$ | $0.140345$ | $0.9678$ | 1 | just below the edge, $2/\lambda_{\max}(H)=3.0179$ |
| $5$ | $0.149517$ | $0.9867$ | 1 | oscillating above the minimum |
| $8$ | $0.599431$ | $1.0000$ | 1 | cross-entropy $5.9\times10^{-9}$, norm large: bouncing |
| $10$ | $0.693147$ | $0.5000$ | 3 | collapsed; $\log 2$ is the give-up loss |
| $12$ | diverged at step 15 | — | — | overflow |
| $20$ | diverged at step 9 | — | — | overflow |

<svg viewBox="0 0 560 358" style="max-width:100%;height:auto" role="img" aria-label="Two panels sharing a logarithmic step-size axis from 0.01 to 20. (a) D1's regularised loss after 200 steps at each step size of the sweep table: 0.5 to 2 settle on L* = 0.140339, 3 sits at the edge 2 over lambda-max = 3.018, 5 oscillates, 8 is flung out at 0.599431, 10 collapses to log 2 = 0.693147, 12 and 20 overflow. (b) The factor |1 - eta lambda-max| = |1 - 0.6627 eta| by which one step scales the error along the steepest direction: zero at 1.509, 0.988 at 3, crossing 1 at 3.018, 2.31 at 5.">
  <defs><marker id="aSBe" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) L<tspan dy="3" font-size="10">λ</tspan><tspan dy="-3" dx="3">after 200 steps, at each η of the table</tspan></text>
  <line x1="58" y1="188" x2="540" y2="188" stroke="currentColor" stroke-width="1"/>
  <line x1="58" y1="34" x2="58" y2="188" stroke="currentColor" stroke-width="1"/>
  <line x1="54" y1="188.0" x2="58" y2="188.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="191.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="54" y1="149.5" x2="58" y2="149.5" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="153.0" font-size="10" fill="currentColor" text-anchor="end">0.2</text>
  <line x1="54" y1="111.0" x2="58" y2="111.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="114.5" font-size="10" fill="currentColor" text-anchor="end">0.4</text>
  <line x1="54" y1="72.5" x2="58" y2="72.5" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="76.0" font-size="10" fill="currentColor" text-anchor="end">0.6</text>
  <line x1="54" y1="34.0" x2="58" y2="34.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="37.5" font-size="10" fill="currentColor" text-anchor="end">0.8</text>
  <line x1="58" y1="54.6" x2="540" y2="54.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <line x1="58" y1="79.6" x2="540" y2="79.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="4 3"/>
  <line x1="58" y1="161.0" x2="540" y2="161.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <text x="62" y="50.6" font-size="10.5" fill="currentColor">log 2 = 0.693147: gave up</text>
  <text x="62" y="75.6" font-size="10" fill="currentColor" fill-opacity="0.75">start 0.563262</text>
  <text x="62" y="157.0" font-size="10.5" fill="currentColor">L* = 0.140339</text>
  <line x1="420.1" y1="112" x2="420.1" y2="322" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 3"/>
  <text x="420.1" y="107" font-size="10.5" fill="currentColor" text-anchor="middle">2/λ<tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H) = 3.018</tspan></text>
  <circle cx="58.0" cy="138.8" r="3.2" fill="currentColor"/>
  <circle cx="204.0" cy="160.4" r="3.2" fill="currentColor"/>
  <circle cx="306.1" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="350.0" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="394.0" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="419.7" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="452.1" cy="159.2" r="3.2" fill="currentColor"/>
  <circle cx="481.9" cy="72.6" r="3.2" fill="currentColor"/>
  <circle cx="496.0" cy="54.6" r="3.2" fill="currentColor"/>
  <line x1="507.6" y1="86" x2="507.6" y2="37" stroke="currentColor" stroke-width="1.4" marker-end="url(#aSBe)"/>
  <line x1="540.0" y1="86" x2="540.0" y2="37" stroke="currentColor" stroke-width="1.4" marker-end="url(#aSBe)"/>
  <text x="540" y="29" font-size="10.5" fill="currentColor" text-anchor="end">12 and 20: overflow</text>
  <text x="490.0" y="48.6" font-size="10.5" fill="currentColor" text-anchor="end">10: three dead units</text>
  <text x="474.9" y="76.1" font-size="10.5" fill="currentColor" text-anchor="end">8: CE 5.9·10⁻⁹, weights flung out</text>
  <text x="458.1" y="151.2" font-size="10.5" fill="currentColor">5: oscillates</text>
  <text x="64.0" y="142.8" font-size="10.5" fill="currentColor">0.01: 0.256, still descending</text>
  <text x="204.0" y="175.4" font-size="10.5" fill="currentColor" text-anchor="middle">0.1: 0.143</text>
  <text x="350.0" y="176.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.5–2 settle on L*</text>
  <line x1="306.1" y1="180.0" x2="394.0" y2="180.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="58.0" y1="188" x2="58.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <line x1="204.0" y1="188" x2="204.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <line x1="350.0" y1="188" x2="350.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <line x1="496.0" y1="188" x2="496.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <text x="12" y="224" font-size="11.5" fill="currentColor">(b) per-step factor on the steepest direction, |1 − η λ<tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H)|, λ</tspan><tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H) = 0.6627</tspan></text>
  <line x1="58" y1="322" x2="540" y2="322" stroke="currentColor" stroke-width="1"/>
  <line x1="58" y1="236" x2="58" y2="322" stroke="currentColor" stroke-width="1"/>
  <line x1="54" y1="322.0" x2="58" y2="322.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="325.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="54" y1="293.3" x2="58" y2="293.3" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="296.8" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <line x1="54" y1="264.7" x2="58" y2="264.7" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="268.2" font-size="10" fill="currentColor" text-anchor="end">2</text>
  <line x1="54" y1="236.0" x2="58" y2="236.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="239.5" font-size="10" fill="currentColor" text-anchor="end">3</text>
  <line x1="58" y1="293.3" x2="540" y2="293.3" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <polyline points="58.0,293.5 59.2,293.5 60.4,293.5 61.6,293.5 62.8,293.5 64.0,293.5 65.2,293.5 66.4,293.6 67.6,293.6 68.8,293.6 70.0,293.6 71.3,293.6 72.5,293.6 73.7,293.6 74.9,293.6 76.1,293.6 77.3,293.6 78.5,293.6 79.7,293.6 80.9,293.6 82.1,293.6 83.3,293.6 84.5,293.6 85.7,293.6 86.9,293.6 88.1,293.6 89.3,293.6 90.5,293.7 91.7,293.7 92.9,293.7 94.1,293.7 95.4,293.7 96.6,293.7 97.8,293.7 99.0,293.7 100.2,293.7 101.4,293.7 102.6,293.7 103.8,293.7 105.0,293.7 106.2,293.7 107.4,293.7 108.6,293.8 109.8,293.8 111.0,293.8 112.2,293.8 113.4,293.8 114.6,293.8 115.8,293.8 117.0,293.8 118.2,293.8 119.5,293.8 120.7,293.8 121.9,293.9 123.1,293.9 124.3,293.9 125.5,293.9 126.7,293.9 127.9,293.9 129.1,293.9 130.3,293.9 131.5,293.9 132.7,294.0 133.9,294.0 135.1,294.0 136.3,294.0 137.5,294.0 138.7,294.0 139.9,294.0 141.1,294.0 142.3,294.1 143.6,294.1 144.8,294.1 146.0,294.1 147.2,294.1 148.4,294.1 149.6,294.1 150.8,294.2 152.0,294.2 153.2,294.2 154.4,294.2 155.6,294.2 156.8,294.2 158.0,294.3 159.2,294.3 160.4,294.3 161.6,294.3 162.8,294.3 164.0,294.3 165.2,294.4 166.5,294.4 167.7,294.4 168.9,294.4 170.1,294.4 171.3,294.5 172.5,294.5 173.7,294.5 174.9,294.5 176.1,294.6 177.3,294.6 178.5,294.6 179.7,294.6 180.9,294.7 182.1,294.7 183.3,294.7 184.5,294.7 185.7,294.8 186.9,294.8 188.1,294.8 189.3,294.8 190.5,294.9 191.8,294.9 193.0,294.9 194.2,295.0 195.4,295.0 196.6,295.0 197.8,295.1 199.0,295.1 200.2,295.1 201.4,295.2 202.6,295.2 203.8,295.2 205.0,295.3 206.2,295.3 207.4,295.3 208.6,295.4 209.8,295.4 211.0,295.5 212.2,295.5 213.4,295.5 214.7,295.6 215.9,295.6 217.1,295.7 218.3,295.7 219.5,295.8 220.7,295.8 221.9,295.9 223.1,295.9 224.3,295.9 225.5,296.0 226.7,296.1 227.9,296.1 229.1,296.2 230.3,296.2 231.5,296.3 232.7,296.3 233.9,296.4 235.1,296.4 236.3,296.5 237.5,296.6 238.8,296.6 240.0,296.7 241.2,296.7 242.4,296.8 243.6,296.9 244.8,296.9 246.0,297.0 247.2,297.1 248.4,297.2 249.6,297.2 250.8,297.3 252.0,297.4 253.2,297.5 254.4,297.5 255.6,297.6 256.8,297.7 258.0,297.8 259.2,297.9 260.4,298.0 261.6,298.0 262.9,298.1 264.1,298.2 265.3,298.3 266.5,298.4 267.7,298.5 268.9,298.6 270.1,298.7 271.3,298.8 272.5,298.9 273.7,299.0 274.9,299.1 276.1,299.3 277.3,299.4 278.5,299.5 279.7,299.6 280.9,299.7 282.1,299.8 283.3,300.0 284.5,300.1 285.7,300.2 286.9,300.4 288.2,300.5 289.4,300.6 290.6,300.8 291.8,300.9 293.0,301.1 294.2,301.2 295.4,301.4 296.6,301.5 297.8,301.7 299.0,301.8 300.2,302.0 301.4,302.2 302.6,302.3 303.8,302.5 305.0,302.7 306.2,302.9 307.4,303.0 308.6,303.2 309.8,303.4 311.1,303.6 312.3,303.8 313.5,304.0 314.7,304.2 315.9,304.4 317.1,304.6 318.3,304.8 319.5,305.1 320.7,305.3 321.9,305.5 323.1,305.8 324.3,306.0 325.5,306.2 326.7,306.5 327.9,306.7 329.1,307.0 330.3,307.3 331.5,307.5 332.7,307.8 333.9,308.1 335.1,308.4 336.4,308.6 337.6,308.9 338.8,309.2 340.0,309.5 341.2,309.9 342.4,310.2 343.6,310.5 344.8,310.8 346.0,311.2 347.2,311.5 348.4,311.9 349.6,312.2 350.8,312.6 352.0,312.9 353.2,313.3 354.4,313.7 355.6,314.1 356.8,314.5 358.0,314.9 359.2,315.3 360.5,315.7 361.7,316.2 362.9,316.6 364.1,317.0 365.3,317.5 366.5,318.0 367.7,318.4 368.9,318.9 370.1,319.4 371.3,319.9 372.5,320.4 373.7,320.9 374.9,321.5 376.1,322.0 377.3,321.5 378.5,320.9 379.7,320.3 380.9,319.7 382.1,319.1 383.4,318.5 384.6,317.9 385.8,317.3 387.0,316.7 388.2,316.0 389.4,315.3 390.6,314.7 391.8,314.0 393.0,313.3 394.2,312.5 395.4,311.8 396.6,311.1 397.8,310.3 399.0,309.5 400.2,308.7 401.4,307.9 402.6,307.1 403.8,306.3 405.0,305.4 406.2,304.6 407.4,303.7 408.7,302.8 409.9,301.9 411.1,300.9 412.3,300.0 413.5,299.0 414.7,298.0 415.9,297.0 417.1,296.0 418.3,294.9 419.5,293.9 420.7,292.8 421.9,291.7 423.1,290.5 424.3,289.4 425.5,288.2 426.7,287.0 427.9,285.8 429.1,284.5 430.3,283.3 431.6,282.0 432.8,280.6 434.0,279.3 435.2,277.9 436.4,276.5 437.6,275.1 438.8,273.7 440.0,272.2 441.2,270.7 442.4,269.1 443.6,267.6 444.8,266.0 446.0,264.4 447.2,262.7 448.4,261.0 449.6,259.3 450.8,257.5 452.0,255.8 453.2,253.9 454.4,252.1 455.6,250.2 456.9,248.3 458.1,246.3 459.3,244.3 460.5,242.3 461.7,240.2 462.9,238.1 464.1,236.0" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="464.0" y1="246" x2="474.0" y2="236" stroke="currentColor" stroke-width="1.2" marker-end="url(#aSBe)"/>
  <text x="478.0" y="246" font-size="10.5" fill="currentColor">grows past 3</text>
  <circle cx="376.1" cy="322.0" r="2.8" fill="currentColor"/>
  <text x="300" y="318" font-size="10.5" fill="currentColor" text-anchor="end">fastest: 1/λ<tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H) = 1.509</tspan></text>
  <line x1="303" y1="315" x2="371.1" y2="320" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <circle cx="419.7" cy="293.7" r="2.8" fill="currentColor"/>
  <text x="413.7" y="287.3" font-size="10.5" fill="currentColor" text-anchor="end">0.988 at η = 3</text>
  <circle cx="452.1" cy="255.7" r="2.8" fill="currentColor"/>
  <text x="466.1" y="259.7" font-size="10.5" fill="currentColor">2.31 at η = 5</text>
  <text x="62" y="287.3" font-size="10" fill="currentColor" fill-opacity="0.8">factor 1: below it the error shrinks, above it grows</text>
  <line x1="58.0" y1="322" x2="58.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="58.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">0.01</text>
  <line x1="204.0" y1="322" x2="204.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="204.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">0.1</text>
  <line x1="350.0" y1="322" x2="350.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="350.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="496.0" y1="322" x2="496.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="496.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">10</text>
  <line x1="306.1" y1="322" x2="306.1" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="394.0" y1="322" x2="394.0" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="419.7" y1="322" x2="419.7" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="452.1" y1="322" x2="452.1" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="481.9" y1="322" x2="481.9" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="507.6" y1="322" x2="507.6" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="540.0" y1="322" x2="540.0" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <text x="299" y="353" font-size="11" fill="currentColor" text-anchor="middle">step size η (log scale)</text>
</svg>

The sweep of the table on a logarithmic step-size axis. (a) After 200 steps every $\eta$ from $0.5$ to $2$ sits on $L^\ast=0.140339$, and $\eta=3$, just below the edge $2/\lambda_{\max}(H)=3.018$, has nearly arrived; $\eta=5$ oscillates at $0.149517$, $\eta=8$ is flung out to $0.599431$, $\eta=10$ collapses to $\log2=0.693147$, and $12$ and $20$ overflow. (b) Near the minimum one step multiplies the error along the steepest direction by $\lvert1-\eta\lambda_{\max}(H)\rvert$ with $\lambda_{\max}(H)=0.6627$: $0$ at $\eta=1.509$, $0.988$ at $\eta=3$, and above $1$ — growth — past $3.018$.

**Reading the sweep.** Four things the hand derivation could not have told you.

- **The useful boundary is the settling boundary, and it is exactly $2/\lambda_{\max}(H)$.** Rows $0.5$ through $2$ land on $L^\ast=0.140339$ to six figures; row $3$, at $0.140345$, misses it in the fifth, because at $\eta=3$ the figure's factor is $0.988$: each step removes only about $1\%$ of the error left along the steepest direction, and 200 steps are not enough. Part 3 of the listing walks to $\theta^\ast$, builds the $12\times12$ Hessian by finite differences and reports $\lambda_{\max}(H)=0.6627$, hence $2/\lambda_{\max}(H)=3.0179$. Bisecting the loop for the largest $\eta$ that still settles — the last lines of problem 4's template do it — gives $3.0180$. The textbook condition is not an approximation here; it is the measurement, to four significant figures.
- **Above that boundary the failure is silent before it is loud.** At $\eta=8$ the cross-entropy is $5.9\times10^{-9}$ — the model is *perfect* on its one training point — while $L_\lambda=0.599431$, four times the minimum, because the weights have been thrown far from the origin. A run monitored on accuracy alone shows nothing wrong. At $\eta=10$ all three hidden units are dead, $p=(0.5,0.5)$, and the loss sits at exactly $\log 2=0.693147$: every weight has been decayed to zero and the network predicts the prior. That number is worth recognising on sight, because a two-class run stuck at $0.693$ has not converged, it has given up.
- **One unit dies on purpose, and that is not the bug.** Every row from $\eta=0.1$ to $\eta=8$ ends with one dead unit, and so does the minimum itself: $\theta^\ast$ has $W_1$'s first row and $W_2$'s first column at zero. The backward pass wanted to push hidden unit 1 down ($\partial L/\partial z_1=+0.268941$) and the decay finished the job. Weight decay prunes; three dead units is collapse, one is the objective doing what it was asked.
- **The overflow boundary is not a boundary at all.** It is tempting to report the divergence threshold the way the settling threshold was reported. Part 3 scans $\eta$ from $10.40$ to $10.6095$ in steps of $0.0005$: the first divergence is at $\eta=10.4015$, and of the 417 grid points at or above it, 285 still survive 200 steps. Past the stability limit the iterate bounces across the ReLU kinks and whether it escapes is not monotone in $\eta$. A paper quoting "training diverges above $\eta=10.4$" on a plot of this kind is quoting one grid.

### Self-check

1. Which of $W_2$, $h$, $\eta$, $\lambda$, and the ReLU mask are parameters, which activations, which hyperparameters?
2. Why do implementations fuse softmax and cross-entropy into one block?
3. D1's $\partial L/\partial h$ has a zero third entry. Which number in the object caused it, and does a better prediction change it?
4. A two-class training run flatlines at loss $0.693$. What is the single most likely diagnosis, and what would confirm it?
5. Why does a learning-rate sweep on plain cross-entropy over one separable sample teach nothing about stability?

> [!tip]- Answers
> 1. Parameters: $W_2$ (and $W_1$). Activations: $h$, and the ReLU mask too — it is computed from the sample and kept for the backward pass, though no one learns it and no one chooses it (§1's non-example). Hyperparameters: $\eta$ and $\lambda$.
> 2. Their Jacobians are ugly separately — $p_i(\delta_{ij}-p_j)$ and $-y_i/p_i$ — and their product cancels to $p-y$. Fusing also avoids taking $\log$ of an underflowed probability.
> 3. $W_2$'s third column, $(0,0)$: unit 3 feeds nothing forward, so no error reaches it, and a better or worse prediction changes nothing — at these weights the zero is a property of the wiring, not of the error. It is not permanent: the column itself gets the gradient $(-0.268941,\ 0.268941)$, so one step at $\eta=0.1$ makes it $(0.026894,\ -0.026894)$ and the entry is no longer zero.
> 4. The model is predicting the class prior and learning nothing: $\log 2=0.693147$ is the loss of $p=(0.5,0.5)$. Confirm by printing the logits — if $s_1\approx s_2$ with tiny weights, the step size collapsed the network (the $\eta=10$ row); if the weights are large and $s$ is still flat, the wiring is broken.
> 5. That objective has no minimiser: the logits can run to infinity and the loss falls monotonically for every $\eta$ in the table. There is no minimum to overshoot, so nothing in the sweep can be unstable. Weight decay supplies the floor (§4).

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and [[03-deep-learning/lab-objects|0. Lab Objects]]. The object is D1 throughout; question 1 changes the input, 2 the logits, 3 the selection protocol, and 4 the target class and the decay, so none of the page's numbers can be copied.

1. **Draw.** The picture for a new input, $x=(2,-1)$, with the same weights and target class 1: every tensor with its shape and its values, the forward pass down one side and the backward pass up the other, as far as $\partial L/\partial z$. Mark the backward arrow the ReLU mask blocks and the one $W_2$'s zero column blocks, and say which of the two blocks is still there after one SGD step at $\eta=0.1$.
2. **Derive.** For logits $(0,\log 3)$ and target class 1, compute probabilities, loss, and $p-y$.
3. **Interpret.** A team tries ten augmentation settings, scores each once on the test set, and reports the best. Suppose none of the ten is really better than the others, and the test score varies from run to run with $\sigma=0.4$ points. (a) Which boundary was crossed, and which split should have chosen the setting? (b) About how far above the method's true level does the reported number sit? (c) The chosen setting is rerun with a new seed and loses most of its gain. Is the method broken?
4. **Do.** Fill the `?` blanks, then re-run the lab with the target changed to **class 2** ($y=(0,1)$, so the catalog model starts *wrong*) and the decay raised to $\lambda=0.2$. Report (a) the starting $L_\lambda$; (b) the sweep over $\eta\in\{0.05,0.5,2,5,20\}$ at 200 steps, as a table of $L_\lambda$, dead units, and any divergence step; (c) the largest $\eta$ that still settles at the minimum, by bisection. Then run (b)'s $\eta=0.5$ row and the bisection once more with the target kept at class 2 but $\lambda$ back at $0.1$, and say which of the two changes moved the boundary relative to §6, and why.

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

> [!note]- How to draw it · 그리는 법
> - Draw both directions on the same picture: the forward pass down one side, the backward pass up the other.
> - Label every tensor with its shape, batch dimension included. An unlabelled arrow is where a shape error hides, and a shape error is the most common reason a re-implementation silently trains the wrong model.
> - Draw the ReLU as a gate on $z$, not on $h$. The mask $\mathbf 1[z>0]$ is read off the pre-activation and fixed for the sample before any gradient flows; drawing it after $h$ claims the backward pass can choose the mask, which it cannot.
> - Draw softmax and cross-entropy as one block. Separately each has an ugly Jacobian; together they emit $p-y$ (§2), and the block's output arrow is the only place that expression appears.
> - Draw no arrow from $L$ straight to $W_1$. The gradient reaches $W_1$ only through $W_2$ and then through the mask; that path is the whole of backpropagation, and a diagram with a shortcut is a diagram of a different algorithm.
> - Draw the biases and mark them *held at zero*: they are 5 of the architecture's 17 slots, but this page never trains them, so the step updates 12 numbers — the convention by which [[02-foundations/neural-network-basics|0.8 §2]] counts P1's 9 of 13.
> - Label each zero in $\partial L/\partial z$ with its cause. A zero from the mask means the sample switched the unit off; a zero from a zero column of $W_2$ means the weights carry nothing back yet. The two causes behave differently after a step, and a drawing that does not tell them apart cannot answer the Draw item.

> [!tip]- Solutions
> 1. Forward: $z=W_1x=(2,-1,2)$, so the mask is $(1,0,1)$ and $h=(2,0,2)$; $s=W_2h=(0,2)$, $p=(0.119203,\ 0.880797)$, and $L=-\log0.119203=2.126928$ nats, a confident wrong answer. Backward: $p-y=(-0.880797,\ 0.880797)$, $\partial L/\partial h=W_2^\top(p-y)=(0.880797,\ -0.880797,\ 0)$ and $\partial L/\partial z=(0.880797,\ 0,\ 0)$. Unit 3's zero is $W_2$'s zero third column, as on the page; unit 2's is the mask, because $z_2=-1$. After one step the two part ways. Unit 3's column has a gradient of its own, $(p-y)\,h_3=(-1.761594,\ 1.761594)$, so it becomes $(0.176159,\ -0.176159)$ and the path back to unit 3 opens: $\partial L/\partial h_3=-0.202859$ at the new weights. Unit 2 gets no gradient in either layer — $h_2=0$ zeroes its column of $\partial L/\partial W_2$ and the mask zeroes its row of $\partial L/\partial W_1$ — so $z_2$ stays $-1$ and the mask still blocks it, for this input; at the catalog input $x=(1,2)$ the same unit is on. The zero column is a fact about the weights and lasts one step; the mask is a fact about the sample.
> 2. $p=(1/4,3/4)$, $L=-\log(1/4)=1.386$, $p-y=(-3/4,3/4)$.
> 3. (a) The test set became part of model selection, so the reported test result is no longer an untouched estimate; a validation split should have chosen the setting, and the test set should have scored only the chosen one, once. (b) The best of ten equally good runs sits on average $1.539\sigma$ above their mean (§3), so $1.539\times0.4=0.62$ points of the reported number are selection. (c) No. A drop of that size is what picking the best of ten predicts; the rerun is the honest estimate.
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
>    (c) Bisection gives $1.9801$, and $L^\ast=0.235806$. With class 2 at $\lambda=0.1$ the $\eta=0.5$ row reads $0.140339$ and bisection gives $3.0180$, §6's numbers exactly, so the flip moved nothing: swapping the two rows of $W_2$ turns the class-2 objective into the class-1 objective without changing $\lVert\theta\rVert^2$, so the two share their minimum value and the curvature there, and the flip changes only the path, which starts wrong. The decay moved the boundary **down** from $3.0180$, because $\lambda_{\max}(H)$ at the new minimum is $1.0100$ instead of $0.6627$. The decay term itself adds $0.1$ of that rise, since its Hessian is $\lambda I$ and lifts every eigenvalue by $\lambda$; the other $0.247$ is the cross-entropy's own curvature, larger because the heavier decay leaves the prediction less confident, $p=0.937$ on the target against $0.968$, where the softmax bends more. Heavier regularization is not a free way to stabilise training — it buys a floor for the loss and pays for it with a tighter step-size ceiling. The $\eta=5$ row is the same $\log 2$ collapse as §6's $\eta=10$ row, reached at half the step size.

### Sources

- A. Krizhevsky, I. Sutskever & G. E. Hinton, "ImageNet classification with deep convolutional neural networks," *NeurIPS* 2012 — dropout of 0.5 and augmentation in §5 ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet note]]).
- K. He, X. Zhang, S. Ren & J. Sun, "Deep residual learning for image recognition," *CVPR* 2016 — batch normalization after every convolution, no dropout ([[01-canonical-papers/notes/1-foundations/resnet|ResNet note]]).
- A. Vaswani et al., "Attention is all you need," *NeurIPS* 2017 — the post-norm layout and its warmup ([[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer note]]).
- R. Xiong et al., "On layer normalization in the Transformer architecture," *ICML* 2020 — the warmup ablation, BLEU 8.45 against about 34, as the Transformer note reports it.
- D. P. Kingma & J. Ba, "Adam: A method for stochastic optimization," *ICLR* 2015 — the defaults β₁ = 0.9 and β₂ = 0.999 ([[01-canonical-papers/notes/1-foundations/adam|Adam note]]).
- I. Loshchilov & F. Hutter, "Decoupled weight decay regularization," *ICLR* 2019 — the decoupled weight decay of §4's non-example, worked in [[02-foundations/optimization|4. Optimization]].
- E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association* 22(158):209–212 (1927) — the interval quoted in §3.
- D1 is a teaching object of [[03-deep-learning/lab-objects|0. Lab Objects]]; every number on this page was computed here, by hand or by the listing in §6.

## 한국어

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 *학습과 적응* 층을 여는 페이지로, "*저 패널을 프레임에 설치해*"에 들어가는 학습된 부품 모두의 밑에 있는 학습 루프다. 2단계 *패널과 프레임을 식별하는* 검출기부터 7단계 *끼움을 수행하는* 학습된 정책까지가 여기에 기댄다([[physical-ai-map|피지컬 AI 지도]]의 학습과 적응 띠에 이 페이지의 자리가 있다). 학습된 부품의 숫자는 그 뒤의 루프만큼만 믿을 수 있는데, 스텝 하나로는 루프가 보이지 않는다. 딥러닝 트랙의 고정 2층 분류기 D1([[03-deep-learning/lab-objects|0. Lab Objects]])에서 $\eta=0.1$의 한 스텝은 gradient가 약속한 감소의 $81\%$를 내고, $2/\lambda_{\max}(H)=3.018$ 아래의 보폭은 스텝만 충분하면 모두 같은 최소점에 정착하며, $\eta=8$은 하나뿐인 샘플에 cross-entropy $5.9\times10^{-9}$로 맞추면서 가중치를 원점에서 멀리 던지고, $\eta=10$은 $\log2=0.693$에서 포기한다(§6). $\eta$, $\lambda$, 스텝 수 없이 인용한 loss는 이 가운데 아무것도 보여 주지 않는다. 이 페이지의 softmax, cross-entropy, $p-y$는 이미지마다 배치에서 자기 캡션을 골라내는 [[03-deep-learning/vlm/index|3. VLM §2]]에서 다시 나오고, 이 페이지의 갱신이 [[03-deep-learning/vla/index|4. VLA §2]]와 [[05-construction-robotics/imitating-contact|10. 접촉 모방 §2]]의 행동 복제 정책을 학습시키며, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 4의 딥러닝 쪽을 여는 페이지로 딥러닝 1–3회차에 해당하고 [[02-foundations/rl-robot-learning|7.5 RL §1과 §4]] 다음에 읽는다. 이 페이지를 마치면 신경망에 입력 하나를 앞으로, 갱신 하나를 뒤로 손으로 흘릴 수 있고, 루프가 되풀이할 수 있는 보폭을 잴 수 있으며, 학습 recipe가 자기 숫자에 의미를 주려면 무엇을 적어야 하는지 나열할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 세 회차이고, [[03-deep-learning/index|딥러닝 학습 일정]]의 1–3행이다. 앞의 두 회차가 첫 읽기다. **1회차:** 계속 쓰는 대상, 그림, 계산 절을 풀이를 가리고 손으로 한다. $L=0.313262$ nat, $p-y=(-0.268941,\,0.268941)$, $\eta=0.1$에서 $\Delta L=-0.129177$이 나오면 된다. **2회차:** §1–§5를 읽고 — §1의 접힌 복습은 softmax나 cross-entropy가 흐릿할 때만 연다 — 스스로 점검 1–3과 5, 과제 1–3을 한다. **3회차:** §6의 코드를 돌리고 그림과 네 가지 읽기를 읽은 뒤 과제 4를 한다. 끝으로 $2/\lambda_{\max}(H)=3.018$이 왜 정착하는 가장 큰 보폭인지, 그리고 — §6이 있어야 풀리는 스스로 점검 4 — $0.693$에 멈춘 2클래스 run이 왜 수렴한 것이 아니라 포기한 것인지를 자기 말로 설명한다.

### 계속 쓰는 대상: D1

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D1**, 곧 딥러닝 트랙의 고정 2층 분류기를 쓴다.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}.$$

순전파: $W_1x=(1,2,1)$, $h=\operatorname{ReLU}(W_1x)=(1,2,1)$, $s=W_2h=(2,1)$, $p=\operatorname{softmax}(s)$. 그림에 $2\rightarrow3\rightarrow2$ shape를 적는다. [[02-foundations/lab-plants|0.6 Lab Plants]]의 2층 연습 신경망 **P1**($2\to3\to1$ MSE)과 다른 장치다.

**bias는 0에 고정한다.** 이 구조에는 층마다 bias 벡터 $b_1\in\mathbb R^3$, $b_2\in\mathbb R^2$가 있고, 이 페이지는 그 다섯 성분을 모두 0에 고정한다. 갱신하지도 decay하지도 않는다. 그래서 D1이 학습하는 파라미터는 $W_1$의 여섯 성분과 $W_2$의 여섯 성분, $12$개이고, 구조의 자리는 $17$개다. [[02-foundations/neural-network-basics|0.8 §2]]가 P1을 자리 $13$개 가운데 가중치 $9$개로 세는 것과 같은 관례다. 프레임워크의 선형층은 기본값으로 bias도 학습하는데, bias까지 학습하면 $\eta=0.1$의 한 스텝이 다른 곳, 곧 $s=(2.353964,\ 0.646036)$, $\Delta L=-0.146696$에 닿는다. 학습하는 숫자가 $17$개인 다른 모델일 뿐, 어느 쪽 계산의 오류도 아니다.

**표기.** 이 페이지는 logit을 $s$, 클래스 수를 $C$, 보폭을 $\eta$, weight decay를 $\lambda$로 쓴다. [[02-foundations/calculus-backprop|2. 미적분과 역전파 §4.1]]과 [[02-foundations/neural-network-basics|0.8 §6]]은 logit을 $z$, 클래스 수를 $K$로 쓴다(여기서 $z$는 pre-activation이므로 2 §4.1의 $\partial L/\partial z=p-y$가 이 페이지의 $\partial L/\partial s$다). 0.8 §3과 [[02-foundations/optimization|4. 최적화 §3]]은 일반 규칙에서 보폭을 $\alpha$로 쓰는데, 4도 P1로 계산한 스텝에서는 이미 $\eta$를 쓴다. 그리고 4는 Hessian의 고유값을 $\lambda_i$로 쓴다. 그래서 이 페이지에서 곡률은 언제나 $\lambda_{\max}(H)$이고, 맨 $\lambda$로 쓰지 않는다.

이 페이지에서 정답은 항상 1번 클래스이므로 $y=(1,0)$이고, 아래의 모든 숫자는 $W_1$, $W_2$, $x$, $y$와 0인 bias만으로 나온다.

*범위: 이 페이지는 입력 하나에서 파라미터 갱신 하나까지의 형식 붙은 경로 — shape, softmax, cross-entropy, 역전파, SGD 한 스텝, 그리고 그 스텝이 지켜야 하는 보폭 — 와 학습 주장이 갖춰야 할 증거를 가르친다. 미분이 어디서 오는지는 가르치지 않는다. 그것은 [[02-foundations/calculus-backprop|2. 미적분과 역전파 §2]]다. optimizer 자체(momentum, Adam, schedule)도 아니다. 그것은 [[02-foundations/optimization|4. 최적화 §3]]다. 숫자를 결과로 바꾸는 실험 절차도 아니다. 그것은 [[02-foundations/ml-practice|9. ML 실무 §4]]다. 2층 MLP 너머의 구조도 아니다. convolution과 patch token은 [[03-deep-learning/computer-vision/index|2. 컴퓨터비전]], attention은 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]]와 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]다. 이 페이지 위에 서는 이 모듈의 하위 강의는 [[03-deep-learning/foundations/sequence-models|1.1 시퀀스 모델]], [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]], [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습]], [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산]] 넷이다.*

### 그림으로 먼저 보기

<svg viewBox="0 0 560 588" style="max-width:100%;height:auto" role="img" aria-label="D1의 순전파를 왼쪽 열에 텐서마다 shape와 값을 달아 내려 그리고, 가운데에 가중치와 0에 고정한 bias를, 오른쪽 열에 gradient 값을 단 역전파를 올려 그리고, 맨 아래 띠에 가중치 12개에 대한 SGD 한 스텝의 예측 변화 -0.159125와 실제 변화 -0.129177을 그린 그림">
  <defs><marker id="aD1k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="22" font-size="12" fill="currentColor">D1 · 정답 1번 클래스, y = (1, 0) · 실선: 순전파 · 점선: 역전파</text>
  <text x="75" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">순전파 · activation</text>
  <text x="265" y="46" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">파라미터 · bias는 0에 고정</text>
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
  <line x1="12" y1="516" x2="548" y2="516" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <text x="12" y="534" font-size="11" fill="currentColor">SGD 한 스텝, η = 0.1, 가중치 12개만: s → (2.299452, 0.700548), L → 0.184085</text>
  <text x="12" y="557" font-size="11" fill="currentColor">예측, −η‖g‖²</text>
  <rect x="150" y="548" width="200" height="11" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="356" y="557" font-size="11" fill="currentColor">−0.159125</text>
  <text x="12" y="577" font-size="11" fill="currentColor">실제, ΔL</text>
  <rect x="150" y="568" width="162.4" height="11" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="1"/>
  <text x="318.4" y="577" font-size="11" fill="currentColor">−0.129177, 예측의 81%</text>
</svg>

카탈로그 숫자로 그린 D1의 계산 절이고, 정답은 1번 클래스다. 순전파는 왼쪽 열을 따라 $x=(1,2)\to z=(1,2,1)\to h=(1,2,1)\to s=(2,1)$로 내려가 softmax와 cross-entropy를 합친 한 블록에서 $p_1=0.731059$, $L=0.313262$ nat을 내고, 가운데에는 가중치와 0에 고정한 bias가 있다. 역전파는 오른쪽 열을 따라 $\partial L/\partial s=p-y=(-0.268941,0.268941)$에서 $\partial L/\partial h=(0.268941,-0.268941,0)$ — 0은 $W_2$의 비어 있는 3열 때문이다 — 으로, 다시 ReLU mask $\mathbf 1[z>0]=(1,1,1)$을 지나 $\partial L/\partial W_1$로 올라가며, $L$에서 $W_1$으로 곧장 가는 화살표는 없다. 맨 아래 띠는 계산 절의 한 스텝, 곧 $\eta=0.1$에서 가중치 12개만 갱신한 결과다. loss는 $0.129177$ 줄어, gradient가 예측한 $0.159125$의 $81\%$다.

### 대상으로 한 번 끝까지

이것이 과제의 대상이다. 과제가 요구하는 세 가지 — 순전파, 역전파, 한 스텝 — 를 카탈로그 숫자로 여기서 먼저 한다. 그러면 과제는 입력과 정답 클래스와 손잡이를 바꾸는 일이지 첫 유도가 아니다. 이 페이지의 로그는 전부 자연로그이므로 loss의 단위는 nat이다.

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

세 번째 성분이 정확히 0인데 $W_2$의 세 번째 열이 $(0,0)$이기 때문이다. 이 가중치에서 은닉 유닛 3은 앞으로 아무것도 내보내지 않으므로 오차가 아무리 커도 그 유닛으로는 되돌아오지 않고, 이번 스텝에서 $W_1$의 세 번째 행의 gradient는 0이다. 이 막힘은 영구적이지 않다. $W_2$의 세 번째 열은 위 행렬에서 보듯 자기 gradient $(-0.268941,\ 0.268941)$을 가지는데, 유닛 3이 켜져 있기($h_3=1$) 때문이다. 그래서 한 스텝이 그 열에 $(0.026894,\ -0.026894)$을 써 넣고, 유닛 3으로 돌아가는 길이 열린다. mask(여기서는 전부 1)를 걸고 $x=(1,2)$와 한 번 더 외적하면

$$\frac{\partial L}{\partial W_1}=\begin{pmatrix}0.268941&0.537883\\-0.268941&-0.537883\\0&0\end{pmatrix}.$$

**SGD 한 스텝.** 규칙은 $\theta\leftarrow\theta-\eta\,\partial L/\partial\theta$이고, 가중치 12개에만 적용하며 bias는 0에 둔다. $\eta=0.1$이면 logit이 $s=(2.299452,\ 0.700548)$로 옮겨 가는데, $\pm0.299452$로 대칭인 이유는 두 클래스에서 $p-y$가 반대칭이기 때문이다. 그리고

$$p=(0.831865,\ 0.168135),\qquad L=0.184085,\qquad \Delta L=-0.129177\ \text{nat}.$$

1차 예측값은 $-\eta\lVert g\rVert^2=-0.1\times1.591249=-0.159125$이므로 이 스텝은 gradient가 약속한 값의 $81\%$를 실제로 냈다. 그 차이가 곡률이다. §2의 2차 항을 더하면 예측이 $-0.1267$로 옮겨 가서, 실제의 $-0.1292$와 $0.0025$밖에 차이 나지 않는다. 곡률 항은 $\eta^2$으로, 약속된 감소는 $\eta$로만 자라므로 스텝이 충분히 크면 곡률이 이긴다. §6은 되풀이한 스텝이 더는 정착하지 않게 되기 전까지 $\eta$를 얼마나 키울 수 있는지 잰다.

### 1. 모델은 형식이 붙은 계산이다

*한 문장으로:* 말로 쓴 모델은 텐서마다 모양을 붙이고 숫자마다 학습되는 것·계산되는 것·고르는 것으로 나눈 뒤에야 검증할 수 있다. D1에서는 그렇게 형식을 붙이면 logit 두 개가 두 줄 만에 확률과 loss가 된다.

*이 절에서 하나만 가져간다면:* 세 갈래 구분이다. 파라미터는 optimizer가, activation은 입력이, 하이퍼파라미터는 사람이 쓴다. 이 구분이 주장이 "더 작다", "학습이 싸다", "튜닝이 싸다" 중 무엇인지를 정한다.

구조를 설명하는 글은 shape를 붙인 뒤에야 검증할 수 있다. 배치 크기 $B$이면 $X\in\mathbb R^{B\times2}$, $H\in\mathbb R^{B\times3}$, $S\in\mathbb R^{B\times2}$다. 그 안의 숫자를 아래의 세 갈래로 나누지 않으면 파라미터 수와 효율에 대한 주장을 믿을 수 없게 된다.

> **파라미터·activation·하이퍼파라미터, 세 갈래의 정의.** 셋 다 *같은 프로그램 안의 숫자*라서 헷갈린다. 구분은 **무엇이 그 값을 바꾸는가**다. **파라미터**는 optimizer가 쓰는 숫자다. gradient가 있고, "모델 크기"에 세어지고, checkpoint에 저장된다. D1에서는 $W_1$과 $W_2$의 12개다. bias 다섯 개는 0에 고정되어 한 번도 쓰이지 않으므로, 이 페이지에서는 파라미터가 아니라 구조의 자리다. **activation**은 입력을 흘려서 만들어지는 숫자다. 자기 gradient를 저장하지 않고, 샘플마다 바뀌며, 역전파를 위해 보관해야 하므로 학습 메모리 가운데 배치와 context에 따라 커지는 부분이 된다([[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §5]]). D1의 $z$, $h$, $s$, $p$가 그것이다. **하이퍼파라미터**는 경사하강 밖에서 사람이나 탐색이 고르는 숫자다. learning rate $\eta$, decay $\lambda$, batch 크기, 은닉 유닛 수.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta}\qquad\text{— }\theta\text{는 파라미터, }\eta\text{는 하이퍼파라미터, }L\text{은 activation에서 나왔다}$$
>
> 갱신식 하나에 셋이 모두 들어 있으므로, 이 식을 왼쪽부터 읽는 것이 논문에 나온 임의의 숫자를 분류하는 가장 빠른 방법이다.
>
> - **예**: D1의 은닉 폭 3은 하이퍼파라미터, 거기서 나온 $h=(1,2,1)$은 activation, 그것을 만든 $W_1$은 파라미터다. 폭을 바꾸면 파라미터 수가 바뀌고, 입력을 바꾸면 activation만 바뀐다.
> - **비예**: ReLU mask $\mathbf 1[z>0]=(1,1,1)$. activation이다. 아무도 학습하지 않으니 파라미터가 아니고, 아무도 고르지 않았으니 하이퍼파라미터도 아니다. 샘플에서 유도된 값이다. 그래서 "sparsity"를 보고하는 논문은 *무엇의*, *어떤 데이터에서의* sparsity인지 말해야 한다.
> - **비예**: Adam의 optimizer state. optimizer가 쓰고 checkpoint에 저장되니 파라미터처럼 보이지만 순전파에 쓰이지 않으므로 모델 크기에 세면 안 된다. 파라미터 수 대신 "checkpoint 크기"를 인용하는 논문이 세고 있는 것이 이것이다.
> - **왜 중요한가**: "우리 모델이 3배 작다"는 파라미터 주장, "학습 메모리가 3배 적다"는 activation 주장, "튜닝이 3배 싸다"는 하이퍼파라미터 주장이다. 서로 다른 세 실험이고, 이를 뭉뚱그린 논문은 셋 중 어느 것도 하지 않은 것이다. 실험 절을 읽기 위한 같은 구분은 [[02-foundations/neural-network-basics|0.8 신경망 §5]]에 있다.

계산 절은 D1의 logit을 softmax와 cross-entropy로 $p$와 $L$로 바꾸었고, 두 사상의 정의는 기초 페이지에 완전하게 있다. 접힌 복습이 그것을 다시 적고, 그 뒤의 목록이 이 페이지가 덧붙이는 것을 드러내 둔다.

> [!note]- 복습 · Recap
> **Softmax**([[02-foundations/calculus-backprop|2. 미적분과 역전파 §4.1]], [[02-foundations/neural-network-basics|0.8 §6]])는 실수 logit을 확률 벡터로 보내는 사상이다. 파라미터가 있는 층이 아니라 함수다.
>
> $$p_i=\frac{e^{s_i}}{\sum_{j=1}^{C}e^{s_j}}$$
>
> $s\in\mathbb R^{C}$는 logit, $C$는 클래스 수다. 출력은 양수이고 합이 1이다. 평행이동 불변이라 $\operatorname{softmax}(s+c\mathbf 1)=\operatorname{softmax}(s)$이고, 따라서 logit의 차이만 정보를 나른다. 그래서 logit $C$개의 자유도는 $C-1$이고, 구현은 $e^{s_j}$가 overflow하지 않도록 먼저 $\max_j s_j$를 뺀다. 그리고 모든 $p_i$가 분모 하나를 공유하므로 logit의 순위가 곧 확률의 순위이고, softmax는 어느 클래스가 가장 큰지를 바꾸지 않는다. D1의 $s=(2,1)$과 $s=(102,101)$은 둘 다 $p=(0.731059,\ 0.268941)$을 준다.
>
> **Cross-entropy**([[02-foundations/neural-network-basics|0.8 §3]], [[02-foundations/information-theory|5. 정보이론 §2]])는 예측 분포 $p$를 정답 분포 $y$에 대해 채점한다.
>
> $$L=-\sum_{i=1}^{C}y_i\log p_i\ \ \xrightarrow{\ y\text{가 }c\text{에서 one-hot}\ }\ \ L=-\log p_c$$
>
> one-hot $y$가 정답 클래스의 항만 남기고 모두 0으로 만들기 때문이다. 정답의 음의 로그가능도이므로 이것을 최소화하는 것이 최대가능도 추정이고, 두 인자에 대해 비대칭이라 $H(y,p)\ne H(p,y)$이며 학습되는 쪽은 $p$다. D1은 $-\log0.731059=0.313262$ nat($0.451941$ bit)이다. 예측 자체의 엔트로피 $H(p)=0.582$ nat은 loss가 아니다. 예측이 얼마나 퍼져 있는지를 잴 뿐, 그 질량이 정답 위에 얼마나 있는지를 재지 않는다.

이 페이지가 그 정의에 덧붙이는 것:

- **Softmax는 신뢰도가 아니다.** $p_1=0.731$은 모델이 낸 숫자이지 측정된 빈도가 아니다. 그런 예측의 $73\%$가 실제로 맞는지는 **보정**(calibration)의 문제다. $0.73$으로 점수 매긴 사례들 가운데 사건이 $73\%$ 일어나면 그 모델은 보정되어 있다. 보정은 따로, reliability diagram과 그 한 숫자 요약인 기대 보정 오차(ECE)로 잰다([[04-robotics/human-intent-prediction|23. 사람 의도 예측 §4]]).
- **Cross-entropy는 accuracy가 아니다.** D1의 예측은 *맞다* — 1번 클래스의 확률이 더 크다 — 그런데 loss는 양수 $0.313$이다. accuracy가 그대로인 채 loss가 오를 수 있으므로 논문은 둘 다 보고해야 하고, 한쪽 기준의 early stopping은 다른 쪽 기준의 early stopping이 아니다.
- **Cross-entropy는 위로 유계가 아니다.** 확신에 찬 오답은 얼마든지 비쌀 수 있고, 확신에 찬 정답은 이미 가진 것보다 더 아끼지 못한다. 그래서 확신에 찬 예측을 받은 오라벨 샘플 하나가 정답 백 개보다 큰 loss를 낼 수 있고, optimizer 탓으로 돌려지는 학습 불안정의 상당 부분이 여기서 나온다. $\lVert\partial L/\partial s\rVert$가 $\sqrt2$로 묶이는 것은 앞에 softmax가 있기 때문일 뿐이다.

### 2. 한 번의 update는 학습 결과가 아니다

계산 절은 한 스텝을 밟았고 loss가 내려갔다. 그것은 아직 학습 결과가 아니다. 학습은 스텝을 수백 번 되풀이하고, 그 되풀이가 정착하는지는 loss의 곡률에 비해 보폭이 얼마나 큰지에 달렸는데, 한 스텝으로는 그것이 보이지 않는다. §4의 decay를 건 D1에서 $\eta=5$와 $\eta=10$은 둘 다 첫 스텝에 $L_\lambda$를 $0.563262$에서 각각 $2.186$과 $7.956$으로 *올리지만*, 끝나는 곳은 정반대다. $\eta=5$는 최소점 근처에서, $\eta=10$은 $\log2$로 붕괴한 채 끝난다(§6). 이 절은 모든 스텝을 시작하는 gradient를 적고, 스텝을 정의하고, 그 스텝을 되풀이할 수 있는지를 정하는 숫자를 이름 붙인다.

one-hot $y$에 대해 softmax와 cross-entropy를 합치면 $\partial L/\partial s=p-y$다. 여기서는 $(-0.269,0.269)$이므로 정답 logit은 올리고 다른 logit은 내린다. backprop은 gradient를 계산하고 optimizer가 update로 바꾼다. 그러므로 SGD, momentum, Adam이 바꾸는 것은 *갱신 규칙*이지 모델의 순전파 정의가 아니다. $p-y$가 $W_1$까지 되돌아가는 사슬은 위의 계산 절에 전부 적혀 있고, 일반 기계는 [[02-foundations/calculus-backprop|2. 미적분과 역전파 §3]]에 있다.

그 미분이 왜 그렇게 깨끗한지는 한 줄 적어 둘 만하다. 두 블록을 하나로 그리는 이유가 그것이기 때문이다. softmax의 Jacobian은 $\partial p_i/\partial s_j=p_i(\delta_{ij}-p_j)$이고 loss의 미분은 $\partial L/\partial p_i=-y_i/p_i$인데, 곱하면 $p_i$가 전부 약분되고 $p-y$만 남는다. 각각은 다루기 나쁘고 곱은 뺄셈 하나다. 구현이 둘을 융합하는 이유이고, softmax를 실수로 두 번 걸 수 있는 프레임워크가 오류 없이 느리고 틀리게 학습되는 이유이기도 하다.

> **SGD 스텝과 learning rate의 정의.** **경사하강 스텝**은 *파라미터 벡터에 적용되는 갱신 규칙*, 즉 $\theta\mapsto\theta'$인 사상이다. loss도 방향도 아니다. 정의 조건 셋. **자기가 받은 loss의 gradient 반대 방향으로** 움직이므로, 내려가는 대상은 그 gradient가 나온 목적함수다(weight decay가 있으면 cross-entropy가 아니다). 미분 밖에서 고른 **보폭**을 $\eta$로 가지며, 그래서 $\eta$가 하이퍼파라미터다. 그리고 **국소적인 진술일 뿐**이다. $L(\theta')<L(\theta)$ 보장은 충분히 작은 $\eta$에 대해 성립하지, 당신이 고른 특정 $\eta$에 대해 성립하지 않는다.
>
> $$\theta\leftarrow\theta-\eta\,\frac{\partial L}{\partial\theta},\qquad L(\theta')\approx L(\theta)-\eta\lVert g\rVert^2+\tfrac{\eta^2}{2}g^\top Hg$$
>
> $g=\partial L/\partial\theta$, $H$는 $\theta$에서의 Hessian, $\lambda_{\max}(H)$는 그 최대 고유값, 곧 가장 가파른 방향의 곡률이다. 하강이 하강이 아니게 될 수 있는 이유가 2차 항이다. 이차형식 loss에서는 스텝마다 $H$의 고유방향 각각의 오차에 $1-\eta\lambda_i$가 곱해지므로, 되풀이한 스텝은 $\lvert1-\eta\lambda_{\max}(H)\rvert<1$, 곧 $\eta<2/\lambda_{\max}(H)$인 동안만 수렴한다. [[02-foundations/optimization|4. 최적화 §3]]의 논증이고, 거기서는 $\alpha$로 쓴다. 이 경계 위에서도 한 스텝은 loss를 낮출 수 있다. 무너지는 것은 되풀이이고, 가장 가파른 방향의 오차가 스텝마다 $\lvert1-\eta\lambda_{\max}(H)\rvert>1$배로 자라기 때문이다.
>
> - **예**: $\eta=0.1$의 D1. 1차 항은 $-\eta\lVert g\rVert^2=-0.159125$를 예측하고, 2차 항이 $\tfrac{\eta^2}{2}g^\top Hg=+0.0325$를 더하므로($H$는 카탈로그 가중치에서의 cross-entropy Hessian) 이차 모형은 $-0.1267$을 예측하며, 실제 스텝은 $-0.1292$를 낸다. $\eta^2$ 항을 넣은 모형은 $0.0025$만 빗나가고, 나머지는 더 높은 차수의 몫이다.
> - **비예**: 전체 데이터를 한 배치로 넣은 "SGD" — 이 페이지가 돌리는 것이 바로 그것이다. stochastic gradient descent는 gradient가 *표본 추정치*라는 뜻인데, D1은 샘플이 하나라 모든 gradient가 정확하고 SGD의 잡음 논증은 하나도 적용되지 않는다. full-batch를 "SGD"라 부르는 논문은 코드에서는 틀리지 않고 해석에서는 틀린다.
> - **비예**: Adam. $\eta$만 다른 같은 규칙이 아니다. 좌표마다 2차 모멘트로 나누므로 실효 보폭이 $\eta$가 아니고 $2/\lambda_{\max}(H)$ 경계도 그대로 옮겨 가지 않는다. optimizer를 바꾸며 "같은 learning rate"를 비교하는 것은 아무것도 비교하지 않는 것이다.
> - **왜 중요한가**: $2/\lambda_{\max}(H)$는 어림이 아니라 *측정 가능한* 숫자이고, §6이 D1에서 유효숫자 네 자리까지 측정한다. optimizer 계열은 [[02-foundations/optimization|4. 최적화 §3]]이다.

### 3. Train·validation·test의 질문은 다르다

학습 run에서 나온 숫자는 세 질문 가운데 하나에 답하고, D1이 셋을 합칠 수 없는 이유를 보여 준다. 샘플이 하나뿐이라 train loss밖에 없고, §6의 sweep은 그 loss 하나로 보폭의 순위를 매긴다. $\eta=8$ 행의 cross-entropy는 $5.9\times10^{-9}$로, 가진 자료 전부에 완벽히 맞췄다. 그런데 정규화된 목적함수는 $0.599431$로 최솟값의 네 배이고, 그 가중치가 두 번째 입력을 맞게 분류할지는 표의 어떤 숫자도 말해 주지 못한다. 세 질문과 각각에 답하는 자료는 이렇다.

- train loss: 학습 배치를 맞출 수 있는가.
- validation: checkpoint와 hyperparameter 중 무엇을 고를 것인가.
- test: 이미 고정한 결정을 미사용 자료에서 평가하면 어떤가.

validation 집합은 어느 후보도 맞추는 데 쓰지 않은 자료로 후보들을 채점하고, test 집합은 그렇게 고른 후보 하나만 채점한다. test를 보며 계속 조정하면 test 정보가 학습 절차로 샌다. 미리 정한 선택 규칙 없이 가장 좋은 seed를 보고한 논문은 방법의 질과 함께 운도 추정한 것이다. 분할 규율과 무엇이 유출인지는 [[02-foundations/ml-practice|9. ML 실무 §1]]에 있다.

가장 좋은 seed라는 문장에는 크기가 있다. 한 방법의 점수가 seed마다 표준편차 $\sigma$로 대략 정규분포를 따르면, seed $k$개 중 최고는 평균적으로 방법의 평균보다 $k=5$일 때 $1.163\sigma$, $k=10$일 때 $1.539\sigma$ 위에 놓인다. 표준정규 표본 $k$개의 최댓값의 기댓값이다. $\sigma=0.5$포인트면 다섯 개 중 최고는 다시 돌려도 재현되지 않는 약 $0.58$포인트를 보고하고, 이는 흔히 주장되는 개선의 크기다. 모든 seed의 평균과 퍼짐을 보고하거나, 보기 전에 선택 규칙을 선언한다. seed 사이의 퍼짐이 작은 개선에 무엇을 하는지는 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §3]]에 있다. 로봇 결과는 대개 몇 번의 시행에서 나온 성공률이고, 거기서는 퍼짐이 시행 수 자체에서 온다. $10$번 중 $9$번 성공의 Wilson 구간은 $[0.596,\ 0.982]$다([[02-foundations/ml-practice|9. ML 실무]]의 계산 절 4번).

### 4. 정규화와 scaling은 통제가 필요한 주장이다

분리 가능한 점 하나에 대한 cross-entropy에는 최소점이 없다. logit이 무한으로 달아나면서 loss가 단조 감소하므로 어떤 보폭도 너무 클 수 없고, 거기서 한 보폭 sweep은 아무것도 재지 못한다(스스로 점검 5). 안정성 경계가 존재하려면 무언가가 목적함수에 유한한 $\theta^\ast$의 바닥을 줘야 하고, D1에서 그것은 여러 정규화 방법 가운데 하나인 weight decay다. weight decay, augmentation, dropout, early stopping, 데이터와 compute 증가는 서로 다른 기제로 결과를 바꾼다. scaling 주장은 parameter·data·compute 축을 분리해야 한다. “우리 모델이 더 크니 더 좋다”는 어느 축이 이득을 냈는지 밝히지 못한다. compute를 나머지 두 축으로 세는 식 $C\approx6ND$와, 고정된 예산을 두 축에 나누는 법은 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §6–§7]]에 있다.

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
> - **왜 중요한가**: §6의 보폭들이 넘어설 수 있는 유한한 최소점, 곧 $\lambda=0.1$에서 $L^\ast=0.140339$를 D1에 주는 것이 이것이고, $\lambda$를 키우면 그 최소점의 곡률이 바뀌는데 과제 4가 그것을 잰다. 정규화라는 우산 전체는 [[02-foundations/ml-practice|9. ML 실무 §2]]에 있다.

### 5. 학습 recipe 읽기

보고된 숫자는 recipe 전체의 출력이고, 아래 항목마다 목록에 오른 이유는 그것 하나만 바꿔도 그 숫자가 바뀌기 때문이다. 데이터 혼합·split, 전처리, 초기화, 목적함수와 계수, optimizer·schedule, batch와 update 수, precision·hardware, checkpoint 선택, seed와 불확실성을 뽑는다. 그다음 ablation에서 무엇이 필수인지 확인한다. 이것이 [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]], [[01-canonical-papers/notes/1-foundations/adam|Adam]]으로 가는 실무 다리다. 그중 세 항목에는 하위 강의가 숫자를 붙인다. 층마다의 초기화는 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §1]], 파라미터마다의 precision은 [[03-deep-learning/foundations/training-at-scale|1.3 §4]], 연산마다의 hardware는 [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산 §3]]이고, 최적화하기 전에 재는 법은 [[03-deep-learning/foundations/gpu-computing|1.4 §7]]이다.

D1이 그중 셋을 보여 준다. **전처리**: 같은 가중치에 $x$ 대신 $2x=(2,4)$를 넣으면, bias가 0인 ReLU 망은 양의 동차이므로 logit이 모두 두 배가 되어 $s=(4,2)$이고, 가중치 하나 바꾸지 않았는데 loss가 $0.313262$에서 $0.126928$로 떨어진다. 학습 때와 test 때 입력의 척도가 다르면 다른 모델인 셈이다. **목적함수의 계수**: 같은 카탈로그 가중치가 $\lambda=0.1$에서는 $0.563262$를 받으므로(§4), $\lambda$ 없이 인용한 loss는 $\lambda$가 붙은 loss와 비교할 수 없다. **optimizer와 update 수**: 똑같이 $200$스텝을 돈 뒤에도 $\eta=0.1$은 아직 $0.143118$에 있고 $\eta=0.5$는 최솟값 $0.140339$에 도달했으므로(§6), "200스텝 학습"은 보폭 없이는 거의 아무 말도 하지 않는다. 데이터, checkpoint 선택, seed는 §3의 질문이고, 나머지 항목에 논문이 쓰는 어휘 — warmup과 cosine schedule, decoupled weight decay, gradient accumulation, 가중치 평균 — 는 [[02-foundations/ml-practice|9. ML 실무 §6]]에 있다.

ablation은 어느 항목이 결과를 떠받치는지 독자가 알아내는 방법이다. 하나를 바꾸고, 나머지와 학습 예산은 고정한 채, 차이를 그 퍼짐과 함께 보고한다([[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §5]]). 위 네 노트에는 저마다 그런 항목이 있다. AlexNet의 recipe에는 $0.5$의 dropout과 강한 augmentation이 들어 있다. ResNet은 모든 convolution 뒤에 batch normalization을 두고 dropout을 쓰지 않는다. Transformer의 post-norm 배치는 learning-rate warmup에 기대고, Xiong 외의 ablation에서 warmup을 빼자 품질 대부분을 잃어 BLEU가 약 $34$ 대신 $8.45$였다(warmup이 왜 그 배치를 지키는지는 [[03-deep-learning/foundations/training-at-scale|1.3 §9]]). 그리고 Adam의 기본값 $\beta_1=0.9$, $\beta_2=0.999$는 recipe가 그대로 쓰더라도 적어야 하는 하이퍼파라미터다.

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
| $3$ | $0.140345$ | $0.9678$ | 1 | 경계 바로 아래, $2/\lambda_{\max}(H)=3.0179$ |
| $5$ | $0.149517$ | $0.9867$ | 1 | 최소점 위에서 진동 |
| $8$ | $0.599431$ | $1.0000$ | 1 | cross-entropy는 $5.9\times10^{-9}$, norm은 큼: 튕기는 중 |
| $10$ | $0.693147$ | $0.5000$ | 3 | 붕괴, $\log 2$는 포기한 loss |
| $12$ | 15스텝에서 발산 | — | — | overflow |
| $20$ | 9스텝에서 발산 | — | — | overflow |

<svg viewBox="0 0 560 358" style="max-width:100%;height:auto" role="img" aria-label="로그 보폭 축(0.01–20)을 함께 쓰는 두 칸. (a) sweep 표의 각 보폭에서 200스텝 뒤 D1의 정규화 loss: 0.5–2는 L* = 0.140339에 정착, 3은 경계 2/λ_max = 3.018에 걸침, 5는 진동, 8은 0.599431로 튕겨 나감, 10은 log 2 = 0.693147로 붕괴, 12와 20은 overflow. (b) 한 스텝이 가장 가파른 방향의 오차에 곱하는 배율 |1 − η λ_max| = |1 − 0.6627 η|: 1.509에서 0, 3에서 0.988, 3.018에서 1을 넘고, 5에서 2.31.">
  <defs><marker id="aSBk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) 200스텝 뒤의 L<tspan dy="3" font-size="10">λ</tspan><tspan dy="-3" dx="3">(표의 각 η에서)</tspan></text>
  <line x1="58" y1="188" x2="540" y2="188" stroke="currentColor" stroke-width="1"/>
  <line x1="58" y1="34" x2="58" y2="188" stroke="currentColor" stroke-width="1"/>
  <line x1="54" y1="188.0" x2="58" y2="188.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="191.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="54" y1="149.5" x2="58" y2="149.5" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="153.0" font-size="10" fill="currentColor" text-anchor="end">0.2</text>
  <line x1="54" y1="111.0" x2="58" y2="111.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="114.5" font-size="10" fill="currentColor" text-anchor="end">0.4</text>
  <line x1="54" y1="72.5" x2="58" y2="72.5" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="76.0" font-size="10" fill="currentColor" text-anchor="end">0.6</text>
  <line x1="54" y1="34.0" x2="58" y2="34.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="37.5" font-size="10" fill="currentColor" text-anchor="end">0.8</text>
  <line x1="58" y1="54.6" x2="540" y2="54.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <line x1="58" y1="79.6" x2="540" y2="79.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="4 3"/>
  <line x1="58" y1="161.0" x2="540" y2="161.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <text x="62" y="50.6" font-size="10.5" fill="currentColor">log 2 = 0.693147: 포기</text>
  <text x="62" y="75.6" font-size="10" fill="currentColor" fill-opacity="0.75">시작 0.563262</text>
  <text x="62" y="157.0" font-size="10.5" fill="currentColor">L* = 0.140339</text>
  <line x1="420.1" y1="112" x2="420.1" y2="322" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 3"/>
  <text x="420.1" y="107" font-size="10.5" fill="currentColor" text-anchor="middle">2/λ<tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H) = 3.018</tspan></text>
  <circle cx="58.0" cy="138.8" r="3.2" fill="currentColor"/>
  <circle cx="204.0" cy="160.4" r="3.2" fill="currentColor"/>
  <circle cx="306.1" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="350.0" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="394.0" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="419.7" cy="161.0" r="3.2" fill="currentColor"/>
  <circle cx="452.1" cy="159.2" r="3.2" fill="currentColor"/>
  <circle cx="481.9" cy="72.6" r="3.2" fill="currentColor"/>
  <circle cx="496.0" cy="54.6" r="3.2" fill="currentColor"/>
  <line x1="507.6" y1="86" x2="507.6" y2="37" stroke="currentColor" stroke-width="1.4" marker-end="url(#aSBk)"/>
  <line x1="540.0" y1="86" x2="540.0" y2="37" stroke="currentColor" stroke-width="1.4" marker-end="url(#aSBk)"/>
  <text x="540" y="29" font-size="10.5" fill="currentColor" text-anchor="end">12와 20: overflow</text>
  <text x="490.0" y="48.6" font-size="10.5" fill="currentColor" text-anchor="end">10: 죽은 유닛 셋</text>
  <text x="474.9" y="76.1" font-size="10.5" fill="currentColor" text-anchor="end">8: CE 5.9·10⁻⁹, 가중치가 튕겨 나감</text>
  <text x="458.1" y="151.2" font-size="10.5" fill="currentColor">5: 진동</text>
  <text x="64.0" y="142.8" font-size="10.5" fill="currentColor">0.01: 0.256, 아직 내려가는 중</text>
  <text x="204.0" y="175.4" font-size="10.5" fill="currentColor" text-anchor="middle">0.1: 0.143</text>
  <text x="350.0" y="176.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.5–2는 L*에 정착</text>
  <line x1="306.1" y1="180.0" x2="394.0" y2="180.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="58.0" y1="188" x2="58.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <line x1="204.0" y1="188" x2="204.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <line x1="350.0" y1="188" x2="350.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <line x1="496.0" y1="188" x2="496.0" y2="192" stroke="currentColor" stroke-width="1"/>
  <text x="12" y="224" font-size="11.5" fill="currentColor">(b) 가장 가파른 방향의 스텝당 배율 |1 − η λ<tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H)|, λ</tspan><tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H) = 0.6627</tspan></text>
  <line x1="58" y1="322" x2="540" y2="322" stroke="currentColor" stroke-width="1"/>
  <line x1="58" y1="236" x2="58" y2="322" stroke="currentColor" stroke-width="1"/>
  <line x1="54" y1="322.0" x2="58" y2="322.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="325.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="54" y1="293.3" x2="58" y2="293.3" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="296.8" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <line x1="54" y1="264.7" x2="58" y2="264.7" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="268.2" font-size="10" fill="currentColor" text-anchor="end">2</text>
  <line x1="54" y1="236.0" x2="58" y2="236.0" stroke="currentColor" stroke-width="1"/>
  <text x="51" y="239.5" font-size="10" fill="currentColor" text-anchor="end">3</text>
  <line x1="58" y1="293.3" x2="540" y2="293.3" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <polyline points="58.0,293.5 59.2,293.5 60.4,293.5 61.6,293.5 62.8,293.5 64.0,293.5 65.2,293.5 66.4,293.6 67.6,293.6 68.8,293.6 70.0,293.6 71.3,293.6 72.5,293.6 73.7,293.6 74.9,293.6 76.1,293.6 77.3,293.6 78.5,293.6 79.7,293.6 80.9,293.6 82.1,293.6 83.3,293.6 84.5,293.6 85.7,293.6 86.9,293.6 88.1,293.6 89.3,293.6 90.5,293.7 91.7,293.7 92.9,293.7 94.1,293.7 95.4,293.7 96.6,293.7 97.8,293.7 99.0,293.7 100.2,293.7 101.4,293.7 102.6,293.7 103.8,293.7 105.0,293.7 106.2,293.7 107.4,293.7 108.6,293.8 109.8,293.8 111.0,293.8 112.2,293.8 113.4,293.8 114.6,293.8 115.8,293.8 117.0,293.8 118.2,293.8 119.5,293.8 120.7,293.8 121.9,293.9 123.1,293.9 124.3,293.9 125.5,293.9 126.7,293.9 127.9,293.9 129.1,293.9 130.3,293.9 131.5,293.9 132.7,294.0 133.9,294.0 135.1,294.0 136.3,294.0 137.5,294.0 138.7,294.0 139.9,294.0 141.1,294.0 142.3,294.1 143.6,294.1 144.8,294.1 146.0,294.1 147.2,294.1 148.4,294.1 149.6,294.1 150.8,294.2 152.0,294.2 153.2,294.2 154.4,294.2 155.6,294.2 156.8,294.2 158.0,294.3 159.2,294.3 160.4,294.3 161.6,294.3 162.8,294.3 164.0,294.3 165.2,294.4 166.5,294.4 167.7,294.4 168.9,294.4 170.1,294.4 171.3,294.5 172.5,294.5 173.7,294.5 174.9,294.5 176.1,294.6 177.3,294.6 178.5,294.6 179.7,294.6 180.9,294.7 182.1,294.7 183.3,294.7 184.5,294.7 185.7,294.8 186.9,294.8 188.1,294.8 189.3,294.8 190.5,294.9 191.8,294.9 193.0,294.9 194.2,295.0 195.4,295.0 196.6,295.0 197.8,295.1 199.0,295.1 200.2,295.1 201.4,295.2 202.6,295.2 203.8,295.2 205.0,295.3 206.2,295.3 207.4,295.3 208.6,295.4 209.8,295.4 211.0,295.5 212.2,295.5 213.4,295.5 214.7,295.6 215.9,295.6 217.1,295.7 218.3,295.7 219.5,295.8 220.7,295.8 221.9,295.9 223.1,295.9 224.3,295.9 225.5,296.0 226.7,296.1 227.9,296.1 229.1,296.2 230.3,296.2 231.5,296.3 232.7,296.3 233.9,296.4 235.1,296.4 236.3,296.5 237.5,296.6 238.8,296.6 240.0,296.7 241.2,296.7 242.4,296.8 243.6,296.9 244.8,296.9 246.0,297.0 247.2,297.1 248.4,297.2 249.6,297.2 250.8,297.3 252.0,297.4 253.2,297.5 254.4,297.5 255.6,297.6 256.8,297.7 258.0,297.8 259.2,297.9 260.4,298.0 261.6,298.0 262.9,298.1 264.1,298.2 265.3,298.3 266.5,298.4 267.7,298.5 268.9,298.6 270.1,298.7 271.3,298.8 272.5,298.9 273.7,299.0 274.9,299.1 276.1,299.3 277.3,299.4 278.5,299.5 279.7,299.6 280.9,299.7 282.1,299.8 283.3,300.0 284.5,300.1 285.7,300.2 286.9,300.4 288.2,300.5 289.4,300.6 290.6,300.8 291.8,300.9 293.0,301.1 294.2,301.2 295.4,301.4 296.6,301.5 297.8,301.7 299.0,301.8 300.2,302.0 301.4,302.2 302.6,302.3 303.8,302.5 305.0,302.7 306.2,302.9 307.4,303.0 308.6,303.2 309.8,303.4 311.1,303.6 312.3,303.8 313.5,304.0 314.7,304.2 315.9,304.4 317.1,304.6 318.3,304.8 319.5,305.1 320.7,305.3 321.9,305.5 323.1,305.8 324.3,306.0 325.5,306.2 326.7,306.5 327.9,306.7 329.1,307.0 330.3,307.3 331.5,307.5 332.7,307.8 333.9,308.1 335.1,308.4 336.4,308.6 337.6,308.9 338.8,309.2 340.0,309.5 341.2,309.9 342.4,310.2 343.6,310.5 344.8,310.8 346.0,311.2 347.2,311.5 348.4,311.9 349.6,312.2 350.8,312.6 352.0,312.9 353.2,313.3 354.4,313.7 355.6,314.1 356.8,314.5 358.0,314.9 359.2,315.3 360.5,315.7 361.7,316.2 362.9,316.6 364.1,317.0 365.3,317.5 366.5,318.0 367.7,318.4 368.9,318.9 370.1,319.4 371.3,319.9 372.5,320.4 373.7,320.9 374.9,321.5 376.1,322.0 377.3,321.5 378.5,320.9 379.7,320.3 380.9,319.7 382.1,319.1 383.4,318.5 384.6,317.9 385.8,317.3 387.0,316.7 388.2,316.0 389.4,315.3 390.6,314.7 391.8,314.0 393.0,313.3 394.2,312.5 395.4,311.8 396.6,311.1 397.8,310.3 399.0,309.5 400.2,308.7 401.4,307.9 402.6,307.1 403.8,306.3 405.0,305.4 406.2,304.6 407.4,303.7 408.7,302.8 409.9,301.9 411.1,300.9 412.3,300.0 413.5,299.0 414.7,298.0 415.9,297.0 417.1,296.0 418.3,294.9 419.5,293.9 420.7,292.8 421.9,291.7 423.1,290.5 424.3,289.4 425.5,288.2 426.7,287.0 427.9,285.8 429.1,284.5 430.3,283.3 431.6,282.0 432.8,280.6 434.0,279.3 435.2,277.9 436.4,276.5 437.6,275.1 438.8,273.7 440.0,272.2 441.2,270.7 442.4,269.1 443.6,267.6 444.8,266.0 446.0,264.4 447.2,262.7 448.4,261.0 449.6,259.3 450.8,257.5 452.0,255.8 453.2,253.9 454.4,252.1 455.6,250.2 456.9,248.3 458.1,246.3 459.3,244.3 460.5,242.3 461.7,240.2 462.9,238.1 464.1,236.0" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="464.0" y1="246" x2="474.0" y2="236" stroke="currentColor" stroke-width="1.2" marker-end="url(#aSBk)"/>
  <text x="478.0" y="246" font-size="10.5" fill="currentColor">3을 넘음</text>
  <circle cx="376.1" cy="322.0" r="2.8" fill="currentColor"/>
  <text x="300" y="318" font-size="10.5" fill="currentColor" text-anchor="end">가장 빠름: 1/λ<tspan dy="3" font-size="10">max</tspan><tspan dy="-3">(H) = 1.509</tspan></text>
  <line x1="303" y1="315" x2="371.1" y2="320" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <circle cx="419.7" cy="293.7" r="2.8" fill="currentColor"/>
  <text x="413.7" y="287.3" font-size="10.5" fill="currentColor" text-anchor="end">η = 3에서 0.988</text>
  <circle cx="452.1" cy="255.7" r="2.8" fill="currentColor"/>
  <text x="466.1" y="259.7" font-size="10.5" fill="currentColor">η = 5에서 2.31</text>
  <text x="62" y="287.3" font-size="10" fill="currentColor" fill-opacity="0.8">배율 1: 아래면 오차가 줄고, 위면 커진다</text>
  <line x1="58.0" y1="322" x2="58.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="58.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">0.01</text>
  <line x1="204.0" y1="322" x2="204.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="204.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">0.1</text>
  <line x1="350.0" y1="322" x2="350.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="350.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="496.0" y1="322" x2="496.0" y2="326" stroke="currentColor" stroke-width="1"/>
  <text x="496.0" y="337" font-size="10" fill="currentColor" text-anchor="middle">10</text>
  <line x1="306.1" y1="322" x2="306.1" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="394.0" y1="322" x2="394.0" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="419.7" y1="322" x2="419.7" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="452.1" y1="322" x2="452.1" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="481.9" y1="322" x2="481.9" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="507.6" y1="322" x2="507.6" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <line x1="540.0" y1="322" x2="540.0" y2="324.5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.7"/>
  <text x="299" y="353" font-size="11" fill="currentColor" text-anchor="middle">보폭 η (로그 눈금)</text>
</svg>

표의 sweep을 로그 보폭 축에 그린 것이다. (a) 200스텝 뒤 $\eta=0.5$부터 $2$까지는 모두 $L^\ast=0.140339$에 있고, 경계 $2/\lambda_{\max}(H)=3.018$ 바로 아래의 $\eta=3$은 거의 도착했다. $\eta=5$는 $0.149517$에서 진동하고, $\eta=8$은 $0.599431$로 튕겨 나가며, $\eta=10$은 $\log2=0.693147$로 붕괴하고, $12$와 $20$은 overflow한다. (b) 최소점 근처에서 한 스텝은 가장 가파른 방향의 오차에 $\lvert1-\eta\lambda_{\max}(H)\rvert$를 곱한다. $\lambda_{\max}(H)=0.6627$이므로 이 배율은 $\eta=1.509$에서 $0$, $\eta=3$에서 $0.988$이고, $3.018$을 넘으면 $1$보다 커져 오차가 자란다.

**Sweep 읽기.** 손 유도가 알려줄 수 없었던 것 넷.

- **쓸모 있는 경계는 정착 경계이고, 그것이 정확히 $2/\lambda_{\max}(H)$다.** $0.5$부터 $2$까지의 행이 $L^\ast=0.140339$에 여섯 자리까지 내려앉고, $3$의 행은 $0.140345$로 다섯째 자리에서 어긋난다. $\eta=3$에서 그림의 배율이 $0.988$이라 한 스텝이 가장 가파른 방향에 남은 오차의 약 $1\%$만 없애고, 200스텝으로는 모자라기 때문이다. 코드 3부는 $\theta^\ast$까지 내려가 유한차분으로 $12\times12$ Hessian을 만들고 $\lambda_{\max}(H)=0.6627$, 즉 $2/\lambda_{\max}(H)=3.0179$를 보고한다. 같은 반복문을 이분법으로 훑어 여전히 정착하는 최대 $\eta$를 찾으면 — 과제 4 템플릿의 마지막 줄들이 이 일을 한다 — $3.0180$이다. 교과서의 조건이 여기서는 근사가 아니라 측정값이고, 유효숫자 네 자리까지 맞는다.
- **경계 위에서는 실패가 시끄러워지기 전에 조용하다.** $\eta=8$에서 cross-entropy는 $5.9\times10^{-9}$이다. 모델은 자기 학습점 하나에 대해 *완벽하다*. 그런데 $L_\lambda=0.599431$로 최소점의 네 배인데, 가중치가 원점에서 멀리 던져졌기 때문이다. accuracy만 보는 run은 아무 이상도 보지 못한다. $\eta=10$에서는 은닉 유닛 셋이 모두 죽고 $p=(0.5,0.5)$, loss는 정확히 $\log 2=0.693147$이다. 모든 가중치가 0으로 감쇠했고 신경망은 사전 확률을 예측한다. 이 숫자는 눈에 익혀 둘 가치가 있다. $0.693$에 멈춘 2클래스 run은 수렴한 것이 아니라 포기한 것이다.
- **유닛 하나가 죽는 것은 의도이고 버그가 아니다.** $\eta=0.1$부터 $\eta=8$까지의 모든 행이 죽은 유닛 하나로 끝나고, 최소점 자체가 그렇다. $\theta^\ast$에서 $W_1$의 첫 행과 $W_2$의 첫 열이 0이다. 역전파가 은닉 유닛 1을 내리려 했고($\partial L/\partial z_1=+0.268941$) decay가 마무리했다. weight decay는 가지치기를 한다. 죽은 유닛 셋은 붕괴이고, 하나는 목적함수가 시킨 대로 한 것이다.
- **Overflow 경계는 경계가 아니다.** 정착 경계처럼 발산 임계값을 보고하고 싶어진다. 코드 3부는 $\eta$를 $10.40$에서 $10.6095$까지 $0.0005$ 간격으로 훑는다. 첫 발산은 $\eta=10.4015$이고, 그 이상의 격자점 417개 중 285개가 여전히 200스텝을 살아남는다. 안정성 한계를 넘으면 반복이 ReLU의 꺾인 점들 위를 튕기고, 탈출 여부가 $\eta$에 대해 단조롭지 않다. 이런 그림에서 "$\eta=10.4$ 위에서 학습이 발산한다"고 적은 논문은 격자 하나를 인용하고 있는 것이다.

### 스스로 점검 · Self-check

1. $W_2$, $h$, $\eta$, $\lambda$, ReLU mask 중 무엇이 파라미터이고 activation이고 하이퍼파라미터인가.
2. 구현은 왜 softmax와 cross-entropy를 한 블록으로 융합하는가.
3. D1의 $\partial L/\partial h$는 세 번째 성분이 0이다. 대상의 어느 숫자가 그렇게 만들었고, 예측이 좋아지면 달라지는가.
4. 2클래스 학습이 loss $0.693$에서 평평해졌다. 가장 그럴듯한 진단 하나와 확인 방법은?
5. 분리 가능한 샘플 하나에 대한 순수 cross-entropy에서 learning rate sweep이 안정성에 대해 아무것도 가르치지 못하는 이유는?

> [!tip]- 정답 · Answers
> 1. 파라미터는 $W_2$(그리고 $W_1$)다. activation은 $h$이고, ReLU mask도 activation이다. 샘플에서 계산되어 역전파를 위해 보관되지만, 아무도 학습하지 않고 아무도 고르지 않는다(§1의 비예). 하이퍼파라미터는 $\eta$와 $\lambda$다.
> 2. 따로 두면 Jacobian이 $p_i(\delta_{ij}-p_j)$와 $-y_i/p_i$로 지저분한데 곱하면 $p-y$로 약분된다. 융합하면 underflow된 확률에 $\log$를 거는 일도 피한다.
> 3. $W_2$의 세 번째 열 $(0,0)$이다. 유닛 3이 앞으로 아무것도 내보내지 않으니 오차가 닿지 않고, 예측이 좋아지든 나빠지든 달라지지 않는다. 이 가중치에서 그 0은 배선의 성질이지 오차의 성질이 아니다. 다만 영구적이지는 않다. 그 열 자체는 gradient $(-0.268941,\ 0.268941)$을 받으므로 $\eta=0.1$의 한 스텝이 그 열을 $(0.026894,\ -0.026894)$로 만들고, 그 성분은 더 이상 0이 아니다.
> 4. 모델이 클래스 사전 확률을 예측하고 아무것도 배우지 않는 상태다. $\log 2=0.693147$이 $p=(0.5,0.5)$의 loss다. logit을 찍어 확인한다. 가중치가 작으면서 $s_1\approx s_2$이면 보폭이 신경망을 붕괴시킨 것이고($\eta=10$의 행), 가중치가 큰데도 $s$가 평평하면 배선이 끊긴 것이다.
> 5. 그 목적함수에는 최소점이 없다. logit이 무한으로 갈 수 있어서 표의 모든 $\eta$에서 loss가 단조 감소한다. 넘어설 최소점이 없으므로 sweep 안의 어떤 것도 불안정할 수 없다. 바닥을 주는 것이 weight decay다(§4).

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[03-deep-learning/lab-objects|0. Lab Objects]]만 쓴다. 대상은 계속 D1이고, 문제 1은 입력을, 2는 logit을, 3은 선택 절차를, 4는 정답 클래스와 decay를 바꾸므로 페이지의 숫자를 그대로 옮길 수 없다.

1. **그리기.** 새 입력 $x=(2,-1)$, 같은 가중치, 정답 1번 클래스로 그림을 그린다. 모든 텐서에 shape와 값을 달고, 순전파는 한쪽을 따라 내려가고 역전파는 다른 쪽을 따라 $\partial L/\partial z$까지 올라가게 한다. 역방향 화살표 가운데 ReLU mask가 막는 것과 $W_2$의 0인 열이 막는 것을 표시하고, $\eta=0.1$에서 SGD 한 스텝을 밟은 뒤에도 남는 막힘이 어느 쪽인지 말한다.
2. **유도.** logit $(0,\log3)$, 정답 1번의 확률·loss·$p-y$를 구한다.
3. **해석.** 한 팀이 augmentation 설정 열 가지를 시험해 각각을 test 집합에서 한 번씩 채점하고 가장 좋은 것을 보고한다. 열 가지 가운데 어느 것도 실제로는 더 낫지 않고, test 점수는 run마다 $\sigma=0.4$포인트로 흔들린다고 하자. (a) 어떤 경계를 넘었고, 설정은 어느 분할이 골랐어야 하는가. (b) 보고된 숫자는 방법의 실제 수준보다 대략 얼마나 위에 있는가. (c) 고른 설정을 새 seed로 다시 돌렸더니 이득 대부분이 사라졌다. 방법이 고장 난 것인가.
4. **실행.** 영어 절 템플릿의 `?`를 채운 뒤, 정답을 **2번 클래스**로 바꾸고($y=(0,1)$, 즉 카탈로그 모델이 *틀린* 상태에서 출발한다) decay를 $\lambda=0.2$로 올려 다시 돌린다. (a) 시작 $L_\lambda$, (b) $\eta\in\{0.05,0.5,2,5,20\}$, 200스텝의 $L_\lambda$·죽은 유닛·발산 스텝 표, (c) 이분법으로 찾은, 여전히 최소점에 정착하는 최대 $\eta$를 보고한다. 그다음 정답은 2번 클래스로 둔 채 $\lambda$만 $0.1$로 되돌려 (b)의 $\eta=0.5$ 행과 이분법을 한 번 더 돌리고, 두 변경 가운데 어느 쪽이 §6 대비 경계를 옮겼는지와 그 이유를 말한다.

> [!note]- 그리는 법 · How to draw it
> - 순방향과 역방향을 한 장에 함께 그린다. 순전파는 한쪽을 따라 내려가고 역전파는 다른 쪽을 따라 올라간다.
> - 모든 텐서에 배치 차원까지 포함한 shape를 적는다. 이름 없는 화살표가 shape 오류가 숨는 자리이고, shape 오류는 재구현이 조용히 다른 모델을 학습시키는 가장 흔한 이유다.
> - ReLU는 $h$가 아니라 $z$에 걸린 게이트로 그린다. mask $\mathbf 1[z>0]$은 활성화 이전 값에서 읽고, 이 샘플에 대해 gradient가 흐르기 전에 이미 고정된다. $h$ 뒤에 그리면 역전파가 mask를 고를 수 있다는 주장이 되는데 그렇지 않다.
> - softmax와 cross-entropy는 한 블록으로 그린다. 따로 두면 각각의 Jacobian이 지저분하지만 합치면 $p-y$만 남고(§2), 그 식이 나타나는 자리는 이 블록의 출력 화살표뿐이다.
> - $L$에서 $W_1$으로 곧장 가는 화살표는 그리지 않는다. gradient는 $W_2$를 지나고 mask를 지나야만 $W_1$에 닿는다. 그 경로가 역전파의 전부이고, 지름길이 있는 그림은 다른 알고리즘의 그림이다.
> - bias를 그리고 *0에 고정*이라고 적는다. 구조의 자리 17개 가운데 5개이지만 이 페이지는 한 번도 학습시키지 않으므로 스텝이 갱신하는 숫자는 12개다. [[02-foundations/neural-network-basics|0.8 §2]]가 P1을 자리 13개 가운데 9개로 세는 것과 같은 관례다.
> - $\partial L/\partial z$의 0마다 원인을 적는다. mask에서 온 0은 샘플이 유닛을 끈 것이고, $W_2$의 0인 열에서 온 0은 가중치가 아직 아무것도 되돌려 보내지 않는 것이다. 두 원인은 스텝 뒤에 다르게 움직이므로, 둘을 구별하지 않은 그림으로는 그리기 문제에 답할 수 없다.

> [!tip]- 정답 · Solutions
> 1. 순전파: $z=W_1x=(2,-1,2)$이므로 mask는 $(1,0,1)$, $h=(2,0,2)$다. $s=W_2h=(0,2)$, $p=(0.119203,\ 0.880797)$이고 $L=-\log0.119203=2.126928$ nat, 확신에 찬 오답이다. 역전파: $p-y=(-0.880797,\ 0.880797)$, $\partial L/\partial h=W_2^\top(p-y)=(0.880797,\ -0.880797,\ 0)$, $\partial L/\partial z=(0.880797,\ 0,\ 0)$. 유닛 3의 0은 페이지에서처럼 $W_2$의 0인 세 번째 열 때문이고, 유닛 2의 0은 $z_2=-1$이라 mask 때문이다. 한 스텝 뒤 둘은 갈린다. 유닛 3의 열은 자기 gradient $(p-y)\,h_3=(-1.761594,\ 1.761594)$을 가지므로 $(0.176159,\ -0.176159)$가 되고, 유닛 3으로 돌아가는 길이 열린다. 새 가중치에서 $\partial L/\partial h_3=-0.202859$다. 유닛 2는 어느 층에서도 gradient를 받지 못한다. $h_2=0$이 $\partial L/\partial W_2$의 그 열을, mask가 $\partial L/\partial W_1$의 그 행을 0으로 만들기 때문이다. 그래서 $z_2$는 $-1$에 머물고, 이 입력에서는 mask가 계속 막는다. 카탈로그 입력 $x=(1,2)$에서는 같은 유닛이 켜져 있다. 0인 열은 가중치에 관한 사실이라 한 스텝만 가고, mask는 샘플에 관한 사실이다.
> 2. $p=(1/4,3/4)$, $L=1.386$, $p-y=(-3/4,3/4)$.
> 3. (a) test 집합이 모델 선택에 들어가, 보고된 test 결과는 더 이상 손대지 않은 추정이 아니다. 설정은 validation 분할이 골랐어야 하고, test 집합은 고른 것 하나만 한 번 채점했어야 한다. (b) 똑같이 좋은 run 열 개 가운데 최고는 평균적으로 그 평균보다 $1.539\sigma$ 위에 놓이므로(§3), 보고된 숫자의 $1.539\times0.4=0.62$포인트는 선택의 몫이다. (c) 아니다. 그만한 하락은 열 개 중 최고를 고른 일이 예측하는 것이고, 다시 돌린 값이 정직한 추정이다.
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
>    (c) 이분법은 $1.9801$을 주고 $L^\ast=0.235806$이다. 2번 클래스를 $\lambda=0.1$에서 돌리면 $\eta=0.5$ 행은 $0.140339$, 이분법은 $3.0180$으로 §6의 숫자 그대로이므로, 정답을 뒤집은 것은 아무것도 옮기지 않았다. $W_2$의 두 행을 맞바꾸면 $\lVert\theta\rVert^2$는 그대로인 채 2번 클래스의 목적함수가 1번 클래스의 목적함수가 되므로, 둘은 최솟값과 그 자리의 곡률을 공유하고, 뒤집기가 바꾸는 것은 틀린 채 출발하는 경로뿐이다. 경계를 $3.0180$에서 **내린** 것은 decay다. 새 최소점에서 $\lambda_{\max}(H)$가 $0.6627$이 아니라 $1.0100$이기 때문이다. 그 증가분 가운데 $0.1$은 decay 항 자체가 더한다. 그 Hessian이 $\lambda I$라 모든 고유값을 $\lambda$만큼 올리기 때문이다. 나머지 $0.247$은 cross-entropy 자신의 곡률이다. decay가 무거울수록 예측이 덜 확신하게 남아 정답 확률이 $0.968$ 대신 $0.937$이 되고, 그 자리에서 softmax가 더 많이 휘기 때문이다. 정규화를 세게 거는 것은 학습을 공짜로 안정시키는 방법이 아니다. loss의 바닥을 사고 보폭 천장을 좁혀 지불한다. $\eta=5$의 행은 §6의 $\eta=10$ 행과 같은 $\log 2$ 붕괴가 절반의 보폭에서 온 것이다.

### 출처 · Sources

- A. Krizhevsky, I. Sutskever & G. E. Hinton, "ImageNet classification with deep convolutional neural networks," *NeurIPS* 2012 — §5의 0.5 dropout과 augmentation([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet 노트]]).
- K. He, X. Zhang, S. Ren & J. Sun, "Deep residual learning for image recognition," *CVPR* 2016 — 모든 convolution 뒤의 batch normalization, dropout 없음([[01-canonical-papers/notes/1-foundations/resnet|ResNet 노트]]).
- A. Vaswani et al., "Attention is all you need," *NeurIPS* 2017 — post-norm 배치와 그 warmup([[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]).
- R. Xiong et al., "On layer normalization in the Transformer architecture," *ICML* 2020 — warmup ablation, BLEU 약 34 대 8.45. Transformer 노트가 전하는 수치다.
- D. P. Kingma & J. Ba, "Adam: A method for stochastic optimization," *ICLR* 2015 — 기본값 β₁ = 0.9, β₂ = 0.999([[01-canonical-papers/notes/1-foundations/adam|Adam 노트]]).
- I. Loshchilov & F. Hutter, "Decoupled weight decay regularization," *ICLR* 2019 — §4 비예의 decoupled weight decay. [[02-foundations/optimization|4. 최적화]]에서 계산한다.
- E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association* 22(158):209–212 (1927) — §3에서 인용한 구간.
- D1은 [[03-deep-learning/lab-objects|0. Lab Objects]]의 교육용 대상이다. 이 페이지의 모든 숫자는 손으로 또는 §6의 코드로 여기서 계산했다.
