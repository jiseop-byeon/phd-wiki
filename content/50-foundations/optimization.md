---
title: Optimization
tags: [foundations]
---

## English

Optimization is the shared language of this wiki: training a network ([[canonical-papers/notes/adam|Adam]]),
solving MPC, planning a trajectory, and allocating construction tasks are all instances of
"minimize an objective subject to constraints."

### 1. Anatomy of a problem

$$\min_{x \in \mathbb{R}^n} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; h_j(x) = 0$$

Decision variables, objective, inequality/equality constraints. Every modeling decision is
about *what is a variable, what is a constraint, what is the objective* — formulation is
half the work.

### 2. Convexity — the great divide

A problem is convex if $f$ and the feasible set are convex. Convex ⇒ every local minimum is
global, and efficient reliable solvers exist. The practical skill is *recognizing and
preserving convexity* (LP, QP, and many MPC formulations are convex by design; neural
network training is deliberately non-convex).

### 3. Unconstrained methods

- **Gradient descent**: $x_{k+1} = x_k - \alpha \nabla f(x_k)$ — cheap steps, slow on
  ill-conditioned problems. Stochastic version (SGD) powers all of deep learning.
- **Newton's method**: use curvature $\nabla^2 f$ — quadratic convergence near the optimum,
  expensive per step. Quasi-Newton (BFGS) approximates the Hessian.
- Line search / trust region decide the step size.
- Deep learning connection: [[canonical-papers/notes/adam|Adam]] ≈ diagonal-curvature
  approximation with momentum.

### 4. Constrained methods

- **Lagrangian**: $\mathcal{L}(x,\lambda,\nu) = f + \sum \lambda_i g_i + \sum \nu_j h_j$.
- **KKT conditions** — the first-order optimality certificate: stationarity, primal/dual
  feasibility, complementary slackness. Duality gives bounds and sensitivity (shadow prices).
- Algorithms: active-set, penalty/barrier, **interior-point** (the workhorse of modern LP/QP),
  **SQP** for nonlinear programs — SQP and interior-point are what real-time MPC solvers run.

### 5. Problem classes that matter for robotics

| Class | Form | Where it appears |
|---|---|---|
| LP | linear $f$, linear constraints | resource allocation, scheduling relaxations |
| QP | quadratic $f$, linear constraints | **linear MPC**, trajectory smoothing, inverse dynamics |
| NLP | nonlinear | nonlinear MPC, trajectory optimization, calibration |
| MIP | integer variables | task assignment, sequencing construction activities |
| Global | non-convex, certified | rarely needed; branch-and-bound underneath MIP |

### 6. Reading this wiki through optimization

- MPC = a QP/NLP re-solved every control step ([[20-robotics/index|control track]])
- Network training = stochastic non-convex optimization ([[canonical-papers/notes/adam|Adam]], [[canonical-papers/notes/batch-norm|BatchNorm]] reshapes the landscape)
- [[canonical-papers/notes/lora|LoRA]] = constraining the search space to a low-rank manifold
- Diffusion training = minimizing a variational bound (see [[canonical-papers/canonical-list|section 6]])

## 한국어

최적화는 이 위키의 공용 언어다: 네트워크 학습([[canonical-papers/notes/adam|Adam]]), MPC 풀기,
궤적 계획, 건설 작업 할당 모두 "제약 조건 아래 목적함수 최소화"의 사례들이다.

### 1. 문제의 구조

$$\min_{x \in \mathbb{R}^n} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \; h_j(x) = 0$$

결정 변수, 목적함수, 부등식/등식 제약. 모델링의 모든 결정은 *무엇이 변수이고, 무엇이 제약이고,
무엇이 목적인가*에 관한 것이다 — 정식화가 일의 절반이다.

### 2. 볼록성 — 결정적 분기점

$f$와 가능 영역이 볼록하면 볼록 문제다. 볼록 ⇒ 모든 지역 최솟값이 전역 최솟값이고, 효율적이고
신뢰할 수 있는 솔버가 존재한다. 실전 기술은 *볼록성을 알아보고 보존하는 것*이다
(LP·QP와 많은 MPC 정식화는 의도적으로 볼록하게 설계된다; 신경망 학습은 의도적으로 비볼록이다).

### 3. 무제약 방법

- **경사 하강**: $x_{k+1} = x_k - \alpha \nabla f(x_k)$ — 스텝이 싸지만 조건수 나쁜 문제에서 느리다.
  확률적 버전(SGD)이 딥러닝 전체를 굴린다.
- **뉴턴법**: 곡률 $\nabla^2 f$ 사용 — 최적점 근처에서 이차 수렴하지만 스텝이 비싸다.
  준뉴턴(BFGS)은 헤시안을 근사한다.
- 스텝 크기는 line search / trust region이 결정.
- 딥러닝 연결: [[canonical-papers/notes/adam|Adam]] ≈ 모멘텀을 더한 대각 곡률 근사.

### 4. 제약 방법

- **라그랑지안**: $\mathcal{L}(x,\lambda,\nu) = f + \sum \lambda_i g_i + \sum \nu_j h_j$
- **KKT 조건** — 1차 최적성의 증명서: 정상성, 원/쌍대 가능성, 상보 여유성.
  쌍대성은 하한과 민감도(잠재 가격)를 준다.
- 알고리즘: active-set, 페널티/배리어, **내부점법**(현대 LP/QP의 주력), 비선형 문제의 **SQP**
  — 실시간 MPC 솔버가 돌리는 것이 바로 SQP와 내부점법이다.

### 5. 로보틱스에 중요한 문제 부류

| 부류 | 형태 | 등장하는 곳 |
|---|---|---|
| LP | 선형 $f$, 선형 제약 | 자원 할당, 스케줄링 완화 문제 |
| QP | 이차 $f$, 선형 제약 | **선형 MPC**, 궤적 평활화, 역동역학 |
| NLP | 비선형 | 비선형 MPC, 궤적 최적화, 캘리브레이션 |
| MIP | 정수 변수 | 작업 배정, 건설 공정 순서 결정 |
| 전역 최적화 | 비볼록, 보증 필요 | 드물게 필요; MIP 밑바닥의 branch-and-bound |

### 6. 최적화의 눈으로 이 위키 읽기

- MPC = 제어 주기마다 다시 푸는 QP/NLP ([[20-robotics/index|제어 트랙]])
- 네트워크 학습 = 확률적 비볼록 최적화 ([[canonical-papers/notes/adam|Adam]], [[canonical-papers/notes/batch-norm|BatchNorm]]은 지형을 다듬는 장치)
- [[canonical-papers/notes/lora|LoRA]] = 탐색 공간을 저랭크 다양체로 제약하는 것
- 디퓨전 학습 = 변분 하한의 최소화 ([[canonical-papers/canonical-list|6번 섹션]])
