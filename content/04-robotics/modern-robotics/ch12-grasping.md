---
title: "MR Ch.12 — Grasping & Manipulation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On P2's panel tile, write the four friction-cone wrench edges, settle force closure and form closure with the positive-span test, and size the preload that holds the tile."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.12** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the wrench (moment + force) from [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §6]], the vector cross product from [[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §1]], and linear independence, rank and rank–nullity from [[02-foundations/linear-algebra|1. Linear Algebra §2]] — the closure test on this page is a rank check. The object is the panel tile that P2 carries, defined below from [[02-foundations/lab-plants|0.6 Lab Plants]].
> [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §6]]의 렌치(모멘트+힘), [[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §1]]의 벡터 외적, 그리고 [[02-foundations/linear-algebra|1. 선형대수 §2]]의 선형 독립, 랭크, 랭크–널리티 정리가 필요하다. 이 페이지의 closure 검사가 랭크 검사다. 대상은 P2가 나르는 패널 타일이고, [[02-foundations/lab-plants|0.6 Lab Plants]]에서 아래와 같이 정의한다.

## English

**Core question**: when does a grasp actually hold the object?

> [!note] First pass · 처음이라면
> Read the running plant, the picture and Steps 1–3 and 6 of the worked case — the cone as an angle, the four edge wrenches, the closure test, and the preload that actually holds the tile — then §3, the same test stated once for any set of contacts. Steps 4, 5 and 7 (frictionless contacts, the pinwheel, and a closure that survives any friction while the preload it needs diverges) and §2's definitions are the second pass, and §1's contact counts are the part to come back to when a paper quotes a finger number. Then the self-check and the problem set, which lowers the friction and shifts the centre of mass.

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] carries a tool, and the tool holds **the panel tile** — frozen here, numbers unchanged for the rest of the page.

| quantity | value | note |
|---|---:|---|
| tile size | $0.200 \times 0.100\ \mathrm{m}$ | corners at $(\pm 0.100,\ \pm 0.050)$ in the tile frame |
| tile mass | $0.500\ \mathrm{kg}$ | weight $W = mg = 0.500 \times 9.81 = 4.905\ \mathrm{N}$, $g$ from 0.6 |
| contacts | $r_1 = (-0.100,\ 0)$, $r_2 = (+0.100,\ 0)$ | midpoints of the two short edges |
| inward normals | $\hat n_1 = (+1,\ 0)$, $\hat n_2 = (-1,\ 0)$ | two point fingers squeezing along $\pm x$ |
| friction | $\mu = 0.5$ | Coulomb, the same $\mu$ the chapter already uses |
| preload | $f_n = 20\ \mathrm{N}$ per finger | the squeeze the gripper applies |

The tile frame's origin is the centre of mass, which is also the midpoint of the two contacts; its $x$ axis is the squeeze axis and its $y$ axis is world-vertical, so gravity acts along $-y$. A planar wrench is written $w = (f_x,\ f_y,\ m_z)$ throughout. That is force first, the order grasping papers use; [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §6]] writes the spatial wrench moment first, $\mathcal F=(m,\ f)$, so reorder the components when you move between the two.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 341" style="max-width:100%;height:auto" role="img" aria-label="the panel tile held by two point fingers at the midpoints of its short edges: inward normals, friction cones of half-angle 26.565°, the contact line through both cones, the 4.905 N weight at the centre of mass and two 2.4525 N finger forces, and the four cone-edge wrenches">
  <defs><marker id="ar12e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="140" y1="30" x2="420" y2="30"/><line x1="140" y1="25" x2="140" y2="35"/><line x1="420" y1="25" x2="420" y2="35"/></g>
  <text x="280" y="24" font-size="11" text-anchor="middle" fill="currentColor">0.200 m</text>
  <path d="M140 120 L229.4 75.3 A100 100 0 0 1 229.4 164.7 Z" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3"><line x1="140" y1="120" x2="229.4" y2="75.3"/><line x1="140" y1="120" x2="229.4" y2="164.7"/></g>
  <text x="233.4" y="73.3" font-size="11.5" text-anchor="start" fill="currentColor">1<tspan dy="-4.4" font-size="9">+</tspan></text>
  <text x="233.4" y="174.7" font-size="11.5" text-anchor="start" fill="currentColor">1<tspan dy="-4.4" font-size="9">−</tspan></text>
  <path d="M420 120 L330.6 75.3 A100 100 0 0 0 330.6 164.7 Z" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3"><line x1="420" y1="120" x2="330.6" y2="75.3"/><line x1="420" y1="120" x2="330.6" y2="164.7"/></g>
  <text x="326.6" y="73.3" font-size="11.5" text-anchor="end" fill="currentColor">2<tspan dy="-4.4" font-size="9">+</tspan></text>
  <text x="326.6" y="174.7" font-size="11.5" text-anchor="end" fill="currentColor">2<tspan dy="-4.4" font-size="9">−</tspan></text>
  <rect x="140" y="50" width="280" height="140" fill="none" stroke="currentColor" stroke-width="2"/>
  <line x1="140" y1="120" x2="420" y2="120" stroke="currentColor" stroke-width="0.9" opacity="0.65"/>
  <g stroke="currentColor" stroke-width="2.2" marker-end="url(#ar12e)"><line x1="140" y1="120" x2="196" y2="120"/><line x1="420" y1="120" x2="364" y2="120"/></g>
  <text x="200" y="114" font-size="12" fill="currentColor">n<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text><polyline points="201,106.8 203.4,104.4 205.8,106.8" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="346" y="114" font-size="12" fill="currentColor">n<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text><polyline points="347,106.8 349.4,104.4 351.8,106.8" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M176 120 L175.9 117.6 L175.7 115.2 L175.3 112.9 L174.7 110.6 L174 108.3 L173.2 106.1 L172.2 103.9" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <text x="193.2" y="87.8" font-size="11" text-anchor="middle" fill="currentColor" transform="rotate(-26.565 193.2 87.8)">α = 26.565°</text>
  <circle cx="140" cy="120" r="3.6" fill="currentColor"/>
  <circle cx="420" cy="120" r="3.6" fill="currentColor"/>
  <circle cx="280" cy="120" r="6" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <path d="M280 120 L286 120 A6 6 0 0 0 280 114 Z M280 120 L274 120 A6 6 0 0 0 280 126 Z" fill="currentColor"/>
  <text x="271" y="111" font-size="11" text-anchor="end" fill="currentColor">CoM</text>
  <line x1="280" y1="127" x2="280" y2="198.5" stroke="currentColor" stroke-width="2.2" marker-end="url(#ar12e)"/>
  <g stroke="currentColor" stroke-width="2" marker-end="url(#ar12e)"><line x1="133" y1="120" x2="133" y2="80.8"/><line x1="427" y1="120" x2="427" y2="80.8"/></g>
  <g fill="currentColor">
  <text x="289" y="206" font-size="11.5">W = 4.905 N</text>
  <text x="289" y="220" font-size="11" opacity="0.85">f<tspan dy="3.1" font-size="8.6">y1</tspan><tspan dy="-3.1" dx="3.3">+ f</tspan><tspan dy="3.1" font-size="8.6">y2</tspan><tspan dy="-3.1" dx="3.3">= W</tspan></text>
  <text x="126" y="98" font-size="11" text-anchor="end">f<tspan dy="3.1" font-size="8.6">y1</tspan><tspan dy="-3.1" dx="3.3">= 2.4525 N</tspan></text>
  <text x="434" y="98" font-size="11">f<tspan dy="3.1" font-size="8.6">y2</tspan><tspan dy="-3.1" dx="3.3">= 2.4525 N</tspan></text>
  <text x="152" y="208" font-size="11" text-anchor="end">r<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = (−0.100, 0)</tspan></text>
  <text x="408" y="208" font-size="11">r<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = (+0.100, 0)</tspan></text>
  </g>
  <rect x="16" y="236" width="528" height="74" fill="none" stroke="currentColor" stroke-width="1" opacity="0.7" rx="4"/>
  <text x="28" y="254" font-size="11" fill="currentColor" font-weight="bold">cone-edge wrenches w = (f<tspan dy="3.1" font-size="8.6">x</tspan><tspan dy="-3.1">, f</tspan><tspan dy="3.1" font-size="8.6">y</tspan><tspan dy="-3.1">, m</tspan><tspan dy="3.1" font-size="8.6">z</tspan><tspan dy="-3.1">), unit normal force</tspan></text>
  <text x="28" y="276" font-size="12" fill="currentColor">1<tspan dy="-4.6" font-size="9.4">+</tspan><tspan dy="4.6" dx="3.6"> (1, 0.5, −0.05)</tspan></text>
  <text x="158" y="276" font-size="12" fill="currentColor">1<tspan dy="-4.6" font-size="9.4">−</tspan><tspan dy="4.6" dx="3.6"> (1, −0.5, +0.05)</tspan></text>
  <text x="288" y="276" font-size="12" fill="currentColor">2<tspan dy="-4.6" font-size="9.4">+</tspan><tspan dy="4.6" dx="3.6"> (−1, 0.5, +0.05)</tspan></text>
  <text x="418" y="276" font-size="12" fill="currentColor">2<tspan dy="-4.6" font-size="9.4">−</tspan><tspan dy="4.6" dx="3.6"> (−1, −0.5, −0.05)</tspan></text>
  <text x="28" y="298" font-size="11" fill="currentColor" opacity="0.9">λ = (1, 1, 1, 1) sums them to (0, 0, 0) and the rank is 3: force closure</text>
  <text x="16" y="328" font-size="11" fill="currentColor" opacity="0.8">tile 0.200 × 0.100 m, 0.500 kg · μ = 0.5 · preload f<tspan dy="3.1" font-size="8.6">n</tspan><tspan dy="-3.1" dx="3.3">= 20 N per finger</tspan></text>
</svg>

