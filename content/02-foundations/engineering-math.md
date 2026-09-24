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

*[[02-foundations/overview|0. Overview]] drew the map. This page closes the undergraduate mathematics that map assumes —
derivatives, matrix arithmetic, logs, complex numbers. Most of the other Foundations pages name it as a prerequisite, which is why it comes first.*

The engineering math that pages 1–9 silently assume, self-contained in one place. Each
section says exactly which foundation page uses it. A few machine-learning words turn up here
as examples before any page has taught them — *loss*, *ReLU*, *layer*, *batch*, *softmax*: read
them as labels for now, since [[02-foundations/neural-network-basics|0.8 What a Neural Network Is]]
defines each one (and §10 below defines softmax). If all of this reads easily, go on in the
study order of [[02-foundations/overview|0. Overview]], not straight to 1. Linear Algebra:
[[02-foundations/lab-plants|0.6 Lab Plants]] — *plant* is control's word for the system being
controlled, and that page freezes six small test systems, P1–P6, that every problem set reuses —
and [[02-foundations/lab-kernel|0.7 Lab Kernel]], then the physics floor
([[02-foundations/basic-mechanics|0.6.1]], [[02-foundations/basic-circuits-electronics|0.6.2]],
[[02-foundations/fluid-power|0.6.3]]) where your degree left a gap, then 0.8.

> [!note] Why this matters · 왜 배우는가
> **Where you are:** on the [[physical-ai-map|Physical AI Map]] this page is the mathematics floor under the whole stack of [[07-research-program/index|7. Research Program §5]]: derivatives, matrices and logarithms sit under every layer, and the linear ordinary differential equations (ODEs) and poles of §8–§9 sit directly under manipulation and contact — in "install that panel on the frame", the steps where the robot moves the panel, feels the frame and seats it. **Why:** a contact behaves like a mass on a spring and a damper, so the same push can make it ring or settle; P3, the wiki's one-degree-of-freedom test handle ([[02-foundations/lab-plants|0.6 Lab Plants]]), pushed with $0.4\,\mathrm N$ into its $400\,\mathrm{N/m}$ wall, overshoots by $73\%$ and needs $0.38\,\mathrm s$ to settle at damping ratio $\zeta = 0.10$, yet overshoots $2\%$ and settles in $36\,\mathrm{ms}$ at $\zeta = 0.78$ ([[02-foundations/basic-mechanics|0.6.1 §10]]). §8's $\zeta = c/(2\sqrt{km})$ tells you which before anything touches steel. **Direction:** [[04-robotics/control-theory-ce397|5. Control Theory §2–§5]], [[04-robotics/system-identification|5.5 System Identification §2]] and [[04-robotics/modern-robotics/ch11-robot-control|MR ch.11 §1]] build on §8–§9, [[02-foundations/calculus-backprop|2. Calculus §1]] and [[02-foundations/optimization|4. Optimization §3]] open on §1–§2, and on the dissertation path of [[07-research-program/index|7. Research Program §8]] the page is the ground under block 1, the foundations gate. **Payoff:** you can differentiate and linearize a function, solve and sketch the response of a first-order plant such as the leaky heater P4 ([[02-foundations/lab-plants|0.6]]), read stability off a pole, and test whether a map is linear.

> [!note] First pass · 처음이라면
> A reference, not a narrative, so the first pass is a test followed by targeted reading — about two sessions of 60–90 minutes. **Session 1:** answer the six self-check questions closed-book (about 30 minutes) and read the section behind any you miss. Then read the four parts that are not standard engineering mathematics even for a fluent reader: §1's worked gradient with its contour figure, §4.5 (linearity, the definition every later page reuses), §6's log-sum-exp, and one skim of §10's notation dictionary. **Session 2:** the picture and §8 in full — the time constant, the block diagram and the P4 worked case are new if dynamics is — then the problem set, drawing item 1 before you open *How to draw it*. §9 is a preview of the control track: read it once for its vocabulary, or leave it until [[04-robotics/control-theory-ce397|5. Control Theory]].

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 336" style="max-width:100%;height:auto" role="img" aria-label="Block diagram of the leaky heater P4: command u = 1 enters a summing junction whose output is x-dot, an integrator returns the temperature error x, and x comes back through a unit gain with a minus sign. Inset: the step response with its initial tangent reaching 1 at t = 1 s, and a magnified view where the two Euler points sit above the two exact points.">
  <defs><marker id="emHw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="16,44 109,44" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#emHw)"/>
  <text x="20" y="36" font-size="11" fill="currentColor">u = 1</text>
  <circle cx="122" cy="44" r="12" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="106" y="39" font-size="13" text-anchor="end" fill="currentColor">+</text>
  <text x="116" y="69" font-size="13" text-anchor="end" fill="currentColor">−</text>
  <polyline points="134,44 213,44" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#emHw)"/>
  <text x="174" y="36" font-size="11" text-anchor="middle" fill="currentColor">ẋ = u − x</text>
  <text x="174" y="64" font-size="11" text-anchor="middle" opacity="0.9" fill="currentColor">t = 0, x = 0:</text>
  <text x="174" y="77" font-size="11" text-anchor="middle" opacity="0.9" fill="currentColor">ẋ = 1 per s</text>
  <rect x="214" y="22" width="60" height="44" rx="3" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <text x="244" y="45" font-size="18" text-anchor="middle" fill="currentColor">∫</text>
  <text x="244" y="60" font-size="11" text-anchor="middle" fill="currentColor">1/s</text>
  <polyline points="274,44 548,44" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#emHw)"/>
  <text x="288" y="36" font-size="11" fill="currentColor">x: temperature error, the only state</text>
  <circle cx="500" cy="44" r="2.8" fill="currentColor"/>
  <polyline points="500,44 500,108 303,108" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#emHw)"/>
  <text x="507" y="80" font-size="11" fill="currentColor">x</text>
  <rect x="272" y="96" width="30" height="24" rx="2" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <text x="287" y="112" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <text x="287" y="135" font-size="11" text-anchor="middle" opacity="0.9" fill="currentColor">gain 1 (later 1 + K)</text>
  <polyline points="272,108 122,108 122,57" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#emHw)"/>
  <polyline points="52,310 264,310" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#emHw)"/>
  <polyline points="52,310 52,168" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#emHw)"/>
  <text x="266" y="314" font-size="11" fill="currentColor">t (s)</text>
  <text x="48" y="166" font-size="11" text-anchor="end" fill="currentColor">x</text>
  <polyline points="132,310 132,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="132" y="326" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="212,310 212,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="212" y="326" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <polyline points="52,250 48,250" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="254" font-size="11" text-anchor="end" fill="currentColor">0.5</text>
  <polyline points="52,190 48,190" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="194" font-size="11" text-anchor="end" fill="currentColor">1</text>
  <text x="45" y="324" font-size="11" text-anchor="end" fill="currentColor">0</text>
  <polyline points="52,190 252,190" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <text x="252" y="184" font-size="11" text-anchor="end" opacity="0.9" fill="currentColor">steady value 1</text>
  <polyline points="132,310 132,190" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.7"/>
  <text x="137" y="252" font-size="11" fill="currentColor">τ = 1 s</text>
  <polyline points="52,310 53.7,307.5 55.3,305.1 57,302.7 58.7,300.4 60.3,298.1 62,295.9 63.7,293.7 65.3,291.6 67,289.5 68.7,287.4 70.3,285.4 72,283.5 73.7,281.5 75.3,279.6 77,277.8 78.7,276 80.3,274.2 82,272.5 83.7,270.8 85.3,269.1 87,267.5 88.7,265.9 90.3,264.3 92,262.8 93.7,261.3 95.3,259.8 97,258.4 98.7,257 100.3,255.6 102,254.2 103.7,252.9 105.3,251.6 107,250.3 108.7,249.1 110.3,247.9 112,246.7 113.7,245.5 115.3,244.4 117,243.2 118.7,242.2 120.3,241.1 122,240 123.7,239 125.3,238 127,237 128.7,236 130.3,235.1 132,234.1 133.7,233.2 135.3,232.3 137,231.5 138.7,230.6 140.3,229.8 142,229 143.7,228.2 145.3,227.4 147,226.6 148.7,225.8 150.3,225.1 152,224.4 153.7,223.7 155.3,223 157,222.3 158.7,221.6 160.3,221 162,220.3 163.7,219.7 165.3,219.1 167,218.5 168.7,217.9 170.3,217.3 172,216.8 173.7,216.2 175.3,215.7 177,215.2 178.7,214.6 180.3,214.1 182,213.6 183.7,213.1 185.3,212.7 187,212.2 188.7,211.7 190.3,211.3 192,210.9 193.7,210.4 195.3,210 197,209.6 198.7,209.2 200.3,208.8 202,208.4 203.7,208 205.3,207.7 207,207.3 208.7,206.9 210.3,206.6 212,206.2 213.7,205.9 215.3,205.6 217,205.3 218.7,204.9 220.3,204.6 222,204.3 223.7,204 225.3,203.7 227,203.5 228.7,203.2 230.3,202.9 232,202.6 233.7,202.4 235.3,202.1 237,201.9 238.7,201.6 240.3,201.4 242,201.2 243.7,200.9 245.3,200.7 247,200.5 248.7,200.3 250.3,200.1 252,199.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="52,310 140,178" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <circle cx="132" cy="190" r="2.6" fill="currentColor"/>
  <text x="60" y="206" font-size="11" fill="currentColor">slope 1 /s</text>
  <text x="204" y="227.9" font-size="11" fill="currentColor">x = 1 − e<tspan dy="-5" font-size="10">−t</tspan></text>
  <rect x="58" y="284.6" width="12" height="14.9" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="70,292 330,292" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" stroke-opacity="0.8"/>
  <rect x="330" y="146" width="210" height="164" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>
  <polyline points="365,310 365,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="326" font-size="11" text-anchor="middle" fill="currentColor">0.1</text>
  <polyline points="505,310 505,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="505" y="326" font-size="11" text-anchor="middle" fill="currentColor">0.2</text>
  <text x="540" y="326" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">t (s)</text>
  <polyline points="354,310 357.1,307.3 360.2,304.7 363.3,302 366.4,299.4 369.5,296.7 372.6,294.1 375.7,291.4 378.8,288.8 381.9,286.2 385,283.6 388.1,281 391.2,278.4 394.3,275.8 397.4,273.2 400.5,270.6 403.6,268 406.7,265.4 409.8,262.9 412.9,260.3 416,257.7 419.1,255.2 422.2,252.6 425.3,250.1 428.4,247.6 431.5,245 434.6,242.5 437.7,240 440.8,237.5 443.9,235 447,232.5 450.1,230 453.2,227.5 456.3,225 459.4,222.5 462.5,220 465.6,217.6 468.7,215.1 471.8,212.6 474.9,210.2 478,207.7 481.1,205.3 484.2,202.9 487.3,200.4 490.4,198 493.5,195.6 496.6,193.2 499.7,190.8 502.8,188.4 505.9,186 509,183.6 512.1,181.2 515.2,178.8 518.3,176.4 521.4,174 524.5,171.7 527.6,169.3 530.7,166.9 533.8,164.6 536.9,162.3 540,159.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="348.2,310 521.8,146" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <circle cx="365" cy="294.1" r="2.9" fill="currentColor"/>
  <circle cx="365" cy="300.5" r="2.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="358" y="291.1" font-size="11" text-anchor="end" fill="currentColor">0.10</text>
  <text x="373" y="307.5" font-size="11" fill="currentColor">0.095</text>
  <circle cx="505" cy="175.1" r="2.9" fill="currentColor"/>
  <circle cx="505" cy="186.6" r="2.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="501" y="157.1" font-size="11" text-anchor="end" fill="currentColor">0.19</text>
  <polyline points="501,160.1 503.5,171.7" fill="none" stroke="currentColor" stroke-width="0.8"/>
  <text x="513" y="193.6" font-size="11" fill="currentColor">0.181</text>
  <circle cx="440" cy="280" r="2.9" fill="currentColor"/>
  <text x="449" y="284" font-size="11" fill="currentColor">forward Euler</text>
  <circle cx="440" cy="295" r="2.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="449" y="299" font-size="11" fill="currentColor">exact</text>
</svg>

The plant (in control, the physical system being controlled) **P4** — the wiki's leaky-heater test system, a temperature that slowly follows its heater command ([[02-foundations/lab-plants|0.6 Lab Plants]]) — is the leaky heater $\dot x=-x+u$ of §8, drawn as a block diagram: the command $u=1$ enters a summing junction with $+$ and the fed-back $x$ with $-$, their sum is $\dot x$, and an integrator ($\int$, or $1/s$) returns the temperature error $x$, the only state, which comes back through a unit gain (no disturbance input: $d=0$ here). The inset is the step response from $x=0$: the initial slope is $1$ per second, its tangent reaches the steady value $1$ at the time constant $t=1\,\mathrm{s}$, and the curve $x=1-e^{-t}$ passes below it. In the magnified corner, forward Euler's $0.10$ and $0.19$ sit $0.005$ and $0.009$ above the exact $0.095$ and $0.181$ at $t=0.1$ and $0.2$, because Euler uses the slope at the start of each step, where $1-x$ is largest.

### 1. Derivatives (→ used by 2. Calculus, 4. Optimization)

Every method on the learning and control path — a training step nudging millions of weights to lower a loss, a controller nudging a motor command to shrink an error — asks one question: nudge this input, and how much does the output move? The derivative is the number that answers it, and the gradient is that number for many inputs at once.

- The **derivative** $f'$ is a new function that gives, at each point $x$, the instantaneous
  rate of change of $f$. Definition as sensitivity:
  $$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$$
  — "nudge the input, how much does the output move?" Here $h$ is the size of the nudge, the
  fraction is the slope of the line through $(x, f(x))$ and $(x+h, f(x+h))$, so the limit
  asks whether that slope settles to one value as $h$ shrinks from either side. When it does, $f$ is
  *differentiable* at $x$. Example: $f(x) = x^2$ at $x = 3$ with $h = 0.01$ gives
  $(9.0601 - 9)/0.01 = 6.01$, closing in on $f'(3) = 6$. Non-example: $f(x) = |x|$ at $0$,
  where the slope is $+1$ from the right and $-1$ from the left, so no single limit exists —
  the same kink that ReLU, the function $\max(0, x)$ of 0.8, has at zero.
- The rules you actually use:

| Rule | Formula |
|---|---|
| Power | $(x^n)' = nx^{n-1}$ |
| Product | $(fg)' = f'g + fg'$ |
| **Chain** | $(f(g(x)))' = f'(g(x))\,g'(x)$ — the rule backprop is built on |
| Exp/Log | $(e^x)' = e^x$, $(\ln x)' = 1/x$ |

- **Partial derivative** $\partial f/\partial x_i$: differentiate w.r.t. one variable,
  hold the rest fixed. Written out, with $e_i$ the unit vector along coordinate $i$,
  $$\frac{\partial f}{\partial x_i}(x) = \lim_{h\to 0}\frac{f(x + h\,e_i) - f(x)}{h}$$
  so it is the ordinary derivative along one axis. The **gradient**
  $\nabla f = (\partial f/\partial x_1, \ldots, \partial f/\partial x_n)$ stacks all $n$ of
  them into a vector. It points in the direction of steepest increase, because for a small step
  $\delta$ the change in $f$ is about $\nabla f^\top \delta = \sum_i (\partial f/\partial x_i)\,\delta_i$ —
  each partial derivative times its own nudge, added up (the $^\top$ is §4's transpose) — which
  is largest when $\delta$ lines up with $\nabla f$ — so gradient *descent* steps the opposite way.
- Worked example (the shape of every loss-gradient computation; a *loss* is the single number
  that scores how wrong a model is, [[02-foundations/neural-network-basics|0.8 §3]]):
  $f(x, y) = (xy - 3)^2$ ⇒ $\partial f/\partial x = 2(xy-3)\cdot y$ — outer derivative
  times inner derivative, chain rule in action. **Evaluate at $(x,y) = (2,1)$:** the inner
  part is $xy - 3 = -1$, so $\partial f/\partial x = 2(-1)(1) = -2$ and
  $\partial f/\partial y = 2(-1)(2) = -4$, i.e. $\nabla f = (-2, -4)$. Read the answer: both
  components are negative, so *increasing* either variable lowers the loss — correct, since
  $xy = 2$ is still short of the target $3$. And $|{-4}| > |{-2}|$ says $y$ is the more
  effective knob here, because it is multiplied by the larger $x$. Gradient descent steps
  $-\alpha(-2,-4)$: push both up, push $y$ twice as hard. Every loss-gradient in this wiki is
  this computation with more indices.

<svg viewBox="0 0 560 366" style="max-width:100%;height:auto" role="img" aria-label="Level sets of f = (xy - 3) squared on the square from 0.5 to 3.5: the zero set xy = 3 as a thick hyperbola, and pairs of hyperbolas xy = 2.5 and 3.5 (f = 0.25), 2 and 4 (f = 1), 1 and 5 (f = 4). At A = (2, 1), on the f = 1 curve, the gradient (-2, -4) drawn at a tenth of its length points away from xy = 3, perpendicular to the curve; one step of -0.1 times the gradient moves by (0.2, 0.4) to B = (2.2, 1.4), where f = 0.0064.">
  <defs><marker id="emGr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="60" y="40" width="300" height="300" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
  <polyline points="60,190 61.7,196.5 63.4,202.6 65.1,208.4 66.7,213.8 68.4,218.8 70.1,223.6 71.8,228.2 73.5,232.5 75.2,236.6 76.9,240.4 78.5,244.1 80.2,247.6 81.9,250.9 83.6,254.1 85.3,257.2 87,260.1 88.7,262.9 90.3,265.5 92,268.1 93.7,270.5 95.4,272.9 97.1,275.2 98.8,277.3 100.4,279.4 102.1,281.5 103.8,283.4 105.5,285.3 107.2,287.1 108.9,288.9 110.6,290.6 112.2,292.2 113.9,293.8 115.6,295.3 117.3,296.8 119,298.2 120.7,299.6 122.4,301 124,302.3 125.7,303.6 127.4,304.8 129.1,306 130.8,307.2 132.5,308.3 134.2,309.5 135.8,310.5 137.5,311.6 139.2,312.6 140.9,313.6 142.6,314.6 144.3,315.5 146,316.4 147.6,317.3 149.3,318.2 151,319.1 152.7,319.9 154.4,320.7 156.1,321.5 157.8,322.3 159.4,323.1 161.1,323.8 162.8,324.6 164.5,325.3 166.2,326 167.9,326.7 169.6,327.3 171.2,328 172.9,328.6 174.6,329.2 176.3,329.9 178,330.5 179.7,331.1 181.3,331.6 183,332.2 184.7,332.8 186.4,333.3 188.1,333.8 189.8,334.4 191.5,334.9 193.1,335.4 194.8,335.9 196.5,336.4 198.2,336.9 199.9,337.3 201.6,337.8 203.3,338.3 204.9,338.7 206.6,339.1 208.3,339.6 210,340" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <polyline points="152.9,40 155.2,45.6 157.5,51 159.8,56.3 162.2,61.4 164.5,66.4 166.8,71.2 169.1,75.8 171.5,80.4 173.8,84.8 176.1,89 178.5,93.2 180.8,97.2 183.1,101.2 185.4,105 187.8,108.7 190.1,112.4 192.4,115.9 194.8,119.4 197.1,122.7 199.4,126 201.7,129.2 204.1,132.3 206.4,135.4 208.7,138.4 211,141.3 213.4,144.1 215.7,146.9 218,149.6 220.4,152.3 222.7,154.9 225,157.5 227.3,159.9 229.7,162.4 232,164.8 234.3,167.1 236.6,169.4 239,171.6 241.3,173.8 243.6,176 246,178.1 248.3,180.2 250.6,182.2 252.9,184.2 255.3,186.1 257.6,188.1 259.9,189.9 262.2,191.8 264.6,193.6 266.9,195.4 269.2,197.1 271.6,198.8 273.9,200.5 276.2,202.2 278.5,203.8 280.9,205.4 283.2,207 285.5,208.5 287.8,210 290.2,211.5 292.5,213 294.8,214.5 297.2,215.9 299.5,217.3 301.8,218.7 304.1,220 306.5,221.3 308.8,222.7 311.1,224 313.5,225.2 315.8,226.5 318.1,227.7 320.4,228.9 322.8,230.1 325.1,231.3 327.4,232.5 329.7,233.6 332.1,234.8 334.4,235.9 336.7,237 339.1,238 341.4,239.1 343.7,240.2 346,241.2 348.4,242.2 350.7,243.2 353,244.2 355.3,245.2 357.7,246.2 360,247.1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <polyline points="67.1,40 70.4,59.1 73.7,76.1 77,91.6 80.3,105.5 83.6,118.2 86.9,129.9 90.2,140.6 93.5,150.4 96.8,159.5 100,167.9 103.3,175.7 106.6,183 109.9,189.8 113.2,196.2 116.5,202.2 119.8,207.8 123.1,213.1 126.4,218.1 129.7,222.9 133,227.3 136.2,231.6 139.5,235.6 142.8,239.4 146.1,243.1 149.4,246.5 152.7,249.8 156,253 159.3,256 162.6,258.9 165.9,261.7 169.1,264.3 172.4,266.9 175.7,269.3 179,271.7 182.3,273.9 185.6,276.1 188.9,278.2 192.2,280.2 195.5,282.2 198.8,284 202.1,285.9 205.3,287.6 208.6,289.3 211.9,291 215.2,292.5 218.5,294.1 221.8,295.6 225.1,297 228.4,298.4 231.7,299.8 235,301.1 238.3,302.4 241.5,303.6 244.8,304.8 248.1,306 251.4,307.2 254.7,308.3 258,309.4 261.3,310.4 264.6,311.4 267.9,312.4 271.2,313.4 274.4,314.4 277.7,315.3 281,316.2 284.3,317.1 287.6,318 290.9,318.8 294.2,319.6 297.5,320.4 300.8,321.2 304.1,322 307.4,322.7 310.6,323.5 313.9,324.2 317.2,324.9 320.5,325.6 323.8,326.3 327.1,326.9 330.4,327.6 333.7,328.2 337,328.8 340.3,329.4 343.5,330 346.8,330.6 350.1,331.2 353.4,331.8 356.7,332.3 360,332.9" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
  <polyline points="124.3,40 126.9,47.9 129.6,55.5 132.2,62.8 134.9,69.7 137.5,76.3 140.2,82.7 142.8,88.9 145.5,94.7 148.1,100.4 150.8,105.8 153.4,111.1 156.1,116.2 158.7,121 161.4,125.7 164,130.3 166.7,134.7 169.3,138.9 172,143 174.6,147 177.3,150.8 179.9,154.6 182.6,158.2 185.2,161.7 187.8,165.1 190.5,168.4 193.1,171.6 195.8,174.7 198.4,177.7 201.1,180.7 203.7,183.5 206.4,186.3 209,189 211.7,191.7 214.3,194.2 217,196.7 219.6,199.2 222.3,201.6 224.9,203.9 227.6,206.2 230.2,208.4 232.9,210.5 235.5,212.6 238.2,214.7 240.8,216.7 243.5,218.7 246.1,220.6 248.8,222.5 251.4,224.3 254.1,226.1 256.7,227.9 259.4,229.6 262,231.3 264.7,232.9 267.3,234.5 270,236.1 272.6,237.7 275.2,239.2 277.9,240.7 280.5,242.2 283.2,243.6 285.8,245 288.5,246.4 291.1,247.7 293.8,249 296.4,250.4 299.1,251.6 301.7,252.9 304.4,254.1 307,255.3 309.7,256.5 312.3,257.7 315,258.8 317.6,260 320.3,261.1 322.9,262.2 325.6,263.2 328.2,264.3 330.9,265.3 333.5,266.4 336.2,267.4 338.8,268.4 341.5,269.3 344.1,270.3 346.8,271.2 349.4,272.1 352.1,273.1 354.7,274 357.4,274.8 360,275.7" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
  <polyline points="81.4,40 84.6,54.7 87.7,68.2 90.8,80.7 93.9,92.2 97.1,102.9 100.2,112.9 103.3,122.2 106.5,130.8 109.6,139 112.7,146.6 115.9,153.8 119,160.6 122.1,167 125.2,173.1 128.4,178.8 131.5,184.3 134.6,189.4 137.8,194.3 140.9,199 144,203.5 147.2,207.7 150.3,211.8 153.4,215.7 156.5,219.4 159.7,223 162.8,226.4 165.9,229.7 169.1,232.8 172.2,235.9 175.3,238.8 178.5,241.6 181.6,244.3 184.7,246.9 187.8,249.4 191,251.9 194.1,254.2 197.2,256.5 200.4,258.7 203.5,260.8 206.6,262.9 209.8,264.8 212.9,266.8 216,268.7 219.1,270.5 222.3,272.2 225.4,273.9 228.5,275.6 231.7,277.2 234.8,278.8 237.9,280.3 241.1,281.8 244.2,283.2 247.3,284.7 250.4,286 253.6,287.4 256.7,288.7 259.8,289.9 263,291.2 266.1,292.4 269.2,293.6 272.4,294.7 275.5,295.8 278.6,296.9 281.7,298 284.9,299.1 288,300.1 291.1,301.1 294.3,302.1 297.4,303 300.5,304 303.7,304.9 306.8,305.8 309.9,306.6 313,307.5 316.2,308.3 319.3,309.2 322.4,310 325.6,310.8 328.7,311.6 331.8,312.3 335,313.1 338.1,313.8 341.2,314.5 344.3,315.2 347.5,315.9 350.6,316.6 353.7,317.3 356.9,317.9 360,318.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <polyline points="110,40 112.8,49.6 115.6,58.6 118.4,67.2 121.2,75.4 124,83.1 126.9,90.5 129.7,97.5 132.5,104.2 135.3,110.6 138.1,116.8 140.9,122.6 143.7,128.2 146.5,133.6 149.3,138.8 152.1,143.8 154.9,148.5 157.8,153.1 160.6,157.5 163.4,161.8 166.2,165.9 169,169.9 171.8,173.7 174.6,177.4 177.4,180.9 180.2,184.4 183,187.7 185.8,191 188.7,194.1 191.5,197.1 194.3,200.1 197.1,202.9 199.9,205.7 202.7,208.4 205.5,211 208.3,213.5 211.1,216 213.9,218.4 216.7,220.7 219.6,223 222.4,225.2 225.2,227.3 228,229.4 230.8,231.5 233.6,233.5 236.4,235.4 239.2,237.3 242,239.2 244.8,241 247.6,242.7 250.4,244.4 253.3,246.1 256.1,247.8 258.9,249.4 261.7,250.9 264.5,252.5 267.3,254 270.1,255.4 272.9,256.9 275.7,258.3 278.5,259.7 281.3,261 284.2,262.3 287,263.6 289.8,264.9 292.6,266.1 295.4,267.4 298.2,268.6 301,269.7 303.8,270.9 306.6,272 309.4,273.1 312.2,274.2 315.1,275.3 317.9,276.3 320.7,277.3 323.5,278.4 326.3,279.3 329.1,280.3 331.9,281.3 334.7,282.2 337.5,283.1 340.3,284 343.1,284.9 346,285.8 348.8,286.7 351.6,287.5 354.4,288.4 357.2,289.2 360,290" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <polyline points="95.7,40 98.7,51.7 101.7,62.7 104.6,73 107.6,82.6 110.6,91.7 113.5,100.2 116.5,108.3 119.5,116 122.4,123.2 125.4,130.1 128.4,136.6 131.3,142.8 134.3,148.7 137.3,154.3 140.3,159.7 143.2,164.8 146.2,169.7 149.2,174.4 152.1,178.9 155.1,183.3 158.1,187.4 161,191.4 164,195.2 167,198.9 170,202.4 172.9,205.9 175.9,209.2 178.9,212.3 181.8,215.4 184.8,218.4 187.8,221.2 190.7,224 193.7,226.7 196.7,229.3 199.6,231.8 202.6,234.2 205.6,236.6 208.6,238.9 211.5,241.1 214.5,243.3 217.5,245.4 220.4,247.4 223.4,249.4 226.4,251.4 229.3,253.2 232.3,255.1 235.3,256.8 238.3,258.6 241.2,260.3 244.2,261.9 247.2,263.5 250.1,265.1 253.1,266.6 256.1,268.1 259,269.5 262,271 265,272.3 267.9,273.7 270.9,275 273.9,276.3 276.9,277.6 279.8,278.8 282.8,280 285.8,281.2 288.7,282.4 291.7,283.5 294.7,284.6 297.6,285.7 300.6,286.8 303.6,287.8 306.5,288.8 309.5,289.8 312.5,290.8 315.5,291.8 318.4,292.7 321.4,293.7 324.4,294.6 327.3,295.5 330.3,296.3 333.3,297.2 336.2,298 339.2,298.9 342.2,299.7 345.2,300.5 348.1,301.3 351.1,302 354.1,302.8 357,303.6 360,304.3" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <polyline points="110,340 110,344" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="356" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="56,290 60,290" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="294" font-size="11" text-anchor="end" fill="currentColor">1</text>
  <polyline points="210,340 210,344" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="210" y="356" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <polyline points="56,190 60,190" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="194" font-size="11" text-anchor="end" fill="currentColor">2</text>
  <polyline points="310,340 310,344" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="356" font-size="11" text-anchor="middle" fill="currentColor">3</text>
  <polyline points="56,90 60,90" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="94" font-size="11" text-anchor="end" fill="currentColor">3</text>
  <text x="368" y="344" font-size="11" fill="currentColor">x</text>
  <text x="52" y="44" font-size="11" text-anchor="end" fill="currentColor">y</text>
  <polyline points="210,290 190.2,329.6" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emGr)"/>
  <polyline points="210,290 228.6,252.9" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#emGr)"/>
  <polyline points="213.1,283.7 219.4,286.9 216.3,293.1" fill="none" stroke="currentColor" stroke-width="0.9"/>
  <circle cx="210" cy="290" r="3.2" fill="currentColor"/>
  <circle cx="230" cy="250" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="219" y="310" font-size="12" fill="currentColor">A</text>
  <text x="214" y="242" font-size="12" fill="currentColor">B</text>
  <text x="376" y="44" font-size="12" fill="currentColor">f(x, y) = (xy − 3)<tspan dy="-5" font-size="10">2</tspan></text>
  <polyline points="376,66 402,66" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <text x="408" y="70" font-size="11" fill="currentColor">f = 0: xy = 3</text>
  <polyline points="376,86 402,86" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <text x="408" y="90" font-size="11" fill="currentColor">f = 0.25</text>
  <polyline points="376,106 402,106" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
  <text x="408" y="110" font-size="11" fill="currentColor">f = 1</text>
  <polyline points="376,126 402,126" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <text x="408" y="130" font-size="11" fill="currentColor">f = 4</text>
  <polyline points="376,146 401,146" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emGr)"/>
  <text x="408" y="150" font-size="11" fill="currentColor">∇f at A, drawn ×0.1</text>
  <polyline points="376,166 399,166" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#emGr)"/>
  <text x="408" y="170" font-size="11" fill="currentColor">one step −0.1∇f</text>
  <circle cx="389" cy="186" r="3.2" fill="currentColor"/>
  <text x="408" y="190" font-size="11" fill="currentColor">A (2, 1): f = 1</text>
  <circle cx="389" cy="206" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="408" y="210" font-size="11" fill="currentColor">B (2.2, 1.4): f = 0.0064</text>
