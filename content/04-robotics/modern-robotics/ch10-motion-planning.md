---
title: "MR Ch.10 — Motion Planning"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P2, write the panel's collision test, count a 30° grid's blocked cells, check a straight C-space edge by hand, and run Dijkstra on a five-node roadmap."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.10** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the C-space idea from [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]] — specifically the panel's C-obstacle derived there — and the basics of graph search (BFS/Dijkstra).
> [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 C-space 개념, 특히 거기서 유도한 패널의 C-장애물과 그래프 탐색(BFS/다익스트라)의 기초가 필요하다.

## English

**Core question**: how do we find a collision-free path through C-space?

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] and the panel frozen on [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]]: the rigid half-plane $x \ge 1$, links modelled as zero-thickness segments. That chapter derived the penetration depth and the C-obstacle; this page plans inside them.

$$d(\theta) = \max\bigl(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)\bigr) - 1, \qquad \mathcal{C}_{\text{free}} = \{\theta : d(\theta) \le 0\}$$

with contact ($d = 0$) counted as free, because the running task ends in contact. Here $d$ is a penetration depth, positive inside the obstacle — the opposite sign to MR's signed distance, as ch.2 warns. P2's configuration space is the torus $T^2$, and the panel blocks $18.478\,\%$ of it.

**The query** is the elbow flip of [[04-robotics/modern-robotics/ch09-trajectory-generation|ch.9]]: start at $A = (0°, 90°)$, reach $B = (90°, -90°)$. Both put the tip on the panel target $(1,1)$; ch.9 timed the straight line between them, and this page asks whether that line is legal.

### Homework diagram · 과제가 그릴 그림

One square, $\theta_1$ horizontal and $\theta_2$ vertical, both $-180°$ to $+180°$, with the opposite edges marked as identified — the same torus chart as ch.2. On it, four layers.

1. **The C-obstacle**, shaded: the lens $\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1$ spanning $\theta_1 \in (-90°, 90°)$.
2. **The grid**: tick marks every $30°$ on both axes, giving $12 \times 12$ nodes. Put a cross on every node that lies in the shaded region, and a small open circle on every node that lies exactly on its boundary.
3. **The roadmap**: five labelled dots $A, B, C, D, E$ at the configurations tabulated below, with a straight segment drawn between every pair. Draw the two segments that cut through the shaded region as dashed and put an X on each.
4. **The answer path**: trace the shortest surviving chain from $A$ to $B$ in a heavier line and write its length beside it.

The problem set asks for the same square with the shaded region redrawn for a panel moved back half a metre, and the point of the exercise is which dashed segments come back to life.

### Worked on the plant · 장치로 한 번 끝까지

**Step 1 — the collision test, written as a procedure.** A planner calls this on every candidate configuration, so it has to be cheap and exact:

1. elbow $e_x = \cos\theta_1$;
2. tip $p_x = \cos\theta_1 + \cos(\theta_1{+}\theta_2)$;
3. $d = \max(e_x, p_x) - 1$; report *collision* if $d > 0$.

Only the two endpoints are tested because $x$ is linear along a straight segment, so its maximum over a link is attained at an end. And since $|\cos\theta_1| \le 1$, step 1 can never fire on its own — the elbow grazes the wall at $\theta_1 = 0$ and never crosses it.

**Step 2 — the grid, counted.** Discretize both angles at $30°$: $360/30 = 12$ values each, so $12^2 = \mathbf{144}$ nodes. Evaluating $d$ at all of them gives

| | count | share |
|---|---:|---:|
| $d > 0$, blocked | $21$ | $14.58\,\%$ |
| $d = 0$, exactly touching | $13$ | $9.03\,\%$ |
| $d < 0$, strictly free | $110$ | $76.39\,\%$ |

and the row that teaches something is the first against ch.2's continuous answer. The true obstacle covers $18.478\,\%$ of the torus, which is $0.18478 \times 144 = 26.6$ cells' worth of area, but only $21$ *nodes* land inside it. **A node-sampled grid systematically underestimates the obstacle**, by $5.6$ cells here, because a cell whose centre is free can still be half full of obstacle. That gap is the whole content of resolution completeness in §3. Of the 13 touching nodes, 7 have $\theta_1 = 0$, where link 1's elbow grazes the wall; in two of those, $(0°, \pm 90°)$, the tip lands on the face as well, and only those two are contacts the *tool* makes.

**Step 3 — the edge test, and the query's direct edge.** An edge is a straight segment in C-space, $\theta(\lambda) = (1-\lambda)q_1 + \lambda q_2$. Testing it means evaluating $d$ at $m$ interior values of $\lambda$. Take the query's direct edge, $A = (0°,90°)$ to $B = (90°,-90°)$. Along it $\theta_1 = 90°\lambda$ and $\theta_1 + \theta_2 = 90° - 90°\lambda$, so the tip's $x$-coordinate is

$$p_x(\lambda) = \cos(90°\lambda) + \sin(90°\lambda)$$

