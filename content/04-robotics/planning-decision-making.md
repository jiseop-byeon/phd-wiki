---
title: 4. Planning & Decision-Making
tags: [robotics, planning, decision-making]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

*Group C, and the only page in it. Stands on the [[04-robotics/modern-robotics/index|Modern Robotics chapters]], [[04-robotics/mpc|7. MPC]] and the optimization and RL pages.
Choosing an executable future; group I specialises this for unstructured environments.*

Planning asks how a robot should choose a feasible sequence of future states and actions to reach a goal. The difficulty is not merely finding a short path: robot geometry, dynamics, contact, uncertainty, computation time, and changing observations constrain what can actually be executed.

*Scope: this page teaches the objects and the guarantees — the five words of §1, the spaces and the map and cost representations of §2, the four strengths of completeness in §5, the constraints that make a path undrivable in §5.5, and the shape of the trajectory-optimization program in §6 — plus enough of each method family to place a paper in it. It does not teach any single algorithm to implementation depth. A\*'s proofs and code are in [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms §6]], the sampling planners are surveyed here and implemented nowhere in this wiki, receding-horizon control is [[04-robotics/mpc|7. MPC]], policy learning is [[02-foundations/rl-basics|RL Basics]], and one navigation stack's concrete parameters are [[04-robotics/ros2/navigation-nav2|25.9 Nav2]].*

> [!info] Depth target
> Distinguish search, motion planning, trajectory optimization, task planning, policy learning, and control; read feasibility and optimality claims; and identify whether a generated trajectory is collision-free, dynamically feasible, and evaluated in closed loop.

> [!note] Prerequisites
> [[02-foundations/optimization|Optimization]] · [[02-foundations/rl-basics|RL Basics]] · [[04-robotics/modern-robotics/ch02-configuration-space|Configuration Space]] · [[04-robotics/modern-robotics/ch10-motion-planning|Motion Planning]] — §6 previews [[04-robotics/mpc|MPC]] (track page 7); read it lightly here and return after that page.

> [!note] First pass · 처음이라면
> Read §1 — five words the literature uses interchangeably and should not — then §2, then §4's worked example. §5 through §8 are a survey; read the family a paper belongs to rather than all of them.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 320" style="max-width:100%;height:auto" role="img" aria-label="Left: P2's workspace with the reach disc of radius 2 m, the panel line x = 1 m, the task point (1, 1), the arm straight with its tip at (2, 0) and at the frozen pose with its elbow at (1, 0) and tip at (1, 1), and the quarter circle the tip traces. Right: the configuration-space torus with q_start = (0, 0), q_goal = (0, 90 degrees), the single edge between them, the region the tip check forbids shaded, and the goal on its boundary. An arrow f, the forward kinematics, joins them.">
  <defs><marker id="aPDM" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <circle cx="128.0" cy="162.0" r="100" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="128.0" y1="162.0" x2="57.3" y2="91.3" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55" stroke-dasharray="2 3"/>
  <line x1="178.0" y1="75.4" x2="178.0" y2="248.6" stroke="currentColor" stroke-width="1.3"/>
  <path d="M178.0 79.4 l-7 7 M178.0 88.4 l-7 7 M178.0 97.4 l-7 7 M178.0 106.4 l-7 7 M178.0 115.4 l-7 7 M178.0 124.4 l-7 7 M178.0 133.4 l-7 7 M178.0 142.4 l-7 7 M178.0 151.4 l-7 7 M178.0 160.4 l-7 7 M178.0 169.4 l-7 7 M178.0 178.4 l-7 7 M178.0 187.4 l-7 7 M178.0 196.4 l-7 7 M178.0 205.4 l-7 7 M178.0 214.4 l-7 7 M178.0 223.4 l-7 7 M178.0 232.4 l-7 7 M178.0 241.4 l-7 7" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" fill="none"/>
  <path d="M228.0 162.0 A50 50 0 0 0 178.0 112.0" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>
  <g stroke="currentColor" stroke-linecap="round" fill="none">
    <polyline points="128.0,162.0 178.0,162.0 228.0,162.0" stroke-width="4" stroke-opacity="0.35"/>
    <polyline points="128.0,162.0 178.0,162.0 178.0,112.0" stroke-width="3"/>
  </g>
  <circle cx="128.0" cy="162.0" r="4.5" fill="currentColor"/>
  <circle cx="178.0" cy="162.0" r="3.5" fill="currentColor"/>
  <circle cx="228.0" cy="162.0" r="3.5" fill="currentColor" fill-opacity="0.45"/>
  <circle cx="178.0" cy="112.0" r="4.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <path d="M352 72 h180 v180 h-180 Z M397 117 L398 110.4 L399 108.2 L400 106.8 L401 105.7 L402 104.9 L403 104.2 L404 103.6 L405 103.2 L406 102.9 L407 102.6 L408 102.4 L409 102.2 L410 102.1 L411 102 L412 102 L413 102 L414 102.1 L415 102.2 L416 102.3 L417 102.5 L418 102.7 L419 102.9 L420 103.1 L421 103.4 L422 103.8 L423 104.1 L424 104.5 L425 104.9 L426 105.4 L427 105.8 L428 106.4 L429 106.9 L430 107.5 L431 108.1 L432 108.7 L433 109.4 L434 110.1 L435 110.9 L436 111.6 L437 112.4 L438 113.3 L439 114.2 L440 115.1 L441 116 L442 117 L443 118 L444 119.1 L445 120.2 L446 121.3 L447 122.4 L448 123.6 L449 124.9 L450 126.1 L451 127.4 L452 128.7 L453 130.1 L454 131.5 L455 132.9 L456 134.4 L457 135.8 L458 137.4 L459 138.9 L460 140.5 L461 142.1 L462 143.8 L463 145.4 L464 147.1 L465 148.9 L466 150.7 L467 152.5 L468 154.3 L469 156.2 L470 158.1 L471 160 L472 162 L473 164 L474 166.1 L475 168.2 L476 170.4 L477 172.6 L478 174.9 L479 177.2 L480 179.6 L481 182.2 L482 184.9 L483 187.7 L484 190.8 L485 194.2 L486 198.4 L487 207 L487 207 L486 213.6 L485 215.8 L484 217.2 L483 218.3 L482 219.1 L481 219.8 L480 220.4 L479 220.8 L478 221.1 L477 221.4 L476 221.6 L475 221.8 L474 221.9 L473 222 L472 222 L471 222 L470 221.9 L469 221.8 L468 221.7 L467 221.5 L466 221.3 L465 221.1 L464 220.9 L463 220.6 L462 220.2 L461 219.9 L460 219.5 L459 219.1 L458 218.6 L457 218.2 L456 217.6 L455 217.1 L454 216.5 L453 215.9 L452 215.3 L451 214.6 L450 213.9 L449 213.1 L448 212.4 L447 211.6 L446 210.7 L445 209.8 L444 208.9 L443 208 L442 207 L441 206 L440 204.9 L439 203.8 L438 202.7 L437 201.6 L436 200.4 L435 199.1 L434 197.9 L433 196.6 L432 195.3 L431 193.9 L430 192.5 L429 191.1 L428 189.6 L427 188.2 L426 186.6 L425 185.1 L424 183.5 L423 181.9 L422 180.2 L421 178.6 L420 176.9 L419 175.1 L418 173.3 L417 171.5 L416 169.7 L415 167.8 L414 165.9 L413 164 L412 162 L411 160 L410 157.9 L409 155.8 L408 153.6 L407 151.4 L406 149.1 L405 146.8 L404 144.4 L403 141.8 L402 139.1 L401 136.3 L400 133.2 L399 129.8 L398 125.6 L397 117 Z" fill="currentColor" fill-opacity="0.16" fill-rule="evenodd"/>
  <path d="M397 117 L398 110.4 L399 108.2 L400 106.8 L401 105.7 L402 104.9 L403 104.2 L404 103.6 L405 103.2 L406 102.9 L407 102.6 L408 102.4 L409 102.2 L410 102.1 L411 102 L412 102 L413 102 L414 102.1 L415 102.2 L416 102.3 L417 102.5 L418 102.7 L419 102.9 L420 103.1 L421 103.4 L422 103.8 L423 104.1 L424 104.5 L425 104.9 L426 105.4 L427 105.8 L428 106.4 L429 106.9 L430 107.5 L431 108.1 L432 108.7 L433 109.4 L434 110.1 L435 110.9 L436 111.6 L437 112.4 L438 113.3 L439 114.2 L440 115.1 L441 116 L442 117 L443 118 L444 119.1 L445 120.2 L446 121.3 L447 122.4 L448 123.6 L449 124.9 L450 126.1 L451 127.4 L452 128.7 L453 130.1 L454 131.5 L455 132.9 L456 134.4 L457 135.8 L458 137.4 L459 138.9 L460 140.5 L461 142.1 L462 143.8 L463 145.4 L464 147.1 L465 148.9 L466 150.7 L467 152.5 L468 154.3 L469 156.2 L470 158.1 L471 160 L472 162 L473 164 L474 166.1 L475 168.2 L476 170.4 L477 172.6 L478 174.9 L479 177.2 L480 179.6 L481 182.2 L482 184.9 L483 187.7 L484 190.8 L485 194.2 L486 198.4 L487 207 L487 207 L486 213.6 L485 215.8 L484 217.2 L483 218.3 L482 219.1 L481 219.8 L480 220.4 L479 220.8 L478 221.1 L477 221.4 L476 221.6 L475 221.8 L474 221.9 L473 222 L472 222 L471 222 L470 221.9 L469 221.8 L468 221.7 L467 221.5 L466 221.3 L465 221.1 L464 220.9 L463 220.6 L462 220.2 L461 219.9 L460 219.5 L459 219.1 L458 218.6 L457 218.2 L456 217.6 L455 217.1 L454 216.5 L453 215.9 L452 215.3 L451 214.6 L450 213.9 L449 213.1 L448 212.4 L447 211.6 L446 210.7 L445 209.8 L444 208.9 L443 208 L442 207 L441 206 L440 204.9 L439 203.8 L438 202.7 L437 201.6 L436 200.4 L435 199.1 L434 197.9 L433 196.6 L432 195.3 L431 193.9 L430 192.5 L429 191.1 L428 189.6 L427 188.2 L426 186.6 L425 185.1 L424 183.5 L423 181.9 L422 180.2 L421 178.6 L420 176.9 L419 175.1 L418 173.3 L417 171.5 L416 169.7 L415 167.8 L414 165.9 L413 164 L412 162 L411 160 L410 157.9 L409 155.8 L408 153.6 L407 151.4 L406 149.1 L405 146.8 L404 144.4 L403 141.8 L402 139.1 L401 136.3 L400 133.2 L399 129.8 L398 125.6 L397 117 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <rect x="352" y="72" width="180" height="180" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <path d="M348 210 L352 204 L356 210 M528 210 L532 204 L536 210 M496 68 L502 72 L496 76 M502 68 L508 72 L502 76 M496 248 L502 252 L496 256 M502 248 L508 252 L502 256" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.5">
    <line x1="397" y1="252" x2="397" y2="256"/>
    <line x1="348" y1="207" x2="352" y2="207"/>
    <line x1="442" y1="252" x2="442" y2="256"/>
    <line x1="348" y1="162" x2="352" y2="162"/>
    <line x1="487" y1="252" x2="487" y2="256"/>
    <line x1="348" y1="117" x2="352" y2="117"/>
  </g>
  <line x1="442" y1="162" x2="442" y2="117" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="442" cy="162" r="4" fill="currentColor"/>
  <circle cx="442" cy="117" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="442" y1="111" x2="442" y2="64" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <path d="M437 139.5 Q 327.7 82.6 218.4 126.6" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#aPDM)"/>
  <circle cx="442" cy="139.5" r="2.6" fill="currentColor"/>
  <circle cx="213.4" cy="126.6" r="2.6" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
    <text x="10" y="20" font-size="12">workspace: positions (m)</text>
    <text x="322" y="20" font-size="12">configuration space C = T²: angles</text>
    <text x="119.0" y="166.0" text-anchor="end">base (0, 0)</text>
    <text x="169.0" y="179.0" text-anchor="end" opacity="0.9">elbow (1, 0)</text>
    <text x="234.0" y="156.0" opacity="0.75">tip (2, 0)</text>
    <text x="170.0" y="104.0" text-anchor="end">p* = (1, 1)</text>
    <text x="182.0" y="71.4">panel x = 1 m</text>
    <text x="97" y="113" text-anchor="middle" opacity="0.85">r = 2 m</text>
    <text x="209" y="110.5" opacity="0.85">tip path</text>
    <text x="292" y="100.6" text-anchor="middle">f: forward kinematics</text>
    <text x="417" y="149.5" text-anchor="middle" font-size="12">C<tspan font-size="9.5" dy="3">free</tspan><tspan dy="-3" dx="1.5"></tspan></text>
    <text x="358" y="244" opacity="0.85">tip x &lt; 1: forbidden</text>
    <text x="449" y="175">q<tspan font-size="9.5" dy="3">start</tspan><tspan dy="-3" dx="1.5"> (0°, 0°)</tspan></text>
    <text x="442" y="60" text-anchor="middle">q<tspan font-size="9.5" dy="3">goal</tspan><tspan dy="-3" dx="1.5"> (0°, 90°): on the boundary, contact</tspan></text>
    <text x="352" y="267" text-anchor="middle" font-size="11">−180°</text>
    <text x="346" y="256" text-anchor="end" font-size="11">−180°</text>
    <text x="442" y="267" text-anchor="middle" font-size="11">0°</text>
    <text x="346" y="166" text-anchor="end" font-size="11">0°</text>
    <text x="532" y="267" text-anchor="middle" font-size="11">180°</text>
    <text x="346" y="76" text-anchor="end" font-size="11">180°</text>
    <text x="482" y="267" font-size="12">θ<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="326" y="150" font-size="12">θ<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="532.0" y="284" text-anchor="end" font-size="11" opacity="0.85">opposite edges identified: 179° and −179° are neighbours</text>
    <text x="10" y="307" opacity="0.9">Planner guarantees are claims about the right panel; what the robot does is on the left.</text>
  </g>
</svg>

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (unit links, base at the world origin) and the panel, the half-plane $x<1$ m, in the same pairing as the figure in §2. Left, the workspace: the $2$ m reach disc, the arm straight with its tip at $(2,0)$ and at the frozen pose with its elbow at $(1,0)$ and its tip on the task point $p^\star=(1,1)$, and the quarter circle the tip traces between the two. Right, the configuration space $\mathcal{C}=T^2$ with opposite edges identified: the single edge from $q_\mathrm{start}=(0°,0°)$ to $q_\mathrm{goal}=(0°,90°)$ and the shaded region the tip check forbids, $\cos\theta_1+\cos(\theta_1+\theta_2)<1$, with the goal on its boundary (contact, not free space), and the arrow $f$, the forward kinematics, is all that relates the two panels.

### 1. Plan, path, trajectory, policy, controller

| Term | Meaning |
|---|---|
| Plan | Proposed future sequence of decisions or actions |
| Path | Geometric curve without timing |
| Trajectory | Time-indexed state, velocity, and often input |
| Policy | Rule mapping available information to an action |
| Controller | Feedback system that tracks a reference or regulates behavior |

A planner may produce a path that a trajectory generator times ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]] — time scaling, via points, time-optimal scaling) and a controller tracks. When the plan lives in task space but the robot is commanded in joint space, [[04-robotics/modern-robotics/ch06-inverse-kinematics|inverse kinematics (MR ch.6)]] sits between them, and its multimodality is a planning problem in miniature. In learned systems, a policy can collapse these boundaries, but the physical requirements do not disappear.

**The five, as mathematical objects.** Let $\mathcal{C}$ be the configuration space, $\mathcal{X}$ the state space and $\mathcal{U}$ the input space (all three are defined in §2).

