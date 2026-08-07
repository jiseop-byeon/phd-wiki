---
title: 0.5 Engineering Math
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> None — this is the entry point. It assumes only first- or second-year engineering mathematics, and re-derives what it needs.
> 없음 — 여기가 진입점이다. 공대 1~2학년 공업수학만 전제하고, 필요한 것은 이 페이지가 다시 세운다.
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

The engineering math that pages 1–9 silently assume, self-contained in one place. Each
section says exactly which foundation page uses it. If all of this reads easily, skip
straight to [[02-foundations/linear-algebra|1. Linear Algebra]].

### 1. Derivatives (→ used by 2. Calculus, 4. Optimization)

- Definition as sensitivity: $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ — "nudge the
  input, how much does the output move?"
- The rules you actually use:

| Rule | Formula |
|---|---|
| Power | $(x^n)' = nx^{n-1}$ |
| Product | $(fg)' = f'g + fg'$ |
| **Chain** | $(f(g(x)))' = f'(g(x))\,g'(x)$ — the rule backprop is built on |
| Exp/Log | $(e^x)' = e^x$, $(\ln x)' = 1/x$ |

- **Partial derivative** $\partial f/\partial x_i$: differentiate w.r.t. one variable,
  hold the rest fixed. The **gradient** $\nabla f = (\partial f/\partial x_1, \ldots)$
  stacks them into a vector.
- Worked example (the shape of every loss-gradient computation):
  $f(x, y) = (xy - 3)^2$ ⇒ $\partial f/\partial x = 2(xy-3)\cdot y$ — outer derivative
  times inner derivative, chain rule in action.

### 2. Taylor expansion (→ 2. Calculus, 4. Optimization)

$$f(x + \delta) \approx f(x) + f'(x)\,\delta + \tfrac12 f''(x)\,\delta^2$$

"Any smooth function is locally a line (1st order) or a parabola (2nd order)."
Gradient descent trusts the line; Newton's method trusts the parabola. Sanity check with
$f = x^2$ at $x=1$: $f(1+\delta) = 1 + 2\delta + \delta^2$ — exact, because $x^2$ *is* a
parabola.

### 3. Integrals and expectations (→ 3. Probability)

- An integral is a weighted sum **in the continuum limit** — slice the axis into pieces,
  multiply each $f$ value by its slice width, add them up, then let the slice width shrink
  to zero. "Continuum limit" always means exactly that: a sum whose steps have been taken
  all the way down to infinitesimal. That sum is written $\int f(x)\,dx$.
- The only integral pattern the foundations really use:
  $E[g(X)] = \int g(x)\,p(x)\,dx$ — "average $g$ over the distribution $p$."
  In code this is always a sample mean; you almost never solve integrals by hand here.
- $\int p(x)\,dx = 1$ (probabilities sum to one) is the identity used in half the proofs
  (e.g., KL non-negativity in [[02-foundations/information-theory|5. Information Theory]]).

### 4. Matrix arithmetic (→ 1. Linear Algebra — its entry requirement)

- $(AB)_{ij} = \sum_k A_{ik}B_{kj}$: row of $A$ · column of $B$. Shapes:
  $(m\times n)(n \times p) = m \times p$.
- Worked 2×2:
  $\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix} = \begin{pmatrix}2&1\\4&3\end{pmatrix}$
  (it swapped the columns — matrices *do things*).
- Not commutative: $AB \ne BA$ in general. Transpose flips indices ($A^\top_{ij} = A_{ji}$);
  identity $I$ changes nothing; the inverse $A^{-1}$ undoes ($A^{-1}A = I$) and only exists
  for square, **full-rank** $A$ — full rank means no column is a combination of the others,
  so the map squashes nothing flat and can be undone. (Rank gets its proper definition in
  [[02-foundations/linear-algebra|1. Linear Algebra §2]]; here, read "full-rank" as
  "nothing was lost, so it is reversible.")

### 5. Series and the geometric sum (→ 7. RL Basics)

$$1 + \gamma + \gamma^2 + \cdots = \frac{1}{1-\gamma} \quad (|\gamma| < 1)$$

**Where that comes from.** Give the sum a name:

$$S = 1 + \gamma + \gamma^2 + \gamma^3 + \cdots$$

Multiply both sides by $\gamma$. Every term just moves up one power:

$$\gamma S = \gamma + \gamma^2 + \gamma^3 + \gamma^4 + \cdots$$

Now put the two lines side by side. The second one is the first one **with the leading $1$
removed** — after that, they match term for term forever. Written as an equation, that
observation is exactly

$$\gamma S = S - 1$$

and that is the whole trick: multiplying by $\gamma$ reproduces the *same* infinite tail, so
the infinity cancels itself and only ordinary algebra is left:

$$\gamma S = S - 1 \;\Rightarrow\; \gamma S - S = -1 \;\Rightarrow\; S(1 - \gamma) = 1 \;\Rightarrow\; S = \frac{1}{1-\gamma}$$

The condition $|\gamma| < 1$ is what lets the tail shrink to nothing; at $\gamma = 1$ the sum
really is infinite, and the formula correctly blows up. Sanity check with $\gamma = 0.5$: the
formula says $S = 1/0.5 = 2$, and by hand $1 + 0.5 + 0.25 + 0.125 + \cdots$ does creep toward $2$.

The truncated version, which is the one that shows up in papers (same proof, one leftover term):

$$1 + \gamma + \cdots + \gamma^{n-1} = \frac{1 - \gamma^n}{1 - \gamma}$$

**Why RL cares.** A reward $k$ steps in the future is counted with weight $\gamma^k$, so the
total weight an agent can ever collect is precisely this sum, $1/(1-\gamma)$. At
$\gamma = 0.99$ that is $100$: the agent behaves roughly as if it were adding up 100
undiscounted steps and ignoring everything past them. Corroboration from the other side —
$0.99^{100} \approx 0.37$, so by step 100 the weight on a reward has already fallen to about a
third. Hence the phrase "effective horizon ≈ 100 steps" in [[02-foundations/rl-basics|RL]].

### 6. Exponentials and logarithms (→ 5. Information Theory — its entry requirement)

- $e^x$: the function that is its own derivative; growth at a rate proportional to itself.
  ($e \approx 2.718$.)
- **Which base?** $\ln$ always means base $e$ (the *natural* log — that is what the "n"
  stands for), and $\log_2$ means base 2. A bare $\log$ has no universal meaning: in this
  wiki and in most ML papers it means base $e$, except in information theory, where the
  unit is the **bit** and the base is 2. The good news is that it almost never matters:
  changing base only multiplies everything by a constant (third rule below), and constants
  do not change where a minimum is.
- $\log$ is the inverse of the exponential: $\log(e^x) = x$. The three rules that carry all
  of information theory and every likelihood computation:

| Rule | Why it matters |
|---|---|
| $\log(ab) = \log a + \log b$ | products of probabilities → **sums** of log-probs (why losses are sums) |
| $\log(a^n) = n\log a$ | powers become multiplications |
| $\log_b x = \ln x / \ln b$ | change of base: base 2 (bits) vs base $e$ (nats) differ by a constant — that's all |

  Where the third rule comes from: let $y = \log_b x$, which by definition means $b^y = x$.
  Take $\ln$ of both sides — $y \ln b = \ln x$ — and divide. So $1/\ln b$ is just a fixed
  number: $\log_2 x = \ln x / \ln 2 \approx 1.4427\,\ln x$. One nat $\approx 1.44$ bits.
- Numbers to internalize: $\log 1 = 0$; $\log x < 0$ for $x<1$ (log-probs are negative!);
  $\log$ grows painfully slowly.
