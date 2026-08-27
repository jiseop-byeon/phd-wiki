---
title: "7. MPC"
tags: [robotics, control]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Key reference** — Mayne, Rawlings, Rao & Scokaert, *Constrained model predictive control: Stability and optimality*, Automatica 2000 · [DOI](https://doi.org/10.1016/S0005-1098(99)00214-9)

## English

*Group D. Stands on [[04-robotics/control-theory-ce397|5]] and [[04-robotics/lqr-lqg|6]]. Handling input and state constraints natively is its whole reason for existing
next to LQR, and [[04-robotics/convex-mpc-legged|8. Convex MPC]] is the application that made it standard on legged robots.*

> [!info] Depth target · 깊이 목표
> Read an MPC formulation (cost, horizon, constraints), identify what is solved online at each step, judge feasibility/stability claims, and recognize the standard failure modes. Solver internals are optional.
> MPC 정식화(비용·지평·제약)를 읽고, 매 스텝 온라인으로 무엇이 풀리는지 짚고, feasibility/안정성 주장을 판단하고, 표준 실패 모드를 알아볼 수 있으면 된다. 솔버 내부는 선택이다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/control-theory-ce397|5. Control Theory]] (state space, stability, and *why saturation breaks every linear guarantee* — the gap MPC exists to close) · [[04-robotics/lqr-lqg|6. LQR/LQG]] (its Riccati $P$ is MPC's usual terminal cost) · [[02-foundations/optimization|4. Optimization §2–5]] (convexity, KKT, and the MPC-as-QP example written out there)
> [[04-robotics/control-theory-ce397|5. 제어 이론]] (상태공간, 안정성, 그리고 *포화가 모든 선형 보장을 왜 깨는가* — MPC가 메우려는 그 간극) · [[04-robotics/lqr-lqg|6. LQR/LQG]] (그 리카티 $P$가 MPC의 표준 종단 비용) · [[02-foundations/optimization|4. 최적화 §2–5]] (볼록성, KKT, 거기 써 놓은 MPC-QP 예제)

**What it is**: **Model Predictive Control** solves, at every control step, a finite-horizon
optimal control problem from the current state, applies only the first input, and re-solves
at the next step (receding horizon). With linear dynamics and quadratic cost it is a
convex QP — written out fully in [[02-foundations/optimization|4. Optimization §5]] —
and constraints on inputs and states are handled *natively*, which is
MPC's whole advantage over [[04-robotics/lqr-lqg|LQR]].

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="receding horizon: plan over the horizon, execute one step, re-plan">
  <g stroke="currentColor" stroke-width="1" opacity="0.3">
    <line x1="30" y1="170" x2="440" y2="170"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.25" stroke-dasharray="2 4">
    <line x1="60" y1="20" x2="60" y2="170"/><line x1="100" y1="20" x2="100" y2="170"/><line x1="140" y1="20" x2="140" y2="170"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.45" stroke-dasharray="5 3">
    <path d="M60,120 C110,96 170,88 260,84"/>
    <path d="M100,110 C150,88 210,80 300,78"/>
    <path d="M140,100 C190,80 250,74 340,72"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="2.4">
    <path d="M60,120 L100,110"/><path d="M100,110 L140,100"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="120" r="3.5"/><circle cx="100" cy="110" r="3.5"/><circle cx="140" cy="100" r="3.5"/></g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="186">t</text><text x="90" y="186">t+1</text><text x="130" y="186">t+2</text>
    <text x="268" y="88" opacity="0.8">planned horizon (thrown away)</text>
    <text x="150" y="130">actually executed</text>
    <text x="30" y="16" opacity="0.9">each step: solve the whole horizon, keep only the first input, shift, solve again</text>
  </g>
</svg>



**The Mayne et al. 2000 survey** is the field's canonical reference: it settled *when MPC
is stable* — the roles of the terminal cost, terminal constraint set, and horizon length —
turning a practical heuristic into a theory. The mechanism, in one paragraph: if the
horizon ends inside a **terminal set** that is *invariant* under a known local controller
(invariant = once the state is inside that set, the controller keeps it inside forever),
then a feasible plan today implies a feasible plan tomorrow (append one step of that
controller) — this is **recursive feasibility**, the property MPC papers invoke by name;
and if the terminal cost decreases like a Lyapunov function under that controller, closed-loop
stability follows. Read the survey after the optimization page's example; skim §2–3 for
the formulation and stability conditions rather than every proof.

### 1. When is the QP actually convex?

The "it's just a QP" claim carries conditions worth checking in any paper:

- **Cost**: $Q \succeq 0$, $R \succ 0$, terminal $P \succeq 0$ — the quadratic must be
  (semi)definite ([[02-foundations/linear-algebra|SPD, page 1 §3]]). An indefinite $Q$
  (e.g., from a learned cost) breaks convexity silently.
- **Dynamics**: linear (or linearized — then the QP is only an approximation whose quality
  decays away from the linearization point).
- **Constraints**: input/state sets must be convex (boxes, polytopes). **Obstacle-avoidance
  constraints are non-convex** — which is why collision-aware MPC papers either convexify
  locally (safe corridors) or leave the QP world entirely.

### 2. What the solver actually sees

Two standard ways to write the same problem — papers assume you know which one they use:

- **Stacked (sparse) form**: keep all states $x_{0:N}$ and inputs $u_{0:N-1}$ as
  variables and add dynamics as equality constraints — a large, *sparse, banded* problem
  that interior-point solvers exploit; cost matrices sit in blocks along the diagonal.
- **Condensed form**: eliminate the states using $x_k = A^k x_0 + \sum_j A^{k-1-j}Bu_j$,
  leaving only $u_{0:N-1}$ — a smaller but *dense* QP whose condition number worsens with
  horizon length (powers of $A$).

**Size it, so "large" and "small" stop being adjectives.** Take a quadruped centroidal MPC
of the kind [[04-robotics/convex-mpc-legged|convex MPC papers]] run: state $n_x = 13$
(position, orientation, their velocities, plus gravity), input $n_u = 12$ (a 3-vector force
at each of 4 feet), horizon $N = 10$.

| | variables | equality constraints | Hessian |
|---|---|---|---|
| **Stacked** | $(N{+}1)n_x + Nn_u = 143 + 120 = 263$ | $Nn_x = 130$ | $263\times263$, **banded** — mostly zeros |
| **Condensed** | $Nn_u = 120$ | none (dynamics substituted in) | $120\times120$, **dense** — every entry filled |

Condensed has under half the variables, which sounds decisive until you notice its Hessian is
dense: $120^2 = 14{,}400$ nonzeros, against a stacked matrix whose nonzero count grows only
linearly in $N$. Doubling the horizon roughly doubles stacked work; it *quadruples* the
condensed Hessian's entry count and, because dense factorization is cubic in the variable
count, multiplies condensed solve
work. And at 50 Hz the entire solve must finish inside **20 ms**, minus whatever state
estimation already spent — which is why this choice is a real engineering decision rather
than a stylistic one.

Rule of thumb when reading: long horizons and state constraints → stacked; short horizons,
input constraints only → condensed. (The conditioning penalty applies to marginally stable
or unstable $A$ — the usual robotics case; for strictly stable $A$ the powers decay and
condensed stays well-behaved.)

### 3. The failure modes papers gloss over

- **Infeasibility**: a disturbance pushes the state where *no* input sequence satisfies
  the constraints — the solver returns nothing, and the controller must do *something*.
  Standard fix: **constraint softening** — replace hard state constraints with penalized
  slack variables $\sigma \ge 0$ (cost $+\rho\|\sigma\|$), so the QP always has an answer
  that violates gracefully rather than crashing. Input (actuator) constraints stay hard.
- **Model mismatch**: MPC optimizes the *model's* future; bias between model and plant
  turns "optimal" plans into repeated small errors that feedback (the re-solving itself)
  must absorb. Watch for papers quantifying this vs assuming it away.
- **Latency and rate**: the plan is computed from a state estimate that is stale by the
  solve time ([[04-robotics/robot-systems-deployment|systems page §3]]). **Warm starting**
  — initializing the solver from the previous solution shifted one step — is what makes
  high-rate MPC possible; cold-started NMPC at 100 Hz is a red flag.
- **Estimator coupling**: MPC consumes $\hat{x}$, not $x$
  ([[04-robotics/state-estimation-slam|estimation page]]) — estimator bias becomes
  systematic constraint violation.

### 4. Linear vs nonlinear vs contact

- **Linear MPC**: convex QP; solve times from microseconds to milliseconds *for
  small-to-moderate problems on modern CPUs* — always condition speed claims on problem
  size, solver, and hardware.
- **Nonlinear MPC (NMPC)**: sequential quadratic programming or DDP-style solvers;
  local optima and initialization sensitivity return
  ([[04-robotics/planning-decision-making|planning §6]]).
- **Contact-implicit MPC**: contact mode switches make the problem non-smooth
  ([[04-robotics/contact-force-tactile|contact §1]]); the
  [[04-robotics/convex-mpc-legged|legged convex-MPC]] trick is to *pre-specify* the
  contact schedule so the remaining problem is convex — read that page as the
  representative escape route.

**Where it meets learning** (this wiki's angle):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]] is MPC with a *learned* model and CEM solver;
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]'s receding-horizon action
chunks borrow MPC's structure; learned-dynamics MPC for excavators is an active
construction-robotics direction ([[05-construction-robotics/earthmoving-heavy-machinery|stream 3]]).

### Self-check

1. You plug a learned cost matrix $Q$ into an MPC and the solver misbehaves. First thing to check?
2. Horizon $N=50$ with many state constraints — expect stacked or condensed? Why?
3. A disturbance pushes the state outside the constraint set. What happens under hard-constrained vs softened MPC?
4. A paper claims "our NMPC runs at 200 Hz." Name three things to check.

> [!tip]- Answers
> 1. Whether $Q \succeq 0$ — if indefinite, the QP is non-convex and solver behavior is undefined.
> 2. Stacked — at long horizons the condensed form becomes dense and ill-conditioned via powers of $A$, and state constraints are natural in the stacked form.
> 3. Hard: infeasible — the solver returns nothing and a separate fallback must act. Soft: slacks activate and it returns a penalized, gracefully violating solution — control continues.
> 4. ① Warm-started or cold? ② Problem size (horizon, state dimension) and solver? ③ Is 200 Hz solve time or end-to-end latency ([[04-robotics/robot-systems-deployment|frequency ≠ latency]])?

### Continue beyond this guide

See [[04-robotics/planning-decision-making|Planning & Decision-Making]] for trajectory optimization, replanning, task planning, and planning under uncertainty.

## 한국어

*[[04-robotics/control-theory-ce397|5]]·[[04-robotics/lqr-lqg|6]]번 위에 선다. D군이다. 입력·상태 제약을 태생적으로 다루는 것이 LQR 옆에 존재하는 이유이고,
[[04-robotics/convex-mpc-legged|8. Convex MPC]]가 이것을 보행 로봇의 표준으로 만든 응용이다.*

**무엇인가**: **모델 예측 제어**는 매 제어 주기마다 현재 상태에서 유한 지평 최적 제어
문제를 풀고, 첫 입력만 적용한 뒤, 다음 주기에 다시 푼다(receding horizon). 선형 동역학과
이차 비용이면 볼록 QP가 되고 — [[02-foundations/optimization|4. 최적화 §5]]에 완전히 써
놓았다 — 입력·상태 제약을 *태생적으로* 다루는 것이
[[04-robotics/lqr-lqg|LQR]] 대비 MPC의 존재 이유다.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="receding horizon: 지평 전체를 계획하고 한 스텝만 실행한 뒤 다시 계획">
  <g stroke="currentColor" stroke-width="1" opacity="0.3">
    <line x1="30" y1="170" x2="440" y2="170"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.25" stroke-dasharray="2 4">
    <line x1="60" y1="20" x2="60" y2="170"/><line x1="100" y1="20" x2="100" y2="170"/><line x1="140" y1="20" x2="140" y2="170"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.45" stroke-dasharray="5 3">
    <path d="M60,120 C110,96 170,88 260,84"/>
    <path d="M100,110 C150,88 210,80 300,78"/>
    <path d="M140,100 C190,80 250,74 340,72"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="2.4">
    <path d="M60,120 L100,110"/><path d="M100,110 L140,100"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="120" r="3.5"/><circle cx="100" cy="110" r="3.5"/><circle cx="140" cy="100" r="3.5"/></g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="186">t</text><text x="90" y="186">t+1</text><text x="130" y="186">t+2</text>
    <text x="268" y="88" opacity="0.8">계획된 지평(버려진다)</text>
    <text x="150" y="130">실제로 실행된 부분</text>
    <text x="30" y="16" opacity="0.9">매 주기: 지평 전체를 풀고, 첫 입력만 남기고, 한 칸 밀어 다시 푼다</text>
  </g>
</svg>



**Mayne et al. 2000 서베이**는 이 분야의 정본이다: *MPC가 언제 안정한가* — 종단 비용,
종단 제약 집합, 지평 길이의 역할 — 를 정리해 실용적 휴리스틱을 이론으로 만들었다.
메커니즘을 한 단락으로: 지평의 끝이 알려진 국소 제어기 아래 *불변*인 **종단 집합** 안에
떨어지면(불변 = 일단 상태가 그 집합 안에 들어오면 그 제어기가 영원히 그 안에 잡아둔다), 오늘의 실행 가능한 계획이 내일의 실행 가능한 계획을 함의한다(그 제어기 한
스텝을 이어 붙이면 된다) — 이것이 MPC 논문들이 이름으로 부르는 **recursive
feasibility**다; 그리고 종단 비용이 그 제어기 아래 리아푸노프 함수처럼 감소하면 폐루프
안정성이 따라온다. 서베이는 최적화 페이지의 예제를 본 뒤에 읽되, 모든 증명보다는
§2~3의 정식화와 안정성 조건을 훑는 것을 권한다.

### 1. QP는 언제 실제로 볼록한가?

"그냥 QP다"라는 주장에는 논문에서 확인할 조건들이 붙어 있다:

- **비용**: $Q \succeq 0$, $R \succ 0$, 종단 $P \succeq 0$ — 이차형식이 (준)정부호여야
  한다 ([[02-foundations/linear-algebra|SPD, 1페이지 §3]]). (학습된 비용 등에서 나온)
  부정부호 $Q$는 볼록성을 조용히 깨뜨린다.
- **동역학**: 선형(또는 선형화 — 이 경우 QP는 선형화 지점에서 멀어질수록 품질이 떨어지는
  근사일 뿐이다).
- **제약**: 입력/상태 집합이 볼록해야 한다(박스, 폴리토프). **장애물 회피 제약은
  비볼록이다** — 충돌 인지 MPC 논문들이 국소 볼록화(안전 통로)를 하거나 아예 QP 세계를
  떠나는 이유다.

### 2. 솔버가 실제로 보는 것

같은 문제를 쓰는 표준적인 두 방식 — 논문은 독자가 어느 쪽인지 안다고 가정한다:

- **Stacked (희소) 형태**: 모든 상태 $x_{0:N}$과 입력 $u_{0:N-1}$을 변수로 두고 동역학을
  등식 제약으로 추가 — 크지만 *희소·띠 구조*라 내부점 솔버가 활용한다; 비용 행렬이
  대각 블록으로 놓인다.
- **Condensed (축약) 형태**: $x_k = A^k x_0 + \sum_j A^{k-1-j}Bu_j$로 상태를 소거해
  $u_{0:N-1}$만 남긴다 — 작지만 *조밀*하고, 지평이 길수록($A$의 거듭제곱) 조건수가
  나빠진다.

**크기를 재 보자 — 그래야 "크다"와 "작다"가 형용사에서 벗어난다.**
[[04-robotics/convex-mpc-legged|convex MPC 논문]]들이 돌리는 사족보행 centroidal MPC로 예를
들면: 상태 $n_x = 13$(위치, 자세, 그 속도들, 그리고 중력), 입력 $n_u = 12$(발 4개 각각의
3차원 힘), 지평 $N = 10$.

| | 변수 | 등식 제약 | 헤시안 |
|---|---|---|---|
| **Stacked** | $(N{+}1)n_x + Nn_u = 143 + 120 = 263$ | $Nn_x = 130$ | $263\times263$, **띠 구조** — 대부분 0 |
| **Condensed** | $Nn_u = 120$ | 없음(동역학을 대입해 소거) | $120\times120$, **밀집** — 모든 성분이 채워짐 |

Condensed는 변수가 절반 이하라 결정적으로 보이지만, 헤시안이 밀집이라는 점을 보면 달라진다:
비영 성분이 $120^2 = 14{,}400$개인 반면 stacked의 비영 성분은 $N$에 대해 선형으로만 늘어난다.
지평을 두 배로 하면 stacked는 대략 두 배가 되고, condensed는 헤시안 *원소 수*가 네 배가 되며, 조밀 분해가 변수 수의 3제곱이므로 실제 풀이 일은 약 **여덟 배**가 된다. 그리고 50 Hz라면
이 풀이 전체가 **20 ms** 안에 끝나야 하고, 거기서 상태 추정이 이미 쓴 시간을 빼야 한다 —
이 선택이 취향이 아니라 실제 엔지니어링 결정인 이유다.

읽을 때의 어림 규칙: 긴 지평 + 상태 제약 → stacked; 짧은 지평 + 입력 제약만 → condensed.
(조건수 페널티는 한계 안정/불안정 $A$ — 로봇의 통상 사례 — 에 해당하고, 엄격히 안정한
$A$에서는 거듭제곱이 감쇠해 condensed도 얌전하다.)

### 3. 논문이 얼버무리는 실패 모드

- **Infeasibility**: 외란이 상태를 *어떤* 입력 시퀀스로도 제약을 만족할 수 없는 곳으로
  밀면 — 솔버는 아무것도 돌려주지 않고, 제어기는 *뭐라도* 해야 한다. 표준 처방:
  **제약 연화(constraint softening)** — 딱딱한 상태 제약을 벌점 붙은 슬랙 변수
  $\sigma \ge 0$(비용 $+\rho\|\sigma\|$)로 바꿔, QP가 우아하게 위반하는 답이라도 항상
  내놓게 한다. 입력(액추에이터) 제약은 딱딱하게 유지한다.
- **모델 불일치**: MPC는 *모델의* 미래를 최적화한다; 모델과 플랜트의 편차는 "최적" 계획을
  피드백(재풀이 자체)이 흡수해야 하는 반복적 소오차로 바꾼다. 이를 정량화하는 논문과
  가정으로 치우는 논문을 구분하라.
- **지연과 주기**: 계획은 풀이 시간만큼 낡은 상태 추정에서 계산된다
  ([[04-robotics/robot-systems-deployment|시스템 페이지 §3]]). **Warm start** — 이전 해를
  한 스텝 밀어 솔버를 초기화 — 가 고주기 MPC를 가능하게 하는 것이다; 100 Hz의 cold-start
  NMPC는 적신호다.
- **추정기 결합**: MPC는 $x$가 아니라 $\hat{x}$를 소비한다
  ([[04-robotics/state-estimation-slam|추정 페이지]]) — 추정기 편향은 계통적 제약 위반이
  된다.

### 4. 선형 vs 비선형 vs 접촉

- **선형 MPC**: 볼록 QP; *현대 CPU에서 중소 규모 문제라면* 마이크로초~밀리초의 풀이
  시간 — 속도 주장은 항상 문제 크기·솔버·하드웨어를 조건으로 달아 읽어라.
- **비선형 MPC (NMPC)**: SQP 또는 DDP류 솔버; 국소 최적과 초기화 민감성이 돌아온다
  ([[04-robotics/planning-decision-making|계획 §6]]).
- **접촉 내재 MPC**: 접촉 모드 전환이 문제를 비매끄럽게 만든다
  ([[04-robotics/contact-force-tactile|접촉 §1]]);
  [[04-robotics/convex-mpc-legged|보행 convex MPC]]의 트릭은 접촉 스케줄을 *미리 지정*해
  남는 문제를 볼록하게 만드는 것 — 대표적 탈출로로 그 페이지를 읽어라.

**학습과 만나는 지점** (이 위키의 관심사):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]]은 *학습된* 모델과 CEM 솔버의 MPC이고,
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]의 receding-horizon 행동
청크는 MPC의 구조를 빌린 것이며, 굴착기의 학습 동역학 MPC는 건설로봇의 활발한 연구
방향이다 ([[05-construction-robotics/earthmoving-heavy-machinery|스트림 3]]).

