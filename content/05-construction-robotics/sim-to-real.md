---
title: "7.5 Sim-to-Real for Field Robots"
tags: [construction, sim-to-real, robotics, learning]
study-depth: Working
wiki-support: Working
depth-goal: "On S2's trench, turn a sim-to-real gap into a number, say what range a randomized controller must cover and what share of real soils it reaches, size an identification from a few passes, bound a residual, and place any transfer paper on the deployment ladder."
mastery-when: "Raise to Mastery when this task stream or deployment layer is the thesis contribution."
---

## English

Simulation makes dangerous, slow, and expensive robot experience cheap. It does not make
that experience real. **Sim-to-real** is the set of modeling, training, adaptation, and
evaluation practices used to keep a policy useful when its simulator assumptions fail.

> [!info] Depth target
> Read a sim-to-real paper and identify: which gap (dynamics, contact, sensing, task,
> implementation) dominates, which strategy addresses it and at what cost, what real-data
> and intervention budget the transfer consumed, and which rung of the deployment ladder
> the evidence actually reaches. Designing transfer pipelines is a working/mastery topic.

> [!note] Prerequisites
> [[05-construction-robotics/site-engineering|2.5 Site Robotics as an Engineering System]] (S2, this page's object) · [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] (the machine, and why its soil is unknown) · [[02-foundations/probability|3. Probability §2–§3]] (the CDF, the Gaussian, and the spread of a mean) · [[02-foundations/rl-basics|7. RL Basics]] (policy and return) · [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §4–§5]] (RL on a machine, safety filters, "zero-shot") · [[04-robotics/system-identification|5.5 System Identification §1, §3–§6]] (least squares, excitation, noise in the regressor, held-out validation) · [[04-robotics/contact-force-tactile|9. Contact §3]] (the contact models behind §1's warning) · [[04-robotics/robot-systems-deployment|10. Robot Systems §3, §9]] (a delay as a distance; staged deployment)

> [!note] First pass · 처음이라면
> Read the running object and look at the picture: S2's trench, and what one simulator number — the soil's cutting resistance — does to a controller when the real soil is harder. Then §1 for the gap as a number, §2 for the strategies, and §6–§8, which price three of them on S2; the Worked case after §8 puts all of them on one site. §3–§5 are what you use to place a paper on the ladder, including §4's example that six parameters randomized at 80% coverage each cover only 26% of real conditions, and §9 is the lab.

### Running object · 이 페이지의 대상

**S2** from [[05-construction-robotics/site-engineering|2.5 Site Robotics as an Engineering System]]: the $5$-tonne-class excavator digging the $20\,\mathrm{m}$ long, $0.6\,\mathrm{m}$ wide, $1.0\,\mathrm{m}$ deep utility trench to a bottom grade of $\pm30\,\mathrm{mm}$. S2 freezes the soil's specific cutting resistance at $k_c=60\,\mathrm{kPa}$, the cutting force per unit area of the slice's cross-section. A bucket of width $w$ cutting a slice of depth $d$ cuts a cross-section $w\,d$, so the cutting force is

$$F_c=k_c\,w\,d,$$

in kilonewtons when $k_c$ is in kilopascals and $w\,d$ in square metres: the simplest cutting model that 2.5's definition allows, defined in full, with the conditions under which it holds, in [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §2]]. This page reads S2's $60\,\mathrm{kPa}$ as **the simulator's soil**, $k_{\text{sim}}$, and asks what happens when the ground under the real bucket differs. 2.5 says a real site's soil has to be measured; this is the page that measures it.

The controller being transferred is a force-based dig controller tuned in simulation, a course model: on every pass it pushes the bucket with the cutting force that, in the simulator's soil, cuts the planned slice.

| Symbol | Value | What it is |
|---|---:|---|
| $k_{\text{sim}}$ | $60\,\mathrm{kPa}$ | S2's $k_c$, read here as the simulator's soil |
| $w$ | $0.6\,\mathrm{m}$ | S2's bucket width, equal to the trench width |
| $d_0$ | $0.1\,\mathrm{m}$ | the slice the controller was tuned to cut per pass |
| $F_b$ | $3.6\,\mathrm{kN}$ | the force it pushes, $k_{\text{sim}}\,w\,d_0=60\times0.6\times0.1$ |
| $k_{\text{site}}$ | $80\,\mathrm{kPa}$ | the worked case's real site |
| site distribution | $\ln k_c\sim\mathcal N(\ln60,\ 0.25^2)$ | how $k_c$ spreads over the sites S2 might be dug on: lognormal, median $60\,\mathrm{kPa}$ (§6) |
| $[k_{lo},\ k_{hi}]$ | $[40,\ 80]\,\mathrm{kPa}$ | the worked case's randomization range |
| $\sigma_F$ | $0.3\,\mathrm{kN}$ | scatter of the cutting force measured on one pass |

$d_0$, $k_{\text{site}}$, the site distribution, the range and $\sigma_F$ are this page's own frozen numbers, and they are course numbers too: the site distribution is a teaching assumption, not a survey of real soils. Everything else is S2's, including $V_b$, $k_f$, $s$ and $T_c$, which the worked case turns into productivity, and $\tau_h$ and $v$, which §3 turns into a distance.

*Scope: this page teaches the reality gap as a measured number, domain randomization and the coverage of its range, identifying one soil parameter from a few passes, residual and adaptive policies, and the ladder that grades transfer evidence, all on S2's soil. It does not teach identification in general ([[04-robotics/system-identification|5.5 System Identification]]), RL fine-tuning and safety filters ([[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §4]]), privileged teacher–student distillation ([[04-robotics/legged-locomotion|18. Legged Locomotion §2]]), or which simulator models soil and how well ([[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets §4]]).*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 346" style="max-width:100%;height:auto" role="img" aria-label="Slice depth per pass against the soil's specific cutting resistance. The simulator-tuned controller pushes 3.6 kN and cuts 0.100 m at 60 kPa but 0.075 m at 80 kPa. A controller adapted over 40 to 80 kPa holds 0.100 m across that range; a blind controller made safe over the same range cuts 0.067 m at 60 kPa and 0.050 m at 80 kPa. Below, the page's site distribution of the cutting resistance: 82.3 percent of sites lie inside 40 to 80 kPa, 5.2 percent are softer and 12.5 percent harder.">
<text x="16" y="18" font-size="12" fill="currentColor" font-weight="600">slice cut per pass against the soil's cutting resistance</text>
<rect x="158.4" y="66.0" width="188.8" height="160.0" fill="currentColor" fill-opacity="0.07"/>
<text x="252.8" y="78.0" font-size="10.5" fill="currentColor" text-anchor="middle">trained on 40–80 kPa</text>
<line x1="64.0" y1="226.0" x2="536.0" y2="226.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="64.0" y1="66.0" x2="64.0" y2="226.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="60.0" y1="226.0" x2="64.0" y2="226.0" stroke="currentColor"/><text x="57.0" y="229.5" font-size="10" fill="currentColor" text-anchor="end">0.00</text>
<line x1="60.0" y1="181.6" x2="64.0" y2="181.6" stroke="currentColor"/><text x="57.0" y="185.1" font-size="10" fill="currentColor" text-anchor="end">0.05</text>
<line x1="60.0" y1="137.1" x2="64.0" y2="137.1" stroke="currentColor"/><text x="57.0" y="140.6" font-size="10" fill="currentColor" text-anchor="end">0.10</text>
<line x1="60.0" y1="92.7" x2="64.0" y2="92.7" stroke="currentColor"/><text x="57.0" y="96.2" font-size="10" fill="currentColor" text-anchor="end">0.15</text>
<text x="57.0" y="60.0" font-size="10" fill="currentColor" text-anchor="end">slice (m)</text>
<line x1="64.0" y1="137.1" x2="536.0" y2="137.1" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="3 3"/>
<text x="534.0" y="150.1" font-size="10" fill="currentColor" text-anchor="end">planned slice d₀ = 0.10 m</text>
<line x1="64.0" y1="110.4" x2="536.0" y2="110.4" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="1 3"/>
<text x="534.0" y="106.4" font-size="10" fill="currentColor" text-anchor="end">30 mm too deep: off grade on the last pass</text>
<polyline points="126.9,66.0 137.2,75.8 147.4,84.4 157.6,92.1 167.8,99.0 178.1,105.2 188.3,110.9 198.5,116.0 208.7,120.7 219.0,125.1 229.2,129.0 239.4,132.7 249.7,136.1 259.9,139.3 270.1,142.2 280.3,145.0 290.6,147.6 300.8,150.0 311.0,152.3 321.2,154.4 331.5,156.4 341.7,158.3 351.9,160.2 362.1,161.9 372.4,163.5 382.6,165.0 392.8,166.5 403.1,167.9 413.3,169.3 423.5,170.5 433.7,171.8 444.0,172.9 454.2,174.1 464.4,175.1 474.6,176.2 484.9,177.1 495.1,178.1 505.3,179.0 515.5,179.9 525.8,180.7 536.0,181.6" fill="none" stroke="currentColor" stroke-width="2"/>
<polyline points="74.5,66.0 79.7,73.6 85.0,80.5 90.2,86.9 95.5,92.7 100.7,98.0 106.0,102.9 111.2,107.5 116.4,111.7 121.7,115.7 126.9,119.3 132.2,122.8 137.4,126.0 142.7,129.0 147.9,131.9 153.2,134.6 158.4,137.1 347.2,137.1 359.0,139.8 370.8,142.3 382.6,144.7 394.4,147.0 406.2,149.1 418.0,151.1 429.8,153.1 441.6,154.9 453.4,156.6 465.2,158.3 477.0,159.9 488.8,161.4 500.6,162.8 512.4,164.2 524.2,165.5 536.0,166.7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="8 4" stroke-opacity="0.8"/>
<polyline points="74.5,66.0 86.0,81.9 97.6,94.9 109.1,105.7 120.6,114.9 132.2,122.8 143.7,129.6 155.3,135.6 166.8,140.9 178.3,145.6 189.9,149.8 201.4,153.6 212.9,157.0 224.5,160.2 236.0,163.0 247.6,165.6 259.1,168.0 270.6,170.3 282.2,172.3 293.7,174.2 305.2,176.0 316.8,177.7 328.3,179.2 339.9,180.7 351.4,182.0 362.9,183.3 374.5,184.5 386.0,185.7 397.5,186.8 409.1,187.8 420.6,188.8 432.2,189.7 443.7,190.6 455.2,191.4 466.8,192.2 478.3,193.0 489.8,193.7 501.4,194.4 512.9,195.1 524.5,195.8 536.0,196.4" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="2 3"/>
<line x1="16" y1="32.5" x2="40" y2="32.5" stroke="currentColor" stroke-width="2"/><text x="46" y="36" font-size="10" fill="currentColor">fixed 3.6 kN, tuned at 60 kPa</text>
<line x1="288" y1="32.5" x2="312" y2="32.5" stroke="currentColor" stroke-width="2.4" stroke-dasharray="8 4"/><text x="318" y="36" font-size="10" fill="currentColor">adaptive, trained on 40–80 kPa</text>
<line x1="16" y1="46.5" x2="40" y2="46.5" stroke="currentColor" stroke-width="2" stroke-dasharray="2 3"/><text x="46" y="50" font-size="10" fill="currentColor">blind, made safe on 40–80 kPa</text>
<circle cx="252.8" cy="137.1" r="3.8" fill="currentColor"/>
<text x="257.8" y="128.1" font-size="10" fill="currentColor">simulator’s soil, 60 kPa: 0.100</text>
<circle cx="347.2" cy="159.3" r="3.8" fill="currentColor"/>
<text x="354.2" y="163.3" font-size="10" fill="currentColor">0.075</text>
<circle cx="347.2" cy="181.6" r="3" fill="currentColor"/>
<text x="354.2" y="194.6" font-size="10" fill="currentColor">0.050</text>
<circle cx="347.2" cy="137.1" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
<text x="64.0" y="246.0" font-size="10" fill="currentColor">how the soil varies over S2's sites (lognormal, median 60 kPa)</text>
<polygon points="64.0,288.0 64.0,288.0 71.9,288.0 79.7,287.9 87.6,287.8 95.5,287.6 103.3,287.2 111.2,286.5 119.1,285.5 126.9,284.0 134.8,282.1 142.7,279.8 150.5,277.0 158.4,274.0 166.3,270.7 174.1,267.3 182.0,264.0 189.9,260.9 197.7,258.2 205.6,255.9 213.5,254.1 221.3,252.9 229.2,252.2 237.1,252.0 244.9,252.3 252.8,253.1 260.7,254.3 268.5,255.7 276.4,257.4 284.3,259.3 292.1,261.2 300.0,263.3 307.9,265.3 315.7,267.3 323.6,269.3 331.5,271.1 339.3,272.9 347.2,274.5 355.1,276.0 362.9,277.4 370.8,278.7 378.7,279.8 386.5,280.8 394.4,281.8 402.3,282.6 410.1,283.3 418.0,283.9 425.9,284.5 433.7,285.0 441.6,285.4 449.5,285.8 457.3,286.1 465.2,286.4 473.1,286.6 480.9,286.8 488.8,287.0 496.7,287.1 504.5,287.3 512.4,287.4 520.3,287.5 528.1,287.6 536.0,287.6 536.0,288.0" fill="currentColor" fill-opacity="0.12"/>
<polygon points="158.4,288.0 158.4,274.0 166.3,270.7 174.1,267.3 182.0,264.0 189.9,260.9 197.7,258.2 205.6,255.9 213.5,254.1 221.3,252.9 229.2,252.2 237.1,252.0 244.9,252.3 252.8,253.1 260.7,254.3 268.5,255.7 276.4,257.4 284.3,259.3 292.1,261.2 300.0,263.3 307.9,265.3 315.7,267.3 323.6,269.3 331.5,271.1 339.3,272.9 347.2,274.5 347.2,288.0" fill="currentColor" fill-opacity="0.32"/>
<polyline points="64.0,288.0 71.9,288.0 79.7,287.9 87.6,287.8 95.5,287.6 103.3,287.2 111.2,286.5 119.1,285.5 126.9,284.0 134.8,282.1 142.7,279.8 150.5,277.0 158.4,274.0 166.3,270.7 174.1,267.3 182.0,264.0 189.9,260.9 197.7,258.2 205.6,255.9 213.5,254.1 221.3,252.9 229.2,252.2 237.1,252.0 244.9,252.3 252.8,253.1 260.7,254.3 268.5,255.7 276.4,257.4 284.3,259.3 292.1,261.2 300.0,263.3 307.9,265.3 315.7,267.3 323.6,269.3 331.5,271.1 339.3,272.9 347.2,274.5 355.1,276.0 362.9,277.4 370.8,278.7 378.7,279.8 386.5,280.8 394.4,281.8 402.3,282.6 410.1,283.3 418.0,283.9 425.9,284.5 433.7,285.0 441.6,285.4 449.5,285.8 457.3,286.1 465.2,286.4 473.1,286.6 480.9,286.8 488.8,287.0 496.7,287.1 504.5,287.3 512.4,287.4 520.3,287.5 528.1,287.6 536.0,287.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="64.0" y1="288.0" x2="536.0" y2="288.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="64.0" y1="288.0" x2="64.0" y2="292.0" stroke="currentColor"/><text x="64.0" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">20</text>
<line x1="158.4" y1="288.0" x2="158.4" y2="292.0" stroke="currentColor"/><text x="158.4" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">40</text>
<line x1="252.8" y1="288.0" x2="252.8" y2="292.0" stroke="currentColor"/><text x="252.8" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">60</text>
<line x1="347.2" y1="288.0" x2="347.2" y2="292.0" stroke="currentColor"/><text x="347.2" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">80</text>
<line x1="441.6" y1="288.0" x2="441.6" y2="292.0" stroke="currentColor"/><text x="441.6" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">100</text>
<line x1="536.0" y1="288.0" x2="536.0" y2="292.0" stroke="currentColor"/><text x="536.0" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">120</text>
<text x="300.0" y="318.0" font-size="10.5" fill="currentColor" text-anchor="middle">the soil's specific cutting resistance (kPa)</text>
<text x="300.0" y="336.0" font-size="10.5" fill="currentColor" text-anchor="middle">sites: 5.2% softer than 40 kPa · 82.3% inside the range · 12.5% harder than 80 kPa</text>
</svg>

S2's slice per pass against the soil's cutting resistance. The simulator-tuned controller pushes $3.6\,\mathrm{kN}$, which cuts the planned $0.100\,\mathrm{m}$ only in the simulator's $60\,\mathrm{kPa}$ soil and $0.075\,\mathrm{m}$ at $80\,\mathrm{kPa}$, a quarter short; a controller that senses the resistance and was trained on $40$–$80\,\mathrm{kPa}$ holds $0.100\,\mathrm{m}$ across that range, while a blind one made safe on the same range cuts $0.067\,\mathrm{m}$ at $60$ and $0.050\,\mathrm{m}$ at $80\,\mathrm{kPa}$. The strip is the page's site distribution: the range covers $82.3\%$ of sites and misses $5.2\%$ softer and $12.5\%$ harder.

### 1. Where the reality gap comes from

*In one sentence:* the gap is not a simulator's error but what that error does to one policy's task metric, so the same wrong number can cost one controller a quarter of every slice and another nothing.

| Gap | Examples in field robots | Typical response |
|---|---|---|
| Dynamics | mass, friction, hydraulic delay, backlash | system identification, parameter randomization, residual models |
| Contact/material | soil, rubble, tire slip, cutting resistance | randomized terrain, learned contact models, online adaptation |
| Sensing | dust, glare, vibration, latency, missing returns | sensor noise/latency models, augmentation, robust estimation |
| Task distribution | unseen sites, geometry, weather, operators | diverse procedural scenes, curriculum, real-data fine-tuning |
| Software/hardware | control rate, saturation, dropped messages | hardware-in-the-loop, action delay and limit randomization |

The important question is not “Was simulation photorealistic?” but **which variables
that affect the policy were represented, varied, or adapted**.

**S2's gap, in the contact/material row.** S2's cutting resistance is one entry of the second row, and it is one number: the simulator says $60\,\mathrm{kPa}$ and the site says whatever its soil says. On the worked case's site, $80\,\mathrm{kPa}$, the force that cuts the planned $0.1\,\mathrm{m}$ in simulation cuts $0.075\,\mathrm{m}$. The simulator's side of that comparison is not exact either: the leading real-time soil models are validated only to roughly 10–25% of a particle-level reference ([[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets §4]]), so a digging force read off any of them carries that error before the site adds its own. The shortfall is the gap, and it needs a definition precise enough to measure, because the looser use of the word names the mismatches themselves, the rows of the table, which this page calls the gap's *sources*.

> **Reality gap, defined.** The **reality gap** of a policy is a *measured difference in task performance*, what one policy achieves in the simulator against what it achieves on the real system. It is not a property of the simulator alone, and not the parameter error that causes it. Three defining conditions. **One frozen policy**: nothing about it is updated between the two evaluations, or the difference measures adaptation, not the gap. **One task and one metric** in both worlds: the same task cases, initial conditions and definition of success, so the two numbers can be compared. And **both numbers are measured**: the simulated one in the simulator, the real one on the real system, neither predicted from the other.
>
> $$\rho=\frac{J_{\text{real}}(\pi)}{J_{\text{sim}}(\pi)},\qquad \Delta J=J_{\text{sim}}(\pi)-J_{\text{real}}(\pi)$$
>
> where $\pi$ is the policy, $J$ its task metric (a success rate, a slice depth, a volume per hour), and $\rho$ the real-to-sim performance ratio that §4 lists among the useful measures; $\rho=1$ means no gap on this metric, since the policy then does in reality what it did in simulation.
>
> - **Example**: S2's controller, metric the slice per pass. In simulation $J_{\text{sim}}=0.100\,\mathrm{m}$; on the $80\,\mathrm{kPa}$ site the same $3.6\,\mathrm{kN}$ cuts $3.6/(80\times0.6)=0.075\,\mathrm{m}$, so $\rho=0.75$ and $\Delta J=25\,\mathrm{mm}$.
> - **Non-example**: "the simulator's $k_c$ is $20\,\mathrm{kPa}$ too low." That is the cause, a parameter error, and its gap depends on the policy: the same $20\,\mathrm{kPa}$ costs the fixed-force controller a quarter of every slice and costs nothing to a controller that senses resistance and was trained on $40$–$80\,\mathrm{kPa}$ (§6).
> - **Non-example**: simulated success against real success after the policy was fine-tuned on real passes. The second number belongs to a different policy, so the difference mixes the gap with what adaptation recovered.
> - **Why it matters**: because the gap belongs to a policy–simulator pair, it can be closed from either side, by making the simulator right (identification, §7) or by making the policy insensitive to what the simulator got wrong (randomization, residuals, adaptation: §6, §8). A paper that reports only simulator fidelity, or only real success, has reported half of it.

**The sign of the gap decides which requirement fails.** On softer ground the same $3.6\,\mathrm{kN}$ cuts deeper: at $40\,\mathrm{kPa}$ it cuts $3.6/(40\times0.6)=0.150\,\mathrm{m}$, $50\,\mathrm{mm}$ more than planned. Mid-trench that is extra soil, and the bucket caps it: the planned pass fills the bucket to $k_f=0.85$ of its heaped capacity, so no pass carries more than $1/0.85=1.18$ times the planned volume, and the rest spills. On the pass that reaches the bottom it is over-excavation outside S2's $\pm30\,\mathrm{mm}$ grade. On harder ground the failure is productivity instead. One simulator number breaks two different requirements, depending on which way reality moved it.

> [!warning] The contact row is not like the others
> Every gap can contain both a *parameter* error and a **model-form or coverage** error.
> Diagnose whether the range is wrong or whether a phenomenon, state, event, or task case is
> missing before choosing identification or randomization. Contact is where model-form error
> is especially likely to dominate.
> Rigid-body engines resolve contact as point constraints solved per timestep: at each small
> time step the engine picks a few contact points and computes the forces that keep the
> bodies from passing through each other, then moves everything forward. The
> underlying dynamics are genuinely non-smooth — impacts and stick–slip transitions are
> discontinuities, and numerical integrators lose both accuracy and stability exactly there.
> Randomizing the friction coefficient does not fix a contact model that cannot represent
> the contact patch in the first place.
>
> This is why a contact-rich result and a locomotion result are not comparable evidence of
> sim-to-real maturity, even when both come from the same simulator. Legged locomotion
> tolerates a crude contact model because the policy is rejecting disturbance at 50 Hz over
> a foot that only needs to not slip; insertion, drilling and panel seating are *defined* by
> the contact patch the model is failing to represent. Treat "we transferred from
> simulation" as a claim whose strength depends on which side of that line the task sits.