The panel tile, $0.200 \times 0.100\,\mathrm{m}$ and $0.500\,\mathrm{kg}$, held by two point fingers at the midpoints of its short edges, $(\pm 0.100,\ 0)$, each contact with its inward normal and a friction cone of half-angle $\tan^{-1}0.5 = 26.565°$. The line joining the contacts lies inside both cones — here it coincides with the normals — and the $4.905\,\mathrm{N}$ weight at the centre of mass is carried by two tangential finger forces of $2.4525\,\mathrm{N}$. The box lists the four cone-edge wrenches $(f_x, f_y, m_z)$; $\lambda = (1,1,1,1)$ sums them to zero and their rank, the number of linearly independent directions among them ([[02-foundations/linear-algebra|1. Linear Algebra §2]]), is 3, so the grasp is a force closure.

### Worked on the plant · 장치로 한 번 끝까지

**Step 1 — the friction cone as an angle.** Coulomb's condition $|f_t| \le \mu f_n$ says the contact force must lie within

$$\alpha = \tan^{-1}\mu = \tan^{-1}0.5 = 26.565°$$

of the inward normal, because $f_t/f_n = \tan(\text{angle from the normal})$. The cone's two boundary rays are therefore the directions $\hat n \pm \mu\,\hat t$, and any force in the cone is a nonnegative combination of them.

**Step 2 — turn each cone edge into a wrench.** A planar contact force $f$ applied at $r$ produces

$$w = (f_x,\ f_y,\ m_z), \qquad m_z = r_x f_y - r_y f_x$$

because the planar cross product $r \times f$ has only a $z$ component. With $r_y = 0$ at both contacts this reduces to $m_z = r_x f_y$, so only the *tangential* force makes a moment here. Taking unit normal component at each edge:

| edge | $r$ | $f$ | $m_z = r_x f_y$ | wrench $w$ |
|---|---|---|---:|---|
| $1^{+}$ | $(-0.100, 0)$ | $(1,\ +0.5)$ | $-0.05$ | $(1,\ 0.5,\ -0.05)$ |
| $1^{-}$ | $(-0.100, 0)$ | $(1,\ -0.5)$ | $+0.05$ | $(1,\ -0.5,\ +0.05)$ |
| $2^{+}$ | $(+0.100, 0)$ | $(-1,\ +0.5)$ | $+0.05$ | $(-1,\ 0.5,\ +0.05)$ |
| $2^{-}$ | $(+0.100, 0)$ | $(-1,\ -0.5)$ | $-0.05$ | $(-1,\ -0.5,\ -0.05)$ |

**Step 3 — the closure test, applied.** Closure asks whether these four wrenches **positively span** $\mathbb{R}^3$: whether every external wrench can be resisted by a nonnegative combination, contacts being able to push but never pull. The computable form of that question is two conditions — find strictly positive coefficients that cancel, and check the rank:

$$\exists\,\lambda > 0 \text{ with } \sum_i \lambda_i w_i = 0, \qquad \operatorname{rank}\,[w_1\ w_2\ w_3\ w_4] = 3$$

since a strictly positive null combination puts the origin in the *interior* of the cone's cross-section, and full rank rules out the whole thing collapsing into a plane. Here $\lambda = (1,1,1,1)$ already works:

$$w_{1^{+}} + w_{1^{-}} + w_{2^{+}} + w_{2^{-}} = (1{+}1{-}1{-}1,\ \ 0.5{-}0.5{+}0.5{-}0.5,\ \ -0.05{+}0.05{+}0.05{-}0.05) = (0,0,0)$$

and the rank is 3 because three independent directions come out of pairs: $w_{1^{+}} + w_{1^{-}} = (2,0,0)$, $w_{1^{+}} + w_{2^{+}} = (0,1,0)$, and $w_{1^{+}} + w_{2^{-}} = (0,0,-0.1)$. Both conditions hold, so the two-finger grasp is a **force closure** — closure with each contact using its whole friction cone; its frictionless twin, form closure, tested in Steps 4–5, uses the normals alone, and §3 defines both. Cross-check it against the antipodal rule of §1: the line joining the contacts runs along $\hat x$, which is the normal at both contacts, so it makes a $0°$ angle with each normal — well inside $26.565°$.

**Step 4 — the same contacts without friction are not form closure.** Set $\mu = 0$ and only the normals survive: $w_1 = (1,0,0)$ and $w_2 = (-1,0,0)$. They cancel with $\lambda = (1,1)$, but the rank is $1$. Their positive span is one line, so the grasp resists nothing in $f_y$ and nothing in $m_z$ — the tile slides down and spins out. That is why frictionless planar form closure needs at least four contacts.

**Step 5 — four frictionless contacts that do close, and four that do not.** Place them as a pinwheel, each normal offset from the centre so that it carries a moment:

| contact | $r$ | $\hat n$ | wrench |
|---|---|---|---|
| $c_1$ | $(-0.100,\ +0.025)$ | $(1,\ 0)$ | $(1,\ 0,\ -0.025)$ |
| $c_2$ | $(+0.100,\ -0.025)$ | $(-1,\ 0)$ | $(-1,\ 0,\ -0.025)$ |
| $c_3$ | $(-0.050,\ +0.050)$ | $(0,\ -1)$ | $(0,\ -1,\ +0.050)$ |
| $c_4$ | $(+0.050,\ -0.050)$ | $(0,\ +1)$ | $(0,\ +1,\ +0.050)$ |

Try $\lambda = (1,1,1,1)$: the sum is $(0,\ 0,\ +0.05)$, not zero — so that choice fails, and the test is not "any $\lambda$". To find the one that works, write $\sum_i \lambda_i w_i = 0$ one component at a time:

$$f_x:\ \lambda_1 - \lambda_2 = 0, \qquad f_y:\ -\lambda_3 + \lambda_4 = 0, \qquad m_z:\ -0.025(\lambda_1 + \lambda_2) + 0.050(\lambda_3 + \lambda_4) = 0$$

so the first two rows force $\lambda_1 = \lambda_2 = a$ and $\lambda_3 = \lambda_4 = b$, and the moment row becomes $-0.05a + 0.1b = 0$, i.e. $a = 2b$. Every solution is therefore a multiple of $\lambda = (2,2,1,1)$, whose coefficients are all positive, and its sum is $(0,\ 0,\ -0.05-0.05+0.05+0.05) = (0,0,0)$. The same system settles the rank: its solutions form a single line, so the null space of the $3 \times 4$ matrix $[w_1\ w_2\ w_3\ w_4]$ has dimension $1$ and rank–nullity gives rank $= 4 - 1 = 3$. **Form closure.** Now move the same four contacts to the edge midpoints, $(\pm 0.100, 0)$ and $(0, \pm 0.050)$, so that every normal passes through the centre of mass. The wrenches become $(\pm1, 0, 0)$ and $(0, \pm1, 0)$, rank $2$, and no positive combination produces any $m_z$ at all: four contacts, the count satisfied, and the tile still free to spin. **The bound of four is necessary, not sufficient.**

**Step 6 — how hard to squeeze.** Closure says a wrench *can* be resisted; it says nothing about how much force that takes. Hold the tile against gravity: the fingers must supply $(0, +W, 0)$, and by symmetry $f_{y1} = f_{y2} = W/2 = 2.4525\,\mathrm{N}$, each of which Coulomb caps at $\mu f_n$. So

$$f_n^{\min} = \frac{W}{2\mu} = \frac{4.905}{2 \times 0.5} = 4.905\ \mathrm{N}$$

because the two contacts share the load and each converts preload into $\mu$ times as much friction. The frozen preload of $20\,\mathrm{N}$ therefore carries a safety factor of $20/4.905 = 4.08$, a total tangential budget of $2\mu f_n = 20\,\mathrm{N}$, and a moment capacity about $z$ of $2\,(\mu f_n)\,(0.100) = 2.00\ \mathrm{N\cdot m}$.

**Step 7 — the limit that separates the two questions.** Repeat Step 3 with a general $\mu > 0$: the four edges are $(1, \pm\mu, \mp 0.1\mu)$ and $(-1, \pm\mu, \pm 0.1\mu)$ in the same pattern, $\lambda = (1,1,1,1)$ still cancels, and the rank is still 3. So the grasp is a force closure **for every positive $\mu$, however small** — and yet $f_n^{\min} = W/(2\mu)$ diverges: at $\mu = 0.05$ it is $49.05\,\mathrm{N}$, ten times the Step 6 figure. Closure is a statement about *directions*; preload is a statement about *magnitudes*. A paper that reports a force-closure grasp has told you the first and nothing about the second.

### 1. The chapter in one list

- **Contact models**: a frictionless point contact can only *push* along the surface
  normal; a point contact with friction can push anywhere inside the **friction cone** —
  half-angle $\alpha = \tan^{-1}\mu$. For $\mu = 0.5$, $\alpha \approx 26.6°$: the physical
  meaning of a friction coefficient is *an angle*. First-order form closure's "at least 4 planar contacts" is falsified by second-order curvature with two contacts, named below.

> **Contact models, defined.** A **contact model** is *a rule for which wrenches one contact can transmit to the body*. MR states the three point-contact models by the motions each forbids (§12.1.5), each forbidding more than the last: a **frictionless point contact** forbids only penetration along the normal, a **point contact with friction** also forbids slip, and a **soft finger** also forbids spin about the contact normal, since a deforming fingertip touches over an area. On the force side each admits more: a push along the inward normal; any force in the friction cone, whose Coulomb form is MR §12.2.1 (§2 here); and that force plus a moment about the normal, whose size MR does not bound. In the plane the last two coincide, since that moment is not a planar wrench component.
>
> $$\text{frictionless: } f = f_n\hat n,\ f_n \ge 0; \qquad \text{with friction: } \lVert f_t\rVert \le \mu f_n; \qquad \text{soft finger: } \lVert f_t\rVert \le \mu f_n \ \text{plus a moment } m_n\hat n$$
>
> where $f_n$ is the push along the inward normal $\hat n$, $f_t$ the tangential part and $m_n$ a moment about $\hat n$, which a model using soft fingers must bound itself. Counting free directions gives $1$, $3$ and $4$ wrench components in space and $1$, $2$ and $2$ in the plane, as many as the motion constraints each contact imposes.
>
> - **Example**: finger 1 on the tile. Frictionless, it transmits only $f_n(1, 0, 0)$; with $\mu = 0.5$, any nonnegative mix of $(1, 0.5, -0.05)$ and $(1, -0.5, 0.05)$, so the frozen $20$ N squeeze allows up to $10$ N of vertical force there.
> - **Non-example**: the two fingers as hard point contacts in space. Both act on the $x$ axis, at $r = (\pm 0.100, 0, 0)$, so every force they apply has moment $r_y f_z - r_z f_y = 0$ about it: their wrenches span $5$ of $6$ dimensions, and a torque about the jaw axis turns the tile at any $\mu$ and squeeze. Soft fingers supply that moment.

