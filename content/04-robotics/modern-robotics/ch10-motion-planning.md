---
title: "MR Ch.10 — Motion Planning"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.10** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

## English

**Core question**: how do we find a collision-free path through C-space?

- **The framing**: obstacles in the workspace become **C-space obstacles** — planning is
  navigation in [[04-robotics/modern-robotics/ch02-configuration-space|configuration
  space]], where the robot is a point.
- **Grid/graph search**: discretize C-space, run **A\*** (Dijkstra + admissible heuristic)
  — complete and optimal on the grid, but the grid explodes exponentially with dof.
- **Sampling-based planning** — the high-dof workhorses:
  - **RRT**: grow a tree by sampling random configurations and extending toward them;
    RRT\* adds rewiring for asymptotic optimality.
  - **PRM**: sample many configurations, connect neighbors into a roadmap, then query.
  - Guarantee: **probabilistic completeness** — if a solution exists, you'll find it
    eventually (no promise about when, or how ugly; hence post-smoothing).
- Nonholonomic/kinodynamic planning: sample *controls* instead of configurations when
  velocity constraints bind (cars, [[04-robotics/convex-mpc-legged|legged machines]]).

**Wiki connections**: the classical layer that learned policies increasingly *absorb* —
a [[01-canonical-papers/notes/4-vla/pi0|VLA]] implicitly plans in its forward pass, and
[[01-canonical-papers/notes/5-world-models/planet|latent-space CEM]] is planning with a learned model;
on real sites, sampling planners still provide the safety-checkable backbone that learned
proposals get filtered through.

## 한국어

**핵심 질문**: C-space를 통과하는 충돌 없는 경로를 어떻게 찾는가?

- **프레이밍**: 작업 공간의 장애물이 **C-space 장애물**이 된다 — 계획은
  [[04-robotics/modern-robotics/ch02-configuration-space|컨피규레이션 공간]]에서의 항해이고,
  거기서 로봇은 점이다.
- **격자/그래프 탐색**: C-space를 이산화하고 **A\***(다익스트라 + 허용 가능 휴리스틱)를
  돌린다 — 격자 위에서 완전하고 최적이지만, 격자가 자유도에 지수적으로 폭발한다.
- **샘플링 기반 계획** — 고자유도의 주력:
  - **RRT**: 무작위 컨피규레이션을 샘플링하고 그쪽으로 확장하며 트리를 키운다; RRT\*는
    재배선을 더해 점근적 최적성을 얻는다.
  - **PRM**: 많이 샘플링해 이웃을 로드맵으로 연결한 뒤 질의한다.
  - 보장: **확률적 완전성** — 해가 존재하면 언젠가는 찾는다 (언제인지, 얼마나 못생겼는지는
    약속 없음; 그래서 사후 평활화를 한다).
- 비홀로노믹/키노다이나믹 계획: 속도 제약이 물 때는 컨피규레이션 대신 *제어*를
  샘플링한다(자동차, [[04-robotics/convex-mpc-legged|보행 기계]]).

**위키 연결**: 학습된 정책이 점점 *흡수*하는 고전 계층 —
[[01-canonical-papers/notes/4-vla/pi0|VLA]]는 forward pass 안에서 암묵적으로 계획하고,
[[01-canonical-papers/notes/5-world-models/planet|잠재 공간 CEM]]은 학습된 모델로 하는 계획이다;
실제 현장에서는 샘플링 플래너가 여전히 학습된 제안을 거르는 안전 검증 가능한 척추를
제공한다.
