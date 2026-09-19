---
title: "MR Ch.10 — Motion Planning"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.10** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the C-space idea from [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]] and the basics of graph search (BFS/Dijkstra).
> [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 C-space 개념과 그래프 탐색(BFS/다익스트라)의 기초가 필요하다.

## English

**Core question**: how do we find a collision-free path through C-space?

- **The framing**: obstacles in the workspace become **C-space obstacles** — planning is
  navigation in [[04-robotics/modern-robotics/ch02-configuration-space|configuration space]], where the robot is a point.
- **Grid/graph search**: discretize C-space, run **A\*** (Dijkstra + admissible heuristic, i.e. a cost-to-go guess that never overestimates the true remaining cost)
  — complete on the grid, and optimal there given an admissible heuristic plus the revisit
  bookkeeping a closed set needs (see [[04-robotics/planning-decision-making|4. Planning & Decision-Making]] §3; the correctness proof and an implementation are [[02-foundations/algorithms/graph-algorithms|11.6 §6]]), but the grid explodes exponentially with dof.
- **Sampling-based planning** — the high-dof workhorses:
  - **RRT**: grow a tree by sampling random configurations and extending toward them;
    RRT\* adds rewiring for asymptotic optimality.
  - **PRM**: sample many configurations, connect neighbors into a roadmap, then query.
  - Guarantee: **probabilistic completeness** — the probability of finding an existing solution
    tends to one as sampling continues. *Resolution* completeness is a different, grid-relative guarantee: it finds a solution if one exists at the chosen discretization resolution (MR §10.1), so a passage narrower than the grid can be missed. Both are weaker than full completeness. No promise about when, or how ugly; hence
    post-smoothing.
- Nonholonomic/kinodynamic planning: keep sampling configurations or states, but replace the straight-line local planner with one that respects the constraints — integrate a discrete set of controls, or use Reeds–Shepp curves for cars (MR §10.5.1.3) — when
  velocity constraints bind (cars, [[04-robotics/convex-mpc-legged|legged machines]]).

> [!example] Worked example · 계산 예제
> **How big is the grid?** Discretize each revolute joint's full $360°$ range at $10°$ resolution: $36$ values per joint. A grid planner must, in the worst case, collision-check every cell.
> - **2-DOF arm:** $36^2 = 1{,}296$ cells. Trivial.
> - **6-DOF arm:** $36^6 \approx 2.18 \times 10^9$ cells — $36^4 \approx 1.7$ million times more for four extra joints.
> - At $1$ µs per collision check that is about $36$ minutes; at a more realistic $1$ ms, about $25$ days. And $10°$ is coarse: halve the step and the 6-DOF count grows $2^6 = 64\times$.
>
> The homework's intractability claim *is* $36^6\approx 2.18\times 10^9$ at $1\,\mathrm{ms}\approx 25$ days. Probabilistic completeness is not a time bound: a planner can run forever on a problem that has a solution. An RRT path that puts P2's tip on the panel has not checked $F_n$ on the P3 wall.
>
> **The fix.** Sampling planners never build the grid. One RRT step: sample a random $q_\text{rand}$, find the nearest tree node $q_\text{near}$, move a fixed step from $q_\text{near}$ toward $q_\text{rand}$ to get $q_\text{new}$, and add it if the segment is collision-free. The cost is paid per sample, not per cell.

**Wiki connections**: the classical layer that learned policies increasingly *absorb* —
a [[01-canonical-papers/notes/4-vla/pi0|VLA]] implicitly plans in its forward pass, and
[[01-canonical-papers/notes/5-world-models/planet|latent-space CEM]] is planning with a learned model;
on real sites, sampling planners still provide the safety-checkable backbone that learned
proposals get filtered through.

### Problem set · 과제

Tier C. Claim-reading. Running task: plan **P2** to the panel ([[02-foundations/lab-plants|0.6]]).

1. **Claim.** Which number is the claim that a $10^\circ$ grid on a 6-dof arm is intractable?
2. **Falsify.** What observation would falsify treating probabilistic completeness as a *time* guarantee?
3. **Task.** An RRT path that puts P2's tip on the panel: what has not been checked about the wall?

> [!tip]- Solutions
> 1. $36^6\approx2.18\times10^9$ cells (and $25$ days at $1\,\mathrm{ms/check}$) — that count *is* the intractability claim.
> 2. A solution exists, the planner eventually finds it, but only after an unbounded wait. Completeness says “probability $\to 1$”, not “by the control period”.
> 3. Collision-free in $\mathcal{C}$ is not $F_n$, $\mu$, or P3 stiffness. Sampling did not promise contact force (or when the path is found).

### Continue beyond this chapter

[[04-robotics/planning-decision-making|Planning & Decision-Making]] connects this chapter to A*, sampling-based planning, trajectory optimization, TAMP, uncertainty, MPC, and learned planners.

## 한국어

**핵심 질문**: C-space를 통과하는 충돌 없는 경로를 어떻게 찾는가?

- **프레이밍**: 작업 영역(workspace)의 장애물이 **C-space 장애물**이 된다 — 계획은
  [[04-robotics/modern-robotics/ch02-configuration-space|컨피규레이션 공간]]에서의 항해이고,
  거기서 로봇은 점이다.
- **격자/그래프 탐색**: C-space를 이산화하고 **A\***(다익스트라 + 허용 가능 휴리스틱, 즉 실제 남은 비용을 절대 과대추정하지 않는 비용 추정)를
  돌린다 — 격자 위에서 완전하고, 허용 가능 휴리스틱에 더해 닫힌 집합이 요구하는 재방문 처리까지 갖추면 최적이다([[04-robotics/planning-decision-making|4. 계획과 의사결정]] §3. 정확성 증명과 구현은 [[02-foundations/algorithms/graph-algorithms|11.6 §6]]). 다만 격자가 자유도에 지수적으로 폭발한다.
- **샘플링 기반 계획** — 고자유도의 주력:
  - **RRT**: 무작위 컨피규레이션을 샘플링하고 그쪽으로 확장하며 트리를 키운다; RRT\*는
    재배선을 더해 점근적 최적성을 얻는다.
  - **PRM**: 많이 샘플링해 이웃을 로드맵으로 연결한 뒤 질의한다.
  - 보장: **확률적 완전성** — 표본을 계속 뽑으면 존재하는 해를 찾을 확률이 1로 간다. *해상도* 완전성은 격자에 상대적인 다른 보장이다: 선택한 이산화 해상도에서 해가 존재하면 찾는다(MR §10.1). 그래서 격자보다 좁은 통로는 놓칠 수 있다. 둘 다 완전한 완전성보다 약하다. (언제인지, 얼마나 못생겼는지는
    약속 없음; 그래서 사후 평활화를 한다).
- 비홀로노믹/키노다이나믹 계획: 속도 제약이 물 때도 컨피규레이션이나 상태는 계속 샘플링하되, 직선 국소 계획기를 제약을 지키는 것으로 바꾼다 — 이산 제어 집합을 적분하거나 자동차라면 Reeds–Shepp 곡선을 쓴다(MR §10.5.1.3)(자동차, [[04-robotics/convex-mpc-legged|보행 기계]]).

> [!example] 계산 예제 · Worked example
> **격자는 얼마나 큰가?** 회전 관절마다 전체 $360°$ 범위를 $10°$ 해상도로 이산화하면 관절당 $36$개 값이다. 격자 계획기는 최악의 경우 모든 칸을 충돌 검사해야 한다.
> - **2자유도 팔:** $36^2 = 1{,}296$칸. 사소하다.
> - **6자유도 팔:** $36^6 \approx 2.18 \times 10^9$칸 — 관절 4개를 더했을 뿐인데 $36^4 \approx 170$만 배다.
> - 충돌 검사 1회에 $1$ µs면 약 $36$분, 더 현실적인 $1$ ms면 약 $25$일이다. 게다가 $10°$는 거칠다: 간격을 절반으로 줄이면 6자유도 칸 수는 $2^6 = 64$배가 된다.
>
> **해결책.** 샘플링 계획기는 격자를 만들지 않는다. RRT 한 스텝: 무작위 $q_\text{rand}$를 뽑고, 트리에서 가장 가까운 노드 $q_\text{near}$를 찾고, $q_\text{near}$에서 $q_\text{rand}$ 쪽으로 고정 보폭만큼 움직여 $q_\text{new}$를 얻은 뒤, 그 선분에 충돌이 없으면 트리에 더한다. 비용은 칸마다가 아니라 표본마다 든다.

**위키 연결**: 학습된 정책이 점점 *흡수*하는 고전 계층 —
[[01-canonical-papers/notes/4-vla/pi0|VLA]]는 forward pass 안에서 암묵적으로 계획하고,
[[01-canonical-papers/notes/5-world-models/planet|잠재 공간 CEM]]은 학습된 모델로 하는 계획이다;
실제 현장에서는 샘플링 플래너가 여전히 학습된 제안을 거르는 안전 검증 가능한 척추를
제공한다.

### 이 장 너머로

[[04-robotics/planning-decision-making|계획과 의사결정]]이 이 장을 A*, 표본 기반 계획, 궤적 최적화, TAMP, 불확실성, MPC, 학습된 계획기로 이어 준다.

### Self-check · 스스로 점검

1. Discretize a 7-dof arm's C-space at 100 cells per axis — how many cells? What does that explain about sampling-based planning? · 7자유도 팔의 C-space를 축당 100칸으로 이산화하면 격자 크기는? 이것이 샘플링 기반 계획의 존재 이유를 어떻게 설명하는가?
2. What does RRT's "probabilistic completeness" guarantee, and what does it not? · RRT의 "확률적 완전성"이 보장하는 것과 보장하지 않는 것은?
3. Why can't you run plain RRT on a car? · 자동차에 일반 RRT를 그대로 쓰면 안 되는 이유는?

> [!tip]- Answers · 정답
> 1. $100^7 = 10^{14}$ cells. Grid search explodes exponentially in dof, so beyond a few dimensions only sampling is tractable — you cannot even enumerate the space, let alone search it. · 격자 탐색은 자유도에 지수적으로 폭발하므로 고차원에서는 샘플링만이 실용적이다.
> 2. Guaranteed: if a solution exists (under the method's assumptions), the probability of finding it tends to 1 as computation grows. Not guaranteed: *when* it is found, or the quality of the path — plain RRT paths are typically far from optimal, which is what RRT\* and post-smoothing address. · 언제 찾는지와 경로 품질은 보장하지 않는다.
> 3. Its extension step connects two configurations with a straight line in C-space, but a nonholonomic vehicle cannot execute sideways motion — the "edge" is not a feasible trajectory. Keep sampling states, but extend with a constraint-respecting local planner — integrate discretized controls or use Reeds–Shepp curves (kinodynamic planning). · 비홀로노믹 제약 때문에 직선 확장이 실행 불가능한 운동일 수 있다 — 상태 샘플링은 그대로 두고, 이산 제어를 적분하거나 Reeds–Shepp 곡선을 쓰는 제약 준수 국소 계획기로 확장해야 한다. ([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|ch.13]])

### 과제 · Problem set

Tier C. 주장 읽기. 관통 과제: [[02-foundations/lab-plants|0.6]]의 **P2**를 패널까지 계획.

1. **주장.** $10^\circ$ 격자 6자유도 팔이 감당 안 된다는 주장은 어느 숫자인가?
2. **반증.** 확률적 완전성을 *시간* 보장으로 읽는 주장을 깨는 관찰은?
3. **과제.** P2 말단을 패널에 두는 RRT 경로가 벽에 대해 검사하지 않은 것은?

> [!tip]- 정답 · Solutions
> 1. $36^6\approx2.18\times10^9$칸(그리고 $1\,\mathrm{ms}$면 약 $25$일) — 그 개수가 곧 비실용 주장이다.
> 2. 해는 있고 결국 찾지만 대기 시간은 무계. 완전성은 “확률 $\to 1$”이지 “제어 주기 안에”가 아니다.
> 3. $\mathcal{C}$에서 충돌 없음은 $F_n$, $\mu$, P3 강성이 아니다. 샘플링은 접촉력을 약속하지 않는다.
