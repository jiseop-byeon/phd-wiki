---
title: 4. Planning & Decision-Making
tags: [robotics, planning, decision-making]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

*Group C, and the only page in it. Stands on the [[04-robotics/modern-robotics/index|Modern Robotics chapters]], [[04-robotics/mpc|7. MPC]] and the optimization and RL pages.
Choosing an executable future; group I specialises this for unstructured environments.*

Planning asks how a robot should choose a feasible sequence of future states and actions to reach a goal. The difficulty is not merely finding a short path: robot geometry, dynamics, contact, uncertainty, computation time, and changing observations constrain what can actually be executed.

> [!info] Depth target
> Distinguish search, motion planning, trajectory optimization, task planning, policy learning, and control; read feasibility and optimality claims; and identify whether a generated trajectory is collision-free, dynamically feasible, and evaluated in closed loop.

> [!note] Prerequisites
> [[02-foundations/optimization|Optimization]] · [[02-foundations/rl-basics|RL Basics]] · [[04-robotics/modern-robotics/ch02-configuration-space|Configuration Space]] · [[04-robotics/modern-robotics/ch10-motion-planning|Motion Planning]] — §6 previews [[04-robotics/mpc|MPC]] (track page 7); read it lightly here and return after that page.

### 1. Plan, path, trajectory, policy, controller

| Term | Meaning |
|---|---|
| Plan | Proposed future sequence of decisions or actions |
| Path | Geometric curve without timing |
| Trajectory | Time-indexed state, velocity, and often input |
| Policy | Rule mapping available information to an action |
| Controller | Feedback system that tracks a reference or regulates behavior |

A planner may produce a path that a trajectory generator times ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]] — time scaling, via points, time-optimal scaling) and a controller tracks. When the plan lives in task space but the robot is commanded in joint space, [[04-robotics/modern-robotics/ch06-inverse-kinematics|inverse kinematics (MR ch.6)]] sits between them, and its multimodality is a planning problem in miniature. In learned systems, a policy can collapse these boundaries, but the physical requirements do not disappear.

### 2. Spaces and constraints

- **Workspace:** physical positions occupied by the robot and obstacles.
- **Configuration space:** robot configurations; obstacles become forbidden regions.
- **State space:** configuration plus variables such as velocity.
- **Action/input space:** commands available to the system.
- **Task space:** variables directly tied to the task, such as end-effector pose.

Collision-free in workspace does not imply joint, torque, velocity, stability, or contact feasibility.

**How that space is actually stored.** Two pages of this wiki send you here for occupancy and
cost representations, so they belong in this section rather than in a system paper's
appendix.

- **Occupancy grid** — the map is a grid of cells, each holding the probability that the cell
  is occupied. Updates are done in **log-odds** so that accumulating evidence is an addition
  rather than a multiplication, and to avoid the numerical trouble of probabilities pressed
  against 0 or 1. Note the direction of the remaining hazard: log-odds is *unbounded*, so a
  cell observed occupied a thousand times needs a thousand contrary observations to flip —
  which is why implementations add an explicit **clamping** range (OctoMap's contribution) so
  the map can still adapt when the world changes. A cell reads as *free*, *occupied*, or
  **unknown**, and the third is the one beginners drop: unknown is not free, and the difference is what exploration is about.
- **Inflation** — a planner that treats the robot as a point (the figure above) has to grow
  the obstacles instead. Inflating occupied cells by the robot radius produces a C-space
  obstacle directly on the grid **for a circular robot** — for any other footprint it is an
  approximation, which is why a stack like Nav2 still runs a separate footprint collision
  check. Adding a decaying cost outside that radius produces a margin the planner prefers not
  to enter.
- **Costmap** — an occupancy grid whose cells carry *traversal cost* rather than a binary.
  Cost combines inflation with whatever else the robot should avoid: unknown space, rough
  terrain, one-way regions, keep-out zones. **A costmap is where a policy preference stops
  being a plan and becomes geometry** — this is the representation
  [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy §1]] argues is
  the wrong place to encode a learned affordance, and you need to know what it is to see why.
- **Layered costmaps** — production stacks keep several layers (static map, obstacles, inflation,
  sensor-specific) and compose them, so that clearing a stale obstacle does not erase the map.
