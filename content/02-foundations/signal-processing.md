---
title: 6. Signal Processing
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled; P3 is the catalog's one-axis haptic handle) · [[02-foundations/engineering-math|0.5 §7]] (complex numbers, Euler's formula) · [[02-foundations/engineering-math|0.5 §9]] (Laplace, poles) · [[02-foundations/linear-algebra|1. Linear Algebra §3, §5]] (eigenvectors, for §3's diagonalizing basis; controllability and observability, for §5) · [[02-foundations/probability|3. Probability §5]] (white noise, stationarity) · background, if dynamics or electronics is new: [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §4–§5]] (viscous damping, for §2's hold) and [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics §5, §10]] (the RC low-pass and the ADC, for §2's anti-alias filter and quantization)
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3**(카탈로그의 1축 햅틱 핸들) · [[02-foundations/engineering-math|0.5 §7]](복소수·오일러 공식) · [[02-foundations/engineering-math|0.5 §9]](라플라스·극점) · [[02-foundations/linear-algebra|1. 선형대수 §3, §5]](고유벡터, §3의 대각화 기저용; 가제어성과 가관측성, §5용) · [[02-foundations/probability|3. 확률 §5]](백색 잡음·정상성) · 동역학이나 전자가 처음이라면 배경으로: [[02-foundations/basic-mechanics|0.6.1 기초 역학 §4–§5]](점성 감쇠, §2의 홀드용)와 [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자 §5, §10]](RC 저역통과와 ADC, §2의 안티에일리어스 필터와 양자화용)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/probability|3. Probability]] and Euler's formula from [[02-foundations/engineering-math|0.5]]. A domain bridge: from here the data stops being given
and starts arriving from a sensor. Its order against [[02-foundations/rl-basics|7. RL Basics]] is free.*

Every sensor a construction robot carries — camera, LiDAR (a scanning laser rangefinder), IMU (an inertial measurement unit: accelerometers and gyroscopes), encoder (a counter of shaft rotation) — hands you a
sampled, noisy signal. Course-depth treatment: convolution worked by hand, the sampling
theorem with its math, DFT/FFT, filter design basics, and the bridge to control's transfer
functions.

> [!note] Why this matters · 왜 배우는가
> Every camera, LiDAR, IMU and encoder hands a robot a sampled, noisy signal, so this page is the mathematical floor under two layers of the physical-AI stack in [[07-research-program/index|7. Research Program §5]]: perception, and contact, force and tactile feedback, where a filtered force signal decides that contact has begun. In *"Install that panel on the frame"* it sits under *identifies panel and frame* and *detects contact* (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it the data mislead quietly: sampled at $200\,\mathrm{Hz}$, a $170\,\mathrm{Hz}$ motor vibration shows up in an IMU log as a $30\,\mathrm{Hz}$ "mode" that no later software can remove, and two 5-tap smoothers in series make P3's wall notice contact $4\,\mathrm{ms}$ late. Later pages lean on it section by section — [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] on §2's sampling and quantization, [[04-robotics/control-theory-ce397|5. Control Theory]] on §1's LTI systems and §4's filter lag, [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]] on §2's hold and §5's z-transform, [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection]] on §1 and §3 — and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) it is tested by question 10 of block 1's [[02-foundations/overview#Gate check — are the foundations done?|foundations gate]], and block 2, the robotics common track, runs on it. After it you can choose a sampling rate, say where an alias will land, and price a filter's delay in milliseconds before it reaches a controller.

> [!note] First pass · 처음이라면
> About two and a half sessions of 60–90 minutes. Session 1: the Running object, the picture and §1, whose convolution figure you should redo by hand. Session 2: §2 with its proof left folded — sampling, aliasing, the zero-order hold and quantization are what actually bite. Session 3, a shorter one: §3's frequency-response bullet, which says what a filter's gain and phase are, then §4's FIR and group-delay bullets, which §6 prices, and §6's field habits. End with self-checks 1–2, problem 1 and question 10 of the [[02-foundations/overview#Gate check — are the foundations done?|gate check]]. The rest of §3, and §5, are the machinery: open them when a paper works in the frequency domain.

### Running object · 이 페이지의 대상

**P3** from [[02-foundations/lab-plants|0.6 Lab Plants]], the one-axis haptic handle, with the numbers this page uses: a virtual wall of stiffness $k_w = 400\,\mathrm{N/m}$ at $x_w = 0.030\,\mathrm{m}$ ($+x$ points into the wall), a motor pulley of radius $r_m = 0.010\,\mathrm{m}$, and an encoder of $N = 1024$ counts per revolution. Its servo loop runs at $1\,\mathrm{kHz}$, the period $T = 1\,\mathrm{ms}$ that [[02-foundations/lab-kernel|0.7 Lab Kernel §1]] sets for haptic walls. In the picture the handle oscillates at $30\,\mathrm{Hz}$ and crosses the wall at $t_c = 4.45\,\mathrm{ms}$:
$$x(t) = x_w + A\sin\big(2\pi \cdot 30\,\mathrm{Hz} \cdot (t - t_c)\big), \qquad A = 0.163\,\mathrm{mm}$$
so its speed peaks as it crosses the wall, because a sine is steepest where it crosses zero: $2\pi \cdot 30\,\mathrm{Hz} \cdot A = 30.7\,\mathrm{mm/s}$, exactly half the speed $\Delta x/T = 61.4\,\mathrm{mm/s}$ at which one new encoder count appears per tick. §2 and §6 also borrow **P6**, the catalog's one-dimensional cart ([[02-foundations/lab-plants|0.6]]), for its load cell's anti-alias filter and its clocks.

*Scope: this page teaches discrete-time signals and systems — convolution, sampling and quantization, the DFT, filter basics and the z-transform — on P3. It does not teach the circuits that build a filter or an ADC ([[02-foundations/basic-circuits-electronics|0.6.2]]), the Kalman filter ([[02-foundations/probability|3. Probability §5]]), or how delay decides a loop's stability ([[04-robotics/control-theory-ce397|5. Control Theory]] and [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]).*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 440" font-size="12" style="max-width:100%;height:auto" role="img" aria-label="plant P3 on its 1 kHz servo: handle, ideal sampler, zero-order hold and wall law in a row; below, the handle position, its eight samples and the hold's staircase against the wall, on a grid one encoder count tall">
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
  <text x="146.0" y="82.0" fill="currentColor" text-anchor="middle" opacity="0.9">closes every T = 1 ms</text>
  <text x="146.0" y="96.0" fill="currentColor" text-anchor="middle" opacity="0.9">f<tspan dy="3" font-size="10">s</tspan><tspan dx="3.3" dy="-3">= 1000 Hz</tspan></text>
  <text x="146.0" y="110.0" fill="currentColor" text-anchor="middle" opacity="0.9">Nyquist 500 Hz</text>
  <line x1="167" y1="50" x2="250" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSp)"/>
  <text x="208.0" y="43.0" fill="currentColor" text-anchor="middle">x[n] = x(nT)</text>
  <rect x="252" y="33" width="64" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="258,60 270,60 270,53 282,53 282,46 294,46 294,40 310,40" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="284.0" y="23.0" fill="currentColor" text-anchor="middle">zero-order hold</text>
  <text x="284.0" y="96.0" fill="currentColor" text-anchor="middle" opacity="0.9">holds x[n] on [nT, (n+1)T),</text>
  <text x="284.0" y="110.0" fill="currentColor" text-anchor="middle" opacity="0.9">then jumps</text>
  <line x1="316" y1="50" x2="410" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSp)"/>
  <text x="362.0" y="43.0" fill="currentColor" text-anchor="middle">held x</text>
  <rect x="412" y="33" width="136" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="480.0" y="47.0" fill="currentColor" text-anchor="middle">wall law</text>
  <text x="480.0" y="61.0" fill="currentColor" text-anchor="middle">F = −k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3">(x − x</tspan><tspan dy="3" font-size="10">w</tspan><tspan dy="-3">)</tspan></text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.18"><line x1="60" y1="306.0" x2="364" y2="306.0"/><line x1="60" y1="262.0" x2="364" y2="262.0"/><line x1="60" y1="218.0" x2="364" y2="218.0"/><line x1="60" y1="174.0" x2="364" y2="174.0"/><line x1="60" y1="130.0" x2="364" y2="130.0"/></g>
  <text x="0" y="0" transform="translate(48 229) rotate(-90)" fill="currentColor" text-anchor="middle" opacity="0.8">position x · one gridline = one count</text>
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
  <text x="374.0" y="338.0" fill="currentColor" opacity="0.8">t (ms)</text>
  <line x1="99.0" y1="370.0" x2="135.0" y2="370.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <line x1="135.0" y1="370.0" x2="99.0" y2="370.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <text x="142.0" y="374.0" fill="currentColor">T = 1 ms: the clock</text>
  <line x1="60" y1="221.3" x2="372" y2="221.3" stroke="currentColor" stroke-width="1.6" stroke-dasharray="7 4"/>
  <text x="378.0" y="225.3" fill="currentColor">x<tspan dy="3" font-size="10">w</tspan><tspan dx="3.3" dy="-3">= 0.030 m</tspan></text>
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
  <text x="185.4" y="281.8" fill="currentColor">on x[n], contact begins</text>
  <text x="185.4" y="295.8" fill="currentColor">at a tick (5 ms), not at the</text>
  <text x="185.4" y="309.8" fill="currentColor" opacity="0.85">true crossing (4.45 ms)</text>
  <line x1="372" y1="131.0" x2="372" y2="173.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <line x1="372" y1="173.0" x2="372" y2="131.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSp)"/>
  <text x="380.0" y="140.0" fill="currentColor" opacity="1">Δx = 61.4 μm:</text>
  <text x="380.0" y="154.0" fill="currentColor" opacity="0.9">one encoder count</text>
  <text x="380.0" y="172.0" fill="currentColor" opacity="1">k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3">·Δx = 400 × 61.4 μm</tspan></text>
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
  <text x="14.0" y="400.0" fill="currentColor" opacity="1">Where the grids meet: Δx/T = 61.4 mm/s gives one new count per tick.</text>
  <text x="14.0" y="414.0" fill="currentColor" opacity="0.95">This x(t) peaks at 30.7 mm/s as it crosses the wall, so every other tick reports no motion,</text>
  <text x="14.0" y="428.0" fill="currentColor" opacity="0.95">and a velocity from differenced counts reads 0, then 61.4 mm/s.</text>
</svg>

Plant **P3** on its $1\,\mathrm{kHz}$ servo, moving as the Running object's $x(t)$: the ideal sampler reads $x[n]=x(nT)$ every $T=1\,\mathrm{ms}$ (Nyquist $500\,\mathrm{Hz}$; §2), and the zero-order hold (§2) turns the samples into a staircase that runs $T/2=0.5\,\mathrm{ms}$ late on average, so a wall law acting on $x[n]$ first sees contact with the wall at $x_w=0.030\,\mathrm{m}$ at the $5\,\mathrm{ms}$ tick, not at the true crossing at $4.45\,\mathrm{ms}$. The faint grid is one encoder count, $\Delta x=61.4\,\mu\mathrm{m}$, worth $k_w\,\Delta x=0.025\,\mathrm{N}$ of wall force, and the diamonds are the samples snapped to the nearest count. The two grids meet at $\Delta x/T=61.4\,\mathrm{mm/s}$, one new count per tick, while this motion peaks at $30.7\,\mathrm{mm/s}$ as it crosses the wall, so every other tick brings no new count and a velocity from differenced counts reads $0$, then $61.4\,\mathrm{mm/s}$.

### 1. Signals, systems, and convolution

A short physical event can affect several later samples through the sensor and filter response, so the record of an event is never quite the event. This section gives the exact rule for that spreading, convolution, and shows that for a linear, time-invariant system it is the only rule there is.

- A **system** $\mathcal{S}$ is a rule that turns an input sequence $x[n]$ into an output sequence
  $y[n] = \mathcal{S}\{x\}[n]$, where $n$ is the integer sample index (the letter $\mathcal{S}$ keeps $T$ free for §2's sample period). A system is **LTI** (linear,
  time-invariant) when it has **two** properties, and each can fail without the other.
- **Linearity** is additivity *and* homogeneity together, i.e. superposition (the full
  definition, with non-examples, is [[02-foundations/engineering-math|0.5 §4.5]]). For all
  inputs $x_1, x_2$ and all scalars $a, b$:
  $$\mathcal{S}\{a x_1[n] + b x_2[n]\} = a\,\mathcal{S}\{x_1[n]\} + b\,\mathcal{S}\{x_2[n]\}$$
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
  **impulse response** is what the system does to it, $h[n] = \mathcal{S}\{\delta\}[n]$. For the
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
  $x[n] = \sum_k x[k]\,\delta[n-k]$. Push it through the system $\mathcal{S}$ and use *linearity* to
  move $\mathcal{S}$ inside the sum: $y[n] = \mathcal{S}\{\sum_k x[k]\delta[n-k]\} = \sum_k x[k]\,\mathcal{S}\{\delta[n-k]\}$.
  Now use *time-invariance*: the response to an impulse at $k$ is the response to an impulse
  at $0$, shifted — $\mathcal{S}\{\delta[n-k]\} = h[n-k]$. Substitute and you have the formula above.
  So the sum is not a modelling choice: **if a system is linear and time-invariant then it
  convolves, and there is nothing else it could do.** That is also why one measurement — the
  impulse response — determines the system completely, and why the whole frequency-domain
  toolkit exists: convolution is the only operation there is to diagonalize.
- Worked example: $x = [1, 2, 3]$, $h = [1, 1]$ (a running sum):
  $y = [1,\ 1{+}2,\ 2{+}3,\ 3] = [1, 3, 5, 3]$ — flip, slide, multiply, accumulate.
  Length: $N_x + N_h - 1$.

<svg viewBox="0 0 560 318" style="max-width:100%;height:auto" role="img" aria-label="convolution as flip, slide, multiply, accumulate: for x = [1, 2, 3] and h = [1, 1], the flipped h slides one step per output sample under the input, n = 0 to 3, giving y = [1, 3, 5, 3]">
  <text x="138" y="24" font-size="11" text-anchor="end" font-style="italic" opacity="0.85" fill="currentColor">k</text>
  <text x="172" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">−1</text>
  <text x="216" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">0</text>
  <text x="260" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">1</text>
  <text x="304" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">2</text>
  <text x="348" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">3</text>
  <text x="138" y="51.5" font-size="12" text-anchor="end" fill="currentColor">x[k]</text>
  <rect x="153" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.5"/>
  <text x="172" y="51.5" font-size="12" text-anchor="middle" opacity="0.5" fill="currentColor">0</text>
  <rect x="197" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="51.5" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <rect x="241" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="51.5" font-size="12" text-anchor="middle" fill="currentColor">2</text>
  <rect x="285" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="51.5" font-size="12" text-anchor="middle" fill="currentColor">3</text>
  <rect x="329" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.5"/>
  <text x="348" y="51.5" font-size="12" text-anchor="middle" opacity="0.5" fill="currentColor">0</text>
  <text x="388" y="51.5" font-size="12" fill="currentColor">h = [h[0], h[1]] = [1, 1]</text>
  <text x="24" y="82" font-size="11" opacity="0.9" fill="currentColor">flip h, then slide it one step per n</text>
  <text x="388" y="82" font-size="11" opacity="0.9" fill="currentColor">multiply, then add</text>
  <text x="138" y="109.5" font-size="12" text-anchor="end" fill="currentColor">n = 0</text>
  <rect x="153" y="92" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="172" y="109.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="197" y="92" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="109.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="109.5" font-size="12" fill="currentColor">1·1 = 1</text>
  <text x="492" y="109.5" font-size="12" font-weight="bold" fill="currentColor">y[0] = 1</text>
  <text x="138" y="153.5" font-size="12" text-anchor="end" fill="currentColor">n = 1</text>
  <rect x="197" y="136" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="153.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="241" y="136" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="153.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="153.5" font-size="12" fill="currentColor">1·1 + 2·1 = 3</text>
  <text x="492" y="153.5" font-size="12" font-weight="bold" fill="currentColor">y[1] = 3</text>
  <text x="138" y="197.5" font-size="12" text-anchor="end" fill="currentColor">n = 2</text>
  <rect x="241" y="180" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="197.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="285" y="180" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="197.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="197.5" font-size="12" fill="currentColor">2·1 + 3·1 = 5</text>
  <text x="492" y="197.5" font-size="12" font-weight="bold" fill="currentColor">y[2] = 5</text>
  <text x="138" y="241.5" font-size="12" text-anchor="end" fill="currentColor">n = 3</text>
  <rect x="285" y="224" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="241.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="329" y="224" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="348" y="241.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="241.5" font-size="12" fill="currentColor">3·1 = 3</text>
  <text x="492" y="241.5" font-size="12" font-weight="bold" fill="currentColor">y[3] = 3</text>
  <defs><marker id="arCv" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <line x1="172" y1="127" x2="216" y2="127" stroke="currentColor" stroke-width="1.1" opacity="0.7" marker-end="url(#arCv)"/>
  <line x1="216" y1="171" x2="260" y2="171" stroke="currentColor" stroke-width="1.1" opacity="0.7" marker-end="url(#arCv)"/>
  <line x1="260" y1="215" x2="304" y2="215" stroke="currentColor" stroke-width="1.1" opacity="0.7" marker-end="url(#arCv)"/>
  <text x="138" y="287.5" font-size="12" text-anchor="end" font-weight="bold" fill="currentColor">y[n]</text>
  <rect x="197" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <rect x="241" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">3</text>
  <rect x="285" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">5</text>
  <rect x="329" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="348" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">3</text>
  <text x="388" y="287.5" font-size="12" fill="currentColor">length 3 + 2 − 1 = 4</text>
</svg>

The worked example drawn as flip, slide, multiply, accumulate: for each output time $n$ the kernel $h = [1, 1]$ is laid backwards under the input — $h[0]$ under $x[n]$, $h[1]$ under $x[n-1]$ — and the overlapping pairs are multiplied and added. The four positions $n = 0, 1, 2, 3$ give $y = [1, 3, 5, 3]$, of length $3 + 2 - 1 = 4$.

- A CNN (convolutional neural network) layer is a *learned bank* of such $h$'s in 2D (plus nonlinearity; frameworks
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

The force pulse when a tool touches a wall, for example, may appear spread out even if contact began abruptly. **The reading this gives you.** Ask whether a broad measured event belongs to the world or to the pipeline impulse response. Cascaded filters change that response together, so evaluating a filter in isolation can miss the timing seen by the controller.

### 2. Sampling — the contract between continuous and digital

A controller sees a signal only as numbers taken at clock ticks and rounded to a resolution; between the ticks and below the resolution it sees nothing. This section is the contract that says when those numbers still determine the signal (sampling), what goes wrong when they do not (aliasing), how a digital system turns them back into a signal (the hold), and how coarse the rounding is (quantization).

- **Sampling** reads a continuous-time signal $x_c(t)$ once every $T_s$ seconds,
  $x[n] = x_c(nT_s)$, so the **sampling rate** is $f_s = 1/T_s$ samples per second (Hz). Half
  of it, $f_s/2$, is the **Nyquist frequency**: the highest frequency the samples can
  represent without ambiguity.
- **Nyquist–Shannon sampling theorem.** It has two conditions. The signal must be
  **band-limited** to $B$ Hz (no content above $B$), *and* the rate must exceed twice that
  band edge, the **Nyquist rate** $2B$:
  $$f_s > 2B$$
  Then the signal is *perfectly* recoverable from its samples, because sampling makes copies
  of the spectrum spaced $f_s$ apart and those copies do not overlap (proved in the folded note below). Example: audio
  band-limited to 20 kHz needs $f_s > 40$ kHz, which is why CD audio uses 44.1 kHz.