</svg>

Level sets of $f(x,y)=(xy-3)^2$ on $[0.5,3.5]^2$: the thick curve is the zero set $xy=3$, and every other level is a pair of hyperbolas $xy=3\pm\sqrt f$. At $A=(2,1)$, on the level $f=1$, the gradient $\nabla f=(-2,-4)$ (drawn at a tenth of its length) is perpendicular to that level curve and points uphill, away from $xy=3$. One gradient-descent step with $\alpha=0.1$ moves against it by $(0.2,\,0.4)$ — $y$ twice as far as $x$ — to $B=(2.2,\,1.4)$, where $f=0.0064$.

### 2. Taylor expansion (→ 2. Calculus, 4. Optimization)

An optimizer never sees a function whole: at each step it knows only the value and a few derivatives where it stands, and must guess what lies one step away. Taylor expansion is that guess, and it also says how far the guess can be trusted.

$$f(x + \delta) \approx f(x) + f'(x)\,\delta + \tfrac12 f''(x)\,\delta^2$$

"Any smooth function is locally a line (1st order) or a parabola (2nd order)."
Gradient descent trusts the line; Newton's method trusts the parabola.

The **Taylor expansion** approximates a function near a point by a polynomial built from its
derivatives *at* that point. In the formula, $x$ is the expansion point, $\delta$ the step away
from it, and $f'(x)$, $f''(x)$ the first and second derivatives there. The approximation is
only local: when $f$ has three continuous derivatives, the error of the second-order version
shrinks like $\delta^3$, so halving the step cuts the error about eightfold. The version with
many variables, which optimization uses, replaces $f'$ by the gradient and $f''$ by the Hessian
matrix $H$ of second derivatives:
$$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12\,\delta^\top H(x)\,\delta$$
where $\delta$ is now a vector and $\delta^\top H \delta$ is the quadratic form read in
[[02-foundations/linear-algebra|1. Linear Algebra §3]].

**Sanity check.** With $f = x^2$ at $x=1$: $f(1+\delta) = 1 + 2\delta + \delta^2$ — exact,
because $x^2$ *is* a parabola.

**Worked example with real numbers** — estimate $\sqrt{4.1}$ without a calculator. Take
$f(x) = \sqrt{x}$ and expand around $x = 4$, where you already know the answer is $2$. You
need two derivatives: $f'(x) = \frac{1}{2\sqrt x}$, so $f'(4) = \frac{1}{4} = 0.25$; and
$f''(x) = -\frac{1}{4x^{3/2}}$, so $f''(4) = -\frac{1}{32} = -0.03125$. With $\delta = 0.1$:

| Order | Computation | Result | Error |
|---|---|---|---|
| 0th | $2$ | 2 | $2.5\times10^{-2}$ |
| 1st | $2 + 0.25(0.1)$ | 2.025 | $1.5\times10^{-4}$ |
| 2nd | $2.025 + \tfrac12(-0.03125)(0.1)^2$ | 2.02484375 | $1.9\times10^{-6}$ |

(True value $\sqrt{4.1} = 2.0248456\ldots$) Each order costs one more derivative and buys
about two more correct decimal digits *for a small step*. That trade is the entire argument
between gradient descent and Newton's method in
[[02-foundations/optimization|4. Optimization §3]]: Newton uses the second derivative to take
a far better step, and pays $O(n^3)$ per step for it — the cost of solving an $n\times n$ linear system (the notation is [[02-foundations/algorithms/complexity-recursion|11.1 §2]]).

**Two first-order expansions worth memorizing**, because papers use them silently:
$e^\delta \approx 1 + \delta$ and $\log(1+\delta) \approx \delta$ for small $\delta$. (Check at
$\delta = 0.01$: $e^{0.01} = 1.01005$, $\log(1.01) = 0.00995$.) Whenever a derivation says
"for small $\epsilon$, this is approximately…", this is what happened.

### 3. Integrals and expectations (→ 3. Probability)

Probability pages average a quantity over every outcome — the expected loss over a dataset, the expected return of a policy, the mean of a noisy range reading — and when the outcomes form a continuum, that average is an integral. This section reads an integral as a sum, then uses it for the one pattern the foundations need, the expectation.

- An integral is a weighted sum **in the continuum limit** — slice the axis into pieces,
  multiply each $f$ value by its slice width, add them up, then let the slice width shrink
  to zero. "Continuum limit" always means exactly that: a sum whose steps have been taken
  all the way down to infinitesimal. That sum is written $\int f(x)\,dx$. As a formula
  (the Riemann sum), over an interval $[a, b]$ cut into $N$ equal slices,
  $$\int_a^b f(x)\,dx = \lim_{N\to\infty} \sum_{i=0}^{N-1} f(x_i)\,\Delta x, \qquad \Delta x = \frac{b-a}{N},\quad x_i = a + i\,\Delta x$$
  where $\Delta x$ is the slice width and $x_i$ the left edge of slice $i$; the limit exists for
  every continuous $f$, so the answer does not depend on how finely you started. Example:
  $\int_0^1 x\,dx$ with $N = 10$ slices gives $0.45$, with $N = 100$ gives $0.495$, with
  $N = 1000$ gives $0.4995$ — creeping to the exact $\tfrac12$.
- The only integral pattern the foundations really use is the **expectation**, the
  probability-weighted average of a quantity $g(X)$ of a random variable $X$. It is a single
  number, computed as a sum when $X$ takes discrete values with probabilities $p(x)$ and as an
  integral when $X$ has a density $p(x)$:
  $$E[g(X)] = \sum_x g(x)\,p(x) \qquad\text{or}\qquad E[g(X)] = \int g(x)\,p(x)\,dx$$
  — "average $g$ over the distribution $p$." Because it is a sum, it is linear,
  $E[aX + bY] = aE[X] + bE[Y]$ (§4.5).
  **Made concrete, three ways:**
  - *Discrete, so "weighted sum" is literal.* A fair die: $E[X] = \sum_x x\,p(x)
    = 1(\tfrac16) + 2(\tfrac16) + \cdots + 6(\tfrac16) = \tfrac{21}{6} = 3.5$. Each value is
    weighted by how often it happens. The integral is this same sum taken to the continuum
    limit.
  - *Continuous, done by hand.* $X$ uniform on $[0,1]$, so $p(x) = 1$ there:
    $E[X] = \int_0^1 x\cdot 1\,dx = \big[\tfrac{x^2}{2}\big]_0^1 = \tfrac12$, and
    $E[X^2] = \int_0^1 x^2\,dx = \tfrac13$. Note $E[X^2] = \tfrac13 \ne (E[X])^2 = \tfrac14$ —
    the gap between them *is* the variance, $\tfrac13 - \tfrac14 = \tfrac{1}{12}$
    ([[02-foundations/probability|3. Probability §2]]).
  - *In code, often a sample mean.* When an expectation is not summed or integrated
    analytically, draw $N$ samples and average,
    $E[g(X)] \approx \frac1N\sum_{i=1}^N g(x_i)$. A finite discrete distribution may be
    summed exactly, and some models permit analytic integration or dynamic programming.
    Many expected losses and returns are nevertheless estimated from samples, so report
    sampling uncertainty ([[02-foundations/ml-practice|9. ML Practice §4]]).
- $\int p(x)\,dx = 1$ (probabilities sum to one) is the identity used in half the proofs
  (e.g., KL non-negativity in [[02-foundations/information-theory|5. Information Theory]]).

### 4. Matrix arithmetic (→ 1. Linear Algebra — its entry requirement)

A robot arm turns joint rates into a tip velocity through a matrix, and a network layer turns 512 features into 10 scores through another; both are a matrix times a vector, and the first thing that breaks in code is a shape that does not match. This section is the arithmetic that 1. Linear Algebra assumes, each rule computed once by hand.

- $(AB)_{ij} = \sum_k A_{ik}B_{kj}$: **row $i$ of $A$ dotted with column $j$ of $B$.** Shapes:
  $(m\times n)(n \times p) = m \times p$ — the inner dimensions must match and then vanish.
- **One entry, computed slowly.** With
  $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $B = \begin{pmatrix}0&1\\1&0\end{pmatrix}$:
  $(AB)_{11}$ is row 1 of $A$, which is $(1, 2)$, dotted with column 1 of $B$, which is
  $(0, 1)$ — so $(AB)_{11} = 1(0) + 2(1) = 2$. Doing the other three the same way:
  $AB = \begin{pmatrix}2&1\\4&3\end{pmatrix}$ — $A$ with its **columns** swapped.
- **Why order matters, seen rather than asserted.** Multiply the other way:
  $BA = \begin{pmatrix}3&4\\1&2\end{pmatrix}$ — $A$ with its **rows** swapped. Same two
  matrices, different answers, and now you can see *why*: multiplying on the right acts on
  columns, multiplying on the left acts on rows. That asymmetry is the reason $W_2W_1x$ and
  $W_1W_2x$ are different networks, and the reason frame order matters in
  [[02-foundations/se3-geometry|SE(3)]] ($R_1R_2 \ne R_2R_1$).
- **Transpose**: flip across the diagonal, $A^\top_{ij} = A_{ji}$. Here
  $A^\top = \begin{pmatrix}1&3\\2&4\end{pmatrix}$. It reverses products,
  $(AB)^\top = B^\top A^\top$: above, $(AB)^\top = \begin{pmatrix}2&4\\1&3\end{pmatrix}$, and
  $B^\top A^\top$ gives the same. The **identity** $I$ has $1$ on the diagonal and $0$
  elsewhere, $I_{ij} = 1$ if $i = j$ and $0$ otherwise, so $AI = IA = A$: it changes nothing.
- **Determinant**: a single number assigned to a square matrix. For a $2\times2$ matrix
  $\begin{pmatrix}a&b\\c&d\end{pmatrix}$ it is $\det A = ad - bc$, and $|\det A|$ is the factor
  by which the map scales area (volume in higher dimensions), with a negative sign meaning the
  orientation is flipped. Our $A$ has $\det A = 1(4) - 2(3) = -2$: it doubles areas and mirrors
  them. The consequence that matters: $\det A \ne 0$ exactly when $A$ is invertible.
- **Inverse, with the numbers.** $A^{-1}$ undoes $A$ from either side,
  $A^{-1}A = AA^{-1} = I$, and exists only for
  square, **full-rank** $A$ (equivalently $\det A \ne 0$). For a $2\times2$,
  $A^{-1} = \frac{1}{\det A}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$ with
  $\det A = ad - bc$. For our $A$: $\det A = 1(4) - 2(3) = -2 \ne 0$, so
  $A^{-1} = -\tfrac12\begin{pmatrix}4&-2\\-3&1\end{pmatrix} = \begin{pmatrix}-2&1\\1.5&-0.5\end{pmatrix}$.
  Check the first entry of $AA^{-1}$: $1(-2) + 2(1.5) = 1$ ✓.
- **What "full rank" rules out, concretely.** Take
  $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$. Its second column is exactly $2\times$ the
  first, so $C$ maps the entire plane onto a single line — every input's information about
  the perpendicular direction is gone. Consistently, $\det C = 1(4) - 2(2) = 0$, and the
  inverse formula divides by zero: **there is nothing to invert back to.** That is rank
  deficiency, and rank gets its proper definition in
  [[02-foundations/linear-algebra|1. Linear Algebra §2]]. Here, read "full rank" as
  "nothing was lost, so it is reversible."
- **A shape check you will do constantly.** A linear layer — one matrix step of a neural
  network, [[02-foundations/neural-network-basics|0.8 §1]] — from 512 features to 10 class
  scores is $y = Wx$ with $x$ a $512\times1$ column, so $W$ must be $10\times512$ and
  $(10\times512)(512\times1) = 10\times1$: one score per class. A batch of 32 samples — inputs pushed
  through together, [[02-foundations/neural-network-basics|0.8 §4]] — stacked as the columns of $X$ ($512\times32$), goes through in one product,
  $(10\times512)(512\times32) = 10\times32$ — one score column per sample. This column
  convention is the one pages 0.8 and 2 use. Reading shapes like this *is* reading an
  architecture ([[02-foundations/linear-algebra|1. Linear Algebra §1]]).
  *Footnote, for code.* Libraries and attention formulas usually store a batch as rows
  instead: $X$ is $32\times512$, the layer's matrix is kept as its transpose ($512\times10$),
  and the output $XW$ is $32\times10$ — the same numbers transposed, by
  $(AB)^\top = B^\top A^\top$ above. The attention projection $Q = XW_Q$ in the collapsed box at the end of
  1. Linear Algebra §1 is written this way.

### 4.5 Linearity: additivity and homogeneity (→ 1. Linear Algebra, 6. Signal Processing, control track)

"Linear" is the most used word in this wiki and has an exact meaning. A map $f$ (a function, a matrix, a system, an operator) is **linear** when it satisfies **two** conditions for all inputs $x, y$ and every scalar $a$:

- **Additivity**: adding the inputs first gives the same result as adding the outputs.
$$f(x + y) = f(x) + f(y)$$
- **Homogeneity** (degree 1): scaling the input scales the output by the same factor.
$$f(a x) = a\,f(x)$$

Together they are the **superposition principle**, written as one line because any weighted sum of inputs can be split term by term:
$$f(a x + b y) = a\,f(x) + b\,f(y)$$
Applying it repeatedly gives $f\big(\sum_k a_k x_k\big) = \sum_k a_k f(x_k)$ for any finite sum, so the response to a complicated input is the sum of the responses to its simple pieces. That one consequence is why linear systems are tractable: measure the response to a few basis inputs and you know the response to everything.

**Why both conditions are listed.** Additivity alone already forces $f(qx) = q f(x)$ for every rational $q$ (apply it to $x + x + \dots$), but not for every real $a$ unless $f$ is also continuous. Stating homogeneity separately closes that gap, which is why textbooks list both.

> [!example] Worked example · 계산 예제
> **A matrix is linear.** For $W = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $x = (1,0)$, $y = (0,1)$, $a = 2$, $b = 3$: $W(2x + 3y) = W(2,3) = (8, 18)$, and $2Wx + 3Wy = 2(1,3) + 3(2,4) = (8, 18)$. Equal, as distributivity of matrix multiplication guarantees for every input.
>
> **$f(x) = 2x + 1$ is not linear**, even though its graph is a straight line. Additivity: $f(1 + 2) = 7$ but $f(1) + f(2) = 3 + 5 = 8$. Homogeneity: $f(2 \cdot 1) = 5$ but $2 f(1) = 6$. The quick test is $f(0)$: every linear map sends $0$ to $0$ (take $a = 0$), and here $f(0) = 1$. A line with an offset is **affine**, not linear.
>
> **$f(x) = x^2$ is not linear**: $f(1 + 1) = 4$ but $f(1) + f(1) = 2$.
>
> **ReLU, $f(x) = \max(0, x)$, is not linear**: $f(-1 + 1) = 0$ but $f(-1) + f(1) = 0 + 1 = 1$. It is homogeneous only for $a \ge 0$, since $f(-1 \cdot 1) = 0 \ne -f(1) = -1$.

**Where the wiki uses it.**
- **Matrices and layers.** Every matrix is a linear map ([[02-foundations/linear-algebra|1. Linear Algebra §1]]). A "linear layer" $Wx + b$ is strictly affine; it is linear only when $b = 0$. Stacked linear maps collapse into one, which is why networks need a nonlinearity between them ([[02-foundations/neural-network-basics|0.8 §1]]).
- **Operators.** Differentiation, integration and expectation are linear: $\frac{d}{dt}(af + bg) = a f' + b g'$ and $E[aX + bY] = aE[X] + bE[Y]$ (§1, §3, [[02-foundations/probability|3. Probability]]).
- **Systems.** A linear time-invariant system is additive and homogeneous in its input signal and also shift-invariant; superposition is exactly what forces its output to be a convolution ([[02-foundations/signal-processing|6. Signal Processing §1]]).
- **Linearization.** A nonlinear $f$ is replaced near an operating point $x_0$ by $f(x_0 + \delta) \approx f(x_0) + f'(x_0)\,\delta$; the map $\delta \mapsto f'(x_0)\,\delta$ is linear in the deviation $\delta$, which is what lets control design work locally (§2, [[04-robotics/control-theory-ce397|5. Control Theory]]).

### 5. Series and the geometric sum (→ 7. RL Basics)

**Why reinforcement learning (RL) cares.** A reward $k$ steps in the future is counted with weight $\gamma^k$, so the
total weight an agent can ever collect is the infinite sum below, which the derivation shows
equals $1/(1-\gamma)$. At $\gamma = 0.99$ that is $100$: the agent behaves roughly as if it were
adding up 100 undiscounted steps and ignoring everything past them. Corroboration from the
other side — $0.99^{100} \approx 0.37$, so by step 100 the weight on a reward has already fallen
to about a third. Hence the phrase "effective horizon ≈ 100 steps" in [[02-foundations/rl-basics|RL]].

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

### 6. Exponentials and logarithms (→ 5. Information Theory — its entry requirement)

The probability of a thousand independent readings is a product of a thousand numbers below one — $10^{-1000}$ if each is $0.1$, which float64 rounds to exactly $0$. Its logarithm, $-2302.6$, is an ordinary number, because the log turns the product into a sum; that is why every likelihood, loss and bit count in the wiki is written with logarithms and their inverse, the exponential.

- $e^x$: the function that is its own derivative; growth at a rate proportional to itself.
  ($e \approx 2.718$.) Precisely, the exponential is the one function with both properties
  $$\frac{d}{dx}e^x = e^x, \qquad e^0 = 1$$
  so growth is proportional to size; the number $e$ is where compound growth ends up, $e = \lim_{n\to\infty}(1 + 1/n)^n$:
  $n = 1$ gives $2$, $n = 10$ gives $2.594$, $n = 100$ gives $2.705$, $n = 1000$ gives $2.717$,
  approaching $2.71828$. Equivalently $e^x = \sum_{k \ge 0} x^k/k!$, which differentiates
  term by term into itself.
- **Which base?** $\ln$ always means base $e$ (the *natural* log — that is what the "n"
  stands for), and $\log_2$ means base 2. A bare $\log$ has no universal meaning: in this
  wiki and in most ML papers it means base $e$, except in information theory, where the
  unit is the **bit** and the base is 2. The good news is that it almost never matters:
  changing base only multiplies everything by a constant (third rule below), and constants
  do not change where a minimum is.
