---
title: 5. Information Theory
tags: [foundations]
study-depth: Literacy
depth-goal: "Read the notation and recurring ideas accurately; return for deeper derivations when a paper requires them."
mastery-when: "Raise to Working or Mastery when the thesis objective depends directly on these formulations."
---

> [!note] Prerequisites · 선수 지식
> Plant **P5** (its crack detector) from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled or measured) · [[02-foundations/engineering-math|0.5 §6]] (log rules — §0 below re-states them) · [[02-foundations/probability|3. Probability §1–2]] (distributions, expectation) · [[02-foundations/optimization|4. Optimization §2]] (convexity, for Jensen's inequality in §3)
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치(plant: 제어하거나 측정하는 대상 시스템) **P5**(균열 감지기) · [[02-foundations/engineering-math|0.5 §6]](로그 규칙 — 아래 §0이 다시 정리한다) · [[02-foundations/probability|3. 확률 §1–2]](분포·기댓값) · [[02-foundations/optimization|4. 최적화 §2]](볼록성, §3의 옌센 부등식용)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/probability|3. Probability]] and the logs from [[02-foundations/engineering-math|0.5]]. Second applied pillar: it names what those objectives all measure,
which is that cross-entropy is maximum likelihood is KL.*

Everything in deep learning that involves a probability distribution eventually speaks
information theory: cross-entropy loss, KL divergence, the ELBO (evidence lower bound, derived in §5), contrastive learning,
even "perplexity." This page is the complete working set for reading modern papers —
no prior background assumed. Its running object is the crack detector of plant P5 ([[02-foundations/lab-plants|0.6 Lab Plants]]): it fires on 95% of cracks and on 5% of sound panels, where 1% of panels are cracked.

> [!note] Why this matters · 왜 배우는가
> Information theory is the mathematical floor under the learning-and-adaptation layer of the physical-AI stack in [[07-research-program/index|7. Research Program §5]] and under its language-driven form, which turns *"Install that panel on the frame"* into action; it serves the first step, resolving the instruction, where cross-entropy (§2) is the loss of every language model and of every policy that emits its actions as tokens, and InfoNCE (§4) is how a vision–language model learns which words go with which image of the panel (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it a failure is unreadable: operators pass a scaffold tie $60$ mm to its left or to its right, and one Gaussian fitted to their commands by maximum likelihood — the forward KL of §3 — puts its mean between the two routes, into the tie ([[05-construction-robotics/imitating-contact|10. Imitating Contact §4]]); a KL penalty, or "the loss fell to 0.7 nats", means nothing without §2–§3. On the dissertation path of [[07-research-program/index|7. Research Program §8]] this page is block 4's working language — [[03-deep-learning/foundations/index|1. Learning Systems §1]] trains on §2's loss, [[03-deep-learning/vlm/index|3. VLM §2]] on §4's bound, and [[03-deep-learning/vla/index|4. VLA §2]] trains tokenized actions with §2 and names the multimodality §3 explains — and block 7's 10. Imitating Contact §4 turns §3 into two demonstrators and one mean. After it you can compute entropy, cross-entropy and KL by hand in bits or nats, and say which KL direction a loss minimizes and what that does to the fitted policy.

> [!note] First pass · 처음이라면
> Two sessions of 60–90 minutes, with a calculator. **Session 1, entropy and cross-entropy:** the picture, §0 (three log rules, five minutes), §1 and §2, doing every bit calculation by hand — they are the page; end with self-check 1–2. **Session 2, KL:** §3 through the forward and reverse fits of the two-bump mixture and their figure, then the problem set. Second pass: §4 when a paper puts mutual information or a contrastive loss in its objective (its InfoNCE proof last) and §5 when it puts an ELBO there, with self-check 3–4; the collapsed notes on codes can wait, and §6 is a reference table to come back to.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 324" style="max-width:100%;height:auto" role="img" aria-label="The P5 crack detector as a binary channel: prior boxes to scale, a line for cracked at 0.01 and a tall box for sound at 0.99; four arrows with their conditionals and joint masses; the alarm node split into 0.161 from cracked and 0.839 from sound inside a bracket labelled P(+) = 0.059; 0.95 and 0.161 circled.">
  <defs><marker id="itHw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="104" y="46" width="36" height="2" fill="currentColor" fill-opacity="0.85"/>
  <rect x="104" y="62" width="36" height="198" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.3"/>
  <text x="96" y="44" font-size="11" text-anchor="end" fill="currentColor">c  cracked</text>
  <text x="96" y="58" font-size="11" text-anchor="end" fill="currentColor">P(c) = 0.01</text>
  <text x="96" y="157" font-size="11" text-anchor="end" fill="currentColor">¬c  sound</text>
  <text x="96" y="171" font-size="11" text-anchor="end" fill="currentColor">P(¬c) = 0.99</text>
  <text x="96" y="191" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">to scale: 99 : 1</text>
  <rect x="376" y="72" width="24" height="10.3" fill="currentColor" fill-opacity="0.55"/>
  <rect x="376" y="82.3" width="24" height="53.7" fill="currentColor" fill-opacity="0.12"/>
  <rect x="376" y="196" width="24" height="64" fill="currentColor" fill-opacity="0.07"/>
  <rect x="376" y="72" width="24" height="64" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="376" y="196" width="24" height="64" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="400" y="50" font-size="11" text-anchor="end" fill="currentColor">+  alarm</text>
  <text x="400" y="276" font-size="11" text-anchor="end" fill="currentColor">−  silent</text>
  <line x1="140" y1="47" x2="375" y2="77.2" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHw)"/>
  <line x1="140" y1="116" x2="375" y2="109.2" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHw)"/>
  <line x1="140" y1="47" x2="375" y2="208" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHw)"/>
  <line x1="140" y1="220" x2="375" y2="242" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHw)"/>
  <circle cx="257.5" cy="42.1" r="15.8" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="257.5" y="46.1" font-size="11" text-anchor="middle" fill="currentColor">0.95</text>
  <text x="304.5" y="103.2" font-size="11" text-anchor="middle" fill="currentColor">0.05</text>
  <text x="300.9" y="148" font-size="11" fill="currentColor">0.05</text>
  <text x="257.5" y="247" font-size="11" text-anchor="middle" fill="currentColor">0.95</text>
  <text x="346" y="63.5" font-size="11" text-anchor="end" fill="currentColor">0.0095</text>
  <text x="364" y="126.2" font-size="11" text-anchor="end" fill="currentColor">0.0495</text>
  <text x="350" y="214" font-size="11" text-anchor="end" fill="currentColor">0.0005</text>
  <text x="364" y="259" font-size="11" text-anchor="end" fill="currentColor">0.9405</text>
  <circle cx="426" cy="77.2" r="18.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="426" y="81.2" font-size="11" text-anchor="middle" fill="currentColor">0.161</text>
  <text x="408" y="113.2" font-size="11" fill="currentColor">0.839</text>
  <path d="M 458 72 q 6 0 6 6 V 98 q 0 6 6 6 q -6 0 -6 6 V 130 q 0 6 -6 6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="475" y="108" font-size="11" fill="currentColor">P(+) = 0.059</text>
  <text x="424" y="162" font-size="11" opacity="0.9" fill="currentColor">joint masses:</text>
  <text x="424" y="176" font-size="11" opacity="0.9" fill="currentColor">0.0095 + 0.0005</text>
  <text x="424" y="190" font-size="11" opacity="0.9" fill="currentColor">+ 0.0495 + 0.9405</text>
  <text x="424" y="204" font-size="11" opacity="0.9" fill="currentColor">= 1 ✓</text>
  <text x="12" y="299" font-size="11" opacity="0.9" fill="currentColor">The arrows leaving each left node sum to 1 (0.95 + 0.05); those entering + need not.</text>
  <text x="12" y="313" font-size="11" opacity="0.9" fill="currentColor">Circled: P(+|c) = 0.95 on the arrow, P(c|+) = 0.161 in the bracket, about six times apart.</text>
</svg>

The **P5** crack detector from [[02-foundations/lab-plants|0.6 Lab Plants]] as a binary channel, with the prior drawn to scale — cracked, $P(c)=0.01$, is a line and sound, $P(\neg c)=0.99$, fills the column — and four arrows carrying $P(+|c)=0.95$, $P(-|c)=0.05$, $P(+|\neg c)=0.05$ and $P(-|\neg c)=0.95$. At the arrowheads sit the joint masses $0.0095$, $0.0005$, $0.0495$ and $0.9405$, which sum to $1$; the two that land on $+$ make $P(+)=0.059$, split into the shares $0.161$ from cracked and $0.839$ from sound. The two circled numbers are the point — the sensitivity $P(+|c)=0.95$ on an arrow and the posterior $P(c|+)=0.161$ in the bracket, about six times apart — and §2 prices confusing them at $H(p,q)\approx 3.64$ bits (the cross-entropy, §2) against a floor of $H(p)\approx 0.637$ bits (the entropy of the true posterior, §1).

### 0. Prerequisite: the three log rules

Everything on this page runs on logarithms. If these three lines are not second nature,
read [[02-foundations/engineering-math|0.5 Engineering Math §6]] first (5 minutes):
$\log(ab) = \log a + \log b$ (products of probabilities become sums — why losses are sums);
$\log(a^n) = n \log a$; and base 2 vs base $e$ only changes units (**bits** vs **nats**) by
a constant factor. The factor comes from the change-of-base rule $\log_2 x = \ln x / \ln 2$, so any quantity on this page converts as
$$H_{\text{bits}} = \frac{H_{\text{nats}}}{\ln 2}, \qquad 1\ \text{nat} = 1.443\ \text{bits}$$
because every term is a log and every log rescales by the same $1/\ln 2$. Papers in machine learning usually report nats (PyTorch's losses use $\ln$); coding and communication papers use bits. Also remember: probabilities live in $[0,1]$, so log-probabilities are
$\le 0$ — a "smaller cross-entropy" means log-probs closer to zero.

**The three rules on P5.** A sound panel stays silent with probability $P(-|\neg c)=0.95$ ([[02-foundations/lab-plants|0.6 Lab Plants]]). An inspection run over $N$ sound panels, each read independently, stays silent with probability $0.95^N$, and rules 1 and 2 turn that product into $N\ln 0.95$: for $N=100$, $0.95^{100}=0.0059$ and $100\ln 0.95=-5.13$ nats. Rule 3 converts it, $-5.13\times1.443=-7.40$ bits, and the same rule prices the surprise of learning that a panel is cracked, at the prior $P(c)=0.01$, as $-\ln 0.01=4.61$ nats or $6.64$ bits: one fact in two units. The sum is not a convenience. Multiplied out, $0.95^N$ falls below the smallest number float32 stores at full precision (about $10^{-38}$) at $N\approx1{,}700$, and below float64's (about $10^{-308}$) at $N\approx13{,}800$ (what a float can hold is [[02-foundations/tools/python-research-code|12.3 Python §5]]). Past that point the product keeps fewer and fewer correct digits, and a few hundred readings later it is gone: computed as a power it rounds to exactly $0$ at $N\approx14{,}500$, whose log is $-\infty$, and computed as a running product it stalls at one tiny value however many more readings arrive. The sum $20{,}000\ln 0.95=-1{,}026$ nats is an ordinary number, which is why every likelihood in this wiki is computed as a sum of logs, and why the softmax behind a classifier's loss is evaluated with the log-sum-exp identity of [[02-foundations/engineering-math|0.5 §6]].

Logarithms are useful because they turn the joint probability of many observations into an additive score. For example, a classifier can assign plausible labels to most frames yet be strongly penalized for confidently rejecting the correct label on a few. **The reading this gives you.** When a paper reports a log loss, ask which events receive probability and how the score is aggregated. A loss decrease concerns those assigned probabilities; it does not automatically imply a particular improvement in task success. Before comparing two reported losses, put them in one base and one normalization: $0.693$ nats is one bit, and a log-likelihood summed over a dataset grows in magnitude with the number of samples, one term per sample by rule 1, so only per-sample or per-token averages compare across datasets (§2 turns the per-token average into perplexity).

### 1. Surprise and entropy

A reading tells you something only if you could not already predict it, so every learning system needs one number for how unexpected a single outcome was and one for how unpredictable a whole source is. This section defines both — surprise and its average, entropy — and prices them in bits on the crack detector.

- **Surprise** of an outcome: $-\log p(x)$. Rare events carry more information (a sensor
  reading you predicted perfectly tells you nothing).
  Also called *self-information* or *Shannon information content*, it is a function of one outcome's probability:
  $$h(x) = -\log p(x) = \log\frac{1}{p(x)}$$
  where $p(x)$ is the probability the model gives outcome $x$. Its three properties are what make the log the right choice: $h(x) \ge 0$ since $p(x) \le 1$; $h(x) = 0$ exactly when $p(x) = 1$ (a certain outcome tells you nothing); and for independent outcomes it *adds*, $h(x, y) = h(x) + h(y)$, since $p(x,y) = p(x)p(y)$ and the log turns the product into a sum. *Example:* an outcome of probability $\tfrac18$ carries $\log_2 8 = 3$ bits, and two heads from two fair coins carry $\log_2 4 = 2 = 1 + 1$ bits.
- **Entropy** = expected surprise:
  $H(p) = -\sum_x p(x)\log p(x)$
  — how unpredictable a source is, in bits (log base 2) or nats (log base e).
  Uniform distribution = maximum entropy; deterministic = zero.
  Written out, for a discrete random variable $X$ with PMF $p$ over a set $\mathcal{X}$ of $|\mathcal{X}|$ possible values:
  $$H(X) = E_{x \sim p}[h(x)] = -\sum_{x \in \mathcal{X}} p(x)\log p(x), \qquad 0 \le H(X) \le \log|\mathcal{X}|$$
  using the convention $0 \log 0 = 0$, since an impossible outcome contributes nothing. The lower bound holds because every surprise is $\ge 0$, with equality only when one outcome has probability 1. The upper bound is reached only by the uniform distribution. *Example:* uniform over 8 values gives $\log_2 8 = 3$ bits, the most any 8-valued source can have. Entropy depends only on the probabilities, not on the values: relabelling outcomes, or a die with faces $10, 20, \dots, 60$, leaves it unchanged.
- **Joint and conditional entropy** extend the same average to two variables $X$ and $Y$ with joint PMF $p(x,y)$. Joint entropy is the uncertainty of the pair. Conditional entropy is the uncertainty left in $X$ once $Y$ is known, averaged over the values of $Y$:
  $$H(X,Y) = -\sum_{x,y} p(x,y)\log p(x,y), \qquad H(X \mid Y) = \sum_y p(y)\,H(X \mid Y{=}y) = -\sum_{x,y} p(x,y)\log p(x \mid y)$$
  They are tied by the **chain rule** $H(X,Y) = H(Y) + H(X \mid Y)$, since $\log p(x,y) = \log p(y) + \log p(x \mid y)$. On average, conditioning never increases uncertainty: $H(X \mid Y) \le H(X)$, with equality iff $X$ and $Y$ are independent (§4 turns the gap into mutual information).
  - *Example* (the crack detector of the picture, $X$ = crack, $Y$ = alarm): $H(X) = 0.081$ bits. After an alarm $P(\text{crack}) = 0.161$, so $H(X \mid Y{=}1) = 0.637$ bits; after silence it is $0.0005/0.941 = 0.00053$, so $H(X \mid Y{=}0) = 0.0065$ bits. Weighting by how often each happens, $H(X \mid Y) = 0.059 \times 0.637 + 0.941 \times 0.0065 = 0.044$ bits.
  - *Non-example, the boundary readers miss:* the inequality is about the average only. After an alarm the uncertainty is $0.637$ bits, far *more* than the $0.081$ before, so a single observation can raise uncertainty; it is outweighed by the silent case, $0.0065$ bits, which happens 94% of the time.
- **Expected code length.** A **code** $C$ assigns each outcome $x$ a binary codeword of length $\ell(x)$ bits. Its average cost is
  $$L(C, X) = \sum_x p(x)\,\ell(x)$$
  so frequent outcomes should get short words. *Example:* the Huffman code for $p = (0.7, 0.2, 0.1)$ has lengths $(1, 2, 2)$ and $L = 0.7 + 0.4 + 0.2 = 1.3$ bits, the figure used in §2.
- Intuition anchor: entropy is a **lower bound** on the average number of yes/no questions needed to
  identify an outcome — the *compression limit* of the source. No code beats it, and a per-symbol
  code generally does not reach it: the Huffman code's $1.3$ bits sit above this source's $1.157$ bits (§2).

> [!note]- Deeper · 더 깊이
> **Which codes the bound covers.** A code is *uniquely decodable* if every concatenation of codewords can be split back in only one way, and a *prefix code* (no codeword begins another; built as a tree in [[02-foundations/algorithms/greedy-mst|11.4 §5]]) is the common kind that can be decoded on the fly. Every uniquely decodable code has $L(C,X) \ge H(X)$, with equality only when every code length equals its Shannon information content — the surprise $\log_2(1/p(x))$ defined above, in bits (MacKay eq. 5.17) — and MacKay's Theorem 5.1 guarantees that *some* prefix code achieves $L(C,X) < H(X)+1$.

- **Worked numbers** — a coin with $P(\text{H}) = 0.9$:
  $H = -0.9\log_2 0.9 - 0.1\log_2 0.1 = 0.9(0.152) + 0.1(3.322) \approx 0.47$ bits —
  less than half the fair coin's 1 bit, because the outcome is mostly predictable.
  And the KL from this coin to a fair coin:
  $D_{KL} = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5} \approx 0.763 - 0.232 = 0.53$
  bits — the *extra* cost per toss of encoding the biased coin with the fair-coin code.
  Run these two computations by hand once; every formula on this page becomes concrete.
- **Differential entropy** is the continuous-variable analogue, used when $X$ has a density $p(x)$ rather than a PMF (it is the quantity [[02-foundations/probability|3. Probability §3]] cites for the Gaussian):
  $$h(X) = -\int p(x)\log p(x)\,dx$$
  It keeps the formula but not all the meaning. Because a density can exceed 1, $h$ can be negative, and it changes when you change units, since rescaling $X$ by $a$ adds $\log|a|$. So it is not a count of bits; only *differences* of differential entropies (as in mutual information and KL) keep their meaning. Mind the letter: this $h(X)$, of a random variable with a density, is not the surprise $h(x)$ of one outcome from the top of this section; two conventions share it (MacKay writes the surprise $h(x)$, Cover and Thomas the differential entropy $h(X)$), so read the argument — one outcome means a surprise, a continuous random variable a differential entropy.
  - *Examples:* uniform on $[0, a]$ has $h = \log a$, so uniform on $[0, 0.5]$ has $h = -1$ bit. A Gaussian with variance $\sigma^2$ has $h = \tfrac12\log(2\pi e\sigma^2)$, which is $2.047$ bits for $\sigma = 1$, the largest of any density with that variance.

### 2. Cross-entropy — the loss function you already use

Training a classifier or a language model means scoring a predicted distribution against what actually happened, and the score nearly all of them use is cross-entropy. This section defines it, prices it in bits on a three-symbol example and on the crack detector, and shows that it is the maximum-likelihood loss.

- $H(p, q) = -\sum_x p(x)\log q(x)$: the cost of encoding data from true distribution $p$
  using a code optimized for your model $q$.
  It is a function of **two** distributions over the same outcomes, the true (or data) distribution $p$ and the model $q$:
  $$H(p, q) = E_{x \sim p}\big[-\log q(x)\big] = -\sum_x p(x)\log q(x)$$
  so it is the surprise *measured by the model*, averaged over outcomes drawn *from the truth*. Its defining properties: $H(p,q) \ge H(p)$ with equality iff $q = p$ (§3 proves this), and it is not symmetric in $p$ and $q$. In training, $p$ is the empirical distribution of $N$ labelled examples, so the loss is the average $-\frac1N\sum_{i=1}^N \log q(y_i \mid x_i)$ of the model's surprise at each true label $y_i$. *Non-example of a usable model:* if $q(x) = 0$ for an outcome with $p(x) > 0$, the cross-entropy is infinite, which is why classifiers output a softmax ([[02-foundations/engineering-math|0.5 §10]]) that never assigns exactly 0.
- **Worked, in bits.** True $p = (0.7,\,0.2,\,0.1)$, model $q = (0.5,\,0.3,\,0.2)$.
  $$H(p) = -[0.7\log_2 0.7 + 0.2\log_2 0.2 + 0.1\log_2 0.1] = 1.157\ \text{bits}$$
  $$H(p,q) = -[0.7\log_2 0.5 + 0.2\log_2 0.3 + 0.1\log_2 0.2] = 1.280\ \text{bits}$$
  The model costs $1.280$ bits per symbol where $1.157$ is the floor — an overpayment of
  $0.123$ bits. Hold that number; §3 shows it is exactly the KL.

<svg viewBox="0 0 560 150" style="max-width:100%;height:auto" role="img" aria-label="two bars of bits per symbol: the entropy floor of 1.157 bits and the 1.280 bits a code built for the model pays, with the 0.123-bit excess marked as the KL divergence">
  <g fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2">
    <rect x="156" y="30" width="231.4" height="26" rx="3"/>
    <rect x="156" y="72" width="231.4" height="26" rx="3"/>
  </g>
  <rect x="387.4" y="72" width="24.6" height="26" rx="2" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2"/>
  <line x1="387.4" y1="22" x2="387.4" y2="108" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity="0.5"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.55"><line x1="156" y1="118" x2="416" y2="118"/><line x1="156" y1="114" x2="156" y2="122"/><line x1="356" y1="114" x2="356" y2="122"/></g>
  <g font-size="11" fill="currentColor">
    <text x="16" y="47">H(p) = 1.157 bits</text>
    <text x="16" y="89">H(p, q) = 1.280 bits</text>
    <text x="422.0" y="89">KL = 0.123</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="156" y="134" text-anchor="middle">0</text>
    <text x="356" y="134" text-anchor="middle">1 bit</text>
    <text x="395.4" y="134">the floor: no code beats it</text>
  </g>
