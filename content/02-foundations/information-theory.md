---
title: 5. Information Theory
tags: [foundations]
study-depth: Literacy
depth-goal: "Read the notation and recurring ideas accurately; return for deeper derivations when a paper requires them."
mastery-when: "Raise to Working or Mastery when the thesis objective depends directly on these formulations."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §6]] (log rules — §0 below re-states them) · [[02-foundations/probability|3. Probability §1–2]] (distributions, expectation)
> [[02-foundations/engineering-math|0.5 §6]](로그 규칙 — 아래 §0이 다시 정리한다) · [[02-foundations/probability|3. 확률 §1–2]](분포·기댓값)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/probability|3. Probability]] and the logs from [[02-foundations/engineering-math|0.5]]. Second applied pillar: it names what those objectives all measure,
which is that cross-entropy is maximum likelihood is KL.*

Everything in deep learning that involves a probability distribution eventually speaks
information theory: cross-entropy loss, KL divergence, the ELBO (evidence lower bound, derived in §5), contrastive learning,
even "perplexity." This page is the complete working set for reading modern papers —
no prior background assumed.

> [!note] First pass · 처음이라면
> Read §0 (three log rules, five minutes), §1, §2, §3 — and do the bit calculations by hand, they are the page. §4 and §5 are for when a paper puts mutual information or an ELBO in its objective.

### Homework diagram · 과제가 그릴 그림

The page's object is the **P5** crack detector from [[02-foundations/lab-plants|0.6 Lab Plants]], and every number below is drawn as a channel. The problem set asks for this same figure.

**The channel itself.** Two nodes on the left, stacked: $c$ (cracked) on top, $\neg c$ (sound) below. Two nodes on the right, also stacked: $+$ (alarm) on top, $-$ (silent) below. Four arrows, every left node to every right node, none omitted — the two diagonal arrows are the errors and they are the whole lesson. Write the conditional on each: $c\to+$ is $0.95$, $c\to-$ is $0.05$, $\neg c\to+$ is $0.05$, $\neg c\to-$ is $0.95$. Check on the drawing that the two arrows leaving each left node sum to $1$, and that the two arrows entering each right node do *not* — a column of a channel matrix is a distribution, a row of it is not.

**The prior, drawn to scale.** Draw the two left nodes as boxes whose heights are their prior masses, $P(c)=0.01$ against $P(\neg c)=0.99$. Drawn honestly, the top box is a line and the bottom one is the whole figure. That ratio of $99$ is the only reason the page's punchline exists, so it must be visible before any arithmetic starts.

**The four joint masses, at the arrowheads.** Multiply prior by conditional along each arrow and write the product where the arrow lands: $0.0095$ on $c\to+$, $0.0005$ on $c\to-$, $0.0495$ on $\neg c\to+$, $0.9405$ on $\neg c\to-$. The four sum to $1$; write that check on the page. Then bracket the two arrows that land on $+$ and write their total, $P(+)=0.059$, beside the bracket. Inside the bracket, split it into the two shares $0.0095/0.059$ and $0.0495/0.059$ and label them $0.161$ and $0.839$: the posterior after an alarm, read off the picture rather than from Bayes' rule.

**The last annotation, which is the point.** Beside the $c\to+$ arrow write $0.95$ once more and circle it; beside the bracket write $0.161$ and circle that. Two circled numbers, one arrow apart, differing by a factor of about six. §2 charges $H(p,q)\approx 3.64$ bits against a floor of $H(p)\approx 0.637$ bits for confusing them, and the problem set asks you to pay that bill by hand.

### 0. Prerequisite: the three log rules

Everything on this page runs on logarithms. If these three lines are not second nature,
read [[02-foundations/engineering-math|0.5 Engineering Math §6]] first (5 minutes):
$\log(ab) = \log a + \log b$ (products of probabilities become sums — why losses are sums);
$\log(a^n) = n \log a$; and base 2 vs base $e$ only changes units (**bits** vs **nats**) by
a constant factor. The factor comes from the change-of-base rule $\log_2 x = \ln x / \ln 2$, so any quantity on this page converts as
$$H_{\text{bits}} = \frac{H_{\text{nats}}}{\ln 2}, \qquad 1\ \text{nat} = 1.443\ \text{bits}$$
because every term is a log and every log rescales by the same $1/\ln 2$. Papers in machine learning usually report nats (PyTorch's losses use $\ln$); coding and communication papers use bits. Also remember: probabilities live in $[0,1]$, so log-probabilities are
$\le 0$ — a "smaller cross-entropy" means log-probs closer to zero.

Logarithms are useful because they turn the joint probability of many observations into an additive score. For example, a classifier can assign plausible labels to most frames yet be strongly penalized for confidently rejecting the correct label on a few. **The reading this gives you.** When a paper reports a log loss, ask which events receive probability and how the score is aggregated. A loss decrease concerns those assigned probabilities; it does not automatically imply a particular improvement in task success.

### 1. Surprise and entropy

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
  $$H(X) = E_p[h(X)] = -\sum_{x \in \mathcal{X}} p(x)\log p(x), \qquad 0 \le H(X) \le \log|\mathcal{X}|$$
  using the convention $0 \log 0 = 0$, since an impossible outcome contributes nothing. The lower bound holds because every surprise is $\ge 0$, with equality only when one outcome has probability 1. The upper bound is reached only by the uniform distribution. *Example:* uniform over 8 values gives $\log_2 8 = 3$ bits, the most any 8-valued source can have. Entropy depends only on the probabilities, not on the values: relabelling outcomes, or a die with faces $10, 20, \dots, 60$, leaves it unchanged.
- **Joint and conditional entropy** extend the same average to two variables $X$ and $Y$ with joint PMF $p(x,y)$. Joint entropy is the uncertainty of the pair. Conditional entropy is the uncertainty left in $X$ once $Y$ is known, averaged over the values of $Y$:
  $$H(X,Y) = -\sum_{x,y} p(x,y)\log p(x,y), \qquad H(X \mid Y) = \sum_y p(y)\,H(X \mid Y{=}y) = -\sum_{x,y} p(x,y)\log p(x \mid y)$$
  They are tied by the **chain rule** $H(X,Y) = H(Y) + H(X \mid Y)$, since $\log p(x,y) = \log p(y) + \log p(x \mid y)$. On average, conditioning never increases uncertainty: $H(X \mid Y) \le H(X)$, with equality iff $X$ and $Y$ are independent (§4 turns the gap into mutual information).
  - *Example* (the crack detector of §4): $H(X) = 0.081$ bits and $H(X \mid Y) = 0.044$ bits.
  - *Non-example, the boundary readers miss:* the inequality is about the average only. After an alarm, $P(\text{crack} \mid \text{alarm}) = 0.161$, so $H(X \mid Y{=}1) = 0.637$ bits, far *more* than the $0.081$ before; a single observation can raise uncertainty. It is outweighed by the silent case, $H(X \mid Y{=}0) = 0.007$ bits, which happens 94% of the time.
- **Expected code length.** A **code** $C$ assigns each outcome $x$ a binary codeword of length $\ell(x)$ bits. It is *uniquely decodable* if every concatenation of codewords can be split back in only one way, and a *prefix code* (no codeword begins another; built as a tree in [[02-foundations/algorithms/greedy-mst|11.4 §5]]) is the common kind that can be decoded on the fly. Its average cost is
  $$L(C, X) = \sum_x p(x)\,\ell(x)$$
  so frequent outcomes should get short words. *Example:* the Huffman code for $p = (0.7, 0.2, 0.1)$ has lengths $(1, 2, 2)$ and $L = 0.7 + 0.4 + 0.2 = 1.3$ bits, the figure used in §2.
- Intuition anchor: entropy is a **lower bound** on the average number of yes/no questions needed to
  identify an outcome — the *compression limit* of the source. No code beats it, and a per-symbol
  code generally does not reach it: every uniquely decodable code has $L(C,X) \ge H(X)$, with equality only when every code length equals its Shannon information content — the surprise $\log_2(1/p(x))$ defined above, in bits (MacKay eq. 5.17), and MacKay's Theorem 5.1 guarantees that *some* prefix code achieves $L(C,X) < H(X)+1$.
- **Worked numbers** — a coin with $P(\text{H}) = 0.9$:
  $H = -0.9\log_2 0.9 - 0.1\log_2 0.1 = 0.9(0.152) + 0.1(3.322) \approx 0.47$ bits —
  less than half the fair coin's 1 bit, because the outcome is mostly predictable.
  And the KL from this coin to a fair coin:
  $D_{KL} = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5} \approx 0.763 - 0.232 = 0.53$
  bits — the *extra* cost per toss of encoding the biased coin with the fair-coin code.
  Run these two computations by hand once; every formula on this page becomes concrete.
