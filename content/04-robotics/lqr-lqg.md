---
title: "6. LQR / LQG"
tags: [robotics, control]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Study links** — [Underactuated Robotics, LQR chapter (Tedrake, MIT)](https://underactuated.csail.mit.edu/lqr.html) · [Stanford EE363 lecture notes (Boyd)](https://web.stanford.edu/class/ee363/)

## English

*Group D. Stands on [[04-robotics/control-theory-ce397|5. Control Theory]] plus probability and optimization. Instead of placing poles by hand you
let a cost place them, and the separation principle says when estimator and controller may be designed apart.*

> [!info] Depth target · 깊이 목표
> State the LQR problem, the role of the Riccati equation, the conditions under which the solution exists and stabilizes, and LQG's estimator–controller separation with its caveat. Deriving or implementing Riccati solvers is optional.
> LQR 문제, 리카티 방정식의 역할, 해가 존재하고 안정화하는 조건, LQG의 추정기–제어기 분리와 그 단서를 말할 수 있으면 된다. 리카티 해법의 유도·구현은 선택이다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/control-theory-ce397|5. Control Theory]] (state space, eigenvalue stability, controllability/observability, pole placement — this page is *"choose $K$ by optimization instead of by hand"*) · [[02-foundations/optimization|4. Optimization]] (quadratic objectives) · [[02-foundations/probability|3. Probability]] (the Kalman filter, for the LQG half)
> [[04-robotics/control-theory-ce397|5. 제어 이론]] (상태공간, 고유값 안정성, 가제어성/가관측성, 극점 배치 — 이 페이지는 *"$K$를 손이 아니라 최적화로 고르기"*다) · [[02-foundations/optimization|4. 최적화]] (이차 목적함수) · [[02-foundations/probability|3. 확률]] (LQG 절반을 위한 칼만 필터)

**What it is**: the **Linear Quadratic Regulator** is the exactly-solvable heart of optimal
control. For linear dynamics $\dot x = Ax + Bu$ and quadratic cost
$\int (x^\top Q x + u^\top R u)\,dt$, the optimal controller is a constant linear feedback
$u = -Kx$, with $K = R^{-1}B^\top P$ where $P$ solves the **algebraic Riccati equation** —
no iteration at runtime.
**LQG** adds Gaussian noise and partial observation: the optimal solution is a
[[02-foundations/probability|Kalman filter]] feeding an LQR (the **separation principle**:
estimate optimally, then control the estimate optimally, and it is jointly optimal).

> [!note] First pass · 처음이라면
> A short page; read it through. If you only have ten minutes, §2 is the one that changes how you read papers — "LQR guarantees stability" has two conditions attached, and papers linearising a nonlinear system inherit them only at the linearisation point.

### 1. The Riccati equation, read structurally

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

(Robotics papers usually use the **discrete-time twin** — the DARE, with gain $K=(R+B^\top P B)^{-1}B^\top P A$ — same structure, same reading.) You never solve this by hand — but reading it structurally pays: $Q$ injects state cost,
the quadratic $-PBR^{-1}B^\top P$ term is *feedback eating cost through control*, and the
stabilizing solution $P \succeq 0$ is what makes $V(x)=x^\top P x$ a Lyapunov function for
the closed loop. When a paper says "we solve a Riccati equation," it means this constant
$P$, computed once offline (or once per linearization in iterative/time-varying LQR).

### 2. When does this actually work? Two conditions