because $\cos(90° - u) = \sin u$. That is $\sqrt2\cos(90°\lambda - 45°)$, maximal when $90°\lambda = 45°$, i.e. at $\lambda = 0.5$, where the arm is straight at $45°$ and the tip sits at $(\sqrt2, \sqrt2)$:

$$d_{\max} = \sqrt2 - 1 = 0.4142\ \mathrm{m}$$

so the edge ch.9 spent a whole chapter timing drives the arm **41 cm into the panel** at its midpoint. Both endpoints have $d = 0$; only the interior offends. Checking $m = 1$ interior sample already catches it, because that sample is $\lambda = 0.5$ exactly.

**Step 4 — an edge that a careless test misses.** Not every violation sits at a midpoint. The edge $B = (90°,-90°)$ to $C = (60°,90°)$ has length $182.48°$ and penetrates over only $\lambda \in (0,\ 0.155]$, peaking at $d = 0.0201\,\mathrm{m}$ near $\lambda = 0.077$ — a $2\,\mathrm{cm}$ bite spread over a $28.2°$ band. With $m$ evenly spaced interior samples the spacing is $182.48°/(m+1)$, so

| $m$ | spacing | verdict |
|---:|---:|---|
| $3$ | $45.6°$ | missed |
| $5$ | $30.4°$ | missed |
| $6$ | $26.1°$ | caught |

and the rule is visible in the table: **a sample spacing wider than the violating band can step over it**. Nothing about the checker is wrong; it is answering a question about $m$ points, and the planner then reports a path the robot cannot execute. Real planners handle this with a bound on how fast the body can move per radian of joint motion, not by hoping.

**Step 5 — the roadmap.** Five configurations, the query's two endpoints plus three samples:

| node | $(\theta_1, \theta_2)$ | tip | $d$ |
|---|---|---|---:|
| $A$ | $(0°,\ 90°)$ | $(1,\ 1)$ | $0$ |
| $B$ | $(90°,\ -90°)$ | $(1,\ 1)$ | $0$ |
| $C$ | $(60°,\ 90°)$ | $(-0.366,\ 1.366)$ | $-0.500$ |
| $D$ | $(120°,\ 30°)$ | $(-1.366,\ 1.366)$ | $-1.500$ |
| $E$ | $(135°,\ -45°)$ | $(-0.707,\ 0.707)$ | $-1.707$ |

All ten pairs get the edge test, edge length being the Euclidean distance on the chart (taking the short way round each circle):

| edge | length | verdict |
|---|---:|---|
| $A$–$B$ | $3.5124$ | blocked, $d_{\max}=0.4142$ |
| $A$–$C$ | $1.0472$ | free |
| $A$–$D$ | $2.3416$ | free |
| $A$–$E$ | $3.3322$ | free |
| $B$–$C$ | $3.1849$ | blocked, $d_{\max}=0.0201$ |
| $B$–$D$ | $2.1589$ | free |
| $B$–$E$ | $1.1107$ | free |
| $C$–$D$ | $1.4811$ | free |
| $C$–$E$ | $2.6954$ | free |
| $D$–$E$ | $1.3349$ | free |

Now run Dijkstra from $A$. The direct edge is gone, so the candidates are $A$–$E$–$B = 3.3322 + 1.1107 = 4.4429$, $A$–$D$–$B = 2.3416 + 2.1589 = 4.5005$, $A$–$C$–$D$–$B = 4.6872$, and $A$–$D$–$E$–$B = 4.7872$. The winner is

$$A \to E \to B, \qquad \text{cost } 3.3322 + 1.1107 = 4.4429\ \mathrm{rad} = \pi\sqrt2$$

because $A$–$E$ moves $(135°,-135°)$ and $E$–$B$ moves $(45°,45°)$, so the two lengths are $135°\sqrt2$ and $45°\sqrt2$ and they sum to $180°\sqrt2 = \pi\sqrt2$. Against the blocked direct edge's $(\pi/2)\sqrt5 = 3.5124$, the detour costs $2\sqrt2/\sqrt5 = 1.265$, i.e. $\mathbf{26.5\,\%}$ extra joint travel. The margin over $A$–$D$–$B$ is only $0.058\,\mathrm{rad}$; a roadmap this sparse decides such things by which samples happened to be drawn, which is exactly the property §3 names.

### 1. The chapter in one list

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
> The intractability claim *is* $36^6\approx 2.18\times 10^9$ at $1\,\mathrm{ms}\approx 25$ days. Probabilistic completeness is not a time bound: a planner can run forever on a problem that has a solution. An RRT path that puts P2's tip on the panel has not checked $F_n$ on the P3 wall.
>
> **The fix.** Sampling planners never build the grid. One RRT step: sample a random $q_\text{rand}$, find the nearest tree node $q_\text{near}$, move a fixed step from $q_\text{near}$ toward $q_\text{rand}$ to get $q_\text{new}$, and add it if the segment is collision-free. The cost is paid per sample, not per cell.

### 2. The collision test, defined