- **Differential entropy** is the continuous-variable analogue, used when $X$ has a density $p(x)$ rather than a PMF (it is the quantity [[02-foundations/probability|3. Probability §3]] cites for the Gaussian):
  $$h(X) = -\int p(x)\log p(x)\,dx$$
  It keeps the formula but not all the meaning. Because a density can exceed 1, $h$ can be negative, and it changes when you change units, since rescaling $X$ by $a$ adds $\log|a|$. So it is not a count of bits; only *differences* of differential entropies (as in mutual information and KL) keep their meaning.
  - *Examples:* uniform on $[0, a]$ has $h = \log a$, so uniform on $[0, 0.5]$ has $h = -1$ bit. A Gaussian with variance $\sigma^2$ has $h = \tfrac12\log(2\pi e\sigma^2)$, which is $2.047$ bits for $\sigma = 1$, the largest of any density with that variance.

### 2. Cross-entropy — the loss function you already use

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
- **Worked: P5 crack detector.** Catalog $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$ ([[02-foundations/lab-plants|0.6]]). $P(+)=0.059$, $P(c|+)\approx 0.161$. The true posterior is Bernoulli($0.161$) with $H(p)\approx 0.63$ bits. A model that treats the *sensitivity* $0.95$ as if it were $P(c|+)$ pays $H(p,q)\approx 3.64$ bits. False alarms from the $99\%$ non-crack mass ($0.0495$) dominate true positives ($0.0095$). Sensitivity is $P(+|c)$, not $P(c|+)$. The problem set is this channel as a drawing. Both figures are expected
  costs, not code lengths. Entropy bounds the *expected* length, and a per-symbol code reaches
  it only when every probability is a power of two, because a symbol's code length has to be a
  whole number of bits: the best symbol code here is Huffman at $1.3$ bits (built and proved optimal in [[02-foundations/algorithms/greedy-mst|11.4 §5]]). The floor is approached by coding long blocks of **i.i.d.** ([[02-foundations/probability|3. Probability §2]])
  symbols, which is what Shannon's source coding theorem says — $N$ i.i.d. variables compress into
  about $NH(X)$ bits as $N\to\infty$. That hypothesis matters for the next bullet: language tokens
  are strongly dependent, so their floor is the entropy *rate*, not the single-symbol $H(p)$ just
  computed. The **entropy rate** of a sequence $X_1, X_2, \dots$ is the per-symbol uncertainty once all dependence is accounted for:
  $$H_{\text{rate}} = \lim_{n\to\infty} \frac1n H(X_1, \dots, X_n)$$
  For i.i.d. symbols it equals $H(X_1)$, because the joint entropy of independent symbols is the sum of theirs. *Non-example:* a binary sequence that repeats its previous symbol with probability 0.9 spends half its time on each symbol, so the single-symbol entropy is 1 bit, but its entropy rate is only $H(0.9, 0.1) = 0.469$ bits, since each symbol is mostly predicted by the one before.
- Classification training: $p$ = one-hot label, $q$ = softmax output ⇒
<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="two bars of bits per symbol, the entropy floor and the longer cost of coding with the model, with the excess marked as the KL divergence">
  <g fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2">
    <rect x="90" y="34" width="231.4" height="26" rx="3"/>
    <rect x="90" y="76" width="231.4" height="26" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2">
    <rect x="321.4" y="76" width="24.6" height="26" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="3 3">
    <line x1="321.4" y1="28" x2="321.4" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="24" y="51">H(p) = 1.157 bits</text>
    <text x="24" y="93">H(p, q) = 1.280 bits</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="356" y="93">KL = 0.123</text>
    <text x="315" y="126" text-anchor="end">the floor &#8212; no code beats this</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="160">Entropy is a floor set by the data: no code, however clever, gets below 1.157 bits per symbol.</text>
    <text x="24" y="176">Your model&#8217;s code pays 1.280, and the excess is exactly the KL. So minimising cross-entropy is</text>
    <text x="24" y="192">minimising KL &#8212; the floor is a constant you do not control, and every bit of training progress is</text>
    <text x="24" y="208">the dark band getting narrower.</text>
  </g>
</svg>

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

### 3. KL divergence — the distance-that-isn't

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

