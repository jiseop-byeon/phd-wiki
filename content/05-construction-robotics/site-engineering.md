---
title: 2.5 Site Robotics as an Engineering System
tags: [construction-robotics, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Turn one construction task into a traceable requirement, frame, uncertainty, safety, productivity, and evidence specification."
mastery-when: "Raise when the deployment workflow or field-evaluation method carries the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> Transforms and the frame chain from [[04-robotics/robot-systems-deployment|10. Robot Systems §4]]; the safety vocabulary and the counting rule from [[04-robotics/hri-safety|11. HRI & Safety §6]] and [[04-robotics/hri-safety|§2]]; variance, covariance and the Gaussian tail from [[02-foundations/probability|3. Probability §2]] and [[02-foundations/probability|§6]]; the evidence ladder from [[06-research-practice/real-world-impact|6. Real-World Impact §2]]; and trial design from [[06-research-practice/experimental-design-reproducibility|Experimental Design]].
> 변환과 좌표계 사슬은 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §4]], 안전 어휘와 집계 규칙은 [[04-robotics/hri-safety|11. HRI·안전 §6]]과 [[04-robotics/hri-safety|§2]], 분산·공분산과 가우시안 꼬리는 [[02-foundations/probability|3. 확률 §2]]와 [[02-foundations/probability|§6]], 증거 사다리는 [[06-research-practice/real-world-impact|6. 실세계 임팩트 §2]], 시행 설계는 [[06-research-practice/experimental-design-reproducibility|실험 설계]]에서 가져온다.

## English

> [!note] First pass · 처음이라면
> Read the Running object and look at the picture, then §1–§4 and the Worked case after §4: they turn S1 into a work package, an error budget, a safe state per phase and a time denominator, and put two numbers on each. Complete the requirement ledger of After reading before opening a stream page. §5 and §6 are for when you read a paper or choose a stream.

### Running object · 이 페이지의 대상

The construction track runs on two frozen site objects, both defined here and reused by the stream pages. They are course objects, not proposed products: their numbers exist to make every design claim testable, and no other page changes them.

**S1 — facade panel placement** (pages 2.5, 4, 5, 6, 7 and 9). A mobile manipulator picks a $20\,\mathrm{kg}$ facade panel from a rack, moves it $8\,\mathrm{m}$, aligns two mounting holes $400\,\mathrm{mm}$ apart within $\pm5\,\mathrm{mm}$, holds while a worker fastens it, and clears the area. People may enter the shared site, GNSS can be blocked, and the base is repositioned between panels.

| Symbol | Value | What it is |
|---|---:|---|
| $m$ | $20\,\mathrm{kg}$ | panel mass; its weight is $196\,\mathrm{N}$, which P2 would hold at its tip with $215.8\,\mathrm{N{\cdot}m}$ at the shoulder ([[02-foundations/basic-mechanics\|0.6.1 §8]]) |
| hole spacing | $400\,\mathrm{mm}$ | between the two mounting holes |
| tolerance | $\pm5\,\mathrm{mm}$ | hole residual allowed at alignment |
| transport | $8\,\mathrm{m}$ | rack to wall |
| error budget | map $1$, base $2$, arm $1$, tool $0.5$, part $1\,\mathrm{mm}$ | the allocation per source that §2 adds up |
| observed day | $8$ panels: $160\,\mathrm{min}$ of cycles, $20$ of setup, $15$ of resets, $5$ of rework | the work package §4 divides |

**S2 — trench excavation** (pages 3 and 7.5). A $5$-tonne-class compact excavator digs a utility trench $20\,\mathrm{m}$ long, $0.6\,\mathrm{m}$ wide and $1.0\,\mathrm{m}$ deep to a bottom grade of $\pm30\,\mathrm{mm}$, casting the spoil beside the trench while a worker checks depth at its far end.

| Symbol | Value | What it is |
|---|---:|---|
| $L_1,\ L_2,\ L_3$ | $2.5$, $1.3$, $0.6\,\mathrm{m}$ | boom, stick, and bucket from pin to tip |
| $w,\ V_b$ | $0.6\,\mathrm{m}$, $0.14\,\mathrm{m^3}$ | bucket width, equal to the trench width, and heaped capacity |
| $T_c$ | $16\,\mathrm{s}$ | one cycle: dig $6$, swing $4$, dump $2$, return $4\,\mathrm{s}$ |
| $k_f,\ s$ | $0.85$, $1.25$ | fill factor, and swell — loose volume over bank volume |
| $\gamma$ | $18\,\mathrm{kN/m^3}$ | the soil's unit weight in the bank |
| $k_c$ | $60\,\mathrm{kPa}$ | specific cutting resistance: cutting force per unit area of the slice's cross-section |
| $e_{\text{GNSS}},\ \Delta\theta$ | $20\,\mathrm{mm}$, $0.1^\circ$ | two-sigma vertical error of the cab's RTK receiver, and of each link's angle sensor |
| $\tau_h,\ v$ | $0.15\,\mathrm{s}$, $0.3\,\mathrm{m/s}$ | valve-to-motion latency, and bucket-tip speed on the finishing pass |

S2's soil and machine are course numbers, frozen rather than measured; a real site's soil has to be measured, which is the point of [[05-construction-robotics/sim-to-real|7.5]]. S1 is this page's object. S2 is introduced here so that the two pages that need a machine rather than a panel share one. Every number the Worked case uses is in the S1 table: this page freezes no numbers beyond these two tables.

*Scope: this page teaches how to turn one construction task into a specification — its work package, its frame chain and error budget, a safe state for each phase, a time denominator, and an evidence protocol — worked on S1. It does not teach how the base localizes ([[04-robotics/navigation-mobile-manipulation|16]]), how contact is controlled ([[04-robotics/force-compliance-control|13]]), or what the safety standards require ([[04-robotics/hri-safety|11. §6]]); it uses their vocabulary, and the stream pages routed in §6 take S1 and S2 further.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 310" style="max-width:100%;height:auto" role="img" aria-label="Top: S1's five error allocations stacked add to 5.5 mm, past the 5 mm tolerance line, while their root-sum-square is 2.69 mm, inside it. Bottom: S1's observed day as one 200-minute bar, 20 min setup, eight 20-minute cycles, 15 min resets and 5 min rework; 8 panels over the 160 minutes of cycles is 3.0 panels per hour, over the whole 200 minutes 2.4.">
<text x="20" y="20" font-size="12" fill="currentColor" font-weight="600">S1&#8217;s error budget, read two ways (mm)</text>
<text x="440.0" y="36" font-size="10.5" fill="currentColor" text-anchor="middle">tolerance &#177;5</text>
<rect x="40.0" y="56" width="80.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="80.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">map</text>
<text x="80.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<rect x="120.0" y="56" width="160.0" height="22" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-opacity="0.55"/>
<text x="200.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">base</text>
<text x="200.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">2</text>
<rect x="280.0" y="56" width="80.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="320.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">arm</text>
<text x="320.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<rect x="360.0" y="56" width="40.0" height="22" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-opacity="0.55"/>
<text x="380.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">tool</text>
<text x="380.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">0.5</text>
<rect x="400.0" y="56" width="80.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="420.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">part</text>
<text x="420.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<text x="40" y="94" font-size="11" fill="currentColor">linear: 1 + 2 + 1 + 0.5 + 1 = 5.5 mm, 0.5 over the tolerance</text>
<rect x="40" y="102" width="215.4" height="22" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-opacity="0.55"/>
<text x="147.7" y="117" font-size="10.5" fill="currentColor" text-anchor="middle">2.69</text>
<text x="40" y="140" font-size="11" fill="currentColor">root-sum-square: &#8730;7.25 = 2.69 mm, 2.31 inside the tolerance</text>
<line x1="440.0" y1="42" x2="440.0" y2="128" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>
<line x1="40" y1="150" x2="520.0" y2="150" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="40.0" y1="150" x2="40.0" y2="154" stroke="currentColor"/><text x="40.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="120.0" y1="150" x2="120.0" y2="154" stroke="currentColor"/><text x="120.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<line x1="200.0" y1="150" x2="200.0" y2="154" stroke="currentColor"/><text x="200.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">2</text>
<line x1="280.0" y1="150" x2="280.0" y2="154" stroke="currentColor"/><text x="280.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">3</text>
<line x1="360.0" y1="150" x2="360.0" y2="154" stroke="currentColor"/><text x="360.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">4</text>
<line x1="440.0" y1="150" x2="440.0" y2="154" stroke="currentColor"/><text x="440.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">5</text>
<line x1="520.0" y1="150" x2="520.0" y2="154" stroke="currentColor"/><text x="520.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">6</text>
<text x="20" y="192" font-size="12" fill="currentColor" font-weight="600">S1&#8217;s observed day (min)</text>
<rect x="40.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-opacity="0.55"/>
<text x="64.0" y="215" font-size="10" fill="currentColor" text-anchor="middle">setup</text>
<rect x="88.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="112.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="136.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="160.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="184.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="208.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="232.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="256.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="280.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="304.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="328.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="352.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="376.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="400.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="424.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="448.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="472.0" y="200" width="36.0" height="22" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-opacity="0.55"/>
<text x="490.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">15</text>
<rect x="508.0" y="200" width="12.0" height="22" fill="currentColor" fill-opacity="0.6" stroke="currentColor" stroke-opacity="0.55"/>
<text x="514.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">5</text>
<text x="490.0" y="195" font-size="10" fill="currentColor" text-anchor="end">resets, rework</text>
<line x1="490.0" y1="197" x2="490.0" y2="200" stroke="currentColor"/>
<text x="280.0" y="195" font-size="10" fill="currentColor" text-anchor="middle">eight cycles of 20</text>
<line x1="40" y1="228" x2="520.0" y2="228" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="40.0" y1="228" x2="40.0" y2="232" stroke="currentColor"/><text x="40.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="160.0" y1="228" x2="160.0" y2="232" stroke="currentColor"/><text x="160.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">50</text>
<line x1="280.0" y1="228" x2="280.0" y2="232" stroke="currentColor"/><text x="280.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">100</text>
<line x1="400.0" y1="228" x2="400.0" y2="232" stroke="currentColor"/><text x="400.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">150</text>
<line x1="520.0" y1="228" x2="520.0" y2="232" stroke="currentColor"/><text x="520.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">200</text>
<path d="M88.0 257V262H472.0V257" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="276" font-size="11" fill="currentColor" text-anchor="middle">cycles only: 8 panels in 160 min = 3.0 panels/h</text>
<path d="M40.0 285V290H520.0V285" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="304" font-size="11" fill="currentColor" text-anchor="middle">whole day: 8 panels in 200 min = 2.4 panels/h</text>
</svg>

S1 drawn from its own numbers. Top: the five allocations stacked end to end add to $5.5\,\mathrm{mm}$, past the $\pm5\,\mathrm{mm}$ tolerance, while their root-sum-square is $2.69\,\mathrm{mm}$, inside it with $2.31$ to spare; which bar is right depends on whether the errors are independent and zero-mean (§2). Bottom: the observed day, $200$ minutes for $8$ panels — $3.0$ panels/h counted over the $160$ minutes of cycles, $2.4$ over the whole day (§4).

### 1. Begin with the work package, not the robot

Write the unit of production, start and end states, tolerances, cycle-time target, predecessors, successors, and responsibility boundaries. “Install panels autonomously” hides at least five phases — acquire, transport, align (which begins by localizing against the structure), hold/fasten, and verify (which ends in release) — and each has a different dominant failure.

| Phase | Required evidence | Dominant uncertainty | Safe fallback |
|---|---|---|---|
| acquire | stable grasp and payload margin | panel pose, suction/contact | lower and regrasp |
| transport | collision-free base motion | people, terrain, localization | controlled stop |
| align | hole residual $\le5$ mm | base/arm/frame error | retreat and rescan |
| hold/fasten | force and pose inside envelope | worker action, compliance | freeze or yield |
| verify | fastener/pose completion record | sensor observability | request inspection |

Those seven items, grouped, are the definition this section turns on.

