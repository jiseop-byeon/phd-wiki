---
title: "MR Ch.02 — Configuration Space"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P2, count the C-space dimension from Grübler, name its topology, and derive by hand the C-obstacle of the panel wall together with the two contact configurations on its boundary."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.2** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> An intuition for degrees of freedom plus the rotation representations of [[02-foundations/se3-geometry|SE(3) §2]] is enough — this chapter is the robotics track's real starting point. Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] is the object throughout.
> 자유도(DoF)의 직관과 [[02-foundations/se3-geometry|SE(3)]]의 회전 표현(§2)을 알고 있으면 충분하다 — 이 장이 로보틱스 트랙의 실질적 출발점이다. 전체에서 쓰는 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**다.

## English

**Core question**: what is the space of all possible "positions" of a robot, and what shape is it?

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], with its frozen numbers: a planar 2R arm, $L_1 = L_2 = 1\,\mathrm{m}$, base at the origin, $\theta_1$ measured from the $+x$ axis and $\theta_2$ the elbow angle relative to link 1. Elbow and tip are then

$$e(\theta) = (\cos\theta_1,\ \sin\theta_1), \qquad p(\theta) = e(\theta) + (\cos(\theta_1{+}\theta_2),\ \sin(\theta_1{+}\theta_2))$$

because each unit-length link contributes one unit vector at its own absolute angle, and the absolute angle of link 2 is $\theta_1 + \theta_2$. At the catalog pose $\theta = (0°, 90°)$ the elbow is at $(1,0)$ and the tip at $(1,1)$.

**The panel**, frozen here and reused by [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]], is the running task's wall: the rigid half-plane $x \ge 1$, whose face is the vertical line $x = 1$. That face contains the catalog target $(1,1)$. Both links are modelled as zero-thickness segments, so "collision" means a point of a link has $x > 1$.

### Homework diagram · 과제가 그릴 그림

Draw two panels side by side.

**Left — the workspace.** The base at the origin; the unit circle the elbow traces; the wall drawn as a vertical line at $x = 1$ with hatching to its right. Note that the wall is *tangent* to the elbow circle at $(1,0)$. Draw P2 twice: once at $(0°, 90°)$, where link 2 runs from $(1,0)$ to $(1,1)$ and lies flat along the face, and once at $(90°, -90°)$, where link 1 runs from the origin to $(0,1)$ and link 2 runs from $(0,1)$ to $(1,1)$, touching the face only at the tip. Mark the target $(1,1)$.

**Right — the C-space chart.** A square with $\theta_1$ on the horizontal axis and $\theta_2$ on the vertical, both from $-180°$ to $+180°$. Draw arrows on the left and right edges showing they are the same edge, and again on the top and bottom: that double identification is what makes the square a torus rather than a rectangle. Shade the region where the arm penetrates the panel — a lens that spans $\theta_1 \in (-90°, 90°)$ and pinches to a point at each end. Mark the two configurations from the left panel as dots on the shaded region's boundary, and label the boundary curve "contact".

The problem set asks for the same pair of drawings with the wall moved.

### Worked on the plant · 장치로 한 번 끝까지

**Step 1 — the dimension.** Grübler counts the ground link, so P2 as an open chain has $N = 3$ links (ground, upper arm, forearm), $J = 2$ revolute joints, each $f_i = 1$, and $m = 3$ in the plane:

$$\text{dof} = m(N - 1 - J) + \sum_i f_i = 3(3 - 1 - 2) + (1 + 1) = 0 + 2 = 2$$

so P2's configuration space is two-dimensional, and two numbers $(\theta_1, \theta_2)$ are a complete configuration. The first term vanishes because an open serial chain has $J = N - 1$, which is the pattern below.

**Step 2 — the shape.** Each joint angle lives on a circle $S^1$, and the two are independent, so $\mathcal{C} = S^1 \times S^1 = T^2$, a torus. The chart above is the torus cut open; every quantity on this page must be read modulo $360°$ in both axes.

**Step 3 — the C-obstacle, derived.** A configuration is in collision when some point of the arm has $x > 1$. The $x$-coordinate along a straight segment is linear in the parameter, so its maximum over a segment is attained at an endpoint, and the arm's three endpoints are the base $(x = 0)$, the elbow, and the tip. Therefore the deepest penetration is

$$d(\theta) = \max\bigl(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)\bigr) - 1$$

and the configuration collides exactly when $d(\theta) > 0$. Now simplify: $\cos\theta_1 \le 1$ always, with equality only at $\theta_1 = 0$, so the elbow term can never make $d$ positive — link 1 can touch the wall but never cross it, which is the tangency drawn in the left panel. The test collapses to one inequality:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in T^2 \;:\; \cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\,\}$$

because only the tip's $x$-coordinate can exceed the wall. Note that $L_1 = 1$ equals the wall distance; that is a fact about the catalog, not a general theorem, and the problem set breaks it.

> [!warning] Sign convention · 부호 약속
> On this page and on [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]], $d(\theta)$ is a **penetration depth**: positive inside the obstacle, zero at contact. MR's contact-kinematics chapter writes $d(q)$ for the signed *distance*, positive when the bodies are apart. Same information, opposite sign — check which one a source means before comparing numbers.
> 이 페이지와 [[04-robotics/modern-robotics/ch10-motion-planning|10장]]에서 $d(\theta)$는 **침투 깊이**다. 장애물 안에서 양수, 접촉에서 0이다. MR의 접촉 기구학 장은 $d(q)$를 부호 있는 *거리*로 써서 떨어져 있을 때 양수다. 정보는 같고 부호가 반대이니, 숫자를 비교하기 전에 출처가 어느 쪽을 뜻하는지 확인해야 한다.