<svg viewBox="0 0 480 120" style="max-width:100%;height:auto" role="img" aria-label="cross-entropy equals entropy plus KL">
  <g fill="currentColor" opacity="0.10"><rect x="30" y="74" width="105" height="30" transform="translate(180,0)"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <rect x="30" y="32" width="180" height="30" rx="3"/>
    <rect x="30" y="74" width="180" height="30" rx="3"/>
    <rect x="210" y="74" width="105" height="30" rx="3"/>
  </g>
  <g font-size="12.5" fill="currentColor" text-anchor="middle">
    <text x="120" y="52">H(p)</text><text x="120" y="94">H(p)</text><text x="262" y="94">KL(p‖q)</text>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="20" opacity="0.85">H(p, q)  =  H(p)  +  KL(p‖q)</text>
    <text x="228" y="52" opacity="0.8">the floor: no code can beat it</text>
    <text x="330" y="94" opacity="0.8">what q costs you extra</text>
  </g>
</svg>


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
  *Numbers, in nats (natural log):* $D_{KL}\big(\mathcal{N}(1,1)\,\|\,\mathcal{N}(0,1)\big) = 0 + \tfrac{1 + 1}{2} - \tfrac12 = 0.5$. With widths instead, $D_{KL}\big(\mathcal{N}(0,2^2)\,\|\,\mathcal{N}(0,1)\big) = 0.807$ but $D_{KL}\big(\mathcal{N}(0,1)\,\|\,\mathcal{N}(0,2^2)\big) = 0.318$: a first-slot distribution twice as wide as the second costs more than one half as wide.
- Properties that matter: $\ge 0$, zero iff $p = q$, and **asymmetric** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$ true, fit $q$): mode-**covering** — $q$ spreads to cover all of $p$'s mass.
  - Reverse KL (used in *variational inference* — approximating an intractable distribution
    by picking the closest member of a simple family): mode-**seeking** — $q$ locks onto one mode.
  - The two are two different optimization problems over a family $\mathcal{Q}$ of simple distributions:
  $$q_{\text{fwd}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(p\,\|\,q), \qquad q_{\text{rev}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(q\,\|\,p)$$
    The behaviours follow from where the infinite penalty sits. Forward KL averages over $p$, so it punishes $q \approx 0$ anywhere $p$ has mass; reverse KL averages over $q$, so it punishes $q$ putting mass where $p \approx 0$. *Example:* fit a single Gaussian to the two-bump mixture $p = \tfrac12\mathcal{N}(-2, 0.5^2) + \tfrac12\mathcal{N}(2, 0.5^2)$. Forward KL gives $\mathcal{N}(0, 2.06^2)$, which matches the mixture's mean and variance and puts its peak where $p$ has almost no mass (KL $0.72$ nats). Reverse KL gives $\mathcal{N}(2, 0.5^2)$ (or its mirror at $-2$), one bump exactly, at KL $0.69$ nats. Each answer is poor under the other criterion: the wide fit costs $2.10$ nats in reverse KL, and the one-bump fit costs $15.3$ nats in forward KL.
  This asymmetry contributes to VAEs' limited posterior coverage and to RL-style objectives
  collapsing to narrow behaviors — though classical VAE blur is *primarily* the Gaussian
  pixel likelihood averaging plausible outputs (see the self-check answer below).
- Where you've seen it:
  - [[01-canonical-papers/notes/6-diffusion/vae|VAE]]: the ELBO's regularizer $D_{KL}(q_\phi(z|x)\,\|\,p(z))$.
  - [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]]: per-token KL penalty keeping the
    policy near the SFT model — literally "don't drift too many bits from the reference."
  - [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]: the variational bound is a sum of KL terms between
    Gaussians (which is why it collapses to MSE).
  - Knowledge distillation: student minimizes KL to teacher's soft labels.

### 4. Mutual information

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — how many bits knowing $Y$ tells you about $X$; zero iff independent.
  **Mutual information** is a number attached to a pair of random variables with joint distribution $p(x,y)$ and marginals $p(x)$, $p(y)$. It has three equivalent forms, each a different reading:
  $$I(X;Y) = \sum_{x,y} p(x,y)\log\frac{p(x,y)}{p(x)\,p(y)} = H(X) - H(X \mid Y) = H(X) + H(Y) - H(X,Y)$$
  The first says how far the joint is from the independent product $p(x)p(y)$ (a KL, §3); the second, how much knowing $Y$ reduces uncertainty about $X$ (§1); the third follows from the chain rule of §1. Its properties: **symmetric**, $I(X;Y) = I(Y;X)$; **non-negative**, since it is a KL; **zero iff $X$ and $Y$ are independent**, because only then is the joint equal to the product; and bounded, $I(X;Y) \le \min\big(H(X), H(Y)\big)$.
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
  states no information-theoretic reason for it). Caveat: how tight this MI bound is depends on the negative-sampling
  scheme and distributional assumptions — treat it as guiding intuition, not a guarantee.
  In the formula, $x_i$ and $y_i$ are the two views of the $i$-th pair, so the term $j = i$ is the positive and every $j \ne i$ is a negative. Since $\mathcal{L} \ge 0$, the bound can never certify more than $\log N$, which for CLIP's batch is $\ln 32{,}768 = 10.4$ nats (15 bits).
- Representation learning framings (information bottleneck): keep what predicts the label,
  discard the rest — compression as a theory of generalization.
  The **information bottleneck** (Tishby, Pereira and Bialek, 1999) makes that an objective over a stochastic encoder $p(z \mid x)$ that maps input $X$ to representation $Z$, given a target $Y$:
  $$\min_{p(z \mid x)} \; I(X;Z) - \beta\, I(Z;Y)$$
  The first term is the compression (how much of the input $Z$ keeps), the second the relevance (how much $Z$ tells about the label), and $\beta > 0$ sets the trade-off, so a large $\beta$ keeps more of the input for the sake of prediction. It is assumed that $Z$ depends on $Y$ only through $X$, i.e. $Y \to X \to Z$ form a Markov chain.

