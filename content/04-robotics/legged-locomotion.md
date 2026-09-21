---
title: 18. Legged Locomotion
tags: [robotics, locomotion, unstructured]
study-depth: Working
wiki-support: Working
depth-goal: "Explain privileged teacher-student distillation, say what each landmark locomotion result actually claimed, and read a locomotion paper without inheriting its reputation."
mastery-when: "Raise to Mastery only if locomotion becomes the platform your contribution runs on — the research program keeps it supporting."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to read the canon accurately and to use these platforms, not to
> advance them.
> **Working** — 정본을 정확히 읽고 이 플랫폼들을 쓸 만큼. 그것을 진전시키기 위해서가 아니라.

> [!note] Prerequisites · 선수 지식
> You need RL and policy gradients ([[02-foundations/rl-basics|7. RL Basics §4]]), the manipulator equation and why actuator models matter ([[02-foundations/manipulator-kinematics-dynamics|10. §2, §7]]), and DAgger ([[01-canonical-papers/notes/4-vla/dagger|DAgger]]) — because distillation here is DAgger with a simulator as the expert.
> RL과 정책 경사([[02-foundations/rl-basics|7. RL 기초 §4]]), 매니퓰레이터 방정식과 액추에이터 모델이 중요한 이유([[02-foundations/manipulator-kinematics-dynamics|10. §2, §7]]), 그리고 DAgger([[01-canonical-papers/notes/4-vla/dagger|DAgger]])가 필요하다 — 여기서의 증류가 시뮬레이터를 전문가로 삼은 DAgger이기 때문이다.

## English

*Group I. Stands on [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Dynamics]] and [[02-foundations/rl-basics|7. RL Basics]].
Privileged teacher–student distillation is the idea to take from here, and the page doubles as practice at correcting over-citation.*

> [!note] First pass · 처음이라면
> Read §1, then §2 — privileged teacher–student distillation is the one idea to take away — then §3, where each canonical result is pinned to what it actually claimed. §1.5 is there for when you meet a biped paper written in the classical language. The running object, the picture and the worked derivation on them are the lecture the problem set assumes; do those in order (object, picture, §1.5, worked) if you are here for the course rather than for the literature.

### Running object · 이 페이지의 장치

None of the six plants in [[02-foundations/lab-plants|0.6 Lab Plants]] is a legged body, so this
page freezes its own and the next two pages reuse it rather than inventing a second one.

**Q — the frozen quadruped.** One rigid body on four massless legs, standing square.

| Symbol | Value | Meaning |
|---|---:|---|
| $m$ | $12\,\mathrm{kg}$ | total body mass |
| $z$ | $0.30\,\mathrm{m}$ | centre-of-mass height when standing |
| hip rectangle | $0.60\times0.30\,\mathrm{m}$ | feet at $(\pm0.30,\pm0.15)\,\mathrm{m}$ under the CoM |
| $\ell$ | $0.34\,\mathrm{m}$ | leg length, hip to foot |
| $\mu$ | $0.6$ | foot–ground friction coefficient |
| $T$ | $0.40\,\mathrm{s}$ | gait period |
| $\beta$ | $0.50$ | duty factor of the nominal trot |
| $h_{\max}$ | $0.15\,\mathrm{m}$ | step-over height the catalog grants it |
| $f_{z,\max}$ | $200\,\mathrm{N}$ | per-foot vertical force limit |
| $g$ | $9.81\,\mathrm{m/s}^2$ | gravity |

Only the last four rows are stipulations. $h_{\max}$ and $f_{z,\max}$ are catalog numbers the way
P3's hand stiffness is a catalog number — stated once, never derived here, changed only in a
problem set. Everything else on this page is computed from the rows above, and no number below
contradicts one of them.

Q carries the wiki's running robotics task: **P2** from [[02-foundations/lab-plants|0.6]] rides
on Q's back, and the worked derivation below ends by computing what that arm costs the body. Q is
also the body of the QP on [[04-robotics/convex-mpc-legged|8. Convex MPC]] and the robot whose
costmap is built on [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]].

The humanoid in §1.5 with $z=0.9$ m is a *different* body, kept because that is the size the
capture-point literature is written about. When the two disagree it is because they are two
machines, not because one number is stale.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="top: the frozen quadruped as an inverted pendulum with its capture point inside a foothold reach bracket; bottom: a trot gait chart over one period">
  <defs><marker id="arQ" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.6"><line x1="40" y1="120" x2="520" y2="120"/></g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.9"><line x1="250" y1="58" x2="200" y2="120"/></g>
  <circle cx="250" cy="58" r="5" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.45" stroke-dasharray="3 3"><line x1="250" y1="58" x2="250" y2="120"/></g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.9" marker-end="url(#arQ)"><line x1="260" y1="58" x2="304" y2="58"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.8"><line x1="200" y1="114" x2="200" y2="126"/><line x1="250" y1="114" x2="250" y2="126"/><line x1="296" y1="114" x2="296" y2="126"/></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7"><line x1="130" y1="144" x2="370" y2="144"/><line x1="130" y1="138" x2="130" y2="150"/><line x1="370" y1="138" x2="370" y2="150"/></g>
  <g font-size="10" fill="currentColor">
    <text x="262" y="50" font-size="11">x&#775;</text>
    <text x="180" y="140" font-size="9.5" opacity="0.85">p</text>
    <text x="244" y="140" font-size="9.5" opacity="0.85">x</text>
    <text x="290" y="140" font-size="9.5" opacity="0.85">&#958;</text>
    <text x="262" y="34" opacity="0.85">CoM, z = 0.30 m, m = 12 kg</text>
    <text x="250" y="164" font-size="9.5" text-anchor="middle" opacity="0.85">foothold reach, 0.46 m each way</text>
    <text x="40" y="184" font-size="10.5" opacity="0.9">&#958; inside the bracket means one step can still bring it to rest.</text>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.5"><line x1="80" y1="268" x2="480" y2="268"/><line x1="80" y1="268" x2="80" y2="274"/><line x1="280" y1="268" x2="280" y2="274"/><line x1="480" y1="268" x2="480" y2="274"/></g>
  <g fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6">
    <rect x="80" y="199" width="200" height="14" rx="2"/>
    <rect x="280" y="219" width="200" height="14" rx="2"/>
    <rect x="280" y="239" width="200" height="14" rx="2"/>
    <rect x="80" y="259" width="200" height="14" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="0.8" fill="none" opacity="0.35"><line x1="80" y1="199" x2="480" y2="199"/><line x1="80" y1="219" x2="480" y2="219"/><line x1="80" y1="239" x2="480" y2="239"/><line x1="80" y1="259" x2="480" y2="259"/></g>
  <g font-size="9.5" fill="currentColor" opacity="0.9">
    <text x="46" y="210">LF</text><text x="46" y="230">RF</text><text x="46" y="250">LH</text><text x="46" y="270">RH</text>
    <text x="80" y="286" text-anchor="middle">0</text><text x="280" y="286" text-anchor="middle">0.20 s</text><text x="480" y="286" text-anchor="middle">0.40 s</text>
    <text x="40" y="306" font-size="10.5">Shaded = stance. Trot: two diagonal feet down at a time, swapping every 0.20 s.</text>
  </g>
</svg>

Top: Q as a linear inverted pendulum, its CoM at $z = 0.30$ m moving at the trot command $\dot x = 1.0$ m/s over the stance foot $p$, with the capture point $\xi$ at $\dot x/\omega_0 = 0.175$ m ahead of the CoM's projection $x$ and well inside the foothold-reach bracket of $0.46$ m each way, so one step can still bring Q to rest. Bottom: the nominal trot over one period $T = 0.40$ s, LF and RH in stance for the first $0.20$ s and RF and LH for the second; read as a table, the chart is the contact schedule [[04-robotics/convex-mpc-legged|8. Convex MPC]] is handed.

### 1. Why this page exists

This literature is **systematically over-cited beyond its actual claims**. The famous results
are famous for approximately the right reasons and are then quoted for something adjacent
that they did not show. That makes it a good page for practising the reading discipline the
rest of this wiki asks for, and it makes the corrections below the most useful content here.