- **Frontier** — a boundary cell between *known free* and *unknown*. **Frontier exploration**
  is the classic answer to "where next": drive to the nearest frontier, and the known region
  grows until no frontier remains. Some semantic-navigation methods keep this candidate set
  and let the learned part supply only a *score* over it — [[04-robotics/semantic-language-navigation|19. §3]]'s
  VLFM is exactly that. Others do not: SemExp's learned global policy picks an arbitrary
  long-term goal on the map, which is what its own note means by "goal-oriented rather than
  frontier-based" ([[01-canonical-papers/notes/9-navigation/semexp|SemExp]]). **Which of the
  two a paper does is the thing to identify**, because it decides whether the learned
  component chooses candidates or only ranks them.

> [!warning] Two meanings of "frontier"
> §4 below uses *frontier nodes* for the open list of a graph search — the set of nodes
> discovered but not yet expanded. That is a **different object** from an exploration frontier
> on a map, though not an unrelated one: both name the boundary between what has been explored
> and what has not, one in a graph and one in a grid. Papers rarely disambiguate.

**Global and local.** Navigation stacks split planning in two: a **global planner** searches
the whole costmap for a route (§3–§5), and a **local planner** repeatedly picks the next few
seconds of motion, given the route, the robot's dynamics, and obstacles that appeared since.
The local layer is where the classical names live — *dynamic window* approaches sample
feasible velocity pairs and score them; the **elastic band** deforms a *path* under an
internal contraction force and an external obstacle repulsion, with no notion of time, and
**timed elastic band** is the descendant that adds the time intervals its name refers to; **sampling-based MPC** (the family
[[01-canonical-papers/notes/9-navigation/badgr|BADGR]] uses) samples many action sequences
around a running estimate, rolls each forward through a model, refits the estimate by a
**reward-weighted average** over the samples rather than taking the single best, and executes
its first action. §6 gives the
optimization view of the same layer. In a classical navigation stack the learned component is usually the local layer, with the
global search and the costmap untouched — but not always: learned global planners and learned
search heuristics exist, and the end-to-end line of
[[04-robotics/semantic-language-navigation|19. §3]] replaces the whole stack. **Identify which
layer a paper actually replaced**, because that bounds what its result can claim.

<svg viewBox="0 0 460 216" style="max-width:100%;height:auto" role="img" aria-label="workspace obstacle versus its inflated configuration-space obstacle">
  <g stroke="currentColor" stroke-width="1.3" fill="none"><rect x="25" y="25" width="185" height="150" rx="3"/><rect x="250" y="25" width="185" height="150" rx="3"/></g>
  <g fill="currentColor" opacity="0.22"><rect x="95" y="70" width="45" height="45" rx="2"/><rect x="308" y="53" width="79" height="79" rx="2"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.7"><rect x="308" y="53" width="79" height="79" rx="2"/></g>
  <g fill="currentColor"><circle cx="55" cy="150" r="4"/><circle cx="180" cy="50" r="4"/><circle cx="280" cy="150" r="4"/><circle cx="405" cy="50" r="4"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.8"><path d="M55,150 C80,150 88,124 92,124 C96,124 140,124 146,118 C152,112 150,60 180,50"/><path d="M280,150 C300,150 300,142 302,140 C304,138 395,140 398,134 C401,128 400,62 405,50"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="25" y="18">workspace</text><text x="250" y="18">configuration space</text>
    <text x="117" y="96" font-size="10.5" text-anchor="middle">obstacle</text>
    <text x="347" y="96" font-size="10.5" text-anchor="middle">C-obstacle</text>
    <text x="25" y="193" opacity="0.85">planning shrinks the robot to a single point &#8212;</text>
    <text x="25" y="209" opacity="0.85">the obstacle grows by the robot's shape instead, so a point-path is a safe path</text>
  </g>
</svg>



### 3. Graph search

For A*,

$$f(n)=g(n)+h(n)$$

- $g(n)$: known cost from the start to node $n$.
- $h(n)$: estimated cost from $n$ to the goal.
- $f(n)$: priority used for expansion.

