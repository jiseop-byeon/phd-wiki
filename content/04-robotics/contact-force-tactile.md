---
title: 9. Contact, Force & Tactile Interaction
tags: [robotics, contact, manipulation, tactile]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
wiki-support: Working
---

## English

*Group E, and the only page in it, because everything in group H branches from here. Stands on [[02-foundations/linear-algebra|linear algebra]],
optimization and the [[04-robotics/modern-robotics/index|MR chapters]]. This is where geometry stops being enough, the moment the robot touches something.*

Once a robot touches the world, geometry alone is insufficient. Contact introduces forces, friction, impacts, changing modes, deformation, and uncertainty. These effects are central to grasping, assembly, excavation, wiping, drilling, and handling flexible materials.

> [!info] Depth target
> Read contact-rich manipulation papers by identifying the contact model, sensing, control mode, material assumptions, and evaluation. Detailed complementarity solvers and continuum mechanics remain optional working/mastery topics.

> [!note] Prerequisites
> [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/optimization|Optimization]] · [[04-robotics/modern-robotics/ch05-velocity-kinematics|Statics and Jacobians]] · [[04-robotics/modern-robotics/ch08-dynamics|Dynamics]] · [[04-robotics/modern-robotics/ch12-grasping|Grasping]]

> [!note] First pass · 처음이라면
> Read the running object and the worked case below — they are the one calculation this page owes you, and they run from "is there a contact at all" to "does the grip hold". Then §1, why contact changes the problem at all, then §5 (position, force, impedance, admittance), then §6, the wall-wiping scenario that puts all four in one task. §2 to §4 are the mechanics; read them when a paper's friction or closure claims matter.

> [!tip] From sensing contact to displaying it
> This page explains robot-side contact. Continue to [[04-robotics/haptics-teleoperation/tactile-display-design|Tactile Display Design]] when the contact cue must be rendered to a person, and to [[04-robotics/haptics-teleoperation/rendering-sampling-stability|Rendering, Sampling & Stability]] when a virtual wall or force-feedback loop must remain stable.

### Running object: P2 against a P3-stiffness panel

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the planar 2R arm, $L_1=L_2=1\,\mathrm{m}$ — at the frozen pose $\theta=(0^\circ,90^\circ)$, where the tip sits at $(1,1)\,\mathrm{m}$, carrying a tool that presses a flat panel. The panel's face is the plane $x=1\,\mathrm{m}$, so the tip touches it exactly at that pose, and its stiffness is **P3**'s wall value. This is the catalog's robotics running task — *move a tool to a panel and make controlled contact* — with the panel standing up, where the question is friction. [[04-robotics/force-compliance-control|13. Force & Compliance Control]] takes the same arm and tool with the panel lying under the tip, where the question is the relation between motion and force.

| Symbol | Value | What it is |
|---|---:|---|
| $\hat n$ | $+x$ | contact normal, counted positive **into** the panel |
| $\hat t_1,\ \hat t_2$ | $-y$, $+z$ | the two tangent directions in the panel's face |
| $k_w$ | $400\,\mathrm{N/m}$ | panel stiffness — P3's virtual-wall value |
| $d_c$ | $4\,\mathrm{N\cdot s/m}$ | contact damping for §3's penalty model — this page's only addition to P3 |
| $\mu$ | $0.5$ | friction coefficient, tool on panel |
| $\delta$ | $5\,\mathrm{mm}$ | commanded penetration past the face |
| $\dot\delta$ | $0.02\,\mathrm{m/s}$ | closing speed at the instant of first touch |
| $m_p$ | $1.0\,\mathrm{kg}$ | the panel's own mass, for when it is picked up in §4 |
| $g$ | $9.81\,\mathrm{m/s^2}$ | gravity, acting in $-y$ |

Two tangents and not one, although P2 is planar: the *arm* moves in a plane but the *contact* is three-dimensional, and §2's cone is a three-dimensional cone. Collapsing it to one tangent would hide the entire linearization question, which is where half the contact literature's optimizers live.

*Scope: this page teaches the mechanics of one contact — when a contact exists, how much force it can carry, how that force becomes an object wrench, and what closure does and does not promise — plus how to read a contact-rich paper's sensing and evaluation. It does not teach how to choose a controller for that contact ([[04-robotics/force-compliance-control|13. Force & Compliance Control]]), how to plan or score a grasp ([[04-robotics/grasping|Grasping]]), how a tactile signal is rendered back to a person ([[04-robotics/haptics-teleoperation/tactile-display-design|24.2 Tactile Display Design]]), or how a contact simulator's solver is built ([[06-research-practice/simulators-benchmarks-datasets|Simulators, Benchmarks & Datasets]]).*

### Homework diagram: the contact frame on the panel, with the cone standing on it

Draw it once; the problem set asks for the same drawing at different numbers.

**Left — the arm and the panel, in the $x$–$y$ plane, to scale.** P2's base at the origin, link 1 along $+x$ to the elbow at $(1,0)$, link 2 up to the tip at $(1,1)$. A vertical line at $x=1$ for the panel's face, with the panel drawn as a rectangle hanging on it. At the tip, the contact frame: $\hat n$ pointing $+x$ into the face, $\hat t_1$ pointing $-y$ down the face along the wipe. A small spring symbol between tip and face labelled $k_w=400$ N/m, compressed by $\delta=5$ mm — drawn much larger than to scale, with a note saying so, because 5 mm on a 1 m arm is invisible.

**Right — the cone, in the contact frame.** The normal axis $\hat n$ vertical, the tangent plane $(\hat t_1,\hat t_2)$ horizontal. The circular cone opening upward with half-angle $\arctan\mu=26.6^\circ$, marked as an angle. On the tangent plane, three closed curves drawn concentrically: the true circle of radius $\mu f_n$; outside it the **square** of the outer box pyramid, touching the circle at four points; inside it the **square** of the four-generator inner cone, with its four corners *on* the circle. One arrow for the commanded wipe, drawn at its actual length, so the reader can see which of the three sets contains it.

**Underneath — the gap axis.** A horizontal line for $\phi$ with zero marked. To the left of zero ($\phi>0$, apart) write $f_n=0$; at $\phi=0$ and to the right write $f_n\ge0$. Two dots: one at $\phi=+2$ mm before touchdown, one at $\phi=-5$ mm, the penetration the penalty model of §3 allows and the rigid model of §1 forbids. The pair $(\phi,f_n)$ must never be off the two rays — that picture *is* complementarity.

### Worked case: one contact, from gap to grip margin

Six steps on the object above, each proved by the section named in its heading. Every number here is recomputed in the problem set with two of the table's entries changed.

**Step 1 — is there a contact at all? (§1).** Hold the tool 2 mm short of the face: $\phi=0.002$ m and $f_n=0$ N, so $\phi f_n=0$ and the pair sits on the left ray. Drive to the face: $\phi=0$, and now $f_n$ may be anything non-negative — the model has stopped predicting the force and started only constraining it. That switch is the whole difficulty: the two cases are different sets of equations, so the number that decides which one holds is a *measurement*, not a command.

**Step 2 — how much normal force? (§3).** The rigid model cannot answer, because at $\phi=0$ it only says $f_n\ge0$. Commanding $\delta=5$ mm past the face makes the rigid model infeasible, so use the penalty model, which trades non-penetration for a spring:

$$f_n=k_w\,\delta+d_c\,\dot\delta=400\times0.005+4\times0.02=2.00+0.08=2.08\ \mathrm{N}$$

so at rest the panel carries $f_n=2.00$ N and the extra $0.08$ N exists only while the tool is still closing at $0.02$ m/s. Hold that 2 N: every bound below is proportional to it.

**Step 3 — how much wipe will the contact carry? (§2).** The cone's half-angle is $\arctan 0.5=26.5651^\circ\to26.6^\circ$, and at $f_n=2.00$ N it allows

$$\lVert f_t\rVert\le\mu f_n=0.5\times2.00=1.00\ \mathrm{N}$$

A 3 N downward wipe is three times the bound, so the tool slides and friction pins $f_t$ at $-1.00$ N opposing the slip. A 1 N wipe sits *exactly* on the bound: allowed, with zero margin. That is the honest reading of "it sticks" — the model permits it and nothing in the model says it will survive a 1% change in $\mu$.

**Step 4 — what is a solver allowed to believe? (§2, the linearization).** An optimizer that must stay a QP replaces the circle by facets, and the two standard replacements err in opposite directions. The outer box pyramid's corner at this contact is $\lVert f_t\rVert=\sqrt{1.00^2+1.00^2}=1.414$ N, which is $41.4\%$ past the real bound — it would authorise a wipe that slips. The four-generator inner cone allows only $\mu\cos(\pi/4)\times f_n=0.354\times2.00=0.707$ N, throwing away $29.3\%$ of the available friction — it would refuse the 1 N wipe the real contact permits. Eight generators cut that loss to $7.6\%$ ($0.924$ N) and sixteen to $1.9\%$ ($0.981$ N).

**Step 5 — the same contact as an object wrench (§4).** Put the panel's frame origin on its mounting bracket, $0.40$ m below the contact, so $r=(0,0.40,0)$ m, and take the full contact force with the 1 N wipe, $f=(2.00,-1.00,0)$ N. Then $m=r\times f=(0,0,-0.80)$ N·m and

$$\mathcal{F}=\begin{pmatrix}m\\ f\end{pmatrix}=(0,\ 0,\ -0.80,\ 2.00,\ -1.00,\ 0)$$

so the panel feels a 0.80 N·m twist about $z$ that nobody commanded. It appeared only because the origin moved 0.40 m; the physical push is unchanged. Move the origin to the contact and the moment is zero.

**Step 6 — and the grip that has to hold the panel afterwards (§4).** Two fingers squeeze the 1.0 kg panel at $\pm0.05$ m with 10 N each. Each cone admits $\mu\times10=5$ N of tangential force, so the pair carries $2\times5=10.0$ N against a weight of $m_pg=1.0\times9.81=9.81$ N. The margin is $0.19$ N, which is $1.9\%$ of the load. Equivalently, the coefficient at which the grip exactly holds is

$$\mu^\star=\frac{m_pg}{2f}=\frac{9.81}{2\times10}=0.4905$$

so the nominal $\mu=0.5$ clears it by $1.9\%$. Dust dropping $\mu$ to $0.40$ takes the capacity to 8.0 N, short of the weight by 1.81 N: the panel goes to the floor.

**What the six steps add up to.** The wipe has exactly zero margin and the grip has $1.9\%$, and *both bounds are the same $\mu$* — a number that was assumed, not measured, and that dust changes without moving the panel one pixel in the camera. Every quantity on this page is either proportional to $f_n$, which the controller sets, or proportional to $\mu$, which nobody observed. §7 is about closing that gap with measurement, and §9 is about what a paper has to report before its contact claim means anything.

### 1. Why contact changes the problem

A contact is typically **unilateral**: objects may push but do not pull through an ordinary surface. Motion can switch among separation, impact, sticking, and sliding. This makes the dynamics hybrid and often nonsmooth.

Write $\phi(q)$ for the **gap**: the distance between the nearest points of the two surfaces when the robot and object are in configuration $q$ (for a fingertip above a table, simply its height above the table), positive when they are apart and zero when they touch. In practice a collision-geometry library computes it from the two shapes and their poses. For a gap $\phi(q)\ge 0$ and normal force $f_n\ge 0$, ideal rigid contact is summarized by

$$\phi(q)f_n=0$$

If separated, force is zero; if normal force is positive, the gap is closed. This complementarity is an idealized model, not a literal description of material deformation.

**Rigid unilateral contact, all three conditions.** The model is a set of conditions on a pair of scalars, the gap $\phi(q)$ and the normal force $f_n$ (the force component along the contact normal, positive when the surfaces push each other apart). A pair satisfies the **complementarity condition** when all three hold:

- **Non-penetration**: the bodies never overlap, so the gap cannot be negative.
$$\phi(q)\ge 0$$
- **Unilaterality**: the surface can push but never pull, so the normal force cannot be negative.
$$f_n\ge 0$$
- **Complementarity**: at most one of the two is nonzero, since a force can act only across a closed gap.
$$\phi(q)\,f_n=0$$

The three are written together as $0\le\phi(q)\perp f_n\ge 0$, where $\perp$ means "their product is zero". Because each case (apart with $f_n=0$, or touching with $f_n\ge0$) is a different set of equations, the dynamics switch between **contact modes**, which is what makes contact hybrid and nonsmooth. Stacking these conditions for every contact point turns one simulation step into a **linear complementarity problem** (LCP: find $z\ge0$ with $w=Mz+q\ge0$ and $z^\top w=0$), the form rigid-body simulators solve ([[06-research-practice/simulators-benchmarks-datasets|Simulators, Benchmarks & Datasets]]).