It also matters directly: legged platforms are what most of
[[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] runs on, and
the field's single highest-leverage training idea was invented here.

### 1.5 The classical vocabulary this page does not use

Everything below is the learned line, and it does not speak the language most legged papers
before roughly 2019 were written in. You still need that language to read them, so here it
is at literacy depth, with the reason it is absent from the rest of this page.

- **Support polygon** — the convex hull of the contact points on the ground. The classical
  stability question is whether a particular point stays inside it. Written out, with $c_1,\dots,c_k$ the contact points projected onto the ground plane, it is every weighted average of them with nonnegative weights summing to one:
$$\mathcal{S}=\mathrm{conv}\{c_1,\dots,c_k\}=\Big\{\sum_i\lambda_ic_i:\ \lambda_i\ge0,\ \sum_i\lambda_i=1\Big\}$$
  The **static stability criterion** requires the vertical projection of the centre of mass (CoM) to lie in $\mathcal S$, because nonnegative vertical foot forces can only produce a resultant located inside the hull, and standing still needs that resultant directly under the CoM. Example: feet at $(\pm0.3,\pm0.15)$ m give a $0.6\times0.3$ m rectangle, and a CoM projection at $(0.1,0.05)$ m is inside. Non-example: in a trot only a diagonal pair is down, the polygon collapses to the segment between them, and the CoM is almost never on that segment, yet trotting robots do not fall, since a trot is balanced dynamically, not statically.
- **ZMP (zero-moment point)** — the point on the ground where the ground reaction force
  produces no horizontal moment. Keep the ZMP strictly inside the support polygon and the
  foot cannot rotate about its edge; let it reach the boundary and the foot tips. Almost
  every walking-pattern generator of that era is a device for producing a ZMP trajectory the
  robot can track. On flat ground the ZMP coincides with the **centre of pressure**, the force-weighted average of the contact points,
$$p_{\text{ZMP}}=\frac{\sum_i f_{z,i}\,c_i}{\sum_i f_{z,i}}$$
  where $f_{z,i}\ge0$ is the vertical force at contact $c_i$; the vertical forces produce no horizontal moment about this point, so it satisfies the definition. Because the weights are nonnegative, a ZMP measured from real forces is always inside the polygon; the criterion is about the ZMP the *planned motion* demands. For a CoM at constant height $z$ (the linear inverted pendulum below) that demand is $p=x-(z/g)\,\ddot x$, with $x$ the CoM's horizontal position. Example: four feet at $x=0.3,0.3,-0.3,-0.3$ m carrying $40,30,20,10$ N put the ZMP at $x=0.12$ m. A CoM at $z=0.9$ m accelerating forward at $1$ m/s² demands a ZMP $0.9/9.81=0.092$ m behind the CoM, so a foot reaching $0.125$ m behind it allows at most $9.81\times0.125/0.9=1.36$ m/s² before the demanded ZMP leaves the foot and it tips.
- **Capture point / DCM (divergent component of motion)** — where you would have to place
  the next footfall to come to a complete stop. From the linear inverted pendulum model with
  centre-of-mass height $z$, $\;\omega_0 = \sqrt{g/z}\;$ and the capture point sits
  $\;\dot x/\omega_0\;$ ahead of the centre of mass. **Worked:** a humanoid with
  $z = 0.9$ m has $\omega_0 = \sqrt{9.81/0.9} = 3.30$ rad/s, so at $\dot x = 0.5$ m/s it
  must step $0.5/3.30 = 0.15$ m ahead to stop; at $1.0$ m/s, $0.30$ m. DCM is the
  three-dimensional generalisation used by modern whole-body controllers. The model behind it is the **linear inverted pendulum**: a point mass at constant height $z$ on a massless leg whose foot, the ZMP, is at $p$. Its dynamics and the capture point $\xi$ are
$$\ddot x=\omega_0^2\,(x-p),\qquad \xi=x+\frac{\dot x}{\omega_0},\qquad \dot\xi=\omega_0\,(\xi-p)$$
  so the last equation follows by differentiating $\xi$ and substituting the first. It has a positive rate $\omega_0$, so $\xi$ runs away from $p$ exponentially unless the foot is placed on $\xi$; placing it there makes $\dot\xi=0$ and the CoM comes to rest over the foot. Non-example: step 5 cm short of $\xi$ with $\omega_0=3.30$ rad/s, and the gap grows to $0.05\,e^{3.30\times0.5}=0.26$ m within half a second.

**Why this page does not use any of it.** ZMP assumes a flat, known, co-planar support
surface and a foot that makes full contact with it. That assumption is what the learned line
gave up on purpose: on rubble, on a slope, on a toe-only foothold, the support polygon is not
the object ZMP needs. What replaces it is not a better criterion but a different bargain:
the controller gives up any verified balance criterion, and in exchange a policy reacts to
disturbances 50 times a second while relying on only one physical condition — that the foot
does not slip ([[04-robotics/convex-mpc-legged|8. Convex MPC]] keeps the model-based half of that bargain
by *pre-specifying* the contact schedule).

So: expect ZMP and capture point in humanoid, biped and whole-body-control papers, and expect
their absence in the learned results §3 covers. Neither absence is an oversight.

**The third word: limit cycle.** A limit cycle is an isolated closed trajectory in state
space — a nonlinear system's own preferred oscillation, which it returns to after a small
push, with no external clock telling it the period. A steady walking gait is exactly this,
and reading it that way explains two things at once. First, why *passive dynamic walkers* —
legged machines with no actuators at all, walking down a shallow slope on gravity alone —
work: the gait is a stable limit cycle of the mechanism, and the slope only pays for the
energy lost at each foot strike. Second, what "stability" means for a walker: not that the
state stays near a point (a walker is never at rest) but that the trajectory returns to the
cycle after a disturbance. That is why gait stability is studied through the *return map* —
the state at one foot strike as a function of the state at the previous one — and why a
walker can be stable in this sense while violating both the static criterion (CoM projection inside the support polygon) and the dynamic ZMP criterion.

**The same idea as formulas.** For a system $\dot x=f(x)$, a **periodic orbit** is a solution with $x(t+T)=x(t)$ for a smallest period $T>0$, and it is a **limit cycle** when it is isolated, meaning no other periodic orbit lies arbitrarily close. The **return map** (Poincaré map) samples the state once per cycle, at each foot strike, $x_{k+1}=P(x_k)$. A periodic gait is a fixed point of that map, and it is locally stable when every eigenvalue of the map's Jacobian there has magnitude below one:
$$x^\star=P(x^\star),\qquad \Big|\lambda_i\Big(\tfrac{\partial P}{\partial x}(x^\star)\Big)\Big|<1$$
because a small deviation $\delta_k=x_k-x^\star$ then evolves as $\delta_{k+1}\approx\frac{\partial P}{\partial x}\delta_k$ and shrinks. Example: $P(x)=0.5x+0.1$ has $x^\star=0.2$ and slope $0.5$, so a start at $0.3$ goes $0.25,\ 0.225,\dots$ and the deviation halves every step. Non-examples: $P(x)=1.2x-0.04$ has the same fixed point but deviations grow by $1.2$ per step, an unstable cycle; and an undamped harmonic oscillator has closed orbits at every amplitude, a continuum rather than an isolated one, so none of them is a limit cycle and a push simply leaves it on a neighbouring orbit.

The learned policies in §3 never name the concept, but they inherit it: what a locomotion
reward actually selects for, when it rewards forward velocity without prescribing a gait, is
a limit cycle the network found on its own. The trotting and bounding patterns that emerge
unbidden in those papers are that object appearing without being asked for.

- M. Vukobratović and B. Borovac, "Zero-moment point — thirty five years of its life,"
  *International Journal of Humanoid Robotics*, vol. 1, no. 1, 2004.
- J. Pratt, J. Carff, S. Drakunov, A. Goswami, "Capture Point: A Step toward Humanoid Push
  Recovery," *Humanoids 2006*.
- J. Englsberger, C. Ott, A. Albu-Schäffer, "Three-Dimensional Bipedal Walking Control Based
  on Divergent Component of Motion," *IEEE Transactions on Robotics*, vol. 31, no. 2, 2015.

### Worked on Q · 장치로 한 번 끝까지

Everything here is the linear inverted pendulum of §1.5 evaluated on Q's rows, plus the gait
arithmetic that turns it into a speed limit. Do it once here and the problem set is a change of
knobs rather than a first derivation.

**1. The time constant.** The LIP obeys $\ddot x=\omega_0^2(x-p)$ with $\omega_0=\sqrt{g/z}$, and
that rate depends on height alone — not on mass, not on leg length, not on how many feet are down —
so Q's is fixed the moment its standing height is:

$$\omega_0=\sqrt{\frac{g}{z}}=\sqrt{\frac{9.81}{0.30}}=5.72\ \mathrm{rad/s},\qquad \frac{1}{\omega_0}=0.175\ \mathrm{s}$$

An uncorrected lean grows by a factor $e$ every $0.175$ s, so a $5$ cm error that nobody pays for
becomes $0.05\,e^{1}=0.136$ m of it one time constant later. A 10 Hz controller gets fewer than two
samples per time constant; that is the arithmetic behind §2's policies running at 50 Hz and above, and behind
every locomotion stack having a fast inner loop.

**2. The capture point.** From §1.5, $\xi=x+\dot x/\omega_0$, and placing the next foot on $\xi$
makes $\dot\xi=0$, so the distance the foot must go ahead of the CoM to bring Q to rest in one step is

$$\xi-x=\frac{\dot x}{\omega_0}=\frac{1.0}{5.72}=0.175\ \mathrm{m}$$

at the trot command $\dot x=1.0$ m/s. The number is small; the question is whether Q's leg can reach it.

**3. Where a foot can actually go.** The hip sits $d=0.30$ m ahead of the CoM (half the hip
rectangle). The foot lies on a sphere of radius $\ell=0.34$ m about the hip, and while the hip is at
standing height the vertical side of that right triangle is $z=0.30$ m, so the horizontal excursion
left over is

$$R=\sqrt{\ell^2-z^2}=\sqrt{0.34^2-0.30^2}=\sqrt{0.0256}=0.16\ \mathrm{m}$$

The hip-relative window is therefore $2R=0.32$ m wide, and the furthest foothold ahead of the CoM is
$d+R=0.30+0.16=0.46$ m. That $0.46$ m is the bracket in the picture above.

**4. Two speed limits, and which one binds.** The first is balance: a one-step stop needs
$\xi-x\le d+R$, so $\dot x\le\omega_0(d+R)=5.72\times0.46=2.63$ m/s. The second is stroke. During
stance the foot is pinned to the ground while the hip travels forward $\dot x\,\beta T$, so the foot
sweeps backwards through the hip-relative window by exactly that much and must fit inside $2R$:

$$\dot x_{\max}=\frac{2R}{\beta T}=\frac{2\times0.16}{0.50\times0.40}=\frac{0.32}{0.20}=1.60\ \mathrm{m/s}$$

The stroke limit binds first, and by a wide margin. At Q's frozen height and trot the legs run out of
stroke at $1.60$ m/s while the capture point at that speed is only $1.60/5.72=0.28$ m out, well
inside the $0.46$ m the leg can reach. Going faster is
therefore a *gait* change — a shorter stance — and not a balance problem at all, which is the reason
the table below is the object a locomotion paper is really varying when it reports a top speed.

**5. Gait timing.** **Duty factor** $\beta$ is the fraction of the gait period one foot spends in
stance, $\beta=T_{\mathrm{st}}/T$, a dimensionless number in $(0,1]$ defined per foot; the gaits
below are symmetric, so all four feet share one $\beta$ and differ only in phase offset. Example:
Q's nominal trot has $T_{\mathrm{st}}=0.20$ s out of $T=0.40$ s, so $\beta=0.50$. Non-example:
$\beta$ is not the number of feet on the ground — that is $4\beta$ on average, which is why
$\beta<0.25$ forces intervals with no foot down whatever the phase offsets are, and why a gallop is
a ballistic problem the LIP above cannot describe. It matters because $\beta$ is the only knob in
the stroke limit that a controller actually chooses.

| Gait | $\beta$ | $T_{\mathrm{st}}$ | $T_{\mathrm{sw}}$ | feet down, $4\beta$ on average | $\dot x_{\max}=2R/\beta T$ |
|---|---:|---:|---:|---|---:|
| crawl | $0.75$ | $0.30\,\mathrm{s}$ | $0.10\,\mathrm{s}$ | $3$ — exactly three at quarter-period offsets | $1.07\,\mathrm{m/s}$ |
| trot | $0.50$ | $0.20\,\mathrm{s}$ | $0.20\,\mathrm{s}$ | $2$ — one diagonal pair | $1.60\,\mathrm{m/s}$ |
| bound | $0.40$ | $0.16\,\mathrm{s}$ | $0.24\,\mathrm{s}$ | $1.6$ — fore or hind pair, flight in between | $2.00\,\mathrm{m/s}$ |
| gallop | $0.30$ | $0.12\,\mathrm{s}$ | $0.28\,\mathrm{s}$ | $1.2$ — feet in rotation, flight phases | $2.67\,\mathrm{m/s}$ |

Read the last column against the $2.63$ m/s balance limit: only at the gallop row do the two finally
meet. A quadruped shortens its stance not because balance demands it but because the leg runs out of
travel, and it arrives at the balance limit just as it arrives at a gait with no support polygon left.

**6. Friction, the one physical condition the learned line keeps.** Whatever the gait, the tangential
force summed over the feet cannot exceed $\mu$ times the vertical force they carry, and in steady
support that vertical total is $mg$, so the horizontal acceleration is capped independently of how
many feet are down:

$$a_{\max}=\frac{\mu\,m\,g}{m}=\mu g=0.6\times9.81=5.89\ \mathrm{m/s}^2$$

Reaching the $1.60$ m/s stroke limit from rest therefore takes at least $1.60/5.886=0.272$ s, most
of one gait cycle. Per foot: standing square, each carries $mg/4=29.43$ N; in the trot only two are
down, so each carries $mg/2=58.86$ N and may push sideways with at most $\mu f_z=0.6\times58.86=35.3$
N. Those three numbers are exactly what [[04-robotics/convex-mpc-legged|8. Convex MPC]] turns into
constraint rows, and the $\mu$ that produces them is the single physical condition §1.5 says the
learned controllers still rely on.

**7. What P2 costs Q.** Mount **P2** ([[02-foundations/lab-plants|0.6]]) with its shoulder at Q's
CoM. At P2's frozen pose $\theta=(0^\circ,90^\circ)$ its two $1$ kg masses sit $1$ m forward of the
shoulder, one at shoulder height and one $1$ m above it, so the combined body has

$$z'=\frac{12(0.30)+1(0.30)+1(1.30)}{14}=\frac{5.20}{14}=0.371\ \mathrm{m},\qquad \Delta x=\frac{1(1.0)+1(1.0)}{14}=0.143\ \mathrm{m}$$

because a centre of mass is the mass-weighted average of the parts. Two consequences, both bad.
The pendulum slows to $\omega_0'=\sqrt{9.81/0.371}=5.14$ rad/s, so the capture point at $1.0$ m/s
moves out from $0.175$ m to $0.195$ m. And the reach bracket is measured from the *new* CoM, which
has moved $0.143$ m forward into it, leaving $0.46-0.143=0.317$ m: the balance limit falls to
$5.14\times0.317=1.63$ m/s. The stroke limit has not moved. Carrying P2 collapses $2.63$ and $1.60$
m/s onto $1.63$ and $1.60$, and the margin between "the legs run out" and "it cannot stop" is gone.

Laterally, P2's frozen pose is in the sagittal plane, so it shifts no mass sideways but still raises
the CoM. Static tip-over about a lateral foot pair happens when the CoM projection crosses the
$0.15$ m half-width, at $\arctan(0.15/z)$ — $26.6^\circ$ bare and $\arctan(0.15/0.371)=22.0^\circ$
carrying P2. That $22.0^\circ$ is the slope gate the costmap on
[[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] uses.

### 2. The idea worth taking away: privileged teacher-student distillation

If you learn one thing from this page, learn this. It has no analogue in classical robotics,
and it — not any particular reward design — is what made rough-terrain locomotion work.

<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="a teacher trained on privileged simulator state is distilled into a student that sees only proprioceptive history">
  <g fill="currentColor">
    <rect x="24" y="52" width="150" height="76" rx="4" fill-opacity="0.14"/>
    <rect x="330" y="52" width="150" height="76" rx="4" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="52" width="150" height="76" rx="4"/><rect x="330" y="52" width="150" height="76" rx="4"/>
  </g>
  <g stroke="currentColor" stroke-width="3.4" fill="none" opacity="0.85" marker-end="url(#arL)">
    <line x1="180" y1="82" x2="324" y2="82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" marker-end="url(#arL)" stroke-dasharray="5 3">
    <path d="M 405 134 L 405 156 L 99 156 L 99 134"/>
  </g>
  <defs><marker id="arL" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="99" y="72">teacher</text>
    <text x="99" y="90" font-size="9.5" opacity="0.85">trained by RL, in simulation</text>
    <text x="99" y="106" font-size="9.5" opacity="0.85">sees privileged state</text>
    <text x="405" y="72">student</text>
    <text x="405" y="90" font-size="9.5" opacity="0.85">supervised by the teacher</text>
    <text x="405" y="106" font-size="9.5" opacity="0.85">sees proprioceptive history</text>
    <text x="252" y="76" font-size="10" opacity="0.85">distil</text>
    <text x="252" y="172" font-size="9.5" opacity="0.8">the student rolls out; the teacher labels the states it actually visited</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.9">
    <text x="24" y="196">privileged, and unavailable on the robot: terrain profile under each foot, contact states and forces,</text>
    <text x="24" y="210">friction coefficients, applied disturbances</text>
    <text x="24" y="232" font-size="11">The student never learns to see. It learns to INFER those quantities from how the body just moved.</text>
  </g>
</svg>

The teacher is trained by RL with access to **ground-truth simulator state** — the terrain
profile, contact states and forces, friction coefficients, applied disturbance forces. None
of that exists on the real robot. The teacher is then **distilled by supervised learning**
into a student that sees only a short history of proprioception, with DAgger-style data
collection: the student rolls out, the teacher labels the states the student actually
visited.

The student does not learn to perceive. It learns to **infer the privileged quantities from
how the body has just been moving** — which is why a blind robot can adapt to mud it cannot
see, after it has stepped in it.

**RMA** is a close relative that positions itself explicitly against Lee 2020 — no predefined trajectory generator and no actuator model — with a sharper deployment story in three steps.
First, it compresses a 17-dimensional privileged environment vector into an **8-dimensional latent** (these dimensions, the 0.5 s history and both rates are body figures, not abstract ones).
Second, an adaptation module estimates that latent from 0.5 s of proprioceptive history, by supervised regression trained
purely in simulation.
Third, the two parts run **asynchronously — base policy at 100 Hz, adaptation module
at 10 Hz — on a cheap robot's onboard CPU.**

The pattern has since generalised well past locomotion: multi-expert distillation into a
generalist, model-based experts relabelling passive data, and — in a different guise — the
teacher-student structure inside sim-to-real recipes generally
([[05-construction-robotics/sim-to-real|Sim-to-Real §2]]).

**What is inside the training loop these papers share.** The distillation story above is the
contribution; the four things below are the *recipe*, assumed without explanation in every
2024–26 locomotion method section. They are also where most of the engineering actually is.

- **Gait and contact schedule.** A gait is a pattern of which feet are on the ground when —
  *trot* (diagonal pairs), *bound*, *pace*, *crawl*. Model-based controllers are handed this
  as a **contact schedule** and solve for forces within it, which is what
  [[04-robotics/convex-mpc-legged|8. Convex MPC]] assumes. Learned controllers split on this,
  and the split runs through the canon below. Rudin 2021 and the parkour work impose no schedule, and the gait emerges from the reward.
  Lee 2020 and Miki 2022 build on a **foot
  trajectory generator** with a per-leg phase, and the policy outputs frequency offsets and
  residuals on top of it. Hwangbo 2019 outputs joint position targets directly, with no gait prior. The bipedal and humanoid lines almost always condition on a gait
  phase or a reference motion. So **check whether a schedule is imposed**; "learned
  locomotion" covers both.
- **Reward terms.** Locomotion reward is a weighted sum, and the weights are the method. The
  recurring groups: a **task** term (track the commanded velocity), **regularization** terms
  (penalize joint torque, joint velocity, action rate, orientation error), and **shaping**
  terms (foot clearance, air time, contact-force smoothness). Energy or
  bioenergetics-inspired penalties are what produce natural-looking gaits without prescribing
  one. **When a paper says "we use the standard reward", it means this stack.** Field
  folklore holds that removing a regularization term hurts hardware transfer more than it
  hurts simulated return — plausible, and worth knowing as a hypothesis, but the standard
  reference implementations publish no per-term ablation to support it.
- **Termination and curriculum.** Episodes end early on a fall or a bad body orientation, so
  termination *is* a reward signal. **Terrain curriculum** raises difficulty as the policy
  succeeds — flat, then rough, then stairs and gaps — because a policy that starts on the
  hardest terrain never gets enough successful episodes to learn from.
- **Domain randomization.** Sampling mass, friction, motor gains, latency and terrain
  parameters over a range at training time so the policy is forced to be robust across them
  rather than tuned to one. It is one of the two or three load-bearing sim-to-real
  techniques — alongside actuator modelling and privileged distillation, both of which this
  page already credits — and not a strict requirement: Xie et al. (ICRA 2021) transfer
  quadrupedal locomotion to hardware *without* dynamics randomization.
  [[05-construction-robotics/sim-to-real|Sim-to-Real §2]] treats it properly; the reading rule
  here is that **the randomization ranges are part of the result**. A policy robust over a
  ±20% friction range and one robust over ±60% are not the same claim, and the ranges live in
  an appendix table.

> [!warning] Randomization is not free robustness
> Widening the ranges makes the policy more robust and *less* performant — it must hedge
> against conditions it now sees. A paper reporting both a robustness result and a
> peak-performance result should say whether they came from the same policy. Domain
randomization also cannot fix an effect the simulator never models
> at all — though be careful which example you reach for.
> [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al.]] is *not*
> that case: their learned distrust is produced **by** randomization moved onto the
> exteroceptive channel — height-map noise at three scopes and three regimes, one of which
> simulates the map being absent entirely. It is evidence that randomizing the right channel
> works, not that randomization failed.

### 3. The canon, and what each result actually claimed

| Work | What it is famous for | What it actually claimed |
|---|---|---|
| **Hwangbo et al. 2019** | "RL locomotion" | the **actuator net** — a hybrid simulator. Demonstrated skills are flat-ground command following, record high-speed running, and **fall recovery**. Rough terrain is not the claim |
| **Lee et al. 2020** | rough-terrain locomotion | **blind** robustness via privileged distillation; mud, snow, rubble, vegetation, running water. Speed gains modest and terrain-specific |
| **Rudin et al. 2021** | "walk in minutes" | **wall-clock training time on one GPU** — not sample efficiency. Matters as infrastructure |
| **Miki et al. 2022** | "beat a human hiker" | perceptive locomotion with a **learned gate** on how much to trust the height map |
| **ANYmal parkour 2024** | parkour | **hierarchical** skills plus a high-level policy aware of each skill's capability envelope |

Three of those deserve expanding, because the gap between reputation and claim is where the
reading practice lives.

**Hwangbo 2019's contribution is a simulator, not a gait.** They keep analytical rigid-body
physics and replace the part nobody models well — the series-elastic actuator and its control
software — with a small network regressing joint torque from a history of position errors
and velocities, trained on **under four minutes of robot data**. The payoff is roughly
1000× real-time simulation on one workstation. Both figures are from the body; the abstract
carries neither. The durable idea is "learn the component you
cannot model, keep the physics you can" — and it is the ancestor of every sim-to-real
actuator-modelling result since.

**Rudin 2021 is infrastructure, and should be framed that way.** Thousands of robots in
parallel on a single workstation GPU, PPO (the standard on-policy policy-gradient algorithm, [[02-foundations/rl-basics|7. RL Basics §4]]) retuned for that regime, and a game-inspired
terrain curriculum that promotes and demotes robots by difficulty. The released
`legged_gym` / `rsl_rl` code is what made the 2022–2026 explosion economically possible in
ordinary labs. Its scientific claim is narrow; its causal influence is enormous. Keeping
those two things separate is exactly the kind of correction this wiki exists to make.

**Miki 2022's mechanism is the interesting part, not the hike.** An attention-based recurrent
**belief-state** encoder fuses proprioception with an exteroceptive height map and learns an
**adaptive gating factor** for how much of the map to trust — so when the map lies (snow,
tall grass, water, reflective surfaces) the controller degrades gracefully back to
proprioceptive locomotion, with no hand-designed rule for when to stop believing it.

> [!warning] Three over-citations to avoid
> - **The Alps hike is one instrumented route against a planner time**, not a benchmarked
>   comparison against human hikers. 2.2 km, 120 m of gain, 78 minutes against a hiking planner's
>   76-minute estimate (the summit took 31 minutes against 35 signposted).
> - **"Walk in minutes" is wall-clock on one GPU.** It consumes vastly *more* simulated
>   experience than prior work, and it is not real-robot learning time.
> - **The humanoid rough-terrain paper is a preprint.** Radosavovic et al.'s peer-reviewed
>   *Science Robotics* humanoid result is **blind flat-to-mildly-uneven outdoor walking**; the
>   challenging-terrain follow-up with the Berkeley trails and San Francisco hills is an
>   arXiv preprint that is frequently cited as though it were published.

### 4. The parkour contrast, and why it is instructive

Two papers months apart, opposite architectures, opposite hardware, and both called parkour.

| | **ANYmal parkour** (Science Robotics 2024) | **Extreme Parkour** (ICRA 2024) |
|---|---|---|
| Architecture | hierarchical: separate RL skills + a skill-selecting navigation policy | one monolithic network, depth to action |
| Perception | explicit obstacle reconstruction from occluded, noisy depth | a single front-facing depth camera, end to end |
| Hardware | ANYmal, ~50 kg research quadruped | low-cost robot, imprecise actuators |
| Notable mechanism | the high-level policy knows each skill's **capability envelope** | a learned inner yaw reward lets the policy **aim itself**, no separate planner |

Neither has been shown to generalise beyond hand-built or hand-selected obstacle courses.
The pair is worth reading together because it shows the field genuinely undecided between
composition and monolith at the same moment — and because **ANYmal parkour is where
locomotion crosses into navigation**: a high-level policy reasoning about which skill a
piece of terrain affords is skill-affordance-aware planning, and that is the actual interface
between this page and [[04-robotics/semantic-language-navigation|19]].

### 5. Where it went, 2025–2026

The centre of gravity moved from "can it walk on X" to **generalist and cross-embodiment
policies**, plus terrain-representation learning.

- **Attention-based map encoding** (Science Robotics, 2025) trains a terrain-map encoder
  conditioned on proprioception **end to end inside the RL controller**, learning to attend
  to steppable regions for future footholds — and demonstrates it on **both a 12-DoF ANYmal-D
  and a 23-DoF humanoid**, which is the notable part.
- **Parkour in the wild** (IJRR, 2026) distils terrain-specific experts into one generalist
  depth-input policy by DAgger, then RL fine-tunes on expanded terrain including real-world
  3D scans — collapsing ANYmal parkour's skill hierarchy into a single extensible policy.
- **High-speed control on discrete terrain** (Science Robotics, 2025) is a **planner-plus-learner
  hybrid**: sampling-based foothold optimisation with heuristic and neural filtering, plus an
  RL tracker. Stepping stones at 4 m/s, a 1.3 m gap jump. Worth citing as evidence the
  pendulum is swinging partly back toward hybrids for precision terrain.
- **LocoFormer** (CoRL 2025, Best Paper finalist) is the nearest thing to a locomotion
  foundation model: one policy for unseen legged *and wheeled* robots without precise
  kinematics, trained over procedurally generated morphologies, whose actual novelty is a
  context window extended to **span episode boundaries** — producing emergent cross-episode
  adaptation, so the policy learns from falls in earlier episodes.

There is no consensus locomotion foundation model, and no 2026 result of Miki-2022 or
Rudin-2021 stature. Saying so is more useful than naming a preprint.

### 6. The tooling, because it dates the papers

- **Isaac Gym Preview is formally deprecated** — NVIDIA's own page calls it legacy software
  that is no longer supported, and the `IsaacGymEnvs` / `OmniIsaacGymEnvs` repositories were
  archived read-only (GitHub exposes no archive date, so do not quote a month). A 2026 paper saying "we use Isaac Gym" is on a dead
  preview release.
- **Isaac Lab** is the successor; as of August 2026 the stable line is 2.3.x with 3.0 in beta.
- **MuJoCo Playground / MJX** is the credible vendor-neutral alternative and the reason MJX
  became an academic default.
- **Newton** — co-developed by Disney Research, Google DeepMind and NVIDIA, contributed to the
  Linux Foundation in September 2025 — is becoming the shared physics layer under both,
  integrating MuJoCo Warp as a backend. The Isaac/MuJoCo split is converging at the solver
  layer.

See [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]]
for the full picture and the licensing traps.