</svg>

Bits per symbol for $p=(0.7,\,0.2,\,0.1)$: the entropy floor $H(p)=1.157$ bits, which no code beats, and the $1.280$ bits that a code built for the model $q=(0.5,\,0.3,\,0.2)$ pays. The dark excess, $0.123$ bits, is the KL divergence of §3, so minimizing cross-entropy is minimizing KL: the floor is set by the data, and every bit of training progress narrows the dark band.

- **Worked: P5 crack detector.** Catalog $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$ ([[02-foundations/lab-plants|0.6]]). $P(+)=0.059$, $P(c|+)\approx 0.161$. The true posterior is Bernoulli($0.161$) with $H(p)\approx 0.64$ bits. A model that treats the *sensitivity* $0.95$ as if it were $P(c|+)$ pays $H(p,q)\approx 3.64$ bits. False alarms from the $99\%$ non-crack mass ($0.0495$) dominate true positives ($0.0095$). Sensitivity is $P(+|c)$, not $P(c|+)$. The picture at the top of the page is this channel, drawn.
- Classification training: $p$ = one-hot label, $q$ = softmax output ⇒
  cross-entropy loss $= -\log q(\text{correct class})$. Every other term is multiplied by
  $p(x) = 0$ and vanishes — which is why the loss in code is a *single* log. If the model
  gives the correct class probability $0.5$, the loss is $-\log 0.5 = 0.693$ nats ($=1$ bit);
  at $0.9$ it is $0.105$; at $0.99$, $0.010$. The loss falls steeply at first and then barely
  moves — most of the training signal comes from examples the model still gets wrong.
  **Minimizing cross-entropy = MLE** (see [[02-foundations/probability|3. Probability §4]]).
- Language models: per-token cross-entropy is *the* pretraining objective
  ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]); **perplexity** $= 2^{H(p,q)}$ when $H$ is in bits, $e^{H(p,q)}$ when it is in nats — "the model is as
  confused as if choosing among perplexity-many options."
  On a test text of $N$ tokens $w_1, \dots, w_N$, it is the exponential of the average per-token cross-entropy, where $q(w_i \mid w_{<i})$ is the probability the model gave the actual next token:
  $$\text{PPL} = \exp\Big(-\frac1N \sum_{i=1}^N \ln q(w_i \mid w_{<i})\Big)$$
  The reading as "effective number of options" is exact for a uniform guess, since a model that spreads probability evenly over $K$ tokens has cross-entropy $\ln K$ and so $\text{PPL} = K$. *Example:* the model $q$ of the worked example above pays $1.280$ bits, so its perplexity is $2^{1.280} = 2.43$ options, against $2^{1.157} = 2.23$ for the true distribution. Perplexities are comparable only on the same tokenizer and test set, because changing either changes $N$ and the outcomes.

> [!note]- Deeper · 더 깊이
> **Codes, blocks and the entropy rate.** The entropies and cross-entropies above are expected costs, not code lengths. Entropy bounds the *expected* length, and a per-symbol code reaches it only when every probability is a power of two, because a symbol's code length has to be a whole number of bits: for $p = (0.7, 0.2, 0.1)$ the best symbol code is Huffman at $1.3$ bits against the floor of $1.157$ (built and proved optimal in [[02-foundations/algorithms/greedy-mst|11.4 §5]]). The floor is approached by coding long blocks of **i.i.d.** ([[02-foundations/probability|3. Probability §2]]) symbols, which is what Shannon's source coding theorem says — $N$ i.i.d. variables compress into about $NH(X)$ bits as $N\to\infty$. That hypothesis matters for language models: tokens are strongly dependent, so their floor is the entropy *rate*, not a single-symbol entropy. The **entropy rate** of a sequence $X_1, X_2, \dots$ is the per-symbol uncertainty once all dependence is accounted for:
> $$H_{\text{rate}} = \lim_{n\to\infty} \frac1n H(X_1, \dots, X_n)$$
> For i.i.d. symbols it equals $H(X_1)$, because the joint entropy of independent symbols is the sum of theirs. *Non-example:* a binary sequence that repeats its previous symbol with probability 0.9 spends half its time on each symbol, so the single-symbol entropy is 1 bit, but its entropy rate is only $H(0.9, 0.1) = 0.469$ bits, since each symbol is mostly predicted by the one before.

### 3. KL divergence — the distance-that-isn't

Cross-entropy mixes two things: the uncertainty of the data itself, which no model can remove, and the model's own mismatch. KL divergence is the second part alone — the excess of §2's $1.280$ bits over the $1.157$-bit floor — and it is what VAEs, RLHF penalties and distillation minimize.

- $D_{KL}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$
  — the *extra* bits paid for using $q$ when the truth is $p$.
  The **Kullback–Leibler divergence** is a function of an ordered pair of distributions on the same outcomes, the reference $p$ (first slot, the one you average over) and the approximation $q$ (second slot):
  $$D_{KL}(p\,\|\,q) = E_{x\sim p}\Big[\log\frac{p(x)}{q(x)}\Big], \qquad D_{KL}(p\,\|\,q) = \int p(x)\log\frac{p(x)}{q(x)}\,dx \ \text{(densities)}$$
  It is finite only if $q(x) > 0$ wherever $p(x) > 0$, since a term with $p(x) > 0 = q(x)$ is $+\infty$; terms with $p(x) = 0$ contribute 0. It is a *divergence*, not a distance: of the four metric axioms it keeps non-negativity and "zero iff equal" (proved below) but fails **symmetry** and the **triangle inequality**.
- **Same numbers as §2, computed directly** — substitute $p = (0.7, 0.2, 0.1)$ and $q = (0.5, 0.3, 0.2)$ into the sum term by term:
  $$D_{KL} = 0.7\log_2\tfrac{0.7}{0.5} + 0.2\log_2\tfrac{0.2}{0.3} + 0.1\log_2\tfrac{0.1}{0.2} = 0.340 - 0.117 - 0.100 = 0.123\ \text{bits}$$
  — exactly $H(p,q) - H(p) = 1.280 - 1.157$. Two things become visible: individual terms
  **can be negative** (the middle one is), yet the total never is; and the total is zero only
  when $q = p$ everywhere.
  - *Non-example of symmetry:* swapping the slots gives $D_{KL}(q\,\|\,p) = 0.133$ bits, not $0.123$.
  - *Non-example of the triangle inequality:* for coins with heads probability $0.1$, $0.5$ and $0.9$, going directly costs $D_{KL}(0.1\,\|\,0.9) = 2.536$ bits, more than the detour $D_{KL}(0.1\,\|\,0.5) + D_{KL}(0.5\,\|\,0.9) = 0.531 + 0.737 = 1.268$ bits.

- **Jensen's inequality** is a statement about a function $f$ and a random variable $X$. If $f$ is concave (it lies above its chords, the reverse of the convexity condition in [[02-foundations/optimization|4. Optimization §2]]), then
  $$E[f(X)] \le f\big(E[X]\big)$$
  and the inequality flips for convex $f$. Equality holds when $X$ is constant, and for strictly concave $f$ (such as $\log$) only then. Why: a chord of a concave graph lies below the graph, so the weighted average of the values $f(x)$ sits below the value of $f$ at the weighted average of the points. *Example:* $X$ is $1$ or $4$ with equal probability, $f = \log_2$. Then $E[\log_2 X] = \tfrac{0 + 2}{2} = 1$ while $\log_2 E[X] = \log_2 2.5 = 1.32$.
- **Non-negativity, proved in two lines** (Jensen's inequality — $\log$ is concave, so that the expectation of a log is at most the log of the expectation):
  $$-D_{KL}(p\|q) = E_p\Big[\log\frac{q}{p}\Big] \le \log E_p\Big[\frac{q}{p}\Big] = \log \sum_{x:\,p(x)>0} q(x) \le \log 1 = 0$$
  Equality iff $p = q$. This tiny proof powers the ELBO's validity and half of learning theory.
- **Gaussian KL, closed form** (the formula inside every VAE implementation): for
  $\mathcal{N}(\mu_1,\sigma_1^2)$ vs $\mathcal{N}(\mu_2,\sigma_2^2)$:
  $$D_{KL} = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac12$$
  Against a standard normal prior ($\mu_2=0, \sigma_2=1$) this is the exact regularizer
  term coded in [[01-canonical-papers/notes/6-diffusion/vae|VAE]] losses.
  Read the three terms rather than memorizing them: $\log(\sigma_2/\sigma_1)$ charges for
  having the wrong *width*, the fraction charges for the mismatch in spread and in mean —
  both measured in units of the **target's** variance, which is why $\sigma_2$ sits in the
  denominator and why the penalty is asymmetric — and the $-\tfrac12$ is the constant that
  makes the whole thing vanish when the two distributions coincide. Set
  $\sigma_1 = \sigma_2$ and $\mu_1 = \mu_2$: the first term is $0$, the fraction is
  $\tfrac12$, and the total is $0$, as it must be.
  *Numbers, in nats (natural log):* $D_{KL}\big(\mathcal{N}(1,1)\,\|\,\mathcal{N}(0,1)\big) = 0 + \tfrac{1 + 1}{2} - \tfrac12 = 0.5$. With widths instead, $D_{KL}\big(\mathcal{N}(0,2^2)\,\|\,\mathcal{N}(0,1)\big) = 0.807$ but $D_{KL}\big(\mathcal{N}(0,1)\,\|\,\mathcal{N}(0,2^2)\big) = 0.318$: a first-slot distribution twice as wide as the second costs more than one half as wide. The formula is derived term by term, as the expectation of the log-ratio under the first slot, in [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs §2]].
