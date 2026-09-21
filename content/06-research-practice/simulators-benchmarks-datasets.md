---
title: 7. Simulators, Benchmarks & Datasets
tags: [research-practice, guide, tooling]
study-depth: Working
wiki-support: Working
depth-goal: "Choose a simulator, benchmark, or dataset for a stated experiment, and know what each one cannot give you; on P3's handle against RS1's panel, compute the step a penalty contact needs and show what each Euler integrator does to one bounce."
mastery-when: "This is operational knowledge — keep it current rather than deep; the field replaces these tools faster than it replaces its ideas."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/lab-kernel|0.65 Lab Kernel §2–§3]] (explicit and semi-implicit Euler, the two integrators the lab compares) · [[02-foundations/lab-plants|0.6 Lab Plants]] (**P3**, whose handle the drop cell borrows, and **P2**, the arm of RS1) · natural frequency and damping ratio from [[04-robotics/control-theory-ce397|5. Control Theory §5]], and the discrete-time stability test from its §4 · the penalty contact law from [[04-robotics/contact-force-tactile|9. Contact §3]]
> [[02-foundations/lab-kernel|0.65 Lab Kernel §2–§3]](명시적·반암시적 오일러, 랩이 비교하는 두 적분기) · [[02-foundations/lab-plants|0.6 Lab Plants]](낙하 셀이 핸들을 빌려 오는 **P3**, RS1의 팔인 **P2**) · [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]의 고유 진동수와 감쇠비, 같은 페이지 §4의 이산시간 안정성 판정 · [[04-robotics/contact-force-tactile|9. 접촉 §3]]의 페널티 접촉 법칙

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to pick the instrument for an experiment, and to read someone else's
> tooling section for what it quietly rules out.
> **Working** — 실험에 쓸 도구를 고르고, 남의 논문의 도구 절에서 그것이 조용히 배제하는 것을
> 읽어낼 만큼.

> [!warning] This page goes stale faster than any other · 이 페이지가 가장 빨리 낡는다
> Versions, licenses and maintenance status change constantly, and stale tooling advice
> wastes weeks. Everything here was checked against **official sources** on **2026-08-22**,
> and every scale figure is quoted from the paper's own **abstract** unless labelled
> otherwise. Three of the entries below changed status within the last two years. Re-check
> the official page before acting.
> 버전·라이선스·유지보수 상태가 끊임없이 바뀌고, 낡은 도구 조언은 몇 주를 낭비시킨다. 여기
> 있는 것은 전부 **2026-08-22**에 **공식 출처**로 확인했고, 모든 규모 수치는 따로 표시하지
> 않는 한 논문 **자신의 초록**에서 인용한 것이다. 아래 항목 중 셋은 지난 2년 안에 상태가
> 바뀌었다. 행동에 옮기기 전에 공식 페이지를 다시 확인하라.

## English

*Stands on [[02-foundations/lab-kernel|0.65 Lab Kernel]] and [[02-foundations/lab-plants|0.6 Lab Plants]]. A later use of plant **P3** — its home is [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]], and this page borrows only its mass and its wall — and a restatement of RS1, the study every research-practice page shares. Most of this page is a reading page about tools; the running object gives its one numerical claim, §3's, a lab.*

> [!note] First pass · 처음이라면
> Read the running object, then work the worked case — one bounce, stepped by hand with both integrators. Then §3, where the same drop runs as a lab and its table puts a price on what "fast and stable" costs a simulator. After that, §2 (the status traps) and §7–§8 (the missing force data), which are the page's citable absences. §6 and §11 are for the day you read someone else's benchmark numbers.

### Running object · 이 페이지의 대상

Two objects. The study is RS1, which every page of this track shares; the thing this page simulates is a page-local **drop cell** built from **P3**'s handle and RS1's panel.

**RS1 — the running study** (restated on every research-practice page; its numbers never change). *Question:* does impedance control (B) make the planar arm's contact with a panel safer than position control with a force-threshold stop (A)? The arm is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]]; the panel's stiffness is **P3**'s wall, $k_w=400\,\mathrm{N/m}$. One trial is an approach to the panel that makes contact, and a trial succeeds when its peak contact force is at most $10\,\mathrm{N}$. The pilot is **illustrative data, frozen** — a teaching record, not a measurement:

| Arm | Peak contact force per trial (N) | Successes | Mean (N) | Sample sd (N) | Median (N) |
|---|---|---:|---:|---:|---:|
| A — position control + force stop | 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 | 6/10 | 10.66 | 2.414 | 9.85 |
| B — impedance control | 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 | 9/10 | 7.50 | 1.356 | 7.30 |

RS1's outcome is a **peak contact force**. Whenever part of RS1 runs in a simulator first — a controller tuned, a protocol rehearsed — that number comes out of a contact model and an integrator before any controller has a say in it. That is §3's claim, and the drop cell isolates it.

**The drop cell** (page-local, frozen). P3's handle meets a penalty wall with nothing else attached: no hand ($k_h=b_h=0$), no device damper ($b=0$), no controller. Outside the wall no force acts, so every joule the handle gains or loses is the contact's or the integrator's.

| Symbol | Value | What it is |
|---|---:|---|
| $m$ | $0.04\,\mathrm{kg}$ | handle mass — **P3**'s |
| $k$ | $400\,\mathrm{N/m}$ | the panel — RS1's, which is **P3**'s $k_w$ |
| $k$ | $40{,}000\,\mathrm{N/m}$ | the stiff variant — a hundred times the panel, standing in for a hard surface (illustrative) |
| $d$ | $0$ | contact damping by default — the case that isolates the integrator |
| $d$ | $0.8$ and $8\,\mathrm{N{\cdot}s/m}$ | the damped case, on the panel and on the stiff wall — damping ratio $\zeta=0.1$ on both |
| $v_0$ | $0.1\,\mathrm{m/s}$ | closing speed at the touch — the representative approach speed of [[04-robotics/haptics-teleoperation/rendering-sampling-stability\|24.4]] |
| $\Delta t$ | swept | the simulator's step; the worked case uses $1\,\mathrm{ms}$ |

The wall law is the penalty model of [[04-robotics/contact-force-tactile|9. Contact §3]], with the penetration $\delta=x-x_w$ measured from P3's face at $x_w=0.030\,\mathrm{m}$ ($+x$ is into the wall):

$$F=-\max\big(0,\ k\delta+d\dot\delta\big)\ \text{ for }\delta>0,\qquad F=0\ \text{ for }\delta\le0$$

so the wall pushes the handle out and never pulls it in. The drop starts at the touch, $\delta=0$ and $\dot\delta=v_0$, so the contact begins exactly on a sample. That keeps the worked case steppable by hand, and it keeps the lab's table from depending on where between two samples the handle happened to arrive; §3 bounds how much that placement can matter.

**Why this body and not RS1's arm.** The step a contact needs scales with $\sqrt{m/k}$ (worked case, step 4), so the lightest body on the stiffest contact sets the step for a whole scene. P2's tip at its catalog pose has an operational-space inertia of $1\,\mathrm{kg}$ along $x$ and $2\,\mathrm{kg}$ along $y$ ([[02-foundations/lab-plants|0.6]]), so against the same panel it rings at $\sqrt{400/1}=20$ or $\sqrt{400/2}=14.1\,\mathrm{rad/s}$, depending on which way the panel faces. P3's handle rings at $100\,\mathrm{rad/s}$. The handle is the harder case, so it is the one worth running.

*Scope: this page teaches how to choose and cite a simulator, a benchmark or a dataset — and, on the drop cell, why a simulator's contact model and step decide the contact force it reports. It does not teach how a contact solver is built (complementarity is defined in [[04-robotics/contact-force-tactile|9. Contact §1]]; solver internals are not taught here); nor the energy leak of a controller's zero-order hold, which is [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]] — a different energy source whose bound looks similar; nor the statistics of RS1's pilot, which belong to [[06-research-practice/experimental-design-reproducibility|3. Experimental Design & Reproducibility]].*

### Homework diagram · 과제가 그릴 그림

One figure in two parts, and the problem set asks for the same figure for a lighter handle.

<svg viewBox="0 0 560 470" style="max-width:100%;height:auto" role="img" aria-label="one bounce in the phase plane: the exact half circle, explicit Euler spiralling outward, semi-implicit Euler on a tilted ellipse; below, the stable interval of omega times the step">
  <defs><marker id="dcA" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" opacity="0.07"><rect x="150" y="48" width="150" height="282"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.6">
    <line x1="30" y1="150" x2="300" y2="150"/>
    <line x1="150" y1="48" x2="150" y2="330"/>
  </g>
  <g stroke="currentColor" stroke-width="2.2" fill="none"><path d="M150,110 A40,40 0 0 1 150,190"/></g>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-dasharray="2 3" opacity="0.9"><ellipse cx="150" cy="150" rx="56.6" ry="32.7" transform="rotate(-45 150 150)"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="7 4"><path d="M150,110 L190,110 L230,150 L230,230 L150,310"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <path d="M150,310 L40,310" marker-end="url(#dcA)"/>
    <path d="M110,190 L40,190" marker-end="url(#dcA)"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none">
    <rect x="145" y="105" width="10" height="10"/><rect x="185" y="105" width="10" height="10"/>
    <rect x="225" y="145" width="10" height="10"/><rect x="225" y="225" width="10" height="10"/>
    <rect x="145" y="305" width="10" height="10"/>
  </g>
  <g fill="currentColor">
    <circle cx="150" cy="110" r="3.2"/><circle cx="190" cy="110" r="3.2"/><circle cx="190" cy="150" r="3.2"/>
    <circle cx="150" cy="190" r="3.2"/><circle cx="110" cy="190" r="3.2"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="30" y="24" font-weight="600">stiff wall, &#916;t = 1 ms, &#969;&#916;t = 1</text>
    <text x="156" y="44">v (m/s)</text>
    <text x="254" y="143">&#969;&#948; (m/s)</text>
    <text x="96" y="64">outside</text>
    <text x="158" y="64">inside the wall</text>
    <text x="44" y="303">leaves at 4v<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="44" y="183">leaves at v<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="104" y="106">v<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  </g>
  <g stroke="currentColor" fill="none">
    <line x1="318" y1="66" x2="344" y2="66" stroke-width="2.2"/>
    <line x1="318" y1="98" x2="344" y2="98" stroke-width="1.4" stroke-dasharray="7 4"/>
    <rect x="326" y="93" width="10" height="10" stroke-width="1.3"/>
    <line x1="318" y1="146" x2="344" y2="146" stroke-width="1" stroke-dasharray="2 3"/>
  </g>
  <g fill="currentColor"><circle cx="331" cy="146" r="3.2"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="352" y="70">exact: half circle, radius v<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="352" y="102">explicit Euler: each step</text>
    <text x="352" y="116">&#8730;2 farther out; E &#215; 16</text>
    <text x="352" y="150">semi-implicit Euler: on the</text>
    <text x="352" y="164">ellipse of E&#771;; E &#215; 1</text>
    <text x="318" y="198">energy = half the squared</text>
    <text x="318" y="212">distance from the origin</text>
    <text x="318" y="242">peak force: exact 4 N,</text>
    <text x="318" y="256">semi-implicit 4 N, explicit 8 N</text>
  </g>
  <g fill="currentColor" opacity="0.18"><rect x="60" y="392" width="300" height="16"/></g>
  <g stroke="currentColor" stroke-width="1.2">
    <line x1="60" y1="400" x2="510" y2="400"/>
    <line x1="60" y1="392" x2="60" y2="408"/><line x1="210" y1="394" x2="210" y2="406"/>
    <line x1="360" y1="388" x2="360" y2="412"/><line x1="510" y1="394" x2="510" y2="406"/>
  </g>
  <g fill="currentColor"><circle cx="75" cy="400" r="4"/><circle cx="210" cy="400" r="4"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="64" y="384">semi-implicit stable: 0 &lt; &#969;&#916;t &lt; 2</text>
    <text x="398" y="384">both unstable</text>
    <text x="518" y="404">&#969;&#916;t</text>
    <text x="60" y="424" text-anchor="middle">0</text><text x="210" y="424" text-anchor="middle">1</text>
    <text x="360" y="424" text-anchor="middle">2</text><text x="510" y="424" text-anchor="middle">3</text>
    <text x="60" y="442">panel at 1 ms = 0.1</text>
    <text x="196" y="442">stiff at 1 ms = 1</text>
    <text x="318" y="442">2 = 20 ms panel, 2 ms stiff</text>
    <text x="60" y="462" font-style="italic">explicit Euler with d = 0 has no stable &#969;&#916;t at all &#8212; not even inside the band</text>
  </g>
</svg>

Four things the drawing has to get right, each of which is a claim about the physics.
**The axes are scaled so that energy is distance.** Put $\omega\delta$ across and $v$ up, both in m/s. The energy per unit mass, $\tfrac12(v^2+\omega^2\delta^2)$, is then half the squared distance from the origin, so the exact bounce is a half circle of radius $v_0$ from $(0,v_0)$ to $(0,-v_0)$, and leaving on the circle means leaving with the energy that arrived.
**Explicit Euler is a polygon that grows.** Each vertex is $\sqrt{1+(\omega\Delta t)^2}$ times farther out than the last — $\sqrt2$ here — so the handle leaves faster than it came.
**Semi-implicit Euler sits on a tilted ellipse.** Its points leave the circle and come back to it, because what this step conserves is the modified energy $\tilde E$ of step 3, not the true energy. Draw the ellipse through the points.
**The strip underneath.** An $\omega\Delta t$ axis from 0 to 3, with $0<\omega\Delta t<2$ shaded as semi-implicit Euler's stable interval and a note that explicit Euler has none at $d=0$. Mark both walls at $\Delta t=1\,\mathrm{ms}$ — $0.1$ and $1$ — and write under the 2 what it means for each wall in milliseconds.

### Worked case · 대상으로 한 번 끝까지

This is the homework object, worked once on the frozen numbers: the contact frequency, what each integrator does to one step, the stable step in milliseconds, one bounce stepped by hand, and what contact damping changes. The problem set runs the same steps with half the mass.

**Step 1 — the contact frequency.** Inside the wall with $d=0$ the handle obeys $m\ddot\delta=-k\delta$, the undamped mass–spring of [[04-robotics/control-theory-ce397|5. Control Theory §5]]. Starting from the touch,

$$\delta(t)=\frac{v_0}{\omega}\sin\omega t,\qquad \omega=\sqrt{k/m}$$

because $\delta(0)=0$ and $\dot\delta(0)=v_0$ fix the amplitude at $v_0/\omega$. The wall only pushes, so only the first half-period happens: the contact lasts $\pi/\omega$, and the handle leaves at $-v_0$ with the energy it brought.

| | panel, $k=400$ | stiff wall, $k=40{,}000$ |
|---|---:|---:|
| $\omega=\sqrt{k/m}$ | $100\,\mathrm{rad/s}$ | $1000\,\mathrm{rad/s}$ |
| contact time $\pi/\omega$ | $31.4\,\mathrm{ms}$ | $3.14\,\mathrm{ms}$ |
| peak penetration $v_0/\omega$ | $1.00\,\mathrm{mm}$ | $0.100\,\mathrm{mm}$ |
| peak force $kv_0/\omega=v_0\sqrt{km}$ | $0.40\,\mathrm{N}$ | $4.0\,\mathrm{N}$ |

The last row is the quantity RS1 scores, and it depends on $k$ as much as on the approach: the same drop peaks ten times higher on the stiff wall, since $\sqrt{100}=10$.

**Step 2 — explicit Euler adds energy on every step in contact.** Take the energy per unit mass as $\tfrac12(v^2+\omega^2\delta^2)$. One explicit step ([[02-foundations/lab-kernel|0.65 §2]]) is $\delta'=\delta+\Delta t\,v$ and $v'=v-\Delta t\,\omega^2\delta$; squaring and adding,

$$v'^2+\omega^2\delta'^2=\big(1+(\omega\Delta t)^2\big)\big(v^2+\omega^2\delta^2\big)$$

since the cross terms $\mp2\Delta t\,\omega^2\delta v$ cancel exactly. So every step taken from the face or inside it multiplies that energy by $1+(\omega\Delta t)^2>1$, whatever the phase and whatever the step; only the exit step, which lands outside, loses part of the product, because a spring stretched past the face does not exist. No step is small enough to stop it: a smaller step makes each gain smaller and takes more of them. One contact takes about $\pi/(\omega\Delta t)$ steps, so the gains compound to about $e^{\pi\omega\Delta t}$ per bounce while $\omega\Delta t$ is small.

**Step 3 — semi-implicit Euler is stable only for $\omega\Delta t<2$.** The semi-implicit step ([[02-foundations/lab-kernel|0.65 §3]]) updates the velocity first and moves with the new one: $v'=v-\Delta t\,\omega^2\delta$, then $\delta'=\delta+\Delta t\,v'$. As a matrix acting on $(\delta,v)$,

$$\begin{pmatrix}\delta'\\ v'\end{pmatrix}=\begin{pmatrix}1-(\omega\Delta t)^2 & \Delta t\\ -\omega^2\Delta t & 1\end{pmatrix}\begin{pmatrix}\delta\\ v\end{pmatrix}$$

so the determinant is exactly $1$, the trace is $2-(\omega\Delta t)^2$, and the eigenvalues solve $\lambda^2-\big(2-(\omega\Delta t)^2\big)\lambda+1=0$. Their product is $1$. Either they are a complex pair on the unit circle, or they are real and one of them lies outside it. They are complex exactly when $\lvert2-(\omega\Delta t)^2\rvert<2$, which for a positive step is

$$0<\omega\Delta t<2$$

and that is the stable interval by the discrete-time test of [[04-robotics/control-theory-ce397|5. Control Theory §4]]: eigenvalues on the circle and distinct, so bounded but not decaying, like the undamped spring it models. At $\omega\Delta t=2$ the pair collides at $-1$ and the energy grows linearly. Inside the interval the step conserves, exactly, a nearby energy,

$$\tilde E=\tfrac12 mv^2+\tfrac12 k\delta^2-\tfrac12 k\,\Delta t\,\delta v$$

which you can confirm by substituting the step; it is a closed ellipse in the $(\delta,v)$ plane only while $(\omega\Delta t)^2<4$, the same bound. So semi-implicit Euler's true energy wobbles around $\tilde E$ instead of drifting away.

**Step 4 — the bound in milliseconds.** The interval is $\Delta t<2/\omega=2\sqrt{m/k}$:

- **panel**: $2/100=20\,\mathrm{ms}$. At the haptic step of $1\,\mathrm{ms}$, $\omega\Delta t=0.1$ and one contact takes about 31 steps.
- **stiff wall**: $2/1000=2\,\mathrm{ms}$. At $1\,\mathrm{ms}$, $\omega\Delta t=1$ and one contact takes three.

A hundredfold stiffer contact costs a tenfold smaller step, because the bound falls as $1/\sqrt k$. Stable is not the same as accurate: at the bound the whole contact lasts $\pi/2\approx1.6$ steps.

**Step 5 — one bounce by hand: the stiff wall at $\Delta t=1\,\mathrm{ms}$.** Here $\omega\Delta t=1$ — inside semi-implicit Euler's interval, and exactly where explicit Euler's factor per step is $1+1^2=2$. With $\Delta t\,\omega^2=10^{-3}\cdot10^{6}=1000\,\mathrm{s^{-1}}$ and $\Delta t\,v_0=0.1\,\mathrm{mm}$, start at $(\delta,v)=(0,\ 0.1\,\mathrm{m/s})$:

| step | explicit $\delta$ (mm) | explicit $v$ (m/s) | semi-implicit $\delta$ (mm) | semi-implicit $v$ (m/s) |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0.1 | 0 | 0.1 |
| 1 | 0.1 | 0.1 | 0.1 | 0.1 |
| 2 | 0.2 | 0 | 0.1 | 0 |
| 3 | 0.2 | −0.2 | 0 | −0.1 |
| 4 | 0 | −0.4 | −0.1, outside | −0.1 |
| 5 | −0.4, outside | −0.4 | | |

Step 1 is a free step for both, since the force at $\delta=0$ is zero. Step 2 is where they part: both compute $v=0.1-1000\cdot0.0001=0$, but explicit Euler moved $\delta$ with the old velocity, to $0.2\,\mathrm{mm}$, and semi-implicit Euler moved it with the new one, so it stays at $0.1\,\mathrm{mm}$.

- **Explicit**: the handle leaves at $0.4\,\mathrm{m/s}$, so $E_{\text{out}}/E_{\text{in}}=(0.4/0.1)^2=16=2^4$ — one factor of 2 for each of the four steps that began at or inside the face. Peak penetration $0.2\,\mathrm{mm}$; peak force $40{,}000\times0.0002=8\,\mathrm{N}$, twice the exact $4\,\mathrm{N}$.
- **Semi-implicit**: the handle leaves at $0.1\,\mathrm{m/s}$, so $E_{\text{out}}/E_{\text{in}}=1$; peak penetration $0.1\,\mathrm{mm}$ and peak force $4\,\mathrm{N}$, the exact values. At step 1 its true energy per unit mass was $\tfrac12(0.1^2+0.1^2)$, twice what arrived — that is the wobble — while $\tilde E$ held at $\tfrac12\cdot0.1^2$ throughout.

That exact 1 is a property of this step, not of the integrator. At $\omega\Delta t=1$ each semi-implicit step turns the phase by exactly $60^\circ$ ($\cos\theta=1-\tfrac12(\omega\Delta t)^2=\tfrac12$), so the handle is back on the face exactly at a sample; §3's lab shows the general case. On the panel at the same step ($\omega\Delta t=0.1$) the bounce takes 32 steps, too many for hand. Step 2 predicts explicit $\approx e^{0.1\pi}=1.37$, and the loop gives $1.372$, with $1.002$ for semi-implicit.

RS1's line sits at $10\,\mathrm{N}$. Everything in this drop is linear in $v_0$, so the same drop at $0.15\,\mathrm{m/s}$ peaks at an exact $6\,\mathrm{N}$ — a pass by RS1's rule — while explicit Euler at $1\,\mathrm{ms}$ reports $12\,\mathrm{N}$, a failure. No controller changed; the integrator scored the trial.

**Step 6 — what contact damping does.** Give the wall a damper $d$. Three things change, and only the first is physics.

*The bounce loses energy.* With the damping ratio $\zeta=d/(2\sqrt{km})$ of [[04-robotics/control-theory-ce397|5. Control Theory §5]], a linear spring–damper returns the fraction $e=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ of the speed — the same exponential as that section's overshoot. The drop cell's damped case has $\zeta=0.8/(2\sqrt{400\cdot0.04})=8/(2\sqrt{40{,}000\cdot0.04})=0.1$ on both walls, so that formula gives $e=0.729$ and an energy ratio $e^2=0.532$. The wall law's $\max(0,\cdot)$ lets the handle go as soon as the force reaches zero, before the damper can tug it back, so the drop cell's exact ratio is a little higher: $0.554$ ($e=0.744$), from the law solved exactly and matched by a fine-step run.

*Explicit Euler can become stable, if the damper pays for the step.* For a lightly damped contact ($\zeta<1$) the eigenvalues of the damped explicit step have squared modulus $1-2\zeta\,\omega\Delta t+(\omega\Delta t)^2$, which is at most 1 exactly when $\omega\Delta t\le2\zeta$. Substituting $\zeta$ and $\omega$ turns that into

$$d\ \ge\ k\,\Delta t$$

and the mass has cancelled, because $\omega\Delta t$ and $2\zeta$ carry the same factor $1/\sqrt m$. Panel: $d=0.8\ge400\cdot10^{-3}=0.4$, so the step is stable at $1\,\mathrm{ms}$, and up to $2\,\mathrm{ms}$. Stiff wall: $d=8<40$, still unstable at $1\,\mathrm{ms}$; it needs $\Delta t\le0.2\,\mathrm{ms}$. The form echoes the hold's bound $K\le2b/T$ in [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]] — a damper paying for stiffness times period — but the energy source is the integrator, not a hold, and that page's non-example says why the two must not be confused.

*Semi-implicit Euler's interval shrinks.* With the damping force computed from the old velocity, as in the lab, the interval becomes $\omega\Delta t<2(\sqrt{1+\zeta^2}-\zeta)$, which is $1.81$ at $\zeta=0.1$: $18.1\,\mathrm{ms}$ on the panel and $1.81\,\mathrm{ms}$ on the stiff wall. Damping does not buy the symplectic step a larger $\Delta t$; it costs it a little.

Checked with Python: the listing steps the bounce of step 5 with both integrators and prints the ratios. §3's lab runs the same loop over a sweep.

```python
# Worked case, step 5: one bounce on the stiff wall at dt = 1 ms, both integrators.
m, k, dt, v0 = 0.04, 40000.0, 1e-3, 0.1
for method in ("explicit", "semi-implicit"):
    delta, v, peak = 0.0, v0, 0.0            # at the touch
    for _ in range(100):
        a = -k * delta / m if delta > 0 else 0.0
        if method == "explicit":             # position moves with the OLD velocity
            delta, v = delta + dt * v, v + dt * a
        else:                                # position moves with the NEW velocity
            v = v + dt * a
            delta = delta + dt * v
        peak = max(peak, delta)
        if delta < 0:                        # first sample outside: the bounce is over
            break
    print(f"{method:14s} E_out/E_in = {(v / v0)**2:.6f}   peak = {peak*1e3:.4f} mm"
          f"   peak force = {k * peak:.3f} N")
```