<svg viewBox="0 0 560 282" style="max-width:100%;height:auto" role="img" aria-label="a parameter gap where randomization spans the real curve, next to a contact gap where every simulated curve is smooth and the real one has a jump">
  <g font-size="11" fill="currentColor">
    <text x="50" y="16">a parameter problem</text><text x="330" y="16">a model problem</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.75">
    <text x="50" y="29">dynamics &#183; sensing &#183; task distribution &#183; implementation</text><text x="330" y="29">contact &#8212; friction against slip velocity</text>
  </g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.5" fill="none">
    <polyline points="50,40 50,150 250,150"/>
    <line x1="330" y1="105" x2="530" y2="105"/>
    <line x1="430" y1="44" x2="430" y2="154"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.4" stroke-dasharray="5 4">
    <path d="M50,132 C110,106 180,84 250,72"/>
    <path d="M50,144 C110,122 180,102 250,92"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <path d="M50,138 C110,114 180,93 250,82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.45" stroke-dasharray="5 4">
    <path d="M338,74 C412,74 448,136 522,136"/>
    <path d="M338,86 C412,86 448,124 522,124"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <polyline points="338,66 428,66"/>
    <polyline points="432,144 522,144"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="62" y="58">the real system lies inside the spread</text>
    <text x="330" y="176">every simulated curve is smooth</text>
    <text x="330" y="190">the real one jumps at the stick&#8211;slip transition</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">Left: the physics is right and a number is wrong, so a distribution over that number covers the</text>
    <text x="24" y="228">real system. Right: stick becomes slip discontinuously, and a regularized rigid-body contact</text>
    <text x="24" y="244">passes smoothly through exactly there. Randomizing the friction coefficient slides those curves</text>
    <text x="24" y="260">up and down; it does not give them a shape they cannot take. That is the whole reason a</text>
    <text x="24" y="276">locomotion transfer and an insertion transfer are not comparable evidence.</text>
  </g>
</svg>

**Which side of that line S2's soil sits on.** A soil at $80$ instead of $60\,\mathrm{kPa}$ is the left panel: the law $F_c=k_c\,w\,d$ is right and one number in it is wrong, so a range of $k_c$ can cover the site. A boulder under the trench is the right panel: no value of $k_c$ reproduces a force that jumps when the tooth meets rock, so no range of $k_c$ covers it, and whether a policy trained on a range copes anyway is an empirical question. Egli et al. (2022) asked it on a real 12-tonne excavator: their test site's soil was relatively soft, so they buried a block of granite in the digging path to emulate extremely hard soil, and their policy, trained on randomized soils drawn once per episode, dragged over the block and still filled the bucket ([[01-canonical-papers/notes/8-construction/egli-rl|note]]; §4 reads that evidence).

### 2. Main strategies

*In one sentence:* each strategy closes the gap from a different side, and on S2 each has a concrete form — measure $k_c$, train across it, let a student infer it, correct the controller within a bound, or adapt on a few real passes.

- **System identification** fits simulator parameters to measured trajectories. It makes
  one simulator more faithful but can overfit one machine and one operating condition.
  The stream's canonical payoff is [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL]]:
  a learned neural-network valve/actuator model makes the excavator simulator faithful
  enough that the RL policy runs on the real M545 without fine-tuning. On S2 it means measuring $k_c$ on the site from the force and depth of a few passes (§7); the method in general is [[04-robotics/system-identification|5.5 System Identification §1]].
- **Domain randomization** trains across a distribution of dynamics, sensing, and scene
  parameters. Success depends on whether the real system lies inside a useful training
  distribution; “more random” is not automatically better. On S2: a fresh $k_c$ for every training episode, drawn from $[40,\ 80]\,\mathrm{kPa}$. Defined below; §6 prices the range.
- **Teacher–student / privileged learning** lets a teacher observe simulator-only state
  (terrain parameters, perfect pose) and distills behavior into a student using deployable
  observations. Always check what information exists at test time. On S2 the teacher sees $k_c$; a student that sees cylinder pressures and joint angles can recover it, because one pass's force and depth give $k_c=F_c/(w\,d)$, while a buried boulder stays invisible to it until the tooth strikes. The method is taught in [[04-robotics/legged-locomotion|18. Legged Locomotion §2]].
- **Residual learning** keeps a model-based controller and learns a correction. This can
  reduce the search space, but safety still depends on how the residual is bounded. On S2: keep the $3.6\,\mathrm{kN}$ controller and learn a correction $\Delta F$ with $\lvert\Delta F\rvert\le B$; §8 defines it and prices $B$.
- **Real-data adaptation** fine-tunes representations, dynamics, or policies using a
  small real dataset. Report how much real machine time and human intervention it costs. On S2 its cheapest form is §7's four supervised probe passes.
- **Parallel simulation** creates experience quickly; it improves sample throughput, not
  simulator validity. Thousands of environments can repeat the same wrong physics. On S2, ten thousand environments at $k_c=60\,\mathrm{kPa}$ teach the $60\,\mathrm{kPa}$ soil ten thousand times.

Domain randomization is the strategy most often named and least often specified, so it gets its full definition here.

> **Domain randomization, defined.** **Domain randomization** is a *training procedure*, training one policy across a distribution of simulator parameters. It is not a robustness result and not a test protocol. Four defining conditions. A named **parameter vector** $\theta$ of the simulator, here $k_c$. A **training distribution** $p_{\text{train}}(\theta)$ with a stated support and shape, sampled afresh for each episode. The policy is **not given $\theta$**: it acts from what it can observe, so whatever it learns has to work across the distribution. And the objective **averages over the distribution**:
>
> $$\pi^\star=\arg\max_{\pi}\ \mathbb{E}_{\theta\sim p_{\text{train}}}\big[J(\pi;\theta)\big]$$
>
> where $J(\pi;\theta)$ is the policy's return in the simulator run at parameters $\theta$, so the real system is served only insofar as it looks like one more draw from $p_{\text{train}}$, which is what §6's coverage measures.
>
> - **Example**: S2's controller trained with $k_c\sim\mathcal U[40,\ 80]\,\mathrm{kPa}$, a fresh soil each episode.
> - **Non-example**: the same draws with $k_c$ fed to the policy as an input. That is a policy conditioned on the soil, and on the machine it needs $k_c$ from somewhere: identification (§7) or a student that infers it (above).
> - **Non-example**: sweeping $k_c$ only at evaluation. That measures robustness; it trains nothing.
> - **Why it matters**: what the policy makes of the randomization depends on what it can sense. A policy that observes the cutting force can learn to adapt across the range; a blind one can only hedge against the range's worst member, and pays for the width at every soil (§6).

### 3. A deployment ladder

1. Simulator-only evaluation with held-out parameters —
   [[01-canonical-papers/notes/8-construction/exact-2024|ExACT]] sits here: end-to-end
   imitation from multimodal sensors to hydraulic valve commands, validated in simulation
   only, so its claim stops at this rung.
2. Hardware-in-the-loop and timing/saturation tests.
3. Slow, supervised real trials inside a safety envelope.
4. Adaptation without changing the evaluation cases: the policy may be updated on real data, but the test tasks, sites, and conditions used to score it stay fixed and are never used for tuning.
5. Repeated operation across materials, machines, sites, and days.

Zero-shot transfer means no target-domain training update before deployment; it does not
mean no real-system knowledge was used to build or tune the simulator.

> **Zero-shot transfer, defined.** **Zero-shot transfer** is a property of a *deployment protocol*, of what was allowed to change between the end of training and the real evaluation. It is not a statement about how the simulator was built, nor about the policy's internal state. Three defining conditions. The policy's trained **parameters are frozen** from the end of simulation training through the real evaluation. **No target-domain data enters a training update**, before or during the evaluation. And the evaluation is **on the target system**; a held-out simulator is rung 1, not transfer.
>
> $$\phi_{\text{deployed}}=\phi_{\text{sim}}$$
>
> where $\phi$ are the policy's trained parameters (a network's weights, a controller's tuned constants) and $\phi_{\text{sim}}$ their values at the end of simulation training, so an estimate the policy computes online may change during the evaluation while the parameters that compute it may not.
>
> - **Example**: S2's adaptive controller trained on $[40,\ 80]\,\mathrm{kPa}$ and run on the $80\,\mathrm{kPa}$ site. Its estimate of the soil moves from pass to pass; its trained parameters do not.
> - **Example**: Egli RL on the M545 (§2) is zero-shot although real machine data built the actuator model inside the simulator. Werner et al. (2026) use the same learned weights on an 11.5-tonne excavator and on a 500-gram tabletop robot, deployed through a calibrated machine interface: zero-shot in the weights, with the real-system knowledge moved into the calibration.
> - **Non-example**: §7's probe passes followed by resetting the controller's $k_c$ to the estimate. A parameter of the deployed controller was fitted to target data, so that is few-shot adaptation, on rung 4 if the scoring cases stay fixed.
> - **Why it matters**: "zero-shot" answers one narrow question. Ask separately what real data built the simulator and what the policy adapts online, since either can carry most of the transfer; [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §5]] lists the phrase among those an RL experimental section must be checked for.

The ladder separates uncertainties because a physically plausible policy can still fail through timing or saturation on hardware. For example, a digging command that works with immediate simulated actuation may arrive too late through the real control interface. **The reading this gives you.** Name what each transition validates and keep later tuning out of the held-out evaluation. Moving up the ladder means adding evidence about a boundary, not simply filming the same behavior on a larger machine.

**The same ladder on S2.** Rung 1: train on $[40,\ 80]\,\mathrm{kPa}$ and evaluate on soils the training never drew, $35$ and $90\,\mathrm{kPa}$. Rung 2 is where S2's valve latency lives: a command reaches motion $\tau_h=0.15\,\mathrm{s}$ after it is sent, and on the finishing pass the tip moves at $v=0.3\,\mathrm{m/s}$, so it travels $\tau_h v=0.15\times0.3=0.045\,\mathrm{m}$ along its path before a correction takes effect. That is $45\,\mathrm{mm}$, one and a half times the $30\,\mathrm{mm}$ the grade allows on either side, and invisible in a simulator that actuates instantly ([[04-robotics/robot-systems-deployment|10. Robot Systems §3]] reads a delay as a distance the same way). Rung 3 is §7's probe passes, slow and supervised. Rung 4 re-identifies or adapts on real passes while the trench sections used for scoring stay fixed. Rung 5 samples §6's site distribution itself: other soils, machines and days.

### 4. Reading the evidence

> [!warning] Reading the claim · 핵심 주장 읽는 법
> “Successful sim-to-real transfer” proves transfer only for the reported machine,
> operating range, and intervention protocol. Find the randomized variables, real-data
> budget, safety controller, failed trials, and whether evaluation conditions were used
> while tuning. A video is evidence of possibility, not a transfer distribution.

Useful measures include real/sim performance ratio, interventions per hour, constraint
violations, performance across parameter shifts, adaptation data/time, and degradation
outside the training range.

> [!example] Worked example · 계산 예제
> **Marginal coverage is not joint coverage.** Suppose each of 6 randomized parameters covers 80% of its real marginal distribution. If the real parameters are independent, the chance of a real condition lying inside every range is 0.8⁶ ≈ **26%**. Covering 90% per parameter gives 0.9⁶ ≈ **53%**.
>
> **The reading this gives you.** Ask for variables, ranges, and dependencies before accepting a robustness claim. In the first hypothetical setting, about 74% of joint real conditions lie outside the randomization box. That is not a predicted failure rate, nor proof that all points inside were adequately sampled. Real parameter correlations also change the coverage; separate training support from actual transfer evaluation.

**The checklist, run on one paper.** Egli et al.'s soil-adaptive excavation (RA-L 2022) answers most of the box's questions in its own text, which is why it is worth reading closely. *Randomized variables and ranges*: six soil parameters of the fundamental equation of earthmoving, drawn uniformly at the start of every episode (cohesion $0$ to $105\,\mathrm{kPa}$, adhesion from $0$ up to the cohesion, internal friction angle $0.3$ to $0.8\,\mathrm{rad}$, unit weight $17$ to $22\,\mathrm{kN/m^3}$, soil–bucket friction angle $0.2$ to $0.4\,\mathrm{rad}$, a cavity-pressure factor $0$ to $300$), plus the soil height; the paper states no real-soil distribution, so coverage in §6's sense cannot be computed from it. *What the policy senses*: its observations include joint torques, which on the machine come from cylinder pressures, and they are noise-free in training. The authors also trained a policy without torque observations and found it overly cautious, staying well inside the machine's torque limits: §6's blind policy, met in a real training run. *Real data and rung*: the policy is trained only in simulation and run on a 12-tonne machine through the machine's own joint-velocity controllers, on a test site with relatively soft soil and a buried granite block, which places it on rung 3. *Failed or partial trials*: scoops started close to the machine are pulled up early to avoid self-collision, filling the bucket to about a third ($0.32$). *The metric*: the reported bucket fill is computed by integrating the bucket's path through the soil and assumes all of that material ends up in the bucket, so it is an estimate, not a measurement.

### 5. Where this stream is moving (2019–2025)

