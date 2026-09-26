---
title: 4. Planning & Decision-Making
tags: [robotics, planning, decision-making]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

*Group C, and the only page in it. Stands on the [[04-robotics/modern-robotics/index|Modern Robotics chapters]] and the optimization and RL pages; [[04-robotics/mpc|7. MPC]], later in the track, develops §6.
Choosing an executable future; group I specialises this for unstructured environments.*

Planning asks how a robot should choose a feasible sequence of future states and actions to reach a goal. The difficulty is not merely finding a short path: robot geometry, dynamics, contact, uncertainty, computation time, and changing observations constrain what can actually be executed.

> [!info] Depth target
> Distinguish search, motion planning, trajectory optimization, task planning, policy learning, and control; read feasibility and optimality claims; and identify whether a generated trajectory is collision-free, dynamically feasible, and evaluated in closed loop.

> [!note] Prerequisites
> [[02-foundations/lab-plants|0.6 Lab Plants]] (plant P2; *plant* is control's word for the system being controlled) · [[02-foundations/optimization|Optimization]] · [[02-foundations/rl-basics|RL Basics]] · [[04-robotics/modern-robotics/ch02-configuration-space|Configuration Space]] · [[04-robotics/modern-robotics/ch09-trajectory-generation|Trajectory Generation]] (time scaling) · [[04-robotics/state-estimation-slam|3. State Estimation]] (the Bayes filter of its §4, used in §7). [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 Motion Planning]] is read inside this page's sessions, after the Worked case.

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this page is the map of the motion-and-task-planning layer, and in *"install that panel on the frame"* it serves two steps — *decompose the job*, which is task planning (§7), and *move the component*, a free and cheap route for the tool to the panel (§1–§6) — with its chip in the planning layer of the [[physical-ai-map|Physical AI Map]], on the dissertation path. A planner's "optimal" and "complete" are claims about a metric and a discretisation it chose: from the Worked case's start P2 reaches the panel point on two inverse-kinematics (IK) branches, one $\sqrt2$ times the other in joint-space length yet exactly tied under the max-norm, and only one of them points the tool at the face, while a $10$ cm grid can report "no path" through a $5$ cm gap (§5). [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]], read inside this page's sessions, works the collision test, a roadmap and three completeness notions on the same two goals; [[04-robotics/mpc|7. MPC]] develops §6 and asks in its §1 when that program is convex; [[04-robotics/capstone-panel-contact|26. Capstone §2]] plans around a panel inflated by the uncertainty of its estimated position; and whether a learned vision-language-action (VLA) policy of [[03-deep-learning/vla/index|deep learning 4]] keeps any of these guarantees is §8's question — block 2 of the dissertation path, robotics sessions 52–60, with §8 looking ahead to block 4 ([[07-research-program/index|7. Research Program §8]]). After it you can place a planning paper in its family, say which guarantee it keeps and which a learned component removes, and check that its "collision-free" and "optimal" name their collision model and their metric.

> [!note] First pass · 처음이라면
> Two sessions of 60–90 minutes, then [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]] inside this page. **Session 1:** the Running object and the picture, §1, and §2 up to its map summary — the five spaces, the configuration space, the path-planning problem and the disc-robot example; leave §2's Deeper note, and end by sorting the disc robot's four centres into $\mathcal{C}_{\text{obs}}$ and $\mathcal{C}_{\text{free}}$ with the figure covered. **Session 2:** §3 and §4, then the Worked case by hand with the page covered — both branches' tip paths and $d(s)$, their costs under joint-space length and under the max-norm, and what A\* returns — and end with self-check 2. Then MR ch.10's three sessions, which join the same $q_A$ and $q_B$ to each other. The Working pass comes back for §5 with §5.5.1 and §5.5.5, then §6–§7, then §8–§9, and closes with the self-check and the problem set, whose arm is stopped halfway along branch A. The Deeper notes — the map storage of §2, the Dubins, lattice and kinodynamic planners of §5.5 and the local planners of §6 — are for when a navigation or vehicle paper needs them.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's planar two-link arm: links $L_1=L_2=1$ m, base at the origin, $\theta_1$ measured from the $+x$ axis and $\theta_2$ the elbow angle relative to link 1, so the elbow is at $(\cos\theta_1,\sin\theta_1)$ and the tip one more metre along the absolute angle $\theta_1+\theta_2$. Its configuration space is the torus $T^2$, both angles wrapping at $\pm180°$ ([[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2]]).

**The panel** that [[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2]] freezes and [[04-robotics/modern-robotics/ch09-trajectory-generation|ch.9]], [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] and [[04-robotics/capstone-panel-contact|26]] reuse, 26 with the face moved out to $x=1.10$ m on the drawing ($1.116$ estimated, $1.120$ true) and mounted compliantly at $400$ N/m: the rigid half-plane $x\ge1$ m, whose face, the line $x=1$, holds the task point $p^\star=(1,1)$ m. The collision test checks the whole arm against it, and only penetration collides:

$$d(\theta)=\max\bigl(\cos\theta_1,\ \cos\theta_1+\cos(\theta_1+\theta_2)\bigr)-1,\qquad \mathcal{C}_{\text{free}}=\{\theta:\ d(\theta)\le0\}$$

because a link's $x$-coordinate is largest at one of its two ends, so the elbow and the tip are the only points to test (MR ch.10, its Step 1), and contact, $d=0$, counts as free because the task ends in contact. Here $d$ is a penetration depth, positive inside the panel. The C-obstacle it defines is the lens $\cos\theta_1+\cos(\theta_1+\theta_2)>1$, $18.478\,\%$ of the torus.

**The query and the metric.** The arm starts parked straight up, $q_\mathrm{start}=(90°,0°)$, with its tip at $(0,2)$ and $d=-1$, and must put the tip on $p^\star$ by either inverse-kinematics branch, $q_A=(0°,90°)$ or $q_B=(90°,-90°)$ — the two contact configurations that MR ch.10 joins to each other. Edges are straight segments in $\mathcal{C}$, costed by their joint-space length in radians unless a step says otherwise.

*Scope: this page teaches the objects and the guarantees — the five words of §1, the spaces and the map and cost representations of §2, the four strengths of completeness in §5, the constraints that make a path undrivable in §5.5, and the shape of the trajectory-optimization program in §6 — plus enough of each method family to place a paper in it. It does not teach any single algorithm to implementation depth. A\*'s proofs and code are in [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms §6]]; the sampling planners are surveyed here and worked by hand on P2 in [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]] — one step of an RRT (rapidly-exploring random tree) and a five-node roadmap — but no page implements one in code; receding-horizon control is [[04-robotics/mpc|7. MPC]], policy learning is [[02-foundations/rl-basics|RL Basics]], and one navigation stack's concrete parameters are [[04-robotics/ros2/navigation-nav2|25.9 Nav2]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 330" style="max-width:100%;height:auto" role="img" aria-label="Left, the workspace: P2's base at the origin, the panel face x = 1 hatched on the x ≥ 1 side, the arm at the start (straight up, tip at (0, 2)), at goal A with link 2 flush on the face and at goal B touching only at the tip, the tip's quarter circle about (0, 1) that both edges trace, its midpoint (0.707, 1.707) at d = −0.293, and the elbow's arc on edge A. Right, the torus chart of (θ1, θ2) with the C-obstacle lens shaded, the start (90°, 0°), the straight edges to A (0°, 90°) and to B (90°, −90°) running outside the lens, and A and B ringed on its boundary. Two arrows f carry both edges' midpoints to the same workspace point.">
  <defs><marker id="aPDM" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="146" y="53.8" width="42" height="243.6" fill="currentColor" fill-opacity="0.07"/>
  <path d="M146 55.8 l 12 12 M146 67.8 l 12 12 M146 79.8 l 12 12 M146 91.8 l 12 12 M146 103.8 l 12 12 M146 115.8 l 12 12 M146 127.8 l 12 12 M146 139.8 l 12 12 M146 151.8 l 12 12 M146 163.8 l 12 12 M146 175.8 l 12 12 M146 187.8 l 12 12 M146 199.8 l 12 12 M146 211.8 l 12 12 M146 223.8 l 12 12 M146 235.8 l 12 12 M146 247.8 l 12 12 M146 259.8 l 12 12 M146 271.8 l 12 12 M146 283.8 l 12 12" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="146" y1="53.8" x2="146" y2="297.4" stroke="currentColor" stroke-width="1.3"/>
  <path d="M62 184 A84 84 0 0 1 146 268" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity="0.75"/>
  <path d="M62 100 A84 84 0 0 1 146 184" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#aPDM)"/>
  <g stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <polyline points="62,268 62,184 62,100" stroke-width="4" stroke-opacity="0.28"/>
    <polyline points="62,268 146,268 146,184" stroke-width="2.6"/>
    <polyline points="62,268 62,184 146,184" stroke-width="2.6" stroke-dasharray="7 3"/>
  </g>
  <circle cx="62" cy="268" r="4.5" fill="currentColor"/>
  <circle cx="62" cy="184" r="3.2" fill="currentColor"/>
  <circle cx="146" cy="268" r="3.2" fill="currentColor"/>
  <circle cx="62" cy="100" r="3.2" fill="currentColor" fill-opacity="0.45"/>
  <circle cx="146" cy="184" r="5.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="121.4" cy="124.6" r="2.6" fill="currentColor"/>
  <path d="M368 125 L368.5 120.1 L369 118.4 L369.5 117.2 L370 116.2 L370.5 115.5 L371 114.8 L371.5 114.2 L372 113.7 L372.5 113.3 L373 112.9 L373.5 112.5 L374 112.2 L374.5 111.9 L375 111.6 L375.5 111.4 L376 111.2 L376.5 111 L377 110.9 L377.5 110.7 L378 110.6 L378.5 110.5 L379 110.4 L379.5 110.3 L380 110.2 L380.5 110.1 L381 110.1 L381.5 110 L382 110 L382.5 110 L383 110 L383.5 110 L384 110 L384.5 110 L385 110.1 L385.5 110.1 L386 110.2 L386.5 110.2 L387 110.3 L387.5 110.4 L388 110.5 L388.5 110.6 L389 110.7 L389.5 110.8 L390 110.9 L390.5 111 L391 111.1 L391.5 111.3 L392 111.4 L392.5 111.6 L393 111.8 L393.5 111.9 L394 112.1 L394.5 112.3 L395 112.5 L395.5 112.7 L396 112.9 L396.5 113.1 L397 113.4 L397.5 113.6 L398 113.8 L398.5 114.1 L399 114.4 L399.5 114.6 L400 114.9 L400.5 115.2 L401 115.5 L401.5 115.8 L402 116.1 L402.5 116.4 L403 116.7 L403.5 117.1 L404 117.4 L404.5 117.8 L405 118.1 L405.5 118.5 L406 118.9 L406.5 119.2 L407 119.6 L407.5 120 L408 120.4 L408.5 120.9 L409 121.3 L409.5 121.7 L410 122.2 L410.5 122.6 L411 123.1 L411.5 123.5 L412 124 L412.5 124.5 L413 125 L413.5 125.5 L414 126 L414.5 126.5 L415 127.1 L415.5 127.6 L416 128.2 L416.5 128.7 L417 129.3 L417.5 129.9 L418 130.4 L418.5 131 L419 131.6 L419.5 132.2 L420 132.9 L420.5 133.5 L421 134.1 L421.5 134.8 L422 135.4 L422.5 136.1 L423 136.7 L423.5 137.4 L424 138.1 L424.5 138.8 L425 139.5 L425.5 140.2 L426 140.9 L426.5 141.6 L427 142.4 L427.5 143.1 L428 143.8 L428.5 144.6 L429 145.4 L429.5 146.1 L430 146.9 L430.5 147.7 L431 148.5 L431.5 149.3 L432 150.1 L432.5 150.9 L433 151.8 L433.5 152.6 L434 153.4 L434.5 154.3 L435 155.1 L435.5 156 L436 156.9 L436.5 157.8 L437 158.7 L437.5 159.6 L438 160.5 L438.5 161.4 L439 162.3 L439.5 163.2 L440 164.2 L440.5 165.1 L441 166.1 L441.5 167 L442 168 L442.5 169 L443 170 L443.5 171 L444 172 L444.5 173 L445 174.1 L445.5 175.1 L446 176.2 L446.5 177.3 L447 178.4 L447.5 179.5 L448 180.6 L448.5 181.7 L449 182.9 L449.5 184 L450 185.2 L450.5 186.4 L451 187.6 L451.5 188.9 L452 190.2 L452.5 191.5 L453 192.9 L453.5 194.3 L454 195.7 L454.5 197.2 L455 198.8 L455.5 200.5 L456 202.2 L456.5 204.2 L457 206.4 L457.5 209.1 L458 215 L458 215 L457.5 219.9 L457 221.6 L456.5 222.8 L456 223.8 L455.5 224.5 L455 225.2 L454.5 225.8 L454 226.3 L453.5 226.7 L453 227.1 L452.5 227.5 L452 227.8 L451.5 228.1 L451 228.4 L450.5 228.6 L450 228.8 L449.5 229 L449 229.1 L448.5 229.3 L448 229.4 L447.5 229.5 L447 229.6 L446.5 229.7 L446 229.8 L445.5 229.9 L445 229.9 L444.5 230 L444 230 L443.5 230 L443 230 L442.5 230 L442 230 L441.5 230 L441 229.9 L440.5 229.9 L440 229.8 L439.5 229.8 L439 229.7 L438.5 229.6 L438 229.5 L437.5 229.4 L437 229.3 L436.5 229.2 L436 229.1 L435.5 229 L435 228.9 L434.5 228.7 L434 228.6 L433.5 228.4 L433 228.2 L432.5 228.1 L432 227.9 L431.5 227.7 L431 227.5 L430.5 227.3 L430 227.1 L429.5 226.9 L429 226.6 L428.5 226.4 L428 226.2 L427.5 225.9 L427 225.6 L426.5 225.4 L426 225.1 L425.5 224.8 L425 224.5 L424.5 224.2 L424 223.9 L423.5 223.6 L423 223.3 L422.5 222.9 L422 222.6 L421.5 222.2 L421 221.9 L420.5 221.5 L420 221.1 L419.5 220.8 L419 220.4 L418.5 220 L418 219.6 L417.5 219.1 L417 218.7 L416.5 218.3 L416 217.8 L415.5 217.4 L415 216.9 L414.5 216.5 L414 216 L413.5 215.5 L413 215 L412.5 214.5 L412 214 L411.5 213.5 L411 212.9 L410.5 212.4 L410 211.8 L409.5 211.3 L409 210.7 L408.5 210.1 L408 209.6 L407.5 209 L407 208.4 L406.5 207.8 L406 207.1 L405.5 206.5 L405 205.9 L404.5 205.2 L404 204.6 L403.5 203.9 L403 203.3 L402.5 202.6 L402 201.9 L401.5 201.2 L401 200.5 L400.5 199.8 L400 199.1 L399.5 198.4 L399 197.6 L398.5 196.9 L398 196.2 L397.5 195.4 L397 194.6 L396.5 193.9 L396 193.1 L395.5 192.3 L395 191.5 L394.5 190.7 L394 189.9 L393.5 189.1 L393 188.2 L392.5 187.4 L392 186.6 L391.5 185.7 L391 184.9 L390.5 184 L390 183.1 L389.5 182.2 L389 181.3 L388.5 180.4 L388 179.5 L387.5 178.6 L387 177.7 L386.5 176.8 L386 175.8 L385.5 174.9 L385 173.9 L384.5 173 L384 172 L383.5 171 L383 170 L382.5 169 L382 168 L381.5 167 L381 165.9 L380.5 164.9 L380 163.8 L379.5 162.7 L379 161.6 L378.5 160.5 L378 159.4 L377.5 158.3 L377 157.1 L376.5 156 L376 154.8 L375.5 153.6 L375 152.4 L374.5 151.1 L374 149.8 L373.5 148.5 L373 147.1 L372.5 145.7 L372 144.3 L371.5 142.8 L371 141.2 L370.5 139.5 L370 137.8 L369.5 135.8 L369 133.6 L368.5 130.9 L368 125 Z" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1" stroke-opacity="0.75"/>
  <rect x="323" y="80" width="180" height="180" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <path d="M319 226 L323 220 L327 226 M499 226 L503 220 L507 226 M457 76 L463 80 L457 84 M463 76 L469 80 L463 84 M457 256 L463 260 L457 264 M463 256 L469 260 L463 264" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6"><line x1="323" y1="260" x2="323" y2="264"/><line x1="319" y1="260" x2="323" y2="260"/><line x1="368" y1="260" x2="368" y2="264"/><line x1="319" y1="215" x2="323" y2="215"/><line x1="413" y1="260" x2="413" y2="264"/><line x1="319" y1="170" x2="323" y2="170"/><line x1="458" y1="260" x2="458" y2="264"/><line x1="319" y1="125" x2="323" y2="125"/><line x1="503" y1="260" x2="503" y2="264"/><line x1="319" y1="80" x2="323" y2="80"/></g>
  <line x1="458" y1="170" x2="413" y2="125" stroke="currentColor" stroke-width="2.2"/>
  <line x1="458" y1="170" x2="458" y2="215" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <circle cx="458" cy="170" r="4" fill="currentColor"/>
  <circle cx="413" cy="125" r="3" fill="currentColor"/>
  <circle cx="413" cy="125" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="458" cy="215" r="3" fill="currentColor"/>
  <circle cx="458" cy="215" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="435.5" cy="147.5" r="2.4" fill="currentColor"/>
  <circle cx="458" cy="192.5" r="2.4" fill="currentColor"/>
  <path d="M431.5 146.5 C 315.5 125.5 271.4 100.6 128.4 123.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" marker-end="url(#aPDM)"/>
  <path d="M454 192.5 C 298 214.5 296.4 164.6 127.4 127.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" stroke-dasharray="4 2" marker-end="url(#aPDM)"/>
  <g fill="currentColor">
    <text x="10" y="20" font-size="12">workspace (m)</text>
    <text x="323" y="20" font-size="12">configuration space C = T² (deg)</text>
    <text x="150" y="47.8" font-size="11">panel x ≥ 1</text>
    <text x="54" y="272" font-size="11" text-anchor="end">base</text>
    <text x="54" y="104" font-size="11" text-anchor="end" opacity="0.85">start (0, 2)</text>
    <text x="139" y="261" font-size="12" text-anchor="end" font-weight="bold">A</text>
    <text x="54" y="188" font-size="12" text-anchor="end" font-weight="bold">B</text>
    <text x="138" y="175" font-size="11" text-anchor="end">p* = (1, 1)</text>
    <text x="117.4" y="142.6" font-size="10" text-anchor="end">d = −0.293</text>
    <text x="78.8" y="78.2" font-size="10" opacity="0.9">tip path,</text>
    <text x="78.8" y="90.2" font-size="10" opacity="0.9">both edges</text>
    <text x="70.4" y="224.3" font-size="10" opacity="0.85">elbow on</text>
    <text x="70.4" y="236.3" font-size="10" opacity="0.85">edge A</text>
    <text x="466" y="174" font-size="11">start</text>
    <text x="466" y="187" font-size="10">(90°, 0°)</text>
    <text x="421" y="117" font-size="11">A (0°, 90°)</text>
    <text x="467" y="219" font-size="11" font-weight="bold">B</text>
    <text x="467" y="232" font-size="10">(90°, −90°)</text>
    <text x="411" y="166" font-size="11" text-anchor="middle">C-obstacle</text>
    <text x="411" y="179" font-size="11" text-anchor="middle">d > 0</text>
    <text x="323" y="275" font-size="10" text-anchor="middle">−180°</text>
    <text x="317" y="264" font-size="10" text-anchor="end">−180°</text>
    <text x="413" y="275" font-size="10" text-anchor="middle">0°</text>
    <text x="317" y="174" font-size="10" text-anchor="end">0°</text>
    <text x="503" y="275" font-size="10" text-anchor="middle">180°</text>
    <text x="317" y="84" font-size="10" text-anchor="end">180°</text>
    <text x="458" y="275" font-size="12" text-anchor="middle">θ<tspan dy="3" font-size="10">1</tspan></text>
    <text x="305" y="104" font-size="12" text-anchor="middle">θ<tspan dy="3" font-size="10">2</tspan></text>
    <text x="323" y="292" font-size="10" opacity="0.85">opposite edges identified</text>
    <text x="323" y="306" font-size="10" opacity="0.85">ringed: contact, d = 0, free</text>
    <text x="246" y="111" font-size="12" text-anchor="middle" font-style="italic">f</text>
  </g>
</svg>

P2 against the panel $x\ge1$, with branch A drawn solid and branch B dashed in both panels. Left, the workspace: from the start, straight up with its tip at $(0,2)$, the arm reaches $p^\star=(1,1)$ at $q_A=(0°,90°)$, with link 2 flush on the face, or at $q_B=(90°,-90°)$, touching only at the tip, and both straight edges carry the tip along one quarter circle about $(0,1)$, $0.293$ m clear of the face at its midpoint $(0.707,1.707)$. Right, the torus $\mathcal{C}=T^2$ with the C-obstacle lens shaded: the edges are two different segments that stay outside the lens and touch it only at their goals — contact, which counts as free — and they cost $\pi/\sqrt2=2.2214$ rad to $q_A$ and $\pi/2=1.5708$ rad to $q_B$, while the two arrows $f$, the forward kinematics, carry both midpoints to the one workspace point.

### 1. Plan, path, trajectory, policy, controller

The literature uses five words for what a robot will do almost interchangeably, and a claim made about one is often read as a claim about another. The split that matters most is the plan against the policy: a plan is one answer for one start, and a policy is an answer for every state it may meet.

| Term | Meaning |
|---|---|
| Plan | Proposed future sequence of decisions or actions |
| Path | Geometric curve without timing |
| Trajectory | Time-indexed state, velocity, and often input |
| Policy | Rule mapping available information to an action |
| Controller | Feedback system that tracks a reference or regulates behavior |

A planner may produce a path that a trajectory generator times ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]] — time scaling, via points, time-optimal scaling) and a controller tracks. When the plan lives in task space but the robot is commanded in joint space, [[04-robotics/modern-robotics/ch06-inverse-kinematics|inverse kinematics (MR ch.6)]] sits between them, and its multimodality is a planning problem in miniature. In learned systems, a policy can collapse these boundaries, but the physical requirements do not disappear.

**The five, as mathematical objects.** Let $\mathcal{C}$ be the configuration space, the set of all configurations $q$, the lists of numbers that place every point of the robot (for P2, the joint-angle pairs $(\theta_1,\theta_2)$); $\mathcal{X}$ the state space, a configuration together with its velocity, $x=(q,\dot q)$; and $\mathcal{U}$ the input space, the set of commands the actuators accept. §2 gives each its full definition.

- A **path** is a continuous map from a normalised parameter $s$ to configurations, with both ends fixed. The parameter is not time, so a path says only *where*.
$$\sigma:[0,1]\to\mathcal{C},\qquad \sigma(0)=q_{\text{start}},\quad \sigma(1)=q_{\text{goal}}$$
- A **trajectory** adds timing: the state, and usually the input, as functions of time over a duration $T$. Every trajectory traces a path, but one path has infinitely many trajectories, since any increasing time scaling $s(t)$ with $s(0)=0$ and $s(T)=1$ gives another ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]]).
$$x:[0,T]\to\mathcal{X},\qquad u:[0,T]\to\mathcal{U}$$
- A **plan** is a finite sequence of decisions $(a_0,\dots,a_{K-1})$, whether symbolic actions, waypoints or inputs, computed *before* execution for one start state.
- A **policy** is a rule evaluated *during* execution. It maps whatever information $I_t$ is available (the state, an observation history, a belief) to an action, $a_t=\pi(I_t)$, or to a distribution $\pi(a_t\mid I_t)$ ([[02-foundations/rl-basics|RL Basics §1]]).
- A **controller** is a feedback law, usually fast, that computes the actuator command from the measured state and a reference, $u_t=\kappa(x_t,\,x^{\text{ref}}_t)$.

Example: the straight segment from $(0,0)$ to $(1,0)$ m is one path. Driving it at a constant 0.5 m/s is a trajectory with $T=2$ s, and driving it at 1 m/s is a different trajectory, with $T=1$ s, on the same path. **Non-example:** a list of waypoints without times is a path or a plan, not a trajectory, so it cannot be checked against velocity or acceleration limits until something times it.

### 2. Spaces and constraints

*In one sentence:* before a planner can search, the problem has to be written in the right space, the robot's joint angles rather than the room, and the map has to be stored in a form the planner can read, with its costs and its unknown cells marked.

*If you need only one thing from this section:* a C-obstacle is a set of configurations, not a region of the room; in the disc-robot example below, the empty point $(0.6,1.5)$ m lies inside $\mathcal{C}_{\text{obs}}$ because a robot centred there would overlap the square.

#### The five spaces, and the configuration space defined

- **Workspace:** physical positions occupied by the robot and obstacles.
- **Configuration space:** robot configurations; obstacles become forbidden regions.
- **State space:** configuration plus variables such as velocity.
- **Action/input space:** commands available to the system.
- **Task space:** variables directly tied to the task, such as end-effector pose.

Collision-free in workspace does not imply joint, torque, velocity, stability, or contact feasibility.

**Configuration space, defined.** A **configuration** $q$ is a specification of the position of every point of the robot. Two conditions make one: it is **complete**, so no body point is left undetermined, and it is **minimal**, so no shorter list of numbers does the same job. The **configuration space** $\mathcal{C}$ is the set of all configurations, and minimality is what makes its dimension the number of degrees of freedom:

$$\mathcal{C}=\{\,q:q\ \text{locates every point of the robot}\,\},\qquad \dim\mathcal{C}=\text{dof}$$

The set matters more than the count, because $\mathcal{C}$ is usually not a box. A planar 2R arm's is the torus $T^2$, not the rectangle $[0,2\pi)^2$, since each joint angle wraps — so a planner that treats $359°$ and $1°$ as far apart is using the wrong space. **Non-example:** the tool's pose is *not* a configuration whenever more than one joint vector gives it — a redundant arm's pose, or P2's tip position $(1,1)$, which two configurations reach (the Worked case, step 1) — because the body points are then not determined. That is task space, the last item in the list above.

$\mathcal{C}$ splits into the **C-obstacle** $\mathcal{C}_{\text{obs}}$ and the **free space** $\mathcal{C}_{\text{free}}=\mathcal{C}\setminus\mathcal{C}_{\text{obs}}$. Both are defined, derived on plant **P2**, and given their example and non-example in [[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2 §2]]; this page uses them rather than restating them. For the panel of the Running object the C-obstacle is the lens $\cos\theta_1+\cos(\theta_1+\theta_2)>1$, and the collision test that decides membership — the only way a planner ever learns about the world — is defined in [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 §2]]. Two consequences of that definition are what the rest of this page rests on: a C-obstacle is a set of *configurations* and never a region of the workspace, and the construction shrinks a robot of some shape to a *point* moving in $\mathcal{C}_{\text{free}}$, which is the form every planner below is written for.

The **path-planning problem** is then: given $q_{\text{start}},q_{\text{goal}}\in\mathcal{C}_{\text{free}}$, find a path $\sigma$ (§1) with $\sigma(s)\in\mathcal{C}_{\text{free}}$ for every $s\in[0,1]$, or report that none exists. [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 §1]] states it as a definition, with P2's query $A\to B$ as its example and the straight elbow flip, which leaves $\mathcal{C}_{\text{free}}$ at its midpoint, as its non-example. The **state space** $\mathcal{X}$ adds velocities, $x=(q,\dot q)$, so an $n$-dof robot has a $2n$-dimensional state. The **input space** $\mathcal{U}$ is the set of admissible commands, for example $|u_i|\le u_{\max}$ for each actuator. Workspace and task space are sets of physical positions or poses, while $\mathcal{C}$ is a set of robot configurations, which is why the figure below needs two panels.