> [!example] Worked example · 계산 예제
> A 0.1 kg block held 2 mm above a table has $\phi=0.002$ m and $f_n=0$, so $\phi f_n=0$ ✓. Set it down and at rest $\phi=0$ and $f_n=mg=0.1\times9.81=0.981$ N, again $\phi f_n=0$ ✓.
> **Non-examples**: $\phi=0.001$ m with $f_n=0.5$ N violates complementarity (a force across an open gap), $f_n=-0.5$ N violates unilaterality (the table pulling the block down), and $\phi<0$ violates non-penetration; a penalty model (§3) deliberately allows that last one.

### 2. Normal force and friction

Coulomb friction is commonly approximated by

$$\lVert f_t\rVert\le \mu f_n$$

where $f_n$ is normal force, $f_t$ tangential force, and $\mu$ the friction coefficient. Forces inside the friction cone can be consistent with sticking; boundary or exceeded conditions indicate impending or actual slip under the model. The cone is a *force-feasibility bound* — whether the contact actually sticks or slides also depends on relative motion and the contact law. Real friction depends on material, speed, pressure, wear, and surface state.

**The friction cone and Coulomb's law, each part named.** Split the contact force $f\in\mathbb{R}^3$ into its normal component $f_n$ (a scalar along the unit normal) and its tangential component $f_t\in\mathbb{R}^2$ (in the contact plane), and let $v_t$ be the relative sliding velocity in that plane. The **friction cone** is the set of contact forces the model allows,

$$FC=\{\,f:\ f_n\ge 0,\ \lVert f_t\rVert\le\mu f_n\,\}$$

so it has two conditions: **unilaterality** ($f_n\ge0$, as in §1) and the **Coulomb bound** ($\lVert f_t\rVert\le\mu f_n$). It is a circular cone about the normal with half-angle $\arctan\mu$, because the bound says the force may tilt from the normal until tangential over normal equals $\mu$. **Coulomb's law** then adds which boundary the force sits on:

- **Sticking** ($v_t=0$): any $f\in FC$ is allowed, and $f_t$ is whatever holds the contact still.
- **Sliding** ($v_t\ne0$): the force is on the cone's surface and opposes the slip, since friction dissipates energy.
$$f_t=-\mu f_n\,\frac{v_t}{\lVert v_t\rVert}$$

Many models use a larger static coefficient $\mu_s$ for the stick bound and a smaller kinetic $\mu_k$ while sliding; a single $\mu$ assumes they are equal.

**The linearized friction cone, and which way it errs.** The bound $\lVert f_t\rVert\le\mu f_n$ is a *second-order* cone: the constraint is a norm, not a set of linear inequalities. Any optimizer that needs a quadratic program ([[02-foundations/optimization|4. Optimization §5]]) therefore replaces it by a **polyhedral cone** — a cone bounded by finitely many flat facets. There are two standard replacements, they approximate from opposite sides, and calling both of them "the friction pyramid" is how the error gets lost.

- The **outer box pyramid** bounds each tangential axis separately, $|f_{t,1}|\le\mu f_n$ and $|f_{t,2}|\le\mu f_n$ — four facets, two per axis. It **contains** the true cone, so it admits forces that would slip: at $f_n=2$ N and $\mu=0.5$ its corner is $\lVert f_t\rVert=\sqrt{1^2+1^2}=1.414$ N against a true bound of 1 N, $41.4\%$ too generous. This is the form [[04-robotics/convex-mpc-legged|8. Convex MPC]] uses in its fourth modelling move, and shrinking the coefficient to $\mu/\sqrt2$ is how that page buys the error back.
- The **inner polyhedral cone** is instead *spanned* by $m$ generator rays spaced evenly around the normal, each ray lying on the true cone's surface:

$$f=\sum_{j=1}^{m}\lambda_j\,g_j,\qquad \lambda_j\ge0,\qquad g_j=\hat n+\mu\left(\cos\tfrac{2\pi j}{m}\,\hat t_1+\sin\tfrac{2\pi j}{m}\,\hat t_2\right)$$

  where $\lambda_j$ is the non-negative weight on ray $j$ and $m$ is the facet count the modeller chooses. Every force it admits is **inside** the true cone, since the generators are on the cone and the cone is convex, so a nonnegative combination of them cannot leave it. Its price is the friction it discards: the inscribed polygon's inradius gives it an effective coefficient $\mu\cos(\pi/m)$, which is $0.354$ at $m=4$ ($29.3\%$ of the bound thrown away), $0.462$ at $m=8$ ($7.6\%$) and $0.490$ at $m=16$ ($1.9\%$).

At $m=4$ the inner cone's coefficient $\mu\cos(\pi/4)$ and the shrunk box's $\mu/\sqrt2$ are the same number, $0.354$, which is why the two constructions are so easily confused. They are still different sets, and the direction of the error is the point: **outer is optimistic about grip, inner is pessimistic, and neither is the cone.** Which one a paper solved decides whether its planner can promise a contact it cannot hold, or refuse one it could.

> [!example] Worked example · 계산 예제
> $\mu=0.5$ gives a half-angle $\arctan0.5=26.6°$. With $f_n=10$ N the cone allows $\lVert f_t\rVert\le5$ N: a 4 N tangential load can stick, and a 6 N demand cannot (Self-check 2).
> **On the running object** the same arithmetic runs at $f_n=2$ N and is worked in full in the worked case above, steps 3 and 4 — including what each linearization would have allowed instead.
> **Non-example**: $f_n=-2$ N is outside the cone for every $\mu$, however small $f_t$ is, because a surface cannot pull. And the circular cone is not the same set as either polyhedral cone above, which is why a solver's reported friction margin is a margin against its own facets. Grasp analysis builds on these cones in [[04-robotics/grasping|Grasping §2]].

<svg viewBox="0 0 440 214" style="max-width:100%;height:auto" role="img" aria-label="the friction cone: forces inside stick, forces outside slip">
  <defs><marker id="fcA" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6"><line x1="30" y1="150" x2="410" y2="150"/></g>
  <g fill="currentColor" opacity="0.10"><path d="M150,150 L96,36 L204,36 Z"/></g>
  <g stroke="currentColor" stroke-width="1.5" fill="none"><path d="M150,150 L96,36"/><path d="M150,150 L204,36"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.6"><line x1="150" y1="150" x2="150" y2="30"/></g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.75"><path d="M150,95 A55,55 0 0 1 175.9,101.1"/></g>
  <g stroke="currentColor" stroke-width="2" fill="none">
    <path d="M150,150 L172,72" marker-end="url(#fcA)"/>
    <path d="M150,150 L252,92" marker-end="url(#fcA)"/>
  </g>
  <g fill="currentColor"><circle cx="150" cy="150" r="3.5"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="138" y="24">f_n</text>
    <text x="215" y="60">inside the cone: can stick</text>
    <text x="264" y="100">outside: slips</text>
    <text x="30" y="172">the marked angle is the cone half-angle = arctan(mu)</text>
    <text x="30" y="192" opacity="0.85">the cone bounds the force, not the motion &#8212;</text>
    <text x="30" y="208" opacity="0.85">whether contact actually sticks also depends on the contact law</text>
  </g>
</svg>

The inequality is useful because increasing tangential demand without enough normal support can exceed the assumed sticking region. For example, dust on a grasped panel can change the usable friction while its visual pose stays nearly unchanged. A planner that treats μ as known may therefore overestimate the contact margin. **The reading this gives you.** Ask how μ was obtained and whether slip feedback can correct a mistaken assumption before the object is lost. The force bound explains a possible failure mechanism; it does not substitute for observing the actual contact state.

### 3. Rigid and compliant models

| Model | Useful when | Main limitation |
|---|---|---|
| Rigid contact | deformation is small relative to task scale | impacts and mode switches are nonsmooth |
| Penalty/compliant contact | simulation needs continuous penetration forces | stiffness and damping are hard to identify |
| Learned/residual model | repeatable mismatch remains in data | extrapolation and physical consistency |

**The penalty model, written out.** A penalty (compliant) contact drops §1's non-penetration condition and instead lets the bodies overlap by a small **penetration depth** $\delta=\max(0,-\phi)$, then pushes back like a spring and damper:

$$f_n=\max\!\big(0,\ k\,\delta+d\,\dot\delta\big)$$

so $k$ (contact stiffness, N/m) sets how much force a given overlap produces, $d$ (contact damping, N·s/m) resists the rate of overlap $\dot\delta$, and the outer $\max$ keeps unilaterality because the model must never pull. Example: $k=10^4$ N/m and a 1 mm overlap at rest give $f_n=10^4\times0.001=10$ N. It is continuous where the rigid model switches, which is why simulators like it, and its price is that $k$ and $d$ are numerical choices rather than measured material constants. A **learned residual** has the form $x_{t+1}=f_{\text{phys}}(x_t,u_t)+r_\theta(x_t,u_t)$, where $f_{\text{phys}}$ is the physics model's prediction and $r_\theta$ a fitted correction with parameters $\theta$.

Simulator contact parameters are often numerical compromises. Success under one simulator setting is not evidence of robustness to real material variation.

The model choice matters because an apparent controller improvement may come from a more forgiving simulated contact. For example, a compliant wall can absorb a wiping path error that would produce a force spike against a stiffer surface. A learned residual (a model fitted to the part of the true dynamics that the physics-based model leaves unexplained) can correct repeatable mismatch, but only where its training observations constrain that correction. **The reading this gives you.** Separate the contact law, its parameter identification, and numerical settings. Then look for validation against the relevant physical response rather than success under one convenient simulator configuration.

### 4. Grasp and wrench language

A contact force produces a force and moment on the object; stacked into one vector they are a **wrench** (defined in [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5]]). The **grasp map** is the matrix that adds up all the contact forces into a single object wrench. Two closure notions build on it:

- **Form closure** immobilizes an object through geometry alone, under a specified contact model.
- **Force closure** uses admissible contact forces, commonly including friction, to resist arbitrary external wrenches.

Required contact counts depend on dimension, friction and contact assumptions, and general-position conditions, meaning the count assumes no degenerate, coincidental arrangement such as contact normals that happen to line up.

**Build the wrench from one contact first.** A force $f$ applied at displacement $r$ from the chosen object origin creates moment $r\times f$. Moving the origin changes the moment coordinates even though the physical push is unchanged. Express every contact in a common frame before summing forces and moments; otherwise the grasp map combines incompatible quantities.

**Wrench, grasp map and the two closures as formulas.**

- A **wrench** is a six-vector stacking a moment $m\in\mathbb{R}^3$ on a force $f\in\mathbb{R}^3$, in Modern Robotics' order. For a force applied at point $r$ in the object frame, the moment is taken about the frame origin:
$$\mathcal{F}=\begin{pmatrix}m\\ f\end{pmatrix}=\begin{pmatrix}r\times f\\ f\end{pmatrix}\in\mathbb{R}^6$$
  Example: $f=(0,0,-10)$ N at $r=(0.2,0,0)$ m gives $m=r\times f=(0,2,0)$ N·m, so the object feels 10 N down plus a 2 N·m twist about $y$.
- The **grasp map** $G$ sums the wrenches of $k$ point contacts. Stack the contact forces into $f_c=(f_1,\dots,f_k)\in\mathbb{R}^{3k}$, all expressed in the object frame; each column block $G_i$ turns $f_i$ into its wrench, so
$$\mathcal{F}_{\text{obj}}=G\,f_c=\sum_{i=1}^{k}\begin{pmatrix}r_i\times f_i\\ f_i\end{pmatrix}$$
  and $G$ is a $6\times3k$ matrix. It is linear in the forces, which is why closure questions become questions about cones and spans.
- **Force closure**: for every external wrench $\mathcal{F}_{\text{ext}}$ there are admissible contact forces that cancel it, where admissible means each $f_i$ lies in its friction cone $FC_i$ (§2).
$$\forall\,\mathcal{F}_{\text{ext}}\in\mathbb{R}^6\ \ \exists\, f_i\in FC_i:\quad G\,f_c=-\mathcal{F}_{\text{ext}}$$
  Because the cones are closed under positive scaling, this says the image of the cones under $G$ is all of $\mathbb{R}^6$.
- **Form closure** (first order): the same statement with **frictionless** contacts, so each $f_i=\lambda_i n_i$ with $\lambda_i\ge0$ along the inward normal $n_i$; the normal wrenches must positively span $\mathbb{R}^6$ (every wrench is a nonnegative combination of them). That needs at least 4 contacts in the plane and 7 in space, and the counts and their qualifiers are in [[04-robotics/grasping|Grasping §3]].

Now imagine two fingers squeezing a panel. The two opposing forces may have zero net object wrench while maintaining a compressive preload at the contacts. That preload can make friction available against a later disturbance. Thus a zero net wrench does not mean “no contact forces,” and a large squeeze does not by itself establish force closure. The allowable contact forces must collectively resist disturbances in every required direction, under the stated friction and unilateral-contact constraints. With finite actuator limits, they resist a bounded set rather than literally unbounded external loads.