Dijkstra uses no informative heuristic. A* is optimal on a graph under the appropriate admissibility/consistency conditions; this theorem does not guarantee that a discretized graph represents every feasible continuous robot motion.

### 4. Worked example: what a heuristic changes

Suppose two frontier nodes have $(g,h)=(6,3)$ and $(4,6)$. Their A* priorities are $9$ and $10$, so the first is expanded even though it has a larger cost-to-come. The heuristic directs effort toward states estimated to be closer to the goal. An *underestimating* heuristic remains admissible — though if it is too weak, A* gains little speed over Dijkstra; an *overestimating* heuristic can lose the usual optimality guarantee.

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



<svg viewBox="0 0 660 214" style="max-width:100%;height:auto" role="img" aria-label="how a sampling-based planner grows a tree through free space">
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.5"><rect x="30" y="30" width="330" height="140" rx="3"/></g>
  <g fill="currentColor" opacity="0.20"><rect x="150" y="96" width="52" height="40" rx="2"/><rect x="240" y="128" width="52" height="34" rx="2"/></g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.85"><line x1="60" y1="150" x2="85" y2="132"/><line x1="85" y1="132" x2="110" y2="110"/><line x1="110" y1="110" x2="135" y2="88"/><line x1="135" y1="88" x2="170" y2="74"/><line x1="170" y1="74" x2="210" y2="66"/><line x1="210" y1="66" x2="250" y2="80"/><line x1="250" y1="80" x2="290" y2="66"/><line x1="290" y1="66" x2="330" y2="52"/><line x1="85" y1="132" x2="70" y2="108"/><line x1="110" y1="110" x2="96" y2="146"/><line x1="170" y1="74" x2="178" y2="46"/><line x1="210" y1="66" x2="226" y2="40"/><line x1="250" y1="80" x2="258" y2="110"/><line x1="290" y1="66" x2="304" y2="92"/></g>
  <g fill="currentColor" opacity="0.85"><circle cx="85" cy="132" r="2.4"/><circle cx="110" cy="110" r="2.4"/><circle cx="135" cy="88" r="2.4"/><circle cx="170" cy="74" r="2.4"/><circle cx="210" cy="66" r="2.4"/><circle cx="250" cy="80" r="2.4"/><circle cx="290" cy="66" r="2.4"/><circle cx="330" cy="52" r="2.4"/><circle cx="70" cy="108" r="2.4"/><circle cx="96" cy="146" r="2.4"/><circle cx="178" cy="46" r="2.4"/><circle cx="226" cy="40" r="2.4"/><circle cx="258" cy="110" r="2.4"/><circle cx="304" cy="92" r="2.4"/></g>
  <g fill="currentColor"><circle cx="60" cy="150" r="4.5"/><circle cx="330" cy="52" r="4.5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="40" y="166">start</text><text x="306" y="44">goal</text>
    <text x="370" y="62">1. sample a random point</text><text x="370" y="80">2. find the nearest node</text><text x="370" y="98">3. extend toward it if collision-free</text>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle" opacity="0.9">
    <text x="176" y="120">obstacle</text><text x="266" y="149">obstacle</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="190" opacity="0.9">The tree never enumerates the space &#8212; it only ever asks whether one short segment is free.</text>
    <text x="30" y="205" opacity="0.9">That is why it survives high dimensions, and why the path comes out jagged and needs smoothing.</text>
  </g>
</svg>



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

> [!warning] Reading the claim · 핵심 주장 읽는 법
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