> [!example] Worked example · 계산 예제
> MR ch.2 derives the C-obstacle of an *arm*, where it is a curved lens on a torus. Here is the other case, the one the grid inflation below depends on. A disc robot of radius 0.5 m that translates without rotating has configuration $q=(x,y)$, its centre, so $\mathcal{C}=\mathbb{R}^2$. With a square obstacle $[1,2]\times[1,2]$ m, $q\in\mathcal{C}_{\text{obs}}$ exactly when the centre is closer than 0.5 m to the square. $q=(0.6,1.5)$ is 0.4 m from it, so it is in $\mathcal{C}_{\text{obs}}$ even though the workspace *point* $(0.6,1.5)$ is empty. $q=(0.4,1.5)$ is 0.6 m away and free.
>
> **Non-example:** the C-obstacle is not the square grown into the box $[0.5,2.5]^2$. Its corners are rounded, because it is the square's Minkowski sum with the disc. So $q=(0.6,0.6)$, inside that box, is 0.566 m from the corner $(1,1)$ and free, while $(0.7,0.7)$, at 0.424 m, is not. This is the inflation of the list below, and it is exact only because the robot is a disc.

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="Left, the workspace: the square obstacle [1, 2]² m and a disc robot of radius 0.5 m centred at (0.6, 1.5), which overlaps the square, and at (0.6, 0.6), which clears its corner by 0.066 m. Right, the configuration space of the centre: the C-obstacle is the square grown by 0.5 m with quarter-circle corners, not the dashed box [0.5, 2.5]²; the centres (0.6, 1.5) and (0.7, 0.7) are inside it, 0.40 and 0.424 m from the square, and (0.4, 1.5) and (0.6, 0.6) are free, 0.60 and 0.566 m from it.">
  <g stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55"><line x1="12" y1="282" x2="228.6" y2="282"/><line x1="12" y1="282" x2="12" y2="76.8"/><line x1="27.2" y1="282" x2="27.2" y2="286"/><line x1="8" y1="282" x2="12" y2="282"/><line x1="103.2" y1="282" x2="103.2" y2="286"/><line x1="8" y1="206" x2="12" y2="206"/><line x1="179.2" y1="282" x2="179.2" y2="286"/><line x1="8" y1="130" x2="12" y2="130"/></g>
  <g stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55"><line x1="250" y1="279" x2="545" y2="279"/><line x1="250" y1="279" x2="250" y2="24"/><line x1="280" y1="279" x2="280" y2="283"/><line x1="380" y1="279" x2="380" y2="283"/><line x1="246" y1="194" x2="250" y2="194"/><line x1="480" y1="279" x2="480" y2="283"/><line x1="246" y1="94" x2="250" y2="94"/></g>
  <rect x="103.2" y="130" width="76" height="76" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="72.8" cy="168" r="38" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="72.8" cy="168" r="2.4" fill="currentColor"/>
  <circle cx="72.8" cy="236.4" r="38" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 3"/>
  <circle cx="72.8" cy="236.4" r="2.4" fill="currentColor"/>
  <path d="M103.2 145.2 A38 38 0 0 1 103.2 190.8 Z" fill="currentColor" fill-opacity="0.6"/>
  <path d="M380 244 L480 244 A50 50 0 0 0 530 194 L530 94 A50 50 0 0 0 480 44 L380 44 A50 50 0 0 0 330 94 L330 194 A50 50 0 0 0 380 244 Z" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.2"/>
  <rect x="330" y="44" width="200" height="200" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <rect x="380" y="94" width="100" height="100" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55"/>
  <line x1="380" y1="194" x2="340" y2="234" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.75"/>
  <circle cx="380" cy="194" r="1.8" fill="currentColor"/>
  <circle cx="340" cy="144" r="3" fill="currentColor"/>
  <circle cx="320" cy="144" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="340" cy="234" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="350" cy="224" r="3" fill="currentColor"/>
  <g fill="currentColor">
    <text x="12" y="16" font-size="12">workspace (m)</text>
    <text x="250" y="16" font-size="12">configuration space: the centre (m)</text>
    <text x="27.2" y="297" font-size="10" text-anchor="middle">0</text>
    <text x="6" y="286" font-size="10" text-anchor="end">0</text>
    <text x="103.2" y="297" font-size="10" text-anchor="middle">1</text>
    <text x="6" y="210" font-size="10" text-anchor="end">1</text>
    <text x="179.2" y="297" font-size="10" text-anchor="middle">2</text>
    <text x="6" y="134" font-size="10" text-anchor="end">2</text>
    <text x="280" y="294" font-size="10" text-anchor="middle">0</text>
    <text x="380" y="294" font-size="10" text-anchor="middle">1</text>
    <text x="244" y="198" font-size="10" text-anchor="end">1</text>
    <text x="480" y="294" font-size="10" text-anchor="middle">2</text>
    <text x="244" y="98" font-size="10" text-anchor="end">2</text>
    <text x="141.2" y="162.9" font-size="11" text-anchor="middle">obstacle</text>
    <text x="110.5" y="194.8" font-size="10">overlap</text>
    <text x="72.8" y="123.9" font-size="10" text-anchor="middle">robot, r = 0.5</text>
    <text x="72.8" y="183" font-size="10" text-anchor="middle">(0.6, 1.5)</text>
    <text x="72.8" y="251.4" font-size="10" text-anchor="middle">(0.6, 0.6)</text>
    <text x="112.2" y="221.6" font-size="10">0.066 clear</text>
    <text x="430" y="122" font-size="11" text-anchor="middle">C-obstacle</text>
    <text x="430" y="148" font-size="10" text-anchor="middle" opacity="0.8">square</text>
    <text x="530" y="259" font-size="10" text-anchor="end" opacity="0.9">box [0.5, 2.5]²</text>
    <text x="347" y="148" font-size="10">in 0.40</text>
    <text x="313" y="148" font-size="10" text-anchor="end">free 0.60</text>
    <text x="357" y="233" font-size="10">in 0.424</text>
    <text x="334" y="255" font-size="10" text-anchor="end">free 0.566</text>
  </g>
</svg>

The example drawn to scale. Left, the room: the disc robot centred at $(0.6,1.5)$ overlaps the square although its centre is empty floor, and centred at $(0.6,0.6)$ it clears the corner $(1,1)$ by $0.066$ m. Right, the same four centres as points of $\mathcal{C}$: the C-obstacle is the square grown by $0.5$ m with quarter-circle corners, not the dashed box, so $(0.6,1.5)$ and $(0.7,0.7)$, $0.40$ and $0.424$ m from the square, are inside it, and $(0.4,1.5)$ and $(0.6,0.6)$, $0.60$ and $0.566$ m from it, are free.

#### How the map is stored: grids, costs and frontiers

A robot that plans in a space it has only sensed stores that space as a grid, and a navigation paper assumes five facts about the grid:

- **Occupancy grid**: a grid of cells, each holding the probability that it is occupied, updated by adding each new reading's evidence in log-odds.
- **Unknown is not free**: a cell reads free, occupied or unknown, and treating the unknown as free is the beginner's error that exploration exists to correct.
- **Inflation**: growing every occupied cell by the robot's radius turns the grid into the C-obstacle of a disc robot — exactly, by the example above — and only approximately for any other footprint.
- **Costmap**: a grid whose cells carry a traversal cost instead of a yes or no, so a preference such as keeping clear of walls becomes geometry a planner can search.
- **Frontier**: a known-free cell next to an unknown one; driving to the nearest frontier until none is left is classical exploration.

The Deeper note writes each of them out — the log-odds update with OctoMap's numbers, the inflation cost and its three radii, the layered costmap, and how semantic navigation uses frontiers — for when a navigation paper needs them.

> [!note]- Deeper · 더 깊이
> Several pages of this wiki link here for occupancy and cost representations, so they are kept in this section rather than in a system paper's appendix.
>
> **Occupancy grid and log-odds.** The map is a grid of cells, each holding the probability that the cell is occupied. Updates are done in **log-odds**, $\ell=\log\frac{p}{1-p}$, which maps $p=0.5$ to $0$ and $p\to 0$ or $1$ to $\mp\infty$. Bayes' rule multiplies a cell's odds $p/(1-p)$ by each new reading's likelihood ratio, so after the log, accumulating evidence is an addition rather than a multiplication (OctoMap's $+0.85$ is $\log(0.7/0.3)$, a "hit" worth $p=0.7$). It also avoids the numerical trouble of probabilities pressed against 0 or 1. Note the direction of the remaining hazard: log-odds is *unbounded*, so a cell observed occupied a thousand times needs on the order of a thousand contrary observations to flip (about 2,100 with OctoMap's default +0.85/−0.4 log-odds increments) — which is why implementations add an explicit **clamping** range (proposed by Yguel et al. 2007 and adopted by OctoMap) so the map can still adapt when the world changes. A cell reads as *free*, *occupied*, or **unknown**, and the third is the one beginners drop: unknown is not free, and the difference is what exploration is about.
>
> **The update, written out.** Let $m_i=1$ mean "cell $i$ is occupied" and $p_0$ be the prior occupancy probability. Each reading $z_t$ adds its own evidence and the prior is subtracted once, so it is not counted again with every reading:
> $$\ell_t(i)=\ell_{t-1}(i)+\log\frac{p(m_i=1\mid z_t)}{1-p(m_i=1\mid z_t)}-\log\frac{p_0}{1-p_0},\qquad p=1-\frac{1}{1+e^{\ell}}$$
> The middle term is the **inverse sensor model**, the occupancy probability that this one reading alone implies, and the second formula converts log-odds back to a probability. With $p_0=0.5$ the prior term is $0$. Two OctoMap hits then give $\ell=1.70$ and $p=0.846$, and one miss ($-0.4$) after them gives $\ell=1.30$ and $p=0.786$. Clamping bounds $\ell$ to an interval $[\ell_{\min},\ell_{\max}]$ after every update.
>
> **Inflation.** A planner that treats the robot as a point (the figure above) has to grow the obstacles instead. Inflating occupied cells by the robot radius produces a C-space obstacle directly on the grid **for a circular robot** — for any other footprint it is an approximation, which is why a stack like Nav2 still runs a separate footprint collision check. Adding a decaying cost outside that radius produces a margin the planner prefers not to enter. As a function of a cell's distance $d$ to the nearest obstacle cell, with inscribed robot radius $r$ and decay rate $\alpha>0$, ROS costmaps use an exponential:
> $$c(d)=\begin{cases}c_{\text{lethal}} & d=0\\ c_{\text{insc}} & 0<d\le r\\ c_{\text{insc}}\,e^{-\alpha(d-r)} & r<d\le d_{\text{infl}}\\ 0 & d>d_{\text{infl}}\end{cases}$$
> so a cell within the inscribed radius means certain collision for a robot centred there, the cost decays with distance outside it, and cells beyond the inflation radius $d_{\text{infl}}$ cost nothing. With $\alpha=3$ /m, a cell 0.2 m outside the inscribed radius costs $e^{-0.6}=0.55$ of the inscribed value; raising $\alpha$ narrows the margin.
>
> **Three radii, and they are not the same number.** A footprint has an **inscribed radius** $r_{\text{insc}}$, the radius of the largest disc centred at the robot's origin that fits *inside* it, and a **circumscribed radius** $r_{\text{circ}}$, the smallest disc that *contains* it. Within $r_{\text{insc}}$ of an obstacle the robot is in collision at every heading; beyond $r_{\text{circ}}$ it is clear at every heading; in between, collision depends on heading, which is the band a footprint check exists to resolve. The **inflation radius** $d_{\text{infl}}$ is a third thing entirely: the distance at which the decaying cost is truncated to zero. It is a *preference* knob and not a safety margin — the safety is $r_{\text{insc}}$, which comes from the footprint and not from $d_{\text{infl}}$. **Non-example, and the most common misconfiguration in the ecosystem:** reading `inflation_radius` as "keep the robot this far from walls" ([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §5]]). With $r_{\text{insc}}=0.30$ m, $\alpha=3$ /m, $d_{\text{infl}}=1.00$ m and the ROS byte scale ($c_{\text{lethal}}=254$ for the obstacle cell, $c_{\text{insc}}=253$, and the skirt scaled by $252$), the cost is $252\,e^{-0.6}=138$ at $d=0.50$ m, $56$ at $0.80$ m and $30$ just inside $1.00$ m — and $0$ just outside it. That step of 30 at $d_{\text{infl}}$ is a **cost cliff**: the decay was meant to fade smoothly to nothing, and a planner that follows the cost downhill meets a jump there instead, so $d_{\text{infl}}$ wants to be large enough that the truncated value is small.
>
> **Costmap.** An occupancy grid whose cells carry *traversal cost* rather than a binary. Cost combines inflation with whatever else the robot should avoid: unknown space, rough terrain, one-way regions, keep-out zones. **A costmap is where a policy preference stops being a plan and becomes geometry** — and it is the representation [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy §1]] argues *is* the right carrier for a learned affordance, since the same scene yields different costmaps for different robots. What that page rejects is the plain occupancy grid, the geometric predicate.
>
> **Layered costmap.** The costmap a planner reads is not one grid that everything writes to. It is a **master grid** produced by composing an ordered list of **layers**, and a layer is a component with exactly two operations, run once per update cycle: it first declares the rectangle of the map it is about to touch, and then writes costs into the master grid inside that rectangle. Two conditions make this a layered costmap rather than a pile of grids. Each layer sees the master grid *as the layers before it left it*, and each layer writes with a declared combination rule — **overwrite**, **maximum**, or maximum-ignoring-unknown. Order is therefore part of the specification and the composition does not commute: the usual order is static map, then obstacles (which mark and clear from live sensor data), then inflation, and inflation must be last because it measures distance to whatever the earlier layers left lethal. *Example*: a person steps in front of the robot; the obstacle layer marks those cells and the inflation layer grows them; the person walks away and ray-casting clears exactly those cells, while the wall behind is untouched because it was never the obstacle layer's to write. **Non-example**: one flattened grid. There, clearing the stale person means clearing cells the static map also claims, so either the wall is erased or the person is permanent — which is the whole reason the layers exist. *Why it matters when reading*: "the costmap" in a paper is a composition, and which layer produced a cost decides whether anything can clear it ([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §4]] for one stack's layer list and defaults).
>
> **Frontier.** A boundary cell between *known free* and *unknown*: precisely, a cell that is itself known free and has at least one unknown neighbour (4- or 8-connected). **Frontier exploration** is the classic answer to "where next": drive to the nearest frontier, and the known region grows until no frontier remains. Some semantic-navigation methods keep this candidate set and let the learned part supply only a *score* over it — [[04-robotics/semantic-language-navigation|19. §3]]'s VLFM is exactly that. Others do not: SemExp's learned global policy picks an arbitrary long-term goal on the map, which is what its own note means by "goal-oriented rather than frontier-based" ([[01-canonical-papers/notes/9-navigation/semexp|SemExp]]). **Which of the two a paper does is the thing to identify**, because it decides whether the learned component chooses candidates or only ranks them.

> [!warning] Two meanings of "frontier"
> §3 and §4 below use *frontier nodes* for the open list of a graph search — the set of nodes
> discovered but not yet expanded. That is a **different object** from an exploration frontier
> on a map, though not an unrelated one: both name the boundary between what has been explored
> and what has not, one in a graph and one in a grid. Papers rarely disambiguate.

A navigation stack searches this costmap in two layers: a global planner finds the route (§3–§5), and a local planner picks the next few seconds of motion along it. The local layer's classical methods are small receding-horizon optimizers, so §6's Deeper note writes them out.

### 3. Graph search

A search holds many partly built routes at once and must choose which one to extend next. A\* ranks them by one number, the cost already paid plus an estimate of the cost still to come, so that the route with the smallest estimated total goes first:

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

A heuristic is meant to change how much work A\* does, never which answer it returns, and whether that promise holds depends on the heuristic. Suppose two frontier nodes have $(g,h)=(6,3)$ and $(4,6)$. Their A* priorities are $9$ and $10$, so the first is expanded even though it has a larger cost-to-come. The heuristic directs effort toward states estimated to be closer to the goal. An *underestimating* heuristic remains admissible — though if it is too weak, A* gains little speed over Dijkstra; an *overestimating* heuristic can lose the usual optimality guarantee.

Here is that loss with numbers. Suppose the second node's true remaining cost is $4$, so its route totals $4+4=8$ and $h=6$ overestimated it by $2$, and suppose the first node's $h=3$ is exact, so its route totals $9$. A\* expands the first node, pushes the goal at $f=9$, pops it before the second node's $f=10$ and returns $9$ when $8$ was available — $12.5\,\%$ over, and no error message. §8 meets the same failure on the Worked case, where a learned heuristic makes A\* return the branch that costs $41\,\%$ more.

### Worked case · 대상으로 한 번 끝까지

§4's $(g,h)$ pairs were bare numbers. Here they come from the Running object — P2, the panel and the query from $q_\mathrm{start}=(90°,0°)$ to the task point $p^\star=(1,1)$ — and the question is the one §3 exists for: which goal does A\* return, and along which edge? Answering it uses §1 (a path is a curve of configurations), §2 (the C-obstacle) and §3 (A\*) at once. [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]], the next three sessions, joins the same two goals to each other.

**1. One task point, two configurations.** Inverse kinematics on P2 ([[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] derives it; here it is only checked): with $r=\lVert p^\star\rVert=\sqrt2=1.4142$ m, the law of cosines gives $\cos\theta_2=(r^2-L_1^2-L_2^2)/(2L_1L_2)=(2-1-1)/2=0$, so $\theta_2=\pm90°$ and there are exactly two goal configurations:

$$q_A=(0°,\ 90°),\qquad q_B=(90°,\ -90°)$$

because each sign of $\theta_2$ fixes the one $\theta_1$ that turns the bent arm onto $p^\star$. Check $q_B$ by forward kinematics, since a goal you did not verify is a goal you invented: $x=\cos 90°+\cos 0°=1$ and $y=\sin 90°+\sin 0°=1$, the same point. Both goals have $d=0$: they lie on the lens's boundary, contact configurations that count as free. They are not the same contact — at $q_A$ link 2 lies flush along the face, at $q_B$ only the tip touches — and in $\mathcal{C}$ they are $\lVert q_A-q_B\rVert=\sqrt{(\pi/2)^2+\pi^2}=\pi\sqrt{1.25}=3.512$ rad apart. That is §2's non-example with a number on it: the tool's position is not a configuration, and the two configurations that realise it are three and a half radians of joint motion apart.

**2. Two different C-space paths, one workspace curve.** Interpolate each goal straight in joint space, $\theta(s)=(1-s)\,q_\mathrm{start}+s\,q_\mathrm{goal}$ for $s\in[0,1]$ — the $s$ of §1's path, which MR ch.10 calls $\lambda$. Branch A is $\theta(s)=(90°-90°s,\ 90°s)$: the sum $\theta_1+\theta_2$ stays at $90°$, so the forearm points straight up and the tip sits one metre above the elbow, at $x=\sin(90°s)$, $y=1+\cos(90°s)$. Branch B is $\theta(s)=(90°,\ -90°s)$: the elbow stays at $(0,1)$ while the forearm swings down from vertical to horizontal, so the tip is at $x=\cos(90°-90°s)=\sin(90°s)$ and $y=1+\sin(90°-90°s)=1+\cos(90°s)$ — the *same* two functions. Check at the midpoint: A is $(45°,45°)$ and B is $(90°,-45°)$, and both put the tip at $(0.7071,\ 1.7071)$. Both edges therefore trace one quarter circle of radius $1$ about $(0,1)$, from $(0,2)$ to $p^\star$.

Now the collision test of the Running object, which checks the elbow as well as the tip. On branch A the elbow and the tip share $x=\sin(90°s)$; on branch B the elbow's $x$ is $0$ and the tip's is $\sin(90°s)$. So on both edges

$$d(s)=\sin(90°s)-1\le0$$

with equality only at $s=1$: each edge is free and touches the panel only at its goal. At the midpoint $d=0.7071-1=-0.2929$ on both, the same $29$ cm of clearance. In $\mathcal{C}$ the edges are different segments — A the diagonal from $(90°,0°)$ to $(0°,90°)$, B the drop from $(90°,0°)$ to $(90°,-90°)$, the lens's pinch point — and both stay outside the lens. Two paths in $\mathcal{C}$, one curve in the workspace, equal clearance — which is why §1 defines a path by its configurations, $\sigma(s)\in\mathcal{C}$, and not by the curve the tool traces.

**3. Same curve, different cost.** Cost the two edges by joint-space length, the usual default:

$$g_A=\lVert(-90°,\ 90°)\rVert=\pi/\sqrt2=2.2214\ \text{rad},\qquad g_B=\lVert(0°,\ -90°)\rVert=\pi/2=1.5708\ \text{rad}$$

so branch A costs exactly $\sqrt2$ times branch B for the same tool motion, because A turns both joints $90°$ where B turns only the elbow. On the three-node graph — start, $q_A$ and $q_B$, both edges tested free — A\* expands the start, pushes both goals and returns $q_B$.

**4. A heuristic that is admissible, and one that only looks it.** Take $h(q)=\lVert p(q)-p^\star\rVert/\sqrt5$, the straight-line task-space distance scaled down. It is admissible because on P2 no joint motion moves the tip more than $\sqrt5$ times as fast. Here $J$ is P2's tip Jacobian, the $2\times2$ matrix with $\dot p=J(\theta)\dot\theta$ whose columns are the tip velocities each joint produces alone ([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §2]] derives it for this arm), and its largest singular value $\sigma_{\max}$ is the most tip speed one unit of joint speed can buy, $\max_{\lVert\dot\theta\rVert=1}\lVert J\dot\theta\rVert$ ([[02-foundations/linear-algebra|1. Linear Algebra §4]]). The trace of $JJ^\top$ is the sum of both squared singular values, so
$\sigma_{\max}^2\le\operatorname{tr}(JJ^\top)=3+2\cos\theta_2\le5$,
with equality at $\theta_2=0$ where the arm is straight and $J$'s two columns are parallel. So a joint path of length $\ell$ moves the tip at most $\sqrt5\,\ell$, and dividing by $\sqrt5$ turns a workspace distance into a lower bound on joint distance. At the start the tip is at $(0,2)$, so $h=\sqrt2/\sqrt5=0.6325$ rad and $f(q_\mathrm{start})=0+0.6325$; once both goals are pushed, $f(q_B)=1.5708$ and $f(q_A)=2.2214$, since $h=0$ at a goal. **Non-example:** the *unscaled* $\lVert p(q)-p^\star\rVert$ is not admissible on this arm, because $\sigma_{\max}>1$ lets the tip outrun the joints. At the start it happens not to overestimate — $1.4142<1.5708$ — so the bad heuristic passes the test case. It fails near $q_B$, where $J$'s largest singular value is $1.618$: step $0.1$ rad from $q_B$ along the joint direction that value belongs to, to the free configuration $q=(94.87°,-86.99°)$, and the tip is $0.164$ m from $p^\star$, so the unscaled $h$ reads $0.164$ against a true remaining cost of $0.100$, the straight edge back to $q_B$.

**5. What the collision model decided.** Both verdicts of step 2 came from one model: links of zero thickness, the whole arm tested, contact free. Change the model and the verdict changes while the path and its cost stay put. Test the tip alone and, for this panel, nothing changes: link 1 is exactly as long as the panel is far, so the elbow term can never fire ([[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2]], its Step 3) — a coincidence of the catalog, not a licence. Move the wall to $x\ge0.5$ and a tip test passes the folded pose $(0°,180°)$, tip back at the base, while link 1 is half a metre through the wall ([[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 §2]]'s non-example). Or grow each link into a capsule of radius $5$ cm — a conservative model, which a valid collision test may use because it only makes the robot bigger — and both edges now collide wherever $\sin(90°s)>0.95$, their last fifth ($s>0.798$), while both goals lie inside the grown obstacle: under that model this contact query has no solution at all. That is one reason a contact task is not planned all the way into contact: [[04-robotics/capstone-panel-contact|26. Capstone §4]] ends the planned motion at a pose outside the band where the panel might be, given its estimated position, and lets a compliant force controller make the contact. $\mathcal{C}_\mathrm{obs}$ is built from a specific geometry, and a paper that reports a collision rate without its collision model has reported half a number.

**6. What "optimal" meant here.** Swap the metric and the answer moves. Under the max-norm, which is what you want when every joint has the same speed limit, the cost is $\max_i\lvert\Delta\theta_i\rvert=\pi/2$ for *both* branches, a tie: at $1$ rad/s per joint both execute in $1.571$ s, A turning both joints at once and B only the elbow. Joint-space length prefers B by $\sqrt2$; execution time cannot tell them apart. The task can: the tool rides along the forearm and must point at the face to press on it, and only B points it along $+x$ — A lays it flush along the face — which is why [[04-robotics/capstone-panel-contact|26. Capstone]] puts its pre-contact pose on B's branch. Here the metric happened to agree with the task; a planner whose goal set holds both branches is trusting that luck, and the problem set shows it failing. Neither number says anything about the force the tool applies once the tip meets the panel: both goals are contact configurations inside $\mathcal{C}_\mathrm{free}$, and $\mathcal{C}_\mathrm{free}$ is silent about force.

### 5. Major method families

Every planning paper belongs to a family, and the family decides what the paper can promise: an answer that is exact, one that is exact only on its grid, or one that becomes likely only as its samples grow. The table places the families; the completeness list after it says what each can promise.

| Family | Representative ideas | Best read as |
|---|---|---|
| Graph search | BFS, Dijkstra, A* | Search over an explicit discretization |
| Sampling based | PRM (probabilistic roadmap), RRT, RRT* | Explore high-dimensional free space through samples |
| Trajectory optimization | shooting, transcription, collocation | Optimize states/inputs under constraints |
| Task planning | symbolic operators and goals | Choose discrete actions |
| TAMP | task and motion planning | Couple symbolic choices to geometric feasibility |
| Feedback / potential field | attractive-to-goal plus repulsive-from-obstacle fields; navigation functions (potentials constructed to have a single minimum, at the goal) | Produce an action for *every* state rather than one path — cheap and reactive, but a plain potential field has local minima that trap the robot short of the goal |
| Uncertain planning | MDP, POMDP, belief space (§7) | Choose actions while accounting for uncertain state/outcomes |

<svg viewBox="0 0 560 176" style="max-width:100%;height:auto" role="img" aria-label="A tree grown from the start through free space around two obstacles toward the goal, with one step drawn: a random sample q_rand, its nearest tree node q_near, and the new node q_new one step ε from q_near toward it, kept because that short segment is free.">
  <rect x="20" y="20" width="330" height="140" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5"/>
  <g fill="currentColor" fill-opacity="0.22"><rect x="140" y="86" width="52" height="40" rx="2"/><rect x="230" y="118" width="52" height="34" rx="2"/></g>
  <g stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"><line x1="50" y1="140" x2="75" y2="122"/><line x1="75" y1="122" x2="100" y2="100"/><line x1="100" y1="100" x2="125" y2="78"/><line x1="125" y1="78" x2="160" y2="64"/><line x1="160" y1="64" x2="200" y2="56"/><line x1="200" y1="56" x2="240" y2="70"/><line x1="240" y1="70" x2="280" y2="56"/><line x1="280" y1="56" x2="320" y2="42"/><line x1="75" y1="122" x2="60" y2="98"/><line x1="100" y1="100" x2="86" y2="136"/><line x1="160" y1="64" x2="168" y2="36"/><line x1="200" y1="56" x2="216" y2="30"/><line x1="240" y1="70" x2="248" y2="100"/><line x1="280" y1="56" x2="294" y2="82"/></g>
  <g fill="currentColor" fill-opacity="0.85"><circle cx="75" cy="122" r="2.4"/><circle cx="100" cy="100" r="2.4"/><circle cx="125" cy="78" r="2.4"/><circle cx="160" cy="64" r="2.4"/><circle cx="200" cy="56" r="2.4"/><circle cx="240" cy="70" r="2.4"/><circle cx="280" cy="56" r="2.4"/><circle cx="320" cy="42" r="2.4"/><circle cx="60" cy="98" r="2.4"/><circle cx="86" cy="136" r="2.4"/><circle cx="168" cy="36" r="2.4"/><circle cx="216" cy="30" r="2.4"/><circle cx="248" cy="100" r="2.4"/></g>
  <g fill="currentColor"><circle cx="50" cy="140" r="4.5"/><circle cx="320" cy="42" r="4.5"/></g>
  <line x1="294" y1="82" x2="322" y2="128" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/>
  <line x1="294" y1="82" x2="307" y2="103.4" stroke="currentColor" stroke-width="2.4"/>
  <circle cx="322" cy="128" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="294" cy="82" r="4.2" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="307" cy="103.4" r="3" fill="currentColor"/>
  <g fill="currentColor">
    <text x="30" y="156" font-size="10.5">start</text>
    <text x="296" y="32" font-size="10.5">goal</text>
    <text x="166" y="110" font-size="10" text-anchor="middle" opacity="0.9">obstacle</text>
    <text x="256" y="139" font-size="10" text-anchor="middle" opacity="0.9">obstacle</text>
    <text x="316" y="143" font-size="10.5" text-anchor="end">q<tspan dy="3" font-size="10">rand</tspan><tspan dy="-3"> </tspan></text>
    <text x="287" y="87" font-size="10.5" text-anchor="end">q<tspan dy="3" font-size="10">near</tspan><tspan dy="-3"> </tspan></text>
    <text x="315" y="107.4" font-size="10.5">q<tspan dy="3" font-size="10">new</tspan><tspan dy="-3"> </tspan></text>
    <text x="362" y="52" font-size="11">1. sample a point q<tspan dy="3" font-size="10">rand</tspan><tspan dy="-3"> </tspan></text>
    <text x="362" y="72" font-size="11">2. find the nearest node q<tspan dy="3" font-size="10">near</tspan><tspan dy="-3"> </tspan></text>
    <text x="362" y="92" font-size="11">3. step ε toward it and keep</text>
    <text x="376" y="112" font-size="11">q<tspan dy="3" font-size="10">new</tspan><tspan dy="-3"> </tspan> if that segment is free</text>
  </g>
</svg>

A sampling-based planner grows a tree from the start through free space. Each step samples a point $q_\text{rand}$, finds the nearest node $q_\text{near}$ and adds $q_\text{new}$ one step toward it if that short segment is free — [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 §1]] writes the step as a formula and takes one on P2. The tree never enumerates the space, which is why it survives high dimensions, and its path comes out jagged, so it is smoothed afterwards.

**The potential field, written out.** A potential field is a scalar function $U:\mathcal{C}\to\mathbb{R}$ whose downhill direction is the command, $\dot q=-\nabla U(q)$. It is built from an attractive part and a repulsive part:
$$U(q)=\tfrac12 k_a\lVert q-q_{\text{goal}}\rVert^2+\begin{cases}\tfrac12 k_r\big(\tfrac1{\rho(q)}-\tfrac1{\rho_0}\big)^2 & \rho(q)\le\rho_0\\ 0 & \rho(q)>\rho_0\end{cases}$$
Here $k_a,k_r>0$ are gains, $\rho(q)$ is the distance to the nearest obstacle and $\rho_0$ is the range beyond which obstacles are ignored, so the robot slides toward the goal and is pushed back ever harder as $\rho\to0$. A **navigation function** (Rimon & Koditschek 1992) is a potential that satisfies four further conditions: it is smooth on the free space, has a *unique* minimum at the goal, is uniformly maximal on every obstacle boundary, and has only non-degenerate critical points. Its gradient therefore reaches the goal from almost every start.

> [!example] Worked example · 계산 예제
> Goal at the origin, a point obstacle at $(1,0)$, and $k_a=k_r=\rho_0=1$. On the axis beyond the obstacle ($x>1$) the attractive force at $x$ is $-x$ and the repulsive force is $(1/\rho-1)/\rho^2$ with $\rho=x-1$. They cancel at $x=1.618$ ($\rho=0.618$), so a robot released at $(2,0)$ comes to rest there, short of the goal.
>
> **Non-example of a local minimum:** that point is a *saddle*. Moving sideways lowers the potential, $\partial^2U/\partial y^2=1-1.618/0.618=-1.62<0$, so any perturbation lets the robot slide around the obstacle. A concave obstacle such as a U-shaped wall creates a true minimum, and that is the trap the table warns of.

**Completeness, in four strengths.** These words state what a planner guarantees about *finding* a solution. The first three have definition boxes worked on P2 in [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 §3]], so here they get one line each; the fourth is this page's.

