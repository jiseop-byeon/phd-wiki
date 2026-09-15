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

> [!note] First pass · 처음이라면
> Read §1 — five words the literature uses interchangeably and should not — then §2, then §4's worked example. §5 through §8 are a survey; read the family a paper belongs to rather than all of them.

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
  cell observed occupied a thousand times needs on the order of a thousand contrary observations to flip (about 2,100 with OctoMap's default +0.85/−0.4 log-odds increments) —
  which is why implementations add an explicit **clamping** range (proposed by Yguel et al. 2007 and adopted by OctoMap) so
  the map can still adapt when the world changes. A cell reads as *free*, *occupied*, or
  **unknown**, and the third is the one beginners drop: unknown is not free, and the difference is what exploration is about.
- **Inflation** — a planner that treats the robot as a point (the figure below) has to grow
  the obstacles instead. Inflating occupied cells by the robot radius produces a C-space
  obstacle directly on the grid **for a circular robot** — for any other footprint it is an
  approximation, which is why a stack like Nav2 still runs a separate footprint collision
  check. Adding a decaying cost outside that radius produces a margin the planner prefers not
  to enter.
- **Costmap** — an occupancy grid whose cells carry *traversal cost* rather than a binary.
  Cost combines inflation with whatever else the robot should avoid: unknown space, rough
  terrain, one-way regions, keep-out zones. **A costmap is where a policy preference stops
  being a plan and becomes geometry** — and it is the representation
  [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy §1]] argues *is*
  the right carrier for a learned affordance, since the same scene yields different costmaps for
  different robots. What that page rejects is the plain occupancy grid, the geometric predicate.
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

Dijkstra uses no informative heuristic. A* is optimal on a graph under the appropriate admissibility/consistency conditions. *Admissible* means $h$ never **over**estimates the true remaining cost, so the estimate is optimistic; *consistent* means it additionally never drops by more than the cost of the edge just traversed, so the estimates agree with each other along a path. This theorem does not guarantee that a discretized graph represents every feasible continuous robot motion.

**Think of the frontier as unfinished routes.** Each queued node represents a route that has reached somewhere but has not yet been explored onward. g records what that route has already cost. h estimates the remaining work, and f decides which unfinished route deserves attention next. Expanding a node means considering its outgoing edges; it does not mean the robot physically moves there.

If a cheaper route reaches an already encountered node, its best-known cost and parent may need updating. This bookkeeping is part of the algorithm, not a detail that can be ignored when quoting optimality. For nonnegative edge costs, consistency makes heuristic values cooperate with the graph's edges; admissibility alone requires appropriate handling of revisits.

**Check your understanding.** The heuristic is a lower-bound estimate for the graph problem, not permission to ignore obstacles in the final route. A straight-line distance can be useful precisely because it is optimistic, while collision checking still decides which graph connections are allowed. Search efficiency and physical feasibility are separate checks.

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
| Feedback / potential field | attractive-to-goal plus repulsive-from-obstacle fields, navigation functions | Produce an action for *every* state rather than one path — cheap and reactive, but a plain potential field has local minima that trap the robot short of the goal |
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



### 5.5 Planning under dynamics: kinodynamic search, lattices, and flatness

A robot that cannot move in every direction at every speed needs a planner whose edges are motions the machine can execute, so the straight-line connection that grid edges and §5's sampling tree assume has to be replaced by a steering rule that respects the dynamics.

**Why a geometric path is not enough.** Three kinds of constraint break the straight-segment assumption:

- **Nonholonomic.** A car has no sideways velocity and a minimum turning radius, so a path with a corner or a sideways shift is undrivable as written, even though the car can still reach every pose ([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR ch.13]] explains why).
- **Dynamic.** An excavator boom carries inertia and a crane's suspended load swings, so the plan must also keep accelerations low enough that the machine stays stable and the load does not oscillate.
- **Bounds.** Velocity, acceleration, and actuator limits hold even for a robot that can move in any direction.

*Kinodynamic* originally named planning under velocity and acceleration bounds; it now covers any planning in a state space with $\dot x = f(x,u)$. A problem can be nonholonomic, kinodynamic, or both: a car with a dynamics model is both. MR ch.10 names the sampling version and its local planners in one line; this section is the longer map.

**Exact shortest paths for a car in free space.**

- **Dubins (1957):** a forward-only car at constant speed with minimum turning radius $\rho$. Between any two poses $(x,y,\theta)$ the shortest path has at most three segments, each a full-lock left arc $L$, a full-lock right arc $R$, or a straight $S$. Only six *words* can be optimal: $LSL, LSR, RSL, RSR, LRL, RLR$. In the $CCC$ words the middle arc turns through more than $\pi$. The intuition is a shortest route around a bend: turn as tightly as allowed, drive straight, turn as tightly as allowed again — a gentler arc only adds length — and Dubins proved that three such pieces always suffice.
- **Reeds–Shepp (1990):** the same car allowed to reverse. The shortest path is one of a fixed list of fewer than fifty words, each at most five segments long with at most two gear changes (cusps).

Both are closed-form, so planners use them as a **steering function**, meaning an exact connection between two states. They also serve as the obstacle-free, turning-radius-aware half of the lattice heuristic in [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms]] §8. Two limits come with them. They ignore obstacles. And curvature jumps at every segment joint, so a real steering wheel cannot follow the corner exactly.

**Search over motion primitives.** A* itself is [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms]] §6; what changes here is what an edge is.

- **State lattice** (Pivtoraiko, Knepper & Kelly 2009). Discretize $(x,y,\theta)$, sometimes with curvature or speed, on a regular grid. Offline, solve boundary-value problems — find an input that drives the model from one given state to exactly another — for a small set of feasible primitives that start and end exactly on lattice states. The set is translation-invariant, so the same primitives are reused everywhere.
- **Hybrid A\*** (Dolgov, Thrun, Montemerlo & Diebel 2010). Expand a node by integrating the car model for a few steering values. Keep one *continuous* pose per discrete $(x,y,\theta)$ cell and prune later arrivals in the same cell. Try an analytic Reeds–Shepp shot to the goal as the search nears it, then smooth the result.

