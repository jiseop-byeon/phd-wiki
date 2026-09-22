---
title: 6. Signal Processing
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]] · [[02-foundations/engineering-math|0.5 §7]] (complex numbers, Euler's formula) · [[02-foundations/engineering-math|0.5 §9]] (Laplace, poles) · [[02-foundations/linear-algebra|1. Linear Algebra §3, §5]] (eigenvectors, for §3's diagonalizing basis; controllability and observability, for §5) · [[02-foundations/probability|3. Probability §5]] (white noise, stationarity)
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3** · [[02-foundations/engineering-math|0.5 §7]](복소수·오일러 공식) · [[02-foundations/engineering-math|0.5 §9]](라플라스·극점) · [[02-foundations/linear-algebra|1. 선형대수 §3, §5]](고유벡터, §3의 대각화 기저용; 가제어성과 가관측성, §5용) · [[02-foundations/probability|3. 확률 §5]](백색 잡음·정상성)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/probability|3. Probability]] and Euler's formula from [[02-foundations/engineering-math|0.5]]. A domain bridge: from here the data stops being given
and starts arriving from a sensor. Its order against [[02-foundations/rl-basics|7. RL Basics]] is free.*

Every sensor a construction robot carries — camera, LiDAR, IMU, encoder — hands you a
sampled, noisy signal. Course-depth treatment: convolution worked by hand, the sampling
theorem with its math, DFT/FFT, filter design basics, and the bridge to control's transfer
functions.

> [!note] First pass · 처음이라면
> Read the picture, §1, §2 — the sampling contract, aliasing and the zero-order hold are what actually bite — then §6 for the field habits. §2's four-step proof of the sampling theorem is a second pass. §3 to §5 are the machinery; open them when a paper does something in the frequency domain.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 432" style="max-width:100%;height:auto" role="img" aria-label="plant P3 on its 1 kHz servo: handle, ideal sampler, zero-order hold and wall law in a row; below, the handle position, its eight samples and the hold's staircase against the wall, on a grid one encoder count tall">
  <defs><marker id="arSp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <rect x="12" y="33" width="66" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="45.0" y="47.0" fill="currentColor" text-anchor="middle">handle</text>
  <text x="45.0" y="61.0" fill="currentColor" text-anchor="middle" opacity="0.85">P3</text>
  <line x1="78" y1="50" x2="124" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSp)"/>
  <text x="101.0" y="43.0" fill="currentColor" text-anchor="middle">x(t)</text>
  <g fill="currentColor"><circle cx="128" cy="50" r="2.6"/><circle cx="164" cy="50" r="2.6"/></g>
  <line x1="128" y1="50" x2="160" y2="36" stroke="currentColor" stroke-width="1.8"/>
  <path d="M150 30 A 14 14 0 0 1 162 43" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" marker-end="url(#arSp)"/>
  <text x="146.0" y="23.0" fill="currentColor" text-anchor="middle">ideal sampler</text>
  <text x="146.0" y="72.0" fill="currentColor" text-anchor="middle" opacity="0.9">closes every T = 1 ms</text>
  <text x="146.0" y="86.0" fill="currentColor" text-anchor="middle" opacity="0.9">f<tspan dy="3" font-size="11">s</tspan><tspan dx="3.3" dy="-3">= 1000 Hz</tspan></text>
  <text x="146.0" y="100.0" fill="currentColor" text-anchor="middle" opacity="0.9">Nyquist 500 Hz</text>
  <line x1="167" y1="50" x2="250" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSp)"/>
  <text x="208.0" y="43.0" fill="currentColor" text-anchor="middle">x[n] = x(nT)</text>
  <rect x="252" y="33" width="64" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="258,60 270,60 270,53 282,53 282,46 294,46 294,40 310,40" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="284.0" y="23.0" fill="currentColor" text-anchor="middle">zero-order hold</text>
  <text x="284.0" y="86.0" fill="currentColor" text-anchor="middle" opacity="0.9">holds x[n] on [nT, (n+1)T),</text>
  <text x="284.0" y="100.0" fill="currentColor" text-anchor="middle" opacity="0.9">then jumps</text>
  <line x1="316" y1="50" x2="410" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSp)"/>
  <text x="362.0" y="43.0" fill="currentColor" text-anchor="middle">held x</text>
  <rect x="412" y="33" width="136" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="480.0" y="47.0" fill="currentColor" text-anchor="middle">wall law</text>
  <text x="480.0" y="61.0" fill="currentColor" text-anchor="middle">F = −k<tspan dy="3" font-size="11">w</tspan><tspan dy="-3">(x − x</tspan><tspan dy="3" font-size="11">w</tspan><tspan dy="-3">)</tspan></text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.18"><line x1="60" y1="306.0" x2="364" y2="306.0"/><line x1="60" y1="262.0" x2="364" y2="262.0"/><line x1="60" y1="218.0" x2="364" y2="218.0"/><line x1="60" y1="174.0" x2="364" y2="174.0"/><line x1="60" y1="130.0" x2="364" y2="130.0"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none"><line x1="60" y1="124.0" x2="60" y2="334.0"/><line x1="60" y1="334.0" x2="368" y2="334.0"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="60.0" y1="334.0" x2="60.0" y2="338.0"/><line x1="98.0" y1="334.0" x2="98.0" y2="338.0"/><line x1="136.0" y1="334.0" x2="136.0" y2="338.0"/><line x1="174.0" y1="334.0" x2="174.0" y2="338.0"/><line x1="212.0" y1="334.0" x2="212.0" y2="338.0"/><line x1="250.0" y1="334.0" x2="250.0" y2="338.0"/><line x1="288.0" y1="334.0" x2="288.0" y2="338.0"/><line x1="326.0" y1="334.0" x2="326.0" y2="338.0"/><line x1="364.0" y1="334.0" x2="364.0" y2="338.0"/></g>
  <text x="60.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">0</text>
  <text x="98.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">1</text>
  <text x="136.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">2</text>
  <text x="174.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">3</text>
  <text x="212.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">4</text>
  <text x="250.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">5</text>
  <text x="288.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">6</text>
  <text x="326.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">7</text>
  <text x="364.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">8</text>
  <text x="364.0" y="364.0" fill="currentColor" text-anchor="end" opacity="0.8">t (ms)</text>
  <line x1="99.0" y1="360.0" x2="135.0" y2="360.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <line x1="135.0" y1="360.0" x2="99.0" y2="360.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <text x="142.0" y="364.0" fill="currentColor">T = 1 ms: the clock</text>
  <line x1="60" y1="221.3" x2="372" y2="221.3" stroke="currentColor" stroke-width="1.6" stroke-dasharray="7 4"/>
  <text x="378.0" y="225.3" fill="currentColor">x<tspan dy="3" font-size="11">w</tspan><tspan dx="3.3" dy="-3">= 0.030 m</tspan></text>
  <path d="M60.0 308.2L61.9 307.4L63.8 306.7L65.7 305.9L67.6 305.2L69.5 304.4L71.4 303.6L73.3 302.8L75.2 302.0L77.1 301.2L79.0 300.4L80.9 299.6L82.8 298.8L84.7 298.0L86.6 297.1L88.5 296.3L90.4 295.5L92.3 294.6L94.2 293.7L96.1 292.9L98.0 292.0L99.9 291.1L101.8 290.2L103.7 289.4L105.6 288.5L107.5 287.6L109.4 286.6L111.3 285.7L113.2 284.8L115.1 283.9L117.0 283.0L118.9 282.0L120.8 281.1L122.7 280.1L124.6 279.2L126.5 278.2L128.4 277.3L130.3 276.3L132.2 275.3L134.1 274.3L136.0 273.3L137.9 272.4L139.8 271.4L141.7 270.4L143.6 269.4L145.5 268.4L147.4 267.4L149.3 266.3L151.2 265.3L153.1 264.3L155.0 263.3L156.9 262.3L158.8 261.2L160.7 260.2L162.6 259.2L164.5 258.1L166.4 257.1L168.3 256.0L170.2 255.0L172.1 253.9L174.0 252.8L175.9 251.8L177.8 250.7L179.7 249.7L181.6 248.6L183.5 247.5L185.4 246.4L187.3 245.4L189.2 244.3L191.1 243.2L193.0 242.1L194.9 241.0L196.8 240.0L198.7 238.9L200.6 237.8L202.5 236.7L204.4 235.6L206.3 234.5L208.2 233.4L210.1 232.3L212.0 231.2L213.9 230.1L215.8 229.0L217.7 227.9L219.6 226.8L221.5 225.7L223.4 224.6L225.3 223.5L227.2 222.4L229.1 221.3L231.0 220.2L232.9 219.1L234.8 218.0L236.7 216.9L238.6 215.8L240.5 214.7L242.4 213.7L244.3 212.6L246.2 211.5L248.1 210.4L250.0 209.3L251.9 208.2L253.8 207.1L255.7 206.0L257.6 204.9L259.5 203.8L261.4 202.7L263.3 201.6L265.2 200.6L267.1 199.5L269.0 198.4L270.9 197.3L272.8 196.2L274.7 195.2L276.6 194.1L278.5 193.0L280.4 192.0L282.3 190.9L284.2 189.8L286.1 188.8L288.0 187.7L289.9 186.7L291.8 185.6L293.7 184.6L295.6 183.5L297.5 182.5L299.4 181.5L301.3 180.4L303.2 179.4L305.1 178.4L307.0 177.4L308.9 176.3L310.8 175.3L312.7 174.3L314.6 173.3L316.5 172.3L318.4 171.3L320.3 170.3L322.2 169.3L324.1 168.4L326.0 167.4L327.9 166.4L329.8 165.4L331.7 164.5L333.6 163.5L335.5 162.6L337.4 161.6L339.3 160.7L341.2 159.7L343.1 158.8L345.0 157.9L346.9 157.0L348.8 156.0L350.7 155.1L352.6 154.2L354.5 153.3L356.4 152.4L358.3 151.6L360.2 150.7L362.1 149.8L364.0 148.9" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.75"/>
  <polyline points="60.0,308.2 98.0,308.2 98.0,292.0 136.0,292.0 136.0,273.3 174.0,273.3 174.0,252.8 212.0,252.8 212.0,231.2 250.0,231.2 250.0,209.3 288.0,209.3 288.0,187.7 326.0,187.7 326.0,167.4 364.0,167.4" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="98.0,292.0 99.9,291.1 101.8,290.2 103.7,289.4 105.6,288.5 107.5,287.6 109.4,286.6 111.3,285.7 113.2,284.8 115.1,283.9 117.0,283.0 118.9,282.0 120.8,281.1 122.7,280.1 124.6,279.2 126.5,278.2 128.4,277.3 130.3,276.3 132.2,275.3 134.1,274.3 136.0,273.3 136.0,292.0 98.0,292.0" fill="currentColor" fill-opacity="0.28" stroke="none"/>
  <line x1="118.9" y1="285.0" x2="94.2" y2="146.7" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="66.0" y="128.7" fill="currentColor">hold late by T/2 = 0.5 ms</text>
  <text x="66.0" y="142.7" fill="currentColor" opacity="0.85">on average (§2: phase lag)</text>
  <g fill="currentColor"><circle cx="60.0" cy="308.2" r="3.3"/><circle cx="98.0" cy="292.0" r="3.3"/><circle cx="136.0" cy="273.3" r="3.3"/><circle cx="174.0" cy="252.8" r="3.3"/><circle cx="212.0" cy="231.2" r="3.3"/><circle cx="250.0" cy="209.3" r="3.3"/><circle cx="288.0" cy="187.7" r="3.3"/><circle cx="326.0" cy="167.4" r="3.3"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.4"><path d="M60.0 301.0L65.0 306.0L60.0 311.0L55.0 306.0z"/><path d="M98.0 301.0L103.0 306.0L98.0 311.0L93.0 306.0z"/><path d="M136.0 257.0L141.0 262.0L136.0 267.0L131.0 262.0z"/><path d="M174.0 257.0L179.0 262.0L174.0 267.0L169.0 262.0z"/><path d="M212.0 213.0L217.0 218.0L212.0 223.0L207.0 218.0z"/><path d="M250.0 213.0L255.0 218.0L250.0 223.0L245.0 218.0z"/><path d="M288.0 169.0L293.0 174.0L288.0 179.0L283.0 174.0z"/><path d="M326.0 169.0L331.0 174.0L326.0 179.0L321.0 174.0z"/></g>
  <ellipse cx="269.0" cy="209.3" rx="26" ry="9" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="229.1" y1="214.3" x2="229.1" y2="228.3" stroke="currentColor" stroke-width="1.8"/>
  <line x1="227.1" y1="213.3" x2="189.2" y2="185.0" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="187.3" y="183.0" fill="currentColor" text-anchor="end">true crossing</text>
  <line x1="271.0" y1="218.3" x2="285.0" y2="269.8" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="185.4" y="281.8" fill="currentColor">contact begins at a tick (5 ms),</text>
  <text x="185.4" y="295.8" fill="currentColor" opacity="0.85">not at the true crossing</text>
  <line x1="372" y1="131.0" x2="372" y2="173.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <line x1="372" y1="173.0" x2="372" y2="131.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <text x="380.0" y="140.0" fill="currentColor" opacity="1">Δx = 61.4 μm:</text>
  <text x="380.0" y="154.0" fill="currentColor" opacity="0.9">one encoder count</text>
  <text x="380.0" y="172.0" fill="currentColor" opacity="1">k<tspan dy="3" font-size="11">w</tspan><tspan dy="-3">·Δx = 400 × 61.4 μm</tspan></text>
  <text x="380.0" y="186.0" fill="currentColor" opacity="0.9">= 0.025 N, the smallest</text>
  <text x="380.0" y="200.0" fill="currentColor" opacity="0.9">force step in the wall</text>
  <line x1="378" y1="260.0" x2="392" y2="260.0" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.75"/>
  <circle cx="385" cy="274.0" r="3.3" fill="currentColor"/>
  <polyline points="378,292.0 385,292.0 385,284.0 392,284.0" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <path d="M385 297.0L390 302.0L385 307.0L380 302.0z" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="398.0" y="264.0" fill="currentColor" opacity="0.9">x(t), 30 Hz</text>
  <text x="398.0" y="278.0" fill="currentColor" opacity="0.9">x[n] = x(nT)</text>
  <text x="398.0" y="292.0" fill="currentColor" opacity="0.9">ZOH output</text>
  <text x="398.0" y="306.0" fill="currentColor" opacity="0.9">x[n] snapped to a count</text>
  <text x="14.0" y="394.0" fill="currentColor" opacity="1">Where the grids meet: Δx/T = 61.4 mm/s gives one new count per tick.</text>
  <text x="14.0" y="408.0" fill="currentColor" opacity="0.95">This x(t) never exceeds 30.7 mm/s, so every other tick reports no motion,</text>
  <text x="14.0" y="422.0" fill="currentColor" opacity="0.95">and a velocity from differenced positions reads 0, then 61.4 mm/s.</text>
</svg>

Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]], the haptic handle on its $1\,\mathrm{kHz}$ servo: the ideal sampler reads $x[n]=x(nT)$ every $T=1\,\mathrm{ms}$ (Nyquist $500\,\mathrm{Hz}$; §2), and the zero-order hold (defined and derived in §2) turns the samples into a staircase that runs $T/2=0.5\,\mathrm{ms}$ late on average, so contact with the wall at $x_w=0.030\,\mathrm{m}$ begins at a tick ($5\,\mathrm{ms}$), not at the true crossing. The faint horizontal grid is one encoder count, $\Delta x=61.4\,\mu\mathrm{m}$; inside the wall one count is worth $k_w\,\Delta x=0.025\,\mathrm{N}$, the smallest force step. The two grids meet at $\Delta x/T=61.4\,\mathrm{mm/s}$, one new count per tick; this handle never moves faster than $30.7\,\mathrm{mm/s}$, so every other tick reports no motion and a velocity from differenced positions reads $0$, then $61.4\,\mathrm{mm/s}$.

### 1. Signals, systems, and convolution

- A **system** $T$ is a rule that turns an input sequence $x[n]$ into an output sequence
  $y[n] = T\{x\}[n]$, where $n$ is the integer sample index. A system is **LTI** (linear,
  time-invariant) when it has **two** properties, and each can fail without the other.
- **Linearity** is additivity *and* homogeneity together, i.e. superposition (the full
  definition, with non-examples, is [[02-foundations/engineering-math|0.5 §4.5]]). For all
  inputs $x_1, x_2$ and all scalars $a, b$:
  $$T\{a x_1[n] + b x_2[n]\} = a\,T\{x_1[n]\} + b\,T\{x_2[n]\}$$
  so a weighted sum of inputs comes out as the same weighted sum of outputs.
  *Non-example:* the squarer $y[n] = x[n]^2$. Constant inputs $1$ and $2$ give outputs $1$
  and $4$, but their sum $3$ gives $9 \ne 1 + 4 = 5$.
- **Time invariance** (shift invariance): delaying the input by $n_0$ samples only delays
  the output by the same $n_0$,
  $$x[n] \mapsto y[n] \implies x[n-n_0] \mapsto y[n-n_0]$$
  where $\mapsto$ reads "the system turns this input into this output" and $n_0$ is any
  integer shift. It holds when the rule never looks at the clock, since then an input that
  arrives later is treated exactly as it would have been earlier. *Non-example:* the ramp
  gain $y[n] = n\,x[n]$ is linear but not time-invariant, because an impulse at $n = 0$
  produces the all-zero output while the same impulse at $n = 1$ produces $1$ at $n = 1$,
  which is not a shifted zero.
- *Example that passes both:* the running sum $y[n] = x[n] + x[n-1]$. Adding or scaling
  inputs adds or scales both terms, so it is linear; it only refers to $n$ and $n-1$, so a
  delayed input gives a delayed output.
- The **unit impulse** is $\delta[n] = 1$ at $n = 0$ and $0$ everywhere else, and the
  **impulse response** is what the system does to it, $h[n] = T\{\delta\}[n]$. For the
  running sum, $h = [1, 1]$.
- **The consequence.** An LTI system is completely characterized by its impulse
  response $h$; the output is the **convolution** of the input with $h$:
  $$y[n] = (x * h)[n] = \sum_k x[k]\, h[n-k]$$
  Here $k$ runs over every input sample, $x[k]$ is the input at time $k$, and $h[n-k]$ is
  the response to that one sample, delayed so it starts at $k$. So convolution is an
  operation that takes two sequences and returns a third: the sum of delayed copies of $h$,
  each scaled by one input sample.
- **Where that comes from — convolution is not a definition, it is forced.** Three lines.
  First, any signal is a sum of shifted impulses, which is a tautology:
  $x[n] = \sum_k x[k]\,\delta[n-k]$. Push it through the system $T$ and use *linearity* to
  move $T$ inside the sum: $y[n] = T\{\sum_k x[k]\delta[n-k]\} = \sum_k x[k]\,T\{\delta[n-k]\}$.
  Now use *time-invariance*: the response to an impulse at $k$ is the response to an impulse
  at $0$, shifted — $T\{\delta[n-k]\} = h[n-k]$. Substitute and you have the formula above.
  So the sum is not a modelling choice: **if a system is linear and time-invariant then it
  convolves, and there is nothing else it could do.** That is also why one measurement — the
  impulse response — determines the system completely, and why the whole frequency-domain
  toolkit exists: convolution is the only operation there is to diagonalize.
- Worked example: $x = [1, 2, 3]$, $h = [1, 1]$ (a running sum):
  $y = [1,\ 1{+}2,\ 2{+}3,\ 3] = [1, 3, 5, 3]$ — flip, slide, multiply, accumulate.
  Length: $N_x + N_h - 1$.
- A CNN layer is a *learned bank* of such $h$'s in 2D (plus nonlinearity; frameworks
  actually compute cross-correlation — convolution without the kernel flip,
  $(x \star h)[n] = \sum_k x[n+k]\,h[k]$ — but since the
  kernel is learned the distinction is immaterial, and papers say "convolution" by convention) —
  [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] onward; "padding/stride" are the boundary and
  sampling choices of this same operation.
- Key properties: commutative ($x * h = h * x$), associative
  ($(x * h_1) * h_2 = x * (h_1 * h_2)$, so cascaded LTI systems = one convolved $h$),
  and the delta is the identity ($x * \delta = x$).
- **Causality** is a system property: the output at time $n$ may use only present and past
  inputs $x[k]$ with $k \le n$. For an LTI system it is one condition on the impulse response,
  $$h[n] = 0 \quad \text{for all } n < 0$$
  because a nonzero $h[-1]$ would let the input at $n+1$ reach the output at $n$. The running
  sum is causal; the centered average $y[n] = \tfrac12\big(x[n+1] + x[n-1]\big)$ is not, since
  it needs the next sample. Only causal filters can run in real time, which is where the phase
  lag of §4 comes from.