- **Log-sum-exp**: $\log \sum_i e^{x_i}$ is everywhere (it is the denominator of softmax),
  and computed literally it overflows — $e^{800}$ is already $\infty$ in float64. The fix,
  with $x_{max} = \max_i x_i$:

  $$\log \sum_i e^{x_i} = x_{max} + \log\sum_i e^{x_i - x_{max}}$$

  Where it comes from: factor the largest term out of the sum,
  $\sum_i e^{x_i} = e^{x_{max}}\sum_i e^{x_i - x_{max}}$, then take $\log$ and use
  $\log(ab) = \log a + \log b$ from the table above. It is an *exact* identity, not an
  approximation. Why it fixes the problem: every exponent $x_i - x_{max}$ is now $\le 0$,
  so every $e^{(\cdot)}$ is between $0$ and $1$ — nothing can overflow, and the largest term
  is exactly $1$, so nothing underflows to an all-zero sum either. This is why
  softmax+cross-entropy code never blows up
  ([[02-foundations/calculus-backprop|2. Calculus §4]]).

### 7. Complex numbers and Euler's formula (→ 6. Signal Processing — its entry requirement)

- $j = \sqrt{-1}$; a complex number $a + jb$ is a point in the 2D plane, $a$ across and $b$
  up; $|a+jb| = \sqrt{a^2+b^2}$ is its distance from the origin, and its angle is
  $\theta = \operatorname{atan2}(b, a)$.
- **What atan2 is**: the two-argument arctangent, a function every language ships
  (`atan2(y, x)` in C, Python, NumPy, MATLAB). It takes the two coordinates *separately*
  and returns the angle of the point $(x, y)$ over the full circle, $(-\pi, \pi]$.
- **Why not $\arctan(b/a)$**: dividing first throws away information. $\arctan$ only ever
  sees the single number $b/a$, and a point and its exact opposite have the *same* ratio.
  Concretely, $(a,b) = (1,1)$ and $(a,b) = (-1,-1)$ both give $b/a = 1$, so $\arctan$ returns
  $45°$ for both — but the second point is in the third quadrant, at $225°$ (i.e. $-135°$).
  That is what "loses the quadrant" means: the answer is off by exactly $180°$ for half the
  plane, and $\arctan$ has no way to know which half you were in. It also breaks at $a = 0$
  (division by zero) where the true angle is a perfectly ordinary $\pm 90°$. `atan2` keeps
  both signs, so it gets all four quadrants and the vertical axis right. In robotics this is
  the difference between a joint commanded forward and the same joint commanded backward —
  which is why the [[02-foundations/se3-geometry|SE(3)]] page and every IK implementation use
  atan2 exclusively.