Their guarantees differ. A lattice planner's completeness or optimality claim is relative to its primitive set, not to the continuous problem. Hybrid A\*'s path is drivable, but the cell pruning gives up completeness and optimality even on the lattice.

[[04-robotics/ros2/navigation-nav2|Nav2]] ships both as its "feasible" planners.

**Sampling with dynamics.** *Kinodynamic RRT* (LaValle & Kuffner 2001) samples a state, finds the nearest tree node under a chosen metric, and extends it by integrating $\dot x = f(x,u)$ for some input and duration. That forward propagation needs no boundary-value solver, but new nodes never land exactly on the sampled state, and the metric choice matters. Karaman & Frazzoli (2011) showed that plain RRT converges to a suboptimal path with probability one; RRT\* and PRM\* restore asymptotic optimality by connecting each sample to neighbours within a radius that shrinks like $(\log n / n)^{1/d}$. That rate keeps on the order of $\log n$ samples in each ball, because the ball's volume scales as $r^d \propto \log n/n$ and there are $n$ samples: few enough that rewiring stays cheap, yet enough that the graph stays connected as samples multiply. FMT\* (Janson et al. 2015) reaches the same guarantee with a lazy dynamic-programming pass over a batch of samples that postpones collision checks. The asymptotically optimal versions for dynamical systems need an exact steering function plus its cost — Dubins or Reeds–Shepp for cars, a precomputed lattice, or flatness below.

**Differential flatness.** Some systems let you plan a few output curves freely and read every state and input off them. Fliess, Lévine, Martin & Rouchon (1995) call a system $\dot x = f(x,u)$ *flat* when there are outputs $z$ (as many as there are inputs) such that

$$x=\beta(z,\dot z,\dots,z^{(q)}),\qquad u=\gamma(z,\dot z,\dots,z^{(q)})$$

for a finite $q$, so any smooth curve $z(t)$ yields a state and input trajectory that satisfies the dynamics exactly. For the unicycle $\dot x = v\cos\theta,\ \dot y = v\sin\theta,\ \dot\theta = \omega$ with $z=(x,y)$:

$$\theta=\operatorname{atan2}(\dot y,\dot x),\qquad v=\sqrt{\dot x^2+\dot y^2},\qquad \omega=\frac{\dot x\ddot y-\dot y\ddot x}{\dot x^2+\dot y^2}$$

These hold because the velocity $(\dot x,\dot y)$ points along the heading with length $v$, so heading and speed are its angle and norm, and $\omega$ is the rate of that angle. The kinematic car adds a steering angle $\phi=\arctan(L\kappa)$, where $L$ is the wheelbase and $\kappa=\omega/v$ is the path curvature. That comes from the bicycle model: with the front wheel steered by $\phi$, the rear axle circles a centre at radius $R$ with $\tan\phi = L/R$, and $\kappa = 1/R$. A turning-radius limit is therefore a bound on the geometry of $z$, not on its timing.

For a quadrotor, Mellinger & Kumar (2011) use position and yaw as flat outputs. The rotors can push only along the body $z$ axis, so the acceleration the curve demands (plus gravity) fixes both the thrust magnitude and the direction that axis must point, which with yaw is the attitude. Differentiating once more says how fast the attitude must turn, so body rates come from jerk; once more gives angular acceleration, so torques come from snap. That is why they minimise snap.

**Why flatness turns planning into curve fitting.** Write $z(t)$ as polynomials. Boundary conditions on $z$ and its derivatives are then *linear* in the coefficients, so one linear solve gives a dynamically feasible trajectory. What remains are the inequality constraints — speed, curvature, obstacles. They are checked afterwards, fixed by time scaling ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]]), or handed to the optimisation of §6 with the polynomial coefficients as decision variables. Flatness removes the dynamics constraint from §6's program, not the obstacle constraints.

> [!example] Worked example · 계산 예제
> Take the flat output $z(t)=(t,\,t^2)$, a parabola, so $\dot x=1,\ \dot y=2t,\ \ddot x=0,\ \ddot y=2$. The formulas give $v=\sqrt{1+4t^2}$, $\omega=2/(1+4t^2)$, and curvature $\kappa=\omega/v=2/(1+4t^2)^{3/2}$.
>
> | $t$ | $\theta$ | $v$ | $\omega$ | finite-difference $\dot\theta$ | $\kappa$ |
> |---|---|---|---|---|---|
> | 0 | 0° | 1.000 | 2.000 | 2.000 | 2.000 |
> | 0.5 | 45.00° | 1.414 | 1.000 | 1.000 | 0.707 |
> | 1 | 63.43° | 2.236 | 0.400 | 0.400 | 0.179 |
>
> Integrating the unicycle from $(0,0,0)$ with these $v(t)$ and $\omega(t)$ (Euler, $\Delta t=10^{-4}$) ends at $(1.000, 1.000, 1.107\text{ rad})$, within $10^{-4}$ of $z(1)=(1,1)$ and $\theta(1)=\arctan 2$. The inputs really do reproduce the curve.
>
> **Now add a car with a 1 m minimum turning radius** ($\kappa\le 1$). At the vertex $\kappa=2$, a 0.5 m radius, and the bound is violated until $(1+4t^2)^{3/2}=2$, which gives $t\approx 0.383$. Driving slower does not help. Traversing the same parabola at half speed, $z(t)=(t/2,\,t^2/4)$, gives $v=0.5$ and $\omega=1$ at the vertex, and $\kappa$ is still 2. The fix is a different geometry.