- Properties that matter: $\ge 0$, zero iff $p = q$, and **asymmetric** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$ true, fit $q$): mode-**covering** — $q$ spreads to cover all of $p$'s mass.
  - Reverse KL (used in *variational inference* — approximating an intractable distribution
    by picking the closest member of a simple family): mode-**seeking** — $q$ locks onto one mode.
  - The two are two different optimization problems over a family $\mathcal{Q}$ of simple distributions:
  $$q_{\text{fwd}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(p\,\|\,q), \qquad q_{\text{rev}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(q\,\|\,p)$$
    The behaviours follow from where the infinite penalty sits. Forward KL averages over $p$, so it punishes $q \approx 0$ anywhere $p$ has mass; reverse KL averages over $q$, so it punishes $q$ putting mass where $p \approx 0$. *Example:* fit a single Gaussian to the two-bump mixture $p = \tfrac12\mathcal{N}(-2, 0.5^2) + \tfrac12\mathcal{N}(2, 0.5^2)$. Forward KL gives $\mathcal{N}(0, 2.06^2)$, which matches the mixture's mean $0$ and variance $0.5^2 + 2^2 = 4.25$ — for a Gaussian $q$ the only part of $D_{KL}(p\,\|\,q)$ that depends on $q$ is $-E_p[\log q]$, which sees $p$ only through its mean and variance, so the best $q$ copies both — and puts its peak where $p$ has almost no mass (KL $0.72$ nats). Reverse KL gives $\mathcal{N}(2, 0.5^2)$ (or its mirror at $-2$), one bump exactly, at KL $0.69$ nats. Each answer is poor under the other criterion: the wide fit costs $2.10$ nats in reverse KL, and the one-bump fit costs $15.3$ nats in forward KL.
  This asymmetry contributes to VAEs' limited posterior coverage and to RL-style objectives
  collapsing to narrow behaviors — though classical VAE blur is *primarily* the Gaussian
  pixel likelihood averaging plausible outputs (see the self-check answer below).

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="One Gaussian fitted to the two-bump mixture p: forward KL gives N(0, 2.06 squared), covering both bumps with its peak in the empty middle at 0.72 nats; reverse KL gives N(2, 0.5 squared), locked onto one bump at 0.69 nats">
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55"><line x1="40" y1="222" x2="520" y2="222"/><line x1="40" y1="222" x2="40" y2="44"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45"><line x1="88" y1="222" x2="88" y2="226"/><line x1="184" y1="222" x2="184" y2="226"/><line x1="280" y1="222" x2="280" y2="226"/><line x1="376" y1="222" x2="376" y2="226"/><line x1="472" y1="222" x2="472" y2="226"/><line x1="36" y1="182" x2="40" y2="182"/><line x1="36" y1="142" x2="40" y2="142"/><line x1="36" y1="102" x2="40" y2="102"/><line x1="36" y1="62" x2="40" y2="62"/></g>
  <path d="M40 222 L41.2 222 L42.4 222 L43.6 222 L44.8 222 L46 222 L47.2 222 L48.4 222 L49.6 222 L50.8 222 L52 222 L53.2 222 L54.4 222 L55.6 222 L56.8 222 L58 222 L59.2 222 L60.4 222 L61.6 222 L62.8 222 L64 222 L65.2 222 L66.4 222 L67.6 222 L68.8 222 L70 222 L71.2 222 L72.4 222 L73.6 222 L74.8 222 L76 222 L77.2 222 L78.4 222 L79.6 222 L80.8 222 L82 222 L83.2 222 L84.4 222 L85.6 222 L86.8 222 L88 222 L89.2 222 L90.4 222 L91.6 222 L92.8 221.9 L94 221.9 L95.2 221.9 L96.4 221.9 L97.6 221.9 L98.8 221.9 L100 221.8 L101.2 221.8 L102.4 221.8 L103.6 221.7 L104.8 221.7 L106 221.6 L107.2 221.5 L108.4 221.4 L109.6 221.3 L110.8 221.2 L112 221.1 L113.2 221 L114.4 220.8 L115.6 220.6 L116.8 220.4 L118 220.2 L119.2 219.9 L120.4 219.6 L121.6 219.3 L122.8 218.9 L124 218.5 L125.2 218 L126.4 217.5 L127.6 217 L128.8 216.3 L130 215.7 L131.2 214.9 L132.4 214.1 L133.6 213.2 L134.8 212.2 L136 211.2 L137.2 210.1 L138.4 208.9 L139.6 207.6 L140.8 206.2 L142 204.7 L143.2 203.2 L144.4 201.5 L145.6 199.8 L146.8 198 L148 196.1 L149.2 194.1 L150.4 192.1 L151.6 189.9 L152.8 187.7 L154 185.5 L155.2 183.2 L156.4 180.8 L157.6 178.4 L158.8 176 L160 173.6 L161.2 171.2 L162.4 168.8 L163.6 166.4 L164.8 164.1 L166 161.8 L167.2 159.5 L168.4 157.4 L169.6 155.4 L170.8 153.4 L172 151.6 L173.2 149.9 L174.4 148.3 L175.6 147 L176.8 145.7 L178 144.7 L179.2 143.8 L180.4 143.1 L181.6 142.6 L182.8 142.3 L184 142.2 L185.2 142.3 L186.4 142.6 L187.6 143.1 L188.8 143.8 L190 144.7 L191.2 145.7 L192.4 147 L193.6 148.3 L194.8 149.9 L196 151.6 L197.2 153.4 L198.4 155.4 L199.6 157.4 L200.8 159.5 L202 161.8 L203.2 164.1 L204.4 166.4 L205.6 168.8 L206.8 171.2 L208 173.6 L209.2 176 L210.4 178.4 L211.6 180.8 L212.8 183.2 L214 185.5 L215.2 187.7 L216.4 189.9 L217.6 192.1 L218.8 194.1 L220 196.1 L221.2 198 L222.4 199.8 L223.6 201.5 L224.8 203.2 L226 204.7 L227.2 206.2 L228.4 207.6 L229.6 208.9 L230.8 210.1 L232 211.2 L233.2 212.2 L234.4 213.2 L235.6 214.1 L236.8 214.9 L238 215.7 L239.2 216.3 L240.4 217 L241.6 217.5 L242.8 218 L244 218.5 L245.2 218.9 L246.4 219.3 L247.6 219.6 L248.8 219.9 L250 220.2 L251.2 220.4 L252.4 220.6 L253.6 220.8 L254.8 221 L256 221.1 L257.2 221.2 L258.4 221.3 L259.6 221.4 L260.8 221.5 L262 221.6 L263.2 221.7 L264.4 221.7 L265.6 221.8 L266.8 221.8 L268 221.8 L269.2 221.8 L270.4 221.9 L271.6 221.9 L272.8 221.9 L274 221.9 L275.2 221.9 L276.4 221.9 L277.6 221.9 L278.8 221.9 L280 221.9 L281.2 221.9 L282.4 221.9 L283.6 221.9 L284.8 221.9 L286 221.9 L287.2 221.9 L288.4 221.9 L289.6 221.9 L290.8 221.8 L292 221.8 L293.2 221.8 L294.4 221.8 L295.6 221.7 L296.8 221.7 L298 221.6 L299.2 221.5 L300.4 221.4 L301.6 221.3 L302.8 221.2 L304 221.1 L305.2 221 L306.4 220.8 L307.6 220.6 L308.8 220.4 L310 220.2 L311.2 219.9 L312.4 219.6 L313.6 219.3 L314.8 218.9 L316 218.5 L317.2 218 L318.4 217.5 L319.6 217 L320.8 216.3 L322 215.7 L323.2 214.9 L324.4 214.1 L325.6 213.2 L326.8 212.2 L328 211.2 L329.2 210.1 L330.4 208.9 L331.6 207.6 L332.8 206.2 L334 204.7 L335.2 203.2 L336.4 201.5 L337.6 199.8 L338.8 198 L340 196.1 L341.2 194.1 L342.4 192.1 L343.6 189.9 L344.8 187.7 L346 185.5 L347.2 183.2 L348.4 180.8 L349.6 178.4 L350.8 176 L352 173.6 L353.2 171.2 L354.4 168.8 L355.6 166.4 L356.8 164.1 L358 161.8 L359.2 159.5 L360.4 157.4 L361.6 155.4 L362.8 153.4 L364 151.6 L365.2 149.9 L366.4 148.3 L367.6 147 L368.8 145.7 L370 144.7 L371.2 143.8 L372.4 143.1 L373.6 142.6 L374.8 142.3 L376 142.2 L377.2 142.3 L378.4 142.6 L379.6 143.1 L380.8 143.8 L382 144.7 L383.2 145.7 L384.4 147 L385.6 148.3 L386.8 149.9 L388 151.6 L389.2 153.4 L390.4 155.4 L391.6 157.4 L392.8 159.5 L394 161.8 L395.2 164.1 L396.4 166.4 L397.6 168.8 L398.8 171.2 L400 173.6 L401.2 176 L402.4 178.4 L403.6 180.8 L404.8 183.2 L406 185.5 L407.2 187.7 L408.4 189.9 L409.6 192.1 L410.8 194.1 L412 196.1 L413.2 198 L414.4 199.8 L415.6 201.5 L416.8 203.2 L418 204.7 L419.2 206.2 L420.4 207.6 L421.6 208.9 L422.8 210.1 L424 211.2 L425.2 212.2 L426.4 213.2 L427.6 214.1 L428.8 214.9 L430 215.7 L431.2 216.3 L432.4 217 L433.6 217.5 L434.8 218 L436 218.5 L437.2 218.9 L438.4 219.3 L439.6 219.6 L440.8 219.9 L442 220.2 L443.2 220.4 L444.4 220.6 L445.6 220.8 L446.8 221 L448 221.1 L449.2 221.2 L450.4 221.3 L451.6 221.4 L452.8 221.5 L454 221.6 L455.2 221.7 L456.4 221.7 L457.6 221.8 L458.8 221.8 L460 221.8 L461.2 221.9 L462.4 221.9 L463.6 221.9 L464.8 221.9 L466 221.9 L467.2 221.9 L468.4 222 L469.6 222 L470.8 222 L472 222 L473.2 222 L474.4 222 L475.6 222 L476.8 222 L478 222 L479.2 222 L480.4 222 L481.6 222 L482.8 222 L484 222 L485.2 222 L486.4 222 L487.6 222 L488.8 222 L490 222 L491.2 222 L492.4 222 L493.6 222 L494.8 222 L496 222 L497.2 222 L498.4 222 L499.6 222 L500.8 222 L502 222 L503.2 222 L504.4 222 L505.6 222 L506.8 222 L508 222 L509.2 222 L510.4 222 L511.6 222 L512.8 222 L514 222 L515.2 222 L516.4 222 L517.6 222 L518.8 222 L520 222" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="2.4"/>
  <path d="M40 220 L41.2 219.9 L42.4 219.8 L43.6 219.8 L44.8 219.7 L46 219.6 L47.2 219.6 L48.4 219.5 L49.6 219.4 L50.8 219.4 L52 219.3 L53.2 219.2 L54.4 219.1 L55.6 219 L56.8 219 L58 218.9 L59.2 218.8 L60.4 218.7 L61.6 218.6 L62.8 218.5 L64 218.4 L65.2 218.3 L66.4 218.2 L67.6 218.1 L68.8 218 L70 217.9 L71.2 217.8 L72.4 217.7 L73.6 217.6 L74.8 217.5 L76 217.4 L77.2 217.3 L78.4 217.1 L79.6 217 L80.8 216.9 L82 216.8 L83.2 216.6 L84.4 216.5 L85.6 216.4 L86.8 216.2 L88 216.1 L89.2 216 L90.4 215.8 L91.6 215.7 L92.8 215.5 L94 215.4 L95.2 215.2 L96.4 215.1 L97.6 214.9 L98.8 214.8 L100 214.6 L101.2 214.4 L102.4 214.3 L103.6 214.1 L104.8 213.9 L106 213.8 L107.2 213.6 L108.4 213.4 L109.6 213.2 L110.8 213 L112 212.8 L113.2 212.7 L114.4 212.5 L115.6 212.3 L116.8 212.1 L118 211.9 L119.2 211.7 L120.4 211.5 L121.6 211.3 L122.8 211 L124 210.8 L125.2 210.6 L126.4 210.4 L127.6 210.2 L128.8 210 L130 209.7 L131.2 209.5 L132.4 209.3 L133.6 209 L134.8 208.8 L136 208.6 L137.2 208.3 L138.4 208.1 L139.6 207.9 L140.8 207.6 L142 207.4 L143.2 207.1 L144.4 206.9 L145.6 206.6 L146.8 206.4 L148 206.1 L149.2 205.8 L150.4 205.6 L151.6 205.3 L152.8 205.1 L154 204.8 L155.2 204.5 L156.4 204.3 L157.6 204 L158.8 203.7 L160 203.4 L161.2 203.2 L162.4 202.9 L163.6 202.6 L164.8 202.3 L166 202.1 L167.2 201.8 L168.4 201.5 L169.6 201.2 L170.8 200.9 L172 200.7 L173.2 200.4 L174.4 200.1 L175.6 199.8 L176.8 199.5 L178 199.2 L179.2 199 L180.4 198.7 L181.6 198.4 L182.8 198.1 L184 197.8 L185.2 197.5 L186.4 197.3 L187.6 197 L188.8 196.7 L190 196.4 L191.2 196.1 L192.4 195.8 L193.6 195.6 L194.8 195.3 L196 195 L197.2 194.7 L198.4 194.5 L199.6 194.2 L200.8 193.9 L202 193.6 L203.2 193.4 L204.4 193.1 L205.6 192.8 L206.8 192.6 L208 192.3 L209.2 192 L210.4 191.8 L211.6 191.5 L212.8 191.3 L214 191 L215.2 190.8 L216.4 190.5 L217.6 190.3 L218.8 190 L220 189.8 L221.2 189.6 L222.4 189.3 L223.6 189.1 L224.8 188.9 L226 188.7 L227.2 188.4 L228.4 188.2 L229.6 188 L230.8 187.8 L232 187.6 L233.2 187.4 L234.4 187.2 L235.6 187 L236.8 186.8 L238 186.6 L239.2 186.5 L240.4 186.3 L241.6 186.1 L242.8 185.9 L244 185.8 L245.2 185.6 L246.4 185.5 L247.6 185.3 L248.8 185.2 L250 185 L251.2 184.9 L252.4 184.8 L253.6 184.7 L254.8 184.5 L256 184.4 L257.2 184.3 L258.4 184.2 L259.6 184.1 L260.8 184 L262 183.9 L263.2 183.9 L264.4 183.8 L265.6 183.7 L266.8 183.6 L268 183.6 L269.2 183.5 L270.4 183.5 L271.6 183.4 L272.8 183.4 L274 183.4 L275.2 183.3 L276.4 183.3 L277.6 183.3 L278.8 183.3 L280 183.3 L281.2 183.3 L282.4 183.3 L283.6 183.3 L284.8 183.3 L286 183.4 L287.2 183.4 L288.4 183.4 L289.6 183.5 L290.8 183.5 L292 183.6 L293.2 183.6 L294.4 183.7 L295.6 183.8 L296.8 183.9 L298 183.9 L299.2 184 L300.4 184.1 L301.6 184.2 L302.8 184.3 L304 184.4 L305.2 184.5 L306.4 184.7 L307.6 184.8 L308.8 184.9 L310 185 L311.2 185.2 L312.4 185.3 L313.6 185.5 L314.8 185.6 L316 185.8 L317.2 185.9 L318.4 186.1 L319.6 186.3 L320.8 186.5 L322 186.6 L323.2 186.8 L324.4 187 L325.6 187.2 L326.8 187.4 L328 187.6 L329.2 187.8 L330.4 188 L331.6 188.2 L332.8 188.4 L334 188.7 L335.2 188.9 L336.4 189.1 L337.6 189.3 L338.8 189.6 L340 189.8 L341.2 190 L342.4 190.3 L343.6 190.5 L344.8 190.8 L346 191 L347.2 191.3 L348.4 191.5 L349.6 191.8 L350.8 192 L352 192.3 L353.2 192.6 L354.4 192.8 L355.6 193.1 L356.8 193.4 L358 193.6 L359.2 193.9 L360.4 194.2 L361.6 194.5 L362.8 194.7 L364 195 L365.2 195.3 L366.4 195.6 L367.6 195.8 L368.8 196.1 L370 196.4 L371.2 196.7 L372.4 197 L373.6 197.3 L374.8 197.5 L376 197.8 L377.2 198.1 L378.4 198.4 L379.6 198.7 L380.8 199 L382 199.2 L383.2 199.5 L384.4 199.8 L385.6 200.1 L386.8 200.4 L388 200.7 L389.2 200.9 L390.4 201.2 L391.6 201.5 L392.8 201.8 L394 202.1 L395.2 202.3 L396.4 202.6 L397.6 202.9 L398.8 203.2 L400 203.4 L401.2 203.7 L402.4 204 L403.6 204.3 L404.8 204.5 L406 204.8 L407.2 205.1 L408.4 205.3 L409.6 205.6 L410.8 205.8 L412 206.1 L413.2 206.4 L414.4 206.6 L415.6 206.9 L416.8 207.1 L418 207.4 L419.2 207.6 L420.4 207.9 L421.6 208.1 L422.8 208.3 L424 208.6 L425.2 208.8 L426.4 209 L427.6 209.3 L428.8 209.5 L430 209.7 L431.2 210 L432.4 210.2 L433.6 210.4 L434.8 210.6 L436 210.8 L437.2 211 L438.4 211.3 L439.6 211.5 L440.8 211.7 L442 211.9 L443.2 212.1 L444.4 212.3 L445.6 212.5 L446.8 212.7 L448 212.8 L449.2 213 L450.4 213.2 L451.6 213.4 L452.8 213.6 L454 213.8 L455.2 213.9 L456.4 214.1 L457.6 214.3 L458.8 214.4 L460 214.6 L461.2 214.8 L462.4 214.9 L463.6 215.1 L464.8 215.2 L466 215.4 L467.2 215.5 L468.4 215.7 L469.6 215.8 L470.8 216 L472 216.1 L473.2 216.2 L474.4 216.4 L475.6 216.5 L476.8 216.6 L478 216.8 L479.2 216.9 L480.4 217 L481.6 217.1 L482.8 217.3 L484 217.4 L485.2 217.5 L486.4 217.6 L487.6 217.7 L488.8 217.8 L490 217.9 L491.2 218 L492.4 218.1 L493.6 218.2 L494.8 218.3 L496 218.4 L497.2 218.5 L498.4 218.6 L499.6 218.7 L500.8 218.8 L502 218.9 L503.2 219 L504.4 219 L505.6 219.1 L506.8 219.2 L508 219.3 L509.2 219.4 L510.4 219.4 L511.6 219.5 L512.8 219.6 L514 219.6 L515.2 219.7 L516.4 219.8 L517.6 219.8 L518.8 219.9 L520 220" fill="none" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.8" stroke-dasharray="7 4"/>
  <path d="M40 222 L41.2 222 L42.4 222 L43.6 222 L44.8 222 L46 222 L47.2 222 L48.4 222 L49.6 222 L50.8 222 L52 222 L53.2 222 L54.4 222 L55.6 222 L56.8 222 L58 222 L59.2 222 L60.4 222 L61.6 222 L62.8 222 L64 222 L65.2 222 L66.4 222 L67.6 222 L68.8 222 L70 222 L71.2 222 L72.4 222 L73.6 222 L74.8 222 L76 222 L77.2 222 L78.4 222 L79.6 222 L80.8 222 L82 222 L83.2 222 L84.4 222 L85.6 222 L86.8 222 L88 222 L89.2 222 L90.4 222 L91.6 222 L92.8 222 L94 222 L95.2 222 L96.4 222 L97.6 222 L98.8 222 L100 222 L101.2 222 L102.4 222 L103.6 222 L104.8 222 L106 222 L107.2 222 L108.4 222 L109.6 222 L110.8 222 L112 222 L113.2 222 L114.4 222 L115.6 222 L116.8 222 L118 222 L119.2 222 L120.4 222 L121.6 222 L122.8 222 L124 222 L125.2 222 L126.4 222 L127.6 222 L128.8 222 L130 222 L131.2 222 L132.4 222 L133.6 222 L134.8 222 L136 222 L137.2 222 L138.4 222 L139.6 222 L140.8 222 L142 222 L143.2 222 L144.4 222 L145.6 222 L146.8 222 L148 222 L149.2 222 L150.4 222 L151.6 222 L152.8 222 L154 222 L155.2 222 L156.4 222 L157.6 222 L158.8 222 L160 222 L161.2 222 L162.4 222 L163.6 222 L164.8 222 L166 222 L167.2 222 L168.4 222 L169.6 222 L170.8 222 L172 222 L173.2 222 L174.4 222 L175.6 222 L176.8 222 L178 222 L179.2 222 L180.4 222 L181.6 222 L182.8 222 L184 222 L185.2 222 L186.4 222 L187.6 222 L188.8 222 L190 222 L191.2 222 L192.4 222 L193.6 222 L194.8 222 L196 222 L197.2 222 L198.4 222 L199.6 222 L200.8 222 L202 222 L203.2 222 L204.4 222 L205.6 222 L206.8 222 L208 222 L209.2 222 L210.4 222 L211.6 222 L212.8 222 L214 222 L215.2 222 L216.4 222 L217.6 222 L218.8 222 L220 222 L221.2 222 L222.4 222 L223.6 222 L224.8 222 L226 222 L227.2 222 L228.4 222 L229.6 222 L230.8 222 L232 222 L233.2 222 L234.4 222 L235.6 222 L236.8 222 L238 222 L239.2 222 L240.4 222 L241.6 222 L242.8 222 L244 222 L245.2 222 L246.4 222 L247.6 222 L248.8 222 L250 222 L251.2 222 L252.4 222 L253.6 222 L254.8 222 L256 222 L257.2 222 L258.4 222 L259.6 222 L260.8 222 L262 222 L263.2 222 L264.4 222 L265.6 222 L266.8 222 L268 222 L269.2 222 L270.4 222 L271.6 222 L272.8 222 L274 222 L275.2 222 L276.4 222 L277.6 222 L278.8 222 L280 221.9 L281.2 221.9 L282.4 221.9 L283.6 221.9 L284.8 221.9 L286 221.9 L287.2 221.8 L288.4 221.8 L289.6 221.8 L290.8 221.7 L292 221.7 L293.2 221.6 L294.4 221.5 L295.6 221.4 L296.8 221.3 L298 221.2 L299.2 221 L300.4 220.9 L301.6 220.7 L302.8 220.5 L304 220.2 L305.2 219.9 L306.4 219.6 L307.6 219.3 L308.8 218.8 L310 218.4 L311.2 217.8 L312.4 217.2 L313.6 216.6 L314.8 215.8 L316 215 L317.2 214.1 L318.4 213 L319.6 211.9 L320.8 210.7 L322 209.3 L323.2 207.8 L324.4 206.2 L325.6 204.4 L326.8 202.5 L328 200.4 L329.2 198.2 L330.4 195.8 L331.6 193.2 L332.8 190.4 L334 187.5 L335.2 184.4 L336.4 181.1 L337.6 177.6 L338.8 174 L340 170.2 L341.2 166.2 L342.4 162.1 L343.6 157.8 L344.8 153.5 L346 148.9 L347.2 144.3 L348.4 139.6 L349.6 134.9 L350.8 130 L352 125.2 L353.2 120.4 L354.4 115.6 L355.6 110.8 L356.8 106.1 L358 101.5 L359.2 97.1 L360.4 92.8 L361.6 88.7 L362.8 84.8 L364 81.2 L365.2 77.8 L366.4 74.7 L367.6 71.9 L368.8 69.4 L370 67.3 L371.2 65.6 L372.4 64.2 L373.6 63.2 L374.8 62.6 L376 62.4 L377.2 62.6 L378.4 63.2 L379.6 64.2 L380.8 65.6 L382 67.3 L383.2 69.4 L384.4 71.9 L385.6 74.7 L386.8 77.8 L388 81.2 L389.2 84.8 L390.4 88.7 L391.6 92.8 L392.8 97.1 L394 101.5 L395.2 106.1 L396.4 110.8 L397.6 115.6 L398.8 120.4 L400 125.2 L401.2 130 L402.4 134.9 L403.6 139.6 L404.8 144.3 L406 148.9 L407.2 153.5 L408.4 157.8 L409.6 162.1 L410.8 166.2 L412 170.2 L413.2 174 L414.4 177.6 L415.6 181.1 L416.8 184.4 L418 187.5 L419.2 190.4 L420.4 193.2 L421.6 195.8 L422.8 198.2 L424 200.4 L425.2 202.5 L426.4 204.4 L427.6 206.2 L428.8 207.8 L430 209.3 L431.2 210.7 L432.4 211.9 L433.6 213 L434.8 214.1 L436 215 L437.2 215.8 L438.4 216.6 L439.6 217.2 L440.8 217.8 L442 218.4 L443.2 218.8 L444.4 219.3 L445.6 219.6 L446.8 219.9 L448 220.2 L449.2 220.5 L450.4 220.7 L451.6 220.9 L452.8 221 L454 221.2 L455.2 221.3 L456.4 221.4 L457.6 221.5 L458.8 221.6 L460 221.7 L461.2 221.7 L462.4 221.8 L463.6 221.8 L464.8 221.8 L466 221.9 L467.2 221.9 L468.4 221.9 L469.6 221.9 L470.8 221.9 L472 221.9 L473.2 222 L474.4 222 L475.6 222 L476.8 222 L478 222 L479.2 222 L480.4 222 L481.6 222 L482.8 222 L484 222 L485.2 222 L486.4 222 L487.6 222 L488.8 222 L490 222 L491.2 222 L492.4 222 L493.6 222 L494.8 222 L496 222 L497.2 222 L498.4 222 L499.6 222 L500.8 222 L502 222 L503.2 222 L504.4 222 L505.6 222 L506.8 222 L508 222 L509.2 222 L510.4 222 L511.6 222 L512.8 222 L514 222 L515.2 222 L516.4 222 L517.6 222 L518.8 222 L520 222" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="2 3"/>
  <line x1="280" y1="179.3" x2="280" y2="167.3" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <g font-size="10.5" fill="currentColor" opacity="0.8">
    <text x="88" y="238" text-anchor="middle">−4</text>
    <text x="184" y="238" text-anchor="middle">−2</text>
    <text x="280" y="238" text-anchor="middle">0</text>
    <text x="376" y="238" text-anchor="middle">2</text>
    <text x="472" y="238" text-anchor="middle">4</text>
    <text x="32" y="186" text-anchor="end">0.2</text>
    <text x="32" y="146" text-anchor="end">0.4</text>
    <text x="32" y="106" text-anchor="end">0.6</text>
    <text x="32" y="66" text-anchor="end">0.8</text>
    <text x="520" y="238" text-anchor="end">x</text>
  </g>
  <text x="12" y="30" font-size="11" fill="currentColor" opacity="0.85">density</text>
  <text x="280" y="163.3" font-size="10.5" fill="currentColor" text-anchor="middle" opacity="0.85">its peak where p ≈ 0</text>
  <line x1="52" y1="58" x2="76" y2="58" stroke="currentColor" stroke-width="2.4" stroke-opacity="1.0"/>
  <text x="82" y="62" font-size="11" fill="currentColor">p = ½N(−2, 0.5²) + ½N(2, 0.5²)</text>
  <line x1="52" y1="80" x2="76" y2="80" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.8" stroke-dasharray="7 4"/>
  <text x="82" y="84" font-size="11" fill="currentColor">forward-KL fit N(0, 2.06²): KL(p‖q) 0.72 nats</text>
  <text x="82" y="98" font-size="10.5" fill="currentColor" opacity="0.8">scored by reverse KL(q‖p): 2.10</text>
  <line x1="52" y1="116" x2="76" y2="116" stroke="currentColor" stroke-width="2.2" stroke-opacity="1.0" stroke-dasharray="2 3"/>
  <text x="82" y="120" font-size="11" fill="currentColor">reverse-KL fit N(2, 0.5²): KL(q‖p) 0.69 nats</text>
  <text x="82" y="134" font-size="10.5" fill="currentColor" opacity="0.8">scored by forward KL(p‖q): 15.3</text>
</svg>

One Gaussian fitted to the two-bump mixture $p=\tfrac12\mathcal N(-2,\,0.5^2)+\tfrac12\mathcal N(2,\,0.5^2)$ in the two directions. Forward KL averages over $p$, so the fit must cover both bumps and gives $\mathcal N(0,\,2.06^2)$, whose peak sits where $p\approx0$ ($0.72$ nats); reverse KL averages over $q$, so the fit may ignore a bump and locks onto one, $\mathcal N(2,\,0.5^2)$ at $0.69$ nats. Each fit is poor under the other criterion: $2.10$ nats for the wide fit, $15.3$ for the one-bump fit.

- Where you've seen it:
  - [[01-canonical-papers/notes/6-diffusion/vae|VAE]]: the ELBO's regularizer $D_{KL}(q_\phi(z|x)\,\|\,p(z))$.
  - [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]]: per-token KL penalty keeping the
    policy near the SFT model — literally "don't drift too many bits from the reference."
  - [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]: the variational bound is a sum of KL terms between
    Gaussians (which is why it collapses to MSE).
  - Knowledge distillation: student minimizes KL to teacher's soft labels.

### 4. Mutual information

*Second pass: read it when a paper puts mutual information or a contrastive loss in its objective; the First pass stops at §3.*

How much does an alarm tell you about a crack, or an image about its caption? Mutual information answers in bits: it is the drop in uncertainty about one variable once the other is known, and it sees dependence that correlation misses.

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — how many bits knowing $Y$ tells you about $X$; zero iff independent.
  **Mutual information** is a number attached to a pair of random variables with joint distribution $p(x,y)$ and marginals $p(x)$, $p(y)$. It has three equivalent forms, each a different reading:
  $$I(X;Y) = \sum_{x,y} p(x,y)\log\frac{p(x,y)}{p(x)\,p(y)} = H(X) - H(X \mid Y) = H(X) + H(Y) - H(X,Y)$$
  The first says how far the joint is from the independent product $p(x)p(y)$ (a KL, §3); the second, how much knowing $Y$ reduces uncertainty about $X$ (§1); the third, how much the two entropies overlap. The second follows from the first by one substitution: $p(x,y) = p(y)\,p(x \mid y)$, so $\log\frac{p(x,y)}{p(x)p(y)} = \log\frac{p(x \mid y)}{p(x)} = -\log p(x) + \log p(x \mid y)$, and averaging over $p(x,y)$ turns the two terms into $H(X)$ and $-H(X \mid Y)$ by the definitions of §1. The third then follows from the chain rule of §1, $H(X \mid Y) = H(X,Y) - H(Y)$. Its properties: **symmetric**, $I(X;Y) = I(Y;X)$; **non-negative**, since it is a KL; **zero iff $X$ and $Y$ are independent**, because only then is the joint equal to the product; and bounded, $I(X;Y) \le \min\big(H(X), H(Y)\big)$.
- **Worked, with the crack detector from [[02-foundations/probability|3. Probability §1]].**
  $X$ = crack present ($P = 0.01$), $Y$ = alarm fires, with $P(Y{=}1|X{=}1) = 0.95$ and
  $P(Y{=}1|X{=}0) = 0.05$. Then $P(Y{=}1) = 0.95(0.01) + 0.05(0.99) = 0.059$. Computing the
  four joint terms gives $I(X;Y) = 0.037$ bits, while $H(X) = 0.081$ bits. So the alarm
  removes **46% of the uncertainty** about whether a crack is there — informative, but
  nothing like "knowing." That single ratio is the honest version of the sentence
  "our sensor detects cracks with 95% accuracy": high sensitivity on a rare event still
  leaves most of the question open, which is the same fact Bayes' rule showed as
  $P(X|Y) = 0.16$.
- **Non-example: zero correlation is not zero information.** Take $X$ uniform on $\{-1, 0, 1\}$ and $Y = X^2$, whose covariance is 0 ([[02-foundations/probability|3. Probability §2]]). Yet $I(X;Y) = H(Y) - H(Y \mid X) = H(\tfrac13, \tfrac23) - 0 = 0.918$ bits, since $X$ determines $Y$ completely. Mutual information sees any dependence, linear or not, which is why representation-learning papers use it instead of correlation.
- **InfoNCE / contrastive learning** ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]'s objective) is a
  lower bound on mutual information between views/modalities — "maximize what the image
  embedding tells you about the text embedding." Written out for a batch of $N$ pairs with
  similarity $s(\cdot,\cdot)$ and temperature $\tau$:
  $$\mathcal{L} = -\frac1N\sum_i \log\frac{e^{s(x_i,y_i)/\tau}}{\sum_j e^{s(x_i,y_j)/\tau}}$$
  — cross-entropy where "the classes" are the other samples in the batch; because it satisfies
  $I(X;Y) \ge \log N - \mathcal{L}$, bigger batches permit tighter bounds (CLIP used a batch of 32,768, though the paper
  states no information-theoretic reason for it). Caveat: the bound is guaranteed only when the negatives are independent draws from the marginal
  $p(y)$ (the proof below uses exactly that), and how tight it is depends on the score function and on $N$ — read the number as a floor under $I$, not an estimate of it.
  In the formula, $x_i$ and $y_i$ are the two views of the $i$-th pair, so the term $j = i$ is the positive and every $j \ne i$ is a negative. Since $\mathcal{L} \ge 0$, the bound can never certify more than $\log N$, which for CLIP's batch is $\ln 32{,}768 = 10.4$ nats (15 bits).
