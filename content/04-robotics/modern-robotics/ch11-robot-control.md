---
title: "MR Ch.11 — Robot Control"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.11** — [[04-robotics/modern-robotics-book|book guide & free PDF]] · continues into [[04-robotics/lqr-lqg|LQR]] → [[04-robotics/mpc|MPC]]

> [!note] Prerequisites · 선수 지식
> You need the equation of motion from [[04-robotics/modern-robotics/ch08-dynamics|ch.8]] and second-order error dynamics ($\zeta, \omega_n$) from [[02-foundations/engineering-math|0.5 §8]]; [[04-robotics/control-theory-ce397|5. Control Theory]] develops the same ideas in state-space form.
> [[04-robotics/modern-robotics/ch08-dynamics|8장]]의 운동 방정식과 [[02-foundations/engineering-math|0.5 §8]]의 오차 미분방정식($\zeta, \omega_n$)이 필요하다; [[04-robotics/control-theory-ce397|5. 제어 이론]]이 같은 내용을 상태공간으로 전개한다.

## English

**Core question**: how do we make the robot actually follow the trajectory?

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at the catalog pose $\theta = (0^\circ, 90^\circ)$, standing in the vertical plane, with the three numbers the previous chapter produced there:

$$M = \begin{pmatrix}3&1\\1&1\end{pmatrix}\ \mathrm{kg\,m^2}, \qquad g = (19.62,\ 0)\ \mathrm{N\,m}, \qquad J = \begin{pmatrix}-1&-1\\1&0\end{pmatrix}$$

All three are properties of *this* configuration and not of the arm, so every gain conclusion below is tied to one pose and none of it survives a move unexamined. Also $c = 0$ whenever the arm is at rest, and the catalog's operational-space inertia $\Lambda = (JM^{-1}J^\top)^{-1} = \mathrm{diag}(1,2)$ for the one task-space calculation at the end. Gains on this page are $K_p = 100$ and $K_d = 20$ unless a line says otherwise, and the desired state is the pose itself: $\theta_d$ constant, $\dot\theta_d = \ddot\theta_d = 0$, error $e = \theta_d - \theta$.

*Scope: this page teaches setpoint regulation at one pose — what the controller must multiply by, and what happens when it does not. It does not teach trajectory tracking through a changing $M(\theta)$, contact force control ([[04-robotics/force-compliance-control|13. Force & Compliance Control]]), or optimal feedback ([[04-robotics/lqr-lqg|LQR]]).*

### Homework diagram · 과제가 그릴 그림

One signal-flow drawing with a small picture of the arm attached to it. Draw it left to right in three columns.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="three columns: P2 at the catalog pose with the shoulder 0.1 rad behind the command; PD with gravity compensation above computed torque, fed the same error; the plant with the off-diagonal cells of M inverse shaded. PD gives accelerations (5, −5) with the elbow circled, computed torque (10, 0)">
  <g transform="translate(0 3)">
    <defs><marker id="ar11e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
    <g fill="currentColor" font-weight="bold"><text x="10" y="18" font-size="11.5">1 · the error</text><text x="150" y="18" font-size="11.5">2 · two controllers, one error</text><text x="426" y="18" font-size="11.5">3 · the plant</text></g>
    <line x1="12" y1="40" x2="30" y2="40" stroke="currentColor" stroke-width="2" stroke-dasharray="5 3" opacity="0.75"/>
    <line x1="12" y1="56" x2="30" y2="56" stroke="currentColor" stroke-width="3"/>
    <g fill="currentColor"><text x="35" y="44" font-size="11">commanded</text><text x="35" y="60" font-size="11">actual</text></g>
    <g stroke="currentColor" stroke-width="2" stroke-dasharray="5 3" fill="none" opacity="0.75"><polyline points="22,218 114,218 114,126"/></g>
    <g stroke="currentColor" stroke-width="3" fill="none" stroke-linejoin="round"><polyline points="22,218 113.5,227.2 122.7,135.6"/></g>
    <polygon points="22,218 14,230 30,230" fill="none" stroke="currentColor" stroke-width="1.1"/>
    <circle cx="22" cy="218" r="3.6" fill="currentColor"/>
    <circle cx="113.5" cy="227.2" r="3.4" fill="currentColor"/>
    <circle cx="114" cy="218" r="3.2" fill="none" stroke="currentColor" stroke-width="1.1"/>
    <circle cx="122.7" cy="135.6" r="3.4" fill="currentColor"/>
    <circle cx="114" cy="126" r="3.4" fill="none" stroke="currentColor" stroke-width="1.2"/>
    <line x1="114" y1="126" x2="122.7" y2="135.6" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 1.5"/>
    <text x="106" y="124" font-size="11" text-anchor="end" fill="currentColor">tip gap 0.14 m</text>
    <g fill="currentColor">
    <text x="12" y="256" font-size="11" font-weight="bold">e = (0.1, 0) rad</text>
    <text x="12" y="271" font-size="11">shoulder back 0.1 rad</text>
    <text x="12" y="285" font-size="11">= 5.73°; elbow exact</text>
    </g>
    <text x="150" y="48" font-size="11.5" fill="currentColor" font-weight="bold">PD + gravity compensation</text>
    <g fill="currentColor"><text x="150" y="84" font-size="11.5">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="150" y="112" font-size="11.5">e<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text></g>
    <text x="190" y="65" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.85">K<tspan dy="3.1" font-size="8.6">p</tspan><tspan dy="-3.1">e + K</tspan><tspan dy="3.1" font-size="8.6">d</tspan><tspan dy="-3.1">ė</tspan></text>
    <g stroke="currentColor" stroke-width="1.1" fill="none"><line x1="170" y1="71" x2="170" y2="89"/><line x1="210" y1="71" x2="210" y2="89"/><polyline points="170,75 175,75 178,71 182.4,79 186.8,71 191.2,79 195.6,71 200,79 204,75 210,75" fill="none"/><line x1="170" y1="85" x2="184" y2="85"/><path d="M182 81 L196 81 M182 89 L196 89 M182 81 L182 89" fill="none"/><line x1="189" y1="82.5" x2="189" y2="87.5"/><line x1="189" y1="85" x2="210" y2="85"/><line x1="170" y1="99" x2="170" y2="117"/><line x1="210" y1="99" x2="210" y2="117"/><polyline points="170,103 175,103 178,99 182.4,107 186.8,99 191.2,107 195.6,99 200,107 204,103 210,103" fill="none"/><line x1="170" y1="113" x2="184" y2="113"/><path d="M182 109 L196 109 M182 117 L196 117 M182 109 L182 117" fill="none"/><line x1="189" y1="110.5" x2="189" y2="115.5"/><line x1="189" y1="113" x2="210" y2="113"/></g>
    <g stroke="currentColor" stroke-width="1.2"><line x1="164" y1="80" x2="170" y2="80"/><line x1="164" y1="108" x2="170" y2="108"/></g>
    <text x="150" y="168" font-size="11.5" fill="currentColor" font-weight="bold">computed torque</text>
    <g fill="currentColor"><text x="150" y="204" font-size="11.5">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="150" y="232" font-size="11.5">e<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text></g>
    <text x="190" y="185" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.85">K<tspan dy="3.1" font-size="8.6">p</tspan><tspan dy="-3.1">e + K</tspan><tspan dy="3.1" font-size="8.6">d</tspan><tspan dy="-3.1">ė</tspan></text>
    <g stroke="currentColor" stroke-width="1.1" fill="none"><line x1="170" y1="191" x2="170" y2="209"/><line x1="210" y1="191" x2="210" y2="209"/><polyline points="170,195 175,195 178,191 182.4,199 186.8,191 191.2,199 195.6,191 200,199 204,195 210,195" fill="none"/><line x1="170" y1="205" x2="184" y2="205"/><path d="M182 201 L196 201 M182 209 L196 209 M182 201 L182 209" fill="none"/><line x1="189" y1="202.5" x2="189" y2="207.5"/><line x1="189" y1="205" x2="210" y2="205"/><line x1="170" y1="219" x2="170" y2="237"/><line x1="210" y1="219" x2="210" y2="237"/><polyline points="170,223 175,223 178,219 182.4,227 186.8,219 191.2,227 195.6,219 200,227 204,223 210,223" fill="none"/><line x1="170" y1="233" x2="184" y2="233"/><path d="M182 229 L196 229 M182 237 L196 237 M182 229 L182 237" fill="none"/><line x1="189" y1="230.5" x2="189" y2="235.5"/><line x1="189" y1="233" x2="210" y2="233"/></g>
    <g stroke="currentColor" stroke-width="1.2"><line x1="164" y1="200" x2="170" y2="200"/><line x1="164" y1="228" x2="170" y2="228"/></g>
    <rect x="232" y="66" width="32" height="56" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>
    <g stroke="currentColor" stroke-width="1.2"><line x1="210" y1="80" x2="264" y2="80"/><line x1="210" y1="108" x2="264" y2="108"/></g>
    <text x="248" y="98" font-size="11.5" text-anchor="middle" fill="currentColor">+ g</text>
    <g stroke="currentColor" stroke-width="1.2" marker-end="url(#ar11e)"><line x1="264" y1="80" x2="425" y2="80"/><line x1="264" y1="108" x2="425" y2="108"/></g>
    <text x="345" y="74" font-size="11" text-anchor="middle" fill="currentColor">τ = (29.62, 0)</text>
    <rect x="222" y="186" width="40" height="56" fill="none" stroke="currentColor" stroke-width="1.4" rx="3"/>
    <g stroke="currentColor" stroke-width="1.2"><line x1="210" y1="200" x2="222" y2="200"/><line x1="210" y1="228" x2="222" y2="228"/></g>
    <g stroke="currentColor" stroke-width="1" opacity="0.75"><line x1="222" y1="200" x2="262" y2="200"/><line x1="222" y1="228" x2="262" y2="228"/><line x1="222" y1="200" x2="262" y2="228"/><line x1="222" y1="228" x2="262" y2="200"/></g>
    <text x="242" y="182" font-size="11.5" text-anchor="middle" fill="currentColor">M(θ)</text>
    <rect x="270" y="186" width="26" height="56" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>
    <text x="283" y="218" font-size="11.5" text-anchor="middle" fill="currentColor">+ c</text>
    <rect x="302" y="186" width="26" height="56" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>
    <text x="315" y="218" font-size="11.5" text-anchor="middle" fill="currentColor">+ g</text>
    <g stroke="currentColor" stroke-width="1.2"><line x1="262" y1="200" x2="270" y2="200"/><line x1="262" y1="228" x2="270" y2="228"/><line x1="296" y1="200" x2="302" y2="200"/><line x1="296" y1="228" x2="302" y2="228"/></g>
    <g stroke="currentColor" stroke-width="1.2" marker-end="url(#ar11e)"><line x1="328" y1="200" x2="425" y2="200"/><line x1="328" y1="228" x2="425" y2="228"/></g>
    <text x="377" y="194" font-size="11" text-anchor="middle" fill="currentColor">τ = (49.62, 10)</text>
    <text x="150" y="140" font-size="12" fill="currentColor">θ = (</text><circle cx="151.6" cy="129.7" r="0.9" fill="currentColor"/><circle cx="154.7" cy="129.7" r="0.9" fill="currentColor"/>
    <text x="178.1" y="140" font-size="12" text-anchor="middle" fill="currentColor">5</text>
    <text x="182.1" y="140" font-size="12" fill="currentColor">,</text>
    <text x="201.4" y="140" font-size="12" text-anchor="middle" fill="currentColor">−5</text>
    <text x="212.9" y="140" font-size="12" fill="currentColor">) rad/s²</text>
    <ellipse cx="201.4" cy="136" rx="12" ry="10" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <text x="268" y="140" font-size="11" fill="currentColor" opacity="0.85">← elbow: e<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 0, τ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 0</tspan></text>
    <text x="150" y="260" font-size="12" fill="currentColor">θ = (</text><circle cx="151.6" cy="249.7" r="0.9" fill="currentColor"/><circle cx="154.7" cy="249.7" r="0.9" fill="currentColor"/>
    <text x="181.6" y="260" font-size="12" text-anchor="middle" fill="currentColor">10</text>
    <text x="189" y="260" font-size="12" fill="currentColor">,</text>
    <text x="199.4" y="260" font-size="12" text-anchor="middle" fill="currentColor">0</text>
    <text x="203.9" y="260" font-size="12" fill="currentColor">) rad/s²</text>
    <rect x="426" y="58" width="122" height="190" fill="none" stroke="currentColor" stroke-width="1.4" rx="4"/>
    <text x="435" y="80" font-size="11.5" fill="currentColor">θ = M<tspan dy="-4.4" font-size="9">−1</tspan><tspan dy="4.4">(τ − c − g)</tspan></text><circle cx="436.5" cy="70.1" r="0.9" fill="currentColor"/><circle cx="439.5" cy="70.1" r="0.9" fill="currentColor"/>
    <text x="435" y="96" font-size="11" fill="currentColor" opacity="0.8">at rest: c = 0</text>
    <text x="449" y="117" font-size="11.5" fill="currentColor">M<tspan dy="-4.4" font-size="9">−1</tspan><tspan dy="4.4" dx="3.4">=</tspan></text>
    <rect x="449" y="124" width="38" height="26" fill="currentColor" fill-opacity="0" stroke="currentColor" stroke-width="1.2"/>
    <text x="468" y="141.5" font-size="12" text-anchor="middle" fill="currentColor">0.5</text>
    <rect x="487" y="124" width="38" height="26" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2"/>
    <text x="506" y="141.5" font-size="12" text-anchor="middle" fill="currentColor" font-weight="bold">−0.5</text>
    <rect x="449" y="150" width="38" height="26" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2"/>
    <text x="468" y="167.5" font-size="12" text-anchor="middle" fill="currentColor" font-weight="bold">−0.5</text>
    <rect x="487" y="150" width="38" height="26" fill="currentColor" fill-opacity="0" stroke="currentColor" stroke-width="1.2"/>
    <text x="506" y="167.5" font-size="12" text-anchor="middle" fill="currentColor">1.5</text>
    <text x="435" y="196" font-size="11" fill="currentColor" opacity="0.85">shaded: a push on one</text>
    <text x="435" y="210" font-size="11" fill="currentColor" opacity="0.85">joint moves the other</text>
  </g>