> [!tip] Going deeper · 더 깊이
> LaValle's [*Planning Algorithms*](http://lavalle.pl/planning/) is free and is the reference for the sampling-based half; Tedrake's [*Underactuated Robotics*](https://underactuated.csail.mit.edu/) covers the trajectory-optimization half with code you can run.

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

*C군이고, 그 안에 있는 유일한 페이지다. [[04-robotics/modern-robotics/index|MR 챕터 요약]]과 [[04-robotics/mpc|7. MPC]], 그리고 최적화·RL 기초 위에 선다.
실행 가능한 미래를 고르는 문제이며, I군이 이것을 비정형 환경으로 특수화한다.*

Planning은 목표에 도달하기 위한 실행 가능한 미래 상태·행동 시퀀스를 고르는 문제다.
어려움은 짧은 경로 찾기가 아니다: 로봇 형상, 동역학, 접촉, 불확실성, 계산 시간, 변하는
관측이 실제로 실행할 수 있는 것을 제약한다.

> [!info] 깊이 목표
> 탐색·모션 플래닝·궤적 최적화·과제 계획·정책 학습·제어를 구분한다; feasibility와
> optimality 주장을 읽는다; 생성된 궤적이 충돌 없음·동역학적 실행 가능·폐루프 평가인지
> 판별한다.

> [!note] 선수 지식
> [[02-foundations/optimization|최적화]] · [[02-foundations/rl-basics|RL 기초]] · [[04-robotics/modern-robotics/ch02-configuration-space|컨피규레이션 공간]] · [[04-robotics/modern-robotics/ch10-motion-planning|모션 플래닝]] — §6은 [[04-robotics/mpc|MPC]](트랙 7번)를 미리 쓴다; 여기서는 가볍게 읽고 그 페이지 후에 돌아오라.

### 1. Plan, path, trajectory, policy, controller

| 용어 | 의미 |
|---|---|
| Plan | 미래 결정·행동의 제안된 시퀀스 |
| Path | 시간 없는 기하학적 곡선 |
| Trajectory | 시간이 매겨진 상태·속도·(대개) 입력 |
| Policy | 가용 정보를 행동으로 사상하는 규칙 |
| Controller | 기준을 추종하거나 거동을 조절하는 피드백 시스템 |

플래너가 path를 내면 궤적 생성기가 시간을 매기고([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]
— 시간 스케일링, 경유점, 시간 최적 스케일링) 제어기가 추종한다. 계획은 작업 영역에 있는데
로봇은 관절 공간으로 명령받는다면 그 사이에
[[04-robotics/modern-robotics/ch06-inverse-kinematics|역기구학(MR 6장)]]이 앉고, 그 다봉성은
축소판 계획 문제다. 학습 시스템에서는 정책이 이 경계들을 합칠 수 있지만, 물리적 요구 사항이
사라지는 것은 아니다.

### 2. 공간과 제약

- **작업 영역(workspace):** 로봇과 장애물이 차지하는 물리적 위치.
- **컨피규레이션 공간:** 로봇 컨피규레이션; 장애물은 금지 영역이 된다.
- **상태 공간:** 컨피규레이션 + 속도 같은 변수.
- **행동/입력 공간:** 시스템이 쓸 수 있는 명령.
- **과제 공간(task space):** 말단 pose처럼 과제에 직접 묶인 변수.

작업 영역에서 충돌이 없다는 것이 관절·토크·속도·안정성·접촉의 실행 가능성을 함의하지
않는다.

**그 공간을 실제로 저장하는 방법.** 이 위키의 두 페이지가 점유·비용 표현을 위해 여기로
보내므로, 시스템 논문의 부록이 아니라 이 절에 있어야 한다.

- **점유 격자(occupancy grid)** — 지도를 격자로 두고 각 칸이 점유되어 있을 확률을 담는다.
  갱신은 **로그 승산(log-odds)** 으로 하는데, 그래야 증거 누적이 곱셈이 아니라 덧셈이 되고,
  확률이 0이나 1에 바짝 붙었을 때의 수치 문제를 피할 수 있다. 남는 위험의 방향을 짚어야 한다:
  로그 승산은 *유계가 아니어서*, 점유로 천 번 관측된 칸은 뒤집으려면 반대 관측 천 번이 필요하다 —
  그래서 구현들은 명시적 **클램핑** 범위를 둔다(OctoMap의 기여). 세상이 바뀌었을 때 지도가
  적응할 수 있게 하려는 것이다. 칸은 *비어 있음*, *점유됨*, 그리고
  **미지**의 셋 중 하나이고, 초심자가 빠뜨리는 것이 셋째다. 미지는 비어 있음이 아니며,
  그 차이가 곧 탐색이 존재하는 이유다.
- **팽창(inflation)** — 로봇을 점으로 다루는 계획기(위 그림)는 대신 장애물을 키워야 한다.
  점유 칸을 로봇 반경만큼 팽창시키면 **원형 로봇에 한해** 격자 위에서 바로 C-공간 장애물이
  된다 — 다른 형상에서는 근사이고, 그래서 Nav2 같은 스택은 별도의 footprint 충돌 검사를 따로
  돌린다. 그 바깥에 감쇠하는 비용을 더하면 계획기가 들어가기를 꺼리는 여유가 생긴다.
- **비용 지도(costmap)** — 칸이 이진값이 아니라 *통행 비용*을 담는 점유 격자다. 비용은
  팽창에 더해 로봇이 피해야 할 다른 모든 것을 합친다: 미지 영역, 거친 지형, 일방향 구역,
  진입 금지 구역. **비용 지도는 정책적 선호가 계획이기를 그만두고 기하가 되는 자리다** —
  [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성 §1]]이 학습된
  어포던스를 넣기에 잘못된 자리라고 논하는 바로 그 표현이고, 왜 그런지 보려면 이것이
  무엇인지 알아야 한다.