- **Why the InfoNCE bound holds.** The bound is from Oord, Li & Vinyals (2018, contrastive predictive coding); Poole et al. (ICML 2019) prove it rigorously, and the three steps below are a compact version of that multi-sample argument, using only §1–§3. Fix one anchor $x$ and write $f(x,y) = s(x,y)/\tau$ for its scaled score. Its row of the batch holds the positive $y_1 \sim p(y \mid x)$ and $N - 1$ negatives $y_2, \dots, y_N \sim p(y)$, all independent, and $\mathcal{L}$ is the expected loss $E\big[-\log\big(e^{f(x,y_1)}/\sum_j e^{f(x,y_j)}\big)\big]$. *Step 1, the negatives add nothing:* $Y_{2:N}$ is independent of $(X, Y_1)$, so by the chain rule of §1 $I(X;Y_1) = I(X;Y_{1:N})$. *Step 2, any normalized guess gives a lower bound:* for any conditional distribution $q(y_{1:N} \mid x)$, $I(X;Y_{1:N}) \ge E\big[\log\big(q(y_{1:N} \mid x)/p(y_{1:N})\big)\big]$, because the gap is the average of $D_{KL}\big(p(y_{1:N} \mid x)\,\|\,q(y_{1:N} \mid x)\big) \ge 0$ (§3). *Step 3, the softmax is such a guess:*
  $$q(y_{1:N} \mid x) = p(y_1)\cdots p(y_N)\cdot\frac{N\,e^{f(x,y_1)}}{\sum_{j=1}^{N} e^{f(x,y_j)}}$$
  sums to 1, because under $p(y_1)\cdots p(y_N)$ the $N$ positions are interchangeable, so each of the $N$ softmax weights averages to $1/N$ and the factor $N$ restores 1. Its log-ratio to $p(y_{1:N}) = p(y_1)\cdots p(y_N)$ is $\log N + \log\big(e^{f(x,y_1)}/\sum_j e^{f(x,y_j)}\big)$, so step 2 gives $I(X;Y) \ge \log N - \mathcal{L}$. The bound holds for every score function; a poor one only loosens it, and a constant score gives exactly $\log N - \log N = 0$.
  - *Worked on the crack detector* (anchor $X$, candidates the alarm readings $Y$, and the best score $f = \log\frac{p(y \mid x)}{p(y)}$). Exact enumeration gives a bound of $0.009$ bits at $N = 2$, $0.025$ at $N = 8$ and $0.030$ at $N = 16$: it climbs toward $I(X;Y) = 0.037$ bits and never passes it, while the ceiling $\log_2 N$ is 1, 3 and 4 bits. Here the small mutual information limits the bound, not the batch; the $\log N$ ceiling bites only when $I$ is large, as for image–text pairs.
- Representation learning framings (information bottleneck): keep what predicts the label,
  discard the rest — compression as a theory of generalization.
  The **information bottleneck** (Tishby, Pereira and Bialek, 1999) makes that an objective over a stochastic encoder $p(z \mid x)$ that maps input $X$ to representation $Z$, given a target $Y$:
  $$\min_{p(z \mid x)} \; I(X;Z) - \beta\, I(Z;Y)$$
  The first term is the compression (how much of the input $Z$ keeps), the second the relevance (how much $Z$ tells about the label), and $\beta > 0$ sets the trade-off, so a large $\beta$ keeps more of the input for the sake of prediction. It is assumed that $Z$ depends on $Y$ only through $X$, i.e. $Y \to X \to Z$ form a Markov chain.

### 5. The ELBO, derived honestly

*Second pass: read it when a paper trains on an ELBO — a VAE, a diffusion model or a latent world model; the First pass stops at §3.*

Goal: maximize $\log p_\theta(x)$, intractable because of the **latent** $z$ — a variable the
model uses but never observes (the "code" behind an image, the compressed state behind a
sensor stream); to get $p(x)$ you would have to integrate over every value it could take,
$$p_\theta(x) = \int p_\theta(x \mid z)\,p(z)\,dz$$
where $p(z)$ is the prior over the latent and $p_\theta(x \mid z)$ the decoder with parameters $\theta$; this integral has no closed form once the decoder is a neural network, so it is intractable. The trick that
makes $q$ appear: multiply and divide the integrand by any distribution $q(z|x)$, which
turns the integral into an expectation over $q$ — then Jensen's inequality ($\log$ is
concave, so $\log E \ge E \log$) drops the log inside:

$$\log p_\theta(x) = \log E_{q}\!\left[\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \;\ge\; E_{q}\!\left[\log\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \quad\text{(Jensen)}$$

Now split that single log with $\log\frac{p(x|z)\,p(z)}{q} = \log p(x|z) + \log\frac{p(z)}{q}$
and take the expectation term by term — the first piece is the reconstruction term, the
second is *minus* a KL:

$$= \underbrace{E_{q}[\log p_\theta(x|z)]}_{\text{reconstruction}} \;+\; \underbrace{E_{q}\!\left[\log\frac{p(z)}{q(z|x)}\right]}_{-\,D_{KL}(q\,\|\,p(z))} \;=\; E_{q}[\log p_\theta(x|z)] - D_{KL}(q(z|x)\,\|\,p(z))$$

(the second expectation is $-E_q[\log\frac{q}{p(z)}]$, which is exactly $-D_{KL}(q\|p(z))$ by
its definition in §3.) The gap between the two sides is exactly $D_{KL}(q(z|x)\,\|\,p_\theta(z|x))$ — so maximizing
the ELBO simultaneously (1) raises the likelihood bound and (2) pulls $q$ toward the true
posterior. Many foundational VAE, diffusion, and latent world-model papers use this ELBO
or a closely related variational objective (though not all — flow matching and
non-variational world models take different routes).

**The definition in one place.** $\log p_\theta(x)$ is called the **evidence**. For any **variational distribution** $q(z \mid x)$ (a tractable distribution over the latent, usually a Gaussian whose mean and variance an encoder network outputs), the **evidence lower bound** is
$$\text{ELBO}(q, \theta) = E_{q(z|x)}\big[\log p_\theta(x, z) - \log q(z \mid x)\big], \qquad \log p_\theta(x) = \text{ELBO}(q, \theta) + D_{KL}\big(q(z|x)\,\|\,p_\theta(z|x)\big)$$
so it is a lower bound on the evidence for every $q$, since the KL on the right is $\ge 0$ (§3), and it is tight exactly when $q$ equals the true posterior. *Example with two latent values:* let $z \in \{0, 1\}$ with prior $(\tfrac12, \tfrac12)$, and let the observed $x$ have likelihood $0.8$ under $z = 0$ and $0.2$ under $z = 1$. Then the evidence is $\log p(x) = \ln 0.5 = -0.693$ nats and the true posterior is $(0.8, 0.2)$. A uniform $q = (\tfrac12, \tfrac12)$ gives $\text{ELBO} = \tfrac12\ln\tfrac{0.4}{0.5} + \tfrac12\ln\tfrac{0.1}{0.5} = -0.916$ nats, and the gap $0.223$ nats is exactly $D_{KL}\big(q\,\|\,(0.8, 0.2)\big)$. Setting $q$ to the posterior closes the gap, and the ELBO rises to $-0.693$. The same identity reached without Jensen, by Bayes' rule inside the logarithm, and its gap computed both ways for a Gaussian encoder ($0.154544$ nats), are in [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs §2]].

### 6. Quick reference table

| Quantity | Formula | Deep learning role |
|---|---|---|
| Entropy $H(p)$ | $-E_p[\log p]$ | uncertainty; exploration bonuses in RL |
| Cross-entropy $H(p,q)$ | $-E_p[\log q]$ | the classification/LM loss |
| KL $D_{KL}(p\|q)$ | $E_p[\log p/q]$ | VAE regularizer, RLHF penalty, distillation |
| Mutual info $I(X;Y)$ | $H(X)-H(X\mid Y)$ | contrastive learning (CLIP), info bottleneck |
| Perplexity | $2^{H(p,q)}$ in bits, $e^{H(p,q)}$ in nats | LM evaluation |
| ELBO | $E_q[\log p(x\mid z)] - D_{KL}(q\|p)$ | VAEs and variational diffusion/world-model formulations |

> [!tip] Going deeper · 더 깊이
> MacKay's [*Information Theory, Inference, and Learning Algorithms*](https://www.inference.org.uk/mackay/itila/) is free and unusually readable; Cover and Thomas's *Elements of Information Theory* is what you want when a theorem has to be stated precisely rather than explained.

### Self-check

1. Compute the entropy of a coin with $P(\text{H}) = 0.99$, and say why it is smaller than the 0.9 coin's.
2. A classifier assigns probability 0.25 to the correct class. What is this sample's cross-entropy loss in nats?
3. *(Second pass, §3 and §5.)* Which KL direction appears where in a VAE, and which one relates to blurry samples?
4. *(Second pass, §4.)* In CLIP's InfoNCE, how much can doubling the batch size improve the mutual-information bound?

> [!tip]- Answers
> 1. $H = -0.99\log_2 0.99 - 0.01\log_2 0.01 \approx 0.08$ bits — the more predictable, the smaller the average surprise.
> 2. $-\ln 0.25 = \ln 4 \approx 1.39$ nats.
> 3. Reverse KL, $KL(q(z|x)\|p(z|x))$, sits in the posterior fit: being mode-seeking, it tends to under-disperse $q$, which is a statement about the latent, not about blur. Blur comes from the data-level side: maximum likelihood minimises the *forward* $KL(p_{data}\|p_\theta)$, which is mass-covering, and a Gaussian pixel likelihood turns uncertainty into averaged pixels.
> 4. $I \ge \log N - \mathcal{L}$, so the bound's ceiling rises by $\log 2 \approx 0.69$ nats (= 1 bit).

### Problem set · 과제

Tier B. **P5** crack detector from [[02-foundations/lab-plants|0.6]]: $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$. Use bits ($\log_2$).

1. **Draw.** The picture above for an improved detector whose false-alarm rate falls from $0.05$ to $P(+|\neg c)=0.01$, with the same sensitivity $0.95$ and prior $P(c)=0.01$: the binary channel $C\in\{c,\neg c\}$ into $\{+,-\}$ with all four transitions, the four joint masses, and the bracket on $+$ with $P(+)$ and its two shares. Which of the two circled numbers moved, and by how much?
2. **Derive.** Keep item 1's improved detector. After an alarm the true posterior is Bernoulli($p$) with $p=P(c|+)$ from item 1. (a) $H(p)$. (b) The cross-entropy $H(p,q)$ of a model that still reports the sensitivity, $q=0.95$, as if it were $P(c|+)$. (c) $D_{KL}(p\,\|\,q)$ computed term by term from its definition in §3, and checked against $H(p,q)-H(p)$. (d) Set the three beside the catalog detector's $0.637$ and $3.64$ bits from §2 and their difference, $3.00$: which moved which way, and why?
3. **Interpret.** An alarm from the improved detector leaves almost a full bit of uncertainty, more than the catalog detector's $0.637$. Is the improved detector the worse one? Settle it with the conditional entropy of §1: find $P(-)$, $P(c|-)$, $H(X|Y{=}0)$ and $H(X|Y)$ for the improved detector, compare with the catalog's $0.044$ bits, and say which term of the average changed, and why.

> [!note]- How to draw it · 그리는 법
> - Two input nodes on the left, $c$ above $\neg c$, and two output nodes on the right, $+$ above $-$, joined by four arrows, every input to every output: none omitted, because the two diagonal arrows are the errors and they are the whole lesson.
> - Write the conditional $P(y|x)$ on each arrow and check that the two arrows leaving each left node sum to $1$. The two entering a right node need not: in the picture above they did only because that channel was symmetric, and this one is not — in a channel matrix with one column per input, a column is a distribution and a row need not be.
> - Draw the left nodes as boxes whose heights are their prior masses; drawn honestly, the $c$ box is a line, and that ratio must be visible before any arithmetic starts.
> - Multiply prior by conditional along each arrow and write the product where the arrow lands; write on the page the check that the four joint masses sum to $1$.
> - Bracket the two arrows that land on $+$, write their total $P(+)$ beside the bracket, and split it into the two shares: the posterior after an alarm, read off the picture rather than from Bayes' rule. The two masses in the bracket are now nearly equal, and that near-tie is the answer.
> - Circle the sensitivity $P(+|c)$ on its arrow and the posterior $P(c|+)$ at the bracket, and set each beside its value in the picture above: one of them did not move at all.

> [!tip]- Solutions
> 1. Arrows $c\to+$ at $0.95$, $c\to-$ at $0.05$, $\neg c\to+$ at $0.01$, $\neg c\to-$ at $0.99$. The two entering $+$ now sum to $0.96$, not $1$: the channel is no longer symmetric, and nothing required it to be. Joint masses $0.0095$, $0.0005$, $0.0099$, $0.9801$, summing to $1$. $P(+)=0.0194$, split into $0.490$ from cracked and $0.510$ from sound. The sensitivity is still $0.95$; the posterior $P(c|+)$ rose from $0.161$ to $0.490$, about three times, because false alarms, not misses, were what swamped the alarm. It is still below one half: at a $1\%$ prior, one false alarm per hundred sound panels produces as many alarms as the cracks do.
> 2. $P(+)=0.0095+0.0099=0.0194$ and $p=0.0095/0.0194=0.490$. (a) $H(p)=-0.490\log_2 0.490-0.510\log_2 0.510\approx1.000$ bits ($0.9997$ to four places), a hair under the $1$ bit of a fair coin. (b) $H(p,q)=-0.490\log_2 0.95-0.510\log_2 0.05=0.490(0.074)+0.510(4.322)\approx2.24$ bits. (c) $D_{KL}=0.490\log_2\tfrac{0.490}{0.95}+0.510\log_2\tfrac{0.510}{0.05}\approx-0.47+1.71=1.24$ bits, which matches $2.24-1.00$: the first term is negative and the second makes the total positive, as §3 said it must. (d) The floor $H(p)$ rose, $0.637\to1.000$, because the posterior moved from $0.161$ to $0.490$, next to a coin flip. The cross-entropy fell, $3.64\to2.24$, and the excess fell most, $3.00\to1.24$ bits, because $0.490$ is much closer than $0.161$ to the $0.95$ the confused model reports. With the better detector the same mistake is cheaper, but it still costs $1.24$ bits per alarm.
> 3. $P(-)=1-0.0194=0.9806$ and $P(c|-)=0.0005/0.9806=0.00051$, so $H(X|Y{=}0)=0.0063$ bits. Then $H(X|Y)=0.0194\times1.000+0.9806\times0.0063=0.0194+0.0062=0.026$ bits, against the catalog's $0.044$: on average the improved detector leaves less uncertainty, as a better sensor should. The silent term hardly moved ($0.0062$ in both); the alarm term fell from $0.059\times0.637=0.038$ to $0.019$. Each alarm now leaves more uncertainty, but alarms are three times rarer, because the false alarms that were $0.0495$ of the $0.059$ are now only $0.0099$ of $0.0194$. One reading's entropy can rise while the average falls — the boundary §1's non-example drew — so judge a sensor by the average over its readings, each weighted by how often it happens. (§4 names the drop $H(X)-H(X|Y)$ the mutual information: $0.081-0.026=0.055$ bits, $68\%$ of the uncertainty, against $0.037$ bits and $46\%$ for the catalog detector.)

## 한국어

*[[02-foundations/probability|3. 확률]]과 [[02-foundations/engineering-math|0.5]]의 로그 위에 선다. 둘째 응용 기둥이고, 목적함수들이 공통으로 재는 것에
이름을 붙인다 — 교차 엔트로피가 곧 최대우도이고 곧 KL이다.*

딥러닝에서 확률 분포가 등장하는 모든 것은 결국 정보이론의 언어로 말한다: 교차 엔트로피
손실, KL divergence, ELBO(evidence lower bound, 증거 하한 — §5에서 유도), 대조학습, 심지어 "perplexity"까지. 이 페이지는 최신 논문을
읽는 데 필요한 전부를 사전지식 없이 따라올 수 있게 담았다. 이 페이지가 계속 쓰는 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치(plant: 제어하거나 측정하는 대상 시스템) P5의 균열 감지기, 곧 균열의 95%와 정상 패널의 5%에서 울리고 패널의 1%만 균열인 감지기다.

> [!note] 왜 배우는가 · Why this matters
> 정보이론은 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 학습과 적응 층, 그리고 "*저 패널을 프레임에 설치해*"를 행동으로 바꾸는 언어 기반 스택 아래에 깔린 수학의 바닥이다. 이 페이지가 맡는 것은 첫 단계인 지시 해석이다. 교차 엔트로피(§2)는 모든 언어모델과, 행동을 토큰으로 내는 모든 정책의 손실이고, InfoNCE(§4)는 비전–언어 모델이 패널 사진마다 어떤 말이 어울리는지 배우는 방법이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 이것 없이는 실패를 읽을 수 없다. 조작자들이 비계 연결재를 왼쪽이나 오른쪽으로 $60$ mm 비켜 지나가는데, 그 명령에 최대우도로 — §3의 forward KL로 — 가우시안 하나를 맞추면 평균은 두 경로 사이, 곧 연결재 속으로 간다([[05-construction-robotics/imitating-contact|10. 접촉 모방 §4]]). KL 벌점이나 "손실이 0.7나트로 떨어졌다"는 문장도 §2–§3 없이는 아무 뜻이 없다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지는 블록 4의 작업 언어다. [[03-deep-learning/foundations/index|1. 학습 시스템 §1]]은 §2의 손실로, [[03-deep-learning/vlm/index|3. VLM §2]]는 §4의 하한으로 학습하고, [[03-deep-learning/vla/index|4. VLA §2]]는 토큰화한 행동을 §2로 학습하면서 §3이 설명하는 다봉성에 이름을 붙인다. 블록 7의 10. 접촉 모방 §4는 §3을 시연자 둘과 평균 하나로 옮겨 놓는다. 이 페이지를 마치면 엔트로피, 교차 엔트로피, KL을 비트나 나트로 손으로 계산하고, 어떤 손실이 어느 방향의 KL을 줄이며 그것이 맞춘 정책에 무슨 일을 하는지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 계산기를 옆에 두고 60–90분짜리 두 회차면 된다. **1회차, 엔트로피와 교차 엔트로피:** 그림, §0(로그 세 규칙, 5분), §1, §2. 비트 계산은 전부 손으로 해라. 그것이 이 페이지다. 스스로 점검 1–2로 마친다. **2회차, KL:** §3을 두 봉우리 혼합의 forward·reverse 적합과 그 그림까지 읽고 과제를 푼다. 두 번째 읽기: 논문이 목적함수에 상호 정보량이나 대조 손실을 넣을 때 §4를(InfoNCE 증명은 맨 나중에), ELBO를 넣을 때 §5를 읽고 스스로 점검 3–4를 함께 푼다. 접어 둔 부호 이야기는 나중에 펴도 되고, §6은 돌아와서 찾아보는 참조 표다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 324" style="max-width:100%;height:auto" role="img" aria-label="장치 P5 균열 감지기를 이진 채널로 그린 그림: 사전확률을 실제 비율로 그린 상자, 균열 0.01은 선 하나이고 멀쩡함 0.99는 긴 상자다. 조건부 확률과 결합 질량이 적힌 화살표 넷, P(+) = 0.059라고 적힌 묶음 안에서 균열 몫 0.161과 멀쩡함 몫 0.839로 나뉜 경보 노드, 동그라미 친 0.95와 0.161.">
  <defs><marker id="itHwk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="104" y="46" width="36" height="2" fill="currentColor" fill-opacity="0.85"/>
  <rect x="104" y="62" width="36" height="198" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.3"/>
  <text x="96" y="44" font-size="11" text-anchor="end" fill="currentColor">c  균열</text>
  <text x="96" y="58" font-size="11" text-anchor="end" fill="currentColor">P(c) = 0.01</text>
  <text x="96" y="157" font-size="11" text-anchor="end" fill="currentColor">¬c  멀쩡함</text>
  <text x="96" y="171" font-size="11" text-anchor="end" fill="currentColor">P(¬c) = 0.99</text>
  <text x="96" y="191" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">실제 비율: 99 : 1</text>
  <rect x="376" y="72" width="24" height="10.3" fill="currentColor" fill-opacity="0.55"/>
  <rect x="376" y="82.3" width="24" height="53.7" fill="currentColor" fill-opacity="0.12"/>
  <rect x="376" y="196" width="24" height="64" fill="currentColor" fill-opacity="0.07"/>
  <rect x="376" y="72" width="24" height="64" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <rect x="376" y="196" width="24" height="64" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="400" y="50" font-size="11" text-anchor="end" fill="currentColor">+  경보</text>
  <text x="400" y="276" font-size="11" text-anchor="end" fill="currentColor">−  침묵</text>
  <line x1="140" y1="47" x2="375" y2="77.2" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHwk)"/>
  <line x1="140" y1="116" x2="375" y2="109.2" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHwk)"/>
  <line x1="140" y1="47" x2="375" y2="208" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHwk)"/>
  <line x1="140" y1="220" x2="375" y2="242" stroke="currentColor" stroke-width="1.5" marker-end="url(#itHwk)"/>
  <circle cx="257.5" cy="42.1" r="15.8" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="257.5" y="46.1" font-size="11" text-anchor="middle" fill="currentColor">0.95</text>
  <text x="304.5" y="103.2" font-size="11" text-anchor="middle" fill="currentColor">0.05</text>
  <text x="300.9" y="148" font-size="11" fill="currentColor">0.05</text>
  <text x="257.5" y="247" font-size="11" text-anchor="middle" fill="currentColor">0.95</text>
  <text x="346" y="63.5" font-size="11" text-anchor="end" fill="currentColor">0.0095</text>
  <text x="364" y="126.2" font-size="11" text-anchor="end" fill="currentColor">0.0495</text>
  <text x="350" y="214" font-size="11" text-anchor="end" fill="currentColor">0.0005</text>
  <text x="364" y="259" font-size="11" text-anchor="end" fill="currentColor">0.9405</text>
  <circle cx="426" cy="77.2" r="18.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="426" y="81.2" font-size="11" text-anchor="middle" fill="currentColor">0.161</text>
  <text x="408" y="113.2" font-size="11" fill="currentColor">0.839</text>
  <path d="M 458 72 q 6 0 6 6 V 98 q 0 6 6 6 q -6 0 -6 6 V 130 q 0 6 -6 6" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="475" y="108" font-size="11" fill="currentColor">P(+) = 0.059</text>
  <text x="424" y="162" font-size="11" opacity="0.9" fill="currentColor">결합 질량:</text>
  <text x="424" y="176" font-size="11" opacity="0.9" fill="currentColor">0.0095 + 0.0005</text>
  <text x="424" y="190" font-size="11" opacity="0.9" fill="currentColor">+ 0.0495 + 0.9405</text>
  <text x="424" y="204" font-size="11" opacity="0.9" fill="currentColor">= 1 ✓</text>
  <text x="12" y="299" font-size="11" opacity="0.9" fill="currentColor">왼쪽 노드 하나에서 나가는 두 화살표의 합은 1이다(0.95 + 0.05). +로 들어오는 둘은 아니어도 된다.</text>
  <text x="12" y="313" font-size="11" opacity="0.9" fill="currentColor">동그라미: 화살표 위의 P(+|c) = 0.95와 묶음 안의 P(c|+) = 0.161, 약 여섯 배 차이다.</text>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 P5 균열 감지기를 이진 채널로 그린 것으로, 사전확률은 실제 비율대로 — 균열 $P(c)=0.01$은 선 하나, 멀쩡함 $P(\neg c)=0.99$는 기둥 전체 — 그렸고 화살표 넷에는 $P(+|c)=0.95$, $P(-|c)=0.05$, $P(+|\neg c)=0.05$, $P(-|\neg c)=0.95$가 실려 있다. 화살촉 자리의 결합 질량 $0.0095$, $0.0005$, $0.0495$, $0.9405$는 합이 $1$이고, $+$에 닿는 둘이 $P(+)=0.059$를 이루며 그 안은 균열 몫 $0.161$과 멀쩡함 몫 $0.839$로 나뉜다. 요점은 동그라미 친 두 숫자, 곧 화살표 위의 민감도 $P(+|c)=0.95$와 묶음 안의 사후확률 $P(c|+)=0.161$이 약 여섯 배 차이 난다는 것이고, 둘을 혼동한 대가로 §2는 바닥 $H(p)\approx 0.637$비트(참 사후분포의 엔트로피, §1)에 대해 $H(p,q)\approx 3.64$비트(교차 엔트로피, §2)를 청구한다.