> **Work package, defined.** A **work package** is a *contract for one unit of production*, written before a robot is chosen. Five defining conditions. Its **unit** is countable: one panel installed, not "facade work". Its **start and end states** are physical and checkable. Its **acceptance test** names a tolerance and the frame it is measured in. Its **time target** carries a denominator (§4). And its **boundaries** name what must be done before, what follows, and who owns each hand-off.
>
> $$\mathcal W=(u,\ s_0,\ s_f,\ \mathrm{acc},\ T^\ast,\ \mathcal B)$$
>
> where $u$ is the unit, $s_0$ and $s_f$ the start and end states, $\mathrm{acc}$ the acceptance test, $T^\ast$ the time target with its denominator, and $\mathcal B$ the boundaries; it is written as a tuple because a claim about a robot is a claim about one of these six entries, so each must exist before the claim can be checked.
>
> - **Example**: S1. $u$ is one panel; $s_0$ the $20\,\mathrm{kg}$ panel on its rack, $8\,\mathrm{m}$ from the wall; $s_f$ the panel fastened with both holes within $\pm5\,\mathrm{mm}$ and the area clear; $\mathrm{acc}$ the two hole residuals in the structure's frame (§2); $T^\ast$ a rate per hour of the whole day, not of the cycle (§4); $\mathcal B$ the brackets set and surveyed before, a worker fastening during hold, inspection after.
> - **Non-example**: "install panels autonomously". It has no count, no end state, no tolerance and no owner, so no experiment can contradict it, and it quietly assigns the survey, the fastening and the inspection to nobody.
> - **Why it matters**: each later section fills one entry. §2 makes $\mathrm{acc}$ checkable, §3 gives every phase between $s_0$ and $s_f$ a safe state, §4 supplies the denominator of $T^\ast$, and §5 says under what conditions the units were observed.

### 2. Close the frame and error budget

*In one sentence:* the tool-to-target error is a sum of one error per link of the frame chain, and whether those errors add like lengths or like variances is an assumption the budget has to state.

The tool-to-target error is not one sensor number. S1's hole reaches its target through a chain of five transforms in the sense of [[04-robotics/robot-systems-deployment|10. Robot Systems §4]]: the design model tied to the site map (map), the map to the mobile base (base), the base to the arm's flange (arm), the flange to the gripper (tool), and the gripper to the hole in the panel (part). Linearized about the nominal chain, the hole's displacement is the sum of the displacements each link's small error causes at the hole; a rotation error enters multiplied by its distance to the hole, which is why an allocation is written at the hole rather than at the link. So a first-order conservative budget can be recorded as

$$e_{\text{total}}\lesssim e_{\text{map}}+e_{\text{base}}+e_{\text{arm}}+e_{\text{tool}}+e_{\text{part}}.$$

If S1 allocates 1, 2, 1, 0.5, and 1 mm, the sum is 5.5 mm—already over tolerance. Root-sum-square would give $\sqrt{7.25}=2.69$ mm only under approximately independent zero-mean errors. The choice is an assumption to defend, not arithmetic decoration.

**Where the two readings come from.** Both start from the sum $e=\sum_i e_i$. If every $|e_i|\le a_i$ is a hard bound, the triangle inequality gives $|e|\le\sum_i a_i$ whatever the signs and correlations: the linear reading. If instead the $e_i$ are random with zero mean and standard deviations $\sigma_i$, the variance of the sum is $\sum_i\sigma_i^2+2\sum_{i<j}\operatorname{Cov}(e_i,e_j)$ ([[02-foundations/probability|3. Probability §2]]), so variances add only once the covariances vanish; and if every allocation is the same multiple $k$ of its own $\sigma_i$, then $k\,\sigma_{\text{total}}=\sqrt{\sum_i a_i^2}$. That is the root-sum-square reading, with both of its assumptions in view.

> **Error budget, defined.** An **error budget** is a *specification*, not a measurement: one allocation per error source along the frame chain from the reference to the feature that must meet a tolerance, plus a rule that combines the allocations into a total compared with that tolerance. Four defining conditions. It is **complete**: every link has a term, since a missing term stays invisible until a part misses. It is **commensurable**: every allocation is a displacement at the feature, along the tolerance's direction, with one meaning — all hard bounds, or all the same multiple $k$ of their standard deviations. It **names its rule and the rule's assumption**: linear needs only that each bound holds, root-sum-square needs zero-mean, uncorrelated errors. And it is **closed**: the total is compared with the tolerance and the margin written down.
>
> $$e_{\text{lin}}=\sum_{i=1}^{N}a_i\ \ \ge\ \ e_{\text{RSS}}=\sqrt{\sum_{i=1}^{N}a_i^2}$$
>
> where $a_i\ge0$ is the allocation of source $i$ and $N$ the number of sources; the linear total can never be the smaller, because squaring $\sum_i a_i$ adds the non-negative cross terms $2\sum_{i<j}a_ia_j$ to $\sum_i a_i^2$.
>
> - **Example**: S1, $a=(1,2,1,0.5,1)$ mm: $e_{\text{lin}}=5.5$ mm, $0.5$ over the tolerance; $e_{\text{RSS}}=2.69$ mm, $2.31$ inside it. The base term is $4/7.25=55\%$ of the root-sum-square variance, so it is the term to buy down.
> - **Non-example**: root-sum-square over a bias. If the map term is a survey offset, the same $1$ mm on every panel, it does not average against the others but shifts them all: $1+\sqrt{4+1+0.25+1}=3.5$ mm, not $2.69$. Correlation fails the same way: if map and base errors come from one survey and move together, they add first, $\sqrt{(1+2)^2+1+0.25+1}=3.35$ mm.
> - **Why it matters**: the rule decides the verdict. Read linearly, S1 as specified cannot promise $\pm5$ mm; by root-sum-square it can, with room left for a larger base error. A budget reported as one number without its rule has not said which of the two its authors believe.

Every transform must name source, target, update rate, timestamp, and calibration owner. The timestamp is part of the error: on a base moving at $0.5$ m/s each millisecond of stamp error is $0.5$ mm at the hole, so the base's $2$ mm leaves the whole rig $4$ ms of unexplained time, priced sensor by sensor in [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §9]]. A BIM frame with no measured tie to the robot frame is not a robot command.

### 3. Safety is a system state

*In one sentence:* a safe state is a condition of the whole work system, chosen per phase, reachable in time and independent of whatever failed, so a safety architecture is a list of such states, one per phase, not a single stop button.

Separate hazard (what can cause harm), risk (severity and likelihood/exposure), safeguard, monitored variable, and safe state. Hazard, risk and the stop functions that lead to a safe state are the vocabulary of [[04-robotics/hri-safety|11. HRI & Safety §6]]; a safeguard is any measure that reduces a risk; the monitored variable and the safe state are this section's. An emergency stop is not the whole safety architecture: normal protective stops, speed/force limits, exclusion zones, human authority, restart conditions, and failure of the safety sensor all need ownership.

The last column of §1's table is S1's list of safe states, one per phase, and reading it as a list is the point: which state is safe depends on what the system is doing. For each phase the specification also names the **monitored variable** whose value triggers the move into that state — suction pressure or the payload estimate while acquiring, a person's distance while transporting, both hole residuals while aligning, contact force and pose while holding, the fastening record while verifying — and who may lead the system out of it again. How long the suction pressure holds once the pump stops — four cups at a safety factor of $4.8$ keep the required $2$ for $41$ s — is [[02-foundations/fluid-power|0.6.3 Fluid Power §9–§10]].

> **Safe state, defined.** A **safe state** is a *state of the whole work system in one phase* — robot, payload, people and site together — not a button, a command, or a property of the robot alone. Four defining conditions. It **bounds the phase's hazards**: nothing powered moves toward a person, and the payload is supported. It is **reachable in time** from anywhere in the phase. It **does not rely on the failed function**: it holds without the sensor, power or software whose failure sent the system there. And it is **left deliberately**: leaving it needs a stated restart condition and a person with the authority to give it.
>
> $$T_{\text{detect}}+T_{\text{react}}+T_{\text{enter}}\le T_{\text{harm}}$$
>
> writes out the second condition, where $T_{\text{detect}}$ runs from the hazard's onset to its detection by the monitored variable, $T_{\text{react}}$ from detection to the command, $T_{\text{enter}}$ from the command until the state is reached, and $T_{\text{harm}}$ from onset until harm would occur; the delays add because they happen one after another, so the protective separation distance of 11 §6 is this budget written in metres, with the robot's own travel and the sensing uncertainties added.
>
> - **Example**: S1 in hold/fasten, a worker's hands at the panel. The safe state is *freeze*: joint brakes set, no powered motion, the $196\,\mathrm{N}$ panel carried by the brakes rather than the servo loop — so it still holds if servo power is lost, the third condition — and left only when the worker steps back and releases it.
> - **Non-example**: *retreat and rescan*. It is align's safe state, where no one is at the panel and a miss costs only time; in hold/fasten it would drag a half-fastened panel away through the worker's hands. An emergency stop is a second non-example: it is a transition, and whether it ends in a safe state depends on what holds the load once power is cut.
> - **Why it matters**: a safety architecture is this list — one state per phase, each with its monitored variable and restart rule. A single stop for every phase assumes that every phase has the same safe state, which S1's table shows is false.

**The time condition in numbers.** Borrow the P2 cell of 11's worked case, whose reaction time splits exactly into the first two terms: $T_{\text{detect}}=0.06$ s from a body entering the sensing field to the tracker's report, $T_{\text{react}}=0.04$ s for the decision and the brake command, and $T_{\text{enter}}=0.30$ s to stop. A worker walking at the standard $1.6$ m/s closes $1.6\times(0.06+0.04+0.30)=0.64$ m in those $0.40$ s, so that cell's distance monitor has to trip while a person is still more than $0.64$ m away, before the robot's own travel and the sensing uncertainties are added. That is the $S_h$ term of 11 §6, reached from the safe-state side. S1's base stops more slowly with the $20$ kg panel on the arm: [[05-construction-robotics/hrc-worker-centered|6. HRC]] freezes $T_s=0.40$ s for it, which makes the same term $1.6\times(0.10+0.40)=0.80$ m. The budget has to be written with the stopping time measured on the machine that will run.

Do not infer certification from experimental success. A research paper can establish performance under stated safeguards; compliance claims require the applicable standards and an accountable assessment process.

### 4. Productivity needs a denominator

For $n$ completed units over observed time $T$, throughput is $n/T$, but deployment comparison also needs setup, calibration, supervision, resets, rework, and downtime. For S1 the denominator is the sum of every interval the work package paid for, since none of them was free:

$$T_{\text{effective}}=T_{\text{setup}}+\sum_i(T_{\text{cycle},i}+T_{\text{reset},i}+T_{\text{rework},i})+T_{\text{down}}.$$

If 8 panels take 160 min of cycles, 20 min setup, 15 min resets, and 5 min rework, headline cycle throughput is 3 panels/h while effective throughput is $8/200\times60=2.4$ panels/h. Both numbers are true; only the latter describes the observed work package.

The terms of that sum are not alike. Setup is paid once per work package, however many panels follow it; cycles, resets and rework are paid again with every panel, since misses and defects arrive panel by panel; downtime is paid per event. That split decides whether a longer day helps, which the Worked case below computes. Report the people-time beside the rate as well: a supervisor present for the whole day adds $200$ min of attention to $8$ panels, $25$ min per panel, which no cycle time shows.

> **Effective throughput, defined.** **Effective throughput** is a *rate*: accepted units per unit of the whole observed time of a work package. Four defining conditions. The **numerator counts accepted units only** — a panel that failed acceptance and was reworked counts once, when it finally passes. The **denominator is the whole observed interval**: setup, every cycle, reset and rework, and all downtime, with nothing dropped because it was not the robot's fault. **Both come from one window**, so a good hour is never divided into a whole day's count. And the **window is stated** — its length and how many setups it spans — because the fixed overheads are spread over it.
>
> $$\eta_{\text{eff}}=\frac{n_{\text{acc}}}{T_{\text{effective}}}$$
>
> where $n_{\text{acc}}$ is the number of units that passed the work package's acceptance test inside the window and $T_{\text{effective}}$ is the sum above over the same window, so numerator and denominator count the same minutes.
>
> - **Example**: S1's day, $8$ accepted panels over $200$ min: $\eta_{\text{eff}}=2.4$ panels/h, $25$ min per panel.
> - **Non-example**: the cycle throughput, $8$ panels over the $160$ min of cycles, $3.0$ panels/h. It is true and useful for tuning motion, but it covers $160$ of the day's $200$ minutes; quoted as the work package's productivity it overstates it by a quarter, $3.0/2.4=1.25$.
> - **Why it matters**: a construction robot competes with a crew's day, not with a crew's fastest cycle, and the gap between the two rates — setup, resets, rework, downtime — is work people do around the robot, which is where a deployment is won or lost.