- **Form closure**: the geometry alone traps the object (no friction needed) — for
  frictionless point contacts, at least 4 contacts in the plane and 7 in space (both counts
  derived from the closure test in §3). Robust but demanding. Those counts are for **first-order** form closure, which is the qualifier that
  matters: they follow from linearizing the contact constraints, so they only see the contact
  normals. Let the surfaces curve and second-order effects can immobilize a planar body with
  **two** contacts, well under the bound. So the number to quote depends on the order of the
  analysis, not on how the contacts are arranged.
- **Force closure**: with friction, the contacts can resist *any* external wrench —
  the contact friction cones must positively span the whole wrench space (every wrench is a
  *nonnegative* combination of cone directions, because a contact can push but never pull). Practical grasps
  are usually force closures with 2–3 fingers.
- **The antipodal intuition** (worked): for a **planar body with two frictional point
  contacts**, the line joining the contacts must lie inside both friction cones — "the
  fingers can see each other through their cones." The antipodal grasp is defined, with its three conditions, in [[04-robotics/grasping|15. Grasping §3]]. In spatial grasping, two hard point
  contacts cannot resist torque about their connecting axis, because each contact force acts
  at a point on that axis and so has no lever arm about it; at least three point contacts
  are needed. Two **soft-finger** contacts can add torsional moments and achieve spatial
  force closure. Always name the contact model before claiming closure. The lever-arm
  sentence is the whole proof that two hard contacts fail; that three frictional contacts
  can succeed, and the soft-contact model itself, are stated here, not derived — see MR
  §12.2.3.1 and §12.1.5.