</svg>

1. **Left — the error, as geometry.** P2 at the catalog pose twice: the commanded arm dashed, and the actual arm solid with the **shoulder** rotated back by $e_1 = 0.1\,\mathrm{rad} = 5.73^\circ$ while the elbow angle is unchanged. Mark both tips and the gap between them. One joint is wrong and the other is exactly right — hold on to that, because it is what the rest of the figure is about.
2. **Middle — two controllers, stacked, sharing that one error.** The upper path is joint-space PD with gravity compensation: draw a spring and a damper on each joint *separately*, with no line crossing between the two joints, then a box adding $g$. The absence of a crossing line is not laziness in the drawing; it is the controller's assumption. The lower path is computed torque: the same $K_pe + K_d\dot e$ signal, but routed through a box labelled $M(\theta)$ that has both joints' wires entering and both leaving, then boxes adding $c$ and $g$.
3. **Right — the plant, drawn as the thing that couples.** One box, $\ddot\theta = M^{-1}(\tau - c - g)$, with $M^{-1}$ sketched as a $2\times2$ grid and the two off-diagonal cells shaded. Shade them heavily. Every surprise on this page comes out of those two cells.

Under each of the two paths write the accelerations it actually produces for the error in column 1 — $(5,\ -5)\,\mathrm{rad/s^2}$ for PD, $(10,\ 0)$ for computed torque — and circle the elbow entry in the PD row, the joint that had no error and no commanded torque.

The problem set asks for this same three-column figure with the error moved to the elbow.

### Worked case · 대상으로 한 번 끝까지

One state, two controllers, all numbers exact. The arm is at rest at the catalog pose, the shoulder is $0.1\,\mathrm{rad}$ away from where it should be, and the elbow is perfect: $e = (0.1,\ 0)\,\mathrm{rad}$, $\dot e = 0$, $\ddot\theta_d = 0$. At rest $c = 0$ ([[04-robotics/modern-robotics/ch08-dynamics|ch.8]]), so the plant is $\ddot\theta = M^{-1}(\tau - g)$ and only two terms are in play.

**Step 1 — computed torque, evaluated.** The law is $\tau = M(\theta)(\ddot\theta_d + K_pe + K_d\dot e) + c + g$. The bracket is $K_pe = (10,\ 0)\,\mathrm{rad/s^2}$, a *desired acceleration*, and $M$ converts it into the torque that actually delivers it:

$$\tau = \begin{pmatrix}3&1\\1&1\end{pmatrix}\begin{pmatrix}10\\0\end{pmatrix} + \begin{pmatrix}19.62\\0\end{pmatrix} = \begin{pmatrix}30\\10\end{pmatrix} + \begin{pmatrix}19.62\\0\end{pmatrix} = \begin{pmatrix}49.62\\10\end{pmatrix}\ \mathrm{N\,m}$$

and note the second entry: the controller sends $10\,\mathrm{N\,m}$ to the **elbow**, a joint with zero error, because accelerating the shoulder would otherwise drag the elbow along with it. That entry is $M_{21}$ doing its job.

**Step 2 — what the plant does with it.** Substituting into $\ddot\theta = M^{-1}(\tau - g)$, the $M$ and $M^{-1}$ cancel exactly:

$$\ddot\theta = M^{-1}\bigl(M(K_pe) + g - g\bigr) = K_pe = (10,\ 0)\ \mathrm{rad/s^2}$$

so the shoulder accelerates at exactly the commanded rate and the elbow does not move at all. Since $e = \theta_d - \theta$ with $\theta_d$ constant, $\ddot e = -\ddot\theta$, and the error obeys $\ddot e + K_p e = 0$ joint by joint — check it: $-10 + 100(0.1) = 0$. With $K_d$ switched on the same cancellation leaves $\ddot e + K_d\dot e + K_pe = 0$, giving $\omega_n = \sqrt{K_p} = 10\,\mathrm{rad/s}$, $\zeta = K_d/(2\sqrt{K_p}) = 1$, and a $2\,\%$ settling estimate of $4/(\zeta\omega_n) = 0.4\,\mathrm{s}$ — **the same pair of numbers for both joints**, which is the whole prize.

**Step 3 — the same error, PD with gravity compensation.** Now drop the $M$ and send $\tau = K_pe + K_d\dot e + g = (10,\ 0) + (19.62,\ 0) = (29.62,\ 0)\,\mathrm{N\,m}$. The elbow gets nothing, because it asked for nothing. The plant disagrees:

$$\ddot\theta = M^{-1}\begin{pmatrix}10\\0\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}\begin{pmatrix}10\\0\end{pmatrix} = \begin{pmatrix}5\\-5\end{pmatrix}\ \mathrm{rad/s^2}$$

Two things went wrong at once, and they are the two cells of $M^{-1}$. The shoulder got **half** the acceleration it asked for, because $(M^{-1})_{11} = 0.5$, not $1$. And the elbow, with zero error and zero commanded torque, is accelerating at $-5\,\mathrm{rad/s^2}$, because $(M^{-1})_{21} = -0.5$. There is no bug and no disturbance; the arm is simply one body, and pushing one end of it moves the other.