### Worked case · 대상으로 한 번 끝까지

Six steps on S1's own numbers: the budget read both ways, what the root-sum-square number means at two confidence multiples, then the day read both ways and carried to the question a site manager asks — would a longer day help? They are course computations on a frozen object, not measurements of a machine or a site.

**Step 1 — the budget as a worst case.** $e_{\text{lin}}=1+2+1+0.5+1=5.5\,\mathrm{mm}$ against a $5\,\mathrm{mm}$ tolerance: $0.5\,\mathrm{mm}$ over. If the five allocations are hard bounds and nothing stops the errors lining up, S1 as specified cannot promise its tolerance, and no amount of testing changes that; only a smaller allocation does.

**Step 2 — the budget as independent zero-mean errors.** $e_{\text{RSS}}=\sqrt{1+4+1+0.25+1}=\sqrt{7.25}=2.69\,\mathrm{mm}$, inside the tolerance with $5-2.69=2.31\,\mathrm{mm}$ to spare, $46\%$ of it. The variance shares are base $4/7.25=55\%$, map, arm and part $1/7.25=14\%$ each, and tool $0.25/7.25=3\%$. Halving the base term takes the total to $\sqrt{4.25}=2.06\,\mathrm{mm}$; removing the tool term altogether only to $\sqrt{7}=2.65\,\mathrm{mm}$.

**Step 3 — what 2.69 mm means depends on $k$.** An allocation is a bound only together with its multiple $k$ of its own standard deviation. If each is a two-sigma bound — the reading [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] later adopts at the pin — the combined standard deviation is $\sigma=2.693/2=1.346\,\mathrm{mm}$ and the tolerance sits at $5/1.346=3.714\,\sigma$. For Gaussian errors the chance that a hole misses on one axis is then

$$P(|e|>5\,\mathrm{mm})=2\,Q(3.714)=2.0\times10^{-4}$$

since both tails count, where $Q$ is the Gaussian upper tail of [[02-foundations/probability|3. Probability §6]]: about one hole-axis in $4{,}900$. Read as one-sigma values, the same numbers give $\sigma=2.693\,\mathrm{mm}$, a tolerance at $1.857\,\sigma$, and $2\,Q(1.857)=0.063$, about one in $16$ — $310$ times as often. Five allocations without their $k$ do not yet say how often align must retreat.

**Step 4 — the day, per cycle.** $8$ panels in $160$ min of cycles: $8/160\times60=3.0$ panels/h, $20$ min per panel.

**Step 5 — the day, effective.** $T_{\text{effective}}=20+160+15+5+0=200$ min, with no downtime that day, so $\eta_{\text{eff}}=8/200\times60=2.4$ panels/h, $25$ min per panel. The overheads come to $40$ min, $20\%$ of the day, and the effective rate is $0.8$ of the cycle rate.

**Step 6 — carried through: would a longer day help?** Setup is paid once; suppose resets and rework recur per panel at the day's average, $(15+5)/8=2.5$ min. Then $n$ panels after one setup take $20+(20+2.5)\,n$ minutes, so

$$\eta_{\text{eff}}(n)=\frac{60\,n}{20+22.5\,n}\ \text{panels/h}$$

which is $2.4$ at $n=8$, $2.53$ at $n=16$, and approaches $60/22.5=2.67$ panels/h as $n$ grows. No length of day reaches the headline $3.0$: setup dilutes, resets and rework do not. Even approaching $3.0$ needs the per-panel total down to $20$ min — a $17.5$ min cycle with today's resets and rework, or today's cycle with none — and Step 3 bounds how often align itself must retreat and rescan, time that lands in the cycle or the reset column according to §5's counting rule: at $k=1$ one hole-axis in $16$ misses, and a panel has four hole-axes; at $k=2$, one in $4{,}900$.

### 5. Evidence ladder

Simulation tests algorithms and rare conditions; laboratory tests real sensing/contact under arranged conditions; mock-up tests scale and workflow; active site tests integration with changing work and people. A higher rung does not repair a weak protocol. At every rung define episode, success, intervention, reset, failure taxonomy, variation, and baseline.

The rungs, and the sentence each licenses, are laid out in [[06-research-practice/real-world-impact|6. Real-World Impact §2]], and a rung is defined completely in that page's Worked case: it is set by the conditions in the methods section, not by the words in the abstract. What this page adds is what S1 has to show on each rung, and it follows from §2, because each rung turns a different set of the budget's terms from assumptions into measurements.

| Rung | S1's budget terms measured there rather than assumed |
|---|---|
| simulation | none: all five allocations are inputs, so the rung tests the align decision, not the tolerance |
| laboratory | arm, tool and part on real hardware; map and base only against fixed targets the lab arranged |
| full-scale mock-up | the same, now with a full-size panel, real brackets, and the base re-placed between panels |
| active site | map and base against a structure that changes as it is built, with people and weather: the only rung where all five are measured |

Weighted by §2's budget, the laboratory rung measures the arm, tool and part terms, $(1+0.25+1)/7.25=31\%$ of S1's root-sum-square variance; the map and base terms, the other $69\%$, are measured against a changing structure only on an active site. That is the arithmetic behind the warning that a mock-up result does not transfer on its own.

The seven protocol items, written for S1 before the first trial:

| Item | S1's version |
|---|---|
| episode | one panel, from the grasp at the rack to release with the robot clear |
| success | both holes within $\pm5$ mm in the structure's frame at release, and fastened |
| intervention | any human action that changes the robot's state or the panel's pose during an episode |
| reset | returning panel and robot to a start state after a failed episode, timed and charged to §4's denominator |
| failure taxonomy | the phase of §1's table in which the first failure occurred |
| variation | panels, rack slots, base poses, bracket surveys, people nearby, light and weather, each with its range |
| baseline | a crew's rate on the same panels, per day (§4), not per cycle |

Whether an episode an operator rescued counts as a success is decided here too, before any run is watched ([[04-robotics/hri-safety|11. §2]]); a success rate without its counting rule is not yet a number.

### 6. Route into the domain

After S1 is specified, choose the matching stream: [[05-construction-robotics/earthmoving-heavy-machinery|earthmoving]], [[05-construction-robotics/assembly-fabrication|assembly]], [[05-construction-robotics/site-perception|site perception]], [[05-construction-robotics/hrc-worker-centered|HRC]], or [[05-construction-robotics/digital-twin-workflows|digital twins]]. Use [[05-construction-robotics/sim-to-real|sim-to-real]] and [[05-construction-robotics/industry-deployment|deployment]] as cross-cutting layers, not substitute topics.

Each stream takes one part of this page further on the same frozen objects, and a page that needs more numbers than S1 or S2 gives freezes its own and says so. Read against §2, the pages divide S1's sum of squared allocations, $7.25\,\mathrm{mm^2}$: the map term ($1$) sits with the design model and its registration to the site (7 and 5), the base term ($4$) with localization and base placement ([[04-robotics/navigation-mobile-manipulation|16]]), the arm and tool terms ($1$ and $0.25$) with the manipulator (4 and 9), and the part term ($1$) with fabrication tolerance (4). Choose by the question, not by the machine:

| If the question is about | Object | Stream |
|---|---|---|
| the two holes as a pair: translate, yaw or retreat | S1 | [[05-construction-robotics/assembly-fabrication\|4. Assembly & Fabrication]] |
| scanning and registering the as-built structure, which §2's map term rests on | S1 | [[05-construction-robotics/site-perception\|5. Site Perception]] |
| people in the shared site, and the phases with a worker at the panel | S1 | [[05-construction-robotics/hrc-worker-centered\|6. HRC]] |
| the design model behind the map term, and tasks generated from it | S1 | [[05-construction-robotics/digital-twin-workflows\|7. Digital Twins]] |
| the hole meeting its pin: capture and contact force | S1 | [[05-construction-robotics/construction-manipulation\|9. Construction Manipulation]] |
| digging to grade with a compact excavator | S2 | [[05-construction-robotics/earthmoving-heavy-machinery\|3. Earthmoving]] |
| what a simulator must match before its numbers transfer | S2 | [[05-construction-robotics/sim-to-real\|7.5 Sim-to-Real]] |
| who sells what, at which autonomy level | both | [[05-construction-robotics/industry-deployment\|8. Industry & Deployment]] |

### After reading

- [ ] Write any construction task as a work package: unit, start and end states, acceptance test, time target with its denominator, and boundaries.
- [ ] Build an error budget along the frame chain, combine it both ways, and state the assumption each way needs, including the multiple $k$.
- [ ] Name the safe state of each phase and check it against the four conditions.
- [ ] Compute a work package's cycle and effective throughput, and say which overheads a longer day dilutes.
- [ ] Place a result on the evidence ladder, say which budget terms its rung measured, and fix the seven protocol items before the first trial.
- [ ] For any construction-robotics claim, produce a one-page ledger of work unit, tolerances, frames, uncertainty, people/authority, safety state, time denominator, intervention/reset, evidence rung, and failure taxonomy.

### Self-check

1. Why can the linear total of an error budget never be smaller than its root-sum-square total, and when are the two equal?
2. S1's map term turns out to be a survey offset, the same $1$ mm on every panel. How does it enter the budget, and what total results?
3. Why is *retreat and rescan* a safe state for align but not for hold/fasten?
4. For each of S1's five phases, name its safe state and the monitored variable that triggers it, and say which actors a drawing of the phases must show.
5. A vendor quotes "20 minutes per panel". What do you ask before comparing it with a crew?
6. A report calls a full-scale mock-up result "validated for site deployment". Which rung is it on, which sentence does it license, and which of S1's budget terms has it not measured?

> [!tip]- Answers
> 1. Squaring the linear total gives $\sum_i a_i^2+2\sum_{i<j}a_ia_j$, and the cross terms are non-negative because every allocation is; they vanish only when at most one allocation is non-zero, so the totals are equal only for a single-source budget. For S1 they are $5.5$ and $2.69$ mm.
> 2. Linearly, because a bias does not average against the random terms: $1+\sqrt{4+1+0.25+1}=1+2.5=3.5$ mm. That is still inside $\pm5$ mm, but $0.81$ mm above the all-root-sum-square $2.69$, and the margin shrinks from $2.31$ to $1.5$ mm.
> 3. In align no one is at the panel and a miss costs only time, so backing away and measuring again bounds the hazard. In hold/fasten a worker's hands are at the panel and a bolt may be half in; moving the panel away would drag it through the worker's hands. Hold/fasten's safe state is freeze with the brakes set, which holds the panel without the servo loop.
> 4. Acquire: lower and regrasp, on suction pressure or the payload estimate. Transport: controlled stop, on a person's distance or lost localization. Align: retreat and rescan, when the two hole residuals show that no correction available to the robot brings both holes inside $\pm5$ mm, or the scan cannot be trusted. Hold/fasten: freeze or yield, on contact force or pose leaving its envelope. Verify: request inspection, on a missing or unobservable fastening record. The drawing must show the worker, supervisor, robot, target/BIM, perception, controller, and the stop and recovery paths — not only the nominal robot arrows.
> 5. Whether it is a cycle time or an effective one — which of setup, resets, rework and downtime it includes — over what window and how many panels, and how much supervision the robot needed. For S1, 20 min is the cycle; the whole day gives 25.
> 6. The full-scale mock-up rung, which licenses "it survives realistic geometry and scale", not "it survived conditions I did not choose". It has not measured the map and base terms against a structure that changes as it is built, and those two carry $(1+4)/7.25=69\%$ of S1's root-sum-square variance.