### 0. 사전 준비: 로그의 세 규칙

이 페이지 전체가 로그로 굴러간다. 아래 세 줄이 자동으로 나오지 않으면
[[02-foundations/engineering-math|0.5 공업수학 §6]]을 먼저 읽어라 (5분이면 된다):
$\log(ab) = \log a + \log b$ (확률의 곱이 합이 된다 — 손실이 합인 이유);
$\log(a^n) = n \log a$; 그리고 밑 2와 밑 $e$는 단위(**비트** vs **나트**)만 상수배 바꾼다. 그 상수는 밑 변환 규칙 $\log_2 x = \ln x / \ln 2$에서 오며, 이 페이지의 모든 양은 다음처럼 환산된다.
$$H_{\text{비트}} = \frac{H_{\text{나트}}}{\ln 2}, \qquad 1\ \text{나트} = 1.443\ \text{비트}$$
모든 항이 로그이고 모든 로그가 같은 $1/\ln 2$로 스케일되기 때문이다. 머신러닝 논문은 보통 나트로 보고하고(PyTorch 손실은 $\ln$을 쓴다), 부호화·통신 논문은 비트를 쓴다.
하나 더: 확률은 $[0,1]$에 살므로 로그 확률은 $\le 0$이다 — "교차 엔트로피가 작다" =
로그 확률이 0에 가깝다는 뜻.

**P5에서 본 세 규칙.** 멀쩡한 패널은 확률 $P(-|\neg c)=0.95$로 조용하다([[02-foundations/lab-plants|0.6 Lab Plants]]). 멀쩡한 패널 $N$개를 하나씩 독립적으로 읽는 점검이 끝까지 조용할 확률은 $0.95^N$이고, 규칙 1과 2가 이 곱을 $N\ln 0.95$로 바꾼다. $N=100$이면 $0.95^{100}=0.0059$, $100\ln 0.95=-5.13$나트다. 규칙 3으로 옮기면 $-5.13\times1.443=-7.40$비트이고, 같은 규칙으로 사전확률 $P(c)=0.01$에서 패널에 균열이 있다는 사실을 알게 되는 놀라움을 매기면 $-\ln 0.01=4.61$나트, 곧 $6.64$비트다. 한 사실을 두 단위로 적은 것이다. 합으로 바꾸는 것은 편의가 아니다. 그대로 곱하면 $0.95^N$은 $N\approx1{,}700$에서 float32가 온전한 정밀도로 담는 가장 작은 수(약 $10^{-38}$) 아래로, $N\approx13{,}800$에서 float64의 그것(약 $10^{-308}$) 아래로 떨어진다(float가 담을 수 있는 수는 [[02-foundations/tools/python-research-code|12.3 Python §5]]). 그 뒤로 곱은 맞는 자릿수를 점점 잃다가 몇백 번의 측정 뒤에는 사라진다. 거듭제곱으로 계산하면 $N\approx14{,}500$에서 정확히 $0$으로 반올림되어 로그가 $-\infty$가 되고, 누적 곱으로 계산하면 측정이 아무리 더 들어와도 아주 작은 한 값에 멈춰 선다. 합 $20{,}000\ln 0.95=-1{,}026$나트는 평범한 수다. 이 위키의 모든 우도가 로그의 합으로 계산되는 이유이고, 분류기 손실 뒤의 softmax를 [[02-foundations/engineering-math|0.5 §6]]의 log-sum-exp 항등식으로 계산하는 이유다.

로그는 여러 관측에 대한 결합 확률을 더할 수 있는 점수로 바꾼다. 분류기가 대부분 프레임을 그럴듯하게 예측해도 일부 정답에 자신 있게 낮은 확률을 주면 큰 벌점을 받을 수 있다. **여기서 얻는 독법.** 로그 손실에서 어떤 사건에 확률을 주고 어떻게 집계하는지 묻는다. 손실 감소는 그 확률 배정에 관한 결과다. 과제 성공이 특정 정도로 개선된다는 뜻은 아니다. 보고된 두 손실을 비교하기 전에 밑과 정규화를 맞춘다. $0.693$나트는 1비트이고, 데이터셋 전체에 걸쳐 더한 로그우도는 규칙 1에 따라 표본마다 항이 하나씩 붙으므로 그 절댓값이 표본 수와 함께 커진다. 그래서 데이터셋 사이에서 비교되는 것은 표본당 또는 토큰당 평균뿐이다(§2가 토큰당 평균을 perplexity로 바꾼다).

### 1. 놀라움과 엔트로피

측정값은 미리 예측할 수 없었을 때만 무언가를 알려준다. 그래서 모든 학습 시스템에는 결과 하나가 얼마나 뜻밖이었는지 재는 수 하나와, 소스 전체가 얼마나 예측하기 어려운지 재는 수 하나가 필요하다. 이 절은 그 둘, 곧 놀라움과 그 평균인 엔트로피를 정의하고 균열 감지기에서 비트로 값을 매긴다.

- 사건의 **놀라움**: $-\log p(x)$. 드문 사건일수록 정보가 많다 (완벽히 예측한 센서 값은
  아무것도 알려주지 않는다).
  *자기 정보량* 또는 *Shannon 정보량*이라고도 하며, 결과 하나의 확률의 함수다:
  $$h(x) = -\log p(x) = \log\frac{1}{p(x)}$$
  $p(x)$는 모델이 결과 $x$에 주는 확률이다. 로그가 올바른 선택인 이유가 세 성질이다: $p(x) \le 1$이므로 $h(x) \ge 0$; $p(x) = 1$일 때만 $h(x) = 0$(확실한 결과는 아무것도 알려주지 않는다); 독립인 결과에서는 $p(x,y) = p(x)p(y)$이고 로그가 곱을 합으로 바꾸므로 *더해진다*, $h(x, y) = h(x) + h(y)$. *예:* 확률 $\tfrac18$인 결과는 $\log_2 8 = 3$비트를, 공정한 동전 둘에서 나온 앞면 둘은 $\log_2 4 = 2 = 1 + 1$비트를 담는다.
- **엔트로피** = 놀라움의 기댓값:
  $H(p) = -\sum_x p(x)\log p(x)$
  — 소스가 얼마나 예측 불가능한가를 비트(밑 2) 또는 나트(밑 e)로 잰 것.
  균등 분포 = 최대 엔트로피; 결정론적 = 0.
  식으로 쓰면, 가능한 값 $|\mathcal{X}|$개의 집합 $\mathcal{X}$ 위에서 PMF $p$를 갖는 이산 확률변수 $X$에 대해:
  $$H(X) = E_{x \sim p}[h(x)] = -\sum_{x \in \mathcal{X}} p(x)\log p(x), \qquad 0 \le H(X) \le \log|\mathcal{X}|$$
  불가능한 결과는 아무것도 보태지 않으므로 $0 \log 0 = 0$으로 약속한다. 모든 놀라움이 $\ge 0$이므로 하한이 성립하고, 등호는 한 결과의 확률이 1일 때뿐이다. 상한에는 균등 분포만 닿는다. *예:* 값 8개 위의 균등 분포는 $\log_2 8 = 3$비트로, 8값 소스가 가질 수 있는 최대다. 엔트로피는 값이 아니라 확률에만 의존한다: 결과의 이름을 바꾸거나 면이 $10, 20, \dots, 60$인 주사위를 써도 그대로다.
- **결합 엔트로피와 조건부 엔트로피는** 같은 평균을 결합 PMF $p(x,y)$를 갖는 두 변수 $X$, $Y$로 넓힌다. 결합 엔트로피는 쌍의 불확실성이다. 조건부 엔트로피는 $Y$를 안 뒤 $X$에 남은 불확실성을 $Y$의 값들에 대해 평균 낸 것이다:
  $$H(X,Y) = -\sum_{x,y} p(x,y)\log p(x,y), \qquad H(X \mid Y) = \sum_y p(y)\,H(X \mid Y{=}y) = -\sum_{x,y} p(x,y)\log p(x \mid y)$$
  $\log p(x,y) = \log p(y) + \log p(x \mid y)$이므로 둘은 **연쇄 법칙** $H(X,Y) = H(Y) + H(X \mid Y)$로 묶인다. 평균적으로 조건화는 불확실성을 늘리지 않는다: $H(X \mid Y) \le H(X)$이고, 등호는 $X$와 $Y$가 독립일 때만이다(§4가 그 차이를 상호 정보량으로 만든다).
  - *예*(그림의 균열 감지기, $X$ = 균열, $Y$ = 경보): $H(X) = 0.081$비트. 경보가 울리면 $P(\text{균열}) = 0.161$이므로 $H(X \mid Y{=}1) = 0.637$비트이고, 조용하면 균열 확률이 $0.0005/0.941 = 0.00053$이므로 $H(X \mid Y{=}0) = 0.0065$비트다. 각 경우가 일어나는 빈도로 가중하면 $H(X \mid Y) = 0.059 \times 0.637 + 0.941 \times 0.0065 = 0.044$비트다.
  - *반례, 독자가 놓치는 경계:* 부등식은 평균에 대한 것일 뿐이다. 경보가 울린 뒤의 불확실성 $0.637$비트는 이전의 $0.081$보다 훨씬 *크다*. 관측 하나가 불확실성을 키울 수 있다. 94%의 경우에 일어나는 조용한 쪽의 $0.0065$비트가 이를 상쇄한다.
- **기대 부호 길이.** **부호** $C$는 각 결과 $x$에 길이 $\ell(x)$비트인 이진 부호어를 배정한다. 평균 비용은
  $$L(C, X) = \sum_x p(x)\,\ell(x)$$
  이므로 자주 나오는 결과에 짧은 부호어를 줘야 한다. *예:* $p = (0.7, 0.2, 0.1)$의 허프만 부호는 길이가 $(1, 2, 2)$이고 $L = 0.7 + 0.4 + 0.2 = 1.3$비트로, §2에서 쓰는 값이다.
- 직관의 닻: 엔트로피는 결과 하나를 알아내는 데 필요한 예/아니오 질문 평균 개수의 **하한**이다.
  그 소스의 *압축 한계*이고, 어떤 부호도 이보다 잘하지 못하며, 심볼 단위 부호는 보통 여기에
  닿지도 못한다. 허프만 부호의 $1.3$비트는 이 소스의 $1.157$비트(§2)보다 위에 있다.

> [!note]- 더 깊이 · Deeper
> **이 하한이 덮는 부호.** 부호어를 어떻게 이어 붙여도 한 가지로만 다시 쪼갤 수 있으면 부호가 *유일 복호 가능*하고, *접두 부호*(어떤 부호어도 다른 부호어의 앞부분이 아님; 트리로 만드는 법은 [[02-foundations/algorithms/greedy-mst|11.4 §5]])는 읽는 즉시 복호할 수 있는 흔한 종류다. 유일 복호 가능한 모든 부호는 $L(C,X) \ge H(X)$이고, 등호는 모든 부호 길이가 자기 Shannon 정보량 — 위에서 정의한 놀라움 $\log_2(1/p(x))$, 비트 단위 — 과 같을 때만 성립한다(MacKay 식 5.17). MacKay의 정리 5.1은 $L(C,X) < H(X)+1$을 만족하는 접두 부호가 *존재함*을 보장한다.

- **숫자로 한 번** — $P(\text{앞}) = 0.9$인 동전:
  $H = -0.9\log_2 0.9 - 0.1\log_2 0.1 = 0.9(0.152) + 0.1(3.322) \approx 0.47$ 비트 — 공정 동전(1비트)의 절반 이하다.
  결과가 대부분 예측 가능하기 때문. 이 동전과 공정 동전 사이의 KL:
  $D_{KL} = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5} \approx 0.763 - 0.232 = 0.53$ 비트 —
  편향 동전을 공정 동전용 부호로 인코딩할 때 토스당 내는 *추가* 비용이다.
  이 두 계산을 손으로 한 번 해 보라 — 이 페이지의 모든 공식이 구체화된다.
- **미분 엔트로피는** $X$가 PMF가 아니라 밀도 $p(x)$를 가질 때 쓰는 연속 변수 판본이다([[02-foundations/probability|3. 확률 §3]]이 가우시안에 대해 인용하는 양):
  $$h(X) = -\int p(x)\log p(x)\,dx$$
  식은 같지만 의미는 전부 따라오지 않는다. 밀도는 1을 넘을 수 있으므로 $h$는 음수가 될 수 있고, $X$를 $a$배 하면 $\log|a|$가 더해지므로 단위를 바꾸면 값이 바뀐다. 그래서 비트 개수가 아니며, 미분 엔트로피의 *차이*(상호 정보량과 KL처럼)만 의미를 유지한다. 글자에 주의하라. 밀도를 가진 확률변수의 이 $h(X)$는 이 절 첫머리에서 정의한 결과 하나의 놀라움 $h(x)$가 아니다. 두 관례가 같은 글자를 쓰므로(MacKay는 놀라움을 $h(x)$로, Cover·Thomas는 미분 엔트로피를 $h(X)$로 쓴다) 괄호 안을 읽어라. 결과 하나면 놀라움, 연속 확률변수면 미분 엔트로피다.
  - *예:* $[0, a]$ 위의 균등 분포는 $h = \log a$이므로 $[0, 0.5]$ 위의 균등 분포는 $h = -1$비트다. 분산 $\sigma^2$인 가우시안은 $h = \tfrac12\log(2\pi e\sigma^2)$이고 $\sigma = 1$이면 $2.047$비트로, 그 분산을 갖는 밀도 중 최대다.

### 2. 교차 엔트로피 — 이미 쓰고 있는 그 손실함수

분류기나 언어모델을 학습시킨다는 것은 예측한 분포를 실제로 일어난 일에 대어 채점하는 것이고, 그 채점에 거의 모두가 쓰는 것이 교차 엔트로피다. 이 절은 교차 엔트로피를 정의하고, 세 심볼 예제와 균열 감지기에서 비트로 값을 매긴 뒤, 그것이 최대우도 손실임을 보인다.

- $H(p, q) = -\sum_x p(x)\log q(x)$: 진짜 분포가 $p$인 데이터를, 내 모델 $q$에 최적화된
  부호로 인코딩할 때의 비용.
  같은 결과들 위의 **두** 분포, 참(또는 데이터) 분포 $p$와 모델 $q$의 함수다:
  $$H(p, q) = E_{x \sim p}\big[-\log q(x)\big] = -\sum_x p(x)\log q(x)$$
  즉 *진실에서* 뽑힌 결과들에 대해 평균 낸, *모델이 잰* 놀라움이다. 정의적 성질: $H(p,q) \ge H(p)$이고 등호는 $q = p$일 때만이며(§3이 증명한다), $p$와 $q$에 대해 대칭이 아니다. 학습에서 $p$는 라벨 달린 예제 $N$개의 경험 분포이므로, 손실은 각 정답 라벨 $y_i$에 대한 모델의 놀라움의 평균 $-\frac1N\sum_{i=1}^N \log q(y_i \mid x_i)$다. *쓸 수 없는 모델의 반례:* $p(x) > 0$인 결과에 $q(x) = 0$을 주면 교차 엔트로피가 무한대다. 분류기가 정확히 0을 주지 않는 소프트맥스([[02-foundations/engineering-math|0.5 §10]])를 출력하는 이유다.
- **비트 단위 계산 예제.** 참분포 $p = (0.7,\,0.2,\,0.1)$, 모델 $q = (0.5,\,0.3,\,0.2)$.
  $$H(p) = -[0.7\log_2 0.7 + 0.2\log_2 0.2 + 0.1\log_2 0.1] = 1.157\ \text{비트}$$
  $$H(p,q) = -[0.7\log_2 0.5 + 0.2\log_2 0.3 + 0.1\log_2 0.2] = 1.280\ \text{비트}$$
  바닥이 $1.157$인 자리에 모델이 심볼당 $1.280$비트를 치른다 — $0.123$비트를 더 낸 것이다. 이 숫자를 기억해 두라. 3절에서 이것이 정확히 KL임을 보인다.

<svg viewBox="0 0 560 150" style="max-width:100%;height:auto" role="img" aria-label="심볼당 비트 수를 나타내는 두 막대: 엔트로피 바닥 1.157비트와 모델의 부호가 치르는 1.280비트, 그 초과분 0.123비트가 KL">
  <g fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2">
    <rect x="156" y="30" width="231.4" height="26" rx="3"/>
    <rect x="156" y="72" width="231.4" height="26" rx="3"/>
  </g>
  <rect x="387.4" y="72" width="24.6" height="26" rx="2" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2"/>
  <line x1="387.4" y1="22" x2="387.4" y2="108" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity="0.5"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.55"><line x1="156" y1="118" x2="416" y2="118"/><line x1="156" y1="114" x2="156" y2="122"/><line x1="356" y1="114" x2="356" y2="122"/></g>
  <g font-size="11" fill="currentColor">
    <text x="16" y="47">H(p) = 1.157 비트</text>
    <text x="16" y="89">H(p, q) = 1.280 비트</text>
    <text x="422.0" y="89">KL = 0.123</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="156" y="134" text-anchor="middle">0</text>
    <text x="356" y="134" text-anchor="middle">1 비트</text>
    <text x="395.4" y="134">바닥: 이보다 짧은 부호는 없다</text>
  </g>
</svg>

$p=(0.7,\,0.2,\,0.1)$의 심볼당 비트 수다. 어떤 부호도 넘지 못하는 엔트로피 바닥 $H(p)=1.157$비트와, 모델 $q=(0.5,\,0.3,\,0.2)$에 맞춘 부호가 치르는 $1.280$비트다. 짙은 초과분 $0.123$비트가 §3의 KL이므로 교차 엔트로피를 줄이는 것이 곧 KL을 줄이는 것이다. 바닥은 데이터가 정하고, 학습의 진전은 전부 저 짙은 띠가 좁아지는 것이다.

- **계산: P5 균열 감지기.** 카탈로그의 $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$([[02-foundations/lab-plants|0.6]]). $P(+)=0.059$, $P(c|+)\approx 0.161$. 참 사후분포는 Bernoulli($0.161$)이고 $H(p)\approx 0.64$비트다. *민감도* $0.95$를 $P(c|+)$인 양 쓰는 모델은 $H(p,q)\approx 3.64$비트를 치른다. 균열이 없는 $99\%$ 질량에서 나온 거짓 경보($0.0495$)가 참양성($0.0095$)을 압도한다. 민감도는 $P(+|c)$이지 $P(c|+)$가 아니다. 맨 위의 그림이 이 채널을 그린 것이다.
- 분류 학습: $p$ = 원-핫 라벨, $q$ = 소프트맥스 출력 ⇒ 교차 엔트로피 손실
  $= -\log q(\text{정답 클래스})$. 나머지 항은 전부 $p(x) = 0$이 곱해져 사라진다 — 코드에서
  보는 손실이 로그 *하나*인 이유가 이것이다. 모델이 정답 클래스에 확률 $0.5$를 주면 손실은
  $-\log 0.5 = 0.693$ 나트($=1$비트), $0.9$면 $0.105$, $0.99$면 $0.010$이다. 손실이 처음엔
  가파르게 떨어지다 이후 거의 움직이지 않는다 — 학습 신호의 대부분은 모델이 아직 틀리는
  예제에서 온다. **교차 엔트로피 최소화 = MLE**
  ([[02-foundations/probability|3. 확률 §4]] 참고).
