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
> An intuition for degrees of freedom and the rotation representations of [[02-foundations/se3-geometry|8. SE(3) §2]] are enough to start; §3 also uses partial derivatives ([[02-foundations/engineering-math|0.5 §1]]) and P2's Jacobian $J$ ([[02-foundations/manipulator-kinematics-dynamics|10 §1]]), and the worked case's Step 5 an integral read as an area ([[02-foundations/engineering-math|0.5 §3]]). This chapter is the robotics track's real starting point. The object throughout is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled).
> 자유도의 직관과 [[02-foundations/se3-geometry|8. SE(3) §2]]의 회전 표현이면 시작할 수 있다. §3은 편미분([[02-foundations/engineering-math|0.5 §1]])과 P2의 야코비안 $J$([[02-foundations/manipulator-kinematics-dynamics|10 §1]])를, '대상으로 한 번 끝까지'의 5단계는 넓이로 읽는 적분([[02-foundations/engineering-math|0.5 §3]])을 함께 쓴다. 이 장이 로보틱스 트랙의 실질적 출발점이다. 전체에서 쓰는 대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치(plant, 제어에서 제어 대상인 시스템을 부르는 말) **P2**다.

## English

**Core question**: what is the space of all possible "positions" of a robot, and what shape is it?

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this page is the ground floor of the motion-and-task-planning layer, and in *"install that panel on the frame"* it serves *move the component*: every planner that moves P2 toward the panel searches the set this page builds, not the workspace (its chip sits in the planning band of the [[physical-ai-map|Physical AI Map]]). Without it the arm is planned from pictures of the wall: read the $(\theta_1, \theta_2)$ chart as a flat square and the move from $(170°, 0°)$ to $(-170°, 0°)$ goes the long way through $\theta_1 = 0$, where the straight arm is $1\,\mathrm{m}$ inside the panel, although the torus offers a free $20°$ move (§1); and a controller that keeps only the tip $(1, 1)$ cannot tell contact A, link 2 flush on the face, from contact B, the tip alone. Later pages build on it section by section — [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10 §2]] tests exactly §2's C-obstacle, [[04-robotics/planning-decision-making|4. Planning §2]] counts the configuration space among its five spaces, [[04-robotics/capstone-panel-contact|26. Capstone §2]] inflates §2's lens-shaped C-obstacle by the uncertainty of the panel's estimated position, and [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR ch.13 §1]] starts from §3's nonholonomic constraint — and on the dissertation path ([[07-research-program/index|7 §8]]) it comes at the start of block 2, the robotics common track, as robotics sessions 2–4. After it you can count P2's degrees of freedom, name its C-space as a torus, derive the panel's C-obstacle and its one-dimensional contact set by hand, and tell a configuration from a tip position.

> [!note] First pass · 처음이라면
> One session, robotics session 2: the Running object, the picture and the Worked case, Steps 1–7 by hand with the answers covered — take Step 5's integral as given, the one number on the page not done by hand — then §2, which defines the set Step 3 built. End it with self-check 4, and by saying, page closed, why the tip $(1,1)$ is not a configuration and why the lens removes no dimension from the torus while contact removes one. The second pass is sessions 3–4: §1 and §1.5 (Grübler's count, the torus and the task space), §3's constraints — come back to §3 before ch.13 — and then the rest of the self-check and the problem set.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], with its frozen numbers: a planar 2R arm — two revolute (R) joints turning in one plane — with $L_1 = L_2 = 1\,\mathrm{m}$, base at the origin, $\theta_1$ measured from the $+x$ axis and $\theta_2$ the elbow angle relative to link 1. Elbow and tip are then

$$e(\theta) = (\cos\theta_1,\ \sin\theta_1), \qquad p(\theta) = e(\theta) + (\cos(\theta_1{+}\theta_2),\ \sin(\theta_1{+}\theta_2))$$

because each unit-length link contributes one unit vector at its own absolute angle, and the absolute angle of link 2 is $\theta_1 + \theta_2$. At the catalog pose $\theta = (0°, 90°)$ the elbow is at $(1,0)$ and the tip at $(1,1)$.

**The panel**, frozen here and reused by [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]], is the running task's wall: the rigid half-plane $x \ge 1$, whose face is the vertical line $x = 1$. That face contains the catalog target $(1,1)$. Both links are modelled as zero-thickness segments, so "collision" means a point of a link has $x > 1$.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 342" style="max-width:100%;height:auto" role="img" aria-label="Left, P2's workspace with the wall x = 1 tangent to the elbow circle and the arm in its two contact configurations A and B; right, the torus chart of (θ1, θ2) with the shaded C-obstacle lens and A and B on its contact boundary.">
  <rect x="206" y="37.5" width="45" height="220.5" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="206" y1="47.5" x2="216" y2="37.5"/><line x1="206" y1="57.5" x2="226" y2="37.5"/><line x1="206" y1="67.5" x2="236" y2="37.5"/><line x1="206" y1="77.5" x2="246" y2="37.5"/><line x1="206" y1="87.5" x2="251" y2="42.5"/><line x1="206" y1="97.5" x2="251" y2="52.5"/><line x1="206" y1="107.5" x2="251" y2="62.5"/><line x1="206" y1="117.5" x2="251" y2="72.5"/><line x1="206" y1="127.5" x2="251" y2="82.5"/><line x1="206" y1="137.5" x2="251" y2="92.5"/><line x1="206" y1="147.5" x2="251" y2="102.5"/><line x1="206" y1="157.5" x2="251" y2="112.5"/><line x1="206" y1="167.5" x2="251" y2="122.5"/><line x1="206" y1="177.5" x2="251" y2="132.5"/><line x1="206" y1="187.5" x2="251" y2="142.5"/><line x1="206" y1="197.5" x2="251" y2="152.5"/><line x1="206" y1="207.5" x2="251" y2="162.5"/><line x1="206" y1="217.5" x2="251" y2="172.5"/><line x1="206" y1="227.5" x2="251" y2="182.5"/><line x1="206" y1="237.5" x2="251" y2="192.5"/><line x1="206" y1="247.5" x2="251" y2="202.5"/><line x1="206" y1="257.5" x2="251" y2="212.5"/><line x1="215.5" y1="258" x2="251" y2="222.5"/><line x1="225.5" y1="258" x2="251" y2="232.5"/><line x1="235.5" y1="258" x2="251" y2="242.5"/><line x1="245.5" y1="258" x2="251" y2="252.5"/></g>
  <line x1="206" y1="37.5" x2="206" y2="258" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="116" cy="150" r="90" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.55"/>
  <polyline points="116,150 116,60 206,60" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round" opacity="0.45"/>
  <polyline points="116,150 206,150 206,60" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="116" cy="150" r="5" fill="currentColor"/>
  <circle cx="206" cy="150" r="3.8" fill="currentColor"/>
  <circle cx="116" cy="60" r="3.8" fill="currentColor" fill-opacity="0.45"/>
  <circle cx="206" cy="60" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <line x1="190.7" y1="177" x2="203.5" y2="153" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"><line x1="368" y1="50" x2="368" y2="250"/><line x1="318" y1="200" x2="518" y2="200"/><line x1="418" y1="50" x2="418" y2="250"/><line x1="318" y1="150" x2="518" y2="150"/><line x1="468" y1="50" x2="468" y2="228"/><line x1="318" y1="100" x2="518" y2="100"/></g>
  <path d="M368 100 L368 99 L368.1 98 L368.2 97 L368.3 96.1 L368.4 95.2 L368.6 94.3 L368.8 93.5 L369.1 92.7 L369.4 92 L369.7 91.2 L370.1 90.6 L370.4 89.9 L370.9 89.3 L371.3 88.7 L371.8 88.1 L372.3 87.6 L372.9 87.1 L373.4 86.6 L374.1 86.2 L374.7 85.7 L375.4 85.4 L376.1 85 L376.8 84.7 L377.5 84.4 L378.3 84.2 L379.1 84 L380 83.8 L380.8 83.6 L381.7 83.5 L382.6 83.4 L383.6 83.4 L384.5 83.3 L385.5 83.3 L386.5 83.4 L387.6 83.5 L388.6 83.6 L389.7 83.8 L390.8 84 L391.9 84.2 L393 84.5 L394.1 84.8 L395.3 85.1 L396.5 85.5 L397.7 86 L398.9 86.5 L400.1 87 L401.3 87.6 L402.5 88.2 L403.8 88.9 L405.1 89.7 L406.3 90.4 L407.6 91.3 L408.9 92.2 L410.2 93.1 L411.5 94.1 L412.8 95.2 L414.1 96.3 L415.4 97.5 L416.7 98.7 L418 100 L419.3 101.3 L420.6 102.7 L421.9 104.2 L423.2 105.7 L424.5 107.2 L425.8 108.8 L427.1 110.4 L428.4 112.1 L429.7 113.8 L430.9 115.5 L432.2 117.3 L433.5 119.1 L434.7 121 L435.9 122.8 L437.1 124.7 L438.3 126.7 L439.5 128.6 L440.7 130.5 L441.9 132.5 L443 134.5 L444.1 136.4 L445.2 138.4 L446.3 140.4 L447.4 142.4 L448.4 144.4 L449.5 146.3 L450.5 148.3 L451.5 150.2 L452.4 152.2 L453.4 154.1 L454.3 156 L455.2 157.9 L456 159.8 L456.9 161.7 L457.7 163.5 L458.5 165.3 L459.2 167.1 L459.9 168.9 L460.6 170.6 L461.3 172.4 L461.9 174 L462.6 175.7 L463.1 177.3 L463.7 178.9 L464.2 180.5 L464.7 182 L465.1 183.5 L465.6 185 L465.9 186.4 L466.3 187.8 L466.6 189.2 L466.9 190.5 L467.2 191.8 L467.4 193.1 L467.6 194.3 L467.7 195.5 L467.8 196.7 L467.9 197.8 L468 198.9 L468 200 L468 201 L467.9 202 L467.8 203 L467.7 203.9 L467.6 204.8 L467.4 205.7 L467.2 206.5 L466.9 207.3 L466.6 208 L466.3 208.8 L465.9 209.4 L465.6 210.1 L465.1 210.7 L464.7 211.3 L464.2 211.9 L463.7 212.4 L463.1 212.9 L462.6 213.4 L461.9 213.8 L461.3 214.3 L460.6 214.6 L459.9 215 L459.2 215.3 L458.5 215.6 L457.7 215.8 L456.9 216 L456 216.2 L455.2 216.4 L454.3 216.5 L453.4 216.6 L452.4 216.6 L451.5 216.7 L450.5 216.7 L449.5 216.6 L448.4 216.5 L447.4 216.4 L446.3 216.2 L445.2 216 L444.1 215.8 L443 215.5 L441.9 215.2 L440.7 214.9 L439.5 214.5 L438.3 214 L437.1 213.5 L435.9 213 L434.7 212.4 L433.5 211.8 L432.2 211.1 L430.9 210.3 L429.7 209.6 L428.4 208.7 L427.1 207.8 L425.8 206.9 L424.5 205.9 L423.2 204.8 L421.9 203.7 L420.6 202.5 L419.3 201.3 L418 200 L416.7 198.7 L415.4 197.3 L414.1 195.8 L412.8 194.3 L411.5 192.8 L410.2 191.2 L408.9 189.6 L407.6 187.9 L406.3 186.2 L405.1 184.5 L403.8 182.7 L402.5 180.9 L401.3 179 L400.1 177.2 L398.9 175.3 L397.7 173.3 L396.5 171.4 L395.3 169.5 L394.1 167.5 L393 165.5 L391.9 163.6 L390.8 161.6 L389.7 159.6 L388.6 157.6 L387.6 155.6 L386.5 153.7 L385.5 151.7 L384.5 149.8 L383.6 147.8 L382.6 145.9 L381.7 144 L380.8 142.1 L380 140.2 L379.1 138.3 L378.3 136.5 L377.5 134.7 L376.8 132.9 L376.1 131.1 L375.4 129.4 L374.7 127.6 L374.1 126 L373.4 124.3 L372.9 122.7 L372.3 121.1 L371.8 119.5 L371.3 118 L370.9 116.5 L370.4 115 L370.1 113.6 L369.7 112.2 L369.4 110.8 L369.1 109.5 L368.8 108.2 L368.6 106.9 L368.4 105.7 L368.3 104.5 L368.2 103.3 L368.1 102.2 L368 101.1 L368 100 Z" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
  <rect x="318" y="50" width="200" height="200" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="318" y1="250" x2="318" y2="254"/><line x1="314" y1="250" x2="318" y2="250"/><line x1="368" y1="250" x2="368" y2="254"/><line x1="314" y1="200" x2="318" y2="200"/><line x1="418" y1="250" x2="418" y2="254"/><line x1="314" y1="150" x2="318" y2="150"/><line x1="468" y1="250" x2="468" y2="254"/><line x1="314" y1="100" x2="318" y2="100"/><line x1="518" y1="250" x2="518" y2="254"/><line x1="314" y1="50" x2="318" y2="50"/></g>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-linejoin="round"><polyline points="313,78 318,72 323,78"/><polyline points="513,78 518,72 523,78"/><polyline points="336,45 342,50 336,55"/><polyline points="343,45 349,50 343,55"/><polyline points="336,245 342,250 336,255"/><polyline points="343,245 349,250 343,255"/></g>
  <circle cx="418" cy="100" r="4.5" fill="currentColor"/>
  <circle cx="468" cy="200" r="4.5" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"/>
  <line x1="346.9" y1="73.3" x2="369.8" y2="87.1" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <line x1="468" y1="206" x2="468" y2="230" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18" font-size="12">Workspace</text>
    <text x="300" y="18" font-size="12">C-space chart, cut-open torus</text>
    <text x="230.5" y="31.5" text-anchor="middle">wall x = 1</text>
    <text x="109" y="168" text-anchor="end">base (0, 0)</text>
    <text x="109" y="53" text-anchor="end" opacity="0.75">(0, 1)</text>
    <text x="197" y="49" text-anchor="end">target (1, 1)</text>
    <text x="197" y="142" text-anchor="end">A</text>
    <text x="124" y="81" opacity="0.75">B</text>
    <text x="188.7" y="190" text-anchor="end">tangent at (1, 0)</text>
    <text x="116" y="214.8" text-anchor="middle" opacity="0.8">elbow circle, r = 1</text>
    <text x="318" y="268" text-anchor="middle">−180°</text>
    <text x="311" y="254" text-anchor="end">−180°</text>
    <text x="368" y="268" text-anchor="middle">−90°</text>
    <text x="311" y="204" text-anchor="end">−90°</text>
    <text x="418" y="268" text-anchor="middle">0°</text>
    <text x="311" y="154" text-anchor="end">0°</text>
    <text x="468" y="268" text-anchor="middle">90°</text>
    <text x="311" y="104" text-anchor="end">90°</text>
    <text x="518" y="268" text-anchor="middle">180°</text>
    <text x="311" y="54" text-anchor="end">180°</text>
    <text x="418" y="284" text-anchor="middle" font-size="12">θ<tspan dy="3.5">1</tspan></text>
    <text x="311" y="36" text-anchor="end" font-size="12">θ<tspan dy="3.5">2</tspan></text>
    <text x="425" y="93">A (0°, 90°)</text>
    <text x="468" y="242" text-anchor="middle">B (90°, −90°)</text>
    <text x="340.2" y="68.9" text-anchor="middle">contact</text>
    <text x="418" y="142.2" text-anchor="middle">C<tspan dy="3.5">obs</tspan></text>
    <text x="419.7" y="162.2" text-anchor="middle">18.478 %</text>
    <text x="12" y="300" opacity="0.9">A = (0°, 90°): link 2 lies flush along the face · B = (90°, −90°): only the tip touches.</text>
    <text x="12" y="316" opacity="0.9">Both have d = 0, so both lie on the contact curve. Shaded: cos θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">+ cos(θ</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">+θ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">) &gt; 1.</tspan></text>
    <text x="12" y="332" opacity="0.9">Matching arrows glue the edges (left = right, top = bottom): the square is the torus T².</text>
  </g>
</svg>

Left, P2's workspace: the wall $x = 1$ is tangent to the elbow circle at $(1,0)$, and the arm reaches the target $(1,1)$ in two contact configurations — A at $(0°, 90°)$ with link 2 flush along the face, B at $(90°, -90°)$ touching it only at the tip. Right, the cut-open torus of $(\theta_1, \theta_2)$, its matching edges glued: the shaded C-obstacle $\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1$ is a lens over $\theta_1 \in (-90°, 90°)$ that pinches to a point at each end and blocks 18.478 % of the torus; A lies on its contact boundary, and B is its right-hand pinch at $\theta_1 = 90°$, on the boundary too, not inside.