- **계층형 비용 지도** — 실제 스택은 여러 층(정적 지도, 장애물, 팽창, 센서별)을 두고 합성한다.
  그래야 낡은 장애물 하나를 지우는 일이 지도를 지워버리지 않는다.
- **Frontier** — *알려진 자유 공간*과 *미지* 사이의 경계 칸. **frontier 탐색**은 "다음에
  어디로"에 대한 고전적 답이다: 가장 가까운 frontier로 가면 아는 영역이 자라고, frontier가
  없어질 때까지 반복한다. [[04-robotics/semantic-language-navigation|19. §3]]에서 "어디를
  탐색할지 고른다"는 의미 내비게이션 방법 중 일부는 이 후보 집합을 그대로 두고 학습된 부분이
  그 위의 *점수*만 공급한다 — [[04-robotics/semantic-language-navigation|19. §3]]의 VLFM이
  정확히 그렇다. 그렇지 않은 것도 있다: SemExp의 학습된 전역 정책은 지도 위의 임의의 장기
  목표를 고르고, 그것이 그 노트가 "frontier 기반이 아니라 목표 지향"이라고 말하는 뜻이다
  ([[01-canonical-papers/notes/9-navigation/semexp|SemExp]]). **논문이 둘 중 어느 쪽인지를
  가려내는 것이 핵심이고**, 그것이 학습된 구성요소가 후보를 고르는지 순위만 매기는지를 정한다.

> [!warning] "frontier"의 두 가지 뜻
> 아래 §4는 그래프 탐색의 열린 목록 — 발견했지만 아직 확장하지 않은 노드 집합 — 을 가리켜
> *frontier 노드*라고 쓴다. 지도 위의 탐색 frontier와는 다른 대상이고, 단어만 같을 뿐 서로
> 무관하지는 않다: 둘 다 탐색된 것과 아닌 것의 경계를 가리키고, 하나는 그래프에서 하나는
> 격자에서 그럴 뿐이다. 논문들은 이것을 거의 구분해 주지 않는다.

**전역과 지역.** 내비게이션 스택은 계획을 둘로 나눈다: **전역 계획기**가 비용 지도 전체에서
경로를 탐색하고(§3~§5), **지역 계획기**가 그 경로와 로봇의 동역학, 그리고 그사이 나타난
장애물을 놓고 다음 몇 초의 운동을 반복해서 고른다. 고전적 이름들이 사는 곳이 지역 층이다 —
*dynamic window* 계열은 실행 가능한 속도 쌍을 표본으로 뽑아 점수를 매기고, **elastic band**는
내부 수축력과 외부 장애물 반발력으로 시간 개념 없이 *경로*를 변형하며, **timed elastic band**는
이름이 가리키는 시간 간격을 더한 후손이다. **표본 기반 MPC**([[01-canonical-papers/notes/9-navigation/badgr|BADGR]]이
쓰는 계열)는 running estimate 주변에서 많은 행동열을 표본으로 뽑아 모델로 굴린 뒤, 가장 좋은
하나를 고르는 대신 **보상 가중 평균**으로 추정을 갱신하고 그 첫 행동을 실행한다.
§6이 같은 층을 최적화 관점에서 다룬다. **"계획기를 대체했다"는 논문은 거의 언제나 지역
계획기를 뜻하고**, 전역 탐색과 비용 지도는 건드리지 않는다 — 그것이 그 결과가 주장할 수 있는
범위를 한정한다.