### 5. The ELBO, derived honestly

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
so it is a lower bound on the evidence for every $q$, since the KL on the right is $\ge 0$ (§3), and it is tight exactly when $q$ equals the true posterior. *Example with two latent values:* let $z \in \{0, 1\}$ with prior $(\tfrac12, \tfrac12)$, and let the observed $x$ have likelihood $0.8$ under $z = 0$ and $0.2$ under $z = 1$. Then the evidence is $\log p(x) = \ln 0.5 = -0.693$ nats and the true posterior is $(0.8, 0.2)$. A uniform $q = (\tfrac12, \tfrac12)$ gives $\text{ELBO} = \tfrac12\ln\tfrac{0.4}{0.5} + \tfrac12\ln\tfrac{0.1}{0.5} = -0.916$ nats, and the gap $0.223$ nats is exactly $D_{KL}\big(q\,\|\,(0.8, 0.2)\big)$. Setting $q$ to the posterior closes the gap, and the ELBO rises to $-0.693$.

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
3. Which KL direction appears where in a VAE, and which one relates to blurry samples?
4. In CLIP's InfoNCE, how much can doubling the batch size improve the mutual-information bound?

> [!tip]- Answers
> 1. $H = -0.99\log_2 0.99 - 0.01\log_2 0.01 \approx 0.08$ bits — the more predictable, the smaller the average surprise.
> 2. $-\ln 0.25 = \ln 4 \approx 1.39$ nats.
> 3. Reverse KL, $KL(q(z|x)\|p(z|x))$, sits in the posterior fit: being mode-seeking, it tends to under-disperse $q$, which is a statement about the latent, not about blur. Blur comes from the data-level side: maximum likelihood minimises the *forward* $KL(p_{data}\|p_\theta)$, which is mass-covering, and a Gaussian pixel likelihood turns uncertainty into averaged pixels.
> 4. $I \ge \log N - \mathcal{L}$, so the bound's ceiling rises by $\log 2 \approx 0.69$ nats (= 1 bit).

### Problem set · 과제

Tier B. **P5** crack detector from [[02-foundations/lab-plants|0.6]]: $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$. Use bits ($\log_2$).

1. **Draw.** Binary channel $C\in\{c,\neg c\}$ into $\{+,-\}$. Label all four transitions. Mark the rare prior $P(c)=0.01$.
2. **Derive.** (a) $P(+)$ and $P(c|+)$ from Bayes. (b) After a $+$ reading the true posterior is Bernoulli($p$) with that $p$. Binary cross-entropy of a model that outputs $q=0.95$ (the sensitivity, treated as if it were $P(c|+)$). Compare to $H(p)$.
3. **Interpret.** Why is $P(c|+)\approx 0.16$ even though sensitivity is 95%?

> [!tip]- Solutions
> 1. $c\to +$ at $0.95$, $c\to -$ at $0.05$; $\neg c\to +$ at $0.05$, $\neg c\to -$ at $0.95$. Almost all prior mass on $\neg c$.
> 2. $P(+)=0.95\cdot 0.01+0.05\cdot 0.99=0.059$. $P(c|+)=0.0095/0.059\approx 0.161$. $H(p,q)=-p\log_2 0.95-(1-p)\log_2 0.05\approx 3.64$ bits, while $H(p)\approx 0.63$ bits: sensitivity is a badly calibrated posterior.
> 3. False alarms from the 99% non-crack mass dominate true positives ($0.0495$ vs $0.0095$). Sensitivity is $P(+|c)$, not $P(c|+)$.

## 한국어

*[[02-foundations/probability|3. 확률]]과 [[02-foundations/engineering-math|0.5]]의 로그 위에 선다. 둘째 응용 기둥이고, 목적함수들이 공통으로 재는 것에
이름을 붙인다 — 교차 엔트로피가 곧 최대우도이고 곧 KL이다.*

딥러닝에서 확률 분포가 등장하는 모든 것은 결국 정보이론의 언어로 말한다: 교차 엔트로피
손실, KL divergence, ELBO(evidence lower bound, 증거 하한 — §5에서 유도), 대조학습, 심지어 "perplexity"까지. 이 페이지는 최신 논문을
읽는 데 필요한 전부를 사전지식 없이 따라올 수 있게 담았다.

> [!note] 처음이라면 · First pass
> 먼저 §0(로그 세 규칙, 5분), §1, §2, §3 — 비트 계산은 손으로 해라, 그것이 이 페이지다. §4·§5는 논문이 목적함수에 상호 정보량이나 ELBO를 넣을 때 보면 된다.

### 과제가 그릴 그림 · Homework diagram

이 페이지의 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P5** 균열 감지기이고, 아래 숫자는 전부 채널 하나로 그려진다. 과제가 바로 이 그림을 요구한다.

**채널 자체.** 왼쪽에 노드 둘을 위아래로: 위가 $c$(균열 있음), 아래가 $\neg c$(멀쩡함). 오른쪽에도 둘: 위가 $+$(경보), 아래가 $-$(침묵). 화살표는 넷이고 왼쪽 노드마다 오른쪽 노드 둘 모두로 간다. 하나도 빼지 않는다. 대각선 화살표 둘이 오류이고 그것이 이 페이지의 교훈 전부이기 때문이다. 각 화살표에 조건부 확률을 쓴다. $c\to+$는 $0.95$, $c\to-$는 $0.05$, $\neg c\to+$는 $0.05$, $\neg c\to-$는 $0.95$. 그림 위에서 확인할 것 둘: 왼쪽 노드 하나에서 나가는 두 화살표의 합은 $1$이고, 오른쪽 노드 하나로 들어오는 두 화살표의 합은 $1$이 *아니다*. 채널 행렬의 열은 분포지만 행은 분포가 아니다.

**사전확률, 실제 비율로.** 왼쪽 노드 둘을 사전 질량 높이의 상자로 그린다. $P(c)=0.01$ 대 $P(\neg c)=0.99$다. 정직하게 그리면 위 상자는 선 하나이고 아래 상자가 그림 전체다. $99$라는 이 비율이 이 페이지 결론의 유일한 근거이므로, 산술을 시작하기 전에 눈에 보여야 한다.

**결합 질량 넷, 화살촉 자리에.** 화살표마다 사전확률과 조건부를 곱해 화살표가 닿는 자리에 적는다. $c\to+$에 $0.0095$, $c\to-$에 $0.0005$, $\neg c\to+$에 $0.0495$, $\neg c\to-$에 $0.9405$. 넷의 합이 $1$이고, 그 확인을 그림에 적는다. 그다음 $+$에 닿는 화살표 둘을 묶음으로 표시하고 옆에 합 $P(+)=0.059$를 쓴다. 묶음 안을 두 몫 $0.0095/0.059$와 $0.0495/0.059$로 나누고 각각 $0.161$, $0.839$라고 쓴다. 베이즈 공식이 아니라 그림에서 읽어 낸 경보 후의 사후확률이다.