It prints `E_out/E_in = 16.000000`, a peak of `0.2000 mm` and `8.000 N` for explicit Euler, and `1.000000`, `0.1000 mm` and `4.000 N` for semi-implicit Euler — the hand values.

### 1. What this page is for

Three questions get asked at the start of every project and answered badly: *which
simulator, which benchmark, which data?* They are usually answered by what a labmate used.
This page answers them by what each tool can and cannot represent — which for contact-rich
construction manipulation turns out to be the deciding question.

The most useful content here is not the recommendations. It is the **absences**: things that
sound like they should exist and do not. Each one is a citable gap.

For example, a wall-wiping experiment can need both a model of contact and a record of real force feedback. A simulator supplies predictions under its contact assumptions; a dataset supplies only the channels that were collected; a benchmark supplies a task and scoring rule. None automatically supplies the other two.

**The reading this gives you.** Write the variable that decides the research claim before selecting a tool. Then inspect whether the tool represents, measures, or merely assumes that variable. This order prevents choosing an attractive platform and later discovering that its available observations cannot answer the intended question.

### 2. Simulators — general purpose

| Simulator | Maintainer | License | Canonical paper | The one thing it is best at |
|---|---|---|---|---|
| **MuJoCo** | Google DeepMind | Apache-2.0 | Todorov, Erez & Tassa, IROS 2012 | fast, stable articulated dynamics; analytically invertible |
| **Isaac Sim** / **Isaac Lab** | NVIDIA | see caveat below / BSD-3 | none / Orbit, RA-L 2023 | thousands of GPU-parallel envs, RTX-photoreal sensors |
| **PyBullet** | community | Zlib | **none** (cite the `@misc`) | easy, mature, CPU-friendly |
| **Gazebo** (`gz`) | Open Source Robotics Alliance | Apache-2.0 | Koenig & Howard, IROS 2004 | ROS 2 integration, sensors, headless CI |
| **Drake** | MIT origin, led by Toyota Research Institute | BSD-3 | **none** (cite the `@misc`) | **hydroelastic contact** — a contact patch with a pressure distribution |
| **SAPIEN** | UCSD SU Lab / Hillbot | see caveat | Xiang et al., CVPR 2020 | part-level articulated objects, via PartNet-Mobility |

Four things in that table need saying out loud, because each is a way to be wrong in print.

> [!warning] Four status traps
> - **Isaac Gym is deprecated.** NVIDIA's own page says: "This is legacy software. Developers
>   may download and continue to use it, but it is no longer supported." `IsaacGymEnvs` and
>   `OmniIsaacGymEnvs` are both archived read-only (GitHub does not expose the archive date). Use Isaac Lab.
> - **"Isaac Sim is Apache 2.0" is not safe to write unqualified.** The same LICENSE file
>   states that building or using it requires additional components — the Omniverse Kit SDK
>   and 3D assets — governed by a separate NVIDIA agreement.
> - **Gazebo Classic reached end of life on 2025-01-29** and its repo was archived. "Ignition"
>   should appear only as history: the rename to `gz` happened because of, in Open Robotics'
>   words, "a trademark obstacle regarding our use of the name 'Ignition'."
> - **SAPIEN's license is genuinely ambiguous**: the repo LICENSE says Apache-2.0, the PyPI
>   metadata says MIT, and GitHub's detector says NOASSERTION. State the ambiguity rather
>   than picking one.

**PyBullet, Drake, Isaac Sim and Genesis have no peer-reviewed paper.** All four officially
direct you to a `@misc` or a URL. That is fine — but write "we used Drake [software
citation]", not a fabricated venue.

### 3. The axis that actually matters: how contact is modelled

For this program the interesting difference between simulators is not speed. It is what
each one *means* by a contact.

- **MuJoCo** solves a soft convex optimisation with elliptic or pyramidal friction cones
  (the set of contact forces Coulomb friction allows, see
  [[04-robotics/contact-force-tactile|Contact, Force & Tactile §2]]),
  and its documentation is explicit that constraint violations are permitted by design — it
  is not a complementarity solver (one that enforces "gap zero or contact force zero"
  exactly, see [[04-robotics/contact-force-tactile|Contact, Force & Tactile §1]]). That is what makes it fast and stable, and it is also why
  a MuJoCo contact force is not the force a load cell would read.
- **Drake's hydroelastic contact** goes the other way: rigid bodies "penetrate slightly, as
  if the rigid body had a slightly deformable layer", producing an approximate contact
  *patch* and *pressure distribution* rather than a point force, with temporal coherence
  across non-convex geometry. Its own documented limits are equally clear — it cannot
  produce a contact surface between two rigid hydroelastic geometries, and it "cannot model
  true deformations given the model does not introduce state", so tangential compliance and
  short-timescale waves are absent.
- **PhysX**, under Isaac, is a game-engine lineage tuned for throughput.

MuJoCo 3.x has been moving toward contact-rich work in a way worth tracking: 3.0 introduced
Flex deformables, 3.3.0 made native convex collision the default, and **3.3.5 added native
SDF support plus a contact sensor and a tactile sensor** — the latter "measuring the
penetration depth between two objects at given points". For a project about
[[04-robotics/tactile-visuotactile|tactile manipulation]], that is a material change.

**The claim on the running object.** Those bullets are three answers to one question, and the drop cell asks it in numbers: *what may a contact do between two time steps?* A penalty spring answers "push back in proportion to the overlap", and the worked case followed that answer to its consequences — a contact frequency the step has to resolve, and an integrator that decides whether the resolved contact keeps its energy, gains it, or throws the body out. Four definitions make the argument portable to any simulator; then the lab runs it.

> **Contact frequency, defined.** The **contact frequency** of a body on a compliant contact is an *angular rate*, in rad/s — a property of a pair, the body and the contact, not of the surface alone and not of the body alone. Three defining conditions. The contact is **modelled as a spring** of stiffness $k$, by a penalty or other compliant law ([[04-robotics/contact-force-tactile|9. Contact §3]]); a rigid complementarity contact has no stiffness, so it has no contact frequency. The mass is the body's **effective mass along the contact normal**, $m$. And the frequency is the one the pair would ring at if the spring could pull as well as push; a unilateral contact lives through only half a period of it.
>
> $$\omega=\sqrt{k/m},\qquad t_c=\pi/\omega$$
>
> where $t_c$ is the duration of an undamped bounce — the natural frequency of [[04-robotics/control-theory-ce397|5. Control Theory §5]] specialised to a contact, which is why it sets the time scale a simulator's step has to resolve.
>
> - **Example**: the drop cell — $100\,\mathrm{rad/s}$ and $31.4\,\mathrm{ms}$ on the panel, $1000\,\mathrm{rad/s}$ and $3.14\,\mathrm{ms}$ on the stiff wall.
> - **Non-example**: "the panel's frequency". The same $400\,\mathrm{N/m}$ panel rings at $20\,\mathrm{rad/s}$ against P2's $1\,\mathrm{kg}$ tip and at $100\,\mathrm{rad/s}$ against P3's handle; the number belongs to the pair.
> - **Non-example**: the $141\,\mathrm{rad/s}$ of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]'s worked case, on the same handle. That loop includes the hand's spring, $\sqrt{(k_h+k_w)/m}$; the contact frequency is the wall's spring alone.
> - **Why it matters**: it turns a contact parameter into a time-step requirement, $\Delta t<2/\omega$ for semi-implicit Euler, and it is the reason the lightest body on the stiffest contact sets the step for a whole scene.

> **Stable step, defined.** A time step $\Delta t$ is **stable** for an integrator on a contact when the integrator's one-step map keeps every trajectory of the in-contact dynamics bounded — a property of the *triple* (integrator, step, contact), never of the integrator alone. Three defining conditions. The test is made on the **linear in-contact dynamics** $m\ddot\delta=-k\delta-d\dot\delta$, where one step is a fixed matrix $A(\Delta t)$ acting on $(\delta,v)$. The eigenvalues of $A$ must lie **inside or on the unit circle**, the discrete-time test of [[04-robotics/control-theory-ce397|5. Control Theory §4]]. And an eigenvalue **on** the circle must not be repeated with a single eigenvector, since that Jordan block grows linearly.
>
> $$\rho\big(A(\Delta t)\big)\le1$$
>
> where $\rho$ is the spectral radius, the largest eigenvalue modulus. For an undamped contact, explicit Euler has $\rho=\sqrt{1+(\omega\Delta t)^2}>1$ at every step, and semi-implicit Euler has $\rho=1$ exactly while $\omega\Delta t<2$, so the stable step is a ceiling, $\Delta t<2/\omega$, for one integrator and does not exist for the other.
>
> - **Example**: semi-implicit Euler on the stiff wall at $1\,\mathrm{ms}$, where $\omega\Delta t=1$.
> - **Non-example**: explicit Euler on an undamped contact at any step — the worked case's factor $1+(\omega\Delta t)^2$ on every step.
> - **Non-example**: "stable, so accurate". At $\omega\Delta t=1.58$ the lab's semi-implicit bounce passes this test and returns $2.25$ times its energy: stability bounds the error; it does not make it small.
> - **Why it matters**: past an unstable step a contact force is the integrator's number rather than the model's, and no post-processing recovers the model's.

> **Symplectic step, defined.** A one-step integrator is **symplectic** when its step map preserves phase-space area — for one degree of freedom, the area of any patch of $(\delta,v)$ states — a property of the *map*, checked on its Jacobian, and not the same thing as conserving energy. Three defining conditions. The system must be **conservative** (Hamiltonian), like the undamped contact, or there is nothing for the map to preserve. The Jacobian of the map must have **determinant 1** at every state, for one degree of freedom. And the payoff, which follows from the definition rather than being part of it, is a **modified energy** $\tilde E$ that tends to the true energy as the step shrinks and that the map conserves — exactly for a linear spring like this contact, and nearly, over very long times, for nonlinear systems.
>
> $$\det\frac{\partial(\delta',v')}{\partial(\delta,v)}=1$$
>
> since a map that keeps area cannot spiral outward, which needs area to grow, or inward, which needs it to shrink — so its orbits close, on the ellipse $\tilde E$ of the worked case, step 3.
>
> - **Example**: semi-implicit Euler, whose step matrix has determinant $\big(1-(\omega\Delta t)^2\big)\cdot1+\omega^2\Delta t\cdot\Delta t=1$.
> - **Non-example**: explicit Euler, with determinant $1+(\omega\Delta t)^2$ — area grows on every step, which is the energy growth seen from another side.
> - **Non-example**: "symplectic means energy-conserving". In the worked case the semi-implicit handle's true energy reached twice $E_{\text{in}}$ mid-bounce; what it conserves is $\tilde E$. And past $\omega\Delta t=2$ the same area-keeping map is unstable, so being symplectic does not replace the stable-step test.
> - **Why it matters**: it is why the lab's semi-implicit column stays near 1 across a range of steps where the explicit column runs away, at the same cost of one force evaluation per step.

> **Energy ratio of a bounce, defined.** The **energy ratio** of one bounce is a *dimensionless ratio of kinetic energies* of the same body in free flight, after and before one contact — the square of the coefficient of restitution, and a property of the simulated contact *including its integrator and step*. Three defining conditions. Both energies are measured **in free flight**, never mid-contact, where part of the energy is stored in the spring. **No other force acts** between the two measurements, so the whole change belongs to the contact. And the body is **one rigid body**, with no internal energy for the difference to hide in.
>
> $$r_E=\frac{E_{\text{out}}}{E_{\text{in}}}=\Big(\frac{v_{\text{out}}}{v_{\text{in}}}\Big)^2=e^2$$
>
> where $v_{\text{in}}$ and $v_{\text{out}}$ are the normal speeds before and after the bounce and $e$ is the coefficient of restitution. A passive physical contact has $r_E\le1$, so any $r_E>1$ was created by the simulation.
>
> - **Example**: the exact undamped bounce, $r_E=1$; the damped drop cell, $r_E=0.554$.
> - **Non-example**: the semi-implicit handle's energy at step 1 of the worked case, twice $E_{\text{in}}$. It was measured mid-contact, so it includes spring energy that is returned.
> - **Non-example**: explicit Euler's $16$ on the stiff wall at $1\,\mathrm{ms}$ is a correctly measured energy ratio, but it is not the contact's; it is the integrator's. The definition measures the simulation, which is what makes it useful.
> - **Why it matters**: it is a one-number test of any simulator's contact that needs no force sensor. Drop a body with no damping configured; if it comes back faster than it arrived, the step or the integrator is wrong for that contact.

**Lab — one drop, two integrators, a sweep over $\Delta t$ and $k$.** The listing runs the drop cell as the worked case did, on three stiffnesses — the panel, the stiff wall, and a tenfold step between them — at five steps from $0.1$ to $20\,\mathrm{ms}$, and reports the energy ratio and the peak penetration for each integrator. It uses the two integrators of [[02-foundations/lab-kernel|0.65 §2 and §3]] and nothing else; a second loop reruns part of the sweep with the frozen dampers.

```python
import numpy as np

# The drop cell, frozen: P3's handle meets a penalty wall at v0; the clock starts at the touch.
m, v0 = 0.04, 0.1                   # kg, m/s

def drop(k, d, dt, method, t1=0.1):
    """One bounce; delta is the penetration (> 0 inside the wall).
    Returns (E_out/E_in, peak penetration in m)."""
    delta, v, peak = 0.0, v0, 0.0
    for _ in range(int(round(t1 / dt))):
        f = max(0.0, k * delta + d * v) if delta > 0 else 0.0   # pushes out, never pulls
        a = -f / m
        if method == "explicit":    # 0.65 section 2: position moves with the OLD velocity
            delta, v = delta + dt * v, v + dt * a
        else:                       # 0.65 section 3: position moves with the NEW velocity
            v = v + dt * a
            delta = delta + dt * v
        peak = max(peak, delta)
    return (v / v0) ** 2, peak      # after the exit only kinetic energy is left

print(" k N/m  dt ms   w*dt  E ratio ex  E ratio si  pen ex mm  pen si mm  exact mm")
for k in (400.0, 4000.0, 40000.0):
    w = np.sqrt(k / m)
    for dt in (1e-4, 1e-3, 2e-3, 5e-3, 2e-2):
        rx, px = drop(k, 0.0, dt, "explicit")
        rs, ps = drop(k, 0.0, dt, "semi")
        mark = "  <- semi-implicit unstable" if round(w * dt, 9) >= 2 else ""
        print(f"{k:6.0f} {dt*1e3:6.1f} {w*dt:6.3f} {rx:11.4g} {rs:11.4g}"
              f" {px*1e3:10.4f} {ps*1e3:10.4f} {v0/w*1e3:9.4f}{mark}")

print("\ndamped, zeta = 0.1 on both walls (exact E ratio 0.554)")
print(" k N/m  d Ns/m  dt ms   k*dt   w*dt  E ratio ex  E ratio si")
for k, d in ((400.0, 0.8), (40000.0, 8.0)):
    w = np.sqrt(k / m)
    for dt in (1e-4, 1e-3, 2e-3, 5e-3):
        rx, _ = drop(k, d, dt, "explicit")
        rs, _ = drop(k, d, dt, "semi")
        print(f"{k:6.0f} {d:6.1f} {dt*1e3:6.1f} {k*dt:6.2f} {w*dt:6.2f} {rx:11.4g} {rs:11.4g}")

# the worked case, as a check on the loop
assert abs(drop(40000.0, 0.0, 1e-3, "explicit")[0] - 16.0) < 1e-9
assert abs(drop(40000.0, 0.0, 1e-3, "semi")[0] - 1.0) < 1e-9
```

The undamped sweep, as the listing prints it. **Bold** marks an unstable step: every explicit cell, because with $d=0$ explicit Euler has no stable step at all (the column shows what each step costs), and the semi-implicit cells at $\omega\Delta t\ge2$.

| $k$ (N/m) | $\Delta t$ (ms) | $\omega\Delta t$ | $E_{\text{out}}/E_{\text{in}}$, explicit | $E_{\text{out}}/E_{\text{in}}$, semi-implicit | peak $\delta$, explicit (mm) | peak $\delta$, semi-implicit (mm) | exact $v_0/\omega$ (mm) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.1 | 0.010 | **1.032** | 1.000 | 1.008 | 1.000 | 1.000 |
| 400 | 1 | 0.100 | **1.372** | 1.002 | 1.083 | 1.001 | 1.000 |
| 400 | 2 | 0.200 | **1.872** | 1.009 | 1.170 | 1.005 | 1.000 |
| 400 | 5 | 0.500 | **4.717** | 1.045 | 1.500 | 1.031 | 1.000 |
| 400 | 20 | 2.000 | **121** | **9** | 4.000 | 2.000 | 1.000 |
| 4,000 | 0.1 | 0.032 | **1.105** | 1.000 | 0.324 | 0.316 | 0.316 |
| 4,000 | 1 | 0.316 | **2.708** | 1.010 | 0.406 | 0.320 | 0.316 |
| 4,000 | 2 | 0.632 | **7.097** | 1.045 | 0.520 | 0.320 | 0.316 |
| 4,000 | 5 | 1.581 | **60.06** | 2.250 | 1.000 | 0.500 | 0.316 |
| 4,000 | 20 | 6.325 | **$1.416\times10^4$** | **1,521** | 4.000 | 2.000 | 0.316 |
| 40,000 | 0.1 | 0.100 | **1.372** | 1.002 | 0.108 | 0.100 | 0.100 |
| 40,000 | 1 | 1.000 | **16** | 1.000 | 0.200 | 0.100 | 0.100 |
| 40,000 | 2 | 2.000 | **121** | **9** | 0.400 | 0.200 | 0.100 |
| 40,000 | 5 | 5.000 | **5,476** | **576** | 1.000 | 0.500 | 0.100 |
| 40,000 | 20 | 20.00 | **$1.438\times10^6$** | **$1.592\times10^5$** | 4.000 | 2.000 | 0.100 |

The damped rerun, $\zeta=0.1$ on both walls, where the exact ratio is $0.554$. Explicit Euler is stable where $k\Delta t\le d$ and semi-implicit Euler where $\omega\Delta t<1.81$ (worked case, step 6); **bold** marks the cells outside those conditions.

| $k$ (N/m) | $d$ (N·s/m) | $\Delta t$ (ms) | $k\Delta t$ | $\omega\Delta t$ | $E_{\text{out}}/E_{\text{in}}$, explicit | $E_{\text{out}}/E_{\text{in}}$, semi-implicit |
|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.8 | 0.1 | 0.04 | 0.01 | 0.573 | 0.555 |
| 400 | 0.8 | 1 | 0.40 | 0.10 | 0.776 | 0.565 |
| 400 | 0.8 | 2 | 0.80, the boundary | 0.20 | 1.089 | 0.580 |
| 400 | 0.8 | 5 | 2.00 | 0.50 | **2.887** | 0.646 |
| 40,000 | 8 | 0.1 | 4 | 0.10 | 0.776 | 0.565 |
| 40,000 | 8 | 1 | 40 | 1.00 | **12.45** | 0.922 |
| 40,000 | 8 | 2 | 80 | 2.00 | **100.8** | **11.56** |
| 40,000 | 8 | 5 | 200 | 5.00 | **2,500** | **625** |

Reading the two tables.

**It is one table in $\omega\Delta t$.** The panel at $1\,\mathrm{ms}$ and the stiff wall at $0.1\,\mathrm{ms}$ share $\omega\Delta t=0.1$ and give the same ratios, $1.372$ and $1.002$; only the millimetres differ, by the factor $v_0/\omega$. So do the panel at $20\,\mathrm{ms}$ and the stiff wall at $2\,\mathrm{ms}$. Nothing but $\omega\Delta t$ decides how a step treats a contact, which is why step 4's bound, $\Delta t<2/\omega$, is the whole rule.

**Explicit Euler gains in every undamped cell** — 3% at $\omega\Delta t=0.01$, 37% at $0.1$, sixteenfold at $1$. That column is a price list, not a stability boundary.

**Semi-implicit Euler holds until $\omega\Delta t=2$ and then fails as step 3 said**: $9$ at the boundary, $576$ at $5$. Inside the interval its ratio stays within a band set by where the contact starts and ends between samples. If the first sample inside the wall is a fraction $\varphi$ of a step past the face, the conserved $\tilde E$ equals $E_{\text{in}}\big(1-(\omega\Delta t)^2\varphi(1-\varphi)\big)$ there; if the first sample outside is a fraction $s$ of a step beyond it, $E_{\text{out}}\big(1-(\omega\Delta t)^2s(1-s)\big)=\tilde E$. Both products $\varphi(1-\varphi)$ and $s(1-s)$ lie between $0$ and $\tfrac14$, so

$$1-\tfrac14(\omega\Delta t)^2\ \le\ \frac{E_{\text{out}}}{E_{\text{in}}}\ \le\ \frac{1}{1-\tfrac14(\omega\Delta t)^2}$$

Since the drop cell starts on a sample ($\varphi=0$), its column can only sit at or above 1. Every entry does, below its ceiling: $1.045$ at $\omega\Delta t=0.5$ against $1.067$, and $2.25$ at $1.58$ against $2.67$. That last cell passes the stability test and is still a bad number.

**Penetration tells the same story in millimetres.** Explicit Euler's peak grows with its spiral — $1.5\,\mathrm{mm}$ on the panel at $5\,\mathrm{ms}$ against an exact $1.0\,\mathrm{mm}$. Semi-implicit Euler's stays within the ellipse's widest point, $v_0/\big(\omega\sqrt{1-\tfrac14(\omega\Delta t)^2}\big)$. Outside the interval both peaks are just the first samples inside the wall, $\Delta t\,v_0$ and twice that: $2$ and $4\,\mathrm{mm}$ on a wall whose true peak is $0.1\,\mathrm{mm}$.

**One scene, one step.** A simulator steps every contact in a scene with the same $\Delta t$, so the stiffest contact on the lightest body decides it. With the panel and the stiff wall in one scene, $1\,\mathrm{ms}$ is the largest step on this grid that keeps semi-implicit Euler inside its interval for both; at that step the panel gets about 31 steps per contact and the stiff wall three.

**Damping does what step 6 said.** Explicit Euler becomes stable where $d\ge k\Delta t$ — the panel at $0.1$ and $1\,\mathrm{ms}$, the stiff wall at $0.1\,\mathrm{ms}$ — and even there it overstates the restitution: $0.776$ against the exact $0.554$ at $\omega\Delta t=0.1$. On its boundary (the panel at $2\,\mathrm{ms}$) a bounce still gains 9%. Semi-implicit Euler tracks $0.554$ closely until its narrowed interval ends: $0.922$ at $\omega\Delta t=1$, inside the interval and already far off, and $11.6$ at $2\,\mathrm{ms}$, outside it — worse than the undamped $9$.

**What the table says about the simulators above.** None of the simulators in §2 is the drop cell, and nothing in these tables measures one of them. What the tables do is put a price on choices that §2 and §3 already attribute to them.

- **MuJoCo** permits constraint violations by design (above): its contacts interpenetrate softly instead of enforcing a zero gap, which puts it on the compliant side of the table in [[04-robotics/contact-force-tactile|9. Contact §3]], with the drop cell, rather than on the rigid side. In a penalty model the stable step, $2\sqrt{m/k}$, and the peak penetration, $v_0\sqrt{m/k}$, carry the same $\sqrt{m/k}$, so softening a contact until it is stable at a coarse step deepens its penetration by the same factor. "Fast and stable" and "not the force a load cell would read" are one choice seen from two sides.
- **MuJoCo 3.3.5's tactile sensor** reports a penetration depth (above). The penetration columns show a simulated penetration moving with the contact's softness and with the step — $0.1\,\mathrm{mm}$ exact and $0.2\,\mathrm{mm}$ under explicit Euler at $1\,\mathrm{ms}$, on the same wall — so a simulated tactile reading carries the contact model and the step inside it.
- **Drake's hydroelastic contact** also lets rigid bodies penetrate, through a "slightly deformable layer" (above). Any such compliance, together with the masses resting on it, sets a time scale that a fixed-step simulation has to resolve; the drop cell does not say how Drake's solver meets it.
- **PhysX under Isaac** is "tuned for throughput", and **Isaac Lab** runs thousands of parallel environments (§2). Throughput is counted in steps, and the $\omega\Delta t$ column is the condition every step has to meet: halving $\Delta t$ doubles the steps for the same simulated time, and a tenfold stiffer contact on the same mass needs a step $\sqrt{10}\approx3.2$ times smaller — $6.3\,\mathrm{ms}$ instead of $20$ in the table's middle rows.
- **PyBullet** appears in §2 only as easy, mature and CPU-friendly. This page says nothing about how it steps contact, and the lab does not change that.

Which integrator and which default step each of them uses is in its own documentation and can change between versions, which is why §10 asks for both.

### 4. Terrain and earthmoving

A separate world, with separate tools, and the only part of this domain where simulation is
genuinely mature.

