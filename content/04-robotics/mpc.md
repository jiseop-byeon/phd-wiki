---
title: "7. MPC"
tags: [robotics, control]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Key reference** — Mayne, Rawlings, Rao & Scokaert, *Constrained model predictive control: Stability and optimality*, Automatica 2000 · [DOI](https://doi.org/10.1016/S0005-1098(99)00214-9)

## English

*Group D. Stands on [[04-robotics/control-theory-ce397|5]] and [[04-robotics/lqr-lqg|6]], and turns the finite-horizon program of [[04-robotics/planning-decision-making|4. Planning §6]] into feedback. Handling input and state constraints natively is its whole reason for existing
next to LQR, and [[04-robotics/convex-mpc-legged|8. Convex MPC]] is the application that made it standard on legged robots.*

> [!info] Depth target · 깊이 목표
> Read an MPC formulation (cost, horizon, constraints), identify what is solved online at each step, judge feasibility/stability claims, and recognize the standard failure modes. Solver internals are optional.
> MPC 정식화(비용·지평·제약)를 읽고, 매 스텝 온라인으로 무엇이 풀리는지 짚고, 실행 가능성(feasibility)·안정성 주장을 판단하고, 표준 실패 모드를 알아볼 수 있으면 된다. 솔버 내부는 선택이다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/control-theory-ce397|5. Control Theory §4 and §9]] (when a sampled loop is stable, and §9's rail on the leaky heater — saturation is the gap MPC exists to close) · [[04-robotics/lqr-lqg|6. LQR / LQG §1–§2]] (the Riccati $P$, MPC's usual terminal cost, and its discrete-time twin) · [[04-robotics/planning-decision-making|4. Planning §6]] (the finite-horizon program, direct shooting and direct transcription) · [[02-foundations/optimization|4. Optimization §2–5]] (convexity, the KKT optimality conditions, and the example that writes MPC as a quadratic program, a QP: a quadratic cost under linear constraints) · [[04-robotics/state-estimation-slam|3. State Estimation §5]] (the Kalman filter, which can also estimate a disturbance) · [[02-foundations/lab-plants|0.6 Lab Plants]] (P4, the catalog's leaky heater, the running object; a *plant* is control's word for the system being controlled)
> [[04-robotics/control-theory-ce397|5. 제어 이론 §4, §9]] (샘플한 루프가 언제 안정한가, 그리고 새는 히터에 레일을 건 §9 — 포화가 MPC가 메우려는 그 간극이다) · [[04-robotics/lqr-lqg|6. LQR / LQG §1–§2]] (MPC의 표준 종단 비용인 리카티 $P$와 그 이산 시간 쌍둥이) · [[04-robotics/planning-decision-making|4. 계획 §6]] (유한 지평 문제, direct shooting과 direct transcription) · [[02-foundations/optimization|4. 최적화 §2–5]] (볼록성, KKT 최적성 조건, 그리고 MPC를 이차 계획, 곧 선형 제약 아래의 이차 비용인 QP로 적은 예제) · [[04-robotics/state-estimation-slam|3. 상태 추정 §5]] (외란도 추정할 수 있는 칼만 필터) · [[02-foundations/lab-plants|0.6 Lab Plants]] (이 페이지의 대상인 카탈로그의 새는 히터 P4. *장치*(plant)는 제어에서 제어 대상이 되는 시스템을 부르는 말이다)

> [!note] Why this matters · 왜 배우는가
> On the [[physical-ai-map|Physical AI Map]] this page sits in the control column beside the robot stack of [[07-research-program/index|7. Research Program §5]], and in *"install that panel on the frame"* it serves *move the component* within the limits the hardware and the site impose: actuator effort, joint range, the panel as an obstacle. A gain designed without those limits promises motion the hardware cannot deliver: [[04-robotics/control-theory-ce397|5. Control Theory §4]]'s hand gain $K=99$ asks P4, the catalog's leaky heater ([[02-foundations/lab-plants|0.6]]), for $u=-49.5$ at $x=0.5$ against a rail $|u|\le1$ and, sampled at the catalog's $0.1$ s, is not even stable, whereas an MPC that plans with the rail stays stable at that clock and shows exactly what it gives up — an offset of $0.154$ from the disturbance its model leaves out (Worked case). [[04-robotics/convex-mpc-legged|8. Convex MPC §2]] solves the same kind of QP at tens of hertz on contact forces, [[02-foundations/rl-robot-learning|7.5 RL §4]] names MPC as the usual safety filter around a learned policy, and [[03-deep-learning/vla/index|deep learning 4. VLA §3]] reads a policy's action chunk as a receding-horizon plan run partly open loop, the trade [[05-construction-robotics/imitating-contact|construction 10 §4]] faces at the panel; the page is block 2 of the dissertation path ([[07-research-program/index|7 §8]], robotics sessions 77–78), and those links lead into blocks 4 and 7. After it you can read an MPC formulation (cost, horizon, constraints, terminal ingredients), say what is solved online at each step, and check a paper's feasibility, stability and solve-time claims.

> [!note] First pass · 처음이라면
> Two sessions of 60–90 minutes, robotics 77–78. **Session 1 (77):** the definition below, the Running object, the picture, and the Worked case with a calculator — Steps 1–4 by hand, Steps 5–6 read — then §1 and §3. End by redoing Step 2 with the page covered (the three predicted states, and why even the last input stays on the rail) and naming Step 5's offset and what would remove it; then find two of §3's failure modes in a paper's MPC section. **Session 2 (78):** §2 (its Deeper note is optional), §4, and §5 — Mayne's two conditions, checked by hand on the discrete integrator with its number-line figure — then the self-check and the problem set; end with problem 2(d), the terminal set and feasible set at half the rail. A Literacy pass stops after session 1.

**What it is**: **Model Predictive Control** solves, at every control step, a finite-horizon
optimal control problem from the current state, applies only the first input, and re-solves
at the next step (receding horizon). Written out, at time $t$, with measured (or estimated) state
$x(t)$, it solves

$$\min_{u_0,\ldots,u_{N-1}} \sum_{k=0}^{N-1} \ell(x_k, u_k) + V_f(x_N) \quad \text{s.t.} \quad x_{k+1} = f(x_k, u_k),\;\; x_k \in \mathcal X,\;\; u_k \in \mathcal U,\;\; x_N \in \mathcal X_f,\;\; x_0 = x(t)$$

and applies $u(t) = u_0^\star$, because only the first input is used before the next measurement
arrives and the whole problem is solved again. Its named components are the **prediction model**
$f$ (for linear MPC $f(x,u) = Ax + Bu$); the **horizon** $N$, the number of steps looked ahead;
the **stage cost** $\ell$ (for linear MPC $x^\top Q x + u^\top R u$); the **terminal cost** $V_f$,
which stands in for everything after step $N$ (typically $x^\top P x$ with the LQR $P$); the
**constraint sets** $\mathcal X$ and $\mathcal U$ for states and inputs; and the **terminal set**
$\mathcal X_f$ in which the prediction must end. This is the program of [[04-robotics/planning-decision-making|4. Planning §6]] — its terminal cost $\ell_f$ is $V_f$ here — re-solved at every step; [[02-foundations/optimization|4. Optimization §5]] wrote its linear-quadratic case as a QP and capped the discrete integrator at $|u|\le0.2$. *Non-example:* solving this once and executing the
whole sequence $u_0, \ldots, u_{N-1}$ is open-loop optimal control, not MPC; the re-solve from a new
measurement is what supplies the feedback. With linear dynamics, positive-semidefinite quadratic
state/terminal costs, a positive-definite input cost, and affine equality plus linear
inequality constraints, it is a convex QP — written out fully in
[[02-foundations/optimization|4. Optimization §5]]. More general convex constraints can
produce a convex program that is not a QP —
and constraints on inputs and states are handled *natively*, which is
MPC's whole advantage over [[04-robotics/lqr-lqg|LQR]].

### Running object · 이 페이지의 대상

**P4** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's leaky heater: $\dot x=-x+u+d$, with $x$ the temperature error, $u$ the heater command and $d$ a disturbance. Held constant over each step of $T=0.1$ s (a zero-order hold, [[04-robotics/control-theory-ce397|5. Control Theory §4]]) it is exactly

$$x_{k+1}=a\,x_k+b\,(u_k+d),\qquad a=e^{-T}=0.904837,\qquad b=1-e^{-T}=0.095163$$

since $d$ enters beside $u$ and so gets the same factor $b$ — 0.6's sampled model with the disturbance put back. Note $a+b=1$. On this page the heater has a **rail** $|u_k|\le1$, the actuator's limit, and a constant $d=1$ that the planner does **not** measure: its prediction model leaves $d$ out. The MPC that runs on it is frozen as:

| Symbol | Value | Meaning |
|---|---|---|
| model | $x_{k+1}=0.904837\,x_k+0.095163\,u_k$ | the planner's prediction, with $d$ left out |
| $N$ | $3$ | horizon: three steps, $0.3$ s |
| $\ell(x,u)$ | $100x^2+u^2$ | stage cost: $q=100$ on the error, $r=1$ on the command |
| $V_f(x)$ | $152.43\,x^2$ | terminal cost, the discrete Riccati solution for this $q,r$ (Worked case, Step 1) |
| $\mathcal U$ | $\lvert u\rvert\le1$ | the rail; no state constraint until the problem set |
| $x(t)$ | $0.5$ | the measured state the Worked case starts from |

The ratio $q/r=100$ is chosen, not arbitrary: it is what makes both plans of the Worked case put all three inputs on the rail (it takes $q$ above $88$ at $r=1$; at $q=1$ the plan from $0.5$ would be $(-0.19,-0.17,-0.15)$, well inside it).

