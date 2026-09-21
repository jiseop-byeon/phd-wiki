---
title: 11. Human–Robot Interaction & Safety
tags: [robotics, hri, safety, construction]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
wiki-support: Working
---

## English

*Group G, and the only page in it. Stands on [[04-robotics/robot-systems-deployment|10. Robot Systems]] and [[02-foundations/ml-practice|ML Practice]].
The point where a success rate stops being a sufficient answer, because someone is standing next to the machine.*

When people operate, supervise, share space with, or depend on a robot, task success alone is not enough. Human–robot interaction studies authority, information, workload, trust, and performance; safety analysis asks which hazards can cause harm and how risk is reduced.

> [!info] Depth target
> Read HRI and safety claims — autonomy level, intervention, trust, hazard/risk — precisely, and audit human-study designs. Running human studies requires dedicated methods training beyond this page.

> [!warning] Scope
> This page is a literacy guide for reading research, not a certification or legal-compliance guide. Applicable laws and standards must be checked from current official sources for the specific machine, workplace, and jurisdiction.

> [!note] Prerequisites
> [[02-foundations/ml-practice|ML Practice & Evaluation]] · [[04-robotics/robot-systems-deployment|Robot Systems]] — §9 connects onward to [[05-construction-robotics/index|Construction Robotics]] (the next track, not a prerequisite).

> [!note] First pass · 처음이라면
> Read the running object and the worked case below — they are the one calculation this page owes you — then §1 and §2, where most confusion in this literature is one of these two spectra being collapsed, then §6 for the safety vocabulary, then §10, which works one interpretation end to end.

### Running object: the P2 safety cell

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the planar 2R arm, $L_1 = L_2 = 1$ m — carrying a tool, at the pose $\theta = (0^\circ, 90^\circ)$ where the tip sits at $(1,1)$ m and seats the tool on a panel. The arm stands in a cell that one operator may walk into while it works. The numbers below are the ones §6's example already uses, with the reaction time split one step finer so that the detector is visible as its own term.

| Symbol | Value | What it is |
|---|---:|---|
| $L_1, L_2$ | 1.00 m each | P2's link lengths, frozen in 0.6 |
| $L_t$ | 0.25 m | the tool, held along the forearm axis and extending that far beyond the tip — this page's only addition to P2 |
| $v_h$ | 1.6 m/s | the operator's approach speed, the standard walking speed of ISO 13855 |
| $v_r$ | 1.0 m/s | the robot's tip speed in the direction of the person |
| $T_{\text{sens}}$ | 0.06 s | detector latency: body enters the sensing field → the tracker reports it |
| $T_{\text{ctrl}}$ | 0.04 s | controller decision plus brake command |
| $T_r$ | 0.10 s | reaction time, $T_r = T_{\text{sens}} + T_{\text{ctrl}}$ |
| $T_s$ | 0.30 s | stopping time once braking starts |
| $C$ | 0.20 m | intrusion distance — how far a body part reaches into the field before it is detected at all |
| $Z_d$ | 0.10 m | operator position uncertainty of the presence-sensing device |
| $Z_r$ | 0.05 m | robot position uncertainty |

The tool matters because the hazard is the swept volume, not the base: with the arm outstretched the hazard reaches $R_h = L_1 + L_2 + L_t = 2.25$ m from the base, and every separation distance is measured from *that* boundary.

*Scope: this page teaches how to read an autonomy, trust or safety claim and how to size one safety function — speed and separation monitoring — on a named machine. It does not teach how to certify a machine (that is the standards themselves, named in §6), how to run a human study (that is [[06-research-practice/psychophysics-human-measurement|8. Psychophysics]] and [[06-research-practice/experimental-design-reproducibility|Experimental Design]]), or how the perception that feeds the separation function works ([[04-robotics/video-action-understanding|20. Video & Action Understanding]], [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]]).*

### Homework diagram: the cell in plan, with the clock underneath

Draw it once; the problem set asks for the same drawing at different numbers.

<svg viewBox="0 0 560 516" style="max-width:100%;height:auto" role="img" aria-label="Safety-cell homework diagram: P2 in plan with its tool, the dashed hazard circle of radius 2.25 m, the solid sensing-field circle at 3.49 m, the six terms of the 1.24 m separation distance laid end to end to scale along one approach line, and underneath the clock from the field boundary to the stop at 0.40 s">
  <text x="16" y="24" font-size="12" fill="currentColor" font-weight="600">plan view (m)</text>
  <path d="M521.1 294 A223.4 223.4 0 1 0 78.9 294" stroke="currentColor" stroke-width="1.8" fill="none"/>
  <path d="M440.4 294 A144 144 0 1 0 159.6 294" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="6 4"/>
  <line x1="300" y1="262" x2="364" y2="262" stroke="currentColor" stroke-width="4.0" stroke-linecap="round"/>
  <line x1="364" y1="262" x2="364" y2="198" stroke="currentColor" stroke-width="4.0" stroke-linecap="round"/>
  <line x1="364" y1="198" x2="364" y2="182" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
  <rect x="291" y="253" width="18" height="18" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.25"/>
  <circle cx="364" cy="262" r="4" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="1.0"/>
  <circle cx="364" cy="182" r="2.6" stroke="none" fill="currentColor"/>
  <text x="354" y="236" font-size="11" fill="currentColor" text-anchor="end">P2 at θ = (0°, 90°)</text>
  <text x="356" y="187" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">tool 0.25 m</text>
  <text x="300" y="148" font-size="11" fill="currentColor" text-anchor="middle">hazard boundary</text>
  <text x="300" y="163" font-size="11" fill="currentColor" text-anchor="middle">R<tspan dy="3.1" font-size="8.6">h</tspan><tspan dx="3.1" dy="-3.1">= 2.25 m</tspan></text>
  <text x="300" y="72.6" font-size="11" fill="currentColor" text-anchor="middle">sensing-field boundary</text>
  <text x="300" y="87.6" font-size="11" fill="currentColor" text-anchor="middle">R<tspan dy="3.1" font-size="8.6">h</tspan><tspan dx="3.1" dy="-3.1">+ S</tspan><tspan dy="3.1" font-size="8.6">p</tspan><tspan dx="3.1" dy="-3.1">= 3.49 m</tspan></text>
  <line x1="156" y1="262" x2="288" y2="262" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.5" stroke-dasharray="2 3"/>
  <rect x="76.6" y="258" width="6.4" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.07"/>
  <rect x="83" y="258" width="12.8" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.3"/>
  <rect x="95.8" y="258" width="41" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.15"/>
  <rect x="136.8" y="258" width="9.6" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.38"/>
  <rect x="146.4" y="258" width="6.4" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.22"/>
  <rect x="152.8" y="258" width="3.2" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.46"/>
  <circle cx="65.6" cy="242" r="4.6" stroke="currentColor" stroke-width="1.3" fill="none"/>
  <line x1="65.6" y1="247" x2="65.6" y2="259" stroke="currentColor" stroke-width="1.6"/>
  <line x1="65.6" y1="259" x2="60.6" y2="270" stroke="currentColor" stroke-width="1.6"/>
  <line x1="65.6" y1="259" x2="70.6" y2="270" stroke="currentColor" stroke-width="1.6"/>
  <line x1="59.6" y1="251" x2="71.6" y2="251" stroke="currentColor" stroke-width="1.6"/>
  <line x1="88.6" y1="236" x2="115.8" y2="236" stroke="currentColor" stroke-width="1.4"/>
  <path d="M120.6 236 L114.6 238.5 L114.6 233.5 Z" fill="currentColor" stroke="none"/>
  <text x="86.6" y="228" font-size="11" fill="currentColor">v<tspan dy="3.1" font-size="8.6">h</tspan><tspan dx="3.1" dy="-3.1">= 1.6 m/s</tspan></text>
  <text x="78.6" y="282" font-size="11" fill="currentColor" fill-opacity="0.85">× 6 below</text>
  <rect x="50" y="327" width="38.4" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.07"/>
  <text x="69.2" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.10</text>
  <text x="69.2" y="340" font-size="11" fill="currentColor" text-anchor="middle">Z<tspan dy="3.1" font-size="8.6">d</tspan></text>
  <rect x="88.4" y="327" width="76.8" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.3"/>
  <text x="126.8" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.20</text>
  <text x="126.8" y="340" font-size="11" fill="currentColor" text-anchor="middle">C</text>
  <rect x="165.2" y="327" width="245.8" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.15"/>
  <text x="288.1" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.64</text>
  <text x="288.1" y="340" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">h</tspan></text>
  <rect x="411" y="327" width="57.6" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.38"/>
  <text x="439.8" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.15</text>
  <text x="439.8" y="340" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">s</tspan></text>
  <rect x="468.6" y="327" width="38.4" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22"/>
  <text x="487.8" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.10</text>
  <text x="487.8" y="340" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">r</tspan></text>
  <rect x="507" y="327" width="19.2" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.46"/>
  <text x="516.6" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.05</text>
  <text x="516.6" y="340" font-size="11" fill="currentColor" text-anchor="middle">Z<tspan dy="3.1" font-size="8.6">r</tspan></text>
  <text x="50" y="322" font-size="11" fill="currentColor" fill-opacity="0.85">field boundary</text>
  <text x="526.2" y="322" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">hazard boundary</text>
  <text x="288.1" y="322" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">p</tspan><tspan dx="3.1" dy="-3.1">= 1.24 m</tspan></text>
  <text x="50" y="378" font-size="11" fill="currentColor">t = 0: the body crosses the field boundary</text>
  <rect x="50" y="384" width="400" height="13" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22"/>
  <text x="250" y="394" font-size="11" fill="currentColor" text-anchor="middle">person still walking, all 0.40 s</text>
  <line x1="50" y1="410" x2="490" y2="410" stroke="currentColor" stroke-width="1.2"/>
  <path d="M502 410 L496 412.5 L496 407.5 Z" fill="currentColor" stroke="none"/>
  <text x="506" y="414" font-size="11" fill="currentColor">t (s)</text>
  <line x1="50" y1="405" x2="50" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <line x1="110" y1="405" x2="110" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <line x1="150" y1="405" x2="150" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <line x1="450" y1="405" x2="450" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <text x="50" y="429" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="150" y1="416" x2="150" y2="425" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="1.5 2"/>
  <line x1="110" y1="416" x2="110" y2="443" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="1.5 2"/>
  <line x1="450" y1="416" x2="450" y2="425" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="1.5 2"/>
  <text x="153" y="435" font-size="11" fill="currentColor">T<tspan dy="3.1" font-size="8.6">r</tspan><tspan dx="3.1" dy="-3.1">= 0.10 s: brake command</tspan></text>
  <text x="450" y="435" font-size="11" fill="currentColor" text-anchor="middle">T<tspan dy="3.1" font-size="8.6">r</tspan><tspan dx="3.1" dy="-3.1">+ T</tspan><tspan dy="3.1" font-size="8.6">s</tspan><tspan dx="3.1" dy="-3.1">= 0.40 s: stopped</tspan></text>
  <text x="113" y="453" font-size="11" fill="currentColor">T<tspan dy="3.1" font-size="8.6">sens</tspan><tspan dx="3.1" dy="-3.1">= 0.06 s: tracker reports</tspan></text>
  <text x="16" y="484" font-size="11" fill="currentColor" fill-opacity="0.9">S<tspan dy="3.1" font-size="8.6">p</tspan><tspan dx="3.1" dy="-3.1">= 0.64 + 0.10 + 0.15 + 0.20 + 0.10 + 0.05 = 1.24 m, measured outward from the hazard boundary;</tspan></text>
  <text x="16" y="500" font-size="11" fill="currentColor" fill-opacity="0.9">S<tspan dy="3.1" font-size="8.6">h</tspan><tspan dy="-3.1">, the person walking, is 51.6% of it. The field starts at 3.49 m: 38.3 m² of floor for a 2.25 m reach.</tspan></text>
</svg>

**Top — the plan view.** P2's base at the origin. Link 1 along $+x$ to $(1,0)$, link 2 up to the tip at $(1,1)$, the tool beyond it. A dashed circle of radius $R_h = 2.25$ m around the base: the hazard boundary. A second, solid circle at $R_h + S_p$: the sensing-field boundary. One straight approach line running inward from the field boundary toward the arm, with the person on it walking at $v_h$. On that line, mark the six contributions end to end as segments, in the order a body actually spends them: $C$ first (the reach into the field before detection), then $S_h$ (how far the person travels while the robot reacts and stops), then $S_r$ and $S_s$ (the robot's own travel and stopping distance, measured from the hazard boundary outward), and $Z_d$, $Z_r$ at each end as the two uncertainty pads. The segments must be drawn to scale — that is the whole point of the drawing.

**Bottom — the clock, on the same horizontal axis.** $t = 0$ when the body crosses the field boundary. A tick at $T_{\text{sens}} = 0.06$ s where the tracker first reports the person; a tick at $T_r = 0.10$ s where the brake command leaves the controller; a tick at $T_r + T_s = 0.40$ s where motion has stopped. Above the clock, one bar showing the person still walking through all 0.40 s, because nothing the robot does shortens it.

### Worked case: the protective separation distance, term by term

> [!info] Definition · 정의 — protective separation distance $S_p$
> **What kind of thing it is.** A *distance in metres*: the smallest gap between the person and the robot's hazard boundary at which the robot is still allowed to keep moving. It is recomputed continuously as speeds change — it is not a fence radius and not a fixed trigger threshold.
>
> **Its defining conditions.** Three of them, and dropping any one makes the number meaningless. (i) It is a **sum of six contributions**, not a threshold anyone chooses. (ii) Each contribution must be an **over-estimate** of the quantity it stands for, because the sum is a bound and a bound built from best-case terms bounds nothing. (iii) It is measured **from the hazard boundary** — the swept volume of arm plus tool — not from the base, the tool tip, or the sensor.
>
> $$S_p = \underbrace{v_h\,(T_r + T_s)}_{S_h} + \underbrace{v_r\,T_r}_{S_r} + \underbrace{\tfrac{1}{2}\,v_r\,T_s}_{S_s} + C + Z_d + Z_r$$
>
> $S_h$ is how far the operator walks during the whole reaction-plus-stop interval at approach speed $v_h$; $S_r$ is how far the robot travels at $v_r$ during its reaction time $T_r$; $S_s$ is its stopping distance during $T_s$, which is $\tfrac{1}{2}v_r T_s$ under constant deceleration; $C$ is the intrusion distance; $Z_d$ and $Z_r$ are the position uncertainties of the operator measurement and of the robot. Detector latency does not appear as its own symbol — it is inside $T_r$, which is exactly why it is easy to lose.
>
> **Example.** The cell above: 1.24 m, derived term by term below.
>
> **Non-examples.** "The scanner stops the robot when someone is within 1 m" is not an $S_p$: a fixed trigger distance has no $T_r$, no $T_s$ and no $v_h$ in it, so it does not change when the robot speeds up or the detector slows down. "The field is set at 1.24 m from the robot's base" is not one either — the same number measured from the wrong origin leaves the person $2.25 - 1.24 = 1.01$ m *inside* the hazard boundary before the field even notices them.
>
> **Why it matters.** It is the one safety function whose cost is a *number of metres of floor*, so it turns every claim about faster perception, or about slowing a robot down, into a quantity you can check.