**Step 4 — the boundary, in numbers.** Put $\varphi = \theta_1 + \theta_2$, the forearm's absolute angle. The boundary $\cos\theta_1 + \cos\varphi = 1$ solves as $\varphi = \pm\arccos(1 - \cos\theta_1)$, which has a solution only when $0 \le 1 - \cos\theta_1 \le 1$, i.e. $\cos\theta_1 \ge 0$:

| $\theta_1$ | $\cos\theta_1$ | needed $\cos\varphi$ | $\varphi$ | $\theta_2 = \varphi - \theta_1$ |
|---:|---:|---:|---:|---|
| $0°$ | $1$ | $0$ | $\pm 90°$ | $+90°$ or $-90°$ |
| $30°$ | $0.8660$ | $0.1340$ | $\pm 82.30°$ | $52.30°$ or $-112.30°$ |
| $60°$ | $0.5$ | $0.5$ | $\pm 60°$ | $0°$ or $-120°$ |
| $90°$ | $0$ | $1$ | $0°$ | $-90°$ (the pinch) |
| $>90°$ | $<0$ | $>1$ | none | region is empty |

The row $\theta_1 = 60°,\ \theta_2 = 0°$ is worth checking by hand: the arm is straight at $60°$, so the tip is at $(2\cos 60°,\ 2\sin 60°) = (1,\ 1.732)$, exactly on the face. The rows mirror for negative $\theta_1$, so the obstacle is a closed lens spanning $\theta_1 \in [-90°, 90°]$ and pinching to a single point at each end.

**Step 5 — how much of the torus is lost.** The change of variables $(\theta_1, \theta_2) \mapsto (\theta_1, \varphi)$ has unit Jacobian determinant, so it preserves area on the torus, and the blocked area is

$$A = \int_{-\pi/2}^{\pi/2} 2\arccos(1 - \cos u)\,du = 7.2949\ \mathrm{rad}^2$$

since for each admissible $\theta_1 = u$ the forbidden $\varphi$ interval has length $2\arccos(1-\cos u)$. The whole torus has area $4\pi^2 = 39.478\ \mathrm{rad}^2$, so the panel costs **18.478 %** of P2's configuration space.

**Step 6 — the two contact configurations.** Both inverse-kinematics solutions for the tip at $(1,1)$ sit on the boundary, and the arithmetic is one line each:

- $\theta = (0°, 90°)$: $\cos 0° + \cos 90° = 1 + 0 = 1$, so $d = 0$.
- $\theta = (90°, -90°)$: $\cos 90° + \cos 0° = 0 + 1 = 1$, so $d = 0$.

They are the same point of task space and two different points of C-space, and they are not equivalent contacts: at $(0°,90°)$ link 2 lies flush along the face over its whole length, while at $(90°,-90°)$ only the tip touches. The C-space picture says "both on $\partial\mathcal{C}_{\text{obs}}$" and stops; which contact the tool actually makes is a workspace question.

**Step 7 — what contact does to the dimension.** Requiring the tip to stay on the face is the single equation $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$, one independent holonomic constraint, so the set of configurations that maintain contact has dimension $2 - 1 = 1$: it is exactly the boundary curve drawn in the diagram. The obstacle *region* removes no dimension — it is an open subset of a 2-D space and is still 2-D. **An inequality carves; an equality reduces.** That distinction is the whole content of the next section.

### 1. Configuration, degrees of freedom, and Grübler

- **Configuration** = a complete specification of every point of the robot; the minimum
  number of coordinates needed = **degrees of freedom (dof)**. C-space = the set of all
  configurations.
- **Grübler's formula**: for a mechanism of $N$ links **counting the ground link** and $J$ joints with joint freedoms $f_i$:
  $\text{dof} = m(N - 1 - J) + \sum_i f_i$ ($m = 3$ planar, $6$ spatial). Worked: the planar
  four-bar → $3(4-1-4)+4 = 1$ dof — one number describes the whole mechanism.
- **Topology matters**: a 2R arm's C-space is a torus ($T^2 = S^1 \times S^1$), not a plane —
  angles wrap. This is exactly why naive angle regression breaks
  ([[02-foundations/se3-geometry|8. SE(3) §2]]) and why "C-space distance" needs care.
- Representations: **explicit** (minimal coordinates, may have singularities — e.g. Euler angles at gimbal lock, where two of the three angles turn the same axis; [[02-foundations/se3-geometry|SE(3) §2]]) vs
  **implicit** (embed in higher-dim space + constraints — like rotation matrices with
  $R^\top R = I$). MR consistently chooses implicit — the same choice modern robot
  learning makes.
- **Task space vs C-space**: where the tool lives vs where the robot lives; the map
  between them is kinematics (ch.4–6). Keep *task space* apart from *workspace*: the task
  chooses the first, the robot's structure fixes the second.
- **Why the distinction matters**: points of the task space
  can lie outside the workspace entirely — which is exactly what makes a task infeasible
  for a given arm. A target 2 m from the base of an arm with 1 m of reach is a valid point
  of the task space but not of that arm's workspace.