- $\log$ is the inverse of the exponential: $\log(e^x) = x$. For a base $b > 0$, $b \ne 1$,
  $$y = \log_b x \iff b^y = x$$
  so $\log_b x$ is "the power you raise $b$ to in order to get $x$": $\log_2 8 = 3$ since
  $2^3 = 8$. It is defined only for $x > 0$, because no power of a positive base is zero or
  negative; that is why a model that assigns probability $0$ to an observed event gets a
  log-likelihood of $-\infty$. The three rules that carry all
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
- **Log-sum-exp**: $\log \sum_i e^{x_i}$ is everywhere (it is the log of the normalizing
  denominator of softmax, the scores-to-probabilities map defined in §10),
  and computed literally it overflows — $e^{800}$ is already $\infty$ in float64, whose largest
  value is about $1.8\times10^{308}=e^{709.8}$ (how a float stores numbers is
  [[02-foundations/tools/python-research-code|12.3 §5]]). The fix,
  with $x_{max} = \max_i x_i$:

  $$\log \sum_i e^{x_i} = x_{max} + \log\sum_i e^{x_i - x_{max}}$$

  Where it comes from: factor the largest term out of the sum,
  $\sum_i e^{x_i} = e^{x_{max}}\sum_i e^{x_i - x_{max}}$, then take $\log$ and use
  $\log(ab) = \log a + \log b$ from the table above. It is an *exact* identity, not an
  approximation. Why it fixes the problem: every exponent $x_i - x_{max}$ is now $\le 0$,
  so every $e^{(\cdot)}$ is between $0$ and $1$ — nothing can overflow, and the largest term
  is exactly $1$, so this particular sum cannot underflow to all zeros. This stabilizes the
  normalization step; NaNs (not-a-number values) can still arise elsewhere from invalid inputs, extreme arithmetic,
  or unrelated operations. Stable softmax+cross-entropy implementations use this identity
  ([[02-foundations/calculus-backprop|2. Calculus §4]]).

  *With numbers.* For $x = (800, 799)$, computing $e^{800}$ overflows, but the identity gives
  $800 + \log(1 + e^{-1}) = 800.3133$. That also shows what log-sum-exp *is*: a smooth
  maximum, always between $\max_i x_i$ and $\max_i x_i + \log n$ for $n$ entries — here
  between $800$ and $800.693$.

### 7. Complex numbers and Euler's formula (→ 6. Signal Processing — its entry requirement)

A vibration, a filter or a feedback loop is described by what it does to oscillations, and an oscillation carries two numbers at once — how large it is and how far it is shifted in time. A complex number holds that pair as one number and turns "scale and shift" into a single multiplication, which is why signal processing and control are written in them.

- $j = \sqrt{-1}$; a complex number $a + jb$ is a point in the 2D plane, $a$ across and $b$
  up; $|a+jb| = \sqrt{a^2+b^2}$ is its distance from the origin, and its angle is
  $\theta = \operatorname{atan2}(b, a)$. Formally it is a pair of reals, the **real part** $a$
  and the **imaginary part** $b$, with the one extra rule $j^2 = -1$. Addition is
  componentwise; multiplication expands the brackets and uses $j^2 = -1$. The same number in
  **polar form** is
  $$a + jb = r\,e^{j\theta}, \qquad r = \sqrt{a^2 + b^2}, \quad \theta = \operatorname{atan2}(b, a)$$
  where $r$ is the magnitude and $\theta$ the angle (the $e^{j\theta}$ is Euler's formula,
  below). So multiplying two complex numbers multiplies their magnitudes and adds their angles.
  Examples: $3 + 4j$ has $r = 5$ and $\theta = 53.13°$; $(1 + j)^2 = 1 + 2j + j^2 = 2j$, and in
  polar form $1 + j$ has $r = \sqrt2$, $\theta = 45°$, so its square has $r = 2$, $\theta = 90°$,
  which is $2j$ ✓. The **conjugate** $\overline{a + jb} = a - jb$ mirrors the point, and
  $z\bar z = |z|^2$.
- **What atan2 is**: the two-argument arctangent, a function every language ships
  (`atan2(y, x)` in C, Python, NumPy, MATLAB). It takes the two coordinates *separately*
  and returns the angle of the point $(x, y)$ over the full circle, $(-\pi, \pi]$. Written
  out, it corrects $\arctan$ by half a turn whenever the point is on the left:
  $$\operatorname{atan2}(y, x) = \begin{cases} \arctan(y/x) & x > 0 \\ \arctan(y/x) + \pi & x < 0,\ y \ge 0 \\ \arctan(y/x) - \pi & x < 0,\ y < 0 \\ +\pi/2 & x = 0,\ y > 0 \\ -\pi/2 & x = 0,\ y < 0 \end{cases}$$
  so the sign of $x$ decides whether a correction is needed, since $\arctan$ alone only
  returns angles between $-90°$ and $90°$ ($\operatorname{atan2}(0, 0)$ is left undefined).
  For $(x, y) = (-1, -1)$: $\arctan(1) - \pi = 45° - 180° = -135°$.
- **Why not $\arctan(b/a)$**: dividing first throws away information. $\arctan$ only ever
  sees the single number $b/a$, and a point and its exact opposite have the *same* ratio.
  Concretely, $(a,b) = (1,1)$ and $(a,b) = (-1,-1)$ both give $b/a = 1$, so $\arctan$ returns
  $45°$ for both — but the second point is in the third quadrant, at $225°$ (i.e. $-135°$).
  That is what "loses the quadrant" means: the answer is off by exactly $180°$ for half the
  plane, and $\arctan$ has no way to know which half you were in. It also breaks at $a = 0$
  (division by zero) where the true angle is a perfectly ordinary $\pm 90°$. `atan2` keeps
  both signs, so it gets all four quadrants and the vertical axis right. In robotics this is
  the difference between a joint commanded forward and the same joint commanded backward —
  which is why the [[02-foundations/se3-geometry|SE(3)]] page and every inverse-kinematics (IK) implementation use
  atan2 exclusively.

<svg viewBox="0 0 560 200" style="max-width:100%;height:auto" role="img" aria-label="Two opposite points, (1, 1) and (-1, -1), on the same dashed line through the origin, at 45 and 225 degrees. A table beside them: both have b/a = 1, so arctan(b/a) gives 45 degrees for both, wrong for (-1, -1); atan2(b, a) gives 45 and -135 degrees.">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="26" y1="100" x2="234" y2="100"/><line x1="130" y1="16" x2="130" y2="184"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="4 3"><line x1="48" y1="182" x2="212" y2="18"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.7"><path d="M130,100 L183,47"/><path d="M130,100 L77,153"/></g>
  <g fill="currentColor"><circle cx="185" cy="45" r="4.5"/><circle cx="75" cy="155" r="4.5"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.75"><path d="M152,100 A22,22 0 0 0 145.6,84.4"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.55"><path d="M172,100 A42,42 0 1 0 100.3,129.7"/></g>
  <text x="194" y="52" font-size="11" fill="currentColor">(1, 1)</text>
  <text x="18" y="160" font-size="11" fill="currentColor">(−1, −1)</text>
  <text x="152" y="88" font-size="10" fill="currentColor">45°</text>
  <text x="86" y="152" font-size="10" fill="currentColor">225°</text>
  <text x="262" y="70" font-size="11" fill="currentColor">point</text>
  <text x="342" y="70" font-size="11" text-anchor="middle" fill="currentColor">b/a</text>
  <text x="410" y="70" font-size="11" text-anchor="middle" fill="currentColor">arctan(b/a)</text>
  <text x="500" y="70" font-size="11" text-anchor="middle" fill="currentColor">atan2(b, a)</text>
  <polyline points="258,78 540,78" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="262" y="100" font-size="11" fill="currentColor">(1, 1)</text>
  <text x="342" y="100" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <text x="410" y="100" font-size="11" text-anchor="middle" fill="currentColor">45°</text>
  <text x="500" y="100" font-size="11" text-anchor="middle" fill="currentColor">45°</text>
  <text x="262" y="128" font-size="11" fill="currentColor">(−1, −1)</text>
  <text x="342" y="128" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <text x="410" y="128" font-size="11" text-anchor="middle" fill="currentColor">45°, wrong</text>
  <text x="500" y="128" font-size="11" text-anchor="middle" fill="currentColor">−135°</text>
</svg>

Both points lie on the same dashed line through the origin, so $b/a = 1$ for each and $\arctan(b/a)$ returns $45°$ for both — right for $(1, 1)$, wrong by $180°$ for $(-1, -1)$. $\operatorname{atan2}(b, a)$ sees the two signs separately and returns $45°$ and $-135°$, the same direction as $225°$.


- **Euler's formula**: $e^{j\theta} = \cos\theta + j\sin\theta$ — the unit-circle point at
  angle $\theta$. Consequence: multiplying by $e^{j\theta}$ **rotates** by $\theta$, because its
  magnitude is $\sqrt{\cos^2\theta + \sin^2\theta} = 1$ and its angle is $\theta$. Example:
  $e^{j\pi/2} = \cos 90° + j\sin 90° = j$, and multiplying $3 + 4j$ by $j$ gives $-4 + 3j$,
  the same point turned a quarter-turn counter-clockwise.
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

  So the DFT (discrete Fourier transform) formula $X[k] = \sum_n x[n]\,e^{-j2\pi kn/N}$ in
  [[02-foundations/signal-processing|6. Signal Processing]] has no hidden content: the
  $e^{-j(\cdot)}$ is the counter-rotation of step 2, and the $\sum_n$ is the averaging.
  It is one dot product per frequency.