- **Complete**: it returns a solution in finite time when one exists and reports failure in finite time when none does — exact cell decomposition in low dimensions, almost nothing practical in high ones.
- **Resolution complete**: complete relative to a discretisation. A\* on a grid finds any solution the grid can represent, and its failure proves nothing about a passage narrower than a cell.
- **Probabilistically complete**: when a *robust* solution exists — one whose $\delta$-neighbourhood lies in $\mathcal{C}_{\text{free}}$ for some $\delta>0$, also called $\delta$-clear — the probability of having found one tends to $1$ as the samples grow. A path that only grazes obstacles has probability zero of being sampled, which is why the Worked case's contact goals are handed to a sampling planner by the query and never sampled. The planner cannot report "no solution", and the guarantee is not fast success. PRM and RRT have it.
- **Asymptotically optimal**: the cost $c_n$ of the best solution after $n$ samples converges to the optimal cost $c^*$ with probability one. This is a statement about the limit, so it says nothing about the quality available under a real-time budget. RRT\* and PRM\* have it; plain RRT does not (§5.5.4, in §5.5's Deeper note).
$$P\Big(\lim_{n\to\infty}c_n=c^*\Big)=1$$

> [!example] Worked example · 계산 예제
> In a simplified model, suppose every solution passes through a narrow passage that fills 1% of $\mathcal{C}$, and the planner succeeds once one uniform sample lands inside it. Each sample misses with probability $0.99$, independently, so the failure probability after $n$ samples is $0.99^n$: $0.366$ at $n=100$, $0.0066$ at $n=500$, and $4.3\times10^{-5}$ at $n=1000$. It tends to zero, which is probabilistic completeness, yet a third of the 100-sample runs fail, which is why the guarantee says nothing about speed.
>
> **Non-example of completeness:** a grid of 10 cm cells can return "no path" on a map whose only gap is 5 cm wide, because every cell that straddles the gap is marked occupied. The answer is correct for the grid, as resolution completeness promises, and wrong for the world.

### 5.5 Planning under dynamics: kinodynamic search, lattices, and flatness

*In one sentence:* a car cannot slide sideways and a crane's load swings, so the pieces a planner strings together have to be motions the machine can actually drive, and this section shows four standard ways to make such pieces.

*If you need only one thing from this section:* whether a curve can be driven is decided by its shape, not by the speed along it; §5.5.5's parabola has curvature $2\,\mathrm{m^{-1}}$ at its vertex at every speed, twice what a $1\,\mathrm{m}$ turning radius allows.

A robot that cannot move in every direction at every speed needs a planner whose edges are motions the machine can execute, so the straight-line connection that grid edges and §5's sampling tree assume has to be replaced by a steering rule that respects the dynamics.

#### 5.5.1 Why a geometric path is not enough

Three kinds of constraint break the straight-segment assumption:

- **Nonholonomic.** A car has no sideways velocity and a minimum turning radius, so a path with a corner or a sideways shift is undrivable as written, even though the car can still reach every pose ([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR ch.13]] explains why). Formally, a nonholonomic constraint is a velocity constraint $A(q)\dot q=0$ that cannot be integrated into a constraint on $q$ alone. For a car or unicycle with heading $\theta$ it reads as follows, because the velocity must point along the heading:
$$\dot x\sin\theta-\dot y\cos\theta=0$$
  At $\theta=0$, forward motion $(\dot x,\dot y)=(1,0)$ gives $0$ and is allowed, while sideways motion $(0,1)$ gives $-1$ and is forbidden. A **holonomic** constraint $g(q)=0$ removes a dimension from $\mathcal{C}$; a nonholonomic one removes directions of motion but no reachable configurations.
- **Dynamic.** An excavator boom carries inertia and a crane's suspended load swings, so the plan must also keep accelerations low enough that the machine stays stable and the load does not oscillate.
- **Bounds.** Velocity, acceleration, and actuator limits hold even for a robot that can move in any direction.

*Kinodynamic* originally named planning under velocity and acceleration bounds; it now covers any planning in a state space with $\dot x = f(x,u)$. A problem can be nonholonomic, kinodynamic, or both: a car with a dynamics model is both. MR ch.10 names the sampling version and its local planners in one line; this section is the longer map.

Three standard ways to build edges that a car or a machine can drive — exact shortest car paths (Dubins and Reeds–Shepp), search over precomputed motion primitives (state lattices and Hybrid A\*), and sampling with the dynamics integrated (kinodynamic RRT, RRT\* and FMT\*) — are §5.5.2–§5.5.4, in the Deeper note below; open it when a vehicle or excavator paper names one of them. The fourth, differential flatness, stays in the main text as §5.5.5, because its worked example is the one to compute.

> [!note]- Deeper · 더 깊이
> **5.5.2 Exact shortest paths for a car: Dubins and Reeds–Shepp.**
>
> - **Dubins (1957):** a forward-only car at constant speed with minimum turning radius $\rho$. Between any two poses $(x,y,\theta)$ the shortest path has at most three segments, each a full-lock left arc $L$, a full-lock right arc $R$, or a straight $S$. Only six *words* can be optimal: $LSL, LSR, RSL, RSR, LRL, RLR$. In the $CCC$ words the middle arc turns through more than $\pi$. The intuition is a shortest route around a bend: turn as tightly as allowed, drive straight, turn as tightly as allowed again — a gentler arc only adds length — and Dubins proved that three such pieces always suffice.
> - **Reeds–Shepp (1990):** the same car allowed to reverse. The shortest path is one of a fixed list of fewer than fifty words, each at most five segments long with at most two gear changes (cusps).
>
> Both are closed-form, so planners use them as a **steering function**, meaning an exact connection between two states. They also serve as the obstacle-free, turning-radius-aware half of the lattice heuristic in [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms]] §8. Two limits come with them. They ignore obstacles. And curvature jumps at every segment joint, so a real steering wheel cannot follow the corner exactly.
>
> **5.5.3 Search over motion primitives: state lattices and Hybrid A\*.** A\* itself is [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms]] §6; what changes here is what an edge is.
>
> - **State lattice** (Pivtoraiko, Knepper & Kelly 2009). Discretize $(x,y,\theta)$, sometimes with curvature or speed, on a regular grid. Offline, solve boundary-value problems — find an input that drives the model from one given state to exactly another — for a small set of feasible primitives that start and end exactly on lattice states. The set is translation-invariant, so the same primitives are reused everywhere.
> - **Hybrid A\*** (Dolgov, Thrun, Montemerlo & Diebel 2010). Expand a node by integrating the car model for a few steering values. Keep one *continuous* pose per discrete $(x,y,\theta)$ cell and prune later arrivals in the same cell. Try an analytic Reeds–Shepp shot to the goal as the search nears it, then smooth the result.
>
> Their guarantees differ. A lattice planner's completeness or optimality claim is relative to its primitive set, not to the continuous problem. Hybrid A\*'s path is drivable, but the cell pruning gives up completeness and optimality even on the lattice. [[04-robotics/ros2/navigation-nav2|Nav2]] ships both as its "feasible" planners.
>
> **5.5.4 Sampling with dynamics: kinodynamic RRT, RRT\* and FMT\*.** *Kinodynamic RRT* (LaValle & Kuffner 2001) samples a state, finds the nearest tree node under a chosen metric, and extends it by integrating $\dot x = f(x,u)$ for some input and duration. That forward propagation needs no boundary-value solver, but new nodes never land exactly on the sampled state, and the metric choice matters. Karaman & Frazzoli (2011) showed that plain RRT converges to a suboptimal path with probability one; RRT\* and PRM\* restore asymptotic optimality by connecting each sample to neighbours within a radius that shrinks like $(\log n / n)^{1/d}$. That rate keeps on the order of $\log n$ samples in each ball, because the ball's volume scales as $r^d \propto \log n/n$ and there are $n$ samples: few enough that rewiring stays cheap, yet enough that the graph stays connected as samples multiply. FMT\* (Janson et al. 2015) reaches the same guarantee with a lazy dynamic-programming pass over a batch of samples that postpones collision checks. The asymptotically optimal versions for dynamical systems need an exact steering function plus its cost — Dubins or Reeds–Shepp for cars, a precomputed lattice, or flatness below.

#### 5.5.5 Differential flatness

Some systems let you plan a few output curves freely and read every state and input off them. Fliess, Lévine, Martin & Rouchon (1995) call a system $\dot x = f(x,u)$ *flat* when there are outputs $z$ (as many as there are inputs) such that

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

A search returns a route through free space but not the motion along it — how fast, with which inputs, at what effort. Trajectory optimization chooses that motion by minimising a cost under the dynamics and the obstacles, and MPC re-solves it as the robot moves.

A common formulation is the trajectory-optimization program of [[02-foundations/optimization|4. Optimization]] — read it as a running cost paid at every step plus a terminal cost at the end, with the physics and the obstacles as constraints:

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. dynamics, bounds, and collision constraints.}$$

**Every symbol.** $x_t\in\mathbb{R}^n$ is the state at step $t$ and $u_t\in\mathbb{R}^m$ the input. $N$ is the **horizon**, the number of steps. The **running** (or **stage**) **cost** $\ell(x_t,u_t)$ is a scalar paid at every step, such as distance to the goal or control effort. The **terminal cost** $\ell_f(x_N)$ is paid once, on the final state, and is often written $\phi(x_T)$. Their sum is the objective $J$, so the program minimises the total cost of one proposed future. The constraints have three named kinds:

- **dynamics** $x_{t+1}=f(x_t,u_t)$ for every $t$, with $x_0$ fixed to the current state;
- **bounds** such as $u_{\min}\le u_t\le u_{\max}$;
- **collision constraints** such as $\mathrm{sd}(x_t)\ge d_{\text{safe}}$, where $\mathrm{sd}$ is the signed distance to the nearest obstacle, positive outside it — the opposite sign to the penetration depth $d$ of the Running object and MR ch.10, which is positive inside.

This is the general program of [[02-foundations/optimization|4. Optimization §1]] with the decision variable spread over time, and its linear-quadratic special case, written as a quadratic program (QP), is in [[02-foundations/optimization|4. Optimization §5]].

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

A navigation stack runs this loop in miniature: its local planner re-plans the next few seconds of motion every cycle, around the route its global planner found. The Deeper note lists the classical local planners and writes out two of them.

> [!note]- Deeper · 더 깊이
> **Global and local.** Navigation stacks split planning in two: a **global planner** searches the whole costmap of §2 for a route (§3–§5), and a **local planner** repeatedly picks the next few seconds of motion, given the route, the robot's dynamics, and obstacles that appeared since. The local layer is where the classical names live:
>
> | Local planner | What it does each cycle |
> |---|---|
> | *Dynamic window* | Samples velocity pairs (forward, turning) the robot can reach within one cycle, and scores each |
> | **Elastic band** | Deforms a *path* under an internal contraction force and an external obstacle repulsion, with no notion of time |
> | **Timed elastic band** | The descendant that adds the time intervals its name refers to |
> | **Sampling-based MPC** (the family [[01-canonical-papers/notes/9-navigation/badgr\|BADGR]] uses) | Samples many action sequences around a running estimate, rolls each forward through a model, refits the estimate by a **reward-weighted average** over the samples rather than taking the single best, and executes its first action |
>
> **Dynamic window** (Fox, Burgard & Thrun 1997). Let $(v_c,\omega_c)$ be the current forward and turning velocities, $\dot v_{\max},\dot\omega_{\max}$ the acceleration limits and $\Delta t$ the cycle time. The candidates must satisfy three conditions at once. They must be velocities the robot can have at all ($V_s$). They must be reachable within one cycle, which is a small box because accelerations are bounded:
> $$V_d=\{(v,\omega): |v-v_c|\le\dot v_{\max}\Delta t,\ |\omega-\omega_c|\le\dot\omega_{\max}\Delta t\}$$
> And they must be **admissible**, meaning the robot can still brake to a stop before the nearest obstacle on that arc, $v\le\sqrt{2\,\mathrm{dist}(v,\omega)\,\dot v_b}$ with braking deceleration $\dot v_b$ (and likewise for $\omega$). Each pair in $V_s\cap V_d\cap V_a$ is scored by a weighted sum of heading toward the goal, clearance and speed, and the best pair is executed for one cycle. Example: $v_c=0.5$ m/s, $\dot v_{\max}=0.5$ m/s² and $\Delta t=0.25$ s give $v\in[0.375,0.625]$ m/s. An obstacle 0.5 m along the arc with $\dot v_b=0.5$ m/s² caps $v$ at $\sqrt{0.5}=0.71$ m/s, so here the window, not the obstacle, is the binding limit.
>
> **Reward-weighted average.** Sample $K$ action sequences $u^{(k)}$ around the current estimate $\bar u$, roll each through the model to a return $R_k$, and refit:
> $$\bar u\leftarrow\sum_{k=1}^{K}w_k\,u^{(k)},\qquad w_k=\frac{\exp(R_k/\lambda)}{\sum_{j=1}^{K}\exp(R_j/\lambda)}$$
> The weights are positive and sum to one, so every sample contributes in proportion to how good it was, and the temperature $\lambda>0$ sets how sharply they favour the best ($\lambda\to0$ recovers "take the single best"). Example: two samples whose first actions are $0.4$ and $0$, with returns $1$ and $0$ and $\lambda=1$, get weights $0.731$ and $0.269$, so the new first action is $0.292$.
>
> The program above is the optimization view of the same layer. In a classical navigation stack the learned component is usually the local layer, with the global search and the costmap untouched — but not always: learned global planners and learned search heuristics exist, and the end-to-end line of [[04-robotics/semantic-language-navigation|19. §3]] replaces the whole stack. **Identify which layer a paper actually replaced**, because that bounds what its result can claim.

**Check your understanding.** A solver's feasible output is conditional on its initial state, model, discretization, and constraints. If state estimates are stale or a collision occurs between checked points, solving the optimization accurately is not enough. See the [trajectory-optimization notes](https://underactuated.mit.edu/trajopt.html) for the distinction between representing a trajectory and executing it with feedback.

### 7. Task planning, uncertainty, and replanning

A symbolic instruction such as `pick(block)` may be logically valid yet geometrically impossible because no collision-free grasp exists. TAMP alternates or jointly reasons over discrete actions and continuous feasibility.

**Symbolic task planning, defined.** A classical (STRIPS-style) planning problem has four parts. There is a set of Boolean **propositions**, facts such as `holding(block)`. A **state** $s$ is the set of propositions currently true, with an initial state $s_0$ and a **goal** $G$, the set of propositions that must end up true. And there are **operators**, each with a precondition set $\mathrm{pre}(a)$, an add list $\mathrm{add}(a)$ and a delete list $\mathrm{del}(a)$. An operator is applicable in $s$ when $\mathrm{pre}(a)\subseteq s$, and applying it replaces exactly the facts it names, so the successor state is
$$s'=\big(s\setminus\mathrm{del}(a)\big)\cup\mathrm{add}(a)$$
A plan is a sequence of applicable operators after which $G\subseteq s$. Example, simplified: `pick(block)` with pre $\{$`handempty`, `clear(block)`$\}$, del $\{$`handempty`$\}$ and add $\{$`holding(block)`$\}$ takes $\{$`handempty`, `clear(block)`$\}$ to $\{$`clear(block)`, `holding(block)`$\}$. **Non-example:** nothing in that state records where the block is or whether a collision-free grasp exists, so a valid symbolic plan is not yet an executable one. That gap is what TAMP fills.