<svg viewBox="0 0 460 216" style="max-width:100%;height:auto" role="img" aria-label="작업 공간 장애물과 부풀려진 배위 공간 장애물">
  <g stroke="currentColor" stroke-width="1.3" fill="none"><rect x="25" y="25" width="185" height="150" rx="3"/><rect x="250" y="25" width="185" height="150" rx="3"/></g>
  <g fill="currentColor" opacity="0.22"><rect x="95" y="70" width="45" height="45" rx="2"/><rect x="308" y="53" width="79" height="79" rx="2"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.7"><rect x="308" y="53" width="79" height="79" rx="2"/></g>
  <g fill="currentColor"><circle cx="55" cy="150" r="4"/><circle cx="180" cy="50" r="4"/><circle cx="280" cy="150" r="4"/><circle cx="405" cy="50" r="4"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.8"><path d="M55,150 C80,150 88,124 92,124 C96,124 140,124 146,118 C152,112 150,60 180,50"/><path d="M280,150 C300,150 300,142 302,140 C304,138 395,140 398,134 C401,128 400,62 405,50"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="25" y="18">작업 영역</text><text x="250" y="18">배위 공간</text>
    <text x="117" y="96" font-size="10.5" text-anchor="middle">장애물</text>
    <text x="347" y="96" font-size="10.5" text-anchor="middle">C-장애물</text>
    <text x="25" y="193" opacity="0.85">계획은 로봇을 점 하나로 줄인다 &#8212;</text>
    <text x="25" y="209" opacity="0.85">대신 장애물이 로봇의 형상만큼 커지므로, 점의 경로가 곧 안전한 경로다</text>
  </g>
</svg>



### 3. 그래프 탐색

A*에서,

$$f(n)=g(n)+h(n)$$

- $g(n)$: 시작에서 노드 $n$까지의 알려진 비용.
- $h(n)$: $n$에서 목표까지의 추정 비용.
- $f(n)$: 확장 우선순위.

Dijkstra는 정보성 휴리스틱이 없는 경우다. A*는 적절한 admissibility/consistency 조건
아래 그래프 위에서 최적이다. *admissible*(허용성)은 $h$가 남은 실제 비용을 절대 **과대**
평가하지 않는다는 뜻(낙관적 추정)이고, *consistent*(일관성)은 거기에 더해 방금 지난 간선의
비용보다 더 많이 줄어들지 않는다는 뜻이다 — 그래야 경로를 따라 추정이 서로 어긋나지 않는다.
다만 이 정리는 이산화된 그래프가 모든 실행 가능한 연속 로봇
운동을 대표한다는 것까지 보장하지 않는다.

### 4. 계산 예제: 휴리스틱이 바꾸는 것

프런티어의 두 노드가 $(g,h)=(6,3)$과 $(4,6)$이라 하자. A* 우선순위는 $9$와 $10$이므로,
cost-to-come이 더 큰데도 첫 노드가 먼저 확장된다. 휴리스틱은 목표에 가깝다고 추정되는
상태 쪽으로 노력을 돌린다. *과소평가* 휴리스틱은 admissible을 유지한다 — 너무 약하면 A*가 Dijkstra보다 빨라지는
이득이 거의 없을 뿐이다; *과대평가* 휴리스틱은 통상적 최적성 보장을 잃을 수 있다.

### 5. 주요 방법 계열

| 계열 | 대표 아이디어 | 이렇게 읽어라 |
|---|---|---|
| 그래프 탐색 | BFS, Dijkstra, A* | 명시적 이산화 위의 탐색 |
| 샘플링 기반 | PRM, RRT, RRT* | 표본으로 고차원 자유 공간 탐사 |
| 궤적 최적화 | shooting, transcription, collocation | 제약 아래 상태/입력 최적화 |
| 과제 계획 | 기호적 연산자와 목표 | 이산 행동 선택 |
| TAMP | task and motion planning | 기호적 선택을 기하학적 실행 가능성과 결합 |
| 불확실성 계획 | MDP, POMDP, belief space | 불확실한 상태/결과 아래 행동 선택 |