A **configuration collision test** is a *predicate* on a single configuration: given $q$, it returns whether $\mathcal{A}(q) \cap \mathcal{O} \neq \varnothing$, i.e. whether $q \in \mathcal{C}_{\text{obs}}$. It is the only way a planner ever learns about the world; the planner itself has no picture of the obstacle. An **edge test** is the derived predicate on a pair, and the honest version of it is not a predicate at all but an approximation:

$$\text{edge}(q_1,q_2) \text{ declared free} \iff d\bigl((1-\lambda)q_1 + \lambda q_2\bigr) \le 0 \ \text{ for } \lambda = \tfrac{1}{m+1}, \dots, \tfrac{m}{m+1}$$

because testing a continuum would cost infinitely much, so a finite $m$ stands in for it and the result is only as true as $m$ is large.

- **Example**: P2's test above, three arithmetic lines and one comparison. A real manipulator's is a broad-phase bounding-volume pass followed by a narrow-phase mesh–mesh query, but the interface is the same predicate.
- **Non-example**: "the tip is outside the wall." That tests one *point* of the robot, not the robot, so it passes any configuration in which a link crosses the obstacle while the tip does not — stand the wall closer than $L_1$ and a folded elbow goes straight through it unseen. For P2 and this wall the two tests happen to agree, and ch.2's derivation is what establishes that; it is not a general licence to test the tip alone.
- **Why it matters**: every completeness claim in §3 is a claim about this predicate being called on enough points. Planners are usually correct; the discretization of their edge test is what fails.

### 3. Two completeness guarantees, defined apart

Both are weaker than **completeness** proper, which means: if a solution exists, the algorithm finds one in finite time, and if none exists it says so.

- **Resolution completeness** is relative to a chosen discretization: if a solution exists *that the discretization can represent*, the algorithm finds it. Its failure mode is geometric — a free passage narrower than the grid spacing is invisible, and Step 2 of the worked section shows the same effect on the obstacle, whose area the node sample understates by $5.6$ cells out of $144$.
- **Probabilistic completeness** is relative to the number of samples: the probability of finding an existing solution tends to $1$ as sampling continues. Its failure mode is temporal — the guarantee names no deadline, so a planner may still be running when the control period ends.

$$\lim_{n \to \infty} P[\text{solution found in } n \text{ samples}] = 1$$

because the sampler eventually puts points in every region of positive measure, which is also why a passage of *zero* measure — an exactly-touching contact configuration like $A$ or $B$ — is never found by sampling at all and must be supplied by the query.

- **Example**: the five-node roadmap above is not probabilistically complete at five nodes; it becomes so in the limit. Its margin of $0.058\,\mathrm{rad}$ between the best and second-best path is decided by which three samples were drawn.
- **Non-example of each**: an RRT that has not returned yet is not evidence that no path exists (that would be reading probabilistic completeness as completeness); a grid planner reporting failure at $30°$ is not evidence either (that would be reading resolution completeness as completeness).
- **Why it matters**: a paper that reports "the planner failed" has reported a fact about its resolution or its budget, not about the robot's workspace, unless it says which.

**Wiki connections**: the classical layer that learned policies increasingly *absorb* —
a [[01-canonical-papers/notes/4-vla/pi0|VLA]] implicitly plans in its forward pass, and
[[01-canonical-papers/notes/5-world-models/planet|latent-space CEM]] is planning with a learned model;
on real sites, sampling planners still provide the safety-checkable backbone that learned
proposals get filtered through.

### Self-check

1. Discretize a 7-dof arm's C-space at 100 cells per axis — how many cells? What does that explain about sampling-based planning?
2. What does RRT's "probabilistic completeness" guarantee, and what does it not?
3. Why can't you run plain RRT on a car?
4. Both endpoints of the direct edge $A$–$B$ are collision-free. Why is the edge not?

> [!tip]- Answers
> 1. $100^7 = 10^{14}$ cells. Grid search explodes exponentially in dof, so beyond a few dimensions only sampling is tractable — you cannot even enumerate the space, let alone search it.
> 2. Guaranteed: if a solution exists (under the method's assumptions), the probability of finding it tends to 1 as computation grows. Not guaranteed: *when* it is found, or the quality of the path — plain RRT paths are typically far from optimal, which is what RRT\* and post-smoothing address.
> 3. Its extension step connects two configurations with a straight line in C-space, but a nonholonomic vehicle cannot execute sideways motion — the "edge" is not a feasible trajectory. Keep sampling states, but extend with a constraint-respecting local planner — integrate discretized controls or use Reeds–Shepp curves (kinodynamic planning; [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|ch.13]]).
> 4. Because $\mathcal{C}_{\text{free}}$ is not convex: the segment between two of its points may leave it. Here $p_x(\lambda) = \cos(90°\lambda)+\sin(90°\lambda)$ rises from $1$ to $\sqrt2$ and back, so the interior penetrates $0.4142\,\mathrm{m}$ while both ends merely touch.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same plant **P2**, same five nodes, same query $A \to B$ — but the panel is rebuilt at $x \ge 1.5$, the wall of ch.2's problem set.