**Step 4 — what that does to the error dynamics, as poles.** With gravity cancelled and $c = 0$, PD control gives $M\ddot e + K_d\dot e + K_pe = 0$, i.e. $\ddot e + K_dM^{-1}\dot e + K_pM^{-1}e = 0$. Both matrix coefficients are the *same* matrix $M^{-1}$ times a scalar, so the system decouples in the eigenvectors of $M$ — not in the joints. With $\mu$ an eigenvalue of $M^{-1}$, each mode obeys $\ddot e_i + K_d\mu_i\dot e_i + K_p\mu_ie_i = 0$, so

$$\omega_{n,i} = \sqrt{K_p\mu_i}, \qquad \zeta_i = \frac{K_d\mu_i}{2\sqrt{K_p\mu_i}} = \frac{K_d\sqrt{\mu_i}}{2\sqrt{K_p}} = \sqrt{\mu_i}$$

the last equality holding because this page's $K_d = 2\sqrt{K_p}$. Since $M$'s eigenvalues are $2 \pm \sqrt2$, those of $M^{-1}$ are $\mu = (2 \mp \sqrt2)/2 = 0.2929$ and $1.7071$, and the two modes come out as

| mode | direction | $\mu$ | $\omega_n$ | $\zeta$ | $4/(\zeta\omega_n)$ | overshoot |
|---|---|---:|---:|---:|---:|---:|
| heavy | $(0.924,\ 0.383)$, mostly shoulder | $0.2929$ | $5.412$ | $0.5412$ | $1.366\,\mathrm{s}$ | $13.2\,\%$ |
| light | $(0.383,\ -0.924)$, elbow counter-rotating | $1.7071$ | $13.066$ | $1.3066$ | $0.234\,\mathrm{s}$ | none |

One pair of gains, and the arm answers with two natural frequencies a factor of $2.4$ apart and two damping ratios straddling $1$: the heavy direction rings and takes $1.37\,\mathrm{s}$ to settle, the light one is overdamped and sluggish in its own way at $0.66\,\mathrm{s}$, set by its slower pole $-\zeta\omega_n + \omega_n\sqrt{\zeta^2-1} = -6.08\,\mathrm{rad/s}$ (the table's $4/(\zeta\omega_n)$ holds only for $\zeta \le 1$). Neither is the $\zeta = 1$, $0.4\,\mathrm{s}$ response that was designed. **Choosing $K_d = 2\sqrt{K_p}$ buys critical damping only if the inertia is $1$.** Computed torque makes it $1$ by dividing it out first; that is the only difference between steps 2 and 3.

**Step 5 — the same physics at the tip.** The catalog's $\Lambda = \mathrm{diag}(1,2)$ says a task-space controller asking for a tip acceleration $a$ must apply the wrench $F = \Lambda a$, and $\tau = J^\top F$ turns that into joint torques ([[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5 §3]]). For $a = (1,1)\,\mathrm{m/s^2}$: $F = (1,\ 2)\,\mathrm{N}$ — twice as much force for the same acceleration in $y$ as in $x$, which is what "the tip feels twice as heavy in $y$" means — and $\tau = J^\top F = (1,\ -1)\,\mathrm{N\,m}$. The structure is identical to step 1 with $\Lambda$ in place of $M$ and $J^\top$ bolted on, which is why operational-space control is a re-coordinatization of this chapter rather than a new idea.

### 1. Error dynamics and the two input regimes

- **Error dynamics thinking**: design the controller so the *error* obeys a stable
  differential equation ([[02-foundations/engineering-math|0.5 §8]]) — e.g.,
  $\ddot e + K_d \dot e + K_p e = 0$ with gains picking damping/frequency.
- **Velocity-input regime (MR §11.3): P and PI swap the roles you expect.**
  - **P alone** gives *first-order* error dynamics, $\dot\theta_e + K_p\theta_e = c$. Here $c$
    is zero for a setpoint and nonzero for a constant-velocity target; that nonzero $c$ leaves the
    steady-state offset $c/K_p$.
  - **Adding I** removes the offset. Differentiating once shows the cost:
    $\ddot\theta_e + K_p\dot\theta_e + K_i\theta_e = 0$. **PI in this same section is second
    order**, with $\omega_n=\sqrt{K_i}$ and $\zeta = K_p/(2\sqrt{K_i})$.
  - **Read the roles off those two expressions**: under velocity inputs $K_p$ is the *damping*
    and $K_i$ is the stiffness.
  - **Warning**: I also brings windup — hence anti-windup wherever the actuator can saturate.
- **Torque-input regime (MR §11.4): $K_p$ is the spring, $K_d$ the damper.**
  - With unit inertia, PD gives $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$, so
    $\omega_n=\sqrt{K_p}$ and $\zeta = K_d/(2\sqrt{K_p})$ — the opposite of the velocity-input
    roles. The same symbol does a different job in each regime, which is why gains do not
    transfer between them.
  - PID goes one order further still: its setpoint error dynamics are *third* order.

> [!example] Worked example · 계산 예제
> Torque-input PD with unit inertia: $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$, pick $K_p = 100$.
> - $\omega_n = \sqrt{K_p} = 10$ rad/s.
> - Critical damping: $K_d = 2\sqrt{K_p} = 20$, so $\zeta = 1$.
> - 2% settling time $\approx 4/(\zeta\omega_n) = 4/10 = 0.4$ s (MR §11.3 gives settling $\approx 4t$ with time constant $t = 1/(\zeta\omega_n)$).
> - Now halve the damper, $K_d = 10$: $\zeta = 10/(2\cdot 10) = 0.5$.
> - Overshoot $= e^{-\pi\zeta/\sqrt{1-\zeta^2}} \approx 16\%$ (MR lists 16% for $\zeta = 0.5$), and settling $\approx 4/(0.5\cdot 10) = 0.8$ s.
> - Halving $K_d$ bought no speed: $\zeta\omega_n$ halved, so settling doubled and the error now overshoots.

Every line of that callout assumes the inertia is $1$. Step 4 of the worked case is what the same gains do when it is $M$ instead, and the answer is two different responses from one design.

### 2. Computed torque, defined

**Computed torque** (equivalently the inverse-dynamics controller, or feedback linearization applied to a manipulator) is a control law that uses a model of the plant's own dynamics to cancel them, so that what is left to stabilize is a *linear, decoupled* error system. It is not a gain-tuning trick and it is not "PD plus a gravity term": it has three defining parts, and dropping any one of them breaks the property it exists for.

1. a **feedforward acceleration** $\ddot\theta_d$, the acceleration the trajectory itself calls for;
2. a **feedback acceleration** $K_pe + K_d\dot e$, in the same units as the first — this is the part that is *not* a torque;
3. a **model multiplication and offset**: the sum of 1 and 2 is multiplied by $\hat M(\theta)$ and the modelled $\hat c$ and $\hat g$ are added, converting a desired acceleration into the torque that produces it.

$$\tau = \hat M(\theta)\bigl(\ddot\theta_d + K_pe + K_d\dot e\bigr) + \hat c(\theta,\dot\theta) + \hat g(\theta)$$

where $\hat M, \hat c, \hat g$ are the *modelled* mass matrix, velocity-product and gravity terms ([[04-robotics/modern-robotics/ch08-dynamics|ch.8]]), $e = \theta_d - \theta$, and $K_p, K_d$ are gain matrices, conventionally $k_pI$ and $k_dI$. Substituting into the true plant $M\ddot\theta = \tau - c - g$ and setting $\hat M = M$, $\hat c = c$, $\hat g = g$ leaves $\ddot e + K_d\dot e + K_pe = 0$ exactly, with no $M$ anywhere, because the modelled $\hat M$ on the way in cancels the real $M^{-1}$ on the way out. That cancellation is why the gains now mean what a textbook second-order system says they mean.

- **Example**: step 1 of the worked case. $K_pe = (10,0)$ is a desired acceleration; $M(K_pe) = (30,10)$ is the torque that delivers it; the $10\,\mathrm{N\,m}$ at the zero-error elbow is condition 3 paying for the coupling, and the plant returns $\ddot\theta = (10,0)$ exactly.
- **Non-example**: PD with gravity compensation, $\tau = K_pe + K_d\dot e + \hat g(\theta)$ — the approximation MR offers when the full model is too slow or too uncertain to evaluate. It has parts 1 (trivially) and 2 and *half* of part 3, and it is a perfectly good controller; it is simply not computed torque, because $M$ was never applied. Step 3 measures the difference on P2: $(5,-5)$ instead of $(10,0)$ from the identical error.
- **Why it matters, and where it stops**: the cancellation is only as good as $\hat M, \hat c, \hat g$. When the model is wrong, the residual $\ (\hat M - M)\ddot\theta + (\hat c - c) + (\hat g - g)$ does not vanish — it enters the error dynamics as a disturbance the PD gains have to absorb, and both tracking and stability margin degrade as it grows. That is the precise sense in which model-based control is "only as good as its model", and it is the reason the rest of the track keeps adding layers that need less of one.

### 3. Contact, and where control goes after this chapter

**Worked: P2 under a $10\,\mathrm{N}$ contact, PD versus inverse dynamics.** Catalog pose, $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ ([[02-foundations/lab-plants|0.6]]). A panel pushes the tip with $F=(0,-10)\,\mathrm{N}$ (the robot pressing down). Duality gives $\tau=J^\top F=(-10,0)\,\mathrm{N{\cdot}m}$ — the shoulder carries the load, the elbow does not, because the forearm is vertical. Inverse dynamics can add that $J^\top F$ (and $g$) and hold with $e=0$. Joint-space PD cannot: if gravity is already cancelled and the only restoring torque is $K_p e$ with a deliberately soft $K_p=10\,\mathrm{N{\cdot}m/rad}$ on each joint — a tenth of this page's usual gain, chosen so the sag comes out a round number — the linear map predicts $e_1\approx 10/10=1\,\mathrm{rad}$ of sag at the shoulder. That $O(1)$ radian is the lecture saying the linear spring is the wrong object for a $10\,\mathrm{N}$ contact. PD turns contact into position error times stiffness; a stiff PD on a stiff panel makes huge force from a millimetre. Impedance, next page, commands the *relationship* instead.

**Force and impedance control**: when contact matters, control the *relationship* between
motion and force (virtual spring-damper; full treatment in [[04-robotics/force-compliance-control|13. Force & Compliance Control]]) rather than position alone — the entry point to
contact-rich manipulation.

The modern continuation: optimal feedback ([[04-robotics/lqr-lqg|LQR]]) → constraints
([[04-robotics/mpc|MPC]]) → learned policies ([[02-foundations/rl-basics|RL]],
[[01-canonical-papers/notes/4-vla/pi0|VLA]]) — each layer absorbing more of the modeling burden.

**Wiki connections**: VLA outputs ultimately pass through platform-specific position,
velocity, torque, or impedance interfaces and their low-level loops. Contact safety depends
on that whole stack — actuators, limits, passive compliance, speed, task setup, and control —
not on impedance control alone.

### Self-check

1. In $\ddot e + K_d\dot e + K_p e = 0$, what relation between $K_d$ and $K_p$ gives critical damping?
2. What does "computed torque is only as good as the model" mean concretely — what is left when $M, c, g$ are wrong?
3. Name two situations where impedance control beats position control.
4. On P2 at the catalog pose, PD with gravity compensation and $K_p = 100$, $K_d = 20$ produced $\zeta = 0.541$ on one mode and $1.307$ on the other. Without recomputing the eigenvectors, say what would have to be true of the arm for both to equal $1$, and why computed torque gets there without it.

> [!tip]- Answers
> 1. Matching $\ddot e + 2\zeta\omega_n\dot e + \omega_n^2 e = 0$ gives $\omega_n^2 = K_p$ and $2\zeta\omega_n = K_d$, so $\zeta = 1 \iff K_d = 2\sqrt{K_p}$ ([[02-foundations/engineering-math|0.5 §8]]).
> 2. The cancellation is incomplete, so residual nonlinear terms remain inside the error dynamics — they act as a disturbance the PD gains must suppress. The error dynamics are no longer exactly linear, and both tracking performance and stability margin degrade as model error grows.
> 3. Contact tasks (polishing, insertion — where a small position error against a stiff surface produces a huge force) and human collaboration (compliance so a collision is survivable). Both are cases where the *force–motion relationship* matters more than positional accuracy.
> 4. Since $\zeta_i = K_d\sqrt{\mu_i}/(2\sqrt{K_p})$ with $\mu_i$ the eigenvalues of $M^{-1}$, both damping ratios equal $1$ only when $M$ has a single repeated eigenvalue equal to $1$ — that is, when $M = I$, an arm whose inertia is $1$ in every direction and at every pose. P2 is not that arm, and no serial manipulator with revolute joints is. Computed torque multiplies by $M(\theta)$ before the gains ever see the plant, so the error system it leaves behind genuinely has inertia $1$ in every direction, and the single designed $\zeta$ applies to both joints.

### Problem set · 과제

Tier B. Same plant **P2** at the same catalog pose from [[02-foundations/lab-plants|0.6]], same gains $K_p = 100$, $K_d = 20$, same rest condition — but the error has moved to the other joint: $e = (0,\ 0.1)\,\mathrm{rad}$, $\dot e = 0$, $\ddot\theta_d = 0$. The shoulder is now the joint that is exactly right. No simulator.

1. **Draw.** The three-column figure above with the elbow displaced instead of the shoulder, both off-diagonal cells of $M^{-1}$ shaded, and the two resulting acceleration pairs written under the two controller paths. Circle the joint in the PD row that has zero error and zero commanded torque and is moving anyway.
2. **Derive.** (a) The computed-torque $\tau$ and the $\ddot\theta$ it produces. (b) The PD-with-gravity-compensation $\tau$ and the $\ddot\theta$ it produces. (c) The tip accelerations $\ddot p = J\ddot\theta$ for both — and say which component the two controllers agree on. (d) State the two modal $\zeta$ values for this error without recomputing them, and justify the answer in one sentence.
3. **Interpret.** In the worked case the coupling *shrank* the commanded acceleration, $5$ instead of $10$. Here it *grows* it. Explain both outcomes from the entries of $M^{-1}$, and say what that implies about the common practice of tuning a manipulator's gains one joint at a time with the other joints held.

> [!tip]- Solutions
> 1. Same figure, shoulder and elbow roles exchanged. PD row: $\ddot\theta = (-5,\ 15)$, with the **shoulder** circled. Computed-torque row: $\ddot\theta = (0,\ 10)$.
> 2. (a) $K_pe = (0,10)$, so $\tau = M(0,10)^\top + g = (10,10) + (19.62,0) = (29.62,\ 10)\,\mathrm{N\,m}$ and $\ddot\theta = K_pe = (0,\ 10)\,\mathrm{rad/s^2}$ — elbow only, as commanded. (b) $\tau = K_pe + g = (19.62,\ 10)\,\mathrm{N\,m}$, and $\ddot\theta = M^{-1}(0,10)^\top = (-5,\ 15)\,\mathrm{rad/s^2}$. (c) $J(0,10)^\top = (-10,\ 0)\,\mathrm{m/s^2}$ and $J(-5,15)^\top = (-10,\ -5)\,\mathrm{m/s^2}$: the two controllers agree exactly on the tip's $x$-acceleration and disagree entirely on $y$. The first row of $J$ at this pose is $(-1,-1)$, so $\ddot p_x = -(\ddot\theta_1 + \ddot\theta_2)$, and the second column of $M^{-1}$ sums to $-0.5 + 1.5 = 1$, so an elbow-only torque of $10\,\mathrm{N\,m}$ redistributes into joint accelerations whose *total* is still $10$ — the coupling moves acceleration between the joints without changing the sum this row reads. The second row of $J$ is $(1,0)$, so $\ddot p_y = \ddot\theta_1$ and reports the shoulder's spurious $-5\,\mathrm{rad/s^2}$ undiluted. The same modelling error is invisible in one task direction and fully visible in the other, which is why a task-space check has to look at both. (d) Unchanged: $\zeta = 0.541$ and $1.307$. The error dynamics $M\ddot e + K_d\dot e + K_pe = 0$ are homogeneous and linear, so $e$ is an initial condition, not a parameter — moving the error to a different joint changes how much of each mode is excited, never where the poles are.
> 3. $M^{-1} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}$. A shoulder-only torque is scaled by $(M^{-1})_{11} = 0.5$ and shrinks; an elbow-only torque is scaled by $(M^{-1})_{22} = 1.5$ and grows; and the shared off-diagonal $-0.5$ pushes the *other* joint backwards in both cases. Tuning one joint at a time therefore measures $(M^{-1})_{ii}$ at one pose — a number that is neither $1$ nor constant across the workspace — and never measures $(M^{-1})_{ij}$ at all, so the cross-coupling is invisible to the whole tuning procedure and shows up only when both joints move together.