**마지막 주석, 이것이 요점이다.** $c\to+$ 화살표 옆에 $0.95$를 한 번 더 쓰고 동그라미를 친다. 묶음 옆에는 $0.161$을 쓰고 역시 동그라미를 친다. 화살표 하나 떨어진 두 숫자가 약 여섯 배 차이 난다. 이 둘을 혼동한 대가로 §2는 바닥 $H(p)\approx 0.637$비트에 대해 $H(p,q)\approx 3.64$비트를 청구하고, 과제는 그 청구서를 손으로 치르게 한다.

### 0. 사전 준비: 로그의 세 규칙

이 페이지 전체가 로그로 굴러간다. 아래 세 줄이 자동으로 나오지 않으면
[[02-foundations/engineering-math|0.5 공업수학 §6]]을 먼저 읽어라 (5분이면 된다):
$\log(ab) = \log a + \log b$ (확률의 곱이 합이 된다 — 손실이 합인 이유);
$\log(a^n) = n \log a$; 그리고 밑 2와 밑 $e$는 단위(**비트** vs **나트**)만 상수배 바꾼다. 그 상수는 밑 변환 규칙 $\log_2 x = \ln x / \ln 2$에서 오며, 이 페이지의 모든 양은 다음처럼 환산된다.
$$H_{\text{비트}} = \frac{H_{\text{나트}}}{\ln 2}, \qquad 1\ \text{나트} = 1.443\ \text{비트}$$
모든 항이 로그이고 모든 로그가 같은 $1/\ln 2$로 스케일되기 때문이다. 머신러닝 논문은 보통 나트로 보고하고(PyTorch 손실은 $\ln$을 쓴다), 부호화·통신 논문은 비트를 쓴다.
하나 더: 확률은 $[0,1]$에 살므로 로그 확률은 $\le 0$이다 — "교차 엔트로피가 작다" =
로그 확률이 0에 가깝다는 뜻.

로그는 여러 관측에 대한 결합 확률을 더할 수 있는 점수로 바꾼다. 분류기가 대부분 프레임을 그럴듯하게 예측해도 일부 정답에 자신 있게 낮은 확률을 주면 큰 벌점을 받을 수 있다. **여기서 얻는 독법.** 로그 손실에서 어떤 사건에 확률을 주고 어떻게 집계하는지 묻는다. 손실 감소는 그 확률 배정에 관한 결과다. 과제 성공이 특정 정도로 개선된다는 뜻은 아니다.

### 1. 놀라움과 엔트로피

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
  $$H(X) = E_p[h(X)] = -\sum_{x \in \mathcal{X}} p(x)\log p(x), \qquad 0 \le H(X) \le \log|\mathcal{X}|$$
  불가능한 결과는 아무것도 보태지 않으므로 $0 \log 0 = 0$으로 약속한다. 모든 놀라움이 $\ge 0$이므로 하한이 성립하고, 등호는 한 결과의 확률이 1일 때뿐이다. 상한에는 균등 분포만 닿는다. *예:* 값 8개 위의 균등 분포는 $\log_2 8 = 3$비트로, 8값 소스가 가질 수 있는 최대다. 엔트로피는 값이 아니라 확률에만 의존한다: 결과의 이름을 바꾸거나 면이 $10, 20, \dots, 60$인 주사위를 써도 그대로다.
- **결합 엔트로피와 조건부 엔트로피는** 같은 평균을 결합 PMF $p(x,y)$를 갖는 두 변수 $X$, $Y$로 넓힌다. 결합 엔트로피는 쌍의 불확실성이다. 조건부 엔트로피는 $Y$를 안 뒤 $X$에 남은 불확실성을 $Y$의 값들에 대해 평균 낸 것이다:
  $$H(X,Y) = -\sum_{x,y} p(x,y)\log p(x,y), \qquad H(X \mid Y) = \sum_y p(y)\,H(X \mid Y{=}y) = -\sum_{x,y} p(x,y)\log p(x \mid y)$$
  $\log p(x,y) = \log p(y) + \log p(x \mid y)$이므로 둘은 **연쇄 법칙** $H(X,Y) = H(Y) + H(X \mid Y)$로 묶인다. 평균적으로 조건화는 불확실성을 늘리지 않는다: $H(X \mid Y) \le H(X)$이고, 등호는 $X$와 $Y$가 독립일 때만이다(§4가 그 차이를 상호 정보량으로 만든다).
  - *예*(§4의 균열 감지기): $H(X) = 0.081$비트, $H(X \mid Y) = 0.044$비트.
  - *반례, 독자가 놓치는 경계:* 부등식은 평균에 대한 것일 뿐이다. 경보가 울리면 $P(\text{균열} \mid \text{경보}) = 0.161$이므로 $H(X \mid Y{=}1) = 0.637$비트로, 이전의 $0.081$보다 훨씬 *크다*. 관측 하나가 불확실성을 키울 수 있다. 94%의 경우에 일어나는 조용한 쪽 $H(X \mid Y{=}0) = 0.007$비트가 이를 상쇄한다.
- **기대 부호 길이.** **부호** $C$는 각 결과 $x$에 길이 $\ell(x)$비트인 이진 부호어를 배정한다. 부호어를 어떻게 이어 붙여도 한 가지로만 다시 쪼갤 수 있으면 *유일 복호 가능*하고, *접두 부호*(어떤 부호어도 다른 부호어의 앞부분이 아님; 트리로 만드는 법은 [[02-foundations/algorithms/greedy-mst|11.4 §5]])는 읽는 즉시 복호할 수 있는 흔한 종류다. 평균 비용은
  $$L(C, X) = \sum_x p(x)\,\ell(x)$$
  이므로 자주 나오는 결과에 짧은 부호어를 줘야 한다. *예:* $p = (0.7, 0.2, 0.1)$의 허프만 부호는 길이가 $(1, 2, 2)$이고 $L = 0.7 + 0.4 + 0.2 = 1.3$비트로, §2에서 쓰는 값이다.
- 직관의 닻: 엔트로피는 결과 하나를 알아내는 데 필요한 예/아니오 질문 평균 개수의 **하한**이다.
  그 소스의 *압축 한계*이고, 어떤 부호도 이보다 잘하지 못하며, 심볼 단위 부호는 보통 여기에
  닿지도 못한다. 유일 복호 가능한 모든 부호는 $L(C,X) \ge H(X)$이고, 등호는 모든 부호 길이가 자기 Shannon 정보량 — 위에서 정의한 놀라움 $\log_2(1/p(x))$, 비트 단위 — 과
  같을 때만 성립한다(MacKay 식 5.17). MacKay의 정리 5.1은 $L(C,X) < H(X)+1$을 만족하는 접두 부호가 *존재함*을 보장한다.