1. **Draw.** The torus chart again with the new, smaller obstacle shaded, the same $12 \times 12$ grid crosses, and the same five nodes with all ten edges. Mark which previously dashed edges are now solid.
2. **Derive.** (a) Re-test the direct edge $A$–$B$: use $p_x(\lambda) = \cos(90°\lambda) + \sin(90°\lambda)$ and report $d_{\max}$ against the new wall. (b) Re-test $B$–$C$, whose worst point was $d = 0.0201$ before. (c) Give the new shortest path and its cost, and the percentage saved against the old answer $\pi\sqrt2$.
3. **Interpret.** At $30°$ the new wall blocks $9$ of $144$ nodes, against a true blocked area of $8.515\,\%$ of the torus. Is the grid still underestimating, and by how many cells? Then say what had to be recomputed when the wall moved — the nodes, the edges, both — and what that implies about caching a roadmap on a site where the geometry is surveyed once and then changes.

> [!tip]- Solutions
> 1. Both previously dashed edges become solid, so the roadmap is complete on five nodes and the direct $A$–$B$ edge is available.
> 2. (a) $p_x$ still peaks at $\sqrt2 = 1.4142$ at $\lambda = 0.5$, but the wall is now at $1.5$, so $d_{\max} = 1.4142 - 1.5 = -0.0858\,\mathrm{m}$: free, with $8.6\,\mathrm{cm}$ to spare. (b) Every $d$ along that edge drops by exactly $0.5$, so its worst point becomes $0.0201 - 0.5 = -0.4799$: free. (c) The shortest path is now the direct edge, $(\pi/2)\sqrt5 = 3.5124\,\mathrm{rad}$, saving $1 - 3.5124/4.4429 = 20.9\,\%$ against $\pi\sqrt2$.
> 3. Still underestimating: the true area is $0.08515 \times 144 = 12.3$ cells' worth against $9$ blocked nodes, a shortfall of $3.3$ cells. Moving the wall changed no node's *coordinates* and every node's *label*, and it invalidated all ten edge verdicts — the graph's geometry is a property of the robot, its occupancy is a property of the world. So a roadmap may be cached and reused only while the world is the one it was checked against; on a site, that means re-running the tests after every survey update, which is cheap (the samples are kept) compared with re-sampling, and is exactly why PRM separates its learning phase from its query phase.

### Continue beyond this chapter

[[04-robotics/planning-decision-making|Planning & Decision-Making]] connects this chapter to A*, sampling-based planning, trajectory optimization, TAMP, uncertainty, MPC, and learned planners.

## 한국어

**핵심 질문**: C-space를 통과하는 충돌 없는 경로를 어떻게 찾는가?

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**와 [[04-robotics/modern-robotics/ch02-configuration-space|2장]]에서 고정한 패널: 강체 반평면 $x \ge 1$, 링크는 두께 0인 선분. 그 장에서 침투 깊이와 C-장애물을 유도했고, 이 페이지는 그 안에서 계획한다.

$$d(\theta) = \max\bigl(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)\bigr) - 1, \qquad \mathcal{C}_{\text{free}} = \{\theta : d(\theta) \le 0\}$$

접촉($d = 0$)은 자유로 센다. 관통 과제가 접촉으로 끝나기 때문이다. 여기서 $d$는 장애물 안에서 양수인 침투 깊이이고, 2장이 경고하듯 MR의 부호 있는 거리와는 부호가 반대다. P2의 컨피규레이션 공간은 원환면 $T^2$이고 패널이 그중 $18.478\,\%$를 막는다.

**질의**는 [[04-robotics/modern-robotics/ch09-trajectory-generation|9장]]의 엘보 뒤집기다. $A = (0°, 90°)$에서 출발해 $B = (90°, -90°)$에 도달한다. 둘 다 말단을 패널 목표 $(1,1)$에 두고, 9장은 그 둘 사이의 직선에 시간을 입혔으며, 이 페이지는 그 직선이 합법인지 묻는다.

### 과제가 그릴 그림 · Homework diagram

정사각형 하나, 가로 $\theta_1$ 세로 $\theta_2$, 둘 다 $-180°$에서 $+180°$, 마주 보는 변은 동일시 표시 — 2장과 같은 원환면 도표다. 그 위에 네 겹.

1. **C-장애물**을 칠한다: $\theta_1 \in (-90°, 90°)$에 걸친 렌즈 $\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1$.
2. **격자**: 두 축에 $30°$마다 눈금, $12 \times 12$개의 노드. 칠한 영역 안의 노드마다 가위표, 경계에 정확히 걸린 노드마다 작은 빈 동그라미.
3. **로드맵**: 아래 표의 자세에 점 다섯 $A, B, C, D, E$를 찍고 모든 쌍을 직선으로 잇는다. 칠한 영역을 가로지르는 두 선분은 점선으로 그리고 X 표시를 한다.
4. **정답 경로**: $A$에서 $B$로 살아남은 가장 짧은 사슬을 굵게 덧그리고 옆에 길이를 쓴다.