> [!example] Worked example · 계산 예제
> Grübler: $\text{dof} = m(N-1-J) + \sum_i f_i$, with the ground counted in $N$.
> - **Planar four-bar** (MR Example 2.3): $m = 3$, links $N = 4$ (ground + crank + coupler + rocker), $J = 4$ revolute joints, each $f_i = 1$. $3(4-1-4) + 4 = -3 + 4 = 1$. Fix the crank angle and the whole loop is determined.
> - **Spatial 6R arm**: $m = 6$, links $N = 7$ (base + 6 moving links), $J = 6$ revolute joints, each $f_i = 1$. $6(7-1-6) + 6 = 0 + 6 = 6$ — enough to place the tool at any position and orientation in its reachable workspace.
>
> **Pattern**: for an open serial chain $J = N - 1$, so the first term vanishes and dof is just $\sum_i f_i$. Each closed loop subtracts constraints, which is why the four-bar's 4 joints give only 1 dof. The formula assumes independent constraints; special geometry can break it (MR Example 2.6).
>
> The homework's 1-dof claim *is* $3(4-1-4)+4=1$. Special geometry (MR 2.6) is what would falsify “Grübler always gives the mobility.” P2 reaching $(1,1)$ is in task space and in the workspace; two C-space points map to it (ch.6).

### 2. C-obstacles and free space, defined

A **C-obstacle** is a *subset of the configuration space*, not of the workspace. Given a rigid obstacle $\mathcal{O}$ in the world and the set $\mathcal{A}(\theta)$ of world points the robot body occupies at configuration $\theta$, the definition has exactly two conditions — it is a set of configurations, and membership is decided by intersection of bodies:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in \mathcal{C} \;:\; \mathcal{A}(\theta) \cap \mathcal{O} \neq \varnothing\,\}, \qquad \mathcal{C}_{\text{free}} = \mathcal{C} \setminus \mathcal{C}_{\text{obs}}$$

where $\mathcal{C}$ is the whole configuration space, so $\mathcal{C}_{\text{free}}$ is everything the robot may legally be. The point of the definition is that it turns a robot of some shape moving among obstacles into a *point* moving in $\mathcal{C}_{\text{free}}$, which is why every planner in [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] is written for a point.

- **Example**: the lens derived above, $\{\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\}$, occupying 18.478 % of P2's torus. It was obtained not by drawing the wall in C-space — the wall has no picture there — but by evaluating the workspace collision test at each configuration.
- **Non-example**: the wall itself, $\{x \ge 1\}$. A workspace region is not a C-obstacle, and the two do not even have the same dimension in general; a point obstacle in a 2-D workspace becomes a *curve* in a 2-D C-space.
- **Why it matters**: the shape of $\mathcal{C}_{\text{obs}}$, not the shape of the wall, decides whether a planner's straight-line edge is legal. [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] checks exactly this set, and this page is where its test comes from.

### 3. Holonomic and nonholonomic constraints, defined

A **constraint** on a mechanism is a condition its motion must satisfy. Two kinds, distinguished by one test — whether the condition can be written without velocities.

- A **holonomic constraint** is an equation on configuration alone, $g(\theta) = 0$. Each independent one reduces the dimension of the configuration space by one, because it confines $\theta$ to a level set of $g$. *Example*: P2's tip held on the panel face, $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$, leaving a 1-D contact curve. *Example*: a closed loop, which is why the four-bar has 1 dof and not 4.
- A **nonholonomic constraint** is an equation on velocity, $A(\theta)\dot\theta = 0$, that is *not* the time derivative of any $g(\theta) = 0$. It removes a direction of motion at every configuration but removes no dimension from the reachable set. *Example*: a wheel that cannot slide sideways ([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|ch.13]]): a car reaches every pose, just not along every path.
- **Non-example of the distinction**: "the tip must stay outside the panel" is neither, because it is an *inequality*. It removes no dimension and no direction; it deletes an open region. Confusing the three is the standard way a dof count comes out wrong.

**Wiki connections**: C-space is the "state" half of every
[[02-foundations/rl-basics|MDP]] for robots; VLA action spaces are coordinates on it.

### Self-check

1. How many numbers describe the configuration of a planar differential-drive robot, and what is the constraint?
2. Use Grübler's formula on a planar slider-crank (4 links, 3 revolute + 1 prismatic joint).
3. Why does the 2R arm's C-space being a torus $T^2$ rather than the plane $\mathbb{R}^2$ cause trouble for learned angle regression?
4. P2 is at $\theta = (45°, 0°)$. Compute $d(\theta)$ for the panel and say what the arm is doing.

