---
title: 17. Traversability & Off-Road Autonomy
tags: [robotics, navigation, unstructured]
study-depth: Working
wiki-support: Working
depth-goal: "Say what traversability actually is in current research, judge whether a paper claims adaptation or generalization, and read a field-autonomy result for what it established."
mastery-when: "Raise to Mastery only if terrain interaction or the traversability model itself becomes the contribution — the research program keeps navigation supporting."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to choose a traversability approach, and to see through the most
> common overclaim in the area.
> **Working** — traversability 접근법을 고르고, 이 분야에서 가장 흔한 과잉 주장을 꿰뚫어 볼 만큼.

> [!note] Prerequisites · 선수 지식
> You need occupancy and cost representations ([[04-robotics/planning-decision-making|4. Planning §2]]), MPC ([[04-robotics/mpc|MPC]]), and self-supervision — a training signal built from the data's own structure rather than labels ([[02-foundations/ml-practice|9. ML Practice]]).
> 점유·비용 표현([[04-robotics/planning-decision-making|4. 계획 §2]]), MPC([[04-robotics/mpc|MPC]]), 그리고 자기지도 — 라벨이 아니라 데이터 자신의 구조에서 만든 학습 신호([[02-foundations/ml-practice|9. ML 실무]]) — 가 필요하다.

## English

*Group I. Stands on [[04-robotics/mpc|7. MPC]], [[04-robotics/planning-decision-making|4. Planning]] and [[02-foundations/ml-practice|ML Practice]].
The reframing that reorganised the field: traversability is a learned affordance of a particular robot, not a geometric property of terrain.*

> [!note] First pass · 처음이라면
> Read §1 — one reframing that reorganised the field — then §2 on where the labels come from, then §6. §4 and §5 are a record of what each field programme established; read them when you need to cite one. The running object and the worked derivation that follows §1 turn §1's claim into arithmetic; do them if you are here for the course rather than for the literature.

### Running object · 이 페이지의 장치

Traversability is a property of a robot *and* a patch of ground, so this page freezes one of each.

**The patch.** A $3\times3$ window of the robot-centric elevation map that §3 describes, cell size
$c=0.20$ m, heights in metres, $x$ east and $y$ north, rows printed north to south:

$$H=\begin{pmatrix}0.08&0.12&0.16\\0.06&0.10&0.14\\0.04&0.08&0.32\end{pmatrix}$$

Eight of the nine cells lie exactly on the plane $h=0.10+0.20x+0.10y$; the ninth, the south-east
corner, has been raised to $0.32$ m. So the patch is a clean ramp with one rock on it, and every
number derived below is either the ramp or the rock — which is what makes it possible to say, at the
end, which of them each traversability term was actually measuring.

**The machines.** Two of them, because §1's first consequence is that the same patch has different
costmaps for different robots.

| Limit | **Q**, the quadruped | **T**, a tracked vehicle |
|---|---:|---:|
| $\theta_{\max}$, slope | $25^\circ$ | $30^\circ$ |
| $h_{\max}$, step-over | $0.15\,\mathrm{m}$ | $0.40\,\mathrm{m}$ |
| $\sigma_{\max}$, roughness | $0.05\,\mathrm{m}$ | $0.10\,\mathrm{m}$ |

Both use the same weights $(w_\theta,w_h,w_\sigma)=(0.4,0.4,0.2)$.

Q is the frozen quadruped of [[04-robotics/legged-locomotion|18. Legged Locomotion]] — $12$ kg, CoM
$0.30$ m up, feet at $(\pm0.30,\pm0.15)$ m — and its $\theta_{\max}$ is *not* a stipulation. Q tips
sideways about a lateral foot pair when the CoM projection crosses the $0.15$ m half-width, at
$\arctan(0.15/0.30)=26.6^\circ$, so $25^\circ$ is that angle with a degree and a half of margin. Its
$h_{\max}$ and $\sigma_{\max}$ are catalog numbers, stated once and changed only in a problem set.
T is frozen by these three limits and nothing else; it exists here for the contrast.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="the frozen three by three elevation patch: eight cells on a plane and one raised corner cell">
  <defs><marker id="arT" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1" stroke-opacity="0.55">
    <rect x="170" y="54" width="64" height="44"/><rect x="234" y="54" width="64" height="44"/><rect x="298" y="54" width="64" height="44"/>
    <rect x="170" y="98" width="64" height="44"/><rect x="234" y="98" width="64" height="44"/><rect x="298" y="98" width="64" height="44"/>
    <rect x="170" y="142" width="64" height="44"/><rect x="234" y="142" width="64" height="44"/>
  </g>
  <g fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"><rect x="298" y="142" width="64" height="44"/></g>
  <g font-size="11.5" fill="currentColor" text-anchor="middle">
    <text x="202" y="82">0.08</text><text x="266" y="82">0.12</text><text x="330" y="82">0.16</text>
    <text x="202" y="126">0.06</text><text x="266" y="126">0.10</text><text x="330" y="126">0.14</text>
    <text x="202" y="170">0.04</text><text x="266" y="170">0.08</text><text x="330" y="170">0.32</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="202" y="46">x = &#8722;0.20</text><text x="266" y="46">0</text><text x="330" y="46">+0.20</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8" text-anchor="end">
    <text x="163" y="80">y = +0.20</text><text x="163" y="124">0</text><text x="163" y="168">&#8722;0.20</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" marker-end="url(#arT)">
    <line x1="382" y1="196" x2="422" y2="196"/><line x1="382" y1="196" x2="382" y2="164"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="426" y="200">+x east</text><text x="388" y="160">+y north</text>
    <text x="382" y="128">cell 0.20 m</text>
    <text x="382" y="76">heights in metres</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="218">Eight cells lie exactly on h = 0.10 + 0.20x + 0.10y &#8212; a clean 12.6&#176; ramp.</text>
    <text x="40" y="234">The shaded corner was raised to 0.32 m. One cell moves the fitted slope by 7.8&#176;, supplies</text>
    <text x="40" y="250">56% of the roughness, and is the only reason the step-height term exists at all.</text>
  </g>
</svg>

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="the middle row seen side-on and drawn to scale, where the least-squares line rises 8.8 degrees more steeply than the central-difference line through 0.06, 0.10 and 0.14, beside the slope, step and roughness bars for Q and T over each robot's own limit, of which only Q's step bar, 1.600, crosses the gate at 1">
  <g font-size="12" fill="currentColor" opacity="0.9">
    <text x="12" y="16">The two slopes</text><text x="296" y="16">The decision</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.75">
    <text x="12" y="31">middle row seen from the south, drawn 1:1</text><text x="296" y="31">each term over that robot's own limit</text>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <line x1="34" y1="165" x2="238" y2="165"/>
    <line x1="34" y1="165" x2="34" y2="170"/><line x1="102" y1="165" x2="102" y2="170"/><line x1="170" y1="165" x2="170" y2="170"/><line x1="238" y1="165" x2="238" y2="170"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.4" stroke-dasharray="2 3"><line x1="204" y1="62.2" x2="204" y2="165"/></g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.4" stroke-dasharray="2 3"><line x1="68" y1="148.6" x2="68" y2="165"/><line x1="136" y1="135" x2="136" y2="165"/></g>
  <g stroke="currentColor" stroke-width="1.7" fill="none">
    <line x1="34" y1="151.4" x2="238" y2="110.6"/>
    <line x1="34" y1="160.8" x2="238" y2="86" stroke-dasharray="7 4"/>
  </g>
  <path d="M229.9 112.2 A142 142 0 0 0 224 91.2" stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.8"/>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="204" y1="117.4" x2="204" y2="98.5"/><line x1="200" y1="98.5" x2="208" y2="98.5"/>
  </g>
  <g fill="currentColor"><circle cx="68" cy="144.6" r="3.6"/><circle cx="136" cy="131" r="3.6"/><circle cx="204" cy="117.4" r="3.6"/></g>
  <rect x="199" y="51.2" width="10" height="10" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <g font-size="11" fill="currentColor">
    <text x="194" y="60.2" text-anchor="end">rock, one row south: 0.32</text>
    <text x="198" y="90.5" text-anchor="end">0.0556 m</text>
    <text x="243" y="102.3">8.8°</text>
    <text x="72" y="160">0.06</text>
    <text x="140" y="160">0.10</text>
    <text x="208" y="160">0.14</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="68" y="182">−0.20</text><text x="136" y="182">0</text><text x="204" y="182">+0.20</text>
  </g>
  <text x="243" y="182" font-size="11" fill="currentColor" opacity="0.8">x (m)</text>
  <g stroke="currentColor" stroke-width="1.7" fill="none">
    <line x1="12" y1="202" x2="34" y2="202"/><line x1="12" y1="219" x2="34" y2="219" stroke-dasharray="7 4"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="40" y="206">central difference (the dots): 11.3°</text><text x="40" y="223">least squares (all nine cells): 20.1°</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="5 3"><line x1="458" y1="50" x2="458" y2="184"/></g>
  <text x="458" y="46" font-size="11" fill="currentColor" text-anchor="middle">gate</text>
  <g font-size="11" fill="currentColor"><text x="296" y="60">Q (25°, 0.15 m, 0.05 m)</text><text x="552" y="60" text-anchor="end">gate trips</text></g>
  <rect x="362" y="66" width="78.5" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="75.8" text-anchor="end" opacity="0.85">slope</text><text x="436.5" y="75.8" text-anchor="end">0.818</text></g>
  <rect x="362" y="82" width="153.6" height="12" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="91.8" text-anchor="end" opacity="0.85">step</text><text x="511.6" y="91.8" text-anchor="end">1.600</text></g>
  <rect x="362" y="98" width="95.4" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="107.8" text-anchor="end" opacity="0.85">roughness</text><text x="453.4" y="107.8" text-anchor="end">0.994</text></g>
  <g font-size="11" fill="currentColor"><text x="296" y="127">T (30°, 0.40 m, 0.10 m)</text><text x="552" y="127" text-anchor="end">clear, C = 0.612</text></g>
  <rect x="362" y="133" width="65.4" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="142.8" text-anchor="end" opacity="0.85">slope</text><text x="423.4" y="142.8" text-anchor="end">0.681</text></g>
  <rect x="362" y="149" width="57.6" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="158.8" text-anchor="end" opacity="0.85">step</text><text x="415.6" y="158.8" text-anchor="end">0.600</text></g>
  <rect x="362" y="165" width="47.7" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="174.8" text-anchor="end" opacity="0.85">roughness</text><text x="405.7" y="174.8" text-anchor="end">0.497</text></g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <line x1="362" y1="184" x2="520.4" y2="184"/><line x1="362" y1="184" x2="362" y2="188"/><line x1="410" y1="184" x2="410" y2="188"/><line x1="458" y1="184" x2="458" y2="188"/><line x1="506" y1="184" x2="506" y2="188"/>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="362" y="199">0</text><text x="410" y="199">0.5</text><text x="458" y="199">1</text><text x="506" y="199">1.5</text>
  </g>
  <text x="296" y="216" font-size="11" fill="currentColor" opacity="0.85">where σ² comes from, cell by cell</text>
  <rect x="296" y="222" width="142.2" height="15" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <rect x="438.2" y="222" width="113.8" height="15" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  <g font-size="11" fill="currentColor"><text x="301" y="233.5">the rock, 56%</text><text x="443.2" y="233.5">the other eight, 44%</text></g>
  <text x="12" y="254" font-size="11" fill="currentColor" opacity="0.9">Full slopes, with the north–south gradient added: the ramp 12.6°, the fit 20.4°, 7.8° apart.</text>
</svg>

The frozen patch, a $3\times3$ window of the elevation map with $0.20$ m cells and heights in metres: eight cells lie exactly on the plane $h=0.10+0.20x+0.10y$, a clean $12.6^\circ$ ramp, and the shaded south-east corner is the rock, raised to $0.32$ m. That one cell moves the fitted slope by $7.8^\circ$, supplies $56\%$ of the roughness, and is the only reason the step-height term exists at all. In the figure under the patch, the middle row seen side-on has the least-squares trace $8.8^\circ$ steeper than the central-difference line through $0.06$, $0.10$ and $0.14$ ($7.8^\circ$ once the north–south gradient is added), and of the bars, each term over the robot's own limit, only Q's step bar, at $1.600$, crosses the gate at $1$. Every number in the worked derivation after §1 — two slopes, a step, a roughness, and opposite verdicts for Q and T — comes from these nine heights.

### 1. The idea that reorganised the field

A classical planner builds an occupancy grid, marks occupied cells as obstacles, and plans
around them. Put that robot in tall grass and it stops, because grass returns lidar hits and
lidar hits mean obstacle.

The correction is the premise of everything on this page:

> **Traversability is not a geometric predicate. It is a robot-specific, velocity-conditioned
> affordance learned from the robot's own experience of driving somewhere.**

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="the same three terrain patches read two ways: an occupancy grid and a learned affordance">
  <g font-size="10.5" fill="currentColor" opacity="0.8">
    <text x="40" y="14">one scene, three patches</text>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="32" font-size="11" text-anchor="middle">tall grass</text>
    <text x="280" y="32" font-size="11" text-anchor="middle">smooth concrete</text>
    <text x="445" y="32" font-size="11" text-anchor="middle">rubble pile</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="52">What geometry says &#8212; occupancy grid</text>
  </g>
  <g>
    <rect x="40" y="58" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="205" y="58" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="370" y="58" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  </g>
  <g fill="currentColor">
    <text x="115" y="81" font-size="11" text-anchor="middle">obstacle</text>
    <text x="280" y="81" font-size="11" text-anchor="middle">free</text>
    <text x="445" y="81" font-size="11" text-anchor="middle">obstacle</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="122">What driving experience says &#8212; this robot, this speed</text>
  </g>
  <g>
    <rect x="40" y="128" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="205" y="128" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="370" y="128" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  </g>
  <g fill="currentColor">
    <text x="115" y="151" font-size="11" text-anchor="middle">passable</text>
    <text x="280" y="151" font-size="11" text-anchor="middle">preferred</text>
    <text x="445" y="151" font-size="11" text-anchor="middle">obstacle</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.75" stroke-dasharray="4 3">
    <path d="M32,76 C14,88 14,116 32,128"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="196" y="106" text-anchor="end">this cell flips</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="178">&#8220;A lidar return is an obstacle&#8221; is the rule that stops the robot in grass.</text>
    <text x="40" y="193">Cost learned from consequences flips that cell. And the bottom row moves when the</text>
    <text x="40" y="208">robot or the commanded speed changes &#8212; the top row never does.</text>
  </g>
</svg>

BADGR is the canonical statement. It trains a predictive model on **self-supervised
off-policy real-world data** — no simulator, no human labels — with events like collision
and bumpiness auto-labelled from the IMU, LIDAR and wheel odometry, and a model that takes only the RGB image and the planned actions (GPS supplies the goal). The result is a
robot that drives *through* the grass and prefers smooth concrete, having learned both
preferences from consequences rather than from geometry.

Three consequences worth stating, because they are what a textbook does not prepare you for:

- **The same scene has different costmaps for different robots.** A 12-ton tracked vehicle
  and a quadruped disagree about a rubble pile, and neither is wrong.
- **Cost depends on commanded speed.** Terrain that is fine at 1 m/s is not fine at 10 m/s,
  so a costmap conditioned on velocity is a different object from a static one.