- **Stabilizability** of $(A,B)$: every unstable mode of $A$ must be influenceable by $u$ —
  the exact (necessary and sufficient) condition for a stabilizing feedback to exist,
  weaker than the full controllability rank test in
  [[02-foundations/linear-algebra|page 1's control section]]. Otherwise no feedback can
  stabilize, Riccati or not.
- **Detectability** of $(A,Q^{1/2})$: every unstable mode must show up in the cost —
  otherwise the optimizer can "not care" about a mode that is quietly diverging, and the
  optimal-cost controller is not stabilizing.

These two are the fine print behind "LQR is guaranteed stable." Papers that linearize a
nonlinear system and run LQR inherit both conditions *at the linearization point only*.

### 3. What Q and R do to behavior — a worked reading

Double integrator (cart): $x = (p, v)$, $u$ = force, so
$A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$, $B = \begin{pmatrix}0\\1\end{pmatrix}$.
Choose $Q = \mathrm{diag}(q, 0)$ and $R = r$.

**This one you can actually solve by hand**, and the answer teaches more than any solver
output. Write $P = \begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$ and substitute
into the Riccati equation. Its three distinct entries give three scalar equations:

$$q - \frac{p_{12}^2}{r} = 0, \qquad p_{11} - \frac{p_{12}p_{22}}{r} = 0, \qquad 2p_{12} - \frac{p_{22}^2}{r} = 0$$

Solve in that order: $p_{12} = \sqrt{qr}$, then $p_{22} = \sqrt{2r\sqrt{qr}}$, then $p_{11}$
follows. The gain $K = R^{-1}B^\top P$ is the bottom row of $P$ divided by $r$:

$$k_1 = \sqrt{\rho}, \qquad k_2 = \sqrt{2}\,\rho^{1/4}, \qquad \text{where } \rho = q/r$$

Now read what that says — three separate facts fall out at once.

| $q$ | $r$ | $\rho = q/r$ | $K = (k_1, k_2)$ | $\omega_n$ | $\zeta$ | settling $\approx 4/\zeta\omega_n$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7 s |
| 100 | 1 | 100 | $(10.0,\ 4.47)$ | 3.16 | 0.707 | 1.8 s |
| 1 | 100 | 0.01 | $(0.10,\ 0.45)$ | 0.32 | 0.707 | 17.9 s |
| 10 | 10 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7 s |

- **Only the ratio matters.** Rows 1 and 4 have identical gains: scaling $Q$ and $R$ together
  multiplies the cost but moves nothing about its argmin. This is why papers quote $Q/R$
  ratios rather than absolute weights — and it answers self-check 2 before you try it.
- **The damping is not yours to choose.** Every row has $\zeta = 1/\sqrt2 = 0.707$. The
  closed-loop characteristic polynomial is
  $\lambda^2 + \sqrt2\rho^{1/4}\lambda + \sqrt\rho$, so $\omega_n = \rho^{1/4}$ and
  $2\zeta\omega_n = \sqrt2\rho^{1/4}$ force $\zeta = 0.707$ for *any* weights. LQR on a
  double integrator always lands on the textbook-optimal damping: the weights buy speed, not
  shape. That is the general claim "LQR picks the poles by optimization instead of by hand"
  made concrete — [[04-robotics/control-theory-ce397|control theory §7]] placed poles at
  $\zeta = 0.7$ by hand, and LQR arrived at essentially the same place without being told.
- **Speed is a fourth root, which is brutal.** $\omega_n = \rho^{1/4}$ means doubling the
  controller's bandwidth costs a **16×** increase in $q/r$; ten times faster costs $10^4$.
  When an experimental section says "we raised the state weight by two orders of magnitude",
  that bought a factor of $\sqrt{10} \approx 3.2$ in bandwidth — and, because
  $k_1 = \sqrt\rho$ grew 10×, roughly 10× the commanded force and 10× the amplified sensor
  noise along with it.

The qualitative vocabulary experimental sections use maps onto exactly this arithmetic:

- **Large $q/r$** ("state expensive, control cheap"): aggressive gains — fast recovery, large
  force spikes, more noise amplification, actuator saturation risk (which LQR itself does not
  model — that is [[04-robotics/mpc|MPC]]'s job).
- **Small $q/r$** ("control expensive"): gentle gains, slow recovery, smooth inputs.
- Weights on velocity vs position shape *damping* vs *stiffness* of the response — the knob
  vocabulary behind "we tuned Q/R for a settling time of…".

<svg viewBox="0 0 440 206" style="max-width:100%;height:auto" role="img" aria-label="LQR step responses at three Q/R ratios, all with the same damping">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="40" y1="50" x2="410" y2="50" stroke-dasharray="4 4"/><line x1="40" y1="140" x2="410" y2="140"/><line x1="40" y1="20" x2="40" y2="140"/></g>
  <path d="M40.0 140.0L42.6 132.6L45.1 116.5L47.7 98.1L50.3 81.3L52.9 67.7L55.4 58.0L58.0 51.6L60.6 48.0L63.1 46.4L65.7 46.1L68.3 46.5L70.9 47.3L73.4 48.0L76.0 48.8L78.6 49.3L81.1 49.7L83.7 50.0L86.3 50.1L88.9 50.2L91.4 50.2L94.0 50.1L96.6 50.1L99.1 50.1L101.7 50.0L104.3 50.0L106.9 50.0L109.4 50.0L112.0 50.0L114.6 50.0L117.1 50.0L119.7 50.0L122.3 50.0L124.9 50.0L127.4 50.0L130.0 50.0L132.6 50.0L135.1 50.0L137.7 50.0L140.3 50.0L142.9 50.0L145.4 50.0L148.0 50.0L150.6 50.0L153.1 50.0L155.7 50.0L158.3 50.0L160.9 50.0L163.4 50.0L166.0 50.0L168.6 50.0L171.1 50.0L173.7 50.0L176.3 50.0L178.9 50.0L181.4 50.0L184.0 50.0L186.6 50.0L189.1 50.0L191.7 50.0L194.3 50.0L196.9 50.0L199.4 50.0L202.0 50.0L204.6 50.0L207.1 50.0L209.7 50.0L212.3 50.0L214.9 50.0L217.4 50.0L220.0 50.0L222.6 50.0L225.1 50.0L227.7 50.0L230.3 50.0L232.9 50.0L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M40.0 140.0L42.6 139.1L45.1 136.8L47.7 133.3L50.3 128.9L52.9 123.8L55.4 118.3L58.0 112.6L60.6 106.7L63.1 100.9L65.7 95.2L68.3 89.7L70.9 84.5L73.4 79.6L76.0 75.0L78.6 70.8L81.1 67.0L83.7 63.6L86.3 60.6L88.9 57.9L91.4 55.6L94.0 53.6L96.6 51.8L99.1 50.4L101.7 49.2L104.3 48.3L106.9 47.5L109.4 47.0L112.0 46.6L114.6 46.3L117.1 46.2L119.7 46.1L122.3 46.1L124.9 46.2L127.4 46.4L130.0 46.6L132.6 46.8L135.1 47.0L137.7 47.3L140.3 47.5L142.9 47.8L145.4 48.0L148.0 48.3L150.6 48.5L153.1 48.7L155.7 48.9L158.3 49.1L160.9 49.2L163.4 49.4L166.0 49.5L168.6 49.6L171.1 49.8L173.7 49.8L176.3 49.9L178.9 50.0L181.4 50.0L184.0 50.1L186.6 50.1L189.1 50.1L191.7 50.1L194.3 50.2L196.9 50.2L199.4 50.2L202.0 50.2L204.6 50.2L207.1 50.2L209.7 50.1L212.3 50.1L214.9 50.1L217.4 50.1L220.0 50.1L222.6 50.1L225.1 50.1L227.7 50.1L230.3 50.1L232.9 50.1L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/>
  <path d="M40.0 140.0L42.6 139.9L45.1 139.6L47.7 139.2L50.3 138.7L52.9 137.9L55.4 137.1L58.0 136.1L60.6 135.1L63.1 133.9L65.7 132.6L68.3 131.3L70.9 129.8L73.4 128.3L76.0 126.8L78.6 125.2L81.1 123.5L83.7 121.8L86.3 120.0L88.9 118.3L91.4 116.5L94.0 114.7L96.6 112.8L99.1 111.0L101.7 109.1L104.3 107.3L106.9 105.4L109.4 103.6L112.0 101.7L114.6 99.9L117.1 98.1L119.7 96.3L122.3 94.5L124.9 92.8L127.4 91.0L130.0 89.3L132.6 87.7L135.1 86.0L137.7 84.4L140.3 82.8L142.9 81.3L145.4 79.7L148.0 78.3L150.6 76.8L153.1 75.4L155.7 74.0L158.3 72.7L160.9 71.4L163.4 70.1L166.0 68.9L168.6 67.7L171.1 66.6L173.7 65.5L176.3 64.4L178.9 63.4L181.4 62.4L184.0 61.4L186.6 60.5L189.1 59.6L191.7 58.8L194.3 58.0L196.9 57.2L199.4 56.4L202.0 55.7L204.6 55.1L207.1 54.4L209.7 53.8L212.3 53.2L214.9 52.7L217.4 52.1L220.0 51.6L222.6 51.2L225.1 50.7L227.7 50.3L230.3 49.9L232.9 49.5L235.4 49.2L238.0 48.9L240.6 48.6L243.1 48.3L245.7 48.0L248.3 47.8L250.9 47.6L253.4 47.4L256.0 47.2L258.6 47.0L261.1 46.9L263.7 46.8L266.3 46.6L268.9 46.5L271.4 46.4L274.0 46.4L276.6 46.3L279.1 46.2L281.7 46.2L284.3 46.2L286.9 46.1L289.4 46.1L292.0 46.1L294.6 46.1L297.1 46.1L299.7 46.1L302.3 46.2L304.9 46.2L307.4 46.2L310.0 46.3L312.6 46.3L315.1 46.4L317.7 46.4L320.3 46.5L322.9 46.5L325.4 46.6L328.0 46.7L330.6 46.7L333.1 46.8L335.7 46.9L338.3 46.9L340.9 47.0L343.4 47.1L346.0 47.2L348.6 47.3L351.1 47.3L353.7 47.4L356.3 47.5L358.9 47.6L361.4 47.7L364.0 47.7L366.6 47.8L369.1 47.9L371.7 48.0L374.3 48.0L376.9 48.1L379.4 48.2L382.0 48.3L384.6 48.3L387.1 48.4L389.7 48.5L392.3 48.6L394.9 48.6L397.4 48.7L400.0 48.8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/>
  <g stroke="currentColor"><line x1="40" y1="160" x2="70" y2="160" stroke-width="2"/><line x1="40" y1="176" x2="70" y2="176" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/><line x1="40" y1="192" x2="70" y2="192" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/></g>
  <g font-size="11" fill="currentColor">
    <text x="6" y="54">target</text><text x="6" y="144">0</text><text x="386" y="156">time (s)</text>
    <text x="78" y="164">q/r = 100 &#183; wn = 3.16 &#183; settles 1.8 s</text>
    <text x="78" y="180">q/r = 1 &#183; wn = 1.00 &#183; settles 5.7 s</text>
    <text x="78" y="196">q/r = 0.01 &#183; wn = 0.32 &#183; settles 17.9 s</text>
  </g>
</svg>



### 4. LQG's fine print

The separation principle is exact for linear-Gaussian models — and famously fragile:
**LQG has no guaranteed robustness margins** (Doyle 1978's one-line abstract: "there are
none"). Estimator error and model error interact; real systems re-introduce margin checks
or robust variants. Read "we use LQG" as *nominal-optimal, robustness unverified unless
shown*.

**Why study it**: LQR is the reference point everything else is measured against —
[[04-robotics/mpc|MPC]] is "LQR + constraints, re-solved online" (its terminal cost $P$
is typically the LQR Riccati solution); RL policy evaluation on
linear-Gaussian problems recovers LQR; and time-varying LQR around a trajectory is the
standard tracking controller that learned planners hand their outputs to.

**Suggested path**: EE363 notes 1–4 (LQR derivation via dynamic programming) →
Underactuated ch. (geometric intuition, code) → connect to the
[[02-foundations/optimization|MPC-as-QP example]].

### Self-check

1. What happens to the Riccati approach if $(A,B)$ is not stabilizable?
2. On the double integrator, scale $Q$ by 10 and $R$ by 10 together — what happens to $K$?
3. In one sentence: why is "LQG is optimal, therefore robust" wrong?
4. Why use LQR's $P$ as the MPC terminal cost?

> [!tip]- Answers
> 1. No feedback can catch the unstable mode, so no stabilizing solution $P$ exists — the problem itself is ill-posed.
> 2. Unchanged — only the overall cost scale changes; the minimizing gain is the same. Only the ratio $Q/R$ determines $K$.
> 3. Optimality is with respect to the nominal model, and LQG is proven to have no guaranteed margins against model error (Doyle 1978).
> 4. $x^\top P x$ summarizes the exact unconstrained cost-to-go beyond the horizon, so a short horizon still supports the stability argument — Mayne 2000's terminal ingredient.

### Continue beyond this guide

The estimator side of LQG is developed in [[04-robotics/state-estimation-slam|State Estimation, Localization & SLAM]].

## 한국어

*[[04-robotics/control-theory-ce397|5. 제어 이론]]과 확률·최적화 위에 선다. D군이다. 극점을 손으로 고르는 대신 비용이 고르게 하고,
분리 원리가 추정기와 제어기를 따로 설계해도 되는 조건을 말해 준다.*

**무엇인가**: **LQR**은 최적 제어에서 정확히 풀리는 심장부다. 선형 동역학
$\dot x = Ax + Bu$와 이차 비용 $\int (x^\top Q x + u^\top R u)\,dt$에 대해 최적 제어기는
상수 선형 피드백 $u = -Kx$이고, $K = R^{-1}B^\top P$에서 $P$는 **대수 리카티 방정식**의
해다 — 실행 시 반복 계산이 없다. **LQG**는 가우시안 노이즈와 부분 관측을 더한 것: 최적해는
[[02-foundations/probability|칼만 필터]]가 LQR에 추정값을 공급하는 구조다
(**분리 원리**: 최적으로 추정하고, 그 추정값을 최적으로 제어하면, 그 결합이 전체 최적이다).

> [!note] 처음이라면 · First pass
> 짧은 페이지이니 통독하라. 10분뿐이라면 §2다 — "LQR은 안정성이 보장된다"에는 조건이 둘 붙어 있고, 비선형계를 선형화해 쓰는 논문은 그 조건을 선형화 지점에서만 물려받는다.

### 1. 리카티 방정식, 구조로 읽기

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

(로봇 논문은 대개 **이산 시간 쌍둥이** — DARE, 이득 $K=(R+B^\top P B)^{-1}B^\top P A$ — 를 쓴다; 구조도 읽는 법도 같다.) 손으로 푸는 일은 없다 — 하지만 구조로 읽으면 남는 게 있다: $Q$는 상태 비용을 주입하고,
이차 항 $-PBR^{-1}B^\top P$는 *피드백이 제어를 통해 비용을 깎아먹는* 항이며, 안정화 해
$P \succeq 0$가 $V(x)=x^\top P x$를 폐루프의 리아푸노프 함수로 만든다. 논문이 "리카티
방정식을 푼다"고 하면 이 상수 $P$를 오프라인에서 한 번(반복/시변 LQR에서는 선형화마다
한 번) 계산한다는 뜻이다.

### 2. 언제 실제로 통하는가? 두 조건

- **$(A,B)$의 안정화 가능성(stabilizability)**: $A$의 모든 불안정 모드가 $u$의 영향을
  받아야 한다 — 안정화 피드백이 존재하기 위한 정확한(필요충분) 조건이며,
  [[02-foundations/linear-algebra|1페이지 제어 섹션]]의 완전한 가제어성 랭크 검정보다
  약하다. 아니면 리카티든 뭐든 어떤 피드백도 안정화할 수 없다.
- **$(A,Q^{1/2})$의 검출 가능성(detectability)**: 모든 불안정 모드가 비용에 나타나야
  한다 — 아니면 최적화기가 조용히 발산하는 모드를 "신경 안 쓰는" 것이 허용되어, 최적
  비용의 제어기가 안정화 제어기가 아니게 된다.

이 둘이 "LQR은 안정성이 보장된다"의 작은 글씨다. 비선형 시스템을 선형화해 LQR을 쓰는
논문은 두 조건을 *선형화 지점에서만* 상속한다.

### 3. Q와 R이 거동에 하는 일 — 읽기용 예제

이중 적분기(카트): $x = (p, v)$, $u$ = 힘이므로
$A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$, $B = \begin{pmatrix}0\\1\end{pmatrix}$.
$Q = \mathrm{diag}(q, 0)$, $R = r$로 두자.

**이 경우는 손으로 실제로 풀린다**, 그리고 그 답이 어떤 솔버 출력보다 많은 것을 가르쳐 준다.
$P = \begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$로 놓고 리카티 방정식에 대입하면
서로 다른 세 성분에서 스칼라 방정식 셋이 나온다:

$$q - \frac{p_{12}^2}{r} = 0, \qquad p_{11} - \frac{p_{12}p_{22}}{r} = 0, \qquad 2p_{12} - \frac{p_{22}^2}{r} = 0$$

순서대로 풀면 $p_{12} = \sqrt{qr}$, 이어서 $p_{22} = \sqrt{2r\sqrt{qr}}$, 그리고 $p_{11}$이
따라 나온다. 이득 $K = R^{-1}B^\top P$는 $P$의 아랫줄을 $r$로 나눈 것이다:

$$k_1 = \sqrt{\rho}, \qquad k_2 = \sqrt{2}\,\rho^{1/4}, \qquad \rho = q/r$$

이제 이 식이 하는 말을 읽어보자 — 서로 다른 사실 셋이 한꺼번에 떨어진다.

| $q$ | $r$ | $\rho = q/r$ | $K = (k_1, k_2)$ | $\omega_n$ | $\zeta$ | 정착 시간 $\approx 4/\zeta\omega_n$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7초 |
| 100 | 1 | 100 | $(10.0,\ 4.47)$ | 3.16 | 0.707 | 1.8초 |
| 1 | 100 | 0.01 | $(0.10,\ 0.45)$ | 0.32 | 0.707 | 17.9초 |
| 10 | 10 | 1 | $(1.00,\ 1.41)$ | 1.00 | 0.707 | 5.7초 |

- **비(ratio)만 의미가 있다.** 1행과 4행의 이득이 완전히 같다: $Q$와 $R$을 함께 스케일하면
  비용값은 커지지만 그 argmin은 움직이지 않는다. 논문이 절대 가중치가 아니라 $Q/R$ 비를
  인용하는 이유이고, 스스로 점검 2번의 답이 여기 미리 나와 있다.
- **감쇠는 당신이 고르는 값이 아니다.** 모든 행에서 $\zeta = 1/\sqrt2 = 0.707$이다. 폐루프
  특성 다항식이 $\lambda^2 + \sqrt2\rho^{1/4}\lambda + \sqrt\rho$이므로
  $\omega_n = \rho^{1/4}$, $2\zeta\omega_n = \sqrt2\rho^{1/4}$가 되어 *어떤* 가중치에서도
  $\zeta = 0.707$이 강제된다. 이중 적분기 위의 LQR은 언제나 교과서적 최적 감쇠에 착륙한다:
  가중치가 사는 것은 속도이지 모양이 아니다. "LQR은 극점을 손이 아니라 최적화가 고른다"는
  일반론이 구체화된 것이다 — [[04-robotics/control-theory-ce397|제어 이론 §7]]은 손으로
  $\zeta = 0.7$에 놓았고, LQR은 시키지 않아도 사실상 같은 자리에 도착했다.
- **속도는 네제곱근이고, 이건 가혹하다.** $\omega_n = \rho^{1/4}$이므로 대역폭을 두 배로
  올리려면 $q/r$을 **16배**, 열 배로 올리려면 $10^4$배 키워야 한다. 실험 절에 "상태 가중치를
  두 자릿수 올렸다"고 쓰여 있으면 대역폭으로는 $\sqrt{10} \approx 3.2$배를 산 것이고,
  $k_1 = \sqrt\rho$가 10배 커졌으니 명령 힘도 대략 10배, 증폭되는 센서 잡음도 10배다.

실험 절이 쓰는 정성적 어휘가 정확히 이 산수에 대응한다:

- **큰 $q/r$**("상태가 비싸고 제어가 싸다"): 공격적 이득 — 빠른 회복, 큰 힘 스파이크, 잡음
  증폭 증가, 액추에이터 포화 위험(LQR 자신은 이를 모델링하지 않는다 —
  [[04-robotics/mpc|MPC]]의 몫이다).
- **작은 $q/r$**("제어가 비싸다"): 부드러운 이득, 느린 회복, 매끄러운 입력.
- 속도 vs 위치 가중치는 응답의 *감쇠* vs *강성*을 빚는다 — "정착 시간 …를 위해 Q/R을
  튜닝했다"는 문장 뒤의 손잡이 어휘다.

<svg viewBox="0 0 440 206" style="max-width:100%;height:auto" role="img" aria-label="세 가지 Q/R 비에서의 LQR 계단 응답 — 감쇠는 모두 같다">
  <g stroke="currentColor" stroke-width="1" opacity="0.3"><line x1="40" y1="50" x2="410" y2="50" stroke-dasharray="4 4"/><line x1="40" y1="140" x2="410" y2="140"/><line x1="40" y1="20" x2="40" y2="140"/></g>
  <path d="M40.0 140.0L42.6 132.6L45.1 116.5L47.7 98.1L50.3 81.3L52.9 67.7L55.4 58.0L58.0 51.6L60.6 48.0L63.1 46.4L65.7 46.1L68.3 46.5L70.9 47.3L73.4 48.0L76.0 48.8L78.6 49.3L81.1 49.7L83.7 50.0L86.3 50.1L88.9 50.2L91.4 50.2L94.0 50.1L96.6 50.1L99.1 50.1L101.7 50.0L104.3 50.0L106.9 50.0L109.4 50.0L112.0 50.0L114.6 50.0L117.1 50.0L119.7 50.0L122.3 50.0L124.9 50.0L127.4 50.0L130.0 50.0L132.6 50.0L135.1 50.0L137.7 50.0L140.3 50.0L142.9 50.0L145.4 50.0L148.0 50.0L150.6 50.0L153.1 50.0L155.7 50.0L158.3 50.0L160.9 50.0L163.4 50.0L166.0 50.0L168.6 50.0L171.1 50.0L173.7 50.0L176.3 50.0L178.9 50.0L181.4 50.0L184.0 50.0L186.6 50.0L189.1 50.0L191.7 50.0L194.3 50.0L196.9 50.0L199.4 50.0L202.0 50.0L204.6 50.0L207.1 50.0L209.7 50.0L212.3 50.0L214.9 50.0L217.4 50.0L220.0 50.0L222.6 50.0L225.1 50.0L227.7 50.0L230.3 50.0L232.9 50.0L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M40.0 140.0L42.6 139.1L45.1 136.8L47.7 133.3L50.3 128.9L52.9 123.8L55.4 118.3L58.0 112.6L60.6 106.7L63.1 100.9L65.7 95.2L68.3 89.7L70.9 84.5L73.4 79.6L76.0 75.0L78.6 70.8L81.1 67.0L83.7 63.6L86.3 60.6L88.9 57.9L91.4 55.6L94.0 53.6L96.6 51.8L99.1 50.4L101.7 49.2L104.3 48.3L106.9 47.5L109.4 47.0L112.0 46.6L114.6 46.3L117.1 46.2L119.7 46.1L122.3 46.1L124.9 46.2L127.4 46.4L130.0 46.6L132.6 46.8L135.1 47.0L137.7 47.3L140.3 47.5L142.9 47.8L145.4 48.0L148.0 48.3L150.6 48.5L153.1 48.7L155.7 48.9L158.3 49.1L160.9 49.2L163.4 49.4L166.0 49.5L168.6 49.6L171.1 49.8L173.7 49.8L176.3 49.9L178.9 50.0L181.4 50.0L184.0 50.1L186.6 50.1L189.1 50.1L191.7 50.1L194.3 50.2L196.9 50.2L199.4 50.2L202.0 50.2L204.6 50.2L207.1 50.2L209.7 50.1L212.3 50.1L214.9 50.1L217.4 50.1L220.0 50.1L222.6 50.1L225.1 50.1L227.7 50.1L230.3 50.1L232.9 50.1L235.4 50.0L238.0 50.0L240.6 50.0L243.1 50.0L245.7 50.0L248.3 50.0L250.9 50.0L253.4 50.0L256.0 50.0L258.6 50.0L261.1 50.0L263.7 50.0L266.3 50.0L268.9 50.0L271.4 50.0L274.0 50.0L276.6 50.0L279.1 50.0L281.7 50.0L284.3 50.0L286.9 50.0L289.4 50.0L292.0 50.0L294.6 50.0L297.1 50.0L299.7 50.0L302.3 50.0L304.9 50.0L307.4 50.0L310.0 50.0L312.6 50.0L315.1 50.0L317.7 50.0L320.3 50.0L322.9 50.0L325.4 50.0L328.0 50.0L330.6 50.0L333.1 50.0L335.7 50.0L338.3 50.0L340.9 50.0L343.4 50.0L346.0 50.0L348.6 50.0L351.1 50.0L353.7 50.0L356.3 50.0L358.9 50.0L361.4 50.0L364.0 50.0L366.6 50.0L369.1 50.0L371.7 50.0L374.3 50.0L376.9 50.0L379.4 50.0L382.0 50.0L384.6 50.0L387.1 50.0L389.7 50.0L392.3 50.0L394.9 50.0L397.4 50.0L400.0 50.0" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/>
  <path d="M40.0 140.0L42.6 139.9L45.1 139.6L47.7 139.2L50.3 138.7L52.9 137.9L55.4 137.1L58.0 136.1L60.6 135.1L63.1 133.9L65.7 132.6L68.3 131.3L70.9 129.8L73.4 128.3L76.0 126.8L78.6 125.2L81.1 123.5L83.7 121.8L86.3 120.0L88.9 118.3L91.4 116.5L94.0 114.7L96.6 112.8L99.1 111.0L101.7 109.1L104.3 107.3L106.9 105.4L109.4 103.6L112.0 101.7L114.6 99.9L117.1 98.1L119.7 96.3L122.3 94.5L124.9 92.8L127.4 91.0L130.0 89.3L132.6 87.7L135.1 86.0L137.7 84.4L140.3 82.8L142.9 81.3L145.4 79.7L148.0 78.3L150.6 76.8L153.1 75.4L155.7 74.0L158.3 72.7L160.9 71.4L163.4 70.1L166.0 68.9L168.6 67.7L171.1 66.6L173.7 65.5L176.3 64.4L178.9 63.4L181.4 62.4L184.0 61.4L186.6 60.5L189.1 59.6L191.7 58.8L194.3 58.0L196.9 57.2L199.4 56.4L202.0 55.7L204.6 55.1L207.1 54.4L209.7 53.8L212.3 53.2L214.9 52.7L217.4 52.1L220.0 51.6L222.6 51.2L225.1 50.7L227.7 50.3L230.3 49.9L232.9 49.5L235.4 49.2L238.0 48.9L240.6 48.6L243.1 48.3L245.7 48.0L248.3 47.8L250.9 47.6L253.4 47.4L256.0 47.2L258.6 47.0L261.1 46.9L263.7 46.8L266.3 46.6L268.9 46.5L271.4 46.4L274.0 46.4L276.6 46.3L279.1 46.2L281.7 46.2L284.3 46.2L286.9 46.1L289.4 46.1L292.0 46.1L294.6 46.1L297.1 46.1L299.7 46.1L302.3 46.2L304.9 46.2L307.4 46.2L310.0 46.3L312.6 46.3L315.1 46.4L317.7 46.4L320.3 46.5L322.9 46.5L325.4 46.6L328.0 46.7L330.6 46.7L333.1 46.8L335.7 46.9L338.3 46.9L340.9 47.0L343.4 47.1L346.0 47.2L348.6 47.3L351.1 47.3L353.7 47.4L356.3 47.5L358.9 47.6L361.4 47.7L364.0 47.7L366.6 47.8L369.1 47.9L371.7 48.0L374.3 48.0L376.9 48.1L379.4 48.2L382.0 48.3L384.6 48.3L387.1 48.4L389.7 48.5L392.3 48.6L394.9 48.6L397.4 48.7L400.0 48.8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/>
  <g stroke="currentColor"><line x1="40" y1="160" x2="70" y2="160" stroke-width="2"/><line x1="40" y1="176" x2="70" y2="176" stroke-width="1.7" opacity="0.7" stroke-dasharray="7 4"/><line x1="40" y1="192" x2="70" y2="192" stroke-width="1.5" opacity="0.45" stroke-dasharray="2 3"/></g>
  <g font-size="11" fill="currentColor">
    <text x="6" y="54">목표값</text><text x="6" y="144">0</text><text x="386" y="156">시간 (초)</text>
    <text x="78" y="164">q/r = 100 &#183; wn = 3.16 &#183; 정착 1.8초</text>
    <text x="78" y="180">q/r = 1 &#183; wn = 1.00 &#183; 정착 5.7초</text>
    <text x="78" y="196">q/r = 0.01 &#183; wn = 0.32 &#183; 정착 17.9초</text>
  </g>
</svg>



### 4. LQG의 작은 글씨

분리 원리는 선형-가우시안 모델에서 정확하다 — 그리고 유명하게 취약하다: **LQG에는
보장된 강건성 여유가 없다** (Doyle 1978의 한 줄 초록: "there are none"). 추정 오차와 모델
오차가 상호작용한다; 실제 시스템은 여유 검사나 강건 변형을 다시 도입한다. "LQG를 쓴다"는
*공칭 최적, 강건성은 보이기 전까지 미검증*으로 읽어라.

**왜 공부하나**: LQR은 다른 모든 것을 재는 기준점이다 — [[04-robotics/mpc|MPC]]는 "제약을
더해 온라인으로 다시 푸는 LQR"이고(그 종단 비용 $P$가 보통 LQR 리카티 해다),
선형-가우시안 문제의 RL 정책 평가는 LQR을 복원하며, 궤적 주변의 시변 LQR은 학습된
플래너가 출력을 넘기는 표준 추종 제어기다.

**권장 경로**: EE363 노트 1~4 (동적 계획법으로 LQR 유도) → Underactuated 해당 장(기하적
직관, 코드) → [[02-foundations/optimization|MPC-QP 예제]]로 연결.

### 연결

- 기초: [[02-foundations/linear-algebra|선형대수]] (리카티, 고유값), [[02-foundations/probability|확률]] (칼만), [[02-foundations/optimization|최적화]]
- 다음: [[04-robotics/mpc|MPC]]

### 스스로 점검 · Self-check

1. $(A,B)$가 안정화 가능하지 않으면 리카티 접근에 무슨 일이 생기나?
2. 이중 적분기에서 $Q$를 10배, $R$을 10배 함께 키우면 $K$는 어떻게 되나?
3. "LQG는 최적이므로 강건하다"가 틀린 이유를 한 문장으로.
4. MPC의 종단 비용으로 LQR의 $P$를 쓰는 이유는?

> [!tip]- 정답 · Answers
> 1. 불안정 모드를 어떤 피드백도 못 잡으므로 안정화 해 $P$가 존재하지 않는다 — 문제 자체가 불량이다.
> 2. 불변 — 비용 전체의 스케일만 바뀌고 최소화 지점(이득)은 같다. 비율 $Q/R$만이 $K$를 정한다.
> 3. 최적성은 공칭 모델에 대한 것이고, LQG는 모델 오차에 대한 보장된 여유가 없음이 증명되어 있다(Doyle 1978).
> 4. 지평 끝 이후의 "남은 최적 비용"을 LQR의 $x^\top P x$가 정확히(비제약 영역에서) 요약해 주므로, 짧은 지평으로도 안정성 논증이 성립한다 — Mayne 2000의 종단 재료.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] State the LQR problem and the form of its solution ($u = -Kx$, $K = R^{-1}B^\top P$) · LQR 문제 설정과 해의 형태를 말할 수 있다
- [ ] Say what stabilizability and detectability each guarantee, and what fails without them · 안정화 가능성·검출 가능성이 각각 무엇을 보장하는 조건인지 말할 수 있다
- [ ] Explain with the worked example how the $Q/R$ ratio changes gains, response, and saturation risk · $Q/R$ 비율이 이득·응답·포화 위험을 어떻게 바꾸는지 예제로 말할 수 있다
- [ ] State the separation principle and its fragility (LQG has no guaranteed margins), and why LQR is the reference point for MPC and RL · 분리 원리와 그 취약성(LQG 무여유), LQR이 MPC·RL의 기준점인 이유를 말할 수 있다