### Problem set · 과제

Tier B. S1 from the Running object, worked by hand; no simulator and no code.

1. **Draw.** The picture for S1 on a harder site and a longer day: the base term grown to $3\,\mathrm{mm}$ with the other four unchanged, and the 20-panel day of item 2(c). Show both budget bars against the tolerance, and the day as one bar with its cycle-only and whole-day rates.
2. **Derive.** (a) With the base term at $3\,\mathrm{mm}$: the linear and root-sum-square totals, the margin, the base term's share of the variance, and the one-axis miss probability if every allocation is a two-sigma bound. (b) The largest base term for which the root-sum-square total still meets $\pm5\,\mathrm{mm}$, and the largest for which the linear total does. (c) A 20-panel day with $18$ min cycles, $30$ min setup, one $12$ min reset every four panels, and rework on $10\%$ of panels at $9$ min each: the effective time, and the effective and cycle-only throughput. (d) The limit of (c)'s effective rate as the day grows, with setup paid once and resets and rework per panel.
3. **Interpret.** A paper reports "95% success over 20 attempts" for a panel-installation robot on one indoor mock-up with manual resets. (a) Place it on the ladder and write the sentence it licenses. (b) State three claims it cannot yet support. (c) If three of its 19 successes were finished after an operator took over, what is the autonomous success rate under a rule that ends an episode at its first intervention? (d) Which of §5's seven protocol items must the paper state before its 95% means anything?

> [!note]- How to draw it · 그리는 법
> - **Top, a millimetre axis from 0 to 7**: the stacked allocations $1, 3, 1, 0.5, 1$ ($6.5\,\mathrm{mm}$), the root-sum-square bar at $\sqrt{12.25}=3.50\,\mathrm{mm}$, and the tolerance line at $5\,\mathrm{mm}$; mark the linear overshoot ($1.5\,\mathrm{mm}$) and the root-sum-square margin ($1.5\,\mathrm{mm}$).
> - **Bottom, a minute axis from 0 to 500**: setup $30$, twenty cycles of $18$ ($360$), resets $5\times12=60$, rework $2\times9=18$ — $468$ min in all. Bracket the cycles "20 panels in 360 min = 3.33 panels/h" and the whole bar "20 panels in 468 min = 2.56 panels/h".
> - **Keep both axes linear and starting at zero**: a broken axis hides exactly the overheads the picture exists to show.
> - The drawing is wrong if the root-sum-square bar is drawn at $12.25$, the sum of squares, instead of its square root, or if the day's bar leaves out the resets because no panel was installed during them.

> [!tip]- Solutions
> 1. As in the How-to-draw list: $6.5$ and $3.50\,\mathrm{mm}$ against $5$; $468$ min; $3.33$ and $2.56$ panels/h.
> 2. (a) $1+3+1+0.5+1=6.5\,\mathrm{mm}$, $1.5$ over; $\sqrt{1+9+1+0.25+1}=\sqrt{12.25}=3.50\,\mathrm{mm}$, margin $1.50$; base share $9/12.25=73\%$; $\sigma=3.50/2=1.75\,\mathrm{mm}$, the tolerance at $5/1.75=2.857\,\sigma$, and $2\,Q(2.857)=0.0043$, about one hole-axis in $234$ — twenty-one times the $2.0\times10^{-4}$ of the $2\,\mathrm{mm}$ base. (b) Root-sum-square: $\sqrt{25-3.25}=\sqrt{21.75}=4.66\,\mathrm{mm}$; linear: $5-3.5=1.5\,\mathrm{mm}$. (c) Cycles $360$ + setup $30$ + resets $5\times12=60$ + expected rework $2\times9=18$: $468$ min, so $20/(468/60)=2.56$ panels/h, against $20/(360/60)=3.33$ panels/h over the cycles alone. (d) Per panel $18+12/4+0.1\times9=21.9$ min, so the rate approaches $60/21.9=2.74$ panels/h.
> 3. (a) The full-scale mock-up rung at best, licensing "it survives realistic geometry and scale"; if the mock-up is not full scale, the laboratory rung, licensing "it works on real hardware, in my conditions". (b) Examples: active-site robustness, low-intervention autonomy (the resets were manual), cross-site generalization, weather tolerance, or competitive productivity (no denominator and no baseline). (c) $(19-3)/20=16/20=80\%$. (d) All seven, and above all the counting rule for interventions, what success was measured on (the holes in the structure's frame, or the robot's pose), what each reset cost in time, and the baseline.

### Sources

S1, S2 and every number in the Worked case are course values defined on this page; nothing here reports a measurement of a real machine or site.

**Within this wiki**

- [[02-foundations/probability|3. Probability §2]] — variance, covariance and the variance of a sum, behind §2's root-sum-square; [[02-foundations/probability|§6]] — the Gaussian tail $Q$ of the Worked case.
- [[04-robotics/robot-systems-deployment|10. Robot Systems §4]] — transforms and the frame chain of §2.
- [[04-robotics/hri-safety|11. HRI & Safety §6]] — the safety vocabulary and standards §3 builds on; [[04-robotics/hri-safety|§2]] — the counting rule of §5.
- [[06-research-practice/real-world-impact|6. Real-World Impact §2]] — the evidence ladder that §5 applies to S1; the definition of a rung is in that page's Worked case.

## 한국어

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고 그림을 본 뒤, §1–§4와 §4 뒤의 계산 절을 읽는다. 이 부분이 S1을 작업 묶음, 오차 예산, 단계마다의 안전 상태, 시간 분모로 바꾸고 각각에 숫자 둘을 붙인다. 스트림 페이지를 열기 전에 읽고 나면 절의 요구사항 장부를 채운다. §5와 §6은 논문을 읽거나 스트림을 고를 때 본다.

### 이 페이지의 대상 · Running object

건설 트랙은 고정된 현장 대상 둘로 돌아간다. 둘 다 여기서 정의하고 스트림 페이지들이 다시 쓴다. 제품 제안이 아니라 교과 대상이다. 숫자는 모든 설계 주장을 검사할 수 있게 하려고 있고, 다른 페이지는 이 숫자를 바꾸지 않는다.

**S1 — 외장 패널 설치**(2.5, 4, 5, 6, 7, 9번 페이지). 모바일 매니퓰레이터가 $20\,\mathrm{kg}$ 외장 패널을 거치대에서 집어 $8\,\mathrm{m}$ 옮기고, $400\,\mathrm{mm}$ 떨어진 두 체결 구멍을 $\pm5\,\mathrm{mm}$ 안에 맞추고, 작업자가 체결하는 동안 들고 있다가 구역을 비운다. 공유 현장에는 사람이 들어올 수 있고, GNSS는 가려질 수 있으며, 패널마다 베이스가 자리를 옮긴다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $m$ | $20\,\mathrm{kg}$ | 패널 질량. 무게는 $196\,\mathrm{N}$이고, P2가 말단에서 그것을 들면 어깨에 $215.8\,\mathrm{N{\cdot}m}$가 든다([[02-foundations/basic-mechanics\|0.6.1 §8]]) |
| 구멍 간격 | $400\,\mathrm{mm}$ | 두 체결 구멍 사이 |
| 허용오차 | $\pm5\,\mathrm{mm}$ | 정렬 때 허용되는 구멍 잔차 |
| 이동 | $8\,\mathrm{m}$ | 거치대에서 벽까지 |
| 오차 예산 | 지도 $1$, 베이스 $2$, 팔 $1$, 공구 $0.5$, 부재 $1\,\mathrm{mm}$ | §2가 더하는 원천별 배분 |
| 관측한 하루 | 패널 $8$장: 사이클 $160\,\mathrm{min}$, 준비 $20$, 리셋 $15$, 재작업 $5$ | §4가 나누는 작업 묶음 |

**S2 — 트렌치 굴착**(3, 7.5번 페이지). $5$톤급 소형 굴착기가 길이 $20\,\mathrm{m}$, 폭 $0.6\,\mathrm{m}$, 깊이 $1.0\,\mathrm{m}$의 매설관 트렌치를 바닥 고저 $\pm30\,\mathrm{mm}$로 파고, 흙은 트렌치 옆에 쌓으며, 작업자 한 명이 먼 끝에서 깊이를 확인한다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $L_1,\ L_2,\ L_3$ | $2.5$, $1.3$, $0.6\,\mathrm{m}$ | 붐, 암, 핀에서 날 끝까지의 버킷 |
| $w,\ V_b$ | $0.6\,\mathrm{m}$, $0.14\,\mathrm{m^3}$ | 트렌치 폭과 같은 버킷 폭, 산적 용량 |
| $T_c$ | $16\,\mathrm{s}$ | 한 사이클: 굴착 $6$, 선회 $4$, 덤프 $2$, 복귀 $4\,\mathrm{s}$ |
| $k_f,\ s$ | $0.85$, $1.25$ | 버킷 계수, 그리고 부피 증가율 — 흐트러진 부피를 자연 상태 부피로 나눈 값 |
| $\gamma$ | $18\,\mathrm{kN/m^3}$ | 자연 상태 흙의 단위중량 |
| $k_c$ | $60\,\mathrm{kPa}$ | 비절삭 저항: 깎는 단면의 단위 면적당 절삭력 |
| $e_{\text{GNSS}},\ \Delta\theta$ | $20\,\mathrm{mm}$, $0.1^\circ$ | 운전석 RTK 수신기의 수직 오차와 링크마다 각도 센서의 오차, 둘 다 2시그마 |
| $\tau_h,\ v$ | $0.15\,\mathrm{s}$, $0.3\,\mathrm{m/s}$ | 밸브에서 움직임까지의 지연, 마무리 패스의 버킷 날 끝 속도 |

S2의 흙과 기계는 측정한 값이 아니라 고정한 교과 숫자다. 실제 현장의 흙은 재야 하고, 그것이 [[05-construction-robotics/sim-to-real|7.5]]의 요점이다. 이 페이지의 대상은 S1이다. S2는 패널이 아니라 기계가 필요한 두 페이지가 대상 하나를 함께 쓰도록 여기서 도입한다. 계산 절이 쓰는 숫자는 모두 S1 표에 있고, 이 페이지는 두 표 밖의 숫자를 따로 고정하지 않는다.