```python
import numpy as np
xd, yd = lambda t: 1.0 + 0*t, lambda t: 2*t          # z(t) = (t, t^2)
xdd, ydd = lambda t: 0*t, lambda t: 2.0 + 0*t
theta = lambda t: np.arctan2(yd(t), xd(t))
v = lambda t: np.hypot(xd(t), yd(t))
omega = lambda t: (xd(t)*ydd(t) - yd(t)*xdd(t)) / (xd(t)*xd(t) + yd(t)*yd(t))
for t in [0.0, 0.5, 1.0]:
    h = 1e-5                                          # finite-difference check
    fd = (theta(t + h) - theta(t - h)) / (2*h)
    print(f"t={t}: theta={np.degrees(theta(t)):.2f} deg  v={v(t):.3f}  "
          f"omega={omega(t):.3f}  fd={fd:.3f}  kappa={omega(t)/v(t):.3f}")
dt, s = 1e-4, np.array([0.0, 0.0, 0.0])              # unicycle state (x, y, theta)
for t in np.arange(0, 1, dt):
    s = s + dt*np.array([v(t)*np.cos(s[2]), v(t)*np.sin(s[2]), omega(t)])
print("end state", s.round(3), "target (1, 1, %.3f)" % theta(1.0))
```

> [!warning] Pitfalls and what to check in papers
> - **Zero speed is a singularity.** When $\dot z\to 0$, $\theta=\operatorname{atan2}(0,0)$ is undefined and $\omega$'s denominator vanishes. Take $z(t)=(t^3,t^2)$: the heading is $-89.14°$ at $t=-0.01$ and $+89.14°$ at $t=+0.01$. That jump of almost $180°$ is a cusp, a gear change that a forward-speed parametrisation cannot express. Planners therefore keep interior points at nonzero speed, split trajectories at intended stops and reversals, and impose boundary headings through $\dot z(0)=v_0(\cos\theta_0,\sin\theta_0)$ with $v_0\neq 0$.
> - **"Optimal" relative to what?** A lattice planner is optimal over its primitive set, Hybrid A\* is not optimal at all, and a Dubins or Reeds–Shepp cost ignores obstacles. The Dubins distance is not even symmetric, so using it as a nearest-neighbour metric needs care.
> - **Check what survived smoothing.** After post-processing, check that curvature continuity, the turning-radius bound, and the speed and acceleration bounds still hold.
> - **Flatness is a property to verify, not assume.** The paper should name its flat outputs.
>
> **For construction machines.** Articulated wheel loaders steer by bending the frame, and tracked excavators turn by skid-steering with heavy slip. Both have turning-radius or slip constraints that a costmap path ignores. A crane or boom adds load-swing dynamics on top, which is why [[05-construction-robotics/earthmoving-heavy-machinery|heavy-machine autonomy]] needs this section's feasibility checks rather than a 2-D grid planner alone.

### 6. Trajectory optimization and MPC

A common formulation is the trajectory-optimization program of [[02-foundations/optimization|4. Optimization]] — read it as a running cost paid at every step plus a terminal cost at the end, with the physics and the obstacles as constraints:

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. dynamics, bounds, and collision constraints.}$$

- **Given:** initial state, model, goal, constraints, and cost.
- **Optimized:** state and/or input sequence.
- **Runtime:** offline planning or repeated online as MPC.
- **Caveat:** nonlinear dynamics and obstacle constraints usually create local, initialization-sensitive problems.

Direct shooting optimizes controls and simulates states. Direct transcription treats states and controls as variables. Collocation enforces dynamics at selected points. None automatically proves global optimality in a nonconvex robot problem.

**Unpack the subscripts as a proposed future.** x₀ is fixed by the current estimated state. Later x values describe predicted states, and u values are the inputs that would produce them under the model. Stage costs judge each part of the future, while the terminal cost values where the horizon ends. The dynamics constraints tie this imagined sequence together so the optimizer cannot choose attractive states disconnected from achievable motion.

MPC makes this formulation into feedback: execute the first input, observe the new state, and solve again. The unexecuted future still mattered because it influenced the first decision. Replanning then corrects discrepancies instead of assuming the entire prediction came true. An offline trajectory optimizer may solve a similar mathematical problem without performing this repeated feedback loop.