- **Learning-era continuation**: grasp synthesis is now largely learned (grasp-detection
  networks, dexterous-hand policies), but the *verification* language — cones, wrenches,
  closure — is still how failures are analyzed. Construction case in this wiki:
  [[01-canonical-papers/notes/8-construction/heap|HEAP's dry-stone wall]] grasps irregular,
  multi-tonne stones, exactly where closure analysis matters, though its open sources
  describe the gripper and the scans rather than a closure analysis.

### 2. The contact wrench and the friction cone, defined

A **contact wrench** is a *vector in wrench space* — $\mathbb{R}^3$ in the plane, $\mathbb{R}^6$ in space — recording everything one contact force does to the body. Two ingredients define it: the force, and the point it acts at. In the plane

$$w(r, f) = (f_x,\ f_y,\ r_x f_y - r_y f_x)$$

where $r$ is the contact position in the body frame and $f$ the force the finger applies to the body, so the third entry is the moment about the frame's origin. Changing the frame origin changes $m_z$ but not $f$, which is why every wrench on this page is referred to the tile's centre of mass.

- **Example**: edge $1^{+}$ above, $w = (1,\ 0.5,\ -0.05)$ — pushing right, dragging up, and rotating the tile clockwise because the upward drag acts $0.100\,\mathrm{m}$ to the left of centre.
- **Non-example**: the pair $(f_x, f_y)$ alone. Two grasps with identical contact forces and different contact *locations* hold the tile differently, and dropping $m_z$ makes them look the same. Step 5 has such a pair: the pinwheel and the edge-midpoint four apply the same forces $(\pm 1, 0)$ and $(0, \pm 1)$, yet with $m_z$ their wrench matrices have rank $3$ and $2$, one holding the tile and one letting it spin, which a force-only check cannot tell apart.

A **friction cone** at a point contact is the *set of forces the contact can transmit*. Its defining conditions are two, and both are inequalities: the normal component cannot pull, $f_n \ge 0$; and the tangential component obeys Coulomb, $|f_t| \le \mu f_n$. Equivalently it is the circular cone of half-angle $\alpha = \tan^{-1}\mu$ about the inward normal, and in the plane it degenerates to a wedge with two edges $\hat n \pm \mu \hat t$.

$$\mathcal{FC} = \{f :\ f_n \ge 0,\ \lVert f_t\rVert \le \mu f_n\}, \qquad \alpha = \tan^{-1}\mu, \qquad \text{plane: } \mathcal{FC} = \{\lambda_+(\hat n + \mu\hat t) + \lambda_-(\hat n - \mu\hat t) :\ \lambda_\pm \ge 0\}$$

where $f_n = f \cdot \hat n$ is the push along the inward normal, $f_t = f - f_n\hat n$ the tangential part and $\mu$ Coulomb's coefficient; MR §12.2.1 writes the spatial cone with the normal along $z$, as $\sqrt{f_x^2 + f_y^2} \le \mu f_z$. The plane form holds because a planar cone has exactly two edges, and every force between them is a nonnegative mix of the two.

- **Example**: $\mu = 0.5$ gives $\alpha = 26.565°$; $\mu = 1.0$ gives exactly $45°$.
- **Non-example**: "$\mu$ is the cone angle." Doubling $\mu$ from $0.5$ to $1.0$ doubles the allowed force *ratio* but takes the angle from $26.565°$ to $45°$, not to $53.13°$. The cone angle is the arctangent, and it saturates at $90°$ however large $\mu$ becomes.
- **Why it matters**: closure tests are linear-algebra questions about the cone *edges*. Get the edge directions wrong and every wrench-space conclusion after them is wrong.

### 3. Form closure and force closure, defined by a computable test

**Form closure** is a property of a *set of contacts on a body*: the contact normals alone, with no friction, immobilize the body. **Force closure** is the same property when each contact may use its whole friction cone. Both are the same mathematical condition applied to different generator sets — the normals, or the cone edges — and the condition is **positive spanning**: every wrench in the space is $\sum_i \lambda_i w_i$ for some $\lambda_i \ge 0$. Made checkable:

$$\text{closure} \iff \exists\,\lambda > 0 \text{ with } \textstyle\sum_i \lambda_i w_i = 0 \ \text{ and } \ \operatorname{rank}[w_1 \cdots w_k] = n$$

with $n = 3$ in the plane and $6$ in space, because a strictly positive combination summing to zero places the origin in the relative interior of the generated cone, and full rank forbids that cone from lying in a proper subspace.

- **Example**: the two frictional fingers, $\lambda = (1,1,1,1)$, rank 3 — force closure. And the pinwheel, $\lambda = (2,2,1,1)$, rank 3 — form closure.
- **Non-example, rank**: two frictionless antipodal normals. They cancel with positive $\lambda$, but rank 1, so the cone is a line.
- **Non-example, count**: four frictionless normals all passing through the centre of mass. Four contacts is the textbook minimum and this arrangement still has rank 2. The minimum is necessary, never sufficient.
- **The minimum, derived from the test**: rank $n$ needs at least $n$ generators, and a nonzero $\lambda$ with $\sum_i \lambda_i w_i = 0$ means the null space of $[w_1 \cdots w_k]$ is not just zero, so rank–nullity gives $k - n \ge 1$. Hence $k \ge n + 1$: four frictionless contacts in the plane and seven in space (MR §12.1.7.1, Theorem 12.6). For force closure the generators are cone edges rather than contacts, which is how two frictional planar contacts, with two edges each, reach the four that $n = 3$ needs.
- **Why it matters**: the test costs a small linear program and gives a yes or no. It gives no margin, no required preload, and no answer at all about whether the fingers can be placed there — which is why Step 6 exists and why grasp *quality* metrics are a separate literature.

> **Internal force, defined.** An **internal force** is *a set of contact forces, one per contact, whose net wrench on the body is zero*: it squeezes without pushing or turning, so the hand can set its size freely (MR §12.2.3). Three conditions define it. **Zero net force**. **Zero net moment**, so equal and opposite is not enough: the pushes must share a line. **Each part inside its own cone**. When a load is held, the contact forces are a load-carrying part plus an internal part, and the internal part is what brings each total force inside its cone; the frozen preload is its size.
>
> $$\sum_i f_{\text{int},i} = 0, \qquad \sum_i r_i \times f_{\text{int},i} = 0, \qquad f_{\text{int},i} \in \mathcal{FC}_i; \qquad \text{tile: } f_{\text{int}} = (s\hat n_1,\ s\hat n_2),\ \ s \ge \frac{W}{2\mu}$$
>
> where $f_{\text{int},i}$ is the internal part at contact $i$, $r_i$ its position, $\mathcal{FC}_i$ its cone and $s$ the squeeze. The tile has four force components and three independent wrench equations, so its internal forces form one line, equal pushes along the contact line; the bound on $s$ is Step 6's, since each finger's friction $\mu s$ must cover $W/2$.
>
> - **Example**: the frozen $s = 20$ N adds $(20 - 20,\ 0,\ 0) = 0$ to the tile and gives each finger $\mu s = 10$ N of friction against the $2.4525$ N it carries, Step 6's safety factor of $4.08$.
> - **Non-example**: $20$ N pushes along the normals from fingers at $(-0.100, +0.025)$ and $(+0.100, -0.025)$. The forces cancel but the moments add to $-1.00$ N·m, so the pair turns the tile instead of squeezing it. For those contacts the internal force lies along the line joining them, $14.0°$ off each normal, and exists only because $14.0° < 26.565°$.

### Self-check

1. What is the friction cone half-angle for $\mu = 1.0$? What does that imply physically?
2. Why does form closure need more contacts than force closure?
3. State the antipodal grasp condition for a parallel-jaw gripper.
4. The tile is lifted with an upward acceleration of $2\,\mathrm{m/s^2}$. What preload does it now need at $\mu = 0.5$?

> [!tip]- Answers
> 1. $\alpha = \tan^{-1}1.0 = 45°$: the contact force may tilt up to 45° away from the surface normal before the model says it slips. A friction coefficient is an *angle*, which is why doubling $\mu$ from 0.5 to 1.0 widens the cone from ~26.6° to 45°: the allowed tangential-to-normal force ratio doubles, but the cone angle does not.
> 2. Form closure must block every direction using geometry alone, without the "free" tangential directions that friction cones supply — so it needs more contacts (at least 4 in the plane, 7 in space for frictionless point contacts). Those bounds are first-order results; curvature is a second-order effect and can immobilize a planar body with two contacts.
> 3. For the planar two-point model, the line joining the contacts lies inside both friction cones. This is not by itself a spatial force-closure test for two hard point contacts; a spatial parallel-jaw argument needs a soft-finger contact model or another source of torsional resistance.
> 4. The fingers must supply $m(g+a) = 0.500 \times 11.81 = 5.905\,\mathrm{N}$ instead of $4.905$, so $f_n^{\min} = 5.905/(2 \times 0.5) = 5.905\,\mathrm{N}$ — a $20.4\,\%$ rise, exactly the ratio $11.81/9.81$. Force closure is unaffected: acceleration changes the wrench to be resisted, not the set of wrenches that can be.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same tile, same two fingers at $(\pm 0.100, 0)$, but two knobs move: site dust drops the friction to $\mu = 0.2$, and the tile now carries a bracket that puts its centre of mass at $(+0.030,\ 0)$ in the grasp frame instead of at the origin.

1. **Draw.** The picture above, with the narrower cones and the shifted centre of mass. Draw the weight arrow at its new location, mark the $0.030\,\mathrm{m}$ lever arm, and add the moment the weight now makes about the grasp midpoint. Write the new half-angle on a cone edge.
2. **Derive.** (a) The new half-angle $\alpha$, and the four cone-edge wrenches. (b) Decide force closure with the positive-span test — state the $\lambda$ you use and the rank. (c) The gravity wrench about the grasp midpoint, then the two tangential forces $f_{y1}, f_{y2}$ that resist it, then the minimum preload $f_n^{\min}$. (d) Does the frozen $20\,\mathrm{N}$ preload still hold the tile, and with what margin?
3. **Interpret.** Did either knob change the force-closure verdict? Answer for each, with the reason. Then explain what the offset costs as a formula rather than a number, and say what would have to change before the grasp fails outright rather than merely needing a harder squeeze.

> [!note]- How to draw it · 그리는 법
> - The tile as a rectangle with its centre of mass marked, and both contact points on the short edges.
> - At each contact, the inward normal as a solid arrow.
> - At each contact, the friction cone: two dashed rays at $\pm\tan^{-1}\mu$ from the normal, the wedge between them shaded, and the half-angle written on one ray.
> - The line joining the two contacts, thin and straight all the way through the tile. Check by eye that it lies inside both shaded wedges — that is the antipodal condition.
> - The weight $W$ as a downward arrow at the centre of mass, and beside it the two tangential (vertical) finger forces that must add up to it.
> - If the weight's line of action misses the grasp midpoint, mark the lever arm and add the moment the weight makes about that midpoint as a curved arrow — the arrow the picture above does not need.
> - In a margin box, the four cone-edge wrenches as $(f_x, f_y, m_z)$ triples.

> [!tip]- Solutions
> 1. The cones are visibly thinner and the weight arrow no longer passes through the grasp midpoint, so a curved moment arrow appears about it.
> 2. (a) $\alpha = \tan^{-1}0.2 = 11.310°$. Edges: $(1,\ 0.2,\ -0.02)$, $(1,\ -0.2,\ +0.02)$, $(-1,\ 0.2,\ +0.02)$, $(-1,\ -0.2,\ -0.02)$. (b) $\lambda = (1,1,1,1)$ sums to $(0,0,0)$, and the rank is 3 because the pairs give $(2,0,0)$, $(0,0.4,0)$ and $(0,0,-0.04)$. Force closure holds. (c) Gravity acts at $(0.030, 0)$ with force $(0,-4.905)$, so $m_z = r_x f_y = 0.030 \times (-4.905) = -0.14715\ \mathrm{N\cdot m}$ and the grasp must supply $(0,\ +4.905,\ +0.14715)$. Then $f_{y1}+f_{y2} = 4.905$ and $-0.100f_{y1} + 0.100f_{y2} = 0.14715$, giving $f_{y2} - f_{y1} = 1.4715$, so $f_{y2} = 3.18825$ and $f_{y1} = 1.71675\ \mathrm{N}$. The binding finger is the one nearer the centre of mass: $f_n^{\min} = 3.18825/0.2 = 15.941\ \mathrm{N}$. (d) Yes: the budget per finger is $\mu f_n = 0.2 \times 20 = 4\ \mathrm{N}$ against a demand of $3.188\ \mathrm{N}$, a margin of $4/3.188 = 1.25$ — against $4.08$ in Step 6, so almost all of the safety factor is gone.
> 3. Neither changed it. Force closure is decided by the cone-edge *directions* and the contact positions, and $\mu > 0$ with unchanged antipodal geometry keeps the positive-span test passing, while moving the centre of mass changes the wrench to be resisted, not the wrenches available. Both knobs move only the preload. As a formula, the offset $e$ raises the worst finger's tangential demand from $W/2$ to $\tfrac{W}{2}(1 + e/\ell)$ with $\ell = 0.100\,\mathrm{m}$ the half-span of the grasp, so $f_n^{\min} = \tfrac{W}{2\mu}(1 + e/\ell)$ — here $1 + 0.3 = 1.30$, a $30\,\%$ surcharge at any $\mu$. Outright failure needs the *directions* to change: $\mu \to 0$ exactly (rank drops to 1), or a re-grasp that stops the contact line from lying inside both cones. An offset never does, not even $e > \ell$ with the centre of mass outside the fingers: $f_{y1} = \tfrac{W}{2}(1 - e/\ell)$ merely turns negative, which friction allows, and the formula above still gives the squeeze.

### Continue beyond this chapter

[[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] extends grasping to contact modes, force/impedance control, tactile sensing, deformable materials, and sim-to-real evaluation.

## 한국어

**핵심 질문**: 파지는 언제 실제로 물체를 붙잡는가?

> [!note] 처음이라면 · First pass
> 이 페이지의 장치, 그림, 그리고 계산의 1–3단계와 6단계 — 각도로서의 원뿔, 모서리 렌치 넷, closure 검사, 그리고 타일을 실제로 붙잡는 예압 — 를 읽고, 그다음 같은 검사를 임의의 접촉 집합에 대해 한 번에 적은 §3을 읽어라. 4·5·7단계(마찰 없는 접촉, 바람개비, 그리고 마찰이 아무리 작아도 유지되지만 필요한 예압은 발산하는 closure)와 §2의 정의는 두 번째 읽기이고, §1의 접촉 개수는 논문이 손가락 수를 인용할 때 돌아와 볼 부분이다. 그다음 스스로 점검과, 마찰을 낮추고 질량 중심을 옮기는 과제.

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**가 도구를 들고, 그 도구가 **패널 타일**을 잡는다. 여기서 고정하고 이 페이지 끝까지 숫자를 바꾸지 않는다.

| 양 | 값 | 비고 |
|---|---:|---|
| 타일 크기 | $0.200 \times 0.100\ \mathrm{m}$ | 타일 좌표계에서 꼭짓점 $(\pm 0.100,\ \pm 0.050)$ |
| 타일 질량 | $0.500\ \mathrm{kg}$ | 무게 $W = mg = 0.500 \times 9.81 = 4.905\ \mathrm{N}$, $g$는 0.6 |
| 접촉점 | $r_1 = (-0.100,\ 0)$, $r_2 = (+0.100,\ 0)$ | 짧은 두 변의 중점 |
| 안쪽 법선 | $\hat n_1 = (+1,\ 0)$, $\hat n_2 = (-1,\ 0)$ | 점 손가락 둘이 $\pm x$로 쥔다 |
| 마찰 | $\mu = 0.5$ | 쿨롱, 이 장이 이미 쓰던 그 $\mu$ |
| 예압 | 손가락당 $f_n = 20\ \mathrm{N}$ | 그리퍼가 주는 쥐는 힘 |

타일 좌표계의 원점은 질량 중심이고 동시에 두 접촉점의 중점이다. $x$축이 쥐는 축, $y$축이 세계의 연직이므로 중력은 $-y$로 작용한다. 평면 렌치는 전부 $w = (f_x,\ f_y,\ m_z)$로 쓴다. 힘이 먼저인 이 순서는 파지 논문들이 쓰는 순서다. [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §6]]은 공간 렌치를 모멘트 먼저 $\mathcal F=(m,\ f)$로 쓰므로, 둘 사이를 오갈 때는 성분 순서를 바꿔야 한다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 341" style="max-width:100%;height:auto" role="img" aria-label="짧은 두 변의 중점에서 점 손가락 둘이 잡은 패널 타일: 안쪽 법선, 반각 26.565°의 마찰 원뿔, 두 원뿔을 지나는 접촉선, 질량 중심의 4.905 N 무게와 2.4525 N 손가락 힘 둘, 그리고 원뿔 모서리 렌치 넷">
  <defs><marker id="ar12k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="140" y1="30" x2="420" y2="30"/><line x1="140" y1="25" x2="140" y2="35"/><line x1="420" y1="25" x2="420" y2="35"/></g>
  <text x="280" y="24" font-size="11" text-anchor="middle" fill="currentColor">0.200 m</text>
  <path d="M140 120 L229.4 75.3 A100 100 0 0 1 229.4 164.7 Z" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3"><line x1="140" y1="120" x2="229.4" y2="75.3"/><line x1="140" y1="120" x2="229.4" y2="164.7"/></g>
  <text x="233.4" y="73.3" font-size="11.5" text-anchor="start" fill="currentColor">1<tspan dy="-4.4" font-size="9">+</tspan></text>
  <text x="233.4" y="174.7" font-size="11.5" text-anchor="start" fill="currentColor">1<tspan dy="-4.4" font-size="9">−</tspan></text>
  <path d="M420 120 L330.6 75.3 A100 100 0 0 0 330.6 164.7 Z" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <g stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3"><line x1="420" y1="120" x2="330.6" y2="75.3"/><line x1="420" y1="120" x2="330.6" y2="164.7"/></g>
  <text x="326.6" y="73.3" font-size="11.5" text-anchor="end" fill="currentColor">2<tspan dy="-4.4" font-size="9">+</tspan></text>
  <text x="326.6" y="174.7" font-size="11.5" text-anchor="end" fill="currentColor">2<tspan dy="-4.4" font-size="9">−</tspan></text>
  <rect x="140" y="50" width="280" height="140" fill="none" stroke="currentColor" stroke-width="2"/>
  <line x1="140" y1="120" x2="420" y2="120" stroke="currentColor" stroke-width="0.9" opacity="0.65"/>
  <g stroke="currentColor" stroke-width="2.2" marker-end="url(#ar12k)"><line x1="140" y1="120" x2="196" y2="120"/><line x1="420" y1="120" x2="364" y2="120"/></g>
  <text x="200" y="114" font-size="12" fill="currentColor">n<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text><polyline points="201,106.8 203.4,104.4 205.8,106.8" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="346" y="114" font-size="12" fill="currentColor">n<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text><polyline points="347,106.8 349.4,104.4 351.8,106.8" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M176 120 L175.9 117.6 L175.7 115.2 L175.3 112.9 L174.7 110.6 L174 108.3 L173.2 106.1 L172.2 103.9" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <text x="193.2" y="87.8" font-size="11" text-anchor="middle" fill="currentColor" transform="rotate(-26.565 193.2 87.8)">α = 26.565°</text>
  <circle cx="140" cy="120" r="3.6" fill="currentColor"/>
  <circle cx="420" cy="120" r="3.6" fill="currentColor"/>
  <circle cx="280" cy="120" r="6" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <path d="M280 120 L286 120 A6 6 0 0 0 280 114 Z M280 120 L274 120 A6 6 0 0 0 280 126 Z" fill="currentColor"/>
  <text x="271" y="111" font-size="11" text-anchor="end" fill="currentColor">질량 중심</text>
  <line x1="280" y1="127" x2="280" y2="198.5" stroke="currentColor" stroke-width="2.2" marker-end="url(#ar12k)"/>
  <g stroke="currentColor" stroke-width="2" marker-end="url(#ar12k)"><line x1="133" y1="120" x2="133" y2="80.8"/><line x1="427" y1="120" x2="427" y2="80.8"/></g>
  <g fill="currentColor">
  <text x="289" y="206" font-size="11.5">W = 4.905 N</text>
  <text x="289" y="220" font-size="11" opacity="0.85">f<tspan dy="3.1" font-size="8.6">y1</tspan><tspan dy="-3.1" dx="3.3">+ f</tspan><tspan dy="3.1" font-size="8.6">y2</tspan><tspan dy="-3.1" dx="3.3">= W</tspan></text>
  <text x="126" y="98" font-size="11" text-anchor="end">f<tspan dy="3.1" font-size="8.6">y1</tspan><tspan dy="-3.1" dx="3.3">= 2.4525 N</tspan></text>
  <text x="434" y="98" font-size="11">f<tspan dy="3.1" font-size="8.6">y2</tspan><tspan dy="-3.1" dx="3.3">= 2.4525 N</tspan></text>
  <text x="152" y="208" font-size="11" text-anchor="end">r<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = (−0.100, 0)</tspan></text>
  <text x="408" y="208" font-size="11">r<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = (+0.100, 0)</tspan></text>
  </g>
  <rect x="16" y="236" width="528" height="74" fill="none" stroke="currentColor" stroke-width="1" opacity="0.7" rx="4"/>
  <text x="28" y="254" font-size="11" fill="currentColor" font-weight="bold">원뿔 모서리 렌치 w = (f<tspan dy="3.1" font-size="8.6">x</tspan><tspan dy="-3.1">, f</tspan><tspan dy="3.1" font-size="8.6">y</tspan><tspan dy="-3.1">, m</tspan><tspan dy="3.1" font-size="8.6">z</tspan><tspan dy="-3.1">), 법선 성분 1</tspan></text>
  <text x="28" y="276" font-size="12" fill="currentColor">1<tspan dy="-4.6" font-size="9.4">+</tspan><tspan dy="4.6" dx="3.6"> (1, 0.5, −0.05)</tspan></text>
  <text x="158" y="276" font-size="12" fill="currentColor">1<tspan dy="-4.6" font-size="9.4">−</tspan><tspan dy="4.6" dx="3.6"> (1, −0.5, +0.05)</tspan></text>
  <text x="288" y="276" font-size="12" fill="currentColor">2<tspan dy="-4.6" font-size="9.4">+</tspan><tspan dy="4.6" dx="3.6"> (−1, 0.5, +0.05)</tspan></text>
  <text x="418" y="276" font-size="12" fill="currentColor">2<tspan dy="-4.6" font-size="9.4">−</tspan><tspan dy="4.6" dx="3.6"> (−1, −0.5, −0.05)</tspan></text>
  <text x="28" y="298" font-size="11" fill="currentColor" opacity="0.9">λ = (1, 1, 1, 1)로 합이 (0, 0, 0)이고 랭크는 3: force closure</text>
  <text x="16" y="328" font-size="11" fill="currentColor" opacity="0.8">타일 0.200 × 0.100 m, 0.500 kg · μ = 0.5 · 손가락당 예압 f<tspan dy="3.1" font-size="8.6">n</tspan><tspan dy="-3.1" dx="3.3">= 20 N</tspan></text>
</svg>

짧은 두 변의 중점 $(\pm 0.100,\ 0)$에서 점 손가락 둘이 잡은 $0.200 \times 0.100\,\mathrm{m}$, $0.500\,\mathrm{kg}$의 패널 타일이고, 각 접촉점에 안쪽 법선과 반각 $\tan^{-1}0.5 = 26.565°$의 마찰 원뿔이 있다. 두 접촉점을 잇는 선은 두 원뿔 안에 있고(여기서는 법선과 일치한다), 질량 중심의 무게 $4.905\,\mathrm{N}$은 $2.4525\,\mathrm{N}$씩의 접선 손가락 힘 둘이 받친다. 상자 안의 원뿔 모서리 렌치 넷 $(f_x, f_y, m_z)$은 $\lambda = (1,1,1,1)$로 합이 0이고, 그 가운데 선형 독립인 방향의 수인 랭크([[02-foundations/linear-algebra|1. 선형대수 §2]])가 3이므로 이 파지는 force closure다.

### 장치로 한 번 끝까지 · Worked on the plant

**1단계 — 마찰 원뿔은 각도다.** 쿨롱 조건 $|f_t| \le \mu f_n$은 접촉력이 안쪽 법선에서

$$\alpha = \tan^{-1}\mu = \tan^{-1}0.5 = 26.565°$$

이내에 있어야 한다는 뜻이다. $f_t/f_n = \tan(\text{법선에서의 각})$이기 때문이다. 따라서 원뿔의 두 경계 방향은 벡터 $\hat n \pm \mu\,\hat t$이고, 원뿔 안의 모든 힘은 그 둘의 음이 아닌 결합이다.

**2단계 — 원뿔 모서리를 렌치로.** 평면에서 $r$에 작용하는 접촉력 $f$는

$$w = (f_x,\ f_y,\ m_z), \qquad m_z = r_x f_y - r_y f_x$$

를 만든다. 평면 외적 $r \times f$가 $z$ 성분만 갖기 때문이다. 두 접촉 모두 $r_y = 0$이므로 $m_z = r_x f_y$로 줄고, 여기서는 *접선* 힘만 모멘트를 만든다. 각 모서리에서 법선 성분을 1로 두면:

| 모서리 | $r$ | $f$ | $m_z = r_x f_y$ | 렌치 $w$ |
|---|---|---|---:|---|
| $1^{+}$ | $(-0.100, 0)$ | $(1,\ +0.5)$ | $-0.05$ | $(1,\ 0.5,\ -0.05)$ |
| $1^{-}$ | $(-0.100, 0)$ | $(1,\ -0.5)$ | $+0.05$ | $(1,\ -0.5,\ +0.05)$ |
| $2^{+}$ | $(+0.100, 0)$ | $(-1,\ +0.5)$ | $+0.05$ | $(-1,\ 0.5,\ +0.05)$ |
| $2^{-}$ | $(+0.100, 0)$ | $(-1,\ -0.5)$ | $-0.05$ | $(-1,\ -0.5,\ -0.05)$ |

**3단계 — closure 검사를 적용한다.** closure는 이 렌치 넷이 $\mathbb{R}^3$를 **양으로 생성**하는지 묻는다. 즉 모든 외부 렌치를 음이 아닌 결합으로 버틸 수 있는지다. 접촉은 밀 수만 있고 당길 수 없기 때문이다. 그 질문의 계산 가능한 형태는 조건 둘이다. 상쇄되는 엄격히 양인 계수를 찾고, 랭크를 확인한다:

$$\exists\,\lambda > 0,\ \sum_i \lambda_i w_i = 0, \qquad \operatorname{rank}\,[w_1\ w_2\ w_3\ w_4] = 3$$

엄격히 양인 영결합이 원점을 원뿔 단면의 *내부*에 놓고, 풀랭크가 전체가 평면으로 주저앉는 것을 막기 때문이다. 여기서는 $\lambda = (1,1,1,1)$이 이미 된다:

$$w_{1^{+}} + w_{1^{-}} + w_{2^{+}} + w_{2^{-}} = (1{+}1{-}1{-}1,\ \ 0.5{-}0.5{+}0.5{-}0.5,\ \ -0.05{+}0.05{+}0.05{-}0.05) = (0,0,0)$$

랭크가 3인 이유는 쌍에서 독립인 방향 셋이 나오기 때문이다. $w_{1^{+}} + w_{1^{-}} = (2,0,0)$, $w_{1^{+}} + w_{2^{+}} = (0,1,0)$, $w_{1^{+}} + w_{2^{-}} = (0,0,-0.1)$. 두 조건이 모두 성립하므로 손가락 둘의 파지는 **force closure**다. 각 접촉이 마찰 원뿔 전체를 쓰는 closure라는 뜻이고, 4–5단계가 검사하는 마찰 없는 짝인 form closure는 법선만 쓴다. 둘 다 §3이 정의한다. §1의 대척 규칙으로 교차 확인하면, 두 접촉점을 잇는 선이 $\hat x$이고 그것이 양쪽 법선이므로 각 법선과 이루는 각이 $0°$, $26.565°$ 안쪽으로 충분하다.

**4단계 — 같은 접촉을 마찰 없이 두면 form closure가 아니다.** $\mu = 0$으로 두면 법선만 남아 $w_1 = (1,0,0)$, $w_2 = (-1,0,0)$이다. $\lambda = (1,1)$로 상쇄되지만 랭크가 $1$이다. 양의 생성이 직선 하나뿐이라 $f_y$도 $m_z$도 전혀 버티지 못한다. 타일이 미끄러져 내려가고 돌아 빠진다. 마찰 없는 평면 form closure에 접촉이 최소 넷 필요한 이유다.

**5단계 — closure가 되는 마찰 없는 접촉 넷과 안 되는 넷.** 바람개비처럼 놓아 각 법선이 중심에서 벗어나게 하면 모멘트를 낸다:

| 접촉 | $r$ | $\hat n$ | 렌치 |
|---|---|---|---|
| $c_1$ | $(-0.100,\ +0.025)$ | $(1,\ 0)$ | $(1,\ 0,\ -0.025)$ |
| $c_2$ | $(+0.100,\ -0.025)$ | $(-1,\ 0)$ | $(-1,\ 0,\ -0.025)$ |
| $c_3$ | $(-0.050,\ +0.050)$ | $(0,\ -1)$ | $(0,\ -1,\ +0.050)$ |
| $c_4$ | $(+0.050,\ -0.050)$ | $(0,\ +1)$ | $(0,\ +1,\ +0.050)$ |

$\lambda = (1,1,1,1)$을 넣으면 합이 $(0,\ 0,\ +0.05)$로 0이 아니다. 그 선택은 실패하며, 검사는 "아무 $\lambda$나"가 아니다. 되는 것을 찾으려면 $\sum_i \lambda_i w_i = 0$을 성분별로 쓴다:

$$f_x:\ \lambda_1 - \lambda_2 = 0, \qquad f_y:\ -\lambda_3 + \lambda_4 = 0, \qquad m_z:\ -0.025(\lambda_1 + \lambda_2) + 0.050(\lambda_3 + \lambda_4) = 0$$

처음 두 행이 $\lambda_1 = \lambda_2 = a$, $\lambda_3 = \lambda_4 = b$를 강제하고, 모멘트 행은 $-0.05a + 0.1b = 0$, 곧 $a = 2b$가 된다. 따라서 모든 해는 $\lambda = (2,2,1,1)$의 배수이고, 그 계수는 모두 양수이며 합은 $(0,\ 0,\ -0.05-0.05+0.05+0.05) = (0,0,0)$이다. 같은 연립방정식이 랭크도 정한다. 해가 직선 하나를 이루므로 $3 \times 4$ 행렬 $[w_1\ w_2\ w_3\ w_4]$의 영공간은 $1$차원이고, 랭크–널리티 정리로 랭크 $= 4 - 1 = 3$이다. **Form closure.** 이제 같은 접촉 넷을 변의 중점 $(\pm 0.100, 0)$과 $(0, \pm 0.050)$으로 옮겨 모든 법선이 질량 중심을 지나게 해 보자. 렌치는 $(\pm1, 0, 0)$과 $(0, \pm1, 0)$이 되어 랭크 $2$, 어떤 양의 결합도 $m_z$를 전혀 만들지 못한다. 접촉은 넷이고 개수 조건은 채웠는데 타일은 여전히 자유롭게 돈다. **넷이라는 하한은 필요조건이지 충분조건이 아니다.**

**6단계 — 얼마나 세게 쥐어야 하는가.** closure는 렌치를 버틸 수 *있다*고 말할 뿐 얼마나 큰 힘이 드는지는 말하지 않는다. 중력에 맞서 타일을 든다고 하자. 손가락이 $(0, +W, 0)$을 내야 하고 대칭에서 $f_{y1} = f_{y2} = W/2 = 2.4525\,\mathrm{N}$이며, 쿨롱은 각각을 $\mu f_n$으로 자른다. 따라서

$$f_n^{\min} = \frac{W}{2\mu} = \frac{4.905}{2 \times 0.5} = 4.905\ \mathrm{N}$$

이다. 두 접촉이 하중을 나눠 지고 각각이 예압을 그 $\mu$배의 마찰로 바꾸기 때문이다. 그러므로 고정된 $20\,\mathrm{N}$ 예압은 안전율 $20/4.905 = 4.08$, 접선 여유 총 $2\mu f_n = 20\,\mathrm{N}$, $z$ 둘레 모멘트 용량 $2\,(\mu f_n)\,(0.100) = 2.00\ \mathrm{N\cdot m}$을 준다.

**7단계 — 두 질문을 가르는 극한.** 3단계를 일반의 $\mu > 0$으로 반복하면 모서리 넷이 같은 형태의 $(1, \pm\mu, \mp 0.1\mu)$와 $(-1, \pm\mu, \pm 0.1\mu)$이고, $\lambda = (1,1,1,1)$이 여전히 상쇄되며 랭크도 여전히 3이다. 즉 **$\mu$가 아무리 작아도 양이기만 하면** force closure다. 그런데 $f_n^{\min} = W/(2\mu)$는 발산한다. $\mu = 0.05$면 $49.05\,\mathrm{N}$, 6단계 값의 열 배다. closure는 *방향*에 관한 진술이고 예압은 *크기*에 관한 진술이다. force closure 파지를 보고한 논문은 앞의 것을 말한 것이고 뒤의 것은 아무것도 말하지 않은 것이다.

### 1. 이 장을 목록 하나로

- **접촉 모델**: 마찰 없는 점 접촉은 표면 법선 방향으로만 *밀 수* 있다; 마찰 있는 점
  접촉은 **마찰 원뿔** 안 어디로든 밀 수 있다 — 반각 $\alpha = \tan^{-1}\mu$.
  $\mu = 0.5$면 $\alpha \approx 26.6°$: 마찰 계수의 물리적 의미는 *각도*다. 1차 form closure의 "평면 접촉 최소 4개"는 아래에 이름을 적은 2차 곡률 효과, 접촉 둘로 반증된다.

> **접촉 모델의 정의.** **접촉 모델**(contact model)은 *접촉 하나가 물체에 전달할 수 있는 렌치를 정하는 규칙*이다. MR은 점 접촉 모델 셋을 각 접촉이 막는 운동으로 정의하며(§12.1.5), 뒤의 것일수록 더 많이 막는다. **마찰 없는 점 접촉**(frictionless point contact)은 법선 방향의 침투만 막고, **마찰 있는 점 접촉**(point contact with friction)은 미끄럼도 막으며, **soft finger**는 접촉 법선 둘레의 회전까지 막는다. 변형되는 손가락 끝은 면적으로 닿기 때문이다. 힘 쪽에서는 뒤의 것일수록 더 많이 허용한다. 안쪽 법선 방향의 밀기, 마찰 원뿔 안의 어떤 힘(쿨롱 원뿔은 MR §12.2.1, 여기서는 §2), 그리고 그 힘에 법선 둘레 모멘트를 더한 것인데, 그 모멘트의 크기를 MR은 제한하지 않는다. 평면에서는 그 모멘트가 평면 렌치의 성분이 아니므로 뒤의 둘이 같다.
>
> $$\text{마찰 없음: } f = f_n\hat n,\ f_n \ge 0; \qquad \text{마찰 있음: } \lVert f_t\rVert \le \mu f_n; \qquad \text{soft finger: } \lVert f_t\rVert \le \mu f_n\text{에 모멘트 } m_n\hat n\text{ 추가}$$
>
> 여기서 $f_n$은 안쪽 법선 $\hat n$ 방향의 밀기, $f_t$는 접선 성분, $m_n$은 $\hat n$ 둘레의 모멘트이고, soft finger를 쓰는 모델은 그 한계를 스스로 정해야 한다. 자유로운 방향을 세면 렌치 성분이 공간에서 $1$, $3$, $4$개, 평면에서 $1$, $2$, $2$개로, 각 접촉이 가하는 운동 구속의 수와 같다.
>
> - **예**: 타일의 손가락 1. 마찰이 없으면 $f_n(1, 0, 0)$만 전달하고, $\mu = 0.5$면 $(1, 0.5, -0.05)$와 $(1, -0.5, 0.05)$의 음이 아닌 결합이면 무엇이든 전달한다. 그래서 고정된 $20$ N 쥐기로 그 손가락에서 연직 힘을 $10$ N까지 낼 수 있다.
> - **비예**: 두 손가락을 공간의 hard point 접촉으로 본 것. 둘 다 $x$축 위의 $r = (\pm 0.100, 0, 0)$에 작용하므로, 가하는 모든 힘의 그 축 둘레 모멘트가 $r_y f_z - r_z f_y = 0$이다. 렌치가 $6$차원 중 $5$차원만 생성하고, 조 축 둘레의 토크는 어떤 $\mu$와 쥐기에서도 타일을 돌린다. soft finger가 그 모멘트를 준다.

- **Form closure**: 기하만으로 물체를 가둔다(마찰 불필요) — 마찰 없는 점 접촉에서 평면
  최소 4개, 공간 최소 7개의 접촉이 필요하다(두 수 모두 §3에서 closure 검사로부터 유도한다). 강건하지만 요구가 크다. 이 수는 **1차**
  form closure에 대한 것이고, 그 단서가 핵심이다. 접촉 구속을 선형화해서 얻은 결과라 접촉
  법선만 본다. 표면이 휘면 2차 효과가 개입해 평면 물체를 접촉 **2개**로 가둘 수 있고, 이는
  경계보다 한참 아래다. 즉 인용할 숫자는 접촉을 어떻게 배치했는지가 아니라 몇 차까지
  분석했는지에 달렸다.
- **Force closure**: 마찰이 있으면 접촉들이 *임의의* 외부 렌치를 버틸 수 있다 — 접촉
  마찰 원뿔들이 렌치 공간 전체를 양의 결합으로 생성해야 한다(모든 렌치가 원뿔 방향들의 *음이 아닌* 결합이어야 한다는 뜻이다. 접촉은 밀 수만 있고 당길 수 없기 때문이다). 실용적 파지는 대개 손가락
  2~3개의 force closure다.
- **대척 파지의 직관** (예제): **평면 물체와 마찰 점접촉 둘**의 모델에서는 두 접촉점을
  잇는 선이 두 마찰 원뿔 안에 있어야 한다 — "두 손가락이 원뿔을 통해 서로를 본다." 대척 파지의 세 정의 조건은 [[04-robotics/grasping|15. 파지 §3]]에 있다.
  공간에서는 hard point 접촉 둘만으로 두 점을 잇는 축 둘레의 토크를 막을 수 없어(각 접촉력이 그 축 위의 점에 작용하므로 축에 대한 지렛대 팔이 없다) 최소 세
  점접촉이 필요하다. **Soft-finger** 접촉 둘은 비틀림 모멘트를 더해 공간 force closure가
  가능하다. Closure를 주장하기 전에 접촉 모델부터 밝혀야 한다. hard 접촉 둘이 실패한다는
  것은 지렛대 팔 문장이 증명 전부다. 마찰 접촉 셋이면 성공할 수 있다는 것과 soft 접촉 모델
  자체는 여기서 유도하지 않고 진술만 한다 — MR §12.2.3.1과 §12.1.5를 보라.
- **학습 시대의 연속**: 파지 생성은 이제 대부분 학습된다(파지 검출 네트워크, 정밀 손
  정책) — 하지만 *검증*의 언어(원뿔, 렌치, closure)는 여전히 실패 분석의 도구다. 이
  위키의 건설 사례: [[01-canonical-papers/notes/8-construction/heap|HEAP의 돌담]]은 불규칙한
  수 톤급 돌을 파지하므로 closure 분석이 중요한 바로 그 자리다. 다만 공개 출처는 closure
  분석이 아니라 그리퍼와 스캔을 기술한다.

### 2. 접촉 렌치와 마찰 원뿔의 정의

**접촉 렌치**는 *렌치 공간의 벡터*다. 평면이면 $\mathbb{R}^3$, 공간이면 $\mathbb{R}^6$이고, 접촉력 하나가 물체에 하는 일을 전부 담는다. 정의에 들어가는 재료는 둘, 힘과 그 작용점이다. 평면에서는

$$w(r, f) = (f_x,\ f_y,\ r_x f_y - r_y f_x)$$

이고 $r$은 물체 좌표계의 접촉 위치, $f$는 손가락이 물체에 주는 힘이므로 셋째 성분은 좌표 원점 둘레의 모멘트다. 원점을 바꾸면 $m_z$는 바뀌고 $f$는 안 바뀐다. 이 페이지의 모든 렌치를 타일의 질량 중심 기준으로 쓰는 이유다.

- **예**: 위의 모서리 $1^{+}$, $w = (1,\ 0.5,\ -0.05)$ — 오른쪽으로 밀고, 위로 끌고, 타일을 시계 방향으로 돌린다. 위로 끄는 힘이 중심에서 왼쪽으로 $0.100\,\mathrm{m}$ 떨어진 곳에 작용하기 때문이다.
- **반례**: 쌍 $(f_x, f_y)$만. 접촉력은 같고 접촉 *위치*가 다른 두 파지는 타일을 다르게 잡는데, $m_z$를 버리면 둘이 같아 보인다. 5단계에 그런 쌍이 있다. 바람개비와 변 중점 배치는 같은 힘 $(\pm 1, 0)$과 $(0, \pm 1)$을 가하지만, $m_z$를 넣으면 렌치 행렬의 랭크가 $3$과 $2$라 하나는 타일을 붙잡고 하나는 돌게 둔다. 힘만 보는 검사로는 둘을 가를 수 없다.

점 접촉의 **마찰 원뿔**은 *그 접촉이 전달할 수 있는 힘들의 집합*이다. 정의 조건은 둘이고 둘 다 부등식이다. 법선 성분은 당길 수 없다, 즉 $f_n \ge 0$. 접선 성분은 쿨롱을 지킨다, 즉 $|f_t| \le \mu f_n$. 같은 말로, 안쪽 법선 둘레의 반각 $\alpha = \tan^{-1}\mu$인 원뿔이며, 평면에서는 모서리 $\hat n \pm \mu \hat t$ 둘을 가진 쐐기로 축퇴한다.

$$\mathcal{FC} = \{f :\ f_n \ge 0,\ \lVert f_t\rVert \le \mu f_n\}, \qquad \alpha = \tan^{-1}\mu, \qquad \text{평면: } \mathcal{FC} = \{\lambda_+(\hat n + \mu\hat t) + \lambda_-(\hat n - \mu\hat t) :\ \lambda_\pm \ge 0\}$$

여기서 $f_n = f \cdot \hat n$은 안쪽 법선 방향의 밀기, $f_t = f - f_n\hat n$은 접선 성분, $\mu$는 쿨롱 계수다. MR §12.2.1은 법선을 $z$로 두고 공간 원뿔을 $\sqrt{f_x^2 + f_y^2} \le \mu f_z$로 쓴다. 평면 형태가 성립하는 것은 평면 원뿔의 모서리가 정확히 둘이고, 그 사이의 모든 힘이 두 모서리의 음이 아닌 결합이기 때문이다.

- **예**: $\mu = 0.5$면 $\alpha = 26.565°$; $\mu = 1.0$이면 정확히 $45°$.
- **반례**: "$\mu$가 원뿔 각이다". $\mu$를 $0.5$에서 $1.0$으로 두 배 하면 허용 힘 *비*는 두 배가 되지만 각은 $26.565°$에서 $45°$가 되지 $53.13°$가 되지 않는다. 원뿔 각은 아크탄젠트이고, $\mu$가 아무리 커져도 $90°$에서 포화한다.
- **왜 중요한가**: closure 검사는 원뿔 *모서리*에 대한 선형대수 질문이다. 모서리 방향을 틀리면 그 뒤의 렌치 공간 결론이 전부 틀린다.

### 3. Form closure와 force closure를 계산 가능한 검사로 정의하기

**Form closure**는 *물체 위 접촉 집합*의 성질이다. 마찰 없이 접촉 법선만으로 물체를 못 움직이게 한다는 뜻이다. **Force closure**는 각 접촉이 자기 마찰 원뿔 전체를 쓸 수 있을 때의 같은 성질이다. 둘은 생성자 집합만 다를 뿐 — 법선이냐 원뿔 모서리냐 — 같은 수학 조건이고, 그 조건이 **양의 생성**이다. 공간의 모든 렌치가 어떤 $\lambda_i \ge 0$에 대해 $\sum_i \lambda_i w_i$여야 한다. 검사 가능한 형태로 쓰면:

$$\text{closure} \iff \exists\,\lambda > 0,\ \textstyle\sum_i \lambda_i w_i = 0 \ \text{ 이고 } \ \operatorname{rank}[w_1 \cdots w_k] = n$$

평면이면 $n = 3$, 공간이면 $6$이다. 엄격히 양인 결합이 0이 된다는 것은 원점이 생성된 원뿔의 상대적 내부에 있다는 뜻이고, 풀랭크는 그 원뿔이 진부분공간에 갇히는 것을 막기 때문이다.

- **예**: 마찰 손가락 둘, $\lambda = (1,1,1,1)$, 랭크 3 — force closure. 그리고 바람개비, $\lambda = (2,2,1,1)$, 랭크 3 — form closure.
- **반례(랭크)**: 마찰 없는 대척 법선 둘. 양의 $\lambda$로 상쇄되지만 랭크가 1이라 원뿔이 직선이다.
- **반례(개수)**: 질량 중심을 모두 지나는 마찰 없는 법선 넷. 넷은 교과서적 최소치인데 이 배치는 랭크가 2다. 최소치는 필요조건일 뿐 절대 충분조건이 아니다.
- **검사에서 유도한 최소치**: 랭크 $n$에는 생성자가 적어도 $n$개 필요하고, $\sum_i \lambda_i w_i = 0$인 0이 아닌 $\lambda$가 있다는 것은 $[w_1 \cdots w_k]$의 영공간이 0만이 아니라는 뜻이므로, 랭크–널리티 정리가 $k - n \ge 1$을 준다. 따라서 $k \ge n + 1$, 곧 평면에서 마찰 없는 접촉 넷, 공간에서 일곱이다(MR §12.1.7.1, 정리 12.6). force closure에서는 생성자가 접촉이 아니라 원뿔 모서리이므로, 모서리를 둘씩 가진 평면 마찰 접촉 둘이 $n = 3$에 필요한 넷을 채운다.
- **왜 중요한가**: 검사는 작은 선형계획 하나 값이고 예/아니오를 준다. 여유도, 필요한 예압도, 손가락을 거기 놓을 수 있는지도 말해 주지 않는다. 6단계가 있는 이유이자 파지 *품질* 지표가 별개의 문헌인 이유다.

> **내력의 정의.** **내력**(internal force)은 *접촉마다 하나씩인 접촉력의 집합으로, 물체에 주는 합 렌치가 0인 것*이다. 밀지도 돌리지도 않고 쥐기만 하므로 손이 그 크기를 마음대로 정할 수 있다(MR §12.2.3). 정의 조건은 셋이다. **합력이 0**이다. **합 모멘트가 0**이다. 그래서 크기가 같고 방향이 반대인 것만으로는 부족하고, 두 밀기가 한 직선 위에 있어야 한다. **각 성분이 제 원뿔 안에 있다.** 하중을 들 때 접촉력은 하중을 나르는 부분과 내력 부분의 합이고, 각 합력을 원뿔 안으로 들여놓는 것이 내력 부분이다. 고정된 예압이 그 크기다.
>
> $$\sum_i f_{\text{int},i} = 0, \qquad \sum_i r_i \times f_{\text{int},i} = 0, \qquad f_{\text{int},i} \in \mathcal{FC}_i; \qquad \text{타일: } f_{\text{int}} = (s\hat n_1,\ s\hat n_2),\ \ s \ge \frac{W}{2\mu}$$
>
> 여기서 $f_{\text{int},i}$는 접촉 $i$의 내력 부분, $r_i$는 그 위치, $\mathcal{FC}_i$는 그 원뿔, $s$는 쥐는 힘이다. 타일은 힘 성분이 넷이고 독립인 렌치 방정식이 셋이므로, 내력은 직선 하나, 곧 접촉선을 따라 같은 크기로 미는 것뿐이다. $s$의 하한은 6단계의 것이다. 손가락마다 마찰 $\mu s$가 $W/2$를 덮어야 하기 때문이다.
>
> - **예**: 고정된 $s = 20$ N은 타일에 $(20 - 20,\ 0,\ 0) = 0$을 더하고, 손가락마다 나르는 $2.4525$ N에 맞서 마찰 $\mu s = 10$ N을 준다. 6단계의 안전율 $4.08$이다.
> - **비예**: $(-0.100, +0.025)$와 $(+0.100, -0.025)$의 손가락이 법선을 따라 미는 $20$ N. 힘은 상쇄되지만 모멘트가 더해져 $-1.00$ N·m가 되므로, 이 쌍은 타일을 쥐는 대신 돌린다. 그 접촉들의 내력은 둘을 잇는 선을 따라 각 법선에서 $14.0°$ 기울어 있고, $14.0° < 26.565°$이기 때문에만 존재한다.

### 스스로 점검

1. $\mu = 1.0$일 때 마찰 원뿔 반각은? 물리적으로 무엇을 의미하는가?
2. form closure가 force closure보다 많은 접촉을 요구하는 이유는?
3. 평행 그리퍼의 대척 파지 조건을 말하라.
4. 타일을 $2\,\mathrm{m/s^2}$로 위로 가속하며 든다. $\mu = 0.5$에서 예압은 얼마가 되어야 하는가?

> [!tip]- 정답 · Answers
> 1. $\alpha = \tan^{-1}1.0 = 45°$ — 접촉력이 법선에서 45°까지 기울어도 미끄러지지 않는다. 마찰 계수는 *각도*이므로 $\mu$를 0.5에서 1.0으로 두 배 하면 원뿔이 ~26.6°에서 45°로 넓어진다. 허용되는 접선 대 법선 힘의 비는 두 배가 되지만 원뿔 각은 두 배가 되지 않는다.
> 2. 마찰 원뿔이 주는 여유 방향 없이 기하만으로 모든 방향을 막아야 하기 때문이다(마찰 없는 점 접촉에서 평면 최소 4개, 공간 최소 7개). 이 경계는 1차 결과이고, 곡률은 2차 효과라 평면 물체를 접촉 2개로 가둘 수 있다.
> 3. 평면 2점 모델에서는 두 접촉점을 잇는 선이 두 마찰 원뿔 안에 있어야 한다. 이것만으로
> 공간의 hard point 접촉 둘이 force closure인 것은 아니다. 공간 평행 그리퍼에는 soft-finger
> 모델이나 다른 비틀림 저항이 필요하다.
> 4. 손가락이 $4.905$ 대신 $m(g+a) = 0.500 \times 11.81 = 5.905\,\mathrm{N}$을 내야 하므로 $f_n^{\min} = 5.905/(2 \times 0.5) = 5.905\,\mathrm{N}$, $20.4\,\%$ 증가이고 정확히 비 $11.81/9.81$이다. force closure는 영향을 받지 않는다. 가속은 버텨야 할 렌치를 바꾸지 버틸 수 있는 렌치의 집합을 바꾸지 않는다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 타일도 같고 $(\pm 0.100, 0)$의 손가락 둘도 같지만 노브 둘이 움직인다. 현장 먼지로 마찰이 $\mu = 0.2$로 떨어지고, 타일이 브래킷을 달아 질량 중심이 파지 좌표계의 원점이 아니라 $(+0.030,\ 0)$에 온다.

1. **그리기.** 위의 그림을 좁아진 원뿔과 옮겨진 질량 중심으로 다시 그린다. 무게 화살표를 새 위치에 그리고 $0.030\,\mathrm{m}$ 지렛대 팔을 표시하며, 무게가 이제 파지 중점 둘레에 만드는 모멘트를 더한다. 원뿔 모서리에 새 반각을 적는다.
2. **유도.** (a) 새 반각 $\alpha$와 마찰 원뿔 모서리 렌치 넷. (b) 양의 생성 검사로 force closure를 판정하라. 쓴 $\lambda$와 랭크를 밝힐 것. (c) 파지 중점 둘레의 중력 렌치, 그것을 버티는 접선 힘 $f_{y1}, f_{y2}$, 그리고 최소 예압 $f_n^{\min}$. (d) 고정된 $20\,\mathrm{N}$ 예압으로 타일을 여전히 잡는가, 여유는 얼마인가?
3. **해석.** 두 노브 중 force closure 판정을 바꾼 것이 있는가? 각각에 대해 이유와 함께 답하라. 그다음 옮겨진 질량 중심의 대가를 숫자가 아니라 공식으로 설명하고, 더 세게 쥐는 정도가 아니라 파지가 아예 실패하려면 무엇이 바뀌어야 하는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - 타일은 질량 중심을 표시한 직사각형으로, 접촉점 둘은 짧은 두 변 위에 그린다.
> - 각 접촉점에 안쪽 법선을 실선 화살표로 그린다.
> - 각 접촉점에 마찰 원뿔을 그린다. 법선에서 $\pm\tan^{-1}\mu$인 점선 두 개, 그 사이를 칠한 쐐기, 그리고 한쪽 선에 적은 반각.
> - 두 접촉점을 잇는 선을 타일을 관통하는 가는 직선으로 긋고, 칠한 두 쐐기 안에 있는지 눈으로 확인한다. 그것이 대척 조건이다.
> - 질량 중심에 무게 $W$를 아래 방향 화살표로, 그 옆에 합이 그것과 같아야 하는 접선(연직) 손가락 힘 두 개를 그린다.
> - 무게의 작용선이 파지 중점을 비껴가면 지렛대 팔을 표시하고, 무게가 그 중점 둘레에 만드는 모멘트를 굽은 화살표로 더한다. 위의 그림에는 필요 없던 화살표다.
> - 여백 상자에 원뿔 모서리 렌치 네 개를 $(f_x, f_y, m_z)$ 삼중항으로 나열한다.

> [!tip]- 정답 · Solutions
> 1. 원뿔이 눈에 띄게 얇아지고 무게 화살표가 더 이상 파지 중점을 지나지 않으므로, 그 둘레에 굽은 모멘트 화살표가 하나 나타난다.
> 2. (a) $\alpha = \tan^{-1}0.2 = 11.310°$. 모서리: $(1,\ 0.2,\ -0.02)$, $(1,\ -0.2,\ +0.02)$, $(-1,\ 0.2,\ +0.02)$, $(-1,\ -0.2,\ -0.02)$. (b) $\lambda = (1,1,1,1)$의 합이 $(0,0,0)$이고, 쌍에서 $(2,0,0)$, $(0,0.4,0)$, $(0,0,-0.04)$가 나오므로 랭크는 3이다. force closure가 성립한다. (c) 중력은 $(0.030, 0)$에 $(0,-4.905)$로 작용하므로 $m_z = r_x f_y = 0.030 \times (-4.905) = -0.14715\ \mathrm{N\cdot m}$이고 파지는 $(0,\ +4.905,\ +0.14715)$를 내야 한다. 그러면 $f_{y1}+f_{y2} = 4.905$, $-0.100f_{y1} + 0.100f_{y2} = 0.14715$에서 $f_{y2} - f_{y1} = 1.4715$이므로 $f_{y2} = 3.18825$, $f_{y1} = 1.71675\ \mathrm{N}$. 걸리는 쪽은 질량 중심에 가까운 손가락이고 $f_n^{\min} = 3.18825/0.2 = 15.941\ \mathrm{N}$. (d) 잡는다. 손가락당 여유가 $\mu f_n = 0.2 \times 20 = 4\ \mathrm{N}$인데 요구가 $3.188\ \mathrm{N}$이라 $4/3.188 = 1.25$배다. 6단계의 $4.08$에 비하면 안전율이 거의 사라졌다.
> 3. 둘 다 바꾸지 않았다. force closure는 원뿔 모서리의 *방향*과 접촉 위치가 결정하는데, 대척 기하가 그대로이고 $\mu > 0$이면 양의 생성 검사는 계속 통과한다. 질량 중심을 옮기는 것은 버텨야 할 렌치를 바꾸지 쓸 수 있는 렌치를 바꾸지 않는다. 두 노브는 예압만 움직인다. 공식으로 쓰면, 편심 $e$는 가장 불리한 손가락의 접선 요구를 $W/2$에서 $\tfrac{W}{2}(1 + e/\ell)$로 올린다. $\ell = 0.100\,\mathrm{m}$은 파지의 반너비다. 따라서 $f_n^{\min} = \tfrac{W}{2\mu}(1 + e/\ell)$이고, 여기서는 $1 + 0.3 = 1.30$, 어떤 $\mu$에서도 $30\,\%$ 할증이다. 아예 실패하려면 *방향*이 바뀌어야 한다. $\mu$가 정확히 0이 되거나(랭크가 1로 떨어진다), 접촉선이 두 원뿔 안에 있지 않게 다시 쥐어야 한다. 편심은 $e > \ell$로 질량 중심이 손가락 바깥으로 나가도 파지를 아예 실패시키지 못한다. $f_{y1} = \tfrac{W}{2}(1 - e/\ell)$이 음수가 될 뿐이고 마찰은 그것을 허용하므로, 쥐는 힘은 여전히 위 공식이 정한다.

### 이 장 다음으로

[[04-robotics/contact-force-tactile|접촉·힘·촉각 상호작용]]이 파지를 접촉 모드, 힘·임피던스
제어, 촉각 센싱, 변형체, sim-to-real 평가로 확장한다.