> [!note]- Deeper · 더 깊이
> **Why the theorem holds — a proof in four steps.** It needs the continuous-time Fourier transform, the counter-rotate-and-average of [[02-foundations/engineering-math|0.5 §7]] done with an integral over time (§3's frequency response is its version for sequences):
> $$X_c(f) = \int_{-\infty}^{\infty} x_c(t)\,e^{-j2\pi ft}\,dt, \qquad x_c(t) = \int_{-\infty}^{\infty} X_c(f)\,e^{j2\pi ft}\,df$$
> and "band-limited to $B$" means $X_c(f) = 0$ for $|f| > B$.
> *Step 1, the samples see only a folded spectrum.* Put $t = nT_s$ into the inverse transform and cut the frequency axis into bands of width $f_s$, writing $f = f' + kf_s$ with $|f'| \le f_s/2$ and $k$ any integer. Because $e^{j2\pi kf_s nT_s} = e^{j2\pi kn} = 1$,
> $$x[n] = \int_{-f_s/2}^{f_s/2} \Big(\sum_{k=-\infty}^{\infty} X_c(f' + kf_s)\Big)\,e^{j2\pi f' nT_s}\,df'$$
> so the samples depend on $X_c$ only through the sum of its copies shifted by every multiple of $f_s$: the "copies of the spectrum" above.
> *Step 2, with $f_s > 2B$ the copies miss the band.* For $|f'| \le f_s/2$ and $k \ne 0$, $|f' + kf_s| \ge f_s/2 > B$, so every copy except $k = 0$ is zero there and the bracket is $X_c(f')$ itself. The samples are then the Fourier-series coefficients of $X_c$ on that band, and those fix it: $X_c(f) = T_s\sum_n x[n]\,e^{-j2\pi fnT_s}$ for $|f| < f_s/2$.
> *Step 3, rebuild the signal.* Put that back into the inverse transform. Sample $n$ contributes $x[n]\,T_s\int_{-f_s/2}^{f_s/2} e^{j2\pi f(t - nT_s)}\,df$, and the integral evaluates to a sinc pulse:
> $$x_c(t) = \sum_n x[n]\,\operatorname{sinc}\Big(\frac{t - nT_s}{T_s}\Big), \qquad \operatorname{sinc}(u) = \frac{\sin \pi u}{\pi u}$$
> Each pulse is 1 at its own sample instant and 0 at every other one, so the sum passes through all the samples and fills in between them. That is the theorem's "perfectly recoverable", and in the frequency domain it is an ideal low-pass filter (§4) with cutoff $f_s/2$.
> *Step 4, failure is aliasing.* If $f_s \le 2B$, some copy with $k \ne 0$ lands inside the band and adds to $X_c(f')$: a tone at $f$ is counted at $f - kf_s$, which is the aliasing formula below.
> *Checked numerically:* take $x_c(t) = \cos(2\pi \cdot 1.3t) + 0.5\sin(2\pi \cdot 2.9t + 0.4)$, band-limited to $B = 2.9$ Hz, and sample it at $f_s = 10$ Hz ($2B = 5.8 < 10$). Between two samples, at $t = 0.53$ s, the sinc sum over the 8,001 samples nearest $t$ gives $-0.669513$ against the true $-0.669532$: the truncated sum is off by $2 \times 10^{-5}$, and ten times more samples cut that tenfold. (At a sample instant such as $t = 0.5$ s every sinc but one is zero, so the sum returns that sample for any signal, and a check there proves nothing.) A $7$ Hz tone at the same rate rebuilds at $t = 0.123$ s as $-0.680$, the value of the $3$ Hz cosine it aliases to, while the true $7$ Hz value is $+0.642$.

- **Worked: plant P3 at $1\,\mathrm{kHz}$.** The haptic servo uses $T=10^{-3}\,\mathrm{s}$, the period [[02-foundations/lab-kernel|0.7 Lab Kernel §1]] sets for haptic walls, so $f_s=1000\,\mathrm{Hz}$ and Nyquist is $500\,\mathrm{Hz}$. Contact you care about below $30\,\mathrm{Hz}$ is far inside the theorem; sampling is not the bottleneck. One encoder count is $\Delta x=r_m 2\pi/N=0.010\cdot 2\pi/1024=61.4\,\mu\mathrm{m}$ — a *quantization* stair in space, not a $T_s$. The two stairs have separate knobs: a finer encoder (larger $N$) shrinks the step in space, $\Delta x$; a faster clock (larger $f_s$) shrinks the step in time, $T$. *Which reading does the wall use?* The picture's wall law acts on the exact sample $x[n]$, which first lies inside the wall at the $5\,\mathrm{ms}$ tick. Fed the encoder count instead, it would switch on one tick early: the count line nearest the wall lies $4.7\,\mu\mathrm{m}$ inside it, so the $4\,\mathrm{ms}$ sample, $13.8\,\mu\mathrm{m}$ short of the wall, snaps to a reading $4.7\,\mu\mathrm{m}$ inside. Sampling makes contact late by up to one tick; rounding to a count moves it by up to half a count either way. The problem set redraws this sampler and hold on a clock four times slower.
- **Zero-order hold (ZOH).** The step back from samples to a continuous signal that the picture's staircase draws: it holds each sample until the next one,
  $$x_h(t) = x[n] \quad \text{for } nT \le t < (n+1)T$$
  so its output is piecewise constant, jumps at every tick, and never uses a future sample (it is causal). It is the reconstruction a DAC (digital-to-analog converter, the chip that turns numbers back into a voltage) or a servo actually performs, in place of the sinc sum above, which would need samples that have not arrived yet. *Why it runs $T/2$ late on average:* at a time $t$ inside interval $n$ the held value is $x(nT)$, a reading $t - nT$ seconds old, and that age runs evenly from $0$ to $T$, so it averages $T/2$. For a ramp $x = vt$ the staircase is the ramp shifted $T/2$ later on average. The frequency response says the same thing exactly. The hold's impulse response is a unit pulse of width $T$, whose transform is
  $$H_{\text{zoh}}(f) = \int_0^T e^{-j2\pi ft}\,dt = T\,e^{-j\pi fT}\operatorname{sinc}(fT)$$
  a pure delay of $T/2$ (phase $-\pi fT$, a group delay of $T/2$ at every frequency, §4) times a gentle droop in gain. For P3 ($T = 1$ ms) at $30$ Hz the phase is $-5.4°$ and the gain is $0.9985$ of its DC value $T$; at the $500$ Hz Nyquist frequency they are $-90°$ and $0.637$ of it. In a loop that renders a spring $K$, the delay is what costs stability. A spring felt $T/2$ late pushes with $F = -K\,x(t - T/2) \approx -Kx + K\tfrac{T}{2}\dot x$, by a first-order Taylor step ([[02-foundations/engineering-math|0.5 §2]]). A viscous damper pushes with $-b\dot x$ ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §4–§5]]), so the extra term is a damper with $b = -KT/2$: *negative* damping, which feeds energy into the motion instead of draining it. That is the term in the haptic wall bound of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]].
- **Aliasing** is what happens when the condition fails. Content at a frequency $f$ above
  $f_s/2$ shows up in the samples at
  $$f_{alias} = |f - k f_s|$$
  where $k$ is the integer nearest to $f/f_s$, so that $f_{alias}$ lands between $0$ and
  $f_s/2$. The true tone and its alias produce identical samples, so no later processing can
  separate them. Wheels spin backwards on camera; a 60 Hz vibration sampled at 50 Hz ($k = 1$)
  masquerades as 10 Hz; in the figure below, 170 Hz sampled at 200 Hz ($k = 1$) becomes 30 Hz.