Now the cell. Substituting the frozen numbers, term by term, in metres:

$$S_h = 1.6\,(0.10 + 0.30) = 0.64,\quad S_r = 1.0 \times 0.10 = 0.10,\quad S_s = \tfrac{1}{2}(1.0)(0.30) = 0.15$$

so, adding the three uncertainty terms $C = 0.20$, $Z_d = 0.10$, $Z_r = 0.05$ unchanged:

$$S_p = 0.64 + 0.10 + 0.15 + 0.20 + 0.10 + 0.05 = 1.24\ \mathrm{m}$$

**Which term dominates.** As a share of the 1.24 m: $S_h$ 51.6%, $C$ 16.1%, $S_s$ 12.1%, $S_r$ 8.1%, $Z_d$ 8.1%, $Z_r$ 4.0%. Over half the budget is the human walking, and the robot's own two motion terms together are 20.2%. That ranking is the result; the sum is only its total.

**What the cell costs.** The sensing field must begin at $R_h + S_p = 2.25 + 1.24 = 3.49$ m from P2's base, so the monitored floor is $\pi (3.49)^2 = 38.3\ \mathrm{m}^2$ — for an arm whose own reach is 2.25 m.

**The three sensitivities, and the one that decides.** Differentiate the definition, holding the rest fixed:

$$\frac{\partial S_p}{\partial T_r} = v_h + v_r = 2.6\ \mathrm{m/s}, \qquad \frac{\partial S_p}{\partial v_r} = T_r + \tfrac{1}{2}T_s = 0.25\ \mathrm{s}, \qquad \frac{\partial S_p}{\partial v_h} = T_r + T_s = 0.40\ \mathrm{s}$$

Reaction time is charged twice — once to the person's approach through $S_h$ and once to the robot's own travel through $S_r$ — which is why it carries $v_h + v_r$ and the robot's speed does not. Put the numbers to work:

- A detector 0.1 s slower costs $2.6 \times 0.1 = 0.26$ m, so the field moves out to 3.75 m and the monitored floor grows to $\pi(3.75)^2 = 44.2\ \mathrm{m}^2$, about 5.9 m² more.
- Slowing the robot from 1.0 to 0.5 m/s saves $0.25 \times 0.5 = 0.125$ m: $S_p$ falls to 1.115 m.
- Stopping the robot dead, $v_r = 0$, still leaves $S_p = 0.99$ m. So the **entire** budget available from robot speed is $1.24 - 0.99 = 0.25$ m.

That last line is the whole lecture in one comparison: the robot's entire speed budget, $0.25$ m, is about what one tenth of a second of detector latency costs, $0.26$ m. The sensitivities are slopes at this cell, and $S_p$ contains the product $v_rT_r$, so settle the trade exactly: with the slower detector $T_r = 0.20$ s and $S_p = 1.15 + 0.35\,v_r$, so getting back to 1.24 m needs $v_r \le 0.09/0.35 = 0.26$ m/s. One tenth of a second of latency is paid for with three quarters of the robot's speed. Speed scaling and sensing latency are not interchangeable knobs at any rate a paper would advertise, and §6 is where you will see papers trade one for the other in words. Step 8 of [[04-robotics/capstone-panel-contact|26. Capstone]] runs a joint-limit trapezoid through this same $S_p$: the tip reaches $2.04\,\mathrm{m/s}$, $S_p$ grows to $1.50\,\mathrm{m}$, and the check fails until that leg is slowed at the tip.

### 1. Autonomy is a spectrum

| Mode | Human and robot roles |
|---|---|
| Direct teleoperation | human continuously commands motion |
| Assisted teleoperation | robot stabilizes, filters, or avoids constraints |
| Shared autonomy | authority is blended or allocated between human and autonomy |
| Supervisory control | human sets goals and monitors autonomous execution |
| Conditional autonomy | robot acts within a defined operating condition and requests help |
| Full autonomy | robot performs the scoped task without runtime intervention |

The label “autonomous” is incomplete without the task, operating domain, intervention policy, reset procedure, and fallback.



<svg viewBox="0 0 620 234" style="max-width:100%;height:auto" role="img" aria-label="the autonomy spectrum drawn as the human's shrinking share of moment-to-moment decisions">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="150" y1="26" x2="150" y2="196"/><line x1="430" y1="26" x2="430" y2="196"/></g>
  <rect x="150" y="29" width="269.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="42" font-size="10.5" fill="currentColor" text-anchor="end">Direct teleoperation</text>
  <rect x="150" y="56" width="218.1" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="69" font-size="10.5" fill="currentColor" text-anchor="end">Assisted teleoperation</text>
  <rect x="150" y="83" width="166.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="96" font-size="10.5" fill="currentColor" text-anchor="end">Shared autonomy</text>
  <rect x="150" y="110" width="115.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="123" font-size="10.5" fill="currentColor" text-anchor="end">Supervisory control</text>
  <rect x="150" y="137" width="63.5" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="150" font-size="10.5" fill="currentColor" text-anchor="end">Conditional autonomy</text>
  <rect x="150" y="164" width="12.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="177" font-size="10.5" fill="currentColor" text-anchor="end">Full autonomy</text>
  <g font-size="10.5" fill="currentColor">
    <text x="152" y="20">human&#39;s share of the moment-to-moment decisions &#8594;</text><text x="456" y="20">&#8592; robot&#39;s share</text>
    <text x="20" y="210" opacity="0.9">The bar is the human's share. No rung is &#8220;autonomous&#8221; by itself &#8212;</text>
    <text x="20" y="224" opacity="0.9">name the task, the domain, who may intervene, and who resets.</text>
  </g>
</svg>



### 2. Human in, on, and out of the loop

- **In the loop:** human input is part of normal decision/action execution.
- **On the loop:** autonomy acts while a human supervises and may intervene.
- **Out of the loop:** no runtime human role within the stated scope.

Intervention, approval, takeover, teleoperation recovery, and physical reset are different. Papers should report which occurred and whether they count as failures.

### 3. Shared control and authority

Shared autonomy combines human command $u_h$ and autonomous command $u_r$ through arbitration, constraints, or role allocation. A simple blend $u=\alpha u_h+(1-\alpha)u_r$ illustrates the idea but can be unsafe or confusing if commands conflict. Check how intent is inferred, authority changes, conflict is communicated, and the human can override.

Blending is attractive because it gives a smooth command, but a smooth command is not necessarily a safe compromise. With α = 0.5, suppose the human steers left around an obstacle while autonomy steers equally far right, and both retain forward motion. The lateral commands cancel; the combined command can continue straight toward the obstacle even though each original path avoids it.

The conflict is about which side to pass, not simply how much assistance to apply. Arbitration can choose a consistent route or constrain the combined motion, but the worker must understand which authority is active and how to change it.

**The reading this gives you.** Ask what happens when both commands are individually reasonable and mutually incompatible. Inspect conflict handling, constraint checking after combination, and the override path. A blending coefficient by itself does not specify a complete shared-control policy.

### 3.5 Modelling the human inside the robot's decision

The blend of §3 sets by hand how much the human is trusted; the methods below put a model of the human inside the robot's optimisation instead, either as a hidden goal to infer or as an agent who reacts to the robot.

**Shared autonomy as inference over the goal.** The robot does not know where the user is heading, so it treats the goal as the hidden state of a POMDP ([[04-robotics/planning-decision-making|Planning & Decision-Making §7]]) and each joystick command as an observation of it. Javdani, Srinivasa & Bagnell (RSS 2015) model the user as noisy-rational over a discrete goal set and update a belief $b(g)$ by Bayes' rule:

$$P(u \mid x, g) = \frac{\exp\big(\beta\,Q_g(x,u)\big)}{\sum_{u'}\exp\big(\beta\,Q_g(x,u')\big)}, \qquad b'(g) \propto b(g)\,P(u \mid x, g)$$

$Q_g(x,u)$ is the value of command $u$ for someone heading to $g$ (a negative cost-to-go), and $\beta$ is how rational the user is assumed to be. This noisy-rational model is the same exponential model that [[02-foundations/rl-basics|RL Basics §11]] calls a noisy expert, here applied to one command, and since better commands are exponentially more likely but never certain, one sloppy input moves the belief without flipping it.

Exact planning over beliefs is intractable, so the paper uses **hindsight optimisation**, the QMDP approximation:

$$Q(b, a) \approx \sum_g b(g)\,Q_g(x, a)$$

Each robot action $a$ is scored as if the goal would be revealed right after it. So the robot can help before it is sure, by moving where the goals agree, and the amount of help follows from the belief rather than from a hand-set α. What it gives up: an action whose only payoff is information, such as a motion that would make the user's next command more telling, is worth nothing under this score, and the values are optimistic. In shared autonomy that loss is often tolerable, because the user keeps supplying commands anyway.

> [!example] Worked example · 계산 예제
> **Goal inference.** Goals $g_1, g_2$, prior $(0.5, 0.5)$, $\beta = 1$. The user can command $u_1$ (toward $g_1$), $u_2$ (toward $g_2$) or $u_0$ (straight on), with values $Q_{g_1} = (-1, -3, -2)$ and $Q_{g_2} = (-3, -1, -2)$ for $(u_1, u_2, u_0)$.
>
> - Likelihoods: $P(u_1, u_2, u_0 \mid g_1) = (0.665, 0.090, 0.245)$, mirrored under $g_2$.
> - After one $u_1$: $b(g_1) = e^2/(e^2 + 1) = 0.881$. After a second $u_1$: $e^4/(e^4 + 1) = 0.982$.
> - A $u_0$ leaves 0.982 unchanged, since both goals predict it equally; a later $u_2$ brings it back to 0.881. With $\beta = 0.5$ the first $u_1$ gives only 0.731.
>
> **QMDP action.** Robot actions: toward $g_1$, toward $g_2$, and a middle move that serves both, with $Q_{g_1} = (-2, -6, -3.5)$ and $Q_{g_2} = (-6, -2, -3.5)$.
>
> - At the prior the scores are $(-4, -4, -3.5)$, so the robot takes the **middle** move and helps while unsure.
> - At $b(g_1) = 0.881$ they are $(-2.48, -5.52, -3.5)$, so it commits toward $g_1$. The switch is where $-2b - 6(1 - b) = -3.5$, at $b(g_1) = 0.625$.
>
> **The reading this gives you.** The ratio $e^{2\beta}$ per command holds only because the two goals' normalisers are equal here; in general they differ and must be computed, so check that a paper's likelihood is normalised per goal.

**Interaction as a game.** When the human reacts to the robot, the robot's action changes what the human will do, so the planner should optimise through that response. Sadigh, Sastry, Seshia & Dragan (RSS 2016) cast driving next to a human as a Stackelberg (leader–follower) game over a short receding horizon:

$$u_R^* = \arg\max_{u_R} R_R\big(x, u_R, u_H^*(x, u_R)\big), \qquad u_H^*(x, u_R) = \arg\max_{u_H} R_H(x, u_R, u_H)$$

The robot leads because the human is assumed to see its planned controls over the horizon: the human can then only respond to them, while the robot picks its controls knowing that response is coming. $R_H$ is learned from driving data by inverse RL, which recovers a reward from demonstrated behaviour ([[02-foundations/rl-basics|RL Basics §11]]), and treated as a deterministic best response. To optimise with gradients, note that $\partial R_H/\partial u_H = 0$ holds at $u_H^*$ for every $u_R$. Differentiating that identity in $u_R$, with the chain rule running through $u_H^*(u_R)$, gives $\frac{\partial^2 R_H}{\partial u_H^2}\frac{\partial u_H^*}{\partial u_R} + \frac{\partial^2 R_H}{\partial u_H\,\partial u_R} = 0$; solving for the slope, and feeding it into the robot's total derivative, gives

$$\frac{\partial u_H^*}{\partial u_R} = -\Big(\frac{\partial^2 R_H}{\partial u_H^2}\Big)^{-1}\frac{\partial^2 R_H}{\partial u_H\,\partial u_R}, \qquad \frac{dR_R}{du_R} = \frac{\partial R_R}{\partial u_R} + \frac{\partial R_R}{\partial u_H}\,\frac{\partial u_H^*}{\partial u_R}$$

so the chain rule needs second derivatives of $R_H$ at its optimum, not a derivative through the inner solver. That requires $R_H$ smooth, an interior optimum, and an invertible Hessian. Unscripted behaviours emerge: the autonomous car nudges in front of a human-driven car so that it slows, or backs up at an intersection so the human crosses first. A follow-up (Sadigh et al., IROS 2016) adds the drop in belief entropy about the driver's type to $R_R$, so the car inches forward to learn whether the driver is attentive. The risk is that the model does double duty: a nudge is efficient only if $R_H$ is right, and people are not deterministic optimisers — they adapt to a robot that keeps pushing.

> [!example] Worked example · 계산 예제
> **A scalar Stackelberg game.** Human reward $R_H = -u_H^2 + (2 - u_R)\,u_H$, so the best response is $u_H^* = 1 - 0.5\,u_R$: the further the robot moves in, the more the human slows. The implicit formula gives $-(-2)^{-1}(-1) = -0.5$, the same slope. Robot reward $R_R = -(u_R - 1)^2 - 2u_H^2$: stay near its own target 1 and keep the human slow.
>
> - Treating $u_H$ as fixed, the robot picks $u_R = 1$; the human answers $u_H = 0.5$, and $R_R = -0.5$.
> - Through the response, $dR_R/du_R = 4 - 3u_R$ (1.0 at $u_R = 1$, matching a finite difference), so $u_R^* = 4/3$, $u_H = 1/3$, $R_R = -1/3$.
>
> The leader pushes a third past its own target, and only the modelled slope −0.5 justifies it. If this human does not yield ($u_H = 1$), the push costs the robot: $R_R = -2.11$ instead of $-2.00$ at $u_R = 1$.

**Construction bridge.** A crane slewing a load or an excavator swinging near a signal person or spotter has the same structure with a far less forgiving downside. Yielding under an uncertain belief is the conservative direction; probing is not, because an excavator that inches its bucket toward a spotter to see whether they step back is information gathering whose failure case is contact. Two things must stay outside the learned human model. The separation and stop functions of §6 must hold under every plausible hypothesis about the person, not the belief-weighted average that QMDP optimises. And a stop signal is a command with authority, not one more likelihood term. An "influence the human" objective belongs only inside that constraint set; a shorter cycle bought by workers learning to step aside is a change in their exposure, not a safety result.

**What to check in papers.** Is the goal set closed, or can the true goal lie outside it and produce a confidently wrong belief? Was $\beta$ fitted or assumed, and is the belief calibrated ([[04-robotics/human-intent-prediction|23. Human Intent §4]])? Were the gains measured with real people, or with simulated users drawn from the very model the robot assumes?

### 4. Human performance

