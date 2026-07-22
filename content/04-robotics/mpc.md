---
title: "5. MPC"
tags: [robotics, control, resource]
---

**Key reference** — Mayne, Rawlings, Rao & Scokaert, *Constrained model predictive control: Stability and optimality*, Automatica 2000 · [DOI](https://doi.org/10.1016/S0005-1098(99)00214-9)

## English

**What it is**: **Model Predictive Control** solves, at every control step, a finite-horizon
optimal control problem from the current state, applies only the first input, and re-solves
at the next step (receding horizon). With linear dynamics and quadratic cost it is a
convex QP — written out fully in [[02-foundations/optimization|4. Optimization §5]] —
solvable in milliseconds; constraints on inputs and states are handled *natively*, which is
MPC's whole advantage over [[04-robotics/lqr-lqg|LQR]].

**The Mayne et al. 2000 survey** is the field's canonical reference: it settled *when MPC
is stable* — the roles of the terminal cost, terminal constraint set, and horizon length —
turning a practical heuristic into a theory. Read it after the optimization page's example;
skim §2–3 for the formulation and stability conditions rather than every proof.

**Where it meets learning** (this wiki's angle):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]] is MPC with a *learned* model and CEM solver;
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]'s receding-horizon action
chunks borrow MPC's structure; learned-dynamics MPC for excavators is an active
construction-robotics direction ([[05-construction-robotics/index|section 5]]).

## 한국어

**무엇인가**: **모델 예측 제어**는 매 제어 주기마다 현재 상태에서 유한 지평 최적 제어
문제를 풀고, 첫 입력만 적용한 뒤, 다음 주기에 다시 푼다(receding horizon). 선형 동역학과
이차 비용이면 볼록 QP가 되고 — [[02-foundations/optimization|4. 최적화 §5]]에 완전히 써
놓았다 — 수 밀리초에 풀린다; 입력·상태 제약을 *태생적으로* 다루는 것이
[[04-robotics/lqr-lqg|LQR]] 대비 MPC의 존재 이유다.

**Mayne et al. 2000 서베이**는 이 분야의 정전이다: *MPC가 언제 안정한가* — 종단 비용,
종단 제약 집합, 지평 길이의 역할 — 를 정리해 실용적 휴리스틱을 이론으로 만들었다.
최적화 페이지의 예제를 본 뒤에 읽되, 모든 증명보다는 §2~3의 정식화와 안정성 조건을
훑는 것을 권한다.

**학습과 만나는 지점** (이 위키의 관심사):
[[01-canonical-papers/notes/5-world-models/planet|PlaNet]]은 *학습된* 모델과 CEM 솔버의 MPC이고,
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]의 receding-horizon 행동
청크는 MPC의 구조를 빌린 것이며, 굴착기의 학습 동역학 MPC는 건설로봇의 활발한 연구
방향이다 ([[05-construction-robotics/index|5번 섹션]]).

### 연결

- 기초: [[02-foundations/optimization|최적화]] (QP, KKT), [[02-foundations/linear-algebra|선형대수]]
- 이전: [[04-robotics/lqr-lqg|LQR/LQG]] · 다음: [[04-robotics/convex-mpc-legged|보행 로봇의 convex MPC]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] receding horizon 절차(풀고→첫 입력→재풀이)를 말할 수 있다
- [ ] LQR 대비 MPC의 존재 이유(제약의 태생적 처리)를 말할 수 있다
- [ ] Mayne 2000이 정리한 안정성 재료(종단 비용·종단 제약·지평)를 개요 수준에서 말할 수 있다
- [ ] PlaNet·Diffusion Policy가 MPC의 구조를 빌린 지점을 말할 수 있다
