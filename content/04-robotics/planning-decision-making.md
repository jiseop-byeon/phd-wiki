---
title: 8. Planning & Decision-Making
tags: [robotics, planning, decision-making]
---

## English

Planning asks how a robot should choose a feasible sequence of future states and actions to reach a goal. The difficulty is not merely finding a short path: robot geometry, dynamics, contact, uncertainty, computation time, and changing observations constrain what can actually be executed.

> [!info] Depth target
> Distinguish search, motion planning, trajectory optimization, task planning, policy learning, and control; read feasibility and optimality claims; and identify whether a generated trajectory is collision-free, dynamically feasible, and evaluated in closed loop.

> [!note] Prerequisites
> [[02-foundations/optimization|Optimization]] · [[02-foundations/rl-basics|RL Basics]] · [[04-robotics/modern-robotics/ch02-configuration-space|Configuration Space]] · [[04-robotics/modern-robotics/ch10-motion-planning|Motion Planning]] · [[04-robotics/mpc|MPC]]

### 1. Plan, path, trajectory, policy, controller

| Term | Meaning |
|---|---|
| Plan | Proposed future sequence of decisions or actions |
| Path | Geometric curve without timing |
| Trajectory | Time-indexed state, velocity, and often input |
| Policy | Rule mapping available information to an action |
| Controller | Feedback system that tracks a reference or regulates behavior |

A planner may produce a path that a trajectory generator times and a controller tracks. In learned systems, a policy can collapse these boundaries, but the physical requirements do not disappear.

### 2. Spaces and constraints

- **Workspace:** physical positions occupied by the robot and obstacles.
- **Configuration space:** robot configurations; obstacles become forbidden regions.
- **State space:** configuration plus variables such as velocity.
- **Action/input space:** commands available to the system.
- **Task space:** variables directly tied to the task, such as end-effector pose.

Collision-free in workspace does not imply joint, torque, velocity, stability, or contact feasibility.

### 3. Graph search

For A*,

$$f(n)=g(n)+h(n)$$

- $g(n)$: known cost from the start to node $n$.
- $h(n)$: estimated cost from $n$ to the goal.
- $f(n)$: priority used for expansion.

Dijkstra uses no informative heuristic. A* is optimal on a graph under the appropriate admissibility/consistency conditions; this theorem does not guarantee that a discretized graph represents every feasible continuous robot motion.

### 4. Worked example: what a heuristic changes

Suppose two frontier nodes have $(g,h)=(6,3)$ and $(4,6)$. Their A* priorities are $9$ and $10$, so the first is expanded even though it has a larger cost-to-come. The heuristic directs effort toward states estimated to be closer to the goal. An overoptimistic heuristic may be slow but admissible; an overestimating heuristic can lose the usual optimality guarantee.

### 5. Major method families

| Family | Representative ideas | Best read as |
|---|---|---|
| Graph search | BFS, Dijkstra, A* | Search over an explicit discretization |
| Sampling based | PRM, RRT, RRT* | Explore high-dimensional free space through samples |
| Trajectory optimization | shooting, transcription, collocation | Optimize states/inputs under constraints |
| Task planning | symbolic operators and goals | Choose discrete actions |
| TAMP | task and motion planning | Couple symbolic choices to geometric feasibility |
| Uncertain planning | MDP, POMDP, belief space | Choose actions while accounting for uncertain state/outcomes |

**Probabilistic completeness** means the probability of finding a solution approaches one with increasing computation when a robust solution exists under the method's assumptions. It does not mean fast success. **Asymptotic optimality** concerns convergence toward an optimum with increasing samples, not the quality available under a real-time budget.

### 6. Trajectory optimization and MPC

A common formulation is

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. dynamics, bounds, and collision constraints.}$$

- **Given:** initial state, model, goal, constraints, and cost.
- **Optimized:** state and/or input sequence.
- **Runtime:** offline planning or repeated online as MPC.
- **Caveat:** nonlinear dynamics and obstacle constraints usually create local, initialization-sensitive problems.

Direct shooting optimizes controls and simulates states. Direct transcription treats states and controls as variables. Collocation enforces dynamics at selected points. None automatically proves global optimality in a nonconvex robot problem.

### 7. Task planning, uncertainty, and replanning

A symbolic instruction such as `pick(block)` may be logically valid yet geometrically impossible because no collision-free grasp exists. TAMP alternates or jointly reasons over discrete actions and continuous feasibility.