- A **path** is a continuous map from a normalised parameter $s$ to configurations, with both ends fixed. The parameter is not time, so a path says only *where*.
$$\sigma:[0,1]\to\mathcal{C},\qquad \sigma(0)=q_{\text{start}},\quad \sigma(1)=q_{\text{goal}}$$
- A **trajectory** adds timing: the state, and usually the input, as functions of time over a duration $T$. Every trajectory traces a path, but one path has infinitely many trajectories, since any increasing time scaling $s(t)$ with $s(0)=0$ and $s(T)=1$ gives another ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]]).
$$x:[0,T]\to\mathcal{X},\qquad u:[0,T]\to\mathcal{U}$$
- A **plan** is a finite sequence of decisions $(a_0,\dots,a_{K-1})$, whether symbolic actions, waypoints or inputs, computed *before* execution for one start state.
- A **policy** is a rule evaluated *during* execution. It maps whatever information $I_t$ is available (the state, an observation history, a belief) to an action, $a_t=\pi(I_t)$, or to a distribution $\pi(a_t\mid I_t)$ ([[02-foundations/rl-basics|RL Basics §1]]).
- A **controller** is a feedback law, usually fast, that computes the actuator command from the measured state and a reference, $u_t=\kappa(x_t,\,x^{\text{ref}}_t)$.

The plan/policy split matters most: a plan is one answer for one start, and a policy is an answer for every state it may meet. Example: the straight segment from $(0,0)$ to $(1,0)$ m is one path. Driving it at a constant 0.5 m/s is a trajectory with $T=2$ s, and driving it at 1 m/s is a different trajectory, with $T=1$ s, on the same path. **Non-example:** a list of waypoints without times is a path or a plan, not a trajectory, so it cannot be checked against velocity or acceleration limits until something times it.

### 2. Spaces and constraints

- **Workspace:** physical positions occupied by the robot and obstacles.
- **Configuration space:** robot configurations; obstacles become forbidden regions.
- **State space:** configuration plus variables such as velocity.
- **Action/input space:** commands available to the system.
- **Task space:** variables directly tied to the task, such as end-effector pose.

Collision-free in workspace does not imply joint, torque, velocity, stability, or contact feasibility.

**Configuration space, defined.** A **configuration** $q$ is a specification of the position of every point of the robot. Two conditions make one: it is **complete**, so no body point is left undetermined, and it is **minimal**, so no shorter list of numbers does the same job. The **configuration space** $\mathcal{C}$ is the set of all configurations, and minimality is what makes its dimension the number of degrees of freedom:

$$\mathcal{C}=\{\,q:q\ \text{locates every point of the robot}\,\},\qquad \dim\mathcal{C}=\text{dof}$$

The set matters more than the count, because $\mathcal{C}$ is usually not a box. A planar 2R arm's is the torus $T^2$, not the rectangle $[0,2\pi)^2$, since each joint angle wraps — so a planner that treats $359°$ and $1°$ as far apart is using the wrong space. **Non-example:** the end-effector pose is *not* a configuration of a redundant arm, because many joint vectors give the same pose and the body points are therefore not determined. That is task space, the last item in the list above.

$\mathcal{C}$ splits into the **C-obstacle** $\mathcal{C}_{\text{obs}}$ and the **free space** $\mathcal{C}_{\text{free}}=\mathcal{C}\setminus\mathcal{C}_{\text{obs}}$. Both are defined, derived on plant **P2**, and given their example and non-example in [[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2 §2]]; this page uses them rather than restating them. Two consequences of that definition are what the rest of this page rests on: a C-obstacle is a set of *configurations* and never a region of the workspace, and the construction shrinks a robot of some shape to a *point* moving in $\mathcal{C}_{\text{free}}$, which is the form every planner below is written for.

The **path-planning problem** is then: given $q_{\text{start}},q_{\text{goal}}\in\mathcal{C}_{\text{free}}$, find a path $\sigma$ (§1) with $\sigma(s)\in\mathcal{C}_{\text{free}}$ for every $s\in[0,1]$, or report that none exists. The **state space** $\mathcal{X}$ adds velocities, $x=(q,\dot q)$, so an $n$-dof robot has a $2n$-dimensional state. The **input space** $\mathcal{U}$ is the set of admissible commands, for example $|u_i|\le u_{\max}$ for each actuator. Workspace and task space are sets of physical positions or poses, while $\mathcal{C}$ is a set of robot configurations, which is why the figure below needs two panels.

> [!example] Worked example · 계산 예제
> MR ch.2 derives the C-obstacle of an *arm*, where it is a curved lens on a torus. Here is the other case, the one the grid inflation below depends on. A disc robot of radius 0.5 m that translates without rotating has configuration $q=(x,y)$, its centre, so $\mathcal{C}=\mathbb{R}^2$. With a square obstacle $[1,2]\times[1,2]$ m, $q\in\mathcal{C}_{\text{obs}}$ exactly when the centre is closer than 0.5 m to the square. $q=(0.6,1.5)$ is 0.4 m from it, so it is in $\mathcal{C}_{\text{obs}}$ even though the workspace *point* $(0.6,1.5)$ is empty. $q=(0.4,1.5)$ is 0.6 m away and free.
>
> **Non-example:** the C-obstacle is not the square grown into the box $[0.5,2.5]^2$. Its corners are rounded, because it is the square's Minkowski sum with the disc. So $q=(0.6,0.6)$, inside that box, is 0.566 m from the corner $(1,1)$ and free, while $(0.7,0.7)$, at 0.424 m, is not. This is the inflation of the list below, and it is exact only because the robot is a disc.

**How that space is actually stored.** Two pages of this wiki send you here for occupancy and
cost representations, so they belong in this section rather than in a system paper's
appendix.