### After reading

- [ ] Draw Q's inverted pendulum and its gait chart, and mark the capture point inside the reach bracket.
- [ ] Say which of Q's two speed limits binds at the nominal trot, and what mounting P2 does to the other one.
- [ ] Draw the teacher-student diagram and name what is privileged.
- [ ] State what Hwangbo 2019 actually demonstrated.
- [ ] Explain why "walk in minutes" is not a sample-efficiency claim.
- [ ] Describe Miki's gating mechanism and what it is protecting against.
- [ ] Give the two parkour architectures and say what neither has shown.

> [!tip] Going deeper · 더 깊이
> The two halves of this page go to different places. For the classical vocabulary of §1.5 — support polygon, ZMP, capture point — Tedrake's free [*Underactuated Robotics*](https://underactuated.csail.mit.edu/) is the textbook treatment. For the learned line there is no book, and the substitute is four papers from §2–§3 read in publication order: Hwangbo et al. (2019) for the sim-to-real result, Lee et al. (2020) for privileged teacher–student, Kumar et al. (2021) for adaptation without privileged input at test time, Miki et al. (2022) for adding exteroception. Read them as one argument developing, not as four systems.

### Self-check

1. Why can a blind robot adapt to mud it cannot see?
2. A 2026 paper reports locomotion results trained in Isaac Gym. What do you note?
3. Someone cites Miki 2022 as evidence that robots now outperform human hikers. Correct them.
4. What does LocoFormer's extended context window actually buy?
5. Your project needs a legged platform to carry a manipulator over rough ground. Which
   result on this page is the closest precedent, and what does it not give you?

> [!tip]- Answers
> 1. Because the student was distilled from a teacher that *could* see the friction coefficient and terrain profile, and it learned to infer those quantities from a short history of proprioception — how the body actually moved over the last fraction of a second. It cannot anticipate the mud, but once a foot is in it the recent motion history is informative about what changed, and the policy was trained on exactly that inference. Blindness is why it must make contact first; distillation is why contact is enough.
> 2. That Isaac Gym Preview is deprecated — NVIDIA's own page calls it legacy and unsupported, and the associated env repositories are archived read-only. It does not invalidate the result, but it dates the work and makes reproduction harder, and a current project should be on Isaac Lab or MuJoCo MJX instead.
> 3. The comparison was **one instrumented alpine route** — 2.2 km, 120 m of elevation gain — completed in 78 minutes against a hiking planner's **76-minute estimate** for that route (summit in 31 minutes against 35 signposted). That is a single route against a published time, not a benchmark against human hikers, and the robot was slightly slower overall. The result is genuinely impressive; the claim it supports is narrower than the one usually attributed to it.
> 4. Adaptation *across* episodes rather than within one. With a context window spanning episode boundaries, the policy can condition on what happened in earlier attempts — including falls — so it improves within a deployment without any weight update. That is a different mechanism from RMA-style latent estimation, which adapts within an episode from proprioceptive history and resets when the episode does.
> 5. **ANYmal parkour**, because it is the only one whose high-level policy reasons about what a piece of terrain affords, which is what a mobile manipulator needs to reach a workspace. What it does not give you is the manipulator: it is a navigation-among-obstacles result on a curated course, with no arm, no payload, and no account of how carrying one changes the dynamics. The error-budget consequences of adding an arm are in [[04-robotics/navigation-mobile-manipulation|16. §4]].

**Worked: the three readings the homework asks.** “Walk in minutes” is teacher–student wall clock: the teacher sees friction; minutes are not sample efficiency. Hwangbo 2019 transferred agile quadruped skills, not “sim-to-real is solved.” Closest precedent for a manipulator over rubble is ANYmal parkour — still no arm, no payload.

### Problem set · 과제

Tier B. Using **Q**, this page, and **P2** from [[02-foundations/lab-plants|0.6]]. No simulator: the
Euler loop for a legged body is not on this page and you do not need one.

**The change of knobs.** Q crouches to $z=0.24$ m and walks a **crawl**, $\beta=0.75$ at the same
period $T=0.40$ s, with the four feet offset a quarter period apart in the order LF, RH, RF, LH.
Commanded speed $\dot x=0.6$ m/s. Leg length, hip offset, mass and $\mu$ are unchanged.

1. **Draw.** The picture above, both panels, for the crouched crawl. Top: the inverted pendulum
   at $z=0.24$ m, the capture point at $0.6$ m/s, and the reach bracket for the new standing height —
   mark whether $\xi$ is inside it and by how much. Bottom: the gait chart, four lanes, $0.30$ s of
   stance per lane wrapping around the period. Shade it, then write under the chart how many feet are
   down at every instant and say what shape the support polygon has.
2. **Derive.** (a) $\omega_0$ and $1/\omega_0$ at the crouch. (b) The foot excursion $R$ and the
   furthest foothold ahead of the CoM. (c) The crawl's stroke limit $2R/\beta T$ and the balance limit
   $\omega_0(d+R)$; say which one binds and by how much. (d) Now mount P2 at the shoulder as in the
   worked derivation, recompute $z'$, $\Delta x$ and the balance limit, and say whether the margin of
   (c) survives.
3. **Interpret.** The crouch changes two things at once: it speeds the pendulum up and it lengthens
   the stroke. Say why each happens from the formula, name what the crouch costs that neither formula
   shows, and then answer the reading question: which of §2–§3's learned results would have found this
   trade-off *without* being told it exists, and what does the LIP give you that the policy does not?
4. **Read.** Three claims, using §2–§6 only. (a) A paper says it "learns to walk in minutes." What is
   privileged in the teacher–student diagram, and why is wall-clock minutes not a sample-efficiency
   claim? (b) Hwangbo 2019 is cited as "sim-to-real is solved." What did it actually demonstrate, and
   what transfer does it not license? (c) You need a quadruped to carry a manipulator over rubble.
   Which result on this page is the closest precedent, and which two things does it still not give you?

> [!note]- How to draw it · 그리는 법
> - Top panel: the ground as a horizontal line, a dot for the CoM at the standing height $z$, a straight massless leg from it down to the stance foot $p$, and a horizontal velocity arrow $\dot x$ at the CoM.
> - Three marks on the ground: the foot $p$, the CoM's vertical projection $x$, and the capture point $\xi$ at $\dot x/\omega_0$ ahead of $x$.
> - A bracket on the ground from $d+R$ behind $x$ to $d+R$ ahead of it, labelled *reach*: that is where a foot can be placed at all (worked case: $0.46$ m each way at $z = 0.30$ m).
> - The top panel's whole question is whether $\xi$ lands inside that bracket, so mark it and write the margin.
> - Bottom panel: four horizontal lanes stacked, one per foot, labelled LF, RF, LH, RH, over a time axis covering one period $T = 0.40$ s.
> - Shade each lane where that foot is in stance, wrapping past the end of the period back to $0$ when a stance runs over it (worked case, the trot: LF and RH from $0$ to $0.20$ s, RF and LH from $0.20$ to $0.40$ s).
> - Mark every instant where the shaded set changes: those are the moments the support polygon changes shape, and the chart read as a table is the contact schedule [[04-robotics/convex-mpc-legged|8. Convex MPC]] is handed.