- **BIBO stability** (bounded input, bounded output) is a system property too: every input
  with $|x[n]| \le B_x$ for all $n$ yields an output that also stays below some finite bound.
  For an LTI system this holds exactly when the impulse response is absolutely summable,
  $$\sum_n |h[n]| < \infty$$
  since $|y[n]| \le \sum_k |x[n-k]|\,|h[k]| \le B_x \sum_k |h[k]|$. The running sum passes
  ($\sum_n |h[n]| = 2$). The accumulator $y[n] = y[n-1] + x[n]$, whose $h[n] = 1$ for every
  $n \ge 0$, fails: a constant input of $1$ drives the output to $1, 2, 3, \ldots$ without
  bound. §5 restates the same test as "poles inside the unit circle".

Convolution is useful because a short physical event can affect several later samples through the sensor and filter response. For example, the force pulse when a tool touches a wall may appear spread out even if contact began abruptly. **The reading this gives you.** Ask whether a broad measured event belongs to the world or to the pipeline impulse response. Cascaded filters change that response together, so evaluating a filter in isolation can miss the timing seen by the controller.

### 2. Sampling — the contract between continuous and digital

- **Sampling** reads a continuous-time signal $x_c(t)$ once every $T_s$ seconds,
  $x[n] = x_c(nT_s)$, so the **sampling rate** is $f_s = 1/T_s$ samples per second (Hz). Half
  of it, $f_s/2$, is the **Nyquist frequency**: the highest frequency the samples can
  represent without ambiguity.
- **Nyquist–Shannon sampling theorem.** It has two conditions. The signal must be
  **band-limited** to $B$ Hz (no content above $B$), *and* the rate must exceed twice that
  band edge, the **Nyquist rate** $2B$:
  $$f_s > 2B$$
  Then the signal is *perfectly* recoverable from its samples, because sampling makes copies
  of the spectrum spaced $f_s$ apart and those copies do not overlap (proved below). Example: audio
  band-limited to 20 kHz needs $f_s > 40$ kHz, which is why CD audio uses 44.1 kHz.
- **Why the theorem holds — a proof in four steps.** It needs the continuous-time Fourier transform, the counter-rotate-and-average of [[02-foundations/engineering-math|0.5 §7]] done with an integral over time (§3's frequency response is its version for sequences):
  $$X_c(f) = \int_{-\infty}^{\infty} x_c(t)\,e^{-j2\pi ft}\,dt, \qquad x_c(t) = \int_{-\infty}^{\infty} X_c(f)\,e^{j2\pi ft}\,df$$
  and "band-limited to $B$" means $X_c(f) = 0$ for $|f| > B$.
  *Step 1, the samples see only a folded spectrum.* Put $t = nT_s$ into the inverse transform and cut the frequency axis into bands of width $f_s$, writing $f = f' + kf_s$ with $|f'| \le f_s/2$ and $k$ any integer. Because $e^{j2\pi kf_s nT_s} = e^{j2\pi kn} = 1$,
  $$x[n] = \int_{-f_s/2}^{f_s/2} \Big(\sum_{k=-\infty}^{\infty} X_c(f' + kf_s)\Big)\,e^{j2\pi f' nT_s}\,df'$$
  so the samples depend on $X_c$ only through the sum of its copies shifted by every multiple of $f_s$: the "copies of the spectrum" above.
  *Step 2, with $f_s > 2B$ the copies miss the band.* For $|f'| \le f_s/2$ and $k \ne 0$, $|f' + kf_s| \ge f_s/2 > B$, so every copy except $k = 0$ is zero there and the bracket is $X_c(f')$ itself. The samples are then the Fourier-series coefficients of $X_c$ on that band, and those fix it: $X_c(f) = T_s\sum_n x[n]\,e^{-j2\pi fnT_s}$ for $|f| < f_s/2$.
  *Step 3, rebuild the signal.* Put that back into the inverse transform. Sample $n$ contributes $x[n]\,T_s\int_{-f_s/2}^{f_s/2} e^{j2\pi f(t - nT_s)}\,df$, and the integral evaluates to a sinc pulse:
  $$x_c(t) = \sum_n x[n]\,\operatorname{sinc}\Big(\frac{t - nT_s}{T_s}\Big), \qquad \operatorname{sinc}(u) = \frac{\sin \pi u}{\pi u}$$
  Each pulse is 1 at its own sample instant and 0 at every other one, so the sum passes through all the samples and fills in between them. That is the theorem's "perfectly recoverable", and in the frequency domain it is an ideal low-pass filter (§4) with cutoff $f_s/2$.
  *Step 4, failure is aliasing.* If $f_s \le 2B$, some copy with $k \ne 0$ lands inside the band and adds to $X_c(f')$: a tone at $f$ is counted at $f - kf_s$, which is the aliasing formula below.
  *Checked numerically:* tones at $1.3$ and $2.9$ Hz sampled at $f_s = 10$ Hz ($2B = 5.8 < 10$) are rebuilt at $t = 0.5$ s as $-0.630653$, the true value to six decimals (summing the 8,001 samples nearest $t$). A $7$ Hz tone at the same rate rebuilds at $t = 0.123$ s as $-0.680$, the value of the $3$ Hz cosine it aliases to, while the true $7$ Hz value is $+0.642$.
- **Worked: plant P3 at $1\,\mathrm{kHz}$.** The haptic servo uses $T=10^{-3}\,\mathrm{s}$, so $f_s=1000\,\mathrm{Hz}$ and Nyquist is $500\,\mathrm{Hz}$ ([[02-foundations/lab-plants|0.6]]). Contact you care about below $30\,\mathrm{Hz}$ is far inside the theorem; sampling is not the bottleneck. One encoder count is $\Delta x=r_m 2\pi/N=0.010\cdot 2\pi/1024=61.4\,\mu\mathrm{m}$ — a *quantization* stair in space, not a $T_s$. Raising $N$ shrinks space; raising $f_s$ shrinks time. The problem set is this sampler+ZOH as a drawing.
- **Zero-order hold (ZOH).** The step back from samples to a continuous signal that the picture's staircase draws: it holds each sample until the next one,
  $$x_h(t) = x[n] \quad \text{for } nT \le t < (n+1)T$$
  so its output is piecewise constant, jumps at every tick, and never uses a future sample (it is causal). It is the reconstruction a DAC or a servo actually performs, in place of the sinc sum above, which would need samples that have not arrived yet. *Why it runs $T/2$ late on average:* at a time $t$ inside interval $n$ the held value is $x(nT)$, a reading $t - nT$ seconds old, and that age runs evenly from $0$ to $T$, so it averages $T/2$. For a ramp $x = vt$ the staircase is the ramp shifted $T/2$ later on average. The frequency response says the same thing exactly. The hold's impulse response is a unit pulse of width $T$, whose transform is
  $$H_{\text{zoh}}(f) = \int_0^T e^{-j2\pi ft}\,dt = T\,e^{-j\pi fT}\operatorname{sinc}(fT)$$
  a pure delay of $T/2$ (phase $-\pi fT$, a group delay of $T/2$ at every frequency, §4) times a gentle droop in gain. For P3 ($T = 1$ ms) at $30$ Hz the phase is $-5.4°$ and the gain is $0.9985$ of its DC value $T$; at the $500$ Hz Nyquist frequency they are $-90°$ and $0.637$ of it. In a loop that renders a spring $K$, the delay is what costs stability: a spring felt $T/2$ late, $K\,x(t - T/2) \approx Kx - K\tfrac{T}{2}\dot x$, acts as negative damping $KT/2$, the term in the haptic wall bound of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]].
- **Aliasing** is what happens when the condition fails. Content at a frequency $f$ above
  $f_s/2$ shows up in the samples at
  $$f_{alias} = |f - k f_s|$$
  where $k$ is the integer nearest to $f/f_s$, so that $f_{alias}$ lands between $0$ and
  $f_s/2$. The true tone and its alias produce identical samples, so no later processing can
  separate them. Wheels spin backwards on camera; a 60 Hz vibration sampled at 50 Hz ($k = 1$)
  masquerades as 10 Hz; in the figure below, 170 Hz sampled at 200 Hz ($k = 1$) becomes 30 Hz.

<svg viewBox="0 0 480 160" style="max-width:100%;height:auto" role="img" aria-label="aliasing: a 170 Hz signal sampled at 200 Hz looks like 30 Hz">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="25" y1="75" x2="460" y2="75"/></g>
  <path d="M25.0 75.0L25.7 72.4L26.4 69.9L27.1 67.4L27.9 64.9L28.6 62.4L29.3 60.0L30.0 57.7L30.7 55.4L31.4 53.2L32.2 51.1L32.9 49.1L33.6 47.2L34.3 45.4L35.0 43.7L35.8 42.2L36.5 40.8L37.2 39.5L37.9 38.4L38.6 37.5L39.3 36.7L40.0 36.0L40.8 35.5L41.5 35.2L42.2 35.0L42.9 35.0L43.6 35.2L44.4 35.5L45.1 36.0L45.8 36.6L46.5 37.5L47.2 38.4L47.9 39.5L48.7 40.8L49.4 42.2L50.1 43.7L50.8 45.4L51.5 47.1L52.2 49.0L53.0 51.0L53.7 53.1L54.4 55.3L55.1 57.6L55.8 59.9L56.5 62.4L57.2 64.8L58.0 67.3L58.7 69.8L59.4 72.4L60.1 74.9L60.8 77.5L61.5 80.1L62.3 82.6L63.0 85.1L63.7 87.6L64.4 90.0L65.1 92.3L65.8 94.6L66.6 96.8L67.3 98.9L68.0 100.9L68.7 102.8L69.4 104.6L70.2 106.2L70.9 107.8L71.6 109.2L72.3 110.4L73.0 111.5L73.7 112.5L74.4 113.3L75.2 114.0L75.9 114.5L76.6 114.8L77.3 115.0L78.0 115.0L78.8 114.8L79.5 114.5L80.2 114.0L80.9 113.4L81.6 112.6L82.3 111.6L83.1 110.5L83.8 109.2L84.5 107.9L85.2 106.3L85.9 104.7L86.6 102.9L87.3 101.0L88.1 99.0L88.8 96.9L89.5 94.7L90.2 92.4L90.9 90.1L91.7 87.7L92.4 85.2L93.1 82.7L93.8 80.2L94.5 77.7L95.2 75.1L96.0 72.5L96.7 70.0L97.4 67.5L98.1 65.0L98.8 62.5L99.5 60.1L100.3 57.7L101.0 55.5L101.7 53.3L102.4 51.2L103.1 49.2L103.8 47.3L104.5 45.5L105.3 43.8L106.0 42.3L106.7 40.9L107.4 39.6L108.1 38.5L108.8 37.5L109.6 36.7L110.3 36.0L111.0 35.5L111.7 35.2L112.4 35.0L113.2 35.0L113.9 35.2L114.6 35.5L115.3 36.0L116.0 36.6L116.7 37.4L117.4 38.4L118.2 39.5L118.9 40.7L119.6 42.1L120.3 43.6L121.0 45.3L121.8 47.1L122.5 49.0L123.2 51.0L123.9 53.1L124.6 55.2L125.3 57.5L126.0 59.9L126.8 62.3L127.5 64.7L128.2 67.2L128.9 69.7L129.6 72.3L130.3 74.8L131.1 77.4L131.8 80.0L132.5 82.5L133.2 85.0L133.9 87.5L134.7 89.9L135.4 92.2L136.1 94.5L136.8 96.7L137.5 98.8L138.2 100.8L138.9 102.7L139.7 104.5L140.4 106.2L141.1 107.7L141.8 109.1L142.5 110.4L143.2 111.5L144.0 112.5L144.7 113.3L145.4 114.0L146.1 114.5L146.8 114.8L147.6 115.0L148.3 115.0L149.0 114.8L149.7 114.5L150.4 114.0L151.1 113.4L151.8 112.6L152.6 111.7L153.3 110.5L154.0 109.3L154.7 107.9L155.4 106.4L156.1 104.7L156.9 103.0L157.6 101.1L158.3 99.1L159.0 97.0L159.7 94.8L160.5 92.5L161.2 90.2L161.9 87.8L162.6 85.3L163.3 82.8L164.0 80.3L164.8 77.8L165.5 75.2L166.2 72.6L166.9 70.1L167.6 67.6L168.3 65.1L169.1 62.6L169.8 60.2L170.5 57.8L171.2 55.6L171.9 53.4L172.6 51.2L173.3 49.2L174.1 47.3L174.8 45.5L175.5 43.9L176.2 42.3L176.9 40.9L177.6 39.6L178.4 38.5L179.1 37.5L179.8 36.7L180.5 36.1L181.2 35.5L182.0 35.2L182.7 35.0L183.4 35.0L184.1 35.2L184.8 35.5L185.5 36.0L186.2 36.6L187.0 37.4L187.7 38.3L188.4 39.4L189.1 40.7L189.8 42.1L190.6 43.6L191.3 45.2L192.0 47.0L192.7 48.9L193.4 50.9L194.1 53.0L194.9 55.2L195.6 57.4L196.3 59.8L197.0 62.2L197.7 64.6L198.4 67.1L199.2 69.6L199.9 72.2L200.6 74.7L201.3 77.3L202.0 79.9L202.7 82.4L203.4 84.9L204.2 87.4L204.9 89.8L205.6 92.1L206.3 94.4L207.0 96.6L207.8 98.7L208.5 100.7L209.2 102.6L209.9 104.4L210.6 106.1L211.3 107.7L212.0 109.1L212.8 110.3L213.5 111.5L214.2 112.4L214.9 113.3L215.6 113.9L216.3 114.4L217.1 114.8L217.8 115.0L218.5 115.0L219.2 114.8L219.9 114.5L220.7 114.1L221.4 113.4L222.1 112.6L222.8 111.7L223.5 110.6L224.2 109.4L224.9 108.0L225.7 106.5L226.4 104.8L227.1 103.0L227.8 101.1L228.5 99.2L229.3 97.1L230.0 94.9L230.7 92.6L231.4 90.3L232.1 87.9L232.8 85.4L233.6 82.9L234.3 80.4L235.0 77.9L235.7 75.3L236.4 72.7L237.1 70.2L237.8 67.7L238.6 65.1L239.3 62.7L240.0 60.3L240.7 57.9L241.4 55.6L242.2 53.4L242.9 51.3L243.6 49.3L244.3 47.4L245.0 45.6L245.7 43.9L246.4 42.4L247.2 41.0L247.9 39.7L248.6 38.6L249.3 37.6L250.0 36.7L250.8 36.1L251.5 35.6L252.2 35.2L252.9 35.0L253.6 35.0L254.3 35.2L255.1 35.5L255.8 35.9L256.5 36.6L257.2 37.3L257.9 38.3L258.6 39.4L259.3 40.6L260.1 42.0L260.8 43.5L261.5 45.2L262.2 46.9L262.9 48.8L263.6 50.8L264.4 52.9L265.1 55.1L265.8 57.3L266.5 59.7L267.2 62.1L267.9 64.5L268.7 67.0L269.4 69.5L270.1 72.1L270.8 74.6L271.5 77.2L272.2 79.8L273.0 82.3L273.7 84.8L274.4 87.3L275.1 89.7L275.8 92.0L276.6 94.3L277.3 96.5L278.0 98.6L278.7 100.7L279.4 102.6L280.1 104.4L280.9 106.0L281.6 107.6L282.3 109.0L283.0 110.3L283.7 111.4L284.4 112.4L285.2 113.2L285.9 113.9L286.6 114.4L287.3 114.8L288.0 115.0L288.7 115.0L289.4 114.8L290.2 114.5L290.9 114.1L291.6 113.5L292.3 112.7L293.0 111.7L293.8 110.6L294.5 109.4L295.2 108.0L295.9 106.5L296.6 104.9L297.3 103.1L298.1 101.2L298.8 99.2L299.5 97.1L300.2 95.0L300.9 92.7L301.6 90.4L302.3 88.0L303.1 85.5L303.8 83.0L304.5 80.5L305.2 78.0L305.9 75.4L306.7 72.8L307.4 70.3L308.1 67.8L308.8 65.2L309.5 62.8L310.2 60.4L311.0 58.0L311.7 55.7L312.4 53.5L313.1 51.4L313.8 49.4L314.5 47.5L315.2 45.7L316.0 44.0L316.7 42.4L317.4 41.0L318.1 39.7L318.8 38.6L319.6 37.6L320.3 36.8L321.0 36.1L321.7 35.6L322.4 35.2L323.1 35.0L323.9 35.0L324.6 35.1L325.3 35.4L326.0 35.9L326.7 36.5L327.4 37.3L328.1 38.3L328.9 39.3L329.6 40.6L330.3 41.9L331.0 43.5L331.7 45.1L332.4 46.9L333.2 48.7L333.9 50.7L334.6 52.8L335.3 55.0L336.0 57.2L336.8 59.6L337.5 62.0L338.2 64.4L338.9 66.9L339.6 69.4L340.3 72.0L341.1 74.5L341.8 77.1L342.5 79.7L343.2 82.2L343.9 84.7L344.6 87.2L345.3 89.6L346.1 91.9L346.8 94.2L347.5 96.4L348.2 98.6L348.9 100.6L349.7 102.5L350.4 104.3L351.1 106.0L351.8 107.5L352.5 109.0L353.2 110.2L353.9 111.4L354.7 112.4L355.4 113.2L356.1 113.9L356.8 114.4L357.5 114.8L358.2 115.0L359.0 115.0L359.7 114.9L360.4 114.6L361.1 114.1L361.8 113.5L362.6 112.7L363.3 111.8L364.0 110.7L364.7 109.5L365.4 108.1L366.1 106.6L366.8 104.9L367.6 103.2L368.3 101.3L369.0 99.3L369.7 97.2L370.4 95.1L371.1 92.8L371.9 90.5L372.6 88.1L373.3 85.6L374.0 83.1L374.7 80.6L375.4 78.1L376.2 75.5L376.9 72.9L377.6 70.4L378.3 67.9L379.0 65.3L379.8 62.9L380.5 60.5L381.2 58.1L381.9 55.8L382.6 53.6L383.3 51.5L384.1 49.5L384.8 47.5L385.5 45.7L386.2 44.1L386.9 42.5L387.6 41.1L388.4 39.8L389.1 38.6L389.8 37.6L390.5 36.8L391.2 36.1L391.9 35.6L392.6 35.2L393.4 35.0L394.1 35.0L394.8 35.1L395.5 35.4L396.2 35.9L396.9 36.5L397.7 37.3L398.4 38.2L399.1 39.3L399.8 40.5L400.5 41.9L401.2 43.4L402.0 45.0L402.7 46.8L403.4 48.7L404.1 50.6L404.8 52.7L405.6 54.9L406.3 57.2L407.0 59.5L407.7 61.9L408.4 64.3L409.1 66.8L409.9 69.3L410.6 71.9L411.3 74.4L412.0 77.0L412.7 79.6L413.4 82.1L414.2 84.6L414.9 87.1L415.6 89.5L416.3 91.8L417.0 94.1L417.7 96.3L418.4 98.5L419.2 100.5L419.9 102.4L420.6 104.2L421.3 105.9L422.0 107.5L422.8 108.9L423.5 110.2L424.2 111.3L424.9 112.3L425.6 113.2L426.3 113.9L427.1 114.4L427.8 114.8L428.5 115.0L429.2 115.0L429.9 114.9L430.6 114.6L431.4 114.1L432.1 113.5L432.8 112.7L433.5 111.8L434.2 110.7L434.9 109.5L435.7 108.1L436.4 106.6L437.1 105.0L437.8 103.2L438.5 101.4L439.2 99.4L439.9 97.3L440.7 95.1L441.4 92.9L442.1 90.6L442.8 88.2L443.5 85.7L444.3 83.2L445.0 80.7L445.7 78.2L446.4 75.6L447.1 73.0L447.8 70.5L448.6 67.9L449.3 65.4L450.0 63.0L450.7 60.6L451.4 58.2L452.1 55.9L452.9 53.7L453.6 51.6L454.3 49.5L455.0 47.6" fill="none" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <path d="M25.0 75.0L25.7 75.5L26.4 75.9L27.1 76.4L27.9 76.8L28.6 77.3L29.3 77.7L30.0 78.2L30.7 78.6L31.4 79.1L32.2 79.5L32.9 80.0L33.6 80.4L34.3 80.9L35.0 81.3L35.8 81.8L36.5 82.2L37.2 82.6L37.9 83.1L38.6 83.5L39.3 84.0L40.0 84.4L40.8 84.9L41.5 85.3L42.2 85.7L42.9 86.2L43.6 86.6L44.4 87.0L45.1 87.5L45.8 87.9L46.5 88.3L47.2 88.7L47.9 89.2L48.7 89.6L49.4 90.0L50.1 90.4L50.8 90.8L51.5 91.3L52.2 91.7L53.0 92.1L53.7 92.5L54.4 92.9L55.1 93.3L55.8 93.7L56.5 94.1L57.2 94.5L58.0 94.9L58.7 95.3L59.4 95.7L60.1 96.0L60.8 96.4L61.5 96.8L62.3 97.2L63.0 97.6L63.7 97.9L64.4 98.3L65.1 98.7L65.8 99.0L66.6 99.4L67.3 99.8L68.0 100.1L68.7 100.5L69.4 100.8L70.2 101.1L70.9 101.5L71.6 101.8L72.3 102.2L73.0 102.5L73.7 102.8L74.4 103.1L75.2 103.5L75.9 103.8L76.6 104.1L77.3 104.4L78.0 104.7L78.8 105.0L79.5 105.3L80.2 105.6L80.9 105.9L81.6 106.2L82.3 106.5L83.1 106.7L83.8 107.0L84.5 107.3L85.2 107.5L85.9 107.8L86.6 108.1L87.3 108.3L88.1 108.6L88.8 108.8L89.5 109.0L90.2 109.3L90.9 109.5L91.7 109.7L92.4 110.0L93.1 110.2L93.8 110.4L94.5 110.6L95.2 110.8L96.0 111.0L96.7 111.2L97.4 111.4L98.1 111.6L98.8 111.7L99.5 111.9L100.3 112.1L101.0 112.3L101.7 112.4L102.4 112.6L103.1 112.7L103.8 112.9L104.5 113.0L105.3 113.2L106.0 113.3L106.7 113.4L107.4 113.5L108.1 113.7L108.8 113.8L109.6 113.9L110.3 114.0L111.0 114.1L111.7 114.2L112.4 114.3L113.2 114.4L113.9 114.4L114.6 114.5L115.3 114.6L116.0 114.6L116.7 114.7L117.4 114.8L118.2 114.8L118.9 114.8L119.6 114.9L120.3 114.9L121.0 114.9L121.8 115.0L122.5 115.0L123.2 115.0L123.9 115.0L124.6 115.0L125.3 115.0L126.0 115.0L126.8 115.0L127.5 115.0L128.2 114.9L128.9 114.9L129.6 114.9L130.3 114.8L131.1 114.8L131.8 114.7L132.5 114.7L133.2 114.6L133.9 114.6L134.7 114.5L135.4 114.4L136.1 114.3L136.8 114.3L137.5 114.2L138.2 114.1L138.9 114.0L139.7 113.9L140.4 113.8L141.1 113.6L141.8 113.5L142.5 113.4L143.2 113.3L144.0 113.1L144.7 113.0L145.4 112.9L146.1 112.7L146.8 112.5L147.6 112.4L148.3 112.2L149.0 112.1L149.7 111.9L150.4 111.7L151.1 111.5L151.8 111.3L152.6 111.2L153.3 111.0L154.0 110.8L154.7 110.5L155.4 110.3L156.1 110.1L156.9 109.9L157.6 109.7L158.3 109.5L159.0 109.2L159.7 109.0L160.5 108.7L161.2 108.5L161.9 108.3L162.6 108.0L163.3 107.7L164.0 107.5L164.8 107.2L165.5 106.9L166.2 106.7L166.9 106.4L167.6 106.1L168.3 105.8L169.1 105.5L169.8 105.2L170.5 104.9L171.2 104.6L171.9 104.3L172.6 104.0L173.3 103.7L174.1 103.4L174.8 103.1L175.5 102.7L176.2 102.4L176.9 102.1L177.6 101.8L178.4 101.4L179.1 101.1L179.8 100.7L180.5 100.4L181.2 100.0L182.0 99.7L182.7 99.3L183.4 99.0L184.1 98.6L184.8 98.2L185.5 97.9L186.2 97.5L187.0 97.1L187.7 96.7L188.4 96.3L189.1 96.0L189.8 95.6L190.6 95.2L191.3 94.8L192.0 94.4L192.7 94.0L193.4 93.6L194.1 93.2L194.9 92.8L195.6 92.4L196.3 92.0L197.0 91.6L197.7 91.2L198.4 90.7L199.2 90.3L199.9 89.9L200.6 89.5L201.3 89.1L202.0 88.6L202.7 88.2L203.4 87.8L204.2 87.4L204.9 86.9L205.6 86.5L206.3 86.1L207.0 85.6L207.8 85.2L208.5 84.8L209.2 84.3L209.9 83.9L210.6 83.4L211.3 83.0L212.0 82.5L212.8 82.1L213.5 81.7L214.2 81.2L214.9 80.8L215.6 80.3L216.3 79.9L217.1 79.4L217.8 79.0L218.5 78.5L219.2 78.1L219.9 77.6L220.7 77.2L221.4 76.7L222.1 76.3L222.8 75.8L223.5 75.4L224.2 74.9L224.9 74.4L225.7 74.0L226.4 73.5L227.1 73.1L227.8 72.6L228.5 72.2L229.3 71.7L230.0 71.3L230.7 70.8L231.4 70.4L232.1 69.9L232.8 69.5L233.6 69.0L234.3 68.6L235.0 68.1L235.7 67.7L236.4 67.3L237.1 66.8L237.8 66.4L238.6 65.9L239.3 65.5L240.0 65.1L240.7 64.6L241.4 64.2L242.2 63.7L242.9 63.3L243.6 62.9L244.3 62.4L245.0 62.0L245.7 61.6L246.4 61.2L247.2 60.7L247.9 60.3L248.6 59.9L249.3 59.5L250.0 59.1L250.8 58.7L251.5 58.2L252.2 57.8L252.9 57.4L253.6 57.0L254.3 56.6L255.1 56.2L255.8 55.8L256.5 55.4L257.2 55.0L257.9 54.6L258.6 54.3L259.3 53.9L260.1 53.5L260.8 53.1L261.5 52.7L262.2 52.4L262.9 52.0L263.6 51.6L264.4 51.2L265.1 50.9L265.8 50.5L266.5 50.2L267.2 49.8L267.9 49.5L268.7 49.1L269.4 48.8L270.1 48.4L270.8 48.1L271.5 47.8L272.2 47.4L273.0 47.1L273.7 46.8L274.4 46.5L275.1 46.2L275.8 45.8L276.6 45.5L277.3 45.2L278.0 44.9L278.7 44.6L279.4 44.3L280.1 44.1L280.9 43.8L281.6 43.5L282.3 43.2L283.0 42.9L283.7 42.7L284.4 42.4L285.2 42.1L285.9 41.9L286.6 41.6L287.3 41.4L288.0 41.1L288.7 40.9L289.4 40.7L290.2 40.4L290.9 40.2L291.6 40.0L292.3 39.8L293.0 39.6L293.8 39.4L294.5 39.2L295.2 39.0L295.9 38.8L296.6 38.6L297.3 38.4L298.1 38.2L298.8 38.0L299.5 37.9L300.2 37.7L300.9 37.5L301.6 37.4L302.3 37.2L303.1 37.1L303.8 36.9L304.5 36.8L305.2 36.7L305.9 36.5L306.7 36.4L307.4 36.3L308.1 36.2L308.8 36.1L309.5 36.0L310.2 35.9L311.0 35.8L311.7 35.7L312.4 35.6L313.1 35.5L313.8 35.5L314.5 35.4L315.2 35.3L316.0 35.3L316.7 35.2L317.4 35.2L318.1 35.2L318.8 35.1L319.6 35.1L320.3 35.1L321.0 35.0L321.7 35.0L322.4 35.0L323.1 35.0L323.9 35.0L324.6 35.0L325.3 35.0L326.0 35.0L326.7 35.0L327.4 35.1L328.1 35.1L328.9 35.1L329.6 35.2L330.3 35.2L331.0 35.3L331.7 35.3L332.4 35.4L333.2 35.5L333.9 35.5L334.6 35.6L335.3 35.7L336.0 35.8L336.8 35.9L337.5 36.0L338.2 36.1L338.9 36.2L339.6 36.3L340.3 36.4L341.1 36.5L341.8 36.6L342.5 36.8L343.2 36.9L343.9 37.0L344.6 37.2L345.3 37.3L346.1 37.5L346.8 37.6L347.5 37.8L348.2 38.0L348.9 38.2L349.7 38.3L350.4 38.5L351.1 38.7L351.8 38.9L352.5 39.1L353.2 39.3L353.9 39.5L354.7 39.7L355.4 39.9L356.1 40.1L356.8 40.4L357.5 40.6L358.2 40.8L359.0 41.1L359.7 41.3L360.4 41.6L361.1 41.8L361.8 42.1L362.6 42.3L363.3 42.6L364.0 42.8L364.7 43.1L365.4 43.4L366.1 43.7L366.8 44.0L367.6 44.2L368.3 44.5L369.0 44.8L369.7 45.1L370.4 45.4L371.1 45.7L371.9 46.0L372.6 46.4L373.3 46.7L374.0 47.0L374.7 47.3L375.4 47.7L376.2 48.0L376.9 48.3L377.6 48.7L378.3 49.0L379.0 49.3L379.8 49.7L380.5 50.0L381.2 50.4L381.9 50.8L382.6 51.1L383.3 51.5L384.1 51.9L384.8 52.2L385.5 52.6L386.2 53.0L386.9 53.4L387.6 53.7L388.4 54.1L389.1 54.5L389.8 54.9L390.5 55.3L391.2 55.7L391.9 56.1L392.6 56.5L393.4 56.9L394.1 57.3L394.8 57.7L395.5 58.1L396.2 58.5L396.9 58.9L397.7 59.3L398.4 59.8L399.1 60.2L399.8 60.6L400.5 61.0L401.2 61.5L402.0 61.9L402.7 62.3L403.4 62.7L404.1 63.2L404.8 63.6L405.6 64.0L406.3 64.5L407.0 64.9L407.7 65.3L408.4 65.8L409.1 66.2L409.9 66.7L410.6 67.1L411.3 67.6L412.0 68.0L412.7 68.4L413.4 68.9L414.2 69.3L414.9 69.8L415.6 70.2L416.3 70.7L417.0 71.1L417.7 71.6L418.4 72.0L419.2 72.5L419.9 72.9L420.6 73.4L421.3 73.8L422.0 74.3L422.8 74.7L423.5 75.2L424.2 75.7L424.9 76.1L425.6 76.6L426.3 77.0L427.1 77.5L427.8 77.9L428.5 78.4L429.2 78.8L429.9 79.3L430.6 79.7L431.4 80.2L432.1 80.6L432.8 81.1L433.5 81.5L434.2 82.0L434.9 82.4L435.7 82.8L436.4 83.3L437.1 83.7L437.8 84.2L438.5 84.6L439.2 85.0L439.9 85.5L440.7 85.9L441.4 86.4L442.1 86.8L442.8 87.2L443.5 87.6L444.3 88.1L445.0 88.5L445.7 88.9L446.4 89.4L447.1 89.8L447.8 90.2L448.6 90.6L449.3 91.0L450.0 91.4L450.7 91.8L451.4 92.3L452.1 92.7L452.9 93.1L453.6 93.5L454.3 93.9L455.0 94.3" fill="none" stroke="currentColor" stroke-width="2"/>
  <g fill="currentColor"><circle cx="25.0" cy="75.0" r="3"/><circle cx="84.7" cy="107.4" r="3"/><circle cx="144.4" cy="113.0" r="3"/><circle cx="204.2" cy="87.4" r="3"/><circle cx="263.9" cy="51.5" r="3"/><circle cx="323.6" cy="35.0" r="3"/><circle cx="383.3" cy="51.5" r="3"/><circle cx="443.1" cy="87.4" r="3"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="25" y="20" opacity="0.7">thin: the real 170 Hz vibration &#183; dots: the 8 samples taken at 200 Hz</text>
    <text x="25" y="136">thick: the 30 Hz ghost &#8212; it passes through every one</text>
    <text x="25" y="150">of those samples, so the data cannot tell the two apart</text>
  </g>
</svg>


- Therefore: **anti-alias filter before downsampling**, always (this includes decimating
  IMU logs in software). An anti-alias filter is a low-pass filter (§4) placed before the
  sampler or the decimator that removes content above the *new* $f_s/2$, so nothing is left
  that could fold down.
- Engineering corollary: pick sensor rates from the fastest dynamics you must *observe*,
  with margin — a 10 Hz perception loop cannot even see, let alone damp, a 50 Hz vibration.
- **Quantization** rounds each sample to one of $2^N$ levels, where $N$ is the number of bits
  of the ADC (analog-to-digital converter). Over an input range $R$ the step is
  $\Delta = R/2^N$, and the rounding error behaves like uniform noise on
  $[-\Delta/2, \Delta/2]$, whose variance is $\Delta^2/12$. Finite bits therefore add ~uniform noise — roughly **6 dB of SNR per bit**. *SNR* =
  signal-to-noise ratio, signal power divided by noise power; *dB* (decibel) is the log scale
  it is quoted on, where +6 dB ≈ 2× in amplitude. So each extra bit of an ADC halves
  the RMS quantization noise, which quarters its power — that factor of 4 is the 6 dB. For a
  full-scale sine wave the standard formula is
  $$\text{SNR}_{dB} = 10\log_{10}\frac{P_{signal}}{P_{noise}} \approx 6.02\,N + 1.76$$
  where $P_{signal}$ and $P_{noise}$ are the two powers, $6.02 = 10\log_{10}4$ is the per-bit
  gain, and $1.76$ dB comes from the sine's power relative to the $\Delta^2/12$ noise. A 12-bit
  ADC gives about $74$ dB and a 16-bit one about $98$ dB; a 12-bit converter spanning 10 V has
  steps of $2.44$ mV and RMS quantization noise of $0.70$ mV. This is the *other* half of digitization. When a quantized sensor's error really is white, and when it is a fixed bias instead (an encoder at rest), is [[04-robotics/sensor-models|3.2 Sensor Models & Noise §4]].
- Where this contract becomes a stability problem: a haptic loop rendering a virtual wall
  must close on a human hand every millisecond, and there sampling and quantization stop
  being accuracy questions and start deciding whether the device buzzes
  ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]]).