- **Occupancy grid** — the map is a grid of cells, each holding the probability that the cell
  is occupied. Updates are done in **log-odds**, $\ell=\log\frac{p}{1-p}$, which maps $p=0.5$ to
  $0$ and $p\to 0$ or $1$ to $\mp\infty$. Bayes' rule multiplies a cell's odds $p/(1-p)$ by each
  new reading's likelihood ratio, so after the log, accumulating evidence is an addition
  rather than a multiplication (OctoMap's $+0.85$ is $\log(0.7/0.3)$, a "hit" worth $p=0.7$). It also avoids the numerical trouble of probabilities pressed
  against 0 or 1. Note the direction of the remaining hazard: log-odds is *unbounded*, so a
  cell observed occupied a thousand times needs on the order of a thousand contrary observations to flip (about 2,100 with OctoMap's default +0.85/−0.4 log-odds increments) —
  which is why implementations add an explicit **clamping** range (proposed by Yguel et al. 2007 and adopted by OctoMap) so
  the map can still adapt when the world changes. A cell reads as *free*, *occupied*, or
  **unknown**, and the third is the one beginners drop: unknown is not free, and the difference is what exploration is about.
  **The update, written out.** Let $m_i=1$ mean "cell $i$ is occupied" and $p_0$ be the prior occupancy probability. Each reading $z_t$ adds its own evidence and the prior is subtracted once, so it is not counted again with every reading:
  $$\ell_t(i)=\ell_{t-1}(i)+\log\frac{p(m_i=1\mid z_t)}{1-p(m_i=1\mid z_t)}-\log\frac{p_0}{1-p_0},\qquad p=1-\frac{1}{1+e^{\ell}}$$
  The middle term is the **inverse sensor model**, the occupancy probability that this one reading alone implies, and the second formula converts log-odds back to a probability. With $p_0=0.5$ the prior term is $0$. Two OctoMap hits then give $\ell=1.70$ and $p=0.846$, and one miss ($-0.4$) after them gives $\ell=1.30$ and $p=0.786$. Clamping bounds $\ell$ to an interval $[\ell_{\min},\ell_{\max}]$ after every update.
- **Inflation** — a planner that treats the robot as a point (the figure below) has to grow
  the obstacles instead. Inflating occupied cells by the robot radius produces a C-space
  obstacle directly on the grid **for a circular robot** — for any other footprint it is an
  approximation, which is why a stack like Nav2 still runs a separate footprint collision
  check. Adding a decaying cost outside that radius produces a margin the planner prefers not
  to enter. As a function of a cell's distance $d$ to the nearest obstacle cell, with inscribed robot radius $r$ and decay rate $\alpha>0$, ROS costmaps use an exponential:
  $$c(d)=\begin{cases}c_{\text{lethal}} & d=0\\ c_{\text{insc}} & 0<d\le r\\ c_{\text{insc}}\,e^{-\alpha(d-r)} & r<d\le d_{\text{infl}}\\ 0 & d>d_{\text{infl}}\end{cases}$$
  so a cell within the inscribed radius means certain collision for a robot centred there, the cost decays with distance outside it, and cells beyond the inflation radius $d_{\text{infl}}$ cost nothing. With $\alpha=3$ /m, a cell 0.2 m outside the inscribed radius costs $e^{-0.6}=0.55$ of the inscribed value; raising $\alpha$ narrows the margin.
  **Three radii, and they are not the same number.** A footprint has an **inscribed radius** $r_{\text{insc}}$, the radius of the largest disc centred at the robot's origin that fits *inside* it, and a **circumscribed radius** $r_{\text{circ}}$, the smallest disc that *contains* it. Within $r_{\text{insc}}$ of an obstacle the robot is in collision at every heading; beyond $r_{\text{circ}}$ it is clear at every heading; in between, collision depends on heading, which is the band a footprint check exists to resolve. The **inflation radius** $d_{\text{infl}}$ is a third thing entirely: the distance at which the decaying cost is truncated to zero. It is a *preference* knob and not a safety margin — the safety is $r_{\text{insc}}$, which comes from the footprint and not from $d_{\text{infl}}$. **Non-example, and the most common misconfiguration in the ecosystem:** reading `inflation_radius` as "keep the robot this far from walls" ([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §5]]). With $r_{\text{insc}}=0.30$ m, $\alpha=3$ /m, $d_{\text{infl}}=1.00$ m and the ROS byte scale ($c_{\text{lethal}}=254$ for the obstacle cell, $c_{\text{insc}}=253$, and the skirt scaled by $252$), the cost is $252\,e^{-0.6}=138$ at $d=0.50$ m, $56$ at $0.80$ m and $30$ just inside $1.00$ m — and $0$ just outside it. That step of 30 at $d_{\text{infl}}$ is a **cost cliff**, a discontinuity the gradient-following argument above does not survive, so $d_{\text{infl}}$ wants to be large enough that the truncated value is small.
- **Costmap** — an occupancy grid whose cells carry *traversal cost* rather than a binary.
  Cost combines inflation with whatever else the robot should avoid: unknown space, rough
  terrain, one-way regions, keep-out zones. **A costmap is where a policy preference stops
  being a plan and becomes geometry** — and it is the representation
  [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy §1]] argues *is*
  the right carrier for a learned affordance, since the same scene yields different costmaps for
  different robots. What that page rejects is the plain occupancy grid, the geometric predicate.
- **Layered costmap** — the costmap a planner reads is not one grid that everything writes to.
  It is a **master grid** produced by composing an ordered list of **layers**, and a layer is a
  component with exactly two operations, run once per update cycle: it first declares the
  rectangle of the map it is about to touch, and then writes costs into the master grid inside
  that rectangle. Two conditions make this a layered costmap rather than a pile of grids. Each
  layer sees the master grid *as the layers before it left it*, and each layer writes with a
  declared combination rule — **overwrite**, **maximum**, or maximum-ignoring-unknown. Order is
  therefore part of the specification and the composition does not commute: the usual order is
  static map, then obstacles (which mark and clear from live sensor data), then inflation, and
  inflation must be last because it measures distance to whatever the earlier layers left lethal.
  *Example*: a person steps in front of the robot; the obstacle layer marks those cells and the
  inflation layer grows them; the person walks away and ray-casting clears exactly those cells,
  while the wall behind is untouched because it was never the obstacle layer's to write.
  **Non-example**: one flattened grid. There, clearing the stale person means clearing cells the
  static map also claims, so either the wall is erased or the person is permanent — which is the
  whole reason the layers exist. *Why it matters when reading*: "the costmap" in a paper is a
  composition, and which layer produced a cost decides whether anything can clear it
  ([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §4]] for one stack's layer list and defaults).
- **Frontier** — a boundary cell between *known free* and *unknown*: precisely, a cell that is itself known free and has at least one unknown neighbour (4- or 8-connected). **Frontier exploration**
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
The local layer is where the classical names live:

| Local planner | What it does each cycle |
|---|---|
| *Dynamic window* | Samples velocity pairs (forward, turning) the robot can reach within one cycle, and scores each |
| **Elastic band** | Deforms a *path* under an internal contraction force and an external obstacle repulsion, with no notion of time |
| **Timed elastic band** | The descendant that adds the time intervals its name refers to |
| **Sampling-based MPC** (the family [[01-canonical-papers/notes/9-navigation/badgr\|BADGR]] uses) | Samples many action sequences around a running estimate, rolls each forward through a model, refits the estimate by a **reward-weighted average** over the samples rather than taking the single best, and executes its first action |

**Two of those rows, written out.**

- **Dynamic window** (Fox, Burgard & Thrun 1997). Let $(v_c,\omega_c)$ be the current forward and turning velocities, $\dot v_{\max},\dot\omega_{\max}$ the acceleration limits and $\Delta t$ the cycle time. The candidates must satisfy three conditions at once. They must be velocities the robot can have at all ($V_s$). They must be reachable within one cycle, which is a small box because accelerations are bounded:
$$V_d=\{(v,\omega): |v-v_c|\le\dot v_{\max}\Delta t,\ |\omega-\omega_c|\le\dot\omega_{\max}\Delta t\}$$
  And they must be **admissible**, meaning the robot can still brake to a stop before the nearest obstacle on that arc, $v\le\sqrt{2\,\mathrm{dist}(v,\omega)\,\dot v_b}$ with braking deceleration $\dot v_b$ (and likewise for $\omega$). Each pair in $V_s\cap V_d\cap V_a$ is scored by a weighted sum of heading toward the goal, clearance and speed, and the best pair is executed for one cycle. Example: $v_c=0.5$ m/s, $\dot v_{\max}=0.5$ m/s² and $\Delta t=0.25$ s give $v\in[0.375,0.625]$ m/s. An obstacle 0.5 m along the arc with $\dot v_b=0.5$ m/s² caps $v$ at $\sqrt{0.5}=0.71$ m/s, so here the window, not the obstacle, is the binding limit.
- **Reward-weighted average.** Sample $K$ action sequences $u^{(k)}$ around the current estimate $\bar u$, roll each through the model to a return $R_k$, and refit:
$$\bar u\leftarrow\sum_{k=1}^{K}w_k\,u^{(k)},\qquad w_k=\frac{\exp(R_k/\lambda)}{\sum_{j=1}^{K}\exp(R_j/\lambda)}$$
  The weights are positive and sum to one, so every sample contributes in proportion to how good it was, and the temperature $\lambda>0$ sets how sharply they favour the best ($\lambda\to0$ recovers "take the single best"). Example: two samples whose first actions are $0.4$ and $0$, with returns $1$ and $0$ and $\lambda=1$, get weights $0.731$ and $0.269$, so the new first action is $0.292$.

§6 gives the
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

In symbols, with $h^*(n)$ the true cheapest cost from $n$ to the goal and $c(n,n')$ the cost of the edge $n\to n'$, the two conditions are:
$$\text{admissible: } 0\le h(n)\le h^*(n)\ \ \forall n,\qquad \text{consistent: } h(n)\le c(n,n')+h(n')\ \ \forall (n,n'),\ \ h(\text{goal})=0$$
Consistency implies admissibility, because summing its inequality along an optimal path from $n$ gives $h(n)\le h^*(n)$. Dijkstra is the case $h\equiv0$, which is both. **Optimal** here means that the returned path's cost equals the least cost $C^*$ over all paths in the graph. The proofs, a counterexample for each condition and an implementation are in [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms §6]].

**Think of the frontier as unfinished routes.** Each queued node represents a route that has reached somewhere but has not yet been explored onward. g records what that route has already cost. h estimates the remaining work, and f decides which unfinished route deserves attention next. Expanding a node means considering its outgoing edges; it does not mean the robot physically moves there.

If a cheaper route reaches an already encountered node, its best-known cost and parent may need updating. This bookkeeping is part of the algorithm, not a detail that can be ignored when quoting optimality. For nonnegative edge costs, consistency makes heuristic values cooperate with the graph's edges; admissibility alone requires appropriate handling of revisits.

**Check your understanding.** The heuristic is a lower-bound estimate for the graph problem, not permission to ignore obstacles in the final route. A straight-line distance can be useful precisely because it is optimistic, while collision checking still decides which graph connections are allowed. Search efficiency and physical feasibility are separate checks.

### 4. Worked example: what a heuristic changes

Suppose two frontier nodes have $(g,h)=(6,3)$ and $(4,6)$. Their A* priorities are $9$ and $10$, so the first is expanded even though it has a larger cost-to-come. The heuristic directs effort toward states estimated to be closer to the goal. An *underestimating* heuristic remains admissible — though if it is too weak, A* gains little speed over Dijkstra; an *overestimating* heuristic can lose the usual optimality guarantee.

### Worked case · 대상으로 한 번 끝까지

§4's $(g,h)$ pairs were bare numbers. Here they come from an object. **P2** from
[[02-foundations/lab-plants|0.6 Lab Plants]], unit links $L_1=L_2=1$ m, base at the world origin;
the panel is the half-plane $x<1$ m and the task point on it is $p^\star=(1,1)$ m. This half-plane is a keep-out region for the tip alone, not the physical panel of [[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2]] ($x\ge1$): the check below tests only the tip, so the base standing in $x<1$ does not count, whereas MR ch.2 checks the whole arm, and there the straight pose would collide. The arm starts
folded out straight, $q_\mathrm{start}=(0°,0°)$, tip at $(2,0)$. The question is the one §3 exists
for — which edge does A* return — and answering it needs all of §1, §2 and §3 at once.

**1. One task pose, two configurations.** Inverse kinematics on a planar 2R: with
$r=\lVert p^\star\rVert=\sqrt2=1.4142$ m, the law of cosines gives
$\cos\theta_2=(r^2-L_1^2-L_2^2)/(2L_1L_2)=(2-1-1)/2=0$, so $\theta_2=\pm90°$ and there are exactly
two goal configurations:

$$q_A=(0°,\ 90°),\qquad q_B=(90°,\ -90°)$$

Check $q_B$ by forward kinematics, since a goal you did not verify is a goal you invented:
$x=\cos 90°+\cos 0°=1$ and $y=\sin 90°+\sin 0°=1$, the same point. In $\mathcal{C}$ they are
$\lVert q_A-q_B\rVert=\sqrt{(\pi/2)^2+\pi^2}=\pi\sqrt{1.25}=3.512$ rad apart. That is §1's
non-example with a number on it: the end-effector pose is not a configuration, and here the two
configurations that realise one pose are three and a half radians of joint motion apart.

**2. Two different C-space paths, one workspace curve.** Interpolate each goal straight in joint
space. Branch A is $\theta(s)=(0°,\,90°s)$, so the tip is at $x=1+\cos(90°s)$, $y=\sin(90°s)$.
Branch B is $\theta(s)=(90°s,\,-90°s)$, whose shoulder-plus-elbow sum $\theta_1+\theta_2$ is $0$ for
every $s$, so its tip is at $x=\cos(90°s)+1$, $y=\sin(90°s)+0$ — the *same* two functions. Check at
the midpoint: A is $(0°,45°)$ and B is $(45°,-45°)$, and both put the tip at
$(1.7071,\ 0.7071)$. Both segments therefore trace the identical quarter circle of radius $1$
about $(1,0)$, and since $\cos(90°s)\ge0$ on $[0,1]$ both keep $x(s)\ge1$ throughout, with equality
only at $s=1$. Two different paths in $\mathcal{C}$, one path in the workspace, equal clearance —
which is why §1 insists these are different objects rather than two names for one.

**3. Same curve, different cost.** Cost the two edges by joint-space length, the usual default:

$$g_A=\lVert q_A-q_\mathrm{start}\rVert=\pi/2=1.5708\ \text{rad},\qquad g_B=\pi/\sqrt2=2.2214\ \text{rad}$$

so branch B costs exactly $\sqrt2$ times branch A while delivering the same tool motion. A
three-node graph — start, $q_A$, $q_B$ — and A* expands the start, pushes both goals, and returns
A.

**4. A heuristic that is admissible, and one that only looks it.** Take
$h(q)=\lVert p(q)-p^\star\rVert/\sqrt5$, the straight-line task-space distance scaled down. It is
admissible because on P2 no joint motion moves the tip faster than $\sqrt5$ times as fast: the
largest singular value of $J$ satisfies $\sigma_{\max}^2\le\operatorname{tr}(JJ^\top)=3+2\cos\theta_2\le5$,
with equality at $\theta_2=0$ where the arm is straight and $J$'s two columns are parallel. So a
joint path of length $\ell$ moves the tip at most $\sqrt5\,\ell$, and dividing by $\sqrt5$ turns a
workspace distance into a lower bound on joint distance. At the start
$h=\sqrt2/\sqrt5=0.6325$ rad, giving $f(q_\mathrm{start})=0+0.6325$, then $f(q_A)=1.5708$ and
$f(q_B)=2.2214$ once both are expanded. **Non-example:** the *unscaled* $\lVert p(q)-p^\star\rVert$
is not admissible on this arm, because $\sqrt5>1$ means it can exceed the true joint cost. On this
instance it happens not to — $1.4142<1.5708$ — so the bad heuristic passes the test case and is
still wrong, which is the failure mode worth remembering.

**5. What the tip check did not check.** Collision-checking the tip is not
collision-checking the arm. On branch B the elbow sits at $(\cos 90°s,\ \sin 90°s)$, whose
$x$-coordinate falls from $1$ to $0$, so against an *infinite* wall at $x=1$ the elbow — not the
tip — is inside the obstacle for every $s>0$; against the finite panel patch this page uses it is
free. The path did not change and the cost did not change; the answer to "is it collision-free"
changed because the obstacle model did. $\mathcal{C}_\mathrm{obs}$ is built from a specific
geometry, and a paper that reports a collision rate without reporting its collision model has
reported half a number.

**6. What "optimal" meant here.** Swap the metric and the answer moves. Under the max-norm, which
is what you want when each joint has its own speed limit, the cost is
$\max_i\lvert\Delta\theta_i\rvert=\pi/2$ for *both* branches, a tie; at $1$ rad/s per joint both
execute in $1.571$ s. Joint-Euclidean prefers A by $\sqrt2$; execution time cannot tell them apart.
Neither number says anything about the force the tool will apply when the tip reaches the panel —
that is contact, not $\mathcal{C}_\mathrm{free}$, and it is where the problem set ends.

### 5. Major method families

| Family | Representative ideas | Best read as |
|---|---|---|
| Graph search | BFS, Dijkstra, A* | Search over an explicit discretization |
| Sampling based | PRM, RRT, RRT* | Explore high-dimensional free space through samples |
| Trajectory optimization | shooting, transcription, collocation | Optimize states/inputs under constraints |
| Task planning | symbolic operators and goals | Choose discrete actions |
| TAMP | task and motion planning | Couple symbolic choices to geometric feasibility |
| Feedback / potential field | attractive-to-goal plus repulsive-from-obstacle fields; navigation functions (potentials constructed to have a single minimum, at the goal) | Produce an action for *every* state rather than one path — cheap and reactive, but a plain potential field has local minima that trap the robot short of the goal |
| Uncertain planning | MDP, POMDP, belief space | Choose actions while accounting for uncertain state/outcomes |

**The potential field, written out.** A potential field is a scalar function $U:\mathcal{C}\to\mathbb{R}$ whose downhill direction is the command, $\dot q=-\nabla U(q)$. It is built from an attractive part and a repulsive part:
$$U(q)=\tfrac12 k_a\lVert q-q_{\text{goal}}\rVert^2+\begin{cases}\tfrac12 k_r\big(\tfrac1{\rho(q)}-\tfrac1{\rho_0}\big)^2 & \rho(q)\le\rho_0\\ 0 & \rho(q)>\rho_0\end{cases}$$
Here $k_a,k_r>0$ are gains, $\rho(q)$ is the distance to the nearest obstacle and $\rho_0$ is the range beyond which obstacles are ignored, so the robot slides toward the goal and is pushed back ever harder as $\rho\to0$. A **navigation function** (Rimon & Koditschek 1992) is a potential that satisfies four further conditions: it is smooth on the free space, has a *unique* minimum at the goal, is uniformly maximal on every obstacle boundary, and has only non-degenerate critical points. Its gradient therefore reaches the goal from almost every start.

> [!example] Worked example · 계산 예제
> Goal at the origin, a point obstacle at $(1,0)$, and $k_a=k_r=\rho_0=1$. On the axis beyond the obstacle ($x>1$) the attractive force at $x$ is $-x$ and the repulsive force is $(1/\rho-1)/\rho^2$ with $\rho=x-1$. They cancel at $x=1.618$ ($\rho=0.618$), so a robot released at $(2,0)$ comes to rest there, short of the goal.
>
> **Non-example of a local minimum:** that point is a *saddle*. Moving sideways lowers the potential, $\partial^2U/\partial y^2=1-1.618/0.618=-1.62<0$, so any perturbation lets the robot slide around the obstacle. A concave obstacle such as a U-shaped wall creates a true minimum, and that is the trap the table warns of.

**Completeness, in four strengths.** These words state what a planner guarantees about *finding* a solution, and each has an exact meaning.

- **Complete**: for every problem instance, it returns a solution in finite time when one exists and reports failure in finite time when none does. Exact cell decomposition achieves this in low dimensions; almost nothing practical does in high dimensions.
- **Resolution complete**: complete *relative to a discretisation*. If a solution exists in the grid or lattice at the chosen resolution, the search finds it, and otherwise it reports failure. A* on a grid is resolution complete, but a passage narrower than a cell can be missed, so failure at one resolution proves nothing about the continuous problem.
- **Probabilistically complete**: when a *robust* solution exists, the probability of having found one approaches one as the number of samples $n$ grows,
$$\lim_{n\to\infty}P\big(\text{a solution is found within } n \text{ samples}\big)=1$$
  where robust (or $\delta$-clear) means a path whose $\delta$-neighbourhood lies in $\mathcal{C}_{\text{free}}$ for some $\delta>0$, since a path that only grazes obstacles has probability zero of being sampled. The method cannot report "no solution": failure after any finite $n$ is still possible. PRM and RRT have this property. It does not mean fast success.
- **Asymptotically optimal**: the cost $c_n$ of the best solution after $n$ samples converges to the optimal cost $c^*$ with probability one. This is a statement about the limit, so it says nothing about the quality available under a real-time budget. RRT\* and PRM\* have it; plain RRT does not (§5.5).
$$P\Big(\lim_{n\to\infty}c_n=c^*\Big)=1$$

> [!example] Worked example · 계산 예제
> In a simplified model, suppose every solution passes through a narrow passage that fills 1% of $\mathcal{C}$, and the planner succeeds once one uniform sample lands inside it. Each sample misses with probability $0.99$, independently, so the failure probability after $n$ samples is $0.99^n$: $0.366$ at $n=100$, $0.0066$ at $n=500$, and $4.3\times10^{-5}$ at $n=1000$. It tends to zero, which is probabilistic completeness, yet a third of the 100-sample runs fail, which is why the guarantee says nothing about speed.
>
> **Non-example of completeness:** a grid of 10 cm cells can return "no path" on a map whose only gap is 5 cm wide, because every cell that straddles the gap is marked occupied. The answer is correct for the grid, as resolution completeness promises, and wrong for the world.



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

- **Nonholonomic.** A car has no sideways velocity and a minimum turning radius, so a path with a corner or a sideways shift is undrivable as written, even though the car can still reach every pose ([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR ch.13]] explains why). Formally, a nonholonomic constraint is a velocity constraint $A(q)\dot q=0$ that cannot be integrated into a constraint on $q$ alone. For a car or unicycle with heading $\theta$ it reads as follows, because the velocity must point along the heading:
$$\dot x\sin\theta-\dot y\cos\theta=0$$
  At $\theta=0$, forward motion $(\dot x,\dot y)=(1,0)$ gives $0$ and is allowed, while sideways motion $(0,1)$ gives $-1$ and is forbidden. A **holonomic** constraint $g(q)=0$ removes a dimension from $\mathcal{C}$; a nonholonomic one removes directions of motion but no reachable configurations.
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

**Every symbol.** $x_t\in\mathbb{R}^n$ is the state at step $t$ and $u_t\in\mathbb{R}^m$ the input. $N$ is the **horizon**, the number of steps. The **running** (or **stage**) **cost** $\ell(x_t,u_t)$ is a scalar paid at every step, such as distance to the goal or control effort. The **terminal cost** $\ell_f(x_N)$ is paid once, on the final state, and is often written $\phi(x_T)$. Their sum is the objective $J$, so the program minimises the total cost of one proposed future. The constraints have three named kinds:

- **dynamics** $x_{t+1}=f(x_t,u_t)$ for every $t$, with $x_0$ fixed to the current state;
- **bounds** such as $u_{\min}\le u_t\le u_{\max}$;
- **collision constraints** such as $\mathrm{sd}(x_t)\ge d_{\text{safe}}$, where $\mathrm{sd}$ is the signed distance to the nearest obstacle.

This is the general program of [[02-foundations/optimization|4. Optimization §1]] with the decision variable spread over time, and its linear-quadratic special case, written as a QP, is in [[02-foundations/optimization|4. Optimization §5]].

> [!example] Worked example · 계산 예제
> Take scalar dynamics $x_{t+1}=x_t+u_t$ with $x_0=1$, $N=2$, $\ell=x_t^2+u_t^2$ and $\ell_f=x_N^2$. The inputs $(-0.5,-0.5)$ give the states $1, 0.5, 0$ and $J=(1+0.25)+(0.25+0.25)+0=1.75$. The inputs $(-1,0)$ reach the goal a step sooner, with states $1,0,0$, but $J=(1+1)+(0+0)+0=2$, since one large input costs more than two half-size ones. Doing nothing, $(0,0)$, gives $J=1+1+1=3$.
>
> **Non-example of a candidate:** the states $1,0,0$ paired with the inputs $(0,0)$ would cost only $1$, but they violate $x_1=x_0+u_0$, so they are not a trajectory at all. Ruling that out is the job of the dynamics constraint.

- **Given:** initial state, model, goal, constraints, and cost.
- **Optimized:** state and/or input sequence.
- **Runtime:** offline planning or repeated online as MPC.
- **Caveat:** nonlinear dynamics and obstacle constraints usually create local, initialization-sensitive problems.

The three classic ways to hand this program to a solver differ in what they make a decision variable:

- **Direct shooting** optimizes only the controls $u_{0:N-1}$ and obtains the states by simulating forward from $x_0$. There are few variables and the dynamics always hold, but a small change to an early input moves the whole rest of the trajectory, so long horizons become badly conditioned.
- **Direct transcription** makes both states and controls variables and writes the dynamics $x_{t+1}=f(x_t,u_t)$ as equality constraints. There are more variables, but each constraint touches only neighbouring steps, and the solver can start from an infeasible guess such as a straight line of states through an obstacle and repair it.
- **Collocation** is transcription with a smoother trajectory representation: polynomials between knot points, with the dynamics enforced by requiring the polynomial's derivative to equal $f(x,u)$ at selected points.

None automatically proves global optimality in a nonconvex robot problem.

**Unpack the subscripts as a proposed future.** x₀ is fixed by the current estimated state. Later x values describe predicted states, and u values are the inputs that would produce them under the model. Stage costs judge each part of the future, while the terminal cost values where the horizon ends. The dynamics constraints tie this imagined sequence together so the optimizer cannot choose attractive states disconnected from achievable motion.

MPC makes this formulation into feedback: execute the first input, observe the new state, and solve again. The unexecuted future still mattered because it influenced the first decision. Replanning then corrects discrepancies instead of assuming the entire prediction came true. An offline trajectory optimizer may solve a similar mathematical problem without performing this repeated feedback loop.

**Check your understanding.** A solver's feasible output is conditional on its initial state, model, discretization, and constraints. If state estimates are stale or a collision occurs between checked points, solving the optimization accurately is not enough. See the [trajectory-optimization notes](https://underactuated.mit.edu/trajopt.html) for the distinction between representing a trajectory and executing it with feedback.

### 7. Task planning, uncertainty, and replanning

A symbolic instruction such as `pick(block)` may be logically valid yet geometrically impossible because no collision-free grasp exists. TAMP alternates or jointly reasons over discrete actions and continuous feasibility.

**Symbolic task planning, defined.** A classical (STRIPS-style) planning problem has four parts. There is a set of Boolean **propositions**, facts such as `holding(block)`. A **state** $s$ is the set of propositions currently true, with an initial state $s_0$ and a **goal** $G$, the set of propositions that must end up true. And there are **operators**, each with a precondition set $\mathrm{pre}(a)$, an add list $\mathrm{add}(a)$ and a delete list $\mathrm{del}(a)$. An operator is applicable in $s$ when $\mathrm{pre}(a)\subseteq s$, and applying it replaces exactly the facts it names, so the successor state is
$$s'=\big(s\setminus\mathrm{del}(a)\big)\cup\mathrm{add}(a)$$
A plan is a sequence of applicable operators after which $G\subseteq s$. Example, simplified: `pick(block)` with pre $\{$`handempty`, `clear(block)`$\}$, del $\{$`handempty`$\}$ and add $\{$`holding(block)`$\}$ takes $\{$`handempty`, `clear(block)`$\}$ to $\{$`clear(block)`, `holding(block)`$\}$. **Non-example:** nothing in that state records where the block is or whether a collision-free grasp exists, so a valid symbolic plan is not yet an executable one. That gap is what TAMP fills.

**MDP and POMDP, as tuples.** An **MDP** is $(\mathcal{S},\mathcal{A},T,R,\gamma)$: a state set, an action set, a transition kernel $T(s'\mid s,a)$, a reward $R(s,a)$ and a discount $\gamma\in[0,1]$, together with the Markov property that the next state depends only on the current state and action. Its complete definition is [[02-foundations/rl-basics|RL Basics §1]].

With partial observability, the planning state becomes a **belief**: a probability distribution over the hidden state, updated after every action and observation. A POMDP distinguishes hidden state, observation, action, transition, observation model, and reward. Written as a tuple, a **POMDP** is
$$(\mathcal{S},\mathcal{A},\Omega,T,Z,R,\gamma,b_0)$$
which adds three components to the MDP, because the state is no longer seen: an **observation space** $\Omega$, an **observation model** $Z(o\mid s',a)$ giving the probability of observing $o$ when action $a$ has led to state $s'$, and an **initial belief** $b_0$. The belief $b(s)$ is the posterior probability of state $s$ given every action and observation so far. After taking $a$ and observing $o$, Bayes' rule updates it:
$$b'(s')=\eta\,Z(o\mid s',a)\sum_{s\in\mathcal{S}}T(s'\mid s,a)\,b(s)$$
The sum is the **prediction**, which pushes the old belief through the dynamics; the factor $Z$ is the **correction**, which weights each state by how well it explains $o$; and $\eta$ is the normaliser that makes $b'$ sum to one. This is the Bayes filter of [[04-robotics/state-estimation-slam|3. State Estimation §4]] with a chosen action attached. Since the belief summarises the whole history, a POMDP is an MDP whose states are beliefs, with expected reward $\rho(b,a)=\sum_s b(s)\,R(s,a)$. **Non-example:** the latest observation alone is not a Markov state. The same "open" reading moves a belief of $0.5$ to $0.8$ but a belief of $0.8$ to $0.94$ in the example below.

> [!example] Worked example · 계산 예제
> A robot must go through a door it cannot see clearly. **Hidden state:** open or closed. **Action:** look again, or drive through. **Transition:** looking changes nothing; driving moves the robot. **Observation:** a sensor reading "open" or "closed". **Observation model:** the reading is right 80% of the time. **Reward:** $+1$ for getting through, $-1$ for hitting a closed door.
>
> Start from belief $P(\text{open})=0.5$. One "open" reading gives $0.8\cdot0.5/(0.8\cdot0.5+0.2\cdot0.5)=0.8$; a second gives $0.8\cdot0.8/(0.8\cdot0.8+0.2\cdot0.2)\approx0.94$. These are the update formula above: looking leaves the state unchanged, so the sum is just $b(s')$, $Z$ is $0.8$ or $0.2$, and $\eta=1/0.5=2$ the first time and $1/0.68=1.47$ the second. Driving at belief 0.8 has expected reward $\rho=0.8\cdot(+1)+0.2\cdot(-1)=0.6$; at 0.94 it is $0.88$. Whether one more look is worth its time is exactly the question a POMDP planner answers, and it is asked about the belief, not the true door.

Exact belief-space planning is often intractable, so papers use approximations, receding horizons, learned values, or contingency policies.

Online replanning incorporates new observations. Reported replanning frequency is not enough: compare it with perception latency, scene dynamics, and controller bandwidth.

### 8. Learning-based planning

Learned components may provide a heuristic, cost, dynamics/world model, value function, proposal distribution, trajectory generator, or entire policy. A VLA that outputs actions is usually a policy; a world model that rolls out futures supports planning only when a selection or optimization procedure uses those futures.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> “Generates plausible trajectories” does not imply collision-free, dynamically feasible, stable, or safe execution. Check explicit constraints, downstream controllers, replanning, and closed-loop robot results.

### 9. Evaluation and failure modes

Check success rate, collision rate, path/trajectory cost, planning and execution time, optimality gap (the relative excess cost $(C-C^*)/C^*$, so an 11 m path against a 10 m optimum is a 10% gap), constraint violation, replanning rate, robustness to map/state error, and closed-loop execution. Separate planning failure, perception failure, tracking failure, and hardware failure.

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

### Problem set · 과제

Tier B. First pass. **P2** to the panel ([[02-foundations/lab-plants|0.6]]). Two-node graph. No simulator.

1. **Draw.** The picture above: node $q_\mathrm{start}=\theta=(0^\circ,0^\circ)$ (tip at $(2,0)$) and $q_\mathrm{goal}=$ frozen pose (tip at $(1,1)$ on the panel). One edge in $\mathcal{C}$. Label $\mathcal{C}_\mathrm{free}$.
2. **Derive.** Straight interpolation $\theta(s)=(0^\circ,90^\circ s)$. Tip $x(s)=1+\cos(90^\circ s)$. If the panel is the wall $x=1$, when does the tip first touch? What does A* return on this two-node graph?
3. **Interpret.** What can this search not promise about contact force at the panel?

> [!note]- How to draw it · 그리는 법
> - Left panel, the workspace: the base at the origin, the reachable disc of radius $2$ m around it, the panel as a vertical line at $x=1$ with hatching on its far side, and the task point $p^\star=(1,1)$ m on that line.
> - The arm twice: once straight along $+x$ with its tip at $(2,0)$, once at the frozen pose with its elbow at $(1,0)$ and its tip on the panel. Two configurations, one picture, and nothing on it is yet a plan.
> - Right panel, the configuration space: axes $\theta_1$ and $\theta_2$, each from $-180°$ to $180°$, with a note that opposite edges are identified. $\mathcal{C}$ is the torus $T^2$, and a planner that treats $179°$ and $-179°$ as far apart is using the wrong space (§2).
> - $q_\mathrm{start}$ and $q_\mathrm{goal}$ as two dots, joined by the straight segment that is the graph's single edge.
> - The region the tip-only check forbids, $\cos\theta_1+\cos(\theta_1+\theta_2)<1$, shaded, and the rest labelled $\mathcal{C}_\mathrm{free}$.
> - The one point of the segment that lies on the boundary, marked as contact, not free space.
> - One arrow from the segment on the right to the curve the tip traces on the left, labelled $f$, the forward kinematics. The two panels are not two views of one object: the right is a set of configurations, the left a set of positions, and that arrow is the only thing relating them.

> [!tip]- Solutions
> 1. Two dots in $\mathcal{C}=T^2$, one segment. Free except the goal, which is on the contact set.
> 2. $x(s)=1$ only at $s=1$, so the open segment is free. A* returns that single edge as a feasible path (cost = whatever you put on it).
> 3. A path is geometry without force. Search does not know $k_w$, $\mu$, or $F_n$ — those are contact, not $\mathcal{C}_\mathrm{free}$ (Self-check 1: collision-free $\neq$ dynamically / contact feasible).

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
- D. Fox, W. Burgard, S. Thrun, "The dynamic window approach to collision avoidance," *IEEE Robotics & Automation Magazine* 4(1), 23–33, 1997.
- E. Rimon, D. E. Koditschek, "Exact robot navigation using artificial potential functions," *IEEE Transactions on Robotics and Automation* 8(5), 501–518, 1992.
- S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005 — ch.9 (occupancy grid log-odds update).

## 한국어

*C군이고, 그 안에 있는 유일한 페이지다. [[04-robotics/modern-robotics/index|MR 챕터 요약]]과 [[04-robotics/mpc|7. MPC]], 그리고 최적화·RL 기초 위에 선다.
실행 가능한 미래를 고르는 문제이며, I군이 이것을 비정형 환경으로 특수화한다.*

Planning은 목표에 도달하기 위한 실행 가능한 미래 상태·행동 시퀀스를 고르는 문제다.
어려움은 짧은 경로 찾기가 아니다: 로봇 형상, 동역학, 접촉, 불확실성, 계산 시간, 변하는
관측이 실제로 실행할 수 있는 것을 제약한다.

*범위: 이 페이지는 대상과 보장을 가르친다 — §1의 다섯 단어, §2의 공간들과 지도·비용 표현, §5의 완전성 네 강도, §5.5의 경로를 운전 불가능하게 만드는 제약들, §6의 궤적 최적화 문제 형태 — 그리고 논문을 어느 계열에 놓을지 판단할 만큼의 각 방법군. 어떤 알고리즘도 구현 깊이로는 가르치지 않는다. A\*의 증명과 코드는 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘 §6]]에 있고, 샘플링 플래너는 여기서 조망만 하며 이 위키 어디에도 구현하지 않는다. 후퇴 지평 제어는 [[04-robotics/mpc|7. MPC]], 정책 학습은 [[02-foundations/rl-basics|RL 기초]], 실제 내비게이션 스택 하나의 구체적 파라미터는 [[04-robotics/ros2/navigation-nav2|25.9 Nav2]]다.*

> [!info] 깊이 목표
> 탐색·모션 플래닝·궤적 최적화·과제 계획·정책 학습·제어를 구분한다; feasibility와
> optimality 주장을 읽는다; 생성된 궤적이 충돌 없음·동역학적 실행 가능·폐루프 평가인지
> 판별한다.

> [!note] 선수 지식
> [[02-foundations/optimization|최적화]] · [[02-foundations/rl-basics|RL 기초]] · [[04-robotics/modern-robotics/ch02-configuration-space|컨피규레이션 공간]] · [[04-robotics/modern-robotics/ch10-motion-planning|모션 플래닝]] — §6은 [[04-robotics/mpc|MPC]](트랙 7번)를 미리 쓴다; 여기서는 가볍게 읽고 그 페이지 후에 돌아오라.

> [!note] 처음이라면 · First pass
> 먼저 §1 — 문헌이 섞어 쓰지만 섞어 쓰면 안 되는 다섯 단어 — 그다음 §2, 그다음 §4의 계산 예제. §5~§8은 조망이니 전부가 아니라 지금 논문이 속한 계열만 읽어라.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 320" style="max-width:100%;height:auto" role="img" aria-label="왼쪽: 반지름 2 m 도달 원판, 패널 선 x = 1 m, 과제 점 (1, 1), 말단이 (2, 0)에 있는 곧게 편 팔과 엘보 (1, 0), 말단 (1, 1)의 고정 자세, 말단이 그리는 사분원을 그린 P2의 작업 영역. 오른쪽: q_start = (0, 0)과 q_goal = (0, 90도), 그 사이의 유일한 간선, 말단 검사가 금지하는 영역의 음영, 그 경계 위의 목표를 그린 컨피규레이션 공간 토러스. 순기구학 화살표 f가 둘을 잇는다.">
  <defs><marker id="aPDMk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <circle cx="128.0" cy="162.0" r="100" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="128.0" y1="162.0" x2="57.3" y2="91.3" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55" stroke-dasharray="2 3"/>
  <line x1="178.0" y1="75.4" x2="178.0" y2="248.6" stroke="currentColor" stroke-width="1.3"/>
  <path d="M178.0 79.4 l-7 7 M178.0 88.4 l-7 7 M178.0 97.4 l-7 7 M178.0 106.4 l-7 7 M178.0 115.4 l-7 7 M178.0 124.4 l-7 7 M178.0 133.4 l-7 7 M178.0 142.4 l-7 7 M178.0 151.4 l-7 7 M178.0 160.4 l-7 7 M178.0 169.4 l-7 7 M178.0 178.4 l-7 7 M178.0 187.4 l-7 7 M178.0 196.4 l-7 7 M178.0 205.4 l-7 7 M178.0 214.4 l-7 7 M178.0 223.4 l-7 7 M178.0 232.4 l-7 7 M178.0 241.4 l-7 7" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" fill="none"/>
  <path d="M228.0 162.0 A50 50 0 0 0 178.0 112.0" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>
  <g stroke="currentColor" stroke-linecap="round" fill="none">
    <polyline points="128.0,162.0 178.0,162.0 228.0,162.0" stroke-width="4" stroke-opacity="0.35"/>
    <polyline points="128.0,162.0 178.0,162.0 178.0,112.0" stroke-width="3"/>
  </g>
  <circle cx="128.0" cy="162.0" r="4.5" fill="currentColor"/>
  <circle cx="178.0" cy="162.0" r="3.5" fill="currentColor"/>
  <circle cx="228.0" cy="162.0" r="3.5" fill="currentColor" fill-opacity="0.45"/>
  <circle cx="178.0" cy="112.0" r="4.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <path d="M352 72 h180 v180 h-180 Z M397 117 L398 110.4 L399 108.2 L400 106.8 L401 105.7 L402 104.9 L403 104.2 L404 103.6 L405 103.2 L406 102.9 L407 102.6 L408 102.4 L409 102.2 L410 102.1 L411 102 L412 102 L413 102 L414 102.1 L415 102.2 L416 102.3 L417 102.5 L418 102.7 L419 102.9 L420 103.1 L421 103.4 L422 103.8 L423 104.1 L424 104.5 L425 104.9 L426 105.4 L427 105.8 L428 106.4 L429 106.9 L430 107.5 L431 108.1 L432 108.7 L433 109.4 L434 110.1 L435 110.9 L436 111.6 L437 112.4 L438 113.3 L439 114.2 L440 115.1 L441 116 L442 117 L443 118 L444 119.1 L445 120.2 L446 121.3 L447 122.4 L448 123.6 L449 124.9 L450 126.1 L451 127.4 L452 128.7 L453 130.1 L454 131.5 L455 132.9 L456 134.4 L457 135.8 L458 137.4 L459 138.9 L460 140.5 L461 142.1 L462 143.8 L463 145.4 L464 147.1 L465 148.9 L466 150.7 L467 152.5 L468 154.3 L469 156.2 L470 158.1 L471 160 L472 162 L473 164 L474 166.1 L475 168.2 L476 170.4 L477 172.6 L478 174.9 L479 177.2 L480 179.6 L481 182.2 L482 184.9 L483 187.7 L484 190.8 L485 194.2 L486 198.4 L487 207 L487 207 L486 213.6 L485 215.8 L484 217.2 L483 218.3 L482 219.1 L481 219.8 L480 220.4 L479 220.8 L478 221.1 L477 221.4 L476 221.6 L475 221.8 L474 221.9 L473 222 L472 222 L471 222 L470 221.9 L469 221.8 L468 221.7 L467 221.5 L466 221.3 L465 221.1 L464 220.9 L463 220.6 L462 220.2 L461 219.9 L460 219.5 L459 219.1 L458 218.6 L457 218.2 L456 217.6 L455 217.1 L454 216.5 L453 215.9 L452 215.3 L451 214.6 L450 213.9 L449 213.1 L448 212.4 L447 211.6 L446 210.7 L445 209.8 L444 208.9 L443 208 L442 207 L441 206 L440 204.9 L439 203.8 L438 202.7 L437 201.6 L436 200.4 L435 199.1 L434 197.9 L433 196.6 L432 195.3 L431 193.9 L430 192.5 L429 191.1 L428 189.6 L427 188.2 L426 186.6 L425 185.1 L424 183.5 L423 181.9 L422 180.2 L421 178.6 L420 176.9 L419 175.1 L418 173.3 L417 171.5 L416 169.7 L415 167.8 L414 165.9 L413 164 L412 162 L411 160 L410 157.9 L409 155.8 L408 153.6 L407 151.4 L406 149.1 L405 146.8 L404 144.4 L403 141.8 L402 139.1 L401 136.3 L400 133.2 L399 129.8 L398 125.6 L397 117 Z" fill="currentColor" fill-opacity="0.16" fill-rule="evenodd"/>
  <path d="M397 117 L398 110.4 L399 108.2 L400 106.8 L401 105.7 L402 104.9 L403 104.2 L404 103.6 L405 103.2 L406 102.9 L407 102.6 L408 102.4 L409 102.2 L410 102.1 L411 102 L412 102 L413 102 L414 102.1 L415 102.2 L416 102.3 L417 102.5 L418 102.7 L419 102.9 L420 103.1 L421 103.4 L422 103.8 L423 104.1 L424 104.5 L425 104.9 L426 105.4 L427 105.8 L428 106.4 L429 106.9 L430 107.5 L431 108.1 L432 108.7 L433 109.4 L434 110.1 L435 110.9 L436 111.6 L437 112.4 L438 113.3 L439 114.2 L440 115.1 L441 116 L442 117 L443 118 L444 119.1 L445 120.2 L446 121.3 L447 122.4 L448 123.6 L449 124.9 L450 126.1 L451 127.4 L452 128.7 L453 130.1 L454 131.5 L455 132.9 L456 134.4 L457 135.8 L458 137.4 L459 138.9 L460 140.5 L461 142.1 L462 143.8 L463 145.4 L464 147.1 L465 148.9 L466 150.7 L467 152.5 L468 154.3 L469 156.2 L470 158.1 L471 160 L472 162 L473 164 L474 166.1 L475 168.2 L476 170.4 L477 172.6 L478 174.9 L479 177.2 L480 179.6 L481 182.2 L482 184.9 L483 187.7 L484 190.8 L485 194.2 L486 198.4 L487 207 L487 207 L486 213.6 L485 215.8 L484 217.2 L483 218.3 L482 219.1 L481 219.8 L480 220.4 L479 220.8 L478 221.1 L477 221.4 L476 221.6 L475 221.8 L474 221.9 L473 222 L472 222 L471 222 L470 221.9 L469 221.8 L468 221.7 L467 221.5 L466 221.3 L465 221.1 L464 220.9 L463 220.6 L462 220.2 L461 219.9 L460 219.5 L459 219.1 L458 218.6 L457 218.2 L456 217.6 L455 217.1 L454 216.5 L453 215.9 L452 215.3 L451 214.6 L450 213.9 L449 213.1 L448 212.4 L447 211.6 L446 210.7 L445 209.8 L444 208.9 L443 208 L442 207 L441 206 L440 204.9 L439 203.8 L438 202.7 L437 201.6 L436 200.4 L435 199.1 L434 197.9 L433 196.6 L432 195.3 L431 193.9 L430 192.5 L429 191.1 L428 189.6 L427 188.2 L426 186.6 L425 185.1 L424 183.5 L423 181.9 L422 180.2 L421 178.6 L420 176.9 L419 175.1 L418 173.3 L417 171.5 L416 169.7 L415 167.8 L414 165.9 L413 164 L412 162 L411 160 L410 157.9 L409 155.8 L408 153.6 L407 151.4 L406 149.1 L405 146.8 L404 144.4 L403 141.8 L402 139.1 L401 136.3 L400 133.2 L399 129.8 L398 125.6 L397 117 Z" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <rect x="352" y="72" width="180" height="180" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <path d="M348 210 L352 204 L356 210 M528 210 L532 204 L536 210 M496 68 L502 72 L496 76 M502 68 L508 72 L502 76 M496 248 L502 252 L496 256 M502 248 L508 252 L502 256" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.5">
    <line x1="397" y1="252" x2="397" y2="256"/>
    <line x1="348" y1="207" x2="352" y2="207"/>
    <line x1="442" y1="252" x2="442" y2="256"/>
    <line x1="348" y1="162" x2="352" y2="162"/>
    <line x1="487" y1="252" x2="487" y2="256"/>
    <line x1="348" y1="117" x2="352" y2="117"/>
  </g>
  <line x1="442" y1="162" x2="442" y2="117" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="442" cy="162" r="4" fill="currentColor"/>
  <circle cx="442" cy="117" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="442" y1="111" x2="442" y2="64" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <path d="M437 139.5 Q 327.7 82.6 218.4 126.6" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#aPDMk)"/>
  <circle cx="442" cy="139.5" r="2.6" fill="currentColor"/>
  <circle cx="213.4" cy="126.6" r="2.6" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
    <text x="10" y="20" font-size="12">작업 영역: 위치 (m)</text>
    <text x="322" y="20" font-size="12">컨피규레이션 공간 C = T²: 각도</text>
    <text x="119.0" y="166.0" text-anchor="end">베이스 (0, 0)</text>
    <text x="169.0" y="179.0" text-anchor="end" opacity="0.9">엘보 (1, 0)</text>
    <text x="234.0" y="156.0" opacity="0.75">말단 (2, 0)</text>
    <text x="170.0" y="104.0" text-anchor="end">p* = (1, 1)</text>
    <text x="182.0" y="71.4">패널 x = 1 m</text>
    <text x="97" y="113" text-anchor="middle" opacity="0.85">r = 2 m</text>
    <text x="209" y="110.5" opacity="0.85">말단 경로</text>
    <text x="292" y="100.6" text-anchor="middle">f: 순기구학</text>
    <text x="417" y="149.5" text-anchor="middle" font-size="12">C<tspan font-size="9.5" dy="3">free</tspan><tspan dy="-3" dx="1.5"></tspan></text>
    <text x="358" y="244" opacity="0.85">말단 x &lt; 1: 금지</text>
    <text x="449" y="175">q<tspan font-size="9.5" dy="3">start</tspan><tspan dy="-3" dx="1.5"> (0°, 0°)</tspan></text>
    <text x="442" y="60" text-anchor="middle">q<tspan font-size="9.5" dy="3">goal</tspan><tspan dy="-3" dx="1.5"> (0°, 90°): 경계 위, 곧 접촉</tspan></text>
    <text x="352" y="267" text-anchor="middle" font-size="11">−180°</text>
    <text x="346" y="256" text-anchor="end" font-size="11">−180°</text>
    <text x="442" y="267" text-anchor="middle" font-size="11">0°</text>
    <text x="346" y="166" text-anchor="end" font-size="11">0°</text>
    <text x="532" y="267" text-anchor="middle" font-size="11">180°</text>
    <text x="346" y="76" text-anchor="end" font-size="11">180°</text>
    <text x="482" y="267" font-size="12">θ<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="326" y="150" font-size="12">θ<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="532.0" y="284" text-anchor="end" font-size="11" opacity="0.85">마주 보는 변은 붙어 있다: 179°와 −179°는 이웃</text>
    <text x="10" y="307" opacity="0.9">플래너의 보장은 오른쪽 칸에 대한 주장이고, 로봇이 하는 일은 왼쪽 칸에 있다.</text>
  </g>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**(단위 링크, 베이스는 월드 원점)와 반평면 $x<1$ m인 패널을 §2의 그림과 같은 짝으로 나란히 놓았다. 왼쪽 작업 영역에는 $2$ m 도달 원판, 말단이 $(2,0)$에 있는 곧게 편 팔과 엘보가 $(1,0)$, 말단이 과제 점 $p^\star=(1,1)$에 있는 고정 자세, 그리고 둘 사이에서 말단이 그리는 사분원이 있다. 오른쪽은 마주 보는 변이 붙은 컨피규레이션 공간 $\mathcal{C}=T^2$로, $q_\mathrm{start}=(0°,0°)$에서 $q_\mathrm{goal}=(0°,90°)$까지의 유일한 간선과 말단 검사가 금지하는 영역 $\cos\theta_1+\cos(\theta_1+\theta_2)<1$의 음영이 있고, 목표는 그 경계 위(자유 공간이 아니라 접촉)에 있으며, 두 칸을 잇는 것은 순기구학 화살표 $f$뿐이다.

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

**다섯 가지를 수학적 대상으로 쓰면.** $\mathcal{C}$를 컨피규레이션 공간, $\mathcal{X}$를 상태 공간, $\mathcal{U}$를 입력 공간이라 하자(셋 다 §2에서 정의한다).

- **path**는 정규화된 매개변수 $s$에서 컨피규레이션으로 가는 연속 사상이고, 양 끝이 고정되어 있다. 매개변수는 시간이 아니므로 path는 *어디로*만 말한다.
$$\sigma:[0,1]\to\mathcal{C},\qquad \sigma(0)=q_{\text{start}},\quad \sigma(1)=q_{\text{goal}}$$
- **trajectory**는 시간을 더한다: 지속 시간 $T$ 동안 상태와 (대개) 입력을 시간의 함수로 준다. 모든 trajectory는 path 하나를 그리지만, path 하나에는 trajectory가 무한히 많다. $s(0)=0$, $s(T)=1$인 증가하는 시간 스케일링 $s(t)$마다 다른 trajectory가 나오기 때문이다([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]).
$$x:[0,T]\to\mathcal{X},\qquad u:[0,T]\to\mathcal{U}$$
- **plan**은 실행 *전에* 한 시작 상태에 대해 계산한 결정의 유한 열 $(a_0,\dots,a_{K-1})$이다. 기호적 행동일 수도, 웨이포인트나 입력일 수도 있다.
- **policy**는 실행 *중에* 평가하는 규칙이다. 가용 정보 $I_t$(상태, 관측 이력, belief)를 행동 $a_t=\pi(I_t)$ 또는 분포 $\pi(a_t\mid I_t)$로 사상한다([[02-foundations/rl-basics|RL 기초 §1]]).
- **controller**는 측정 상태와 기준으로부터 구동기 명령을 계산하는, 대개 빠른 피드백 법칙 $u_t=\kappa(x_t,\,x^{\text{ref}}_t)$이다.

가장 중요한 구분은 plan과 policy다. plan은 한 시작점에 대한 답 하나이고, policy는 만날 수 있는 모든 상태에 대한 답이다. 예: $(0,0)$에서 $(1,0)$ m까지의 직선 구간은 path 하나다. 이를 일정한 0.5 m/s로 달리면 $T=2$ s인 trajectory이고, 1 m/s로 달리면 같은 path 위의 다른 trajectory($T=1$ s)다. **반례:** 시각이 없는 웨이포인트 목록은 path나 plan이지 trajectory가 아니다. 그래서 무언가가 시간을 매겨 주기 전에는 속도·가속도 한계에 비추어 검사할 수 없다.

### 2. 공간과 제약

- **작업 영역(workspace):** 로봇과 장애물이 차지하는 물리적 위치.
- **컨피규레이션 공간:** 로봇 컨피규레이션; 장애물은 금지 영역이 된다.
- **상태 공간:** 컨피규레이션 + 속도 같은 변수.
- **행동/입력 공간:** 시스템이 쓸 수 있는 명령.
- **과제 공간(task space):** 말단 pose처럼 과제에 직접 묶인 변수.

작업 영역에서 충돌이 없다는 것이 관절·토크·속도·안정성·접촉의 실행 가능성을 함의하지
않는다.

**컨피규레이션 공간의 정의.** **컨피규레이션** $q$는 로봇의 모든 점의 위치를 지정한 것이다. 조건이 둘이다. **완전**해야 한다 — 위치가 정해지지 않는 몸체의 점이 없어야 한다. 그리고 **최소**여야 한다 — 더 짧은 수의 목록으로 같은 일을 할 수 없어야 한다. **컨피규레이션 공간** $\mathcal{C}$는 모든 컨피규레이션의 집합이고, 차원이 자유도 수가 되는 것은 이 최소성 때문이다:

$$\mathcal{C}=\{\,q:q\ \text{는 로봇의 모든 점을 지정한다}\,\},\qquad \dim\mathcal{C}=\text{dof}$$

개수보다 집합이 중요하다. $\mathcal{C}$는 대개 상자가 아니기 때문이다. 평면 2R 팔의 것은 직사각형 $[0,2\pi)^2$가 아니라 토러스 $T^2$다. 관절각이 각각 한 바퀴 돌아 붙기 때문이다 — 그래서 $359°$와 $1°$를 멀다고 보는 플래너는 틀린 공간을 쓰고 있는 것이다. **반례:** 말단 pose는 여유 자유도를 가진 팔의 컨피규레이션이 *아니다*. 같은 pose를 주는 관절 벡터가 여럿이라 몸체의 점들이 정해지지 않기 때문이다. 그것은 위 목록의 마지막 항목인 과제 공간이다.

$\mathcal{C}$는 **C-장애물** $\mathcal{C}_{\text{obs}}$와 **자유 공간** $\mathcal{C}_{\text{free}}=\mathcal{C}\setminus\mathcal{C}_{\text{obs}}$로 나뉜다. 둘 다 [[04-robotics/modern-robotics/ch02-configuration-space|MR 2장 §2]]에서 정의되고 장치 **P2** 위에서 유도되며 예와 반례까지 붙어 있다. 이 페이지는 다시 쓰지 않고 가져다 쓴다. 그 정의의 두 귀결이 이 페이지의 나머지가 딛고 선 것이다. C-장애물은 *컨피규레이션*의 집합이지 결코 작업 영역의 영역이 아니라는 것, 그리고 이 구성이 모양을 가진 로봇을 $\mathcal{C}_{\text{free}}$ 안을 움직이는 *점*으로 줄인다는 것 — 아래의 모든 플래너가 쓰인 형태가 그것이다.

그러면 **경로 계획 문제**는 이렇다: $q_{\text{start}},q_{\text{goal}}\in\mathcal{C}_{\text{free}}$가 주어졌을 때 모든 $s\in[0,1]$에서 $\sigma(s)\in\mathcal{C}_{\text{free}}$인 path $\sigma$(§1)를 찾거나, 없다고 보고한다. **상태 공간** $\mathcal{X}$는 속도를 더한 $x=(q,\dot q)$이므로 자유도 $n$인 로봇의 상태는 $2n$차원이다. **입력 공간** $\mathcal{U}$는 허용되는 명령의 집합이다. 예를 들어 구동기마다 $|u_i|\le u_{\max}$다. 작업 영역과 과제 공간은 물리적 위치나 pose의 집합이고 $\mathcal{C}$는 로봇 컨피규레이션의 집합이다. 아래 그림에 칸이 두 개 필요한 이유다.

> [!example] 계산 예제 · Worked example
> MR 2장은 *팔*의 C-장애물을 유도한다. 거기서는 토러스 위의 휘어진 렌즈다. 여기서는 다른 쪽 경우, 아래의 격자 팽창이 기대고 있는 경우를 본다. 회전하지 않고 평행이동만 하는 반경 0.5 m 원판 로봇의 컨피규레이션은 중심 $q=(x,y)$이므로 $\mathcal{C}=\mathbb{R}^2$다. 정사각형 장애물 $[1,2]\times[1,2]$ m가 있으면, 중심이 정사각형에서 0.5 m보다 가까울 때 정확히 $q\in\mathcal{C}_{\text{obs}}$다. $q=(0.6,1.5)$는 0.4 m 떨어져 있으므로, 작업 영역의 *점* $(0.6,1.5)$는 비어 있는데도 $\mathcal{C}_{\text{obs}}$에 속한다. $q=(0.4,1.5)$는 0.6 m 떨어져 있어 자유다.
>
> **반례:** C-장애물은 정사각형을 상자 $[0.5,2.5]^2$로 키운 것이 아니다. 정사각형과 원판의 민코프스키 합이라 모서리가 둥글다. 그래서 그 상자 안의 $q=(0.6,0.6)$은 모서리 $(1,1)$에서 0.566 m라 자유이고, 0.424 m인 $(0.7,0.7)$은 자유가 아니다. 이것이 아래 목록의 팽창이며, 로봇이 원판이기 때문에만 정확하다.

**그 공간을 실제로 저장하는 방법.** 이 위키의 두 페이지가 점유·비용 표현을 위해 여기로
보내므로, 시스템 논문의 부록이 아니라 이 절에 있어야 한다.

- **점유 격자(occupancy grid)** — 지도를 격자로 두고 각 칸이 점유되어 있을 확률을 담는다.
  갱신은 **로그 승산(log-odds)** $\ell=\log\frac{p}{1-p}$ 으로 한다. 이 값은 $p=0.5$를 $0$으로,
  $p\to 0$이나 $1$을 $\mp\infty$로 보낸다. 베이즈 규칙은 칸의 승산 $p/(1-p)$에 새 측정마다
  우도비를 곱하므로, 로그를 취하면 증거 누적이 곱셈이 아니라 덧셈이 된다(OctoMap의 $+0.85$는
  $\log(0.7/0.3)$, 즉 $p=0.7$짜리 "적중" 하나다). 또한 확률이 0이나 1에 바짝 붙었을 때의 수치 문제를 피할 수 있다. 남는 위험의 방향을 짚어야 한다:
  로그 승산은 *유계가 아니어서*, 점유로 천 번 관측된 칸은 뒤집으려면 반대 관측이 천 번 단위로 필요하다(OctoMap 기본 로그 승산 증분 +0.85/−0.4이면 약 2,100번) —
  그래서 구현들은 명시적 **클램핑** 범위를 둔다(Yguel 외 2007이 제안하고 OctoMap이 채택). 세상이 바뀌었을 때 지도가
  적응할 수 있게 하려는 것이다. 칸은 *비어 있음*, *점유됨*, 그리고
  **미지**의 셋 중 하나이고, 초심자가 빠뜨리는 것이 셋째다. 미지는 비어 있음이 아니며,
  그 차이가 곧 탐색이 존재하는 이유다.
  **갱신 식.** $m_i=1$을 "칸 $i$가 점유됨", $p_0$을 사전 점유 확률이라 하자. 판독 $z_t$마다 자기 증거를 더하고, 사전 확률은 판독마다 다시 세지 않도록 한 번 뺀다:
  $$\ell_t(i)=\ell_{t-1}(i)+\log\frac{p(m_i=1\mid z_t)}{1-p(m_i=1\mid z_t)}-\log\frac{p_0}{1-p_0},\qquad p=1-\frac{1}{1+e^{\ell}}$$
  가운데 항은 **역센서 모델**(inverse sensor model), 즉 이 판독 하나만으로 본 점유 확률이고, 둘째 식은 로그 승산을 확률로 되돌린다. $p_0=0.5$이면 사전 항은 $0$이다. 그러면 OctoMap 적중 두 번은 $\ell=1.70$, $p=0.846$을 주고, 그 뒤 빗나감 한 번($-0.4$)은 $\ell=1.30$, $p=0.786$을 준다. 클램핑은 매 갱신 뒤 $\ell$을 구간 $[\ell_{\min},\ell_{\max}]$ 안에 가둔다.
- **팽창(inflation)** — 로봇을 점으로 다루는 계획기(아래 그림)는 대신 장애물을 키워야 한다.
  점유 칸을 로봇 반경만큼 팽창시키면 **원형 로봇에 한해** 격자 위에서 바로 C-공간 장애물이
  된다 — 다른 형상에서는 근사이고, 그래서 Nav2 같은 스택은 별도의 footprint 충돌 검사를 따로
  돌린다. 그 바깥에 감쇠하는 비용을 더하면 계획기가 들어가기를 꺼리는 여유가 생긴다. 칸에서 가장 가까운 장애물 칸까지의 거리 $d$, 내접 로봇 반경 $r$, 감쇠율 $\alpha>0$에 대해 ROS costmap은 지수 함수를 쓴다:
  $$c(d)=\begin{cases}c_{\text{lethal}} & d=0\\ c_{\text{insc}} & 0<d\le r\\ c_{\text{insc}}\,e^{-\alpha(d-r)} & r<d\le d_{\text{infl}}\\ 0 & d>d_{\text{infl}}\end{cases}$$
  내접 반경 안의 칸은 로봇 중심을 거기 두면 반드시 충돌한다는 뜻이고, 그 바깥에서 비용은 거리에 따라 감쇠하며, 팽창 반경 $d_{\text{infl}}$ 너머의 칸은 비용이 없다. $\alpha=3$ /m이면 내접 반경에서 0.2 m 바깥 칸의 비용은 내접값의 $e^{-0.6}=0.55$배다. $\alpha$를 키우면 여유가 좁아진다.
  **반경이 셋이고, 셋은 같은 수가 아니다.** footprint에는 **내접 반경** $r_{\text{insc}}$ — 로봇 원점을 중심으로 그 안에 *들어가는* 가장 큰 원의 반경 — 과 **외접 반경** $r_{\text{circ}}$ — footprint를 *담는* 가장 작은 원 — 이 있다. 장애물에서 $r_{\text{insc}}$ 안이면 어느 방향으로 서 있든 충돌이고, $r_{\text{circ}}$ 밖이면 어느 방향으로 서 있든 안전하며, 그 사이에서는 충돌 여부가 방향에 달려 있다. footprint 검사가 존재하는 이유가 바로 그 띠다. **팽창 반경** $d_{\text{infl}}$은 아예 세 번째 것이다. 감쇠 비용을 0으로 자르는 거리다. 이것은 *선호* 손잡이이지 안전 여유가 아니다 — 안전을 담당하는 것은 $d_{\text{infl}}$이 아니라 footprint에서 나오는 $r_{\text{insc}}$다. **반례, 그리고 이 생태계에서 가장 흔한 오설정:** `inflation_radius`를 "벽에서 이만큼 떨어뜨려라"로 읽는 것([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §5]]). $r_{\text{insc}}=0.30$ m, $\alpha=3$ /m, $d_{\text{infl}}=1.00$ m에 ROS의 바이트 척도(장애물 칸 자체가 $c_{\text{lethal}}=254$, $c_{\text{insc}}=253$, 치맛자락은 $252$로 스케일)를 쓰면 비용은 $d=0.50$ m에서 $252\,e^{-0.6}=138$, $0.80$ m에서 $56$, $1.00$ m 바로 안쪽에서 $30$ — 그리고 바로 바깥에서 $0$이다. $d_{\text{infl}}$에서의 이 30짜리 단차가 **비용 절벽**이다. 위의 경사 따라가기 논증이 살아남지 못하는 불연속이므로, 잘리는 값이 충분히 작아지도록 $d_{\text{infl}}$을 크게 잡아야 한다.
- **비용 지도(costmap)** — 칸이 이진값이 아니라 *통행 비용*을 담는 점유 격자다. 비용은
  팽창에 더해 로봇이 피해야 할 다른 모든 것을 합친다: 미지 영역, 거친 지형, 일방향 구역,
  진입 금지 구역. **비용 지도는 정책적 선호가 계획이기를 그만두고 기하가 되는 자리다** —
  [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성 §1]]이 학습된
  어포던스를 담기에 *맞는* 그릇이라고 논하는 바로 그 표현이다. 같은 장면이 로봇마다 다른
  costmap을 내놓기 때문이다. 그 페이지가 거부하는 것은 기하 술어인 점유 격자 쪽이고, 그것을 보려면 이것이
  무엇인지 알아야 한다.