<svg viewBox="0 0 560 236" style="max-width:100%;height:auto" role="img" aria-label="aliasing: a 170 Hz vibration sampled at 200 Hz looks like a phase-inverted 30 Hz tone">
  <line x1="56" y1="128" x2="536" y2="128" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="56" y1="186" x2="536" y2="186" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="56" y1="186" x2="56" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="56" y1="82" x2="56" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="56" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">0</text>
  <line x1="122.7" y1="186" x2="122.7" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="122.7" y1="82" x2="122.7" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="122.7" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">5</text>
  <line x1="189.3" y1="186" x2="189.3" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="189.3" y1="82" x2="189.3" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="189.3" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">10</text>
  <line x1="256" y1="186" x2="256" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="256" y1="82" x2="256" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="256" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">15</text>
  <line x1="322.7" y1="186" x2="322.7" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="322.7" y1="82" x2="322.7" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="322.7" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">20</text>
  <line x1="389.3" y1="186" x2="389.3" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="389.3" y1="82" x2="389.3" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="389.3" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">25</text>
  <line x1="456" y1="186" x2="456" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="456" y1="82" x2="456" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="456" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">30</text>
  <line x1="522.7" y1="186" x2="522.7" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="522.7" y1="82" x2="522.7" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="522.7" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">35</text>
  <text x="536" y="219" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">t (ms)</text>
  <text x="48" y="132" font-size="12" text-anchor="end" font-style="italic" fill="currentColor">x</text>
  <path d="M56 128L56.5 126.3L57.1 124.6L57.6 122.9L58.1 121.2L58.7 119.5L59.2 117.9L59.7 116.2L60.3 114.6L60.8 113L61.3 111.4L61.9 109.9L62.4 108.4L62.9 106.9L63.5 105.5L64 104.1L64.5 102.7L65.1 101.4L65.6 100.2L66.1 99L66.7 97.8L67.2 96.7L67.7 95.7L68.3 94.7L68.8 93.8L69.3 92.9L69.9 92.2L70.4 91.4L70.9 90.8L71.5 90.2L72 89.7L72.5 89.2L73.1 88.8L73.6 88.5L74.1 88.3L74.7 88.1L75.2 88L75.7 88L76.3 88.1L76.8 88.2L77.3 88.4L77.9 88.7L78.4 89L78.9 89.4L79.5 89.9L80 90.5L80.5 91.1L81.1 91.8L81.6 92.5L82.1 93.3L82.7 94.2L83.2 95.2L83.7 96.2L84.3 97.2L84.8 98.4L85.3 99.5L85.9 100.8L86.4 102L86.9 103.4L87.5 104.7L88 106.1L88.5 107.6L89.1 109.1L89.6 110.6L90.1 112.2L90.7 113.7L91.2 115.4L91.7 117L92.3 118.6L92.8 120.3L93.3 122L93.9 123.7L94.4 125.4L94.9 127.1L95.5 128.8L96 130.5L96.5 132.2L97.1 133.9L97.6 135.6L98.1 137.3L98.7 138.9L99.2 140.6L99.7 142.2L100.3 143.7L100.8 145.3L101.3 146.8L101.9 148.3L102.4 149.8L102.9 151.2L103.5 152.6L104 153.9L104.5 155.2L105.1 156.4L105.6 157.6L106.1 158.7L106.7 159.8L107.2 160.8L107.7 161.7L108.3 162.6L108.8 163.4L109.3 164.2L109.9 164.9L110.4 165.5L110.9 166.1L111.5 166.6L112 167L112.5 167.3L113.1 167.6L113.6 167.8L114.1 167.9L114.7 168L115.2 168L115.7 167.9L116.3 167.7L116.8 167.5L117.3 167.2L117.9 166.8L118.4 166.4L118.9 165.9L119.5 165.3L120 164.6L120.5 163.9L121.1 163.1L121.6 162.2L122.1 161.3L122.7 160.4L123.2 159.3L123.7 158.2L124.3 157.1L124.8 155.9L125.3 154.6L125.9 153.3L126.4 152L126.9 150.6L127.5 149.2L128 147.7L128.5 146.2L129.1 144.7L129.6 143.1L130.1 141.5L130.7 139.9L131.2 138.2L131.7 136.6L132.3 134.9L132.8 133.2L133.3 131.5L133.9 129.8L134.4 128.1L134.9 126.4L135.5 124.7L136 123L136.5 121.3L137.1 119.6L137.6 118L138.1 116.3L138.7 114.7L139.2 113.1L139.7 111.5L140.3 110L140.8 108.5L141.3 107L141.9 105.6L142.4 104.2L142.9 102.8L143.5 101.5L144 100.3L144.5 99L145.1 97.9L145.6 96.8L146.1 95.8L146.7 94.8L147.2 93.9L147.7 93L148.3 92.2L148.8 91.5L149.3 90.8L149.9 90.2L150.4 89.7L150.9 89.2L151.5 88.8L152 88.5L152.5 88.3L153.1 88.1L153.6 88L154.1 88L154.7 88.1L155.2 88.2L155.7 88.4L156.3 88.6L156.8 89L157.3 89.4L157.9 89.9L158.4 90.4L158.9 91L159.5 91.7L160 92.5L160.5 93.3L161.1 94.2L161.6 95.1L162.1 96.1L162.7 97.2L163.2 98.3L163.7 99.5L164.3 100.7L164.8 102L165.3 103.3L165.9 104.7L166.4 106.1L166.9 107.5L167.5 109L168 110.5L168.5 112.1L169.1 113.6L169.6 115.3L170.1 116.9L170.7 118.5L171.2 120.2L171.7 121.9L172.3 123.6L172.8 125.3L173.3 127L173.9 128.7L174.4 130.4L174.9 132.1L175.5 133.8L176 135.5L176.5 137.2L177.1 138.8L177.6 140.5L178.1 142.1L178.7 143.7L179.2 145.2L179.7 146.7L180.3 148.2L180.8 149.7L181.3 151.1L181.9 152.5L182.4 153.8L182.9 155.1L183.5 156.3L184 157.5L184.5 158.6L185.1 159.7L185.6 160.7L186.1 161.7L186.7 162.6L187.2 163.4L187.7 164.2L188.3 164.8L188.8 165.5L189.3 166L189.9 166.5L190.4 167L190.9 167.3L191.5 167.6L192 167.8L192.5 167.9L193.1 168L193.6 168L194.1 167.9L194.7 167.7L195.2 167.5L195.7 167.2L196.3 166.8L196.8 166.4L197.3 165.9L197.9 165.3L198.4 164.7L198.9 163.9L199.5 163.1L200 162.3L200.5 161.4L201.1 160.4L201.6 159.4L202.1 158.3L202.7 157.2L203.2 156L203.7 154.7L204.3 153.4L204.8 152.1L205.3 150.7L205.9 149.3L206.4 147.8L206.9 146.3L207.5 144.8L208 143.2L208.5 141.6L209.1 140L209.6 138.3L210.1 136.7L210.7 135L211.2 133.3L211.7 131.6L212.3 129.9L212.8 128.2L213.3 126.5L213.9 124.8L214.4 123.1L214.9 121.4L215.5 119.7L216 118.1L216.5 116.4L217.1 114.8L217.6 113.2L218.1 111.6L218.7 110.1L219.2 108.6L219.7 107.1L220.3 105.6L220.8 104.2L221.3 102.9L221.9 101.6L222.4 100.3L222.9 99.1L223.5 98L224 96.9L224.5 95.8L225.1 94.8L225.6 93.9L226.1 93L226.7 92.2L227.2 91.5L227.7 90.8L228.3 90.2L228.8 89.7L229.3 89.3L229.9 88.9L230.4 88.5L230.9 88.3L231.5 88.1L232 88L232.5 88L233.1 88L233.6 88.2L234.1 88.4L234.7 88.6L235.2 89L235.7 89.4L236.3 89.8L236.8 90.4L237.3 91L237.9 91.7L238.4 92.4L238.9 93.2L239.5 94.1L240 95.1L240.5 96.1L241.1 97.1L241.6 98.2L242.1 99.4L242.7 100.6L243.2 101.9L243.7 103.2L244.3 104.6L244.8 106L245.3 107.4L245.9 108.9L246.4 110.4L246.9 112L247.5 113.6L248 115.2L248.5 116.8L249.1 118.4L249.6 120.1L250.1 121.8L250.7 123.5L251.2 125.2L251.7 126.9L252.3 128.6L252.8 130.3L253.3 132L253.9 133.7L254.4 135.4L254.9 137.1L255.5 138.7L256 140.4L256.5 142L257.1 143.6L257.6 145.1L258.1 146.7L258.7 148.1L259.2 149.6L259.7 151L260.3 152.4L260.8 153.7L261.3 155L261.9 156.2L262.4 157.4L262.9 158.6L263.5 159.6L264 160.7L264.5 161.6L265.1 162.5L265.6 163.3L266.1 164.1L266.7 164.8L267.2 165.4L267.7 166L268.3 166.5L268.8 166.9L269.3 167.3L269.9 167.6L270.4 167.8L270.9 167.9L271.5 168L272 168L272.5 167.9L273.1 167.8L273.6 167.5L274.1 167.2L274.7 166.9L275.2 166.4L275.7 165.9L276.3 165.3L276.8 164.7L277.3 164L277.9 163.2L278.4 162.4L278.9 161.4L279.5 160.5L280 159.5L280.5 158.4L281.1 157.2L281.6 156L282.1 154.8L282.7 153.5L283.2 152.2L283.7 150.8L284.3 149.3L284.8 147.9L285.3 146.4L285.9 144.8L286.4 143.3L286.9 141.7L287.5 140.1L288 138.4L288.5 136.8L289.1 135.1L289.6 133.4L290.1 131.7L290.7 130L291.2 128.3L291.7 126.6L292.3 124.9L292.8 123.2L293.3 121.5L293.9 119.8L294.4 118.1L294.9 116.5L295.5 114.9L296 113.3L296.5 111.7L297.1 110.2L297.6 108.6L298.1 107.2L298.7 105.7L299.2 104.3L299.7 103L300.3 101.7L300.8 100.4L301.3 99.2L301.9 98L302.4 96.9L302.9 95.9L303.5 94.9L304 94L304.5 93.1L305.1 92.3L305.6 91.6L306.1 90.9L306.7 90.3L307.2 89.7L307.7 89.3L308.3 88.9L308.8 88.6L309.3 88.3L309.9 88.1L310.4 88L310.9 88L311.5 88L312 88.2L312.5 88.3L313.1 88.6L313.6 88.9L314.1 89.3L314.7 89.8L315.2 90.3L315.7 91L316.3 91.6L316.8 92.4L317.3 93.2L317.9 94.1L318.4 95L318.9 96L319.5 97.1L320 98.2L320.5 99.3L321.1 100.5L321.6 101.8L322.1 103.1L322.7 104.5L323.2 105.9L323.7 107.3L324.3 108.8L324.8 110.3L325.3 111.9L325.9 113.5L326.4 115.1L326.9 116.7L327.5 118.3L328 120L328.5 121.7L329.1 123.4L329.6 125.1L330.1 126.8L330.7 128.5L331.2 130.2L331.7 131.9L332.3 133.6L332.8 135.3L333.3 137L333.9 138.6L334.4 140.3L334.9 141.9L335.5 143.5L336 145L336.5 146.6L337.1 148.1L337.6 149.5L338.1 150.9L338.7 152.3L339.2 153.7L339.7 154.9L340.3 156.2L340.8 157.4L341.3 158.5L341.9 159.6L342.4 160.6L342.9 161.6L343.5 162.5L344 163.3L344.5 164.1L345.1 164.8L345.6 165.4L346.1 166L346.7 166.5L347.2 166.9L347.7 167.3L348.3 167.6L348.8 167.8L349.3 167.9L349.9 168L350.4 168L350.9 167.9L351.5 167.8L352 167.5L352.5 167.3L353.1 166.9L353.6 166.5L354.1 165.9L354.7 165.4L355.2 164.7L355.7 164L356.3 163.2L356.8 162.4L357.3 161.5L357.9 160.5L358.4 159.5L358.9 158.4L359.5 157.3L360 156.1L360.5 154.9L361.1 153.6L361.6 152.2L362.1 150.9L362.7 149.4L363.2 148L363.7 146.5L364.3 144.9L364.8 143.4L365.3 141.8L365.9 140.2L366.4 138.5L366.9 136.9L367.5 135.2L368 133.5L368.5 131.8L369.1 130.1L369.6 128.4L370.1 126.7L370.7 125L371.2 123.3L371.7 121.6L372.3 119.9L372.8 118.2L373.3 116.6L373.9 115L374.4 113.4L374.9 111.8L375.5 110.2L376 108.7L376.5 107.3L377.1 105.8L377.6 104.4L378.1 103L378.7 101.7L379.2 100.5L379.7 99.3L380.3 98.1L380.8 97L381.3 95.9L381.9 94.9L382.4 94L382.9 93.1L383.5 92.3L384 91.6L384.5 90.9L385.1 90.3L385.6 89.8L386.1 89.3L386.7 88.9L387.2 88.6L387.7 88.3L388.3 88.1L388.8 88L389.3 88L389.9 88L390.4 88.1L390.9 88.3L391.5 88.6L392 88.9L392.5 89.3L393.1 89.8L393.6 90.3L394.1 90.9L394.7 91.6L395.2 92.3L395.7 93.1L396.3 94L396.8 94.9L397.3 95.9L397.9 97L398.4 98.1L398.9 99.3L399.5 100.5L400 101.7L400.5 103L401.1 104.4L401.6 105.8L402.1 107.3L402.7 108.7L403.2 110.2L403.7 111.8L404.3 113.4L404.8 115L405.3 116.6L405.9 118.2L406.4 119.9L406.9 121.6L407.5 123.3L408 125L408.5 126.7L409.1 128.4L409.6 130.1L410.1 131.8L410.7 133.5L411.2 135.2L411.7 136.9L412.3 138.5L412.8 140.2L413.3 141.8L413.9 143.4L414.4 144.9L414.9 146.5L415.5 148L416 149.4L416.5 150.9L417.1 152.2L417.6 153.6L418.1 154.9L418.7 156.1L419.2 157.3L419.7 158.4L420.3 159.5L420.8 160.5L421.3 161.5L421.9 162.4L422.4 163.2L422.9 164L423.5 164.7L424 165.4L424.5 165.9L425.1 166.5L425.6 166.9L426.1 167.3L426.7 167.5L427.2 167.8L427.7 167.9L428.3 168L428.8 168L429.3 167.9L429.9 167.8L430.4 167.6L430.9 167.3L431.5 166.9L432 166.5L432.5 166L433.1 165.4L433.6 164.8L434.1 164.1L434.7 163.3L435.2 162.5L435.7 161.6L436.3 160.6L436.8 159.6L437.3 158.5L437.9 157.4L438.4 156.2L438.9 154.9L439.5 153.7L440 152.3L440.5 150.9L441.1 149.5L441.6 148.1L442.1 146.6L442.7 145L443.2 143.5L443.7 141.9L444.3 140.3L444.8 138.6L445.3 137L445.9 135.3L446.4 133.6L446.9 131.9L447.5 130.2L448 128.5L448.5 126.8L449.1 125.1L449.6 123.4L450.1 121.7L450.7 120L451.2 118.3L451.7 116.7L452.3 115.1L452.8 113.5L453.3 111.9L453.9 110.3L454.4 108.8L454.9 107.3L455.5 105.9L456 104.5L456.5 103.1L457.1 101.8L457.6 100.5L458.1 99.3L458.7 98.2L459.2 97.1L459.7 96L460.3 95L460.8 94.1L461.3 93.2L461.9 92.4L462.4 91.6L462.9 91L463.5 90.3L464 89.8L464.5 89.3L465.1 88.9L465.6 88.6L466.1 88.3L466.7 88.2L467.2 88L467.7 88L468.3 88L468.8 88.1L469.3 88.3L469.9 88.6L470.4 88.9L470.9 89.3L471.5 89.7L472 90.3L472.5 90.9L473.1 91.6L473.6 92.3L474.1 93.1L474.7 94L475.2 94.9L475.7 95.9L476.3 96.9L476.8 98L477.3 99.2L477.9 100.4L478.4 101.7L478.9 103L479.5 104.3L480 105.7L480.5 107.2L481.1 108.6L481.6 110.2L482.1 111.7L482.7 113.3L483.2 114.9L483.7 116.5L484.3 118.1L484.8 119.8L485.3 121.5L485.9 123.2L486.4 124.9L486.9 126.6L487.5 128.3L488 130L488.5 131.7L489.1 133.4L489.6 135.1L490.1 136.8L490.7 138.4L491.2 140.1L491.7 141.7L492.3 143.3L492.8 144.8L493.3 146.4L493.9 147.9L494.4 149.3L494.9 150.8L495.5 152.2L496 153.5L496.5 154.8L497.1 156L497.6 157.2L498.1 158.4L498.7 159.5L499.2 160.5L499.7 161.4L500.3 162.4L500.8 163.2L501.3 164L501.9 164.7L502.4 165.3L502.9 165.9L503.5 166.4L504 166.9L504.5 167.2L505.1 167.5L505.6 167.8L506.1 167.9L506.7 168L507.2 168L507.7 167.9L508.3 167.8L508.8 167.6L509.3 167.3L509.9 166.9L510.4 166.5L510.9 166L511.5 165.4L512 164.8L512.5 164.1L513.1 163.3L513.6 162.5L514.1 161.6L514.7 160.7L515.2 159.6L515.7 158.6L516.3 157.4L516.8 156.2L517.3 155L517.9 153.7L518.4 152.4L518.9 151L519.5 149.6L520 148.1L520.5 146.7L521.1 145.1L521.6 143.6L522.1 142L522.7 140.4L523.2 138.7L523.7 137.1L524.3 135.4L524.8 133.7L525.3 132L525.9 130.3L526.4 128.6L526.9 126.9L527.5 125.2L528 123.5L528.5 121.8L529.1 120.1L529.6 118.4L530.1 116.8L530.7 115.2L531.2 113.6L531.7 112L532.3 110.4L532.8 108.9L533.3 107.4L533.9 106L534.4 104.6L534.9 103.2L535.5 101.9L536 100.6" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <path d="M56 128L57.6 128.9L59.2 129.8L60.8 130.7L62.4 131.6L64 132.5L65.6 133.4L67.2 134.3L68.8 135.2L70.4 136.1L72 137L73.6 137.9L75.2 138.7L76.8 139.6L78.4 140.5L80 141.3L81.6 142.2L83.2 143L84.8 143.8L86.4 144.7L88 145.5L89.6 146.3L91.2 147.1L92.8 147.9L94.4 148.7L96 149.4L97.6 150.2L99.2 150.9L100.8 151.7L102.4 152.4L104 153.1L105.6 153.8L107.2 154.5L108.8 155.2L110.4 155.8L112 156.5L113.6 157.1L115.2 157.7L116.8 158.3L118.4 158.9L120 159.5L121.6 160L123.2 160.5L124.8 161.1L126.4 161.6L128 162L129.6 162.5L131.2 163L132.8 163.4L134.4 163.8L136 164.2L137.6 164.6L139.2 164.9L140.8 165.3L142.4 165.6L144 165.9L145.6 166.2L147.2 166.4L148.8 166.7L150.4 166.9L152 167.1L153.6 167.3L155.2 167.4L156.8 167.6L158.4 167.7L160 167.8L161.6 167.9L163.2 167.9L164.8 168L166.4 168L168 168L169.6 168L171.2 167.9L172.8 167.9L174.4 167.8L176 167.7L177.6 167.6L179.2 167.4L180.8 167.3L182.4 167.1L184 166.9L185.6 166.6L187.2 166.4L188.8 166.1L190.4 165.9L192 165.5L193.6 165.2L195.2 164.9L196.8 164.5L198.4 164.2L200 163.8L201.6 163.3L203.2 162.9L204.8 162.5L206.4 162L208 161.5L209.6 161L211.2 160.5L212.8 159.9L214.4 159.4L216 158.8L217.6 158.2L219.2 157.6L220.8 157L222.4 156.4L224 155.7L225.6 155.1L227.2 154.4L228.8 153.7L230.4 153L232 152.3L233.6 151.6L235.2 150.9L236.8 150.1L238.4 149.3L240 148.6L241.6 147.8L243.2 147L244.8 146.2L246.4 145.4L248 144.6L249.6 143.7L251.2 142.9L252.8 142.1L254.4 141.2L256 140.4L257.6 139.5L259.2 138.6L260.8 137.8L262.4 136.9L264 136L265.6 135.1L267.2 134.2L268.8 133.3L270.4 132.4L272 131.5L273.6 130.6L275.2 129.7L276.8 128.8L278.4 127.9L280 127L281.6 126.1L283.2 125.2L284.8 124.3L286.4 123.4L288 122.5L289.6 121.6L291.2 120.7L292.8 119.8L294.4 118.9L296 118.1L297.6 117.2L299.2 116.3L300.8 115.4L302.4 114.6L304 113.7L305.6 112.9L307.2 112.1L308.8 111.2L310.4 110.4L312 109.6L313.6 108.8L315.2 108L316.8 107.3L318.4 106.5L320 105.7L321.6 105L323.2 104.2L324.8 103.5L326.4 102.8L328 102.1L329.6 101.4L331.2 100.8L332.8 100.1L334.4 99.5L336 98.8L337.6 98.2L339.2 97.6L340.8 97.1L342.4 96.5L344 95.9L345.6 95.4L347.2 94.9L348.8 94.4L350.4 93.9L352 93.4L353.6 93L355.2 92.6L356.8 92.2L358.4 91.8L360 91.4L361.6 91L363.2 90.7L364.8 90.4L366.4 90.1L368 89.8L369.6 89.5L371.2 89.3L372.8 89.1L374.4 88.9L376 88.7L377.6 88.5L379.2 88.4L380.8 88.3L382.4 88.2L384 88.1L385.6 88.1L387.2 88L388.8 88L390.4 88L392 88L393.6 88.1L395.2 88.1L396.8 88.2L398.4 88.3L400 88.5L401.6 88.6L403.2 88.8L404.8 89L406.4 89.2L408 89.4L409.6 89.6L411.2 89.9L412.8 90.2L414.4 90.5L416 90.8L417.6 91.2L419.2 91.5L420.8 91.9L422.4 92.3L424 92.7L425.6 93.1L427.2 93.6L428.8 94.1L430.4 94.6L432 95.1L433.6 95.6L435.2 96.1L436.8 96.7L438.4 97.2L440 97.8L441.6 98.4L443.2 99L444.8 99.7L446.4 100.3L448 101L449.6 101.7L451.2 102.3L452.8 103L454.4 103.8L456 104.5L457.6 105.2L459.2 106L460.8 106.7L462.4 107.5L464 108.3L465.6 109.1L467.2 109.9L468.8 110.7L470.4 111.5L472 112.3L473.6 113.2L475.2 114L476.8 114.9L478.4 115.7L480 116.6L481.6 117.5L483.2 118.3L484.8 119.2L486.4 120.1L488 121L489.6 121.9L491.2 122.8L492.8 123.7L494.4 124.6L496 125.5L497.6 126.4L499.2 127.3L500.8 128.2L502.4 129.1L504 130L505.6 130.9L507.2 131.8L508.8 132.7L510.4 133.6L512 134.5L513.6 135.4L515.2 136.3L516.8 137.2L518.4 138L520 138.9L521.6 139.8L523.2 140.6L524.8 141.5L526.4 142.4L528 143.2L529.6 144L531.2 144.8L532.8 145.7L534.4 146.5L536 147.3" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <g fill="currentColor"><circle cx="56" cy="128" r="3.4"/><circle cx="122.7" cy="160.4" r="3.4"/><circle cx="189.3" cy="166" r="3.4"/><circle cx="256" cy="140.4" r="3.4"/><circle cx="322.7" cy="104.5" r="3.4"/><circle cx="389.3" cy="88" r="3.4"/><circle cx="456" cy="104.5" r="3.4"/><circle cx="522.7" cy="140.4" r="3.4"/></g>
  <line x1="56" y1="18" x2="78" y2="18" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text x="84" y="22" font-size="11" fill="currentColor">the real vibration, 170 Hz</text>
  <circle cx="304" cy="18" r="3.4" fill="currentColor"/>
  <text x="314" y="22" font-size="11" fill="currentColor">the samples, every 5 ms (f<tspan dy="3" font-size="10">s</tspan><tspan dx="3.1" dy="-3">= 200 Hz)</tspan></text>
  <line x1="56" y1="38" x2="78" y2="38" stroke="currentColor" stroke-width="2.2"/>
  <text x="84" y="42" font-size="11" fill="currentColor">what the samples show: 30 Hz, phase-inverted (−sin 2π·30t)</text>
</svg>

A $170\,\mathrm{Hz}$ vibration (thin) sampled every $5\,\mathrm{ms}$ ($f_s = 200\,\mathrm{Hz}$, dots) gives exactly the samples of a $30\,\mathrm{Hz}$ tone (thick), because $170 - 200 = -30$: the ghost is $-\sin(2\pi \cdot 30t)$, a $30\,\mathrm{Hz}$ tone with its phase inverted. Nothing computed from the eight dots can tell the two apart, so the filtering has to happen before the sampler.

- Therefore: **anti-alias filter before downsampling**, always (this includes decimating
  IMU logs in software). An anti-alias filter is a low-pass filter (§4) placed before the
  sampler or the decimator that removes content above the *new* $f_s/2$, so nothing is left
  that could fold down. On P6's load cell the analog one is a single RC stage, sized against its
  $12$-bit ADC: the RC low-pass, the ADC, and the trade between the filter's cutoff and what still folds down are [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics §5, §10 and §12]].
- Engineering corollary: pick sensor rates from the fastest dynamics you must *observe*,
  with margin — a 10 Hz perception loop cannot even see, let alone damp, a 50 Hz vibration.
- **Quantization** rounds each sample to one of $2^N$ levels, where $N$ is the number of bits
  of the ADC (analog-to-digital converter; this $N$ counts bits, not the encoder's lines per revolution above). Over an input range $R$ the step is
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
  steps of $2.44$ mV and RMS quantization noise of $0.70$ mV. This is the *other* half of digitization. When a quantized sensor's error really is white, and when it is a fixed bias instead (an encoder at rest), is [[04-robotics/sensor-models|3.2 Sensor Models & Noise §4]]. The same rounding happens when a number is printed with a fixed count of decimals, which is how a log file quietly quantizes its time column ([[02-foundations/tools/config-data-formats|12.4 Config and Data Formats §2]]).
- Where this contract becomes a stability problem: a haptic loop rendering a virtual wall
  must close on a human hand every millisecond, and there sampling and quantization stop
  being accuracy questions and start deciding whether the device buzzes
  ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]]).

### 3. Frequency domain — the diagonalizing basis

Two fluctuations that look alike in time can need opposite treatment: a narrow machinery vibration peak and a broad contact transient can overlap in time yet occupy different frequencies, and only one of them should be filtered out. This section builds the frequency view in which such signals separate, and shows why it simplifies every LTI system.

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
- **DFT** (discrete Fourier transform) maps a block of $N$ samples (here $N$ is the block length) $x[0], \ldots, x[N-1]$ to
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

Removing such a machinery peak may help, while indiscriminate smoothing may erase the contact signal. **The reading this gives you.** Relate spectral peaks to operating conditions and preserve the windowing and sampling details. A peak in a finite-window spectrum is evidence to investigate, not automatic identification of a physical source.

### 4. Filtering — design basics

Every sensor signal carries noise the controller should not act on, and removing it has a price: a filter that smooths also delays. This section names the filter types, builds the two families (FIR and IIR) with what each costs in delay, and measures that delay in samples — the number §6 turns into milliseconds on P3.

- **Filter types, named by the frequencies they pass.** With a cutoff $f_c$, an ideal
  **low-pass** filter has $|H(f)| = 1$ for $|f| < f_c$ and $|H(f)| = 0$ above it; a
  **high-pass** filter is the reverse; a **band-pass** filter keeps one band; a **notch**
  filter removes one narrow band around a frequency $f_0$. Real filters replace the sharp edge
  with a transition band. Choosing: low-pass for sensor noise, high-pass for drift removal,
  notch at known vibration harmonics, complementary filters to fuse IMU accel (low-passed) + gyro
  (high-passed).
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
- **Phase delay and group delay** state how late a filter's output is. The phase response is
  $\angle H(f)$ (§3). The **group delay** is its negative slope, measured in samples,
  $$\tau_g(f) = -\frac{1}{2\pi}\,\frac{d\,\angle H(f)}{df}$$
  so a filter whose phase falls linearly with frequency delays every frequency by the same
  number of samples and keeps the waveform's shape. The symmetric 5-tap moving average has
  $\angle H(f) = -4\pi f$ in its passband, hence $\tau_g = 2$ samples everywhere. The exponential
  smoother of the next bullet is not linear-phase: with $\alpha = 0.9$ at $f = 0.05$ cycles/sample its gain is
  $0.32$ and its phase $-62.6°$, and the delay changes from one frequency to the next.
- **IIR** (infinite impulse response) filter: the output also feeds back past *outputs*,
  $$y[n] = \sum_{k=0}^{M} b_k\, x[n-k] - \sum_{k=1}^{N} a_k\, y[n-k]$$
  where the $b_k$ weight inputs as in an FIR and the $a_k$ weight the $N$ previous outputs ($N$ here is the filter's order, the number of past outputs fed back).
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
  D-term, the derivative term of a controller, which acts on velocity). This is the practical reason to prefer model-based estimation:
  under an accurate linear-Gaussian state-space model and noise covariances, the
  **Kalman filter** ([[02-foundations/probability|derived in 3. Probability §5]]) minimizes mean-square
  estimation error. Model mismatch removes that guarantee.

### 5. Bridge to control: transforms

A filter inside a feedback loop cannot be judged alone: its delay becomes part of the loop, and whether the loop settles or grows depends on filter, plant and controller together. Transforms help because they expose how a system changes each frequency and how its internal dynamics grow or decay, in the one language control uses for all three.

- The Laplace transform (continuous, defined in [[02-foundations/engineering-math|0.5 §9]]) / **Z-transform** (discrete) generalize Fourier:
  convolution ↦ multiplication by a *transfer function* $H(s)$ or $H(z)$.
- The **Z-transform** turns a sequence into a function of a complex variable $z$,
  $$X(z) = \sum_n x[n]\, z^{-n}$$
  so a one-sample delay becomes multiplication by $z^{-1}$. It is tied to the Laplace variable
  by $z = e^{sT_s}$, and on the unit circle $z = e^{j2\pi f}$ it reduces to the frequency
  response of §3. The tie is sampling itself: a continuous mode $e^{st}$ read every $T_s$ gives $e^{snT_s} = (e^{sT_s})^n$, a discrete mode $z^n$ with $z = e^{sT_s}$. Since $|e^{sT_s}| = e^{\operatorname{Re}(s)\,T_s}$, a pole in the left half-plane ($\operatorname{Re}(s) < 0$) lands inside the unit circle ($|z| < 1$), so the two stability tests of the next bullet are one test in two coordinates ([[02-foundations/engineering-math|0.5 §8]]). The leaky heater P4 of [[02-foundations/lab-plants|0.6]], with its pole at $s = -1$, sampled every $T_s = 0.1\,\mathrm{s}$ lands at $z = e^{-0.1} = 0.905$, the factor of its sampled model there. The **transfer function** is the ratio of output to input transforms, with
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