## 한국어

**핵심 질문**: 로봇이 궤적을 실제로 따르게 만드는 방법은?

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그 자세 $\theta = (0^\circ, 90^\circ)$로 연직 평면에 서 있고, 앞 장이 거기서 만들어 낸 숫자 셋을 가지고 온다:

$$M = \begin{pmatrix}3&1\\1&1\end{pmatrix}\ \mathrm{kg\,m^2}, \qquad g = (19.62,\ 0)\ \mathrm{N\,m}, \qquad J = \begin{pmatrix}-1&-1\\1&0\end{pmatrix}$$

셋 다 팔이 아니라 *이* 자세의 성질이므로, 아래의 모든 이득 결론은 한 자세에 묶여 있고 자세가 바뀌면 그대로 살아남지 않는다. 그리고 팔이 정지해 있으면 $c = 0$이다. 마지막의 작업 공간 계산 하나를 위해 카탈로그의 작업 공간 관성 $\Lambda = (JM^{-1}J^\top)^{-1} = \mathrm{diag}(1,2)$도 쓴다. 이 페이지의 이득은 따로 말하지 않는 한 $K_p = 100$, $K_d = 20$이고, 목표 상태는 그 자세 자체다. $\theta_d$가 상수, $\dot\theta_d = \ddot\theta_d = 0$, 오차는 $e = \theta_d - \theta$.