- 언어모델: 토큰별 교차 엔트로피가 사전학습 목적함수 *그 자체*다
  ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]); **perplexity**는 $H$가 비트면 $2^{H(p,q)}$, nat이면 $e^{H(p,q)}$다 — "모델이
  perplexity개의 선택지 사이에서 고민하는 것만큼 헷갈려 한다."
  토큰 $N$개 $w_1, \dots, w_N$의 테스트 텍스트에서, $q(w_i \mid w_{<i})$를 모델이 실제 다음 토큰에 준 확률이라 하면 토큰당 평균 교차 엔트로피의 지수다:
  $$\text{PPL} = \exp\Big(-\frac1N \sum_{i=1}^N \ln q(w_i \mid w_{<i})\Big)$$
  $K$개 토큰에 확률을 고르게 퍼뜨린 모델은 교차 엔트로피가 $\ln K$라서 $\text{PPL} = K$이므로, "실질적인 선택지 수"라는 해석은 균등 추측에서 정확하다. *예:* 위 계산 예제의 모델 $q$는 $1.280$비트를 치르므로 perplexity가 $2^{1.280} = 2.43$개 선택지이고, 참분포는 $2^{1.157} = 2.23$이다. 토크나이저나 테스트 세트를 바꾸면 $N$과 결과가 바뀌므로, perplexity는 같은 토크나이저와 테스트 세트에서만 비교할 수 있다.

> [!note]- 더 깊이 · Deeper
> **부호, 블록, 엔트로피율.** 위의 엔트로피와 교차 엔트로피는 기대 비용이지 부호 길이가 아니다. 엔트로피가 묶는 것은 *기대* 길이이고, 심볼 단위 부호가 그 바닥에 닿는 것은 모든 확률이 2의 거듭제곱일 때뿐인데, 한 심볼의 부호 길이가 정수 비트여야 하기 때문이다. $p = (0.7, 0.2, 0.1)$에서 최선의 심볼 부호는 바닥 $1.157$에 대해 $1.3$비트인 허프만이다(만드는 법과 최적성 증명은 [[02-foundations/algorithms/greedy-mst|11.4 §5]]). 바닥에 다가가는 길은 **i.i.d.**([[02-foundations/probability|3. 확률 §2]]) 심볼의 긴 블록을 부호화하는 것이며, 그것이 섀넌의 원천 부호화 정리다. $N$개의 i.i.d. 변수는 $N\to\infty$에서 약 $NH(X)$비트로 압축된다. 이 전제가 언어모델에서 중요하다. 언어 토큰은 서로 강하게 의존하므로 그쪽의 바닥은 단일 심볼 엔트로피가 아니라 엔트로피 *율*이다. 수열 $X_1, X_2, \dots$의 **엔트로피율은** 의존성을 전부 반영한 뒤의 심볼당 불확실성이다:
> $$H_{\text{rate}} = \lim_{n\to\infty} \frac1n H(X_1, \dots, X_n)$$
> 독립인 심볼들의 결합 엔트로피는 각 엔트로피의 합이므로, i.i.d. 심볼이면 $H(X_1)$과 같다. *반례:* 직전 심볼을 확률 0.9로 반복하는 이진 수열은 두 심볼에 시간을 반씩 쓰므로 단일 심볼 엔트로피는 1비트지만, 각 심볼이 대부분 직전 심볼로 예측되므로 엔트로피율은 $H(0.9, 0.1) = 0.469$비트뿐이다.

### 3. KL divergence — 거리 같지만 거리가 아닌 것

교차 엔트로피에는 두 가지가 섞여 있다. 어떤 모델도 없앨 수 없는 데이터 자체의 불확실성, 그리고 모델 자신의 어긋남이다. KL divergence는 뒤의 것만 따로 잰 것 — §2의 $1.280$비트가 바닥 $1.157$비트를 넘는 부분 — 이고, VAE, RLHF 벌점, 증류가 줄이는 양이 이것이다.

- $D_{KL}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$
  — 진실이 $p$인데 $q$를 썼을 때 *추가로* 내는 비트.
  **쿨백–라이블러 발산은** 같은 결과들 위의 분포 순서쌍의 함수다: 기준 $p$(첫째 자리, 평균을 내는 쪽)와 근사 $q$(둘째 자리).
  $$D_{KL}(p\,\|\,q) = E_{x\sim p}\Big[\log\frac{p(x)}{q(x)}\Big], \qquad D_{KL}(p\,\|\,q) = \int p(x)\log\frac{p(x)}{q(x)}\,dx \ \text{(밀도)}$$
  $p(x) > 0 = q(x)$인 항은 $+\infty$이므로 $p(x) > 0$인 곳마다 $q(x) > 0$이어야만 유한하고, $p(x) = 0$인 항은 0을 보탠다. 거리가 아니라 *발산*이다: 거리 공리 넷 중 비음수성과 "같을 때만 0"(아래에서 증명)은 지키지만 **대칭성과** **삼각 부등식을** 어긴다.
- **2절과 같은 숫자를, 이번엔 직접 계산** — $p = (0.7, 0.2, 0.1)$과 $q = (0.5, 0.3, 0.2)$를 합의 각 항에 대입하면:
  $$D_{KL} = 0.7\log_2\tfrac{0.7}{0.5} + 0.2\log_2\tfrac{0.2}{0.3} + 0.1\log_2\tfrac{0.1}{0.2} = 0.340 - 0.117 - 0.100 = 0.123\ \text{비트}$$
  — 정확히 $H(p,q) - H(p) = 1.280 - 1.157$이다. 두 가지가 눈에 보인다: 개별 항은 **음수가 될
  수 있지만**(가운데 항이 그렇다) 총합은 결코 음수가 되지 않으며, 총합이 0이 되는 것은 모든
  곳에서 $q = p$일 때뿐이다.
  - *대칭성의 반례:* 자리를 바꾸면 $D_{KL}(q\,\|\,p) = 0.133$비트로, $0.123$이 아니다.
  - *삼각 부등식의 반례:* 앞면 확률이 $0.1$, $0.5$, $0.9$인 동전에서 곧장 가는 비용 $D_{KL}(0.1\,\|\,0.9) = 2.536$비트가 돌아가는 비용 $D_{KL}(0.1\,\|\,0.5) + D_{KL}(0.5\,\|\,0.9) = 0.531 + 0.737 = 1.268$비트보다 크다.

- **옌센 부등식은** 함수 $f$와 확률변수 $X$에 대한 명제다. $f$가 오목하면(현 위에 놓임, [[02-foundations/optimization|4. 최적화 §2]]의 볼록성 조건의 반대)
  $$E[f(X)] \le f\big(E[X]\big)$$
  이고, 볼록 $f$면 부등호가 뒤집힌다. 등호는 $X$가 상수일 때 성립하며, ($\log$ 같은) 순오목 $f$면 그때뿐이다. 이유: 오목한 그래프의 현은 그래프 아래에 있으므로, 값 $f(x)$들의 가중 평균은 점들의 가중 평균에서의 $f$ 값 아래에 놓인다. *예:* $X$가 같은 확률로 $1$ 또는 $4$이고 $f = \log_2$. 그러면 $E[\log_2 X] = \tfrac{0 + 2}{2} = 1$이고 $\log_2 E[X] = \log_2 2.5 = 1.32$다.
- **비음수성, 두 줄 증명** (옌센 부등식 — $\log$는 오목이므로 로그의 기댓값이 기댓값의 로그를 넘지 못한다):
  $$-D_{KL}(p\|q) = E_p\Big[\log\frac{q}{p}\Big] \le \log E_p\Big[\frac{q}{p}\Big] = \log \sum_{x:\,p(x)>0} q(x) \le \log 1 = 0$$
  등호는 $p = q$일 때만. 이 작은 증명이 ELBO의 유효성과 학습 이론의 절반을 떠받친다.
- **가우시안 KL의 닫힌 형태** (모든 VAE 구현 속의 그 공식):
  $\mathcal{N}(\mu_1,\sigma_1^2)$ vs $\mathcal{N}(\mu_2,\sigma_2^2)$에 대해:
  $$D_{KL} = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac12$$
  표준 정규 사전($\mu_2=0, \sigma_2=1$)에 대한 이 식이 [[01-canonical-papers/notes/6-diffusion/vae|VAE]]
  손실에 코딩되는 정규화 항 그 자체다.
  외우지 말고 세 항을 읽어라. $\log(\sigma_2/\sigma_1)$은 *폭*이 틀린 값을 청구하고, 분수는
  퍼짐과 평균이 어긋난 값을 청구한다 — 둘 다 **목표 분포의** 분산을 단위로 재는데, $\sigma_2$가
  분모에 앉는 이유이고 이 벌점이 비대칭인 이유다 — 그리고 $-\tfrac12$은 두 분포가 일치할 때
  전체가 0이 되게 만드는 상수다. $\sigma_1 = \sigma_2$, $\mu_1 = \mu_2$를 넣어 보면 첫 항이
  $0$, 분수가 $\tfrac12$, 합이 $0$이다. 그래야만 하는 대로.
  *숫자로, 나트(자연로그) 단위:* $D_{KL}\big(\mathcal{N}(1,1)\,\|\,\mathcal{N}(0,1)\big) = 0 + \tfrac{1 + 1}{2} - \tfrac12 = 0.5$. 폭을 바꾸면 $D_{KL}\big(\mathcal{N}(0,2^2)\,\|\,\mathcal{N}(0,1)\big) = 0.807$이지만 $D_{KL}\big(\mathcal{N}(0,1)\,\|\,\mathcal{N}(0,2^2)\big) = 0.318$이다: 첫째 자리 분포가 둘째보다 두 배 넓을 때가 절반 폭일 때보다 비싸다. 이 공식을 첫째 자리 분포 아래에서 로그 비의 기댓값으로 항별 유도한 것이 [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN §2]]다.