> [!example] Worked example · 계산 예제
> Fingers at $r_1=(-0.05,0,0)$ m and $r_2=(0.05,0,0)$ m squeeze with $f_1=(10,0,0)$ N and $f_2=(-10,0,0)$ N. The net force is $(0,0,0)$ and both moments are zero ($r_i\parallel f_i$), so $G f_c=0$ although each contact carries 10 N. With $\mu=0.5$ each cone admits up to $0.5\times10=5$ N of tangential force, so the pair can hold a vertical load of up to $2\times5=10$ N at this squeeze.
> **Non-example**: the same squeeze with frictionless fingers ($\mu=0$) resists no vertical load at all, since every admissible force is along $x$; it is not force closure however hard it squeezes.

> [!question] Check what closure promises · 닫힘의 보장 확인
> Does force closure guarantee that the selected grip will hold a heavy panel? **Answer:** no. Closure is a capability under a contact model. The particular load must also fit within friction, actuator and material limits at the selected forces.

### 5. Position, force, impedance, and admittance

| Mode | What is regulated |
|---|---|
| Position control | pose or trajectory error |
| Force control | measured contact force |
| Impedance control | desired relationship from motion error to force |
| Admittance control | desired motion response to measured force |

Impedance does not simply “control both position and force.” It shapes interaction behavior, often as a virtual mass–spring–damper — written out, the controller commands a spring and a damper anchored at the reference, the inertia term dropped as most implementations do, so that the force it produces is set by displacement and velocity alone:

$$F = K(x_d - x) + D(\dot x_d - \dot x)$$

so $K$ (stiffness, N/m) and $D$ (damping, N·s/m) are the *design* variables, and the force that actually appears depends on how far the environment pushed the tool off $x_d$. Position control is the limit $K \to \infty$; force control regulates $F$ directly and lets $x$ go where it must. Admittance is useful when a stiff, accurate position-controlled robot can convert measured force into a compliant motion command. The three coefficients this whole table turns on — stiffness, its inverse **compliance**, and damping, with their units and the series rule that makes the softest element win — are defined once in [[04-robotics/force-compliance-control|13. Force & Compliance Control §1]].

**The four modes as control laws.** Each row of the table is a different choice of what the feedback acts on. Here $x_d$ is the reference pose, $F$ the force the robot applies to the environment (so the force on the robot is $F_{ext}=-F$), $F_d$ the desired force and $F_m$ the measured one.

- **Position control** feeds back pose error only, and contact force is whatever results: $u=K_p(x_d-x)+K_v(\dot x_d-\dot x)$ with high gains $K_p,K_v$ (the PD law of [[04-robotics/control-theory-ce397|Control Theory §7]]).
- **Force control** feeds back force error, commonly with a proportional-integral law, and position is whatever results: $F=F_d+K_f(F_d-F_m)+K_i\int(F_d-F_m)\,dt$.
- **Impedance control** renders the spring-damper above, a map from motion error to force; its full target dynamics with the inertia term are in [[04-robotics/force-compliance-control|13. Force & Compliance Control §2]].
- **Admittance control** is the inverse map, from measured force to motion: it integrates the virtual dynamics to get a motion reference $x_c$ and hands $x_c$ to an inner position loop.
$$M_d\ddot x_c+D\,(\dot x_c-\dot x_d)+K\,(x_c-x_d)=F_{ext}$$
  Because the measured force drives the reference, the robot yields where it is pushed.

> [!example] Worked example · 계산 예제
> Impedance with $K=200$ N/m and $D=20$ N·s/m, tool held 1 cm short of its reference ($x_d-x=0.01$ m) and at rest: $F=200\times0.01=2$ N. If the tool is instead being pushed back at $0.05$ m/s ($\dot x_d-\dot x=0.05$), the damper adds $20\times0.05=1$ N, so $F=3$ N. **Non-example**: a stiff PD position loop is formally an impedance with $K=K_p$, but calling it "compliant" is wrong at $K_p=10^5$ N/m, where the same 1 cm asks for 1000 N. The law's structure does not decide compliance; the numbers do.

### 6. Scenario: cleaning a wall

A pure position controller commands the tool 2 cm beyond an estimated wall. A 1 cm wall-location error can cause very different force because contact stiffness is high. **With numbers**: a *compliantly mounted* tool meeting the wall at $K = 10^4$ N/m turns a 1 cm position error into $10^4 \times 0.01 = 100$ N — enough to gouge the surface or trip a force limit — while a 3 cm error would demand 300 N the arm may not even be able to produce. That stiffness is deliberately a soft one; a bare tool on a real arm against steel is up to about one order stiffer — about $10^5$ N/m as the series stiffness of tool, sensor, arm and part — where the same 1 cm error asks for about $10^3$ N and the force diverges long before the error closes. Only a bare indenter on a rigid fixture approaches the $10^7$ N/m material stiffness. The stiffness scale is tabulated in [[04-robotics/force-compliance-control|13. Force & Compliance Control §1]]. Set the *controller's* stiffness to $K = 200$ N/m instead and the same 1 cm error asks for 2 N. That ratio, not any control theory, is why contact tasks are run compliantly. An impedance controller instead permits pose error while shaping the restoring force; a force controller regulates normal force directly but still needs tangential motion and stability handling. The best architecture depends on actuator bandwidth, sensing, surface variation, and safety limits.

### 7. Force, tactile, and material state

- Wrist force/torque sensing measures net wrench but not the full pressure distribution.
- Tactile arrays can estimate contact location, pressure, shear, and slip cues.
- **Proprioception** measures the robot's own state (joint encoders for angles and velocities, motor currents for torque, an IMU for body orientation and acceleration); **exteroception** measures the world outside it (cameras, lidar, depth sensors). A wrist F/T sensor and a tactile skin sit between the two: they are on the robot, but what they report is the external contact.
- Vision can observe global geometry while tactile sensing resolves local contact ambiguity.

What all of these feed is one estimate, and it is worth naming because papers use it without defining it.

> [!info] Definition · 정의 — contact-state estimation
> **What kind of thing it is.** An *estimator*, not a controller and not a sensor: a map from a window of measured signals — wrist wrench, joint torques, tactile array, commanded and measured motion — to the contact's current **mode**, a discrete label, together with the continuous quantities that mode needs (contact location, normal direction, an estimate of $\mu$).
>
> **Its defining conditions.** Two, and dropping either leaves something that is not contact-state estimation. (i) The output includes a **discrete mode** drawn from a stated, finite set — for the running object, $\{\text{free},\ \text{touching and sticking},\ \text{touching and sliding}\}$, which is exactly the list of cases §1's complementarity switches between. (ii) The estimate comes from **measurement**, not from the commanded pose, because the reason the mode is uncertain in the first place is that the panel is not where the model says it is.
>
> $$\hat s_t=\arg\max_{s\in\mathcal{S}}\ p\big(s\mid z_{t-w:t},\,u_{t-w:t}\big)$$
>
> where $\mathcal{S}$ is the declared mode set, $z$ the measurements over a window of $w$ samples, $u$ the commands over the same window, and $\hat s_t$ the chosen mode. The window is in the formula rather than a single sample because sticking and slow sliding produce the same instantaneous force and differ only in how the tangential force moves over time.
>
> **Example.** The running object's own numbers separate the three modes. $f_n\approx0$ N is *free*. $f_n=2$ N with $\lVert f_t\rVert=1$ N and no tangential motion is *sticking*. The same 2 N with the tool moving while $\lVert f_t\rVert$ stays pinned at the $\mu f_n=1$ N bound is *sliding* — the force magnitude is identical in the last two cases, and only the motion, or the fact that $f_t$ has stopped rising, tells them apart.
>
> **Non-example.** "The trajectory says the tool should be 5 mm into the panel, so we are in contact" is not an estimate; it is the command re-labelled, and it will report contact at exactly the moment a mislocated panel guarantees there is none. A bare force threshold is a *detector* of one boundary, not an estimator over a mode set — it cannot report sliding.
>
> **Why it matters.** Every controller in [[04-robotics/force-compliance-control|13. Force & Compliance Control]] is a different set of equations per mode: its §3 selection matrix has to know which directions the contact blocks, and its §5 impact argument only begins once the mode has changed. A claim that a system "handles contact" is a claim about this estimate, whether or not the paper names it.

Rope, cloth, soil, wet concrete, cables, and bulk material have high-dimensional, changing state. Their behavior depends on history and unobserved material properties, making representation and prediction difficult.

### 8. Learning and sim-to-real

Learning may estimate residual dynamics, contact state, friction/material properties, grasp scores, or a tactile-conditioned policy. Domain randomization (training over a distribution of simulator parameters, defined with its objective in [[04-robotics/legged-locomotion|18. Legged Locomotion §2]]) can broaden training conditions, but the chosen randomization distribution defines what variation was covered. Privileged simulator state ([[05-construction-robotics/sim-to-real|Sim-to-Real §2]]) can aid training while being unavailable at deployment; check how the policy replaces it at test time. One pushing task shows all three: a residual-dynamics network learns the difference between the simulator's predicted next state and the real one; domain randomization resamples μ and object mass every episode; and the policy trains with the simulator's exact object pose but must deploy with a pose estimated from the camera.

### 9. Evaluation and paper language

Measure task success, peak/mean force, force-tracking error, slip/drop rate, object or surface damage, recovery, safety violations, and robustness across materials and friction. “Contact-rich,” “compliant,” and “robust” require explicit task and perturbation definitions.

**The four force metrics, defined.** Each is a different kind of number, and each fails in its own way.

- **Peak contact force** $F_{\max}=\max_t\lVert f(t)\rVert$ over the contact episode, in newtons. It is a *sampled* maximum, so it is only as true as the sensor's rate: a 1 kHz channel watching a 1.4 ms impact gets about one sample inside the event ([[04-robotics/force-compliance-control|13. Force & Compliance Control §5]]), and the reported peak can sit far below the real one. **Mean force** over the same interval is the companion number, and reporting only the mean hides exactly what the peak was for.
- **Force-tracking error**, the root-mean-square difference between the commanded and the measured normal force over the contact interval $[0,T]$, in newtons:

$$e_{\mathrm{RMS}}=\sqrt{\frac{1}{T}\int_0^T\big(f_d(t)-f_m(t)\big)^2\,dt}$$

  where $f_d$ is the commanded force, $f_m$ the measured one and $T$ the duration of contact — not of the trial, which is the substitution that flatters a controller by averaging in the free-space seconds. Example on the running object: a commanded $f_d=2$ N measured as $2.0,\ 2.3,\ 1.8,\ 2.1$ N gives errors $0,\ 0.3,\ -0.2,\ 0.1$ N, so $e_{\mathrm{RMS}}=\sqrt{0.035}=0.187$ N, $9.4\%$ of the target, while the mean absolute error is only $0.150$ N. RMS charges the single 0.3 N excursion more heavily, which is why it is the honest one to quote against a force limit.
- **Slip rate** and **drop rate**: the fraction of contact time in which tangential motion occurs while the controller commanded sticking, and the fraction of grasp trials in which the object leaves the hand before the goal. Both are proportions, so both are meaningless without the trial count beside them — and both are measured against a *commanded* intent, which means they presuppose the contact-state estimate of §7.

**Non-example.** A peak force quoted with no sensor rate, an RMS error quoted over the whole trial, or a slip rate quoted without $n$ are three different ways of reporting a number that cannot be compared with anyone else's.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> A higher task success rate does not identify whether the gain came from tactile sensing, better control, safer force limits, or easier contact conditions. Look for matched baselines and ablations across sensing, controller, material, and initialization.

### After reading

- Explain unilateral contact and complementarity qualitatively.
- Interpret the friction-cone inequality and its assumptions.
- Say which way each linearization of the cone errs, and name the coefficient it effectively uses.
- Distinguish form closure from force closure.
- Compare force, impedance, and admittance control.
- Identify what tactile sensing adds beyond wrist force and vision, and state what contact-state estimation has to output.
- Audit material variation and contact-related failure metrics, including what a peak force and an RMS force error each need reported beside them.