A smoothing filter, for example, may attenuate vibration while introducing delay into the feedback used for contact control. **The reading this gives you.** Inspect both gain and phase before calling a filtered signal better. Also distinguish state-space modes from transfer-function poles: unobservable or uncontrollable modes (a mode the output never shows, or one the input never excites; defined with their rank tests in [[02-foundations/linear-algebra|1. Linear Algebra §5]]) can disappear through cancellation, so the pole–eigenvalue correspondence needs a minimal realization when used as an equality.

### 6. Sensor-pipeline habits (field-tested)

A pipeline that is right on paper can still hand the controller a signal that is late, stale, or smoothed of the very event that mattered, and a plot of it shows none of this. Three habits prevent it; each comes with the reason it exists and, on P3's $1\,\mathrm{kHz}$ loop from the picture, what skipping it costs.

- **Log raw, filter later; never filter twice implicitly (driver + your code).** A raw log can be filtered again any way you like after the fact; a filtered log has already discarded what the filter removed, and its delay cannot be taken back. Filtering twice is the silent version of the same loss, because the delays of filters in series add. Each symmetric 5-tap moving average of §4 delays by $(M-1)/2 = 2$ samples, so one in the driver and one in your controller delay P3's position by $2 + 2 = 4$ samples: $4\,\mathrm{ms}$ at $1\,\mathrm{kHz}$, eight times the hold's average lag of $0.5\,\mathrm{ms}$ (§2). At the handle's peak speed, the $30.7\,\mathrm{mm/s}$ it has as it crosses the wall, that is $30.7 \times 4 = 122.8\,\mu\mathrm{m}$, two encoder counts of travel into the wall before the filtered signal shows the crossing.
- **Timestamp at the sensor, synchronize clocks before fusing (extrinsics — the sensors' poses relative to one another — *and* time offsets for camera-LiDAR-IMU).** A reading describes the world at the instant it was taken, not the instant it arrived, and a time error $\delta$ on something moving at speed $v$ becomes a position error $v\delta$. That error is a bias, not scatter, so no noise setting absorbs it. On P3, stamping a position when the controller reads it, one tick after the encoder latched it, gives $\delta = 1\,\mathrm{ms}$ and, at peak speed, an error of $30.7\,\mu\mathrm{m}$, half a count. Across machines the offsets reach tens of milliseconds: on P6's cart a range reading that arrives $70\,\mathrm{ms}$ late at $0.5\,\mathrm{m/s}$ describes the world $3.5\,\mathrm{cm}$ ago, three and a half times that sensor's noise (the running object of [[04-robotics/state-estimation-slam|3. State Estimation]]). A time offset is calibrated like an extrinsic, by correlating the motion two sensors see ([[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §5]]).
- **Check the spectrum before choosing a filter: name the noise before you fight it.** A cutoff has to fall between the band that carries the signal and the band that carries the noise, and only a spectrum shows where that gap is. On P3 the velocity from differenced positions alternates $0$ and $61.4\,\mathrm{mm/s}$ (the picture), a pattern that repeats every two ticks and so sits at $500\,\mathrm{Hz}$, the Nyquist frequency, while hand-and-wall contact lives below $30\,\mathrm{Hz}$ (§2). The 5-tap average of §4 has gain $|\sin(5\pi f)/(5\sin\pi f)|$, which is $0.2$ at $f = 0.5$ and $0.965$ at $30\,\mathrm{Hz}$ ($f = 0.03$): it shrinks the swing around the true $30.7\,\mathrm{mm/s}$ from $\pm30.7$ to $\pm6.1\,\mathrm{mm/s}$ and passes the contact band almost whole, for $2\,\mathrm{ms}$ of delay. The chatter is quantization, not random noise, and it has a failure no average fixes: when the handle creeps, a whole window can pass without a new count and the averaged velocity reads exactly zero ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]).

A common case: a driver may already smooth force readings before a second filter is applied in the controller. The combined stream looks clean while contact onset arrives late. Keeping the raw stream and documenting both stages makes that delay diagnosable. **The reading this gives you.** Trace the signal from acquisition to decision, including clock conversion and every transformation. A plot without its processing history cannot tell you whether the apparent smoothness came from better sensing or from removing the transient that mattered.

> [!tip] Going deeper · 더 깊이
> Oppenheim and Schafer's *Discrete-Time Signal Processing* is the standard course this page compresses. §2 proves the sampling theorem in four steps; its sampling and DFT chapters add the convergence details and practical reconstruction filters that proof leaves out.

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

Tier B. **P3** from [[02-foundations/lab-plants|0.6]], the Running object's handle, with one knob changed per item: the loop four times slower, $250\,\mathrm{Hz}$ ($T = 4\,\mathrm{ms}$), in items 1 and 2, and a finer encoder, $N = 4096$ counts per revolution, in item 3 at the usual $1\,\mathrm{kHz}$. This page §2. No simulator.

1. **Draw.** The picture above for the same handle and encoder on a loop four times slower, $250\,\mathrm{Hz}$ ($T=4\,\mathrm{ms}$): continuous handle position $x(t)$ through an ideal sampler of period $T$, then a zero-order hold, over eight ticks. Mark the wall $x_w$, the Nyquist frequency, the average lag of the hold, and the encoder grid. At the handle's peak speed, $30.7\,\mathrm{mm/s}$, how many new counts appear per tick now, and what does the velocity from differenced positions read?
2. **Derive.** On the $250\,\mathrm{Hz}$ loop: the Nyquist frequency and the largest band $B$ the theorem allows; where a $170\,\mathrm{Hz}$ motor vibration lands in the samples; and the zero-order hold's phase at $30\,\mathrm{Hz}$, against $-5.4°$ at $1\,\mathrm{kHz}$. Is $250\,\mathrm{Hz}$ still enough, on sampling grounds alone, for contact below $30\,\mathrm{Hz}$, and what did the slower clock cost?
3. **Interpret.** Back at $1\,\mathrm{kHz}$, the encoder is replaced by one with $N = 4096$ counts per revolution. Compute the new count $\Delta x = r_m\,2\pi/N$, the smallest force step $k_w\,\Delta x$ in the wall, and the speed at which one new count appears per tick. What does the velocity from differenced counts read at the handle's peak speed now, and which of the picture's two effects — the velocity chatter or the hold's lag — did the finer encoder remove?

> [!note]- How to draw it · 그리는 법
> - The signal path as blocks in a row: the handle giving $x(t)$; an ideal sampler, drawn as a switch that closes for an instant every $T=4\,\mathrm{ms}$, with $f_s=250\,\mathrm{Hz}$ and Nyquist $125\,\mathrm{Hz}$ under it; the sequence $x[n]=x(nT)$; a zero-order hold, drawn as a box whose output is a staircase; and the held signal that the wall law actually sees.
> - Under the hold, the one thing it does: it holds $x[n]$ constant on $[nT,\ (n+1)T)$ and then jumps.
> - Underneath, one time axis about $32\,\mathrm{ms}$ long so that eight ticks fit, with $x(t)$ as a smooth curve rising through the wall and a dot on it at each tick. Those dots are $x[n]$, and nothing between them exists for the controller.
> - The ZOH staircase on the same axis, each tread flat at the height of the *previous* dot. Shade the sliver between curve and staircase on one tread and label it: the hold is late by $T/2=2\,\mathrm{ms}$ on average, four times the picture's $0.5\,\mathrm{ms}$.
> - The wall $x_w=0.030\,\mathrm{m}$ as a dashed horizontal line, and a circle on the first tread above it: contact begins at a tick, now up to $4\,\mathrm{ms}$ after the true crossing.
> - Faint horizontal gridlines one encoder count apart, $\Delta x=61.4\,\mu\mathrm{m}$ as before, with the dots snapped to the nearest line. Label the two steps so they cannot be confused: $T$ along time, set by the clock, which changed, and $\Delta x$ along space, set by the encoder, which did not.
> - At the bottom, the speed at which one new count appears per tick, $\Delta x/T=15.3\,\mathrm{mm/s}$. At its peak speed, $30.7\,\mathrm{mm/s}$, the handle moves $122.8\,\mu\mathrm{m}$ per tick, two counts, so every tick near the crossing reports motion and the differenced velocity is a steady $30.7\,\mathrm{mm/s}$ — not the $0$, $61.4$ alternation of the picture above.

> [!tip]- Solutions
> 1. Sampler $x[n]=x(nT)$ every $4\,\mathrm{ms}$ ($f_s=250\,\mathrm{Hz}$, Nyquist $125\,\mathrm{Hz}$), so eight ticks span $32\,\mathrm{ms}$. The ZOH holds each value on $[nT,(n+1)T)$ and runs $T/2=2\,\mathrm{ms}$ late on average, four times the picture's $0.5\,\mathrm{ms}$; contact still begins at a tick, now up to $4\,\mathrm{ms}$ after the true crossing. The encoder grid is unchanged at $61.4\,\mu\mathrm{m}$, but one count per tick now means only $\Delta x/T=15.3\,\mathrm{mm/s}$, so at the peak speed of $30.7\,\mathrm{mm/s}$ each tick sees two new counts and the differenced velocity reads a steady $30.7\,\mathrm{mm/s}$ instead of alternating $0$ and $61.4\,\mathrm{mm/s}$. The slower clock removed the velocity chatter by making every reading four times staler: the clock sets how old a reading is, the encoder how fine. Nyquist $125\,\mathrm{Hz}$ is still well above $30\,\mathrm{Hz}$.
> 2. $f_s = 250\,\mathrm{Hz}$, so Nyquist is $125\,\mathrm{Hz}$ and the theorem allows $B < 125\,\mathrm{Hz}$. The $170\,\mathrm{Hz}$ vibration is above Nyquist; the multiple of $f_s$ nearest to it is $250\,\mathrm{Hz}$ ($k = 1$), so it lands at $|170 - 250| = 80\,\mathrm{Hz}$, inside the band, where nothing downstream can tell it from a real $80\,\mathrm{Hz}$ signal: only an analog anti-alias filter before the sampler removes it. The hold's phase at $30\,\mathrm{Hz}$ is $-\pi fT = -\pi \cdot 30 \cdot 0.004 = -0.377\,\mathrm{rad} = -21.6°$, four times the $-5.4°$ at $1\,\mathrm{kHz}$, since the lag grows in proportion to $T$. On sampling grounds alone $250\,\mathrm{Hz}$ still covers a $30\,\mathrm{Hz}$ contact band. What the slower clock costs is a lower Nyquist, which lets vibrations above $125\,\mathrm{Hz}$ fold into the band, and four times the lag, which in a wall loop is what the stability bound of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] charges.
> 3. $\Delta x = 0.010 \cdot 2\pi/4096 = 15.3\,\mu\mathrm{m}$, a quarter of $61.4\,\mu\mathrm{m}$, and the smallest force step is $k_w\,\Delta x = 400 \times 15.3\,\mu\mathrm{m} = 6.1\,\mathrm{mN}$, against $25\,\mathrm{mN}$ before. One new count per tick now happens at $\Delta x/T = 15.3\,\mathrm{mm/s}$, so at the peak speed of $30.7\,\mathrm{mm/s}$ the handle crosses two counts every tick, and near the crossing the differenced velocity reads a steady $30.7\,\mathrm{mm/s}$ instead of alternating $0$ and $61.4\,\mathrm{mm/s}$. The finer encoder removed the chatter; the hold's $0.5\,\mathrm{ms}$ lag is untouched, because the clock sets it — $N$ shrinks the step in space, $f_s$ the step in time. Item 1 removed the same chatter by slowing the clock, which made every reading four times staler; the finer encoder removes it at no cost in delay.

### Robotics bridge

Filtering, sampling, aliasing, and sensor timing continue in [[04-robotics/state-estimation-slam|State Estimation]] and [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]].

### Sources

- A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Prentice Hall, 2010 — the standard course that §1–§5 compress: LTI systems and convolution, sampling and its proof, the DFT, filter design and the z-transform.
- The numeric examples on this page, P3's included, were computed here from the stated numbers, not quoted from a source; recompute them rather than trusting them.

## 한국어

*[[02-foundations/probability|3. 확률]]과 [[02-foundations/engineering-math|0.5]]의 오일러 공식 위에 선다. 도메인 다리 하나다: 여기서부터 데이터는 주어지는 것이
아니라 센서에서 도착한다. [[02-foundations/rl-basics|7. RL 기초]]와의 순서는 자유다.*

건설로봇이 싣고 다니는 모든 센서 — 카메라, LiDAR(레이저로 훑어 거리를 재는 센서), IMU(관성 측정 장치: 가속도계와 자이로), 엔코더(축의 회전을 세는 센서) — 는 샘플링된, 노이즈 낀
신호를 건네준다. 교재 수준의 서술: 손으로 푸는 합성곱, 수식이 있는 샘플링 정리, DFT/FFT,
필터 설계 기초, 그리고 제어의 전달함수로 가는 다리.

> [!note] 왜 배우는가 · Why this matters
> 카메라, LiDAR, IMU, 엔코더는 모두 로봇에게 샘플링되고 잡음 섞인 신호를 건넨다. 그래서 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택 가운데 두 층의 수학 바닥이다. 하나는 인식이고, 다른 하나는 필터를 거친 힘 신호로 접촉이 시작됐는지 판정하는 접촉·힘·촉각 피드백 층이다. "*저 패널을 프레임에 설치해*"로 말하면 패널과 프레임을 식별하는 단계와 접촉을 감지하는 단계 밑에 놓인다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 이것을 모르면 데이터가 소리 없이 속인다. $200\,\mathrm{Hz}$로 찍은 IMU 로그에서 $170\,\mathrm{Hz}$ 모터 진동은 $30\,\mathrm{Hz}$짜리 "고유 모드"로 나타나 뒤의 어떤 소프트웨어로도 지울 수 없고, 5탭 평활기 두 개를 직렬로 두면 P3(카탈로그의 1축 햅틱 핸들, [[02-foundations/lab-plants|0.6]])의 벽이 접촉을 $4\,\mathrm{ms}$ 늦게 안다. 뒤의 페이지들은 이것을 절 단위로 딛고 선다. [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]은 §2의 샘플링과 양자화를, [[04-robotics/control-theory-ce397|5. 제어 이론]]은 §1의 LTI 시스템과 §4의 필터 지연을, [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]은 §2의 홀드와 §5의 Z-변환을, [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]]은 §1과 §3을 쓴다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 1 블록 [[02-foundations/overview#통과 점검 — 기초는 끝났는가|기초 통과 점검]]의 10번 문제가 이 페이지를 시험하고, 2 블록인 로보틱스 공통 트랙이 이 위에서 돈다. 이 페이지를 마치면 샘플링 주기를 고르고, 에일리어스가 어디에 떨어질지 말하고, 필터의 지연이 제어기에 닿기 전에 몇 밀리초인지 값을 매길 수 있다.

> [!note] 처음이라면 · First pass
> 60~90분짜리 회차 두 번 반쯤 든다. 1회차: 이 페이지의 대상, 그림, §1. §1의 합성곱 그림은 손으로 다시 해 본다. 2회차: 증명은 접어 둔 채 §2 — 실제로 발목을 잡는 것은 샘플링, 에일리어싱, 영차 홀드, 양자화다. 3회차는 짧다. 필터의 이득과 위상이 무엇인지 말해 주는 §3의 주파수 응답 항목, 이어서 §6이 값을 매기는 §4의 FIR 항목과 군지연 항목, 그리고 §6의 현장 습관. 끝으로 스스로 점검 1–2번, 과제 1번, [[02-foundations/overview#통과 점검 — 기초는 끝났는가|통과 점검]] 10번을 푼다. §3의 나머지와 §5는 기계장치이니 논문이 주파수 영역에서 무언가 할 때 펴라.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P3**, 곧 1축 햅틱 핸들이고, 이 페이지가 쓰는 숫자는 다음과 같다. 강성 $k_w = 400\,\mathrm{N/m}$의 가상 벽이 $x_w = 0.030\,\mathrm{m}$에 있고($+x$가 벽 안쪽), 모터 풀리 반지름은 $r_m = 0.010\,\mathrm{m}$, 엔코더는 한 바퀴에 $N = 1024$ 카운트다. 서보 루프는 $1\,\mathrm{kHz}$, 곧 [[02-foundations/lab-kernel|0.7 Lab Kernel §1]]이 햅틱 벽에 정한 주기 $T = 1\,\mathrm{ms}$로 돈다. 그림에서 핸들은 $30\,\mathrm{Hz}$로 흔들리며 $t_c = 4.45\,\mathrm{ms}$에 벽을 지난다.
$$x(t) = x_w + A\sin\big(2\pi \cdot 30\,\mathrm{Hz} \cdot (t - t_c)\big), \qquad A = 0.163\,\mathrm{mm}$$
사인은 0을 지날 때 가장 가파르므로 속도는 벽을 지나는 순간 가장 커서 $2\pi \cdot 30\,\mathrm{Hz} \cdot A = 30.7\,\mathrm{mm/s}$이고, 이는 눈금마다 엔코더 카운트가 새로 하나씩 생기는 속도 $\Delta x/T = 61.4\,\mathrm{mm/s}$의 정확히 절반이다. §2와 §6은 로드셀의 안티에일리어스 필터와 시계를 보이려고 **P6**, 곧 카탈로그의 1차원 카트([[02-foundations/lab-plants|0.6]])도 빌려 쓴다.

*범위: 이 페이지는 이산시간 신호와 시스템 — 합성곱, 샘플링과 양자화, DFT, 필터 기초, Z-변환 — 을 P3 위에서 가르친다. 필터나 ADC를 실제로 만드는 회로([[02-foundations/basic-circuits-electronics|0.6.2]]), 칼만 필터([[02-foundations/probability|3. 확률 §5]]), 지연이 루프의 안정성을 어떻게 정하는지([[04-robotics/control-theory-ce397|5. 제어 이론]]과 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]])는 가르치지 않는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 440" font-size="12" style="max-width:100%;height:auto" role="img" aria-label="1 kHz 서보로 도는 장치 P3: 핸들, 이상 샘플러, 영차 홀드, 벽 법칙을 한 줄로 놓고, 그 아래에 핸들 위치와 그 여덟 샘플과 홀드의 계단을 벽과 함께, 엔코더 한 카운트 높이의 격자 위에 그린 그림">
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
  <text x="146.0" y="82.0" fill="currentColor" text-anchor="middle" opacity="0.9">T = 1 ms마다 닫힌다</text>
  <text x="146.0" y="96.0" fill="currentColor" text-anchor="middle" opacity="0.9">f<tspan dy="3" font-size="10">s</tspan><tspan dx="3.3" dy="-3">= 1000 Hz</tspan></text>
  <text x="146.0" y="110.0" fill="currentColor" text-anchor="middle" opacity="0.9">나이퀴스트 500 Hz</text>
  <line x1="167" y1="50" x2="250" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSpk)"/>
  <text x="208.0" y="43.0" fill="currentColor" text-anchor="middle">x[n] = x(nT)</text>
  <rect x="252" y="33" width="64" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="258,60 270,60 270,53 282,53 282,46 294,46 294,40 310,40" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="284.0" y="23.0" fill="currentColor" text-anchor="middle">영차 홀드</text>
  <text x="284.0" y="96.0" fill="currentColor" text-anchor="middle" opacity="0.9">x[n]을 [nT, (n+1)T) 동안 유지,</text>
  <text x="284.0" y="110.0" fill="currentColor" text-anchor="middle" opacity="0.9">그다음 튄다</text>
  <line x1="316" y1="50" x2="410" y2="50" stroke="currentColor" stroke-width="1.6" marker-end="url(#arSpk)"/>
  <text x="362.0" y="43.0" fill="currentColor" text-anchor="middle">유지된 x</text>
  <rect x="412" y="33" width="136" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="480.0" y="47.0" fill="currentColor" text-anchor="middle">벽 법칙</text>
  <text x="480.0" y="61.0" fill="currentColor" text-anchor="middle">F = −k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3">(x − x</tspan><tspan dy="3" font-size="10">w</tspan><tspan dy="-3">)</tspan></text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.18"><line x1="60" y1="306.0" x2="364" y2="306.0"/><line x1="60" y1="262.0" x2="364" y2="262.0"/><line x1="60" y1="218.0" x2="364" y2="218.0"/><line x1="60" y1="174.0" x2="364" y2="174.0"/><line x1="60" y1="130.0" x2="364" y2="130.0"/></g>
  <text x="0" y="0" transform="translate(48 229) rotate(-90)" fill="currentColor" text-anchor="middle" opacity="0.8">위치 x · 격자 한 칸 = 카운트 하나</text>
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
  <text x="374.0" y="338.0" fill="currentColor" opacity="0.8">t (ms)</text>
  <line x1="99.0" y1="370.0" x2="135.0" y2="370.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <line x1="135.0" y1="370.0" x2="99.0" y2="370.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <text x="142.0" y="374.0" fill="currentColor">T = 1 ms: 시계</text>
  <line x1="60" y1="221.3" x2="372" y2="221.3" stroke="currentColor" stroke-width="1.6" stroke-dasharray="7 4"/>
  <text x="378.0" y="225.3" fill="currentColor">x<tspan dy="3" font-size="10">w</tspan><tspan dx="3.3" dy="-3">= 0.030 m</tspan></text>
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
  <text x="185.4" y="281.8" fill="currentColor">x[n]으로 보면 접촉은</text>
  <text x="185.4" y="295.8" fill="currentColor">눈금(5 ms)에서 시작한다.</text>
  <text x="185.4" y="309.8" fill="currentColor" opacity="0.85">참된 교차(4.45 ms)가 아니다</text>
  <line x1="372" y1="131.0" x2="372" y2="173.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <line x1="372" y1="173.0" x2="372" y2="131.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arSpk)"/>
  <text x="380.0" y="140.0" fill="currentColor" opacity="1">Δx = 61.4 μm:</text>
  <text x="380.0" y="154.0" fill="currentColor" opacity="0.9">엔코더 한 카운트</text>
  <text x="380.0" y="172.0" fill="currentColor" opacity="1">k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3">·Δx = 400 × 61.4 μm</tspan></text>
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
  <text x="14.0" y="400.0" fill="currentColor" opacity="1">두 격자가 만나는 곳: Δx/T = 61.4 mm/s이면 눈금마다 새 카운트가 하나 생긴다.</text>
  <text x="14.0" y="414.0" fill="currentColor" opacity="0.95">이 x(t)의 최고 속도는 벽을 지날 때의 30.7 mm/s이므로 한 눈금 걸러 움직임이 없고,</text>
  <text x="14.0" y="428.0" fill="currentColor" opacity="0.95">카운트를 차분해 얻은 속도는 0이었다가 61.4 mm/s로 튄다.</text>