> [!tip]- Answers
> 1. Three for the chassis: $(x, y, \theta)$ (five if the two wheel rolling angles are included, as MR §13.3 does). The nonholonomic constraint (no sideways slip) restricts *velocities*, not reachable chassis configurations — the robot can still reach any pose, just not by any path.
> 2. $\text{dof} = 3(4-1-4) + (3\cdot 1 + 1\cdot 1) = -3 + 4 = 1$. The prismatic joint contributes its one freedom exactly like a revolute one; what matters to the count is $f_i$, not the joint's kind.
> 3. $359°$ and $1°$ are neighbours on the circle but far apart in Euclidean distance, so a naive MSE regression is penalized enormously at the wrap point and learns a discontinuous target ([[02-foundations/se3-geometry|SE(3) §2]]).
> 4. The arm is straight at $45°$, so the tip is at $(\sqrt2, \sqrt2) = (1.4142, 1.4142)$ and $d = \cos 45° + \cos 45° - 1 = \sqrt2 - 1 = 0.4142\,\mathrm{m}$ — it is $41.4\,\mathrm{cm}$ inside the panel, the deepest point of the lens along the line $\theta_2 = 0$.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same plant **P2**, but the panel is rebuilt 0.5 m further out: the wall is now $x \ge 1.5$.

1. **Draw.** The same two-panel figure as above for the new wall. In the workspace panel, show that the wall no longer touches the elbow circle. In the C-space chart, shade the new obstacle and mark where it pinches. State in one sentence what happened to the catalog pose $(0°,90°)$.
2. **Derive.** (a) Write $d(\theta)$ for the new wall and argue again that only the tip term matters. (b) The boundary condition $\cos\theta_1 + \cos\varphi = 1.5$: find the two values of $\theta_1$ where the obstacle pinches, and the $\theta_2$ values on the boundary at $\theta_1 = 0°$ and $\theta_1 = 30°$. (c) For the *straight* arm, $\theta_2 = 0°$, find the range of $\theta_1$ that penetrates.
3. **Interpret.** The blocked fraction of the torus falls from 18.478 % to 8.515 %. Does the C-obstacle's *dimension* change? Does P2's dof change? And does the running task — put the tool on the panel at the catalog target — still have a solution?

> [!tip]- Solutions
> 1. Workspace: the elbow circle has radius 1 and the wall is at $x=1.5$, so the closest elbow point $(1,0)$ is $0.5\,\mathrm{m}$ clear — link 1 is now strictly free everywhere. C-space: a smaller lens, pinching at $\theta_1 = \pm 60°$. The catalog pose has $\cos 0° + \cos 90° = 1 < 1.5$, so $d = -0.5$: it is now an interior free configuration, no longer a contact configuration.
> 2. (a) $d(\theta) = \max(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)) - 1.5$; $\cos\theta_1 \le 1 < 1.5$, so the elbow term is always negative and only the tip can offend. (b) Pinch where $\cos\varphi$ must equal 1, i.e. $\cos\theta_1 = 0.5$, so $\theta_1 = \pm 60°$. At $\theta_1 = 0°$: $\cos\varphi = 0.5$, $\varphi = \pm 60°$, so $\theta_2 = \pm 60°$. At $\theta_1 = 30°$: $\cos\varphi = 1.5 - 0.8660 = 0.6340$, $\varphi = \pm 50.66°$, so $\theta_2 = 20.66°$ or $-80.66°$. (c) Straight arm: tip at $2\cos\theta_1 > 1.5$, i.e. $\cos\theta_1 > 0.75$, so $|\theta_1| < 41.41°$.
> 3. The dimension does not change: $\mathcal{C}_{\text{obs}}$ is an open subset of a 2-D space and stays 2-D, smaller but not thinner. P2's dof is still 2, because Grübler counts links and joints and neither moved — obstacles are inequalities and never enter the count. The task loses its solution as stated: the catalog target $(1,1)$ has $x = 1 < 1.5$ and is no longer on the face, so the contact target must be respecified. The nearest face point straight out is $(1.5, 1)$, at radius $\sqrt{1.5^2+1^2} = 1.803 < 2$, so it is still inside the workspace and the new task is feasible.

## 한국어

**핵심 질문**: 로봇의 가능한 "자세" 전체의 공간은 무엇이고, 그 모양은 어떠한가?

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**를 고정된 숫자 그대로 쓴다. 평면 2R 팔, $L_1 = L_2 = 1\,\mathrm{m}$, 베이스는 원점, $\theta_1$은 $+x$축 기준, $\theta_2$는 링크 1에 대한 상대 엘보 각. 엘보와 말단은

$$e(\theta) = (\cos\theta_1,\ \sin\theta_1), \qquad p(\theta) = e(\theta) + (\cos(\theta_1{+}\theta_2),\ \sin(\theta_1{+}\theta_2))$$

이다. 길이 1인 링크가 각자의 절대각 방향 단위 벡터를 하나씩 더하고, 링크 2의 절대각이 $\theta_1 + \theta_2$이기 때문이다. 카탈로그 자세 $\theta = (0°, 90°)$에서 엘보는 $(1,0)$, 말단은 $(1,1)$.

**패널**은 여기서 고정하고 [[04-robotics/modern-robotics/ch10-motion-planning|10장]]이 그대로 쓴다. 관통 과제의 벽이며, 강체 반평면 $x \ge 1$이고 그 면은 수직선 $x = 1$이다. 이 면이 카탈로그 목표 $(1,1)$을 포함한다. 두 링크는 두께 0인 선분으로 모형화하므로, 충돌이란 링크의 어떤 점이 $x > 1$이 되는 것이다.

### 과제가 그릴 그림 · Homework diagram

그림 두 개를 나란히 그린다.