### 3. Frequency domain — the diagonalizing basis

- Fourier's claim: signals = sums of sinusoids. Deeper claim: **complex exponentials are
  the eigenfunctions of LTI systems** ([[02-foundations/linear-algebra|eigen-thinking]]) —
  for a stable LTI system, a complex exponential comes out multiplied by $H(f)$, so a real sinusoid comes out at the same frequency, scaled by $|H(f)|$ and phase-shifted by $\angle H(f)$. That is why frequency
  analysis diagonalizes filtering.
- **Frequency response.** For an LTI system with impulse response $h$ it is the complex-valued
  function of frequency
  $$H(f) = \sum_n h[n]\, e^{-j2\pi f n}$$
  where $f$ is in cycles per sample ($f = f_{Hz}/f_s$), the magnitude $|H(f)|$ is the gain at
  that frequency and the angle $\angle H(f)$ is the phase shift. It is exactly the eigenvalue
  in the claim above, since feeding $x[n] = e^{j2\pi fn}$ into the convolution of §1 gives
  $y[n] = \sum_k h[k]\,e^{j2\pi f(n-k)} = H(f)\,e^{j2\pi fn}$. For the running sum $h = [1, 1]$:
  $H(0) = 2$ (a constant is doubled), $H(1/4) = 1 - j$, so the gain is $\sqrt2 \approx 1.414$
  with a $-45°$ phase, and $H(1/2) = 0$ (the alternating input $+1, -1, +1, \ldots$ cancels).
- **DFT** (discrete Fourier transform) maps a block of $N$ samples $x[0], \ldots, x[N-1]$ to
  $N$ complex coefficients,
  $$X[k] = \sum_{n=0}^{N-1} x[n]\, e^{-j2\pi kn/N}$$
  where the bin index $k = 0, \ldots, N-1$ stands for the frequency $k f_s/N$ Hz (bins above
  $N/2$ are the negative frequencies), $|X[k]|$ says how much of that frequency is present and
  $\angle X[k]$ its phase. It is invertible, $x[n] = \frac1N \sum_{k} X[k]\,e^{j2\pi kn/N}$, so
  no information is lost. The bin spacing $f_s/N$ is the frequency resolution: 1000 samples at
  200 Hz resolve $0.2$ Hz. Each $X[k]$ is the correlation of the signal
  with one basis frequency ([[02-foundations/engineering-math|0.5 §7]] unpacks *why* that
  sum is a projection); the **FFT** (fast Fourier transform) is not a different transform but an
  algorithm that computes all $N$ coefficients in $O(N\log N)$ instead of $O(N^2)$.
- **Worked DFT, $N = 4$, by hand.** Take $x = [1, 0, -1, 0]$ — one full cycle across the
  4-sample window. The twiddle factor is $e^{-j2\pi kn/4} = (-j)^{kn}$, so:
  $$X[0] = 1 + 0 - 1 + 0 = 0, \qquad X[1] = 1(1) + 0(-j) + (-1)(-1) + 0(j) = 2$$
  $$X[2] = 0, \qquad X[3] = 2$$
  Read it off: $X[0] = 0$ says the signal has **no DC** — it averages to zero, which it
  visibly does. All the energy sits in $k = 1$ and its mirror $k = 3$ (the same frequency
  seen as negative — for a real signal the magnitude spectrum is always symmetric, which is why one-sided FFT plots show only the first half). One frequency lit up, and it is the bin whose rotation completes
  exactly one turn across the window. That is the entire DFT.
- **Convolution theorem**: convolving in time is multiplying in frequency,
  $$y = x * h \quad\Longleftrightarrow\quad Y(f) = X(f)\,H(f)$$
  where $X(f) = \sum_n x[n]e^{-j2\pi fn}$ and $Y(f)$ are the transforms of input and output,
  built the same way as $H(f)$ above. It holds because each complex exponential in $x$ is just
  multiplied by $H(f)$. Check it on §1's example at $f = 1/4$, where $e^{-j2\pi n/4} = (-j)^n$:
  $X = 1 + 2(-j) + 3(-1) = -2 - 2j$ and $H = 1 - j$, so $XH = -4$; directly,
  $Y = 1 + 3(-j) + 5(-1) + 3(j) = -4$ ✓. So filtering is multiplication
  in frequency; also the lens for neural nets' spectral bias (they fit low frequencies first, so a network
  fed raw coordinates learns an over-smooth function — the reason
  [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]] lifts its inputs to Fourier features).