- **숫자로 한 번** — $P(\text{앞}) = 0.9$인 동전:
  $H = -0.9\log_2 0.9 - 0.1\log_2 0.1 = 0.9(0.152) + 0.1(3.322) \approx 0.47$ 비트 — 공정 동전(1비트)의 절반 이하다.
  결과가 대부분 예측 가능하기 때문. 이 동전과 공정 동전 사이의 KL:
  $D_{KL} = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5} \approx 0.763 - 0.232 = 0.53$ 비트 —
  편향 동전을 공정 동전용 부호로 인코딩할 때 토스당 내는 *추가* 비용이다.
  이 두 계산을 손으로 한 번 해 보라 — 이 페이지의 모든 공식이 구체화된다.
- **미분 엔트로피는** $X$가 PMF가 아니라 밀도 $p(x)$를 가질 때 쓰는 연속 변수 판본이다([[02-foundations/probability|3. 확률 §3]]이 가우시안에 대해 인용하는 양):
  $$h(X) = -\int p(x)\log p(x)\,dx$$
  식은 같지만 의미는 전부 따라오지 않는다. 밀도는 1을 넘을 수 있으므로 $h$는 음수가 될 수 있고, $X$를 $a$배 하면 $\log|a|$가 더해지므로 단위를 바꾸면 값이 바뀐다. 그래서 비트 개수가 아니며, 미분 엔트로피의 *차이*(상호 정보량과 KL처럼)만 의미를 유지한다.
  - *예:* $[0, a]$ 위의 균등 분포는 $h = \log a$이므로 $[0, 0.5]$ 위의 균등 분포는 $h = -1$비트다. 분산 $\sigma^2$인 가우시안은 $h = \tfrac12\log(2\pi e\sigma^2)$이고 $\sigma = 1$이면 $2.047$비트로, 그 분산을 갖는 밀도 중 최대다.

### 2. 교차 엔트로피 — 이미 쓰고 있는 그 손실함수

- $H(p, q) = -\sum_x p(x)\log q(x)$: 진짜 분포가 $p$인 데이터를, 내 모델 $q$에 최적화된
  부호로 인코딩할 때의 비용.
  같은 결과들 위의 **두** 분포, 참(또는 데이터) 분포 $p$와 모델 $q$의 함수다:
  $$H(p, q) = E_{x \sim p}\big[-\log q(x)\big] = -\sum_x p(x)\log q(x)$$
  즉 *진실에서* 뽑힌 결과들에 대해 평균 낸, *모델이 잰* 놀라움이다. 정의적 성질: $H(p,q) \ge H(p)$이고 등호는 $q = p$일 때만이며(§3이 증명한다), $p$와 $q$에 대해 대칭이 아니다. 학습에서 $p$는 라벨 달린 예제 $N$개의 경험 분포이므로, 손실은 각 정답 라벨 $y_i$에 대한 모델의 놀라움의 평균 $-\frac1N\sum_{i=1}^N \log q(y_i \mid x_i)$다. *쓸 수 없는 모델의 반례:* $p(x) > 0$인 결과에 $q(x) = 0$을 주면 교차 엔트로피가 무한대다. 분류기가 정확히 0을 주지 않는 소프트맥스([[02-foundations/engineering-math|0.5 §10]])를 출력하는 이유다.
- **비트 단위 계산 예제.** 참분포 $p = (0.7,\,0.2,\,0.1)$, 모델 $q = (0.5,\,0.3,\,0.2)$.
  $$H(p) = -[0.7\log_2 0.7 + 0.2\log_2 0.2 + 0.1\log_2 0.1] = 1.157\ \text{비트}$$
  $$H(p,q) = -[0.7\log_2 0.5 + 0.2\log_2 0.3 + 0.1\log_2 0.2] = 1.280\ \text{비트}$$
  바닥이 $1.157$인 자리에 모델이 심볼당 $1.280$비트를 치른다 — $0.123$비트를 더 낸 것이다. 이 숫자를 기억해 두라. 3절에서 이것이 정확히 KL임을 보인다.
- **계산: P5 균열 감지기.** 카탈로그의 $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$([[02-foundations/lab-plants|0.6]]). $P(+)=0.059$, $P(c|+)\approx 0.161$. 참 사후분포는 Bernoulli($0.161$)이고 $H(p)\approx 0.63$비트다. *민감도* $0.95$를 $P(c|+)$인 양 쓰는 모델은 $H(p,q)\approx 3.64$비트를 치른다. 균열이 없는 $99\%$ 질량에서 나온 거짓 경보($0.0495$)가 참양성($0.0095$)을 압도한다. 민감도는 $P(+|c)$이지 $P(c|+)$가 아니다. 과제는 이 채널을 그림으로 그리는 것이다.
  두 값 모두 기대 비용이지 부호 길이가 아니다. 엔트로피가 묶는 것은 *기대* 길이이고, 심볼
  단위 부호가 그 바닥에 닿는 것은 모든 확률이 2의 거듭제곱일 때뿐인데, 한 심볼의 부호 길이가
  정수 비트여야 하기 때문이다. 여기서 최선의 심볼
  부호는 허프만이고 $1.3$비트다(만드는 법과 최적성 증명은 [[02-foundations/algorithms/greedy-mst|11.4 §5]]). 바닥에 다가가는 길은 **i.i.d.**([[02-foundations/probability|3. 확률 §2]]) 심볼의 긴 블록을 부호화하는 것이며, 그것이 섀넌의 원천 부호화
  정리다. $N$개의 i.i.d. 변수는 $N\to\infty$에서 약 $NH(X)$비트로 압축된다. 이 전제가 다음
  항목에서 중요해진다. 언어 토큰은 서로 강하게 의존하므로 그쪽의 바닥은 방금 계산한 단일 심볼
  $H(p)$가 아니라 엔트로피 *율*이다. 수열 $X_1, X_2, \dots$의 **엔트로피율은** 의존성을 전부 반영한 뒤의 심볼당 불확실성이다:
  $$H_{\text{rate}} = \lim_{n\to\infty} \frac1n H(X_1, \dots, X_n)$$
  독립인 심볼들의 결합 엔트로피는 각 엔트로피의 합이므로, i.i.d. 심볼이면 $H(X_1)$과 같다. *반례:* 직전 심볼을 확률 0.9로 반복하는 이진 수열은 두 심볼에 시간을 반씩 쓰므로 단일 심볼 엔트로피는 1비트지만, 각 심볼이 대부분 직전 심볼로 예측되므로 엔트로피율은 $H(0.9, 0.1) = 0.469$비트뿐이다.