과제는 패널을 0.5 m 뒤로 물린 뒤 칠한 영역을 다시 그린 같은 정사각형을 요구하며, 문제의 핵심은 어느 점선이 되살아나는가다.

### 장치로 한 번 끝까지 · Worked on the plant

**1단계 — 충돌 검사를 절차로.** 계획기가 후보 자세마다 부르므로 싸고 정확해야 한다:

1. 엘보 $e_x = \cos\theta_1$;
2. 말단 $p_x = \cos\theta_1 + \cos(\theta_1{+}\theta_2)$;
3. $d = \max(e_x, p_x) - 1$; $d > 0$이면 *충돌*이라고 보고.

끝점 둘만 보는 이유는 직선 선분 위에서 $x$가 일차라 최댓값이 끝에서 나오기 때문이다. 그리고 $|\cos\theta_1| \le 1$이므로 1단계가 혼자 발화할 수 없다. 엘보는 $\theta_1 = 0$에서 벽을 스칠 뿐 넘지 못한다.

**2단계 — 격자를 세다.** 두 각을 $30°$로 이산화하면 각각 $360/30 = 12$개 값이라 노드가 $12^2 = \mathbf{144}$개다. 전부에서 $d$를 계산하면

| | 개수 | 비율 |
|---|---:|---:|
| $d > 0$, 막힘 | $21$ | $14.58\,\%$ |
| $d = 0$, 정확히 닿음 | $13$ | $9.03\,\%$ |
| $d < 0$, 엄격히 자유 | $110$ | $76.39\,\%$ |

이고, 배울 것이 있는 행은 2장의 연속적 답과 맞댄 첫 행이다. 진짜 장애물은 원환면의 $18.478\,\%$, 즉 $0.18478 \times 144 = 26.6$칸어치 넓이를 덮는데 그 안에 떨어진 *노드*는 $21$개뿐이다. **노드만 표본하는 격자는 장애물을 체계적으로 과소평가한다.** 여기서는 $5.6$칸만큼인데, 중심이 자유인 칸도 절반이 장애물일 수 있기 때문이다. 이 간극이 §3의 해상도 완전성의 내용 전부다. 닿는 노드 13개 중 7개는 $\theta_1 = 0$으로 링크 1의 엘보가 벽을 스치는 자리다. 그중 둘, $(0°, \pm 90°)$에서는 말단도 면에 닿으며, *도구*가 만드는 접촉은 그 둘뿐이다.

**3단계 — 간선 검사와 질의의 직통 간선.** 간선은 C-space의 직선 선분 $\theta(\lambda) = (1-\lambda)q_1 + \lambda q_2$다. 검사란 $\lambda$의 내부 값 $m$개에서 $d$를 계산하는 일이다. 질의의 직통 간선 $A = (0°,90°) \to B = (90°,-90°)$를 보자. 그 위에서 $\theta_1 = 90°\lambda$, $\theta_1 + \theta_2 = 90° - 90°\lambda$이므로 말단의 $x$ 좌표는

$$p_x(\lambda) = \cos(90°\lambda) + \sin(90°\lambda)$$

다. $\cos(90° - u) = \sin u$이기 때문이다. 이는 $\sqrt2\cos(90°\lambda - 45°)$이고 $90°\lambda = 45°$, 즉 $\lambda = 0.5$에서 최대이며 그때 팔은 $45°$로 곧게 펴져 말단이 $(\sqrt2, \sqrt2)$에 있다:

$$d_{\max} = \sqrt2 - 1 = 0.4142\ \mathrm{m}$$

따라서 9장이 한 장을 통째로 들여 시간을 입힌 그 간선은 중간점에서 팔을 **패널 안으로 41 cm** 밀어 넣는다. 양 끝점은 $d = 0$이고 내부만 위반한다. 내부 표본 $m = 1$이면 이미 잡힌다. 그 표본이 정확히 $\lambda = 0.5$이기 때문이다.

**4단계 — 부주의한 검사가 놓치는 간선.** 모든 위반이 중간점에 있지는 않다. 간선 $B = (90°,-90°) \to C = (60°,90°)$는 길이가 $182.48°$인데 $\lambda \in (0,\ 0.155]$에서만 파고들고 $\lambda \approx 0.077$에서 $d = 0.0201\,\mathrm{m}$로 최대다. $28.2°$ 띠에 퍼진 $2\,\mathrm{cm}$짜리 한 입이다. 내부 표본 $m$개를 고르게 두면 간격이 $182.48°/(m+1)$이므로

| $m$ | 간격 | 판정 |
|---:|---:|---|
| $3$ | $45.6°$ | 놓침 |
| $5$ | $30.4°$ | 놓침 |
| $6$ | $26.1°$ | 잡음 |