**Check your understanding.** A solver's feasible output is conditional on its initial state, model, discretization, and constraints. If state estimates are stale or a collision occurs between checked points, solving the optimization accurately is not enough. See the [trajectory-optimization notes](https://underactuated.mit.edu/trajopt.html) for the distinction between representing a trajectory and executing it with feedback.

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
> LaValle's [*Planning Algorithms*](http://lavalle.pl/planning/) is free and is the reference for the sampling-based half, though it is a 2006 book: it stops at probabilistic completeness and has neither RRT\* nor asymptotic optimality, which are Karaman and Frazzoli (2011); Tedrake's [*Underactuated Robotics*](https://underactuated.csail.mit.edu/) covers the trajectory-optimization half with code you can run.

### Self-check

1. Why can a collision-free path be dynamically infeasible?
2. What is lost when planning only in workspace rather than configuration space?
3. Why can trajectory optimization fail even when a feasible trajectory exists?
4. What evidence would support a “real-time closed-loop planner” claim?
5. A Hybrid A\* paper and a state-lattice paper both call their paths "optimal". Optimal with respect to what, in each case?
6. The parabola $z(t)=(t,t^2)$ violates a 1 m minimum turning radius near its vertex. Why does slowing down along the same curve not fix it?

> [!tip]- Answers
> 1. It may require impossible velocity, acceleration, torque, contact, or timing. 2. Robot geometry, joint limits, and multiple configurations for the same task pose. 3. The problem can be nonconvex and sensitive to initialization. 4. End-to-end latency distributions on specified hardware, execution with disturbances/dynamic obstacles, constraint violations and failures—not planner compute time alone. 5. The lattice planner is optimal only over its precomputed primitive set and resolution, so it can miss paths that need headings or curvatures the set lacks; Hybrid A\* is not optimal even on its grid, because it keeps one continuous pose per cell and prunes the rest. 6. The turning-radius limit bounds the curvature $\kappa=\omega/v$, which depends only on the geometry: at half speed the vertex has $v=0.5$ and $\omega=1$, so $\kappa$ is still 2. Only a different curve helps.

### Sources

- [Modern Robotics, Chapter 10](http://modernrobotics.org)
- [MIT Underactuated Robotics](https://underactuated.csail.mit.edu/)
- [OMPL: planning concepts](https://ompl.kavrakilab.org/)
- L. E. Dubins, "On curves of minimal length with a constraint on average curvature, and with prescribed initial and terminal positions and tangents," *American Journal of Mathematics* 79(3), 497–516, 1957. doi:10.2307/2372560
- J. A. Reeds, L. A. Shepp, "Optimal paths for a car that goes both forwards and backwards," *Pacific Journal of Mathematics* 145(2), 367–393, 1990. doi:10.2140/pjm.1990.145.367
- M. Pivtoraiko, R. A. Knepper, A. Kelly, "Differentially constrained mobile robot motion planning in state lattices," *Journal of Field Robotics* 26(3), 308–333, 2009.
- D. Dolgov, S. Thrun, M. Montemerlo, J. Diebel, "Path planning for autonomous vehicles in unknown semi-structured environments," *International Journal of Robotics Research* 29(5), 485–501, 2010.
- S. M. LaValle, J. J. Kuffner, "Randomized kinodynamic planning," *International Journal of Robotics Research* 20(5), 378–400, 2001. doi:10.1177/02783640122067453
- S. Karaman, E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *International Journal of Robotics Research* 30(7), 846–894, 2011. doi:10.1177/0278364911406761
- L. Janson, E. Schmerling, A. Clark, M. Pavone, "Fast marching tree: a fast marching sampling-based method for optimal motion planning in many dimensions," *International Journal of Robotics Research* 34(7), 883–921, 2015. doi:10.1177/0278364915577958
- M. Fliess, J. Lévine, P. Martin, P. Rouchon, "Flatness and defect of non-linear systems: introductory theory and examples," *International Journal of Control* 61(6), 1327–1361, 1995. doi:10.1080/00207179508921959
- D. Mellinger, V. Kumar, "Minimum snap trajectory generation and control for quadrotors," *IEEE International Conference on Robotics and Automation (ICRA)*, 2520–2525, 2011. doi:10.1109/ICRA.2011.5980409
- S. M. LaValle, *Planning Algorithms*, Cambridge University Press, 2006 — §14.1 (kinodynamic terminology) and §15.3 (Dubins and Reeds–Shepp curves).

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

> [!note] 처음이라면 · First pass
> 먼저 §1 — 문헌이 섞어 쓰지만 섞어 쓰면 안 되는 다섯 단어 — 그다음 §2, 그다음 §4의 계산 예제. §5~§8은 조망이니 전부가 아니라 지금 논문이 속한 계열만 읽어라.

### 1. Plan, path, trajectory, policy, controller

| 용어 | 의미 |
|---|---|
| Plan | 미래 결정·행동의 제안된 시퀀스 |
| Path | 시간 없는 기하학적 곡선 |
| Trajectory | 시간이 매겨진 상태·속도·(대개) 입력 |
| Policy | 가용 정보를 행동으로 사상하는 규칙 |
| Controller | 기준을 추종하거나 거동을 조절하는 피드백 시스템 |

플래너가 path를 내면 궤적 생성기가 시간을 매기고([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]
— 시간 스케일링, 경유점, 시간 최적 스케일링) 제어기가 추종한다. 계획은 과제 공간에 있는데
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
  로그 승산은 *유계가 아니어서*, 점유로 천 번 관측된 칸은 뒤집으려면 반대 관측이 천 번 단위로 필요하다(OctoMap 기본 로그 승산 증분 +0.85/−0.4이면 약 2,100번) —
  그래서 구현들은 명시적 **클램핑** 범위를 둔다(Yguel 외 2007이 제안하고 OctoMap이 채택). 세상이 바뀌었을 때 지도가
  적응할 수 있게 하려는 것이다. 칸은 *비어 있음*, *점유됨*, 그리고
  **미지**의 셋 중 하나이고, 초심자가 빠뜨리는 것이 셋째다. 미지는 비어 있음이 아니며,
  그 차이가 곧 탐색이 존재하는 이유다.
- **팽창(inflation)** — 로봇을 점으로 다루는 계획기(아래 그림)는 대신 장애물을 키워야 한다.
  점유 칸을 로봇 반경만큼 팽창시키면 **원형 로봇에 한해** 격자 위에서 바로 C-공간 장애물이
  된다 — 다른 형상에서는 근사이고, 그래서 Nav2 같은 스택은 별도의 footprint 충돌 검사를 따로
  돌린다. 그 바깥에 감쇠하는 비용을 더하면 계획기가 들어가기를 꺼리는 여유가 생긴다.
- **비용 지도(costmap)** — 칸이 이진값이 아니라 *통행 비용*을 담는 점유 격자다. 비용은
  팽창에 더해 로봇이 피해야 할 다른 모든 것을 합친다: 미지 영역, 거친 지형, 일방향 구역,
  진입 금지 구역. **비용 지도는 정책적 선호가 계획이기를 그만두고 기하가 되는 자리다** —
  [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성 §1]]이 학습된
  어포던스를 담기에 *맞는* 그릇이라고 논하는 바로 그 표현이다. 같은 장면이 로봇마다 다른
  costmap을 내놓기 때문이다. 그 페이지가 거부하는 것은 기하 술어인 점유 격자 쪽이고, 그것을 보려면 이것이
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
§6이 같은 층을 최적화 관점에서 다룬다. 고전적인 내비게이션 스택에서 학습되는 부분은 보통 지역 층이고 전역 탐색과 비용 지도는
건드리지 않는다. 다만 항상 그런 것은 아니다. 학습된 전역 계획기와 학습된 탐색 휴리스틱이
존재하고, [[04-robotics/semantic-language-navigation|19. §3]]의 end-to-end 계열은 스택 전체를
대체한다. **논문이 실제로 어느 층을 대체했는지 확인하라** — 그것이 그 결과가 주장할 수 있는
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

**프런티어를 아직 끝나지 않은 경로로 생각한다.** 대기 중인 노드는 어느 곳까지 도달했지만 그 뒤를 아직 탐색하지 않은 경로다. g는 이미 쓴 비용, h는 남은 일의 추정, f는 다음으로 볼 경로의 우선순위다. 노드를 확장한다는 것은 나가는 간선을 검토한다는 뜻이다. 로봇이 실제로 그곳으로 움직이는 것은 아니다.

이미 본 노드에 더 싼 경로가 도달하면 알려진 최저 비용과 부모를 갱신해야 할 수 있다. 최적성을 말할 때 생략해도 되는 구현 세부가 아니라 알고리즘의 일부다. 음수가 아닌 간선 비용에서 일관성은 휴리스틱과 간선 비용이 맞물리게 한다. 허용성만 있으면 재방문을 적절히 처리해야 한다.

**이해 확인.** 휴리스틱은 그래프 문제의 하한 추정이지 최종 경로에서 장애물을 무시할 허가가 아니다. 직선 거리는 낙관적이어서 유용할 수 있고, 실제 허용 연결은 충돌 검사가 정한다. 탐색 효율과 물리적 가능성은 별도 검사다.

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
| 피드백 / 퍼텐셜장 | 목표로 끌고 장애물에서 미는 장, 내비게이션 함수 | 경로 하나가 아니라 *모든* 상태에 대해 행동을 만든다 — 값싸고 반응적이지만, 단순한 퍼텐셜장에는 로봇을 목표 앞에서 가두는 국소 최솟값이 있다 |
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



### 5.5 동역학을 지키는 계획: kinodynamic 탐색, 격자, 평탄성

모든 방향으로 모든 속도로 움직일 수 없는 로봇에는 간선이 곧 그 기계가 실행할 수 있는 운동인 계획기가 필요하다. 그래서 격자의 간선과 §5의 표본 트리가 가정하는 직선 연결을, 동역학을 지키는 조향 규칙으로 바꿔야 한다.

**기하학적 경로만으로 부족한 이유.** 세 종류의 제약이 직선 구간 가정을 깬다.

- **비홀로노믹 제약.** 자동차에는 옆 방향 속도가 없고 최소 회전 반경이 있다. 그래서 모서리나 옆으로 비키는 구간이 있는 경로는 쓰인 그대로는 운전할 수 없다. 그래도 차는 모든 pose에 도달할 수 있다(이유는 [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR 13장]]).
- **동역학 제약.** 굴착기 붐에는 관성이 있고 크레인에 매달린 짐은 흔들린다. 그래서 계획은 기계가 안정을 유지하고 짐이 진동하지 않을 만큼 가속도를 낮게 지켜야 한다.
- **한계.** 속도·가속도·구동기 한계는 어느 방향으로든 움직일 수 있는 로봇에도 걸린다.

*kinodynamic*은 원래 속도·가속도 한계 아래의 계획을 가리켰고, 지금은 $\dot x = f(x,u)$인 상태 공간에서의 계획 전반을 뜻한다. 문제는 비홀로노믹이거나, kinodynamic이거나, 둘 다일 수 있다. 동역학 모델을 가진 자동차가 둘 다다. MR 10장은 표본 기반 판본과 그 지역 계획기를 한 줄로 짚고, 이 절은 그 긴 지도다.

**자유 공간에서 자동차의 정확한 최단 경로.**

- **Dubins (1957):** 일정 속도로 전진만 하고 최소 회전 반경이 $\rho$인 차. 임의의 두 pose $(x,y,\theta)$ 사이 최단 경로는 최대 세 구간이고, 각 구간은 최대 조향 좌회전 호 $L$, 최대 조향 우회전 호 $R$, 직진 $S$ 중 하나다. 최적일 수 있는 *단어*는 여섯 개뿐이다: $LSL, LSR, RSL, RSR, LRL, RLR$. $CCC$ 단어에서 가운데 호는 $\pi$보다 크게 돈다. 직관은 굽은 길을 가장 짧게 도는 방법이다: 허용되는 만큼 최대로 꺾고, 곧게 달리고, 다시 최대로 꺾는다 — 더 완만한 호는 길이만 늘린다 — 그리고 Dubins는 이런 조각 세 개면 언제나 충분함을 증명했다.
- **Reeds–Shepp (1990):** 같은 차에 후진을 허용한다. 최단 경로는 쉰 개가 안 되는 고정된 단어 목록 중 하나이고, 각 단어는 최대 다섯 구간, 기어 변환(cusp)은 최대 두 번이다.

둘 다 닫힌 형태라서 계획기는 이것을 **조향 함수(steering function)**, 즉 두 상태 사이의 정확한 연결로 쓴다. 또한 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘]] §8의 격자 휴리스틱에서 장애물을 무시하되 회전 반경은 지키는 쪽 절반이 된다. 한계도 둘 따라온다. 장애물을 무시한다. 그리고 구간 이음매마다 곡률이 점프하므로 실제 핸들은 그 모서리를 정확히 따라갈 수 없다.