*범위: 이 페이지는 한 자세에서의 설정점 제어를 가르친다. 제어기가 무엇을 곱해야 하는지, 곱하지 않으면 무슨 일이 일어나는지다. $M(\theta)$가 변하는 궤적 추종, 접촉 힘 제어([[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]), 최적 피드백([[04-robotics/lqr-lqg|LQR]])은 가르치지 않는다.*

### 과제가 그릴 그림 · Homework diagram

신호 흐름도 하나에 팔 그림을 작게 붙인다. 왼쪽에서 오른쪽으로 세 열이다.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="세 열: 명령보다 어깨가 0.1 rad 뒤진 카탈로그 자세의 P2, 같은 오차를 받는 중력 보상 PD와 그 아래의 계산 토크, 그리고 M 역행렬의 비대각 칸을 칠한 플랜트. PD는 가속도 (5, −5)를 내고 엘보에 동그라미, 계산 토크는 (10, 0)">
  <g transform="translate(0 3)">
    <defs><marker id="ar11k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
    <g fill="currentColor" font-weight="bold"><text x="10" y="18" font-size="11.5">1 · 오차</text><text x="150" y="18" font-size="11.5">2 · 제어기 둘, 오차 하나</text><text x="426" y="18" font-size="11.5">3 · 플랜트</text></g>
    <line x1="12" y1="40" x2="30" y2="40" stroke="currentColor" stroke-width="2" stroke-dasharray="5 3" opacity="0.75"/>
    <line x1="12" y1="56" x2="30" y2="56" stroke="currentColor" stroke-width="3"/>
    <g fill="currentColor"><text x="35" y="44" font-size="11">명령</text><text x="35" y="60" font-size="11">실제</text></g>
    <g stroke="currentColor" stroke-width="2" stroke-dasharray="5 3" fill="none" opacity="0.75"><polyline points="22,218 114,218 114,126"/></g>
    <g stroke="currentColor" stroke-width="3" fill="none" stroke-linejoin="round"><polyline points="22,218 113.5,227.2 122.7,135.6"/></g>
    <polygon points="22,218 14,230 30,230" fill="none" stroke="currentColor" stroke-width="1.1"/>
    <circle cx="22" cy="218" r="3.6" fill="currentColor"/>
    <circle cx="113.5" cy="227.2" r="3.4" fill="currentColor"/>
    <circle cx="114" cy="218" r="3.2" fill="none" stroke="currentColor" stroke-width="1.1"/>
    <circle cx="122.7" cy="135.6" r="3.4" fill="currentColor"/>
    <circle cx="114" cy="126" r="3.4" fill="none" stroke="currentColor" stroke-width="1.2"/>
    <line x1="114" y1="126" x2="122.7" y2="135.6" stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 1.5"/>
    <text x="106" y="124" font-size="11" text-anchor="end" fill="currentColor">말단 간격 0.14 m</text>
    <g fill="currentColor">
    <text x="12" y="256" font-size="11" font-weight="bold">e = (0.1, 0) rad</text>
    <text x="12" y="271" font-size="11">어깨가 0.1 rad 뒤로</text>
    <text x="12" y="285" font-size="11">= 5.73°, 엘보는 정확</text>
    </g>
    <text x="150" y="48" font-size="11.5" fill="currentColor" font-weight="bold">중력 보상 PD</text>
    <g fill="currentColor"><text x="150" y="84" font-size="11.5">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="150" y="112" font-size="11.5">e<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text></g>
    <text x="190" y="65" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.85">K<tspan dy="3.1" font-size="8.6">p</tspan><tspan dy="-3.1">e + K</tspan><tspan dy="3.1" font-size="8.6">d</tspan><tspan dy="-3.1">ė</tspan></text>
    <g stroke="currentColor" stroke-width="1.1" fill="none"><line x1="170" y1="71" x2="170" y2="89"/><line x1="210" y1="71" x2="210" y2="89"/><polyline points="170,75 175,75 178,71 182.4,79 186.8,71 191.2,79 195.6,71 200,79 204,75 210,75" fill="none"/><line x1="170" y1="85" x2="184" y2="85"/><path d="M182 81 L196 81 M182 89 L196 89 M182 81 L182 89" fill="none"/><line x1="189" y1="82.5" x2="189" y2="87.5"/><line x1="189" y1="85" x2="210" y2="85"/><line x1="170" y1="99" x2="170" y2="117"/><line x1="210" y1="99" x2="210" y2="117"/><polyline points="170,103 175,103 178,99 182.4,107 186.8,99 191.2,107 195.6,99 200,107 204,103 210,103" fill="none"/><line x1="170" y1="113" x2="184" y2="113"/><path d="M182 109 L196 109 M182 117 L196 117 M182 109 L182 117" fill="none"/><line x1="189" y1="110.5" x2="189" y2="115.5"/><line x1="189" y1="113" x2="210" y2="113"/></g>
    <g stroke="currentColor" stroke-width="1.2"><line x1="164" y1="80" x2="170" y2="80"/><line x1="164" y1="108" x2="170" y2="108"/></g>
    <text x="150" y="168" font-size="11.5" fill="currentColor" font-weight="bold">계산 토크</text>
    <g fill="currentColor"><text x="150" y="204" font-size="11.5">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="150" y="232" font-size="11.5">e<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text></g>
    <text x="190" y="185" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.85">K<tspan dy="3.1" font-size="8.6">p</tspan><tspan dy="-3.1">e + K</tspan><tspan dy="3.1" font-size="8.6">d</tspan><tspan dy="-3.1">ė</tspan></text>
    <g stroke="currentColor" stroke-width="1.1" fill="none"><line x1="170" y1="191" x2="170" y2="209"/><line x1="210" y1="191" x2="210" y2="209"/><polyline points="170,195 175,195 178,191 182.4,199 186.8,191 191.2,199 195.6,191 200,199 204,195 210,195" fill="none"/><line x1="170" y1="205" x2="184" y2="205"/><path d="M182 201 L196 201 M182 209 L196 209 M182 201 L182 209" fill="none"/><line x1="189" y1="202.5" x2="189" y2="207.5"/><line x1="189" y1="205" x2="210" y2="205"/><line x1="170" y1="219" x2="170" y2="237"/><line x1="210" y1="219" x2="210" y2="237"/><polyline points="170,223 175,223 178,219 182.4,227 186.8,219 191.2,227 195.6,219 200,227 204,223 210,223" fill="none"/><line x1="170" y1="233" x2="184" y2="233"/><path d="M182 229 L196 229 M182 237 L196 237 M182 229 L182 237" fill="none"/><line x1="189" y1="230.5" x2="189" y2="235.5"/><line x1="189" y1="233" x2="210" y2="233"/></g>
    <g stroke="currentColor" stroke-width="1.2"><line x1="164" y1="200" x2="170" y2="200"/><line x1="164" y1="228" x2="170" y2="228"/></g>
    <rect x="232" y="66" width="32" height="56" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>
    <g stroke="currentColor" stroke-width="1.2"><line x1="210" y1="80" x2="264" y2="80"/><line x1="210" y1="108" x2="264" y2="108"/></g>
    <text x="248" y="98" font-size="11.5" text-anchor="middle" fill="currentColor">+ g</text>
    <g stroke="currentColor" stroke-width="1.2" marker-end="url(#ar11k)"><line x1="264" y1="80" x2="425" y2="80"/><line x1="264" y1="108" x2="425" y2="108"/></g>
    <text x="345" y="74" font-size="11" text-anchor="middle" fill="currentColor">τ = (29.62, 0)</text>
    <rect x="222" y="186" width="40" height="56" fill="none" stroke="currentColor" stroke-width="1.4" rx="3"/>
    <g stroke="currentColor" stroke-width="1.2"><line x1="210" y1="200" x2="222" y2="200"/><line x1="210" y1="228" x2="222" y2="228"/></g>
    <g stroke="currentColor" stroke-width="1" opacity="0.75"><line x1="222" y1="200" x2="262" y2="200"/><line x1="222" y1="228" x2="262" y2="228"/><line x1="222" y1="200" x2="262" y2="228"/><line x1="222" y1="228" x2="262" y2="200"/></g>
    <text x="242" y="182" font-size="11.5" text-anchor="middle" fill="currentColor">M(θ)</text>
    <rect x="270" y="186" width="26" height="56" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>
    <text x="283" y="218" font-size="11.5" text-anchor="middle" fill="currentColor">+ c</text>
    <rect x="302" y="186" width="26" height="56" fill="none" stroke="currentColor" stroke-width="1.2" rx="3"/>
    <text x="315" y="218" font-size="11.5" text-anchor="middle" fill="currentColor">+ g</text>
    <g stroke="currentColor" stroke-width="1.2"><line x1="262" y1="200" x2="270" y2="200"/><line x1="262" y1="228" x2="270" y2="228"/><line x1="296" y1="200" x2="302" y2="200"/><line x1="296" y1="228" x2="302" y2="228"/></g>
    <g stroke="currentColor" stroke-width="1.2" marker-end="url(#ar11k)"><line x1="328" y1="200" x2="425" y2="200"/><line x1="328" y1="228" x2="425" y2="228"/></g>
    <text x="377" y="194" font-size="11" text-anchor="middle" fill="currentColor">τ = (49.62, 10)</text>
    <text x="150" y="140" font-size="12" fill="currentColor">θ = (</text><circle cx="151.6" cy="129.7" r="0.9" fill="currentColor"/><circle cx="154.7" cy="129.7" r="0.9" fill="currentColor"/>
    <text x="178.1" y="140" font-size="12" text-anchor="middle" fill="currentColor">5</text>
    <text x="182.1" y="140" font-size="12" fill="currentColor">,</text>
    <text x="201.4" y="140" font-size="12" text-anchor="middle" fill="currentColor">−5</text>
    <text x="212.9" y="140" font-size="12" fill="currentColor">) rad/s²</text>
    <ellipse cx="201.4" cy="136" rx="12" ry="10" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <text x="268" y="140" font-size="11" fill="currentColor" opacity="0.85">← 엘보: e<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 0, τ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 0</tspan></text>
    <text x="150" y="260" font-size="12" fill="currentColor">θ = (</text><circle cx="151.6" cy="249.7" r="0.9" fill="currentColor"/><circle cx="154.7" cy="249.7" r="0.9" fill="currentColor"/>
    <text x="181.6" y="260" font-size="12" text-anchor="middle" fill="currentColor">10</text>
    <text x="189" y="260" font-size="12" fill="currentColor">,</text>
    <text x="199.4" y="260" font-size="12" text-anchor="middle" fill="currentColor">0</text>
    <text x="203.9" y="260" font-size="12" fill="currentColor">) rad/s²</text>
    <rect x="426" y="58" width="122" height="190" fill="none" stroke="currentColor" stroke-width="1.4" rx="4"/>
    <text x="435" y="80" font-size="11.5" fill="currentColor">θ = M<tspan dy="-4.4" font-size="9">−1</tspan><tspan dy="4.4">(τ − c − g)</tspan></text><circle cx="436.5" cy="70.1" r="0.9" fill="currentColor"/><circle cx="439.5" cy="70.1" r="0.9" fill="currentColor"/>
    <text x="435" y="96" font-size="11" fill="currentColor" opacity="0.8">정지: c = 0</text>
    <text x="449" y="117" font-size="11.5" fill="currentColor">M<tspan dy="-4.4" font-size="9">−1</tspan><tspan dy="4.4" dx="3.4">=</tspan></text>
    <rect x="449" y="124" width="38" height="26" fill="currentColor" fill-opacity="0" stroke="currentColor" stroke-width="1.2"/>
    <text x="468" y="141.5" font-size="12" text-anchor="middle" fill="currentColor">0.5</text>
    <rect x="487" y="124" width="38" height="26" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2"/>
    <text x="506" y="141.5" font-size="12" text-anchor="middle" fill="currentColor" font-weight="bold">−0.5</text>
    <rect x="449" y="150" width="38" height="26" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2"/>
    <text x="468" y="167.5" font-size="12" text-anchor="middle" fill="currentColor" font-weight="bold">−0.5</text>
    <rect x="487" y="150" width="38" height="26" fill="currentColor" fill-opacity="0" stroke="currentColor" stroke-width="1.2"/>
    <text x="506" y="167.5" font-size="12" text-anchor="middle" fill="currentColor">1.5</text>
    <text x="435" y="196" font-size="11" fill="currentColor" opacity="0.85">칠한 칸: 한 관절을</text>
    <text x="435" y="210" font-size="11" fill="currentColor" opacity="0.85">밀면 다른 관절이</text>
    <text x="435" y="224" font-size="11" fill="currentColor" opacity="0.85">움직인다</text>
  </g>
</svg>

1. **왼쪽 — 오차를 기하로.** 카탈로그 자세의 P2를 두 번 그린다. 명령된 팔은 점선, 실제 팔은 실선인데 **어깨**만 $e_1 = 0.1\,\mathrm{rad} = 5.73^\circ$만큼 뒤로 돌아가 있고 엘보 각은 그대로다. 두 말단과 그 사이의 간격을 표시한다. 한 관절은 틀렸고 다른 관절은 정확히 맞다는 것을 붙들고 있어라. 그림의 나머지가 그것에 대한 것이다.
2. **가운데 — 그 오차 하나를 나눠 쓰는 제어기 둘, 위아래로.** 위쪽 경로는 중력 보상을 붙인 관절 공간 PD다. 관절마다 스프링과 댐퍼를 *따로* 그리고, 두 관절 사이를 건너는 선은 하나도 그리지 않은 뒤 $g$를 더하는 상자를 붙인다. 건너는 선이 없는 것은 그림을 대충 그린 것이 아니라 그 제어기의 가정이다. 아래쪽 경로는 계산 토크다. 같은 $K_pe + K_d\dot e$ 신호를 $M(\theta)$라고 쓴 상자로 보내는데, 그 상자에는 두 관절의 선이 모두 들어가고 모두 나온다. 그다음 $c$와 $g$를 더하는 상자가 있다.
3. **오른쪽 — 결합을 만드는 쪽인 플랜트.** 상자 하나, $\ddot\theta = M^{-1}(\tau - c - g)$. $M^{-1}$을 $2\times2$ 격자로 스케치하고 비대각 칸 둘을 칠한다. 진하게 칠한다. 이 페이지의 모든 놀라움이 그 두 칸에서 나온다.

두 경로 아래에는 1열의 오차에 대해 각 경로가 실제로 만드는 가속도를 적는다. PD는 $(5,\ -5)\,\mathrm{rad/s^2}$, 계산 토크는 $(10,\ 0)$이다. 그리고 PD 줄의 엘보 항목, 곧 오차도 0이고 명령 토크도 0인 관절에 동그라미를 친다.

과제는 오차를 엘보로 옮긴 같은 3열 그림을 요구한다.

### 대상으로 한 번 끝까지 · Worked case

상태 하나, 제어기 둘, 숫자는 전부 정확하다. 팔은 카탈로그 자세에 정지해 있고, 어깨가 있어야 할 자리에서 $0.1\,\mathrm{rad}$ 벗어나 있으며, 엘보는 완벽하다. $e = (0.1,\ 0)\,\mathrm{rad}$, $\dot e = 0$, $\ddot\theta_d = 0$이다. 정지 상태라 $c = 0$이므로([[04-robotics/modern-robotics/ch08-dynamics|8장]]) 플랜트는 $\ddot\theta = M^{-1}(\tau - g)$이고 항은 둘뿐이다.

**1단계 — 계산 토크를 계산한다.** 법칙은 $\tau = M(\theta)(\ddot\theta_d + K_pe + K_d\dot e) + c + g$다. 괄호 안은 $K_pe = (10,\ 0)\,\mathrm{rad/s^2}$, 곧 *원하는 가속도*이고, $M$이 그것을 실제로 만들어 내는 토크로 바꾼다:

$$\tau = \begin{pmatrix}3&1\\1&1\end{pmatrix}\begin{pmatrix}10\\0\end{pmatrix} + \begin{pmatrix}19.62\\0\end{pmatrix} = \begin{pmatrix}30\\10\end{pmatrix} + \begin{pmatrix}19.62\\0\end{pmatrix} = \begin{pmatrix}49.62\\10\end{pmatrix}\ \mathrm{N\,m}$$

둘째 성분을 보라. 제어기가 오차가 0인 **엘보**에 $10\,\mathrm{N\,m}$을 보내는데, 그러지 않으면 어깨를 가속하는 동안 엘보가 함께 끌려가기 때문이다. 그 성분이 $M_{21}$이 제 일을 하는 모습이다.

**2단계 — 플랜트가 그것으로 무엇을 하는가.** $\ddot\theta = M^{-1}(\tau - g)$에 넣으면 $M$과 $M^{-1}$이 정확히 상쇄된다:

$$\ddot\theta = M^{-1}\bigl(M(K_pe) + g - g\bigr) = K_pe = (10,\ 0)\ \mathrm{rad/s^2}$$

어깨는 정확히 명령한 만큼 가속하고 엘보는 전혀 움직이지 않는다. $\theta_d$가 상수인 $e = \theta_d - \theta$이므로 $\ddot e = -\ddot\theta$이고, 오차는 관절별로 $\ddot e + K_p e = 0$을 따른다. 검산하면 $-10 + 100(0.1) = 0$이다. $K_d$까지 켜면 같은 상쇄가 $\ddot e + K_d\dot e + K_pe = 0$을 남겨 $\omega_n = \sqrt{K_p} = 10\,\mathrm{rad/s}$, $\zeta = K_d/(2\sqrt{K_p}) = 1$, $2\,\%$ 정착 시간 추정 $4/(\zeta\omega_n) = 0.4\,\mathrm{s}$가 된다. **두 관절 모두 같은 숫자 쌍**이고, 그것이 얻으려는 상 전부다.

**3단계 — 같은 오차, 중력 보상만 붙인 PD.** 이번에는 $M$을 빼고 $\tau = K_pe + K_d\dot e + g = (10,\ 0) + (19.62,\ 0) = (29.62,\ 0)\,\mathrm{N\,m}$을 보낸다. 엘보는 아무것도 요구하지 않았으므로 아무것도 받지 않는다. 플랜트의 대답은 다르다:

$$\ddot\theta = M^{-1}\begin{pmatrix}10\\0\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}\begin{pmatrix}10\\0\end{pmatrix} = \begin{pmatrix}5\\-5\end{pmatrix}\ \mathrm{rad/s^2}$$