</svg>

$1\,\mathrm{kHz}$ 서보로 도는 장치 **P3**가 이 페이지의 대상에 적은 $x(t)$로 움직인다. 이상 샘플러는 $T=1\,\mathrm{ms}$마다 $x[n]=x(nT)$를 읽고(나이퀴스트 $500\,\mathrm{Hz}$; §2) 영차 홀드(§2)는 그 표본을 평균 $T/2=0.5\,\mathrm{ms}$ 늦은 계단으로 바꾸므로, $x[n]$에 작용하는 벽 법칙은 $x_w=0.030\,\mathrm{m}$의 벽과의 접촉을 참된 교차 시각 $4.45\,\mathrm{ms}$가 아니라 $5\,\mathrm{ms}$ 눈금에서 처음 본다. 흐린 격자는 엔코더 한 카운트 $\Delta x=61.4\,\mu\mathrm{m}$로 벽 힘 $k_w\,\Delta x=0.025\,\mathrm{N}$에 해당하고, 마름모는 표본을 가장 가까운 카운트에 스냅한 값이다. 두 격자는 눈금마다 새 카운트 하나가 생기는 $\Delta x/T=61.4\,\mathrm{mm/s}$에서 만나는데, 이 움직임은 벽을 지날 때 최고 속도 $30.7\,\mathrm{mm/s}$에 이를 뿐이라 한 눈금 걸러 새 카운트가 없고, 카운트를 차분한 속도는 $0$이었다가 $61.4\,\mathrm{mm/s}$로 튄다.

### 1. 신호, 시스템, 합성곱

짧은 물리 사건도 센서와 필터의 응답을 거치며 뒤의 여러 표본에 흔적을 남기므로, 기록된 사건은 결코 사건 그 자체가 아니다. 이 절은 그 퍼짐의 정확한 규칙인 합성곱을 세우고, 선형 시불변 시스템에서는 그것이 유일한 규칙임을 보인다.

- **시스템** $\mathcal{S}$는 입력 수열 $x[n]$을 출력 수열 $y[n] = \mathcal{S}\{x\}[n]$으로 바꾸는 규칙이다.
  $n$은 정수 샘플 번호다(시스템 기호를 $\mathcal{S}$로 두는 것은 $T$를 §2의 샘플 주기로 남겨 두기 위해서다). 시스템이 **두** 성질을 모두 가지면 **LTI**(선형 시불변)라 하고,
  둘은 서로 따로 깨질 수 있다.
- **선형성**은 가법성과 동차성을 함께 뜻한다. 즉 중첩 원리다(비예시까지 담은 완전한 정의는
  [[02-foundations/engineering-math|0.5 §4.5]]). 모든 입력 $x_1, x_2$와 모든 스칼라 $a, b$에 대해
  $$\mathcal{S}\{a x_1[n] + b x_2[n]\} = a\,\mathcal{S}\{x_1[n]\} + b\,\mathcal{S}\{x_2[n]\}$$
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
  시스템이 그것에 하는 일, $h[n] = \mathcal{S}\{\delta\}[n]$이다. 연속 합이라면 $h = [1, 1]$이다.
- **결과.** LTI 시스템은 임펄스 응답 $h$로 완전히 특성화되고, 출력은 입력과 $h$의
  **합성곱**이다:
  $$y[n] = (x * h)[n] = \sum_k x[k]\, h[n-k]$$
  $k$는 모든 입력 샘플을 훑고, $x[k]$는 시각 $k$의 입력, $h[n-k]$는 그 샘플 하나에 대한
  응답을 $k$에서 시작하도록 늦춘 것이다. 그래서 합성곱은 두 수열을 받아 셋째 수열을 돌려주는
  연산이다. 입력 샘플 하나씩으로 배수한, 늦춰진 $h$ 복사본들의 합이다.
- **이것이 어디서 오는가 — 합성곱은 정의가 아니라 강제된 결과다.** 세 줄이면 된다. 첫째,
  어떤 신호든 옮겨진 임펄스의 합이다. 이건 항등식이다: $x[n] = \sum_k x[k]\,\delta[n-k]$.
  이것을 시스템 $\mathcal{S}$에 통과시키고 *선형성*으로 $\mathcal{S}$를 합 안으로 밀어 넣는다:
  $y[n] = \mathcal{S}\{\sum_k x[k]\delta[n-k]\} = \sum_k x[k]\,\mathcal{S}\{\delta[n-k]\}$. 이제 *시불변성*을
  쓴다. $k$에서의 임펄스에 대한 응답은 $0$에서의 응답을 옮긴 것이다 —
  $\mathcal{S}\{\delta[n-k]\} = h[n-k]$. 대입하면 위의 식이 나온다. 그러므로 저 합은 모델링 선택이
  아니다. **시스템이 선형이고 시불변이면 합성곱을 하며, 다른 것을 할 여지가 없다.** 측정
  하나 — 임펄스 응답 — 가 시스템을 완전히 결정하는 이유이고, 주파수 영역 도구 전체가
  존재하는 이유이기도 하다. 대각화할 연산이 합성곱 하나뿐이기 때문이다.
- 계산 예제: $x = [1, 2, 3]$, $h = [1, 1]$(연속 합):
  $y = [1,\ 1{+}2,\ 2{+}3,\ 3] = [1, 3, 5, 3]$ — 뒤집고, 밀고, 곱하고, 누적한다.
  길이: $N_x + N_h - 1$.