**왼쪽 — 작업 영역.** 원점의 베이스, 엘보가 그리는 단위원, $x = 1$의 수직선으로 그린 벽(오른쪽에 빗금). 벽은 엘보 원에 $(1,0)$에서 *접한다*는 점을 표시한다. P2를 두 번 그린다. $(0°, 90°)$에서는 링크 2가 $(1,0)$에서 $(1,1)$로 가며 면에 완전히 붙어 눕고, $(90°, -90°)$에서는 링크 1이 원점에서 $(0,1)$로, 링크 2가 $(0,1)$에서 $(1,1)$로 가서 말단만 면에 닿는다. 목표 $(1,1)$을 표시한다.

**오른쪽 — C-space 도표.** 가로축 $\theta_1$, 세로축 $\theta_2$, 둘 다 $-180°$에서 $+180°$인 정사각형. 좌·우 변이 같은 변임을 화살표로, 위·아래 변도 같은 변임을 화살표로 표시한다. 이 두 겹의 동일시가 정사각형을 직사각형이 아니라 원환면으로 만든다. 팔이 패널을 파고드는 영역을 칠한다 — $\theta_1 \in (-90°, 90°)$에 걸치고 양 끝에서 한 점으로 오므라드는 렌즈 모양이다. 왼쪽 그림의 두 자세를 그 영역 경계 위의 점으로 찍고, 경계 곡선에 "접촉"이라고 쓴다.

과제는 벽을 옮긴 채로 같은 그림 두 장을 요구한다.

### 장치로 한 번 끝까지 · Worked on the plant

**1단계 — 차원.** 그뤼블러는 접지 링크를 세므로, 열린 체인 P2는 링크 $N = 3$(접지, 상완, 전완), 회전관절 $J = 2$, 각 $f_i = 1$, 평면이므로 $m = 3$:

$$\text{dof} = m(N - 1 - J) + \sum_i f_i = 3(3 - 1 - 2) + (1 + 1) = 0 + 2 = 2$$

따라서 P2의 컨피규레이션 공간은 2차원이고, 숫자 두 개 $(\theta_1, \theta_2)$가 완전한 컨피규레이션이다. 열린 직렬 체인은 $J = N - 1$이라 첫 항이 사라지는데, 이것이 아래의 패턴이다.

**2단계 — 모양.** 각 관절각은 원 $S^1$ 위에 살고 둘은 독립이므로 $\mathcal{C} = S^1 \times S^1 = T^2$, 즉 원환면이다. 위의 도표는 그 원환면을 잘라 편 것이고, 이 페이지의 모든 양은 두 축 모두에서 $360°$로 나눈 나머지로 읽어야 한다.

**3단계 — C-장애물 유도.** 팔의 어떤 점이 $x > 1$이면 충돌이다. 선분 위에서 $x$ 좌표는 매개변수의 일차 함수이므로 최댓값은 끝점에서 나오고, 팔의 끝점은 베이스($x = 0$), 엘보, 말단 셋뿐이다. 따라서 가장 깊은 침투는

$$d(\theta) = \max\bigl(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)\bigr) - 1$$

이고 $d(\theta) > 0$일 때 정확히 충돌이다. 여기서 정리하면, $\cos\theta_1 \le 1$이 항상 성립하고 등호는 $\theta_1 = 0$에서만 나오므로 엘보 항은 $d$를 양수로 만들 수 없다. 링크 1은 벽에 닿을 수는 있어도 넘을 수 없고, 이것이 왼쪽 그림의 접선 관계다. 검사는 부등식 하나로 줄어든다:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in T^2 \;:\; \cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\,\}$$

말단의 $x$만 벽을 넘을 수 있기 때문이다. 단 $L_1 = 1$이 벽까지의 거리와 같다는 사실은 카탈로그의 성질이지 일반 정리가 아니며, 과제가 이 조건을 깬다.

**4단계 — 경계를 숫자로.** $\varphi = \theta_1 + \theta_2$를 전완의 절대각이라 두면 경계 $\cos\theta_1 + \cos\varphi = 1$은 $\varphi = \pm\arccos(1 - \cos\theta_1)$로 풀리고, 해가 있으려면 $0 \le 1 - \cos\theta_1 \le 1$, 즉 $\cos\theta_1 \ge 0$이어야 한다:

| $\theta_1$ | $\cos\theta_1$ | 필요한 $\cos\varphi$ | $\varphi$ | $\theta_2 = \varphi - \theta_1$ |
|---:|---:|---:|---:|---|
| $0°$ | $1$ | $0$ | $\pm 90°$ | $+90°$ 또는 $-90°$ |
| $30°$ | $0.8660$ | $0.1340$ | $\pm 82.30°$ | $52.30°$ 또는 $-112.30°$ |
| $60°$ | $0.5$ | $0.5$ | $\pm 60°$ | $0°$ 또는 $-120°$ |
| $90°$ | $0$ | $1$ | $0°$ | $-90°$ (오므라드는 점) |
| $>90°$ | $<0$ | $>1$ | 없음 | 영역이 비어 있다 |

$\theta_1 = 60°,\ \theta_2 = 0°$ 행은 손으로 확인할 값이 있다. 팔이 $60°$로 곧게 펴지므로 말단은 $(2\cos 60°,\ 2\sin 60°) = (1,\ 1.732)$, 정확히 면 위다. 음의 $\theta_1$에서 좌우 대칭이므로 장애물은 $\theta_1 \in [-90°, 90°]$에 걸치고 양 끝에서 한 점으로 오므라드는 닫힌 렌즈다.