*Scope: this page teaches linear MPC at reading level — the problem solved online (the definition, the Worked case), when it is a convex QP (§1), its two solver forms (§2), how it fails on hardware (§3), where nonlinear and contact MPC depart (§4), and Mayne's conditions for feasibility and stability (§5). It does not teach solver internals, explicit MPC, or robust (tube) and offset-free MPC in full; those are in the books under Sources, and the estimator that offset-free MPC needs is [[04-robotics/state-estimation-slam|3. State Estimation §5]]'s. The one application worked end to end is [[04-robotics/convex-mpc-legged|8. Convex MPC]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 380" style="max-width:100%;height:auto" role="img" aria-label="Receding horizon of length 3 on the leaky heater P4 at x(t) = 0.5, with stage cost 100x² + u² and terminal cost 152.4x²: predicted states 0.357, 0.228 and 0.111 above a time axis, the three planned inputs pinned at the rail u = −1 inside the band from −1 to +1, the K = 99 demand of −49.5 far below it, d = 1 entering the plant unmeasured, the new measurement 0.452 above the predicted state and the horizon re-planned from it; right, the steady states from 0 to 2 that the rail permits, with the MPC's settling point 0.154 marked and K = 99's aim of 0.01 noted as unstable once sampled.">
  <defs><marker id="aMPC" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <rect x="20" y="26" width="128" height="46" rx="3"/>
    <circle cx="206" cy="47" r="10"/>
    <rect x="252" y="30" width="150" height="34" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" marker-end="url(#aMPC)">
    <line x1="148" y1="47" x2="194" y2="47"/>
    <line x1="206" y1="12" x2="206" y2="35"/>
    <line x1="216" y1="47" x2="250" y2="47"/>
    <polyline points="402,47 470,47 470,84 84,84 84,74"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="56" y1="210" x2="268" y2="210"/>
    <line x1="64" y1="206" x2="64" y2="214"/>
    <line x1="128" y1="206" x2="128" y2="214"/>
    <line x1="192" y1="206" x2="192" y2="214"/>
    <line x1="256" y1="206" x2="256" y2="214"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.45">
    <line x1="268" y1="210" x2="328" y2="210"/>
    <line x1="320" y1="206" x2="320" y2="214"/>
    <line x1="64" y1="200" x2="320" y2="200" stroke-dasharray="1 3"/>
  </g>
  <rect x="64" y="238" width="192" height="50" fill="currentColor" fill-opacity="0.10"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.7">
    <line x1="64" y1="238" x2="256" y2="238"/>
    <line x1="64" y1="288" x2="256" y2="288"/>
    <line x1="64" y1="263" x2="256" y2="263" stroke-dasharray="1 3"/>
  </g>
  <rect x="78" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="142" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="206" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <ellipse cx="96" cy="275.5" rx="27" ry="16" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <line x1="96" y1="291" x2="96" y2="302"/>
    <path d="M90 305 L102 301 M90 310 L102 306"/>
    <line x1="96" y1="309" x2="96" y2="356" marker-end="url(#aMPC)"/>
  </g>
  <polyline points="64,105 128,132.1 192,156.7 256,178.9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="128,114 192,140.3 256,164.1 320,185.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" stroke-opacity="0.45"/>
  <circle cx="64" cy="105" r="4" fill="currentColor"/>
  <circle cx="128" cy="132.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="156.7" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="256" cy="178.9" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="140.3" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="256" cy="164.1" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="320" cy="185.6" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="128" cy="114" r="4" fill="currentColor"/>
  <path d="M134 114 H137 V132.1 H134" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <line x1="137" y1="123.1" x2="196" y2="112" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <rect x="330" y="284" width="200" height="16" fill="currentColor" fill-opacity="0.22"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="318" y1="292" x2="544" y2="292"/>
    <line x1="330" y1="281" x2="330" y2="303"/>
    <line x1="430" y1="281" x2="430" y2="303"/>
    <line x1="530" y1="281" x2="530" y2="303"/>
  </g>
  <path d="M345.4 302 l-5 9 h10 z" fill="currentColor"/>
  <path d="M324 322 l-4.5 8 h9 z" fill="currentColor"/>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="84" y="40">MPC: N = 3, |u| ≤ 1</text>
    <text x="84" y="54">ℓ = 100x² + u²</text>
    <text x="84" y="67" xml:space="preserve">V<tspan dy="3" font-size="10">f</tspan><tspan dy="-3"> = 152.4x²</tspan></text>
    <text x="327" y="52" font-size="12">ẋ = −x + u + d</text>
    <text x="64" y="226">t</text>
    <text x="128" y="226">t+1</text>
    <text x="192" y="226">t+2</text>
    <text x="256" y="226">t+3</text>
    <text x="320" y="226" opacity="0.5">t+4</text>
    <text x="96" y="255">u<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="160" y="255">u<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="224" y="255">u<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="330" y="276">0</text>
    <text x="430" y="276">1</text>
    <text x="530" y="276">2</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="160" y="41">u<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="214" y="22">d = 1, not measured</text>
    <text x="462" y="80" text-anchor="end" opacity="0.85">measured x</text>
    <text x="58" y="95">x(t) = 0.5, measured</text>
    <text x="200" y="110">new measurement at t+1, above the predicted x<tspan dy="3.5">1</tspan><tspan dy="-3.5">:</tspan></text>
    <text x="200" y="124">that gap is the feedback (d = 1 is not in the model)</text>
    <text x="336" y="150" opacity="0.9">dashed: the plan, only step one runs</text>
    <text x="336" y="164" opacity="0.6">lighter: re-planned from the new x</text>
    <text x="58" y="242" text-anchor="end">u = +1</text>
    <text x="58" y="292" text-anchor="end">u = −1</text>
    <text x="58" y="204" text-anchor="end" opacity="0.7">x = 0</text>
    <text x="140" y="306" opacity="0.85" xml:space="preserve">only u<tspan dy="3.5">0</tspan><tspan dy="-3.5"> reaches the plant</tspan></text>
    <text x="108" y="338">K = 99 asks u = −Kx = −49.5</text>
    <text x="108" y="352" opacity="0.85">far below the band (off scale)</text>
    <text x="318" y="248">steady states the rail permits</text>
    <text x="318" y="262" xml:space="preserve">0 = −x + u + d ⇒ x<tspan font-size="10" dy="3">ss</tspan><tspan dy="-3"> = u + 1 ∈ [0, 2]</tspan></text>
    <text x="332" y="330">0.154 = d/(1 + 5.51): this MPC</text>
    <text x="318" y="344">settles here, d missing from its model</text>
    <text x="318" y="360" opacity="0.85">0.01 = d/(1 + 99): K = 99's aim, a gain</text>
    <text x="318" y="374" opacity="0.85">the 0.1 s clock makes unstable</text>
    <text x="342" y="226" opacity="0.7">one step = 0.1 s</text>
  </g>
</svg>

One receding-horizon step of the Running object at the measured $x(t)=0.5$: with stage cost $100x^2+u^2$ and terminal cost $152.4x^2$ the $N=3$ plan pins all three inputs at the rail $u=-1$ and predicts $0.357$, $0.228$ and $0.111$, while the hand gain $K=99$ would ask $u=-49.5$. Only the circled $u_0$ reaches the plant; the unmeasured $d=1$ lifts the next measurement to $0.452$, and that gap is the feedback — the lighter plan is re-solved from it ($0.314$, $0.189$, $0.076$). On the right, the steady states the rail permits, $x_\mathrm{ss}=u+1\in[0,2]$: this MPC settles at $0.154$ (Worked case, Step 5), and $K=99$'s aim of $0.01$ needs a gain the $0.1$ s clock makes unstable (Step 6).

### Worked case · 대상으로 한 번 끝까지

One step of the receding horizon on P4, from the terminal cost to where the loop settles. Every number is a calculator's work.

**Step 1 — The terminal cost.** $V_f$ stands in for the whole future after step $3$, and the cost of that future under the best linear law is what the discrete-time Riccati equation (DARE) returns ([[04-robotics/lqr-lqg|6. LQR / LQG §1.5]], where the discrete integrator's $P=1.618$ is worked). For one state it reads

$$P=q+a^2P-\frac{(abP)^2}{r+b^2P}\quad\Longleftrightarrow\quad b^2P^2+\big((1-a^2)\,r-q\,b^2\big)P-q\,r=0$$

because multiplying through by $r+b^2P$ cancels the two $a^2b^2P^2$ terms. With the numbers it is $0.009056\,P^2-0.7243\,P-100=0$, whose positive root is $P=152.43$, and the law it belongs to has the gain $K=abP/(r+b^2P)=13.125/2.380=5.514$. (Check on 6's integrator, $a=b=q=r=1$: the quadratic becomes $P^2-P-1=0$ and $P=1.618$.) So $V_f=152.43\,x^2$, and the loop $u=-5.514x$ would multiply the state by $a-bK=0.380$ each step.

**Step 2 — The plan from $x=0.5$.** Without the rail the answer would be that law: $u_0=-5.514\times0.5=-2.76$, beyond $|u|\le1$. So try all three inputs on the rail. Each step then multiplies by $a$ and subtracts $b$, so the model predicts

$$x_1=0.904837\times0.5-0.095163=0.357,\qquad x_2=0.228,\qquad x_3=0.111$$

Is even the last input on the rail? From $x_2=0.228$ the terminal law would ask $-Kx_2=-1.26$, still beyond it, so $u_2=-1$ too. The full check is the KKT condition for a box ([[02-foundations/optimization|4. Optimization §4]]): at a lower bound the cost's slope must be positive, so that raising the input off the rail would cost more. Differentiating $J=\sum_{k=0}^{2}(100x_k^2+u_k^2)+152.43\,x_3^2$ through the model gives $\partial J/\partial u_k=11.37,\ 5.26,\ 1.23$ for $k=0,1,2$ — the last is $2(u_2+bPx_3)=2(-1+1.613)$ — and all three are positive. The plan is $u=(-1,-1,-1)$, at a predicted cost of $47.85$.

**Step 3 — Apply one input, measure.** Only $u_0=-1$ reaches the plant, which also receives $d=1$, so its net input is $u_0+d=0$ and

$$x(t+1)=a\,x(t)+b\,(u_0+d)=0.904837\times0.5=0.452$$

against the predicted $0.357$. The gap, $0.095=b\,d$, is one step of the disturbance the model left out, and it is the only way the controller ever learns of $d$.

**Step 4 — Re-plan from the measurement.** The same problem from $x=0.452$ returns the rail again: predictions $0.314$, $0.189$ and $0.076$, with the last input only just pinned ($-Kx_2=-1.04$; slopes $9.04$, $3.59$, $0.20$). Nothing of Step 2's plan beyond its first input was ever executed: that is the receding horizon.

**Step 5 — Where the loop settles.** Repeating Steps 3–4, the rail cancels $d$ exactly ($u+d=0$), so $x$ coasts like the unforced heater, shrinking by the factor $0.905$ a step (a $1$ s time constant). After eleven steps on the rail $x=0.166$, below $1/K=0.181$, and the plan leaves it. From there the input is the LQR law $u=-5.514x$ — $V_f$ is the exact cost-to-go, so off the rail the short horizon changes nothing — and with $d$ acting, the steady state solves

$$x=a\,x+b\,(-Kx+d)\quad\Longrightarrow\quad x_\mathrm{ss}=\frac{d}{1+K}=\frac{1}{6.514}=0.154$$

since $1-a=b$. The loop settles at $0.154$ with $u=-0.846$, inside the rail: stable, but off target, and each plan still predicts a descent that $d$ undoes — §3's model mismatch in one number. No weights remove it: any LQR gain stays below the deadbeat gain $a/b=9.51$, so the offset stays above $1/(1+a/b)=b=0.095$. What removes it is integral action ([[04-robotics/control-theory-ce397|5. Control Theory §7]]) or, in MPC's own terms, putting $d$ into the model and estimating it like any other state ([[04-robotics/state-estimation-slam|3. State Estimation §5]]), which is called offset-free MPC. On this one-state plant the eleven steps also show that the applied input is exactly the clipped law $u=\mathrm{sat}(-5.514x)$; the QP earns more than clipping when a constraint lies ahead in the plan — the problem set's state limit, or §5's terminal set.

**Step 6 — What $K=99$ would have done.** [[04-robotics/control-theory-ce397|5. Control Theory §4]]'s hand gain $K=99$ was chosen for a steady state of $d/(1+K)=0.01$, and at $x=0.5$ it asks $u=-49.5$. Clipped to the rail in continuous time, $u=\mathrm{sat}(-99x)$ still gets there: while $99x>1$ the rail cancels $d$, $x=0.5\,e^{-t}$ reaches $1/99=0.0101$ at $t=\ln49.5=3.9$ s, and the loop then settles at $0.0100$. What the rail voids is the transient the linear design promised — its pole at $-100$, a $10$ ms time constant — not the steady state. On this page's clock the gain fails outright: held over $T=0.1$ s, $u_k=-Kx_k$ gives $x_{k+1}=(0.905-0.095K)\,x_k+0.095\,d$, stable only for $K<(1+a)/b=20.02$ ($19$ under explicit Euler, 5 §4). $K=99$ gives the multiplier $-8.52$, and the clipped loop rides the rail down to $0.01$ in $3.9$ s, then bounces between $0.009$ and $0.017$ without ever settling. MPC's gain came from a cost on the sampled model, so it is stable at the same clock; the price of leaving $d$ out is Step 5's offset.

### 1. When is the QP actually convex?

The "it's just a QP" claim carries conditions worth checking in any paper:

- **Cost**: $Q \succeq 0$, $R \succ 0$, terminal $P \succeq 0$ — the quadratic must be
  (semi)definite ([[02-foundations/linear-algebra|1. Linear Algebra §3]]). An indefinite $Q$
  (e.g., from a learned cost) breaks convexity silently.
- **Dynamics**: linear (or linearized — then the QP is only an approximation whose quality
  decays away from the linearization point).
- **Constraints**: input/state sets must be convex (boxes, polytopes). **Obstacle-avoidance
  constraints are non-convex** — which is why collision-aware MPC papers either convexify
  locally (safe corridors) or leave the QP world entirely. A set is convex when the segment
  between any two of its points stays inside it (the definition, and the conditions for a convex
  problem, are in [[02-foundations/optimization|4. Optimization §2]]). The free space outside a
  unit-radius obstacle at the origin, $\lVert p\rVert \ge 1$, contains $(-1.5, 0)$ and $(1.5, 0)$
  but not their midpoint $(0, 0)$, so it fails that test.

**The test on a number.** Condense the integrator that [[04-robotics/planning-decision-making|4. Planning §6]] costed by hand — $x_{t+1}=x_t+u_t$, $x_0=1$, $N=2$, $\ell=x^2+u^2$, terminal cost $x_2^2$ — by substituting $x_1=1+u_0$ and $x_2=1+u_0+u_1$:

$$J(u_0,u_1)=1+u_0^2+(1+u_0)^2+u_1^2+(1+u_0+u_1)^2,\qquad H=\begin{pmatrix}6&2\\2&4\end{pmatrix}$$

where $H$ is the Hessian, the matrix of $J$'s second derivatives. Its eigenvalues $5\pm\sqrt5=7.24$ and $2.76$ are positive, so $J$ is a strictly convex bowl and its one stationary point, $u=(-0.6,-0.2)$ with $J=1.60$, is the global minimum — below all three plans 4 §6 costed ($1.75$, $2$ and $3$). *Non-example:* put a weight $q=-3$ on $x_1$, as a learned cost can; the top-left entry becomes $4+2q=-2$ and $\det H=-12<0$, a saddle, so the QP is non-convex and a local solver can stop at a stationary point that is not a minimum. $Q\succeq0$ is the condition a paper can state; the Hessian's eigenvalues are the test.

### 2. What the solver actually sees

At 50 Hz the entire solve must finish inside **20 ms**, minus whatever state estimation already spent, and how the problem is written down decides how much of that budget the solver needs. There are two standard ways to write the same problem — papers assume you know which one they use — and they are [[04-robotics/planning-decision-making|4. Planning §6]]'s direct transcription and direct shooting under MPC's names:

- **Stacked (sparse) form**, 4 §6's direct transcription: keep all states $x_{0:N}$ and inputs $u_{0:N-1}$ as
  variables and add dynamics as equality constraints — a large, *sparse, banded* problem
  that interior-point solvers exploit; cost matrices sit in blocks along the diagonal.
- **Condensed form**, its direct shooting: eliminate the states using $x_k = A^k x_0 + \sum_j A^{k-1-j}Bu_j$,
  leaving only $u_{0:N-1}$ — a smaller but *dense* QP whose conditioning can worsen with
  horizon length (powers of $A$, cost weights and input directions).

**Size it, so "large" and "small" stop being adjectives.** Take a quadruped centroidal MPC
of the kind [[04-robotics/convex-mpc-legged|convex MPC papers]] run: state $n_x = 13$
(position, orientation, their velocities, plus gravity), input $n_u = 12$ (a 3-vector force
at each of 4 feet), horizon $N = 10$.

| | variables | equality constraints | Hessian |
|---|---|---|---|
| **Stacked** | $(N{+}1)n_x + Nn_u = 143 + 120 = 263$ | $Nn_x+n_x = 130+13 = 143$ | $263\times263$, **banded** — mostly zeros |
| **Condensed** | $Nn_u = 120$ | none (dynamics substituted in) | $120\times120$, **generally dense** — up to 14,400 entries |

Condensed has under half the variables, which sounds decisive until you notice its Hessian is
dense: $120^2 = 14{,}400$ stored entries in a dense representation, against a stacked matrix whose nonzero count grows only
linearly in $N$. Doubling the horizon roughly doubles stacked storage at fixed state/input dimensions; it *quadruples* the
condensed Hessian's entry count and, because generic dense Cholesky factorization is cubic in the variable
count, multiplies that factorization work by about eight — which is why this choice is a real engineering decision rather
than a stylistic one. [[04-robotics/convex-mpc-legged|8. Convex MPC]]'s sizing box counts the same condensed QP's $160$ friction-pyramid rows. The Deeper note says why the cubic is not forced, and how the initial state changes the stacked count.

> [!note]- Deeper · 더 깊이
> **The cubic is not forced by the dense form.** Axehill & Morari (*Systems & Control Letters* 61, 2012, Theorem 3) build a Cholesky factor of the condensed Hessian from the Riccati recursion's quantities in $O(N^2)$, and note that adding the eliminated states back as variables recovers the classical $O(N)$ Riccati solve. Rawlings, Mayne & Diehl §8.8.4 surveys condensing methods with this quadratic horizon dependence.
>
> **Count the initial state explicitly.** In the table, $x_0$ is retained as a variable, so its measured value requires another $n_x=13$ equality constraints in addition to the 130 dynamics equations. If you substitute the measured $x_0$ before forming the QP, remove both its 13 variables and those 13 constraints: the equivalent stacked formulation has 250 variables and 130 dynamics equalities. This bookkeeping changes the matrix dimensions, not the control problem.

Rule of thumb when reading: long horizons and state constraints → stacked; short horizons,
input constraints only → condensed. (Large powers of $A$ can worsen conditioning. Stable dynamics help, but do not alone guarantee good conditioning: weights, controllability and scaling also matter. Storage and dense factorization counts are not guarantees about total solver runtime.)

### 3. The failure modes papers gloss over

An MPC that works in simulation fails on hardware in four predictable ways, and a paper's MPC section is worth reading for which of them it measures and which it assumes away.

- **Infeasibility**: a disturbance pushes the state where *no* input sequence satisfies
  the constraints — the solver returns nothing, and the controller must do *something*.
  Standard fix: **constraint softening** — replace hard state constraints with penalized
  slack variables $\sigma \ge 0$ (cost $+\rho\|\sigma\|$), allowing violations of the relaxed constraints at a cost. For a state bound $x_k \le x_{max}$ it reads
  $$x_k \le x_{max} + \sigma_k, \qquad \sigma_k \ge 0, \qquad \text{cost} = \textstyle\sum_k \ell(x_k, u_k) + V_f(x_N) + \rho \sum_k \sigma_k$$
  so a violation of size $\sigma_k$ is permitted but costs $\rho\,\sigma_k$; with this linear ($\ell_1$) penalty and $\rho$ larger than the constraint's Lagrange multiplier, the softened problem returns the hard-constrained solution whenever that one exists (an *exact penalty*). This does not guarantee feasibility if the remaining hard constraints conflict. Input (actuator) constraints stay hard, and the controller needs a defined fallback when no usable solution is available.
- **Model mismatch**: MPC optimizes the *model's* future; bias between model and plant
  turns "optimal" plans into repeated small errors that feedback (the re-solving itself)
  must absorb — and re-solving absorbs it only in part: the Worked case's unmodelled $d=1$ leaves P4 at $0.154$ for good while every plan predicts a descent (Step 5), and estimating the bias as a state removes it. Watch for papers quantifying this vs assuming it away.
- **Latency and rate**: the plan is computed from a state estimate that is stale by the
  solve time ([[04-robotics/robot-systems-deployment|10. Robot Systems §3]]), and a better plan from an older state can be less useful than a modest plan from the current one, which is why timing belongs in the formulation rather than in a runtime footnote. **Warm starting**
  — initializing the solver from the previous solution shifted one step — is what makes
  high-rate MPC possible; cold-started NMPC at 100 Hz is a red flag.
- **Estimator coupling**: MPC consumes $\hat{x}$, not $x$
  ([[04-robotics/state-estimation-slam|3. State Estimation §5]]) — estimator bias becomes
  systematic constraint violation.

### 4. Linear vs nonlinear vs contact

Everything so far assumed linear dynamics, which is what made the problem a QP; once the model is nonlinear, or contact switches forces on and off, the problem changes class and so do the guarantees.

- **Linear MPC**: convex QP; solve times from microseconds to milliseconds *for
  small-to-moderate problems on modern CPUs* — always condition speed claims on problem
  size, solver, and hardware.
- **Nonlinear MPC (NMPC)**: sequential quadratic programming (SQP: solve a QP model of the problem at the current iterate, step, repeat, [[02-foundations/optimization|4. Optimization §4]]) or DDP-style solvers (differential dynamic programming: a second-order trajectory optimizer that alternates an LQR-like backward pass around the current trajectory with a forward rollout);
  local optima and initialization sensitivity return
  ([[04-robotics/planning-decision-making|4. Planning §6]]).
- **Contact-implicit MPC**: contact mode switches make the problem non-smooth
  ([[04-robotics/contact-force-tactile|9. Contact §1]]); the
  [[04-robotics/convex-mpc-legged|legged convex-MPC]] trick is to *pre-specify* the
  contact schedule so the remaining problem is convex — read that page as the
  representative escape route.

**Where it meets learning** (this wiki's angle):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]] is MPC with a *learned* model and a CEM solver (the cross-entropy method: sample input sequences, refit a Gaussian to the best few, repeat);
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]'s receding-horizon action
chunks borrow MPC's structure; learned-dynamics MPC for excavators is an active
construction-robotics direction ([[05-construction-robotics/earthmoving-heavy-machinery|construction 3. Earthmoving & Heavy Machinery]]).

### 5. When the plan stays feasible and the loop stable

Re-solving from every new state promises neither that the next problem has a solution nor that the state reaches the origin, and a well-behaved simulation proves neither. **The Mayne et al. 2000 survey**, the field's canonical reference, settled both with two conditions on the terminal cost and the terminal set:

- **(a) Recursive feasibility.** Suppose the horizon ends inside a **terminal set** that is
  *invariant* under a known local controller $\kappa_f$ (usually the LQR law $-Kx$): once the state is inside, that controller keeps it inside,
  $$x \in \mathcal X_f \implies f\big(x, \kappa_f(x)\big) \in \mathcal X_f, \qquad \mathcal X_f \subseteq \mathcal X, \qquad \kappa_f(x) \in \mathcal U \ \text{ for all } x \in \mathcal X_f$$
  so the state stays in the set, the set respects the state constraints, and the local control respects the input constraints. Then a feasible plan today implies
  a feasible plan tomorrow: drop the first step and append one step of that controller. This
  is **recursive feasibility**, the property MPC papers invoke by name.
- **(b) Stability from a cost decrease.** Suppose also that the terminal cost decreases by
  **at least the stage cost** under that controller, so that
  $V_f(f(x,u)) - V_f(x) \le -\ell(x,u)$ with $u = \kappa_f(x)$, for every $x \in \mathcal X_f$. Then the
  optimal cost becomes a Lyapunov function
  (a positive "energy" that strictly decreases along the closed loop, so the state must settle
  at the origin; the three defining conditions are in [[04-robotics/control-theory-ce397|5. Control Theory §4]]) and the origin is
  **asymptotically** stable, with the feasible set as its domain of attraction. The **feasible
  set** is the set of initial states for which at least one input sequence satisfies every
  constraint, and a **domain of attraction** is a set of initial states from which the closed loop
  converges to the origin. Merely
  decreasing is not enough; the decrease has to dominate the stage cost, and the conclusion
  holds only from states that were feasible to begin with.

Both conditions speak about the prediction model: "tomorrow's state" in (a) is the state the plan predicted, which a disturbance the model leaves out does not deliver. And the inequality in (b) is one assumption of four; the Deeper note lists the rest.

> [!note]- Deeper · 더 깊이
> **Fine print.** Borrelli's Theorem 12.2 also requires the stage and terminal costs to be continuous and
> positive definite, the sets to be closed and to contain the origin in their interior, and
> the terminal set to be control invariant inside the state constraints; Rawlings adds a
> stage-cost lower bound and weak controllability.
> With $\ell=x^\top Qx+u^\top Ru$, $Q\succ0$, $R\succ0$, $V_f=x^\top Px$
> from the LQR, and box constraints such as $|u|\le1$, most of these hold automatically: a
> positive-definite quadratic is continuous and positive definite and bounds the stage cost below
> by $\lambda_{\min}(Q)\lVert x\rVert^2$, a box around zero is closed with the origin inside, and weak
> controllability follows from a terminal set around the origin and a bounded feasible set. Two are real design work: finding a terminal set that the local law keeps
> invariant — the scalar example below does it by hand, and beyond a few states it is a polytope
> computation — and, when $Q$ is only semidefinite, checking detectability as in
> [[04-robotics/lqr-lqg|6. LQR / LQG §2]], because positive definiteness is then no longer free.

**Worked, on a second plant — not P4.** This example leaves the heater for the discrete integrator
$x_{k+1} = x_k + u_k$, because its LQR solution is already worked in
[[04-robotics/lqr-lqg|6. LQR / LQG §1.5]] and makes every check below a line of arithmetic. Take $|u_k| \le 1$, stage cost $\ell = x^2 + u^2$, and that
discrete LQR solution: $V_f = 1.618\,x^2$ and $\kappa_f(x) = -0.618\,x$.
- *Terminal set.* $|\kappa_f(x)| \le 1$ exactly when $|x| \le 1.618$, and the next state
  $0.382\,x$ stays in that interval, so $\mathcal X_f = [-1.618,\ 1.618]$ is invariant.
- *Cost decrease.* $V_f(0.382x) - V_f(x) = -1.382\,x^2$ and $\ell(x, \kappa_f(x)) = x^2 + 0.382\,x^2 = 1.382\,x^2$,
  so condition (b) holds with equality, as it must when $V_f$ is the exact LQR cost-to-go.
- *Feasible set.* Each step moves the state by at most $1$, so with $N = 2$ the feasible set is
  $|x| \le 2 + 1.618 = 3.618$. From $x = 4$ the problem has no solution.
- *One step.* From $x = 3$, unconstrained LQR would command $-1.854$, which violates $|u| \le 1$.
  The MPC problem returns $u_0 = u_1 = -1$ (predicted $x_2 = 1 \in \mathcal X_f$, cost $16.62$),
  the plant receives $-1$, and the next problem starts from $x = 2$. The shifted plan
  $(-1,\ \kappa_f(1) = -0.618)$ ends at $0.382 \in \mathcal X_f$, so it is feasible, exactly as (a)
  promised.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="Number line of the discrete integrator x(k+1) = x(k) + u(k) with |u| ≤ 1 and N = 2: the terminal set from −1.618 to 1.618 shaded dark, the feasible set from −3.618 to 3.618 shaded light, x = 4 crossed out as having no plan; above the axis the plan from x = 3 hops to 2 and then to 1 with u = −1 twice, cost 16.62; below it, dashed, the shifted plan from 2 hops to 1 and then to 0.382 with u = −1 and −0.618.">
  <defs><marker id="mayA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="62.9" y="116" width="434.2" height="24" fill="currentColor" fill-opacity="0.10"/>
  <rect x="182.9" y="116" width="194.2" height="24" fill="currentColor" fill-opacity="0.28"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="22.0" y1="140" x2="544.0" y2="140"/>
    <line x1="40.0" y1="136" x2="40.0" y2="144"/>
    <line x1="100.0" y1="136" x2="100.0" y2="144"/>
    <line x1="160.0" y1="136" x2="160.0" y2="144"/>
    <line x1="220.0" y1="136" x2="220.0" y2="144"/>
    <line x1="280.0" y1="136" x2="280.0" y2="144"/>
    <line x1="340.0" y1="136" x2="340.0" y2="144"/>
    <line x1="400.0" y1="136" x2="400.0" y2="144"/>
    <line x1="460.0" y1="136" x2="460.0" y2="144"/>
    <line x1="520.0" y1="136" x2="520.0" y2="144"/>
  </g>
  <path d="M515.0 135 L525.0 145 M515.0 145 L525.0 135" stroke="currentColor" stroke-width="2" fill="none"/>
  <path d="M458.0 134 Q430.0 88 403.0 134" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#mayA)"/>
  <path d="M398.0 134 Q370.0 88 343.0 134" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#mayA)"/>
  <path d="M398.0 146 Q370.0 180 343.0 146" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#mayA)"/>
  <path d="M338.0 146 Q321.5 180 305.9 146" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#mayA)"/>
  <circle cx="460.0" cy="140" r="4.2" fill="currentColor"/>
  <circle cx="400.0" cy="140" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="340.0" cy="140" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="302.9" cy="140" r="3.2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <g fill="currentColor">
    <text x="280" y="20" text-anchor="middle" font-size="12" xml:space="preserve">x(k+1) = x(k) + u(k),  |u| ≤ 1,  N = 2,  ℓ = x² + u²,  V<tspan dy="3" font-size="10">f</tspan><tspan dy="-3"> = 1.618x²</tspan></text>
    <text x="24" y="46" font-size="11" xml:space="preserve">solid: the plan from x = 3 through 2 to 1, u = (−1, −1), cost 16.62</text>
    <text x="24" y="62" font-size="11" opacity="0.85" xml:space="preserve">(the LQR law alone would ask −0.618 × 3 = −1.854, off the rail)</text>
    <text x="430.0" y="106" text-anchor="middle" font-size="11" xml:space="preserve">u<tspan dy="3" font-size="10">0</tspan><tspan dy="-3"> = −1</tspan></text>
    <text x="370.0" y="106" text-anchor="middle" font-size="11" xml:space="preserve">u<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"> = −1</tspan></text>
    <text x="332.0" y="88" text-anchor="end" font-size="11" xml:space="preserve">x<tspan dy="3" font-size="10">2</tspan><tspan dy="-3"> = 1 ∈ X</tspan><tspan dy="3" font-size="10">f</tspan></text>
    <text x="552" y="162" text-anchor="end" font-size="11">x = 4: no plan</text>
    <text x="40.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−4</text>
    <text x="100.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−3</text>
    <text x="160.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−2</text>
    <text x="220.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−1</text>
    <text x="280.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">0</text>
    <text x="460.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">3</text>
    <text x="370.0" y="182" text-anchor="middle" font-size="11">−1</text>
    <text x="321.5" y="182" text-anchor="middle" font-size="11">−0.618</text>
    <text x="302.9" y="130" text-anchor="middle" font-size="10">0.382</text>
    <text x="24" y="204" font-size="11" xml:space="preserve">dashed: after u₀ runs, the shifted plan from 2, (−1, κ<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">(1) = −0.618), ends at 0.382 ∈ </tspan>X<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">​</tspan></text>
    <text x="24" y="222" font-size="11" xml:space="preserve">dark: terminal set X<tspan dy="3" font-size="10">f</tspan><tspan dy="-3"> = [−1.618, 1.618], where </tspan>κ<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">(x) = −0.618x respects |u| ≤ 1</tspan></text>
    <text x="24" y="240" font-size="11" xml:space="preserve">light: feasible set, |x| ≤ 2 + 1.618 = 3.618, two unit steps from X<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">​</tspan></text>
  </g>
</svg>

The example on one line: the terminal set $[-1.618,1.618]$ (dark) inside the feasible set $|x|\le3.618$ (light), with $x=4$ outside both. Above the axis, the plan $3\to2\to1$ at cost $16.62$; below it, the shifted plan $2\to1\to0.382$ that (a) guarantees.

### After reading

- [ ] Describe the receding-horizon procedure (solve → apply the first input → re-solve), and run one step of it on P4 by hand
- [ ] State the conditions for a convex QP ($Q,R,P$ definiteness and affine/polyhedral constraints), distinguish it from a general convex program, and say where obstacle constraints break convexity
- [ ] Explain the stacked vs condensed trade-off, and infeasibility, constraint softening, and warm starting
- [ ] Say why an MPC whose model leaves a disturbance out settles off target, and what removes the offset
- [ ] Name Mayne 2000's stability ingredients (terminal cost, terminal set, horizon) and where PlaNet and Diffusion Policy borrow MPC's structure

### Self-check

1. You plug a learned cost matrix $Q$ into an MPC and the solver misbehaves. First thing to check?
2. Horizon $N=50$ with many state constraints — expect stacked or condensed? Why?
3. A disturbance pushes the state outside the constraint set. What happens under hard-constrained vs softened MPC?
4. A paper claims "our NMPC runs at 200 Hz." Name three things to check.

> [!tip]- Answers
> 1. Whether $Q \succeq 0$ — if indefinite, the QP can be non-convex (§1's saddle) and solver behavior is undefined.
> 2. Stacked — its structured (Riccati or sparse) solve grows linearly in $N$, while generic dense factorization of the condensed form grows as $N^3$ (or $N^2$ with Axehill–Morari); the condensed Hessian is dense at every horizon and its conditioning can degrade through powers of $A$; and state constraints stay sparse in the stacked form.
> 3. Hard: infeasible — the solver returns no usable command and a separate fallback must act. Soft: slacks can return a penalized violation **if the remaining hard constraints are feasible**; softening selected constraints does not guarantee that control can continue.
> 4. ① Warm-started or cold? ② Problem size (horizon, state dimension) and solver? ③ Is 200 Hz solve time or end-to-end latency ([[04-robotics/robot-systems-deployment|frequency ≠ latency]])?

### Problem set · 과제

Tier B. **P4** from [[02-foundations/lab-plants|0.6]], the Running object's MPC ($N=3$, $\ell=100x^2+u^2$, $V_f=152.43x^2$, $|u|\le1$, $d$ left out of the model), but now the disturbance is $d=1.5$; problem 2(d) returns to §5's discrete integrator. No simulator.

1. **Draw.** The picture for $d=1.5$, from the measured $x(t)=0.5$: the plan and its three predicted states, the $K=99$ demand, the new measurement at $t+1$ and the re-plan from it, and on the right the steady states the rail now permits, with the limit $x\le0.3$ of problem 2(c) and $K=99$'s aim marked.
2. **Derive.** (a) Under $|u|\le1$ and $d=1.5$, what interval can $x_\mathrm{ss}$ sit in? What steady state does $K=99$ aim at, and what $u$ would holding it take? Show that no controller can hold $x$ below $0.5$. (b) From $x=0.5$, what does the MPC plan, what does it predict for $t+1$, and what is measured? Where does the loop settle? (c) Add the state limit $x_k\le0.3$ on the predicted states $x_1,x_2,x_3$. From which measured $x$ is the hard-constrained problem feasible, and is it ever feasible in this loop? Soften it as in §3: what slack does each plan predict, and by how much does the plant actually violate the limit? (d) §5's discrete integrator with the rail halved, $|u|\le0.5$ (same $\ell$, $V_f$, $\kappa_f$, $N=2$): the terminal set, the feasible set, the plan from $x=1.5$ with its cost, the shifted plan after one step, and the verdict at $x=2$.
3. **Interpret.** Start the hard-constrained MPC of 2(c) at $x=0.4$, still with $d=1.5$. It is feasible there. When does it first fail? Does that contradict §5's condition (a)? Say which assumption failed and what a paper must state before it claims recursive feasibility on hardware.

> [!note]- How to draw it · 그리는 법
> - A time axis with ticks $t$ through $t+3$ (and $t+4$ for the re-plan). Above it the measured $x(t)=0.5$ as a filled dot, the predicted $x_1,x_2,x_3=0.357,\ 0.228,\ 0.111$ as open dots on a dashed line — the planner's problem is the lecture's, because its model has no $d$.
> - Below the axis, the input band between $u=-1$ and $u=+1$ with both edges labelled, the three planned inputs as bars on the rail, and $u_0$ circled, the only one that reaches the plant.
> - $K=99$'s demand as an arrow leaving the band: $u=-49.5$ at $x=0.5$, unchanged, since the gain does not depend on $d$.
> - $d=1.5$ on its own arrow into the summing junction ahead of the plant box, never through the controller.
> - The new measurement at $t+1$: $0.500$, level with $x(t)$, not the lecture's $0.452$. The gap to the predicted $0.357$ is $0.143=b\,d$. The re-plan, in a lighter line, starts from $0.500$ and repeats the first plan one tick to the right.
> - Beside it, a short $x$-axis with every steady state the rail permits shaded, $[0.5,\ 2.5]$, and both the limit $x\le0.3$ and $K=99$'s aim $0.015$ marked *outside* the shaded interval.
> - The drawing is wrong the moment the new measurement sits on the predicted $x_1$: that is the open-loop non-example at the top of this page. Here it is also wrong if the measured states descend: with $d=1.5$ the loop never leaves $0.5$.

> [!tip]- Solutions
> 1. As the checklist: the plan is the lecture's, but the measurement comes back at $0.500$, so the lighter re-plan is a copy of the first one shifted a tick. The loop is stuck on the rail, predicting a descent that never comes; the shaded steady states begin at $0.5$, and $0.3$ and $0.015$ both lie left of them.
> 2. (a) $0=-x+u+d$ gives $x_\mathrm{ss}=u+1.5\in[0.5,\ 2.5]$. $K=99$ aims at $d/(1+K)=0.015$, and holding it takes $u=-99\times0.015=-1.485$, beyond the rail. Holding any $x$ takes $u=x-1.5$, and $u\ge-1$ forces $x\ge0.5$ — 5. Control Theory §9's saturated steady state $x=d-1$, whatever the controller. (b) The planner's problem is the lecture's, so the plan is $(-1,-1,-1)$ and it predicts $0.357$. The plant receives $u+d=0.5$ and returns $x=0.904837\times0.5+0.095163\times0.5=0.500$, since $a+b=1$: the measurement equals the old state, the loop sits at $0.5$ with $u=-1$ for good, and every plan is the same. (c) The best the model can do in one step is $x_1=ax-b$, so $x_1\le0.3$ needs $x\le(0.3+b)/a=0.437$; the plant never goes below $0.5$, so the hard problem is infeasible at every tick. Softened, the plan stays $(-1,-1,-1)$ — $u_0$ is already on the rail — with a predicted slack of $0.357-0.3=0.057$ on $x_1$ and none on $x_2$ or $x_3$ ($0.228$, $0.111$), while the plant sits at $0.5$, $0.2$ above the limit, every tick: the planner underestimates its own violation by the same $b\,d$ it never models. (d) $|\kappa_f(x)|=0.618|x|\le0.5$ gives $\mathcal X_f=[-0.809,\ 0.809]$, invariant because $0.382x$ stays inside, and (b) still holds with equality, since the rail does not enter it. Each step moves $x$ by at most $0.5$, so the feasible set is $|x|\le1+0.809=1.809$. From $x=1.5$ LQR alone would ask $-0.927$; the plan is $(-0.5,-0.5)$, through $1.0$ to $0.5\in\mathcal X_f$, at cost $2.25+0.25+1+0.25+1.618\times0.25=4.15$ — both slopes at the rail are positive, $\partial J/\partial u_0=-1+2+1.618=2.618$ and $\partial J/\partial u_1=-1+1.618=0.618$. After one step the shifted plan $(-0.5,\ \kappa_f(0.5)=-0.309)$ from $1.0$ ends at $0.191\in\mathcal X_f$. From $x=2$ two steps reach $1.0$ at best, outside $\mathcal X_f$: no plan. Halving the rail halves both sets, because every bound scales with it.
> 3. The model predicts $x_1=0.267$ from $0.4$, but the plant returns $0.410$; the next measurements are $0.418$, $0.426$, $0.433$ and $0.439$, which is above $0.437$, so the sixth solve, at $t=0.5$ s, is infeasible. It does not contradict (a): (a) promises a feasible plan from the state the plan *predicted*, and the unmodelled $d$ puts the plant $b\,d=0.143$ higher every step (this MPC also has no terminal set, so (a)'s hypothesis was never met). From problem 2(a), no input keeps $x\le0.3$ under $d=1.5$, so the five feasible solves were a promise the plant could not keep. Before claiming recursive feasibility on hardware a paper must state the disturbance its constraints were designed for — tightened by the worst-case drift, as robust (tube) MPC does, or with $d$ estimated — and show that the tightened problem is still feasible.

### Sources

- D. Q. Mayne, J. B. Rawlings, C. V. Rao, P. O. M. Scokaert, "Constrained model predictive control: Stability and optimality," *Automatica* 36(6), 789–814, 2000 · [DOI](https://doi.org/10.1016/S0005-1098(99)00214-9) — the survey behind §5; read it after [[02-foundations/optimization|4. Optimization §5]]'s example, skimming the formulation and stability sections rather than every proof.
- J. B. Rawlings, D. Q. Mayne, M. M. Diehl, [*Model Predictive Control: Theory, Computation, and Design*](https://sites.engineering.ucsb.edu/~jbraw/mpc/), 2nd ed., Nob Hill, 2017 (free) — the guarantees in the most general setting, read when a paper claims recursive feasibility; §8.8.4 on condensing.
- F. Borrelli, A. Bemporad, M. Morari, [*Predictive Control for Linear and Hybrid Systems*](http://cse.lab.imtlucca.it/~bemporad/publications/papers/BBMbook.pdf), Cambridge University Press, 2017 (free) — the same guarantees for the linear polytopic case of this page (persistent feasibility §12.3.1, stability §12.3.2, Theorem 12.2), and the computational side: explicit MPC, the QP structure of §2, hybrid formulations for §4's contact case.
- D. Axehill, M. Morari, "An alternative use of the Riccati recursion for efficient optimization," *Systems & Control Letters* 61(1), 37–40, 2012 — the $O(N^2)$ condensed factorization of §2's Deeper note.

## 한국어

*[[04-robotics/control-theory-ce397|5]]·[[04-robotics/lqr-lqg|6]]번 위에 서고, [[04-robotics/planning-decision-making|4. 계획 §6]]의 유한 지평 문제를 피드백으로 바꾼다. D군이다. 입력·상태 제약을 태생적으로 다루는 것이 LQR 옆에 존재하는 이유이고,
[[04-robotics/convex-mpc-legged|8. Convex MPC]]가 이것을 보행 로봇의 표준으로 만든 응용이다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[physical-ai-map|피지컬 AI 지도]]에서 [[07-research-program/index|7. 연구 프로그램 §5]]의 로봇 스택 옆 제어 열에 놓이고, "*저 패널을 프레임에 설치해*"에서는 하드웨어와 현장이 거는 한계 — 액추에이터의 힘, 관절 범위, 장애물로서의 패널 — 안에서 *부재를 옮기는* 단계를 받친다. 그 한계를 모른 채 설계한 이득은 하드웨어가 해 줄 수 없는 움직임을 약속한다. [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]의 손으로 고른 이득 $K=99$는 카탈로그의 새는 히터 P4([[02-foundations/lab-plants|0.6]])에게 $x=0.5$에서 레일 $|u|\le1$을 넘는 $u=-49.5$를 요구하고, 카탈로그의 $0.1$ s로 샘플하면 안정하지도 않다. 반면 레일을 알고 계획하는 MPC는 같은 시계에서 안정하게 남고, 무엇을 포기하는지도 정확히 보여 준다 — 모델이 빠뜨린 외란에서 오는 오프셋 $0.154$('대상으로 한 번 끝까지'). [[04-robotics/convex-mpc-legged|8. Convex MPC §2]]는 같은 종류의 QP를 접촉력 위에서 수십 Hz로 풀고, [[02-foundations/rl-robot-learning|7.5 RL §4]]는 학습된 정책을 감싸는 흔한 안전 필터로 MPC를 꼽으며, [[03-deep-learning/vla/index|딥러닝 4. VLA §3]]은 정책의 행동 청크를 일부를 개루프로 실행하는 후퇴 지평 계획으로 읽는다. [[05-construction-robotics/imitating-contact|건설 10 §4]]가 패널 앞에서 마주하는 맞거래가 그것이다. 이 페이지는 학위논문 경로의 블록 2, 로보틱스 77–78회차이고([[07-research-program/index|7 §8]]), 이 연결들은 블록 4와 7로 이어진다. 이 페이지를 마치면 MPC 정식화(비용, 지평, 제약, 종단 재료)를 읽고, 매 스텝 온라인으로 무엇이 풀리는지 말하고, 논문의 실행 가능성(feasibility)·안정성·풀이 시간 주장을 확인할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분 회차 둘, 로보틱스 77–78회차다. **1회차(77):** 아래 정의, 이 페이지의 대상, 그림, 그리고 계산기를 곁에 둔 '대상으로 한 번 끝까지' — 1–4단계는 손으로, 5–6단계는 읽기 — 다음 §1과 §3. 페이지를 가린 채 2단계를 다시 풀고(예측 상태 셋, 그리고 마지막 입력까지 레일에 남는 이유) 5단계의 오프셋과 그것을 없애는 방법을 말하며 마친 뒤, 논문의 MPC 절에서 §3의 실패 모드 두 개를 찾는다. **2회차(78):** §2(더 깊이 노트는 선택), §4, 그리고 §5 — Mayne의 두 조건을 이산 적분기 위에서 수직선 그림과 함께 손으로 확인 — 다음 스스로 점검과 과제. 레일을 절반으로 줄인 종단 집합과 실행 가능 집합, 곧 과제 2(d)로 마친다. Literacy 통과는 1회차에서 멈춘다.

**무엇인가**: **모델 예측 제어**는 매 제어 주기마다 현재 상태에서 유한 지평 최적 제어
문제를 풀고, 첫 입력만 적용한 뒤, 다음 주기에 다시 푼다(**후퇴 지평**, receding horizon). 식으로 쓰면, 시각 $t$에서
측정한(또는 추정한) 상태 $x(t)$로부터 다음을 푼다.

$$\min_{u_0,\ldots,u_{N-1}} \sum_{k=0}^{N-1} \ell(x_k, u_k) + V_f(x_N) \quad \text{s.t.} \quad x_{k+1} = f(x_k, u_k),\;\; x_k \in \mathcal X,\;\; u_k \in \mathcal U,\;\; x_N \in \mathcal X_f,\;\; x_0 = x(t)$$

그리고 $u(t) = u_0^\star$를 적용한다. 다음 측정이 오기 전까지 쓰이는 것은 첫 입력뿐이고 문제 전체를
다시 풀기 때문이다. 이름 붙은 구성 요소는 **예측 모델** $f$(선형 MPC에서는 $f(x,u) = Ax + Bu$),
앞을 내다보는 스텝 수인 **지평** $N$, **단계 비용** $\ell$(선형 MPC에서는 $x^\top Q x + u^\top R u$),
$N$스텝 이후 전부를 대신하는 **종단 비용** $V_f$(보통 LQR의 $P$로 $x^\top P x$), 상태와 입력의
**제약 집합** $\mathcal X$와 $\mathcal U$, 그리고 예측이 끝나야 하는 **종단 집합** $\mathcal X_f$다.
이것은 [[04-robotics/planning-decision-making|4. 계획 §6]]의 문제 — 거기의 종단 비용 $\ell_f$가 여기의 $V_f$다 — 를 매 스텝 다시 푸는 것이고, [[02-foundations/optimization|4. 최적화 §5]]는 그 선형-이차 경우를 QP로 적고 이산 적분기의 입력을 $|u|\le0.2$로 묶어 보았다.
*비예:* 이 문제를 한 번 풀고 시퀀스 $u_0, \ldots, u_{N-1}$ 전체를 실행하는 것은 MPC가 아니라 개루프
최적 제어다. 피드백을 공급하는 것은 새 측정에서 다시 푸는 일이다. 선형 동역학,
양의 준정부호 상태·종단 비용, 양의 정부호 입력 비용, 아핀 등식과 선형 부등식 제약이면 볼록
QP가 된다 — [[02-foundations/optimization|4. 최적화 §5]]에 완전히 써 놓았다. 더 일반적인 볼록
제약은 볼록 최적화 문제를 만들 수 있지만 반드시 QP인 것은 아니다. 입력·상태 제약을 *태생적으로* 다루는 것이
[[04-robotics/lqr-lqg|LQR]] 대비 MPC의 존재 이유다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P4**, 카탈로그의 새는 히터 $\dot x=-x+u+d$다(제어되는 이런 시스템을 제어에서는 *장치*(plant)라 부른다). $x$는 온도 오차, $u$는 히터 명령, $d$는 외란이다. $T=0.1$ s마다 입력을 일정하게 붙들면(영차 유지, [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]) 정확히

$$x_{k+1}=a\,x_k+b\,(u_k+d),\qquad a=e^{-T}=0.904837,\qquad b=1-e^{-T}=0.095163$$

이다. $d$가 $u$ 옆으로 들어오므로 같은 인자 $b$를 받기 때문이다 — 0.6의 샘플 모델에 외란을 도로 넣은 것이다. $a+b=1$임을 기억해 두자. 이 페이지에서 히터에는 액추에이터의 한계인 **레일** $|u_k|\le1$이 있고, 계획기가 측정하지 **않는** 일정한 $d=1$이 있다. 곧 예측 모델에는 $d$가 없다. 그 위에서 도는 MPC는 이렇게 고정한다.

| 기호 | 값 | 뜻 |
|---|---|---|
| 모델 | $x_{k+1}=0.904837\,x_k+0.095163\,u_k$ | 계획기의 예측, $d$는 빠져 있다 |
| $N$ | $3$ | 지평: 세 스텝, $0.3$ s |
| $\ell(x,u)$ | $100x^2+u^2$ | 단계 비용: 오차에 $q=100$, 명령에 $r=1$ |
| $V_f(x)$ | $152.43\,x^2$ | 종단 비용, 이 $q,r$에 대한 이산 리카티 해('대상으로 한 번 끝까지' 1단계) |
| $\mathcal U$ | $\lvert u\rvert\le1$ | 레일. 과제 전까지 상태 제약은 없다 |
| $x(t)$ | $0.5$ | '대상으로 한 번 끝까지'가 출발하는 측정 상태 |

비 $q/r=100$은 아무렇게나 고른 값이 아니다. '대상으로 한 번 끝까지'의 두 계획이 모두 세 입력을 레일에 붙이게 만드는 값이다($r=1$이면 $q$가 $88$을 넘어야 한다. $q=1$이면 $0.5$에서의 계획이 $(-0.19,-0.17,-0.15)$로 레일 한참 안쪽이다).

*범위: 이 페이지는 선형 MPC를 읽기 수준으로 가르친다 — 온라인으로 푸는 문제(정의, '대상으로 한 번 끝까지'), 그것이 볼록 QP가 되는 때(§1), 두 솔버 형태(§2), 하드웨어에서 실패하는 방식(§3), 비선형·접촉 MPC가 갈라지는 곳(§4), 실행 가능성과 안정성에 대한 Mayne의 조건(§5). 솔버 내부, explicit MPC, robust(tube) MPC와 offset-free MPC 전체는 가르치지 않는다. 그것들은 출처의 책들에 있고, offset-free MPC가 필요로 하는 추정기는 [[04-robotics/state-estimation-slam|3. 상태 추정 §5]]의 것이다. 처음부터 끝까지 계산한 응용 하나는 [[04-robotics/convex-mpc-legged|8. Convex MPC]]다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 380" style="max-width:100%;height:auto" role="img" aria-label="x(t) = 0.5인 새는 히터 P4 위의 길이 3 후퇴 지평, 단계 비용 100x² + u²과 종단 비용 152.4x²: 시간 축 위의 예측 상태 0.357, 0.228, 0.111, -1과 +1 사이 띠 안에서 레일 u = -1에 붙은 계획 입력 셋, 그 한참 아래의 K = 99 요구값 -49.5, 측정되지 않은 채 장치로 들어가는 d = 1, 예측보다 위에 찍힌 새 측정값 0.452와 거기서 다시 세운 지평; 오른쪽은 레일이 허용하는 정상상태 0에서 2까지, 이 MPC가 자리 잡는 0.154의 표시와, 샘플하면 불안정해지는 K = 99의 목표 0.01.">
  <defs><marker id="aMPCk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <rect x="20" y="26" width="128" height="46" rx="3"/>
    <circle cx="206" cy="47" r="10"/>
    <rect x="252" y="30" width="150" height="34" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" marker-end="url(#aMPCk)">
    <line x1="148" y1="47" x2="194" y2="47"/>
    <line x1="206" y1="12" x2="206" y2="35"/>
    <line x1="216" y1="47" x2="250" y2="47"/>
    <polyline points="402,47 470,47 470,84 84,84 84,74"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="56" y1="210" x2="268" y2="210"/>
    <line x1="64" y1="206" x2="64" y2="214"/>
    <line x1="128" y1="206" x2="128" y2="214"/>
    <line x1="192" y1="206" x2="192" y2="214"/>
    <line x1="256" y1="206" x2="256" y2="214"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.45">
    <line x1="268" y1="210" x2="328" y2="210"/>
    <line x1="320" y1="206" x2="320" y2="214"/>
    <line x1="64" y1="200" x2="320" y2="200" stroke-dasharray="1 3"/>
  </g>
  <rect x="64" y="238" width="192" height="50" fill="currentColor" fill-opacity="0.10"/>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.7">
    <line x1="64" y1="238" x2="256" y2="238"/>
    <line x1="64" y1="288" x2="256" y2="288"/>
    <line x1="64" y1="263" x2="256" y2="263" stroke-dasharray="1 3"/>
  </g>
  <rect x="78" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="142" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <rect x="206" y="263" width="36" height="25" fill="currentColor" fill-opacity="0.55"/>
  <ellipse cx="96" cy="275.5" rx="27" ry="16" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.5" fill="none">
    <line x1="96" y1="291" x2="96" y2="302"/>
    <path d="M90 305 L102 301 M90 310 L102 306"/>
    <line x1="96" y1="309" x2="96" y2="356" marker-end="url(#aMPCk)"/>
  </g>
  <polyline points="64,105 128,132.1 192,156.7 256,178.9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="128,114 192,140.3 256,164.1 320,185.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" stroke-opacity="0.45"/>
  <circle cx="64" cy="105" r="4" fill="currentColor"/>
  <circle cx="128" cy="132.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="156.7" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="256" cy="178.9" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="192" cy="140.3" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="256" cy="164.1" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="320" cy="185.6" r="3.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.45"/>
  <circle cx="128" cy="114" r="4" fill="currentColor"/>
  <path d="M134 114 H137 V132.1 H134" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <line x1="137" y1="123.1" x2="196" y2="112" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <rect x="330" y="284" width="200" height="16" fill="currentColor" fill-opacity="0.22"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="318" y1="292" x2="544" y2="292"/>
    <line x1="330" y1="281" x2="330" y2="303"/>
    <line x1="430" y1="281" x2="430" y2="303"/>
    <line x1="530" y1="281" x2="530" y2="303"/>
  </g>
  <path d="M345.4 302 l-5 9 h10 z" fill="currentColor"/>
  <path d="M324 322 l-4.5 8 h9 z" fill="currentColor"/>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="84" y="40">MPC: N = 3, |u| ≤ 1</text>
    <text x="84" y="54">ℓ = 100x² + u²</text>
    <text x="84" y="67" xml:space="preserve">V<tspan dy="3" font-size="10">f</tspan><tspan dy="-3"> = 152.4x²</tspan></text>
    <text x="327" y="52" font-size="12">ẋ = −x + u + d</text>
    <text x="64" y="226">t</text>
    <text x="128" y="226">t+1</text>
    <text x="192" y="226">t+2</text>
    <text x="256" y="226">t+3</text>
    <text x="320" y="226" opacity="0.5">t+4</text>
    <text x="96" y="255">u<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="160" y="255">u<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="224" y="255">u<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="330" y="276">0</text>
    <text x="430" y="276">1</text>
    <text x="530" y="276">2</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="160" y="41">u<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="214" y="22">d = 1, 측정 안 됨</text>
    <text x="462" y="80" text-anchor="end" opacity="0.85">측정한 x</text>
    <text x="58" y="95">x(t) = 0.5, 측정값</text>
    <text x="200" y="110">t+1의 새 측정값은 예측한 x<tspan dy="3.5">1</tspan><tspan dy="-3.5">보다 위에 있다:</tspan></text>
    <text x="200" y="124">그 간격이 피드백이다 (모델에는 d = 1이 없다)</text>
    <text x="336" y="150" opacity="0.9">파선: 계획, 실행되는 것은 첫 스텝뿐</text>
    <text x="336" y="164" opacity="0.6">옅은 선: 새 x에서 다시 세운 계획</text>
    <text x="58" y="242" text-anchor="end">u = +1</text>
    <text x="58" y="292" text-anchor="end">u = −1</text>
    <text x="58" y="204" text-anchor="end" opacity="0.7">x = 0</text>
    <text x="140" y="306" opacity="0.85">장치에 닿는 것은 u<tspan dy="3.5">0</tspan><tspan dy="-3.5">뿐</tspan></text>
    <text x="108" y="338">K = 99는 u = −Kx = −49.5를 요구</text>
    <text x="108" y="352" opacity="0.85">띠보다 한참 아래 (축척 밖)</text>
    <text x="318" y="248">레일이 허용하는 정상상태</text>
    <text x="318" y="262" xml:space="preserve">0 = −x + u + d ⇒ x<tspan font-size="10" dy="3">ss</tspan><tspan dy="-3"> = u + 1 ∈ [0, 2]</tspan></text>
    <text x="332" y="330">0.154 = d/(1 + 5.51): 이 MPC가</text>
    <text x="318" y="344">자리 잡는 곳, 모델에 d가 없다</text>
    <text x="318" y="360" opacity="0.85">0.01 = d/(1 + 99): K = 99의 목표,</text>
    <text x="318" y="374" opacity="0.85">0.1초 시계에서는 불안정한 이득</text>
    <text x="342" y="226" opacity="0.7">한 스텝 = 0.1초</text>
  </g>
</svg>

측정한 $x(t)=0.5$에서 이 페이지의 대상이 밟는 후퇴 지평 한 스텝이다. 단계 비용 $100x^2+u^2$과 종단 비용 $152.4x^2$ 아래 $N=3$ 계획은 세 입력을 모두 레일 $u=-1$에 붙이고 $0.357$, $0.228$, $0.111$을 예측하는데, 손으로 고른 이득 $K=99$는 $u=-49.5$를 요구한다. 장치에 닿는 것은 동그라미 친 $u_0$뿐이고, 측정되지 않는 $d=1$이 다음 측정값을 $0.452$로 끌어올리며 그 간격이 곧 피드백이다 — 옅은 계획은 거기서 다시 푼 것이다($0.314$, $0.189$, $0.076$). 오른쪽은 레일이 허용하는 정상상태 $x_\mathrm{ss}=u+1\in[0,2]$로, 이 MPC는 $0.154$에 자리 잡고('대상으로 한 번 끝까지' 5단계), $K=99$가 노린 $0.01$에는 $0.1$ s 시계가 불안정하게 만드는 이득이 필요하다(6단계).

### 대상으로 한 번 끝까지 · Worked case

P4 위의 후퇴 지평 한 스텝을, 종단 비용부터 루프가 자리 잡는 곳까지 따라간다. 모든 수는 계산기로 나온다.

**1단계 — 종단 비용.** $V_f$는 3스텝 이후의 미래 전체를 대신하고, 가장 좋은 선형 법칙 아래 그 미래의 비용을 돌려주는 것이 이산 시간 리카티 방정식(DARE)이다([[04-robotics/lqr-lqg|6. LQR / LQG §1.5]]에 이산 적분기의 $P=1.618$이 계산되어 있다). 상태가 하나면

$$P=q+a^2P-\frac{(abP)^2}{r+b^2P}\quad\Longleftrightarrow\quad b^2P^2+\big((1-a^2)\,r-q\,b^2\big)P-q\,r=0$$

이다. $r+b^2P$를 양변에 곱하면 $a^2b^2P^2$ 두 항이 지워지기 때문이다. 수를 넣으면 $0.009056\,P^2-0.7243\,P-100=0$이고 양의 근은 $P=152.43$, 이 해에 딸린 법칙의 이득은 $K=abP/(r+b^2P)=13.125/2.380=5.514$다. (6의 적분기 $a=b=q=r=1$로 확인하면 이차식이 $P^2-P-1=0$이 되어 $P=1.618$이다.) 그러니 $V_f=152.43\,x^2$이고, 루프 $u=-5.514x$는 매 스텝 상태에 $a-bK=0.380$을 곱한다.

**2단계 — $x=0.5$에서의 계획.** 레일이 없다면 답은 그 법칙, $u_0=-5.514\times0.5=-2.76$이고 $|u|\le1$ 밖이다. 그러니 세 입력을 모두 레일에 붙여 본다. 그러면 스텝마다 $a$를 곱하고 $b$를 빼므로 모델은

$$x_1=0.904837\times0.5-0.095163=0.357,\qquad x_2=0.228,\qquad x_3=0.111$$

을 예측한다. 마지막 입력까지 정말 레일에 있을까? $x_2=0.228$에서 종단 법칙은 $-Kx_2=-1.26$을 요구해 여전히 레일 밖이므로 $u_2=-1$이다. 완전한 확인은 상자 제약의 KKT 조건이다([[02-foundations/optimization|4. 최적화 §4]]). 하한에 붙은 입력에서는 비용의 기울기가 양이어야 한다. 입력을 레일에서 떼어 올리면 비용이 커져야 한다는 뜻이다. $J=\sum_{k=0}^{2}(100x_k^2+u_k^2)+152.43\,x_3^2$을 모델을 따라 미분하면 $k=0,1,2$에 대해 $\partial J/\partial u_k=11.37,\ 5.26,\ 1.23$이고 — 마지막은 $2(u_2+bPx_3)=2(-1+1.613)$ — 셋 모두 양이다. 계획은 $u=(-1,-1,-1)$, 예측 비용은 $47.85$다.

**3단계 — 입력 하나를 적용하고 잰다.** 장치에 닿는 것은 $u_0=-1$뿐이고, 장치는 $d=1$도 함께 받으므로 알짜 입력은 $u_0+d=0$이다.

$$x(t+1)=a\,x(t)+b\,(u_0+d)=0.904837\times0.5=0.452$$

예측했던 $0.357$보다 높다. 간격 $0.095=b\,d$는 모델이 빠뜨린 외란의 한 스텝어치이고, 제어기가 $d$에 대해 알게 되는 유일한 길이 이것이다.

**4단계 — 측정값에서 다시 계획한다.** $x=0.452$에서 같은 문제를 풀면 다시 레일이다. 예측은 $0.314$, $0.189$, $0.076$이고, 마지막 입력은 간신히 붙어 있다($-Kx_2=-1.04$, 기울기 $9.04$, $3.59$, $0.20$). 2단계 계획에서 첫 입력 말고는 아무것도 실행되지 않았다. 그것이 후퇴 지평이다.

**5단계 — 루프가 자리 잡는 곳.** 3–4단계를 되풀이하면 레일이 $d$를 정확히 상쇄하므로($u+d=0$) $x$는 힘을 받지 않는 히터처럼 스텝마다 $0.905$배로 줄어든다(시간 상수 $1$ s). 레일 위에서 열한 스텝을 가면 $x=0.166$으로 $1/K=0.181$ 아래가 되고, 계획이 레일을 떠난다. 거기서부터 입력은 LQR 법칙 $u=-5.514x$다 — $V_f$가 정확한 남은 비용이므로 레일을 떠나면 짧은 지평이 아무것도 바꾸지 않는다 — 그리고 $d$가 작용하는 정상상태는 다음을 푼다.

$$x=a\,x+b\,(-Kx+d)\quad\Longrightarrow\quad x_\mathrm{ss}=\frac{d}{1+K}=\frac{1}{6.514}=0.154$$

$1-a=b$이기 때문이다. 루프는 레일 안쪽의 $u=-0.846$으로 $0.154$에 자리 잡는다. 안정하지만 목표를 벗어났고, 계획은 매번 $d$가 되돌려 놓을 하강을 예측한다 — §3의 모델 불일치가 수 하나로 나타난 것이다. 어떤 가중치도 이것을 없애지 못한다. LQR 이득은 늘 데드비트 이득 $a/b=9.51$ 아래에 있으므로 오프셋은 $1/(1+a/b)=b=0.095$ 위에 남는다. 이것을 없애는 것은 적분 동작([[04-robotics/control-theory-ce397|5. 제어 이론 §7]]), 또는 MPC 자신의 말로는 $d$를 모델에 넣고 다른 상태처럼 추정하는 일이다([[04-robotics/state-estimation-slam|3. 상태 추정 §5]]). 이것을 offset-free MPC라 한다. 이 한 상태짜리 장치에서는 열한 스텝이 적용 입력이 정확히 잘라 낸 법칙 $u=\mathrm{sat}(-5.514x)$임도 보여 준다. QP가 자르기보다 더 벌어들이는 것은 계획 앞쪽에 제약이 놓일 때다 — 과제의 상태 한계, 또는 §5의 종단 집합.

**6단계 — $K=99$였다면.** [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]의 손으로 고른 이득 $K=99$는 정상상태 $d/(1+K)=0.01$을 위해 고른 것이고, $x=0.5$에서 $u=-49.5$를 요구한다. 연속 시간에서 레일로 잘라 낸 $u=\mathrm{sat}(-99x)$도 거기에 닿기는 한다. $99x>1$인 동안 레일이 $d$를 상쇄해 $x=0.5\,e^{-t}$가 $t=\ln49.5=3.9$ s에 $1/99=0.0101$에 이르고, 그 뒤 $0.0100$에 자리 잡는다. 레일이 무효로 만드는 것은 정상상태가 아니라 선형 설계가 약속한 과도 — 극점 $-100$, 곧 $10$ ms의 시간 상수 — 이다. 이 페이지의 시계에서는 아예 실패한다. $T=0.1$ s 동안 붙든 $u_k=-Kx_k$는 $x_{k+1}=(0.905-0.095K)\,x_k+0.095\,d$를 주고, 이것은 $K<(1+a)/b=20.02$일 때만 안정하다(명시적 오일러로는 $19$, 5 §4). $K=99$면 배수가 $-8.52$이고, 잘라 낸 루프는 레일을 타고 $3.9$ s 만에 $0.01$까지 내려온 뒤 $0.009$와 $0.017$ 사이를 오가며 끝내 자리 잡지 못한다. MPC의 이득은 샘플한 모델 위의 비용에서 나왔으므로 같은 시계에서 안정하다. $d$를 빠뜨린 대가는 5단계의 오프셋이다.

### 1. QP는 언제 실제로 볼록한가?

"그냥 QP다"라는 주장에는 논문에서 확인할 조건들이 붙어 있다:

- **비용**: $Q \succeq 0$, $R \succ 0$, 종단 $P \succeq 0$ — 이차형식이 (준)정부호여야
  한다 ([[02-foundations/linear-algebra|1. 선형대수 §3]]). (학습된 비용 등에서 나온)
  부정부호 $Q$는 볼록성을 조용히 깨뜨린다.
- **동역학**: 선형(또는 선형화 — 이 경우 QP는 선형화 지점에서 멀어질수록 품질이 떨어지는
  근사일 뿐이다).
- **제약**: 입력/상태 집합이 볼록해야 한다(박스, 폴리토프). **장애물 회피 제약은
  비볼록이다** — 충돌 인지 MPC 논문들이 국소 볼록화(안전 통로)를 하거나 아예 QP 세계를
  떠나는 이유다. 집합은 그 안의 두 점을 잇는 선분이 집합 안에 머물 때 볼록하다(정의와 볼록 문제의
  조건은 [[02-foundations/optimization|4. 최적화 §2]]). 원점에 있는 반지름 1 장애물 바깥의 자유 공간
  $\lVert p\rVert \ge 1$은 $(-1.5, 0)$과 $(1.5, 0)$을 담지만 그 중점 $(0, 0)$은 담지 않으므로 이 검사에
  실패한다.

**수 하나로 해 보는 검사.** [[04-robotics/planning-decision-making|4. 계획 §6]]이 손으로 비용을 매긴 적분기 — $x_{t+1}=x_t+u_t$, $x_0=1$, $N=2$, $\ell=x^2+u^2$, 종단 비용 $x_2^2$ — 에 $x_1=1+u_0$과 $x_2=1+u_0+u_1$을 대입해 condensed 형태로 만든다.

$$J(u_0,u_1)=1+u_0^2+(1+u_0)^2+u_1^2+(1+u_0+u_1)^2,\qquad H=\begin{pmatrix}6&2\\2&4\end{pmatrix}$$

여기서 $H$는 헤시안, 곧 $J$의 2계 도함수 행렬이다. 고윳값 $5\pm\sqrt5=7.24$와 $2.76$이 양수이므로 $J$는 엄격히 볼록한 그릇이고, 하나뿐인 정류점 $u=(-0.6,-0.2)$, $J=1.60$이 전역 최소다 — 4 §6이 비용을 매긴 세 계획($1.75$, $2$, $3$)보다 모두 낮다. *비예:* 학습된 비용이 그럴 수 있듯 $x_1$에 가중치 $q=-3$을 주면 왼쪽 위 성분이 $4+2q=-2$가 되고 $\det H=-12<0$, 곧 안장점이다. QP가 비볼록해지고, 국소 솔버는 최소가 아닌 정류점에서 멈출 수 있다. $Q\succeq0$은 논문이 적을 수 있는 조건이고, 헤시안의 고윳값이 실제 검사다.

### 2. 솔버가 실제로 보는 것

50 Hz라면 풀이 전체가 **20 ms** 안에 끝나야 하고, 거기서 상태 추정이 이미 쓴 시간을 빼야 한다. 문제를 어떻게 적느냐가 그 예산 가운데 솔버가 얼마를 쓰는지를 정한다. 같은 문제를 쓰는 표준적인 두 방식이 있고 — 논문은 독자가 어느 쪽인지 안다고 가정한다 — 둘은 [[04-robotics/planning-decision-making|4. 계획 §6]]의 direct transcription과 direct shooting을 MPC의 이름으로 부른 것이다.

- **Stacked (희소) 형태**, 4 §6의 direct transcription: 모든 상태 $x_{0:N}$과 입력 $u_{0:N-1}$을 변수로 두고 동역학을
  등식 제약으로 추가 — 크지만 *희소·띠 구조*라 내부점 솔버가 활용한다. 비용 행렬이
  대각 블록으로 놓인다.
- **Condensed (축약) 형태**, 그 direct shooting: $x_k = A^k x_0 + \sum_j A^{k-1-j}Bu_j$로 상태를 소거해
  $u_{0:N-1}$만 남긴다 — 작지만 *조밀*하고, 지평이 길어지며($A$의 거듭제곱, 비용 가중치, 입력 방향) 조건수가
  나빠질 수 있다.

**크기를 재 보자 — 그래야 "크다"와 "작다"가 형용사에서 벗어난다.**
[[04-robotics/convex-mpc-legged|convex MPC 논문]]들이 돌리는 사족보행 centroidal MPC로 예를
들면: 상태 $n_x = 13$(위치, 자세, 그 속도들, 그리고 중력), 입력 $n_u = 12$(발 4개 각각의
3차원 힘), 지평 $N = 10$.

| | 변수 | 등식 제약 | 헤시안 |
|---|---|---|---|
| **Stacked** | $(N{+}1)n_x + Nn_u = 143 + 120 = 263$ | $Nn_x+n_x = 130+13 = 143$ | $263\times263$, **띠 구조** — 대부분 0 |
| **Condensed** | $Nn_u = 120$ | 없음(동역학을 대입해 소거) | $120\times120$, **일반적으로 밀집** — 최대 14,400개 성분 |

Condensed는 변수가 절반 이하라 결정적으로 보이지만, 헤시안이 밀집이라는 점을 보면 달라진다:
조밀하게 저장하면 원소가 $120^2 = 14{,}400$개인 반면 stacked의 비영 성분은 $N$에 대해 선형으로만 늘어난다.
고정 상태·입력 차원에서 지평을 두 배로 하면 stacked 저장량은 대략 두 배가 되고, condensed는 헤시안 *원소 수*가 네 배가 되며, 범용 조밀 Cholesky 분해가 변수 수의 3제곱이므로 그 분해 연산량은 약 여덟 배가 된다 — 이 선택이 취향이 아니라 실제 엔지니어링 결정인 이유다. [[04-robotics/convex-mpc-legged|8. Convex MPC]]의 크기 상자는 같은 condensed QP의 마찰 피라미드 행 $160$개를 센다. 3제곱이 왜 강제되지 않는지, 초기 상태가 stacked의 개수를 어떻게 바꾸는지는 더 깊이 노트에 있다.

> [!note]- 더 깊이 · Deeper
> **3제곱은 조밀 형태가 강제하는 것이 아니다.** Axehill과 Morari(*Systems & Control Letters* 61, 2012, 정리 3)는 Riccati 재귀의 양들로 condensed 헤시안의 Cholesky 인자를 $O(N^2)$에 만들고, 소거한 상태를 다시 변수로 넣으면 고전적인 $O(N)$ Riccati 풀이로 돌아간다고 적는다. Rawlings, Mayne, Diehl §8.8.4도 이런 이차 지평 의존도의 condensing 방법들을 정리한다.
>
> **초기 상태를 명시적으로 센다.** 표에서는 $x_0$도 변수이므로 측정값에 고정하는 $n_x=13$개 등식이 동역학 130개 외에 필요하다. QP를 만들기 전에 측정한 $x_0$를 대입하면 변수 13개와 고정 등식 13개를 함께 뺀다. 같은 문제를 변수 250개, 동역학 등식 130개로 쓸 수 있다. 행렬 크기의 장부가 달라질 뿐 제어 문제는 같다.

읽을 때의 어림 규칙: 긴 지평 + 상태 제약 → stacked; 짧은 지평 + 입력 제약만 → condensed.
($A$의 큰 거듭제곱은 조건수를 나쁘게 만들 수 있다. 안정 동역학은 유리하지만 가중치·제어 가능성·스케일도 중요하므로 그것만으로 좋은 조건수를 보장하지는 않는다. 저장량과 조밀 분해 연산량은 전체 솔버 시간의 보장이 아니다.)

### 3. 논문이 얼버무리는 실패 모드

시뮬레이션에서 잘 도는 MPC가 하드웨어에서 실패하는 길은 예측 가능한 네 가지이고, 논문의 MPC 절은 그중 무엇을 재고 무엇을 가정으로 치우는지 보려고 읽는 것이다.

- **실행 불가능**(infeasibility): 외란이 상태를 *어떤* 입력 시퀀스로도 제약을 만족할 수 없는 곳으로
  밀면 — 솔버는 아무것도 돌려주지 않고, 제어기는 *뭐라도* 해야 한다. 표준 처방:
  **제약 연화**(constraint softening) — 딱딱한 상태 제약을 벌점 붙은 슬랙 변수
  $\sigma \ge 0$(비용 $+\rho\|\sigma\|$)로 바꿔, 연화한 제약을 비용을 치르고 위반하도록 허용한다. 상태 한계 $x_k \le x_{max}$라면
  $$x_k \le x_{max} + \sigma_k, \qquad \sigma_k \ge 0, \qquad \text{cost} = \textstyle\sum_k \ell(x_k, u_k) + V_f(x_N) + \rho \sum_k \sigma_k$$
  이다. 크기 $\sigma_k$의 위반이 허용되지만 $\rho\,\sigma_k$만큼 비용이 붙는다. 이 선형($\ell_1$) 벌점에서 $\rho$가 그 제약의 라그랑주 승수보다 크면, 경성 제약 해가 존재할 때 연화한 문제도 그 해를 돌려준다(*정확한 벌점*). 남은 경성 제약이 충돌하면 여전히 해가 없을 수 있다. 입력(액추에이터) 제약은 경성으로 유지하며, 쓸 수 있는 해가 없을 때의 대체 동작도 정해야 한다.
- **모델 불일치**: MPC는 *모델의* 미래를 최적화한다. 모델과 장치의 편차는 "최적" 계획을
  피드백(재풀이 자체)이 흡수해야 하는 반복적 소오차로 바꾸고, 재풀이는 그것을 일부만 흡수한다 — '대상으로 한 번 끝까지'에서 모델에 없는 $d=1$은 계획이 매번 하강을 예측하는 동안 P4를 $0.154$에 영영 붙들어 두고(5단계), 편차를 상태로 추정하면 그것이 사라진다. 이를 정량화하는 논문과 가정으로 치우는 논문을 구분하라.
- **지연과 주기**: 계획은 풀이 시간만큼 낡은 상태 추정에서 계산되고([[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]), 오래된 상태에서 세운 더 나은 계획보다 현재 상태의 평범한 계획이 유용할 수 있다. 시간이 실행 부록의 각주가 아니라 문제 구성에 들어가야 하는 이유다. **Warm start** — 이전 해를
  한 스텝 밀어 솔버를 초기화 — 가 고주기 MPC를 가능하게 하는 것이다. 100 Hz의 cold-start
  NMPC는 적신호다.
- **추정기 결합**: MPC는 $x$가 아니라 $\hat{x}$를 소비한다
  ([[04-robotics/state-estimation-slam|3. 상태 추정 §5]]) — 추정기 편향은 계통적 제약 위반이
  된다.

### 4. 선형 vs 비선형 vs 접촉

지금까지는 선형 동역학을 가정했고, 문제를 QP로 만든 것이 바로 그 가정이다. 모델이 비선형이 되거나 접촉이 힘을 켰다 껐다 하면 문제의 부류가 바뀌고 보장도 함께 바뀐다.

- **선형 MPC**: 볼록 QP. *현대 CPU에서 중소 규모 문제라면* 마이크로초~밀리초의 풀이
  시간 — 속도 주장은 항상 문제 크기·솔버·하드웨어를 조건으로 달아 읽어라.
- **비선형 MPC (NMPC)**: SQP(현재 반복점에서 문제의 QP 모델을 풀고, 한 스텝 가고, 반복한다, [[02-foundations/optimization|4. 최적화 §4]]) 또는 DDP류 솔버(differential dynamic programming: 현재 궤적 주위에서 LQR 같은 역방향 패스와 순방향 롤아웃을 번갈아 도는 2차 궤적 최적화기). 국소 최적과 초기화 민감성이 돌아온다
  ([[04-robotics/planning-decision-making|4. 계획 §6]]).
- **접촉 내재 MPC**: 접촉 모드 전환이 문제를 비매끄럽게 만든다
  ([[04-robotics/contact-force-tactile|9. 접촉 §1]]).
  [[04-robotics/convex-mpc-legged|보행 convex MPC]]의 트릭은 접촉 스케줄을 *미리 지정*해
  남는 문제를 볼록하게 만드는 것 — 대표적 탈출로로 그 페이지를 읽어라.

**학습과 만나는 지점** (이 위키의 관심사):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]]은 *학습된* 모델과 CEM 솔버(교차 엔트로피 방법: 입력 시퀀스를 표본으로 뽑고, 가장 좋은 몇 개에 가우시안을 다시 맞추기를 되풀이한다)의 MPC이고,
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]의 후퇴 지평 행동
청크는 MPC의 구조를 빌린 것이며, 굴착기의 학습 동역학 MPC는 건설로봇의 활발한 연구
방향이다 ([[05-construction-robotics/earthmoving-heavy-machinery|건설 3. 토공과 중장비]]).

### 5. 계획이 실행 가능하게 남고 루프가 안정한 때

새 상태마다 다시 푼다고 해서 다음 문제에 해가 있다는 보장도, 상태가 원점에 닿는다는 보장도 생기지 않고, 잘 도는 시뮬레이션은 둘 중 어느 것도 증명하지 못한다. 이 분야의 정본인 **Mayne et al. 2000 서베이**가 종단 비용과 종단 집합에 대한 조건 둘로 둘 다를 정리했다:

- **(a) 재귀적 실행 가능성(recursive feasibility).** 지평의 끝이 알려진 국소 제어기 $\kappa_f$(보통 LQR 법칙 $-Kx$) 아래
  *불변*인 **종단 집합** 안에 떨어진다고 하자. 일단 상태가 안에 들어오면 그 제어기가 안에 잡아 둔다는 뜻이다.
  $$x \in \mathcal X_f \implies f\big(x, \kappa_f(x)\big) \in \mathcal X_f, \qquad \mathcal X_f \subseteq \mathcal X, \qquad \kappa_f(x) \in \mathcal U \ \text{ for all } x \in \mathcal X_f$$
  곧 상태가 집합 안에 머물고, 집합이 상태 제약을 지키고, 국소 제어가 입력 제약을 지킨다. 그러면 오늘의 실행 가능한 계획이 내일의 실행 가능한 계획을 함의한다: 첫 스텝을 떼어 내고
  그 제어기 한 스텝을 이어 붙이면 된다. 이것이 MPC 논문들이 이름으로 부르는
  성질, **재귀적 실행 가능성**이다.
- **(b) 비용 감소에서 오는 안정성.** 또 종단 비용이 그 제어기 아래 **최소한 단계 비용만큼**
  감소한다고 하자, 즉 모든 $x \in \mathcal X_f$에서 $u = \kappa_f(x)$일 때
  $V_f(f(x,u)) - V_f(x) \le -\ell(x,u)$. 그러면 최적 비용이 리아푸노프
  함수(폐루프를 따라 계속 줄어드는 양의 "에너지"라서 상태가 원점에 자리 잡을 수밖에 없게
  만드는 함수. 세 정의 조건은 [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]에 있다)가 되고 원점이
  **점근적으로** 안정해진다. 그 흡인 영역은 실행 가능 집합이다. **실행 가능 집합**은 모든 제약을
  만족하는 입력 시퀀스가 하나라도 있는 초기 상태들의 집합이고, **흡인 영역**은 폐루프가 원점으로
  수렴하는 초기 상태들의 집합이다. 그냥 감소하는 것으로는
  부족하고 감소가 단계 비용을 압도해야 하며, 결론은 애초에 실행 가능했던 상태에서만 성립한다.

두 조건 모두 예측 모델에 대한 말이다. (a)의 "내일의 상태"는 계획이 예측한 상태이고, 모델이 빠뜨린 외란은 그 상태를 가져다주지 않는다. 또 (b)의 부등식은 가정 넷 중 하나일 뿐이다. 나머지는 더 깊이 노트에 있다.

> [!note]- 더 깊이 · Deeper
> **작은 글씨.** Borrelli의 정리 12.2는 단계 비용과
> 종단 비용이 연속이고 양정부호일 것, 집합들이 닫혀 있고 원점을 내부에 포함할 것, 종단 집합이
> 상태 제약 안에서 제어 불변일 것도 함께 요구하고, Rawlings는 단계 비용의 하한과 약한
> 제어가능성을 더한다.
> $Q\succ0$, $R\succ0$인 $\ell=x^\top Qx+u^\top Ru$, LQR에서 온
> $V_f=x^\top Px$, $|u|\le1$ 같은 상자 제약이면 대부분이 저절로 성립한다. 양의 정부호
> 이차식은 연속이고 양의 정부호이며 단계 비용을 아래에서 $\lambda_{\min}(Q)\lVert x\rVert^2$로
> 받치고, 원점을 둘러싼 상자는 닫혀 있고 원점을 내부에 품으며, 원점을 둘러싼 종단 집합과
> 유계인 실행 가능 집합에서 약한 제어가능성도 따라 나온다. 실제 설계 일은 둘이다. 국소 법칙이
> 불변으로 유지하는 종단 집합을 찾는 일 — 아래 스칼라 예제가 손으로 하고, 상태가 몇 개를 넘으면
> 다면체 계산이 된다 — 그리고 $Q$가 준정부호일 뿐일 때는 양의 정부호성이 더는 공짜가 아니므로
> [[04-robotics/lqr-lqg|6. LQR / LQG §2]]처럼 검출 가능성을 확인하는 일이다.

**두 번째 장치로 계산하기 — P4가 아니다.** 이 예제는 히터를 떠나 이산 적분기 $x_{k+1} = x_k + u_k$를
쓴다. 그 LQR 해가 이미 [[04-robotics/lqr-lqg|6. LQR / LQG §1.5]]에서 계산되어 있어 아래 확인이 모두 한 줄 산수가
되기 때문이다. $|u_k| \le 1$, 단계 비용 $\ell = x^2 + u^2$,
그리고 그 이산 LQR 해 $V_f = 1.618\,x^2$, $\kappa_f(x) = -0.618\,x$를 쓰자.
- *종단 집합.* $|\kappa_f(x)| \le 1$은 정확히 $|x| \le 1.618$일 때이고 다음 상태 $0.382\,x$도 그 구간에
  머물므로, $\mathcal X_f = [-1.618,\ 1.618]$은 불변이다.
- *비용 감소.* $V_f(0.382x) - V_f(x) = -1.382\,x^2$이고 $\ell(x, \kappa_f(x)) = x^2 + 0.382\,x^2 = 1.382\,x^2$이므로
  조건 (b)가 등호로 성립한다. $V_f$가 정확한 LQR cost-to-go이면 그래야 한다.
- *실행 가능 집합.* 한 스텝에 상태가 최대 $1$만큼 움직이므로 $N = 2$면 실행 가능 집합은
  $|x| \le 2 + 1.618 = 3.618$이다. $x = 4$에서는 해가 없다.
- *한 스텝.* $x = 3$에서 제약 없는 LQR은 $|u| \le 1$을 어기는 $-1.854$를 명령한다. MPC 문제는
  $u_0 = u_1 = -1$을 돌려주고(예측 $x_2 = 1 \in \mathcal X_f$, 비용 $16.62$), 장치는 $-1$을 받으며,
  다음 문제는 $x = 2$에서 시작한다. 한 칸 민 계획 $(-1,\ \kappa_f(1) = -0.618)$은 $0.382 \in \mathcal X_f$에서
  끝나므로 실행 가능하다. (a)가 약속한 그대로다.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="|u| ≤ 1, N = 2인 이산 적분기 x(k+1) = x(k) + u(k)의 수직선: −1.618에서 1.618까지 진하게 칠한 종단 집합, −3.618에서 3.618까지 옅게 칠한 실행 가능 집합, 계획이 없어 ×로 지운 x = 4; 축 위에는 x = 3에서 u = −1을 두 번 써 2와 1로 건너가는 비용 16.62의 계획, 축 아래 파선은 2에서 u = −1과 −0.618로 1과 0.382로 건너가는 한 칸 민 계획.">
  <defs><marker id="mayAk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="62.9" y="116" width="434.2" height="24" fill="currentColor" fill-opacity="0.10"/>
  <rect x="182.9" y="116" width="194.2" height="24" fill="currentColor" fill-opacity="0.28"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none">
    <line x1="22.0" y1="140" x2="544.0" y2="140"/>
    <line x1="40.0" y1="136" x2="40.0" y2="144"/>
    <line x1="100.0" y1="136" x2="100.0" y2="144"/>
    <line x1="160.0" y1="136" x2="160.0" y2="144"/>
    <line x1="220.0" y1="136" x2="220.0" y2="144"/>
    <line x1="280.0" y1="136" x2="280.0" y2="144"/>
    <line x1="340.0" y1="136" x2="340.0" y2="144"/>
    <line x1="400.0" y1="136" x2="400.0" y2="144"/>
    <line x1="460.0" y1="136" x2="460.0" y2="144"/>
    <line x1="520.0" y1="136" x2="520.0" y2="144"/>
  </g>
  <path d="M515.0 135 L525.0 145 M515.0 145 L525.0 135" stroke="currentColor" stroke-width="2" fill="none"/>
  <path d="M458.0 134 Q430.0 88 403.0 134" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#mayAk)"/>
  <path d="M398.0 134 Q370.0 88 343.0 134" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#mayAk)"/>
  <path d="M398.0 146 Q370.0 180 343.0 146" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#mayAk)"/>
  <path d="M338.0 146 Q321.5 180 305.9 146" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#mayAk)"/>
  <circle cx="460.0" cy="140" r="4.2" fill="currentColor"/>
  <circle cx="400.0" cy="140" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="340.0" cy="140" r="3.8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="302.9" cy="140" r="3.2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <g fill="currentColor">
    <text x="280" y="20" text-anchor="middle" font-size="12" xml:space="preserve">x(k+1) = x(k) + u(k),  |u| ≤ 1,  N = 2,  ℓ = x² + u²,  V<tspan dy="3" font-size="10">f</tspan><tspan dy="-3"> = 1.618x²</tspan></text>
    <text x="24" y="46" font-size="11" xml:space="preserve">실선: x = 3에서 2를 거쳐 1로 가는 계획, u = (−1, −1), 비용 16.62</text>
    <text x="24" y="62" font-size="11" opacity="0.85" xml:space="preserve">(LQR 법칙만으로는 −0.618 × 3 = −1.854를 요구해 레일을 벗어난다)</text>
    <text x="430.0" y="106" text-anchor="middle" font-size="11" xml:space="preserve">u<tspan dy="3" font-size="10">0</tspan><tspan dy="-3"> = −1</tspan></text>
    <text x="370.0" y="106" text-anchor="middle" font-size="11" xml:space="preserve">u<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"> = −1</tspan></text>
    <text x="332.0" y="88" text-anchor="end" font-size="11" xml:space="preserve">x<tspan dy="3" font-size="10">2</tspan><tspan dy="-3"> = 1 ∈ X</tspan><tspan dy="3" font-size="10">f</tspan></text>
    <text x="552" y="162" text-anchor="end" font-size="11">x = 4: 계획 없음</text>
    <text x="40.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−4</text>
    <text x="100.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−3</text>
    <text x="160.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−2</text>
    <text x="220.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">−1</text>
    <text x="280.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">0</text>
    <text x="460.0" y="157" text-anchor="middle" font-size="10" opacity="0.8">3</text>
    <text x="370.0" y="182" text-anchor="middle" font-size="11">−1</text>
    <text x="321.5" y="182" text-anchor="middle" font-size="11">−0.618</text>
    <text x="302.9" y="130" text-anchor="middle" font-size="10">0.382</text>
    <text x="24" y="204" font-size="11" xml:space="preserve">파선: u₀ 실행 뒤 2에서 다시 세운 한 칸 민 계획 (−1, κ<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">(1) = −0.618), 0.382 ∈ </tspan>X<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">에서 끝난다</tspan></text>
    <text x="24" y="222" font-size="11" xml:space="preserve">진한 띠: 종단 집합 X<tspan dy="3" font-size="10">f</tspan><tspan dy="-3"> = [−1.618, 1.618], </tspan>κ<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">(x) = −0.618x가 |u| ≤ 1을 지키는 곳</tspan></text>
    <text x="24" y="240" font-size="11" xml:space="preserve">옅은 띠: 실행 가능 집합, |x| ≤ 2 + 1.618 = 3.618, 크기 1 이하의 두 걸음으로 X<tspan dy="3" font-size="10">f</tspan><tspan dy="-3">에 닿는 곳</tspan></text>
  </g>
</svg>

위 예제를 수직선 하나에 그렸다. 종단 집합 $[-1.618,1.618]$(진한 띠)을 실행 가능 집합 $|x|\le3.618$(옅은 띠)이 품고, $x=4$는 둘 다의 밖이다. 축 위는 비용 $16.62$의 계획 $3\to2\to1$, 축 아래는 (a)가 보장하는 한 칸 민 계획 $2\to1\to0.382$다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 후퇴 지평 절차(풀고 → 첫 입력만 적용하고 → 다시 푼다)를 말하고, P4 위에서 한 스텝을 손으로 밟을 수 있다
- [ ] 볼록 QP의 조건($Q,R,P$의 정부호성과 아핀·다면체 제약)과 일반 볼록 최적화의 차이, 장애물 제약이 볼록성을 깨뜨리는 지점을 말할 수 있다
- [ ] stacked/condensed 정식화의 트레이드오프와 실행 불가능·연화·warm start를 설명할 수 있다
- [ ] 모델이 외란을 빠뜨린 MPC가 왜 목표를 벗어나 자리 잡는지, 무엇이 그 오프셋을 없애는지 말할 수 있다
- [ ] Mayne 2000의 안정성 재료(종단 비용·종단 집합·지평)와 PlaNet·Diffusion Policy가 MPC 구조를 빌린 지점을 말할 수 있다

### 스스로 점검 · Self-check

1. 학습된 비용 행렬 $Q$를 MPC에 꽂았더니 솔버가 이상하게 군다. 가장 먼저 확인할 것은?
2. 지평 $N=50$, 상태 제약이 많은 문제 — stacked와 condensed 중 무엇을 기대해야 하나? 왜?
3. 외란으로 상태가 제약 밖으로 밀렸다. 하드 제약 MPC와 소프트 제약 MPC는 각각 어떻게 되나?
4. "우리 NMPC는 200 Hz로 돈다"라는 주장에서 확인할 세 가지는?

> [!tip]- 정답 · Answers
> 1. $Q \succeq 0$인지 — 부정부호면 QP가 비볼록해질 수 있고(§1의 안장점) 솔버 거동이 정의되지 않는다.
> 2. Stacked — 구조화된(리카티 또는 희소) 풀이는 $N$에 선형으로 늘지만, condensed 형태의 범용 조밀 분해는 $N^3$(Axehill–Morari를 쓰면 $N^2$)으로 는다. condensed 헤시안은 지평과 무관하게 조밀하고, $A$의 거듭제곱 때문에 조건수가 나빠질 수 있으며, 상태 제약은 stacked에서 희소하게 남는다.
> 3. 하드: 실행 불가능 — 솔버가 쓸 수 있는 명령을 반환하지 않아 별도의 폴백이 필요. 소프트: **남은 하드 제약이 실행 가능할 때** 슬랙으로 벌점 있는 위반 해를 반환할 수 있다. 일부 제약을 연화한다고 제어 지속이 보장되지는 않는다.
> 4. ① warm start 여부 ② 문제 크기(지평·상태 차원)와 솔버 ③ 그 200 Hz가 풀이 시간인지 끝-끝 지연인지 ([[04-robotics/robot-systems-deployment|주파수 ≠ 지연]]).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P4**, 이 페이지의 대상인 MPC($N=3$, $\ell=100x^2+u^2$, $V_f=152.43x^2$, $|u|\le1$, 모델에 $d$ 없음) 그대로이되 이제 외란은 $d=1.5$다. 과제 2(d)는 §5의 이산 적분기로 돌아간다. 시뮬레이터 없음.

1. **그리기.** 측정한 $x(t)=0.5$에서 출발하는 $d=1.5$의 그림: 계획과 그 예측 상태 셋, $K=99$의 요구값, $t+1$의 새 측정값과 거기서 다시 세운 계획, 그리고 오른쪽에는 레일이 이제 허용하는 정상상태와 함께 과제 2(c)의 한계 $x\le0.3$과 $K=99$의 목표를 표시한다.
2. **유도.** (a) $|u|\le1$, $d=1.5$에서 $x_\mathrm{ss}$가 앉을 수 있는 구간은? $K=99$는 어떤 정상상태를 노리고, 그것을 붙들려면 $u$가 얼마여야 하나? 어떤 제어기도 $x$를 $0.5$ 아래로 붙들 수 없음을 보여라. (b) $x=0.5$에서 MPC는 무엇을 계획하고, $t+1$에 무엇을 예측하며, 실제로 무엇이 측정되나? 루프는 어디에 자리 잡나? (c) 예측 상태 $x_1,x_2,x_3$에 상태 한계 $x_k\le0.3$을 더한다. 경성 제약 문제는 측정한 $x$가 얼마 이하일 때 실행 가능하고, 이 루프에서 한 번이라도 실행 가능한가? §3처럼 연화하면 계획마다 예측하는 슬랙은 얼마이고, 장치는 실제로 한계를 얼마나 넘나? (d) 레일을 절반 $|u|\le0.5$로 줄인 §5의 이산 적분기($\ell$, $V_f$, $\kappa_f$, $N=2$는 그대로): 종단 집합, 실행 가능 집합, $x=1.5$에서의 계획과 그 비용, 한 스텝 뒤 한 칸 민 계획, 그리고 $x=2$에서의 판정.
3. **해석.** 2(c)의 경성 제약 MPC를 여전히 $d=1.5$인 채 $x=0.4$에서 출발시킨다. 거기서는 실행 가능하다. 처음 실패하는 것은 언제인가? 그것은 §5의 조건 (a)와 모순되는가? 어느 가정이 깨졌는지, 그리고 논문이 하드웨어에서 재귀적 실행 가능성을 주장하기 전에 무엇을 밝혀야 하는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - $t$부터 $t+3$까지(다시 세운 계획을 위해 $t+4$까지) 눈금이 있는 시간 축. 그 위에 첫 눈금의 채운 점으로 측정값 $x(t)=0.5$, 파선 위의 빈 점으로 예측값 $x_1,x_2,x_3=0.357,\ 0.228,\ 0.111$을 찍는다 — 계획기의 모델에 $d$가 없으니 계획기가 푸는 문제는 강의의 것과 같다.
> - 축 아래는 입력: $u=-1$과 $u=+1$ 사이를 칠하고 양쪽 가장자리에 값을 적은 띠, 레일에 붙은 막대로 그린 계획 입력 셋, 그리고 장치에 닿는 유일한 입력 $u_0$에 친 동그라미.
> - $K=99$의 요구값을 띠 밖으로 나가는 화살표로: $x=0.5$에서 $u=-49.5$. 이득이 $d$에 의존하지 않으므로 그대로다.
> - 제어기를 거치지 않고 장치 상자 앞 합산점으로 바로 들어가는 별도 화살표 위의 $d=1.5$.
> - $t+1$의 새 측정값: 강의의 $0.452$가 아니라 $x(t)$와 같은 높이의 $0.500$. 예측한 $0.357$과의 간격은 $0.143=b\,d$다. 옅은 선으로 그린 다시 세운 계획은 $0.500$에서 출발해 첫 계획을 한 눈금 오른쪽에 되풀이한다.
> - 옆에 짧은 $x$축을 그리고 레일이 허용하는 정상상태 $[0.5,\ 2.5]$를 칠한 뒤, 한계 $x\le0.3$과 $K=99$의 목표 $0.015$를 둘 다 칠한 구간 *밖에* 표시한다.
> - 새 측정값이 예측한 $x_1$ 위에 겹치는 순간 그림은 틀렸다. 그것은 이 페이지 첫머리의 비예인 개루프다. 여기서는 측정 상태가 내려가게 그려도 틀렸다. $d=1.5$에서 루프는 $0.5$를 떠나지 않는다.

> [!tip]- 정답 · Solutions
> 1. 체크리스트대로다. 계획은 강의의 것이지만 측정값이 $0.500$으로 돌아오므로 옅은 계획은 첫 계획을 한 눈금 민 사본이다. 루프는 레일에 묶여 오지 않을 하강을 예측하고, 칠한 정상상태는 $0.5$에서 시작하며 $0.3$과 $0.015$는 둘 다 그 왼쪽에 놓인다.
> 2. (a) $0=-x+u+d$에서 $x_\mathrm{ss}=u+1.5\in[0.5,\ 2.5]$. $K=99$는 $d/(1+K)=0.015$를 노리고, 그것을 붙들려면 $u=-99\times0.015=-1.485$가 필요해 레일 밖이다. 어떤 $x$든 붙들려면 $u=x-1.5$여야 하고 $u\ge-1$이 $x\ge0.5$를 강제한다 — 제어기가 무엇이든 5. 제어 이론 §9의 포화 정상상태 $x=d-1$이다. (b) 계획기가 푸는 문제는 강의의 것이므로 계획은 $(-1,-1,-1)$이고 $0.357$을 예측한다. 장치는 $u+d=0.5$를 받고 $x=0.904837\times0.5+0.095163\times0.5=0.500$을 돌려준다. $a+b=1$이기 때문이다. 측정값이 이전 상태와 같으니 루프는 $u=-1$로 $0.5$에 영영 머물고 계획은 매번 같다. (c) 모델이 한 스텝에 할 수 있는 최선은 $x_1=ax-b$이므로 $x_1\le0.3$은 $x\le(0.3+b)/a=0.437$을 요구한다. 장치는 $0.5$ 아래로 내려가지 않으므로 경성 문제는 매 틱 실행 불가능하다. 연화하면 계획은 $(-1,-1,-1)$ 그대로이고 — $u_0$가 이미 레일에 있다 — $x_1$에 예측 슬랙 $0.357-0.3=0.057$, $x_2$와 $x_3$($0.228$, $0.111$)에는 슬랙이 없다. 그동안 장치는 매 틱 한계보다 $0.2$ 위인 $0.5$에 머문다. 계획기는 자기가 모델에 넣지 않은 바로 그 $b\,d$만큼 자기 위반을 과소평가한다. (d) $|\kappa_f(x)|=0.618|x|\le0.5$에서 $\mathcal X_f=[-0.809,\ 0.809]$이고, $0.382x$가 안에 머물므로 불변이며, 레일이 들어가지 않으므로 (b)는 여전히 등호로 성립한다. 한 스텝에 $x$는 최대 $0.5$ 움직이므로 실행 가능 집합은 $|x|\le1+0.809=1.809$다. $x=1.5$에서 LQR만으로는 $-0.927$을 요구하고, 계획은 $(-0.5,-0.5)$로 $1.0$을 거쳐 $0.5\in\mathcal X_f$에 가며 비용은 $2.25+0.25+1+0.25+1.618\times0.25=4.15$다 — 레일에서의 두 기울기가 모두 양이다, $\partial J/\partial u_0=-1+2+1.618=2.618$, $\partial J/\partial u_1=-1+1.618=0.618$. 한 스텝 뒤 $1.0$에서의 한 칸 민 계획 $(-0.5,\ \kappa_f(0.5)=-0.309)$는 $0.191\in\mathcal X_f$에서 끝난다. $x=2$에서는 두 걸음으로 가 봐야 $1.0$이라 $\mathcal X_f$ 밖이다. 계획이 없다. 모든 경계가 레일에 비례하므로 레일을 절반으로 하면 두 집합도 절반이 된다.
> 3. 모델은 $0.4$에서 $x_1=0.267$을 예측하지만 장치는 $0.410$을 돌려주고, 다음 측정값은 $0.418$, $0.426$, $0.433$, 그리고 $0.437$을 넘는 $0.439$이므로 $t=0.5$ s의 여섯 번째 풀이가 실행 불가능하다. (a)와 모순되지는 않는다. (a)는 계획이 *예측한* 상태에서 실행 가능한 계획을 약속하는데, 모델에 없는 $d$가 장치를 매 스텝 $b\,d=0.143$만큼 더 높이 올려놓는다(게다가 이 MPC에는 종단 집합도 없어 (a)의 가정은 처음부터 채워지지 않았다). 과제 2(a)에서 보았듯 $d=1.5$ 아래에서는 어떤 입력도 $x\le0.3$을 지켜 주지 못하므로, 실행 가능했던 다섯 번의 풀이는 장치가 지킬 수 없는 약속이었다. 하드웨어에서 재귀적 실행 가능성을 주장하기 전에 논문은 제약을 어떤 외란에 맞춰 설계했는지 — robust(tube) MPC처럼 최악의 표류만큼 조이거나, $d$를 추정하거나 — 밝히고, 조인 문제가 여전히 실행 가능함을 보여야 한다.

### 출처

- D. Q. Mayne, J. B. Rawlings, C. V. Rao, P. O. M. Scokaert, "Constrained model predictive control: Stability and optimality," *Automatica* 36(6), 789–814, 2000 · [DOI](https://doi.org/10.1016/S0005-1098(99)00214-9) — §5의 바탕인 서베이. [[02-foundations/optimization|4. 최적화 §5]]의 예제를 본 뒤 읽되, 모든 증명보다 정식화와 안정성 절을 훑는다.
- J. B. Rawlings, D. Q. Mayne, M. M. Diehl, [*Model Predictive Control: Theory, Computation, and Design*](https://sites.engineering.ucsb.edu/~jbraw/mpc/), 2판, Nob Hill, 2017(무료) — 가장 일반적인 설정의 보장. 논문이 재귀적 실행 가능성을 주장할 때 읽는다. §8.8.4가 condensing을 다룬다.
- F. Borrelli, A. Bemporad, M. Morari, [*Predictive Control for Linear and Hybrid Systems*](http://cse.lab.imtlucca.it/~bemporad/publications/papers/BBMbook.pdf), Cambridge University Press, 2017(무료) — 이 페이지의 선형 폴리토프 경우에 대한 같은 보장(지속 실행 가능성 §12.3.1, 안정성 §12.3.2, 정리 12.2)과 계산 쪽: explicit MPC, §2의 QP 구조, §4의 접촉 사례를 위한 하이브리드 정식화.
- D. Axehill, M. Morari, "An alternative use of the Riccati recursion for efficient optimization," *Systems & Control Letters* 61(1), 37–40, 2012 — §2 더 깊이 노트의 $O(N^2)$ condensed 분해.