### 연결

- 기초: [[02-foundations/optimization|최적화]] (QP, KKT), [[02-foundations/linear-algebra|선형대수]]
- 이전: [[04-robotics/lqr-lqg|LQR/LQG]] · 다음: [[04-robotics/convex-mpc-legged|보행 로봇의 convex MPC]]

### 스스로 점검 · Self-check

1. 학습된 비용 행렬 $Q$를 MPC에 꽂았더니 솔버가 이상하게 군다. 가장 먼저 확인할 것은?
2. 지평 $N=50$, 상태 제약이 많은 문제 — stacked와 condensed 중 무엇을 기대해야 하나? 왜?
3. 외란으로 상태가 제약 밖으로 밀렸다. 하드 제약 MPC와 소프트 제약 MPC는 각각 어떻게 되나?
4. "우리 NMPC는 200 Hz로 돈다"라는 주장에서 확인할 세 가지는?

> [!tip]- 정답 · Answers
> 1. $Q \succeq 0$인지 — 부정부호면 QP가 비볼록이 되어 솔버 거동이 정의되지 않는다.
> 2. Stacked — 긴 지평에서 condensed는 $A$의 거듭제곱으로 조밀·악조건이 되고, 상태 제약은 stacked에서 자연스럽다.
> 3. 하드: infeasible — 솔버가 해를 반환하지 않아 별도의 폴백이 필요. 소프트: 슬랙이 켜져 벌점을 내며 위반하는 해를 반환 — 제어는 계속된다.
> 4. ① warm start 여부 ② 문제 크기(지평·상태 차원)와 솔버 ③ 그 200 Hz가 풀이 시간인지 끝-끝 지연인지 ([[04-robotics/robot-systems-deployment|주파수 ≠ 지연]]).

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Describe the receding-horizon procedure (solve → apply the first input → re-solve) · receding horizon 절차를 말할 수 있다
- [ ] State the conditions for QP convexity ($Q,R,P$ definiteness, convex constraints) and where obstacle constraints break them · QP 볼록성의 조건과 장애물 제약이 깨뜨리는 지점을 말할 수 있다
- [ ] Explain the stacked vs condensed trade-off, and infeasibility, constraint softening, and warm starting · stacked/condensed 정식화의 트레이드오프와 infeasibility·softening·warm start를 설명할 수 있다
- [ ] Name Mayne 2000's stability ingredients (terminal cost, terminal set, horizon) and where PlaNet and Diffusion Policy borrow MPC's structure · Mayne 2000의 안정성 재료와 PlaNet·Diffusion Policy가 MPC 구조를 빌린 지점을 말할 수 있다
