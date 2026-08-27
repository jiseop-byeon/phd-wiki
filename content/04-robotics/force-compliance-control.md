---
title: 13. Force & Compliance Control
tags: [robotics, manipulation, control]
study-depth: Mastery
wiki-support: Working
depth-goal: "Choose between impedance, admittance, hybrid, and passive compliance for a stated task and environment; say what a force-control claim in a paper actually established."
mastery-when: "This is the contribution-bearing layer of contact-rich manipulation — Mastery is the point of the manipulation track, not an optional upgrade."
---

> [!abstract] Depth target · 깊이 목표
> **Mastery** — with [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] this is the pair the
> [[07-research-program/index|research program]] promotes past Working, because every
> contact-rich manipulation claim is ultimately a claim about one of these controllers.
> **Mastery** — [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]]과 함께
> [[07-research-program/index|연구 프로그램]]이 Working 위로 올리는 쌍이다. 접촉이 많은 조작의
> 모든 주장이 결국 이 제어기들 중 하나에 관한 주장이기 때문이다.

> [!note] Before you start · 시작 전 점검
> You need the manipulator equation and the operational-space inertia $\Lambda$ ([[02-foundations/manipulator-kinematics-dynamics|10. §2, §6]]), friction and contact modes ([[04-robotics/contact-force-tactile|Contact, Force & Tactile §2–3]]), and closed-loop stability and bandwidth ([[04-robotics/control-theory-ce397|Control Theory §5, §7]]).
> 매니퓰레이터 방정식과 작업 공간 관성 $\Lambda$([[02-foundations/manipulator-kinematics-dynamics|10. §2, §6]]), 마찰과 접촉 모드([[04-robotics/contact-force-tactile|접촉·힘·촉각 §2–3]]), 폐루프 안정성과 대역폭([[04-robotics/control-theory-ce397|제어 이론 §5, §7]])이 필요하다.

## English

### 1. Position control cannot survive contact

A position controller's job is to drive position error to zero, and it does so with whatever
force that requires. In free space this is exactly right. In contact it is a specification
for breaking things, because the environment now decides what position error means.

Take the wall from [[04-robotics/contact-force-tactile|Contact, Force & Tactile §6]]:
a **compliantly mounted** tool meeting a surface at roughly $K_e = 10^4$ N/m, commanded 1 cm
past it.

$$F = K_e\,\Delta x = 10^4 \times 0.01 = 100\ \text{N}$$

The controller does not "decide" to push with 100 N; it is simply what closing a 1 cm error
against that stiffness costs. A compliant controller rendering $K = 200$ N/m in the same
situation produces $200 \times 0.01 = 2$ N and holds a 1 cm error it never resolves — which
in contact is the correct behaviour, not a failure.

Environment stiffness spans six orders of magnitude, and papers name the contact rather than
the number — so keep a scale, because the same control law is safe at one end and impossible
at the other:

| Contact | $K_e$ (N/m) |
|---|---:|
| soft padding, foam, carton | $10^3$–$10^4$ |
| compliant wrist or series-elastic joint, *in its compliant direction* | $10^3$–$10^4$ |
| hard paper, aluminium, steel — as **identified by a force controller** | $10^4$–$10^5$ |
| steel-on-steel **local material contact** (Hertzian) | $10^7$–$10^8$ |

> [!warning] Two stiffnesses wear the same symbol
> The last two rows are not a range, they are different quantities. A force controller
> identifies the **series** stiffness of tool + F/T sensor + arm structure + environment, and
> the structure is far softer than the material: Pham & Pham measure bare steel at
> $8\times10^4$ N/m and synthesize controllers against $\le 10^5$–$10^6$. The $10^7$–$10^8$
> figure is the *material's* local contact stiffness, and a control loop essentially never
> sees it. **When a paper reports an environment stiffness, it is reporting the fourth-row
> number only if it measured a bare indenter on a rigid fixture** — otherwise expect the third
> row. An RCC is also directional: compliant laterally ($\approx 10^4$) and stiff axially
> ($\approx 10^6$), so a single scalar $K_e$ for it is a simplification that fails for a
> straight-in push.

The example above sits in the second row. Run the same arithmetic in the fourth and it stops
being survivable: a 1 cm error against $10^7$ N/m asks for $10^5$ N, which no arm produces and
no tool survives. **That is the real reason a position controller is never pointed at
structure** — the force diverges long before the error closes. §5 uses the same two rows to
compute impact forces, so a claim about "a stiff contact" should always be read back to a row
of this table.

This is the whole subject in one comparison. **Contact turns position error into force**, so
control in contact is about choosing the *relation* between them rather than eliminating
either one. Mason's 1981 formalisation of this is still the cleanest way to say it: contact
imposes **natural constraints** (the wall determines the force normal to it, whatever you
command) and leaves you **artificial constraints** (you choose the motion along it). The
two sets are complementary, and **you cannot control position and force in the same
direction** — not because it is hard, but because the task's geometry has already assigned
one of them to the environment.

### 2. Impedance and admittance — the same idea, opposite causality

Both aim at the same thing: make the robot behave like a chosen mass–spring–damper

$$\mathcal{F} = M_d(\ddot x_d - \ddot x) + D_d(\dot x_d - \dot x) + K_d(x_d - x)$$

with $M_d, D_d, K_d$ the *desired* inertia, damping, and stiffness. They differ in which
variable is measured and which is commanded, and that single difference decides which
hardware and which environment each one suits.