<svg viewBox="0 0 560 318" style="max-width:100%;height:auto" role="img" aria-label="합성곱을 뒤집고, 밀고, 곱하고, 누적하기로: x = [1, 2, 3]과 h = [1, 1]에서 n = 0부터 3까지 뒤집은 h가 입력 아래를 한 칸씩 밀려 가며 y = [1, 3, 5, 3]을 만든다">
  <text x="138" y="24" font-size="11" text-anchor="end" font-style="italic" opacity="0.85" fill="currentColor">k</text>
  <text x="172" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">−1</text>
  <text x="216" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">0</text>
  <text x="260" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">1</text>
  <text x="304" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">2</text>
  <text x="348" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">3</text>
  <text x="138" y="51.5" font-size="12" text-anchor="end" fill="currentColor">x[k]</text>
  <rect x="153" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.5"/>
  <text x="172" y="51.5" font-size="12" text-anchor="middle" opacity="0.5" fill="currentColor">0</text>
  <rect x="197" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="51.5" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <rect x="241" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="51.5" font-size="12" text-anchor="middle" fill="currentColor">2</text>
  <rect x="285" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="51.5" font-size="12" text-anchor="middle" fill="currentColor">3</text>
  <rect x="329" y="34" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.5"/>
  <text x="348" y="51.5" font-size="12" text-anchor="middle" opacity="0.5" fill="currentColor">0</text>
  <text x="388" y="51.5" font-size="12" fill="currentColor">h = [h[0], h[1]] = [1, 1]</text>
  <text x="24" y="82" font-size="11" opacity="0.9" fill="currentColor">뒤집은 h를 n마다 한 칸씩 민다</text>
  <text x="388" y="82" font-size="11" opacity="0.9" fill="currentColor">곱하고 더한다</text>
  <text x="138" y="109.5" font-size="12" text-anchor="end" fill="currentColor">n = 0</text>
  <rect x="153" y="92" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="172" y="109.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="197" y="92" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="109.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="109.5" font-size="12" fill="currentColor">1·1 = 1</text>
  <text x="492" y="109.5" font-size="12" font-weight="bold" fill="currentColor">y[0] = 1</text>
  <text x="138" y="153.5" font-size="12" text-anchor="end" fill="currentColor">n = 1</text>
  <rect x="197" y="136" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="153.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="241" y="136" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="153.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="153.5" font-size="12" fill="currentColor">1·1 + 2·1 = 3</text>
  <text x="492" y="153.5" font-size="12" font-weight="bold" fill="currentColor">y[1] = 3</text>
  <text x="138" y="197.5" font-size="12" text-anchor="end" fill="currentColor">n = 2</text>
  <rect x="241" y="180" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="197.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="285" y="180" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="197.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="197.5" font-size="12" fill="currentColor">2·1 + 3·1 = 5</text>
  <text x="492" y="197.5" font-size="12" font-weight="bold" fill="currentColor">y[2] = 5</text>
  <text x="138" y="241.5" font-size="12" text-anchor="end" fill="currentColor">n = 3</text>
  <rect x="285" y="224" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="241.5" font-size="11" text-anchor="middle" fill="currentColor">h[1]</text>
  <rect x="329" y="224" width="38" height="26" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="348" y="241.5" font-size="11" text-anchor="middle" fill="currentColor">h[0]</text>
  <text x="388" y="241.5" font-size="12" fill="currentColor">3·1 = 3</text>
  <text x="492" y="241.5" font-size="12" font-weight="bold" fill="currentColor">y[3] = 3</text>
  <defs><marker id="arCvk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <line x1="172" y1="127" x2="216" y2="127" stroke="currentColor" stroke-width="1.1" opacity="0.7" marker-end="url(#arCvk)"/>
  <line x1="216" y1="171" x2="260" y2="171" stroke="currentColor" stroke-width="1.1" opacity="0.7" marker-end="url(#arCvk)"/>
  <line x1="260" y1="215" x2="304" y2="215" stroke="currentColor" stroke-width="1.1" opacity="0.7" marker-end="url(#arCvk)"/>
  <text x="138" y="287.5" font-size="12" text-anchor="end" font-weight="bold" fill="currentColor">y[n]</text>
  <rect x="197" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="216" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <rect x="241" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="260" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">3</text>
  <rect x="285" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="304" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">5</text>
  <rect x="329" y="270" width="38" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="348" y="287.5" font-size="12" text-anchor="middle" fill="currentColor">3</text>
  <text x="388" y="287.5" font-size="12" fill="currentColor">길이 3 + 2 − 1 = 4</text>
</svg>

계산 예제를 뒤집고, 밀고, 곱하고, 누적하는 과정으로 그렸다. 출력 시각 $n$마다 커널 $h = [1, 1]$을 입력 아래에 거꾸로 놓고 — $h[0]$은 $x[n]$ 아래, $h[1]$은 $x[n-1]$ 아래 — 겹치는 쌍을 곱해 더한다. 네 위치 $n = 0, 1, 2, 3$이 $y = [1, 3, 5, 3]$을 주고, 길이는 $3 + 2 - 1 = 4$다.

- CNN(합성곱 신경망) 층은 이런 $h$들의 *학습된 2D 묶음*(+ 비선형성)이다 — 실제 프레임워크는 커널을
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

예컨대 도구가 벽에 닿는 힘 펄스는 접촉이 급격해도 퍼져 보일 수 있다. **여기서 얻는 독법.** 넓게 측정된 사건이 세계의 성질인지 파이프라인 임펄스 응답인지 묻는다. 직렬 필터가 응답을 함께 바꾸므로 필터 하나의 평가로는 제어기가 겪는 시점을 놓칠 수 있다.

### 2. 샘플링 — 연속과 디지털 사이의 계약

제어기는 신호를 시계 눈금마다 찍어 어떤 분해능으로 반올림한 숫자로만 본다. 눈금 사이와 분해능 아래는 보이지 않는다. 이 절은 그 숫자들이 언제 여전히 신호를 결정하는지(샘플링), 그렇지 못하면 무엇이 잘못되는지(에일리어싱), 디지털 시스템이 그것을 어떻게 다시 신호로 바꾸는지(홀드), 반올림이 얼마나 거친지(양자화)를 정하는 계약이다.

- **샘플링**은 연속시간 신호 $x_c(t)$를 $T_s$초마다 한 번씩 읽는 것이다.
  $x[n] = x_c(nT_s)$이므로 **샘플링 주파수**는 초당 $f_s = 1/T_s$개(Hz)다. 그 절반 $f_s/2$가
  **나이퀴스트 주파수**, 즉 샘플이 모호함 없이 표현할 수 있는 가장 높은 주파수다.
- **나이퀴스트–섀넌 샘플링 정리.** 조건이 둘이다. 신호가 $B$ Hz로 **대역 제한**되어
  있어야 하고($B$ 위 성분이 없음), *그리고* 샘플링 주파수가 그 대역 끝의 두 배인
  **나이퀴스트 율** $2B$보다 커야 한다.
  $$f_s > 2B$$
  그러면 신호는 샘플에서 *완벽히* 복원된다. 샘플링은 스펙트럼 복사본을 $f_s$ 간격으로
  만드는데, 이 조건에서는 복사본끼리 겹치지 않기 때문이다(아래 접힌 상자에서 증명). 예: 20 kHz로 대역 제한된 오디오는
  $f_s > 40$ kHz가 필요하고, 그래서 CD 오디오가 44.1 kHz를 쓴다.

> [!note]- 더 깊이 · Deeper
> **정리가 성립하는 이유 — 네 단계 증명.** 연속시간 푸리에 변환이 필요하다. [[02-foundations/engineering-math|0.5 §7]]의 "거꾸로 돌려 평균하기"를 시간에 대한 적분으로 한 것이다(§3의 주파수 응답은 이것의 수열 판이다):
> $$X_c(f) = \int_{-\infty}^{\infty} x_c(t)\,e^{-j2\pi ft}\,dt, \qquad x_c(t) = \int_{-\infty}^{\infty} X_c(f)\,e^{j2\pi ft}\,df$$
> "$B$로 대역 제한"은 $|f| > B$에서 $X_c(f) = 0$이라는 뜻이다.
> *1단계, 샘플은 접힌 스펙트럼만 본다.* 역변환에 $t = nT_s$를 넣고 주파수 축을 폭 $f_s$의 띠로 자른다. $|f'| \le f_s/2$, $k$는 임의의 정수로 $f = f' + kf_s$라 쓴다. $e^{j2\pi kf_s nT_s} = e^{j2\pi kn} = 1$이므로
> $$x[n] = \int_{-f_s/2}^{f_s/2} \Big(\sum_{k=-\infty}^{\infty} X_c(f' + kf_s)\Big)\,e^{j2\pi f' nT_s}\,df'$$
> 이다. 그래서 샘플은 $f_s$의 모든 배수만큼 옮긴 복사본들의 합을 통해서만 $X_c$에 의존한다. 위에서 말한 "스펙트럼 복사본"이 이것이다.
> *2단계, $f_s > 2B$이면 복사본이 띠를 비켜 간다.* $|f'| \le f_s/2$이고 $k \ne 0$이면 $|f' + kf_s| \ge f_s/2 > B$이므로, 그곳에서는 $k = 0$ 말고 모든 복사본이 0이고 괄호는 $X_c(f')$ 자체다. 그러면 샘플은 그 띠 위에서 $X_c$의 푸리에 급수 계수이고, 계수가 함수를 정한다: $|f| < f_s/2$에서 $X_c(f) = T_s\sum_n x[n]\,e^{-j2\pi fnT_s}$.
> *3단계, 신호를 다시 짓는다.* 그것을 역변환에 되넣는다. 샘플 $n$은 $x[n]\,T_s\int_{-f_s/2}^{f_s/2} e^{j2\pi f(t - nT_s)}\,df$를 보태고, 이 적분은 sinc 펄스가 된다:
> $$x_c(t) = \sum_n x[n]\,\operatorname{sinc}\Big(\frac{t - nT_s}{T_s}\Big), \qquad \operatorname{sinc}(u) = \frac{\sin \pi u}{\pi u}$$
> 각 펄스는 자기 샘플 순간에 1, 다른 모든 샘플 순간에 0이므로, 합은 모든 샘플을 지나며 그 사이를 채운다. 이것이 정리의 "완벽히 복원"이고, 주파수 영역에서는 차단 주파수 $f_s/2$인 이상적 저역 통과 필터(§4)다.
> *4단계, 실패는 곧 에일리어싱이다.* $f_s \le 2B$이면 $k \ne 0$인 어떤 복사본이 띠 안에 들어와 $X_c(f')$에 더해진다. 주파수 $f$의 음이 $f - kf_s$에서 세어지고, 이것이 아래의 에일리어싱 공식이다.
> *수치 확인:* $x_c(t) = \cos(2\pi \cdot 1.3t) + 0.5\sin(2\pi \cdot 2.9t + 0.4)$는 $B = 2.9$ Hz로 대역 제한되어 있고, 이를 $f_s = 10$ Hz로 샘플링한다($2B = 5.8 < 10$). 두 샘플 사이인 $t = 0.53$ s에서 $t$에 가장 가까운 샘플 8,001개로 sinc 합을 내면 참값 $-0.669532$에 대해 $-0.669513$이 나온다. 잘라 낸 합의 오차는 $2 \times 10^{-5}$이고, 샘플을 열 배로 늘리면 오차가 열 배 준다. (샘플 순간, 예컨대 $t = 0.5$ s에서는 sinc 하나만 빼고 모두 0이라 어떤 신호든 그 샘플이 그대로 나오므로, 거기서 한 확인은 아무것도 증명하지 못한다.) 같은 샘플링 주파수의 $7$ Hz 음은 $t = 0.123$ s에서 $-0.680$으로 복원되는데, 이것은 에일리어스인 $3$ Hz 코사인의 값이고 참 $7$ Hz 값은 $+0.642$다.

- **계산: $1\,\mathrm{kHz}$의 장치 P3.** 햅틱 서보는 [[02-foundations/lab-kernel|0.7 Lab Kernel §1]]이 햅틱 벽에 정한 주기 $T=10^{-3}\,\mathrm{s}$로 돌므로 $f_s=1000\,\mathrm{Hz}$, 나이퀴스트는 $500\,\mathrm{Hz}$다. 신경 쓰는 $30\,\mathrm{Hz}$ 아래 접촉은 정리의 한참 안쪽이라 샘플링이 병목이 아니다. 엔코더 한 카운트는 $\Delta x=r_m 2\pi/N=0.010\cdot 2\pi/1024=61.4\,\mu\mathrm{m}$로, 시간 간격 $T_s$가 아니라 공간의 *양자화* 계단이다. 두 계단은 손잡이가 따로다. $N$을 키우면(더 촘촘한 엔코더) 공간 계단 $\Delta x$가, $f_s$를 키우면(더 빠른 시계) 시간 계단 $T$가 줄어든다. *벽은 어느 읽기를 쓰는가?* 그림의 벽 법칙은 정확한 표본 $x[n]$에 작용하고, 그 표본은 $5\,\mathrm{ms}$ 눈금에서 처음 벽 안에 든다. 대신 엔코더 카운트를 넣으면 한 눈금 일찍 켜진다. 벽에 가장 가까운 카운트 선이 벽 안쪽 $4.7\,\mu\mathrm{m}$에 있어서, 벽에서 $13.8\,\mu\mathrm{m}$ 모자란 $4\,\mathrm{ms}$ 표본이 벽 안쪽 $4.7\,\mu\mathrm{m}$로 스냅되기 때문이다. 샘플링은 접촉을 최대 한 눈금 늦게 만들고, 카운트로의 반올림은 접촉을 어느 쪽으로든 최대 반 카운트만큼 옮긴다. 과제는 이 샘플러와 홀드를 네 배 느린 시계에서 다시 그린다.
- **영차 홀드(zero-order hold, ZOH).** 그림의 계단이 그리는 것, 곧 샘플에서 연속 신호로 돌아가는 단계다. 각 샘플을 다음 샘플까지 유지한다:
  $$x_h(t) = x[n] \quad \text{for } nT \le t < (n+1)T$$
  그래서 출력은 조각마다 일정하고, 눈금마다 튀며, 미래 샘플을 쓰지 않는다(인과적이다). DAC(디지털-아날로그 변환기, 숫자를 다시 전압으로 바꾸는 칩)나 서보가 실제로 하는 복원이 이것이고, 아직 도착하지 않은 샘플이 필요한 위의 sinc 합을 대신한다. *왜 평균 $T/2$ 늦는가:* 구간 $n$ 안의 시각 $t$에서 유지되는 값은 $x(nT)$, 곧 $t - nT$초 묵은 측정이고, 그 나이는 $0$에서 $T$까지 고르게 퍼지므로 평균 $T/2$다. 경사 $x = vt$라면 계단은 평균 $T/2$ 늦게 옮긴 경사다. 주파수 응답도 같은 것을 정확히 말한다. 홀드의 임펄스 응답은 폭 $T$의 단위 펄스이고, 그 변환은
  $$H_{\text{zoh}}(f) = \int_0^T e^{-j2\pi ft}\,dt = T\,e^{-j\pi fT}\operatorname{sinc}(fT)$$
  로, 순수한 $T/2$ 지연(위상 $-\pi fT$, 모든 주파수에서 군지연 $T/2$, §4)에 완만한 이득 처짐을 곱한 것이다. P3($T = 1$ ms)에서 $30$ Hz의 위상은 $-5.4°$, 이득은 DC 값 $T$의 $0.9985$배이고, $500$ Hz 나이퀴스트 주파수에서는 $-90°$와 그 $0.637$배다. 스프링 $K$를 렌더링하는 루프에서 안정성을 깎는 것은 이 지연이다. $T/2$ 늦게 느끼는 스프링은 1차 테일러 전개([[02-foundations/engineering-math|0.5 §2]])로 $F = -K\,x(t - T/2) \approx -Kx + K\tfrac{T}{2}\dot x$의 힘을 낸다. 점성 댐퍼의 힘은 $-b\dot x$이므로([[02-foundations/basic-mechanics|0.6.1 기초 역학 §4–§5]]) 덧붙은 항은 $b = -KT/2$인 댐퍼, 곧 *음의* 감쇠다. 운동에서 에너지를 빼는 대신 넣는 것이다. [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]의 햅틱 벽 한계식에 들어 있는 항이 이것이다.
- **에일리어싱**은 조건이 깨질 때 벌어지는 일이다. $f_s/2$ 위의 주파수 $f$ 성분은 샘플에서
  $$f_{alias} = |f - k f_s|$$
  에 나타난다. $k$는 $f/f_s$에 가장 가까운 정수이고, 그래서 $f_{alias}$가 $0$과 $f_s/2$
  사이에 떨어진다. 실제 음과 그 에일리어스는 똑같은 샘플을 만들므로 뒤의 어떤 처리로도 둘을
  가를 수 없다. 카메라 속 바퀴가 거꾸로 돌고, 50 Hz로 샘플링한 60 Hz 진동($k = 1$)은 10 Hz로
  위장하며, 아래 그림에서는 200 Hz로 샘플링한 170 Hz($k = 1$)가 30 Hz가 된다.

<svg viewBox="0 0 560 236" style="max-width:100%;height:auto" role="img" aria-label="에일리어싱: 200 Hz로 샘플링한 170 Hz 진동이 위상이 뒤집힌 30 Hz로 보인다">
  <line x1="56" y1="128" x2="536" y2="128" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="56" y1="186" x2="536" y2="186" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="56" y1="186" x2="56" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="56" y1="82" x2="56" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="56" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">0</text>
  <line x1="122.7" y1="186" x2="122.7" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="122.7" y1="82" x2="122.7" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="122.7" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">5</text>
  <line x1="189.3" y1="186" x2="189.3" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="189.3" y1="82" x2="189.3" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="189.3" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">10</text>
  <line x1="256" y1="186" x2="256" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="256" y1="82" x2="256" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="256" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">15</text>
  <line x1="322.7" y1="186" x2="322.7" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="322.7" y1="82" x2="322.7" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="322.7" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">20</text>
  <line x1="389.3" y1="186" x2="389.3" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="389.3" y1="82" x2="389.3" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="389.3" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">25</text>
  <line x1="456" y1="186" x2="456" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="456" y1="82" x2="456" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="456" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">30</text>
  <line x1="522.7" y1="186" x2="522.7" y2="190" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="522.7" y1="82" x2="522.7" y2="186" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"/>
  <text x="522.7" y="203" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">35</text>
  <text x="536" y="219" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">t (ms)</text>
  <text x="48" y="132" font-size="12" text-anchor="end" font-style="italic" fill="currentColor">x</text>
  <path d="M56 128L56.5 126.3L57.1 124.6L57.6 122.9L58.1 121.2L58.7 119.5L59.2 117.9L59.7 116.2L60.3 114.6L60.8 113L61.3 111.4L61.9 109.9L62.4 108.4L62.9 106.9L63.5 105.5L64 104.1L64.5 102.7L65.1 101.4L65.6 100.2L66.1 99L66.7 97.8L67.2 96.7L67.7 95.7L68.3 94.7L68.8 93.8L69.3 92.9L69.9 92.2L70.4 91.4L70.9 90.8L71.5 90.2L72 89.7L72.5 89.2L73.1 88.8L73.6 88.5L74.1 88.3L74.7 88.1L75.2 88L75.7 88L76.3 88.1L76.8 88.2L77.3 88.4L77.9 88.7L78.4 89L78.9 89.4L79.5 89.9L80 90.5L80.5 91.1L81.1 91.8L81.6 92.5L82.1 93.3L82.7 94.2L83.2 95.2L83.7 96.2L84.3 97.2L84.8 98.4L85.3 99.5L85.9 100.8L86.4 102L86.9 103.4L87.5 104.7L88 106.1L88.5 107.6L89.1 109.1L89.6 110.6L90.1 112.2L90.7 113.7L91.2 115.4L91.7 117L92.3 118.6L92.8 120.3L93.3 122L93.9 123.7L94.4 125.4L94.9 127.1L95.5 128.8L96 130.5L96.5 132.2L97.1 133.9L97.6 135.6L98.1 137.3L98.7 138.9L99.2 140.6L99.7 142.2L100.3 143.7L100.8 145.3L101.3 146.8L101.9 148.3L102.4 149.8L102.9 151.2L103.5 152.6L104 153.9L104.5 155.2L105.1 156.4L105.6 157.6L106.1 158.7L106.7 159.8L107.2 160.8L107.7 161.7L108.3 162.6L108.8 163.4L109.3 164.2L109.9 164.9L110.4 165.5L110.9 166.1L111.5 166.6L112 167L112.5 167.3L113.1 167.6L113.6 167.8L114.1 167.9L114.7 168L115.2 168L115.7 167.9L116.3 167.7L116.8 167.5L117.3 167.2L117.9 166.8L118.4 166.4L118.9 165.9L119.5 165.3L120 164.6L120.5 163.9L121.1 163.1L121.6 162.2L122.1 161.3L122.7 160.4L123.2 159.3L123.7 158.2L124.3 157.1L124.8 155.9L125.3 154.6L125.9 153.3L126.4 152L126.9 150.6L127.5 149.2L128 147.7L128.5 146.2L129.1 144.7L129.6 143.1L130.1 141.5L130.7 139.9L131.2 138.2L131.7 136.6L132.3 134.9L132.8 133.2L133.3 131.5L133.9 129.8L134.4 128.1L134.9 126.4L135.5 124.7L136 123L136.5 121.3L137.1 119.6L137.6 118L138.1 116.3L138.7 114.7L139.2 113.1L139.7 111.5L140.3 110L140.8 108.5L141.3 107L141.9 105.6L142.4 104.2L142.9 102.8L143.5 101.5L144 100.3L144.5 99L145.1 97.9L145.6 96.8L146.1 95.8L146.7 94.8L147.2 93.9L147.7 93L148.3 92.2L148.8 91.5L149.3 90.8L149.9 90.2L150.4 89.7L150.9 89.2L151.5 88.8L152 88.5L152.5 88.3L153.1 88.1L153.6 88L154.1 88L154.7 88.1L155.2 88.2L155.7 88.4L156.3 88.6L156.8 89L157.3 89.4L157.9 89.9L158.4 90.4L158.9 91L159.5 91.7L160 92.5L160.5 93.3L161.1 94.2L161.6 95.1L162.1 96.1L162.7 97.2L163.2 98.3L163.7 99.5L164.3 100.7L164.8 102L165.3 103.3L165.9 104.7L166.4 106.1L166.9 107.5L167.5 109L168 110.5L168.5 112.1L169.1 113.6L169.6 115.3L170.1 116.9L170.7 118.5L171.2 120.2L171.7 121.9L172.3 123.6L172.8 125.3L173.3 127L173.9 128.7L174.4 130.4L174.9 132.1L175.5 133.8L176 135.5L176.5 137.2L177.1 138.8L177.6 140.5L178.1 142.1L178.7 143.7L179.2 145.2L179.7 146.7L180.3 148.2L180.8 149.7L181.3 151.1L181.9 152.5L182.4 153.8L182.9 155.1L183.5 156.3L184 157.5L184.5 158.6L185.1 159.7L185.6 160.7L186.1 161.7L186.7 162.6L187.2 163.4L187.7 164.2L188.3 164.8L188.8 165.5L189.3 166L189.9 166.5L190.4 167L190.9 167.3L191.5 167.6L192 167.8L192.5 167.9L193.1 168L193.6 168L194.1 167.9L194.7 167.7L195.2 167.5L195.7 167.2L196.3 166.8L196.8 166.4L197.3 165.9L197.9 165.3L198.4 164.7L198.9 163.9L199.5 163.1L200 162.3L200.5 161.4L201.1 160.4L201.6 159.4L202.1 158.3L202.7 157.2L203.2 156L203.7 154.7L204.3 153.4L204.8 152.1L205.3 150.7L205.9 149.3L206.4 147.8L206.9 146.3L207.5 144.8L208 143.2L208.5 141.6L209.1 140L209.6 138.3L210.1 136.7L210.7 135L211.2 133.3L211.7 131.6L212.3 129.9L212.8 128.2L213.3 126.5L213.9 124.8L214.4 123.1L214.9 121.4L215.5 119.7L216 118.1L216.5 116.4L217.1 114.8L217.6 113.2L218.1 111.6L218.7 110.1L219.2 108.6L219.7 107.1L220.3 105.6L220.8 104.2L221.3 102.9L221.9 101.6L222.4 100.3L222.9 99.1L223.5 98L224 96.9L224.5 95.8L225.1 94.8L225.6 93.9L226.1 93L226.7 92.2L227.2 91.5L227.7 90.8L228.3 90.2L228.8 89.7L229.3 89.3L229.9 88.9L230.4 88.5L230.9 88.3L231.5 88.1L232 88L232.5 88L233.1 88L233.6 88.2L234.1 88.4L234.7 88.6L235.2 89L235.7 89.4L236.3 89.8L236.8 90.4L237.3 91L237.9 91.7L238.4 92.4L238.9 93.2L239.5 94.1L240 95.1L240.5 96.1L241.1 97.1L241.6 98.2L242.1 99.4L242.7 100.6L243.2 101.9L243.7 103.2L244.3 104.6L244.8 106L245.3 107.4L245.9 108.9L246.4 110.4L246.9 112L247.5 113.6L248 115.2L248.5 116.8L249.1 118.4L249.6 120.1L250.1 121.8L250.7 123.5L251.2 125.2L251.7 126.9L252.3 128.6L252.8 130.3L253.3 132L253.9 133.7L254.4 135.4L254.9 137.1L255.5 138.7L256 140.4L256.5 142L257.1 143.6L257.6 145.1L258.1 146.7L258.7 148.1L259.2 149.6L259.7 151L260.3 152.4L260.8 153.7L261.3 155L261.9 156.2L262.4 157.4L262.9 158.6L263.5 159.6L264 160.7L264.5 161.6L265.1 162.5L265.6 163.3L266.1 164.1L266.7 164.8L267.2 165.4L267.7 166L268.3 166.5L268.8 166.9L269.3 167.3L269.9 167.6L270.4 167.8L270.9 167.9L271.5 168L272 168L272.5 167.9L273.1 167.8L273.6 167.5L274.1 167.2L274.7 166.9L275.2 166.4L275.7 165.9L276.3 165.3L276.8 164.7L277.3 164L277.9 163.2L278.4 162.4L278.9 161.4L279.5 160.5L280 159.5L280.5 158.4L281.1 157.2L281.6 156L282.1 154.8L282.7 153.5L283.2 152.2L283.7 150.8L284.3 149.3L284.8 147.9L285.3 146.4L285.9 144.8L286.4 143.3L286.9 141.7L287.5 140.1L288 138.4L288.5 136.8L289.1 135.1L289.6 133.4L290.1 131.7L290.7 130L291.2 128.3L291.7 126.6L292.3 124.9L292.8 123.2L293.3 121.5L293.9 119.8L294.4 118.1L294.9 116.5L295.5 114.9L296 113.3L296.5 111.7L297.1 110.2L297.6 108.6L298.1 107.2L298.7 105.7L299.2 104.3L299.7 103L300.3 101.7L300.8 100.4L301.3 99.2L301.9 98L302.4 96.9L302.9 95.9L303.5 94.9L304 94L304.5 93.1L305.1 92.3L305.6 91.6L306.1 90.9L306.7 90.3L307.2 89.7L307.7 89.3L308.3 88.9L308.8 88.6L309.3 88.3L309.9 88.1L310.4 88L310.9 88L311.5 88L312 88.2L312.5 88.3L313.1 88.6L313.6 88.9L314.1 89.3L314.7 89.8L315.2 90.3L315.7 91L316.3 91.6L316.8 92.4L317.3 93.2L317.9 94.1L318.4 95L318.9 96L319.5 97.1L320 98.2L320.5 99.3L321.1 100.5L321.6 101.8L322.1 103.1L322.7 104.5L323.2 105.9L323.7 107.3L324.3 108.8L324.8 110.3L325.3 111.9L325.9 113.5L326.4 115.1L326.9 116.7L327.5 118.3L328 120L328.5 121.7L329.1 123.4L329.6 125.1L330.1 126.8L330.7 128.5L331.2 130.2L331.7 131.9L332.3 133.6L332.8 135.3L333.3 137L333.9 138.6L334.4 140.3L334.9 141.9L335.5 143.5L336 145L336.5 146.6L337.1 148.1L337.6 149.5L338.1 150.9L338.7 152.3L339.2 153.7L339.7 154.9L340.3 156.2L340.8 157.4L341.3 158.5L341.9 159.6L342.4 160.6L342.9 161.6L343.5 162.5L344 163.3L344.5 164.1L345.1 164.8L345.6 165.4L346.1 166L346.7 166.5L347.2 166.9L347.7 167.3L348.3 167.6L348.8 167.8L349.3 167.9L349.9 168L350.4 168L350.9 167.9L351.5 167.8L352 167.5L352.5 167.3L353.1 166.9L353.6 166.5L354.1 165.9L354.7 165.4L355.2 164.7L355.7 164L356.3 163.2L356.8 162.4L357.3 161.5L357.9 160.5L358.4 159.5L358.9 158.4L359.5 157.3L360 156.1L360.5 154.9L361.1 153.6L361.6 152.2L362.1 150.9L362.7 149.4L363.2 148L363.7 146.5L364.3 144.9L364.8 143.4L365.3 141.8L365.9 140.2L366.4 138.5L366.9 136.9L367.5 135.2L368 133.5L368.5 131.8L369.1 130.1L369.6 128.4L370.1 126.7L370.7 125L371.2 123.3L371.7 121.6L372.3 119.9L372.8 118.2L373.3 116.6L373.9 115L374.4 113.4L374.9 111.8L375.5 110.2L376 108.7L376.5 107.3L377.1 105.8L377.6 104.4L378.1 103L378.7 101.7L379.2 100.5L379.7 99.3L380.3 98.1L380.8 97L381.3 95.9L381.9 94.9L382.4 94L382.9 93.1L383.5 92.3L384 91.6L384.5 90.9L385.1 90.3L385.6 89.8L386.1 89.3L386.7 88.9L387.2 88.6L387.7 88.3L388.3 88.1L388.8 88L389.3 88L389.9 88L390.4 88.1L390.9 88.3L391.5 88.6L392 88.9L392.5 89.3L393.1 89.8L393.6 90.3L394.1 90.9L394.7 91.6L395.2 92.3L395.7 93.1L396.3 94L396.8 94.9L397.3 95.9L397.9 97L398.4 98.1L398.9 99.3L399.5 100.5L400 101.7L400.5 103L401.1 104.4L401.6 105.8L402.1 107.3L402.7 108.7L403.2 110.2L403.7 111.8L404.3 113.4L404.8 115L405.3 116.6L405.9 118.2L406.4 119.9L406.9 121.6L407.5 123.3L408 125L408.5 126.7L409.1 128.4L409.6 130.1L410.1 131.8L410.7 133.5L411.2 135.2L411.7 136.9L412.3 138.5L412.8 140.2L413.3 141.8L413.9 143.4L414.4 144.9L414.9 146.5L415.5 148L416 149.4L416.5 150.9L417.1 152.2L417.6 153.6L418.1 154.9L418.7 156.1L419.2 157.3L419.7 158.4L420.3 159.5L420.8 160.5L421.3 161.5L421.9 162.4L422.4 163.2L422.9 164L423.5 164.7L424 165.4L424.5 165.9L425.1 166.5L425.6 166.9L426.1 167.3L426.7 167.5L427.2 167.8L427.7 167.9L428.3 168L428.8 168L429.3 167.9L429.9 167.8L430.4 167.6L430.9 167.3L431.5 166.9L432 166.5L432.5 166L433.1 165.4L433.6 164.8L434.1 164.1L434.7 163.3L435.2 162.5L435.7 161.6L436.3 160.6L436.8 159.6L437.3 158.5L437.9 157.4L438.4 156.2L438.9 154.9L439.5 153.7L440 152.3L440.5 150.9L441.1 149.5L441.6 148.1L442.1 146.6L442.7 145L443.2 143.5L443.7 141.9L444.3 140.3L444.8 138.6L445.3 137L445.9 135.3L446.4 133.6L446.9 131.9L447.5 130.2L448 128.5L448.5 126.8L449.1 125.1L449.6 123.4L450.1 121.7L450.7 120L451.2 118.3L451.7 116.7L452.3 115.1L452.8 113.5L453.3 111.9L453.9 110.3L454.4 108.8L454.9 107.3L455.5 105.9L456 104.5L456.5 103.1L457.1 101.8L457.6 100.5L458.1 99.3L458.7 98.2L459.2 97.1L459.7 96L460.3 95L460.8 94.1L461.3 93.2L461.9 92.4L462.4 91.6L462.9 91L463.5 90.3L464 89.8L464.5 89.3L465.1 88.9L465.6 88.6L466.1 88.3L466.7 88.2L467.2 88L467.7 88L468.3 88L468.8 88.1L469.3 88.3L469.9 88.6L470.4 88.9L470.9 89.3L471.5 89.7L472 90.3L472.5 90.9L473.1 91.6L473.6 92.3L474.1 93.1L474.7 94L475.2 94.9L475.7 95.9L476.3 96.9L476.8 98L477.3 99.2L477.9 100.4L478.4 101.7L478.9 103L479.5 104.3L480 105.7L480.5 107.2L481.1 108.6L481.6 110.2L482.1 111.7L482.7 113.3L483.2 114.9L483.7 116.5L484.3 118.1L484.8 119.8L485.3 121.5L485.9 123.2L486.4 124.9L486.9 126.6L487.5 128.3L488 130L488.5 131.7L489.1 133.4L489.6 135.1L490.1 136.8L490.7 138.4L491.2 140.1L491.7 141.7L492.3 143.3L492.8 144.8L493.3 146.4L493.9 147.9L494.4 149.3L494.9 150.8L495.5 152.2L496 153.5L496.5 154.8L497.1 156L497.6 157.2L498.1 158.4L498.7 159.5L499.2 160.5L499.7 161.4L500.3 162.4L500.8 163.2L501.3 164L501.9 164.7L502.4 165.3L502.9 165.9L503.5 166.4L504 166.9L504.5 167.2L505.1 167.5L505.6 167.8L506.1 167.9L506.7 168L507.2 168L507.7 167.9L508.3 167.8L508.8 167.6L509.3 167.3L509.9 166.9L510.4 166.5L510.9 166L511.5 165.4L512 164.8L512.5 164.1L513.1 163.3L513.6 162.5L514.1 161.6L514.7 160.7L515.2 159.6L515.7 158.6L516.3 157.4L516.8 156.2L517.3 155L517.9 153.7L518.4 152.4L518.9 151L519.5 149.6L520 148.1L520.5 146.7L521.1 145.1L521.6 143.6L522.1 142L522.7 140.4L523.2 138.7L523.7 137.1L524.3 135.4L524.8 133.7L525.3 132L525.9 130.3L526.4 128.6L526.9 126.9L527.5 125.2L528 123.5L528.5 121.8L529.1 120.1L529.6 118.4L530.1 116.8L530.7 115.2L531.2 113.6L531.7 112L532.3 110.4L532.8 108.9L533.3 107.4L533.9 106L534.4 104.6L534.9 103.2L535.5 101.9L536 100.6" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <path d="M56 128L57.6 128.9L59.2 129.8L60.8 130.7L62.4 131.6L64 132.5L65.6 133.4L67.2 134.3L68.8 135.2L70.4 136.1L72 137L73.6 137.9L75.2 138.7L76.8 139.6L78.4 140.5L80 141.3L81.6 142.2L83.2 143L84.8 143.8L86.4 144.7L88 145.5L89.6 146.3L91.2 147.1L92.8 147.9L94.4 148.7L96 149.4L97.6 150.2L99.2 150.9L100.8 151.7L102.4 152.4L104 153.1L105.6 153.8L107.2 154.5L108.8 155.2L110.4 155.8L112 156.5L113.6 157.1L115.2 157.7L116.8 158.3L118.4 158.9L120 159.5L121.6 160L123.2 160.5L124.8 161.1L126.4 161.6L128 162L129.6 162.5L131.2 163L132.8 163.4L134.4 163.8L136 164.2L137.6 164.6L139.2 164.9L140.8 165.3L142.4 165.6L144 165.9L145.6 166.2L147.2 166.4L148.8 166.7L150.4 166.9L152 167.1L153.6 167.3L155.2 167.4L156.8 167.6L158.4 167.7L160 167.8L161.6 167.9L163.2 167.9L164.8 168L166.4 168L168 168L169.6 168L171.2 167.9L172.8 167.9L174.4 167.8L176 167.7L177.6 167.6L179.2 167.4L180.8 167.3L182.4 167.1L184 166.9L185.6 166.6L187.2 166.4L188.8 166.1L190.4 165.9L192 165.5L193.6 165.2L195.2 164.9L196.8 164.5L198.4 164.2L200 163.8L201.6 163.3L203.2 162.9L204.8 162.5L206.4 162L208 161.5L209.6 161L211.2 160.5L212.8 159.9L214.4 159.4L216 158.8L217.6 158.2L219.2 157.6L220.8 157L222.4 156.4L224 155.7L225.6 155.1L227.2 154.4L228.8 153.7L230.4 153L232 152.3L233.6 151.6L235.2 150.9L236.8 150.1L238.4 149.3L240 148.6L241.6 147.8L243.2 147L244.8 146.2L246.4 145.4L248 144.6L249.6 143.7L251.2 142.9L252.8 142.1L254.4 141.2L256 140.4L257.6 139.5L259.2 138.6L260.8 137.8L262.4 136.9L264 136L265.6 135.1L267.2 134.2L268.8 133.3L270.4 132.4L272 131.5L273.6 130.6L275.2 129.7L276.8 128.8L278.4 127.9L280 127L281.6 126.1L283.2 125.2L284.8 124.3L286.4 123.4L288 122.5L289.6 121.6L291.2 120.7L292.8 119.8L294.4 118.9L296 118.1L297.6 117.2L299.2 116.3L300.8 115.4L302.4 114.6L304 113.7L305.6 112.9L307.2 112.1L308.8 111.2L310.4 110.4L312 109.6L313.6 108.8L315.2 108L316.8 107.3L318.4 106.5L320 105.7L321.6 105L323.2 104.2L324.8 103.5L326.4 102.8L328 102.1L329.6 101.4L331.2 100.8L332.8 100.1L334.4 99.5L336 98.8L337.6 98.2L339.2 97.6L340.8 97.1L342.4 96.5L344 95.9L345.6 95.4L347.2 94.9L348.8 94.4L350.4 93.9L352 93.4L353.6 93L355.2 92.6L356.8 92.2L358.4 91.8L360 91.4L361.6 91L363.2 90.7L364.8 90.4L366.4 90.1L368 89.8L369.6 89.5L371.2 89.3L372.8 89.1L374.4 88.9L376 88.7L377.6 88.5L379.2 88.4L380.8 88.3L382.4 88.2L384 88.1L385.6 88.1L387.2 88L388.8 88L390.4 88L392 88L393.6 88.1L395.2 88.1L396.8 88.2L398.4 88.3L400 88.5L401.6 88.6L403.2 88.8L404.8 89L406.4 89.2L408 89.4L409.6 89.6L411.2 89.9L412.8 90.2L414.4 90.5L416 90.8L417.6 91.2L419.2 91.5L420.8 91.9L422.4 92.3L424 92.7L425.6 93.1L427.2 93.6L428.8 94.1L430.4 94.6L432 95.1L433.6 95.6L435.2 96.1L436.8 96.7L438.4 97.2L440 97.8L441.6 98.4L443.2 99L444.8 99.7L446.4 100.3L448 101L449.6 101.7L451.2 102.3L452.8 103L454.4 103.8L456 104.5L457.6 105.2L459.2 106L460.8 106.7L462.4 107.5L464 108.3L465.6 109.1L467.2 109.9L468.8 110.7L470.4 111.5L472 112.3L473.6 113.2L475.2 114L476.8 114.9L478.4 115.7L480 116.6L481.6 117.5L483.2 118.3L484.8 119.2L486.4 120.1L488 121L489.6 121.9L491.2 122.8L492.8 123.7L494.4 124.6L496 125.5L497.6 126.4L499.2 127.3L500.8 128.2L502.4 129.1L504 130L505.6 130.9L507.2 131.8L508.8 132.7L510.4 133.6L512 134.5L513.6 135.4L515.2 136.3L516.8 137.2L518.4 138L520 138.9L521.6 139.8L523.2 140.6L524.8 141.5L526.4 142.4L528 143.2L529.6 144L531.2 144.8L532.8 145.7L534.4 146.5L536 147.3" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <g fill="currentColor"><circle cx="56" cy="128" r="3.4"/><circle cx="122.7" cy="160.4" r="3.4"/><circle cx="189.3" cy="166" r="3.4"/><circle cx="256" cy="140.4" r="3.4"/><circle cx="322.7" cy="104.5" r="3.4"/><circle cx="389.3" cy="88" r="3.4"/><circle cx="456" cy="104.5" r="3.4"/><circle cx="522.7" cy="140.4" r="3.4"/></g>
  <line x1="56" y1="18" x2="78" y2="18" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text x="84" y="22" font-size="11" fill="currentColor">실제 진동, 170 Hz</text>
  <circle cx="304" cy="18" r="3.4" fill="currentColor"/>
  <text x="314" y="22" font-size="11" fill="currentColor">샘플, 5 ms마다 (f<tspan dy="3" font-size="10">s</tspan><tspan dx="3.1" dy="-3">= 200 Hz)</tspan></text>
  <line x1="56" y1="38" x2="78" y2="38" stroke="currentColor" stroke-width="2.2"/>
  <text x="84" y="42" font-size="11" fill="currentColor">샘플이 보여 주는 것: 30 Hz, 위상 반전 (−sin 2π·30t)</text>
</svg>

$5\,\mathrm{ms}$마다($f_s = 200\,\mathrm{Hz}$, 점) 샘플링한 $170\,\mathrm{Hz}$ 진동(가는 선)은 $30\,\mathrm{Hz}$ 음(굵은 선)과 똑같은 샘플을 준다. $170 - 200 = -30$이기 때문이고, 그래서 유령은 위상이 뒤집힌 $30\,\mathrm{Hz}$ 음 $-\sin(2\pi \cdot 30t)$다. 여덟 점으로 계산하는 어떤 것도 둘을 가르지 못하므로, 거르는 일은 샘플러 앞에서 해야 한다.

- 따라서: **다운샘플링 전 안티에일리어스 필터**, 항상 (소프트웨어에서 IMU 로그를 솎아낼
  때도 포함). 안티에일리어스 필터는 샘플러나 데시메이터 앞에 두는 저역통과 필터(§4)로,
  *새* $f_s/2$ 위의 성분을 없애 접혀 내려올 것을 남기지 않는다. P6의 로드셀에서는 아날로그 필터가 RC 단
  하나이고 그 $12$비트 ADC에 맞춰 크기를 정한다. RC 저역통과, ADC, 그리고 필터 차단 주파수와 여전히 접혀 내려오는 성분 사이의 맞바꿈은 [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자 §5, §10, §12]]에 있다.
- 공학적 따름정리: *관측해야 할* 가장 빠른 동역학에서 여유를 두고 센서 주기를 정하라 —
  10 Hz 인식 루프는 50 Hz 진동을 감쇠는커녕 보지도 못한다.
- **양자화**는 각 샘플을 $2^N$개 준위 중 하나로 반올림한다. $N$은 ADC(아날로그-디지털
  변환기)의 비트 수다(위 엔코더의 한 바퀴 카운트 수와는 다른 $N$이다). 입력 범위가 $R$이면 한 칸은 $\Delta = R/2^N$이고, 반올림 오차는
  $[-\Delta/2, \Delta/2]$ 위의 균일 잡음처럼 행동하며 그 분산은 $\Delta^2/12$다. 그래서
  유한 비트는 거의 균일한 노이즈를 더한다 — 대략 **비트당 6 dB의 SNR**. *SNR*은
  신호 대 잡음비(신호 전력 ÷ 잡음 전력)이고, *dB*(데시벨)는 그것을 표기하는 로그 척도로
  +6 dB가 진폭 약 2배다. 즉 ADC의 비트 하나가 늘 때마다 양자화 잡음의 RMS가 절반, 전력은 4분의 1이 되고, 그 4배가 6 dB다.
  최대 진폭 사인파에 대한 표준 공식은
  $$\text{SNR}_{dB} = 10\log_{10}\frac{P_{signal}}{P_{noise}} \approx 6.02\,N + 1.76$$
  이다. $P_{signal}$과 $P_{noise}$는 두 전력, $6.02 = 10\log_{10}4$는 비트당 이득이고,
  $1.76$ dB는 사인파 전력과 잡음 $\Delta^2/12$의 비에서 나온다. 12비트 ADC는 약 $74$ dB,
  16비트는 약 $98$ dB다. 10 V를 덮는 12비트 변환기의 한 칸은 $2.44$ mV, 양자화 잡음 RMS는
  $0.70$ mV다. 디지털화의 나머지 절반이 이것이다. 양자화된 센서의 오차가 정말 백색인 조건과, 대신 고정된 바이어스가 되는 경우(정지한 엔코더)는 [[04-robotics/sensor-models|3.2 센서 모델과 잡음 §4]]에 있다. 숫자를 정해진 소수 자릿수로 찍을 때도 같은 반올림이 일어나고, 로그 파일은 그렇게 시각 열을 조용히 양자화한다([[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식 §2]]).
- 이 계약이 안정성 문제로 바뀌는 자리: 가상 벽을 렌더링하는 햅틱 루프는 사람 손을 상대로
  매 밀리초 닫혀야 하고, 거기서 샘플링과 양자화는 정확도 문제이기를 그치고 장치가 떨지
  말지를 정하는 요인이 된다
  ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]).

### 3. 주파수 영역 — 대각화하는 기저

시간 위에서 비슷해 보이는 두 변동이 정반대의 처리를 요구할 수 있다. 좁은 기계 진동 피크와 넓은 접촉 과도응답은 시간상 겹쳐도 차지하는 주파수가 다르고, 걸러 내야 할 것은 그중 하나뿐이다. 이 절은 그런 신호가 갈라져 보이는 주파수 관점을 세우고, 그것이 왜 모든 LTI 시스템을 단순하게 만드는지 보인다.

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
- **DFT**(이산 푸리에 변환)는 샘플 $N$개(여기서 $N$은 블록 길이다) $x[0], \ldots, x[N-1]$의 블록을 복소 계수 $N$개로
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

그런 기계 진동 피크를 없애면 도움이 되지만, 무차별 평활은 접촉 신호까지 지울 수 있다. **여기서 얻는 독법.** 피크를 운용 조건과 연결하고 윈도·샘플링 정보를 보존한다. 유한 구간 스펙트럼의 피크는 조사할 증거이지 물리 원인의 자동 식별은 아니다.

### 4. 필터링 — 설계 기초

모든 센서 신호에는 제어기가 반응하면 안 되는 잡음이 실려 있고, 그것을 없애는 데는 값이 든다. 매끄럽게 하는 필터는 늦게도 만든다. 이 절은 필터 종류에 이름을 붙이고, 두 계열(FIR과 IIR)을 각각이 지연으로 치르는 값과 함께 세우고, 그 지연을 샘플 단위로 잰다. §6이 P3에서 밀리초로 바꾸는 숫자가 그것이다.

- **필터 종류는 통과시키는 주파수로 이름 붙는다.** 차단 주파수가 $f_c$일 때 이상적인
  **저역통과** 필터는 $|f| < f_c$에서 $|H(f)| = 1$, 그 위에서 $|H(f)| = 0$이다.
  **고역통과** 필터는 그 반대, **대역통과** 필터는 한 대역만 남기고, **노치** 필터는 주파수
  $f_0$ 주변의 좁은 대역 하나를 없앤다. 실제 필터는 날카로운 경계 대신 전이 대역을 가진다.
  선택: 센서 노이즈엔 저역통과, 드리프트 제거엔 고역통과, 알려진 진동 고조파엔 노치,
  IMU 융합엔 상보 필터(가속도 저역 + 자이로 고역).
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
- **위상 지연과 군지연**은 필터 출력이 얼마나 늦는지를 말한다. 위상 응답은 $\angle H(f)$다(§3).
  **군지연**은 그 기울기에 음수를 붙인 것으로, 샘플 단위로 잰다.
  $$\tau_g(f) = -\frac{1}{2\pi}\,\frac{d\,\angle H(f)}{df}$$
  그래서 위상이 주파수에 따라 선형으로 떨어지는 필터는 모든 주파수를 같은 샘플 수만큼 늦추고
  파형 모양을 지킨다. 대칭 5탭 이동 평균은 통과대역에서 $\angle H(f) = -4\pi f$이므로 어디서나
  $\tau_g = 2$ 샘플이다. 다음 항목의 지수 평활기는 선형 위상이 아니다. $\alpha = 0.9$, $f = 0.05$
  cycles/sample에서 이득은 $0.32$, 위상은 $-62.6°$이고, 지연이 주파수마다 달라진다.
- **IIR**(무한 임펄스 응답) 필터: 과거 *출력*도 되먹인다.
  $$y[n] = \sum_{k=0}^{M} b_k\, x[n-k] - \sum_{k=1}^{N} a_k\, y[n-k]$$
  $b_k$는 FIR처럼 입력에 가중치를 주고, $a_k$는 직전 출력 $N$개에 가중치를 준다($N$은 여기서 필터의 차수, 곧 되먹이는 과거 출력의 개수다). 모든
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
  필터링은 *제어기와 싸운다*(지연된 속도 추정이 D항, 곧 속도에 작용하는 제어기의 미분 항을 불안정하게 만든다). 모델 기반
  추정을 선호하는 실전적 이유가 이것이다: 정확한 선형-가우시안 상태공간 모델과 잡음
  공분산 아래에서는 **칼만 필터**([[02-foundations/probability|3. 확률 §5에서 유도]])가 평균제곱
  추정 오차를 최소화한다. 모델이 어긋나면 이 보장은 사라진다.

### 5. 제어로 가는 다리: 변환

피드백 루프 안의 필터는 따로 떼어 판단할 수 없다. 그 지연이 루프의 일부가 되고, 루프가 가라앉을지 커질지는 필터, 플랜트(제어하는 대상 시스템), 제어기가 함께 정하기 때문이다. 변환은 시스템이 주파수마다 무엇을 하는지와 내부 동역학이 어떻게 커지거나 줄어드는지를, 제어가 셋 모두에 쓰는 하나의 언어로 드러내 준다.

- 라플라스 변환(연속, [[02-foundations/engineering-math|0.5 §9]]에 정의) / **Z-변환**(이산)은 푸리에의 일반화: 합성곱 ↦ *전달함수*
  $H(s)$ 또는 $H(z)$와의 곱.
- **Z-변환**은 수열을 복소 변수 $z$의 함수로 바꾼다.
  $$X(z) = \sum_n x[n]\, z^{-n}$$
  그래서 한 샘플 지연이 $z^{-1}$ 곱하기가 된다. 라플라스 변수와는 $z = e^{sT_s}$로 묶이고,
  단위원 $z = e^{j2\pi f}$ 위에서는 §3의 주파수 응답으로 줄어든다. 그 묶음은 샘플링 자체에서 나온다. 연속 모드 $e^{st}$를 $T_s$마다 읽으면 $e^{snT_s} = (e^{sT_s})^n$, 곧 $z = e^{sT_s}$인 이산 모드 $z^n$이 된다. $|e^{sT_s}| = e^{\operatorname{Re}(s)\,T_s}$이므로 좌반평면의 극점($\operatorname{Re}(s) < 0$)은 단위원 안($|z| < 1$)에 떨어지고, 다음 항목의 두 안정성 판정은 좌표만 다른 한 판정이다([[02-foundations/engineering-math|0.5 §8]]). 극점이 $s = -1$인 [[02-foundations/lab-plants|0.6]]의 새는 히터 P4를 $T_s = 0.1\,\mathrm{s}$마다 샘플링하면 $z = e^{-0.1} = 0.905$에 떨어지는데, 그것이 그곳의 샘플링된 모델의 계수다. **전달함수**는 시스템이
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

예컨대 평활 필터는 진동을 줄이면서 접촉 제어 피드백에 지연을 더할 수 있다. **여기서 얻는 독법.** 필터 신호가 더 좋다고 하기 전에 이득과 위상을 함께 본다. 상태 공간 모드와 전달함수 극점도 구분한다. 관측·제어할 수 없는 모드(출력에 전혀 드러나지 않는 모드, 또는 입력이 전혀 들뜨게 하지 못하는 모드; 계수 판정과 함께 [[02-foundations/linear-algebra|1. 선형대수 §5]]에서 정의)는 상쇄로 사라질 수 있어 극점과 고유값의 동일성에는 최소 실현 조건이 필요하다.

### 6. 센서 파이프라인 습관 (현장 검증됨)

종이 위에서는 맞는 파이프라인도 늦거나, 묵었거나, 정작 중요한 사건까지 매끄럽게 지워진 신호를 제어기에 건넬 수 있고, 그 신호를 그린 그림에는 아무것도 드러나지 않는다. 그것을 막는 습관이 셋이다. 저마다 그것이 있는 이유와, 그림의 $1\,\mathrm{kHz}$ P3 루프에서 그것을 건너뛰면 치르는 값을 함께 적는다.

- **원시 데이터로 기록하고 필터링은 나중에; 암묵적 이중 필터링(드라이버 + 내 코드) 금지.** 원시 기록은 나중에 얼마든지 다른 방식으로 다시 거를 수 있지만, 걸러진 기록은 필터가 없앤 것을 이미 버렸고 그 지연은 되돌릴 수 없다. 두 번 거르는 것은 같은 손실의 조용한 판이다. 직렬로 이은 필터의 지연은 더해지기 때문이다. §4의 대칭 5탭 이동 평균 하나가 $(M-1)/2 = 2$ 샘플을 늦추므로, 드라이버에 하나, 제어기에 하나 있으면 P3의 위치가 $2 + 2 = 4$ 샘플 늦어진다. $1\,\mathrm{kHz}$에서 $4\,\mathrm{ms}$이고, 홀드의 평균 지연 $0.5\,\mathrm{ms}$(§2)의 여덟 배다. 벽을 지날 때 핸들의 최고 속도인 $30.7\,\mathrm{mm/s}$에서 그것은 $30.7 \times 4 = 122.8\,\mu\mathrm{m}$, 걸러진 신호가 벽 통과를 보여 주기 전에 벽 안으로 들어간 엔코더 두 카운트다.
- **센서에서 타임스탬프를 찍고, 융합 전에 시계를 동기화(카메라-LiDAR-IMU의 외부 파라미터, 곧 센서끼리의 상대 자세 *그리고* 시간 오프셋).** 측정값은 도착한 순간이 아니라 측정한 순간의 세계를 말하고, 속도 $v$로 움직이는 것의 시간 오차 $\delta$는 위치 오차 $v\delta$가 된다. 그 오차는 흩어짐이 아니라 편향이어서 어떤 잡음 설정도 흡수하지 못한다. P3에서 위치를 엔코더가 잡은 순간이 아니라 한 틱 뒤 제어기가 읽는 순간에 찍으면 $\delta = 1\,\mathrm{ms}$이고, 최고 속도에서 오차는 $30.7\,\mu\mathrm{m}$로 카운트의 절반이다. 기계 사이로 넘어가면 오프셋은 수십 밀리초에 이른다. P6의 카트에서 $70\,\mathrm{ms}$ 늦게 도착한 거리 측정은 $0.5\,\mathrm{m/s}$에서 $3.5\,\mathrm{cm}$ 전의 세계를 말하고, 이는 그 센서 잡음의 3.5배다([[04-robotics/state-estimation-slam|3. 상태 추정]]의 대상 절). 시간 오프셋은 외부 파라미터처럼 보정하는 양이고, 두 센서가 보는 운동의 상관으로 추정한다([[04-robotics/geometric-perception-calibration|3.5 기하 인식 §5]]).
- **필터를 고르기 전에 스펙트럼부터 봐라: 싸울 노이즈의 이름부터 알아내라.** 차단 주파수는 신호가 사는 대역과 잡음이 사는 대역 사이에 놓여야 하고, 그 틈이 어디인지는 스펙트럼만이 보여 준다. P3에서 위치를 차분해 얻은 속도는 $0$과 $61.4\,\mathrm{mm/s}$를 오간다(그림). 두 틱마다 되풀이되는 무늬이므로 나이퀴스트 주파수인 $500\,\mathrm{Hz}$에 있고, 손과 벽의 접촉은 $30\,\mathrm{Hz}$ 아래에 산다(§2). §4의 5탭 평균의 이득은 $|\sin(5\pi f)/(5\sin\pi f)|$로, $f = 0.5$에서 $0.2$, $30\,\mathrm{Hz}$($f = 0.03$)에서 $0.965$다. 그래서 참값 $30.7\,\mathrm{mm/s}$ 둘레의 흔들림을 $\pm30.7$에서 $\pm6.1\,\mathrm{mm/s}$로 줄이면서 접촉 대역은 거의 그대로 통과시키고, 그 값으로 $2\,\mathrm{ms}$의 지연을 치른다. 이 떨림은 무작위 잡음이 아니라 양자화이고, 어떤 평균으로도 고치지 못하는 고장이 있다. 핸들이 기어가듯 움직이면 창 하나가 새 카운트 없이 통째로 지나가, 평균한 속도가 정확히 0이 된다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]).