- 분류 학습: $p$ = 원-핫 라벨, $q$ = 소프트맥스 출력 ⇒ 교차 엔트로피 손실
<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="심볼당 비트 수를 나타내는 두 막대. 엔트로피 바닥과 모델의 부호가 치르는 더 긴 비용, 그 초과분이 KL로 표시되어 있다">
  <g fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2">
    <rect x="90" y="34" width="231.4" height="26" rx="3"/>
    <rect x="90" y="76" width="231.4" height="26" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2">
    <rect x="321.4" y="76" width="24.6" height="26" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="3 3">
    <line x1="321.4" y1="28" x2="321.4" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="24" y="51">H(p) = 1.157 비트</text>
    <text x="24" y="93">H(p, q) = 1.280 비트</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="356" y="93">KL = 0.123</text>
    <text x="315" y="126" text-anchor="end">바닥 &#8212; 어떤 부호도 이보다 낮출 수 없다</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="160">엔트로피는 데이터가 정하는 바닥이다: 아무리 영리한 부호도 심볼당 1.157비트 아래로 내려가지</text>
    <text x="24" y="176">못한다. 내 모델의 부호는 1.280을 치르고, 그 초과분이 정확히 KL이다. 그래서 교차 엔트로피를</text>
    <text x="24" y="192">줄이는 것이 곧 KL을 줄이는 것이다 &#8212; 바닥은 내가 건드릴 수 없는 상수이고, 학습의 진전은 전부</text>
    <text x="24" y="208">저 짙은 띠가 좁아지는 것이다.</text>
  </g>
</svg>

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

### 3. KL divergence — 거리 같지만 거리가 아닌 것

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

<svg viewBox="0 0 480 120" style="max-width:100%;height:auto" role="img" aria-label="교차 엔트로피 = 엔트로피 + KL">
  <g fill="currentColor" opacity="0.10"><rect x="30" y="74" width="105" height="30" transform="translate(180,0)"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <rect x="30" y="32" width="180" height="30" rx="3"/>
    <rect x="30" y="74" width="180" height="30" rx="3"/>
    <rect x="210" y="74" width="105" height="30" rx="3"/>
  </g>
  <g font-size="12.5" fill="currentColor" text-anchor="middle">
    <text x="120" y="52">H(p)</text><text x="120" y="94">H(p)</text><text x="262" y="94">KL(p‖q)</text>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="20" opacity="0.85">H(p, q)  =  H(p)  +  KL(p‖q)</text>
    <text x="228" y="52" opacity="0.8">바닥: 어떤 부호도 이보다 낮출 수 없다</text>
    <text x="330" y="94" opacity="0.8">q를 써서 더 내는 비용</text>
  </g>
</svg>


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
  *숫자로, 나트(자연로그) 단위:* $D_{KL}\big(\mathcal{N}(1,1)\,\|\,\mathcal{N}(0,1)\big) = 0 + \tfrac{1 + 1}{2} - \tfrac12 = 0.5$. 폭을 바꾸면 $D_{KL}\big(\mathcal{N}(0,2^2)\,\|\,\mathcal{N}(0,1)\big) = 0.807$이지만 $D_{KL}\big(\mathcal{N}(0,1)\,\|\,\mathcal{N}(0,2^2)\big) = 0.318$이다: 첫째 자리 분포가 둘째보다 두 배 넓을 때가 절반 폭일 때보다 비싸다.
- 중요한 성질: $\ge 0$, $p = q$일 때만 0, 그리고 **비대칭** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$가 참, $q$를 적합): 모드 **커버링** — $q$가 $p$의 질량 전체를 덮으려 퍼진다.
  - Reverse KL(*변분 추론*에서 사용 — 계산 불가능한 분포를, 다루기 쉬운 분포 가족 중
    가장 가까운 것으로 근사하는 방법): 모드 **시킹** — $q$가 한 모드에 들러붙는다.
  - 둘은 단순한 분포 가족 $\mathcal{Q}$ 위의 서로 다른 최적화 문제다:
  $$q_{\text{fwd}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(p\,\|\,q), \qquad q_{\text{rev}} = \arg\min_{q \in \mathcal{Q}} D_{KL}(q\,\|\,p)$$
    두 행동은 무한대 벌점이 어디 앉는지에서 나온다. Forward KL은 $p$에 대해 평균 내므로 $p$에 질량이 있는 곳에서 $q \approx 0$이면 벌하고, reverse KL은 $q$에 대해 평균 내므로 $p \approx 0$인 곳에 $q$가 질량을 두면 벌한다. *예:* 두 봉우리 혼합 $p = \tfrac12\mathcal{N}(-2, 0.5^2) + \tfrac12\mathcal{N}(2, 0.5^2)$에 가우시안 하나를 맞춘다. Forward KL은 혼합의 평균과 분산을 맞춘 $\mathcal{N}(0, 2.06^2)$을 주는데, 그 봉우리는 $p$의 질량이 거의 없는 곳에 있다(KL $0.72$나트). Reverse KL은 봉우리 하나에 정확히 맞춘 $\mathcal{N}(2, 0.5^2)$(또는 $-2$의 거울상)을 주고 KL은 $0.69$나트다. 각 답은 다른 기준으로 재면 나쁘다: 넓은 적합은 reverse KL로 $2.10$나트, 봉우리 하나짜리 적합은 forward KL로 $15.3$나트다.
  이 비대칭은 VAE의 제한적 사후분포 커버리지와 RL식 목적함수가 좁은 행동으로 붕괴하는
  현상에 기여한다 — 단 고전적 VAE 흐릿함의 *주원인*은 가우시안 픽셀 우도의 평균화다
  (아래 스스로 점검 정답 참고).
- 이미 만난 곳들:
  - [[01-canonical-papers/notes/6-diffusion/vae|VAE]]: ELBO의 정규화 항 $D_{KL}(q_\phi(z|x)\,\|\,p(z))$
  - [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]]: 정책을 SFT 모델 근처에 붙잡는
    토큰별 KL 페널티 — 말 그대로 "기준에서 너무 많은 비트만큼 벗어나지 마라".
  - [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]: 변분 하한이 가우시안 사이 KL 항들의 합이다
    (그래서 MSE로 접힌다).
  - 지식 증류: 학생이 교사의 소프트 라벨에 대한 KL을 최소화.