- 중요한 성질: $\ge 0$, $p = q$일 때만 0, 그리고 **비대칭** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$가 참, $q$를 적합): 모드 **커버링** — $q$가 $p$의 질량 전체를 덮으려 퍼진다.
  - Reverse KL(*변분 추론*에서 사용 — 계산 불가능한 분포를, 다루기 쉬운 분포 가족 중
    가장 가까운 것으로 근사하는 방법): 모드 **시킹** — $q$가 한 모드에 들러붙는다.
  - 둘은 단순한 분포 가족 $\mathcal{Q}$ 위의 서로 다른 최적화 문제다:
  $$q_{\text{fwd}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(p\,\|\,q), \qquad q_{\text{rev}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(q\,\|\,p)$$
    두 행동은 무한대 벌점이 어디 앉는지에서 나온다. Forward KL은 $p$에 대해 평균 내므로 $p$에 질량이 있는 곳에서 $q \approx 0$이면 벌하고, reverse KL은 $q$에 대해 평균 내므로 $p \approx 0$인 곳에 $q$가 질량을 두면 벌한다. *예:* 두 봉우리 혼합 $p = \tfrac12\mathcal{N}(-2, 0.5^2) + \tfrac12\mathcal{N}(2, 0.5^2)$에 가우시안 하나를 맞춘다. Forward KL은 혼합의 평균 $0$과 분산 $0.5^2 + 2^2 = 4.25$를 그대로 맞춘 $\mathcal{N}(0, 2.06^2)$을 준다. 가우시안 $q$에서 $D_{KL}(p\,\|\,q)$ 가운데 $q$에 따라 달라지는 부분은 $-E_p[\log q]$뿐이고 이 항은 $p$를 평균과 분산으로만 보므로, 최선의 $q$는 그 둘을 그대로 베낀다. 그 봉우리는 $p$의 질량이 거의 없는 곳에 있다(KL $0.72$나트). Reverse KL은 봉우리 하나에 정확히 맞춘 $\mathcal{N}(2, 0.5^2)$(또는 $-2$의 거울상)을 주고 KL은 $0.69$나트다. 각 답은 다른 기준으로 재면 나쁘다: 넓은 적합은 reverse KL로 $2.10$나트, 봉우리 하나짜리 적합은 forward KL로 $15.3$나트다.
  이 비대칭은 VAE의 제한적 사후분포 커버리지와 RL식 목적함수가 좁은 행동으로 붕괴하는
  현상에 기여한다 — 단 고전적 VAE 흐릿함의 *주원인*은 가우시안 픽셀 우도의 평균화다
  (아래 스스로 점검 정답 참고).

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="두 봉우리 혼합 p에 가우시안 하나를 맞춘 두 결과: forward KL은 N(0, 2.06²)로 두 봉우리를 덮고 봉우리를 p가 거의 없는 가운데에 두며(0.72나트), reverse KL은 N(2, 0.5²)로 한 봉우리에 붙는다(0.69나트)">
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55"><line x1="40" y1="222" x2="520" y2="222"/><line x1="40" y1="222" x2="40" y2="44"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45"><line x1="88" y1="222" x2="88" y2="226"/><line x1="184" y1="222" x2="184" y2="226"/><line x1="280" y1="222" x2="280" y2="226"/><line x1="376" y1="222" x2="376" y2="226"/><line x1="472" y1="222" x2="472" y2="226"/><line x1="36" y1="182" x2="40" y2="182"/><line x1="36" y1="142" x2="40" y2="142"/><line x1="36" y1="102" x2="40" y2="102"/><line x1="36" y1="62" x2="40" y2="62"/></g>
  <path d="M40 222 L41.2 222 L42.4 222 L43.6 222 L44.8 222 L46 222 L47.2 222 L48.4 222 L49.6 222 L50.8 222 L52 222 L53.2 222 L54.4 222 L55.6 222 L56.8 222 L58 222 L59.2 222 L60.4 222 L61.6 222 L62.8 222 L64 222 L65.2 222 L66.4 222 L67.6 222 L68.8 222 L70 222 L71.2 222 L72.4 222 L73.6 222 L74.8 222 L76 222 L77.2 222 L78.4 222 L79.6 222 L80.8 222 L82 222 L83.2 222 L84.4 222 L85.6 222 L86.8 222 L88 222 L89.2 222 L90.4 222 L91.6 222 L92.8 221.9 L94 221.9 L95.2 221.9 L96.4 221.9 L97.6 221.9 L98.8 221.9 L100 221.8 L101.2 221.8 L102.4 221.8 L103.6 221.7 L104.8 221.7 L106 221.6 L107.2 221.5 L108.4 221.4 L109.6 221.3 L110.8 221.2 L112 221.1 L113.2 221 L114.4 220.8 L115.6 220.6 L116.8 220.4 L118 220.2 L119.2 219.9 L120.4 219.6 L121.6 219.3 L122.8 218.9 L124 218.5 L125.2 218 L126.4 217.5 L127.6 217 L128.8 216.3 L130 215.7 L131.2 214.9 L132.4 214.1 L133.6 213.2 L134.8 212.2 L136 211.2 L137.2 210.1 L138.4 208.9 L139.6 207.6 L140.8 206.2 L142 204.7 L143.2 203.2 L144.4 201.5 L145.6 199.8 L146.8 198 L148 196.1 L149.2 194.1 L150.4 192.1 L151.6 189.9 L152.8 187.7 L154 185.5 L155.2 183.2 L156.4 180.8 L157.6 178.4 L158.8 176 L160 173.6 L161.2 171.2 L162.4 168.8 L163.6 166.4 L164.8 164.1 L166 161.8 L167.2 159.5 L168.4 157.4 L169.6 155.4 L170.8 153.4 L172 151.6 L173.2 149.9 L174.4 148.3 L175.6 147 L176.8 145.7 L178 144.7 L179.2 143.8 L180.4 143.1 L181.6 142.6 L182.8 142.3 L184 142.2 L185.2 142.3 L186.4 142.6 L187.6 143.1 L188.8 143.8 L190 144.7 L191.2 145.7 L192.4 147 L193.6 148.3 L194.8 149.9 L196 151.6 L197.2 153.4 L198.4 155.4 L199.6 157.4 L200.8 159.5 L202 161.8 L203.2 164.1 L204.4 166.4 L205.6 168.8 L206.8 171.2 L208 173.6 L209.2 176 L210.4 178.4 L211.6 180.8 L212.8 183.2 L214 185.5 L215.2 187.7 L216.4 189.9 L217.6 192.1 L218.8 194.1 L220 196.1 L221.2 198 L222.4 199.8 L223.6 201.5 L224.8 203.2 L226 204.7 L227.2 206.2 L228.4 207.6 L229.6 208.9 L230.8 210.1 L232 211.2 L233.2 212.2 L234.4 213.2 L235.6 214.1 L236.8 214.9 L238 215.7 L239.2 216.3 L240.4 217 L241.6 217.5 L242.8 218 L244 218.5 L245.2 218.9 L246.4 219.3 L247.6 219.6 L248.8 219.9 L250 220.2 L251.2 220.4 L252.4 220.6 L253.6 220.8 L254.8 221 L256 221.1 L257.2 221.2 L258.4 221.3 L259.6 221.4 L260.8 221.5 L262 221.6 L263.2 221.7 L264.4 221.7 L265.6 221.8 L266.8 221.8 L268 221.8 L269.2 221.8 L270.4 221.9 L271.6 221.9 L272.8 221.9 L274 221.9 L275.2 221.9 L276.4 221.9 L277.6 221.9 L278.8 221.9 L280 221.9 L281.2 221.9 L282.4 221.9 L283.6 221.9 L284.8 221.9 L286 221.9 L287.2 221.9 L288.4 221.9 L289.6 221.9 L290.8 221.8 L292 221.8 L293.2 221.8 L294.4 221.8 L295.6 221.7 L296.8 221.7 L298 221.6 L299.2 221.5 L300.4 221.4 L301.6 221.3 L302.8 221.2 L304 221.1 L305.2 221 L306.4 220.8 L307.6 220.6 L308.8 220.4 L310 220.2 L311.2 219.9 L312.4 219.6 L313.6 219.3 L314.8 218.9 L316 218.5 L317.2 218 L318.4 217.5 L319.6 217 L320.8 216.3 L322 215.7 L323.2 214.9 L324.4 214.1 L325.6 213.2 L326.8 212.2 L328 211.2 L329.2 210.1 L330.4 208.9 L331.6 207.6 L332.8 206.2 L334 204.7 L335.2 203.2 L336.4 201.5 L337.6 199.8 L338.8 198 L340 196.1 L341.2 194.1 L342.4 192.1 L343.6 189.9 L344.8 187.7 L346 185.5 L347.2 183.2 L348.4 180.8 L349.6 178.4 L350.8 176 L352 173.6 L353.2 171.2 L354.4 168.8 L355.6 166.4 L356.8 164.1 L358 161.8 L359.2 159.5 L360.4 157.4 L361.6 155.4 L362.8 153.4 L364 151.6 L365.2 149.9 L366.4 148.3 L367.6 147 L368.8 145.7 L370 144.7 L371.2 143.8 L372.4 143.1 L373.6 142.6 L374.8 142.3 L376 142.2 L377.2 142.3 L378.4 142.6 L379.6 143.1 L380.8 143.8 L382 144.7 L383.2 145.7 L384.4 147 L385.6 148.3 L386.8 149.9 L388 151.6 L389.2 153.4 L390.4 155.4 L391.6 157.4 L392.8 159.5 L394 161.8 L395.2 164.1 L396.4 166.4 L397.6 168.8 L398.8 171.2 L400 173.6 L401.2 176 L402.4 178.4 L403.6 180.8 L404.8 183.2 L406 185.5 L407.2 187.7 L408.4 189.9 L409.6 192.1 L410.8 194.1 L412 196.1 L413.2 198 L414.4 199.8 L415.6 201.5 L416.8 203.2 L418 204.7 L419.2 206.2 L420.4 207.6 L421.6 208.9 L422.8 210.1 L424 211.2 L425.2 212.2 L426.4 213.2 L427.6 214.1 L428.8 214.9 L430 215.7 L431.2 216.3 L432.4 217 L433.6 217.5 L434.8 218 L436 218.5 L437.2 218.9 L438.4 219.3 L439.6 219.6 L440.8 219.9 L442 220.2 L443.2 220.4 L444.4 220.6 L445.6 220.8 L446.8 221 L448 221.1 L449.2 221.2 L450.4 221.3 L451.6 221.4 L452.8 221.5 L454 221.6 L455.2 221.7 L456.4 221.7 L457.6 221.8 L458.8 221.8 L460 221.8 L461.2 221.9 L462.4 221.9 L463.6 221.9 L464.8 221.9 L466 221.9 L467.2 221.9 L468.4 222 L469.6 222 L470.8 222 L472 222 L473.2 222 L474.4 222 L475.6 222 L476.8 222 L478 222 L479.2 222 L480.4 222 L481.6 222 L482.8 222 L484 222 L485.2 222 L486.4 222 L487.6 222 L488.8 222 L490 222 L491.2 222 L492.4 222 L493.6 222 L494.8 222 L496 222 L497.2 222 L498.4 222 L499.6 222 L500.8 222 L502 222 L503.2 222 L504.4 222 L505.6 222 L506.8 222 L508 222 L509.2 222 L510.4 222 L511.6 222 L512.8 222 L514 222 L515.2 222 L516.4 222 L517.6 222 L518.8 222 L520 222" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="2.4"/>
  <path d="M40 220 L41.2 219.9 L42.4 219.8 L43.6 219.8 L44.8 219.7 L46 219.6 L47.2 219.6 L48.4 219.5 L49.6 219.4 L50.8 219.4 L52 219.3 L53.2 219.2 L54.4 219.1 L55.6 219 L56.8 219 L58 218.9 L59.2 218.8 L60.4 218.7 L61.6 218.6 L62.8 218.5 L64 218.4 L65.2 218.3 L66.4 218.2 L67.6 218.1 L68.8 218 L70 217.9 L71.2 217.8 L72.4 217.7 L73.6 217.6 L74.8 217.5 L76 217.4 L77.2 217.3 L78.4 217.1 L79.6 217 L80.8 216.9 L82 216.8 L83.2 216.6 L84.4 216.5 L85.6 216.4 L86.8 216.2 L88 216.1 L89.2 216 L90.4 215.8 L91.6 215.7 L92.8 215.5 L94 215.4 L95.2 215.2 L96.4 215.1 L97.6 214.9 L98.8 214.8 L100 214.6 L101.2 214.4 L102.4 214.3 L103.6 214.1 L104.8 213.9 L106 213.8 L107.2 213.6 L108.4 213.4 L109.6 213.2 L110.8 213 L112 212.8 L113.2 212.7 L114.4 212.5 L115.6 212.3 L116.8 212.1 L118 211.9 L119.2 211.7 L120.4 211.5 L121.6 211.3 L122.8 211 L124 210.8 L125.2 210.6 L126.4 210.4 L127.6 210.2 L128.8 210 L130 209.7 L131.2 209.5 L132.4 209.3 L133.6 209 L134.8 208.8 L136 208.6 L137.2 208.3 L138.4 208.1 L139.6 207.9 L140.8 207.6 L142 207.4 L143.2 207.1 L144.4 206.9 L145.6 206.6 L146.8 206.4 L148 206.1 L149.2 205.8 L150.4 205.6 L151.6 205.3 L152.8 205.1 L154 204.8 L155.2 204.5 L156.4 204.3 L157.6 204 L158.8 203.7 L160 203.4 L161.2 203.2 L162.4 202.9 L163.6 202.6 L164.8 202.3 L166 202.1 L167.2 201.8 L168.4 201.5 L169.6 201.2 L170.8 200.9 L172 200.7 L173.2 200.4 L174.4 200.1 L175.6 199.8 L176.8 199.5 L178 199.2 L179.2 199 L180.4 198.7 L181.6 198.4 L182.8 198.1 L184 197.8 L185.2 197.5 L186.4 197.3 L187.6 197 L188.8 196.7 L190 196.4 L191.2 196.1 L192.4 195.8 L193.6 195.6 L194.8 195.3 L196 195 L197.2 194.7 L198.4 194.5 L199.6 194.2 L200.8 193.9 L202 193.6 L203.2 193.4 L204.4 193.1 L205.6 192.8 L206.8 192.6 L208 192.3 L209.2 192 L210.4 191.8 L211.6 191.5 L212.8 191.3 L214 191 L215.2 190.8 L216.4 190.5 L217.6 190.3 L218.8 190 L220 189.8 L221.2 189.6 L222.4 189.3 L223.6 189.1 L224.8 188.9 L226 188.7 L227.2 188.4 L228.4 188.2 L229.6 188 L230.8 187.8 L232 187.6 L233.2 187.4 L234.4 187.2 L235.6 187 L236.8 186.8 L238 186.6 L239.2 186.5 L240.4 186.3 L241.6 186.1 L242.8 185.9 L244 185.8 L245.2 185.6 L246.4 185.5 L247.6 185.3 L248.8 185.2 L250 185 L251.2 184.9 L252.4 184.8 L253.6 184.7 L254.8 184.5 L256 184.4 L257.2 184.3 L258.4 184.2 L259.6 184.1 L260.8 184 L262 183.9 L263.2 183.9 L264.4 183.8 L265.6 183.7 L266.8 183.6 L268 183.6 L269.2 183.5 L270.4 183.5 L271.6 183.4 L272.8 183.4 L274 183.4 L275.2 183.3 L276.4 183.3 L277.6 183.3 L278.8 183.3 L280 183.3 L281.2 183.3 L282.4 183.3 L283.6 183.3 L284.8 183.3 L286 183.4 L287.2 183.4 L288.4 183.4 L289.6 183.5 L290.8 183.5 L292 183.6 L293.2 183.6 L294.4 183.7 L295.6 183.8 L296.8 183.9 L298 183.9 L299.2 184 L300.4 184.1 L301.6 184.2 L302.8 184.3 L304 184.4 L305.2 184.5 L306.4 184.7 L307.6 184.8 L308.8 184.9 L310 185 L311.2 185.2 L312.4 185.3 L313.6 185.5 L314.8 185.6 L316 185.8 L317.2 185.9 L318.4 186.1 L319.6 186.3 L320.8 186.5 L322 186.6 L323.2 186.8 L324.4 187 L325.6 187.2 L326.8 187.4 L328 187.6 L329.2 187.8 L330.4 188 L331.6 188.2 L332.8 188.4 L334 188.7 L335.2 188.9 L336.4 189.1 L337.6 189.3 L338.8 189.6 L340 189.8 L341.2 190 L342.4 190.3 L343.6 190.5 L344.8 190.8 L346 191 L347.2 191.3 L348.4 191.5 L349.6 191.8 L350.8 192 L352 192.3 L353.2 192.6 L354.4 192.8 L355.6 193.1 L356.8 193.4 L358 193.6 L359.2 193.9 L360.4 194.2 L361.6 194.5 L362.8 194.7 L364 195 L365.2 195.3 L366.4 195.6 L367.6 195.8 L368.8 196.1 L370 196.4 L371.2 196.7 L372.4 197 L373.6 197.3 L374.8 197.5 L376 197.8 L377.2 198.1 L378.4 198.4 L379.6 198.7 L380.8 199 L382 199.2 L383.2 199.5 L384.4 199.8 L385.6 200.1 L386.8 200.4 L388 200.7 L389.2 200.9 L390.4 201.2 L391.6 201.5 L392.8 201.8 L394 202.1 L395.2 202.3 L396.4 202.6 L397.6 202.9 L398.8 203.2 L400 203.4 L401.2 203.7 L402.4 204 L403.6 204.3 L404.8 204.5 L406 204.8 L407.2 205.1 L408.4 205.3 L409.6 205.6 L410.8 205.8 L412 206.1 L413.2 206.4 L414.4 206.6 L415.6 206.9 L416.8 207.1 L418 207.4 L419.2 207.6 L420.4 207.9 L421.6 208.1 L422.8 208.3 L424 208.6 L425.2 208.8 L426.4 209 L427.6 209.3 L428.8 209.5 L430 209.7 L431.2 210 L432.4 210.2 L433.6 210.4 L434.8 210.6 L436 210.8 L437.2 211 L438.4 211.3 L439.6 211.5 L440.8 211.7 L442 211.9 L443.2 212.1 L444.4 212.3 L445.6 212.5 L446.8 212.7 L448 212.8 L449.2 213 L450.4 213.2 L451.6 213.4 L452.8 213.6 L454 213.8 L455.2 213.9 L456.4 214.1 L457.6 214.3 L458.8 214.4 L460 214.6 L461.2 214.8 L462.4 214.9 L463.6 215.1 L464.8 215.2 L466 215.4 L467.2 215.5 L468.4 215.7 L469.6 215.8 L470.8 216 L472 216.1 L473.2 216.2 L474.4 216.4 L475.6 216.5 L476.8 216.6 L478 216.8 L479.2 216.9 L480.4 217 L481.6 217.1 L482.8 217.3 L484 217.4 L485.2 217.5 L486.4 217.6 L487.6 217.7 L488.8 217.8 L490 217.9 L491.2 218 L492.4 218.1 L493.6 218.2 L494.8 218.3 L496 218.4 L497.2 218.5 L498.4 218.6 L499.6 218.7 L500.8 218.8 L502 218.9 L503.2 219 L504.4 219 L505.6 219.1 L506.8 219.2 L508 219.3 L509.2 219.4 L510.4 219.4 L511.6 219.5 L512.8 219.6 L514 219.6 L515.2 219.7 L516.4 219.8 L517.6 219.8 L518.8 219.9 L520 220" fill="none" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.8" stroke-dasharray="7 4"/>
  <path d="M40 222 L41.2 222 L42.4 222 L43.6 222 L44.8 222 L46 222 L47.2 222 L48.4 222 L49.6 222 L50.8 222 L52 222 L53.2 222 L54.4 222 L55.6 222 L56.8 222 L58 222 L59.2 222 L60.4 222 L61.6 222 L62.8 222 L64 222 L65.2 222 L66.4 222 L67.6 222 L68.8 222 L70 222 L71.2 222 L72.4 222 L73.6 222 L74.8 222 L76 222 L77.2 222 L78.4 222 L79.6 222 L80.8 222 L82 222 L83.2 222 L84.4 222 L85.6 222 L86.8 222 L88 222 L89.2 222 L90.4 222 L91.6 222 L92.8 222 L94 222 L95.2 222 L96.4 222 L97.6 222 L98.8 222 L100 222 L101.2 222 L102.4 222 L103.6 222 L104.8 222 L106 222 L107.2 222 L108.4 222 L109.6 222 L110.8 222 L112 222 L113.2 222 L114.4 222 L115.6 222 L116.8 222 L118 222 L119.2 222 L120.4 222 L121.6 222 L122.8 222 L124 222 L125.2 222 L126.4 222 L127.6 222 L128.8 222 L130 222 L131.2 222 L132.4 222 L133.6 222 L134.8 222 L136 222 L137.2 222 L138.4 222 L139.6 222 L140.8 222 L142 222 L143.2 222 L144.4 222 L145.6 222 L146.8 222 L148 222 L149.2 222 L150.4 222 L151.6 222 L152.8 222 L154 222 L155.2 222 L156.4 222 L157.6 222 L158.8 222 L160 222 L161.2 222 L162.4 222 L163.6 222 L164.8 222 L166 222 L167.2 222 L168.4 222 L169.6 222 L170.8 222 L172 222 L173.2 222 L174.4 222 L175.6 222 L176.8 222 L178 222 L179.2 222 L180.4 222 L181.6 222 L182.8 222 L184 222 L185.2 222 L186.4 222 L187.6 222 L188.8 222 L190 222 L191.2 222 L192.4 222 L193.6 222 L194.8 222 L196 222 L197.2 222 L198.4 222 L199.6 222 L200.8 222 L202 222 L203.2 222 L204.4 222 L205.6 222 L206.8 222 L208 222 L209.2 222 L210.4 222 L211.6 222 L212.8 222 L214 222 L215.2 222 L216.4 222 L217.6 222 L218.8 222 L220 222 L221.2 222 L222.4 222 L223.6 222 L224.8 222 L226 222 L227.2 222 L228.4 222 L229.6 222 L230.8 222 L232 222 L233.2 222 L234.4 222 L235.6 222 L236.8 222 L238 222 L239.2 222 L240.4 222 L241.6 222 L242.8 222 L244 222 L245.2 222 L246.4 222 L247.6 222 L248.8 222 L250 222 L251.2 222 L252.4 222 L253.6 222 L254.8 222 L256 222 L257.2 222 L258.4 222 L259.6 222 L260.8 222 L262 222 L263.2 222 L264.4 222 L265.6 222 L266.8 222 L268 222 L269.2 222 L270.4 222 L271.6 222 L272.8 222 L274 222 L275.2 222 L276.4 222 L277.6 222 L278.8 222 L280 221.9 L281.2 221.9 L282.4 221.9 L283.6 221.9 L284.8 221.9 L286 221.9 L287.2 221.8 L288.4 221.8 L289.6 221.8 L290.8 221.7 L292 221.7 L293.2 221.6 L294.4 221.5 L295.6 221.4 L296.8 221.3 L298 221.2 L299.2 221 L300.4 220.9 L301.6 220.7 L302.8 220.5 L304 220.2 L305.2 219.9 L306.4 219.6 L307.6 219.3 L308.8 218.8 L310 218.4 L311.2 217.8 L312.4 217.2 L313.6 216.6 L314.8 215.8 L316 215 L317.2 214.1 L318.4 213 L319.6 211.9 L320.8 210.7 L322 209.3 L323.2 207.8 L324.4 206.2 L325.6 204.4 L326.8 202.5 L328 200.4 L329.2 198.2 L330.4 195.8 L331.6 193.2 L332.8 190.4 L334 187.5 L335.2 184.4 L336.4 181.1 L337.6 177.6 L338.8 174 L340 170.2 L341.2 166.2 L342.4 162.1 L343.6 157.8 L344.8 153.5 L346 148.9 L347.2 144.3 L348.4 139.6 L349.6 134.9 L350.8 130 L352 125.2 L353.2 120.4 L354.4 115.6 L355.6 110.8 L356.8 106.1 L358 101.5 L359.2 97.1 L360.4 92.8 L361.6 88.7 L362.8 84.8 L364 81.2 L365.2 77.8 L366.4 74.7 L367.6 71.9 L368.8 69.4 L370 67.3 L371.2 65.6 L372.4 64.2 L373.6 63.2 L374.8 62.6 L376 62.4 L377.2 62.6 L378.4 63.2 L379.6 64.2 L380.8 65.6 L382 67.3 L383.2 69.4 L384.4 71.9 L385.6 74.7 L386.8 77.8 L388 81.2 L389.2 84.8 L390.4 88.7 L391.6 92.8 L392.8 97.1 L394 101.5 L395.2 106.1 L396.4 110.8 L397.6 115.6 L398.8 120.4 L400 125.2 L401.2 130 L402.4 134.9 L403.6 139.6 L404.8 144.3 L406 148.9 L407.2 153.5 L408.4 157.8 L409.6 162.1 L410.8 166.2 L412 170.2 L413.2 174 L414.4 177.6 L415.6 181.1 L416.8 184.4 L418 187.5 L419.2 190.4 L420.4 193.2 L421.6 195.8 L422.8 198.2 L424 200.4 L425.2 202.5 L426.4 204.4 L427.6 206.2 L428.8 207.8 L430 209.3 L431.2 210.7 L432.4 211.9 L433.6 213 L434.8 214.1 L436 215 L437.2 215.8 L438.4 216.6 L439.6 217.2 L440.8 217.8 L442 218.4 L443.2 218.8 L444.4 219.3 L445.6 219.6 L446.8 219.9 L448 220.2 L449.2 220.5 L450.4 220.7 L451.6 220.9 L452.8 221 L454 221.2 L455.2 221.3 L456.4 221.4 L457.6 221.5 L458.8 221.6 L460 221.7 L461.2 221.7 L462.4 221.8 L463.6 221.8 L464.8 221.8 L466 221.9 L467.2 221.9 L468.4 221.9 L469.6 221.9 L470.8 221.9 L472 221.9 L473.2 222 L474.4 222 L475.6 222 L476.8 222 L478 222 L479.2 222 L480.4 222 L481.6 222 L482.8 222 L484 222 L485.2 222 L486.4 222 L487.6 222 L488.8 222 L490 222 L491.2 222 L492.4 222 L493.6 222 L494.8 222 L496 222 L497.2 222 L498.4 222 L499.6 222 L500.8 222 L502 222 L503.2 222 L504.4 222 L505.6 222 L506.8 222 L508 222 L509.2 222 L510.4 222 L511.6 222 L512.8 222 L514 222 L515.2 222 L516.4 222 L517.6 222 L518.8 222 L520 222" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="2 3"/>
  <line x1="280" y1="179.3" x2="280" y2="167.3" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <g font-size="10.5" fill="currentColor" opacity="0.8">
    <text x="88" y="238" text-anchor="middle">−4</text>
    <text x="184" y="238" text-anchor="middle">−2</text>
    <text x="280" y="238" text-anchor="middle">0</text>
    <text x="376" y="238" text-anchor="middle">2</text>
    <text x="472" y="238" text-anchor="middle">4</text>
    <text x="32" y="186" text-anchor="end">0.2</text>
    <text x="32" y="146" text-anchor="end">0.4</text>
    <text x="32" y="106" text-anchor="end">0.6</text>
    <text x="32" y="66" text-anchor="end">0.8</text>
    <text x="520" y="238" text-anchor="end">x</text>
  </g>
  <text x="12" y="30" font-size="11" fill="currentColor" opacity="0.85">밀도</text>
  <text x="280" y="163.3" font-size="10.5" fill="currentColor" text-anchor="middle" opacity="0.85">p ≈ 0인 곳에 봉우리</text>
  <line x1="52" y1="58" x2="76" y2="58" stroke="currentColor" stroke-width="2.4" stroke-opacity="1.0"/>
  <text x="82" y="62" font-size="11" fill="currentColor">p = ½N(−2, 0.5²) + ½N(2, 0.5²)</text>
  <line x1="52" y1="80" x2="76" y2="80" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.8" stroke-dasharray="7 4"/>
  <text x="82" y="84" font-size="11" fill="currentColor">forward KL(p‖q) 적합 N(0, 2.06²): 0.72나트</text>
  <text x="82" y="98" font-size="10.5" fill="currentColor" opacity="0.8">reverse KL(q‖p)로 재면 2.10</text>
  <line x1="52" y1="116" x2="76" y2="116" stroke="currentColor" stroke-width="2.2" stroke-opacity="1.0" stroke-dasharray="2 3"/>
  <text x="82" y="120" font-size="11" fill="currentColor">reverse KL(q‖p) 적합 N(2, 0.5²): 0.69나트</text>
  <text x="82" y="134" font-size="10.5" fill="currentColor" opacity="0.8">forward KL(p‖q)로 재면 15.3</text>
</svg>

두 봉우리 혼합 $p=\tfrac12\mathcal N(-2,\,0.5^2)+\tfrac12\mathcal N(2,\,0.5^2)$에 가우시안 하나를 두 방향으로 맞춘 것이다. Forward KL은 $p$에 대해 평균하므로 두 봉우리를 모두 덮어야 해서 $\mathcal N(0,\,2.06^2)$을 주고, 그 봉우리는 $p\approx0$인 곳에 선다($0.72$나트). Reverse KL은 $q$에 대해 평균하므로 봉우리 하나를 무시해도 되어 한쪽에 붙은 $\mathcal N(2,\,0.5^2)$을 주고 $0.69$나트다. 각 적합은 다른 기준으로 재면 나쁘다: 넓은 적합은 $2.10$나트, 봉우리 하나짜리 적합은 $15.3$나트다.

- 이미 만난 곳들:
  - [[01-canonical-papers/notes/6-diffusion/vae|VAE]]: ELBO의 정규화 항 $D_{KL}(q_\phi(z|x)\,\|\,p(z))$
  - [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]]: 정책을 SFT 모델 근처에 붙잡는
    토큰별 KL 페널티 — 말 그대로 "기준에서 너무 많은 비트만큼 벗어나지 마라".
  - [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]: 변분 하한이 가우시안 사이 KL 항들의 합이다
    (그래서 MSE로 접힌다).
  - 지식 증류: 학생이 교사의 소프트 라벨에 대한 KL을 최소화.

### 4. 상호 정보량

*두 번째 읽기: 논문이 목적함수에 상호 정보량이나 대조 손실을 넣을 때 읽는다. 처음에는 §3에서 멈춘다.*

경보는 균열에 대해, 사진은 그 설명문에 대해 얼마나 알려주는가? 상호 정보량은 비트로 답한다. 한 변수를 알고 나서 다른 변수에 대한 불확실성이 얼마나 줄었는가이고, 상관이 놓치는 의존성까지 본다.

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — $Y$를 알면 $X$에 대해 몇 비트를 알게 되는가; 독립일 때만 0.
  **상호 정보량은** 결합 분포 $p(x,y)$와 주변 분포 $p(x)$, $p(y)$를 갖는 확률변수 쌍에 붙는 수다. 동치인 세 형태가 있고 각각 다르게 읽힌다:
  $$I(X;Y) = \sum_{x,y} p(x,y)\log\frac{p(x,y)}{p(x)\,p(y)} = H(X) - H(X \mid Y) = H(X) + H(Y) - H(X,Y)$$
  첫째는 결합 분포가 독립 곱 $p(x)p(y)$에서 얼마나 먼지(KL, §3), 둘째는 $Y$를 알면 $X$에 대한 불확실성이 얼마나 줄어드는지(§1), 셋째는 두 엔트로피가 얼마나 겹치는지다. 둘째는 첫째에서 대입 한 번으로 나온다: $p(x,y) = p(y)\,p(x \mid y)$이므로 $\log\frac{p(x,y)}{p(x)p(y)} = \log\frac{p(x \mid y)}{p(x)} = -\log p(x) + \log p(x \mid y)$이고, $p(x,y)$로 평균하면 §1의 정의에 따라 두 항이 $H(X)$와 $-H(X \mid Y)$가 된다. 셋째는 다시 §1의 연쇄 법칙 $H(X \mid Y) = H(X,Y) - H(Y)$에서 나온다. 성질: **대칭**, $I(X;Y) = I(Y;X)$; KL이므로 **비음수**; 결합이 곱과 같을 때만이므로 **$X$와 $Y$가 독립일 때만 0**; 그리고 $I(X;Y) \le \min\big(H(X), H(Y)\big)$로 유계.
- **[[02-foundations/probability|3. 확률 §1]]의 균열 감지기로 계산해 보면.**
  $X$ = 균열 있음($P = 0.01$), $Y$ = 경보 울림, $P(Y{=}1|X{=}1) = 0.95$,
  $P(Y{=}1|X{=}0) = 0.05$. 그러면 $P(Y{=}1) = 0.95(0.01) + 0.05(0.99) = 0.059$이고, 네 개의
  결합 항을 계산하면 $I(X;Y) = 0.037$비트, 한편 $H(X) = 0.081$비트다. 즉 경보는 균열 유무에
  대한 불확실성 중 **46퍼센트**를 없앤다 — 정보가 있긴 하지만 "안다"와는 거리가 멀다. 이 비 하나가
  "우리 센서는 95% 정확도로 균열을 감지한다"는 문장의 정직한 판본이다: 희귀 사건에 대한 높은
  민감도는 여전히 질문의 대부분을 열어둔 채로 남기고, 베이즈 정리가 $P(X|Y) = 0.16$으로 보여준
  것과 같은 사실이다.
- **반례: 상관 0은 정보 0이 아니다.** $X$가 $\{-1, 0, 1\}$ 위에서 균등하고 $Y = X^2$이면 공분산은 0이다([[02-foundations/probability|3. 확률 §2]]). 그런데 $X$가 $Y$를 완전히 정하므로 $I(X;Y) = H(Y) - H(Y \mid X) = H(\tfrac13, \tfrac23) - 0 = 0.918$비트다. 상호 정보량은 선형이든 아니든 모든 의존성을 보므로, 표현 학습 논문이 상관 대신 이것을 쓴다.
- **InfoNCE / 대조학습** ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 목적함수)은 뷰/모달리티 간
  상호 정보량의 하한이다 — "이미지 임베딩이 텍스트 임베딩에 대해 알려주는 양을 최대화하라."
  유사도 $s(\cdot,\cdot)$와 온도 $\tau$, $N$쌍 배치에 대해 써보면:
  $$\mathcal{L} = -\frac1N\sum_i \log\frac{e^{s(x_i,y_i)/\tau}}{\sum_j e^{s(x_i,y_j)/\tau}}$$
  — "클래스"가 배치 안의 다른 샘플들인 교차 엔트로피다; $I(X;Y) \ge \log N - \mathcal{L}$을
  만족하므로 배치가 클수록 더 빡빡한 하한이 가능하다 (CLIP은 배치 32,768을 썼지만, 논문은 그 이유로 정보이론을 들지 않는다).
  단서: 이 하한은 음성이 주변분포 $p(y)$에서 독립으로 뽑혔을 때만 보장되고(아래 증명이 정확히 그것을 쓴다),
  얼마나 빡빡한지는 점수 함수와 $N$에 달려 있다 — 그 수는 $I$의 추정이 아니라 $I$ 아래의 바닥으로 읽어라.
  식에서 $x_i$와 $y_i$는 $i$번째 쌍의 두 뷰이므로 $j = i$ 항이 양성이고 $j \ne i$인 항은 모두 음성이다. $\mathcal{L} \ge 0$이므로 하한은 $\log N$보다 많은 것을 결코 보증하지 못하며, CLIP의 배치에서는 $\ln 32{,}768 = 10.4$나트(15비트)다.