> [!tip] Going deeper · 더 깊이
> Mason's *Mechanics of Robotic Manipulation* is the compact classical treatment of contact and friction; Tedrake's [*Robotic Manipulation*](https://manipulation.csail.mit.edu/) covers the same ground with simulators you can run — which matters here, because contact is where simulation and reality diverge first.

### Self-check

1. Why can increasing position gain be dangerous during contact?
2. A tangential force is 6 N, normal force 10 N, and $\mu=0.5$. Is sticking allowed by the simple cone?
3. Why may a policy trained with one friction coefficient fail even with perfect perception?
4. What should a tactile-policy ablation hold constant?
5. A planner reports that its grasp has friction margin to spare. It constrained each contact with the outer box pyramid. Which way is its margin wrong, and by how much at the corner?
6. A system logs "in contact" whenever the commanded pose is past the surface. Which of the two defining conditions of contact-state estimation does that fail, and what will it report at the worst possible moment?

> [!tip]- Answers
> 1. Small pose/model errors can generate large forces and instability.
> 2. No: $6>0.5\times10=5$ N.
> 3. Feasible forces, slip transitions, and dynamics change.
> 4. Demonstrations, architecture capacity, controller, initialization, materials, and evaluation protocol; remove or replace tactile information without making the rest easier.
> 5. Optimistically wrong. The box pyramid contains the true cone, so it authorises tangential forces that slip; at the corner it allows $\sqrt2$ times the real bound, $41.4\%$ too much. The inner polyhedral cone errs the other way and would have understated the margin instead.
> 6. Condition (ii): the estimate must come from measurement, not from the command. It will report contact exactly when a mislocated panel guarantees there is none — the case the estimate existed for.

### Problem set · 과제

Tier B. The running object with **two entries changed**: the commanded penetration becomes $\delta=8\,\mathrm{mm}$, and dust on the panel drops the friction coefficient to $\mu=0.35$. Everything else — **P2** at $\theta=(0^\circ,90^\circ)$, the panel at $x=1\,\mathrm{m}$, $k_w=400\,\mathrm{N/m}$, $m_p=1.0\,\mathrm{kg}$, the 10 N two-finger squeeze at $\pm0.05\,\mathrm{m}$ — is unchanged ([[02-foundations/lab-plants|0.6]]). Using only this page, its prerequisites and the object catalog. No simulator.

1. **Draw.** Both panels of the homework diagram at the new numbers. On the right-hand panel the three closed curves must now be drawn for $\mu=0.35$ at the new $f_n$, and the 1 N wipe arrow drawn to the same scale — the drawing has to show which of the three sets contains it.
2. **Derive.** (a) $f_n$ at rest at $\delta=8\,\mathrm{mm}$. (b) The cone half-angle and the largest tangential force that can stick. (c) Does the $1\,\mathrm{N}$ wipe still stick, and with what margin? (d) The effective coefficient of the four-generator inner cone, and the largest wipe *it* would authorise. (e) The squeeze the two fingers now need to hold the panel, and what the unchanged 10 N squeeze can carry.
3. **Interpret.** Two failures are available here — the wipe slipping and the panel dropping — and only one of them has happened. Which one, and why did the same $30\%$ loss of $\mu$ move the two bounds in opposite directions? Name the one measurement that would have told you before the panel hit the floor, and say which section of this page defines it.

> [!tip]- Solutions
> 1. Same two panels. The cone is now narrower ($19.3^\circ$ instead of $26.6^\circ$) but the circle on the tangent plane is *larger*, because $f_n$ rose faster than $\mu$ fell. The four-generator square's corners still sit on the circle; the box pyramid's square still circumscribes it.
> 2. (a) $f_n=400\times0.008=3.20\,\mathrm{N}$ at rest; add $d_c\dot\delta$ only while still closing. (b) $\arctan0.35=19.29^\circ$, and $\lVert f_t\rVert\le0.35\times3.20=1.12\,\mathrm{N}$. (c) Yes: $1.00<1.12$, a margin of $0.12\,\mathrm{N}$, so the wipe uses $89.3\%$ of the bound — it went from exactly on the bound to just inside it, because the deeper press bought more friction than the dust took away. (d) $\mu\cos(\pi/4)=0.35\times0.7071=0.2475$, allowing only $0.2475\times3.20=0.792\,\mathrm{N}$: the conservative model *rejects* the very wipe the real contact carries. (e) $f\ge m_pg/(2\mu)=9.81/0.70=14.01\,\mathrm{N}$, while the unchanged 10 N squeeze carries $2\times0.35\times10=7.00\,\mathrm{N}$ — $2.81\,\mathrm{N}$ short of the panel's $9.81\,\mathrm{N}$ weight.
> 3. The panel drops; the wipe is fine. Both bounds are $\mu f_n$ and both lost the same $30\%$ of $\mu$, but the wipe's normal force was raised by the command from $2.00$ to $3.20\,\mathrm{N}$ — a $60\%$ gain that more than paid for the dust, $1.6\times0.7=1.12$ — while the grip's normal force is fixed by the squeeze and got no such compensation, $1.0\times0.7=0.70$. The lesson is that a friction margin is a margin in the *product* $\mu f_n$, and only one of the two contacts had someone pushing harder. The measurement that would have caught it is contact-state estimation (§7): the fingers sliding while the controller commanded sticking is a mode change, visible in the tangential force pinned at its bound, and it happens before the panel leaves the hand. A camera watching the panel's pose sees nothing until it is already falling.

### Sources

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation (Tedrake) — force control & contact chapters](https://manipulation.csail.mit.edu/)
- [Modern Robotics course wiki — ch. 12 videos & software](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)

## 한국어

*E군이고 그 안의 유일한 페이지다 — H군 전체가 여기서 갈라져 나오기 때문이다. [[02-foundations/linear-algebra|선형대수]]·최적화와
[[04-robotics/modern-robotics/index|MR 챕터 요약]] 위에 선다. 로봇이 무언가에 닿는 순간 기하만으로는 부족해지는 지점이 여기다.*

> [!tip] 접촉을 감지하는 것에서 표현하는 것으로
> 이 페이지는 로봇 쪽의 접촉을 다룬다. 그 접촉 cue를 사람에게 표현해야 할 때는 [[04-robotics/haptics-teleoperation/tactile-display-design|Tactile Display Design]]으로, 가상 벽이나 힘 반영 루프가 안정해야 할 때는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|Rendering, Sampling & Stability]]로 이어 읽는다.


로봇이 세계에 닿는 순간 기하만으로는 부족하다. 접촉은 힘, 마찰, 충격, 모드 전환, 변형,
불확실성을 끌고 들어온다. 이 효과들은 파지, 조립, 굴착, 닦기, 천공, 유연 재료 취급의
중심에 있다.

> [!info] 깊이 목표
> 접촉이 많은(contact-rich) 매니퓰레이션 논문에서 접촉 모델, 센싱, 제어 모드, 재료 가정,
> 평가를 짚어내며 읽는다. Complementarity 솔버와 연속체 역학의 세부는 선택적
> 실무/숙달 주제다.

> [!note] 선수 지식
> [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/optimization|최적화]] · [[04-robotics/modern-robotics/ch05-velocity-kinematics|정역학과 야코비안]] · [[04-robotics/modern-robotics/ch08-dynamics|동역학]] · [[04-robotics/modern-robotics/ch12-grasping|파지]]

> [!note] 처음이라면 · First pass
> 먼저 아래의 계속 쓰는 대상과 계산 예제를 읽어라. 이 페이지가 갚아야 할 계산 하나이고, "접촉이 있기는 한가"에서 "그 파지가 버티는가"까지 이어진다. 그다음 §1(접촉이 애초에 문제를 왜 바꾸는가), 그다음 §5(위치·힘·임피던스·어드미턴스), 그다음 그 넷을 한 과제에 넣어 보는 §6의 벽 닦기. §2~§4는 역학이고, 논문의 마찰이나 closure 주장이 중요해질 때 읽어라.

### 계속 쓰는 대상: P3 강성 패널을 미는 P2 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2** — 평면 2R 팔, $L_1=L_2=1\,\mathrm{m}$ — 를 고정 자세 $\theta=(0^\circ,90^\circ)$에 두면 말단이 $(1,1)\,\mathrm{m}$에 있고, 거기 달린 공구가 평평한 패널을 민다. 패널 면은 평면 $x=1\,\mathrm{m}$이라 이 자세에서 말단이 정확히 닿고, 강성은 **P3**의 벽 값을 쓴다. 카탈로그의 로보틱스 관통 과제 — *도구를 패널까지 옮겨 힘을 조절하며 접촉한다* — 를 패널을 세워 놓고 하는 판본이고, 여기서 묻는 것은 마찰이다. 같은 팔과 공구로 패널을 말단 아래에 눕혀 놓고 운동과 힘의 관계를 묻는 쪽은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $\hat n$ | $+x$ | 접촉 법선, 패널 **안쪽**을 양으로 센다 |
| $\hat t_1,\ \hat t_2$ | $-y$, $+z$ | 패널 면 안의 두 접선 방향 |
| $k_w$ | $400\,\mathrm{N/m}$ | 패널 강성 — P3의 가상 벽 값 |
| $d_c$ | $4\,\mathrm{N\cdot s/m}$ | §3 페널티 모델의 접촉 감쇠 — 이 페이지가 P3에 더하는 유일한 값 |
| $\mu$ | $0.5$ | 공구-패널 마찰 계수 |
| $\delta$ | $5\,\mathrm{mm}$ | 면보다 안쪽으로 명령한 침투량 |
| $\dot\delta$ | $0.02\,\mathrm{m/s}$ | 처음 닿는 순간의 접근 속도 |
| $m_p$ | $1.0\,\mathrm{kg}$ | 패널 자체의 질량, §4에서 들어 올릴 때 쓴다 |
| $g$ | $9.81\,\mathrm{m/s^2}$ | 중력, $-y$ 방향 |

P2가 평면인데도 접선을 둘 두는 이유: 움직이는 것은 *팔*이지만 *접촉*은 3차원이고 §2의 원뿔도 3차원 원뿔이다. 접선 하나로 줄이면 선형화 문제 전체가 사라지는데, 접촉 문헌의 최적화기 절반이 바로 거기에 산다.