*범위: 이 페이지는 건설 작업 하나를 명세로 바꾸는 법 — 작업 묶음, 좌표계 사슬과 오차 예산, 단계마다의 안전 상태, 시간 분모, 증거 프로토콜 — 을 S1 위에서 가르친다. 베이스가 위치를 추정하는 법([[04-robotics/navigation-mobile-manipulation|16]]), 접촉을 제어하는 법([[04-robotics/force-compliance-control|13]]), 안전 표준이 요구하는 것([[04-robotics/hri-safety|11. §6]])은 가르치지 않고 그 어휘만 쓴다. S1과 S2를 더 끌고 가는 것은 §6이 안내하는 스트림 페이지들이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 310" style="max-width:100%;height:auto" role="img" aria-label="위: S1의 다섯 오차 할당을 쌓으면 5.5 mm로 5 mm 허용오차 선을 넘고, 제곱합의 제곱근은 2.69 mm로 그 안에 있다. 아래: S1의 관측한 하루를 200분 막대 하나로, 준비 20분, 20분 사이클 여덟 번, 리셋 15분, 재작업 5분. 사이클 160분에 대해 패널 8장은 시간당 3.0장, 하루 200분 전체에 대해서는 2.4장이다.">
<text x="20" y="20" font-size="12" fill="currentColor" font-weight="600">S1의 오차 예산, 두 가지로 읽기 (mm)</text>
<text x="440.0" y="36" font-size="10.5" fill="currentColor" text-anchor="middle">허용오차 &#177;5</text>
<rect x="40.0" y="56" width="80.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="80.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">지도</text>
<text x="80.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<rect x="120.0" y="56" width="160.0" height="22" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-opacity="0.55"/>
<text x="200.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">베이스</text>
<text x="200.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">2</text>
<rect x="280.0" y="56" width="80.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="320.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">팔</text>
<text x="320.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<rect x="360.0" y="56" width="40.0" height="22" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-opacity="0.55"/>
<text x="380.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">공구</text>
<text x="380.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">0.5</text>
<rect x="400.0" y="56" width="80.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="420.0" y="51" font-size="10" fill="currentColor" text-anchor="middle">부재</text>
<text x="420.0" y="71" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<text x="40" y="94" font-size="11" fill="currentColor">선형 합: 1 + 2 + 1 + 0.5 + 1 = 5.5 mm, 허용오차를 0.5 넘는다</text>
<rect x="40" y="102" width="215.4" height="22" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-opacity="0.55"/>
<text x="147.7" y="117" font-size="10.5" fill="currentColor" text-anchor="middle">2.69</text>
<text x="40" y="140" font-size="11" fill="currentColor">제곱합의 제곱근: &#8730;7.25 = 2.69 mm, 허용오차 안쪽으로 2.31</text>
<line x1="440.0" y1="42" x2="440.0" y2="128" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3"/>
<line x1="40" y1="150" x2="520.0" y2="150" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="40.0" y1="150" x2="40.0" y2="154" stroke="currentColor"/><text x="40.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="120.0" y1="150" x2="120.0" y2="154" stroke="currentColor"/><text x="120.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<line x1="200.0" y1="150" x2="200.0" y2="154" stroke="currentColor"/><text x="200.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">2</text>
<line x1="280.0" y1="150" x2="280.0" y2="154" stroke="currentColor"/><text x="280.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">3</text>
<line x1="360.0" y1="150" x2="360.0" y2="154" stroke="currentColor"/><text x="360.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">4</text>
<line x1="440.0" y1="150" x2="440.0" y2="154" stroke="currentColor"/><text x="440.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">5</text>
<line x1="520.0" y1="150" x2="520.0" y2="154" stroke="currentColor"/><text x="520.0" y="165" font-size="10.5" fill="currentColor" text-anchor="middle">6</text>
<text x="20" y="192" font-size="12" fill="currentColor" font-weight="600">S1의 관측한 하루 (분)</text>
<rect x="40.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-opacity="0.55"/>
<text x="64.0" y="215" font-size="10" fill="currentColor" text-anchor="middle">준비</text>
<rect x="88.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="112.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="136.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="160.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="184.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="208.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="232.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="256.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="280.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="304.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="328.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="352.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="376.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="400.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="424.0" y="200" width="48.0" height="22" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-opacity="0.55"/>
<text x="448.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<rect x="472.0" y="200" width="36.0" height="22" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-opacity="0.55"/>
<text x="490.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">15</text>
<rect x="508.0" y="200" width="12.0" height="22" fill="currentColor" fill-opacity="0.6" stroke="currentColor" stroke-opacity="0.55"/>
<text x="514.0" y="215" font-size="10.5" fill="currentColor" text-anchor="middle">5</text>
<text x="490.0" y="195" font-size="10" fill="currentColor" text-anchor="end">리셋, 재작업</text>
<line x1="490.0" y1="197" x2="490.0" y2="200" stroke="currentColor"/>
<text x="280.0" y="195" font-size="10" fill="currentColor" text-anchor="middle">20분 사이클 여덟 번</text>
<line x1="40" y1="228" x2="520.0" y2="228" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="40.0" y1="228" x2="40.0" y2="232" stroke="currentColor"/><text x="40.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="160.0" y1="228" x2="160.0" y2="232" stroke="currentColor"/><text x="160.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">50</text>
<line x1="280.0" y1="228" x2="280.0" y2="232" stroke="currentColor"/><text x="280.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">100</text>
<line x1="400.0" y1="228" x2="400.0" y2="232" stroke="currentColor"/><text x="400.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">150</text>
<line x1="520.0" y1="228" x2="520.0" y2="232" stroke="currentColor"/><text x="520.0" y="243" font-size="10.5" fill="currentColor" text-anchor="middle">200</text>
<path d="M88.0 257V262H472.0V257" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="276" font-size="11" fill="currentColor" text-anchor="middle">사이클만: 패널 8장 / 160분 = 시간당 3.0장</text>
<path d="M40.0 285V290H520.0V285" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="304" font-size="11" fill="currentColor" text-anchor="middle">하루 전체: 패널 8장 / 200분 = 시간당 2.4장</text>
</svg>

S1을 제 숫자로 그린 것이다. 위: 다섯 할당을 이어 쌓으면 $5.5\,\mathrm{mm}$로 $\pm5\,\mathrm{mm}$ 허용오차를 넘지만, 제곱합의 제곱근은 $2.69\,\mathrm{mm}$로 $2.31$을 남기고 그 안에 든다. 어느 막대가 맞는지는 오차가 독립이고 평균이 0인지에 달려 있다(§2). 아래: 관측한 하루는 패널 $8$장에 $200$분이다. 사이클 $160$분으로 세면 시간당 $3.0$장, 하루 전체로 세면 $2.4$장이다(§4).

### 1. 로봇보다 작업 묶음부터

생산 단위, 시작·끝 상태, 허용오차, 사이클 목표, 선행·후속 공정, 책임 경계를 쓴다. "패널을 자율로 설치한다"는 말에는 적어도 다섯 단계가 숨어 있다 — 집기, 운반, 정렬(구조물에 대고 위치를 추정하는 데서 시작한다), 지지·체결, 확인(놓는 것으로 끝난다) — 그리고 단계마다 지배적인 실패가 다르다.

| 단계 | 필요한 증거 | 지배적 불확실성 | 안전 대비책 |
|---|---|---|---|
| 집기 | 안정된 파지와 탑재 하중 여유 | 패널 자세, 흡착·접촉 | 내려놓고 다시 집기 |
| 운반 | 충돌 없는 베이스 운동 | 사람, 지형, 위치 추정 | 제어된 정지 |
| 정렬 | 구멍 잔차 $\le5$ mm | 베이스·팔·좌표계 오차 | 후퇴 후 재스캔 |
| 지지·체결 | 힘과 자세가 허용 범위 안 | 작업자 행동, 컴플라이언스 | 정지 유지 또는 양보 |
| 확인 | 체결·자세 완료 기록 | 센서 관측 가능성 | 검사 요청 |

앞에서 쓰라고 한 일곱 가지를 묶은 것이 이 절이 기대는 정의다.

> **작업 묶음의 정의.** **작업 묶음**(work package)은 로봇을 고르기 전에 쓰는, *생산 단위 하나에 대한 계약*이다. 정의 조건 다섯. **단위**는 셀 수 있다. "외장 공사"가 아니라 패널 한 장 설치다. **시작 상태와 끝 상태**는 물리적이고 확인할 수 있다. **합격 시험**은 허용오차와 그것을 재는 좌표계를 밝힌다. **시간 목표**에는 분모가 붙는다(§4). 그리고 **경계**가 무엇이 먼저 끝나 있어야 하고, 무엇이 뒤따르며, 넘겨주는 지점마다 누가 책임지는지를 밝힌다.
>
> $$\mathcal W=(u,\ s_0,\ s_f,\ \mathrm{acc},\ T^\ast,\ \mathcal B)$$
>
> $u$는 단위, $s_0$와 $s_f$는 시작·끝 상태, $\mathrm{acc}$는 합격 시험, $T^\ast$는 분모가 붙은 시간 목표, $\mathcal B$는 경계다. 로봇에 대한 주장은 이 여섯 항목 가운데 하나에 대한 주장이므로, 주장을 검사하려면 여섯이 모두 있어야 해서 순서쌍으로 쓴다.
>
> - **예**: S1. $u$는 패널 한 장, $s_0$는 벽에서 $8\,\mathrm{m}$ 떨어진 거치대 위의 $20\,\mathrm{kg}$ 패널, $s_f$는 두 구멍이 $\pm5\,\mathrm{mm}$ 안에 들고 체결되었으며 구역이 비워진 상태다. $\mathrm{acc}$는 구조물 좌표계에서 잰 두 구멍의 잔차(§2), $T^\ast$는 사이클이 아니라 하루 전체에 대한 시간당 비율(§4), $\mathcal B$는 미리 설치·측량된 브래킷, 지지하는 동안 체결하는 작업자, 그 뒤의 검사다.
> - **비예**: "패널을 자율로 설치한다". 개수도 끝 상태도 허용오차도 책임자도 없어서 어떤 실험도 이 말을 반박할 수 없고, 측량·체결·검사를 슬그머니 아무에게도 맡기지 않는다.
> - **왜 중요한가**: 뒤의 절이 항목을 하나씩 채운다. §2는 $\mathrm{acc}$를 검사할 수 있게 만들고, §3은 $s_0$와 $s_f$ 사이의 단계마다 안전 상태를 주고, §4는 $T^\ast$의 분모를 대고, §5는 단위들이 어떤 조건에서 관측되었는지 말한다.

### 2. 좌표계와 오차 예산 닫기

*한 문장으로:* 공구가 목표에 닿는 오차는 좌표계 사슬의 고리마다 하나씩 생기는 오차의 합이고, 그 오차들이 길이처럼 더해지는지 분산처럼 더해지는지는 예산이 밝혀야 할 가정이다.

공구와 목표 사이의 오차는 센서 숫자 하나가 아니다. S1의 구멍은 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §4]]가 말하는 변환 다섯 개의 사슬을 지나 목표에 닿는다. 설계 모델을 현장 지도에 묶는 변환(지도), 지도에서 모바일 베이스로(베이스), 베이스에서 팔의 플랜지로(팔), 플랜지에서 그리퍼로(공구), 그리퍼에서 패널의 구멍으로(부재). 명목 사슬 주위에서 선형화하면 구멍의 변위는 고리마다의 작은 오차가 구멍에 만드는 변위의 합이다. 회전 오차는 구멍까지의 거리를 곱한 채로 들어오고, 그래서 할당은 고리가 아니라 구멍에서 적는다. 그러므로 1차 보수 예산은 다음처럼 적을 수 있다.

$$e_{\text{total}}\lesssim e_{\text{map}}+e_{\text{base}}+e_{\text{arm}}+e_{\text{tool}}+e_{\text{part}}.$$

S1이 1, 2, 1, 0.5, 1 mm를 할당하면 합은 5.5 mm로 이미 허용오차를 넘는다. 제곱합의 제곱근(root-sum-square)은 $\sqrt{7.25}=2.69$ mm를 주지만, 오차들이 대략 독립이고 평균이 0일 때만 그렇다. 어느 쪽을 쓸지는 산수의 장식이 아니라 방어해야 할 가정이다.

**두 읽기는 어디서 오는가.** 둘 다 합 $e=\sum_i e_i$에서 출발한다. 모든 $|e_i|\le a_i$가 확실한 경계라면 삼각부등식이 부호와 상관에 관계없이 $|e|\le\sum_i a_i$를 준다. 이것이 선형 읽기다. 반대로 $e_i$가 평균 0, 표준편차 $\sigma_i$인 확률변수라면 합의 분산은 $\sum_i\sigma_i^2+2\sum_{i<j}\operatorname{Cov}(e_i,e_j)$이다([[02-foundations/probability|3. 확률 §2]]). 그러니 공분산이 사라져야만 분산이 더해지고, 모든 할당이 제 $\sigma_i$의 같은 배수 $k$라면 $k\,\sigma_{\text{total}}=\sqrt{\sum_i a_i^2}$가 된다. 이것이 제곱합의 제곱근 읽기이고, 두 가정이 모두 눈에 보인다.

