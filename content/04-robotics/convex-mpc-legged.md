---
title: "8. Convex MPC (Legged Robots)"
tags: [robotics, control, resource]
study-depth: Literacy
wiki-support: Working
depth-goal: "Read the MPC formulation and recognize its assumptions and role in a complete robot system."
mastery-when: "Raise to Working or Mastery when legged control or MPC design is used directly."
---

**Key references** — Di Carlo et al., *Dynamic Locomotion in the MIT Cheetah 3 Through Convex Model-Predictive Control*, IROS 2018 · [IEEE](https://ieeexplore.ieee.org/document/8594448) · Kim et al., *Highly Dynamic Quadruped Locomotion via Whole-Body Impulse Control and MPC* (open access) · [arXiv](https://arxiv.org/abs/1909.06586) · [PDF](https://arxiv.org/pdf/1909.06586)

## English

*Last of group D and its worked application. Stands on [[04-robotics/mpc|7. MPC]], [[04-robotics/contact-force-tactile|9. Contact]] and the [[04-robotics/modern-robotics/index|MR chapters]].
The cleanest case study of the skill the optimization page teaches: choose the approximation that makes the problem convex.*

> [!info] Depth target · 깊이 목표
> Understand why the problem is convexified and what the simplification costs. This is a representative-application read, not a controller-design guide.
> 왜 문제를 볼록화했고 그 단순화의 대가가 무엇인지 이해하는 것이 목표다. 대표 응용 읽기이지 제어기 설계 가이드가 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/mpc|7. MPC]] (the formulation being applied) · [[02-foundations/optimization|4. Optimization §5]] (QP) · [[04-robotics/contact-force-tactile|9. Contact §2]] (the friction cone that becomes the constraint set) · [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8]] (what the single-rigid-body approximation throws away) · [[02-foundations/se3-geometry|8. 3D Geometry §2]] (roll, pitch, yaw)
> [[04-robotics/mpc|7. MPC]] (적용되는 정식화) · [[02-foundations/optimization|4. 최적화 §5]] (QP) · [[04-robotics/contact-force-tactile|9. 접촉 §2]] (제약 집합이 되는 마찰 원뿔) · [[04-robotics/modern-robotics/ch08-dynamics|MR 8장]] (단일 강체 근사가 버리는 것) · [[02-foundations/se3-geometry|8. 3D 기하 §2]] (롤·피치·요)

### Running object · 이 페이지의 장치

The body is **Q**, the frozen quadruped of [[04-robotics/legged-locomotion|18. Legged Locomotion]]:
$m=12$ kg, CoM $0.30$ m up, feet at $(\pm0.30,\pm0.15)$ m, $\mu=0.6$, a trot of period
$T=0.40$ s at duty factor $\beta=0.50$, and a per-foot ceiling $f_{z,\max}=200$ N. Four numbers
the QP needs that the locomotion page has no use for:

| Symbol | Value | Meaning |
|---|---:|---|
| $I_B$ | $\mathrm{diag}(0.104,\,0.374,\,0.450)\,\mathrm{kg\,m^2}$ | body inertia, a uniform $0.60\times0.30\times0.12$ m box of $12$ kg |
| $\Delta t$ | $0.06\,\mathrm{s}$ | one step of the MPC horizon |
| $N$ | $2$ | horizon length, so $0.12$ s of prediction |
| $q,\ r$ | $q=1\,\mathrm{m^{-2}}$, $r=\lambda\,q\,\alpha^2$ | tracking and force weights, with $\lambda$ the dimensionless knob, $\lambda=1$ nominal |

The case worked below starts from $z_0=0.27$ m and $\dot z_0=0$: Q has sagged $3$ cm below its
commanded height $z^{\mathrm{ref}}=0.30$ m and must be pushed back up.

A $0.12$ s horizon is shorter than the trot's $0.20$ s stance, so the **contact schedule is
constant across it** — the same two diagonal feet are down at every step of the horizon, nothing
lifts off mid-plan, and no swing equality switches on or off. That is what makes the QP below small
enough to finish on paper, and it is also a real property of the controller: Di Carlo et al. re-solve
tens of times a second precisely so that each solve sees a short, nearly static schedule.

### Homework diagram · 과제가 그릴 그림

One figure in three parts; the problem set asks for the same one.

**Left — the horizon timeline.** A time axis with ticks at $0$, $\Delta t$, $2\Delta t$. Mark the
measured state $x_0$ at the first tick, the two decisions $u_0$ and $u_1$ as arrows leaving the
first two ticks, and the two predicted states $x_1$, $x_2$ at the ticks they land on. Draw the
reference height $z^{\mathrm{ref}}$ as a dashed horizontal line across all three and shade the gap
$e_k=z_k-z^{\mathrm{ref}}$ that the cost is squaring. Circle $u_0$: it is the only decision that is
ever applied.

**Middle — the schedule.** Under the same axis, redraw the trot gait chart from
[[04-robotics/legged-locomotion|18. Legged Locomotion]] and shade the $0.12$ s the horizon covers.
The point of the drawing is that the shaded window sits inside one stance phase.

**Right — the constraint block.** Draw the decision vector as a grid, $4$ feet $\times\ 3$ force
components $\times\ 2$ steps $=24$ cells. Cross out the $12$ cells belonging to the two swing feet:
those are the equalities $f_i=0$. On one surviving stance foot, draw the four pyramid faces
$\pm f_x\le\mu f_z$, $\pm f_y\le\mu f_z$ as four lines and the unilateral bound $f_z\ge0$ as a
fifth. Count what is left. That count is the QP.

**What it is**: the paper that made real-time MPC standard on legged robots. The trick is a
*deliberate simplification*, made in five modelling moves:

1. **Single rigid body**: approximate the robot as one rigid body (ignore leg dynamics). That is reasonable when the legs are light compared with the body, but it is a real omission: the momentum of a fast leg swing is simply not in the model.
2. **Small roll and pitch**: linearize the rotation dynamics under a small roll-and-pitch
   assumption (roll, pitch and yaw are the body's rotations about its forward, sideways and
   vertical axes). The single state matrix uses the *average* reference yaw over the horizon, while
   each step's input matrix uses that step's reference yaw and footholds.
   The one exception is the first step, which uses the current robot state instead.
3. **Forces as decisions**: treat ground reaction forces as the decision variables.
4. **Friction pyramid**: approximate each circular friction cone by linear facets.
5. **Condensed QP, solved fast**: those linear inequalities keep the problem a **convex QP**,
   solved in the condensed form of [[04-robotics/mpc|7. MPC §2]], that solved in under a
   millisecond in the reported implementation and was re-run at tens of Hz (Di Carlo et al.'s
   abstract says 20–30 Hz while their experiments ran at 25 to 50 Hz depending on gait, so the
   50 Hz [[04-robotics/mpc|7. MPC §2]] sizes is the top of the paper's own range, not a
   disagreement) — exactly the machinery of [[02-foundations/optimization|4. Optimization §5]].

**The model behind the five moves, written out.**

- **Single rigid body dynamics** (move 1). With the legs treated as massless, the only forces on the body are gravity and the four ground reaction forces, so Newton's and Euler's equations give
$$m\,\ddot p=\sum_{i=1}^{4}f_i-m\,g,\qquad \frac{d}{dt}\big(I\,\omega\big)=\sum_{i=1}^{4}r_i\times f_i$$
  where $m$ is the total mass, $p$ the centre-of-mass position, $g=(0,0,9.81)$ m/s², $f_i\in\mathbb{R}^3$ the ground reaction force at foot $i$, $r_i$ the foot position relative to the centre of mass, $I$ the body inertia in world axes and $\omega$ the angular velocity. Example: a 12 kg robot standing still on four feet with equal load needs $f_{i,z}=12\times9.81/4=29.43$ N per foot. Non-example: a 2 kg leg swung fast carries momentum these equations have no term for.
- **Small roll and pitch** (move 2). Write $\Theta=(\phi,\theta,\psi)$ for roll, pitch and yaw. The exact map from $\omega$ to $\dot\Theta$ contains factors $\tan\theta$ and $1/\cos\theta$; with $\phi\approx\theta\approx0$ it keeps only yaw, and the world-frame inertia keeps only the yaw rotation of the body-frame inertia $I_B$:
$$\dot\Theta\approx R_z(\psi)^\top\omega,\qquad I\approx R_z(\psi)\,I_B\,R_z(\psi)^\top$$
  and the gyroscopic term $\omega\times I\omega$ is dropped as small. At $5°$ pitch the neglected factors are $\tan5°=0.087$ and $1/\cos5°=1.004$; at $30°$ they are $0.577$ and $1.155$, which is where the approximation stops being small. With the 13-dimensional state $x=(\Theta,p,\omega,\dot p,g)$ (gravity appended as a constant state so the model has no offset term), discretizing gives $x_{k+1}=A\,x_k+B_k\,u_k$, with one $A$ from the average yaw and a $B_k$ per step.