<svg viewBox="0 0 560 424" style="max-width:100%;height:auto" role="img" aria-label="A point e to the j theta on the unit circle at theta = 50 degrees; its shadow on the real axis is a thick horizontal segment from the centre, of length cos theta = 0.643. Below, the shadow plotted against theta, which grows downward from 0 to 360 degrees, traces a cosine whose swing equals the circle's radius, plus and minus 1, and the same thick segment reappears on the wave at 50 degrees.">
  <defs><marker id="emCs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="126,84 294,84" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <polyline points="210,12 210,156" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <circle cx="210" cy="84" r="64" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="210,84 251.1,35" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <path d="M232,84 A22,22 0 0 0 224.1,67.1" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <polyline points="251.1,35 251.1,84" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <polyline points="251.1,86 251.1,203" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity="0.7"/>
  <polyline points="210,84 251.1,84" fill="none" stroke="currentColor" stroke-width="3.4"/>
  <polyline points="210,206 251.1,206" fill="none" stroke="currentColor" stroke-width="3.4"/>
  <polyline points="146,164 146,396" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1 3" stroke-opacity="0.55"/>
  <polyline points="274,164 274,396" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1 3" stroke-opacity="0.55"/>
  <text x="146" y="160" font-size="11" text-anchor="middle" fill="currentColor">−1</text>
  <text x="274" y="160" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="210,170 210,410" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" marker-end="url(#emCs)"/>
  <polyline points="274,176 273.9,177.8 273.6,179.6 273.2,181.4 272.6,183.2 271.8,185 270.9,186.8 269.7,188.6 268.5,190.4 267,192.2 265.4,194 263.7,195.8 261.8,197.6 259.7,199.4 257.6,201.2 255.3,203 252.8,204.8 250.3,206.6 247.6,208.4 244.9,210.2 242,212 239.1,213.8 236,215.6 232.9,217.4 229.8,219.2 226.6,221 223.3,222.8 220,224.6 216.7,226.4 213.3,228.2 210,230 206.7,231.8 203.3,233.6 200,235.4 196.7,237.2 193.4,239 190.2,240.8 187.1,242.6 184,244.4 180.9,246.2 178,248 175.1,249.8 172.4,251.6 169.7,253.4 167.2,255.2 164.7,257 162.4,258.8 160.3,260.6 158.2,262.4 156.3,264.2 154.6,266 153,267.8 151.5,269.6 150.3,271.4 149.1,273.2 148.2,275 147.4,276.8 146.8,278.6 146.4,280.4 146.1,282.2 146,284 146.1,285.8 146.4,287.6 146.8,289.4 147.4,291.2 148.2,293 149.1,294.8 150.3,296.6 151.5,298.4 153,300.2 154.6,302 156.3,303.8 158.2,305.6 160.3,307.4 162.4,309.2 164.7,311 167.2,312.8 169.7,314.6 172.4,316.4 175.1,318.2 178,320 180.9,321.8 184,323.6 187.1,325.4 190.2,327.2 193.4,329 196.7,330.8 200,332.6 203.3,334.4 206.7,336.2 210,338 213.3,339.8 216.7,341.6 220,343.4 223.3,345.2 226.6,347 229.8,348.8 232.9,350.6 236,352.4 239.1,354.2 242,356 244.9,357.8 247.6,359.6 250.3,361.4 252.8,363.2 255.3,365 257.6,366.8 259.7,368.6 261.8,370.4 263.7,372.2 265.4,374 267,375.8 268.5,377.6 269.7,379.4 270.9,381.2 271.8,383 272.6,384.8 273.2,386.6 273.6,388.4 273.9,390.2 274,392" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="206,176 214,176" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="180" font-size="11" fill="currentColor">0°</text>
  <polyline points="206,230 214,230" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="234" font-size="11" fill="currentColor">90°</text>
  <polyline points="206,284 214,284" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="288" font-size="11" fill="currentColor">180°</text>
  <polyline points="206,338 214,338" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="342" font-size="11" fill="currentColor">270°</text>
  <polyline points="206,392 214,392" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="396" font-size="11" fill="currentColor">360°</text>
  <circle cx="251.1" cy="35" r="4" fill="currentColor"/>
  <circle cx="251.1" cy="206" r="4" fill="currentColor"/>
  <circle cx="251.1" cy="84" r="2.6" fill="currentColor"/>
  <text x="259" y="30" font-size="11" fill="currentColor">e<tspan dy="-5" font-size="10">jθ</tspan></text>
  <text x="236" y="76" font-size="11" fill="currentColor">θ</text>
  <text x="230" y="101" font-size="11" text-anchor="middle" fill="currentColor">cos θ</text>
  <text x="228" y="199" font-size="11" text-anchor="middle" fill="currentColor">cos θ</text>
  <text x="318" y="38" font-size="11" fill="currentColor">a point going round the unit circle, θ = 50°</text>
  <text x="318" y="88" font-size="11" fill="currentColor">its shadow on the real axis: cos θ</text>
  <text x="318" y="210" font-size="11" fill="currentColor">the same length on the wave: cos 50° = 0.643</text>
  <text x="318" y="300" font-size="11" fill="currentColor">the shadow, plotted as θ grows</text>
  <text x="218" y="408" font-size="11" fill="currentColor">θ grows downward</text>
</svg>

A point $e^{j\theta}$ goes round the unit circle; its shadow on the real axis is the thick segment from the centre, of length $\cos\theta$ — $0.643$ at $\theta = 50°$. Plotted against $\theta$, which grows downward here, that shadow traces the wave below: the same thick segment reappears at $50°$, and the wave swings between $-1$ and $1$, the circle's own radius. The wave is not a second object but the rotation seen edge-on, which is why "decompose into sinusoids" and "project onto rotations" are one sentence.



### 8. Linear differential equations (→ control track: pages 5–7)

Push a handle into a wall, switch a heater on or command a joint, and the question is the same: how does the system move from then on — does it settle, how fast, and does it ring? The answer is the solution of a differential equation, and this section solves the linear ones by hand. Physical systems are described by ODEs — this is the modeling language of all of control, picked up directly in [[04-robotics/control-theory-ce397|5. Control Theory §2–4]]. The mass–spring–damper this section solves is derived from a free-body diagram, with units and energy, on the plant **P3** — the wiki's one-degree-of-freedom handle pushed into a wall ([[02-foundations/lab-plants|0.6 Lab Plants]]) — in [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §5]].

- An **ODE** (ordinary differential equation) is an equation relating an unknown function
  of one variable, here $x(t)$, to its derivatives; its **order** is the highest derivative
  that appears. It is **linear** when $x$ and its derivatives appear only to the first power,
  multiplied by coefficients that do not depend on $x$:
  $$a_n\,x^{(n)} + \cdots + a_1\,\dot x + a_0\,x = u(t)$$
  where $\dot x = dx/dt$, $x^{(n)}$ is the $n$-th derivative, the $a_i$ are the coefficients
  (constants throughout this section) and $u(t)$ is the input. Linear ODEs obey superposition
  (§4.5), so solutions to separate inputs add up, which is why every tool below works. Non-example:
  $\dot x = -x^2$. Both $x_1 = 1/(t+1)$ and $x_2 = 1/(t+2)$ solve it, but their sum does not:
  at $t = 0$ the sum has slope $-1 - 0.25 = -1.25$, while $-(\text{sum})^2 = -(1.5)^2 = -2.25$.
- **First order**: $\dot x = ax$ has solution $x(t) = x(0)\,e^{at}$. You do not have to solve
  anything to believe it — just differentiate the candidate and check:
  $\frac{d}{dt}\big(x(0)e^{at}\big) = a\,x(0)e^{at} = a\,x(t)$ ✓, and at $t=0$ it gives
  $x(0)$ ✓. That is the entire content of "$e$ is the function that is its own derivative"
  (§6) applied to a physical system. Everything follows from this one fact: $a < 0$ decays (stable), $a > 0$ blows up (unstable). Here "stable" means
  *asymptotically stable*: from every starting value $x(0)$ the solution returns to $0$ as
  $t \to \infty$ (the full definition is [[04-robotics/control-theory-ce397|5. Control Theory §4]]). A robot joint,
  a heating room, a draining tank — all locally this equation.
- **Time constant.** A stable first-order response closes the gap to its final value $x_\infty$
  exponentially, and the **time constant** $\tau$ is the *time* that sets how fast. For
  $\dot x = ax$ with $a < 0$ (a constant input only moves $x_\infty$),
  $$\tau = \frac{1}{|a|}, \qquad x(t) - x_\infty = \big(x(0) - x_\infty\big)\,e^{-t/\tau}$$
  so in every $\tau$ the gap shrinks by a factor $e$: after one $\tau$ the response has covered
  $1 - e^{-1} = 63\%$ of the way, and its starting tangent reaches $x_\infty$ exactly at $t = \tau$.
  It exists only for $a < 0$. Example: P4 has $a = -1$, so $\tau = 1\,\mathrm s$; the problem
  set's heater $\dot x = -2x + u$ has $\tau = 0.5\,\mathrm s$. Non-example: $\tau$ is not the time
  to *reach* $x_\infty$, which an exponential never quite does. Why it matters: settling within
  2% takes $\ln 50 = 3.9$ time constants, about $4\tau$, so this one number says how fast a
  first-order plant responds ([[02-foundations/basic-mechanics|0.6.1 §5]] extends it to the
  envelope of a ringing mass–spring–damper).
- **Worked: plant P4.** The leaky heater of [[02-foundations/lab-plants|0.6]] is $\dot x=-x+u$ (its disturbance $d$ set to $0$). With $u=1$ and $x(0)=0$, solve it in three moves. A constant that makes the right side zero solves it: $x=1$ gives $\dot x=0=-1+1$ — the *particular* solution, the steady state the input holds. The input-free equation $\dot x=-x$ is the first-order case above with $a=-1$, solved by $ce^{-t}$ for any $c$ — the *homogeneous* solution. By superposition (§4.5) their sum $x(t)=1+ce^{-t}$ still solves $\dot x=-x+1$, and $x(0)=0$ fixes $c=-1$:
  $$x(t) = 1 - e^{-t}$$
  so at $t=0.1$ and $0.2$ it is $0.095$ and $0.181$. **Forward Euler** is the simplest way code steps an ODE: follow the slope at the start of the step for one step of length $T$, $x_{k+1}=x_k+T\,\dot x(x_k)$ — here $x\leftarrow x+T(-x+u)$ ([[02-foundations/lab-kernel|0.7 Lab Kernel §2]] calls it explicit Euler). With $T=0.1$ it gives $0.10$ then $0.19$. It is high because the slope at the *start* of each step is where $1-x$ is largest.
- **Reading the picture.** The picture at the top of the page is this ODE as a block diagram, read left to right. The circle is a **summing junction**, which adds its inputs with the signs written beside them, so its output is $\dot x=u-x$; the box marked $\int$ or $1/s$ is an **integrator**, which turns a rate back into the quantity it changes (§9 shows why integrating is dividing by $s$); and the small box is a **gain**, a plain multiplier, here $1$, the heater's own leak rate. A controller $u=-Kx$ ([[04-robotics/control-theory-ce397|5. Control Theory §1]]) feeds $x$ back through a second gain $K$, the **feedback gain**, and the two add, so the loop becomes $\dot x=-(1+K)x$ — the picture's "later $1+K$".
- **With input**: $\dot x = ax + bu$ — the solution is "decayed initial state + accumulated
  input",
  $$x(t) = e^{at}\,x(0) + \int_0^t e^{a(t-t')}\,b\,u(t')\,dt'$$
  because each slice of input $b\,u(t')\,dt'$ enters at time $t'$ and then decays like the free
  response for the remaining time $t-t'$, and superposition (§4.5) adds the slices. Check on P4
  ($a=-1$, $b=1$, $u=1$, $x(0)=0$): $\int_0^t e^{-(t-t')}\,dt' = 1-e^{-t}$, the worked case's
  answer. This is the scalar version of the state-space model
  $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$ ([[02-foundations/linear-algebra|linear algebra §5]]),
  and $e^{at}$ becomes the matrix exponential $e^{At}$ with eigenvalues playing the role of $a$.
- **Second order**: $\ddot x + 2\zeta\omega_n \dot x + \omega_n^2 x = 0$ — the
  mass-spring-damper. Two numbers describe every response: natural frequency $\omega_n$
  (the undamped frequency scale) and damping ratio $\zeta$ (whether it rings: $0<\zeta<1$
  oscillates while decaying, at $\omega_d = \omega_n\sqrt{1-\zeta^2}$; $\zeta \ge 1$ doesn't; $\zeta = 0$ oscillates forever and $\zeta<0$ grows). Robot arms and suspension systems are tuned in this
  vocabulary. Both numbers come from the physical form $m\ddot x + c\dot x + kx = 0$ with mass
  $m$, damping coefficient $c$ and stiffness $k$: dividing by $m$ and matching terms gives
  $$\omega_n = \sqrt{k/m}, \qquad \zeta = \frac{c}{2\sqrt{km}}$$
  so stiffness raises the frequency and damping raises $\zeta$. The three named regimes are
  *underdamped* ($0 < \zeta < 1$), *critically damped* ($\zeta = 1$, the fastest return with no
  overshoot) and *overdamped* ($\zeta > 1$). Example: $m = 1$, $c = 1$, $k = 4$ gives
  $\omega_n = 2$ rad/s and $\zeta = 0.25$, underdamped, ringing at
  $\omega_d = 2\sqrt{1 - 0.0625} = 1.936$ rad/s. The same two numbers on P3's handle — its
  damper, its $\zeta$ and the overshoot they cause, from a free-body diagram — are
  [[02-foundations/basic-mechanics|0.6.1 §4–§5]]; and with the motion stopped,
  $\ddot x = \dot x = 0$, a push $F$ on the right-hand side leaves only the statics you know, $kx = F$.
- Discrete time (what code runs): $x_{t+1} = a x_t$ ⇒ $x_t = a^t x_0$ — stable iff
  $|a| < 1$. The continuous and discrete conditions ($\text{Re}(a) < 0$ vs $|a_d| < 1$) are
  the same statement, and here is the bridge: sampling $\dot x = ax$ every $\Delta t$ gives
  $x_{t+1} = e^{a\Delta t}x_t$, so the discrete factor is $a_d = e^{a\Delta t}$. Since
  $|e^{a\Delta t}| = e^{\text{Re}(a)\Delta t}$, that magnitude is below $1$ exactly when
  $\text{Re}(a) < 0$. The left half-plane *maps into* the open unit disc — one story, two
  coordinate systems.

### 9. Laplace transform and the s-plane (→ control track, 6. Signal Processing §5)

> [!note] This section is a preview, not the destination
> §9 exists so the words *pole*, *transfer function*, and *frequency response* are not new
> when you meet them. The places that actually teach them are
> [[04-robotics/control-theory-ce397|5. Control Theory §5]] — which turns pole positions into
> the settling-time and overshoot **numbers** papers quote — and
> [[02-foundations/signal-processing|6. Signal Processing §5]], which uses the same object to
> design filters. It is thin by design: read it once for vocabulary, let the zero and
> minimal-realization details go by on a first pass, and come back after those two.

A control loop chains several blocks, and solving their ODEs in time, block by block, is slow and buries the two things a designer needs: whether the loop settles, and how fast. The Laplace transform turns ODEs into algebra — and [[04-robotics/control-theory-ce397|5. Control Theory §5]] turns the resulting pole picture into the settling-time and overshoot numbers papers quote:

- Definition: the **Laplace transform** maps a signal $f(t)$, defined for $t \ge 0$, to a
  function of a complex variable,
  $$F(s) = \mathcal{L}[f](s) = \int_0^\infty f(t)\,e^{-st}\,dt$$
  where $s = \sigma + j\omega$ is a complex frequency: its real part $\sigma$ sets a decay rate
  and its imaginary part $\omega$ an oscillation rate. The integral exists only for $\text{Re}(s)$
  large enough, since $e^{-st}$ must beat the growth of $f$. Two properties make it useful. It is
  linear, $\mathcal{L}[af + bg] = aF + bG$ (§4.5). And, the one property that matters most,
  **differentiation becomes multiplication by $s$** — $\mathcal{L}[\dot f] = sF(s) - f(0)$,
  which follows from integrating by parts. Read backwards, it turns **integration into
  division by $s$**: the running integral $g(t) = \int_0^t f(t')\,dt'$ has $g(0) = 0$ and
  $\dot g = f$, so $F = sG$ and
  $$\mathcal{L}\Big[\int_0^t f(t')\,dt'\Big] = \frac{F(s)}{s}$$
  which is why the picture's integrator box is labelled $1/s$. Example: for $f(t) = e^{at}$,
  $F(s) = \int_0^\infty e^{(a-s)t}\,dt = \frac{1}{s-a}$ whenever $\text{Re}(s) > a$; with
  $a = -3$ and $s = 1$ that is $1/4$, and integrating $e^{-4t}$ numerically gives $0.25$ ✓.
- Consequence: an ODE becomes a polynomial equation, and a system becomes a
  **transfer function** $G(s) = \frac{\text{output}(s)}{\text{input}(s)}$.
  **Worked, in four lines.** Take $\dot x = ax + u$ and Laplace-transform both sides.
  Transfer functions are always defined with the system starting at rest, $x(0) = 0$, so
  the left side is $\mathcal{L}[\dot x] = sX(s) - x(0) = sX(s)$, and the right side is
  $aX(s) + U(s)$ because the transform is linear. So:
  $$sX(s) = aX(s) + U(s) \;\Rightarrow\; (s-a)X(s) = U(s) \;\Rightarrow\; G(s) = \frac{X(s)}{U(s)} = \frac{1}{s-a}$$
  Notice what just happened: a differential equation became a *division*. And the one value
  of $s$ that breaks the division, $s = a$, is the **pole** — the same $a$ whose sign decided
  stability back in §8. Poles are not a new idea; they are §8's exponents, relabelled.
- **Poles** = roots of the denominator = the $a$'s of section 8 = eigenvalues of the
  state-space $A$ (every pole is an eigenvalue; the note below says when an eigenvalue can hide). Plotted in the complex **s-plane**:
  - left half-plane (negative real part) → decaying → **stable**
  - right half-plane → growing → **unstable**
  - imaginary part → oscillation frequency; distance from axis → decay speed

<svg viewBox="0 0 560 336" style="max-width:100%;height:auto" role="img" aria-label="The s-plane with the page's poles: a real pole at -3 from 1/(s+3), a real pole at -1 from the leaky heater P4, and the complex pair -0.5 plus or minus 1.936j of the mass-spring-damper with m = 1, c = 1, k = 4, all in the shaded stable left half-plane; an unstable pole at +1 in the right half-plane. Dashed segments from the upper pole mark sigma = -0.5 to the imaginary axis and omega_d = 1.936 down to the real axis.">
  <defs><marker id="emSp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="40" y="10" width="290" height="320" fill="currentColor" fill-opacity="0.06"/>
  <polyline points="44,170 520,170" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emSp)"/>
  <polyline points="330,328 330,8" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emSp)"/>
  <text x="120" y="188" font-size="11" text-anchor="middle" fill="currentColor">−3</text>
  <polyline points="190,166 190,174" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="188" font-size="11" text-anchor="middle" fill="currentColor">−2</text>
  <text x="260" y="188" font-size="11" text-anchor="middle" fill="currentColor">−1</text>
  <text x="400" y="188" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="470,166 470,174" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="470" y="188" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <polyline points="326,310 334,310" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="314" font-size="11" fill="currentColor">−2</text>
  <polyline points="326,240 334,240" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="244" font-size="11" fill="currentColor">−1</text>
  <polyline points="326,100 334,100" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="104" font-size="11" fill="currentColor">1</text>
  <polyline points="326,30 334,30" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="34" font-size="11" fill="currentColor">2</text>
  <text x="510" y="190" font-size="11" text-anchor="end" fill="currentColor">Re</text>
  <text x="340" y="18" font-size="11" fill="currentColor">Im</text>
  <polyline points="295,34.4 330,34.4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="295,34.4 295,170" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="312.5" y="27.4" font-size="12" text-anchor="middle" fill="currentColor">σ</text>
  <text x="289" y="106.2" font-size="12" text-anchor="end" fill="currentColor">ω<tspan dy="3" font-size="10">d</tspan></text>
  <path d="M290,29.4 L300,39.4 M290,39.4 L300,29.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M290,300.6 L300,310.6 M290,310.6 L300,300.6" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M115,165 L125,175 M115,175 L125,165" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M255,165 L265,175 M255,175 L265,165" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M395,165 L405,175 M395,175 L405,165" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="283" y="35.4" font-size="11" text-anchor="end" fill="currentColor">−0.5 ± 1.936j</text>
  <text x="283" y="49.4" font-size="11" text-anchor="end" fill="currentColor">§8's m = 1, c = 1, k = 4</text>
  <text x="120" y="157" font-size="11" text-anchor="middle" fill="currentColor">−3: 1/(s + 3)</text>
  <text x="260" y="157" font-size="11" text-anchor="middle" fill="currentColor">−1: P4</text>
  <text x="400" y="157" font-size="11" text-anchor="middle" fill="currentColor">+1: grows as e<tspan dy="-5" font-size="10">t</tspan></text>
  <text x="48" y="322" font-size="11" fill="currentColor">left half-plane: stable</text>
  <text x="392" y="322" font-size="11" fill="currentColor">right half-plane: unstable</text>
</svg>

The page's own poles: $-3$ from $1/(s+3)$, $-1$ from P4, the pair $-0.5 \pm 1.936j$ of §8's mass–spring–damper ($m=1$, $c=1$, $k=4$), and an unstable $+1$ for contrast. For the pair, the horizontal dashed segment is $\sigma = -\zeta\omega_n = -0.5$, the rate of its decaying envelope $e^{-0.5t}$, and the vertical one is $\omega_d = 1.936$ rad/s, its ringing frequency. Farther left means faster decay, farther from the real axis faster oscillation, and anything right of the imaginary axis grows.

> [!note]- Deeper · 더 깊이
> **Zeros, cancellation and the minimal realization.** Every pole is an eigenvalue, but an eigenvalue appears as a pole only when no pole–zero cancellation hides it. A **zero** is a root of the numerator; if the same factor sits on top and bottom, as in $\frac{s-1}{(s-1)(s+2)} = \frac{1}{s+2}$, it cancels and that eigenvalue ($s=1$ here) vanishes from $G(s)$. A state-space model with no such hidden modes is called a *minimal realization* (Åström & Murray Example 9.7). A cancelled unstable eigenvalue is invisible in $G(s)$: the transfer function looks stable while a state inside the system grows.

- This is why §7's complex plane matters for control:
  *a system's entire qualitative behavior is a picture — where its poles sit.*
- **What "frequency response is $G(j\omega)$" means.** $G$ was defined for complex $s$, so you
  may ask what it does at any $s$ you like. Put $s = j\omega$ — a purely imaginary number,
  which by §7 is a pure rotation at rate $\omega$: an input that oscillates forever without
  growing or decaying. That is exactly "feed the system a sine wave at frequency $\omega$."
  The answer $G(j\omega)$ is a complex number, and its two parts are the two things you
  measure in the lab: its **magnitude** $|G(j\omega)|$ is how much the system amplifies that
  frequency, and its **angle** is how much it delays it. Sweep $\omega$ from low to high and
  you have plotted the system's filter — which is why the same picture serves control and
  [[02-foundations/signal-processing|signal processing]]. Poles near the imaginary axis at
  height $\omega$ make $|G(j\omega)|$ large there: that is a resonance.
  (Discrete-time twin: the Z-transform, unit circle instead of left half-plane.)
  As a formula: for a stable $G$ and the input $u(t) = \sin\omega t$, once the transient has
  died out the output is
  $$y(t) = |G(j\omega)|\,\sin\!\big(\omega t + \angle G(j\omega)\big)$$
  so the same frequency comes out, scaled by the magnitude and shifted by the angle. Worked for
  $G(s) = \frac{1}{s+3}$: at $\omega = 0.3$ rad/s, $|G| = 0.332$ and the angle is $-5.7°$; at
  $\omega = 3$, $|G| = 1/(3\sqrt2) = 0.236$ and $-45°$; at $\omega = 30$, $|G| = 0.033$ and
  $-84.3°$. Slow inputs pass almost untouched and fast ones are attenuated and delayed — the
  system is a low-pass filter with its corner at the pole's distance, $3$ rad/s. The same
  one-pole filter built from a resistor and a capacitor, with its pole at $303\,\mathrm{s^{-1}}$,
  is [[02-foundations/basic-circuits-electronics|0.6.2 §5]].

### 10. Notation dictionary (all pages)

Two definitions used everywhere before they are formally introduced:

- **Softmax** turns any score vector into a probability distribution:
  $$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$
  where $z = (z_1, \ldots, z_K)$ are $K$ real scores (often called *logits*) and $i$ picks one
  entry. It has three properties — every output is positive, the outputs sum to 1,
  and the largest score gets the largest probability (a smooth $\arg\max$) — since
  exponentials are positive and increasing and the denominator is the sum of the numerators.
  Other maps share those properties, so the formula, not the list, is what defines softmax.
  Example: $z = (1, 2, 3)$ gives $(0.090, 0.245, 0.665)$, and adding $100$ to every score gives
  exactly the same output, because the common factor $e^{100}$ cancels (the fact the log-sum-exp
  trick of §6 uses). Non-example: plain normalization $z_i / \sum_j z_j$ fails on negative
  scores, since $z = (-1, 2)$ would give the "probabilities" $(-1, 2)$. It appears in attention,
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
| $O(\cdot)$ | order of growth: $O(n^3)$ is at most a constant times $n^3$ for large $n$ (§2) |
| $\mathbb{R}^n$, $\mathbb{R}^{m\times n}$ | real vectors with $n$ entries; real $m\times n$ matrices |
| $\hat x$ | "$x$ hat": an estimate or prediction of $x$ (a network's output is $\hat y$, 0.8) |
| $A^\top$ | transpose — flip the matrix across its diagonal ($A^\top_{ij} = A_{ji}$) |
| $\det A$ | determinant — $\lvert\det A\rvert$ is the factor by which the map scales volume (the sign records an orientation flip); $0$ means it flattens space, so it has no inverse |
| $A \succeq 0$, $A \succ 0$ | positive semidefinite / definite — the matrix version of "$\ge 0$" / "$>0$": for symmetric $A$, $x^\top A x \ge 0$ for every $x$ ($\succeq$) and $x^\top A x > 0$ for every $x \ne 0$ ($\succ$) |

> [!tip] Going deeper · 더 깊이
> The honest route out of this page is not another maths book — it is the foundations pages themselves, which is what each section title points at. If a section here is not a reminder but genuinely new, the underlying course is a standard one and any of the usual engineering-mathematics texts will do; Boas, *Mathematical Methods in the Physical Sciences* and Kreyszig, *Advanced Engineering Mathematics* are the two most likely to be on a shelf near you. Read the one chapter, not the book: nothing on this page needs a term of study, and the rest of the track is where the payoff is.

### Self-check

1. Differentiate $f(x) = \log(1 + e^x)$ (softplus) using the chain rule; show the result
   is the sigmoid $\sigma(x) = 1/(1+e^{-x})$.
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

### Problem set · 과제

Tier B. **P4** from [[02-foundations/lab-plants|0.6]] with $d=0$ here; this page §8; Euler numbers on [[02-foundations/lab-kernel|0.7]]. No simulator.

1. **Draw.** The picture above for a heater that loses heat twice as fast, $\dot x=-2x+u$: the same four parts, with the feedback gain block now marked $2$. Label $x$ as temperature error. On a small inset of $x$ against $t$ for $u=1$, $x(0)=0$, mark the initial slope, the steady value and the time constant, and the exact and forward-Euler ($T=0.1$) values at $t=0.1$ and $0.2$.
2. **Derive.** Item 1's heater, $\dot x=-2x+u$ with $u=1$, now starts part-way, at $x(0)=0.25$. Solve it by §8's recipe (particular plus homogeneous), check your $x(t)$ against §8's with-input formula, and give the time constant and $x(0.5)$.
3. **Interpret.** Forward Euler on the same heater, $u=1$ from $x_0=0$, but with long steps, $T=0.75\,\mathrm s$ and $T=1.2\,\mathrm s$: take three steps with each and compare them with the exact $\tfrac12(1-e^{-2t})$. Writing the update as $x_{k+1}=(1-2T)\,x_k+T$, use §8's discrete-time rule to say for which $T$ Euler stays stable, and why a stable heater can give an unstable simulation.

> [!note]- How to draw it · 그리는 법
> - The command $u$ enters from the left and meets a summing junction, a small circle with two inputs; the second input arrives from below.
> - Write $+$ beside the $u$ arrow and $-$ beside the fed-back one: the sign at the junction, not a sign inside a box, is what makes this a *negative* feedback loop.
> - Label the junction's output $\dot x$, because the whole picture is the sentence "the sum *is* the derivative", and send it into one box marked $\int$ or $1/s$ (§9 says why those are the same box); the box's output $x$ is the temperature error, the only state.
> - Tap $x$ and route it back to the junction's lower input through a gain block marked $2$. That block is the only thing that changed: the loss rate lives in the feedback gain, not in the integrator.
> - No disturbance arrow. P4's $d$ enters the same junction as $u$, and this page sets $d=0$; [[02-foundations/rl-basics|7. RL Basics]] and the control track add that third input.
> - The inset: at $t=0$ with $x=0$ the junction outputs $\dot x=u=1$ whatever the gain, so the initial slope is unchanged. The tangent from the origin reaches the steady value $u/2=0.5$ at the time constant $1/2=0.5\,\mathrm s$, and the true curve passes below it.
> - Put four points on the inset and nothing else: exact $\tfrac12(1-e^{-2t})=0.0906$ and $0.1648$, forward Euler $0.100$ and $0.180$, each Euler point drawn *above* its exact partner — that gap, not the curve, is the argument.

> [!tip]- Solutions
> 1. The picture's loop with feedback gain $2$: $u$ and $-2x$ meet at the sum, the sum is $\dot x$, an integrator returns $x$. For $u=1$, $x(0)=0$ the solution is $x(t)=\tfrac12(1-e^{-2t})$: initial slope $1$ (the gain multiplies $x$, which is $0$ at the start), steady value $0.5$, time constant $0.5\,\mathrm s$. Exact $0.0906$ and $0.1648$ at $t=0.1$ and $0.2$; Euler $x_1=0.1\times1=0.100$, $x_2=0.100+0.1(-0.200+1)=0.180$, both high, for the picture's reason: Euler takes each step's slope at its start, where the gap is largest. Doubling the loss rate halves both the steady value and the time constant; with $u=0$ the error decays as $e^{-2t}$.
> 2. Particular: the constant that makes the right side zero, $x=\tfrac12$. Homogeneous: $ce^{-2t}$. $x(0)=0.25$ gives $c=-0.25$, so $x(t)=0.5-0.25\,e^{-2t}$. The with-input formula agrees: $0.25\,e^{-2t}+\int_0^t e^{-2(t-t')}\,dt'=0.25\,e^{-2t}+\tfrac12(1-e^{-2t})=0.5-0.25\,e^{-2t}$. The time constant is $1/2=0.5\,\mathrm s$ whatever the start, and $x(0.5)=0.5-0.25\,e^{-1}=0.408$: a part-way start only shrinks the gap the exponential has to close.
> 3. $T=0.75$: the factor $1-2T$ is $-0.5$, and Euler gives $0.75$, $0.375$, $0.5625$ against the exact $0.388$, $0.475$, $0.494$ — it overshoots the steady value $0.5$ and then swings around it, the swing halving at every step. $T=1.2$: the factor is $-1.4$, and Euler gives $1.2$, $-0.48$, $1.872$ against the exact $0.455$, $0.496$, $0.500$ — the swing grows 1.4-fold per step and the simulation diverges although the heater is stable. The error $e_k=x_k-0.5$ obeys $e_{k+1}=(1-2T)\,e_k$, so by §8's rule Euler is stable exactly when $|1-2T|<1$, that is $0<T<1\,\mathrm s=2\tau$, and it approaches without swinging only for $T\le\tau=0.5\,\mathrm s$. The heater's true factor per step is $e^{-2T}$, always between 0 and 1; Euler replaces it by $1-2T$, its first-order Taylor expansion (§2), which is close only when $T\ll\tau$.

## 한국어

*[[02-foundations/overview|0. Overview]]가 지도를 그렸다. 이 페이지는 그 지도가 말없이 전제하는 학부 수학 — 미분, 행렬 연산,
로그, 복소수 — 을 닫는다. 나머지 기초 페이지 대부분이 여기를 선수 지식으로 지목한다. 그래서 맨 앞이다.*

1~9 페이지가 말없이 전제하는 공업수학을 한곳에 자체 완결로 정리했다.
각 절이 정확히 어느 기초 페이지에 쓰이는지 표시했다. 기계학습 용어 몇 개 — *손실*, *ReLU*,
*층*, *배치*, *softmax* — 는 어느 페이지도 가르치기 전에 예시로 먼저 나온다. 지금은 이름표로만
읽어 두면 되고, [[02-foundations/neural-network-basics|0.8 신경망이란 무엇인가]]가 하나씩 정의한다
(softmax는 아래 §10에서도 정의한다). 전부 술술 읽히면 1. 선형대수로 바로 건너뛰지 말고
[[02-foundations/overview|0. Overview]]의 학습 순서대로 간다. 먼저 [[02-foundations/lab-plants|0.6 Lab Plants]]
— *장치*(plant)는 제어하려는 시스템을 부르는 제어공학의 말이고, 그 페이지는 모든 과제가 다시 쓰는
작은 시험 시스템 여섯 개 P1–P6을 고정해 둔다 — 와 [[02-foundations/lab-kernel|0.7 Lab Kernel]],
그다음 학부에서 비어 있던 물리 바닥([[02-foundations/basic-mechanics|0.6.1]],
[[02-foundations/basic-circuits-electronics|0.6.2]], [[02-foundations/fluid-power|0.6.3]]),
그리고 0.8이다.

> [!note] 왜 배우는가 · Why this matters
> **지금 있는 곳:** [[physical-ai-map|피지컬 AI 지도]]에서 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 스택 전체를 받치는 수학 바닥으로, 미분·행렬·로그는 모든 층 밑에, §8–§9의 선형 미분방정식과 극점은 조작과 접촉 바로 밑에 있다 — "저 패널을 프레임에 설치해"에서 로봇이 패널을 옮기고, 프레임에 닿은 것을 느끼고, 끼워 앉히는 단계들이다. **왜:** 접촉은 스프링과 댐퍼에 매달린 질량처럼 움직여서 같은 힘으로 밀어도 울리기도 하고 곧장 가라앉기도 하는데, 위키의 1자유도 시험용 핸들 P3([[02-foundations/lab-plants|0.6 Lab Plants]])를 $400\,\mathrm{N/m}$ 벽에 $0.4\,\mathrm N$으로 밀면 감쇠비 $\zeta = 0.10$에서는 $73\%$ 넘어갔다가 가라앉는 데 $0.38\,\mathrm s$가 걸리고, $\zeta = 0.78$에서는 $2\%$만 넘고 $36\,\mathrm{ms}$ 만에 가라앉는다([[02-foundations/basic-mechanics|0.6.1 §10]]). 어느 쪽일지는 무엇이 강철에 닿기도 전에 §8의 $\zeta = c/(2\sqrt{km})$가 알려 준다. **방향:** [[04-robotics/control-theory-ce397|5. 제어 이론 §2–§5]], [[04-robotics/system-identification|5.5 시스템 식별 §2]], [[04-robotics/modern-robotics/ch11-robot-control|MR 11장 §1]]이 §8–§9 위에 서고, [[02-foundations/calculus-backprop|2. 미적분 §1]]과 [[02-foundations/optimization|4. 최적화 §3]]은 §1–§2에서 출발하며, [[07-research-program/index|7. 연구 프로그램 §8]]의 학위논문 경로에서 이 페이지는 블록 1, 곧 기초 통과 점검의 바닥이다. **얻는 것:** 함수를 미분하고 선형화하고, 새는 히터 P4([[02-foundations/lab-plants|0.6]]) 같은 1차 장치의 응답을 풀어 그리고, 극점에서 안정성을 읽고, 어떤 사상이 선형인지 판별할 수 있다.

> [!note] 처음이라면 · First pass
> 이 페이지는 서사가 아니라 참고서라서, 첫 읽기는 시험을 먼저 치르고 필요한 곳만 골라 읽는 방식이다 — 60–90분짜리 두 회차쯤 된다. **1회차:** 스스로 점검 여섯 문항을 책을 덮고 풀고(30분쯤), 틀린 문항의 절만 읽는다. 그다음 공업수학에 익숙한 사람에게도 표준 과목이 아닌 네 부분을 읽는다: §1의 그래디언트 계산 예제와 등고선 그림, §4.5(뒤의 모든 페이지가 다시 쓰는 선형성의 정의), §6의 log-sum-exp, 그리고 §10 표기법 사전 한 번 훑기. **2회차:** 그림과 §8 전체를 읽고 — 동역학이 처음이라면 시정수, 블록선도, P4 계산이 새롭다 — 과제를 푸는데, 그리기 문항은 *그리는 법*을 열기 전에 먼저 그린다. §9는 제어 트랙의 예고편이니 어휘만 한 번 읽거나 [[04-robotics/control-theory-ce397|5. 제어 이론]]에 닿을 때까지 미뤄도 된다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 336" style="max-width:100%;height:auto" role="img" aria-label="새는 히터 P4의 블록선도: 명령 u = 1이 합산점으로 들어가고 그 출력이 x-dot이며, 적분기가 온도 오차 x를 돌려주고, x는 이득 1을 거쳐 음의 부호로 돌아온다. 삽도: 계단 응답과 t = 1 s에서 1에 닿는 초기 접선, 그리고 오일러 점 둘이 정확값 점 둘 위에 있는 확대 그림.">
  <defs><marker id="emHwk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="16,44 109,44" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#emHwk)"/>
  <text x="20" y="36" font-size="11" fill="currentColor">u = 1</text>
  <circle cx="122" cy="44" r="12" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="106" y="39" font-size="13" text-anchor="end" fill="currentColor">+</text>
  <text x="116" y="69" font-size="13" text-anchor="end" fill="currentColor">−</text>
  <polyline points="134,44 213,44" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#emHwk)"/>
  <text x="174" y="36" font-size="11" text-anchor="middle" fill="currentColor">ẋ = u − x</text>
  <text x="174" y="64" font-size="11" text-anchor="middle" opacity="0.9" fill="currentColor">t = 0, x = 0</text>
  <text x="174" y="77" font-size="11" text-anchor="middle" opacity="0.9" fill="currentColor">ẋ = 초당 1</text>
  <rect x="214" y="22" width="60" height="44" rx="3" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <text x="244" y="45" font-size="18" text-anchor="middle" fill="currentColor">∫</text>
  <text x="244" y="60" font-size="11" text-anchor="middle" fill="currentColor">1/s</text>
  <polyline points="274,44 548,44" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#emHwk)"/>
  <text x="288" y="36" font-size="11" fill="currentColor">x: 온도 오차, 유일한 상태</text>
  <circle cx="500" cy="44" r="2.8" fill="currentColor"/>
  <polyline points="500,44 500,108 303,108" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#emHwk)"/>
  <text x="507" y="80" font-size="11" fill="currentColor">x</text>
  <rect x="272" y="96" width="30" height="24" rx="2" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <text x="287" y="112" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <text x="287" y="135" font-size="11" text-anchor="middle" opacity="0.9" fill="currentColor">이득 1 (나중에 1 + K)</text>
  <polyline points="272,108 122,108 122,57" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#emHwk)"/>
  <polyline points="52,310 264,310" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#emHwk)"/>
  <polyline points="52,310 52,168" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#emHwk)"/>
  <text x="266" y="314" font-size="11" fill="currentColor">t (s)</text>
  <text x="48" y="166" font-size="11" text-anchor="end" fill="currentColor">x</text>
  <polyline points="132,310 132,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="132" y="326" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="212,310 212,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="212" y="326" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <polyline points="52,250 48,250" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="254" font-size="11" text-anchor="end" fill="currentColor">0.5</text>
  <polyline points="52,190 48,190" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="194" font-size="11" text-anchor="end" fill="currentColor">1</text>
  <text x="45" y="324" font-size="11" text-anchor="end" fill="currentColor">0</text>
  <polyline points="52,190 252,190" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <text x="252" y="184" font-size="11" text-anchor="end" opacity="0.9" fill="currentColor">정상값 1</text>
  <polyline points="132,310 132,190" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.7"/>
  <text x="137" y="252" font-size="11" fill="currentColor">τ = 1 s</text>
  <polyline points="52,310 53.7,307.5 55.3,305.1 57,302.7 58.7,300.4 60.3,298.1 62,295.9 63.7,293.7 65.3,291.6 67,289.5 68.7,287.4 70.3,285.4 72,283.5 73.7,281.5 75.3,279.6 77,277.8 78.7,276 80.3,274.2 82,272.5 83.7,270.8 85.3,269.1 87,267.5 88.7,265.9 90.3,264.3 92,262.8 93.7,261.3 95.3,259.8 97,258.4 98.7,257 100.3,255.6 102,254.2 103.7,252.9 105.3,251.6 107,250.3 108.7,249.1 110.3,247.9 112,246.7 113.7,245.5 115.3,244.4 117,243.2 118.7,242.2 120.3,241.1 122,240 123.7,239 125.3,238 127,237 128.7,236 130.3,235.1 132,234.1 133.7,233.2 135.3,232.3 137,231.5 138.7,230.6 140.3,229.8 142,229 143.7,228.2 145.3,227.4 147,226.6 148.7,225.8 150.3,225.1 152,224.4 153.7,223.7 155.3,223 157,222.3 158.7,221.6 160.3,221 162,220.3 163.7,219.7 165.3,219.1 167,218.5 168.7,217.9 170.3,217.3 172,216.8 173.7,216.2 175.3,215.7 177,215.2 178.7,214.6 180.3,214.1 182,213.6 183.7,213.1 185.3,212.7 187,212.2 188.7,211.7 190.3,211.3 192,210.9 193.7,210.4 195.3,210 197,209.6 198.7,209.2 200.3,208.8 202,208.4 203.7,208 205.3,207.7 207,207.3 208.7,206.9 210.3,206.6 212,206.2 213.7,205.9 215.3,205.6 217,205.3 218.7,204.9 220.3,204.6 222,204.3 223.7,204 225.3,203.7 227,203.5 228.7,203.2 230.3,202.9 232,202.6 233.7,202.4 235.3,202.1 237,201.9 238.7,201.6 240.3,201.4 242,201.2 243.7,200.9 245.3,200.7 247,200.5 248.7,200.3 250.3,200.1 252,199.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="52,310 140,178" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <circle cx="132" cy="190" r="2.6" fill="currentColor"/>
  <text x="60" y="206" font-size="11" fill="currentColor">기울기 1 /s</text>
  <text x="204" y="227.9" font-size="11" fill="currentColor">x = 1 − e<tspan dy="-5" font-size="10">−t</tspan></text>
  <rect x="58" y="284.6" width="12" height="14.9" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="70,292 330,292" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" stroke-opacity="0.8"/>
  <rect x="330" y="146" width="210" height="164" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>
  <polyline points="365,310 365,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="326" font-size="11" text-anchor="middle" fill="currentColor">0.1</text>
  <polyline points="505,310 505,314" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="505" y="326" font-size="11" text-anchor="middle" fill="currentColor">0.2</text>
  <text x="540" y="326" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">t (s)</text>
  <polyline points="354,310 357.1,307.3 360.2,304.7 363.3,302 366.4,299.4 369.5,296.7 372.6,294.1 375.7,291.4 378.8,288.8 381.9,286.2 385,283.6 388.1,281 391.2,278.4 394.3,275.8 397.4,273.2 400.5,270.6 403.6,268 406.7,265.4 409.8,262.9 412.9,260.3 416,257.7 419.1,255.2 422.2,252.6 425.3,250.1 428.4,247.6 431.5,245 434.6,242.5 437.7,240 440.8,237.5 443.9,235 447,232.5 450.1,230 453.2,227.5 456.3,225 459.4,222.5 462.5,220 465.6,217.6 468.7,215.1 471.8,212.6 474.9,210.2 478,207.7 481.1,205.3 484.2,202.9 487.3,200.4 490.4,198 493.5,195.6 496.6,193.2 499.7,190.8 502.8,188.4 505.9,186 509,183.6 512.1,181.2 515.2,178.8 518.3,176.4 521.4,174 524.5,171.7 527.6,169.3 530.7,166.9 533.8,164.6 536.9,162.3 540,159.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="348.2,310 521.8,146" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <circle cx="365" cy="294.1" r="2.9" fill="currentColor"/>
  <circle cx="365" cy="300.5" r="2.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="358" y="291.1" font-size="11" text-anchor="end" fill="currentColor">0.10</text>
  <text x="373" y="307.5" font-size="11" fill="currentColor">0.095</text>
  <circle cx="505" cy="175.1" r="2.9" fill="currentColor"/>
  <circle cx="505" cy="186.6" r="2.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="501" y="157.1" font-size="11" text-anchor="end" fill="currentColor">0.19</text>
  <polyline points="501,160.1 503.5,171.7" fill="none" stroke="currentColor" stroke-width="0.8"/>
  <text x="513" y="193.6" font-size="11" fill="currentColor">0.181</text>
  <circle cx="440" cy="280" r="2.9" fill="currentColor"/>
  <text x="449" y="284" font-size="11" fill="currentColor">전진 오일러</text>
  <circle cx="440" cy="295" r="2.9" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="449" y="299" font-size="11" fill="currentColor">정확값</text>
</svg>

§8의 새는 히터 $\dot x=-x+u$, 곧 제어 대상(plant: 제어하려는 물리 시스템) **P4**(위키의 연습용 1차 시스템인 '새는 히터'. 온도가 히터 명령을 천천히 따라간다, [[02-foundations/lab-plants|0.6 Lab Plants]])의 블록선도로, 명령 $u=1$은 $+$로, 되먹임된 $x$는 $-$로 합산점에 들어가 그 합이 $\dot x$가 되고, 적분기($\int$ 또는 $1/s$)가 유일한 상태인 온도 오차 $x$를 돌려주며, $x$는 이득 $1$을 거쳐 되돌아온다($d=0$이라 외란 입력은 없다). 삽도는 $x=0$에서 시작한 계단 응답으로, 초당 $1$인 초기 기울기의 접선이 시정수 $t=1\,\mathrm{s}$에서 정상값 $1$에 닿고 곡선 $x=1-e^{-t}$는 그 아래로 지난다. 확대한 모서리에서는 $t=0.1$과 $0.2$의 전진 오일러 $0.10$과 $0.19$가 정확값 $0.095$와 $0.181$보다 각각 $0.005$, $0.009$ 위에 있는데, 오일러가 $1-x$가 가장 큰 스텝 시작점의 기울기를 쓰기 때문이다.

### 1. 미분 (→ 2. 미적분, 4. 최적화에서 사용)

학습과 제어의 모든 방법은 — 손실을 줄이려고 가중치 수백만 개를 미는 학습 스텝이든, 오차를 줄이려고 모터 명령을 미는 제어기든 — 한 가지를 묻는다: 이 입력을 살짝 밀면 출력이 얼마나 움직이는가? 그 물음에 답하는 숫자가 도함수이고, 입력이 여럿일 때의 답이 그래디언트다.

- **도함수** $f'$은 각 점 $x$에서 $f$의 순간 변화율을 돌려주는 새 함수다. 민감도로서의 정의:
  $$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$$
  — "입력을 살짝 밀면 출력이 얼마나 움직이는가?" $h$는 미는 크기, 분수는 $(x, f(x))$와
  $(x+h, f(x+h))$를 잇는 직선의 기울기이고, 극한은 $h$가 어느 쪽에서 줄어들든 그 기울기가
  한 값으로 모인다는 뜻이다. 모이면 $f$가 $x$에서 *미분 가능*하다고 한다. 예: $f(x) = x^2$,
  $x = 3$, $h = 0.01$이면 $(9.0601 - 9)/0.01 = 6.01$로 $f'(3) = 6$에 다가간다. 비예시:
  $f(x) = |x|$의 $0$에서는 오른쪽 기울기가 $+1$, 왼쪽이 $-1$이라 극한이 하나로 정해지지 않는다
  — 0.8의 함수 ReLU, 곧 $\max(0, x)$가 0에서 가진 바로 그 꺾임이다.
- 실제로 쓰는 규칙들:

| 규칙 | 공식 |
|---|---|
| 거듭제곱 | $(x^n)' = nx^{n-1}$ |
| 곱 | $(fg)' = f'g + fg'$ |
| **연쇄** | $(f(g(x)))' = f'(g(x))\,g'(x)$ — 역전파가 세워진 그 규칙 |
| 지수/로그 | $(e^x)' = e^x$, $(\ln x)' = 1/x$ |

- **편미분** $\partial f/\partial x_i$: 한 변수로만 미분하고 나머지는 고정. 좌표 $i$ 방향
  단위벡터를 $e_i$라 하면
  $$\frac{\partial f}{\partial x_i}(x) = \lim_{h\to 0}\frac{f(x + h\,e_i) - f(x)}{h}$$
  이므로 축 하나를 따라가는 보통의 도함수다. **그래디언트**
  $\nabla f = (\partial f/\partial x_1, \ldots, \partial f/\partial x_n)$는 그 $n$개를 벡터로
  쌓은 것이다. 작은 스텝 $\delta$에 대한 $f$의 변화가 약 $\nabla f^\top \delta = \sum_i (\partial f/\partial x_i)\,\delta_i$
  — 편미분마다 제 몫의 스텝을 곱해 더한 것이고, $^\top$은 §4의 전치다 — 이고 이 값은
  $\delta$가 $\nabla f$와 같은 방향일 때 가장 크므로, 그래디언트는 가장 가파르게 증가하는
  방향을 가리킨다. 그래서 경사 *하강*은 반대로 간다.
- 계산 예제 (모든 손실-그래디언트 계산의 원형. *손실*은 모델이 얼마나 틀렸는지를 매기는 숫자
  하나다, [[02-foundations/neural-network-basics|0.8 §3]]):
  $f(x, y) = (xy - 3)^2$ ⇒ $\partial f/\partial x = 2(xy-3)\cdot y$ — 바깥 미분 × 안쪽
  미분, 연쇄 법칙의 실전. **$(x,y) = (2,1)$에서 값을 넣어 보면:** 안쪽이 $xy - 3 = -1$이므로
  $\partial f/\partial x = 2(-1)(1) = -2$, $\partial f/\partial y = 2(-1)(2) = -4$, 즉
  $\nabla f = (-2, -4)$다. 답을 읽어보자: 두 성분이 모두 음수이므로 어느 변수든 *키우면*
  손실이 줄어든다 — $xy = 2$가 아직 목표 $3$에 못 미치니 맞는 말이다. 그리고
  $|{-4}| > |{-2}|$는 여기서 $y$가 더 효과적인 손잡이라는 뜻인데, $y$에 곱해지는 $x$가 더 크기
  때문이다. 경사 하강은 $-\alpha(-2,-4)$만큼 움직인다: 둘 다 올리되 $y$를 두 배 세게. 이 위키의
  모든 손실 그래디언트가 인덱스만 더 많은 이 계산이다.

<svg viewBox="0 0 560 366" style="max-width:100%;height:auto" role="img" aria-label="0.5에서 3.5까지의 정사각형 위 f = (xy - 3)의 제곱의 등고선: 굵은 쌍곡선이 영점 집합 xy = 3이고, xy = 2.5와 3.5(f = 0.25), 2와 4(f = 1), 1과 5(f = 4)가 쌍으로 그려진다. f = 1 곡선 위의 A = (2, 1)에서 10분의 1 길이로 그린 그래디언트 (-2, -4)는 곡선에 수직이고 xy = 3에서 멀어지는 쪽을 가리킨다. 그 반대로 0.1배 만큼의 스텝 (0.2, 0.4)가 f = 0.0064인 B = (2.2, 1.4)로 옮긴다.">
  <defs><marker id="emGrk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="60" y="40" width="300" height="300" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
  <polyline points="60,190 61.7,196.5 63.4,202.6 65.1,208.4 66.7,213.8 68.4,218.8 70.1,223.6 71.8,228.2 73.5,232.5 75.2,236.6 76.9,240.4 78.5,244.1 80.2,247.6 81.9,250.9 83.6,254.1 85.3,257.2 87,260.1 88.7,262.9 90.3,265.5 92,268.1 93.7,270.5 95.4,272.9 97.1,275.2 98.8,277.3 100.4,279.4 102.1,281.5 103.8,283.4 105.5,285.3 107.2,287.1 108.9,288.9 110.6,290.6 112.2,292.2 113.9,293.8 115.6,295.3 117.3,296.8 119,298.2 120.7,299.6 122.4,301 124,302.3 125.7,303.6 127.4,304.8 129.1,306 130.8,307.2 132.5,308.3 134.2,309.5 135.8,310.5 137.5,311.6 139.2,312.6 140.9,313.6 142.6,314.6 144.3,315.5 146,316.4 147.6,317.3 149.3,318.2 151,319.1 152.7,319.9 154.4,320.7 156.1,321.5 157.8,322.3 159.4,323.1 161.1,323.8 162.8,324.6 164.5,325.3 166.2,326 167.9,326.7 169.6,327.3 171.2,328 172.9,328.6 174.6,329.2 176.3,329.9 178,330.5 179.7,331.1 181.3,331.6 183,332.2 184.7,332.8 186.4,333.3 188.1,333.8 189.8,334.4 191.5,334.9 193.1,335.4 194.8,335.9 196.5,336.4 198.2,336.9 199.9,337.3 201.6,337.8 203.3,338.3 204.9,338.7 206.6,339.1 208.3,339.6 210,340" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <polyline points="152.9,40 155.2,45.6 157.5,51 159.8,56.3 162.2,61.4 164.5,66.4 166.8,71.2 169.1,75.8 171.5,80.4 173.8,84.8 176.1,89 178.5,93.2 180.8,97.2 183.1,101.2 185.4,105 187.8,108.7 190.1,112.4 192.4,115.9 194.8,119.4 197.1,122.7 199.4,126 201.7,129.2 204.1,132.3 206.4,135.4 208.7,138.4 211,141.3 213.4,144.1 215.7,146.9 218,149.6 220.4,152.3 222.7,154.9 225,157.5 227.3,159.9 229.7,162.4 232,164.8 234.3,167.1 236.6,169.4 239,171.6 241.3,173.8 243.6,176 246,178.1 248.3,180.2 250.6,182.2 252.9,184.2 255.3,186.1 257.6,188.1 259.9,189.9 262.2,191.8 264.6,193.6 266.9,195.4 269.2,197.1 271.6,198.8 273.9,200.5 276.2,202.2 278.5,203.8 280.9,205.4 283.2,207 285.5,208.5 287.8,210 290.2,211.5 292.5,213 294.8,214.5 297.2,215.9 299.5,217.3 301.8,218.7 304.1,220 306.5,221.3 308.8,222.7 311.1,224 313.5,225.2 315.8,226.5 318.1,227.7 320.4,228.9 322.8,230.1 325.1,231.3 327.4,232.5 329.7,233.6 332.1,234.8 334.4,235.9 336.7,237 339.1,238 341.4,239.1 343.7,240.2 346,241.2 348.4,242.2 350.7,243.2 353,244.2 355.3,245.2 357.7,246.2 360,247.1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <polyline points="67.1,40 70.4,59.1 73.7,76.1 77,91.6 80.3,105.5 83.6,118.2 86.9,129.9 90.2,140.6 93.5,150.4 96.8,159.5 100,167.9 103.3,175.7 106.6,183 109.9,189.8 113.2,196.2 116.5,202.2 119.8,207.8 123.1,213.1 126.4,218.1 129.7,222.9 133,227.3 136.2,231.6 139.5,235.6 142.8,239.4 146.1,243.1 149.4,246.5 152.7,249.8 156,253 159.3,256 162.6,258.9 165.9,261.7 169.1,264.3 172.4,266.9 175.7,269.3 179,271.7 182.3,273.9 185.6,276.1 188.9,278.2 192.2,280.2 195.5,282.2 198.8,284 202.1,285.9 205.3,287.6 208.6,289.3 211.9,291 215.2,292.5 218.5,294.1 221.8,295.6 225.1,297 228.4,298.4 231.7,299.8 235,301.1 238.3,302.4 241.5,303.6 244.8,304.8 248.1,306 251.4,307.2 254.7,308.3 258,309.4 261.3,310.4 264.6,311.4 267.9,312.4 271.2,313.4 274.4,314.4 277.7,315.3 281,316.2 284.3,317.1 287.6,318 290.9,318.8 294.2,319.6 297.5,320.4 300.8,321.2 304.1,322 307.4,322.7 310.6,323.5 313.9,324.2 317.2,324.9 320.5,325.6 323.8,326.3 327.1,326.9 330.4,327.6 333.7,328.2 337,328.8 340.3,329.4 343.5,330 346.8,330.6 350.1,331.2 353.4,331.8 356.7,332.3 360,332.9" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
  <polyline points="124.3,40 126.9,47.9 129.6,55.5 132.2,62.8 134.9,69.7 137.5,76.3 140.2,82.7 142.8,88.9 145.5,94.7 148.1,100.4 150.8,105.8 153.4,111.1 156.1,116.2 158.7,121 161.4,125.7 164,130.3 166.7,134.7 169.3,138.9 172,143 174.6,147 177.3,150.8 179.9,154.6 182.6,158.2 185.2,161.7 187.8,165.1 190.5,168.4 193.1,171.6 195.8,174.7 198.4,177.7 201.1,180.7 203.7,183.5 206.4,186.3 209,189 211.7,191.7 214.3,194.2 217,196.7 219.6,199.2 222.3,201.6 224.9,203.9 227.6,206.2 230.2,208.4 232.9,210.5 235.5,212.6 238.2,214.7 240.8,216.7 243.5,218.7 246.1,220.6 248.8,222.5 251.4,224.3 254.1,226.1 256.7,227.9 259.4,229.6 262,231.3 264.7,232.9 267.3,234.5 270,236.1 272.6,237.7 275.2,239.2 277.9,240.7 280.5,242.2 283.2,243.6 285.8,245 288.5,246.4 291.1,247.7 293.8,249 296.4,250.4 299.1,251.6 301.7,252.9 304.4,254.1 307,255.3 309.7,256.5 312.3,257.7 315,258.8 317.6,260 320.3,261.1 322.9,262.2 325.6,263.2 328.2,264.3 330.9,265.3 333.5,266.4 336.2,267.4 338.8,268.4 341.5,269.3 344.1,270.3 346.8,271.2 349.4,272.1 352.1,273.1 354.7,274 357.4,274.8 360,275.7" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
  <polyline points="81.4,40 84.6,54.7 87.7,68.2 90.8,80.7 93.9,92.2 97.1,102.9 100.2,112.9 103.3,122.2 106.5,130.8 109.6,139 112.7,146.6 115.9,153.8 119,160.6 122.1,167 125.2,173.1 128.4,178.8 131.5,184.3 134.6,189.4 137.8,194.3 140.9,199 144,203.5 147.2,207.7 150.3,211.8 153.4,215.7 156.5,219.4 159.7,223 162.8,226.4 165.9,229.7 169.1,232.8 172.2,235.9 175.3,238.8 178.5,241.6 181.6,244.3 184.7,246.9 187.8,249.4 191,251.9 194.1,254.2 197.2,256.5 200.4,258.7 203.5,260.8 206.6,262.9 209.8,264.8 212.9,266.8 216,268.7 219.1,270.5 222.3,272.2 225.4,273.9 228.5,275.6 231.7,277.2 234.8,278.8 237.9,280.3 241.1,281.8 244.2,283.2 247.3,284.7 250.4,286 253.6,287.4 256.7,288.7 259.8,289.9 263,291.2 266.1,292.4 269.2,293.6 272.4,294.7 275.5,295.8 278.6,296.9 281.7,298 284.9,299.1 288,300.1 291.1,301.1 294.3,302.1 297.4,303 300.5,304 303.7,304.9 306.8,305.8 309.9,306.6 313,307.5 316.2,308.3 319.3,309.2 322.4,310 325.6,310.8 328.7,311.6 331.8,312.3 335,313.1 338.1,313.8 341.2,314.5 344.3,315.2 347.5,315.9 350.6,316.6 353.7,317.3 356.9,317.9 360,318.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <polyline points="110,40 112.8,49.6 115.6,58.6 118.4,67.2 121.2,75.4 124,83.1 126.9,90.5 129.7,97.5 132.5,104.2 135.3,110.6 138.1,116.8 140.9,122.6 143.7,128.2 146.5,133.6 149.3,138.8 152.1,143.8 154.9,148.5 157.8,153.1 160.6,157.5 163.4,161.8 166.2,165.9 169,169.9 171.8,173.7 174.6,177.4 177.4,180.9 180.2,184.4 183,187.7 185.8,191 188.7,194.1 191.5,197.1 194.3,200.1 197.1,202.9 199.9,205.7 202.7,208.4 205.5,211 208.3,213.5 211.1,216 213.9,218.4 216.7,220.7 219.6,223 222.4,225.2 225.2,227.3 228,229.4 230.8,231.5 233.6,233.5 236.4,235.4 239.2,237.3 242,239.2 244.8,241 247.6,242.7 250.4,244.4 253.3,246.1 256.1,247.8 258.9,249.4 261.7,250.9 264.5,252.5 267.3,254 270.1,255.4 272.9,256.9 275.7,258.3 278.5,259.7 281.3,261 284.2,262.3 287,263.6 289.8,264.9 292.6,266.1 295.4,267.4 298.2,268.6 301,269.7 303.8,270.9 306.6,272 309.4,273.1 312.2,274.2 315.1,275.3 317.9,276.3 320.7,277.3 323.5,278.4 326.3,279.3 329.1,280.3 331.9,281.3 334.7,282.2 337.5,283.1 340.3,284 343.1,284.9 346,285.8 348.8,286.7 351.6,287.5 354.4,288.4 357.2,289.2 360,290" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <polyline points="95.7,40 98.7,51.7 101.7,62.7 104.6,73 107.6,82.6 110.6,91.7 113.5,100.2 116.5,108.3 119.5,116 122.4,123.2 125.4,130.1 128.4,136.6 131.3,142.8 134.3,148.7 137.3,154.3 140.3,159.7 143.2,164.8 146.2,169.7 149.2,174.4 152.1,178.9 155.1,183.3 158.1,187.4 161,191.4 164,195.2 167,198.9 170,202.4 172.9,205.9 175.9,209.2 178.9,212.3 181.8,215.4 184.8,218.4 187.8,221.2 190.7,224 193.7,226.7 196.7,229.3 199.6,231.8 202.6,234.2 205.6,236.6 208.6,238.9 211.5,241.1 214.5,243.3 217.5,245.4 220.4,247.4 223.4,249.4 226.4,251.4 229.3,253.2 232.3,255.1 235.3,256.8 238.3,258.6 241.2,260.3 244.2,261.9 247.2,263.5 250.1,265.1 253.1,266.6 256.1,268.1 259,269.5 262,271 265,272.3 267.9,273.7 270.9,275 273.9,276.3 276.9,277.6 279.8,278.8 282.8,280 285.8,281.2 288.7,282.4 291.7,283.5 294.7,284.6 297.6,285.7 300.6,286.8 303.6,287.8 306.5,288.8 309.5,289.8 312.5,290.8 315.5,291.8 318.4,292.7 321.4,293.7 324.4,294.6 327.3,295.5 330.3,296.3 333.3,297.2 336.2,298 339.2,298.9 342.2,299.7 345.2,300.5 348.1,301.3 351.1,302 354.1,302.8 357,303.6 360,304.3" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <polyline points="110,340 110,344" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="356" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="56,290 60,290" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="294" font-size="11" text-anchor="end" fill="currentColor">1</text>
  <polyline points="210,340 210,344" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="210" y="356" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <polyline points="56,190 60,190" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="194" font-size="11" text-anchor="end" fill="currentColor">2</text>
  <polyline points="310,340 310,344" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="356" font-size="11" text-anchor="middle" fill="currentColor">3</text>
  <polyline points="56,90 60,90" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="94" font-size="11" text-anchor="end" fill="currentColor">3</text>
  <text x="368" y="344" font-size="11" fill="currentColor">x</text>
  <text x="52" y="44" font-size="11" text-anchor="end" fill="currentColor">y</text>
  <polyline points="210,290 190.2,329.6" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emGrk)"/>
  <polyline points="210,290 228.6,252.9" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#emGrk)"/>
  <polyline points="213.1,283.7 219.4,286.9 216.3,293.1" fill="none" stroke="currentColor" stroke-width="0.9"/>
  <circle cx="210" cy="290" r="3.2" fill="currentColor"/>
  <circle cx="230" cy="250" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="219" y="310" font-size="12" fill="currentColor">A</text>
  <text x="214" y="242" font-size="12" fill="currentColor">B</text>
  <text x="376" y="44" font-size="12" fill="currentColor">f(x, y) = (xy − 3)<tspan dy="-5" font-size="10">2</tspan></text>
  <polyline points="376,66 402,66" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <text x="408" y="70" font-size="11" fill="currentColor">f = 0: xy = 3</text>
  <polyline points="376,86 402,86" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <text x="408" y="90" font-size="11" fill="currentColor">f = 0.25</text>
  <polyline points="376,106 402,106" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
  <text x="408" y="110" font-size="11" fill="currentColor">f = 1</text>
  <polyline points="376,126 402,126" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <text x="408" y="130" font-size="11" fill="currentColor">f = 4</text>
  <polyline points="376,146 401,146" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emGrk)"/>
  <text x="408" y="150" font-size="11" fill="currentColor">A의 ∇f (0.1배로 그림)</text>
  <polyline points="376,166 399,166" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#emGrk)"/>
  <text x="408" y="170" font-size="11" fill="currentColor">스텝 하나 −0.1∇f</text>
  <circle cx="389" cy="186" r="3.2" fill="currentColor"/>
  <text x="408" y="190" font-size="11" fill="currentColor">A (2, 1): f = 1</text>
  <circle cx="389" cy="206" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="408" y="210" font-size="11" fill="currentColor">B (2.2, 1.4): f = 0.0064</text>
</svg>

$[0.5,3.5]^2$ 위 $f(x,y)=(xy-3)^2$의 등고선이다. 굵은 곡선이 영점 집합 $xy=3$이고, 나머지 등고선은 저마다 쌍곡선 한 쌍 $xy=3\pm\sqrt f$다. $f=1$ 등고선 위의 $A=(2,1)$에서 그래디언트 $\nabla f=(-2,-4)$(길이의 10분의 1로 그렸다)는 그 등고선에 수직이고, $xy=3$에서 멀어지는 오르막을 가리킨다. $\alpha=0.1$인 경사 하강 한 스텝은 그 반대로 $(0.2,\,0.4)$ — $y$를 $x$의 두 배 — 만큼 움직여 $f=0.0064$인 $B=(2.2,\,1.4)$에 닿는다.

### 2. 테일러 전개 (→ 2. 미적분, 4. 최적화)

최적화기는 함수 전체를 보지 못하고, 스텝마다 지금 선 자리의 값과 도함수 몇 개만 가지고 한 걸음 앞을 짐작해야 한다. 테일러 전개가 그 짐작이고, 그 짐작을 얼마나 멀리까지 믿어도 되는지도 함께 말해 준다.

$$f(x + \delta) \approx f(x) + f'(x)\,\delta + \tfrac12 f''(x)\,\delta^2$$

"매끄러운 함수는 국소적으로 직선(1차)이거나 포물선(2차)이다." 경사 하강은 직선을 믿고,
뉴턴법은 포물선을 믿는다.

**테일러 전개**는 한 점 근처의 함수를 그 점*에서의* 도함수로 만든 다항식으로 근사한다. 식에서
$x$는 전개점, $\delta$는 거기서 떨어진 스텝, $f'(x)$와 $f''(x)$는 그 점의 1차·2차 도함수다.
근사는 국소적일 뿐이다. $f$가 연속인 3차 도함수를 가지면 2차 근사의 오차는 $\delta^3$처럼
줄어들어, 스텝을 반으로 줄이면 오차가 약 8분의 1이 된다. 최적화가 쓰는 다변수판은 $f'$ 대신
그래디언트, $f''$ 대신 2차 도함수의 행렬인 헤시안 $H$를 쓴다.
$$f(x + \delta) \approx f(x) + \nabla f(x)^\top \delta + \tfrac12\,\delta^\top H(x)\,\delta$$
이제 $\delta$는 벡터이고, $\delta^\top H \delta$는
[[02-foundations/linear-algebra|1. 선형대수 §3]]에서 읽는 이차형식이다.

**검산.** $f = x^2$, $x=1$에서: $f(1+\delta) = 1 + 2\delta + \delta^2$ — 정확히 맞다,
$x^2$ 자체가 포물선이니까.

**실제 숫자로 하는 계산 예제** — 계산기 없이 $\sqrt{4.1}$을 추정해 보자. $f(x) = \sqrt{x}$를
답을 이미 아는 지점 $x = 4$ 주위로 전개한다. 도함수 둘이 필요하다: $f'(x) = \frac{1}{2\sqrt x}$이니
$f'(4) = \frac{1}{4} = 0.25$, 그리고 $f''(x) = -\frac{1}{4x^{3/2}}$이니
$f''(4) = -\frac{1}{32} = -0.03125$. $\delta = 0.1$로 두면:

| 차수 | 계산 | 결과 | 오차 |
|---|---|---|---|
| 0차 | $2$ | 2 | $2.5\times10^{-2}$ |
| 1차 | $2 + 0.25(0.1)$ | 2.025 | $1.5\times10^{-4}$ |
| 2차 | $2.025 + \tfrac12(-0.03125)(0.1)^2$ | 2.02484375 | $1.9\times10^{-6}$ |

(참값 $\sqrt{4.1} = 2.0248456\ldots$) 차수를 하나 올릴 때마다 도함수 하나를 더 치르고,
*작은 스텝에 한해* 소수점 두 자리쯤을 더 얻는다. 이 거래가 곧
[[02-foundations/optimization|4. 최적화 §3]]에서 경사 하강과 뉴턴법이 벌이는 논쟁 전부다:
뉴턴법은 2차 도함수로 훨씬 나은 스텝을 밟고, 그 대가로 스텝당 $O(n^3)$을 낸다 — $n\times n$ 선형계를 푸는 비용이다(표기는 [[02-foundations/algorithms/complexity-recursion|11.1 §2]]).

**외워둘 만한 1차 전개 둘** — 논문이 말없이 쓴다: 작은 $\delta$에 대해
$e^\delta \approx 1 + \delta$, $\log(1+\delta) \approx \delta$. ($\delta = 0.01$에서 검산:
$e^{0.01} = 1.01005$, $\log(1.01) = 0.00995$.) 유도 중에 "작은 $\epsilon$에 대해 이것은
근사적으로…"가 나오면 십중팔구 이 일이 벌어진 것이다.

### 3. 적분과 기댓값 (→ 3. 확률)

확률 페이지는 어떤 양을 모든 결과에 걸쳐 평균하는데(데이터 전체의 기대 손실, 정책의 기대 리턴, 잡음 섞인 거리 측정의 평균), 결과가 연속으로 이어져 있으면 그 평균이 적분이다. 이 절은 적분을 합으로 읽는 법부터 말하고, 기초 페이지가 쓰는 단 하나의 패턴인 기댓값에 그것을 쓴다.

- 적분은 **연속 극한**(continuum limit)의 가중합이다 — 축을 조각으로 자르고, 각 $f$ 값에
  조각의 폭을 곱해 더한 뒤, 조각의 폭을 0으로 보낸 것. "연속 극한"은 언제나 이 뜻이다:
  더하는 단위를 끝까지 무한소로 내려보낸 합. 그 합을 $\int f(x)\,dx$로 쓴다. 식으로 쓰면
  (리만 합), 구간 $[a, b]$를 같은 폭의 조각 $N$개로 자를 때
  $$\int_a^b f(x)\,dx = \lim_{N\to\infty} \sum_{i=0}^{N-1} f(x_i)\,\Delta x, \qquad \Delta x = \frac{b-a}{N},\quad x_i = a + i\,\Delta x$$
  이다. $\Delta x$는 조각 폭, $x_i$는 조각 $i$의 왼쪽 끝이다. 연속인 $f$라면 이 극한이 항상
  존재하므로 처음에 얼마나 잘게 잘랐는지와 답이 무관하다. 예: $\int_0^1 x\,dx$는 $N = 10$이면
  $0.45$, $N = 100$이면 $0.495$, $N = 1000$이면 $0.4995$로 정확한 값 $\tfrac12$에 다가간다.
- 기초 페이지들이 실제로 쓰는 적분 패턴은 사실상 하나, **기댓값**이다. 확률변수 $X$의 어떤 양
  $g(X)$를 확률로 가중해 평균한 값이다. 숫자 하나이고, $X$가 확률 $p(x)$를 갖는 이산값이면 합으로,
  밀도 $p(x)$를 가지면 적분으로 계산한다.
  $$E[g(X)] = \sum_x g(x)\,p(x) \qquad\text{or}\qquad E[g(X)] = \int g(x)\,p(x)\,dx$$
  — "분포 $p$ 위에서 $g$의 평균." 합이므로 선형이다: $E[aX + bY] = aE[X] + bE[Y]$ (§4.5).
  **구체적으로, 세 가지 방식:**
  - *이산 — 그래서 "가중합"이 말 그대로다.* 공정한 주사위:
    $E[X] = \sum_x x\,p(x) = 1(\tfrac16) + 2(\tfrac16) + \cdots + 6(\tfrac16) = \tfrac{21}{6} = 3.5$.
    각 값에 그 값이 나오는 빈도를 가중한 것이다. 적분은 이 합을 연속 극한으로 보낸 것이다.
  - *연속 — 손으로 계산.* $X$가 $[0,1]$에서 균등하면 그 구간에서 $p(x) = 1$이므로
    $E[X] = \int_0^1 x\cdot 1\,dx = \big[\tfrac{x^2}{2}\big]_0^1 = \tfrac12$,
    $E[X^2] = \int_0^1 x^2\,dx = \tfrac13$. $E[X^2] = \tfrac13$이 $(E[X])^2 = \tfrac14$과
    다르다는 점에 주목하라 — 그 차이가 곧 분산이다: $\tfrac13 - \tfrac14 = \tfrac{1}{12}$
    ([[02-foundations/probability|3. 확률 §2]]).
  - *코드에서는 흔히 샘플 평균.* 기댓값을 해석적으로 합하거나 적분하지 못할 때 $N$개를 뽑아
    평균 낸다: $E[g(X)] \approx \frac1N\sum_{i=1}^N g(x_i)$. 유한 이산분포는 정확히 합할 수 있고,
    어떤 모델은 해석적 적분이나 동적계획법도 가능하다. 그래도 많은 기대 손실과 리턴은 표본으로
    추정하므로 표본 불확실성을 보고한다([[02-foundations/ml-practice|9. ML 실무 §4]]).
- $\int p(x)\,dx = 1$ (확률의 합은 1) — 증명의 절반에 쓰이는 항등식이다
  (예: [[02-foundations/information-theory|5. 정보이론]]의 KL 비음수성).

### 4. 행렬 연산 (→ 1. 선형대수의 입장 조건)

로봇 팔은 관절 속도를 행렬 하나로 끝점 속도로 바꾸고 신경망의 층은 특징 512개를 또 다른 행렬로 점수 10개로 바꾸는데, 둘 다 행렬 곱하기 벡터라서 코드에서 가장 먼저 깨지는 것은 맞지 않는 모양이다. 이 절은 1. 선형대수가 전제하는 산수를 규칙마다 한 번씩 손으로 계산해 둔다.

- $(AB)_{ij} = \sum_k A_{ik}B_{kj}$: **$A$의 $i$행과 $B$의 $j$열의 내적.** 모양:
  $(m\times n)(n \times p) = m \times p$ — 안쪽 차원이 맞아야 하고, 맞으면 사라진다.
- **한 성분을 천천히 계산해 보면.**
  $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $B = \begin{pmatrix}0&1\\1&0\end{pmatrix}$일 때
  $(AB)_{11}$은 $A$의 1행 $(1, 2)$와 $B$의 1열 $(0, 1)$의 내적이므로
  $(AB)_{11} = 1(0) + 2(1) = 2$. 나머지 셋도 같은 방식으로 하면
  $AB = \begin{pmatrix}2&1\\4&3\end{pmatrix}$ — $A$의 **열**이 서로 바뀐 것이다.
- **순서가 왜 중요한지, 단정이 아니라 눈으로.** 반대로 곱해 보면
  $BA = \begin{pmatrix}3&4\\1&2\end{pmatrix}$ — 이번엔 $A$의 **행**이 바뀌었다. 같은 두 행렬,
  다른 답이고, 이제 *왜*인지 보인다: 오른쪽에서 곱하면 열에 작용하고, 왼쪽에서 곱하면 행에
  작용한다. 이 비대칭이 $W_2W_1x$와 $W_1W_2x$가 서로 다른 신경망인 이유이고,
  [[02-foundations/se3-geometry|SE(3)]]에서 프레임 순서가 중요한 이유($R_1R_2 \ne R_2R_1$)다.
- **전치**: 대각선 기준으로 뒤집기, $A^\top_{ij} = A_{ji}$. 위의 $A$라면
  $A^\top = \begin{pmatrix}1&3\\2&4\end{pmatrix}$. 곱의 순서를 뒤집는다:
  $(AB)^\top = B^\top A^\top$. 위에서 $(AB)^\top = \begin{pmatrix}2&4\\1&3\end{pmatrix}$이고
  $B^\top A^\top$도 같다. **항등 행렬** $I$는 대각선이 $1$, 나머지가 $0$, 즉 $i = j$이면
  $I_{ij} = 1$, 아니면 $0$이므로 $AI = IA = A$다. 아무것도 바꾸지 않는다.
- **행렬식**: 정방 행렬에 붙는 숫자 하나. $2\times2$ 행렬 $\begin{pmatrix}a&b\\c&d\end{pmatrix}$에서는
  $\det A = ad - bc$이고, $|\det A|$는 사상이 넓이(고차원에서는 부피)를 몇 배로 만드는지, 음의
  부호는 방향이 뒤집힌다는 뜻이다. 위의 $A$는 $\det A = 1(4) - 2(3) = -2$이므로 넓이를 두 배로
  만들고 거울상으로 뒤집는다. 중요한 결과: $\det A \ne 0$일 때와 $A$가 가역일 때가 정확히 같다.
- **역행렬, 숫자와 함께.** $A^{-1}$은 $A$를 어느 쪽에서든 되돌리고($A^{-1}A = AA^{-1} = I$),
  정방·**풀랭크**일 때만(동치로 $\det A \ne 0$일 때만) 존재한다. $2\times2$에서는
  $A^{-1} = \frac{1}{\det A}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$, $\det A = ad - bc$.
  위의 $A$는 $\det A = 1(4) - 2(3) = -2 \ne 0$이므로
  $A^{-1} = -\tfrac12\begin{pmatrix}4&-2\\-3&1\end{pmatrix} = \begin{pmatrix}-2&1\\1.5&-0.5\end{pmatrix}$.
  $AA^{-1}$의 첫 성분으로 검산: $1(-2) + 2(1.5) = 1$ ✓.
- **"풀랭크"가 배제하는 것, 구체적으로.** $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$를 보자.
  둘째 열이 첫째 열의 정확히 $2$배라서, $C$는 평면 전체를 직선 하나 위로 보낸다 — 수직
  방향에 대한 정보가 통째로 사라진다. 일관되게 $\det C = 1(4) - 2(2) = 0$이고, 역행렬 공식은
  0으로 나눈다: **되돌아갈 곳이 없다.** 이것이 랭크 부족이고, 랭크의 정식 정의는
  [[02-foundations/linear-algebra|1. 선형대수 §2]]에 있다. 여기서는 "풀랭크" = "잃어버린 것이
  없어 되돌릴 수 있다"로 읽으면 된다.
- **앞으로 끊임없이 하게 될 모양 검사.** 특징 512개에서 클래스 점수 10개로 가는 선형 층 — 신경망의
  행렬 한 단계, [[02-foundations/neural-network-basics|0.8 §1]] — 은
  $x$가 $512\times1$ 열인 $y = Wx$이므로, $W$는 $10\times512$여야 하고
  $(10\times512)(512\times1) = 10\times1$ — 클래스마다 점수 하나다. 샘플 32개 — 함께 통과시키는
  입력 묶음인 배치, [[02-foundations/neural-network-basics|0.8 §4]] — 를 $X$의 열로 쌓은 것($512\times32$)은
  곱 한 번으로 지나간다:
  $(10\times512)(512\times32) = 10\times32$ — 샘플마다 점수 열 하나. 0.8과 2 페이지가 쓰는
  것이 이 열벡터 관례다. 이렇게 모양을 읽는 것이 곧 아키텍처를 읽는 것이다
  ([[02-foundations/linear-algebra|1. 선형대수 §1]]).
  *코드를 위한 각주.* 라이브러리와 어텐션 식은 보통 배치를 행으로 저장한다: $X$는
  $32\times512$, 층의 행렬은 전치($512\times10$)로 두고, 출력 $XW$는 $32\times10$ — 위의
  $(AB)^\top = B^\top A^\top$에 따라 같은 숫자를 전치한 것이다. 1. 선형대수 §1 끝의 접힌 상자에 나오는
  어텐션 투영 $Q = XW_Q$가 이렇게 쓰여 있다.

### 4.5 선형성: 가법성과 동차성 (→ 1. 선형대수, 6. 신호처리, 제어 트랙)

"선형"은 이 위키에서 가장 자주 쓰는 말이고, 뜻이 정확히 정해져 있다. 사상 $f$(함수, 행렬, 시스템, 연산자)가 모든 입력 $x, y$와 모든 스칼라 $a$에 대해 **두** 조건을 만족하면 **선형**이다.

- **가법성(additivity)**: 입력을 먼저 더한 결과가 출력을 더한 결과와 같다.
$$f(x + y) = f(x) + f(y)$$
- **동차성(homogeneity, 1차)**: 입력을 몇 배 하면 출력도 같은 배수만큼 커진다.
$$f(a x) = a\,f(x)$$

둘을 합친 것이 중첩 원리(**superposition principle**)이다. 입력의 가중합을 항마다 나눌 수 있으므로 한 줄로 쓴다.
$$f(a x + b y) = a\,f(x) + b\,f(y)$$
이를 되풀이하면 유한합에 대해 $f\big(\sum_k a_k x_k\big) = \sum_k a_k f(x_k)$가 된다. 복잡한 입력에 대한 응답은 단순한 조각들의 응답을 더한 것이다. 선형 시스템을 다루기 쉬운 이유가 바로 이 결과다. 기저 입력 몇 개의 응답만 재면 모든 입력의 응답을 안다.

**두 조건을 모두 적는 이유.** 가법성만으로도 모든 유리수 $q$에 대해 $f(qx) = q f(x)$가 나온다($x + x + \dots$에 적용). 하지만 $f$가 연속이라는 조건이 없으면 모든 실수 $a$로는 넓혀지지 않는다. 동차성을 따로 적으면 그 틈이 닫히므로 교과서는 두 조건을 모두 쓴다.

> [!example] 계산 예제 · Worked example
> **행렬은 선형이다.** $W = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $x = (1,0)$, $y = (0,1)$, $a = 2$, $b = 3$이면 $W(2x + 3y) = W(2,3) = (8, 18)$이고 $2Wx + 3Wy = 2(1,3) + 3(2,4) = (8, 18)$이다. 행렬곱의 분배법칙이 모든 입력에서 이를 보장한다.
>
> **$f(x) = 2x + 1$은 선형이 아니다.** 그래프가 직선인데도 그렇다. 가법성: $f(1 + 2) = 7$이지만 $f(1) + f(2) = 3 + 5 = 8$. 동차성: $f(2 \cdot 1) = 5$이지만 $2 f(1) = 6$. 빠른 판별법은 $f(0)$이다. 선형 사상은 $a = 0$을 넣으면 알 수 있듯 항상 $0$을 $0$으로 보내는데, 여기서는 $f(0) = 1$이다. 절편이 있는 직선은 선형이 아니라 아핀(**affine**)이다.
>
> **$f(x) = x^2$은 선형이 아니다**: $f(1 + 1) = 4$이지만 $f(1) + f(1) = 2$.
>
> **ReLU $f(x) = \max(0, x)$는 선형이 아니다**: $f(-1 + 1) = 0$이지만 $f(-1) + f(1) = 0 + 1 = 1$. 동차성도 $a \ge 0$일 때만 성립한다. $f(-1 \cdot 1) = 0 \ne -f(1) = -1$이기 때문이다.

**위키에서 쓰이는 곳.**
- **행렬과 층.** 모든 행렬은 선형 사상이다([[02-foundations/linear-algebra|1. 선형대수 §1]]). "선형층" $Wx + b$는 엄밀히는 아핀이고 $b = 0$일 때만 선형이다. 선형 사상을 쌓으면 하나로 접히므로 신경망은 층 사이에 비선형성이 필요하다([[02-foundations/neural-network-basics|0.8 §1]]).
- **연산자.** 미분, 적분, 기댓값은 선형이다: $\frac{d}{dt}(af + bg) = a f' + b g'$, $E[aX + bY] = aE[X] + bE[Y]$ (§1, §3, [[02-foundations/probability|3. 확률]]).
- **시스템.** 선형 시불변 시스템은 입력 신호에 대해 가법적이고 동차적이며, 시간 이동에도 불변이다. 중첩 원리가 바로 그 출력을 합성곱으로 만든다([[02-foundations/signal-processing|6. 신호처리 §1]]).
- **선형화.** 비선형 $f$를 동작점 $x_0$ 근처에서 $f(x_0 + \delta) \approx f(x_0) + f'(x_0)\,\delta$로 바꾼다. 사상 $\delta \mapsto f'(x_0)\,\delta$는 편차 $\delta$에 대해 선형이고, 그래서 제어 설계가 국소적으로 작동한다(§2, [[04-robotics/control-theory-ce397|5. 제어 이론]]).

### 5. 급수와 기하급수 합 (→ 7. RL 기초)

**강화학습(RL)이 이것을 쓰는 이유.** $k$ 스텝 뒤의 보상은 가중치 $\gamma^k$로 세므로, 에이전트가 평생
모을 수 있는 가중치의 총합이 정확히 아래의 무한합이고, 아래 유도대로 그 값은 $1/(1-\gamma)$다.
$\gamma = 0.99$면 $100$ — 즉 할인 없는 100 스텝을 더하고 그 뒤는 무시하는 것과 대략 같게
행동한다. 반대편에서의 확인: $0.99^{100} \approx 0.37$이므로 100 스텝쯤이면 보상에 걸리는
가중치가 이미 3분의 1 수준으로 떨어져 있다. [[02-foundations/rl-basics|RL]]에서 말하는
"유효 지평 약 100 스텝"이 이 뜻이다.

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

### 6. 지수와 로그 (→ 5. 정보이론의 입장 조건)

서로 독립인 측정 천 개의 확률은 1보다 작은 수 천 개의 곱이다 — 하나하나가 $0.1$이면 $10^{-1000}$이고, float64는 이것을 정확히 $0$으로 반올림한다. 그 로그 $-2302.6$은 평범한 숫자인데, 로그가 곱을 합으로 바꾸기 때문이고, 이 위키의 모든 우도, 손실, 비트 수가 로그와 그 역함수인 지수로 쓰이는 이유도 그것이다.

- $e^x$: 자기 자신이 도함수인 함수; 자신에 비례하는 속도로 성장. ($e \approx 2.718$.)
  정확히는 두 성질을 함께 가진 유일한 함수다.
  $$\frac{d}{dx}e^x = e^x, \qquad e^0 = 1$$
  그리고 수 $e$는 복리 성장이 도달하는 값 $e = \lim_{n\to\infty}(1 + 1/n)^n$이다. $n = 1$이면
  $2$, $n = 10$이면 $2.594$, $n = 100$이면 $2.705$, $n = 1000$이면 $2.717$로 $2.71828$에
  다가간다. 동치로 $e^x = \sum_{k \ge 0} x^k/k!$이고, 항마다 미분하면 자기 자신이 된다.
- **밑이 뭔가?** $\ln$은 언제나 밑이 $e$다(*자연로그*, natural log의 n이다). $\log_2$는 밑이 2.
  밑 없는 $\log$는 보편적 약속이 없다: 이 위키와 대부분의 ML 논문에서는 밑이 $e$이고,
  정보이론에서만 단위가 **비트**라서 밑이 2다. 다행히 거의 문제가 되지 않는다 — 밑을 바꿔도
  전체에 상수가 곱해질 뿐이고(아래 셋째 규칙), 상수는 최솟값의 위치를 바꾸지 않는다.
- $\log$는 지수함수의 역함수: $\log(e^x) = x$. 밑 $b > 0$, $b \ne 1$에 대해
  $$y = \log_b x \iff b^y = x$$
  이므로 $\log_b x$는 "$x$를 얻으려고 $b$에 올리는 지수"다. $2^3 = 8$이므로 $\log_2 8 = 3$.
  양수 밑의 거듭제곱은 0이나 음수가 될 수 없으므로 $x > 0$에서만 정의된다. 관측된 사건에 확률
  $0$을 준 모델의 로그 우도가 $-\infty$인 이유다. 정보이론 전체와 모든 우도 계산을 떠받치는 세 규칙:

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
- **Log-sum-exp**: $\log \sum_i e^{x_i}$는 어디에나 나오며(점수를 확률로 바꾸는 softmax — §10에서
  정의 — 의 정규화 분모의 로그다), 식 그대로 계산하면 넘친다 — float64의 가장 큰 값이 약
  $1.8\times10^{308}=e^{709.8}$이라 $e^{800}$은 이미 $\infty$다(부동소수점이 수를 저장하는 방식은
  [[02-foundations/tools/python-research-code|12.3 §5]]). $x_{max} = \max_i x_i$로
  두면 해법은:

  $$\log \sum_i e^{x_i} = x_{max} + \log\sum_i e^{x_i - x_{max}}$$

  어디서 나왔나: 합에서 가장 큰 항을 묶어내면
  $\sum_i e^{x_i} = e^{x_{max}}\sum_i e^{x_i - x_{max}}$이고, 여기에 $\log$를 취한 뒤 위 표의
  $\log(ab) = \log a + \log b$를 쓴 것이다. 근사가 아니라 *정확한* 항등식이다. 왜 문제가
  풀리나: 이제 모든 지수 $x_i - x_{max}$가 $\le 0$이므로 각 $e^{(\cdot)}$가 $0$과 $1$ 사이에
  있다 — 이 정규화에서는 넘칠 수 없고, 가장 큰 항이 정확히 $1$이므로 합 전체가 0으로
  가라앉지도 않는다. 다른 잘못된 입력·극단 연산·별도 연산은 여전히 NaN(숫자가 아님을 뜻하는 값)을 만들 수 있지만,
  안정적인 softmax+교차 엔트로피 구현이 이 항등식을 쓰는 이유가 이것이다
  ([[02-foundations/calculus-backprop|2. 미적분 §4]]).

  *숫자로.* $x = (800, 799)$에서 $e^{800}$을 계산하면 넘치지만, 항등식은
  $800 + \log(1 + e^{-1}) = 800.3133$을 준다. log-sum-exp가 *무엇인지*도 보인다. 매끄러운
  최댓값으로, 성분이 $n$개면 항상 $\max_i x_i$와 $\max_i x_i + \log n$ 사이에 있다. 여기서는
  $800$과 $800.693$ 사이다.

### 7. 복소수와 오일러 공식 (→ 6. 신호처리의 입장 조건)

진동, 필터, 피드백 루프는 진동하는 입력에 무엇을 하는가로 기술되는데, 진동에는 숫자가 둘 딸려 있다 — 얼마나 큰가, 그리고 시간상 얼마나 밀렸는가. 복소수는 그 쌍을 숫자 하나에 담고 '키우고 미는' 일을 곱셈 한 번으로 만들기 때문에, 신호처리와 제어가 복소수로 쓰인다.

- $j = \sqrt{-1}$; 복소수 $a + jb$는 2차원 평면의 점(가로 $a$, 세로 $b$);
  $|a+jb| = \sqrt{a^2+b^2}$가 원점으로부터의 거리, 각도는 $\theta = \operatorname{atan2}(b, a)$.
  형식적으로는 실수 둘의 쌍, 즉 **실수부** $a$와 **허수부** $b$에 규칙 $j^2 = -1$ 하나를 더한
  것이다. 덧셈은 성분별이고, 곱셈은 괄호를 전개한 뒤 $j^2 = -1$을 쓴다. 같은 수의 **극형식**은
  $$a + jb = r\,e^{j\theta}, \qquad r = \sqrt{a^2 + b^2}, \quad \theta = \operatorname{atan2}(b, a)$$
  이다. $r$은 크기, $\theta$는 각도다($e^{j\theta}$는 아래의 오일러 공식). 그래서 복소수 둘을
  곱하면 크기는 곱해지고 각도는 더해진다. 예: $3 + 4j$는 $r = 5$, $\theta = 53.13°$.
  $(1 + j)^2 = 1 + 2j + j^2 = 2j$이고, 극형식으로 $1 + j$는 $r = \sqrt2$, $\theta = 45°$이므로
  제곱은 $r = 2$, $\theta = 90°$, 즉 $2j$다 ✓. **켤레** $\overline{a + jb} = a - jb$는 점을
  거울에 비추고, $z\bar z = |z|^2$이다.
- **atan2가 뭔가**: 인자가 둘인 아크탄젠트로, 어느 언어에나 있는 함수다
  (C·파이썬·NumPy·MATLAB의 `atan2(y, x)`). 두 좌표를 *따로* 받아서 점 $(x, y)$의 각도를
  원 전체 $(-\pi, \pi]$ 범위로 돌려준다. 풀어 쓰면, 점이 왼쪽에 있을 때마다 $\arctan$을 반 바퀴
  보정한다.
  $$\operatorname{atan2}(y, x) = \begin{cases} \arctan(y/x) & x > 0 \\ \arctan(y/x) + \pi & x < 0,\ y \ge 0 \\ \arctan(y/x) - \pi & x < 0,\ y < 0 \\ +\pi/2 & x = 0,\ y > 0 \\ -\pi/2 & x = 0,\ y < 0 \end{cases}$$
  $\arctan$ 혼자서는 $-90°$와 $90°$ 사이의 각만 돌려주므로 $x$의 부호가 보정 여부를 정한다
  ($\operatorname{atan2}(0, 0)$은 정의하지 않는다). $(x, y) = (-1, -1)$이면
  $\arctan(1) - \pi = 45° - 180° = -135°$다.
- **왜 $\arctan(b/a)$가 아닌가**: 먼저 나누는 순간 정보가 버려진다. $\arctan$은 $b/a$라는
  숫자 하나만 보는데, 어떤 점과 그 정반대 점의 비는 *똑같다*. 구체적으로 $(a,b) = (1,1)$과
  $(a,b) = (-1,-1)$은 둘 다 $b/a = 1$이라서 $\arctan$은 둘 다 $45°$를 준다 — 하지만 두 번째
  점은 3사분면의 $225°$($=-135°$)다. "사분면을 잃는다"가 이 뜻이다: 평면의 절반에서 답이
  정확히 $180°$만큼 틀리는데, $\arctan$에는 어느 절반이었는지 알 방법이 없다. 게다가
  $a = 0$에서 0으로 나누므로 깨지는데, 실제 각도는 지극히 평범한 $\pm 90°$다. `atan2`는 두
  부호를 모두 들고 있으므로 네 사분면과 수직축을 전부 맞힌다. 로보틱스에서 이것은 관절을
  앞으로 보내느냐 뒤로 보내느냐의 차이이고, 그래서 [[02-foundations/se3-geometry|SE(3)]]
  페이지와 모든 역기구학 구현이 atan2만 쓴다.

<svg viewBox="0 0 560 200" style="max-width:100%;height:auto" role="img" aria-label="원점을 지나는 같은 점선 위의 정반대인 두 점 (1, 1)과 (-1, -1), 각도 45°와 225°. 옆의 표: 둘 다 b/a = 1이라 arctan(b/a)는 둘 다 45°를 주고 (-1, -1)에서는 틀린다. atan2(b, a)는 45°와 -135°를 준다.">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="26" y1="100" x2="234" y2="100"/><line x1="130" y1="16" x2="130" y2="184"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="4 3"><line x1="48" y1="182" x2="212" y2="18"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.7"><path d="M130,100 L183,47"/><path d="M130,100 L77,153"/></g>
  <g fill="currentColor"><circle cx="185" cy="45" r="4.5"/><circle cx="75" cy="155" r="4.5"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.75"><path d="M152,100 A22,22 0 0 0 145.6,84.4"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.55"><path d="M172,100 A42,42 0 1 0 100.3,129.7"/></g>
  <text x="194" y="52" font-size="11" fill="currentColor">(1, 1)</text>
  <text x="18" y="160" font-size="11" fill="currentColor">(−1, −1)</text>
  <text x="152" y="88" font-size="10" fill="currentColor">45°</text>
  <text x="86" y="152" font-size="10" fill="currentColor">225°</text>
  <text x="262" y="70" font-size="11" fill="currentColor">점</text>
  <text x="342" y="70" font-size="11" text-anchor="middle" fill="currentColor">b/a</text>
  <text x="410" y="70" font-size="11" text-anchor="middle" fill="currentColor">arctan(b/a)</text>
  <text x="500" y="70" font-size="11" text-anchor="middle" fill="currentColor">atan2(b, a)</text>
  <polyline points="258,78 540,78" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="262" y="100" font-size="11" fill="currentColor">(1, 1)</text>
  <text x="342" y="100" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <text x="410" y="100" font-size="11" text-anchor="middle" fill="currentColor">45°</text>
  <text x="500" y="100" font-size="11" text-anchor="middle" fill="currentColor">45°</text>
  <text x="262" y="128" font-size="11" fill="currentColor">(−1, −1)</text>
  <text x="342" y="128" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <text x="410" y="128" font-size="11" text-anchor="middle" fill="currentColor">45°, 틀림</text>
  <text x="500" y="128" font-size="11" text-anchor="middle" fill="currentColor">−135°</text>
</svg>

두 점은 원점을 지나는 같은 점선 위에 있어 둘 다 $b/a = 1$이고, 그래서 $\arctan(b/a)$는 둘 모두에 $45°$를 준다 — $(1, 1)$에는 맞고 $(-1, -1)$에는 $180°$ 틀린다. $\operatorname{atan2}(b, a)$는 두 부호를 따로 보므로 $45°$와 $-135°$를 주고, $-135°$는 $225°$와 같은 방향이다.


- **오일러 공식**: $e^{j\theta} = \cos\theta + j\sin\theta$ — 각도 $\theta$의 단위원 위의 점.
  따름정리: $e^{j\theta}$를 곱하는 것 = $\theta$만큼 **회전**. 크기가
  $\sqrt{\cos^2\theta + \sin^2\theta} = 1$이고 각도가 $\theta$이기 때문이다. 예:
  $e^{j\pi/2} = \cos 90° + j\sin 90° = j$이고, $3 + 4j$에 $j$를 곱하면 $-4 + 3j$, 같은 점을
  반시계로 4분의 1 바퀴 돌린 것이다.
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

  그래서 [[02-foundations/signal-processing|6. 신호처리]]의 DFT(이산 푸리에 변환) 공식
  $X[k] = \sum_n x[n]\,e^{-j2\pi kn/N}$에는 숨은 내용이 없다: $e^{-j(\cdot)}$가 2단계의 반대
  회전이고, $\sum_n$이 평균이다. 주파수 하나당 내적 하나일 뿐이다.

<svg viewBox="0 0 560 424" style="max-width:100%;height:auto" role="img" aria-label="θ = 50°에서 단위원 위의 점 e^{jθ}; 실수축 위의 그림자는 중심에서 나온 굵은 가로 선분이고 길이는 cos θ = 0.643이다. 아래에서는 θ를 0°에서 360°까지 아래로 키우며 그림자를 그리면 원의 반지름만큼, 곧 ±1로 흔들리는 코사인이 되고, 같은 굵은 선분이 50°의 파형 위에 다시 나타난다.">
  <defs><marker id="emCsk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="126,84 294,84" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <polyline points="210,12 210,156" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <circle cx="210" cy="84" r="64" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="210,84 251.1,35" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <path d="M232,84 A22,22 0 0 0 224.1,67.1" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <polyline points="251.1,35 251.1,84" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <polyline points="251.1,86 251.1,203" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity="0.7"/>
  <polyline points="210,84 251.1,84" fill="none" stroke="currentColor" stroke-width="3.4"/>
  <polyline points="210,206 251.1,206" fill="none" stroke="currentColor" stroke-width="3.4"/>
  <polyline points="146,164 146,396" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1 3" stroke-opacity="0.55"/>
  <polyline points="274,164 274,396" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1 3" stroke-opacity="0.55"/>
  <text x="146" y="160" font-size="11" text-anchor="middle" fill="currentColor">−1</text>
  <text x="274" y="160" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="210,170 210,410" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" marker-end="url(#emCsk)"/>
  <polyline points="274,176 273.9,177.8 273.6,179.6 273.2,181.4 272.6,183.2 271.8,185 270.9,186.8 269.7,188.6 268.5,190.4 267,192.2 265.4,194 263.7,195.8 261.8,197.6 259.7,199.4 257.6,201.2 255.3,203 252.8,204.8 250.3,206.6 247.6,208.4 244.9,210.2 242,212 239.1,213.8 236,215.6 232.9,217.4 229.8,219.2 226.6,221 223.3,222.8 220,224.6 216.7,226.4 213.3,228.2 210,230 206.7,231.8 203.3,233.6 200,235.4 196.7,237.2 193.4,239 190.2,240.8 187.1,242.6 184,244.4 180.9,246.2 178,248 175.1,249.8 172.4,251.6 169.7,253.4 167.2,255.2 164.7,257 162.4,258.8 160.3,260.6 158.2,262.4 156.3,264.2 154.6,266 153,267.8 151.5,269.6 150.3,271.4 149.1,273.2 148.2,275 147.4,276.8 146.8,278.6 146.4,280.4 146.1,282.2 146,284 146.1,285.8 146.4,287.6 146.8,289.4 147.4,291.2 148.2,293 149.1,294.8 150.3,296.6 151.5,298.4 153,300.2 154.6,302 156.3,303.8 158.2,305.6 160.3,307.4 162.4,309.2 164.7,311 167.2,312.8 169.7,314.6 172.4,316.4 175.1,318.2 178,320 180.9,321.8 184,323.6 187.1,325.4 190.2,327.2 193.4,329 196.7,330.8 200,332.6 203.3,334.4 206.7,336.2 210,338 213.3,339.8 216.7,341.6 220,343.4 223.3,345.2 226.6,347 229.8,348.8 232.9,350.6 236,352.4 239.1,354.2 242,356 244.9,357.8 247.6,359.6 250.3,361.4 252.8,363.2 255.3,365 257.6,366.8 259.7,368.6 261.8,370.4 263.7,372.2 265.4,374 267,375.8 268.5,377.6 269.7,379.4 270.9,381.2 271.8,383 272.6,384.8 273.2,386.6 273.6,388.4 273.9,390.2 274,392" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="206,176 214,176" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="180" font-size="11" fill="currentColor">0°</text>
  <polyline points="206,230 214,230" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="234" font-size="11" fill="currentColor">90°</text>
  <polyline points="206,284 214,284" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="288" font-size="11" fill="currentColor">180°</text>
  <polyline points="206,338 214,338" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="342" font-size="11" fill="currentColor">270°</text>
  <polyline points="206,392 214,392" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="396" font-size="11" fill="currentColor">360°</text>
  <circle cx="251.1" cy="35" r="4" fill="currentColor"/>
  <circle cx="251.1" cy="206" r="4" fill="currentColor"/>
  <circle cx="251.1" cy="84" r="2.6" fill="currentColor"/>
  <text x="259" y="30" font-size="11" fill="currentColor">e<tspan dy="-5" font-size="10">jθ</tspan></text>
  <text x="236" y="76" font-size="11" fill="currentColor">θ</text>
  <text x="230" y="101" font-size="11" text-anchor="middle" fill="currentColor">cos θ</text>
  <text x="228" y="199" font-size="11" text-anchor="middle" fill="currentColor">cos θ</text>
  <text x="318" y="38" font-size="11" fill="currentColor">단위원을 도는 점, θ = 50°</text>
  <text x="318" y="88" font-size="11" fill="currentColor">실수축 위의 그림자: cos θ</text>
  <text x="318" y="210" font-size="11" fill="currentColor">파형 위의 같은 길이: cos 50° = 0.643</text>
  <text x="318" y="300" font-size="11" fill="currentColor">θ가 커지는 동안 그린 그림자</text>
  <text x="218" y="408" font-size="11" fill="currentColor">θ는 아래로 커진다</text>
</svg>

점 $e^{j\theta}$가 단위원을 돈다. 실수축 위의 그림자는 중심에서 나온 굵은 선분이고, 그 길이가 $\cos\theta$, $\theta = 50°$에서 $0.643$이다. 여기서는 아래로 커지는 $\theta$에 대해 그 그림자를 그리면 아래의 파형이 되는데, 같은 굵은 선분이 $50°$에 다시 나타나고 파형은 원의 반지름 그대로 $-1$과 $1$ 사이를 오간다. 파형은 별개의 대상이 아니라 회전을 옆에서 본 것이고, 그래서 "사인파로 분해"와 "회전들에 투영"이 같은 문장이다.



### 8. 선형 미분방정식 (→ 제어 트랙 5~7번)

핸들을 벽에 밀어 넣든, 히터를 켜든, 관절에 명령을 주든 질문은 같다: 그 뒤로 시스템이 어떻게 움직이는가 — 가라앉는가, 얼마나 빨리, 그리고 울리는가? 답은 미분방정식의 해이고, 이 절은 선형인 것들을 손으로 푼다. 물리 시스템은 미분방정식으로 기술된다 — 제어 전체의 모델링 언어이며, [[04-robotics/control-theory-ce397|5. 제어 이론 §2–4]]가 이것을 그대로 이어받는다. 이 절이 푸는 질량–스프링–댐퍼를 단위와 에너지까지 갖춰 자유물체도에서 유도하는 곳은, 벽을 미는 위키의 1자유도 핸들인 장치 **P3**([[02-foundations/lab-plants|0.6 Lab Plants]]) 위의 [[02-foundations/basic-mechanics|0.6.1 기초 역학 §5]]다.

- **상미분방정식**(ODE)은 한 변수의 미지 함수, 여기서는 $x(t)$와 그 도함수들 사이의 관계식이다.
  나타나는 가장 높은 도함수의 차수가 방정식의 **차수**(order)다. $x$와 그 도함수들이 1제곱으로만, $x$에
  의존하지 않는 계수와 곱해져 나타나면 **선형**이다.
  $$a_n\,x^{(n)} + \cdots + a_1\,\dot x + a_0\,x = u(t)$$
  $\dot x = dx/dt$, $x^{(n)}$은 $n$계 도함수, $a_i$는 계수(이 절에서는 전부 상수), $u(t)$는
  입력이다. 선형 ODE는 중첩 원리(§4.5)를 따르므로 입력별 해를 더할 수 있고, 그래서 아래의 모든
  도구가 작동한다. 비예시: $\dot x = -x^2$. $x_1 = 1/(t+1)$과 $x_2 = 1/(t+2)$는 둘 다 해이지만
  합은 해가 아니다. $t = 0$에서 합의 기울기는 $-1 - 0.25 = -1.25$인데
  $-(\text{합})^2 = -(1.5)^2 = -2.25$다.
- **1차**: $\dot x = ax$의 해는 $x(t) = x(0)\,e^{at}$. 이걸 믿기 위해 방정식을 풀 필요는 없다 —
  후보를 미분해서 확인만 하면 된다: $\frac{d}{dt}\big(x(0)e^{at}\big) = a\,x(0)e^{at} = a\,x(t)$ ✓,
  그리고 $t=0$에서 $x(0)$ ✓. 6절의 "$e$는 자기 자신이 도함수인 함수"를 물리 시스템에 적용한
  것이 내용의 전부다. 모든 것이 이 한 사실에서 나온다:
  $a < 0$이면 감쇠(안정), $a > 0$이면 폭발(불안정). 여기서 "안정"은 *점근 안정*, 즉 어떤
  초기값 $x(0)$에서 출발해도 $t \to \infty$에서 해가 $0$으로 돌아온다는 뜻이다(완전한 정의는
  [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]). 로봇 관절, 데워지는 방, 빠지는 물탱크
  — 전부 국소적으로 이 방정식이다.
- **시정수**(time constant). 안정한 1차 응답은 최종값 $x_\infty$까지 남은 차이를 지수적으로 좁히고,
  그 빠르기를 정하는 *시간*이 **시정수** $\tau$다. $a < 0$인 $\dot x = ax$에 대해(상수 입력은
  $x_\infty$만 옮긴다)
  $$\tau = \frac{1}{|a|}, \qquad x(t) - x_\infty = \big(x(0) - x_\infty\big)\,e^{-t/\tau}$$
  이므로 $\tau$마다 차이가 $e$분의 1로 줄어든다. $\tau$ 한 번이 지나면 갈 길의 $1 - e^{-1} = 63\%$를
  왔고, 출발점의 접선을 늘이면 정확히 $t = \tau$에서 $x_\infty$에 닿는다. $a < 0$일 때만 존재한다.
  예: P4는 $a = -1$이라 $\tau = 1\,\mathrm s$이고, 과제의 히터 $\dot x = -2x + u$는
  $\tau = 0.5\,\mathrm s$다. 비예시: $\tau$는 $x_\infty$에 *도달하는* 시간이 아니다. 지수함수는
  끝내 완전히 닿지 않는다. 왜 중요한가: 2% 안으로 가라앉는 데 $\ln 50 = 3.9$ 시정수, 약 $4\tau$가
  걸리므로 이 숫자 하나가 1차 장치의 빠르기를 말해 준다([[02-foundations/basic-mechanics|0.6.1 §5]]가
  울리는 질량–스프링–댐퍼의 포락선으로 넓힌다).
- **계산: 장치 P4.** [[02-foundations/lab-plants|0.6]]의 새는 히터는 $\dot x=-x+u$(외란 $d$는 $0$). $u=1$, $x(0)=0$이면 세 단계로 푼다. 우변을 0으로 만드는 상수가 해다: $x=1$이면 $\dot x=0=-1+1$ — 입력이 붙잡아 두는 정상상태, 곧 *특수해*다. 입력이 없는 $\dot x=-x$는 위 1차 경우에서 $a=-1$인 것이므로 임의의 $c$에 대해 $ce^{-t}$가 푼다 — *동차해*다. 중첩(§4.5)에 의해 그 합 $x(t)=1+ce^{-t}$도 $\dot x=-x+1$을 풀고, $x(0)=0$이 $c=-1$을 정한다.
  $$x(t) = 1 - e^{-t}$$
  그래서 $t=0.1$, $0.2$에서 $0.095$, $0.181$이다. **전진 오일러**(forward Euler)는 코드가 ODE를 전진하는 가장 단순한 방법이다: 스텝 시작의 기울기를 따라 길이 $T$만큼 간다, $x_{k+1}=x_k+T\,\dot x(x_k)$ — 여기서는 $x\leftarrow x+T(-x+u)$([[02-foundations/lab-kernel|0.7 Lab Kernel §2]]는 이것을 명시적 오일러라 부른다). $T=0.1$이면 $0.10$ 다음 $0.19$. 각 스텝 *시작*의 기울기가 $1-x$가 가장 클 때의 기울기이므로 높다.
- **그림 읽기.** 맨 위의 그림은 이 ODE를 블록선도로 그린 것이고, 왼쪽에서 오른쪽으로 읽는다. 동그라미는 **합산점**(summing junction)으로 옆에 적힌 부호대로 입력을 더하므로 그 출력이 곧 $\dot x=u-x$다. $\int$ 또는 $1/s$라고 쓴 상자는 **적분기**로 변화율을 그것이 바꾸는 양으로 되돌리고(적분이 왜 $s$로 나누기인지는 §9가 보인다), 작은 상자는 **이득**(gain), 곧 단순한 곱셈기로 여기서는 히터 자신의 누설률 $1$이다. 제어기 $u=-Kx$([[04-robotics/control-theory-ce397|5. 제어 이론 §1]])는 $x$를 두 번째 이득 $K$, 곧 **피드백 이득**을 거쳐 다시 되먹이고 두 이득이 더해져 루프는 $\dot x=-(1+K)x$가 되는데, 그림의 '나중에 $1+K$'가 이것이다.
- **입력이 있으면**: $\dot x = ax + bu$ — 해는 "감쇠한 초기 상태 + 누적된 입력"이다.
  $$x(t) = e^{at}\,x(0) + \int_0^t e^{a(t-t')}\,b\,u(t')\,dt'$$
  시각 $t'$에 들어온 입력 조각 $b\,u(t')\,dt'$는 남은 시간 $t-t'$ 동안 자유 응답처럼 감쇠하고,
  중첩(§4.5)이 그 조각들을 더하기 때문이다. P4($a=-1$, $b=1$, $u=1$, $x(0)=0$)로 확인하면
  $\int_0^t e^{-(t-t')}\,dt' = 1-e^{-t}$, 위 계산의 답 그대로다. 이것은
  상태공간 모델 $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$
  ([[02-foundations/linear-algebra|선형대수 §5]])의 스칼라판이고, $e^{at}$는 행렬 지수
  $e^{At}$가 되며 고유값이 $a$의 역할을 한다.
- **2차**: $\ddot x + 2\zeta\omega_n \dot x + \omega_n^2 x = 0$ — 질량-스프링-댐퍼.
  모든 응답을 두 숫자가 기술한다: 고유 진동수 $\omega_n$(감쇠 없을 때의 진동수 척도)과 감쇠비
  $\zeta$(울리는가: $0<\zeta<1$이면 $\omega_d = \omega_n\sqrt{1-\zeta^2}$로 진동하며 감쇠, $\zeta \ge 1$이면 안 함; $\zeta = 0$이면 영원히 진동하고 $\zeta<0$이면 커진다). 로봇 팔과 서스펜션이
  이 어휘로 튜닝된다. 두 숫자는 질량 $m$, 감쇠 계수 $c$, 강성 $k$로 쓴 물리적 형태
  $m\ddot x + c\dot x + kx = 0$에서 나온다. $m$으로 나누고 항을 맞추면
  $$\omega_n = \sqrt{k/m}, \qquad \zeta = \frac{c}{2\sqrt{km}}$$
  이므로 강성은 진동수를, 감쇠는 $\zeta$를 올린다. 이름 붙은 세 영역은 *부족감쇠*
  ($0 < \zeta < 1$), *임계감쇠*($\zeta = 1$, 오버슈트 없이 가장 빨리 돌아옴), *과감쇠*($\zeta > 1$)다.
  예: $m = 1$, $c = 1$, $k = 4$면 $\omega_n = 2$ rad/s, $\zeta = 0.25$로 부족감쇠이고
  $\omega_d = 2\sqrt{1 - 0.0625} = 1.936$ rad/s로 울린다. 같은 두 숫자를 P3의 핸들 위에서 — 그 댐퍼,
  그 $\zeta$, 그것이 만드는 오버슈트를 자유물체도에서 — 계산하는 곳이
  [[02-foundations/basic-mechanics|0.6.1 §4–§5]]다. 그리고 운동이 멈춰 $\ddot x = \dot x = 0$이면,
  우변에 힘 $F$를 둔 식에는 익숙한 정역학 $kx = F$만 남는다.
- 이산 시간 (코드가 실제로 도는 곳): $x_{t+1} = a x_t$ ⇒ $x_t = a^t x_0$ — $|a| < 1$일
  때만 안정. 연속과 이산의 조건($\text{Re}(a) < 0$ vs $|a_d| < 1$)은 같은 말이고, 다리는
  이것이다: $\dot x = ax$를 $\Delta t$마다 샘플링하면 $x_{t+1} = e^{a\Delta t}x_t$이므로 이산
  계수가 $a_d = e^{a\Delta t}$다. 그런데 $|e^{a\Delta t}| = e^{\text{Re}(a)\Delta t}$이므로, 이
  크기가 $1$보다 작을 조건이 정확히 $\text{Re}(a) < 0$이다. 좌반평면이 열린 단위원 *안으로
  사상된다* — 하나의 이야기를 두 좌표계로 쓴 것이다.

### 9. 라플라스 변환과 s-평면 (→ 제어 트랙, 6. 신호처리 §5)

> [!note] 이 절은 예고편이지 목적지가 아니다
> 9절은 *극점*, *전달함수*, *주파수 응답*이라는 말을 처음 만나는 것이 아니게 하려고 있다.
> 실제로 가르치는 곳은 [[04-robotics/control-theory-ce397|5. 제어 이론 §5]] — 극점 위치를
> 논문이 인용하는 정착 시간·오버슈트 숫자로 바꾸는 곳 — 와, 같은 대상으로 필터를 설계하는
> [[02-foundations/signal-processing|6. 신호처리 §5]]다. 얇은 것은 설계 의도다: 어휘용으로 한
> 번 읽고, 영점과 최소 실현의 세부는 처음에는 흘려보내고, 저 둘을 본 뒤 다시 오라.

제어 루프는 블록 여러 개를 잇는데, 그 미분방정식들을 블록마다 시간 영역에서 풀면 느리고, 설계자에게 필요한 두 가지 — 루프가 가라앉는가, 얼마나 빨리 — 가 묻혀 버린다. 라플라스 변환은 미분방정식을 대수로 바꾼다 — 그리고 [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]가 그 극점 그림을 논문이 인용하는 정착 시간·오버슈트 숫자로 바꾼다:

- 정의: **라플라스 변환**은 $t \ge 0$에서 정의된 신호 $f(t)$를 복소 변수의 함수로 보낸다.
  $$F(s) = \mathcal{L}[f](s) = \int_0^\infty f(t)\,e^{-st}\,dt$$
  $s = \sigma + j\omega$는 복소 주파수다. 실수부 $\sigma$는 감쇠율을, 허수부 $\omega$는 진동
  속도를 정한다. 적분은 $e^{-st}$가 $f$의 성장을 이길 만큼 $\text{Re}(s)$가 클 때만 존재한다.
  쓸모 있는 성질이 둘이다. 선형이다: $\mathcal{L}[af + bg] = aF + bG$ (§4.5). 그리고 가장 중요한
  성질, **미분이 $s$ 곱하기가 된다** — $\mathcal{L}[\dot f] = sF(s) - f(0)$. 부분적분에서
  나온다. 거꾸로 읽으면 **적분은 $s$로 나누기가 된다**: 누적 적분 $g(t) = \int_0^t f(t')\,dt'$는
  $g(0) = 0$이고 $\dot g = f$이므로 $F = sG$, 곧
  $$\mathcal{L}\Big[\int_0^t f(t')\,dt'\Big] = \frac{F(s)}{s}$$
  이고, 그래서 그림의 적분기 상자에 $1/s$라고 적는다. 예: $f(t) = e^{at}$면 $\text{Re}(s) > a$일 때
  $F(s) = \int_0^\infty e^{(a-s)t}\,dt = \frac{1}{s-a}$다. $a = -3$, $s = 1$이면 $1/4$이고,
  $e^{-4t}$를 수치 적분하면 $0.25$다 ✓.
- 따름정리: 미분방정식이 다항 방정식이 되고, 시스템이 **전달함수**
  $G(s) = \frac{\text{출력}(s)}{\text{입력}(s)}$가 된다.
  **네 줄 유도.** $\dot x = ax + u$의 양변에 라플라스 변환을 취한다. 전달함수는 언제나 시스템이
  정지 상태에서 출발한다는 가정($x(0) = 0$) 위에 정의되므로 좌변은
  $\mathcal{L}[\dot x] = sX(s) - x(0) = sX(s)$이고, 변환이 선형이므로 우변은 $aX(s) + U(s)$다:
  $$sX(s) = aX(s) + U(s) \;\Rightarrow\; (s-a)X(s) = U(s) \;\Rightarrow\; G(s) = \frac{X(s)}{U(s)} = \frac{1}{s-a}$$
  방금 무슨 일이 일어났는지 보라: 미분방정식이 *나눗셈*이 되었다. 그리고 그 나눗셈을 깨뜨리는
  단 하나의 $s$ 값, $s = a$가 **극점**이다 — 8절에서 부호로 안정성을 결정하던 바로 그 $a$다.
  극점은 새 개념이 아니라, 8절의 지수를 다른 이름으로 부른 것이다.
- **극점** = 분모의 근 = 8절의 $a$들 = 상태공간 $A$의 고유값(모든 극점은 고유값이다. 고유값이 숨을 수 있는 경우는 아래 노트에 있다). 복소 **s-평면**에 그리면:
  - 좌반평면(실수부 음수) → 감쇠 → **안정**
  - 우반평면 → 성장 → **불안정**
  - 허수부 → 진동 주파수; 축에서의 거리 → 감쇠 속도

<svg viewBox="0 0 560 336" style="max-width:100%;height:auto" role="img" aria-label="이 페이지의 극점을 찍은 s-평면: 1/(s+3)의 실수 극점 -3, 새는 히터 P4의 실수 극점 -1, m = 1, c = 1, k = 4인 질량-스프링-댐퍼의 복소 켤레쌍 -0.5 ± 1.936j가 음영 친 안정한 좌반평면에 있고, 우반평면에는 불안정한 극점 +1이 있다. 위쪽 극점에서 나온 점선이 허수축까지의 σ = -0.5와 실수축까지의 ω_d = 1.936을 표시한다.">
  <defs><marker id="emSpk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="40" y="10" width="290" height="320" fill="currentColor" fill-opacity="0.06"/>
  <polyline points="44,170 520,170" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emSpk)"/>
  <polyline points="330,328 330,8" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#emSpk)"/>
  <text x="120" y="188" font-size="11" text-anchor="middle" fill="currentColor">−3</text>
  <polyline points="190,166 190,174" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="188" font-size="11" text-anchor="middle" fill="currentColor">−2</text>
  <text x="260" y="188" font-size="11" text-anchor="middle" fill="currentColor">−1</text>
  <text x="400" y="188" font-size="11" text-anchor="middle" fill="currentColor">1</text>
  <polyline points="470,166 470,174" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="470" y="188" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <polyline points="326,310 334,310" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="314" font-size="11" fill="currentColor">−2</text>
  <polyline points="326,240 334,240" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="244" font-size="11" fill="currentColor">−1</text>
  <polyline points="326,100 334,100" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="104" font-size="11" fill="currentColor">1</text>
  <polyline points="326,30 334,30" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="34" font-size="11" fill="currentColor">2</text>
  <text x="510" y="190" font-size="11" text-anchor="end" fill="currentColor">Re</text>
  <text x="340" y="18" font-size="11" fill="currentColor">Im</text>
  <polyline points="295,34.4 330,34.4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="295,34.4 295,170" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="312.5" y="27.4" font-size="12" text-anchor="middle" fill="currentColor">σ</text>
  <text x="289" y="106.2" font-size="12" text-anchor="end" fill="currentColor">ω<tspan dy="3" font-size="10">d</tspan></text>
  <path d="M290,29.4 L300,39.4 M290,39.4 L300,29.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M290,300.6 L300,310.6 M290,310.6 L300,300.6" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M115,165 L125,175 M115,175 L125,165" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M255,165 L265,175 M255,175 L265,165" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M395,165 L405,175 M395,175 L405,165" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="283" y="35.4" font-size="11" text-anchor="end" fill="currentColor">−0.5 ± 1.936j</text>
  <text x="283" y="49.4" font-size="11" text-anchor="end" fill="currentColor">§8의 m = 1, c = 1, k = 4</text>
  <text x="120" y="157" font-size="11" text-anchor="middle" fill="currentColor">−3: 1/(s + 3)</text>
  <text x="260" y="157" font-size="11" text-anchor="middle" fill="currentColor">−1: P4</text>
  <text x="400" y="157" font-size="11" text-anchor="middle" fill="currentColor">+1: e<tspan dy="-5" font-size="10">t</tspan><tspan dy="5">로 커진다</tspan></text>
  <text x="48" y="322" font-size="11" fill="currentColor">좌반평면: 안정</text>
  <text x="392" y="322" font-size="11" fill="currentColor">우반평면: 불안정</text>
</svg>

이 페이지의 극점들이다: $1/(s+3)$의 $-3$, P4의 $-1$, §8 질량–스프링–댐퍼($m=1$, $c=1$, $k=4$)의 켤레쌍 $-0.5 \pm 1.936j$, 그리고 대비를 위한 불안정한 $+1$. 켤레쌍에서 가로 점선은 $\sigma = -\zeta\omega_n = -0.5$로 감쇠하는 포락선 $e^{-0.5t}$의 속도이고, 세로 점선은 $\omega_d = 1.936$ rad/s로 울리는 진동수다. 왼쪽일수록 빨리 감쇠하고, 실수축에서 멀수록 빨리 진동하며, 허수축 오른쪽에 있는 것은 모두 자란다.

> [!note]- 더 깊이 · Deeper
> **영점, 상쇄, 최소 실현.** 모든 극점은 고유값이지만, 모든 고유값이 극점으로 보이는 것은 극점–영점 상쇄가 없을 때뿐이다. **영점**은 분자의 근이다. $\frac{s-1}{(s-1)(s+2)} = \frac{1}{s+2}$처럼 같은 인수가 분자와 분모에 함께 있으면 약분되어 그 고유값(여기서는 $s=1$)이 $G(s)$에서 사라진다. 이렇게 숨은 모드가 없는 상태공간 모델을 *최소 실현*이라 부른다(Åström & Murray 예제 9.7). 상쇄된 불안정 고유값은 $G(s)$에 보이지 않는다. 전달함수는 안정해 보이는데 시스템 안의 상태 하나는 자라고 있을 수 있다.

- 7절의 복소평면이 제어에서 중요한 이유가 이것이다:
  *시스템의 정성적 거동 전체가 그림 하나 — 극점이 어디에 앉아 있는가 — 다.*
- **"주파수 응답이 $G(j\omega)$다"가 무슨 뜻인가.** $G$는 복소수 $s$에 대해 정의되었으므로,
  원하는 아무 $s$에서나 값을 물어볼 수 있다. 거기에 $s = j\omega$를 넣어 보자 — 순허수이고,
  7절에 따르면 속도 $\omega$의 순수한 회전, 즉 자라지도 줄지도 않고 영원히 진동하는 입력이다.
  이것이 정확히 "시스템에 주파수 $\omega$의 사인파를 넣는다"는 뜻이다. 답 $G(j\omega)$는
  복소수이고, 그 두 부분이 실험실에서 재는 바로 그 두 가지다: **크기** $|G(j\omega)|$는 그
  주파수를 얼마나 증폭하는가, **각도**는 얼마나 지연시키는가. $\omega$를 낮은 쪽에서 높은
  쪽으로 훑으면 그 시스템의 필터를 그린 것이 되고, 그래서 같은 그림이 제어와
  [[02-foundations/signal-processing|신호처리]] 양쪽에 쓰인다. 허수축 근처 높이 $\omega$에
  극점이 있으면 거기서 $|G(j\omega)|$가 커지는데, 그것이 공진이다.
  (이산 시간의 쌍둥이: Z-변환, 좌반평면 대신 단위원.)
  식으로 쓰면: 안정한 $G$에 입력 $u(t) = \sin\omega t$를 넣고 과도응답이 사라진 뒤의 출력은
  $$y(t) = |G(j\omega)|\,\sin\!\big(\omega t + \angle G(j\omega)\big)$$
  이므로 같은 주파수가 크기만큼 배수되고 각도만큼 밀려 나온다. $G(s) = \frac{1}{s+3}$로 계산하면
  $\omega = 0.3$ rad/s에서 $|G| = 0.332$, 각도 $-5.7°$; $\omega = 3$에서
  $|G| = 1/(3\sqrt2) = 0.236$, $-45°$; $\omega = 30$에서 $|G| = 0.033$, $-84.3°$다. 느린 입력은
  거의 그대로 지나가고 빠른 입력은 줄고 늦어진다 — 극점까지의 거리 $3$ rad/s에 모서리가 있는
  저역통과 필터다. 저항과 커패시터로 만든 같은 단극 필터와 그 극점 $303\,\mathrm{s^{-1}}$은
  [[02-foundations/basic-circuits-electronics|0.6.2 §5]]에 있다.

### 10. 표기법 사전 (전 페이지 공용)

정식 도입 전에 어디서나 쓰이는 정의 둘:

- **Softmax**는 임의의 점수 벡터를 확률분포로 바꾼다:
  $$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$
  $z = (z_1, \ldots, z_K)$는 실수 점수 $K$개(흔히 *로짓*이라 부름), $i$는 성분 하나를 고른다.
  성질이 셋이다 — 모든 출력이 양수이고, 합이 1이며, 가장 큰 점수가 가장 큰 확률을
  받는다(매끄러운 $\arg\max$). 지수함수는 양수이고 증가하며, 분모가 분자들의 합이기 때문이다.
  다른 사상도 이 성질들을 가질 수 있으므로, softmax를 정의하는 것은 성질의 목록이 아니라 위의 식이다.
  예: $z = (1, 2, 3)$이면 $(0.090, 0.245, 0.665)$이고, 모든 점수에 $100$을 더해도 공통 인수
  $e^{100}$이 약분되어 출력이 똑같다(§6의 log-sum-exp 요령이 쓰는 사실). 비예시: 그냥 정규화
  $z_i / \sum_j z_j$는 음수 점수에서 깨진다. $z = (-1, 2)$면 "확률"이 $(-1, 2)$가 된다.
  어텐션, 분류 손실, 정책 어디에나 나온다.
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
| $O(\cdot)$ | 증가 차수: $O(n^3)$은 $n$이 클 때 $n^3$의 상수배 이하 (§2) |
| $\mathbb{R}^n$, $\mathbb{R}^{m\times n}$ | 성분이 $n$개인 실수 벡터; 실수 $m\times n$ 행렬 |
| $\hat x$ | "$x$ 햇": $x$의 추정값이나 예측값 (신경망의 출력은 $\hat y$, 0.8) |
| $A^\top$ | 전치 — 대각선을 기준으로 뒤집기 ($A^\top_{ij} = A_{ji}$) |
| $\det A$ | 행렬식 — $\lvert\det A\rvert$가 사상이 부피를 몇 배로 만드는가다(부호는 방향 뒤집힘); $0$이면 공간을 납작하게 뭉개므로 역행렬이 없다 |
| $A \succeq 0$, $A \succ 0$ | 양의 준정부호/정부호 — 행렬판 "$\ge 0$"/"$>0$": 대칭 $A$에 대해 모든 $x$에서 $x^\top A x \ge 0$($\succeq$), 모든 $x \ne 0$에서 $x^\top A x > 0$($\succ$) |

> [!tip] 더 깊이 · Going deeper
> 이 페이지에서 나가는 정직한 경로는 또 다른 수학책이 아니라 기초 페이지들 자신이고, 각 절 제목이 가리키는 것이 바로 그것이다. 여기 어떤 절이 상기가 아니라 정말로 처음이라면, 그 밑에 깔린 과목은 표준적인 것이라 흔한 공업수학 교재 아무거나로 충분하다. Boas의 *Mathematical Methods in the Physical Sciences*와 Kreyszig의 *Advanced Engineering Mathematics*가 근처 책장에 있을 가능성이 가장 높은 둘이다. 책이 아니라 그 한 장만 읽어라. 이 페이지의 무엇도 한 학기를 필요로 하지 않고, 보상은 트랙의 나머지에 있다.

### 스스로 점검

1. $f(x) = \log(1 + e^x)$ (softplus)를 연쇄 법칙으로 미분하고, 결과가 시그모이드
   $\sigma(x) = 1/(1+e^{-x})$임을 보여라.
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

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P4** ($d=0$), 이 페이지 §8, [[02-foundations/lab-kernel|0.7]]의 오일러 숫자. 시뮬레이터 없음.

1. **그리기.** 열을 두 배 빨리 잃는 히터 $\dot x=-2x+u$에 대해 위의 그림을 그려라. 네 부분은 같고, 피드백 이득 블록에만 $2$를 쓴다. $x$는 온도 오차다. $u=1$, $x(0)=0$일 때 $x$ 대 $t$의 작은 삽도에 초기 기울기, 정상값, 시정수, 그리고 $t=0.1$과 $0.2$의 정확값과 전진 오일러($T=0.1$) 값을 표시하라.
2. **유도.** 1번의 히터 $\dot x=-2x+u$, $u=1$이 이번에는 중간쯤인 $x(0)=0.25$에서 출발한다. §8의 방법(특수해 + 동차해)으로 풀고, 그 $x(t)$를 §8의 입력이 있는 해의 식과 맞춰 보고, 시정수와 $x(0.5)$를 구하라.
3. **해석.** 같은 히터에 $u=1$, $x_0=0$으로 전진 오일러를 쓰되, 긴 스텝 $T=0.75\,\mathrm s$와 $T=1.2\,\mathrm s$로 각각 세 스텝씩 가서 정확해 $\tfrac12(1-e^{-2t})$와 비교하라. 갱신을 $x_{k+1}=(1-2T)\,x_k+T$로 쓰고, §8의 이산 시간 규칙으로 어떤 $T$에서 오일러가 안정한지, 그리고 안정한 히터가 왜 불안정한 시뮬레이션을 낳을 수 있는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - 명령 $u$가 왼쪽에서 들어와 합산점, 곧 입력 둘을 가진 작은 원을 만난다. 둘째 입력은 아래에서 올라온다.
> - $u$ 화살표 옆에 $+$, 되먹임 화살표 옆에 $-$를 쓴다. 이 루프를 *음*의 피드백으로 만드는 것은 상자 안의 부호가 아니라 합산점의 부호다.
> - 합산점의 출력에 $\dot x$라는 이름을 적는다. 이 그림 전체가 "합이 곧 미분이다"라는 한 문장이기 때문이다. 그 화살표는 $\int$ 또는 $1/s$라고 쓴 상자 하나로 들어가고(둘이 왜 같은 상자인지는 §9가 말한다), 상자의 출력 $x$가 온도 오차이자 유일한 상태다.
> - $x$를 따서 이득 블록 $2$를 거쳐 합산점의 아래 입력으로 되돌린다. 바뀐 것은 이 블록 하나다. 열을 잃는 빠르기는 적분기가 아니라 피드백 이득에 들어 있다.
> - 외란 화살표는 없다. P4의 $d$는 $u$와 같은 합산점으로 들어오지만 이 페이지는 $d=0$으로 둔다. [[02-foundations/rl-basics|7. RL 기초]]와 제어 트랙이 그 셋째 입력을 더한다.
> - 삽도: $t=0$, $x=0$에서 합산점의 출력은 이득과 상관없이 $\dot x=u=1$이므로 초기 기울기는 그대로다. 원점에서 그은 접선은 시정수 $1/2=0.5\,\mathrm s$에서 정상값 $u/2=0.5$에 닿고, 참 곡선은 그 아래로 지난다.
> - 삽도에는 점 넷만 찍는다. 정확값 $\tfrac12(1-e^{-2t})=0.0906$과 $0.1648$, 전진 오일러 $0.100$과 $0.180$이고, 오일러 점은 각각 짝이 되는 정확값 *위*에 찍힌다. 곡선이 아니라 그 간격이 논증이다.

> [!tip]- 정답 · Solutions
> 1. 피드백 이득이 $2$인 위 그림의 루프다. $u$와 $-2x$가 합산되고, 합이 $\dot x$, 적분기가 $x$를 돌려준다. $u=1$, $x(0)=0$이면 해는 $x(t)=\tfrac12(1-e^{-2t})$다. 초기 기울기 $1$(이득은 $x$에 곱해지는데 시작에서 $x=0$이다), 정상값 $0.5$, 시정수 $0.5\,\mathrm s$. $t=0.1$과 $0.2$에서 정확값 $0.0906$, $0.1648$. 오일러는 $x_1=0.1\times1=0.100$, $x_2=0.100+0.1(-0.200+1)=0.180$으로 둘 다 높은데, 이유는 그림의 것과 같다: 오일러는 각 스텝의 기울기를 차이가 가장 큰 시작점에서 잡는다. 열을 잃는 빠르기가 두 배가 되면 정상값과 시정수가 함께 반이 된다. $u=0$이면 오차는 $e^{-2t}$로 감쇠한다.
> 2. 특수해: 우변을 0으로 만드는 상수 $x=\tfrac12$. 동차해: $ce^{-2t}$. $x(0)=0.25$에서 $c=-0.25$이므로 $x(t)=0.5-0.25\,e^{-2t}$다. 입력이 있는 해의 식도 같다: $0.25\,e^{-2t}+\int_0^t e^{-2(t-t')}\,dt'=0.25\,e^{-2t}+\tfrac12(1-e^{-2t})=0.5-0.25\,e^{-2t}$. 시정수는 출발점과 상관없이 $1/2=0.5\,\mathrm s$이고, $x(0.5)=0.5-0.25\,e^{-1}=0.408$이다. 중간에서 출발하면 지수함수가 좁혀야 할 차이가 줄어들 뿐이다.
> 3. $T=0.75$: 인수 $1-2T$가 $-0.5$이고, 오일러는 $0.75$, $0.375$, $0.5625$를 주는데 정확해는 $0.388$, $0.475$, $0.494$다 — 정상값 $0.5$를 넘어갔다가 그 주위를 흔들리고, 흔들림은 스텝마다 반으로 준다. $T=1.2$: 인수가 $-1.4$이고, 오일러는 $1.2$, $-0.48$, $1.872$, 정확해는 $0.455$, $0.496$, $0.500$이다 — 흔들림이 스텝마다 1.4배로 커져서, 히터는 안정한데도 시뮬레이션이 발산한다. 오차 $e_k=x_k-0.5$는 $e_{k+1}=(1-2T)\,e_k$를 따르므로, §8의 규칙에 따라 오일러는 정확히 $|1-2T|<1$, 곧 $0<T<1\,\mathrm s=2\tau$일 때 안정하고, 흔들림 없이 다가가는 것은 $T\le\tau=0.5\,\mathrm s$일 때뿐이다. 히터의 참된 스텝당 인수는 언제나 0과 1 사이인 $e^{-2T}$인데, 오일러는 이것을 1차 테일러 전개(§2) $1-2T$로 바꿔 쓰고, 그 근사는 $T\ll\tau$일 때만 가깝다.