### Worked case · 대상으로 한 번 끝까지

**Step 1 — the dimension.** Grübler's formula (§1) counts a mechanism's degrees of freedom (dof) from its links and joints, and it counts the ground as a link, so P2 as an open chain has $N = 3$ links (ground, upper arm, forearm), $J = 2$ revolute joints (here $J$ counts joints; the $J$ of [[02-foundations/manipulator-kinematics-dynamics|10 §1]] and of ch.5 is the Jacobian), each allowing $f_i = 1$ freedom, and $m = 3$, the freedoms of a free rigid body in the plane:

$$\text{dof} = m(N - 1 - J) + \sum_i f_i = 3(3 - 1 - 2) + (1 + 1) = 0 + 2 = 2$$

so P2's configuration space is two-dimensional, and two numbers $(\theta_1, \theta_2)$ are a complete configuration. The first term vanishes because an open serial chain has $J = N - 1$, which is the pattern below.

**Step 2 — the shape.** Each joint angle lives on a circle $S^1$, and the two are independent, so $\mathcal{C} = S^1 \times S^1 = T^2$, a torus. The chart above is the torus cut open; every quantity on this page must be read modulo $360°$ in both axes.

**Step 3 — the C-obstacle, derived.** A configuration is in collision when some point of the arm has $x > 1$. The $x$-coordinate along a straight segment is linear in the parameter, so its maximum over a segment is attained at an endpoint, and the arm's three endpoints are the base $(x = 0)$, the elbow, and the tip. Therefore the deepest penetration is

$$d(\theta) = \max\bigl(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)\bigr) - 1$$

and the configuration collides exactly when $d(\theta) > 0$; $d$ is a penetration depth, positive inside the panel and zero at contact, the opposite sign of MR's signed distance (§2's Deeper note). Now simplify: $\cos\theta_1 \le 1$ always, with equality only at $\theta_1 = 0$, so the elbow term can never make $d$ positive — link 1 can touch the wall but never cross it, which is the tangency drawn in the left panel. The test collapses to one inequality:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in T^2 \;:\; \cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\,\}$$

because only the tip's $x$-coordinate can exceed the wall. Note that $L_1 = 1$ equals the wall distance; that is a fact about the catalog, not a general theorem, and the problem set breaks it.

**Step 4 — the boundary, in numbers.** Put $\varphi = \theta_1 + \theta_2$, the forearm's absolute angle. The boundary $\cos\theta_1 + \cos\varphi = 1$ solves as $\varphi = \pm\arccos(1 - \cos\theta_1)$, which has a solution only when $0 \le 1 - \cos\theta_1 \le 1$, i.e. $\cos\theta_1 \ge 0$:

| $\theta_1$ | $\cos\theta_1$ | needed $\cos\varphi$ | $\varphi$ | $\theta_2 = \varphi - \theta_1$ |
|---:|---:|---:|---:|---|
| $0°$ | $1$ | $0$ | $\pm 90°$ | $+90°$ or $-90°$ |
| $30°$ | $0.8660$ | $0.1340$ | $\pm 82.30°$ | $52.30°$ or $-112.30°$ |
| $60°$ | $0.5$ | $0.5$ | $\pm 60°$ | $0°$ or $-120°$ |
| $90°$ | $0$ | $1$ | $0°$ | $-90°$ (the pinch) |
| $>90°$ | $<0$ | $>1$ | none | region is empty |

The row $\theta_1 = 60°,\ \theta_2 = 0°$ is worth checking by hand: the arm is straight at $60°$, so the tip is at $(2\cos 60°,\ 2\sin 60°) = (1,\ 1.732)$, exactly on the face. The rows mirror for negative $\theta_1$, so the obstacle is an open lens spanning $\theta_1 \in (-90°, 90°)$ — open because Step 3's inequality is strict, so the contact curve bounds it without belonging to it — and that boundary pinches to a single point at each end, $\theta_1 = \pm 90°$. The right-hand pinch, the table's $\theta_1 = 90°$ row, is contact B $= (90°, -90°)$ itself.

**Step 5 — how much of the torus is lost.** The change of variables $(\theta_1, \theta_2) \mapsto (\theta_1, \varphi)$ is the linear map $\begin{pmatrix}1&0\\1&1\end{pmatrix}$, whose determinant is $1$, so it preserves area on the torus, and the blocked area is

$$\operatorname{area}(\mathcal{C}_{\text{obs}}) = \int_{-\pi/2}^{\pi/2} 2\arccos(1 - \cos u)\,du = 7.2949\ \mathrm{rad}^2$$

since for each admissible $\theta_1 = u$ the forbidden $\varphi$ interval has length $2\arccos(1-\cos u)$. The integral is evaluated numerically (any quadrature rule gives it to four places); it is the one number on this page not done by hand, and the problem set never asks for it. The whole torus has area $4\pi^2 = 39.478\ \mathrm{rad}^2$, so the panel costs **18.478 %** of P2's configuration space.

**Step 6 — the two contact configurations.** Both inverse-kinematics solutions for the tip at $(1,1)$ — the joint angles that put the tip there; [[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6]] derives why there are exactly these two, and here they are only checked — sit on the boundary, and the arithmetic is one line each:

- $\theta = (0°, 90°)$: $\cos 0° + \cos 90° = 1 + 0 = 1$, so $d = 0$.
- $\theta = (90°, -90°)$: $\cos 90° + \cos 0° = 0 + 1 = 1$, so $d = 0$.

They are the same point of task space and two different points of C-space, and they are not equivalent contacts: at $(0°,90°)$ link 2 lies flush along the face over its whole length, while at $(90°,-90°)$ only the tip touches. The C-space picture says "both on $\partial\mathcal{C}_{\text{obs}}$" and stops; which contact the tool actually makes is a workspace question.

**Step 7 — what contact does to the dimension.** Requiring the tip to stay on the face is the single equation $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$, one independent holonomic constraint (an equation on the configuration alone, defined in §3), so the set of configurations that maintain contact has dimension $2 - 1 = 1$: it is exactly the boundary curve drawn in the picture. The obstacle *region* removes no dimension — it is an open subset of a 2-D space and is still 2-D. **An inequality carves; an equality reduces.** That distinction is the whole content of §3.

### 1. Configuration, degrees of freedom, and Grübler

A planner, a controller and a learned policy all need one list of numbers that says where the whole robot is, and two shortcuts fail on P2: the tip position $(1,1)$ cannot tell contact A from contact B, and the joint-angle chart read as a flat plane sends the move from $(170°, 0°)$ to $(-170°, 0°)$ through the panel.

*In one sentence:* that list is the configuration, the set of all of them is the configuration space, its dimension is the dof that Grübler's formula counts, and its shape — a torus for P2 — decides which configurations are near each other.

- **Configuration** = a complete specification of every point of the robot; the minimum
  number of coordinates needed = **degrees of freedom (dof)**. C-space = the set of all
  configurations.
- **Grübler's formula**: for a mechanism of $N$ links **counting the ground link** and $J$ joints with joint freedoms $f_i$:
  $\text{dof} = m(N - 1 - J) + \sum_i f_i$ ($m = 3$ planar, $6$ spatial), worked below on a four-bar and a six-joint arm.

> **Configuration space and degrees of freedom, defined.** The **configuration space** (C-space) $\mathcal{C}$ is *a set*: every configuration the robot can take, where a **configuration** is a **complete** specification of the position of every point of the robot. The **degrees of freedom** are *a number*, the dimension of $\mathcal{C}$: the **smallest** count of **real-valued** coordinates that represents a configuration (MR Def. 2.1). Grübler's formula counts it for rigid links and joints (MR §2.2.2):
>
> $$\text{dof} = m(N - 1 - J) + \sum_{i=1}^{J} f_i$$
>
> where $m$ is a free rigid body's dof ($3$ planar, $6$ spatial), $N$ the links **with the ground counted**, $J$ the joints and $f_i$ joint $i$'s freedoms; the $N - 1$ moving links start with $m(N-1)$ freedoms and each joint removes $m - f_i$, so the count is exact only when those removals are **independent**, and a lower bound otherwise.
>
> - **Example**: P2, $3(3 - 1 - 2) + 2 = 2$: $(\theta_1, \theta_2)$ is a complete configuration.
> - **Non-example**: the tip position $(1,1)$, two real numbers but not a configuration: $(0°, 90°)$ and $(90°, -90°)$ both put the tip there (Step 6). A policy whose state is the tip cannot tell A, link 2 flush on the face, from B, touching only at the tip.

> [!example] Worked example · 계산 예제
> Grübler: $\text{dof} = m(N-1-J) + \sum_i f_i$, with the ground counted in $N$.
> - **Planar four-bar** (MR Example 2.3): $m = 3$, links $N = 4$ (ground + crank + coupler + rocker), $J = 4$ revolute joints, each $f_i = 1$. $3(4-1-4) + 4 = -3 + 4 = 1$. Fix the crank angle and the whole loop is determined.
> - **Spatial 6R arm**: $m = 6$, links $N = 7$ (base + 6 moving links), $J = 6$ revolute joints, each $f_i = 1$. $6(7-1-6) + 6 = 0 + 6 = 6$ — enough to place the tool at any position and orientation in its reachable workspace.
>
> **Pattern**: for an open serial chain $J = N - 1$, so the first term vanishes and dof is just $\sum_i f_i$. Each closed loop subtracts constraints, which is why the four-bar's 4 joints give only 1 dof. The formula assumes independent constraints, and special geometry can break it: add a third link to a parallelogram linkage, parallel to and as long as the two cranks, and Grübler counts $N = 5$, $J = 6$, so $3(5-1-6) + 6 = 0$ dof — yet the linkage still moves with 1, because the extra link's constraints repeat ones the parallelogram already imposes (MR Example 2.6). For such mechanisms Grübler is only a lower bound.

- **Topology matters**: a 2R arm's C-space is a torus ($T^2 = S^1 \times S^1$), not a plane —
  angles wrap. This is exactly why naive angle regression breaks
  ([[02-foundations/se3-geometry|8. SE(3) §2]]) and why "C-space distance" needs care.

> **C-space topology, defined.** The **topology** of a C-space is *a property of the space itself*, not of its coordinates: two spaces share it when one can be **deformed continuously** into the other **without cutting or gluing** (MR §2.3.1). Two facts fix it for a 2R arm: each angle **wraps**, $\theta_i$ and $\theta_i + 360°$ being one configuration, so each joint lives on a circle $S^1$; and the joints are **independent**, so the space is the product of the circles.
>
> $$\mathcal{C}_{\text{P2}} = S^1 \times S^1 = T^2, \qquad (\theta_1,\ \theta_2) \sim (\theta_1 + 360°\,k_1,\ \theta_2 + 360°\,k_2),\ \ k_1, k_2 \in \mathbb{Z}$$
>
> where $T^2$ is the torus and $\sim$ reads "is the same configuration as"; it is a torus because P2 has no joint limits, which would turn each circle into a closed interval.
>
> - **Example**: $(170°, 0°)$ and $(-170°, 0°)$ are $20°$ apart on the torus; the short move swings the straight arm past $\theta_1 = 180°$, away from the panel, and stays free.
> - **Non-example**: the square chart read as the plane $\mathbb{R}^2$. There the two points are $340°$ apart, and the straight line between them passes $\theta_1 = 0$, where the straight arm is $1\,\mathrm{m}$ inside the panel: a planner interpolating in the chart takes the long way, through the wall.