> **오차 예산의 정의.** **오차 예산**(error budget)은 측정이 아니라 *명세*다. 기준에서 허용오차를 지켜야 할 형상까지 이어지는 좌표계 사슬 위의 오차 원천마다 할당 하나씩, 그리고 할당들을 합쳐 그 허용오차와 비교할 총량을 만드는 규칙이다. 정의 조건 넷. **완전하다**: 모든 고리에 항이 있다. 빠진 항은 부재가 어긋날 때까지 보이지 않기 때문이다. **같은 잣대로 잰다**: 모든 할당이 형상에서의 변위이고, 허용오차의 방향을 따르며, 뜻이 하나다 — 모두 확실한 경계이거나, 모두 제 표준편차의 같은 배수 $k$다. **규칙과 그 가정을 밝힌다**: 선형 합은 각 경계가 지켜지기만 하면 되고, 제곱합의 제곱근은 평균이 0이고 서로 상관없는 오차를 요구한다. 그리고 **닫혀 있다**: 총량을 허용오차와 비교하고 여유를 적어 둔다.
>
> $$e_{\text{lin}}=\sum_{i=1}^{N}a_i\ \ \ge\ \ e_{\text{RSS}}=\sqrt{\sum_{i=1}^{N}a_i^2}$$
>
> $a_i\ge0$는 원천 $i$의 할당, $N$은 원천의 수다. $\sum_i a_i$를 제곱하면 $\sum_i a_i^2$에 음이 아닌 교차항 $2\sum_{i<j}a_ia_j$가 더해지기 때문에 선형 총량이 더 작아질 수는 없다.
>
> - **예**: S1, $a=(1,2,1,0.5,1)$ mm. $e_{\text{lin}}=5.5$ mm로 허용오차를 $0.5$ 넘고, $e_{\text{RSS}}=2.69$ mm로 그 안쪽에 $2.31$을 남긴다. 베이스 항이 제곱합의 제곱근 분산의 $4/7.25=55\%$이므로 줄여야 할 항은 베이스다.
> - **비예**: 편향 위에 씌운 제곱합의 제곱근. 지도 항이 측량 오프셋이라 모든 패널에 똑같이 $1$ mm라면, 다른 항과 평균되지 않고 모두를 한꺼번에 민다. $2.69$가 아니라 $1+\sqrt{4+1+0.25+1}=3.5$ mm다. 상관도 같은 식으로 틀린다. 지도와 베이스 오차가 한 번의 측량에서 나와 함께 움직이면 먼저 더해져서 $\sqrt{(1+2)^2+1+0.25+1}=3.35$ mm가 된다.
> - **왜 중요한가**: 규칙이 판정을 정한다. 선형으로 읽으면 명세된 S1은 $\pm5$ mm를 약속하지 못하고, 제곱합의 제곱근으로 읽으면 약속할 수 있으며 베이스 오차가 더 커질 여지까지 남는다. 규칙 없이 숫자 하나로 보고한 예산은 저자들이 둘 중 무엇을 믿는지 말하지 않은 것이다.

모든 변환에는 출발 좌표계, 도착 좌표계, 갱신 주기, 타임스탬프, 보정 책임자가 있어야 한다. 타임스탬프도 오차의 일부다. $0.5$ m/s로 움직이는 베이스에서 스탬프 오차 1밀리초는 구멍에서 $0.5$ mm이므로, 베이스의 $2$ mm는 리그 전체에 설명되지 않은 시간 $4$ ms를 남긴다. 그 값을 센서마다 매기는 곳이 [[04-robotics/perception-sensors-rigs|3.6 인식 센서 §9]]다. 로봇 좌표계와 측정으로 묶이지 않은 BIM 좌표계는 로봇 명령이 아니다.

### 3. 안전은 시스템 상태다

*한 문장으로:* 안전 상태는 단계마다 고르는 작업 시스템 전체의 조건이고, 제때 닿을 수 있으며 고장 난 것에 기대지 않으므로, 안전 구조는 정지 버튼 하나가 아니라 단계마다 하나씩인 그런 상태들의 목록이다.

위험원(해를 끼칠 수 있는 것), 위험도(심각도와 가능성·노출), 안전 조치, 감시 변수, 안전 상태를 구분한다. 위험원, 위험도, 그리고 안전 상태로 가는 정지 기능들은 [[04-robotics/hri-safety|11. HRI·안전 §6]]의 어휘이고, 안전 조치는 위험도를 줄이는 모든 수단이며, 감시 변수와 안전 상태가 이 절의 것이다. 비상정지만으로 안전 구조가 끝나지 않는다. 평상시의 보호 정지, 속도·힘 제한, 출입 금지 구역, 사람의 권한, 재시작 조건, 안전 센서 자체의 고장에도 모두 책임자가 있어야 한다.

§1 표의 마지막 열이 단계마다 하나씩인 S1의 안전 상태 목록이고, 그것을 목록으로 읽는 것이 요점이다. 어느 상태가 안전한지는 시스템이 무엇을 하고 있느냐에 달렸다. 단계마다 명세는 그 상태로 옮기게 하는 **감시 변수**도 밝힌다 — 집을 때는 흡착 압력이나 탑재 하중 추정값, 운반할 때는 사람과의 거리, 정렬할 때는 두 구멍의 잔차, 지지할 때는 접촉력과 자세, 확인할 때는 체결 기록 — 그리고 누가 시스템을 그 상태에서 다시 데리고 나올 수 있는지도 밝힌다. 펌프가 멈춘 뒤 흡착 압력이 얼마나 버티는지 — 안전율 $4.8$로 잡은 흡착컵 넷은 요구되는 $2$를 $41$ s 동안만 지킨다 — 는 [[02-foundations/fluid-power|0.6.3 유체 동력 §9–§10]]이다.

> **안전 상태의 정의.** **안전 상태**(safe state)는 버튼도 명령도 로봇 혼자의 성질도 아니고, *한 단계에서 작업 시스템 전체*가 — 로봇, 탑재물, 사람, 현장이 함께 — 놓이는 상태다. 정의 조건 넷. **그 단계의 위험원을 묶어 둔다**: 동력으로 움직이는 어떤 것도 사람 쪽으로 가지 않고, 탑재물은 받쳐져 있다. **제때 닿을 수 있다**: 그 단계의 어디서든 도달한다. **고장 난 기능에 기대지 않는다**: 시스템을 그리로 보낸 센서·동력·소프트웨어 없이도 유지된다. 그리고 **의도적으로만 떠난다**: 떠나려면 밝혀 둔 재시작 조건과 그것을 허락할 권한을 가진 사람이 있어야 한다.
>
> $$T_{\text{detect}}+T_{\text{react}}+T_{\text{enter}}\le T_{\text{harm}}$$
>
> 는 둘째 조건을 풀어 쓴 것이다. $T_{\text{detect}}$는 위험원이 생긴 때부터 감시 변수가 그것을 검출할 때까지, $T_{\text{react}}$는 검출부터 명령까지, $T_{\text{enter}}$는 명령부터 그 상태에 이를 때까지, $T_{\text{harm}}$은 위험원이 생긴 때부터 해가 닥칠 때까지의 시간이다. 지연들이 차례로 일어나므로 더해지고, 그래서 11 §6의 보호 이격 거리는 이 예산을 미터로 쓰고 로봇 자신의 이동과 센싱 불확실성을 더한 것이다.
>
> - **예**: 지지·체결 단계의 S1, 작업자의 손이 패널에 있다. 안전 상태는 *정지 유지*(freeze)다. 관절 브레이크를 걸고 동력 운동이 없으며, $196\,\mathrm{N}$ 패널을 서보 루프가 아니라 브레이크가 받친다. 그래서 서보 동력이 끊겨도 유지되고(셋째 조건), 작업자가 물러나 풀어 줄 때만 떠난다.
> - **비예**: *후퇴 후 재스캔*. 패널 곁에 아무도 없고 놓침이 시간만 잃게 하는 정렬 단계의 안전 상태다. 지지·체결 단계에서라면 반쯤 체결된 패널을 작업자의 손 사이로 끌고 나간다. 비상정지가 둘째 비예다. 그것은 전이이고, 전원이 끊긴 뒤 무엇이 하중을 받치느냐에 따라 안전 상태에 닿을 수도 닿지 못할 수도 있다.
> - **왜 중요한가**: 안전 구조란 바로 이 목록이다 — 단계마다 상태 하나, 그리고 저마다의 감시 변수와 재시작 규칙. 모든 단계에 정지 하나만 두는 설계는 모든 단계의 안전 상태가 같다고 가정하는 것이고, S1의 표는 그 가정이 틀렸음을 보여 준다.

**숫자로 본 시간 조건.** 11 계산 절의 P2 셀을 빌리자. 그 반응 시간이 앞의 두 항으로 정확히 나뉜다. 몸이 감지 영역에 들어와서 추적기가 알릴 때까지 $T_{\text{detect}}=0.06$ s, 결정과 브레이크 명령에 $T_{\text{react}}=0.04$ s, 멈추기까지 $T_{\text{enter}}=0.30$ s다. 표준 보행 속도 $1.6$ m/s로 걷는 작업자는 그 $0.40$ s 동안 $1.6\times(0.06+0.04+0.30)=0.64$ m를 다가오므로, 그 셀의 거리 감시는 사람이 아직 $0.64$ m보다 멀리 있을 때 작동해야 한다. 로봇 자신의 이동과 센싱 불확실성은 그 위에 더한다. 11 §6의 $S_h$ 항에 안전 상태 쪽에서 도달한 것이다. S1의 베이스는 $20$ kg 패널을 든 채라 더 느리게 선다. [[05-construction-robotics/hrc-worker-centered|6. HRC]]은 그 정지 시간을 $T_s=0.40$ s로 고정하고, 그러면 같은 항은 $1.6\times(0.10+0.40)=0.80$ m가 된다. 예산은 실제로 돌릴 기계에서 잰 정지 시간으로 써야 한다.

실험 성공에서 인증을 추론하지 마라. 연구 논문은 밝힌 안전 조치 아래의 성능을 확립할 수 있을 뿐이고, 적합성 주장에는 해당 표준과 책임 있는 평가 절차가 필요하다.

### 4. 생산성에는 분모가 필요하다

관측 시간 $T$ 동안 끝낸 단위가 $n$개면 처리량은 $n/T$이지만, 배치를 비교하려면 준비, 보정, 감독, 리셋, 재작업, 정지 시간도 있어야 한다. S1의 분모는 작업 묶음이 치른 모든 구간의 합이다. 어느 것도 공짜가 아니었기 때문이다.

$$T_{\text{effective}}=T_{\text{setup}}+\sum_i(T_{\text{cycle},i}+T_{\text{reset},i}+T_{\text{rework},i})+T_{\text{down}}.$$

패널 8장에 사이클 160분, 준비 20분, 리셋 15분, 재작업 5분이 들었다면 사이클 기준의 헤드라인 처리량은 시간당 3장이고, 유효 처리량은 $8/200\times60=2.4$장이다. 두 숫자 모두 참이지만, 관측한 작업 묶음을 기술하는 것은 뒤의 것뿐이다.

그 합의 항들은 같은 종류가 아니다. 준비는 뒤에 패널이 몇 장 오든 작업 묶음마다 한 번 치르고, 사이클·리셋·재작업은 놓침과 결함이 패널마다 생기므로 패널마다 다시 치르며, 정지 시간은 사건마다 치른다. 이 구분이 하루를 늘리면 도움이 되는지를 정하고, 아래 계산 절이 그것을 계산한다. 사람의 시간도 비율 옆에 적어라. 하루 종일 곁에 있는 감독자는 패널 $8$장에 $200$분의 주의를, 곧 패널당 $25$분을 더하는데, 어떤 사이클 시간도 이것을 보여 주지 않는다.

> **유효 처리량의 정의.** **유효 처리량**(effective throughput)은 *비율*이다. 작업 묶음 전체의 관측 시간 단위당 합격한 단위의 수다. 정의 조건 넷. **분자는 합격한 단위만 센다**: 합격 시험에 떨어져 재작업한 패널은 마침내 통과할 때 한 번만 센다. **분모는 관측 구간 전체다**: 준비, 모든 사이클·리셋·재작업, 모든 정지 시간을 넣고, 로봇 탓이 아니었다는 이유로 빼는 것이 없다. **둘은 한 창에서 온다**: 좋은 한 시간을 하루 전체의 개수로 나누지 않는다. 그리고 **창을 밝힌다**: 길이와 준비를 몇 번 포함하는지. 고정 부담이 그 창 위에 나뉘어 얹히기 때문이다.
>
> $$\eta_{\text{eff}}=\frac{n_{\text{acc}}}{T_{\text{effective}}}$$
>
> $n_{\text{acc}}$는 창 안에서 작업 묶음의 합격 시험을 통과한 단위의 수, $T_{\text{effective}}$는 같은 창에 대한 위의 합이다. 그래서 분자와 분모가 같은 분(分)들을 센다.
>
> - **예**: S1의 하루, 합격한 패널 $8$장에 $200$분. $\eta_{\text{eff}}$는 시간당 $2.4$장, 패널당 $25$분이다.
> - **비예**: 사이클 처리량, 곧 사이클 $160$분에 패널 $8$장인 시간당 $3.0$장. 참이고 동작을 다듬는 데 쓸모 있지만, 하루 $200$분 가운데 $160$분만 다룬다. 작업 묶음의 생산성으로 인용하면 $3.0/2.4=1.25$, 곧 4분의 1만큼 부풀린다.
> - **왜 중요한가**: 건설 로봇은 작업조의 가장 빠른 사이클이 아니라 작업조의 하루와 경쟁한다. 두 비율 사이의 틈 — 준비, 리셋, 재작업, 정지 — 은 사람이 로봇 주위에서 하는 일이고, 배치의 성패가 거기서 갈린다.