<svg viewBox="0 0 560 248" style="max-width:100%;height:auto" role="img" aria-label="impedance control measures motion and commands torque, admittance control measures force and commands position into an inner loop">
  <g font-size="11" fill="currentColor" font-weight="600">
    <text x="20" y="22">IMPEDANCE &#8212; measure motion, command force</text>
    <text x="20" y="128">ADMITTANCE &#8212; measure force, command motion</text>
  </g>
  <g fill="currentColor">
    <rect x="96" y="34" width="96" height="38" rx="3" fill-opacity="0.14"/>
    <rect x="232" y="34" width="96" height="38" rx="3" fill-opacity="0.14"/>
    <rect x="368" y="34" width="96" height="38" rx="3" fill-opacity="0.28"/>
    <rect x="96" y="140" width="96" height="38" rx="3" fill-opacity="0.14"/>
    <rect x="232" y="140" width="96" height="38" rx="3" fill-opacity="0.28"/>
    <rect x="368" y="140" width="96" height="38" rx="3" fill-opacity="0.14"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="96" y="34" width="96" height="38" rx="3"/><rect x="232" y="34" width="96" height="38" rx="3"/><rect x="368" y="34" width="96" height="38" rx="3"/>
    <rect x="96" y="140" width="96" height="38" rx="3"/><rect x="232" y="140" width="96" height="38" rx="3"/><rect x="368" y="140" width="96" height="38" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.85" marker-end="url(#arF)">
    <line x1="196" y1="53" x2="228" y2="53"/><line x1="332" y1="53" x2="364" y2="53"/>
    <line x1="196" y1="159" x2="228" y2="159"/><line x1="332" y1="159" x2="364" y2="159"/>
    <path d="M 464 80 L 490 80 L 490 96 L 76 96 L 76 53 L 92 53"/>
    <path d="M 464 186 L 490 186 L 490 202 L 76 202 L 76 159 L 92 159"/>
  </g>
  <defs><marker id="arF" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="144" y="51">measured</text><text x="144" y="64">position</text>
    <text x="280" y="51">desired</text><text x="280" y="64">impedance</text>
    <text x="416" y="51">joint torque</text><text x="416" y="64">on the arm</text>
    <text x="144" y="157">measured</text><text x="144" y="170">force</text>
    <text x="280" y="157">desired</text><text x="280" y="170">admittance</text>
    <text x="416" y="157">inner position</text><text x="416" y="170">loop</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.85" text-anchor="end">
    <text x="536" y="30">needs a backdrivable, torque-controlled arm</text>
    <text x="536" y="136">needs a force sensor at the wrist</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="222">The shaded box is where each one needs hardware it cannot fake.</text>
    <text x="20" y="236">That is usually what decides the choice.</text>
  </g>
</svg>

- **Impedance control** measures motion and commands force. It needs an arm whose joints can
  be commanded in torque and are backdrivable. The robot is *soft by default* and its
  position accuracy in free space is only as good as its model.
- **Admittance control** measures force and commands motion into a stiff inner position
  loop. It needs a force sensor, and it works with the industrial arms that only accept
  position commands. The robot is *stiff by default*.

The rule that follows is not a preference but a consequence:

| | Suits | Fails against |
|---|---|---|
| **Impedance** | stiff environments — the arm's own compliance absorbs the contact | very soft environments and free space, where "soft by default" means poor positioning |
| **Admittance** | soft environments and precise free-space motion | stiff environments — a micron of motion makes a large force, the outer loop over-reacts, and the loop oscillates |

The asymmetry is worth internalising, because it inverts the naive expectation. The
*stiff* robot is the one that cannot handle a *stiff* wall.

> [!warning] The most common quiet error in reading force-control papers
> An industrial arm with a wrist force sensor doing "force control" is doing **admittance**
> control, and the vendor's position loop is in series with the environment. The two
> stiffnesses add, so a result demonstrated against foam says nothing about steel. Ask what
> the inner loop is before believing any compliance claim — see
> [[02-foundations/manipulator-kinematics-dynamics|10. §8]].

### 3. Hybrid position/force control

Mason's constraint analysis says which directions belong to the environment. Raibert and
Craig's 1981 architecture is how you act on that: choose a task frame, and a diagonal
**selection matrix** $S$ of ones and zeros that assigns each direction to one controller.

$$\tau = J^\top\left[\,S\,\mathcal{F}_{\text{pos}} + (I - S)\,\mathcal{F}_{\text{force}}\right]$$

Position control runs in the $S$ directions, force control in the complementary ones, and
the two never fight because they never address the same axis. For sliding a tool along a
surface: position control in the two tangential directions, force control along the normal.

This is the architecture that made constrained-manipulation tasks *specifiable*, and its
limitation is the same as its premise — it assumes you know the task frame and the contact
geometry. When the surface is where you thought it was, hybrid control is exact and easy to
tune. When the part is 3 mm from where the model says, the selection matrix is assigning
force control to a direction that is no longer normal to anything, which is the standard
way construction geometry breaks a factory controller.

### 4. Operational-space control

Khatib's 1987 formulation is what makes the previous two sections implementable on a real
arm rather than on a point mass. Control is written directly in task coordinates using the
operational-space inertia from [[02-foundations/manipulator-kinematics-dynamics|10. §6]]:

$$\mathcal{F} = \Lambda(\theta)\,\ddot x_d + \mu(\theta,\dot\theta) + p(\theta), \qquad \tau = J^\top\mathcal{F}$$

with $\mu$ and $p$ the task-space Coriolis and gravity terms. Two consequences that matter:

- The arm's configuration-dependent inertia is **compensated**, so a commanded task-space
  behaviour is the same in every pose. Without this, the factor-of-five inertia change from
  [[02-foundations/manipulator-kinematics-dynamics|10. §3]] shows up directly as a
  pose-dependent change in the contact behaviour you thought you had specified.
- Redundancy resolution becomes a **null-space projection**: a redundant arm can satisfy a
  secondary objective — stay away from joint limits, keep the elbow clear of a worker —
  using motion that produces no task-space force. For a mobile manipulator on a site with
  people in it, this is the mechanism, not a nicety.

**The projector, written out.** "Null-space" is used loosely across the literature, so it is
worth seeing the object. With $\bar J = M^{-1}J^\top\Lambda$ the dynamically-consistent
inverse of the Jacobian, the secondary torque is filtered through

$$\tau = J^\top\mathcal{F} \;+\; \underbrace{\left(I - J^\top\bar J^{\,\top}\right)}_{\text{null-space projector } N^\top}\tau_0$$

where $\tau_0$ is whatever the secondary objective asks for. The projector's job is that
**$\tau_0$ cannot disturb the task**. Be precise about *which* disturbance, because this is
commonly stated backwards: a projector built from the plain Moore–Penrose pseudo-inverse is
already **statically consistent** — in steady state the secondary torque produces no task
force at all. What it does not do is prevent the task from *accelerating* during the
transient, because $JM^{-1}\tau_0 \neq 0$ when $M^{-1} \neq I$. **Dynamic consistency buys
the transient, not the static force**: only $\bar J$ makes $JM^{-1}N^\top = 0$
(Dietrich, Ott & Albu-Schäffer, *IJRR* 2015).

**Task priority, and whole-body control.** Stack more than two objectives and this becomes a
hierarchy: each level is projected into the null space of all levels above it, so a lower
priority can never fight a higher one. That is the classical form. The modern form solves the
same problem as a **quadratic program** at every control step —

- minimize the weighted task errors,
- subject to joint-position, velocity and torque limits, friction cones at the contacts, and
  balance or base-stability constraints.

**This QP is what "whole-body control" names.** The reason the field moved to it is not
elegance: strict null-space priority cannot express *inequality* constraints, and joint
limits, torque saturation and contact friction are all inequalities. A humanoid or a mobile
manipulator that must respect all of them simultaneously is solving a QP, and the priority
hierarchy survives inside it as constraint weights or as a cascade of QPs.

For the mobile-manipulation case — where the "arm" includes a driveable base — the same QP
absorbs base and arm degrees of freedom into one problem, which is the formal version of the
choice [[04-robotics/navigation-mobile-manipulation|16. §4]] describes as deciding whether to
drive closer or reach further.

### 5. Contact transitions — where the theory earns its keep

Steady contact is the easy part. The hard part is the microsecond the robot arrives, and
the argument here is quantitative rather than rhetorical.

Model the impact as the end-effector's apparent mass $\Lambda$ meeting a spring of stiffness
$K$ at approach speed $v$. The contact is a half-sine, with

$$F_{\max} = v\sqrt{\Lambda K}, \qquad t_{\text{contact}} = \pi\sqrt{\Lambda/K}$$

Take the $\Lambda = 2$ kg from [[02-foundations/manipulator-kinematics-dynamics|10. §6]] and
a gentle approach at $v = 5$ cm/s.

| Interface | $K$ (N/m) | $F_{\max}$ | contact duration | 1 kHz samples inside the contact |
|---|---:|---:|---:|---:|
| bare tool on a stiff structure | $10^7$ | **224 N** | **1.4 ms** | about 1 |
| compliant wrist in series | $10^4$ | **7.1 N** | **44 ms** | about 44 |

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="the stiff contact drawn to scale as a needle-thin spike between two control samples, against the compliant contact as a broad flat bump">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="55" y1="170" x2="512" y2="170"/><line x1="55" y1="170" x2="55" y2="40"/>
  </g>
  <g stroke="currentColor" stroke-width="0.7" opacity="0.55" fill="none"><line x1="60.0" y1="170" x2="60.0" y2="176"/><line x1="68.8" y1="170" x2="68.8" y2="176"/><line x1="77.6" y1="170" x2="77.6" y2="176"/><line x1="86.4" y1="170" x2="86.4" y2="176"/><line x1="95.2" y1="170" x2="95.2" y2="176"/><line x1="104.0" y1="170" x2="104.0" y2="176"/><line x1="112.8" y1="170" x2="112.8" y2="176"/><line x1="121.6" y1="170" x2="121.6" y2="176"/><line x1="130.4" y1="170" x2="130.4" y2="176"/><line x1="139.2" y1="170" x2="139.2" y2="176"/><line x1="148.0" y1="170" x2="148.0" y2="176"/><line x1="156.8" y1="170" x2="156.8" y2="176"/><line x1="165.6" y1="170" x2="165.6" y2="176"/><line x1="174.4" y1="170" x2="174.4" y2="176"/><line x1="183.2" y1="170" x2="183.2" y2="176"/><line x1="192.0" y1="170" x2="192.0" y2="176"/><line x1="200.8" y1="170" x2="200.8" y2="176"/><line x1="209.6" y1="170" x2="209.6" y2="176"/><line x1="218.4" y1="170" x2="218.4" y2="176"/><line x1="227.2" y1="170" x2="227.2" y2="176"/><line x1="236.0" y1="170" x2="236.0" y2="176"/><line x1="244.8" y1="170" x2="244.8" y2="176"/><line x1="253.6" y1="170" x2="253.6" y2="176"/><line x1="262.4" y1="170" x2="262.4" y2="176"/><line x1="271.2" y1="170" x2="271.2" y2="176"/><line x1="280.0" y1="170" x2="280.0" y2="176"/><line x1="288.8" y1="170" x2="288.8" y2="176"/><line x1="297.6" y1="170" x2="297.6" y2="176"/><line x1="306.4" y1="170" x2="306.4" y2="176"/><line x1="315.2" y1="170" x2="315.2" y2="176"/><line x1="324.0" y1="170" x2="324.0" y2="176"/><line x1="332.8" y1="170" x2="332.8" y2="176"/><line x1="341.6" y1="170" x2="341.6" y2="176"/><line x1="350.4" y1="170" x2="350.4" y2="176"/><line x1="359.2" y1="170" x2="359.2" y2="176"/><line x1="368.0" y1="170" x2="368.0" y2="176"/><line x1="376.8" y1="170" x2="376.8" y2="176"/><line x1="385.6" y1="170" x2="385.6" y2="176"/><line x1="394.4" y1="170" x2="394.4" y2="176"/><line x1="403.2" y1="170" x2="403.2" y2="176"/><line x1="412.0" y1="170" x2="412.0" y2="176"/><line x1="420.8" y1="170" x2="420.8" y2="176"/><line x1="429.6" y1="170" x2="429.6" y2="176"/><line x1="438.4" y1="170" x2="438.4" y2="176"/><line x1="447.2" y1="170" x2="447.2" y2="176"/><line x1="456.0" y1="170" x2="456.0" y2="176"/><line x1="464.8" y1="170" x2="464.8" y2="176"/><line x1="473.6" y1="170" x2="473.6" y2="176"/><line x1="482.4" y1="170" x2="482.4" y2="176"/><line x1="491.2" y1="170" x2="491.2" y2="176"/><line x1="500.0" y1="170" x2="500.0" y2="176"/></g>
  <path d="M 60 170 C 64 10 68 10 72.4 170" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.3"/>
  <path d="M 60 170 C 190 165 321 165 451 170" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.7">
    <line x1="80" y1="56" x2="120" y2="56"/><line x1="300" y1="150" x2="300" y2="164"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="126" y="60">224 N, and all of it inside 1.4 ms</text>
    <text x="300" y="146" text-anchor="middle">7.1 N spread over 44 ms</text>
    <text x="60" y="192" font-size="10" opacity="0.85">1 kHz control samples</text>
    <text x="16" y="106" font-size="10" opacity="0.85">force</text>
    <text x="512" y="164" font-size="10" opacity="0.85" text-anchor="end">time (50 ms shown)</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="218">Both axes are to scale. The bare-tool contact is the needle at the left &#8212; taller than the plot</text>
    <text x="20" y="234">can hold, and narrower than the gap between two control samples. The compliant contact is</text>
    <text x="20" y="250">the broad bump: barely visible on that force axis, long enough for about 44 samples.</text>
  </g>
</svg>

Read the table rather than the picture. Against the bare structure the entire impact is over
in 1.4 ms, so a 1 kHz controller sees roughly **one sample** of it, arriving as late as
1 ms in — possibly after the peak has already passed. No control law fixes this, because
the information arrives after the event.

Put a compliant element in series and both numbers move, in opposite directions and by the
same factor: $F_{\max} \propto \sqrt{K}$ and $t_{\text{contact}} \propto 1/\sqrt{K}$, so
softening by $1000\times$ buys $\sqrt{1000} \approx 32\times$ in each. The force becomes
something the arm can survive *and* the event becomes long enough to regulate.

The lesson generalises past the arithmetic: **passive compliance is not a cheap substitute
for active control; it is the only thing that acts at contact bandwidth.** Whitney's 1982
quasi-static analysis of compliantly supported insertion is the mature version of this
idea — it derives, for chamfered and chamferless peg-in-hole, the conditions under which
misalignment causes **wedging** (opposing contact forces lock the part) or **jamming**
(the applied wrench falls outside the cone that produces insertion), and turns them into
design inequalities the support compliance must satisfy. A remote-centre compliance device
places the compliance centre at the part's tip, so a lateral error produces lateral motion
and an angular error produces rotation about the tip, and the two errors stop feeding each
other. It solves the insertion problem in aluminium, with no sensor and no latency.

Colgate and Hogan's 1988 result is the theoretical boundary of the active alternative: for
a manipulator coupled to an arbitrary passive but unknown environment, coupled stability
holds if and only if the manipulator's driving-point impedance is passive. That converts
contact stability from a per-experiment tuning question into a frequency-domain test, and
it says something uncomfortable — there is a **limit** to how light an apparent inertia or
how high a stiffness a controller can render stably. The controller cannot pretend the
arm's mass away.

### 6. Where learned policies sit

The framing this wiki's [[07-research-program/index|research program]] uses is deliberately
not "replace control with learning":

> **human demonstrations + a learned policy + classical control + tactile/visual feedback**

The division of labour follows directly from §5. A learned policy chooses *what compliance
to ask for and where to go* — decisions that require perception and context, and that run
happily at 10–50 Hz. A classical impedance or hybrid controller *realises* that request at
500–1000 Hz, and passive compliance handles the millisecond nobody can sample. A policy
that outputs joint positions into a stiff vendor loop has quietly opted out of all three
lower layers, whatever its paper says about contact.

This is also why the action space is the first thing to check in a manipulation-policy
paper: end-effector pose, joint position, joint torque, and *impedance parameters* are four
different claims about which layer the learning is contributing to.

#### The two papers that established this empirically

The claim above is not a stylistic preference — it was measured, twice, in 2019–2020, and
both papers are worth reading as a pair because they choose *different* spaces and reach the
same conclusion.

- **Martín-Martín et al., IROS 2019** — *Variable Impedance Control in End-Effector Space*.
  Treats the **impedance parameters themselves as the RL action space** (VICES), and compares
  it head-to-head against torque, joint-position, and end-effector-pose action spaces on
  contact-rich tasks. The finding that matters: the action space, not the algorithm, is what
  determines whether the policy can learn a contact task at all — and it changes sample
  efficiency and transfer, not just final score.
- **Bogdanovic, Khadiv & Righetti, RA-L 2020** — *Learning Variable Impedance Control for
  Contact Sensitive Tasks*. Same question in **joint space**: the policy outputs desired
  position *and* impedance gains. Its contribution is the robustness axis — it varies contact
  uncertainty deliberately and shows where torque control and position control each fail,
  while a learned variable-impedance action space degrades gracefully.

Read them against §2: choosing an action space *is* choosing where on the impedance–admittance
causality spectrum the learned layer sits. A policy emitting positions has picked the stiff
end and cannot express compliance at all; a policy emitting torques has picked the soft end
and must relearn the inner loop from scratch; a policy emitting impedance parameters is
asking the classical controller for a behaviour and letting it realise it at 1 kHz — which is
exactly the division of labour above.

> [!tip] Why this matters for a demonstration-collection thesis
> If the contribution is force-bearing demonstration data, the action space question arrives
> twice: once for what the *teleoperator* commands during collection, and once for what the
> *policy* emits at deployment. They do not have to match, and the mismatch is a design
> decision that most papers leave implicit.

#### The convergence, and the interface it is settling on

That framing is no longer only this wiki's opinion — it is where the field is moving, and
the direction is one-way. **The VLA is being demoted from motor controller to a slow
semantic layer that parameterises a classical inner loop.** That is a classical-control idea
winning an architectural argument.

- **ForceVLA** (NeurIPS 2025) treats 6-axis force/torque as a **primary** input channel
  rather than an auxiliary one, fused through a force-aware mixture of experts during action
  decoding — reporting +23.2% average success and up to 80% on plug insertion.
- **PaCo-VLA** goes further and is the sharpest single datapoint: it reframes VLA outputs as
  **task-level compliance proposals** and interposes a high-frequency **passivity shield**
  with energy-tank accounting, claiming zero passivity violations under adversarial
  compliance shifts. Passivity and energy tanks are 1990s interaction-control theory being
  used as a **runtime safety contract on a foundation model** — Colgate and Hogan's condition
  from §5, enforced at execution time.
- **VIDP** predicts pose *and* task compliance — stiffness profiles — jointly, without force
  sensors, separating geometric adaptation from intentional compliance change in the
  demonstrations.

The honest counterweight: this is convergence of **practice**, not of community. The
classical contact line — Tedrake's group on contact-mode explosion and non-smooth contact
gradients — goes largely uncited by the frontier VLA papers, and the flagship releases remain
position-controlled and largely force-blind. What is happening is that every group trying to
deploy a VLA on a contact-rich task independently rediscovers that it needs an
impedance or admittance inner loop, and reaches for the toolbox on this page.

> [!note] The prediction worth recording
> If the merge completes, **the interface will be compliance parameters, not positions.**
> That is the thing to watch, and it is the reason this page sits at Mastery in a research
> programme whose contribution is contact-rich manipulation.

### 7. Reading force control in a paper

| Question | What a wrong answer hides |
|---|---|
| Impedance or admittance? What is the inner loop? | Admittance on a stiff vendor loop cannot claim contact compliance |
| Was it tested against a **stiff** environment? | Foam and free space hide the instability entirely |
| Are $M_d, D_d, K_d$ reported, with units? | "Compliant" without numbers is not a specification |
| Contact **transition** shown, or only steady contact? | The transition is where §5 says the difficulty lives |
| Control rate, and sensor rate? | Below about 500 Hz, contact regulation is mostly the mechanics, not the controller |
| Any passive compliance in the hardware? | If yes, part of the result belongs to the spring, not the algorithm |
| Position accuracy in free space *and* force accuracy in contact? | Each architecture is bad at one of them; reporting one is reporting half |

### 8. The path to Mastery

| Need | Where |
|---|---|
| The impedance argument in its original form | Hogan 1985, Part I — the causality argument is the part to read closely |
| Constraint analysis and the task frame | Mason 1981; then Raibert & Craig 1981 for the architecture |
| Task-space implementation | Khatib 1987, with [[02-foundations/manipulator-kinematics-dynamics\|10. §6]] as the prerequisite |
| Why stiff contact destabilizes | Colgate & Hogan 1988 |
| The assembly reality check | Whitney 1982, and Whitney's 1987 IJRR survey for the landscape |
| Hands-on | A simulator with a torque-controlled arm: render $K_d$ from 50 to 5000 N/m against a stiff surface and find where it buzzes |

The Mastery test: given an arm, an environment stiffness, a sensor rate, and a task
tolerance, say which architecture can meet it — and whether any can.

### After reading

- [ ] State why position and force cannot be controlled in the same direction.
- [ ] Say which of impedance and admittance suits a stiff environment, and why it is the opposite of the naive guess.
- [ ] Write the selection-matrix form of hybrid control and give a task for it.
- [ ] Compute $F_{\max}$ and contact duration for a given $\Lambda$, $K$, $v$, and say how many control samples land inside.
- [ ] Explain what Colgate and Hogan's passivity condition forbids.

### Self-check

1. An industrial arm with a wrist force sensor holds 5 N against foam beautifully and
   oscillates violently against a steel plate. Name the architecture and the cause.
2. Approach speed doubles from 5 to 10 cm/s. What happens to the peak contact force and to
   the contact duration?
3. Why does a remote-centre compliance device solve peg-in-hole insertion without any sensor?
4. A paper reports a learned policy achieving "compliant insertion", with the policy
   outputting end-effector positions at 10 Hz to a position-controlled arm. What is the
   strongest claim it can actually support?
5. Hybrid position/force control is exact when the geometry is known. Why is that a problem
   specifically in construction?

> [!tip]- Answers
> 1. It is admittance control — the force sensor drives an outer loop that commands positions into the vendor's stiff inner loop. Against foam a large motion produces a small force, so the loop gain is low and it behaves. Against steel, micrometres of motion produce large forces, so the effective loop gain is enormous; the outer loop over-reacts, and the sensor and inner-loop delays turn that into oscillation. The stiff robot is the one that cannot handle the stiff wall.
> 2. $F_{\max} = v\sqrt{\Lambda K}$ is linear in $v$, so the peak force doubles to about 450 N in the stiff case. The duration $\pi\sqrt{\Lambda/K}$ does not contain $v$ at all, so it stays at 1.4 ms. Approaching faster buys you nothing in reaction time and costs you proportionally in force — which is why approach-speed limits, not better control, are the usual fix.
> 3. Because it places the compliance centre at the tip of the peg, so a lateral misalignment produces lateral compliance and an angular misalignment produces rotation about the tip, instead of each error generating the other. The correction is mechanical, so it happens at the speed of the material rather than the speed of a control loop — and §5 shows the control loop is too slow to have helped anyway.
> 4. That the policy chose good *positions*. Every compliance in the system belongs to the arm's inner loop and whatever passive give exists in the tool and part; the policy at 10 Hz cannot be regulating contact force, since the contact events of §5 are three orders of magnitude faster. It may well be a good result — it is a result about trajectory selection, not about compliance.
> 5. Because the architecture assigns force control to a direction it believes is normal to the surface, and that belief comes from a model. On a construction site the part is where it was placed, not where the drawing says: a few millimetres or a couple of degrees of error means force control is now acting partly along the surface and position control partly into it, which is exactly the fighting the architecture was designed to avoid. It is the difference between a fixtured factory cell and [[05-construction-robotics/assembly-fabrication|construction assembly]].

### Sources

**The classics — verified citations**

- N. Hogan, "Impedance Control: An Approach to Manipulation: Part I—Theory / Part II—Implementation / Part III—Applications," *ASME Journal of Dynamic Systems, Measurement, and Control*, vol. 107, no. 1, pp. 1–7, 8–16, 17–24, March 1985. An undivided earlier version appeared at the 1984 American Control Conference, pp. 304–313.
- M. T. Mason, "Compliance and Force Control for Computer Controlled Manipulators," *IEEE Transactions on Systems, Man, and Cybernetics*, vol. SMC-11, no. 6, pp. 418–432, 1981 — natural and artificial constraints.
- R. Martín-Martín, M. A. Lee, R. Gardner, S. Savarese, J. Bohg, "Variable Impedance Control in End-Effector Space: An Action Space for Reinforcement Learning in Contact-Rich Tasks," *IROS 2019*, pp. 1010–1017. DOI 10.1109/IROS40897.2019.8968201
- M. Bogdanovic, M. Khadiv, L. Righetti, "Learning Variable Impedance Control for Contact Sensitive Tasks," *IEEE RA-L* 5(4), pp. 6129–6136, 2020. DOI 10.1109/LRA.2020.3011379 · [arXiv:1907.07500](https://arxiv.org/abs/1907.07500)
- M. H. Raibert and J. J. Craig, "Hybrid Position/Force Control of Manipulators," *ASME Journal of Dynamic Systems, Measurement, and Control*, vol. **103**, no. 2, pp. 126–133, June 1981. Widely miscited as vol. 102; the volume is 103.
- J. K. Salisbury, "Active stiffness control of a manipulator in cartesian coordinates," *IEEE Conference on Decision and Control*, pp. 95–100, 1980 — Cartesian stiffness via $J^\top$, the direct antecedent of impedance control.
- O. Khatib, "A unified approach for motion and force control of robot manipulators: The operational space formulation," *IEEE Journal **on** Robotics and Automation*, vol. 3, no. 1, pp. 43–53, 1987.
- J. E. Colgate and N. Hogan, "Robust control of dynamically interacting systems," *International Journal of Control*, vol. 48, no. 1, pp. 65–88, 1988 — coupled stability as a passivity condition on driving-point impedance.
- D. E. Whitney, "Quasi-Static Assembly of Compliantly Supported Rigid Parts," *ASME Journal of Dynamic Systems, Measurement, and Control*, vol. 104, no. 1, pp. 65–77, March 1982 — wedging and jamming conditions. For the landscape, D. E. Whitney, "Historical Perspective and State of the Art in Robot Force Control," *IJRR*, vol. 6, no. 1, pp. 3–14, 1987.

> [!note] On citing the RCC itself
> Whitney 1982 is the *analysis* that justifies the remote-centre compliance, not its
> introduction. The device is usually traced to S. H. Drake's 1977 MIT PhD thesis and to
> Whitney & Nevins, "What is the Remote Center Compliance (RCC) and What Can It Do?",
> 9th International Symposium on Industrial Robots, 1979 — neither of which could be
> confirmed against an indexed primary record here, both predating DOI coverage. Check them
> against a library catalogue before citing rather than copying them from a secondary source.

**Within this wiki**

- [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] — $\Lambda$, the manipulator equation, and why the inner loop matters.
- [[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] — friction, contact modes, and the wall example §1 reuses.
- Convergence work cited in §6: Yu et al., "ForceVLA," NeurIPS 2025 ([arXiv:2505.22159](https://arxiv.org/abs/2505.22159)); Cao et al., "PaCo-VLA" ([arXiv:2606.00515](https://arxiv.org/abs/2606.00515), **preprint, under review**); Khalil et al., "VIDP" ([arXiv:2608.06210](https://arxiv.org/abs/2608.06210), **preprint**). The classical counterweight: Pang, Suh, Yang, Tedrake, *IEEE T-RO*, 2023 ([arXiv:2206.10787](https://arxiv.org/abs/2206.10787)).
- The impact numbers in §5 were computed here from the stated $\Lambda$, $K$, and $v$ with the linear half-sine impact model; recompute them rather than trusting them.

## 한국어

### 1. 위치 제어는 접촉에서 살아남지 못한다

위치 제어기의 일은 위치 오차를 0으로 모는 것이고, 그러기 위해 필요한 힘이 얼마든 그것을 쓴다.
자유 공간에서는 정확히 옳다. 접촉에서는 물건을 부수라는 명세가 된다. 이제 위치 오차가 무엇을
뜻하는지를 환경이 결정하기 때문이다.

[[04-robotics/contact-force-tactile|접촉·힘·촉각 §6]]의 벽을 보자: **유연하게 장착된** 도구가
대략 $K_e = 10^4$ N/m인 표면에 닿는데, 표면보다 1 cm 안쪽을 명령했다.

$$F = K_e\,\Delta x = 10^4 \times 0.01 = 100\ \text{N}$$

제어기가 100 N으로 밀기로 "결정"한 것이 아니다. 그 강성에 대해 1 cm 오차를 닫는 비용이 그저
그것일 뿐이다. 같은 상황에서 $K = 200$ N/m를 구현하는 유연한 제어기는 $200 \times 0.01 = 2$ N을
내고 끝내 해소하지 않는 1 cm 오차를 유지한다 — 접촉에서는 이것이 실패가 아니라 올바른 거동이다.

환경 강성은 여섯 자릿수에 걸쳐 있고, 논문은 숫자 대신 접촉을 이름으로 부른다 — 그러니 눈금을
갖고 있어야 한다. 같은 제어 법칙이 한쪽 끝에서는 안전하고 반대쪽 끝에서는 불가능하기 때문이다:

| 접촉 | $K_e$ (N/m) |
|---|---:|
| 무른 패딩, 폼, 판지 | $10^3$–$10^4$ |
| 유연 손목이나 직렬 탄성 관절, *그 유연한 방향에서* | $10^3$–$10^4$ |
| 두꺼운 종이, 알루미늄, 강재 — **힘 제어기가 식별하는 값** | $10^4$–$10^5$ |
| 강철 대 강철의 **국소 재료 접촉**(헤르츠) | $10^7$–$10^8$ |

> [!warning] 같은 기호를 쓰는 두 개의 강성
> 마지막 두 행은 하나의 범위가 아니라 서로 다른 양이다. 힘 제어기가 식별하는 것은 도구 + F/T
> 센서 + 팔 구조 + 환경의 **직렬** 강성이고, 구조가 재료보다 훨씬 무르다: Pham & Pham은 맨
> 강재를 $8\times10^4$ N/m로 측정하고 $10^5$–$10^6$ 이하를 상대로 제어기를 합성한다.
> $10^7$–$10^8$은 *재료의* 국소 접촉 강성이고, 제어 루프는 사실상 그것을 볼 일이 없다.
> **논문이 환경 강성을 보고할 때 그것이 넷째 행의 숫자이려면 강체 지그 위의 맨 인덴터를
> 측정한 경우여야 하고**, 그 밖에는 셋째 행이라고 보면 된다. RCC도 방향성이 있다: 측면으로는
> 유연하고($\approx 10^4$) 축 방향으로는 단단하다($\approx 10^6$). 그래서 스칼라 $K_e$ 하나로
> 적는 것은 곧장 밀어 넣는 경우에는 성립하지 않는 단순화다.

위 예는 둘째 행에 있다. 같은 계산을 넷째 행에서 하면 더 이상 견딜 수 있는 값이 아니다:
$10^7$ N/m에 대한 1 cm 오차는 $10^5$ N을 요구하고, 그것을 낼 수 있는 팔도 견딜 수 있는 도구도
없다. **위치 제어기를 구조체에 겨누지 않는 진짜 이유가 이것이다** — 오차가 닫히기 한참 전에
힘이 발산한다. §5도 같은 두 행으로 충격력을 계산하므로, "단단한 접촉"이라는 주장은 언제나
이 표의 어느 행인지로 되읽어야 한다.

이 비교 하나가 주제 전체다. **접촉은 위치 오차를 힘으로 바꾼다.** 그러므로 접촉에서의 제어는
둘 중 하나를 없애는 일이 아니라 둘 사이의 *관계*를 고르는 일이다. Mason이 1981년에 이것을
형식화한 방식이 여전히 가장 깔끔하다: 접촉은 **자연 제약**(natural constraint)을 부과하고
— 무엇을 명령하든 벽이 자기에 수직한 힘을 결정한다 — **인공 제약**(artificial constraint)을
남긴다 — 표면을 따라가는 운동은 당신이 고른다. 두 집합은 상보적이며, **같은 방향에서 위치와
힘을 동시에 제어할 수 없다**. 어려워서가 아니라, 과제의 기하가 둘 중 하나를 이미 환경에
배정해 버렸기 때문이다.

### 2. 임피던스와 어드미턴스 — 같은 발상, 반대 인과

둘 다 같은 것을 노린다: 로봇이 선택된 질량–스프링–감쇠기처럼 거동하게 만드는 것

$$\mathcal{F} = M_d(\ddot x_d - \ddot x) + D_d(\dot x_d - \dot x) + K_d(x_d - x)$$

($M_d, D_d, K_d$는 *원하는* 관성·감쇠·강성). 차이는 어느 변수를 측정하고 어느 것을 명령하는가
뿐이며, 그 하나의 차이가 어떤 하드웨어와 어떤 환경에 맞는지를 결정한다.

<svg viewBox="0 0 560 248" style="max-width:100%;height:auto" role="img" aria-label="임피던스 제어는 운동을 재고 토크를 명령하며, 어드미턴스 제어는 힘을 재고 내부 루프에 위치를 명령한다">
  <g font-size="11" fill="currentColor" font-weight="600">
    <text x="20" y="22">임피던스 &#8212; 운동을 재고, 힘을 명령한다</text>
    <text x="20" y="128">어드미턴스 &#8212; 힘을 재고, 운동을 명령한다</text>
  </g>
  <g fill="currentColor">
    <rect x="96" y="34" width="96" height="38" rx="3" fill-opacity="0.14"/>
    <rect x="232" y="34" width="96" height="38" rx="3" fill-opacity="0.14"/>
    <rect x="368" y="34" width="96" height="38" rx="3" fill-opacity="0.28"/>
    <rect x="96" y="140" width="96" height="38" rx="3" fill-opacity="0.14"/>
    <rect x="232" y="140" width="96" height="38" rx="3" fill-opacity="0.28"/>
    <rect x="368" y="140" width="96" height="38" rx="3" fill-opacity="0.14"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="96" y="34" width="96" height="38" rx="3"/><rect x="232" y="34" width="96" height="38" rx="3"/><rect x="368" y="34" width="96" height="38" rx="3"/>
    <rect x="96" y="140" width="96" height="38" rx="3"/><rect x="232" y="140" width="96" height="38" rx="3"/><rect x="368" y="140" width="96" height="38" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.85" marker-end="url(#arFk)">
    <line x1="196" y1="53" x2="228" y2="53"/><line x1="332" y1="53" x2="364" y2="53"/>
    <line x1="196" y1="159" x2="228" y2="159"/><line x1="332" y1="159" x2="364" y2="159"/>
    <path d="M 464 80 L 490 80 L 490 96 L 76 96 L 76 53 L 92 53"/>
    <path d="M 464 186 L 490 186 L 490 202 L 76 202 L 76 159 L 92 159"/>
  </g>
  <defs><marker id="arFk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="144" y="51">측정된</text><text x="144" y="64">위치</text>
    <text x="280" y="51">원하는</text><text x="280" y="64">임피던스</text>
    <text x="416" y="51">팔에 가하는</text><text x="416" y="64">관절 토크</text>
    <text x="144" y="157">측정된</text><text x="144" y="170">힘</text>
    <text x="280" y="157">원하는</text><text x="280" y="170">어드미턴스</text>
    <text x="416" y="157">내부 위치</text><text x="416" y="170">루프</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.85" text-anchor="end">
    <text x="536" y="30">역구동 가능한 토크 제어 팔이 필요하다</text>
    <text x="536" y="136">손목에 힘 센서가 필요하다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="222">음영 상자가 각각이 흉내 낼 수 없는 하드웨어를 요구하는 자리다.</text>
    <text x="20" y="236">대개 그것이 선택을 결정한다.</text>
  </g>
</svg>

- **임피던스 제어**는 운동을 재고 힘을 명령한다. 관절을 토크로 명령할 수 있고 역구동 가능한
  팔이 필요하다. 로봇은 *기본적으로 무르고*, 자유 공간에서의 위치 정확도는 모델이 정확한
  만큼만이다.
- **어드미턴스 제어**는 힘을 재고 뻣뻣한 내부 위치 루프에 운동을 명령한다. 힘 센서가
  필요하고, 위치 명령만 받는 산업용 팔에서도 동작한다. 로봇은 *기본적으로 뻣뻣하다*.

여기서 따라 나오는 규칙은 취향이 아니라 귀결이다:

| | 맞는 곳 | 무너지는 곳 |
|---|---|---|
| **임피던스** | 단단한 환경 — 팔 자신의 유연성이 접촉을 흡수한다 | 매우 무른 환경과 자유 공간. "기본적으로 무르다"가 곧 위치 정확도 부족이다 |
| **어드미턴스** | 무른 환경과 정밀한 자유 공간 운동 | 단단한 환경 — 마이크로미터의 운동이 큰 힘을 만들고, 외부 루프가 과반응하며, 루프가 진동한다 |

이 비대칭은 몸에 새겨 둘 가치가 있다. 소박한 예상을 뒤집기 때문이다: **뻣뻣한** 로봇이야말로
**단단한** 벽을 감당하지 못하는 쪽이다.

> [!warning] 힘 제어 논문을 읽을 때 가장 흔한, 조용한 오독
> 손목 힘 센서를 단 산업용 팔이 하는 "힘 제어"는 **어드미턴스** 제어이고, 벤더의 위치 루프가
> 환경과 직렬로 끼어 있다. 두 강성이 더해지므로, 폼(foam)에 대해 보인 결과는 강철에 대해
> 아무것도 말해 주지 않는다. 어떤 컴플라이언스 주장이든 믿기 전에 내부 루프가 무엇인지
> 물어라 — [[02-foundations/manipulator-kinematics-dynamics|10. §8]]을 보라.

### 3. 하이브리드 위치/힘 제어

Mason의 제약 분석이 어느 방향이 환경의 것인지를 말해 준다. Raibert와 Craig의 1981년
아키텍처는 그것을 실행하는 방법이다: 과제 프레임을 고르고, 각 방향을 어느 제어기에 배정할지를
0과 1로 적은 대각 **선택 행렬** $S$를 고른다.

$$\tau = J^\top\left[\,S\,\mathcal{F}_{\text{pos}} + (I - S)\,\mathcal{F}_{\text{force}}\right]$$

$S$ 방향에서는 위치 제어가, 나머지 방향에서는 힘 제어가 돈다. 같은 축을 건드리는 일이 없으므로
둘이 싸우지 않는다. 표면을 따라 공구를 미끄러뜨린다면: 접선 두 방향은 위치 제어, 법선 방향은
힘 제어.

구속 조작 과제를 *명세 가능하게* 만든 아키텍처이고, 그 한계는 그 전제와 같다 — 과제 프레임과
접촉 기하를 안다고 가정한다. 표면이 생각한 자리에 있으면 하이브리드 제어는 정확하고 튜닝도
쉽다. 부재가 모델이 말하는 곳에서 3 mm 벗어나 있으면, 선택 행렬은 더 이상 아무것에도 수직이
아닌 방향에 힘 제어를 배정하고 있는 것이다. 건설 현장의 기하가 공장용 제어기를 깨뜨리는
표준적인 방식이 이것이다.

### 4. 작업공간(operational space) 제어

Khatib의 1987년 정식화가 앞의 두 절을 점질량이 아니라 실제 팔 위에서 구현 가능하게 만든다.
제어를 [[02-foundations/manipulator-kinematics-dynamics|10. §6]]의 작업 공간 관성을 써서 과제
좌표에서 직접 쓴다:

$$\mathcal{F} = \Lambda(\theta)\,\ddot x_d + \mu(\theta,\dot\theta) + p(\theta), \qquad \tau = J^\top\mathcal{F}$$

($\mu$와 $p$는 작업 공간의 코리올리·중력 항). 중요한 귀결 둘:

- 팔의 자세 의존적 관성이 **보상된다.** 그래서 명령한 작업 공간 거동이 모든 자세에서 같아진다.
  이것이 없으면 [[02-foundations/manipulator-kinematics-dynamics|10. §3]]의 5배 관성 변화가
  곧바로, 명세했다고 믿은 접촉 거동의 자세 의존적 변화로 나타난다.
- 여유 자유도 해소가 **영공간 투영**이 된다: 여유 자유도가 있는 팔은 작업 공간 힘을 전혀 만들지
  않는 운동으로 부차 목표 — 관절 한계에서 멀어지기, 팔꿈치를 작업자에게서 비키기 — 를 만족할 수
  있다. 사람이 있는 현장의 모바일 매니퓰레이터에게 이것은 덤이 아니라 기제 그 자체다.

**투영자를 실제로 써 보면.** "영공간"은 문헌에서 느슨하게 쓰이므로 그 대상을 직접 볼 값어치가
있다. $\bar J = M^{-1}J^\top\Lambda$를 자코비안의 동역학적으로 일관된 역이라 하면, 부차 토크는
다음을 통과한다:

$$\tau = J^\top\mathcal{F} + \underbrace{\left(I - J^\top\bar J^{\,\top}\right)}_{\text{영공간 투영자 } N^\top}\tau_0$$

여기서 $\tau_0$는 부차 목표가 요구하는 무엇이든 된다. 투영자의 임무는 **$\tau_0$가 작업을
교란할 수 없게** 하는 것이다. 다만 *어떤* 교란인지를 정확히 해야 한다. 이 부분은 거꾸로 서술되는
일이 흔하다: 평범한 Moore–Penrose 유사역행렬로 만든 투영자도 이미 **정적으로 일관되다** —
정상 상태에서 부차 토크는 작업 힘을 전혀 만들지 않는다. 그것이 막지 못하는 것은 과도 구간에서
작업이 *가속되는* 것이다. $M^{-1} \neq I$이면 $JM^{-1}\tau_0 \neq 0$이기 때문이다.
**동역학적 일관성이 사는 것은 정적인 힘이 아니라 과도 구간이다**: $JM^{-1}N^\top = 0$을
만드는 것은 $\bar J$뿐이다(Dietrich, Ott & Albu-Schäffer, *IJRR* 2015).

**과제 우선순위, 그리고 whole-body control.** 목표를 둘 이상 쌓으면 이것이 계층이 된다: 각
층이 자기 위의 모든 층의 영공간으로 투영되므로, 낮은 우선순위가 높은 것과 다툴 수 없다. 그것이
고전적 형태다. 현대적 형태는 같은 문제를 매 제어 스텝의 **이차 계획법(QP)** 으로 푼다 —

- 가중된 과제 오차를 최소화하고,
- 관절 위치·속도·토크 한계, 접촉점의 마찰 원뿔, 균형 또는 베이스 안정성 제약 아래에서.

**이 QP가 "whole-body control"이 가리키는 것이다.** 이 분야가 그리로 옮겨간 이유는 우아함이
아니다: 엄격한 영공간 우선순위는 *부등식* 제약을 표현할 수 없는데, 관절 한계도 토크 포화도
접촉 마찰도 전부 부등식이다. 그것들을 동시에 지켜야 하는 휴머노이드나 모바일 매니퓰레이터는
QP를 풀고 있고, 우선순위 계층은 그 안에서 제약 가중치나 QP의 종속 연쇄로 살아남는다.

모바일 매니퓰레이션의 경우 — "팔"에 주행 가능한 베이스가 포함될 때 — 같은 QP가 베이스와 팔의
자유도를 하나의 문제로 흡수하고, 그것이 [[04-robotics/navigation-mobile-manipulation|16. §4]]가
더 다가갈지 더 뻗을지를 정하는 선택이라고 기술한 것의 형식적 판본이다.

### 5. 접촉 천이 — 이론이 값을 하는 지점

정상 접촉은 쉬운 부분이다. 어려운 것은 로봇이 도착하는 그 순간이고, 여기서의 논증은 수사가
아니라 정량적이다.

충돌을 말단의 겉보기 질량 $\Lambda$가 접근 속도 $v$로 강성 $K$인 스프링을 만나는 것으로
모델링하면, 접촉은 반주기 사인이고

$$F_{\max} = v\sqrt{\Lambda K}, \qquad t_{\text{contact}} = \pi\sqrt{\Lambda/K}$$

[[02-foundations/manipulator-kinematics-dynamics|10. §6]]의 $\Lambda = 2$ kg와 부드러운
접근 $v = 5$ cm/s를 넣자.

| 접촉면 | $K$ (N/m) | $F_{\max}$ | 접촉 지속 | 접촉 중 1 kHz 샘플 수 |
|---|---:|---:|---:|---:|
| 맨 공구가 단단한 구조물에 | $10^7$ | **224 N** | **1.4 ms** | 약 1개 |
| 유연 손목을 직렬로 | $10^4$ | **7.1 N** | **44 ms** | 약 44개 |

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="단단한 접촉이 제어 샘플 두 개 사이에 들어가는 바늘 같은 스파이크로, 유연한 접촉이 넓고 평평한 봉우리로 실제 비례로 그려져 있다">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="55" y1="170" x2="512" y2="170"/><line x1="55" y1="170" x2="55" y2="40"/>
  </g>
  <g stroke="currentColor" stroke-width="0.7" opacity="0.55" fill="none"><line x1="60.0" y1="170" x2="60.0" y2="176"/><line x1="68.8" y1="170" x2="68.8" y2="176"/><line x1="77.6" y1="170" x2="77.6" y2="176"/><line x1="86.4" y1="170" x2="86.4" y2="176"/><line x1="95.2" y1="170" x2="95.2" y2="176"/><line x1="104.0" y1="170" x2="104.0" y2="176"/><line x1="112.8" y1="170" x2="112.8" y2="176"/><line x1="121.6" y1="170" x2="121.6" y2="176"/><line x1="130.4" y1="170" x2="130.4" y2="176"/><line x1="139.2" y1="170" x2="139.2" y2="176"/><line x1="148.0" y1="170" x2="148.0" y2="176"/><line x1="156.8" y1="170" x2="156.8" y2="176"/><line x1="165.6" y1="170" x2="165.6" y2="176"/><line x1="174.4" y1="170" x2="174.4" y2="176"/><line x1="183.2" y1="170" x2="183.2" y2="176"/><line x1="192.0" y1="170" x2="192.0" y2="176"/><line x1="200.8" y1="170" x2="200.8" y2="176"/><line x1="209.6" y1="170" x2="209.6" y2="176"/><line x1="218.4" y1="170" x2="218.4" y2="176"/><line x1="227.2" y1="170" x2="227.2" y2="176"/><line x1="236.0" y1="170" x2="236.0" y2="176"/><line x1="244.8" y1="170" x2="244.8" y2="176"/><line x1="253.6" y1="170" x2="253.6" y2="176"/><line x1="262.4" y1="170" x2="262.4" y2="176"/><line x1="271.2" y1="170" x2="271.2" y2="176"/><line x1="280.0" y1="170" x2="280.0" y2="176"/><line x1="288.8" y1="170" x2="288.8" y2="176"/><line x1="297.6" y1="170" x2="297.6" y2="176"/><line x1="306.4" y1="170" x2="306.4" y2="176"/><line x1="315.2" y1="170" x2="315.2" y2="176"/><line x1="324.0" y1="170" x2="324.0" y2="176"/><line x1="332.8" y1="170" x2="332.8" y2="176"/><line x1="341.6" y1="170" x2="341.6" y2="176"/><line x1="350.4" y1="170" x2="350.4" y2="176"/><line x1="359.2" y1="170" x2="359.2" y2="176"/><line x1="368.0" y1="170" x2="368.0" y2="176"/><line x1="376.8" y1="170" x2="376.8" y2="176"/><line x1="385.6" y1="170" x2="385.6" y2="176"/><line x1="394.4" y1="170" x2="394.4" y2="176"/><line x1="403.2" y1="170" x2="403.2" y2="176"/><line x1="412.0" y1="170" x2="412.0" y2="176"/><line x1="420.8" y1="170" x2="420.8" y2="176"/><line x1="429.6" y1="170" x2="429.6" y2="176"/><line x1="438.4" y1="170" x2="438.4" y2="176"/><line x1="447.2" y1="170" x2="447.2" y2="176"/><line x1="456.0" y1="170" x2="456.0" y2="176"/><line x1="464.8" y1="170" x2="464.8" y2="176"/><line x1="473.6" y1="170" x2="473.6" y2="176"/><line x1="482.4" y1="170" x2="482.4" y2="176"/><line x1="491.2" y1="170" x2="491.2" y2="176"/><line x1="500.0" y1="170" x2="500.0" y2="176"/></g>
  <path d="M 60 170 C 64 10 68 10 72.4 170" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.3"/>
  <path d="M 60 170 C 190 165 321 165 451 170" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.7">
    <line x1="80" y1="56" x2="120" y2="56"/><line x1="300" y1="150" x2="300" y2="164"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="126" y="60">224 N, 그 전부가 1.4 ms 안에</text>
    <text x="300" y="146" text-anchor="middle">7.1 N이 44 ms에 걸쳐</text>
    <text x="60" y="192" font-size="10" opacity="0.85">1 kHz 제어 샘플</text>
    <text x="16" y="106" font-size="10" opacity="0.85">힘</text>
    <text x="512" y="164" font-size="10" opacity="0.85" text-anchor="end">시간 (50 ms 구간)</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="218">두 축 모두 실제 비례다. 맨 공구의 접촉이 왼쪽의 바늘이다 &#8212; 그림이 담기 버거울 만큼</text>
    <text x="20" y="234">높고, 제어 샘플 두 개 사이보다 좁다. 유연한 접촉은 넓은 봉우리다: 같은 힘 축에서는</text>
    <text x="20" y="250">거의 보이지 않고, 샘플이 약 44개 들어올 만큼 길다.</text>
  </g>
</svg>

그림보다 표를 읽어라. 맨 구조물에 대해서는 충돌 전체가 1.4 ms 안에 끝나므로, 1 kHz 제어기는
그중 **샘플 하나** 정도를 보고, 그마저 최대 1 ms 늦게 — 정점이 이미 지나간 뒤에 — 도착할 수
있다. 어떤 제어 법칙도 이것을 고치지 못한다. 정보가 사건 뒤에 오기 때문이다.

유연 요소를 직렬로 넣으면 두 숫자가 반대 방향으로, 같은 배수만큼 움직인다:
$F_{\max} \propto \sqrt{K}$이고 $t_{\text{contact}} \propto 1/\sqrt{K}$이므로 $1000\times$
무르게 하면 각각 $\sqrt{1000} \approx 32\times$를 산다. 힘은 팔이 견딜 만한 것이 되고, *동시에*
사건이 조절할 수 있을 만큼 길어진다.

교훈은 산수 너머로 일반화된다: **수동 컴플라이언스는 능동 제어의 값싼 대체품이 아니라, 접촉
대역폭에서 작동하는 유일한 것이다.** Whitney의 1982년 준정적 분석이 이 발상의 성숙한 판본이다 —
챔퍼가 있는 경우와 없는 경우의 peg-in-hole에 대해, 정렬 오차가 언제 **wedging**(맞서는 접촉력이
부재를 잠가 버림)이나 **jamming**(가해진 렌치가 삽입을 만드는 원뿔 밖으로 벗어남)을 일으키는지의
조건을 유도하고, 그것을 지지부 컴플라이언스가 만족해야 할 설계 부등식으로 바꾼다. RCC 장치는
컴플라이언스 중심을 부재의 끝점에 놓아서, 횡방향 오차는 횡방향 운동을, 각도 오차는 끝점 둘레의
회전을 만들게 하고 두 오차가 서로를 먹여 살리지 못하게 한다. 알루미늄으로, 센서 없이, 지연
없이 삽입 문제를 푼다.

Colgate와 Hogan의 1988년 결과가 능동적 대안의 이론적 경계다: 임의의 수동적이지만 알려지지 않은
환경에 결합된 매니퓰레이터에 대해, 결합 안정성은 매니퓰레이터의 구동점 임피던스가 수동적일 때
그리고 오직 그때만 성립한다. 접촉 안정성을 실험마다의 튜닝 문제에서 주파수 영역의 판정으로
바꾸고, 불편한 것을 하나 말해 준다 — 제어기가 안정하게 구현할 수 있는 겉보기 관성의 가벼움과
강성의 높음에는 **한계가 있다.** 제어기가 팔의 질량을 없는 척할 수는 없다.

### 6. 학습된 정책이 앉는 자리

이 위키의 [[07-research-program/index|연구 프로그램]]이 쓰는 프레이밍은 의도적으로 "제어를
학습으로 대체한다"가 아니다:

> **사람의 시연 + 학습된 정책 + 고전 제어 + 촉각·시각 피드백**

분업은 §5에서 곧바로 따라 나온다. 학습된 정책은 *어떤 컴플라이언스를 요구하고 어디로 갈지*를
고른다 — 인식과 맥락이 필요하고, 10~50 Hz에서 편안히 도는 결정들이다. 고전적 임피던스 또는
하이브리드 제어기가 그 요구를 500~1000 Hz에서 *실현한다.* 그리고 수동 컴플라이언스가 아무도
샘플링할 수 없는 그 밀리초를 맡는다. 뻣뻣한 벤더 루프에 관절 위치를 내보내는 정책은, 논문이
접촉에 대해 무슨 말을 하든, 아래 세 층에서 조용히 빠져나온 것이다.

조작 정책 논문에서 행동 공간을 가장 먼저 확인해야 하는 이유이기도 하다: 말단 자세, 관절 위치,
관절 토크, 그리고 *임피던스 파라미터*는 학습이 어느 층에 기여하고 있는가에 대한 네 개의 서로
다른 주장이다.

#### 이것을 실증적으로 세운 두 편

위 주장은 취향이 아니라 2019~2020년에 두 번 측정된 것이다. 두 편은 *서로 다른* 공간을 고르고
같은 결론에 도달하므로 짝으로 읽어야 한다.

- **Martín-Martín 외, IROS 2019** — *Variable Impedance Control in End-Effector Space*.
  **임피던스 파라미터 자체를 RL의 행동 공간으로** 삼고(VICES), 토크·관절 위치·말단 자세 행동
  공간과 접촉이 많은 과제에서 정면 비교한다. 중요한 발견은 이것이다: 정책이 접촉 과제를 애초에
  학습할 수 있느냐를 정하는 것은 알고리즘이 아니라 **행동 공간**이고, 최종 점수만이 아니라 표본
  효율과 전이가 함께 바뀐다.
- **Bogdanovic, Khadiv & Righetti, RA-L 2020** — *Learning Variable Impedance Control for
  Contact Sensitive Tasks*. 같은 질문을 **관절 공간**에서 던진다: 정책이 목표 위치 *와* 임피던스
  이득을 함께 낸다. 기여는 강건성 축이다 — 접촉 불확실성을 의도적으로 변화시켜 토크 제어와 위치
  제어가 각각 어디서 무너지는지를 보이고, 학습된 가변 임피던스 행동 공간은 완만하게 나빠진다.

§2에 비추어 읽어라: 행동 공간을 고르는 일이 곧 **학습 층을 임피던스–어드미턴스 인과 스펙트럼의
어디에 놓을지 고르는 일**이다. 위치를 내는 정책은 뻣뻣한 끝을 골랐으므로 컴플라이언스를 아예
표현할 수 없고, 토크를 내는 정책은 무른 끝을 골랐으므로 내부 루프를 처음부터 다시 배워야 하며,
임피던스 파라미터를 내는 정책은 고전 제어기에게 *거동*을 요청하고 1 kHz에서 실현하게 맡긴다 —
이것이 바로 위의 분업이다.

> [!tip] 시연 수집이 기여인 논문에 이것이 왜 중요한가
> 기여가 힘을 담은 시연 데이터라면 행동 공간 질문이 두 번 온다. 수집 중에 *원격조작자*가 무엇을
> 명령하는가에서 한 번, 배치 시에 *정책*이 무엇을 내는가에서 한 번. 둘이 같을 필요는 없고, 그
> 불일치는 대부분의 논문이 암묵에 두는 설계 결정이다.

#### 수렴, 그리고 그것이 자리 잡아 가는 인터페이스

이 프레이밍은 더 이상 이 위키의 의견만이 아니다 — 분야가 움직이고 있는 방향이고, 그 방향은
일방향이다. **VLA가 운동 제어기에서, 고전적 내부 루프를 매개변수화하는 느린 의미 층으로 강등되고
있다.** 고전 제어의 발상이 아키텍처 논쟁에서 이기고 있는 것이다.

- **ForceVLA**(NeurIPS 2025)는 6축 힘/토크를 부차가 아니라 **주** 입력 채널로 다루고, 행동
  디코딩 중에 힘 인지 mixture of experts로 융합한다 — 평균 성공률 +23.2%, 플러그 삽입에서 최대
  80%를 보고한다.
- **PaCo-VLA**는 한 걸음 더 나아가며 가장 날카로운 단일 근거다: VLA의 출력을 **과제 수준
  컴플라이언스 제안**으로 재해석하고, 에너지 탱크 회계를 갖춘 고주파 **수동성 방패**(passivity
  shield)를 끼워 넣어, 적대적인 컴플라이언스 변화에서도 수동성 위반이 0이라고 주장한다.
  수동성과 에너지 탱크는 1990년대 상호작용 제어 이론이며, 그것이 **파운데이션 모델 위의 런타임
  안전 계약**으로 쓰이고 있다 — §5의 Colgate–Hogan 조건을 실행 시점에 강제하는 것이다.
- **VIDP**는 자세 *와* 과제 컴플라이언스 — 강성 프로파일 — 를 힘 센서 없이 함께 예측하며,
  시연 안에서 기하적 적응과 의도적 컴플라이언스 변화를 구분한다.

정직한 균형추: 이것은 **실무**의 수렴이지 공동체의 수렴이 아니다. 고전적 접촉 계열 — 접촉 모드
폭발과 비평활 접촉 그래디언트에 관한 Tedrake 그룹의 작업 — 은 프런티어 VLA 논문들에 거의 인용되지
않고, 대표 릴리스들은 여전히 위치 제어되고 대체로 힘에 눈이 멀어 있다. 실제로 일어나는 일은,
접촉이 많은 과제에 VLA를 배치하려는 모든 그룹이 임피던스나 어드미턴스 내부 루프가 필요하다는
것을 독립적으로 재발견하고, 이 페이지의 도구상자로 손을 뻗는 것이다.

> [!note] 기록해 둘 예측
> 그 합류가 완성된다면 **인터페이스는 위치가 아니라 컴플라이언스 파라미터일 것이다.**
> 그것이 지켜볼 지점이고, 기여가 접촉이 많은 조작인 연구 프로그램에서 이 페이지가 Mastery에 있는
> 이유다.

### 7. 논문에서 힘 제어 읽기

| 질문 | 틀린 답이 감추는 것 |
|---|---|
| 임피던스인가 어드미턴스인가? 내부 루프는 무엇인가? | 뻣뻣한 벤더 루프 위의 어드미턴스는 접촉 컴플라이언스를 주장할 수 없다 |
| **단단한** 환경에서 검증했는가? | 폼과 자유 공간은 불안정을 통째로 감춘다 |
| $M_d, D_d, K_d$를 단위와 함께 보고했는가? | 숫자 없는 "유연함"은 명세가 아니다 |
| 접촉 **천이**를 보였는가, 정상 접촉만인가? | §5에 따르면 어려움은 천이에 산다 |
| 제어 주기와 센서 주기는? | 약 500 Hz 아래에서는 접촉 조절의 대부분이 제어기가 아니라 역학이다 |
| 하드웨어에 수동 컴플라이언스가 있는가? | 있다면 결과의 일부는 알고리즘이 아니라 스프링의 몫이다 |
| 자유 공간의 위치 정확도 *그리고* 접촉의 힘 정확도를 함께 보고했는가? | 각 아키텍처는 둘 중 하나에 약하다. 하나만 보고하는 것은 절반만 보고하는 것이다 |

### 8. Mastery로 가는 길

| 필요한 것 | 어디서 |
|---|---|
| 임피던스 논증의 원형 | Hogan 1985 Part I — 인과(causality) 논증을 정독할 것 |
| 제약 분석과 과제 프레임 | Mason 1981, 그다음 아키텍처는 Raibert & Craig 1981 |
| 작업 공간 구현 | Khatib 1987, 선수 지식은 [[02-foundations/manipulator-kinematics-dynamics\|10. §6]] |
| 단단한 접촉이 왜 불안정하게 만드는가 | Colgate & Hogan 1988 |
| 조립의 현실 점검 | Whitney 1982, 분야 조감은 Whitney의 1987 IJRR 서베이 |
| 직접 해 보기 | 토크 제어 팔이 있는 시뮬레이터에서 단단한 면에 대해 $K_d$를 50에서 5000 N/m까지 올리며 어디서 떨리기 시작하는지 찾을 것 |

Mastery 시험: 팔, 환경 강성, 센서 주기, 과제 공차가 주어졌을 때 어느 아키텍처가 그것을 만족할
수 있는지 — 그리고 만족할 수 있는 것이 하나라도 있는지 — 말하는 것.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 같은 방향에서 위치와 힘을 동시에 제어할 수 없는 이유를 말한다.
- [ ] 임피던스와 어드미턴스 중 단단한 환경에 맞는 쪽과, 그것이 왜 소박한 예상과 반대인지 말한다.
- [ ] 하이브리드 제어의 선택 행렬 형태를 쓰고 적합한 과제를 하나 든다.
- [ ] 주어진 $\Lambda$, $K$, $v$에 대해 $F_{\max}$와 접촉 지속을 계산하고 제어 샘플이 몇 개 들어가는지 말한다.
- [ ] Colgate와 Hogan의 수동성 조건이 무엇을 금지하는지 설명한다.

### 스스로 점검

1. 손목 힘 센서를 단 산업용 팔이 폼에 대해서는 5 N을 훌륭하게 유지하는데 강판에 대해서는
   격렬하게 진동한다. 아키텍처와 원인을 대라.
2. 접근 속도가 5에서 10 cm/s로 두 배가 된다. 최대 접촉력과 접촉 지속 시간은 어떻게 되는가?
3. RCC 장치는 왜 센서 하나 없이 peg-in-hole 삽입을 푸는가?
4. 어떤 논문이 학습된 정책으로 "유연한 삽입"을 달성했다고 보고하는데, 정책은 위치 제어되는
   팔에 10 Hz로 말단 위치를 내보낸다. 이 논문이 실제로 뒷받침할 수 있는 가장 강한 주장은?
5. 하이브리드 위치/힘 제어는 기하를 알 때 정확하다. 왜 그것이 하필 건설에서 문제인가?

> [!tip]- 정답 · Answers
> 1. 어드미턴스 제어다 — 힘 센서가 외부 루프를 구동해 벤더의 뻣뻣한 내부 루프에 위치를 명령한다. 폼에서는 큰 운동이 작은 힘을 만들어 루프 게인이 낮고 얌전하다. 강철에서는 마이크로미터의 운동이 큰 힘을 만들어 실효 루프 게인이 거대해지고, 센서와 내부 루프의 지연이 그것을 진동으로 바꾼다. 뻣뻣한 로봇이야말로 단단한 벽을 감당하지 못하는 쪽이다.
> 2. $F_{\max} = v\sqrt{\Lambda K}$는 $v$에 선형이므로 단단한 경우 최대 힘은 약 450 N으로 두 배가 된다. 지속 시간 $\pi\sqrt{\Lambda/K}$에는 $v$가 아예 없으므로 1.4 ms 그대로다. 빨리 접근해도 반응 시간은 하나도 벌지 못하고 힘만 비례해서 치른다 — 더 나은 제어가 아니라 접근 속도 제한이 통상적인 처방인 이유다.
> 3. 컴플라이언스 중심을 peg의 끝점에 놓기 때문이다. 그러면 횡방향 정렬 오차는 횡방향 컴플라이언스를, 각도 오차는 끝점 둘레의 회전을 만들고, 각 오차가 다른 오차를 생성하지 않는다. 보정이 기계적이므로 제어 루프의 속도가 아니라 재료의 속도로 일어난다 — 그리고 §5는 어차피 제어 루프가 도와주기에는 너무 느렸음을 보여준다.
> 4. 정책이 좋은 *위치*를 골랐다는 것. 시스템의 모든 컴플라이언스는 팔의 내부 루프와 공구·부재에 있는 수동적 여유의 몫이다. 10 Hz의 정책이 접촉력을 조절하고 있을 수는 없다. §5의 접촉 사건은 세 자릿수 더 빠르기 때문이다. 좋은 결과일 수는 있다 — 다만 컴플라이언스가 아니라 궤적 선택에 관한 결과다.
> 5. 아키텍처가 표면에 수직이라고 *믿는* 방향에 힘 제어를 배정하는데, 그 믿음이 모델에서 오기 때문이다. 건설 현장에서 부재는 도면이 말하는 곳이 아니라 놓인 곳에 있다: 몇 밀리미터나 몇 도의 오차는 힘 제어가 이제 부분적으로 표면을 따라, 위치 제어가 부분적으로 표면 안으로 작용한다는 뜻이고, 이것이야말로 그 아키텍처가 피하려고 설계된 바로 그 싸움이다. 지그로 고정된 공장 셀과 [[05-construction-robotics/assembly-fabrication|건설 조립]]의 차이가 이것이다.

### 출처

**고전 — 검증된 인용**

- N. Hogan, "Impedance Control: An Approach to Manipulation: Part I—Theory / Part II—Implementation / Part III—Applications," *ASME Journal of Dynamic Systems, Measurement, and Control*, vol. 107, no. 1, pp. 1–7, 8–16, 17–24, March 1985. 나뉘지 않은 이전 판본이 1984 American Control Conference, pp. 304–313에 있다.
- M. T. Mason, "Compliance and Force Control for Computer Controlled Manipulators," *IEEE Transactions on Systems, Man, and Cybernetics*, vol. SMC-11, no. 6, pp. 418–432, 1981 — 자연 제약과 인공 제약.
- R. Martín-Martín, M. A. Lee, R. Gardner, S. Savarese, J. Bohg, "Variable Impedance Control in End-Effector Space: An Action Space for Reinforcement Learning in Contact-Rich Tasks," *IROS 2019*, pp. 1010–1017. DOI 10.1109/IROS40897.2019.8968201
- M. Bogdanovic, M. Khadiv, L. Righetti, "Learning Variable Impedance Control for Contact Sensitive Tasks," *IEEE RA-L* 5(4), pp. 6129–6136, 2020. DOI 10.1109/LRA.2020.3011379 · [arXiv:1907.07500](https://arxiv.org/abs/1907.07500)
- M. H. Raibert and J. J. Craig, "Hybrid Position/Force Control of Manipulators," *ASME Journal of Dynamic Systems, Measurement, and Control*, vol. **103**, no. 2, pp. 126–133, June 1981. vol. 102로 널리 잘못 인용된다. 실제 권은 103이다.
- J. K. Salisbury, "Active stiffness control of a manipulator in cartesian coordinates," *IEEE Conference on Decision and Control*, pp. 95–100, 1980 — $J^\top$를 통한 카테시안 강성, 임피던스 제어의 직계 선조.
- O. Khatib, "A unified approach for motion and force control of robot manipulators: The operational space formulation," *IEEE Journal **on** Robotics and Automation*, vol. 3, no. 1, pp. 43–53, 1987.
- J. E. Colgate and N. Hogan, "Robust control of dynamically interacting systems," *International Journal of Control*, vol. 48, no. 1, pp. 65–88, 1988 — 구동점 임피던스의 수동성 조건으로서의 결합 안정성.
- D. E. Whitney, "Quasi-Static Assembly of Compliantly Supported Rigid Parts," *ASME Journal of Dynamic Systems, Measurement, and Control*, vol. 104, no. 1, pp. 65–77, March 1982 — wedging과 jamming 조건. 분야 조감은 D. E. Whitney, "Historical Perspective and State of the Art in Robot Force Control," *IJRR*, vol. 6, no. 1, pp. 3–14, 1987.

> [!note] RCC 자체를 인용하는 것에 대하여
> Whitney 1982는 remote-centre compliance를 정당화하는 *분석*이지 그것을 도입한 논문이 아니다.
> 장치는 보통 S. H. Drake의 1977년 MIT 박사학위 논문과 Whitney & Nevins, "What is the Remote
> Center Compliance (RCC) and What Can It Do?", 9th International Symposium on Industrial
> Robots, 1979로 거슬러 올라간다 — 둘 다 DOI 시대 이전이라 여기서는 색인된 1차 기록으로
> 확인하지 못했다. 2차 출처에서 베끼지 말고 도서관 목록에서 확인한 뒤 인용하라.

**이 위키 안에서**

- [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]] — $\Lambda$, 매니퓰레이터 방정식, 그리고 내부 루프가 중요한 이유.
- [[04-robotics/contact-force-tactile|접촉·힘·촉각 상호작용]] — 마찰, 접촉 모드, 그리고 §1이 다시 쓰는 벽 예제.
- §6이 인용하는 수렴 연구: Yu et al., "ForceVLA," NeurIPS 2025 ([arXiv:2505.22159](https://arxiv.org/abs/2505.22159)); Cao et al., "PaCo-VLA" ([arXiv:2606.00515](https://arxiv.org/abs/2606.00515), **프리프린트, 심사 중**); Khalil et al., "VIDP" ([arXiv:2608.06210](https://arxiv.org/abs/2608.06210), **프리프린트**). 고전 쪽 균형추: Pang, Suh, Yang, Tedrake, *IEEE T-RO*, 2023 ([arXiv:2206.10787](https://arxiv.org/abs/2206.10787)).
- §5의 충돌 수치는 명시된 $\Lambda$, $K$, $v$와 선형 반주기 사인 충돌 모델로 여기서 계산한 것이다. 믿지 말고 다시 계산하라.