- **Terrain that a planner calls impassable is often passable.** The Verti-Wheelers line
  makes this its thesis: the ICRA 2024 paper names "irregular boulders and fallen trees" that classical planners
  label non-traversable are crossable by *ordinary wheeled robots with **little** hardware
  modification* — the paper's own hedge. The rocky outcroppings and the "3D, 6-DoF vehicle-terrain dynamics model in SE(3)" come from the group's companion paper, [arXiv:2306.11611](https://arxiv.org/abs/2306.11611), not from this one. That reframes traversability as a
  **modelling** problem rather than a segmentation problem.

### Worked on the patch · 패치로 한 번 끝까지

The three consequences above are claims. Here they are as arithmetic on the frozen patch, and the
problem set is the same arithmetic with the rock changed.

**1. Slope, computed two ways that disagree.** The **slope** of a cell is the angle between the
terrain's local surface normal and vertical — equivalently, the arctangent of the height field's
gradient magnitude there. It is an angle in $[0^\circ,90^\circ)$, it is a property of a *fitted*
surface rather than of the raw cells, and that is where the trouble starts, because the fit is a
choice.

*Central differences at the centre cell.* Take the east–west and north–south neighbours of the middle
cell, so only four of the nine heights are used:

$$g_x=\frac{0.14-0.06}{2c}=\frac{0.08}{0.40}=0.20,\qquad g_y=\frac{0.12-0.08}{2c}=\frac{0.04}{0.40}=0.10,\qquad \theta=\arctan\sqrt{0.20^2+0.10^2}=\arctan 0.2236=12.60^\circ$$

*Least squares over all nine.* Fit $h=a+bx+c_0y$, writing $c_0$ because $c$ is already the cell size. The nine sample points are centred and symmetric, so
$\sum x_i=\sum y_i=\sum x_iy_i=0$ and the three estimates decouple into one-line quotients:

$$b=\frac{\sum x_ih_i}{\sum x_i^2}=\frac{0.088}{0.24}=0.3667,\qquad c_0=\frac{\sum y_ih_i}{\sum y_i^2}=\frac{-0.016}{0.24}=-0.0667,\qquad a=\bar h=\frac{1.10}{9}=0.1222$$

because with the sums decoupled each coefficient is just a weighted average of the heights along its
own axis. The pieces are $\sum x_i^2=\sum y_i^2=6(0.20)^2=0.24$,
$\sum x_ih_i=0.2(0.16+0.14+0.32)-0.2(0.08+0.06+0.04)=0.088$ and
$\sum y_ih_i=0.2(0.36)-0.2(0.44)=-0.016$. The slope is then
$\arctan\sqrt{0.3667^2+0.0667^2}=\arctan 0.3727=20.44^\circ$.

The two estimators disagree by $7.83^\circ$ on the same nine numbers, and the north–south gradient
even changes sign, from $+0.10$ to $-0.0667$. Neither is wrong. The central difference never touched
the corner cell, so it reports the ramp; the plane fit weights that corner as heavily as any other
cell, so the rock reaches it and it reports a tilted compromise. **A paper reporting "slope
threshold $25^\circ$" has not yet told you which of these two numbers it thresholded** — and on this
patch that omission is worth almost eight degrees.

**2. Step height.** The **step height** of a window is the largest absolute height difference between
4-connected neighbouring cells in it. It is a length, it is defined on pairs rather than on cells, and
it is the term that asks whether a foot or a track can get *over* something rather than *up* it. On
the patch, every ramp pair differs by $0.20\times c=0.04$ m east–west or $0.10\times c=0.02$ m
north–south, so the maximum can only come from the rock:

$$\Delta h=\max_{i\sim j}\lvert h_i-h_j\rvert=\max(0.32-0.08,\ 0.32-0.14)=0.24\ \mathrm{m}$$

Non-example: step height is *not* the window's range $\max h-\min h=0.28$ m. That measure charges
the ramp's own rise to the step term, and a ramp is something a robot walks up, not something it
steps over. Confusing the two is the most common way a geometric costmap ends up refusing hills.

**3. Roughness.** The **roughness** of a window is the root-mean-square residual of its cell heights
about the fitted plane — a length, defined only relative to a fit, and it measures what the slope term
has already explained away. Using $\hat h=0.1222+0.3667x-0.0667y$, the nine residuals in metres are

$$\begin{pmatrix}+0.0444&+0.0111&-0.0222\\+0.0111&-0.0222&-0.0556\\-0.0222&-0.0556&+0.1111\end{pmatrix},\qquad \sigma=\sqrt{\tfrac{1}{9}\textstyle\sum r_i^2}=\sqrt{\tfrac{0.02222}{9}}=0.0497\ \mathrm{m}$$

The rock's own residual is $0.32-0.2089=0.1111$ m, so its square is $0.01235$ of the total $0.02222$:
**56% of the roughness comes from one of nine cells.** Non-example: roughness is not a stand-in for
difficulty. A perfectly smooth $40^\circ$ slab has $\sigma=0$ and will still roll a quadruped, which
is exactly why slope and roughness are separate terms rather than one "terrain badness" number.

**4. The cost, and the gate.** A **traversability cost** here is a scalar field over cells defined for
*a named robot*, made of two parts that behave differently: a hard **gate**, a predicate that says the
cell is off the map entirely, and a soft **cost** in $[0,1]$ that ranks the cells that survive it.
Three conditions define it. Each raw measurement is divided by that robot's own limit, so the terms are
dimensionless and comparable; the weights are nonnegative and sum to one, so the surviving cost lands
in $[0,1]$; and the gate is a separate predicate rather than a large number:

$$C=w_\theta\frac{\theta}{\theta_{\max}}+w_h\frac{\Delta h}{h_{\max}}+w_\sigma\frac{\sigma}{\sigma_{\max}},\qquad\text{untraversable if}\quad \max\Big(\frac{\theta}{\theta_{\max}},\frac{\Delta h}{h_{\max}},\frac{\sigma}{\sigma_{\max}}\Big)>1$$

The gate has to be a predicate and not a big finite cost, because a planner minimising a sum will
cheerfully pay $10^4$ to save two hundred metres, and a cell that rolls the robot is not a cell you
want purchasable at any price. Substituting the three measurements for each machine:

| Term | raw | **Q** ($25^\circ$, $0.15$ m, $0.05$ m) | **T** ($30^\circ$, $0.40$ m, $0.10$ m) |
|---|---:|---:|---:|
| slope | $20.44^\circ$ | $0.818$ | $0.681$ |
| step | $0.24\,\mathrm{m}$ | $\mathbf{1.600}$ | $0.600$ |
| roughness | $0.0497\,\mathrm{m}$ | $0.994$ | $0.497$ |
| gate | | **trips** | clear |
| $C$ | | $1.166$ | $0.612$ |

**The decision.** For Q the gate trips and the cell is untraversable; $C=1.166$ is printed only to be
compared, since a gated cell has no usable cost. For T nothing trips and the cell is ordinary
mid-range terrain at $C=0.612$. One patch, nine numbers, opposite verdicts — which is §1's first
consequence with the hand-waving removed.

Two things to read off the table. The term that decides for Q is **step height, not slope**, and it is
not close: $1.60$ against $0.818$. A paper that reports only a slope threshold has reported the term
that was never going to bind. And the roughness term sits at $0.994$ — raise the rock by one more
centimetre, to $0.33$ m, and $\sigma$ becomes $0.0522$ m and that term trips the gate *on its own*.
A cell can be one centimetre from being refused for a reason nobody is watching.

**5. What P2 does to the verdict.** [[04-robotics/legged-locomotion|18. Legged Locomotion]] computes
that mounting P2 raises Q's centre of mass from $0.30$ m to $0.371$ m, so the lateral tip-over angle
falls from $26.6^\circ$ to $\arctan(0.15/0.371)=22.0^\circ$ and the honest $\theta_{\max}$ for the
loaded robot is $22^\circ$, not $25^\circ$. The slope term becomes $20.44/22=0.929$: within $7\%$ of
its own gate, on terrain that was comfortable at $0.818$ unloaded. The gate still trips on step height,
so the verdict does not change here — but the slope term's own margin is mostly gone, with no
change in the ground at all. That sharpens §1's claim from "traversability is
robot-specific" to **robot-configuration-specific**, and it is the concrete reason a costmap built on
an unloaded survey pass does not transfer to the loaded return trip.

### 2. Where the supervision comes from

Every method here is defined by what it uses as a label, and that is the useful axis.

| Supervision source | What it means | Representative |
|---|---|---|
| **Onboard event detection** | collisions and bumpiness auto-labelled from sensors | BADGR |
| **Proprioceptive consequence** | IMU and shock feedback — literally how it felt to drive there | *How Does It Feel?* |
| **Velocity tracking** | did the robot achieve the speed it commanded? | Wild Visual Navigation |
| **Predicted proprioception** | predict the experience a vehicle *would* undergo, from geometry | ScaTE |
| **An existing stack** | distil a slow classical pipeline into a fast learned one | RoadRunner |

**Wild Visual Navigation** is the system the current field is organised around. It runs
online, vision-only, on [[01-canonical-papers/notes/2-computer-vision/dino|DINO]] features (general-purpose image features learned without labels), supervised by the robot's own velocity tracking, with
**training and inference concurrent onboard** an ANYmal — and its claim is carefully
limited: *less than five minutes of in-field training* from a short human demonstration,
then 1.4 km of footpath following and high grass.

**How Does It Feel?** pairs vision with proprioceptive IMU and shock feedback and conditions
the costmap on commanded velocity, reporting a reduction in interventions of **up to 57%** against an
occupancy baseline over courses of 400 m to 3,150 m.

**SALON** is the sharpest current statement of the same thesis: online adaptation producing
joint **cost and speed** maps while actively avoiding unfamiliar terrain, claiming
kilometre-scale routes after *seconds* of real data, matching methods that need
"100–1000× more data".

> [!important] The claim divergence — read every paper for this
> The papers split, but not the way a first reading suggests — check each abstract rather
> than assuming.
>
> | Paper | Adaptation claim | Generalization claim |
> |---|---|---|
> | **WVN** | in-field, five minutes from a demonstration | yes — "can generalize to any ground robot" |
> | ***How Does It Feel?*** | **none** — self-supervision is offline, from proprioceptive feedback | — |
> | **SALON** | "within seconds" | yes — "promising results on significantly different robots in different environments" |
> | **V-STRONG** | — (the pure generalization case) | "unprecedented performance for generalization to new environments", zero- and few-shot |
>
> That disagreement is the
> most interesting open question in the thread, and the two claims require completely
> different evidence. When you read a traversability paper, the first thing to establish is
> which of the two it is claiming — the abstracts do not always make it obvious.

### 3. The geometric side did not go away

Two things a learning-first reading would miss.

**The elevation map underneath.** Nearly every legged-navigation paper assumes a
robot-centric 2.5D elevation map that propagates pose-estimate drift and sensor uncertainty
into a **per-cell variance** (because each cell's height was computed from where the sensor
was *believed* to be when it saw that cell, an error in that belief becomes an error in the height) — Fankhauser, Bloesch and Hutter's formulation, shipped as the
`elevation_mapping` ROS package. Learned traversability usually runs *on top of* this, not
instead of it.

**Risk-aware geometric planning.** STEP is the counterweight: uncertainty-aware
traversability evaluation, **tail-risk assessment via Conditional Value-at-Risk (CVaR)**,
and a risk-constrained kinodynamic MPC solved by sequential quadratic programming (SQP: solve a quadratic-program approximation at each iterate — [[02-foundations/optimization|4. Optimization §4]]). It is not
a learning paper and makes no generalization claim; it plugs straight into the material in
[[04-robotics/mpc|MPC]] and it is the traversability module of the NeBula stack that
competed in DARPA SubT.

CVaR is worth knowing as a modelling choice rather than a detail: optimising the *mean*
outcome and optimising the *worst decile* give different plans, and on terrain where the
failure is a rollover rather than a delay, the second is the right objective.

> [!example] Worked example · 계산 예제
> **Why the geometric side runs out at range.** A 64-beam lidar at 1.8 m height with 0.4°
> vertical spacing puts consecutive rings on flat ground at $r = h/\tan\theta$. Two beams near
> $\theta = 5.15°$ and $5.55°$ land at $1.8/\tan 5.15° = 20.0$ m and $1.8/\tan 5.55° = 18.5$ m —
> a ring spacing of **1.4 m**. The same pair of beams near $\theta = 10.2°$ and $10.6°$ land at
> 10.00 m and 9.62 m: **0.39 m**.
>
> So a flat 0.3 m hazard — a rut or a hole — gets roughly one ring at 10 m and usually **none** at 20 m; ring spacing already exceeds 0.3 m beyond about 9 m. (A rock 0.3 m *tall* still catches about two returns on its face at 20 m: enough to detect, not to characterise.) It is not
> that the geometry is noisy out there; there is almost no geometry out there.
>
> **The reading this gives you.** A vehicle at 5 m/s that spends 4 s reacting and braking at near-full speed needs about 20 m of
> assessed terrain (braking uniformly to rest in 4 s would need 10 m), which is well past the range where ring spacing exceeds hazard size. That
> is the structural reason the field moved to learned traversability from images: not because
> learning is better at classifying rocks, but because at the range where the decision has to be
> made, appearance is the only signal that still has resolution. When a paper reports lidar-based
> traversability, its top speed and its lookahead are the two numbers that tell you whether it
> ever entered this regime.

### 4. What the field programmes established

**DARPA SubT** (2018–2021) is the largest empirical event in unstructured-environment
autonomy. Team CERBERUS won the Systems track with a **heterogeneous legged-plus-aerial
system-of-systems** — four ANYmal C quadrupeds as the backbone — with resilient multi-modal
SLAM under communication- and GPS-denied conditions. That result, more than any single
paper, converted "legged robots in the field" from a demonstration into an engineering
result. The other complete published stack is **NeBula**, whose organising idea is
**belief-space, uncertainty-aware modular autonomy**: reasoning and deciding over
distributions rather than over point estimates.

**DARPA RACER** (2021 → completion announced January 2026) took the same question to speed.
Its stated goal was off-road traversal limited only by sensor performance, mechanical
constraints and safety, with parity to a human driver as the minimum bar; its stack ran
**without GPS and without pre-mapped routes**, on a drive-by-wire Polaris RZR and a ~12-ton
tracked platform. DARPA names the **perception architecture** as the headline outcome and
cites retraining for a new environment dropping from weeks to a day.

> [!warning] Three citation traps in this area
> - **DARPA does publish RACER speed and distance figures — use them, and cite darpa.mil.**
>   The 2023 release reports 55+ driverless runs of roughly 4–11 miles at about 25 mph, and
>   246 miles over 24.6 hours on course; the 2024 release reports 30+ runs on 3–10 mile
>   courses, 150+ autonomous unoccupied miles, and speeds **up to 30 mph**. (An earlier
>   version of this page asserted the opposite and told you not to quote a top speed — that
>   was wrong.) Paper-level numbers complement rather than replace them: RoadRunner states up
>   to **15 m/s** on the Polaris RZR, and its 20 m/s figure is a *design* statement about
>   prediction cadence, not a measured run.
> - **RACER expands to *Robotic Autonomy in Complex Environments with Resiliency*,** not
>   "Rapid Autonomy". And there is a **name collision**: a separate paper titled "RACER:
>   Epistemic Risk-Sensitive RL" is a 1/10-scale rally-car method with no connection to the
>   programme.
> - **CODa is an urban campus dataset**, not off-road, despite being cited that way.

### 5. Datasets, and what each one actually established

| Dataset | What it established |
|---|---|
| **RUGD** (IROS 2019) | made off-road **semantic segmentation** a measurable task — images only |
| **RELLIS-3D** (ICRA 2021) | forced **LiDAR** into the conversation; its diagnostic finding is that **models designed for urban segmentation fail on it** |
| **TartanDrive** (ICRA 2022) | ~200k off-road interactions across 7 modalities — reframed off-road learning around **dynamics** rather than segmentation |
| **GOOSE** (ICRA 2024) | 10,000 labelled image + point-cloud pairs, and — the real contribution — a **published ontology** that made cross-dataset off-road labelling comparable |
| **GOOSE-Ex** (ICRA 2025) | adds 5,000 frames from a **robotic excavator** and a quadruped, for cross-embodiment |

GOOSE-Ex is the one to notice from this wiki's angle: an off-road perception dataset that
includes construction machinery is the nearest existing bridge between this page and
[[05-construction-robotics/construction-manipulation|9. Construction Manipulation]].

### 6. Reading a traversability paper

| Question | What a vague answer hides |
|---|---|
| Adaptation or generalization? | They need different evidence and the field disagrees |
| What supplied the labels? | The supervision source *is* the method |
| Is the costmap conditioned on speed? | An unconditioned costmap is wrong at some speed |
| Which robot, and would the map transfer? | Traversability is robot-specific by construction |
| Is there a geometric layer underneath? | Most learned methods sit on an elevation map they do not mention |
| Distance and intervention count, not just success | Field autonomy's honest metric is interventions per kilometre |

### After reading

- [ ] Compute slope, step height and roughness on the frozen patch and say which term gates it for Q.
- [ ] Say why the same nine numbers make the cell untraversable for Q and ordinary for T.
- [ ] State why tall grass is the canonical counterexample to occupancy mapping.
- [ ] Name three supervision sources and the paper for each.
- [ ] Explain the adaptation-versus-generalization divergence and why it matters.
- [ ] Say what CVaR buys over optimising the mean.
- [ ] Name what SubT and RACER each established, citing DARPA's own published speed and distance figures.

> [!tip] Going deeper · 더 깊이
> There is no textbook and no survey that has held up, so the substitute is three papers read as a single argument. BADGR (*RA-L* 2021) first, because it states the reframing in its barest form — the robot labels its own terrain by driving on it. Then "How Does It Feel?" (ICRA 2023) for the same idea with proprioception producing a costmap. Then Wild Visual Navigation, cited as RSS 2023 for priority and read as the 2025 *Autonomous Robots* version for the full system. After those three, the field-programme record in §4 is readable as evidence rather than as a list of names.

### Self-check

1. A paper reports a traversability model trained on one robot and deployed on another with
   no retraining. What should you check first?
2. Why does a costmap need to know the commanded velocity?
3. A learned traversability system reports 95% success on a 2 km course. What is the more
   informative number to ask for?
4. Someone cites "RACER" for a reinforcement-learning method on a small car. What has
   happened?
5. Your project involves an excavator on rough ground. Which dataset on this page is the
   nearest starting point, and what is still missing from it?
6. A costmap computes slope by central differences on a $0.20$ m grid and thresholds at
   $25^\circ$. What class of hazard does it structurally miss?

> [!tip]- Answers
> 1. Whether the paper claims *adaptation* or *generalization*, and whether the second robot's dynamics are close enough for the first robot's learned consequences to be valid. Traversability is robot-specific by construction — a rubble pile a tracked vehicle crosses easily may roll a quadruped — so cross-robot transfer is a strong claim needing its own evidence, not a free consequence of the visual features being general.
> 2. Because traversability is a function of what the robot is trying to do, not only of what the terrain is. Ruts that are comfortable at 1 m/s can pitch a vehicle at 10 m/s, so a single static cost is wrong at one end of the speed range. Conditioning on commanded velocity is what lets one map serve a whole speed envelope — which is why *How Does It Feel?* conditions its cost on velocity, and SALON predicts a speed map alongside its cost map.
> 3. **Interventions per kilometre**, plus the distance itself. Success rate on a fixed course conflates "drove it cleanly" with "drove it after three operator rescues", and the intervention count is the number that tracks deployability. *How Does It Feel?*'s headline is exactly this — an up-to-57% reduction in interventions — rather than a success percentage.
> 4. A name collision. The DARPA programme is *Robotic Autonomy in Complex Environments with Resiliency*; a separate, unrelated paper uses RACER for an epistemic risk-sensitive RL method on a 1/10-scale rally car. Both are real; citing one for the other is a common error.
> 5. **GOOSE-Ex**, because it is the only off-road perception dataset here containing a robotic excavator, and it was built for cross-embodiment generalization. What is still missing is everything about the machine's own state — no actuator, joint, hydraulic-pressure or force channel is released, which is the same gap [[06-research-practice/simulators-benchmarks-datasets|7. §8]] documents across the whole construction dataset landscape.
> 6. Anything whose signature is a pairwise or diagonal height difference rather than a gradient: a boulder on a corner cell, a kerb, a narrow ditch that falls between the stencil's arms. The frozen patch is the minimal example — the corner rock moves the least-squares slope by $7.83^\circ$ and pushes the step height to $0.24$ m while leaving the central difference at exactly $12.60^\circ$. The fix is not a finer slope estimator; it is a separate step-height term, because no gradient of a fitted surface can express a quantity defined on pairs of cells.

**Worked: the three readings the homework asks.** Tall grass occupied in lidar is the canonical counterexample; BADGR or *How Does It Feel?* replaces the occupancy label with consequence. Interventions per kilometre beat 95% success. CVaR, not the mean, is the excavator-on-a-slope objective.

### Problem set · 과제

Tier B. Using this page's patch, **Q**, **T**, and **P2** from [[02-foundations/lab-plants|0.6]].
Hand arithmetic only — nine numbers do not need a simulator.

**The change of knobs.** The rock is smaller: the south-east cell is $0.20$ m, not $0.32$ m. A kerb,
not a boulder. Everything else — cell size, the other eight heights, both machines' limits, the
weights — is unchanged.

1. **Draw.** All three panels of the picture above, for the new patch. Left: the grid with the corrected corner. Middle: the
   side view along the middle row with both fitted lines, and — this is the point of the redraw —
   the central-difference line *before* you compute anything, plus your prediction of whether it moves.
   Right: the three normalized bars against the gate line, drawn three times now: Q, Q carrying P2, and T.
2. **Derive.** (a) The central-difference slope at the centre cell. (b) The least-squares plane's
   $a$, $b$, $c_0$ and its slope, using the decoupled quotients. (c) The step height and the roughness.
   (d) The gate and $C$ for Q, for Q carrying P2 (use the $\theta_{\max}$ that page 18 derives for the
   loaded robot), and for T. Rank the three.
3. **Interpret.** One of your two slope estimates did not move at all between the lecture's patch and
   this one, while the verdict for Q flipped. Say which, say exactly why, and say what that implies
   about a costmap pipeline that computes slope from central differences on a $0.20$ m grid. Then:
   name the supervision source from §2 that would have reached the right answer on *both* patches
   without computing any of this, and state precisely what it needs that geometry does not.
4. **Read.** Three claims, using §1–§6 only. (a) A lidar occupancy map labels tall grass as occupied.
   Why is that the canonical counterexample, and what supervision source (name a paper) replaces the
   occupancy label? (b) A learned system reports 95% success on a 2 km course. Which number is more
   informative, and what two courses of driving does 95% conflate? (c) A planner minimises expected
   cost on a costmap. What does CVaR buy over the mean, and when is the mean the *wrong* objective for
   an excavator on a slope?

> [!note]- How to draw it · 그리는 법
> - **Left, the patch**: the $3\times3$ grid with the nine heights written in the cells, the cell size $c=0.20$ m marked on one edge, and arrows for $+x$ east and $+y$ north.
> - **Shade the south-east cell**: that one is the rock, and everything that follows turns on it.
> - **Middle, a side view along the middle row**: the three heights $0.06$, $0.10$, $0.14$ as dots over a ground axis, and a line through them — that is the central difference.
> - **The least-squares plane's trace through the same section as a second, steeper line**, with the vertical gap marked at the rock's column. The angle between the two lines in this section is the figure ($8.8^\circ$ in the worked derivation).
> - **Right, the decision**: three horizontal bars, one per normalized term $\theta/\theta_{\max}$, $\Delta h/h_{\max}$, $\sigma/\sigma_{\max}$, with a vertical line at $1$ marking the gate.
> - **One set of bars per machine, all on the same axis**: the point is which side of the line the same three raw measurements land on for each machine. In the worked derivation only Q's step bar crosses it, and all of T's stay short.

> [!tip]- Solutions
> 1. The middle panel's central-difference line is unchanged, because that estimator only ever reads the four edge-adjacent neighbours of the centre cell and the corner is not one of them. The right panel: Q's bars are all left of the gate now, Q-with-P2's slope bar has moved right but is still left of it, and T's are further left again.
> 2. (a) Unchanged: $g_x=0.20$, $g_y=0.10$, $\theta=12.60^\circ$. (b) $\sum x_ih_i=0.2(0.16+0.14+0.20)-0.2(0.08+0.06+0.04)=0.064$, so $b=0.064/0.24=0.2667$; $\sum y_ih_i=0.2(0.36)-0.2(0.32)=0.008$, so $c_0=0.008/0.24=0.0333$ — positive again, the sign flip was the rock's doing; $a=0.98/9=0.1089$; $\theta=\arctan\sqrt{0.2667^2+0.0333^2}=\arctan 0.2687=15.04^\circ$. (c) $\Delta h=0.20-0.08=0.12$ m; $\sigma=0.0199$ m. (d) Q: $15.04/25=0.602$, $0.12/0.15=0.800$, $0.0199/0.05=0.398$ — gate clear, $C=0.640$. Q with P2 at $\theta_{\max}=22^\circ$: $0.684$, $0.800$, $0.398$ — clear, $C=0.673$. T: $0.501$, $0.300$, $0.199$ — clear, $C=0.360$. Ranking T $<$ Q $<$ Q+P2, and for the first time all three can cross.
> 3. The central difference did not move, and it could not have: its stencil is the four 4-connected neighbours of the centre cell, and the cell that changed is a diagonal corner it never reads. So a pipeline computing slope by central differences on a $0.20$ m grid returns $12.60^\circ$ for a patch Q can cross and for a patch Q cannot — it is blind to exactly the feature that decides, and its agreement with the plane fit on smooth ground is what hides this. The fix is not a better estimator but a second term: step height is what separated the two patches ($1.60$ against $0.800$), and it is a pairwise quantity no gradient can express. As for §2 — **velocity tracking**, the supervision behind Wild Visual Navigation, would have got both right, because it asks whether the robot achieved the speed it commanded while actually driving there, which is the consequence all three geometric terms are proxies for. What it needs that geometry does not is *the robot having been there*: it is a record of experience, so it cannot score ground nobody has driven, and that is the whole reason §1's papers pair it with a vision model that generalises the label outward.
> 4. (a) Grass is occupied in the grid and traversable for many platforms. BADGR (drive-and-label), or proprioceptive cost (*How Does It Feel?*), replaces geometry with consequence. (b) Interventions per kilometre, plus the distance. 95% conflates a clean run with a run after operator rescues. (c) CVaR penalises the tail, not the average rut. A mean-optimal path can still include a rare roll-over; an excavator on a slope cares about that tail — and the gate in the worked derivation is the crudest possible version of the same instinct, a term you refuse to let the average buy off.

### Sources

- G. Kahn, P. Abbeel, S. Levine, "BADGR: An Autonomous Self-Supervised Learning-Based Navigation System," *IEEE RA-L*, vol. 6, no. 2, pp. 1312–1319, 2021 ([arXiv:2002.05700](https://arxiv.org/abs/2002.05700)).
- J. Frey, M. Mattamala, N. Chebrolu, et al., "Fast Traversability Estimation for Wild Visual Navigation," RSS 2023 ([arXiv:2305.08510](https://arxiv.org/abs/2305.08510)). Journal version: M. Mattamala et al., "Wild visual navigation: fast traversability learning via pre-trained models and online self-supervision," *Autonomous Robots*, vol. 49, no. 3, art. 19, 2025 — **the same system, two papers**; cite RSS for priority and the journal for the full description.
- M. Guaman Castro, S. Triest, W. Wang, et al., "How Does It Feel? Self-Supervised Costmap Learning for Off-Road Vehicle Traversability," ICRA 2023 ([arXiv:2209.10788](https://arxiv.org/abs/2209.10788)).
- M. Sivaprakasam, S. Triest, C. Ho, et al., "SALON: Self-supervised Adaptive Learning for Off-road Navigation," ICRA 2025 ([arXiv:2412.07826](https://arxiv.org/abs/2412.07826)).
- S. Jung, J. Lee, X. Meng, B. Boots, A. Lambert, "V-STRONG: Visual Self-Supervised Traversability Learning for Off-road Navigation," ICRA 2024 ([arXiv:2312.16016](https://arxiv.org/abs/2312.16016)) — the zero-shot generalization claim.
- D. D. Fan, K. Otsu, Y. Kubo, et al., "STEP: Stochastic Traversability Evaluation and Planning for Risk-Aware Off-road Navigation," RSS 2021 ([arXiv:2103.02828](https://arxiv.org/abs/2103.02828)).
- P. Fankhauser, M. Bloesch, M. Hutter, "Probabilistic Terrain Mapping for Mobile Robots With Uncertain Localization," *IEEE RA-L*, vol. 3, no. 4, pp. 3019–3026, 2018 — the `elevation_mapping` package.
- J. Frey, M. Patel, D. Atha, et al., "RoadRunner," accepted *IEEE T-FR* ([arXiv:2402.19341](https://arxiv.org/abs/2402.19341)); M. Patel et al., "RoadRunner M&M," *IEEE RA-L*, vol. 9, no. 12, pp. 11425–11432, 2024.
- A. Datar, C. Pan, M. Nazeri, X. Xiao, "Toward Wheeled Mobility on Vertically Challenging Terrain," ICRA 2024, pp. 16322–16329 ([arXiv:2303.00998](https://arxiv.org/abs/2303.00998)) — the Verti-Wheelers line, from George Mason University.
- M. Tranzatto, T. Miki, M. Dharmadhikari, et al., "CERBERUS in the DARPA Subterranean Challenge," *Science Robotics*, vol. 7, no. 66, eabp9742, 2022. Fuller account: *Field Robotics*, vol. 4, no. 1, pp. 249–312, 2024. NeBula: A. Agha et al. ([arXiv:2103.11470](https://arxiv.org/abs/2103.11470)).
- Datasets: RUGD (IROS 2019); P. Jiang et al., "RELLIS-3D," ICRA 2021 ([arXiv:2011.12954](https://arxiv.org/abs/2011.12954)); S. Triest et al., "TartanDrive," ICRA 2022 ([arXiv:2205.01791](https://arxiv.org/abs/2205.01791)); P. Mortimer et al., "GOOSE," ICRA 2024 ([arXiv:2310.16788](https://arxiv.org/abs/2310.16788)); R. Hagmanns et al., "GOOSE-Ex," ICRA 2025 ([arXiv:2409.18788](https://arxiv.org/abs/2409.18788)).

**Within this wiki**

- **Paper notes** — [[01-canonical-papers/notes/9-navigation/badgr|BADGR]] · [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]]
- [[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]] — the pose estimate whose drift the elevation map propagates
- [[04-robotics/mpc|MPC]] — what STEP's risk-constrained planner is a variant of
- [[04-robotics/legged-locomotion|18. Legged Locomotion]] — the robots most of this work runs on
- [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] — the construction end of terrain interaction

## 한국어

*I군이다. [[04-robotics/mpc|7. MPC]]·[[04-robotics/planning-decision-making|4. 계획]]과 [[02-foundations/ml-practice|ML 실무]] 위에 선다.
이 분야를 재편한 재프레이밍: 통과 가능성은 지형의 기하학적 성질이 아니라 특정 로봇이 학습한 어포던스다.*

> [!note] 처음이라면 · First pass
> 먼저 §1 — 이 분야를 재편한 재프레이밍 하나 — 그다음 라벨이 어디서 오는지인 §2, 그다음 §6. §4·§5는 각 필드 프로그램이 무엇을 확립했는지의 기록이니 인용이 필요할 때 읽어라. 이 페이지의 장치와 §1 뒤에 오는 유도는 §1의 주장을 산수로 바꾼다. 문헌이 아니라 수업 때문에 왔다면 그것부터 하라.

### 이 페이지의 장치 · Running object

통과 가능성은 로봇 *그리고* 한 뙈기의 땅에 대한 성질이다. 그래서 이 페이지는 각각 하나씩을
고정한다.

**패치.** §3이 서술하는 로봇 중심 높이 지도의 $3\times3$ 창. 셀 크기 $c=0.20$ m, 높이 단위는
미터, $x$는 동쪽, $y$는 북쪽이고 행은 북에서 남으로 적는다.

$$H=\begin{pmatrix}0.08&0.12&0.16\\0.06&0.10&0.14\\0.04&0.08&0.32\end{pmatrix}$$

아홉 셀 중 여덟은 평면 $h=0.10+0.20x+0.10y$ 위에 정확히 놓이고, 아홉 번째인 남동쪽 모서리만
$0.32$ m로 올라가 있다. 그러니 이 패치는 바위 하나가 얹힌 깨끗한 경사면이고, 아래에서 유도하는
모든 수는 경사면 아니면 바위다 — 마지막에 각 통과 가능성 항이 실제로 무엇을 재고 있었는지 말할
수 있는 이유가 그것이다.

**기계 둘.** §1의 첫 번째 귀결이 같은 패치가 로봇마다 다른 비용 지도를 갖는다는 것이기 때문이다.

| 한계 | **Q**, 사족 | **T**, 궤도 차량 |
|---|---:|---:|
| $\theta_{\max}$, 경사 | $25^\circ$ | $30^\circ$ |
| $h_{\max}$, 넘어설 수 있는 단차 | $0.15\,\mathrm{m}$ | $0.40\,\mathrm{m}$ |
| $\sigma_{\max}$, 거칠기 | $0.05\,\mathrm{m}$ | $0.10\,\mathrm{m}$ |

가중치는 둘 다 $(w_\theta,w_h,w_\sigma)=(0.4,0.4,0.2)$로 같다.

Q는 [[04-robotics/legged-locomotion|18. 레그드 로코모션]]의 고정 사족이고($12$ kg, 무게중심
$0.30$ m, 발은 $(\pm0.30,\pm0.15)$ m), 그 $\theta_{\max}$는 규정이 *아니다*. Q는 무게중심 투영이
$0.15$ m 반폭을 넘을 때 측면 발 한 쌍을 축으로 넘어가고 그 각도가
$\arctan(0.15/0.30)=26.6^\circ$이므로, $25^\circ$는 거기에 1.5도의 여유를 둔 값이다. $h_{\max}$와
$\sigma_{\max}$는 카탈로그 숫자로, 한 번 적고 과제에서만 바꾼다. T는 이 세 한계로만 고정되며,
대조를 위해 여기 있다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="고정된 3x3 높이 패치: 여덟 셀은 평면 위에, 모서리 한 셀만 올라가 있다">
  <defs><marker id="arTk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1" stroke-opacity="0.55">
    <rect x="170" y="54" width="64" height="44"/><rect x="234" y="54" width="64" height="44"/><rect x="298" y="54" width="64" height="44"/>
    <rect x="170" y="98" width="64" height="44"/><rect x="234" y="98" width="64" height="44"/><rect x="298" y="98" width="64" height="44"/>
    <rect x="170" y="142" width="64" height="44"/><rect x="234" y="142" width="64" height="44"/>
  </g>
  <g fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"><rect x="298" y="142" width="64" height="44"/></g>
  <g font-size="11.5" fill="currentColor" text-anchor="middle">
    <text x="202" y="82">0.08</text><text x="266" y="82">0.12</text><text x="330" y="82">0.16</text>
    <text x="202" y="126">0.06</text><text x="266" y="126">0.10</text><text x="330" y="126">0.14</text>
    <text x="202" y="170">0.04</text><text x="266" y="170">0.08</text><text x="330" y="170">0.32</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="202" y="46">x = &#8722;0.20</text><text x="266" y="46">0</text><text x="330" y="46">+0.20</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.8" text-anchor="end">
    <text x="163" y="80">y = +0.20</text><text x="163" y="124">0</text><text x="163" y="168">&#8722;0.20</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" marker-end="url(#arTk)">
    <line x1="382" y1="196" x2="422" y2="196"/><line x1="382" y1="196" x2="382" y2="164"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="426" y="200">+x 동쪽</text><text x="388" y="160">+y 북쪽</text>
    <text x="382" y="128">셀 0.20 m</text>
    <text x="382" y="76">높이 단위 m</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="218">여덟 셀은 h = 0.10 + 0.20x + 0.10y 위에 정확히 놓인다 &#8212; 깨끗한 12.6&#176; 경사면.</text>
    <text x="40" y="234">칠한 모서리만 0.32 m로 올렸다. 셀 하나가 적합 경사를 7.8&#176; 움직이고, 거칠기의 56%를</text>
    <text x="40" y="250">공급하며, 단차 항이 존재할 이유 전부다.</text>
  </g>
</svg>

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="축척대로 옆에서 본 가운데 행에서 최소제곱 선이 0.06, 0.10, 0.14를 지나는 중앙 차분 선보다 8.8도 더 가파르고, 그 옆 Q와 T의 경사·단차·거칠기를 각 로봇 자신의 한계로 나눈 막대 중 1의 관문을 넘는 것은 Q의 단차 막대 1.600 하나뿐이다">
  <g font-size="12" fill="currentColor" opacity="0.9">
    <text x="12" y="16">두 개의 경사</text><text x="296" y="16">판정</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.75">
    <text x="12" y="31">가운데 행을 남쪽에서 본 모습, 1:1 축척</text><text x="296" y="31">각 항을 그 로봇 자신의 한계로 나눈 값</text>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <line x1="34" y1="165" x2="238" y2="165"/>
    <line x1="34" y1="165" x2="34" y2="170"/><line x1="102" y1="165" x2="102" y2="170"/><line x1="170" y1="165" x2="170" y2="170"/><line x1="238" y1="165" x2="238" y2="170"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.4" stroke-dasharray="2 3"><line x1="204" y1="62.2" x2="204" y2="165"/></g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.4" stroke-dasharray="2 3"><line x1="68" y1="148.6" x2="68" y2="165"/><line x1="136" y1="135" x2="136" y2="165"/></g>
  <g stroke="currentColor" stroke-width="1.7" fill="none">
    <line x1="34" y1="151.4" x2="238" y2="110.6"/>
    <line x1="34" y1="160.8" x2="238" y2="86" stroke-dasharray="7 4"/>
  </g>
  <path d="M229.9 112.2 A142 142 0 0 0 224 91.2" stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.8"/>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="204" y1="117.4" x2="204" y2="98.5"/><line x1="200" y1="98.5" x2="208" y2="98.5"/>
  </g>
  <g fill="currentColor"><circle cx="68" cy="144.6" r="3.6"/><circle cx="136" cy="131" r="3.6"/><circle cx="204" cy="117.4" r="3.6"/></g>
  <rect x="199" y="51.2" width="10" height="10" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <g font-size="11" fill="currentColor">
    <text x="194" y="60.2" text-anchor="end">바위, 한 행 남쪽: 0.32</text>
    <text x="198" y="90.5" text-anchor="end">0.0556 m</text>
    <text x="243" y="102.3">8.8°</text>
    <text x="72" y="160">0.06</text>
    <text x="140" y="160">0.10</text>
    <text x="208" y="160">0.14</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="68" y="182">−0.20</text><text x="136" y="182">0</text><text x="204" y="182">+0.20</text>
  </g>
  <text x="243" y="182" font-size="11" fill="currentColor" opacity="0.8">x (m)</text>
  <g stroke="currentColor" stroke-width="1.7" fill="none">
    <line x1="12" y1="202" x2="34" y2="202"/><line x1="12" y1="219" x2="34" y2="219" stroke-dasharray="7 4"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="40" y="206">중앙 차분(점 셋을 지남): 11.3°</text><text x="40" y="223">최소제곱(아홉 셀 전부): 20.1°</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="5 3"><line x1="458" y1="50" x2="458" y2="184"/></g>
  <text x="458" y="46" font-size="11" fill="currentColor" text-anchor="middle">관문</text>
  <g font-size="11" fill="currentColor"><text x="296" y="60">Q (25°, 0.15 m, 0.05 m)</text><text x="552" y="60" text-anchor="end">관문 걸림</text></g>
  <rect x="362" y="66" width="78.5" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="75.8" text-anchor="end" opacity="0.85">경사</text><text x="436.5" y="75.8" text-anchor="end">0.818</text></g>
  <rect x="362" y="82" width="153.6" height="12" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="91.8" text-anchor="end" opacity="0.85">단차</text><text x="511.6" y="91.8" text-anchor="end">1.600</text></g>
  <rect x="362" y="98" width="95.4" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="107.8" text-anchor="end" opacity="0.85">거칠기</text><text x="453.4" y="107.8" text-anchor="end">0.994</text></g>
  <g font-size="11" fill="currentColor"><text x="296" y="127">T (30°, 0.40 m, 0.10 m)</text><text x="552" y="127" text-anchor="end">통과, C = 0.612</text></g>
  <rect x="362" y="133" width="65.4" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="142.8" text-anchor="end" opacity="0.85">경사</text><text x="423.4" y="142.8" text-anchor="end">0.681</text></g>
  <rect x="362" y="149" width="57.6" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="158.8" text-anchor="end" opacity="0.85">단차</text><text x="415.6" y="158.8" text-anchor="end">0.600</text></g>
  <rect x="362" y="165" width="47.7" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor"><text x="356" y="174.8" text-anchor="end" opacity="0.85">거칠기</text><text x="405.7" y="174.8" text-anchor="end">0.497</text></g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <line x1="362" y1="184" x2="520.4" y2="184"/><line x1="362" y1="184" x2="362" y2="188"/><line x1="410" y1="184" x2="410" y2="188"/><line x1="458" y1="184" x2="458" y2="188"/><line x1="506" y1="184" x2="506" y2="188"/>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="362" y="199">0</text><text x="410" y="199">0.5</text><text x="458" y="199">1</text><text x="506" y="199">1.5</text>
  </g>
  <text x="296" y="216" font-size="11" fill="currentColor" opacity="0.85">σ²의 셀별 몫</text>
  <rect x="296" y="222" width="142.2" height="15" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <rect x="438.2" y="222" width="113.8" height="15" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  <g font-size="11" fill="currentColor"><text x="301" y="233.5">바위 56%</text><text x="443.2" y="233.5">나머지 여덟 셀 44%</text></g>
  <text x="12" y="254" font-size="11" fill="currentColor" opacity="0.9">남북 기울기까지 넣은 전체 경사로는 경사면 12.6°, 적합 20.4°로 7.8° 차이다.</text>
</svg>

고정된 패치는 셀 $0.20$ m, 높이 단위 미터인 높이 지도의 $3\times3$ 창으로, 여덟 셀은 평면 $h=0.10+0.20x+0.10y$ 위에 정확히 놓인 깨끗한 $12.6^\circ$ 경사면이고 칠한 남동쪽 모서리가 $0.32$ m로 올라간 바위다. 그 셀 하나가 적합 경사를 $7.8^\circ$ 움직이고, 거칠기의 $56\%$를 공급하며, 단차 항이 존재할 이유 전부다. 패치 아래 그림에서, 가운데 행을 옆에서 보면 최소제곱 자취가 $0.06$, $0.10$, $0.14$를 지나는 중앙 차분 선보다 $8.8^\circ$ 더 가파르고(남북 기울기까지 넣으면 $7.8^\circ$), 각 항을 그 로봇 자신의 한계로 나눈 막대 중 $1$의 관문을 넘는 것은 Q의 단차 막대 $1.600$ 하나뿐이다. §1 뒤의 유도에 나오는 경사 둘, 단차, 거칠기, 그리고 Q와 T의 반대 판정이 모두 이 아홉 높이에서 나온다.

### 1. 이 분야를 재편한 발상

고전적 계획기는 점유 격자를 만들고, 점유된 셀을 장애물로 표시하고, 그것을 돌아간다. 그 로봇을
키 큰 풀밭에 놓으면 멈춘다. 풀이 라이다 반사를 만들고, 라이다 반사는 곧 장애물이기 때문이다.

그에 대한 교정이 이 페이지 전체의 전제다:

> **Traversability는 기하학적 술어가 아니다. 로봇마다 다르고 속도에 조건부이며, 로봇 자신이
> 거기를 주행한 경험에서 학습되는 어포던스다.**

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="같은 지형 세 곳을 점유 격자와 학습된 어포던스 두 방식으로 읽은 것">
  <g font-size="10.5" fill="currentColor" opacity="0.8">
    <text x="40" y="14">같은 장면, 세 지형</text>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="32" font-size="11" text-anchor="middle">키 큰 풀</text>
    <text x="280" y="32" font-size="11" text-anchor="middle">매끈한 콘크리트</text>
    <text x="445" y="32" font-size="11" text-anchor="middle">잔해 더미</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="52">기하가 말하는 것 &#8212; 점유 격자</text>
  </g>
  <g>
    <rect x="40" y="58" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="205" y="58" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="370" y="58" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  </g>
  <g fill="currentColor">
    <text x="115" y="81" font-size="11" text-anchor="middle">장애물</text>
    <text x="280" y="81" font-size="11" text-anchor="middle">자유 공간</text>
    <text x="445" y="81" font-size="11" text-anchor="middle">장애물</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="122">주행 경험이 말하는 것 &#8212; 이 로봇, 이 속도</text>
  </g>
  <g>
    <rect x="40" y="128" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="205" y="128" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
    <rect x="370" y="128" width="150" height="36" rx="3" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  </g>
  <g fill="currentColor">
    <text x="115" y="151" font-size="11" text-anchor="middle">통과 가능</text>
    <text x="280" y="151" font-size="11" text-anchor="middle">선호</text>
    <text x="445" y="151" font-size="11" text-anchor="middle">장애물</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.75" stroke-dasharray="4 3">
    <path d="M32,76 C14,88 14,116 32,128"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="196" y="106" text-anchor="end">이 칸이 뒤집힌다</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="40" y="178">&#8220;라이다 반사는 곧 장애물&#8221;이라는 규칙이 풀밭에서 로봇을 세운다.</text>
    <text x="40" y="193">결과에서 배운 비용은 그 칸을 뒤집는다. 그리고 아래 줄은 로봇이나 명령 속도가</text>
    <text x="40" y="208">바뀌면 함께 바뀐다 &#8212; 위 줄은 결코 바뀌지 않는다.</text>
  </g>
</svg>

BADGR가 그 정본 진술이다. **자기지도 off-policy 실세계 데이터**로 예측 모델을 학습한다 —
시뮬레이터도, 사람의 라벨도 없이 — 충돌이나 덜컹거림 같은 사건을 IMU·LIDAR·바퀴 오도메트리로 자동 라벨링하고,
모델 입력은 RGB 영상과 계획된 행동뿐이다(GPS는 목표를 준다). 결과는 풀을 *통과해* 주행하고 매끈한 콘크리트를 선호하는 로봇이며, 두 선호를
기하가 아니라 결과에서 배운 것이다.

교과서가 대비시켜 주지 않는 귀결 셋:

- **같은 장면이 로봇마다 다른 costmap을 갖는다.** 12톤 궤도 차량과 4족 로봇은 잔해 더미에 대해
  의견이 다르고, 둘 다 틀리지 않았다.
- **비용이 명령 속도에 의존한다.** 1 m/s에서 괜찮은 지형이 10 m/s에서는 괜찮지 않으므로, 속도를
  조건으로 하는 costmap은 정적인 것과 다른 대상이다.
- **계획기가 통과 불가라고 부르는 지형이 흔히 통과 가능하다.** Verti-Wheelers 계열이 이것을 자기
  주장으로 삼는다: ICRA 2024 논문이 부르는 "불규칙한 바위와 쓰러진 나무"를 *하드웨어를
  **거의 개조하지 않은** 평범한 바퀴 로봇이* 넘는다 — 논문 자신의 유보다. 바위 노두와 "SE(3)의
  3D 6자유도 차량-지형 동역학 모델"은 같은 그룹의 자매 논문([arXiv:2306.11611](https://arxiv.org/abs/2306.11611))의 것이지 이 논문의 것이 아니다. Traversability를
  분할(segmentation) 문제가 아니라 **모델링** 문제로 재프레이밍한다.

### 패치로 한 번 끝까지 · Worked on the patch

위의 세 귀결은 주장이다. 여기서는 고정된 패치 위의 산수로 만든다. 과제는 바위만 바꾼 같은 산수다.

**1. 서로 어긋나는 두 가지 경사 계산.** 한 셀의 **경사**는 지형의 국소 법선과 수직 사이의
각이다 — 같은 말로, 그 자리에서 높이장 기울기 크기의 아크탄젠트다. $[0^\circ,90^\circ)$의 각이고,
원본 셀이 아니라 *적합된* 곡면의 성질이며, 문제가 시작되는 곳이 바로 거기다. 적합은 선택이기
때문이다.

*가운데 셀의 중앙 차분.* 가운데 셀의 동서·남북 이웃을 쓴다. 아홉 중 넷만 쓰는 셈이다.

$$g_x=\frac{0.14-0.06}{2c}=\frac{0.08}{0.40}=0.20,\qquad g_y=\frac{0.12-0.08}{2c}=\frac{0.04}{0.40}=0.10,\qquad \theta=\arctan\sqrt{0.20^2+0.10^2}=\arctan 0.2236=12.60^\circ$$

*아홉 개 전부에 대한 최소제곱.* $h=a+bx+c_0y$를 적합한다. $c$는 이미 셀 크기라서 이 계수는 $c_0$ 기호로 쓴다. 표본점 아홉 개가 중심화되어 있고
대칭이라 $\sum x_i=\sum y_i=\sum x_iy_i=0$이고, 세 추정이 한 줄짜리 몫으로 분리된다.

$$b=\frac{\sum x_ih_i}{\sum x_i^2}=\frac{0.088}{0.24}=0.3667,\qquad c_0=\frac{\sum y_ih_i}{\sum y_i^2}=\frac{-0.016}{0.24}=-0.0667,\qquad a=\bar h=\frac{1.10}{9}=0.1222$$

합이 분리되면 각 계수가 자기 축을 따르는 높이들의 가중 평균일 뿐이기 때문이다. 조각들은
$\sum x_i^2=\sum y_i^2=6(0.20)^2=0.24$,
$\sum x_ih_i=0.2(0.16+0.14+0.32)-0.2(0.08+0.06+0.04)=0.088$,
$\sum y_ih_i=0.2(0.36)-0.2(0.44)=-0.016$이다. 경사는 그러면
$\arctan\sqrt{0.3667^2+0.0667^2}=\arctan 0.3727=20.44^\circ$다.

두 추정기가 같은 아홉 개의 수에 대해 $7.83^\circ$ 어긋나고, 남북 기울기는 부호까지 $+0.10$에서
$-0.0667$로 바뀐다. 어느 쪽도 틀리지 않았다. 중앙 차분은 모서리 셀을 건드린 적이 없으니 경사면을
보고하고, 평면 적합은 그 모서리를 다른 셀과 똑같이 무겁게 세므로 바위에 닿고, 그래서 기울어진
타협을 보고한다. **"경사 임계 $25^\circ$"라고 적은 논문은 이 둘 중 무엇에 임계를 걸었는지 아직 말하지
않은 것이고**, 이 패치에서 그 누락의 값은 거의 8도다.

**2. 단차 높이.** 한 창의 **단차 높이**는 그 안에서 4-연결 이웃 셀 사이 높이 차의 절댓값 중
최대다. 길이이고, 셀이 아니라 쌍 위에 정의되며, 발이나 궤도가 무언가를 *올라갈* 수 있는지가 아니라
*넘어설* 수 있는지를 묻는 항이다. 이 패치에서 경사면 쌍은 동서로 $0.20\times c=0.04$ m, 남북으로
$0.10\times c=0.02$ m씩만 다르므로 최댓값은 바위에서만 나올 수 있다.

$$\Delta h=\max_{i\sim j}\lvert h_i-h_j\rvert=\max(0.32-0.08,\ 0.32-0.14)=0.24\ \mathrm{m}$$

반례: 단차 높이는 창의 범위 $\max h-\min h=0.28$ m가 *아니다*. 그 척도는 경사면 자신의 상승을
단차 항에 물리는데, 경사면은 로봇이 올라가는 것이지 넘어서는 것이 아니다. 둘을 혼동하는 것이
기하 기반 비용 지도가 결국 언덕을 거부하게 되는 가장 흔한 경로다.

**3. 거칠기.** 한 창의 **거칠기**는 적합 평면에 대한 셀 높이 잔차의 제곱평균제곱근이다. 길이이고,
적합에 상대적으로만 정의되며, 경사 항이 이미 설명해 버린 것을 뺀 나머지를 잰다.
$\hat h=0.1222+0.3667x-0.0667y$를 쓰면 아홉 잔차는 미터 단위로 다음과 같다.

$$\begin{pmatrix}+0.0444&+0.0111&-0.0222\\+0.0111&-0.0222&-0.0556\\-0.0222&-0.0556&+0.1111\end{pmatrix},\qquad \sigma=\sqrt{\tfrac{1}{9}\textstyle\sum r_i^2}=\sqrt{\tfrac{0.02222}{9}}=0.0497\ \mathrm{m}$$

바위 자신의 잔차는 $0.32-0.2089=0.1111$ m이므로 그 제곱은 전체 $0.02222$ 중 $0.01235$다.
**거칠기의 56%가 아홉 셀 중 하나에서 온다.** 반례: 거칠기는 난이도의 대용이 아니다. 완벽하게
매끄러운 $40^\circ$ 슬래브는 $\sigma=0$이고 그래도 사족을 굴린다. 경사와 거칠기가 "지형 나쁨"
하나가 아니라 별개의 항인 이유가 정확히 그것이다.

**4. 비용과 관문.** 여기서 **통과 가능성 비용**은 *이름이 붙은 로봇*에 대해 정의된 셀 위의
스칼라장이고, 서로 다르게 행동하는 두 부분으로 되어 있다. 셀을 아예 지도 밖으로 빼는 술어인 단단한
**관문**, 그리고 그것을 통과한 셀들의 순위를 매기는 $[0,1]$의 부드러운 **비용**이다. 정의 조건이
셋이다. 각 원시 측정값을 그 로봇 자신의 한계로 나누어 항들을 무차원이자 비교 가능하게 만든다.
가중치는 음이 아니고 합이 1이라 살아남은 비용이 $[0,1]$에 놓인다. 그리고 관문은 큰 수가 아니라
별개의 술어다.

$$C=w_\theta\frac{\theta}{\theta_{\max}}+w_h\frac{\Delta h}{h_{\max}}+w_\sigma\frac{\sigma}{\sigma_{\max}},\qquad \max\Big(\frac{\theta}{\theta_{\max}},\frac{\Delta h}{h_{\max}},\frac{\sigma}{\sigma_{\max}}\Big)>1\ \text{이면 통과 불가}$$

관문이 큰 유한 비용이 아니라 술어여야 하는 것은, 합을 최소화하는 계획기가 200 m를 아끼려고
$10^4$쯤은 기꺼이 치르기 때문이고, 로봇을 굴릴 셀은 어떤 값에도 살 수 있어서는 안 되기 때문이다.
기계마다 세 측정값을 대입하면 이렇다.

| 항 | 원시값 | **Q** ($25^\circ$, $0.15$ m, $0.05$ m) | **T** ($30^\circ$, $0.40$ m, $0.10$ m) |
|---|---:|---:|---:|
| 경사 | $20.44^\circ$ | $0.818$ | $0.681$ |
| 단차 | $0.24\,\mathrm{m}$ | $\mathbf{1.600}$ | $0.600$ |
| 거칠기 | $0.0497\,\mathrm{m}$ | $0.994$ | $0.497$ |
| 관문 | | **걸린다** | 통과 |
| $C$ | | $1.166$ | $0.612$ |

**판정.** Q에게는 관문이 걸려 셀이 통과 불가다. $C=1.166$은 비교용으로만 적었다. 관문에 걸린 셀의
비용은 쓸 수 없기 때문이다. T에게는 아무것도 걸리지 않아 $C=0.612$의 평범한 중간 지형이다. 패치
하나, 수 아홉 개, 정반대 판정 — 손짓을 걷어낸 §1의 첫 번째 귀결이다.

표에서 읽을 것이 둘이다. Q에게 판정을 내리는 항은 **경사가 아니라 단차 높이**이고, 그것도 아슬아슬하지
않다. $0.818$에 대해 $1.60$이다. 경사 임계만 보고하는 논문은 애초에 결정권이 없던 항을 보고한
것이다. 그리고 거칠기 항이 $0.994$에 앉아 있다. 바위를 1 cm만 더, $0.33$ m로 올리면 $\sigma$가
$0.0522$ m가 되어 그 항이 *혼자서* 관문을 걸어 버린다. 아무도 보고 있지 않은 이유로 거부되기까지
1 cm 남은 셀도 있을 수 있다는 뜻이다.

**5. P2가 판정에 하는 일.** [[04-robotics/legged-locomotion|18. 레그드 로코모션]]이 계산하듯 P2를
얹으면 Q의 무게중심이 $0.30$ m에서 $0.371$ m로 올라가므로 측면 전복 각이 $26.6^\circ$에서
$\arctan(0.15/0.371)=22.0^\circ$로 내려가고, 실린 로봇의 정직한 $\theta_{\max}$는 $25^\circ$가
아니라 $22^\circ$다. 경사 항은 $20.44/22=0.929$가 된다. 맨몸일 때 $0.818$로 편안하던 지형에서,
이제 자기 관문의 $7\%$ 안쪽이다. 관문은 여전히 단차에서 걸리므로 여기서 판정이 바뀌지는 않지만,
지면은 하나도 바뀌지 않은 채 경사 항 자신의 여유가 대부분 사라졌다. §1의 주장을
"통과 가능성은 로봇에 특정적이다"에서 **로봇 *구성*에 특정적이다**로 날카롭게 하는 것이고,
짐을 싣지 않은 탐사 주행에서 만든 비용 지도가 짐을 실은 복귀 주행에 넘어가지 않는 구체적인
이유다.

### 2. 지도 신호는 어디서 오는가

여기의 모든 방법이 무엇을 라벨로 쓰는가로 정의되고, 그것이 쓸모 있는 축이다.

| 지도 신호의 출처 | 뜻 | 대표 |
|---|---|---|
| **온보드 사건 검출** | 충돌과 덜컹거림을 센서로 자동 라벨링 | BADGR |
| **고유수용감각적 결과** | IMU와 충격 피드백 — 문자 그대로 거기를 달린 느낌 | *How Does It Feel?* |
| **속도 추종** | 로봇이 명령한 속도를 달성했는가? | Wild Visual Navigation |
| **예측된 고유수용감각** | 차량이 겪게 *될* 경험을 기하로부터 예측 | ScaTE |
| **기존 스택** | 느린 고전 파이프라인을 빠른 학습 모델로 증류 | RoadRunner |

**Wild Visual Navigation**이 현재 분야가 조직되어 있는 시스템이다. 온라인으로, 비전만으로, [[01-canonical-papers/notes/2-computer-vision/dino|DINO]]
특징(레이블 없이 학습한 범용 이미지 특징) 위에서, 로봇 자신의 속도 추종을 지도 신호 삼아, **학습과 추론을 ANYmal 온보드에서 동시에**
돌린다 — 그리고 주장을 신중하게 제한한다: 짧은 사람 시연으로부터 *5분 미만의 현장 학습*, 그다음
1.4 km의 오솔길 추종과 키 큰 풀.

**How Does It Feel?** 은 비전을 고유수용감각 IMU·충격 피드백과 짝짓고 costmap을 명령 속도에
조건화해, 400 m–3,150 m 코스에서 점유 기반 기준선 대비 **개입 최대 57% 감소**를 보고한다.

**SALON**이 같은 주장의 가장 날카로운 현재 진술이다: 낯선 지형을 능동적으로 피하면서 **비용과
속도**를 함께 담은 지도를 만드는 온라인 적응. 실제 데이터 *수 초* 만에 킬로미터 규모 경로를
주장하며, "100~1000배 많은 데이터"를 필요로 하는 방법들과 대등하다고 말한다.

> [!important] 주장의 분기 — 논문마다 이것부터 확인하라
> 논문들은 갈리지만 처음 읽을 때 보이는 방식으로는 아니다 — 가정하지 말고 초록을 각각 확인하라.
>
> | 논문 | 적응 주장 | 일반화 주장 |
> |---|---|---|
> | **WVN** | 현장 적응, 시연으로부터 5분 | 있음 — "어떤 지상 로봇으로도 일반화될 수 있다" |
> | ***How Does It Feel?*** | **없음** — 자기지도가 오프라인이고 고유수용 피드백에서 온다 | — |
> | **SALON** | "수 초 안에" | 있음 — "상당히 다른 로봇과 다른 환경에서의 유망한 결과" |
> | **V-STRONG** | — (순수한 일반화 사례) | zero-shot·few-shot에서 "새 환경으로의 일반화에서 전례 없는 성능" |
>
> 적응 주장과 일반화 주장은 완전히 다른 증거를 요구하므로, traversability
> 논문을 읽을 때 가장 먼저 확정할 것은 어느 쪽을 주장하는가이고, 초록이 늘 분명히 밝혀 주지는
> 않는다.

### 3. 기하학적 쪽이 사라진 것은 아니다

학습 위주로만 읽으면 놓치는 것 둘.

**밑에 깔린 고도 지도.** 거의 모든 레그드 내비게이션 논문이, 자세 추정 드리프트와 센서 불확실성을
**셀별 분산**으로 전파하는(각 셀의 높이는 센서가 그 셀을 볼 때 *있다고 믿은* 위치로부터 계산되므로, 그 믿음의 오차가 곧 높이의 오차가 된다) 로봇 중심 2.5D 고도 지도를 가정한다 — Fankhauser, Bloesch, Hutter의
정식화이며 `elevation_mapping` ROS 패키지로 배포된다. 학습된 traversability는 대개 이것을 *대신*
하는 것이 아니라 이것 *위에서* 돈다.

**위험 인지 기하 계획.** STEP이 그 균형추다: 불확실성 인지 traversability 평가, **Conditional
Value-at-Risk(CVaR)를 통한 꼬리 위험 평가**, 그리고 순차 이차 계획법(SQP: 반복점마다 이차 계획 근사를 푼다 — [[02-foundations/optimization|4. 최적화 §4]])으로 푸는 위험 제약
기구·동역학 MPC. 학습 논문이 아니고 일반화를 주장하지 않는다. [[04-robotics/mpc|MPC]]의 내용에
곧바로 연결되며, DARPA SubT에 나간 NeBula 스택의 traversability 모듈이다.

CVaR은 세부가 아니라 모델링 선택으로 알아 둘 가치가 있다: *평균* 결과를 최적화하는 것과 *최악
10분위*를 최적화하는 것은 다른 계획을 낳고, 실패가 지연이 아니라 전복인 지형에서는 후자가 옳은
목적함수다.

> [!example] 계산 예제 · Worked example
> **기하학적 쪽이 원거리에서 바닥나는 이유.** 높이 1.8 m에 수직 간격 0.4°인 64빔 라이다는
> 평지 위 연속한 링을 $r = h/\tan\theta$에 놓는다. $\theta = 5.15°$와 $5.55°$인 두 빔은
> $1.8/\tan 5.15° = 20.0$ m와 $1.8/\tan 5.55° = 18.5$ m에 떨어진다 — 링 간격 **1.4 m**. 같은
> 두 빔이 $\theta = 10.2°$와 $10.6°$일 때는 10.00 m와 9.62 m, 즉 **0.39 m**다.
>
> 그러므로 길이 0.3 m의 평평한 위험 — 바퀴 자국이나 구멍 — 은 10 m에서 링 하나에 겨우 걸치고 20 m에서는 대개 **하나도** 걸치지
> 않는다. 링 간격은 약 9 m부터 이미 0.3 m를 넘는다. (높이 0.3 m인 바위라면 20 m에서도 앞면에 반사점이 두 개쯤 찍힌다: 검출은 되지만 특성을 파악할 만큼은 아니다.) 그곳의 기하가 잡음이 많은 것이 아니라, 그곳에는 기하가 거의 없다.
>
> **여기서 얻는 독법.** 5 m/s로 달리며 반응과 제동에 4초를 거의 전속으로 쓰는 차량은 약 20 m의 판정된 지형이
> 필요한데(4초 동안 균일하게 감속해 멈춘다면 10 m), 그 거리는 링 간격이 위험 크기를 넘어서는 지점을 한참 지난다. 이 분야가 영상 기반 학습
> traversability로 옮겨 간 구조적 이유가 이것이다. 학습이 바위를 더 잘 분류해서가 아니라,
> *결정을 내려야 하는 거리에서 아직 분해능이 남아 있는 신호가 겉모습뿐*이기 때문이다. 라이다
> 기반 traversability를 보고하는 논문이라면, 최고 속도와 전방 판정 거리 두 숫자가 그 논문이
> 이 영역에 들어와 보기는 했는지 알려 준다.

### 4. 필드 프로그램이 확립한 것

**DARPA SubT**(2018~2021)가 비정형 환경 자율성에서 가장 큰 경험적 사건이다. Team CERBERUS가
**이종 레그드+공중 시스템의 시스템** — ANYmal C 4족 넷을 중추로 — 으로, 통신과 GNSS가 거부된
조건에서 견고한 다중 모달 SLAM과 함께 시스템 부문을 우승했다. 그 결과가 어떤 단일 논문보다도
"필드의 레그드 로봇"을 실연에서 공학적 결과로 바꿔 놓았다. 발표된 다른 완결 스택은 **NeBula**이고,
그 조직 원리는 **믿음 공간(belief-space)의 불확실성 인지 모듈형 자율성**이다: 점 추정이 아니라
분포 위에서 추론하고 결정한다.

**DARPA RACER**(2021 → 2026년 1월 완료 발표)는 같은 질문을 속도로 가져갔다. 명시된 목표는 센서
성능·기계적 제약·안전만이 제한하는 오프로드 주행이었고 최소 기준선이 사람 운전자와의 대등함이었다.
스택은 **GNSS 없이, 사전 지도 없이** 돌았고, 드라이브 바이 와이어 Polaris RZR과 약 12톤 궤도
플랫폼 위에서였다. DARPA는 **인식 아키텍처**를 대표 성과로 지목하며, 새 환경에 대한 재학습이 몇
주에서 하루로 줄었다고 밝힌다.

> [!warning] 이 분야의 인용 함정 셋
> - **DARPA는 RACER의 속도·거리 수치를 발표한다 — 그것을 쓰고 darpa.mil을 인용하라.**
>   2023년 발표는 약 4~11마일 무인 주행 55회 이상, 시속 약 25마일, 코스에서 24.6시간 동안
>   246마일을 보고한다. 2024년 발표는 3~10마일 코스 30회 이상, 무인 자율 150마일 이상,
>   **시속 최대 30마일**을 보고한다. (이 페이지의 이전 판은 정반대로 적고 최고 속도를 인용하지
>   말라고 했다. 그것이 틀렸다.) 논문 수준 수치는 대체재가 아니라 보완재다: RoadRunner는
>   Polaris RZR에서 **15 m/s**까지를 진술하고, 20 m/s는 측정된 주행이 아니라 예측 주기에 대한
>   *설계* 진술이다.
> - **RACER는 *Robotic Autonomy in Complex Environments with Resiliency*의 약자**이지 "Rapid
>   Autonomy"가 아니다. 그리고 **이름 충돌**이 있다: "RACER: Epistemic Risk-Sensitive RL"이라는
>   별개 논문은 1/10 스케일 랠리카 방법으로 이 프로그램과 무관하다.
> - **CODa는 도심 캠퍼스 데이터셋**이지 오프로드가 아니다. 그렇게 인용되는 일이 있지만 아니다.

### 5. 데이터셋과, 각각이 실제로 확립한 것

| 데이터셋 | 확립한 것 |
|---|---|
| **RUGD** (IROS 2019) | 오프로드 **의미 분할**을 측정 가능한 과제로 만들었다 — 이미지만 |
| **RELLIS-3D** (ICRA 2021) | **LiDAR**를 대화에 끌어들였다. 진단적 발견은 **도심 분할용으로 설계된 모델이 여기서 실패한다**는 것 |
| **TartanDrive** (ICRA 2022) | 7개 모달리티에 걸친 약 20만 오프로드 상호작용 — 오프로드 학습을 분할이 아니라 **동역학** 중심으로 재편 |
| **GOOSE** (ICRA 2024) | 라벨된 이미지+포인트 클라우드 쌍 1만 개, 그리고 진짜 기여인 **공개된 온톨로지** — 데이터셋을 가로지르는 오프로드 라벨링을 비교 가능하게 만들었다 |
| **GOOSE-Ex** (ICRA 2025) | **로봇 굴착기**와 4족에서 5,000 프레임을 추가, 교차 embodiment용 |

이 위키의 각도에서 눈여겨볼 것은 GOOSE-Ex다: 건설 기계를 포함한 오프로드 인식 데이터셋이,
이 페이지와 [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] 사이의
가장 가까운 기존 다리다.

### 6. Traversability 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 적응인가 일반화인가? | 요구되는 증거가 다르고 분야의 의견이 갈린다 |
| 라벨을 무엇이 공급했는가? | 지도 신호의 출처가 곧 방법이다 |
| Costmap이 속도에 조건화되어 있는가? | 조건화되지 않은 costmap은 어떤 속도에서 틀리다 |
| 어느 로봇이며, 그 지도가 이전되겠는가? | Traversability는 구조적으로 로봇마다 다르다 |
| 밑에 기하 층이 있는가? | 대부분의 학습 방법은 언급하지 않는 고도 지도 위에 앉아 있다 |
| 성공률이 아니라 거리와 개입 횟수 | 필드 자율성의 정직한 지표는 킬로미터당 개입 수다 |

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 고정된 패치에서 경사·단차 높이·거칠기를 계산하고, Q에게 관문을 거는 항이 무엇인지 말한다.
- [ ] 똑같은 아홉 개의 수가 왜 Q에게는 통과 불가이고 T에게는 평범한지 말한다.
- [ ] 키 큰 풀이 왜 점유 지도의 정본 반례인지 말한다.
- [ ] 지도 신호의 출처 셋과 각각의 논문을 댄다.
- [ ] 적응 대 일반화의 분기를 설명하고 왜 중요한지 말한다.
- [ ] CVaR이 평균 최적화에 비해 무엇을 사는지 말한다.
- [ ] SubT와 RACER가 각각 확립한 것을, DARPA가 발표한 속도·거리 수치를 인용하며 말한다.

> [!tip] 더 깊이 · Going deeper
> 교과서도 없고 버텨 낸 서베이도 없으니, 대체물은 세 논문을 하나의 논증으로 읽는 것이다. 먼저 BADGR(*RA-L* 2021) — 재프레이밍을 가장 헐벗은 형태로 진술하기 때문이다: 로봇이 직접 달려 보며 자기 지형에 라벨을 붙인다. 그다음 "How Does It Feel?"(ICRA 2023), 같은 발상을 고유수용 감각으로 비용 지도까지 밀고 간다. 그다음 Wild Visual Navigation — 우선권은 RSS 2023으로 인용하되 전체 시스템은 2025년 *Autonomous Robots* 판으로 읽어라. 이 셋을 지나면 §4의 필드 프로그램 기록이 이름의 나열이 아니라 증거로 읽힌다.

### 스스로 점검

1. 어떤 논문이 한 로봇에서 학습한 traversability 모델을 재학습 없이 다른 로봇에 배치했다고
   보고한다. 무엇을 먼저 확인해야 하는가?
2. Costmap이 왜 명령 속도를 알아야 하는가?
3. 학습 기반 traversability 시스템이 2 km 코스에서 95% 성공을 보고한다. 더 정보가 되는 숫자는?
4. 누군가 소형 자동차의 강화학습 방법에 "RACER"를 인용한다. 무슨 일이 일어난 것인가?
5. 프로젝트가 거친 지반 위의 굴착기를 다룬다. 이 페이지에서 가장 가까운 출발점은 무엇이고,
   거기에 여전히 없는 것은?
6. 어떤 비용 지도가 $0.20$ m 격자에서 중앙 차분으로 경사를 계산하고 $25^\circ$에 임계를 건다.
   구조적으로 놓치는 위험의 부류는 무엇인가?

> [!tip]- 정답 · Answers
> 1. 그 논문이 *적응*을 주장하는지 *일반화*를 주장하는지, 그리고 두 번째 로봇의 동역학이 첫 로봇이 학습한 결과가 유효할 만큼 가까운지. Traversability는 구조적으로 로봇마다 다르다 — 궤도 차량이 쉽게 넘는 잔해 더미가 4족을 굴릴 수 있다 — 그러니 로봇 간 이전은 시각 특징이 일반적이라는 데서 공짜로 따라 나오는 것이 아니라 자기 증거가 필요한 강한 주장이다.
> 2. Traversability가 지형이 무엇인가만이 아니라 로봇이 무엇을 하려 하는가의 함수이기 때문이다. 1 m/s에서 편안한 골이 10 m/s에서는 차량을 튀어 오르게 할 수 있으므로, 단일 정적 비용은 속도 범위의 한쪽 끝에서 틀린다. 명령 속도에 조건화하는 것이 지도 하나로 속도 포락선 전체를 감당하게 만들고, *How Does It Feel?* 가 비용을 속도에 조건화하고 SALON이 비용 지도와 함께 속도 지도를 예측하는 이유다.
> 3. **킬로미터당 개입 횟수**, 그리고 거리 그 자체. 고정 코스의 성공률은 "깨끗하게 주행했다"와 "조작자가 세 번 구해 준 뒤 주행했다"를 뭉뚱그리고, 배치 가능성을 추적하는 숫자는 개입 횟수다. *How Does It Feel?* 의 대표 수치가 성공률이 아니라 정확히 이것 — 개입 **최대** 57% 감소 — 이다.
> 4. 이름 충돌이다. DARPA 프로그램은 *Robotic Autonomy in Complex Environments with Resiliency*이고, 별개의 무관한 논문이 1/10 스케일 랠리카의 epistemic risk-sensitive RL 방법에 RACER를 쓴다. 둘 다 실재하며, 하나를 다른 하나로 인용하는 것이 흔한 오류다.
> 5. **GOOSE-Ex.** 여기서 로봇 굴착기를 담은 유일한 오프로드 인식 데이터셋이고 교차 embodiment 일반화를 위해 만들어졌기 때문이다. 여전히 없는 것은 기계 자신의 상태 전부다 — 액추에이터·관절·유압·힘 채널이 하나도 공개되지 않으며, 이는 [[06-research-practice/simulators-benchmarks-datasets|7. §8]]이 건설 데이터셋 전반에 대해 기록한 바로 그 공백이다.
> 6. 기울기가 아니라 쌍이나 대각선의 높이 차로 나타나는 것 전부다. 모서리 셀 위의 바위, 연석, 스텐실의 팔 사이로 빠지는 좁은 도랑. 고정된 패치가 최소 사례다 — 모서리 바위가 최소제곱 경사를 $7.83^\circ$ 움직이고 단차 높이를 $0.24$ m로 밀어 올리면서도 중앙 차분은 정확히 $12.60^\circ$에 남겨 둔다. 해법은 더 정교한 경사 추정기가 아니라 별개의 단차 항이다. 셀 쌍 위에 정의된 양을 적합 곡면의 기울기가 표현할 방법은 없기 때문이다.

**Worked: 과제가 묻는 세 가지 읽기.** 라이다에서 점유로 찍히는 키 큰 풀이 대표 반례다. BADGR이나 *How Does It Feel?*은 점유 라벨을 결과(consequence)로 바꾼다. 킬로미터당 개입 횟수가 성공률 95%보다 나은 지표다. 경사면의 굴삭기가 목적함수로 삼아야 하는 것은 평균이 아니라 CVaR이다.

### 과제 · Problem set

Tier B. 이 페이지의 패치, **Q**, **T**, 그리고 [[02-foundations/lab-plants|0.6]]의 **P2**를 쓴다.
손 계산만 한다. 수 아홉 개에 시뮬레이터는 필요 없다.

**바꿀 손잡이.** 바위가 더 작다. 남동쪽 셀이 $0.32$ m가 아니라 $0.20$ m다. 바위가 아니라 연석이다.
나머지 — 셀 크기, 다른 여덟 높이, 두 기계의 한계, 가중치 — 는 그대로다.

1. **그려라.** 새 패치에 대해 위의 그림 세 칸을 모두 그린다. 왼쪽: 모서리를 고친 격자. 가운데: 가운데 행의
   측면도에 두 적합 선을 그리되 — 이것이 다시 그리는 이유인데 — 중앙 차분 선은 아무것도 계산하기
   *전에* 긋고, 그것이 움직일지에 대한 예측을 함께 적는다. 오른쪽: 관문 선에 대한 정규화 막대 셋을
   이번에는 세 벌 그린다. Q, P2를 실은 Q, 그리고 T.
2. **유도하라.** (a) 가운데 셀의 중앙 차분 경사. (b) 최소제곱 평면의 $a$, $b$, $c_0$ 및 그 경사를
   분리된 몫으로 구한다. (c) 단차 높이와 거칠기. (d) Q, P2를 실은 Q(18번 페이지가 실린 로봇에
   대해 유도하는 $\theta_{\max}$를 쓴다), 그리고 T에 대한 관문과 $C$. 셋의 순위를 매긴다.
3. **해석하라.** 두 경사 추정 중 하나는 강의의 패치와 이 패치 사이에서 전혀 움직이지 않았는데 Q의
   판정은 뒤집혔다. 어느 쪽인지, 정확히 왜인지, 그리고 그것이 $0.20$ m 격자에서 중앙 차분으로
   경사를 계산하는 비용 지도 파이프라인에 대해 무엇을 뜻하는지 말하라. 그다음: 이 산수를 하나도
   하지 않고 *두* 패치 모두에서 옳은 답에 도달했을 §2의 지도 신호 출처를 대고, 그것이 기하에는
   필요 없는 무엇을 필요로 하는지 정확히 진술하라.
4. **읽어라.** §1~§6만 써서 세 가지 주장을 다룬다. (a) 라이다 occupancy 지도가 키 큰 풀을 점유로
   표시한다. 이것이 정본 반례인 이유와, occupancy 레이블을 대체하는 지도 신호의 출처(논문 이름)는?
   (b) 학습 시스템이 2 km 코스에서 95% 성공을 보고한다. 더 정보가 되는 숫자와, 95%가 뭉뚱그리는
   주행 둘은? (c) 플래너가 costmap에서 기댓값을 최소화한다. 평균 대신 CVaR가 사는 것과, 경사면
   굴착기에서 평균이 *틀린* 목적인 때는?

> [!note]- 그리는 법 · How to draw it
> - **왼쪽, 패치**: 셀 안에 아홉 개의 높이를 적은 $3\times3$ 격자를 그리고, 한 변에 셀 크기 $c=0.20$ m를 표시하고, $+x$ 동쪽과 $+y$ 북쪽 화살표를 넣는다.
> - **남동쪽 셀을 칠한다**: 그것이 바위이고, 이어지는 모든 것이 그 셀에 달려 있다.
> - **가운데, 가운데 행을 따라 옆에서 본 그림**: 높이 $0.06$, $0.10$, $0.14$를 지면 축 위의 점 셋으로 찍고 그 점들을 지나는 선을 긋는다. 그것이 중앙 차분이다.
> - **같은 단면을 지나는 최소제곱 평면의 자취는 더 가파른 두 번째 선으로 긋고**, 바위가 있는 열에서 수직 간격을 표시한다. 두 선이 이 단면에서 어긋나는 각이 이 그림이다(§1 뒤의 유도에서는 $8.8^\circ$).
> - **오른쪽, 판정**: 정규화된 항 $\theta/\theta_{\max}$, $\Delta h/h_{\max}$, $\sigma/\sigma_{\max}$ 하나에 하나씩 수평 막대 셋을 그리고, $1$에 관문을 뜻하는 수직선을 긋는다.
> - **기계마다 막대 한 벌씩, 모두 같은 축 위에**: 똑같은 세 측정값이 기계마다 선의 어느 쪽에 놓이는지가 요점이다. §1 뒤의 유도에서는 Q의 단차 막대만 선을 넘고, T의 막대는 모두 선에 못 미친다.

> [!tip]- 정답 · Solutions
> 1. 가운데 칸의 중앙 차분 선은 그대로다. 그 추정기는 가운데 셀의 변으로 인접한 이웃 넷만 읽는데 모서리는 그중 하나가 아니기 때문이다. 오른쪽 칸: 이제 Q의 막대는 셋 다 관문 왼쪽이고, P2를 실은 Q의 경사 막대는 오른쪽으로 갔지만 여전히 왼쪽이며, T의 막대는 더 왼쪽이다.
> 2. (a) 그대로다: $g_x=0.20$, $g_y=0.10$, $\theta=12.60^\circ$. (b) $\sum x_ih_i=0.2(0.16+0.14+0.20)-0.2(0.08+0.06+0.04)=0.064$이므로 $b=0.064/0.24=0.2667$. $\sum y_ih_i=0.2(0.36)-0.2(0.32)=0.008$이므로 $c_0=0.008/0.24=0.0333$ — 다시 양수다. 부호가 뒤집혔던 것은 바위가 한 일이었다. $a=0.98/9=0.1089$, $\theta=\arctan\sqrt{0.2667^2+0.0333^2}=\arctan 0.2687=15.04^\circ$. (c) $\Delta h=0.20-0.08=0.12$ m, $\sigma=0.0199$ m. (d) Q: $15.04/25=0.602$, $0.12/0.15=0.800$, $0.0199/0.05=0.398$ — 관문 통과, $C=0.640$. P2를 실은 Q($\theta_{\max}=22^\circ$): $0.684$, $0.800$, $0.398$ — 통과, $C=0.673$. T: $0.501$, $0.300$, $0.199$ — 통과, $C=0.360$. 순위는 T $<$ Q $<$ Q+P2이고, 처음으로 셋 다 건널 수 있다.
> 3. 중앙 차분이 움직이지 않았고, 움직일 수도 없었다. 그 스텐실은 가운데 셀의 4-연결 이웃 넷인데 바뀐 셀은 그것이 읽지 않는 대각선 모서리다. 그러니 $0.20$ m 격자에서 중앙 차분으로 경사를 계산하는 파이프라인은 Q가 건널 수 있는 패치와 건널 수 없는 패치에 똑같이 $12.60^\circ$를 돌려준다 — 판정을 내리는 바로 그 특징에 눈이 멀어 있고, 매끄러운 지면에서 평면 적합과 잘 맞는다는 사실이 그것을 가린다. 해법은 더 나은 추정기가 아니라 두 번째 항이다. 두 패치를 갈라놓은 것은 단차 높이이고($0.800$에 대해 $1.60$), 그것은 어떤 기울기도 표현할 수 없는 쌍 위의 양이다. §2에서는 — Wild Visual Navigation 뒤의 지도 신호인 **속도 추종**이 둘 다 맞혔을 것이다. 실제로 거기를 달리면서 명령한 속도를 냈는지를 묻는데, 그것이 세 기하 항 전부가 대리하고 있던 결과이기 때문이다. 기하에는 필요 없는데 그것에는 필요한 것은 *로봇이 거기에 가 봤다는 사실*이다. 경험의 기록이라 아무도 달려 보지 않은 땅에는 점수를 매길 수 없고, §1의 논문들이 그것을 라벨을 바깥으로 일반화하는 비전 모델과 짝짓는 이유 전부가 그것이다.
> 4. (a) 풀은 격자에서 점유지만 많은 플랫폼에는 통과 가능하다. BADGR(달려 보며 라벨)이나 고유수용 비용(*How Does It Feel?*)이 기하를 결과로 바꾼다. (b) 킬로미터당 개입, 그리고 거리. 95%는 깨끗한 주행과 조작자 구조 뒤 주행을 섞는다. (c) CVaR는 평균 골이 아니라 꼬리를 벌한다. 평균 최적 경로에도 드문 전복이 남을 수 있고, 경사면 굴착기는 그 꼬리를 본다 — 그리고 위 유도의 관문이 같은 직관의 가장 거친 판본이다. 평균이 사 버리도록 두지 않는 항 하나.

### 출처

- G. Kahn, P. Abbeel, S. Levine, "BADGR: An Autonomous Self-Supervised Learning-Based Navigation System," *IEEE RA-L*, vol. 6, no. 2, pp. 1312–1319, 2021 ([arXiv:2002.05700](https://arxiv.org/abs/2002.05700)).
- J. Frey, M. Mattamala, N. Chebrolu, et al., "Fast Traversability Estimation for Wild Visual Navigation," RSS 2023 ([arXiv:2305.08510](https://arxiv.org/abs/2305.08510)). 저널판: M. Mattamala et al., "Wild visual navigation: fast traversability learning via pre-trained models and online self-supervision," *Autonomous Robots*, vol. 49, no. 3, art. 19, 2025 — **같은 시스템, 두 논문**. 우선권은 RSS를, 전체 서술은 저널판을 인용하라.
- M. Guaman Castro, S. Triest, W. Wang, et al., "How Does It Feel? Self-Supervised Costmap Learning for Off-Road Vehicle Traversability," ICRA 2023 ([arXiv:2209.10788](https://arxiv.org/abs/2209.10788)).
- M. Sivaprakasam, S. Triest, C. Ho, et al., "SALON: Self-supervised Adaptive Learning for Off-road Navigation," ICRA 2025 ([arXiv:2412.07826](https://arxiv.org/abs/2412.07826)).
- S. Jung, J. Lee, X. Meng, B. Boots, A. Lambert, "V-STRONG," ICRA 2024 ([arXiv:2312.16016](https://arxiv.org/abs/2312.16016)) — zero-shot 일반화 주장.
- D. D. Fan, K. Otsu, Y. Kubo, et al., "STEP," RSS 2021 ([arXiv:2103.02828](https://arxiv.org/abs/2103.02828)).
- P. Fankhauser, M. Bloesch, M. Hutter, "Probabilistic Terrain Mapping for Mobile Robots With Uncertain Localization," *IEEE RA-L*, vol. 3, no. 4, pp. 3019–3026, 2018 — `elevation_mapping` 패키지.
- J. Frey, M. Patel, D. Atha, et al., "RoadRunner," *IEEE T-FR* 게재 확정 ([arXiv:2402.19341](https://arxiv.org/abs/2402.19341)); M. Patel et al., "RoadRunner M&M," *IEEE RA-L*, vol. 9, no. 12, pp. 11425–11432, 2024.
- A. Datar, C. Pan, M. Nazeri, X. Xiao, "Toward Wheeled Mobility on Vertically Challenging Terrain," ICRA 2024, pp. 16322–16329 ([arXiv:2303.00998](https://arxiv.org/abs/2303.00998)) — Verti-Wheelers 계열, 조지메이슨대.
- M. Tranzatto, T. Miki, M. Dharmadhikari, et al., "CERBERUS in the DARPA Subterranean Challenge," *Science Robotics*, vol. 7, no. 66, eabp9742, 2022. 더 자세한 서술: *Field Robotics*, vol. 4, no. 1, pp. 249–312, 2024. NeBula: A. Agha et al. ([arXiv:2103.11470](https://arxiv.org/abs/2103.11470)).
- 데이터셋: RUGD (IROS 2019); P. Jiang et al., "RELLIS-3D," ICRA 2021 ([arXiv:2011.12954](https://arxiv.org/abs/2011.12954)); S. Triest et al., "TartanDrive," ICRA 2022 ([arXiv:2205.01791](https://arxiv.org/abs/2205.01791)); P. Mortimer et al., "GOOSE," ICRA 2024 ([arXiv:2310.16788](https://arxiv.org/abs/2310.16788)); R. Hagmanns et al., "GOOSE-Ex," ICRA 2025 ([arXiv:2409.18788](https://arxiv.org/abs/2409.18788)).

**이 위키 안에서**

- **논문 노트** — [[01-canonical-papers/notes/9-navigation/badgr|BADGR]] · [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]]
- [[04-robotics/state-estimation-slam|3. 상태 추정·위치추정·SLAM]] — 고도 지도가 드리프트를 전파하는 그 자세 추정
- [[04-robotics/mpc|MPC]] — STEP의 위험 제약 계획기가 그 변형인 것
- [[04-robotics/legged-locomotion|18. 레그드 로코모션]] — 이 연구 대부분이 돌아가는 로봇들
- [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 자율화]] — 지형 상호작용의 건설 쪽 끝