- Signal fingerprints: white noise = flat spectrum (uncorrelated samples; defined in
  [[02-foundations/probability|3. Probability §5]]); drift/bias = spike near **DC** ("DC" is
  borrowed from direct current and here just means zero frequency — the constant part); rotating
  machinery = sharp peaks at harmonics (an excavator's engine band is a notch-filter target).

Frequency analysis is useful because visually similar fluctuations can require different interventions. For example, a narrow machinery vibration peak and broad contact transients can overlap in time but occupy different spectral patterns. Removing the peak may help, while indiscriminate smoothing may erase the contact signal. **The reading this gives you.** Relate spectral peaks to operating conditions and preserve the windowing and sampling details. A peak in a finite-window spectrum is evidence to investigate, not automatic identification of a physical source.

### 4. Filtering — design basics

- **FIR** (finite impulse response) filter: the output is a fixed weighted sum of the
  current input and the previous $M-1$ inputs, and nothing else,
  $$y[n] = \sum_{k=0}^{M-1} b_k\, x[n-k]$$
  where the $b_k$ are the coefficients and $M$ is the filter length. Feed it $\delta[n]$ and
  the output is the coefficient list itself, $h[k] = b_k$, which ends after $M$ samples: that
  is the "finite". Two consequences follow. It is always BIBO stable, since
  $\sum_n |h[n]| = \sum_k |b_k|$ is a finite sum (§1). And it has exactly linear phase
  whenever the coefficients are symmetric, $b_k = b_{M-1-k}$, which delays every frequency by
  the same $(M-1)/2$ samples, so the waveform is not distorted: a 5-tap moving average delays
  everything by 2 samples, i.e. 20 ms at 100 Hz. The price is that it needs more **taps** — one tap = one $b_k$,
  i.e. one past sample the filter still has to keep and multiply, so "more taps" means more
  memory, more arithmetic, and more delay. The moving average is the
  simplest FIR. Feeding it a pure tone $e^{j2\pi fn}$ ($f$ in cycles/sample) multiplies the tone by
  $H(f) = \tfrac1M\sum_{k=0}^{M-1} e^{-j2\pi fk}$, a geometric series that sums to
  $\tfrac1M(1-e^{-j2\pi fM})/(1-e^{-j2\pi f})$; factoring $e^{-j\pi fM}$ out of the top and
  $e^{-j\pi f}$ out of the bottom leaves two sines, so $|H(f)| = |\sin(\pi f M)/(M\sin \pi f)|$. It shows the
  tradeoff: longer window ⇒ narrower passband *and* more delay.
- **IIR** (infinite impulse response) filter: the output also feeds back past *outputs*,
  $$y[n] = \sum_{k=0}^{M} b_k\, x[n-k] - \sum_{k=1}^{N} a_k\, y[n-k]$$
  where the $b_k$ weight inputs as in an FIR and the $a_k$ weight the $N$ previous outputs.
  Because every output re-enters later outputs, one impulse echoes forever, so $h$ never ends.
  The simplest case is the exponential smoother $y[n] = \alpha y[n-1] + (1-\alpha)x[n]$
  ($b_0 = 1-\alpha$, $a_1 = -\alpha$), whose impulse response is $h[n] = (1-\alpha)\alpha^n$
  for $n \ge 0$: with $\alpha = 0.9$ that is $0.1, 0.09, 0.081, 0.0729, \ldots$, never exactly
  zero. Stability is no longer automatic: for $0 < \alpha < 1$ the sum $\sum_n |h[n]|$ is $1$,
  but at $\alpha = 1.1$ the terms grow. IIR filters are cheap; phase is nonlinear. Higher-order IIR designs can be sharp but can ring or go unstable; this simplest one has a single real pole at $z=\alpha$ ($z$ is the Z-transform variable of §5, and §5 derives this pole), so for $0<\alpha<1$ it is always stable, never rings, and rolls off gently.
- **The $\alpha$ in that formula is a convention, not a quantity.** Written as above, a
  large $\alpha$ trusts the *previous output* and filters more. Many papers and lecture
  notes instead write $y[n] = \alpha x[n] + (1-\alpha)y[n-1]$, where a large $\alpha$
  trusts the *new sample* and filters less. The two are the same filter with $\alpha$
  replaced by $1-\alpha$, so the symbol alone tells you nothing — read the equation
  before you read the number.
- **The smoother, traced step by step.** Run $y[n] = 0.9\,y[n-1] + 0.1\,x[n]$ on a step: the
  input jumps from $0$ to $1$ and stays. Starting at $y = 0$ the output goes
  $0.1,\ 0.19,\ 0.271,\ 0.344,\ 0.410,\ \ldots$ — reaching 90% of the new value takes about
  **22 samples**, since $0.9^{22} \approx 0.1$. At 100 Hz its step response therefore needs
  about $0.22$ s to traverse 90% of the change. This is not a pure $0.22$ s dead time: the
  filter has frequency-dependent phase and group delay. Set $\alpha = 0.5$ instead and the
  first discrete sample above 90% is sample 4. For independent white input noise, this
  coefficient convention gives variance gain $(1-\alpha)/(1+\alpha)$ — in steady state the output
  variance must satisfy $\sigma_y^2 = \alpha^2\sigma_y^2 + (1-\alpha)^2\sigma_x^2$, since $y[n-1]$ and the new
  noise sample are independent, and $(1-\alpha)^2/(1-\alpha^2)$ simplifies to that ratio: 0.053 versus 0.333,
  a factor of 6.3 in variance and 2.5 in standard deviation. This trade — noise rejection
  bought with slower response and phase lag — is central to filter design, and the reason a control engineer always asks what your filter cost you
  in phase ([[04-robotics/control-theory-ce397|control theory §7]]).
- **Filter types, named by the frequencies they pass.** With a cutoff $f_c$, an ideal
  **low-pass** filter has $|H(f)| = 1$ for $|f| < f_c$ and $|H(f)| = 0$ above it; a
  **high-pass** filter is the reverse; a **band-pass** filter keeps one band; a **notch**
  filter removes one narrow band around a frequency $f_0$. Real filters replace the sharp edge
  with a transition band. Choosing: low-pass for sensor noise, high-pass for drift removal,
  notch at known vibration harmonics, complementary filters to fuse IMU accel (low-passed) + gyro
  (high-passed).
- **Complementary filter**: a fusion filter for two sensors that measure the same quantity but
  are trustworthy in *different* frequency bands. One sensor goes through a low-pass $H_L$, the
  other through a high-pass $H_H$, and the pair is chosen so the two responses add to exactly
  one,
  $$H_L(f) + H_H(f) = 1$$
  so the true signal, which both sensors see, passes with unit gain and no distortion, while
  each sensor's bad band is suppressed. For IMU tilt, the accelerometer angle $\theta_{acc}$ is
  right on average but noisy, and the gyro rate $\omega$ integrates smoothly but drifts, so the
  update is one line
  $$\hat\theta[n] = \alpha\big(\hat\theta[n-1] + \omega[n]\,\Delta t\big) + (1-\alpha)\,\theta_{acc}[n]$$
  where $\hat\theta$ is the fused estimate, $\Delta t$ the sample period and $\alpha$ sets the
  crossover. With $\alpha = 0.98$, $\Delta t = 0.01$ s, previous estimate $10°$, gyro rate
  $5°/\text{s}$ and accelerometer reading $11°$, the new estimate is
  $0.98 \times 10.05 + 0.02 \times 11 = 10.069°$. The crossover time constant is
  $\tau = \alpha\Delta t/(1-\alpha) = 0.49$ s: slower changes follow the accelerometer, faster
  ones the gyro.
- **Phase lag is the price of causal smoothing**: realizable causal smoothing generally
  introduces frequency-dependent phase or group delay over the passband —
  aggressive filtering *fights your controller* (a lagged velocity estimate destabilizes a
  D-term). This is the practical reason to prefer model-based estimation:
  under an accurate linear-Gaussian state-space model and noise covariances, the
  **Kalman filter** ([[02-foundations/probability|derived in 3. Probability §5]]) minimizes mean-square
  estimation error. Model mismatch removes that guarantee.
- **Phase delay and group delay** state how late a filter's output is. The phase response is
  $\angle H(f)$ (§3). The **group delay** is its negative slope, measured in samples,
  $$\tau_g(f) = -\frac{1}{2\pi}\,\frac{d\,\angle H(f)}{df}$$
  so a filter whose phase falls linearly with frequency delays every frequency by the same
  number of samples and keeps the waveform's shape. The symmetric 5-tap moving average has
  $\angle H(f) = -4\pi f$ in its passband, hence $\tau_g = 2$ samples everywhere. The exponential
  smoother is not linear-phase: with $\alpha = 0.9$ at $f = 0.05$ cycles/sample its gain is
  $0.32$ and its phase $-62.6°$, and the delay changes from one frequency to the next.

### 5. Bridge to control: transforms

- The Laplace transform (continuous, defined in [[02-foundations/engineering-math|0.5 §9]]) / **Z-transform** (discrete) generalize Fourier:
  convolution ↦ multiplication by a *transfer function* $H(s)$ or $H(z)$.
- The **Z-transform** turns a sequence into a function of a complex variable $z$,
  $$X(z) = \sum_n x[n]\, z^{-n}$$
  so a one-sample delay becomes multiplication by $z^{-1}$. It is tied to the Laplace variable
  by $z = e^{sT_s}$, and on the unit circle $z = e^{j2\pi f}$ it reduces to the frequency
  response of §3. The **transfer function** is the ratio of output to input transforms, with
  the system starting at rest,
  $$H(z) = \frac{Y(z)}{X(z)}$$
  which is the transform of $h$, since convolution became multiplication. Worked: transform the
  exponential smoother term by term, $Y(z) = \alpha z^{-1} Y(z) + (1-\alpha) X(z)$, so
  $H(z) = (1-\alpha)/(1-\alpha z^{-1})$. Its **pole** (a $z$ that makes the denominator zero;
  poles and zeros are defined in [[02-foundations/engineering-math|0.5 §9]]) is $z = \alpha$. Its
  gain at DC ($z = 1$) is exactly $1$, so a constant passes unchanged; at the Nyquist frequency
  ($z = -1$) it is $(1-\alpha)/(1+\alpha)$, which is $0.053$ for $\alpha = 0.9$.
- For a minimal realization ([[02-foundations/engineering-math|0.5 §9]]), poles of $H$ = eigenvalues of the state-space $A$
  ([[02-foundations/linear-algebra|1. Linear Algebra §5]]): stability = poles in the left
  half-plane (continuous) / inside the unit circle, $|z| < 1$ (discrete), for a causal system.
  This is §1's BIBO test in another form, because a pole at $z = \alpha$ contributes a term
  $\alpha^n$ to $h[n]$, which is summable only when $|\alpha| < 1$. Filters, plants, and
  controllers all speak this one language — which is why the control-theory course packet
  and this page are two views of the same object.

Transforms help because they expose how a system changes each frequency and how internal dynamics can grow or decay. For example, a smoothing filter may attenuate vibration while introducing delay into the feedback used for contact control. **The reading this gives you.** Inspect both gain and phase before calling a filtered signal better. Also distinguish state-space modes from transfer-function poles: unobservable or uncontrollable modes (a mode the output never shows, or one the input never excites; defined with their rank tests in [[02-foundations/linear-algebra|1. Linear Algebra §5]]) can disappear through cancellation, so the pole–eigenvalue correspondence needs a minimal realization when used as an equality.

### 6. Sensor-pipeline habits (field-tested)

- Log **raw**, filter later; never filter twice implicitly (driver + your code).
- Timestamp at the sensor, synchronize clocks before fusing (extrinsics *and* time offsets
  for camera-LiDAR-IMU).
- Check the spectrum before choosing a filter: name the noise before you fight it.

> [!tip] Going deeper · 더 깊이
> Oppenheim and Schafer's *Discrete-Time Signal Processing* is the standard course this page compresses. §2 proves the sampling theorem in four steps; its sampling and DFT chapters add the convergence details and practical reconstruction filters that proof leaves out.

For example, a driver may already smooth force readings before a second filter is applied in the controller. The combined stream looks clean while contact onset arrives late. Keeping the raw stream and documenting both stages makes that delay diagnosable. **The reading this gives you.** Trace the signal from acquisition to decision, including clock conversion and every transformation. A plot without its processing history cannot tell you whether the apparent smoothness came from better sensing or from removing the transient that mattered.

### Self-check

1. Convolve $x = [1, 0, -1]$ with $h = [1, 2, 1]$ by hand, and give the output length.
2. An IMU samples at 200 Hz; a motor vibrates at 170 Hz. Where does the vibration appear
   in the data, and what should have been done?
3. Derive the frequency response of the 2-point moving average and find the frequency it
   nulls completely.
4. When its motion/noise models are roughly right, why does a Kalman filter tend to beat
   a hand-tuned low-pass for velocity estimation in a control loop? (Two reasons: one
   about lag, one about models.) And when would the low-pass win?

> [!tip]- Answers
> 1. Flip, slide, multiply, accumulate: $y = [1\cdot 1,\; 1\cdot 2 + 0\cdot 1,\; 1\cdot 1 + 0\cdot 2 + (-1)\cdot 1,\; 0\cdot 1 + (-1)\cdot 2,\; (-1)\cdot 1] = [1, 2, 0, -2, -1]$, of length $3+3-1 = 5$.
> 2. It aliases to $|170 - 200| = 30$ Hz — it will look like a real 30 Hz structural mode and you may "fix" the wrong thing. The remedy is an analog anti-alias filter (cutoff below 100 Hz) *before* sampling, or a sample rate above 340 Hz.
> 3. $H(f) = \tfrac12(1 + e^{-j2\pi f})$, so $|H(f)| = |\cos(\pi f)|$ with $f$ in cycles/sample. It nulls completely at $f = 1/2$ — the Nyquist frequency, where consecutive samples alternate sign and average to zero.
> 4. Lag: the Kalman filter's *prediction* step advances the state before correcting, so it does not pay the full phase lag a causal low-pass does. Models: it uses an explicit process/measurement noise ratio to compute a time-varying optimal gain, instead of one fixed cutoff. The low-pass wins when the motion model is wrong or unknown, when the noise is far from the assumed statistics, or when you simply cannot afford the modeling and tuning effort — a wrong model makes the Kalman filter confidently wrong.

### Problem set · 과제

Tier B. **P3** from [[02-foundations/lab-plants|0.6]]. This page §2. The haptic loop is $1\,\mathrm{kHz}$ ($T=10^{-3}\,\mathrm{s}$). No simulator.

1. **Draw.** The picture above, by hand: continuous handle position $x(t)$ through an ideal sampler of period $T$, then a zero-order hold (value held constant until the next tick). Mark the wall $x_w$.
2. **Derive.** Nyquist frequency at $1\,\mathrm{kHz}$, and the largest band $B$ the theorem allows. If the hand/wall contact you care about lives below $30\,\mathrm{Hz}$, is $1\,\mathrm{kHz}$ enough on sampling grounds alone?
3. **Interpret.** One motor encoder count is $\Delta x=r_m\,2\pi/N$. Compute it. Sampling interval or quantization step? What does raising $N$ change that raising $f_s$ does not?

> [!note]- How to draw it · 그리는 법
> - The signal path as blocks in a row: the handle giving $x(t)$; an ideal sampler, drawn as a switch that closes for an instant every $T=10^{-3}\,\mathrm{s}$, with $f_s=1000\,\mathrm{Hz}$ and Nyquist $500\,\mathrm{Hz}$ under it; the sequence $x[n]=x(nT)$; a zero-order hold, drawn as a box whose output is a staircase; and the held signal that the wall law actually sees.
> - Under the hold, the one thing it does: it holds $x[n]$ constant on $[nT,\ (n+1)T)$ and then jumps.
> - Underneath, one time axis about $8\,\mathrm{ms}$ long so that eight ticks fit, with $x(t)$ as a smooth curve rising through the wall and a dot on it at each tick. Those dots are $x[n]$, and nothing between them exists for the controller.
> - The ZOH staircase on the same axis, each tread flat at the height of the *previous* dot. Shade the sliver between curve and staircase on one tread and label it: the hold is late by $T/2=0.5\,\mathrm{ms}$ on average, which §2 turns into a phase lag.
> - The wall $x_w=0.030\,\mathrm{m}$ as a dashed horizontal line across all three curves, and a circle on the first tread above it: the controller's contact begins at a tick, never at the true crossing.
> - For item 3, faint horizontal gridlines one encoder count apart, $\Delta x=r_m\,2\pi/N=0.010\cdot2\pi/1024=61.4\,\mu\mathrm{m}$, with the dots redrawn snapped to the nearest line. Label the two steps so they cannot be confused: $T$ along time, set by the clock, and $\Delta x$ along space, set by the encoder.
> - Beside the grid, what one count costs in force on this wall, $k_w\,\Delta x=400\times61.4\,\mu\mathrm{m}=0.025\,\mathrm{N}$; at the bottom, the speed at which one new count appears per tick, $\Delta x/T=61.4\,\mathrm{mm/s}$. Slower than that, some ticks report no motion, so a velocity from differenced positions reads zero and then jumps — the quantization noise §4's filtering handles, even for $30\,\mathrm{Hz}$ contact sampled $33.3$ times per cycle.

> [!tip]- Solutions
> 1. Sampler $x[n]=x(nT)$. ZOH: a stair of height $x[n]$ on $[nT,(n+1)T)$. Wall at $x_w=0.030\,\mathrm{m}$.
> 2. $f_s=1000\,\mathrm{Hz}$, Nyquist $500\,\mathrm{Hz}$, so $B<500\,\mathrm{Hz}$. $30\,\mathrm{Hz}$ is far below; sampling is not the bottleneck.
> 3. $\Delta x=0.010\cdot 2\pi/1024=6.14\times 10^{-5}\,\mathrm{m}$ ($61.4\,\mu\mathrm{m}$). Quantization of position, not a $T_s$. Larger $N$ shrinks the stair in space; larger $f_s$ shrinks it in time.

### Robotics bridge

Filtering, sampling, aliasing, and sensor timing continue in [[04-robotics/state-estimation-slam|State Estimation]] and [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]].

## 한국어

*[[02-foundations/probability|3. 확률]]과 [[02-foundations/engineering-math|0.5]]의 오일러 공식 위에 선다. 도메인 다리 하나다: 여기서부터 데이터는 주어지는 것이
아니라 센서에서 도착한다. [[02-foundations/rl-basics|7. RL 기초]]와의 순서는 자유다.*

건설로봇이 싣고 다니는 모든 센서 — 카메라, LiDAR, IMU, 엔코더 — 는 샘플링된, 노이즈 낀
신호를 건네준다. 교재 수준의 서술: 손으로 푸는 합성곱, 수식이 있는 샘플링 정리, DFT/FFT,
필터 설계 기초, 그리고 제어의 전달함수로 가는 다리.