**모션 프리미티브 위의 탐색.** A* 자체는 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘]] §6에 있다. 여기서 바뀌는 것은 간선이 무엇이냐다.

- **상태 격자(state lattice)** (Pivtoraiko, Knepper & Kelly 2009). $(x,y,\theta)$를, 때로는 곡률이나 속도까지 규칙적인 격자로 이산화한다. 오프라인에서 경계값 문제 — 주어진 한 상태에서 다른 한 상태로 모델을 정확히 옮기는 입력을 찾는 문제 — 를 풀어, 격자 상태에서 정확히 시작해 격자 상태에서 정확히 끝나는 실행 가능한 프리미티브의 작은 집합을 만든다. 이 집합은 평행이동에 불변이라 어디서나 같은 프리미티브를 재사용한다.
- **Hybrid A\*** (Dolgov, Thrun, Montemerlo & Diebel 2010). 몇 개의 조향값으로 차 모델을 적분해 노드를 확장한다. 이산 $(x,y,\theta)$ 칸마다 *연속* pose를 하나만 두고, 같은 칸에 나중에 도착한 것은 가지친다. 목표에 가까워지면 목표까지 해석적 Reeds–Shepp 연결을 시도하고, 결과를 평활화한다.

둘의 보장은 다르다. 격자 계획기의 완전성이나 최적성 주장은 연속 문제가 아니라 그 프리미티브 집합에 대한 것이다. Hybrid A\*의 경로는 운전 가능하지만, 칸 단위 가지치기 때문에 격자 위에서조차 완전성과 최적성을 포기한다.