**Probabilistic completeness**는 방법의 가정 아래 robust한 해가 존재할 때 계산이 늘수록
해를 찾을 확률이 1에 다가간다는 뜻이다. 빠른 성공을 뜻하지 않는다. **Asymptotic
optimality**도 표본이 늘 때의 수렴 성질이지, 실시간 예산에서 얻는 품질이 아니다.

<svg viewBox="0 0 660 214" style="max-width:100%;height:auto" role="img" aria-label="표본 기반 플래너가 자유 공간에 트리를 키우는 방식">
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.5"><rect x="30" y="30" width="330" height="140" rx="3"/></g>
  <g fill="currentColor" opacity="0.20"><rect x="150" y="96" width="52" height="40" rx="2"/><rect x="240" y="128" width="52" height="34" rx="2"/></g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.85"><line x1="60" y1="150" x2="85" y2="132"/><line x1="85" y1="132" x2="110" y2="110"/><line x1="110" y1="110" x2="135" y2="88"/><line x1="135" y1="88" x2="170" y2="74"/><line x1="170" y1="74" x2="210" y2="66"/><line x1="210" y1="66" x2="250" y2="80"/><line x1="250" y1="80" x2="290" y2="66"/><line x1="290" y1="66" x2="330" y2="52"/><line x1="85" y1="132" x2="70" y2="108"/><line x1="110" y1="110" x2="96" y2="146"/><line x1="170" y1="74" x2="178" y2="46"/><line x1="210" y1="66" x2="226" y2="40"/><line x1="250" y1="80" x2="258" y2="110"/><line x1="290" y1="66" x2="304" y2="92"/></g>
  <g fill="currentColor" opacity="0.85"><circle cx="85" cy="132" r="2.4"/><circle cx="110" cy="110" r="2.4"/><circle cx="135" cy="88" r="2.4"/><circle cx="170" cy="74" r="2.4"/><circle cx="210" cy="66" r="2.4"/><circle cx="250" cy="80" r="2.4"/><circle cx="290" cy="66" r="2.4"/><circle cx="330" cy="52" r="2.4"/><circle cx="70" cy="108" r="2.4"/><circle cx="96" cy="146" r="2.4"/><circle cx="178" cy="46" r="2.4"/><circle cx="226" cy="40" r="2.4"/><circle cx="258" cy="110" r="2.4"/><circle cx="304" cy="92" r="2.4"/></g>
  <g fill="currentColor"><circle cx="60" cy="150" r="4.5"/><circle cx="330" cy="52" r="4.5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="40" y="166">시작</text><text x="306" y="44">목표</text>
    <text x="370" y="62">1. 무작위 점을 하나 뽑는다</text><text x="370" y="80">2. 가장 가까운 노드를 찾는다</text><text x="370" y="98">3. 충돌이 없으면 그쪽으로 뻗는다</text>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle" opacity="0.9">
    <text x="176" y="120">장애물</text><text x="266" y="149">장애물</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="190" opacity="0.9">트리는 공간을 열거하지 않는다 &#8212; 짧은 선분 하나가 자유로운지만 매번 묻는다.</text>
    <text x="30" y="205" opacity="0.9">고차원에서 살아남는 이유이자, 경로가 들쭉날쭉하게 나와 평활화가 필요한 이유다.</text>
  </g>
</svg>



### 6. 궤적 최적화와 MPC

흔한 정식화는

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. 동역학, 한계, 충돌 제약}$$

- **주어진 것:** 초기 상태, 모델, 목표, 제약, 비용.
- **최적화하는 것:** 상태·입력 시퀀스.
- **실행 시점:** 오프라인 계획 또는 MPC로 반복 온라인.
- **주의:** 비선형 동역학과 장애물 제약은 대개 국소적·초기화 민감 문제를 만든다.

Direct shooting은 제어를 최적화하고 상태를 시뮬레이션한다. Direct transcription은
상태·제어를 모두 변수로 둔다. Collocation은 선택한 점들에서 동역학을 강제한다. 어느
것도 비볼록 로봇 문제의 전역 최적성을 자동으로 증명하지 않는다.