**MDP and POMDP, as tuples.** An **MDP** is $(\mathcal{S},\mathcal{A},T,R,\gamma)$: a state set, an action set, a transition kernel $T(s'\mid s,a)$, a reward $R(s,a)$ and a discount $\gamma\in[0,1]$, together with the Markov property that the next state depends only on the current state and action. Its complete definition is [[02-foundations/rl-basics|RL Basics §1]].

With partial observability, the planning state becomes a **belief**: a probability distribution over the hidden state, updated after every action and observation by the **Bayes filter** of [[04-robotics/state-estimation-slam|3. State Estimation §4]] — a predict step that pushes the belief through the motion model, then a correct step that reweights it by the observation's likelihood and renormalises. A POMDP distinguishes hidden state, observation, action, transition, observation model, and reward. Written as a tuple, a **POMDP** (partially observable MDP) is
$$(\mathcal{S},\mathcal{A},\Omega,T,Z,R,\gamma,b_0)$$
which adds three components to the MDP, because the state is no longer seen: an **observation space** $\Omega$, an **observation model** $Z(o\mid s',a)$ giving the probability of observing $o$ when action $a$ has led to state $s'$, and an **initial belief** $b_0$. The belief $b(s)$ is the posterior probability of state $s$ given every action and observation so far. After taking $a$ and observing $o$, Bayes' rule updates it:
$$b'(s')=\eta\,Z(o\mid s',a)\sum_{s\in\mathcal{S}}T(s'\mid s,a)\,b(s)$$
The sum is the **prediction**, which pushes the old belief through the dynamics; the factor $Z$ is the **correction**, which weights each state by how well it explains $o$; and $\eta$ is the normaliser that makes $b'$ sum to one. This is that Bayes filter with the action chosen by the planner rather than given, so the planner can ask which action will leave the most useful belief. Since the belief summarises the whole history, a POMDP is an MDP whose states are beliefs, with expected reward $\rho(b,a)=\sum_s b(s)\,R(s,a)$. **Non-example:** the latest observation alone is not a Markov state. The same "open" reading moves a belief of $0.5$ to $0.8$ but a belief of $0.8$ to $0.94$ in the example below.

> [!example] Worked example · 계산 예제
> A robot must go through a door it cannot see clearly. **Hidden state:** open or closed. **Action:** look again, or drive through. **Transition:** looking changes nothing; driving moves the robot. **Observation:** a sensor reading "open" or "closed". **Observation model:** the reading is right 80% of the time. **Reward:** $+1$ for getting through, $-1$ for hitting a closed door.
>
> Start from belief $P(\text{open})=0.5$. One "open" reading gives $0.8\cdot0.5/(0.8\cdot0.5+0.2\cdot0.5)=0.8$; a second gives $0.8\cdot0.8/(0.8\cdot0.8+0.2\cdot0.2)\approx0.94$. These are the update formula above: looking leaves the state unchanged, so the sum is just $b(s')$, $Z$ is $0.8$ or $0.2$, and $\eta=1/0.5=2$ the first time and $1/0.68=1.47$ the second. Driving at belief 0.8 has expected reward $\rho=0.8\cdot(+1)+0.2\cdot(-1)=0.6$; at 0.94 it is $0.88$. Whether one more look is worth its time is exactly the question a POMDP planner answers, and it is asked about the belief, not the true door.

Exact belief-space planning is often intractable, so papers use approximations, receding horizons, learned values, or contingency policies.

Online replanning incorporates new observations. Reported replanning frequency is not enough: compare it with perception latency, scene dynamics, and controller bandwidth.

### 8. Learning-based planning

A paper that swaps a learned network into a planner has to answer one question: does the planner still keep the guarantee of the slot the network fills? Learned components may provide a heuristic, cost, dynamics/world model, value function, proposal distribution, trajectory generator, or entire policy. A VLA that outputs actions is usually a policy; a world model that rolls out futures supports planning only when a selection or optimization procedure uses those futures.

**What a learned piece does to the guarantees.** A learned component keeps the guarantee of the slot it fills only if it meets that slot's conditions, and a trained network is measured on a test set, never shown to meet a condition everywhere. Two slots, worked on this page's own numbers.

*A learned heuristic in A\*.* A regressor of cost-to-go is rarely admissible (§3). If its overestimate is bounded everywhere, $h\le\varepsilon h^*$ for some factor $\varepsilon>1$, the argument behind weighted A\* ([[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms §6]]), with a node reopened whenever a cheaper route reaches it, still bounds the returned cost by $\varepsilon C^*$. On the Worked case, branch A costs $\sqrt2=1.414$ times branch B, so any $\varepsilon<1.414$ still forces A\* to return B. The bound also needs $h=0$ at every goal, since $h^*$ is zero there, and regression does not enforce that: on the Worked case's three-node graph, a network that reads more than $0.651$ rad higher at $q_B$ than at $q_A$ makes $f(q_B)=1.5708+h(q_B)$ exceed $f(q_A)=2.2214+h(q_A)$, and A\* returns the branch that costs $41\%$ more.

*A learned sampler in a sampling planner.* Probabilistic completeness (§5) needs only that every region of $\mathcal{C}_{\text{free}}$ keeps a positive chance of being sampled. In §5's narrow passage, a learned proposal that puts $20\%$ of its samples in the passage still misses after $20$ samples with probability $0.8^{20}=0.012$, against $0.99^{20}=0.818$ for uniform sampling; but a proposal that never samples some region has lost the guarantee on every map whose only solution runs there. Drawing half the samples uniformly keeps every region's chance at no less than half its uniform value, $0.005$ per sample for this passage, which restores the guarantee, and on this passage the mixture still misses only $0.895^{20}=0.109$ of the time.

So the question to put to a paper is which slot its network fills and which of that slot's conditions still hold. A learned policy or trajectory generator fills no slot that carries a guarantee at all, which is what the warning below is about.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> “Generates plausible trajectories” does not imply collision-free, dynamically feasible, stable, or safe execution. Check explicit constraints, downstream controllers, replanning, and closed-loop robot results.

### 9. Evaluation and failure modes

A planning paper reports its result as a handful of numbers, and each of them misleads unless the condition it was measured under comes with it. Check success rate, collision rate, path/trajectory cost, planning and execution time, optimality gap (the relative excess cost $(C-C^*)/C^*$, so an 11 m path against a 10 m optimum is a 10% gap), constraint violation, replanning rate, robustness to map/state error, and closed-loop execution. Separate planning failure, perception failure, tracking failure, and hardware failure.

**Four of those numbers need their conditions, worked on this page.** An optimality gap is relative to a cost. On the Worked case, branch A's gap is $(2.2214-1.5708)/1.5708=41\%$ under joint-space length and $0\%$ under the max-norm, where both branches take $1.571$ s at $1$ rad/s per joint, so a gap that does not name its metric says nothing. A success rate is relative to its trial count. Eighteen successes in twenty is $90\%$ with a 95% Wilson interval of $[0.70,\ 0.97]$ — the interval [[02-foundations/ml-practice|9. ML Practice & Evaluation]] derives in its worked case and computes for these same 18 of 20 in its problem 3 — a rival's sixteen of twenty gives $[0.58,\ 0.92]$, and a twenty-trial table that separates two planners by two successes has not ranked them ([[06-research-practice/experimental-design-reproducibility|Experimental Design §4]], later in research practice). And planning time is a distribution. In §5's narrow passage the number of samples to the first success is geometric, with mean $1/0.01=100$, median $69$ and 95th percentile $299$, because $0.99^n$ first drops below $0.05$ at $n=299$; a planner reported by its mean hides a tail three times as long. And a replanning rate is bounded by the rate of new information. Replanning at $10$ Hz from a costmap refreshed at $2$ Hz makes five plans per map, four of them from data already used, and a new obstacle can wait up to one map period plus one planning period, $0.5+0.1=0.6$ s not counting computation, before any plan reflects it: $0.6$ m of travel at $1$ m/s. That is the sampling-latency argument of [[04-robotics/robot-systems-deployment|10. Robot Systems §3]].

**Attribute a failure before counting it.** A collision in execution is a planning failure only if the collision model the planner checked is the one the robot met. In the Worked case's step 5, a tip-only check agrees with the whole-arm test against this panel only because link 1 is exactly as long as the panel is far; against a wall at $x\ge0.5$ it would pass the folded pose $(0°,180°)$ with link 1 half a metre inside. A robot that planned with that check and then hit the wall did what its search was told, so the collision belongs to the collision model, not to the planner. Keeping the first violated contract apart from the visible outcome is the failure taxonomy of [[04-robotics/robot-systems-deployment|10. Robot Systems §10]], and [[06-research-practice/failure-analysis-system-evaluation|3. Failure Analysis §1]] applies it to a whole log.

### After reading

You should be able to:

- distinguish plan, path, trajectory, policy, and controller;
- interpret $g$, $h$, and $f$ in A*;
- explain probabilistic completeness without calling it a speed guarantee;
- compare graph search, sampling, and trajectory optimization;
- explain why TAMP must test geometric feasibility;
- identify what a learned trajectory generator does not guarantee;
- check that a "collision-free" or "optimal" claim names its collision model and its metric.

> [!tip] Going deeper · 더 깊이
> LaValle's [*Planning Algorithms*](http://lavalle.pl/planning/) is free and is the reference for the sampling-based half, though it is a 2006 book: it stops at probabilistic completeness and has neither RRT\* nor asymptotic optimality, which are Karaman and Frazzoli (2011); Tedrake's [*Underactuated Robotics*](https://underactuated.csail.mit.edu/) covers the trajectory-optimization half with code you can run.

### Self-check

1. Why can a collision-free path be dynamically infeasible?
2. What is lost when planning only in workspace rather than configuration space?
3. Why can trajectory optimization fail even when a feasible trajectory exists?
4. What evidence would support a “real-time closed-loop planner” claim?
5. (With §5.5's Deeper note.) A Hybrid A\* paper and a state-lattice paper both call their paths "optimal". Optimal with respect to what, in each case?
6. The parabola $z(t)=(t,t^2)$ violates a 1 m minimum turning radius near its vertex. Why does slowing down along the same curve not fix it?

> [!tip]- Answers
> 1. It may require impossible velocity, acceleration, torque, contact, or timing. 2. Robot geometry, joint limits, and multiple configurations for the same task pose. 3. The problem can be nonconvex and sensitive to initialization. 4. End-to-end latency distributions on specified hardware, execution with disturbances/dynamic obstacles, constraint violations and failures—not planner compute time alone. 5. The lattice planner is optimal only over its precomputed primitive set and resolution, so it can miss paths that need headings or curvatures the set lacks; Hybrid A\* is not optimal even on its grid, because it keeps one continuous pose per cell and prunes the rest. 6. The turning-radius limit bounds the curvature $\kappa=\omega/v$, which depends only on the geometry: at half speed the vertex has $v=0.5$ and $\omega=1$, so $\kappa$ is still 2. Only a different curve helps.

### Problem set · 과제

Tier B, taken in the Working pass. **P2** ([[02-foundations/lab-plants|0.6]], the catalog's planar two-link arm), the panel $x\ge1$ and the goals $q_A$, $q_B$ of the Worked case, with two changes. The arm was stopped halfway along branch A, at $q_h=(45°,45°)$ — elbow $(0.7071,0.7071)$, tip $(0.7071,1.7071)$ — and the task now requires the tool to point at the face, which only $q_B$ does (step 6). And the shoulder is geared down to $0.5$ rad/s while the elbow keeps $1$ rad/s. Graphs of two or three nodes, no simulator.

1. **Draw.** The picture for this variant. In $\mathcal{C}$: the lens, $q_h$, $q_\mathrm{start}$, $q_A$ and $q_B$, the straight edge $q_h\to q_B$ with the point where it enters the lens marked, and the detour $q_h\to q_\mathrm{start}\to q_B$. In the workspace: the arm at $q_h$ and at $q_B$, the tip's path along the straight edge with its farthest point past the face labelled, and the detour's tip path. Which curve of the Worked case does the detour's tip retrace?
2. **Derive.** (a) Cost the straight edge $q_h\to q_B$ by joint-space length, by the max-norm, and by the travel time $t=\max(\lvert\Delta\theta_1\rvert/0.5,\ \lvert\Delta\theta_2\rvert/1)$ in seconds. (b) Along that edge write the tip's $x(s)$ and find the deepest penetration: substitute $w=45°+45°s$ and use $\sin(2w-90°)=-\cos 2w$ to write $x$ as a quadratic in $c=\cos w$. Over which range of $s$ is the edge inside the panel, and does the elbow term ever decide? (c) Test the detour's two legs with the same $d$, cost the detour in radians and in seconds, and give its excess over the blocked straight edge.
3. **Interpret.** On the three-node graph $\{q_h,\ q_A,\ q_B\}$ with both edges tested, A\* returns $q_A$. Say why that answer is right for the graph and wrong for the task, which change to the query fixes the goal, and what A\* then reports on the two-node graph $\{q_h,\ q_B\}$ — and whether that report says anything about $\mathcal{C}_\mathrm{free}$ (§5).

> [!note]- How to draw it · 그리는 법
> - Right panel, the configuration space: $\theta_1$ across and $\theta_2$ up, each from $-180°$ to $180°$, with a note that opposite edges are identified ($\mathcal{C}=T^2$, §2). Shade the lens $\cos\theta_1+\cos(\theta_1+\theta_2)>1$; ch.2's Step 4 table gives points on its boundary, among them $(0°,\pm90°)$, $(\pm60°,0°)$, $(60°,-120°)$, $(-60°,120°)$ and the two pinches $(90°,-90°)$ and $(-90°,90°)$.
> - Dots at $q_h=(45°,45°)$, $q_\mathrm{start}=(90°,0°)$, $q_A=(0°,90°)$ and $q_B=(90°,-90°)$, with $q_A$ and $q_B$ ringed as contact, free.
> - The straight edge $q_h\to q_B$ as one segment; mark where it crosses into the lens and put an X at its deepest point.
> - The detour as two segments: $q_h\to q_\mathrm{start}$ along the line $\theta_1+\theta_2=90°$, then straight down to $q_B$.
> - Left panel, the workspace: the base at the origin, the face $x=1$ hatched on the $x>1$ side, $p^\star=(1,1)$ on it, and the arm drawn link by link at $q_h$ and at $q_B$ — elbow at $(\cos\theta_1,\sin\theta_1)$, tip one more metre along $\theta_1+\theta_2$.
> - The tip's path on the straight edge, from $(0.707,1.707)$ across the face and back to $p^\star$, with its entry point and its farthest point labelled; then the detour's tip path, dashed.

> [!tip]- Solutions
> 1. In $\mathcal{C}$ the straight edge from $(45°,45°)$ to $(90°,-90°)$ enters the lens at $s=1/3$, the configuration $(60°,0°)$ — the arm straight at $60°$ with its tip on the face at $(1,1.732)$, a boundary point of ch.2's table — and stays inside until it reaches $q_B$ at the pinch; its deepest point is $(75.52°,-46.57°)$. The detour's first leg lies on the Worked case's edge A (the line $\theta_1+\theta_2=90°$) and its second leg is edge B, so both stay outside the lens. In the workspace the straight edge's tip crosses the face at $(1,1.732)$, bulges out to $(1.125,1.452)$ and comes back to $p^\star$. The detour's tip retraces the Worked case's quarter circle about $(0,1)$: up to $(0,2)$ and down again to $p^\star$.
> 2. (a) $\Delta\theta=(45°,-135°)$: joint-space length $45°\sqrt{10}=2.4836$ rad, max-norm $135°=2.3562$ rad, and time $\max(0.785/0.5,\ 2.356/1)=2.356$ s, set by the elbow. (b) $\theta_1=45°+45°s$ and $\theta_1+\theta_2=90°-90°s$, so $x(s)=\cos(45°+45°s)+\sin(90°s)$. With $w=45°+45°s$, $90°s=2w-90°$ and $\sin(2w-90°)=-\cos 2w=1-2\cos^2 w$, so $x=1+c-2c^2$. It peaks at $c=1/4$, where $x=1.125$: $d_{\max}=0.125$ m at $w=75.52°$, $s=0.678$, $\theta=(75.52°,-46.57°)$, tip $(1.125,1.452)$. And $x>1$ exactly when $c(1-2c)>0$, i.e. $0<c<1/2$, $w\in(60°,90°)$, $s\in(1/3,1)$: the edge is inside the panel over its last two thirds and touches the face again only at $q_B$. The elbow's $x=\cos w\le0.707$ never decides. (c) Leg 1, $q_h\to q_\mathrm{start}$, keeps $\theta_1+\theta_2=90°$, so the tip's $x$ equals the elbow's, $\cos\theta_1\le0.707$: free, $45°\sqrt2=1.1107$ rad, $\max(0.785/0.5,\ 0.785/1)=1.571$ s. Leg 2 is the Worked case's edge B: free, $1.5708$ rad, $1.571$ s. The detour costs $2.6815$ rad and $3.142$ s, $0.198$ rad ($8.0\,\%$) and $0.785$ s ($33\,\%$) more than the blocked edge. A better via point is branch B's midpoint $(90°,-45°)$: its first leg's closest approach to the face is $0.235$ m, and the detour costs $2.5416$ rad, $2.3\,\%$ over, and exactly the straight edge's $2.356$ s, because the elbow — the joint that sets the time — still turns $135°$ in all.
> 3. The edge $q_h\to q_A$ keeps $\theta_1+\theta_2=90°$, so it is free, and at $1.1107$ rad it is the cheapest edge to any goal: A\* is right for the graph and the goal set it was given. The goal set is what is wrong — "tip at $(1,1)$" admits both branches, and the task wants the tool pointing at the face. Written as a task-space pose with the tool heading, $(1,1,0°)$, the goal has one configuration, $q_B$ ([[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2 §1.5]]'s task-space box makes the same point with a $45°$ heading). On $\{q_h,\ q_B\}$ the one edge is blocked, so A\* reports failure — a fact about a two-node graph, not about $\mathcal{C}_\mathrm{free}$, since the detour through $q_\mathrm{start}$ is free. That is resolution completeness read correctly (§5): failure on a discretisation proves nothing about the continuous problem, and adding one node gives A\* the detour.

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

*C군이고, 그 안에 있는 유일한 페이지다. [[04-robotics/modern-robotics/index|MR 챕터 요약]]과 최적화·RL 기초 위에 서며, 트랙 뒤쪽의 [[04-robotics/mpc|7. MPC]]가 §6을 이어서 전개한다.
실행 가능한 미래를 고르는 문제이며, I군이 이것을 비정형 환경으로 특수화한다.*

계획(planning)은 목표에 도달하기 위한 실행 가능한 미래 상태·행동 시퀀스를 고르는 문제다.
어려움은 짧은 경로 찾기가 아니다: 로봇 형상, 동역학, 접촉, 불확실성, 계산 시간, 변하는
관측이 실제로 실행할 수 있는 것을 제약한다.

> [!info] 깊이 목표
> 탐색·모션 플래닝·궤적 최적화·과제 계획·정책 학습·제어를 구분한다; feasibility와
> optimality 주장을 읽는다; 생성된 궤적이 충돌 없음·동역학적 실행 가능·폐루프 평가인지
> 판별한다.

> [!note] 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]](장치 P2. *장치*(plant)는 제어에서 제어 대상이 되는 시스템을 부르는 말이다) · [[02-foundations/optimization|최적화]] · [[02-foundations/rl-basics|RL 기초]] · [[04-robotics/modern-robotics/ch02-configuration-space|컨피규레이션 공간]] · [[04-robotics/modern-robotics/ch09-trajectory-generation|궤적 생성]](시간 스케일링) · [[04-robotics/state-estimation-slam|3. 상태 추정]](§7에서 쓰는 그 §4의 베이즈 필터). [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 모션 플래닝]]은 이 페이지의 회차 안에서, 계산 절을 마친 뒤 읽는다.

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 운동·과제 계획 층의 지도이고, "*저 패널을 프레임에 설치해*"의 여덟 단계 가운데 둘을 받친다 — 과제 계획으로 *작업을 분해하는* 단계(§7), 그리고 도구가 패널까지 가는 충돌 없고 값싼 경로를 찾아 *부재를 옮기는* 단계(§1–§6)다([[physical-ai-map|피지컬 AI 지도]]에서 계획 층의 학위논문 경로 위에 놓인 칩이다). 계획기가 말하는 "최적"과 "완전"은 그 계획기가 고른 척도와 이산화에 대한 주장이다. 계산 절의 시작 자세에서 P2는 역기구학(IK) 가지 둘로 패널 점에 닿는데, 관절 공간 길이로는 한쪽이 다른 쪽의 $\sqrt2$배이면서 max-norm으로는 정확히 동점이고 도구가 면을 향하는 것은 그중 하나뿐이며, $10$ cm 격자는 $5$ cm 틈을 두고 "경로 없음"을 보고할 수 있다(§5). 이 페이지의 회차 안에서 읽는 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]은 같은 두 목표 위에서 충돌 검사, 로드맵, 완전성 세 가지를 풀고, [[04-robotics/mpc|7. MPC]]는 §6을 이어 가며, 그 문제가 언제 볼록한지를 자기 §1에서 따지고, [[04-robotics/capstone-panel-contact|26. 캡스톤 §2]]는 추정한 위치의 불확실성만큼 부풀린 패널을 피해 계획하고, [[03-deep-learning/vla/index|딥러닝 4]]의 학습된 VLA(시각·언어 입력에서 행동을 내는 모델) 정책이 이 보장 가운데 무엇을 지키는지는 §8이 묻는다 — 학위논문 경로의 블록 2, 로보틱스 52–60회차이고, §8은 블록 4를 내다본다([[07-research-program/index|7. 연구 프로그램 §8]]). 이 페이지를 마치면 계획 논문을 제 계열에 놓고, 그 논문이 지키는 보장과 학습된 구성요소가 없애는 보장을 말하고, 그 논문의 "충돌 없음"과 "최적"이 자기 충돌 모델과 척도를 밝혔는지 확인할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분 회차 둘, 그다음 이 페이지 안에서 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]. **1회차:** 이 페이지의 대상과 그림, §1, 그리고 §2의 지도 요약까지 — 다섯 공간, 컨피규레이션 공간, 경로 계획 문제, 원판 로봇 예제. §2의 더 깊이 노트는 남겨 두고, 그림을 가린 채 원판 로봇의 네 중심을 $\mathcal{C}_{\text{obs}}$와 $\mathcal{C}_{\text{free}}$로 갈라 보며 마친다. **2회차:** §3과 §4를 읽고, 계산 절을 페이지를 가린 채 손으로 푼다 — 두 가지의 말단 경로와 $d(s)$, 관절 공간 길이와 max-norm으로 매긴 비용, 그리고 A\*가 돌려주는 답. 스스로 점검 2로 마친다. 그다음 같은 $q_A$와 $q_B$를 서로 잇는 MR 10장의 세 회차. Working 통과는 §5와 §5.5.1·§5.5.5, 이어서 §6–§7, §8–§9로 돌아와 스스로 점검과 과제로 끝나며, 과제의 팔은 가지 A의 중간에 멈춰 있다. 더 깊이 노트들 — §2의 지도 저장, §5.5의 Dubins·격자·kinodynamic 계획기, §6의 지역 계획기 — 은 내비게이션이나 차량 논문이 필요로 할 때 연다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그의 평면 2링크 팔이다. 링크는 $L_1=L_2=1$ m, 베이스는 원점이고, $\theta_1$은 $+x$축에서 재며 $\theta_2$는 링크 1에 대한 엘보 각이다. 그래서 엘보는 $(\cos\theta_1,\sin\theta_1)$에, 말단은 절대각 $\theta_1+\theta_2$ 방향으로 1 m 더 간 곳에 있다. 컨피규레이션 공간은 두 각이 모두 $\pm180°$에서 감기는 원환면 $T^2$다([[04-robotics/modern-robotics/ch02-configuration-space|MR 2장]]).

**패널**은 [[04-robotics/modern-robotics/ch02-configuration-space|MR 2장]]이 고정하고 [[04-robotics/modern-robotics/ch09-trajectory-generation|9장]], [[04-robotics/modern-robotics/ch10-motion-planning|10장]], [[04-robotics/capstone-panel-contact|26]]이 다시 쓰는 그것이다(26은 면을 도면상 $x=1.10$ m, 추정 $1.116$ m, 실제 $1.120$ m로 옮기고 $400$ N/m로 유연하게 장착한다). 강체 반평면 $x\ge1$ m이고, 그 면인 직선 $x=1$ 위에 과제 점 $p^\star=(1,1)$ m가 있다. 충돌 검사는 팔 전체를 패널에 대 보고, 관통만 충돌로 센다:

$$d(\theta)=\max\bigl(\cos\theta_1,\ \cos\theta_1+\cos(\theta_1+\theta_2)\bigr)-1,\qquad \mathcal{C}_{\text{free}}=\{\theta:\ d(\theta)\le0\}$$

링크의 $x$ 좌표는 두 끝 가운데 하나에서 가장 크므로 엘보와 말단만 검사하면 되기 때문이고(MR 10장의 1단계), 접촉 $d=0$은 과제가 접촉으로 끝나기 때문에 자유로 센다. 여기서 $d$는 패널 안에서 양수인 침투 깊이다. 이 검사가 정하는 C-장애물은 렌즈 $\cos\theta_1+\cos(\theta_1+\theta_2)>1$로, 원환면의 $18.478\,\%$다.

**질의와 척도.** 팔은 곧게 선 $q_\mathrm{start}=(90°,0°)$에서 출발하고, 그때 말단은 $(0,2)$, $d=-1$이다. 역기구학의 두 가지 $q_A=(0°,90°)$와 $q_B=(90°,-90°)$ 가운데 어느 쪽으로든 말단을 $p^\star$에 놓아야 한다 — MR 10장이 서로 잇는 바로 그 두 접촉 컨피규레이션이다. 간선은 $\mathcal{C}$의 직선 구간이고, 단계에서 따로 말하지 않으면 관절 공간 길이(rad)로 비용을 매긴다.

*범위: 이 페이지는 대상과 보장을 가르친다 — §1의 다섯 단어, §2의 공간들과 지도·비용 표현, §5의 완전성 네 강도, §5.5의 경로를 운전 불가능하게 만드는 제약들, §6의 궤적 최적화 문제 형태 — 그리고 논문을 어느 계열에 놓을지 판단할 만큼의 각 방법군. 어떤 알고리즘도 구현 깊이로는 가르치지 않는다. A\*의 증명과 코드는 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘 §6]]에 있다. 표본 기반 계획기는 여기서 조망하고 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]이 P2 위에서 손으로 풀지만 — RRT(rapidly-exploring random tree) 한 스텝과 노드 다섯짜리 로드맵 — 코드로 구현한 페이지는 없다. 후퇴 지평 제어는 [[04-robotics/mpc|7. MPC]], 정책 학습은 [[02-foundations/rl-basics|RL 기초]], 실제 내비게이션 스택 하나의 구체적 파라미터는 [[04-robotics/ros2/navigation-nav2|25.9 Nav2]]다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 330" style="max-width:100%;height:auto" role="img" aria-label="왼쪽은 작업 영역: 원점의 P2 베이스, x ≥ 1 쪽에 빗금을 친 패널 면 x = 1, 시작 자세(곧게 선 팔, 말단 (0, 2)), 링크 2가 면에 붙는 목표 A와 말단만 닿는 목표 B의 팔, 두 간선이 함께 그리는 (0, 1) 중심의 말단 사분원과 d = −0.293인 중간점 (0.707, 1.707), 간선 A의 엘보 호. 오른쪽은 (θ1, θ2) 원환면 도표: 칠한 C-장애물 렌즈, 시작 (90°, 0°), 렌즈 밖을 지나 A (0°, 90°)와 B (90°, −90°)로 가는 직선 간선, 렌즈 경계 위에 고리를 친 A와 B. 화살표 f 둘이 두 간선의 중간점을 작업 영역의 같은 점으로 보낸다.">
  <defs><marker id="aPDMk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="146" y="53.8" width="42" height="243.6" fill="currentColor" fill-opacity="0.07"/>
  <path d="M146 55.8 l 12 12 M146 67.8 l 12 12 M146 79.8 l 12 12 M146 91.8 l 12 12 M146 103.8 l 12 12 M146 115.8 l 12 12 M146 127.8 l 12 12 M146 139.8 l 12 12 M146 151.8 l 12 12 M146 163.8 l 12 12 M146 175.8 l 12 12 M146 187.8 l 12 12 M146 199.8 l 12 12 M146 211.8 l 12 12 M146 223.8 l 12 12 M146 235.8 l 12 12 M146 247.8 l 12 12 M146 259.8 l 12 12 M146 271.8 l 12 12 M146 283.8 l 12 12" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="146" y1="53.8" x2="146" y2="297.4" stroke="currentColor" stroke-width="1.3"/>
  <path d="M62 184 A84 84 0 0 1 146 268" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 3" stroke-opacity="0.75"/>
  <path d="M62 100 A84 84 0 0 1 146 184" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#aPDMk)"/>
  <g stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <polyline points="62,268 62,184 62,100" stroke-width="4" stroke-opacity="0.28"/>
    <polyline points="62,268 146,268 146,184" stroke-width="2.6"/>
    <polyline points="62,268 62,184 146,184" stroke-width="2.6" stroke-dasharray="7 3"/>
  </g>
  <circle cx="62" cy="268" r="4.5" fill="currentColor"/>
  <circle cx="62" cy="184" r="3.2" fill="currentColor"/>
  <circle cx="146" cy="268" r="3.2" fill="currentColor"/>
  <circle cx="62" cy="100" r="3.2" fill="currentColor" fill-opacity="0.45"/>
  <circle cx="146" cy="184" r="5.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="121.4" cy="124.6" r="2.6" fill="currentColor"/>
  <path d="M368 125 L368.5 120.1 L369 118.4 L369.5 117.2 L370 116.2 L370.5 115.5 L371 114.8 L371.5 114.2 L372 113.7 L372.5 113.3 L373 112.9 L373.5 112.5 L374 112.2 L374.5 111.9 L375 111.6 L375.5 111.4 L376 111.2 L376.5 111 L377 110.9 L377.5 110.7 L378 110.6 L378.5 110.5 L379 110.4 L379.5 110.3 L380 110.2 L380.5 110.1 L381 110.1 L381.5 110 L382 110 L382.5 110 L383 110 L383.5 110 L384 110 L384.5 110 L385 110.1 L385.5 110.1 L386 110.2 L386.5 110.2 L387 110.3 L387.5 110.4 L388 110.5 L388.5 110.6 L389 110.7 L389.5 110.8 L390 110.9 L390.5 111 L391 111.1 L391.5 111.3 L392 111.4 L392.5 111.6 L393 111.8 L393.5 111.9 L394 112.1 L394.5 112.3 L395 112.5 L395.5 112.7 L396 112.9 L396.5 113.1 L397 113.4 L397.5 113.6 L398 113.8 L398.5 114.1 L399 114.4 L399.5 114.6 L400 114.9 L400.5 115.2 L401 115.5 L401.5 115.8 L402 116.1 L402.5 116.4 L403 116.7 L403.5 117.1 L404 117.4 L404.5 117.8 L405 118.1 L405.5 118.5 L406 118.9 L406.5 119.2 L407 119.6 L407.5 120 L408 120.4 L408.5 120.9 L409 121.3 L409.5 121.7 L410 122.2 L410.5 122.6 L411 123.1 L411.5 123.5 L412 124 L412.5 124.5 L413 125 L413.5 125.5 L414 126 L414.5 126.5 L415 127.1 L415.5 127.6 L416 128.2 L416.5 128.7 L417 129.3 L417.5 129.9 L418 130.4 L418.5 131 L419 131.6 L419.5 132.2 L420 132.9 L420.5 133.5 L421 134.1 L421.5 134.8 L422 135.4 L422.5 136.1 L423 136.7 L423.5 137.4 L424 138.1 L424.5 138.8 L425 139.5 L425.5 140.2 L426 140.9 L426.5 141.6 L427 142.4 L427.5 143.1 L428 143.8 L428.5 144.6 L429 145.4 L429.5 146.1 L430 146.9 L430.5 147.7 L431 148.5 L431.5 149.3 L432 150.1 L432.5 150.9 L433 151.8 L433.5 152.6 L434 153.4 L434.5 154.3 L435 155.1 L435.5 156 L436 156.9 L436.5 157.8 L437 158.7 L437.5 159.6 L438 160.5 L438.5 161.4 L439 162.3 L439.5 163.2 L440 164.2 L440.5 165.1 L441 166.1 L441.5 167 L442 168 L442.5 169 L443 170 L443.5 171 L444 172 L444.5 173 L445 174.1 L445.5 175.1 L446 176.2 L446.5 177.3 L447 178.4 L447.5 179.5 L448 180.6 L448.5 181.7 L449 182.9 L449.5 184 L450 185.2 L450.5 186.4 L451 187.6 L451.5 188.9 L452 190.2 L452.5 191.5 L453 192.9 L453.5 194.3 L454 195.7 L454.5 197.2 L455 198.8 L455.5 200.5 L456 202.2 L456.5 204.2 L457 206.4 L457.5 209.1 L458 215 L458 215 L457.5 219.9 L457 221.6 L456.5 222.8 L456 223.8 L455.5 224.5 L455 225.2 L454.5 225.8 L454 226.3 L453.5 226.7 L453 227.1 L452.5 227.5 L452 227.8 L451.5 228.1 L451 228.4 L450.5 228.6 L450 228.8 L449.5 229 L449 229.1 L448.5 229.3 L448 229.4 L447.5 229.5 L447 229.6 L446.5 229.7 L446 229.8 L445.5 229.9 L445 229.9 L444.5 230 L444 230 L443.5 230 L443 230 L442.5 230 L442 230 L441.5 230 L441 229.9 L440.5 229.9 L440 229.8 L439.5 229.8 L439 229.7 L438.5 229.6 L438 229.5 L437.5 229.4 L437 229.3 L436.5 229.2 L436 229.1 L435.5 229 L435 228.9 L434.5 228.7 L434 228.6 L433.5 228.4 L433 228.2 L432.5 228.1 L432 227.9 L431.5 227.7 L431 227.5 L430.5 227.3 L430 227.1 L429.5 226.9 L429 226.6 L428.5 226.4 L428 226.2 L427.5 225.9 L427 225.6 L426.5 225.4 L426 225.1 L425.5 224.8 L425 224.5 L424.5 224.2 L424 223.9 L423.5 223.6 L423 223.3 L422.5 222.9 L422 222.6 L421.5 222.2 L421 221.9 L420.5 221.5 L420 221.1 L419.5 220.8 L419 220.4 L418.5 220 L418 219.6 L417.5 219.1 L417 218.7 L416.5 218.3 L416 217.8 L415.5 217.4 L415 216.9 L414.5 216.5 L414 216 L413.5 215.5 L413 215 L412.5 214.5 L412 214 L411.5 213.5 L411 212.9 L410.5 212.4 L410 211.8 L409.5 211.3 L409 210.7 L408.5 210.1 L408 209.6 L407.5 209 L407 208.4 L406.5 207.8 L406 207.1 L405.5 206.5 L405 205.9 L404.5 205.2 L404 204.6 L403.5 203.9 L403 203.3 L402.5 202.6 L402 201.9 L401.5 201.2 L401 200.5 L400.5 199.8 L400 199.1 L399.5 198.4 L399 197.6 L398.5 196.9 L398 196.2 L397.5 195.4 L397 194.6 L396.5 193.9 L396 193.1 L395.5 192.3 L395 191.5 L394.5 190.7 L394 189.9 L393.5 189.1 L393 188.2 L392.5 187.4 L392 186.6 L391.5 185.7 L391 184.9 L390.5 184 L390 183.1 L389.5 182.2 L389 181.3 L388.5 180.4 L388 179.5 L387.5 178.6 L387 177.7 L386.5 176.8 L386 175.8 L385.5 174.9 L385 173.9 L384.5 173 L384 172 L383.5 171 L383 170 L382.5 169 L382 168 L381.5 167 L381 165.9 L380.5 164.9 L380 163.8 L379.5 162.7 L379 161.6 L378.5 160.5 L378 159.4 L377.5 158.3 L377 157.1 L376.5 156 L376 154.8 L375.5 153.6 L375 152.4 L374.5 151.1 L374 149.8 L373.5 148.5 L373 147.1 L372.5 145.7 L372 144.3 L371.5 142.8 L371 141.2 L370.5 139.5 L370 137.8 L369.5 135.8 L369 133.6 L368.5 130.9 L368 125 Z" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1" stroke-opacity="0.75"/>
  <rect x="323" y="80" width="180" height="180" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <path d="M319 226 L323 220 L327 226 M499 226 L503 220 L507 226 M457 76 L463 80 L457 84 M463 76 L469 80 L463 84 M457 256 L463 260 L457 264 M463 256 L469 260 L463 264" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6"><line x1="323" y1="260" x2="323" y2="264"/><line x1="319" y1="260" x2="323" y2="260"/><line x1="368" y1="260" x2="368" y2="264"/><line x1="319" y1="215" x2="323" y2="215"/><line x1="413" y1="260" x2="413" y2="264"/><line x1="319" y1="170" x2="323" y2="170"/><line x1="458" y1="260" x2="458" y2="264"/><line x1="319" y1="125" x2="323" y2="125"/><line x1="503" y1="260" x2="503" y2="264"/><line x1="319" y1="80" x2="323" y2="80"/></g>
  <line x1="458" y1="170" x2="413" y2="125" stroke="currentColor" stroke-width="2.2"/>
  <line x1="458" y1="170" x2="458" y2="215" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <circle cx="458" cy="170" r="4" fill="currentColor"/>
  <circle cx="413" cy="125" r="3" fill="currentColor"/>
  <circle cx="413" cy="125" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="458" cy="215" r="3" fill="currentColor"/>
  <circle cx="458" cy="215" r="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="435.5" cy="147.5" r="2.4" fill="currentColor"/>
  <circle cx="458" cy="192.5" r="2.4" fill="currentColor"/>
  <path d="M431.5 146.5 C 315.5 125.5 271.4 100.6 128.4 123.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" marker-end="url(#aPDMk)"/>
  <path d="M454 192.5 C 298 214.5 296.4 164.6 127.4 127.6" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" stroke-dasharray="4 2" marker-end="url(#aPDMk)"/>
  <g fill="currentColor">
    <text x="10" y="20" font-size="12">작업 영역 (m)</text>
    <text x="323" y="20" font-size="12">컨피규레이션 공간 C = T² (도)</text>
    <text x="150" y="47.8" font-size="11">패널 x ≥ 1</text>
    <text x="54" y="272" font-size="11" text-anchor="end">베이스</text>
    <text x="54" y="104" font-size="11" text-anchor="end" opacity="0.85">시작 (0, 2)</text>
    <text x="139" y="261" font-size="12" text-anchor="end" font-weight="bold">A</text>
    <text x="54" y="188" font-size="12" text-anchor="end" font-weight="bold">B</text>
    <text x="138" y="175" font-size="11" text-anchor="end">p* = (1, 1)</text>
    <text x="117.4" y="142.6" font-size="10" text-anchor="end">d = −0.293</text>
    <text x="78.8" y="78.2" font-size="10" opacity="0.9">말단 경로,</text>
    <text x="78.8" y="90.2" font-size="10" opacity="0.9">두 간선 공통</text>
    <text x="70.4" y="224.3" font-size="10" opacity="0.85">간선 A의</text>
    <text x="70.4" y="236.3" font-size="10" opacity="0.85">엘보</text>
    <text x="466" y="174" font-size="11">시작</text>
    <text x="466" y="187" font-size="10">(90°, 0°)</text>
    <text x="421" y="117" font-size="11">A (0°, 90°)</text>
    <text x="467" y="219" font-size="11" font-weight="bold">B</text>
    <text x="467" y="232" font-size="10">(90°, −90°)</text>
    <text x="411" y="166" font-size="11" text-anchor="middle">C-장애물</text>
    <text x="411" y="179" font-size="11" text-anchor="middle">d > 0</text>
    <text x="323" y="275" font-size="10" text-anchor="middle">−180°</text>
    <text x="317" y="264" font-size="10" text-anchor="end">−180°</text>
    <text x="413" y="275" font-size="10" text-anchor="middle">0°</text>
    <text x="317" y="174" font-size="10" text-anchor="end">0°</text>
    <text x="503" y="275" font-size="10" text-anchor="middle">180°</text>
    <text x="317" y="84" font-size="10" text-anchor="end">180°</text>
    <text x="458" y="275" font-size="12" text-anchor="middle">θ<tspan dy="3" font-size="10">1</tspan></text>
    <text x="305" y="104" font-size="12" text-anchor="middle">θ<tspan dy="3" font-size="10">2</tspan></text>
    <text x="323" y="292" font-size="10" opacity="0.85">마주 보는 변은 붙어 있다</text>
    <text x="323" y="306" font-size="10" opacity="0.85">고리: 접촉, d = 0, 자유</text>
    <text x="246" y="111" font-size="12" text-anchor="middle" font-style="italic">f</text>
  </g>
</svg>

패널 $x\ge1$ 앞의 P2로, 두 칸 모두에서 가지 A는 실선, 가지 B는 점선으로 그렸다. 왼쪽 작업 영역: 말단이 $(0,2)$에 있는 곧게 선 시작 자세에서, 팔은 링크 2가 면에 붙는 $q_A=(0°,90°)$나 말단만 닿는 $q_B=(90°,-90°)$로 $p^\star=(1,1)$에 닿고, 두 직선 간선은 모두 말단을 $(0,1)$ 중심의 같은 사분원을 따라 옮기며 그 중간점 $(0.707,1.707)$은 면에서 $0.293$ m 떨어져 있다. 오른쪽은 C-장애물 렌즈를 칠한 원환면 $\mathcal{C}=T^2$로, 두 간선은 서로 다른 선분이면서 둘 다 렌즈 밖에 머물다 목표에서만 렌즈에 닿고 — 자유로 세는 접촉이다 — 비용은 $q_A$까지 $\pi/\sqrt2=2.2214$ rad, $q_B$까지 $\pi/2=1.5708$ rad이며, 순기구학 화살표 $f$ 둘이 두 중간점을 작업 영역의 한 점으로 보낸다.

### 1. 계획·경로·궤적·정책·제어기

문헌은 로봇이 할 일을 가리키는 다섯 단어를 거의 섞어 쓰고, 그래서 한 단어에 대한 주장이 다른 단어에 대한 주장으로 읽히는 일이 잦다. 가장 중요한 구분은 계획과 정책이다. 계획은 한 시작점에 대한 답 하나이고, 정책은 만날 수 있는 모든 상태에 대한 답이다.

| 용어 | 의미 |
|---|---|
| 계획(plan) | 미래 결정·행동의 제안된 시퀀스 |
| 경로(path) | 시간 없는 기하학적 곡선 |
| 궤적(trajectory) | 시간이 매겨진 상태·속도·(대개) 입력 |
| 정책(policy) | 가용 정보를 행동으로 사상하는 규칙 |
| 제어기(controller) | 기준을 추종하거나 거동을 조절하는 피드백 시스템 |

계획기가 경로를 내면 궤적 생성기가 시간을 매기고([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]
— 시간 스케일링, 경유점, 시간 최적 스케일링) 제어기가 추종한다. 계획은 작업 공간에 있는데
로봇은 관절 공간으로 명령받는다면 그 사이에
[[04-robotics/modern-robotics/ch06-inverse-kinematics|역기구학(MR 6장)]]이 앉고, 그 다봉성은
축소판 계획 문제다. 학습 시스템에서는 정책이 이 경계들을 합칠 수 있지만, 물리적 요구 사항이
사라지는 것은 아니다.

**다섯 가지를 수학적 대상으로 쓰면.** $\mathcal{C}$는 컨피규레이션 공간, 곧 로봇의 모든 점의 위치를 정하는 숫자 목록인 컨피규레이션 $q$ 전체의 집합이다(P2라면 관절각 쌍 $(\theta_1,\theta_2)$). $\mathcal{X}$는 상태 공간, 곧 컨피규레이션과 그 속도를 함께 쓴 $x=(q,\dot q)$의 집합이고, $\mathcal{U}$는 입력 공간, 곧 구동기가 받아들이는 명령의 집합이다. 셋의 완전한 정의는 §2에 있다.

- **경로**는 정규화된 매개변수 $s$에서 컨피규레이션으로 가는 연속 사상이고, 양 끝이 고정되어 있다. 매개변수는 시간이 아니므로 경로는 *어디로*만 말한다.
$$\sigma:[0,1]\to\mathcal{C},\qquad \sigma(0)=q_{\text{start}},\quad \sigma(1)=q_{\text{goal}}$$
- **궤적**은 시간을 더한다: 지속 시간 $T$ 동안 상태와 (대개) 입력을 시간의 함수로 준다. 모든 궤적은 경로 하나를 그리지만, 경로 하나에는 궤적이 무한히 많다. $s(0)=0$, $s(T)=1$인 증가하는 시간 스케일링 $s(t)$마다 다른 궤적이 나오기 때문이다([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]).
$$x:[0,T]\to\mathcal{X},\qquad u:[0,T]\to\mathcal{U}$$
- **계획**은 실행 *전에* 한 시작 상태에 대해 계산한 결정의 유한 열 $(a_0,\dots,a_{K-1})$이다. 기호적 행동일 수도, 웨이포인트나 입력일 수도 있다.
- **정책**은 실행 *중에* 평가하는 규칙이다. 가용 정보 $I_t$(상태, 관측 이력, belief)를 행동 $a_t=\pi(I_t)$ 또는 분포 $\pi(a_t\mid I_t)$로 사상한다([[02-foundations/rl-basics|RL 기초 §1]]).
- **제어기**는 측정 상태와 기준으로부터 구동기 명령을 계산하는, 대개 빠른 피드백 법칙 $u_t=\kappa(x_t,\,x^{\text{ref}}_t)$이다.

예: $(0,0)$에서 $(1,0)$ m까지의 직선 구간은 경로 하나다. 이를 일정한 0.5 m/s로 달리면 $T=2$ s인 궤적이고, 1 m/s로 달리면 같은 경로 위의 다른 궤적($T=1$ s)이다. **비예:** 시각이 없는 웨이포인트 목록은 경로나 계획이지 궤적이 아니다. 그래서 무언가가 시간을 매겨 주기 전에는 속도·가속도 한계에 비추어 검사할 수 없다.

### 2. 공간과 제약

*한 문장으로:* 계획기가 탐색을 시작하기 전에, 문제는 올바른 공간 — 방이 아니라 로봇의 관절각 — 에 적혀 있어야 하고, 지도는 비용과 미지의 칸이 표시된 채 계획기가 읽을 수 있는 꼴로 저장되어 있어야 한다.

*이 절에서 하나만 가져간다면:* C-장애물은 방의 한 영역이 아니라 컨피규레이션의 집합이다. 아래 원판 로봇 예에서 비어 있는 점 $(0.6,1.5)$ m가 $\mathcal{C}_{\text{obs}}$ 안에 드는 것은, 그곳에 중심을 둔 로봇이 사각형과 겹치기 때문이다.

#### 다섯 공간, 그리고 컨피규레이션 공간의 정의

- **작업 영역(workspace):** 로봇과 장애물이 차지하는 물리적 위치.
- **컨피규레이션 공간:** 로봇 컨피규레이션; 장애물은 금지 영역이 된다.
- **상태 공간:** 컨피규레이션 + 속도 같은 변수.
- **행동/입력 공간:** 시스템이 쓸 수 있는 명령.
- **작업 공간(task space):** 말단 자세처럼 과제에 직접 묶인 변수.

작업 영역에서 충돌이 없다는 것이 관절·토크·속도·안정성·접촉의 실행 가능성을 함의하지
않는다.

**컨피규레이션 공간의 정의.** **컨피규레이션** $q$는 로봇의 모든 점의 위치를 지정한 것이다. 조건이 둘이다. **완전**해야 한다 — 위치가 정해지지 않는 몸체의 점이 없어야 한다. 그리고 **최소**여야 한다 — 더 짧은 수의 목록으로 같은 일을 할 수 없어야 한다. **컨피규레이션 공간** $\mathcal{C}$는 모든 컨피규레이션의 집합이고, 차원이 자유도 수가 되는 것은 이 최소성 때문이다:

$$\mathcal{C}=\{\,q:q\ \text{는 로봇의 모든 점을 지정한다}\,\},\qquad \dim\mathcal{C}=\text{dof}$$

개수보다 집합이 중요하다. $\mathcal{C}$는 대개 상자가 아니기 때문이다. 평면 2R 팔의 것은 직사각형 $[0,2\pi)^2$가 아니라 원환면 $T^2$다. 관절각이 각각 한 바퀴 돌아 붙기 때문이다 — 그래서 $359°$와 $1°$를 멀다고 보는 계획기는 틀린 공간을 쓰고 있는 것이다. **비예:** 도구의 자세는 그것을 주는 관절 벡터가 둘 이상이면 컨피규레이션이 *아니다* — 여유 자유도를 가진 팔의 자세가 그렇고, 두 컨피규레이션이 만드는 P2의 말단 위치 $(1,1)$도 그렇다(계산 절의 1단계). 그때는 몸체의 점들이 정해지지 않기 때문이다. 그것은 위 목록의 마지막 항목인 작업 공간이다.

$\mathcal{C}$는 **C-장애물** $\mathcal{C}_{\text{obs}}$와 **자유 공간** $\mathcal{C}_{\text{free}}=\mathcal{C}\setminus\mathcal{C}_{\text{obs}}$로 나뉜다. 둘 다 [[04-robotics/modern-robotics/ch02-configuration-space|MR 2장 §2]]에서 정의되고 장치 **P2** 위에서 유도되며 예와 비예까지 붙어 있다. 이 페이지는 다시 쓰지 않고 가져다 쓴다. 이 페이지의 대상인 패널에서 C-장애물은 렌즈 $\cos\theta_1+\cos(\theta_1+\theta_2)>1$이고, 그 소속을 가르는 충돌 검사 — 계획기가 세계에 대해 배우는 유일한 통로 — 는 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 §2]]가 정의한다. 그 정의의 두 귀결이 이 페이지의 나머지가 딛고 선 것이다. C-장애물은 *컨피규레이션*의 집합이지 결코 작업 영역의 영역이 아니라는 것, 그리고 이 구성이 모양을 가진 로봇을 $\mathcal{C}_{\text{free}}$ 안을 움직이는 *점*으로 줄인다는 것 — 아래의 모든 계획기가 쓰인 형태가 그것이다.