[[04-robotics/ros2/navigation-nav2|Nav2]]는 둘 다 "실현 가능(feasible)" 계획기로 제공한다.

**동역학을 넣은 표본 기반 계획.** *Kinodynamic RRT*(LaValle & Kuffner 2001)는 상태를 표본으로 뽑고, 정한 거리 척도로 가장 가까운 트리 노드를 찾은 뒤, 어떤 입력과 지속 시간으로 $\dot x = f(x,u)$를 적분해 뻗는다. 이 전방 전파에는 경계값 문제 풀이기가 필요 없지만, 새 노드는 뽑은 상태에 정확히 닿지 않고 거리 척도의 선택이 결과를 좌우한다. Karaman & Frazzoli(2011)는 단순 RRT가 확률 1로 준최적 경로에 수렴함을 보였고, RRT\*와 PRM\*는 각 표본을 $(\log n / n)^{1/d}$처럼 줄어드는 반경 안의 이웃과 연결해 점근적 최적성을 되찾는다. 이 속도면 공 하나에 표본이 $\log n$에 비례하는 개수만큼 들어간다. 공의 부피가 $r^d \propto \log n/n$이고 표본이 $n$개이기 때문이다. 재연결이 싸게 유지될 만큼 적으면서, 표본이 늘어도 그래프가 연결된 채로 남을 만큼은 많다. FMT\*(Janson 외 2015)는 표본 묶음 위에서 충돌 검사를 미루는 게으른 동적 계획법으로 같은 보장을 얻는다. 동역학 시스템용 점근 최적 판본에는 정확한 조향 함수와 그 비용이 필요하다 — 자동차라면 Dubins나 Reeds–Shepp, 아니면 미리 계산한 격자, 아니면 아래의 평탄성.

**미분 평탄성(differential flatness).** 어떤 시스템은 몇 개의 출력 곡선을 자유롭게 계획하면 모든 상태와 입력을 거기서 읽어낼 수 있다. Fliess, Lévine, Martin & Rouchon(1995)은 시스템 $\dot x = f(x,u)$가 (입력 개수만큼의) 출력 $z$를 가져

$$x=\beta(z,\dot z,\dots,z^{(q)}),\qquad u=\gamma(z,\dot z,\dots,z^{(q)})$$

를 유한한 $q$에 대해 만족하면 *평탄하다*고 부른다. 그래서 매끄러운 곡선 $z(t)$ 하나가 동역학을 정확히 만족하는 상태·입력 궤적을 준다. 유니사이클 $\dot x = v\cos\theta,\ \dot y = v\sin\theta,\ \dot\theta = \omega$에서 $z=(x,y)$로 두면:

$$\theta=\operatorname{atan2}(\dot y,\dot x),\qquad v=\sqrt{\dot x^2+\dot y^2},\qquad \omega=\frac{\dot x\ddot y-\dot y\ddot x}{\dot x^2+\dot y^2}$$

이것이 성립하는 이유는 속도 $(\dot x,\dot y)$가 길이 $v$로 heading 방향을 가리키기 때문이다. 그래서 heading과 속력은 그 벡터의 각도와 크기이고, $\omega$는 그 각도의 변화율이다. 기구학적 자동차는 조향각 $\phi=\arctan(L\kappa)$를 더한다. 여기서 $L$은 축간 거리, $\kappa=\omega/v$는 경로 곡률이다. 이는 자전거 모델에서 나온다: 앞바퀴를 $\phi$만큼 조향하면 뒤축은 반경 $R$인 원을 돌고 $\tan\phi = L/R$이며, $\kappa = 1/R$이다. 따라서 회전 반경 한계는 $z$의 시간 배분이 아니라 기하에 대한 한계다.

쿼드로터에 대해 Mellinger & Kumar(2011)는 위치와 yaw를 평탄 출력으로 쓴다. 로터는 몸체 $z$축 방향으로만 밀 수 있으므로, 곡선이 요구하는 가속도(에 중력을 더한 것)가 추력의 크기와 그 축이 가리켜야 할 방향을 함께 정하고, 거기에 yaw를 더하면 자세가 된다. 한 번 더 미분하면 자세가 얼마나 빨리 돌아야 하는지가 나오므로 몸체 각속도는 저크에서 나온다. 또 한 번 미분하면 각가속도, 곧 토크가 스냅에서 나온다. 그래서 이들은 스냅을 최소화한다.

**평탄성이 계획을 곡선 맞추기로 바꾸는 이유.** $z(t)$를 다항식으로 쓴다. 그러면 $z$와 그 도함수에 대한 경계 조건이 계수에 대해 *선형*이 되고, 선형 풀이 한 번으로 동역학적으로 실행 가능한 궤적이 나온다. 남는 것은 부등식 제약 — 속도, 곡률, 장애물 — 이다. 이것들은 나중에 검사하거나, 시간 스케일링([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]])으로 고치거나, 다항식 계수를 결정 변수로 삼아 §6의 최적화에 넘긴다. 평탄성이 §6 프로그램에서 없애는 것은 동역학 제약이지 장애물 제약이 아니다.