- **계층형 비용 지도** — 계획기가 읽는 비용 지도는 모두가 같이 쓰는 격자 하나가 아니다.
  순서가 정해진 **층(layer)** 목록을 합성해서 만든 **마스터 격자**이고, 한 층은 갱신 주기마다
  정확히 두 가지 연산을 수행하는 구성 요소다. 먼저 자기가 건드릴 지도의 사각형 범위를
  선언하고, 그다음 그 사각형 안에서 마스터 격자에 비용을 쓴다. 이것을 격자 더미가 아니라
  계층형 비용 지도로 만드는 조건이 둘이다. 각 층은 *앞선 층들이 남겨 놓은 상태의* 마스터
  격자를 보고, 각 층은 선언된 결합 규칙 — **덮어쓰기**, **최댓값**, 또는 미지를 무시한
  최댓값 — 으로 쓴다. 그러므로 순서가 명세의 일부이고 합성은 교환되지 않는다. 보통의 순서는
  정적 지도, 그다음 장애물(실시간 센서 데이터로 표시하고 지운다), 그다음 팽창이며, 팽창이
  마지막이어야 하는 이유는 앞선 층들이 치명으로 남긴 것까지의 거리를 재기 때문이다.
  *예*: 사람이 로봇 앞으로 들어온다. 장애물 층이 그 칸들을 표시하고 팽창 층이 그것을 키운다.
  사람이 걸어 나가면 광선 투사가 정확히 그 칸들만 지우고, 뒤의 벽은 그대로다. 애초에 그 벽은
  장애물 층이 쓴 것이 아니기 때문이다. **반례**: 납작한 격자 하나. 거기서 낡은 사람을
  지우려면 정적 지도도 자기 것이라고 주장하는 칸을 지워야 하므로, 벽이 지워지거나 사람이
  영영 남거나 둘 중 하나다 — 층이 존재하는 이유 전부가 이것이다. *읽을 때 왜 중요한가*:
  논문 속의 "비용 지도"는 합성물이고, 어느 층이 그 비용을 썼는지가 그것을 지울 수 있는지를
  결정한다([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §4]]에 한 스택의 층 목록과 기본값이 있다).