그러면 **경로 계획 문제**는 이렇다: $q_{\text{start}},q_{\text{goal}}\in\mathcal{C}_{\text{free}}$가 주어졌을 때 모든 $s\in[0,1]$에서 $\sigma(s)\in\mathcal{C}_{\text{free}}$인 경로 $\sigma$(§1)를 찾거나, 없다고 보고한다. [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 §1]]은 이것을 정의로 쓰고, P2의 질의 $A\to B$를 예로, 중간점에서 $\mathcal{C}_{\text{free}}$를 벗어나는 곧은 엘보 뒤집기를 비예로 든다. **상태 공간** $\mathcal{X}$는 속도를 더한 $x=(q,\dot q)$이므로 자유도 $n$인 로봇의 상태는 $2n$차원이다. **입력 공간** $\mathcal{U}$는 허용되는 명령의 집합이다. 예를 들어 구동기마다 $|u_i|\le u_{\max}$다. 작업 영역과 작업 공간은 물리적 위치나 자세의 집합이고 $\mathcal{C}$는 로봇 컨피규레이션의 집합이다. 아래 그림에 칸이 두 개 필요한 이유다.

> [!example] 계산 예제 · Worked example
> MR 2장은 *팔*의 C-장애물을 유도한다. 거기서는 원환면 위의 휘어진 렌즈다. 여기서는 다른 쪽 경우, 아래의 격자 팽창이 기대고 있는 경우를 본다. 회전하지 않고 평행이동만 하는 반경 0.5 m 원판 로봇의 컨피규레이션은 중심 $q=(x,y)$이므로 $\mathcal{C}=\mathbb{R}^2$다. 정사각형 장애물 $[1,2]\times[1,2]$ m가 있으면, 중심이 정사각형에서 0.5 m보다 가까울 때 정확히 $q\in\mathcal{C}_{\text{obs}}$다. $q=(0.6,1.5)$는 0.4 m 떨어져 있으므로, 작업 영역의 *점* $(0.6,1.5)$는 비어 있는데도 $\mathcal{C}_{\text{obs}}$에 속한다. $q=(0.4,1.5)$는 0.6 m 떨어져 있어 자유다.
>
> **비예:** C-장애물은 정사각형을 상자 $[0.5,2.5]^2$로 키운 것이 아니다. 정사각형과 원판의 민코프스키 합이라 모서리가 둥글다. 그래서 그 상자 안의 $q=(0.6,0.6)$은 모서리 $(1,1)$에서 0.566 m라 자유이고, 0.424 m인 $(0.7,0.7)$은 자유가 아니다. 이것이 아래 목록의 팽창이며, 로봇이 원판이기 때문에만 정확하다.

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="왼쪽은 작업 영역: 사각형 장애물 [1, 2]² m와 반지름 0.5 m 원판 로봇. 중심이 (0.6, 1.5)이면 사각형과 겹치고, (0.6, 0.6)이면 모서리에서 0.066 m 떨어진다. 오른쪽은 중심의 컨피규레이션 공간: C-장애물은 사각형을 0.5 m 키우되 모서리가 사분원인 모양이지 점선 상자 [0.5, 2.5]²가 아니다. 중심 (0.6, 1.5)와 (0.7, 0.7)은 사각형에서 0.40, 0.424 m라 그 안에, (0.4, 1.5)와 (0.6, 0.6)은 0.60, 0.566 m라 자유에 있다.">
  <g stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55"><line x1="12" y1="282" x2="228.6" y2="282"/><line x1="12" y1="282" x2="12" y2="76.8"/><line x1="27.2" y1="282" x2="27.2" y2="286"/><line x1="8" y1="282" x2="12" y2="282"/><line x1="103.2" y1="282" x2="103.2" y2="286"/><line x1="8" y1="206" x2="12" y2="206"/><line x1="179.2" y1="282" x2="179.2" y2="286"/><line x1="8" y1="130" x2="12" y2="130"/></g>
  <g stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55"><line x1="250" y1="279" x2="545" y2="279"/><line x1="250" y1="279" x2="250" y2="24"/><line x1="280" y1="279" x2="280" y2="283"/><line x1="380" y1="279" x2="380" y2="283"/><line x1="246" y1="194" x2="250" y2="194"/><line x1="480" y1="279" x2="480" y2="283"/><line x1="246" y1="94" x2="250" y2="94"/></g>
  <rect x="103.2" y="130" width="76" height="76" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="72.8" cy="168" r="38" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="72.8" cy="168" r="2.4" fill="currentColor"/>
  <circle cx="72.8" cy="236.4" r="38" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 3"/>
  <circle cx="72.8" cy="236.4" r="2.4" fill="currentColor"/>
  <path d="M103.2 145.2 A38 38 0 0 1 103.2 190.8 Z" fill="currentColor" fill-opacity="0.6"/>
  <path d="M380 244 L480 244 A50 50 0 0 0 530 194 L530 94 A50 50 0 0 0 480 44 L380 44 A50 50 0 0 0 330 94 L330 194 A50 50 0 0 0 380 244 Z" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.2"/>
  <rect x="330" y="44" width="200" height="200" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <rect x="380" y="94" width="100" height="100" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55"/>
  <line x1="380" y1="194" x2="340" y2="234" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.75"/>
  <circle cx="380" cy="194" r="1.8" fill="currentColor"/>
  <circle cx="340" cy="144" r="3" fill="currentColor"/>
  <circle cx="320" cy="144" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="340" cy="234" r="3.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="350" cy="224" r="3" fill="currentColor"/>
  <g fill="currentColor">
    <text x="12" y="16" font-size="12">작업 영역 (m)</text>
    <text x="250" y="16" font-size="12">컨피규레이션 공간: 중심 (m)</text>
    <text x="27.2" y="297" font-size="10" text-anchor="middle">0</text>
    <text x="6" y="286" font-size="10" text-anchor="end">0</text>
    <text x="103.2" y="297" font-size="10" text-anchor="middle">1</text>
    <text x="6" y="210" font-size="10" text-anchor="end">1</text>
    <text x="179.2" y="297" font-size="10" text-anchor="middle">2</text>
    <text x="6" y="134" font-size="10" text-anchor="end">2</text>
    <text x="280" y="294" font-size="10" text-anchor="middle">0</text>
    <text x="380" y="294" font-size="10" text-anchor="middle">1</text>
    <text x="244" y="198" font-size="10" text-anchor="end">1</text>
    <text x="480" y="294" font-size="10" text-anchor="middle">2</text>
    <text x="244" y="98" font-size="10" text-anchor="end">2</text>
    <text x="141.2" y="162.9" font-size="11" text-anchor="middle">장애물</text>
    <text x="110.5" y="194.8" font-size="10">겹침</text>
    <text x="72.8" y="123.9" font-size="10" text-anchor="middle">로봇, r = 0.5</text>
    <text x="72.8" y="183" font-size="10" text-anchor="middle">(0.6, 1.5)</text>
    <text x="72.8" y="251.4" font-size="10" text-anchor="middle">(0.6, 0.6)</text>
    <text x="112.2" y="221.6" font-size="10">0.066 떨어짐</text>
    <text x="430" y="122" font-size="11" text-anchor="middle">C-장애물</text>
    <text x="430" y="148" font-size="10" text-anchor="middle" opacity="0.8">사각형</text>
    <text x="530" y="259" font-size="10" text-anchor="end" opacity="0.9">상자 [0.5, 2.5]²</text>
    <text x="347" y="148" font-size="10">안 0.40</text>
    <text x="313" y="148" font-size="10" text-anchor="end">자유 0.60</text>
    <text x="357" y="233" font-size="10">안 0.424</text>
    <text x="334" y="255" font-size="10" text-anchor="end">자유 0.566</text>
  </g>
</svg>

위 예제를 축척대로 그렸다. 왼쪽은 방: 중심이 $(0.6,1.5)$인 원판 로봇은 중심 자리가 빈 바닥인데도 사각형과 겹치고, 중심이 $(0.6,0.6)$이면 모서리 $(1,1)$을 $0.066$ m 차이로 비켜 간다. 오른쪽은 같은 네 중심을 $\mathcal{C}$의 점으로 찍은 것이다. C-장애물은 사각형을 $0.5$ m 키우되 모서리가 사분원인 모양이지 점선 상자가 아니어서, 사각형에서 $0.40$, $0.424$ m인 $(0.6,1.5)$와 $(0.7,0.7)$은 그 안에, $0.60$, $0.566$ m인 $(0.4,1.5)$와 $(0.6,0.6)$은 자유에 있다.

#### 지도를 저장하는 방식: 격자, 비용, 프런티어

감지만 해 본 공간에서 계획하는 로봇은 그 공간을 격자로 저장하고, 내비게이션 논문은 그 격자에 관한 다섯 가지를 안다고 가정한다:

- **점유 격자(occupancy grid):** 칸마다 그 칸이 점유되어 있을 확률을 담는 격자이고, 새 판독의 증거를 로그 승산으로 더해 갱신한다.
- **미지는 비어 있음이 아니다:** 칸은 비어 있음·점유됨·미지 중 하나로 읽히고, 미지를 비어 있음으로 다루는 것이 탐색이 바로잡으려고 존재하는 초심자의 오류다.
- **팽창(inflation):** 점유 칸을 모두 로봇 반경만큼 키우면 격자가 원판 로봇의 C-장애물이 된다 — 위 예제대로 정확히 — 그리고 다른 모양의 footprint에서는 근사일 뿐이다.
- **비용 지도(costmap):** 칸이 예/아니오 대신 통행 비용을 담는 격자라서, 벽에서 떨어지라는 선호 같은 것이 계획기가 탐색할 수 있는 기하가 된다.
- **프런티어(frontier):** 미지 칸과 이웃한, 비어 있다고 알려진 칸. 가장 가까운 프런티어로 가기를 프런티어가 남지 않을 때까지 되풀이하는 것이 고전적 탐색이다.

더 깊이 노트는 이 다섯을 하나씩 풀어 쓴다 — OctoMap의 숫자로 쓴 로그 승산 갱신, 팽창 비용과 그 반경 셋, 계층형 비용 지도, 그리고 의미 내비게이션이 프런티어를 쓰는 방식. 내비게이션 논문이 필요로 할 때 연다.