*범위: 이 페이지는 접촉 하나의 역학을 가르친다 — 언제 접촉이 존재하는가, 그 접촉이 얼마나 되는 힘을 견디는가, 그 힘이 어떻게 물체 렌치가 되는가, closure가 무엇을 보장하고 무엇을 보장하지 않는가 — 그리고 접촉이 많은 논문의 센싱과 평가를 읽는 법을 가르친다. 그 접촉에 어떤 제어기를 고를지([[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]), 파지를 어떻게 계획하고 채점할지([[04-robotics/grasping|파지]]), 촉각 신호를 사람에게 어떻게 되돌려 줄지([[04-robotics/haptics-teleoperation/tactile-display-design|24.2 촉각 디스플레이 설계]]), 접촉 시뮬레이터의 솔버를 어떻게 만드는지([[06-research-practice/simulators-benchmarks-datasets|시뮬레이터·벤치마크·데이터셋]])는 가르치지 않는다.*

### 과제가 그릴 그림: 패널 위의 접촉 프레임과 그 위에 선 원뿔 · Homework diagram

한 번 그려 두면 과제는 같은 그림을 다른 숫자로 묻는다.

**왼쪽 — 팔과 패널, $x$–$y$ 평면, 실제 비율.** 원점에 P2 베이스, 링크 1이 $+x$로 뻗어 엘보가 $(1,0)$, 링크 2가 올라가 말단이 $(1,1)$. $x=1$에 패널 면의 수직선을 긋고 패널을 직사각형으로 걸어 둔다. 말단에 접촉 프레임: $\hat n$은 $+x$로 면 안쪽, $\hat t_1$은 $-y$로 닦는 방향. 말단과 면 사이에 $k_w=400$ N/m이라고 적은 스프링 기호를 $\delta=5$ mm만큼 눌린 모습으로 그리되 — 비율보다 훨씬 크게 그리고 그렇게 그렸다고 적어 둔다. 1 m짜리 팔에서 5 mm는 눈에 보이지 않는다.

**오른쪽 — 접촉 프레임 안의 원뿔.** 법선 축 $\hat n$을 세로로, 접선 평면 $(\hat t_1,\hat t_2)$을 가로로. 위로 열린 원형 원뿔의 반각 $\arctan\mu=26.6^\circ$를 각으로 표시한다. 접선 평면 위에는 닫힌 곡선 셋을 동심으로 그린다. 반지름 $\mu f_n$인 참 원, 그 바깥으로 네 점에서 원에 접하는 **외접 상자 피라미드**의 정사각형, 그 안쪽으로 네 꼭짓점이 원 *위에* 놓이는 4-생성자 내접 원뿔의 정사각형. 명령한 닦기 힘을 실제 길이의 화살표 하나로 그려서 셋 중 어느 집합이 그것을 포함하는지 눈으로 보이게 한다.

**아래 — 간극 축.** $\phi$에 대한 수평선을 긋고 0을 표시한다. 0의 왼쪽($\phi>0$, 떨어짐)에는 $f_n=0$, $\phi=0$과 그 오른쪽에는 $f_n\ge0$이라고 적는다. 점 둘: 닿기 전 $\phi=+2$ mm, 그리고 §3의 페널티 모델은 허용하고 §1의 강체 모델은 금지하는 침투 $\phi=-5$ mm. 쌍 $(\phi,f_n)$은 결코 두 반직선을 벗어나지 못한다 — 그 그림이 곧 complementarity다.

### 대상으로 한 번 끝까지: 간극에서 파지 여유까지 · Worked case

위의 대상에서 여섯 단계를 밟는다. 각 단계는 제목에 적은 절이 증명한다. 여기 모든 숫자를 과제에서 표의 항목 두 개만 바꿔 다시 계산한다.

**1단계 — 접촉이 있기는 한가? (§1).** 공구를 면에서 2 mm 앞에 두면 $\phi=0.002$ m, $f_n=0$ N이므로 $\phi f_n=0$이고 쌍은 왼쪽 반직선 위에 있다. 면까지 몰면 $\phi=0$이고, 이제 $f_n$은 음이 아니기만 하면 무엇이든 될 수 있다 — 모델이 힘을 예측하기를 그만두고 제약하기만 시작한 것이다. 그 전환이 어려움의 전부다. 두 경우가 서로 다른 방정식 묶음이므로, 어느 쪽인지 정하는 값은 명령이 아니라 *측정*이다.

**2단계 — 법선력은 얼마인가? (§3).** 강체 모델은 $\phi=0$에서 $f_n\ge0$만 말하므로 답할 수 없다. $\delta=5$ mm 안쪽을 명령하면 강체 모델은 실행 불가능해지니, 비침투를 스프링과 맞바꾸는 페널티 모델을 쓴다.

$$f_n=k_w\,\delta+d_c\,\dot\delta=400\times0.005+4\times0.02=2.00+0.08=2.08\ \mathrm{N}$$

정지하면 패널이 받는 힘은 $f_n=2.00$ N이고, 나머지 $0.08$ N은 공구가 $0.02$ m/s로 아직 다가오는 동안에만 있다. 이 2 N을 붙들어 두자. 아래의 모든 경계가 여기에 비례한다.

**3단계 — 닦는 힘은 얼마까지 견디는가? (§2).** 원뿔의 반각은 $\arctan 0.5=26.5651^\circ\to26.6^\circ$이고, $f_n=2.00$ N에서 허용하는 것은

$$\lVert f_t\rVert\le\mu f_n=0.5\times2.00=1.00\ \mathrm{N}$$

아래로 3 N 닦기는 경계의 세 배라 공구가 미끄러지고 마찰이 $f_t$를 미끄럼 반대 방향 $-1.00$ N에 고정한다. 1 N 닦기는 경계 *위에 정확히* 놓인다. 허용되지만 여유는 0이다. "고착한다"의 정직한 독법이 이것이다. 모델이 허락할 뿐, $\mu$가 1%만 달라져도 버틴다는 말은 모델 어디에도 없다.

**4단계 — 솔버는 무엇을 믿어도 되는가? (§2, 선형화).** QP로 남아야 하는 최적화기는 원을 면들로 바꾸는데, 표준적인 두 대체가 서로 반대 방향으로 틀린다. 이 접촉에서 외접 상자 피라미드의 모서리는 $\lVert f_t\rVert=\sqrt{1.00^2+1.00^2}=1.414$ N으로 참 경계보다 $41.4\%$ 크다 — 미끄러질 닦기를 허가해 준다. 4-생성자 내접 원뿔은 $\mu\cos(\pi/4)\times f_n=0.354\times2.00=0.707$ N까지만 허용해 쓸 수 있는 마찰의 $29.3\%$를 버린다 — 실제 접촉이 허용하는 1 N 닦기를 거절한다. 생성자를 여덟으로 늘리면 손실이 $7.6\%$($0.924$ N), 열여섯이면 $1.9\%$($0.981$ N)로 줄어든다.

**5단계 — 같은 접촉을 물체 렌치로 (§4).** 패널 프레임 원점을 접촉에서 $0.40$ m 아래인 브래킷에 두면 $r=(0,0.40,0)$ m이고, 1 N 닦기를 포함한 접촉력은 $f=(2.00,-1.00,0)$ N이다. 그러면 $m=r\times f=(0,0,-0.80)$ N·m이므로

$$\mathcal{F}=\begin{pmatrix}m\\ f\end{pmatrix}=(0,\ 0,\ -0.80,\ 2.00,\ -1.00,\ 0)$$

이고, 패널은 아무도 명령하지 않은 $z$축 둘레 0.80 N·m 비틀림을 느낀다. 그것이 생긴 이유는 원점을 $0.40$ m 옮겼기 때문이고 물리적 밀기는 그대로다. 원점을 접촉으로 옮기면 모멘트는 0이 된다.

**6단계 — 그다음 패널을 들어야 하는 파지 (§4).** 손가락 둘이 1.0 kg 패널을 $\pm0.05$ m에서 각각 10 N으로 조인다. 각 원뿔이 $\mu\times10=5$ N의 접선력을 허용하므로 둘이 합쳐 $2\times5=10.0$ N을 버티고, 무게는 $m_pg=1.0\times9.81=9.81$ N이다. 여유는 $0.19$ N, 곧 하중의 $1.9\%$다. 같은 말로, 파지가 딱 버티는 마찰 계수는

$$\mu^\star=\frac{m_pg}{2f}=\frac{9.81}{2\times10}=0.4905$$

이므로 명목값 $\mu=0.5$는 $1.9\%$ 차이로 넘긴다. 먼지가 $\mu$를 $0.40$으로 떨어뜨리면 버티는 힘이 8.0 N이 되어 무게보다 1.81 N 모자라고, 패널은 바닥으로 간다.

**여섯 단계를 합치면.** 닦기의 여유는 정확히 0이고 파지의 여유는 $1.9\%$인데, *두 경계 모두 같은 $\mu$에서 나온다* — 측정한 적 없이 가정한 수이고, 카메라 속 패널을 1픽셀도 움직이지 않으면서 먼지가 바꾸는 수다. 이 페이지의 모든 양은 제어기가 정하는 $f_n$에 비례하거나, 아무도 관측하지 않은 $\mu$에 비례한다. §7은 그 틈을 측정으로 메우는 이야기이고, §9는 접촉 주장이 뜻을 가지려면 논문이 무엇을 보고해야 하는지에 관한 이야기다.

### 1. 접촉이 문제를 바꾸는 이유

접촉은 보통 **단방향**(unilateral)이다: 물체는 밀 수 있지만 평범한 표면을 통해 당길 수는
없다. 운동은 분리·충격·고착(sticking)·미끄럼(sliding) 사이를 오간다. 그래서 동역학이
하이브리드가 되고 대개 비매끄럽다.

$\phi(q)$를 **간극**이라 하자. 로봇과 물체가 구성 $q$에 있을 때 두 표면의 가장 가까운 두 점 사이 거리이고(탁자 위 손끝이라면 그냥 탁자 위 높이), 떨어져 있으면 양수, 닿으면 0이다. 실제로는 충돌 기하 라이브러리가 두 형상과 자세로부터 계산한다. 간극 $\phi(q)\ge 0$와 법선력 $f_n\ge 0$에 대해 이상적 강체 접촉은

$$\phi(q)f_n=0$$

으로 요약된다. 떨어져 있으면 힘이 0이고, 법선력이 양수면 간극이 닫혀 있다. 이
complementarity는 이상화된 모델이지 재료 변형의 문자 그대로의 기술이 아니다.

**강체 단방향 접촉의 세 조건.** 이 모델은 두 스칼라, 곧 간극 $\phi(q)$와 법선력 $f_n$(접촉 법선 방향의 힘 성분으로, 두 표면이 서로 밀어낼 때 양수)에 대한 조건들의 묶음이다. 세 조건이 모두 성립할 때 **상보성 조건**(complementarity condition)을 만족한다고 한다.

- **비침투**: 두 물체는 겹치지 않으므로 간극이 음수일 수 없다.
$$\phi(q)\ge 0$$
- **단방향성**: 표면은 밀 수만 있고 당길 수 없으므로 법선력이 음수일 수 없다.
$$f_n\ge 0$$
- **상보성**: 힘은 닫힌 간극을 통해서만 작용하므로 둘 중 많아야 하나만 0이 아니다.
$$\phi(q)\,f_n=0$$

셋을 한데 묶어 $0\le\phi(q)\perp f_n\ge 0$로 쓰고, $\perp$는 "곱이 0"이라는 뜻이다. 떨어져 있고 $f_n=0$인 경우와 닿아 있고 $f_n\ge0$인 경우가 서로 다른 방정식 묶음이므로 동역학이 **접촉 모드** 사이를 전환하고, 이것이 접촉을 하이브리드·비매끄럽게 만든다. 접촉점마다 이 조건을 쌓으면 시뮬레이션 한 스텝이 **선형 상보성 문제**(LCP: $w=Mz+q\ge0$, $z\ge0$, $z^\top w=0$인 $z$를 찾는 문제)가 되고, 강체 시뮬레이터가 푸는 것이 이 형태다([[06-research-practice/simulators-benchmarks-datasets|시뮬레이터·벤치마크·데이터셋]]).

> [!example] 계산 예제 · Worked example
> 탁자 위 2 mm에 들고 있는 0.1 kg 블록은 $\phi=0.002$ m, $f_n=0$이므로 $\phi f_n=0$ ✓. 내려놓고 정지하면 $\phi=0$, $f_n=mg=0.1\times9.81=0.981$ N이고 역시 $\phi f_n=0$ ✓.
> **반례**: $\phi=0.001$ m에서 $f_n=0.5$ N은 상보성 위반(열린 간극을 가로지르는 힘), $f_n=-0.5$ N은 단방향성 위반(탁자가 블록을 끌어당김), $\phi<0$은 비침투 위반이다. 페널티 모델(§3)은 마지막 것을 일부러 허용한다.

### 2. 법선력과 마찰

Coulomb 마찰은 흔히

$$\lVert f_t\rVert\le \mu f_n$$

로 근사한다. $f_n$은 법선력, $f_t$는 접선력, $\mu$는 마찰 계수다. 마찰 원뿔 안의 힘은
고착과 양립할 수 있고, 경계·초과 조건은 이 모델 아래 임박한·실제의 미끄럼을 나타낸다.
원뿔은 *힘의 실행 가능성 경계*다 — 실제로 고착하는지 미끄러지는지는 상대 운동과 접촉
법칙에도 의존한다.
실제 마찰은 재료, 속도, 압력, 마모, 표면 상태에 의존한다.

**마찰 원뿔과 Coulomb 법칙, 부분마다 이름을 붙여.** 접촉력 $f\in\mathbb{R}^3$를 법선 성분 $f_n$(단위 법선 방향의 스칼라)과 접선 성분 $f_t\in\mathbb{R}^2$(접촉 평면 안)로 나누고, 그 평면 안의 상대 미끄럼 속도를 $v_t$라 하자. **마찰 원뿔**은 모델이 허용하는 접촉력의 집합이다.

$$FC=\{\,f:\ f_n\ge 0,\ \lVert f_t\rVert\le\mu f_n\,\}$$

그래서 조건은 둘이다. **단방향성**($f_n\ge0$, §1과 같음)과 **Coulomb 경계**($\lVert f_t\rVert\le\mu f_n$). 이 경계는 접선 대 법선의 비가 $\mu$가 될 때까지 힘이 법선에서 기울 수 있다는 뜻이므로, 원뿔은 법선을 축으로 반각 $\arctan\mu$인 원형 원뿔이다. **Coulomb 법칙**은 여기에 힘이 어느 경계에 놓이는지를 더한다.

- **고착**($v_t=0$): $FC$ 안의 어떤 $f$든 허용되고, $f_t$는 접촉을 멈춰 두는 데 필요한 값이 된다.
- **미끄럼**($v_t\ne0$): 마찰은 에너지를 소산하므로 힘은 원뿔 표면에 놓이고 미끄럼과 반대 방향이다.
$$f_t=-\mu f_n\,\frac{v_t}{\lVert v_t\rVert}$$

많은 모델이 고착 경계에는 더 큰 정지 마찰 계수 $\mu_s$를, 미끄러지는 동안에는 더 작은 운동 마찰 계수 $\mu_k$를 쓴다. $\mu$ 하나만 쓰면 둘이 같다고 가정한 것이다.

**선형화한 마찰 원뿔, 그리고 어느 쪽으로 틀리는가.** 경계 $\lVert f_t\rVert\le\mu f_n$은 *2차* 원뿔이다. 제약이 노름이지 선형 부등식들이 아니다. 그래서 이차계획법이 필요한 최적화기는([[02-foundations/optimization|4. 최적화 §5]]) 이것을 **다면 원뿔**(polyhedral cone), 곧 유한한 개수의 평평한 면으로 둘러싸인 원뿔로 바꾼다. 표준적인 대체가 둘이고, 둘은 서로 반대쪽에서 근사하며, 양쪽을 모두 "마찰 피라미드"라고 부르는 순간 오차의 방향이 사라진다.

- **외접 상자 피라미드**는 접선 축을 하나씩 따로 묶는다. $|f_{t,1}|\le\mu f_n$, $|f_{t,2}|\le\mu f_n$ — 축마다 두 면씩 네 면이다. 참 원뿔을 **포함하므로** 미끄러질 힘까지 허용한다. $f_n=2$ N, $\mu=0.5$에서 모서리는 $\lVert f_t\rVert=\sqrt{1^2+1^2}=1.414$ N이라 참 경계 1 N보다 $41.4\%$ 후하다. [[04-robotics/convex-mpc-legged|8. Convex MPC]]가 네 번째 모델링 수에서 쓰는 형태가 이것이고, 계수를 $\mu/\sqrt2$로 줄이는 것이 그 페이지가 오차를 되사는 방법이다.
- **내접 다면 원뿔**은 대신 법선 둘레에 고르게 놓인 $m$개의 생성자 반직선으로 *생성*되며, 각 반직선은 참 원뿔의 표면 위에 있다.

$$f=\sum_{j=1}^{m}\lambda_j\,g_j,\qquad \lambda_j\ge0,\qquad g_j=\hat n+\mu\left(\cos\tfrac{2\pi j}{m}\,\hat t_1+\sin\tfrac{2\pi j}{m}\,\hat t_2\right)$$

  여기서 $\lambda_j$는 반직선 $j$에 걸리는 음이 아닌 가중치이고 $m$은 모델러가 고르는 면의 수다. 생성자가 원뿔 위에 있고 원뿔이 볼록하므로 그들의 음이 아닌 결합은 원뿔을 벗어날 수 없고, 따라서 이 집합이 허용하는 힘은 모두 참 원뿔 **안**에 있다. 대가는 버리는 마찰이다. 내접 다각형의 내접원 반지름 때문에 유효 계수가 $\mu\cos(\pi/m)$이 되어, $m=4$에서 $0.354$(경계의 $29.3\%$를 버림), $m=8$에서 $0.462$($7.6\%$), $m=16$에서 $0.490$($1.9\%$)이다.

$m=4$에서는 내접 원뿔의 계수 $\mu\cos(\pi/4)$와 줄인 상자의 $\mu/\sqrt2$가 같은 수 $0.354$가 된다. 두 구성이 그렇게 쉽게 헷갈리는 이유다. 그래도 집합은 서로 다르고, 요점은 오차의 방향이다. **외접은 파지에 낙관적이고 내접은 비관적이며, 둘 다 원뿔은 아니다.** 어느 쪽을 풀었는지가, 그 계획기가 버틸 수 없는 접촉을 약속하는지 버틸 수 있는 접촉을 거절하는지를 정한다.

> [!example] 계산 예제 · Worked example
> $\mu=0.5$이면 반각은 $\arctan0.5=26.6°$다. $f_n=10$ N이면 원뿔은 $\lVert f_t\rVert\le5$ N을 허용한다. 4 N 접선 하중은 고착할 수 있고, 6 N 요구는 그럴 수 없다(스스로 점검 2).
> **계속 쓰는 대상에서는** 같은 계산이 $f_n=2$ N에서 돌아가고, 위의 계산 예제 3·4단계에 끝까지 적혀 있다 — 각 선형화가 대신 무엇을 허용했을지까지.
> **반례**: $f_n=-2$ N은 $f_t$가 아무리 작아도 어떤 $\mu$에서든 원뿔 밖이다. 표면은 당길 수 없기 때문이다. 그리고 원형 원뿔은 위의 두 다면 원뿔 어느 쪽과도 같은 집합이 아니다. 솔버가 보고하는 마찰 여유가 제 면에 대한 여유인 이유가 그것이다. 파지 해석이 이 원뿔 위에 서는 방식은 [[04-robotics/grasping|파지 §2]]에 있다.

<svg viewBox="0 0 440 214" style="max-width:100%;height:auto" role="img" aria-label="마찰 원뿔: 안쪽 힘은 고착, 바깥 힘은 미끄럼">
  <defs><marker id="fcA" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.6"><line x1="30" y1="150" x2="410" y2="150"/></g>
  <g fill="currentColor" opacity="0.10"><path d="M150,150 L96,36 L204,36 Z"/></g>
  <g stroke="currentColor" stroke-width="1.5" fill="none"><path d="M150,150 L96,36"/><path d="M150,150 L204,36"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.6"><line x1="150" y1="150" x2="150" y2="30"/></g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.75"><path d="M150,95 A55,55 0 0 1 175.9,101.1"/></g>
  <g stroke="currentColor" stroke-width="2" fill="none">
    <path d="M150,150 L172,72" marker-end="url(#fcA)"/>
    <path d="M150,150 L252,92" marker-end="url(#fcA)"/>
  </g>
  <g fill="currentColor"><circle cx="150" cy="150" r="3.5"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="138" y="24">f_n</text>
    <text x="215" y="60">원뿔 안: 고착 가능</text>
    <text x="264" y="100">바깥: 미끄러짐</text>
    <text x="30" y="172">표시된 각이 원뿔의 반각 = arctan(mu)</text>
    <text x="30" y="192" opacity="0.85">원뿔은 힘의 경계일 뿐 운동의 보장이 아니다 &#8212;</text>
    <text x="30" y="208" opacity="0.85">실제로 고착하는지는 접촉 법칙에도 달려 있다</text>
  </g>
</svg>

법선 지지가 부족한 상태에서 접선 요구가 커지면 가정한 고착 영역을 벗어날 수 있어 이 부등식이 유용하다. 잡은 패널의 먼지는 시각적 자세를 거의 바꾸지 않고 마찰을 바꿀 수 있다. μ를 안다고 취급하는 계획기는 접촉 여유를 과대평가할 수 있다. **여기서 얻는 독법.** μ를 어떻게 얻고 물체를 놓치기 전에 미끄러짐 피드백으로 잘못된 가정을 고칠 수 있는지 묻는다. 힘 경계는 가능한 실패 기전을 설명하지만 실제 접촉 상태의 관찰을 대신하지는 않는다.

### 3. 강체 모델과 유연 모델

| 모델 | 유용한 경우 | 주된 한계 |
|---|---|---|
| 강체 접촉 | 변형이 과제 스케일 대비 작을 때 | 충격·모드 전환이 비매끄러움 |
| 페널티/유연 접촉 | 시뮬레이션에 연속적 침투력이 필요할 때 | 강성·감쇠의 동정이 어려움 |
| 학습/잔차 모델 | 반복 가능한 불일치가 데이터에 남을 때 | 외삽과 물리적 일관성 |

**페널티 모델을 풀어 쓰면.** 페널티(유연) 접촉은 §1의 비침투 조건을 버리고, 두 물체가 작은 **침투 깊이** $\delta=\max(0,-\phi)$만큼 겹치게 둔 뒤 스프링과 댐퍼처럼 되민다.

$$f_n=\max\!\big(0,\ k\,\delta+d\,\dot\delta\big)$$

$k$(접촉 강성, N/m)는 주어진 겹침이 만드는 힘의 크기를, $d$(접촉 감쇠, N·s/m)는 겹침 속도 $\dot\delta$에 대한 저항을 정하고, 모델이 절대 당겨서는 안 되므로 바깥의 $\max$가 단방향성을 지킨다. 예: $k=10^4$ N/m, 정지 상태 1 mm 겹침이면 $f_n=10^4\times0.001=10$ N이다. 강체 모델이 전환하는 곳에서 연속적이라 시뮬레이터가 선호하고, 그 대가는 $k$와 $d$가 측정된 재료 상수가 아니라 수치적 선택이라는 점이다. **학습 잔차**는 $x_{t+1}=f_{\text{phys}}(x_t,u_t)+r_\theta(x_t,u_t)$ 꼴이다. $f_{\text{phys}}$는 물리 모델의 예측, $r_\theta$는 파라미터 $\theta$로 맞춘 보정이다.

시뮬레이터의 접촉 파라미터는 대개 수치적 타협이다. 한 시뮬레이터 설정에서의 성공이
실제 재료 변동에 대한 강건성의 증거는 아니다.

겉보기 제어 개선이 더 관대한 시뮬레이션 접촉에서 올 수 있어 모델 선택이 중요하다. 순응적인 벽은 단단한 표면에서 힘 급증을 만들 닦기 경로 오차를 흡수할 수 있다. 학습 잔차(물리 기반 모델이 설명하지 못하고 남긴 실제 동역학의 몫에 맞춘 모델)는 반복 불일치를 고치지만 학습 관측이 보정을 제약하는 범위 안에서만 근거가 있다. **여기서 얻는 독법.** 접촉 법칙, 파라미터 식별, 수치 설정을 나눈다. 편한 설정 하나의 성공보다 관련 물리 반응과의 검증을 찾는다.

### 4. 파지와 렌치의 언어

접촉력은 물체에 힘과 모멘트를 만들고, 이 둘을 한 벡터로 쌓은 것이 렌치다(**wrench**, [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장]]에서 정의). **Grasp map**은 모든 접촉력을 더해 물체 렌치 하나로 만드는 행렬이다. 그 위에 두 가지 닫힘 개념이 선다.