- **AGX Dynamics** (Algoryx) is the strongest documented option. Its `agxTerrain` module
  models a 3D voxel grid carrying mass, compaction and soil type under a height-field
  surface; a digging tool creates failure zones that convert solid terrain mass into dynamic
  mass, parameterised by **angle of internal friction and cohesion** (the two soil-strength
  parameters: how much shear resistance grows with the pressure on the soil, and how much it
  has at zero pressure), with solid cells
  becoming 6-DoF particles and a mass-aggregate body supplying inertial resistance through
  the failure plane. Penetration resistance and digging resistance are separate. It models
  compaction, swell factor, and angle of repose.
  - Uniquely, it has **both** vendor parameter-level documentation **and** a peer-reviewed
    open-access physics paper: Servin, Berglund and Nystedt, *A multiscale model of terrain
    dynamics for real-time earthmoving simulation*, 2021. Algoryx states the model's digging
    resistance and soil displacements "agree with the reference model up to 10-25%, and run
    more than three orders of magnitude faster".
  - Commercial, yearly subscription per seat, **price on request**. Academic single and group
    licences exist, strictly non-commercial.
- **Vortex Studio** (CM Labs) has documented deformable terrain, soil materials and soil
  particles, and is commercially proven in operator training. Two problems for research:
  no retrievable vendor theory document for its soil model — the best descriptions are
  third-party — and, in CM Labs' own words, **"An academic License is not offered anymore."**
- **Project Chrono** is the best open option (BSD-3) and the only one offering a *ladder* of
  soil fidelity in one framework: **SCM** (Soil Contact Model, a deformable ground mesh driven
  by the Bekker-Wong semi-empirical pressure–sinkage relations), granular **DEM** (discrete
  element method, which simulates individual grains), **FEA** (finite element analysis of the
  soil as a continuous material), and **CRM**, a continuum model solved with SPH (smoothed
  particle hydrodynamics, a mesh-free particle method). Moving from an empirical law toward
  modelling the material and its grains adds detail and computational cost. CRM's paper
  explicitly covers "digging, grading" and validates against a real digging robot. **Chrono DEM-Engine** is the
  high-fidelity reference to validate against rather than to run policies in.

> [!note] The honest recommendation
> **AGX if you can buy it, Chrono::CRM if you need open and citable**, with DEM-Engine as the
> reference model. And carry the caveat: both leading real-time soil models are validated
> only to roughly **10-25%** of a DEM reference. Quantitative digging forces out of any
> real-time simulator are approximate, and a paper that reports them to three significant
> figures is over-claiming.

### 5. Deformable construction materials — a gap, stated plainly

**No simulator has a documented model for construction materials as such.** Not drywall, not
rebar cages, not building membranes. What exists is generic primitives you would have to
parameterise and validate yourself:

| Material | Nearest primitive | State of the art |
|---|---|---|
| Cable, rope, hose | AGX `agxCable` | **solved at industrial grade** — lumped rigid bodies with all six DOF, so bending, twisting and stretching are tracked, plus plasticity. Documented limits: cables must be circular and homogeneous, fixed resolution |
| Rebar mesh, cages | networks of connected rods | **no dedicated model.** Nearest is DisMech (RA-L 2024), which handles arbitrary connections between rods |
| Membranes, sheets | thin shells | Chrono's `ChElementShellReissner` is the most physically appropriate documented formulation, and BSD-3 — but **no construction-material validation exists anywhere** |
| **Drywall panel** | — | **nothing.** A stiff, brittle, heavy panel that *fractures* rather than deforming elastically is not modelled by anything verifiable |

One more limit worth knowing before choosing Isaac for deformable work: its documentation
states that **"Particles and deformable body do not support contact reports"**, along with
no static friction and no friction combine mode. You cannot read contact forces off a
deformable — which is the measurement a contact-rich manipulation study exists to make.

> [!warning] Genesis — read the history before citing it
> Genesis (now **Genesis World**, developed under the company Genesis AI) offers unusually
> broad multi-physics under one API. Its December 2024 README claimed, verbatim, "over 43
> million FPS when simulating a Franka robotic arm with a single RTX 4090 (430,000 times
> faster than real-time)". A MuJoCo maintainer questioned the comparison publicly; a
> ManiSkill developer filed an issue arguing the benchmark used the fastest physics setting,
> took one action followed by 999 no-op steps, and disabled self-collisions. The team then
> published a corrected benchmark whose script header says it is "mostly identical to" the
> critic's, and the issue was closed by the critic saying the new numbers "look more accurate
> given the right context" — while noting he had not re-verified them. **The 43-million-FPS
> claim was removed from the README in May 2026 as part of a rewrite, with no labelled
> retraction.** There is still no peer-reviewed paper; the official citation block offers a
> company blog post and a repo URL. None of this means the software is bad. It means you
> cannot cite it as a validated result, and you should say "software" when you cite it.

### 6. Benchmarks

| Benchmark | Venue | Sim / real | What it measures | Abstract-stated scale |
|---|---|---|---|---|
| **RLBench** | RA-L 2020 | simulation | task success, few-shot generalization | "100 completely unique, hand-designed tasks" |
| **Meta-World** | CoRL 2019 | simulation | multi-task and meta-RL transfer to held-out tasks | "50 distinct robotic manipulation tasks" |
| **ManiSkill 3** | RSS 2025 | simulation | throughput and task coverage | "up to 30,000+ FPS"; "12 distinct domains" |
| **CALVIN** | RA-L 2022 | simulation | long-horizon language-conditioned, zero-shot | **no numbers in the abstract** |
| **LIBERO** | NeurIPS 2023 D&B | simulation | **lifelong** transfer — forward, backward, task ordering | "four task suites (130 tasks in total)" |
| **FurnitureBench** | RSS 2023 | **both** | real-world long-horizon contact-rich **assembly** | "200+ hours of pre-collected data (5000+ demonstrations)" |
| **RoboCasa** | RSS 2024 | simulation | data-scaling behaviour for imitation learning | "over 150 object categories"; "100 tasks" |
| **NIST Assembly Task Boards** | RA-L 2020 | **real only** | time-to-complete against **tabulated** human handling times | "three task board artifacts" |
| **RAMP** | RA-L 2024 | **both** | assembly planning *and* execution, three difficulty classes | **no scale figures in the abstract** |

> **Benchmark, defined.** A **benchmark** is a *shared evaluation instrument* — a task with a fixed scoring rule that anyone can reuse — not a dataset, not a simulator, and not one paper's comparison. Three defining conditions, and the absences in this section are claims about them. It has a **public protocol**: the task, its starting conditions and what counts as success are written down well enough to rerun. It has **public artifacts**: the environments, objects or boards the protocol runs on are available to others. And **results can be added**: someone who did not build it can report a score comparable to the published ones.
>
> - **Example**: the NIST Assembly Task Boards — physical artifacts and a human-referenced scoring protocol, as below.
> - **Non-example**: a comparative evaluation inside one paper, such as the construction-skill comparisons in Self-check answer 5. It may be careful, but it has no public protocol that others add results to.
> - **Non-example**: Open X-Embodiment (§7). It supplies recorded channels, not a task and a scoring rule, which makes it a dataset in §1's sense.
> - **Why it matters**: every absence in this section is a claim that nothing in a domain meets all three conditions. Name the condition that fails and the claim becomes checkable.

**The assembly line of descent is the relevant one here**: NIST task boards give physical
artifacts and a human-referenced scoring protocol (peg insertion, gear meshing, connectors,
nut threading, and in later boards cable routing and wire harnesses); FurnitureBench adds a
real-robot long-horizon benchmark with a simulator alongside; and **RAMP** is the only one
framed on construction — its Section I says the domain is *offsite* construction and that
"the assembly of beams into frames remains a manual process".

> [!important] Cite RAMP carefully
> RAMP's abstract says only "real-world industrial assembly tasks" — **the word
> construction does not appear in it**. The offsite-construction framing is in the paper
> body. If you cite RAMP as a construction benchmark, cite the section, not the abstract.

**Two verified absences in the benchmark landscape** — the third, on the dataset side, is in §7. There is **no benchmark for on-site construction manipulation** —
nothing for bricklaying, drywall, rebar tying, façade installation or overhead work. What
exists is vendor throughput figures and one-off papers with bespoke evaluations: no shared
protocol, no shared artifacts, no leaderboard. And there is **no standardised benchmark or
test-pit protocol for excavation or earthmoving**. ISO 7546, ISO 6165, ISO 10968 and the SAE
MTC1 committee standardise *machines*, not autonomy performance. NASA's Lunabotics has
published rules and a rubric, but it is regolith-simulant, student-scoped, and the rules
change annually.

### 7. Datasets — and the modality that is missing

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="three bands of dataset capability, the third of which is empty">
  <g fill="currentColor">
    <rect x="24" y="42" width="512" height="48" rx="4" fill-opacity="0.07"/>
    <rect x="24" y="112" width="512" height="48" rx="4" fill-opacity="0.16"/>
    <rect x="40" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="205" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="370" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="40" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="205" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="370" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.5">
    <rect x="24" y="42" width="512" height="48" rx="4"/><rect x="24" y="112" width="512" height="48" rx="4"/>
    <rect x="40" y="52" width="150" height="28" rx="3"/><rect x="205" y="52" width="150" height="28" rx="3"/><rect x="370" y="52" width="150" height="28" rx="3"/>
    <rect x="40" y="122" width="150" height="28" rx="3"/><rect x="205" y="122" width="150" height="28" rx="3"/><rect x="370" y="122" width="150" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.75" stroke-dasharray="6 4">
    <rect x="24" y="182" width="512" height="48" rx="4"/>
  </g>
  <g font-size="10.5" fill="currentColor" font-weight="600">
    <text x="24" y="36">vision + proprioception + language</text>
    <text x="24" y="106">&#8230; and a force / torque channel</text>
    <text x="24" y="176">&#8230; and on a construction task</text>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="115" y="66">Open X-Embodiment</text><text x="115" y="77" font-size="9">527 skills, 160,266 tasks</text>
    <text x="280" y="66">DROID</text><text x="280" y="77" font-size="9">65,000 trajectories</text>
    <text x="445" y="66">BridgeData V2</text><text x="445" y="77" font-size="9">53,896 trajectories</text>
    <text x="115" y="136">RH20T</text><text x="115" y="147" font-size="9">110,000+ sequences</text>
    <text x="280" y="136">FMB</text><text x="280" y="147" font-size="9">functional manipulation</text>
    <text x="445" y="136">REASSEMBLE</text><text x="445" y="147" font-size="9">4,551 demonstrations</text>
    <text x="280" y="212" font-size="11" opacity="0.9">no shared real-robot force data</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="250">Every count is quoted from that paper&#8217;s own abstract. The third band is empty, and that is the finding.</text>
  </g>
</svg>

The large manipulation corpora are **vision, proprioception and language**. That is not an
oversight in any one dataset — it is baked into the shared schema. The Open X-Embodiment
overview sheet's columns run *robot, episodes, file size, morphology, gripper, action space,
RGB cameras, depth cameras, wrist cameras, language annotations, collection method,
proprioception, scene type, control frequency* — **there is no force column and no tactile
column.** The dominant data format cannot represent the modality that
[[04-robotics/force-compliance-control|contact-rich manipulation]] most depends on.

The datasets that do break the pattern:

- **RH20T** is the important one: its abstract states "over 110,000 contact-rich robot
  manipulation sequences", and its project page documents a **6-DoF force/torque channel at
  100 Hz** alongside RGB, depth, joint torque and audio. Fingertip tactile exists but only
  on **one of seven robot configurations** — do not describe the whole corpus as tactile.
- **FMB** (IJRR) exposes end-effector force and torque fields explicitly.
- **REASSEMBLE** records event cameras, force-torque, microphones and multi-view RGB, on
  NIST task boards — "4,551 demonstrations, of which 4,035 were successful".
- Inside OXE, two constituent datasets do carry force — but be precise about where.
  `iamlab_cmu_pickup_insert` puts it **in the state vector** (20-dim: 7 joint angles, gripper,
  6 joint torques, 6 end-effector force). `stanford_kuka_multimodal` (the
  [[01-canonical-papers/notes/7-robotics/vision-and-touch|Vision-and-Touch]] data) does **not**:
  its state is 8-dim proprioception only, and force lives in a sibling observation field
  (`ee_forces_continuous`). Both are small, and the pooled schema surfaces neither.

> [!warning] Two citation traps in the big datasets
> **DROID** reports different numbers in different places: the arXiv abstract says 76k
> trajectories and 84 tasks; the RSS proceedings abstract says 65,000 and 86.
> **BridgeData V2** likewise: 60,096 trajectories on arXiv, 53,896 in the PMLR proceedings.
> Quote the number that matches the version you cite.

### 8. Construction and field data

Real construction-site datasets exist, and every one of them is a **perception** corpus:

- **ConSLAM** — and note there are **two distinct papers**, not one. The ECCV 2022 Workshops
  paper announces the dataset (images, LiDAR, IMU, terrestrial-laser ground truth, collected
  periodically). The *Journal of Computing in Civil Engineering* 2023 paper is the extended
  version and adds what makes it a benchmark: it quantifies the release at "five sequences",
  **recovers a ground-truth trajectory** by registering sequential LiDAR to the reference
  scans, and documents how to score SLAM error against it automatically. The authors' own
  repository labels the journal paper a "Free Journal Extension Paper" of the workshop one —
  it is one dataset published twice, not two datasets.
- **Hilti-Oxford** (RA-L 2023) and the **Hilti SLAM Challenge** series — LiDAR, cameras,
  IMU, with millimetre-accurate ground truth in construction environments, CC BY-NC-SA.
- **Rohbau3D** (*Scientific Data*, 2025) — "504 high-resolution LiDAR scans captured with a
  terrestrial laser scanner across 14 distinct construction sites", semantically labelled,
  **CC BY 4.0**. The best-licensed construction-site 3D corpus found.
- **ConRebSeg** — "14,805 RGB images with segmentation labels for autonomous robotic
  inspection of reinforced concrete defects", CC BY 4.0.
- **SODA**, **MOCS**, **ACID**, **CIS** — construction *image* datasets for detection and
  segmentation. Note two traps: ACID is sometimes miscited as an excavation dataset when it
  is images of machines with no soil, forces or trajectories — and there is an unrelated
  robotics paper also called ACID, on deformable-object manipulation.

For earthmoving specifically, the largest trajectory corpus is a corporate release —
excavator motion data with RGB, LiDAR-derived elevation maps and joint angles, under a
non-commercial licence, **with no paper behind it**. ETH's dry-stone dataset releases 1,100
digitised stone meshes with placement-viability labels under CC BY 4.0 — geometry and
labels, no trajectories, no force. **No public dataset of measured bucket forces or
soil-tool interaction exists.**

> [!important] The sharpest way to state the gap
> Two of these datasets were recorded **from real construction machines** — the Hilti SLAM
> Challenge 2023 used a drilling-robot platform drawing on the Jaibot (the challenge paper's
> abstract says only "an off-the-shelf LiDAR mounted on a robot", so the platform identity
> comes from elsewhere), and **ETHcavation**
> was recorded from a Menzi Muck M545 walking excavator, releasing "502 hand-labeled sample
> images with panoptic annotations from construction sites". Neither releases an actuator,
> joint, hydraulic-pressure or force channel. **The machines were instrumented; the forces
> were not shared.**
>
> This is corroborated independently. *OpenConstruction*, a peer-reviewed catalogue of "51
> publicly available visual datasets that span the 2005-2024 period", organises them by a
> modality taxonomy of RGB, thermal, depth, LiDAR point cloud and synthetic — **there is no
> force, torque, tactile or contact row in it at all.**

> [!important] The gap this program sits in
> **No shared dataset of *real-robot, contact-rich* construction manipulation demonstrations
> exists.** Not at DROID scale, not at 10,000, not at 1,000. Be exact about what is and is
> not missing, because three papers in this wiki look like counter-examples and are not:
> [[01-canonical-papers/notes/8-construction/ext|ExT]] has 150,000 episodes for three of its four tasks and 2,000 for the fourth, but
> they are generated in simulation and carry no real contact;
> [[01-canonical-papers/notes/8-construction/liang-lfd|Liang]] uses 3,000 virtual plus 85
> real demonstration *videos* and evaluates in Gazebo; and
> [[01-canonical-papers/notes/8-construction/kindle-jaibot|Kindle]] releases seven datasets,
> but they are accelerometer and pose recordings for deflection compensation, not
> manipulation demonstrations. What none of them provides is force-bearing real-robot
> demonstrations in a shared schema. The OXE `scene type` column takes values like *table top,
> kitchen, hallway, office, pantry, shelf, workshop, outdoors* — no construction, no site,
> no heavy machinery.
>
> The gap is three to four orders of magnitude, and it is a gap in **kind** as much as
> degree: no force channel, no tactile channel, no shared schema. That is what makes a
> curated dataset of a real construction task disproportionately valuable
> ([[06-research-practice/real-world-impact|6. §3]]), and it is why the demonstration-collection
> question in [[04-robotics/teleoperation-demonstration|12]] is a research question here
> rather than an engineering detail.

### 9. Choosing, for this program

| If you are doing | Use | Because |
|---|---|---|
| Contact-rich manipulation policy learning | MuJoCo, or Isaac Lab for scale | speed and stability; check whether you need real contact forces |
| Anything where the contact **force** is the result | Drake (hydroelastic), plus real hardware | a patch and a pressure distribution, not a point force |
| Excavation or terrain | AGX if funded, Chrono::CRM if not | the only documented soil models with citable physics |
| Assembly evaluation | NIST task boards → FurnitureBench → RAMP | artifacts, then real-robot, then construction-framed |
| Deformable construction materials | nothing exists — build and validate | say so in the paper; it is a contribution, not a gap in your work |
| Pretraining a manipulation policy | Open X-Embodiment, DROID, RH20T | and RH20T if you need the force channel |

**The reading this gives you.** Treat each row as a starting hypothesis about tool fit, then validate the deciding physical quantity. For example, a force-sensitive insertion study needs evidence that the modeled contact predicts the measured response at the relevant materials and speeds. A platform can support useful policy iteration while remaining an inadequate instrument for a force-accuracy claim. Record that distinction in the experiment design before interpreting its benchmark score.

### 10. Reading someone else's tooling section

| Question | What a vague answer hides |
|---|---|
| Which simulator, which version? | Isaac Gym results predate a deprecation; MuJoCo contact changed across 3.x |
| Which integrator and step, at what contact stiffness? | A contact force or bounce from a step that does not resolve $\omega=\sqrt{k/m}$ is the integrator's number, not the model's (§3 lab) |
| Were contact forces **simulated** or **measured**? | A simulator's contact force is a modelling choice, not a measurement |
| Sim-only, real-only, or both? | Benchmarks differ on this and the word "benchmark" hides it |
| Which dataset **version**, and which abstract's numbers? | DROID and BridgeData V2 both report two different counts |
| Does the data contain force or tactile at all? | Most does not, and most papers do not say so |
| Is the tool citable? | PyBullet, Drake, Isaac Sim and Genesis have no peer-reviewed paper |

**The reading this gives you.** Reconstruct the path from a physical event to the reported metric. For a contact-force result, ask where force originated, which calibration or model produced it, and whether the evaluation compares against independent measurements. If the same simulation assumption both generates the data and judges the outcome, agreement establishes internal consistency rather than physical validity. The tool name alone cannot resolve that distinction.

### 11. Reading a learned-policy evaluation

The tooling section tells you what the numbers were produced *on*. This section is about the
numbers themselves — the part of a VLA, diffusion-policy or locomotion paper where a
percentage appears and has to be interpreted before it can be compared.

**What "success rate" leaves out.** A single percentage compresses four independent choices,
and two papers reporting 80% may agree on none of them:

| Choice | Why it moves the number |
|---|---|
| **How many trials** | 10 trials resolves nothing below ~10 percentage points. By the rule of three ($3/n$), zero failures in 10 trials is consistent with a true failure rate near **30%** — the exact bound is 26%, and the wiki uses $3/n$ throughout — so "10/10" is *not* evidence of reliability ([[06-research-practice/experimental-design-reproducibility\|3. Experimental Design §4]]) |
| **Initial-state distribution** | were object poses randomized, or reset to the same spot? A policy evaluated from a fixed start is being asked an easier question than one evaluated from a distribution |
| **What counts as done** | a time limit, a pose tolerance, a human judge. The tolerance is often unstated and is frequently the whole difference between two systems |
| **Whether resets and retries count** | a human straightening the object between trials is part of the system; if it is not counted, the reported autonomy is not the measured autonomy |

**Progress and partial credit.** Long-horizon and chained tasks are increasingly scored by
*how far the policy got* rather than whether it finished — stage completion, subtask counts,
or a normalized progress score. This is a reasonable response to binary success being too
coarse, and it introduces a specific failure of comparison: **a high progress score and a
zero success rate are compatible**, and they describe a policy that reliably starts a task and
reliably fails to finish it. The independent evaluation in
[[01-canonical-papers/notes/4-vla/pi0|π0]]'s claim box is exactly this shape. When a paper
leads with progress, look for the completion number; when it leads with completion, look for
whether partial credit was available to the baselines too.

**Seen versus unseen.** Nearly every generalization claim in this literature rests on a split,
and the split's *axis* is the claim: unseen object instances, unseen object categories, unseen
backgrounds, unseen lighting, unseen scenes, unseen embodiments. These are not equally hard
and papers rarely rank them. A method that generalizes across instances of a trained category
is making a much weaker claim than one that generalizes across categories — **read the split
definition before the number**, because the number is only meaningful relative to it.

**First-party versus independent numbers.** Robot-learning results are expensive to reproduce,
so most published comparisons are the authors' own reproductions of someone else's method.
That is not dishonest, and it is also not independent. Where a genuinely third-party
evaluation exists it is worth more than the headline, and the gap between the two is
frequently large — see [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al.]]
(77% in simulation to 23% in six real homes) and π0's independent re-evaluation. **When you
cite a comparison, say whose evaluation it was.**

> [!warning] The three questions that settle most policy tables
> **1. How many trials, and from what initial-state distribution?** **2. Is this simulation,
> a lab testbed, or the deployment environment?** **3. Whose evaluation is it?** A results
> table that does not let you answer all three is reporting a demonstration, not a
> measurement — which is a legitimate contribution, but a different one, and it should not be
> compared against a table that does.

### After reading

- [ ] Name the four status traps in §2 and why each one produces a wrong sentence.
- [ ] Say what MuJoCo and Drake each mean by a contact, and when the difference matters.
- [ ] Give the honest recommendation for terrain simulation and the accuracy caveat attached.
- [ ] State what the OXE schema cannot represent, and why that matters here.
- [ ] Name the three verified absences on this page.
- [ ] From a body's mass and a contact's stiffness, give the contact frequency and the largest stable semi-implicit step in milliseconds, and say what explicit Euler does to one bounce at that step.

### Self-check

1. A paper reports contact forces from an Isaac Sim deformable-object experiment. What is
   the problem?
2. You need to cite the simulator you used. It is Drake. What do you write?
3. Someone quotes "43 million FPS" for Genesis. How do you respond?
4. Your related-work section says "DROID contains 76,000 trajectories". When is that wrong?
5. A reviewer asks why you did not evaluate on a standard construction manipulation
   benchmark. What is your answer?
6. A paper simulates a 40 g tool tip against a contact of stiffness 40,000 N/m at a 5 ms step
   and reports its peak contact forces. What do you check first?