### 7. 과제 계획, 불확실성, replanning

`pick(block)` 같은 기호적 명령은 논리적으로 타당해도 충돌 없는 파지가 존재하지 않아
기하학적으로 불가능할 수 있다. TAMP는 이산 행동과 연속 실행 가능성을 번갈아 또는
공동으로 추론한다.

부분 관측에서는 계획의 상태가 belief가 된다. POMDP는 숨은 상태, 관측, 행동, 전이,
관측 모델, 보상을 구분한다. 정확한 belief-space 계획은 대개 계산 불가능해서 논문들은
근사, receding horizon, 학습된 가치, 비상 정책을 쓴다.

온라인 replanning은 새 관측을 반영한다. 보고된 replanning 주기만으로는 부족하다 —
인식 지연, 장면 동역학, 제어기 대역폭과 비교하라.

### 8. 학습 기반 계획

학습된 구성요소는 휴리스틱, 비용, 동역학/월드모델, 가치 함수, 제안 분포, 궤적 생성기,
정책 전체 중 무엇이든 될 수 있다. 행동을 출력하는 VLA는 대개 정책이다; 미래를 롤아웃하는
월드모델은 그 미래를 *선택·최적화 절차가 사용할 때에만* 계획을 지원한다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "그럴듯한 궤적을 생성한다"는 충돌 없음, 동역학적 실행 가능, 안정, 안전한 실행을
> 함의하지 않는다. 명시적 제약, 하류 제어기, replanning, 폐루프 로봇 결과를 확인하라.

### 9. 평가와 실패 모드

성공률, 충돌률, 경로/궤적 비용, 계획·실행 시간, 최적성 갭, 제약 위반, replanning 빈도,
지도/상태 오차에 대한 강건성, 폐루프 실행을 확인하라. 계획 실패, 인식 실패, 추종 실패,
하드웨어 실패를 분리하라.

### 읽고 나면 말할 수 있어야 하는 것

- plan·path·trajectory·policy·controller를 구분할 수 있다
- A*의 $g$, $h$, $f$를 해석할 수 있다
- probabilistic completeness를 속도 보장이라 부르지 않고 설명할 수 있다
- 그래프 탐색·샘플링·궤적 최적화를 비교할 수 있다
- TAMP가 기하학적 실행 가능성을 검사해야 하는 이유를 설명할 수 있다
- 학습된 궤적 생성기가 보장하지 않는 것을 짚을 수 있다

> [!tip] 더 깊이 · Going deeper
> LaValle의 [*Planning Algorithms*](http://lavalle.pl/planning/)가 무료이고 샘플링 기반 쪽의 참고서다. 궤적 최적화 쪽은 Tedrake의 [*Underactuated Robotics*](https://underactuated.csail.mit.edu/)가 실행 가능한 코드와 함께 다룬다.

### 스스로 점검

1. 충돌 없는 path가 동역학적으로 실행 불가능할 수 있는 이유는?
2. 컨피규레이션 공간 대신 작업 영역에서만 계획하면 무엇을 잃는가?
3. 실행 가능한 궤적이 존재하는데도 궤적 최적화가 실패할 수 있는 이유는?
4. "실시간 폐루프 플래너" 주장을 지지하는 증거는?

> [!tip]- 정답 · Answers
> 1. 불가능한 속도·가속도·토크·접촉·타이밍을 요구할 수 있다.
> 2. 로봇 형상, 관절 한계, 같은 과제 pose에 대한 복수의 컨피규레이션.
> 3. 문제가 비볼록이고 초기화에 민감할 수 있다.
> 4. 명시된 하드웨어에서의 끝-끝 지연 분포, 교란·동적 장애물 아래의 실행, 제약 위반과 실패 — 플래너 계산 시간만으로는 안 된다.

### 출처

- [Modern Robotics, Chapter 10](http://modernrobotics.org)
- [MIT Underactuated Robotics](https://underactuated.csail.mit.edu/)
- [OMPL: planning concepts](https://ompl.kavrakilab.org/)