With partial observability, the planning state becomes a belief. A POMDP distinguishes hidden state, observation, action, transition, observation model, and reward. Exact belief-space planning is often intractable, so papers use approximations, receding horizons, learned values, or contingency policies.

Online replanning incorporates new observations. Reported replanning frequency is not enough: compare it with perception latency, scene dynamics, and controller bandwidth.

### 8. Learning-based planning

Learned components may provide a heuristic, cost, dynamics/world model, value function, proposal distribution, trajectory generator, or entire policy. A VLA that outputs actions is usually a policy; a world model that rolls out futures supports planning only when a selection or optimization procedure uses those futures.

> [!warning] Reading the claim
> “Generates plausible trajectories” does not imply collision-free, dynamically feasible, stable, or safe execution. Check explicit constraints, downstream controllers, replanning, and closed-loop robot results.

### 9. Evaluation and failure modes

Check success rate, collision rate, path/trajectory cost, planning and execution time, optimality gap, constraint violation, replanning rate, robustness to map/state error, and closed-loop execution. Separate planning failure, perception failure, tracking failure, and hardware failure.

### After reading

You should be able to:

- distinguish plan, path, trajectory, policy, and controller;
- interpret $g$, $h$, and $f$ in A*;
- explain probabilistic completeness without calling it a speed guarantee;
- compare graph search, sampling, and trajectory optimization;
- explain why TAMP must test geometric feasibility;
- identify what a learned trajectory generator does not guarantee.

### Self-check

1. Why can a collision-free path be dynamically infeasible?
2. What is lost when planning only in workspace rather than configuration space?
3. Why can trajectory optimization fail even when a feasible trajectory exists?
4. What evidence would support a “real-time closed-loop planner” claim?

> [!tip]- Answers
> 1. It may require impossible velocity, acceleration, torque, contact, or timing. 2. Robot geometry, joint limits, and multiple configurations for the same task pose. 3. The problem can be nonconvex and sensitive to initialization. 4. End-to-end latency distributions on specified hardware, execution with disturbances/dynamic obstacles, constraint violations and failures—not planner compute time alone.

### Sources

- [Modern Robotics, Chapter 10](http://modernrobotics.org)
- [MIT Underactuated Robotics](https://underactuated.csail.mit.edu/)
- [OMPL: planning concepts](https://ompl.kavrakilab.org/)

## 한국어

Planning은 목표까지 가는 실행 가능한 미래 상태와 행동을 선택하는 문제다. 짧은 선만 찾는 것이 아니라 로봇 형상, 동역학, 접촉, 불확실성, 계산 시간과 새 관측을 함께 고려해야 한다.

**Path**는 시간 없는 기하학적 곡선, **trajectory**는 시간에 따른 상태·입력, **plan**은 미래 결정의 제안, **policy**는 현재 정보에서 행동으로의 규칙, **controller**는 feedback으로 실행을 유지하는 시스템이다. 학습 정책이 이 경계를 합칠 수 있지만 물리적 제약이 사라지는 것은 아니다.

A*의 $f(n)=g(n)+h(n)$에서 $g$는 지금까지의 비용, $h$는 남은 비용의 추정이다. Probabilistic completeness는 시간이 늘면 해를 찾을 확률이 1에 가까워진다는 성질이지 빠르다는 보장이 아니다. Asymptotic optimality도 무한히 많은 표본에서의 성질이지 실시간 예산에서 좋은 답을 보장하지 않는다.

Graph search는 명시적 이산 그래프, PRM/RRT는 표본으로 고차원 자유공간, trajectory optimization은 동역학·제약 아래 상태와 입력을 최적화한다. Task planning은 이산 행동을, TAMP는 그 행동의 기하학적 실행 가능성까지 다룬다. POMDP와 belief-space planning은 상태가 불확실할 때의 의사결정을 다룬다.

생성 모델이나 VLA가 trajectory/action을 출력해도 자동으로 충돌 회피, 동역학 가능성, 안정성과 안전이 보장되는 것은 아니다. 논문에서 명시적 제약, downstream controller, replanning, closed-loop 실행과 실패 분류를 확인해야 한다.

위 영어 절의 After reading과 Self-check로 search·planning·optimization·policy·control의 역할을 구분하고 논문의 실시간성·완전성·안전성 주장을 정확히 읽을 수 있는지 점검하라.