> [!note] 처음이라면 · First pass
> 먼저 그림, §1, §2 — 실제로 무는 것은 샘플링 계약, 에일리어싱, 영차 홀드다 — 그다음 §6의 현장 습관. §2의 네 단계 샘플링 정리 증명은 두 번째 읽기에서 본다. §3~§5는 기계장치이고, 논문이 주파수 영역에서 무언가 할 때 펴라.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 432" style="max-width:100%;height:auto" role="img" aria-label="1 kHz 서보로 도는 장치 P3: 핸들, 이상 샘플러, 영차 홀드, 벽 법칙을 한 줄로 놓고, 그 아래에 핸들 위치와 그 여덟 샘플과 홀드의 계단을 벽과 함께, 엔코더 한 카운트 높이의 격자 위에 그린 그림">
  <defs><marker id="arSpk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <rect x="12" y="33" width="66" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="45.0" y="47.0" fill="currentColor" text-anchor="middle">핸들</text>
  <text x="45.0" y="61.0" fill="currentColor" text-anchor="middle" opacity="0.85">P3</text>
  <line x1="78" y1="50" x2="124" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSpk)"/>
  <text x="101.0" y="43.0" fill="currentColor" text-anchor="middle">x(t)</text>
  <g fill="currentColor"><circle cx="128" cy="50" r="2.6"/><circle cx="164" cy="50" r="2.6"/></g>
  <line x1="128" y1="50" x2="160" y2="36" stroke="currentColor" stroke-width="1.8"/>
  <path d="M150 30 A 14 14 0 0 1 162 43" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" marker-end="url(#arSpk)"/>
  <text x="146.0" y="23.0" fill="currentColor" text-anchor="middle">이상 샘플러</text>
  <text x="146.0" y="72.0" fill="currentColor" text-anchor="middle" opacity="0.9">T = 1 ms마다 닫힌다</text>
  <text x="146.0" y="86.0" fill="currentColor" text-anchor="middle" opacity="0.9">f<tspan dy="3" font-size="11">s</tspan><tspan dx="3.3" dy="-3">= 1000 Hz</tspan></text>
  <text x="146.0" y="100.0" fill="currentColor" text-anchor="middle" opacity="0.9">나이퀴스트 500 Hz</text>
  <line x1="167" y1="50" x2="250" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSpk)"/>
  <text x="208.0" y="43.0" fill="currentColor" text-anchor="middle">x[n] = x(nT)</text>
  <rect x="252" y="33" width="64" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="258,60 270,60 270,53 282,53 282,46 294,46 294,40 310,40" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="284.0" y="23.0" fill="currentColor" text-anchor="middle">영차 홀드</text>
  <text x="284.0" y="86.0" fill="currentColor" text-anchor="middle" opacity="0.9">x[n]을 [nT, (n+1)T) 동안 유지,</text>
  <text x="284.0" y="100.0" fill="currentColor" text-anchor="middle" opacity="0.9">그다음 튄다</text>
  <line x1="316" y1="50" x2="410" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSpk)"/>
  <text x="362.0" y="43.0" fill="currentColor" text-anchor="middle">유지된 x</text>
  <rect x="412" y="33" width="136" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="480.0" y="47.0" fill="currentColor" text-anchor="middle">벽 법칙</text>
  <text x="480.0" y="61.0" fill="currentColor" text-anchor="middle">F = −k<tspan dy="3" font-size="11">w</tspan><tspan dy="-3">(x − x</tspan><tspan dy="3" font-size="11">w</tspan><tspan dy="-3">)</tspan></text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.18"><line x1="60" y1="306.0" x2="364" y2="306.0"/><line x1="60" y1="262.0" x2="364" y2="262.0"/><line x1="60" y1="218.0" x2="364" y2="218.0"/><line x1="60" y1="174.0" x2="364" y2="174.0"/><line x1="60" y1="130.0" x2="364" y2="130.0"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none"><line x1="60" y1="124.0" x2="60" y2="334.0"/><line x1="60" y1="334.0" x2="368" y2="334.0"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="60.0" y1="334.0" x2="60.0" y2="338.0"/><line x1="98.0" y1="334.0" x2="98.0" y2="338.0"/><line x1="136.0" y1="334.0" x2="136.0" y2="338.0"/><line x1="174.0" y1="334.0" x2="174.0" y2="338.0"/><line x1="212.0" y1="334.0" x2="212.0" y2="338.0"/><line x1="250.0" y1="334.0" x2="250.0" y2="338.0"/><line x1="288.0" y1="334.0" x2="288.0" y2="338.0"/><line x1="326.0" y1="334.0" x2="326.0" y2="338.0"/><line x1="364.0" y1="334.0" x2="364.0" y2="338.0"/></g>
  <text x="60.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">0</text>
  <text x="98.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">1</text>
  <text x="136.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">2</text>
  <text x="174.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">3</text>
  <text x="212.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">4</text>
  <text x="250.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">5</text>
  <text x="288.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">6</text>
  <text x="326.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">7</text>
  <text x="364.0" y="350.0" fill="currentColor" text-anchor="middle" opacity="0.8">8</text>
  <text x="364.0" y="364.0" fill="currentColor" text-anchor="end" opacity="0.8">t (ms)</text>
  <line x1="99.0" y1="360.0" x2="135.0" y2="360.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <line x1="135.0" y1="360.0" x2="99.0" y2="360.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <text x="142.0" y="364.0" fill="currentColor">T = 1 ms: 시계</text>
  <line x1="60" y1="221.3" x2="372" y2="221.3" stroke="currentColor" stroke-width="1.6" stroke-dasharray="7 4"/>
  <text x="378.0" y="225.3" fill="currentColor">x<tspan dy="3" font-size="11">w</tspan><tspan dx="3.3" dy="-3">= 0.030 m</tspan></text>
  <path d="M60.0 308.2L61.9 307.4L63.8 306.7L65.7 305.9L67.6 305.2L69.5 304.4L71.4 303.6L73.3 302.8L75.2 302.0L77.1 301.2L79.0 300.4L80.9 299.6L82.8 298.8L84.7 298.0L86.6 297.1L88.5 296.3L90.4 295.5L92.3 294.6L94.2 293.7L96.1 292.9L98.0 292.0L99.9 291.1L101.8 290.2L103.7 289.4L105.6 288.5L107.5 287.6L109.4 286.6L111.3 285.7L113.2 284.8L115.1 283.9L117.0 283.0L118.9 282.0L120.8 281.1L122.7 280.1L124.6 279.2L126.5 278.2L128.4 277.3L130.3 276.3L132.2 275.3L134.1 274.3L136.0 273.3L137.9 272.4L139.8 271.4L141.7 270.4L143.6 269.4L145.5 268.4L147.4 267.4L149.3 266.3L151.2 265.3L153.1 264.3L155.0 263.3L156.9 262.3L158.8 261.2L160.7 260.2L162.6 259.2L164.5 258.1L166.4 257.1L168.3 256.0L170.2 255.0L172.1 253.9L174.0 252.8L175.9 251.8L177.8 250.7L179.7 249.7L181.6 248.6L183.5 247.5L185.4 246.4L187.3 245.4L189.2 244.3L191.1 243.2L193.0 242.1L194.9 241.0L196.8 240.0L198.7 238.9L200.6 237.8L202.5 236.7L204.4 235.6L206.3 234.5L208.2 233.4L210.1 232.3L212.0 231.2L213.9 230.1L215.8 229.0L217.7 227.9L219.6 226.8L221.5 225.7L223.4 224.6L225.3 223.5L227.2 222.4L229.1 221.3L231.0 220.2L232.9 219.1L234.8 218.0L236.7 216.9L238.6 215.8L240.5 214.7L242.4 213.7L244.3 212.6L246.2 211.5L248.1 210.4L250.0 209.3L251.9 208.2L253.8 207.1L255.7 206.0L257.6 204.9L259.5 203.8L261.4 202.7L263.3 201.6L265.2 200.6L267.1 199.5L269.0 198.4L270.9 197.3L272.8 196.2L274.7 195.2L276.6 194.1L278.5 193.0L280.4 192.0L282.3 190.9L284.2 189.8L286.1 188.8L288.0 187.7L289.9 186.7L291.8 185.6L293.7 184.6L295.6 183.5L297.5 182.5L299.4 181.5L301.3 180.4L303.2 179.4L305.1 178.4L307.0 177.4L308.9 176.3L310.8 175.3L312.7 174.3L314.6 173.3L316.5 172.3L318.4 171.3L320.3 170.3L322.2 169.3L324.1 168.4L326.0 167.4L327.9 166.4L329.8 165.4L331.7 164.5L333.6 163.5L335.5 162.6L337.4 161.6L339.3 160.7L341.2 159.7L343.1 158.8L345.0 157.9L346.9 157.0L348.8 156.0L350.7 155.1L352.6 154.2L354.5 153.3L356.4 152.4L358.3 151.6L360.2 150.7L362.1 149.8L364.0 148.9" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.75"/>
  <polyline points="60.0,308.2 98.0,308.2 98.0,292.0 136.0,292.0 136.0,273.3 174.0,273.3 174.0,252.8 212.0,252.8 212.0,231.2 250.0,231.2 250.0,209.3 288.0,209.3 288.0,187.7 326.0,187.7 326.0,167.4 364.0,167.4" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="98.0,292.0 99.9,291.1 101.8,290.2 103.7,289.4 105.6,288.5 107.5,287.6 109.4,286.6 111.3,285.7 113.2,284.8 115.1,283.9 117.0,283.0 118.9,282.0 120.8,281.1 122.7,280.1 124.6,279.2 126.5,278.2 128.4,277.3 130.3,276.3 132.2,275.3 134.1,274.3 136.0,273.3 136.0,292.0 98.0,292.0" fill="currentColor" fill-opacity="0.28" stroke="none"/>
  <line x1="118.9" y1="285.0" x2="94.2" y2="146.7" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="66.0" y="128.7" fill="currentColor">홀드는 평균 T/2 = 0.5 ms 늦다</text>
  <text x="66.0" y="142.7" fill="currentColor" opacity="0.85">(§2에서 위상 지연이 된다)</text>
  <g fill="currentColor"><circle cx="60.0" cy="308.2" r="3.3"/><circle cx="98.0" cy="292.0" r="3.3"/><circle cx="136.0" cy="273.3" r="3.3"/><circle cx="174.0" cy="252.8" r="3.3"/><circle cx="212.0" cy="231.2" r="3.3"/><circle cx="250.0" cy="209.3" r="3.3"/><circle cx="288.0" cy="187.7" r="3.3"/><circle cx="326.0" cy="167.4" r="3.3"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.4"><path d="M60.0 301.0L65.0 306.0L60.0 311.0L55.0 306.0z"/><path d="M98.0 301.0L103.0 306.0L98.0 311.0L93.0 306.0z"/><path d="M136.0 257.0L141.0 262.0L136.0 267.0L131.0 262.0z"/><path d="M174.0 257.0L179.0 262.0L174.0 267.0L169.0 262.0z"/><path d="M212.0 213.0L217.0 218.0L212.0 223.0L207.0 218.0z"/><path d="M250.0 213.0L255.0 218.0L250.0 223.0L245.0 218.0z"/><path d="M288.0 169.0L293.0 174.0L288.0 179.0L283.0 174.0z"/><path d="M326.0 169.0L331.0 174.0L326.0 179.0L321.0 174.0z"/></g>
  <ellipse cx="269.0" cy="209.3" rx="26" ry="9" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="229.1" y1="214.3" x2="229.1" y2="228.3" stroke="currentColor" stroke-width="1.8"/>
  <line x1="227.1" y1="213.3" x2="189.2" y2="185.0" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="187.3" y="183.0" fill="currentColor" text-anchor="end">참된 교차점</text>
  <line x1="271.0" y1="218.3" x2="285.0" y2="269.8" stroke="currentColor" stroke-width="0.9" opacity="0.7"/>
  <text x="185.4" y="281.8" fill="currentColor">접촉은 눈금(5 ms)에서 시작하고,</text>
  <text x="185.4" y="295.8" fill="currentColor" opacity="0.85">참된 교차점에서 시작하지 않는다</text>
  <line x1="372" y1="131.0" x2="372" y2="173.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <line x1="372" y1="173.0" x2="372" y2="131.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <text x="380.0" y="140.0" fill="currentColor" opacity="1">Δx = 61.4 μm:</text>
  <text x="380.0" y="154.0" fill="currentColor" opacity="0.9">엔코더 한 카운트</text>
  <text x="380.0" y="172.0" fill="currentColor" opacity="1">k<tspan dy="3" font-size="11">w</tspan><tspan dy="-3">·Δx = 400 × 61.4 μm</tspan></text>
  <text x="380.0" y="186.0" fill="currentColor" opacity="0.9">= 0.025 N, 벽 안에서</text>
  <text x="380.0" y="200.0" fill="currentColor" opacity="0.9">가장 작은 힘 단위</text>
  <line x1="378" y1="260.0" x2="392" y2="260.0" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.75"/>
  <circle cx="385" cy="274.0" r="3.3" fill="currentColor"/>
  <polyline points="378,292.0 385,292.0 385,284.0 392,284.0" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <path d="M385 297.0L390 302.0L385 307.0L380 302.0z" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="398.0" y="264.0" fill="currentColor" opacity="0.9">x(t), 30 Hz</text>
  <text x="398.0" y="278.0" fill="currentColor" opacity="0.9">x[n] = x(nT)</text>
  <text x="398.0" y="292.0" fill="currentColor" opacity="0.9">ZOH 출력</text>
  <text x="398.0" y="306.0" fill="currentColor" opacity="0.9">카운트에 스냅한 x[n]</text>
  <text x="14.0" y="394.0" fill="currentColor" opacity="1">두 격자가 만나는 곳: Δx/T = 61.4 mm/s이면 눈금마다 새 카운트가 하나 생긴다.</text>
  <text x="14.0" y="408.0" fill="currentColor" opacity="0.95">이 x(t)는 30.7 mm/s를 넘지 않으므로 한 눈금 걸러 움직임이 없다고 보고하고,</text>
  <text x="14.0" y="422.0" fill="currentColor" opacity="0.95">위치를 차분해 얻은 속도는 0이었다가 61.4 mm/s로 튄다.</text>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3**, 곧 $1\,\mathrm{kHz}$ 서보로 도는 햅틱 핸들에서는 이상 샘플러가 $T=1\,\mathrm{ms}$마다 $x[n]=x(nT)$를 읽고(나이퀴스트 $500\,\mathrm{Hz}$; §2) 영차 홀드(§2에서 정의·유도)가 그 표본을 평균 $T/2=0.5\,\mathrm{ms}$ 늦은 계단으로 바꾸므로, 벽($x_w=0.030\,\mathrm{m}$)과의 접촉은 참된 교차점이 아니라 눈금($5\,\mathrm{ms}$)에서 시작한다. 흐린 수평 격자는 엔코더 한 카운트 $\Delta x=61.4\,\mu\mathrm{m}$이고, 벽 안에서 한 카운트는 가장 작은 힘 단위인 $k_w\,\Delta x=0.025\,\mathrm{N}$에 해당한다. 두 격자는 눈금마다 새 카운트 하나가 생기는 $\Delta x/T=61.4\,\mathrm{mm/s}$에서 만나는데, 이 핸들은 $30.7\,\mathrm{mm/s}$를 넘지 않으므로 한 눈금 걸러 움직임이 없다고 보고하고, 위치를 차분해 얻은 속도는 $0$이었다가 $61.4\,\mathrm{mm/s}$로 튄다.

### 1. 신호, 시스템, 합성곱

- **시스템** $T$는 입력 수열 $x[n]$을 출력 수열 $y[n] = T\{x\}[n]$으로 바꾸는 규칙이다.
  $n$은 정수 샘플 번호다. 시스템이 **두** 성질을 모두 가지면 **LTI**(선형 시불변)라 하고,
  둘은 서로 따로 깨질 수 있다.
- **선형성**은 가법성과 동차성을 함께 뜻한다. 즉 중첩 원리다(비예시까지 담은 완전한 정의는
  [[02-foundations/engineering-math|0.5 §4.5]]). 모든 입력 $x_1, x_2$와 모든 스칼라 $a, b$에 대해
  $$T\{a x_1[n] + b x_2[n]\} = a\,T\{x_1[n]\} + b\,T\{x_2[n]\}$$
  이므로 입력의 가중합은 출력의 같은 가중합으로 나온다.
  *비예시:* 제곱기 $y[n] = x[n]^2$. 상수 입력 $1$과 $2$는 출력 $1$과 $4$를 주지만, 그 합
  $3$은 $9 \ne 1 + 4 = 5$를 준다.
- **시불변성**(이동 불변성): 입력을 $n_0$ 샘플 늦추면 출력도 같은 $n_0$만큼만 늦춰진다.
  $$x[n] \mapsto y[n] \implies x[n-n_0] \mapsto y[n-n_0]$$
  여기서 $\mapsto$는 "시스템이 이 입력을 이 출력으로 바꾼다"로 읽고, $n_0$은 임의의 정수
  이동량이다. 규칙이 시계를 보지 않으면 성립한다. 늦게 도착한 입력도 일찍 왔을 때와 똑같이
  다뤄지기 때문이다. *비예시:* 램프 이득 $y[n] = n\,x[n]$은 선형이지만 시불변이 아니다.
  $n = 0$의 임펄스는 전부 0인 출력을 내는데, 같은 임펄스를 $n = 1$에 넣으면 $n = 1$에서
  $1$이 나오고, 이것은 0을 옮긴 것이 아니기 때문이다.
- *둘 다 통과하는 예:* 연속 합 $y[n] = x[n] + x[n-1]$. 입력을 더하거나 배수하면 두 항이
  함께 더해지거나 배수되므로 선형이다. $n$과 $n-1$만 참조하므로 늦춘 입력은 늦춘 출력을
  준다.
- **단위 임펄스**는 $n = 0$에서 $1$, 나머지에서 $0$인 $\delta[n]$이고, **임펄스 응답**은
  시스템이 그것에 하는 일, $h[n] = T\{\delta\}[n]$이다. 연속 합이라면 $h = [1, 1]$이다.
- **결과.** LTI 시스템은 임펄스 응답 $h$로 완전히 특성화되고, 출력은 입력과 $h$의
  **합성곱**이다:
  $$y[n] = (x * h)[n] = \sum_k x[k]\, h[n-k]$$
  $k$는 모든 입력 샘플을 훑고, $x[k]$는 시각 $k$의 입력, $h[n-k]$는 그 샘플 하나에 대한
  응답을 $k$에서 시작하도록 늦춘 것이다. 그래서 합성곱은 두 수열을 받아 셋째 수열을 돌려주는
  연산이다. 입력 샘플 하나씩으로 배수한, 늦춰진 $h$ 복사본들의 합이다.
- **이것이 어디서 오는가 — 합성곱은 정의가 아니라 강제된 결과다.** 세 줄이면 된다. 첫째,
  어떤 신호든 옮겨진 임펄스의 합이다. 이건 항등식이다: $x[n] = \sum_k x[k]\,\delta[n-k]$.
  이것을 시스템 $T$에 통과시키고 *선형성*으로 $T$를 합 안으로 밀어 넣는다:
  $y[n] = T\{\sum_k x[k]\delta[n-k]\} = \sum_k x[k]\,T\{\delta[n-k]\}$. 이제 *시불변성*을
  쓴다. $k$에서의 임펄스에 대한 응답은 $0$에서의 응답을 옮긴 것이다 —
  $T\{\delta[n-k]\} = h[n-k]$. 대입하면 위의 식이 나온다. 그러므로 저 합은 모델링 선택이
  아니다. **시스템이 선형이고 시불변이면 합성곱을 하며, 다른 것을 할 여지가 없다.** 측정
  하나 — 임펄스 응답 — 가 시스템을 완전히 결정하는 이유이고, 주파수 영역 도구 전체가
  존재하는 이유이기도 하다. 대각화할 연산이 합성곱 하나뿐이기 때문이다.
- 계산 예제: $x = [1, 2, 3]$, $h = [1, 1]$(연속 합):
  $y = [1,\ 1{+}2,\ 2{+}3,\ 3] = [1, 3, 5, 3]$ — 뒤집고, 밀고, 곱하고, 누적한다.
  길이: $N_x + N_h - 1$.
- CNN 층은 이런 $h$들의 *학습된 2D 묶음*(+ 비선형성)이다 — 실제 프레임워크는 커널을
  뒤집지 않는 교차상관(cross-correlation) $(x \star h)[n] = \sum_k x[n+k]\,h[k]$을 계산하지만, 커널이 학습되므로 기능상 차이가
  없어 관례적으로 convolution이라 부른다 —
  [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] 이후 전부; "패딩/스트라이드"는 같은 연산의
  경계·샘플링 선택지다.
- 핵심 성질: 교환 법칙($x * h = h * x$), 결합 법칙($(x * h_1) * h_2 = x * (h_1 * h_2)$,
  그래서 직렬 LTI = 합성곱된 $h$ 하나), $\delta$가 항등원($x * \delta = x$).
- **인과성**은 시스템의 성질이다. 시각 $n$의 출력은 현재와 과거 입력, 즉 $k \le n$인
  $x[k]$만 쓸 수 있다. LTI 시스템에서는 임펄스 응답에 대한 조건 하나가 된다.
  $$h[n] = 0 \quad \text{for all } n < 0$$
  $h[-1]$이 0이 아니면 시각 $n+1$의 입력이 시각 $n$의 출력에 닿기 때문이다. 연속 합은
  인과적이다. 중심 평균 $y[n] = \tfrac12\big(x[n+1] + x[n-1]\big)$은 다음 샘플이 필요하므로
  인과적이지 않다. 실시간으로 돌 수 있는 것은 인과 필터뿐이고, §4의 위상 지연이 여기서 나온다.
- **BIBO 안정성**(유계 입력, 유계 출력)도 시스템의 성질이다. 모든 $n$에서
  $|x[n]| \le B_x$인 모든 입력에 대해 출력도 어떤 유한한 한계 아래에 머문다. LTI
  시스템에서는 임펄스 응답이 절대 합산 가능할 때와 정확히 같다.
  $$\sum_n |h[n]| < \infty$$
  $|y[n]| \le \sum_k |x[n-k]|\,|h[k]| \le B_x \sum_k |h[k]|$이기 때문이다. 연속 합은
  통과한다($\sum_n |h[n]| = 2$). 모든 $n \ge 0$에서 $h[n] = 1$인 누산기 $y[n] = y[n-1] + x[n]$은
  실패한다. 상수 입력 $1$이 출력을 $1, 2, 3, \ldots$으로 한없이 키운다. §5는 같은 판정을
  "극점이 단위원 안"으로 다시 쓴다.

짧은 물리 사건도 센서·필터 응답을 통해 뒤의 여러 표본에 영향을 줘 합성곱이 유용하다. 도구가 벽에 닿는 힘 펄스는 접촉이 급격해도 퍼져 보일 수 있다. **여기서 얻는 독법.** 넓게 측정된 사건이 세계의 성질인지 파이프라인 임펄스 응답인지 묻는다. 직렬 필터가 응답을 함께 바꾸므로 필터 하나의 평가로는 제어기가 겪는 시점을 놓칠 수 있다.

### 2. 샘플링 — 연속과 디지털 사이의 계약

- **샘플링**은 연속시간 신호 $x_c(t)$를 $T_s$초마다 한 번씩 읽는 것이다.
  $x[n] = x_c(nT_s)$이므로 **샘플링 주파수**는 초당 $f_s = 1/T_s$개(Hz)다. 그 절반 $f_s/2$가
  **나이퀴스트 주파수**, 즉 샘플이 모호함 없이 표현할 수 있는 가장 높은 주파수다.
- **나이퀴스트–섀넌 샘플링 정리.** 조건이 둘이다. 신호가 $B$ Hz로 **대역 제한**되어
  있어야 하고($B$ 위 성분이 없음), *그리고* 샘플링 주파수가 그 대역 끝의 두 배인
  **나이퀴스트 율** $2B$보다 커야 한다.
  $$f_s > 2B$$
  그러면 신호는 샘플에서 *완벽히* 복원된다. 샘플링은 스펙트럼 복사본을 $f_s$ 간격으로
  만드는데, 이 조건에서는 복사본끼리 겹치지 않기 때문이다(아래에서 증명). 예: 20 kHz로 대역 제한된 오디오는
  $f_s > 40$ kHz가 필요하고, 그래서 CD 오디오가 44.1 kHz를 쓴다.