Relevant constructs include workload, situation awareness (correctly perceiving and understanding what the system and site are doing right now), attention, reaction time, fatigue, skill, mental model (the operator's internal picture of how the system behaves, which sets what they expect it to do next), and trust. High trust is not automatically good: **calibrated trust** means reliance matches system capability and uncertainty. Self-reported trust should be paired with behavior and task outcomes.

Trust is useful when it helps a person allocate attention to the system's actual strengths and weaknesses. It becomes harmful when a reassuring interface makes the operator stop noticing failures. For example, an excavator assistant may receive higher trust ratings and fewer overrides while stale localization goes unnoticed. The reduced intervention rate would then reflect missed opportunities to intervene rather than improved autonomy.

Pair ratings with behavior during recoverable system errors. Can the operator detect the error, identify the active mode, and take over before the task boundary is lost? Also record the monitoring effort required during ordinary operation.

**The reading this gives you.** Ask whether reliance changes appropriately when system competence changes. Favorable attitudes alone cannot establish calibrated trust. A useful human-performance result links the subjective measure to task behavior and explains the conditions under which the interface helps or misleads.

### 5. Interfaces

Visual, audio, haptic, and physical interfaces can show state, intent, uncertainty, warnings, and required action. “Intuitive,” “transparent,” or “natural” are claims requiring measurements. More alarms can reduce safety through alarm fatigue; more explanations can increase workload.

### 6. Safety vocabulary

This section gives you the words a safety paragraph is written in, in four steps. First the
general vocabulary, then which standard defines what. Then the four collaboration methods, and
last a worked example of what the separation distance costs.

**The general vocabulary.**

| Term | Meaning |
|---|---|
| Hazard | potential source or situation of harm |
| Risk | combination of likelihood/exposure and consequence under a method |
| Safety constraint/envelope | boundary intended to keep operation within acceptable conditions |
| Safe stop | controlled transition intended to reduce risk |
| Emergency stop | dedicated means for urgent hazardous-motion stopping |
| Fail-safe | failure leads toward a lower-risk state |
| Fail-operational | selected function continues despite specified failures |
| Near miss | event without harm that could plausibly have produced it |

No learned policy is “safe” merely because it had zero collisions in a small test. Safety is a system property involving sensing, control, hardware, people, environment, procedures, and evidence. Incident 5 of F1, in the worked case of [[06-research-practice/failure-analysis-system-evaluation|3. Failure Analysis & System Evaluation]], is that sentence in one trace: a force-threshold stop kept comparing a stalled sensor's last value with its limit, never fired, and let a 31 N contact through — a stop, and the watchdog guarding it, must check how old its input is, not only its value.

**Which standard says what.** Safety sections quote standard numbers as shorthand. The
shorthand carries the actual claim. You are reading them, not certifying against them. But you
cannot check a safety claim without knowing which document defines the term.

| Standard | Covers | What it gives a reader |
|---|---|---|
| **ISO 10218-1 / -2:2025** | industrial robots (part 1: the robot; part 2: applications and robot cells) | the base requirements; **published February 2025**, first revision since 2011 |
| **ISO/TS 15066:2016** | collaborative applications, biomechanical thresholds | the origin of the force and pressure limits — still a current ISO publication; see below |
| **ISO 13482:2014** | personal care robots | service robots in physical contact with people. Its revision, ISO/FDIS 13482 *Safety requirements for service robots*, widens the scope to personal and professional service robots and is referenced in Europe as EN ISO 13482:2026 — check ISO's catalogue for the published edition before citing either |
| **ISO 3691-4:2023** | driverless industrial trucks — AGVs and AMRs, owned by the industrial-truck committee | the **warehouse and plant** mobile-base standard |
| **ISO 17757:2019** | **autonomous and semi-autonomous earth-moving and mining machines** | the standard for an autonomous excavator or loader — the ISO 6165 machine classes, outdoors |

The takeaway: each standard is scoped to a kind of machine, so check the machine before you accept the citation.

> [!warning] Two mistakes that are easy to make with these numbers
> **ISO/TS 15066 is not withdrawn.** ISO 10218:2025 folded the collaborative-application and
> power-and-force-limiting requirements into the 10218 series, so 10218-1/-2:2025 is now the
> primary citation for a collaborative application. But ISO's own catalogue shows TS 15066:2016
> as *Published*, last confirmed in **2022**, with the note that "this version remains
> current"; its replacement, **ISO/AWI 15066-1** on biomechanical thresholds, is still under
> development. So it remains the citable source for the threshold **data**. Cite 10218:2025 for
> requirements and TS 15066 for the numbers, and do not call it superseded.
>
> **A construction machine is not an industrial truck.** ISO 3691-4 is part of the
> industrial-truck series, scoped to powered materials-handling vehicles in warehouses and
> plants. An autonomous excavator, dozer or loader is read against **ISO 17757:2019** instead.
> Getting this wrong also inflates the "no standard covers outdoor sites" claim: ISO 17757 *was*
> written for outdoor autonomous earth-moving machines. The real gap is narrower and more
> interesting — learned perception, and a site layout that changes weekly.

**The four collaboration methods.** These are the vocabulary a pHRI paper's safety paragraph is
written in. Note that the 2025 revision **renamed the first one**. What the 2011 edition and
TS 15066 call a *safety-rated monitored stop* is **monitored standstill** in ISO 10218-2:2025.
The reason is that it is used for more than collaborative applications. The other three names
are unchanged.

| Method | The mechanism | What it costs |
|---|---|---|
| Monitored standstill (was: safety-rated monitored stop) | robot halts while a person is in the shared space; motion resumes when they leave | throughput — no concurrent work |
| Hand guiding | the operator moves the robot through a hand-operated device | requires the human at the robot |
| **Speed and separation monitoring (SSM)** | keep a *protective separation distance*; slow or stop as it closes | needs reliable person tracking |
| **Power and force limiting (PFL)** | contact is permitted, bounded by force/pressure limits per body region | caps speed and payload by design |

The takeaway: every method trades something away, and the last column names what.

The two that generate research are the last two, and they fail differently. SSM's separation
distance is a **sum of six contributions**, not a threshold. They are: how far the operator
travels while the robot reacts *and* stops; how far the robot travels during its reaction time;
its stopping distance; the **intrusion distance** $C$ — how far a body part reaches into the
sensing field before it is detected at all; and the position uncertainty of the operator and of
the robot. Every learned-perception paper that claims to enable SSM is making a claim about $C$
and the two uncertainty terms. Detector latency enters the distance directly: it adds to the
robot's reaction time $T_r$, which sets both the operator's approach and the robot's reaction
travel (at the example's speeds below, each extra 0.1 s adds 0.26 m). PFL's limits are
**per body region** — the tolerable force on a hand differs from that on a face. They are also
split by contact type: *quasi-static* (the body part is trapped against a surface) versus
*transient* (it can recoil). "Under the force limit" is meaningless without naming region and
contact type.

For construction, match the standard to the machine: a wheeled or tracked **autonomous
earth-moving machine** against ISO 17757, an **arm working next to a person** against ISO
10218, an **AMR moving material in a plant** against ISO 3691-4. None of them was written for
an unfenced, weather-exposed site whose layout changes week to week. But say that against the
named standard, not against "safety" in general.

**What the separation distance costs.** The example below puts numbers on the six-term sum.

> [!example] Worked example · 계산 예제
> **What the separation distance costs you.** ISO/TS 15066 sizes speed-and-separation
> monitoring as $S_p = S_h + S_r + S_s + C + Z_d + Z_r$: the operator's approach, the robot's
> travel during its reaction time, its stopping distance, the intrusion distance $C$ as defined
> in ISO 13855, the operator's position uncertainty $Z_d$ as measured by the presence-sensing
> device, and the robot's position uncertainty $Z_r$. The standard was not read here (UT Libraries
> does not collect ISO standards); the equation and term definitions are as quoted in
> [Himmelsbach et al., *Sensors* 21(21):7144, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8587097/), an open-access paper, which
> also gives the constant-speed form $S_h = 1.6\,(T_r + T_s)$. A 2026 comparative review
> ([Hartmann et al., arXiv 2602.17822](https://arxiv.org/abs/2602.17822)) places this in TS 15066 clause 5.5.4 and
> reports that ISO 10218-2:2025 moves the formulas into its normative Annex L, with SSM in §5.14.5. Take the standard walking speed
> $v_h = 1.6$ m/s from ISO 13855, a robot at $v_r = 1.0$ m/s, reaction $T_r = 0.1$ s, stopping
> $T_s = 0.3$ s, and $C = 0.20$ m, $Z_d = 0.10$ m, $Z_r = 0.05$ m.
>
> $S_h = 1.6(0.1 + 0.3) = 0.64$ m · $S_r = 1.0 \times 0.1 = 0.10$ m · $S_s = \tfrac{1}{2}(1.0)(0.3) = 0.15$ m (assuming constant deceleration over $T_s$).
> Sum: $0.64 + 0.10 + 0.15 + 0.20 + 0.10 + 0.05 = \mathbf{1.24}$ m.
>
> Now halve the robot to 0.5 m/s: $S_r = 0.05$, $S_s = 0.075$, total **1.115 m**. Stop the robot
> dead — $v_r = 0$ — and it is still **0.99 m**. The operator's own 0.64 m does not move,
> because it is the human walking in during the robot's 0.4 s of reaction and stopping.
>
> **The reading this gives you.** In a 1 m cell, slowing the robot buys almost nothing; the
> budget is spent on human approach speed and on $T_r + T_s$. That is why papers claiming
> "safe collaboration by speed scaling" are really claiming a *sensing latency* result, and why
> a stated cycle-time cost is the honest way to report one.

### 7. Human-study design

Within-subject studies compare conditions on the same participant; between-subject studies assign different participants. Counterbalancing helps separate condition effects from practice, fatigue, and order effects. Report participant population, expertise, sample size, exclusions, task realism, objective and subjective measures, and appropriate ethics review by an IRB (Institutional Review Board, the institutional committee that approves research with human participants). When the claim is *perceptual* — the operator felt or noticed something — the measurement procedures themselves are a settled toolbox: [[06-research-practice/psychophysics-human-measurement|8. Psychophysics & Human Measurement]] covers thresholds, the classical procedures, and how to tell a perception study from a performance study. [[04-robotics/haptics-teleoperation/experiments-readings|24.6 Experiments & Reading Map]] works the same design through for a haptic study, including the statistical unit and the safety controls a force-producing device needs.

Order matters because people learn the task while they are being measured. Suppose every participant uses interface A before interface B in a bucket-placement study. B may appear easier because the operator has already learned the target geometry and machine response. A worse interface could therefore look better when it always receives the practice benefit.

Counterbalance the order, provide a declared familiarization procedure, and preserve participant-level comparisons. If learning carries over asymmetrically, simply reversing the order may not remove it; the study should explain how carryover is handled. Repeated trials help characterize each participant, but do not create additional independent participants.

**The reading this gives you.** Inspect the sequence a participant actually experiences, including training and rest. Ask whether the favored condition systematically occurs after practice or before fatigue. A within-subject label does not guarantee a fair comparison unless the schedule supports the interpretation.

### 8. Evaluation

Measure task quality/time, intervention and reset rate, takeover time, workload, situation awareness, trust calibration, safety violations, near misses, productivity, usability, and learning/fatigue. A lower intervention rate may mean better autonomy—or reluctant, overloaded, or poorly informed operators.

A set of measures is needed because improvements can move costs between the robot and the person. For example, an assistant can reduce bucket-placement time while forcing the operator to watch an ambiguous mode indicator continuously. Completion time improves while the monitoring burden grows, and the cost may appear only when an unexpected event occurs.

Choose measures that cover the proposed benefit and its plausible failure mode. If the claim concerns assistance, include the work needed to request, supervise, correct, and reset that assistance. Keep the intervention policy fixed or explain how it differs across conditions.

**The reading this gives you.** Read the evaluation as a ledger of the whole human–robot task. Ask which costs remain outside the reported time and whether a lower event count could result from lower detection. A convincing interpretation connects outcome, operator behavior, and exposure rather than selecting whichever metric improved.

### 9. Construction and field context

Heavy machinery adds blind spots, momentum, noise, dust, vibration, PPE, remote operation, spotters, mixed work zones, trained operators, workflow constraints, and consequential failure. State who holds responsibility, who can stop the machine, and how communication works during degraded operation.

### 10. Worked interpretation

An automated excavator receives a goal from an operator, plans and executes a digging cycle, and allows override. This is supervisory or shared autonomy depending on continuous authority—not simply “fully autonomous.” Evaluation should report overrides, planner/controller failures, unsafe approaches, productivity, operator workload, and the operating conditions in which autonomy was enabled.

Consider a hypothetical study in which the operator chooses a trench target, the excavator executes the digging cycle, and the operator monitors for intervention. Classify authority by decision rather than by the word “autonomous.” Goal selection belongs to the operator; trajectory generation and ordinary execution belong to the machine; emergency recognition may still rely on the operator. This is evidence about supervised task execution. If human commands continuously shape motion, describe that additional shared-control role explicitly.

Next define the counting rule before watching the successful runs. An operator stop ends an autonomous attempt under the proposed rule, even if the machine later completes the dig after assistance. Keep that assisted completion in a separate measure. A reset starts another attempt only after the original attempt has been recorded. Automatic recovery can remain within an attempt if that rule is declared consistently. These distinctions prevent selective editing from turning several rescued attempts into one apparently uninterrupted success.

Record productivity together with the time spent specifying goals, monitoring, recovering, and resetting. Include task quality, unsafe approaches, overrides, failed plans, and sensor outages. Pair workload and trust reports with behavior: whether the operator noticed an error, understood the mode, and took over in time. Specify the soil, machine, visibility, operator experience, and permitted operating envelope. A supervised study cannot omit the supervisor from its system boundary.

Finally, state the strongest conclusion that the design could support: under the tested conditions, the supervised excavator completed the declared task with the reported productivity, intervention burden, and observed failures relative to the stated comparator. If a matched baseline is absent, remove the comparative part. If only a demonstration exists, narrow the conclusion to demonstrated capability. Neither a high success fraction nor a favorable workload rating establishes safe unsupervised operation across construction sites. That larger claim requires evidence about the conditions and failure handling that this study kept outside its boundary.

### After reading

- Describe autonomy using task, domain, intervention, and reset—not one adjective.
- Distinguish human-in/on/out-of-the-loop roles.
- Explain authority allocation and override in shared control.
- Distinguish hazard, risk, fail-safe, and fail-operational.
- Audit human-study population, order effects, and ecological validity.
- Interpret safety and trust claims from measured evidence.

> [!tip] Going deeper · 더 깊이
> This field does have a textbook, and it is free: Bartneck, Belpaeme, Eyssel, Kanda, Keijsers and Šabanović, [*Human-Robot Interaction: An Introduction*](https://www.human-robot-interaction.org/) (Cambridge, 2nd ed. 2024), released as per-chapter PDFs. Read it for §4, §5 and §7 — human performance, interfaces and study design are where a book beats a paper trail, because the methods are settled. Do **not** read it for §6: safety vocabulary comes from the standards themselves, and the versions move. For those, go to the ISO catalogue entries named in the table.

### Self-check

1. Why is “zero collisions in 20 trials” insufficient evidence of safety?
2. When might fewer interventions indicate worse HRI?
3. Why should experienced operators and general participants not be pooled casually?
4. What information is missing from the phrase “fully autonomous construction robot”?
5. In the §3.5 goal-inference example the belief is still 0.5/0.5, yet the QMDP robot moves. Why, and what kind of action can QMDP never favour?
6. A paper plans an excavator swing with a Stackelberg model in which the spotter steps back as the bucket approaches, and reports shorter cycles. What do you ask?

> [!tip]- Answers
> 1. The exposure is small and may omit rare hazards, distribution shift, severity, and system failures. Put a number on it: by the rule of three ([[06-research-practice/experimental-design-reproducibility|Experimental Design §4]]), zero failures in 20 trials still leaves a 95% upper confidence bound on the failure rate of about 14% (exact; the rule-of-three shortcut $3/20 = 15\%$ is rough below $n \approx 30$) — about one collision in seven runs. 2. The operator may miss hazards, distrust the interface, be overloaded, or lack authority. 3. Skill, mental models, speed, workload, and risk response differ. 4. Task, operating domain, human role, intervention/reset, safety fallback, duration, and failure handling. 5. The middle move scores −3.5 against −4 for either goal, because it makes progress that both goals share, so acting beats waiting. QMDP assumes the goal is revealed after one step, so an action whose only benefit is information (a probe that makes the next command more telling) has no value under it. 6. Where $R_H$ came from and whether it was validated on spotters rather than drivers or authors; what happens when the spotter does not step back (distracted, new to the site); whether the separation and stop functions of §6 hold independently of the model; and whether the shorter cycle was bought by workers adapting to a pushing machine, which is a change in exposure rather than a safety gain.

### Problem set · 과제

Tier B. Hand derivation on the **P2** safety cell above, using only this page, its prerequisites and [[02-foundations/lab-plants|0.6]]. The cell is unchanged except where a question changes a number; $v_h = 1.6$ m/s, $T_s = 0.30$ s, $C = 0.20$ m, $Z_d = 0.10$ m and $Z_r = 0.05$ m stay frozen throughout.

A procurement decision has landed on the cell. The new person-tracker is cheaper and 0.1 s slower, so $T_{\text{sens}}$ rises from 0.06 s to 0.16 s and $T_r$ becomes 0.20 s. To compensate, the integrator proposes slowing the robot from $v_r = 1.0$ to $v_r = 0.6$ m/s.

1. **Draw.** Redraw the homework diagram at the new numbers: the plan view with the hazard circle, the sensing-field circle, and the six segments to scale along the approach line; the clock underneath with ticks at $T_{\text{sens}}$, $T_r$ and $T_r + T_s$. Mark the three segments whose lengths did **not** change, and mark on the clock the interval during which the person is walking but nothing about the robot has yet begun to move.
2. **Derive.** Compute $S_h$, $S_r$, $S_s$ and $S_p$ at the new numbers, then the radius at which the sensing field must now start. Then, from the three sensitivities, state the largest reduction in $S_p$ that the robot's speed could possibly buy at $T_r = 0.20$ s, and say whether the integrator's compensation works.
3. **Interpret.** The integrator's report says: "Speed scaling reduced the required separation, keeping the existing cell." A later paper on the same system claims speed scaling shrank the cell by 0.5 m. Using only the sensitivities, say which quantity the paper must actually have changed, and name the two things about the cell that a reported $S_p$ still does not tell you.

> [!tip]- Solutions
> 1. The drawing must keep $C$, $Z_d$ and $Z_r$ at the lengths they had — those three are the unchanged ones, since none of them contains a speed or a time. $S_h$ must be visibly longer than before and $S_s$ visibly shorter. On the clock, the interval from $t = 0$ to $t = 0.20$ s is the person walking while the robot has not yet begun to brake, and the first 0.16 s of it is the detector alone.
> 2. $S_h = 1.6(0.20 + 0.30) = 0.80$ m; $S_r = 0.6 \times 0.20 = 0.12$ m; $S_s = \tfrac{1}{2}(0.6)(0.30) = 0.09$ m; $S_p = 0.80 + 0.12 + 0.09 + 0.20 + 0.10 + 0.05 = 1.36$ m. The field must start at $2.25 + 1.36 = 3.61$ m. The compensation fails, and by more than it looks: $S_p$ went **up** by 0.12 m even after the robot gave up 40% of its speed. At $T_r = 0.20$ s the sensitivity is $\partial S_p/\partial v_r = 0.20 + 0.15 = 0.35$ s, and $S_p$ is linear in $v_r$ at fixed $T_r$, so the robot's whole 1.0 m/s buys at most $0.35$ m ($1.50 \to 1.15$ m), and from the proposed 0.6 m/s only $0.35 \times 0.6 = 0.21$ m is left. Getting back to 1.24 m needs $1.15 + 0.35\,v_r \le 1.24$, that is $v_r \le 0.26$ m/s: the slower detector can be bought back with speed only by giving up three quarters of it.
> 3. It must have changed $T_r$ (a faster detector, or a shorter brake-command path) or $C$ (a sensing field that detects a body earlier, which is the same claim in different clothing). Speed cannot do it: the whole speed budget is $0.25$ m at $T_r = 0.10$ s and $0.35$ m at $T_r = 0.20$ s, both below 0.5 m. What an $S_p$ still does not tell you: whether the cell actually stops — the separation function is worthless without a verified stop, which is the monitored-standstill and emergency-stop machinery of §6 — and what the change cost in cycle time, which is the honest way to report a separation result at all.

### Sources


- The perception layer these decisions run on: [[04-robotics/video-action-understanding|20. Video & Action Understanding]], [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]], [[04-robotics/egocentric-perception|22. Egocentric Perception]], [[04-robotics/human-intent-prediction|23. Human Intent & Trajectory Prediction]] — autonomy and authority are decisions; those pages are what the decision is made from.
- S. Javdani, S. S. Srinivasa, and J. A. Bagnell, "Shared Autonomy via Hindsight Optimization," *Robotics: Science and Systems (RSS)*, 2015 — goal belief from a noisy-rational user model, assistance by the QMDP approximation (§3.5).
- D. Sadigh, S. Sastry, S. A. Seshia, and A. Dragan, "Planning for Autonomous Cars that Leverage Effects on Human Actions," *RSS*, 2016 — the Stackelberg formulation and its implicit-gradient solution (§3.5).
- D. Sadigh, S. Sastry, S. A. Seshia, and A. Dragan, "Information Gathering Actions over Human Internal State," *IEEE/RSJ IROS*, 2016; both combined in D. Sadigh et al., "Planning for cars that coordinate with people: leveraging effects on human actions for planning and active information gathering over human internal state," *Autonomous Robots* 42(7):1405–1426, 2018 — belief-entropy reduction as part of the robot reward (§3.5).
- [NIST Human-Robot Interaction](https://www.nist.gov/topics/human-robot-interaction)
- [NIST Robotics Test Methods](https://www.nist.gov/programs-projects/robotic-systems-smart-manufacturing-program)
- [ACM/IEEE International Conference on Human-Robot Interaction (HRI)](https://humanrobotinteraction.org/) — the field's flagship venue; its papers set the de facto standard for human-study design

## 한국어

*G군이고 그 안의 유일한 페이지다. [[04-robotics/robot-systems-deployment|10. 로봇 시스템]]과 [[02-foundations/ml-practice|ML 실무]] 위에 선다.
기계 옆에 사람이 서 있기 때문에 성공률이 더는 충분한 답이 아니게 되는 지점이다.*

사람이 로봇을 조작·감독하거나, 공간을 공유하거나, 로봇에 의존할 때 과제 성공만으로는
부족하다. 인간-로봇 상호작용(HRI)은 권한, 정보, 작업 부하, 신뢰, 성능을 연구하고, 안전
분석은 어떤 위험 요인이 해를 낳을 수 있고 위험을 어떻게 줄이는지 묻는다.

> [!info] 깊이 목표
> HRI·안전 주장 — 자율성 수준, 개입, 신뢰, hazard/risk — 을 정확히 읽고 인간 대상 연구
> 설계를 검사한다. 인간 대상 연구를 직접 수행하려면 이 페이지 너머의 전문 방법론 훈련이
> 필요하다.

> [!warning] 범위
> 이 페이지는 연구를 읽기 위한 문해력 가이드이지 인증·법규 준수 가이드가 아니다. 해당
> 기계·작업장·관할권에 적용되는 법과 표준은 최신 공식 출처에서 확인해야 한다.

> [!note] 선수 지식
> [[02-foundations/ml-practice|ML 실무와 평가]] · [[04-robotics/robot-systems-deployment|로봇 시스템]] — §9는 [[05-construction-robotics/index|건설로봇]](다음 트랙, 선수 지식 아님)으로 이어진다.

> [!note] 처음이라면 · First pass
> 먼저 아래의 계속 쓰는 대상과 끝까지 계산해 보는 예제 — 이 페이지가 독자에게 빚진 계산은 그 하나다 — 그다음 §1과 §2, 이 문헌의 혼란 대부분이 이 두 스펙트럼 중 하나를 뭉갠 것이다, 그다음 §6의 안전 어휘, 그다음 한 해석을 끝까지 해 보는 §10.

### 계속 쓰는 대상: P2 안전 셀

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2** — 평면 2R 팔, $L_1 = L_2 = 1$ m — 가 도구를 들고 $\theta = (0^\circ, 90^\circ)$ 자세에 있다. 말단은 $(1,1)$ m에서 패널에 도구를 안착시킨다. 팔은 작업 중에도 작업자 한 명이 걸어 들어올 수 있는 셀 안에 서 있다. 아래 숫자는 §6 예제가 이미 쓰는 것과 같고, 검출기가 자기 항으로 보이도록 반응 시간만 한 단계 더 쪼갰다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $L_1, L_2$ | 각 1.00 m | 0.6이 고정한 P2 링크 길이 |
| $L_t$ | 0.25 m | 전완 축을 따라 들어 말단 너머로 그만큼 나오는 도구 — 이 페이지가 P2에 더하는 유일한 값 |
| $v_h$ | 1.6 m/s | 작업자 접근 속도, ISO 13855의 표준 보행 속도 |
| $v_r$ | 1.0 m/s | 사람 방향으로의 로봇 말단 속도 |
| $T_{\text{sens}}$ | 0.06 s | 검출 지연: 신체가 감지 영역에 들어옴 → 추적기가 보고함 |
| $T_{\text{ctrl}}$ | 0.04 s | 제어기 판단과 제동 명령 |
| $T_r$ | 0.10 s | 반응 시간, $T_r = T_{\text{sens}} + T_{\text{ctrl}}$ |
| $T_s$ | 0.30 s | 제동 시작 후 정지까지 걸리는 시간 |
| $C$ | 0.20 m | 침입 거리 — 신체 부위가 감지되기까지 영역 안으로 들어가는 거리 |
| $Z_d$ | 0.10 m | 존재 감지 장치가 재는 작업자 위치 불확실성 |
| $Z_r$ | 0.05 m | 로봇 위치 불확실성 |

도구가 중요한 이유는 위험원이 베이스가 아니라 쓸고 지나가는 부피이기 때문이다. 팔을 뻗으면 위험은 베이스에서 $R_h = L_1 + L_2 + L_t = 2.25$ m까지 닿고, 모든 이격 거리는 *그* 경계에서부터 잰다.

*범위: 이 페이지는 자율성·신뢰·안전 주장을 읽는 법과, 이름을 댄 기계 하나에 안전 기능 하나 — 속도·이격 감시 — 를 치수화하는 법을 가르친다. 기계를 인증하는 법(그것은 §6이 이름을 댄 표준 문서 자체다), 인간 대상 연구를 수행하는 법([[06-research-practice/psychophysics-human-measurement|8. 심리물리]]와 [[06-research-practice/experimental-design-reproducibility|실험 설계]]), 이격 기능에 입력을 넣는 인지가 어떻게 동작하는지([[04-robotics/video-action-understanding|20. 비디오·행동 이해]], [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]])는 가르치지 않는다.*

### 과제가 그릴 그림: 셀의 평면도와 그 아래의 시계

한 번 그려 두면 과제가 같은 그림을 다른 숫자로 다시 요구한다.

<svg viewBox="0 0 560 516" style="max-width:100%;height:auto" role="img" aria-label="안전 셀 과제 그림: 도구를 든 P2의 평면도, 반지름 2.25 m의 점선 위험 원, 3.49 m의 실선 감지 영역 원, 접근선 하나를 따라 축척대로 이어 붙인 1.24 m 이격 거리의 여섯 항, 그리고 그 아래 영역 경계에서 0.40초 정지까지의 시계">
  <text x="16" y="24" font-size="12" fill="currentColor" font-weight="600">평면도 (m)</text>
  <path d="M521.1 294 A223.4 223.4 0 1 0 78.9 294" stroke="currentColor" stroke-width="1.8" fill="none"/>
  <path d="M440.4 294 A144 144 0 1 0 159.6 294" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="6 4"/>
  <line x1="300" y1="262" x2="364" y2="262" stroke="currentColor" stroke-width="4.0" stroke-linecap="round"/>
  <line x1="364" y1="262" x2="364" y2="198" stroke="currentColor" stroke-width="4.0" stroke-linecap="round"/>
  <line x1="364" y1="198" x2="364" y2="182" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
  <rect x="291" y="253" width="18" height="18" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.25"/>
  <circle cx="364" cy="262" r="4" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="1.0"/>
  <circle cx="364" cy="182" r="2.6" stroke="none" fill="currentColor"/>
  <text x="354" y="236" font-size="11" fill="currentColor" text-anchor="end">P2, θ = (0°, 90°)</text>
  <text x="356" y="187" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">도구 0.25 m</text>
  <text x="300" y="148" font-size="11" fill="currentColor" text-anchor="middle">위험 경계</text>
  <text x="300" y="163" font-size="11" fill="currentColor" text-anchor="middle">R<tspan dy="3.1" font-size="8.6">h</tspan><tspan dx="3.1" dy="-3.1">= 2.25 m</tspan></text>
  <text x="300" y="72.6" font-size="11" fill="currentColor" text-anchor="middle">감지 영역 경계</text>
  <text x="300" y="87.6" font-size="11" fill="currentColor" text-anchor="middle">R<tspan dy="3.1" font-size="8.6">h</tspan><tspan dx="3.1" dy="-3.1">+ S</tspan><tspan dy="3.1" font-size="8.6">p</tspan><tspan dx="3.1" dy="-3.1">= 3.49 m</tspan></text>
  <line x1="156" y1="262" x2="288" y2="262" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.5" stroke-dasharray="2 3"/>
  <rect x="76.6" y="258" width="6.4" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.07"/>
  <rect x="83" y="258" width="12.8" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.3"/>
  <rect x="95.8" y="258" width="41" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.15"/>
  <rect x="136.8" y="258" width="9.6" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.38"/>
  <rect x="146.4" y="258" width="6.4" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.22"/>
  <rect x="152.8" y="258" width="3.2" height="8" stroke="currentColor" stroke-width="0.6" fill="currentColor" fill-opacity="0.46"/>
  <circle cx="65.6" cy="242" r="4.6" stroke="currentColor" stroke-width="1.3" fill="none"/>
  <line x1="65.6" y1="247" x2="65.6" y2="259" stroke="currentColor" stroke-width="1.6"/>
  <line x1="65.6" y1="259" x2="60.6" y2="270" stroke="currentColor" stroke-width="1.6"/>
  <line x1="65.6" y1="259" x2="70.6" y2="270" stroke="currentColor" stroke-width="1.6"/>
  <line x1="59.6" y1="251" x2="71.6" y2="251" stroke="currentColor" stroke-width="1.6"/>
  <line x1="88.6" y1="236" x2="115.8" y2="236" stroke="currentColor" stroke-width="1.4"/>
  <path d="M120.6 236 L114.6 238.5 L114.6 233.5 Z" fill="currentColor" stroke="none"/>
  <text x="86.6" y="228" font-size="11" fill="currentColor">v<tspan dy="3.1" font-size="8.6">h</tspan><tspan dx="3.1" dy="-3.1">= 1.6 m/s</tspan></text>
  <text x="78.6" y="282" font-size="11" fill="currentColor" fill-opacity="0.85">아래에 6배</text>
  <rect x="50" y="327" width="38.4" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.07"/>
  <text x="69.2" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.10</text>
  <text x="69.2" y="340" font-size="11" fill="currentColor" text-anchor="middle">Z<tspan dy="3.1" font-size="8.6">d</tspan></text>
  <rect x="88.4" y="327" width="76.8" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.3"/>
  <text x="126.8" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.20</text>
  <text x="126.8" y="340" font-size="11" fill="currentColor" text-anchor="middle">C</text>
  <rect x="165.2" y="327" width="245.8" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.15"/>
  <text x="288.1" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.64</text>
  <text x="288.1" y="340" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">h</tspan></text>
  <rect x="411" y="327" width="57.6" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.38"/>
  <text x="439.8" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.15</text>
  <text x="439.8" y="340" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">s</tspan></text>
  <rect x="468.6" y="327" width="38.4" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22"/>
  <text x="487.8" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.10</text>
  <text x="487.8" y="340" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">r</tspan></text>
  <rect x="507" y="327" width="19.2" height="18" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.46"/>
  <text x="516.6" y="361" font-size="11" fill="currentColor" text-anchor="middle">0.05</text>
  <text x="516.6" y="340" font-size="11" fill="currentColor" text-anchor="middle">Z<tspan dy="3.1" font-size="8.6">r</tspan></text>
  <text x="50" y="322" font-size="11" fill="currentColor" fill-opacity="0.85">영역 경계</text>
  <text x="526.2" y="322" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">위험 경계</text>
  <text x="288.1" y="322" font-size="11" fill="currentColor" text-anchor="middle">S<tspan dy="3.1" font-size="8.6">p</tspan><tspan dx="3.1" dy="-3.1">= 1.24 m</tspan></text>
  <text x="50" y="378" font-size="11" fill="currentColor">t = 0: 신체가 영역 경계를 넘는다</text>
  <rect x="50" y="384" width="400" height="13" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22"/>
  <text x="250" y="394" font-size="11" fill="currentColor" text-anchor="middle">사람은 0.40초 내내 계속 걷는다</text>
  <line x1="50" y1="410" x2="490" y2="410" stroke="currentColor" stroke-width="1.2"/>
  <path d="M502 410 L496 412.5 L496 407.5 Z" fill="currentColor" stroke="none"/>
  <text x="506" y="414" font-size="11" fill="currentColor">t (s)</text>
  <line x1="50" y1="405" x2="50" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <line x1="110" y1="405" x2="110" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <line x1="150" y1="405" x2="150" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <line x1="450" y1="405" x2="450" y2="415" stroke="currentColor" stroke-width="1.4"/>
  <text x="50" y="429" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="150" y1="416" x2="150" y2="425" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="1.5 2"/>
  <line x1="110" y1="416" x2="110" y2="443" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="1.5 2"/>
  <line x1="450" y1="416" x2="450" y2="425" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="1.5 2"/>
  <text x="153" y="435" font-size="11" fill="currentColor">T<tspan dy="3.1" font-size="8.6">r</tspan><tspan dx="3.1" dy="-3.1">= 0.10 s: 제동 명령</tspan></text>
  <text x="450" y="435" font-size="11" fill="currentColor" text-anchor="middle">T<tspan dy="3.1" font-size="8.6">r</tspan><tspan dx="3.1" dy="-3.1">+ T</tspan><tspan dy="3.1" font-size="8.6">s</tspan><tspan dx="3.1" dy="-3.1">= 0.40 s: 정지</tspan></text>
  <text x="113" y="453" font-size="11" fill="currentColor">T<tspan dy="3.1" font-size="8.6">sens</tspan><tspan dx="3.1" dy="-3.1">= 0.06 s: 추적기 보고</tspan></text>
  <text x="16" y="484" font-size="11" fill="currentColor" fill-opacity="0.9">S<tspan dy="3.1" font-size="8.6">p</tspan><tspan dx="3.1" dy="-3.1">= 0.64 + 0.10 + 0.15 + 0.20 + 0.10 + 0.05 = 1.24 m, 위험 경계에서 바깥쪽으로 잰다.</tspan></text>
  <text x="16" y="500" font-size="11" fill="currentColor" fill-opacity="0.9">사람이 걷는 몫 S<tspan dy="3.1" font-size="8.6">h</tspan><tspan dy="-3.1">가 51.6%다. 영역은 3.49 m에서 시작한다: 2.25 m 팔에 바닥 38.3 m².</tspan></text>
</svg>

**위 — 평면도.** P2의 베이스가 원점. 링크 1이 $+x$로 $(1,0)$까지, 링크 2가 위로 말단 $(1,1)$까지, 그 너머로 도구. 베이스를 중심으로 반지름 $R_h = 2.25$ m의 점선 원: 위험 경계. 그 밖에 $R_h + S_p$의 실선 원: 감지 영역 경계. 영역 경계에서 팔 쪽으로 곧게 들어오는 접근선 하나를 긋고, 그 위에 $v_h$로 걷는 사람을 놓는다. 그 선 위에 여섯 기여를, 신체가 실제로 쓰는 순서대로 이어 붙여 표시한다: 먼저 $C$(감지되기 전에 영역 안으로 들어간 거리), 다음 $S_h$(로봇이 반응하고 멈추는 동안 사람이 이동한 거리), 다음 $S_r$과 $S_s$(위험 경계에서 바깥쪽으로 잰 로봇 자신의 이동 거리와 정지 거리), 그리고 양 끝에 두 불확실성 여유 $Z_d$, $Z_r$. 선분은 반드시 축척에 맞게 그려야 한다 — 그것이 이 그림의 전부다.

**아래 — 같은 가로축 위의 시계.** 신체가 영역 경계를 넘는 순간이 $t = 0$. $T_{\text{sens}} = 0.06$ s에 추적기가 사람을 처음 보고하는 눈금, $T_r = 0.10$ s에 제동 명령이 제어기를 떠나는 눈금, $T_r + T_s = 0.40$ s에 운동이 멈춘 눈금. 시계 위에는 0.40초 내내 계속 걷고 있는 사람을 막대 하나로 그린다. 로봇이 무엇을 하든 그 구간은 짧아지지 않기 때문이다.

### 대상으로 한 번 끝까지: 보호 이격 거리를 항별로

> [!info] 정의 · Definition — 보호 이격 거리 $S_p$
> **어떤 종류의 것인가.** *미터 단위의 거리*다. 로봇이 계속 움직여도 되는, 사람과 로봇 위험 경계 사이의 최소 간격이다. 속도가 바뀌면 계속 다시 계산된다 — 울타리 반지름도 아니고 고정된 트리거 문턱값도 아니다.
>
> **정의 조건.** 셋이고, 하나라도 빠지면 숫자가 무의미해진다. (i) 누가 고르는 문턱값이 아니라 **여섯 기여의 합**이다. (ii) 각 기여는 대표하는 양의 **과대평가**여야 한다. 합이 상한이고, 최선의 경우로 쌓은 상한은 아무것도 한정하지 못하기 때문이다. (iii) **위험 경계**에서 잰다 — 베이스도, 도구 끝도, 센서도 아니고 팔과 도구가 쓸고 지나가는 부피의 경계다.
>
> $$S_p = \underbrace{v_h\,(T_r + T_s)}_{S_h} + \underbrace{v_r\,T_r}_{S_r} + \underbrace{\tfrac{1}{2}\,v_r\,T_s}_{S_s} + C + Z_d + Z_r$$
>
> $S_h$는 반응과 정지를 합친 구간 내내 작업자가 접근 속도 $v_h$로 걷는 거리, $S_r$은 로봇이 반응 시간 $T_r$ 동안 $v_r$로 이동하는 거리, $S_s$는 $T_s$ 동안의 정지 거리로 일정 감속 가정에서 $\tfrac{1}{2}v_r T_s$, $C$는 침입 거리, $Z_d$와 $Z_r$은 작업자 측정과 로봇의 위치 불확실성이다. 검출 지연은 자기 기호로 나타나지 않는다 — $T_r$ 안에 들어 있고, 그래서 잃어버리기 쉽다.
>
> **예.** 위의 셀: 1.24 m, 아래에서 항별로 유도한다.
>
> **비-예.** "누가 1 m 안에 들어오면 스캐너가 로봇을 세운다"는 $S_p$가 아니다. 고정 트리거 거리에는 $T_r$도, $T_s$도, $v_h$도 들어 있지 않아서 로봇이 빨라지거나 검출기가 느려져도 변하지 않는다. "영역을 로봇 베이스에서 1.24 m에 설정했다"도 아니다 — 같은 숫자를 잘못된 원점에서 재면, 영역이 사람을 알아채기도 전에 그 사람이 위험 경계 *안으로* $2.25 - 1.24 = 1.01$ m 들어와 있게 된다.
>
> **왜 중요한가.** 비용이 *바닥 면적의 미터 수*로 나오는 유일한 안전 기능이다. 그래서 더 빠른 인지에 대한 주장이든 로봇을 늦추자는 주장이든, 검산할 수 있는 양으로 바뀐다.

이제 셀이다. 고정된 숫자를 항별로, 미터 단위로 대입하면

$$S_h = 1.6\,(0.10 + 0.30) = 0.64,\quad S_r = 1.0 \times 0.10 = 0.10,\quad S_s = \tfrac{1}{2}(1.0)(0.30) = 0.15$$

이고, 그대로인 세 불확실성 항 $C = 0.20$, $Z_d = 0.10$, $Z_r = 0.05$를 더하므로

$$S_p = 0.64 + 0.10 + 0.15 + 0.20 + 0.10 + 0.05 = 1.24\ \mathrm{m}$$

**어느 항이 지배하는가.** 1.24 m에 대한 비중으로: $S_h$ 51.6%, $C$ 16.1%, $S_s$ 12.1%, $S_r$ 8.1%, $Z_d$ 8.1%, $Z_r$ 4.0%. 예산의 절반 이상이 사람이 걷는 몫이고, 로봇 자신의 두 운동 항을 합쳐도 20.2%다. 이 순위가 결과이고, 합은 그 총계일 뿐이다.

**셀이 치르는 비용.** 감지 영역은 P2 베이스에서 $R_h + S_p = 2.25 + 1.24 = 3.49$ m부터 시작해야 하므로, 감시해야 하는 바닥은 $\pi (3.49)^2 = 38.3\ \mathrm{m}^2$다 — 자기 도달 범위가 2.25 m인 팔 하나를 위해서.

**세 민감도, 그리고 결정을 내리는 하나.** 나머지를 고정하고 정의를 미분하면

$$\frac{\partial S_p}{\partial T_r} = v_h + v_r = 2.6\ \mathrm{m/s}, \qquad \frac{\partial S_p}{\partial v_r} = T_r + \tfrac{1}{2}T_s = 0.25\ \mathrm{s}, \qquad \frac{\partial S_p}{\partial v_h} = T_r + T_s = 0.40\ \mathrm{s}$$

반응 시간은 두 번 청구된다 — 한 번은 $S_h$를 통해 사람의 접근에, 한 번은 $S_r$을 통해 로봇 자신의 이동에. 그래서 $v_h + v_r$을 달고 있고 로봇 속도는 그렇지 않다. 숫자를 넣어 보면:

- 검출기가 0.1초 느려지면 $2.6 \times 0.1 = 0.26$ m가 들고, 영역은 3.75 m로 밀려나며 감시 바닥은 $\pi(3.75)^2 = 44.2\ \mathrm{m}^2$, 약 5.9 m² 늘어난다.
- 로봇을 1.0에서 0.5 m/s로 늦추면 $0.25 \times 0.5 = 0.125$ m를 아낀다. $S_p$는 1.115 m로 떨어진다.
- 로봇을 아예 세워도, $v_r = 0$에서 $S_p = 0.99$ m가 남는다. 즉 로봇 속도로 쓸 수 있는 예산 **전부**가 $1.24 - 0.99 = 0.25$ m다.

마지막 줄이 비교 하나로 요약한 이 강의다. 로봇 속도가 가진 예산 전체 $0.25$ m가 검출 지연 0.1초의 값 $0.26$ m와 거의 같다. 민감도는 이 셀에서의 기울기이고 $S_p$에는 곱 $v_rT_r$이 들어 있으니 맞교환을 정확히 따져 보자. 느려진 검출기에서는 $T_r = 0.20$ s, $S_p = 1.15 + 0.35\,v_r$이므로, 1.24 m로 돌아가려면 $v_r \le 0.09/0.35 = 0.26$ m/s여야 한다. 0.1초의 지연을 로봇 속도의 4분의 3으로 치르는 셈이다. 속도 스케일링과 감지 지연은 논문이 내세울 만한 어떤 비율로도 서로 바꿔 쓸 수 있는 손잡이가 아니고, §6은 논문들이 그 둘을 말로 맞바꾸는 것을 보게 되는 곳이다. [[04-robotics/capstone-panel-contact|26. 캡스톤]]의 8단계는 관절 한계 사다리꼴을 이 같은 $S_p$에 통과시킨다. 말단이 $2.04\,\mathrm{m/s}$에 이르러 $S_p$가 $1.50\,\mathrm{m}$로 커지고, 그 구간을 말단에서 늦출 때까지 검사는 실패한다.

### 1. 자율성은 스펙트럼이다

| 모드 | 사람과 로봇의 역할 |
|---|---|
| 직접 원격조작 | 사람이 운동을 연속적으로 명령 |
| 보조 원격조작 | 로봇이 안정화·필터링·제약 회피를 수행 |
| 공유 자율성 | 권한이 사람과 자율성 사이에 혼합·배분됨 |
| 감독 제어 | 사람이 목표를 정하고 자율 실행을 감시 |
| 조건부 자율성 | 정의된 운용 조건 안에서 행동하고 도움을 요청 |
| 완전 자율성 | 범위가 정해진 과제를 런타임 개입 없이 수행 |

"autonomous"라는 라벨은 과제, 운용 도메인, 개입 정책, 리셋 절차, 폴백 없이는 불완전하다.

<svg viewBox="0 0 620 234" style="max-width:100%;height:auto" role="img" aria-label="순간순간의 결정에서 사람의 몫이 줄어드는 것으로 그린 자율성 스펙트럼">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="150" y1="26" x2="150" y2="196"/><line x1="430" y1="26" x2="430" y2="196"/></g>
  <rect x="150" y="29" width="269.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="42" font-size="10.5" fill="currentColor" text-anchor="end">직접 원격조작</text>
  <rect x="150" y="56" width="218.1" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="69" font-size="10.5" fill="currentColor" text-anchor="end">보조 원격조작</text>
  <rect x="150" y="83" width="166.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="96" font-size="10.5" fill="currentColor" text-anchor="end">공유 자율</text>
  <rect x="150" y="110" width="115.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="123" font-size="10.5" fill="currentColor" text-anchor="end">감독 제어</text>
  <rect x="150" y="137" width="63.5" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="150" font-size="10.5" fill="currentColor" text-anchor="end">조건부 자율</text>
  <rect x="150" y="164" width="12.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="177" font-size="10.5" fill="currentColor" text-anchor="end">완전 자율</text>
  <g font-size="10.5" fill="currentColor">
    <text x="152" y="20">순간순간의 결정 중 사람의 몫 &#8594;</text><text x="456" y="20">&#8592; 로봇의 몫</text>
    <text x="20" y="210" opacity="0.9">막대는 사람의 몫이다. 어느 단도 그 자체로 &#8220;자율&#8221;이 아니다 &#8212;</text>
    <text x="20" y="224" opacity="0.9">과제·영역·개입 권한·리셋 주체를 함께 말해야 한다.</text>
  </g>
</svg>



### 2. Human in / on / out of the loop

- **In the loop:** 사람 입력이 정상적 결정·행동 실행의 일부다.
- **On the loop:** 자율성이 행동하고 사람은 감독하며 개입할 수 있다.
- **Out of the loop:** 명시된 범위 안에서 런타임 인간 역할이 없다.

개입, 승인, 인수(takeover), 원격조작 회복, 물리적 리셋은 서로 다르다. 논문은 무엇이
일어났고 그것이 실패로 집계되는지 보고해야 한다.

### 3. 공유 제어와 권한

공유 자율성은 사람 명령 $u_h$와 자율 명령 $u_r$을 중재(arbitration), 제약, 역할 배분으로
결합한다. 단순 혼합 $u=\alpha u_h+(1-\alpha)u_r$은 아이디어를 보여 주지만 두 명령이
충돌하면 위험하거나 혼란스러울 수 있다. 의도를 어떻게 추론하고, 권한이 어떻게 바뀌고,
충돌이 어떻게 전달되고, 사람이 어떻게 override하는지 확인하라.

블렌딩은 부드러운 명령을 주지만 부드러운 명령이 안전한 타협은 아니다. α = 0.5에서 사람은 장애물 왼쪽으로, 자율성은 같은 크기로 오른쪽으로 조향하고 둘 다 전진한다고 하자. 횡방향 명령이 상쇄된다. 원래 경로는 각각 장애물을 피해도 합친 명령은 장애물 정면으로 갈 수 있다.

갈등은 도움의 양보다 어느 쪽으로 지날지에 있다. 중재는 일관된 경로를 선택하거나 합친 동작에 제약을 걸 수 있다. 작업자는 현재 어느 권한이 활성화됐고 어떻게 바꾸는지 알아야 한다.

**여기서 얻는 독법.** 개별적으로 합리적이지만 양립하지 않는 명령이 만나면 어떻게 되는지 묻는다. 갈등 처리, 결합 뒤 제약 검사, 덮어쓰기 경로를 확인한다. 블렌딩 계수만으로 공유 제어 정책 전체가 정해지지는 않는다.

### 3.5 로봇의 결정 안에 사람을 모델링하기

§3의 블렌딩은 사람을 얼마나 믿을지를 손으로 정한다. 아래 방법들은 대신 사람의 모델을 로봇의 최적화 안에 넣는다. 추론할 숨은 목표로 넣거나, 로봇에 반응하는 행위자로 넣는다.

**목표에 대한 추론으로서의 공유 자율성.** 로봇은 사용자가 어디로 가려는지 모르므로, 목표를 POMDP([[04-robotics/planning-decision-making|계획과 의사결정 §7]])의 숨은 상태로, 조이스틱 명령 하나하나를 그 관측으로 다룬다. Javdani, Srinivasa & Bagnell(RSS 2015)은 사용자를 이산 목표 집합 위의 noisy-rational 행위자로 모델링하고 믿음(belief) $b(g)$를 베이즈 규칙으로 갱신한다:

$$P(u \mid x, g) = \frac{\exp\big(\beta\,Q_g(x,u)\big)}{\sum_{u'}\exp\big(\beta\,Q_g(x,u')\big)}, \qquad b'(g) \propto b(g)\,P(u \mid x, g)$$

$Q_g(x,u)$는 $g$로 가려는 사람에게 명령 $u$가 갖는 가치(음의 cost-to-go)이고, $\beta$는 사용자가 얼마나 합리적이라고 가정하는지다. 이 noisy-rational 모델은 [[02-foundations/rl-basics|RL 기초 §11]]이 noisy expert라고 부르는 바로 그 지수형 모델을 명령 하나에 적용한 것이다. 더 좋은 명령일수록 지수적으로 더 그럴듯하지만 확실하지는 않기 때문에, 엉성한 입력 하나는 믿음을 움직일 뿐 뒤집지 않는다.

믿음 위의 정확한 계획은 계산 불가능하므로 이 논문은 **hindsight optimization**, 곧 QMDP 근사를 쓴다:

$$Q(b, a) \approx \sum_g b(g)\,Q_g(x, a)$$

로봇 행동 $a$ 각각을, 그 직후에 목표가 드러난다고 가정하고 점수 매긴다. 그래서 로봇은 확신하기 전에도 목표들이 합의하는 방향으로 움직이며 도울 수 있고, 도움의 양은 손으로 정한 α가 아니라 믿음에서 나온다. 대가도 있다. 정보만을 얻는 행동 — 사용자의 다음 명령을 더 분별력 있게 만드는 동작 같은 것 — 은 이 점수에서 가치가 0이고, 값은 낙관적이다. 공유 자율성에서는 사용자가 어차피 명령을 계속 주기 때문에 이 손실을 대개 감수할 만하다.

> [!example] 계산 예제 · Worked example
> **목표 추론.** 목표 $g_1, g_2$, 사전 $(0.5, 0.5)$, $\beta = 1$. 사용자는 $u_1$($g_1$ 쪽), $u_2$($g_2$ 쪽), $u_0$(직진)을 명령할 수 있고, $(u_1, u_2, u_0)$의 가치는 $Q_{g_1} = (-1, -3, -2)$, $Q_{g_2} = (-3, -1, -2)$다.
>
> - 우도: $P(u_1, u_2, u_0 \mid g_1) = (0.665, 0.090, 0.245)$, $g_2$에서는 좌우를 뒤집은 값.
> - $u_1$ 한 번 뒤: $b(g_1) = e^2/(e^2 + 1) = 0.881$. $u_1$을 한 번 더: $e^4/(e^4 + 1) = 0.982$.
> - $u_0$는 두 목표가 똑같이 예측하므로 0.982를 그대로 두고, 이어서 $u_2$가 오면 0.881로 돌아간다. $\beta = 0.5$라면 첫 $u_1$ 뒤 값은 0.731에 그친다.
>
> **QMDP 행동.** 로봇 행동은 $g_1$ 쪽, $g_2$ 쪽, 둘 다에 도움이 되는 가운데 이동이고, $Q_{g_1} = (-2, -6, -3.5)$, $Q_{g_2} = (-6, -2, -3.5)$다.
>
> - 사전에서 점수는 $(-4, -4, -3.5)$이므로 로봇은 **가운데 이동을** 골라 불확실한 채로 돕는다.
> - $b(g_1) = 0.881$에서는 $(-2.48, -5.52, -3.5)$이므로 $g_1$ 쪽으로 확정한다. 전환점은 $-2b - 6(1 - b) = -3.5$인 $b(g_1) = 0.625$다.
>
> **여기서 얻는 독법.** 명령 하나당 비율 $e^{2\beta}$는 여기서 두 목표의 정규화 상수가 같기 때문에만 성립한다. 일반적으로는 다르므로 계산해야 한다. 논문의 우도가 목표별로 정규화됐는지 확인하라.

**게임으로서의 상호작용.** 사람이 로봇에 반응하면 로봇의 행동이 사람이 할 일을 바꾸므로, 플래너는 그 반응을 거쳐 최적화해야 한다. Sadigh, Sastry, Seshia & Dragan(RSS 2016)은 사람 옆에서의 주행을 짧은 receding horizon 위의 Stackelberg(선도자–추종자) 게임으로 세운다:

$$u_R^* = \arg\max_{u_R} R_R\big(x, u_R, u_H^*(x, u_R)\big), \qquad u_H^*(x, u_R) = \arg\max_{u_H} R_H(x, u_R, u_H)$$

사람이 horizon 동안 로봇의 계획된 제어를 본다고 가정하기 때문에 로봇이 선도자다: 그러면 사람은 그 제어에 반응할 수밖에 없고, 로봇은 그 반응이 올 것을 알고 제어를 고른다. $R_H$는 주행 데이터에서 역강화학습 — 시연된 행동으로부터 보상을 복원하는 방법([[02-foundations/rl-basics|RL 기초 §11]]) — 으로 배우고, 결정론적 최적 반응으로 취급한다. 경사로 최적화하려면, $u_H^*$에서 $\partial R_H/\partial u_H = 0$이 모든 $u_R$에 대해 성립한다는 점을 쓴다. 그 항등식을 $u_R$로 미분하면, 연쇄 법칙이 $u_H^*(u_R)$를 거쳐 $\frac{\partial^2 R_H}{\partial u_H^2}\frac{\partial u_H^*}{\partial u_R} + \frac{\partial^2 R_H}{\partial u_H\,\partial u_R} = 0$을 주고, 이를 기울기에 대해 풀고 로봇의 전미분에 넣으면 다음과 같다.

$$\frac{\partial u_H^*}{\partial u_R} = -\Big(\frac{\partial^2 R_H}{\partial u_H^2}\Big)^{-1}\frac{\partial^2 R_H}{\partial u_H\,\partial u_R}, \qquad \frac{dR_R}{du_R} = \frac{\partial R_R}{\partial u_R} + \frac{\partial R_R}{\partial u_H}\,\frac{\partial u_H^*}{\partial u_R}$$

이므로 연쇄 법칙에는 내부 풀이기를 거친 미분이 아니라 최적점에서 $R_H$의 2계 도함수만 필요하다. 이를 위해 $R_H$가 매끄럽고, 최적점이 내부에 있고, 헤시안이 가역이어야 한다. 아무도 스크립트하지 않은 행동이 나온다. 자율주행차가 사람이 모는 차 앞으로 비집고 들어가 그 차를 늦추거나, 교차로에서 살짝 후진해 사람이 먼저 건너게 한다. 후속 연구(Sadigh et al., IROS 2016)는 운전자 유형에 대한 믿음의 엔트로피 감소를 $R_R$에 더해, 차가 조금씩 앞으로 나가며 운전자가 주의하고 있는지 알아내게 한다. 위험은 모델이 두 가지 일을 한다는 데 있다. 비집고 들어가기는 $R_H$가 맞을 때만 효율적이고, 사람은 결정론적 최적화기가 아니며 계속 밀어붙이는 로봇에 적응한다.

> [!example] 계산 예제 · Worked example
> **스칼라 Stackelberg 게임.** 사람 보상 $R_H = -u_H^2 + (2 - u_R)\,u_H$이면 최적 반응은 $u_H^* = 1 - 0.5\,u_R$이다. 로봇이 더 들어올수록 사람은 더 늦춘다. 암묵 미분 공식은 $-(-2)^{-1}(-1) = -0.5$로 같은 기울기를 준다. 로봇 보상 $R_R = -(u_R - 1)^2 - 2u_H^2$: 자기 목표 1 근처에 머물고 사람을 느리게 둔다.
>
> - $u_H$를 고정으로 취급하면 로봇은 $u_R = 1$을 고르고, 사람은 $u_H = 0.5$로 답하며 $R_R = -0.5$다.
> - 반응을 거치면 $dR_R/du_R = 4 - 3u_R$($u_R = 1$에서 1.0, 유한 차분과 일치)이므로 $u_R^* = 4/3$, $u_H = 1/3$, $R_R = -1/3$이다.
>
> 선도자는 자기 목표보다 3분의 1 더 밀고 들어가며, 그것을 정당화하는 것은 모델의 기울기 −0.5뿐이다. 이 사람이 양보하지 않으면($u_H = 1$) 그 밀기는 로봇에게 손해다: $u_R = 1$일 때의 $-2.00$ 대신 $R_R = -2.11$.

**건설로 잇기.** 짐을 선회시키는 크레인이나 신호수·유도원 근처에서 선회하는 굴착기는 같은 구조이지만 실패의 대가가 훨씬 가혹하다. 믿음이 불확실할 때 양보하는 것은 보수적인 방향이다. 탐색은 그렇지 않다. 유도원이 물러서는지 보려고 버킷을 조금씩 들이미는 굴착기는, 실패하면 접촉으로 끝나는 정보 수집이기 때문이다. 두 가지는 학습된 사람 모델 밖에 두어야 한다. §6의 이격·정지 기능은 QMDP가 최적화하는 믿음 가중 평균이 아니라, 사람에 대한 그럴듯한 모든 가설 아래에서 성립해야 한다. 그리고 정지 신호는 권한을 가진 명령이지 우도 항 하나가 아니다. "사람에게 영향을 주는" 목적함수는 그 제약 집합 안에만 있어야 한다. 작업자가 비켜서는 법을 익혀서 얻은 짧은 사이클은 그들의 노출이 바뀐 것이지 안전 결과가 아니다.

**논문에서 확인할 것.** 목표 집합이 닫혀 있는가, 아니면 진짜 목표가 그 밖에 있어 확신에 찬 틀린 믿음이 나올 수 있는가? $\beta$는 적합했는가 가정했는가, 그리고 믿음은 보정됐는가([[04-robotics/human-intent-prediction|23. 인간 의도 §4]])? 이득은 실제 사람으로 측정했는가, 아니면 로봇이 가정한 바로 그 모델에서 뽑은 모의 사용자로 측정했는가?

### 4. 인간 성능

작업 부하, 상황 인식(시스템과 현장이 지금 무엇을 하고 있는지 올바르게 지각하고 이해하는 상태), 주의, 반응 시간, 피로, 숙련,
멘탈 모델(시스템이 어떻게 움직이는지에 대한 조작자의 내적 그림으로, 다음에 무엇을 기대할지를 정한다), 신뢰가 관련 구성 개념이다.
높은 신뢰가 자동으로 좋은 것이 아니다: **보정된 신뢰**(calibrated trust)란 의존이 시스템의
능력과 불확실성에 맞는 상태다. 자기 보고 신뢰는 행동·과제 결과와 짝지어 읽어야 한다.

신뢰는 사람이 시스템의 실제 장단점에 맞춰 주의를 배분할 때 유용하다. 안심시키는 인터페이스 때문에 실패를 알아채지 못하면 해롭다. 굴착기 보조 기능의 신뢰 점수는 오르고 덮어쓰기는 줄었지만 낡은 위치 추정을 놓쳤다고 하자. 개입 감소는 자율성 개선보다 개입 기회를 놓친 결과일 수 있다.

평점을 회복 가능한 시스템 오류 중의 행동과 짝짓는다. 운전자가 오류를 감지하고, 활성 모드를 파악하고, 과제 경계를 잃기 전에 인수할 수 있는가? 정상 운전의 감시 노력도 기록한다.

**여기서 얻는 독법.** 시스템 능력이 달라질 때 의존도도 적절히 달라지는지 묻는다. 호의적인 태도만으로 보정된 신뢰를 확립할 수 없다. 유용한 인간 수행 결과는 주관 지표를 과제 행동과 연결하고 인터페이스가 돕거나 오도하는 조건을 설명한다.

### 5. 인터페이스

시각·청각·햅틱·물리 인터페이스는 상태, 의도, 불확실성, 경고, 요구 행동을 보여 줄 수
있다. "Intuitive", "transparent", "natural"은 측정을 요구하는 주장이다. 경보가 많으면
경보 피로로 오히려 안전이 떨어질 수 있고, 설명이 많으면 작업 부하가 늘 수 있다.

### 6. 안전 어휘

이 절은 안전 문단이 쓰이는 어휘를 네 단계로 준다. 먼저 일반 어휘, 다음으로 어느 표준이 무엇을
정의하는지 본다. 이어서 네 가지 협동 방법을 보고, 마지막으로 이격 거리가 무엇을 앗아가는지
계산 예제로 확인한다.

**일반 어휘.**

| 용어 | 의미 |
|---|---|
| Hazard | 잠재적 해의 원천·상황 |
| Risk | 정해진 방법 아래 가능성/노출과 결과의 결합 |
| 안전 제약/엔벨로프 | 허용 조건 안에 운용을 유지하려는 경계 |
| Safe stop | 위험을 낮추려는 통제된 전이 |
| 비상 정지 | 긴급한 위험 운동 정지를 위한 전용 수단 |
| Fail-safe | 실패가 더 낮은 위험 상태로 이어짐 |
| Fail-operational | 명시된 실패에도 선택 기능이 지속 |
| Near miss | 해는 없었지만 그럴듯하게 해를 낳을 수 있었던 사건 |

작은 시험에서 충돌이 없었다는 이유만으로 학습 정책이 "안전"한 것은 아니다. 안전은 센싱,
제어, 하드웨어, 사람, 환경, 절차, 증거가 얽힌 시스템 속성이다. [[06-research-practice/failure-analysis-system-evaluation|3. 실패 분석·시스템 평가]] worked case의 F1 사건 5가 이 문장을 기록 하나로 보여 준다. 힘 문턱 정지가 멈춘 센서의 마지막 값을 문턱과 계속 비교하다가 끝내 작동하지 않았고, 31 N 접촉이 그대로 지나갔다. 정지 기능과 그것을 지키는 watchdog은 입력의 값만이 아니라 그 입력이 얼마나 오래되었는지를 검사해야 한다.

**어느 표준이 무엇을 말하는가.** 안전 절은 표준 번호를 약칭처럼 인용한다. 그 약칭이 실제
주장을 지고 있다. 우리는 인증하는 것이 아니라 읽는 것이다. 그래도 어느 문서가 그 용어를
정의하는지 모르면 안전 주장을 검증할 수 없다.

| 표준 | 대상 | 읽는 사람에게 주는 것 |
|---|---|---|
| **ISO 10218-1 / -2:2025** | 산업용 로봇(1부: 로봇, 2부: 응용과 로봇 셀) | 기본 요구사항. **2025년 2월 발행**, 2011년 이후 첫 개정 |
| **ISO/TS 15066:2016** | 협동 응용, 생체역학 임계값 | 힘·압력 한계의 출처. 여전히 유효한 ISO 발행물이다 — 아래를 보라 |
| **ISO 13482:2014** | 개인 돌봄 로봇 | 사람과 물리적으로 접촉하는 서비스 로봇. 개정판 ISO/FDIS 13482 *Safety requirements for service robots*는 범위를 개인·전문 서비스 로봇으로 넓히며, 유럽에서는 EN ISO 13482:2026으로 인용된다 — 어느 쪽이든 인용 전에 ISO 카탈로그에서 발행판을 확인하라 |
| **ISO 3691-4:2023** | 무인 산업 차량 — AGV·AMR, 산업차량 위원회 소관 | **창고와 공장**의 이동 베이스 표준 |
| **ISO 17757:2019** | **자율·반자율 토공 및 광산 기계** | 자율 굴착기나 로더의 표준 — ISO 6165 기계 분류, 옥외 |

요점: 표준마다 대상 기계가 정해져 있으니, 인용을 받아들이기 전에 기계부터 확인하라.

> [!warning] 이 번호들에서 저지르기 쉬운 두 가지 실수
> **ISO/TS 15066은 폐지되지 않았다.** ISO 10218:2025가 협동 응용과 동력 및 힘 제한(Power and Force Limiting, PFL) 요구사항을
> 10218 시리즈로 흡수했으므로, 협동 응용의 1차 인용은 이제 10218-1/-2:2025다. 그러나 ISO의
> 카탈로그는 TS 15066:2016을 *Published*로 두고 있고, 최종 확인이 **2022년**이며, "이 판본은
> 여전히 유효하다"고 적고 있다. 후속인 **ISO/AWI 15066-1**(생체역학 임계값)은 아직 개발 중이다.
> 그러니 임계값 **데이터**의 인용처로는 여전히 유효하다. 요구사항은 10218:2025를, 숫자는
> TS 15066을 인용하고, 대체되었다고 말하지 마라.
>
> **건설 기계는 산업 차량이 아니다.** ISO 3691-4는 산업차량 시리즈의 일부로, 창고와 공장의
> 동력 자재취급 차량을 범위로 한다. 자율 굴착기·도저·로더는 대신 **ISO 17757:2019**로 읽는다.
> 이것을 틀리면 "옥외 현장을 다루는 표준이 없다"는 주장도 부풀려진다: ISO 17757은 *바로*
> 옥외 자율 토공 기계를 위해 쓰였다. 진짜 빈틈은 더 좁고 더 흥미롭다 — 학습된 인지, 그리고
> 주 단위로 바뀌는 현장 배치.

**네 가지 협동 방법.** 이것이 pHRI 논문의 안전 문단이 쓰이는 어휘다. 2025년 개정이
**첫 번째의 이름을 바꿨다는 점**을 유의하라. 2011년판과 TS 15066이 *safety-rated monitored
stop*이라 부르는 것이 ISO 10218-2:2025에서는 **monitored standstill**이다. 협동 응용 외에도
쓰이기 때문이다. 나머지 셋의 이름은 그대로다.

| 방법 | 기구 | 대가 |
|---|---|---|
| Monitored standstill(구: safety-rated monitored stop) | 사람이 공유 공간에 있는 동안 로봇이 멈추고, 나가면 재개 | 처리량 — 동시 작업이 불가능 |
| Hand guiding | 조작자가 손으로 조작하는 장치로 로봇을 움직인다 | 사람이 로봇 옆에 있어야 함 |
| **속도·이격 감시(SSM)** | *보호 이격 거리*를 유지하고, 거리가 좁혀지면 감속·정지 | 신뢰할 수 있는 사람 추적이 필요 |
| **동력 및 힘 제한(PFL)** | 접촉을 허용하되 신체 부위별 힘·압력 한계로 제한 | 설계상 속도와 가반하중이 묶임 |

요점: 모든 방법은 무언가를 내주며, 마지막 열이 그것을 적는다.

연구를 낳는 것은 뒤의 둘이고, 둘은 서로 다르게 실패한다. SSM의 이격 거리는 임계값이 아니라
**여섯 항의 합**이다. 그 항은 다음과 같다: 로봇이 반응하고 *또* 정지하는 동안 조작자가 이동한
거리; 로봇이 반응 시간 동안 이동한 거리; 로봇의 정지 거리; **침입 거리** $C$ — 신체 부위가
감지되기까지 감지 영역 안으로 얼마나 들어가는가; 그리고 조작자와 로봇 각각의 위치 불확실성.
SSM을 가능하게 한다고 주장하는 모든 학습 기반 인지 논문은 사실 $C$와 두 불확실성 항에 대한
주장을 하고 있다. 검출기의 지연은 그 거리에 직접 들어간다: 지연은 로봇의 반응 시간 $T_r$에
더해지고, $T_r$은 조작자의 접근 거리와 로봇의 반응 중 이동 거리를 함께 정한다(아래 예제의
속도라면 지연 0.1초마다 0.26 m가 늘어난다). PFL의 한계는 **신체 부위별**이다 —
손에 허용되는 힘은 얼굴의 것과 다르다. 접촉 유형으로도 갈린다: *준정적*(신체 부위가 표면에
끼임) 대 *과도*(튕겨 나올 수 있음). "힘 한계 이하"는 부위와 접촉 유형을 밝히지 않으면 아무
의미가 없다.

건설에서는 기계에 표준을 맞춰라: 바퀴·궤도형 **자율 토공 기계**는 ISO 17757, 사람 옆에서
일하는 **팔**은 ISO 10218, 공장에서 자재를 나르는 **AMR**은 ISO 3691-4. 그중 어느 것도 울타리
없이 날씨에 노출되고 배치가 주 단위로 바뀌는 현장을 위해 쓰이지 않았다. 다만 그것을 "안전"
일반이 아니라 이름을 댄 표준에 대고 말하라.

**이격 거리가 무엇을 앗아가는가.** 아래 예제는 여섯 항의 합에 숫자를 넣어 본다.

> [!example] 계산 예제 · Worked example
> **분리 거리가 실제로 무엇을 앗아가는가.** ISO/TS 15066은 속도·분리 감시를
> $S_p = S_h + S_r + S_s + C + Z_d + Z_r$로 계산한다: 작업자의 접근, 로봇이 반응 시간 동안
> 이동한 거리, 정지 거리, ISO 13855에서 정의한 침입 거리 $C$, 존재 감지 장치로 측정한 작업자
> 위치 불확실성 $Z_d$, 로봇 위치 불확실성 $Z_r$이다. 여기서 표준 원문을 읽지는 못했다(UT 도서관은
> ISO 표준을 소장하지 않는다). 식과 항 정의는
> 공개 논문 [Himmelsbach 외, *Sensors* 21(21):7144, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8587097/)이 인용한 그대로이며, 이 논문은
> 속도 일정 형태 $S_h = 1.6\,(T_r + T_s)$도 준다. 2026년 비교 리뷰
> ([Hartmann 외](https://arxiv.org/abs/2602.17822))는 이 내용을 TS 15066 5.5.4절에 두고,
> ISO 10218-2:2025가 이 식들을 규범 부속서 L로 옮기고 SSM을 §5.14.5에 두었다고 보고한다.
> ISO 13855의 표준 보행 속도 $v_h = 1.6$ m/s, 로봇 $v_r = 1.0$ m/s, 반응 $T_r = 0.1$ s,
> 정지 $T_s = 0.3$ s, $C = 0.20$ m, $Z_d = 0.10$ m, $Z_r = 0.05$ m를 넣자.
>
> $S_h = 1.6(0.1 + 0.3) = 0.64$ m · $S_r = 1.0 \times 0.1 = 0.10$ m · $S_s = \tfrac{1}{2}(1.0)(0.3) = 0.15$ m($T_s$ 동안 일정하게 감속한다고 가정).
> 합: $0.64 + 0.10 + 0.15 + 0.20 + 0.10 + 0.05 = \mathbf{1.24}$ m.
>
> 이제 로봇을 절반인 0.5 m/s로 줄이면 $S_r = 0.05$, $S_s = 0.075$, 합 **1.115 m**. 아예 세워도
> — $v_r = 0$ — 여전히 **0.99 m**다. 작업자 몫 0.64 m는 꿈쩍하지 않는다. 로봇이 반응하고
> 멈추는 0.4초 동안 사람이 걸어 들어오는 거리이기 때문이다.
>
> **여기서 얻는 독법.** 1 m 셀에서는 로봇을 늦춰 봐야 거의 얻는 것이 없다. 예산은 사람의
> 접근 속도와 $T_r + T_s$가 다 쓴다. "속도 스케일링으로 안전한 협업"을 주장하는 논문이 사실은
> *감지 지연* 결과를 주장하고 있는 이유이고, 사이클 타임 손실을 함께 밝히는 것이 그런 결과를
> 정직하게 보고하는 방법인 이유다.

### 7. 인간 대상 연구 설계

Within-subject 연구는 같은 참가자에게 조건들을 비교하고, between-subject 연구는 참가자를
나눠 배정한다. Counterbalancing은 조건 효과를 연습·피로·순서 효과와 분리하는 데 돕는다.
참가자 모집단, 전문성, 표본 크기, 제외, 과제 현실성, 객관·주관 지표, 적절한 윤리 심의(IRB,
즉 사람 참가자 연구를 승인하는 기관 연구윤리위원회)를 보고하라. 주장이 *지각*에 관한 것이라면 — 작업자가 느꼈다, 알아챘다 — 측정 절차
자체가 정착된 공구함이다:
[[06-research-practice/psychophysics-human-measurement|8. 심리물리와 인간 측정]]이 임계값,
고전적 절차들, 그리고 지각 연구와 성능 연구를 구분하는 법을 다룬다.
[[04-robotics/haptics-teleoperation/experiments-readings|24.6 실험과 읽기 지도]]는 같은 설계를
햅틱 연구에서 끝까지 밟는다. 통계 단위와, 힘을 내는 장치에 필요한 안전 통제까지 포함한다.

측정 중에도 사람이 과제를 배우므로 순서가 중요하다. 버킷 배치 연구에서 모든 참가자가 A 인터페이스를 먼저, B를 나중에 쓴다고 하자. B는 운전자가 이미 목표 형상과 기계 반응을 익혔기 때문에 쉬워 보일 수 있다. 더 나쁜 인터페이스도 항상 연습 효과를 받으면 더 좋아 보인다.

순서를 균형 배치하고 익숙해지는 절차를 명시하며 참가자별 비교를 보존한다. 학습의 이월 효과가 비대칭이면 순서 반전만으로 사라지지 않을 수 있다. 처리 방법을 설명해야 한다. 반복 시행은 각 참가자를 더 잘 측정하지만 독립 참가자를 늘리지는 않는다.

**여기서 얻는 독법.** 훈련과 휴식을 포함해 참가자가 실제 경험한 순서를 본다. 유리한 조건이 늘 연습 뒤나 피로 전인지 묻는다. 일정이 해석을 뒷받침하지 않으면 within-subject라는 이름만으로 공정한 비교가 보장되지 않는다.

### 8. 평가

과제 품질/시간, 개입·리셋 빈도, 인수 시간, 작업 부하, 상황 인식, 신뢰 보정, 안전 위반,
near miss, 생산성, 사용성, 학습·피로 효과를 재라. 낮은 개입률은 더 나은 자율성을 뜻할
수도 있고 — 꺼리거나, 과부하거나, 정보가 부족한 운용자를 뜻할 수도 있다.

개선이 로봇과 사람 사이에 비용을 옮길 수 있어 여러 측정이 필요하다. 보조 기능이 버킷 배치 시간을 줄이면서 운전자에게 모호한 모드 표시를 계속 감시하게 할 수 있다. 완료 시간은 좋아져도 감시 부담은 늘고 예상 밖 사건에서야 비용이 드러난다.

제안한 이점과 그럴듯한 실패 방식을 함께 다루는 지표를 고른다. 보조를 주장하면 보조를 요청하고 감독하고 고치고 리셋하는 일도 포함한다. 개입 정책을 고정하거나 조건별 차이를 설명한다.

**여기서 얻는 독법.** 평가를 인간–로봇 과제 전체의 비용 기록으로 읽는다. 보고 시간 밖에 남은 비용과 사건 감소가 감지 감소에서 올 가능성을 묻는다. 설득력 있는 해석은 좋아진 지표만 고르지 않고 결과, 운전자 행동, 노출을 연결한다.

### 9. 건설·현장 맥락

중장비는 사각지대, 관성, 소음, 먼지, 진동, PPE, 원격 운용, 신호수(spotter), 혼재 작업
구역, 숙련 운용자, 공정 제약, 결과가 무거운 실패를 더한다. 책임이 누구에게 있고, 누가
기계를 멈출 수 있고, 성능 저하 운용 중 소통이 어떻게 되는지를 명시하라.

### 10. 해석 예제

자동화 굴착기가 운용자에게서 목표를 받아 굴착 사이클을 계획·실행하고 override를
허용한다. 이는 연속적 권한 여부에 따라 감독 제어 또는 공유 자율성이다 — 단순히 "완전
자율"이 아니다. 평가는 override, 플래너/제어기 실패, 위험 접근, 생산성, 운용자 작업
부하, 그리고 자율성이 켜져 있던 운용 조건을 보고해야 한다.

가상 연구에서 운전자가 도랑 목표를 고르고, 굴착기가 사이클을 실행하며, 운전자는 개입을 위해 감시한다고 하자. “자율”이라는 단어보다 결정별로 권한을 분류한다. 목표 선택은 사람, 궤적 생성과 정상 실행은 기계, 비상 인지는 여전히 사람에게 의존할 수 있다. 이는 감독하 과제 실행의 증거다. 사람 명령이 동작을 계속 바꾸면 공유 제어 역할도 따로 밝힌다.

성공 영상을 보기 전에 집계 규칙을 정한다. 여기서는 운전자 정지가 자율 시도를 끝낸다. 이후 보조를 받아 굴착을 마쳐도 보조 완료로 별도 집계한다. 리셋은 원래 시도를 기록한 뒤에만 새 시도를 시작한다. 자동 회복은 일관된 사전 규칙이 있으면 같은 시도 안에 남길 수 있다. 이 구분이 있어야 여러 번 구조한 시도를 편집해 중단 없는 성공처럼 만들지 않는다.

생산성과 함께 목표 지정, 감시, 회복, 리셋 시간을 기록한다. 과제 품질, 위험 접근, 덮어쓰기, 계획 실패, 센서 중단도 포함한다. 작업부하·신뢰 평점은 오류 인지, 모드 이해, 제때 인수했는지와 짝짓는다. 토질, 기계, 가시성, 운전자 숙련도, 허용 운용 범위를 밝힌다. 감독 연구에서 감독자를 시스템 경계 밖으로 뺄 수 없다.

마지막으로 설계가 지지할 수 있는 가장 강한 결론을 쓴다. 시험 조건에서 감독하 굴착기가 명시한 비교 대상 대비 보고한 생산성·개입 부담·관찰 실패로 과제를 수행했다는 것이다. 짝지은 베이스라인이 없으면 비교 부분을 뺀다. 시연만 있으면 시연된 능력으로 좁힌다. 높은 성공 비율이나 좋은 작업부하 평점만으로 건설 현장 전반의 안전한 무감독 운용을 확립할 수 없다. 더 큰 주장에는 이번 연구가 경계 밖에 둔 조건과 실패 처리에 관한 증거가 필요하다.

### 읽고 나면 말할 수 있어야 하는 것

- 자율성을 형용사 하나가 아니라 과제·도메인·개입·리셋으로 기술할 수 있다
- human-in/on/out-of-the-loop 역할을 구분할 수 있다
- 공유 제어의 권한 배분과 override를 설명할 수 있다
- hazard·risk·fail-safe·fail-operational을 구분할 수 있다
- 인간 연구의 모집단·순서 효과·생태적 타당성을 검사할 수 있다
- 안전·신뢰 주장을 측정된 증거로부터 해석할 수 있다

> [!tip] 더 깊이 · Going deeper
> 이 분야에는 교과서가 있고, 무료다: Bartneck, Belpaeme, Eyssel, Kanda, Keijsers, Šabanović, [*Human-Robot Interaction: An Introduction*](https://www.human-robot-interaction.org/) (Cambridge, 2판 2024), 장별 PDF로 공개돼 있다. §4·§5·§7 — 인간 성능, 인터페이스, 연구 설계 — 을 위해 읽어라. 방법론이 정착된 영역이라 책이 논문 더미를 이긴다. §6을 위해서는 읽지 **마라**. 안전 어휘는 표준 문서 자체에서 오고 판본이 계속 움직인다. 그쪽은 표에 적힌 ISO 카탈로그 항목으로 직접 가라.

### 스스로 점검

1. "20회 시행에서 충돌 0"이 안전의 증거로 불충분한 이유는?
2. 개입이 적은 것이 오히려 나쁜 HRI를 나타낼 수 있는 경우는?
3. 숙련 운용자와 일반 참가자를 함부로 합치면 안 되는 이유는?
4. "완전 자율 건설로봇"이라는 문구에 빠진 정보는?
5. §3.5 목표 추론 예제에서 믿음이 아직 0.5/0.5인데도 QMDP 로봇은 움직인다. 왜이고, QMDP가 결코 선호할 수 없는 행동은 어떤 종류인가?
6. 어떤 논문이 버킷이 다가오면 유도원이 물러선다는 Stackelberg 모델로 굴착기 선회를 계획하고 더 짧은 사이클을 보고한다. 무엇을 묻겠는가?

> [!tip]- 정답 · Answers
> 1. 노출이 작고 희귀 위험, 분포 이동, 심각도, 시스템 실패를 놓칠 수 있다. 숫자로 말하면: rule of three([[06-research-practice/experimental-design-reproducibility|실험 설계 §4]])에 따라 20회에서 실패 0이어도 실패율의 95% 신뢰 상한은 약 14%다(정확한 값. rule of three의 $3/20 = 15\%$는 $n \approx 30$ 미만에서 거칠다) — 일곱 번에 한 번꼴의 충돌이다.
> 2. 운용자가 위험을 놓치거나, 인터페이스를 불신하거나, 과부하이거나, 권한이 없을 때.
> 3. 숙련, 멘탈 모델, 속도, 작업 부하, 위험 반응이 다르다.
> 4. 과제, 운용 도메인, 인간 역할, 개입/리셋, 안전 폴백, 지속 시간, 실패 처리.
> 5. 가운데 이동은 두 목표가 공유하는 진척을 내기 때문에 어느 한 목표 쪽의 −4보다 나은 −3.5를 받고, 그래서 기다리기보다 움직이는 편이 낫다. QMDP는 한 단계 뒤에 목표가 드러난다고 가정하므로, 이득이 정보뿐인 행동(다음 명령을 더 분별력 있게 만드는 탐색)은 가치가 없다.
> 6. $R_H$가 어디서 왔고 운전자나 저자가 아니라 유도원으로 검증됐는가; 유도원이 물러서지 않으면(주의 분산, 현장 신참) 어떻게 되는가; §6의 이격·정지 기능이 모델과 독립적으로 성립하는가; 짧은 사이클이 밀어붙이는 기계에 작업자가 적응해서 얻은 것은 아닌가 — 그렇다면 안전 이득이 아니라 노출의 변화다.

### 과제 · Problem set

Tier B. 위의 **P2** 안전 셀 위에서 손으로 유도한다. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 문제가 바꾸는 숫자 말고는 셀이 그대로이고, $v_h = 1.6$ m/s, $T_s = 0.30$ s, $C = 0.20$ m, $Z_d = 0.10$ m, $Z_r = 0.05$ m는 끝까지 고정이다.

셀에 구매 결정이 하나 내려왔다. 새 사람 추적기는 더 싸고 0.1초 느려서 $T_{\text{sens}}$가 0.06초에서 0.16초로, $T_r$은 0.20초가 된다. 이를 보상하려고 통합 담당자가 로봇을 $v_r = 1.0$에서 $v_r = 0.6$ m/s로 늦추자고 제안한다.

1. **그리기.** 과제가 그릴 그림을 새 숫자로 다시 그려라: 위험 원, 감지 영역 원, 접근선 위 여섯 선분을 축척에 맞게 그린 평면도와, $T_{\text{sens}}$·$T_r$·$T_r + T_s$에 눈금을 둔 아래 시계. 길이가 바뀌지 **않은** 세 선분을 표시하고, 시계 위에는 사람은 걷고 있지만 로봇 쪽에서는 아직 아무 운동도 시작되지 않은 구간을 표시하라.
2. **유도.** 새 숫자에서 $S_h$, $S_r$, $S_s$, $S_p$를 계산하고, 감지 영역이 이제 어느 반지름에서 시작해야 하는지 구하라. 그다음 세 민감도로부터, $T_r = 0.20$ s에서 로봇 속도가 살 수 있는 $S_p$ 감소의 최대치를 말하고, 통합 담당자의 보상이 성립하는지 판정하라.
3. **해석.** 담당자의 보고서에는 "속도 스케일링으로 필요한 이격을 줄여 기존 셀을 유지했다"고 적혀 있다. 이후 같은 시스템에 대한 논문이 속도 스케일링으로 셀을 0.5 m 줄였다고 주장한다. 민감도만 써서, 그 논문이 실제로 바꾼 양이 무엇인지 말하고, 보고된 $S_p$ 하나로는 여전히 알 수 없는 셀의 두 가지를 대라.

> [!tip]- 정답 · Solutions
> 1. 그림에서 $C$, $Z_d$, $Z_r$은 이전 길이 그대로여야 한다. 셋 다 안에 속도도 시간도 없으므로 바뀌지 않은 것이 이 셋이다. $S_h$는 눈에 띄게 길어지고 $S_s$는 눈에 띄게 짧아져야 한다. 시계에서 $t = 0$부터 $t = 0.20$ s까지가 로봇이 아직 제동을 시작하지 않은 채 사람이 걷는 구간이고, 그중 앞의 0.16초는 검출기만의 몫이다.
> 2. $S_h = 1.6(0.20 + 0.30) = 0.80$ m, $S_r = 0.6 \times 0.20 = 0.12$ m, $S_s = \tfrac{1}{2}(0.6)(0.30) = 0.09$ m, $S_p = 0.80 + 0.12 + 0.09 + 0.20 + 0.10 + 0.05 = 1.36$ m. 영역은 $2.25 + 1.36 = 3.61$ m에서 시작해야 한다. 보상은 실패하고, 보이는 것보다 더 크게 실패한다. 로봇이 속도의 40%를 내놓았는데도 $S_p$는 오히려 0.12 m **늘었다**. $T_r = 0.20$ s에서 민감도는 $\partial S_p/\partial v_r = 0.20 + 0.15 = 0.35$ s이고 $T_r$이 고정이면 $S_p$는 $v_r$에 선형이므로, 로봇의 1.0 m/s 전부로 살 수 있는 것은 최대 $0.35$ m($1.50 \to 1.15$ m)이고 제안된 0.6 m/s에서는 $0.35 \times 0.6 = 0.21$ m만 남는다. 1.24 m로 돌아가려면 $1.15 + 0.35\,v_r \le 1.24$, 곧 $v_r \le 0.26$ m/s여야 한다. 느려진 검출기의 값은 로봇 속도의 4분의 3을 내놓아야만 속도로 되갚을 수 있다.
> 3. $T_r$(더 빠른 검출기, 또는 더 짧은 제동 명령 경로)이나 $C$(신체를 더 일찍 감지하는 감지 영역, 곧 옷만 갈아입은 같은 주장)를 바꿨어야 한다. 속도로는 불가능하다. 속도 예산 전체가 $T_r = 0.10$ s에서 $0.25$ m, $T_r = 0.20$ s에서 $0.35$ m로 둘 다 0.5 m에 못 미친다. $S_p$ 하나로 여전히 알 수 없는 것: 셀이 실제로 멈추는지 — 검증된 정지 없이는 이격 기능이 아무 값도 하지 않으며, 그것이 §6의 monitored standstill과 비상 정지 장치다 — 그리고 그 변경이 사이클 타임으로 얼마를 치렀는지. 후자가 이격 결과를 정직하게 보고하는 방법이다.

### 출처


- 이 결정들이 딛고 선 인지 층: [[04-robotics/video-action-understanding|20. 비디오·행동 이해]], [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]], [[04-robotics/egocentric-perception|22. 자기중심 인지]], [[04-robotics/human-intent-prediction|23. 인간 의도·궤적 예측]] — 자율성과 권한은 결정이고, 그 페이지들이 그 결정의 근거다.
- S. Javdani, S. S. Srinivasa, and J. A. Bagnell, "Shared Autonomy via Hindsight Optimization," *Robotics: Science and Systems (RSS)*, 2015 — noisy-rational 사용자 모델로 목표 믿음을 세우고 QMDP 근사로 돕는다(§3.5).
- D. Sadigh, S. Sastry, S. A. Seshia, and A. Dragan, "Planning for Autonomous Cars that Leverage Effects on Human Actions," *RSS*, 2016 — Stackelberg 정식화와 암묵 미분 풀이(§3.5).
- D. Sadigh, S. Sastry, S. A. Seshia, and A. Dragan, "Information Gathering Actions over Human Internal State," *IEEE/RSJ IROS*, 2016; both combined in D. Sadigh et al., "Planning for cars that coordinate with people: leveraging effects on human actions for planning and active information gathering over human internal state," *Autonomous Robots* 42(7):1405–1426, 2018 — 믿음 엔트로피 감소를 로봇 보상에 넣는다(§3.5).
- [NIST Human-Robot Interaction](https://www.nist.gov/topics/human-robot-interaction)
- [NIST Robotics Test Methods](https://www.nist.gov/programs-projects/robotic-systems-smart-manufacturing-program)
- [ACM/IEEE International Conference on Human-Robot Interaction (HRI)](https://humanrobotinteraction.org/) — 분야 대표 학회; 인간 대상 연구 설계의 실제 기준을 보여주는 논문들