- **Frontier** — *알려진 자유 공간*과 *미지* 사이의 경계 칸. 정확히는 자신은 자유로 알려져 있고 이웃(4-연결 또는 8-연결) 중 적어도 하나가 미지인 칸이다. **frontier 탐색**은 "다음에
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
장애물을 놓고 다음 몇 초의 운동을 반복해서 고른다. 고전적 이름들이 사는 곳이 지역 층이다.

| 지역 계획기 | 매 주기에 하는 일 |
|---|---|
| *Dynamic window* | 한 주기 안에 도달할 수 있는 속도 쌍(전진, 회전)을 표본으로 뽑아 각각 점수를 매긴다 |
| **Elastic band** | 내부 수축력과 외부 장애물 반발력으로 시간 개념 없이 *경로*를 변형한다 |
| **Timed elastic band** | 이름이 가리키는 시간 간격을 더한 후손이다 |
| **표본 기반 MPC**([[01-canonical-papers/notes/9-navigation/badgr\|BADGR]]이 쓰는 계열) | running estimate 주변에서 많은 행동열을 표본으로 뽑아 모델로 굴린 뒤, 가장 좋은 하나를 고르는 대신 **보상 가중 평균**으로 추정을 갱신하고 그 첫 행동을 실행한다 |

**두 행을 식으로 쓰면.**