- **Form closure**는 명시된 접촉 모델 아래 기하만으로 물체를 고정한다.
- **Force closure**는 허용 접촉력(대개 마찰 포함)으로 임의 외부 렌치에 저항한다.

필요한 접촉 수는 차원, 마찰·접촉 가정, 일반 위치 조건에 의존한다. 일반 위치 조건이란 접촉 법선들이 우연히 한 줄로 늘어서는 것 같은 퇴화한 배치가 없다고 가정한다는 뜻이다.

**접촉 하나의 렌치부터 만든다.** 물체 원점에서 변위 $r$인 곳에 힘 $f$가 가해지면 모멘트는 $r\times f$다. 원점을 옮기면 같은 물리적 밀기라도 모멘트 좌표가 달라진다. 힘과 모멘트를 더하기 전에 모든 접촉을 같은 프레임으로 표현해야 한다. 그렇지 않으면 파지 사상이 서로 맞지 않는 양을 합친다.

**렌치, grasp map, 두 닫힘을 식으로.**

- **렌치**는 모멘트 $m\in\mathbb{R}^3$을 힘 $f\in\mathbb{R}^3$ 위에 쌓은 6차원 벡터다(Modern Robotics의 순서). 물체 프레임의 점 $r$에 힘이 가해지면 모멘트는 프레임 원점에 대해 잰다.
$$\mathcal{F}=\begin{pmatrix}m\\ f\end{pmatrix}=\begin{pmatrix}r\times f\\ f\end{pmatrix}\in\mathbb{R}^6$$
  예: $r=(0.2,0,0)$ m에 $f=(0,0,-10)$ N이면 $m=r\times f=(0,2,0)$ N·m이다. 물체는 아래로 10 N과 $y$축 둘레 2 N·m 비틀림을 느낀다.
- **Grasp map** $G$는 점접촉 $k$개의 렌치를 더한다. 접촉력을 모두 물체 프레임으로 표현해 $f_c=(f_1,\dots,f_k)\in\mathbb{R}^{3k}$로 쌓으면, 각 열 블록 $G_i$가 $f_i$를 그 렌치로 바꾸므로
$$\mathcal{F}_{\text{obj}}=G\,f_c=\sum_{i=1}^{k}\begin{pmatrix}r_i\times f_i\\ f_i\end{pmatrix}$$
  이고 $G$는 $6\times3k$ 행렬이다. 힘에 대해 선형이므로 닫힘 질문이 원뿔과 생성(span)의 질문이 된다.
- **Force closure**: 모든 외부 렌치 $\mathcal{F}_{\text{ext}}$에 대해 그것을 상쇄하는 허용 접촉력이 있다. 허용이란 각 $f_i$가 자기 마찰 원뿔 $FC_i$(§2) 안에 있다는 뜻이다.
$$\forall\,\mathcal{F}_{\text{ext}}\in\mathbb{R}^6\ \ \exists\, f_i\in FC_i:\quad G\,f_c=-\mathcal{F}_{\text{ext}}$$
  원뿔은 양의 배율에 닫혀 있으므로, 이는 원뿔들의 $G$에 의한 상이 $\mathbb{R}^6$ 전체라는 말과 같다.
- **Form closure**(1차): 같은 명제를 **마찰 없는** 접촉으로 쓴 것이다. 각 $f_i=\lambda_i n_i$이고 $\lambda_i\ge0$, $n_i$는 안쪽 법선이다. 법선 렌치들이 $\mathbb{R}^6$을 양의 계수로 생성해야 한다(모든 렌치가 그것들의 음이 아닌 결합). 평면에서 최소 4개, 공간에서 최소 7개의 접촉이 필요하고, 그 개수와 단서는 [[04-robotics/grasping|파지 §3]]에 있다.