> [!tip]- Solutions
> 1. Top: $\xi$ sits $0.094$ m ahead of the CoM and the bracket now runs to $0.541$ m, so it is inside with roughly $0.45$ m to spare. Bottom: with $\beta=0.75$ and quarter-period offsets, exactly $4\beta=3$ feet are down at every instant, so the support polygon is a triangle that swaps one vertex every $0.10$ s and never collapses to a segment — the opposite of the trot in the lecture chart.
> 2. (a) $\omega_0=\sqrt{9.81/0.24}=6.39\,\mathrm{rad/s}$, $1/\omega_0=0.156\,\mathrm{s}$. (b) $R=\sqrt{0.34^2-0.24^2}=\sqrt{0.058}=0.241\,\mathrm{m}$, furthest foothold $0.30+0.241=0.541\,\mathrm{m}$. (c) Stroke $2(0.241)/0.30=1.61\,\mathrm{m/s}$; balance $6.39\times0.541=3.46\,\mathrm{m/s}$. Stroke binds, and the gap is wider than at standing height — but note the crawl at a crouch ($1.61$ m/s) matches the trot at full height ($1.60$ m/s), so the crouch bought back everything the higher duty factor cost. (d) $z'=(12(0.24)+1(0.24)+1(1.24))/14=4.36/14=0.311\,\mathrm{m}$, $\Delta x=0.143\,\mathrm{m}$ unchanged, $\omega_0'=5.61\,\mathrm{rad/s}$, balance $=5.61\times(0.541-0.143)=2.23\,\mathrm{m/s}$. The margin survives: $2.23$ against a stroke limit of $1.61$. At standing height the same arm erased the margin entirely, so crouching is the fix for carrying it.
> 3. $\omega_0=\sqrt{g/z}$ rises as $z$ falls, so the pendulum diverges faster and the controller has less time — that is the cost hidden in (a), and it is why a crouch is not free. $R=\sqrt{\ell^2-z^2}$ rises as $z$ falls because the leg's fixed length buys horizontal travel with the vertical it no longer spends. What neither formula shows is the joint torque: holding a crouch loads the knee against gravity for the whole stance, and the LIP has no torque in it at all. As for the reading question — all of them, in the sense that a reward for forward velocity plus a torque penalty selects exactly this trade without anyone writing $\sqrt{\ell^2-z^2}$ down; that is what §2 means by a limit cycle the network found on its own. What the LIP gives you that the policy does not is the *reason*: two closed-form limits you can check before building anything, and a way to say which of them a reported top speed was actually up against.
> 4. (a) The teacher sees friction and terrain; the student sees proprioception (and maybe a camera). Minutes are parallel-simulator wall clock, not environment steps per skill — Rudin's claim is throughput, not sample efficiency. (b) Agile skills on a quadruped transferred from a rigid-body sim with system ID and domain randomisation. Not contact-rich manipulation, not any other robot, not "solved." (c) ANYmal parkour (affordance at the high level). Not the arm, not the payload dynamics. Adding the manipulator is an error-budget problem [[04-robotics/navigation-mobile-manipulation|16. §4]] does not find in the locomotion papers — and §7 of the worked derivation gives you the two numbers it costs: the capture point moves out $0.175\to0.195$ m and the reach bracket loses $0.143$ m.

### Sources