한꺼번에 둘이 틀어졌고, 둘 다 $M^{-1}$의 성분이다. 어깨는 요구한 가속도의 **절반**만 얻었다. $(M^{-1})_{11} = 0.5$이지 $1$이 아니기 때문이다. 그리고 오차도 0, 명령 토크도 0인 엘보가 $-5\,\mathrm{rad/s^2}$로 가속하고 있다. $(M^{-1})_{21} = -0.5$이기 때문이다. 버그도 외란도 아니다. 팔은 그냥 하나의 물체이고, 한쪽 끝을 밀면 다른 쪽이 움직인다.

**4단계 — 그것이 오차 동역학의 극점에 하는 일.** 중력이 상쇄되고 $c = 0$이면 PD 제어는 $M\ddot e + K_d\dot e + K_pe = 0$, 곧 $\ddot e + K_dM^{-1}\dot e + K_pM^{-1}e = 0$을 준다. 두 행렬 계수가 *같은* 행렬 $M^{-1}$에 스칼라를 곱한 것이므로, 계는 관절이 아니라 $M$의 고유벡터에서 분리된다. $\mu$를 $M^{-1}$의 고윳값이라 하면 각 모드가 $\ddot e_i + K_d\mu_i\dot e_i + K_p\mu_ie_i = 0$을 따르므로

$$\omega_{n,i} = \sqrt{K_p\mu_i}, \qquad \zeta_i = \frac{K_d\mu_i}{2\sqrt{K_p\mu_i}} = \frac{K_d\sqrt{\mu_i}}{2\sqrt{K_p}} = \sqrt{\mu_i}$$

이고, 마지막 등호는 이 페이지의 $K_d = 2\sqrt{K_p}$ 때문에 성립한다. $M$의 고윳값이 $2 \pm \sqrt2$이므로 $M^{-1}$의 고윳값은 $\mu = (2 \mp \sqrt2)/2 = 0.2929$와 $1.7071$이고, 두 모드는 이렇게 나온다:

| 모드 | 방향 | $\mu$ | $\omega_n$ | $\zeta$ | $4/(\zeta\omega_n)$ | 오버슈트 |
|---|---|---:|---:|---:|---:|---:|
| 무거운 쪽 | $(0.924,\ 0.383)$, 주로 어깨 | $0.2929$ | $5.412$ | $0.5412$ | $1.366\,\mathrm{s}$ | $13.2\,\%$ |
| 가벼운 쪽 | $(0.383,\ -0.924)$, 엘보 역회전 | $1.7071$ | $13.066$ | $1.3066$ | $0.234\,\mathrm{s}$ | 없음 |