- **Dynamic window** (Fox, Burgard & Thrun 1997). $(v_c,\omega_c)$를 현재 전진·회전 속도, $\dot v_{\max},\dot\omega_{\max}$를 가속도 한계, $\Delta t$를 주기라 하자. 후보는 세 조건을 동시에 만족해야 한다. 로봇이 애초에 낼 수 있는 속도여야 한다($V_s$). 한 주기 안에 도달할 수 있어야 하는데, 가속도가 유계이므로 이것은 작은 상자다:
$$V_d=\{(v,\omega): |v-v_c|\le\dot v_{\max}\Delta t,\ |\omega-\omega_c|\le\dot\omega_{\max}\Delta t\}$$
  그리고 **허용 가능**해야 한다. 즉 그 호 위의 가장 가까운 장애물 앞에서 멈출 수 있어야 하므로, 제동 감속도 $\dot v_b$에 대해 $v\le\sqrt{2\,\mathrm{dist}(v,\omega)\,\dot v_b}$다($\omega$도 마찬가지). $V_s\cap V_d\cap V_a$의 각 쌍에 목표 방향·여유 거리·속력의 가중합으로 점수를 매기고, 최고의 쌍을 한 주기 동안 실행한다. 예: $v_c=0.5$ m/s, $\dot v_{\max}=0.5$ m/s², $\Delta t=0.25$ s이면 $v\in[0.375,0.625]$ m/s다. 호를 따라 0.5 m 앞의 장애물은 $\dot v_b=0.5$ m/s²에서 $v$를 $\sqrt{0.5}=0.71$ m/s로 제한하므로, 여기서 묶는 한계는 장애물이 아니라 창이다.
- **보상 가중 평균.** 현재 추정 $\bar u$ 주변에서 행동열 $K$개 $u^{(k)}$를 뽑아 모델로 굴려 반환값 $R_k$를 얻고, 다시 맞춘다:
$$\bar u\leftarrow\sum_{k=1}^{K}w_k\,u^{(k)},\qquad w_k=\frac{\exp(R_k/\lambda)}{\sum_{j=1}^{K}\exp(R_j/\lambda)}$$
  가중치는 양수이고 합이 1이므로 모든 표본이 좋은 정도에 비례해 기여하고, 온도 $\lambda>0$가 최고 표본을 얼마나 날카롭게 편애할지 정한다($\lambda\to0$이면 "가장 좋은 하나 고르기"로 돌아간다). 예: 첫 행동이 $0.4$와 $0$, 반환값이 $1$과 $0$인 두 표본에 $\lambda=1$이면 가중치는 $0.731$과 $0.269$이고, 새 첫 행동은 $0.292$다.

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

기호로 쓰면, $h^*(n)$을 $n$에서 목표까지의 참 최소 비용, $c(n,n')$을 간선 $n\to n'$의 비용이라 할 때 두 조건은 다음과 같다:
$$\text{admissible: } 0\le h(n)\le h^*(n)\ \ \forall n,\qquad \text{consistent: } h(n)\le c(n,n')+h(n')\ \ \forall (n,n'),\ \ h(\text{goal})=0$$
일관성은 허용성을 함의한다. $n$에서 나가는 최적 경로를 따라 부등식을 더하면 $h(n)\le h^*(n)$이 나오기 때문이다. Dijkstra는 $h\equiv0$인 경우이고 둘 다 만족한다. 여기서 **최적**이란 돌려준 경로의 비용이 그래프 안 모든 경로의 최소 비용 $C^*$와 같다는 뜻이다. 증명, 각 조건의 반례, 구현은 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘 §6]]에 있다.

**프런티어를 아직 끝나지 않은 경로로 생각한다.** 대기 중인 노드는 어느 곳까지 도달했지만 그 뒤를 아직 탐색하지 않은 경로다. g는 이미 쓴 비용, h는 남은 일의 추정, f는 다음으로 볼 경로의 우선순위다. 노드를 확장한다는 것은 나가는 간선을 검토한다는 뜻이다. 로봇이 실제로 그곳으로 움직이는 것은 아니다.

이미 본 노드에 더 싼 경로가 도달하면 알려진 최저 비용과 부모를 갱신해야 할 수 있다. 최적성을 말할 때 생략해도 되는 구현 세부가 아니라 알고리즘의 일부다. 음수가 아닌 간선 비용에서 일관성은 휴리스틱과 간선 비용이 맞물리게 한다. 허용성만 있으면 재방문을 적절히 처리해야 한다.

**이해 확인.** 휴리스틱은 그래프 문제의 하한 추정이지 최종 경로에서 장애물을 무시할 허가가 아니다. 직선 거리는 낙관적이어서 유용할 수 있고, 실제 허용 연결은 충돌 검사가 정한다. 탐색 효율과 물리적 가능성은 별도 검사다.

