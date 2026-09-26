---
title: "6. LQR / LQG"
tags: [robotics, control]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Study links** — [Underactuated Robotics, LQR chapter (Tedrake, MIT)](https://underactuated.csail.mit.edu/lqr.html) · [lecture slides on linear-quadratic control (Stanford)](https://web.stanford.edu/class/ee363/)

## English

*Group D. Stands on [[04-robotics/control-theory-ce397|5. Control Theory]] plus probability and optimization. Instead of placing poles by hand you
let a cost place them, and the separation principle says when estimator and controller may be designed apart.*

> [!info] Depth target · 깊이 목표
> State the LQR problem, the role of the Riccati equation, the conditions under which the solution exists and stabilizes, and LQG's estimator–controller separation with its caveat. Deriving or implementing Riccati solvers is optional.
> LQR 문제, 리카티 방정식의 역할, 해가 존재하고 안정화하는 조건, LQG의 추정기–제어기 분리와 그 단서를 말할 수 있으면 된다. 리카티 해법의 유도·구현은 선택이다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/control-theory-ce397|5. Control Theory]] (state space, eigenvalue stability, controllability/observability, pole placement, observers — this page is *"choose $K$ by optimization instead of by hand"*) · [[02-foundations/optimization|4. Optimization]] (quadratic objectives) · [[02-foundations/probability|3. Probability §5.2]] and [[04-robotics/state-estimation-slam|3. State Estimation §5]] (the Kalman filter, for the LQG half) · [[02-foundations/linear-algebra|1. Linear Algebra §3]] (positive definite and semidefinite matrices, the conditions on $Q$ and $R$) · [[02-foundations/lab-plants|0.6 Lab Plants]] (plant **P4**, the catalog's leaky heater, the running example; *plant*: control's word for the system being controlled)
> [[04-robotics/control-theory-ce397|5. 제어 이론]] (상태공간, 고유값 안정성, 가제어성/가관측성, 극점 배치, 관측기 — 이 페이지는 *"$K$를 손이 아니라 최적화로 고르기"*다) · [[02-foundations/optimization|4. 최적화]] (이차 목적함수) · [[02-foundations/probability|3. 확률 §5.2]]와 [[04-robotics/state-estimation-slam|3. 상태 추정 §5]] (LQG 절반을 위한 칼만 필터) · [[02-foundations/linear-algebra|1. 선형대수 §3]] (양의 정부호·준정부호 행렬, $Q$와 $R$에 걸린 조건) · [[02-foundations/lab-plants|0.6 Lab Plants]] (관통 예제인 장치 **P4**, 곧 카탈로그의 새는 히터. 장치(plant)는 제어 공학에서 제어 대상 시스템을 부르는 말이다)

> [!note] Why this matters · 왜 배우는가
> On the [[physical-ai-map|Physical AI Map]] this page sits in the control column beside the robot stack of [[07-research-program/index|7. Research Program §5]], and in *"install that panel on the frame"* it serves *move the component*: it chooses the feedback gain that carries the arm or the panel along its plan by pricing error against effort, and its LQG half, LQR run on a Kalman filter's estimate (§4), is where the belief of *identify panel and frame* ([[04-robotics/state-estimation-slam|3. State Estimation §5]]) enters the controller. Without a cost a gain is taste, and "optimal" says less than it sounds: on **P4**, the catalog's leaky heater ([[02-foundations/lab-plants|0.6]]), the optimal gain at $Q = 4$, $R = 1$ is $K = 1.236$ (pole $-2.236$, $x_{ss} = 0.447$ for $d = 1$), far gentler than the hand gain $K = 9$ of [[04-robotics/control-theory-ce397|5. Control Theory §1]] (Worked case), and on Doyle's system a jointly optimal LQG loop goes unstable when the actuator is $1\,\%$ stronger than modelled ($0.930 < m < 1.010$, §4). [[04-robotics/mpc|7. MPC §5]] reuses §1.5's discrete Riccati solution $P = 1.618$ as the terminal cost of its stability argument, and [[04-robotics/convex-mpc-legged|8. Convex MPC §2]] re-solves a quadratic cost of the same form at tens of hertz on a walking robot, both with this page in block 2 of the dissertation path ([[07-research-program/index|7 §8]], robotics sessions 75–76). After it you can solve a scalar Riccati equation by hand, check stabilizability and detectability, and read "we tuned $Q/R$" and "we use LQG" for what they do and do not promise.

> [!note] First pass · 처음이라면
> About two 60–90-minute sessions, robotics 75–76. **Session 1:** the Running object, the picture and the Worked case on P4 by hand — $P = K = 1.236$, pole $-2.236$, $x_{ss} = 0.447$, and the check $J = P$ — then §1, which repeats those steps with matrices, and §2. End by reading the ARE term by term and naming what each of §2's two conditions buys. **Session 2:** §1.5, the discrete-time twin ($P = 1.618$ and $K = 0.618$ on the discrete integrator, the numbers [[04-robotics/mpc|7. MPC]] reuses), §3 and §4, then the self-check and the problem set. The collapsed *Deeper* note in §1 is second pass. If you only have ten minutes, read §2: "LQR guarantees stability" has two conditions attached, and papers linearising a nonlinear system inherit them only at the linearisation point.

### Running object · 이 페이지의 대상

**P4** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's leaky heater — a first-order plant, so its whole model is one line:

$$\dot x = -x + u + d$$

where $x$ is the temperature error, $u$ the command and $d$ an unknown disturbance; in LQR's letters $A = -1$ and $B = 1$, and the open-loop pole sits at $-1$. It is the plant of [[04-robotics/control-theory-ce397|5. Control Theory §1]], where the feedback $u = -Kx$ leaves $x_{ss} = d/(1+K)$ and the hand gain $K = 9$ cut $d$ tenfold. On it this page asks the question that section left to the designer: which $K$ is best, and by what measure?

**The measure, written out.** The **linear quadratic regulator** (LQR) is the exactly solvable heart of optimal control. For linear dynamics and a quadratic cost, the infinite-horizon LQR problem is

$$\min_{u(\cdot)}\; J = \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt \quad \text{subject to} \quad \dot x = Ax + Bu,\;\; x(0) = x_0$$

with four named ingredients: the linear model $(A, B)$; the **state weight** $Q$, positive semidefinite ($x^\top Q x \ge 0$ for every $x$), which prices deviation from the origin; the **input weight** $R$, positive definite ($u^\top R u > 0$ for every $u \ne 0$, so $R^{-1}$ exists), which prices effort and must be strictly positive so that no input is free; and the infinite horizon, which is why the optimal gain is constant rather than time-varying. (Definiteness is defined in [[02-foundations/linear-algebra|1. Linear Algebra §3]].) On P4 all four are scalars and the cost is $J = \int_0^\infty (Qx^2 + Ru^2)\,dt$. Tracking a reference is the same problem written in error coordinates $x - x_{ref}$.

**Four more objects, each frozen where it is used:** the unstable scalar $\dot x = x + u$ of §1; the discrete integrator $x_{k+1} = x_k + u_k$ of §1.5, which [[04-robotics/mpc|7. MPC]] reuses; §3's cart, a unit mass on a line with position $p$ and velocity $v$ pushed by a force $u$, the double integrator $\ddot p = u$; and Doyle's two-state system in §4.

*Scope: this page teaches the infinite-horizon LQR in continuous and discrete time, when its solution exists and stabilizes, what $Q$ and $R$ do to the response, and LQG's separation principle with its missing margins. It does not teach finite-horizon or time-varying LQR beyond naming them, Riccati solvers, or robust control; the Kalman filter itself is taught on [[04-robotics/state-estimation-slam|3. State Estimation §5]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 376" style="max-width:100%;height:auto" role="img" aria-label="Top: P4, the leaky heater's feedback loop with the disturbance entering at the summing junction, and a dashed ledger that prices x with Q and u with R into J. Bottom: the real axis with the open-loop pole at -1 and the closed-loop poles at -1.414 for Q = 1 and -2.236 for Q = 4.">
  <defs><marker id="aLQR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <circle cx="96" cy="80" r="11"/>
    <rect x="160" y="60" width="160" height="40" rx="3"/>
    <rect x="238" y="138" width="60" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aLQR)">
    <line x1="96" y1="26" x2="96" y2="68"/>
    <line x1="107" y1="80" x2="158" y2="80"/>
    <line x1="320" y1="80" x2="424" y2="80"/>
    <polyline points="380,80 380,152 300,152"/>
    <polyline points="238,152 96,152 96,92"/>
  </g>
  <circle cx="380" cy="80" r="3" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-dasharray="4 3" stroke-opacity="0.75">
    <polyline points="424,80 452,80"/>
    <polyline points="472,94 472,204"/>
    <polyline points="140,152 140,204"/>
    <polyline points="160,218 300,218"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.75">
    <rect x="452" y="66" width="40" height="28" rx="3"/>
    <rect x="120" y="204" width="40" height="28" rx="3"/>
    <rect x="300" y="204" width="240" height="28" rx="3"/>
  </g>
  <circle cx="140" cy="152" r="2.6" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="50" y1="306.0" x2="519.5" y2="306.0"/>
    <line x1="470" y1="301.0" x2="470" y2="311.0"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.45">
    <line x1="170" y1="303.0" x2="170" y2="309.0"/>
    <line x1="320" y1="303.0" x2="320" y2="309.0"/>
  </g>
  <g stroke="currentColor" fill="none">
    <path d="M314.5 300.5 L325.5 311.5 M314.5 311.5 L325.5 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M252.4 300.5 L263.4 311.5 M252.4 311.5 L263.4 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M129.1 300.5 L140.1 311.5 M129.1 311.5 L140.1 300.5" stroke-width="2.4" stroke-opacity="1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aLQR)">
    <line x1="320" y1="282.0" x2="138.6" y2="282.0"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="96" y="84">Σ</text>
    <text x="240" y="85">ẋ = −x + u + d</text>
    <text x="268" y="157">−K</text>
    <text x="472" y="85">Q</text>
    <text x="140" y="223">R</text>
    <text x="420" y="223">J = ∫<tspan font-size="10" dy="4">0</tspan><tspan font-size="10" dy="-10">∞</tspan><tspan dy="6"> (Qx² + Ru²) dt</tspan></text>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="104" y="38">d</text>
    <text x="360" y="73">x</text>
    <text x="182" y="146">u</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="240" y="52" text-anchor="middle" opacity="0.85">P4, the leaky heater</text>
    <text x="268" y="184" text-anchor="middle">(Q, R) → P → K: offline, once</text>
    <text x="268" y="198" text-anchor="middle" opacity="0.85">Q = 4, R = 1 gives P = K = 1.236</text>
    <text x="540" y="250" text-anchor="end" opacity="0.8">ledger: an accounting path, it never touches the plant</text>
    <text x="227.3" y="275.0" text-anchor="middle">raise Q/R: the closed-loop pole slides left</text>
    <text x="170" y="298.0" text-anchor="middle" font-size="10" opacity="0.8">−2</text>
    <text x="328" y="326.0">−1</text>
    <text x="328" y="340.0" opacity="0.85">open loop</text>
    <text x="257.9" y="326.0" text-anchor="middle" opacity="0.85">−√2 = −1.414</text>
    <text x="257.9" y="340.0" text-anchor="middle" opacity="0.85">Q = 1</text>
    <text x="134.6" y="326.0" text-anchor="middle">−√5 = −2.236</text>
    <text x="134.6" y="340.0" text-anchor="middle">Q = 4, Worked case</text>
    <text x="470" y="326.0" text-anchor="middle">0</text>
    <text x="523.5" y="310.0">Re s</text>
    <text x="12" y="363" opacity="0.9">closed-loop pole −(1 + K) = −√(1 + Q) at R = 1; nothing else in the figure moves</text>
  </g>
</svg>

**P4**, the leaky heater $\dot x=-x+u+d$ of [[04-robotics/control-theory-ce397|5. Control Theory §1]], in its feedback loop through $-K$, with the ledger LQR adds drawn dashed beside it. The ledger prices $x$ by $Q$ and $u$ by $R$ into $J=\int_0^\infty (Qx^2+Ru^2)\,dt$ and never touches the plant, and the Riccati equation is the one offline arrow $(Q,R)\rightarrow P\rightarrow K$ ($Q=4$, $R=1$ gives $P=K=1.236$). On the real axis $\mathrm{Re}\,s$ of the $s$-plane ([[02-foundations/engineering-math|0.5 §9]]) below, the open-loop pole sits at $-1$ and, at $R=1$, the closed-loop pole at $-(1+K)=-\sqrt{1+Q}$, which is $-\sqrt2=-1.414$ at $Q=1$ and $-\sqrt5=-2.236$ at $Q=4$: raising $Q/R$ slides that pole left, and nothing else in the figure moves.

### Worked case · 대상으로 한 번 끝까지

P4 at $Q = 4$, $R = 1$, solved by hand in four steps; §1 then repeats the same four steps with matrices.

**Step 1 — guess the price of a state.** The cost-to-go $V(x)$ is the least cost $J$ still achievable from the state $x$ (§1 defines it for any system). For a linear plant and a quadratic cost it is itself quadratic, $V(x) = Px^2$ — a guess justified afterwards by the fact that it closes. The one number $P$ is the price of standing at $x = 1$.

**Step 2 — the optimality condition, minimised over $u$.** At the optimum, the cost being paid now plus the rate at which the cost-to-go changes along the motion is zero once the best input is chosen (the continuous-time Bellman equation, §1). With $d = 0$ — the cost prices the regulator, and $d$ returns in Step 4 — and $V'(x) = 2Px$, that condition reads

$$0 = \min_u\big[\,4x^2 + u^2 + 2Px\,(-x + u)\,\big]$$

The bracket is a parabola in $u$, and its derivative $2u + 2Px$ vanishes at $u^\star = -Px$, so the gain is $K = P/R = P$: it falls out of the price rather than being chosen.

**Step 3 — substitute back and solve for $P$.** With $u^\star = -Px$ the bracket is $4x^2 + P^2x^2 - 2Px^2 - 2P^2x^2 = (4 - 2P - P^2)\,x^2$, which must vanish for every $x$, so

$$-2P - P^2 + 4 = 0 \quad\Rightarrow\quad P = -1 \pm \sqrt5$$

and only $P = -1 + \sqrt5 = 1.236$ gives a stable loop; the other root, $-3.236$, would give $K = -3.236$ and $\dot x = +2.236\,x$. So $P = K = 1.236$.

**Step 4 — read the answer, and check the price.** The closed loop is $\dot x = -(1 + K)x + d = -2.236\,x + d$: the pole moves from the open loop's $-1$ to $-2.236$, and a constant $d = 1$ settles at $x_{ss} = d/(1 + K) = 0.447$. From $x_0 = 1$ with $d = 0$, $x = e^{-2.236t}$ and $u = -1.236\,x$, so

$$J = \int_0^\infty (4 + 1.236^2)\,e^{-4.472t}\,dt = \frac{5.528}{4.472} = 1.236 = P$$

because the integral of $e^{-at}$ is $1/a$: the cost-to-go at $x_0 = 1$ is $P$, as Step 1 claimed.

**Against the hand gains.** [[04-robotics/control-theory-ce397|5. Control Theory §1]] chose $K = 9$ by hand for tenfold rejection (pole $-10$, $x_{ss} = 0.1$), and its problem set runs $K = 4$ (pole $-5$, $x_{ss} = 0.2$). The same integral with $1 + K$ in place of $2.236$ prices every gain on this ledger, $J(K) = (4 + K^2)/(2(1 + K))$ from $x_0 = 1$, and the figure draws it. $Q = 4$ prices the state above effort, so LQR acts, but gently: the hand gains buy more rejection than this ledger thinks is worth paying for. Raising $Q/R$ is the $(1+K)$ trade of 5 §1 — smaller $x_{ss}$, more effort, and more amplified sensor noise.