두 손가락이 패널을 조이는 상황을 보자. 반대 방향 힘은 합성 물체 렌치가 0이어도 접촉의 압축 예압을 유지할 수 있다. 그 예압이 이후 외란에 대한 마찰력을 제공한다. 따라서 합성 렌치가 0이라고 접촉력이 없는 것은 아니다. 세게 조인다고 힘 닫힘이 성립하는 것도 아니다. 허용 접촉력들이 마찰과 단방향 접촉 조건 아래 필요한 모든 방향의 외란에 대응해야 한다. 액추에이터 한계가 유한하면 실제로 버틸 하중 집합도 유한하다.

> [!example] 계산 예제 · Worked example
> 손가락이 $r_1=(-0.05,0,0)$ m와 $r_2=(0.05,0,0)$ m에서 $f_1=(10,0,0)$ N, $f_2=(-10,0,0)$ N으로 조인다. 합력은 $(0,0,0)$이고 두 모멘트도 0이다($r_i\parallel f_i$). 그래서 각 접촉에 10 N이 걸려 있어도 $G f_c=0$이다. $\mu=0.5$이면 각 원뿔이 접선력을 $0.5\times10=5$ N까지 허용하므로, 이 조임에서 두 손가락은 수직 하중을 $2\times5=10$ N까지 버틴다.
> **반례**: 같은 조임이라도 마찰 없는 손가락($\mu=0$)은 허용되는 힘이 전부 $x$ 방향이라 수직 하중을 전혀 버티지 못한다. 아무리 세게 조여도 force closure가 아니다.

> [!question] 닫힘의 보장 확인 · Check what closure promises
> 힘 닫힘이면 선택한 파지로 무거운 패널을 들 수 있는가? **답:** 그것만으로는 부족하다. 닫힘은 접촉 모델 아래의 능력이다. 선택한 힘에서 실제 하중이 마찰·액추에이터·재료 한계 안에도 들어야 한다.

### 5. 위치, 힘, 임피던스, 어드미턴스

| 모드 | 조절 대상 |
|---|---|
| 위치 제어 | pose 또는 궤적 오차 |
| 힘 제어 | 측정된 접촉력 |
| 임피던스 제어 | 운동 오차 → 힘의 원하는 관계 |
| 어드미턴스 제어 | 측정 힘 → 운동 응답의 원하는 관계 |

임피던스는 단순히 "위치와 힘을 동시에 제어"하는 것이 아니다. 상호작용 거동을 — 대개
가상 질량-스프링-댐퍼로 — *형성*한다. 풀어 쓰면 제어기가 명령하는 것은 기준점에 매단 스프링과 댐퍼이고, 관성 항은 대부분의 구현처럼 뺐다. 그래서 만들어지는 힘은 변위와 속도만으로 정해진다:

$$F = K(x_d - x) + D(\dot x_d - \dot x)$$

이고, $K$(강성, N/m)와 $D$(감쇠, N·s/m)가 *설계* 변수이며, 실제로 나타나는 힘은 환경이 도구를 $x_d$에서 얼마나 밀어냈는가에 달려 있다. 위치 제어는 $K \to \infty$의 극한이고, 힘 제어는 $F$를 직접 조절하며 $x$는 가야 할 곳으로 가게 둔다. 어드미턴스는 강성 높고 정확한 위치 제어 로봇이
측정 힘을 유연한 운동 명령으로 바꿀 때 유용하다. 이 표 전체가 매달려 있는 세 계수 — 강성, 그 역수인 **컴플라이언스**, 그리고 감쇠 — 를 단위와 함께, 그리고 가장 무른 요소가 이기게 만드는 직렬 규칙과 함께 한 번만 정의한 곳은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §1]]이다.

**네 모드를 제어 법칙으로.** 표의 각 행은 피드백이 무엇에 작용하는지를 다르게 고른 것이다. $x_d$는 기준 자세, $F$는 로봇이 환경에 가하는 힘(그래서 로봇이 받는 힘은 $F_{ext}=-F$), $F_d$는 원하는 힘, $F_m$은 측정 힘이다.

- **위치 제어**는 자세 오차만 되먹이고 접촉력은 결과로 따라온다: 높은 게인 $K_p,K_v$로 $u=K_p(x_d-x)+K_v(\dot x_d-\dot x)$([[04-robotics/control-theory-ce397|제어 이론 §7]]의 PD 법칙).
- **힘 제어**는 힘 오차를 되먹이고, 흔히 비례-적분 법칙을 쓰며, 위치는 결과로 따라온다: $F=F_d+K_f(F_d-F_m)+K_i\int(F_d-F_m)\,dt$.
- **임피던스 제어**는 위의 스프링-댐퍼, 곧 운동 오차에서 힘으로 가는 사상을 구현한다. 관성 항까지 넣은 전체 목표 동역학은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §2]]에 있다.
- **어드미턴스 제어**는 반대 방향의 사상, 곧 측정 힘에서 운동으로 간다. 가상 동역학을 적분해 운동 기준 $x_c$를 얻고 그것을 내부 위치 루프에 넘긴다.
$$M_d\ddot x_c+D\,(\dot x_c-\dot x_d)+K\,(x_c-x_d)=F_{ext}$$
  측정 힘이 기준을 움직이므로 로봇은 밀리는 쪽으로 물러난다.

> [!example] 계산 예제 · Worked example
> $K=200$ N/m, $D=20$ N·s/m인 임피던스에서 공구가 기준보다 1 cm 못 미친 채($x_d-x=0.01$ m) 정지해 있으면 $F=200\times0.01=2$ N이다. 대신 공구가 $0.05$ m/s로 밀려나는 중이면($\dot x_d-\dot x=0.05$) 댐퍼가 $20\times0.05=1$ N을 더해 $F=3$ N이 된다. **반례**: 뻣뻣한 PD 위치 루프도 형식상 $K=K_p$인 임피던스지만, $K_p=10^5$ N/m에서 같은 1 cm가 1000 N을 요구하므로 "유연하다"고 부르면 틀린다. 유연함을 정하는 것은 법칙의 구조가 아니라 숫자다.

### 6. 시나리오: 벽 닦기

순수 위치 제어기가 도구를 추정 벽면보다 2 cm 안쪽으로 명령한다. 접촉 강성이 높아 벽
위치의 1 cm 오차가 완전히 다른 힘을 만들 수 있다. **숫자로 보면**: *유연하게 장착된* 도구가
벽에 $K = 10^4$ N/m로 닿으면 1 cm 위치 오차가 $10^4 \times 0.01 = 100$ N이 된다 — 표면을 파거나 힘
제한을 걸기에 충분하고, 3 cm 오차라면 팔이 낼 수조차 없을 300 N을 요구한다. 이 강성은
의도적으로 무른 쪽을 고른 값이다. 실제 팔에 단 맨 공구가 강철에 닿으면 최대 한 자릿수쯤 더 단단하고 — 공구·센서·팔·부재의 직렬 강성으로 약 $10^5$ N/m —
그때는 같은 1 cm 오차가 약 $10^3$ N을 요구해서 오차가 닫히기 한참 전에 힘이 발산한다. $10^7$ N/m의 재료 강성에 다가가는 것은 강체 지그 위의 맨 압자뿐이다.
강성 눈금은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §1]]에 표로 있다. 대신
*제어기의* 강성을 $K = 200$ N/m로 두면 같은 1 cm 오차가 요구하는 힘은 2 N이다. 접촉
작업을 유연하게 돌리는 이유는 어떤 제어 이론이 아니라 이 비율이다. 임피던스 제어기는 pose 오차를
허용하면서 복원력을 형성하고, 힘 제어기는 법선력을 직접 조절하지만 접선 운동과 안정성
처리가 따로 필요하다. 최선의 구조는 액추에이터 대역폭, 센싱, 표면 변동, 안전 한계에
달려 있다.

### 7. 힘, 촉각, 재료 상태

- 손목 힘/토크 센서는 합성 렌치를 재지만 전체 압력 분포는 못 잰다.
- 촉각 어레이는 접촉 위치, 압력, 전단, 미끄럼 신호를 추정할 수 있다.
- **고유수용감각**(proprioception)은 로봇 자신의 상태를 잰다(각도·속도를 재는 관절 엔코더, 토크를 재는 모터 전류, 몸통 자세·가속도를 재는 IMU). **외수용감각**(exteroception)은 로봇 바깥 세계를 잰다(카메라, 라이다, 깊이 센서). 손목 F/T 센서와 촉각 피부는 그 사이에 있다. 로봇 위에 달려 있지만 보고하는 것은 외부 접촉이다.
- 비전은 전역 기하를 보고, 촉각은 국소 접촉의 모호성을 푼다.

이 모두가 흘러 들어가는 곳은 추정 하나이고, 논문들이 정의 없이 쓰는 말이라 이름을 붙여 둘 값이 있다.

> [!info] 정의 · Definition — 접촉 상태 추정(contact-state estimation)
> **어떤 종류의 것인가.** *추정기*다. 제어기도 센서도 아니다. 측정 신호의 한 구간 — 손목 렌치, 관절 토크, 촉각 어레이, 명령한 운동과 측정한 운동 — 을 접촉의 현재 **모드**, 곧 이산 레이블에 대응시키고, 그 모드가 필요로 하는 연속량(접촉 위치, 법선 방향, $\mu$의 추정값)을 함께 내놓는다.
>
> **정의 조건은 둘이고**, 하나만 빠져도 접촉 상태 추정이 아니다. (i) 출력에 명시된 유한 집합에서 고른 **이산 모드**가 들어 있어야 한다. 계속 쓰는 대상이라면 $\{\text{떨어짐},\ \text{닿아서 고착},\ \text{닿아서 미끄럼}\}$이고, 이는 §1의 complementarity가 오가는 경우들의 목록과 정확히 같다. (ii) 추정은 명령한 자세가 아니라 **측정**에서 나와야 한다. 애초에 모드가 불확실한 이유가 패널이 모델이 말하는 자리에 없다는 것이기 때문이다.
>
> $$\hat s_t=\arg\max_{s\in\mathcal{S}}\ p\big(s\mid z_{t-w:t},\,u_{t-w:t}\big)$$
>
> $\mathcal{S}$는 선언한 모드 집합, $z$는 $w$ 샘플 구간의 측정, $u$는 같은 구간의 명령, $\hat s_t$는 고른 모드다. 한 샘플이 아니라 구간이 식에 들어가는 이유는, 고착과 느린 미끄럼이 순간 힘으로는 같아 보이고 접선력이 시간에 따라 어떻게 움직이는가에서만 갈리기 때문이다.
>
> **예.** 계속 쓰는 대상의 숫자가 세 모드를 가른다. $f_n\approx0$ N이면 *떨어짐*. $f_n=2$ N에 $\lVert f_t\rVert=1$ N이고 접선 운동이 없으면 *고착*. 같은 2 N인데 공구가 움직이면서 $\lVert f_t\rVert$가 $\mu f_n=1$ N 경계에 붙어 있으면 *미끄럼*이다. 뒤 두 경우는 힘의 크기가 똑같고, 운동 또는 $f_t$가 더 오르기를 멈췄다는 사실만이 둘을 가른다.
>
> **반례.** "궤적이 공구를 패널 안 5 mm로 보내라고 했으니 접촉 중이다"는 추정이 아니라 명령에 이름표만 바꿔 붙인 것이고, 패널이 잘못된 자리에 있어 접촉이 없음이 보장되는 바로 그 순간에 접촉이라고 보고한다. 맨 힘 임계값도 경계 하나의 *검출기*이지 모드 집합 위의 추정기가 아니다. 미끄럼을 보고하지 못한다.
>
> **왜 중요한가.** [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]의 모든 제어기가 모드마다 다른 방정식 묶음이다. 그 §3의 선택 행렬은 접촉이 어느 방향을 막는지 알아야 하고, 그 §5의 충격 논증은 모드가 바뀐 뒤에야 시작된다. 어떤 시스템이 "접촉을 다룬다"는 주장은, 논문이 그 이름을 쓰든 안 쓰든, 이 추정에 관한 주장이다.

로프, 천, 흙, 젖은 콘크리트, 케이블, 벌크 재료는 고차원의 변하는 상태를 갖는다. 이력과
관측 안 되는 재료 성질에 의존해 표현과 예측이 어렵다.

### 8. 학습과 sim-to-real