- **Forces as decisions** (move 3). The input at step $k$ is $u_k=(f_1,\dots,f_4)\in\mathbb{R}^{12}$. A gait's **contact schedule** ([[04-robotics/legged-locomotion|18. Legged Locomotion §2]]) says which feet are down at each step, and a foot in swing gets the equality constraint $f_i=0$, since it cannot push on the ground.
- **Friction pyramid** (move 4). The circular cone $\sqrt{f_x^2+f_y^2}\le\mu f_z$ of [[04-robotics/contact-force-tactile|Contact, Force & Tactile §2]] is not linear. Bounding each tangential axis separately is, and each absolute value is two linear inequalities, which gives the four faces counted below:
$$|f_x|\le\mu f_z,\qquad |f_y|\le\mu f_z$$
  Example: $\mu=0.6$, $f_z=100$ N. The cone allows tangential force up to $60$ N, but the pyramid's corner $(60,60)$ N has magnitude $84.9$ N, so this pyramid admits forces that would slip. Shrinking the coefficient to $\mu/\sqrt2=0.424$ puts the corner at exactly $60$ N, which is safe but rejects $(60,0)$, a force the real cone allows.
- **The QP** (move 5). With reference states $x^{\text{ref}}_k$ from the commanded body motion, weights $Q\succeq0$ on tracking error and $R\succ0$ on force magnitude, and $\lVert v\rVert_Q^2=v^\top Qv$, the controller solves
$$\min_{u_0,\dots,u_{N-1}}\ \sum_{k=0}^{N-1}\lVert x_{k+1}-x_{k+1}^{\text{ref}}\rVert_Q^2+\lVert u_k\rVert_R^2$$
  subject to the dynamics, the pyramid inequalities and the swing equalities. The cost is quadratic and every constraint is linear, so it is a convex QP; substituting the dynamics out leaves the condensed form.

Cheetah 3 galloped on this; the follow-up (Kim et al., open access) pairs the MPC with
whole-body impulse control (built from the null-space task priority and whole-body QP of [[04-robotics/force-compliance-control|13. Force & Compliance Control §4]]) — the standard two-level stack (slow MPC plans forces, fast WBC
tracks them) that echoes [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]'s System 2/System 1 split.

> [!example] Worked example · 계산 예제
> How big is the QP? Take a 13-dimensional state, 4 feet × 3 force components = 12 inputs per step, and horizon $N = 10$.
> - Condensed form eliminates the states, so the decision variables are the forces only: $N \cdot 12 = 120$.
> - (Keeping states as variables too would give $10\cdot 13 + 10\cdot 12 = 250$ — condensing trades these for a denser matrix.)
> - Friction pyramid: 4 faces per foot, per step: $4 \cdot 4 \cdot 10 = 160$ linear inequalities.
> - This counts only the pyramid faces; any force bounds or swing-foot constraints the implementation adds come on top and are not counted here.
> - A 120-variable, 160-inequality QP is tiny, which is why a sub-millisecond solve is plausible.

### Worked on Q · 장치로 한 번 끝까지

The box above sizes the paper's own $N=10$ QP. This section solves the $N=2$ one on Q, by hand,
and then lets a loop vary the two things you would actually tune.

**1. The slice, and why it is honest.** Command Q to hold height with no horizontal motion. Then
$f_x=f_y=0$ at every foot, the roll-and-pitch channels are at their references, and the twelve-input
problem collapses to one decision per step: the *total* vertical force $f_z^{\mathrm{tot}}$ shared by
the two stance feet. Writing $u=f_z^{\mathrm{tot}}-mg$ for the deviation from the force that merely
holds Q up, Newton's equation from move 1 becomes $m\ddot z=u$, so exact integration over a constant
$u$ gives the discrete model

$$z_{k+1}=z_k+\Delta t\,\dot z_k+\frac{\Delta t^2}{2m}u_k,\qquad \dot z_{k+1}=\dot z_k+\frac{\Delta t}{m}u_k$$

This is the same $x_{k+1}=Ax_k+B_ku_k$ as move 2, restricted to the two rows that move under a purely
vertical command. It is a slice, not a different model, and step 10 below says exactly what the
slice hides.

**2. Condensing.** Write $e_k=z_k-z^{\mathrm{ref}}$ and $\alpha=\Delta t^2/(2m)=0.06^2/24=1.5\times10^{-4}$
m/N. Substituting the dynamics forward from $\dot z_0=0$ eliminates the states, which is what
[[04-robotics/mpc|7. MPC §2]] calls the condensed form:

$$e_1=e_0+\alpha u_0,\qquad e_2=e_0+3\alpha u_0+\alpha u_1$$

The $3\alpha$ appears because $u_0$ acts on $e_2$ twice: once through the position it moved in the
first interval and once through the velocity it left behind, $\alpha+2\alpha=3\alpha$.

**3. The cost, and the normal equations.** With $q$ on tracking error, $r=\lambda q\alpha^2$ on force
and $J=q(e_1^2+e_2^2)+r(u_0^2+u_1^2)$, setting both partial derivatives to zero and dividing through
by $2q\alpha^2$ gives a $2\times2$ system whose matrix entries are pure numbers and whose
right-hand side is a force:

$$\begin{pmatrix}10+\lambda&3\\3&1+\lambda\end{pmatrix}\begin{pmatrix}u_0\\u_1\end{pmatrix}=-\frac{e_0}{\alpha}\begin{pmatrix}4\\1\end{pmatrix}$$

The $\lambda$ sits on the diagonal because the force penalty is the only term that touches $u_k$ alone,
so raising it makes the matrix more diagonally dominant and shrinks the solution — which is the whole
mechanism by which "weight the forces more" means "push less hard".

**4. One solved step.** At the nominal $\lambda=1$ with $e_0=-0.03$ m, so $e_0/\alpha=-200$ N:

$$\begin{pmatrix}11&3\\3&2\end{pmatrix}\begin{pmatrix}u_0\\u_1\end{pmatrix}=\begin{pmatrix}800\\200\end{pmatrix}\mathrm{N}\ \Longrightarrow\ u_0=\frac{1600-600}{13}=\frac{1000}{13}=76.92\ \mathrm{N},\quad u_1=\frac{2200-2400}{13}=-15.38\ \mathrm{N}$$

since the determinant is $22-9=13$. In physical units the first command is
$f_z^{\mathrm{tot}}=mg+u_0=117.72+76.92=194.64$ N, which the two stance feet split as $97.32$ N each.
The plan it is part of predicts $e_1=-0.03+1.5\times10^{-4}(76.92)=-0.0185$ m and
$e_2=+0.0023$ m — it deliberately overshoots by $2.3$ mm, because arriving with
$\dot z_1=\Delta t\,u_0/m=0.385$ m/s and then braking is cheaper in this cost than creeping up.

**5. The rows, and which of them bind.** For the full $N=2$ trot QP the count is: $4\times3\times2=24$
decision variables, $2\times3\times2=12$ of them killed by the swing equalities $f_i=0$, leaving $12$
free; $4\times4\times2=32$ friction-pyramid inequalities; $4\times2=8$ unilateral rows $f_{z,i}\ge0$;
and $8$ more if the $200$ N/foot ceiling is imposed. An **active** (binding) constraint is an
inequality row that the optimum satisfies with equality, so that deleting it would move the answer;
a **slack** row is satisfied strictly and could be deleted with no effect at all. At the solution
above, every pyramid row is slack, because the command is vertical and $|f_x|=0\le\mu f_z=0.6\times97.32=58.39$
N with $58.39$ N to spare, and the stance feet's unilateral rows are slack at both steps since
$97.32$ N and $(117.72-15.38)/2=51.17$ N are both positive. Every row is slack, so
the unconstrained stationary point *is* the QP solution — which is the licence for having solved it on
paper. Non-example: a pyramid row is not "inactive because the friction is high"; it is inactive
because this particular command asks for no tangential force, and the first sideways step makes it the
row that decides everything.

**6. When a row does bind.** The system is linear in $e_0$, so start Q $10$ cm *high* instead
($e_0=+0.10$ m, $e_0/\alpha=666.7$ N) and the same matrix returns $u_0=-256.4$ N, i.e.
$f_z^{\mathrm{tot}}=117.72-256.4=-138.7$ N. Feet cannot pull. The unilateral row activates, the QP
clamps to $f_z^{\mathrm{tot}}=0$, and the optimal action is to stop pushing and let gravity do the
work. That discontinuity — a smooth cost, a solution that suddenly stops responding to the weights —
is what the inequality rows are for, and it is invisible in any presentation that only writes the
cost down.

**7. Receding horizon.** Only $u_0$ is applied. **Receding-horizon control** is a feedback policy, not
a trajectory: at each tick it (i) measures the state, (ii) solves a finite-horizon optimal-control
problem starting there, (iii) applies the first input only, and (iv) discards the rest and repeats.
The policy is $u(x)=[\,u_0^\star(x)\,]$ where $u^\star$ is the solve above. Example: Q applies $76.92$
N for one $\Delta t$, re-measures, and solves again from wherever it actually is — so a modelling error
in $\alpha$ is corrected next tick rather than integrated. Non-example: solving once and playing
$u_0,u_1$ out to the end of the horizon is *not* receding-horizon control; it is an open-loop
trajectory, and on a robot whose real $m$ differs by 10% it drifts with nothing to pull it back. This
is why the paper's re-solve rate, not its horizon, is the number that makes the controller work.