<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="The ledger's price J of every gain K on P4 at Q = 4, R = 1 from x0 = 1: a curve with its minimum 1.236 at K = 1.236, the open loop K = 0 and the hand gain K = 4 both at 2.0, and the hand gain K = 9 at 4.25.">
  <g stroke="currentColor" stroke-width="1" fill="none"><line x1="70.0" y1="30.0" x2="70.0" y2="200.0"/><line x1="70.0" y1="200.0" x2="520.0" y2="200.0"/></g>
  <g stroke="currentColor" stroke-width="1"><line x1="66.0" y1="200.0" x2="70.0" y2="200.0"/><line x1="66.0" y1="166.0" x2="70.0" y2="166.0"/><line x1="66.0" y1="132.0" x2="70.0" y2="132.0"/><line x1="66.0" y1="98.0" x2="70.0" y2="98.0"/><line x1="66.0" y1="64.0" x2="70.0" y2="64.0"/><line x1="66.0" y1="30.0" x2="70.0" y2="30.0"/><line x1="70.0" y1="200.0" x2="70.0" y2="204.0"/><line x1="160.0" y1="200.0" x2="160.0" y2="204.0"/><line x1="250.0" y1="200.0" x2="250.0" y2="204.0"/><line x1="340.0" y1="200.0" x2="340.0" y2="204.0"/><line x1="430.0" y1="200.0" x2="430.0" y2="204.0"/><line x1="520.0" y1="200.0" x2="520.0" y2="204.0"/></g>
  <g font-size="10" fill="currentColor" text-anchor="end"><text x="63.0" y="203.5">0</text><text x="63.0" y="169.5">1</text><text x="63.0" y="135.5">2</text><text x="63.0" y="101.5">3</text><text x="63.0" y="67.5">4</text><text x="63.0" y="33.5">5</text></g>
  <g font-size="10" fill="currentColor" text-anchor="middle"><text x="70.0" y="215.0">0</text><text x="160.0" y="215.0">2</text><text x="250.0" y="215.0">4</text><text x="340.0" y="215.0">6</text><text x="430.0" y="215.0">8</text><text x="520.0" y="215.0">10</text></g>
  <text x="63.0" y="22.0" font-size="11" fill="currentColor">cost J from x₀ = 1</text>
  <text x="528.0" y="204.0" font-size="11" fill="currentColor">K</text>
  <line x1="70.0" y1="132.0" x2="250.0" y2="132.0" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <path d="M70.0 132.0 L72.2 135.2 L74.5 138.0 L76.8 140.5 L79.0 142.8 L81.2 144.8 L83.5 146.5 L85.8 148.1 L88.0 149.5 L90.2 150.7 L92.5 151.8 L94.8 152.8 L97.0 153.7 L99.2 154.4 L101.5 155.1 L103.8 155.7 L106.0 156.2 L108.2 156.6 L110.5 157.0 L112.8 157.3 L115.0 157.5 L117.2 157.7 L119.5 157.8 L121.8 157.9 L124.0 158.0 L126.2 158.0 L128.5 157.9 L130.8 157.9 L133.0 157.8 L135.2 157.7 L137.5 157.5 L139.8 157.3 L142.0 157.1 L144.2 156.9 L146.5 156.6 L148.8 156.3 L151.0 156.0 L153.2 155.7 L155.5 155.4 L157.8 155.0 L160.0 154.7 L162.2 154.3 L164.5 153.9 L166.8 153.5 L169.0 153.0 L171.2 152.6 L173.5 152.1 L175.8 151.7 L178.0 151.2 L180.2 150.7 L182.5 150.2 L184.8 149.7 L187.0 149.2 L189.2 148.7 L191.5 148.1 L193.8 147.6 L196.0 147.0 L198.2 146.5 L200.5 145.9 L202.8 145.3 L205.0 144.8 L207.2 144.2 L209.5 143.6 L211.8 143.0 L214.0 142.4 L216.2 141.8 L218.5 141.1 L220.8 140.5 L223.0 139.9 L225.2 139.2 L227.5 138.6 L229.8 138.0 L232.0 137.3 L234.3 136.7 L236.5 136.0 L238.8 135.4 L241.0 134.7 L243.2 134.0 L245.5 133.4 L247.8 132.7 L250.0 132.0 L252.2 131.3 L254.5 130.6 L256.8 129.9 L259.0 129.3 L261.2 128.6 L263.5 127.9 L265.8 127.2 L268.0 126.5 L270.2 125.8 L272.5 125.0 L274.8 124.3 L277.0 123.6 L279.2 122.9 L281.5 122.2 L283.8 121.5 L286.0 120.7 L288.2 120.0 L290.5 119.3 L292.8 118.6 L295.0 117.8 L297.2 117.1 L299.5 116.4 L301.8 115.6 L304.0 114.9 L306.2 114.2 L308.5 113.4 L310.8 112.7 L313.0 111.9 L315.2 111.2 L317.5 110.4 L319.8 109.7 L322.0 108.9 L324.2 108.2 L326.5 107.4 L328.8 106.7 L331.0 105.9 L333.2 105.1 L335.5 104.4 L337.8 103.6 L340.0 102.9 L342.3 102.1 L344.5 101.3 L346.8 100.6 L349.0 99.8 L351.2 99.0 L353.5 98.3 L355.8 97.5 L358.0 96.7 L360.2 95.9 L362.5 95.2 L364.8 94.4 L367.0 93.6 L369.2 92.8 L371.5 92.1 L373.8 91.3 L376.0 90.5 L378.2 89.7 L380.5 88.9 L382.8 88.2 L385.0 87.4 L387.3 86.6 L389.5 85.8 L391.8 85.0 L394.0 84.2 L396.2 83.4 L398.5 82.7 L400.8 81.9 L403.0 81.1 L405.2 80.3 L407.5 79.5 L409.8 78.7 L412.0 77.9 L414.2 77.1 L416.5 76.3 L418.8 75.5 L421.0 74.7 L423.2 73.9 L425.5 73.1 L427.8 72.4 L430.0 71.6 L432.3 70.8 L434.5 70.0 L436.8 69.2 L439.0 68.4 L441.2 67.6 L443.5 66.8 L445.8 66.0 L448.0 65.2 L450.3 64.4 L452.5 63.6 L454.8 62.7 L457.0 61.9 L459.2 61.1 L461.5 60.3 L463.8 59.5 L466.0 58.7 L468.2 57.9 L470.5 57.1 L472.8 56.3 L475.0 55.5 L477.3 54.7 L479.5 53.9 L481.8 53.1 L484.0 52.3 L486.2 51.5 L488.5 50.6 L490.8 49.8 L493.0 49.0 L495.3 48.2 L497.5 47.4 L499.8 46.6 L502.0 45.8 L504.2 45.0 L506.5 44.2 L508.8 43.3 L511.0 42.5 L513.2 41.7 L515.5 40.9 L517.8 40.1 L520.0 39.3" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="322.0" y="123.5" font-size="11" fill="currentColor">J(K) = (4 + K²) / (2(1 + K))</text>
  <circle cx="70.0" cy="132.0" r="3.2" fill="currentColor"/>
  <circle cx="125.6" cy="158.0" r="4" fill="currentColor"/>
  <circle cx="250.0" cy="132.0" r="3.2" fill="currentColor"/>
  <circle cx="475.0" cy="55.5" r="3.2" fill="currentColor"/>
  <text x="76.0" y="124.0" font-size="10.5" fill="currentColor">open loop, K = 0: J = 2.0</text>
  <text x="129.6" y="175.0" font-size="10.5" fill="currentColor" font-weight="bold">LQR, K = P = 1.236: J = 1.236</text>
  <text x="257.0" y="147.0" font-size="10.5" fill="currentColor">K = 4 (5's problem set): J = 2.0</text>
  <text x="469.0" y="47.5" font-size="10.5" fill="currentColor" text-anchor="end">K = 9 (5 §1): J = 4.25</text>
  <g font-size="10" fill="currentColor" opacity="0.85"><text x="64.0" y="232.0" text-anchor="start">pole −1</text><text x="125.6" y="232.0" text-anchor="middle">−2.24</text><text x="250.0" y="232.0" text-anchor="middle">−5</text><text x="475.0" y="232.0" text-anchor="middle">−10</text></g>
</svg>

The ledger's price $J(K) = (4 + K^2)/(2(1 + K))$ of every gain on P4 at $Q = 4$, $R = 1$, from $x_0 = 1$, with each marked gain's closed-loop pole $-(1+K)$ under the axis. Its minimum is $1.236$ at $K = 1.236$, the LQR gain, equal to $P$; the open loop and the hand gain $K = 4$ both cost $2.0$, and 5 §1's $K = 9$ costs $4.25$.

### 1. The Riccati equation, read structurally

[[04-robotics/control-theory-ce397|5. Control Theory §7]] placed poles where the designer chose, and the Worked case let a cost choose one, on a scalar. For any linear system the question is the same — which gain $K$ is best by the measure $J$ of the Running object — and the answer is again a constant linear feedback $u = -Kx$ with $K = R^{-1}B^\top P$, where $P$ solves one matrix equation, computed once offline, so nothing is iterated at runtime:

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

This is the **algebraic Riccati equation (ARE)**: a matrix equation, quadratic in the unknown
symmetric $n \times n$ matrix $P$, whose data are the model $A, B$ and the weights $Q, R$. $P$ is
the matrix of the optimal **cost-to-go** (value function), the least cost achievable from a
given starting state:

$$V(x_0) = \min_{u(\cdot)} \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt = x_0^\top P x_0$$

so $P$ answers "how expensive is it to be at $x_0$" for every $x_0$ at once.

**Where it comes from, in four steps** — the Worked case's four steps, with matrices. Guess that the optimal cost-to-go is quadratic,
$V(x) = x^\top P x$ — a guess justified afterwards by the fact that it closes. Substitute it
into the optimality condition (the continuous-time Bellman equation, or HJB for Hamilton–Jacobi–Bellman — the Bellman equation is introduced in discrete time in [[02-foundations/rl-basics|7. RL Basics §2]]), which says the
instantaneous cost plus the rate of change of the cost-to-go is zero at the optimum:
$0 = \min_u\,[\,x^\top Q x + u^\top R u + \nabla V^\top(Ax + Bu)\,]$, with $\nabla V = 2Px$.
Third, minimise over $u$ — now an ordinary quadratic: setting the derivative to zero gives
$2Ru + 2B^\top P x = 0$, so $u^\star = -R^{-1}B^\top P x$. **That is where the LQR gain
$K = R^{-1}B^\top P$ comes from; it falls out rather than being designed.** Fourth, put
$u^\star$ back in, term by term:
- the effort term is $u^{\star\top}Ru^\star = x^\top PBR^{-1}RR^{-1}B^\top Px = x^\top PBR^{-1}B^\top Px$;
- the rate term is $\nabla V^\top(Ax + Bu^\star) = 2x^\top PAx - 2x^\top PBR^{-1}B^\top Px$;
- and $2x^\top PAx = x^\top(A^\top P + PA)\,x$, because a scalar equals its own transpose, so $x^\top PAx = x^\top A^\top Px$ and the two halves can be written symmetrically.

Adding the state term $x^\top Qx$, the bracket is $x^\top(A^\top P + PA - PBR^{-1}B^\top P + Q)\,x$, which must be $0$ for every $x$; a symmetric matrix whose quadratic form vanishes for every $x$ is the zero matrix, and that is exactly the equation above. On P4 ($A = -1$, $B = 1$, $R = 1$, $Q = 4$) it is the Worked case's $-2P - P^2 + 4 = 0$.

Reading it that way makes the strange middle term ordinary. $-PBR^{-1}B^\top P$ is not an
extra modelling choice — it is the optimal feedback substituted back into the cost, which is
why it is quadratic in $P$ and why it is subtracted: it is the cost the controller *avoids*
by acting.

**Worked, scalar.** Take the unstable $\dot x = x + u$ ($A = B = 1$) with $Q = R = 1$. The ARE
becomes $2P - P^2 + 1 = 0$, which has **two** roots, $P = 1 + \sqrt2 = 2.414$ and
$P = 1 - \sqrt2 = -0.414$. The **stabilizing solution** is the one whose gain makes $A - BK$
stable: $P = 2.414$ gives $K = 2.414$ and the closed loop $\dot x = -1.414\,x$, while
$P = -0.414$ gives $\dot x = +1.414\,x$. A Riccati equation generally has several solutions, and
"the" solution in any paper means the stabilizing one. Check the cost-to-go: from $x_0 = 1$ the
closed loop gives $x = e^{-1.414t}$ and $u = -2.414\,x$, so
$J = \int_0^\infty (1 + 2.414^2)\,e^{-2.828t}\,dt = 2.414 = P$.

**Reading the ARE structurally.** At robot scale you never solve a Riccati equation by hand — but reading it structurally pays: $Q$ injects state cost,
the quadratic $-PBR^{-1}B^\top P$ term is *feedback eating cost through control*, and the
stabilizing solution $P$ — positive definite when $(A,Q^{1/2})$ is observable — is what makes $V(x)=x^\top P x$ a Lyapunov function for
the closed loop. (A **Lyapunov function** is a scalar "energy" of the state that is positive everywhere except at $x=0$ and decreases along every closed-loop trajectory; if one exists, the state has nowhere to go but $0$, so its existence proves stability; the three conditions and a worked example are in [[04-robotics/control-theory-ce397|5. Control Theory §4]]. Here the HJB condition gives $\dot V = -(x^\top Q x + u^{\star\top} R u^\star)$, minus the running cost.) When $Q$ is only positive semidefinite, $P$ can be singular and that Lyapunov argument needs one more step; the collapsed note says which. When a paper says "we solve a Riccati equation," it means this constant
$P$, computed once offline (or once per linearization in iterative/time-varying LQR).

> [!note]- Deeper · 더 깊이
> **When $Q$ is only semidefinite.** Under detectability alone (every mode that does not decay by itself shows up in the cost; it is the second condition of §2) $P \succeq 0$, and the argument needs a LaSalle-type step — LaSalle's invariance principle, which still proves convergence when $\dot V$ is only $\le 0$, provided no trajectory can stay forever where $\dot V = 0$ except at the origin.

### 1.5 The discrete-time twin

A robot's controller runs on a clock: it reads the state and holds its command for one period at a time, so the plant it acts on is $x_{k+1} = Ax_k + Bu_k$. Robotics papers, [[04-robotics/mpc|7. MPC]]'s terminal cost and §4's LQG all use this discrete form, so §1's question has to be asked again with a sum in place of the integral — a gain designed in continuous time and run on a slow clock is not the answer ([[04-robotics/control-theory-ce397|5. Control Theory §4]] watched $K = 99$ go unstable at $T = 0.1\,\mathrm{s}$).

For $x_{k+1} = Ax_k + Bu_k$ and the cost $\sum_k (x_k^\top Q x_k + u_k^\top R u_k)$ the cost-to-go is again quadratic, $V(x) = x^\top Px$, and the Bellman equation now says that the cost-to-go from here is the stage cost plus the cost-to-go of the next state under the best input, $V(x) = \min_u\,[\,x^\top Qx + u^\top Ru + V(Ax + Bu)\,]$. Minimising gives $u^\star = -Kx$ with $K = (R + B^\top PB)^{-1}B^\top PA$, and substituting it back gives the **discrete algebraic Riccati equation (DARE)**,

$$P = A^\top P A - A^\top P B\,(R + B^\top P B)^{-1} B^\top P A + Q$$

which has §1's structure and reading, since it is the same bookkeeping one step at a time: $Q$ injects cost, the subtracted term is the cost feedback removes, and the stabilizing solution makes $V$ a Lyapunov function — with "stable" now meaning every eigenvalue of $A - BK$ inside the unit circle, and §2's two conditions checked on the modes with $|\lambda| \ge 1$.

*Example, by hand.* The discrete integrator $x_{k+1} = x_k + u_k$ ($A = B = 1$) with $Q = R = 1$. With $V(x) = Px^2$ the bracket $x^2 + u^2 + P(x + u)^2$ is a parabola in $u$; its derivative $2u + 2P(x + u)$ vanishes at $u^\star = -\tfrac{P}{1+P}\,x$, so $K = P/(1+P)$. Putting $u^\star$ back gives $P = 1 + K^2 + P(1 - K)^2$, and because $1 - K = 1/(1 + P)$ the last two terms add up to $P/(1+P)$, so $P = 1 + P/(1+P)$, that is,

$$P^2 - P - 1 = 0 \quad\Rightarrow\quad P = \tfrac{1 + \sqrt5}{2} = 1.618$$

the positive root. Then $K = 0.618$, and the closed loop $x_{k+1} = (1 - K)\,x_k = 0.382\,x_k$ shrinks the state by $62\,\%$ a step, well inside the unit circle. [[04-robotics/mpc|7. MPC §5]] reuses exactly these numbers, $V_f = 1.618\,x^2$ and $u = -0.618\,x$, as the terminal cost and terminal controller of its stability argument, and §4 takes its LQR gain from this equation.

*Non-example.* The equation's other root, $P = (1 - \sqrt5)/2 = -0.618$, solves the DARE too, but it gives $K = -0.618/0.382 = -1.618$ and $x_{k+1} = 2.618\,x_k$, outside the unit circle: as in §1, "the" solution means the stabilizing one.

### 2. When does this actually work? Two conditions

"LQR is guaranteed stable" has fine print: two conditions, one on the model and one on the cost, and papers that linearize a nonlinear system and run LQR inherit both *at the linearization point only*. This section states each with its rank test and a pair of examples.

- **Stabilizability** of $(A,B)$: every mode of $A$ with $\text{Re}\,\lambda \ge 0$ — including the double integrator's modes at $\lambda = 0$ — must be influenceable by $u$ —
  the exact (necessary and sufficient) condition for a stabilizing feedback to exist,
  weaker than the full controllability rank test in
  [[02-foundations/linear-algebra|1. Linear Algebra §5.3]]. Otherwise no feedback can
  stabilize, Riccati or not.
  Stated as a definition, $(A,B)$ is **stabilizable** when some gain $K$ makes every eigenvalue of
  $A - BK$ have negative real part. It is checked mode by mode with the PBH
  (Popov–Belevitch–Hautus) rank test,
  $$\text{rank}\,[\,A - \lambda I \;\; B\,] = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  because the rank drops below $n$ exactly at an eigenvalue whose mode the input cannot touch;
  demanding full rank at *every* eigenvalue is controllability itself. (In discrete time the
  unstable modes are those with $|\lambda| \ge 1$.) *Example:* the uncontrollable pair of
  [[04-robotics/control-theory-ce397|5. Control Theory §6]], $A = \text{diag}(-1,-2)$ with
  $B = (1, 0)^\top$, loses rank only at $\lambda = -2$, a mode that decays by itself, so it is
  stabilizable. *Non-example:* $A = \text{diag}(1, 2)$ with the same $B$ loses rank at
  $\lambda = 2$, an unstable mode, so no $K$ exists.
- **Detectability** of $(A,Q^{1/2})$: every mode with $\text{Re}\,\lambda \ge 0$ must show up in the cost —
  otherwise the optimizer can "not care" about a mode that is quietly diverging, and the
  optimal-cost controller is not stabilizing.
  Here $Q^{1/2}$ is any matrix with $(Q^{1/2})^\top Q^{1/2} = Q$, so that
  $x^\top Q x = \lVert Q^{1/2}x\rVert^2$ is the "output" the cost sees. Detectability is the dual
  of stabilizability, with the rows stacked instead of the columns:
  $$\text{rank}\begin{bmatrix} A - \lambda I \\ Q^{1/2} \end{bmatrix} = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  since a rank drop means some non-decaying mode $v$ has $Q^{1/2}v = 0$ and so costs nothing.
  *Example:* on the §3 double integrator, $Q = \text{diag}(q, 0)$ passes (rank 2 at $\lambda = 0$),
  because position is penalized and velocity changes position. *Non-example:* $Q = \text{diag}(0, 1)$,
  velocity only, with $R = 1$, has rank 1 at $\lambda = 0$. Its positive semidefinite Riccati
  solution is $P = \text{diag}(0, 1)$, so $K = (0\;\;1)$ and the closed-loop eigenvalues are
  $0$ and $-1$: started at position $1$ with velocity $1$, the cart stops at position $2$ and stays
  there, because the cost never asked it to come back.

### 3. What Q and R do to behavior — a worked reading

Experimental sections describe their tuning in words — "aggressive gains", "we raised the state weight by two orders of magnitude" — and those words map onto exact arithmetic. On the one system in this page where the Riccati equation still solves by hand beyond a scalar, the cart of the Running object, this section derives what $Q$ and $R$ do.

Double integrator (cart): $x = (p, v)$, $u$ = force, so
$A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$, $B = \begin{pmatrix}0\\1\end{pmatrix}$.
Choose $Q = \mathrm{diag}(q, 0)$ and $R = r$.

**This one you can actually solve by hand**, and the answer teaches more than any solver
output. Write $P = \begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$ and substitute
into the Riccati equation. Its three distinct entries give three scalar equations:

$$q - \frac{p_{12}^2}{r} = 0, \qquad p_{11} - \frac{p_{12}p_{22}}{r} = 0, \qquad 2p_{12} - \frac{p_{22}^2}{r} = 0$$

They are triangular, which is why you can solve for $p_{12}$ first and let the rest follow: $p_{12} = \sqrt{qr}$, then $p_{22} = \sqrt{2r\sqrt{qr}}$, then $p_{11}$
follows. The gain $K = R^{-1}B^\top P$ is the bottom row of $P$ divided by $r$:

$$k_1 = \sqrt{\rho}, \qquad k_2 = \sqrt{2}\,\rho^{1/4}, \qquad \text{where } \rho = q/r$$

Now read what that says — three separate facts fall out at once.

| $q$ | $r$ | $\rho = q/r$ | $K = (k_1, k_2)$ | $\omega_n$ | $\zeta$ | settling $\approx 4/\zeta\omega_n$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7 s |
| 100 | 1 | 100 | $(10.0,\ 4.47)$ | 3.16 | 0.707 | 1.8 s |
| 1 | 100 | 0.01 | $(0.10,\ 0.45)$ | 0.32 | 0.707 | 17.9 s |
| 10 | 10 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7 s |

- **A common scalar scale does not matter.** Rows 1 and 4 have identical gains: multiplying
  every entry of $Q$ and $R$ by the same positive scalar changes the cost scale, not its
  argmin. Relative weights within the matrices still matter.
- **For this position-only $Q=\operatorname{diag}(q,0)$, the damping is fixed.** Every row has $\zeta = 1/\sqrt2 = 0.707$. The
  closed-loop characteristic polynomial is
  $\lambda^2 + \sqrt2\rho^{1/4}\lambda + \sqrt\rho$, so $\omega_n = \rho^{1/4}$ and
  $2\zeta\omega_n = \sqrt2\rho^{1/4}$ force $\zeta = 0.707$ for any $q/r$ **under this special choice of $Q$**. Adding a velocity-state weight changes the Riccati solution and can change damping. Here the weights buy speed, not shape. This makes the claim "LQR picks the poles by optimization instead of by hand"
  made concrete — [[04-robotics/control-theory-ce397|5. Control Theory §7]] placed poles at
  $\zeta = 0.7$ by hand, and LQR arrived at essentially the same place without being told.
- **Speed is a fourth root, which is brutal.** $\omega_n = \rho^{1/4}$ means doubling the
  controller's bandwidth costs a **16×** increase in $q/r$; ten times faster costs $10^4$.
  When an experimental section says "we raised the state weight by two orders of magnitude",
  that bought a factor of $\sqrt{10} \approx 3.2$ in bandwidth — and, because
  $k_1 = \sqrt\rho$ grew 10×, roughly 10× the commanded force and 10× the amplified sensor
  noise along with it.

In the words experimental sections use:

- **Large $q/r$** ("state expensive, control cheap"): aggressive gains — fast recovery, large
  force spikes, more noise amplification, actuator saturation risk (which LQR itself does not
  model — that is [[04-robotics/mpc|MPC]]'s job).
- **Small $q/r$** ("control expensive"): gentle gains, slow recovery, smooth inputs.
- Weights on velocity vs position shape *damping* vs *stiffness* of the response — the knob
  vocabulary behind "we tuned Q/R for a settling time of…".

<svg viewBox="0 0 560 240" style="max-width:100%;height:auto" role="img" aria-label="Step responses of the cart under LQR at q/r = 100, 1 and 0.01 over 0 to 20 s: all overshoot the target by 4.3 percent, peaking at 1.41, 4.44 and 14.1 s, and settle in 1.8, 5.7 and 17.9 s.">
  <g stroke="currentColor" stroke-width="1" fill="none"><line x1="56.0" y1="23.5" x2="56.0" y2="150.0"/><line x1="56.0" y1="150.0" x2="536.0" y2="150.0"/><line x1="56.0" y1="40.0" x2="536.0" y2="40.0" stroke-dasharray="4 4" stroke-opacity="0.5"/></g>
  <g stroke="currentColor" stroke-width="1"><line x1="56.0" y1="150.0" x2="56.0" y2="154.0"/><line x1="176.0" y1="150.0" x2="176.0" y2="154.0"/><line x1="296.0" y1="150.0" x2="296.0" y2="154.0"/><line x1="416.0" y1="150.0" x2="416.0" y2="154.0"/><line x1="536.0" y1="150.0" x2="536.0" y2="154.0"/><line x1="52.0" y1="40.0" x2="56.0" y2="40.0"/><line x1="52.0" y1="150.0" x2="56.0" y2="150.0"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle"><text x="56.0" y="165.0">0</text><text x="176.0" y="165.0">5</text><text x="296.0" y="165.0">10</text><text x="416.0" y="165.0">15</text><text x="536.0" y="165.0">20</text></g>
  <g font-size="10.5" fill="currentColor" text-anchor="end"><text x="49.0" y="43.5">target 1</text><text x="49.0" y="153.5">0</text></g>
  <text x="536.0" y="178.0" font-size="10.5" fill="currentColor" text-anchor="end">t (s)</text>
  <path d="M56.0 150.0 L57.2 148.7 L58.4 145.3 L59.6 140.2 L60.8 133.8 L62.0 126.7 L63.2 119.0 L64.4 111.1 L65.6 103.2 L66.8 95.5 L68.0 88.1 L69.2 81.1 L70.4 74.5 L71.6 68.5 L72.8 63.1 L74.0 58.3 L75.2 54.0 L76.4 50.2 L77.6 47.0 L78.8 44.3 L80.0 42.0 L81.2 40.1 L82.4 38.6 L83.6 37.5 L84.8 36.6 L86.0 36.0 L87.2 35.6 L88.4 35.3 L89.6 35.2 L90.8 35.3 L92.0 35.4 L93.2 35.6 L94.4 35.9 L95.6 36.2 L96.8 36.6 L98.0 36.9 L99.2 37.2 L100.4 37.6 L101.6 37.9 L102.8 38.2 L104.0 38.5 L105.2 38.7 L106.4 39.0 L107.6 39.2 L108.8 39.4 L110.0 39.5 L111.2 39.7 L112.4 39.8 L113.6 39.9 L114.8 40.0 L116.0 40.1 L117.2 40.1 L118.4 40.1 L119.6 40.2 L120.8 40.2 L122.0 40.2 L123.2 40.2 L124.4 40.2 L125.6 40.2 L126.8 40.2 L128.0 40.2 L129.2 40.2 L130.4 40.2 L131.6 40.1 L132.8 40.1 L134.0 40.1 L135.2 40.1 L136.4 40.1 L137.6 40.1 L138.8 40.1 L140.0 40.0 L141.2 40.0 L142.4 40.0 L143.6 40.0 L144.8 40.0 L146.0 40.0 L147.2 40.0 L148.4 40.0 L149.6 40.0 L150.8 40.0 L152.0 40.0 L153.2 40.0 L154.4 40.0 L155.6 40.0 L156.8 40.0 L158.0 40.0 L159.2 40.0 L160.4 40.0 L161.6 40.0 L162.8 40.0 L164.0 40.0 L165.2 40.0 L166.4 40.0 L167.6 40.0 L168.8 40.0 L170.0 40.0 L171.2 40.0 L172.4 40.0 L173.6 40.0 L174.8 40.0 L176.0 40.0 L177.2 40.0 L178.4 40.0 L179.6 40.0 L180.8 40.0 L182.0 40.0 L183.2 40.0 L184.4 40.0 L185.6 40.0 L186.8 40.0 L188.0 40.0 L189.2 40.0 L190.4 40.0 L191.6 40.0 L192.8 40.0 L194.0 40.0 L195.2 40.0 L196.4 40.0 L197.6 40.0 L198.8 40.0 L200.0 40.0 L201.2 40.0 L202.4 40.0 L203.6 40.0 L204.8 40.0 L206.0 40.0 L207.2 40.0 L208.4 40.0 L209.6 40.0 L210.8 40.0 L212.0 40.0 L213.2 40.0 L214.4 40.0 L215.6 40.0 L216.8 40.0 L218.0 40.0 L219.2 40.0 L220.4 40.0 L221.6 40.0 L222.8 40.0 L224.0 40.0 L225.2 40.0 L226.4 40.0 L227.6 40.0 L228.8 40.0 L230.0 40.0 L231.2 40.0 L232.4 40.0 L233.6 40.0 L234.8 40.0 L236.0 40.0 L237.2 40.0 L238.4 40.0 L239.6 40.0 L240.8 40.0 L242.0 40.0 L243.2 40.0 L244.4 40.0 L245.6 40.0 L246.8 40.0 L248.0 40.0 L249.2 40.0 L250.4 40.0 L251.6 40.0 L252.8 40.0 L254.0 40.0 L255.2 40.0 L256.4 40.0 L257.6 40.0 L258.8 40.0 L260.0 40.0 L261.2 40.0 L262.4 40.0 L263.6 40.0 L264.8 40.0 L266.0 40.0 L267.2 40.0 L268.4 40.0 L269.6 40.0 L270.8 40.0 L272.0 40.0 L273.2 40.0 L274.4 40.0 L275.6 40.0 L276.8 40.0 L278.0 40.0 L279.2 40.0 L280.4 40.0 L281.6 40.0 L282.8 40.0 L284.0 40.0 L285.2 40.0 L286.4 40.0 L287.6 40.0 L288.8 40.0 L290.0 40.0 L291.2 40.0 L292.4 40.0 L293.6 40.0 L294.8 40.0 L296.0 40.0 L297.2 40.0 L298.4 40.0 L299.6 40.0 L300.8 40.0 L302.0 40.0 L303.2 40.0 L304.4 40.0 L305.6 40.0 L306.8 40.0 L308.0 40.0 L309.2 40.0 L310.4 40.0 L311.6 40.0 L312.8 40.0 L314.0 40.0 L315.2 40.0 L316.4 40.0 L317.6 40.0 L318.8 40.0 L320.0 40.0 L321.2 40.0 L322.4 40.0 L323.6 40.0 L324.8 40.0 L326.0 40.0 L327.2 40.0 L328.4 40.0 L329.6 40.0 L330.8 40.0 L332.0 40.0 L333.2 40.0 L334.4 40.0 L335.6 40.0 L336.8 40.0 L338.0 40.0 L339.2 40.0 L340.4 40.0 L341.6 40.0 L342.8 40.0 L344.0 40.0 L345.2 40.0 L346.4 40.0 L347.6 40.0 L348.8 40.0 L350.0 40.0 L351.2 40.0 L352.4 40.0 L353.6 40.0 L354.8 40.0 L356.0 40.0 L357.2 40.0 L358.4 40.0 L359.6 40.0 L360.8 40.0 L362.0 40.0 L363.2 40.0 L364.4 40.0 L365.6 40.0 L366.8 40.0 L368.0 40.0 L369.2 40.0 L370.4 40.0 L371.6 40.0 L372.8 40.0 L374.0 40.0 L375.2 40.0 L376.4 40.0 L377.6 40.0 L378.8 40.0 L380.0 40.0 L381.2 40.0 L382.4 40.0 L383.6 40.0 L384.8 40.0 L386.0 40.0 L387.2 40.0 L388.4 40.0 L389.6 40.0 L390.8 40.0 L392.0 40.0 L393.2 40.0 L394.4 40.0 L395.6 40.0 L396.8 40.0 L398.0 40.0 L399.2 40.0 L400.4 40.0 L401.6 40.0 L402.8 40.0 L404.0 40.0 L405.2 40.0 L406.4 40.0 L407.6 40.0 L408.8 40.0 L410.0 40.0 L411.2 40.0 L412.4 40.0 L413.6 40.0 L414.8 40.0 L416.0 40.0 L417.2 40.0 L418.4 40.0 L419.6 40.0 L420.8 40.0 L422.0 40.0 L423.2 40.0 L424.4 40.0 L425.6 40.0 L426.8 40.0 L428.0 40.0 L429.2 40.0 L430.4 40.0 L431.6 40.0 L432.8 40.0 L434.0 40.0 L435.2 40.0 L436.4 40.0 L437.6 40.0 L438.8 40.0 L440.0 40.0 L441.2 40.0 L442.4 40.0 L443.6 40.0 L444.8 40.0 L446.0 40.0 L447.2 40.0 L448.4 40.0 L449.6 40.0 L450.8 40.0 L452.0 40.0 L453.2 40.0 L454.4 40.0 L455.6 40.0 L456.8 40.0 L458.0 40.0 L459.2 40.0 L460.4 40.0 L461.6 40.0 L462.8 40.0 L464.0 40.0 L465.2 40.0 L466.4 40.0 L467.6 40.0 L468.8 40.0 L470.0 40.0 L471.2 40.0 L472.4 40.0 L473.6 40.0 L474.8 40.0 L476.0 40.0 L477.2 40.0 L478.4 40.0 L479.6 40.0 L480.8 40.0 L482.0 40.0 L483.2 40.0 L484.4 40.0 L485.6 40.0 L486.8 40.0 L488.0 40.0 L489.2 40.0 L490.4 40.0 L491.6 40.0 L492.8 40.0 L494.0 40.0 L495.2 40.0 L496.4 40.0 L497.6 40.0 L498.8 40.0 L500.0 40.0 L501.2 40.0 L502.4 40.0 L503.6 40.0 L504.8 40.0 L506.0 40.0 L507.2 40.0 L508.4 40.0 L509.6 40.0 L510.8 40.0 L512.0 40.0 L513.2 40.0 L514.4 40.0 L515.6 40.0 L516.8 40.0 L518.0 40.0 L519.2 40.0 L520.4 40.0 L521.6 40.0 L522.8 40.0 L524.0 40.0 L525.2 40.0 L526.4 40.0 L527.6 40.0 L528.8 40.0 L530.0 40.0 L531.2 40.0 L532.4 40.0 L533.6 40.0 L534.8 40.0 L536.0 40.0" fill="none" stroke="currentColor" stroke-width="2" />
  <path d="M56.0 150.0 L57.2 149.9 L58.4 149.5 L59.6 148.8 L60.8 148.0 L62.0 146.9 L63.2 145.7 L64.4 144.3 L65.6 142.7 L66.8 141.0 L68.0 139.2 L69.2 137.3 L70.4 135.2 L71.6 133.1 L72.8 130.9 L74.0 128.6 L75.2 126.2 L76.4 123.8 L77.6 121.4 L78.8 119.0 L80.0 116.5 L81.2 114.0 L82.4 111.5 L83.6 109.0 L84.8 106.5 L86.0 104.0 L87.2 101.5 L88.4 99.0 L89.6 96.6 L90.8 94.2 L92.0 91.8 L93.2 89.5 L94.4 87.2 L95.6 85.0 L96.8 82.8 L98.0 80.6 L99.2 78.5 L100.4 76.4 L101.6 74.4 L102.8 72.5 L104.0 70.6 L105.2 68.7 L106.4 67.0 L107.6 65.2 L108.8 63.6 L110.0 62.0 L111.2 60.4 L112.4 58.9 L113.6 57.5 L114.8 56.1 L116.0 54.7 L117.2 53.5 L118.4 52.2 L119.6 51.1 L120.8 50.0 L122.0 48.9 L123.2 47.9 L124.4 46.9 L125.6 46.0 L126.8 45.2 L128.0 44.3 L129.2 43.6 L130.4 42.8 L131.6 42.2 L132.8 41.5 L134.0 40.9 L135.2 40.3 L136.4 39.8 L137.6 39.3 L138.8 38.9 L140.0 38.4 L141.2 38.1 L142.4 37.7 L143.6 37.4 L144.8 37.1 L146.0 36.8 L147.2 36.6 L148.4 36.3 L149.6 36.1 L150.8 36.0 L152.0 35.8 L153.2 35.7 L154.4 35.6 L155.6 35.5 L156.8 35.4 L158.0 35.3 L159.2 35.3 L160.4 35.3 L161.6 35.3 L162.8 35.2 L164.0 35.3 L165.2 35.3 L166.4 35.3 L167.6 35.3 L168.8 35.4 L170.0 35.4 L171.2 35.5 L172.4 35.6 L173.6 35.6 L174.8 35.7 L176.0 35.8 L177.2 35.9 L178.4 36.0 L179.6 36.1 L180.8 36.2 L182.0 36.3 L183.2 36.4 L184.4 36.5 L185.6 36.6 L186.8 36.7 L188.0 36.8 L189.2 36.9 L190.4 37.0 L191.6 37.1 L192.8 37.3 L194.0 37.4 L195.2 37.5 L196.4 37.6 L197.6 37.7 L198.8 37.8 L200.0 37.9 L201.2 38.0 L202.4 38.1 L203.6 38.2 L204.8 38.3 L206.0 38.3 L207.2 38.4 L208.4 38.5 L209.6 38.6 L210.8 38.7 L212.0 38.8 L213.2 38.8 L214.4 38.9 L215.6 39.0 L216.8 39.1 L218.0 39.1 L219.2 39.2 L220.4 39.3 L221.6 39.3 L222.8 39.4 L224.0 39.4 L225.2 39.5 L226.4 39.5 L227.6 39.6 L228.8 39.6 L230.0 39.7 L231.2 39.7 L232.4 39.7 L233.6 39.8 L234.8 39.8 L236.0 39.9 L237.2 39.9 L238.4 39.9 L239.6 39.9 L240.8 40.0 L242.0 40.0 L243.2 40.0 L244.4 40.0 L245.6 40.1 L246.8 40.1 L248.0 40.1 L249.2 40.1 L250.4 40.1 L251.6 40.1 L252.8 40.1 L254.0 40.2 L255.2 40.2 L256.4 40.2 L257.6 40.2 L258.8 40.2 L260.0 40.2 L261.2 40.2 L262.4 40.2 L263.6 40.2 L264.8 40.2 L266.0 40.2 L267.2 40.2 L268.4 40.2 L269.6 40.2 L270.8 40.2 L272.0 40.2 L273.2 40.2 L274.4 40.2 L275.6 40.2 L276.8 40.2 L278.0 40.2 L279.2 40.2 L280.4 40.2 L281.6 40.2 L282.8 40.2 L284.0 40.2 L285.2 40.2 L286.4 40.2 L287.6 40.2 L288.8 40.2 L290.0 40.2 L291.2 40.2 L292.4 40.1 L293.6 40.1 L294.8 40.1 L296.0 40.1 L297.2 40.1 L298.4 40.1 L299.6 40.1 L300.8 40.1 L302.0 40.1 L303.2 40.1 L304.4 40.1 L305.6 40.1 L306.8 40.1 L308.0 40.1 L309.2 40.1 L310.4 40.1 L311.6 40.1 L312.8 40.1 L314.0 40.1 L315.2 40.1 L316.4 40.1 L317.6 40.1 L318.8 40.1 L320.0 40.0 L321.2 40.0 L322.4 40.0 L323.6 40.0 L324.8 40.0 L326.0 40.0 L327.2 40.0 L328.4 40.0 L329.6 40.0 L330.8 40.0 L332.0 40.0 L333.2 40.0 L334.4 40.0 L335.6 40.0 L336.8 40.0 L338.0 40.0 L339.2 40.0 L340.4 40.0 L341.6 40.0 L342.8 40.0 L344.0 40.0 L345.2 40.0 L346.4 40.0 L347.6 40.0 L348.8 40.0 L350.0 40.0 L351.2 40.0 L352.4 40.0 L353.6 40.0 L354.8 40.0 L356.0 40.0 L357.2 40.0 L358.4 40.0 L359.6 40.0 L360.8 40.0 L362.0 40.0 L363.2 40.0 L364.4 40.0 L365.6 40.0 L366.8 40.0 L368.0 40.0 L369.2 40.0 L370.4 40.0 L371.6 40.0 L372.8 40.0 L374.0 40.0 L375.2 40.0 L376.4 40.0 L377.6 40.0 L378.8 40.0 L380.0 40.0 L381.2 40.0 L382.4 40.0 L383.6 40.0 L384.8 40.0 L386.0 40.0 L387.2 40.0 L388.4 40.0 L389.6 40.0 L390.8 40.0 L392.0 40.0 L393.2 40.0 L394.4 40.0 L395.6 40.0 L396.8 40.0 L398.0 40.0 L399.2 40.0 L400.4 40.0 L401.6 40.0 L402.8 40.0 L404.0 40.0 L405.2 40.0 L406.4 40.0 L407.6 40.0 L408.8 40.0 L410.0 40.0 L411.2 40.0 L412.4 40.0 L413.6 40.0 L414.8 40.0 L416.0 40.0 L417.2 40.0 L418.4 40.0 L419.6 40.0 L420.8 40.0 L422.0 40.0 L423.2 40.0 L424.4 40.0 L425.6 40.0 L426.8 40.0 L428.0 40.0 L429.2 40.0 L430.4 40.0 L431.6 40.0 L432.8 40.0 L434.0 40.0 L435.2 40.0 L436.4 40.0 L437.6 40.0 L438.8 40.0 L440.0 40.0 L441.2 40.0 L442.4 40.0 L443.6 40.0 L444.8 40.0 L446.0 40.0 L447.2 40.0 L448.4 40.0 L449.6 40.0 L450.8 40.0 L452.0 40.0 L453.2 40.0 L454.4 40.0 L455.6 40.0 L456.8 40.0 L458.0 40.0 L459.2 40.0 L460.4 40.0 L461.6 40.0 L462.8 40.0 L464.0 40.0 L465.2 40.0 L466.4 40.0 L467.6 40.0 L468.8 40.0 L470.0 40.0 L471.2 40.0 L472.4 40.0 L473.6 40.0 L474.8 40.0 L476.0 40.0 L477.2 40.0 L478.4 40.0 L479.6 40.0 L480.8 40.0 L482.0 40.0 L483.2 40.0 L484.4 40.0 L485.6 40.0 L486.8 40.0 L488.0 40.0 L489.2 40.0 L490.4 40.0 L491.6 40.0 L492.8 40.0 L494.0 40.0 L495.2 40.0 L496.4 40.0 L497.6 40.0 L498.8 40.0 L500.0 40.0 L501.2 40.0 L502.4 40.0 L503.6 40.0 L504.8 40.0 L506.0 40.0 L507.2 40.0 L508.4 40.0 L509.6 40.0 L510.8 40.0 L512.0 40.0 L513.2 40.0 L514.4 40.0 L515.6 40.0 L516.8 40.0 L518.0 40.0 L519.2 40.0 L520.4 40.0 L521.6 40.0 L522.8 40.0 L524.0 40.0 L525.2 40.0 L526.4 40.0 L527.6 40.0 L528.8 40.0 L530.0 40.0 L531.2 40.0 L532.4 40.0 L533.6 40.0 L534.8 40.0 L536.0 40.0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-dasharray="7 4" stroke-opacity="0.8"/>
  <path d="M56.0 150.0 L57.2 150.0 L58.4 149.9 L59.6 149.9 L60.8 149.8 L62.0 149.7 L63.2 149.5 L64.4 149.4 L65.6 149.2 L66.8 149.0 L68.0 148.7 L69.2 148.5 L70.4 148.2 L71.6 147.9 L72.8 147.6 L74.0 147.2 L75.2 146.9 L76.4 146.5 L77.6 146.1 L78.8 145.7 L80.0 145.3 L81.2 144.8 L82.4 144.4 L83.6 143.9 L84.8 143.4 L86.0 142.9 L87.2 142.4 L88.4 141.8 L89.6 141.3 L90.8 140.7 L92.0 140.2 L93.2 139.6 L94.4 139.0 L95.6 138.4 L96.8 137.8 L98.0 137.1 L99.2 136.5 L100.4 135.8 L101.6 135.2 L102.8 134.5 L104.0 133.8 L105.2 133.2 L106.4 132.5 L107.6 131.8 L108.8 131.1 L110.0 130.3 L111.2 129.6 L112.4 128.9 L113.6 128.2 L114.8 127.4 L116.0 126.7 L117.2 125.9 L118.4 125.2 L119.6 124.4 L120.8 123.7 L122.0 122.9 L123.2 122.1 L124.4 121.4 L125.6 120.6 L126.8 119.8 L128.0 119.0 L129.2 118.2 L130.4 117.4 L131.6 116.7 L132.8 115.9 L134.0 115.1 L135.2 114.3 L136.4 113.5 L137.6 112.7 L138.8 111.9 L140.0 111.1 L141.2 110.3 L142.4 109.5 L143.6 108.7 L144.8 108.0 L146.0 107.2 L147.2 106.4 L148.4 105.6 L149.6 104.8 L150.8 104.0 L152.0 103.2 L153.2 102.4 L154.4 101.7 L155.6 100.9 L156.8 100.1 L158.0 99.3 L159.2 98.6 L160.4 97.8 L161.6 97.0 L162.8 96.3 L164.0 95.5 L165.2 94.7 L166.4 94.0 L167.6 93.2 L168.8 92.5 L170.0 91.7 L171.2 91.0 L172.4 90.3 L173.6 89.5 L174.8 88.8 L176.0 88.1 L177.2 87.3 L178.4 86.6 L179.6 85.9 L180.8 85.2 L182.0 84.5 L183.2 83.8 L184.4 83.1 L185.6 82.4 L186.8 81.7 L188.0 81.1 L189.2 80.4 L190.4 79.7 L191.6 79.0 L192.8 78.4 L194.0 77.7 L195.2 77.1 L196.4 76.4 L197.6 75.8 L198.8 75.2 L200.0 74.5 L201.2 73.9 L202.4 73.3 L203.6 72.7 L204.8 72.1 L206.0 71.5 L207.2 70.9 L208.4 70.3 L209.6 69.7 L210.8 69.1 L212.0 68.5 L213.2 68.0 L214.4 67.4 L215.6 66.9 L216.8 66.3 L218.0 65.8 L219.2 65.2 L220.4 64.7 L221.6 64.2 L222.8 63.6 L224.0 63.1 L225.2 62.6 L226.4 62.1 L227.6 61.6 L228.8 61.1 L230.0 60.6 L231.2 60.1 L232.4 59.7 L233.6 59.2 L234.8 58.7 L236.0 58.3 L237.2 57.8 L238.4 57.4 L239.6 56.9 L240.8 56.5 L242.0 56.0 L243.2 55.6 L244.4 55.2 L245.6 54.8 L246.8 54.4 L248.0 54.0 L249.2 53.6 L250.4 53.2 L251.6 52.8 L252.8 52.4 L254.0 52.0 L255.2 51.7 L256.4 51.3 L257.6 50.9 L258.8 50.6 L260.0 50.2 L261.2 49.9 L262.4 49.5 L263.6 49.2 L264.8 48.9 L266.0 48.6 L267.2 48.2 L268.4 47.9 L269.6 47.6 L270.8 47.3 L272.0 47.0 L273.2 46.7 L274.4 46.4 L275.6 46.1 L276.8 45.9 L278.0 45.6 L279.2 45.3 L280.4 45.0 L281.6 44.8 L282.8 44.5 L284.0 44.3 L285.2 44.0 L286.4 43.8 L287.6 43.5 L288.8 43.3 L290.0 43.1 L291.2 42.9 L292.4 42.6 L293.6 42.4 L294.8 42.2 L296.0 42.0 L297.2 41.8 L298.4 41.6 L299.6 41.4 L300.8 41.2 L302.0 41.0 L303.2 40.8 L304.4 40.6 L305.6 40.5 L306.8 40.3 L308.0 40.1 L309.2 40.0 L310.4 39.8 L311.6 39.6 L312.8 39.5 L314.0 39.3 L315.2 39.2 L316.4 39.0 L317.6 38.9 L318.8 38.8 L320.0 38.6 L321.2 38.5 L322.4 38.4 L323.6 38.2 L324.8 38.1 L326.0 38.0 L327.2 37.9 L328.4 37.8 L329.6 37.7 L330.8 37.6 L332.0 37.5 L333.2 37.4 L334.4 37.3 L335.6 37.2 L336.8 37.1 L338.0 37.0 L339.2 36.9 L340.4 36.8 L341.6 36.7 L342.8 36.7 L344.0 36.6 L345.2 36.5 L346.4 36.4 L347.6 36.4 L348.8 36.3 L350.0 36.2 L351.2 36.2 L352.4 36.1 L353.6 36.1 L354.8 36.0 L356.0 36.0 L357.2 35.9 L358.4 35.9 L359.6 35.8 L360.8 35.8 L362.0 35.7 L363.2 35.7 L364.4 35.7 L365.6 35.6 L366.8 35.6 L368.0 35.6 L369.2 35.5 L370.4 35.5 L371.6 35.5 L372.8 35.4 L374.0 35.4 L375.2 35.4 L376.4 35.4 L377.6 35.4 L378.8 35.3 L380.0 35.3 L381.2 35.3 L382.4 35.3 L383.6 35.3 L384.8 35.3 L386.0 35.3 L387.2 35.3 L388.4 35.3 L389.6 35.3 L390.8 35.2 L392.0 35.2 L393.2 35.2 L394.4 35.2 L395.6 35.2 L396.8 35.3 L398.0 35.3 L399.2 35.3 L400.4 35.3 L401.6 35.3 L402.8 35.3 L404.0 35.3 L405.2 35.3 L406.4 35.3 L407.6 35.3 L408.8 35.3 L410.0 35.4 L411.2 35.4 L412.4 35.4 L413.6 35.4 L414.8 35.4 L416.0 35.4 L417.2 35.5 L418.4 35.5 L419.6 35.5 L420.8 35.5 L422.0 35.5 L423.2 35.6 L424.4 35.6 L425.6 35.6 L426.8 35.6 L428.0 35.6 L429.2 35.7 L430.4 35.7 L431.6 35.7 L432.8 35.7 L434.0 35.8 L435.2 35.8 L436.4 35.8 L437.6 35.9 L438.8 35.9 L440.0 35.9 L441.2 35.9 L442.4 36.0 L443.6 36.0 L444.8 36.0 L446.0 36.1 L447.2 36.1 L448.4 36.1 L449.6 36.2 L450.8 36.2 L452.0 36.2 L453.2 36.3 L454.4 36.3 L455.6 36.3 L456.8 36.4 L458.0 36.4 L459.2 36.4 L460.4 36.5 L461.6 36.5 L462.8 36.5 L464.0 36.6 L465.2 36.6 L466.4 36.6 L467.6 36.7 L468.8 36.7 L470.0 36.7 L471.2 36.8 L472.4 36.8 L473.6 36.8 L474.8 36.9 L476.0 36.9 L477.2 36.9 L478.4 37.0 L479.6 37.0 L480.8 37.0 L482.0 37.1 L483.2 37.1 L484.4 37.1 L485.6 37.2 L486.8 37.2 L488.0 37.2 L489.2 37.3 L490.4 37.3 L491.6 37.3 L492.8 37.4 L494.0 37.4 L495.2 37.4 L496.4 37.5 L497.6 37.5 L498.8 37.5 L500.0 37.6 L501.2 37.6 L502.4 37.6 L503.6 37.7 L504.8 37.7 L506.0 37.7 L507.2 37.8 L508.4 37.8 L509.6 37.8 L510.8 37.9 L512.0 37.9 L513.2 37.9 L514.4 38.0 L515.6 38.0 L516.8 38.0 L518.0 38.0 L519.2 38.1 L520.4 38.1 L521.6 38.1 L522.8 38.2 L524.0 38.2 L525.2 38.2 L526.4 38.3 L527.6 38.3 L528.8 38.3 L530.0 38.3 L531.2 38.4 L532.4 38.4 L533.6 38.4 L534.8 38.5 L536.0 38.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 3" stroke-opacity="0.7"/>
  <circle cx="89.7" cy="35.2" r="2.6" fill="currentColor"/>
  <text x="96.7" y="30.2" font-size="10.5" fill="currentColor">4.3 % overshoot on every curve</text>
  <line x1="56.0" y1="192.0" x2="86.0" y2="192.0" stroke="currentColor" stroke-width="2" />
  <text x="94.0" y="196.0" font-size="11" fill="currentColor" xml:space="preserve">q/r = 100 · ω<tspan dy="3" font-size="10">n</tspan><tspan dy="-3"> = 3.16 rad/s</tspan> · settles in 1.8 s</text>
  <line x1="56.0" y1="208.0" x2="86.0" y2="208.0" stroke="currentColor" stroke-width="1.7" stroke-dasharray="7 4" stroke-opacity="0.8"/>
  <text x="94.0" y="212.0" font-size="11" fill="currentColor" xml:space="preserve">q/r = 1 · ω<tspan dy="3" font-size="10">n</tspan><tspan dy="-3"> = 1.00 rad/s</tspan> · settles in 5.7 s</text>
  <line x1="56.0" y1="224.0" x2="86.0" y2="224.0" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 3" stroke-opacity="0.7"/>
  <text x="94.0" y="228.0" font-size="11" fill="currentColor" xml:space="preserve">q/r = 0.01 · ω<tspan dy="3" font-size="10">n</tspan><tspan dy="-3"> = 0.32 rad/s</tspan> · settles in 17.9 s</text>
</svg>

The cart's step response under LQR for the table's first three rows. Every curve has the same $\zeta = 0.707$, so the same $4.3\,\%$ overshoot, and they settle in $1.8$, $5.7$ and $17.9\,\mathrm{s}$: a factor of $100$ in $q/r$ buys only $\sqrt{10}$ in speed.

### 4. LQG's fine print

The controller never sees $x$, only a noisy reading $y$. Can LQR's gain run on an estimate of the state, and what does that cost? **LQG** — LQR with Gaussian noise and partial observation — answers: yes, and exactly, for the nominal model — estimate optimally with a Kalman filter, then control the estimate optimally with the LQR gain, and the pair is jointly optimal — at the price of every robustness guarantee LQR had.

**The LQG problem, written out.** Both the dynamics and the sensor carry zero-mean Gaussian white
noise, independent of each other ([[02-foundations/probability|3. Probability §5.2]]):

$$x_{k+1} = Ax_k + Bu_k + w_k, \qquad y_k = Cx_k + v_k, \qquad w_k \sim \mathcal N(0, W), \quad v_k \sim \mathcal N(0, V)$$

Here $W$ and $V$ are the process and measurement noise covariances. [[02-foundations/probability|3. Probability §5.2]] and [[04-robotics/state-estimation-slam|3. State Estimation §5]] both call them $Q$ and $R$; they are renamed here because $Q$ and $R$ are already the cost weights. The filter is the one you met in 3. State Estimation §5, which also writes $H$ for $C$, $z$ for the reading $y$, and $\nu$ for the innovation $y - C\hat x^-$. $u_k$ may use
only the measurements up to step $k$. The objective is the expected LQR cost per step,
$\lim_{T\to\infty}\tfrac1T E\big[\sum_{k<T} (x_k^\top Q x_k + u_k^\top R u_k)\big]$, since the noise
never lets the state settle. The solution has three named parts:
- a **Kalman filter** that produces $\hat x_k$, with a gain $L$ from a filter Riccati equation that
  involves only $A, C, W, V$ — $L$ is the Kalman gain the estimation pages call $K$, renamed here
  because $K$ is the LQR gain, and it plays the role of [[04-robotics/control-theory-ce397|5. Control Theory §8]]'s observer gain $L$;
- an **LQR gain** $K$ from the DARE of §1.5, which involves only $A, B, Q, R$;
- the **certainty-equivalent controller** $u_k = -K\hat x_k$, which treats the estimate as if it
  were the true state.

That the two gains can be computed separately and the combination is still optimal is the
**separation principle**; its pole version, closed-loop eigenvalues equal to those of $A - BK$
together with those of $A - LC$, is derived in
[[04-robotics/control-theory-ce397|5. Control Theory §8]] for the continuous-time observer. (For the discrete filter in the estimation pages' predict–correct form the estimation error evolves by $(I - LC)A$, whose eigenvalues are those of $A - ALC$; the two agree when $A = 1$, as in the example below.) Existence needs $(A, B)$ stabilizable and
$(A, Q^{1/2})$ detectable for the controller, and the dual pair of conditions for the filter.
*Example:* with $A = B = C = 1$ and $Q = R = W = V = 1$, both Riccati equations reduce to
$P^2 - P - 1 = 0$. On the controller side $P = 1.618$ is §1.5's cost-to-go. On the filter side the
root $1.618$ is the *predicted* covariance $P^-$ of the estimation pages, and the corrected
$P^+ = 0.618$ solves [[04-robotics/state-estimation-slam|3. State Estimation §5]]'s $P^2 + qP - q = 0$ at $q = 1$. So the LQR gain $K$
and the steady-state Kalman gain $L = P^-/(P^- + V)$ are both $0.618$, the duality made literal.

The separation principle is exact for linear-Gaussian models — and famously fragile:
**LQG has no guaranteed robustness margins** (Doyle 1978's one-line abstract: "there are
none"; gain, phase and stability margins are defined in
[[04-robotics/control-theory-ce397|5. Control Theory §5.5]]). Estimator error and model error interact; real systems re-introduce margin checks
or robust variants. Read "we use LQG" as *nominal-optimal, robustness unverified unless
shown*.

*Non-example, with numbers — Doyle's own system.* In continuous time, where $W$ and $V$ are noise
intensities, take $\dot x=\begin{pmatrix}1&1\\0&1\end{pmatrix}x+\begin{pmatrix}0\\1\end{pmatrix}u+\begin{pmatrix}1\\1\end{pmatrix}w$ and
$y=x_1+v$, with $Q=60\begin{pmatrix}1&1\\1&1\end{pmatrix}$, $R=1$, process-noise intensity $60$ on the
scalar $w$ and $V=1$. Both Riccati equations return the same round numbers, $K=(10,\ 10)$ and
$L=(10,\ 10)^\top$. Now let the actuator deliver $m\,u$ where the model assumed $u$. Fed the true
state, $u=-Kx$, the loop is stable for every $m>0.2$, because its characteristic polynomial is
$\lambda^2+(10m-2)\lambda+1$. Fed the Kalman estimate, $u=-K\hat x$, it is stable only for
$0.930<m<1.010$: an actuator one percent stronger than modelled destabilizes the jointly optimal
controller. Nothing in the separation principle is violated — it never promised anything about
$m\neq1$ — and that is the whole point of Doyle's one-line abstract.

**Why study it**: LQR is the reference point everything else is measured against —
[[04-robotics/mpc|7. MPC]], the next page, is "LQR + constraints, re-solved online" (its terminal cost $P$
is typically the LQR Riccati solution, §1.5's); RL policy iteration or policy optimization on
linear-quadratic problems recovers LQR (evaluation alone only prices a fixed gain); and time-varying LQR around a trajectory is the
standard tracking controller that learned planners hand their outputs to.

### After reading

- [ ] State the LQR problem and the form of its solution ($u=-Kx$, $K=R^{-1}B^\top P$)
- [ ] Solve a scalar Riccati equation by hand, pick the stabilizing root, and check that $J = P$
- [ ] Write the DARE and its gain, and solve it on the discrete integrator
- [ ] Say what stabilizability and detectability each guarantee, and what fails without them
- [ ] Explain with the worked example how the $Q/R$ ratio changes gains, response, and saturation risk
- [ ] State the separation principle and its fragility (LQG has no guaranteed margins), map its $W$, $V$ and $L$ onto the estimation pages' $Q$, $R$ and $K$, and say why LQR is the reference point for MPC and RL

### Self-check

1. What happens to the Riccati approach if $(A,B)$ is not stabilizable?
2. On the double integrator, scale $Q$ by 10 and $R$ by 10 together — what happens to $K$?
3. In one sentence: why is "LQG is optimal, therefore robust" wrong?
4. Why use LQR's $P$ as the MPC terminal cost?

> [!tip]- Answers
> 1. No feedback can catch the unstable mode, so no stabilizing solution $P$ exists — the problem itself is ill-posed.
> 2. Unchanged — multiplying all of $Q$ and $R$ by the same positive scalar changes only the overall cost scale. Relative weights within matrix-valued $Q$ and $R$ still determine $K$.
> 3. Optimality is with respect to the nominal model, and LQG is proven to have no guaranteed margins against model error (Doyle 1978).
> 4. $x^\top P x$ is the exact cost-to-go inside a terminal set where the LQR law satisfies the constraints and keeps the state in the set. With that terminal constraint added, a short horizon still supports the stability argument — the terminal cost and terminal set together are the ingredients of [[04-robotics/mpc|7. MPC §5]]'s stability argument, the Mayne conditions (Borrelli Theorem 12.2).

### Problem set · 과제

Tier B. **P4**, the catalog's leaky heater $\dot x=-x+u+d$ from [[02-foundations/lab-plants|0.6]], now priced at $Q=3$, $R=1$. No simulator.

1. **Draw.** The picture above at the problem set's weights, $Q=3$, $R=1$: the leaky heater with $u=-Kx$, boxes for $Q$ and $R$, disturbance $d$, and the Riccati arrow labelled with this $P$ and $K$. On the pole axis mark this closed-loop pole and, beside the picture's $Q=1$, $R=1$ pole, the one for $Q=1$, $R=4$; say which way raising $R$ moves a pole.
2. **Derive.** (a) The scalar ARE at $Q=3$, $R=1$: its two roots, the stabilizing $P$ and $K$, the closed-loop pole, and $x_\mathrm{ss}$ for $d=1$. (b) The ledger's price of three gains from $x_0=1$ with $d=0$: $J(K)=(3+K^2)/(2(1+K))$ at your $K$, at $K=0$ and at 5 §1's hand gain $K=9$; check that the smallest is $P$. (c) The twist: which $Q/R$ makes LQR choose $K=9$ itself? Give its pole and $x_\mathrm{ss}$.
3. **Interpret.** Part (c) says that 5 §1's hand gain is LQR-optimal for some weights. Show that on P4 every gain $K\ge0$ is, say what that means for a paper that reports "we used LQR" but not its $Q$ and $R$, and say what raising $Q/R$ buys and costs (the $(1+K)$ trade of [[04-robotics/control-theory-ce397|5. Control Theory §1]]).

> [!note]- How to draw it · 그리는 법
> - The loop: a summing junction, the plant box $\dot x=-x+u+d$ after it, the disturbance $d$ entering at that junction beside $u$, the state $x$ leaving the box, and a feedback path from $x$ through a gain block $-K$ back into the junction. That much is the control page's picture, unchanged.
> - The ledger, which is what LQR adds: a branch from $x$ into a box $Q$, a branch from $u$ into a box $R$, and both into an accumulator labelled $J=\int_0^\infty (Qx^2+Ru^2)\,dt$.
> - Draw the ledger with a different line weight, because it never touches the plant: it is an accounting path, not a control path, and keeping it visually separate is how $Q$ and $R$ stay distinct from the noise covariances $W$ and $V$ that enter the same loop in §4.
> - Beside the $-K$ block, the single arrow the Riccati equation is, $(Q,R)\rightarrow P\rightarrow K$, labelled *offline, once*, with this set's numbers on it, $(3,1)\rightarrow1\rightarrow1$, not the picture's $1.236$.
> - Under the loop, a real axis with the open-loop pole at $-1$, where the uncontrolled heater already sits, and the closed-loop pole at $-(1+K)$.
> - On this plant the stabilizing Riccati solution is $P=-R+\sqrt{R^2+QR}$ and $K=P/R=-1+\sqrt{1+Q/R}$, so the closed-loop pole lands at $-\sqrt{1+Q/R}$: $-2$ at $Q=3$, $R=1$, and $-1.118$ at $Q=1$, $R=4$, to the right of the picture's $-1.414$.
> - The arrow worth drawing: raising $R$ slides a pole back toward $-1$, exactly as lowering $Q$ would, because only the ratio $Q/R$ appears.

> [!tip]- Solutions
> 1. The picture's loop and ledger at $Q=3$, $R=1$; the Riccati arrow reads $(3,1)\rightarrow P=1\rightarrow K=1$. On the axis: the open-loop pole $-1$, this closed-loop pole $-\sqrt{1+Q/R}=-2$, and at $Q=1$, $R=4$ the pole $-\sqrt{1.25}=-1.118$, from $P=-4+\sqrt{20}=0.472$ and $K=P/R=0.118$ — to the right of the picture's $-1.414$ at $Q=1$, $R=1$. Raising $R$ slides a pole back toward $-1$: only $Q/R$ sets it, so pricing effort up is the same move as pricing error down.
> 2. (a) $-2P-P^2+3=0$, that is $(P-1)(P+3)=0$, so $P=1$ or $P=-3$. The stabilizing root is $P=1$, so $K=1$, the pole is $-(1+K)=-2$ and $x_\mathrm{ss}=1/2=0.5$; the root $-3$ would give $K=-3$ and $\dot x=+2x$. (b) $J(1)=4/4=1.0=P$, $J(0)=3/2=1.5$ and $J(9)=84/20=4.2$: the open loop costs half as much again as LQR, and the hand gain more than four times as much. (c) $K=-1+\sqrt{1+Q/R}=9$ exactly when $1+Q/R=100$, so $Q/R=99$; the pole is $-10$ and $x_\mathrm{ss}=0.1$.
> 3. Inverting $K=-1+\sqrt{1+\rho}$ gives $\rho=Q/R=(1+K)^2-1=K^2+2K$, which is $\ge0$ for every $K\ge0$. So every non-negative gain on this plant, hand-picked or not, is LQR-optimal for the weights $Q/R=K^2+2K$ — $3$ for $K=1$, $24$ for $K=4$, $99$ for $K=9$. "Optimal" without the weights therefore says nothing about how hard the loop acts; the weights are the design. Raising $Q/R$ raises $K$, which buys a smaller $x_\mathrm{ss}=d/(1+K)$ — at $Q/R=99$ ten times smaller than the open loop's — and costs effort, $u=-Kx$, and noise, since sensor noise enters $u$ through the same $K$: 5 §1's trade.

### Sources

- R. E. Kalman, "Contributions to the theory of optimal control," *Boletín de la Sociedad Matemática Mexicana* 5, 1960 — the infinite-horizon linear-quadratic regulator and its Riccati equation.
- B. D. O. Anderson and J. B. Moore, *Optimal Control: Linear Quadratic Methods*, Prentice Hall, 1990 (Dover reprint, 2007) — the standard text for §1–§4: the continuous and discrete Riccati equations, stabilizability and detectability, and LQG.
- J. C. Doyle, "Guaranteed margins for LQG regulators," *IEEE Transactions on Automatic Control* 23(4), 1978 — §4's example and its one-line abstract.
- F. Borrelli, A. Bemporad and M. Morari, *Predictive Control for Linear and Hybrid Systems*, Cambridge University Press, 2017 — Theorem 12.2, cited in self-check 4.
- R. Tedrake, *Underactuated Robotics*, the LQR chapter (online text, linked at the top) — geometric intuition and code.
- The lecture slides linked at the top — finite-horizon discrete-time LQR first, then its derivation with Lagrange multipliers, the infinite horizon and continuous time; read them after §1.5, then connect to the MPC-as-QP example of [[02-foundations/optimization|4. Optimization §5]].
- Every number on this page was worked by hand from the page's own equations and checked with NumPy.

## 한국어

*[[04-robotics/control-theory-ce397|5. 제어 이론]]과 확률·최적화 위에 선다. D군이다. 극점을 손으로 고르는 대신 비용이 고르게 하고,
분리 원리가 추정기와 제어기를 따로 설계해도 되는 조건을 말해 준다.*

> [!note] 왜 배우는가 · Why this matters
> [[physical-ai-map|피지컬 AI 지도]]에서 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 로봇 스택 옆 제어 열에 있고, "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계를 받친다. 오차와 노력에 값을 매겨서 팔이나 패널을 계획대로 끌고 가는 피드백 이득을 고르고, 칼만 필터의 추정값 위에서 LQR을 돌리는 LQG 쪽(§4)은 *패널과 프레임을 식별하는* 단계의 믿음([[04-robotics/state-estimation-slam|3. 상태 추정 §5]])이 제어기로 들어오는 자리다. 비용 없이 고른 이득은 취향일 뿐이고, "최적"이라는 말은 들리는 것보다 적게 말한다. 카탈로그의 새는 히터 **P4**([[02-foundations/lab-plants|0.6]])에서 $Q = 4$, $R = 1$의 최적 이득은 $K = 1.236$(극점 $-2.236$, $d = 1$이면 $x_{ss} = 0.447$)으로, [[04-robotics/control-theory-ce397|5. 제어 이론 §1]]이 손으로 고른 $K = 9$보다 훨씬 부드럽다('대상으로 한 번 끝까지'). 그리고 Doyle의 시스템에서는 결합 최적인 LQG 루프가 구동기가 모델보다 $1\,\%$만 세도 불안정해진다($0.930 < m < 1.010$, §4). [[04-robotics/mpc|7. MPC §5]]는 §1.5의 이산 리카티 해 $P = 1.618$을 안정성 논증의 종단 비용으로 다시 쓰고, [[04-robotics/convex-mpc-legged|8. Convex MPC §2]]는 같은 꼴의 이차 비용을 걷는 로봇에서 수십 Hz로 다시 푼다. 둘 다 이 페이지와 함께 학위논문 경로([[07-research-program/index|7 §8]])의 블록 2에 있다(이 페이지는 로보틱스 75–76회차). 이 페이지를 마치면 스칼라 리카티 방정식을 손으로 풀고, 안정화 가능성과 검출 가능성을 확인하고, "$Q/R$을 튜닝했다"와 "LQG를 쓴다"가 무엇을 약속하고 무엇을 약속하지 않는지 읽을 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 두 회차, 로보틱스 75–76회차다. **1회차:** 이 페이지의 대상, 그림, 그리고 P4를 손으로 푸는 '대상으로 한 번 끝까지'. $P = K = 1.236$, 극점 $-2.236$, $x_{ss} = 0.447$, 그리고 $J = P$ 검산이다. 이어서 같은 단계를 행렬로 되풀이하는 §1과 §2. 끝나면 ARE를 항마다 읽고, §2의 두 조건이 각각 무엇을 사 주는지 말할 수 있어야 한다. **2회차:** 이산 시간 쌍둥이인 §1.5(이산 적분기에서 $P = 1.618$, $K = 0.618$, [[04-robotics/mpc|7. MPC]]가 다시 쓰는 숫자다), §3과 §4, 그다음 스스로 점검과 과제. §1의 접힌 *더 깊이* 메모는 두 번째 읽기다. 10분뿐이라면 §2를 읽어라. "LQR은 안정성이 보장된다"에는 조건이 둘 붙어 있고, 비선형계를 선형화해 쓰는 논문은 그 조건을 선형화 지점에서만 물려받는다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P4**, 곧 카탈로그의 새는 히터다. 1차 장치라서 모델 전체가 한 줄이다:

$$\dot x = -x + u + d$$

$x$는 온도 오차, $u$는 명령, $d$는 모르는 외란이다. LQR의 글자로는 $A = -1$, $B = 1$이고, 개루프 극점은 $-1$에 있다. [[04-robotics/control-theory-ce397|5. 제어 이론 §1]]의 장치이고, 거기서 피드백 $u = -Kx$는 $x_{ss} = d/(1+K)$를 남기며 손으로 고른 이득 $K = 9$가 $d$를 10분의 1로 줄였다. 이 페이지는 그 절이 설계자에게 맡겨 둔 질문을 이 장치 위에서 묻는다. 어떤 $K$가 가장 좋은가, 그리고 무엇으로 재서 그런가?

**그 잣대를 식으로.** **LQR**(선형 이차 조정기, linear quadratic regulator)은 최적 제어에서 정확히 풀리는 심장부다. 선형 동역학과 이차 비용에 대해 무한 지평 LQR 문제는

$$\min_{u(\cdot)}\; J = \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt \quad \text{subject to} \quad \dot x = Ax + Bu,\;\; x(0) = x_0$$

이고 이름 붙은 재료가 넷이다. 선형 모델 $(A, B)$; 원점에서 벗어난 것에 값을 매기는 **상태 가중치** $Q$, 양의 준정부호(모든 $x$에서 $x^\top Q x \ge 0$); 노력에 값을 매기는 **입력 가중치** $R$, 양의 정부호(모든 $u \ne 0$에서 $u^\top R u > 0$이라 $R^{-1}$이 존재)이며 공짜 입력이 없도록 엄격히 양수여야 한다; 그리고 무한 지평, 이것 때문에 최적 이득이 시변이 아니라 상수다. (정부호성은 [[02-foundations/linear-algebra|1. 선형대수 §3]]에서 정의한다.) P4에서는 넷이 모두 스칼라이고 비용은 $J = \int_0^\infty (Qx^2 + Ru^2)\,dt$다. 기준 궤적 추종은 오차 좌표 $x - x_{ref}$로 쓴 같은 문제다.

**쓰이는 자리에서 고정하는 대상 넷:** §1의 불안정한 스칼라 $\dot x = x + u$, [[04-robotics/mpc|7. MPC]]가 다시 쓰는 §1.5의 이산 적분기 $x_{k+1} = x_k + u_k$, §3의 카트(직선 위의 단위 질량으로, 위치 $p$와 속도 $v$를 갖고 힘 $u$로 밀린다. 이중 적분기 $\ddot p = u$), 그리고 §4의 상태 둘인 Doyle의 시스템이다.

*범위: 이 페이지는 연속 시간과 이산 시간의 무한 지평 LQR, 그 해가 존재하고 안정화하는 조건, $Q$와 $R$이 응답에 하는 일, 그리고 LQG의 분리 원리와 그것에 없는 여유를 가르친다. 유한 지평·시변 LQR은 이름만 대고, 리카티 해법과 강건 제어는 가르치지 않는다. 칼만 필터 자체는 [[04-robotics/state-estimation-slam|3. 상태 추정 §5]]가 가르친다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 376" style="max-width:100%;height:auto" role="img" aria-label="위: 외란이 합산점으로 들어오는 새는 히터 P4의 피드백 루프와, x에는 Q로 u에는 R로 값을 매겨 J로 모으는 파선 장부. 아래: 개루프 극점 -1, Q = 1의 폐루프 극점 -1.414, Q = 4의 폐루프 극점 -2.236을 찍은 실수축.">
  <defs><marker id="aLQRk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6" fill="none">
    <circle cx="96" cy="80" r="11"/>
    <rect x="160" y="60" width="160" height="40" rx="3"/>
    <rect x="238" y="138" width="60" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aLQRk)">
    <line x1="96" y1="26" x2="96" y2="68"/>
    <line x1="107" y1="80" x2="158" y2="80"/>
    <line x1="320" y1="80" x2="424" y2="80"/>
    <polyline points="380,80 380,152 300,152"/>
    <polyline points="238,152 96,152 96,92"/>
  </g>
  <circle cx="380" cy="80" r="3" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-dasharray="4 3" stroke-opacity="0.75">
    <polyline points="424,80 452,80"/>
    <polyline points="472,94 472,204"/>
    <polyline points="140,152 140,204"/>
    <polyline points="160,218 300,218"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.75">
    <rect x="452" y="66" width="40" height="28" rx="3"/>
    <rect x="120" y="204" width="40" height="28" rx="3"/>
    <rect x="300" y="204" width="240" height="28" rx="3"/>
  </g>
  <circle cx="140" cy="152" r="2.6" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="50" y1="306.0" x2="519.5" y2="306.0"/>
    <line x1="470" y1="301.0" x2="470" y2="311.0"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.45">
    <line x1="170" y1="303.0" x2="170" y2="309.0"/>
    <line x1="320" y1="303.0" x2="320" y2="309.0"/>
  </g>
  <g stroke="currentColor" fill="none">
    <path d="M314.5 300.5 L325.5 311.5 M314.5 311.5 L325.5 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M252.4 300.5 L263.4 311.5 M252.4 311.5 L263.4 300.5" stroke-width="1.6" stroke-opacity="0.6"/>
    <path d="M129.1 300.5 L140.1 311.5 M129.1 311.5 L140.1 300.5" stroke-width="2.4" stroke-opacity="1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aLQRk)">
    <line x1="320" y1="282.0" x2="138.6" y2="282.0"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="96" y="84">Σ</text>
    <text x="240" y="85">ẋ = −x + u + d</text>
    <text x="268" y="157">−K</text>
    <text x="472" y="85">Q</text>
    <text x="140" y="223">R</text>
    <text x="420" y="223">J = ∫<tspan font-size="10" dy="4">0</tspan><tspan font-size="10" dy="-10">∞</tspan><tspan dy="6"> (Qx² + Ru²) dt</tspan></text>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="104" y="38">d</text>
    <text x="360" y="73">x</text>
    <text x="182" y="146">u</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="240" y="52" text-anchor="middle" opacity="0.85">P4, 새는 히터</text>
    <text x="268" y="184" text-anchor="middle">(Q, R) → P → K: 오프라인에서 한 번</text>
    <text x="268" y="198" text-anchor="middle" opacity="0.85">Q = 4, R = 1이면 P = K = 1.236</text>
    <text x="540" y="250" text-anchor="end" opacity="0.8">장부: 회계 경로이며 장치를 전혀 건드리지 않는다</text>
    <text x="227.3" y="275.0" text-anchor="middle">Q/R을 올리면 폐루프 극점이 왼쪽으로 미끄러진다</text>
    <text x="170" y="298.0" text-anchor="middle" font-size="10" opacity="0.8">−2</text>
    <text x="328" y="326.0">−1</text>
    <text x="328" y="340.0" opacity="0.85">개루프</text>
    <text x="257.9" y="326.0" text-anchor="middle" opacity="0.85">−√2 = −1.414</text>
    <text x="257.9" y="340.0" text-anchor="middle" opacity="0.85">Q = 1</text>
    <text x="134.6" y="326.0" text-anchor="middle">−√5 = −2.236</text>
    <text x="134.6" y="340.0" text-anchor="middle">Q = 4, 대상으로 한 번 끝까지</text>
    <text x="470" y="326.0" text-anchor="middle">0</text>
    <text x="523.5" y="310.0">Re s</text>
    <text x="12" y="363" opacity="0.9">R = 1에서 폐루프 극점 −(1 + K) = −√(1 + Q), 그림의 나머지는 움직이지 않는다</text>
  </g>
</svg>

[[04-robotics/control-theory-ce397|5. 제어 이론 §1]]의 새는 히터 **P4**, $\dot x=-x+u+d$가 $-K$를 거치는 피드백 루프에 있고, 그 옆에 LQR이 더하는 장부가 파선으로 붙어 있다. 장부는 $x$에는 $Q$, $u$에는 $R$로 값을 매겨 $J=\int_0^\infty (Qx^2+Ru^2)\,dt$에 모을 뿐 장치를 전혀 건드리지 않고, 리카티 방정식은 오프라인에서 한 번 도는 화살표 $(Q,R)\rightarrow P\rightarrow K$ 하나다($Q=4$, $R=1$이면 $P=K=1.236$). 아래 $s$-평면([[02-foundations/engineering-math|0.5 §9]])의 실수축 $\mathrm{Re}\,s$에는 개루프 극점 $-1$과, $R=1$에서 $-(1+K)=-\sqrt{1+Q}$인 폐루프 극점($Q=1$이면 $-\sqrt2=-1.414$, $Q=4$면 $-\sqrt5=-2.236$)이 있고, $Q/R$을 올리면 그 극점이 왼쪽으로 미끄러질 뿐 그림의 나머지는 움직이지 않는다.

### 대상으로 한 번 끝까지 · Worked case

$Q = 4$, $R = 1$인 P4를 네 단계로 손으로 푼다. §1은 같은 네 단계를 행렬로 되풀이한다.

**1단계 — 상태의 값을 추측한다.** cost-to-go $V(x)$는 상태 $x$에서 아직 달성할 수 있는 가장 작은 비용 $J$다(어떤 계에서든 쓸 수 있게 §1이 정의한다). 선형 장치와 이차 비용에서는 그것도 이차식이다. $V(x) = Px^2$로 추측하고, 맞아떨어진다는 사실로 사후에 정당화한다. 숫자 하나 $P$가 $x = 1$에 서 있는 값이다.

**2단계 — 최적성 조건을 $u$에 대해 최소화한다.** 최적에서는 지금 치르는 비용과 운동을 따라 cost-to-go가 변하는 속도의 합이, 가장 좋은 입력을 고르고 나면 0이다(연속 시간 벨만 방정식, §1). $d = 0$으로 두고(비용은 조정기에 값을 매기는 것이고, $d$는 4단계에서 돌아온다) $V'(x) = 2Px$를 쓰면 그 조건은

$$0 = \min_u\big[\,4x^2 + u^2 + 2Px\,(-x + u)\,\big]$$

이다. 괄호 안은 $u$에 대한 포물선이고, 그 도함수 $2u + 2Px$는 $u^\star = -Px$에서 0이 되므로 이득은 $K = P/R = P$다. 고른 것이 아니라 값에서 떨어져 나온다.

**3단계 — 도로 넣고 $P$를 푼다.** $u^\star = -Px$를 넣으면 괄호는 $4x^2 + P^2x^2 - 2Px^2 - 2P^2x^2 = (4 - 2P - P^2)\,x^2$이고, 모든 $x$에서 0이어야 하므로

$$-2P - P^2 + 4 = 0 \quad\Rightarrow\quad P = -1 \pm \sqrt5$$

이며, 안정한 루프를 주는 것은 $P = -1 + \sqrt5 = 1.236$뿐이다. 다른 근 $-3.236$은 $K = -3.236$과 $\dot x = +2.236\,x$를 준다. 그래서 $P = K = 1.236$이다.

**4단계 — 답을 읽고, 값을 검산한다.** 폐루프는 $\dot x = -(1 + K)x + d = -2.236\,x + d$다. 극점이 개루프의 $-1$에서 $-2.236$으로 옮겨 가고, 상수 $d = 1$은 $x_{ss} = d/(1 + K) = 0.447$에 머문다. $d = 0$, $x_0 = 1$에서 $x = e^{-2.236t}$, $u = -1.236\,x$이므로

$$J = \int_0^\infty (4 + 1.236^2)\,e^{-4.472t}\,dt = \frac{5.528}{4.472} = 1.236 = P$$

이다. $e^{-at}$의 적분이 $1/a$이기 때문이다. $x_0 = 1$에서의 cost-to-go가 1단계가 말한 대로 $P$다.

**손 이득과 견주면.** [[04-robotics/control-theory-ce397|5. 제어 이론 §1]]은 10배 억제를 위해 손으로 $K = 9$를 골랐고(극점 $-10$, $x_{ss} = 0.1$), 그 페이지의 과제는 $K = 4$를 돌린다(극점 $-5$, $x_{ss} = 0.2$). $2.236$ 자리에 $1 + K$를 넣은 같은 적분이 이 장부 위의 모든 이득에 값을 매긴다. $x_0 = 1$에서 $J(K) = (4 + K^2)/(2(1 + K))$이고, 아래 그림이 그것을 그린다. $Q = 4$는 상태에 노력보다 높은 값을 매기므로 LQR이 움직이긴 하지만 부드럽게 움직인다. 손 이득은 이 장부가 값을 치를 만하다고 보는 것보다 더 많은 억제를 산다. $Q/R$을 올리는 것이 5 §1의 $(1+K)$ 거래다. $x_{ss}$는 줄고, 노력과 증폭되는 센서 잡음은 는다.

<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="Q = 4, R = 1인 P4에서 x0 = 1부터 잰, 이득 K마다의 장부 가격 J: 최솟값 1.236이 K = 1.236에 있고, 개루프 K = 0과 손 이득 K = 4는 둘 다 2.0, 손 이득 K = 9는 4.25인 곡선.">
  <g stroke="currentColor" stroke-width="1" fill="none"><line x1="70.0" y1="30.0" x2="70.0" y2="200.0"/><line x1="70.0" y1="200.0" x2="520.0" y2="200.0"/></g>
  <g stroke="currentColor" stroke-width="1"><line x1="66.0" y1="200.0" x2="70.0" y2="200.0"/><line x1="66.0" y1="166.0" x2="70.0" y2="166.0"/><line x1="66.0" y1="132.0" x2="70.0" y2="132.0"/><line x1="66.0" y1="98.0" x2="70.0" y2="98.0"/><line x1="66.0" y1="64.0" x2="70.0" y2="64.0"/><line x1="66.0" y1="30.0" x2="70.0" y2="30.0"/><line x1="70.0" y1="200.0" x2="70.0" y2="204.0"/><line x1="160.0" y1="200.0" x2="160.0" y2="204.0"/><line x1="250.0" y1="200.0" x2="250.0" y2="204.0"/><line x1="340.0" y1="200.0" x2="340.0" y2="204.0"/><line x1="430.0" y1="200.0" x2="430.0" y2="204.0"/><line x1="520.0" y1="200.0" x2="520.0" y2="204.0"/></g>
  <g font-size="10" fill="currentColor" text-anchor="end"><text x="63.0" y="203.5">0</text><text x="63.0" y="169.5">1</text><text x="63.0" y="135.5">2</text><text x="63.0" y="101.5">3</text><text x="63.0" y="67.5">4</text><text x="63.0" y="33.5">5</text></g>
  <g font-size="10" fill="currentColor" text-anchor="middle"><text x="70.0" y="215.0">0</text><text x="160.0" y="215.0">2</text><text x="250.0" y="215.0">4</text><text x="340.0" y="215.0">6</text><text x="430.0" y="215.0">8</text><text x="520.0" y="215.0">10</text></g>
  <text x="63.0" y="22.0" font-size="11" fill="currentColor">x₀ = 1에서의 비용 J</text>
  <text x="528.0" y="204.0" font-size="11" fill="currentColor">K</text>
  <line x1="70.0" y1="132.0" x2="250.0" y2="132.0" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <path d="M70.0 132.0 L72.2 135.2 L74.5 138.0 L76.8 140.5 L79.0 142.8 L81.2 144.8 L83.5 146.5 L85.8 148.1 L88.0 149.5 L90.2 150.7 L92.5 151.8 L94.8 152.8 L97.0 153.7 L99.2 154.4 L101.5 155.1 L103.8 155.7 L106.0 156.2 L108.2 156.6 L110.5 157.0 L112.8 157.3 L115.0 157.5 L117.2 157.7 L119.5 157.8 L121.8 157.9 L124.0 158.0 L126.2 158.0 L128.5 157.9 L130.8 157.9 L133.0 157.8 L135.2 157.7 L137.5 157.5 L139.8 157.3 L142.0 157.1 L144.2 156.9 L146.5 156.6 L148.8 156.3 L151.0 156.0 L153.2 155.7 L155.5 155.4 L157.8 155.0 L160.0 154.7 L162.2 154.3 L164.5 153.9 L166.8 153.5 L169.0 153.0 L171.2 152.6 L173.5 152.1 L175.8 151.7 L178.0 151.2 L180.2 150.7 L182.5 150.2 L184.8 149.7 L187.0 149.2 L189.2 148.7 L191.5 148.1 L193.8 147.6 L196.0 147.0 L198.2 146.5 L200.5 145.9 L202.8 145.3 L205.0 144.8 L207.2 144.2 L209.5 143.6 L211.8 143.0 L214.0 142.4 L216.2 141.8 L218.5 141.1 L220.8 140.5 L223.0 139.9 L225.2 139.2 L227.5 138.6 L229.8 138.0 L232.0 137.3 L234.3 136.7 L236.5 136.0 L238.8 135.4 L241.0 134.7 L243.2 134.0 L245.5 133.4 L247.8 132.7 L250.0 132.0 L252.2 131.3 L254.5 130.6 L256.8 129.9 L259.0 129.3 L261.2 128.6 L263.5 127.9 L265.8 127.2 L268.0 126.5 L270.2 125.8 L272.5 125.0 L274.8 124.3 L277.0 123.6 L279.2 122.9 L281.5 122.2 L283.8 121.5 L286.0 120.7 L288.2 120.0 L290.5 119.3 L292.8 118.6 L295.0 117.8 L297.2 117.1 L299.5 116.4 L301.8 115.6 L304.0 114.9 L306.2 114.2 L308.5 113.4 L310.8 112.7 L313.0 111.9 L315.2 111.2 L317.5 110.4 L319.8 109.7 L322.0 108.9 L324.2 108.2 L326.5 107.4 L328.8 106.7 L331.0 105.9 L333.2 105.1 L335.5 104.4 L337.8 103.6 L340.0 102.9 L342.3 102.1 L344.5 101.3 L346.8 100.6 L349.0 99.8 L351.2 99.0 L353.5 98.3 L355.8 97.5 L358.0 96.7 L360.2 95.9 L362.5 95.2 L364.8 94.4 L367.0 93.6 L369.2 92.8 L371.5 92.1 L373.8 91.3 L376.0 90.5 L378.2 89.7 L380.5 88.9 L382.8 88.2 L385.0 87.4 L387.3 86.6 L389.5 85.8 L391.8 85.0 L394.0 84.2 L396.2 83.4 L398.5 82.7 L400.8 81.9 L403.0 81.1 L405.2 80.3 L407.5 79.5 L409.8 78.7 L412.0 77.9 L414.2 77.1 L416.5 76.3 L418.8 75.5 L421.0 74.7 L423.2 73.9 L425.5 73.1 L427.8 72.4 L430.0 71.6 L432.3 70.8 L434.5 70.0 L436.8 69.2 L439.0 68.4 L441.2 67.6 L443.5 66.8 L445.8 66.0 L448.0 65.2 L450.3 64.4 L452.5 63.6 L454.8 62.7 L457.0 61.9 L459.2 61.1 L461.5 60.3 L463.8 59.5 L466.0 58.7 L468.2 57.9 L470.5 57.1 L472.8 56.3 L475.0 55.5 L477.3 54.7 L479.5 53.9 L481.8 53.1 L484.0 52.3 L486.2 51.5 L488.5 50.6 L490.8 49.8 L493.0 49.0 L495.3 48.2 L497.5 47.4 L499.8 46.6 L502.0 45.8 L504.2 45.0 L506.5 44.2 L508.8 43.3 L511.0 42.5 L513.2 41.7 L515.5 40.9 L517.8 40.1 L520.0 39.3" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="322.0" y="123.5" font-size="11" fill="currentColor">J(K) = (4 + K²) / (2(1 + K))</text>
  <circle cx="70.0" cy="132.0" r="3.2" fill="currentColor"/>
  <circle cx="125.6" cy="158.0" r="4" fill="currentColor"/>
  <circle cx="250.0" cy="132.0" r="3.2" fill="currentColor"/>
  <circle cx="475.0" cy="55.5" r="3.2" fill="currentColor"/>
  <text x="76.0" y="124.0" font-size="10.5" fill="currentColor">개루프, K = 0: J = 2.0</text>
  <text x="129.6" y="175.0" font-size="10.5" fill="currentColor" font-weight="bold">LQR, K = P = 1.236: J = 1.236</text>
  <text x="257.0" y="147.0" font-size="10.5" fill="currentColor">K = 4 (5의 과제): J = 2.0</text>
  <text x="469.0" y="47.5" font-size="10.5" fill="currentColor" text-anchor="end">K = 9 (5 §1): J = 4.25</text>
  <g font-size="10" fill="currentColor" opacity="0.85"><text x="64.0" y="232.0" text-anchor="start">극점 −1</text><text x="125.6" y="232.0" text-anchor="middle">−2.24</text><text x="250.0" y="232.0" text-anchor="middle">−5</text><text x="475.0" y="232.0" text-anchor="middle">−10</text></g>
</svg>

$Q = 4$, $R = 1$인 P4에서 $x_0 = 1$부터 잰, 이득마다의 장부 가격 $J(K) = (4 + K^2)/(2(1 + K))$이고, 표시한 이득의 폐루프 극점 $-(1+K)$를 축 아래에 적었다. 최솟값 $1.236$이 LQR 이득 $K = 1.236$에 있고 $P$와 같다. 개루프와 손 이득 $K = 4$는 둘 다 $2.0$, 5 §1의 $K = 9$는 $4.25$가 든다.

### 1. 리카티 방정식, 구조로 읽기

[[04-robotics/control-theory-ce397|5. 제어 이론 §7]]은 설계자가 고른 자리에 극점을 놓았고, '대상으로 한 번 끝까지'는 스칼라 하나에서 비용이 극점을 고르게 했다. 어떤 선형계에서든 질문은 같다. 이 페이지의 대상에서 정의한 잣대 $J$로 잴 때 가장 좋은 이득 $K$는 무엇인가. 답도 다시 상수 선형 피드백 $u = -Kx$, $K = R^{-1}B^\top P$이고, $P$는 오프라인에서 한 번 푸는 행렬 방정식 하나의 해이므로 실행 중에는 아무것도 반복 계산하지 않는다:

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

이것이 **대수 리카티 방정식**(ARE)이다. 모르는 대칭 $n \times n$ 행렬 $P$에 대해 이차인 행렬
방정식이고, 자료는 모델 $A, B$와 가중치 $Q, R$이다. $P$는 최적 **cost-to-go**(가치 함수), 즉 주어진
출발 상태에서 달성할 수 있는 최소 비용의 행렬이다.

$$V(x_0) = \min_{u(\cdot)} \int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt = x_0^\top P x_0$$

그래서 $P$는 모든 $x_0$에 대해 한꺼번에 "$x_0$에 있는 것이 얼마나 비싼가"에 답한다.

**어디서 오는가, 네 단계로** — '대상으로 한 번 끝까지'의 네 단계를 행렬로. 최적 cost-to-go가 이차형식이라고 추측한다,
$V(x) = x^\top P x$ — 맞아떨어지기 때문에 사후에 정당화되는 추측이다. 그것을 최적성
조건(연속 시간 벨만 방정식, 곧 HJB(해밀턴–야코비–벨만) 방정식 — 벨만 방정식은 [[02-foundations/rl-basics|7. RL 기초 §2]]에서 이산 시간으로 소개된다)에 대입한다. 최적에서는 순간 비용과 cost-to-go의 변화율의
합이 0이라는 조건이다: $0 = \min_u\,[\,x^\top Q x + u^\top R u + \nabla V^\top(Ax + Bu)\,]$,
그리고 $\nabla V = 2Px$다. 셋째, $u$에 대해 최소화하는데 이제 평범한 이차식이다. 미분을 0으로
두면 $2Ru + 2B^\top P x = 0$, 즉 $u^\star = -R^{-1}B^\top P x$다. **LQR 이득
$K = R^{-1}B^\top P$가 여기서 나온다. 설계된 것이 아니라 떨어져 나온다.** 넷째, $u^\star$를
도로 넣는다. 항마다 보면:
- 노력 항은 $u^{\star\top}Ru^\star = x^\top PBR^{-1}RR^{-1}B^\top Px = x^\top PBR^{-1}B^\top Px$다;
- 변화율 항은 $\nabla V^\top(Ax + Bu^\star) = 2x^\top PAx - 2x^\top PBR^{-1}B^\top Px$다;
- 그리고 $2x^\top PAx = x^\top(A^\top P + PA)\,x$다. 스칼라는 자기 전치와 같으므로 $x^\top PAx = x^\top A^\top Px$이고, 두 절반을 대칭으로 쓸 수 있기 때문이다.

상태 항 $x^\top Qx$까지 더하면 괄호는 $x^\top(A^\top P + PA - PBR^{-1}B^\top P + Q)\,x$이고, 이것이 모든 $x$에서 $0$이어야 한다. 모든 $x$에서 이차형식이 0인 대칭 행렬은 영행렬이고, 그것이 바로 위의 방정식이다. P4($A = -1$, $B = 1$, $R = 1$, $Q = 4$)에서는 '대상으로 한 번 끝까지'의 $-2P - P^2 + 4 = 0$이 된다.

그렇게 읽으면 이상해 보이던 가운데 항이 평범해진다. $-PBR^{-1}B^\top P$는 덧붙인 모델링 선택이
아니라 *최적 피드백을 비용에 도로 대입한 것*이다. $P$에 대해 이차인 이유이고, 빼는 이유다 —
제어기가 행동함으로써 *치르지 않게 된* 비용이다.

**계산 예제, 스칼라.** 불안정한 $\dot x = x + u$($A = B = 1$)에 $Q = R = 1$을 쓰자. ARE는
$2P - P^2 + 1 = 0$이 되고 근이 **둘**, $P = 1 + \sqrt2 = 2.414$와 $P = 1 - \sqrt2 = -0.414$다.
**안정화 해**는 그 이득이 $A - BK$를 안정하게 만드는 해다. $P = 2.414$는 $K = 2.414$와 폐루프
$\dot x = -1.414\,x$를 주고, $P = -0.414$는 $\dot x = +1.414\,x$를 준다. 리카티 방정식은 일반적으로
해가 여럿이고, 논문의 "그" 해는 언제나 안정화 해를 뜻한다. cost-to-go를 검산하면, $x_0 = 1$에서
폐루프는 $x = e^{-1.414t}$, $u = -2.414\,x$이므로
$J = \int_0^\infty (1 + 2.414^2)\,e^{-2.828t}\,dt = 2.414 = P$다.

**ARE를 구조로 읽기.** 로봇 규모에서 리카티 방정식을 손으로 푸는 일은 없다 — 하지만 구조로 읽으면 남는 게 있다: $Q$는 상태 비용을 주입하고,
이차 항 $-PBR^{-1}B^\top P$는 *피드백이 제어를 통해 비용을 깎아먹는* 항이며, 안정화 해
$P$가 — $(A,Q^{1/2})$가 가관측이면 양의 정부호 — $V(x)=x^\top P x$를 폐루프의 리아푸노프 함수로 만든다. (**리아푸노프 함수**(Lyapunov function)란 $x=0$을 뺀 모든 곳에서 양수이고 모든 폐루프 궤적을 따라 줄어드는 상태의 스칼라 "에너지"다. 그런 함수가 있으면 상태는 $0$ 말고 갈 곳이 없으므로, 그 존재가 곧 안정성의 증명이다. 세 조건과 계산 예제는 [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]에 있다. 여기서는 HJB 조건이 $\dot V = -(x^\top Q x + u^{\star\top} R u^\star)$, 즉 순간 비용에 음수를 붙인 값을 준다.) $Q$가 양의 준정부호에 그치면 $P$가 특이할 수 있어 이 리아푸노프 논증에 한 단계가 더 필요하다. 접힌 메모가 그 단계를 말한다. 논문이 "리카티
방정식을 푼다"고 하면 이 상수 $P$를 오프라인에서 한 번(반복/시변 LQR에서는 선형화마다
한 번) 계산한다는 뜻이다.

> [!note]- 더 깊이 · Deeper
> **$Q$가 준정부호에 그칠 때.** 검출 가능성(스스로 줄어들지 않는 모든 모드가 비용에 나타난다는 조건으로, §2의 두 번째 조건이다)만 있으면 $P \succeq 0$이고 LaSalle류 논증이 필요하다 — LaSalle 불변 원리는 $\dot V$가 $\le 0$에 그칠 때도, 원점 말고는 어떤 궤적도 $\dot V = 0$인 곳에 영원히 머물 수 없다면 수렴을 증명해 준다.

### 1.5 이산 시간 쌍둥이

로봇의 제어기는 시계 위에서 돈다. 상태를 읽고 한 주기 동안 명령을 붙들어 두므로, 제어기가 상대하는 장치는 $x_{k+1} = Ax_k + Bu_k$다. 로봇 논문, [[04-robotics/mpc|7. MPC]]의 종단 비용, §4의 LQG가 모두 이 이산 형태를 쓰니, §1의 질문을 적분 대신 합으로 다시 물어야 한다. 연속 시간에서 설계한 이득을 느린 시계로 돌리는 것은 답이 아니다([[04-robotics/control-theory-ce397|5. 제어 이론 §4]]는 $T = 0.1\,\mathrm{s}$에서 $K = 99$가 불안정해지는 것을 보았다).

$x_{k+1} = Ax_k + Bu_k$와 비용 $\sum_k (x_k^\top Q x_k + u_k^\top R u_k)$에서도 cost-to-go는 이차식 $V(x) = x^\top Px$이고, 벨만 방정식은 이제 여기서의 cost-to-go가 단계 비용에 가장 좋은 입력 아래 다음 상태의 cost-to-go를 더한 것이라고 말한다. $V(x) = \min_u\,[\,x^\top Qx + u^\top Ru + V(Ax + Bu)\,]$. 최소화하면 $u^\star = -Kx$, $K = (R + B^\top PB)^{-1}B^\top PA$가 나오고, 그것을 도로 넣으면 **이산 대수 리카티 방정식**(DARE)이 된다.

$$P = A^\top P A - A^\top P B\,(R + B^\top P B)^{-1} B^\top P A + Q$$

같은 장부를 한 스텝씩 적는 것이므로 구조와 읽는 법이 §1과 같다. $Q$는 비용을 주입하고, 빼는 항은 피드백이 없애는 비용이며, 안정화 해가 $V$를 리아푸노프 함수로 만든다. 다만 "안정"은 이제 $A - BK$의 모든 고유값이 단위원 안에 있다는 뜻이고, §2의 두 조건은 $|\lambda| \ge 1$인 모드에서 확인한다.

*예, 손으로.* 이산 적분기 $x_{k+1} = x_k + u_k$($A = B = 1$), $Q = R = 1$. $V(x) = Px^2$로 두면 괄호 $x^2 + u^2 + P(x + u)^2$는 $u$에 대한 포물선이고, 그 도함수 $2u + 2P(x + u)$는 $u^\star = -\tfrac{P}{1+P}\,x$에서 0이 되므로 $K = P/(1+P)$다. $u^\star$를 도로 넣으면 $P = 1 + K^2 + P(1 - K)^2$이고, $1 - K = 1/(1 + P)$이므로 뒤의 두 항의 합은 $P/(1+P)$다. 그래서 $P = 1 + P/(1+P)$, 곧

$$P^2 - P - 1 = 0 \quad\Rightarrow\quad P = \tfrac{1 + \sqrt5}{2} = 1.618$$

이고, 양의 근을 취한다. 그러면 $K = 0.618$이고, 폐루프 $x_{k+1} = (1 - K)\,x_k = 0.382\,x_k$는 한 스텝마다 상태를 $62\,\%$ 줄이며 단위원 안쪽 깊숙이 있다. [[04-robotics/mpc|7. MPC §5]]는 바로 이 숫자, $V_f = 1.618\,x^2$와 $u = -0.618\,x$를 안정성 논증의 종단 비용과 종단 제어기로 다시 쓰고, §4는 LQR 이득을 이 방정식에서 가져온다.

*비예.* 방정식의 다른 근 $P = (1 - \sqrt5)/2 = -0.618$도 DARE를 만족하지만, $K = -0.618/0.382 = -1.618$과 $x_{k+1} = 2.618\,x_k$를 주어 단위원 밖에 있다. §1에서처럼 "그" 해는 안정화 해를 뜻한다.

### 2. 언제 실제로 통하는가? 두 조건

"LQR은 안정성이 보장된다"에는 작은 글씨가 있다. 모델에 하나, 비용에 하나, 조건이 둘 붙고, 비선형 시스템을 선형화해 LQR을 쓰는 논문은 두 조건을 *선형화 지점에서만* 상속한다. 이 절은 각각을 랭크 검정과 예·비예 한 쌍으로 적는다.

- **$(A,B)$의 안정화 가능성**(stabilizability): $\text{Re}\,\lambda \ge 0$인 $A$의 모든 모드가 — 이중 적분기의 $\lambda = 0$ 모드도 포함해 — $u$의 영향을
  받아야 한다 — 안정화 피드백이 존재하기 위한 정확한(필요충분) 조건이며,
  [[02-foundations/linear-algebra|1. 선형대수 §5.3]]의 완전한 가제어성 랭크 검정보다
  약하다. 아니면 리카티든 뭐든 어떤 피드백도 안정화할 수 없다.
  정의로 쓰면, 어떤 이득 $K$가 $A - BK$의 모든 고유값의 실수부를 음수로 만들 때 $(A,B)$가
  **안정화 가능**하다. 모드별로는 PBH(Popov–Belevitch–Hautus) 랭크 검정으로 확인한다.
  $$\text{rank}\,[\,A - \lambda I \;\; B\,] = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  입력이 건드릴 수 없는 모드의 고유값에서 정확히 랭크가 $n$ 아래로 떨어지기 때문이다. *모든*
  고유값에서 완전 랭크를 요구하면 그것이 가제어성 자체다. (이산 시간에서는 $|\lambda| \ge 1$인 모드가
  불안정 모드다.) *예:* [[04-robotics/control-theory-ce397|5. 제어 이론 §6]]의 불가제어 쌍
  $A = \text{diag}(-1,-2)$, $B = (1, 0)^\top$은 스스로 감쇠하는 모드인 $\lambda = -2$에서만 랭크를
  잃으므로 안정화 가능하다. *비예:* 같은 $B$에 $A = \text{diag}(1, 2)$이면 불안정 모드인
  $\lambda = 2$에서 랭크를 잃으므로 그런 $K$가 없다.
- **$(A,Q^{1/2})$의 검출 가능성**(detectability): $\text{Re}\,\lambda \ge 0$인 모든 모드가 비용에 나타나야
  한다 — 아니면 최적화기가 조용히 발산하는 모드를 "신경 안 쓰는" 것이 허용되어, 최적
  비용의 제어기가 안정화 제어기가 아니게 된다.
  $Q^{1/2}$는 $(Q^{1/2})^\top Q^{1/2} = Q$인 아무 행렬이며, 그래서 $x^\top Q x = \lVert Q^{1/2}x\rVert^2$가
  비용이 보는 "출력"이 된다. 검출 가능성은 안정화 가능성의 쌍대로, 열 대신 행을 쌓는다.
  $$\text{rank}\begin{bmatrix} A - \lambda I \\ Q^{1/2} \end{bmatrix} = n \quad \text{for every eigenvalue } \lambda \text{ of } A \text{ with } \text{Re}\,\lambda \ge 0$$
  랭크가 떨어진다는 것은 감쇠하지 않는 어떤 모드 $v$가 $Q^{1/2}v = 0$이라 비용이 들지 않는다는 뜻이기
  때문이다. *예:* §3의 이중 적분기에서 $Q = \text{diag}(q, 0)$은 통과한다($\lambda = 0$에서 랭크 2).
  위치에 벌점이 붙고 속도가 위치를 바꾸기 때문이다. *비예:* 속도만 보는 $Q = \text{diag}(0, 1)$,
  $R = 1$은 $\lambda = 0$에서 랭크 1이다. 양의 준정부호 리카티 해는 $P = \text{diag}(0, 1)$이라
  $K = (0\;\;1)$이고 폐루프 고유값은 $0$과 $-1$이다. 위치 $1$, 속도 $1$에서 출발한 카트는 위치 $2$에서
  멈추고 거기 머문다. 비용이 돌아오라고 요구한 적이 없기 때문이다.

### 3. Q와 R이 거동에 하는 일 — 읽기용 예제

실험 절은 튜닝을 말로 적는다. "공격적인 이득", "상태 가중치를 두 자릿수 올렸다". 그 말들은 정확한 산수에 대응한다. 이 페이지에서 스칼라 너머로도 리카티 방정식이 손으로 풀리는 유일한 계, 이 페이지의 대상에 적은 카트에서 이 절은 $Q$와 $R$이 무엇을 하는지 유도한다.

이중 적분기(카트): $x = (p, v)$, $u$ = 힘이므로
$A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$, $B = \begin{pmatrix}0\\1\end{pmatrix}$.
$Q = \mathrm{diag}(q, 0)$, $R = r$로 두자.

**이 경우는 손으로 실제로 풀린다**, 그리고 그 답이 어떤 솔버 출력보다 많은 것을 가르쳐 준다.
$P = \begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$로 놓고 리카티 방정식에 대입하면
서로 다른 세 성분에서 스칼라 방정식 셋이 나온다:

$$q - \frac{p_{12}^2}{r} = 0, \qquad p_{11} - \frac{p_{12}p_{22}}{r} = 0, \qquad 2p_{12} - \frac{p_{22}^2}{r} = 0$$

세 식은 삼각 구조라 $p_{12}$부터 풀고 나머지를 따라오게 할 수 있다: $p_{12} = \sqrt{qr}$, 이어서 $p_{22} = \sqrt{2r\sqrt{qr}}$, 그리고 $p_{11}$이
따라 나온다. 이득 $K = R^{-1}B^\top P$는 $P$의 아랫줄을 $r$로 나눈 것이다:

$$k_1 = \sqrt{\rho}, \qquad k_2 = \sqrt{2}\,\rho^{1/4}, \qquad \rho = q/r$$

이제 이 식이 하는 말을 읽어보자 — 서로 다른 사실 셋이 한꺼번에 떨어진다.

| $q$ | $r$ | $\rho = q/r$ | $K = (k_1, k_2)$ | $\omega_n$ | $\zeta$ | 정착 시간 $\approx 4/\zeta\omega_n$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7초 |
| 100 | 1 | 100 | $(10.0,\ 4.47)$ | 3.16 | 0.707 | 1.8초 |
| 1 | 100 | 0.01 | $(0.10,\ 0.45)$ | 0.32 | 0.707 | 17.9초 |
| 10 | 10 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7초 |

- **공통 스칼라 배율은 의미가 없다.** 1행과 4행의 이득이 완전히 같다. $Q$와 $R$의 모든
  원소에 같은 양의 스칼라를 곱하면 비용의 크기만 바뀌고 argmin은 움직이지 않는다. 행렬 내부의
  상태·입력 사이 상대 가중치는 여전히 중요하다.
- **위치만 보는 이 $Q=\operatorname{diag}(q,0)$에서는 감쇠가 고정된다.** 모든 행에서 $\zeta = 1/\sqrt2 = 0.707$이다. 폐루프
  특성 다항식이 $\lambda^2 + \sqrt2\rho^{1/4}\lambda + \sqrt\rho$이므로
  $\omega_n = \rho^{1/4}$, $2\zeta\omega_n = \sqrt2\rho^{1/4}$가 되어 **이 특수한 $Q$에서**
  어떤 $q/r$을 써도 $\zeta = 0.707$이다. 속도 상태 가중치를 추가하면 리카티 해와 감쇠가
  달라질 수 있다. 이 예에서는 가중치가 사는 것이 속도이지 모양이 아니다. "LQR은 극점을 손이 아니라 최적화가 고른다"는
  일반론이 구체화된 것이다 — [[04-robotics/control-theory-ce397|5. 제어 이론 §7]]은 손으로
  $\zeta = 0.7$에 놓았고, LQR은 시키지 않아도 사실상 같은 자리에 도착했다.
- **속도는 네제곱근이고, 이건 가혹하다.** $\omega_n = \rho^{1/4}$이므로 대역폭을 두 배로
  올리려면 $q/r$을 **16배**, 열 배로 올리려면 $10^4$배 키워야 한다. 실험 절에 "상태 가중치를
  두 자릿수 올렸다"고 쓰여 있으면 대역폭으로는 $\sqrt{10} \approx 3.2$배를 산 것이고,
  $k_1 = \sqrt\rho$가 10배 커졌으니 명령 힘도 대략 10배, 증폭되는 센서 잡음도 10배다.

실험 절이 쓰는 말로 하면:

- **큰 $q/r$**("상태가 비싸고 제어가 싸다"): 공격적 이득 — 빠른 회복, 큰 힘 스파이크, 잡음
  증폭 증가, 액추에이터 포화 위험(LQR 자신은 이를 모델링하지 않는다 —
  [[04-robotics/mpc|MPC]]의 몫이다).
- **작은 $q/r$**("제어가 비싸다"): 부드러운 이득, 느린 회복, 매끄러운 입력.
- 속도 vs 위치 가중치는 응답의 *감쇠* vs *강성*을 빚는다 — "정착 시간 …를 위해 Q/R을
  튜닝했다"는 문장 뒤의 손잡이 어휘다.

<svg viewBox="0 0 560 240" style="max-width:100%;height:auto" role="img" aria-label="q/r = 100, 1, 0.01에서 LQR 아래 카트의 계단 응답, 0에서 20초까지: 셋 다 목표를 4.3% 넘고, 1.41, 4.44, 14.1초에 정점을 찍으며, 1.8, 5.7, 17.9초에 정착한다.">
  <g stroke="currentColor" stroke-width="1" fill="none"><line x1="56.0" y1="23.5" x2="56.0" y2="150.0"/><line x1="56.0" y1="150.0" x2="536.0" y2="150.0"/><line x1="56.0" y1="40.0" x2="536.0" y2="40.0" stroke-dasharray="4 4" stroke-opacity="0.5"/></g>
  <g stroke="currentColor" stroke-width="1"><line x1="56.0" y1="150.0" x2="56.0" y2="154.0"/><line x1="176.0" y1="150.0" x2="176.0" y2="154.0"/><line x1="296.0" y1="150.0" x2="296.0" y2="154.0"/><line x1="416.0" y1="150.0" x2="416.0" y2="154.0"/><line x1="536.0" y1="150.0" x2="536.0" y2="154.0"/><line x1="52.0" y1="40.0" x2="56.0" y2="40.0"/><line x1="52.0" y1="150.0" x2="56.0" y2="150.0"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle"><text x="56.0" y="165.0">0</text><text x="176.0" y="165.0">5</text><text x="296.0" y="165.0">10</text><text x="416.0" y="165.0">15</text><text x="536.0" y="165.0">20</text></g>
  <g font-size="10.5" fill="currentColor" text-anchor="end"><text x="49.0" y="43.5">목표 1</text><text x="49.0" y="153.5">0</text></g>
  <text x="536.0" y="178.0" font-size="10.5" fill="currentColor" text-anchor="end">t (초)</text>
  <path d="M56.0 150.0 L57.2 148.7 L58.4 145.3 L59.6 140.2 L60.8 133.8 L62.0 126.7 L63.2 119.0 L64.4 111.1 L65.6 103.2 L66.8 95.5 L68.0 88.1 L69.2 81.1 L70.4 74.5 L71.6 68.5 L72.8 63.1 L74.0 58.3 L75.2 54.0 L76.4 50.2 L77.6 47.0 L78.8 44.3 L80.0 42.0 L81.2 40.1 L82.4 38.6 L83.6 37.5 L84.8 36.6 L86.0 36.0 L87.2 35.6 L88.4 35.3 L89.6 35.2 L90.8 35.3 L92.0 35.4 L93.2 35.6 L94.4 35.9 L95.6 36.2 L96.8 36.6 L98.0 36.9 L99.2 37.2 L100.4 37.6 L101.6 37.9 L102.8 38.2 L104.0 38.5 L105.2 38.7 L106.4 39.0 L107.6 39.2 L108.8 39.4 L110.0 39.5 L111.2 39.7 L112.4 39.8 L113.6 39.9 L114.8 40.0 L116.0 40.1 L117.2 40.1 L118.4 40.1 L119.6 40.2 L120.8 40.2 L122.0 40.2 L123.2 40.2 L124.4 40.2 L125.6 40.2 L126.8 40.2 L128.0 40.2 L129.2 40.2 L130.4 40.2 L131.6 40.1 L132.8 40.1 L134.0 40.1 L135.2 40.1 L136.4 40.1 L137.6 40.1 L138.8 40.1 L140.0 40.0 L141.2 40.0 L142.4 40.0 L143.6 40.0 L144.8 40.0 L146.0 40.0 L147.2 40.0 L148.4 40.0 L149.6 40.0 L150.8 40.0 L152.0 40.0 L153.2 40.0 L154.4 40.0 L155.6 40.0 L156.8 40.0 L158.0 40.0 L159.2 40.0 L160.4 40.0 L161.6 40.0 L162.8 40.0 L164.0 40.0 L165.2 40.0 L166.4 40.0 L167.6 40.0 L168.8 40.0 L170.0 40.0 L171.2 40.0 L172.4 40.0 L173.6 40.0 L174.8 40.0 L176.0 40.0 L177.2 40.0 L178.4 40.0 L179.6 40.0 L180.8 40.0 L182.0 40.0 L183.2 40.0 L184.4 40.0 L185.6 40.0 L186.8 40.0 L188.0 40.0 L189.2 40.0 L190.4 40.0 L191.6 40.0 L192.8 40.0 L194.0 40.0 L195.2 40.0 L196.4 40.0 L197.6 40.0 L198.8 40.0 L200.0 40.0 L201.2 40.0 L202.4 40.0 L203.6 40.0 L204.8 40.0 L206.0 40.0 L207.2 40.0 L208.4 40.0 L209.6 40.0 L210.8 40.0 L212.0 40.0 L213.2 40.0 L214.4 40.0 L215.6 40.0 L216.8 40.0 L218.0 40.0 L219.2 40.0 L220.4 40.0 L221.6 40.0 L222.8 40.0 L224.0 40.0 L225.2 40.0 L226.4 40.0 L227.6 40.0 L228.8 40.0 L230.0 40.0 L231.2 40.0 L232.4 40.0 L233.6 40.0 L234.8 40.0 L236.0 40.0 L237.2 40.0 L238.4 40.0 L239.6 40.0 L240.8 40.0 L242.0 40.0 L243.2 40.0 L244.4 40.0 L245.6 40.0 L246.8 40.0 L248.0 40.0 L249.2 40.0 L250.4 40.0 L251.6 40.0 L252.8 40.0 L254.0 40.0 L255.2 40.0 L256.4 40.0 L257.6 40.0 L258.8 40.0 L260.0 40.0 L261.2 40.0 L262.4 40.0 L263.6 40.0 L264.8 40.0 L266.0 40.0 L267.2 40.0 L268.4 40.0 L269.6 40.0 L270.8 40.0 L272.0 40.0 L273.2 40.0 L274.4 40.0 L275.6 40.0 L276.8 40.0 L278.0 40.0 L279.2 40.0 L280.4 40.0 L281.6 40.0 L282.8 40.0 L284.0 40.0 L285.2 40.0 L286.4 40.0 L287.6 40.0 L288.8 40.0 L290.0 40.0 L291.2 40.0 L292.4 40.0 L293.6 40.0 L294.8 40.0 L296.0 40.0 L297.2 40.0 L298.4 40.0 L299.6 40.0 L300.8 40.0 L302.0 40.0 L303.2 40.0 L304.4 40.0 L305.6 40.0 L306.8 40.0 L308.0 40.0 L309.2 40.0 L310.4 40.0 L311.6 40.0 L312.8 40.0 L314.0 40.0 L315.2 40.0 L316.4 40.0 L317.6 40.0 L318.8 40.0 L320.0 40.0 L321.2 40.0 L322.4 40.0 L323.6 40.0 L324.8 40.0 L326.0 40.0 L327.2 40.0 L328.4 40.0 L329.6 40.0 L330.8 40.0 L332.0 40.0 L333.2 40.0 L334.4 40.0 L335.6 40.0 L336.8 40.0 L338.0 40.0 L339.2 40.0 L340.4 40.0 L341.6 40.0 L342.8 40.0 L344.0 40.0 L345.2 40.0 L346.4 40.0 L347.6 40.0 L348.8 40.0 L350.0 40.0 L351.2 40.0 L352.4 40.0 L353.6 40.0 L354.8 40.0 L356.0 40.0 L357.2 40.0 L358.4 40.0 L359.6 40.0 L360.8 40.0 L362.0 40.0 L363.2 40.0 L364.4 40.0 L365.6 40.0 L366.8 40.0 L368.0 40.0 L369.2 40.0 L370.4 40.0 L371.6 40.0 L372.8 40.0 L374.0 40.0 L375.2 40.0 L376.4 40.0 L377.6 40.0 L378.8 40.0 L380.0 40.0 L381.2 40.0 L382.4 40.0 L383.6 40.0 L384.8 40.0 L386.0 40.0 L387.2 40.0 L388.4 40.0 L389.6 40.0 L390.8 40.0 L392.0 40.0 L393.2 40.0 L394.4 40.0 L395.6 40.0 L396.8 40.0 L398.0 40.0 L399.2 40.0 L400.4 40.0 L401.6 40.0 L402.8 40.0 L404.0 40.0 L405.2 40.0 L406.4 40.0 L407.6 40.0 L408.8 40.0 L410.0 40.0 L411.2 40.0 L412.4 40.0 L413.6 40.0 L414.8 40.0 L416.0 40.0 L417.2 40.0 L418.4 40.0 L419.6 40.0 L420.8 40.0 L422.0 40.0 L423.2 40.0 L424.4 40.0 L425.6 40.0 L426.8 40.0 L428.0 40.0 L429.2 40.0 L430.4 40.0 L431.6 40.0 L432.8 40.0 L434.0 40.0 L435.2 40.0 L436.4 40.0 L437.6 40.0 L438.8 40.0 L440.0 40.0 L441.2 40.0 L442.4 40.0 L443.6 40.0 L444.8 40.0 L446.0 40.0 L447.2 40.0 L448.4 40.0 L449.6 40.0 L450.8 40.0 L452.0 40.0 L453.2 40.0 L454.4 40.0 L455.6 40.0 L456.8 40.0 L458.0 40.0 L459.2 40.0 L460.4 40.0 L461.6 40.0 L462.8 40.0 L464.0 40.0 L465.2 40.0 L466.4 40.0 L467.6 40.0 L468.8 40.0 L470.0 40.0 L471.2 40.0 L472.4 40.0 L473.6 40.0 L474.8 40.0 L476.0 40.0 L477.2 40.0 L478.4 40.0 L479.6 40.0 L480.8 40.0 L482.0 40.0 L483.2 40.0 L484.4 40.0 L485.6 40.0 L486.8 40.0 L488.0 40.0 L489.2 40.0 L490.4 40.0 L491.6 40.0 L492.8 40.0 L494.0 40.0 L495.2 40.0 L496.4 40.0 L497.6 40.0 L498.8 40.0 L500.0 40.0 L501.2 40.0 L502.4 40.0 L503.6 40.0 L504.8 40.0 L506.0 40.0 L507.2 40.0 L508.4 40.0 L509.6 40.0 L510.8 40.0 L512.0 40.0 L513.2 40.0 L514.4 40.0 L515.6 40.0 L516.8 40.0 L518.0 40.0 L519.2 40.0 L520.4 40.0 L521.6 40.0 L522.8 40.0 L524.0 40.0 L525.2 40.0 L526.4 40.0 L527.6 40.0 L528.8 40.0 L530.0 40.0 L531.2 40.0 L532.4 40.0 L533.6 40.0 L534.8 40.0 L536.0 40.0" fill="none" stroke="currentColor" stroke-width="2" />
  <path d="M56.0 150.0 L57.2 149.9 L58.4 149.5 L59.6 148.8 L60.8 148.0 L62.0 146.9 L63.2 145.7 L64.4 144.3 L65.6 142.7 L66.8 141.0 L68.0 139.2 L69.2 137.3 L70.4 135.2 L71.6 133.1 L72.8 130.9 L74.0 128.6 L75.2 126.2 L76.4 123.8 L77.6 121.4 L78.8 119.0 L80.0 116.5 L81.2 114.0 L82.4 111.5 L83.6 109.0 L84.8 106.5 L86.0 104.0 L87.2 101.5 L88.4 99.0 L89.6 96.6 L90.8 94.2 L92.0 91.8 L93.2 89.5 L94.4 87.2 L95.6 85.0 L96.8 82.8 L98.0 80.6 L99.2 78.5 L100.4 76.4 L101.6 74.4 L102.8 72.5 L104.0 70.6 L105.2 68.7 L106.4 67.0 L107.6 65.2 L108.8 63.6 L110.0 62.0 L111.2 60.4 L112.4 58.9 L113.6 57.5 L114.8 56.1 L116.0 54.7 L117.2 53.5 L118.4 52.2 L119.6 51.1 L120.8 50.0 L122.0 48.9 L123.2 47.9 L124.4 46.9 L125.6 46.0 L126.8 45.2 L128.0 44.3 L129.2 43.6 L130.4 42.8 L131.6 42.2 L132.8 41.5 L134.0 40.9 L135.2 40.3 L136.4 39.8 L137.6 39.3 L138.8 38.9 L140.0 38.4 L141.2 38.1 L142.4 37.7 L143.6 37.4 L144.8 37.1 L146.0 36.8 L147.2 36.6 L148.4 36.3 L149.6 36.1 L150.8 36.0 L152.0 35.8 L153.2 35.7 L154.4 35.6 L155.6 35.5 L156.8 35.4 L158.0 35.3 L159.2 35.3 L160.4 35.3 L161.6 35.3 L162.8 35.2 L164.0 35.3 L165.2 35.3 L166.4 35.3 L167.6 35.3 L168.8 35.4 L170.0 35.4 L171.2 35.5 L172.4 35.6 L173.6 35.6 L174.8 35.7 L176.0 35.8 L177.2 35.9 L178.4 36.0 L179.6 36.1 L180.8 36.2 L182.0 36.3 L183.2 36.4 L184.4 36.5 L185.6 36.6 L186.8 36.7 L188.0 36.8 L189.2 36.9 L190.4 37.0 L191.6 37.1 L192.8 37.3 L194.0 37.4 L195.2 37.5 L196.4 37.6 L197.6 37.7 L198.8 37.8 L200.0 37.9 L201.2 38.0 L202.4 38.1 L203.6 38.2 L204.8 38.3 L206.0 38.3 L207.2 38.4 L208.4 38.5 L209.6 38.6 L210.8 38.7 L212.0 38.8 L213.2 38.8 L214.4 38.9 L215.6 39.0 L216.8 39.1 L218.0 39.1 L219.2 39.2 L220.4 39.3 L221.6 39.3 L222.8 39.4 L224.0 39.4 L225.2 39.5 L226.4 39.5 L227.6 39.6 L228.8 39.6 L230.0 39.7 L231.2 39.7 L232.4 39.7 L233.6 39.8 L234.8 39.8 L236.0 39.9 L237.2 39.9 L238.4 39.9 L239.6 39.9 L240.8 40.0 L242.0 40.0 L243.2 40.0 L244.4 40.0 L245.6 40.1 L246.8 40.1 L248.0 40.1 L249.2 40.1 L250.4 40.1 L251.6 40.1 L252.8 40.1 L254.0 40.2 L255.2 40.2 L256.4 40.2 L257.6 40.2 L258.8 40.2 L260.0 40.2 L261.2 40.2 L262.4 40.2 L263.6 40.2 L264.8 40.2 L266.0 40.2 L267.2 40.2 L268.4 40.2 L269.6 40.2 L270.8 40.2 L272.0 40.2 L273.2 40.2 L274.4 40.2 L275.6 40.2 L276.8 40.2 L278.0 40.2 L279.2 40.2 L280.4 40.2 L281.6 40.2 L282.8 40.2 L284.0 40.2 L285.2 40.2 L286.4 40.2 L287.6 40.2 L288.8 40.2 L290.0 40.2 L291.2 40.2 L292.4 40.1 L293.6 40.1 L294.8 40.1 L296.0 40.1 L297.2 40.1 L298.4 40.1 L299.6 40.1 L300.8 40.1 L302.0 40.1 L303.2 40.1 L304.4 40.1 L305.6 40.1 L306.8 40.1 L308.0 40.1 L309.2 40.1 L310.4 40.1 L311.6 40.1 L312.8 40.1 L314.0 40.1 L315.2 40.1 L316.4 40.1 L317.6 40.1 L318.8 40.1 L320.0 40.0 L321.2 40.0 L322.4 40.0 L323.6 40.0 L324.8 40.0 L326.0 40.0 L327.2 40.0 L328.4 40.0 L329.6 40.0 L330.8 40.0 L332.0 40.0 L333.2 40.0 L334.4 40.0 L335.6 40.0 L336.8 40.0 L338.0 40.0 L339.2 40.0 L340.4 40.0 L341.6 40.0 L342.8 40.0 L344.0 40.0 L345.2 40.0 L346.4 40.0 L347.6 40.0 L348.8 40.0 L350.0 40.0 L351.2 40.0 L352.4 40.0 L353.6 40.0 L354.8 40.0 L356.0 40.0 L357.2 40.0 L358.4 40.0 L359.6 40.0 L360.8 40.0 L362.0 40.0 L363.2 40.0 L364.4 40.0 L365.6 40.0 L366.8 40.0 L368.0 40.0 L369.2 40.0 L370.4 40.0 L371.6 40.0 L372.8 40.0 L374.0 40.0 L375.2 40.0 L376.4 40.0 L377.6 40.0 L378.8 40.0 L380.0 40.0 L381.2 40.0 L382.4 40.0 L383.6 40.0 L384.8 40.0 L386.0 40.0 L387.2 40.0 L388.4 40.0 L389.6 40.0 L390.8 40.0 L392.0 40.0 L393.2 40.0 L394.4 40.0 L395.6 40.0 L396.8 40.0 L398.0 40.0 L399.2 40.0 L400.4 40.0 L401.6 40.0 L402.8 40.0 L404.0 40.0 L405.2 40.0 L406.4 40.0 L407.6 40.0 L408.8 40.0 L410.0 40.0 L411.2 40.0 L412.4 40.0 L413.6 40.0 L414.8 40.0 L416.0 40.0 L417.2 40.0 L418.4 40.0 L419.6 40.0 L420.8 40.0 L422.0 40.0 L423.2 40.0 L424.4 40.0 L425.6 40.0 L426.8 40.0 L428.0 40.0 L429.2 40.0 L430.4 40.0 L431.6 40.0 L432.8 40.0 L434.0 40.0 L435.2 40.0 L436.4 40.0 L437.6 40.0 L438.8 40.0 L440.0 40.0 L441.2 40.0 L442.4 40.0 L443.6 40.0 L444.8 40.0 L446.0 40.0 L447.2 40.0 L448.4 40.0 L449.6 40.0 L450.8 40.0 L452.0 40.0 L453.2 40.0 L454.4 40.0 L455.6 40.0 L456.8 40.0 L458.0 40.0 L459.2 40.0 L460.4 40.0 L461.6 40.0 L462.8 40.0 L464.0 40.0 L465.2 40.0 L466.4 40.0 L467.6 40.0 L468.8 40.0 L470.0 40.0 L471.2 40.0 L472.4 40.0 L473.6 40.0 L474.8 40.0 L476.0 40.0 L477.2 40.0 L478.4 40.0 L479.6 40.0 L480.8 40.0 L482.0 40.0 L483.2 40.0 L484.4 40.0 L485.6 40.0 L486.8 40.0 L488.0 40.0 L489.2 40.0 L490.4 40.0 L491.6 40.0 L492.8 40.0 L494.0 40.0 L495.2 40.0 L496.4 40.0 L497.6 40.0 L498.8 40.0 L500.0 40.0 L501.2 40.0 L502.4 40.0 L503.6 40.0 L504.8 40.0 L506.0 40.0 L507.2 40.0 L508.4 40.0 L509.6 40.0 L510.8 40.0 L512.0 40.0 L513.2 40.0 L514.4 40.0 L515.6 40.0 L516.8 40.0 L518.0 40.0 L519.2 40.0 L520.4 40.0 L521.6 40.0 L522.8 40.0 L524.0 40.0 L525.2 40.0 L526.4 40.0 L527.6 40.0 L528.8 40.0 L530.0 40.0 L531.2 40.0 L532.4 40.0 L533.6 40.0 L534.8 40.0 L536.0 40.0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-dasharray="7 4" stroke-opacity="0.8"/>
  <path d="M56.0 150.0 L57.2 150.0 L58.4 149.9 L59.6 149.9 L60.8 149.8 L62.0 149.7 L63.2 149.5 L64.4 149.4 L65.6 149.2 L66.8 149.0 L68.0 148.7 L69.2 148.5 L70.4 148.2 L71.6 147.9 L72.8 147.6 L74.0 147.2 L75.2 146.9 L76.4 146.5 L77.6 146.1 L78.8 145.7 L80.0 145.3 L81.2 144.8 L82.4 144.4 L83.6 143.9 L84.8 143.4 L86.0 142.9 L87.2 142.4 L88.4 141.8 L89.6 141.3 L90.8 140.7 L92.0 140.2 L93.2 139.6 L94.4 139.0 L95.6 138.4 L96.8 137.8 L98.0 137.1 L99.2 136.5 L100.4 135.8 L101.6 135.2 L102.8 134.5 L104.0 133.8 L105.2 133.2 L106.4 132.5 L107.6 131.8 L108.8 131.1 L110.0 130.3 L111.2 129.6 L112.4 128.9 L113.6 128.2 L114.8 127.4 L116.0 126.7 L117.2 125.9 L118.4 125.2 L119.6 124.4 L120.8 123.7 L122.0 122.9 L123.2 122.1 L124.4 121.4 L125.6 120.6 L126.8 119.8 L128.0 119.0 L129.2 118.2 L130.4 117.4 L131.6 116.7 L132.8 115.9 L134.0 115.1 L135.2 114.3 L136.4 113.5 L137.6 112.7 L138.8 111.9 L140.0 111.1 L141.2 110.3 L142.4 109.5 L143.6 108.7 L144.8 108.0 L146.0 107.2 L147.2 106.4 L148.4 105.6 L149.6 104.8 L150.8 104.0 L152.0 103.2 L153.2 102.4 L154.4 101.7 L155.6 100.9 L156.8 100.1 L158.0 99.3 L159.2 98.6 L160.4 97.8 L161.6 97.0 L162.8 96.3 L164.0 95.5 L165.2 94.7 L166.4 94.0 L167.6 93.2 L168.8 92.5 L170.0 91.7 L171.2 91.0 L172.4 90.3 L173.6 89.5 L174.8 88.8 L176.0 88.1 L177.2 87.3 L178.4 86.6 L179.6 85.9 L180.8 85.2 L182.0 84.5 L183.2 83.8 L184.4 83.1 L185.6 82.4 L186.8 81.7 L188.0 81.1 L189.2 80.4 L190.4 79.7 L191.6 79.0 L192.8 78.4 L194.0 77.7 L195.2 77.1 L196.4 76.4 L197.6 75.8 L198.8 75.2 L200.0 74.5 L201.2 73.9 L202.4 73.3 L203.6 72.7 L204.8 72.1 L206.0 71.5 L207.2 70.9 L208.4 70.3 L209.6 69.7 L210.8 69.1 L212.0 68.5 L213.2 68.0 L214.4 67.4 L215.6 66.9 L216.8 66.3 L218.0 65.8 L219.2 65.2 L220.4 64.7 L221.6 64.2 L222.8 63.6 L224.0 63.1 L225.2 62.6 L226.4 62.1 L227.6 61.6 L228.8 61.1 L230.0 60.6 L231.2 60.1 L232.4 59.7 L233.6 59.2 L234.8 58.7 L236.0 58.3 L237.2 57.8 L238.4 57.4 L239.6 56.9 L240.8 56.5 L242.0 56.0 L243.2 55.6 L244.4 55.2 L245.6 54.8 L246.8 54.4 L248.0 54.0 L249.2 53.6 L250.4 53.2 L251.6 52.8 L252.8 52.4 L254.0 52.0 L255.2 51.7 L256.4 51.3 L257.6 50.9 L258.8 50.6 L260.0 50.2 L261.2 49.9 L262.4 49.5 L263.6 49.2 L264.8 48.9 L266.0 48.6 L267.2 48.2 L268.4 47.9 L269.6 47.6 L270.8 47.3 L272.0 47.0 L273.2 46.7 L274.4 46.4 L275.6 46.1 L276.8 45.9 L278.0 45.6 L279.2 45.3 L280.4 45.0 L281.6 44.8 L282.8 44.5 L284.0 44.3 L285.2 44.0 L286.4 43.8 L287.6 43.5 L288.8 43.3 L290.0 43.1 L291.2 42.9 L292.4 42.6 L293.6 42.4 L294.8 42.2 L296.0 42.0 L297.2 41.8 L298.4 41.6 L299.6 41.4 L300.8 41.2 L302.0 41.0 L303.2 40.8 L304.4 40.6 L305.6 40.5 L306.8 40.3 L308.0 40.1 L309.2 40.0 L310.4 39.8 L311.6 39.6 L312.8 39.5 L314.0 39.3 L315.2 39.2 L316.4 39.0 L317.6 38.9 L318.8 38.8 L320.0 38.6 L321.2 38.5 L322.4 38.4 L323.6 38.2 L324.8 38.1 L326.0 38.0 L327.2 37.9 L328.4 37.8 L329.6 37.7 L330.8 37.6 L332.0 37.5 L333.2 37.4 L334.4 37.3 L335.6 37.2 L336.8 37.1 L338.0 37.0 L339.2 36.9 L340.4 36.8 L341.6 36.7 L342.8 36.7 L344.0 36.6 L345.2 36.5 L346.4 36.4 L347.6 36.4 L348.8 36.3 L350.0 36.2 L351.2 36.2 L352.4 36.1 L353.6 36.1 L354.8 36.0 L356.0 36.0 L357.2 35.9 L358.4 35.9 L359.6 35.8 L360.8 35.8 L362.0 35.7 L363.2 35.7 L364.4 35.7 L365.6 35.6 L366.8 35.6 L368.0 35.6 L369.2 35.5 L370.4 35.5 L371.6 35.5 L372.8 35.4 L374.0 35.4 L375.2 35.4 L376.4 35.4 L377.6 35.4 L378.8 35.3 L380.0 35.3 L381.2 35.3 L382.4 35.3 L383.6 35.3 L384.8 35.3 L386.0 35.3 L387.2 35.3 L388.4 35.3 L389.6 35.3 L390.8 35.2 L392.0 35.2 L393.2 35.2 L394.4 35.2 L395.6 35.2 L396.8 35.3 L398.0 35.3 L399.2 35.3 L400.4 35.3 L401.6 35.3 L402.8 35.3 L404.0 35.3 L405.2 35.3 L406.4 35.3 L407.6 35.3 L408.8 35.3 L410.0 35.4 L411.2 35.4 L412.4 35.4 L413.6 35.4 L414.8 35.4 L416.0 35.4 L417.2 35.5 L418.4 35.5 L419.6 35.5 L420.8 35.5 L422.0 35.5 L423.2 35.6 L424.4 35.6 L425.6 35.6 L426.8 35.6 L428.0 35.6 L429.2 35.7 L430.4 35.7 L431.6 35.7 L432.8 35.7 L434.0 35.8 L435.2 35.8 L436.4 35.8 L437.6 35.9 L438.8 35.9 L440.0 35.9 L441.2 35.9 L442.4 36.0 L443.6 36.0 L444.8 36.0 L446.0 36.1 L447.2 36.1 L448.4 36.1 L449.6 36.2 L450.8 36.2 L452.0 36.2 L453.2 36.3 L454.4 36.3 L455.6 36.3 L456.8 36.4 L458.0 36.4 L459.2 36.4 L460.4 36.5 L461.6 36.5 L462.8 36.5 L464.0 36.6 L465.2 36.6 L466.4 36.6 L467.6 36.7 L468.8 36.7 L470.0 36.7 L471.2 36.8 L472.4 36.8 L473.6 36.8 L474.8 36.9 L476.0 36.9 L477.2 36.9 L478.4 37.0 L479.6 37.0 L480.8 37.0 L482.0 37.1 L483.2 37.1 L484.4 37.1 L485.6 37.2 L486.8 37.2 L488.0 37.2 L489.2 37.3 L490.4 37.3 L491.6 37.3 L492.8 37.4 L494.0 37.4 L495.2 37.4 L496.4 37.5 L497.6 37.5 L498.8 37.5 L500.0 37.6 L501.2 37.6 L502.4 37.6 L503.6 37.7 L504.8 37.7 L506.0 37.7 L507.2 37.8 L508.4 37.8 L509.6 37.8 L510.8 37.9 L512.0 37.9 L513.2 37.9 L514.4 38.0 L515.6 38.0 L516.8 38.0 L518.0 38.0 L519.2 38.1 L520.4 38.1 L521.6 38.1 L522.8 38.2 L524.0 38.2 L525.2 38.2 L526.4 38.3 L527.6 38.3 L528.8 38.3 L530.0 38.3 L531.2 38.4 L532.4 38.4 L533.6 38.4 L534.8 38.5 L536.0 38.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 3" stroke-opacity="0.7"/>
  <circle cx="89.7" cy="35.2" r="2.6" fill="currentColor"/>
  <text x="96.7" y="30.2" font-size="10.5" fill="currentColor">모든 곡선이 4.3 % 오버슈트</text>
  <line x1="56.0" y1="192.0" x2="86.0" y2="192.0" stroke="currentColor" stroke-width="2" />
  <text x="94.0" y="196.0" font-size="11" fill="currentColor" xml:space="preserve">q/r = 100 · ω<tspan dy="3" font-size="10">n</tspan><tspan dy="-3"> = 3.16 rad/s</tspan> · 정착 1.8초</text>
  <line x1="56.0" y1="208.0" x2="86.0" y2="208.0" stroke="currentColor" stroke-width="1.7" stroke-dasharray="7 4" stroke-opacity="0.8"/>
  <text x="94.0" y="212.0" font-size="11" fill="currentColor" xml:space="preserve">q/r = 1 · ω<tspan dy="3" font-size="10">n</tspan><tspan dy="-3"> = 1.00 rad/s</tspan> · 정착 5.7초</text>
  <line x1="56.0" y1="224.0" x2="86.0" y2="224.0" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 3" stroke-opacity="0.7"/>
  <text x="94.0" y="228.0" font-size="11" fill="currentColor" xml:space="preserve">q/r = 0.01 · ω<tspan dy="3" font-size="10">n</tspan><tspan dy="-3"> = 0.32 rad/s</tspan> · 정착 17.9초</text>
</svg>

표의 앞 세 행에서 LQR 아래 카트의 계단 응답이다. 모든 곡선의 $\zeta = 0.707$이 같아서 오버슈트도 똑같이 $4.3\,\%$이고, 정착은 $1.8$, $5.7$, $17.9\,\mathrm{s}$다. $q/r$을 $100$배 해도 속도는 $\sqrt{10}$배밖에 얻지 못한다.

### 4. LQG의 작은 글씨

제어기는 $x$를 보지 못하고 잡음 섞인 측정 $y$만 본다. LQR의 이득을 상태의 추정값 위에서 돌려도 되는가, 그리고 그 대가는 무엇인가? 가우시안 잡음과 부분 관측을 더한 LQR, 곧 **LQG**의 답은 이렇다. 공칭 모델에 대해서는 된다, 그것도 정확히. 칼만 필터로 최적으로 추정하고 그 추정값을 LQR 이득으로 최적으로 제어하면 그 쌍이 결합 최적이다. 대가는 LQR이 가졌던 강건성 보장 전부다.

**LQG 문제를 식으로.** 동역학과 센서 모두에 서로 독립인 평균 0의 가우시안 백색 잡음이 붙는다
([[02-foundations/probability|3. 확률 §5.2]]).

$$x_{k+1} = Ax_k + Bu_k + w_k, \qquad y_k = Cx_k + v_k, \qquad w_k \sim \mathcal N(0, W), \quad v_k \sim \mathcal N(0, V)$$

$W$와 $V$는 공정 잡음과 측정 잡음의 공분산이다. [[02-foundations/probability|3. 확률 §5.2]]와 [[04-robotics/state-estimation-slam|3. 상태 추정 §5]]는 둘 다 $Q$와 $R$로 부르지만, 여기서는 $Q$와 $R$이 이미 비용 가중치라 이름을 바꿨다. 필터는 3. 상태 추정 §5에서 만난 바로 그것이고, 그 페이지는 $C$ 대신 $H$, 측정 $y$ 대신 $z$, 혁신(innovation) $y - C\hat x^-$ 대신 $\nu$를 쓴다. $u_k$는 스텝 $k$까지의 측정만 쓸 수 있다. 잡음 때문에 상태가
결코 가라앉지 않으므로 목적은 스텝당 기대 LQR 비용
$\lim_{T\to\infty}\tfrac1T E\big[\sum_{k<T} (x_k^\top Q x_k + u_k^\top R u_k)\big]$이다. 해는 이름 붙은
세 부분으로 이루어진다.
- $\hat x_k$를 만드는 **칼만 필터**. 그 이득 $L$은 $A, C, W, V$만 들어가는 필터 리카티 방정식에서 나온다. $L$은 추정 페이지들이 $K$라 부르는 칼만 이득인데, 여기서는 $K$가 LQR 이득이라 이름을 바꿨고, [[04-robotics/control-theory-ce397|5. 제어 이론 §8]]의 관측기 이득 $L$과 같은 자리에 있다.
- §1.5의 DARE에서 나오는 **LQR 이득** $K$. $A, B, Q, R$만 들어간다.
- 추정값을 참 상태처럼 다루는 **확실성 등가 제어기** $u_k = -K\hat x_k$.

두 이득을 따로 계산해도 결합이 여전히 최적이라는 것이 **분리 원리**이고, 그 극점판(폐루프 고유값이
$A - BK$의 고유값과 $A - LC$의 고유값을 합친 것)은 [[04-robotics/control-theory-ce397|5. 제어 이론 §8]]에서
연속 시간 관측기로 유도한다. (추정 페이지들의 예측–보정 형태로 쓴 이산 필터에서는 추정 오차가 $(I - LC)A$로 전개되고, 그 고유값은 $A - ALC$의 고유값이다. 아래 예처럼 $A = 1$이면 둘이 같다.) 해가 존재하려면 제어기 쪽에 $(A, B)$ 안정화 가능과 $(A, Q^{1/2})$ 검출 가능이, 필터 쪽에
그 쌍대 조건들이 필요하다. *예:* $A = B = C = 1$, $Q = R = W = V = 1$이면 두 리카티 방정식이 모두
$P^2 - P - 1 = 0$으로 줄어든다. 제어기 쪽의 $P = 1.618$은 §1.5의 cost-to-go다. 필터 쪽의 근 $1.618$은
추정 페이지들의 *예측* 공분산 $P^-$이고, 보정된 $P^+ = 0.618$은 [[04-robotics/state-estimation-slam|3. 상태 추정 §5]]의 $P^2 + qP - q = 0$을
$q = 1$에서 만족한다. 그래서 LQR 이득 $K$와 정상 상태 칼만 이득 $L = P^-/(P^- + V)$가 모두 $0.618$이다. 쌍대성이 글자 그대로
드러난다.

분리 원리는 선형-가우시안 모델에서 정확하다 — 그리고 유명하게 취약하다: **LQG에는
보장된 강건성 여유가 없다** (Doyle 1978의 한 줄 초록: "there are none"; 이득·위상·안정 여유는
[[04-robotics/control-theory-ce397|5. 제어 이론 §5.5]]에서 정의한다). 추정 오차와 모델
오차가 상호작용한다; 실제 시스템은 여유 검사나 강건 변형을 다시 도입한다. "LQG를 쓴다"는
*공칭 최적, 강건성은 보이기 전까지 미검증*으로 읽어라.

*비예, 숫자로 — Doyle 자신의 시스템.* $W$와 $V$가 잡음 세기인 연속 시간에서
$\dot x=\begin{pmatrix}1&1\\0&1\end{pmatrix}x+\begin{pmatrix}0\\1\end{pmatrix}u+\begin{pmatrix}1\\1\end{pmatrix}w$,
$y=x_1+v$를 잡고, $Q=60\begin{pmatrix}1&1\\1&1\end{pmatrix}$, $R=1$, 스칼라 $w$의 공정 잡음 세기 $60$,
$V=1$로 둔다. 두 리카티 방정식이 같은 깔끔한 수를 돌려준다. $K=(10,\ 10)$, $L=(10,\ 10)^\top$.
이제 모델은 $u$라고 가정했는데 구동기가 $m\,u$를 낸다고 하자. 참 상태를 되먹이면($u=-Kx$) 특성
다항식이 $\lambda^2+(10m-2)\lambda+1$이므로 모든 $m>0.2$에서 루프가 안정하다. 칼만 추정값을
되먹이면($u=-K\hat x$) $0.930<m<1.010$에서만 안정하다. 모델보다 1% 센 구동기 하나가 결합 최적
제어기를 불안정하게 만든다. 분리 원리는 아무것도 어기지 않았다 — $m\neq1$에 대해서는 애초에
아무것도 약속하지 않았다 — 그리고 그것이 Doyle의 한 줄 초록이 말하는 요점 전부다.

**왜 공부하나**: LQR은 다른 모든 것을 재는 기준점이다 — 다음 페이지 [[04-robotics/mpc|7. MPC]]는 "제약을
더해 온라인으로 다시 푸는 LQR"이고(그 종단 비용 $P$가 보통 LQR 리카티 해, 곧 §1.5의 해다),
선형-이차 문제의 RL 정책 반복이나 정책 최적화는 LQR을 복원하며(평가만으로는 고정된 이득의 값만 매긴다), 궤적 주변의 시변 LQR은 학습된
플래너가 출력을 넘기는 표준 추종 제어기다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] LQR 문제 설정과 해의 형태($u=-Kx$, $K=R^{-1}B^\top P$)를 말할 수 있다
- [ ] 스칼라 리카티 방정식을 손으로 풀고, 안정화 근을 고르고, $J = P$를 검산할 수 있다
- [ ] DARE와 그 이득을 쓰고, 이산 적분기에서 풀 수 있다
- [ ] 안정화 가능성·검출 가능성이 각각 무엇을 보장하는 조건인지 말할 수 있다
- [ ] $Q/R$ 비율이 이득·응답·포화 위험을 어떻게 바꾸는지 예제로 말할 수 있다
- [ ] 분리 원리와 그 취약성(LQG 무여유)을 말하고, 그 $W$, $V$, $L$을 추정 페이지들의 $Q$, $R$, $K$에 대응시키며, LQR이 MPC·RL의 기준점인 이유를 말할 수 있다

### 스스로 점검 · Self-check

1. $(A,B)$가 안정화 가능하지 않으면 리카티 접근에 무슨 일이 생기나?
2. 이중 적분기에서 $Q$를 10배, $R$을 10배 함께 키우면 $K$는 어떻게 되나?
3. "LQG는 최적이므로 강건하다"가 틀린 이유를 한 문장으로.
4. MPC의 종단 비용으로 LQR의 $P$를 쓰는 이유는?

> [!tip]- 정답 · Answers
> 1. 불안정 모드를 어떤 피드백도 못 잡으므로 안정화 해 $P$가 존재하지 않는다 — 문제 자체가 불량이다.
> 2. 불변 — $Q$와 $R$ 전체에 같은 양의 스칼라를 곱하면 비용 스케일만 바뀐다. 행렬형 $Q,R$ 내부의 상대 가중치는 여전히 $K$를 정한다.
> 3. 최적성은 공칭 모델에 대한 것이고, LQG는 모델 오차에 대한 보장된 여유가 없음이 증명되어 있다(Doyle 1978).
> 4. LQR 법칙이 제약을 지키고 상태를 그 안에 머물게 하는 종단 집합 안에서는 $x^\top P x$가 남은 비용을 정확히 준다. 그 종단 제약을 함께 두어야 짧은 지평으로도 안정성 논증이 성립한다 — 종단 비용과 종단 집합이 함께 [[04-robotics/mpc|7. MPC §5]]의 안정성 논증, 곧 Mayne 조건의 재료다(Borrelli 정리 12.2).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P4**, 곧 카탈로그의 새는 히터 $\dot x=-x+u+d$에 이번에는 $Q=3$, $R=1$로 값을 매긴다. 시뮬레이터 없음.

1. **그리기.** 과제의 가중치 $Q=3$, $R=1$에서의 위의 그림: $u=-Kx$인 새는 히터, $Q$와 $R$ 상자, 외란 $d$, 그리고 이 $P$와 $K$를 적은 리카티 화살표. 극점 축에는 이 폐루프 극점을 표시하고, 그림의 $Q=1$, $R=1$ 극점 옆에 $Q=1$, $R=4$일 때의 극점을 표시한 뒤, $R$을 올리면 극점이 어느 쪽으로 가는지 말하라.
2. **유도.** (a) $Q=3$, $R=1$에서의 스칼라 ARE: 두 근, 안정화 $P$와 $K$, 폐루프 극점, $d=1$의 $x_\mathrm{ss}$. (b) $d=0$, $x_0=1$에서 장부가 이득 셋에 매기는 값: 네가 구한 $K$, $K=0$, 5 §1의 손 이득 $K=9$에서의 $J(K)=(3+K^2)/(2(1+K))$. 가장 작은 것이 $P$인지 확인하라. (c) 비틀기: 어떤 $Q/R$이면 LQR이 스스로 $K=9$를 고르는가? 그 극점과 $x_\mathrm{ss}$도.
3. **해석.** (c)는 5 §1의 손 이득이 어떤 가중치에서는 LQR 최적이라는 뜻이다. P4에서는 $K\ge0$인 모든 이득이 그렇다는 것을 보이고, "LQR을 썼다"고만 쓰고 $Q$와 $R$을 밝히지 않은 논문에 그것이 무슨 뜻인지, 그리고 $Q/R$을 올려서 얻는 것과 치르는 것([[04-robotics/control-theory-ce397|5. 제어 이론 §1]]의 $(1+K)$ 거래)을 말하라.

> [!note]- 그리는 법 · How to draw it
> - 루프: 합산점 하나, 그 뒤의 장치 상자 $\dot x=-x+u+d$, 그 합산점으로 $u$와 나란히 들어오는 외란 $d$, 상자에서 나오는 상태 $x$, 그리고 $x$에서 이득 상자 $-K$를 거쳐 합산점으로 돌아가는 피드백 경로. 여기까지는 제어 이론 페이지의 그림 그대로다.
> - LQR이 더하는 장부: $x$에서 상자 $Q$로 가는 가지, $u$에서 상자 $R$로 가는 가지, 그리고 둘이 함께 들어가는 누산기 $J=\int_0^\infty (Qx^2+Ru^2)\,dt$.
> - 장부는 선 굵기를 달리해 그린다. 장치를 전혀 건드리지 않는 회계 경로이지 제어 경로가 아니며, 이렇게 시각적으로 갈라 두어야 $Q$·$R$이 §4에서 같은 루프로 들어오는 잡음 공분산 $W$·$V$와 섞이지 않는다.
> - $-K$ 상자 옆에는 리카티 방정식이 곧 화살표 하나라는 것: $(Q,R)\rightarrow P\rightarrow K$, *오프라인에서 한 번*. 여기에 이 과제의 숫자 $(3,1)\rightarrow1\rightarrow1$을 적는다. 위 그림의 $1.236$이 아니다.
> - 루프 아래의 실수축: 제어하지 않은 히터가 이미 앉아 있는 개루프 극점 $-1$과 폐루프 극점 $-(1+K)$.
> - 이 장치에서 안정화 리카티 해는 $P=-R+\sqrt{R^2+QR}$, $K=P/R=-1+\sqrt{1+Q/R}$이므로 폐루프 극점은 $-\sqrt{1+Q/R}$에 놓인다. $Q=3$, $R=1$이면 $-2$, $Q=1$, $R=4$면 그림의 $-1.414$보다 오른쪽인 $-1.118$이다.
> - 그릴 값이 있는 화살표: $R$을 올리면 극점이 $-1$ 쪽으로 되돌아가고, $Q$를 내렸을 때와 똑같다. 식에 나오는 것은 비 $Q/R$뿐이기 때문이다.

> [!tip]- 정답 · Solutions
> 1. $Q=3$, $R=1$에서의 위 그림의 루프와 장부이고, 리카티 화살표는 $(3,1)\rightarrow P=1\rightarrow K=1$이다. 축 위에는 개루프 극점 $-1$, 이 폐루프 극점 $-\sqrt{1+Q/R}=-2$, 그리고 $Q=1$, $R=4$일 때 $P=-4+\sqrt{20}=0.472$, $K=P/R=0.118$에서 오는 극점 $-\sqrt{1.25}=-1.118$이 있고, 마지막 것은 $Q=1$, $R=1$인 그림의 $-1.414$보다 오른쪽이다. $R$을 올리면 극점이 $-1$ 쪽으로 되돌아간다. 극점을 정하는 것은 $Q/R$뿐이므로, 노력에 값을 더 매기는 것과 오차에 값을 덜 매기는 것은 같은 수다.
> 2. (a) $-2P-P^2+3=0$, 곧 $(P-1)(P+3)=0$이므로 $P=1$ 또는 $P=-3$이다. 안정화 근은 $P=1$이라 $K=1$, 극점은 $-(1+K)=-2$, $x_\mathrm{ss}=1/2=0.5$다. 근 $-3$은 $K=-3$과 $\dot x=+2x$를 준다. (b) $J(1)=4/4=1.0=P$, $J(0)=3/2=1.5$, $J(9)=84/20=4.2$다. 개루프는 LQR보다 절반이 더 들고, 손 이득은 네 배 넘게 든다. (c) $K=-1+\sqrt{1+Q/R}=9$는 $1+Q/R=100$일 때, 곧 $Q/R=99$일 때다. 극점은 $-10$, $x_\mathrm{ss}=0.1$이다.
> 3. $K=-1+\sqrt{1+\rho}$를 뒤집으면 $\rho=Q/R=(1+K)^2-1=K^2+2K$이고, 이것은 $K\ge0$이면 언제나 $\ge0$이다. 그러니 이 장치에서는 손으로 골랐든 아니든 음수가 아닌 모든 이득이 가중치 $Q/R=K^2+2K$에서 LQR 최적이다. $K=1$이면 $3$, $K=4$면 $24$, $K=9$면 $99$다. 그래서 가중치 없는 "최적"은 루프가 얼마나 세게 움직이는지에 대해 아무것도 말하지 않는다. 설계는 가중치에 있다. $Q/R$을 올리면 $K$가 커져 $x_\mathrm{ss}=d/(1+K)$가 줄고($Q/R=99$면 개루프의 10분의 1), 대가로 노력 $u=-Kx$가 늘고 센서 잡음이 같은 $K$를 거쳐 $u$에 들어온다. 5 §1의 거래다.

### 출처 · Sources

- R. E. Kalman, "Contributions to the theory of optimal control," *Boletín de la Sociedad Matemática Mexicana* 5, 1960 — 무한 지평 선형 이차 조정기와 그 리카티 방정식.
- B. D. O. Anderson and J. B. Moore, *Optimal Control: Linear Quadratic Methods*, Prentice Hall, 1990 (Dover 재간, 2007) — §1–§4의 표준 교재: 연속·이산 리카티 방정식, 안정화 가능성과 검출 가능성, LQG.
- J. C. Doyle, "Guaranteed margins for LQG regulators," *IEEE Transactions on Automatic Control* 23(4), 1978 — §4의 예와 그 한 줄 초록.
- F. Borrelli, A. Bemporad and M. Morari, *Predictive Control for Linear and Hybrid Systems*, Cambridge University Press, 2017 — 스스로 점검 4가 인용하는 정리 12.2.
- R. Tedrake, *Underactuated Robotics*의 LQR 장(온라인 교재, 맨 위 링크) — 기하적 직관과 코드.
- 맨 위에 링크한 강의 슬라이드 — 유한 지평 이산 시간 LQR을 먼저, 이어서 라그랑주 승수로 한 유도, 무한 지평, 연속 시간. §1.5 다음에 읽고, [[02-foundations/optimization|4. 최적화 §5]]의 MPC-QP 예제로 이어 가라.
- 이 페이지의 모든 숫자는 페이지 자신의 식으로 손으로 풀고 NumPy로 검산했다.