### 4. 계산 예제: 휴리스틱이 바꾸는 것

프런티어의 두 노드가 $(g,h)=(6,3)$과 $(4,6)$이라 하자. A* 우선순위는 $9$와 $10$이므로,
cost-to-come이 더 큰데도 첫 노드가 먼저 확장된다. 휴리스틱은 목표에 가깝다고 추정되는
상태 쪽으로 노력을 돌린다. *과소평가* 휴리스틱은 admissible을 유지한다 — 너무 약하면 A*가 Dijkstra보다 빨라지는
이득이 거의 없을 뿐이다; *과대평가* 휴리스틱은 통상적 최적성 보장을 잃을 수 있다.

### 대상으로 한 번 끝까지 · Worked case

§4의 $(g,h)$ 쌍은 맨 숫자였다. 여기서는 그것이 대상에서 나온다.
[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 단위 링크 $L_1=L_2=1$ m, 베이스는 월드
원점. 패널은 반평면 $x<1$ m이고 그 위의 과제 점은 $p^\star=(1,1)$ m다. 이 반평면은 말단만을 위한 진입 금지 영역이지 [[04-robotics/modern-robotics/ch02-configuration-space|MR 2장]]의 물리적 패널($x\ge1$)이 아니다. 아래의 검사는 말단만 시험하므로 $x<1$에 선 베이스는 따지지 않는다. MR 2장은 팔 전체를 검사하고, 거기서는 곧게 편 자세가 충돌한다. 팔은 곧게 편
$q_\mathrm{start}=(0°,0°)$에서 출발하며 말단은 $(2,0)$에 있다. 물음은 §3이 존재하는 이유 그
자체 — A*가 어떤 간선을 돌려주는가 — 이고, 답하려면 §1·§2·§3이 한꺼번에 필요하다.

**1. 과제 pose 하나, 컨피규레이션 둘.** 평면 2R의 역기구학:
$r=\lVert p^\star\rVert=\sqrt2=1.4142$ m이므로 코사인 법칙이
$\cos\theta_2=(r^2-L_1^2-L_2^2)/(2L_1L_2)=(2-1-1)/2=0$을 주고 $\theta_2=\pm90°$, 곧 목표
컨피규레이션이 정확히 둘이다.

$$q_A=(0°,\ 90°),\qquad q_B=(90°,\ -90°)$$

$q_B$는 순기구학으로 검산한다. 검산하지 않은 목표는 지어낸 목표이기 때문이다.
$x=\cos 90°+\cos 0°=1$, $y=\sin 90°+\sin 0°=1$로 같은 점이다. $\mathcal{C}$ 안에서 둘은
$\lVert q_A-q_B\rVert=\sqrt{(\pi/2)^2+\pi^2}=\pi\sqrt{1.25}=3.512$ rad 떨어져 있다. §1의 반례에
숫자를 붙인 것이 이것이다. 말단 pose는 컨피규레이션이 아니고, 여기서 한 pose를 실현하는 두
컨피규레이션은 관절 운동으로 3.5 rad이나 떨어져 있다.

**2. 서로 다른 $\mathcal{C}$ 경로 둘, 작업 영역 곡선 하나.** 두 목표를 각각 관절 공간에서 직선
보간한다. 가지 A는 $\theta(s)=(0°,\,90°s)$이므로 말단은 $x=1+\cos(90°s)$, $y=\sin(90°s)$에 있다.
가지 B는 $\theta(s)=(90°s,\,-90°s)$이고 $\theta_1+\theta_2$가 모든 $s$에서 $0$이므로 말단은
$x=\cos(90°s)+1$, $y=\sin(90°s)+0$ — *같은* 두 함수다. 중간점에서 검산하면 A는 $(0°,45°)$, B는
$(45°,-45°)$이고 둘 다 말단을 $(1.7071,\ 0.7071)$에 놓는다. 그러므로 두 구간은 $(1,0)$을 중심으로
한 반지름 $1$의 같은 사분원을 그리고, $[0,1]$에서 $\cos(90°s)\ge0$이므로 둘 다 내내 $x(s)\ge1$을
지키며 등호는 $s=1$에서만 성립한다. $\mathcal{C}$에서는 다른 경로 둘, 작업 영역에서는 경로 하나,
여유는 동일 — §1이 이 둘을 한 대상의 두 이름이 아니라 서로 다른 대상이라고 못 박는 이유다.

**3. 같은 곡선, 다른 비용.** 두 간선에 흔한 기본값인 관절 공간 길이로 값을 매긴다.

$$g_A=\lVert q_A-q_\mathrm{start}\rVert=\pi/2=1.5708\ \text{rad},\qquad g_B=\pi/\sqrt2=2.2214\ \text{rad}$$

따라서 가지 B는 같은 공구 운동을 주면서 가지 A의 정확히 $\sqrt2$배가 든다. 노드 셋짜리
그래프(시작, $q_A$, $q_B$)에서 A*는 시작을 확장하고 두 목표를 넣은 뒤 A를 돌려준다.

**4. admissible한 휴리스틱 하나와, 그렇게 보이기만 하는 것 하나.**
$h(q)=\lVert p(q)-p^\star\rVert/\sqrt5$, 곧 작업 공간 직선 거리를 줄인 값을 쓰자. 이것이
admissible한 이유는 P2에서 어떤 관절 운동도 말단을 $\sqrt5$배보다 빠르게 움직이지 못하기
때문이다. $J$의 최대 특잇값은
$\sigma_{\max}^2\le\operatorname{tr}(JJ^\top)=3+2\cos\theta_2\le5$를 만족하고, 등호는 팔이 곧게 펴져
$J$의 두 열이 평행해지는 $\theta_2=0$에서 성립한다. 그러니 길이 $\ell$의 관절 경로는 말단을 최대
$\sqrt5\,\ell$만큼 옮기고, $\sqrt5$로 나누면 작업 공간 거리가 관절 거리의 하한이 된다. 출발점에서
$h=\sqrt2/\sqrt5=0.6325$ rad이므로 $f(q_\mathrm{start})=0+0.6325$이고, 둘을 확장한 뒤에는
$f(q_A)=1.5708$, $f(q_B)=2.2214$다. **반례:** 나누지 않은 $\lVert p(q)-p^\star\rVert$는 이 팔에서
admissible하지 않다. $\sqrt5>1$이라 참 관절 비용을 넘을 수 있기 때문이다. 이 사례에서는 마침
넘지 않는다($1.4142<1.5708$). 잘못된 휴리스틱이 시험 사례를 통과하고도 여전히 틀린 것이며, 기억해
둘 실패 방식이 그것이다.

**5. 말단 검사가 검사하지 않은 것.** 말단을 충돌 검사하는 것은 팔을 충돌 검사하는 것이
아니다. 가지 B에서 엘보는 $(\cos 90°s,\ \sin 90°s)$에 있고 그 $x$ 좌표가 $1$에서 $0$으로
떨어지므로, $x=1$의 *무한* 벽에 대해서는 말단이 아니라 엘보가 $s>0$인 모든 곳에서 장애물 안에
있다. 이 페이지가 쓰는 유한한 패널 조각에 대해서는 자유롭다. 경로도 비용도 바뀌지 않았는데
"충돌이 없는가"의 답이 바뀐 것은 장애물 모델이 바뀌었기 때문이다. $\mathcal{C}_\mathrm{obs}$는
특정 기하에서 만들어지며, 충돌 모델을 밝히지 않은 채 충돌률을 보고한 논문은 숫자의 절반만 보고한
것이다.

**6. 여기서 "최적"이 뜻한 것.** 척도를 바꾸면 답이 움직인다. 관절마다 자기 속도 한계가 있을 때
쓰고 싶은 max-norm에서는 비용이 두 가지 모두 $\max_i\lvert\Delta\theta_i\rvert=\pi/2$로 동점이고,
관절당 $1$ rad/s면 둘 다 $1.571$초에 끝난다. 관절 유클리드는 A를 $\sqrt2$만큼 선호하고, 실행
시간은 둘을 구별하지 못한다. 그리고 두 숫자 중 어느 것도 말단이 패널에 닿을 때 공구가 가할 힘에
대해서는 아무 말도 하지 않는다. 그것은 $\mathcal{C}_\mathrm{free}$가 아니라 접촉이고, 과제가
끝나는 지점이 거기다.

### 5. 주요 방법 계열

| 계열 | 대표 아이디어 | 이렇게 읽어라 |
|---|---|---|
| 그래프 탐색 | BFS, Dijkstra, A* | 명시적 이산화 위의 탐색 |
| 샘플링 기반 | PRM, RRT, RRT* | 표본으로 고차원 자유 공간 탐사 |
| 궤적 최적화 | shooting, transcription, collocation | 제약 아래 상태/입력 최적화 |
| 과제 계획 | 기호적 연산자와 목표 | 이산 행동 선택 |
| TAMP | task and motion planning | 기호적 선택을 기하학적 실행 가능성과 결합 |
| 피드백 / 퍼텐셜장 | 목표로 끌고 장애물에서 미는 장; 내비게이션 함수(최솟값이 목표 한 곳에만 있도록 만든 퍼텐셜) | 경로 하나가 아니라 *모든* 상태에 대해 행동을 만든다 — 값싸고 반응적이지만, 단순한 퍼텐셜장에는 로봇을 목표 앞에서 가두는 국소 최솟값이 있다 |
| 불확실성 계획 | MDP, POMDP, belief space | 불확실한 상태/결과 아래 행동 선택 |

**퍼텐셜장을 식으로 쓰면.** 퍼텐셜장은 내리막 방향이 곧 명령인 스칼라 함수 $U:\mathcal{C}\to\mathbb{R}$이고, $\dot q=-\nabla U(q)$다. 끌어당기는 부분과 밀어내는 부분으로 만든다:
$$U(q)=\tfrac12 k_a\lVert q-q_{\text{goal}}\rVert^2+\begin{cases}\tfrac12 k_r\big(\tfrac1{\rho(q)}-\tfrac1{\rho_0}\big)^2 & \rho(q)\le\rho_0\\ 0 & \rho(q)>\rho_0\end{cases}$$
$k_a,k_r>0$는 이득, $\rho(q)$는 가장 가까운 장애물까지의 거리, $\rho_0$는 그보다 먼 장애물을 무시하는 범위다. 그래서 로봇은 목표 쪽으로 미끄러지고 $\rho\to0$일수록 점점 세게 밀려난다. **내비게이션 함수**(Rimon & Koditschek 1992)는 조건 넷을 더 만족하는 퍼텐셜이다: 자유 공간에서 매끄럽고, 최솟값이 목표 한 곳에*만* 있고, 모든 장애물 경계에서 균일하게 최대이며, 임계점이 모두 비퇴화다. 그래서 그 기울기를 따라가면 거의 모든 출발점에서 목표에 닿는다.

> [!example] 계산 예제 · Worked example
> 목표는 원점, 점 장애물은 $(1,0)$, $k_a=k_r=\rho_0=1$이다. 장애물 너머의 축($x>1$) 위의 $x$에서 인력은 $-x$, 척력은 $\rho=x-1$로 두어 $(1/\rho-1)/\rho^2$다. 둘은 $x=1.618$($\rho=0.618$)에서 상쇄되므로, $(2,0)$에서 놓은 로봇은 목표에 못 미친 그곳에서 멈춘다.
>
> **국소 최솟값의 반례:** 그 점은 *안장점*이다. 옆으로 움직이면 퍼텐셜이 낮아지므로($\partial^2U/\partial y^2=1-1.618/0.618=-1.62<0$) 작은 교란만 있어도 로봇은 장애물을 돌아 미끄러진다. U자 벽 같은 오목한 장애물은 진짜 최솟값을 만들고, 표가 경고하는 함정이 그것이다.

**완전성의 네 강도.** 이 낱말들은 계획기가 해를 *찾는 것*에 대해 무엇을 보장하는지 말하며, 각각 정확한 뜻이 있다.

- **완전(complete)**: 모든 문제 사례에서, 해가 있으면 유한 시간 안에 해를 돌려주고 없으면 유한 시간 안에 실패를 보고한다. 저차원에서는 정확한 셀 분해가 이를 달성하지만, 고차원에서 실용적인 방법은 거의 없다.
- **해상도 완전(resolution complete)**: *이산화에 대해* 완전하다. 정한 해상도의 격자나 lattice 안에 해가 있으면 찾고, 없으면 실패를 보고한다. 격자 위의 A*가 해상도 완전하지만 칸보다 좁은 통로는 놓칠 수 있으므로, 한 해상도에서의 실패는 연속 문제에 대해 아무것도 증명하지 않는다.
- **확률적 완전(probabilistically complete)**: *robust한* 해가 존재하면, 표본 수 $n$이 늘수록 해를 찾았을 확률이 1로 간다.
$$\lim_{n\to\infty}P\big(\text{a solution is found within } n \text{ samples}\big)=1$$
  robust(또는 $\delta$-여유)란 어떤 $\delta>0$에 대해 $\delta$-근방이 $\mathcal{C}_{\text{free}}$ 안에 있는 경로라는 뜻이다. 장애물을 스치기만 하는 경로는 표본으로 뽑힐 확률이 0이기 때문이다. 이 방법은 "해 없음"을 보고할 수 없다: 유한한 어떤 $n$ 뒤에도 실패가 가능하다. PRM과 RRT가 이 성질을 가진다. 빠른 성공을 뜻하지 않는다.
- **점근적 최적(asymptotically optimal)**: 표본 $n$개 뒤 최선의 해의 비용 $c_n$이 확률 1로 최적 비용 $c^*$에 수렴한다. 극한에 대한 진술이므로 실시간 예산에서 얻는 품질에 대해서는 아무것도 말하지 않는다. RRT\*와 PRM\*는 이 성질을 가지고, 단순 RRT는 가지지 않는다(§5.5).
$$P\Big(\lim_{n\to\infty}c_n=c^*\Big)=1$$

> [!example] 계산 예제 · Worked example
> 단순화한 모형에서, 모든 해가 $\mathcal{C}$의 1%를 차지하는 좁은 통로를 지나고, 균일 표본 하나가 그 안에 떨어지면 계획기가 성공한다고 하자. 표본마다 독립적으로 확률 $0.99$로 빗나가므로 $n$개 뒤 실패 확률은 $0.99^n$이다: $n=100$에서 $0.366$, $n=500$에서 $0.0066$, $n=1000$에서 $4.3\times10^{-5}$. 0으로 가므로 확률적 완전이지만, 표본 100개짜리 실행의 3분의 1은 실패한다. 이 보장이 속도에 대해 아무것도 말하지 않는 이유다.
>
> **완전성의 반례:** 10 cm 칸 격자는 유일한 틈이 5 cm인 지도에서 "경로 없음"을 돌려줄 수 있다. 틈에 걸친 칸이 모두 점유로 표시되기 때문이다. 해상도 완전성이 약속한 대로 격자에 대해서는 맞는 답이고, 세계에 대해서는 틀린 답이다.

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

- **비홀로노믹 제약.** 자동차에는 옆 방향 속도가 없고 최소 회전 반경이 있다. 그래서 모서리나 옆으로 비키는 구간이 있는 경로는 쓰인 그대로는 운전할 수 없다. 그래도 차는 모든 pose에 도달할 수 있다(이유는 [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR 13장]]). 형식적으로 쓰면, 비홀로노믹 제약은 $q$만에 대한 제약으로 적분할 수 없는 속도 제약 $A(q)\dot q=0$이다. heading이 $\theta$인 자동차나 유니사이클에서는 속도가 heading 방향을 가리켜야 하므로 다음과 같다:
$$\dot x\sin\theta-\dot y\cos\theta=0$$
  $\theta=0$에서 전진 운동 $(\dot x,\dot y)=(1,0)$은 $0$을 주어 허용되고, 옆 방향 운동 $(0,1)$은 $-1$을 주어 금지된다. **홀로노믹** 제약 $g(q)=0$은 $\mathcal{C}$에서 차원 하나를 없애지만, 비홀로노믹 제약은 운동 방향을 없앨 뿐 도달 가능한 컨피규레이션은 하나도 없애지 않는다.
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