**8. The loop, and the two knobs.** Everything above is one tick at one setting. The horizon $N$ and
the weight ratio $\lambda$ are what a practitioner actually chooses, and the trade between them is
what a hand calculation cannot show: it lives in the closed loop, over many ticks, with the unilateral
row switching in and out.

```python
import numpy as np

m, g = 12.0, 9.81             # Q: body mass, gravity
dt = 0.06                     # horizon step
zref = 0.30                   # commanded CoM height
n_st, fz_max = 2, 200.0       # stance feet in a trot, per-foot vertical limit
alpha = dt**2 / (2*m)         # 1.5e-4 m per newton-step
u_lo, u_hi = -m*g, n_st*fz_max - m*g

def condensed(N, e0, zd0, lam):
    """J = sum q e_{k+1}^2 + r u_k^2 as (1/2) u'H u + f'u, with r = lam*q*alpha^2."""
    S = np.zeros((N, N)); d = np.zeros(N)
    for k in range(N):
        d[k] = e0 + (k + 1) * dt * zd0
        for j in range(k + 1):
            S[k, j] = alpha * (2 * (k - j) + 1)
    q = 1.0; r = lam * q * alpha**2
    return 2 * (q * S.T @ S + r * np.eye(N)), 2 * q * S.T @ d

def solve_box(H, f, lo, hi):
    """Box-constrained QP by active set: solve the free block, clamp, repeat."""
    n = len(f); u = np.zeros(n); free = np.ones(n, bool)
    for _ in range(20):
        t = u.copy()
        if free.any():
            t[free] = np.linalg.solve(H[np.ix_(free, free)],
                                      -f[free] - H[np.ix_(free, ~free)] @ u[~free])
        c = np.clip(t, lo, hi); nf = (t == c)
        if np.allclose(c, u) and np.array_equal(nf, free):
            return c
        u, free = c, nf
    return u

def run(N, lam, e0=-0.03, zd0=0.0, ticks=12):
    e, zd, peak, u0, rows, hist = e0, zd0, 0.0, None, set(), []
    for _ in range(ticks):
        H, f = condensed(N, e, zd, lam)
        free = np.linalg.solve(H, -f)          # the unconstrained stationary point
        u = solve_box(H, f, u_lo, u_hi)        # the QP solution
        if free[0] < u_lo: rows.add("fz = 0")
        if free[0] > u_hi: rows.add("200 N/foot")
        if u0 is None: u0 = u[0]
        peak = max(peak, (m * g + u[0]) / n_st)
        e, zd = e + dt * zd + alpha * u[0], zd + dt / m * u[0]
        hist.append(e)
    settle = next(((i + 1) * dt for i in range(len(hist))
                   if all(abs(x) <= 0.005 for x in hist[i:])), None)
    return u0, peak, 1000 * max(0.0, max(hist)), settle, ", ".join(sorted(rows)) or "none"

for N in (1, 2, 4, 8):
    for lam in (0.1, 1.0, 10.0, 100.0):
        print(N, N * dt, lam, run(N, lam))
```

**9. The sweep.** Twelve ticks of $0.06$ s from $z_0=0.27$ m. "Settle" is the first tick after which
$|e|$ stays under $5$ mm; "active row" names any inequality the QP had to enforce during the run.

| $N$ | horizon | $\lambda$ | $u_0$ (N) | peak (N/foot) | overshoot (mm) | settle (s) | active row |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | $0.06$ s | $0.1$ | $181.8$ | $200.0$ | $35.73$ | $0.42$ | $200$ N/foot, $f_z=0$ |
| 1 | $0.06$ s | $1$ | $100.0$ | $108.9$ | $11.25$ | $0.24$ | none |
| 1 | $0.06$ s | $10$ | $18.2$ | $68.0$ | $21.23$ | never | none |
| 1 | $0.06$ s | $100$ | $2.0$ | $59.9$ | $2.46$ | $0.66$ | none |
| 2 | $0.12$ s | $0.1$ | $114.2$ | $115.9$ | $3.72$ | $0.12$ | $f_z=0$ |
| 2 | $0.12$ s | $1$ | $76.9$ | $97.3$ | $1.88$ | $0.12$ | none |
| 2 | $0.12$ s | $10$ | $38.9$ | $78.3$ | $6.40$ | $0.36$ | none |
| 2 | $0.12$ s | $100$ | $7.2$ | $62.5$ | $17.25$ | never | none |
| 4 | $0.24$ s | $0.1$ | $112.7$ | $115.2$ | $3.07$ | $0.12$ | $f_z=0$ |
| 4 | $0.24$ s | $1$ | $76.5$ | $97.1$ | $1.70$ | $0.12$ | none |
| 4 | $0.24$ s | $10$ | $35.3$ | $76.5$ | $1.38$ | $0.24$ | none |
| 4 | $0.24$ s | $100$ | $15.0$ | $66.3$ | $4.01$ | $0.30$ | none |
| 8 | $0.48$ s | $0.1$ | $112.7$ | $115.2$ | $3.06$ | $0.12$ | $f_z=0$ |
| 8 | $0.48$ s | $1$ | $76.4$ | $97.1$ | $1.67$ | $0.12$ | none |
| 8 | $0.48$ s | $10$ | $36.3$ | $77.0$ | $1.35$ | $0.24$ | none |
| 8 | $0.48$ s | $100$ | $14.2$ | $65.9$ | $1.33$ | $0.36$ | none |

**10. Reading the sweep.** Four things the algebra could not have told you.

- **One step is blind to the stop.** At $N=1$, $\lambda=0.1$ the controller asks for $181.8$ N, saturates
  both stance feet at the $200$ N ceiling, overshoots $36$ mm, and then has to hit the *other* bound —
  $f_z=0$, free fall — to come back. Going to $N=2$ at the same weight drops the overshoot to $3.7$ mm
  and the settling time from $0.42$ s to $0.12$ s. The second step is worth more than any weight change
  in the table, because it is the first step that can see the braking.
- **The horizon stops paying almost immediately.** At $\lambda=1$ the first command is $76.9$ N at
  $N=2$, $76.5$ N at $N=4$ and $76.4$ N at $N=8$. Predicting eight times as far changes the applied
  force by $0.7\%$, because the plant's own response is over inside about $0.1$ s and there is nothing
  further out for the cost to see. That is the honest reason legged MPC horizons are short, and it is a
  much better reason than "it has to fit in a millisecond".
- **$\lambda$ is a peak-force-versus-time dial, and it is not monotone in quality.** At $N=8$, raising
  $\lambda$ from $0.1$ to $100$ takes the peak from $115$ to $66$ N per foot and the settling time from
  $0.12$ s to $0.36$ s. At $N=1$ the same sweep is not even ordered: $\lambda=10$ never settles while
  $\lambda=100$ does, because a horizon too short to see the overshoot mistunes in both directions.
- **What the slice hides.** Nothing here ever activated a friction row, since a purely vertical command
  asks for no tangential force. Give Q a horizontal acceleration command and $|f_x|\le\mu f_z$ becomes
  the binding row long before the vertical bounds do — at $\mu=0.6$ the whole-body cap is
  $a\le\mu g=5.89$ m/s², the same number [[04-robotics/legged-locomotion|18. Legged Locomotion]]
  derives from friction alone. The pyramid is the interesting half of this QP; it just is not the half
  you can solve on paper.

**Why read it here**: it is the cleanest case study of the modeling craft this wiki's
optimization page teaches — *choose the approximation that makes the problem convex, and
buy back accuracy with re-solving speed*. Also the classical baseline that learned
locomotion policies (RL) are compared against.

**Suggested path**: [[02-foundations/optimization|optimization page]] → Di Carlo et al. (IROS 2018; open copy on MIT DSpace)
§III–IV (simplified dynamics + QP), skimming §V for results → Kim et al. (arXiv 1909.06586) §III–IV for the MPC + whole-body impulse control stack.

### Self-check

1. Which modelling move makes the friction constraint linear, and what does it give up?
2. Why can the state matrix be shared across the horizon while the input matrix changes every step?
3. In the condensed QP above ($N = 10$, 12 inputs), what happens to the number of decision variables if the horizon doubles?
4. On Q's heave slice every friction-pyramid row came out slack. What command would make one of them the active row instead, and what caps the answer?

> [!tip]- Answers
> 1. Move 4, the friction pyramid: replacing the circular cone by linear facets gives linear inequalities (keeping the QP convex), at the cost of only approximating the true cone: near its edge the facets and the circle disagree about which forces are feasible.
> 2. The state matrix uses one *average* reference yaw over the horizon; the input matrix depends on that step's reference yaw and footholds, which change as the feet move.
> 3. It doubles: $20 \cdot 12 = 240$ variables (and $4\cdot 4\cdot 20 = 320$ pyramid inequalities).
> 4. Any horizontal acceleration command. Asking for $ma$ of tangential force needs $|f_x|\le\mu f_z$ at every stance foot, and since the vertical total is $mg$ in steady support the whole-body cap is $a\le\mu g=0.6\times9.81=5.89$ m/s² whatever the gait — the same number [[04-robotics/legged-locomotion|18. Legged Locomotion]] gets from friction alone. The vertical bounds are nowhere near binding at that point, which is why the pyramid, not the unilateral row, is the interesting half of the real QP.