### 대상으로 한 번 끝까지 · Worked case

S1의 숫자로 여섯 단계. 예산을 두 가지로 읽고, 제곱합의 제곱근 숫자가 두 신뢰 배수에서 무엇을 뜻하는지 본 뒤, 하루를 두 가지로 읽고 현장 소장이 묻는 질문 — 하루를 늘리면 나아지는가 — 까지 끌고 간다. 기계나 현장을 잰 것이 아니라 고정된 대상 위의 교과 계산이다.

**1단계 — 최악의 경우로 읽은 예산.** $5\,\mathrm{mm}$ 허용오차에 대해 $e_{\text{lin}}=1+2+1+0.5+1=5.5\,\mathrm{mm}$, $0.5\,\mathrm{mm}$ 초과다. 다섯 할당이 확실한 경계이고 오차들이 한 방향으로 늘어서는 것을 막을 것이 없다면, 명세된 S1은 허용오차를 약속할 수 없다. 시험을 아무리 해도 이것은 바뀌지 않고, 할당을 줄여야만 바뀐다.

**2단계 — 독립이고 평균 0인 오차로 읽은 예산.** $e_{\text{RSS}}=\sqrt{1+4+1+0.25+1}=\sqrt{7.25}=2.69\,\mathrm{mm}$로 허용오차 안쪽에 $5-2.69=2.31\,\mathrm{mm}$, 곧 그 $46\%$를 남긴다. 분산 비중은 베이스 $4/7.25=55\%$, 지도·팔·부재가 각각 $1/7.25=14\%$, 공구 $0.25/7.25=3\%$다. 베이스 항을 반으로 줄이면 총량이 $\sqrt{4.25}=2.06\,\mathrm{mm}$가 되지만, 공구 항을 아예 없애도 $\sqrt{7}=2.65\,\mathrm{mm}$에 그친다.

**3단계 — 2.69 mm의 뜻은 $k$에 달렸다.** 할당은 제 표준편차의 배수 $k$와 함께일 때만 경계다. 각 할당이 2시그마 경계라면 — [[05-construction-robotics/construction-manipulation|9. 건설 조작]]이 나중에 핀에서 택하는 읽기다 — 합친 표준편차는 $\sigma=2.693/2=1.346\,\mathrm{mm}$이고 허용오차는 $5/1.346=3.714\,\sigma$에 놓인다. 가우시안 오차라면 구멍 하나가 한 축에서 벗어날 확률은 양쪽 꼬리를 모두 세므로

$$P(|e|>5\,\mathrm{mm})=2\,Q(3.714)=2.0\times10^{-4}$$

이다. $Q$는 [[02-foundations/probability|3. 확률 §6]]의 가우시안 위쪽 꼬리이고, 구멍-축 $4{,}900$개에 하나꼴이다. 같은 숫자를 1시그마 값으로 읽으면 $\sigma=2.693\,\mathrm{mm}$, 허용오차는 $1.857\,\sigma$, $2\,Q(1.857)=0.063$으로 $16$개에 하나꼴 — $310$배 잦다. $k$ 없는 할당 다섯 개는 정렬이 얼마나 자주 후퇴해야 하는지 아직 말하지 않는다.

**4단계 — 사이클로 센 하루.** 사이클 $160$분에 패널 $8$장이면 $8/160\times60=3.0$, 곧 시간당 $3.0$장이고 패널당 $20$분이다.

**5단계 — 유효하게 센 하루.** $T_{\text{effective}}=20+160+15+5+0=200$분이고 그날 정지 시간은 없었으므로 $\eta_{\text{eff}}=8/200\times60=2.4$, 곧 시간당 $2.4$장이고 패널당 $25$분이다. 부담은 모두 $40$분으로 하루의 $20\%$이고, 유효 비율은 사이클 비율의 $0.8$이다.

**6단계 — 끝까지 끌고 가기: 하루를 늘리면 나아지는가?** 준비는 한 번 치른다. 리셋과 재작업이 하루 평균대로 패널마다 $(15+5)/8=2.5$분씩 되풀이된다고 하자. 그러면 준비 한 번 뒤 패널 $n$장에 $20+(20+2.5)\,n$분이 들고, 그래서

$$\eta_{\text{eff}}(n)=\frac{60\,n}{20+22.5\,n}\ \text{panels/h}$$

는 $n=8$에서 $2.4$, $n=16$에서 $2.53$이고, $n$이 커지면 $60/22.5=2.67$장에 다가간다. 어떤 길이의 하루도 헤드라인 $3.0$에 닿지 못한다. 준비는 묽어지지만 리셋과 재작업은 그렇지 않다. $3.0$에 다가가기만 하려 해도 패널당 합계가 $20$분으로 내려와야 한다 — 지금의 리셋·재작업이라면 사이클 $17.5$분, 지금의 사이클이라면 리셋·재작업 없음. 그리고 정렬이 얼마나 자주 후퇴해 다시 스캔해야 하는지는 3단계가 한정한다. 그 시간은 §5의 집계 규칙에 따라 사이클 열에도, 리셋 열에도 들어간다. $k=1$이면 구멍-축 $16$개에 하나가 벗어나고 패널 한 장에는 구멍-축이 넷 있으며, $k=2$면 $4{,}900$개에 하나다.

### 5. 증거 사다리

시뮬레이션은 알고리즘과 드문 조건을, 실험실은 마련된 조건에서의 실제 센싱·접촉을, 목업은 규모와 작업 흐름을, 가동 중인 현장은 바뀌는 공정·사람과의 통합을 검사한다. 더 높은 단이 약한 프로토콜을 고쳐 주지는 않는다. 모든 단에서 에피소드, 성공, 개입, 리셋, 실패 분류, 변동, 기준선을 정의한다.

단들과 각 단이 허락하는 문장은 [[06-research-practice/real-world-impact|6. 실세계 임팩트 §2]]에 펼쳐져 있고, 단의 완전한 정의는 그 페이지의 계산 절에 있다. 단은 초록의 말이 아니라 방법 절의 조건이 정한다. 이 페이지가 더하는 것은 S1이 각 단에서 보여야 할 것이고, 그것은 §2에서 나온다. 단마다 예산의 서로 다른 항들이 가정에서 측정으로 바뀌기 때문이다.

| 단 | 거기서 가정이 아니라 측정되는 S1 예산의 항 |
|---|---|
| 시뮬레이션 | 없음. 다섯 할당이 모두 입력이므로 이 단은 허용오차가 아니라 정렬 결정을 시험한다 |
| 실험실 | 실제 하드웨어의 팔·공구·부재. 지도와 베이스는 실험실이 마련한 고정 표적에 대해서만 |
| 실물 크기 목업 | 같은 것에 더해 실물 크기 패널, 실제 브래킷, 패널마다 다시 놓는 베이스 |
| 가동 중인 현장 | 지어지면서 바뀌는 구조물에 대한 지도와 베이스, 사람과 날씨까지. 다섯 항이 모두 측정되는 유일한 단 |

§2의 예산으로 무게를 달면, 실험실 단은 팔·공구·부재 항, 곧 S1의 제곱합의 제곱근 분산의 $(1+0.25+1)/7.25=31\%$를 측정한다. 나머지 $69\%$인 지도와 베이스 항은 바뀌는 구조물에 대해서는 가동 중인 현장에서만 측정된다. 목업 결과가 그대로 옮겨 가지 않는다는 경고 뒤의 산수가 이것이다.

첫 시행 전에 S1에 맞게 적은 프로토콜 일곱 항목:

| 항목 | S1에서의 모습 |
|---|---|
| 에피소드 | 패널 한 장, 거치대에서 집는 순간부터 로봇이 비켜선 채 놓을 때까지 |
| 성공 | 놓는 순간 구조물 좌표계에서 두 구멍이 $\pm5$ mm 안에 있고 체결됨 |
| 개입 | 에피소드 도중 로봇의 상태나 패널의 자세를 바꾸는 모든 사람의 행동 |
| 리셋 | 실패한 에피소드 뒤 패널과 로봇을 시작 상태로 되돌리는 일. 시간을 재어 §4의 분모에 넣는다 |
| 실패 분류 | 첫 실패가 일어난 §1 표의 단계 |
| 변동 | 패널, 거치대 칸, 베이스 자세, 브래킷 측량, 주변 사람, 조명과 날씨, 각각의 범위와 함께 |
| 기준선 | 같은 패널에 대한 작업조의 비율. 사이클이 아니라 하루 기준(§4) |

운전자가 구해 낸 에피소드를 성공으로 셀지도 여기서, 어떤 시행도 보기 전에 정한다([[04-robotics/hri-safety|11. §2]]). 집계 규칙 없는 성공률은 아직 숫자가 아니다.

### 6. 도메인 진입

S1을 명세한 뒤 맞는 스트림을 고른다: [[05-construction-robotics/earthmoving-heavy-machinery|토공]], [[05-construction-robotics/assembly-fabrication|조립]], [[05-construction-robotics/site-perception|현장 인식]], [[05-construction-robotics/hrc-worker-centered|HRC]], [[05-construction-robotics/digital-twin-workflows|디지털 트윈]]. [[05-construction-robotics/sim-to-real|sim-to-real]]과 [[05-construction-robotics/industry-deployment|배치]]는 주제를 대신하는 것이 아니라 모든 스트림을 가로지르는 층으로 쓴다.

스트림마다 같은 고정 대상 위에서 이 페이지의 한 부분을 더 끌고 가고, S1이나 S2가 주는 것보다 숫자가 더 필요한 페이지는 제 숫자를 고정하고 그렇다고 밝힌다. §2에 비추어 읽으면 페이지들은 S1의 할당 제곱합 $7.25\,\mathrm{mm^2}$를 나누어 맡는다. 지도 항($1$)은 설계 모델과 그것을 현장에 정합하는 일(7과 5), 베이스 항($4$)은 위치 추정과 베이스 배치([[04-robotics/navigation-mobile-manipulation|16]]), 팔과 공구 항($1$과 $0.25$)은 매니퓰레이터(4와 9), 부재 항($1$)은 제작 공차(4)의 몫이다. 기계가 아니라 질문으로 고른다.

| 질문이 무엇에 관한 것인가 | 대상 | 스트림 |
|---|---|---|
| 한 쌍으로서의 두 구멍: 병진, 요, 후퇴 | S1 | [[05-construction-robotics/assembly-fabrication\|4. 조립·제작]] |
| 시공된 구조물의 스캔과 정합. §2의 지도 항이 여기에 기댄다 | S1 | [[05-construction-robotics/site-perception\|5. 현장 인식]] |
| 공유 현장의 사람들, 작업자가 패널 곁에 있는 단계 | S1 | [[05-construction-robotics/hrc-worker-centered\|6. HRC]] |
| 지도 항 뒤의 설계 모델과 그로부터 생성하는 작업 | S1 | [[05-construction-robotics/digital-twin-workflows\|7. 디지털 트윈]] |
| 구멍이 핀을 만나는 순간: 포착과 접촉력 | S1 | [[05-construction-robotics/construction-manipulation\|9. 건설 조작]] |
| 소형 굴착기로 계획고까지 파기 | S2 | [[05-construction-robotics/earthmoving-heavy-machinery\|3. 토공]] |
| 시뮬레이터의 숫자가 옮겨 가기 전에 맞춰야 할 것 | S2 | [[05-construction-robotics/sim-to-real\|7.5 Sim-to-Real]] |
| 누가 무엇을 어떤 자율 수준으로 파는가 | 둘 다 | [[05-construction-robotics/industry-deployment\|8. 산업·배치]] |