> [!example] 계산 예제 · Worked example
> 평탄 출력 $z(t)=(t,\,t^2)$, 즉 포물선을 잡으면 $\dot x=1,\ \dot y=2t,\ \ddot x=0,\ \ddot y=2$다. 공식은 $v=\sqrt{1+4t^2}$, $\omega=2/(1+4t^2)$, 곡률 $\kappa=\omega/v=2/(1+4t^2)^{3/2}$를 준다.
>
> | $t$ | $\theta$ | $v$ | $\omega$ | 유한차분 $\dot\theta$ | $\kappa$ |
> |---|---|---|---|---|---|
> | 0 | 0° | 1.000 | 2.000 | 2.000 | 2.000 |
> | 0.5 | 45.00° | 1.414 | 1.000 | 1.000 | 0.707 |
> | 1 | 63.43° | 2.236 | 0.400 | 0.400 | 0.179 |
>
> 이 $v(t)$와 $\omega(t)$로 $(0,0,0)$에서 유니사이클을 적분하면(오일러, $\Delta t=10^{-4}$) $(1.000, 1.000, 1.107\text{ rad})$에서 끝나고, $z(1)=(1,1)$과 $\theta(1)=\arctan 2$에서 $10^{-4}$ 이내다. 입력이 정말로 곡선을 재현한다.
>
> **이제 최소 회전 반경 1 m인 차를 더한다**($\kappa\le 1$). 꼭짓점에서 $\kappa=2$, 반경 0.5 m이고, $(1+4t^2)^{3/2}=2$가 되는 $t\approx 0.383$까지 한계를 어긴다. 천천히 달려도 소용없다. 같은 포물선을 절반 속도로 지나는 $z(t)=(t/2,\,t^2/4)$는 꼭짓점에서 $v=0.5$, $\omega=1$이고 $\kappa$는 여전히 2다. 고치려면 기하를 바꿔야 한다.

```python
import numpy as np
xd, yd = lambda t: 1.0 + 0*t, lambda t: 2*t          # z(t) = (t, t^2)
xdd, ydd = lambda t: 0*t, lambda t: 2.0 + 0*t
theta = lambda t: np.arctan2(yd(t), xd(t))
v = lambda t: np.hypot(xd(t), yd(t))
omega = lambda t: (xd(t)*ydd(t) - yd(t)*xdd(t)) / (xd(t)*xd(t) + yd(t)*yd(t))
for t in [0.0, 0.5, 1.0]:
    h = 1e-5                                          # finite-difference check
    fd = (theta(t + h) - theta(t - h)) / (2*h)
    print(f"t={t}: theta={np.degrees(theta(t)):.2f} deg  v={v(t):.3f}  "
          f"omega={omega(t):.3f}  fd={fd:.3f}  kappa={omega(t)/v(t):.3f}")
dt, s = 1e-4, np.array([0.0, 0.0, 0.0])              # unicycle state (x, y, theta)
for t in np.arange(0, 1, dt):
    s = s + dt*np.array([v(t)*np.cos(s[2]), v(t)*np.sin(s[2]), omega(t)])
print("end state", s.round(3), "target (1, 1, %.3f)" % theta(1.0))
```

> [!warning] 함정과 논문에서 확인할 것
> - **속력 0은 특이점이다.** $\dot z\to 0$이면 $\theta=\operatorname{atan2}(0,0)$이 정의되지 않고 $\omega$의 분모가 사라진다. $z(t)=(t^3,t^2)$를 보면 heading이 $t=-0.01$에서 $-89.14°$, $t=+0.01$에서 $+89.14°$다. 거의 $180°$인 이 점프는 cusp, 즉 전진 속력 매개변수화로는 표현할 수 없는 기어 변환이다. 그래서 계획기는 내부 점의 속력을 0이 아니게 두고, 의도한 정지·후진 지점에서 궤적을 나누며, 경계 heading은 $v_0\neq 0$인 $\dot z(0)=v_0(\cos\theta_0,\sin\theta_0)$로 부과한다.
> - **"최적"은 무엇에 대해서인가?** 격자 계획기는 자기 프리미티브 집합 위에서 최적이고, Hybrid A\*는 아예 최적이 아니며, Dubins·Reeds–Shepp 비용은 장애물을 무시한다. Dubins 거리는 대칭조차 아니어서 최근접 이웃 척도로 쓸 때 조심해야 한다.
> - **평활화 뒤에 무엇이 살아남았는지 확인하라.** 후처리 뒤에도 곡률 연속성, 회전 반경 한계, 속도·가속도 한계가 지켜지는지 본다.
> - **평탄성은 가정이 아니라 확인할 성질이다.** 논문은 평탄 출력을 명시해야 한다.
>
> **건설 기계에서는.** 굴절식 휠 로더는 프레임을 꺾어 조향하고, 궤도식 굴착기는 미끄럼이 큰 스키드 조향으로 돈다. 둘 다 비용 지도 경로가 무시하는 회전 반경이나 미끄럼 제약을 가진다. 크레인이나 붐은 그 위에 짐 흔들림 동역학을 더한다. 그래서 [[05-construction-robotics/earthmoving-heavy-machinery|중장비 자율화]]에는 2-D 격자 계획기만이 아니라 이 절의 실행 가능성 검사가 필요하다.

### 6. 궤적 최적화와 MPC

흔한 정식화는 [[02-foundations/optimization|4. 최적화]]의 궤적 최적화 프로그램이다 — 매 스텝 내는 실행 비용에 마지막의 종단 비용을 더한 것으로 읽되, 물리와 장애물이 제약이다:

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. 동역학, 한계, 충돌 제약}$$

- **주어진 것:** 초기 상태, 모델, 목표, 제약, 비용.
- **최적화하는 것:** 상태·입력 시퀀스.
- **실행 시점:** 오프라인 계획 또는 MPC로 반복 온라인.
- **주의:** 비선형 동역학과 장애물 제약은 대개 국소적·초기화 민감 문제를 만든다.

Direct shooting은 제어를 최적화하고 상태를 시뮬레이션한다. Direct transcription은
상태·제어를 모두 변수로 둔다. Collocation은 선택한 점들에서 동역학을 강제한다. 어느
것도 비볼록 로봇 문제의 전역 최적성을 자동으로 증명하지 않는다.