The figure draws the box's example and non-example on P2.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="Left, the straight P2 arm at θ1 = 170°, 180° and −170°, the short move, and at 0°, midway along the long move, 1 m inside the wall; right, the torus chart with (170°, 0°) and (−170°, 0°) joined by the 20° path across the glued edge and by the 340° chart line through the lens.">
  <defs><marker id="mr02wrE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <rect x="155" y="48.8" width="58.5" height="202.5" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="155" y1="60.8" x2="167" y2="48.8"/><line x1="155" y1="72.8" x2="179" y2="48.8"/><line x1="155" y1="84.8" x2="191" y2="48.8"/><line x1="155" y1="96.8" x2="203" y2="48.8"/><line x1="155" y1="108.8" x2="213.5" y2="50.2"/><line x1="155" y1="120.8" x2="213.5" y2="62.2"/><line x1="155" y1="132.8" x2="213.5" y2="74.2"/><line x1="155" y1="144.8" x2="213.5" y2="86.2"/><line x1="155" y1="156.8" x2="213.5" y2="98.2"/><line x1="155" y1="168.8" x2="213.5" y2="110.2"/><line x1="155" y1="180.8" x2="213.5" y2="122.2"/><line x1="155" y1="192.8" x2="213.5" y2="134.2"/><line x1="155" y1="204.8" x2="213.5" y2="146.2"/><line x1="155" y1="216.8" x2="213.5" y2="158.2"/><line x1="155" y1="228.8" x2="213.5" y2="170.2"/><line x1="155" y1="240.8" x2="213.5" y2="182.2"/><line x1="156.5" y1="251.2" x2="213.5" y2="194.2"/><line x1="168.5" y1="251.2" x2="213.5" y2="206.2"/><line x1="180.5" y1="251.2" x2="213.5" y2="218.2"/><line x1="192.5" y1="251.2" x2="213.5" y2="230.2"/><line x1="204.5" y1="251.2" x2="213.5" y2="242.2"/></g>
  <line x1="155" y1="48.8" x2="155" y2="251.2" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="21.4,134.4 22.1,130.5 23.1,126.7 24.2,122.9 25.4,119.2 26.9,115.6 28.4,112 30.2,108.4 32.1,105 34.1,101.6 36.3,98.4 38.6,95.2 41.1,92.1 43.6,89.2 46.4,86.4 49.2,83.6 52.1,81.1 55.2,78.6 58.4,76.3 61.6,74.1 65,72.1 68.4,70.2 72,68.4 75.6,66.9 79.2,65.4 82.9,64.2 86.7,63.1 90.5,62.1 94.4,61.4 98.3,60.8 102.2,60.3 106.1,60.1 110,60 113.9,60.1 117.8,60.3 121.7,60.8 125.6,61.4 129.5,62.1 133.3,63.1 137.1,64.2 140.8,65.4 144.4,66.9 148,68.4 151.6,70.2 155,72.1 158.4,74.1 161.6,76.3 164.8,78.6 167.9,81.1 170.8,83.6 173.6,86.4 176.4,89.2 178.9,92.1 181.4,95.2 183.7,98.4 185.9,101.6 187.9,105 189.8,108.4 191.6,112 193.1,115.6 194.6,119.2 195.8,122.9 196.9,126.7 197.9,130.5 198.6,134.4 199.2,138.3 199.7,142.2 199.9,146.1 200,150 199.9,153.9 199.7,157.8 199.2,161.7 198.6,165.6 197.9,169.5 196.9,173.3 195.8,177.1 194.6,180.8 193.1,184.4 191.6,188 189.8,191.6 187.9,195 185.9,198.4 183.7,201.6 181.4,204.8 178.9,207.9 176.4,210.8 173.6,213.6 170.8,216.4 167.9,218.9 164.8,221.4 161.6,223.7 158.4,225.9 155,227.9 151.6,229.8 148,231.6 144.4,233.1 140.8,234.6 137.1,235.8 133.3,236.9 129.5,237.9 125.6,238.6 121.7,239.2 117.8,239.7 113.9,239.9 110,240 106.1,239.9 102.2,239.7 98.3,239.2 94.4,238.6 90.5,237.9 86.7,236.9 82.9,235.8 79.2,234.6 75.6,233.1 72,231.6 68.4,229.8 65,227.9 61.6,225.9 58.4,223.7 55.2,221.4 52.1,218.9 49.2,216.4 46.4,213.6 43.6,210.8 41.1,207.9 38.6,204.8 36.3,201.6 34.1,198.4 32.1,195 30.2,191.6 28.4,188 26.9,184.4 25.4,180.8 24.2,177.1 23.1,173.3 22.1,169.5 21.4,165.6" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.6" marker-end="url(#mr02wrE)"/>
  <polyline points="155,72.1 158.4,74.1 161.6,76.3 164.8,78.6 167.9,81.1 170.8,83.6 173.6,86.4 176.4,89.2 178.9,92.1 181.4,95.2 183.7,98.4 185.9,101.6 187.9,105 189.8,108.4 191.6,112 193.1,115.6 194.6,119.2 195.8,122.9 196.9,126.7 197.9,130.5 198.6,134.4 199.2,138.3 199.7,142.2 199.9,146.1 200,150 199.9,153.9 199.7,157.8 199.2,161.7 198.6,165.6 197.9,169.5 196.9,173.3 195.8,177.1 194.6,180.8 193.1,184.4 191.6,188 189.8,191.6 187.9,195 185.9,198.4 183.7,201.6 181.4,204.8 178.9,207.9 176.4,210.8 173.6,213.6 170.8,216.4 167.9,218.9 164.8,221.4 161.6,223.7 158.4,225.9 155,227.9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="4 3"/>
  <line x1="110" y1="150" x2="200" y2="150" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="7 4" opacity="0.8"/>
  <circle cx="155" cy="150" r="3.2" fill="currentColor" opacity="0.8"/>
  <circle cx="200" cy="150" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <line x1="110" y1="150" x2="21.4" y2="134.4" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" opacity="0.55"/>
  <circle cx="65.7" cy="142.2" r="2.8" fill="currentColor" opacity="0.55"/>
  <line x1="110" y1="150" x2="20" y2="150" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" opacity="1.0"/>
  <circle cx="65" cy="150" r="2.8" fill="currentColor" opacity="1.0"/>
  <line x1="110" y1="150" x2="21.4" y2="165.6" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" opacity="0.55"/>
  <circle cx="65.7" cy="157.8" r="2.8" fill="currentColor" opacity="0.55"/>
  <polyline points="21.4,134.4 21.1,135.9 20.9,137.5 20.7,139 20.5,140.6 20.3,142.2 20.2,143.7 20.1,145.3 20.1,146.9 20,148.4 20,150 20,151.6 20.1,153.1 20.1,154.7 20.2,156.3 20.3,157.8 20.5,159.4 20.7,161 20.9,162.5 21.1,164.1 21.4,165.6" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#mr02wrE)"/>
  <circle cx="110" cy="150" r="4.5" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.3"><line x1="367" y1="40" x2="367" y2="260"/><line x1="312" y1="205" x2="532" y2="205"/><line x1="422" y1="40" x2="422" y2="260"/><line x1="312" y1="150" x2="532" y2="150"/><line x1="477" y1="40" x2="477" y2="260"/><line x1="312" y1="95" x2="532" y2="95"/></g>
  <path d="M367 95 L367.9 87.9 L368.8 85.5 L369.8 83.8 L370.7 82.5 L371.6 81.5 L372.5 80.7 L373.4 79.9 L374.3 79.3 L375.2 78.8 L376.2 78.4 L377.1 78 L378 77.7 L378.9 77.4 L379.8 77.2 L380.8 77 L381.7 76.9 L382.6 76.8 L383.5 76.7 L384.4 76.7 L385.3 76.7 L386.2 76.7 L387.2 76.7 L388.1 76.8 L389 76.9 L389.9 77 L390.8 77.1 L391.8 77.3 L392.7 77.5 L393.6 77.7 L394.5 77.9 L395.4 78.2 L396.3 78.4 L397.2 78.7 L398.2 79 L399.1 79.4 L400 79.7 L400.9 80.1 L401.8 80.5 L402.8 80.9 L403.7 81.4 L404.6 81.8 L405.5 82.3 L406.4 82.8 L407.3 83.4 L408.2 83.9 L409.2 84.5 L410.1 85.1 L411 85.7 L411.9 86.4 L412.8 87 L413.8 87.7 L414.7 88.4 L415.6 89.2 L416.5 89.9 L417.4 90.7 L418.3 91.5 L419.2 92.4 L420.2 93.2 L421.1 94.1 L422 95 L422.9 95.9 L423.8 96.9 L424.8 97.9 L425.7 98.9 L426.6 99.9 L427.5 100.9 L428.4 102 L429.3 103.1 L430.2 104.2 L431.2 105.4 L432.1 106.5 L433 107.7 L433.9 108.9 L434.8 110.2 L435.8 111.4 L436.7 112.7 L437.6 114 L438.5 115.3 L439.4 116.7 L440.3 118 L441.2 119.4 L442.2 120.8 L443.1 122.3 L444 123.7 L444.9 125.2 L445.8 126.7 L446.8 128.2 L447.7 129.8 L448.6 131.3 L449.5 132.9 L450.4 134.5 L451.3 136.1 L452.2 137.8 L453.2 139.5 L454.1 141.2 L455 142.9 L455.9 144.6 L456.8 146.4 L457.8 148.2 L458.7 150 L459.6 151.8 L460.5 153.7 L461.4 155.6 L462.3 157.6 L463.2 159.5 L464.2 161.6 L465.1 163.6 L466 165.7 L466.9 167.9 L467.8 170.1 L468.8 172.3 L469.7 174.7 L470.6 177.1 L471.5 179.7 L472.4 182.3 L473.3 185.2 L474.2 188.3 L475.2 191.8 L476.1 196.1 L477 205 L476.1 212.1 L475.2 214.5 L474.2 216.2 L473.3 217.5 L472.4 218.5 L471.5 219.3 L470.6 220.1 L469.7 220.7 L468.8 221.2 L467.8 221.6 L466.9 222 L466 222.3 L465.1 222.6 L464.2 222.8 L463.2 223 L462.3 223.1 L461.4 223.2 L460.5 223.3 L459.6 223.3 L458.7 223.3 L457.8 223.3 L456.8 223.3 L455.9 223.2 L455 223.1 L454.1 223 L453.2 222.9 L452.2 222.7 L451.3 222.5 L450.4 222.3 L449.5 222.1 L448.6 221.8 L447.7 221.6 L446.8 221.3 L445.8 221 L444.9 220.6 L444 220.3 L443.1 219.9 L442.2 219.5 L441.2 219.1 L440.3 218.6 L439.4 218.2 L438.5 217.7 L437.6 217.2 L436.7 216.6 L435.8 216.1 L434.8 215.5 L433.9 214.9 L433 214.3 L432.1 213.6 L431.2 213 L430.2 212.3 L429.3 211.6 L428.4 210.8 L427.5 210.1 L426.6 209.3 L425.7 208.5 L424.8 207.6 L423.8 206.8 L422.9 205.9 L422 205 L421.1 204.1 L420.2 203.1 L419.2 202.1 L418.3 201.1 L417.4 200.1 L416.5 199.1 L415.6 198 L414.7 196.9 L413.8 195.8 L412.8 194.6 L411.9 193.5 L411 192.3 L410.1 191.1 L409.2 189.8 L408.2 188.6 L407.3 187.3 L406.4 186 L405.5 184.7 L404.6 183.3 L403.7 182 L402.8 180.6 L401.8 179.2 L400.9 177.7 L400 176.3 L399.1 174.8 L398.2 173.3 L397.2 171.8 L396.3 170.2 L395.4 168.7 L394.5 167.1 L393.6 165.5 L392.7 163.9 L391.8 162.2 L390.8 160.5 L389.9 158.8 L389 157.1 L388.1 155.4 L387.2 153.6 L386.2 151.8 L385.3 150 L384.4 148.2 L383.5 146.3 L382.6 144.4 L381.7 142.4 L380.8 140.5 L379.8 138.4 L378.9 136.4 L378 134.3 L377.1 132.1 L376.2 129.9 L375.2 127.7 L374.3 125.3 L373.4 122.9 L372.5 120.3 L371.6 117.7 L370.7 114.8 L369.8 111.7 L368.8 108.2 L367.9 103.9 Z" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
  <rect x="312" y="40" width="220" height="220" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-linejoin="round"><polyline points="307,128.5 312,122.5 317,128.5"/><polyline points="527,128.5 532,122.5 537,128.5"/><polyline points="507.7,35 513.7,40 507.7,45"/><polyline points="514.7,35 520.7,40 514.7,45"/><polyline points="507.7,255 513.7,260 507.7,265"/><polyline points="514.7,255 520.7,260 514.7,265"/></g>
  <line x1="525.9" y1="150" x2="318.1" y2="150" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.75"/>
  <line x1="458.7" y1="150" x2="385.3" y2="150" stroke="currentColor" stroke-width="2.6" stroke-dasharray="6 3"/>
  <line x1="525.9" y1="150" x2="532" y2="150" stroke="currentColor" stroke-width="3.2"/>
  <line x1="312" y1="150" x2="318.1" y2="150" stroke="currentColor" stroke-width="3.2"/>
  <circle cx="525.9" cy="150" r="4.2" fill="currentColor"/>
  <circle cx="318.1" cy="150" r="4.2" fill="currentColor"/>
  <circle cx="422" cy="150" r="3" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="312" y1="260" x2="312" y2="264"/><line x1="308" y1="260" x2="312" y2="260"/><line x1="367" y1="260" x2="367" y2="264"/><line x1="308" y1="205" x2="312" y2="205"/><line x1="422" y1="260" x2="422" y2="264"/><line x1="308" y1="150" x2="312" y2="150"/><line x1="477" y1="260" x2="477" y2="264"/><line x1="308" y1="95" x2="312" y2="95"/><line x1="532" y1="260" x2="532" y2="264"/><line x1="308" y1="40" x2="312" y2="40"/></g>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18" font-size="12">Workspace</text>
    <text x="300" y="18" font-size="12">C-space chart, cut-open torus</text>
    <text x="184.2" y="42.8" text-anchor="middle">wall x = 1</text>
    <text x="116" y="166">base</text>
    <text x="12" y="268.2">short move: θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 170° → 180° → −170°</tspan></text>
    <text x="12" y="284.2" opacity="0.85">tip stays 2.97 m or more from the face</text>
    <text x="218.5" y="138">θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 0°:</tspan></text>
    <text x="218.5" y="153">tip (2, 0),</text>
    <text x="218.5" y="168">d = 1 m</text>
    <text x="12" y="52" opacity="0.8">long move, tip path: 340°</text>
    <text x="521.9" y="141" text-anchor="end">(170°, 0°)</text>
    <text x="322.1" y="141">(−170°, 0°)</text>
    <text x="422" y="166" text-anchor="middle">d = 1 m</text>
    <text x="394.5" y="113.3" text-anchor="middle">C<tspan dy="3.5">obs</tspan></text>
    <text x="312" y="276" text-anchor="middle">−180°</text>
    <text x="305" y="264" text-anchor="end">−180°</text>
    <text x="422" y="276" text-anchor="middle">0°</text>
    <text x="305" y="154" text-anchor="end">0°</text>
    <text x="532" y="276" text-anchor="middle">180°</text>
    <text x="305" y="44" text-anchor="end">180°</text>
    <text x="422" y="291" text-anchor="middle" font-size="12">θ<tspan dy="3.5">1</tspan></text>
    <text x="305" y="32" text-anchor="end" font-size="12">θ<tspan dy="3.5">2</tspan></text>
    <text x="318" y="240">long move read flat: 340°,</text>
    <text x="318" y="254">inside the lens for |θ<tspan dy="3.5">1</tspan><tspan dy="-3.5">| &lt; 60°</tspan></text>
    <text x="526" y="62" text-anchor="end">short move: 20°,</text>
    <text x="526" y="76" text-anchor="end">across the glued edge,</text>
    <text x="526" y="90" text-anchor="end">free throughout</text>
  </g>
</svg>

The box's two moves on P2. Left, the short move turns the straight arm from $\theta_1 = 170°$ through $180°$ to $-170°$, behind the base, its tip never nearer than $2.97\,\mathrm{m}$ to the face, while the long move's tip sweeps the other $340°$ of the circle and crosses the wall; halfway, at $\theta_1 = 0°$, the tip is at $(2, 0)$, $1\,\mathrm{m}$ inside. Right, the same two moves on the chart: $20°$ across the glued edge, or $340°$ along the flat line $\theta_2 = 0$, which runs inside the lens for $|\theta_1| < 60°$, about a third of the way, and reaches the lens's deepest point, $d = 1\,\mathrm{m}$, at its centre.

How a configuration is written down — in the fewest numbers, or embedded in more numbers with constraints — is a choice with its own trap, folded below.

> [!note]- Deeper · 더 깊이
> **Explicit and implicit representations.** An **explicit** representation uses the minimal number of coordinates and may have singularities — e.g. Euler angles at gimbal lock, where two of the three angles turn the same axis ([[02-foundations/se3-geometry|8. SE(3) §2]]). An **implicit** one embeds the configuration in a higher-dimensional space and adds constraints — like a rotation matrix with $R^\top R = I$. MR consistently chooses implicit — the same choice modern robot learning makes.

### 1.5 Task space and workspace

A task is written where the tool acts — "put the tip on $(1,1)$" — not in joint angles, and a target can be a perfectly good point of that space yet out of the arm's reach, or reachable only with the wrong tool angle. This section keeps the two sets apart.

- **Task space vs C-space**: where the tool lives vs where the robot lives; the map
  between them is kinematics (ch.4–6). Keep *task space* apart from *workspace*: the task
  chooses the first, the robot's structure fixes the second.
- **Why the distinction matters**: points of the task space
  can lie outside the workspace entirely — which is exactly what makes a task infeasible
  for a given arm. A target 2 m from the base of an arm with 1 m of reach is a valid point
  of the task space but not of that arm's workspace.

> **Task space and workspace, defined.** Both are *sets of end-effector configurations* — MR's word for the tool's poses — not of robot configurations, each written in the end-effector freedoms the user chooses to represent (MR §2.5). The **task space** $\mathcal{X}$ is where the task is naturally written, **chosen by the task** independently of the robot. The **workspace** $\mathcal{W}$ is the set of end-effector configurations the robot **can reach**, fixed by its structure independently of the task.
>
> $$\mathcal{W} = \{\, f(\theta) \;:\; \theta \in \mathcal{C} \,\}$$
>
> where $f$ is the forward kinematics of [[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]] in the coordinates chosen for $\mathcal{W}$, so the workspace is the image of the C-space; when $\mathcal{X}$ and $\mathcal{W}$ share coordinates, a task point outside $\mathcal{W}$ is infeasible. The **reachable workspace** $f(\mathcal{C}_{\text{free}})$ keeps only §2's free configurations.
>
> - **Example**: "put the tip on $(1,1)$" lives in $\mathcal{X} = \mathbb{R}^2$, where P2's workspace is the disc of radius $L_1 + L_2 = 2\,\mathrm{m}$; $(1,1)$, at $1.414\,\mathrm{m}$, is inside. With the panel the reachable workspace is the part with $x \le 1$, and $(1,1)$ lies on its edge.
> - **Non-example**: the pose $(1, 1, 45°)$, tip on target with tool heading $\theta_1 + \theta_2 = 45°$, in the task space $\mathbb{R}^2 \times S^1$. In those coordinates P2's workspace has only headings $0°$ (B) and $90°$ (A) at $(1,1)$; $45°$ would put the elbow at $(0.293, 0.293)$, $0.414\,\mathrm{m}$ from the base instead of $1$. A reachable point with a prescribed tool angle can still be infeasible.

### 2. C-obstacles and free space, defined

Whether a planner's straight-line edge is legal is decided by the shape of the C-obstacle, not by the shape of the wall: [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] checks exactly this set, and this section defines it.

A **C-obstacle** is a *subset of the configuration space*, not of the workspace. Given a rigid obstacle $\mathcal{O}$ in the world and the set $\mathcal{A}(\theta)$ of world points the robot body occupies at configuration $\theta$, the definition has three conditions — it is a set of configurations; membership is decided by intersection of bodies; and only **penetration** counts, so the body must meet the obstacle's interior $\operatorname{int}\mathcal{O}$ and a configuration that merely touches the surface stays free (MR §10.1). Counting contact as free is this wiki's choice, because the running task ends in contact; MR and MoveIt often count contact as a collision instead, as the Deeper note below explains. Joint limits, where a robot has them, are C-obstacles too (MR §10.2.1), or they cut each circle to an interval as in §1's topology box (MR §2.3.1); MR models them either way, and P2 has none:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in \mathcal{C} \;:\; \mathcal{A}(\theta) \cap \operatorname{int}\mathcal{O} \neq \varnothing\,\}, \qquad \mathcal{C}_{\text{free}} = \mathcal{C} \setminus \mathcal{C}_{\text{obs}}$$

where $\mathcal{C}$ is the whole configuration space and, for the panel, $\operatorname{int}\mathcal{O}$ is $x > 1$, the collision test of the Running object, so $\mathcal{C}_{\text{free}}$ is everything the robot may legally be, contact included. The point of the definition is that it turns a robot of some shape moving among obstacles into a *point* moving in $\mathcal{C}_{\text{free}}$, which is why every planner in [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] is written for a point.

- **Example**: the lens derived above, $\{\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\}$, occupying 18.478 % of P2's torus. It was obtained not by drawing the wall in C-space — the wall has no picture there — but by evaluating the workspace collision test at each configuration.
- **Non-example**: the wall itself, $\{x \ge 1\}$. A workspace region is not a C-obstacle, and the two need not even have the same dimension: under MR's closed test, where touching counts, a point obstacle in a 2-D workspace becomes a *curve* in the 2-D C-space, the configurations whose arm passes through it; under this page's interior test a point has no interior and blocks nothing, and a small disc blocks a thin band around that curve. Nor does touching the wall put a configuration in the C-obstacle: at the contact configuration A $= (0°, 90°)$ all of link 2 lies on $x = 1$, inside $\{x \ge 1\}$, yet $d = 0$, so A is on the lens's boundary and in $\mathcal{C}_{\text{free}}$.

> [!note]- Deeper · 더 깊이
> **Why contact counts as free here, and the sign of $d$.** MR is not uniform on contact: its collision test counts $d = 0$ as collision (§10.2.2), §10.3 adds the boundary to $\mathcal{C}_{\text{free}}$ only as an exception, and §13.3.2.1 takes free space open and obstacles closed, as MoveIt's planning scene does by treating contact as failure ([[04-robotics/ros2/manipulation-moveit2|25.8 MoveIt 2]]). This wiki counts contact as free because the running task ends in contact, so its test asks for the interior. The sign differs too: on this page and on [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]], $d(\theta)$ is a **penetration depth**, positive inside the obstacle and zero at contact, while MR's contact-kinematics chapter writes $d(q)$ for the signed *distance*, positive when the bodies are apart. Same information, opposite sign — check which one a source means before comparing numbers.

### 3. Holonomic and nonholonomic constraints, defined

An inequality carves; an equality reduces: the tool held on the face is an equation on the joint angles, the arm kept out of the panel is an inequality, and a wheel that cannot slide sideways is an equation on velocities. Confusing the three is the standard way a dof count comes out wrong, and this section gives the one test that separates the two kinds of equation.

A **constraint** on a mechanism is a condition its motion must satisfy. Two kinds, distinguished by one test — whether the condition can be written without velocities. Both can be put in the same velocity form, a **Pfaffian constraint**, and the test asks whether that form integrates (MR §2.4):

$$A(\theta)\,\dot\theta = 0, \qquad \text{holonomic (integrable)} \iff A(\theta) = \Psi(\theta)\,\frac{\partial g}{\partial\theta}(\theta)\ \text{for some } g \text{ and invertible } \Psi(\theta)$$

where $\theta \in \mathbb{R}^n$, $A(\theta)$ is $k \times n$ with one row per constraint, $g: \mathbb{R}^n \to \mathbb{R}^k$, and $\Psi(\theta)$ is an invertible $k \times k$ matrix, an integrating factor (MR states the case $\Psi = I$); the test has this form because differentiating $g(\theta(t)) = 0$ in time gives exactly $\frac{\partial g}{\partial\theta}\dot\theta = 0$, so an integrable velocity constraint says nothing that $g(\theta) = 0$ did not. On P2 the contact constraint is $g(\theta) = \cos\theta_1 + \cos(\theta_1{+}\theta_2) - 1 = 0$, so its row is $A = \partial g/\partial\theta = (-\sin\theta_1 - \sin(\theta_1{+}\theta_2),\ -\sin(\theta_1{+}\theta_2))$, which at the catalog pose $(0°, 90°)$ is $(-1,\ -1)$: $A\dot\theta = -\dot\theta_1 - \dot\theta_2 = 0$ forces $\dot\theta_2 = -\dot\theta_1$, so the only allowed joint rates are multiples of $(1, -1)$, and with P2's Jacobian $J = \begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ ([[02-foundations/manipulator-kinematics-dynamics|10 §1]]) the rates $(1, -1)\,\mathrm{rad/s}$ give the tip velocity $J(1,-1) = (0, 1)\,\mathrm{m/s}$, straight up the face.

- A **holonomic constraint** is an equation on configuration alone, $g(\theta) = 0$. Each independent one reduces the dimension of the configuration space by one, because it confines $\theta$ to a level set of $g$, the configurations where $g$ keeps one value (here $0$). *Example*: P2's tip held on the panel face, $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$, leaving a 1-D contact curve. *Example*: a closed loop, which is why the four-bar has 1 dof and not 4.
- A **nonholonomic constraint** is an equation on velocity, $A(\theta)\dot\theta = 0$, that is *not* the time derivative of any $g(\theta) = 0$. It removes a direction of motion at every configuration but removes no dimension from the reachable set. *Example*: a wheel that cannot slide sideways ([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|ch.13]]): a car reaches every pose, just not along every path.
- **Non-example of the distinction**: "the tip must stay outside the panel" is neither, because it is an *inequality*. It removes no dimension and no direction; it deletes an open region.