> [!tip]- Answers
> 1. Isaac Sim's own documentation states that particles and deformable bodies **do not support contact reports** — so contact forces cannot be read off a deformable there at all. Either the forces came from somewhere else (a rigid proxy, an inferred estimate) and the paper should say so, or the number is not what it appears to be. Static friction and friction combine mode are also unsupported for deformables, which compounds it.
> 2. The software citation Drake itself provides — a `@misc` with the project name, the development team, and the URL. **There is no peer-reviewed Drake paper**, so inventing a venue would be a fabricated citation. If you used hydroelastic contact specifically, cite the contact-model papers the documentation points to (Castro et al.) alongside the software.
> 3. That the figure came from the December 2024 README, was publicly disputed on methodology — fastest physics setting, one action then 999 no-op steps, self-collisions disabled — that the team published a corrected benchmark adopting the critic's own harness, and that **the claim was removed from the README in May 2026 without a labelled retraction**. The current official materials make no such claim. It should not be quoted as a live number.
> 4. When you are citing the RSS proceedings version, whose abstract says **65,000** trajectories and 86 tasks. 76k/84 is the arXiv abstract's figure. Neither is wrong; quoting one against the other version's citation is. The same trap exists for BridgeData V2 — 60,096 on arXiv, 53,896 in PMLR.
> 5. That none exists, and say it plainly: there is no shared benchmark for on-site construction manipulation — no shared protocol, no shared artifacts, no leaderboard — and the nearest thing, RAMP, is framed on *offsite* construction. The defensible move is to state the absence, borrow the closest evaluation apparatus (NIST task boards for assembly scoring, or RAMP's protocol), and define your own protocol explicitly enough that someone else could rerun it — which is itself an artifact worth releasing. Two cautions on the word. Papers whose titles say "benchmarking" construction tasks now exist — [arXiv:2512.14031](https://arxiv.org/abs/2512.14031) compares VLA and RL policies on construction skills, and Construction Research Congress 2026 lists a humanoid-controller benchmarking paper — but a comparative evaluation inside one paper is not a shared benchmark, which needs a public protocol, public artifacts and results others can add to. And none of them is on an active site. The absence claimed here is that specific thing, and it was last checked against arXiv and Crossref in September 2026.
> 6. The step against the contact frequency. $\omega=\sqrt{40{,}000/0.04}=1000\,\mathrm{rad/s}$, so $\omega\Delta t=5$ — outside even semi-implicit Euler's interval, and without damping explicit Euler has no stable step at all. The §3 lab has a row for exactly this pair: at $0.1\,\mathrm{m/s}$, semi-implicit Euler penetrates $0.5\,\mathrm{mm}$, so it reports a $20\,\mathrm{N}$ peak against the exact $4\,\mathrm{N}$, and it returns 576 times the energy. The contact lasts $3.1\,\mathrm{ms}$, less than one step, so even a solver that stays stable here — an implicit one, say — cannot resolve the force inside it. Ask for the integrator, the step and the contact parameters, and read the forces as the simulation's until the paper shows otherwise.

### Problem set · 과제

Tier A. Using only this page, [[02-foundations/lab-kernel|0.65 Lab Kernel]] and [[02-foundations/lab-plants|0.6 Lab Plants]]. The variant is **a lighter handle**: $m=0.02\,\mathrm{kg}$, half of P3's, against the same two walls ($400$ and $40{,}000\,\mathrm{N/m}$), dropped from the touch at the same $v_0=0.1\,\mathrm{m/s}$, with $d=0$ unless a part says otherwise. Original problems; fill the blanks, do not rewrite the loop.

1. **Draw.** The homework diagram for the variant: the $(\omega\delta,v)$ plane of one bounce on the stiff wall at $\Delta t=1\,\mathrm{ms}$ — the exact half circle, the explicit polygon, the semi-implicit points and the ellipse they sit on — and the $\omega\Delta t$ strip with both walls marked at $1\,\mathrm{ms}$ and each wall's stable step written in milliseconds.
2. **Derive.** (a) $\omega$, the contact time, the exact peak penetration and the exact peak force for each wall. (b) The largest stable semi-implicit step for each wall, and the step a scene holding both walls must use. (c) Step one bounce by hand on the stiff wall at $\Delta t=1\,\mathrm{ms}$ with both integrators: the energy ratio, the peak penetration and the peak force. Does either cross RS1's $10\,\mathrm{N}$ line at $0.1\,\mathrm{m/s}$, and at what $v_0$ would the explicit one? (d) The smallest contact damping that makes explicit Euler stable at $\Delta t=1\,\mathrm{ms}$ on each wall. Did halving the mass change it? (e) With $\zeta=0.1$, the semi-implicit stable step on the stiff wall.
3. **Do.** Fill the `?` in the template ([[02-foundations/lab-kernel|0.65]] has both integrators) and run the undamped sweep for the variant. Report the table — energy ratio and peak penetration for both integrators, $\Delta t\in\{0.1,1,2,5,20\}\,\mathrm{ms}$, both walls — with the unstable cells marked. Then answer: (i) which cells changed from the page's table, and why the $\omega\Delta t$ column alone predicts it; (ii) is semi-implicit Euler's exact 1 on the stiff wall at $1\,\mathrm{ms}$ a property of the integrator? Point to a row of your table that settles it; (iii) the largest step on the grid that is stable for both walls.

```python
# The variant: half of P3's handle, same walls, same drop. Fill the ?; do not rewrite the loop.
import numpy as np
m, v0 = 0.02, 0.1

def drop(k, d, dt, method, t1=0.1):
    delta, v, peak = 0.0, v0, 0.0      # at the touch
    for _ in range(int(round(t1 / dt))):
        f = ?                          # penalty law: zero outside the wall, never pulls
        a = -f / m
        if method == "explicit":
            delta, v = ?, ?            # position moves with the OLD velocity
        else:
            v = ?
            delta = ?                  # position moves with the NEW velocity
        peak = max(peak, delta)
    return (v / v0) ** 2, peak

for k in (400.0, 40000.0):
    w = np.sqrt(k / m)
    for dt in (1e-4, 1e-3, 2e-3, 5e-3, 2e-2):
        rx, px = drop(k, 0.0, dt, "explicit")
        rs, ps = drop(k, 0.0, dt, "semi")
        mark = ?                       # "unstable" outside semi-implicit's interval, else ""
        print(f"{k:6.0f} {dt*1e3:5.1f} {w*dt:7.3f} {rx:10.4g} {rs:10.4g}"
              f" {px*1e3:8.4f} {ps*1e3:8.4f}  {mark}")
```

> [!tip]- Solutions
> 1. Explicit vertices, as $(\omega\delta,v)$ in m/s: $(0,0.1)$, $(0.141,0.1)$, $(0.283,-0.1)$, $(0.141,-0.5)$, then out at $v=-0.7$. Each is $\sqrt3$ times farther out than the last, since $1+(\omega\Delta t)^2=3$. Semi-implicit: $(0,0.1)$, $(0.141,0.1)$, $(0,-0.1)$, then out at $-0.1$, all on the ellipse $v^2+(\omega\delta)^2-\sqrt2\,(\omega\delta)\,v=0.01$. On the strip, the panel sits at $\omega\Delta t=0.141$ and the stiff wall at $1.414$; under the 2, write $14.1\,\mathrm{ms}$ and $1.41\,\mathrm{ms}$.
> 2. (a) Panel: $\omega=\sqrt{400/0.02}=141.4\,\mathrm{rad/s}$, contact $22.2\,\mathrm{ms}$, $v_0/\omega=0.707\,\mathrm{mm}$, $v_0\sqrt{km}=0.283\,\mathrm{N}$. Stiff wall: $1414\,\mathrm{rad/s}$, $2.22\,\mathrm{ms}$, $0.0707\,\mathrm{mm}$, $2.83\,\mathrm{N}$. (b) $2/\omega$ gives $14.1\,\mathrm{ms}$ and $1.41\,\mathrm{ms}$; a scene with both walls needs $\Delta t<1.41\,\mathrm{ms}$. (c) Now $\Delta t\,\omega^2=2000\,\mathrm{s^{-1}}$ and $\Delta t\,v_0=0.1\,\mathrm{mm}$. Explicit, $(\delta,v)$ in mm and m/s: $(0,0.1)\to(0.1,0.1)\to(0.2,-0.1)\to(0.1,-0.5)\to(-0.4,-0.7)$, so the ratio is $49$, the peak $0.2\,\mathrm{mm}$ and the peak force $8\,\mathrm{N}$. (Four steps from the face or inside multiply $v^2+\omega^2\delta^2$ by $3^4=81$; the exit sample at $-0.4\,\mathrm{mm}$ holds $32$ of those in a spring that does not exist, leaving $49$.) Semi-implicit: $(0,0.1)\to(0.1,0.1)\to(0,-0.1)\to(-0.1,-0.1)$, so $1$, $0.1\,\mathrm{mm}$ and $4\,\mathrm{N}$ — a peak $1.41$ times the exact $0.0707\,\mathrm{mm}$, which is the ellipse's widest point, $1/\sqrt{1-\tfrac14\cdot2}$. Neither crosses $10\,\mathrm{N}$ at $0.1\,\mathrm{m/s}$; the explicit peak scales with $v_0$ and crosses at $v_0=0.125\,\mathrm{m/s}$, where the exact peak is still only $3.54\,\mathrm{N}$. (d) $d\ge k\,\Delta t$: $0.4\,\mathrm{N{\cdot}s/m}$ on the panel and $40\,\mathrm{N{\cdot}s/m}$ on the stiff wall, the same as for P3's handle, because the mass cancels. As damping ratios they are $\zeta\ge\omega\Delta t/2=0.071$ and $0.71$, which do depend on the mass. (e) $2(\sqrt{1.01}-0.1)/1414=1.28\,\mathrm{ms}$.
> 3. Blanks: `f = max(0.0, k * delta + d * v) if delta > 0 else 0.0`; `delta, v = delta + dt * v, v + dt * a`; `v = v + dt * a`; `delta = delta + dt * v`; `mark = "unstable" if round(w * dt, 9) >= 2 else ""`. The table, with **bold** for the unstable steps (every explicit cell, and semi-implicit at $\omega\Delta t\ge2$):
>
> | $k$ (N/m) | $\Delta t$ (ms) | $\omega\Delta t$ | ratio, explicit | ratio, semi-implicit | peak, explicit (mm) | peak, semi-implicit (mm) |
> |---:|---:|---:|---:|---:|---:|---:|
> | 400 | 0.1 | 0.014 | **1.045** | 1.000 | 0.715 | 0.707 |
> | 400 | 1 | 0.141 | **1.564** | 1.003 | 0.791 | 0.709 |
> | 400 | 2 | 0.283 | **2.449** | 1.005 | 0.888 | 0.708 |
> | 400 | 5 | 0.707 | **8.266** | 1.129 | 1.250 | 0.750 |
> | 400 | 20 | 2.828 | **529** | **49** | 4.000 | 2.000 |
> | 40,000 | 0.1 | 0.141 | **1.564** | 1.003 | 0.079 | 0.071 |
> | 40,000 | 1 | 1.414 | **49** | 1.000 | 0.200 | 0.100 |
> | 40,000 | 2 | 2.828 | **529** | **49** | 0.400 | 0.200 |
> | 40,000 | 5 | 7.071 | **$2.22\times10^4$** | **2,401** | 1.000 | 0.500 |
> | 40,000 | 20 | 28.28 | **$5.755\times10^6$** | **$6.384\times10^5$** | 4.000 | 2.000 |
>
> (i) Every $\omega\Delta t$ is $\sqrt2$ times the page's, because $\omega\propto1/\sqrt m$, so each cell behaves like the page's cell at $\sqrt2$ times the step. The stiff wall's $2\,\mathrm{ms}$ cell crosses the interval ($2.83>2$) and goes from $9$ to $49$; its $1\,\mathrm{ms}$ explicit cell goes from $16$ to $49$. (ii) No. At $\omega\Delta t=\sqrt2$ each semi-implicit step turns the phase by exactly $90^\circ$ ($\cos\theta=1-\tfrac12\cdot2=0$), so the handle is back on the face at a sample; the panel at $5\,\mathrm{ms}$ ($\omega\Delta t=0.707$) returns $1.129$ with the same integrator. (iii) $1\,\mathrm{ms}$; at $2\,\mathrm{ms}$ the stiff wall is outside the interval.

### Sources

Checked against official sources on **2026-08-22**. Scale figures are from each paper's own
abstract unless marked otherwise; claims resting on absence mean the official pages were
checked and contained nothing.

**Simulators** — [MuJoCo](https://mujoco.readthedocs.io/) (Todorov, Erez & Tassa, IROS 2012, pp. 5026–5033, DOI 10.1109/IROS.2012.6386109); [Isaac Sim](https://developer.nvidia.com/isaac/sim) and [Isaac Lab](https://isaac-sim.github.io/IsaacLab/) (predecessor Orbit: Mittal et al., *RA-L* 8(6), 2023, DOI 10.1109/LRA.2023.3270034); [the Isaac Gym legacy notice](https://developer.nvidia.com/isaac-gym); [Bullet](https://github.com/bulletphysics/bullet3); [Gazebo](https://gazebosim.org/docs/latest/releases/) and the [Classic end-of-life notice](https://classic.gazebosim.org/) (Koenig & Howard, IROS 2004, pp. 2149–2154); [Drake](https://drake.mit.edu/) and its [hydroelastic contact guide](https://drake.mit.edu/doxygen_cxx/group__hydroelastic__user__guide.html); [SAPIEN](https://github.com/haosulab/SAPIEN) (Xiang et al., CVPR 2020, pp. 11094–11104); [Genesis World](https://github.com/Genesis-Embodied-AI/genesis-world), [the benchmark issue](https://github.com/Genesis-Embodied-AI/genesis-world/issues/181) and [the MuJoCo discussion](https://github.com/google-deepmind/mujoco/discussions/2303).

**Terrain** — [agxTerrain user manual](https://www.algoryx.se/documentation/complete/agx/tags/latest/doc/UserManual/source/agxTerrain.html); M. Servin, T. Berglund, S. Nystedt, "A multiscale model of terrain dynamics for real-time earthmoving simulation," *Advanced Modeling and Simulation in Engineering Sciences* 8:11, 2021, DOI 10.1186/s40323-021-00196-3; [Vortex Studio licensing](https://vortexstudio.atlassian.net/wiki/spaces/VSD2511/pages/4607410452); [Project Chrono terrain models](https://api.projectchrono.org/vehicle_terrain.html) and Unjhawala et al., [arXiv:2507.05643](https://arxiv.org/abs/2507.05643) for CRM.

**Benchmarks** — RLBench ([arXiv:1909.12271](https://arxiv.org/abs/1909.12271)); Meta-World (CoRL 2019, PMLR v100); ManiSkill 3 ([arXiv:2410.00425](https://arxiv.org/abs/2410.00425) — the RSS proceedings title differs from the arXiv title); CALVIN ([arXiv:2112.03227](https://arxiv.org/abs/2112.03227)); LIBERO ([arXiv:2306.03310](https://arxiv.org/abs/2306.03310)); FurnitureBench (RSS 2023, DOI 10.15607/RSS.2023.XIX.041); RoboCasa (RSS 2024, DOI 10.15607/RSS.2024.XX.050 — the proceedings title says "Household", arXiv says "Everyday"); [NIST Assembly Task Boards](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) (Kimble et al., *RA-L* 2020, DOI 10.1109/LRA.2020.2965869; deformables: Kimble et al., *Frontiers in Robotics and AI* 9, 2022, DOI 10.3389/frobt.2022.999348); RAMP (*RA-L* 9(1):9–16, 2024, DOI 10.1109/LRA.2023.3330611).

**Datasets** — [Open X-Embodiment](https://robotics-transformer-x.github.io/) (ICRA 2024, [arXiv:2310.08864](https://arxiv.org/abs/2310.08864), CC BY 4.0); DROID (RSS 2024, DOI 10.15607/RSS.2024.XX.120, [arXiv:2403.12945](https://arxiv.org/abs/2403.12945)); BridgeData V2 (CoRL 2023, PMLR v229:1723–1736); [RH20T](https://rh20t.github.io/) (ICRA 2024, [arXiv:2307.00595](https://arxiv.org/abs/2307.00595)); FMB (*IJRR*, DOI 10.1177/02783649241276017); REASSEMBLE ([arXiv:2502.05086](https://arxiv.org/abs/2502.05086)); Rohbau3D (*Scientific Data*, 2025, DOI 10.1038/s41597-025-05827-7, CC BY 4.0); ConRebSeg ([arXiv:2407.09372](https://arxiv.org/abs/2407.09372)); ETHcavation ([arXiv:2410.04250](https://arxiv.org/abs/2410.04250)); the Hilti SLAM Challenge 2023 ([arXiv:2404.09765](https://arxiv.org/abs/2404.09765)); the *OpenConstruction* catalogue ([arXiv:2508.11482](https://arxiv.org/abs/2508.11482)); ConSLAM — ECCV 2022 Workshops, DOI 10.1007/978-3-031-25082-8_21, **and** *J. Comput. Civ. Eng.* 37(3):04023009, 2023, DOI 10.1061/JCCEE5.CPENG-5212.

**Numerical integration** — E. Hairer, C. Lubich and G. Wanner, *Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations*, 2nd ed., Springer Series in Computational Mathematics 31, Springer, 2006 — the standard reference for the symplectic Euler method and the modified energy it conserves. The stable intervals, the energy band and the damping conditions of §3 and the worked case are derived on this page and checked by its lab.

**Within this wiki**

- [[05-construction-robotics/sim-to-real|Sim-to-Real for Field Robots]] — the reality gap these tools sit inside
- [[06-research-practice/experimental-design-reproducibility|Experimental Design & Reproducibility]] — what an evaluation has to hold fixed
- [[06-research-practice/real-world-impact|6. Real-World Impact]] — why a released dataset is worth more here than elsewhere
- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — the tasks these absences are absent for
- [[02-foundations/lab-kernel|0.65 Lab Kernel]] — the two integrators the drop cell compares
- [[04-robotics/contact-force-tactile|9. Contact, Force & Tactile]] — the penalty law the drop cell's wall uses
- [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]] — the other energy source on the same handle, a controller's hold

## 한국어

*[[02-foundations/lab-kernel|0.65 Lab Kernel]]과 [[02-foundations/lab-plants|0.6 Lab Plants]] 위에 선다. 장치 P3를 다시 쓰는 페이지다 — P3의 집은 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]이고, 이 페이지는 그 질량과 벽만 빌린다. 그리고 연구 실무의 모든 페이지가 공유하는 연구 RS1을 다시 적는다. 이 페이지의 대부분은 도구에 관한 읽기 페이지이고, 이 페이지의 대상은 그 가운데 하나뿐인 수치적 주장, 곧 §3의 주장에 랩을 붙인다.*

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고, 대상으로 한 번 끝까지 절에서 한 번의 튕김을 두 적분기로 손으로 전진해 본다. 다음은 §3이다. 같은 낙하를 랩으로 돌리고, 그 표가 시뮬레이터의 "빠르고 안정적"이 무엇을 대가로 치르는지 값을 매긴다. 그다음이 §2(상태 함정)와 §7–§8(빠진 힘 데이터)로, 이 페이지의 인용 가능한 부재들이다. §6과 §11은 남의 벤치마크 숫자를 읽는 날을 위해 남겨 둔다.

### 이 페이지의 대상 · Running object

대상은 둘이다. 연구는 이 트랙의 모든 페이지가 공유하는 RS1이고, 이 페이지가 시뮬레이션하는 것은 P3의 핸들과 RS1의 패널로 만든 페이지 전용 **낙하 셀**(drop cell)이다.

**RS1 — 관통 연구** (연구 실무의 모든 페이지가 다시 적고, 숫자는 바뀌지 않는다). *질문:* 평면 팔이 패널에 접촉할 때, 임피던스 제어(B)가 힘 임계 정지를 단 위치 제어(A)보다 접촉을 더 안전하게 만드는가? 팔은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**, 패널 강성은 **P3** 벽의 $k_w=400\,\mathrm{N/m}$이다. 시행 하나는 패널에 다가가 접촉하는 것이고, 최대 접촉력이 $10\,\mathrm{N}$ 이하이면 성공이다. 파일럿은 **예시용 데이터이며 고정되어 있다.** 가르치기 위한 기록이지 측정이 아니다.

| 팔 | 시행별 최대 접촉력 (N) | 성공 | 평균 (N) | 표본 표준편차 (N) | 중앙값 (N) |
|---|---|---:|---:|---:|---:|
| A — 위치 제어 + 힘 정지 | 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 | 6/10 | 10.66 | 2.414 | 9.85 |
| B — 임피던스 제어 | 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 | 9/10 | 7.50 | 1.356 | 7.30 |

RS1이 채점하는 것은 최대 접촉력이다. RS1의 일부를 시뮬레이터에서 먼저 돌린다면 — 제어기를 튜닝하든 프로토콜을 예행하든 — 그 숫자는 어떤 제어기가 관여하기도 전에 접촉 모델과 적분기에서 나온다. 그것이 §3의 주장이고, 낙하 셀은 그 주장만 떼어 낸다.

**낙하 셀** (페이지 전용, 고정). P3의 핸들이 아무것도 붙지 않은 채 페널티 벽을 만난다. 손이 없고($k_h=b_h=0$), 장치 댐퍼가 없고($b=0$), 제어기도 없다. 벽 밖에서는 아무 힘도 작용하지 않으므로, 핸들이 얻거나 잃는 에너지는 모두 접촉이나 적분기의 몫이다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $m$ | $0.04\,\mathrm{kg}$ | 핸들 질량 — P3의 값 |
| $k$ | $400\,\mathrm{N/m}$ | 패널 — RS1의 패널, 곧 P3의 $k_w$ |
| $k$ | $40{,}000\,\mathrm{N/m}$ | 단단한 변형 — 패널의 100배, 딱딱한 표면을 대신하는 값(예시) |
| $d$ | $0$ | 기본 접촉 감쇠 — 적분기만 떼어 보는 경우 |
| $d$ | $0.8$과 $8\,\mathrm{N{\cdot}s/m}$ | 감쇠 경우, 패널과 단단한 벽에서 — 둘 다 감쇠비 $\zeta=0.1$ |
| $v_0$ | $0.1\,\mathrm{m/s}$ | 닿는 순간의 접근 속도 — [[04-robotics/haptics-teleoperation/rendering-sampling-stability\|24.4]]의 대표 접근 속도 |
| $\Delta t$ | 스윕 | 시뮬레이터의 스텝. 계산 절은 $1\,\mathrm{ms}$ |

벽 법칙은 [[04-robotics/contact-force-tactile|9. 접촉 §3]]의 페널티 모델이고, 침투 $\delta=x-x_w$는 P3의 벽면 $x_w=0.030\,\mathrm{m}$에서 잰다($+x$가 벽 안쪽).

$$F=-\max\big(0,\ k\delta+d\dot\delta\big)\ \ (\delta>0),\qquad F=0\ \ (\delta\le0)$$

그래서 벽은 핸들을 밀어내기만 하고 끌어당기지 않는다. 낙하는 닿는 순간, 곧 $\delta=0$, $\dot\delta=v_0$에서 시작하므로 접촉이 정확히 샘플 위에서 시작된다. 그래야 계산 절을 손으로 전진할 수 있고, 랩의 표가 핸들이 두 샘플 사이 어디에 도착했는지에 좌우되지 않는다. 그 위치가 얼마나 중요할 수 있는지는 §3이 범위로 묶는다.

**왜 RS1의 팔이 아니라 이 물체인가.** 접촉에 필요한 스텝은 $\sqrt{m/k}$에 비례하므로(계산 절 4단계), 장면 전체의 스텝은 가장 단단한 접촉 위의 가장 가벼운 물체가 정한다. 카탈로그 자세의 P2 말단은 작업공간 관성이 $x$ 방향 $1\,\mathrm{kg}$, $y$ 방향 $2\,\mathrm{kg}$이므로([[02-foundations/lab-plants|0.6]]), 같은 패널에 대해 패널이 어느 쪽을 향하느냐에 따라 $\sqrt{400/1}=20$ 또는 $\sqrt{400/2}=14.1\,\mathrm{rad/s}$로 울린다. P3의 핸들은 $100\,\mathrm{rad/s}$로 울린다. 핸들 쪽이 더 어려운 경우이므로, 돌려 볼 가치가 있는 것도 핸들이다.

*범위: 이 페이지는 시뮬레이터·벤치마크·데이터셋을 고르고 인용하는 법을 가르치고, 낙하 셀에서는 시뮬레이터의 접촉 모델과 스텝이 왜 그것이 보고하는 접촉력을 결정하는지를 가르친다. 접촉 솔버를 만드는 법은 가르치지 않는다(상보성의 정의는 [[04-robotics/contact-force-tactile|9. 접촉 §1]]에 있고, 솔버 내부는 여기서 다루지 않는다). 제어기의 zero-order hold가 새게 하는 에너지도 아니다. 그것은 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]이고, 경계가 비슷해 보이는 다른 에너지원이다. RS1 파일럿의 통계도 아니다. 그것은 [[06-research-practice/experimental-design-reproducibility|3. 실험 설계와 재현성]]의 몫이다.*

### 과제가 그릴 그림 · Homework diagram

그림 하나, 두 부분. 과제는 더 가벼운 핸들로 같은 그림을 요구한다.

<svg viewBox="0 0 560 486" style="max-width:100%;height:auto" role="img" aria-label="위상 평면 위의 한 번의 튕김: 정확한 반원, 바깥으로 나선을 그리는 명시적 오일러, 기울어진 타원 위의 반암시적 오일러. 아래는 오메가 곱하기 스텝의 안정 구간">
  <defs><marker id="dcK" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor" opacity="0.07"><rect x="150" y="48" width="150" height="282"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.6">
    <line x1="30" y1="150" x2="300" y2="150"/>
    <line x1="150" y1="48" x2="150" y2="330"/>
  </g>
  <g stroke="currentColor" stroke-width="2.2" fill="none"><path d="M150,110 A40,40 0 0 1 150,190"/></g>
  <g stroke="currentColor" stroke-width="1" fill="none" stroke-dasharray="2 3" opacity="0.9"><ellipse cx="150" cy="150" rx="56.6" ry="32.7" transform="rotate(-45 150 150)"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="7 4"><path d="M150,110 L190,110 L230,150 L230,230 L150,310"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <path d="M150,310 L40,310" marker-end="url(#dcK)"/>
    <path d="M110,190 L40,190" marker-end="url(#dcK)"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none">
    <rect x="145" y="105" width="10" height="10"/><rect x="185" y="105" width="10" height="10"/>
    <rect x="225" y="145" width="10" height="10"/><rect x="225" y="225" width="10" height="10"/>
    <rect x="145" y="305" width="10" height="10"/>
  </g>
  <g fill="currentColor">
    <circle cx="150" cy="110" r="3.2"/><circle cx="190" cy="110" r="3.2"/><circle cx="190" cy="150" r="3.2"/>
    <circle cx="150" cy="190" r="3.2"/><circle cx="110" cy="190" r="3.2"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="30" y="24" font-weight="600">단단한 벽, &#916;t = 1 ms, &#969;&#916;t = 1</text>
    <text x="156" y="44">v (m/s)</text>
    <text x="254" y="143">&#969;&#948; (m/s)</text>
    <text x="108" y="64">벽 밖</text>
    <text x="158" y="64">벽 안</text>
    <text x="44" y="303">4v<tspan dy="3.5">0</tspan><tspan dy="-3.5">로 떠남</tspan></text>
    <text x="44" y="183">v<tspan dy="3.5">0</tspan><tspan dy="-3.5">로 떠남</tspan></text>
    <text x="104" y="106">v<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  </g>
  <g stroke="currentColor" fill="none">
    <line x1="318" y1="66" x2="344" y2="66" stroke-width="2.2"/>
    <line x1="318" y1="98" x2="344" y2="98" stroke-width="1.4" stroke-dasharray="7 4"/>
    <rect x="326" y="93" width="10" height="10" stroke-width="1.3"/>
    <line x1="318" y1="146" x2="344" y2="146" stroke-width="1" stroke-dasharray="2 3"/>
  </g>
  <g fill="currentColor"><circle cx="331" cy="146" r="3.2"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="352" y="70">정확한 해: 반지름 v<tspan dy="3.5">0</tspan><tspan dy="-3.5">인 반원</tspan></text>
    <text x="352" y="102">명시적 오일러: 스텝마다</text>
    <text x="352" y="116">&#8730;2배씩 멀어짐, E &#215; 16</text>
    <text x="352" y="150">반암시적 오일러: E&#771;의</text>
    <text x="352" y="164">타원 위, E &#215; 1</text>
    <text x="318" y="198">에너지 = 원점까지 거리</text>
    <text x="318" y="212">제곱의 절반</text>
    <text x="318" y="242">최대 힘: 정확한 값 4 N,</text>
    <text x="318" y="256">반암시적 4 N, 명시적 8 N</text>
  </g>
  <g fill="currentColor" opacity="0.18"><rect x="60" y="392" width="300" height="16"/></g>
  <g stroke="currentColor" stroke-width="1.2">
    <line x1="60" y1="400" x2="510" y2="400"/>
    <line x1="60" y1="392" x2="60" y2="408"/><line x1="210" y1="394" x2="210" y2="406"/>
    <line x1="360" y1="388" x2="360" y2="412"/><line x1="510" y1="394" x2="510" y2="406"/>
  </g>
  <g fill="currentColor"><circle cx="75" cy="400" r="4"/><circle cx="210" cy="400" r="4"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="64" y="384">반암시적 안정: 0 &lt; &#969;&#916;t &lt; 2</text>
    <text x="404" y="384">둘 다 불안정</text>
    <text x="518" y="404">&#969;&#916;t</text>
    <text x="60" y="424" text-anchor="middle">0</text><text x="210" y="424" text-anchor="middle">1</text>
    <text x="360" y="424" text-anchor="middle">2</text><text x="510" y="424" text-anchor="middle">3</text>
    <text x="60" y="442">패널, 1 ms: 0.1</text>
    <text x="196" y="442">단단한 벽, 1 ms: 1</text>
    <text x="60" y="460">2는 패널에서 20 ms, 단단한 벽에서 2 ms</text>
    <text x="60" y="478" font-style="italic">d = 0인 명시적 오일러는 어떤 &#969;&#916;t에서도 안정하지 않다 &#8212; 띠 안에서도</text>
  </g>
</svg>

그림이 맞혀야 할 것이 넷이고, 각각이 물리에 대한 주장이다.
**축을 에너지가 거리가 되도록 잡는다.** 가로에 $\omega\delta$, 세로에 $v$, 둘 다 m/s. 그러면 단위 질량당 에너지 $\tfrac12(v^2+\omega^2\delta^2)$는 원점까지 거리 제곱의 절반이므로, 정확한 튕김은 $(0,v_0)$에서 $(0,-v_0)$까지 반지름 $v_0$인 반원이다. 원 위에서 떠난다는 것은 들어온 에너지를 그대로 갖고 떠난다는 뜻이다.
**명시적 오일러는 커지는 다각형이다.** 꼭짓점마다 앞의 것보다 $\sqrt{1+(\omega\Delta t)^2}$배 — 여기서는 $\sqrt2$배 — 멀어지므로, 핸들은 들어올 때보다 빨리 떠난다.
**반암시적 오일러는 기울어진 타원 위에 있다.** 점들이 원을 벗어났다가 돌아온다. 이 스텝이 보존하는 것은 참 에너지가 아니라 3단계의 수정 에너지 $\tilde E$이기 때문이다. 점들을 지나는 타원을 그린다.
**아래의 띠.** 0부터 3까지의 $\omega\Delta t$ 축에 반암시적 오일러의 안정 구간 $0<\omega\Delta t<2$를 칠하고, $d=0$에서 명시적 오일러에는 안정 구간이 없다고 적는다. $\Delta t=1\,\mathrm{ms}$에서의 두 벽 — $0.1$과 $1$ — 을 표시하고, 2 아래에 그것이 각 벽에서 몇 밀리초인지 적는다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이고, 고정된 숫자로 한 번 끝까지 계산한다. 접촉 진동수, 각 적분기가 한 스텝에 하는 일, 밀리초로 쓴 안정 스텝, 손으로 전진한 한 번의 튕김, 그리고 접촉 감쇠가 바꾸는 것. 과제는 질량을 절반으로 줄여 같은 단계를 밟는다.

**1단계 — 접촉 진동수.** $d=0$일 때 벽 안의 핸들은 $m\ddot\delta=-k\delta$를 따른다. [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]의 감쇠 없는 질량–스프링이다. 닿는 순간부터

$$\delta(t)=\frac{v_0}{\omega}\sin\omega t,\qquad \omega=\sqrt{k/m}$$

이다. $\delta(0)=0$과 $\dot\delta(0)=v_0$이 진폭을 $v_0/\omega$로 정하기 때문이다. 벽은 밀기만 하므로 반 주기만 일어난다. 접촉은 $\pi/\omega$ 동안 이어지고, 핸들은 가져온 에너지 그대로 $-v_0$로 떠난다.

| | 패널, $k=400$ | 단단한 벽, $k=40{,}000$ |
|---|---:|---:|
| $\omega=\sqrt{k/m}$ | $100\,\mathrm{rad/s}$ | $1000\,\mathrm{rad/s}$ |
| 접촉 시간 $\pi/\omega$ | $31.4\,\mathrm{ms}$ | $3.14\,\mathrm{ms}$ |
| 최대 침투 $v_0/\omega$ | $1.00\,\mathrm{mm}$ | $0.100\,\mathrm{mm}$ |
| 최대 힘 $kv_0/\omega=v_0\sqrt{km}$ | $0.40\,\mathrm{N}$ | $4.0\,\mathrm{N}$ |

마지막 행이 RS1이 채점하는 양이고, 접근만큼이나 $k$에 달려 있다. 같은 낙하가 단단한 벽에서는 열 배 높게 솟는다. $\sqrt{100}=10$이기 때문이다.

**2단계 — 명시적 오일러는 접촉 중 매 스텝 에너지를 더한다.** 단위 질량당 에너지를 $\tfrac12(v^2+\omega^2\delta^2)$로 둔다. 명시적 스텝 한 번([[02-foundations/lab-kernel|0.65 §2]])은 $\delta'=\delta+\Delta t\,v$, $v'=v-\Delta t\,\omega^2\delta$이다. 제곱해서 더하면

$$v'^2+\omega^2\delta'^2=\big(1+(\omega\Delta t)^2\big)\big(v^2+\omega^2\delta^2\big)$$

이다. 교차항 $\mp2\Delta t\,\omega^2\delta v$가 정확히 상쇄되기 때문이다. 그러므로 벽면이나 그 안에서 시작하는 스텝은 위상이 어떻든, 스텝이 얼마든 그 에너지를 $1+(\omega\Delta t)^2>1$배 한다. 벽 밖에 떨어지는 마지막 스텝만 그 곱의 일부를 잃는다. 벽면 너머로 늘어난 스프링은 존재하지 않기 때문이다. 이것을 멈출 만큼 작은 스텝은 없다. 스텝을 줄이면 한 번의 이득은 작아지지만 그만큼 여러 번 얻는다. 접촉 한 번은 약 $\pi/(\omega\Delta t)$ 스텝이므로, $\omega\Delta t$가 작을 때 이득이 쌓여 튕김 한 번에 약 $e^{\pi\omega\Delta t}$배가 된다.

**3단계 — 반암시적 오일러는 $\omega\Delta t<2$에서만 안정하다.** 반암시적 스텝([[02-foundations/lab-kernel|0.65 §3]])은 속도를 먼저 갱신하고 새 속도로 움직인다. $v'=v-\Delta t\,\omega^2\delta$, 다음에 $\delta'=\delta+\Delta t\,v'$. $(\delta,v)$에 작용하는 행렬로 쓰면

$$\begin{pmatrix}\delta'\\ v'\end{pmatrix}=\begin{pmatrix}1-(\omega\Delta t)^2 & \Delta t\\ -\omega^2\Delta t & 1\end{pmatrix}\begin{pmatrix}\delta\\ v\end{pmatrix}$$

이므로 행렬식은 정확히 $1$, 대각합은 $2-(\omega\Delta t)^2$이고, 고유값은 $\lambda^2-\big(2-(\omega\Delta t)^2\big)\lambda+1=0$의 해다. 두 고유값의 곱은 $1$이다. 그러니 둘은 단위원 위의 복소 켤레 쌍이거나, 실수이면서 하나가 단위원 밖에 있다. 복소수가 되는 것은 정확히 $\lvert2-(\omega\Delta t)^2\rvert<2$일 때이고, 양의 스텝에서 이는

$$0<\omega\Delta t<2$$

이다. [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]의 이산시간 판정으로 이것이 안정 구간이다. 고유값이 단위원 위에 있고 서로 다르므로, 모델링하는 감쇠 없는 스프링처럼 유계이되 감쇠하지 않는다. $\omega\Delta t=2$에서는 두 고유값이 $-1$에서 만나고 에너지가 선형으로 자란다. 구간 안에서 이 스텝은 가까운 에너지 하나를 정확히 보존한다.

$$\tilde E=\tfrac12 mv^2+\tfrac12 k\delta^2-\tfrac12 k\,\Delta t\,\delta v$$

스텝을 대입하면 확인할 수 있고, 이것이 $(\delta,v)$ 평면의 닫힌 타원이 되는 것은 $(\omega\Delta t)^2<4$일 때뿐이다. 같은 경계다. 그래서 반암시적 오일러의 참 에너지는 표류하지 않고 $\tilde E$ 주위에서 흔들린다.

**4단계 — 밀리초로 쓴 경계.** 구간은 $\Delta t<2/\omega=2\sqrt{m/k}$이다.

- **패널**: $2/100=20\,\mathrm{ms}$. 햅틱 스텝 $1\,\mathrm{ms}$에서는 $\omega\Delta t=0.1$이고 접촉 한 번이 약 31스텝이다.
- **단단한 벽**: $2/1000=2\,\mathrm{ms}$. $1\,\mathrm{ms}$에서는 $\omega\Delta t=1$이고 접촉 한 번이 세 스텝이다.

접촉이 100배 단단해지면 스텝은 10배 작아져야 한다. 경계가 $1/\sqrt k$로 줄기 때문이다. 안정하다고 정확한 것은 아니다. 경계에서는 접촉 전체가 $\pi/2\approx1.6$스텝이다.

**5단계 — 손으로 한 번의 튕김: 단단한 벽, $\Delta t=1\,\mathrm{ms}$.** 여기서 $\omega\Delta t=1$이다. 반암시적 오일러의 구간 안이고, 명시적 오일러의 스텝당 인수가 정확히 $1+1^2=2$가 되는 곳이다. $\Delta t\,\omega^2=10^{-3}\cdot10^{6}=1000\,\mathrm{s^{-1}}$, $\Delta t\,v_0=0.1\,\mathrm{mm}$로 $(\delta,v)=(0,\ 0.1\,\mathrm{m/s})$에서 시작한다.

| 스텝 | 명시적 $\delta$ (mm) | 명시적 $v$ (m/s) | 반암시적 $\delta$ (mm) | 반암시적 $v$ (m/s) |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0.1 | 0 | 0.1 |
| 1 | 0.1 | 0.1 | 0.1 | 0.1 |
| 2 | 0.2 | 0 | 0.1 | 0 |
| 3 | 0.2 | −0.2 | 0 | −0.1 |
| 4 | 0 | −0.4 | −0.1, 벽 밖 | −0.1 |
| 5 | −0.4, 벽 밖 | −0.4 | | |

1스텝은 둘 다 자유 스텝이다. $\delta=0$에서 힘이 0이기 때문이다. 둘이 갈라지는 것은 2스텝이다. 둘 다 $v=0.1-1000\cdot0.0001=0$을 계산하지만, 명시적 오일러는 이전 속도로 $\delta$를 옮겨 $0.2\,\mathrm{mm}$에 가고, 반암시적 오일러는 새 속도로 옮겨 $0.1\,\mathrm{mm}$에 머문다.

- **명시적**: 핸들이 $0.4\,\mathrm{m/s}$로 떠나므로 $E_{\text{out}}/E_{\text{in}}=(0.4/0.1)^2=16=2^4$이다. 벽면이나 그 안에서 시작한 네 스텝마다 2배씩이다. 최대 침투 $0.2\,\mathrm{mm}$, 최대 힘 $40{,}000\times0.0002=8\,\mathrm{N}$으로 정확한 값 $4\,\mathrm{N}$의 두 배다.
- **반암시적**: 핸들이 $0.1\,\mathrm{m/s}$로 떠나므로 $E_{\text{out}}/E_{\text{in}}=1$이다. 최대 침투 $0.1\,\mathrm{mm}$, 최대 힘 $4\,\mathrm{N}$으로 정확한 값과 같다. 1스텝에서 단위 질량당 참 에너지는 $\tfrac12(0.1^2+0.1^2)$로 들어온 양의 두 배였다 — 그것이 흔들림이다 — 그동안 $\tilde E$는 내내 $\tfrac12\cdot0.1^2$을 지켰다.

그 정확한 1은 적분기가 아니라 이 스텝의 성질이다. $\omega\Delta t=1$에서 반암시적 스텝은 위상을 정확히 $60^\circ$씩 돌리므로($\cos\theta=1-\tfrac12(\omega\Delta t)^2=\tfrac12$), 핸들이 정확히 샘플 위에서 벽면으로 돌아온다. 일반적인 경우는 §3의 랩이 보여 준다. 같은 스텝의 패널($\omega\Delta t=0.1$)에서는 튕김이 32스텝이라 손으로는 너무 많다. 2단계는 명시적 오일러가 $\approx e^{0.1\pi}=1.37$이라고 예측하고, 루프는 $1.372$, 반암시적 오일러는 $1.002$를 준다.

RS1의 선은 $10\,\mathrm{N}$에 있다. 이 낙하의 모든 것이 $v_0$에 선형이므로, 같은 낙하를 $0.15\,\mathrm{m/s}$로 하면 정확한 최대 힘은 $6\,\mathrm{N}$ — RS1의 규칙으로 성공 — 인데, $1\,\mathrm{ms}$의 명시적 오일러는 $12\,\mathrm{N}$, 곧 실패를 보고한다. 제어기는 바뀌지 않았다. 시행을 채점한 것은 적분기다.

**6단계 — 접촉 감쇠가 하는 일.** 벽에 댐퍼 $d$를 준다. 세 가지가 바뀌고, 물리는 첫째뿐이다.

*튕김이 에너지를 잃는다.* [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]의 감쇠비 $\zeta=d/(2\sqrt{km})$로 쓰면, 선형 스프링–댐퍼는 속도의 $e=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$만큼을 돌려준다. 그 절의 오버슈트와 같은 지수다. 낙하 셀의 감쇠 경우는 두 벽 모두 $\zeta=0.8/(2\sqrt{400\cdot0.04})=8/(2\sqrt{40{,}000\cdot0.04})=0.1$이므로, 이 식은 $e=0.729$, 에너지 비 $e^2=0.532$를 준다. 벽 법칙의 $\max(0,\cdot)$는 힘이 0이 되는 즉시 핸들을 놓아 주어 댐퍼가 핸들을 다시 끌어당길 틈이 없으므로, 낙하 셀의 정확한 비는 조금 더 높다. 법칙을 정확히 풀고 잘게 쪼갠 스텝으로 확인한 값이 $0.554$($e=0.744$)다.

*댐퍼가 스텝 값을 치르면 명시적 오일러도 안정해질 수 있다.* 가볍게 감쇠된 접촉($\zeta<1$)에서 감쇠 있는 명시적 스텝의 고유값은 절댓값 제곱이 $1-2\zeta\,\omega\Delta t+(\omega\Delta t)^2$이고, 이것이 1 이하인 것은 정확히 $\omega\Delta t\le2\zeta$일 때다. $\zeta$와 $\omega$를 대입하면

$$d\ \ge\ k\,\Delta t$$

가 되고 질량이 사라진다. $\omega\Delta t$와 $2\zeta$가 같은 인수 $1/\sqrt m$을 갖기 때문이다. 패널: $d=0.8\ge400\cdot10^{-3}=0.4$이므로 $1\,\mathrm{ms}$에서 안정하고, $2\,\mathrm{ms}$까지 안정하다. 단단한 벽: $d=8<40$이라 $1\,\mathrm{ms}$에서도 여전히 불안정하고, $\Delta t\le0.2\,\mathrm{ms}$가 필요하다. 이 꼴은 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]에 있는 홀드의 경계 $K\le2b/T$ — 강성 곱하기 주기를 댐퍼가 갚는다 — 를 닮았지만, 에너지원은 홀드가 아니라 적분기다. 둘을 혼동하면 안 되는 이유는 그 페이지의 비예가 말한다.

*반암시적 오일러의 구간이 좁아진다.* 랩처럼 감쇠력을 이전 속도로 계산하면 구간은 $\omega\Delta t<2(\sqrt{1+\zeta^2}-\zeta)$가 되고, $\zeta=0.1$에서 $1.81$이다. 패널에서 $18.1\,\mathrm{ms}$, 단단한 벽에서 $1.81\,\mathrm{ms}$. 감쇠는 심플렉틱 스텝에 더 큰 $\Delta t$를 사 주지 않는다. 오히려 조금 깎는다.

파이썬으로 확인했다. 영어 절의 코드가 5단계의 튕김을 두 적분기로 전진하고 비를 출력한다. 명시적 오일러는 `E_out/E_in = 16.000000`, 최대 침투 `0.2000 mm`, `8.000 N`, 반암시적 오일러는 `1.000000`, `0.1000 mm`, `4.000 N`으로 손으로 구한 값과 같다. §3의 랩은 같은 루프를 스윕으로 돌린다.

### 1. 이 페이지의 용도

모든 프로젝트 초반에 나오고 대개 엉성하게 답해지는 질문 셋: *어느 시뮬레이터, 어느 벤치마크,
어느 데이터?* 보통은 옆자리 사람이 쓰던 것으로 답한다. 이 페이지는 각 도구가 무엇을 표현할 수
있고 없는가로 답한다 — 접촉이 많은 건설 조작에서는 그것이 결정적인 질문이기 때문이다.

여기서 가장 쓸모 있는 내용은 추천이 아니다. **부재**들이다: 있을 법한데 없는 것들. 각각이
인용 가능한 공백이다.

예를 들어 벽 닦기 실험에는 접촉 모델과 실제 힘 피드백 기록이 모두 필요할 수 있다. 시뮬레이터는 접촉 가정 아래의 예측을 준다. 데이터셋에는 수집한 채널만 있다. 벤치마크는 과제와 채점 규칙을 준다. 어느 하나가 나머지 둘을 자동으로 제공하지는 않는다.

**여기서 얻는 독법.** 도구를 고르기 전에 연구 주장을 결정할 변수를 적는다. 도구가 이를 표현하는지, 측정하는지, 가정만 하는지 확인한다. 이 순서를 따르면 플랫폼을 고른 뒤 관측으로 원하는 질문에 답할 수 없음을 뒤늦게 깨닫는 일을 줄인다.

### 2. 시뮬레이터 — 범용

| 시뮬레이터 | 유지 주체 | 라이선스 | 정본 논문 | 가장 잘하는 한 가지 |
|---|---|---|---|---|
| **MuJoCo** | Google DeepMind | Apache-2.0 | Todorov, Erez & Tassa, IROS 2012 | 빠르고 안정적인 관절 동역학, 해석적으로 역산 가능 |
| **Isaac Sim** / **Isaac Lab** | NVIDIA | 아래 단서 참고 / BSD-3 | 없음 / Orbit, RA-L 2023 | GPU 병렬 수천 환경, RTX 실사 센서 |
| **PyBullet** | 커뮤니티 | Zlib | **없음** (`@misc`를 인용) | 쉽고 성숙하며 CPU 친화적 |
| **Gazebo** (`gz`) | Open Source Robotics Alliance | Apache-2.0 | Koenig & Howard, IROS 2004 | ROS 2 통합, 센서, 헤드리스 CI |
| **Drake** | MIT 출발, Toyota Research Institute 주도 | BSD-3 | **없음** (`@misc`를 인용) | **하이드로일래스틱 접촉** — 압력 분포를 가진 접촉면 |
| **SAPIEN** | UCSD SU Lab / Hillbot | 아래 단서 참고 | Xiang et al., CVPR 2020 | PartNet-Mobility 기반 부품 수준 관절 물체 |

이 표에서 소리 내어 말해야 할 것이 넷 있다. 각각이 활자로 틀리는 방법이기 때문이다.

> [!warning] 상태에 관한 함정 넷
> - **Isaac Gym은 지원 종료되었다.** NVIDIA 자신의 페이지가 말한다: "This is legacy software.
>   Developers may download and continue to use it, but it is no longer supported."
>   `IsaacGymEnvs`와 `OmniIsaacGymEnvs`는 둘 다 읽기 전용으로 보관되었다(GitHub은 보관 날짜를 공개하지 않는다). Isaac Lab을 쓰라.
> - **"Isaac Sim은 Apache 2.0"이라고 단서 없이 쓰면 안 된다.** 같은 LICENSE 파일이, 빌드하거나
>   사용하려면 별도의 NVIDIA 계약이 적용되는 추가 구성 요소 — Omniverse Kit SDK와 3D 자산 —
>   가 필요하다고 밝힌다.
> - **Gazebo Classic은 2025-01-29에 수명이 끝났고** 저장소는 보관 처리되었다. "Ignition"은
>   역사로만 등장해야 한다: `gz`로의 개명은 Open Robotics의 표현으로 "'Ignition'이라는 이름
>   사용에 관한 상표 문제" 때문이었다.
> - **SAPIEN의 라이선스는 실제로 모호하다**: 저장소 LICENSE는 Apache-2.0, PyPI 메타데이터는
>   MIT, GitHub 탐지기는 NOASSERTION이라고 한다. 하나를 고르지 말고 모호함을 진술하라.

**PyBullet·Drake·Isaac Sim·Genesis에는 심사받은 논문이 없다.** 넷 다 공식적으로 `@misc`나 URL을
인용하라고 안내한다. 그래도 괜찮다 — 다만 "Drake [소프트웨어 인용]을 사용했다"라고 쓰고,
없는 venue를 지어내지 마라.

### 3. 실제로 중요한 축: 접촉을 어떻게 모델링하는가

이 프로그램에서 시뮬레이터 사이의 흥미로운 차이는 속도가 아니다. 각각이 접촉을 *무엇으로
여기는가*다.

- **MuJoCo**는 타원 또는 각뿔 마찰 원뿔(쿨롱 마찰이 허용하는 접촉력의 집합.
  [[04-robotics/contact-force-tactile|접촉·힘·촉각 §2]] 참고)로 부드러운 볼록 최적화를 푼다. 그리고 문서가 명시적으로
  제약 위반이 설계상 허용된다고 밝힌다 — 상보성 해법(complementarity solver, "간극이 0이거나 접촉력이 0"을 정확히 강제하는 해법.
  [[04-robotics/contact-force-tactile|접촉·힘·촉각 §1]] 참고)이 아니다. 그것이
  빠르고 안정적인 이유이자, MuJoCo의 접촉력이 로드셀이 읽을 힘이 아닌 이유다.
- **Drake의 하이드로일래스틱 접촉**은 반대로 간다: 강체가 "약간의 변형 가능한 층을 가진 것처럼
  살짝 파고들어", 점 힘이 아니라 근사적인 접촉 *면*과 *압력 분포*를 만들고, 비볼록 기하에서도
  시간적으로 일관된 힘을 준다. 문서화된 한계도 그만큼 분명하다 — 두 강체 하이드로일래스틱 기하
  사이에는 접촉면을 만들 수 없고, "모델이 상태를 도입하지 않으므로 진짜 변형을 모델링할 수
  없어" 접선 방향 컴플라이언스와 짧은 시간 규모의 파동이 빠진다.
- **PhysX**는 Isaac 아래에서, 처리량에 맞춰 조율된 게임 엔진 계보다.

MuJoCo 3.x가 접촉이 많은 작업 쪽으로 움직이고 있는 것은 추적할 가치가 있다: 3.0이 Flex 변형체를
도입했고, 3.3.0이 네이티브 볼록 충돌을 기본값으로 만들었으며, **3.3.5가 네이티브 SDF 지원과
함께 접촉 센서와 촉각 센서를 추가했다** — 뒤의 것은 "주어진 점들에서 두 물체 사이의 침투
깊이를 측정"한다. [[04-robotics/tactile-visuotactile|촉각 조작]] 프로젝트에는 실질적인 변화다.

**이 페이지의 대상으로 본 주장.** 위의 항목들은 한 질문에 대한 세 가지 답이고, 낙하 셀은 그 질문을 숫자로 묻는다. *두 시간 스텝 사이에서 접촉은 무엇을 해도 되는가?* 페널티 스프링의 답은 "겹친 만큼 되민다"이고, 계산 절은 그 답을 끝까지 따라갔다. 스텝이 분해해야 하는 접촉 진동수, 그리고 분해된 접촉이 에너지를 지키는지, 얻는지, 물체를 튕겨 내 버리는지를 정하는 적분기. 정의 넷이 이 논증을 어느 시뮬레이터에나 옮길 수 있게 하고, 그다음 랩이 그것을 돌린다.

> **접촉 진동수의 정의.** 유연 접촉 위 물체의 **접촉 진동수**(contact frequency)는 *각속도*이고 단위는 rad/s다. 물체와 접촉이라는 한 쌍의 성질이지, 표면만의 것도 물체만의 것도 아니다. 정의 조건 셋. 첫째, **접촉은 강성 $k$인 스프링으로 모델링된다.** 페널티나 다른 유연 법칙이 그렇다([[04-robotics/contact-force-tactile|9. 접촉 §3]]). 강체 상보성 접촉에는 강성이 없으므로 접촉 진동수도 없다. 둘째, 질량은 물체의 **접촉 법선 방향 유효 질량** $m$이다. 셋째, 이 진동수는 스프링이 밀 뿐 아니라 당길 수도 있을 때 그 쌍이 울릴 진동수이고, 단방향 접촉은 그 반 주기만 겪는다.
>
> $$\omega=\sqrt{k/m},\qquad t_c=\pi/\omega$$
>
> $t_c$는 감쇠 없는 튕김의 지속 시간이다. [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]의 고유 진동수를 접촉에 맞춘 것이고, 그래서 시뮬레이터의 스텝이 분해해야 할 시간 척도를 정한다.
>
> - **예**: 낙하 셀 — 패널에서 $100\,\mathrm{rad/s}$와 $31.4\,\mathrm{ms}$, 단단한 벽에서 $1000\,\mathrm{rad/s}$와 $3.14\,\mathrm{ms}$.
> - **비예**: "패널의 진동수". 같은 $400\,\mathrm{N/m}$ 패널이 P2의 $1\,\mathrm{kg}$ 말단에 대해서는 $20\,\mathrm{rad/s}$, P3의 핸들에 대해서는 $100\,\mathrm{rad/s}$로 울린다. 숫자는 쌍의 것이다.
> - **비예**: 같은 핸들에서 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] 계산 절의 $141\,\mathrm{rad/s}$. 그 루프에는 손의 스프링이 들어 있어 $\sqrt{(k_h+k_w)/m}$이다. 접촉 진동수는 벽의 스프링만의 것이다.
> - **왜 중요한가**: 접촉 파라미터를 시간 스텝 요구 조건, 곧 반암시적 오일러의 $\Delta t<2/\omega$로 바꾼다. 그리고 장면 전체의 스텝을 가장 단단한 접촉 위의 가장 가벼운 물체가 정하는 이유다.

> **안정 스텝의 정의.** 시간 스텝 $\Delta t$가 어떤 접촉 위의 어떤 적분기에 대해 **안정**(stable)하다는 것은, 그 적분기의 한 스텝 사상이 접촉 중 동역학의 모든 궤적을 유계로 유지한다는 뜻이다. (적분기, 스텝, 접촉) *세 짝*의 성질이지 적분기만의 성질이 결코 아니다. 정의 조건 셋. 판정은 **접촉 중의 선형 동역학** $m\ddot\delta=-k\delta-d\dot\delta$ 위에서 하고, 거기서 한 스텝은 $(\delta,v)$에 작용하는 고정 행렬 $A(\Delta t)$다. $A$의 고유값은 **단위원 안이나 위에** 있어야 한다. [[04-robotics/control-theory-ce397|5. 제어 이론 §4]]의 이산시간 판정이다. 그리고 단위원 **위의** 고유값은 고유벡터 하나로 중복되어서는 안 된다. 그 조르당 블록은 선형으로 자라기 때문이다.
>
> $$\rho\big(A(\Delta t)\big)\le1$$
>
> $\rho$는 스펙트럼 반지름, 곧 고유값 절댓값의 최대다. 감쇠 없는 접촉에서 명시적 오일러는 어떤 스텝에서도 $\rho=\sqrt{1+(\omega\Delta t)^2}>1$이고, 반암시적 오일러는 $\omega\Delta t<2$인 동안 정확히 $\rho=1$이다. 그래서 안정 스텝은 한 적분기에게는 $\Delta t<2/\omega$라는 천장이고, 다른 적분기에게는 존재하지 않는다.
>
> - **예**: $1\,\mathrm{ms}$의 단단한 벽 위 반암시적 오일러. $\omega\Delta t=1$이다.
> - **비예**: 감쇠 없는 접촉 위, 어떤 스텝에서든 명시적 오일러. 계산 절에서 본, 스텝마다 곱해지는 $1+(\omega\Delta t)^2$다.
> - **비예**: "안정하니 정확하다". $\omega\Delta t=1.58$에서 랩의 반암시적 튕김은 이 판정을 통과하고도 에너지를 $2.25$배로 돌려준다. 안정성은 오차를 묶을 뿐 작게 만들지 않는다.
> - **왜 중요한가**: 불안정한 스텝을 넘어서면 접촉력은 모델이 아니라 적분기의 숫자이고, 어떤 후처리도 모델의 숫자를 되찾지 못한다.

> **심플렉틱 스텝의 정의.** 한 스텝 적분기가 **심플렉틱**(symplectic)하다는 것은 그 스텝 사상이 위상 공간의 넓이를 보존한다는 뜻이다. 1자유도에서는 $(\delta,v)$ 상태들의 어떤 조각이든 그 넓이다. 야코비안으로 확인하는 *사상*의 성질이고, 에너지 보존과 같은 것이 아니다. 정의 조건 셋. 첫째, 시스템이 감쇠 없는 접촉처럼 **보존계**(해밀토니안)여야 한다. 아니면 사상이 보존할 것이 없다. 둘째, 1자유도에서는 사상의 야코비안 행렬식이 모든 상태에서 **1이어야 한다.** 셋째, 정의의 일부가 아니라 정의에서 따라 나오는 결과로, 스텝이 작아질수록 참 에너지로 다가가고 사상이 보존하는 **수정 에너지** $\tilde E$가 있다. 이 접촉 같은 선형 스프링에서는 정확히, 비선형계에서는 아주 긴 시간 동안 거의 보존된다.
>
> $$\det\frac{\partial(\delta',v')}{\partial(\delta,v)}=1$$
>
> 넓이를 지키는 사상은 바깥으로 나선을 그릴 수도(넓이가 늘어야 한다), 안으로 말려 들어갈 수도(넓이가 줄어야 한다) 없기 때문에 그 궤도는 닫힌다. 계산 절 3단계의 타원 $\tilde E$ 위에서.
>
> - **예**: 반암시적 오일러. 스텝 행렬의 행렬식이 $\big(1-(\omega\Delta t)^2\big)\cdot1+\omega^2\Delta t\cdot\Delta t=1$이다.
> - **비예**: 명시적 오일러. 행렬식이 $1+(\omega\Delta t)^2$라 매 스텝 넓이가 늘고, 이것이 다른 쪽에서 본 에너지 증가다.
> - **비예**: "심플렉틱은 에너지 보존이라는 뜻이다". 계산 절에서 반암시적 핸들의 참 에너지는 튕김 도중 $E_{\text{in}}$의 두 배에 이르렀다. 보존되는 것은 $\tilde E$다. 그리고 $\omega\Delta t=2$를 넘으면 넓이를 지키는 같은 사상이 불안정하므로, 심플렉틱이라는 사실이 안정 스텝 판정을 대신하지 못한다.
> - **왜 중요한가**: 랩에서 명시적 열이 폭주하는 스텝 범위에서도 반암시적 열이 1 근처에 머무는 이유이고, 비용은 똑같이 스텝당 힘 계산 한 번이다.

> **튕김의 에너지 비의 정의.** 한 번의 튕김의 **에너지 비**(energy ratio)는 같은 물체가 자유 비행 중일 때 접촉 한 번 뒤와 앞의 운동 에너지 비이고, *무차원*이다. 반발 계수의 제곱이며, *적분기와 스텝까지 포함한* 시뮬레이션된 접촉의 성질이다. 정의 조건 셋. 첫째, 두 에너지 모두 **자유 비행 중에** 잰다. 접촉 도중에는 에너지 일부가 스프링에 저장되어 있으므로 거기서 재지 않는다. 둘째, 두 측정 사이에 **다른 힘이 작용하지 않아야** 변화 전체가 접촉의 몫이 된다. 셋째, 물체는 **하나의 강체**, 곧 차이가 숨어들 내부 에너지가 없는 물체여야 한다.
>
> $$r_E=\frac{E_{\text{out}}}{E_{\text{in}}}=\Big(\frac{v_{\text{out}}}{v_{\text{in}}}\Big)^2=e^2$$
>
> $v_{\text{in}}$과 $v_{\text{out}}$은 튕김 앞뒤의 법선 속력, $e$는 반발 계수다. 수동적인 물리 접촉은 $r_E\le1$이므로, $r_E>1$은 모두 시뮬레이션이 만든 것이다.
>
> - **예**: 정확한 감쇠 없는 튕김은 $r_E=1$, 감쇠 있는 낙하 셀은 $r_E=0.554$.
> - **비예**: 계산 절 1스텝에서 반암시적 핸들의 에너지, 곧 $E_{\text{in}}$의 두 배. 접촉 도중에 쟀으므로 되돌려줄 스프링 에너지가 들어 있다.
> - **비예**: $1\,\mathrm{ms}$의 단단한 벽에서 명시적 오일러의 $16$은 제대로 잰 에너지 비이지만, 접촉의 것이 아니라 적분기의 것이다. 이 정의는 시뮬레이션을 재고, 그것이 쓸모다.
> - **왜 중요한가**: 힘 센서 없이 어떤 시뮬레이터의 접촉이든 숫자 하나로 시험할 수 있다. 감쇠를 설정하지 않은 물체를 떨어뜨려 들어올 때보다 빨리 튀어나오면, 그 접촉에 대해 스텝이나 적분기가 틀린 것이다.

**랩 — 낙하 한 번, 적분기 둘, $\Delta t$와 $k$에 대한 스윕.** 영어 절의 코드가 계산 절처럼 낙하 셀을 돌린다. 강성 셋 — 패널, 단단한 벽, 그 사이의 열 배 단계 — 에서 $0.1$부터 $20\,\mathrm{ms}$까지 다섯 스텝으로, 각 적분기의 에너지 비와 최대 침투를 보고한다. [[02-foundations/lab-kernel|0.65 §2와 §3]]의 두 적분기만 쓰고, 두 번째 루프는 고정된 댐퍼로 스윕 일부를 다시 돌린다.

감쇠 없는 스윕, 코드가 출력하는 그대로다. 굵게 쓴 칸이 불안정한 스텝이다. $d=0$에서 명시적 오일러는 안정 스텝이 아예 없으므로 명시적 칸은 전부이고(그 열은 각 스텝의 대가를 보여 준다), 반암시적 칸은 $\omega\Delta t\ge2$인 것이다.

| $k$ (N/m) | $\Delta t$ (ms) | $\omega\Delta t$ | $E_{\text{out}}/E_{\text{in}}$, 명시적 | $E_{\text{out}}/E_{\text{in}}$, 반암시적 | 최대 $\delta$, 명시적 (mm) | 최대 $\delta$, 반암시적 (mm) | 정확한 값 $v_0/\omega$ (mm) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.1 | 0.010 | **1.032** | 1.000 | 1.008 | 1.000 | 1.000 |
| 400 | 1 | 0.100 | **1.372** | 1.002 | 1.083 | 1.001 | 1.000 |
| 400 | 2 | 0.200 | **1.872** | 1.009 | 1.170 | 1.005 | 1.000 |
| 400 | 5 | 0.500 | **4.717** | 1.045 | 1.500 | 1.031 | 1.000 |
| 400 | 20 | 2.000 | **121** | **9** | 4.000 | 2.000 | 1.000 |
| 4,000 | 0.1 | 0.032 | **1.105** | 1.000 | 0.324 | 0.316 | 0.316 |
| 4,000 | 1 | 0.316 | **2.708** | 1.010 | 0.406 | 0.320 | 0.316 |
| 4,000 | 2 | 0.632 | **7.097** | 1.045 | 0.520 | 0.320 | 0.316 |
| 4,000 | 5 | 1.581 | **60.06** | 2.250 | 1.000 | 0.500 | 0.316 |
| 4,000 | 20 | 6.325 | **$1.416\times10^4$** | **1,521** | 4.000 | 2.000 | 0.316 |
| 40,000 | 0.1 | 0.100 | **1.372** | 1.002 | 0.108 | 0.100 | 0.100 |
| 40,000 | 1 | 1.000 | **16** | 1.000 | 0.200 | 0.100 | 0.100 |
| 40,000 | 2 | 2.000 | **121** | **9** | 0.400 | 0.200 | 0.100 |
| 40,000 | 5 | 5.000 | **5,476** | **576** | 1.000 | 0.500 | 0.100 |
| 40,000 | 20 | 20.00 | **$1.438\times10^6$** | **$1.592\times10^5$** | 4.000 | 2.000 | 0.100 |

감쇠 있는 재실행이다. 두 벽 모두 $\zeta=0.1$이고 정확한 비는 $0.554$다. 명시적 오일러는 $k\Delta t\le d$에서, 반암시적 오일러는 $\omega\Delta t<1.81$에서 안정하다(계산 절 6단계). 굵게 쓴 칸이 그 조건 밖이다.

| $k$ (N/m) | $d$ (N·s/m) | $\Delta t$ (ms) | $k\Delta t$ | $\omega\Delta t$ | $E_{\text{out}}/E_{\text{in}}$, 명시적 | $E_{\text{out}}/E_{\text{in}}$, 반암시적 |
|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.8 | 0.1 | 0.04 | 0.01 | 0.573 | 0.555 |
| 400 | 0.8 | 1 | 0.40 | 0.10 | 0.776 | 0.565 |
| 400 | 0.8 | 2 | 0.80, 경계 | 0.20 | 1.089 | 0.580 |
| 400 | 0.8 | 5 | 2.00 | 0.50 | **2.887** | 0.646 |
| 40,000 | 8 | 0.1 | 4 | 0.10 | 0.776 | 0.565 |
| 40,000 | 8 | 1 | 40 | 1.00 | **12.45** | 0.922 |
| 40,000 | 8 | 2 | 80 | 2.00 | **100.8** | **11.56** |
| 40,000 | 8 | 5 | 200 | 5.00 | **2,500** | **625** |

표 두 개를 읽는 법.

**$\omega\Delta t$에 대한 표 하나다.** $1\,\mathrm{ms}$의 패널과 $0.1\,\mathrm{ms}$의 단단한 벽은 $\omega\Delta t=0.1$을 공유하고 같은 비 $1.372$와 $1.002$를 준다. 밀리미터만 $v_0/\omega$만큼 다르다. $20\,\mathrm{ms}$의 패널과 $2\,\mathrm{ms}$의 단단한 벽도 그렇다. 스텝이 접촉을 어떻게 다루는지는 $\omega\Delta t$ 하나로 정해지고, 그래서 4단계의 경계 $\Delta t<2/\omega$가 규칙의 전부다.

**명시적 오일러는 감쇠 없는 모든 칸에서 에너지를 얻는다.** $\omega\Delta t=0.01$에서 3%, $0.1$에서 37%, $1$에서 16배. 그 열은 안정 경계가 아니라 가격표다.

**반암시적 오일러는 $\omega\Delta t=2$까지 버티다가 3단계가 말한 대로 무너진다.** 경계에서 $9$, $5$에서 $576$이다. 구간 안에서 그 비는 접촉이 샘플 사이 어디서 시작하고 끝나는지가 정하는 띠 안에 머문다. 벽 안의 첫 샘플이 벽면을 스텝의 $\varphi$만큼 지난 곳이면, 그 자리에서 보존량 $\tilde E$는 $E_{\text{in}}\big(1-(\omega\Delta t)^2\varphi(1-\varphi)\big)$이다. 벽 밖의 첫 샘플이 스텝의 $s$만큼 벗어난 곳이면 $E_{\text{out}}\big(1-(\omega\Delta t)^2s(1-s)\big)=\tilde E$이다. 두 곱 $\varphi(1-\varphi)$와 $s(1-s)$는 $0$과 $\tfrac14$ 사이에 있으므로

$$1-\tfrac14(\omega\Delta t)^2\ \le\ \frac{E_{\text{out}}}{E_{\text{in}}}\ \le\ \frac{1}{1-\tfrac14(\omega\Delta t)^2}$$

이다. 낙하 셀은 샘플 위에서 시작하므로($\varphi=0$) 그 열은 1 이상일 수밖에 없다. 모든 칸이 그렇고, 천장 아래에 있다. $\omega\Delta t=0.5$에서 $1.045$ 대 $1.067$, $1.58$에서 $2.25$ 대 $2.67$. 마지막 칸은 안정성 판정을 통과하고도 나쁜 숫자다.

**침투도 밀리미터로 같은 이야기를 한다.** 명시적 오일러의 최대 침투는 나선을 따라 자란다. $5\,\mathrm{ms}$의 패널에서 정확한 $1.0\,\mathrm{mm}$ 대신 $1.5\,\mathrm{mm}$다. 반암시적 오일러의 것은 타원의 가장 넓은 점 $v_0/\big(\omega\sqrt{1-\tfrac14(\omega\Delta t)^2}\big)$ 안에 머문다. 구간 밖에서는 두 최대 침투가 그저 벽 안의 첫 샘플, 곧 $\Delta t\,v_0$와 그 두 배다. 참 최대가 $0.1\,\mathrm{mm}$인 벽에서 $2$와 $4\,\mathrm{mm}$.

**장면 하나, 스텝 하나.** 시뮬레이터는 한 장면의 모든 접촉을 같은 $\Delta t$로 전진하므로, 가장 단단한 접촉 위의 가장 가벼운 물체가 스텝을 정한다. 패널과 단단한 벽이 한 장면에 있으면, 이 격자에서 둘 모두 반암시적 오일러를 구간 안에 두는 가장 큰 스텝은 $1\,\mathrm{ms}$다. 그 스텝에서 패널은 접촉당 약 31스텝, 단단한 벽은 세 스텝을 받는다.

**감쇠는 6단계가 말한 대로 한다.** 명시적 오일러는 $d\ge k\Delta t$인 곳 — $0.1$과 $1\,\mathrm{ms}$의 패널, $0.1\,\mathrm{ms}$의 단단한 벽 — 에서 안정해지지만, 거기서도 반발을 과대평가한다. $\omega\Delta t=0.1$에서 정확한 $0.554$ 대신 $0.776$이다. 경계(패널, $2\,\mathrm{ms}$)에서는 튕김이 여전히 9%를 얻는다. 반암시적 오일러는 좁아진 구간이 끝날 때까지 $0.554$를 잘 따라간다. $\omega\Delta t=1$에서는 구간 안인데도 이미 크게 벗어난 $0.922$, 구간 밖인 $2\,\mathrm{ms}$에서는 감쇠 없는 $9$보다 나쁜 $11.6$이다.

**이 표가 위의 시뮬레이터들에 대해 말하는 것.** §2의 시뮬레이터 중 어느 것도 낙하 셀이 아니고, 이 표의 무엇도 그중 하나를 재지 않는다. 표가 하는 일은 §2와 §3이 이미 그 시뮬레이터들에 귀속시킨 선택에 값을 매기는 것이다.

- **MuJoCo**: 설계상 제약 위반을 허용한다(위). 접촉이 간극 0을 강제하는 대신 부드럽게 서로 파고들고, 그래서 [[04-robotics/contact-force-tactile|9. 접촉 §3]]의 표에서 강체 쪽이 아니라 낙하 셀과 같은 유연 쪽에 선다. 페널티 모델에서 안정 스텝 $2\sqrt{m/k}$와 최대 침투 $v_0\sqrt{m/k}$는 같은 $\sqrt{m/k}$를 갖는다. 그래서 거친 스텝에서 안정해질 때까지 접촉을 무르게 하면 침투가 같은 비율로 깊어진다. "빠르고 안정적"과 "로드셀이 읽을 힘이 아니다"는 한 선택을 두 쪽에서 본 것이다.
- **MuJoCo 3.3.5의 촉각 센서**: 침투 깊이를 보고한다(위). 침투 열은 시뮬레이션된 침투가 접촉의 무름과 스텝에 따라 움직인다는 것을 보여 준다. 같은 벽에서 정확한 값은 $0.1\,\mathrm{mm}$, $1\,\mathrm{ms}$의 명시적 오일러로는 $0.2\,\mathrm{mm}$다. 그러니 시뮬레이션된 촉각 읽음값 안에는 접촉 모델과 스텝이 들어 있다.
- **Drake의 하이드로일래스틱 접촉**: 이것도 "약간의 변형 가능한 층"(위)으로 강체를 파고들게 한다. 그런 유연성은 그 위에 놓인 질량과 함께, 고정 스텝 시뮬레이션이 분해해야 할 시간 척도를 정한다. Drake의 솔버가 그것을 어떻게 다루는지는 낙하 셀이 말하지 않는다.
- **Isaac 아래의 PhysX와 Isaac Lab**: PhysX는 "처리량에 맞춰 조율된" 계보이고, Isaac Lab은 병렬 환경 수천 개를 돌린다(§2). 처리량은 스텝으로 세고, $\omega\Delta t$ 열은 모든 스텝이 지켜야 할 조건이다. $\Delta t$를 반으로 줄이면 같은 시뮬레이션 시간에 스텝이 두 배가 되고, 같은 질량 위에서 접촉이 열 배 단단해지면 스텝이 $\sqrt{10}\approx3.2$배 작아져야 한다. 표의 가운데 행에서 $20$ 대신 $6.3\,\mathrm{ms}$다.
- **PyBullet**: §2에 쉽고 성숙하며 CPU 친화적이라고만 나온다. 이 페이지는 그것이 접촉을 어떻게 전진하는지 아무것도 말하지 않고, 랩도 그것을 바꾸지 않는다.

각 시뮬레이터가 어떤 적분기와 어떤 기본 스텝을 쓰는지는 그 자신의 문서에 있고 버전에 따라 바뀔 수 있다. §10이 둘 다를 묻는 이유다.

### 4. 지형과 토공

별도의 세계이고, 별도의 도구를 쓰며, 이 도메인에서 시뮬레이션이 진짜로 성숙한 유일한 부분이다.

- **AGX Dynamics**(Algoryx)가 가장 잘 문서화된 선택지다. `agxTerrain` 모듈은 높이장 표면 아래에
  질량·다짐도·토질을 담은 3D 복셀 격자를 모델링한다. 굴착 도구가 실패 영역(failure zone)을
  만들어 고체 지형 질량을 동적 질량으로 바꾸고, **내부 마찰각과 점착력**(흙에 가해진 압력에 따라 전단 저항이 얼마나 커지는지와, 압력이 0일 때
  전단 저항이 얼마인지를 정하는 두 강도 매개변수)으로 매개변수화되며,
  고체 셀이 6자유도 입자가 되고, 질량 집합체가 실패면을 통해 관성 저항을 공급한다. 관입 저항과
  굴착 저항이 분리되어 있다. 다짐, 팽창률(swell factor), 안식각도 모델링한다.
  - 독특하게도 벤더의 매개변수 수준 문서 **와** 심사받은 오픈 액세스 물리 논문을 **둘 다**
    가지고 있다: Servin, Berglund, Nystedt, *A multiscale model of terrain dynamics for
    real-time earthmoving simulation*, 2021. Algoryx는 이 모델의 굴착 저항과 토사 변위가
    "기준 모델과 10~25%까지 일치하며, 3자릿수 이상 빠르게 돈다"고 밝힌다.
  - 상용, 좌석당 연간 구독, **가격은 문의**. 학술 단일/그룹 라이선스가 있으며 엄격히 비상업용이다.
- **Vortex Studio**(CM Labs)는 변형 지형·토질 재료·토사 입자를 문서화하고 있고 운전 교육에서
  상업적으로 검증되었다. 연구에는 문제가 둘이다: 자기 토질 모델에 대해 가져올 수 있는 벤더
  이론 문서가 없어 최선의 서술이 제3자의 것이고, CM Labs 자신의 표현으로
  **"An academic License is not offered anymore."**
- **Project Chrono**가 최선의 오픈 선택지(BSD-3)이며, 하나의 프레임워크에 토질 충실도의
  *사다리*를 제공하는 유일한 것이다: **SCM**(Soil Contact Model. Bekker-Wong 준경험적
  압력–침하 관계로 변형되는 지면 메시), 입상 **DEM**(이산요소법. 흙 알갱이 하나하나를 시뮬레이션),
  **FEA**(흙을 연속 재료로 보는 유한요소해석), 그리고 논문이 "digging, grading"을 명시적으로
  다루고 실제 굴착 로봇에 대해 검증한, SPH(smoothed particle hydrodynamics, 메시 없는 입자 기법)로
  푸는 연속체 모델 **CRM**. 경험 법칙에서 재료와 알갱이를 모델링하는 쪽으로 갈수록 세부와 계산
  비용이 함께 늘어난다. **Chrono DEM-Engine**은 정책을 돌릴 곳이 아니라 검증의 기준으로 쓸 고충실도 모델이다.

> [!note] 정직한 권고
> **살 수 있으면 AGX, 열려 있고 인용 가능해야 하면 Chrono::CRM**, 그리고 DEM-Engine을 기준
> 모델로. 단서도 함께 가져가라: 두 선도적 실시간 토질 모델 모두 DEM 기준의 **10~25%** 수준
> 까지만 검증되었다. 어떤 실시간 시뮬레이터에서 나온 정량적 굴착력도 근사값이고, 그것을 유효
> 숫자 세 자리로 보고하는 논문은 과잉 주장이다.

### 5. 변형되는 건설 자재 — 공백을 분명히 말한다

**어떤 시뮬레이터도 건설 자재를 자재로서 모델링하지 않는다.** 드라이월도, 철근 케이지도,
건축 멤브레인도. 있는 것은 직접 매개변수화하고 직접 검증해야 하는 범용 원시 요소들이다:

| 자재 | 가장 가까운 원시 요소 | 현황 |
|---|---|---|
| 케이블·로프·호스 | AGX `agxCable` | **산업 수준으로 해결됨** — 6자유도 전부를 가진 집중 강체들이라 굽힘·비틀림·신장이 추적되고, 소성도 있다. 문서화된 한계: 케이블은 원형이고 크기·물성이 균질해야 하며, 해상도가 고정이다 |
| 철근 메시·케이지 | 연결된 로드의 네트워크 | **전용 모델 없음.** 가장 가까운 것은 로드 사이의 임의 연결을 다루는 DisMech(RA-L 2024) |
| 멤브레인·판재 | 박판 셸 | Chrono의 `ChElementShellReissner`가 물리적으로 가장 적절한 문서화된 정식화이고 BSD-3다 — 그러나 **건설 자재로 검증된 사례가 어디에도 없다** |
| **드라이월 패널** | — | **없음.** 탄성 변형이 아니라 *파단*하는 뻣뻣하고 취성이며 무거운 판재는 확인 가능한 어떤 것으로도 모델링되지 않는다 |

변형체 작업에 Isaac을 고르기 전에 알아 둘 한계가 하나 더 있다. 문서가
**"Particles and deformable body do not support contact reports"** 라고 밝히며, 정적 마찰도
마찰 결합 모드도 지원하지 않는다. 변형체에서 접촉력을 읽어낼 수 없다 — 접촉이 많은 조작 연구가
하려는 측정이 바로 그것인데.

> [!warning] Genesis — 인용하기 전에 이력을 읽어라
> Genesis(현재 **Genesis World**, 회사 Genesis AI 아래에서 개발)는 하나의 API 아래 이례적으로
> 넓은 멀티피직스를 제공한다. 2024년 12월 README는 이렇게 주장했다: "over 43 million FPS when
> simulating a Franka robotic arm with a single RTX 4090 (430,000 times faster than
> real-time)". MuJoCo 유지보수자가 그 비교를 공개적으로 문제 삼았고, ManiSkill 개발자가 그
> 벤치마크가 가장 빠른(가장 부정확한) 물리 설정을 썼고, 행동 1회 뒤 999스텝을 무행동으로
> 돌렸으며, 자기 충돌을 껐다고 주장하는 이슈를 냈다. 이후 팀은 스크립트 헤더에 비판자의 것과
> "거의 동일하다"고 적힌 수정 벤치마크를 공개했고, 이슈는 비판자가 새 숫자들이 "맥락을 제대로
> 주면 더 정확해 보인다"며 — 다만 자신이 재검증하지는 않았다고 밝히며 — 닫았다.
> **43M FPS 주장은 2026년 5월 재작성 과정에서 철회 표시 없이 README에서 삭제되었다.**
> 여전히 심사받은 논문은 없고, 공식 인용 블록은 회사 블로그 글과 저장소 URL을 제시한다.
> 이 중 무엇도 소프트웨어가 나쁘다는 뜻이 아니다. 검증된 결과로 인용할 수 없다는 뜻이고,
> 인용할 때 "소프트웨어"라고 말해야 한다는 뜻이다.

### 6. 벤치마크

| 벤치마크 | Venue | 시뮬/실제 | 무엇을 재는가 | 초록이 밝힌 규모 |
|---|---|---|---|---|
| **RLBench** | RA-L 2020 | 시뮬레이션 | 과제 성공, few-shot 일반화 | "100 completely unique, hand-designed tasks" |
| **Meta-World** | CoRL 2019 | 시뮬레이션 | 멀티태스크·메타RL의 미본 과제 전이 | "50 distinct robotic manipulation tasks" |
| **ManiSkill 3** | RSS 2025 | 시뮬레이션 | 처리량과 과제 범위 | "up to 30,000+ FPS"; "12 distinct domains" |
| **CALVIN** | RA-L 2022 | 시뮬레이션 | 긴 지평 언어 조건부, zero-shot | **초록에 숫자 없음** |
| **LIBERO** | NeurIPS 2023 D&B | 시뮬레이션 | **평생 학습** 전이 — 순방향·역방향·과제 순서 | "four task suites (130 tasks in total)" |
| **FurnitureBench** | RSS 2023 | **둘 다** | 실세계 긴 지평 접촉이 많은 **조립** | "200+ hours of pre-collected data (5000+ demonstrations)" |
| **RoboCasa** | RSS 2024 | 시뮬레이션 | 모방학습의 데이터 스케일링 거동 | "over 150 object categories"; "100 tasks" |
| **NIST Assembly Task Boards** | RA-L 2020 | **실제만** | **사람 기준선** 대비 완료 시간 | "three task board artifacts" |
| **RAMP** | RA-L 2024 | **둘 다** | 조립 계획 *과* 실행, 난이도 3등급 | **초록에 숫자 없음** |

> **벤치마크의 정의.** **벤치마크**(benchmark)는 *공유된 평가 도구*다. 누구나 다시 쓸 수 있는, 채점 규칙이 고정된 과제이지, 데이터셋도 시뮬레이터도 한 논문의 비교도 아니다. 정의 조건 셋이고, 이 절의 부재들은 이 조건에 대한 주장이다. 첫째, **공개 프로토콜.** 과제, 시작 조건, 무엇을 성공으로 세는지가 다시 돌릴 수 있을 만큼 적혀 있다. 둘째, **공개 실물.** 프로토콜이 돌아가는 환경·물체·보드를 남이 구할 수 있다. 셋째, **결과를 보탤 수 있음.** 그것을 만들지 않은 사람도 발표된 점수와 비교 가능한 점수를 보고할 수 있다.
>
> - **예**: NIST Assembly Task Boards — 아래에서 보듯 물리적 실물과 사람 기준 채점 프로토콜.
> - **비예**: 한 논문 안의 비교 평가. 스스로 점검 답 5의 건설 스킬 비교가 그렇다. 신중할 수는 있어도 남이 결과를 보탤 공개 프로토콜이 없다.
> - **비예**: Open X-Embodiment(§7). 과제와 채점 규칙이 아니라 기록된 채널을 제공하므로, §1의 뜻으로 데이터셋이다.
> - **왜 중요한가**: 이 절의 모든 부재는 어떤 영역에서 세 조건을 모두 만족하는 것이 없다는 주장이다. 어느 조건이 깨지는지 이름을 대면 그 주장을 확인할 수 있게 된다.

**여기서 관련 있는 것은 조립 계보다**: NIST 태스크 보드가 물리적 실물과 사람 기준 채점
프로토콜을 준다(peg 삽입, 기어 맞물림, 커넥터, 너트 체결, 그리고 후속 보드에서 케이블 배선과
와이어 하니스). FurnitureBench가 시뮬레이터를 곁들인 실기계 긴 지평 벤치마크를 더한다. 그리고
**RAMP**가 건설을 틀로 삼은 유일한 것이다 — Section I이 도메인을 *오프사이트* 건설이라고
밝히며 "빔을 프레임으로 조립하는 일은 여전히 수작업으로 남아 있다"고 말한다.

> [!important] RAMP는 조심해서 인용하라
> RAMP의 초록은 "real-world industrial assembly tasks"라고만 말한다 — **construction이라는
> 단어가 초록에 나오지 않는다.** 오프사이트 건설 프레이밍은 본문에 있다. RAMP를 건설
> 벤치마크로 인용한다면 초록이 아니라 절을 인용하라.

**벤치마크 지형에서 검증된 부재 둘** — 셋째는 데이터셋 쪽이고 §7에 있다. **현장 건설 조작 벤치마크는 없다** — 조적, 드라이월, 철근 결속, 파사드
설치, 머리 위 작업 어느 것에도. 있는 것은 벤더의 처리량 수치와 각자의 평가를 쓰는 일회성
논문들이다: 공유 프로토콜도, 공유 실물도, 리더보드도 없다. 그리고 **굴착·토공에 대한 표준
벤치마크나 시험 피트 프로토콜도 없다.** ISO 7546, ISO 6165, ISO 10968과 SAE MTC1 위원회는
자율성 성능이 아니라 *기계*를 표준화한다. NASA의 Lunabotics는 규칙과 채점표를 공개하지만
레골리스 시뮬런트이고 학생 대회 범위이며 규칙이 해마다 바뀐다.

### 7. 데이터셋 — 그리고 빠져 있는 모달리티

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="데이터셋 역량의 세 띠, 그중 세 번째가 비어 있다">
  <g fill="currentColor">
    <rect x="24" y="42" width="512" height="48" rx="4" fill-opacity="0.07"/>
    <rect x="24" y="112" width="512" height="48" rx="4" fill-opacity="0.16"/>
    <rect x="40" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="205" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="370" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="40" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="205" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="370" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.5">
    <rect x="24" y="42" width="512" height="48" rx="4"/><rect x="24" y="112" width="512" height="48" rx="4"/>
    <rect x="40" y="52" width="150" height="28" rx="3"/><rect x="205" y="52" width="150" height="28" rx="3"/><rect x="370" y="52" width="150" height="28" rx="3"/>
    <rect x="40" y="122" width="150" height="28" rx="3"/><rect x="205" y="122" width="150" height="28" rx="3"/><rect x="370" y="122" width="150" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.75" stroke-dasharray="6 4">
    <rect x="24" y="182" width="512" height="48" rx="4"/>
  </g>
  <g font-size="10.5" fill="currentColor" font-weight="600">
    <text x="24" y="36">비전 + 고유수용감각 + 언어</text>
    <text x="24" y="106">&#8230; 그리고 힘/토크 채널</text>
    <text x="24" y="176">&#8230; 그리고 건설 작업에서</text>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="115" y="66">Open X-Embodiment</text><text x="115" y="77" font-size="9">스킬 527, 과제 160,266</text>
    <text x="280" y="66">DROID</text><text x="280" y="77" font-size="9">궤적 65,000</text>
    <text x="445" y="66">BridgeData V2</text><text x="445" y="77" font-size="9">궤적 53,896</text>
    <text x="115" y="136">RH20T</text><text x="115" y="147" font-size="9">시퀀스 110,000+</text>
    <text x="280" y="136">FMB</text><text x="280" y="147" font-size="9">기능적 조작</text>
    <text x="445" y="136">REASSEMBLE</text><text x="445" y="147" font-size="9">시연 4,551</text>
    <text x="280" y="212" font-size="11" opacity="0.9">공유된 실기계 힘 데이터가 없다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="250">모든 수치는 그 논문 자신의 초록에서 인용했다. 세 번째 띠가 비어 있고, 그것이 발견이다.</text>
  </g>
</svg>

큰 조작 코퍼스들은 **비전·고유수용감각·언어**다. 어느 한 데이터셋의 실수가 아니라 공유 스키마에
박혀 있는 것이다. Open X-Embodiment 개요 시트의 열은 *로봇, 에피소드, 파일 크기, 형태, 그리퍼,
행동 공간, RGB 카메라, 깊이 카메라, 손목 카메라, 언어 주석, 수집 방법, 고유수용감각, 장면 유형,
제어 주파수* 로 이어진다 — **force 열도 tactile 열도 없다.** 지배적인 데이터 형식이
[[04-robotics/force-compliance-control|접촉이 많은 조작]]이 가장 의존하는 모달리티를 표현하지 못한다.

이 패턴을 깨는 데이터셋들:

- **RH20T**가 중요한 것이다: 초록이 "over 110,000 contact-rich robot manipulation sequences"라
  말하고, 프로젝트 페이지가 RGB·깊이·관절 토크·오디오와 함께 **100 Hz의 6자유도 힘/토크
  채널**을 문서화한다. 손끝 촉각도 있지만 **로봇 구성 일곱 중 하나에만** 있다 — 코퍼스 전체를
  촉각이라고 서술하지 마라.
- **FMB**(IJRR)는 말단 힘과 토크 필드를 명시적으로 노출한다.
- **REASSEMBLE**은 NIST 태스크 보드 위에서 이벤트 카메라·힘토크·마이크·다시점 RGB를 기록한다 —
  "4,551 demonstrations, of which 4,035 were successful".
- OXE 안에서도 구성 데이터셋 둘이 힘을 담고 있다 — 다만 *어디에* 담기는지를 정확히 하라.
  `iamlab_cmu_pickup_insert`는 **상태 벡터 안에** 넣는다(20차원: 관절각 7, 그리퍼 1, 관절
  토크 6, 말단 힘 6). `stanford_kuka_multimodal`([[01-canonical-papers/notes/7-robotics/vision-and-touch|Vision-and-Touch]]
  데이터)은 **그렇지 않다**: 상태는 8차원 고유수용뿐이고, 힘은 형제 관측 필드
  (`ee_forces_continuous`)에 있다. 둘 다 작고, 통합 스키마는 어느 쪽도 드러내지 않는다.

> [!warning] 큰 데이터셋의 인용 함정 둘
> **DROID**는 곳에 따라 다른 숫자를 보고한다: arXiv 초록은 궤적 76k에 과제 84개, RSS 프로시딩
> 초록은 65,000에 86개다. **BridgeData V2**도 마찬가지다: arXiv 60,096, PMLR 프로시딩 53,896.
> 인용하는 판본에 맞는 숫자를 쓰라.

### 8. 건설·현장 데이터

실제 건설 현장 데이터셋은 존재하고, 그 전부가 **인식** 코퍼스다:

- **ConSLAM** — 그리고 이것은 하나가 아니라 **두 편의 별개 논문**이다. ECCV 2022 Workshops
  논문이 데이터셋을 발표한다(이미지·LiDAR·IMU·지상 레이저 기준 스캔, 주기적으로 수집).
  *Journal of Computing in Civil Engineering* 2023 논문이 확장판이며 그것을 벤치마크로 만드는
  것을 더한다: 공개 규모를 "five sequences"로 명시하고, 순차 LiDAR를 기준 스캔에 정합해
  **기준 궤적을 복원**하며, 그에 대해 SLAM 오차를 자동으로 채점하는 방법을 문서화한다.
  저자들의 저장소가 저널 논문을 워크숍 논문의 "Free Journal Extension Paper"라고 스스로
  이름 붙인다 — 두 데이터셋이 아니라 두 번 발표된 하나의 데이터셋이다.
- **Hilti-Oxford**(RA-L 2023)와 **Hilti SLAM Challenge** 시리즈 — 건설 환경에서의
  LiDAR·카메라·IMU, 밀리미터 정확도 기준값, CC BY-NC-SA.
- **Rohbau3D**(*Scientific Data*, 2025) — "504 high-resolution LiDAR scans captured with a
  terrestrial laser scanner across 14 distinct construction sites", 의미 라벨 포함,
  **CC BY 4.0**. 확인한 것 중 라이선스가 가장 좋은 건설 현장 3D 코퍼스다.
- **ConRebSeg** — "14,805 RGB images with segmentation labels for autonomous robotic
  inspection of reinforced concrete defects", CC BY 4.0.
- **SODA**, **MOCS**, **ACID**, **CIS** — 검출과 분할을 위한 건설 *이미지* 데이터셋. 함정이
  둘 있다: ACID는 때때로 굴착 데이터셋으로 잘못 인용되지만 기계의 이미지일 뿐 토사도 힘도
  궤적도 없고 — 변형체 조작을 다루는 무관한 로보틱스 논문에도 ACID라는 이름이 있다.

토공에 한정하면 가장 큰 궤적 코퍼스는 기업 공개물이다 — RGB, LiDAR 유래 표고 지도, 관절각을
담은 굴착기 동작 데이터로, 비상업 라이선스이며 **뒤에 논문이 없다.** ETH의 건식 석벽 데이터셋은
배치 가능성 라벨이 붙은 디지털화된 돌 메시 1,100개를 CC BY 4.0으로 공개한다 — 기하와 라벨이지
궤적도 힘도 아니다. **측정된 버킷 힘이나 토사-도구 상호작용의 공개 데이터셋은 존재하지 않는다.**

> [!important] 공백을 가장 날카롭게 진술하는 법
> 이 데이터셋 중 둘은 **실제 건설 기계에서** 기록되었다 — Hilti SLAM Challenge 2023은 Jaibot을
> 참조한 드릴링 로봇 플랫폼을 썼고(다만 그 챌린지 논문 초록은 "로봇에 장착한 기성 LiDAR"라고만
> 적으므로 플랫폼 이름은 다른 출처에서 온 것이다), **ETHcavation**은 Menzi Muck M545 보행 굴착기에서 기록해
> "502 hand-labeled sample images with panoptic annotations from construction sites"를 공개한다.
> **어느 쪽도 액추에이터·관절·유압·힘 채널을 공개하지 않는다. 기계는 계측되어 있었고, 힘은
> 공유되지 않았다.**
>
> 이것은 독립적으로 뒷받침된다. "51 publicly available visual datasets that span the
> 2005-2024 period"를 정리한 심사 논문 *OpenConstruction*은 그것들을 RGB·열화상·깊이·LiDAR
> 포인트 클라우드·합성이라는 모달리티 분류로 조직한다 — **거기에 force, torque, tactile,
> contact 행이 아예 없다.**

> [!important] 이 프로그램이 놓인 공백
> **실기계의 *접촉이 많은* 건설 조작 시연을 담은 공유 데이터셋은 존재하지 않는다.** DROID
> 규모도, 10,000도, 1,000도 아니다. 무엇이 없고 무엇이 있는지를 정확히 말해야 한다. 이 위키
> 안의 논문 셋이 반례처럼 보이지만 아니기 때문이다:
> [[01-canonical-papers/notes/8-construction/ext|ExT]]는 과제당 15만 에피소드를 갖지만
> 시뮬레이션에서 생성되어 실제 접촉이 없고,
> [[01-canonical-papers/notes/8-construction/liang-lfd|Liang]]은 가상 3,000 + 실제 85개의
> 시연 *영상*을 쓰고 Gazebo에서 평가하며,
> [[01-canonical-papers/notes/8-construction/kindle-jaibot|Kindle]]은 데이터셋 일곱 개를
> 공개하지만 그것은 변형 보상용 가속도계·자세 기록이지 조작 시연이 아니다. 셋 중 어느
> 것도 공유 스키마의 힘을 동반한 실기계 시연을 제공하지 않는다. OXE의 `scene type` 열은 *table top,
> kitchen, hallway, office, pantry, shelf, workshop, outdoors* 같은 값을 갖는다 — 건설도,
> 현장도, 중장비도 없다.
>
> 공백은 3~4자릿수이고, 정도만이 아니라 **종류**의 공백이다: 힘 채널도, 촉각 채널도, 공유
> 스키마도 없다. 실제 건설 작업의 잘 큐레이션된 데이터셋이 불균형하게 값어치 있는 이유가
> 그것이고([[06-research-practice/real-world-impact|6. §3]]),
> [[04-robotics/teleoperation-demonstration|12번]]의 시연 수집 문제가 여기서는 공학적 세부가
> 아니라 연구 질문인 이유도 그것이다.

### 9. 이 프로그램을 위한 선택

| 하려는 일 | 쓸 것 | 이유 |
|---|---|---|
| 접촉이 많은 조작 정책 학습 | MuJoCo, 규모가 필요하면 Isaac Lab | 속도와 안정성. 진짜 접촉력이 필요한지 먼저 확인할 것 |
| 접촉 **힘**이 곧 결과인 연구 | Drake(하이드로일래스틱) + 실기계 | 점 힘이 아니라 접촉면과 압력 분포 |
| 굴착·지형 | 예산이 되면 AGX, 아니면 Chrono::CRM | 인용 가능한 물리를 갖춘 유일한 문서화된 토질 모델들 |
| 조립 평가 | NIST 태스크 보드 → FurnitureBench → RAMP | 실물, 그다음 실기계, 그다음 건설 프레이밍 |
| 변형되는 건설 자재 | 없다 — 만들고 검증하라 | 논문에 그렇게 쓰라. 당신 연구의 결함이 아니라 기여다 |
| 조작 정책 사전학습 | Open X-Embodiment, DROID, RH20T | 힘 채널이 필요하면 RH20T |

**여기서 얻는 독법.** 각 행을 도구 적합성의 출발 가설로 쓰고 결정적인 물리량을 검증한다. 예를 들어 힘에 민감한 삽입 연구는 해당 재료·속도에서 모델의 접촉이 측정 반응을 예측한다는 증거가 필요하다. 정책 개발에 유용한 플랫폼도 힘 정확도 주장의 측정 도구로는 부족할 수 있다. 벤치마크 점수를 해석하기 전에 이 구분을 설계에 적는다.

### 10. 남의 논문의 도구 절 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 어느 시뮬레이터, 어느 버전인가? | Isaac Gym 결과는 지원 종료 이전의 것이고, MuJoCo 접촉은 3.x에서 바뀌었다 |
| 어느 적분기와 스텝, 어떤 접촉 강성인가? | $\omega=\sqrt{k/m}$를 분해하지 못하는 스텝에서 나온 접촉력이나 튕김은 모델이 아니라 적분기의 숫자다(§3 랩) |
| 접촉력은 **시뮬레이션**인가 **측정**인가? | 시뮬레이터의 접촉력은 측정이 아니라 모델링 선택이다 |
| 시뮬만인가, 실제만인가, 둘 다인가? | 벤치마크마다 다른데 "벤치마크"라는 말이 그것을 감춘다 |
| 어느 데이터셋 **판본**이며, 어느 초록의 숫자인가? | DROID와 BridgeData V2 둘 다 서로 다른 수치를 보고한다 |
| 데이터에 힘이나 촉각이 있기는 한가? | 대개 없고, 대개 논문이 그렇다고 말하지 않는다 |
| 그 도구는 인용 가능한가? | PyBullet·Drake·Isaac Sim·Genesis에는 심사받은 논문이 없다 |

**여기서 얻는 독법.** 물리 사건에서 보고 지표까지의 경로를 복원한다. 접촉력 결과라면 힘의 출처, 이를 만든 보정이나 모델, 독립 측정과의 비교 여부를 묻는다. 같은 시뮬레이션 가정으로 데이터를 만들고 결과까지 판정했다면 일치는 물리적 타당성보다 내부 일관성을 보여 준다. 도구 이름만으로 이 차이를 해소할 수 없다.

### 11. 학습된 정책의 평가 읽기

도구 절은 그 숫자들이 *무엇 위에서* 나왔는지를 알려준다. 이 절은 숫자 자체에 관한 것이다 —
VLA·확산 정책·로코모션 논문에서 백분율이 등장하고, 비교되기 전에 해석되어야 하는 그 부분.

**"성공률"이 빠뜨리는 것.** 백분율 하나가 독립적인 선택 네 개를 압축하고 있고, 80%를 보고한
두 논문이 그중 어느 것에서도 일치하지 않을 수 있다:

| 선택 | 숫자를 움직이는 이유 |
|---|---|
| **시행 횟수** | 10회로는 약 10퍼센트포인트 아래를 분간할 수 없다. 3의 법칙($3/n$)으로, 10회 중 실패 0회는 참 실패율 **30%** 근처까지와 양립한다(정확한 상한은 26%이고, 위키는 전체에서 $3/n$을 쓴다) — 그러니 "10/10"은 신뢰성의 증거가 *아니다*([[06-research-practice/experimental-design-reproducibility\|3. 실험 설계 §4]]) |
| **초기 상태 분포** | 물체 자세를 무작위화했는가, 같은 자리로 리셋했는가? 고정된 시작에서 평가된 정책은 분포에서 평가된 정책보다 쉬운 질문을 받고 있다 |
| **무엇을 완료로 세는가** | 시간 제한, 자세 허용오차, 사람 판정. 허용오차는 자주 명시되지 않고, 두 시스템의 차이 전체가 거기인 경우가 흔하다 |
| **리셋과 재시도를 세는가** | 시행 사이에 사람이 물체를 바로 세워 준다면 그 사람도 시스템의 일부다. 그것을 세지 않으면 보고된 자율성은 측정된 자율성이 아니다 |

**진행도와 부분 점수.** 긴 지평 과제와 연쇄 과제는 완료 여부가 아니라 *정책이 얼마나 갔는지*로
채점되는 일이 늘고 있다 — 단계 완료 수, 하위 과제 수, 정규화된 진행 점수. 이진 성공이 너무
거칠다는 데 대한 합당한 대응이고, 동시에 특정한 비교 실패를 들여온다: **높은 진행 점수와 0%
성공률은 양립한다.** 그리고 그것은 과제를 안정적으로 시작하고 안정적으로 끝내지 못하는 정책을
기술한다. [[01-canonical-papers/notes/4-vla/pi0|π0]] 주장 상자의 독립 평가가 정확히 이 모양이다.
논문이 진행도를 앞세우면 완료 숫자를 찾아보고, 완료를 앞세우면 베이스라인에도 부분 점수가
주어졌는지를 확인하라.

**Seen 대 unseen.** 이 문헌의 거의 모든 일반화 주장이 분할 위에 서 있고, 그 분할의 *축*이 곧
주장이다: 본 적 없는 물체 개체, 본 적 없는 물체 범주, 본 적 없는 배경, 조명, 장면, 신체.
이것들은 난이도가 같지 않은데 논문은 좀처럼 서열을 밝히지 않는다. 학습한 범주의 다른 개체로
일반화하는 방법은 범주를 가로질러 일반화하는 방법보다 훨씬 약한 주장을 하고 있다 — **숫자보다
분할의 정의를 먼저 읽어라.** 숫자는 그것에 상대적으로만 의미가 있다.

**1차 평가 대 독립 평가.** 로봇 학습 결과는 재현 비용이 커서, 출판된 비교 대부분은 저자들이
남의 방법을 직접 재현한 것이다. 부정직한 것은 아니지만 독립적인 것도 아니다. 진짜 제3자
평가가 존재한다면 그것이 헤드라인보다 값어치가 있고, 둘 사이의 격차는 자주 크다 —
[[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등]](시뮬 77% →
실제 주택 여섯 곳 23%)과 π0의 독립 재평가를 보라. **비교를 인용할 때는 누구의 평가인지 밝혀라.**

> [!warning] 정책 표 대부분을 결판내는 세 질문
> **1. 시행 몇 회이고, 어떤 초기 상태 분포에서인가?** **2. 이것은 시뮬레이션인가, 실험실
> 테스트베드인가, 배포 환경인가?** **3. 누구의 평가인가?** 이 셋에 답할 수 없게 만드는 결과
> 표는 측정이 아니라 실증을 보고하고 있는 것이다 — 그것도 정당한 기여이지만 다른 종류의
> 기여이고, 답할 수 있는 표와 나란히 비교되어서는 안 된다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] §2의 상태 함정 넷을 대고, 각각이 어떤 틀린 문장을 만드는지 말한다.
- [ ] MuJoCo와 Drake가 각각 접촉을 무엇으로 여기는지, 그 차이가 언제 중요한지 말한다.
- [ ] 지형 시뮬레이션의 정직한 권고와 거기 붙는 정확도 단서를 댄다.
- [ ] OXE 스키마가 표현할 수 없는 것과, 그것이 여기서 왜 중요한지 말한다.
- [ ] 이 페이지의 검증된 부재 셋을 댄다.
- [ ] 물체의 질량과 접촉 강성에서 접촉 진동수와 반암시적 오일러의 최대 안정 스텝을 밀리초로 대고, 그 스텝에서 명시적 오일러가 한 번의 튕김에 무엇을 하는지 말한다.