- **InfoNCE 하한이 성립하는 이유.** 하한은 Oord, Li, Vinyals(2018, 대조 예측 부호화)에서 나왔고 Poole 등(ICML 2019)이 엄밀히 증명했다. 아래 세 단계는 그 다중 표본 논증을 §1–§3만으로 압축한 것이다. 앵커 $x$ 하나를 고정하고 그 점수를 $f(x,y) = s(x,y)/\tau$로 쓴다. 배치의 그 행에는 양성 $y_1 \sim p(y \mid x)$와 음성 $N - 1$개 $y_2, \dots, y_N \sim p(y)$가 모두 독립으로 들어 있고, $\mathcal{L}$은 기대 손실 $E\big[-\log\big(e^{f(x,y_1)}/\sum_j e^{f(x,y_j)}\big)\big]$이다. *1단계, 음성은 아무것도 더하지 않는다:* $Y_{2:N}$은 $(X, Y_1)$과 독립이므로 §1의 연쇄 법칙으로 $I(X;Y_1) = I(X;Y_{1:N})$이다. *2단계, 정규화된 어떤 추측도 하한을 준다:* 어떤 조건부 분포 $q(y_{1:N} \mid x)$에 대해서도 $I(X;Y_{1:N}) \ge E\big[\log\big(q(y_{1:N} \mid x)/p(y_{1:N})\big)\big]$이다. 그 차이가 $D_{KL}\big(p(y_{1:N} \mid x)\,\|\,q(y_{1:N} \mid x)\big) \ge 0$(§3)의 평균이기 때문이다. *3단계, 소프트맥스가 바로 그런 추측이다:*
  $$q(y_{1:N} \mid x) = p(y_1)\cdots p(y_N)\cdot\frac{N\,e^{f(x,y_1)}}{\sum_{j=1}^{N} e^{f(x,y_j)}}$$
  는 합이 1이다. $p(y_1)\cdots p(y_N)$ 아래에서 $N$개 자리는 서로 바꿔도 같으므로 소프트맥스 가중치 $N$개가 각각 평균 $1/N$이 되고, 인자 $N$이 합을 1로 되돌린다. $p(y_{1:N}) = p(y_1)\cdots p(y_N)$에 대한 로그 비는 $\log N + \log\big(e^{f(x,y_1)}/\sum_j e^{f(x,y_j)}\big)$이므로, 2단계가 $I(X;Y) \ge \log N - \mathcal{L}$을 준다. 이 하한은 어떤 점수 함수에서도 성립한다. 나쁜 점수는 하한을 느슨하게 할 뿐이고, 상수 점수는 정확히 $\log N - \log N = 0$을 준다.
  - *균열 감지기로 계산* (앵커 $X$, 후보는 경보 측정값 $Y$, 최선의 점수 $f = \log\frac{p(y \mid x)}{p(y)}$). 정확히 열거하면 하한은 $N = 2$에서 $0.009$비트, $N = 8$에서 $0.025$비트, $N = 16$에서 $0.030$비트다. $I(X;Y) = 0.037$비트를 향해 올라가지만 결코 넘지 않고, 천장 $\log_2 N$은 1, 3, 4비트다. 여기서 하한을 막는 것은 배치가 아니라 작은 상호 정보량이다. $\log N$ 천장은 이미지–텍스트 쌍처럼 $I$가 클 때만 문제가 된다.
- 표현 학습의 틀(information bottleneck): 라벨을 예측하는 것만 남기고 버려라 —
  압축을 일반화의 이론으로 보는 관점.
  **정보 병목**(Tishby, Pereira, Bialek, 1999)은 이것을, 목표 $Y$가 주어졌을 때 입력 $X$를 표현 $Z$로 보내는 확률적 인코더 $p(z \mid x)$ 위의 목적함수로 만든다:
  $$\min_{p(z \mid x)} \; I(X;Z) - \beta\, I(Z;Y)$$
  첫 항은 압축($Z$가 입력을 얼마나 간직하는가), 둘째 항은 관련성($Z$가 라벨에 대해 얼마나 알려주는가)이고 $\beta > 0$이 둘을 저울질하므로, $\beta$가 크면 예측을 위해 입력을 더 많이 간직한다. $Z$는 $X$를 통해서만 $Y$에 의존한다고, 즉 $Y \to X \to Z$가 마르코프 체인을 이룬다고 가정한다.

### 5. ELBO, 정직하게 유도하기

*두 번째 읽기: 논문이 ELBO로 학습할 때 — VAE, 디퓨전 모델, 잠재 월드모델 — 읽는다. 처음에는 §3에서 멈춘다.*

목표: $\log p_\theta(x)$ 최대화 — **잠재변수(latent)** $z$ 때문에 계산 불가. 잠재변수란
모델이 쓰지만 관측되지는 않는 변수다(이미지 뒤의 "코드", 센서 스트림 뒤의 압축된 상태).
$p(x)$를 얻으려면 $z$가 가질 수 있는 모든 값에 대해 적분해야 한다.
$$p_\theta(x) = \int p_\theta(x \mid z)\,p(z)\,dz$$
$p(z)$는 잠재변수의 사전분포, $p_\theta(x \mid z)$는 파라미터 $\theta$를 가진 디코더다. 디코더가 신경망이면 이 적분에 닫힌 형태가 없으므로 계산 불가능하다. $q$가 등장하는 트릭:
적분 안을 아무 분포 $q(z|x)$로 곱하고 나눠 $q$에 대한 기댓값으로 바꾼 뒤, 옌센
부등식($\log$은 오목이므로 $\log E \ge E \log$)으로 로그를 안으로 떨어뜨린다:

$$\log p_\theta(x) = \log E_{q}\!\left[\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \;\ge\; E_{q}\!\left[\log\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \quad\text{(옌센)}$$

이제 그 로그 하나를 $\log\frac{p(x|z)\,p(z)}{q} = \log p(x|z) + \log\frac{p(z)}{q}$로 쪼개고
항별로 기댓값을 취하면 — 첫 조각은 재구성 항, 둘째는 *마이너스* KL이다:

$$= \underbrace{E_{q}[\log p_\theta(x|z)]}_{\text{재구성}} \;+\; \underbrace{E_{q}\!\left[\log\frac{p(z)}{q(z|x)}\right]}_{-\,D_{KL}(q\,\|\,p(z))} \;=\; E_{q}[\log p_\theta(x|z)] - D_{KL}(q(z|x)\,\|\,p(z))$$

(둘째 기댓값은 $-E_q[\log\frac{q}{p(z)}]$이고, §3의 정의에 의해 정확히 $-D_{KL}(q\|p(z))$다.)
양변의 간극이 정확히 $D_{KL}(q(z|x)\,\|\,p_\theta(z|x))$다 — 그래서 ELBO 최대화는 동시에
(1) 우도 하한을 올리고 (2) $q$를 진짜 사후분포로 끌어당긴다. 기초적인 VAE·디퓨전·잠재
월드모델 논문 다수가 이 ELBO 또는 밀접한 변분 목적함수를 쓴다 (전부는 아니다 — flow
matching이나 비변분 월드모델은 다른 길을 간다).

**정의를 한곳에.** $\log p_\theta(x)$를 **증거**(evidence)라 부른다. 어떤 **변분 분포** $q(z \mid x)$(잠재변수 위의 다루기 쉬운 분포로, 보통 인코더 신경망이 평균과 분산을 출력하는 가우시안)에 대해서든 **증거 하한은**
$$\text{ELBO}(q, \theta) = E_{q(z|x)}\big[\log p_\theta(x, z) - \log q(z \mid x)\big], \qquad \log p_\theta(x) = \text{ELBO}(q, \theta) + D_{KL}\big(q(z|x)\,\|\,p_\theta(z|x)\big)$$
이다. 오른쪽 KL이 $\ge 0$(§3)이므로 모든 $q$에서 증거의 하한이고, $q$가 참 사후분포와 같을 때 정확히 빡빡해진다. *잠재값 두 개짜리 예:* $z \in \{0, 1\}$, 사전 $(\tfrac12, \tfrac12)$, 관측된 $x$의 우도가 $z = 0$에서 $0.8$, $z = 1$에서 $0.2$라 하자. 그러면 증거는 $\log p(x) = \ln 0.5 = -0.693$나트, 참 사후분포는 $(0.8, 0.2)$다. 균등한 $q = (\tfrac12, \tfrac12)$는 $\text{ELBO} = \tfrac12\ln\tfrac{0.4}{0.5} + \tfrac12\ln\tfrac{0.1}{0.5} = -0.916$나트를 주고, 간극 $0.223$나트가 정확히 $D_{KL}\big(q\,\|\,(0.8, 0.2)\big)$다. $q$를 사후분포로 두면 간극이 닫히고 ELBO가 $-0.693$으로 오른다. 옌센 없이 로그 안에 베이즈 규칙을 넣어 같은 항등식에 이르는 길과, 가우시안 인코더에서 그 간극을 두 방법으로 계산한 값($0.154544$나트)은 [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN §2]]에 있다.

### 6. 빠른 참조 표

| 양 | 공식 | 딥러닝에서의 역할 |
|---|---|---|
| 엔트로피 $H(p)$ | $-E_p[\log p]$ | 불확실성; RL의 탐험 보너스 |
| 교차 엔트로피 $H(p,q)$ | $-E_p[\log q]$ | 분류/언어모델 손실 |
| KL $D_{KL}(p\|q)$ | $E_p[\log p/q]$ | VAE 정규화, RLHF 페널티, 증류 |
| 상호 정보량 $I(X;Y)$ | $H(X)-H(X\mid Y)$ | 대조학습(CLIP), 정보 병목 |
| Perplexity | 비트면 $2^{H(p,q)}$, nat이면 $e^{H(p,q)}$ | 언어모델 평가 |
| ELBO | $E_q[\log p(x\mid z)] - D_{KL}(q\|p)$ | VAE와 변분형 디퓨전·월드모델 정식화 |

> [!tip] 더 깊이 · Going deeper
> MacKay의 [*Information Theory, Inference, and Learning Algorithms*](https://www.inference.org.uk/mackay/itila/)가 무료이고 드물게 잘 읽힌다. 정리를 설명이 아니라 정확한 진술로 봐야 할 때는 Cover·Thomas의 *Elements of Information Theory*.

### 스스로 점검 · Self-check

1. $P(\text{H}) = 0.99$인 동전의 엔트로피를 계산하고, 0.9 동전보다 작은 이유를 말하라.
2. 분류기가 정답 클래스에 확률 0.25를 줬다. 이 샘플의 교차 엔트로피 손실(나트)은?
3. *(두 번째 읽기, §3과 §5.)* VAE에서 어느 방향의 KL이 어디에 나타나고, 그중 무엇이 흐릿한 샘플과 관계되는가?
4. *(두 번째 읽기, §4.)* CLIP의 InfoNCE에서 배치를 2배로 키우면 상호 정보량 하한은 얼마나 좋아질 수 있는가?

> [!tip]- 정답 · Answers
> 1. $H = -0.99\log_2 0.99 - 0.01\log_2 0.01 \approx 0.08$ 비트 — 더 예측 가능할수록 놀라움의 평균이 작다.
> 2. $-\ln 0.25 = \ln 4 \approx 1.39$ 나트.
> 3. reverse KL $KL(q(z|x)\|p(z|x))$은 사후분포 근사에 있다. 모드 시킹이라 $q$를 좁게 잡는 경향이 있지만, 이것은 잠재 변수에 대한 이야기이지 흐릿함의 원인이 아니다. 흐릿함은 데이터 쪽에서 온다: 최대우도는 *forward* $KL(p_{data}\|p_\theta)$을 최소화해 질량을 덮으려 하고, 가우시안 픽셀 우도가 그 불확실성을 평균된 픽셀로 바꾼다.
> 4. $I \ge \log N - \mathcal{L}$이므로 하한의 천장이 $\log 2 \approx 0.69$ 나트(= 1비트)만큼 올라간다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P5** 균열 감지기: $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$. 비트($\log_2$).

1. **그리기.** 오경보율이 $0.05$에서 $P(+|\neg c)=0.01$로 내려간 개선된 감지기에 대해 위의 그림을 그려라. 민감도 $0.95$와 사전 $P(c)=0.01$은 같다. 이진 채널 $C\in\{c,\neg c\}$ → $\{+,-\}$의 전이 넷, 결합 질량 넷, 그리고 $+$ 쪽 묶음에 $P(+)$와 그 두 몫. 동그라미 친 두 숫자 가운데 어느 쪽이 얼마나 움직였는가?
2. **유도.** 1번의 개선된 감지기를 그대로 쓴다. 경보 뒤의 참 사후분포는 1번에서 구한 $p=P(c|+)$의 Bernoulli($p$)다. (a) $H(p)$. (b) 민감도 $q=0.95$를 여전히 $P(c|+)$인 양 내놓는 모델의 교차 엔트로피 $H(p,q)$. (c) §3의 정의대로 항별로 계산한 $D_{KL}(p\,\|\,q)$와, 그것을 $H(p,q)-H(p)$에 대어 본 확인. (d) 세 값을 §2에 나온 카탈로그 감지기의 $0.637$비트, $3.64$비트와 그 차이 $3.00$ 옆에 놓고, 어느 것이 어느 쪽으로 움직였는지와 그 이유를 말하라.
3. **해석.** 개선된 감지기의 경보는 1비트에 가까운 불확실성을 남기고, 이는 카탈로그 감지기의 $0.637$비트보다 많다. 그렇다면 개선된 감지기가 더 나쁜 것인가? §1의 조건부 엔트로피로 판가름하라. 개선된 감지기의 $P(-)$, $P(c|-)$, $H(X|Y{=}0)$, $H(X|Y)$를 구해 카탈로그의 $0.044$비트와 비교하고, 평균의 어느 항이 왜 바뀌었는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - 왼쪽에 입력 노드 둘($c$가 위, $\neg c$가 아래), 오른쪽에 출력 노드 둘($+$가 위, $-$가 아래)을 두고, 입력마다 두 출력 모두로 가는 화살표 넷을 긋는다. 하나도 빼지 않는다. 대각선 화살표 둘이 오류이고 그것이 이 페이지의 교훈 전부다.
> - 화살표마다 조건부 확률 $P(y|x)$를 쓰고, 왼쪽 노드 하나에서 나가는 두 화살표의 합이 $1$인지 확인한다. 오른쪽 노드로 들어오는 둘은 $1$일 필요가 없다. 위 그림에서 $1$이 된 것은 그 채널이 대칭이었기 때문이고, 이 채널은 대칭이 아니다. 입력마다 열 하나를 둔 채널 행렬에서 열은 분포지만 행은 분포일 필요가 없다.
> - 왼쪽 노드는 사전 질량 높이의 상자로 그린다. 정직하게 그리면 $c$ 상자는 선 하나이고, 그 비율이 산술을 시작하기 전에 눈에 보여야 한다.
> - 화살표마다 사전확률과 조건부를 곱해 화살표가 닿는 자리에 적고, 결합 질량 넷의 합이 $1$이라는 확인을 그림에 적는다.
> - $+$에 닿는 화살표 둘을 묶음으로 표시하고 옆에 합 $P(+)$를 쓴 다음, 그 안을 두 몫으로 나눈다. 베이즈 공식이 아니라 그림에서 읽어 낸 경보 후의 사후확률이다. 이제 묶음 안의 두 질량이 거의 같고, 그 거의-동률이 답이다.
> - 화살표 위의 민감도 $P(+|c)$와 묶음 쪽의 사후확률 $P(c|+)$에 동그라미를 치고, 각각을 위 그림의 값 옆에 나란히 적는다. 둘 중 하나는 전혀 움직이지 않았다.

> [!tip]- 정답 · Solutions
> 1. 화살표는 $c\to+$가 $0.95$, $c\to-$가 $0.05$, $\neg c\to+$가 $0.01$, $\neg c\to-$가 $0.99$다. $+$로 들어오는 둘의 합은 이제 $1$이 아니라 $0.96$이다. 채널이 더는 대칭이 아니고, 대칭이어야 할 이유도 없었다. 결합 질량은 $0.0095$, $0.0005$, $0.0099$, $0.9801$이고 합은 $1$이다. $P(+)=0.0194$이고, 그 가운데 $0.490$이 균열에서, $0.510$이 정상에서 온다. 민감도는 그대로 $0.95$이고, 사후 $P(c|+)$는 $0.161$에서 $0.490$으로 약 세 배가 되었다. 경보를 묻어 버린 것이 놓침이 아니라 오경보였기 때문이다. 그래도 절반에는 못 미친다. 사전이 $1\%$일 때 정상 패널 백 개당 오경보 하나는 균열이 내는 경보만큼의 경보를 만든다.
> 2. $P(+)=0.0095+0.0099=0.0194$이고 $p=0.0095/0.0194=0.490$이다. (a) $H(p)=-0.490\log_2 0.490-0.510\log_2 0.510\approx1.000$비트(넷째 자리까지 $0.9997$)로, 공정한 동전의 $1$비트에 아주 조금 못 미친다. (b) $H(p,q)=-0.490\log_2 0.95-0.510\log_2 0.05=0.490(0.074)+0.510(4.322)\approx2.24$비트. (c) $D_{KL}=0.490\log_2\tfrac{0.490}{0.95}+0.510\log_2\tfrac{0.510}{0.05}\approx-0.47+1.71=1.24$비트이고, $2.24-1.00$과 맞는다. 첫 항은 음수이고 둘째 항이 합을 양수로 만든다. §3이 그래야 한다고 말한 그대로다. (d) 바닥 $H(p)$는 $0.637$에서 $1.000$으로 올랐다. 사후확률이 $0.161$에서 $0.490$으로, 동전 던지기 바로 옆으로 옮겨 갔기 때문이다. 교차 엔트로피는 $3.64$에서 $2.24$로 줄었고, 초과분은 가장 크게 $3.00$에서 $1.24$비트로 줄었다. 혼동한 모델이 내놓는 $0.95$에 $0.490$이 $0.161$보다 훨씬 가깝기 때문이다. 더 좋은 감지기에서는 같은 실수가 덜 비싸지만, 여전히 경보마다 $1.24$비트를 치른다.
> 3. $P(-)=1-0.0194=0.9806$, $P(c|-)=0.0005/0.9806=0.00051$이므로 $H(X|Y{=}0)=0.0063$비트다. 그러면 $H(X|Y)=0.0194\times1.000+0.9806\times0.0063=0.0194+0.0062=0.026$비트로 카탈로그의 $0.044$보다 낮다. 평균으로는 개선된 감지기가 불확실성을 덜 남기고, 더 좋은 센서라면 마땅히 그래야 한다. 침묵 항은 거의 그대로이고(둘 다 $0.0062$), 경보 항이 $0.059\times0.637=0.038$에서 $0.019$로 줄었다. 경보 하나하나는 이제 불확실성을 더 남기지만 경보가 세 배 드물어졌다. $0.059$ 가운데 $0.0495$를 차지하던 오경보가 이제는 $0.0194$ 가운데 $0.0099$뿐이기 때문이다. 관측 하나의 엔트로피는 올라가도 평균은 내려갈 수 있고, 이것이 §1의 반례가 그은 경계다. 그러니 센서는 측정 하나가 아니라, 측정마다 일어나는 빈도로 가중한 평균으로 판단한다. (§4는 그 감소분 $H(X)-H(X|Y)$를 상호 정보량이라 부른다. $0.081-0.026=0.055$비트로 불확실성의 $68\%$이고, 카탈로그 감지기는 $0.037$비트, $46\%$다.)