**Wiki connections**: C-space is part of the state of every robot [[02-foundations/rl-basics|MDP]] — the configuration sits in the state beside the velocities — and some VLA action spaces are coordinates on it ([[01-canonical-papers/notes/4-vla/pi0|π0]]'s joint chunks), while others ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]]'s arm actions, end-effector position and rotation) live in §1.5's task space ([[02-foundations/se3-geometry|8. SE(3) §5]]).

### Self-check

1. How many numbers describe the configuration of a planar differential-drive robot, and what is the constraint?
2. Use Grübler's formula on a planar slider-crank (4 links, 3 revolute + 1 prismatic joint).
3. Why does the 2R arm's C-space being a torus $T^2$ rather than the plane $\mathbb{R}^2$ cause trouble for learned angle regression?
4. P2 is at $\theta = (45°, 0°)$. Compute $d(\theta)$ for the panel and say what the arm is doing.

> [!tip]- Answers
> 1. Three for the chassis: $(x, y, \theta)$ (five if the two wheel rolling angles are included, as MR §13.3 does). The nonholonomic constraint (no sideways slip) restricts *velocities*, not reachable chassis configurations — the robot can still reach any pose, just not by any path.
> 2. $\text{dof} = 3(4-1-4) + (3\cdot 1 + 1\cdot 1) = -3 + 4 = 1$. The prismatic joint contributes its one freedom exactly like a revolute one; what matters to the count is $f_i$, not the joint's kind.
> 3. $359°$ and $1°$ are neighbours on the circle but far apart in Euclidean distance, so a naive MSE regression is penalized enormously at the wrap point and learns a discontinuous target ([[02-foundations/se3-geometry|SE(3) §2]]).
> 4. The arm is straight at $45°$, so the tip is at $(\sqrt2, \sqrt2) = (1.4142, 1.4142)$ and $d = \cos 45° + \cos 45° - 1 = \sqrt2 - 1 = 0.4142\,\mathrm{m}$ — it is $41.4\,\mathrm{cm}$ inside the panel; along the line $\theta_2 = 0$ the lens is deepest at $\theta_1 = 0$, where $d = 1\,\mathrm{m}$.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same plant **P2**, but the panel is rebuilt 0.5 m further out: the wall is now $x \ge 1.5$.

1. **Draw.** The picture above, for the new wall. In the workspace panel, show that the wall no longer touches the elbow circle. In the C-space chart, shade the new obstacle and mark where it pinches. State in one sentence what happened to the catalog pose $(0°,90°)$.
2. **Derive.** (a) Write $d(\theta)$ for the new wall and argue again that only the tip term matters. (b) The boundary condition $\cos\theta_1 + \cos\varphi = 1.5$: find the two values of $\theta_1$ where the obstacle pinches, and the $\theta_2$ values on the boundary at $\theta_1 = 0°$ and $\theta_1 = 30°$. (c) For the *straight* arm, $\theta_2 = 0°$, find the range of $\theta_1$ that penetrates.
3. **Interpret.** The blocked fraction of the torus falls from 18.478 % to 8.515 %. Does the C-obstacle's *dimension* change? Does P2's dof change? And does the running task — put the tool on the panel at the catalog target — still have a solution?

> [!note]- How to draw it · 그리는 법
> - Two panels side by side: the workspace on the left, the C-space chart on the right.
> - Workspace: the base at the origin, the unit circle the elbow traces, and the wall as a vertical line at its $x$, hatched on the side the arm must not enter. Say whether the wall touches that circle — the wall of the picture above, $x = 1$, is tangent to it at $(1,0)$.
> - Draw each configuration link by link — elbow at $(\cos\theta_1, \sin\theta_1)$, tip one more unit along the absolute angle $\theta_1 + \theta_2$ — at least the catalog pose $(0°, 90°)$, and mark the target $(1,1)$.
> - Chart: a square with $\theta_1$ across and $\theta_2$ up, both from $-180°$ to $180°$, with matching arrows on the left and right edges and again on the top and bottom. Without the arrows the square is a rectangle, not the torus.
> - Shade the region where the arm penetrates the panel: a lens that pinches to a single point at each end. Mark the $\theta_1$ of both pinches (the picture above has them at $\pm 90°$).
> - Label the lens boundary "contact". A configuration with $d = 0$ is a dot on that curve, never inside the shading; one with $d < 0$ lies outside the lens.

> [!tip]- Solutions
> 1. Workspace: the elbow circle has radius 1 and the wall is at $x=1.5$, so the closest elbow point $(1,0)$ is $0.5\,\mathrm{m}$ clear — link 1 is now strictly free everywhere. C-space: a smaller lens, pinching at $\theta_1 = \pm 60°$. The catalog pose has $\cos 0° + \cos 90° = 1 < 1.5$, so $d = -0.5$: it is now an interior free configuration, no longer a contact configuration.
> 2. (a) $d(\theta) = \max(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)) - 1.5$; $\cos\theta_1 \le 1 < 1.5$, so the elbow term is always negative and only the tip can offend. (b) Pinch where $\cos\varphi$ must equal 1, i.e. $\cos\theta_1 = 0.5$, so $\theta_1 = \pm 60°$. At $\theta_1 = 0°$: $\cos\varphi = 0.5$, $\varphi = \pm 60°$, so $\theta_2 = \pm 60°$. At $\theta_1 = 30°$: $\cos\varphi = 1.5 - 0.8660 = 0.6340$, $\varphi = \pm 50.66°$, so $\theta_2 = 20.66°$ or $-80.66°$. (c) Straight arm: tip at $2\cos\theta_1 > 1.5$, i.e. $\cos\theta_1 > 0.75$, so $|\theta_1| < 41.41°$.
> 3. The dimension does not change: $\mathcal{C}_{\text{obs}}$ is an open subset of a 2-D space and stays 2-D, smaller but not thinner. P2's dof is still 2, because Grübler counts links and joints and neither moved — obstacles are inequalities and never enter the count. The task loses its solution as stated: the catalog target $(1,1)$ has $x = 1 < 1.5$ and is no longer on the face, so the contact target must be respecified. The nearest face point straight out is $(1.5, 1)$, at radius $\sqrt{1.5^2+1^2} = 1.803 < 2$, so it is still inside the workspace and the new task is feasible.

### Sources