흔한 경우로, 드라이버가 힘 측정을 이미 평활한 뒤 제어기에서 다시 필터링할 수 있다. 신호는 깨끗해도 접촉 시작이 늦게 도착한다. 원신호와 두 처리 단계를 남겨야 지연을 진단할 수 있다. **여기서 얻는 독법.** 취득에서 결정까지 시계 변환과 모든 처리를 따라간다. 처리 이력이 없는 그림으로는 부드러움이 더 좋은 센싱에서 왔는지 중요한 과도응답을 없애서 생겼는지 알 수 없다.

> [!tip] 더 깊이 · Going deeper
> 이 페이지가 압축한 표준 강의는 Oppenheim·Schafer의 *Discrete-Time Signal Processing*이다. §2가 샘플링 정리를 네 단계로 증명한다. 그 책의 샘플링·DFT 장은 그 증명이 생략한 수렴의 세부와 실제 복원 필터를 더한다.

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

Tier B. [[02-foundations/lab-plants|0.6]]의 **P3**, 곧 이 페이지의 대상인 핸들에서 문항마다 손잡이 하나를 바꾼다. 1번과 2번은 루프를 네 배 느린 $250\,\mathrm{Hz}$($T = 4\,\mathrm{ms}$)로, 3번은 평소의 $1\,\mathrm{kHz}$에서 엔코더를 한 바퀴 $N = 4096$ 카운트로 촘촘하게 한다. 이 페이지 §2. 시뮬레이터 없음.