### Problem set · 과제

Tier A. Using **Q**, this page and [[04-robotics/legged-locomotion|18. Legged Locomotion]]. Running
task: a quadruped carries **P2** toward a panel ([[02-foundations/lab-plants|0.6]]).

**The change of knobs.** Q starts $5$ cm **high**, not low: $z_0=0.35$ m, $\dot z_0=0$, so
$e_0=+0.05$ m. Same $\Delta t$, same trot, same bounds.

1. **Draw.** The three-part homework diagram for this case: the timeline with $e_0$ now above the
   dashed reference, the trot chart with the $0.12$ s window shaded inside one stance, and the
   constraint block with the swing cells crossed out. Add one thing the lecture's version did not
   need: mark on the block which row you expect the answer to hit, and say before computing anything
   why you expect it.
2. **Derive.** (a) $e_0/\alpha$ for this case. (b) Solve the $2\times2$ system at $\lambda=1$ by hand
   and give $u_0$, $u_1$ and $f_z^{\mathrm{tot}}$. (c) Is that solution feasible? If not, name the row,
   give the clamped $u_0$ and the per-foot force. (d) Repeat (b) at $\lambda=10$ — the matrix changes
   in one place only — and say whether the same row binds.
3. **Do.** Fill the `?` in the template. It is the lecture's loop with the sign of $e_0$ flipped and
   the reporting narrowed. Run $N\in\{1,2,4,8\}$ against $\lambda\in\{1,10\}$ for $12$ ticks and
   report, for each: the first applied $u_0$, whether the unconstrained solve was feasible on tick 1,
   the lowest per-foot force reached during the run, and the settling time. Then answer from the table
   rather than from intuition: does a longer horizon change whether the binding row activates? Say
   what *does* change it, and give the physical reason the other knob cannot.

```python
# Q, heave slice of the convex MPC. Fill ?. condensed() and solve_box() are the lecture's.
import numpy as np
m, g, dt = 12.0, 9.81, 0.06
n_st, fz_max = 2, 200.0
alpha = dt**2 / (2*m)
u_lo, u_hi = ?, ?                       # -m*g  and  n_st*fz_max - m*g
for N in (1, 2, 4, 8):
    for lam in (1.0, 10.0):
        e, zd, u0, low, feas, hist = 0.05, 0.0, None, 1e9, None, []
        for _ in range(12):
            H, f = condensed(N, e, zd, lam)
            free = np.linalg.solve(H, -f)
            u = solve_box(H, f, u_lo, u_hi)
            if feas is None: feas = ?    # was the unconstrained tick-1 answer inside the box?
            if u0 is None: u0 = u[0]
            low = min(low, ?)            # (m*g + u[0]) / n_st
            e, zd = ?, ?                 # e + dt*zd + alpha*u[0] ,  zd + dt/m*u[0]
            hist.append(e)
        settle = next(((i+1)*dt for i in range(len(hist))
                       if all(abs(x) <= 0.005 for x in hist[i:])), None)
        print(N, lam, round(u0, 1), feas, round(low, 1), settle)
```

> [!tip]- Solutions
> 1. You should expect the unilateral row $f_z\ge0$. Being high means the cost wants a *downward* correction, the only downward force available is gravity, and the feet can only push — so the request will run into $f_z^{\mathrm{tot}}\ge0$ rather than into the $200$ N ceiling. Predicting the active row before solving is the skill; the $200$ N ceiling is the row that binds when you start low and weight force cheaply, which is the lecture's $N=1$, $\lambda=0.1$ line.
> 2. (a) $e_0/\alpha=0.05/1.5\times10^{-4}=333.3$ N. (b) $11u_0+3u_1=-1333.3$, $3u_0+2u_1=-333.3$, determinant $13$, so $u_0=-1666.7/13=-128.21$ N and $u_1=333.3/13=25.64$ N, giving $f_z^{\mathrm{tot}}=117.72-128.21=-10.49$ N. (c) Not feasible: that is a *pulling* foot. The unilateral row binds, $u_0$ clamps to $-mg=-117.72$ N, $f_z^{\mathrm{tot}}=0$ and each stance foot carries $0$ N — the QP's answer is to unload the legs and fall for one tick. (d) Only the diagonal changes, to $20u_0+3u_1=-1333.3$, $3u_0+11u_1=-333.3$, determinant $211$, giving $u_0=-13666.7/211=-64.77$ N and $u_1=-2666.7/211=-12.64$ N. Now $f_z^{\mathrm{tot}}=117.72-64.77=52.95$ N, i.e. $26.47$ N per foot, and nothing binds. The *weight*, not the geometry, decided whether the constraint was active.
> 3. Blanks: `u_lo, u_hi = -m*g, n_st*fz_max - m*g`; `feas = (u_lo <= free[0] <= u_hi)`; `low = min(low, (m*g + u[0]) / n_st)`; `e, zd = e + dt*zd + alpha*u[0], zd + dt/m*u[0]`. The table: at $\lambda=1$, every $N$ is infeasible on tick 1, applies $u_0=-117.72$ N, unloads the feet to $0$ N and settles in $0.42$ s at $N=1$ and $0.18$ s at $N=2,4,8$. At $\lambda=10$, every $N$ is feasible, with $u_0=-30.3,\,-64.8,\,-58.9,\,-60.5$ N and a lowest per-foot force of $43.7,\,26.5,\,29.4,\,28.6$ N; $N=1$ never settles and the rest take $0.42$, $0.24$, $0.24$ s. **The horizon does not move the row at all** — the weight does, and the answer is the physical reason why. Coming *down* is capped by free fall: with the feet fully unloaded the body loses only $\tfrac12 g\Delta t^2=17.7$ mm in one tick, so any plan that wants $50$ mm gone quickly asks for a pulling foot no matter how far ahead it looks. Lengthening the horizon changes how the descent is distributed, not how fast gravity works, and at $N=2$ it actually asks for *more* than at $N=1$ ($-64.8$ against $-30.3$ N) because it can now plan the catch. Raising $\lambda$ works because it makes the controller want less, which is a different mechanism from making the plant able to do more — and a paper that reports tuning one knob without the other has told you half of its controller.

**Where P2 is still missing.** Everything above is the body alone. Mount P2 and the QP is wrong in
three named ways: $m$ is $14$ kg, not $12$; $I_B$ is a box's inertia and does not include the arm's
contribution about the new centre of mass; and the reaction wrench the arm applies while pressing a
panel is an external force the single-rigid-body model has no term for at all. The QP would absorb it
as an unexplained tracking error and fight it with foot forces. That is the honest reading of "no arm,
no tool wrench, no P3 wall".

> [!tip]- Claim-reading, kept from the earlier version of this set
> - **Claim.** The timing claim for the condensed QP is the sub-millisecond solve, re-run at tens of Hz (abstract 20–30 Hz, experiments 25–50 Hz) — those times *are* the claim.
> - **Falsify.** Pitch $30^\circ$: the neglected factors are $\tan 30^\circ=0.577$ and $1/\cos 30^\circ=1.155$, which this page already calls no longer small. A rear-up or a fall would do it.
> - **Task.** P2 on that body, pressing the panel: no arm, no tool wrench, no P3 wall. Ground-reaction forces on four feet are the decisions; contact at the panel is outside the QP.

## 한국어

*D군의 마지막이자 그 응용 사례다. [[04-robotics/mpc|7. MPC]]·[[04-robotics/contact-force-tactile|9. 접촉]]과 [[04-robotics/modern-robotics/index|MR 챕터 요약]] 위에 선다.
최적화 페이지가 가르치는 기술 — 문제를 볼록하게 만드는 근사를 고르는 것 — 의 가장 깔끔한 사례 연구다.*

### 이 페이지의 장치 · Running object

몸통은 [[04-robotics/legged-locomotion|18. 레그드 로코모션]]의 고정 사족 **Q**다. $m=12$ kg,
무게중심 높이 $0.30$ m, 발은 $(\pm0.30,\pm0.15)$ m, $\mu=0.6$, 주기 $T=0.40$ s에 듀티 팩터
$\beta=0.50$인 trot, 발당 한계 $f_{z,\max}=200$ N. QP에는 필요하지만 로코모션 페이지에는 쓸 일이
없던 숫자가 넷이다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $I_B$ | $\mathrm{diag}(0.104,\,0.374,\,0.450)\,\mathrm{kg\,m^2}$ | 몸통 관성. $12$ kg의 균일한 $0.60\times0.30\times0.12$ m 상자 |
| $\Delta t$ | $0.06\,\mathrm{s}$ | MPC 지평의 한 스텝 |
| $N$ | $2$ | 지평 길이, 곧 $0.12$ s의 예측 |
| $q,\ r$ | $q=1\,\mathrm{m^{-2}}$, $r=\lambda\,q\,\alpha^2$ | 추종·힘 가중치. $\lambda$가 무차원 손잡이, 기준값 $\lambda=1$ |