- K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — ch.2, §2.1–§2.5 (degrees of freedom, Grübler's formula, the topology of C-space, Pfaffian constraints, task space and workspace), with §10.1–§10.3 and §13.3 for the C-obstacle and contact conventions of §2; the [[04-robotics/modern-robotics-book|book guide]] links the free PDF.
- The lens, its 18.478 % share and every other number on this page were computed here from P2's catalog numbers and the panel $x \ge 1$; recompute them rather than trusting them.

## 한국어

**핵심 질문**: 로봇이 취할 수 있는 모든 "위치", 곧 컨피규레이션의 공간은 무엇이고, 그 모양은 어떠한가?

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 모션·과제 계획 층의 맨 아래층이고, "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계를 받친다. P2([[02-foundations/lab-plants|0.6]]의 두 링크 평면 팔)를 패널 쪽으로 옮기는 계획기는 모두 작업 영역이 아니라 이 페이지가 만드는 집합을 탐색한다([[physical-ai-map|피지컬 AI 지도]]의 계획 띠에 이 페이지의 자리가 있다). 이것이 없으면 팔을 벽 그림만 보고 계획하게 된다. $(\theta_1, \theta_2)$ 도표를 평평한 정사각형으로 읽으면 $(170°, 0°)$에서 $(-170°, 0°)$로 가는 이동이, 곧게 편 팔이 패널 안 $1\,\mathrm{m}$까지 들어가는 $\theta_1 = 0$을 지나 먼 길로 돌아간다. 원환면에는 자유로운 $20°$ 이동이 있는데도 그렇다(§1). 또 말단 $(1, 1)$만 기억하는 제어기는 링크 2가 면에 붙은 접촉 A와 말단만 닿는 접촉 B를 구별하지 못한다. 뒤 페이지들은 이 페이지를 절 단위로 가져다 쓴다. [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 §2]]는 바로 §2의 C-장애물을 검사하고, [[04-robotics/planning-decision-making|4. 계획 §2]]는 다섯 공간 가운데 하나로 컨피규레이션 공간을 세며, [[04-robotics/capstone-panel-contact|26. 캡스톤 §2]]는 §2의 렌즈 모양 C-장애물을 패널 위치 추정의 불확실성만큼 부풀리고, [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR 13장 §1]]은 §3의 비홀로노믹 제약에서 출발한다. 학위논문 경로([[07-research-program/index|7 §8]])에서 이 페이지는 블록 2, 곧 로보틱스 공통 트랙의 첫머리에 오는 로보틱스 회차 2–4다. 이 페이지를 마치면 P2의 자유도를 세고, 그 C-space를 원환면이라 부르고, 패널의 C-장애물과 1차원 접촉 집합을 손으로 유도하고, 컨피규레이션과 말단 위치를 구별할 수 있다.

> [!note] 처음이라면 · First pass
> 한 회차, 로보틱스 회차 2다. '이 페이지의 대상', 그림, '대상으로 한 번 끝까지'의 1–7단계를 답을 가린 채 손으로 풀되, 5단계의 적분은 주어진 값으로 받아들인다. 이 페이지에서 손으로 하지 않는 유일한 숫자다. 이어서 3단계가 만든 집합을 정의하는 §2를 읽는다. 회차는 스스로 점검 4번을 풀고, 페이지를 덮은 채 두 가지를 말하며 끝낸다. 말단 $(1,1)$은 왜 컨피규레이션이 아닌가, 그리고 렌즈는 원환면의 차원을 줄이지 않는데 접촉은 왜 하나를 줄이는가. 두 번째 읽기는 회차 3–4다. §1과 §1.5(그뤼블러 계산, 원환면, 작업 공간), §3의 제약(13장에 가기 전에 §3으로 돌아온다), 그리고 나머지 스스로 점검과 과제다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치(plant, 제어에서 제어 대상인 시스템을 부르는 말) **P2**를 고정된 숫자 그대로 쓴다. 평면 2R 팔, 곧 한 평면 안에서 도는 회전(revolute, R) 관절 둘로 된 팔이고, $L_1 = L_2 = 1\,\mathrm{m}$, 베이스는 원점, $\theta_1$은 $+x$축 기준, $\theta_2$는 링크 1에 대한 상대 엘보 각. 엘보와 말단은

$$e(\theta) = (\cos\theta_1,\ \sin\theta_1), \qquad p(\theta) = e(\theta) + (\cos(\theta_1{+}\theta_2),\ \sin(\theta_1{+}\theta_2))$$

이다. 길이 1인 링크가 각자의 절대각 방향 단위 벡터를 하나씩 더하고, 링크 2의 절대각이 $\theta_1 + \theta_2$이기 때문이다. 카탈로그 자세 $\theta = (0°, 90°)$에서 엘보는 $(1,0)$, 말단은 $(1,1)$.

**패널**은 여기서 고정하고 [[04-robotics/modern-robotics/ch10-motion-planning|10장]]이 그대로 쓴다. 관통 과제의 벽이며, 강체 반평면 $x \ge 1$이고 그 면은 수직선 $x = 1$이다. 이 면이 카탈로그 목표 $(1,1)$을 포함한다. 두 링크는 두께 0인 선분으로 모형화하므로, 충돌이란 링크의 어떤 점이 $x > 1$이 되는 것이다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 342" style="max-width:100%;height:auto" role="img" aria-label="왼쪽은 엘보 원에 접하는 벽 x = 1과 두 접촉 컨피규레이션 A, B를 그린 P2 작업 영역이고, 오른쪽은 칠한 C-장애물 렌즈와 그 접촉 경계 위의 A, B를 표시한 (θ1, θ2) 원환면 도표다.">
  <rect x="206" y="37.5" width="45" height="220.5" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="206" y1="47.5" x2="216" y2="37.5"/><line x1="206" y1="57.5" x2="226" y2="37.5"/><line x1="206" y1="67.5" x2="236" y2="37.5"/><line x1="206" y1="77.5" x2="246" y2="37.5"/><line x1="206" y1="87.5" x2="251" y2="42.5"/><line x1="206" y1="97.5" x2="251" y2="52.5"/><line x1="206" y1="107.5" x2="251" y2="62.5"/><line x1="206" y1="117.5" x2="251" y2="72.5"/><line x1="206" y1="127.5" x2="251" y2="82.5"/><line x1="206" y1="137.5" x2="251" y2="92.5"/><line x1="206" y1="147.5" x2="251" y2="102.5"/><line x1="206" y1="157.5" x2="251" y2="112.5"/><line x1="206" y1="167.5" x2="251" y2="122.5"/><line x1="206" y1="177.5" x2="251" y2="132.5"/><line x1="206" y1="187.5" x2="251" y2="142.5"/><line x1="206" y1="197.5" x2="251" y2="152.5"/><line x1="206" y1="207.5" x2="251" y2="162.5"/><line x1="206" y1="217.5" x2="251" y2="172.5"/><line x1="206" y1="227.5" x2="251" y2="182.5"/><line x1="206" y1="237.5" x2="251" y2="192.5"/><line x1="206" y1="247.5" x2="251" y2="202.5"/><line x1="206" y1="257.5" x2="251" y2="212.5"/><line x1="215.5" y1="258" x2="251" y2="222.5"/><line x1="225.5" y1="258" x2="251" y2="232.5"/><line x1="235.5" y1="258" x2="251" y2="242.5"/><line x1="245.5" y1="258" x2="251" y2="252.5"/></g>
  <line x1="206" y1="37.5" x2="206" y2="258" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="116" cy="150" r="90" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.55"/>
  <polyline points="116,150 116,60 206,60" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round" opacity="0.45"/>
  <polyline points="116,150 206,150 206,60" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="116" cy="150" r="5" fill="currentColor"/>
  <circle cx="206" cy="150" r="3.8" fill="currentColor"/>
  <circle cx="116" cy="60" r="3.8" fill="currentColor" fill-opacity="0.45"/>
  <circle cx="206" cy="60" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <line x1="190.7" y1="177" x2="203.5" y2="153" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.35"><line x1="368" y1="50" x2="368" y2="250"/><line x1="318" y1="200" x2="518" y2="200"/><line x1="418" y1="50" x2="418" y2="250"/><line x1="318" y1="150" x2="518" y2="150"/><line x1="468" y1="50" x2="468" y2="228"/><line x1="318" y1="100" x2="518" y2="100"/></g>
  <path d="M368 100 L368 99 L368.1 98 L368.2 97 L368.3 96.1 L368.4 95.2 L368.6 94.3 L368.8 93.5 L369.1 92.7 L369.4 92 L369.7 91.2 L370.1 90.6 L370.4 89.9 L370.9 89.3 L371.3 88.7 L371.8 88.1 L372.3 87.6 L372.9 87.1 L373.4 86.6 L374.1 86.2 L374.7 85.7 L375.4 85.4 L376.1 85 L376.8 84.7 L377.5 84.4 L378.3 84.2 L379.1 84 L380 83.8 L380.8 83.6 L381.7 83.5 L382.6 83.4 L383.6 83.4 L384.5 83.3 L385.5 83.3 L386.5 83.4 L387.6 83.5 L388.6 83.6 L389.7 83.8 L390.8 84 L391.9 84.2 L393 84.5 L394.1 84.8 L395.3 85.1 L396.5 85.5 L397.7 86 L398.9 86.5 L400.1 87 L401.3 87.6 L402.5 88.2 L403.8 88.9 L405.1 89.7 L406.3 90.4 L407.6 91.3 L408.9 92.2 L410.2 93.1 L411.5 94.1 L412.8 95.2 L414.1 96.3 L415.4 97.5 L416.7 98.7 L418 100 L419.3 101.3 L420.6 102.7 L421.9 104.2 L423.2 105.7 L424.5 107.2 L425.8 108.8 L427.1 110.4 L428.4 112.1 L429.7 113.8 L430.9 115.5 L432.2 117.3 L433.5 119.1 L434.7 121 L435.9 122.8 L437.1 124.7 L438.3 126.7 L439.5 128.6 L440.7 130.5 L441.9 132.5 L443 134.5 L444.1 136.4 L445.2 138.4 L446.3 140.4 L447.4 142.4 L448.4 144.4 L449.5 146.3 L450.5 148.3 L451.5 150.2 L452.4 152.2 L453.4 154.1 L454.3 156 L455.2 157.9 L456 159.8 L456.9 161.7 L457.7 163.5 L458.5 165.3 L459.2 167.1 L459.9 168.9 L460.6 170.6 L461.3 172.4 L461.9 174 L462.6 175.7 L463.1 177.3 L463.7 178.9 L464.2 180.5 L464.7 182 L465.1 183.5 L465.6 185 L465.9 186.4 L466.3 187.8 L466.6 189.2 L466.9 190.5 L467.2 191.8 L467.4 193.1 L467.6 194.3 L467.7 195.5 L467.8 196.7 L467.9 197.8 L468 198.9 L468 200 L468 201 L467.9 202 L467.8 203 L467.7 203.9 L467.6 204.8 L467.4 205.7 L467.2 206.5 L466.9 207.3 L466.6 208 L466.3 208.8 L465.9 209.4 L465.6 210.1 L465.1 210.7 L464.7 211.3 L464.2 211.9 L463.7 212.4 L463.1 212.9 L462.6 213.4 L461.9 213.8 L461.3 214.3 L460.6 214.6 L459.9 215 L459.2 215.3 L458.5 215.6 L457.7 215.8 L456.9 216 L456 216.2 L455.2 216.4 L454.3 216.5 L453.4 216.6 L452.4 216.6 L451.5 216.7 L450.5 216.7 L449.5 216.6 L448.4 216.5 L447.4 216.4 L446.3 216.2 L445.2 216 L444.1 215.8 L443 215.5 L441.9 215.2 L440.7 214.9 L439.5 214.5 L438.3 214 L437.1 213.5 L435.9 213 L434.7 212.4 L433.5 211.8 L432.2 211.1 L430.9 210.3 L429.7 209.6 L428.4 208.7 L427.1 207.8 L425.8 206.9 L424.5 205.9 L423.2 204.8 L421.9 203.7 L420.6 202.5 L419.3 201.3 L418 200 L416.7 198.7 L415.4 197.3 L414.1 195.8 L412.8 194.3 L411.5 192.8 L410.2 191.2 L408.9 189.6 L407.6 187.9 L406.3 186.2 L405.1 184.5 L403.8 182.7 L402.5 180.9 L401.3 179 L400.1 177.2 L398.9 175.3 L397.7 173.3 L396.5 171.4 L395.3 169.5 L394.1 167.5 L393 165.5 L391.9 163.6 L390.8 161.6 L389.7 159.6 L388.6 157.6 L387.6 155.6 L386.5 153.7 L385.5 151.7 L384.5 149.8 L383.6 147.8 L382.6 145.9 L381.7 144 L380.8 142.1 L380 140.2 L379.1 138.3 L378.3 136.5 L377.5 134.7 L376.8 132.9 L376.1 131.1 L375.4 129.4 L374.7 127.6 L374.1 126 L373.4 124.3 L372.9 122.7 L372.3 121.1 L371.8 119.5 L371.3 118 L370.9 116.5 L370.4 115 L370.1 113.6 L369.7 112.2 L369.4 110.8 L369.1 109.5 L368.8 108.2 L368.6 106.9 L368.4 105.7 L368.3 104.5 L368.2 103.3 L368.1 102.2 L368 101.1 L368 100 Z" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
  <rect x="318" y="50" width="200" height="200" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="318" y1="250" x2="318" y2="254"/><line x1="314" y1="250" x2="318" y2="250"/><line x1="368" y1="250" x2="368" y2="254"/><line x1="314" y1="200" x2="318" y2="200"/><line x1="418" y1="250" x2="418" y2="254"/><line x1="314" y1="150" x2="318" y2="150"/><line x1="468" y1="250" x2="468" y2="254"/><line x1="314" y1="100" x2="318" y2="100"/><line x1="518" y1="250" x2="518" y2="254"/><line x1="314" y1="50" x2="318" y2="50"/></g>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-linejoin="round"><polyline points="313,78 318,72 323,78"/><polyline points="513,78 518,72 523,78"/><polyline points="336,45 342,50 336,55"/><polyline points="343,45 349,50 343,55"/><polyline points="336,245 342,250 336,255"/><polyline points="343,245 349,250 343,255"/></g>
  <circle cx="418" cy="100" r="4.5" fill="currentColor"/>
  <circle cx="468" cy="200" r="4.5" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"/>
  <line x1="346.9" y1="73.3" x2="369.8" y2="87.1" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <line x1="468" y1="206" x2="468" y2="230" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18" font-size="12">작업 영역</text>
    <text x="300" y="18" font-size="12">C-space 도표 (잘라 편 원환면)</text>
    <text x="230.5" y="31.5" text-anchor="middle">벽 x = 1</text>
    <text x="109" y="168" text-anchor="end">베이스 (0, 0)</text>
    <text x="109" y="53" text-anchor="end" opacity="0.75">(0, 1)</text>
    <text x="197" y="49" text-anchor="end">목표 (1, 1)</text>
    <text x="197" y="142" text-anchor="end">A</text>
    <text x="124" y="81" opacity="0.75">B</text>
    <text x="188.7" y="190" text-anchor="end">(1, 0)에서 접함</text>
    <text x="116" y="214.8" text-anchor="middle" opacity="0.8">엘보 원, r = 1</text>
    <text x="318" y="268" text-anchor="middle">−180°</text>
    <text x="311" y="254" text-anchor="end">−180°</text>
    <text x="368" y="268" text-anchor="middle">−90°</text>
    <text x="311" y="204" text-anchor="end">−90°</text>
    <text x="418" y="268" text-anchor="middle">0°</text>
    <text x="311" y="154" text-anchor="end">0°</text>
    <text x="468" y="268" text-anchor="middle">90°</text>
    <text x="311" y="104" text-anchor="end">90°</text>
    <text x="518" y="268" text-anchor="middle">180°</text>
    <text x="311" y="54" text-anchor="end">180°</text>
    <text x="418" y="284" text-anchor="middle" font-size="12">θ<tspan dy="3.5">1</tspan></text>
    <text x="311" y="36" text-anchor="end" font-size="12">θ<tspan dy="3.5">2</tspan></text>
    <text x="425" y="93">A (0°, 90°)</text>
    <text x="468" y="242" text-anchor="middle">B (90°, −90°)</text>
    <text x="340.2" y="68.9" text-anchor="middle">접촉</text>
    <text x="418" y="142.2" text-anchor="middle">C<tspan dy="3.5">obs</tspan></text>
    <text x="419.7" y="162.2" text-anchor="middle">18.478 %</text>
    <text x="12" y="300" opacity="0.9">A = (0°, 90°): 링크 2가 면에 붙어 눕는다 · B = (90°, −90°): 말단만 닿는다.</text>
    <text x="12" y="316" opacity="0.9">둘 다 d = 0이라 접촉 곡선 위에 있다. 칠한 영역: cos θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">+ cos(θ</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">+θ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">) &gt; 1.</tspan></text>
    <text x="12" y="332" opacity="0.9">같은 화살표끼리 붙인다(왼쪽 = 오른쪽, 위 = 아래). 그래서 정사각형이 원환면 T²다.</text>
  </g>
</svg>

왼쪽 P2의 작업 영역에서 벽 $x = 1$은 엘보 원에 $(1,0)$에서 접하고, 팔은 두 접촉 컨피규레이션으로 목표 $(1,1)$에 닿는다 — $(0°, 90°)$의 A는 링크 2가 면에 붙어 눕고, $(90°, -90°)$의 B는 말단만 면에 닿는다. 오른쪽은 마주 보는 변끼리 붙인 $(\theta_1, \theta_2)$ 원환면을 잘라 편 도표다. 칠한 C-장애물 $\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1$은 $\theta_1 \in (-90°, 90°)$에 걸쳐 양 끝에서 한 점으로 오므라드는 렌즈로 원환면의 18.478 %를 막는다. A는 그 접촉 경계 위에 있고, B는 $\theta_1 = 90°$의 오른쪽 오므라든 점 자체로, 역시 안이 아니라 경계 위에 있다.

### 대상으로 한 번 끝까지 · Worked case

**1단계 — 차원.** 그뤼블러 공식(§1)은 링크와 관절로 기구의 자유도(dof)를 세고, 접지도 링크 하나로 센다. 그래서 열린 체인 P2는 링크 $N = 3$(접지, 상완, 전완), 회전관절 $J = 2$(여기서 $J$는 관절 수다. [[02-foundations/manipulator-kinematics-dynamics|10 §1]]과 5장의 $J$는 야코비안이다), 관절마다 허용하는 자유도 $f_i = 1$, 그리고 평면에서 자유로운 강체의 자유도 $m = 3$이다:

$$\text{dof} = m(N - 1 - J) + \sum_i f_i = 3(3 - 1 - 2) + (1 + 1) = 0 + 2 = 2$$

따라서 P2의 컨피규레이션 공간은 2차원이고, 숫자 두 개 $(\theta_1, \theta_2)$가 완전한 컨피규레이션이다. 열린 직렬 체인은 $J = N - 1$이라 첫 항이 사라지는데, 이것이 아래의 패턴이다.

**2단계 — 모양.** 각 관절각은 원 $S^1$ 위에 살고 둘은 독립이므로 $\mathcal{C} = S^1 \times S^1 = T^2$, 즉 원환면이다. 위의 도표는 그 원환면을 잘라 편 것이고, 이 페이지의 모든 양은 두 축 모두에서 $360°$로 나눈 나머지로 읽어야 한다.

**3단계 — C-장애물 유도.** 팔의 어떤 점이 $x > 1$이면 충돌이다. 선분 위에서 $x$ 좌표는 매개변수의 일차 함수이므로 최댓값은 끝점에서 나오고, 팔의 끝점은 베이스($x = 0$), 엘보, 말단 셋뿐이다. 따라서 가장 깊은 침투는

$$d(\theta) = \max\bigl(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)\bigr) - 1$$

이고 $d(\theta) > 0$일 때 정확히 충돌이다. $d$는 침투 깊이로, 패널 안에서 양수이고 접촉에서 0이며, MR의 부호 있는 거리와는 부호가 반대다(§2의 '더 깊이' 메모). 여기서 정리하면, $\cos\theta_1 \le 1$이 항상 성립하고 등호는 $\theta_1 = 0$에서만 나오므로 엘보 항은 $d$를 양수로 만들 수 없다. 링크 1은 벽에 닿을 수는 있어도 넘을 수 없고, 이것이 왼쪽 그림의 접선 관계다. 검사는 부등식 하나로 줄어든다:

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

$\theta_1 = 60°,\ \theta_2 = 0°$ 행은 손으로 확인할 값이 있다. 팔이 $60°$로 곧게 펴지므로 말단은 $(2\cos 60°,\ 2\sin 60°) = (1,\ 1.732)$, 정확히 면 위다. 음의 $\theta_1$에서 좌우 대칭이므로 장애물은 $\theta_1 \in (-90°, 90°)$에 걸친 열린 렌즈다. 3단계의 부등식이 엄격하므로 접촉 곡선은 렌즈를 둘러싸되 거기에 속하지 않고, 그 경계가 양 끝 $\theta_1 = \pm 90°$에서 한 점으로 오므라든다. 오른쪽 오므라든 점, 곧 표의 $\theta_1 = 90°$ 행이 바로 접촉 B $= (90°, -90°)$다.

**5단계 — 원환면을 얼마나 잃는가.** 변수변환 $(\theta_1, \theta_2) \mapsto (\theta_1, \varphi)$는 행렬이 $\begin{pmatrix}1&0\\1&1\end{pmatrix}$인 선형 사상이고 그 행렬식이 $1$이라 원환면 위의 넓이를 보존하고, 막힌 넓이는

$$\operatorname{area}(\mathcal{C}_{\text{obs}}) = \int_{-\pi/2}^{\pi/2} 2\arccos(1 - \cos u)\,du = 7.2949\ \mathrm{rad}^2$$