1. **그리기.** 같은 핸들과 엔코더를 네 배 느린 루프 $250\,\mathrm{Hz}$($T=4\,\mathrm{ms}$)에 둔 위의 그림: 연속 핸들 위치 $x(t)$가 주기 $T$의 이상 샘플러를 지나 영차 홀드로 가는 것을 눈금 여덟 개에 걸쳐 그린다. 벽 $x_w$, 나이퀴스트 주파수, 홀드의 평균 지연, 엔코더 격자를 표시하라. 핸들의 최고 속도 $30.7\,\mathrm{mm/s}$에서 이제 눈금마다 새 카운트가 몇 개 생기고, 위치를 차분한 속도는 무엇을 읽는가?
2. **유도.** $250\,\mathrm{Hz}$ 루프에서: 나이퀴스트 주파수와 정리가 허용하는 최대 대역 $B$, $170\,\mathrm{Hz}$ 모터 진동이 샘플에서 어디에 떨어지는지, 그리고 $1\,\mathrm{kHz}$에서 $-5.4°$였던 영차 홀드의 $30\,\mathrm{Hz}$ 위상. 샘플링만 놓고 보면 $250\,\mathrm{Hz}$는 $30\,\mathrm{Hz}$ 아래 접촉에 여전히 충분한가? 느린 시계는 무엇을 치렀는가?
3. **해석.** $1\,\mathrm{kHz}$로 돌아와 엔코더를 한 바퀴 $N = 4096$ 카운트짜리로 바꾼다. 새 카운트 $\Delta x = r_m\,2\pi/N$, 벽 안의 가장 작은 힘 단위 $k_w\,\Delta x$, 그리고 눈금마다 새 카운트 하나가 생기는 속도를 구하라. 이제 핸들의 최고 속도에서 카운트를 차분한 속도는 무엇을 읽는가? 그림의 두 효과 — 속도 떨림과 홀드의 지연 — 가운데 촘촘한 엔코더가 없앤 것은 무엇인가?

> [!note]- 그리는 법 · How to draw it
> - 신호 경로를 한 줄의 블록으로: $x(t)$를 내는 핸들, $T=4\,\mathrm{ms}$마다 순간적으로 닫히는 스위치로 그린 이상 샘플러(아래에 $f_s=250\,\mathrm{Hz}$와 나이퀴스트 $125\,\mathrm{Hz}$), 수열 $x[n]=x(nT)$, 출력이 계단인 상자로 그린 영차 홀드, 그리고 벽 법칙이 실제로 보는 유지된 신호.
> - 홀드 아래에는 그 블록이 하는 일 하나: $x[n]$을 $[nT,\ (n+1)T)$ 동안 일정하게 유지하고 그다음 튄다.
> - 그 아래 시간축 하나, 눈금 여덟 개가 들어가도록 약 $32\,\mathrm{ms}$. $x(t)$는 벽을 가로지르며 올라가는 매끄러운 곡선이고, 눈금마다 그 위에 점을 찍는다. 그 점들이 $x[n]$이고, 제어기에게 그 사이는 존재하지 않는다.
> - 같은 축 위의 ZOH 계단, 각 디딤판은 *직전* 점의 높이에서 평평하다. 디딤판 하나에서 곡선과 계단 사이의 조각을 칠하고 이름을 붙인다. 홀드는 평균 $T/2=2\,\mathrm{ms}$ 늦고, 위 그림의 $0.5\,\mathrm{ms}$의 네 배다.
> - 벽 $x_w=0.030\,\mathrm{m}$은 수평 점선으로, 그보다 높은 첫 디딤판에는 동그라미. 접촉은 눈금에서 시작하고, 이제 참된 교차보다 최대 $4\,\mathrm{ms}$ 늦다.
> - 엔코더 한 카운트 간격, 전과 같은 $\Delta x=61.4\,\mu\mathrm{m}$로 흐린 수평 격자선을 긋고 점들을 가장 가까운 선에 스냅한다. 두 스텝은 혼동할 수 없도록 이름을 붙인다. 시간을 따라 시계가 정하는 $T$는 바뀌었고, 공간을 따라 엔코더가 정하는 $\Delta x$는 그대로다.
> - 맨 아래에는 눈금마다 새 카운트 하나가 생기는 속도 $\Delta x/T=15.3\,\mathrm{mm/s}$. 최고 속도 $30.7\,\mathrm{mm/s}$에서 핸들은 눈금마다 $122.8\,\mu\mathrm{m}$, 곧 두 카운트를 움직이므로 교차 근처의 모든 눈금이 움직임을 보고하고, 차분 속도는 위 그림의 $0$, $61.4$ 번갈아 읽기가 아니라 꾸준한 $30.7\,\mathrm{mm/s}$다.

> [!tip]- 정답 · Solutions
> 1. 샘플러 $x[n]=x(nT)$가 $4\,\mathrm{ms}$마다($f_s=250\,\mathrm{Hz}$, 나이퀴스트 $125\,\mathrm{Hz}$) 읽으므로 눈금 여덟 개는 $32\,\mathrm{ms}$에 걸친다. ZOH는 각 값을 $[nT,(n+1)T)$에 유지하고 평균 $T/2=2\,\mathrm{ms}$ 늦어, 위 그림의 $0.5\,\mathrm{ms}$의 네 배다. 접촉은 여전히 눈금에서 시작하고 이제 참된 교차보다 최대 $4\,\mathrm{ms}$ 늦다. 엔코더 격자는 $61.4\,\mu\mathrm{m}$ 그대로지만, 눈금마다 한 카운트는 이제 $\Delta x/T=15.3\,\mathrm{mm/s}$일 뿐이므로 최고 속도 $30.7\,\mathrm{mm/s}$에서는 눈금마다 새 카운트 둘이 보이고, 차분 속도는 $0$과 $61.4\,\mathrm{mm/s}$를 번갈아 읽는 대신 꾸준히 $30.7\,\mathrm{mm/s}$를 읽는다. 느린 시계는 모든 읽기를 네 배 낡게 만드는 값으로 속도 떨림을 없앴다. 시계는 읽기가 얼마나 오래되었는지를, 엔코더는 얼마나 촘촘한지를 정한다. 나이퀴스트 $125\,\mathrm{Hz}$는 여전히 $30\,\mathrm{Hz}$보다 한참 위다.
> 2. $f_s = 250\,\mathrm{Hz}$이므로 나이퀴스트는 $125\,\mathrm{Hz}$이고 정리는 $B < 125\,\mathrm{Hz}$를 허용한다. $170\,\mathrm{Hz}$ 진동은 나이퀴스트 위에 있고, 가장 가까운 $f_s$의 배수가 $250\,\mathrm{Hz}$($k = 1$)이므로 $|170 - 250| = 80\,\mathrm{Hz}$, 곧 대역 안에 떨어진다. 거기서는 뒤의 어떤 처리도 그것을 진짜 $80\,\mathrm{Hz}$ 신호와 가르지 못하므로, 샘플러 앞의 아날로그 안티에일리어스 필터만이 그것을 없앤다. 홀드의 $30\,\mathrm{Hz}$ 위상은 $-\pi fT = -\pi \cdot 30 \cdot 0.004 = -0.377\,\mathrm{rad} = -21.6°$로, 지연이 $T$에 비례해 커지므로 $1\,\mathrm{kHz}$의 $-5.4°$의 네 배다. 샘플링만 놓고 보면 $250\,\mathrm{Hz}$는 여전히 $30\,\mathrm{Hz}$ 접촉 대역을 덮는다. 느린 시계가 치른 값은 $125\,\mathrm{Hz}$ 위의 진동을 대역 안으로 접어 넣는 낮은 나이퀴스트와 네 배의 지연이고, 벽 루프에서는 그 지연이 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]의 안정성 한계가 물리는 값이다.
> 3. $\Delta x = 0.010 \cdot 2\pi/4096 = 15.3\,\mu\mathrm{m}$로 $61.4\,\mu\mathrm{m}$의 4분의 1이고, 가장 작은 힘 단위는 $k_w\,\Delta x = 400 \times 15.3\,\mu\mathrm{m} = 6.1\,\mathrm{mN}$으로 전의 $25\,\mathrm{mN}$보다 작다. 이제 눈금마다 새 카운트 하나는 $\Delta x/T = 15.3\,\mathrm{mm/s}$에서 생기므로, 최고 속도 $30.7\,\mathrm{mm/s}$에서 핸들은 눈금마다 카운트 둘을 지나고, 교차 근처에서 차분 속도는 $0$과 $61.4\,\mathrm{mm/s}$를 오가는 대신 꾸준히 $30.7\,\mathrm{mm/s}$를 읽는다. 촘촘한 엔코더는 떨림을 없앴지만 홀드의 $0.5\,\mathrm{ms}$ 지연은 그대로다. 그 지연은 시계가 정하기 때문이다 — $N$은 공간 계단을, $f_s$는 시간 계단을 줄인다. 1번은 시계를 늦춰 같은 떨림을 없앴고 그 대가로 모든 읽기가 네 배 낡았지만, 촘촘한 엔코더는 지연을 치르지 않고 떨림을 없앤다.

### 로보틱스 다리

샘플링·필터링·지연은 [[04-robotics/robot-systems-deployment|10. 로봇 시스템]]의 타이밍 예산과 [[04-robotics/state-estimation-slam|3. 상태 추정]]의 센서 융합으로 이어진다.

### 출처 · Sources

- A. V. Oppenheim, R. W. Schafer, *Discrete-Time Signal Processing*, 3판, Prentice Hall, 2010 — §1–§5가 압축한 표준 강의: LTI 시스템과 합성곱, 샘플링과 그 증명, DFT, 필터 설계, Z-변환.
- 이 페이지의 수치 예제는 P3의 것까지 모두 명시된 숫자로부터 여기서 직접 계산한 것이며 어느 출처에서 인용한 것이 아니다. 믿지 말고 다시 계산하라.