**5단계 — 원환면을 얼마나 잃는가.** 변수변환 $(\theta_1, \theta_2) \mapsto (\theta_1, \varphi)$는 야코비 행렬식이 1이라 원환면 위의 넓이를 보존하고, 막힌 넓이는

$$A = \int_{-\pi/2}^{\pi/2} 2\arccos(1 - \cos u)\,du = 7.2949\ \mathrm{rad}^2$$

이다. 허용되는 각 $\theta_1 = u$마다 금지된 $\varphi$ 구간의 길이가 $2\arccos(1-\cos u)$이기 때문이다. 원환면 전체 넓이는 $4\pi^2 = 39.478\ \mathrm{rad}^2$이므로, **패널은 P2 컨피규레이션 공간의 18.478 %를 가져간다.**

**6단계 — 접촉 자세 둘.** 말단을 $(1,1)$에 두는 역기구학 해 두 개가 모두 경계 위에 있고, 계산은 각각 한 줄이다:

- $\theta = (0°, 90°)$: $\cos 0° + \cos 90° = 1 + 0 = 1$이므로 $d = 0$.
- $\theta = (90°, -90°)$: $\cos 90° + \cos 0° = 0 + 1 = 1$이므로 $d = 0$.

둘은 작업 공간의 같은 점이고 C-space의 다른 두 점이며, 같은 접촉도 아니다. $(0°,90°)$에서는 링크 2가 면에 전 길이로 붙어 눕고, $(90°,-90°)$에서는 말단만 닿는다. C-space 그림은 "둘 다 $\partial\mathcal{C}_{\text{obs}}$ 위"라고만 말하고 멈춘다. 도구가 실제로 어떤 접촉을 하는지는 작업 영역의 질문이다.

**7단계 — 접촉이 차원에 하는 일.** 말단이 면 위에 머물라는 요구는 $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$ 하나, 독립인 홀로노믹 제약 하나이므로, 접촉을 유지하는 자세들의 집합은 차원 $2 - 1 = 1$이다. 바로 그림의 경계 곡선이다. 장애물 *영역*은 차원을 줄이지 않는다. 2차원 공간의 열린 부분집합이라 여전히 2차원이다. **부등식은 깎고, 등식은 줄인다.** 다음 절이 통째로 이 구별에 관한 것이다.

### 1. 컨피규레이션·자유도·그뤼블러

- **컨피규레이션** = 로봇 모든 점의 완전한 지정; 필요한 최소 좌표 수 = **자유도(dof)**.
  C-space = 모든 컨피규레이션의 집합.
- **그뤼블러 공식**: **접지 링크를 포함해** 링크 $N$개, 관절 $J$개, 관절 자유도 $f_i$인 기구에서
  $\text{dof} = m(N - 1 - J) + \sum_i f_i$ ($m = 3$ 평면, $6$ 공간). 계산 예: 평면 4절
  링크 → $3(4-1-4)+4 = 1$ 자유도 — 숫자 하나가 기구 전체를 기술한다.
- **위상이 중요하다**: 2R 팔의 C-space는 평면이 아니라 원환면($T^2 = S^1 \times S^1$) —
  각도는 감긴다. 순진한 각도 회귀가 깨지는 정확한 이유이고
  ([[02-foundations/se3-geometry|8. SE(3) §2]]), "C-space 거리"에 주의가 필요한 이유다.
- 표현: **명시적**(최소 좌표, 특이점 가능 — 예: 짐벌 락에서 세 오일러 각 중 둘이 같은 축을 돌리게 된다; [[02-foundations/se3-geometry|SE(3) §2]]) vs **암시적**(고차원에 묻고 제약 추가 —
  $R^\top R = I$인 회전 행렬처럼). MR은 일관되게 암시적을 고른다 — 현대 로봇 학습과 같은
  선택이다.
- **작업 공간(task space) vs C-space**: 도구가 사는 곳 vs 로봇이 사는 곳; 둘 사이의 사상이
  기구학이다(4~6장). *작업 공간*과 *작업 영역(workspace)*을 구별하라. 앞의 것은 과제가
  정하고, 뒤의 것은 로봇 구조가 정한다.
- **구별이 중요한 이유**: 작업 공간의 점이 작업 영역 밖에 있을 수 있고, 그것이
  바로 그 팔로는 그 과제를 못 한다는 뜻이다. 도달 거리가 1 m인 팔의 베이스에서 2 m 떨어진
  목표는 작업 공간의 올바른 점이지만 그 팔의 작업 영역에는 속하지 않는다.

> [!example] 계산 예제 · Worked example
> 그뤼블러: $\text{dof} = m(N-1-J) + \sum_i f_i$, 접지는 $N$에 포함한다.
> - **평면 4절 링크**(MR 예제 2.3): $m = 3$, 링크 $N = 4$(접지 + 크랭크 + 커플러 + 로커), 회전관절 $J = 4$, 각 $f_i = 1$. $3(4-1-4) + 4 = -3 + 4 = 1$. 크랭크 각 하나를 정하면 루프 전체가 정해진다.
> - **공간 6R 팔**: $m = 6$, 링크 $N = 7$(베이스 + 움직이는 링크 6), 회전관절 $J = 6$, 각 $f_i = 1$. $6(7-1-6) + 6 = 0 + 6 = 6$ — 도달 가능한 작업 영역 안에서 도구의 위치와 자세를 모두 정하기에 충분하다.
>
> **패턴**: 열린 직렬 체인은 $J = N - 1$이라 첫 항이 사라지고 자유도는 그냥 $\sum_i f_i$다. 닫힌 루프마다 제약이 빠지므로 4절 링크는 관절이 4개여도 자유도가 1이다. 공식은 제약이 서로 독립이라고 가정하며, 특수한 기하에서는 틀릴 수 있다(MR 예제 2.6).