이다. 허용되는 각 $\theta_1 = u$마다 금지된 $\varphi$ 구간의 길이가 $2\arccos(1-\cos u)$이기 때문이다. 이 적분은 수치로 계산한다(어떤 구적법이든 소수 넷째 자리까지 준다). 이 페이지에서 손으로 하지 않는 유일한 숫자이고, 과제도 이것을 묻지 않는다. 원환면 전체 넓이는 $4\pi^2 = 39.478\ \mathrm{rad}^2$이므로, **패널은 P2 컨피규레이션 공간의 18.478 %를 가져간다.**

**6단계 — 접촉 컨피규레이션 둘.** 말단을 $(1,1)$에 두는 역기구학 해 두 개 — 말단을 거기 놓는 관절각이며, 왜 정확히 이 둘인지는 [[04-robotics/modern-robotics/ch06-inverse-kinematics|6장]]이 유도하고 여기서는 확인만 한다 — 가 모두 경계 위에 있고, 계산은 각각 한 줄이다:

- $\theta = (0°, 90°)$: $\cos 0° + \cos 90° = 1 + 0 = 1$이므로 $d = 0$.
- $\theta = (90°, -90°)$: $\cos 90° + \cos 0° = 0 + 1 = 1$이므로 $d = 0$.

둘은 작업 공간의 같은 점이고 C-space의 다른 두 점이며, 같은 접촉도 아니다. $(0°,90°)$에서는 링크 2가 면에 전 길이로 붙어 눕고, $(90°,-90°)$에서는 말단만 닿는다. C-space 그림은 "둘 다 $\partial\mathcal{C}_{\text{obs}}$ 위"라고만 말하고 멈춘다. 도구가 실제로 어떤 접촉을 하는지는 작업 영역의 질문이다.

**7단계 — 접촉이 차원에 하는 일.** 말단이 면 위에 머물라는 요구는 $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$ 하나, 독립인 홀로노믹 제약(컨피규레이션만의 등식, §3에서 정의) 하나이므로, 접촉을 유지하는 컨피규레이션들의 집합은 차원 $2 - 1 = 1$이다. 바로 그림의 경계 곡선이다. 장애물 *영역*은 차원을 줄이지 않는다. 2차원 공간의 열린 부분집합이라 여전히 2차원이다. **부등식은 깎고, 등식은 줄인다.** §3이 통째로 이 구별에 관한 것이다.

### 1. 컨피규레이션·자유도·그뤼블러

계획기도, 제어기도, 학습한 정책도 로봇 전체가 어디 있는지를 말하는 숫자 목록 하나가 필요한데, P2에서는 지름길 두 개가 틀린다. 말단 위치 $(1,1)$은 접촉 A와 접촉 B를 구별하지 못하고, 관절각 도표를 평평한 평면으로 읽으면 $(170°, 0°)$에서 $(-170°, 0°)$로 가는 이동이 패널을 뚫고 지나간다.

*한 문장으로:* 그 목록이 컨피규레이션이고, 그 전부의 집합이 컨피규레이션 공간이며, 그 차원은 그뤼블러 공식이 세는 자유도이고, 그 모양 — P2에서는 원환면 — 이 어떤 컨피규레이션끼리 가까운지를 정한다.

- **컨피규레이션** = 로봇 모든 점의 완전한 지정; 필요한 최소 좌표 수 = **자유도**(dof).
  C-space = 모든 컨피규레이션의 집합.
- **그뤼블러 공식**: **접지 링크를 포함해** 링크 $N$개, 관절 $J$개, 관절 자유도 $f_i$인 기구에서
  $\text{dof} = m(N - 1 - J) + \sum_i f_i$ ($m = 3$ 평면, $6$ 공간)이고, 아래에서 4절 링크와 관절 여섯의 팔로 계산해 본다.

> **컨피규레이션 공간과 자유도의 정의.** **컨피규레이션 공간**(configuration space, C-space) $\mathcal{C}$는 *집합*으로, 로봇이 취할 수 있는 모든 컨피규레이션을 모은 것이다. **컨피규레이션**은 로봇 모든 점의 위치를 **완전히** 정한 것이다. **자유도**(degrees of freedom, dof)는 *수*, 곧 $\mathcal{C}$의 차원이며, 컨피규레이션을 나타내는 **실숫값** 좌표의 **최소** 개수다(MR 정의 2.1). 강체 링크와 관절로 된 기구라면 그뤼블러 공식이 이것을 센다(MR §2.2.2).
>
> $$\text{dof} = m(N - 1 - J) + \sum_{i=1}^{J} f_i$$
>
> 여기서 $m$은 자유로운 강체의 자유도(평면 $3$, 공간 $6$), $N$은 **접지를 포함한** 링크 수, $J$는 관절 수, $f_i$는 관절 $i$의 자유도다. 움직이는 링크 $N - 1$개가 자유도 $m(N-1)$에서 출발하고 관절마다 $m - f_i$개를 빼앗으므로, 빼앗는 것들이 **서로 독립**일 때에만 정확하고 아니면 하한이다.
>
> - **예**: P2는 $3(3 - 1 - 2) + 2 = 2$이다. $(\theta_1, \theta_2)$가 완전한 컨피규레이션이다.
> - **비예**: 말단 위치 $(1,1)$. 실수 두 개이지만 컨피규레이션이 아니다. $(0°, 90°)$과 $(90°, -90°)$이 모두 말단을 거기 둔다(6단계). 말단만 상태로 쥔 정책은 링크 2가 면에 붙은 A와 말단만 닿는 B를 구별하지 못한다.

> [!example] 계산 예제 · Worked example
> 그뤼블러: $\text{dof} = m(N-1-J) + \sum_i f_i$, 접지는 $N$에 포함한다.
> - **평면 4절 링크**(MR 예제 2.3): $m = 3$, 링크 $N = 4$(접지 + 크랭크 + 커플러 + 로커), 회전관절 $J = 4$, 각 $f_i = 1$. $3(4-1-4) + 4 = -3 + 4 = 1$. 크랭크 각 하나를 정하면 루프 전체가 정해진다.
> - **공간 6R 팔**: $m = 6$, 링크 $N = 7$(베이스 + 움직이는 링크 6), 회전관절 $J = 6$, 각 $f_i = 1$. $6(7-1-6) + 6 = 0 + 6 = 6$ — 도달 가능한 작업 영역 안에서 도구의 위치와 자세를 모두 정하기에 충분하다.
>
> **패턴**: 열린 직렬 체인은 $J = N - 1$이라 첫 항이 사라지고 자유도는 그냥 $\sum_i f_i$다. 닫힌 루프마다 제약이 빠지므로 4절 링크는 관절이 4개여도 자유도가 1이다. 공식은 제약이 서로 독립이라고 가정하며, 특수한 기하에서는 틀릴 수 있다. 평행사변형 링크에 두 크랭크와 평행하고 길이가 같은 셋째 링크를 더하면 그뤼블러는 $N = 5$, $J = 6$으로 $3(5-1-6) + 6 = 0$ 자유도를 세지만, 링크는 여전히 1 자유도로 움직인다. 더한 링크의 제약이 평행사변형이 이미 건 제약을 되풀이하기 때문이다(MR 예제 2.6). 이런 기구에서 그뤼블러는 하한일 뿐이다.

- **위상이 중요하다**: 2R 팔의 C-space는 평면이 아니라 원환면($T^2 = S^1 \times S^1$) —
  각도는 감긴다. 순진한 각도 회귀가 깨지는 정확한 이유이고
  ([[02-foundations/se3-geometry|8. SE(3) §2]]), "C-space 거리"에 주의가 필요한 이유다.

> **C-space 위상의 정의.** C-space의 **위상**(topology)은 좌표가 아니라 *공간 자체의 성질*이다. 한 공간을 **자르거나 붙이지 않고 연속으로 변형**해 다른 공간을 만들 수 있으면 두 공간은 위상이 같다(MR §2.3.1). 2R 팔의 위상은 두 사실이 정한다. 각은 **감긴다**. $\theta_i$와 $\theta_i + 360°$가 같은 컨피규레이션이므로 관절마다 원 $S^1$ 위에 산다. 그리고 두 관절은 **서로 독립**이라 공간은 두 원의 곱이다.
>
> $$\mathcal{C}_{\text{P2}} = S^1 \times S^1 = T^2, \qquad (\theta_1,\ \theta_2) \sim (\theta_1 + 360°\,k_1,\ \theta_2 + 360°\,k_2),\ \ k_1, k_2 \in \mathbb{Z}$$
>
> 여기서 $T^2$는 원환면이고 $\sim$는 "같은 컨피규레이션이다"로 읽는다. P2에 관절 한계가 없어서 원환면이다. 한계가 있으면 각 원이 닫힌 구간으로 바뀐다.
>
> - **예**: $(170°, 0°)$과 $(-170°, 0°)$은 원환면에서 $20°$ 떨어져 있다. 짧은 이동은 곧게 편 팔을 패널 반대쪽으로, $\theta_1 = 180°$를 지나 돌리고 내내 자유롭다.
> - **비예**: 정사각형 도표를 평면 $\mathbb{R}^2$로 읽는 것. 거기서 두 점은 $340°$ 떨어져 있고, 둘을 잇는 직선은 곧게 편 팔이 패널 안 $1\,\mathrm{m}$에 있는 $\theta_1 = 0$을 지난다. 도표에서 보간하는 계획기는 먼 길로, 벽을 뚫고 간다.