> [!note]- 더 깊이 · Deeper
> 이 위키의 여러 페이지가 점유·비용 표현을 위해 여기로 오므로, 시스템 논문의 부록이 아니라 이 절에 둔다.
>
> **점유 격자와 로그 승산.** 지도를 격자로 두고 각 칸이 점유되어 있을 확률을 담는다. 갱신은 **로그 승산(log-odds)** $\ell=\log\frac{p}{1-p}$ 으로 한다. 이 값은 $p=0.5$를 $0$으로, $p\to 0$이나 $1$을 $\mp\infty$로 보낸다. 베이즈 규칙은 칸의 승산 $p/(1-p)$에 새 측정마다 우도비를 곱하므로, 로그를 취하면 증거 누적이 곱셈이 아니라 덧셈이 된다(OctoMap의 $+0.85$는 $\log(0.7/0.3)$, 즉 $p=0.7$짜리 "적중" 하나다). 또한 확률이 0이나 1에 바짝 붙었을 때의 수치 문제를 피할 수 있다. 남는 위험의 방향을 짚어야 한다: 로그 승산은 *유계가 아니어서*, 점유로 천 번 관측된 칸은 뒤집으려면 반대 관측이 천 번 단위로 필요하다(OctoMap 기본 로그 승산 증분 +0.85/−0.4이면 약 2,100번) — 그래서 구현들은 명시적 **클램핑** 범위를 둔다(Yguel 외 2007이 제안하고 OctoMap이 채택). 세상이 바뀌었을 때 지도가 적응할 수 있게 하려는 것이다. 칸은 *비어 있음*, *점유됨*, 그리고 **미지**의 셋 중 하나이고, 초심자가 빠뜨리는 것이 셋째다. 미지는 비어 있음이 아니며, 그 차이가 곧 탐색이 존재하는 이유다.
>
> **갱신 식.** $m_i=1$을 "칸 $i$가 점유됨", $p_0$을 사전 점유 확률이라 하자. 판독 $z_t$마다 자기 증거를 더하고, 사전 확률은 판독마다 다시 세지 않도록 한 번 뺀다:
> $$\ell_t(i)=\ell_{t-1}(i)+\log\frac{p(m_i=1\mid z_t)}{1-p(m_i=1\mid z_t)}-\log\frac{p_0}{1-p_0},\qquad p=1-\frac{1}{1+e^{\ell}}$$
> 가운데 항은 **역센서 모델**(inverse sensor model), 즉 이 판독 하나만으로 본 점유 확률이고, 둘째 식은 로그 승산을 확률로 되돌린다. $p_0=0.5$이면 사전 항은 $0$이다. 그러면 OctoMap 적중 두 번은 $\ell=1.70$, $p=0.846$을 주고, 그 뒤 빗나감 한 번($-0.4$)은 $\ell=1.30$, $p=0.786$을 준다. 클램핑은 매 갱신 뒤 $\ell$을 구간 $[\ell_{\min},\ell_{\max}]$ 안에 가둔다.
>
> **팽창.** 로봇을 점으로 다루는 계획기(위 그림)는 대신 장애물을 키워야 한다. 점유 칸을 로봇 반경만큼 팽창시키면 **원형 로봇에 한해** 격자 위에서 바로 C-공간 장애물이 된다 — 다른 형상에서는 근사이고, 그래서 Nav2 같은 스택은 별도의 footprint 충돌 검사를 따로 돌린다. 그 바깥에 감쇠하는 비용을 더하면 계획기가 들어가기를 꺼리는 여유가 생긴다. 칸에서 가장 가까운 장애물 칸까지의 거리 $d$, 내접 로봇 반경 $r$, 감쇠율 $\alpha>0$에 대해 ROS costmap은 지수 함수를 쓴다:
> $$c(d)=\begin{cases}c_{\text{lethal}} & d=0\\ c_{\text{insc}} & 0<d\le r\\ c_{\text{insc}}\,e^{-\alpha(d-r)} & r<d\le d_{\text{infl}}\\ 0 & d>d_{\text{infl}}\end{cases}$$
> 내접 반경 안의 칸은 로봇 중심을 거기 두면 반드시 충돌한다는 뜻이고, 그 바깥에서 비용은 거리에 따라 감쇠하며, 팽창 반경 $d_{\text{infl}}$ 너머의 칸은 비용이 없다. $\alpha=3$ /m이면 내접 반경에서 0.2 m 바깥 칸의 비용은 내접값의 $e^{-0.6}=0.55$배다. $\alpha$를 키우면 여유가 좁아진다.
>
> **반경이 셋이고, 셋은 같은 수가 아니다.** footprint에는 **내접 반경** $r_{\text{insc}}$ — 로봇 원점을 중심으로 그 안에 *들어가는* 가장 큰 원의 반경 — 과 **외접 반경** $r_{\text{circ}}$ — footprint를 *담는* 가장 작은 원 — 이 있다. 장애물에서 $r_{\text{insc}}$ 안이면 어느 방향으로 서 있든 충돌이고, $r_{\text{circ}}$ 밖이면 어느 방향으로 서 있든 안전하며, 그 사이에서는 충돌 여부가 방향에 달려 있다. footprint 검사가 존재하는 이유가 바로 그 띠다. **팽창 반경** $d_{\text{infl}}$은 아예 세 번째 것이다. 감쇠 비용을 0으로 자르는 거리다. 이것은 *선호* 손잡이이지 안전 여유가 아니다 — 안전을 담당하는 것은 $d_{\text{infl}}$이 아니라 footprint에서 나오는 $r_{\text{insc}}$다. **비예, 그리고 이 생태계에서 가장 흔한 오설정:** `inflation_radius`를 "벽에서 이만큼 떨어뜨려라"로 읽는 것([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §5]]). $r_{\text{insc}}=0.30$ m, $\alpha=3$ /m, $d_{\text{infl}}=1.00$ m에 ROS의 바이트 척도(장애물 칸 자체가 $c_{\text{lethal}}=254$, $c_{\text{insc}}=253$, 치맛자락은 $252$로 스케일)를 쓰면 비용은 $d=0.50$ m에서 $252\,e^{-0.6}=138$, $0.80$ m에서 $56$, $1.00$ m 바로 안쪽에서 $30$ — 그리고 바로 바깥에서 $0$이다. $d_{\text{infl}}$에서의 이 30짜리 단차가 **비용 절벽**이다. 감쇠는 매끄럽게 0으로 사라지라고 둔 것인데, 비용을 따라 내려가는 계획기는 거기서 그 대신 단차를 만난다. 그러므로 잘리는 값이 충분히 작아지도록 $d_{\text{infl}}$을 크게 잡아야 한다.
>
> **비용 지도.** 칸이 이진값이 아니라 *통행 비용*을 담는 점유 격자다. 비용은 팽창에 더해 로봇이 피해야 할 다른 모든 것을 합친다: 미지 영역, 거친 지형, 일방향 구역, 진입 금지 구역. **비용 지도는 정책적 선호가 계획이기를 그만두고 기하가 되는 자리다** — [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성 §1]]이 학습된 어포던스를 담기에 *맞는* 그릇이라고 논하는 바로 그 표현이다. 같은 장면이 로봇마다 다른 costmap을 내놓기 때문이다. 그 페이지가 거부하는 것은 기하 술어인 점유 격자 쪽이고, 그것을 보려면 이것이 무엇인지 알아야 한다.
>
> **계층형 비용 지도.** 계획기가 읽는 비용 지도는 모두가 같이 쓰는 격자 하나가 아니다. 순서가 정해진 **층(layer)** 목록을 합성해서 만든 **마스터 격자**이고, 한 층은 갱신 주기마다 정확히 두 가지 연산을 수행하는 구성 요소다. 먼저 자기가 건드릴 지도의 사각형 범위를 선언하고, 그다음 그 사각형 안에서 마스터 격자에 비용을 쓴다. 이것을 격자 더미가 아니라 계층형 비용 지도로 만드는 조건이 둘이다. 각 층은 *앞선 층들이 남겨 놓은 상태의* 마스터 격자를 보고, 각 층은 선언된 결합 규칙 — **덮어쓰기**, **최댓값**, 또는 미지를 무시한 최댓값 — 으로 쓴다. 그러므로 순서가 명세의 일부이고 합성은 교환되지 않는다. 보통의 순서는 정적 지도, 그다음 장애물(실시간 센서 데이터로 표시하고 지운다), 그다음 팽창이며, 팽창이 마지막이어야 하는 이유는 앞선 층들이 치명으로 남긴 것까지의 거리를 재기 때문이다. *예*: 사람이 로봇 앞으로 들어온다. 장애물 층이 그 칸들을 표시하고 팽창 층이 그것을 키운다. 사람이 걸어 나가면 광선 투사가 정확히 그 칸들만 지우고, 뒤의 벽은 그대로다. 애초에 그 벽은 장애물 층이 쓴 것이 아니기 때문이다. **비예**: 납작한 격자 하나. 거기서 낡은 사람을 지우려면 정적 지도도 자기 것이라고 주장하는 칸을 지워야 하므로, 벽이 지워지거나 사람이 영영 남거나 둘 중 하나다 — 층이 존재하는 이유 전부가 이것이다. *읽을 때 왜 중요한가*: 논문 속의 "비용 지도"는 합성물이고, 어느 층이 그 비용을 썼는지가 그것을 지울 수 있는지를 결정한다([[04-robotics/ros2/navigation-nav2|25.9 Nav2 §4]]에 한 스택의 층 목록과 기본값이 있다).
>
> **프런티어.** *알려진 자유 공간*과 *미지* 사이의 경계 칸. 정확히는 자신은 자유로 알려져 있고 이웃(4-연결 또는 8-연결) 중 적어도 하나가 미지인 칸이다. **프런티어 탐색**은 "다음에 어디로"에 대한 고전적 답이다: 가장 가까운 프런티어로 가면 아는 영역이 자라고, 프런티어가 없어질 때까지 반복한다. 어떤 의미 내비게이션 방법은 이 후보 집합을 그대로 두고 학습된 부분이 그 위의 *점수*만 공급한다 — [[04-robotics/semantic-language-navigation|19. §3]]의 VLFM이 정확히 그렇다. 그렇지 않은 것도 있다: SemExp의 학습된 전역 정책은 지도 위의 임의의 장기 목표를 고르고, 그것이 그 노트가 "프런티어 기반이 아니라 목표 지향"이라고 말하는 뜻이다([[01-canonical-papers/notes/9-navigation/semexp|SemExp]]). **논문이 둘 중 어느 쪽인지를 가려내는 것이 핵심이고**, 그것이 학습된 구성요소가 후보를 고르는지 순위만 매기는지를 정한다.

> [!warning] "프런티어"의 두 가지 뜻
> 아래 §3과 §4는 그래프 탐색의 열린 목록 — 발견했지만 아직 확장하지 않은 노드 집합 — 을 가리켜
> *프런티어 노드*라고 쓴다. 지도 위의 탐색 프런티어와는 다른 대상이고, 단어만 같을 뿐 서로
> 무관하지는 않다: 둘 다 탐색된 것과 아닌 것의 경계를 가리키고, 하나는 그래프에서 하나는
> 격자에서 그럴 뿐이다. 논문들은 이것을 거의 구분해 주지 않는다.

내비게이션 스택은 이 비용 지도를 두 층으로 탐색한다. 전역 계획기가 경로를 찾고(§3–§5), 지역 계획기가 그 경로를 따라 다음 몇 초의 운동을 고른다. 지역 층의 고전적 방법들은 작은 후퇴 지평 최적화기이므로, §6의 더 깊이 노트가 그것들을 풀어 쓴다.

### 3. 그래프 탐색

탐색은 부분만 지어진 경로 여럿을 한꺼번에 들고 있고, 다음에 어느 것을 늘릴지 골라야 한다. A\*는 이미 쓴 비용에 남은 비용의 추정을 더한 수 하나로 순위를 매겨, 추정 총비용이 가장 작은 경로가 먼저 나가게 한다:

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

휴리스틱은 A\*가 하는 일의 양만 바꾸고 A\*가 돌려주는 답은 바꾸지 않아야 하는데, 그 약속이 지켜지는지는 휴리스틱에 달려 있다. 프런티어의 두 노드가 $(g,h)=(6,3)$과 $(4,6)$이라 하자. A* 우선순위는 $9$와 $10$이므로,
cost-to-come이 더 큰데도 첫 노드가 먼저 확장된다. 휴리스틱은 목표에 가깝다고 추정되는
상태 쪽으로 노력을 돌린다. *과소평가* 휴리스틱은 admissible을 유지한다 — 너무 약하면 A*가 Dijkstra보다 빨라지는
이득이 거의 없을 뿐이다; *과대평가* 휴리스틱은 통상적 최적성 보장을 잃을 수 있다.

그 손실을 숫자로 보자. 둘째 노드의 참 남은 비용이 $4$라서 그 경로의 총비용은 $4+4=8$이고 $h=6$은 $2$만큼 과대평가했다고 하자. 그리고 첫 노드의 $h=3$은 정확해서 그 경로의 총비용이 $9$라고 하자. A\*는 첫 노드를 확장해 목표를 $f=9$로 넣고, 둘째 노드의 $f=10$보다 먼저 그것을 꺼내, $8$이 가능했는데 $9$를 돌려준다 — $12.5\,\%$ 초과이고, 오류 메시지는 없다. §8은 같은 실패를 계산 절에서 만난다. 거기서는 학습된 휴리스틱 때문에 A\*가 $41\,\%$ 더 비싼 가지를 돌려준다.

### 대상으로 한 번 끝까지 · Worked case

§4의 $(g,h)$ 쌍은 맨 숫자였다. 여기서는 그것이 이 페이지의 대상 — P2, 패널, 그리고 $q_\mathrm{start}=(90°,0°)$에서 과제 점 $p^\star=(1,1)$로 가는 질의 — 에서 나오고, 물음은 §3이 존재하는 이유 그 자체다: A\*는 어느 목표를, 어느 간선을 따라 돌려주는가? 답하려면 §1(경로는 컨피규레이션의 곡선이다), §2(C-장애물), §3(A\*)이 한꺼번에 필요하다. 다음 세 회차의 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]은 같은 두 목표를 서로 잇는다.

**1. 과제 점 하나, 컨피규레이션 둘.** P2의 역기구학([[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장]]이 유도하고, 여기서는 검산만 한다): $r=\lVert p^\star\rVert=\sqrt2=1.4142$ m이므로 코사인 법칙이 $\cos\theta_2=(r^2-L_1^2-L_2^2)/(2L_1L_2)=(2-1-1)/2=0$을 주고 $\theta_2=\pm90°$, 곧 목표 컨피규레이션이 정확히 둘이다.

$$q_A=(0°,\ 90°),\qquad q_B=(90°,\ -90°)$$

$\theta_2$의 부호마다 굽은 팔을 $p^\star$ 쪽으로 돌려 놓는 $\theta_1$이 하나씩 정해지기 때문이다. $q_B$는 순기구학으로 검산한다. 검산하지 않은 목표는 지어낸 목표이기 때문이다. $x=\cos 90°+\cos 0°=1$, $y=\sin 90°+\sin 0°=1$로 같은 점이다. 두 목표 모두 $d=0$이다. 렌즈의 경계 위에 있는, 자유로 세는 접촉 컨피규레이션이다. 그러나 같은 접촉은 아니다 — $q_A$에서는 링크 2가 면을 따라 붙고, $q_B$에서는 말단만 닿는다 — 그리고 $\mathcal{C}$ 안에서 둘은 $\lVert q_A-q_B\rVert=\sqrt{(\pi/2)^2+\pi^2}=\pi\sqrt{1.25}=3.512$ rad 떨어져 있다. §2의 비예에 숫자를 붙인 것이 이것이다. 도구의 위치는 컨피규레이션이 아니고, 그 위치를 실현하는 두 컨피규레이션은 관절 운동으로 3.5 rad이나 떨어져 있다.

**2. 서로 다른 $\mathcal{C}$ 경로 둘, 작업 영역 곡선 하나.** 두 목표를 각각 관절 공간에서 직선 보간한다. $s\in[0,1]$에 대해 $\theta(s)=(1-s)\,q_\mathrm{start}+s\,q_\mathrm{goal}$이고, 이 $s$는 §1의 경로 매개변수이며 MR 10장은 같은 것을 $\lambda$라 부른다. 가지 A는 $\theta(s)=(90°-90°s,\ 90°s)$다. 합 $\theta_1+\theta_2$가 $90°$에 머물므로 전완은 똑바로 위를 가리키고 말단은 엘보보다 1 m 위, $x=\sin(90°s)$, $y=1+\cos(90°s)$에 있다. 가지 B는 $\theta(s)=(90°,\ -90°s)$다. 엘보는 $(0,1)$에 머물고 전완이 수직에서 수평으로 내려오므로 말단은 $x=\cos(90°-90°s)=\sin(90°s)$, $y=1+\sin(90°-90°s)=1+\cos(90°s)$ — *같은* 두 함수다. 중간점에서 검산하면 A는 $(45°,45°)$, B는 $(90°,-45°)$이고 둘 다 말단을 $(0.7071,\ 1.7071)$에 놓는다. 그러므로 두 간선은 $(0,1)$을 중심으로 한 반지름 $1$의 같은 사분원을 $(0,2)$에서 $p^\star$까지 그린다.

이제 이 페이지의 대상의 충돌 검사, 곧 말단뿐 아니라 엘보도 보는 검사를 한다. 가지 A에서는 엘보와 말단이 같은 $x=\sin(90°s)$를 갖고, 가지 B에서는 엘보의 $x$가 $0$, 말단의 $x$가 $\sin(90°s)$다. 그러므로 두 간선 모두에서

$$d(s)=\sin(90°s)-1\le0$$

이고 등호는 $s=1$에서만 성립한다. 두 간선 모두 자유이고 목표에서만 패널에 닿는다. 중간점에서는 둘 다 $d=0.7071-1=-0.2929$, 같은 $29$ cm의 여유다. $\mathcal{C}$에서 두 간선은 서로 다른 선분이다 — A는 $(90°,0°)$에서 $(0°,90°)$로 가는 대각선, B는 $(90°,0°)$에서 렌즈의 꼭짓점인 $(90°,-90°)$로 내려가는 선분 — 그리고 둘 다 렌즈 밖에 머문다. $\mathcal{C}$에서는 경로 둘, 작업 영역에서는 곡선 하나, 여유는 동일 — §1이 경로를 도구가 그리는 곡선이 아니라 컨피규레이션 $\sigma(s)\in\mathcal{C}$로 정의하는 이유다.

**3. 같은 곡선, 다른 비용.** 두 간선에 흔한 기본값인 관절 공간 길이로 값을 매긴다.

$$g_A=\lVert(-90°,\ 90°)\rVert=\pi/\sqrt2=2.2214\ \text{rad},\qquad g_B=\lVert(0°,\ -90°)\rVert=\pi/2=1.5708\ \text{rad}$$

따라서 가지 A는 같은 도구 운동을 주면서 가지 B의 정확히 $\sqrt2$배가 든다. A는 두 관절을 모두 $90°$ 돌리고 B는 엘보만 돌리기 때문이다. 노드 셋짜리 그래프(시작, $q_A$, $q_B$, 두 간선 모두 자유로 검사됨)에서 A\*는 시작을 확장하고 두 목표를 넣은 뒤 $q_B$를 돌려준다.

**4. admissible한 휴리스틱 하나와, 그렇게 보이기만 하는 것 하나.**
$h(q)=\lVert p(q)-p^\star\rVert/\sqrt5$, 곧 작업 공간 직선 거리를 줄인 값을 쓰자. 이것이
admissible한 이유는 P2에서 어떤 관절 운동도 말단을 $\sqrt5$배보다 빠르게 움직이지 못하기
때문이다. 여기서 $J$는 P2의 말단 야코비안, 곧 $\dot p=J(\theta)\dot\theta$를 만족하고 각 열이 관절 하나만 움직일 때의
말단 속도인 $2\times2$ 행렬이다([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §2]]가 이 팔에 대해 유도한다).
그 최대 특잇값 $\sigma_{\max}$는 관절 속도 한 단위로 얻을 수 있는 최대 말단 속력
$\max_{\lVert\dot\theta\rVert=1}\lVert J\dot\theta\rVert$다([[02-foundations/linear-algebra|1. 선형대수 §4]]). $JJ^\top$의 대각합은
두 특잇값 제곱의 합이므로
$\sigma_{\max}^2\le\operatorname{tr}(JJ^\top)=3+2\cos\theta_2\le5$이고, 등호는 팔이 곧게 펴져
$J$의 두 열이 평행해지는 $\theta_2=0$에서 성립한다. 그러니 길이 $\ell$의 관절 경로는 말단을 최대
$\sqrt5\,\ell$만큼 옮기고, $\sqrt5$로 나누면 작업 공간 거리가 관절 거리의 하한이 된다. 출발점에서 말단은 $(0,2)$에 있으므로
$h=\sqrt2/\sqrt5=0.6325$ rad, $f(q_\mathrm{start})=0+0.6325$이고, 두 목표를 넣은 뒤에는 목표에서 $h=0$이므로
$f(q_B)=1.5708$, $f(q_A)=2.2214$다. **비예:** 나누지 않은 $\lVert p(q)-p^\star\rVert$는 이 팔에서
admissible하지 않다. $\sigma_{\max}>1$이라 말단이 관절보다 빨리 움직일 수 있기 때문이다. 출발점에서는 마침
과대평가하지 않으므로($1.4142<1.5708$) 잘못된 휴리스틱이 시험 사례를 통과한다. 그것이 무너지는 곳은 $J$의 최대 특잇값이 $1.618$인 $q_B$ 근처다. $q_B$에서 그 특잇값에 대응하는 관절 방향으로 $0.1$ rad 옮긴 자유 컨피규레이션 $q=(94.87°,-86.99°)$에서 말단은 $p^\star$에서 $0.164$ m 떨어져 있어, 나누지 않은 $h$는 $0.164$를 읽지만 참 남은 비용은 $q_B$로 돌아가는 직선 간선의 $0.100$이다.

**5. 충돌 모델이 정한 것.** 2단계의 두 판정은 한 모델에서 나왔다: 두께 0인 링크, 팔 전체 검사, 접촉은 자유. 모델을 바꾸면 경로와 비용은 그대로인데 판정이 바뀐다. 말단만 검사해도 이 패널에서는 아무것도 바뀌지 않는다. 링크 1의 길이가 패널까지의 거리와 정확히 같아서 엘보 항이 결코 발동하지 않기 때문이다([[04-robotics/modern-robotics/ch02-configuration-space|MR 2장]]의 3단계). 카탈로그의 우연이지 면허가 아니다. 벽을 $x\ge0.5$로 옮기면 말단 검사는 말단이 베이스로 돌아온 접은 자세 $(0°,180°)$를 통과시키지만, 링크 1은 벽을 반 미터 관통한다([[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 §2]]의 비예). 아니면 링크마다 반지름 $5$ cm의 캡슐로 키워 보라 — 로봇을 키우기만 하므로 유효한 충돌 검사가 써도 되는 보수적 모델이다. 그러면 두 간선 모두 $\sin(90°s)>0.95$인 곳, 곧 마지막 5분의 1($s>0.798$)에서 충돌하고, 두 목표도 부풀린 장애물 안에 든다. 그 모델 아래에서 이 접촉 질의는 해가 아예 없다. 접촉 과제를 접촉 순간까지 계획하지 않는 이유 하나가 이것이다. [[04-robotics/capstone-panel-contact|26. 캡스톤 §4]]는 추정한 위치로 보아 패널이 있을 수 있는 띠 바깥의 자세에서 계획한 운동을 끝내고, 접촉은 순응형 힘 제어기에 맡긴다. $\mathcal{C}_\mathrm{obs}$는 특정 기하에서 만들어지며, 충돌 모델을 밝히지 않은 채 충돌률을 보고한 논문은 숫자의 절반만 보고한 것이다.

**6. 여기서 "최적"이 뜻한 것.** 척도를 바꾸면 답이 움직인다. 모든 관절의 속도 한계가 같을 때 쓰고 싶은 max-norm에서는 비용이 두 가지 모두 $\max_i\lvert\Delta\theta_i\rvert=\pi/2$로 동점이다. 관절당 $1$ rad/s면 둘 다 $1.571$초에 끝난다. A는 두 관절을 한꺼번에, B는 엘보만 돌린다. 관절 공간 길이는 B를 $\sqrt2$만큼 선호하고, 실행 시간은 둘을 구별하지 못한다. 과제는 구별한다. 도구는 전완을 따라 달려 있어서 면을 누르려면 면을 향해야 하는데, 도구를 $+x$로 향하게 하는 것은 B뿐이다 — A는 도구를 면을 따라 눕힌다. [[04-robotics/capstone-panel-contact|26. 캡스톤]]이 접촉 전 자세를 B의 가지에 두는 이유가 이것이다. 여기서는 척도가 과제와 우연히 맞았을 뿐이다. 목표 집합에 두 가지를 다 넣은 계획기는 그 운에 기대고 있고, 페이지 끝의 과제(problem set)가 그 운이 깨지는 경우를 보여 준다. 그리고 두 숫자 중 어느 것도 말단이 패널에 닿은 뒤 도구가 가할 힘에 대해서는 아무 말도 하지 않는다. 두 목표 모두 $\mathcal{C}_\mathrm{free}$ 안의 접촉 컨피규레이션이고, $\mathcal{C}_\mathrm{free}$는 힘에 대해 침묵한다.

### 5. 주요 방법 계열

계획 논문은 모두 어느 한 계열에 속하고, 그 논문이 무엇을 약속할 수 있는지는 계열이 정한다. 정확한 답인지, 제 격자 위에서만 정확한 답인지, 표본이 늘어야 비로소 그럴듯해지는 답인지다. 표가 계열들을 놓고, 그 뒤의 완전성 목록이 각 계열이 약속할 수 있는 것을 말한다.

| 계열 | 대표 아이디어 | 이렇게 읽어라 |
|---|---|---|
| 그래프 탐색 | BFS, Dijkstra, A* | 명시적 이산화 위의 탐색 |
| 표본 기반 | PRM(probabilistic roadmap), RRT, RRT* | 표본으로 고차원 자유 공간 탐사 |
| 궤적 최적화 | shooting, transcription, collocation | 제약 아래 상태/입력 최적화 |
| 과제 계획 | 기호적 연산자와 목표 | 이산 행동 선택 |
| TAMP | task and motion planning | 기호적 선택을 기하학적 실행 가능성과 결합 |
| 피드백 / 퍼텐셜장 | 목표로 끌고 장애물에서 미는 장; 내비게이션 함수(최솟값이 목표 한 곳에만 있도록 만든 퍼텐셜) | 경로 하나가 아니라 *모든* 상태에 대해 행동을 만든다 — 값싸고 반응적이지만, 단순한 퍼텐셜장에는 로봇을 목표 앞에서 가두는 국소 최솟값이 있다 |
| 불확실성 계획 | MDP, POMDP, belief space(§7) | 불확실한 상태/결과 아래 행동 선택 |

<svg viewBox="0 0 560 176" style="max-width:100%;height:auto" role="img" aria-label="장애물 둘을 돌아 시작에서 목표 쪽으로 자유 공간에 자란 트리와, 그 한 스텝: 무작위 표본 q_rand, 트리에서 그에 가장 가까운 노드 q_near, 그리고 q_near에서 그쪽으로 한 보폭 ε 나아간 새 노드 q_new. 그 짧은 선분이 자유라서 남긴다.">
  <rect x="20" y="20" width="330" height="140" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.5"/>
  <g fill="currentColor" fill-opacity="0.22"><rect x="140" y="86" width="52" height="40" rx="2"/><rect x="230" y="118" width="52" height="34" rx="2"/></g>
  <g stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"><line x1="50" y1="140" x2="75" y2="122"/><line x1="75" y1="122" x2="100" y2="100"/><line x1="100" y1="100" x2="125" y2="78"/><line x1="125" y1="78" x2="160" y2="64"/><line x1="160" y1="64" x2="200" y2="56"/><line x1="200" y1="56" x2="240" y2="70"/><line x1="240" y1="70" x2="280" y2="56"/><line x1="280" y1="56" x2="320" y2="42"/><line x1="75" y1="122" x2="60" y2="98"/><line x1="100" y1="100" x2="86" y2="136"/><line x1="160" y1="64" x2="168" y2="36"/><line x1="200" y1="56" x2="216" y2="30"/><line x1="240" y1="70" x2="248" y2="100"/><line x1="280" y1="56" x2="294" y2="82"/></g>
  <g fill="currentColor" fill-opacity="0.85"><circle cx="75" cy="122" r="2.4"/><circle cx="100" cy="100" r="2.4"/><circle cx="125" cy="78" r="2.4"/><circle cx="160" cy="64" r="2.4"/><circle cx="200" cy="56" r="2.4"/><circle cx="240" cy="70" r="2.4"/><circle cx="280" cy="56" r="2.4"/><circle cx="320" cy="42" r="2.4"/><circle cx="60" cy="98" r="2.4"/><circle cx="86" cy="136" r="2.4"/><circle cx="168" cy="36" r="2.4"/><circle cx="216" cy="30" r="2.4"/><circle cx="248" cy="100" r="2.4"/></g>
  <g fill="currentColor"><circle cx="50" cy="140" r="4.5"/><circle cx="320" cy="42" r="4.5"/></g>
  <line x1="294" y1="82" x2="322" y2="128" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/>
  <line x1="294" y1="82" x2="307" y2="103.4" stroke="currentColor" stroke-width="2.4"/>
  <circle cx="322" cy="128" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="294" cy="82" r="4.2" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="307" cy="103.4" r="3" fill="currentColor"/>
  <g fill="currentColor">
    <text x="30" y="156" font-size="10.5">시작</text>
    <text x="296" y="32" font-size="10.5">목표</text>
    <text x="166" y="110" font-size="10" text-anchor="middle" opacity="0.9">장애물</text>
    <text x="256" y="139" font-size="10" text-anchor="middle" opacity="0.9">장애물</text>
    <text x="316" y="143" font-size="10.5" text-anchor="end">q<tspan dy="3" font-size="10">rand</tspan><tspan dy="-3"> </tspan></text>
    <text x="287" y="87" font-size="10.5" text-anchor="end">q<tspan dy="3" font-size="10">near</tspan><tspan dy="-3"> </tspan></text>
    <text x="315" y="107.4" font-size="10.5">q<tspan dy="3" font-size="10">new</tspan><tspan dy="-3"> </tspan></text>
    <text x="362" y="52" font-size="11">1. 점 q<tspan dy="3" font-size="10">rand</tspan><tspan dy="-3"> </tspan>를 하나 뽑는다</text>
    <text x="362" y="72" font-size="11">2. 가장 가까운 노드 q<tspan dy="3" font-size="10">near</tspan><tspan dy="-3"> </tspan>를 찾는다</text>
    <text x="362" y="92" font-size="11">3. 그쪽으로 ε만큼 나아가,</text>
    <text x="376" y="112" font-size="11">선분이 자유면 q<tspan dy="3" font-size="10">new</tspan><tspan dy="-3"> </tspan>를 더한다</text>
  </g>