이고 규칙이 표에 보인다. **표본 간격이 위반 띠보다 넓으면 그것을 건너뛸 수 있다.** 검사기가 틀린 것은 없다. 점 $m$개에 대한 질문에 답했을 뿐이고, 그러면 계획기가 로봇이 실행할 수 없는 경로를 보고한다. 실제 계획기는 관절 각도당 몸체가 얼마나 빨리 움직일 수 있는지의 상계로 이것을 다루지, 운에 맡기지 않는다.

**5단계 — 로드맵.** 자세 다섯, 질의의 끝점 둘과 표본 셋:

| 노드 | $(\theta_1, \theta_2)$ | 말단 | $d$ |
|---|---|---|---:|
| $A$ | $(0°,\ 90°)$ | $(1,\ 1)$ | $0$ |
| $B$ | $(90°,\ -90°)$ | $(1,\ 1)$ | $0$ |
| $C$ | $(60°,\ 90°)$ | $(-0.366,\ 1.366)$ | $-0.500$ |
| $D$ | $(120°,\ 30°)$ | $(-1.366,\ 1.366)$ | $-1.500$ |
| $E$ | $(135°,\ -45°)$ | $(-0.707,\ 0.707)$ | $-1.707$ |

열 쌍 모두에 간선 검사를 하고, 간선 길이는 도표 위의 유클리드 거리(각 원에서 짧은 쪽)다:

| 간선 | 길이 | 판정 |
|---|---:|---|
| $A$–$B$ | $3.5124$ | 막힘, $d_{\max}=0.4142$ |
| $A$–$C$ | $1.0472$ | 자유 |
| $A$–$D$ | $2.3416$ | 자유 |
| $A$–$E$ | $3.3322$ | 자유 |
| $B$–$C$ | $3.1849$ | 막힘, $d_{\max}=0.0201$ |
| $B$–$D$ | $2.1589$ | 자유 |
| $B$–$E$ | $1.1107$ | 자유 |
| $C$–$D$ | $1.4811$ | 자유 |
| $C$–$E$ | $2.6954$ | 자유 |
| $D$–$E$ | $1.3349$ | 자유 |

이제 $A$에서 다익스트라를 돌린다. 직통 간선이 사라졌으므로 후보는 $A$–$E$–$B = 3.3322 + 1.1107 = 4.4429$, $A$–$D$–$B = 2.3416 + 2.1589 = 4.5005$, $A$–$C$–$D$–$B = 4.6872$, $A$–$D$–$E$–$B = 4.7872$다. 승자는

$$A \to E \to B, \qquad \text{비용 } 3.3322 + 1.1107 = 4.4429\ \mathrm{rad} = \pi\sqrt2$$

다. $A$–$E$가 $(135°,-135°)$, $E$–$B$가 $(45°,45°)$를 움직이므로 두 길이가 $135°\sqrt2$와 $45°\sqrt2$이고 합이 $180°\sqrt2 = \pi\sqrt2$이기 때문이다. 막힌 직통 간선의 $(\pi/2)\sqrt5 = 3.5124$에 대해 우회 비용은 $2\sqrt2/\sqrt5 = 1.265$배, 즉 관절 이동량 $\mathbf{26.5\,\%}$ 추가다. $A$–$D$–$B$에 대한 여유는 $0.058\,\mathrm{rad}$뿐이다. 이만큼 성긴 로드맵은 그런 것을 어떤 표본이 우연히 뽑혔는지로 결정하며, 그것이 바로 §3이 이름 붙이는 성질이다.

### 1. 이 장을 목록 하나로

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
> 비실용 주장은 곧 $1\,\mathrm{ms}$에 $36^6\approx 2.18\times 10^9$, 약 $25$일이다. 확률적 완전성은 시간 보장이 아니다. 해가 있는 문제에서도 계획기가 영원히 돌 수 있다. P2 말단을 패널에 두는 RRT 경로는 P3 벽의 $F_n$을 검사하지 않았다.
>
> **해결책.** 샘플링 계획기는 격자를 만들지 않는다. RRT 한 스텝: 무작위 $q_\text{rand}$를 뽑고, 트리에서 가장 가까운 노드 $q_\text{near}$를 찾고, $q_\text{near}$에서 $q_\text{rand}$ 쪽으로 고정 보폭만큼 움직여 $q_\text{new}$를 얻은 뒤, 그 선분에 충돌이 없으면 트리에 더한다. 비용은 칸마다가 아니라 표본마다 든다.

### 2. 충돌 검사의 정의

**자세 충돌 검사**는 자세 하나에 대한 *술어*다. $q$가 주어지면 $\mathcal{A}(q) \cap \mathcal{O} \neq \varnothing$인지, 즉 $q \in \mathcal{C}_{\text{obs}}$인지를 돌려준다. 계획기가 세계에 대해 배우는 유일한 통로이며, 계획기 자신은 장애물의 그림을 갖고 있지 않다. **간선 검사**는 쌍에 대해 파생된 술어인데, 정직한 형태는 술어가 아니라 근사다:

$$\text{간선}(q_1,q_2)\text{을 자유로 선언} \iff \lambda = \tfrac{1}{m+1}, \dots, \tfrac{m}{m+1}\text{에서 } d\bigl((1-\lambda)q_1 + \lambda q_2\bigr) \le 0$$

연속체를 검사하면 비용이 무한이므로 유한한 $m$이 그 자리를 대신하고, 결과는 $m$이 큰 만큼만 참이기 때문이다.

- **예**: 위의 P2 검사, 산술 세 줄과 비교 하나. 실제 매니퓰레이터의 검사는 경계 부피 광역 탐색 뒤 메시-메시 정밀 질의지만 인터페이스는 같은 술어다.
- **반례**: "말단이 벽 밖에 있다". 이것은 로봇이 아니라 로봇의 *점 하나*를 검사한다. 말단은 넘지 않는데 링크가 장애물을 가로지르는 자세를 그대로 통과시킨다. 벽을 $L_1$보다 가까이 세우면 접은 엘보가 아무 신호 없이 벽을 통과한다. P2와 이 벽에서는 두 검사가 우연히 일치하고, 그것을 세우는 것이 2장의 유도다. 말단만 검사해도 된다는 일반 면허가 아니다.
- **왜 중요한가**: §3의 모든 완전성 주장은 이 술어가 충분히 많은 점에서 불린다는 주장이다. 계획기는 보통 옳고, 무너지는 것은 간선 검사의 이산화다.

### 3. 완전성 보장 둘을 갈라 정의하기

둘 다 진짜 **완전성**보다 약하다. 완전성이란 해가 있으면 유한 시간에 찾고 없으면 없다고 말하는 성질이다.

- **해상도 완전성**은 고른 이산화에 상대적이다. *그 이산화가 표현할 수 있는* 해가 존재하면 찾는다. 실패 방식은 기하적이다. 격자 간격보다 좁은 자유 통로는 보이지 않고, 위 2단계는 같은 효과를 장애물 쪽에서 보여 준다. 노드 표본이 그 넓이를 $144$칸 중 $5.6$칸만큼 적게 말한다.
- **확률적 완전성**은 표본 수에 상대적이다. 표본을 계속 뽑으면 존재하는 해를 찾을 확률이 $1$로 간다. 실패 방식은 시간적이다. 보장에 기한이 없어서, 제어 주기가 끝나도 계획기가 아직 돌고 있을 수 있다.

$$\lim_{n \to \infty} P[\text{표본 } n \text{개 안에 해를 찾음}] = 1$$

표본기가 결국 양의 측도를 가진 모든 영역에 점을 놓기 때문이다. 바로 그래서 측도가 *0*인 통로 — $A$나 $B$처럼 정확히 닿는 접촉 자세 — 는 샘플링으로 영영 찾을 수 없고 질의가 직접 넣어 주어야 한다.

- **예**: 위의 다섯 노드 로드맵은 다섯 개에서는 확률적으로 완전하지 않고 극한에서 그렇게 된다. 최선과 차선 사이 $0.058\,\mathrm{rad}$의 여유는 어떤 표본 셋이 뽑혔는지가 결정한다.
- **각각의 반례**: 아직 돌아오지 않은 RRT는 경로가 없다는 증거가 아니다(확률적 완전성을 완전성으로 읽은 것). $30°$에서 실패를 보고한 격자 계획기도 증거가 아니다(해상도 완전성을 완전성으로 읽은 것).
- **왜 중요한가**: "계획기가 실패했다"고 보고한 논문은 어느 쪽인지 밝히지 않는 한 로봇의 작업 영역이 아니라 자기 해상도나 자기 예산에 관한 사실을 보고한 것이다.

**위키 연결**: 학습된 정책이 점점 *흡수*하는 고전 계층 —
[[01-canonical-papers/notes/4-vla/pi0|VLA]]는 forward pass 안에서 암묵적으로 계획하고,
[[01-canonical-papers/notes/5-world-models/planet|잠재 공간 CEM]]은 학습된 모델로 하는 계획이다;
실제 현장에서는 샘플링 플래너가 여전히 학습된 제안을 거르는 안전 검증 가능한 척추를
제공한다.

### 스스로 점검

1. 7자유도 팔의 C-space를 축당 100칸으로 이산화하면 격자 칸은 몇 개인가? 이것이 표본 기반 계획의 존재 이유를 어떻게 설명하는가?
2. RRT의 "확률적 완전성"이 보장하는 것과 보장하지 않는 것은 각각 무엇인가?
3. 자동차에 일반 RRT를 그대로 쓰면 안 되는 이유는?
4. 직통 간선 $A$–$B$의 두 끝점은 충돌이 없다. 왜 간선은 충돌이 있는가?