- **정리가 성립하는 이유 — 네 단계 증명.** 연속시간 푸리에 변환이 필요하다. [[02-foundations/engineering-math|0.5 §7]]의 "거꾸로 돌려 평균하기"를 시간에 대한 적분으로 한 것이다(§3의 주파수 응답은 이것의 수열 판이다):
  $$X_c(f) = \int_{-\infty}^{\infty} x_c(t)\,e^{-j2\pi ft}\,dt, \qquad x_c(t) = \int_{-\infty}^{\infty} X_c(f)\,e^{j2\pi ft}\,df$$
  "$B$로 대역 제한"은 $|f| > B$에서 $X_c(f) = 0$이라는 뜻이다.
  *1단계, 샘플은 접힌 스펙트럼만 본다.* 역변환에 $t = nT_s$를 넣고 주파수 축을 폭 $f_s$의 띠로 자른다. $|f'| \le f_s/2$, $k$는 임의의 정수로 $f = f' + kf_s$라 쓴다. $e^{j2\pi kf_s nT_s} = e^{j2\pi kn} = 1$이므로
  $$x[n] = \int_{-f_s/2}^{f_s/2} \Big(\sum_{k=-\infty}^{\infty} X_c(f' + kf_s)\Big)\,e^{j2\pi f' nT_s}\,df'$$
  이다. 그래서 샘플은 $f_s$의 모든 배수만큼 옮긴 복사본들의 합을 통해서만 $X_c$에 의존한다. 위에서 말한 "스펙트럼 복사본"이 이것이다.
  *2단계, $f_s > 2B$이면 복사본이 띠를 비켜 간다.* $|f'| \le f_s/2$이고 $k \ne 0$이면 $|f' + kf_s| \ge f_s/2 > B$이므로, 그곳에서는 $k = 0$ 말고 모든 복사본이 0이고 괄호는 $X_c(f')$ 자체다. 그러면 샘플은 그 띠 위에서 $X_c$의 푸리에 급수 계수이고, 계수가 함수를 정한다: $|f| < f_s/2$에서 $X_c(f) = T_s\sum_n x[n]\,e^{-j2\pi fnT_s}$.
  *3단계, 신호를 다시 짓는다.* 그것을 역변환에 되넣는다. 샘플 $n$은 $x[n]\,T_s\int_{-f_s/2}^{f_s/2} e^{j2\pi f(t - nT_s)}\,df$를 보태고, 이 적분은 sinc 펄스가 된다:
  $$x_c(t) = \sum_n x[n]\,\operatorname{sinc}\Big(\frac{t - nT_s}{T_s}\Big), \qquad \operatorname{sinc}(u) = \frac{\sin \pi u}{\pi u}$$
  각 펄스는 자기 샘플 순간에 1, 다른 모든 샘플 순간에 0이므로, 합은 모든 샘플을 지나며 그 사이를 채운다. 이것이 정리의 "완벽히 복원"이고, 주파수 영역에서는 차단 주파수 $f_s/2$인 이상적 저역 통과 필터(§4)다.
  *4단계, 실패는 곧 에일리어싱이다.* $f_s \le 2B$이면 $k \ne 0$인 어떤 복사본이 띠 안에 들어와 $X_c(f')$에 더해진다. 주파수 $f$의 음이 $f - kf_s$에서 세어지고, 이것이 아래의 에일리어싱 공식이다.
  *수치 확인:* $1.3$ Hz와 $2.9$ Hz 음을 $f_s = 10$ Hz로 샘플링하면($2B = 5.8 < 10$) $t = 0.5$ s에서 $-0.630653$으로 복원되어 참값과 소수 여섯째 자리까지 같다($t$에 가장 가까운 샘플 8,001개를 합함). 같은 샘플링 주파수의 $7$ Hz 음은 $t = 0.123$ s에서 $-0.680$으로 복원되는데, 이것은 에일리어스인 $3$ Hz 코사인의 값이고 참 $7$ Hz 값은 $+0.642$다.
- **계산: $1\,\mathrm{kHz}$의 장치 P3.** 햅틱 서보는 $T=10^{-3}\,\mathrm{s}$이므로 $f_s=1000\,\mathrm{Hz}$, 나이퀴스트 $500\,\mathrm{Hz}$([[02-foundations/lab-plants|0.6]]). $30\,\mathrm{Hz}$ 아래 접촉은 정리 안쪽이고 샘플링이 병목이 아니다. 엔코더 한 카운트 $\Delta x=61.4\,\mu\mathrm{m}$은 공간 양자화이지 $T_s$가 아니다. $N$을 올리면 공간이, $f_s$를 올리면 시간이 줄어든다. 과제는 이 샘플러+ZOH 그림이다.
- **영차 홀드(zero-order hold, ZOH).** 그림의 계단이 그리는 것, 곧 샘플에서 연속 신호로 돌아가는 단계다. 각 샘플을 다음 샘플까지 유지한다:
  $$x_h(t) = x[n] \quad \text{for } nT \le t < (n+1)T$$
  그래서 출력은 조각마다 일정하고, 눈금마다 튀며, 미래 샘플을 쓰지 않는다(인과적이다). DAC나 서보가 실제로 하는 복원이 이것이고, 아직 도착하지 않은 샘플이 필요한 위의 sinc 합을 대신한다. *왜 평균 $T/2$ 늦는가:* 구간 $n$ 안의 시각 $t$에서 유지되는 값은 $x(nT)$, 곧 $t - nT$초 묵은 측정이고, 그 나이는 $0$에서 $T$까지 고르게 퍼지므로 평균 $T/2$다. 경사 $x = vt$라면 계단은 평균 $T/2$ 늦게 옮긴 경사다. 주파수 응답도 같은 것을 정확히 말한다. 홀드의 임펄스 응답은 폭 $T$의 단위 펄스이고, 그 변환은
  $$H_{\text{zoh}}(f) = \int_0^T e^{-j2\pi ft}\,dt = T\,e^{-j\pi fT}\operatorname{sinc}(fT)$$
  로, 순수한 $T/2$ 지연(위상 $-\pi fT$, 모든 주파수에서 군지연 $T/2$, §4)에 완만한 이득 처짐을 곱한 것이다. P3($T = 1$ ms)에서 $30$ Hz의 위상은 $-5.4°$, 이득은 DC 값 $T$의 $0.9985$배이고, $500$ Hz 나이퀴스트 주파수에서는 $-90°$와 그 $0.637$배다. 스프링 $K$를 렌더링하는 루프에서 안정성을 깎는 것은 이 지연이다: $T/2$ 늦게 느끼는 스프링 $K\,x(t - T/2) \approx Kx - K\tfrac{T}{2}\dot x$는 음의 감쇠 $KT/2$로 작용하고, 이것이 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]의 햅틱 벽 한계식에 들어 있는 항이다.
- **에일리어싱**은 조건이 깨질 때 벌어지는 일이다. $f_s/2$ 위의 주파수 $f$ 성분은 샘플에서
  $$f_{alias} = |f - k f_s|$$
  에 나타난다. $k$는 $f/f_s$에 가장 가까운 정수이고, 그래서 $f_{alias}$가 $0$과 $f_s/2$
  사이에 떨어진다. 실제 음과 그 에일리어스는 똑같은 샘플을 만들므로 뒤의 어떤 처리로도 둘을
  가를 수 없다. 카메라 속 바퀴가 거꾸로 돌고, 50 Hz로 샘플링한 60 Hz 진동($k = 1$)은 10 Hz로
  위장하며, 아래 그림에서는 200 Hz로 샘플링한 170 Hz($k = 1$)가 30 Hz가 된다.

<svg viewBox="0 0 480 152" style="max-width:100%;height:auto" role="img" aria-label="에일리어싱: 200 Hz로 샘플링한 170 Hz 신호가 30 Hz로 보인다">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="25" y1="75" x2="460" y2="75"/></g>
  <path d="M25.0 75.0L25.7 72.4L26.4 69.9L27.1 67.4L27.9 64.9L28.6 62.4L29.3 60.0L30.0 57.7L30.7 55.4L31.4 53.2L32.2 51.1L32.9 49.1L33.6 47.2L34.3 45.4L35.0 43.7L35.8 42.2L36.5 40.8L37.2 39.5L37.9 38.4L38.6 37.5L39.3 36.7L40.0 36.0L40.8 35.5L41.5 35.2L42.2 35.0L42.9 35.0L43.6 35.2L44.4 35.5L45.1 36.0L45.8 36.6L46.5 37.5L47.2 38.4L47.9 39.5L48.7 40.8L49.4 42.2L50.1 43.7L50.8 45.4L51.5 47.1L52.2 49.0L53.0 51.0L53.7 53.1L54.4 55.3L55.1 57.6L55.8 59.9L56.5 62.4L57.2 64.8L58.0 67.3L58.7 69.8L59.4 72.4L60.1 74.9L60.8 77.5L61.5 80.1L62.3 82.6L63.0 85.1L63.7 87.6L64.4 90.0L65.1 92.3L65.8 94.6L66.6 96.8L67.3 98.9L68.0 100.9L68.7 102.8L69.4 104.6L70.2 106.2L70.9 107.8L71.6 109.2L72.3 110.4L73.0 111.5L73.7 112.5L74.4 113.3L75.2 114.0L75.9 114.5L76.6 114.8L77.3 115.0L78.0 115.0L78.8 114.8L79.5 114.5L80.2 114.0L80.9 113.4L81.6 112.6L82.3 111.6L83.1 110.5L83.8 109.2L84.5 107.9L85.2 106.3L85.9 104.7L86.6 102.9L87.3 101.0L88.1 99.0L88.8 96.9L89.5 94.7L90.2 92.4L90.9 90.1L91.7 87.7L92.4 85.2L93.1 82.7L93.8 80.2L94.5 77.7L95.2 75.1L96.0 72.5L96.7 70.0L97.4 67.5L98.1 65.0L98.8 62.5L99.5 60.1L100.3 57.7L101.0 55.5L101.7 53.3L102.4 51.2L103.1 49.2L103.8 47.3L104.5 45.5L105.3 43.8L106.0 42.3L106.7 40.9L107.4 39.6L108.1 38.5L108.8 37.5L109.6 36.7L110.3 36.0L111.0 35.5L111.7 35.2L112.4 35.0L113.2 35.0L113.9 35.2L114.6 35.5L115.3 36.0L116.0 36.6L116.7 37.4L117.4 38.4L118.2 39.5L118.9 40.7L119.6 42.1L120.3 43.6L121.0 45.3L121.8 47.1L122.5 49.0L123.2 51.0L123.9 53.1L124.6 55.2L125.3 57.5L126.0 59.9L126.8 62.3L127.5 64.7L128.2 67.2L128.9 69.7L129.6 72.3L130.3 74.8L131.1 77.4L131.8 80.0L132.5 82.5L133.2 85.0L133.9 87.5L134.7 89.9L135.4 92.2L136.1 94.5L136.8 96.7L137.5 98.8L138.2 100.8L138.9 102.7L139.7 104.5L140.4 106.2L141.1 107.7L141.8 109.1L142.5 110.4L143.2 111.5L144.0 112.5L144.7 113.3L145.4 114.0L146.1 114.5L146.8 114.8L147.6 115.0L148.3 115.0L149.0 114.8L149.7 114.5L150.4 114.0L151.1 113.4L151.8 112.6L152.6 111.7L153.3 110.5L154.0 109.3L154.7 107.9L155.4 106.4L156.1 104.7L156.9 103.0L157.6 101.1L158.3 99.1L159.0 97.0L159.7 94.8L160.5 92.5L161.2 90.2L161.9 87.8L162.6 85.3L163.3 82.8L164.0 80.3L164.8 77.8L165.5 75.2L166.2 72.6L166.9 70.1L167.6 67.6L168.3 65.1L169.1 62.6L169.8 60.2L170.5 57.8L171.2 55.6L171.9 53.4L172.6 51.2L173.3 49.2L174.1 47.3L174.8 45.5L175.5 43.9L176.2 42.3L176.9 40.9L177.6 39.6L178.4 38.5L179.1 37.5L179.8 36.7L180.5 36.1L181.2 35.5L182.0 35.2L182.7 35.0L183.4 35.0L184.1 35.2L184.8 35.5L185.5 36.0L186.2 36.6L187.0 37.4L187.7 38.3L188.4 39.4L189.1 40.7L189.8 42.1L190.6 43.6L191.3 45.2L192.0 47.0L192.7 48.9L193.4 50.9L194.1 53.0L194.9 55.2L195.6 57.4L196.3 59.8L197.0 62.2L197.7 64.6L198.4 67.1L199.2 69.6L199.9 72.2L200.6 74.7L201.3 77.3L202.0 79.9L202.7 82.4L203.4 84.9L204.2 87.4L204.9 89.8L205.6 92.1L206.3 94.4L207.0 96.6L207.8 98.7L208.5 100.7L209.2 102.6L209.9 104.4L210.6 106.1L211.3 107.7L212.0 109.1L212.8 110.3L213.5 111.5L214.2 112.4L214.9 113.3L215.6 113.9L216.3 114.4L217.1 114.8L217.8 115.0L218.5 115.0L219.2 114.8L219.9 114.5L220.7 114.1L221.4 113.4L222.1 112.6L222.8 111.7L223.5 110.6L224.2 109.4L224.9 108.0L225.7 106.5L226.4 104.8L227.1 103.0L227.8 101.1L228.5 99.2L229.3 97.1L230.0 94.9L230.7 92.6L231.4 90.3L232.1 87.9L232.8 85.4L233.6 82.9L234.3 80.4L235.0 77.9L235.7 75.3L236.4 72.7L237.1 70.2L237.8 67.7L238.6 65.1L239.3 62.7L240.0 60.3L240.7 57.9L241.4 55.6L242.2 53.4L242.9 51.3L243.6 49.3L244.3 47.4L245.0 45.6L245.7 43.9L246.4 42.4L247.2 41.0L247.9 39.7L248.6 38.6L249.3 37.6L250.0 36.7L250.8 36.1L251.5 35.6L252.2 35.2L252.9 35.0L253.6 35.0L254.3 35.2L255.1 35.5L255.8 35.9L256.5 36.6L257.2 37.3L257.9 38.3L258.6 39.4L259.3 40.6L260.1 42.0L260.8 43.5L261.5 45.2L262.2 46.9L262.9 48.8L263.6 50.8L264.4 52.9L265.1 55.1L265.8 57.3L266.5 59.7L267.2 62.1L267.9 64.5L268.7 67.0L269.4 69.5L270.1 72.1L270.8 74.6L271.5 77.2L272.2 79.8L273.0 82.3L273.7 84.8L274.4 87.3L275.1 89.7L275.8 92.0L276.6 94.3L277.3 96.5L278.0 98.6L278.7 100.7L279.4 102.6L280.1 104.4L280.9 106.0L281.6 107.6L282.3 109.0L283.0 110.3L283.7 111.4L284.4 112.4L285.2 113.2L285.9 113.9L286.6 114.4L287.3 114.8L288.0 115.0L288.7 115.0L289.4 114.8L290.2 114.5L290.9 114.1L291.6 113.5L292.3 112.7L293.0 111.7L293.8 110.6L294.5 109.4L295.2 108.0L295.9 106.5L296.6 104.9L297.3 103.1L298.1 101.2L298.8 99.2L299.5 97.1L300.2 95.0L300.9 92.7L301.6 90.4L302.3 88.0L303.1 85.5L303.8 83.0L304.5 80.5L305.2 78.0L305.9 75.4L306.7 72.8L307.4 70.3L308.1 67.8L308.8 65.2L309.5 62.8L310.2 60.4L311.0 58.0L311.7 55.7L312.4 53.5L313.1 51.4L313.8 49.4L314.5 47.5L315.2 45.7L316.0 44.0L316.7 42.4L317.4 41.0L318.1 39.7L318.8 38.6L319.6 37.6L320.3 36.8L321.0 36.1L321.7 35.6L322.4 35.2L323.1 35.0L323.9 35.0L324.6 35.1L325.3 35.4L326.0 35.9L326.7 36.5L327.4 37.3L328.1 38.3L328.9 39.3L329.6 40.6L330.3 41.9L331.0 43.5L331.7 45.1L332.4 46.9L333.2 48.7L333.9 50.7L334.6 52.8L335.3 55.0L336.0 57.2L336.8 59.6L337.5 62.0L338.2 64.4L338.9 66.9L339.6 69.4L340.3 72.0L341.1 74.5L341.8 77.1L342.5 79.7L343.2 82.2L343.9 84.7L344.6 87.2L345.3 89.6L346.1 91.9L346.8 94.2L347.5 96.4L348.2 98.6L348.9 100.6L349.7 102.5L350.4 104.3L351.1 106.0L351.8 107.5L352.5 109.0L353.2 110.2L353.9 111.4L354.7 112.4L355.4 113.2L356.1 113.9L356.8 114.4L357.5 114.8L358.2 115.0L359.0 115.0L359.7 114.9L360.4 114.6L361.1 114.1L361.8 113.5L362.6 112.7L363.3 111.8L364.0 110.7L364.7 109.5L365.4 108.1L366.1 106.6L366.8 104.9L367.6 103.2L368.3 101.3L369.0 99.3L369.7 97.2L370.4 95.1L371.1 92.8L371.9 90.5L372.6 88.1L373.3 85.6L374.0 83.1L374.7 80.6L375.4 78.1L376.2 75.5L376.9 72.9L377.6 70.4L378.3 67.9L379.0 65.3L379.8 62.9L380.5 60.5L381.2 58.1L381.9 55.8L382.6 53.6L383.3 51.5L384.1 49.5L384.8 47.5L385.5 45.7L386.2 44.1L386.9 42.5L387.6 41.1L388.4 39.8L389.1 38.6L389.8 37.6L390.5 36.8L391.2 36.1L391.9 35.6L392.6 35.2L393.4 35.0L394.1 35.0L394.8 35.1L395.5 35.4L396.2 35.9L396.9 36.5L397.7 37.3L398.4 38.2L399.1 39.3L399.8 40.5L400.5 41.9L401.2 43.4L402.0 45.0L402.7 46.8L403.4 48.7L404.1 50.6L404.8 52.7L405.6 54.9L406.3 57.2L407.0 59.5L407.7 61.9L408.4 64.3L409.1 66.8L409.9 69.3L410.6 71.9L411.3 74.4L412.0 77.0L412.7 79.6L413.4 82.1L414.2 84.6L414.9 87.1L415.6 89.5L416.3 91.8L417.0 94.1L417.7 96.3L418.4 98.5L419.2 100.5L419.9 102.4L420.6 104.2L421.3 105.9L422.0 107.5L422.8 108.9L423.5 110.2L424.2 111.3L424.9 112.3L425.6 113.2L426.3 113.9L427.1 114.4L427.8 114.8L428.5 115.0L429.2 115.0L429.9 114.9L430.6 114.6L431.4 114.1L432.1 113.5L432.8 112.7L433.5 111.8L434.2 110.7L434.9 109.5L435.7 108.1L436.4 106.6L437.1 105.0L437.8 103.2L438.5 101.4L439.2 99.4L439.9 97.3L440.7 95.1L441.4 92.9L442.1 90.6L442.8 88.2L443.5 85.7L444.3 83.2L445.0 80.7L445.7 78.2L446.4 75.6L447.1 73.0L447.8 70.5L448.6 67.9L449.3 65.4L450.0 63.0L450.7 60.6L451.4 58.2L452.1 55.9L452.9 53.7L453.6 51.6L454.3 49.5L455.0 47.6" fill="none" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <path d="M25.0 75.0L25.7 75.5L26.4 75.9L27.1 76.4L27.9 76.8L28.6 77.3L29.3 77.7L30.0 78.2L30.7 78.6L31.4 79.1L32.2 79.5L32.9 80.0L33.6 80.4L34.3 80.9L35.0 81.3L35.8 81.8L36.5 82.2L37.2 82.6L37.9 83.1L38.6 83.5L39.3 84.0L40.0 84.4L40.8 84.9L41.5 85.3L42.2 85.7L42.9 86.2L43.6 86.6L44.4 87.0L45.1 87.5L45.8 87.9L46.5 88.3L47.2 88.7L47.9 89.2L48.7 89.6L49.4 90.0L50.1 90.4L50.8 90.8L51.5 91.3L52.2 91.7L53.0 92.1L53.7 92.5L54.4 92.9L55.1 93.3L55.8 93.7L56.5 94.1L57.2 94.5L58.0 94.9L58.7 95.3L59.4 95.7L60.1 96.0L60.8 96.4L61.5 96.8L62.3 97.2L63.0 97.6L63.7 97.9L64.4 98.3L65.1 98.7L65.8 99.0L66.6 99.4L67.3 99.8L68.0 100.1L68.7 100.5L69.4 100.8L70.2 101.1L70.9 101.5L71.6 101.8L72.3 102.2L73.0 102.5L73.7 102.8L74.4 103.1L75.2 103.5L75.9 103.8L76.6 104.1L77.3 104.4L78.0 104.7L78.8 105.0L79.5 105.3L80.2 105.6L80.9 105.9L81.6 106.2L82.3 106.5L83.1 106.7L83.8 107.0L84.5 107.3L85.2 107.5L85.9 107.8L86.6 108.1L87.3 108.3L88.1 108.6L88.8 108.8L89.5 109.0L90.2 109.3L90.9 109.5L91.7 109.7L92.4 110.0L93.1 110.2L93.8 110.4L94.5 110.6L95.2 110.8L96.0 111.0L96.7 111.2L97.4 111.4L98.1 111.6L98.8 111.7L99.5 111.9L100.3 112.1L101.0 112.3L101.7 112.4L102.4 112.6L103.1 112.7L103.8 112.9L104.5 113.0L105.3 113.2L106.0 113.3L106.7 113.4L107.4 113.5L108.1 113.7L108.8 113.8L109.6 113.9L110.3 114.0L111.0 114.1L111.7 114.2L112.4 114.3L113.2 114.4L113.9 114.4L114.6 114.5L115.3 114.6L116.0 114.6L116.7 114.7L117.4 114.8L118.2 114.8L118.9 114.8L119.6 114.9L120.3 114.9L121.0 114.9L121.8 115.0L122.5 115.0L123.2 115.0L123.9 115.0L124.6 115.0L125.3 115.0L126.0 115.0L126.8 115.0L127.5 115.0L128.2 114.9L128.9 114.9L129.6 114.9L130.3 114.8L131.1 114.8L131.8 114.7L132.5 114.7L133.2 114.6L133.9 114.6L134.7 114.5L135.4 114.4L136.1 114.3L136.8 114.3L137.5 114.2L138.2 114.1L138.9 114.0L139.7 113.9L140.4 113.8L141.1 113.6L141.8 113.5L142.5 113.4L143.2 113.3L144.0 113.1L144.7 113.0L145.4 112.9L146.1 112.7L146.8 112.5L147.6 112.4L148.3 112.2L149.0 112.1L149.7 111.9L150.4 111.7L151.1 111.5L151.8 111.3L152.6 111.2L153.3 111.0L154.0 110.8L154.7 110.5L155.4 110.3L156.1 110.1L156.9 109.9L157.6 109.7L158.3 109.5L159.0 109.2L159.7 109.0L160.5 108.7L161.2 108.5L161.9 108.3L162.6 108.0L163.3 107.7L164.0 107.5L164.8 107.2L165.5 106.9L166.2 106.7L166.9 106.4L167.6 106.1L168.3 105.8L169.1 105.5L169.8 105.2L170.5 104.9L171.2 104.6L171.9 104.3L172.6 104.0L173.3 103.7L174.1 103.4L174.8 103.1L175.5 102.7L176.2 102.4L176.9 102.1L177.6 101.8L178.4 101.4L179.1 101.1L179.8 100.7L180.5 100.4L181.2 100.0L182.0 99.7L182.7 99.3L183.4 99.0L184.1 98.6L184.8 98.2L185.5 97.9L186.2 97.5L187.0 97.1L187.7 96.7L188.4 96.3L189.1 96.0L189.8 95.6L190.6 95.2L191.3 94.8L192.0 94.4L192.7 94.0L193.4 93.6L194.1 93.2L194.9 92.8L195.6 92.4L196.3 92.0L197.0 91.6L197.7 91.2L198.4 90.7L199.2 90.3L199.9 89.9L200.6 89.5L201.3 89.1L202.0 88.6L202.7 88.2L203.4 87.8L204.2 87.4L204.9 86.9L205.6 86.5L206.3 86.1L207.0 85.6L207.8 85.2L208.5 84.8L209.2 84.3L209.9 83.9L210.6 83.4L211.3 83.0L212.0 82.5L212.8 82.1L213.5 81.7L214.2 81.2L214.9 80.8L215.6 80.3L216.3 79.9L217.1 79.4L217.8 79.0L218.5 78.5L219.2 78.1L219.9 77.6L220.7 77.2L221.4 76.7L222.1 76.3L222.8 75.8L223.5 75.4L224.2 74.9L224.9 74.4L225.7 74.0L226.4 73.5L227.1 73.1L227.8 72.6L228.5 72.2L229.3 71.7L230.0 71.3L230.7 70.8L231.4 70.4L232.1 69.9L232.8 69.5L233.6 69.0L234.3 68.6L235.0 68.1L235.7 67.7L236.4 67.3L237.1 66.8L237.8 66.4L238.6 65.9L239.3 65.5L240.0 65.1L240.7 64.6L241.4 64.2L242.2 63.7L242.9 63.3L243.6 62.9L244.3 62.4L245.0 62.0L245.7 61.6L246.4 61.2L247.2 60.7L247.9 60.3L248.6 59.9L249.3 59.5L250.0 59.1L250.8 58.7L251.5 58.2L252.2 57.8L252.9 57.4L253.6 57.0L254.3 56.6L255.1 56.2L255.8 55.8L256.5 55.4L257.2 55.0L257.9 54.6L258.6 54.3L259.3 53.9L260.1 53.5L260.8 53.1L261.5 52.7L262.2 52.4L262.9 52.0L263.6 51.6L264.4 51.2L265.1 50.9L265.8 50.5L266.5 50.2L267.2 49.8L267.9 49.5L268.7 49.1L269.4 48.8L270.1 48.4L270.8 48.1L271.5 47.8L272.2 47.4L273.0 47.1L273.7 46.8L274.4 46.5L275.1 46.2L275.8 45.8L276.6 45.5L277.3 45.2L278.0 44.9L278.7 44.6L279.4 44.3L280.1 44.1L280.9 43.8L281.6 43.5L282.3 43.2L283.0 42.9L283.7 42.7L284.4 42.4L285.2 42.1L285.9 41.9L286.6 41.6L287.3 41.4L288.0 41.1L288.7 40.9L289.4 40.7L290.2 40.4L290.9 40.2L291.6 40.0L292.3 39.8L293.0 39.6L293.8 39.4L294.5 39.2L295.2 39.0L295.9 38.8L296.6 38.6L297.3 38.4L298.1 38.2L298.8 38.0L299.5 37.9L300.2 37.7L300.9 37.5L301.6 37.4L302.3 37.2L303.1 37.1L303.8 36.9L304.5 36.8L305.2 36.7L305.9 36.5L306.7 36.4L307.4 36.3L308.1 36.2L308.8 36.1L309.5 36.0L310.2 35.9L311.0 35.8L311.7 35.7L312.4 35.6L313.1 35.5L313.8 35.5L314.5 35.4L315.2 35.3L316.0 35.3L316.7 35.2L317.4 35.2L318.1 35.2L318.8 35.1L319.6 35.1L320.3 35.1L321.0 35.0L321.7 35.0L322.4 35.0L323.1 35.0L323.9 35.0L324.6 35.0L325.3 35.0L326.0 35.0L326.7 35.0L327.4 35.1L328.1 35.1L328.9 35.1L329.6 35.2L330.3 35.2L331.0 35.3L331.7 35.3L332.4 35.4L333.2 35.5L333.9 35.5L334.6 35.6L335.3 35.7L336.0 35.8L336.8 35.9L337.5 36.0L338.2 36.1L338.9 36.2L339.6 36.3L340.3 36.4L341.1 36.5L341.8 36.6L342.5 36.8L343.2 36.9L343.9 37.0L344.6 37.2L345.3 37.3L346.1 37.5L346.8 37.6L347.5 37.8L348.2 38.0L348.9 38.2L349.7 38.3L350.4 38.5L351.1 38.7L351.8 38.9L352.5 39.1L353.2 39.3L353.9 39.5L354.7 39.7L355.4 39.9L356.1 40.1L356.8 40.4L357.5 40.6L358.2 40.8L359.0 41.1L359.7 41.3L360.4 41.6L361.1 41.8L361.8 42.1L362.6 42.3L363.3 42.6L364.0 42.8L364.7 43.1L365.4 43.4L366.1 43.7L366.8 44.0L367.6 44.2L368.3 44.5L369.0 44.8L369.7 45.1L370.4 45.4L371.1 45.7L371.9 46.0L372.6 46.4L373.3 46.7L374.0 47.0L374.7 47.3L375.4 47.7L376.2 48.0L376.9 48.3L377.6 48.7L378.3 49.0L379.0 49.3L379.8 49.7L380.5 50.0L381.2 50.4L381.9 50.8L382.6 51.1L383.3 51.5L384.1 51.9L384.8 52.2L385.5 52.6L386.2 53.0L386.9 53.4L387.6 53.7L388.4 54.1L389.1 54.5L389.8 54.9L390.5 55.3L391.2 55.7L391.9 56.1L392.6 56.5L393.4 56.9L394.1 57.3L394.8 57.7L395.5 58.1L396.2 58.5L396.9 58.9L397.7 59.3L398.4 59.8L399.1 60.2L399.8 60.6L400.5 61.0L401.2 61.5L402.0 61.9L402.7 62.3L403.4 62.7L404.1 63.2L404.8 63.6L405.6 64.0L406.3 64.5L407.0 64.9L407.7 65.3L408.4 65.8L409.1 66.2L409.9 66.7L410.6 67.1L411.3 67.6L412.0 68.0L412.7 68.4L413.4 68.9L414.2 69.3L414.9 69.8L415.6 70.2L416.3 70.7L417.0 71.1L417.7 71.6L418.4 72.0L419.2 72.5L419.9 72.9L420.6 73.4L421.3 73.8L422.0 74.3L422.8 74.7L423.5 75.2L424.2 75.7L424.9 76.1L425.6 76.6L426.3 77.0L427.1 77.5L427.8 77.9L428.5 78.4L429.2 78.8L429.9 79.3L430.6 79.7L431.4 80.2L432.1 80.6L432.8 81.1L433.5 81.5L434.2 82.0L434.9 82.4L435.7 82.8L436.4 83.3L437.1 83.7L437.8 84.2L438.5 84.6L439.2 85.0L439.9 85.5L440.7 85.9L441.4 86.4L442.1 86.8L442.8 87.2L443.5 87.6L444.3 88.1L445.0 88.5L445.7 88.9L446.4 89.4L447.1 89.8L447.8 90.2L448.6 90.6L449.3 91.0L450.0 91.4L450.7 91.8L451.4 92.3L452.1 92.7L452.9 93.1L453.6 93.5L454.3 93.9L455.0 94.3" fill="none" stroke="currentColor" stroke-width="2"/>
  <g fill="currentColor"><circle cx="25.0" cy="75.0" r="3"/><circle cx="84.7" cy="107.4" r="3"/><circle cx="144.4" cy="113.0" r="3"/><circle cx="204.2" cy="87.4" r="3"/><circle cx="263.9" cy="51.5" r="3"/><circle cx="323.6" cy="35.0" r="3"/><circle cx="383.3" cy="51.5" r="3"/><circle cx="443.1" cy="87.4" r="3"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="25" y="20" opacity="0.7">얇은 선: 실제 170 Hz 진동 &#183; 점: 200 Hz로 찍은 샘플 8개</text>
    <text x="25" y="142">굵은 선: 30 Hz 유령 &#8212; 모든 샘플을 지나가므로 데이터만으로는 둘을 구분할 수 없다</text>
  </g>
</svg>


- 따라서: **다운샘플링 전 안티에일리어스 필터**, 항상 (소프트웨어에서 IMU 로그를 솎아낼
  때도 포함). 안티에일리어스 필터는 샘플러나 데시메이터 앞에 두는 저역통과 필터(§4)로,
  *새* $f_s/2$ 위의 성분을 없애 접혀 내려올 것을 남기지 않는다.
- 공학적 따름정리: *관측해야 할* 가장 빠른 동역학에서 여유를 두고 센서 주기를 정하라 —
  10 Hz 인식 루프는 50 Hz 진동을 감쇠는커녕 보지도 못한다.
- **양자화**는 각 샘플을 $2^N$개 준위 중 하나로 반올림한다. $N$은 ADC(아날로그-디지털
  변환기)의 비트 수다. 입력 범위가 $R$이면 한 칸은 $\Delta = R/2^N$이고, 반올림 오차는
  $[-\Delta/2, \Delta/2]$ 위의 균일 잡음처럼 행동하며 그 분산은 $\Delta^2/12$다. 그래서
  유한 비트는 거의 균일한 노이즈를 더한다 — 대략 **비트당 6 dB의 SNR**. *SNR*은
  신호 대 잡음비(신호 전력 ÷ 잡음 전력)이고, *dB*(데시벨)는 그것을 표기하는 로그 척도로
  +6 dB가 진폭 약 2배다. 즉 ADC의 비트 하나가 늘 때마다 양자화 잡음의 RMS가 절반, 전력은 4분의 1이 되고, 그 4배가 6 dB다.
  최대 진폭 사인파에 대한 표준 공식은
  $$\text{SNR}_{dB} = 10\log_{10}\frac{P_{signal}}{P_{noise}} \approx 6.02\,N + 1.76$$
  이다. $P_{signal}$과 $P_{noise}$는 두 전력, $6.02 = 10\log_{10}4$는 비트당 이득이고,
  $1.76$ dB는 사인파 전력과 잡음 $\Delta^2/12$의 비에서 나온다. 12비트 ADC는 약 $74$ dB,
  16비트는 약 $98$ dB다. 10 V를 덮는 12비트 변환기의 한 칸은 $2.44$ mV, 양자화 잡음 RMS는
  $0.70$ mV다. 디지털화의 나머지 절반이 이것이다. 양자화된 센서의 오차가 정말 백색인 조건과, 대신 고정된 바이어스가 되는 경우(정지한 엔코더)는 [[04-robotics/sensor-models|3.2 센서 모델과 잡음 §4]]에 있다.
- 이 계약이 안정성 문제로 바뀌는 자리: 가상 벽을 렌더링하는 햅틱 루프는 사람 손을 상대로
  매 밀리초 닫혀야 하고, 거기서 샘플링과 양자화는 정확도 문제이기를 그치고 장치가 떨지
  말지를 정하는 요인이 된다
  ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]).