<svg viewBox="0 0 470 200" style="max-width:100%;height:auto" role="img" aria-label="two opposite points share the same b/a ratio, so arctan cannot tell them apart">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="26" y1="100" x2="234" y2="100"/><line x1="130" y1="16" x2="130" y2="184"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="4 3"><line x1="48" y1="182" x2="212" y2="18"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.7"><path d="M130,100 L183,47"/><path d="M130,100 L77,153"/></g>
  <g fill="currentColor"><circle cx="185" cy="45" r="4.5"/><circle cx="75" cy="155" r="4.5"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.75"><path d="M152,100 A22,22 0 0 0 145.6,84.4"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.55"><path d="M172,100 A42,42 0 1 0 100.3,129.7"/></g>
  <g font-size="11" fill="currentColor">
    <text x="196" y="40">(1, 1)</text>
    <text x="22" y="172">(&#8722;1, &#8722;1)</text>
    <text x="152" y="88" font-size="10">45&#176;</text>
    <text x="86" y="152" font-size="10">225&#176;</text>
    <text x="255" y="44">Both points sit on the same dashed line</text>
    <text x="255" y="62">through the origin, so b/a = 1 for both.</text>
    <text x="255" y="92">arctan(b/a) = 45&#176; for both &#8212; right for one,</text>
    <text x="255" y="110">wrong by 180&#176; for the other.</text>
    <text x="255" y="140">atan2(b, a) keeps the two signs apart</text>
    <text x="255" y="158">and returns 45&#176; and &#8722;135&#176;.</text>
  </g>
</svg>


- **Euler's formula**: $e^{j\theta} = \cos\theta + j\sin\theta$ — the unit-circle point at
  angle $\theta$. Consequence: multiplying by $e^{j\theta}$ **rotates** by $\theta$.
- **Why this makes Fourier analysis work.** Three steps, and the third is the whole idea.
  1. *A sinusoid is a rotation seen from the side.* As $t$ runs, $e^{j\omega t}$ is a point
     going around the unit circle $\omega$ radians per second. Its real part — its shadow on
     the horizontal axis — is $\cos\omega t$. So a cosine is not a different kind of object
     from a rotation; it is the same object, viewed edge-on.
  2. *To ask "how much of frequency $\omega$ is in my signal?", counter-rotate and average.*
     Multiply the signal by $e^{-j\omega t}$, a rotation going the opposite way at the same
     rate, and average over time. If the signal really does contain that frequency, the
     counter-rotation cancels its spinning and holds it still, so the average is a nonzero
     number. If it doesn't, the product keeps spinning, visits every direction equally, and
     averages to zero.
  3. *That "multiply and average" is a dot product* — the same operation as
     $\langle a,b\rangle$ in [[02-foundations/linear-algebra|1. Linear Algebra §1]], the one
     that measures how much of one vector lies along another. Measuring the overlap with
     each rotation is projecting the signal onto that rotation. That is all "decompose into
     sinusoids" means.

  So the DFT formula $X[k] = \sum_n x[n]\,e^{-j2\pi kn/N}$ in
  [[02-foundations/signal-processing|6. Signal Processing]] has no hidden content: the
  $e^{-j(\cdot)}$ is the counter-rotation of step 2, and the $\sum_n$ is the averaging.
  It is one dot product per frequency.

<svg viewBox="0 0 470 222" style="max-width:100%;height:auto" role="img" aria-label="a point rotating on the unit circle; its shadow on the real axis traces a cosine">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="20" y1="90" x2="150" y2="90"/><line x1="85" y1="25" x2="85" y2="155"/></g>
  <circle cx="85" cy="90" r="52" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.7" fill="none"><line x1="85" y1="90" x2="118.4" y2="50.2"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.65" stroke-dasharray="4 3"><line x1="118.4" y1="50.2" x2="118.4" y2="90"/></g>
  <g fill="currentColor"><circle cx="118.4" cy="50.2" r="4"/><circle cx="118.4" cy="90" r="3"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.8"><path d="M105,90 A20,20 0 0 0 97.9,74.7"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="175" y1="90" x2="440" y2="90"/></g>
  <path d="M175.0 45.0L176.3 45.0L177.6 45.1L178.9 45.2L180.2 45.4L181.5 45.6L182.8 45.8L184.1 46.1L185.4 46.4L186.7 46.8L188.0 47.2L189.3 47.7L190.6 48.2L191.9 48.7L193.2 49.3L194.5 49.9L195.8 50.6L197.1 51.3L198.4 52.0L199.7 52.8L201.0 53.6L202.3 54.4L203.6 55.3L204.9 56.2L206.2 57.2L207.5 58.2L208.8 59.2L210.1 60.2L211.4 61.3L212.7 62.4L214.0 63.5L215.3 64.7L216.6 65.9L217.9 67.1L219.2 68.3L220.5 69.6L221.8 70.8L223.1 72.1L224.4 73.4L225.7 74.8L227.0 76.1L228.3 77.4L229.6 78.8L230.9 80.2L232.2 81.6L233.5 83.0L234.8 84.4L236.1 85.8L237.4 87.2L238.7 88.6L240.0 90.0L241.3 91.4L242.6 92.8L243.9 94.2L245.2 95.6L246.5 97.0L247.8 98.4L249.1 99.8L250.4 101.2L251.7 102.6L253.0 103.9L254.3 105.2L255.6 106.6L256.9 107.9L258.2 109.2L259.5 110.4L260.8 111.7L262.1 112.9L263.4 114.1L264.7 115.3L266.0 116.5L267.3 117.6L268.6 118.7L269.9 119.8L271.2 120.8L272.5 121.8L273.8 122.8L275.1 123.8L276.4 124.7L277.7 125.6L279.0 126.4L280.3 127.2L281.6 128.0L282.9 128.7L284.2 129.4L285.5 130.1L286.8 130.7L288.1 131.3L289.4 131.8L290.7 132.3L292.0 132.8L293.3 133.2L294.6 133.6L295.9 133.9L297.2 134.2L298.5 134.4L299.8 134.6L301.1 134.8L302.4 134.9L303.7 135.0L305.0 135.0L306.3 135.0L307.6 134.9L308.9 134.8L310.2 134.6L311.5 134.4L312.8 134.2L314.1 133.9L315.4 133.6L316.7 133.2L318.0 132.8L319.3 132.3L320.6 131.8L321.9 131.3L323.2 130.7L324.5 130.1L325.8 129.4L327.1 128.7L328.4 128.0L329.7 127.2L331.0 126.4L332.3 125.6L333.6 124.7L334.9 123.8L336.2 122.8L337.5 121.8L338.8 120.8L340.1 119.8L341.4 118.7L342.7 117.6L344.0 116.5L345.3 115.3L346.6 114.1L347.9 112.9L349.2 111.7L350.5 110.4L351.8 109.2L353.1 107.9L354.4 106.6L355.7 105.2L357.0 103.9L358.3 102.6L359.6 101.2L360.9 99.8L362.2 98.4L363.5 97.0L364.8 95.6L366.1 94.2L367.4 92.8L368.7 91.4L370.0 90.0L371.3 88.6L372.6 87.2L373.9 85.8L375.2 84.4L376.5 83.0L377.8 81.6L379.1 80.2L380.4 78.8L381.7 77.4L383.0 76.1L384.3 74.8L385.6 73.4L386.9 72.1L388.2 70.8L389.5 69.6L390.8 68.3L392.1 67.1L393.4 65.9L394.7 64.7L396.0 63.5L397.3 62.4L398.6 61.3L399.9 60.2L401.2 59.2L402.5 58.2L403.8 57.2L405.1 56.2L406.4 55.3L407.7 54.4L409.0 53.6L410.3 52.8L411.6 52.0L412.9 51.3L414.2 50.6L415.5 49.9L416.8 49.3L418.1 48.7L419.4 48.2L420.7 47.7L422.0 47.2L423.3 46.8L424.6 46.4L425.9 46.1L427.2 45.8L428.5 45.6L429.8 45.4L431.1 45.2L432.4 45.1L433.7 45.0L435.0 45.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.65" stroke-dasharray="4 3"><line x1="211.1" y1="61.1" x2="211.1" y2="90"/></g>
  <g fill="currentColor"><circle cx="211.1" cy="61.1" r="4"/></g>
  <g font-size="11" fill="currentColor">
    <text x="124.4" y="44.2">e^(j&#952;)</text>
    <text x="102" y="86" font-size="10">&#952;</text>
    <text x="96" y="162" font-size="10">Re = cos &#952;</text>
    <text x="176" y="18">cos &#952; as &#952; goes around once</text>
    <text x="416" y="106" font-size="10">&#952;</text>
    <text x="20" y="184" opacity="0.9">The wave on the right is not a second object &#8212; it is the left</text>
    <text x="20" y="199" opacity="0.9">picture's shadow, plotted as the point goes around. That is why</text>
    <text x="20" y="214" opacity="0.9">&#8220;decompose into sinusoids&#8221; and &#8220;project onto rotations&#8221; are one sentence.</text>
  </g>
</svg>



### 8. Linear differential equations (→ control track: pages 5–7)

Physical systems are described by ODEs — this is the modeling language of all of control, picked up directly in [[04-robotics/control-theory-ce397|5. Control Theory §2–4]].

- **First order**: $\dot x = ax$ has solution $x(t) = x(0)\,e^{at}$. You do not have to solve
  anything to believe it — just differentiate the candidate and check:
  $\frac{d}{dt}\big(x(0)e^{at}\big) = a\,x(0)e^{at} = a\,x(t)$ ✓, and at $t=0$ it gives
  $x(0)$ ✓. That is the entire content of "$e$ is the function that is its own derivative"
  (§6) applied to a physical system. Everything follows from this one fact: $a < 0$ decays (stable), $a > 0$ blows up (unstable). A robot joint,
  a heating room, a draining tank — all locally this equation.
- **With input**: $\dot x = ax + bu$ — the solution is "decayed initial state + accumulated
  input"; this is the scalar version of the state-space model
  $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$ ([[02-foundations/linear-algebra|linear algebra §5]]),
  and $e^{at}$ becomes the matrix exponential $e^{At}$ with eigenvalues playing the role of $a$.
- **Second order**: $\ddot x + 2\zeta\omega_n \dot x + \omega_n^2 x = 0$ — the
  mass-spring-damper. Two numbers describe every response: natural frequency $\omega_n$
  (how fast it oscillates) and damping ratio $\zeta$ (whether it rings: $\zeta<1$
  oscillates, $\zeta \ge 1$ doesn't). Robot arms and suspension systems are tuned in this
  vocabulary.
- Discrete time (what code runs): $x_{t+1} = a x_t$ ⇒ $x_t = a^t x_0$ — stable iff
  $|a| < 1$. The continuous and discrete conditions ($\text{Re}(a) < 0$ vs $|a_d| < 1$) are
  the same statement, and here is the bridge: sampling $\dot x = ax$ every $\Delta t$ gives
  $x_{t+1} = e^{a\Delta t}x_t$, so the discrete factor is $a_d = e^{a\Delta t}$. Since
  $|e^{a\Delta t}| = e^{\text{Re}(a)\Delta t}$, that magnitude is below $1$ exactly when
  $\text{Re}(a) < 0$. The left half-plane *maps onto* the unit disc — one story, two
  coordinate systems.

### 9. Laplace transform and the s-plane (→ control track, 6. Signal Processing §5)

The Laplace transform turns ODEs into algebra — and [[04-robotics/control-theory-ce397|5. Control Theory §5]] turns the resulting pole picture into the settling-time and overshoot numbers papers quote:

- Definition: $F(s) = \int_0^\infty f(t)\,e^{-st}\,dt$; the one property that matters:
  **differentiation becomes multiplication by $s$** — $\mathcal{L}[\dot f] = sF(s) - f(0)$.
- Consequence: an ODE becomes a polynomial equation, and a system becomes a
  **transfer function** $G(s) = \frac{\text{output}(s)}{\text{input}(s)}$ — e.g.,
  $\dot x = ax + u$ gives $G(s) = \frac{1}{s - a}$.
- **Poles** = roots of the denominator = the $a$'s of section 8 = eigenvalues of the
  state-space $A$. Plotted in the complex **s-plane**:
  - left half-plane (negative real part) → decaying → **stable**
  - right half-plane → growing → **unstable**
  - imaginary part → oscillation frequency; distance from axis → decay speed

<svg viewBox="0 0 430 212" style="max-width:100%;height:auto" role="img" aria-label="the s-plane: pole locations and what they mean">
  <g fill="currentColor" opacity="0.07"><rect x="20" y="15" width="195" height="160"/></g>
  <g stroke="currentColor" stroke-width="1.3"><line x1="20" y1="103" x2="410" y2="103"/><line x1="215" y1="15" x2="215" y2="190"/></g>
  <g fill="currentColor">
    <path d="M112,58 l6,6 l-6,6 l-6,-6 z"/><path d="M112,142 l6,6 l-6,6 l-6,-6 z"/>
    <path d="M64,97 l6,6 l-6,6 l-6,-6 z"/>
    <path d="M312,71 l6,6 l-6,6 l-6,-6 z"/><path d="M312,129 l6,6 l-6,6 l-6,-6 z"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity="0.6">
    <line x1="112" y1="64" x2="215" y2="103"/><line x1="112" y1="64" x2="112" y2="103"/>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="26" y="32">LEFT half-plane = stable</text><text x="250" y="32">RIGHT half-plane = unstable</text>
    <text x="386" y="120">Re</text><text x="222" y="26">Im</text>
    <text x="124" y="56" font-size="10.5" opacity="0.9">complex pair</text>
    <text x="26" y="90" font-size="10.5" opacity="0.9">real pole</text>
    <text x="26" y="192" font-size="11" opacity="0.85">complex pair = decaying oscillation &#183; real pole = pure decay</text>
    <text x="26" y="206" font-size="11" opacity="0.85">farther left = faster decay &#183; farther from the real axis = faster oscillation</text>
  </g>
</svg>


- This is why [[02-foundations/engineering-math|§7]]'s complex plane matters for control:
  *a system's entire qualitative behavior is a picture — where its poles sit.* Frequency
  response is $G(j\omega)$ — evaluate on the imaginary axis, and you recover
  [[02-foundations/signal-processing|signal processing]]'s filters. (Discrete-time twin:
  the Z-transform, unit circle instead of left half-plane.)

### 10. Notation dictionary (all pages)

Two definitions used everywhere before they are formally introduced:

- **Softmax** turns any score vector into a probability distribution:
  $\text{softmax}(z)_i = e^{z_i} / \sum_j e^{z_j}$ — positive, sums to 1, and the largest
  score gets the largest probability (a smooth $\arg\max$). It appears in attention,
  classification losses, and policies alike.
- **Set notation**: $x \in A$ ("$x$ is in $A$"), $A \cap B$ (both), $A \cup B$ (either),
  $\Omega$ (the set of all outcomes), disjoint = no overlap. Probability pages use these
  from the first line.

| Symbol | Read as |
|---|---|
| $\sum_i$, $\prod_i$ | sum / product over index $i$ |
| $\arg\max_x f(x)$ | the $x$ that maximizes $f$ (not the max value itself) |
| $E[\cdot]$, $\text{Var}(\cdot)$ | expectation, variance |
| $x \sim p$ | $x$ is sampled from distribution $p$ |
| $\propto$ | proportional to (equal up to a constant) |
| $\|x\|$ | norm (length) of $x$ |
| $\mathbb{1}[\cdot]$ | indicator: 1 if true, 0 if false |
| $\odot$ | element-wise product |
| $:=$ | defined as |
| $A^\top$ | transpose — flip the matrix across its diagonal ($A^\top_{ij} = A_{ji}$) |
| $\det A$ | determinant — the factor by which the map scales volume; $0$ means it flattens space, so it has no inverse |
| $A \succeq 0$, $A \succ 0$ | positive semidefinite / definite — the matrix version of "$\ge 0$" / "$>0$": $x^\top A x \ge 0$ for every $x$ |

### Self-check

1. Differentiate $f(x) = \log(1 + e^x)$ (softplus) using the chain rule; show the result
   is the sigmoid.
2. Use the geometric sum to explain why rewards ~200 steps away are nearly invisible to an
   agent with $\gamma = 0.99$.
3. Show $\log \frac{a}{b} = \log a - \log b$ from the product rule.
4. Compute $e^{j\pi}$ from Euler's formula and interpret the result as a rotation.
5. (§8) A joint obeys $\dot x = -3x$. Is it stable? What is $x(t)$ from $x(0)=2$, and roughly
   when has it decayed to ~5% of the start?
6. (§9) The system $\dot x = -3x + u$ has transfer function $G(s) = \frac{1}{s+3}$. Where is
   its pole, which half-plane, and what does that say about stability?

> [!tip]- Answers
> 1. $f'(x) = \frac{e^x}{1+e^x} = \frac{1}{1+e^{-x}} = \sigma(x)$ — softplus's derivative is the sigmoid.
> 2. The weight on a reward 200 steps out is $\gamma^{200}=0.99^{200}\approx 0.13$ — already faint at twice the effective horizon (100 steps); by 400 steps it is ~0.
> 3. $\log\frac{a}{b} = \log(a\cdot b^{-1}) = \log a + \log b^{-1} = \log a - \log b$.
> 4. $e^{j\pi} = \cos\pi + j\sin\pi = -1$ — a 180° rotation sends 1 to $-1$.
> 5. Stable ($a=-3<0$). $x(t) = 2e^{-3t}$; ~5% means $e^{-3t}\approx 0.05 \Rightarrow 3t\approx 3 \Rightarrow t\approx 1$ s.
> 6. Pole at $s=-3$ — left half-plane (negative real part), so **stable**; the pole *is* the $a=-3$ of §8 and the eigenvalue of a 1-D state-space $A$.

## 한국어

1~9 페이지가 말없이 전제하는 공업수학을 한곳에 자체 완결로 정리했다.
각 절이 정확히 어느 기초 페이지에 쓰이는지 표시했다. 전부 술술 읽히면 바로
[[02-foundations/linear-algebra|1. 선형대수]]로 건너뛰어라.

### 1. 미분 (→ 2. 미적분, 4. 최적화에서 사용)

- 민감도로서의 정의: $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ — "입력을 살짝 밀면
  출력이 얼마나 움직이는가?"
- 실제로 쓰는 규칙들:

| 규칙 | 공식 |
|---|---|
| 거듭제곱 | $(x^n)' = nx^{n-1}$ |
| 곱 | $(fg)' = f'g + fg'$ |
| **연쇄** | $(f(g(x)))' = f'(g(x))\,g'(x)$ — 역전파가 세워진 그 규칙 |
| 지수/로그 | $(e^x)' = e^x$, $(\ln x)' = 1/x$ |

- **편미분** $\partial f/\partial x_i$: 한 변수로만 미분하고 나머지는 고정.
  **그래디언트** $\nabla f = (\partial f/\partial x_1, \ldots)$는 그것들을 벡터로 쌓은 것.
- 계산 예제 (모든 손실-그래디언트 계산의 원형):
  $f(x, y) = (xy - 3)^2$ ⇒ $\partial f/\partial x = 2(xy-3)\cdot y$ — 바깥 미분 × 안쪽
  미분, 연쇄 법칙의 실전.

### 2. 테일러 전개 (→ 2. 미적분, 4. 최적화)

$$f(x + \delta) \approx f(x) + f'(x)\,\delta + \tfrac12 f''(x)\,\delta^2$$

"매끄러운 함수는 국소적으로 직선(1차)이거나 포물선(2차)이다." 경사 하강은 직선을 믿고,
뉴턴법은 포물선을 믿는다. $f = x^2$, $x=1$에서 검산: $f(1+\delta) = 1 + 2\delta + \delta^2$
— 정확히 맞다, $x^2$ 자체가 포물선이니까.

### 3. 적분과 기댓값 (→ 3. 확률)

- 적분은 **연속 극한**(continuum limit)의 가중합이다 — 축을 조각으로 자르고, 각 $f$ 값에
  조각의 폭을 곱해 더한 뒤, 조각의 폭을 0으로 보낸 것. "연속 극한"은 언제나 이 뜻이다:
  더하는 단위를 끝까지 무한소로 내려보낸 합. 그 합을 $\int f(x)\,dx$로 쓴다.
- 기초 페이지들이 실제로 쓰는 적분 패턴은 사실상 하나:
  $E[g(X)] = \int g(x)\,p(x)\,dx$ — "분포 $p$ 위에서 $g$의 평균." 코드에서는 언제나 샘플
  평균이 되고, 여기서 적분을 손으로 풀 일은 거의 없다.
- $\int p(x)\,dx = 1$ (확률의 합은 1) — 증명의 절반에 쓰이는 항등식이다
  (예: [[02-foundations/information-theory|5. 정보이론]]의 KL 비음수성).

### 4. 행렬 연산 (→ 1. 선형대수의 입장 조건)

- $(AB)_{ij} = \sum_k A_{ik}B_{kj}$: $A$의 행 · $B$의 열. 모양:
  $(m\times n)(n \times p) = m \times p$.
- 2×2 계산 예제:
  $\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix} = \begin{pmatrix}2&1\\4&3\end{pmatrix}$
  (열이 서로 바뀌었다 — 행렬은 *무언가를 한다*).
- 교환 법칙 없음: 일반적으로 $AB \ne BA$. 전치는 인덱스를 뒤집고($A^\top_{ij} = A_{ji}$),
  항등 행렬 $I$는 아무것도 바꾸지 않으며, 역행렬 $A^{-1}$은 되돌린다($A^{-1}A = I$) —
  정방·**풀랭크**(full rank)일 때만 존재 — 풀랭크란 어떤 열도 다른 열들의 조합이 아니라는
  뜻이고, 그래서 사상이 아무것도 납작하게 뭉개지 않으므로 되돌릴 수 있다. (랭크의 정식
  정의는 [[02-foundations/linear-algebra|1. 선형대수 §2]]. 여기서는 "풀랭크" = "잃어버린
  것이 없어 되돌릴 수 있다"로 읽으면 된다.)

### 5. 급수와 기하급수 합 (→ 7. RL 기초)

$$1 + \gamma + \gamma^2 + \cdots = \frac{1}{1-\gamma} \quad (|\gamma| < 1)$$

**어디서 나온 식인가.** 합에 이름부터 붙인다:

$$S = 1 + \gamma + \gamma^2 + \gamma^3 + \cdots$$

양변에 $\gamma$를 곱한다. 각 항의 지수가 하나씩 올라갈 뿐이다:

$$\gamma S = \gamma + \gamma^2 + \gamma^3 + \gamma^4 + \cdots$$

이제 두 줄을 나란히 놓고 보라. 아래 줄은 위 줄에서 **맨 앞의 $1$만 뺀 것**이고, 그 뒤로는
항이 끝까지 하나씩 정확히 맞물린다. 이 관찰을 식으로 쓴 것이 바로

$$\gamma S = S - 1$$

이다. 요령은 이것이 전부다: $\gamma$를 곱해도 *같은* 무한 꼬리가 그대로 재현되므로, 무한이
스스로 상쇄되고 평범한 대수만 남는다:

$$\gamma S = S - 1 \;\Rightarrow\; \gamma S - S = -1 \;\Rightarrow\; S(1 - \gamma) = 1 \;\Rightarrow\; S = \frac{1}{1-\gamma}$$

$|\gamma| < 1$ 조건이 꼬리를 0으로 줄어들게 만드는 장치다. $\gamma = 1$이면 합은 실제로
무한이고, 공식도 그에 맞게 발산한다. $\gamma = 0.5$로 검산: 공식은 $S = 1/0.5 = 2$라 하고,
손으로 더한 $1 + 0.5 + 0.25 + 0.125 + \cdots$도 실제로 $2$로 다가간다.

논문에서 실제로 보게 되는 유한 합 버전(증명은 같고 항 하나가 남는다):

$$1 + \gamma + \cdots + \gamma^{n-1} = \frac{1 - \gamma^n}{1 - \gamma}$$

**RL이 이것을 쓰는 이유.** $k$ 스텝 뒤의 보상은 가중치 $\gamma^k$로 세므로, 에이전트가 평생
모을 수 있는 가중치의 총합이 정확히 이 합, $1/(1-\gamma)$다. $\gamma = 0.99$면 $100$ — 즉
할인 없는 100 스텝을 더하고 그 뒤는 무시하는 것과 대략 같게 행동한다. 반대편에서의 확인:
$0.99^{100} \approx 0.37$이므로 100 스텝쯤이면 보상에 걸리는 가중치가 이미 3분의 1 수준으로
떨어져 있다. [[02-foundations/rl-basics|RL]]에서 말하는 "유효 지평 약 100 스텝"이 이 뜻이다.

### 6. 지수와 로그 (→ 5. 정보이론의 입장 조건)

- $e^x$: 자기 자신이 도함수인 함수; 자신에 비례하는 속도로 성장. ($e \approx 2.718$.)
- **밑이 뭔가?** $\ln$은 언제나 밑이 $e$다(*자연로그*, natural log의 n이다). $\log_2$는 밑이 2.
  밑 없는 $\log$는 보편적 약속이 없다: 이 위키와 대부분의 ML 논문에서는 밑이 $e$이고,
  정보이론에서만 단위가 **비트**라서 밑이 2다. 다행히 거의 문제가 되지 않는다 — 밑을 바꿔도
  전체에 상수가 곱해질 뿐이고(아래 셋째 규칙), 상수는 최솟값의 위치를 바꾸지 않는다.
- $\log$는 지수함수의 역함수: $\log(e^x) = x$. 정보이론 전체와 모든 우도 계산을 떠받치는 세 규칙:

| 규칙 | 왜 중요한가 |
|---|---|
| $\log(ab) = \log a + \log b$ | 확률의 곱 → 로그 확률의 **합** (손실이 합인 이유) |
| $\log(a^n) = n\log a$ | 거듭제곱이 곱셈이 된다 |
| $\log_b x = \ln x / \ln b$ | 밑 변환: 밑 2(비트)와 밑 $e$(나트)는 상수배 차이 — 그게 전부다 |

  셋째 규칙은 어디서 나오나: $y = \log_b x$라 두면 정의상 $b^y = x$다. 양변에 $\ln$을 취하면
  $y \ln b = \ln x$, 나누면 끝. 즉 $1/\ln b$는 그냥 고정된 숫자다:
  $\log_2 x = \ln x / \ln 2 \approx 1.4427\,\ln x$. 1 나트 $\approx 1.44$ 비트.
- 몸에 익힐 숫자 감각: $\log 1 = 0$; $x<1$이면 $\log x < 0$ (로그 확률은 음수다!);
  $\log$는 고통스럽게 천천히 자란다.
- **Log-sum-exp**: $\log \sum_i e^{x_i}$는 어디에나 나오고(softmax의 분모가 이것이다),
  식 그대로 계산하면 넘친다 — float64에서 $e^{800}$은 이미 $\infty$다. $x_{max} = \max_i x_i$로
  두면 해법은:

  $$\log \sum_i e^{x_i} = x_{max} + \log\sum_i e^{x_i - x_{max}}$$

  어디서 나왔나: 합에서 가장 큰 항을 묶어내면
  $\sum_i e^{x_i} = e^{x_{max}}\sum_i e^{x_i - x_{max}}$이고, 여기에 $\log$를 취한 뒤 위 표의
  $\log(ab) = \log a + \log b$를 쓴 것이다. 근사가 아니라 *정확한* 항등식이다. 왜 문제가
  풀리나: 이제 모든 지수 $x_i - x_{max}$가 $\le 0$이므로 각 $e^{(\cdot)}$가 $0$과 $1$ 사이에
  있다 — 넘칠 수가 없고, 가장 큰 항이 정확히 $1$이므로 합 전체가 0으로 가라앉지도 않는다.
  softmax+교차 엔트로피 코드가 터지지 않는 이유가 이것이다
  ([[02-foundations/calculus-backprop|2. 미적분 §4]]).

### 7. 복소수와 오일러 공식 (→ 6. 신호처리의 입장 조건)

- $j = \sqrt{-1}$; 복소수 $a + jb$는 2차원 평면의 점(가로 $a$, 세로 $b$);
  $|a+jb| = \sqrt{a^2+b^2}$가 원점으로부터의 거리, 각도는 $\theta = \operatorname{atan2}(b, a)$.
- **atan2가 뭔가**: 인자가 둘인 아크탄젠트로, 어느 언어에나 있는 함수다
  (C·파이썬·NumPy·MATLAB의 `atan2(y, x)`). 두 좌표를 *따로* 받아서 점 $(x, y)$의 각도를
  원 전체 $(-\pi, \pi]$ 범위로 돌려준다.
- **왜 $\arctan(b/a)$가 아닌가**: 먼저 나누는 순간 정보가 버려진다. $\arctan$은 $b/a$라는
  숫자 하나만 보는데, 어떤 점과 그 정반대 점의 비는 *똑같다*. 구체적으로 $(a,b) = (1,1)$과
  $(a,b) = (-1,-1)$은 둘 다 $b/a = 1$이라서 $\arctan$은 둘 다 $45°$를 준다 — 하지만 두 번째
  점은 3사분면의 $225°$($=-135°$)다. "사분면을 잃는다"가 이 뜻이다: 평면의 절반에서 답이
  정확히 $180°$만큼 틀리는데, $\arctan$에는 어느 절반이었는지 알 방법이 없다. 게다가
  $a = 0$에서 0으로 나누므로 깨지는데, 실제 각도는 지극히 평범한 $\pm 90°$다. `atan2`는 두
  부호를 모두 들고 있으므로 네 사분면과 수직축을 전부 맞힌다. 로보틱스에서 이것은 관절을
  앞으로 보내느냐 뒤로 보내느냐의 차이이고, 그래서 [[02-foundations/se3-geometry|SE(3)]]
  페이지와 모든 역기구학 구현이 atan2만 쓴다.

<svg viewBox="0 0 470 200" style="max-width:100%;height:auto" role="img" aria-label="정반대인 두 점은 b/a가 같아서 arctan이 구분하지 못한다">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="26" y1="100" x2="234" y2="100"/><line x1="130" y1="16" x2="130" y2="184"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="4 3"><line x1="48" y1="182" x2="212" y2="18"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.7"><path d="M130,100 L183,47"/><path d="M130,100 L77,153"/></g>
  <g fill="currentColor"><circle cx="185" cy="45" r="4.5"/><circle cx="75" cy="155" r="4.5"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.75"><path d="M152,100 A22,22 0 0 0 145.6,84.4"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.55"><path d="M172,100 A42,42 0 1 0 100.3,129.7"/></g>
  <g font-size="11" fill="currentColor">
    <text x="196" y="40">(1, 1)</text>
    <text x="22" y="172">(&#8722;1, &#8722;1)</text>
    <text x="152" y="88" font-size="10">45&#176;</text>
    <text x="86" y="152" font-size="10">225&#176;</text>
    <text x="255" y="44">두 점은 원점을 지나는 같은 점선 위에 있고,</text>
    <text x="255" y="62">따라서 둘 다 b/a = 1이다.</text>
    <text x="255" y="92">arctan(b/a)는 둘 다 45&#176;를 준다 &#8212; 한쪽은 맞고</text>
    <text x="255" y="110">다른 쪽은 180&#176; 틀린다.</text>
    <text x="255" y="140">atan2(b, a)는 두 부호를 따로 들고 있어</text>
    <text x="255" y="158">45&#176;와 &#8722;135&#176;를 각각 준다.</text>
  </g>
</svg>


- **오일러 공식**: $e^{j\theta} = \cos\theta + j\sin\theta$ — 각도 $\theta$의 단위원 위의 점.
  따름정리: $e^{j\theta}$를 곱하는 것 = $\theta$만큼 **회전**.
- **이것이 푸리에 분석을 작동하게 하는 이유.** 세 단계인데, 셋째가 전부다.
  1. *사인파는 회전을 옆에서 본 것이다.* $t$가 흐르면 $e^{j\omega t}$는 초당 $\omega$ 라디안씩
     단위원을 도는 점이다. 그 실수부 — 가로축에 드리운 그림자 — 가 $\cos\omega t$다. 즉
     코사인은 회전과 다른 종류의 대상이 아니라, 같은 대상을 옆에서 본 것이다.
  2. *"내 신호에 주파수 $\omega$가 얼마나 들었나"를 물으려면, 반대로 돌려서 평균 내라.*
     신호에 $e^{-j\omega t}$(같은 속도로 반대 방향으로 도는 회전)를 곱하고 시간에 대해
     평균한다. 신호가 정말 그 주파수를 담고 있다면 반대 회전이 그 성분의 회전을 상쇄해
     제자리에 붙들어 두므로 평균이 0이 아닌 값으로 남는다. 담고 있지 않다면 곱은 계속
     돌면서 모든 방향을 고르게 훑고, 평균이 0이 된다.
  3. *이 "곱하고 평균 내기"가 곧 내적이다* — [[02-foundations/linear-algebra|1. 선형대수 §1]]의
     $\langle a,b\rangle$와 같은 연산, 즉 한 벡터가 다른 벡터 방향으로 얼마나 누워 있는지를
     재는 그 연산이다. 각 회전과의 겹침을 재는 것이 곧 신호를 그 회전 위로 투영하는 것이다.
     "사인파로 분해"의 뜻은 이게 전부다.

  그래서 [[02-foundations/signal-processing|6. 신호처리]]의 DFT 공식
  $X[k] = \sum_n x[n]\,e^{-j2\pi kn/N}$에는 숨은 내용이 없다: $e^{-j(\cdot)}$가 2단계의 반대
  회전이고, $\sum_n$이 평균이다. 주파수 하나당 내적 하나일 뿐이다.

<svg viewBox="0 0 470 205" style="max-width:100%;height:auto" role="img" aria-label="단위원 위를 도는 점과, 실수축에 드리운 그림자가 그리는 코사인">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="20" y1="90" x2="150" y2="90"/><line x1="85" y1="25" x2="85" y2="155"/></g>
  <circle cx="85" cy="90" r="52" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.7" fill="none"><line x1="85" y1="90" x2="118.4" y2="50.2"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.65" stroke-dasharray="4 3"><line x1="118.4" y1="50.2" x2="118.4" y2="90"/></g>
  <g fill="currentColor"><circle cx="118.4" cy="50.2" r="4"/><circle cx="118.4" cy="90" r="3"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.8"><path d="M105,90 A20,20 0 0 0 97.9,74.7"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="175" y1="90" x2="440" y2="90"/></g>
  <path d="M175.0 45.0L176.3 45.0L177.6 45.1L178.9 45.2L180.2 45.4L181.5 45.6L182.8 45.8L184.1 46.1L185.4 46.4L186.7 46.8L188.0 47.2L189.3 47.7L190.6 48.2L191.9 48.7L193.2 49.3L194.5 49.9L195.8 50.6L197.1 51.3L198.4 52.0L199.7 52.8L201.0 53.6L202.3 54.4L203.6 55.3L204.9 56.2L206.2 57.2L207.5 58.2L208.8 59.2L210.1 60.2L211.4 61.3L212.7 62.4L214.0 63.5L215.3 64.7L216.6 65.9L217.9 67.1L219.2 68.3L220.5 69.6L221.8 70.8L223.1 72.1L224.4 73.4L225.7 74.8L227.0 76.1L228.3 77.4L229.6 78.8L230.9 80.2L232.2 81.6L233.5 83.0L234.8 84.4L236.1 85.8L237.4 87.2L238.7 88.6L240.0 90.0L241.3 91.4L242.6 92.8L243.9 94.2L245.2 95.6L246.5 97.0L247.8 98.4L249.1 99.8L250.4 101.2L251.7 102.6L253.0 103.9L254.3 105.2L255.6 106.6L256.9 107.9L258.2 109.2L259.5 110.4L260.8 111.7L262.1 112.9L263.4 114.1L264.7 115.3L266.0 116.5L267.3 117.6L268.6 118.7L269.9 119.8L271.2 120.8L272.5 121.8L273.8 122.8L275.1 123.8L276.4 124.7L277.7 125.6L279.0 126.4L280.3 127.2L281.6 128.0L282.9 128.7L284.2 129.4L285.5 130.1L286.8 130.7L288.1 131.3L289.4 131.8L290.7 132.3L292.0 132.8L293.3 133.2L294.6 133.6L295.9 133.9L297.2 134.2L298.5 134.4L299.8 134.6L301.1 134.8L302.4 134.9L303.7 135.0L305.0 135.0L306.3 135.0L307.6 134.9L308.9 134.8L310.2 134.6L311.5 134.4L312.8 134.2L314.1 133.9L315.4 133.6L316.7 133.2L318.0 132.8L319.3 132.3L320.6 131.8L321.9 131.3L323.2 130.7L324.5 130.1L325.8 129.4L327.1 128.7L328.4 128.0L329.7 127.2L331.0 126.4L332.3 125.6L333.6 124.7L334.9 123.8L336.2 122.8L337.5 121.8L338.8 120.8L340.1 119.8L341.4 118.7L342.7 117.6L344.0 116.5L345.3 115.3L346.6 114.1L347.9 112.9L349.2 111.7L350.5 110.4L351.8 109.2L353.1 107.9L354.4 106.6L355.7 105.2L357.0 103.9L358.3 102.6L359.6 101.2L360.9 99.8L362.2 98.4L363.5 97.0L364.8 95.6L366.1 94.2L367.4 92.8L368.7 91.4L370.0 90.0L371.3 88.6L372.6 87.2L373.9 85.8L375.2 84.4L376.5 83.0L377.8 81.6L379.1 80.2L380.4 78.8L381.7 77.4L383.0 76.1L384.3 74.8L385.6 73.4L386.9 72.1L388.2 70.8L389.5 69.6L390.8 68.3L392.1 67.1L393.4 65.9L394.7 64.7L396.0 63.5L397.3 62.4L398.6 61.3L399.9 60.2L401.2 59.2L402.5 58.2L403.8 57.2L405.1 56.2L406.4 55.3L407.7 54.4L409.0 53.6L410.3 52.8L411.6 52.0L412.9 51.3L414.2 50.6L415.5 49.9L416.8 49.3L418.1 48.7L419.4 48.2L420.7 47.7L422.0 47.2L423.3 46.8L424.6 46.4L425.9 46.1L427.2 45.8L428.5 45.6L429.8 45.4L431.1 45.2L432.4 45.1L433.7 45.0L435.0 45.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.65" stroke-dasharray="4 3"><line x1="211.1" y1="61.1" x2="211.1" y2="90"/></g>
  <g fill="currentColor"><circle cx="211.1" cy="61.1" r="4"/></g>
  <g font-size="11" fill="currentColor">
    <text x="124.4" y="44.2">e^(j&#952;)</text>
    <text x="102" y="86" font-size="10">&#952;</text>
    <text x="96" y="162" font-size="10">Re = cos &#952;</text>
    <text x="176" y="18">&#952;가 한 바퀴 도는 동안의 cos &#952;</text>
    <text x="416" y="106" font-size="10">&#952;</text>
    <text x="20" y="184" opacity="0.9">오른쪽 파형은 별개의 대상이 아니다 &#8212; 점이 도는 동안 왼쪽 그림의 그림자를 옮겨 그린 것이다.</text>
    <text x="20" y="199" opacity="0.9">&#8220;사인파로 분해&#8221;와 &#8220;회전들에 투영&#8221;이 같은 문장인 이유가 이것이다.</text>
  </g>
</svg>



### 8. 선형 미분방정식 (→ 제어 트랙 5~7번)

물리 시스템은 미분방정식으로 기술된다 — 제어 전체의 모델링 언어이며, [[04-robotics/control-theory-ce397|5. 제어 이론 §2–4]]가 이것을 그대로 이어받는다.

- **1차**: $\dot x = ax$의 해는 $x(t) = x(0)\,e^{at}$. 이걸 믿기 위해 방정식을 풀 필요는 없다 —
  후보를 미분해서 확인만 하면 된다: $\frac{d}{dt}\big(x(0)e^{at}\big) = a\,x(0)e^{at} = a\,x(t)$ ✓,
  그리고 $t=0$에서 $x(0)$ ✓. 6절의 "$e$는 자기 자신이 도함수인 함수"를 물리 시스템에 적용한
  것이 내용의 전부다. 모든 것이 이 한 사실에서 나온다:
  $a < 0$이면 감쇠(안정), $a > 0$이면 폭발(불안정). 로봇 관절, 데워지는 방, 빠지는 물탱크
  — 전부 국소적으로 이 방정식이다.
- **입력이 있으면**: $\dot x = ax + bu$ — 해는 "감쇠한 초기 상태 + 누적된 입력";
  상태공간 모델 $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$
  ([[02-foundations/linear-algebra|선형대수 §5]])의 스칼라판이고, $e^{at}$는 행렬 지수
  $e^{At}$가 되며 고유값이 $a$의 역할을 한다.
- **2차**: $\ddot x + 2\zeta\omega_n \dot x + \omega_n^2 x = 0$ — 질량-스프링-댐퍼.
  모든 응답을 두 숫자가 기술한다: 고유 진동수 $\omega_n$(얼마나 빨리 진동하나)과 감쇠비
  $\zeta$(울리는가: $\zeta<1$이면 진동, $\zeta \ge 1$이면 안 함). 로봇 팔과 서스펜션이
  이 어휘로 튜닝된다.
- 이산 시간 (코드가 실제로 도는 곳): $x_{t+1} = a x_t$ ⇒ $x_t = a^t x_0$ — $|a| < 1$일
  때만 안정. 연속과 이산의 조건($\text{Re}(a) < 0$ vs $|a_d| < 1$)은 같은 말이고, 다리는
  이것이다: $\dot x = ax$를 $\Delta t$마다 샘플링하면 $x_{t+1} = e^{a\Delta t}x_t$이므로 이산
  계수가 $a_d = e^{a\Delta t}$다. 그런데 $|e^{a\Delta t}| = e^{\text{Re}(a)\Delta t}$이므로, 이
  크기가 $1$보다 작을 조건이 정확히 $\text{Re}(a) < 0$이다. 좌반평면이 단위원 *안으로
  사상된다* — 하나의 이야기를 두 좌표계로 쓴 것이다.

### 9. 라플라스 변환과 s-평면 (→ 제어 트랙, 6. 신호처리 §5)

라플라스 변환은 미분방정식을 대수로 바꾼다 — 그리고 [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]가 그 극점 그림을 논문이 인용하는 정착 시간·오버슈트 숫자로 바꾼다:

- 정의: $F(s) = \int_0^\infty f(t)\,e^{-st}\,dt$; 중요한 성질은 하나:
  **미분이 $s$ 곱하기가 된다** — $\mathcal{L}[\dot f] = sF(s) - f(0)$.
- 따름정리: 미분방정식이 다항 방정식이 되고, 시스템이 **전달함수**
  $G(s) = \frac{\text{출력}(s)}{\text{입력}(s)}$가 된다 — 예: $\dot x = ax + u$이면
  $G(s) = \frac{1}{s - a}$.
- **극점** = 분모의 근 = 8절의 $a$들 = 상태공간 $A$의 고유값. 복소 **s-평면**에 그리면:
  - 좌반평면(실수부 음수) → 감쇠 → **안정**
  - 우반평면 → 성장 → **불안정**
  - 허수부 → 진동 주파수; 축에서의 거리 → 감쇠 속도

<svg viewBox="0 0 430 212" style="max-width:100%;height:auto" role="img" aria-label="s-평면: 극점 위치와 그 의미">
  <g fill="currentColor" opacity="0.07"><rect x="20" y="15" width="195" height="160"/></g>
  <g stroke="currentColor" stroke-width="1.3"><line x1="20" y1="103" x2="410" y2="103"/><line x1="215" y1="15" x2="215" y2="190"/></g>
  <g fill="currentColor">
    <path d="M112,58 l6,6 l-6,6 l-6,-6 z"/><path d="M112,142 l6,6 l-6,6 l-6,-6 z"/>
    <path d="M64,97 l6,6 l-6,6 l-6,-6 z"/>
    <path d="M312,71 l6,6 l-6,6 l-6,-6 z"/><path d="M312,129 l6,6 l-6,6 l-6,-6 z"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity="0.6">
    <line x1="112" y1="64" x2="215" y2="103"/><line x1="112" y1="64" x2="112" y2="103"/>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="26" y="32">좌반평면 = 안정</text><text x="250" y="32">우반평면 = 불안정</text>
    <text x="386" y="120">Re</text><text x="222" y="26">Im</text>
    <text x="124" y="56" font-size="10.5" opacity="0.9">복소 켤레쌍</text>
    <text x="26" y="90" font-size="10.5" opacity="0.9">실수 극점</text>
    <text x="26" y="192" font-size="11" opacity="0.85">복소 켤레쌍 = 감쇠 진동 &#183; 실수 극점 = 순수 감쇠</text>
    <text x="26" y="206" font-size="11" opacity="0.85">왼쪽일수록 빨리 감쇠 &#183; 실수축에서 멀수록 빨리 진동</text>
  </g>
</svg>


- [[02-foundations/engineering-math|§7]]의 복소평면이 제어에서 중요한 이유가 이것이다:
  *시스템의 정성적 거동 전체가 그림 하나 — 극점이 어디에 앉아 있는가 — 다.* 주파수 응답은
  $G(j\omega)$ — 허수축 위에서 평가하면 [[02-foundations/signal-processing|신호처리]]의
  필터가 복원된다. (이산 시간의 쌍둥이: Z-변환, 좌반평면 대신 단위원.)

### 10. 표기법 사전 (전 페이지 공용)

정식 도입 전에 어디서나 쓰이는 정의 둘:

- **Softmax**는 임의의 점수 벡터를 확률분포로 바꾼다:
  $\text{softmax}(z)_i = e^{z_i} / \sum_j e^{z_j}$ — 양수이고 합이 1이며, 가장 큰 점수가
  가장 큰 확률을 받는다(매끄러운 $\arg\max$). 어텐션, 분류 손실, 정책 어디에나 나온다.
- **집합 표기**: $x \in A$("$x$가 $A$에 속함"), $A \cap B$(둘 다), $A \cup B$(어느 쪽이든),
  $\Omega$(모든 결과의 집합), disjoint = 겹침 없음. 확률 페이지가 첫 줄부터 쓴다.

| 기호 | 읽는 법 |
|---|---|
| $\sum_i$, $\prod_i$ | 인덱스 $i$에 대한 합 / 곱 |
| $\arg\max_x f(x)$ | $f$를 최대화하는 $x$ (최댓값 자체가 아니라) |
| $E[\cdot]$, $\text{Var}(\cdot)$ | 기댓값, 분산 |
| $x \sim p$ | $x$를 분포 $p$에서 샘플링 |
| $\propto$ | 비례 (상수배를 무시하면 같음) |
| $\|x\|$ | $x$의 노름(길이) |
| $\mathbb{1}[\cdot]$ | 지시 함수: 참이면 1, 거짓이면 0 |
| $\odot$ | 원소별 곱 |
| $:=$ | ~로 정의함 |
| $A^\top$ | 전치 — 대각선을 기준으로 뒤집기 ($A^\top_{ij} = A_{ji}$) |
| $\det A$ | 행렬식 — 사상이 부피를 몇 배로 만드는가; $0$이면 공간을 납작하게 뭉개므로 역행렬이 없다 |
| $A \succeq 0$, $A \succ 0$ | 양의 준정부호/정부호 — 행렬판 "$\ge 0$"/"$>0$": 모든 $x$에 대해 $x^\top A x \ge 0$ |

### 스스로 점검

1. $f(x) = \log(1 + e^x)$ (softplus)를 연쇄 법칙으로 미분하고, 결과가 시그모이드임을 보여라.
2. 기하급수 합으로, $\gamma = 0.99$인 에이전트에게 200 스텝 뒤의 보상이 거의 안 보이는
   이유를 설명하라.
3. 곱 규칙에서 $\log \frac{a}{b} = \log a - \log b$를 유도하라.
4. 오일러 공식으로 $e^{j\pi}$를 계산하고, 그 결과를 회전으로 해석하라.
5. (§8) 어떤 관절이 $\dot x = -3x$를 따른다. 안정한가? $x(0)=2$에서 $x(t)$는? 대략 언제 시작값의 ~5%로 감쇠하나?
6. (§9) 시스템 $\dot x = -3x + u$의 전달함수는 $G(s) = \frac{1}{s+3}$이다. 극점은 어디이고 어느 반평면이며, 그것이 안정성에 대해 무엇을 말하나?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $f'(x) = \frac{e^x}{1+e^x} = \frac{1}{1+e^{-x}} = \sigma(x)$ — softplus의 미분이 시그모이드.
> 2. 200스텝 뒤 보상의 가중치는 $\gamma^{200} = 0.99^{200} \approx 0.13$ — 유효 지평(100스텝)의 두 배 거리라 이미 $1/e^2$ 수준으로 희미하고, 400스텝이면 사실상 0이다.
> 3. $\log\frac{a}{b} = \log(a \cdot b^{-1}) = \log a + \log b^{-1} = \log a - \log b$.
> 4. $e^{j\pi} = \cos\pi + j\sin\pi = -1$ — 180° 회전이 1을 $-1$로 보낸다.
> 5. 안정($a=-3<0$). $x(t) = 2e^{-3t}$; ~5%는 $e^{-3t}\approx 0.05 \Rightarrow 3t\approx 3 \Rightarrow t\approx 1$초.
> 6. 극점 $s=-3$ — 좌반평면(음의 실수부)이라 **안정**; 이 극점이 곧 §8의 $a=-3$이자 1차원 상태공간 $A$의 고유값이다.