**아래첨자를 제안한 미래로 풀어 읽는다.** x₀는 현재 추정 상태로 고정된다. 뒤의 x들은 예측 상태이고 u들은 모델상 그 상태를 만드는 입력이다. 단계 비용은 미래의 각 구간을 평가하고 종단 비용은 지평 끝의 위치를 평가한다. 동역학 제약이 상상한 시퀀스를 묶어, 실제 움직임으로 이어지지 않는 매력적인 상태만 고르지 못하게 한다.

MPC는 이 정식화를 피드백으로 쓴다. 첫 입력을 실행하고 새 상태를 관측한 뒤 다시 푼다. 실행하지 않은 미래도 첫 결정을 바꿨으므로 의미가 있다. 재계획은 예측이 모두 맞았다고 가정하는 대신 차이를 고친다. 오프라인 궤적 최적화는 비슷한 수학 문제를 풀어도 이 반복 피드백은 하지 않을 수 있다.

**이해 확인.** 해법의 실행 가능 출력은 초기 상태, 모델, 이산화, 제약에 조건부다. 상태 추정이 낡거나 검사 지점 사이에서 충돌하면 최적화를 정확히 푸는 것만으로 부족하다. 궤적 표현과 피드백 실행의 구분은 [궤적 최적화 강의](https://underactuated.mit.edu/trajopt.html)에서도 다룬다.

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
> LaValle의 [*Planning Algorithms*](http://lavalle.pl/planning/)가 무료이고 샘플링 기반 쪽의 참고서다. 다만 2006년 책이라 확률적 완전성까지만 다루고 RRT\*와 점근적 최적성은 없다 — 그쪽은 Karaman과 Frazzoli(2011)다. 궤적 최적화 쪽은 Tedrake의 [*Underactuated Robotics*](https://underactuated.csail.mit.edu/)가 실행 가능한 코드와 함께 다룬다.

### 스스로 점검

1. 충돌 없는 path가 동역학적으로 실행 불가능할 수 있는 이유는?
2. 컨피규레이션 공간 대신 작업 영역에서만 계획하면 무엇을 잃는가?
3. 실행 가능한 궤적이 존재하는데도 궤적 최적화가 실패할 수 있는 이유는?
4. "실시간 폐루프 플래너" 주장을 지지하는 증거는?
5. Hybrid A\* 논문과 상태 격자 논문이 둘 다 경로가 "최적"이라고 한다. 각각 무엇에 대해 최적인가?
6. 포물선 $z(t)=(t,t^2)$는 꼭짓점 근처에서 최소 회전 반경 1 m를 어긴다. 같은 곡선을 따라 천천히 달려도 고쳐지지 않는 이유는?

> [!tip]- 정답 · Answers
> 1. 불가능한 속도·가속도·토크·접촉·타이밍을 요구할 수 있다.
> 2. 로봇 형상, 관절 한계, 같은 과제 pose에 대한 복수의 컨피규레이션.
> 3. 문제가 비볼록이고 초기화에 민감할 수 있다.
> 4. 명시된 하드웨어에서의 끝-끝 지연 분포, 교란·동적 장애물 아래의 실행, 제약 위반과 실패 — 플래너 계산 시간만으로는 안 된다.
> 5. 격자 계획기는 미리 계산한 프리미티브 집합과 해상도 위에서만 최적이라, 그 집합에 없는 heading이나 곡률이 필요한 경로를 놓칠 수 있다. Hybrid A\*는 칸마다 연속 pose 하나만 남기고 나머지를 가지치기 때문에 자기 격자 위에서조차 최적이 아니다.
> 6. 회전 반경 한계는 곡률 $\kappa=\omega/v$를 제한하는데, 곡률은 기하에만 달려 있다. 절반 속도에서 꼭짓점은 $v=0.5$, $\omega=1$이라 $\kappa$는 여전히 2다. 다른 곡선만이 답이다.

### 출처

- [Modern Robotics, Chapter 10](http://modernrobotics.org)
- [MIT Underactuated Robotics](https://underactuated.csail.mit.edu/)
- [OMPL: planning concepts](https://ompl.kavrakilab.org/)
- L. E. Dubins, "On curves of minimal length with a constraint on average curvature, and with prescribed initial and terminal positions and tangents," *American Journal of Mathematics* 79(3), 497–516, 1957. doi:10.2307/2372560
- J. A. Reeds, L. A. Shepp, "Optimal paths for a car that goes both forwards and backwards," *Pacific Journal of Mathematics* 145(2), 367–393, 1990. doi:10.2140/pjm.1990.145.367
- M. Pivtoraiko, R. A. Knepper, A. Kelly, "Differentially constrained mobile robot motion planning in state lattices," *Journal of Field Robotics* 26(3), 308–333, 2009.
- D. Dolgov, S. Thrun, M. Montemerlo, J. Diebel, "Path planning for autonomous vehicles in unknown semi-structured environments," *International Journal of Robotics Research* 29(5), 485–501, 2010.
- S. M. LaValle, J. J. Kuffner, "Randomized kinodynamic planning," *International Journal of Robotics Research* 20(5), 378–400, 2001. doi:10.1177/02783640122067453
- S. Karaman, E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *International Journal of Robotics Research* 30(7), 846–894, 2011. doi:10.1177/0278364911406761
- L. Janson, E. Schmerling, A. Clark, M. Pavone, "Fast marching tree: a fast marching sampling-based method for optimal motion planning in many dimensions," *International Journal of Robotics Research* 34(7), 883–921, 2015. doi:10.1177/0278364915577958
- M. Fliess, J. Lévine, P. Martin, P. Rouchon, "Flatness and defect of non-linear systems: introductory theory and examples," *International Journal of Control* 61(6), 1327–1361, 1995. doi:10.1080/00207179508921959
- D. Mellinger, V. Kumar, "Minimum snap trajectory generation and control for quadrotors," *IEEE International Conference on Robotics and Automation (ICRA)*, 2520–2525, 2011. doi:10.1109/ICRA.2011.5980409
- S. M. LaValle, *Planning Algorithms*, Cambridge University Press, 2006 — §14.1(kinodynamic 용어)와 §15.3(Dubins·Reeds–Shepp 곡선).