### 2. C-장애물과 자유 공간의 정의

**C-장애물**은 작업 영역이 아니라 *컨피규레이션 공간의 부분집합*이다. 세계에 강체 장애물 $\mathcal{O}$가 있고 자세 $\theta$에서 로봇 몸체가 차지하는 세계 점들의 집합을 $\mathcal{A}(\theta)$라 할 때, 정의에 들어가는 조건은 정확히 두 개다. 자세들의 집합이라는 것, 그리고 소속 여부를 물체끼리의 교집합으로 판정한다는 것:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in \mathcal{C} \;:\; \mathcal{A}(\theta) \cap \mathcal{O} \neq \varnothing\,\}, \qquad \mathcal{C}_{\text{free}} = \mathcal{C} \setminus \mathcal{C}_{\text{obs}}$$

여기서 $\mathcal{C}$는 컨피규레이션 공간 전체이므로 $\mathcal{C}_{\text{free}}$가 로봇이 합법적으로 있을 수 있는 전부다. 이 정의의 요점은 모양을 가진 로봇이 장애물 사이를 지나가는 문제를 $\mathcal{C}_{\text{free}}$ 안을 움직이는 *점*의 문제로 바꾼다는 것이고, [[04-robotics/modern-robotics/ch10-motion-planning|10장]]의 모든 계획기가 점을 위해 쓰인 이유가 그것이다.

- **예**: 위에서 유도한 렌즈 $\{\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\}$, P2 원환면의 18.478 %. 이것은 C-space에 벽을 그려서 얻은 것이 아니라 — 벽은 거기에 그림이 없다 — 각 자세에서 작업 영역의 충돌 검사를 평가해서 얻은 것이다.
- **반례**: 벽 자체 $\{x \ge 1\}$. 작업 영역의 영역은 C-장애물이 아니고, 일반적으로 차원조차 같지 않다. 2차원 작업 영역의 점 장애물은 2차원 C-space에서 *곡선*이 된다.
- **왜 중요한가**: 계획기의 직선 간선이 합법인지를 결정하는 것은 벽의 모양이 아니라 $\mathcal{C}_{\text{obs}}$의 모양이다. [[04-robotics/modern-robotics/ch10-motion-planning|10장]]이 검사하는 것이 정확히 이 집합이고, 그 검사가 나오는 곳이 이 페이지다.

### 3. 홀로노믹 제약과 비홀로노믹 제약의 정의

기구에 걸린 **제약**은 그 운동이 만족해야 하는 조건이다. 속도 없이 쓸 수 있는가 하나로 두 종류가 갈린다.

- **홀로노믹 제약**은 자세만의 방정식 $g(\theta) = 0$이다. 독립인 것 하나마다 컨피규레이션 공간의 차원이 하나 줄어든다. $\theta$를 $g$의 등위집합에 가두기 때문이다. *예*: P2의 말단을 패널 면에 붙들어 두는 $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$, 남는 것은 1차원 접촉 곡선. *예*: 닫힌 루프, 4절 링크의 자유도가 4가 아니라 1인 이유.
- **비홀로노믹 제약**은 속도에 대한 방정식 $A(\theta)\dot\theta = 0$인데, 어떤 $g(\theta) = 0$의 시간 미분도 아닌 것이다. 모든 자세에서 운동 방향 하나를 없애지만 도달 가능 집합의 차원은 줄이지 않는다. *예*: 옆으로 미끄러지지 못하는 바퀴([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|13장]]). 자동차는 모든 자세에 도달하지만 모든 경로로 가지는 못한다.
- **구별의 반례**: "말단은 패널 밖에 있어야 한다"는 둘 중 어느 것도 아니다. *부등식*이기 때문이다. 차원도 방향도 없애지 않고 열린 영역을 지울 뿐이다. 이 셋을 섞는 것이 자유도 계산이 틀리는 표준적인 방식이다.

**위키 연결**: C-space는 로봇 [[02-foundations/rl-basics|MDP]]의 "상태" 절반이고, VLA 행동
공간은 그 위의 좌표다.

### 스스로 점검

1. 평면 차동 구동(differential-drive) 로봇의 컨피규레이션은 숫자 몇 개로 기술되고, 제약은 무엇인가?
2. 그뤼블러 공식으로 평면 슬라이더-크랭크(링크 4, 회전관절 3 + 직동관절 1)의 자유도를 계산하라.
3. 2R 팔의 C-space가 평면 $\mathbb{R}^2$가 아니라 원환면 $T^2$라는 사실이 학습(각도 회귀)에서 왜 문제가 되는가?
4. P2가 $\theta = (45°, 0°)$에 있다. 패널에 대한 $d(\theta)$를 계산하고 팔이 무엇을 하고 있는지 말하라.