> [!tip]- 정답
> 1. $100^7 = 10^{14}$칸이다. 격자 탐색은 자유도에 지수적으로 폭발하므로 몇 차원만 넘어가도 표본 추출만이 실용적이다. 탐색은커녕 공간을 나열하는 것조차 불가능하다.
> 2. 보장하는 것: 해가 존재하면(그 방법의 가정 아래) 계산을 늘릴수록 찾을 확률이 1로 간다. 보장하지 않는 것: *언제* 찾는지, 그리고 경로의 품질이다. 일반 RRT의 경로는 대개 최적과 거리가 멀고, RRT\*와 사후 평활화가 그 문제를 다룬다.
> 3. 확장 단계가 두 자세를 C-space의 직선으로 잇는데, 비홀로노믹 차량은 옆으로 가는 운동을 실행할 수 없다. 그 "간선"이 실행 가능한 궤적이 아닌 것이다. 상태 표본 추출은 그대로 두고, 제약을 지키는 국소 계획기로 확장한다. 이산화한 제어를 적분하거나 Reeds–Shepp 곡선을 쓰는 방식이다(kinodynamic 계획; [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|13장]]).
> 4. $\mathcal{C}_{\text{free}}$가 볼록하지 않기 때문이다. 두 점을 잇는 선분이 밖으로 나갈 수 있다. 여기서 $p_x(\lambda) = \cos(90°\lambda)+\sin(90°\lambda)$는 $1$에서 $\sqrt2$까지 올랐다 내려오므로, 양 끝은 닿기만 하는데 내부는 $0.4142\,\mathrm{m}$ 파고든다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 장치는 같은 **P2**, 노드 다섯도 같고 질의 $A \to B$도 같지만, 패널을 2장 과제의 벽인 $x \ge 1.5$에 다시 세운다.

1. **그리기.** 새로 작아진 장애물을 칠한 원환면 도표, 같은 $12 \times 12$ 격자 가위표, 같은 노드 다섯과 간선 열 개. 전에 점선이던 간선 중 어느 것이 실선이 되는지 표시하라.
2. **유도.** (a) 직통 간선 $A$–$B$를 다시 검사하라. $p_x(\lambda) = \cos(90°\lambda) + \sin(90°\lambda)$를 써서 새 벽에 대한 $d_{\max}$를 보고하라. (b) 전에 최악점이 $d = 0.0201$이던 $B$–$C$를 다시 검사하라. (c) 새 최단 경로와 그 비용, 그리고 옛 답 $\pi\sqrt2$ 대비 절약률을 구하라.
3. **해석.** $30°$에서 새 벽은 $144$개 노드 중 $9$개를 막고, 진짜 막힌 넓이는 원환면의 $8.515\,\%$다. 격자는 여전히 과소평가하는가, 몇 칸만큼인가? 그리고 벽이 움직였을 때 다시 계산해야 했던 것이 노드인지 간선인지 둘 다인지 말하고, 기하를 한 번 측량한 뒤 바뀌는 현장에서 로드맵을 캐시하는 일에 대해 그것이 무엇을 뜻하는지 말하라.

> [!tip]- 정답 · Solutions
> 1. 전에 점선이던 두 간선이 모두 실선이 되므로 다섯 노드 위에서 로드맵은 완전 그래프가 되고 직통 간선 $A$–$B$를 쓸 수 있다.
> 2. (a) $p_x$는 여전히 $\lambda = 0.5$에서 $\sqrt2 = 1.4142$로 최대지만 벽이 이제 $1.5$이므로 $d_{\max} = 1.4142 - 1.5 = -0.0858\,\mathrm{m}$. 자유이고 $8.6\,\mathrm{cm}$ 여유가 있다. (b) 그 간선 위의 모든 $d$가 정확히 $0.5$씩 내려가므로 최악점이 $0.0201 - 0.5 = -0.4799$가 된다. 자유다. (c) 최단 경로는 이제 직통 간선이고 비용은 $(\pi/2)\sqrt5 = 3.5124\,\mathrm{rad}$, $\pi\sqrt2$ 대비 $1 - 3.5124/4.4429 = 20.9\,\%$ 절약이다.
> 3. 여전히 과소평가한다. 진짜 넓이는 $0.08515 \times 144 = 12.3$칸어치인데 막힌 노드는 $9$개라 $3.3$칸 모자란다. 벽이 움직여도 노드의 *좌표*는 하나도 바뀌지 않았고 노드의 *딱지*는 전부 바뀌었으며, 간선 판정 열 개가 모두 무효가 되었다. 그래프의 기하는 로봇의 성질이고 점유는 세계의 성질이다. 따라서 로드맵은 검사할 때 쓴 세계가 유지되는 동안만 캐시해 재사용할 수 있다. 현장에서는 측량이 갱신될 때마다 검사를 다시 돌린다는 뜻이고, 표본은 그대로 두므로 다시 샘플링하는 것보다 싸다. PRM이 학습 단계와 질의 단계를 나누는 이유가 정확히 이것이다.

### 이 장 너머로

[[04-robotics/planning-decision-making|계획과 의사결정]]이 이 장을 A*, 표본 기반 계획, 궤적 최적화, TAMP, 불확실성, MPC, 학습된 계획기로 이어 준다.