### 4. 상호 정보량

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — $Y$를 알면 $X$에 대해 몇 비트를 알게 되는가; 독립일 때만 0.
  **상호 정보량은** 결합 분포 $p(x,y)$와 주변 분포 $p(x)$, $p(y)$를 갖는 확률변수 쌍에 붙는 수다. 동치인 세 형태가 있고 각각 다르게 읽힌다:
  $$I(X;Y) = \sum_{x,y} p(x,y)\log\frac{p(x,y)}{p(x)\,p(y)} = H(X) - H(X \mid Y) = H(X) + H(Y) - H(X,Y)$$
  첫째는 결합 분포가 독립 곱 $p(x)p(y)$에서 얼마나 먼지(KL, §3), 둘째는 $Y$를 알면 $X$에 대한 불확실성이 얼마나 줄어드는지(§1)이고, 셋째는 §1의 연쇄 법칙에서 나온다. 성질: **대칭**, $I(X;Y) = I(Y;X)$; KL이므로 **비음수**; 결합이 곱과 같을 때만이므로 **$X$와 $Y$가 독립일 때만 0**; 그리고 $I(X;Y) \le \min\big(H(X), H(Y)\big)$로 유계.
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
  단서: 이 상호 정보량 하한이 얼마나 빡빡한지는 음성 샘플링 방식과 분포 가정에 의존한다 —
  보장이 아니라 안내하는 직관으로 읽어라.
  식에서 $x_i$와 $y_i$는 $i$번째 쌍의 두 뷰이므로 $j = i$ 항이 양성이고 $j \ne i$인 항은 모두 음성이다. $\mathcal{L} \ge 0$이므로 하한은 $\log N$보다 많은 것을 결코 보증하지 못하며, CLIP의 배치에서는 $\ln 32{,}768 = 10.4$나트(15비트)다.
- 표현 학습의 틀(information bottleneck): 라벨을 예측하는 것만 남기고 버려라 —
  압축을 일반화의 이론으로 보는 관점.
  **정보 병목**(Tishby, Pereira, Bialek, 1999)은 이것을, 목표 $Y$가 주어졌을 때 입력 $X$를 표현 $Z$로 보내는 확률적 인코더 $p(z \mid x)$ 위의 목적함수로 만든다:
  $$\min_{p(z \mid x)} \; I(X;Z) - \beta\, I(Z;Y)$$
  첫 항은 압축($Z$가 입력을 얼마나 간직하는가), 둘째 항은 관련성($Z$가 라벨에 대해 얼마나 알려주는가)이고 $\beta > 0$이 둘을 저울질하므로, $\beta$가 크면 예측을 위해 입력을 더 많이 간직한다. $Z$는 $X$를 통해서만 $Y$에 의존한다고, 즉 $Y \to X \to Z$가 마르코프 체인을 이룬다고 가정한다.

### 5. ELBO, 정직하게 유도하기

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
이다. 오른쪽 KL이 $\ge 0$(§3)이므로 모든 $q$에서 증거의 하한이고, $q$가 참 사후분포와 같을 때 정확히 빡빡해진다. *잠재값 두 개짜리 예:* $z \in \{0, 1\}$, 사전 $(\tfrac12, \tfrac12)$, 관측된 $x$의 우도가 $z = 0$에서 $0.8$, $z = 1$에서 $0.2$라 하자. 그러면 증거는 $\log p(x) = \ln 0.5 = -0.693$나트, 참 사후분포는 $(0.8, 0.2)$다. 균등한 $q = (\tfrac12, \tfrac12)$는 $\text{ELBO} = \tfrac12\ln\tfrac{0.4}{0.5} + \tfrac12\ln\tfrac{0.1}{0.5} = -0.916$나트를 주고, 간극 $0.223$나트가 정확히 $D_{KL}\big(q\,\|\,(0.8, 0.2)\big)$다. $q$를 사후분포로 두면 간극이 닫히고 ELBO가 $-0.693$으로 오른다.

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
3. VAE에서 어느 방향의 KL이 어디에 나타나고, 그중 무엇이 흐릿한 샘플과 관계되는가?
4. CLIP의 InfoNCE에서 배치를 2배로 키우면 상호 정보량 하한은 얼마나 좋아질 수 있는가?

> [!tip]- 정답 · Answers
> 1. $H = -0.99\log_2 0.99 - 0.01\log_2 0.01 \approx 0.08$ 비트 — 더 예측 가능할수록 놀라움의 평균이 작다.
> 2. $-\ln 0.25 = \ln 4 \approx 1.39$ 나트.
> 3. reverse KL $KL(q(z|x)\|p(z|x))$은 사후분포 근사에 있다. 모드 시킹이라 $q$를 좁게 잡는 경향이 있지만, 이것은 잠재 변수에 대한 이야기이지 흐릿함의 원인이 아니다. 흐릿함은 데이터 쪽에서 온다: 최대우도는 *forward* $KL(p_{data}\|p_\theta)$을 최소화해 질량을 덮으려 하고, 가우시안 픽셀 우도가 그 불확실성을 평균된 픽셀로 바꾼다.
> 4. $I \ge \log N - \mathcal{L}$이므로 하한의 천장이 $\log 2 \approx 0.69$ 나트(= 1비트)만큼 올라간다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P5** 균열 감지기: $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$. 비트($\log_2$).

1. **그리기.** 이진 채널 $C\in\{c,\neg c\}$ → $\{+,-\}$. 전이 네 개에 확률. 희귀한 사전 $P(c)=0.01$.
2. **유도.** (a) 베이즈로 $P(+)$와 $P(c|+)$. (b) $+$를 본 뒤 참 사후는 그 $p$의 베르누이. 민감도 $q=0.95$를 $P(c|+)$인 양 쓰는 모델의 이진 교차 엔트로피. $H(p)$와 비교.
3. **해석.** 민감도가 95%인데도 $P(c|+)\approx 0.16$인 이유는?

> [!tip]- 정답 · Solutions
> 1. $c\to +$는 $0.95$, $c\to -$는 $0.05$; $\neg c\to +$는 $0.05$, $\neg c\to -$는 $0.95$. 사전 질량은 거의 $\neg c$.
> 2. $P(+)=0.059$. $P(c|+)=0.0095/0.059\approx 0.161$. $H(p,q)\approx 3.64$비트, $H(p)\approx 0.63$비트: 민감도를 사후로 쓰면 보정이 크게 틀린다.
> 3. 균열이 없는 99%에서 나온 거짓 경보가 참양성을 이긴다($0.0495$ vs $0.0095$). 민감도는 $P(+|c)$이지 $P(c|+)$가 아니다.