이득은 한 쌍인데 팔은 $2.4$배 차이 나는 고유 진동수 둘과 $1$을 사이에 둔 감쇠비 둘로 답한다. 무거운 방향은 울리며 정착에 $1.37\,\mathrm{s}$가 걸리고, 가벼운 방향은 과감쇠라 그 나름대로 굼떠 $0.66\,\mathrm{s}$다. 그 시간은 느린 극점 $-\zeta\omega_n + \omega_n\sqrt{\zeta^2-1} = -6.08\,\mathrm{rad/s}$가 정한다(표의 $4/(\zeta\omega_n)$는 $\zeta \le 1$에서만 맞다). 어느 쪽도 설계한 $\zeta = 1$, $0.4\,\mathrm{s}$가 아니다. **$K_d = 2\sqrt{K_p}$가 임계 감쇠를 사 주는 것은 관성이 $1$일 때뿐이다.** 계산 토크는 먼저 나누어 없애서 관성을 $1$로 만든다. 2단계와 3단계의 차이는 그것 하나다.

**5단계 — 같은 물리를 말단에서.** 카탈로그의 $\Lambda = \mathrm{diag}(1,2)$는 말단 가속도 $a$를 요구하는 작업 공간 제어기가 렌치 $F = \Lambda a$를 가해야 한다는 뜻이고, $\tau = J^\top F$가 그것을 관절 토크로 바꾼다([[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 §3]]). $a = (1,1)\,\mathrm{m/s^2}$이면 $F = (1,\ 2)\,\mathrm{N}$이다. 같은 가속도에 $y$에서 $x$의 두 배 힘이 들고, 그것이 "말단이 $y$에서 두 배 무겁다"의 뜻이다. 그리고 $\tau = J^\top F = (1,\ -1)\,\mathrm{N\,m}$이다. 구조가 1단계와 똑같고 $M$ 자리에 $\Lambda$가, 뒤에 $J^\top$이 붙었을 뿐이다. operational-space 제어가 새 아이디어가 아니라 이 장을 좌표만 바꿔 쓴 것인 이유다.

### 1. 오차 동역학과 두 입력 영역

- **오차 동역학 사고**: *오차*가 안정한 미분방정식([[02-foundations/engineering-math|0.5 §8]])을
  따르도록 제어기를 설계한다 — 예: $\ddot e + K_d \dot e + K_p e = 0$, 이득이 감쇠/주파수를
  고른다.
- **속도 입력 영역(MR §11.3): P와 PI에서는 이득의 역할이 예상과 뒤바뀐다.**
  - **P만** 쓰면 오차 동역학이 *1차*다($\dot\theta_e + K_p\theta_e = c$). $c$는 설정점
    추종이면 0이고 등속 목표면 0이 아니다. 그 0이 아닌 $c$가 정상 상태 오프셋 $c/K_p$를 남긴다.
  - **I를 더하면** 오프셋이 사라진다. 한 번 미분해 보면 대가가 보인다:
    $\ddot\theta_e + K_p\dot\theta_e + K_i\theta_e = 0$. **같은 절의 PI가 이미 2차다.**
    $\omega_n=\sqrt{K_i}$, $\zeta = K_p/(2\sqrt{K_i})$다.
  - **이 두 식에서 역할을 그대로 읽어라**: 속도 입력에서는 $K_p$가 *감쇠*이고 $K_i$가 강성이다.
  - **주의**: I는 와인드업도 데려온다 — 액추에이터가 포화할 수 있는 곳이면 anti-windup이
    필요한 이유다.
- **토크 입력 영역(MR §11.4): $K_p$가 스프링, $K_d$가 댐퍼다.**
  - 단위 관성에서 PD는 $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$이므로
    $\omega_n=\sqrt{K_p}$, $\zeta = K_d/(2\sqrt{K_p})$다 — 속도 입력의 역할과 정반대다. 같은
    기호가 영역마다 다른 일을 하므로 이득은 두 영역 사이에서 옮겨 쓸 수 없다.
  - PID는 한 차수 더 간다. 설정점 오차 동역학이 *3차*다.

> [!example] 계산 예제 · Worked example
> 단위 관성의 토크 입력 PD: $\ddot\theta_e + K_d\dot\theta_e + K_p\theta_e = 0$, $K_p = 100$으로 잡는다.
> - $\omega_n = \sqrt{K_p} = 10$ rad/s.
> - 임계 감쇠: $K_d = 2\sqrt{K_p} = 20$, 즉 $\zeta = 1$.
> - 2% 정착 시간 $\approx 4/(\zeta\omega_n) = 4/10 = 0.4$ s (MR §11.3은 시정수 $t = 1/(\zeta\omega_n)$일 때 정착 $\approx 4t$로 준다).
> - 댐퍼를 절반으로, $K_d = 10$: $\zeta = 10/(2\cdot 10) = 0.5$.
> - 오버슈트 $= e^{-\pi\zeta/\sqrt{1-\zeta^2}} \approx 16\%$ (MR도 $\zeta = 0.5$에 16%를 든다), 정착 $\approx 4/(0.5\cdot 10) = 0.8$ s.
> - $K_d$를 절반으로 줄여도 빨라지지 않는다. $\zeta\omega_n$이 절반이 되어 정착 시간은 두 배가 되고 오차가 오버슈트한다.

이 콜아웃의 모든 줄이 관성을 $1$이라고 가정한다. 관성이 $1$이 아니라 $M$일 때 같은 이득이 무엇을 하는지가 계산의 4단계이고, 답은 설계 하나에서 나온 서로 다른 응답 둘이다.

### 2. 계산 토크의 정의

**계산 토크**(같은 것을 역동역학 제어기, 또는 매니퓰레이터에 적용한 피드백 선형화라고도 한다)는 플랜트 자신의 동역학 모델로 그 동역학을 상쇄해서, 안정화할 대상으로 *선형이고 분리된* 오차 계만 남기는 제어 법칙이다. 이득 조율 요령도 아니고 "PD에 중력 항을 더한 것"도 아니다. 정의에 들어가는 부분이 셋이고, 하나라도 빼면 이것이 존재하는 이유인 그 성질이 깨진다.

1. **피드포워드 가속도** $\ddot\theta_d$, 궤적 자체가 요구하는 가속도;
2. **피드백 가속도** $K_pe + K_d\dot e$, 첫 번째와 단위가 같다 — 이 부분은 토크가 *아니다*;
3. **모델 곱과 보정**: 1과 2의 합에 $\hat M(\theta)$를 곱하고 모델된 $\hat c$와 $\hat g$를 더해, 원하는 가속도를 그것을 만들어 내는 토크로 바꾼다.

$$\tau = \hat M(\theta)\bigl(\ddot\theta_d + K_pe + K_d\dot e\bigr) + \hat c(\theta,\dot\theta) + \hat g(\theta)$$

여기서 $\hat M, \hat c, \hat g$는 *모델된* 질량 행렬, 속도 곱 항, 중력 항이고([[04-robotics/modern-robotics/ch08-dynamics|8장]]), $e = \theta_d - \theta$이며, $K_p, K_d$는 이득 행렬로 관례상 $k_pI$와 $k_dI$다. 실제 플랜트 $M\ddot\theta = \tau - c - g$에 대입하고 $\hat M = M$, $\hat c = c$, $\hat g = g$로 두면 $\ddot e + K_d\dot e + K_pe = 0$만 정확히 남고 $M$은 어디에도 없다. 들어갈 때 곱한 모델 $\hat M$이 나올 때의 실제 $M^{-1}$과 상쇄되기 때문이다. 이제 이득이 2차 계 교과서가 말하는 바로 그 뜻을 갖는 이유가 그 상쇄다.

- **예**: 계산의 1단계. $K_pe = (10,0)$은 원하는 가속도이고, $M(K_pe) = (30,10)$이 그것을 만들어 내는 토크이며, 오차가 0인 엘보의 $10\,\mathrm{N\,m}$이 3번 조건이 결합의 값을 치르는 모습이다. 플랜트는 $\ddot\theta = (10,0)$을 정확히 돌려준다.
- **반례**: 중력 보상을 붙인 PD, $\tau = K_pe + K_d\dot e + \hat g(\theta)$. 전체 모델을 평가하기에 너무 느리거나 너무 불확실할 때 MR이 내놓는 근사다. 1번(자명하게)과 2번, 그리고 3번의 *절반*을 가졌고, 충분히 좋은 제어기다. 다만 계산 토크는 아니다. $M$을 한 번도 적용하지 않았기 때문이다. 3단계가 P2에서 그 차이를 잰다. 같은 오차에서 $(10,0)$이 아니라 $(5,-5)$다.
- **왜 중요한가, 그리고 어디서 멈추는가**: 상쇄는 $\hat M, \hat c, \hat g$만큼만 좋다. 모델이 틀리면 잔차 $(\hat M - M)\ddot\theta + (\hat c - c) + (\hat g - g)$가 사라지지 않고, PD 이득이 떠안아야 할 외란으로 오차 동역학에 들어온다. 잔차가 커질수록 추종 성능과 안정 여유가 함께 나빠진다. 모델 기반 제어가 "모델만큼만 좋다"는 말의 정확한 뜻이고, 트랙의 나머지가 모델을 덜 요구하는 층을 계속 쌓는 이유다.

### 3. 접촉, 그리고 이 장 다음의 제어