### 스스로 점검

1. 어떤 논문이 Isaac Sim의 변형체 실험에서 얻은 접촉력을 보고한다. 무엇이 문제인가?
2. 사용한 시뮬레이터를 인용해야 한다. Drake다. 무엇이라고 쓰겠는가?
3. 누군가 Genesis에 대해 "4,300만 FPS"를 인용한다. 어떻게 답하겠는가?
4. 관련 연구 절에 "DROID는 궤적 76,000개를 담고 있다"고 썼다. 언제 이것이 틀리는가?
5. 심사자가 왜 표준 건설 조작 벤치마크로 평가하지 않았느냐고 묻는다. 답은?
6. 어떤 논문이 40 g 도구 끝을 강성 40,000 N/m의 접촉에 대고 5 ms 스텝으로 시뮬레이션해 최대 접촉력을 보고한다. 무엇부터 확인하겠는가?

> [!tip]- 정답 · Answers
> 1. Isaac Sim 자신의 문서가 입자와 변형체는 **contact report를 지원하지 않는다**고 밝힌다 — 거기서는 변형체에서 접촉력을 읽어낼 수 없다. 힘이 다른 데서 왔거나(강체 프록시, 추정값) 논문이 그렇게 밝혔어야 하거나, 아니면 그 숫자가 보이는 것과 다르다. 변형체에는 정적 마찰과 마찰 결합 모드도 지원되지 않아 문제가 겹친다.
> 2. Drake가 스스로 제시하는 소프트웨어 인용 — 프로젝트 이름, 개발팀, URL을 담은 `@misc`. **심사받은 Drake 논문은 없으므로** venue를 지어내면 조작된 인용이 된다. 하이드로일래스틱 접촉을 썼다면 문서가 가리키는 접촉 모델 논문들(Castro 등)을 소프트웨어와 함께 인용하라.
> 3. 그 수치가 2024년 12월 README에서 나왔고, 방법론이 공개적으로 문제 제기되었으며 — 가장 빠른 물리 설정, 행동 1회 뒤 999스텝 무행동, 자기 충돌 해제 — 팀이 비판자의 하네스를 채택한 수정 벤치마크를 공개했고, **그 주장이 2026년 5월 철회 표시 없이 README에서 삭제되었다**고 답한다. 현재 공식 자료는 그런 주장을 하지 않는다. 살아 있는 수치로 인용해서는 안 된다.
> 4. RSS 프로시딩 판본을 인용할 때. 그 초록은 궤적 **65,000**개에 과제 86개라고 말한다. 76k/84는 arXiv 초록의 수치다. 둘 다 틀린 것이 아니고, 한쪽 인용에 다른 쪽 숫자를 붙이는 것이 틀린 것이다. BridgeData V2에도 같은 함정이 있다 — arXiv 60,096, PMLR 53,896.
> 5. 그런 것이 없다고, 분명히 말한다: 현장 건설 조작에는 공유 벤치마크가 없다 — 공유 프로토콜도, 공유 실물도, 리더보드도 없다 — 그리고 가장 가까운 RAMP는 *오프사이트* 건설을 틀로 삼는다. 방어 가능한 수는 부재를 진술하고, 가장 가까운 평가 장치를 빌려 오고(조립 채점은 NIST 태스크 보드, 또는 RAMP의 프로토콜), 남이 다시 돌릴 수 있을 만큼 명시적으로 자기 프로토콜을 정의하는 것이다 — 그리고 그것 자체가 공개할 가치가 있는 산출물이다. 이 단어에 주의할 점 둘. 제목에 건설 작업 "벤치마킹"을 단 논문은 이제 있다 — [arXiv:2512.14031](https://arxiv.org/abs/2512.14031)은 건설 스킬에서 VLA와 RL 정책을 비교하고, Construction Research Congress 2026에는 휴머노이드 제어기 벤치마킹 논문이 실려 있다 — 그러나 한 논문 안의 비교 평가는 공유 벤치마크가 아니다. 공유 벤치마크에는 공개 프로토콜, 공개 실물, 남이 결과를 보탤 수 있는 구조가 필요하다. 그리고 어느 것도 가동 중인 현장에 있지 않다. 여기서 말하는 부재는 바로 그것이고, 2026년 9월에 arXiv와 Crossref로 마지막으로 확인했다.
> 6. 접촉 진동수에 대한 스텝이다. $\omega=\sqrt{40{,}000/0.04}=1000\,\mathrm{rad/s}$이므로 $\omega\Delta t=5$ — 반암시적 오일러의 구간조차 벗어나고, 감쇠가 없으면 명시적 오일러에는 안정 스텝이 아예 없다. §3의 랩에 바로 이 쌍의 행이 있다. $0.1\,\mathrm{m/s}$에서 반암시적 오일러는 $0.5\,\mathrm{mm}$ 파고들어 정확한 $4\,\mathrm{N}$ 대신 $20\,\mathrm{N}$의 최대 힘을 보고하고, 에너지를 576배로 돌려준다. 접촉은 $3.1\,\mathrm{ms}$로 스텝 하나보다 짧으므로, 여기서 안정하게 남는 솔버 — 이를테면 암시적 솔버 — 라도 그 안의 힘을 분해할 수 없다. 적분기, 스텝, 접촉 파라미터를 묻고, 논문이 달리 보여 주기 전까지 그 힘을 시뮬레이션의 숫자로 읽어라.

### 과제 · Problem set

Tier A. 이 페이지, [[02-foundations/lab-kernel|0.65 Lab Kernel]], [[02-foundations/lab-plants|0.6 Lab Plants]]만으로 푼다. 변형은 **더 가벼운 핸들**: $m=0.02\,\mathrm{kg}$ — P3의 절반 — 이 같은 두 벽($400$과 $40{,}000\,\mathrm{N/m}$)에 같은 $v_0=0.1\,\mathrm{m/s}$로 닿는 순간부터 떨어지고, 따로 말하지 않으면 $d=0$이다. 원래 문제다. 영어 절의 템플릿을 채우고, 루프를 다시 쓰지 마라.

1. **그리기.** 변형의 과제 그림: $1\,\mathrm{ms}$의 단단한 벽 위 한 번의 튕김을 담은 $(\omega\delta,v)$ 평면 — 정확한 반원, 명시적 다각형, 반암시적 점들과 그것이 놓인 타원 — 그리고 두 벽을 $1\,\mathrm{ms}$에 표시하고 각 벽의 안정 스텝을 밀리초로 적은 $\omega\Delta t$ 띠.
2. **유도.** (a) 각 벽의 $\omega$, 접촉 시간, 정확한 최대 침투와 정확한 최대 힘. (b) 각 벽의 가장 큰 반암시적 안정 스텝, 그리고 두 벽을 모두 담은 장면이 써야 할 스텝. (c) $1\,\mathrm{ms}$의 단단한 벽에서 두 적분기로 한 번의 튕김을 손으로 전진: 에너지 비, 최대 침투, 최대 힘. $0.1\,\mathrm{m/s}$에서 어느 쪽이 RS1의 $10\,\mathrm{N}$ 선을 넘는가, 그리고 명시적 쪽은 어떤 $v_0$에서 넘겠는가? (d) $1\,\mathrm{ms}$에서 각 벽의 명시적 오일러를 안정하게 만드는 가장 작은 접촉 감쇠. 질량을 절반으로 줄인 것이 그것을 바꾸었는가? (e) $\zeta=0.1$일 때 단단한 벽의 반암시적 안정 스텝.
3. **실행.** 템플릿의 `?`를 채우고([[02-foundations/lab-kernel|0.65]]에 두 적분기가 있다) 변형의 감쇠 없는 스윕을 돌린다. 두 벽, $\Delta t\in\{0.1,1,2,5,20\}\,\mathrm{ms}$에서 두 적분기의 에너지 비와 최대 침투를 담은 표를 불안정한 칸을 표시해 보고한다. 그리고 답한다: (i) 페이지의 표에서 어느 칸이 바뀌었고, 왜 $\omega\Delta t$ 열 하나가 그것을 예측하는가; (ii) $1\,\mathrm{ms}$의 단단한 벽에서 반암시적 오일러의 정확한 1은 적분기의 성질인가? 그것을 판가름하는 표의 행을 짚어라; (iii) 두 벽 모두에 안정한, 격자 위의 가장 큰 스텝.

> [!tip]- 정답 · Solutions
> 1. 명시적 꼭짓점을 m/s 단위의 $(\omega\delta,v)$로 쓰면 $(0,0.1)$, $(0.141,0.1)$, $(0.283,-0.1)$, $(0.141,-0.5)$이고, 그다음 $v=-0.7$로 벽 밖에 나간다. $1+(\omega\Delta t)^2=3$이므로 각 꼭짓점이 앞의 것보다 $\sqrt3$배 멀다. 반암시적은 $(0,0.1)$, $(0.141,0.1)$, $(0,-0.1)$, 그다음 $-0.1$로 벽 밖이고, 모두 타원 $v^2+(\omega\delta)^2-\sqrt2\,(\omega\delta)\,v=0.01$ 위에 있다. 띠에서 패널은 $\omega\Delta t=0.141$, 단단한 벽은 $1.414$에 있고, 2 아래에 $14.1\,\mathrm{ms}$와 $1.41\,\mathrm{ms}$를 적는다.
> 2. (a) 패널: $\omega=\sqrt{400/0.02}=141.4\,\mathrm{rad/s}$, 접촉 $22.2\,\mathrm{ms}$, $v_0/\omega=0.707\,\mathrm{mm}$, $v_0\sqrt{km}=0.283\,\mathrm{N}$. 단단한 벽: $1414\,\mathrm{rad/s}$, $2.22\,\mathrm{ms}$, $0.0707\,\mathrm{mm}$, $2.83\,\mathrm{N}$. (b) $2/\omega$로 $14.1\,\mathrm{ms}$와 $1.41\,\mathrm{ms}$다. 두 벽을 담은 장면은 $\Delta t<1.41\,\mathrm{ms}$가 필요하다. (c) 이제 $\Delta t\,\omega^2=2000\,\mathrm{s^{-1}}$, $\Delta t\,v_0=0.1\,\mathrm{mm}$다. 명시적을 mm와 m/s의 $(\delta,v)$로 쓰면 $(0,0.1)\to(0.1,0.1)\to(0.2,-0.1)\to(0.1,-0.5)\to(-0.4,-0.7)$이므로 비는 $49$, 최대 침투 $0.2\,\mathrm{mm}$, 최대 힘 $8\,\mathrm{N}$이다. (벽면이나 그 안에서 시작한 네 스텝이 $v^2+\omega^2\delta^2$를 $3^4=81$배 하고, $-0.4\,\mathrm{mm}$의 벽 밖 샘플이 그중 $32$를 존재하지 않는 스프링에 담고 있어 $49$가 남는다.) 반암시적은 $(0,0.1)\to(0.1,0.1)\to(0,-0.1)\to(-0.1,-0.1)$이므로 $1$, $0.1\,\mathrm{mm}$, $4\,\mathrm{N}$이다. 이 최대 침투는 정확한 $0.0707\,\mathrm{mm}$의 $1.41$배이고, 그것이 타원의 가장 넓은 점 $1/\sqrt{1-\tfrac14\cdot2}$다. $0.1\,\mathrm{m/s}$에서는 어느 쪽도 $10\,\mathrm{N}$을 넘지 않는다. 명시적 최대 힘은 $v_0$에 비례하므로 $v_0=0.125\,\mathrm{m/s}$에서 넘고, 그때 정확한 최대 힘은 겨우 $3.54\,\mathrm{N}$이다. (d) $d\ge k\,\Delta t$이므로 패널에서 $0.4\,\mathrm{N{\cdot}s/m}$, 단단한 벽에서 $40\,\mathrm{N{\cdot}s/m}$다. 질량이 상쇄되므로 P3의 핸들과 같다. 감쇠비로는 $\zeta\ge\omega\Delta t/2=0.071$과 $0.71$이고, 이것은 질량에 달려 있다. (e) $2(\sqrt{1.01}-0.1)/1414=1.28\,\mathrm{ms}$.
> 3. 빈칸은 영어 해와 같다. 표에서 굵게 쓴 칸이 불안정한 스텝이다(명시적 칸 전부와 $\omega\Delta t\ge2$인 반암시적 칸).
>
> | $k$ (N/m) | $\Delta t$ (ms) | $\omega\Delta t$ | 비, 명시적 | 비, 반암시적 | 최대 침투, 명시적 (mm) | 최대 침투, 반암시적 (mm) |
> |---:|---:|---:|---:|---:|---:|---:|
> | 400 | 0.1 | 0.014 | **1.045** | 1.000 | 0.715 | 0.707 |
> | 400 | 1 | 0.141 | **1.564** | 1.003 | 0.791 | 0.709 |
> | 400 | 2 | 0.283 | **2.449** | 1.005 | 0.888 | 0.708 |
> | 400 | 5 | 0.707 | **8.266** | 1.129 | 1.250 | 0.750 |
> | 400 | 20 | 2.828 | **529** | **49** | 4.000 | 2.000 |
> | 40,000 | 0.1 | 0.141 | **1.564** | 1.003 | 0.079 | 0.071 |
> | 40,000 | 1 | 1.414 | **49** | 1.000 | 0.200 | 0.100 |
> | 40,000 | 2 | 2.828 | **529** | **49** | 0.400 | 0.200 |
> | 40,000 | 5 | 7.071 | **$2.22\times10^4$** | **2,401** | 1.000 | 0.500 |
> | 40,000 | 20 | 28.28 | **$5.755\times10^6$** | **$6.384\times10^5$** | 4.000 | 2.000 |
>
> (i) $\omega\propto1/\sqrt m$이므로 모든 $\omega\Delta t$가 페이지의 $\sqrt2$배이고, 각 칸은 페이지의 칸을 $\sqrt2$배 스텝에서 본 것처럼 행동한다. 단단한 벽의 $2\,\mathrm{ms}$ 칸은 구간을 넘어($2.83>2$) $9$에서 $49$가 되고, $1\,\mathrm{ms}$의 명시적 칸은 $16$에서 $49$가 된다. (ii) 아니다. $\omega\Delta t=\sqrt2$에서 반암시적 스텝은 위상을 정확히 $90^\circ$씩 돌리므로($\cos\theta=1-\tfrac12\cdot2=0$) 핸들이 샘플 위에서 벽면으로 돌아온다. 같은 적분기로 $5\,\mathrm{ms}$의 패널($\omega\Delta t=0.707$)은 $1.129$를 돌려준다. (iii) $1\,\mathrm{ms}$다. $2\,\mathrm{ms}$에서는 단단한 벽이 구간 밖이다.

### 출처

**2026-08-22**에 공식 출처로 확인했다. 규모 수치는 따로 표시하지 않는 한 각 논문 자신의
초록에서 인용한 것이고, 부재에 근거한 주장은 공식 페이지를 확인했으나 아무것도 없었다는 뜻이다.

**시뮬레이터** — [MuJoCo](https://mujoco.readthedocs.io/)(Todorov, Erez & Tassa, IROS 2012, pp. 5026–5033, DOI 10.1109/IROS.2012.6386109); [Isaac Sim](https://developer.nvidia.com/isaac/sim)과 [Isaac Lab](https://isaac-sim.github.io/IsaacLab/)(선행 Orbit: Mittal et al., *RA-L* 8(6), 2023, DOI 10.1109/LRA.2023.3270034); [Isaac Gym 레거시 고지](https://developer.nvidia.com/isaac-gym); [Bullet](https://github.com/bulletphysics/bullet3); [Gazebo](https://gazebosim.org/docs/latest/releases/)와 [Classic 수명 종료 고지](https://classic.gazebosim.org/)(Koenig & Howard, IROS 2004, pp. 2149–2154); [Drake](https://drake.mit.edu/)와 [하이드로일래스틱 접촉 가이드](https://drake.mit.edu/doxygen_cxx/group__hydroelastic__user__guide.html); [SAPIEN](https://github.com/haosulab/SAPIEN)(Xiang et al., CVPR 2020, pp. 11094–11104); [Genesis World](https://github.com/Genesis-Embodied-AI/genesis-world), [벤치마크 이슈](https://github.com/Genesis-Embodied-AI/genesis-world/issues/181), [MuJoCo 논의](https://github.com/google-deepmind/mujoco/discussions/2303).

**지형** — [agxTerrain 사용자 매뉴얼](https://www.algoryx.se/documentation/complete/agx/tags/latest/doc/UserManual/source/agxTerrain.html); M. Servin, T. Berglund, S. Nystedt, "A multiscale model of terrain dynamics for real-time earthmoving simulation," *Advanced Modeling and Simulation in Engineering Sciences* 8:11, 2021, DOI 10.1186/s40323-021-00196-3; [Vortex Studio 라이선싱](https://vortexstudio.atlassian.net/wiki/spaces/VSD2511/pages/4607410452); [Project Chrono 지형 모델](https://api.projectchrono.org/vehicle_terrain.html)과 CRM은 Unjhawala et al., [arXiv:2507.05643](https://arxiv.org/abs/2507.05643).

**벤치마크** — RLBench([arXiv:1909.12271](https://arxiv.org/abs/1909.12271)); Meta-World(CoRL 2019, PMLR v100); ManiSkill 3([arXiv:2410.00425](https://arxiv.org/abs/2410.00425) — RSS 프로시딩 제목이 arXiv 제목과 다르다); CALVIN([arXiv:2112.03227](https://arxiv.org/abs/2112.03227)); LIBERO([arXiv:2306.03310](https://arxiv.org/abs/2306.03310)); FurnitureBench(RSS 2023, DOI 10.15607/RSS.2023.XIX.041); RoboCasa(RSS 2024, DOI 10.15607/RSS.2024.XX.050 — 프로시딩 제목은 "Household", arXiv는 "Everyday"); [NIST Assembly Task Boards](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly)(Kimble et al., *RA-L* 2020, DOI 10.1109/LRA.2020.2965869; 변형체는 Kimble et al., *Frontiers in Robotics and AI* 9, 2022, DOI 10.3389/frobt.2022.999348); RAMP(*RA-L* 9(1):9–16, 2024, DOI 10.1109/LRA.2023.3330611).

**데이터셋** — [Open X-Embodiment](https://robotics-transformer-x.github.io/)(ICRA 2024, [arXiv:2310.08864](https://arxiv.org/abs/2310.08864), CC BY 4.0); DROID(RSS 2024, DOI 10.15607/RSS.2024.XX.120, [arXiv:2403.12945](https://arxiv.org/abs/2403.12945)); BridgeData V2(CoRL 2023, PMLR v229:1723–1736); [RH20T](https://rh20t.github.io/)(ICRA 2024, [arXiv:2307.00595](https://arxiv.org/abs/2307.00595)); FMB(*IJRR*, DOI 10.1177/02783649241276017); REASSEMBLE([arXiv:2502.05086](https://arxiv.org/abs/2502.05086)); Rohbau3D(*Scientific Data*, 2025, DOI 10.1038/s41597-025-05827-7, CC BY 4.0); ConRebSeg([arXiv:2407.09372](https://arxiv.org/abs/2407.09372)); ETHcavation([arXiv:2410.04250](https://arxiv.org/abs/2410.04250)); Hilti SLAM Challenge 2023([arXiv:2404.09765](https://arxiv.org/abs/2404.09765)); *OpenConstruction* 카탈로그([arXiv:2508.11482](https://arxiv.org/abs/2508.11482)); ConSLAM — ECCV 2022 Workshops, DOI 10.1007/978-3-031-25082-8_21, **그리고** *J. Comput. Civ. Eng.* 37(3):04023009, 2023, DOI 10.1061/JCCEE5.CPENG-5212.

**수치 적분** — E. Hairer, C. Lubich, G. Wanner, *Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations*, 2nd ed., Springer Series in Computational Mathematics 31, Springer, 2006 — 심플렉틱 오일러 방법과 그것이 보존하는 수정 에너지의 표준 참고문헌이다. §3과 계산 절의 안정 구간, 에너지 띠, 감쇠 조건은 이 페이지에서 유도하고 랩으로 확인했다.

**이 위키 안에서**

- [[05-construction-robotics/sim-to-real|필드 로봇 Sim-to-Real]] — 이 도구들이 놓인 reality gap
- [[06-research-practice/experimental-design-reproducibility|실험 설계와 재현성]] — 평가가 무엇을 고정해야 하는가
- [[06-research-practice/real-world-impact|6. 실세계 임팩트]] — 여기서 공개 데이터셋이 다른 곳보다 값어치 있는 이유
- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 이 부재들이 부재인 대상 작업들
- [[02-foundations/lab-kernel|0.65 Lab Kernel]] — 낙하 셀이 비교하는 두 적분기
- [[04-robotics/contact-force-tactile|9. 접촉·힘·촉각]] — 낙하 셀의 벽이 쓰는 페널티 법칙
- [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]] — 같은 핸들 위의 다른 에너지원, 제어기의 홀드