아래에서 푸는 경우는 $z_0=0.27$ m, $\dot z_0=0$에서 시작한다. Q가 명령 높이
$z^{\mathrm{ref}}=0.30$ m보다 $3$ cm 내려앉아 있고 다시 밀어 올려야 한다.

$0.12$ s 지평은 trot의 $0.20$ s 디딤보다 짧다. 그래서 **접촉 스케줄이 지평 내내 고정**이다 —
지평의 모든 스텝에서 같은 대각선 두 발이 땅에 있고, 도중에 발이 떨어지지 않으며, 유각 등식이
켜지거나 꺼지지도 않는다. 아래 QP를 종이 위에서 끝낼 수 있는 이유가 그것이고, 동시에 제어기의
실제 성질이기도 하다. Di Carlo 등이 초당 수십 번 다시 푸는 것은 매 풀이가 짧고 거의 정적인
스케줄만 보게 하기 위해서다.

### 과제가 그릴 그림 · Homework diagram

그림 하나에 칸이 셋이고, 과제가 요구하는 것도 같은 그림이다.

**왼쪽 — 지평 타임라인.** $0$, $\Delta t$, $2\Delta t$에 눈금이 있는 시간 축. 첫 눈금에 측정
상태 $x_0$, 앞 두 눈금에서 떠나는 화살표로 결정 $u_0$와 $u_1$, 그리고 그것들이 도착하는 눈금에
예측 상태 $x_1$, $x_2$를 표시한다. 기준 높이 $z^{\mathrm{ref}}$를 세 눈금을 가로지르는 파선으로
긋고, 비용이 제곱하고 있는 간격 $e_k=z_k-z^{\mathrm{ref}}$를 칠한다. $u_0$에 동그라미를 친다.
실제로 적용되는 결정은 그것 하나뿐이다.

**가운데 — 스케줄.** 같은 축 아래에 [[04-robotics/legged-locomotion|18. 레그드 로코모션]]의
trot 보행 차트를 다시 그리고 지평이 덮는 $0.12$ s를 칠한다. 이 그림의 요점은 칠한 창이 한 디딤
구간 안에 들어간다는 것이다.

**오른쪽 — 제약 블록.** 결정 벡터를 격자로 그린다. 발 $4$개 $\times$ 힘 성분 $3$개 $\times$
스텝 $2$개 $=24$칸. 유각 중인 두 발의 $12$칸을 지운다. 등식 $f_i=0$이 그것이다. 남은 디딤발
하나에 피라미드 네 면 $\pm f_x\le\mu f_z$, $\pm f_y\le\mu f_z$를 네 개의 선으로, 단방향 한계
$f_z\ge0$을 다섯 번째로 그린다. 남은 것을 센다. 그 수가 곧 QP다.

**무엇인가**: 보행 로봇에서 실시간 MPC를 표준으로 만든 논문. 비결은 *의도된 단순화*이고,
다섯 가지 모델링 선택으로 이루어진다:

1. **단일 강체**: 로봇을 단일 강체로 근사한다(다리 동역학 무시). 다리가 몸통에 비해 가벼우면 합리적이지만, 실제로 빠뜨리는 것이 있다. 다리를 빠르게 휘두를 때의 운동량은 모델에 아예 없다.
2. **작은 롤·피치**: 회전 동역학을 롤과 피치가 작다는 가정 아래 선형화한다(롤·피치·요는 몸통의
   앞뒤·좌우·수직 축에 대한 회전이다). 상태 행렬 하나는
   지평 전체 기준 궤적의 *평균* 요를 쓰고, 단계별 입력 행렬은 그 단계의 기준 요와 발 위치를
   쓴다. 단 하나의 예외는 첫 단계로, 그 단계는 대신 현재 로봇 상태를 쓴다.
3. **힘을 결정 변수로**: 지면 반력을 결정 변수로 삼는다.
4. **마찰 피라미드**: 원형 마찰 원뿔을 선형 면들로 이루어진 마찰 피라미드로 근사한다.
5. **condensed QP, 빠른 풀이**: 이 선형 부등식 덕분에 문제는 **볼록 QP**로 남고,
   [[04-robotics/mpc|7. MPC §2]]의 condensed 형태로 푼다. 보고된 구현에서 1밀리초 안에 풀리고
   수십 Hz로 다시 돈다(Di Carlo 등의 초록은 20~30 Hz지만 실험은 보행 방식에 따라 25~50 Hz로
   돌았다. 그러니 [[04-robotics/mpc|7. MPC §2]]가 잡는 50 Hz는 논문 자신의 범위 상단이지
   불일치가 아니다). 정확히 [[02-foundations/optimization|4. 최적화 §5]]의 기계장치다.

**다섯 선택 뒤의 모델을 풀어 쓰면.**

- **단일 강체 동역학**(선택 1). 다리를 질량 없는 것으로 보면 몸통에 작용하는 힘은 중력과 네 지면 반력뿐이므로 뉴턴·오일러 방정식이 다음을 준다.
$$m\,\ddot p=\sum_{i=1}^{4}f_i-m\,g,\qquad \frac{d}{dt}\big(I\,\omega\big)=\sum_{i=1}^{4}r_i\times f_i$$
  $m$은 전체 질량, $p$는 무게중심 위치, $g=(0,0,9.81)$ m/s², $f_i\in\mathbb{R}^3$는 발 $i$의 지면 반력, $r_i$는 무게중심에 대한 발 위치, $I$는 월드 축의 몸통 관성, $\omega$는 각속도다. 예: 네 발로 하중을 똑같이 나눠 가만히 선 12 kg 로봇은 발마다 $f_{i,z}=12\times9.81/4=29.43$ N이 필요하다. 반례: 빠르게 휘두르는 2 kg 다리가 나르는 운동량에는 이 식에 해당 항이 없다.
- **작은 롤·피치**(선택 2). 롤·피치·요를 $\Theta=(\phi,\theta,\psi)$로 쓴다. $\omega$에서 $\dot\Theta$로 가는 정확한 사상에는 $\tan\theta$와 $1/\cos\theta$ 인자가 들어 있다. $\phi\approx\theta\approx0$이면 요만 남고, 월드 프레임 관성도 몸통 프레임 관성 $I_B$를 요만큼 돌린 것만 남는다.
$$\dot\Theta\approx R_z(\psi)^\top\omega,\qquad I\approx R_z(\psi)\,I_B\,R_z(\psi)^\top$$
  자이로 항 $\omega\times I\omega$도 작다고 보고 버린다. 피치 $5°$에서 버린 인자는 $\tan5°=0.087$, $1/\cos5°=1.004$이고, $30°$에서는 $0.577$과 $1.155$라 근사가 더는 작지 않다. 13차원 상태 $x=(\Theta,p,\omega,\dot p,g)$(모델에 오프셋 항이 없도록 중력을 상수 상태로 덧붙임)로 이산화하면 $x_{k+1}=A\,x_k+B_k\,u_k$가 되고, $A$는 평균 요로 하나, $B_k$는 단계마다 하나다.
- **힘을 결정 변수로**(선택 3). 단계 $k$의 입력은 $u_k=(f_1,\dots,f_4)\in\mathbb{R}^{12}$다. 보행 양식의 **접촉 스케줄**([[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]])이 단계마다 어느 발이 땅에 있는지 정하고, 유각 중인 발은 땅을 밀 수 없으므로 등식 제약 $f_i=0$을 받는다.
- **마찰 피라미드**(선택 4). [[04-robotics/contact-force-tactile|접촉·힘·촉각 §2]]의 원형 원뿔 $\sqrt{f_x^2+f_y^2}\le\mu f_z$는 선형이 아니다. 접선 축을 따로따로 묶으면 선형이 되고, 절댓값 하나가 선형 부등식 둘이므로 아래에서 세는 면 네 개가 나온다.
$$|f_x|\le\mu f_z,\qquad |f_y|\le\mu f_z$$
  예: $\mu=0.6$, $f_z=100$ N. 원뿔은 접선력을 $60$ N까지 허용하지만 피라미드의 모서리 $(60,60)$ N은 크기가 $84.9$ N이라, 이 피라미드는 미끄러질 힘을 허용한다. 계수를 $\mu/\sqrt2=0.424$로 줄이면 모서리가 정확히 $60$ N이 되어 안전하지만, 실제 원뿔이 허용하는 $(60,0)$은 거부한다.
- **QP**(선택 5). 명령한 몸통 운동에서 온 기준 상태 $x^{\text{ref}}_k$, 추종 오차 가중치 $Q\succeq0$, 힘 크기 가중치 $R\succ0$, $\lVert v\rVert_Q^2=v^\top Qv$로 제어기는 다음을 푼다.
$$\min_{u_0,\dots,u_{N-1}}\ \sum_{k=0}^{N-1}\lVert x_{k+1}-x_{k+1}^{\text{ref}}\rVert_Q^2+\lVert u_k\rVert_R^2$$
  제약은 동역학, 피라미드 부등식, 유각 등식이다. 비용이 이차이고 모든 제약이 선형이므로 볼록 QP이고, 동역학을 대입해 없애면 condensed 형태가 남는다.