### 읽고 나면

- [ ] 어떤 건설 작업이든 작업 묶음으로 쓴다: 단위, 시작·끝 상태, 합격 시험, 분모가 붙은 시간 목표, 경계.
- [ ] 좌표계 사슬을 따라 오차 예산을 세우고 두 가지로 합치며, 배수 $k$를 포함해 각 방식이 요구하는 가정을 밝힌다.
- [ ] 단계마다 안전 상태를 대고 네 조건에 비추어 확인한다.
- [ ] 작업 묶음의 사이클 처리량과 유효 처리량을 계산하고, 하루를 늘리면 어떤 부담이 묽어지는지 말한다.
- [ ] 결과를 증거 사다리에 놓고 그 단이 어떤 예산 항을 측정했는지 말하며, 첫 시행 전에 프로토콜 일곱 항목을 정한다.
- [ ] 어떤 건설로봇 주장이든 작업 단위·허용오차·좌표계·불확실성·사람과 권한·안전 상태·시간 분모·개입과 리셋·증거 단·실패 분류를 한 장의 장부로 만든다.

### 스스로 점검

1. 오차 예산의 선형 총량은 왜 제곱합의 제곱근 총량보다 작아질 수 없고, 둘은 언제 같은가?
2. S1의 지도 항이 모든 패널에 똑같이 $1$ mm인 측량 오프셋으로 드러났다. 예산에 어떻게 들어가고, 총량은 얼마인가?
3. *후퇴 후 재스캔*은 왜 정렬 단계의 안전 상태이지만 지지·체결 단계의 안전 상태는 아닌가?
4. S1의 다섯 단계마다 안전 상태와 그것을 일으키는 감시 변수를 대고, 단계를 그린 그림에 어떤 행위자들이 있어야 하는지 말하라.
5. 어떤 업체가 "패널당 20분"을 내세운다. 작업조와 비교하기 전에 무엇을 묻는가?
6. 어떤 보고서가 실물 크기 목업 결과를 "현장 배치에 대해 검증됨"이라 부른다. 어느 단이고, 어떤 문장을 허락하며, S1 예산의 어떤 항을 측정하지 않았는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 선형 총량을 제곱하면 $\sum_i a_i^2+2\sum_{i<j}a_ia_j$이고, 모든 할당이 음이 아니므로 교차항도 음이 아니다. 교차항은 0이 아닌 할당이 많아야 하나일 때만 사라지므로, 두 총량은 원천이 하나인 예산에서만 같다. S1에서는 $5.5$와 $2.69$ mm다.
> 2. 선형으로 들어간다. 편향은 무작위 항들과 평균되지 않기 때문이다. $1+\sqrt{4+1+0.25+1}=1+2.5=3.5$ mm. 여전히 $\pm5$ mm 안이지만 모두 제곱합의 제곱근으로 합친 $2.69$보다 $0.81$ mm 크고, 여유는 $2.31$에서 $1.5$ mm로 줄어든다.
> 3. 정렬 단계에서는 패널 곁에 아무도 없고 놓침은 시간만 잃게 하므로, 물러나 다시 재는 것이 위험원을 묶어 둔다. 지지·체결 단계에서는 작업자의 손이 패널에 있고 볼트가 반쯤 들어가 있을 수 있어서, 패널을 빼내면 작업자의 손 사이로 끌고 나가게 된다. 지지·체결의 안전 상태는 브레이크를 건 정지 유지로, 서보 루프 없이 패널을 받친다.
> 4. 집기: 내려놓고 다시 집기, 흡착 압력이나 탑재 하중 추정값으로. 운반: 제어된 정지, 사람과의 거리나 위치 추정 상실로. 정렬: 후퇴 후 재스캔, 로봇이 할 수 있는 어떤 보정으로도 두 구멍을 $\pm5$ mm 안에 넣을 수 없다고 두 구멍의 잔차가 말하거나, 스캔을 믿을 수 없을 때. 지지·체결: 정지 유지 또는 양보, 허용 범위를 벗어난 접촉력이나 자세로. 확인: 검사 요청, 없거나 관측할 수 없는 체결 기록으로. 그림에는 작업자, 감독자, 로봇, 목표/BIM, 인식, 제어기, 그리고 정지·복구 경로가 있어야 한다. 명목상의 로봇 화살표만으로는 안 된다.
> 5. 사이클 시간인지 유효 시간인지 — 준비·리셋·재작업·정지 가운데 무엇을 넣었는지 — 어떤 창에서 몇 장으로 쟀는지, 그리고 로봇에 감독이 얼마나 필요했는지를 묻는다. S1에서 20분은 사이클이고 하루 전체로는 25분이다.
> 6. 실물 크기 목업 단이다. "현실적인 기하와 규모를 견딘다"는 허락하지만 "내가 고르지 않은 조건을 견뎠다"는 허락하지 않는다. 지어지면서 바뀌는 구조물에 대한 지도·베이스 항을 측정하지 않았고, 이 둘이 S1의 제곱합의 제곱근 분산의 $(1+4)/7.25=69\%$를 차지한다.

### 과제 · Problem set

Tier B. 이 페이지의 대상인 S1을 손으로 푼다. 시뮬레이터도 코드도 없다.

1. **그리기.** 더 어려운 현장과 더 긴 하루의 S1 그림: 나머지 넷은 그대로 두고 베이스 항을 $3\,\mathrm{mm}$로 키운 예산과, 2(c)의 20장짜리 하루. 두 예산 막대를 허용오차와 함께, 하루를 사이클만의 비율과 하루 전체의 비율이 붙은 막대 하나로 그린다.
2. **유도.** (a) 베이스 항이 $3\,\mathrm{mm}$일 때 선형 총량과 제곱합의 제곱근 총량, 여유, 베이스 항의 분산 비중, 그리고 모든 할당이 2시그마 경계일 때 한 축에서 벗어날 확률. (b) 제곱합의 제곱근 총량이 아직 $\pm5\,\mathrm{mm}$를 지키는 가장 큰 베이스 항, 그리고 선형 총량이 지키는 가장 큰 베이스 항. (c) 사이클 $18$분, 준비 $30$분, 패널 네 장마다 $12$분 리셋 한 번, 패널의 $10\%$에 $9$분짜리 재작업이 있는 20장의 하루: 유효 시간, 유효 처리량과 사이클만의 처리량. (d) 준비는 한 번, 리셋과 재작업은 패널마다 치를 때, 하루가 길어짐에 따른 (c)의 유효 비율의 극한.
3. **해석.** 어떤 논문이 실내 목업 한 곳에서 수동 리셋으로 패널 설치 로봇이 "20회 시도에 95% 성공"했다고 보고한다. (a) 사다리 위에 놓고 그것이 허락하는 문장을 적어라. (b) 아직 지지하지 못하는 주장 셋을 말하라. (c) 성공 19회 가운데 셋이 운전자가 넘겨받은 뒤 끝났다면, 첫 개입에서 에피소드를 끝내는 규칙 아래 자율 성공률은 얼마인가? (d) 95%가 뜻을 갖기 전에 논문이 밝혀야 할 §5의 프로토콜 항목은 무엇인가?

> [!note]- 그리는 법 · How to draw it
> - **위, 0에서 7까지의 밀리미터 축**: 할당 $1, 3, 1, 0.5, 1$을 쌓은 막대($6.5\,\mathrm{mm}$), $\sqrt{12.25}=3.50\,\mathrm{mm}$의 제곱합의 제곱근 막대, $5\,\mathrm{mm}$의 허용오차 선. 선형 초과분($1.5\,\mathrm{mm}$)과 제곱합의 제곱근 여유($1.5\,\mathrm{mm}$)를 표시한다.
> - **아래, 0에서 500까지의 분 축**: 준비 $30$, $18$분 사이클 스무 번($360$), 리셋 $5\times12=60$, 재작업 $2\times9=18$ — 모두 $468$분. 사이클 부분에 "패널 20장 / 360분 = 시간당 3.33장", 막대 전체에 "패널 20장 / 468분 = 시간당 2.56장"이라는 괄호를 단다.
> - **두 축 모두 선형으로, 0에서 시작한다**: 끊긴 축은 이 그림이 보여 주려는 바로 그 부담을 숨긴다.
> - 제곱합의 제곱근 막대를 제곱근이 아니라 제곱합 $12.25$로 그렸거나, 그동안 설치된 패널이 없다는 이유로 하루 막대에서 리셋을 뺐다면 그림이 틀린 것이다.

> [!tip]- 정답 · Solutions
> 1. 그리는 법 목록과 같다. $5$에 대해 $6.5$와 $3.50\,\mathrm{mm}$, $468$분, 시간당 $3.33$과 $2.56$장.
> 2. (a) $1+3+1+0.5+1=6.5\,\mathrm{mm}$로 $1.5$ 초과. $\sqrt{1+9+1+0.25+1}=\sqrt{12.25}=3.50\,\mathrm{mm}$로 여유 $1.50$. 베이스 비중 $9/12.25=73\%$. $\sigma=3.50/2=1.75\,\mathrm{mm}$, 허용오차는 $5/1.75=2.857\,\sigma$, $2\,Q(2.857)=0.0043$으로 구멍-축 $234$개에 하나꼴 — 베이스가 $2\,\mathrm{mm}$일 때의 $2.0\times10^{-4}$의 스물한 배다. (b) 제곱합의 제곱근: $\sqrt{25-3.25}=\sqrt{21.75}=4.66\,\mathrm{mm}$. 선형: $5-3.5=1.5\,\mathrm{mm}$. (c) 사이클 $360$ + 준비 $30$ + 리셋 $5\times12=60$ + 재작업 기댓값 $2\times9=18$ = $468$분이므로 $20/(468/60)=2.56$, 곧 시간당 $2.56$장이고, 사이클만으로는 $20/(360/60)=3.33$장이다. (d) 패널당 $18+12/4+0.1\times9=21.9$분이므로 비율은 $60/21.9=2.74$, 곧 시간당 $2.74$장에 다가간다.
> 3. (a) 잘해야 실물 크기 목업 단이고 "현실적인 기하와 규모를 견딘다"를 허락한다. 목업이 실물 크기가 아니면 실험실 단이고 "내 조건에서, 실제 하드웨어에서 작동한다"를 허락한다. (b) 예: 가동 중인 현장에서의 견고성, 개입이 적은 자율성(리셋이 수동이었다), 현장 간 일반화, 날씨 내성, 경쟁력 있는 생산성(분모도 기준선도 없다). (c) $(19-3)/20=16/20=80\%$. (d) 일곱 모두. 그 가운데서도 개입의 집계 규칙, 성공을 무엇으로 쟀는지(구조물 좌표계의 구멍인가 로봇의 자세인가), 리셋마다 든 시간, 기준선.

### 출처

S1, S2, 그리고 계산 절의 모든 숫자는 이 페이지가 정의한 교과 값이다. 여기서는 실제 기계나 현장을 잰 결과를 보고하지 않는다.

**이 위키 안에서**

- [[02-foundations/probability|3. 확률 §2]] — §2의 제곱합의 제곱근 뒤에 있는 분산, 공분산, 합의 분산. [[02-foundations/probability|§6]] — 계산 절의 가우시안 꼬리 $Q$.
- [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §4]] — §2의 변환과 좌표계 사슬.
- [[04-robotics/hri-safety|11. HRI·안전 §6]] — §3이 기대는 안전 어휘와 표준. [[04-robotics/hri-safety|§2]] — §5의 집계 규칙.
- [[06-research-practice/real-world-impact|6. 실세계 임팩트 §2]] — §5가 S1에 적용하는 증거 사다리. 단의 정의는 그 페이지의 계산 절에 있다.