학습은 잔차 동역학, 접촉 상태, 마찰/재료 성질, 파지 점수, 촉각 조건부 정책을 추정할 수
있다. Domain randomization은 학습 조건을 넓히지만(시뮬레이터 파라미터의 분포 위에서 학습하는 것이고, 목적함수와 함께 [[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]]에서 정의한다), 선택한 randomization 분포가 곧
"어떤 변동까지 커버했는가"를 정의한다. 시뮬레이터의 특권 정보(privileged state, [[05-construction-robotics/sim-to-real|Sim-to-Real §2]])는 학습을
돕지만 배포 시에는 없다 — 정책이 시험 시점에 그것을 무엇으로 대체하는지 확인하라.
밀기 과제 하나에 셋이 다 들어간다. 잔차 동역학 네트워크는 시뮬레이터가 예측한 다음 상태와
실제 다음 상태의 차이를 배우고, domain randomization은 에피소드마다 μ와 물체 질량을 새로
뽑으며, 정책은 시뮬레이터의 정확한 물체 자세로 학습하지만 배포 때는 카메라로 추정한 자세만 쓴다.

### 9. 평가와 논문 표현

과제 성공, 최대/평균 힘, 힘 추종 오차, 미끄럼/낙하율, 물체·표면 손상, 회복, 안전 위반,
재료·마찰에 걸친 강건성을 재라. "Contact-rich", "compliant", "robust"는 명시적 과제·교란
정의를 요구하는 주장이다.

**네 가지 힘 지표의 정의.** 각각 종류가 다른 수이고, 각각 자기 방식으로 실패한다.

- **최대 접촉력** $F_{\max}=\max_t\lVert f(t)\rVert$, 접촉 구간 전체에 대해, 단위는 뉴턴. *표본으로 잡은* 최댓값이라 센서 속도만큼만 참이다. 1 kHz 채널이 1.4 ms 충격을 보면 사건 안에 샘플이 한 개쯤 들어가므로([[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §5]]) 보고된 최댓값이 실제보다 한참 낮을 수 있다. 같은 구간의 **평균 힘**이 짝인 수이고, 평균만 보고하면 최댓값이 존재하는 이유를 정확히 가린다.
- **힘 추종 오차**, 접촉 구간 $[0,T]$에서 명령한 법선력과 측정한 법선력 차이의 제곱평균제곱근, 단위는 뉴턴:

$$e_{\mathrm{RMS}}=\sqrt{\frac{1}{T}\int_0^T\big(f_d(t)-f_m(t)\big)^2\,dt}$$

  $f_d$는 명령한 힘, $f_m$은 측정한 힘, $T$는 접촉의 길이다 — 시행의 길이가 아니다. 시행 전체로 바꿔 넣으면 자유 공간의 몇 초가 평균에 섞여 제어기를 좋아 보이게 만든다. 계속 쓰는 대상의 예: 명령 $f_d=2$ N을 $2.0,\ 2.3,\ 1.8,\ 2.1$ N으로 측정하면 오차가 $0,\ 0.3,\ -0.2,\ 0.1$ N이므로 $e_{\mathrm{RMS}}=\sqrt{0.035}=0.187$ N, 목표의 $9.4\%$다. 평균 절대 오차는 $0.150$ N밖에 되지 않는다. RMS가 0.3 N짜리 한 번의 튐에 더 무겁게 값을 매기고, 힘 한계를 두고 이야기할 때 정직한 쪽이 그래서 RMS다.
- **미끄럼률**과 **낙하율**: 제어기가 고착을 명령한 동안 접선 운동이 일어난 접촉 시간의 비율, 그리고 목표에 닿기 전에 물체가 손을 떠난 파지 시행의 비율. 둘 다 비율이므로 시행 수를 옆에 적지 않으면 뜻이 없고, 둘 다 *명령한* 의도를 기준으로 재므로 §7의 접촉 상태 추정을 전제한다.

**반례.** 센서 속도 없는 최대 힘, 시행 전체로 잰 RMS 오차, $n$ 없는 미끄럼률은 남의 숫자와 비교할 수 없는 수를 보고하는 세 가지 서로 다른 방법이다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 성공률 상승만으로는 이득이 촉각 센싱, 더 나은 제어, 안전한 힘 한계, 쉬운 접촉 조건 중
> 어디서 왔는지 알 수 없다. 센싱·제어기·재료·초기화에 걸친 짝지은 베이스라인과 절제
> 실험을 찾아라.

### 읽고 나면 말할 수 있어야 하는 것

- 단방향 접촉과 complementarity를 정성적으로 설명할 수 있다
- 마찰 원뿔 부등식과 그 가정을 해석할 수 있다
- 원뿔의 각 선형화가 어느 쪽으로 틀리는지, 그것이 사실상 쓰는 계수가 얼마인지 말할 수 있다
- form closure와 force closure를 구분할 수 있다
- 힘·임피던스·어드미턴스 제어를 비교할 수 있다
- 촉각이 손목 힘·비전 너머에 더하는 것을 짚고, 접촉 상태 추정이 무엇을 출력해야 하는지 말할 수 있다
- 재료 변동과 접촉 관련 실패 지표를 검사할 수 있고, 최대 힘과 RMS 힘 오차가 각각 옆에 무엇을 적어야 하는지 안다

> [!tip] 더 깊이 · Going deeper
> 접촉과 마찰의 간결한 고전적 서술은 Mason의 *Mechanics of Robotic Manipulation*이다. Tedrake의 [*Robotic Manipulation*](https://manipulation.csail.mit.edu/)이 같은 영역을 돌려 볼 수 있는 시뮬레이터와 함께 다루는데, 접촉은 시뮬레이션과 현실이 가장 먼저 갈라지는 곳이라 그 점이 중요하다.

### 스스로 점검

1. 접촉 중에 위치 이득을 올리는 것이 위험할 수 있는 이유는?
2. 접선력 6 N, 법선력 10 N, $\mu=0.5$. 단순 원뿔에서 고착이 허용되는가?
3. 인식이 완벽해도 한 마찰 계수로 학습한 정책이 실패할 수 있는 이유는?
4. 촉각 정책의 절제 실험에서 무엇을 고정해야 하는가?
5. 어떤 계획기가 자기 파지에 마찰 여유가 남는다고 보고한다. 접촉마다 외접 상자 피라미드로 제약했다. 그 여유는 어느 쪽으로 틀렸고, 모서리에서 얼마나 틀렸는가?
6. 명령한 자세가 표면보다 안쪽이면 언제나 "접촉 중"이라고 기록하는 시스템이 있다. 접촉 상태 추정의 두 정의 조건 중 무엇을 어기며, 가장 나쁜 순간에 무엇이라고 보고하는가?

> [!tip]- 정답 · Answers
> 1. 작은 pose/모델 오차가 큰 힘과 불안정을 만들 수 있다.
> 2. 아니다: $6>0.5\times10=5$ N.
> 3. 실행 가능한 힘, 미끄럼 전이, 동역학이 달라진다.
> 4. 시연, 모델 용량, 제어기, 초기화, 재료, 평가 프로토콜 — 나머지를 쉽게 만들지 않으면서 촉각 정보만 제거·대체해야 한다.
> 5. 낙관적인 쪽으로 틀렸다. 상자 피라미드는 참 원뿔을 포함하므로 미끄러질 접선력까지 허가하고, 모서리에서는 참 경계의 $\sqrt2$배, 곧 $41.4\%$ 후하다. 내접 다면 원뿔은 반대쪽으로 틀려 여유를 과소평가했을 것이다.
> 6. (ii)번, 곧 추정이 명령이 아니라 측정에서 나와야 한다는 조건이다. 패널이 잘못된 자리에 있어 접촉이 없음이 보장되는 바로 그 순간에 접촉이라고 보고한다 — 그 추정이 존재하는 이유였던 경우다.

### 과제 · Problem set

Tier B. 계속 쓰는 대상에서 **항목 두 개만 바꾼다**. 명령 침투량이 $\delta=8\,\mathrm{mm}$가 되고, 패널의 먼지가 마찰 계수를 $\mu=0.35$로 떨어뜨린다. 나머지 — $\theta=(0^\circ,90^\circ)$의 **P2**, $x=1\,\mathrm{m}$의 패널, $k_w=400\,\mathrm{N/m}$, $m_p=1.0\,\mathrm{kg}$, $\pm0.05\,\mathrm{m}$에서의 10 N 두 손가락 조임 — 은 그대로다([[02-foundations/lab-plants|0.6]]). 이 페이지와 선수 지식, 객체 카탈로그만 쓴다. 시뮬레이터 없음.

1. **그리기.** 과제 그림의 두 패널을 새 숫자로 다시 그린다. 오른쪽 패널의 닫힌 곡선 셋은 이제 새 $f_n$에서 $\mu=0.35$로 그려야 하고, 1 N 닦기 화살표도 같은 축척으로 그려야 한다 — 셋 중 어느 집합이 그것을 품는지를 그림이 보여 주어야 한다.
2. **유도.** (a) $\delta=8\,\mathrm{mm}$에서 정지 상태의 $f_n$. (b) 원뿔 반각과 고착할 수 있는 최대 접선력. (c) $1\,\mathrm{N}$ 닦기는 아직 고착하는가, 여유는 얼마인가? (d) 4-생성자 내접 원뿔의 유효 계수와 *그것이* 허가하는 최대 닦기. (e) 이제 두 손가락에 필요한 조임과, 바꾸지 않은 10 N 조임이 버티는 힘.
3. **해석.** 여기서 가능한 실패는 둘 — 닦기의 미끄럼과 패널의 낙하 — 인데 하나만 일어났다. 어느 쪽이고, 같은 $30\%$의 $\mu$ 손실이 왜 두 경계를 반대 방향으로 움직였는가? 패널이 바닥에 닿기 전에 알려 주었을 측정 하나를 이름 붙이고, 이 페이지의 어느 절이 그것을 정의하는지 말하라.

> [!tip]- 정답 · Solutions
> 1. 같은 두 패널. 원뿔은 더 좁아지지만($26.6^\circ$ 대신 $19.3^\circ$) 접선 평면 위의 원은 *더 커진다*. $\mu$가 떨어진 것보다 $f_n$이 더 빨리 올랐기 때문이다. 4-생성자 정사각형의 꼭짓점은 여전히 원 위에 있고, 상자 피라미드의 정사각형은 여전히 원에 외접한다.
> 2. (a) 정지 상태 $f_n=400\times0.008=3.20\,\mathrm{N}$. 아직 다가오는 동안에만 $d_c\dot\delta$를 더한다. (b) $\arctan0.35=19.29^\circ$, 그리고 $\lVert f_t\rVert\le0.35\times3.20=1.12\,\mathrm{N}$. (c) 고착한다. $1.00<1.12$이고 여유는 $0.12\,\mathrm{N}$이라 경계의 $89.3\%$를 쓴다 — 경계 위에 정확히 있던 것에서 경계 안쪽으로 들어왔다. 더 깊이 누른 것이 먼지가 빼앗은 것보다 더 많은 마찰을 샀기 때문이다. (d) $\mu\cos(\pi/4)=0.35\times0.7071=0.2475$이므로 $0.2475\times3.20=0.792\,\mathrm{N}$까지만 허용한다. 보수적인 모델이 실제 접촉이 버티는 바로 그 닦기를 *거절*한다. (e) $f\ge m_pg/(2\mu)=9.81/0.70=14.01\,\mathrm{N}$이 필요한데, 바꾸지 않은 10 N 조임은 $2\times0.35\times10=7.00\,\mathrm{N}$을 버틴다 — 패널 무게 $9.81\,\mathrm{N}$보다 $2.81\,\mathrm{N}$ 모자란다.
> 3. 패널이 떨어지고 닦기는 멀쩡하다. 두 경계 모두 $\mu f_n$이고 $\mu$의 같은 $30\%$를 잃었지만, 닦기 쪽은 명령이 법선력을 $2.00$에서 $3.20\,\mathrm{N}$으로 올려 주었다 — $1.6\times0.7=1.12$로 먼지를 갚고도 남는 $60\%$의 이득이다 — 반면 파지 쪽의 법선력은 조임이 정하고 있어 그런 보상이 없었다, $1.0\times0.7=0.70$. 교훈은 마찰 여유가 *곱* $\mu f_n$에 대한 여유이고, 둘 중 더 세게 누른 쪽은 하나뿐이었다는 것이다. 이것을 잡았을 측정은 접촉 상태 추정(§7)이다. 제어기가 고착을 명령한 동안 손가락이 미끄러지는 것은 모드 변화이고, 접선력이 경계에 붙어 버린 데서 보이며, 패널이 손을 떠나기 전에 일어난다. 패널의 자세를 보는 카메라는 이미 떨어지기 시작할 때까지 아무것도 보지 못한다.

### 출처

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation (Tedrake) — 힘 제어·접촉 관련 장](https://manipulation.csail.mit.edu/)
- [Modern Robotics 코스 위키 — 12장 영상·소프트웨어](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)