</svg>

표본 기반 계획기는 시작점에서 자유 공간으로 트리를 키운다. 한 스텝마다 점 $q_\text{rand}$를 뽑고, 가장 가까운 노드 $q_\text{near}$를 찾아, 그 짧은 선분이 자유이면 그쪽으로 한 보폭 나아간 $q_\text{new}$를 더한다 — [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 §1]]이 이 스텝을 식으로 쓰고 P2 위에서 한 번 밟는다. 트리는 공간을 열거하지 않으며, 그래서 고차원에서도 살아남고, 경로는 들쭉날쭉하게 나와 나중에 평활화한다.

**퍼텐셜장을 식으로 쓰면.** 퍼텐셜장은 내리막 방향이 곧 명령인 스칼라 함수 $U:\mathcal{C}\to\mathbb{R}$이고, $\dot q=-\nabla U(q)$다. 끌어당기는 부분과 밀어내는 부분으로 만든다:
$$U(q)=\tfrac12 k_a\lVert q-q_{\text{goal}}\rVert^2+\begin{cases}\tfrac12 k_r\big(\tfrac1{\rho(q)}-\tfrac1{\rho_0}\big)^2 & \rho(q)\le\rho_0\\ 0 & \rho(q)>\rho_0\end{cases}$$
$k_a,k_r>0$는 이득, $\rho(q)$는 가장 가까운 장애물까지의 거리, $\rho_0$는 그보다 먼 장애물을 무시하는 범위다. 그래서 로봇은 목표 쪽으로 미끄러지고 $\rho\to0$일수록 점점 세게 밀려난다. **내비게이션 함수**(Rimon & Koditschek 1992)는 조건 넷을 더 만족하는 퍼텐셜이다: 자유 공간에서 매끄럽고, 최솟값이 목표 한 곳에*만* 있고, 모든 장애물 경계에서 균일하게 최대이며, 임계점이 모두 비퇴화다. 그래서 그 기울기를 따라가면 거의 모든 출발점에서 목표에 닿는다.

> [!example] 계산 예제 · Worked example
> 목표는 원점, 점 장애물은 $(1,0)$, $k_a=k_r=\rho_0=1$이다. 장애물 너머의 축($x>1$) 위의 $x$에서 인력은 $-x$, 척력은 $\rho=x-1$로 두어 $(1/\rho-1)/\rho^2$다. 둘은 $x=1.618$($\rho=0.618$)에서 상쇄되므로, $(2,0)$에서 놓은 로봇은 목표에 못 미친 그곳에서 멈춘다.
>
> **국소 최솟값의 비예:** 그 점은 *안장점*이다. 옆으로 움직이면 퍼텐셜이 낮아지므로($\partial^2U/\partial y^2=1-1.618/0.618=-1.62<0$) 작은 교란만 있어도 로봇은 장애물을 돌아 미끄러진다. U자 벽 같은 오목한 장애물은 진짜 최솟값을 만들고, 표가 경고하는 함정이 그것이다.

**완전성의 네 강도.** 이 낱말들은 계획기가 해를 *찾는 것*에 대해 무엇을 보장하는지 말한다. 앞의 셋은 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 §3]]이 P2 위에서 풀어 쓴 정의 상자가 있으므로 여기서는 한 줄씩만 두고, 넷째는 이 페이지의 것이다.

- **완전(complete)**: 해가 있으면 유한 시간 안에 해를 돌려주고 없으면 유한 시간 안에 실패를 보고한다 — 저차원에서는 정확한 셀 분해가 이를 달성하지만, 고차원에서 실용적인 방법은 거의 없다.
- **해상도 완전(resolution complete)**: 이산화에 대해 완전하다. 격자 위의 A\*는 격자가 표현할 수 있는 해라면 찾고, 그 실패는 칸보다 좁은 통로에 대해 아무것도 증명하지 않는다.
- **확률적 완전(probabilistically complete)**: *robust한* 해 — 어떤 $\delta>0$에 대해 $\delta$-근방이 $\mathcal{C}_{\text{free}}$ 안에 있는 해, $\delta$-여유라고도 한다 — 가 존재하면, 표본이 늘수록 해를 찾았을 확률이 $1$로 간다. 장애물을 스치기만 하는 경로는 표본으로 뽑힐 확률이 0이고, 계산 절의 접촉 목표를 표본 기반 계획기가 뽑지 않고 질의에서 넘겨받는 이유가 이것이다. 이 계획기는 "해 없음"을 보고할 수 없고, 이 보장은 빠른 성공을 뜻하지 않는다. PRM과 RRT가 이 성질을 가진다.
- **점근적 최적(asymptotically optimal)**: 표본 $n$개 뒤 최선의 해의 비용 $c_n$이 확률 1로 최적 비용 $c^*$에 수렴한다. 극한에 대한 진술이므로 실시간 예산에서 얻는 품질에 대해서는 아무것도 말하지 않는다. RRT\*와 PRM\*는 이 성질을 가지고, 단순 RRT는 가지지 않는다(§5.5의 더 깊이 노트 안의 §5.5.4).
$$P\Big(\lim_{n\to\infty}c_n=c^*\Big)=1$$

> [!example] 계산 예제 · Worked example
> 단순화한 모형에서, 모든 해가 $\mathcal{C}$의 1%를 차지하는 좁은 통로를 지나고, 균일 표본 하나가 그 안에 떨어지면 계획기가 성공한다고 하자. 표본마다 독립적으로 확률 $0.99$로 빗나가므로 $n$개 뒤 실패 확률은 $0.99^n$이다: $n=100$에서 $0.366$, $n=500$에서 $0.0066$, $n=1000$에서 $4.3\times10^{-5}$. 0으로 가므로 확률적 완전이지만, 표본 100개짜리 실행의 3분의 1은 실패한다. 이 보장이 속도에 대해 아무것도 말하지 않는 이유다.
>
> **완전성의 비예:** 10 cm 칸 격자는 유일한 틈이 5 cm인 지도에서 "경로 없음"을 돌려줄 수 있다. 틈에 걸친 칸이 모두 점유로 표시되기 때문이다. 해상도 완전성이 약속한 대로 격자에 대해서는 맞는 답이고, 세계에 대해서는 틀린 답이다.

### 5.5 동역학을 지키는 계획: kinodynamic 탐색, 격자, 평탄성

*한 문장으로:* 자동차는 옆으로 미끄러질 수 없고 크레인의 짐은 흔들리므로, 계획기가 이어 붙이는 조각은 그 기계가 실제로 몰 수 있는 운동이어야 하고, 이 절은 그런 조각을 만드는 표준적인 방법 넷을 보인다.

*이 절에서 하나만 가져간다면:* 곡선을 몰 수 있는지는 그 위를 달리는 속도가 아니라 곡선의 모양이 정한다. §5.5.5의 포물선은 어떤 속도로 달려도 꼭짓점의 곡률이 $2\,\mathrm{m^{-1}}$로, 최소 회전 반경 $1\,\mathrm{m}$가 허용하는 값의 두 배다.

모든 방향으로 모든 속도로 움직일 수 없는 로봇에는 간선이 곧 그 기계가 실행할 수 있는 운동인 계획기가 필요하다. 그래서 격자의 간선과 §5의 표본 트리가 가정하는 직선 연결을, 동역학을 지키는 조향 규칙으로 바꿔야 한다.

#### 5.5.1 기하학적 경로만으로 부족한 이유

세 종류의 제약이 직선 구간 가정을 깬다.

- **비홀로노믹 제약.** 자동차에는 옆 방향 속도가 없고 최소 회전 반경이 있다. 그래서 모서리나 옆으로 비키는 구간이 있는 경로는 쓰인 그대로는 운전할 수 없다. 그래도 차는 모든 자세에 도달할 수 있다(이유는 [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR 13장]]). 형식적으로 쓰면, 비홀로노믹 제약은 $q$만에 대한 제약으로 적분할 수 없는 속도 제약 $A(q)\dot q=0$이다. heading이 $\theta$인 자동차나 유니사이클에서는 속도가 heading 방향을 가리켜야 하므로 다음과 같다:
$$\dot x\sin\theta-\dot y\cos\theta=0$$
  $\theta=0$에서 전진 운동 $(\dot x,\dot y)=(1,0)$은 $0$을 주어 허용되고, 옆 방향 운동 $(0,1)$은 $-1$을 주어 금지된다. **홀로노믹** 제약 $g(q)=0$은 $\mathcal{C}$에서 차원 하나를 없애지만, 비홀로노믹 제약은 운동 방향을 없앨 뿐 도달 가능한 컨피규레이션은 하나도 없애지 않는다.
- **동역학 제약.** 굴착기 붐에는 관성이 있고 크레인에 매달린 짐은 흔들린다. 그래서 계획은 기계가 안정을 유지하고 짐이 진동하지 않을 만큼 가속도를 낮게 지켜야 한다.
- **한계.** 속도·가속도·구동기 한계는 어느 방향으로든 움직일 수 있는 로봇에도 걸린다.

*kinodynamic*은 원래 속도·가속도 한계 아래의 계획을 가리켰고, 지금은 $\dot x = f(x,u)$인 상태 공간에서의 계획 전반을 뜻한다. 문제는 비홀로노믹이거나, kinodynamic이거나, 둘 다일 수 있다. 동역학 모델을 가진 자동차가 둘 다다. MR 10장은 표본 기반 판본과 그 지역 계획기를 한 줄로 짚고, 이 절은 그 긴 지도다.

자동차나 기계가 실제로 몰 수 있는 간선을 만드는 표준적인 방법 셋 — 자동차의 정확한 최단 경로(Dubins와 Reeds–Shepp), 미리 계산한 모션 프리미티브 위의 탐색(상태 격자와 Hybrid A\*), 동역학을 적분하며 뽑는 표본 기반 계획(kinodynamic RRT, RRT\*, FMT\*) — 은 아래 더 깊이 노트의 §5.5.2–§5.5.4에 있다. 차량이나 굴착기 논문이 그중 하나를 이름으로 부를 때 연다. 넷째인 미분 평탄성은 계산해 볼 예제가 그것이라서 §5.5.5로 본문에 남는다.

> [!note]- 더 깊이 · Deeper
> **5.5.2 자동차의 정확한 최단 경로: Dubins와 Reeds–Shepp.**
>
> - **Dubins (1957):** 일정 속도로 전진만 하고 최소 회전 반경이 $\rho$인 차. 임의의 두 자세 $(x,y,\theta)$ 사이 최단 경로는 최대 세 구간이고, 각 구간은 최대 조향 좌회전 호 $L$, 최대 조향 우회전 호 $R$, 직진 $S$ 중 하나다. 최적일 수 있는 *단어*는 여섯 개뿐이다: $LSL, LSR, RSL, RSR, LRL, RLR$. $CCC$ 단어에서 가운데 호는 $\pi$보다 크게 돈다. 직관은 굽은 길을 가장 짧게 도는 방법이다: 허용되는 만큼 최대로 꺾고, 곧게 달리고, 다시 최대로 꺾는다 — 더 완만한 호는 길이만 늘린다 — 그리고 Dubins는 이런 조각 세 개면 언제나 충분함을 증명했다.
> - **Reeds–Shepp (1990):** 같은 차에 후진을 허용한다. 최단 경로는 쉰 개가 안 되는 고정된 단어 목록 중 하나이고, 각 단어는 최대 다섯 구간, 기어 변환(cusp)은 최대 두 번이다.
>
> 둘 다 닫힌 형태라서 계획기는 이것을 **조향 함수(steering function)**, 즉 두 상태 사이의 정확한 연결로 쓴다. 또한 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘]] §8의 격자 휴리스틱에서 장애물을 무시하되 회전 반경은 지키는 쪽 절반이 된다. 한계도 둘 따라온다. 장애물을 무시한다. 그리고 구간 이음매마다 곡률이 점프하므로 실제 핸들은 그 모서리를 정확히 따라갈 수 없다.
>
> **5.5.3 모션 프리미티브 위의 탐색: 상태 격자와 Hybrid A\*.** A\* 자체는 [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘]] §6에 있다. 여기서 바뀌는 것은 간선이 무엇이냐다.
>
> - **상태 격자(state lattice)** (Pivtoraiko, Knepper & Kelly 2009). $(x,y,\theta)$를, 때로는 곡률이나 속도까지 규칙적인 격자로 이산화한다. 오프라인에서 경계값 문제 — 주어진 한 상태에서 다른 한 상태로 모델을 정확히 옮기는 입력을 찾는 문제 — 를 풀어, 격자 상태에서 정확히 시작해 격자 상태에서 정확히 끝나는 실행 가능한 프리미티브의 작은 집합을 만든다. 이 집합은 평행이동에 불변이라 어디서나 같은 프리미티브를 재사용한다.
> - **Hybrid A\*** (Dolgov, Thrun, Montemerlo & Diebel 2010). 몇 개의 조향값으로 차 모델을 적분해 노드를 확장한다. 이산 $(x,y,\theta)$ 칸마다 *연속* 자세를 하나만 두고, 같은 칸에 나중에 도착한 것은 가지친다. 목표에 가까워지면 목표까지 해석적 Reeds–Shepp 연결을 시도하고, 결과를 평활화한다.
>
> 둘의 보장은 다르다. 격자 계획기의 완전성이나 최적성 주장은 연속 문제가 아니라 그 프리미티브 집합에 대한 것이다. Hybrid A\*의 경로는 운전 가능하지만, 칸 단위 가지치기 때문에 격자 위에서조차 완전성과 최적성을 포기한다. [[04-robotics/ros2/navigation-nav2|Nav2]]는 둘 다 "실현 가능(feasible)" 계획기로 제공한다.
>
> **5.5.4 동역학을 넣은 표본 기반 계획: kinodynamic RRT, RRT\*, FMT\*.** *Kinodynamic RRT*(LaValle & Kuffner 2001)는 상태를 표본으로 뽑고, 정한 거리 척도로 가장 가까운 트리 노드를 찾은 뒤, 어떤 입력과 지속 시간으로 $\dot x = f(x,u)$를 적분해 뻗는다. 이 전방 전파에는 경계값 문제 풀이기가 필요 없지만, 새 노드는 뽑은 상태에 정확히 닿지 않고 거리 척도의 선택이 결과를 좌우한다. Karaman & Frazzoli(2011)는 단순 RRT가 확률 1로 준최적 경로에 수렴함을 보였고, RRT\*와 PRM\*는 각 표본을 $(\log n / n)^{1/d}$처럼 줄어드는 반경 안의 이웃과 연결해 점근적 최적성을 되찾는다. 이 속도면 공 하나에 표본이 $\log n$에 비례하는 개수만큼 들어간다. 공의 부피가 $r^d \propto \log n/n$이고 표본이 $n$개이기 때문이다. 재연결이 싸게 유지될 만큼 적으면서, 표본이 늘어도 그래프가 연결된 채로 남을 만큼은 많다. FMT\*(Janson 외 2015)는 표본 묶음 위에서 충돌 검사를 미루는 게으른 동적 계획법으로 같은 보장을 얻는다. 동역학 시스템용 점근 최적 판본에는 정확한 조향 함수와 그 비용이 필요하다 — 자동차라면 Dubins나 Reeds–Shepp, 아니면 미리 계산한 격자, 아니면 아래의 평탄성.

#### 5.5.5 미분 평탄성(differential flatness)

어떤 시스템은 몇 개의 출력 곡선을 자유롭게 계획하면 모든 상태와 입력을 거기서 읽어낼 수 있다. Fliess, Lévine, Martin & Rouchon(1995)은 시스템 $\dot x = f(x,u)$가 (입력 개수만큼의) 출력 $z$를 가져

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

코드는 영어 절의 같은 자리에 있고, 위 표의 숫자와 끝 상태를 그대로 출력한다.

> [!warning] 함정과 논문에서 확인할 것
> - **속력 0은 특이점이다.** $\dot z\to 0$이면 $\theta=\operatorname{atan2}(0,0)$이 정의되지 않고 $\omega$의 분모가 사라진다. $z(t)=(t^3,t^2)$를 보면 heading이 $t=-0.01$에서 $-89.14°$, $t=+0.01$에서 $+89.14°$다. 거의 $180°$인 이 점프는 cusp, 즉 전진 속력 매개변수화로는 표현할 수 없는 기어 변환이다. 그래서 계획기는 내부 점의 속력을 0이 아니게 두고, 의도한 정지·후진 지점에서 궤적을 나누며, 경계 heading은 $v_0\neq 0$인 $\dot z(0)=v_0(\cos\theta_0,\sin\theta_0)$로 부과한다.
> - **"최적"은 무엇에 대해서인가?** 격자 계획기는 자기 프리미티브 집합 위에서 최적이고, Hybrid A\*는 아예 최적이 아니며, Dubins·Reeds–Shepp 비용은 장애물을 무시한다. Dubins 거리는 대칭조차 아니어서 최근접 이웃 척도로 쓸 때 조심해야 한다.
> - **평활화 뒤에 무엇이 살아남았는지 확인하라.** 후처리 뒤에도 곡률 연속성, 회전 반경 한계, 속도·가속도 한계가 지켜지는지 본다.
> - **평탄성은 가정이 아니라 확인할 성질이다.** 논문은 평탄 출력을 명시해야 한다.
>
> **건설 기계에서는.** 굴절식 휠 로더는 프레임을 꺾어 조향하고, 궤도식 굴착기는 미끄럼이 큰 스키드 조향으로 돈다. 둘 다 비용 지도 경로가 무시하는 회전 반경이나 미끄럼 제약을 가진다. 크레인이나 붐은 그 위에 짐 흔들림 동역학을 더한다. 그래서 [[05-construction-robotics/earthmoving-heavy-machinery|중장비 자율화]]에는 2-D 격자 계획기만이 아니라 이 절의 실행 가능성 검사가 필요하다.

### 6. 궤적 최적화와 MPC

탐색은 자유 공간을 지나는 경로를 돌려주지만 그 경로를 따라가는 운동 — 얼마나 빨리, 어떤 입력으로, 얼마의 노력으로 — 은 돌려주지 않는다. 궤적 최적화는 동역학과 장애물 아래에서 비용을 최소화해 그 운동을 고르고, MPC는 로봇이 움직이는 동안 그것을 다시 푼다.

흔한 정식화는 [[02-foundations/optimization|4. 최적화]]의 궤적 최적화 프로그램이다 — 매 스텝 내는 실행 비용에 마지막의 종단 비용을 더한 것으로 읽되, 물리와 장애물이 제약이다.

$$\min_{x_{0:N},u_{0:N-1}} \sum_{t=0}^{N-1}\ell(x_t,u_t)+\ell_f(x_N) \quad \text{s.t. 동역학, 한계, 충돌 제약}$$

**모든 기호.** $x_t\in\mathbb{R}^n$은 스텝 $t$의 상태, $u_t\in\mathbb{R}^m$은 입력이다. $N$은 스텝의 수인 **지평**(horizon)이다. **실행 비용**(running cost), 또는 **단계 비용**(stage cost) $\ell(x_t,u_t)$는 목표까지의 거리나 제어 노력처럼 매 스텝 치르는 스칼라다. **종단 비용** $\ell_f(x_N)$은 마지막 상태에 대해 한 번만 치르고, 흔히 $\phi(x_T)$로 쓴다. 둘의 합이 목적함수 $J$이므로, 이 프로그램은 제안된 미래 하나의 총비용을 최소화한다. 제약에는 이름 붙은 세 종류가 있다.

- 모든 $t$에서의 **동역학** $x_{t+1}=f(x_t,u_t)$(단 $x_0$은 현재 상태로 고정);
- $u_{\min}\le u_t\le u_{\max}$ 같은 **한계**;
- $\mathrm{sd}(x_t)\ge d_{\text{safe}}$ 같은 **충돌 제약**. 여기서 $\mathrm{sd}$는 가장 가까운 장애물까지의 부호 거리(signed distance)이고 장애물 밖에서 양수다 — 장애물 안에서 양수인 이 페이지의 대상과 MR 10장의 침투 깊이 $d$와는 부호가 반대다.

이것은 [[02-foundations/optimization|4. 최적화 §1]]의 일반 프로그램에서 결정 변수를 시간에 걸쳐 펼친 것이고, 선형-이차 특수 경우를 이차 계획(QP)으로 쓴 것은 [[02-foundations/optimization|4. 최적화 §5]]에 있다.

> [!example] 계산 예제 · Worked example
> 스칼라 동역학 $x_{t+1}=x_t+u_t$에 $x_0=1$, $N=2$, $\ell=x_t^2+u_t^2$, $\ell_f=x_N^2$을 두자. 입력 $(-0.5,-0.5)$는 상태 $1, 0.5, 0$과 $J=(1+0.25)+(0.25+0.25)+0=1.75$를 준다. 입력 $(-1,0)$은 상태 $1,0,0$으로 한 스텝 먼저 목표에 닿지만 $J=(1+1)+(0+0)+0=2$다. 큰 입력 하나가 절반 크기 입력 둘보다 비싸기 때문이다. 아무것도 하지 않는 $(0,0)$은 $J=1+1+1=3$을 준다.
>
> **후보의 비예:** 상태 $1,0,0$을 입력 $(0,0)$과 짝지으면 비용이 $1$뿐이지만, $x_1=x_0+u_0$을 어기므로 애초에 궤적이 아니다. 그것을 걸러내는 것이 동역학 제약의 일이다.

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

내비게이션 스택은 이 루프를 작게 돌린다. 지역 계획기가 전역 계획기가 찾은 경로 주변에서 다음 몇 초의 운동을 매 주기 다시 계획한다. 더 깊이 노트가 고전적 지역 계획기들을 나열하고 그중 둘을 식으로 쓴다.

> [!note]- 더 깊이 · Deeper
> **전역과 지역.** 내비게이션 스택은 계획을 둘로 나눈다: **전역 계획기**가 §2의 비용 지도 전체에서 경로를 탐색하고(§3–§5), **지역 계획기**가 그 경로와 로봇의 동역학, 그리고 그사이 나타난 장애물을 놓고 다음 몇 초의 운동을 반복해서 고른다. 고전적 이름들이 사는 곳이 지역 층이다.
>
> | 지역 계획기 | 매 주기에 하는 일 |
> |---|---|
> | *Dynamic window* | 한 주기 안에 도달할 수 있는 속도 쌍(전진, 회전)을 표본으로 뽑아 각각 점수를 매긴다 |
> | **Elastic band** | 내부 수축력과 외부 장애물 반발력으로 시간 개념 없이 *경로*를 변형한다 |
> | **Timed elastic band** | 이름이 가리키는 시간 간격을 더한 후손이다 |
> | **표본 기반 MPC**([[01-canonical-papers/notes/9-navigation/badgr\|BADGR]]이 쓰는 계열) | running estimate 주변에서 많은 행동열을 표본으로 뽑아 모델로 굴린 뒤, 가장 좋은 하나를 고르는 대신 **보상 가중 평균**으로 추정을 갱신하고 그 첫 행동을 실행한다 |
>
> **Dynamic window** (Fox, Burgard & Thrun 1997). $(v_c,\omega_c)$를 현재 전진·회전 속도, $\dot v_{\max},\dot\omega_{\max}$를 가속도 한계, $\Delta t$를 주기라 하자. 후보는 세 조건을 동시에 만족해야 한다. 로봇이 애초에 낼 수 있는 속도여야 한다($V_s$). 한 주기 안에 도달할 수 있어야 하는데, 가속도가 유계이므로 이것은 작은 상자다:
> $$V_d=\{(v,\omega): |v-v_c|\le\dot v_{\max}\Delta t,\ |\omega-\omega_c|\le\dot\omega_{\max}\Delta t\}$$
> 그리고 **허용 가능**해야 한다. 즉 그 호 위의 가장 가까운 장애물 앞에서 멈출 수 있어야 하므로, 제동 감속도 $\dot v_b$에 대해 $v\le\sqrt{2\,\mathrm{dist}(v,\omega)\,\dot v_b}$다($\omega$도 마찬가지). $V_s\cap V_d\cap V_a$의 각 쌍에 목표 방향·여유 거리·속력의 가중합으로 점수를 매기고, 최고의 쌍을 한 주기 동안 실행한다. 예: $v_c=0.5$ m/s, $\dot v_{\max}=0.5$ m/s², $\Delta t=0.25$ s이면 $v\in[0.375,0.625]$ m/s다. 호를 따라 0.5 m 앞의 장애물은 $\dot v_b=0.5$ m/s²에서 $v$를 $\sqrt{0.5}=0.71$ m/s로 제한하므로, 여기서 묶는 한계는 장애물이 아니라 창이다.
>
> **보상 가중 평균.** 현재 추정 $\bar u$ 주변에서 행동열 $K$개 $u^{(k)}$를 뽑아 모델로 굴려 반환값 $R_k$를 얻고, 다시 맞춘다:
> $$\bar u\leftarrow\sum_{k=1}^{K}w_k\,u^{(k)},\qquad w_k=\frac{\exp(R_k/\lambda)}{\sum_{j=1}^{K}\exp(R_j/\lambda)}$$
> 가중치는 양수이고 합이 1이므로 모든 표본이 좋은 정도에 비례해 기여하고, 온도 $\lambda>0$가 최고 표본을 얼마나 날카롭게 편애할지 정한다($\lambda\to0$이면 "가장 좋은 하나 고르기"로 돌아간다). 예: 첫 행동이 $0.4$와 $0$, 반환값이 $1$과 $0$인 두 표본에 $\lambda=1$이면 가중치는 $0.731$과 $0.269$이고, 새 첫 행동은 $0.292$다.
>
> 위의 프로그램이 같은 층을 최적화 관점에서 본 것이다. 고전적인 내비게이션 스택에서 학습되는 부분은 보통 지역 층이고 전역 탐색과 비용 지도는 건드리지 않는다. 다만 항상 그런 것은 아니다. 학습된 전역 계획기와 학습된 탐색 휴리스틱이 존재하고, [[04-robotics/semantic-language-navigation|19. §3]]의 end-to-end 계열은 스택 전체를 대체한다. **논문이 실제로 어느 층을 대체했는지 확인하라** — 그것이 그 결과가 주장할 수 있는 범위를 한정한다.