### 3. 주파수 영역 — 대각화하는 기저

- 푸리에의 주장: 신호 = 사인파들의 합. 더 깊은 주장: **복소 지수함수는 LTI 시스템의
  고유함수다** ([[02-foundations/linear-algebra|고유값적 사고]]) — 안정한 LTI 시스템에서 복소 지수함수는
  $H(f)$배 되어 나오므로, 실수 사인파는 같은 주파수로 $|H(f)|$배 커지고 $\angle H(f)$만큼 위상이 밀려 나온다. 주파수 분석이 필터링을 대각화하는 이유가 이것이다.
- **주파수 응답.** 임펄스 응답이 $h$인 LTI 시스템에 대해, 주파수의 복소값 함수
  $$H(f) = \sum_n h[n]\, e^{-j2\pi f n}$$
  이다. $f$는 샘플당 사이클 단위($f = f_{Hz}/f_s$), 크기 $|H(f)|$는 그 주파수의 이득, 각도
  $\angle H(f)$는 위상 이동이다. 위 주장의 고유값이 정확히 이것이다. $x[n] = e^{j2\pi fn}$을
  §1의 합성곱에 넣으면 $y[n] = \sum_k h[k]\,e^{j2\pi f(n-k)} = H(f)\,e^{j2\pi fn}$이 되기
  때문이다. 연속 합 $h = [1, 1]$이라면 $H(0) = 2$(상수가 두 배가 됨), $H(1/4) = 1 - j$이므로
  이득 $\sqrt2 \approx 1.414$에 위상 $-45°$, 그리고 $H(1/2) = 0$(교대 입력 $+1, -1, +1, \ldots$이
  상쇄됨)이다.
- **DFT**(이산 푸리에 변환)는 샘플 $N$개 $x[0], \ldots, x[N-1]$의 블록을 복소 계수 $N$개로
  보낸다.
  $$X[k] = \sum_{n=0}^{N-1} x[n]\, e^{-j2\pi kn/N}$$
  빈 번호 $k = 0, \ldots, N-1$은 주파수 $k f_s/N$ Hz를 뜻하고($N/2$ 위의 빈은 음의 주파수),
  $|X[k]|$는 그 주파수가 얼마나 들었는지, $\angle X[k]$는 그 위상이다. 역변환
  $x[n] = \frac1N \sum_{k} X[k]\,e^{j2\pi kn/N}$이 있으므로 정보가 사라지지 않는다. 빈 간격
  $f_s/N$이 주파수 분해능이다. 200 Hz로 찍은 1000 샘플은 $0.2$ Hz를 가른다. 각 $X[k]$는
  신호와 기저 주파수 하나의 상관이다(그 합이 *왜* 투영인지는 [[02-foundations/engineering-math|0.5 §7]]에서 푼다).
  **FFT**(고속 푸리에 변환)는 다른 변환이 아니라 $N$개 계수 전부를 $O(N^2)$ 대신
  $O(N\log N)$에 계산하는 알고리즘이다.
- **$N = 4$ DFT, 손으로.** $x = [1, 0, -1, 0]$을 보자 — 4샘플 창에서 정확히 한 주기를 도는
  신호다. 회전 인자는 $e^{-j2\pi kn/4} = (-j)^{kn}$이므로:
  $$X[0] = 1 + 0 - 1 + 0 = 0, \qquad X[1] = 1(1) + 0(-j) + (-1)(-1) + 0(j) = 2$$
  $$X[2] = 0, \qquad X[3] = 2$$
  읽어보면: $X[0] = 0$은 이 신호에 **DC가 없다**는 뜻이고, 실제로 평균이 0이다. 에너지 전부가
  $k = 1$과 그 거울상 $k = 3$(같은 주파수를 음수 쪽에서 본 것 — 실수 신호의 크기 스펙트럼은 항상 이렇게
  대칭이라, 단측 FFT 플롯은 앞쪽 절반만 보여준다)에 앉는다. 켜진 주파수는 하나이고, 빈 1의 회전이
  창 전체에서 정확히 한 바퀴를 돈다. DFT의 전부가 이것이다.
- **합성곱 정리**: 시간 영역의 합성곱은 주파수 영역의 곱이다.
  $$y = x * h \quad\Longleftrightarrow\quad Y(f) = X(f)\,H(f)$$
  $X(f) = \sum_n x[n]e^{-j2\pi fn}$와 $Y(f)$는 입력과 출력의 변환으로, 위의 $H(f)$와 같은
  방식으로 만든다. $x$ 안의 복소 지수함수 하나하나가 $H(f)$배 될 뿐이기 때문에 성립한다.
  §1의 예제로 $f = 1/4$에서 검산하면($e^{-j2\pi n/4} = (-j)^n$):
  $X = 1 + 2(-j) + 3(-1) = -2 - 2j$, $H = 1 - j$이므로 $XH = -4$이고, 직접 계산한
  $Y = 1 + 3(-j) + 5(-1) + 3(j) = -4$ ✓. 그래서 필터링은 주파수 영역의 곱;
  신경망의 스펙트럼 편향(저주파부터 맞추므로 날것의 좌표를 입력받은 망은 과하게 매끄러운 함수를
  배운다 — [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]가 입력을 푸리에 특징으로
  들어올리는 이유)을 이해하는 렌즈이기도 하다.
- 신호의 지문: 백색 잡음 = 평평한 스펙트럼(서로 무상관인 샘플;
  [[02-foundations/probability|3. 확률 §5]]에 정의); 드리프트/바이어스 = **DC** 근처 스파이크
  ("DC"는 직류에서 온 말이고 여기서는 그냥 주파수 0 — 신호의 상수 성분을 뜻한다);
  회전 기계 = 고조파의 날카로운 피크 (굴착기 엔진 대역은 노치 필터의 표적).

비슷해 보이는 변동도 대응이 달라 주파수 분석이 유용하다. 좁은 기계 진동 피크와 넓은 접촉 과도응답은 시간상 겹쳐도 스펙트럼 모양이 다를 수 있다. 피크 제거는 도움이 되지만 무차별 평활은 접촉 신호를 지울 수 있다. **여기서 얻는 독법.** 피크를 운용 조건과 연결하고 윈도·샘플링 정보를 보존한다. 유한 구간 스펙트럼의 피크는 조사할 증거이지 물리 원인의 자동 식별은 아니다.

### 4. 필터링 — 설계 기초