- J. Hwangbo, J. Lee, A. Dosovitskiy, et al., "Learning agile and dynamic motor skills for legged robots," *Science Robotics*, vol. 4, no. 26, eaau5872, 2019 ([arXiv:1901.08652](https://arxiv.org/abs/1901.08652)).
- J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, M. Hutter, "Learning Quadrupedal Locomotion over Challenging Terrain," *Science Robotics*, vol. 5, no. 47, eabc5986, 2020 ([arXiv:2010.11251](https://arxiv.org/abs/2010.11251)) — privileged teacher-student.
- N. Rudin, D. Hoeller, P. Reist, M. Hutter, "Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning," CoRL 2021 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — `legged_gym` / `rsl_rl`.
- A. Kumar, Z. Fu, D. Pathak, J. Malik, "RMA: Rapid Motor Adaptation for Legged Robots," RSS 2021, DOI 10.15607/RSS.2021.XVII.011 ([arXiv:2107.04034](https://arxiv.org/abs/2107.04034)).
- T. Miki, J. Lee, J. Hwangbo, et al., "Learning robust perceptive locomotion for quadrupedal robots in the wild," *Science Robotics*, vol. 7, no. 62, eabk2822, 2022 ([arXiv:2201.08117](https://arxiv.org/abs/2201.08117)).
- D. Hoeller, N. Rudin, D. Sako, M. Hutter, "ANYmal parkour: Learning agile navigation for quadrupedal robots," *Science Robotics*, vol. 9, no. 88, eadi7566, 2024 ([arXiv:2306.14874](https://arxiv.org/abs/2306.14874)).
- X. Cheng, K. Shi, A. Agarwal, D. Pathak, "Extreme Parkour with Legged Robots," ICRA 2024, pp. 11443–11450 ([arXiv:2309.14341](https://arxiv.org/abs/2309.14341)); Z. Zhuang et al., "Robot Parkour Learning," CoRL 2023 oral ([arXiv:2309.05665](https://arxiv.org/abs/2309.05665)).
- I. Radosavovic, T. Xiao, B. Zhang, et al., "Real-world humanoid locomotion with reinforcement learning," *Science Robotics*, vol. 9, no. 89, eadi9579, 2024 ([arXiv:2303.03381](https://arxiv.org/abs/2303.03381)). The challenging-terrain follow-up, [arXiv:2410.03654](https://arxiv.org/abs/2410.03654), is **a preprint**.
- 2025–26: He, Zhang, Jenelten, et al., "Attention-based map encoding for learning generalized legged locomotion," *Science Robotics*, vol. 10, no. 105, eadv3604, 2025 ([arXiv:2506.09588](https://arxiv.org/abs/2506.09588)); Rudin, He, Aurand, Hutter, "Parkour in the wild," *IJRR*, 2026, DOI 10.1177/02783649261455067 ([arXiv:2505.11164](https://arxiv.org/abs/2505.11164)); Kim, Oh, Park, et al., "High-speed control and navigation for quadrupedal robots on complex and discrete terrain," *Science Robotics*, vol. 10, no. 102, eads6192, 2025 ([arXiv:2506.02835](https://arxiv.org/abs/2506.02835)); Liu, Pathak, Agarwal, "LocoFormer," CoRL 2025 ([arXiv:2509.23745](https://arxiv.org/abs/2509.23745)).

**Within this wiki**

- **Paper notes** — [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] · [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al. 2022]] · [[01-canonical-papers/notes/9-navigation/rma|RMA]] · [[01-canonical-papers/notes/9-navigation/anymal-parkour|ANYmal Parkour]]
- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — where these robots are sent
- [[04-robotics/convex-mpc-legged|Convex MPC for legged robots]] — the model-based side of the same problem
- [[05-construction-robotics/sim-to-real|Sim-to-Real for Field Robots]] — teacher-student as one strategy among several
- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — the tooling status in §6

## 한국어

*I군이다. [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 동역학]]과 [[02-foundations/rl-basics|7. RL 기초]] 위에 선다.
가져갈 발상은 특권 교사–학생 증류이고, 이 페이지는 동시에 과잉 인용을 교정하는 연습장이다.*

> [!note] 처음이라면 · First pass
> 먼저 §1 다음 §2 — 가져갈 발상은 특권 교사–학생 증류 하나다 — 그다음 각 정본이 실제로 무엇을 주장했는지 못 박아 둔 §3. §1.5는 고전 언어로 쓰인 이족 논문을 만났을 때를 위해 있다. 이 페이지의 장치와 그림, 그리고 그 위에서 끝까지 해 본 유도는 과제가 전제하는 강의다. 문헌이 아니라 수업 때문에 왔다면 장치 → 그림 → §1.5 → 유도 순서로 읽어라.

### 이 페이지의 장치 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 여섯 장치 중 다리 달린 몸은 없다. 그래서 이
페이지가 자기 장치를 고정하고, 다음 두 페이지는 새 장치를 만드는 대신 이것을 다시 쓴다.

**Q — 고정된 사족.** 질량 없는 다리 네 개 위의 단일 강체. 네 발을 정사각으로 딛고 선다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $m$ | $12\,\mathrm{kg}$ | 몸통 전체 질량 |
| $z$ | $0.30\,\mathrm{m}$ | 서 있을 때 무게중심 높이 |
| 고관절 직사각형 | $0.60\times0.30\,\mathrm{m}$ | 무게중심 아래 $(\pm0.30,\pm0.15)\,\mathrm{m}$의 발 |
| $\ell$ | $0.34\,\mathrm{m}$ | 고관절에서 발까지 다리 길이 |
| $\mu$ | $0.6$ | 발–지면 마찰계수 |
| $T$ | $0.40\,\mathrm{s}$ | 보행 주기 |
| $\beta$ | $0.50$ | 기준 trot의 듀티 팩터 |
| $h_{\max}$ | $0.15\,\mathrm{m}$ | 카탈로그가 허락하는 넘어설 수 있는 단차 |
| $f_{z,\max}$ | $200\,\mathrm{N}$ | 발당 수직력 한계 |
| $g$ | $9.81\,\mathrm{m/s}^2$ | 중력 |

규정에 해당하는 것은 마지막 네 줄뿐이다. $h_{\max}$와 $f_{z,\max}$는 P3의 손 강성이 그렇듯
카탈로그 숫자다 — 한 번 적고, 여기서 유도하지 않으며, 과제에서만 바꾼다. 나머지는 모두 위의
줄에서 계산되고, 아래의 어떤 숫자도 그 줄과 모순되지 않는다.

Q는 이 위키의 관통 과제를 나른다: [[02-foundations/lab-plants|0.6]]의 **P2**가 Q의 등에 타고,
아래 유도의 마지막이 그 팔이 몸통에 물리는 비용을 계산한다. Q는
[[04-robotics/convex-mpc-legged|8. Convex MPC]]에서 QP의 몸통으로,
[[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]]에서는 비용 지도를
받는 로봇으로 다시 나온다.

§1.5의 $z=0.9$ m 휴머노이드는 *다른* 몸이다. capture point 문헌이 그 크기에 대해 쓰였기 때문에
그대로 둔다. 두 숫자가 어긋나면 하나가 낡아서가 아니라 기계가 둘이기 때문이다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="위: 발을 놓을 수 있는 구간 괄호 안에 capture point가 들어온 고정 사족의 도립진자. 아래: 한 주기의 trot 보행 차트">
  <defs><marker id="arQk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.6"><line x1="40" y1="120" x2="520" y2="120"/></g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.9"><line x1="250" y1="58" x2="200" y2="120"/></g>
  <circle cx="250" cy="58" r="5" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.45" stroke-dasharray="3 3"><line x1="250" y1="58" x2="250" y2="120"/></g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.9" marker-end="url(#arQk)"><line x1="260" y1="58" x2="304" y2="58"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.8"><line x1="200" y1="114" x2="200" y2="126"/><line x1="250" y1="114" x2="250" y2="126"/><line x1="296" y1="114" x2="296" y2="126"/></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7"><line x1="130" y1="144" x2="370" y2="144"/><line x1="130" y1="138" x2="130" y2="150"/><line x1="370" y1="138" x2="370" y2="150"/></g>
  <g font-size="10" fill="currentColor">
    <text x="262" y="50" font-size="11">x&#775;</text>
    <text x="180" y="140" font-size="9.5" opacity="0.85">p</text>
    <text x="244" y="140" font-size="9.5" opacity="0.85">x</text>
    <text x="290" y="140" font-size="9.5" opacity="0.85">&#958;</text>
    <text x="262" y="34" opacity="0.85">무게중심, z = 0.30 m, m = 12 kg</text>
    <text x="250" y="164" font-size="9.5" text-anchor="middle" opacity="0.85">발을 놓을 수 있는 구간, 앞뒤로 0.46 m</text>
    <text x="40" y="184" font-size="10.5" opacity="0.9">&#958;가 괄호 안이면 한 걸음으로 아직 멈출 수 있다.</text>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.5"><line x1="80" y1="268" x2="480" y2="268"/><line x1="80" y1="268" x2="80" y2="274"/><line x1="280" y1="268" x2="280" y2="274"/><line x1="480" y1="268" x2="480" y2="274"/></g>
  <g fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6">
    <rect x="80" y="199" width="200" height="14" rx="2"/>
    <rect x="280" y="219" width="200" height="14" rx="2"/>
    <rect x="280" y="239" width="200" height="14" rx="2"/>
    <rect x="80" y="259" width="200" height="14" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="0.8" fill="none" opacity="0.35"><line x1="80" y1="199" x2="480" y2="199"/><line x1="80" y1="219" x2="480" y2="219"/><line x1="80" y1="239" x2="480" y2="239"/><line x1="80" y1="259" x2="480" y2="259"/></g>
  <g font-size="9.5" fill="currentColor" opacity="0.9">
    <text x="46" y="210">LF</text><text x="46" y="230">RF</text><text x="46" y="250">LH</text><text x="46" y="270">RH</text>
    <text x="80" y="286" text-anchor="middle">0</text><text x="280" y="286" text-anchor="middle">0.20 s</text><text x="480" y="286" text-anchor="middle">0.40 s</text>
    <text x="40" y="306" font-size="10.5">칠한 구간이 디딤. trot은 대각선 두 발이 0.20 s마다 교대한다.</text>
  </g>
</svg>

위는 선형 도립진자로 본 Q로, 높이 $z = 0.30$ m의 무게중심이 디딤발 $p$ 위에서 trot 명령 $\dot x = 1.0$ m/s로 움직이고, capture point $\xi$는 무게중심의 투영 $x$보다 $\dot x/\omega_0 = 0.175$ m 앞, 앞뒤로 $0.46$ m인 발 디딤 구간 괄호의 한참 안쪽에 있어 한 걸음으로 아직 멈출 수 있다. 아래는 한 주기 $T = 0.40$ s의 기준 trot으로, 앞 $0.20$ s는 LF와 RH가, 뒤 $0.20$ s는 RF와 LH가 디딤이고, 이 차트를 표로 읽은 것이 [[04-robotics/convex-mpc-legged|8. Convex MPC]]가 건네받는 접촉 스케줄이다.

### 1. 이 페이지가 존재하는 이유

이 문헌은 **실제 주장 너머로 체계적으로 과잉 인용된다.** 유명한 결과들이 대체로 옳은 이유로
유명해진 뒤, 그것이 보이지 않은 인접한 무언가에 대해 인용된다. 그래서 이 위키의 나머지가 요구하는
독해 규율을 연습하기 좋은 페이지이고, 아래의 교정들이 여기서 가장 쓸모 있는 내용이다.

직접적으로도 중요하다: [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]]의
대부분이 레그드 플랫폼 위에서 돌아가고, 이 분야의 가장 파급력 큰 학습 아이디어가 여기서 나왔다.

### 1.5 이 페이지가 쓰지 않는 고전 어휘

아래는 전부 학습 기반 계열이고, 대략 2019년 이전의 보행 논문 대부분이 쓰던 언어를 쓰지
않는다. 그 논문들을 읽으려면 그 언어가 여전히 필요하므로, 문해력 수준으로 여기 적어 둔다 —
그리고 이 페이지의 나머지에서 왜 빠져 있는지도 함께.

- **지지 다각형(support polygon)** — 지면 접촉점들의 볼록 껍질. 고전적 안정성 질문은 어떤
  점이 그 안에 머무는가다. 풀어 쓰면, 지면에 투영한 접촉점 $c_1,\dots,c_k$에 대해 합이 1인 음이 아닌 가중치로 만든 모든 가중 평균이다.
$$\mathcal{S}=\mathrm{conv}\{c_1,\dots,c_k\}=\Big\{\sum_i\lambda_ic_i:\ \lambda_i\ge0,\ \sum_i\lambda_i=1\Big\}$$
  **정적 안정성 기준**은 무게중심(CoM)의 수직 투영이 $\mathcal S$ 안에 있기를 요구한다. 음이 아닌 수직 발 힘들은 껍질 안에 놓인 합력만 만들 수 있고, 가만히 서 있으려면 그 합력이 CoM 바로 아래에 있어야 하기 때문이다. 예: 발이 $(\pm0.3,\pm0.15)$ m에 있으면 $0.6\times0.3$ m 직사각형이고, $(0.1,0.05)$ m의 CoM 투영은 그 안에 있다. 반례: 속보(trot)에서는 대각선 한 쌍만 땅에 있어 다각형이 둘 사이의 선분으로 줄어들고, CoM은 거의 그 선분 위에 있지 않다. 그래도 속보하는 로봇은 넘어지지 않는다. 속보는 정적으로가 아니라 동적으로 균형을 잡기 때문이다.
- **ZMP(zero-moment point)** — 지면 반력이 수평 모멘트를 만들지 않는 지면 위의 점. ZMP가
  지지 다각형 안에 확실히 있으면 발이 모서리를 축으로 회전하지 못하고, 경계에 닿으면 발이
  들린다. 그 시대의 보행 패턴 생성기는 사실상 로봇이 추종할 수 있는 ZMP 궤적을 만들어 내는
  장치다. 평지에서 ZMP는 접촉점들을 힘으로 가중 평균한 **압력 중심**과 일치한다.
$$p_{\text{ZMP}}=\frac{\sum_i f_{z,i}\,c_i}{\sum_i f_{z,i}}$$
  $f_{z,i}\ge0$는 접촉점 $c_i$의 수직력이다. 이 점에 대해 수직력들은 수평 모멘트를 만들지 않으므로 정의를 만족한다. 가중치가 음이 아니므로 실제 힘으로 잰 ZMP는 언제나 다각형 안에 있다. 기준이 문제 삼는 것은 *계획한 운동*이 요구하는 ZMP다. 높이 $z$가 일정한 CoM(아래의 선형 도립진자)에서 그 요구는 $p=x-(z/g)\,\ddot x$이고 $x$는 CoM의 수평 위치다. 예: $x=0.3,0.3,-0.3,-0.3$ m의 네 발이 $40,30,20,10$ N을 받치면 ZMP는 $x=0.12$ m다. $z=0.9$ m의 CoM이 앞으로 $1$ m/s²로 가속하면 CoM보다 $0.9/9.81=0.092$ m 뒤의 ZMP를 요구하므로, CoM 뒤로 $0.125$ m까지 뻗은 발은 요구 ZMP가 발을 벗어나 발이 들리기 전까지 최대 $9.81\times0.125/0.9=1.36$ m/s²를 허용한다.
- **Capture point / DCM(divergent component of motion)** — 완전히 멈추려면 다음 발을 어디에
  디뎌야 하는가. 무게중심 높이 $z$의 선형 도립진자 모형에서 $\;\omega_0 = \sqrt{g/z}\;$이고,
  capture point는 무게중심보다 $\;\dot x/\omega_0\;$만큼 앞에 있다. **계산 예제:**
  $z = 0.9$ m인 휴머노이드는 $\omega_0 = \sqrt{9.81/0.9} = 3.30$ rad/s이므로
  $\dot x = 0.5$ m/s에서 멈추려면 $0.5/3.30 = 0.15$ m 앞을 디뎌야 하고, $1.0$ m/s에서는
  $0.30$ m다. DCM은 현대 전신 제어기가 쓰는 3차원 일반화다. 그 뒤의 모델은 **선형 도립진자**다. 높이 $z$가 일정한 점질량이 질량 없는 다리 위에 있고, 그 발(곧 ZMP)이 $p$에 있다. 동역학과 capture point $\xi$는 다음과 같다.
$$\ddot x=\omega_0^2\,(x-p),\qquad \xi=x+\frac{\dot x}{\omega_0},\qquad \dot\xi=\omega_0\,(\xi-p)$$
  마지막 식은 $\xi$를 미분하고 첫 식을 대입하면 나온다. 비율 $\omega_0$가 양수이므로 발을 $\xi$ 위에 놓지 않으면 $\xi$는 $p$에서 지수적으로 멀어진다. 거기에 놓으면 $\dot\xi=0$이 되고 CoM이 발 위에서 멈춘다. 반례: $\omega_0=3.30$ rad/s에서 $\xi$보다 5 cm 짧게 디디면 그 간격이 반 초 만에 $0.05\,e^{3.30\times0.5}=0.26$ m로 커진다.

**이 페이지가 그중 아무것도 쓰지 않는 이유.** ZMP는 평평하고 알려진 동일 평면의 지지면과,
그 면에 발이 온전히 닿는 상황을 전제한다. 학습 계열이 의도적으로 포기한 것이 바로 그
전제다: 잔해 위, 경사면, 발끝만 걸친 디딤에서는 지지 다각형이 ZMP가 요구하는 그 대상이
아니다. 그것을 대신하는 것은 더 나은 기준이 아니라 다른 거래다: 제어기는 검증된 균형 기준을
포기하고, 그 대가로 정책이 1초에 50번 외란에 반응하되 믿는 물리 조건은 하나뿐이다 — 발이
미끄러지지 않는다는 것([[04-robotics/convex-mpc-legged|8. Convex MPC]]는
접촉 스케줄을 *미리 지정*하는 방식으로 그 거래의 모델 기반 쪽을 유지한다).

정리하면: 휴머노이드·이족·전신 제어 논문에서는 ZMP와 capture point를 예상하고, §3이 다루는
학습 기반 결과들에서는 그것들의 부재를 예상하라. 어느 쪽 부재도 실수가 아니다.

**세 번째 단어: 극한주기(limit cycle).** 극한주기는 상태 공간 안의 고립된 닫힌 궤적이다 —
비선형계가 스스로 선호하는 진동이고, 살짝 밀면 그리로 되돌아오며, 주기를 일러 주는 외부 시계가
없다. 정상적인 보행 걸음새가 정확히 이것이고, 그렇게 읽으면 두 가지가 한꺼번에 설명된다. 첫째,
*수동 동보행기(passive dynamic walker)* — 구동기가 하나도 없이 완만한 경사를 중력만으로
걸어 내려가는 다리 기계 — 가 왜 작동하는가. 걸음새가 그 기구의 안정한 극한주기이고, 경사는
발이 땅에 닿을 때마다 잃는 에너지만큼만 값을 치른다. 둘째, 보행기에게 "안정"이 무슨 뜻인가.
상태가 한 점 근처에 머무는 것(보행기는 결코 정지해 있지 않다)이 아니라, 교란 뒤에 궤적이 그
주기로 되돌아오는 것이다. 걸음새 안정성을 *복귀 사상(return map)* — 직전 발 착지의 상태에
대한 함수로서 이번 발 착지의 상태 — 으로 연구하는 이유이고, 정적 기준(지지 다각형 안의 무게중심 투영)과 동적 ZMP 기준을 모두
어기면서도 이 의미에서는 안정할 수 있는 이유다.

**같은 발상을 식으로.** 시스템 $\dot x=f(x)$에서 **주기 궤도**는 가장 작은 주기 $T>0$에 대해 $x(t+T)=x(t)$인 해이고, 그것이 고립되어 있을 때, 곧 임의로 가까운 곳에 다른 주기 궤도가 없을 때 **극한주기**다. **복귀 사상**(푸앵카레 사상)은 한 주기에 한 번, 발 착지마다 상태를 표본으로 뽑는다: $x_{k+1}=P(x_k)$. 주기적 걸음새는 그 사상의 고정점이고, 거기서 사상의 야코비안 고유값이 모두 크기 1 미만이면 국소적으로 안정하다.
$$x^\star=P(x^\star),\qquad \Big|\lambda_i\Big(\tfrac{\partial P}{\partial x}(x^\star)\Big)\Big|<1$$
작은 편차 $\delta_k=x_k-x^\star$가 $\delta_{k+1}\approx\frac{\partial P}{\partial x}\delta_k$로 진화하며 줄어들기 때문이다. 예: $P(x)=0.5x+0.1$은 $x^\star=0.2$, 기울기 $0.5$이므로 $0.3$에서 시작하면 $0.25,\ 0.225,\dots$로 가고 편차가 매 걸음 절반이 된다. 반례: $P(x)=1.2x-0.04$는 고정점이 같지만 편차가 걸음마다 $1.2$배로 커지는 불안정한 주기다. 또 감쇠 없는 조화 진동자는 모든 진폭에서 닫힌 궤도를 가져 고립이 아니라 연속체이므로 그중 어느 것도 극한주기가 아니고, 밀면 이웃 궤도로 옮겨 갈 뿐이다.

§3의 학습된 정책들은 이 개념을 결코 이름 부르지 않지만 물려받는다. 보행 보상이 걸음새를
지정하지 않고 전진 속도만 보상할 때 실제로 골라내는 것은, 신경망이 스스로 찾아낸 극한주기다.
그 논문들에서 시키지 않았는데 나타나는 속보(trot)와 바운드 패턴이 바로 그 대상이 요청 없이
등장한 것이다.

- M. Vukobratović, B. Borovac, "Zero-moment point — thirty five years of its life,"
  *International Journal of Humanoid Robotics*, vol. 1, no. 1, 2004.
- J. Pratt, J. Carff, S. Drakunov, A. Goswami, "Capture Point: A Step toward Humanoid Push
  Recovery," *Humanoids 2006*.
- J. Englsberger, C. Ott, A. Albu-Schäffer, "Three-Dimensional Bipedal Walking Control Based
  on Divergent Component of Motion," *IEEE Transactions on Robotics*, vol. 31, no. 2, 2015.

### 장치로 한 번 끝까지 · Worked on Q

여기 있는 것은 전부 §1.5의 선형 도립진자를 Q의 줄에 대입한 것이고, 거기에 그것을 속도 한계로
바꾸는 보행 산수를 더한 것이다. 여기서 한 번 해 두면 과제는 첫 유도가 아니라 손잡이를 하나
돌리는 일이 된다.

**1. 시간 상수.** 도립진자는 $\ddot x=\omega_0^2(x-p)$를 따르고 $\omega_0=\sqrt{g/z}$인데, 이
비율은 높이 하나로만 정해진다 — 질량도, 다리 길이도, 몇 발이 땅에 있는지도 들어가지 않는다.
그래서 Q의 값은 서 있는 높이를 정하는 순간 함께 정해진다.

$$\omega_0=\sqrt{\frac{g}{z}}=\sqrt{\frac{9.81}{0.30}}=5.72\ \mathrm{rad/s},\qquad \frac{1}{\omega_0}=0.175\ \mathrm{s}$$

바로잡지 않은 기울어짐은 $0.175$ s마다 $e$배로 커지므로, 아무도 값을 치르지 않은 $5$ cm 오차는
시간 상수 하나 뒤에 $0.05\,e^{1}=0.136$ m가 된다. 10 Hz 제어기는 시간 상수당 표본을 둘도
얻지 못한다. §2의 정책이 50 Hz 이상으로 도는 이유, 그리고 모든 보행 스택에 빠른 내부 루프가 있는
이유가 이 산수다.

**2. Capture point.** §1.5에서 $\xi=x+\dot x/\omega_0$이고 다음 발을 $\xi$에 놓으면
$\dot\xi=0$이 되므로, Q를 한 걸음에 멈추려면 발이 무게중심보다 앞서야 하는 거리는 다음과 같다.

$$\xi-x=\frac{\dot x}{\omega_0}=\frac{1.0}{5.72}=0.175\ \mathrm{m}$$

trot 명령 $\dot x=1.0$ m/s에서의 값이다. 숫자 자체는 작다. 문제는 Q의 다리가 거기에 닿느냐다.

**3. 발이 실제로 갈 수 있는 곳.** 고관절은 무게중심보다 $d=0.30$ m 앞에 있다(고관절 직사각형의
절반). 발은 고관절을 중심으로 반지름 $\ell=0.34$ m인 구 위에 있고, 고관절이 서 있는 높이에 있는
동안 그 직각삼각형의 수직 변은 $z=0.30$ m이므로 남는 수평 여유는 다음과 같다.

$$R=\sqrt{\ell^2-z^2}=\sqrt{0.34^2-0.30^2}=\sqrt{0.0256}=0.16\ \mathrm{m}$$

따라서 고관절 기준 창은 $2R=0.32$ m 폭이고, 무게중심 앞 가장 먼 디딤점은 $d+R=0.30+0.16=0.46$
m다. 이 $0.46$ m가 위 그림의 괄호다.

**4. 속도 한계 둘, 그리고 먼저 걸리는 쪽.** 첫째는 균형이다. 한 걸음 정지에는 $\xi-x\le d+R$가
필요하므로 $\dot x\le\omega_0(d+R)=5.72\times0.46=2.63$ m/s다. 둘째는 스트로크다. 디딤 동안 발은
지면에 고정되고 고관절은 $\dot x\,\beta T$만큼 앞으로 가므로, 발은 고관절 기준 창을 정확히 그만큼
뒤로 쓸고 지나가며 그것이 $2R$ 안에 들어와야 한다.

$$\dot x_{\max}=\frac{2R}{\beta T}=\frac{2\times0.16}{0.50\times0.40}=\frac{0.32}{0.20}=1.60\ \mathrm{m/s}$$

스트로크 한계가, 그것도 큰 차이로 먼저 걸린다. Q의 고정된 높이와 trot에서 다리는 $1.60$ m/s에서
행정이 바닥나는데 그 속도의 capture point는 $1.60/5.72=0.28$ m밖에 안 나가 있어 다리가 닿는
$0.46$ m 안쪽에 넉넉히 들어온다. 그러니 더 빨리 가는 것은
*보행 양식*을 바꾸는 일 — 디딤을 짧게 하는 일 — 이지 균형 문제가 아니다. 보행 논문이 최고 속도를
보고할 때 실제로 건드리고 있는 대상이 아래 표인 이유가 이것이다.

**5. 보행 타이밍.** **듀티 팩터** $\beta$는 한 발이 한 주기 중 디딤으로 보내는 비율,
$\beta=T_{\mathrm{st}}/T$이고, $(0,1]$의 무차원 수이며 발마다 정의된다. 아래 보행 양식들은
대칭이라 네 발이 $\beta$ 하나를 공유하고 위상 차만 다르다. 예: Q의 기준 trot은 $T=0.40$ s 중
$T_{\mathrm{st}}=0.20$ s이므로 $\beta=0.50$이다. 반례: $\beta$는 땅에 있는 발의 수가 아니다. 그
수는 평균 $4\beta$이고, 그래서 $\beta<0.25$이면 위상 차가 어떻든 발이 하나도 없는 구간이 생기며,
갤럽이 위의 도립진자로는 서술할 수 없는 탄도 문제인 것도 그 때문이다. 이것이 중요한 이유는
스트로크 한계에서 제어기가 실제로 고르는 손잡이가 $\beta$뿐이기 때문이다.

| 보행 양식 | $\beta$ | $T_{\mathrm{st}}$ | $T_{\mathrm{sw}}$ | 땅에 있는 발, 평균 $4\beta$ | $\dot x_{\max}=2R/\beta T$ |
|---|---:|---:|---:|---|---:|
| crawl | $0.75$ | $0.30\,\mathrm{s}$ | $0.10\,\mathrm{s}$ | $3$ — 4분의 1 주기 위상이면 정확히 셋 | $1.07\,\mathrm{m/s}$ |
| trot | $0.50$ | $0.20\,\mathrm{s}$ | $0.20\,\mathrm{s}$ | $2$ — 대각선 한 쌍 | $1.60\,\mathrm{m/s}$ |
| bound | $0.40$ | $0.16\,\mathrm{s}$ | $0.24\,\mathrm{s}$ | $1.6$ — 앞 또는 뒤 한 쌍, 사이에 체공 | $2.00\,\mathrm{m/s}$ |
| gallop | $0.30$ | $0.12\,\mathrm{s}$ | $0.28\,\mathrm{s}$ | $1.2$ — 발이 돌아가며, 체공 구간 있음 | $2.67\,\mathrm{m/s}$ |

마지막 열을 $2.63$ m/s의 균형 한계와 나란히 읽어라. 둘이 마침내 만나는 곳은 갤럽 줄뿐이다.
사족이 디딤을 줄이는 것은 균형이 요구해서가 아니라 다리 행정이 바닥나서이고, 지지 다각형이 더는
남지 않는 보행 양식에 이르는 바로 그때 균형 한계에도 도달한다.

**6. 마찰, 학습 계열이 유일하게 지키는 물리 조건.** 보행 양식이 무엇이든 발들의 접선력 합은
그들이 받치는 수직력의 $\mu$배를 넘을 수 없고, 정상 지지에서 그 수직 총합은 $mg$다. 그래서 수평
가속도는 땅에 있는 발의 수와 무관하게 묶인다.

$$a_{\max}=\frac{\mu\,m\,g}{m}=\mu g=0.6\times9.81=5.89\ \mathrm{m/s}^2$$

정지에서 $1.60$ m/s의 스트로크 한계까지 가는 데 최소 $1.60/5.886=0.272$ s, 곧 한 보행 주기의
대부분이 든다. 발당으로 보면, 정사각으로 서 있을 때는 각각 $mg/4=29.43$ N을 받치고, trot에서는
둘만 땅에 있으므로 각각 $mg/2=58.86$ N을 받치며 옆으로는 많아야
$\mu f_z=0.6\times58.86=35.3$ N을 밀 수 있다. 이 세 숫자가 정확히
[[04-robotics/convex-mpc-legged|8. Convex MPC]]가 제약 행으로 바꾸는 것이고, 그것을 만들어 내는
$\mu$가 §1.5가 말한 대로 학습 제어기도 여전히 기대는 유일한 물리 조건이다.

**7. P2가 Q에 물리는 비용.** [[02-foundations/lab-plants|0.6]]의 **P2**를 어깨가 Q의 무게중심에
오도록 얹는다. P2의 고정 자세 $\theta=(0^\circ,90^\circ)$에서 $1$ kg 질량 둘은 어깨보다 $1$ m
앞에 있고 하나는 어깨 높이, 하나는 그보다 $1$ m 위에 있다. 그래서 합쳐진 몸은 다음과 같다.

$$z'=\frac{12(0.30)+1(0.30)+1(1.30)}{14}=\frac{5.20}{14}=0.371\ \mathrm{m},\qquad \Delta x=\frac{1(1.0)+1(1.0)}{14}=0.143\ \mathrm{m}$$

무게중심이 부분들의 질량 가중 평균이기 때문이다. 나쁜 귀결이 둘이다. 진자가
$\omega_0'=\sqrt{9.81/0.371}=5.14$ rad/s로 느려져 $1.0$ m/s에서의 capture point가 $0.175$ m에서
$0.195$ m로 멀어진다. 그리고 괄호는 *새* 무게중심에서 재는데 그 무게중심이 괄호 안쪽으로
$0.143$ m 들어와 버려 $0.46-0.143=0.317$ m만 남고, 균형 한계가 $5.14\times0.317=1.63$ m/s로
떨어진다. 스트로크 한계는 그대로다. P2를 실으면 $2.63$과 $1.60$ m/s가 $1.63$과 $1.60$으로
포개지고, "다리가 바닥난다"와 "멈추지 못한다" 사이의 여유가 사라진다.

측면으로는, P2의 고정 자세가 시상면 안에 있어 옆으로 질량을 옮기지는 않지만 무게중심은
그대로 올린다. 측면 발 한 쌍을 축으로 한 정적 전복은 무게중심 투영이 $0.15$ m 반폭을 넘을 때
일어나므로 각도는 $\arctan(0.15/z)$ — 맨몸 $26.6^\circ$, P2를 실으면
$\arctan(0.15/0.371)=22.0^\circ$다. 이 $22.0^\circ$가
[[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]]의 비용 지도가 쓰는
경사 관문이다.

### 2. 가져갈 발상: privileged teacher-student 증류

이 페이지에서 하나만 배운다면 이것이다. 고전 로보틱스에 대응물이 없고, 거친 지형 로코모션을
동작하게 만든 것이 어떤 보상 설계가 아니라 이것이다.

<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="시뮬레이터의 특권적 상태로 학습한 교사가 고유수용감각 이력만 보는 학생으로 증류된다">
  <g fill="currentColor">
    <rect x="24" y="52" width="150" height="76" rx="4" fill-opacity="0.14"/>
    <rect x="330" y="52" width="150" height="76" rx="4" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="52" width="150" height="76" rx="4"/><rect x="330" y="52" width="150" height="76" rx="4"/>
  </g>
  <g stroke="currentColor" stroke-width="3.4" fill="none" opacity="0.85" marker-end="url(#arLk)">
    <line x1="180" y1="82" x2="324" y2="82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" marker-end="url(#arLk)" stroke-dasharray="5 3">
    <path d="M 405 134 L 405 156 L 99 156 L 99 134"/>
  </g>
  <defs><marker id="arLk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="99" y="72">교사</text>
    <text x="99" y="90" font-size="9.5" opacity="0.85">시뮬레이션에서 RL로 학습</text>
    <text x="99" y="106" font-size="9.5" opacity="0.85">특권적 상태를 본다</text>
    <text x="405" y="72">학생</text>
    <text x="405" y="90" font-size="9.5" opacity="0.85">교사가 지도한다</text>
    <text x="405" y="106" font-size="9.5" opacity="0.85">고유수용감각 이력만 본다</text>
    <text x="252" y="76" font-size="10" opacity="0.85">증류</text>
    <text x="252" y="172" font-size="9.5" opacity="0.8">학생이 실행하고, 학생이 실제로 방문한 상태를 교사가 라벨한다</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.9">
    <text x="24" y="196">특권적이며 실제 로봇에는 없는 것: 각 발 밑의 지형 프로파일, 접촉 상태와 힘,</text>
    <text x="24" y="210">마찰계수, 가해진 외란</text>
    <text x="24" y="232" font-size="11">학생은 보는 법을 배우지 않는다. 몸이 방금 어떻게 움직였는지에서 그 양들을 추론하는 법을 배운다.</text>
  </g>
</svg>

교사는 **시뮬레이터의 실제 상태**에 접근한 채 RL로 학습된다 — 지형 프로파일, 접촉 상태와 힘,
마찰계수, 가해진 외란력. 그중 무엇도 실제 로봇에는 없다. 그다음 교사는 짧은 고유수용감각 이력만
보는 학생으로 **지도학습을 통해 증류**되며, 데이터 수집은 DAgger식이다: 학생이 실행하고, 학생이
실제로 방문한 상태를 교사가 라벨한다.

학생은 지각하는 법을 배우지 않는다. **몸이 방금 어떻게 움직였는가로부터 특권적 양들을 추론하는
법**을 배운다 — 눈이 먼 로봇이 보지 못하는 진흙에, 한 번 밟은 뒤에는 적응할 수 있는 이유다.

**RMA**는 Lee 2020에 맞서 자신을 명시적으로 위치시킨 가까운 친척이고 — 미리 정한 궤적 생성기도 액추에이터 모델도 없다 — 배치 이야기가 세 단계로 더 날카롭다.
첫째, 17차원 특권적 환경 벡터를 **8차원 잠재**로 압축한다(이 차원·0.5초 이력·두 주기는 초록이 아니라 본문 수치다).
둘째, 적응 모듈이 그 잠재를 0.5초의 고유수용감각 이력에서 지도 회귀로 추정하며, 이 회귀는
전적으로 시뮬레이션에서 학습한다.
셋째, 두 부분이 **비동기로 — 기본 정책 100 Hz, 적응 모듈 10 Hz — 저가 로봇의
온보드 CPU에서** 돌아간다.

이 패턴은 이후 로코모션을 훨씬 넘어 일반화되었다: 다수 전문가를 일반가로 증류하기, 모델 기반
전문가가 수동 데이터를 다시 라벨하기, 그리고 다른 옷을 입고 sim-to-real 레시피 일반의 교사-학생
구조로([[05-construction-robotics/sim-to-real|Sim-to-Real §2]]).

**이 논문들이 공유하는 학습 루프 안에 있는 것.** 위의 증류 이야기가 기여라면, 아래 넷은
*레시피*이고, 2024~26년 모든 로코모션 방법 절이 설명 없이 전제한다. 실제 공학의 대부분도
거기에 있다.

- **보행 양식과 접촉 스케줄.** 보행 양식은 어느 발이 언제 땅에 있는지의 패턴이다 —
  *trot*(대각쌍), *bound*, *pace*, *crawl*. 모델 기반 제어기는 이것을 **접촉 스케줄**로 받아
  그 안에서 힘을 푸는데, [[04-robotics/convex-mpc-legged|8. Convex MPC]]가 전제하는 것이 그것이다.
  학습 제어기는 여기서 갈리고, 그 갈림이 아래 정본 표를 관통한다. Rudin 2021과
  파쿠르 연구는 스케줄을 부과하지 않고 보행 양식이 보상에서 창발한다.
  Lee 2020과 Miki 2022는 다리별 위상을 갖는 **발 궤적 생성기**
  위에 세워져 있고, 정책은 그 위에서 주파수 오프셋과 잔차를 낸다. Hwangbo 2019는 보행 사전 없이 관절 위치 목표를 직접 낸다. 2족과 휴머노이드 계열은 거의 언제나
  보행 위상이나 참조 동작에 조건화한다. 그러니 **스케줄이 부과되었는지 확인하라.**
  "학습된 로코모션"이 둘 다 덮는다.
- **보상 항.** 로코모션 보상은 가중합이고, 그 가중치가 곧 방법이다. 반복되는 묶음: **과제** 항
  (명령된 속도 추종), **정규화** 항(관절 토크·관절 속도·행동 변화율·자세 오차에 벌점),
  **정형화(shaping)** 항(발 여유 높이, 체공 시간, 접촉력 매끄러움). 에너지나 생체에너지학에서
  착안한 벌점이 양식을 지정하지 않고도 자연스러워 보이는 보행을 만들어 낸다. **논문이 "표준
  보상을 쓴다"고 하면 이 묶음을 뜻한다.** 정규화 항 하나를 빼면 시뮬레이션 리턴보다 하드웨어
  전이가 더 나빠진다는 것이 현장의 통설이고 — 그럴듯하고 가설로 알아둘 값어치가 있지만 —
  표준 참조 구현들은 그것을 뒷받침할 항별 절제 실험을 공개하지 않는다.
- **종료와 커리큘럼.** 넘어지거나 몸 자세가 나빠지면 에피소드가 조기 종료되므로, 종료 조건이
  *곧* 보상 신호다. **지형 커리큘럼**은 정책이 성공함에 따라 난이도를 올린다 — 평지, 그다음
  거친 지형, 그다음 계단과 틈 — 가장 어려운 지형에서 시작한 정책은 배울 만한 성공 에피소드를
  충분히 얻지 못하기 때문이다.
- **도메인 무작위화.** 학습 시점에 질량·마찰·모터 이득·지연·지형 파라미터를 어떤 범위에서
  표본으로 뽑아, 정책이 하나에 맞춰지는 대신 그 전체에 걸쳐 강건해지도록 강제하는 것. 이 분야에서
  무게를 지는 두세 가지 sim-to-real 기법 중 하나이고 — 이 페이지가 이미 공을 돌린 액추에이터
  모델링과 특권 증류가 나머지다 — 절대 요건도 아니다: Xie 등(ICRA 2021)은 동역학 무작위화
  *없이* 4족 로코모션을 하드웨어로 전이한다.
  [[05-construction-robotics/sim-to-real|Sim-to-Real §2]]가 제대로 다루고, 여기서의 읽기 규칙은
  **무작위화 범위가 결과의 일부**라는 것이다. 마찰 ±20% 범위에서 강건한 정책과 ±60%에서 강건한
  정책은 같은 주장이 아니고, 그 범위는 부록 표에 있다.

> [!warning] 무작위화는 공짜 강건함이 아니다
> 범위를 넓히면 정책은 더 강건해지고 성능은 *떨어진다* — 이제 보게 된 조건들에 대비해 헤지해야
> 하기 때문이다. 강건성 결과와 최고 성능 결과를 함께 보고하는 논문은 그 둘이 같은 정책에서
> 나왔는지 밝혀야 한다. 도메인 무작위화는 시뮬레이터가 아예 모형화하지 않는 효과를 고칠 수도
> 없다 — 다만 어떤 예를 드는지 조심해야 한다.
> [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등]]은 그 사례가
> *아니다*: 그들의 학습된 불신은 무작위화를 외수용 채널로 옮겨서 **만들어 낸** 것이다 —
> 세 가지 범위와 세 가지 체제의 높이지도 잡음이고, 그중 하나는 지도가 아예 없는 상황을
> 흉내 낸다. 무작위화가 실패했다는 증거가 아니라 올바른 채널을 무작위화하면 통한다는 증거다.

### 3. 정본과, 각 결과가 실제로 주장한 것

| 연구 | 무엇으로 유명한가 | 실제로 무엇을 주장했나 |
|---|---|---|
| **Hwangbo 등 2019** | "RL 로코모션" | **액추에이터 넷** — 하이브리드 시뮬레이터. 실증된 기술은 평지 명령 추종, 기록적인 고속 달리기, **넘어짐 복구**. 거친 지형은 주장이 아니다 |
| **Lee 등 2020** | 거친 지형 로코모션 | privileged 증류를 통한 **눈먼** 견고성. 진흙·눈·잔해·초목·흐르는 물. 속도 이득은 완만하고 지형에 특정적 |
| **Rudin 등 2021** | "몇 분 만에 걷기" | **GPU 하나에서의 벽시계 학습 시간** — 샘플 효율이 아니다. 인프라로서 중요 |
| **Miki 등 2022** | "사람 등산객을 이겼다" | 높이 지도를 얼마나 믿을지에 대한 **학습된 게이트**를 가진 지각 로코모션 |
| **ANYmal parkour 2024** | 파쿠르 | **계층적** 스킬 + 각 스킬의 능력 범위를 아는 상위 정책 |

셋은 풀어 쓸 값이 있다. 명성과 주장 사이의 간극이 곧 독해 실습이 사는 곳이기 때문이다.

**Hwangbo 2019의 기여는 걸음걸이가 아니라 시뮬레이터다.** 해석적 강체 물리를 유지하고, 아무도
잘 모델링하지 못하는 부분 — 직렬 탄성 액추에이터와 그 제어 소프트웨어 — 을 위치 오차와 속도의
이력에서 관절 토크를 회귀하는 작은 네트워크로 대체한다. **4분 미만의 로봇 데이터**로 학습한다. 이 수치와 실시간 대비 1000배 배속은 초록이 아니라 본문의 것이다.
대가는 워크스테이션 한 대에서 실시간의 약 1000배 시뮬레이션이다. 남는 발상은 "모델링할 수 없는
구성 요소는 배우고, 할 수 있는 물리는 지켜라"이며, 이후 모든 sim-to-real 액추에이터 모델링 결과의
조상이다.

**Rudin 2021은 인프라이고, 그렇게 서술해야 한다.** 워크스테이션 GPU 하나에서 수천 로봇을 병렬로,
그 체제에 맞춰 재조율한 PPO(표준 온폴리시 정책 경사 알고리즘, [[02-foundations/rl-basics|7. RL 기초 §4]]), 그리고 난이도에 따라 로봇을 승급·강등시키는 게임식 지형 커리큘럼.
공개된 `legged_gym` / `rsl_rl` 코드가 2022~2026년의 폭발을 평범한 연구실에서 경제적으로 가능하게
만든 것이다. 과학적 주장은 좁고, 인과적 영향력은 막대하다. 그 둘을 분리해 두는 것이 정확히 이
위키가 존재하는 이유의 교정이다.

**Miki 2022에서 흥미로운 것은 등반이 아니라 기제다.** 어텐션 기반 순환 **믿음 상태(belief state)**
인코더가 고유수용감각과 외수용 높이 지도를 융합하고, 지도를 얼마나 믿을지에 대한 **적응적 게이팅
계수**를 학습한다 — 그래서 지도가 거짓말할 때(눈, 키 큰 풀, 물, 반사면) 제어기가 고유수용감각
로코모션으로 우아하게 후퇴하며, 언제 믿기를 멈출지에 대한 손으로 만든 규칙이 없다.

> [!warning] 피해야 할 과잉 인용 셋
> - **알프스 등반은 플래너 시간에 대한 단일 계측 경로**이지 사람 등산객에 대한 벤치마크 비교가
>   아니다. 2.2 km, 고도 120 m, 하이킹 플래너의 76분 추정치에 대해 78분(정상까지는 표지판 35분에 대해 31분).
> - **"몇 분 만에 걷기"는 GPU 하나에서의 벽시계 시간이다.** 선행 연구보다 시뮬레이션 경험을 훨씬
>   *더 많이* 소모하며, 실기계 학습 시간도 아니다.
> - **휴머노이드 거친 지형 논문은 프리프린트다.** Radosavovic 등의 심사 통과 *Science Robotics*
>   휴머노이드 결과는 **눈먼 평지~완만한 굴곡의 실외 보행**이고, 버클리 등산로와 샌프란시스코
>   언덕이 나오는 거친 지형 후속은 arXiv 프리프린트인데 출판된 것처럼 자주 인용된다.

### 4. 파쿠르의 대조, 그리고 그것이 가르치는 것

몇 달 간격의 두 논문, 반대되는 아키텍처, 반대되는 하드웨어, 둘 다 파쿠르라 불린다.

| | **ANYmal parkour** (Science Robotics 2024) | **Extreme Parkour** (ICRA 2024) |
|---|---|---|
| 아키텍처 | 계층적: 별도 RL 스킬 + 스킬을 고르는 내비게이션 정책 | 단일 모놀리식 네트워크, 깊이에서 행동으로 |
| 인식 | 가려지고 잡음 있는 깊이로부터 명시적 장애물 재구성 | 전방 깊이 카메라 하나, 종단간 |
| 하드웨어 | ANYmal, 약 50 kg 연구용 4족 | 저가 로봇, 부정확한 액추에이터 |
| 눈에 띄는 기제 | 상위 정책이 각 스킬의 **능력 범위**를 안다 | 학습된 내부 yaw 보상이 정책 스스로 **조준하게** 한다, 별도 계획기 없이 |

둘 다 손으로 만들거나 손으로 고른 장애물 코스 너머로 일반화됨을 보이지 못했다. 함께 읽을 가치가
있는 이유는 분야가 같은 시점에 조합과 모놀리식 사이에서 진짜로 미결정 상태임을 보여 주기
때문이고, 또 **ANYmal parkour가 로코모션이 내비게이션으로 건너가는 지점**이기 때문이다: 어떤
지형이 어떤 스킬을 허용하는지 추론하는 상위 정책은 스킬-어포던스 인지 계획이고, 그것이 이
페이지와 [[04-robotics/semantic-language-navigation|19번]] 사이의 실제 인터페이스다.

### 5. 2025~26년에 간 곳

무게 중심이 "X 위를 걸을 수 있는가"에서 **일반가·교차 embodiment 정책**과 지형 표현 학습으로
옮겨 갔다.

- **어텐션 기반 지도 인코딩**(Science Robotics, 2025)은 고유수용감각을 조건으로 하는 지형 지도
  인코더를 **RL 제어기 안에서 종단간으로** 학습해, 미래 발디딤을 위해 디딜 수 있는 영역에
  주의를 두는 법을 배운다 — 그리고 **12자유도 ANYmal-D와 23자유도 휴머노이드 둘 다**에서 실증하는
  것이 눈에 띄는 부분이다.
- **Parkour in the wild**(IJRR, 2026)는 지형별 전문가들을 DAgger로 하나의 일반가 깊이 입력 정책에
  증류한 뒤, 실제 3D 스캔을 포함해 확장된 지형에서 RL 파인튜닝한다 — ANYmal parkour의 스킬 계층을
  단일 확장 가능 정책으로 무너뜨린다.
- **이산 지형에서의 고속 제어**(Science Robotics, 2025)는 **계획기 + 학습기 하이브리드**다:
  휴리스틱·신경망 필터링을 곁들인 표본 기반 발디딤 최적화 + RL 추종기. 4 m/s의 디딤돌, 1.3 m 간극
  점프. 정밀 지형에서는 진자가 부분적으로 하이브리드 쪽으로 되돌아가고 있다는 증거로 인용할 만하다.
- **LocoFormer**(CoRL 2025, 최우수 논문 최종 후보)가 로코모션 파운데이션 모델에 가장 가깝다:
  정밀한 기구학 없이 처음 보는 레그드 *그리고 바퀴* 로봇을 위한 단일 정책. 절차적으로 생성된
  형태들에서 학습하며, 실제 새로움은 **에피소드 경계를 가로지르도록** 늘린 컨텍스트 창이다 —
  창발적인 에피소드 간 적응이 나와서, 앞선 에피소드의 넘어짐으로부터 배운다.

로코모션 파운데이션 모델에 합의는 없고, Miki-2022나 Rudin-2021 급의 2026년 결과도 없다. 그렇게
말하는 편이 프리프린트 하나를 지명하는 것보다 쓸모 있다.

### 6. 도구, 논문의 연대를 정하기 때문에

- **Isaac Gym Preview는 공식 지원 종료다** — NVIDIA 자신의 페이지가 더 이상 지원되지 않는 레거시
  소프트웨어라 부르고, `IsaacGymEnvs`·`OmniIsaacGymEnvs` 저장소는 읽기 전용으로 보관(GitHub이 보관 날짜를 공개하지 않으므로 월을 인용하지 마라)
  처리되었다. 2026년 논문이 "Isaac Gym을 썼다"고 하면 죽은 프리뷰 릴리스 위에 있는 것이다.
- **Isaac Lab**이 후속이고, 2026년 8월 기준 안정 라인은 2.3.x, 3.0은 베타다.
- **MuJoCo Playground / MJX**가 신뢰할 만한 벤더 중립 대안이며 MJX가 학계 기본값이 된 이유다.
- **Newton** — Disney Research·Google DeepMind·NVIDIA 공동 개발, 2025년 9월 리눅스 재단에 기여 —
  이 둘 아래의 공유 물리 층이 되어 가고 있고 MuJoCo Warp를 백엔드로 통합한다. Isaac/MuJoCo 분열이
  솔버 층에서 수렴 중이다.

전체 그림과 라이선스 함정은
[[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]]을 보라.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] Q의 도립진자와 보행 차트를 그리고, capture point가 괄호 안에 있음을 표시한다.
- [ ] 기준 trot에서 Q의 두 속도 한계 중 어느 쪽이 걸리는지, P2를 실으면 나머지 하나가 어떻게 되는지 말한다.
- [ ] 교사-학생 그림을 그리고 무엇이 특권적인지 댄다.
- [ ] Hwangbo 2019가 실제로 무엇을 실증했는지 말한다.
- [ ] "몇 분 만에 걷기"가 왜 샘플 효율 주장이 아닌지 설명한다.
- [ ] Miki의 게이팅 기제와 그것이 무엇을 막는지 서술한다.
- [ ] 두 파쿠르 아키텍처를 대고, 둘 다 보이지 못한 것을 말한다.

> [!tip] 더 깊이 · Going deeper
> 이 페이지의 두 절반은 서로 다른 곳으로 간다. §1.5의 고전 어휘 — 지지 다각형, ZMP, capture point — 는 Tedrake의 무료 [*Underactuated Robotics*](https://underactuated.csail.mit.edu/)가 교과서다. 학습 쪽 계보에는 책이 없고, 대체물은 §2~§3의 네 논문을 출판 순서로 읽는 것이다: sim-to-real 결과의 Hwangbo 외(2019), 특권 교사–학생의 Lee 외(2020), 시험 시점에 특권 입력 없이 적응하는 Kumar 외(2021), 외수용 감각을 더한 Miki 외(2022). 네 개의 시스템이 아니라 하나의 논증이 전개되는 것으로 읽어라.

### 스스로 점검

1. 눈먼 로봇이 어떻게 보지 못하는 진흙에 적응하는가?
2. 2026년 논문이 Isaac Gym에서 학습한 로코모션 결과를 보고한다. 무엇을 짚겠는가?
3. 누군가 Miki 2022를 로봇이 이제 사람 등산객을 능가한다는 근거로 인용한다. 교정하라.
4. LocoFormer의 늘린 컨텍스트 창이 실제로 무엇을 사는가?
5. 프로젝트가 매니퓰레이터를 싣고 거친 지반을 가는 레그드 플랫폼을 필요로 한다. 이 페이지에서
   가장 가까운 선례는 무엇이고, 그것이 주지 않는 것은?

> [!tip]- 정답 · Answers
> 1. 학생이, 마찰계수와 지형 프로파일을 *볼 수 있었던* 교사로부터 증류되었고, 그 양들을 짧은 고유수용감각 이력 — 지난 몇 분의 일 초 동안 몸이 실제로 어떻게 움직였는가 — 에서 추론하는 법을 배웠기 때문이다. 진흙을 미리 예상할 수는 없지만 발이 한 번 들어가고 나면 최근 운동 이력이 무엇이 달라졌는지에 대해 정보를 담고, 정책은 정확히 그 추론으로 학습되었다. 눈이 멀었다는 것이 먼저 접촉해야 하는 이유이고, 증류가 접촉만으로 충분한 이유다.
> 2. Isaac Gym Preview가 지원 종료라는 점 — NVIDIA 자신의 페이지가 레거시이며 지원되지 않는다고 하고, 관련 환경 저장소들은 읽기 전용으로 보관되었다. 결과를 무효화하지는 않지만 작업의 연대를 정하고 재현을 어렵게 만들며, 지금 시작하는 프로젝트는 Isaac Lab이나 MuJoCo MJX에 있어야 한다.
> 3. 비교 대상은 **단일 계측 알프스 경로** — 2.2 km, 고도 120 m — 를 그 경로의 **하이킹 플래너 76분 추정치**에 대해 78분에 완주한 것이다(정상까지는 표지판 35분에 대해 31분). 사람 등산객에 대한 벤치마크가 아니라 발표된 시간에 대한 한 경로이고, 로봇이 전체적으로는 조금 더 느렸다. 결과는 진심으로 인상적이고, 그것이 뒷받침하는 주장은 통상 귀속되는 것보다 좁다.
> 4. 에피소드 *안*이 아니라 에피소드를 *가로지르는* 적응. 컨텍스트 창이 에피소드 경계를 넘으면 정책이 앞선 시도에서 일어난 일 — 넘어짐을 포함해 — 을 조건으로 삼을 수 있어, 가중치 갱신 없이 한 배치 안에서 개선된다. 에피소드 안에서 고유수용감각 이력으로 적응하고 에피소드가 끝나면 초기화되는 RMA식 잠재 추정과는 다른 기제다.
> 5. **ANYmal parkour.** 상위 정책이 어떤 지형이 무엇을 허용하는지 추론하는 유일한 결과이고, 그것이 모바일 매니퓰레이터가 작업 공간에 도달하는 데 필요한 것이기 때문이다. 그것이 주지 않는 것은 매니퓰레이터 자체다: 팔도, 페이로드도, 팔을 실었을 때 동역학이 어떻게 달라지는지에 대한 설명도 없는, 정돈된 코스 위의 장애물 사이 내비게이션 결과다. 팔을 더할 때의 오차 예산 귀결은 [[04-robotics/navigation-mobile-manipulation|16. §4]]에 있다.

**Worked: 과제가 묻는 세 가지 읽기.** "몇 분 만에 걷는다"는 교사–학생의 벽시계 시간이다. 교사는 마찰을 보고 있었고, 분 단위 시간은 표본 효율이 아니다. Hwangbo 2019가 옮긴 것은 민첩한 사족 보행 기술이지 "sim-to-real이 풀렸다"가 아니다. 잔해 위 매니퓰레이터에 가장 가까운 선례는 ANYmal 파쿠르인데, 거기에는 아직 팔도 없고 적재물도 없다.

### 과제 · Problem set

Tier B. **Q**, 이 페이지, 그리고 [[02-foundations/lab-plants|0.6]]의 **P2**를 쓴다. 시뮬레이터는
없다. 다리 달린 몸의 오일러 루프는 이 페이지에 없고, 필요하지도 않다.

**바꿀 손잡이.** Q가 $z=0.24$ m로 몸을 낮추고 **crawl**로 걷는다. 주기는 그대로 $T=0.40$ s,
$\beta=0.75$, 네 발의 위상은 LF, RH, RF, LH 순으로 4분의 1 주기씩 어긋난다. 명령 속도는
$\dot x=0.6$ m/s. 다리 길이, 고관절 거리, 질량, $\mu$는 그대로다.

1. **그려라.** 맨 위의 그림 두 칸을 낮춘 crawl에 대해 모두 그린다. 위: $z=0.24$ m의 도립진자,
   $0.6$ m/s에서의 capture point, 그리고 새 높이에 대한 괄호 — $\xi$가 그 안인지, 얼마나 여유가
   있는지 표시한다. 아래: 보행 차트 네 줄, 줄마다 $0.30$ s의 디딤이 주기를 돌며 들어간다. 칠한
   뒤 차트 아래에 매 순간 발이 몇 개 땅에 있는지 적고, 지지 다각형이 어떤 모양인지 말한다.
2. **유도하라.** (a) 낮춘 자세의 $\omega_0$와 $1/\omega_0$. (b) 발의 여유 $R$과 무게중심 앞
   가장 먼 디딤점. (c) crawl의 스트로크 한계 $2R/\beta T$와 균형 한계 $\omega_0(d+R)$. 어느 쪽이
   먼저 걸리고 차이는 얼마인가. (d) 유도 §7처럼 P2를 어깨에 얹고 $z'$, $\Delta x$, 균형 한계를
   다시 구한 뒤, (c)의 여유가 살아남는지 말한다.
3. **해석하라.** 낮춘 자세는 두 가지를 한꺼번에 바꾼다. 진자를 빠르게 하고 스트로크를 늘린다.
   각각이 왜 그런지 식에서 말하고, 두 식 어디에도 나오지 않는 대가가 무엇인지 대라. 그다음 독해
   질문: §2~§3의 학습 결과들 중 이 맞거래를 *알려 주지 않아도* 찾아냈을 것은 어느 것이고,
   도립진자가 정책이 주지 않는 무엇을 주는가?
4. **읽어라.** §2~§6만 써서 세 가지 주장을 다룬다. (a) 어떤 논문이 "몇 분 만에 걷기를 학습한다"고
   한다. 교사–학생 도식에서 특권인 것과, 벽시계 분이 샘플 효율 주장이 아닌 이유는? (b) Hwangbo
   2019가 "sim-to-real은 풀렸다"로 인용된다. 실제로 보인 것과, 허가하지 않는 이전은? (c) 사족이
   잔해 위로 매니퓰레이터를 실어 나르길 원한다. 이 페이지에서 가장 가까운 선례와, 그것이 여전히
   주지 않는 둘은?

> [!note]- 그리는 법 · How to draw it
> - 위 칸: 수평선으로 그은 지면, 서 있는 높이 $z$의 무게중심 점, 거기서 디딤발 $p$까지 내린 질량 없는 곧은 다리, 그리고 무게중심의 수평 속도 화살표 $\dot x$.
> - 지면 위의 세 점: 발 $p$, 무게중심의 수직 투영 $x$, 그리고 $x$보다 $\dot x/\omega_0$만큼 앞의 capture point $\xi$.
> - $x$의 뒤 $d+R$부터 앞 $d+R$까지 지면에 친 괄호와 *reach*라는 이름. 발을 놓을 수 있는 구간이다(계산 예제: $z = 0.30$ m에서 앞뒤로 $0.46$ m).
> - 위 칸의 물음은 전부 $\xi$가 그 괄호 안에 들어오는가이므로, $\xi$를 표시하고 여유를 적는다.
> - 아래 칸: 발마다 한 줄씩 쌓은 수평 네 줄 LF, RF, LH, RH와 한 주기 $T = 0.40$ s의 시간 축.
> - 그 발이 디딤인 구간을 칠하고, 디딤이 주기 끝을 넘으면 $0$으로 돌아와 이어 칠한다(계산 예제의 trot: LF와 RH가 $0$부터 $0.20$ s까지, RF와 LH가 $0.20$부터 $0.40$ s까지).
> - 칠해진 집합이 바뀌는 순간을 모두 표시한다. 그 순간이 지지 다각형의 모양이 바뀌는 때이고, 이 차트를 표로 읽은 것이 [[04-robotics/convex-mpc-legged|8. Convex MPC]]가 건네받는 접촉 스케줄이다.

> [!tip]- 정답 · Solutions
> 1. 위: $\xi$는 무게중심 앞 $0.094$ m이고 괄호는 이제 $0.541$ m까지 가므로, 약 $0.45$ m 여유를 두고 안쪽이다. 아래: $\beta=0.75$에 4분의 1 주기 위상이면 매 순간 정확히 $4\beta=3$개의 발이 땅에 있으므로, 지지 다각형은 $0.10$ s마다 꼭짓점 하나를 바꾸는 삼각형이고 결코 선분으로 무너지지 않는다 — 강의의 trot 차트와 정반대다.
> 2. (a) $\omega_0=\sqrt{9.81/0.24}=6.39\,\mathrm{rad/s}$, $1/\omega_0=0.156\,\mathrm{s}$. (b) $R=\sqrt{0.34^2-0.24^2}=\sqrt{0.058}=0.241\,\mathrm{m}$, 가장 먼 디딤점 $0.30+0.241=0.541\,\mathrm{m}$. (c) 스트로크 $2(0.241)/0.30=1.61\,\mathrm{m/s}$, 균형 $6.39\times0.541=3.46\,\mathrm{m/s}$. 스트로크가 걸리고 그 차이는 선 자세보다 오히려 크다 — 다만 낮춘 crawl($1.61$ m/s)이 선 자세의 trot($1.60$ m/s)과 같아졌다는 점을 보라. 높은 듀티 팩터가 물린 값을 낮춘 자세가 그대로 되사 왔다. (d) $z'=(12(0.24)+1(0.24)+1(1.24))/14=4.36/14=0.311\,\mathrm{m}$, $\Delta x=0.143\,\mathrm{m}$ 그대로, $\omega_0'=5.61\,\mathrm{rad/s}$, 균형 $=5.61\times(0.541-0.143)=2.23\,\mathrm{m/s}$. 여유는 살아남는다: 스트로크 $1.61$에 대해 $2.23$. 선 자세에서는 같은 팔이 여유를 완전히 지웠으니, 팔을 싣는 문제의 해법이 낮춘 자세다.
> 3. $z$가 작아지면 $\omega_0=\sqrt{g/z}$가 커져 진자가 더 빨리 발산하고 제어기의 시간이 줄어든다 — (a)에 숨은 대가이고, 낮춘 자세가 공짜가 아닌 이유다. $R=\sqrt{\ell^2-z^2}$는 $z$가 작아지면 커지는데, 길이가 정해진 다리가 더는 쓰지 않는 수직 몫으로 수평 이동을 사기 때문이다. 두 식 어디에도 없는 것은 관절 토크다. 낮춘 자세를 유지하려면 디딤 내내 무릎이 중력을 버텨야 하는데 도립진자에는 토크 항이 아예 없다. 독해 질문은 — 전부다. 전진 속도 보상에 토크 벌점을 더하면 누구도 $\sqrt{\ell^2-z^2}$를 적지 않고도 정확히 이 맞거래가 선택된다는 뜻에서 그렇고, 그것이 §2가 말하는, 신경망이 스스로 찾은 극한주기다. 도립진자가 정책 대신 주는 것은 *이유*다. 아무것도 만들기 전에 확인할 수 있는 닫힌 형태의 한계 두 개, 그리고 보고된 최고 속도가 둘 중 어느 것에 부딪혔던 것인지 말할 수 있는 수단.
> 4. (a) 교사는 마찰과 지형을 보고, 학생은 고유수용(과 카메라)을 본다. 분은 병렬 시뮬레이터 벽시계이지 기술당 환경 스텝이 아니다 — Rudin의 주장은 처리량이지 샘플 효율이 아니다. (b) 강체 시뮬에서 시스템 식별과 도메인 랜덤화로 사족의 민첩 기술이 이전된 것. 접촉이 많은 조작도, 다른 로봇도, "풀렸다"도 아니다. (c) ANYmal parkour(상위 수준의 affordance). 팔도, 페이로드 동역학도 아니다. 매니퓰레이터를 더하는 것은 로코모션 논문이 다루지 않는 오차 예산 문제([[04-robotics/navigation-mobile-manipulation|16. §4]])이고, 유도 §7이 그 값을 두 숫자로 준다: capture point가 $0.175\to0.195$ m로 멀어지고 괄호가 $0.143$ m를 잃는다.

### 출처

- J. Hwangbo, J. Lee, A. Dosovitskiy, et al., "Learning agile and dynamic motor skills for legged robots," *Science Robotics*, vol. 4, no. 26, eaau5872, 2019 ([arXiv:1901.08652](https://arxiv.org/abs/1901.08652)).
- J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, M. Hutter, "Learning Quadrupedal Locomotion over Challenging Terrain," *Science Robotics*, vol. 5, no. 47, eabc5986, 2020 ([arXiv:2010.11251](https://arxiv.org/abs/2010.11251)) — privileged teacher-student.
- N. Rudin, D. Hoeller, P. Reist, M. Hutter, "Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning," CoRL 2021 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — `legged_gym` / `rsl_rl`.
- A. Kumar, Z. Fu, D. Pathak, J. Malik, "RMA: Rapid Motor Adaptation for Legged Robots," RSS 2021, DOI 10.15607/RSS.2021.XVII.011 ([arXiv:2107.04034](https://arxiv.org/abs/2107.04034)).
- T. Miki, J. Lee, J. Hwangbo, et al., "Learning robust perceptive locomotion for quadrupedal robots in the wild," *Science Robotics*, vol. 7, no. 62, eabk2822, 2022 ([arXiv:2201.08117](https://arxiv.org/abs/2201.08117)).
- D. Hoeller, N. Rudin, D. Sako, M. Hutter, "ANYmal parkour: Learning agile navigation for quadrupedal robots," *Science Robotics*, vol. 9, no. 88, eadi7566, 2024 ([arXiv:2306.14874](https://arxiv.org/abs/2306.14874)).
- X. Cheng, K. Shi, A. Agarwal, D. Pathak, "Extreme Parkour with Legged Robots," ICRA 2024, pp. 11443–11450 ([arXiv:2309.14341](https://arxiv.org/abs/2309.14341)); Z. Zhuang et al., "Robot Parkour Learning," CoRL 2023 oral ([arXiv:2309.05665](https://arxiv.org/abs/2309.05665)).
- I. Radosavovic, T. Xiao, B. Zhang, et al., "Real-world humanoid locomotion with reinforcement learning," *Science Robotics*, vol. 9, no. 89, eadi9579, 2024 ([arXiv:2303.03381](https://arxiv.org/abs/2303.03381)). 거친 지형 후속 [arXiv:2410.03654](https://arxiv.org/abs/2410.03654)는 **프리프린트**다.
- 2025~26: He, Zhang, Jenelten, et al., "Attention-based map encoding for learning generalized legged locomotion," *Science Robotics*, vol. 10, no. 105, eadv3604, 2025 ([arXiv:2506.09588](https://arxiv.org/abs/2506.09588)); Rudin, He, Aurand, Hutter, "Parkour in the wild," *IJRR*, 2026, DOI 10.1177/02783649261455067 ([arXiv:2505.11164](https://arxiv.org/abs/2505.11164)); Kim, Oh, Park, et al., "High-speed control and navigation for quadrupedal robots on complex and discrete terrain," *Science Robotics*, vol. 10, no. 102, eads6192, 2025 ([arXiv:2506.02835](https://arxiv.org/abs/2506.02835)); Liu, Pathak, Agarwal, "LocoFormer," CoRL 2025 ([arXiv:2509.23745](https://arxiv.org/abs/2509.23745)).

**이 위키 안에서**

- **논문 노트** — [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]] · [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등 2022]] · [[01-canonical-papers/notes/9-navigation/rma|RMA]] · [[01-canonical-papers/notes/9-navigation/anymal-parkour|ANYmal Parkour]]
- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]] — 이 로봇들이 보내지는 곳
- [[04-robotics/convex-mpc-legged|레그드 로봇의 Convex MPC]] — 같은 문제의 모델 기반 쪽
- [[05-construction-robotics/sim-to-real|필드 로봇 Sim-to-Real]] — 여러 전략 중 하나로서의 교사-학생
- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — §6의 도구 현황