**계산: $10\,\mathrm{N}$ 접촉 아래의 P2, PD 대 역동역학.** 카탈로그 자세, $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$([[02-foundations/lab-plants|0.6]]). 패널이 말단을 $F=(0,-10)\,\mathrm{N}$으로 민다(로봇이 아래로 누름). 쌍대는 $\tau=J^\top F=(-10,0)\,\mathrm{N{\cdot}m}$ — 전완이 연직이라 어깨가 짐을 지고 엘보는 안 진다. 역동역학은 그 $J^\top F$(와 $g$)를 더해 $e=0$으로 유지할 수 있다. 관절 공간 PD는 못 한다. 중력이 이미 상쇄되고 복원 토크가 관절마다 $K_p=10\,\mathrm{N{\cdot}m/rad}$인 $K_p e$뿐이면 — 이 페이지의 평소 이득의 10분의 1로 일부러 무르게 잡아 처짐이 깔끔한 숫자로 나오게 한 것이다 — 선형 사상은 어깨 처짐 $e_1\approx 1\,\mathrm{rad}$을 예측한다. 그 $O(1)$ 라디안이 $10\,\mathrm{N}$ 접촉에 선형 스프링이 틀린 대상이라고 강의가 말하는 방식이다. PD는 접촉을 위치 오차 곱하기 강성으로 바꾼다. 단단한 패널 위의 뻣뻣한 PD는 밀리미터에서 큰 힘을 만든다. 임피던스는 다음 페이지에서 그 *관계*를 대신 명령한다.

**힘·임피던스 제어**: 접촉이 중요할 때는 위치만이 아니라 운동과 힘의 *관계*(가상
스프링-댐퍼; 자세한 내용은 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]])를 제어한다 — 접촉이 많은 조작으로 들어가는 입구.

현대적 연속: 최적 피드백([[04-robotics/lqr-lqg|LQR]]) → 제약([[04-robotics/mpc|MPC]]) →
학습된 정책([[02-foundations/rl-basics|RL]], [[01-canonical-papers/notes/4-vla/pi0|VLA]]) —
층마다 모델링 부담을 더 흡수한다.

**위키 연결**: VLA 출력은 플랫폼마다 위치·속도·토크·임피던스 인터페이스와 저수준 루프를
거친다. 접촉 안전은 임피던스 제어 하나가 아니라 액추에이터, 제한기, 수동 순응성, 속도,
과제 설정과 제어를 포함한 전체 스택이 결정한다.

### 스스로 점검

1. $\ddot e + K_d\dot e + K_p e = 0$에서 임계 감쇠가 되는 $K_d$와 $K_p$의 관계는 무엇인가?
2. 계산 토크가 "모델만큼만 좋다"는 말의 구체적 의미는 무엇인가? $M, c, g$가 틀리면 무엇이 남는가?
3. 위치 제어 대신 임피던스 제어가 나은 상황 두 가지를 들어라.
4. 카탈로그 자세의 P2에서 $K_p = 100$, $K_d = 20$인 중력 보상 PD가 한 모드에 $\zeta = 0.541$을, 다른 모드에 $1.307$을 냈다. 고유벡터를 다시 구하지 말고, 둘 다 $1$이 되려면 이 팔이 어떠해야 하는지, 그리고 계산 토크는 왜 그 조건 없이도 거기에 도달하는지 말하라.

> [!tip]- 정답
> 1. $\ddot e + 2\zeta\omega_n\dot e + \omega_n^2 e = 0$과 맞추면 $\omega_n^2 = K_p$, $2\zeta\omega_n = K_d$이므로 $\zeta = 1 \iff K_d = 2\sqrt{K_p}$다([[02-foundations/engineering-math|0.5 §8]]).
> 2. 상쇄가 불완전해서 잔차 비선형 항이 오차 동역학 안에 남고, 그것이 PD 이득이 눌러야 할 외란으로 작용한다. 오차 동역학은 더 이상 정확히 선형이 아니며, 모델 오차가 커질수록 추종 성능과 안정 여유가 함께 나빠진다.
> 3. 접촉 작업(연마, 삽입 — 단단한 표면에 대한 작은 위치 오차가 큰 힘을 만드는 경우)과 인간 협업(충돌을 견딜 수 있게 하는 순응성)이다. 둘 다 위치 정확도보다 *힘–운동 관계*가 중요한 경우다.
> 4. $\zeta_i = K_d\sqrt{\mu_i}/(2\sqrt{K_p})$이고 $\mu_i$가 $M^{-1}$의 고윳값이므로, 두 감쇠비가 모두 $1$이 되려면 $M$의 고윳값이 $1$ 하나로 중복되어야 한다. 곧 $M = I$, 어느 방향에서나 어느 자세에서나 관성이 $1$인 팔이어야 한다. P2는 그런 팔이 아니고, 회전관절로 된 어떤 직렬 매니퓰레이터도 그렇지 않다. 계산 토크는 이득이 플랜트를 보기 전에 $M(\theta)$를 먼저 곱하므로, 뒤에 남는 오차 계의 관성이 모든 방향에서 실제로 $1$이고 설계한 $\zeta$ 하나가 두 관절에 그대로 적용된다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 같은 장치 **P2**, 같은 카탈로그 자세, 같은 이득 $K_p = 100$, $K_d = 20$, 같은 정지 조건. 다만 오차가 반대쪽 관절로 옮겨 갔다. $e = (0,\ 0.1)\,\mathrm{rad}$, $\dot e = 0$, $\ddot\theta_d = 0$이고, 이제 정확히 맞는 관절은 어깨다. 시뮬레이터 없음.

1. **그리기.** 위의 3열 그림을 어깨 대신 엘보가 어긋난 상태로 다시 그린다. $M^{-1}$의 비대각 칸 둘을 칠하고, 두 제어 경로 아래에 각각의 가속도 쌍을 적는다. PD 줄에서 오차도 0, 명령 토크도 0인데 움직이고 있는 관절에 동그라미를 쳐라.
2. **유도.** (a) 계산 토크의 $\tau$와 그것이 만드는 $\ddot\theta$. (b) 중력 보상 PD의 $\tau$와 그것이 만드는 $\ddot\theta$. (c) 둘의 말단 가속도 $\ddot p = J\ddot\theta$, 그리고 두 제어기가 일치하는 성분은 어느 것인지. (d) 이 오차에서의 두 모드 $\zeta$ 값을 다시 계산하지 말고 말하고, 한 문장으로 근거를 대라.
3. **해석.** 위 계산에서는 결합이 명령 가속도를 *줄였다*. $10$ 대신 $5$였다. 여기서는 *키운다*. 두 결과를 $M^{-1}$의 성분으로 설명하고, 다른 관절을 붙들어 놓고 한 관절씩 이득을 조율하는 흔한 관행에 대해 그것이 무엇을 뜻하는지 말하라.

> [!tip]- 정답
> 1. 같은 그림에서 어깨와 엘보의 역할만 바뀐다. PD 줄: $\ddot\theta = (-5,\ 15)$, **어깨**에 동그라미. 계산 토크 줄: $\ddot\theta = (0,\ 10)$.
> 2. (a) $K_pe = (0,10)$이므로 $\tau = M(0,10)^\top + g = (10,10) + (19.62,0) = (29.62,\ 10)\,\mathrm{N\,m}$이고 $\ddot\theta = K_pe = (0,\ 10)\,\mathrm{rad/s^2}$ — 명령한 대로 엘보만 움직인다. (b) $\tau = K_pe + g = (19.62,\ 10)\,\mathrm{N\,m}$이고 $\ddot\theta = M^{-1}(0,10)^\top = (-5,\ 15)\,\mathrm{rad/s^2}$다. (c) $J(0,10)^\top = (-10,\ 0)\,\mathrm{m/s^2}$이고 $J(-5,15)^\top = (-10,\ -5)\,\mathrm{m/s^2}$다. 두 제어기는 말단 $x$ 가속도에서 정확히 일치하고 $y$에서는 완전히 갈린다. 이 자세에서 $J$의 첫 행이 $(-1,-1)$이라 $\ddot p_x = -(\ddot\theta_1 + \ddot\theta_2)$인데, $M^{-1}$의 둘째 열의 합이 $-0.5 + 1.5 = 1$이므로 엘보에만 준 $10\,\mathrm{N\,m}$이 재분배되어도 관절 가속도의 *총합*은 여전히 $10$이다. 결합은 관절 사이에서 가속도를 옮길 뿐 이 행이 읽는 합을 바꾸지 않는다. $J$의 둘째 행은 $(1,0)$이라 $\ddot p_y = \ddot\theta_1$이고 어깨의 엉뚱한 $-5\,\mathrm{rad/s^2}$를 그대로 보고한다. 같은 모델링 오류가 한 과제 방향에서는 보이지 않고 다른 방향에서는 전부 보인다. 작업 공간 검사가 두 방향을 다 봐야 하는 이유다. (d) 그대로 $\zeta = 0.541$과 $1.307$이다. 오차 동역학 $M\ddot e + K_d\dot e + K_pe = 0$은 제차 선형이라 $e$는 초기 조건이지 파라미터가 아니다. 오차를 다른 관절로 옮기면 각 모드가 얼마나 여기되는지가 달라질 뿐 극점의 위치는 달라지지 않는다.
> 3. $M^{-1} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}$다. 어깨에만 준 토크는 $(M^{-1})_{11} = 0.5$가 곱해져 줄고, 엘보에만 준 토크는 $(M^{-1})_{22} = 1.5$가 곱해져 커지며, 공유하는 비대각 $-0.5$가 두 경우 모두 *반대* 관절을 뒤로 민다. 따라서 한 관절씩 조율하는 것은 한 자세에서의 $(M^{-1})_{ii}$를 재는 일인데, 그 값은 $1$도 아니고 작업 영역에서 상수도 아니며, $(M^{-1})_{ij}$는 아예 재지 못한다. 교차 결합은 조율 절차 전체에 보이지 않다가 두 관절이 함께 움직일 때에야 나타난다.