Counted as in [[05-construction-robotics/lineage|lineage §6]], construction robot titles that name learning — deep, reinforcement or imitation — rose from $9$ in 2019–2021 to $30$ in 2023–2025, from $7\%$ to $12\%$ of construction robot papers. The learning-for-control work in these journals includes reinforcement learning boosted by virtual demonstrations for long-horizon construction tasks (Huang et al., *AutCon* 146, 2023, [DOI](https://doi.org/10.1016/j.autcon.2022.104691)), prediction-based path planning via deep reinforcement learning (Cai et al., *J. Computing in Civil Engineering* 37, 2023, [DOI](https://doi.org/10.1061/(asce)cp.1943-5487.0001056)), safety-constrained reinforcement learning for human–robot collaboration (Duan et al., *AutCon* 174, 2025, [DOI](https://doi.org/10.1016/j.autcon.2025.106130)), and learning from demonstration, surveyed by Li et al. (*AEI* 62, 2024, [DOI](https://doi.org/10.1016/j.aei.2024.102625)). Transfer demonstrated on real hardware at construction scale is harder to find; [[01-canonical-papers/notes/8-construction/apolinarska-timber|Apolinarska et al.'s timber insertion]] is a verified construction-journal example, and foundation models had reached these journals in one title by 2025. So when you place a construction-journal learning paper on §3's ladder, read its methods section for where it was evaluated before assuming a rung.

### 6. How wide must the randomization be?

*In one sentence:* a randomization range is worth the share of real sites it covers, which takes a distribution of real soils to compute, and what the range buys depends on whether the policy can sense the soil: a blind policy pays for every kilopascal of width in shallower slices, an adaptive one does not.

**The real distribution comes first.** Coverage needs to know how the real parameter spreads over the deployments that matter, and for S2 this page freezes one. Across the sites the trench might be dug on, $\ln k_c$ is Gaussian with mean $\ln60$ and standard deviation $0.25$, so $k_c$ is **lognormal**: positive, skewed toward hard soils, with median $60\,\mathrm{kPa}$, which makes the simulator right on the median site and wrong on most others. It is a teaching assumption, chosen to be plausible in shape, not fitted to survey data. Probabilities come from the standard normal CDF, $\Phi(z)=P(Z\le z)$ for a standard normal $Z$ ([[02-foundations/probability|3. Probability §2–§3]]), since $\ln k_c$ is Gaussian: a site is harder than $80\,\mathrm{kPa}$ with probability $1-\Phi\big(\ln(80/60)/0.25\big)=1-\Phi(1.151)=0.125$, so one site in eight is harder than the worked case's.

> **Randomization coverage, defined.** **Coverage** is a *probability*, a property of a training range taken together with a distribution of real conditions, not a property of the range alone. Three defining conditions. A stated **distribution of the real parameter** over the deployments that matter, measured, or assumed and said to be assumed. The **support of the training distribution**, the set of values training ever drew. And coverage is **joint**: with several randomized parameters it is the probability that all of them fall inside their ranges together (§4).
>
> $$C=P_{\text{real}}\big(\theta\in\operatorname{supp}p_{\text{train}}\big)=\Phi\Big(\frac{\ln(k_{hi}/60)}{0.25}\Big)-\Phi\Big(\frac{\ln(k_{lo}/60)}{0.25}\Big)$$
>
> where $P_{\text{real}}$ is probability under the real distribution and $\operatorname{supp}p_{\text{train}}$ the training support; the second form is S2's one-parameter case, a range $[k_{lo},k_{hi}]$ in kilopascals against the site distribution, because a lognormal $k_c$ falls in the range exactly when the Gaussian $\ln k_c$ falls between $\ln k_{lo}$ and $\ln k_{hi}$.
>
> - **Example**: $[40,\ 80]\,\mathrm{kPa}$ covers $\Phi(1.151)-\Phi(-1.622)=0.875-0.052=0.823$ of S2's sites.
> - **Non-example**: "we randomized $k_c$ by $\pm33\%$ around nominal." A width is not a coverage: the same $[40,\ 80]$ covers $82.3\%$ of these sites but only $49.7\%$ of a population whose median soil is $80\,\mathrm{kPa}$, and a single training value, $[60,\ 60]$, covers none, since a point has probability zero.
> - **Why it matters**: it turns "we randomized widely" into a number that can be checked, and it demands the one input papers seldom report, the distribution of the real parameter.

**A range symmetric in kilopascals is lopsided in probability.** $[40,\ 80]$ sits $20\,\mathrm{kPa}$ either side of the simulator's number, yet it misses $5.2\%$ of sites on the soft side and $12.5\%$ on the hard side, because the distribution is symmetric in $\ln k_c$, not in $k_c$. The range that covers the central $95\%$ is $60\,e^{\pm1.96\times0.25}=[36.8,\ 97.9]\,\mathrm{kPa}$: $23\,\mathrm{kPa}$ below the median and $38$ above.

**What a range buys depends on what the policy senses.** A **blind** policy, one that does not observe the cutting force, must commit to one force before it knows the soil. If it may never cut deeper than planned anywhere in its range (over-excavation is the costly mistake near grade), the largest force it can use is the one that cuts exactly $d_0$ in the softest soil it trained on,

$$F_{\text{blind}}=k_{lo}\,w\,d_0,\qquad d=\frac{F_{\text{blind}}}{k_c\,w}=d_0\,\frac{k_{lo}}{k_c},$$

since any larger force would cut deeper than $d_0$ at $k_{lo}$. Trained on $[40,\ 80]$, it pushes $2.4\,\mathrm{kN}$ and cuts $0.1\times40/60=0.067\,\mathrm{m}$ in the simulator's own $60\,\mathrm{kPa}$ soil: robustness bought as a shallower slice everywhere. Widening its range at the hard end changes nothing, since only $k_{lo}$ enters. An **adaptive** policy observes the force it meets and pushes $\operatorname{clip}(k_c,k_{lo},k_{hi})\,w\,d_0$, the right force inside its range and the nearest trained force outside it, so once it has felt the site's soil it cuts exactly $d_0$ wherever the site is covered (what the first pass costs is §8's question). The clip is this page's model of "outside the training range"; a real network does not saturate cleanly, it does something untested. Egli et al. (2022) met the blind case in a real training run: without joint-torque observations their excavation policy became overly cautious, staying well inside the machine's torque limits because it had no way to tell soft soil from soil that would stall it, while with torques in its observations it adapted online ([[01-canonical-papers/notes/8-construction/egli-rl|note]]).

**The sweep.** §9 samples 200,000 sites. As the range widens from $[50,\ 70]$ to $[30,\ 120]\,\mathrm{kPa}$, coverage rises from $49.8\%$ to $99.4\%$; the adaptive policy's soil per pass stays at $0.99$ to $1.00$ of plan, while the blind policy's falls from $0.847$ to $0.516$. The unrandomized controller shows why tails and not means are the result: averaged over the sites it loses only $2.1\%$ of soil per pass, because soft sites overcut while hard ones undercut, yet $12.4\%$ of sites leave it a quarter or more short and $14.8\%$ push it more than $30\,\mathrm{mm}$ too deep.

**A second parameter multiplies.** Randomize the fill behaviour too, with a range covering $90\%$ of sites independently of $k_c$, and the joint coverage is $0.823\times0.9=0.740$: §4's arithmetic, now on S2.

### 7. Identifying the soil from a few passes

*In one sentence:* a few supervised passes that log force at a known depth give $k_c$ by one-parameter least squares, with an error that falls only as one over the square root of the number of passes, and no number of passes at one depth reveals a term the model lacks or a soil that changes after the passes.

The alternative to covering the soil is to measure it. **The experiment**: the first $n$ passes on the site run under position control at the planned slice, slow and supervised (rung 3 of §3), while the cylinder pressures give the cutting force. The depth is held by the position loop and taken as exact; the force scatters by $\sigma_F=0.3\,\mathrm{kN}$ per pass, soil that varies along the pass included. **The model** is the running object's law with one unknown, $F_i=k_c\,a_i+e_i$ with $a_i=w\,d_i$, linear in its parameter in the sense of [[04-robotics/system-identification|5.5 System Identification §3]]: the regressor $a_i$ is known from the record and $k_c$ enters only through the product. **The criterion** is least squares, which with one parameter solves in one line:

$$\hat k_c=\frac{\sum_i a_iF_i}{\sum_i a_i^2},\qquad \operatorname{sd}(\hat k_c)=\frac{\sigma_F}{\sqrt{\sum_i a_i^2}}=\frac{\sigma_F}{w\,d_0\sqrt n}$$

because setting the derivative of $\sum_i(F_i-k\,a_i)^2$ to zero gives the first expression, and 5.5 §3's covariance $\sigma^2(\Phi^\top\Phi)^{-1}$ with the single column $\Phi=(a_1,\dots,a_n)^\top$ gives the second. The right-hand form is for $n$ passes all at $d_0$, where $\hat k_c$ is simply the mean force divided by $w\,d_0$.

**On the 80-kPa site.** $\sigma_F/(w\,d_0)=0.3/0.06=5\,\mathrm{kPa}$, so one pass pins $k_c$ to a standard deviation of $5\,\mathrm{kPa}$ and four passes to $2.5$, a $95\%$ interval of $\pm1.96\times2.5=\pm4.9\,\mathrm{kPa}$. Setting the force from the estimate, $F=\hat k_c\,w\,d_0$, then cuts $d=d_0\,\hat k_c/k_c$, within $\pm0.1\times4.9/80=\pm0.0061\,\mathrm{m}$ of plan. Halving that needs four times the passes: $\pm2\,\mathrm{kPa}$ takes $(1.96\times5/2)^2=24.0$, so $25$ passes. And if $\sigma_F$ itself is estimated from the same four passes, the $1.96$ becomes Student's $t_{3,0.975}=3.182$ ([[02-foundations/probability|3. Probability §6]]) and the interval widens to $\pm8.0\,\mathrm{kPa}$.

**A term the model lacks is invisible from one depth.** Suppose the real force has an offset the law leaves out, $F=k_c\,w\,d+F_{\text{off}}$, say drag on the bucket's sides that does not scale with the slice, with $F_{\text{off}}=0.6\,\mathrm{kN}$. Every pass at $d_0$ then reads $k_c\,w\,d_0+F_{\text{off}}$, so the one-parameter fit returns $80+0.6/0.06=90\,\mathrm{kPa}$, and it is exactly right at $0.1\,\mathrm{m}$: the model validates perfectly on its own record. Asked for a $0.05\,\mathrm{m}$ finishing slice it commands $90\times0.6\times0.05=2.7\,\mathrm{kN}$, of which $0.6$ goes to the offset, and cuts $2.1/(80\times0.6)=0.044\,\mathrm{m}$, $6.3\,\mathrm{mm}$ short. Adding $F_{\text{off}}$ as a second parameter does not help while every pass is at one depth: the two columns $a_i$ and $1$ are then proportional, the rank is one, and the split between them is arbitrary. The offset is only one such term: the fundamental equation of earthmoving adds a soil-weight term that grows with the square of the depth ([[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §2]]), and passes at one depth hide it in exactly the same way. Two depths are the least excitation two parameters need ([[04-robotics/system-identification|5.5 System Identification §4]]), and a pass at a depth the fit never saw is the validation that catches the missing term ([[04-robotics/system-identification|5.5 System Identification §6]]); the problem set's Do item runs all four combinations. Had the depth been measured rather than held, its noise would sit in the regressor and bias $\hat k_c$ low, the errors-in-variables case of [[04-robotics/system-identification|5.5 System Identification §5]].

**The soil changes after the passes.** The estimate describes the soil the probe passes cut. Egli et al. (2022) open their abstract with the difficulty: soil cannot be predicted well, and it may change in the middle of a single scoop. A trench a metre deep can cross a layer, and the identified controller keeps the old number until someone re-identifies. Tracking a soil that varies is a mapping problem: Wagner et al. (2025) estimate soil properties and their uncertainty from the blade poses and forces of a simulated compact track loader, with a physics-infused neural network built on the fundamental equation of earthmoving, and keep the estimates as layers of a map updated in a Bayesian manner; all of it is in simulation, rung 1 of §3. The alternative that needs no identification step is a policy that adapts by itself, §8.

### 8. Residual and adaptive policies

*In one sentence:* a residual keeps the simulator's controller and learns a bounded correction, and on S2 its bound is a randomization range in disguise that trades grade safety against reach; an adaptive policy needs no such bound, but the signal it reacts to must exist on the machine.

A residual is how §2's "keep a model-based controller and learn a correction" is built. Silver et al. (2018) and Johannink et al. (2018) both add a learned correction to an existing controller's output, the latter describing the final policy as the superposition of the two control signals; the bound in the definition below is this page's addition, the condition §2 says safety depends on.

> **Residual policy, defined.** A **residual policy** is a *controller architecture*: a fixed base controller plus a learned correction added to its output. It is not a policy learned from scratch, and not a base controller whose gains were retuned. Three defining conditions, and a fourth that this page's safety argument needs. A **base controller** $u_0(s)$ that does the task acceptably on its own. A **learned correction** $r_\phi(s)$ **added to its output**, so the command is their sum. **Only the correction is trained**; the base stays fixed. And, for safety, a **bound** $B$ on the correction, so the command never leaves a band around the base's:
>
> $$u(s)=u_0(s)+\operatorname{clip}\big(r_\phi(s),\,-B,\,B\big)$$
>
> where $s$ is what the controller observes, $u_0$ the base command, $r_\phi$ the correction with trained parameters $\phi$, and $B$ the bound, so whatever the network outputs, the command stays within $B$ of a controller whose behaviour is known.
>
> - **Example**: S2 with $u_0=F_b=3.6\,\mathrm{kN}$ and $B=1.2\,\mathrm{kN}$. The command stays in $[2.4,\ 4.8]\,\mathrm{kN}$, which cuts the planned slice on every soil from $2.4/0.06=40$ to $4.8/0.06=80\,\mathrm{kPa}$.
> - **Non-example**: a network that receives $u_0$ as an input and outputs the command itself. It may learn to use $u_0$, but nothing keeps it near $u_0$, so the base controller's known behaviour guarantees nothing about it.
> - **Why it matters**: the bound does two jobs at once. It sets how far a wrong residual can take the machine, and which soils the residual can serve at all, so one number trades safety against coverage.

**The bound is a range.** A residual bounded by $B$ can place the force anywhere in $[F_b-B,\ F_b+B]$, so it cuts the planned slice on every soil from $(F_b-B)/(w\,d_0)$ to $(F_b+B)/(w\,d_0)$. With $B=1.2\,\mathrm{kN}$ that is $[40,\ 80]\,\mathrm{kPa}$, exactly the adaptive controller's range in §6, and on S2 the two cut the same slice at every soil, so §9's table serves both.

**The bound is also the safety margin.** Whatever the network outputs, the force stays within $B$ of the base controller's, so the slice stays within $B/(k_c\,w)$ of the base controller's slice. At the simulator's $60\,\mathrm{kPa}$ a residual that is wrong in full pushes $1.2/(60\times0.6)=0.033\,\mathrm{m}$ deeper than planned, $33\,\mathrm{mm}$, outside the $\pm30\,\mathrm{mm}$ band if this is the last pass. Keeping even a fully wrong residual inside the band there needs $B\le0.03\times60\times0.6=1.08\,\mathrm{kN}$, and that bound reaches only $[42,\ 78]\,\mathrm{kPa}$: $77.6\%$ of sites instead of $82.3\%$. One number trades safety against reach. The clip is a safety filter of the kind [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §4]] writes as a projection onto a safe set, here the interval $[F_b-B,\ F_b+B]$.

**An adaptive policy.** The alternative senses the soil and reacts, and it needs no identification step. Its price is observability: the signal it reacts to must exist on the machine at deployment rate. Egli et al.'s soil-adaptive controller is this design on a 12-tonne excavator: a feedforward network whose 27 observations include four arm joint torques and its own previous velocity command, trained on soils drawn once per episode, with the torques estimated on the machine from cylinder pressures. It reacted to §1's buried granite block within a single scoop. The S2 model of §6 is cruder, estimating from the last pass, so at a layer change it loses exactly one pass: going from $60$ into $75\,\mathrm{kPa}$, its first pass cuts $3.6/(75\times0.6)=0.080\,\mathrm{m}$ and the next the planned $0.1$, while a controller identified once in the top layer cuts $0.080\,\mathrm{m}$ on every pass below.

**Privileged distillation, on S2.** A teacher that sees $k_c$ in simulation and a student that sees only pressures and joint angles is the same bargain one step removed: the student can learn the adaptive policy's behaviour only because one pass's force and depth determine $k_c=F_c/(w\,d)$. How a student learns to infer what its teacher was given is [[04-robotics/legged-locomotion|18. Legged Locomotion §2]].

### Worked case · 대상으로 한 번 끝까지

S2 on the $80\,\mathrm{kPa}$ site, in five steps. Steps 1 and 2 need only the running object; steps 3 to 5 use §6 to §8. §9's lab reproduces the sampled numbers.

**Step 1 — the gap as a number.** The controller pushes $F_b=k_{\text{sim}}\,w\,d_0=60\times0.6\times0.1=3.6\,\mathrm{kN}$. On the site that force cuts

$$d=\frac{F_b}{k_{\text{site}}\,w}=\frac{3.6}{80\times0.6}=0.075\,\mathrm{m},$$

because the running object's law $F_c=k_c\,w\,d$ solved for $d$ gives it. So $\rho=0.075/0.100=0.75$ and $\Delta J=25\,\mathrm{mm}$ per pass. A position controller that held $0.1\,\mathrm{m}$ would instead need $80\times0.6\times0.1=4.8\,\mathrm{kN}$, a third more force than the simulator ever asked of it: the same gap, moved from depth to force.

**Step 2 — what it costs the trench.** The planned pass fills the bucket to $k_f=0.85$, which is $V_b\,k_f/s=0.14\times0.85/1.25=0.0952\,\mathrm{m^3}$ of soil as it lay in the ground, since S2's swell $s$ converts the loose volume in the bucket back to bank volume. Over the same drag a $0.075\,\mathrm{m}$ slice gathers three quarters of that: fill $0.85\times0.75=0.6375$, or $0.0714\,\mathrm{m^3}$ per cycle. With $T_c=16\,\mathrm{s}$ that is $0.0952\times3600/16=21.42\,\mathrm{m^3/h}$ in simulation against $0.0714\times3600/16=16.07\,\mathrm{m^3/h}$ on the site. The trench's $20\times0.6\times1.0=12\,\mathrm{m^3}$ takes $12/21.42\,\mathrm{h}=33.6\,\mathrm{min}$ of cycles in simulation and $12/16.07\,\mathrm{h}=44.8\,\mathrm{min}$ on the site: $11.2$ minutes, a third more, for one wrong number. Both are cycle times only, without the setup and resets [[05-construction-robotics/site-engineering|2.5 §4]] adds to the denominator.

**Step 3 — randomize over $[40,\ 80]\,\mathrm{kPa}$.** The range covers $\Phi(1.151)-\Phi(-1.622)=0.823$ of S2's sites (§6), and $80\,\mathrm{kPa}$ sits on its hard edge. The adaptive controller pushes $80\times0.06=4.8\,\mathrm{kN}$ there and cuts the full $0.100\,\mathrm{m}$. The blind controller made safe on the same range pushes $40\times0.06=2.4\,\mathrm{kN}$ and cuts $2.4/(80\times0.6)=0.050\,\mathrm{m}$, worse than not randomizing at all, and only $0.067\,\mathrm{m}$ even at $60\,\mathrm{kPa}$.

**Step 4 — identify from four passes.** $\hat k_c=80\pm1.96\times5/\sqrt4=80\pm4.9\,\mathrm{kPa}$ at $95\%$ (§7). Setting $F=\hat k_c\,w\,d_0=4.8\pm0.29\,\mathrm{kN}$ cuts $d=d_0\,\hat k_c/80=0.100\pm0.0061\,\mathrm{m}$. The four passes are rung-3 machine time, and the estimate is a snapshot of this stretch of soil.

**Step 5 — bound a residual.** $B=1.2\,\mathrm{kN}$ reaches exactly $80\,\mathrm{kPa}$: $\Delta F=+1.2$ gives $4.8\,\mathrm{kN}$ and the full $0.100\,\mathrm{m}$. But it lets a residual that is wrong in full cut $33\,\mathrm{mm}$ too deep at $60\,\mathrm{kPa}$ (§8). The grade-safe $B=1.08\,\mathrm{kN}$ reaches $78\,\mathrm{kPa}$, so here it pushes $4.68\,\mathrm{kN}$ and cuts $4.68/(80\times0.6)=0.0975\,\mathrm{m}$, $2.5\,\mathrm{mm}$ short, and its reach $[42,\ 78]$ covers $77.6\%$ of sites.

| Controller on the 80 kPa site | Force (kN) | Slice (m) | Soil per pass, of plan | Trench cycles (min) | What it needed |
|---|---:|---:|---:|---:|---|
| fixed, tuned at 60 kPa | 3.60 | 0.0750 | 0.750 | 44.8 | nothing |
| blind, made safe on 40–80 kPa | 2.40 | 0.0500 | 0.500 | 67.2 | nothing at run time |
| adaptive, trained on 40–80 kPa | 4.80 | 0.1000 | 1.000 | 33.6 | the force, observed on the machine |
| identified from four passes | 4.80 ± 0.29 | 0.1000 ± 0.0061 | 1.00 ± 0.06 | 33.6 | four supervised passes |
| residual, B = 1.08 kN | 4.68 | 0.0975 | 0.975 | 34.5 | a bound chosen for grade |

**The reading this gives you.** Every remedy that closed the gap paid for it with something different: the adaptive controller with a sensor that must exist on the machine, the identification with supervised passes whose answer goes stale, the residual with a bound that trades grade safety against reach. The blind controller did not close the gap at all. It exchanged the gap for a guarantee against over-excavation, and on this site the exchange cost half of every slice.

### 9. Lab: the randomization range, swept over sampled sites

Everything is frozen in the running object. The listing samples 200,000 sites from the site distribution and, for seven training ranges, prints the coverage (exact, then sampled), and for the blind and the adaptive controller the soil per pass as a fraction of plan (capped by the heaped bucket at $1/k_f$), the share of sites cut a quarter or more short, and the share cut more than $30\,\mathrm{mm}$ too deep. The second loop runs $n$ probe passes on the $80\,\mathrm{kPa}$ site, 20,000 times over, and compares the spread of $\hat k_c$ with §7's formula. NumPy and the standard library only; it runs in a second or two.

```python
import numpy as np
from math import erf, log, sqrt

w, d0, k_sim = 0.6, 0.1, 60.0          # S2's bucket width (m), the planned slice (m), the simulator's soil (kPa)
kf = 0.85                              # S2's fill factor, reached when the pass cuts d0
mu, sig = log(k_sim), 0.25             # the site distribution: ln k_c ~ N(ln 60, 0.25^2)
rng = np.random.default_rng(0)
k = rng.lognormal(mu, sig, 200_000)    # one soil per site (kPa)

def Phi(z):                            # standard normal CDF
    return 0.5 * (1 + erf(z / sqrt(2)))

def coverage(lo, hi):                  # exact share of sites with lo <= k_c <= hi
    return Phi((log(hi) - mu) / sig) - Phi((log(lo) - mu) / sig)

def depth(k, lo, hi, adaptive):        # slice cut by a controller trained on [lo, hi] kPa
    F = (np.clip(k, lo, hi) if adaptive else lo) * w * d0    # the force it pushes (kN)
    return F / (k * w)                                       # d = F / (k_c w), in m

for lo, hi in ((60, 60), (50, 70), (42, 78), (40, 80), (40, 90), (35, 100), (30, 120)):
    row = f"{lo:>3}-{hi:<3} cover {coverage(lo, hi):.3f} ({np.mean((k >= lo) & (k <= hi)):.3f})"
    for name, adaptive in (("blind", False), ("adaptive", True)):
        d = depth(k, lo, hi, adaptive)
        per_pass = np.minimum(d / d0, 1 / kf).mean()     # soil per pass / plan; a heaped bucket caps it
        row += f" | {name} {per_pass:.3f} short {np.mean(d <= 0.75 * d0):.3f} deep {np.mean(d > d0 + 0.03):.3f}"
    print(row)

sF, k_site = 0.3, 80.0                 # scatter of one pass's measured force (kN); the worked case's site (kPa)
for n in (1, 4, 16, 25):
    F = k_site * w * d0 + sF * rng.standard_normal((20_000, n))   # n probe passes at d0, 20,000 times over
    k_hat = F.mean(axis=1) / (w * d0)                             # least squares with one regressor
    d_next = k_hat * w * d0 / (k_site * w)                        # the slice once the force is set from k_hat
    print(f"n={n:<2} sd(k_hat) {k_hat.std():.2f} kPa, formula {sF / (w * d0 * sqrt(n)):.2f};"
          f" 95% of slices within {1000 * np.percentile(np.abs(d_next - d0), 95):.1f} mm of plan")
```

The range sweep. "Coverage" is §6's formula, with the sampled share in brackets; "per pass" is soil per pass as a fraction of plan; "short" is the share of sites cut a quarter or more short, "deep" the share cut more than $30\,\mathrm{mm}$ too deep.

| range (kPa) | coverage | blind: per pass | short | deep | adaptive: per pass | short | deep |
|---|---:|---:|---:|---:|---:|---:|---:|
| 60–60 | 0.000 (0.000) | 0.979 | 0.124 | 0.148 | 0.979 | 0.124 | 0.148 |
| 50–70 | 0.498 (0.498) | 0.847 | 0.337 | 0.038 | 0.990 | 0.039 | 0.038 |
| 42–78 | 0.776 (0.776) | 0.720 | 0.609 | 0.007 | 0.990 | 0.014 | 0.007 |
| 40–80 | 0.823 (0.823) | 0.687 | 0.681 | 0.004 | 0.991 | 0.011 | 0.004 |
| 40–90 | 0.895 (0.895) | 0.687 | 0.681 | 0.004 | 1.000 | 0.003 | 0.004 |
| 35–100 | 0.964 (0.964) | 0.602 | 0.842 | 0.001 | 1.000 | 0.001 | 0.001 |
| 30–120 | 0.994 (0.994) | 0.516 | 0.948 | 0.000 | 1.000 | 0.000 | 0.000 |

The probe passes on the $80\,\mathrm{kPa}$ site:

| passes $n$ | sd of $\hat k_c$, sampled (kPa) | §7's formula (kPa) | 95% of slices within |
|---:|---:|---:|---:|
| 1 | 5.01 | 5.00 | 12.2 mm |
| 4 | 2.49 | 2.50 | 6.1 mm |
| 16 | 1.24 | 1.25 | 3.1 mm |
| 25 | 1.01 | 1.00 | 2.5 mm |

Five readings, each tagged with the claim it tests.

**The coverage formula holds** (tests §6's definition). The exact and sampled coverages agree to the third digit in every row, and the unrandomized row covers nothing: a single training value is not a range.

**The blind policy pays only for the soft end** (tests §6's derivation). Its rows for $[40,\ 80]$ and $[40,\ 90]$ are identical, since only $k_{lo}$ enters its force, and its soil per pass falls with $k_{lo}$, from $0.847$ to $0.516$. At $[40,\ 80]$ it is a quarter or more short on $68.1\%$ of sites in exchange for overcutting on $0.4\%$.

**The adaptive policy holds the plan wherever it is covered** (tests §6 and §8). Its soil per pass is $0.990$ to $1.000$; what it misses is the uncovered tail, $1.1\%$ short at $[40,\ 80]$. The $[42,\ 78]$ row is also the grade-safe residual of §8, which cuts the same slice at every soil: $77.6\%$ coverage and $1.4\%$ short.

**The mean hides the tails** (tests §1's asymmetry). The unrandomized controller's $0.979$ looks like a $2\%$ loss, but it averages $12.4\%$ of sites cut a quarter short with $14.8\%$ cut more than $30\,\mathrm{mm}$ too deep.

**Identification improves as one over the square root of the passes** (tests §7). The sampled spread matches $\sigma_F/(w\,d_0\sqrt n)$ in every row, four passes put $95\%$ of the following slices within $6.1\,\mathrm{mm}$, and halving the error costs four times the passes.

### After reading

- Separate dynamics, contact, sensing, task, and implementation gaps.
- Explain system identification, domain randomization, privileged learning, residuals,
  and real-data adaptation without treating them as interchangeable.
- Identify simulator-only information and the real-data budget in a paper.
- State what evidence would support generalization beyond one machine and one soil bin.
- Turn a sim-to-real gap into a number for one policy, and say which requirement its sign breaks.
- Compute the coverage of a randomization range from a stated real distribution, and say why a blind policy pays for the width while an adaptive one does not.
- Size an identification from a few passes, and name what it cannot see: a missing term at one depth, and a soil that changes afterwards.
- Bound a residual and state what the bound trades.

### Self-check

1. A team scales training from 100 to 10,000 parallel environments and reports better
   sim performance. Why might the real-machine result not improve at all?
2. Egli RL transferred zero-shot to the real M545. What did "zero-shot" cost upstream,
   and what does the term not mean?
3. A teacher policy uses ground-truth soil parameters; the student uses joint and
   pressure signals. What is the single most important check before believing the
   deployment claim?
4. ExACT and ExT both apply imitation learning to excavation. Why do their claims sit on
   different rungs of the deployment ladder?
5. Averaged over S2's sites, the unrandomized controller loses only $2.1\%$ of soil per pass. Why is that not evidence that it transfers?
6. A trench crosses from $60$ into $75\,\mathrm{kPa}$ soil halfway down. What does a controller identified once in the top layer cut below the boundary, and what does an adaptive controller trained on $[40,\ 80]\,\mathrm{kPa}$ lose?

> [!tip]- Answers
> 1. Parallelism raises sample throughput, not simulator validity: 10,000 environments can repeat the same wrong hydraulics, contact, and sensing physics. If the dominant gap is a modeling error rather than sample scarcity, more samples converge harder onto the wrong optimum.
> 2. Upstream it cost real-machine data and engineering to fit the neural-network valve/actuator model — real-system knowledge baked into the simulator. "Zero-shot" means no target-domain training update before deployment; it does not mean the simulator was built without real data, nor that transfer holds beyond the identified machine and operating range.
> 3. Whether every observation the student consumes actually exists, at deployment rate and latency, on the real machine — and whether the distillation was evaluated with realistic noise on those signals. Privileged learning fails silently when test-time observability is quietly optimistic.
> 4. ExACT is validated in simulation only, so its evidence stops at rung 1 (simulator-only evaluation); ExT reports centimeter-level transfer on a real machine, reaching the supervised real-trial rungs. Same method family, different evidentiary weight — the ladder, not the method name, sets the claim.
> 5. The average mixes two failures of opposite sign: soft sites overcut, up to the bucket's cap, and hard sites undercut, so they partly cancel in the mean. Site by site, $12.4\%$ are cut a quarter or more short and $14.8\%$ more than $30\,\mathrm{mm}$ too deep, a grade failure on the last pass (§6, §9). A transfer claim is about sites, so report the tails, not the mean.
> 6. The identified controller keeps $\hat k_c=60$ and its $3.6\,\mathrm{kN}$, so below the boundary it cuts $3.6/(75\times0.6)=0.080\,\mathrm{m}$ on every pass, a fifth short, until someone re-identifies. The adaptive controller's range covers $75\,\mathrm{kPa}$, so in the page's model it loses one pass, the first below the boundary, at $0.080\,\mathrm{m}$, and then cuts the planned $0.1\,\mathrm{m}$; a controller that reacts within the pass, as Egli et al.'s does, loses less (§8).

### Problem set · 과제

Tier A. S2 on and around the $80\,\mathrm{kPa}$ site, with [[04-robotics/system-identification|5.5 System Identification]] and [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning]] behind it. The lab samples sites and passes; there is no simulator.

1. **Draw.** The picture above for the grade-safe residual of §8, $B=1.08\,\mathrm{kN}$: its reach as the shaded band, its slice curve, the fixed-force curve, the planned-slice and $30\,\mathrm{mm}$ lines, and the site strip with the new coverage and both tails. Mark the $80\,\mathrm{kPa}$ site's slice under the residual.
2. **Derive.** A softer site, $k_c=45\,\mathrm{kPa}$, everything else as in the running object. (a) The fixed-force controller's slice and overcut: does it break the $\pm30\,\mathrm{mm}$ grade on the last pass, and does the heaped bucket hold a mid-trench pass? (b) The blind controller made safe on $[40,\ 80]$: its slice. (c) An adaptive controller trained on the narrower $[50,\ 70]$: its force and slice. (d) The probe passes needed to know $k_c$ within $\pm4.5\,\mathrm{kPa}$ at $95\%$. (e) The smallest residual bound that reaches $45\,\mathrm{kPa}$, and whether it is grade-safe at $60\,\mathrm{kPa}$. (f) Six independent randomized parameters: what coverage per parameter gives $90\%$ joint coverage, and what joint coverage do ten parameters at $90\%$ each give?
3. **Do.** The soil carries the offset of §7, $F_{\text{off}}=0.6\,\mathrm{kN}$, that the one-parameter model lacks. Fill the `?` so that the script fits both models to eight probe passes, all at $0.1\,\mathrm{m}$ or alternating $0.05$ and $0.1\,\mathrm{m}$, and scores each fit on a held-out $0.05\,\mathrm{m}$ slice, 2,000 times over. Report, for each design, the rank, both estimates of $k_c$ with their spread, and the held-out error. Which fit validates on its own record and still fails the held-out slice? Which design and model recover $k_c$, and what did the second parameter cost?

```python
import numpy as np
w, k_site, F_off, sF = 0.6, 80.0, 0.6, 0.3     # bucket width (m), the site (kPa), the hidden offset (kN), force scatter (kN)
rng = np.random.default_rng(1)
designs = {"one depth": np.full(8, 0.10), "two depths": np.tile([0.05, 0.10], 4)}   # eight probe passes each
for name, d in designs.items():
    a = w * d                                   # the regressor: each slice's cross-section (m^2)
    A = np.column_stack((a, np.ones_like(a)))   # the two-parameter model's columns
    fits = []
    for _ in range(2000):                       # the same eight passes, 2000 times over
        F = k_site * a + F_off + sF * rng.standard_normal(a.size)       # what the cylinder pressures report (kN)
        k1 = ?                                                          # one parameter: F = k a
        k2, off2 = ?                                                    # two parameters: F = k a + F_off
        for kh, oh in ((k1, 0.0), (k2, off2)):
            F_cmd = ?                                                   # the force the fit says cuts 0.05 m
            fits.append((kh, 1000 * ((F_cmd - F_off) / (k_site * w) - 0.05)))   # held-out slice error (mm)
    f = np.array(fits).reshape(-1, 2, 2)
    print(f"{name}: rank {np.linalg.matrix_rank(A)}")
    for i, label in enumerate(("1-param", "2-param")):
        print(f"  {label}: k {f[:, i, 0].mean():6.1f} ± {f[:, i, 0].std():4.1f} kPa,"
              f" held-out 0.05 m slice off by {f[:, i, 1].mean():+6.1f} ± {f[:, i, 1].std():.1f} mm")
```

4. **Interpret.** A paper randomizes twelve parameters "over wide ranges" and reports zero-shot transfer. What does it have to show about the real parameters before its ranges can be called wide? If each range covered $95\%$ of its real marginal and the twelve were independent, what joint coverage would that be, and what does "zero-shot" leave unsaid?

> [!note]- How to draw it · 그리는 법
> - **The band** from $42$ to $78\,\mathrm{kPa}$, labelled as the residual's reach, $F=3.6\pm1.08\,\mathrm{kN}$: narrower than the picture's $40$–$80$ by $2\,\mathrm{kPa}$ at each end.
> - **The residual's slice curve**: flat at $0.100\,\mathrm{m}$ across the band; outside it the force is clipped to $2.52$ or $4.68\,\mathrm{kN}$, so the slice is $0.1\times42/k_c$ on the soft side ($0.140\,\mathrm{m}$ at $30\,\mathrm{kPa}$) and $0.1\times78/k_c$ on the hard side ($0.0975$ at $80$, $0.078$ at $100$, $0.065\,\mathrm{m}$ at $120\,\mathrm{kPa}$).
> - **The fixed-force curve unchanged**, $d=3.6/(0.6\,k_c)$, through $0.100$ at $60$ and $0.075$ at $80\,\mathrm{kPa}$, and the two horizontal lines at $0.10$ and $0.13\,\mathrm{m}$.
> - **The mark at $80\,\mathrm{kPa}$**: $0.0975\,\mathrm{m}$, labelled $2.5\,\mathrm{mm}$ short, just below the plan line.
> - **The strip**: the same lognormal, shaded from $42$ to $78$, with $77.6\%$ inside, $7.7\%$ softer and $14.7\%$ harder.
> - The drawing is wrong if the band is centred in probability: the hard tail is still about twice the soft one, because the distribution is symmetric in $\ln k_c$, not in $k_c$.

> [!tip]- Solutions
> 1. As in the How-to-draw list: band $[42,\ 78]\,\mathrm{kPa}$; residual slice $0.100\,\mathrm{m}$ inside, $0.1\times42/k_c$ and $0.1\times78/k_c$ outside; at $80\,\mathrm{kPa}$, $0.0975\,\mathrm{m}$; strip $77.6\%$ inside, $7.7\%$ softer, $14.7\%$ harder.
> 2. (a) $d=3.6/(45\times0.6)=0.133\,\mathrm{m}$, $33\,\mathrm{mm}$ too deep, outside the $\pm30\,\mathrm{mm}$ band on the last pass. Mid-trench the fill would be $0.85\times0.133/0.1=1.13$ of the heaped capacity, so the bucket overflows: it carries at most $1/0.85=1.18$ planned passes' worth of soil, and the remaining $0.16$ of a planned pass spills. (b) $2.4/(45\times0.6)=0.089\,\mathrm{m}$, $11\,\mathrm{mm}$ short. (c) $45<50$, so it pushes $50\times0.06=3.0\,\mathrm{kN}$ and cuts $3.0/(45\times0.6)=0.111\,\mathrm{m}$, $11\,\mathrm{mm}$ too deep, inside the band. (d) The standard deviation per pass is $5\,\mathrm{kPa}$ whatever the soil, so $n\ge(1.96\times5/4.5)^2=4.74$: five passes. (e) The residual must supply $45\times0.06-3.6=-0.9\,\mathrm{kN}$, so $B\ge0.9\,\mathrm{kN}$; wrong in full at $60\,\mathrm{kPa}$ it cuts $0.1\times0.9/3.6=25\,\mathrm{mm}$ too deep, inside the band, so it is grade-safe. (f) $p^6=0.9$ gives $p=0.9^{1/6}=0.983$: every range must cover $98.3\%$ of its real marginal. And $0.9^{10}=0.349$: adding parameters erodes joint coverage even at generous marginals.
> 3. The blanks are `(a @ F) / (a @ a)`, `np.linalg.lstsq(A, F, rcond=None)[0]` and `kh * w * 0.05 + oh`. The filled script:
>
> ```python
> import numpy as np
> w, k_site, F_off, sF = 0.6, 80.0, 0.6, 0.3     # bucket width (m), the site (kPa), the hidden offset (kN), force scatter (kN)
> rng = np.random.default_rng(1)
> designs = {"one depth": np.full(8, 0.10), "two depths": np.tile([0.05, 0.10], 4)}   # eight probe passes each
> for name, d in designs.items():
>     a = w * d                                   # the regressor: each slice's cross-section (m^2)
>     A = np.column_stack((a, np.ones_like(a)))   # the two-parameter model's columns
>     fits = []
>     for _ in range(2000):                       # the same eight passes, 2000 times over
>         F = k_site * a + F_off + sF * rng.standard_normal(a.size)       # what the cylinder pressures report (kN)
>         k1 = (a @ F) / (a @ a)                                          # one parameter: F = k a
>         k2, off2 = np.linalg.lstsq(A, F, rcond=None)[0]                 # two parameters: F = k a + F_off
>         for kh, oh in ((k1, 0.0), (k2, off2)):
>             F_cmd = kh * w * 0.05 + oh                                  # the force the fit says cuts 0.05 m
>             fits.append((kh, 1000 * ((F_cmd - F_off) / (k_site * w) - 0.05)))   # held-out slice error (mm)
>     f = np.array(fits).reshape(-1, 2, 2)
>     print(f"{name}: rank {np.linalg.matrix_rank(A)}")
>     for i, label in enumerate(("1-param", "2-param")):
>         print(f"  {label}: k {f[:, i, 0].mean():6.1f} ± {f[:, i, 0].std():4.1f} kPa,"
>               f" held-out 0.05 m slice off by {f[:, i, 1].mean():+6.1f} ± {f[:, i, 1].std():.1f} mm")
> ```
>
> It prints, for one depth, rank $1$, the one-parameter fit at $89.9\pm1.8\,\mathrm{kPa}$ missing the held-out slice by $-6.3\pm1.1\,\mathrm{mm}$, and the two-parameter fit at $0.3\,\mathrm{kPa}$ with the held-out slice off by $+49.7\pm2.2\,\mathrm{mm}$; for two depths, rank $2$, the one-parameter fit at $92.0\pm2.2\,\mathrm{kPa}$, off by $-5.0\pm1.4\,\mathrm{mm}$, and the two-parameter fit at $80.0\pm6.9\,\mathrm{kPa}$, off by $-0.0\pm3.0\,\mathrm{mm}$. The one-parameter fit at one depth is the one that validates on its own record: it returns $k_c+F_{\text{off}}/(w\,d_0)=80+10=90\,\mathrm{kPa}$, which is exactly right at $0.1\,\mathrm{m}$, and it still misses a $0.05\,\mathrm{m}$ slice by $6.25\,\mathrm{mm}$ on average. The two-parameter fit at one depth is rank-deficient, and `lstsq` returns the minimum-norm split, which puts almost all the force into the offset and overcuts the held-out slice by about $50\,\mathrm{mm}$ without a warning; that is why the rank is printed. A second depth does not rescue the wrong model: the one-parameter fit then reads $80+0.6\times\sum a_i/\sum a_i^2=92\,\mathrm{kPa}$. Only two depths with two parameters recover $k_c$ without bias, and the price is precision: the slope's spread is $\sigma_F/\sqrt{\sum(a_i-\bar a)^2}=0.3/\sqrt{8\times0.015^2}=7.1\,\mathrm{kPa}$ ($6.9$ sampled), against $1.8$ for the biased one-depth fit. The held-out error is unbiased, with a spread of $3.1\,\mathrm{mm}$ by the formula and $3.0$ sampled.
> 4. Measurements, or credible estimates, of the real parameters' distributions and of their correlations, since coverage is a property of the joint distribution; "wide" relative to what was measured is a claim, and "wide" alone is not. At $95\%$ each and independent, the joint coverage is $0.95^{12}=0.540$, so nearly half of real conditions would fall outside the box. "Zero-shot" says only that the trained parameters were frozen (§3); it leaves unsaid how much real data built the simulator and what the policy adapts online.

### Sources

- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — which simulator actually models terrain and contact, and what each one leaves out.
- [Tobin et al., *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World*](https://arxiv.org/abs/1703.06907)
- [Peng et al., *Sim-to-Real Transfer of Robotic Control with Dynamics Randomization*](https://arxiv.org/abs/1710.06537)
- [Lee et al., *Learning Quadrupedal Locomotion over Challenging Terrain*](https://www.science.org/doi/10.1126/scirobotics.abc5986) — privileged learning example
- P. Egli, D. Gaschen, S. Kerscher, D. Jud, M. Hutter, "Soil-Adaptive Excavation Using Reinforcement Learning," *IEEE Robotics and Automation Letters* 7(4), 2022, [DOI 10.1109/LRA.2022.3189834](https://doi.org/10.1109/LRA.2022.3189834); accepted version open at the [ETH Research Collection](https://www.research-collection.ethz.ch/server/api/core/bitstreams/95ef5691-11e8-4a86-b02d-6f0e2501de9b/content) — the randomized soil parameters of Table I, the torque observations and the ablation without them, the buried granite block, and the bucket-fill caveat of §4.
- T. Silver, K. Allen, J. Tenenbaum, L. Kaelbling, "Residual Policy Learning," [arXiv:1812.06298](https://arxiv.org/abs/1812.06298), 2018 — a learned residual on top of an initial controller.
- T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, S. Levine, "Residual Reinforcement Learning for Robot Control," [arXiv:1812.03201](https://arxiv.org/abs/1812.03201), 2018 — the final policy as a superposition of a conventional controller's signal and an RL residual.
- W. J. Wagner, A. Soylemezoglu, K. Driggs-Campbell, "In-Situ Soil-Property Estimation and Bayesian Mapping with a Simulated Compact Track Loader," [arXiv:2507.22356](https://arxiv.org/abs/2507.22356), 2025 — soil properties estimated from blade poses and forces and mapped in a Bayesian manner, in simulation (Vortex Studio).
- L. Werner, P. Eyschen, S. Costello, P. Micarelli, A. Cramariuc, M. Hutter, "Size Doesn't Matter: Material-State Reinforcement Learning for Excavator Transferable Soil Manipulation," [arXiv:2609.12677](https://arxiv.org/abs/2609.12677), 2026 — the same learned weights on an 11.5-tonne excavator and a 500-gram tabletop robot through a calibrated machine interface.
- Every course number on this page was computed here from S2's frozen values and this page's own with NumPy 2.0.2; the sites and passes are sampled, not measured.

## 한국어

시뮬레이션은 위험하고 느리며 비싼 로봇 경험을 싸게 만든다. 그 경험을 현실로 만들어 주지는
않는다. **Sim-to-real**은 시뮬레이터의 가정이 깨져도 정책이 쓸모 있도록 만드는 모델링·학습·
적응·평가 방법의 묶음이다.

> [!info] 깊이 목표
> Sim-to-real 논문을 읽고 다음을 짚는다: 어느 격차(동역학·접촉·센싱·과제·구현)가
> 지배적인지, 어떤 전략이 어떤 비용으로 이를 다루는지, 전이가 소비한 실데이터·개입
> 예산은 얼마인지, 증거가 배치 사다리의 어느 단에 실제로 도달하는지. 전이 파이프라인
> 설계는 실무/숙달 단계의 주제다.

> [!note] 선수 지식
> [[05-construction-robotics/site-engineering|2.5 현장 로보틱스를 공학 시스템으로]](S2, 이 페이지의 대상) · [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 자율화]](기계, 그리고 그 흙을 왜 모르는가) · [[02-foundations/probability|3. 확률 §2–§3]](CDF, 가우시안, 평균의 퍼짐) · [[02-foundations/rl-basics|7. RL 기초]](정책과 return) · [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §4–§5]](실기계 위의 RL, 안전 필터, "zero-shot") · [[04-robotics/system-identification|5.5 시스템 식별 §1, §3–§6]](최소제곱, 여기, 회귀 벡터의 잡음, 떼어 둔 데이터 검증) · [[04-robotics/contact-force-tactile|9. 접촉 §3]](§1의 경고 뒤에 있는 접촉 모델) · [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3, §9]](거리로 읽는 지연, 단계적 배치)

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고 그림을 본다. S2의 트렌치이고, 실제 흙이 더 단단할 때 시뮬레이터의 숫자 하나 — 흙의 절삭 저항 — 가 제어기에 무슨 일을 하는지 보여 준다. 그다음 §1에서 격차를 숫자로 만들고, §2에서 전략을 보고, §6–§8에서 그중 셋을 S2 위에서 값으로 매긴다. §8 뒤의 계산 절이 그 모두를 한 현장에 올린다. §3–§5는 논문을 사다리에 올려놓을 때 쓰는 부분이고(매개변수 여섯을 각각 80%씩 덮어도 실제 조건의 26%만 덮인다는 §4의 예제도 여기 있다), §9는 랩이다.

### 이 페이지의 대상 · Running object

[[05-construction-robotics/site-engineering|2.5 현장 로보틱스를 공학 시스템으로]]의 **S2**다. $5$톤급 굴착기가 길이 $20\,\mathrm{m}$, 폭 $0.6\,\mathrm{m}$, 깊이 $1.0\,\mathrm{m}$의 매설관 트렌치를 바닥 고저 $\pm30\,\mathrm{mm}$로 판다. S2는 흙의 비절삭 저항을 $k_c=60\,\mathrm{kPa}$로 고정해 두었다. 깎는 단면의 단위 면적당 절삭력이다. 폭 $w$인 버킷이 두께 $d$의 층을 깎으면 단면이 $w\,d$이므로 절삭력은

$$F_c=k_c\,w\,d,$$

이고, $k_c$를 킬로파스칼로, $w\,d$를 제곱미터로 쓰면 킬로뉴턴이 나온다. 2.5의 정의가 허락하는 가장 단순한 절삭 모델이고, 성립 조건까지 갖춘 온전한 정의는 [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공 §2]]에 있다. 이 페이지는 S2의 $60\,\mathrm{kPa}$를 **시뮬레이터의 흙** $k_{\text{sim}}$으로 읽고, 실제 버킷 아래의 땅이 다를 때 무슨 일이 일어나는지 묻는다. 2.5는 실제 현장의 흙은 재야 한다고 말한다. 그것을 재는 페이지가 여기다.

옮겨 가는 제어기는 시뮬레이션에서 맞춘 힘 기반 굴착 제어기이고, 교과용 모델이다. 매 패스마다, 시뮬레이터의 흙에서 계획한 두께를 깎는 절삭력으로 버킷을 민다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $k_{\text{sim}}$ | $60\,\mathrm{kPa}$ | S2의 $k_c$. 여기서는 시뮬레이터의 흙으로 읽는다 |
| $w$ | $0.6\,\mathrm{m}$ | S2의 버킷 폭, 트렌치 폭과 같다 |
| $d_0$ | $0.1\,\mathrm{m}$ | 제어기가 패스마다 깎도록 맞춰진 두께 |
| $F_b$ | $3.6\,\mathrm{kN}$ | 제어기가 미는 힘, $k_{\text{sim}}\,w\,d_0=60\times0.6\times0.1$ |
| $k_{\text{site}}$ | $80\,\mathrm{kPa}$ | 계산 절의 실제 현장 |
| 현장 분포 | $\ln k_c\sim\mathcal N(\ln60,\ 0.25^2)$ | S2를 팔 수 있는 현장들에 $k_c$가 퍼진 모양: 중앙값 $60\,\mathrm{kPa}$인 로그정규(§6) |
| $[k_{lo},\ k_{hi}]$ | $[40,\ 80]\,\mathrm{kPa}$ | 계산 절의 랜덤화 범위 |
| $\sigma_F$ | $0.3\,\mathrm{kN}$ | 한 패스에서 잰 절삭력의 흩어짐 |

$d_0$, $k_{\text{site}}$, 현장 분포, 범위, $\sigma_F$는 이 페이지가 고정한 숫자이고, 이것들도 교과용 숫자다. 현장 분포는 가르치기 위한 가정이지 실제 흙을 조사한 결과가 아니다. 나머지는 모두 S2의 것이다. 계산 절이 생산성으로 바꾸는 $V_b$, $k_f$, $s$, $T_c$와, §3이 거리로 바꾸는 $\tau_h$, $v$도 그렇다.

*범위: 이 페이지는 잰 숫자로서의 reality gap, 도메인 랜덤화와 그 범위의 포함률, 몇 번의 패스로 흙 파라미터 하나를 식별하는 법, 잔차 정책과 적응형 정책, 그리고 전이 증거에 등급을 매기는 사다리를 모두 S2의 흙 위에서 가르친다. 식별 일반([[04-robotics/system-identification|5.5 시스템 식별]]), RL 파인튜닝과 안전 필터([[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §4]]), privileged 교사–학생 증류([[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]]), 어떤 시뮬레이터가 흙을 얼마나 잘 모델링하는지([[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋 §4]])는 가르치지 않는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 346" style="max-width:100%;height:auto" role="img" aria-label="흙의 비절삭 저항에 대한 패스당 절삭 두께. 시뮬레이터에 맞춘 제어기는 3.6 kN을 밀어 60 kPa에서 0.100 m를 깎지만 80 kPa에서는 0.075 m를 깎는다. 40–80 kPa에서 적응하도록 학습한 제어기는 그 범위 전체에서 0.100 m를 지키고, 같은 범위에서 안전하게 만든 블라인드 제어기는 60 kPa에서 0.067 m, 80 kPa에서 0.050 m를 깎는다. 아래는 이 페이지의 현장 분포로, 현장의 82.3퍼센트가 40–80 kPa 안에 있고 5.2퍼센트는 더 무르며 12.5퍼센트는 더 단단하다.">
<text x="16" y="18" font-size="12" fill="currentColor" font-weight="600">한 번의 패스가 깎는 두께와 흙의 절삭 저항</text>
<rect x="158.4" y="66.0" width="188.8" height="160.0" fill="currentColor" fill-opacity="0.07"/>
<text x="252.8" y="78.0" font-size="10.5" fill="currentColor" text-anchor="middle">학습 범위 40–80 kPa</text>
<line x1="64.0" y1="226.0" x2="536.0" y2="226.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="64.0" y1="66.0" x2="64.0" y2="226.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="60.0" y1="226.0" x2="64.0" y2="226.0" stroke="currentColor"/><text x="57.0" y="229.5" font-size="10" fill="currentColor" text-anchor="end">0.00</text>
<line x1="60.0" y1="181.6" x2="64.0" y2="181.6" stroke="currentColor"/><text x="57.0" y="185.1" font-size="10" fill="currentColor" text-anchor="end">0.05</text>
<line x1="60.0" y1="137.1" x2="64.0" y2="137.1" stroke="currentColor"/><text x="57.0" y="140.6" font-size="10" fill="currentColor" text-anchor="end">0.10</text>
<line x1="60.0" y1="92.7" x2="64.0" y2="92.7" stroke="currentColor"/><text x="57.0" y="96.2" font-size="10" fill="currentColor" text-anchor="end">0.15</text>
<text x="57.0" y="60.0" font-size="10" fill="currentColor" text-anchor="end">두께 (m)</text>
<line x1="64.0" y1="137.1" x2="536.0" y2="137.1" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="3 3"/>
<text x="534.0" y="150.1" font-size="10" fill="currentColor" text-anchor="end">계획 두께 d₀ = 0.10 m</text>
<line x1="64.0" y1="110.4" x2="536.0" y2="110.4" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="1 3"/>
<text x="534.0" y="106.4" font-size="10" fill="currentColor" text-anchor="end">30 mm 과굴착: 마지막 패스라면 고저 이탈</text>
<polyline points="126.9,66.0 137.2,75.8 147.4,84.4 157.6,92.1 167.8,99.0 178.1,105.2 188.3,110.9 198.5,116.0 208.7,120.7 219.0,125.1 229.2,129.0 239.4,132.7 249.7,136.1 259.9,139.3 270.1,142.2 280.3,145.0 290.6,147.6 300.8,150.0 311.0,152.3 321.2,154.4 331.5,156.4 341.7,158.3 351.9,160.2 362.1,161.9 372.4,163.5 382.6,165.0 392.8,166.5 403.1,167.9 413.3,169.3 423.5,170.5 433.7,171.8 444.0,172.9 454.2,174.1 464.4,175.1 474.6,176.2 484.9,177.1 495.1,178.1 505.3,179.0 515.5,179.9 525.8,180.7 536.0,181.6" fill="none" stroke="currentColor" stroke-width="2"/>
<polyline points="74.5,66.0 79.7,73.6 85.0,80.5 90.2,86.9 95.5,92.7 100.7,98.0 106.0,102.9 111.2,107.5 116.4,111.7 121.7,115.7 126.9,119.3 132.2,122.8 137.4,126.0 142.7,129.0 147.9,131.9 153.2,134.6 158.4,137.1 347.2,137.1 359.0,139.8 370.8,142.3 382.6,144.7 394.4,147.0 406.2,149.1 418.0,151.1 429.8,153.1 441.6,154.9 453.4,156.6 465.2,158.3 477.0,159.9 488.8,161.4 500.6,162.8 512.4,164.2 524.2,165.5 536.0,166.7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-dasharray="8 4" stroke-opacity="0.8"/>
<polyline points="74.5,66.0 86.0,81.9 97.6,94.9 109.1,105.7 120.6,114.9 132.2,122.8 143.7,129.6 155.3,135.6 166.8,140.9 178.3,145.6 189.9,149.8 201.4,153.6 212.9,157.0 224.5,160.2 236.0,163.0 247.6,165.6 259.1,168.0 270.6,170.3 282.2,172.3 293.7,174.2 305.2,176.0 316.8,177.7 328.3,179.2 339.9,180.7 351.4,182.0 362.9,183.3 374.5,184.5 386.0,185.7 397.5,186.8 409.1,187.8 420.6,188.8 432.2,189.7 443.7,190.6 455.2,191.4 466.8,192.2 478.3,193.0 489.8,193.7 501.4,194.4 512.9,195.1 524.5,195.8 536.0,196.4" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="2 3"/>
<line x1="16" y1="32.5" x2="40" y2="32.5" stroke="currentColor" stroke-width="2"/><text x="46" y="36" font-size="10" fill="currentColor">고정 3.6 kN, 60 kPa에 맞춤</text>
<line x1="288" y1="32.5" x2="312" y2="32.5" stroke="currentColor" stroke-width="2.4" stroke-dasharray="8 4"/><text x="318" y="36" font-size="10" fill="currentColor">적응형, 40–80 kPa에서 학습</text>
<line x1="16" y1="46.5" x2="40" y2="46.5" stroke="currentColor" stroke-width="2" stroke-dasharray="2 3"/><text x="46" y="50" font-size="10" fill="currentColor">블라인드, 40–80 kPa에서 안전하게</text>
<circle cx="252.8" cy="137.1" r="3.8" fill="currentColor"/>
<text x="257.8" y="128.1" font-size="10" fill="currentColor">시뮬레이터의 흙 60 kPa: 0.100</text>
<circle cx="347.2" cy="159.3" r="3.8" fill="currentColor"/>
<text x="354.2" y="163.3" font-size="10" fill="currentColor">0.075</text>
<circle cx="347.2" cy="181.6" r="3" fill="currentColor"/>
<text x="354.2" y="194.6" font-size="10" fill="currentColor">0.050</text>
<circle cx="347.2" cy="137.1" r="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
<text x="64.0" y="246.0" font-size="10" fill="currentColor">S2 현장들의 흙 분포 (로그정규, 중앙값 60 kPa)</text>
<polygon points="64.0,288.0 64.0,288.0 71.9,288.0 79.7,287.9 87.6,287.8 95.5,287.6 103.3,287.2 111.2,286.5 119.1,285.5 126.9,284.0 134.8,282.1 142.7,279.8 150.5,277.0 158.4,274.0 166.3,270.7 174.1,267.3 182.0,264.0 189.9,260.9 197.7,258.2 205.6,255.9 213.5,254.1 221.3,252.9 229.2,252.2 237.1,252.0 244.9,252.3 252.8,253.1 260.7,254.3 268.5,255.7 276.4,257.4 284.3,259.3 292.1,261.2 300.0,263.3 307.9,265.3 315.7,267.3 323.6,269.3 331.5,271.1 339.3,272.9 347.2,274.5 355.1,276.0 362.9,277.4 370.8,278.7 378.7,279.8 386.5,280.8 394.4,281.8 402.3,282.6 410.1,283.3 418.0,283.9 425.9,284.5 433.7,285.0 441.6,285.4 449.5,285.8 457.3,286.1 465.2,286.4 473.1,286.6 480.9,286.8 488.8,287.0 496.7,287.1 504.5,287.3 512.4,287.4 520.3,287.5 528.1,287.6 536.0,287.6 536.0,288.0" fill="currentColor" fill-opacity="0.12"/>
<polygon points="158.4,288.0 158.4,274.0 166.3,270.7 174.1,267.3 182.0,264.0 189.9,260.9 197.7,258.2 205.6,255.9 213.5,254.1 221.3,252.9 229.2,252.2 237.1,252.0 244.9,252.3 252.8,253.1 260.7,254.3 268.5,255.7 276.4,257.4 284.3,259.3 292.1,261.2 300.0,263.3 307.9,265.3 315.7,267.3 323.6,269.3 331.5,271.1 339.3,272.9 347.2,274.5 347.2,288.0" fill="currentColor" fill-opacity="0.32"/>
<polyline points="64.0,288.0 71.9,288.0 79.7,287.9 87.6,287.8 95.5,287.6 103.3,287.2 111.2,286.5 119.1,285.5 126.9,284.0 134.8,282.1 142.7,279.8 150.5,277.0 158.4,274.0 166.3,270.7 174.1,267.3 182.0,264.0 189.9,260.9 197.7,258.2 205.6,255.9 213.5,254.1 221.3,252.9 229.2,252.2 237.1,252.0 244.9,252.3 252.8,253.1 260.7,254.3 268.5,255.7 276.4,257.4 284.3,259.3 292.1,261.2 300.0,263.3 307.9,265.3 315.7,267.3 323.6,269.3 331.5,271.1 339.3,272.9 347.2,274.5 355.1,276.0 362.9,277.4 370.8,278.7 378.7,279.8 386.5,280.8 394.4,281.8 402.3,282.6 410.1,283.3 418.0,283.9 425.9,284.5 433.7,285.0 441.6,285.4 449.5,285.8 457.3,286.1 465.2,286.4 473.1,286.6 480.9,286.8 488.8,287.0 496.7,287.1 504.5,287.3 512.4,287.4 520.3,287.5 528.1,287.6 536.0,287.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="64.0" y1="288.0" x2="536.0" y2="288.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="64.0" y1="288.0" x2="64.0" y2="292.0" stroke="currentColor"/><text x="64.0" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">20</text>
<line x1="158.4" y1="288.0" x2="158.4" y2="292.0" stroke="currentColor"/><text x="158.4" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">40</text>
<line x1="252.8" y1="288.0" x2="252.8" y2="292.0" stroke="currentColor"/><text x="252.8" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">60</text>
<line x1="347.2" y1="288.0" x2="347.2" y2="292.0" stroke="currentColor"/><text x="347.2" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">80</text>
<line x1="441.6" y1="288.0" x2="441.6" y2="292.0" stroke="currentColor"/><text x="441.6" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">100</text>
<line x1="536.0" y1="288.0" x2="536.0" y2="292.0" stroke="currentColor"/><text x="536.0" y="303.0" font-size="10" fill="currentColor" text-anchor="middle">120</text>
<text x="300.0" y="318.0" font-size="10.5" fill="currentColor" text-anchor="middle">흙의 비절삭 저항 (kPa)</text>
<text x="300.0" y="336.0" font-size="10.5" fill="currentColor" text-anchor="middle">현장: 40 kPa보다 무름 5.2% · 범위 안 82.3% · 80 kPa보다 단단함 12.5%</text>
</svg>

흙의 절삭 저항에 따라 S2가 한 패스에 깎는 두께다. 시뮬레이터에 맞춘 제어기는 $3.6\,\mathrm{kN}$을 미는데, 이 힘은 시뮬레이터의 $60\,\mathrm{kPa}$ 흙에서만 계획한 $0.100\,\mathrm{m}$를 깎고 $80\,\mathrm{kPa}$에서는 $0.075\,\mathrm{m}$, 곧 4분의 1이 모자라게 깎는다. 저항을 감지하며 $40$–$80\,\mathrm{kPa}$에서 학습한 제어기는 그 범위 전체에서 $0.100\,\mathrm{m}$를 지키고, 같은 범위에서 안전하게 만든 블라인드 제어기는 $60\,\mathrm{kPa}$에서 $0.067\,\mathrm{m}$, $80\,\mathrm{kPa}$에서 $0.050\,\mathrm{m}$를 깎는다. 아래 띠는 이 페이지의 현장 분포로, 범위가 현장의 $82.3\%$를 덮고 더 무른 $5.2\%$와 더 단단한 $12.5\%$를 놓친다.

### 1. Reality gap은 어디서 생기나

*한 문장으로:* 격차는 시뮬레이터의 오차가 아니라 그 오차가 한 정책의 과제 지표에 하는 일이다. 그래서 같은 틀린 숫자가 한 제어기에게서는 매 패스의 4분의 1을 빼앗고 다른 제어기에게서는 아무것도 빼앗지 않는다.

| 격차 | 필드 로봇의 예 | 대표 대응 |
|---|---|---|
| 동역학 | 질량·마찰·유압 지연·백래시 | 시스템 식별, 파라미터 랜덤화, 잔차 모델 |
| 접촉·재료 | 흙·잔해·타이어 슬립·절삭 저항 | 지형 랜덤화, 학습 접촉 모델, 온라인 적응 |
| 센싱 | 먼지·눈부심·진동·지연·LiDAR 누락 | 노이즈/지연 모델, 증강, 강건 추정 |
| 과제 분포 | 새로운 현장·형상·날씨·작업자 | 절차적 장면, 커리큘럼, 실제 데이터 파인튜닝 |
| 구현 | 제어 주기·포화·메시지 손실 | hardware-in-the-loop, 지연·한계 랜덤화 |

핵심 질문은 “그래픽이 사실적인가?”가 아니라 **정책에 영향을 주는 변수를 무엇까지 표현·
변동·적응했는가**다.

**접촉·재료 행에 있는 S2의 격차.** S2의 절삭 저항은 표 둘째 행의 한 항목이고, 숫자 하나다. 시뮬레이터는 $60\,\mathrm{kPa}$라 하고, 현장은 제 흙이 말하는 대로다. 계산 절의 현장인 $80\,\mathrm{kPa}$에서는, 시뮬레이션에서 계획한 $0.1\,\mathrm{m}$를 깎던 힘이 $0.075\,\mathrm{m}$를 깎는다. 견주는 한쪽인 시뮬레이터도 정확하지 않다. 앞선 실시간 토양 모델들도 입자 수준 기준 모델에 대해 대략 10–25%까지만 검증되어 있으므로([[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋 §4]]), 그중 어느 것에서 읽은 굴착력이든 현장이 제 오차를 더하기 전에 이미 그만큼의 오차를 안고 있다. 그 부족분이 격차이고, 잴 수 있을 만큼 정확한 정의가 필요하다. 느슨하게 쓰면 이 말은 불일치 자체, 곧 표의 행들을 가리키는데, 이 페이지는 그것을 격차의 *원천*이라 부른다.

> **Reality gap의 정의.** 정책의 **reality gap**(현실 격차)은 한 정책이 시뮬레이터에서 이룬 것과 실제 시스템에서 이룬 것 사이의 *잰 과제 성능 차이*다. 시뮬레이터만의 성질이 아니고, 그것을 일으키는 파라미터 오차도 아니다. 정의 조건 셋. **고정된 정책 하나**: 두 평가 사이에 정책의 어떤 것도 갱신되지 않는다. 갱신되면 그 차이는 격차가 아니라 적응을 잰 것이다. 두 세계에서 **같은 과제와 같은 지표**: 과제 사례, 초기 조건, 성공의 정의가 같아서 두 숫자를 견줄 수 있다. 그리고 **두 숫자 모두 잰 값**: 시뮬레이션 값은 시뮬레이터에서, 실제 값은 실제 시스템에서 재며, 어느 쪽도 다른 쪽에서 예측하지 않는다.
>
> $$\rho=\frac{J_{\text{real}}(\pi)}{J_{\text{sim}}(\pi)},\qquad \Delta J=J_{\text{sim}}(\pi)-J_{\text{real}}(\pi)$$
>
> $\pi$는 정책, $J$는 그 과제 지표(성공률, 절삭 두께, 시간당 부피), $\rho$는 §4가 유용한 측정값으로 드는 현실/시뮬 성능 비율이다. $\rho=1$이면 이 지표에서 격차가 없다. 정책이 시뮬레이션에서 한 일을 현실에서도 하기 때문이다.
>
> - **예**: S2의 제어기, 지표는 패스당 절삭 두께. 시뮬레이션에서 $J_{\text{sim}}=0.100\,\mathrm{m}$이고, $80\,\mathrm{kPa}$ 현장에서는 같은 $3.6\,\mathrm{kN}$이 $3.6/(80\times0.6)=0.075\,\mathrm{m}$를 깎으므로 $\rho=0.75$, $\Delta J=25\,\mathrm{mm}$다.
> - **비예**: "시뮬레이터의 $k_c$가 $20\,\mathrm{kPa}$ 낮다." 그것은 원인, 곧 파라미터 오차이고, 그 격차는 정책에 달려 있다. 같은 $20\,\mathrm{kPa}$가 힘을 고정한 제어기에게서는 매 패스의 4분의 1을 빼앗고, 저항을 감지하며 $40$–$80\,\mathrm{kPa}$에서 학습한 제어기에게서는 아무것도 빼앗지 않는다(§6).
> - **비예**: 시뮬레이션 성공률 대 실제 패스로 파인튜닝한 뒤의 실제 성공률. 뒤의 숫자는 다른 정책의 것이므로, 그 차이에는 격차와 적응이 되찾은 몫이 섞여 있다.
> - **왜 중요한가**: 격차는 정책–시뮬레이터 쌍의 것이므로 양쪽에서 닫을 수 있다. 시뮬레이터를 바로잡거나(식별, §7), 정책이 시뮬레이터가 틀린 것에 둔감해지게 하거나(랜덤화, 잔차, 적응: §6, §8). 시뮬레이터 충실도만, 또는 실제 성공만 보고한 논문은 그 절반만 보고한 것이다.

**격차의 부호가 어느 요구조건이 깨질지를 정한다.** 더 무른 땅에서는 같은 $3.6\,\mathrm{kN}$이 더 깊이 깎는다. $40\,\mathrm{kPa}$에서는 $3.6/(40\times0.6)=0.150\,\mathrm{m}$, 계획보다 $50\,\mathrm{mm}$ 더 깎는다. 트렌치 중간에서는 흙이 더 오는 것이고, 버킷이 그것을 막는다. 계획한 패스가 버킷을 산적 용량의 $k_f=0.85$까지 채우므로, 어떤 패스도 계획 부피의 $1/0.85=1.18$배보다 많이 담지 못하고 나머지는 흘러넘친다. 바닥에 닿는 패스라면 S2의 $\pm30\,\mathrm{mm}$ 고저를 벗어난 과굴착이다. 더 단단한 땅에서는 대신 생산성이 깨진다. 시뮬레이터 숫자 하나가 현실이 그것을 어느 쪽으로 옮겼는지에 따라 서로 다른 두 요구조건을 깬다.

> [!warning] 접촉 행은 나머지와 성격이 다르다
> 모든 격차에는 *파라미터* 오차와 **모델 형식·커버리지** 오차가 함께 있을 수 있다. 동정이나
> 랜덤화를 고르기 전에 범위가 틀린 것인지, 현상·상태·사건·과제 사례가 빠진 것인지 진단하라.
> 접촉은 모델 형식 오차가 특히 지배적이기 쉬운 경우다. 강체 엔진은 접촉을 매 시간 단계마다 푸는 점 구속으로 처리한다. 즉 짧은 시간 단계마다 몇 개의 접촉점을 골라 물체가 서로 뚫고 들어가지 않게 하는 힘을 계산한 뒤 모든 것을 앞으로 진행시킨다. 그런데 바탕 동역학이
> 실제로 비평활하다 — 충격과 고착–미끄러짐 천이가 불연속이고, 수치 적분기는 정확히 거기서 정확도와
> 안정성을 함께 잃는다. **마찰 계수를 랜덤화한다고, 접촉 패치를 애초에 표현하지 못하는 접촉 모델이
> 고쳐지지는 않는다.**
>
> 그래서 접촉이 많은 결과와 보행 결과는 같은 시뮬레이터에서 나왔더라도 sim-to-real 성숙도의 증거로
> 비교할 수 없다. 사족보행은 거친 접촉 모델을 견딘다 — 정책이 50 Hz로 외란을 기각하고 있고 발은
> 미끄러지지만 않으면 되기 때문이다. 반면 삽입·드릴링·패널 안착은 그 모델이 표현하지 못하는 접촉
> 패치로 *정의되는* 과제다. "시뮬레이션에서 전이했다"는 주장의 강도는 과제가 이 선의 어느 쪽에
> 있느냐에 달려 있다.

<svg viewBox="0 0 560 266" style="max-width:100%;height:auto" role="img" aria-label="랜덤화가 실제 곡선을 덮는 파라미터 격차와, 시뮬레이션 곡선은 모두 매끄러운데 실제는 도약하는 접촉 격차">
  <g font-size="11" fill="currentColor">
    <text x="50" y="16">파라미터 문제</text><text x="330" y="16">모델 문제</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.75">
    <text x="50" y="29">동역학 &#183; 센싱 &#183; 과제 분포 &#183; 구현</text><text x="330" y="29">접촉 &#8212; 미끄럼 속도에 대한 마찰력</text>
  </g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.5" fill="none">
    <polyline points="50,40 50,150 250,150"/>
    <line x1="330" y1="105" x2="530" y2="105"/>
    <line x1="430" y1="44" x2="430" y2="154"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.4" stroke-dasharray="5 4">
    <path d="M50,132 C110,106 180,84 250,72"/>
    <path d="M50,144 C110,122 180,102 250,92"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <path d="M50,138 C110,114 180,93 250,82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.45" stroke-dasharray="5 4">
    <path d="M338,74 C412,74 448,136 522,136"/>
    <path d="M338,86 C412,86 448,124 522,124"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <polyline points="338,66 428,66"/>
    <polyline points="432,144 522,144"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="62" y="58">실제는 이 퍼짐 안에 있다</text>
    <text x="330" y="176">시뮬레이션 곡선은 모두 매끄럽다</text>
    <text x="330" y="190">실제는 고착&#8211;미끄럼 천이에서 도약한다</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">왼쪽: 물리는 맞고 숫자가 틀렸으니, 그 숫자에 대한 분포가 실제 시스템을 덮는다. 오른쪽: 고착이</text>
    <text x="24" y="228">미끄럼으로 넘어가는 순간이 불연속인데, 정규화된 강체 접촉은 하필 그 자리를 매끄럽게 지난다.</text>
    <text x="24" y="244">마찰 계수를 흔들면 저 곡선들이 위아래로 움직일 뿐, 그들이 가질 수 없는 형태를 만들어 주지는</text>
    <text x="24" y="260">않는다. 보행 전이와 삽입 전이가 비교 가능한 증거가 아닌 이유가 이것 하나다.</text>
  </g>
</svg>

**S2의 흙은 그 선의 어느 쪽에 있나.** $60$이 아니라 $80\,\mathrm{kPa}$인 흙은 왼쪽 그림이다. 법칙 $F_c=k_c\,w\,d$는 맞고 그 안의 숫자 하나가 틀렸으니, $k_c$의 범위가 그 현장을 덮을 수 있다. 트렌치 밑의 큰 돌은 오른쪽 그림이다. 이빨이 암석을 만나는 순간 튀어 오르는 힘을 재현하는 $k_c$ 값은 없으므로, 어떤 $k_c$ 범위도 그것을 덮지 못한다. 범위에서 학습한 정책이 그래도 버티는지는 실험으로 답할 문제다. Egli 등(2022)이 실제 12톤 굴착기로 그것을 물었다. 시험장 흙이 비교적 무르기 때문에 굴착 경로에 화강암 덩어리를 묻어 극도로 단단한 흙을 흉내 냈고, 에피소드마다 한 번씩 뽑은 랜덤 토질로 학습한 정책은 그 덩어리 위를 긁고 지나가면서도 버킷을 채웠다([[01-canonical-papers/notes/8-construction/egli-rl|노트]]; 그 증거는 §4가 읽는다).

### 2. 주요 전략

*한 문장으로:* 전략마다 격차를 다른 쪽에서 닫고, S2에서는 저마다 구체적인 모양이 있다 — $k_c$를 재거나, $k_c$에 걸쳐 학습하거나, 학생이 $k_c$를 추론하게 하거나, 한계 안에서 제어기를 보정하거나, 몇 번의 실제 패스로 적응한다.

- **시스템 식별**은 측정 궤적에 시뮬레이터 파라미터를 맞춘다. 한 조건에는 정확해지지만 한
  기계에 과적합할 수 있다. 이 스트림의 정본 성과가
  [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL]]이다: 학습된 신경망
  밸브/액추에이터 모델이 굴착기 시뮬레이터를 충분히 충실하게 만들어 RL 정책이 파인튜닝
  없이 실제 M545에서 돈다. S2에서는 몇 번의 패스에서 잰 힘과 두께로 현장의 $k_c$를 재는 것이다(§7). 방법 일반은 [[04-robotics/system-identification|5.5 시스템 식별 §1]]이다.
- **도메인 랜덤화**는 동역학·센싱·장면 파라미터의 분포에서 학습한다. 현실이 유용한 학습
  분포 안에 있어야 하며, 무조건 더 많이 흔든다고 좋아지지 않는다. S2에서는 학습 에피소드마다 $[40,\ 80]\,\mathrm{kPa}$에서 새 $k_c$를 뽑는다. 정의는 아래에 있고, 범위의 값은 §6이 매긴다.
- **교사–학생/privileged learning**은 교사가 완벽한 자세나 지반 파라미터 같은 시뮬레이터
  전용 상태를 보고, 배치 가능한 관측만 쓰는 학생에게 행동을 증류한다. 시험 때 가능한
  정보를 반드시 확인하라. S2에서 교사는 $k_c$를 본다. 실린더 압력과 관절 각도를 보는 학생도 그것을 되찾을 수 있는데, 한 패스의 힘과 두께가 $k_c=F_c/(w\,d)$를 주기 때문이다. 반면 묻힌 큰 돌은 이빨이 부딪칠 때까지 학생에게 보이지 않는다. 방법은 [[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]]가 가르친다.
- **잔차 학습**은 모델 기반 제어기를 유지하고 보정량만 학습한다. 탐색 공간을 줄일 수 있지만,
  안전은 여전히 잔차를 어떻게 제한하느냐에 달려 있다. S2에서는 $3.6\,\mathrm{kN}$ 제어기를 두고 $\lvert\Delta F\rvert\le B$인 보정 $\Delta F$를 학습한다. §8이 정의하고 $B$의 값을 매긴다.
- **실데이터 적응**은 소량의 실제 데이터로 표현·동역학·정책을 조정한다. 실제 장비 시간과
  인간 개입 비용을 보고해야 한다. S2에서 가장 싼 형태는 §7의 감독된 시험 패스 네 번이다.
- **병렬 시뮬레이션**은 경험 생산량을 늘릴 뿐 물리의 타당성을 보장하지 않는다. S2에서는 $k_c=60\,\mathrm{kPa}$인 환경 만 개가 $60\,\mathrm{kPa}$ 흙을 만 번 가르친다.

도메인 랜덤화는 가장 자주 이름이 불리고 가장 드물게 명세되는 전략이라, 여기서 온전한 정의를 준다.

> **도메인 랜덤화의 정의.** **도메인 랜덤화**(domain randomization)는 시뮬레이터 파라미터의 분포에 걸쳐 정책 하나를 학습하는 *학습 절차*다. 강건성 결과도, 시험 규약도 아니다. 정의 조건 넷. 시뮬레이터의 이름 붙은 **파라미터 벡터** $\theta$, 여기서는 $k_c$. 지지 집합과 모양을 밝힌 **학습 분포** $p_{\text{train}}(\theta)$, 에피소드마다 새로 뽑는다. 정책은 **$\theta$를 받지 않는다**: 관측할 수 있는 것으로 행동하므로, 무엇을 배우든 분포 전체에서 통해야 한다. 그리고 목적 함수가 **분포에 걸쳐 평균한다**:
>
> $$\pi^\star=\arg\max_{\pi}\ \mathbb{E}_{\theta\sim p_{\text{train}}}\big[J(\pi;\theta)\big]$$
>
> $J(\pi;\theta)$는 파라미터 $\theta$로 돌린 시뮬레이터에서 정책이 얻는 return이다. 그러므로 실제 시스템은 $p_{\text{train}}$에서 한 번 더 뽑은 표본처럼 보이는 만큼만 덕을 보고, 그것을 재는 것이 §6의 포함률이다.
>
> - **예**: $k_c\sim\mathcal U[40,\ 80]\,\mathrm{kPa}$로, 에피소드마다 새 흙으로 학습한 S2의 제어기.
> - **비예**: 같은 표본을 쓰되 $k_c$를 정책의 입력으로 넣는 것. 그것은 흙에 조건화된 정책이고, 기계에서는 어디선가 $k_c$를 얻어야 한다. 식별(§7)이나, 그것을 추론하는 학생(위)에게서.
> - **비예**: 평가 때만 $k_c$를 훑는 것. 강건성을 잴 뿐 아무것도 학습시키지 않는다.
> - **왜 중요한가**: 정책이 랜덤화에서 무엇을 얻는지는 무엇을 감지할 수 있는지에 달려 있다. 절삭력을 관측하는 정책은 범위 전체에서 적응하는 법을 배울 수 있고, 블라인드 정책은 범위의 최악에 대비해 헤지할 수밖에 없어 모든 흙에서 폭의 값을 치른다(§6).

### 3. 배치 사다리

1. 보지 않은 파라미터에서 시뮬레이터 평가 —
   [[01-canonical-papers/notes/8-construction/exact-2024|ExACT]]가 여기에 있다:
   멀티모달 센서에서 유압 밸브 명령까지의 end-to-end 모방이지만 시뮬레이션 검증뿐이라
   주장은 이 단에서 멈춘다
2. hardware-in-the-loop와 지연·포화 시험
3. 안전 영역 안의 저속·감독 실제 시험
4. 평가 사례를 보며 튜닝하지 않는 적응: 정책은 실데이터로 갱신해도 되지만, 점수를 매기는 시험 과제·현장·조건은 고정되고 튜닝에 쓰이지 않는다
5. 재료·기계·현장·날짜를 바꾼 반복 운용

Zero-shot transfer는 배치 전에 목표 도메인 학습 업데이트가 없다는 뜻이지, 시뮬레이터를
만드는 데 실제 시스템 지식을 전혀 쓰지 않았다는 뜻이 아니다.

> **Zero-shot 전이의 정의.** **Zero-shot 전이**(zero-shot transfer)는 *배치 규약*의 성질, 곧 학습이 끝난 때부터 실제 평가까지 무엇이 바뀌어도 되는가의 성질이다. 시뮬레이터를 어떻게 만들었는지에 관한 진술도, 정책의 내부 상태에 관한 진술도 아니다. 정의 조건 셋. 정책의 학습된 **파라미터가 고정된다**: 시뮬레이션 학습이 끝난 때부터 실제 평가가 끝날 때까지. **목표 도메인 데이터가 학습 갱신에 들어가지 않는다**: 평가 전에도, 평가 중에도. 그리고 평가가 **목표 시스템 위에서** 이루어진다. 떼어 둔 시뮬레이터는 1단이지 전이가 아니다.
>
> $$\phi_{\text{deployed}}=\phi_{\text{sim}}$$
>
> $\phi$는 정책의 학습된 파라미터(신경망의 가중치, 제어기의 튜닝된 상수)이고 $\phi_{\text{sim}}$은 시뮬레이션 학습이 끝났을 때의 값이다. 그러므로 정책이 온라인으로 계산하는 추정값은 평가 중에 바뀌어도 되지만, 그것을 계산하는 파라미터는 바뀌면 안 된다.
>
> - **예**: $[40,\ 80]\,\mathrm{kPa}$에서 학습해 $80\,\mathrm{kPa}$ 현장에서 돌리는 S2의 적응형 제어기. 흙에 대한 추정은 패스마다 움직이지만 학습된 파라미터는 움직이지 않는다.
> - **예**: M545 위의 Egli RL(§2)은 실기계 데이터가 시뮬레이터 안의 액추에이터 모델을 만들었는데도 zero-shot이다. Werner 등(2026)은 같은 학습 가중치를 11.5톤 굴착기와 500그램 탁상 로봇에 쓰고, 보정된 기계 인터페이스를 거쳐 배치한다. 가중치로는 zero-shot이고, 실제 시스템 지식은 보정으로 옮겨 갔다.
> - **비예**: §7의 시험 패스 뒤에 제어기의 $k_c$를 추정값으로 다시 맞추는 것. 배치된 제어기의 파라미터 하나를 목표 데이터에 맞췄으므로 few-shot 적응이고, 점수를 매기는 사례가 고정되어 있다면 4단이다.
> - **왜 중요한가**: "zero-shot"은 좁은 질문 하나에만 답한다. 어떤 실데이터가 시뮬레이터를 만들었는지, 정책이 온라인으로 무엇을 적응하는지는 따로 물어라. 어느 쪽이든 전이의 대부분을 떠맡을 수 있다. [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §5]]는 RL 실험 절에서 확인해야 할 표현으로 이 말을 든다.

물리적으로 그럴듯한 정책도 하드웨어의 지연·포화로 실패할 수 있어 단계별 불확실성을 나눈다. 즉시 구동하는 시뮬레이션의 굴착 명령이 실제 제어 인터페이스에서는 늦게 도착할 수 있다. **여기서 얻는 독법.** 단계 이동이 검증하는 것을 밝히고 후속 튜닝을 미관측 평가에서 분리한다. 단계 상승은 큰 기계에서 같은 동작을 촬영하는 것보다 경계에 대한 증거를 추가하는 일이다.

**S2 위의 같은 사다리.** 1단: $[40,\ 80]\,\mathrm{kPa}$에서 학습하고 학습이 한 번도 뽑지 않은 흙, $35$와 $90\,\mathrm{kPa}$에서 평가한다. 2단은 S2의 밸브 지연이 사는 곳이다. 명령은 보낸 뒤 $\tau_h=0.15\,\mathrm{s}$가 지나서야 움직임이 되고, 마무리 패스에서 날 끝은 $v=0.3\,\mathrm{m/s}$로 움직이므로, 보정이 효과를 내기 전에 경로를 따라 $\tau_h v=0.15\times0.3=0.045\,\mathrm{m}$를 간다. $45\,\mathrm{mm}$는 고저가 양쪽으로 허용하는 $30\,\mathrm{mm}$의 1.5배이고, 즉시 구동하는 시뮬레이터에서는 보이지 않는다([[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]도 지연을 같은 방식으로 거리로 읽는다). 3단은 느리고 감독되는 §7의 시험 패스다. 4단은 점수를 매기는 트렌치 구간을 고정한 채 실제 패스로 다시 식별하거나 적응한다. 5단은 §6의 현장 분포 자체에서 표본을 뽑는다. 다른 흙, 다른 기계, 다른 날.

### 4. 증거 읽기

> [!warning] 주장 읽기
> “성공적인 sim-to-real”은 보고된 기계·운용 범위·개입 규약에서만 전이를 증명한다. 랜덤화한
> 변수, 실데이터 예산, 안전 제어기, 실패 시행, 평가 조건을 튜닝에 썼는지 확인하라. 영상은
> 가능성의 증거이지 전이 분포의 증거가 아니다.

유용한 측정값은 현실/시뮬 성능 비율, 시간당 개입, 제약 위반, 파라미터 변화별 성능, 적응
데이터·시간, 학습 범위 밖의 성능 저하다.

> [!example] 계산 예제 · Worked example
> **개별 범위의 포함률과 동시 포함률은 다르다.** 무작위화한 파라미터 6개가 각각 실제 주변분포의 80%를 덮는다고 하자. 실제 파라미터들이 독립이면 모든 범위 안에 실제 조건이 들어갈 확률은 0.8⁶ ≈ **26%** 수준이다. 각각 90%를 덮으면 0.9⁶ ≈ **53%** 수준이다.
>
> **여기서 얻는 독법.** 강건성 주장을 읽기 전에 변수, 범위, 의존 관계를 확인한다. 첫 가상 설정에서는 실제 결합 조건의 약 74%가 무작위화 상자 밖에 있다. 이는 예상 실패율이 아니며 상자 안을 충분히 표집했다는 증거도 아니다. 실제 파라미터의 상관도 포함률을 바꾼다. 학습 범위와 실제 전이 평가를 구분한다.

**점검표를 논문 하나에 돌려 보기.** Egli 등의 토질 적응 굴착(RA-L 2022)은 위 상자의 질문 대부분에 본문 스스로 답하고, 그래서 꼼꼼히 읽을 가치가 있다. *랜덤화한 변수와 범위*: 토공 기본 방정식의 토질 파라미터 여섯 개를 에피소드가 시작될 때마다 균등 분포로 뽑는다(점착력 $0$–$105\,\mathrm{kPa}$, 부착력 $0$부터 점착력까지, 내부 마찰각 $0.3$–$0.8\,\mathrm{rad}$, 단위중량 $17$–$22\,\mathrm{kN/m^3}$, 토양–버킷 마찰각 $0.2$–$0.4\,\mathrm{rad}$, 공동 압력 계수 $0$–$300$). 여기에 토양 높이가 더해진다. 논문은 실제 흙의 분포를 밝히지 않으므로 §6의 뜻의 포함률은 거기서 계산할 수 없다. *정책이 감지하는 것*: 관측에 관절 토크가 들어 있고, 기계에서는 실린더 압력에서 나온다. 학습 때 관측에는 잡음이 없다. 저자들은 토크 관측 없이도 정책을 학습해 보았는데, 기계의 토크 한계에 한참 못 미치는 곳에만 머무는 지나치게 조심스러운 제어기가 나왔다. §6의 블라인드 정책을 실제 학습에서 만난 것이다. *실데이터와 단*: 정책은 시뮬레이션에서만 학습하고, 기계 자체의 관절 속도 제어기를 거쳐 12톤 기계에서 돈다. 흙이 비교적 무른 시험장에 화강암 덩어리를 묻은 곳에서이고, 그래서 3단에 놓인다. *실패하거나 덜 된 시행*: 기계에 가까이 붙여 시작한 굴착은 자기 충돌을 피하려고 일찍 들어 올려 버킷을 3분의 1쯤($0.32$)만 채운다. *지표*: 보고된 버킷 채움은 흙 속 버킷 경로를 적분해 계산하며 그 흙이 모두 버킷에 들어간다고 가정하므로, 측정이 아니라 추정이다.

### 5. 이 흐름은 어디로 가고 있나 (2019–2025)

[[05-construction-robotics/lineage|계보 §6]]과 같은 방식으로 세면, 학습 — 딥, 강화, 모방 — 을 말하는 건설 로봇 제목은 2019–2021년 $9$편에서 2023–2025년 $30$편으로, 건설 로봇 논문의 $7\%$에서 $12\%$로 늘었다. 이 학술지들의 제어 학습 연구에는 가상 시연으로 끌어올린 장기 건설 작업의 강화학습(Huang 외, *AutCon* 146, 2023, [DOI](https://doi.org/10.1016/j.autcon.2022.104691)), 심층 강화학습을 쓴 예측 기반 경로 계획(Cai 외, *J. Computing in Civil Engineering* 37, 2023, [DOI](https://doi.org/10.1061/(asce)cp.1943-5487.0001056)), 인간–로봇 협업을 위한 안전 제약 강화학습(Duan 외, *AutCon* 174, 2025, [DOI](https://doi.org/10.1016/j.autcon.2025.106130)), 그리고 Li 외가 정리한 시연 학습(*AEI* 62, 2024, [DOI](https://doi.org/10.1016/j.aei.2024.102625))이 있다. 건설 규모의 실제 하드웨어에서 보인 전이는 찾기 더 어렵다. [[01-canonical-papers/notes/8-construction/apolinarska-timber|Apolinarska 외의 목재 삽입]]이 확인된 건설 학술지의 예이고, 파운데이션 모델은 2025년까지 이 학술지들에 제목 하나로만 닿았다. 그러니 건설 학술지의 학습 논문을 §3의 사다리에 올릴 때는, 단을 가정하기 전에 방법 절에서 어디서 평가했는지 읽어라.

### 6. 랜덤화 범위는 얼마나 넓어야 하나

*한 문장으로:* 랜덤화 범위의 값어치는 그것이 덮는 실제 현장의 몫이고, 그 몫을 계산하려면 실제 흙의 분포가 있어야 한다. 그리고 범위가 무엇을 사 주는지는 정책이 흙을 감지할 수 있는지에 달려 있다. 블라인드 정책은 폭 1킬로파스칼마다 더 얕은 절삭으로 값을 치르고, 적응형 정책은 치르지 않는다.

**실제 분포가 먼저다.** 포함률을 구하려면 중요한 배치들에 걸쳐 실제 파라미터가 어떻게 퍼지는지 알아야 하고, 이 페이지는 S2를 위해 하나를 고정한다. 트렌치를 팔 수 있는 현장들에 걸쳐 $\ln k_c$는 평균 $\ln60$, 표준편차 $0.25$인 가우시안이므로 $k_c$는 **로그정규**다. 양수이고, 단단한 흙 쪽으로 치우쳐 있으며, 중앙값이 $60\,\mathrm{kPa}$다. 그래서 시뮬레이터는 중앙값 현장에서는 맞고 대부분의 다른 현장에서는 틀린다. 모양이 그럴듯하도록 고른 교과용 가정이지 조사 자료에 맞춘 것이 아니다. 확률은 표준정규 CDF, 곧 표준정규 $Z$에 대한 $\Phi(z)=P(Z\le z)$에서 나온다([[02-foundations/probability|3. 확률 §2–§3]]). $\ln k_c$가 가우시안이기 때문이다. 현장이 $80\,\mathrm{kPa}$보다 단단할 확률은 $1-\Phi\big(\ln(80/60)/0.25\big)=1-\Phi(1.151)=0.125$이므로, 여덟 현장에 하나는 계산 절의 흙보다 단단하다.

> **랜덤화 포함률의 정의.** **포함률**(coverage)은 *확률*이고, 학습 범위와 실제 조건의 분포를 함께 놓았을 때의 성질이다. 범위만의 성질이 아니다. 정의 조건 셋. 중요한 배치들에 걸친 **실제 파라미터의 분포**를 밝힌다. 잰 것이거나, 가정한 것이라면 가정이라고 말한다. **학습 분포의 지지 집합**, 곧 학습이 한 번이라도 뽑은 값들의 집합. 그리고 포함률은 **결합**이다. 랜덤화한 파라미터가 여럿이면 모두가 동시에 각자의 범위 안에 들 확률이다(§4).
>
> $$C=P_{\text{real}}\big(\theta\in\operatorname{supp}p_{\text{train}}\big)=\Phi\Big(\frac{\ln(k_{hi}/60)}{0.25}\Big)-\Phi\Big(\frac{\ln(k_{lo}/60)}{0.25}\Big)$$
>
> $P_{\text{real}}$은 실제 분포 아래의 확률, $\operatorname{supp}p_{\text{train}}$은 학습 지지 집합이다. 둘째 꼴은 S2의 파라미터 하나짜리 경우로, 킬로파스칼 단위의 범위 $[k_{lo},k_{hi}]$를 현장 분포에 대 본 것이다. 로그정규 $k_c$가 범위 안에 드는 것은 가우시안 $\ln k_c$가 $\ln k_{lo}$와 $\ln k_{hi}$ 사이에 드는 것과 정확히 같기 때문이다.
>
> - **예**: $[40,\ 80]\,\mathrm{kPa}$는 S2 현장의 $\Phi(1.151)-\Phi(-1.622)=0.875-0.052=0.823$을 덮는다.
> - **비예**: "$k_c$를 공칭값 둘레 $\pm33\%$로 랜덤화했다." 폭은 포함률이 아니다. 같은 $[40,\ 80]$이 이 현장들의 $82.3\%$를 덮지만 중앙값 흙이 $80\,\mathrm{kPa}$인 현장 집단은 $49.7\%$만 덮고, 학습 값 하나 $[60,\ 60]$은 아무것도 덮지 않는다. 한 점의 확률은 $0$이기 때문이다.
> - **왜 중요한가**: "넓게 랜덤화했다"를 확인할 수 있는 숫자로 바꾸고, 논문이 좀처럼 보고하지 않는 입력 하나, 곧 실제 파라미터의 분포를 요구한다.

**킬로파스칼로 대칭인 범위는 확률로는 한쪽으로 기운다.** $[40,\ 80]$은 시뮬레이터 숫자의 양쪽으로 $20\,\mathrm{kPa}$씩 뻗지만, 무른 쪽에서 현장의 $5.2\%$를, 단단한 쪽에서 $12.5\%$를 놓친다. 분포가 $k_c$가 아니라 $\ln k_c$에서 대칭이기 때문이다. 가운데 $95\%$를 덮는 범위는 $60\,e^{\pm1.96\times0.25}=[36.8,\ 97.9]\,\mathrm{kPa}$로, 중앙값 아래로 $23\,\mathrm{kPa}$, 위로 $38$이다.

**범위가 무엇을 사 주는지는 정책이 무엇을 감지하는지에 달려 있다.** 절삭력을 관측하지 않는 **블라인드 정책**(blind policy)은 흙을 알기 전에 힘 하나를 정해야 한다. 범위 안 어디서도 계획보다 깊이 깎으면 안 된다면(고저 근처에서는 과굴착이 비싼 실수다), 쓸 수 있는 가장 큰 힘은 학습한 가장 무른 흙에서 정확히 $d_0$를 깎는 힘이다.

$$F_{\text{blind}}=k_{lo}\,w\,d_0,\qquad d=\frac{F_{\text{blind}}}{k_c\,w}=d_0\,\frac{k_{lo}}{k_c},$$

그보다 큰 힘은 $k_{lo}$에서 $d_0$보다 깊이 깎기 때문이다. $[40,\ 80]$에서 학습한 블라인드 정책은 $2.4\,\mathrm{kN}$을 밀어, 시뮬레이터 자신의 $60\,\mathrm{kPa}$ 흙에서도 $0.1\times40/60=0.067\,\mathrm{m}$만 깎는다. 강건성을 모든 곳에서의 더 얕은 절삭으로 산 것이다. 범위를 단단한 쪽으로 넓혀도 아무것도 바뀌지 않는다. $k_{lo}$만 들어가기 때문이다. **적응형 정책**(adaptive policy)은 만나는 힘을 관측해 $\operatorname{clip}(k_c,k_{lo},k_{hi})\,w\,d_0$를 민다. 범위 안에서는 맞는 힘을, 범위 밖에서는 학습한 가장 가까운 힘을 쓰므로, 현장의 흙을 한 번 느낀 뒤에는 현장이 덮이는 곳이면 어디서나 정확히 $d_0$를 깎는다(첫 패스가 치르는 값은 §8의 질문이다). clip은 "학습 범위 밖"을 나타내는 이 페이지의 모델이다. 실제 신경망은 깔끔하게 포화하지 않고, 시험해 보지 않은 무언가를 한다. Egli 등(2022)은 블라인드 경우를 실제 학습에서 만났다. 관절 토크 관측 없이 학습한 굴착 정책은 무른 흙과 기계를 멈추게 할 흙을 구별할 길이 없어 기계의 토크 한계에 한참 못 미치는 곳에만 머무는 지나치게 조심스러운 정책이 되었고, 관측에 토크가 있을 때는 온라인으로 적응했다([[01-canonical-papers/notes/8-construction/egli-rl|노트]]).

**훑기.** §9는 현장 200,000곳을 표본으로 뽑는다. 범위를 $[50,\ 70]$에서 $[30,\ 120]\,\mathrm{kPa}$로 넓히면 포함률은 $49.8\%$에서 $99.4\%$로 오르고, 적응형 정책의 패스당 흙은 계획의 $0.99$–$1.00$에 머무르는 반면 블라인드 정책의 것은 $0.847$에서 $0.516$으로 떨어진다. 랜덤화하지 않은 제어기는 결과가 평균이 아니라 꼬리인 이유를 보여 준다. 현장 전체에 걸쳐 평균하면 패스당 흙을 $2.1\%$밖에 잃지 않는데, 무른 현장의 과굴착과 단단한 현장의 부족이 상쇄되기 때문이다. 그런데 현장의 $12.4\%$에서는 4분의 1 이상 모자라고, $14.8\%$에서는 $30\,\mathrm{mm}$ 넘게 과굴착한다.

**둘째 파라미터는 곱해진다.** 채움 거동도 $k_c$와 독립으로, 현장의 $90\%$를 덮는 범위로 랜덤화하면 결합 포함률은 $0.823\times0.9=0.740$이다. §4의 산수가 이제 S2 위에 있다.

### 7. 몇 번의 패스로 흙을 식별하기

*한 문장으로:* 알려진 두께에서 힘을 기록하는 감독된 패스 몇 번이면 파라미터 하나짜리 최소제곱으로 $k_c$를 얻는다. 그 오차는 패스 수의 제곱근에 반비례해서만 줄고, 한 두께에서 몇 번을 파든 모델에 없는 항이나 패스 뒤에 바뀌는 흙은 드러나지 않는다.

흙을 덮는 대신 흙을 잴 수도 있다. **실험**: 현장의 처음 $n$번 패스를 계획한 두께에서 위치 제어로, 느리고 감독되게(§3의 3단) 돌리며 실린더 압력으로 절삭력을 읽는다. 두께는 위치 루프가 붙잡으므로 정확하다고 본다. 힘은 패스마다 $\sigma_F=0.3\,\mathrm{kN}$씩 흩어지고, 패스를 따라 변하는 흙도 여기에 들어 있다. **모델**은 대상의 법칙에 미지수 하나를 둔 $F_i=k_c\,a_i+e_i$, $a_i=w\,d_i$이다. [[04-robotics/system-identification|5.5 시스템 식별 §3]]의 뜻으로 파라미터에 선형이다. 회귀 변수 $a_i$는 기록에서 알고, $k_c$는 곱으로만 들어간다. **기준**은 최소제곱이고, 파라미터가 하나면 한 줄로 풀린다.

$$\hat k_c=\frac{\sum_i a_iF_i}{\sum_i a_i^2},\qquad \operatorname{sd}(\hat k_c)=\frac{\sigma_F}{\sqrt{\sum_i a_i^2}}=\frac{\sigma_F}{w\,d_0\sqrt n}$$

$\sum_i(F_i-k\,a_i)^2$의 도함수를 $0$으로 두면 첫 식이 나오고, 열이 하나인 $\Phi=(a_1,\dots,a_n)^\top$에 5.5 §3의 공분산 $\sigma^2(\Phi^\top\Phi)^{-1}$을 쓰면 둘째 식이 나오기 때문이다. 맨 오른쪽 꼴은 $n$번 패스가 모두 $d_0$에서일 때이고, 그때 $\hat k_c$는 평균 힘을 $w\,d_0$로 나눈 것일 뿐이다.

**80 kPa 현장에서.** $\sigma_F/(w\,d_0)=0.3/0.06=5\,\mathrm{kPa}$이므로 패스 한 번은 $k_c$를 표준편차 $5\,\mathrm{kPa}$로, 네 번은 $2.5$로 잡는다. $95\%$ 구간으로는 $\pm1.96\times2.5=\pm4.9\,\mathrm{kPa}$다. 추정으로 힘을 정하면, $F=\hat k_c\,w\,d_0$는 $d=d_0\,\hat k_c/k_c$를 깎으므로 계획에서 $\pm0.1\times4.9/80=\pm0.0061\,\mathrm{m}$ 안에 든다. 이를 절반으로 줄이려면 패스가 네 배 든다. $\pm2\,\mathrm{kPa}$는 $(1.96\times5/2)^2=24.0$, 곧 $25$번이다. 그리고 $\sigma_F$ 자체를 같은 네 번의 패스에서 추정하면 $1.96$이 스튜던트 $t_{3,0.975}=3.182$가 되어([[02-foundations/probability|3. 확률 §6]]) 구간이 $\pm8.0\,\mathrm{kPa}$로 넓어진다.

**모델에 없는 항은 한 두께에서는 보이지 않는다.** 실제 힘에 법칙이 빠뜨린 오프셋이 있다고 하자. 두께에 비례하지 않는 버킷 옆면의 끌림 같은 것으로, $F=k_c\,w\,d+F_{\text{off}}$, $F_{\text{off}}=0.6\,\mathrm{kN}$이다. 그러면 $d_0$에서의 패스는 모두 $k_c\,w\,d_0+F_{\text{off}}$를 읽으므로, 파라미터 하나짜리 맞춤은 $80+0.6/0.06=90\,\mathrm{kPa}$를 내놓고, $0.1\,\mathrm{m}$에서는 정확히 맞는다. 모델이 자기 기록 위에서는 완벽하게 검증된다. $0.05\,\mathrm{m}$ 마무리 층을 시키면 $90\times0.6\times0.05=2.7\,\mathrm{kN}$을 명령하는데, 그중 $0.6$은 오프셋에 들어가므로 $2.1/(80\times0.6)=0.044\,\mathrm{m}$, $6.3\,\mathrm{mm}$ 모자라게 깎는다. 모든 패스가 한 두께에 있는 한 $F_{\text{off}}$를 둘째 파라미터로 더해도 소용없다. 그때 두 열 $a_i$와 $1$이 비례해 랭크가 1이고, 둘 사이의 나눔은 임의다. 오프셋은 그런 항의 하나일 뿐이다. 토공 기본 방정식에는 두께의 제곱으로 자라는 흙 무게 항이 더 있고([[05-construction-robotics/earthmoving-heavy-machinery|3. 토공 §2]]), 한 두께의 패스는 그것도 똑같이 숨긴다. 파라미터 둘에는 두께 둘이 최소한의 여기이고([[04-robotics/system-identification|5.5 시스템 식별 §4]]), 맞춤이 본 적 없는 두께의 패스가 빠진 항을 잡아내는 검증이다([[04-robotics/system-identification|5.5 시스템 식별 §6]]). 과제의 실행 문항이 네 조합을 모두 돌린다. 두께를 붙잡지 않고 쟀다면 그 잡음이 회귀 변수에 실려 $\hat k_c$를 낮게 편향시켰을 것이다. [[04-robotics/system-identification|5.5 시스템 식별 §5]]의 변수 오차 경우다.

**흙은 패스가 끝난 뒤에 바뀐다.** 추정은 시험 패스가 깎은 흙을 기술한다. Egli 등(2022)은 초록을 그 어려움으로 연다. 흙은 잘 예측되지 않고, 한 번 퍼 올리는 도중에도 바뀔 수 있다. 깊이 1미터의 트렌치는 지층 하나를 가로지를 수 있고, 식별된 제어기는 누군가 다시 식별할 때까지 옛 숫자를 쓴다. 변하는 흙을 따라가는 것은 지도 문제다. Wagner 등(2025)은 시뮬레이션 속 소형 궤도 로더의 블레이드 자세와 힘에서, 토공 기본 방정식 위에 세운 물리 주입 신경망(physics infused neural network)으로 토질과 그 불확실성을 추정하고, 추정값을 베이즈 방식으로 갱신되는 지도의 층으로 보관한다. 모두 시뮬레이션 안의 일이고, §3의 1단이다. 식별 단계가 아예 필요 없는 대안은 스스로 적응하는 정책, §8이다.

### 8. 잔차 정책과 적응형 정책

*한 문장으로:* 잔차는 시뮬레이터의 제어기를 두고 한계가 있는 보정을 학습하는데, S2에서 그 한계는 고저 안전과 도달 범위를 맞바꾸는 랜덤화 범위의 변장이다. 적응형 정책은 그런 한계가 필요 없지만, 반응하는 신호가 기계에 있어야 한다.

잔차는 §2의 "모델 기반 제어기를 유지하고 보정을 학습한다"를 짓는 방법이다. Silver 등(2018)과 Johannink 등(2018)은 둘 다 기존 제어기의 출력에 학습한 보정을 더하고, 뒤의 논문은 최종 정책을 두 제어 신호의 중첩으로 기술한다. 아래 정의의 한계는 이 페이지가 더한 것으로, §2가 안전이 달려 있다고 말한 조건이다.

> **잔차 정책의 정의.** **잔차 정책**(residual policy)은 *제어기 구조*다. 고정된 기본 제어기에 학습한 보정을 그 출력에 더한 것이다. 처음부터 학습한 정책도, 이득을 다시 튜닝한 기본 제어기도 아니다. 정의 조건 셋과, 이 페이지의 안전 논증에 필요한 넷째. 혼자서도 과제를 그럭저럭 해내는 **기본 제어기** $u_0(s)$. 그 **출력에 더해지는 학습 보정** $r_\phi(s)$, 그래서 명령은 둘의 합이다. **보정만 학습한다**. 기본 제어기는 고정이다. 그리고 안전을 위해, 보정에 대한 **한계** $B$, 그래서 명령이 기본 제어기의 명령 둘레의 띠를 벗어나지 않는다.
>
> $$u(s)=u_0(s)+\operatorname{clip}\big(r_\phi(s),\,-B,\,B\big)$$
>
> $s$는 제어기가 관측하는 것, $u_0$는 기본 명령, $r_\phi$는 학습 파라미터 $\phi$를 가진 보정, $B$는 한계다. 그래서 신경망이 무엇을 내놓든, 명령은 행동을 아는 제어기에서 $B$ 안에 머문다.
>
> - **예**: $u_0=F_b=3.6\,\mathrm{kN}$, $B=1.2\,\mathrm{kN}$인 S2. 명령은 $[2.4,\ 4.8]\,\mathrm{kN}$ 안에 머물고, 이는 $2.4/0.06=40$에서 $4.8/0.06=80\,\mathrm{kPa}$까지 모든 흙에서 계획한 두께를 깎는다.
> - **비예**: $u_0$를 입력으로 받아 명령 자체를 내놓는 신경망. $u_0$를 쓰는 법을 배울 수는 있지만 $u_0$ 곁에 붙잡아 두는 것이 없으므로, 기본 제어기의 알려진 행동은 그것에 대해 아무것도 보장하지 않는다.
> - **왜 중요한가**: 한계는 두 가지 일을 한꺼번에 한다. 틀린 잔차가 기계를 얼마나 멀리 데려갈 수 있는지와, 잔차가 애초에 어느 흙을 맡을 수 있는지를 정한다. 그래서 숫자 하나가 안전과 포함률을 맞바꾼다.

**한계는 범위다.** 한계 $B$인 잔차는 힘을 $[F_b-B,\ F_b+B]$ 어디에나 놓을 수 있으므로, $(F_b-B)/(w\,d_0)$부터 $(F_b+B)/(w\,d_0)$까지의 모든 흙에서 계획한 두께를 깎는다. $B=1.2\,\mathrm{kN}$이면 $[40,\ 80]\,\mathrm{kPa}$로, §6의 적응형 제어기의 범위와 정확히 같고, S2에서 둘은 모든 흙에서 같은 두께를 깎는다. 그래서 §9의 표가 둘 모두에 쓰인다.

**한계는 안전 여유이기도 하다.** 신경망이 무엇을 내놓든 힘은 기본 제어기의 힘에서 $B$ 안에 머물므로, 두께는 기본 제어기의 두께에서 $B/(k_c\,w)$ 안에 머문다. 시뮬레이터의 $60\,\mathrm{kPa}$에서 완전히 틀린 잔차는 계획보다 $1.2/(60\times0.6)=0.033\,\mathrm{m}$, $33\,\mathrm{mm}$ 더 깊이 밀고, 이것이 마지막 패스라면 $\pm30\,\mathrm{mm}$ 띠를 벗어난다. 거기서 완전히 틀린 잔차마저 띠 안에 두려면 $B\le0.03\times60\times0.6=1.08\,\mathrm{kN}$이어야 하는데, 이 한계는 $[42,\ 78]\,\mathrm{kPa}$에만 닿는다. 현장의 $82.3\%$가 아니라 $77.6\%$다. 숫자 하나가 안전과 도달 범위를 맞바꾼다. clip은 [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §4]]가 안전 집합으로의 사영으로 쓰는 종류의 안전 필터이고, 여기서 안전 집합은 구간 $[F_b-B,\ F_b+B]$다.

**적응형 정책.** 다른 길은 흙을 감지해 반응하는 정책이고, 식별 단계가 필요 없다. 그 값은 관측 가능성이다. 반응하는 신호가 배치 주기로 기계에 있어야 한다. Egli 등의 토질 적응 제어기가 12톤 굴착기 위의 이 설계다. 순방향 신경망이고, 관측 27개에 팔 관절 토크 넷과 자기 직전 속도 명령이 들어 있으며, 에피소드마다 한 번 뽑은 흙으로 학습했고, 기계에서는 토크를 실린더 압력으로 추정한다. §1의 묻힌 화강암 덩어리에는 한 번의 굴착 안에서 반응했다. §6의 S2 모델은 그보다 거칠어서 직전 패스로 추정하므로, 지층이 바뀌는 곳에서 정확히 한 패스를 잃는다. $60$에서 $75\,\mathrm{kPa}$로 들어가면 첫 패스는 $3.6/(75\times0.6)=0.080\,\mathrm{m}$를 깎고 다음 패스는 계획한 $0.1$을 깎는다. 반면 윗층에서 한 번 식별한 제어기는 그 아래 모든 패스에서 $0.080\,\mathrm{m}$를 깎는다.

**S2 위의 privileged 증류.** 시뮬레이션에서 $k_c$를 보는 교사와 압력과 관절 각도만 보는 학생은 한 단계 떨어진 같은 거래다. 학생이 적응형 정책의 행동을 배울 수 있는 것은 한 패스의 힘과 두께가 $k_c=F_c/(w\,d)$를 정하기 때문이다. 학생이 교사가 받은 것을 추론하는 법은 [[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]]에 있다.

### 대상으로 한 번 끝까지 · Worked case

$80\,\mathrm{kPa}$ 현장의 S2를 다섯 단계로. 1–2단계는 이 페이지의 대상만 있으면 되고, 3–5단계는 §6–§8을 쓴다. §9의 랩이 표본 숫자를 다시 낸다.

**1단계 — 숫자로 만든 격차.** 제어기는 $F_b=k_{\text{sim}}\,w\,d_0=60\times0.6\times0.1=3.6\,\mathrm{kN}$을 민다. 현장에서 그 힘이 깎는 두께는

$$d=\frac{F_b}{k_{\text{site}}\,w}=\frac{3.6}{80\times0.6}=0.075\,\mathrm{m},$$

이다. 대상의 법칙 $F_c=k_c\,w\,d$를 $d$에 대해 풀면 이것이 나오기 때문이다. 그래서 패스마다 $\rho=0.075/0.100=0.75$, $\Delta J=25\,\mathrm{mm}$다. $0.1\,\mathrm{m}$를 붙잡는 위치 제어기라면 대신 $80\times0.6\times0.1=4.8\,\mathrm{kN}$이 필요하다. 시뮬레이터가 한 번도 요구하지 않은 3분의 1만큼 큰 힘이다. 같은 격차가 두께에서 힘으로 옮겨 갔을 뿐이다.

**2단계 — 트렌치가 치르는 값.** 계획한 패스는 버킷을 $k_f=0.85$까지 채우고, 이는 땅속에 있던 상태로 $V_b\,k_f/s=0.14\times0.85/1.25=0.0952\,\mathrm{m^3}$의 흙이다. S2의 부피 증가율 $s$가 버킷 안의 흐트러진 부피를 자연 상태 부피로 되돌리기 때문이다. 같은 끌기에서 $0.075\,\mathrm{m}$ 두께는 그 4분의 3을 모은다. 채움 $0.85\times0.75=0.6375$, 사이클당 $0.0714\,\mathrm{m^3}$다. $T_c=16\,\mathrm{s}$이면 시뮬레이션에서 $0.0952\times3600/16=21.42\,\mathrm{m^3/h}$, 현장에서 $0.0714\times3600/16=16.07\,\mathrm{m^3/h}$다. 트렌치의 $20\times0.6\times1.0=12\,\mathrm{m^3}$는 시뮬레이션에서 사이클 $12/21.42\,\mathrm{h}=33.6\,\mathrm{min}$, 현장에서 $12/16.07\,\mathrm{h}=44.8\,\mathrm{min}$이 걸린다. 틀린 숫자 하나에 $11.2$분, 3분의 1이 더 든다. 둘 다 사이클 시간일 뿐이고, [[05-construction-robotics/site-engineering|2.5 §4]]가 분모에 더하는 준비와 리셋은 빠져 있다.

**3단계 — $[40,\ 80]\,\mathrm{kPa}$에서 랜덤화하기.** 이 범위는 S2 현장의 $\Phi(1.151)-\Phi(-1.622)=0.823$을 덮고(§6), $80\,\mathrm{kPa}$은 그 단단한 쪽 끝에 있다. 적응형 제어기는 거기서 $80\times0.06=4.8\,\mathrm{kN}$을 밀어 $0.100\,\mathrm{m}$를 다 깎는다. 같은 범위에서 안전하게 만든 블라인드 제어기는 $40\times0.06=2.4\,\mathrm{kN}$을 밀어 $2.4/(80\times0.6)=0.050\,\mathrm{m}$를 깎는다. 랜덤화를 아예 안 한 것보다 나쁘고, $60\,\mathrm{kPa}$에서조차 $0.067\,\mathrm{m}$만 깎는다.

**4단계 — 패스 네 번으로 식별하기.** $95\%$로 $\hat k_c=80\pm1.96\times5/\sqrt4=80\pm4.9\,\mathrm{kPa}$다(§7). $F=\hat k_c\,w\,d_0=4.8\pm0.29\,\mathrm{kN}$으로 두면 $d=d_0\,\hat k_c/80=0.100\pm0.0061\,\mathrm{m}$를 깎는다. 네 번의 패스는 3단의 기계 시간이고, 추정은 이 구간 흙의 스냅숏이다.

**5단계 — 잔차에 한계 두기.** $B=1.2\,\mathrm{kN}$은 정확히 $80\,\mathrm{kPa}$까지 닿는다. $\Delta F=+1.2$가 $4.8\,\mathrm{kN}$과 $0.100\,\mathrm{m}$ 전부를 준다. 하지만 완전히 틀린 잔차가 $60\,\mathrm{kPa}$에서 $33\,\mathrm{mm}$ 과굴착하게 둔다(§8). 고저에 안전한 $B=1.08\,\mathrm{kN}$은 $78\,\mathrm{kPa}$까지 닿으므로 여기서는 $4.68\,\mathrm{kN}$을 밀어 $4.68/(80\times0.6)=0.0975\,\mathrm{m}$, $2.5\,\mathrm{mm}$ 모자라게 깎고, 그 도달 범위 $[42,\ 78]$은 현장의 $77.6\%$를 덮는다.

| 80 kPa 현장의 제어기 | 힘 (kN) | 두께 (m) | 패스당 흙, 계획 대비 | 트렌치 사이클 (분) | 필요했던 것 |
|---|---:|---:|---:|---:|---|
| 고정, 60 kPa에 맞춤 | 3.60 | 0.0750 | 0.750 | 44.8 | 없음 |
| 블라인드, 40–80 kPa에서 안전하게 | 2.40 | 0.0500 | 0.500 | 67.2 | 운용 중에는 없음 |
| 적응형, 40–80 kPa에서 학습 | 4.80 | 0.1000 | 1.000 | 33.6 | 기계에서 관측하는 힘 |
| 패스 네 번으로 식별 | 4.80 ± 0.29 | 0.1000 ± 0.0061 | 1.00 ± 0.06 | 33.6 | 감독된 패스 네 번 |
| 잔차, B = 1.08 kN | 4.68 | 0.0975 | 0.975 | 34.5 | 고저에 맞춰 고른 한계 |

**여기서 얻는 독법.** 격차를 닫은 처방은 저마다 다른 것으로 값을 치렀다. 적응형 제어기는 기계에 있어야 할 센서로, 식별은 답이 낡아 가는 감독된 패스로, 잔차는 고저 안전과 도달 범위를 맞바꾸는 한계로. 블라인드 제어기는 격차를 아예 닫지 않았다. 격차를 과굴착에 대한 보장과 바꿨고, 이 현장에서 그 거래는 매 패스의 절반을 대가로 치렀다.

### 9. 랩: 표본으로 뽑은 현장 위에서 랜덤화 범위 훑기

모든 것은 이 페이지의 대상에 고정되어 있다. 영어 절의 코드는 현장 분포에서 현장 200,000곳을 뽑고, 학습 범위 일곱 개마다 포함률(정확값, 그다음 표본값)을 찍고, 블라인드 제어기와 적응형 제어기 각각에 대해 계획 대비 패스당 흙(산적 버킷이 $1/k_f$에서 막는다), 4분의 1 이상 모자라게 깎이는 현장의 몫, $30\,\mathrm{mm}$ 넘게 과굴착하는 현장의 몫을 찍는다. 둘째 루프는 $80\,\mathrm{kPa}$ 현장에서 시험 패스 $n$번을 20,000번 되풀이해 $\hat k_c$의 퍼짐을 §7의 공식과 비교한다. NumPy와 표준 라이브러리만 쓰고, 1–2초면 돈다.

범위 훑기. "포함률"은 §6의 공식이고 괄호 안이 표본에서 센 몫이다. "패스당"은 계획 대비 패스당 흙, "부족"은 4분의 1 이상 모자라게 깎이는 현장의 몫, "과굴착"은 $30\,\mathrm{mm}$ 넘게 깊이 깎이는 현장의 몫이다.

| 범위 (kPa) | 포함률 | 블라인드: 패스당 | 부족 | 과굴착 | 적응형: 패스당 | 부족 | 과굴착 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 60–60 | 0.000 (0.000) | 0.979 | 0.124 | 0.148 | 0.979 | 0.124 | 0.148 |
| 50–70 | 0.498 (0.498) | 0.847 | 0.337 | 0.038 | 0.990 | 0.039 | 0.038 |
| 42–78 | 0.776 (0.776) | 0.720 | 0.609 | 0.007 | 0.990 | 0.014 | 0.007 |
| 40–80 | 0.823 (0.823) | 0.687 | 0.681 | 0.004 | 0.991 | 0.011 | 0.004 |
| 40–90 | 0.895 (0.895) | 0.687 | 0.681 | 0.004 | 1.000 | 0.003 | 0.004 |
| 35–100 | 0.964 (0.964) | 0.602 | 0.842 | 0.001 | 1.000 | 0.001 | 0.001 |
| 30–120 | 0.994 (0.994) | 0.516 | 0.948 | 0.000 | 1.000 | 0.000 | 0.000 |

$80\,\mathrm{kPa}$ 현장의 시험 패스:

| 패스 $n$ | $\hat k_c$의 표준편차, 표본 (kPa) | §7의 공식 (kPa) | 두께의 95%가 드는 폭 |
|---:|---:|---:|---:|
| 1 | 5.01 | 5.00 | 12.2 mm |
| 4 | 2.49 | 2.50 | 6.1 mm |
| 16 | 1.24 | 1.25 | 3.1 mm |
| 25 | 1.01 | 1.00 | 2.5 mm |

다섯 가지 읽기이고, 저마다 시험하는 주장을 달았다.

**포함률 공식이 성립한다**(§6의 정의를 시험). 모든 행에서 정확값과 표본값이 셋째 자리까지 맞고, 랜덤화하지 않은 행은 아무것도 덮지 않는다. 학습 값 하나는 범위가 아니다.

**블라인드 정책은 무른 쪽 끝의 값만 치른다**(§6의 유도를 시험). $[40,\ 80]$과 $[40,\ 90]$ 행이 똑같다. 그 힘에는 $k_{lo}$만 들어가기 때문이다. 패스당 흙은 $k_{lo}$와 함께 $0.847$에서 $0.516$으로 떨어진다. $[40,\ 80]$에서는 과굴착 $0.4\%$를 막는 대가로 현장의 $68.1\%$에서 4분의 1 이상 모자라다.

**적응형 정책은 덮이는 곳이면 계획을 지킨다**(§6과 §8을 시험). 패스당 흙이 $0.990$–$1.000$이고, 놓치는 것은 덮이지 않은 꼬리, $[40,\ 80]$에서 부족 $1.1\%$다. $[42,\ 78]$ 행은 모든 흙에서 같은 두께를 깎는 §8의 고저 안전 잔차이기도 하다. 포함률 $77.6\%$, 부족 $1.4\%$다.

**평균은 꼬리를 숨긴다**(§1의 비대칭을 시험). 랜덤화하지 않은 제어기의 $0.979$는 $2\%$ 손실처럼 보이지만, 4분의 1 모자란 현장 $12.4\%$와 $30\,\mathrm{mm}$ 넘게 과굴착하는 현장 $14.8\%$를 평균한 것이다.

**식별은 패스 수의 제곱근에 반비례해 나아진다**(§7을 시험). 모든 행에서 표본 퍼짐이 $\sigma_F/(w\,d_0\sqrt n)$와 맞고, 네 번의 패스면 뒤따르는 두께의 $95\%$가 $6.1\,\mathrm{mm}$ 안에 들며, 오차를 절반으로 줄이려면 패스가 네 배 든다.

### 읽고 나면

- 동역학·접촉·센싱·과제·구현 격차를 구분한다.
- 시스템 식별, 도메인 랜덤화, privileged learning, 잔차, 실데이터 적응을 구별한다.
- 논문의 시뮬레이터 전용 정보와 실데이터 예산을 찾는다.
- 한 기계·한 토조를 넘어선 일반화를 지지할 증거를 말한다.
- 한 정책의 sim-to-real 격차를 숫자로 만들고, 그 부호가 어느 요구조건을 깨는지 말한다.
- 밝힌 실제 분포로 랜덤화 범위의 포함률을 계산하고, 블라인드 정책은 폭의 값을 치르는데 적응형 정책은 치르지 않는 이유를 말한다.
- 몇 번의 패스로 하는 식별의 크기를 정하고, 그것이 보지 못하는 것 — 한 두께에서 빠진 항, 그 뒤에 바뀌는 흙 — 을 말한다.
- 잔차에 한계를 두고 그 한계가 무엇을 맞바꾸는지 말한다.

### 스스로 점검

1. 병렬 환경을 100개에서 10,000개로 늘려 시뮬레이션 성능이 좋아졌다. 실기계 결과는 왜
   전혀 나아지지 않을 수 있는가?
2. Egli RL은 실제 M545에 zero-shot으로 전이했다. "zero-shot"이 상류에서 무엇을
   지불했으며, 이 용어가 뜻하지 않는 것은?
3. 교사 정책은 지반 파라미터의 정답을 쓰고, 학생은 관절·압력 신호를 쓴다. 배치 주장을
   믿기 전에 가장 중요한 단일 확인 사항은?
4. ExACT와 ExT는 둘 다 굴착에 모방 학습을 적용한다. 두 주장은 왜 배치 사다리의 다른
   단에 있는가?
5. S2의 현장 전체에 걸쳐 평균하면 랜덤화하지 않은 제어기는 패스당 흙을 $2.1\%$만 잃는다. 이것이 왜 전이된다는 증거가 아닌가?
6. 트렌치가 중간 깊이에서 $60$에서 $75\,\mathrm{kPa}$ 흙으로 넘어간다. 윗층에서 한 번 식별한 제어기는 경계 아래에서 무엇을 깎고, $[40,\ 80]\,\mathrm{kPa}$에서 학습한 적응형 제어기는 무엇을 잃는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 병렬화는 샘플 생산량을 올릴 뿐 시뮬레이터 타당성을 올리지 않는다: 10,000개 환경이 같은 잘못된 유압·접촉·센싱 물리를 반복할 수 있다. 지배적 격차가 샘플 부족이 아니라 모델링 오류라면, 더 많은 샘플은 잘못된 최적점에 더 세게 수렴한다.
> 2. 상류에서는 신경망 밸브/액추에이터 모델을 맞추기 위한 실기계 데이터와 엔지니어링 — 실제 시스템 지식을 시뮬레이터에 구워 넣은 것 — 을 지불했다. "Zero-shot"은 배치 전 목표 도메인 학습 업데이트가 없다는 뜻이지, 시뮬레이터를 실데이터 없이 만들었다거나 식별된 기계·운용 범위 너머로 전이가 유지된다는 뜻이 아니다.
> 3. 학생이 소비하는 모든 관측이 실기계에서 배치 주기와 지연으로 실제로 존재하는지 — 그리고 그 신호의 현실적 노이즈 아래에서 증류가 평가되었는지. Privileged learning은 시험 시점 관측 가능성이 조용히 낙관적일 때 소리 없이 실패한다.
> 4. ExACT는 시뮬레이션 검증뿐이라 증거가 1단(시뮬레이터 평가)에서 멈춘다; ExT는 실기계에서 센티미터급 전이를 보고해 감독 실기 시험 단까지 도달한다. 같은 방법 계열, 다른 증거 무게 — 주장을 정하는 것은 방법 이름이 아니라 사다리다.
> 5. 평균은 부호가 반대인 두 실패를 섞는다. 무른 현장은 버킷이 막는 데까지 과굴착하고 단단한 현장은 모자라게 깎아서, 평균에서 서로 일부 상쇄된다. 현장별로 보면 $12.4\%$는 4분의 1 이상 모자라고 $14.8\%$는 $30\,\mathrm{mm}$ 넘게 과굴착한다. 마지막 패스라면 고저 실패다(§6, §9). 전이 주장은 현장에 관한 것이므로 평균이 아니라 꼬리를 보고하라.
> 6. 식별한 제어기는 $\hat k_c=60$과 $3.6\,\mathrm{kN}$을 그대로 쓰므로, 경계 아래에서는 누군가 다시 식별할 때까지 모든 패스에서 $3.6/(75\times0.6)=0.080\,\mathrm{m}$, 5분의 1 모자라게 깎는다. 적응형 제어기의 범위는 $75\,\mathrm{kPa}$를 덮으므로, 이 페이지의 모델에서는 경계 아래 첫 패스 하나를 $0.080\,\mathrm{m}$로 잃고 그다음부터 계획한 $0.1\,\mathrm{m}$를 깎는다. Egli 등의 것처럼 패스 안에서 반응하는 제어기는 그보다 덜 잃는다(§8).

### 과제 · Problem set

Tier A. $80\,\mathrm{kPa}$ 현장과 그 이웃의 S2이고, 뒤에 [[04-robotics/system-identification|5.5 시스템 식별]]과 [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL]]이 있다. 랩은 현장과 패스를 표본으로 뽑고, 시뮬레이터는 없다.

1. **그리기.** §8의 고저 안전 잔차 $B=1.08\,\mathrm{kN}$에 대한 위의 그림. 그 도달 범위를 칠한 띠로, 그 두께 곡선, 힘을 고정한 곡선, 계획 두께 선과 $30\,\mathrm{mm}$ 선, 그리고 새 포함률과 양쪽 꼬리를 적은 현장 띠. 잔차 아래에서 $80\,\mathrm{kPa}$ 현장이 깎는 두께를 표시한다.
2. **유도.** 더 무른 현장, $k_c=45\,\mathrm{kPa}$, 나머지는 이 페이지의 대상과 같다. (a) 힘을 고정한 제어기의 두께와 과굴착: 마지막 패스라면 $\pm30\,\mathrm{mm}$ 고저를 깨는가, 그리고 트렌치 중간의 패스를 산적 버킷이 담는가? (b) $[40,\ 80]$에서 안전하게 만든 블라인드 제어기의 두께. (c) 더 좁은 $[50,\ 70]$에서 학습한 적응형 제어기의 힘과 두께. (d) $95\%$로 $k_c$를 $\pm4.5\,\mathrm{kPa}$ 안에 알려면 필요한 시험 패스 수. (e) $45\,\mathrm{kPa}$에 닿는 가장 작은 잔차 한계, 그리고 그것이 $60\,\mathrm{kPa}$에서 고저에 안전한가. (f) 독립으로 랜덤화한 파라미터 여섯: 결합 포함률 $90\%$를 주는 파라미터별 포함률은 얼마이고, 파라미터 열 개를 각각 $90\%$로 덮으면 결합 포함률은 얼마인가?
3. **실행.** 흙에 §7의 오프셋 $F_{\text{off}}=0.6\,\mathrm{kN}$이 있고, 파라미터 하나짜리 모델에는 그것이 없다. 영어 절 템플릿의 `?`를 채워, 스크립트가 여덟 번의 시험 패스 — 모두 $0.1\,\mathrm{m}$, 또는 $0.05$와 $0.1\,\mathrm{m}$를 번갈아 — 에 두 모델을 맞추고, 각 맞춤을 떼어 둔 $0.05\,\mathrm{m}$ 층으로 채점하는 일을 2,000번 되풀이하게 하라. 설계마다 랭크, $k_c$의 두 추정과 그 퍼짐, 떼어 둔 층의 오차를 보고한다. 어느 맞춤이 자기 기록 위에서는 검증되는데 떼어 둔 층에서는 실패하는가? 어느 설계와 모델이 $k_c$를 되찾고, 둘째 파라미터는 무엇을 대가로 치렀는가?
4. **해석.** 어떤 논문이 매개변수 열두 개를 "넓은 범위로" 무작위화하고 제로샷 전이를 보고한다. 그 범위를 넓다고 부르려면 실제 매개변수에 대해 무엇을 보여야 하는가? 범위마다 실제 주변 분포의 $95\%$를 덮고 열둘이 독립이라면 결합 포함률은 얼마이고, "zero-shot"은 무엇을 말하지 않고 남겨 두는가?

> [!note]- 그리는 법 · How to draw it
> - **띠**를 $42$에서 $78\,\mathrm{kPa}$까지 그리고, 잔차의 도달 범위 $F=3.6\pm1.08\,\mathrm{kN}$이라 적는다. 그림의 $40$–$80$보다 양쪽 끝에서 $2\,\mathrm{kPa}$씩 좁다.
> - **잔차의 두께 곡선**: 띠 전체에서 $0.100\,\mathrm{m}$로 평평하다. 띠 밖에서는 힘이 $2.52$ 또는 $4.68\,\mathrm{kN}$에서 잘리므로, 무른 쪽은 $0.1\times42/k_c$($30\,\mathrm{kPa}$에서 $0.140\,\mathrm{m}$), 단단한 쪽은 $0.1\times78/k_c$($80$에서 $0.0975$, $100$에서 $0.078$, $120\,\mathrm{kPa}$에서 $0.065\,\mathrm{m}$)다.
> - **힘을 고정한 곡선은 그대로**, $d=3.6/(0.6\,k_c)$로 $60$에서 $0.100$, $80\,\mathrm{kPa}$에서 $0.075$를 지나고, 가로선 둘은 $0.10$과 $0.13\,\mathrm{m}$에 긋는다.
> - **$80\,\mathrm{kPa}$의 표시**: $0.0975\,\mathrm{m}$, 계획 선 바로 아래에 $2.5\,\mathrm{mm}$ 부족이라 적는다.
> - **현장 띠**: 같은 로그정규를 $42$에서 $78$까지 칠하고, 안 $77.6\%$, 더 무름 $7.7\%$, 더 단단함 $14.7\%$를 적는다.
> - 띠를 확률로 가운데에 놓으면 틀린 그림이다. 분포가 $k_c$가 아니라 $\ln k_c$에서 대칭이라, 단단한 쪽 꼬리가 여전히 무른 쪽의 두 배쯤 된다.

> [!tip]- 정답 · Solutions
> 1. 그리는 법 목록과 같다. 띠 $[42,\ 78]\,\mathrm{kPa}$, 잔차 두께는 안에서 $0.100\,\mathrm{m}$, 밖에서 $0.1\times42/k_c$와 $0.1\times78/k_c$, $80\,\mathrm{kPa}$에서 $0.0975\,\mathrm{m}$, 현장 띠는 안 $77.6\%$, 더 무름 $7.7\%$, 더 단단함 $14.7\%$.
> 2. (a) $d=3.6/(45\times0.6)=0.133\,\mathrm{m}$, $33\,\mathrm{mm}$ 과굴착으로 마지막 패스라면 $\pm30\,\mathrm{mm}$ 띠를 벗어난다. 트렌치 중간에서 채움은 산적 용량의 $0.85\times0.133/0.1=1.13$이 되려 하므로 버킷이 넘친다. 계획 패스의 $1/0.85=1.18$배까지만 담고, 계획 패스의 나머지 $0.16$은 흘러넘친다. (b) $2.4/(45\times0.6)=0.089\,\mathrm{m}$, $11\,\mathrm{mm}$ 부족. (c) $45<50$이므로 $50\times0.06=3.0\,\mathrm{kN}$을 밀어 $3.0/(45\times0.6)=0.111\,\mathrm{m}$, $11\,\mathrm{mm}$ 과굴착으로 띠 안이다. (d) 패스당 표준편차는 흙과 상관없이 $5\,\mathrm{kPa}$이므로 $n\ge(1.96\times5/4.5)^2=4.74$, 곧 다섯 번. (e) 잔차가 $45\times0.06-3.6=-0.9\,\mathrm{kN}$을 내야 하므로 $B\ge0.9\,\mathrm{kN}$이다. $60\,\mathrm{kPa}$에서 완전히 틀리면 $0.1\times0.9/3.6=25\,\mathrm{mm}$ 과굴착으로 띠 안이니 고저에 안전하다. (f) $p^6=0.9$에서 $p=0.9^{1/6}=0.983$. 모든 범위가 실제 주변 분포의 $98.3\%$를 덮어야 한다. 그리고 $0.9^{10}=0.349$. 주변 분포를 넉넉히 덮어도 매개변수를 더할수록 결합 포함률은 깎인다.
> 3. 빈칸은 `(a @ F) / (a @ a)`, `np.linalg.lstsq(A, F, rcond=None)[0]`, `kh * w * 0.05 + oh`이고, 채운 스크립트는 영어 절 정답에 있다. 한 두께 설계는 랭크 $1$이고, 파라미터 하나짜리 맞춤이 $89.9\pm1.8\,\mathrm{kPa}$로 떼어 둔 층을 $-6.3\pm1.1\,\mathrm{mm}$ 놓치며, 둘짜리 맞춤은 $0.3\,\mathrm{kPa}$로 떼어 둔 층을 $+49.7\pm2.2\,\mathrm{mm}$ 벗어난다. 두 두께 설계는 랭크 $2$이고, 하나짜리 맞춤이 $92.0\pm2.2\,\mathrm{kPa}$로 $-5.0\pm1.4\,\mathrm{mm}$, 둘짜리 맞춤이 $80.0\pm6.9\,\mathrm{kPa}$로 $-0.0\pm3.0\,\mathrm{mm}$다. 자기 기록 위에서 검증되는 것은 한 두께의 하나짜리 맞춤이다. $k_c+F_{\text{off}}/(w\,d_0)=80+10=90\,\mathrm{kPa}$를 내놓아 $0.1\,\mathrm{m}$에서는 정확히 맞는데, $0.05\,\mathrm{m}$ 층은 평균 $6.25\,\mathrm{mm}$ 놓친다. 한 두께의 둘짜리 맞춤은 랭크가 모자라고, `lstsq`는 최소 노름 나눔을 돌려주어 힘을 거의 모두 오프셋에 넣고 경고 없이 떼어 둔 층을 약 $50\,\mathrm{mm}$ 과굴착한다. 그래서 랭크를 찍는다. 두께를 하나 더해도 틀린 모델은 구해지지 않는다. 하나짜리 맞춤은 그때 $80+0.6\times\sum a_i/\sum a_i^2=92\,\mathrm{kPa}$를 읽는다. 두께 둘에 파라미터 둘만이 편향 없이 $k_c$를 되찾고, 대가는 정밀도다. 기울기의 퍼짐이 $\sigma_F/\sqrt{\sum(a_i-\bar a)^2}=0.3/\sqrt{8\times0.015^2}=7.1\,\mathrm{kPa}$(표본으로는 $6.9$)로, 편향된 한 두께 맞춤의 $1.8$보다 크다. 떼어 둔 층의 오차는 편향이 없고, 퍼짐이 공식으로 $3.1\,\mathrm{mm}$, 표본으로 $3.0$이다.
> 4. 실제 매개변수 분포와 그 상관의 측정이나 믿을 만한 추정. 포함률은 결합 분포의 성질이기 때문이다. 잰 것에 비해 "넓다"는 주장이지만, "넓다"만으로는 아니다. 각각 $95\%$에 독립이면 결합 포함률은 $0.95^{12}=0.540$이어서, 실제 조건의 거의 절반이 상자 밖에 떨어진다. "zero-shot"은 학습된 파라미터가 고정되었다는 것만 말한다(§3). 어떤 실데이터가 시뮬레이터를 만들었는지, 정책이 온라인으로 무엇을 적응하는지는 말하지 않는다.

### 출처

- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — 어느 시뮬레이터가 실제로 지형과 접촉을 모델링하는가, 그리고 각각이 무엇을 빠뜨리는가.
- [Tobin et al., Domain Randomization](https://arxiv.org/abs/1703.06907)
- [Peng et al., Dynamics Randomization](https://arxiv.org/abs/1710.06537)
- [Lee et al., challenging-terrain locomotion](https://www.science.org/doi/10.1126/scirobotics.abc5986)
- P. Egli, D. Gaschen, S. Kerscher, D. Jud, M. Hutter, "Soil-Adaptive Excavation Using Reinforcement Learning," *IEEE Robotics and Automation Letters* 7(4), 2022, [DOI 10.1109/LRA.2022.3189834](https://doi.org/10.1109/LRA.2022.3189834). 게재 확정본은 [ETH Research Collection](https://www.research-collection.ethz.ch/server/api/core/bitstreams/95ef5691-11e8-4a86-b02d-6f0e2501de9b/content)에서 공개 — 표 I의 랜덤화한 토질 파라미터, 토크 관측과 그것을 뺀 비교 실험, 묻은 화강암 덩어리, §4의 버킷 채움 단서.
- T. Silver, K. Allen, J. Tenenbaum, L. Kaelbling, "Residual Policy Learning," [arXiv:1812.06298](https://arxiv.org/abs/1812.06298), 2018 — 초기 제어기 위에 학습한 잔차.
- T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, S. Levine, "Residual Reinforcement Learning for Robot Control," [arXiv:1812.03201](https://arxiv.org/abs/1812.03201), 2018 — 기존 제어기의 신호와 RL 잔차의 중첩으로서의 최종 정책.
- W. J. Wagner, A. Soylemezoglu, K. Driggs-Campbell, "In-Situ Soil-Property Estimation and Bayesian Mapping with a Simulated Compact Track Loader," [arXiv:2507.22356](https://arxiv.org/abs/2507.22356), 2025 — 블레이드 자세와 힘에서 추정해 베이즈 방식으로 지도에 올린 토질, 시뮬레이션(Vortex Studio)에서.
- L. Werner, P. Eyschen, S. Costello, P. Micarelli, A. Cramariuc, M. Hutter, "Size Doesn't Matter: Material-State Reinforcement Learning for Excavator Transferable Soil Manipulation," [arXiv:2609.12677](https://arxiv.org/abs/2609.12677), 2026 — 보정된 기계 인터페이스를 거쳐 11.5톤 굴착기와 500그램 탁상 로봇에 쓴 같은 학습 가중치.
- 이 페이지의 교과 숫자는 모두 S2와 이 페이지의 고정값에서 NumPy 2.0.2로 여기서 계산했다. 현장과 패스는 표본으로 뽑은 것이지 잰 것이 아니다.