아래 그림이 상자의 예와 비예를 P2 위에 그린다.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="왼쪽은 곧게 편 P2 팔을 θ1 = 170°, 180°, −170°(짧은 이동)와 벽을 1 m 파고드는 0°(긴 이동의 중간)에 그린 작업 영역이고, 오른쪽은 (170°, 0°)와 (−170°, 0°)를 붙인 변 너머 20° 경로와 렌즈를 가로지르는 340° 도표 직선으로 이은 원환면 도표다.">
  <defs><marker id="mr02wrK" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <rect x="155" y="48.8" width="58.5" height="202.5" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="155" y1="60.8" x2="167" y2="48.8"/><line x1="155" y1="72.8" x2="179" y2="48.8"/><line x1="155" y1="84.8" x2="191" y2="48.8"/><line x1="155" y1="96.8" x2="203" y2="48.8"/><line x1="155" y1="108.8" x2="213.5" y2="50.2"/><line x1="155" y1="120.8" x2="213.5" y2="62.2"/><line x1="155" y1="132.8" x2="213.5" y2="74.2"/><line x1="155" y1="144.8" x2="213.5" y2="86.2"/><line x1="155" y1="156.8" x2="213.5" y2="98.2"/><line x1="155" y1="168.8" x2="213.5" y2="110.2"/><line x1="155" y1="180.8" x2="213.5" y2="122.2"/><line x1="155" y1="192.8" x2="213.5" y2="134.2"/><line x1="155" y1="204.8" x2="213.5" y2="146.2"/><line x1="155" y1="216.8" x2="213.5" y2="158.2"/><line x1="155" y1="228.8" x2="213.5" y2="170.2"/><line x1="155" y1="240.8" x2="213.5" y2="182.2"/><line x1="156.5" y1="251.2" x2="213.5" y2="194.2"/><line x1="168.5" y1="251.2" x2="213.5" y2="206.2"/><line x1="180.5" y1="251.2" x2="213.5" y2="218.2"/><line x1="192.5" y1="251.2" x2="213.5" y2="230.2"/><line x1="204.5" y1="251.2" x2="213.5" y2="242.2"/></g>
  <line x1="155" y1="48.8" x2="155" y2="251.2" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="21.4,134.4 22.1,130.5 23.1,126.7 24.2,122.9 25.4,119.2 26.9,115.6 28.4,112 30.2,108.4 32.1,105 34.1,101.6 36.3,98.4 38.6,95.2 41.1,92.1 43.6,89.2 46.4,86.4 49.2,83.6 52.1,81.1 55.2,78.6 58.4,76.3 61.6,74.1 65,72.1 68.4,70.2 72,68.4 75.6,66.9 79.2,65.4 82.9,64.2 86.7,63.1 90.5,62.1 94.4,61.4 98.3,60.8 102.2,60.3 106.1,60.1 110,60 113.9,60.1 117.8,60.3 121.7,60.8 125.6,61.4 129.5,62.1 133.3,63.1 137.1,64.2 140.8,65.4 144.4,66.9 148,68.4 151.6,70.2 155,72.1 158.4,74.1 161.6,76.3 164.8,78.6 167.9,81.1 170.8,83.6 173.6,86.4 176.4,89.2 178.9,92.1 181.4,95.2 183.7,98.4 185.9,101.6 187.9,105 189.8,108.4 191.6,112 193.1,115.6 194.6,119.2 195.8,122.9 196.9,126.7 197.9,130.5 198.6,134.4 199.2,138.3 199.7,142.2 199.9,146.1 200,150 199.9,153.9 199.7,157.8 199.2,161.7 198.6,165.6 197.9,169.5 196.9,173.3 195.8,177.1 194.6,180.8 193.1,184.4 191.6,188 189.8,191.6 187.9,195 185.9,198.4 183.7,201.6 181.4,204.8 178.9,207.9 176.4,210.8 173.6,213.6 170.8,216.4 167.9,218.9 164.8,221.4 161.6,223.7 158.4,225.9 155,227.9 151.6,229.8 148,231.6 144.4,233.1 140.8,234.6 137.1,235.8 133.3,236.9 129.5,237.9 125.6,238.6 121.7,239.2 117.8,239.7 113.9,239.9 110,240 106.1,239.9 102.2,239.7 98.3,239.2 94.4,238.6 90.5,237.9 86.7,236.9 82.9,235.8 79.2,234.6 75.6,233.1 72,231.6 68.4,229.8 65,227.9 61.6,225.9 58.4,223.7 55.2,221.4 52.1,218.9 49.2,216.4 46.4,213.6 43.6,210.8 41.1,207.9 38.6,204.8 36.3,201.6 34.1,198.4 32.1,195 30.2,191.6 28.4,188 26.9,184.4 25.4,180.8 24.2,177.1 23.1,173.3 22.1,169.5 21.4,165.6" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 3" opacity="0.6" marker-end="url(#mr02wrK)"/>
  <polyline points="155,72.1 158.4,74.1 161.6,76.3 164.8,78.6 167.9,81.1 170.8,83.6 173.6,86.4 176.4,89.2 178.9,92.1 181.4,95.2 183.7,98.4 185.9,101.6 187.9,105 189.8,108.4 191.6,112 193.1,115.6 194.6,119.2 195.8,122.9 196.9,126.7 197.9,130.5 198.6,134.4 199.2,138.3 199.7,142.2 199.9,146.1 200,150 199.9,153.9 199.7,157.8 199.2,161.7 198.6,165.6 197.9,169.5 196.9,173.3 195.8,177.1 194.6,180.8 193.1,184.4 191.6,188 189.8,191.6 187.9,195 185.9,198.4 183.7,201.6 181.4,204.8 178.9,207.9 176.4,210.8 173.6,213.6 170.8,216.4 167.9,218.9 164.8,221.4 161.6,223.7 158.4,225.9 155,227.9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="4 3"/>
  <line x1="110" y1="150" x2="200" y2="150" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="7 4" opacity="0.8"/>
  <circle cx="155" cy="150" r="3.2" fill="currentColor" opacity="0.8"/>
  <circle cx="200" cy="150" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <line x1="110" y1="150" x2="21.4" y2="134.4" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" opacity="0.55"/>
  <circle cx="65.7" cy="142.2" r="2.8" fill="currentColor" opacity="0.55"/>
  <line x1="110" y1="150" x2="20" y2="150" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" opacity="1.0"/>
  <circle cx="65" cy="150" r="2.8" fill="currentColor" opacity="1.0"/>
  <line x1="110" y1="150" x2="21.4" y2="165.6" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" opacity="0.55"/>
  <circle cx="65.7" cy="157.8" r="2.8" fill="currentColor" opacity="0.55"/>
  <polyline points="21.4,134.4 21.1,135.9 20.9,137.5 20.7,139 20.5,140.6 20.3,142.2 20.2,143.7 20.1,145.3 20.1,146.9 20,148.4 20,150 20,151.6 20.1,153.1 20.1,154.7 20.2,156.3 20.3,157.8 20.5,159.4 20.7,161 20.9,162.5 21.1,164.1 21.4,165.6" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#mr02wrK)"/>
  <circle cx="110" cy="150" r="4.5" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.3"><line x1="367" y1="40" x2="367" y2="260"/><line x1="312" y1="205" x2="532" y2="205"/><line x1="422" y1="40" x2="422" y2="260"/><line x1="312" y1="150" x2="532" y2="150"/><line x1="477" y1="40" x2="477" y2="260"/><line x1="312" y1="95" x2="532" y2="95"/></g>
  <path d="M367 95 L367.9 87.9 L368.8 85.5 L369.8 83.8 L370.7 82.5 L371.6 81.5 L372.5 80.7 L373.4 79.9 L374.3 79.3 L375.2 78.8 L376.2 78.4 L377.1 78 L378 77.7 L378.9 77.4 L379.8 77.2 L380.8 77 L381.7 76.9 L382.6 76.8 L383.5 76.7 L384.4 76.7 L385.3 76.7 L386.2 76.7 L387.2 76.7 L388.1 76.8 L389 76.9 L389.9 77 L390.8 77.1 L391.8 77.3 L392.7 77.5 L393.6 77.7 L394.5 77.9 L395.4 78.2 L396.3 78.4 L397.2 78.7 L398.2 79 L399.1 79.4 L400 79.7 L400.9 80.1 L401.8 80.5 L402.8 80.9 L403.7 81.4 L404.6 81.8 L405.5 82.3 L406.4 82.8 L407.3 83.4 L408.2 83.9 L409.2 84.5 L410.1 85.1 L411 85.7 L411.9 86.4 L412.8 87 L413.8 87.7 L414.7 88.4 L415.6 89.2 L416.5 89.9 L417.4 90.7 L418.3 91.5 L419.2 92.4 L420.2 93.2 L421.1 94.1 L422 95 L422.9 95.9 L423.8 96.9 L424.8 97.9 L425.7 98.9 L426.6 99.9 L427.5 100.9 L428.4 102 L429.3 103.1 L430.2 104.2 L431.2 105.4 L432.1 106.5 L433 107.7 L433.9 108.9 L434.8 110.2 L435.8 111.4 L436.7 112.7 L437.6 114 L438.5 115.3 L439.4 116.7 L440.3 118 L441.2 119.4 L442.2 120.8 L443.1 122.3 L444 123.7 L444.9 125.2 L445.8 126.7 L446.8 128.2 L447.7 129.8 L448.6 131.3 L449.5 132.9 L450.4 134.5 L451.3 136.1 L452.2 137.8 L453.2 139.5 L454.1 141.2 L455 142.9 L455.9 144.6 L456.8 146.4 L457.8 148.2 L458.7 150 L459.6 151.8 L460.5 153.7 L461.4 155.6 L462.3 157.6 L463.2 159.5 L464.2 161.6 L465.1 163.6 L466 165.7 L466.9 167.9 L467.8 170.1 L468.8 172.3 L469.7 174.7 L470.6 177.1 L471.5 179.7 L472.4 182.3 L473.3 185.2 L474.2 188.3 L475.2 191.8 L476.1 196.1 L477 205 L476.1 212.1 L475.2 214.5 L474.2 216.2 L473.3 217.5 L472.4 218.5 L471.5 219.3 L470.6 220.1 L469.7 220.7 L468.8 221.2 L467.8 221.6 L466.9 222 L466 222.3 L465.1 222.6 L464.2 222.8 L463.2 223 L462.3 223.1 L461.4 223.2 L460.5 223.3 L459.6 223.3 L458.7 223.3 L457.8 223.3 L456.8 223.3 L455.9 223.2 L455 223.1 L454.1 223 L453.2 222.9 L452.2 222.7 L451.3 222.5 L450.4 222.3 L449.5 222.1 L448.6 221.8 L447.7 221.6 L446.8 221.3 L445.8 221 L444.9 220.6 L444 220.3 L443.1 219.9 L442.2 219.5 L441.2 219.1 L440.3 218.6 L439.4 218.2 L438.5 217.7 L437.6 217.2 L436.7 216.6 L435.8 216.1 L434.8 215.5 L433.9 214.9 L433 214.3 L432.1 213.6 L431.2 213 L430.2 212.3 L429.3 211.6 L428.4 210.8 L427.5 210.1 L426.6 209.3 L425.7 208.5 L424.8 207.6 L423.8 206.8 L422.9 205.9 L422 205 L421.1 204.1 L420.2 203.1 L419.2 202.1 L418.3 201.1 L417.4 200.1 L416.5 199.1 L415.6 198 L414.7 196.9 L413.8 195.8 L412.8 194.6 L411.9 193.5 L411 192.3 L410.1 191.1 L409.2 189.8 L408.2 188.6 L407.3 187.3 L406.4 186 L405.5 184.7 L404.6 183.3 L403.7 182 L402.8 180.6 L401.8 179.2 L400.9 177.7 L400 176.3 L399.1 174.8 L398.2 173.3 L397.2 171.8 L396.3 170.2 L395.4 168.7 L394.5 167.1 L393.6 165.5 L392.7 163.9 L391.8 162.2 L390.8 160.5 L389.9 158.8 L389 157.1 L388.1 155.4 L387.2 153.6 L386.2 151.8 L385.3 150 L384.4 148.2 L383.5 146.3 L382.6 144.4 L381.7 142.4 L380.8 140.5 L379.8 138.4 L378.9 136.4 L378 134.3 L377.1 132.1 L376.2 129.9 L375.2 127.7 L374.3 125.3 L373.4 122.9 L372.5 120.3 L371.6 117.7 L370.7 114.8 L369.8 111.7 L368.8 108.2 L367.9 103.9 Z" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
  <rect x="312" y="40" width="220" height="220" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-linejoin="round"><polyline points="307,128.5 312,122.5 317,128.5"/><polyline points="527,128.5 532,122.5 537,128.5"/><polyline points="507.7,35 513.7,40 507.7,45"/><polyline points="514.7,35 520.7,40 514.7,45"/><polyline points="507.7,255 513.7,260 507.7,265"/><polyline points="514.7,255 520.7,260 514.7,265"/></g>
  <line x1="525.9" y1="150" x2="318.1" y2="150" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.75"/>
  <line x1="458.7" y1="150" x2="385.3" y2="150" stroke="currentColor" stroke-width="2.6" stroke-dasharray="6 3"/>
  <line x1="525.9" y1="150" x2="532" y2="150" stroke="currentColor" stroke-width="3.2"/>
  <line x1="312" y1="150" x2="318.1" y2="150" stroke="currentColor" stroke-width="3.2"/>
  <circle cx="525.9" cy="150" r="4.2" fill="currentColor"/>
  <circle cx="318.1" cy="150" r="4.2" fill="currentColor"/>
  <circle cx="422" cy="150" r="3" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="312" y1="260" x2="312" y2="264"/><line x1="308" y1="260" x2="312" y2="260"/><line x1="367" y1="260" x2="367" y2="264"/><line x1="308" y1="205" x2="312" y2="205"/><line x1="422" y1="260" x2="422" y2="264"/><line x1="308" y1="150" x2="312" y2="150"/><line x1="477" y1="260" x2="477" y2="264"/><line x1="308" y1="95" x2="312" y2="95"/><line x1="532" y1="260" x2="532" y2="264"/><line x1="308" y1="40" x2="312" y2="40"/></g>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18" font-size="12">작업 영역</text>
    <text x="300" y="18" font-size="12">C-space 도표 (잘라 편 원환면)</text>
    <text x="184.2" y="42.8" text-anchor="middle">벽 x = 1</text>
    <text x="116" y="166">베이스</text>
    <text x="12" y="268.2">짧은 이동: θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 170° → 180° → −170°</tspan></text>
    <text x="12" y="284.2" opacity="0.85">말단은 면에서 2.97 m 이상 떨어져 있다</text>
    <text x="218.5" y="138">θ<tspan dy="3.5">1</tspan><tspan dx="3.1" dy="-3.5">= 0°:</tspan></text>
    <text x="218.5" y="153">말단 (2, 0),</text>
    <text x="218.5" y="168">d = 1 m</text>
    <text x="12" y="52" opacity="0.8">긴 이동의 말단 경로, 340°</text>
    <text x="521.9" y="141" text-anchor="end">(170°, 0°)</text>
    <text x="322.1" y="141">(−170°, 0°)</text>
    <text x="422" y="166" text-anchor="middle">d = 1 m</text>
    <text x="394.5" y="113.3" text-anchor="middle">C<tspan dy="3.5">obs</tspan></text>
    <text x="312" y="276" text-anchor="middle">−180°</text>
    <text x="305" y="264" text-anchor="end">−180°</text>
    <text x="422" y="276" text-anchor="middle">0°</text>
    <text x="305" y="154" text-anchor="end">0°</text>
    <text x="532" y="276" text-anchor="middle">180°</text>
    <text x="305" y="44" text-anchor="end">180°</text>
    <text x="422" y="291" text-anchor="middle" font-size="12">θ<tspan dy="3.5">1</tspan></text>
    <text x="305" y="32" text-anchor="end" font-size="12">θ<tspan dy="3.5">2</tspan></text>
    <text x="318" y="240">평면으로 읽은 긴 이동: 340°,</text>
    <text x="318" y="254">|θ<tspan dy="3.5">1</tspan><tspan dy="-3.5">| &lt; 60°에서 렌즈 안</tspan></text>
    <text x="526" y="62" text-anchor="end">짧은 이동: 20°,</text>
    <text x="526" y="76" text-anchor="end">붙인 변을 건너며</text>
    <text x="526" y="90" text-anchor="end">내내 자유</text>
  </g>
</svg>

상자의 두 이동을 P2에 그렸다. 왼쪽에서 짧은 이동은 곧게 편 팔을 $\theta_1 = 170°$에서 $180°$를 지나 $-170°$까지 베이스 뒤쪽으로 돌리고, 그동안 말단은 면에서 늘 $2.97\,\mathrm{m}$ 이상 떨어져 있다. 긴 이동의 말단은 원의 나머지 $340°$를 쓸며 벽을 가로지르고, 그 중간인 $\theta_1 = 0°$에서 말단은 패널 안 $1\,\mathrm{m}$인 $(2, 0)$에 있다. 오른쪽은 같은 두 이동을 도표에 옮긴 것이다. 붙인 변을 건너는 $20°$이거나, 평평한 직선 $\theta_2 = 0$을 따라가는 $340°$인데, 이 직선은 $|\theta_1| < 60°$, 곧 길의 약 3분의 1에서 렌즈 안을 지나고 그 한가운데에서 렌즈의 가장 깊은 점 $d = 1\,\mathrm{m}$에 이른다.

컨피규레이션을 적는 방식 — 가장 적은 숫자로 쓰느냐, 더 많은 숫자에 제약을 달아 묻느냐 — 도 고르는 문제이고 나름의 함정이 있다. 아래에 접어 둔다.

> [!note]- 더 깊이 · Deeper
> **명시적 표현과 암시적 표현.** **명시적** 표현은 최소 개수의 좌표를 쓰고 특이점이 생길 수 있다 — 예: 짐벌 락에서는 세 오일러 각 중 둘이 같은 축을 돌리게 된다([[02-foundations/se3-geometry|8. SE(3) §2]]). **암시적** 표현은 컨피규레이션을 더 높은 차원의 공간에 묻고 제약을 단다 — $R^\top R = I$인 회전 행렬처럼. MR은 일관되게 암시적 표현을 고르고, 현대 로봇 학습도 같은 선택을 한다.

### 1.5 작업 공간과 작업 영역

과제는 관절각이 아니라 도구가 일하는 곳에서 쓴다 — "말단을 $(1,1)$에 둔다". 그리고 목표는 그 공간의 멀쩡한 점이면서도 팔이 닿지 않거나, 틀린 도구 각도로만 닿을 수 있다. 이 절은 두 집합을 갈라 둔다.

- **작업 공간 대 C-space**(task space vs C-space): 도구가 사는 곳 대 로봇이 사는 곳; 둘 사이의 사상이
  기구학이다(4~6장). *작업 공간*과 *작업 영역(workspace)*을 구별하라. 앞의 것은 과제가
  정하고, 뒤의 것은 로봇 구조가 정한다.
- **구별이 중요한 이유**: 작업 공간의 점이 작업 영역 밖에 있을 수 있고, 그것이
  바로 그 팔로는 그 과제를 못 한다는 뜻이다. 도달 거리가 1 m인 팔의 베이스에서 2 m 떨어진
  목표는 작업 공간의 올바른 점이지만 그 팔의 작업 영역에는 속하지 않는다.

> **작업 공간과 작업 영역의 정의.** 둘 다 로봇의 컨피규레이션이 아니라 *말단 컨피규레이션의 집합*이고(MR은 도구의 자세를 컨피규레이션이라 부른다), 둘 다 사용자가 나타내기로 고른 말단 자유도로 쓴다(MR §2.5). **작업 공간**(task space) $\mathcal{X}$는 과제를 자연스럽게 쓰는 공간이고, 로봇과 무관하게 **과제가 고른다**. **작업 영역**(workspace) $\mathcal{W}$는 로봇이 **도달할 수 있는** 말단 컨피규레이션의 집합이고, 과제와 무관하게 로봇의 구조가 정한다.
>
> $$\mathcal{W} = \{\, f(\theta) \;:\; \theta \in \mathcal{C} \,\}$$
>
> 여기서 $f$는 [[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]의 순기구학을 $\mathcal{W}$에 고른 좌표로 쓴 것이므로, 작업 영역은 C-space의 상이다. $\mathcal{X}$와 $\mathcal{W}$가 좌표를 공유하면 $\mathcal{W}$ 밖의 과제 점은 실행 불가능하다. **도달 작업 영역**(reachable workspace) $f(\mathcal{C}_{\text{free}})$는 §2의 자유 컨피규레이션만 남긴다.
>
> - **예**: "말단을 $(1,1)$에 둔다"는 $\mathcal{X} = \mathbb{R}^2$에서 쓰고, 거기서 P2의 작업 영역은 반지름 $L_1 + L_2 = 2\,\mathrm{m}$인 원판이다. $1.414\,\mathrm{m}$ 거리의 $(1,1)$은 그 안에 있다. 패널이 있으면 도달 작업 영역은 그중 $x \le 1$인 부분이고, $(1,1)$은 그 가장자리에 있다.
> - **비예**: 자세 $(1, 1, 45°)$, 곧 말단은 목표에 두고 도구 방향 $\theta_1 + \theta_2$를 $45°$로 정한, 작업 공간 $\mathbb{R}^2 \times S^1$의 점. 그 좌표로 쓴 P2의 작업 영역에서 $(1,1)$의 방향은 $0°$(B)와 $90°$(A)뿐이고, $45°$라면 엘보가 베이스에서 $1$이 아니라 $0.414\,\mathrm{m}$ 떨어진 $(0.293, 0.293)$에 놓여야 한다. 도달할 수 있는 점이라도 도구 각도까지 정하면 실행 불가능할 수 있다.

### 2. C-장애물과 자유 공간의 정의

계획기의 직선 간선이 합법인지를 결정하는 것은 벽의 모양이 아니라 C-장애물의 모양이다. [[04-robotics/modern-robotics/ch10-motion-planning|10장]]이 검사하는 것이 정확히 이 집합이고, 이 절이 그것을 정의한다.

**C-장애물**은 작업 영역이 아니라 *컨피규레이션 공간의 부분집합*이다. 세계에 강체 장애물 $\mathcal{O}$가 있고 컨피규레이션 $\theta$에서 로봇 몸체가 차지하는 세계 점들의 집합을 $\mathcal{A}(\theta)$라 할 때, 정의에 들어가는 조건은 셋이다. 컨피규레이션들의 집합이라는 것, 소속 여부를 물체끼리의 교집합으로 판정한다는 것, 그리고 **침투**만 충돌로 친다는 것이다. 몸체가 장애물의 내부 $\operatorname{int}\mathcal{O}$와 만나야 하고, 표면에 닿기만 한 컨피규레이션은 자유다(MR §10.1). 접촉을 자유로 치는 것은 관통 과제가 접촉으로 끝나기 때문에 이 위키가 고른 약속이다. MR과 MoveIt은 접촉을 충돌로 치는 경우가 많고, 아래의 '더 깊이' 메모가 그 사정을 설명한다. 관절 한계가 있는 로봇이라면 그것도 C-장애물이거나(MR §10.2.1) §1의 위상 상자에서처럼 각 원을 구간으로 자른다(MR §2.3.1). MR은 두 방식을 다 쓰고, P2에는 관절 한계가 없다:

$$\mathcal{C}_{\text{obs}} = \{\,\theta \in \mathcal{C} \;:\; \mathcal{A}(\theta) \cap \operatorname{int}\mathcal{O} \neq \varnothing\,\}, \qquad \mathcal{C}_{\text{free}} = \mathcal{C} \setminus \mathcal{C}_{\text{obs}}$$

여기서 $\mathcal{C}$는 컨피규레이션 공간 전체이고, 패널의 $\operatorname{int}\mathcal{O}$는 '이 페이지의 대상'이 정한 충돌 판정 그대로 $x > 1$이다. 그러므로 $\mathcal{C}_{\text{free}}$가 접촉까지 포함해 로봇이 합법적으로 있을 수 있는 전부다. 이 정의의 요점은 모양을 가진 로봇이 장애물 사이를 지나가는 문제를 $\mathcal{C}_{\text{free}}$ 안을 움직이는 *점*의 문제로 바꾼다는 것이고, [[04-robotics/modern-robotics/ch10-motion-planning|10장]]의 모든 계획기가 점을 위해 쓰인 이유가 그것이다.

- **예**: 위에서 유도한 렌즈 $\{\cos\theta_1 + \cos(\theta_1{+}\theta_2) > 1\}$, P2 원환면의 18.478 %. 이것은 C-space에 벽을 그려서 얻은 것이 아니라 — 벽은 거기에 그림이 없다 — 각 컨피규레이션에서 작업 영역의 충돌 검사를 평가해서 얻은 것이다.
- **비예**: 벽 자체 $\{x \ge 1\}$. 작업 영역의 영역은 C-장애물이 아니고, 둘은 차원이 같을 필요조차 없다. 닿기만 해도 충돌로 치는 MR의 닫힌 검사에서는 2차원 작업 영역의 점 장애물이 2차원 C-space에서 *곡선*, 곧 팔이 그 점을 지나는 컨피규레이션들이 된다. 이 페이지의 내부 검사에서는 점에 내부가 없어 아무것도 막지 않고, 작은 원판은 그 곡선 둘레의 얇은 띠를 막는다. 벽에 닿는다고 C-장애물에 드는 것도 아니다. 접촉 컨피규레이션 A $= (0°, 90°)$에서는 링크 2 전체가 $x = 1$ 위, 곧 $\{x \ge 1\}$ 안에 놓이지만 $d = 0$이라 A는 렌즈의 경계에, 곧 $\mathcal{C}_{\text{free}}$에 있다.

> [!note]- 더 깊이 · Deeper
> **접촉을 여기서 자유로 치는 이유, 그리고 $d$의 부호.** MR은 접촉에 대해 한결같지 않다. 충돌 검사는 $d = 0$을 충돌로 세고(§10.2.2), §10.3은 경계를 $\mathcal{C}_{\text{free}}$에 넣는 것을 예외로만 다루며, §13.3.2.1은 자유 공간을 열린 집합, 장애물을 닫힌 집합으로 잡는다. 접촉을 실패로 치는 MoveIt의 planning scene도 이쪽이다([[04-robotics/ros2/manipulation-moveit2|25.8 MoveIt 2]]). 이 위키는 관통 과제가 접촉으로 끝나므로 접촉을 자유로 치고, 그래서 검사가 내부를 묻는다. 부호도 다르다. 이 페이지와 [[04-robotics/modern-robotics/ch10-motion-planning|10장]]에서 $d(\theta)$는 **침투 깊이**로, 장애물 안에서 양수, 접촉에서 0이다. MR의 접촉 기구학 장은 $d(q)$를 부호 있는 *거리*로 써서 떨어져 있을 때 양수다. 정보는 같고 부호가 반대이니, 숫자를 비교하기 전에 출처가 어느 쪽을 뜻하는지 확인해야 한다.

### 3. 홀로노믹 제약과 비홀로노믹 제약의 정의

부등식은 깎고, 등식은 줄인다. 도구를 면에 붙들어 두는 것은 관절각에 대한 등식이고, 팔을 패널 밖에 두는 것은 부등식이며, 옆으로 미끄러지지 못하는 바퀴는 속도에 대한 등식이다. 이 셋을 섞는 것이 자유도 계산이 틀리는 표준적인 방식이고, 이 절은 두 종류의 등식을 가르는 판정 하나를 준다.

기구에 걸린 **제약**은 그 운동이 만족해야 하는 조건이다. 속도 없이 쓸 수 있는가 하나로 두 종류가 갈린다. 둘 다 같은 속도 꼴, 곧 **파피안 제약**(Pfaffian constraint)으로 쓸 수 있고, 판정은 그 꼴이 적분되는가를 묻는다(MR §2.4):

$$A(\theta)\,\dot\theta = 0, \qquad \text{홀로노믹(적분 가능)} \iff A(\theta) = \Psi(\theta)\,\frac{\partial g}{\partial\theta}(\theta)\ \text{(어떤 } g\text{와 가역 } \Psi(\theta)\text{에 대해)}$$

여기서 $\theta \in \mathbb{R}^n$, $A(\theta)$는 제약마다 한 행씩인 $k \times n$ 행렬, $g: \mathbb{R}^n \to \mathbb{R}^k$, $\Psi(\theta)$는 가역인 $k \times k$ 행렬, 곧 적분 인자다(MR은 $\Psi = I$인 경우로 쓴다). $g(\theta(t)) = 0$을 시간으로 미분하면 정확히 $\frac{\partial g}{\partial\theta}\dot\theta = 0$이 나오므로 판정이 이런 꼴이 되고, 적분되는 속도 제약은 $g(\theta) = 0$이 이미 말한 것 이상을 말하지 않는다. P2에서 접촉 제약은 $g(\theta) = \cos\theta_1 + \cos(\theta_1{+}\theta_2) - 1 = 0$이므로 그 행은 $A = \partial g/\partial\theta = (-\sin\theta_1 - \sin(\theta_1{+}\theta_2),\ -\sin(\theta_1{+}\theta_2))$이고, 카탈로그 자세 $(0°, 90°)$에서 $(-1,\ -1)$이다. $A\dot\theta = -\dot\theta_1 - \dot\theta_2 = 0$이 $\dot\theta_2 = -\dot\theta_1$을 강제하므로 허용되는 관절 속도는 $(1, -1)$의 배수뿐이고, P2의 야코비안 $J = \begin{pmatrix}-1&-1\\1&0\end{pmatrix}$([[02-foundations/manipulator-kinematics-dynamics|10 §1]])로 보면 $(1, -1)\,\mathrm{rad/s}$는 말단 속도 $J(1,-1) = (0, 1)\,\mathrm{m/s}$, 곧 면을 따라 곧장 위로 가는 속도를 준다.

- **홀로노믹 제약**은 컨피규레이션만의 방정식 $g(\theta) = 0$이다. 독립인 것 하나마다 컨피규레이션 공간의 차원이 하나 줄어든다. $\theta$를 $g$의 등위집합, 곧 $g$가 한 값(여기서는 $0$)을 유지하는 컨피규레이션들에 가두기 때문이다. *예*: P2의 말단을 패널 면에 붙들어 두는 $\cos\theta_1 + \cos(\theta_1{+}\theta_2) = 1$, 남는 것은 1차원 접촉 곡선. *예*: 닫힌 루프, 4절 링크의 자유도가 4가 아니라 1인 이유.
- **비홀로노믹 제약**은 속도에 대한 방정식 $A(\theta)\dot\theta = 0$인데, 어떤 $g(\theta) = 0$의 시간 미분도 아닌 것이다. 모든 컨피규레이션에서 운동 방향 하나를 없애지만 도달 가능 집합의 차원은 줄이지 않는다. *예*: 옆으로 미끄러지지 못하는 바퀴([[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|13장]]). 자동차는 모든 자세에 도달하지만 모든 경로로 가지는 못한다.
- **구별의 비예**: "말단은 패널 밖에 있어야 한다"는 둘 중 어느 것도 아니다. *부등식*이기 때문이다. 차원도 방향도 없애지 않고 열린 영역을 지울 뿐이다.

**위키 연결**: C-space는 로봇 [[02-foundations/rl-basics|MDP]]의 상태의 일부다. 컨피규레이션은 속도와 나란히 상태에 들어간다. 어떤 VLA 행동 공간은 그 위의 좌표이고([[01-canonical-papers/notes/4-vla/pi0|π0]]의 관절 청크), 다른 것은([[01-canonical-papers/notes/4-vla/rt-1|RT-1]]의 팔 행동, 곧 말단 위치와 회전) §1.5의 작업 공간에 산다([[02-foundations/se3-geometry|8. SE(3) §5]]).

### 스스로 점검

1. 평면 차동 구동(differential-drive) 로봇의 컨피규레이션은 숫자 몇 개로 기술되고, 제약은 무엇인가?
2. 그뤼블러 공식으로 평면 슬라이더-크랭크(링크 4, 회전관절 3 + 직동관절 1)의 자유도를 계산하라.
3. 2R 팔의 C-space가 평면 $\mathbb{R}^2$가 아니라 원환면 $T^2$라는 사실이 학습(각도 회귀)에서 왜 문제가 되는가?
4. P2가 $\theta = (45°, 0°)$에 있다. 패널에 대한 $d(\theta)$를 계산하고 팔이 무엇을 하고 있는지 말하라.

> [!tip]- 정답
> 1. 차체만 보면 $(x, y, \theta)$ 세 개다(MR §13.3처럼 두 바퀴의 회전각까지 넣으면 다섯). 비홀로노믹 제약(옆 미끄럼 불가)은 *속도*를 제한할 뿐 도달 가능한 차체 자세를 제한하지 않는다. 어떤 자세에도 갈 수 있고, 다만 아무 경로로나 가지는 못한다.
> 2. $\text{dof} = 3(4-1-4) + (3\cdot 1 + 1\cdot 1) = -3 + 4 = 1$. 직동관절도 회전관절과 똑같이 자유도 하나를 보탠다. 계산에 들어가는 것은 관절의 종류가 아니라 $f_i$다.
> 3. $359°$와 $1°$는 원 위에서 이웃인데 유클리드 거리로는 멀다. 순진한 MSE 회귀는 각이 감기는 지점에서 큰 벌점을 받고 불연속인 목표를 학습하게 된다([[02-foundations/se3-geometry|SE(3) §2]]).
> 4. 팔이 $45°$로 곧게 펴져 말단이 $(\sqrt2, \sqrt2) = (1.4142, 1.4142)$이므로 $d = \cos 45° + \cos 45° - 1 = \sqrt2 - 1 = 0.4142\,\mathrm{m}$다. 패널 안으로 $41.4\,\mathrm{cm}$ 들어가 있다. $\theta_2 = 0$ 선 위에서 렌즈가 가장 깊은 지점은 $\theta_1 = 0$이고, 거기서 $d = 1\,\mathrm{m}$다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 장치는 같은 **P2**, 다만 패널을 0.5 m 더 바깥에 다시 세운다. 벽은 이제 $x \ge 1.5$.

1. **그리기.** 새 벽에 대한 위의 그림. 작업 영역 그림에서는 벽이 더 이상 엘보 원에 닿지 않음을 보여라. C-space 도표에서는 새 장애물을 칠하고 오므라드는 지점을 표시하라. 카탈로그 자세 $(0°,90°)$에 무슨 일이 일어났는지 한 문장으로 쓰라.
2. **유도.** (a) 새 벽의 $d(\theta)$를 쓰고, 다시 말단 항만 문제가 됨을 논증하라. (b) 경계 조건 $\cos\theta_1 + \cos\varphi = 1.5$에서 장애물이 오므라드는 $\theta_1$ 두 값과, $\theta_1 = 0°$ 및 $\theta_1 = 30°$에서 경계 위의 $\theta_2$ 값을 구하라. (c) *곧게 편* 팔 $\theta_2 = 0°$에 대해 패널을 파고드는 $\theta_1$ 범위를 구하라.
3. **해석.** 원환면에서 막힌 비율이 18.478 %에서 8.515 %로 줄었다. C-장애물의 *차원*이 바뀌는가? P2의 자유도가 바뀌는가? 그리고 관통 과제 — 도구를 카탈로그 목표의 패널에 붙이기 — 는 여전히 해가 있는가?

> [!note]- 그리는 법 · How to draw it
> - 그림 두 장을 나란히: 왼쪽은 작업 영역, 오른쪽은 C-space 도표.
> - 작업 영역: 원점의 베이스, 엘보가 그리는 단위원, 그리고 벽을 그 $x$ 위치의 수직선으로 긋고 팔이 들어가면 안 되는 쪽에 빗금을 친다. 벽이 그 원에 닿는지 밝힌다. 위의 그림의 벽 $x = 1$은 $(1,0)$에서 원에 접한다.
> - 컨피규레이션마다 링크를 하나씩 그린다. 엘보는 $(\cos\theta_1, \sin\theta_1)$, 말단은 거기서 절대각 $\theta_1 + \theta_2$ 방향으로 한 단위 더 간 곳이다. 적어도 카탈로그 자세 $(0°, 90°)$는 그리고, 목표 $(1,1)$을 표시한다.
> - 도표: 가로 $\theta_1$, 세로 $\theta_2$, 둘 다 $-180°$에서 $180°$인 정사각형에 좌·우 변끼리, 위·아래 변끼리 같은 화살표를 그린다. 화살표가 없으면 정사각형은 원환면이 아니라 직사각형이다.
> - 팔이 패널을 파고드는 영역을 칠한다. 양 끝에서 한 점으로 오므라드는 렌즈다. 오므라드는 두 점의 $\theta_1$을 표시한다(위의 그림에서는 $\pm 90°$).
> - 렌즈의 경계에 "접촉"이라고 쓴다. $d = 0$인 컨피규레이션은 칠한 영역 안이 아니라 그 곡선 위의 점이고, $d < 0$인 컨피규레이션은 렌즈 밖에 있다.

> [!tip]- 정답 · Solutions
> 1. 작업 영역: 엘보 원의 반지름이 1이고 벽이 $x=1.5$이므로 가장 가까운 엘보 점 $(1,0)$도 $0.5\,\mathrm{m}$ 떨어진다. 링크 1은 이제 어디서나 엄격히 자유다. C-space: 더 작은 렌즈, $\theta_1 = \pm 60°$에서 오므라든다. 카탈로그 자세는 $\cos 0° + \cos 90° = 1 < 1.5$이므로 $d = -0.5$. 접촉 컨피규레이션이 아니라 내부의 자유 컨피규레이션이 되었다.
> 2. (a) $d(\theta) = \max(\cos\theta_1,\ \cos\theta_1 + \cos(\theta_1{+}\theta_2)) - 1.5$이고 $\cos\theta_1 \le 1 < 1.5$이므로 엘보 항은 항상 음수다. 말단만 위반할 수 있다. (b) $\cos\varphi$가 1이어야 하는 곳, 즉 $\cos\theta_1 = 0.5$에서 오므라들므로 $\theta_1 = \pm 60°$. $\theta_1 = 0°$: $\cos\varphi = 0.5$, $\varphi = \pm 60°$, 따라서 $\theta_2 = \pm 60°$. $\theta_1 = 30°$: $\cos\varphi = 1.5 - 0.8660 = 0.6340$, $\varphi = \pm 50.66°$, 따라서 $\theta_2 = 20.66°$ 또는 $-80.66°$. (c) 곧게 편 팔: 말단이 $2\cos\theta_1 > 1.5$, 즉 $\cos\theta_1 > 0.75$이므로 $|\theta_1| < 41.41°$.
> 3. 차원은 바뀌지 않는다. $\mathcal{C}_{\text{obs}}$는 2차원 공간의 열린 부분집합이라 더 작아질 뿐 여전히 2차원이다. P2의 자유도도 여전히 2다. 그뤼블러는 링크와 관절을 세는데 둘 다 그대로이고, 장애물은 부등식이라 애초에 계산에 들어가지 않는다. 과제는 쓰인 대로는 해를 잃는다. 카탈로그 목표 $(1,1)$은 $x = 1 < 1.5$라 더 이상 면 위가 아니므로 접촉 목표를 다시 정해야 한다. 곧장 밖으로 가장 가까운 면 위의 점은 $(1.5, 1)$이고 반지름이 $\sqrt{1.5^2+1^2} = 1.803 < 2$이라 작업 영역 안에 있으므로 새 과제는 실행 가능하다.

### 출처 · Sources

- K. M. Lynch, F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — 2장 §2.1–§2.5(자유도, 그뤼블러 공식, C-space의 위상, 파피안 제약, 작업 공간과 작업 영역), 그리고 §2의 C-장애물과 접촉 약속은 §10.1–§10.3과 §13.3. 무료 PDF는 [[04-robotics/modern-robotics-book|책 안내]]에 있다.
- 렌즈와 그 18.478 %를 비롯한 이 페이지의 모든 숫자는 P2의 카탈로그 숫자와 패널 $x \ge 1$로 여기서 직접 계산한 것이다. 믿지 말고 다시 계산하라.