흔한 정식화는 [[02-foundations/optimization|4. 최적화]]의 궤적 최적화 프로그램이다 — 매 스텝 내는 실행 비용에 마지막의 종단 비용을 더한 것으로 읽되, 물리와 장애물이 제약이다.

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. 동역학, 한계, 충돌 제약}$$

**모든 기호.** $x_t\in\mathbb{R}^n$은 스텝 $t$의 상태, $u_t\in\mathbb{R}^m$은 입력이다. $N$은 스텝의 수인 **지평**(horizon)이다. **실행 비용**(running cost), 또는 **단계 비용**(stage cost) $\ell(x_t,u_t)$는 목표까지의 거리나 제어 노력처럼 매 스텝 치르는 스칼라다. **종단 비용** $\ell_f(x_N)$은 마지막 상태에 대해 한 번만 치르고, 흔히 $\phi(x_T)$로 쓴다. 둘의 합이 목적함수 $J$이므로, 이 프로그램은 제안된 미래 하나의 총비용을 최소화한다. 제약에는 이름 붙은 세 종류가 있다.

- 모든 $t$에서의 **동역학** $x_{t+1}=f(x_t,u_t)$(단 $x_0$은 현재 상태로 고정);
- $u_{\min}\le u_t\le u_{\max}$ 같은 **한계**;
- $\mathrm{sd}(x_t)\ge d_{\text{safe}}$ 같은 **충돌 제약**. 여기서 $\mathrm{sd}$는 가장 가까운 장애물까지의 부호 거리(signed distance)다.

이것은 [[02-foundations/optimization|4. 최적화 §1]]의 일반 프로그램에서 결정 변수를 시간에 걸쳐 펼친 것이고, 선형-이차 특수 경우를 QP로 쓴 것은 [[02-foundations/optimization|4. 최적화 §5]]에 있다.

> [!example] 계산 예제 · Worked example
> 스칼라 동역학 $x_{t+1}=x_t+u_t$에 $x_0=1$, $N=2$, $\ell=x_t^2+u_t^2$, $\ell_f=x_N^2$을 두자. 입력 $(-0.5,-0.5)$는 상태 $1, 0.5, 0$과 $J=(1+0.25)+(0.25+0.25)+0=1.75$를 준다. 입력 $(-1,0)$은 상태 $1,0,0$으로 한 스텝 먼저 목표에 닿지만 $J=(1+1)+(0+0)+0=2$다. 큰 입력 하나가 절반 크기 입력 둘보다 비싸기 때문이다. 아무것도 하지 않는 $(0,0)$은 $J=1+1+1=3$을 준다.
>
> **후보의 반례:** 상태 $1,0,0$을 입력 $(0,0)$과 짝지으면 비용이 $1$뿐이지만, $x_1=x_0+u_0$을 어기므로 애초에 궤적이 아니다. 그것을 걸러내는 것이 동역학 제약의 일이다.

- **주어진 것:** 초기 상태, 모델, 목표, 제약, 비용.
- **최적화하는 것:** 상태·입력 시퀀스.
- **실행 시점:** 오프라인 계획 또는 MPC로 반복 온라인.
- **주의:** 비선형 동역학과 장애물 제약은 대개 국소적·초기화 민감 문제를 만든다.

이 프로그램을 풀이기에 넘기는 고전적 방식 세 가지는 무엇을 결정 변수로 삼느냐가 다르다.

- **Direct shooting**은 제어 $u_{0:N-1}$만 최적화하고, 상태는 $x_0$에서 앞으로 시뮬레이션해 얻는다. 변수가 적고 동역학이 늘 성립하지만, 앞쪽 입력을 조금만 바꿔도 나머지 궤적 전체가 움직여서 지평이 길면 조건수가 나빠진다.
- **Direct transcription**은 상태와 제어를 모두 변수로 두고 동역학 $x_{t+1}=f(x_t,u_t)$를 등식 제약으로 쓴다. 변수는 많지만 각 제약이 이웃한 스텝만 건드리고, 장애물을 관통하는 직선 상태열 같은 실행 불가능한 초기 추정에서 출발해 고쳐 나갈 수 있다.
- **Collocation**은 궤적을 더 매끄럽게 표현한 transcription이다. 매듭점 사이를 다항식으로 잇고, 선택한 점들에서 다항식의 도함수가 $f(x,u)$와 같도록 요구해 동역학을 강제한다.

어느 것도 비볼록 로봇 문제의 전역 최적성을 자동으로 증명하지 않는다.

**아래첨자를 제안한 미래로 풀어 읽는다.** x₀는 현재 추정 상태로 고정된다. 뒤의 x들은 예측 상태이고 u들은 모델상 그 상태를 만드는 입력이다. 단계 비용은 미래의 각 구간을 평가하고 종단 비용은 지평 끝의 위치를 평가한다. 동역학 제약이 상상한 시퀀스를 묶어, 실제 움직임으로 이어지지 않는 매력적인 상태만 고르지 못하게 한다.

MPC는 이 정식화를 피드백으로 쓴다. 첫 입력을 실행하고 새 상태를 관측한 뒤 다시 푼다. 실행하지 않은 미래도 첫 결정을 바꿨으므로 의미가 있다. 재계획은 예측이 모두 맞았다고 가정하는 대신 차이를 고친다. 오프라인 궤적 최적화는 비슷한 수학 문제를 풀어도 이 반복 피드백은 하지 않을 수 있다.

**이해 확인.** 해법의 실행 가능 출력은 초기 상태, 모델, 이산화, 제약에 조건부다. 상태 추정이 낡거나 검사 지점 사이에서 충돌하면 최적화를 정확히 푸는 것만으로 부족하다. 궤적 표현과 피드백 실행의 구분은 [궤적 최적화 강의](https://underactuated.mit.edu/trajopt.html)에서도 다룬다.

### 7. 과제 계획, 불확실성, replanning

`pick(block)` 같은 기호적 명령은 논리적으로 타당해도 충돌 없는 파지가 존재하지 않아
기하학적으로 불가능할 수 있다. TAMP는 이산 행동과 연속 실행 가능성을 번갈아 또는
공동으로 추론한다.

**기호적 과제 계획의 정의.** 고전적(STRIPS식) 계획 문제는 네 부분으로 이루어진다. 먼저 `holding(block)` 같은 사실, 곧 불리언 **명제**(proposition)의 집합이 있다. **상태** $s$는 지금 참인 명제의 집합이고, 초기 상태 $s_0$과 끝에 참이 되어야 하는 명제의 집합인 **목표** $G$가 있다. 그리고 **연산자**(operator)가 있는데, 연산자마다 전제 조건 집합 $\mathrm{pre}(a)$, 추가 목록 $\mathrm{add}(a)$, 삭제 목록 $\mathrm{del}(a)$를 가진다. 연산자는 $\mathrm{pre}(a)\subseteq s$일 때 $s$에서 적용할 수 있고, 적용하면 자기가 이름 붙인 사실만 정확히 바꾸므로 다음 상태는
$$s'=\big(s\setminus\mathrm{del}(a)\big)\cup\mathrm{add}(a)$$
이다. 계획은 적용 가능한 연산자들의 열로서, 그것을 다 적용한 뒤 $G\subseteq s$가 되는 것이다. 단순화한 예: pre $\{$`handempty`, `clear(block)`$\}$, del $\{$`handempty`$\}$, add $\{$`holding(block)`$\}$인 `pick(block)`은 $\{$`handempty`, `clear(block)`$\}$를 $\{$`clear(block)`, `holding(block)`$\}$로 옮긴다. **반례:** 그 상태 어디에도 블록이 어디 있는지, 충돌 없는 파지가 존재하는지가 기록되어 있지 않으므로, 타당한 기호적 계획이 아직 실행 가능한 계획은 아니다. 그 간극을 메우는 것이 TAMP다.

**튜플로 쓴 MDP와 POMDP.** **MDP** $(\mathcal{S},\mathcal{A},T,R,\gamma)$는 상태 집합, 행동 집합, 전이 커널 $T(s'\mid s,a)$, 보상 $R(s,a)$, 할인율 $\gamma\in[0,1]$로 이루어지고, 다음 상태가 현재 상태와 행동에만 달려 있다는 마르코프 성질을 함께 가진다. 완전한 정의는 [[02-foundations/rl-basics|RL 기초 §1]]에 있다.

부분 관측에서는 계획의 상태가 **belief**, 즉 숨은 상태에 대한 확률 분포가 되고, 행동과 관측이
있을 때마다 갱신된다. POMDP는 숨은 상태, 관측, 행동, 전이, 관측 모델, 보상을 구분한다. 튜플로 쓰면 **POMDP**(부분 관측 MDP)는
$$(\mathcal{S},\mathcal{A},\Omega,T,Z,R,\gamma,b_0)$$
이고, 상태가 더는 보이지 않으므로 MDP에 구성 요소 셋을 더한다: **관측 공간** $\Omega$, 행동 $a$가 상태 $s'$로 이끌었을 때 $o$를 관측할 확률을 주는 **관측 모델** $Z(o\mid s',a)$, 그리고 **초기 belief** $b_0$. belief $b(s)$는 지금까지의 모든 행동과 관측이 주어졌을 때 상태 $s$의 사후 확률이다. $a$를 하고 $o$를 관측하면 베이즈 규칙이 그것을 갱신한다:
$$b'(s')=\eta\,Z(o\mid s',a)\sum_{s\in\mathcal{S}}T(s'\mid s,a)\,b(s)$$
합은 옛 belief를 동역학에 통과시키는 **예측**(prediction)이고, 인자 $Z$는 각 상태를 그것이 $o$를 얼마나 잘 설명하는지로 가중하는 **보정**(correction)이며, $\eta$는 $b'$의 합이 1이 되게 하는 정규화 상수다. 이것은 [[04-robotics/state-estimation-slam|3. 상태 추정 §4]]의 베이즈 필터에 고른 행동을 붙인 것이다. belief가 이력 전체를 요약하므로 POMDP는 belief를 상태로 삼는 MDP이고, 그 기대 보상은 $\rho(b,a)=\sum_s b(s)\,R(s,a)$다. **반례:** 가장 최근의 관측 하나만으로는 마르코프 상태가 되지 않는다. 아래 예에서 같은 "열림" 판독이 belief $0.5$는 $0.8$로 옮기지만 belief $0.8$은 $0.94$로 옮긴다.

> [!example] 계산 예제 · Worked example
> 로봇이 잘 보이지 않는 문을 지나가야 한다. **숨은 상태:** 열림 또는 닫힘. **행동:** 다시 보기, 또는 지나가기. **전이:** 보기는 아무것도 바꾸지 않고, 지나가기는 로봇을 옮긴다. **관측:** "열림" 또는 "닫힘"이라는 센서 판독. **관측 모델:** 판독은 80% 확률로 맞다. **보상:** 통과하면 $+1$, 닫힌 문에 부딪히면 $-1$.
>
> belief $P(\text{열림})=0.5$에서 시작한다. "열림" 판독 한 번이면 $0.8\cdot0.5/(0.8\cdot0.5+0.2\cdot0.5)=0.8$, 두 번이면 $0.8\cdot0.8/(0.8\cdot0.8+0.2\cdot0.2)\approx0.94$다. 이것이 위의 갱신 식 그대로다. 보기는 상태를 바꾸지 않으므로 합은 그냥 $b(s')$이고, $Z$는 $0.8$ 또는 $0.2$이며, $\eta$는 첫 번째에 $1/0.5=2$, 두 번째에 $1/0.68=1.47$이다. belief 0.8에서 지나가면 기대 보상은 $\rho=0.8\cdot(+1)+0.2\cdot(-1)=0.6$, 0.94에서는 $0.88$이다. 한 번 더 볼 가치가 그 시간만큼 있는지가 바로 POMDP 계획기가 답하는 질문이고, 그 질문은 실제 문이 아니라 belief에 대해 던져진다.

정확한 belief-space 계획은 대개 계산 불가능해서 논문들은
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

성공률, 충돌률, 경로/궤적 비용, 계획·실행 시간, 최적성 갭(상대 초과 비용 $(C-C^*)/C^*$, 그래서 최적 10 m에 대한 11 m 경로는 10% 갭이다), 제약 위반, replanning 빈도,
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

### 과제 · Problem set

Tier B. 첫 패스. [[02-foundations/lab-plants|0.6]]의 **P2**를 패널까지. 노드 둘짜리 그래프. 시뮬레이터 없음.

1. **그리기.** 위의 그림: $q_\mathrm{start}=\theta=(0^\circ,0^\circ)$(말단 $(2,0)$)와 $q_\mathrm{goal}=$ 고정 자세(말단 $(1,1)$, 패널). $\mathcal{C}$의 간선 하나. $\mathcal{C}_\mathrm{free}$를 표시.
2. **유도.** 직선 보간 $\theta(s)=(0^\circ,90^\circ s)$. 말단 $x(s)=1+\cos(90^\circ s)$. 패널이 벽 $x=1$이면 언제 처음 닿는가? 이 두 노드에서 A*가 반환하는 것은?
3. **해석.** 이 탐색이 패널 접촉력에 대해 약속할 수 없는 것은?

> [!note]- 그리는 법 · How to draw it
> - 왼쪽 칸, 작업 영역: 원점의 베이스, 그 둘레 반지름 $2$ m의 도달 원판, $x=1$에 수직선으로 그린 패널과 그 너머의 빗금, 그리고 그 선 위의 과제 점 $p^\star=(1,1)$ m.
> - 팔은 두 번: 한 번은 $+x$ 방향으로 곧게 펴서 말단이 $(2,0)$에, 한 번은 고정 자세로 엘보가 $(1,0)$, 말단이 패널 위에. 컨피규레이션 둘이 그림 하나에 있고, 아직 그 어느 것도 계획이 아니다.
> - 오른쪽 칸, 컨피규레이션 공간: 각각 $-180°$에서 $180°$까지인 $\theta_1$, $\theta_2$ 축과, 마주 보는 변이 서로 붙어 있다는 메모. $\mathcal{C}$는 토러스 $T^2$이고, $179°$와 $-179°$를 멀다고 보는 플래너는 공간을 잘못 고른 것이다(§2).
> - 점 둘로 찍은 $q_\mathrm{start}$와 $q_\mathrm{goal}$, 그리고 둘을 잇는 직선 구간, 곧 그래프의 유일한 간선.
> - 말단만 보는 검사가 금지하는 영역 $\cos\theta_1+\cos(\theta_1+\theta_2)<1$의 음영과, 나머지에 붙인 $\mathcal{C}_\mathrm{free}$라는 이름.
> - 그 구간에서 경계 위에 놓이는 점 하나. 자유 공간이 아니라 접촉으로 표시한다.
> - 오른쪽 구간에서 왼쪽에서 말단이 그리는 곡선으로 가는 화살표 하나와 순기구학 $f$라는 이름. 두 칸은 한 대상의 두 시점이 아니다. 오른쪽은 컨피규레이션의 집합, 왼쪽은 위치의 집합이고, 둘을 잇는 것은 그 화살표뿐이다.

> [!tip]- 정답 · Solutions
> 1. $\mathcal{C}=T^2$의 점 둘, 선분 하나. 목표는 접촉 집합 위.
> 2. $x(s)=1$은 $s=1$뿐이라 열린 선분은 자유. A*는 그 간선 하나를 가능 경로로 반환한다.
> 3. 경로는 힘이 없는 기하. 탐색은 $k_w$, $\mu$, $F_n$을 모른다 — 접촉이지 $\mathcal{C}_\mathrm{free}$가 아니다(스스로 점검 1).

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
- D. Fox, W. Burgard, S. Thrun, "The dynamic window approach to collision avoidance," *IEEE Robotics & Automation Magazine* 4(1), 23–33, 1997.
- E. Rimon, D. E. Koditschek, "Exact robot navigation using artificial potential functions," *IEEE Transactions on Robotics and Automation* 8(5), 501–518, 1992.
- S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005 — 9장(점유 격자 로그 승산 갱신).