Cheetah 3가 이걸로 질주했고, 후속(Kim et al., 공개 접근)은 MPC를 전신 임펄스
제어([[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §4]]의 영공간 과제 우선순위와 전신 QP로 짜인 것)와 결합한다 — 느린 MPC가 힘을 계획하고 빠른 WBC가 추종하는 표준 2단 스택으로,
[[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]의 System 2/System 1 분할과 공명한다.

> [!example] 계산 예제 · Worked example
> QP는 얼마나 큰가? 상태 13차원, 발 4개 × 힘 성분 3개 = 단계당 입력 12개, 지평 $N = 10$으로 잡는다.
> - condensed 형태는 상태를 소거하므로 결정 변수는 힘뿐이다: $N \cdot 12 = 120$개.
> - (상태도 변수로 두면 $10\cdot 13 + 10\cdot 12 = 250$개 — condensed는 이를 더 조밀한 행렬과 맞바꾼다.)
> - 마찰 피라미드: 발마다, 단계마다 면 4개: $4 \cdot 4 \cdot 10 = 160$개의 선형 부등식.
> - 여기서는 피라미드 면만 셌다. 구현이 더하는 힘 한계나 유각(swing) 발 제약은 그 위에 추가되며 세지 않았다.
> - 변수 120개, 부등식 160개짜리 QP는 아주 작다. 1밀리초 미만 풀이가 가능한 이유다.

### 장치로 한 번 끝까지 · Worked on Q

위 상자는 논문 자신의 $N=10$ QP 크기를 잰다. 이 절은 Q 위의 $N=2$ QP를 손으로 풀고, 그다음
실제로 조율하게 되는 두 가지를 루프가 바꿔 보게 한다.

**1. 절단면, 그리고 그것이 정직한 이유.** Q에게 수평 운동 없이 높이만 유지하라고 명령한다. 그러면
모든 발에서 $f_x=f_y=0$이고 롤·피치 채널은 기준값에 있으며, 입력 12개짜리 문제가 스텝당 결정
하나로 줄어든다. 디딤발 둘이 나눠 갖는 *총* 수직력 $f_z^{\mathrm{tot}}$다. Q를 그냥 떠받치는 힘과의
차이를 $u=f_z^{\mathrm{tot}}-mg$로 쓰면 선택 1의 뉴턴 방정식이 $m\ddot z=u$가 되고, 일정한 $u$
위에서 정확히 적분하면 이산 모델이 나온다.

$$z_{k+1}=z_k+\Delta t\,\dot z_k+\frac{\Delta t^2}{2m}u_k,\qquad \dot z_{k+1}=\dot z_k+\frac{\Delta t}{m}u_k$$

선택 2의 $x_{k+1}=Ax_k+B_ku_k$를, 순수한 수직 명령에서 움직이는 두 행으로 제한한 것과 같다. 다른
모델이 아니라 절단면이고, 그 절단면이 무엇을 가리는지는 아래 10번이 말한다.

**2. Condensing.** $e_k=z_k-z^{\mathrm{ref}}$, 그리고
$\alpha=\Delta t^2/(2m)=0.06^2/24=1.5\times10^{-4}$ m/N로 둔다. $\dot z_0=0$에서 동역학을 앞으로
대입하면 상태가 소거되는데, [[04-robotics/mpc|7. MPC §2]]가 condensed 형태라 부르는 것이 이것이다.

$$e_1=e_0+\alpha u_0,\qquad e_2=e_0+3\alpha u_0+\alpha u_1$$

$3\alpha$가 나오는 것은 $u_0$가 $e_2$에 두 번 작용하기 때문이다. 첫 구간에서 옮긴 위치로 한 번,
그리고 남긴 속도로 또 한 번, $\alpha+2\alpha=3\alpha$다.

**3. 비용과 정규방정식.** 추종 오차에 $q$, 힘에 $r=\lambda q\alpha^2$를 두고
$J=q(e_1^2+e_2^2)+r(u_0^2+u_1^2)$로 쓴 뒤 두 편미분을 0으로 두고 $2q\alpha^2$로 나누면, 모든
성분이 순수한 수이고 우변이 힘인 $2\times2$ 연립이 남는다.

$$\begin{pmatrix}10+\lambda&3\\3&1+\lambda\end{pmatrix}\begin{pmatrix}u_0\\u_1\end{pmatrix}=-\frac{e_0}{\alpha}\begin{pmatrix}4\\1\end{pmatrix}$$

$\lambda$가 대각선에 앉는 것은 힘 벌점만이 $u_k$ 하나에만 닿는 항이기 때문이고, 그래서 그것을
키우면 행렬이 더 대각 우세해지며 해가 작아진다 — "힘에 가중치를 더 준다"가 "덜 세게 민다"를
뜻하는 기제가 통째로 이것이다.

**4. 한 스텝을 끝까지.** 기준값 $\lambda=1$, $e_0=-0.03$ m이므로 $e_0/\alpha=-200$ N이다.

$$\begin{pmatrix}11&3\\3&2\end{pmatrix}\begin{pmatrix}u_0\\u_1\end{pmatrix}=\begin{pmatrix}800\\200\end{pmatrix}\mathrm{N}\ \Longrightarrow\ u_0=\frac{1600-600}{13}=\frac{1000}{13}=76.92\ \mathrm{N},\quad u_1=\frac{2200-2400}{13}=-15.38\ \mathrm{N}$$

행렬식이 $22-9=13$이기 때문이다. 물리 단위로 첫 명령은
$f_z^{\mathrm{tot}}=mg+u_0=117.72+76.92=194.64$ N이고, 디딤발 둘이 각각 $97.32$ N으로 나눈다.
이 명령이 속한 계획은 $e_1=-0.03+1.5\times10^{-4}(76.92)=-0.0185$ m와 $e_2=+0.0023$ m를
예측한다. 일부러 $2.3$ mm 지나친다. $\dot z_1=\Delta t\,u_0/m=0.385$ m/s로 도착한 뒤 제동하는
편이 이 비용에서는 살금살금 올라가는 것보다 싸기 때문이다.

**5. 제약 행들, 그리고 그중 걸리는 것.** $N=2$ trot QP 전체를 세면 이렇다. 결정 변수
$4\times3\times2=24$개, 그중 $2\times3\times2=12$개가 유각 등식 $f_i=0$으로 죽고 $12$개가 남는다.
마찰 피라미드 부등식 $4\times4\times2=32$개, 단방향 행 $f_{z,i}\ge0$이 $4\times2=8$개, 발당
$200$ N 천장을 부과하면 $8$개가 더 붙는다. **활성(active)** 제약이란 최적해가 등호로 만족시키는
부등식 행이어서 지우면 답이 움직이는 행이고, **여유(slack)** 행은 부등호로 만족되어 지워도 아무
일이 없는 행이다. 위의 해에서는 피라미드 행이 전부 여유다. 명령이 수직뿐이라
$|f_x|=0\le\mu f_z=0.6\times97.32=58.39$ N이고 $58.39$ N이나 남기 때문이다. 디딤발의 단방향 행도
두 스텝 모두 여유다. $97.32$ N과 $(117.72-15.38)/2=51.17$ N이 둘 다 양수이기 때문이다. 모든 행이 여유이므로 제약 없는 정류점이 *곧* QP의 해이고, 종이 위에서
푼 것이 허용되는 근거가 그것이다. 반례: 피라미드 행이 비활성인 것은 "마찰이 크기 때문"이 아니라
바로 이 명령이 접선력을 전혀 요구하지 않기 때문이고, 옆으로 한 걸음만 내디디면 그 행이 모든 것을
결정하는 행이 된다.

**6. 행이 실제로 걸릴 때.** 연립이 $e_0$에 대해 선형이므로 Q를 $10$ cm *높은* 곳에서
시작시켜 보자($e_0=+0.10$ m, $e_0/\alpha=666.7$ N). 같은 행렬이 $u_0=-256.4$ N, 곧
$f_z^{\mathrm{tot}}=117.72-256.4=-138.7$ N을 돌려준다. 발은 당길 수 없다. 단방향 행이
활성화되고 QP는 $f_z^{\mathrm{tot}}=0$으로 물리며, 최적 행동은 미는 것을 멈추고 중력에 맡기는
것이 된다. 매끄러운 비용에 가중치를 바꿔도 갑자기 반응하지 않는 해 — 그 불연속이 부등식 행이
존재하는 이유이고, 비용만 적어 보여 주는 설명에서는 결코 보이지 않는다.

**7. Receding horizon.** 적용되는 것은 $u_0$뿐이다. **Receding-horizon 제어**는 궤적이 아니라
피드백 정책이다. 매 틱마다 (i) 상태를 측정하고, (ii) 거기서 출발하는 유한 지평 최적 제어 문제를
풀고, (iii) 첫 입력만 적용하고, (iv) 나머지는 버리고 반복한다. 정책은 위 풀이의 $u^\star$에 대해
$u(x)=[\,u_0^\star(x)\,]$다. 예: Q는 $76.92$ N을 $\Delta t$ 동안 적용하고, 다시 측정하고, 실제로
있는 자리에서 다시 푼다 — $\alpha$의 모델 오차가 누적되는 대신 다음 틱에 교정된다. 반례: 한 번
풀고 $u_0,u_1$을 지평 끝까지 재생하는 것은 receding horizon이 *아니다*. 그것은 개루프 궤적이고,
실제 $m$이 10% 다른 로봇에서는 되돌릴 것이 없이 흘러간다. 논문의 지평이 아니라 재풀이 주기가 이
제어기를 작동하게 만드는 숫자인 이유다.

**8. 루프, 그리고 손잡이 둘.** 위의 모든 것은 한 설정에서의 한 틱이다. 실무자가 실제로 고르는
것은 지평 $N$과 가중치 비 $\lambda$이고, 둘 사이의 맞거래는 손 계산이 보여 줄 수 없다. 그것은
단방향 행이 켜졌다 꺼졌다 하는 여러 틱의 폐루프 안에 산다. 영어 쪽의 파이썬 루프가 그
condensed QP를 매 틱 세우고, 활성 집합으로 상자 제약을 풀고, 첫 입력만 적용하며, 아래 표를
찍는다.

**9. 스윕.** $z_0=0.27$ m에서 $0.06$ s로 열두 틱. "정착"은 그 뒤로 $|e|$가 계속 $5$ mm 아래인
첫 틱이고, "활성 행"은 그 실행 중 QP가 실제로 강제해야 했던 부등식이다.

| $N$ | 지평 | $\lambda$ | $u_0$ (N) | 최대 (N/발) | 오버슈트 (mm) | 정착 (s) | 활성 행 |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | $0.06$ s | $0.1$ | $181.8$ | $200.0$ | $35.73$ | $0.42$ | $200$ N/발, $f_z=0$ |
| 1 | $0.06$ s | $1$ | $100.0$ | $108.9$ | $11.25$ | $0.24$ | 없음 |
| 1 | $0.06$ s | $10$ | $18.2$ | $68.0$ | $21.23$ | 안 함 | 없음 |
| 1 | $0.06$ s | $100$ | $2.0$ | $59.9$ | $2.46$ | $0.66$ | 없음 |
| 2 | $0.12$ s | $0.1$ | $114.2$ | $115.9$ | $3.72$ | $0.12$ | $f_z=0$ |
| 2 | $0.12$ s | $1$ | $76.9$ | $97.3$ | $1.88$ | $0.12$ | 없음 |
| 2 | $0.12$ s | $10$ | $38.9$ | $78.3$ | $6.40$ | $0.36$ | 없음 |
| 2 | $0.12$ s | $100$ | $7.2$ | $62.5$ | $17.25$ | 안 함 | 없음 |
| 4 | $0.24$ s | $0.1$ | $112.7$ | $115.2$ | $3.07$ | $0.12$ | $f_z=0$ |
| 4 | $0.24$ s | $1$ | $76.5$ | $97.1$ | $1.70$ | $0.12$ | 없음 |
| 4 | $0.24$ s | $10$ | $35.3$ | $76.5$ | $1.38$ | $0.24$ | 없음 |
| 4 | $0.24$ s | $100$ | $15.0$ | $66.3$ | $4.01$ | $0.30$ | 없음 |
| 8 | $0.48$ s | $0.1$ | $112.7$ | $115.2$ | $3.06$ | $0.12$ | $f_z=0$ |
| 8 | $0.48$ s | $1$ | $76.4$ | $97.1$ | $1.67$ | $0.12$ | 없음 |
| 8 | $0.48$ s | $10$ | $36.3$ | $77.0$ | $1.35$ | $0.24$ | 없음 |
| 8 | $0.48$ s | $100$ | $14.2$ | $65.9$ | $1.33$ | $0.36$ | 없음 |

**10. 표 읽기.** 대수로는 알 수 없었을 것 넷.

- **한 스텝은 정지를 보지 못한다.** $N=1$, $\lambda=0.1$에서 제어기는 $181.8$ N을 요구해 디딤발
  둘을 $200$ N 천장에 포화시키고, $36$ mm 지나친 뒤, 돌아오려고 반대쪽 한계 — $f_z=0$, 곧 자유
  낙하 — 까지 친다. 같은 가중치에서 $N=2$로 가면 오버슈트가 $3.7$ mm로, 정착이 $0.42$ s에서
  $0.12$ s로 떨어진다. 표의 어떤 가중치 변경보다 두 번째 스텝이 더 값어치 있다. 제동을 볼 수 있는
  첫 스텝이 그것이기 때문이다.
- **지평은 거의 곧바로 값을 멈춘다.** $\lambda=1$에서 첫 명령은 $N=2$에 $76.9$ N, $N=4$에
  $76.5$ N, $N=8$에 $76.4$ N이다. 여덟 배 멀리 내다봐도 적용되는 힘은 $0.7\%$ 달라질 뿐이다.
  플랜트 자신의 반응이 대략 $0.1$ s 안에 끝나 비용이 볼 것이 더 없기 때문이다. 보행 MPC의 지평이
  짧은 정직한 이유가 그것이고, "1밀리초 안에 들어가야 해서"보다 훨씬 나은 이유다.
- **$\lambda$는 최대 힘 대 시간의 다이얼이고, 품질에 단조롭지 않다.** $N=8$에서 $\lambda$를
  $0.1$에서 $100$으로 올리면 최대가 발당 $115$ N에서 $66$ N으로, 정착이 $0.12$ s에서 $0.36$ s로
  간다. $N=1$에서는 같은 스윕이 순서조차 맞지 않는다. $\lambda=10$은 정착하지 못하는데
  $\lambda=100$은 정착한다. 오버슈트를 볼 수 없을 만큼 짧은 지평은 양쪽으로 다 잘못 조율된다.
- **절단면이 가리는 것.** 여기서는 마찰 행이 한 번도 활성화되지 않았다. 순수한 수직 명령이 접선력을
  요구하지 않기 때문이다. Q에게 수평 가속 명령을 주면 수직 한계보다 한참 먼저 $|f_x|\le\mu f_z$가
  걸리는 행이 된다 — $\mu=0.6$에서 전신 상한은 $a\le\mu g=5.89$ m/s²이고,
  [[04-robotics/legged-locomotion|18. 레그드 로코모션]]이 마찰만으로 유도하는 바로 그 수다.
  이 QP에서 흥미로운 절반은 피라미드다. 다만 종이 위에서 풀 수 있는 절반이 아닐 뿐이다.

**여기서 읽는 이유**: 이 위키 최적화 페이지가 가르치는 모델링 기술 — *문제를 볼록하게
만드는 근사를 고르고, 정확도는 재풀이 속도로 되산다* — 의 가장 깔끔한 사례 연구다.
학습 기반 보행 정책(RL)이 비교당하는 고전 베이스라인이기도 하다.

**권장 경로**: [[02-foundations/optimization|최적화 페이지]] → Di Carlo 외(IROS 2018; MIT DSpace 공개본) §III~IV(단순화 동역학 + QP), 결과는 §V를 훑기 → Kim 외(arXiv 1909.06586) §III~IV에서 MPC + 전신 임펄스 제어 스택.

### 스스로 점검

1. 마찰 제약을 선형으로 만드는 모델링 선택은 무엇이고, 그 대가는?
2. 상태 행렬은 지평 전체에서 하나를 공유하는데 입력 행렬은 왜 단계마다 바뀌는가?
3. 위 condensed QP($N = 10$, 입력 12개)에서 지평을 두 배로 늘리면 결정 변수 수는?
4. Q의 수직 절단면에서는 마찰 피라미드 행이 전부 여유로 나왔다. 대신 그중 하나를 활성 행으로 만드는 명령은 무엇이고, 그 답의 상한은 무엇이 정하는가?

> [!tip]- 정답
> 1. 4번, 마찰 피라미드: 원형 원뿔을 선형 면으로 바꿔 선형 부등식을 얻고(QP가 볼록하게 남음), 대신 실제 원뿔은 근사로만 남는다: 가장자리 근처에서는 면과 원이 어떤 힘이 허용되는지 서로 다르게 판정한다.
> 2. 상태 행렬은 지평 전체의 *평균* 기준 요 하나를 쓰지만, 입력 행렬은 그 단계의 기준 요와 발 위치에 의존하고 이것들은 발이 움직이며 바뀐다.
> 3. 두 배가 된다: $20 \cdot 12 = 240$개 (피라미드 부등식은 $4\cdot 4\cdot 20 = 320$개).
> 4. 수평 가속 명령이면 어느 것이든 된다. 접선력 $ma$를 요구하려면 디딤발마다 $|f_x|\le\mu f_z$가 필요하고, 정상 지지에서 수직 총합이 $mg$이므로 전신 상한은 보행 양식과 무관하게 $a\le\mu g=0.6\times9.81=5.89$ m/s²다 — [[04-robotics/legged-locomotion|18. 레그드 로코모션]]이 마찰만으로 얻는 그 수와 같다. 그 지점에서 수직 한계는 걸릴 근처에도 가지 않으며, 실제 QP에서 흥미로운 절반이 단방향 행이 아니라 피라미드인 이유가 그것이다.

### 과제 · Problem set

Tier A. **Q**, 이 페이지, [[04-robotics/legged-locomotion|18. 레그드 로코모션]]을 쓴다. 관통
과제: 사족이 [[02-foundations/lab-plants|0.6]]의 **P2**를 패널로 나른다. 파이썬 목록은 영어 쪽에
한 번만 있다.

**바꿀 손잡이.** Q가 낮은 곳이 아니라 $5$ cm **높은** 곳에서 시작한다. $z_0=0.35$ m,
$\dot z_0=0$이므로 $e_0=+0.05$ m다. $\Delta t$도, trot도, 한계도 그대로다.

1. **그려라.** 이 경우에 대한 과제 그림 세 칸. $e_0$가 이번에는 파선 기준 위에 있는 타임라인,
   $0.12$ s 창이 한 디딤 안에 칠해진 trot 차트, 유각 칸을 지운 제약 블록. 강의판에는 없던 것을
   하나 더한다. 답이 어느 행에 부딪힐 것 같은지 블록 위에 표시하고, 계산하기 *전에* 왜 그렇게
   예상하는지 적는다.
2. **유도하라.** (a) 이 경우의 $e_0/\alpha$. (b) $\lambda=1$에서 $2\times2$ 연립을 손으로 풀어
   $u_0$, $u_1$, $f_z^{\mathrm{tot}}$을 낸다. (c) 그 해는 실행 가능한가? 아니라면 행의 이름을
   대고, 물린 $u_0$와 발당 힘을 준다. (d) $\lambda=10$에서 (b)를 반복한다 — 행렬은 한 자리만
   바뀐다 — 그리고 같은 행이 걸리는지 말한다.
3. **해 보라.** 영어 쪽 템플릿의 `?`를 채운다. 강의의 루프에서 $e_0$의 부호를 뒤집고 보고 항목을
   좁힌 것이다. $N\in\{1,2,4,8\}$과 $\lambda\in\{1,10\}$을 열두 틱씩 돌려, 각각에 대해 첫 적용
   $u_0$, 첫 틱의 제약 없는 해가 실행 가능했는지, 실행 중 도달한 최저 발당 힘, 정착 시간을
   보고한다. 그다음 직관이 아니라 표를 보고 답한다: 지평을 늘리면 걸리는 행이 활성화되는지 여부가
   달라지는가? 무엇이 그것을 바꾸는지 말하고, 다른 손잡이가 바꿀 수 *없는* 물리적 이유를 대라.

> [!tip]- 정답 · Solutions
> 1. 단방향 행 $f_z\ge0$을 예상해야 한다. 높다는 것은 비용이 *아래쪽* 교정을 원한다는 뜻이고, 쓸 수 있는 아래쪽 힘은 중력뿐이며, 발은 밀 수만 있다. 그러니 요구는 $200$ N 천장이 아니라 $f_z^{\mathrm{tot}}\ge0$에 부딪힌다. 풀기 전에 활성 행을 맞히는 것이 이 문제의 기술이다. $200$ N 천장은 낮은 곳에서 시작하고 힘을 싸게 매길 때 걸리는 행이고, 그것이 강의의 $N=1$, $\lambda=0.1$ 줄이다.
> 2. (a) $e_0/\alpha=0.05/1.5\times10^{-4}=333.3$ N. (b) $11u_0+3u_1=-1333.3$, $3u_0+2u_1=-333.3$, 행렬식 $13$이므로 $u_0=-1666.7/13=-128.21$ N, $u_1=333.3/13=25.64$ N이고 $f_z^{\mathrm{tot}}=117.72-128.21=-10.49$ N. (c) 실행 불가능하다. 발이 *당기는* 값이다. 단방향 행이 걸리고 $u_0$는 $-mg=-117.72$ N으로 물리며 $f_z^{\mathrm{tot}}=0$, 디딤발마다 $0$ N이 된다 — QP의 답은 다리에서 하중을 빼고 한 틱 떨어지라는 것이다. (d) 대각선만 바뀌어 $20u_0+3u_1=-1333.3$, $3u_0+11u_1=-333.3$, 행렬식 $211$이므로 $u_0=-13666.7/211=-64.77$ N, $u_1=-2666.7/211=-12.64$ N이다. 이제 $f_z^{\mathrm{tot}}=117.72-64.77=52.95$ N, 곧 발당 $26.47$ N이고 걸리는 행이 없다. 제약이 활성인지를 정한 것은 기하가 아니라 *가중치*다.
> 3. 빈칸: `u_lo, u_hi = -m*g, n_st*fz_max - m*g`, `feas = (u_lo <= free[0] <= u_hi)`, `low = min(low, (m*g + u[0]) / n_st)`, `e, zd = e + dt*zd + alpha*u[0], zd + dt/m*u[0]`. 표는 이렇다. $\lambda=1$에서는 모든 $N$이 첫 틱에 실행 불가능해 $u_0=-117.72$ N을 적용하고 발 하중을 $0$ N까지 빼며, $N=1$은 $0.42$ s, $N=2,4,8$은 $0.18$ s에 정착한다. $\lambda=10$에서는 모든 $N$이 실행 가능하고 $u_0$가 각각 $-30.3,\,-64.8,\,-58.9,\,-60.5$ N, 최저 발당 힘이 $43.7,\,26.5,\,29.4,\,28.6$ N이며, $N=1$은 정착하지 못하고 나머지는 $0.42$, $0.24$, $0.24$ s가 걸린다. **지평은 그 행을 전혀 움직이지 못한다.** 움직이는 것은 가중치이고, 그 물리적 이유가 답이다. 내려오는 속도는 자유 낙하로 묶인다. 발 하중을 완전히 빼도 한 틱에 잃는 높이는 $\tfrac12 g\Delta t^2=17.7$ mm뿐이므로, $50$ mm를 빨리 없애려는 계획은 아무리 멀리 내다봐도 당기는 발을 요구한다. 지평을 늘리는 것은 하강을 어떻게 나누는지를 바꿀 뿐 중력이 일하는 속도를 바꾸지 못하고, 실제로 $N=2$는 $N=1$보다 *더* 요구한다($-64.8$ 대 $-30.3$ N). 이제 받아 내는 것까지 계획할 수 있기 때문이다. $\lambda$를 올리는 것이 통하는 이유는 제어기가 덜 원하게 만들기 때문이고, 이는 플랜트가 더 할 수 있게 만드는 것과 다른 기제다 — 한 손잡이만 조율했다고 보고하는 논문은 제어기의 절반만 말한 것이다.

**P2가 아직 빠져 있는 곳.** 위의 모든 것은 몸통뿐이다. P2를 얹으면 QP는 이름 붙일 수 있는 세
가지로 틀린다. $m$이 $12$가 아니라 $14$ kg이고, $I_B$는 상자의 관성이라 새 무게중심에 대한 팔의
기여가 빠져 있으며, 패널을 누르는 동안 팔이 가하는 반작용 렌치는 단일 강체 모델에 해당 항이 아예
없는 외력이다. QP는 그것을 설명되지 않는 추종 오차로 흡수하고 발 힘으로 맞서 싸운다. "팔 없음,
도구 렌치 없음, P3 벽 없음"의 정직한 독해가 이것이다.

> [!tip]- 이전 판에서 이어 온 주장 읽기 · Claim-reading, kept
> - **주장.** condensed QP의 시간 주장은 1밀리초 미만 풀이와 수십 Hz 재실행이다(초록 20–30 Hz, 실험 25–50 Hz) — 그 시간이 곧 주장이다.
> - **반증.** 피치 $30^\circ$: 버린 인자가 $0.577$과 $1.155$로, 이 페이지가 이미 더는 작지 않다고 한다. 뒷발 들기나 전복이면 충분하다.
> - **과제.** 그 몸통 위 P2가 패널을 누를 때 — 팔 없음, 도구 렌치 없음, P3 벽 없음. 결정 변수는 네 발의 지면 반력이고, 패널 접촉은 QP 밖이다.

### 연결

- 기초: [[02-foundations/optimization|최적화]] · 이전: [[04-robotics/mpc|MPC]]
- 반향: [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] (이중 시스템)

### After reading · 읽고 나면 말할 수 있어야 하는 것

- [ ] Solve Q's $N=2$ condensed QP by hand and name which rows came out slack · Q의 $N=2$ condensed QP를 손으로 풀고 어느 행이 여유로 나왔는지 댈 수 있다
- [ ] Say where a longer horizon stops paying on the sweep, and what $\lambda$ trades for what · 스윕에서 지평이 언제부터 값을 못 하는지, $\lambda$가 무엇과 무엇을 맞바꾸는지 말할 수 있다
- [ ] Say what the single-rigid-body approximation throws away and what it buys (convexity) · 단일 강체 근사가 버리는 것과 사는 것(볼록성)을 말할 수 있다
- [ ] Describe the setup in which ground reaction forces are the decision variables and friction cones the constraints · 지면 반력 + 마찰 원뿔이 결정 변수·제약이 되는 구성을 말할 수 있다
- [ ] Explain the division of labor in the slow-MPC + fast-WBC two-level stack · 느린 MPC + 빠른 WBC 2단 스택의 분업을 말할 수 있다
- [ ] State the modeling craft this case teaches: choose the approximation that makes the problem convex · 이 사례가 가르치는 모델링 기술(볼록하게 만드는 근사 선택)을 말할 수 있다