> [!tip]- 정답
> 1. 차체만 보면 $(x, y, \theta)$ 세 개다(MR §13.3처럼 두 바퀴의 회전각까지 넣으면 다섯). 비홀로노믹 제약(옆 미끄럼 불가)은 *속도*를 제한할 뿐 도달 가능한 차체 자세를 제한하지 않는다. 어떤 자세에도 갈 수 있고, 다만 아무 경로로나 가지는 못한다.
> 2. $\text{dof} = 3(4-1-4) + (3\cdot 1 + 1\cdot 1) = -3 + 4 = 1$. 직동관절도 회전관절과 똑같이 자유도 하나를 보탠다. 계산에 들어가는 것은 관절의 종류가 아니라 $f_i$다.
> 3. $359°$와 $1°$는 원 위에서 이웃인데 유클리드 거리로는 멀다. 순진한 MSE 회귀는 각이 감기는 지점에서 큰 벌점을 받고 불연속인 목표를 학습하게 된다([[02-foundations/se3-geometry|SE(3) §2]]).
> 4. 팔이 $45°$로 곧게 펴져 말단이 $(\sqrt2, \sqrt2) = (1.4142, 1.4142)$이므로 $d = \cos 45° + \cos 45° - 1 = \sqrt2 - 1 = 0.4142\,\mathrm{m}$다. 패널 안으로 $41.4\,\mathrm{cm}$ 들어가 있고, $\theta_2 = 0$ 선 위에서 렌즈가 가장 깊은 지점이다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 장치는 같은 **P2**, 다만 패널을 0.5 m 뒤로 다시 세운다. 벽은 이제 $x \ge 1.5$.

1. **그리기.** 새 벽에 대해 위와 같은 두 장짜리 그림. 작업 영역 그림에서는 벽이 더 이상 엘보 원에 닿지 않음을 보여라. C-space 도표에서는 새 장애물을 칠하고 오므라드는 지점을 표시하라. 카탈로그 자세 $(0°,90°)$에 무슨 일이 일어났는지 한 문장으로 쓰라.
2. **유도.** (a) 새 벽의 $d(\theta)$를 쓰고, 다시 말단 항만 문제가 됨을 논증하라. (b) 경계 조건 $\cos\theta_1 + \cos\varphi = 1.5$에서 장애물이 오므라드는 $\theta_1$ 두 값과, $\theta_1 = 0°$ 및 $\theta_1 = 30°$에서 경계 위의 $\theta_2$ 값을 구하라. (c) *곧게 편* 팔 $\theta_2 = 0°$에 대해 패널을 파고드는 $\theta_1$ 범위를 구하라.
3. **해석.** 원환면에서 막힌 비율이 18.478 %에서 8.515 %로 줄었다. C-장애물의 *차원*이 바뀌는가? P2의 자유도가 바뀌는가? 그리고 관통 과제 — 도구를 카탈로그 목표의 패널에 붙이기 — 는 여전히 해가 있는가?

> [!tip]- 정답 · Solutions
> 1. 작업 영역: 엘보 원의 반지름이 1이고 벽이 $x=1.5$이므로 가장 가까운 엘보 점 $(1,0)$도 $0.5\,\mathrm{m}$ 떨어진다. 링크 1은 이제 어디서나 엄격히 자유다. C-space: 더 작은 렌즈, $\theta_1 = \pm 60°$에서 오므라든다. 카탈로그 자세는 $\cos 0° + \cos 90° = 1 < 1.5$이므로 $d = -0.5$. 접촉 자세가 아니라 내부의 자유 자세가 되었다.
> 2. (a) $d(\theta) = \max(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)) - 1.5$이고 $\cos\theta_1 \le 1 < 1.5$이므로 엘보 항은 항상 음수다. 말단만 위반할 수 있다. (b) $\cos\varphi$가 1이어야 하는 곳, 즉 $\cos\theta_1 = 0.5$에서 오므라들므로 $\theta_1 = \pm 60°$. $\theta_1 = 0°$: $\cos\varphi = 0.5$, $\varphi = \pm 60°$, 따라서 $\theta_2 = \pm 60°$. $\theta_1 = 30°$: $\cos\varphi = 1.5 - 0.8660 = 0.6340$, $\varphi = \pm 50.66°$, 따라서 $\theta_2 = 20.66°$ 또는 $-80.66°$. (c) 곧게 편 팔: 말단이 $2\cos\theta_1 > 1.5$, 즉 $\cos\theta_1 > 0.75$이므로 $|\theta_1| < 41.41°$.
> 3. 차원은 바뀌지 않는다. $\mathcal{C}_{\text{obs}}$는 2차원 공간의 열린 부분집합이라 더 작아질 뿐 여전히 2차원이다. P2의 자유도도 여전히 2다. 그뤼블러는 링크와 관절을 세는데 둘 다 그대로이고, 장애물은 부등식이라 애초에 계산에 들어가지 않는다. 과제는 쓰인 대로는 해를 잃는다. 카탈로그 목표 $(1,1)$은 $x = 1 < 1.5$라 더 이상 면 위가 아니므로 접촉 목표를 다시 정해야 한다. 곧장 밖으로 가장 가까운 면 위의 점은 $(1.5, 1)$이고 반지름이 $\sqrt{1.5^2+1^2} = 1.803 < 2$이라 작업 영역 안에 있으므로 새 과제는 실행 가능하다.
