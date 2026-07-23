---
title: "6. LQR / LQG"
tags: [robotics, control, resource]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Study links** — [Underactuated Robotics, LQR chapter (Tedrake, MIT)](https://underactuated.csail.mit.edu/lqr.html) · [Stanford EE363 lecture notes (Boyd)](https://web.stanford.edu/class/ee363/)

## English

> [!info] Depth target · 깊이 목표
> State the LQR problem, the role of the Riccati equation, the conditions under which the solution exists and stabilizes, and LQG's estimator–controller separation with its caveat. Deriving or implementing Riccati solvers is optional.
> LQR 문제, 리카티 방정식의 역할, 해가 존재하고 안정화하는 조건, LQG의 추정기–제어기 분리와 그 단서를 말할 수 있으면 된다. 리카티 해법의 유도·구현은 선택이다.

**What it is**: the **Linear Quadratic Regulator** is the exactly-solvable heart of optimal
control. For linear dynamics $\dot x = Ax + Bu$ and quadratic cost
$\int (x^\top Q x + u^\top R u)\,dt$, the optimal controller is a constant linear feedback
$u = -Kx$, with $K = R^{-1}B^\top P$ where $P$ solves the **algebraic Riccati equation** —
no iteration at runtime.
**LQG** adds Gaussian noise and partial observation: the optimal solution is a
[[02-foundations/probability|Kalman filter]] feeding an LQR (the **separation principle**:
estimate optimally, then control the estimate optimally, and it is jointly optimal).

### 1. The Riccati equation, read structurally

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

You never solve this by hand — but reading it structurally pays: $Q$ injects state cost,
the quadratic $-PBR^{-1}B^\top P$ term is *feedback eating cost through control*, and the
stabilizing solution $P \succeq 0$ is what makes $V(x)=x^\top P x$ a Lyapunov function for
the closed loop. When a paper says "we solve a Riccati equation," it means this constant
$P$, computed once offline (or once per linearization in iterative/time-varying LQR).

### 2. When does this actually work? Two conditions

- **Stabilizability** of $(A,B)$: every unstable mode of $A$ must be influenceable by $u$
  (a weaker, sufficient version of the controllability rank test in
  [[02-foundations/linear-algebra|page 1's control section]]). Otherwise no feedback can
  stabilize, Riccati or not.
- **Detectability** of $(A,Q^{1/2})$: every unstable mode must show up in the cost —
  otherwise the optimizer can "not care" about a mode that is quietly diverging, and the
  optimal-cost controller is not stabilizing.

These two are the fine print behind "LQR is guaranteed stable." Papers that linearize a
nonlinear system and run LQR inherit both conditions *at the linearization point only*.

### 3. What Q and R do to behavior — a worked reading

Double integrator (cart): $x = (p, v)$, $u$ = force. Choose
$Q = \mathrm{diag}(q_p, 0)$, $R = r$:

- **Large $q_p/r$** ("state expensive, control cheap"): aggressive gains — fast position
  recovery, large force spikes, more noise amplification, actuator saturation risk (which
  LQR itself does not model — that's [[04-robotics/mpc|MPC]]'s job).
- **Small $q_p/r$** ("control expensive"): gentle gains, slow recovery, smooth inputs.
- Only the *ratio* matters (scaling $Q,R$ together rescales cost, not $K$), and weights on
  velocity vs position shape *damping* vs *stiffness* of the response — this is the knob
  vocabulary experimental sections use ("we tuned Q/R for a settling time of…").

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

### Continue beyond this guide

The estimator side of LQG is developed in [[04-robotics/state-estimation-slam|State Estimation, Localization & SLAM]].

## 한국어

**무엇인가**: **LQR**은 최적 제어에서 정확히 풀리는 심장부다. 선형 동역학
$\dot x = Ax + Bu$와 이차 비용 $\int (x^\top Q x + u^\top R u)\,dt$에 대해 최적 제어기는
상수 선형 피드백 $u = -Kx$이고, $K = R^{-1}B^\top P$에서 $P$는 **대수 리카티 방정식**의
해다 — 실행 시 반복 계산이 없다. **LQG**는 가우시안 노이즈와 부분 관측을 더한 것: 최적해는
[[02-foundations/probability|칼만 필터]]가 LQR에 추정값을 공급하는 구조다
(**분리 원리**: 최적으로 추정하고, 그 추정값을 최적으로 제어하면, 그 결합이 전체 최적이다).

### 1. 리카티 방정식, 구조로 읽기

$$A^\top P + PA - PBR^{-1}B^\top P + Q = 0$$

손으로 푸는 일은 없다 — 하지만 구조로 읽으면 남는 게 있다: $Q$는 상태 비용을 주입하고,
이차 항 $-PBR^{-1}B^\top P$는 *피드백이 제어를 통해 비용을 깎아먹는* 항이며, 안정화 해
$P \succeq 0$가 $V(x)=x^\top P x$를 폐루프의 리아푸노프 함수로 만든다. 논문이 "리카티
방정식을 푼다"고 하면 이 상수 $P$를 오프라인에서 한 번(반복/시변 LQR에서는 선형화마다
한 번) 계산한다는 뜻이다.

### 2. 언제 실제로 통하는가? 두 조건

- **$(A,B)$의 안정화 가능성(stabilizability)**: $A$의 모든 불안정 모드가 $u$의 영향을
  받아야 한다 ([[02-foundations/linear-algebra|1페이지 제어 섹션]]의 가제어성 랭크 검정의
  더 약한 충분 버전). 아니면 리카티든 뭐든 어떤 피드백도 안정화할 수 없다.
- **$(A,Q^{1/2})$의 검출 가능성(detectability)**: 모든 불안정 모드가 비용에 나타나야
  한다 — 아니면 최적화기가 조용히 발산하는 모드를 "신경 안 쓰는" 것이 허용되어, 최적
  비용의 제어기가 안정화 제어기가 아니게 된다.

이 둘이 "LQR은 안정성이 보장된다"의 작은 글씨다. 비선형 시스템을 선형화해 LQR을 쓰는
논문은 두 조건을 *선형화 지점에서만* 상속한다.

### 3. Q와 R이 거동에 하는 일 — 읽기용 예제

이중 적분기(카트): $x = (p, v)$, $u$ = 힘. $Q = \mathrm{diag}(q_p, 0)$, $R = r$로 두면:

- **$q_p/r$ 큼** ("상태 비싸고 제어 쌈"): 공격적 이득 — 빠른 위치 복귀, 큰 힘 스파이크,
  잡음 증폭 증가, 액추에이터 포화 위험 (LQR 자신은 포화를 모델링하지 않는다 — 그건
  [[04-robotics/mpc|MPC]]의 일).
- **$q_p/r$ 작음** ("제어 비쌈"): 온화한 이득, 느린 복귀, 매끄러운 입력.
- 중요한 건 *비율*뿐이고($Q,R$을 함께 스케일하면 비용만 변하고 $K$는 불변), 속도 대
  위치의 가중이 응답의 *감쇠* 대 *강성*을 조형한다 — 실험 섹션의 "settling time에 맞춰
  Q/R을 튜닝했다"가 쓰는 손잡이 어휘다.

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

- [ ] LQR 문제 설정과 해의 형태($u = -Kx$, $K = R^{-1}B^\top P$)를 말할 수 있다
- [ ] 안정화 가능성·검출 가능성이 각각 무엇을 보장하는 조건인지 말할 수 있다
- [ ] $Q/R$ 비율이 이득·응답·포화 위험을 어떻게 바꾸는지 예제로 말할 수 있다
- [ ] 분리 원리와 그 취약성(LQG 무여유), LQR이 MPC·RL의 기준점인 이유를 말할 수 있다