**이해 확인.** 해법의 실행 가능 출력은 초기 상태, 모델, 이산화, 제약에 조건부다. 상태 추정이 낡거나 검사 지점 사이에서 충돌하면 최적화를 정확히 푸는 것만으로 부족하다. 궤적 표현과 피드백 실행의 구분은 [궤적 최적화 강의](https://underactuated.mit.edu/trajopt.html)에서도 다룬다.

### 7. 과제 계획, 불확실성, replanning

`pick(block)` 같은 기호적 명령은 논리적으로 타당해도 충돌 없는 파지가 존재하지 않아
기하학적으로 불가능할 수 있다. TAMP는 이산 행동과 연속 실행 가능성을 번갈아 또는
공동으로 추론한다.

**기호적 과제 계획의 정의.** 고전적(STRIPS식) 계획 문제는 네 부분으로 이루어진다. 먼저 `holding(block)` 같은 사실, 곧 불리언 **명제**(proposition)의 집합이 있다. **상태** $s$는 지금 참인 명제의 집합이고, 초기 상태 $s_0$과 끝에 참이 되어야 하는 명제의 집합인 **목표** $G$가 있다. 그리고 **연산자**(operator)가 있는데, 연산자마다 전제 조건 집합 $\mathrm{pre}(a)$, 추가 목록 $\mathrm{add}(a)$, 삭제 목록 $\mathrm{del}(a)$를 가진다. 연산자는 $\mathrm{pre}(a)\subseteq s$일 때 $s$에서 적용할 수 있고, 적용하면 자기가 이름 붙인 사실만 정확히 바꾸므로 다음 상태는
$$s'=\big(s\setminus\mathrm{del}(a)\big)\cup\mathrm{add}(a)$$
이다. 계획은 적용 가능한 연산자들의 열로서, 그것을 다 적용한 뒤 $G\subseteq s$가 되는 것이다. 단순화한 예: pre $\{$`handempty`, `clear(block)`$\}$, del $\{$`handempty`$\}$, add $\{$`holding(block)`$\}$인 `pick(block)`은 $\{$`handempty`, `clear(block)`$\}$를 $\{$`clear(block)`, `holding(block)`$\}$로 옮긴다. **비예:** 그 상태 어디에도 블록이 어디 있는지, 충돌 없는 파지가 존재하는지가 기록되어 있지 않으므로, 타당한 기호적 계획이 아직 실행 가능한 계획은 아니다. 그 간극을 메우는 것이 TAMP다.

**튜플로 쓴 MDP와 POMDP.** **MDP** $(\mathcal{S},\mathcal{A},T,R,\gamma)$는 상태 집합, 행동 집합, 전이 커널 $T(s'\mid s,a)$, 보상 $R(s,a)$, 할인율 $\gamma\in[0,1]$로 이루어지고, 다음 상태가 현재 상태와 행동에만 달려 있다는 마르코프 성질을 함께 가진다. 완전한 정의는 [[02-foundations/rl-basics|RL 기초 §1]]에 있다.

부분 관측에서는 계획의 상태가 **belief**, 즉 숨은 상태에 대한 확률 분포가 되고, 행동과 관측이
있을 때마다 [[04-robotics/state-estimation-slam|3. 상태 추정 §4]]의 **베이즈 필터**로 갱신된다. belief를 운동 모델에 통과시키는 예측 단계와, 관측의 우도로 다시 가중하고 정규화하는 보정 단계다. POMDP는 숨은 상태, 관측, 행동, 전이, 관측 모델, 보상을 구분한다. 튜플로 쓰면 **POMDP**(부분 관측 MDP)는
$$(\mathcal{S},\mathcal{A},\Omega,T,Z,R,\gamma,b_0)$$
이고, 상태가 더는 보이지 않으므로 MDP에 구성 요소 셋을 더한다: **관측 공간** $\Omega$, 행동 $a$가 상태 $s'$로 이끌었을 때 $o$를 관측할 확률을 주는 **관측 모델** $Z(o\mid s',a)$, 그리고 **초기 belief** $b_0$. belief $b(s)$는 지금까지의 모든 행동과 관측이 주어졌을 때 상태 $s$의 사후 확률이다. $a$를 하고 $o$를 관측하면 베이즈 규칙이 그것을 갱신한다:
$$b'(s')=\eta\,Z(o\mid s',a)\sum_{s\in\mathcal{S}}T(s'\mid s,a)\,b(s)$$
합은 옛 belief를 동역학에 통과시키는 **예측**(prediction)이고, 인자 $Z$는 각 상태를 그것이 $o$를 얼마나 잘 설명하는지로 가중하는 **보정**(correction)이며, $\eta$는 $b'$의 합이 1이 되게 하는 정규화 상수다. 이것은 바로 그 베이즈 필터이되, 행동이 주어지는 것이 아니라 계획기가 고른다. 그래서 계획기는 어떤 행동이 가장 쓸모 있는 belief를 남길지 물을 수 있다. belief가 이력 전체를 요약하므로 POMDP는 belief를 상태로 삼는 MDP이고, 그 기대 보상은 $\rho(b,a)=\sum_s b(s)\,R(s,a)$다. **비예:** 가장 최근의 관측 하나만으로는 마르코프 상태가 되지 않는다. 아래 예에서 같은 "열림" 판독이 belief $0.5$는 $0.8$로 옮기지만 belief $0.8$은 $0.94$로 옮긴다.

> [!example] 계산 예제 · Worked example
> 로봇이 잘 보이지 않는 문을 지나가야 한다. **숨은 상태:** 열림 또는 닫힘. **행동:** 다시 보기, 또는 지나가기. **전이:** 보기는 아무것도 바꾸지 않고, 지나가기는 로봇을 옮긴다. **관측:** "열림" 또는 "닫힘"이라는 센서 판독. **관측 모델:** 판독은 80% 확률로 맞다. **보상:** 통과하면 $+1$, 닫힌 문에 부딪히면 $-1$.
>
> belief $P(\text{열림})=0.5$에서 시작한다. "열림" 판독 한 번이면 $0.8\cdot0.5/(0.8\cdot0.5+0.2\cdot0.5)=0.8$, 두 번이면 $0.8\cdot0.8/(0.8\cdot0.8+0.2\cdot0.2)\approx0.94$다. 이것이 위의 갱신 식 그대로다. 보기는 상태를 바꾸지 않으므로 합은 그냥 $b(s')$이고, $Z$는 $0.8$ 또는 $0.2$이며, $\eta$는 첫 번째에 $1/0.5=2$, 두 번째에 $1/0.68=1.47$이다. belief 0.8에서 지나가면 기대 보상은 $\rho=0.8\cdot(+1)+0.2\cdot(-1)=0.6$, 0.94에서는 $0.88$이다. 한 번 더 볼 가치가 그 시간만큼 있는지가 바로 POMDP 계획기가 답하는 질문이고, 그 질문은 실제 문이 아니라 belief에 대해 던져진다.

정확한 belief-space 계획은 대개 계산 불가능해서 논문들은
근사, receding horizon, 학습된 가치, 비상 정책을 쓴다.

온라인 replanning은 새 관측을 반영한다. 보고된 replanning 주기만으로는 부족하다 —
인식 지연, 장면 동역학, 제어기 대역폭과 비교하라.

### 8. 학습 기반 계획

학습된 신경망을 계획기에 끼워 넣은 논문은 한 가지 물음에 답해야 한다: 신경망이 채운 자리의 보장을 계획기가 여전히 지키는가? 학습된 구성요소는 휴리스틱, 비용, 동역학/월드모델, 가치 함수, 제안 분포, 궤적 생성기,
정책 전체 중 무엇이든 될 수 있다. 행동을 출력하는 VLA는 대개 정책이다; 미래를 롤아웃하는
월드모델은 그 미래를 *선택·최적화 절차가 사용할 때에만* 계획을 지원한다.

**학습된 조각이 보장에 하는 일.** 학습된 구성 요소는 자기가 채우는 자리의 보장을, 그 자리의 조건을 만족할 때에만 물려받는다. 그런데 학습된 신경망은 시험 집합에서 측정될 뿐, 어떤 조건을 모든 곳에서 만족한다고 증명되는 일은 없다. 두 자리를 이 페이지의 숫자로 풀어 보자.

*A\* 안의 학습된 휴리스틱.* 남은 비용을 회귀하는 신경망은 거의 admissible하지 않다(§3). 과대평가가 모든 곳에서 유계라면, 곧 어떤 배수 $\varepsilon>1$에 대해 $h\le\varepsilon h^*$라면, 더 싼 경로가 닿을 때마다 노드를 다시 여는 한 가중 A\*의 논증([[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘 §6]])이 그대로 반환 비용을 $\varepsilon C^*$ 이하로 묶는다. 계산 절에서 가지 A는 가지 B의 $\sqrt2=1.414$배이므로, $\varepsilon<1.414$이기만 하면 A\*는 여전히 B를 돌려준다. 이 한계는 모든 목표에서 $h=0$이기를 요구하기도 한다. 거기서 $h^*$가 0이기 때문인데, 회귀는 이것을 강제하지 않는다. 계산 절의 노드 세 개짜리 그래프에서 신경망이 $q_B$에서 $q_A$보다 $0.651$ rad 넘게 높게 읽으면 $f(q_B)=1.5708+h(q_B)$가 $f(q_A)=2.2214+h(q_A)$를 넘고, A\*는 $41\%$ 더 비싼 가지를 돌려준다.

*표본 기반 계획기 안의 학습된 표본기(sampler).* 확률적 완전성(§5)이 요구하는 것은 $\mathcal{C}_{\text{free}}$의 모든 영역이 뽑힐 확률을 양수로 유지하는 것뿐이다. §5의 좁은 통로에서, 표본의 $20\%$를 통로에 넣는 학습된 제안 분포는 표본 $20$개 뒤에도 확률 $0.8^{20}=0.012$로만 놓치고, 균일 표본은 $0.99^{20}=0.818$로 놓친다. 그러나 어떤 영역을 전혀 뽑지 않는 제안 분포는, 유일한 해가 그 영역을 지나는 모든 지도에서 보장을 잃는다. 표본의 절반을 균일하게 뽑으면 모든 영역의 확률이 균일할 때의 절반 아래로 떨어지지 않고, 이 통로라면 표본당 $0.005$이므로 보장이 돌아온다. 이 통로에서 그 혼합은 여전히 $0.895^{20}=0.109$만큼만 놓친다.

그러니 논문에 던질 질문은 그 신경망이 어느 자리를 채우고, 그 자리의 조건 가운데 무엇이 아직 성립하느냐다. 학습된 정책이나 궤적 생성기는 보장이 딸린 자리를 하나도 채우지 않으며, 아래 경고가 말하는 것이 바로 그것이다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "그럴듯한 궤적을 생성한다"는 충돌 없음, 동역학적 실행 가능, 안정, 안전한 실행을
> 함의하지 않는다. 명시적 제약, 하류 제어기, replanning, 폐루프 로봇 결과를 확인하라.

### 9. 평가와 실패 모드

계획 논문은 결과를 숫자 몇 개로 보고하고, 그 숫자는 저마다 어떤 조건에서 쟀는지가 함께 오지 않으면 오해를 부른다. 성공률, 충돌률, 경로/궤적 비용, 계획·실행 시간, 최적성 갭(상대 초과 비용 $(C-C^*)/C^*$, 그래서 최적 10 m에 대한 11 m 경로는 10% 갭이다), 제약 위반, replanning 빈도,
지도/상태 오차에 대한 강건성, 폐루프 실행을 확인하라. 계획 실패, 인식 실패, 추종 실패,
하드웨어 실패를 분리하라.

**그중 네 숫자에는 조건이 따라붙어야 하고, 이 페이지에서 계산할 수 있다.** 최적성 갭은 비용에 대해 상대적이다. 계산 절에서 가지 A의 갭은 관절 공간 길이로는 $(2.2214-1.5708)/1.5708=41\%$이고, 두 가지 모두 관절마다 $1$ rad/s로 $1.571$ s 걸리는 max-norm으로는 $0\%$다. 그러므로 척도를 밝히지 않은 갭은 아무것도 말하지 않는다. 성공률은 시도 횟수에 대해 상대적이다. 스무 번 중 열여덟 번 성공은 $90\%$이고 95% Wilson 구간은 $[0.70,\ 0.97]$이다 — [[02-foundations/ml-practice|9. ML 실무와 평가]]가 계산 절에서 유도하고 과제 3에서 바로 이 20번 중 18번에 대해 계산한 구간이다. 경쟁자의 스무 번 중 열여섯 번은 $[0.58,\ 0.92]$이다. 두 계획기를 성공 두 번 차이로 가르는 20회짜리 표는 순위를 정하지 못했다([[06-research-practice/experimental-design-reproducibility|Experimental Design §4]], 연구 실무에서 뒤에 나온다). 그리고 계획 시간은 분포다. §5의 좁은 통로에서 첫 성공까지의 표본 수는 기하 분포를 따르고, 평균은 $1/0.01=100$, 중앙값은 $69$, 95번째 백분위수는 $299$다. $0.99^n$이 처음으로 $0.05$ 아래로 내려가는 것이 $n=299$이기 때문이다. 평균으로 보고된 계획기는 세 배 긴 꼬리를 감춘다. 그리고 재계획 주기는 새 정보가 들어오는 주기에 묶인다. $2$ Hz로 갱신되는 비용 지도에서 $10$ Hz로 재계획하면 지도 하나당 계획이 다섯 번 나오고 그중 넷은 이미 쓴 데이터로 만든 것이며, 새 장애물이 계획에 반영되기까지는 계산 시간을 빼고도 지도 한 주기와 계획 한 주기, 곧 최대 $0.5+0.1=0.6$ s가 걸릴 수 있다. $1$ m/s에서 $0.6$ m를 가는 시간이다. [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]의 샘플링 지연 논증이 바로 이것이다.

**세기 전에 실패의 원인을 가려라.** 실행 중 충돌이 계획 실패인 것은 계획기가 검사한 충돌 모델이 로봇이 실제로 만난 것과 같을 때뿐이다. 계산 절의 5단계에서 말단만 보는 검사가 이 패널에서 팔 전체 검사와 일치하는 것은 링크 1의 길이가 패널까지의 거리와 정확히 같기 때문일 뿐이다. $x\ge0.5$의 벽이라면 그 검사는 링크 1이 반 미터 들어간 접은 자세 $(0°,180°)$를 통과시킨다. 그 검사로 계획한 로봇이 벽에 부딪혔다면 탐색은 시킨 대로 했으므로, 그 충돌은 계획기가 아니라 충돌 모델의 몫이다. 처음 어겨진 약속을 눈에 보이는 결과와 따로 두는 것이 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §10]]의 실패 분류이고, [[06-research-practice/failure-analysis-system-evaluation|3. 실패 분석 §1]]이 그것을 로그 하나 전체에 적용한다.

### 읽고 나면 말할 수 있어야 하는 것

- 계획·경로·궤적·정책·제어기를 구분할 수 있다
- A*의 $g$, $h$, $f$를 해석할 수 있다
- probabilistic completeness를 속도 보장이라 부르지 않고 설명할 수 있다
- 그래프 탐색·표본 기반 계획·궤적 최적화를 비교할 수 있다
- TAMP가 기하학적 실행 가능성을 검사해야 하는 이유를 설명할 수 있다
- 학습된 궤적 생성기가 보장하지 않는 것을 짚을 수 있다
- "충돌 없음"이나 "최적" 주장이 자기 충돌 모델과 척도를 밝혔는지 확인할 수 있다

> [!tip] 더 깊이 · Going deeper
> LaValle의 [*Planning Algorithms*](http://lavalle.pl/planning/)가 무료이고 표본 기반 쪽의 참고서다. 다만 2006년 책이라 확률적 완전성까지만 다루고 RRT\*와 점근적 최적성은 없다 — 그쪽은 Karaman과 Frazzoli(2011)다. 궤적 최적화 쪽은 Tedrake의 [*Underactuated Robotics*](https://underactuated.csail.mit.edu/)가 실행 가능한 코드와 함께 다룬다.

### 스스로 점검

1. 충돌 없는 경로가 동역학적으로 실행 불가능할 수 있는 이유는?
2. 컨피규레이션 공간 대신 작업 영역에서만 계획하면 무엇을 잃는가?
3. 실행 가능한 궤적이 존재하는데도 궤적 최적화가 실패할 수 있는 이유는?
4. "실시간 폐루프 계획기" 주장을 지지하는 증거는?
5. (§5.5의 더 깊이 노트와 함께) Hybrid A\* 논문과 상태 격자 논문이 둘 다 경로가 "최적"이라고 한다. 각각 무엇에 대해 최적인가?
6. 포물선 $z(t)=(t,t^2)$는 꼭짓점 근처에서 최소 회전 반경 1 m를 어긴다. 같은 곡선을 따라 천천히 달려도 고쳐지지 않는 이유는?

> [!tip]- 정답 · Answers
> 1. 불가능한 속도·가속도·토크·접촉·타이밍을 요구할 수 있다.
> 2. 로봇 형상, 관절 한계, 같은 과제 자세에 대한 복수의 컨피규레이션.
> 3. 문제가 비볼록이고 초기화에 민감할 수 있다.
> 4. 명시된 하드웨어에서의 끝-끝 지연 분포, 교란·동적 장애물 아래의 실행, 제약 위반과 실패 — 계획기 계산 시간만으로는 안 된다.
> 5. 격자 계획기는 미리 계산한 프리미티브 집합과 해상도 위에서만 최적이라, 그 집합에 없는 heading이나 곡률이 필요한 경로를 놓칠 수 있다. Hybrid A\*는 칸마다 연속 자세 하나만 남기고 나머지를 가지치기 때문에 자기 격자 위에서조차 최적이 아니다.
> 6. 회전 반경 한계는 곡률 $\kappa=\omega/v$를 제한하는데, 곡률은 기하에만 달려 있다. 절반 속도에서 꼭짓점은 $v=0.5$, $\omega=1$이라 $\kappa$는 여전히 2다. 다른 곡선만이 답이다.

### 과제 · Problem set

Tier B, Working 통과에서 푼다. **P2**([[02-foundations/lab-plants|0.6]], 카탈로그의 평면 2링크 팔), 패널 $x\ge1$, 계산 절의 목표 $q_A$, $q_B$를 그대로 쓰되 두 가지를 바꾼다. 팔은 가지 A의 중간인 $q_h=(45°,45°)$에서 멈춰 있다 — 엘보 $(0.7071,0.7071)$, 말단 $(0.7071,1.7071)$. 그리고 과제가 이제 도구가 면을 향할 것을 요구하는데, 그렇게 하는 것은 $q_B$뿐이다(6단계). 또 어깨를 $0.5$ rad/s로 감속하고 엘보는 $1$ rad/s를 유지한다. 노드 둘이나 셋짜리 그래프, 시뮬레이터 없음.

1. **그리기.** 이 변형의 그림. $\mathcal{C}$에는 렌즈, $q_h$, $q_\mathrm{start}$, $q_A$, $q_B$, 렌즈로 들어가는 점을 표시한 직선 간선 $q_h\to q_B$, 그리고 우회 $q_h\to q_\mathrm{start}\to q_B$. 작업 영역에는 $q_h$와 $q_B$의 팔, 면 너머 가장 먼 점에 이름을 붙인 직선 간선의 말단 경로, 그리고 우회의 말단 경로. 우회의 말단은 계산 절의 어느 곡선을 되짚는가?
2. **유도.** (가) 직선 간선 $q_h\to q_B$의 비용을 관절 공간 길이, max-norm, 그리고 이동 시간 $t=\max(\lvert\Delta\theta_1\rvert/0.5,\ \lvert\Delta\theta_2\rvert/1)$(초)로 매겨라. (나) 그 간선 위에서 말단의 $x(s)$를 쓰고 가장 깊은 침투를 구하라: $w=45°+45°s$로 치환하고 $\sin(2w-90°)=-\cos 2w$를 써서 $x$를 $c=\cos w$의 이차식으로 쓴다. $s$의 어느 범위에서 간선이 패널 안에 있고, 엘보 항이 판정을 좌우하는 일이 있는가? (다) 같은 $d$로 우회의 두 구간을 검사하고, 우회의 비용을 라디안과 초로 매긴 뒤, 막힌 직선 간선보다 얼마나 더 드는지 구하라.
3. **해석.** 두 간선을 모두 검사한 노드 셋짜리 그래프 $\{q_h,\ q_A,\ q_B\}$에서 A\*는 $q_A$를 돌려준다. 그 답이 그래프에는 맞고 과제에는 틀린 이유, 목표를 바로잡는 질의의 변경, 그리고 그 뒤 노드 둘짜리 그래프 $\{q_h,\ q_B\}$에서 A\*가 무엇을 보고하는지 말하라 — 그 보고가 $\mathcal{C}_\mathrm{free}$에 대해 무엇이든 말해 주는지도(§5).

> [!note]- 그리는 법 · How to draw it
> - 오른쪽 칸, 컨피규레이션 공간: 각각 $-180°$에서 $180°$까지인 $\theta_1$(가로)와 $\theta_2$(세로), 그리고 마주 보는 변이 붙어 있다는 메모($\mathcal{C}=T^2$, §2). 렌즈 $\cos\theta_1+\cos(\theta_1+\theta_2)>1$을 칠한다. 2장 4단계의 표가 그 경계 위의 점들을 준다. $(0°,\pm90°)$, $(\pm60°,0°)$, $(60°,-120°)$, $(-60°,120°)$, 그리고 두 꼭짓점 $(90°,-90°)$과 $(-90°,90°)$이 그중 일부다.
> - $q_h=(45°,45°)$, $q_\mathrm{start}=(90°,0°)$, $q_A=(0°,90°)$, $q_B=(90°,-90°)$에 점을 찍고, $q_A$와 $q_B$에는 자유로 세는 접촉이라는 뜻으로 고리를 친다.
> - 직선 간선 $q_h\to q_B$는 선분 하나로. 렌즈로 들어가는 곳을 표시하고 가장 깊은 점에 X를 친다.
> - 우회는 선분 둘로: 직선 $\theta_1+\theta_2=90°$를 따라 $q_h\to q_\mathrm{start}$, 그다음 $q_B$까지 곧장 아래로.
> - 왼쪽 칸, 작업 영역: 원점의 베이스, $x>1$ 쪽에 빗금을 친 면 $x=1$과 그 위의 $p^\star=(1,1)$, 그리고 $q_h$와 $q_B$의 팔을 링크 하나씩 — 엘보는 $(\cos\theta_1,\sin\theta_1)$, 말단은 $\theta_1+\theta_2$ 방향으로 1 m 더.
> - 직선 간선의 말단 경로를 $(0.707,1.707)$에서 면을 지나 $p^\star$로 돌아오기까지 그리고, 들어가는 점과 가장 먼 점에 이름을 붙인다. 그다음 우회의 말단 경로를 점선으로.

> [!tip]- 정답 · Solutions
> 1. $\mathcal{C}$에서 $(45°,45°)$에서 $(90°,-90°)$로 가는 직선 간선은 $s=1/3$, 곧 컨피규레이션 $(60°,0°)$에서 렌즈로 들어간다 — 팔이 $60°$로 곧게 펴져 말단이 면 위 $(1,1.732)$에 닿는, 2장 표의 경계점이다 — 그리고 꼭짓점의 $q_B$에 닿을 때까지 안에 머문다. 가장 깊은 점은 $(75.52°,-46.57°)$다. 우회의 첫 구간은 계산 절의 간선 A(직선 $\theta_1+\theta_2=90°$) 위에 있고 둘째 구간은 간선 B이므로, 둘 다 렌즈 밖에 머문다. 작업 영역에서 직선 간선의 말단은 $(1,1.732)$에서 면을 지나 $(1.125,1.452)$까지 불룩 나갔다가 $p^\star$로 돌아온다. 우회의 말단은 계산 절의 $(0,1)$ 중심 사분원을 되짚는다: $(0,2)$까지 올라갔다가 $p^\star$로 다시 내려온다.
> 2. (가) $\Delta\theta=(45°,-135°)$: 관절 공간 길이 $45°\sqrt{10}=2.4836$ rad, max-norm $135°=2.3562$ rad, 시간 $\max(0.785/0.5,\ 2.356/1)=2.356$ s로 엘보가 정한다. (나) $\theta_1=45°+45°s$, $\theta_1+\theta_2=90°-90°s$이므로 $x(s)=\cos(45°+45°s)+\sin(90°s)$다. $w=45°+45°s$로 두면 $90°s=2w-90°$이고 $\sin(2w-90°)=-\cos 2w=1-2\cos^2 w$이므로 $x=1+c-2c^2$다. $c=1/4$에서 최대 $x=1.125$, 곧 $d_{\max}=0.125$ m이고, 그때 $w=75.52°$, $s=0.678$, $\theta=(75.52°,-46.57°)$, 말단 $(1.125,1.452)$다. $x>1$은 정확히 $c(1-2c)>0$, 곧 $0<c<1/2$, $w\in(60°,90°)$, $s\in(1/3,1)$일 때다. 간선은 뒤쪽 3분의 2에서 패널 안에 있고 $q_B$에서만 다시 면에 닿는다. 엘보의 $x=\cos w\le0.707$은 판정을 좌우하지 않는다. (다) 1구간 $q_h\to q_\mathrm{start}$는 $\theta_1+\theta_2=90°$를 유지하므로 말단의 $x$가 엘보의 $x$, 곧 $\cos\theta_1\le0.707$과 같다: 자유, $45°\sqrt2=1.1107$ rad, $\max(0.785/0.5,\ 0.785/1)=1.571$ s. 2구간은 계산 절의 간선 B다: 자유, $1.5708$ rad, $1.571$ s. 우회는 $2.6815$ rad, $3.142$ s로, 막힌 간선보다 $0.198$ rad($8.0\,\%$), $0.785$ s($33\,\%$) 더 든다. 더 나은 경유점은 가지 B의 중간점 $(90°,-45°)$다. 그 첫 구간이 면에 가장 가까이 가도 $0.235$ m이고, 우회는 $2.5416$ rad로 $2.3\,\%$만 더 들며 시간은 직선 간선과 똑같은 $2.356$ s다. 시간을 정하는 관절인 엘보가 모두 합쳐 여전히 $135°$를 돌기 때문이다.
> 3. 간선 $q_h\to q_A$는 $\theta_1+\theta_2=90°$를 유지하므로 자유이고, $1.1107$ rad로 어느 목표로 가는 간선보다 싸다. A\*는 주어진 그래프와 목표 집합에 대해서는 옳다. 틀린 것은 목표 집합이다 — "말단을 $(1,1)$에"는 두 가지를 모두 허용하는데, 과제는 도구가 면을 향하기를 원한다. 도구 방향까지 넣은 작업 공간 자세 $(1,1,0°)$로 쓰면 목표의 컨피규레이션은 $q_B$ 하나다([[04-robotics/modern-robotics/ch02-configuration-space|MR 2장 §1.5]]의 작업 공간 상자가 $45°$ 방향으로 같은 점을 짚는다). $\{q_h,\ q_B\}$에서는 하나뿐인 간선이 막혀 A\*가 실패를 보고한다 — 노드 둘짜리 그래프에 대한 사실이지 $\mathcal{C}_\mathrm{free}$에 대한 사실이 아니다. $q_\mathrm{start}$를 거치는 우회가 자유이기 때문이다. 해상도 완전성을 제대로 읽으면 이렇다(§5): 이산화 위의 실패는 연속 문제에 대해 아무것도 증명하지 않고, 노드 하나를 더하면 A\*가 우회를 찾는다.

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