- **FIR**(유한 임펄스 응답) 필터: 출력이 현재 입력과 직전 $M-1$개 입력의 고정된 가중합이고,
  그 밖의 것은 쓰지 않는다.
  $$y[n] = \sum_{k=0}^{M-1} b_k\, x[n-k]$$
  $b_k$는 계수, $M$은 필터 길이다. $\delta[n]$을 넣으면 출력이 계수 목록 그 자체
  $h[k] = b_k$이고 $M$ 샘플 뒤에 끝난다. 그것이 "유한"이다. 결과가 둘 따른다.
  $\sum_n |h[n]| = \sum_k |b_k|$가 유한합이므로 항상 BIBO 안정하다(§1). 그리고 계수가
  대칭 $b_k = b_{M-1-k}$이면 정확한 선형 위상을 가져 모든 주파수를 똑같이 $(M-1)/2$ 샘플
  늦추므로 파형이 왜곡되지 않는다. 5탭 이동 평균은 모든 것을 2 샘플, 100 Hz라면 20 ms 늦춘다.
  대신 **탭**(tap)이 많이 필요하다 — 탭 하나 = $b_k$ 하나, 즉 필터가
  아직 들고 있으면서 곱해야 하는 과거 샘플 하나다. 따라서 "탭이 많다"는 메모리·연산량·
  지연이 모두 늘어난다는 뜻이다. 이동 평균이 가장 단순한 FIR이다. 순음 $e^{j2\pi fn}$($f$: cycles/sample)을
  넣으면 출력은 그 순음에 $H(f) = \tfrac1M\sum_{k=0}^{M-1} e^{-j2\pi fk}$를 곱한 것이고, 이 등비급수의 합은
  $\tfrac1M(1-e^{-j2\pi fM})/(1-e^{-j2\pi f})$다. 분자에서 $e^{-j\pi fM}$, 분모에서 $e^{-j\pi f}$를 묶어 내면
  사인 두 개가 남아 $|H(f)| = |\sin(\pi f M)/(M\sin \pi f)|$가 된다. 이 응답이 트레이드오프를 보여준다: 창이 길수록 통과
  대역이 좁아지고 *그리고* 지연이 커진다.
- **IIR**(무한 임펄스 응답) 필터: 과거 *출력*도 되먹인다.
  $$y[n] = \sum_{k=0}^{M} b_k\, x[n-k] - \sum_{k=1}^{N} a_k\, y[n-k]$$
  $b_k$는 FIR처럼 입력에 가중치를 주고, $a_k$는 직전 출력 $N$개에 가중치를 준다. 모든
  출력이 뒤의 출력으로 다시 들어가므로 임펄스 하나가 영원히 메아리치고, 그래서 $h$가 끝나지
  않는다. 가장 단순한 예가 지수 평활기 $y[n] = \alpha y[n-1] + (1-\alpha)x[n]$
  ($b_0 = 1-\alpha$, $a_1 = -\alpha$)이고, 임펄스 응답은 $n \ge 0$에서
  $h[n] = (1-\alpha)\alpha^n$이다. $\alpha = 0.9$면 $0.1, 0.09, 0.081, 0.0729, \ldots$로
  정확히 0이 되는 일이 없다. 안정성도 더는 저절로 보장되지 않는다. $0 < \alpha < 1$이면
  $\sum_n |h[n]|$이 $1$이지만 $\alpha = 1.1$이면 항이 커진다. IIR은 싸고 위상이 비선형. 고차 IIR 설계는 날카로울 수 있지만 링잉·불안정이 가능하다. 이 가장 단순한 IIR은 $z=\alpha$에 실수 극점 하나뿐이라($z$는 §5의 Z-변환 변수이고, 이 극점은 §5에서 유도한다) $0<\alpha<1$이면 항상 안정하고, 링잉이 없으며, 완만하게 감쇠한다.
- **그 식의 $\alpha$는 양이 아니라 규약이다.** 위처럼 쓰면 큰 $\alpha$가 *직전 출력*을
  더 믿어 더 많이 거른다. 많은 논문과 강의안은 반대로 $y[n] = \alpha x[n] + (1-\alpha)y[n-1]$로
  써서, 큰 $\alpha$가 *새 측정*을 더 믿어 덜 거른다. 둘은 $\alpha$를 $1-\alpha$로 바꾼 같은
  필터이므로 기호만으로는 아무것도 알 수 없다. 숫자를 읽기 전에 식을 읽어라.
- **평활기를 한 스텝씩 따라가 보면.** $y[n] = 0.9\,y[n-1] + 0.1\,x[n]$을 계단 입력에 돌려
  보자 — 입력이 $0$에서 $1$로 뛰어 그대로 유지된다. $y = 0$에서 시작하면 출력은
  $0.1,\ 0.19,\ 0.271,\ 0.344,\ 0.410,\ \ldots$으로 가고, 새 값의 90%에 닿는 데 약
  **22 샘플**이 걸린다($0.9^{22} \approx 0.1$이므로). 100 Hz라면 계단 변화의 90%를 따라가는 데
  약 $0.22$초가 필요하다. 이것은 순수한 $0.22$초 dead time이 아니라 주파수에 따라 달라지는
  위상·군지연이다. $\alpha = 0.5$로 두면 90%를 처음 넘는 이산 샘플은 4번째다. 독립 백색 입력
  잡음에 대해 이 계수 정의의 *분산* 이득은 $(1-\alpha)/(1+\alpha)$다 — 정상 상태에서 $y[n-1]$과 새 잡음 표본이 독립이므로 출력
  분산이 $\sigma_y^2 = \alpha^2\sigma_y^2 + (1-\alpha)^2\sigma_x^2$를 만족해야 하고, $(1-\alpha)^2/(1-\alpha^2)$를
  정리하면 그 비가 된다. 그래서 0.053 대 0.333 —
  분산으로 6.3배, 표준편차로 2.5배 차이다.
  이 거래 — 느린 응답과 위상 지연을 치르고 사는 잡음 제거 — 는 필터 설계의 핵심이고, 제어 엔지니어가
  언제나 "그 필터가 위상에서 얼마를 앗아갔나"를 묻는 이유다
  ([[04-robotics/control-theory-ce397|제어 이론 §7]]).
- **필터 종류는 통과시키는 주파수로 이름 붙는다.** 차단 주파수가 $f_c$일 때 이상적인
  **저역통과** 필터는 $|f| < f_c$에서 $|H(f)| = 1$, 그 위에서 $|H(f)| = 0$이다.
  **고역통과** 필터는 그 반대, **대역통과** 필터는 한 대역만 남기고, **노치** 필터는 주파수
  $f_0$ 주변의 좁은 대역 하나를 없앤다. 실제 필터는 날카로운 경계 대신 전이 대역을 가진다.
  선택: 센서 노이즈엔 저역통과, 드리프트 제거엔 고역통과, 알려진 진동 고조파엔 노치,
  IMU 융합엔 상보 필터(가속도 저역 + 자이로 고역).
- **상보 필터**: 같은 양을 재지만 *서로 다른* 주파수 대역에서 믿을 만한 두 센서를 합치는 융합
  필터다. 한 센서는 저역통과 $H_L$을, 다른 센서는 고역통과 $H_H$를 거치고, 두 응답의 합이
  정확히 1이 되도록 짝을 고른다.
  $$H_L(f) + H_H(f) = 1$$
  그래서 두 센서가 함께 보는 참 신호는 이득 1로 왜곡 없이 지나가고, 각 센서의 나쁜 대역은
  억제된다. IMU 기울기에서 가속도계 각도 $\theta_{acc}$는 평균적으로 맞지만 잡음이 많고,
  자이로 각속도 $\omega$는 적분하면 매끄럽지만 드리프트한다. 그래서 한 줄 갱신식이 나온다.
  $$\hat\theta[n] = \alpha\big(\hat\theta[n-1] + \omega[n]\,\Delta t\big) + (1-\alpha)\,\theta_{acc}[n]$$
  $\hat\theta$는 융합 추정값, $\Delta t$는 샘플 주기, $\alpha$는 교차 지점을 정한다.
  $\alpha = 0.98$, $\Delta t = 0.01$ s, 이전 추정 $10°$, 자이로 $5°/\text{s}$, 가속도계
  $11°$이면 새 추정은 $0.98 \times 10.05 + 0.02 \times 11 = 10.069°$다. 교차 시상수는
  $\tau = \alpha\Delta t/(1-\alpha) = 0.49$ s다. 그보다 느린 변화는 가속도계를, 빠른 변화는
  자이로를 따른다.
- **위상 지연은 인과적 평활화의 대가다**: 구현 가능한 인과적 평활화는 일반적으로 통과대역에
  주파수 의존 위상·군지연을 만든다 — 과한
  필터링은 *제어기와 싸운다*(지연된 속도 추정이 D항을 불안정하게 만든다). 모델 기반
  추정을 선호하는 실전적 이유가 이것이다: 정확한 선형-가우시안 상태공간 모델과 잡음
  공분산 아래에서는 **칼만 필터**([[02-foundations/probability|3. 확률 §5에서 유도]])가 평균제곱
  추정 오차를 최소화한다. 모델이 어긋나면 이 보장은 사라진다.
- **위상 지연과 군지연**은 필터 출력이 얼마나 늦는지를 말한다. 위상 응답은 $\angle H(f)$다(§3).
  **군지연**은 그 기울기에 음수를 붙인 것으로, 샘플 단위로 잰다.
  $$\tau_g(f) = -\frac{1}{2\pi}\,\frac{d\,\angle H(f)}{df}$$
  그래서 위상이 주파수에 따라 선형으로 떨어지는 필터는 모든 주파수를 같은 샘플 수만큼 늦추고
  파형 모양을 지킨다. 대칭 5탭 이동 평균은 통과대역에서 $\angle H(f) = -4\pi f$이므로 어디서나
  $\tau_g = 2$ 샘플이다. 지수 평활기는 선형 위상이 아니다. $\alpha = 0.9$, $f = 0.05$
  cycles/sample에서 이득은 $0.32$, 위상은 $-62.6°$이고, 지연이 주파수마다 달라진다.

### 5. 제어로 가는 다리: 변환

- 라플라스 변환(연속, [[02-foundations/engineering-math|0.5 §9]]에 정의) / **Z-변환**(이산)은 푸리에의 일반화: 합성곱 ↦ *전달함수*
  $H(s)$ 또는 $H(z)$와의 곱.
- **Z-변환**은 수열을 복소 변수 $z$의 함수로 바꾼다.
  $$X(z) = \sum_n x[n]\, z^{-n}$$
  그래서 한 샘플 지연이 $z^{-1}$ 곱하기가 된다. 라플라스 변수와는 $z = e^{sT_s}$로 묶이고,
  단위원 $z = e^{j2\pi f}$ 위에서는 §3의 주파수 응답으로 줄어든다. **전달함수**는 시스템이
  정지 상태에서 출발할 때 출력 변환과 입력 변환의 비다.
  $$H(z) = \frac{Y(z)}{X(z)}$$
  합성곱이 곱이 되었으므로 이것은 $h$의 변환이다. 계산: 지수 평활기를 항마다 변환하면
  $Y(z) = \alpha z^{-1} Y(z) + (1-\alpha) X(z)$이므로 $H(z) = (1-\alpha)/(1-\alpha z^{-1})$이다.
  **극점**(분모를 0으로 만드는 $z$. 극점과 영점의 정의는 [[02-foundations/engineering-math|0.5 §9]])은 $z = \alpha$다.
  DC($z = 1$)에서 이득은 정확히 $1$이라 상수는 그대로 지나가고, 나이퀴스트 주파수($z = -1$)에서는
  $(1-\alpha)/(1+\alpha)$, 즉 $\alpha = 0.9$일 때 $0.053$이다.
- 최소 실현([[02-foundations/engineering-math|0.5 §9]])에서 $H$의 극점 = 상태공간 $A$의 고유값
  ([[02-foundations/linear-algebra|1. 선형대수 §5]]): 인과 시스템의 안정성 = 극점이 좌반평면(연속) /
  단위원 안, $|z| < 1$(이산). §1의 BIBO 판정을 다르게 쓴 것이다. $z = \alpha$의 극점은
  $h[n]$에 $\alpha^n$ 항을 보태고, 그 항은 $|\alpha| < 1$일 때만 합산 가능하기 때문이다. 필터, 플랜트, 제어기가 전부 이 하나의 언어를 쓴다 — 제어이론 교재와
  이 페이지가 같은 대상의 두 시점인 이유다.

변환은 주파수별 변화와 내부 동역학의 성장·감쇠를 드러낸다. 평활 필터는 진동을 줄이면서 접촉 제어 피드백에 지연을 추가할 수 있다. **여기서 얻는 독법.** 필터 신호가 더 좋다고 하기 전에 이득과 위상을 함께 본다. 상태 공간 모드와 전달함수 극점도 구분한다. 관측·제어할 수 없는 모드(출력에 전혀 드러나지 않는 모드, 또는 입력이 전혀 들뜨게 하지 못하는 모드; 계수 판정과 함께 [[02-foundations/linear-algebra|1. 선형대수 §5]]에서 정의)는 상쇄로 사라질 수 있어 극점과 고유값의 동일성에는 최소 실현 조건이 필요하다.

### 6. 센서 파이프라인 습관 (현장 검증됨)

- **원시** 데이터로 기록하고 필터링은 나중에; 암묵적 이중 필터링(드라이버 + 내 코드) 금지.
- 센서에서 타임스탬프를 찍고, 융합 전에 시계를 동기화(카메라-LiDAR-IMU의 외부 파라미터
  *그리고* 시간 오프셋).
- 필터를 고르기 전에 스펙트럼부터 봐라: 싸울 노이즈의 이름부터 알아내라.

> [!tip] 더 깊이 · Going deeper
> 이 페이지가 압축한 표준 강의는 Oppenheim·Schafer의 *Discrete-Time Signal Processing*이다. §2가 샘플링 정리를 네 단계로 증명한다. 그 책의 샘플링·DFT 장은 그 증명이 생략한 수렴의 세부와 실제 복원 필터를 더한다.

드라이버가 힘 측정을 이미 평활한 뒤 제어기에서 다시 필터링할 수 있다. 신호는 깨끗해도 접촉 시작이 늦게 도착한다. 원신호와 두 처리 단계를 남겨야 지연을 진단할 수 있다. **여기서 얻는 독법.** 취득에서 결정까지 시계 변환과 모든 처리를 따라간다. 처리 이력이 없는 그림으로는 부드러움이 더 좋은 센싱에서 왔는지 중요한 과도응답을 없애서 생겼는지 알 수 없다.

### 스스로 점검

1. $x = [1, 0, -1]$과 $h = [1, 2, 1]$을 손으로 합성곱하고 출력 길이를 말하라.
2. IMU가 200 Hz로 샘플링하는데 모터가 170 Hz로 진동한다. 진동은 데이터의 어디에
   나타나고, 무엇을 했어야 하는가?
3. 2점 이동 평균의 주파수 응답을 유도하고, 완전히 소거되는 주파수를 찾아라.
4. 운동/잡음 모델이 대략 맞을 때, 제어 루프의 속도 추정에서 칼만 필터가 손튜닝
   저역통과를 이기는 경향이 있는 이유는? 반대로 저역통과가 이기는 경우는?
   (두 가지: 하나는 지연, 하나는 모델에 관한 것.)

> [!tip]- 스스로 점검 정답 · Answers
> 1. $y = [1, 2, 0, -2, -1]$, 길이 $3+3-1 = 5$.
> 2. $|170 - 200| = 30$ Hz로 위장해 나타난다. 샘플링 전에 아날로그 안티에일리어스 필터(차단 <100 Hz)를 넣거나 $f_s > 340$ Hz로 올렸어야 한다.
> 3. $H(f) = \tfrac12(1 + e^{-j2\pi f})$이므로 $|H(f)| = |\cos(\pi f)|$다($f$: cycles/sample). 나이퀴스트 주파수 $f = 1/2$에서 완전히 소거되는데, 연속한 두 표본이 부호를 번갈아 평균이 0이 되기 때문이다.
> 4. 지연: 칼만의 *예측* 단계가 보정 전에 상태를 앞으로 보내므로, 인과적 저역통과가 무는 위상 지연을 전부 물지는 않는다. 없애는 것이 아니라 덜 무는 것이다. 모델: 프로세스/측정 노이즈 비를 명시적으로 써서 시변 최적 이득을 계산한다 — 손튜닝 저역통과에는 둘 다 없다. 반대로 저역통과가 이기는 경우는 운동 모델이 틀렸거나 아예 없을 때, 잡음이 가정한 통계에서 멀 때, 또는 모델링과 튜닝에 들일 여력이 없을 때다. 틀린 모델은 칼만 필터를 확신에 차서 틀리게 만든다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P3**. 이 페이지 §2. 햅틱 루프는 $1\,\mathrm{kHz}$ ($T=10^{-3}\,\mathrm{s}$). 시뮬레이터 없음.

1. **그리기.** 위의 그림을 손으로 다시 그린다. 연속 핸들 위치 $x(t)$가 주기 $T$의 이상 샘플러, 이어서 영차 홀드(다음 틱까지 값을 유지). 벽 $x_w$를 표시.
2. **유도.** $1\,\mathrm{kHz}$에서의 나이퀴스트 주파수, 정리가 허용하는 최대 대역 $B$. 손/벽 접촉이 $30\,\mathrm{Hz}$ 아래라면, 샘플링만으로 $1\,\mathrm{kHz}$는 충분한가?
3. **해석.** 모터 엔코더 한 카운트 $\Delta x=r_m\,2\pi/N$을 계산하라. 샘플 간격인가 양자화 스텝인가? $N$을 키우는 것과 $f_s$를 키우는 것은 무엇이 다른가?

> [!note]- 그리는 법 · How to draw it
> - 신호 경로를 한 줄의 블록으로: $x(t)$를 내는 핸들, $T=10^{-3}\,\mathrm{s}$마다 순간적으로 닫히는 스위치로 그린 이상 샘플러(아래에 $f_s=1000\,\mathrm{Hz}$와 나이퀴스트 $500\,\mathrm{Hz}$), 수열 $x[n]=x(nT)$, 출력이 계단인 상자로 그린 영차 홀드, 그리고 벽 법칙이 실제로 보는 유지된 신호.
> - 홀드 아래에는 그 블록이 하는 일 하나: $x[n]$을 $[nT,\ (n+1)T)$ 동안 일정하게 유지하고 그다음 튄다.
> - 그 아래 시간축 하나, 눈금 여덟 개가 들어가도록 약 $8\,\mathrm{ms}$. $x(t)$는 벽을 가로지르며 올라가는 매끄러운 곡선이고, 눈금마다 그 위에 점을 찍는다. 그 점들이 $x[n]$이고, 제어기에게 그 사이는 존재하지 않는다.
> - 같은 축 위의 ZOH 계단, 각 디딤판은 *직전* 점의 높이에서 평평하다. 디딤판 하나에서 곡선과 계단 사이의 조각을 칠하고 이름을 붙인다. 홀드는 평균 $T/2=0.5\,\mathrm{ms}$ 늦고, §2가 그것을 위상 지연으로 바꾼다.
> - 벽($x_w=0.030\,\mathrm{m}$)은 세 곡선을 모두 가로지르는 수평 점선으로, 그보다 높은 첫 디딤판에는 동그라미. 제어기의 접촉은 언제나 눈금에서 시작하지 참된 교차점에서 시작하지 않는다.
> - 3번을 위해 엔코더 한 카운트($\Delta x=r_m\,2\pi/N=0.010\cdot2\pi/1024=61.4\,\mu\mathrm{m}$) 간격으로 흐린 수평 격자선을 긋고 점들을 가장 가까운 선에 스냅해 다시 찍는다. 두 스텝은 혼동할 수 없도록 이름을 붙인다. 시간을 따라 시계가 정하는 $T$, 공간을 따라 엔코더가 정하는 $\Delta x$.
> - 격자 옆에는 이 벽에서 한 카운트가 힘으로 얼마인지, $k_w\,\Delta x=400\times61.4\,\mu\mathrm{m}=0.025\,\mathrm{N}$. 맨 아래에는 눈금마다 새 카운트 하나가 생기는 속도 $\Delta x/T=61.4\,\mathrm{mm/s}$. 그보다 느리면 어떤 눈금은 움직임을 보고하지 않으므로 위치를 차분한 속도가 0이었다가 튄다. 한 주기에 $33.3$ 샘플이 들어가는 $30\,\mathrm{Hz}$ 접촉에서도 생기는, §4의 필터링이 다루는 양자화 잡음이다.

> [!tip]- 정답 · Solutions
> 1. 샘플러 $x[n]=x(nT)$. ZOH는 $[nT,(n+1)T)$에서 높이 $x[n]$인 계단. 벽 $x_w=0.030\,\mathrm{m}$.
> 2. $f_s=1000\,\mathrm{Hz}$, 나이퀴스트 $500\,\mathrm{Hz}$, 따라서 $B<500\,\mathrm{Hz}$. $30\,\mathrm{Hz}$는 한참 아래라 샘플링이 병목이 아니다.
> 3. $\Delta x=0.010\cdot 2\pi/1024=6.14\times 10^{-5}\,\mathrm{m}$ ($61.4\,\mu\mathrm{m}$). 위치의 양자화이지 $T_s$가 아니다. $N$을 키우면 공간 계단이 줄고, $f_s$를 키우면 시간 계단이 준다.

### 로보틱스 다리

샘플링·필터링·지연은 [[04-robotics/robot-systems-deployment|10. 로봇 시스템]]의 타이밍 예산과 [[04-robotics/state-estimation-slam|3. 상태 추정]]의 센서 융합으로 이어진다.
