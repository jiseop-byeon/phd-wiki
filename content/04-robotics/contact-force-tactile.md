---
title: 9. Contact, Force & Tactile Interaction
tags: [robotics, contact, manipulation, tactile]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
wiki-support: Working
---

## English

*The only page of group E, physical interaction, in the [[04-robotics/index|robotics index]], because group H, the manipulation specialization (12–16), branches from here. Stands on [[02-foundations/linear-algebra|linear algebra]], optimization, the springs and friction of [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §3–§4]] and the [[04-robotics/modern-robotics/index|MR chapters]]. This is where geometry stops being enough, the moment the robot touches something.*

Once a robot touches the world, geometry alone is insufficient. Contact introduces forces, friction, impacts, changing modes, deformation, and uncertainty. These effects are central to grasping, assembly, excavation, wiping, drilling, and handling flexible materials.

> [!info] Depth target
> Read contact-rich manipulation papers by identifying the contact model, sensing, control mode, material assumptions, and evaluation. Detailed complementarity solvers and continuum mechanics remain optional working/mastery topics.

> [!note] Prerequisites
> Plants **P2** and **P3** ([[02-foundations/lab-plants|0.6 Lab Plants]]; a *plant* is control's word for the system being controlled): P2 is the catalog's planar two-link arm, and P3 its one-axis haptic handle, whose $400\,\mathrm{N/m}$ virtual wall sets this page's panel stiffness · [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/optimization|Optimization]] (quadratic programs, §5) · springs, preload and Coulomb friction ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §3–§4]]) · the wrench ([[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §6]]) · [[04-robotics/modern-robotics/ch05-velocity-kinematics|Statics and Jacobians]] · [[04-robotics/modern-robotics/ch08-dynamics|Dynamics]]

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this page opens the contact, force and tactile-feedback layer — the point where geometry stops being enough — and in *"install that panel on the frame"* it serves *detect contact* (whether a contact exists at all, §1, and which mode it is in, §7) and *perform the fitting* (how much force the contact can carry, §2 and §4, and what a controller should regulate, §5–§6); its chip sits in the contact-and-force band of the [[physical-ai-map|Physical AI Map]]. Without it friction looks like a constant you know: at the Worked case's $2\,\mathrm N$ press the $1\,\mathrm N$ wipe sits exactly on the $\mu f_n$ bound, and the two-finger grip on the $1\,\mathrm{kg}$ panel holds by $1.9\,\%$, so dust that drops $\mu$ from $0.5$ to $0.40$ drops the panel without moving it one pixel in the camera. [[04-robotics/force-compliance-control|13. Force & Compliance Control]] builds its §1 stiffness scale on §6's wall, its §2 admittance on §5 and its §5 contact transitions on §2 and §7; [[04-robotics/grasping|15. Grasping §2]] builds its friction cones and their linearization losses on §2, [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing §1 and §3]] its contact states on §1–§2, and [[04-robotics/capstone-panel-contact|26. Capstone §4]] its contact switch on §7 — block 2 of the dissertation path ([[07-research-program/index|7. Research Program §8]], robotics sessions 82–85), with 13 and 15 following in block 3. After it you can say whether a contact exists and what it can carry, say which way a linearized friction cone errs, tell position, force, impedance and admittance control apart by what each commands and measures, and ask a contact-rich paper for its $\mu$, its contact stiffness and its contact-state estimate.

> [!note] First pass · 처음이라면
> About four 60–90-minute sessions, robotics 82–85. **Session 1:** the Running object, the picture and the Worked case by hand — Steps 1–3 and 5–6; Step 4 only points to §2 and waits for session 3. End by redoing Step 6 at $\mu=0.45$ with the answers covered ($9.0\,\mathrm N<9.81\,\mathrm N$: the panel drops). **Session 2:** §1 (its note on the linear complementarity problem, LCP, is second pass), §5 and §6, where the four control modes meet one wall, and §8, where the same $\mu$ becomes a randomization range. **Session 3:** §2–§4 — the friction cone and its two linearizations, the penalty model, the wrench and closure. **Session 4:** §7 and §9 — §7 leans on [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing §1]], so read that section when you reach it — then the self-check and the problem set. The collapsed *Deeper* notes are second pass.

> [!tip] From sensing contact to displaying it
> This page explains robot-side contact. Continue to [[04-robotics/haptics-teleoperation/tactile-display-design|Tactile Display Design]] when the contact cue must be rendered to a person, and to [[04-robotics/haptics-teleoperation/rendering-sampling-stability|Rendering, Sampling & Stability]] when a virtual wall or force-feedback loop must remain stable.

### Running object: P2 against a P3-stiffness panel

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the planar 2R arm, $L_1=L_2=1\,\mathrm{m}$ — at the frozen pose $\theta=(0^\circ,90^\circ)$, where the tip sits at $(1,1)\,\mathrm{m}$, carrying a tool that presses a flat panel. The panel's face is the plane $x=1\,\mathrm{m}$, and the forearm passes beside the panel, out of the drawing plane, so only the tool touches it — in the drawing plane itself link 2 would lie flush along the face over its whole length ([[04-robotics/modern-robotics/ch02-configuration-space|MR ch.2]]), and the 5 mm press below would drive the forearm into the panel. The tool is an L: it reaches back into the page from the tip, in front of the face, and only its short foot meets the face, along $\hat n$ — a straight stub from the tip would lie in the face plane and touch it along its whole length. Reaching into the page adds moments only about axes in the drawing plane, which the joints' bearings carry, so the joint torques are those of the same force applied at the tip $(1,1)$. The panel's stiffness is **P3**'s wall value. This is the catalog's robotics running task — *move a tool to a panel and make controlled contact* — with the panel standing up, where the question is friction. [[04-robotics/force-compliance-control|13. Force & Compliance Control]] takes the same arm and tool with the panel lying under the tip, where the question is the relation between motion and force.

| Symbol | Value | What it is |
|---|---:|---|
| $\hat n$ | $+x$ | contact normal, counted positive **into** the panel |
| $\hat t_1,\ \hat t_2$ | $-y$, $-z$ | the two tangent directions in the panel's face, signed so that $\hat n\times\hat t_1=\hat t_2$ (a right-handed frame) |
| $k_w$ | $400\,\mathrm{N/m}$ | panel stiffness — P3's virtual-wall value |
| $d_c$ | $4\,\mathrm{N\cdot s/m}$ | contact damping for §3's penalty model — this page's only addition to P3 |
| $\mu$ | $0.5$ | friction coefficient, tool on panel |
| $\delta$ | $5\,\mathrm{mm}$ | commanded penetration past the face |
| $\dot\delta$ | $0.02\,\mathrm{m/s}$ | closing speed, held from first touch until the tool stops at $\delta=5\,\mathrm{mm}$ |
| $m_p$ | $1.0\,\mathrm{kg}$ | the panel's own mass, for when it is picked up (§4) |
| $f_g$ | $10\,\mathrm{N}$ | each finger's squeeze when two fingers at $\pm0.05\,\mathrm{m}$ hold the picked-up panel (§4) |
| $r_b$ | $0.40\,\mathrm{m}$ | how far below the contact the panel's mounting bracket, the origin of its wrench, sits (§4) |
| $g$ | $9.81\,\mathrm{m/s^2}$ | gravity, acting in $-y$ |

**Which body the force acts on.** Throughout the page $f$ is the force the tool applies to the panel, split into its normal part $f_n$ along $\hat n$ and its tangential part $f_t$ in the face; the panel pushes the tool back with $-f$. That is the convention of [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5]]'s press, and it is why $\hat n$ counts positive into the panel, as P3's $+x$ counts into its wall.

**How soft this panel is.** $k_w=400\,\mathrm{N/m}$ is P3's rendered wall, softer than the foam row of the stiffness scale in [[04-robotics/force-compliance-control|13. §1]], so read the panel as compliantly mounted. A structural panel met through a real tool and arm is $10^4$–$10^5\,\mathrm{N/m}$ (13 §1), and there the same 5 mm press would ask for 50–500 N (§6 prices the difference).

Two tangents and not one, although P2 is planar, because the *contact* is three-dimensional even though the *arm* moves in a plane; §2 says what the second tangent costs.

*Scope: this page teaches the mechanics of one contact — when a contact exists, how much force it can carry, how that force becomes an object wrench, and what closure does and does not promise — plus how to read a contact-rich paper's sensing and evaluation. It does not teach how to choose a controller for that contact ([[04-robotics/force-compliance-control|13. Force & Compliance Control]]), how to plan or score a grasp ([[04-robotics/grasping|Grasping]]), how a tactile signal is rendered back to a person ([[04-robotics/haptics-teleoperation/tactile-display-design|24.2 Tactile Display Design]]), or how a contact simulator's solver is built ([[06-research-practice/simulators-benchmarks-datasets|research practice 7. Simulators, Benchmarks & Datasets]]).*

### The picture: the contact frame on the panel, with the cone standing on it

<svg viewBox="0 0 560 466" style="max-width:100%;height:auto" role="img" aria-label="Left: P2 at theta (0, 90 degrees) in the x-y plane, the panel face x = 1 m set back behind that plane, the L-shaped tool reaching back from the tip with its foot on the face, the contact frame, the 400 N/m contact spring magnified, and the contact force drawn apart: the tool pushes the panel with (2, -1) N and the panel pushes the tool with (-2, 1) N; right: the friction cone of half-angle 26.6 degrees with, at a normal force of 2.00 N, the 1.00 N circle, the outer box with corner 1.414 N, the inner four-generator square with flat side 0.707 N, and the 1 N wipe on the panel; bottom: the gap axis with its two complementarity rays and the points +2 mm and -5 mm">
  <defs><marker id="cftA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="cftB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor">
    <text x="12" y="22" font-size="12" fill-opacity="0.85" font-weight="600">arm (x–y plane, to scale), panel set back</text>
    <line x1="18.2" y1="259" x2="61.8" y2="259" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <path d="M 20.8 259 L 15.8 265 M 26.3 259 L 21.3 265 M 31.8 259 L 26.8 265 M 37.3 259 L 32.3 265 M 42.8 259 L 37.8 265 M 48.3 259 L 43.3 265 M 53.8 259 L 48.8 265" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
    <path d="M 40 250 L 33 259 L 47 259 Z" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
    <path d="M 181.6 157.1 L 181.6 64.9 L 197.4 49.1 L 197.4 141.2 Z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.75"/>
    <path d="M 197.4 59.1 L 203.4 54.1 M 197.4 69.3 L 203.4 64.3 M 197.4 79.5 L 203.4 74.5 M 197.4 89.7 L 203.4 84.7 M 197.4 99.9 L 203.4 94.9 M 197.4 110.1 L 203.4 105.1 M 197.4 120.3 L 203.4 115.3 M 197.4 130.5 L 203.4 125.5 M 197.4 140.7 L 203.4 135.7" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <line x1="40" y1="250" x2="168" y2="250" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="168" y1="250" x2="168" y2="122" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <polyline points="168,122 179.3,100.5 186.9,100.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="40" cy="250" r="4.5" fill="currentColor"/>
    <circle cx="168" cy="250" r="4" fill="currentColor"/>
    <circle cx="168" cy="122" r="4.5" fill="currentColor"/>
    <circle cx="189.5" cy="100.5" r="2.6" fill="currentColor"/>
    <line x1="193.5" y1="100.5" x2="229.5" y2="100.5" stroke="currentColor" stroke-width="1.6" marker-end="url(#cftA)"/>
    <line x1="189.5" y1="104.5" x2="189.5" y2="138.5" stroke="currentColor" stroke-width="1.6" marker-end="url(#cftA)"/>
    <text x="203.5" y="93.5" font-size="11">n&#770; into panel</text>
    <text x="202.4" y="138.5" font-size="11" xml:space="preserve">t&#770;<tspan dy="3.1" font-size="11">1</tspan><tspan dy="-3.1"> wipe (−y)</tspan></text>
    <text x="202.4" y="57.1" font-size="11">face x = 1 m</text>
    <text x="12" y="281" font-size="11">base (0, 0)</text>
    <text x="168" y="281" font-size="11" text-anchor="middle">elbow (1, 0)</text>
    <text x="160" y="118" font-size="11" text-anchor="end">tip (1, 1)</text>
    <text x="179.5" y="92.5" font-size="11" text-anchor="end">tool</text>
    <text x="104" y="242" font-size="11" text-anchor="middle" fill-opacity="0.85">P2, θ = (0°, 90°)</text>
    <rect x="46" y="150" width="104" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <line x1="128" y1="170" x2="128" y2="206" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 128 172.0 L 136 178.0 M 128 178.5 L 136 184.5 M 128 185.0 L 136 191.0 M 128 191.5 L 136 197.5 M 128 198.0 L 136 204.0 M 128 204.5 L 136 210.5" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <line x1="52" y1="186" x2="88" y2="186" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
    <line x1="88" y1="179" x2="88" y2="193" stroke="currentColor" stroke-width="1.6"/>
    <path d="M 88 186 L 91 186 L 92.7 191 L 96.1 181 L 99.5 191 L 102.9 181 L 106.3 191 L 109.7 181 L 113.1 191 L 116.5 181 L 119.9 191 L 123.3 181 L 125 186 L 128 186" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
    <line x1="78" y1="177" x2="78" y2="198" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
    <line x1="78" y1="198" x2="88" y2="198" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <line x1="88" y1="194" x2="88" y2="201" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <text x="52" y="165" font-size="11" xml:space="preserve">k<tspan dy="3.1" font-size="11">w</tspan><tspan dy="-3.1"> = 400 N/m</tspan></text>
    <text x="54" y="209" font-size="11">δ = 5 mm</text>
    <text x="46" y="226" font-size="10.5" fill-opacity="0.8">magnified, not to scale</text>
    <line x1="150" y1="150" x2="185.5" y2="103.5" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="3 2"/>
    <line x1="244" y1="155.5" x2="244" y2="217.5" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 244 159.5 L 250.0 154.5 M 244 167.5 L 250.0 162.5 M 244 175.5 L 250.0 170.5 M 244 183.5 L 250.0 178.5 M 244 191.5 L 250.0 186.5 M 244 199.5 L 250.0 194.5 M 244 207.5 L 250.0 202.5 M 244 215.5 L 250.0 210.5" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <circle cx="212.0" cy="180.0" r="3.5" fill="currentColor"/>
    <path d="M 219.1 174.8 L 239.3 184.9 L 241.2 181.2 L 245.9 189.7 L 236.3 191.0 L 238.2 187.3 L 217.9 177.1 Z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
    <line x1="240.1" y1="201.3" x2="212.7" y2="187.6" stroke="currentColor" stroke-width="1.3" marker-end="url(#cftA)"/>
    <text x="234.2" y="175.8" font-size="11">f</text>
    <text x="220.6" y="207.6" font-size="11">−f</text>
    <text x="205.0" y="184.0" font-size="10.5" text-anchor="end">tool</text>
    <text x="204" y="230.0" font-size="10.5">f = (2, −1) N: tool on panel</text>
    <text x="204" y="243.0" font-size="10.5">−f: panel on tool</text>
    <text x="204" y="256.0" font-size="10.5">τ = Jᵀf = (−3, −2) N·m</text>
    <text x="12" y="300" font-size="10.5" fill-opacity="0.85">panel set back from the drawing plane: the forearm passes beside it, only the tool’s foot touches</text>
    <text x="280" y="22" font-size="12" fill-opacity="0.85" font-weight="600">the cone, in the contact frame</text>
    <line x1="368" y1="226" x2="368" y2="60.8" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" marker-end="url(#cftA)"/>
    <line x1="368" y1="226" x2="449.2" y2="226" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" marker-end="url(#cftA)"/>
    <line x1="368" y1="226" x2="392.9" y2="201.1" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" marker-end="url(#cftA)"/>
    <text x="375" y="68.8" font-size="12">n&#770;</text>
    <text x="455.2" y="230" font-size="12" xml:space="preserve">t&#770;<tspan dy="3.4" font-size="11">1</tspan></text>
    <text x="398.9" y="213.1" font-size="12" xml:space="preserve">t&#770;<tspan dy="3.4" font-size="11">2</tspan></text>
    <path d="M 368 226 L 428.9 107.5 L 307 131.4 Z" fill="currentColor" fill-opacity="0.06"/>
    <line x1="368" y1="226" x2="307" y2="131.4" stroke="currentColor" stroke-width="1.4"/>
    <line x1="368" y1="226" x2="428.9" y2="107.5" stroke="currentColor" stroke-width="1.4"/>
    <line x1="368" y1="226" x2="388" y2="133.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <line x1="368" y1="226" x2="308.8" y2="133.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <line x1="368" y1="226" x2="348" y2="94.4" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <line x1="368" y1="226" x2="427.2" y2="94.4" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <path d="M 424 114 L 423.3 114.7 L 422.5 115.5 L 421.7 116.2 L 420.8 116.9 L 419.9 117.6 L 419 118.3 L 418 119.1 L 417 119.8 L 416 120.5 L 414.9 121.2 L 413.8 121.9 L 412.7 122.6 L 411.5 123.3 L 410.3 123.9 L 409.1 124.6 L 407.9 125.3 L 406.6 125.9 L 405.3 126.6 L 404 127.2 L 402.6 127.9 L 401.3 128.5 L 399.9 129.1 L 398.5 129.7 L 397 130.3 L 395.6 130.9 L 394.1 131.4 L 392.6 132 L 391.1 132.5 L 389.5 133.1 L 388 133.6 L 386.4 134.1 L 384.9 134.6 L 383.3 135.1 L 381.7 135.5 L 380.1 136 L 378.5 136.4 L 376.9 136.8 L 375.3 137.2 L 373.6 137.6 L 372 138 L 370.4 138.4 L 368.7 138.7 L 367.1 139 L 365.5 139.3 L 363.8 139.6 L 362.2 139.9 L 360.6 140.1 L 358.9 140.4 L 357.3 140.6 L 355.7 140.8 L 354.1 141 L 352.5 141.1 L 351 141.3 L 349.4 141.4 L 347.8 141.5 L 346.3 141.6 L 344.8 141.6 L 343.3 141.7 L 341.8 141.7 L 340.3 141.7 L 338.8 141.7 L 337.4 141.7 L 336 141.6 L 334.6 141.6 L 333.2 141.5 L 331.9 141.4 L 330.5 141.3 L 329.2 141.1 L 328 141 L 326.7 140.8 L 325.5 140.6 L 324.3 140.4 L 323.2 140.1 L 322.1 139.9 L 321 139.6 L 319.9 139.3 L 318.9 139 L 317.9 138.7 L 316.9 138.4 L 316 138 L 315.1 137.6 L 314.3 137.2 L 313.4 136.8 L 312.7 136.4 L 311.9 136 L 311.2 135.5 L 310.6 135.1 L 309.9 134.6 L 309.3 134.1 L 308.8 133.6 L 308.3 133.1 L 307.8 132.5 L 307.4 132 L 307 131.4 L 306.7 130.9 L 306.4 130.3 L 306.1 129.7 L 305.9 129.1 L 305.8 128.5 L 305.6 127.9 L 305.6 127.2 L 305.5 126.6 L 305.5 125.9 L 305.6 125.3 L 305.7 124.6 L 305.8 123.9 L 306 123.3 L 306.2 122.6 L 306.4 121.9 L 306.7 121.2 L 307.1 120.5 L 307.5 119.8 L 307.9 119.1 L 308.4 118.3 L 308.9 117.6 L 309.4 116.9 L 310 116.2 L 310.6 115.5 L 311.3 114.7 L 312 114 L 312.7 113.3 L 313.5 112.5 L 314.3 111.8 L 315.2 111.1 L 316.1 110.4 L 317 109.7 L 318 108.9 L 319 108.2 L 320 107.5 L 321.1 106.8 L 322.2 106.1 L 323.3 105.4 L 324.5 104.7 L 325.7 104.1 L 326.9 103.4 L 328.1 102.7 L 329.4 102.1 L 330.7 101.4 L 332 100.8 L 333.4 100.1 L 334.7 99.5 L 336.1 98.9 L 337.5 98.3 L 339 97.7 L 340.4 97.1 L 341.9 96.6 L 343.4 96 L 344.9 95.5 L 346.5 94.9 L 348 94.4 L 349.6 93.9 L 351.1 93.4 L 352.7 92.9 L 354.3 92.5 L 355.9 92 L 357.5 91.6 L 359.1 91.2 L 360.7 90.8 L 362.4 90.4 L 364 90 L 365.6 89.6 L 367.3 89.3 L 368.9 89 L 370.5 88.7 L 372.2 88.4 L 373.8 88.1 L 375.4 87.9 L 377.1 87.6 L 378.7 87.4 L 380.3 87.2 L 381.9 87 L 383.5 86.9 L 385 86.7 L 386.6 86.6 L 388.2 86.5 L 389.7 86.4 L 391.2 86.4 L 392.7 86.3 L 394.2 86.3 L 395.7 86.3 L 397.2 86.3 L 398.6 86.3 L 400 86.4 L 401.4 86.4 L 402.8 86.5 L 404.1 86.6 L 405.5 86.7 L 406.8 86.9 L 408 87 L 409.3 87.2 L 410.5 87.4 L 411.7 87.6 L 412.8 87.9 L 413.9 88.1 L 415 88.4 L 416.1 88.7 L 417.1 89 L 418.1 89.3 L 419.1 89.6 L 420 90 L 420.9 90.4 L 421.7 90.8 L 422.6 91.2 L 423.3 91.6 L 424.1 92 L 424.8 92.5 L 425.4 92.9 L 426.1 93.4 L 426.7 93.9 L 427.2 94.4 L 427.7 94.9 L 428.2 95.5 L 428.6 96 L 429 96.6 L 429.3 97.1 L 429.6 97.7 L 429.9 98.3 L 430.1 98.9 L 430.2 99.5 L 430.4 100.1 L 430.4 100.8 L 430.5 101.4 L 430.5 102.1 L 430.4 102.7 L 430.3 103.4 L 430.2 104.1 L 430 104.7 L 429.8 105.4 L 429.6 106.1 L 429.3 106.8 L 428.9 107.5 L 428.5 108.2 L 428.1 108.9 L 427.6 109.7 L 427.1 110.4 L 426.6 111.1 L 426 111.8 L 425.4 112.5 L 424.7 113.3 Z" fill="currentColor" fill-opacity="0.1"/>
    <path d="M 396.3 141.7 L 284.3 141.7 L 339.7 86.3 L 451.7 86.3 Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" stroke-dasharray="6 3"/>
    <path d="M 388 133.6 L 308.8 133.6 L 348 94.4 L 427.2 94.4 Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9"/>
    <path d="M 424 114 L 423.3 114.7 L 422.5 115.5 L 421.7 116.2 L 420.8 116.9 L 419.9 117.6 L 419 118.3 L 418 119.1 L 417 119.8 L 416 120.5 L 414.9 121.2 L 413.8 121.9 L 412.7 122.6 L 411.5 123.3 L 410.3 123.9 L 409.1 124.6 L 407.9 125.3 L 406.6 125.9 L 405.3 126.6 L 404 127.2 L 402.6 127.9 L 401.3 128.5 L 399.9 129.1 L 398.5 129.7 L 397 130.3 L 395.6 130.9 L 394.1 131.4 L 392.6 132 L 391.1 132.5 L 389.5 133.1 L 388 133.6 L 386.4 134.1 L 384.9 134.6 L 383.3 135.1 L 381.7 135.5 L 380.1 136 L 378.5 136.4 L 376.9 136.8 L 375.3 137.2 L 373.6 137.6 L 372 138 L 370.4 138.4 L 368.7 138.7 L 367.1 139 L 365.5 139.3 L 363.8 139.6 L 362.2 139.9 L 360.6 140.1 L 358.9 140.4 L 357.3 140.6 L 355.7 140.8 L 354.1 141 L 352.5 141.1 L 351 141.3 L 349.4 141.4 L 347.8 141.5 L 346.3 141.6 L 344.8 141.6 L 343.3 141.7 L 341.8 141.7 L 340.3 141.7 L 338.8 141.7 L 337.4 141.7 L 336 141.6 L 334.6 141.6 L 333.2 141.5 L 331.9 141.4 L 330.5 141.3 L 329.2 141.1 L 328 141 L 326.7 140.8 L 325.5 140.6 L 324.3 140.4 L 323.2 140.1 L 322.1 139.9 L 321 139.6 L 319.9 139.3 L 318.9 139 L 317.9 138.7 L 316.9 138.4 L 316 138 L 315.1 137.6 L 314.3 137.2 L 313.4 136.8 L 312.7 136.4 L 311.9 136 L 311.2 135.5 L 310.6 135.1 L 309.9 134.6 L 309.3 134.1 L 308.8 133.6 L 308.3 133.1 L 307.8 132.5 L 307.4 132 L 307 131.4 L 306.7 130.9 L 306.4 130.3 L 306.1 129.7 L 305.9 129.1 L 305.8 128.5 L 305.6 127.9 L 305.6 127.2 L 305.5 126.6 L 305.5 125.9 L 305.6 125.3 L 305.7 124.6 L 305.8 123.9 L 306 123.3 L 306.2 122.6 L 306.4 121.9 L 306.7 121.2 L 307.1 120.5 L 307.5 119.8 L 307.9 119.1 L 308.4 118.3 L 308.9 117.6 L 309.4 116.9 L 310 116.2 L 310.6 115.5 L 311.3 114.7 L 312 114 L 312.7 113.3 L 313.5 112.5 L 314.3 111.8 L 315.2 111.1 L 316.1 110.4 L 317 109.7 L 318 108.9 L 319 108.2 L 320 107.5 L 321.1 106.8 L 322.2 106.1 L 323.3 105.4 L 324.5 104.7 L 325.7 104.1 L 326.9 103.4 L 328.1 102.7 L 329.4 102.1 L 330.7 101.4 L 332 100.8 L 333.4 100.1 L 334.7 99.5 L 336.1 98.9 L 337.5 98.3 L 339 97.7 L 340.4 97.1 L 341.9 96.6 L 343.4 96 L 344.9 95.5 L 346.5 94.9 L 348 94.4 L 349.6 93.9 L 351.1 93.4 L 352.7 92.9 L 354.3 92.5 L 355.9 92 L 357.5 91.6 L 359.1 91.2 L 360.7 90.8 L 362.4 90.4 L 364 90 L 365.6 89.6 L 367.3 89.3 L 368.9 89 L 370.5 88.7 L 372.2 88.4 L 373.8 88.1 L 375.4 87.9 L 377.1 87.6 L 378.7 87.4 L 380.3 87.2 L 381.9 87 L 383.5 86.9 L 385 86.7 L 386.6 86.6 L 388.2 86.5 L 389.7 86.4 L 391.2 86.4 L 392.7 86.3 L 394.2 86.3 L 395.7 86.3 L 397.2 86.3 L 398.6 86.3 L 400 86.4 L 401.4 86.4 L 402.8 86.5 L 404.1 86.6 L 405.5 86.7 L 406.8 86.9 L 408 87 L 409.3 87.2 L 410.5 87.4 L 411.7 87.6 L 412.8 87.9 L 413.9 88.1 L 415 88.4 L 416.1 88.7 L 417.1 89 L 418.1 89.3 L 419.1 89.6 L 420 90 L 420.9 90.4 L 421.7 90.8 L 422.6 91.2 L 423.3 91.6 L 424.1 92 L 424.8 92.5 L 425.4 92.9 L 426.1 93.4 L 426.7 93.9 L 427.2 94.4 L 427.7 94.9 L 428.2 95.5 L 428.6 96 L 429 96.6 L 429.3 97.1 L 429.6 97.7 L 429.9 98.3 L 430.1 98.9 L 430.2 99.5 L 430.4 100.1 L 430.4 100.8 L 430.5 101.4 L 430.5 102.1 L 430.4 102.7 L 430.3 103.4 L 430.2 104.1 L 430 104.7 L 429.8 105.4 L 429.6 106.1 L 429.3 106.8 L 428.9 107.5 L 428.5 108.2 L 428.1 108.9 L 427.6 109.7 L 427.1 110.4 L 426.6 111.1 L 426 111.8 L 425.4 112.5 L 424.7 113.3 Z" fill="none" stroke="currentColor" stroke-width="1.9"/>
    <circle cx="388" cy="133.6" r="2.2" fill="currentColor"/>
    <circle cx="308.8" cy="133.6" r="2.2" fill="currentColor"/>
    <circle cx="348" cy="94.4" r="2.2" fill="currentColor"/>
    <circle cx="427.2" cy="94.4" r="2.2" fill="currentColor"/>
    <line x1="368" y1="226" x2="424" y2="114" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.75"/>
    <path d="M 388.6 184.9 A 46 46 0 0 0 368 180" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
    <line x1="380.6" y1="182.2" x2="430" y2="200" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="433" y="204" font-size="11">arctan μ = 26.6°</text>
    <line x1="368" y1="114" x2="421.8" y2="114" stroke="currentColor" stroke-width="2.2" marker-end="url(#cftA)"/>
    <circle cx="368" cy="114" r="2.4" fill="currentColor"/>
    <text x="280" y="60" font-size="11" fill-opacity="0.85">slice at</text>
    <text x="280" y="73" font-size="11" fill-opacity="0.85" xml:space="preserve">f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 2.00 N</tspan></text>
    <line x1="300" y1="78" x2="284.3" y2="141.7" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <line x1="453.7" y1="84.3" x2="455" y2="50" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="46" font-size="11">outer box,</text>
    <text x="458" y="59" font-size="11">corner 1.414 N</text>
    <line x1="432.5" y1="101.7" x2="455" y2="101" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="98" font-size="11">circle</text>
    <text x="458" y="111" font-size="11" xml:space="preserve">μf<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 1.00 N</tspan></text>
    <line x1="376.3" y1="127.5" x2="455" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="147" font-size="11">inner 4-generator,</text>
    <text x="458" y="160" font-size="11">flat side 0.707 N</text>
    <line x1="427" y1="116" x2="455" y2="125" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="129" font-size="11">1 N wipe, on panel</text>
  </g>
  <g fill="currentColor" transform="translate(0,34)">
    <line x1="8" y1="282" x2="552" y2="282" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
    <text x="12" y="300" font-size="12" fill-opacity="0.85" font-weight="600">the gap axis</text>
    <line x1="98.8" y1="382" x2="451.6" y2="382" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
    <line x1="250" y1="382" x2="250" y2="316" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6" marker-end="url(#cftB)"/>
    <path d="M 138 382 L 138 386 M 194 382 L 194 386 M 250 382 L 250 386 M 306 382 L 306 386 M 362 382 L 362 386 M 418 382 L 418 386" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="138" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">+4</text>
    <text x="194" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">+2</text>
    <text x="250" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">0</text>
    <text x="306" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">−2</text>
    <text x="362" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">−4</text>
    <text x="418" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">−6</text>
    <text x="457.6" y="386" font-size="11" fill-opacity="0.85">φ (mm)</text>
    <text x="244" y="318" font-size="11" text-anchor="end" fill-opacity="0.85" xml:space="preserve">f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> (N)</tspan></text>
    <line x1="250" y1="382" x2="104.4" y2="382" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="250" y1="382" x2="250" y2="320.8" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="250" y1="382" x2="434.8" y2="318.6" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="5 3"/>
    <circle cx="194" cy="382" r="4.5" fill="currentColor"/>
    <circle cx="390" cy="334" r="4.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
    <text x="12" y="378" font-size="12">φ &gt; 0, apart:</text>
    <text x="12" y="393" font-size="12" xml:space="preserve">f<tspan dy="3.4" font-size="11">n</tspan><tspan dy="-3.4"> = 0</tspan></text>
    <text x="258" y="325.6" font-size="12" xml:space="preserve">φ = 0: f<tspan dy="3.4" font-size="11">n</tspan><tspan dy="-3.4"> ≥ 0</tspan></text>
    <text x="194" y="356" font-size="11" text-anchor="middle">+2 mm,</text>
    <text x="194" y="370" font-size="11" text-anchor="middle">before touch</text>
    <text x="400" y="342" font-size="11" xml:space="preserve">−5 mm, f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 2.00 N</tspan></text>
    <text x="400" y="356" font-size="11" fill-opacity="0.85">penalty allows, rigid forbids</text>
    <text x="311.6" y="375" font-size="11" fill-opacity="0.85" xml:space="preserve">penalty f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = k</tspan><tspan dy="3.1" font-size="11">w</tspan><tspan dy="-3.1">δ</tspan></text>
    <text x="12" y="420" font-size="12" fill-opacity="0.9" xml:space="preserve">(φ, f<tspan dy="3.4" font-size="11">n</tspan><tspan dy="-3.4">) never leaves the two bold rays — that picture is complementarity</tspan></text>
    <path d="M 246 358 L 250 358 M 246 334 L 250 334" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
    <text x="242" y="362" font-size="10.5" text-anchor="end" fill-opacity="0.85">1</text>
    <text x="242" y="338" font-size="10.5" text-anchor="end" fill-opacity="0.85">2</text>
  </g>
</svg>

Left: P2 at $\theta=(0^\circ,90^\circ)$, to scale in the $x$–$y$ plane, with the panel's face $x=1\,\mathrm m$ drawn set back behind that plane, so that the forearm passes beside it and only the short foot of the L-shaped tool, reaching back from the tip in front of the face, touches it; at the contact, the frame — $\hat n$ into the panel, $\hat t_1$ down the face along the wipe — the $k_w=400\,\mathrm{N/m}$ contact spring compressed by $\delta=5\,\mathrm{mm}$, magnified, and the contact force drawn apart: the tool pushes the panel with $f=(2.00,-1.00)\,\mathrm N$, the panel pushes the tool with $-f$, and holding that press costs the joints $\tau=J^\top f=(-3,-2)\,\mathrm{N{\cdot}m}$. Right: the friction cone of half-angle $\arctan\mu=26.6^\circ$, sliced at $f_n=2.00\,\mathrm N$, where the $\mu f_n=1.00\,\mathrm N$ circle lies between the outer box (corner $1.414\,\mathrm N$) and the inner four-generator square (flat side $0.707\,\mathrm N$), and the $1\,\mathrm N$ wipe on the panel, at the same scale, ends exactly on the circle and outside the square. Bottom: the gap axis, where $(\phi,f_n)$ never leaves the two bold rays of complementarity — $f_n=0$ at $+2\,\mathrm{mm}$ before touch, and the $-5\,\mathrm{mm}$ penetration at $2.00\,\mathrm N$ that the penalty model allows and the rigid model forbids.

### Worked case: one contact, from gap to grip margin

Six steps on the object above, each proved by the section named in its heading; Step 4 belongs to §2 and is only pointed to here. The problem set reworks Steps 2–4 and 6, and the picture, with two of the table's entries changed.

**Step 1 — is there a contact at all? (§1).** Hold the tool 2 mm short of the face. The gap $\phi$ — the distance from tool to face, positive while they are apart and never negative for rigid bodies (§1) — is $\phi=0.002$ m and $f_n=0$ N, so $\phi f_n=0$ and the pair sits on the left ray. Drive to the face: $\phi=0$, and now $f_n$ may be anything non-negative — the model has stopped predicting the force and started only constraining it. That switch is the whole difficulty: the two cases are different sets of equations, so the number that decides which one holds is a *measurement*, not a command.

**Step 2 — how much normal force? (§3).** The rigid model cannot answer, because at $\phi=0$ it only says $f_n\ge0$. Commanding $\delta=5$ mm past the face makes the rigid model infeasible, so use the penalty model, which trades non-penetration for a spring and a damper, $k_w$ and $d_c$ of the table. The tool keeps closing at $\dot\delta=0.02$ m/s from first touch until it stops at 5 mm, so at first touch the damper alone pushes $d_c\dot\delta=4\times0.02=0.08$ N, and just before the tool stops

$$f_n=k_w\,\delta+d_c\,\dot\delta=400\times0.005+4\times0.02=2.00+0.08=2.08\ \mathrm{N}$$

so at rest the panel carries $f_n=2.00$ N and the extra $0.08$ N exists only while the tool is still closing. Hold that 2 N: every bound below is proportional to it.

**Step 3 — how much wipe will the contact carry? (§2).** The cone's half-angle is $\arctan 0.5=26.5651^\circ\to26.6^\circ$, and at $f_n=2.00$ N it allows

$$\lVert f_t\rVert\le\mu f_n=0.5\times2.00=1.00\ \mathrm{N}$$

because the tangential force may grow only to $\mu$ times the normal one. A 3 N downward wipe is three times the bound, so the tool slides down the face and friction sits on the bound, against the slip: on the tool it pushes $1.00$ N up the face, and by the third law the panel is dragged $1.00$ N down — $f_t=+1.00$ N along $\hat t_1$, since $f$ is the force on the panel (the Running object's convention). A 1 N wipe sits *exactly* on the bound: allowed, with zero margin. That is the honest reading of "it sticks" — the model permits it and nothing in the model says it will survive a 1% change in $\mu$. Holding the 1 N wipe under the 2 N press, $f=(2.00,-1.00)$ N in $(x,y)$, costs the joints $\tau=J^\top f=(-3,-2)$ N·m by the statics of [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §3]], whose problem 2(e) presses this same face with 10 N.

**Step 4 — what is a solver allowed to believe? (§2).** A planner that must stay a quadratic program replaces the round cone by flat facets, and on this very contact the two standard replacements err in opposite directions: the outer box would authorise a $1.414$ N wipe that slips, and the four-generator inner cone would refuse the 1 N wipe the real contact carries, allowing only $0.707$ N. §2 works both on the running object; on a first pass take the two numbers and move on.

**Step 5 — the same contact as an object wrench (§4).** Put the panel's frame origin on its mounting bracket, $r_b=0.40$ m below the contact, so $r=(0,0.40,0)$ m, and take the full contact force with the 1 N wipe, $f=(2.00,-1.00,0)$ N — the force the tool applies to the panel. The object feels a **wrench**: the moment $m=r\times f$ that force makes about the origin, stacked on the force itself, in Modern Robotics' order ([[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §6]]; §4 here). Then $m=r\times f=(0,0,-0.80)$ N·m and

$$\mathcal{F}=\begin{pmatrix}m\\ f\end{pmatrix}=(0,\ 0,\ -0.80,\ 2.00,\ -1.00,\ 0)$$

so the panel feels a 0.80 N·m moment about $z$ that nobody commanded. It appeared only because the origin moved 0.40 m; the physical push is unchanged. Move the origin to the contact and the moment is zero.

**Step 6 — and the grip that has to hold the panel afterwards (§4).** Two fingers squeeze the 1.0 kg panel at $\pm0.05$ m with $f_g=10$ N each. Each cone admits $\mu\times10=5$ N of tangential force, so the pair carries $2\times5=10.0$ N against a weight of $m_pg=1.0\times9.81=9.81$ N. The margin is $0.19$ N, which is $1.9\%$ of the load. Equivalently, the coefficient at which the grip exactly holds is

$$\mu^\star=\frac{m_pg}{2f_g}=\frac{9.81}{2\times10}=0.4905$$

since the two cones together must carry the whole weight. The nominal $\mu=0.5$ clears it by $1.9\%$. Dust dropping $\mu$ to $0.40$ takes the capacity to 8.0 N, short of the weight by 1.81 N: the panel goes to the floor. The same bound holds a facade panel on a site: S1, the construction track's 20 kg panel task ([[05-construction-robotics/site-engineering|2.5]]), hangs on vacuum cups at the wall, and [[02-foundations/fluid-power|0.6.3 Fluid Power §9]] computes the cups' $1885$ N normal force carrying at most $0.5\times1885=942$ N along the vertical face against the panel's $196.2$ N — a factor of $4.80$, and a multiple of the same unmeasured $\mu$.

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

The three are written together as $0\le\phi(q)\perp f_n\ge 0$, where $\perp$ means "their product is zero". Because each case (apart with $f_n=0$, or touching with $f_n\ge0$) is a different set of equations, the dynamics switch between **contact modes**, which is what makes contact hybrid and nonsmooth. Stacking these conditions for every contact turns one simulation step into a **linear complementarity problem** (LCP), the form rigid-body simulators solve ([[06-research-practice/simulators-benchmarks-datasets|research practice 7. Simulators, Benchmarks & Datasets]]); the note below writes it out and solves it for a block on a table, and the page's Depth target leaves solvers to a second pass.

> [!example] Worked example · 계산 예제
> A 0.1 kg block held 2 mm above a table has $\phi=0.002$ m and $f_n=0$, so $\phi f_n=0$ ✓. Set it down and at rest $\phi=0$ and $f_n=mg=0.1\times9.81=0.981$ N, again $\phi f_n=0$ ✓.
> **Non-examples**: $\phi=0.001$ m with $f_n=0.5$ N violates complementarity (a force across an open gap), $f_n=-0.5$ N violates unilaterality (the table pulling the block down), and $\phi<0$ violates non-penetration; a penalty model (§3) deliberately allows that last one.

> [!note]- Deeper · 더 깊이
> **How a simulator solves it: the LCP.** An LCP is a *problem*, not a model: given a square matrix $M$ and a vector $q$ (the standard letters; this $q$ is not the configuration), find vectors $z$ and $w$ with
>
> $$z\ge0,\qquad w=Mz+q\ge0,\qquad z^\top w=0$$
>
> — the same three conditions as above, one pair $(z_i,w_i)$ per contact. In a time-stepping simulator $z_i$ is contact $i$'s normal impulse over the step and $w_i$ its normal velocity after it, because once a gap has closed the condition moves from position to velocity: the surfaces either separate ($w_i>0$, no impulse) or stay together ($w_i=0$, an impulse $z_i\ge0$), never both.
>
> **The same block as an LCP**, one step of $h=0.01$ s: the velocity after the step is $w=v-gh+z/m$, so $M=1/m=10\ \mathrm{kg^{-1}}$ and $q=v-gh=0-0.0981=-0.0981$ m/s. $z=0$ would leave $w=q<0$, the block sinking into the table, so the solution is $w=0$ and $z=-q/M=0.00981$ N·s — an average force $z/h=0.981$ N $=mg$, the resting force above, found by the solver. **Non-example**: the block moving up at $v=0.5$ m/s has $q=0.4019>0$, so the LCP returns $z=0$ and $w=0.4019$ m/s, and the block leaves. Solving the equation $w=0$ alone would instead give $z=-0.0402$ N·s, the table pulling the block down: the equality without its two inequalities is not an LCP.

### 2. Normal force and friction

A contact's friction coefficient decides whether a wipe sticks or a grasped panel slides, and it is the number nobody measures: dust on a grasped panel can change the usable friction while its visual pose stays nearly unchanged, so a planner that treats $\mu$ as known may overestimate the contact margin. This section bounds what one contact can carry and says which way each solver-friendly approximation of that bound errs.

In one dimension this is the Coulomb friction of [[02-foundations/basic-mechanics|0.6.1 §4]] (a callback): a sticking contact supplies whatever tangential force holds it still, up to $\mu$ times the normal force, and a sliding one opposes the slip with exactly that much. Here the tangential force is a vector in the face, so the bound reads

$$\lVert f_t\rVert\le \mu f_n$$

where $f_n$ is the normal force, $f_t$ the tangential force and $\mu$ the friction coefficient. A force inside the bound can be consistent with sticking; a force on the bound means slip is about to start, and a demand beyond it means the contact slides. The bound is a *force-feasibility bound* — whether the contact actually sticks or slides also depends on relative motion and the contact law.

**The friction cone and Coulomb's law, each part named.** Split the contact force $f\in\mathbb{R}^3$ — the force the tool applies to the panel, as in the Running object — into its normal component $f_n$ (a scalar along the unit normal) and its tangential component $f_t\in\mathbb{R}^2$ (in the contact plane), and let $v_t$ be the sliding velocity, in that plane, of the body $f$ acts on relative to the other: here the panel's velocity relative to the tool. The **friction cone** is the set of contact forces the model allows,

$$FC=\{\,f:\ f_n\ge 0,\ \lVert f_t\rVert\le\mu f_n\,\}$$

so it has two conditions: **unilaterality** ($f_n\ge0$, as in §1) and the **Coulomb bound** ($\lVert f_t\rVert\le\mu f_n$). It is a circular cone about the normal with half-angle $\arctan\mu$, because the bound says the force may tilt from the normal until tangential over normal equals $\mu$. **Coulomb's law** then adds which boundary the force sits on:

- **Sticking** ($v_t=0$): any $f\in FC$ is allowed, and $f_t$ is whatever holds the contact still.
- **Sliding** ($v_t\ne0$): the force is on the cone's surface and opposes the slip, since friction dissipates energy.
$$f_t=-\mu f_n\,\frac{v_t}{\lVert v_t\rVert}$$
  On the running object the tool slides down the face, so the panel moves up relative to it, $v_t$ points along $-\hat t_1$, and $f_t=+\mu f_n\hat t_1$: the panel is dragged down, as Step 3 found.

A single $\mu$ assumes that 0.6.1 §4's breakaway and sliding coefficients, $\mu_s$ and $\mu_k$, are equal.

**The linearized friction cone, and which way it errs.** The bound $\lVert f_t\rVert\le\mu f_n$ is a *second-order* cone: the constraint is a norm, not a set of linear inequalities. Any optimizer that needs a quadratic program ([[02-foundations/optimization|4. Optimization §5]]) therefore replaces it by a **polyhedral cone** — a cone bounded by finitely many flat facets. There are two standard replacements, they approximate from opposite sides, and calling both of them "the friction pyramid" is how the error gets lost. This is why the running object keeps two tangents although P2 is planar: with one tangent the cone is a wedge with exactly two edges, which a polyhedron represents exactly, and the whole question below — where half the contact literature's optimizers live — would disappear.

- The **outer box pyramid** bounds each tangential axis separately, $|f_{t,1}|\le\mu f_n$ and $|f_{t,2}|\le\mu f_n$ — four facets, two per axis. It **contains** the true cone, so it admits forces that would slip: its corners reach $\sqrt2$ times the true bound, $41.4\%$ too generous. This is the form [[04-robotics/convex-mpc-legged|8. Convex MPC]] uses in its fourth modelling move, and shrinking the coefficient to $\mu/\sqrt2$ is how that page buys the error back.
- The **inner polyhedral cone** is instead *spanned* by $m$ generator rays spaced evenly around the normal, each ray lying on the true cone's surface. Every force it admits is **inside** the true cone, since a nonnegative combination of rays on a convex cone cannot leave it. Its price is the friction it discards: its effective coefficient is $\mu\cos(\pi/m)$, which is $0.354$ at $m=4$ ($29.3\%$ of $\mu$ thrown away), $0.462$ at $m=8$ ($7.6\%$) and $0.490$ at $m=16$ ($1.9\%$) — losses in the largest tangential force the cone allows in its worst direction. The note below writes the generators out and gives the losses measured as area instead.

> [!note]- Deeper · 더 깊이
> **The generators, and two ways to count the loss.** The inner cone is spanned by its generators, so every force it admits has the form
>
> $$f=\sum_{j=1}^{m}\lambda_j\,g_j,\qquad \lambda_j\ge0,\qquad g_j=\hat n+\mu\left(\cos\tfrac{(2j-1)\pi}{m}\,\hat t_1+\sin\tfrac{(2j-1)\pi}{m}\,\hat t_2\right)$$
>
> where $\lambda_j$ is the non-negative weight on ray $j$ and $m$ is the facet count the modeller chooses. The half-step offset in the angle puts the middle of a facet, not a ray, on each tangent axis, so the wipe's own direction $\hat t_1$ is this cone's worst one; [[04-robotics/grasping|15. Grasping §2]] places its generators on the axes instead (angles $2\pi j/m$), where the four-generator cone would carry the 1 N wipe along $\hat t_1$ in full and lose its $29.3\%$ at $45^\circ$ — the worst-case coefficient $\mu\cos(\pi/m)$, the inscribed polygon's inradius, is the same in both layouts, and only which directions get it differs. Measured instead as the *area* of the tangential disc the polygon keeps, $\tfrac{m}{2\pi}\sin\tfrac{2\pi}{m}$ of it, the losses are $36.3\%$, $10.0\%$ and $2.6\%$ at $m=4$, $8$ and $16$; Grasping §2 quotes both, and a linearization loss quoted without saying which of the two it is cannot be compared with another.

**On the running object — the Worked case's Step 4.** At $f_n=2.00$ N the true bound is $1.00$ N in every direction. The outer box's corner allows $\sqrt{1.00^2+1.00^2}=1.414$ N, $41.4\%$ past the real bound, so it would authorise a wipe that slips. The four-generator inner cone allows only $0.354\times2.00=0.707$ N along $\hat t_1$, so it would refuse the 1 N wipe the real contact permits; eight generators allow $0.924$ N and sixteen $0.981$ N, $7.6\%$ and $1.9\%$ short of the bound.

At $m=4$ the inner cone's coefficient $\mu\cos(\pi/4)$ and the shrunk box's $\mu/\sqrt2$ are the same number, $0.354$ — with its rays at $45^\circ$ to the axes, as drawn, the four-generator cone *is* the shrunk box — which is why the two constructions are so easily confused. The box at full $\mu$ and the inner cone are still different sets, and the direction of the error is the point: **outer is optimistic about grip, inner is pessimistic, and neither is the cone.** Which one a paper solved decides whether its planner can promise a contact it cannot hold, or refuse one it could.

> [!example] Worked example · 계산 예제
> $\mu=0.5$ gives a half-angle $\arctan0.5=26.6°$. With $f_n=10$ N the cone allows $\lVert f_t\rVert\le5$ N: a 4 N tangential load can stick, and a 6 N demand cannot.
> **Non-example**: $f_n=-2$ N is outside the cone for every $\mu$, however small $f_t$ is, because a surface cannot pull. And the circular cone is not the same set as either polyhedral cone above, which is why a solver's reported friction margin is a margin against its own facets.

**The reading this gives you.** Ask how μ was obtained and whether slip feedback can correct a mistaken assumption before the object is lost. The force bound explains a possible failure mechanism; it does not substitute for observing the actual contact state.

### 3. Rigid and compliant models

Which contact model a result was obtained under matters, because an apparent controller improvement may come from a more forgiving simulated contact: a compliant wall can absorb a wiping path error that would produce a force spike against a stiffer surface. Three families of model are in use.

| Model | Useful when | Main limitation |
|---|---|---|
| Rigid contact | deformation is small relative to task scale | impacts and mode switches are nonsmooth |
| Penalty/compliant contact | simulation needs continuous penetration forces | stiffness and damping are hard to identify |
| Learned/residual model | repeatable mismatch remains in data | extrapolation and physical consistency |

**The penalty model, written out.** A penalty (compliant) contact drops §1's non-penetration condition and instead lets the bodies overlap by a small **penetration depth** $\delta=\max(0,-\phi)$, then pushes back like a spring and damper — the one-sided spring of [[02-foundations/basic-mechanics|0.6.1 §3]], which is P3's own wall, the section's non-example of a linear spring because it only pushes, with a damper beside it:

$$f_n=\max\!\big(0,\ k\,\delta+d\,\dot\delta\big)$$

so $k$ (contact stiffness, N/m) sets how much force a given overlap produces, $d$ (contact damping, N·s/m) resists the rate of overlap $\dot\delta$, and the outer $\max$ keeps unilaterality because the model must never pull. Example: $k=10^4$ N/m and a 1 mm overlap at rest give $f_n=10^4\times0.001=10$ N. It is continuous where the rigid model switches, which is why simulators like it, and its price is that $k$ and $d$ are numerical choices rather than measured material constants. The lab in [[06-research-practice/simulators-benchmarks-datasets|research practice 7. Simulators, Benchmarks & Datasets §3]] prices those choices on P3's handle: $k$ sets the largest stable step, $\Delta t<2\sqrt{m/k}$ for semi-implicit Euler, and a lightly damped contact keeps explicit Euler stable only while $d\ge k\,\Delta t$. A **learned residual** has the form $x_{t+1}=f_{\text{phys}}(x_t,u_t)+r_\theta(x_t,u_t)$, where $f_{\text{phys}}$ is the physics model's prediction and $r_\theta$ a fitted correction with parameters $\theta$.

Simulator contact parameters are often numerical compromises. Success under one simulator setting is not evidence of robustness to real material variation.

A learned residual (a model fitted to the part of the true dynamics that the physics-based model leaves unexplained) can correct repeatable mismatch, but only where its training observations constrain that correction. **The reading this gives you.** Separate the contact law, its parameter identification, and numerical settings. Then look for validation against the relevant physical response rather than success under one convenient simulator configuration.

### 4. Grasp and wrench language

Will the squeeze hold the panel? Two fingers pressing it from opposite sides make no net force at all, yet the grip can carry its weight, and this section gives the language that says how: the wrench each contact force makes, the grasp map that adds them, and the two closures built on it.

A contact force produces a force and a moment on the object; stacked into one six-vector they are a **wrench**, defined with its conditions in [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §6]] and mapped to joint torques by [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5]]. Recalled in two lines: a force $f$ applied at $r$ from the chosen object origin makes the wrench $(r\times f,\ f)$, moment on top in Modern Robotics' order; moving the origin changes the moment coordinates although the physical push is unchanged, so every contact must be expressed in one common frame before forces and moments are summed. Example: $f=(0,0,-10)$ N at $r=(0.2,0,0)$ m gives $m=r\times f=(0,2,0)$ N·m, so the object feels 10 N along $-z$ plus a 2 N·m moment about $y$.

The **grasp map** is the matrix that adds up all the contact forces into a single object wrench. Two closure notions build on it:

- **Form closure** immobilizes an object through geometry alone, under a specified contact model.
- **Force closure** uses admissible contact forces, commonly including friction, to resist arbitrary external wrenches.

Required contact counts depend on dimension, friction and contact assumptions, and general-position conditions, meaning the count assumes no degenerate, coincidental arrangement such as contact normals that happen to line up.

**The grasp map and the two closures as formulas.**

- The **grasp map** $G$ sums the wrenches of $k$ point contacts. Stack the contact forces into $f_c=(f_1,\dots,f_k)\in\mathbb{R}^{3k}$, all expressed in the object frame; each column block $G_i$ turns $f_i$ into its wrench, so
$$\mathcal{F}_{\text{obj}}=G\,f_c=\sum_{i=1}^{k}\begin{pmatrix}r_i\times f_i\\ f_i\end{pmatrix}$$
  and $G$ is a $6\times3k$ matrix. It is linear in the forces, which is why closure questions become questions about cones and spans.
- **Force closure**: for every external wrench $\mathcal{F}_{\text{ext}}$ there are admissible contact forces that cancel it, where admissible means each $f_i$ lies in its friction cone $FC_i$ (§2).
$$\forall\,\mathcal{F}_{\text{ext}}\in\mathbb{R}^6\ \ \exists\, f_i\in FC_i:\quad G\,f_c=-\mathcal{F}_{\text{ext}}$$
  Because the cones are closed under positive scaling, this says the image of the cones under $G$ is all of $\mathbb{R}^6$.
- **Form closure** (first order): the same statement with **frictionless** contacts, so each $f_i=\lambda_i n_i$ with $\lambda_i\ge0$ along the inward normal $n_i$; the normal wrenches must positively span $\mathbb{R}^6$ (every wrench is a nonnegative combination of them). That needs at least 4 contacts in the plane and 7 in space, and the counts and their qualifiers are in [[04-robotics/grasping|Grasping §3]].

Now imagine two fingers squeezing a panel. The two opposing forces may have zero net object wrench while maintaining a compressive preload at the contacts — the preload of [[02-foundations/basic-mechanics|0.6.1 §3]], which keeps a one-sided contact engaged until a load undoes it. That preload can make friction available against a later disturbance. Thus a zero net wrench does not mean “no contact forces,” and a large squeeze does not by itself establish force closure. The allowable contact forces must collectively resist disturbances in every required direction, under the stated friction and unilateral-contact constraints. With finite actuator limits, they resist a bounded set rather than literally unbounded external loads.

> [!example] Worked example · 계산 예제
> Fingers at $r_1=(-0.05,0,0)$ m and $r_2=(0.05,0,0)$ m squeeze with $f_1=(10,0,0)$ N and $f_2=(-10,0,0)$ N. The net force is $(0,0,0)$ and both moments are zero ($r_i\parallel f_i$), so $G f_c=0$ although each contact carries 10 N. With $\mu=0.5$ each cone admits up to $0.5\times10=5$ N of tangential force, so the pair can hold a vertical load of up to $2\times5=10$ N at this squeeze.
> **Non-example**: the same squeeze with frictionless fingers ($\mu=0$) resists no vertical load at all, since every admissible force is along $x$; it is not force closure however hard it squeezes.

> [!question] Check what closure promises · closure의 보장 확인
> Does force closure guarantee that the selected grip will hold a heavy panel? **Answer:** no. Closure is a capability under a contact model. The particular load must also fit within friction, actuator and material limits at the selected forces.

### 5. Position, force, impedance, and admittance

A stiff position loop turns every millimetre by which the wall is not where the model says into force — §6 prices it at 100 N per centimetre — so a contact task has to choose what to regulate: the pose, the force, or a relation between the two. Four modes cover the choices.

| Mode | What is regulated |
|---|---|
| Position control | pose or trajectory error |
| Force control | measured contact force |
| Impedance control | desired relationship from motion error to force |
| Admittance control | desired motion response to measured force |

Impedance does not simply “control both position and force.” It shapes interaction behavior, often as a virtual mass–spring–damper — written out, the controller commands a spring and a damper anchored at the reference, the inertia term dropped as most implementations do, so that the force it produces is set by displacement and velocity alone:

$$F = K_d(x_d - x) + D_d(\dot x_d - \dot x)$$

so $K_d$ (stiffness, N/m) and $D_d$ (damping, N·s/m) are the *design* variables — the subscript $d$ for *desired*, as in [[04-robotics/force-compliance-control|13]] and the glossary, which keep $K_e$ for the environment's stiffness — and the force that actually appears depends on how far the environment pushed the tool off $x_d$. Position control is the limit $K_d \to \infty$; force control regulates $F$ directly and lets $x$ go where it must. Admittance is useful when a stiff, accurate position-controlled robot can convert measured force into a compliant motion command. The spring and the damper as physical elements, with the series rule that makes the softest element win, are [[02-foundations/basic-mechanics|0.6.1 §3–§4]]; the same coefficients as a controller's design variables — stiffness, its inverse **compliance**, and damping — with the scale of real environment stiffness, are [[04-robotics/force-compliance-control|13. Force & Compliance Control §1]].

**The four modes as control laws.** Each row of the table is a different choice of what the feedback acts on. Here $x_d$ is the reference pose, $F$ the force the robot applies to the environment (so the force on the robot is $F_{ext}=-F$), $F_d$ the desired force and $F_m$ the measured one.

- **Position control** feeds back pose error only, and contact force is whatever results: $u=K_p(x_d-x)+K_v(\dot x_d-\dot x)$ with high gains $K_p,K_v$ (the PD law of [[04-robotics/control-theory-ce397|Control Theory §7]]).
- **Force control** feeds back force error, commonly with a proportional-integral law, and position is whatever results: $F=F_d+K_f(F_d-F_m)+K_i\int(F_d-F_m)\,dt$.
- **Impedance control** renders the spring-damper above, a map from motion error to force; its full target dynamics with the inertia term are in [[04-robotics/force-compliance-control|13. Force & Compliance Control §2]].
- **Admittance control** is the inverse map, from measured force to motion: it integrates the virtual dynamics to get a motion reference $x_c$ and hands $x_c$ to an inner position loop.
$$M_d\ddot x_c+D_d\,(\dot x_c-\dot x_d)+K_d\,(x_c-x_d)=F_{ext}$$
  Because the measured force drives the reference, the robot yields where it is pushed, with $M_d$ the virtual mass it integrates.

> [!example] Worked example · 계산 예제
> Impedance with $K_d=200$ N/m and $D_d=20$ N·s/m, tool held 1 cm short of its reference ($x_d-x=0.01$ m) and at rest: $F=200\times0.01=2$ N. If the tool is instead being pushed back at $0.05$ m/s ($\dot x_d-\dot x=0.05$), the damper adds $20\times0.05=1$ N, so $F=3$ N. **Non-example**: a stiff PD position loop is formally an impedance with $K_d=K_p$, but calling it "compliant" is wrong at $K_p=10^5$ N/m, where the same 1 cm asks for 1000 N. The law's structure does not decide compliance; the numbers do.

### 6. Scenario: cleaning a wall

A pure position controller commands the tool 2 cm beyond an estimated wall. A 1 cm wall-location error can cause very different force because contact stiffness is high. **With numbers**: a *compliantly mounted* tool meeting the wall at $K_e = 10^4$ N/m — the environment's stiffness, subscript $e$ as in 13 — turns a 1 cm position error into $10^4 \times 0.01 = 100$ N, enough to gouge the surface or trip a force limit, while a 3 cm error would demand 300 N the arm may not even be able to produce. That stiffness is deliberately a soft one; a bare tool on a real arm against steel is up to about one order stiffer — about $10^5$ N/m as the series stiffness of tool, sensor, arm and part — where the same 1 cm error asks for about $10^3$ N and the force diverges long before the error closes. Only a bare indenter on a rigid fixture approaches the $10^7$ N/m material stiffness; the scale is tabulated in [[04-robotics/force-compliance-control|13. Force & Compliance Control §1]]. The running object's panel, at $k_w=400$ N/m — its $K_e$ in this notation — lies below the whole scale, which is why its 5 mm press costs only 2 N.

Now the other three modes of §5 against the same 1 cm error. **Impedance**: set the controller's stiffness to $K_d = 200$ N/m instead and the error asks for about 2 N — $1.96$ N exactly, since the virtual spring and the wall act in series, $1/(1/200+1/10^4)=196$ N/m. That ratio, not any control theory, is why contact tasks are run compliantly. **Admittance** reaches the same force from the other side: the stiff position loop stays, a wrist sensor measures the wall's push, and the admittance law backs the reference off until $K_d(x_d-x_c)$ balances it, so with the same $K_d=200$ N/m it settles at the same $1.96$ N with the tool $0.2$ mm into the wall. It can only yield as fast as the force is measured and the inner position loop follows, so the first milliseconds of a touchdown still meet the stiff arm; [[04-robotics/force-compliance-control|13. §5]] counts how few 1 kHz samples fall inside one. **Force control** regulates the normal force directly — 2 N wherever the wall turns out to be — but still needs tangential motion and stability handling. The best architecture depends on actuator bandwidth, sensing, surface variation, and safety limits.

### 7. Force, tactile, and material state

The Worked case ended on $\mu$, which nobody observed, and on a contact whose mode — free, sticking or sliding — decides which of §1's equations hold. This section is about what sensing can tell you about that state, and it ends in the one estimate every contact controller consumes.

- Wrist force/torque sensing measures net wrench but not the full pressure distribution.
- Tactile arrays can estimate contact location, pressure, shear, and slip cues — including *incipient slip*, the edge of a contact patch sliding while its centre still sticks and before the object moves ([[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing §3]]).
- **Proprioception** measures the robot's own state (joint encoders for angles and velocities, motor currents for torque, an inertial measurement unit (IMU) for body orientation and acceleration); **exteroception** measures the world outside it (cameras, lidar, depth sensors). A wrist F/T sensor and a tactile skin sit between the two: they are on the robot, but what they report is the external contact.
- Vision can observe global geometry while tactile sensing resolves local contact ambiguity — the argument of [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing §1]], which puts a number on it: at a tangential load of half the friction bound, $37\%$ of a fingertip's contact patch is already sliding while the object has moved $0$ mm, so no camera can see it.

What all of these feed is one estimate, worth naming because papers use it without defining it.

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

The running object's own contact, traced through all three modes, shows why the definition needs a window of samples and not one.

<svg viewBox="0 0 560 350" style="max-width:100%;height:auto" role="img" aria-label="Traces of the running object against time: the normal force steps to 0.08 N at first touch at 0.10 s, rises to 2.08 N while closing, and rests at 2.00 N from 0.35 s; the tangential force follows a demand ramp up to the 1.00 N bound at 1.0 s, sticks there until 1.3 s, and stays pinned at 1.00 N while the demand rises to 2 N and the tool slides; the sliding speed is zero until 1.3 s; the mode strip reads free, touching and sticking, touching and sliding; two windows w show sticking and sliding with the same 1 N force; underneath, a command-based contact flag for a panel 2 mm further away turns on 0.1 s before any measured force">
  <defs><marker id="cstA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor">
    <text x="12" y="18" font-size="12" font-weight="600" fill-opacity="0.85">one contact, three modes: the running object's traces</text>
    <rect x="118.2" y="30.0" width="266.4" height="202.0" fill="currentColor" fill-opacity="0.05"/>
    <rect x="384.6" y="30.0" width="155.4" height="202.0" fill="currentColor" fill-opacity="0.13"/>
    <line x1="118.2" y1="30.0" x2="118.2" y2="254.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" stroke-dasharray="3 3"/>
    <line x1="384.6" y1="30.0" x2="384.6" y2="254.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" stroke-dasharray="3 3"/>
    <line x1="96.0" y1="92.0" x2="540.0" y2="92.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="96.0" y1="92.0" x2="96.0" y2="34.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="92.0" y1="67.0" x2="96.0" y2="67.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="70.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">1</text>
    <line x1="92.0" y1="42.0" x2="96.0" y2="42.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="45.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">2</text>
    <text x="89.0" y="95.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">0</text>
    <text x="12" y="62.0" font-size="11" xml:space="preserve">f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> (N)</tspan></text>
    <line x1="96.0" y1="170.0" x2="540.0" y2="170.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="96.0" y1="170.0" x2="96.0" y2="112.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="92.0" y1="145.0" x2="96.0" y2="145.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="148.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">1</text>
    <line x1="92.0" y1="120.0" x2="96.0" y2="120.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="123.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">2</text>
    <text x="89.0" y="173.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">0</text>
    <text x="12" y="140.0" font-size="11" xml:space="preserve">‖f<tspan dy="3.1" font-size="11">t</tspan><tspan dy="-3.1">‖ (N)</tspan></text>
    <line x1="96.0" y1="226.0" x2="540.0" y2="226.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="96.0" y1="226.0" x2="96.0" y2="186.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="229.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">0</text>
    <text x="12" y="204.0" font-size="11" xml:space="preserve">‖v<tspan dy="3.1" font-size="11">t</tspan><tspan dy="-3.1">‖</tspan></text>
    <text x="12" y="217.0" font-size="10.5" fill-opacity="0.8">(schematic)</text>
    <path d="M 96.0 92.0 L 118.2 92.0 L 118.2 90.0 L 173.7 40.0 L 173.7 42.0 L 540.0 42.0" fill="none" stroke="currentColor" stroke-width="2"/>
    <text x="124.2" y="105.0" font-size="10.5" fill-opacity="0.85">0.08 N damper step at first touch</text>
    <text x="181.7" y="37.0" font-size="10.5" fill-opacity="0.85">2.08 N closing, 2.00 N at rest</text>
    <line x1="173.7" y1="145.0" x2="540.0" y2="145.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" stroke-dasharray="1.5 2.5"/>
    <text x="211.4" y="141.0" font-size="10.5" fill-opacity="0.85" xml:space="preserve">μf<tspan dy="3.1" font-size="10.5">n</tspan><tspan dy="-3.1"> = 1.00 N</tspan></text>
    <path d="M 207.0 170.0 L 318.0 145.0 L 384.6 145.0 L 495.6 120.0 L 540.0 120.0" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="5 3"/>
    <text x="491.6" y="115.0" font-size="10.5" text-anchor="end" fill-opacity="0.85">demand</text>
    <path d="M 96.0 170.0 L 207.0 170.0 L 318.0 145.0 L 540.0 145.0" fill="none" stroke="currentColor" stroke-width="2"/>
    <text x="457.9" y="159.0" font-size="10.5" fill-opacity="0.85">pinned at 1.00 N</text>
    <path d="M 96.0 226.0 L 384.6 226.0 L 385.7 222.9 L 386.8 220.2 L 387.9 217.8 L 389.0 215.7 L 390.1 213.8 L 391.3 212.2 L 392.4 210.7 L 393.5 209.5 L 394.6 208.3 L 395.7 207.3 L 396.8 206.4 L 397.9 205.7 L 399.0 205.0 L 400.1 204.4 L 401.2 203.8 L 402.4 203.4 L 403.5 202.9 L 404.6 202.6 L 405.7 202.3 L 406.8 202.0 L 407.9 201.7 L 409.0 201.5 L 410.1 201.3 L 411.2 201.1 L 412.4 201.0 L 413.5 200.8 L 414.6 200.7 L 415.7 200.6 L 416.8 200.5 L 417.9 200.4 L 419.0 200.4 L 420.1 200.3 L 421.2 200.2 L 422.3 200.2 L 423.5 200.2 L 424.6 200.1 L 425.7 200.1 L 426.8 200.1 L 427.9 200.0 L 429.0 200.0 L 540.0 200.0" fill="none" stroke="currentColor" stroke-width="2"/>
    <rect x="329.1" y="135.0" width="44.4" height="95.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="2 2"/>
    <text x="369.5" y="221.0" font-size="10.5" text-anchor="end">w</text>
    <rect x="406.8" y="135.0" width="44.4" height="95.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="2 2"/>
    <text x="447.2" y="221.0" font-size="10.5" text-anchor="end">w</text>
    <rect x="96.0" y="236.0" width="22.2" height="16" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <rect x="118.2" y="236.0" width="266.4" height="16" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <rect x="384.6" y="236.0" width="155.4" height="16" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="92.0" y="248.0" font-size="10.5" text-anchor="end">free</text>
    <text x="251.4" y="248.0" font-size="10.5" text-anchor="middle">touching, sticking</text>
    <text x="462.3" y="248.0" font-size="10.5" text-anchor="middle">touching, sliding</text>
    <line x1="96.0" y1="256.0" x2="96.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="96.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">0</text>
    <line x1="207.0" y1="256.0" x2="207.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="207.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">0.5</text>
    <line x1="318.0" y1="256.0" x2="318.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="318.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">1</text>
    <line x1="429.0" y1="256.0" x2="429.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="429.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">1.5</text>
    <line x1="540.0" y1="256.0" x2="540.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="540.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">2</text>
    <text x="540.0" y="284.0" font-size="10.5" text-anchor="end" fill-opacity="0.85">time (s)</text>
    <text x="12" y="292.0" font-size="10.5" fill-opacity="0.85">if the panel were 2 mm further than believed:</text>
    <rect x="118.2" y="300.0" width="177.6" height="9" fill="currentColor" fill-opacity="0.35"/>
    <rect x="140.4" y="316.0" width="155.4" height="9" fill="currentColor" fill-opacity="0.8"/>
    <text x="306.9" y="308.5" font-size="10.5">command says “in contact”</text>
    <text x="306.9" y="324.5" font-size="10.5" xml:space="preserve">measured f<tspan dy="3.1" font-size="10.5">n</tspan><tspan dy="-3.1"> &gt; 0</tspan></text>
    <line x1="118.2" y1="332.0" x2="140.4" y2="332.0" stroke="currentColor" stroke-width="1"/>
    <path d="M 118.2 328.0 L 118.2 336.0 M 140.4 328.0 L 140.4 336.0" fill="none" stroke="currentColor" stroke-width="1"/>
    <text x="146.8" y="336.0" font-size="10.5" fill-opacity="0.85">0.1 s of false contact</text>
  </g>
</svg>

The running object pressed and wiped: the tool touches at $0.10$ s, where the damper alone makes a $0.08$ N step, the normal force rises to $2.08$ N while closing and rests at $2.00$ N from $0.35$ s; the tangential force follows the wipe demand up to the $\mu f_n=1.00$ N bound at $1.0$ s, sticks there until $1.3$ s, and stays pinned at $1.00$ N while the demand climbs to 2 N and the tool slides, its sliding speed $\lVert v_t\rVert$, drawn only in shape, rising from zero. In the two windows $w$ the force is the same 1 N, and only the motion, or the demand pulling away from a force that has stopped rising, separates sticking from sliding. Underneath, the non-example's command-based flag for a panel 2 mm further than believed: it says "in contact" from $0.10$ s, $0.1$ s before any force is measured.

Rope, cloth, soil, wet concrete, cables, and bulk material have high-dimensional, changing state. Their behavior depends on history and unobserved material properties, making representation and prediction difficult.

### 8. Learning and sim-to-real

The randomization table in a paper's appendix is the scope of its robustness claim, and this section is about reading it: what learning can estimate about a contact, and what a randomization range does and does not buy.

Learning may estimate residual dynamics, contact state, friction/material properties, grasp scores, or a tactile-conditioned policy. Domain randomization ([[05-construction-robotics/sim-to-real|construction 7.5 Sim-to-Real §2]] defines it, with its objective; [[04-robotics/legged-locomotion|18. Legged Locomotion §2]] shows it at work) can broaden training conditions, but the chosen randomization distribution defines what variation was covered. Privileged simulator state ([[05-construction-robotics/sim-to-real|construction 7.5 §2]]) can aid training while being unavailable at deployment; check how the policy replaces it at test time. One pushing task shows all three: a residual-dynamics network learns the difference between the simulator's predicted next state and the real one; domain randomization resamples μ and object mass every episode; and the policy trains with the simulator's exact object pose but must deploy with a pose estimated from the camera.

**Worked on the running object: what a randomization range buys.** Randomize $\mu$ uniformly over $[0.25,0.75]$ around the table's $0.5$. At the Worked case's $f_n=2.00$ N the friction bound $\mu f_n$ then runs from $0.50$ to $1.50$ N, so the 1 N wipe sticks in exactly the half of the episodes with $\mu\ge0.5$ and slides in the other half. A policy that must succeed in every episode learns to press harder: holding 1 N at $\mu=0.25$ takes $f_n\ge1/0.25=4.00$ N, which is $\delta=4.00/400=10$ mm past the face instead of 5. The robustness was bought as a firmer press, and only inside the range: a wet panel at $\mu=0.15$ carries $0.15\times4.00=0.60$ N at that press, and the wipe slides. The contact model hides the same trap. A policy that learned to command 5 mm past the face in a simulator whose penalty stiffness is $400$ N/m (§3) learned a 2 N press only in that simulator; on a panel ten times stiffer the same 5 mm asks for $4000\times0.005=20$ N.

**The reading this gives you.** Check whether the deployment's $\mu$, mass and contact stiffness lie inside those ranges, and whether the policy outputs a force or a position offset, because a position offset becomes a force only through a stiffness the simulator chose. How widely real contact stiffness ranges is tabulated in [[04-robotics/force-compliance-control|13. Force & Compliance Control §1]].

### 9. Evaluation and paper language

A higher task success rate does not say whether the gain came from tactile sensing, better control, safer force limits or easier contact conditions, so a contact paper has to report enough to trace it: matched baselines and ablations across sensing, controller, material and initialization, and force metrics defined well enough to compare.

Measure task success, peak/mean force, force-tracking error, slip/drop rate, object or surface damage, recovery, safety violations, and robustness across materials and friction. “Contact-rich,” “compliant,” and “robust” require explicit task and perturbation definitions.

**The four force metrics, defined.** Each is a different kind of number, and each fails in its own way.

- **Peak contact force** $F_{\max}=\max_t\lVert f(t)\rVert$ over the contact episode, in newtons. It is a *sampled* maximum, so it is only as true as the sensor's rate: a 1 kHz channel watching a 1.4 ms impact gets about one sample inside the event ([[04-robotics/force-compliance-control|13. Force & Compliance Control §5]]), and the reported peak can sit far below the real one. **Mean force** over the same interval is the companion number, and reporting only the mean hides exactly what the peak was for.
- **Force-tracking error**, the root-mean-square difference between the commanded and the measured normal force over the contact interval $[0,T]$, in newtons:

$$e_{\mathrm{RMS}}=\sqrt{\frac{1}{T}\int_0^T\big(f_d(t)-f_m(t)\big)^2\,dt}$$

  where $f_d$ is the commanded force, $f_m$ the measured one and $T$ the duration of contact — not of the trial, which is the substitution that flatters a controller by averaging in the free-space seconds. Example on the running object: a commanded $f_d=2$ N measured as $2.0,\ 2.3,\ 1.8,\ 2.1$ N gives errors $0,\ -0.3,\ 0.2,\ -0.1$ N, so $e_{\mathrm{RMS}}=\sqrt{0.035}=0.187$ N, $9.4\%$ of the target, while the mean absolute error is only $0.150$ N. RMS charges the single 0.3 N excursion more heavily, which is why it is the honest one to quote against a force limit.
- **Slip rate** and **drop rate**: the fraction of contact time in which tangential motion occurs while the controller commanded sticking, and the fraction of grasp trials in which the object leaves the hand before the goal. Both are proportions, so both are meaningless without the trial count beside them — and both are measured against a *commanded* intent, which means they presuppose the contact-state estimate of §7.

**Non-example.** A peak force quoted with no sensor rate, an RMS error quoted over the whole trial, or a slip rate quoted without $n$ are three different ways of reporting a number that cannot be compared with anyone else's.

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
2. A 3 N tangential demand meets a normal force of 4 N at $\mu=0.6$. Does the simple cone allow sticking, and what normal force would the same demand need at $\mu=0.48$?
3. Why may a policy trained with one friction coefficient fail even with perfect perception?
4. What should a tactile-policy ablation hold constant?
5. A planner reports that its grasp has friction margin to spare. It constrained each contact with the outer box pyramid. Which way is its margin wrong, and by how much at the corner?
6. A system logs "in contact" whenever the commanded pose is past the surface. Which of the two defining conditions of contact-state estimation does that fail, and what will it report at the worst possible moment?

> [!tip]- Answers
> 1. Small pose/model errors can generate large forces and instability.
> 2. No: $3>0.6\times4=2.4$ N, so the contact slides. At $\mu=0.48$ it needs $f_n\ge3/0.48=6.25$ N.
> 3. Feasible forces, slip transitions, and dynamics change.
> 4. Demonstrations, architecture capacity, controller, initialization, materials, and evaluation protocol; remove or replace tactile information without making the rest easier.
> 5. Optimistically wrong. The box pyramid contains the true cone, so it authorises tangential forces that slip; at the corner it allows $\sqrt2$ times the real bound, $41.4\%$ too much. The inner polyhedral cone errs the other way and would have understated the margin instead.
> 6. Condition (ii): the estimate must come from measurement, not from the command. It will report contact exactly when a mislocated panel guarantees there is none — the case the estimate existed for.

### Problem set · 과제

Tier B. The running object with **two entries changed**: the commanded penetration becomes $\delta=8\,\mathrm{mm}$, and dust on the panel drops the friction coefficient to $\mu=0.35$. Everything else — **P2** at $\theta=(0^\circ,90^\circ)$, the panel at $x=1\,\mathrm{m}$, $k_w=400\,\mathrm{N/m}$, $m_p=1.0\,\mathrm{kg}$, the $f_g=10\,\mathrm N$ two-finger squeeze at $\pm0.05\,\mathrm{m}$ — is unchanged ([[02-foundations/lab-plants|0.6]]). Using only this page, its prerequisites and the object catalog. No simulator.

1. **Draw.** All three panels of the picture above at the new numbers. On the right-hand panel the three closed curves must now be drawn for $\mu=0.35$ at the new $f_n$, and the 1 N wipe arrow drawn to the same scale — the drawing has to show which of the three sets contains it.
2. **Derive.** (a) $f_n$ at rest at $\delta=8\,\mathrm{mm}$. (b) The cone half-angle and the largest tangential force that can stick. (c) Does the $1\,\mathrm{N}$ wipe still stick, and with what margin? (d) The effective coefficient of the four-generator inner cone, and the largest wipe *it* would authorise. (e) The squeeze $f_g$ the two fingers now need to hold the panel, and what the unchanged 10 N squeeze can carry.
3. **Interpret.** Two failures are available here — the wipe slipping and the panel dropping — and only one of them has happened. Which one, and why did the same $30\%$ loss of $\mu$ move the two bounds in opposite directions? Name the one measurement that would have told you before the panel hit the floor, and say which section of this page defines it.

> [!note]- How to draw it · 그리는 법
> - **Left, the arm in the $x$–$y$ plane, to scale**: P2's base at the origin, link 1 along $+x$ to the elbow at $(1,0)$, link 2 up to the tip at $(1,1)$. The panel's face $x=1$ is drawn set back behind that plane — offset up and to the right, as a slanted rectangle — so it does not lie on the forearm, and an L-shaped tool reaches back from the tip, in front of the face, with its short foot pressing the face along $\hat n$.
> - **The contact frame where the tool meets the face**: $\hat n$ pointing $+x$ into the face, $\hat t_1$ pointing $-y$ down the face along the wipe.
> - **The contact force drawn apart**: the tool's push on the panel, $f$, as one arrow ending on the face, and the panel's push on the tool, $-f$, as a second arrow beside it, pointing the other way.
> - **A small spring between the tool's end and the face**, labelled with $k_w$ and compressed by the commanded $\delta$ — drawn much larger than to scale, with a note saying so, because a few millimetres on a 1 m arm are invisible.
> - **Right, the cone in the contact frame**: $\hat n$ vertical, the tangent plane $(\hat t_1,\hat t_2)$ horizontal, with $\hat t_2$ receding into the page so the frame stays right-handed, and the circular cone opening upward with its half-angle $\arctan\mu$ marked as an angle.
> - **Three closed curves on the tangent plane, concentric, at the $f_n$ the press produces**: the true circle of radius $\mu f_n$; outside it the square of the outer box pyramid, touching the circle at four points; inside it the square of the four-generator inner cone, with its four corners *on* the circle.
> - **One arrow for the commanded wipe, at its actual length on the same scale**, so the drawing shows which of the three sets contains it.
> - **Underneath, the gap axis**: a horizontal line for $\phi$ with zero marked, $f_n=0$ on the ray to the left of zero ($\phi>0$, apart) and $f_n\ge0$ on the vertical ray at $\phi=0$, and two dots — one before touchdown, one at the commanded penetration, which the penalty model of §3 allows and the rigid model of §1 forbids.
> - **The pair $(\phi,f_n)$ must never be off the two rays** — that picture *is* complementarity.

> [!tip]- Solutions
> 1. On the left, the force pair is now $f=(3.20,-1.00)\,\mathrm N$ on the panel and $-f$ on the tool, and holding it costs $\tau=J^\top f=(-4.20,-3.20)\,\mathrm{N{\cdot}m}$; the spring is compressed $8\,\mathrm{mm}$. On the right, the cone is now narrower ($19.3^\circ$ instead of $26.6^\circ$) but the circle on the tangent plane is *larger*, because $f_n$ rose faster than $\mu$ fell. The four-generator square's corners still sit on the circle; the box pyramid's square still circumscribes it. The 1 N wipe now ends inside the $1.12\,\mathrm N$ circle but still outside the inner square, whose flat side is $0.792\,\mathrm N$. Underneath, the penetration point moves to $-8\,\mathrm{mm}$ at $3.20\,\mathrm N$ on the same $0.4\,\mathrm{N/mm}$ penalty line.
> 2. (a) $f_n=400\times0.008=3.20\,\mathrm{N}$ at rest; add $d_c\dot\delta$ only while still closing. (b) $\arctan0.35=19.29^\circ$, and $\lVert f_t\rVert\le0.35\times3.20=1.12\,\mathrm{N}$. (c) Yes: $1.00<1.12$, a margin of $0.12\,\mathrm{N}$, so the wipe uses $89.3\%$ of the bound — it went from exactly on the bound to just inside it, because the deeper press bought more friction than the dust took away. (d) $\mu\cos(\pi/4)=0.35\times0.7071=0.2475$, allowing only $0.2475\times3.20=0.792\,\mathrm{N}$: the conservative model *rejects* the very wipe the real contact carries. (e) $f_g\ge m_pg/(2\mu)=9.81/0.70=14.01\,\mathrm{N}$, while the unchanged 10 N squeeze carries $2\times0.35\times10=7.00\,\mathrm{N}$ — $2.81\,\mathrm{N}$ short of the panel's $9.81\,\mathrm{N}$ weight.
> 3. The panel drops; the wipe is fine. Both bounds are $\mu f_n$ and both lost the same $30\%$ of $\mu$, but the wipe's normal force was raised by the command from $2.00$ to $3.20\,\mathrm{N}$ — a $60\%$ gain that more than paid for the dust, $1.6\times0.7=1.12$ — while the grip's normal force is fixed by the squeeze and got no such compensation, $1.0\times0.7=0.70$. The lesson is that a friction margin is a margin in the *product* $\mu f_n$, and only one of the two contacts had someone pushing harder. The measurement that would have caught it is contact-state estimation (§7): the fingers sliding while the controller commanded sticking is a mode change, visible in the tangential force pinned at its bound, and it happens before the panel leaves the hand. A camera watching the panel's pose sees nothing until it is already falling — the argument of [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing §1]] — and a tactile finger could warn earlier still, from the incipient slip at the edges of its patch ([[04-robotics/tactile-visuotactile|14. §3]]).

### Sources

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation (Tedrake) — force control & contact chapters](https://manipulation.csail.mit.edu/)
- [Modern Robotics course wiki — ch. 12 videos & software](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)

## 한국어

*[[04-robotics/index|로보틱스 인덱스]]의 E군, 곧 물리 상호작용 묶음의 유일한 페이지다. H군, 곧 매니퓰레이션 전문화(12–16) 전체가 여기서 갈라져 나오기 때문이다. [[02-foundations/linear-algebra|선형대수]], 최적화, [[02-foundations/basic-mechanics|0.6.1 기초 역학 §3–§4]]의 스프링과 마찰, 그리고 [[04-robotics/modern-robotics/index|MR 챕터 요약]] 위에 선다. 로봇이 무언가에 닿는 순간 기하만으로는 부족해지는 지점이 여기다.*

로봇이 세계에 닿는 순간 기하만으로는 부족하다. 접촉은 힘, 마찰, 충격, 모드 전환, 변형, 불확실성을 끌고 들어온다. 이 효과들은 파지, 조립, 굴착, 닦기, 천공, 유연 재료 취급의 중심에 있다.

> [!info] 깊이 목표
> 접촉이 많은(contact-rich) 매니퓰레이션 논문에서 접촉 모델, 센싱, 제어 모드, 재료 가정,
> 평가를 짚어내며 읽는다. Complementarity 솔버와 연속체 역학의 세부는 선택적
> 실무/숙달 주제다.

> [!note] 선수 지식
> 장치 **P2**와 **P3**([[02-foundations/lab-plants|0.6 Lab Plants]]. *장치*(plant)는 제어가 다루는 대상 시스템을 부르는 말이다). P2는 카탈로그의 평면 2링크 팔이고, P3는 1축 햅틱 핸들로, 그 $400\,\mathrm{N/m}$ 가상 벽이 이 페이지 패널의 강성이 된다 · [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/optimization|최적화]](이차계획, §5) · 스프링, 예압, Coulomb 마찰([[02-foundations/basic-mechanics|0.6.1 기초 역학 §3–§4]]) · 렌치([[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §6]]) · [[04-robotics/modern-robotics/ch05-velocity-kinematics|정역학과 야코비안]] · [[04-robotics/modern-robotics/ch08-dynamics|동역학]]

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 접촉·힘·촉각 피드백 층을 연다. 기하만으로는 부족해지는 지점이다. "*저 패널을 프레임에 설치해*"에서는 *접촉을 감지하는* 단계(접촉이 있기는 한가, §1, 그리고 어느 모드인가, §7)와 *끼움을 수행하는* 단계(접촉이 얼마나 되는 힘을 견디는가, §2와 §4, 그리고 제어기가 무엇을 조절해야 하는가, §5–§6)를 받친다. 이 페이지의 칩은 [[physical-ai-map|피지컬 AI 지도]]의 접촉·힘 띠에 있다. 이것이 없으면 마찰이 이미 아는 상수처럼 보인다. '대상으로 한 번 끝까지'의 $2\,\mathrm N$ 누름에서 $1\,\mathrm N$ 닦기는 $\mu f_n$ 경계 위에 정확히 놓이고, $1\,\mathrm{kg}$ 패널을 쥔 두 손가락 파지는 $1.9\,\%$ 차이로 버틴다. 그러니 먼지가 $\mu$를 $0.5$에서 $0.40$으로 떨어뜨리면, 카메라 속에서는 1픽셀도 움직이지 않던 패널이 떨어진다. [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]는 §1의 강성 눈금을 이 페이지 §6의 벽 위에, §2의 어드미턴스를 §5 위에, §5의 접촉 천이를 §2와 §7 위에 세우고, [[04-robotics/grasping|15. 파지 §2]]는 마찰 원뿔과 그 선형화 손실을 §2 위에, [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱 §1과 §3]]은 접촉 상태를 §1–§2 위에, [[04-robotics/capstone-panel-contact|26. 캡스톤 §4]]는 접촉 전환을 §7 위에 세운다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 2, 로보틱스 82–85회차이고, 13과 15가 블록 3에서 뒤따른다. 이 페이지를 마치면 접촉이 있는지와 그것이 얼마를 견디는지 말하고, 선형화한 마찰 원뿔이 어느 쪽으로 틀리는지 말하고, 위치·힘·임피던스·어드미턴스 제어를 각각 무엇을 명령하고 무엇을 재는지로 가르고, 접촉이 많은 논문에 그 $\mu$와 접촉 강성과 접촉 상태 추정을 물을 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 네 번쯤, 로보틱스 82–85회차다. **첫 회차:** 이 페이지의 대상, 그림, '대상으로 한 번 끝까지'를 손으로 한다. 1–3단계와 5–6단계이고, 4단계는 §2를 가리키기만 하므로 셋째 회차로 미룬다. 끝으로 답을 가리고 6단계를 $\mu=0.45$에서 다시 한다($9.0\,\mathrm N<9.81\,\mathrm N$: 패널이 떨어진다). **둘째 회차:** §1(선형 상보성 문제, 곧 LCP를 다루는 메모는 두 번째 읽기), 네 제어 모드가 벽 하나에서 만나는 §5와 §6, 그리고 같은 $\mu$가 무작위화 범위가 되는 §8. **셋째 회차:** §2–§4, 곧 마찰 원뿔과 그 두 선형화, 페널티 모델, 렌치와 closure. **넷째 회차:** §7과 §9 — §7은 [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱 §1]]에 기대므로 §7에 이르면 그 절을 읽는다 — 그리고 스스로 점검과 과제. 접힌 *더 깊이* 메모는 두 번째 읽기다.

> [!tip] 접촉을 감지하는 것에서 표현하는 것으로
> 이 페이지는 로봇 쪽의 접촉을 다룬다. 그 접촉 cue를 사람에게 표현해야 할 때는 [[04-robotics/haptics-teleoperation/tactile-display-design|Tactile Display Design]]으로, 가상 벽이나 힘 반영 루프가 안정해야 할 때는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|Rendering, Sampling & Stability]]로 이어 읽는다.

### 계속 쓰는 대상: P3 강성 패널을 미는 P2 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2** — 평면 2R 팔, $L_1=L_2=1\,\mathrm{m}$ — 를 고정 자세 $\theta=(0^\circ,90^\circ)$에 두면 말단이 $(1,1)\,\mathrm{m}$에 있고, 거기 달린 도구가 평평한 패널을 민다. 패널 면은 평면 $x=1\,\mathrm{m}$이고, 전완은 그림 평면 바깥에서 패널 옆을 지나가므로 패널에 닿는 것은 도구뿐이다. 그림 평면 안이었다면 링크 2가 면을 따라 전체 길이로 붙어 버리고([[04-robotics/modern-robotics/ch02-configuration-space|MR 2장]]), 아래의 5 mm 누름이 전완을 패널 속으로 밀어 넣었을 것이다. 도구는 L자 모양이다. 말단에서 면 앞쪽으로 비켜 그림 평면 뒤로 뻗고, 짧은 발만 $\hat n$ 방향으로 면에 닿는다. 말단에서 곧게 뻗은 막대였다면 면의 평면 안에 놓여 길이 전체로 면에 닿았을 것이다. 그림 평면 뒤로 뻗으면서 생기는 모멘트는 그림 평면 안에 놓인 축에 대한 것뿐이고 그것은 관절 베어링이 받으므로, 관절 토크는 같은 힘을 말단 $(1,1)$에 건 것과 같다. 패널의 강성은 **P3**의 벽 값을 쓴다. 카탈로그의 로보틱스 관통 과제 — *도구를 패널까지 옮겨 힘을 조절하며 접촉한다* — 를 패널을 세워 놓고 하는 판본이고, 여기서 묻는 것은 마찰이다. 같은 팔과 도구로 패널을 말단 아래에 눕혀 놓고 운동과 힘의 관계를 묻는 쪽은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $\hat n$ | $+x$ | 접촉 법선, 패널 **안쪽**을 양으로 센다 |
| $\hat t_1,\ \hat t_2$ | $-y$, $-z$ | 패널 면 안의 두 접선 방향. $\hat n\times\hat t_1=\hat t_2$가 되도록 부호를 잡은 오른손 좌표계 |
| $k_w$ | $400\,\mathrm{N/m}$ | 패널 강성 — P3의 가상 벽 값 |
| $d_c$ | $4\,\mathrm{N\cdot s/m}$ | §3 페널티 모델의 접촉 감쇠 — 이 페이지가 P3에 더하는 유일한 값 |
| $\mu$ | $0.5$ | 도구–패널 마찰 계수 |
| $\delta$ | $5\,\mathrm{mm}$ | 면보다 안쪽으로 명령한 침투량 |
| $\dot\delta$ | $0.02\,\mathrm{m/s}$ | 처음 닿는 순간부터 도구가 $\delta=5\,\mathrm{mm}$에서 멈출 때까지 유지하는 접근 속도 |
| $m_p$ | $1.0\,\mathrm{kg}$ | 패널 자체의 질량, 들어 올릴 때 쓴다(§4) |
| $f_g$ | $10\,\mathrm{N}$ | 들어 올린 패널을 $\pm0.05\,\mathrm{m}$의 두 손가락이 쥘 때 손가락마다의 조임(§4) |
| $r_b$ | $0.40\,\mathrm{m}$ | 패널의 장착 브래킷, 곧 패널 렌치의 원점이 접촉 아래로 떨어진 거리(§4) |
| $g$ | $9.81\,\mathrm{m/s^2}$ | 중력, $-y$ 방향 |

**힘이 어느 물체에 걸리는가.** 이 페이지 전체에서 $f$는 도구가 패널에 가하는 힘이고, $\hat n$ 방향의 법선 성분 $f_n$과 면 안의 접선 성분 $f_t$로 나눈다. 패널은 도구를 $-f$로 되민다. [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장]]이 누르기에 쓰는 규약이고, $\hat n$을 패널 안쪽으로 양으로 세는 이유이기도 하다. P3의 $+x$도 벽 안쪽이다.

**이 패널이 얼마나 무른가.** $k_w=400\,\mathrm{N/m}$은 P3가 렌더링하는 벽이고, [[04-robotics/force-compliance-control|13. §1]]의 강성 눈금에서 폼 줄보다도 무르다. 그러니 유연하게 장착한 패널로 읽어라. 실제 도구와 팔을 거쳐 만나는 구조물 패널은 $10^4$–$10^5\,\mathrm{N/m}$이고(13 §1), 거기서는 같은 5 mm 누름이 50–500 N을 요구한다(그 차이는 §6이 따진다).

P2가 평면인데도 접선을 하나가 아니라 둘 두는 것은, *팔*은 평면에서 움직여도 *접촉*은 3차원이기 때문이다. 두 번째 접선이 무엇을 치르게 하는지는 §2가 말한다.

*범위: 이 페이지는 접촉 하나의 역학을 가르친다 — 언제 접촉이 존재하는가, 그 접촉이 얼마나 되는 힘을 견디는가, 그 힘이 어떻게 물체 렌치가 되는가, closure가 무엇을 보장하고 무엇을 보장하지 않는가 — 그리고 접촉이 많은 논문의 센싱과 평가를 읽는 법을 가르친다. 그 접촉에 어떤 제어기를 고를지([[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]), 파지를 어떻게 계획하고 채점할지([[04-robotics/grasping|파지]]), 촉각 신호를 사람에게 어떻게 되돌려 줄지([[04-robotics/haptics-teleoperation/tactile-display-design|24.2 촉각 디스플레이 설계]]), 접촉 시뮬레이터의 솔버를 어떻게 만드는지([[06-research-practice/simulators-benchmarks-datasets|연구 실무 7. 시뮬레이터·벤치마크·데이터셋]])는 가르치지 않는다.*

### 그림으로 먼저 보기: 패널 위의 접촉 프레임과 그 위에 선 원뿔 · The picture

<svg viewBox="0 0 560 466" style="max-width:100%;height:auto" role="img" aria-label="왼쪽: x–y 평면의 θ = (0, 90도) P2, 그 평면 뒤로 물러선 패널 면 x = 1 m, 말단에서 뒤로 뻗어 발로 면을 누르는 L자 도구, 접촉 프레임, 확대한 400 N/m 접촉 스프링, 그리고 떼어 그린 접촉력: 도구가 패널을 (2, -1) N으로 밀고 패널이 도구를 (-2, 1) N으로 되민다; 오른쪽: 반각 26.6도의 마찰 원뿔과, 법선력 2.00 N에서의 1.00 N 원, 모서리 1.414 N의 외접 상자, 평평한 변 0.707 N의 내접 4-생성자 정사각형, 패널에 걸리는 1 N 닦기; 아래: complementarity의 두 반직선과 +2 mm, -5 mm 두 점이 있는 간극 축">
  <defs><marker id="cftkA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="cftkB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor">
    <text x="12" y="22" font-size="12" fill-opacity="0.85" font-weight="600">팔 (x–y 평면, 실제 비율)과 뒤로 물러선 패널</text>
    <line x1="18.2" y1="259" x2="61.8" y2="259" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <path d="M 20.8 259 L 15.8 265 M 26.3 259 L 21.3 265 M 31.8 259 L 26.8 265 M 37.3 259 L 32.3 265 M 42.8 259 L 37.8 265 M 48.3 259 L 43.3 265 M 53.8 259 L 48.8 265" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
    <path d="M 40 250 L 33 259 L 47 259 Z" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
    <path d="M 181.6 157.1 L 181.6 64.9 L 197.4 49.1 L 197.4 141.2 Z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.75"/>
    <path d="M 197.4 59.1 L 203.4 54.1 M 197.4 69.3 L 203.4 64.3 M 197.4 79.5 L 203.4 74.5 M 197.4 89.7 L 203.4 84.7 M 197.4 99.9 L 203.4 94.9 M 197.4 110.1 L 203.4 105.1 M 197.4 120.3 L 203.4 115.3 M 197.4 130.5 L 203.4 125.5 M 197.4 140.7 L 203.4 135.7" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <line x1="40" y1="250" x2="168" y2="250" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="168" y1="250" x2="168" y2="122" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <polyline points="168,122 179.3,100.5 186.9,100.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="40" cy="250" r="4.5" fill="currentColor"/>
    <circle cx="168" cy="250" r="4" fill="currentColor"/>
    <circle cx="168" cy="122" r="4.5" fill="currentColor"/>
    <circle cx="189.5" cy="100.5" r="2.6" fill="currentColor"/>
    <line x1="193.5" y1="100.5" x2="229.5" y2="100.5" stroke="currentColor" stroke-width="1.6" marker-end="url(#cftkA)"/>
    <line x1="189.5" y1="104.5" x2="189.5" y2="138.5" stroke="currentColor" stroke-width="1.6" marker-end="url(#cftkA)"/>
    <text x="203.5" y="93.5" font-size="11">n&#770; 패널 안쪽</text>
    <text x="202.4" y="138.5" font-size="11" xml:space="preserve">t&#770;<tspan dy="3.1" font-size="11">1</tspan><tspan dy="-3.1"> 닦기 (−y)</tspan></text>
    <text x="202.4" y="57.1" font-size="11">면 x = 1 m</text>
    <text x="12" y="281" font-size="11">베이스 (0, 0)</text>
    <text x="168" y="281" font-size="11" text-anchor="middle">엘보 (1, 0)</text>
    <text x="160" y="118" font-size="11" text-anchor="end">말단 (1, 1)</text>
    <text x="179.5" y="92.5" font-size="11" text-anchor="end">도구</text>
    <text x="104" y="242" font-size="11" text-anchor="middle" fill-opacity="0.85">P2, θ = (0°, 90°)</text>
    <rect x="46" y="150" width="104" height="62" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <line x1="128" y1="170" x2="128" y2="206" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 128 172.0 L 136 178.0 M 128 178.5 L 136 184.5 M 128 185.0 L 136 191.0 M 128 191.5 L 136 197.5 M 128 198.0 L 136 204.0 M 128 204.5 L 136 210.5" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <line x1="52" y1="186" x2="88" y2="186" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
    <line x1="88" y1="179" x2="88" y2="193" stroke="currentColor" stroke-width="1.6"/>
    <path d="M 88 186 L 91 186 L 92.7 191 L 96.1 181 L 99.5 191 L 102.9 181 L 106.3 191 L 109.7 181 L 113.1 191 L 116.5 181 L 119.9 191 L 123.3 181 L 125 186 L 128 186" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
    <line x1="78" y1="177" x2="78" y2="198" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
    <line x1="78" y1="198" x2="88" y2="198" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <line x1="88" y1="194" x2="88" y2="201" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <text x="52" y="165" font-size="11" xml:space="preserve">k<tspan dy="3.1" font-size="11">w</tspan><tspan dy="-3.1"> = 400 N/m</tspan></text>
    <text x="54" y="209" font-size="11">δ = 5 mm</text>
    <text x="46" y="226" font-size="10.5" fill-opacity="0.8">확대, 비율 아님</text>
    <line x1="150" y1="150" x2="185.5" y2="103.5" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="3 2"/>
    <line x1="244" y1="155.5" x2="244" y2="217.5" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 244 159.5 L 250.0 154.5 M 244 167.5 L 250.0 162.5 M 244 175.5 L 250.0 170.5 M 244 183.5 L 250.0 178.5 M 244 191.5 L 250.0 186.5 M 244 199.5 L 250.0 194.5 M 244 207.5 L 250.0 202.5 M 244 215.5 L 250.0 210.5" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <circle cx="212.0" cy="180.0" r="3.5" fill="currentColor"/>
    <path d="M 219.1 174.8 L 239.3 184.9 L 241.2 181.2 L 245.9 189.7 L 236.3 191.0 L 238.2 187.3 L 217.9 177.1 Z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
    <line x1="240.1" y1="201.3" x2="212.7" y2="187.6" stroke="currentColor" stroke-width="1.3" marker-end="url(#cftkA)"/>
    <text x="234.2" y="175.8" font-size="11">f</text>
    <text x="220.6" y="207.6" font-size="11">−f</text>
    <text x="205.0" y="184.0" font-size="10.5" text-anchor="end">도구</text>
    <text x="204" y="230.0" font-size="10.5">f = (2, −1) N: 도구가 패널에</text>
    <text x="204" y="243.0" font-size="10.5">−f: 패널이 도구에</text>
    <text x="204" y="256.0" font-size="10.5">τ = Jᵀf = (−3, −2) N·m</text>
    <text x="12" y="300" font-size="10.5" fill-opacity="0.85">패널은 그림 평면 뒤에 있다: 전완은 그 옆을 지나고 도구의 발만 닿는다</text>
    <text x="280" y="22" font-size="12" fill-opacity="0.85" font-weight="600">접촉 프레임 안의 원뿔</text>
    <line x1="368" y1="226" x2="368" y2="60.8" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" marker-end="url(#cftkA)"/>
    <line x1="368" y1="226" x2="449.2" y2="226" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" marker-end="url(#cftkA)"/>
    <line x1="368" y1="226" x2="392.9" y2="201.1" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" marker-end="url(#cftkA)"/>
    <text x="375" y="68.8" font-size="12">n&#770;</text>
    <text x="455.2" y="230" font-size="12" xml:space="preserve">t&#770;<tspan dy="3.4" font-size="11">1</tspan></text>
    <text x="398.9" y="213.1" font-size="12" xml:space="preserve">t&#770;<tspan dy="3.4" font-size="11">2</tspan></text>
    <path d="M 368 226 L 428.9 107.5 L 307 131.4 Z" fill="currentColor" fill-opacity="0.06"/>
    <line x1="368" y1="226" x2="307" y2="131.4" stroke="currentColor" stroke-width="1.4"/>
    <line x1="368" y1="226" x2="428.9" y2="107.5" stroke="currentColor" stroke-width="1.4"/>
    <line x1="368" y1="226" x2="388" y2="133.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <line x1="368" y1="226" x2="308.8" y2="133.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <line x1="368" y1="226" x2="348" y2="94.4" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <line x1="368" y1="226" x2="427.2" y2="94.4" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3"/>
    <path d="M 424 114 L 423.3 114.7 L 422.5 115.5 L 421.7 116.2 L 420.8 116.9 L 419.9 117.6 L 419 118.3 L 418 119.1 L 417 119.8 L 416 120.5 L 414.9 121.2 L 413.8 121.9 L 412.7 122.6 L 411.5 123.3 L 410.3 123.9 L 409.1 124.6 L 407.9 125.3 L 406.6 125.9 L 405.3 126.6 L 404 127.2 L 402.6 127.9 L 401.3 128.5 L 399.9 129.1 L 398.5 129.7 L 397 130.3 L 395.6 130.9 L 394.1 131.4 L 392.6 132 L 391.1 132.5 L 389.5 133.1 L 388 133.6 L 386.4 134.1 L 384.9 134.6 L 383.3 135.1 L 381.7 135.5 L 380.1 136 L 378.5 136.4 L 376.9 136.8 L 375.3 137.2 L 373.6 137.6 L 372 138 L 370.4 138.4 L 368.7 138.7 L 367.1 139 L 365.5 139.3 L 363.8 139.6 L 362.2 139.9 L 360.6 140.1 L 358.9 140.4 L 357.3 140.6 L 355.7 140.8 L 354.1 141 L 352.5 141.1 L 351 141.3 L 349.4 141.4 L 347.8 141.5 L 346.3 141.6 L 344.8 141.6 L 343.3 141.7 L 341.8 141.7 L 340.3 141.7 L 338.8 141.7 L 337.4 141.7 L 336 141.6 L 334.6 141.6 L 333.2 141.5 L 331.9 141.4 L 330.5 141.3 L 329.2 141.1 L 328 141 L 326.7 140.8 L 325.5 140.6 L 324.3 140.4 L 323.2 140.1 L 322.1 139.9 L 321 139.6 L 319.9 139.3 L 318.9 139 L 317.9 138.7 L 316.9 138.4 L 316 138 L 315.1 137.6 L 314.3 137.2 L 313.4 136.8 L 312.7 136.4 L 311.9 136 L 311.2 135.5 L 310.6 135.1 L 309.9 134.6 L 309.3 134.1 L 308.8 133.6 L 308.3 133.1 L 307.8 132.5 L 307.4 132 L 307 131.4 L 306.7 130.9 L 306.4 130.3 L 306.1 129.7 L 305.9 129.1 L 305.8 128.5 L 305.6 127.9 L 305.6 127.2 L 305.5 126.6 L 305.5 125.9 L 305.6 125.3 L 305.7 124.6 L 305.8 123.9 L 306 123.3 L 306.2 122.6 L 306.4 121.9 L 306.7 121.2 L 307.1 120.5 L 307.5 119.8 L 307.9 119.1 L 308.4 118.3 L 308.9 117.6 L 309.4 116.9 L 310 116.2 L 310.6 115.5 L 311.3 114.7 L 312 114 L 312.7 113.3 L 313.5 112.5 L 314.3 111.8 L 315.2 111.1 L 316.1 110.4 L 317 109.7 L 318 108.9 L 319 108.2 L 320 107.5 L 321.1 106.8 L 322.2 106.1 L 323.3 105.4 L 324.5 104.7 L 325.7 104.1 L 326.9 103.4 L 328.1 102.7 L 329.4 102.1 L 330.7 101.4 L 332 100.8 L 333.4 100.1 L 334.7 99.5 L 336.1 98.9 L 337.5 98.3 L 339 97.7 L 340.4 97.1 L 341.9 96.6 L 343.4 96 L 344.9 95.5 L 346.5 94.9 L 348 94.4 L 349.6 93.9 L 351.1 93.4 L 352.7 92.9 L 354.3 92.5 L 355.9 92 L 357.5 91.6 L 359.1 91.2 L 360.7 90.8 L 362.4 90.4 L 364 90 L 365.6 89.6 L 367.3 89.3 L 368.9 89 L 370.5 88.7 L 372.2 88.4 L 373.8 88.1 L 375.4 87.9 L 377.1 87.6 L 378.7 87.4 L 380.3 87.2 L 381.9 87 L 383.5 86.9 L 385 86.7 L 386.6 86.6 L 388.2 86.5 L 389.7 86.4 L 391.2 86.4 L 392.7 86.3 L 394.2 86.3 L 395.7 86.3 L 397.2 86.3 L 398.6 86.3 L 400 86.4 L 401.4 86.4 L 402.8 86.5 L 404.1 86.6 L 405.5 86.7 L 406.8 86.9 L 408 87 L 409.3 87.2 L 410.5 87.4 L 411.7 87.6 L 412.8 87.9 L 413.9 88.1 L 415 88.4 L 416.1 88.7 L 417.1 89 L 418.1 89.3 L 419.1 89.6 L 420 90 L 420.9 90.4 L 421.7 90.8 L 422.6 91.2 L 423.3 91.6 L 424.1 92 L 424.8 92.5 L 425.4 92.9 L 426.1 93.4 L 426.7 93.9 L 427.2 94.4 L 427.7 94.9 L 428.2 95.5 L 428.6 96 L 429 96.6 L 429.3 97.1 L 429.6 97.7 L 429.9 98.3 L 430.1 98.9 L 430.2 99.5 L 430.4 100.1 L 430.4 100.8 L 430.5 101.4 L 430.5 102.1 L 430.4 102.7 L 430.3 103.4 L 430.2 104.1 L 430 104.7 L 429.8 105.4 L 429.6 106.1 L 429.3 106.8 L 428.9 107.5 L 428.5 108.2 L 428.1 108.9 L 427.6 109.7 L 427.1 110.4 L 426.6 111.1 L 426 111.8 L 425.4 112.5 L 424.7 113.3 Z" fill="currentColor" fill-opacity="0.1"/>
    <path d="M 396.3 141.7 L 284.3 141.7 L 339.7 86.3 L 451.7 86.3 Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" stroke-dasharray="6 3"/>
    <path d="M 388 133.6 L 308.8 133.6 L 348 94.4 L 427.2 94.4 Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9"/>
    <path d="M 424 114 L 423.3 114.7 L 422.5 115.5 L 421.7 116.2 L 420.8 116.9 L 419.9 117.6 L 419 118.3 L 418 119.1 L 417 119.8 L 416 120.5 L 414.9 121.2 L 413.8 121.9 L 412.7 122.6 L 411.5 123.3 L 410.3 123.9 L 409.1 124.6 L 407.9 125.3 L 406.6 125.9 L 405.3 126.6 L 404 127.2 L 402.6 127.9 L 401.3 128.5 L 399.9 129.1 L 398.5 129.7 L 397 130.3 L 395.6 130.9 L 394.1 131.4 L 392.6 132 L 391.1 132.5 L 389.5 133.1 L 388 133.6 L 386.4 134.1 L 384.9 134.6 L 383.3 135.1 L 381.7 135.5 L 380.1 136 L 378.5 136.4 L 376.9 136.8 L 375.3 137.2 L 373.6 137.6 L 372 138 L 370.4 138.4 L 368.7 138.7 L 367.1 139 L 365.5 139.3 L 363.8 139.6 L 362.2 139.9 L 360.6 140.1 L 358.9 140.4 L 357.3 140.6 L 355.7 140.8 L 354.1 141 L 352.5 141.1 L 351 141.3 L 349.4 141.4 L 347.8 141.5 L 346.3 141.6 L 344.8 141.6 L 343.3 141.7 L 341.8 141.7 L 340.3 141.7 L 338.8 141.7 L 337.4 141.7 L 336 141.6 L 334.6 141.6 L 333.2 141.5 L 331.9 141.4 L 330.5 141.3 L 329.2 141.1 L 328 141 L 326.7 140.8 L 325.5 140.6 L 324.3 140.4 L 323.2 140.1 L 322.1 139.9 L 321 139.6 L 319.9 139.3 L 318.9 139 L 317.9 138.7 L 316.9 138.4 L 316 138 L 315.1 137.6 L 314.3 137.2 L 313.4 136.8 L 312.7 136.4 L 311.9 136 L 311.2 135.5 L 310.6 135.1 L 309.9 134.6 L 309.3 134.1 L 308.8 133.6 L 308.3 133.1 L 307.8 132.5 L 307.4 132 L 307 131.4 L 306.7 130.9 L 306.4 130.3 L 306.1 129.7 L 305.9 129.1 L 305.8 128.5 L 305.6 127.9 L 305.6 127.2 L 305.5 126.6 L 305.5 125.9 L 305.6 125.3 L 305.7 124.6 L 305.8 123.9 L 306 123.3 L 306.2 122.6 L 306.4 121.9 L 306.7 121.2 L 307.1 120.5 L 307.5 119.8 L 307.9 119.1 L 308.4 118.3 L 308.9 117.6 L 309.4 116.9 L 310 116.2 L 310.6 115.5 L 311.3 114.7 L 312 114 L 312.7 113.3 L 313.5 112.5 L 314.3 111.8 L 315.2 111.1 L 316.1 110.4 L 317 109.7 L 318 108.9 L 319 108.2 L 320 107.5 L 321.1 106.8 L 322.2 106.1 L 323.3 105.4 L 324.5 104.7 L 325.7 104.1 L 326.9 103.4 L 328.1 102.7 L 329.4 102.1 L 330.7 101.4 L 332 100.8 L 333.4 100.1 L 334.7 99.5 L 336.1 98.9 L 337.5 98.3 L 339 97.7 L 340.4 97.1 L 341.9 96.6 L 343.4 96 L 344.9 95.5 L 346.5 94.9 L 348 94.4 L 349.6 93.9 L 351.1 93.4 L 352.7 92.9 L 354.3 92.5 L 355.9 92 L 357.5 91.6 L 359.1 91.2 L 360.7 90.8 L 362.4 90.4 L 364 90 L 365.6 89.6 L 367.3 89.3 L 368.9 89 L 370.5 88.7 L 372.2 88.4 L 373.8 88.1 L 375.4 87.9 L 377.1 87.6 L 378.7 87.4 L 380.3 87.2 L 381.9 87 L 383.5 86.9 L 385 86.7 L 386.6 86.6 L 388.2 86.5 L 389.7 86.4 L 391.2 86.4 L 392.7 86.3 L 394.2 86.3 L 395.7 86.3 L 397.2 86.3 L 398.6 86.3 L 400 86.4 L 401.4 86.4 L 402.8 86.5 L 404.1 86.6 L 405.5 86.7 L 406.8 86.9 L 408 87 L 409.3 87.2 L 410.5 87.4 L 411.7 87.6 L 412.8 87.9 L 413.9 88.1 L 415 88.4 L 416.1 88.7 L 417.1 89 L 418.1 89.3 L 419.1 89.6 L 420 90 L 420.9 90.4 L 421.7 90.8 L 422.6 91.2 L 423.3 91.6 L 424.1 92 L 424.8 92.5 L 425.4 92.9 L 426.1 93.4 L 426.7 93.9 L 427.2 94.4 L 427.7 94.9 L 428.2 95.5 L 428.6 96 L 429 96.6 L 429.3 97.1 L 429.6 97.7 L 429.9 98.3 L 430.1 98.9 L 430.2 99.5 L 430.4 100.1 L 430.4 100.8 L 430.5 101.4 L 430.5 102.1 L 430.4 102.7 L 430.3 103.4 L 430.2 104.1 L 430 104.7 L 429.8 105.4 L 429.6 106.1 L 429.3 106.8 L 428.9 107.5 L 428.5 108.2 L 428.1 108.9 L 427.6 109.7 L 427.1 110.4 L 426.6 111.1 L 426 111.8 L 425.4 112.5 L 424.7 113.3 Z" fill="none" stroke="currentColor" stroke-width="1.9"/>
    <circle cx="388" cy="133.6" r="2.2" fill="currentColor"/>
    <circle cx="308.8" cy="133.6" r="2.2" fill="currentColor"/>
    <circle cx="348" cy="94.4" r="2.2" fill="currentColor"/>
    <circle cx="427.2" cy="94.4" r="2.2" fill="currentColor"/>
    <line x1="368" y1="226" x2="424" y2="114" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.75"/>
    <path d="M 388.6 184.9 A 46 46 0 0 0 368 180" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
    <line x1="380.6" y1="182.2" x2="430" y2="200" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="433" y="204" font-size="11">arctan μ = 26.6°</text>
    <line x1="368" y1="114" x2="421.8" y2="114" stroke="currentColor" stroke-width="2.2" marker-end="url(#cftkA)"/>
    <circle cx="368" cy="114" r="2.4" fill="currentColor"/>
    <text x="280" y="60" font-size="11" fill-opacity="0.85">단면</text>
    <text x="280" y="73" font-size="11" fill-opacity="0.85" xml:space="preserve">f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 2.00 N</tspan></text>
    <line x1="300" y1="78" x2="284.3" y2="141.7" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <line x1="453.7" y1="84.3" x2="455" y2="50" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="46" font-size="11">외접 상자,</text>
    <text x="458" y="59" font-size="11">모서리 1.414 N</text>
    <line x1="432.5" y1="101.7" x2="455" y2="101" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="98" font-size="11">원</text>
    <text x="458" y="111" font-size="11" xml:space="preserve">μf<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 1.00 N</tspan></text>
    <line x1="376.3" y1="127.5" x2="455" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="147" font-size="11">내접 4-생성자,</text>
    <text x="458" y="160" font-size="11">평평한 변 0.707 N</text>
    <line x1="427" y1="116" x2="455" y2="125" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.55"/>
    <text x="458" y="129" font-size="11">1 N 닦기 (패널에)</text>
  </g>
  <g fill="currentColor" transform="translate(0,34)">
    <line x1="8" y1="282" x2="552" y2="282" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
    <text x="12" y="300" font-size="12" fill-opacity="0.85" font-weight="600">간극 축</text>
    <line x1="98.8" y1="382" x2="451.6" y2="382" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
    <line x1="250" y1="382" x2="250" y2="316" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6" marker-end="url(#cftkB)"/>
    <path d="M 138 382 L 138 386 M 194 382 L 194 386 M 250 382 L 250 386 M 306 382 L 306 386 M 362 382 L 362 386 M 418 382 L 418 386" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="138" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">+4</text>
    <text x="194" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">+2</text>
    <text x="250" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">0</text>
    <text x="306" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">−2</text>
    <text x="362" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">−4</text>
    <text x="418" y="398" font-size="11" text-anchor="middle" fill-opacity="0.85">−6</text>
    <text x="457.6" y="386" font-size="11" fill-opacity="0.85">φ (mm)</text>
    <text x="244" y="318" font-size="11" text-anchor="end" fill-opacity="0.85" xml:space="preserve">f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> (N)</tspan></text>
    <line x1="250" y1="382" x2="104.4" y2="382" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="250" y1="382" x2="250" y2="320.8" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="250" y1="382" x2="434.8" y2="318.6" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="5 3"/>
    <circle cx="194" cy="382" r="4.5" fill="currentColor"/>
    <circle cx="390" cy="334" r="4.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
    <text x="12" y="378" font-size="12">φ &gt; 0, 떨어짐:</text>
    <text x="12" y="393" font-size="12" xml:space="preserve">f<tspan dy="3.4" font-size="11">n</tspan><tspan dy="-3.4"> = 0</tspan></text>
    <text x="258" y="325.6" font-size="12" xml:space="preserve">φ = 0: f<tspan dy="3.4" font-size="11">n</tspan><tspan dy="-3.4"> ≥ 0</tspan></text>
    <text x="194" y="356" font-size="11" text-anchor="middle">+2 mm,</text>
    <text x="194" y="370" font-size="11" text-anchor="middle">닿기 전</text>
    <text x="400" y="342" font-size="11" xml:space="preserve">−5 mm, f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 2.00 N</tspan></text>
    <text x="400" y="356" font-size="11" fill-opacity="0.85">페널티는 허용, 강체는 금지</text>
    <text x="311.6" y="375" font-size="11" fill-opacity="0.85" xml:space="preserve">페널티 f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = k</tspan><tspan dy="3.1" font-size="11">w</tspan><tspan dy="-3.1">δ</tspan></text>
    <text x="12" y="420" font-size="12" fill-opacity="0.9" xml:space="preserve">(φ, f<tspan dy="3.4" font-size="11">n</tspan><tspan dy="-3.4">)은 굵은 두 반직선을 벗어나지 않는다 — 그 그림이 곧 complementarity</tspan></text>
    <path d="M 246 358 L 250 358 M 246 334 L 250 334" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
    <text x="242" y="362" font-size="10.5" text-anchor="end" fill-opacity="0.85">1</text>
    <text x="242" y="338" font-size="10.5" text-anchor="end" fill-opacity="0.85">2</text>
  </g>
</svg>

왼쪽은 $x$–$y$ 평면에 실제 비율로 그린 $\theta=(0^\circ,90^\circ)$의 P2이고, 패널 면 $x=1\,\mathrm m$은 그 평면 뒤로 물러서 그렸다. 그래서 전완은 그 옆을 지나가고, 말단에서 면 앞으로 비켜 뒤로 뻗은 L자 도구의 짧은 발만 면에 닿는다. 닿는 자리에는 접촉 프레임($\hat n$은 패널 안쪽, $\hat t_1$은 닦는 방향으로 면을 따라 아래), $\delta=5\,\mathrm{mm}$만큼 눌린 $k_w=400\,\mathrm{N/m}$ 접촉 스프링의 확대, 그리고 떼어 그린 접촉력이 있다. 도구는 패널을 $f=(2.00,-1.00)\,\mathrm N$으로 밀고 패널은 도구를 $-f$로 되밀며, 그 누름을 유지하는 데 관절이 드는 토크는 $\tau=J^\top f=(-3,-2)\,\mathrm{N{\cdot}m}$다. 오른쪽은 반각 $\arctan\mu=26.6^\circ$의 마찰 원뿔을 $f_n=2.00\,\mathrm N$에서 자른 단면으로, $\mu f_n=1.00\,\mathrm N$의 원이 외접 상자(모서리 $1.414\,\mathrm N$)와 내접 4-생성자 정사각형(평평한 변 $0.707\,\mathrm N$) 사이에 놓이고, 같은 축척으로 그린 패널에 걸리는 $1\,\mathrm N$ 닦기는 정확히 원 위에서, 정사각형 바깥에서 끝난다. 아래는 간극 축으로, $(\phi,f_n)$은 complementarity의 굵은 두 반직선을 벗어나지 않으며, 닿기 전 $+2\,\mathrm{mm}$에서는 $f_n=0$이고 $2.00\,\mathrm N$의 $-5\,\mathrm{mm}$ 침투는 페널티 모델은 허용하고 강체 모델은 금지한다.

### 대상으로 한 번 끝까지: 간극에서 파지 여유까지 · Worked case

위의 대상에서 여섯 단계를 밟는다. 각 단계는 제목에 적은 절이 증명하고, 4단계는 §2의 몫이라 여기서는 가리키기만 한다. 과제는 표의 항목 두 개만 바꿔 2–4단계와 6단계, 그리고 그림을 다시 계산한다.

**1단계 — 접촉이 있기는 한가? (§1).** 도구를 면에서 2 mm 앞에 둔다. 간극 $\phi$ — 도구에서 면까지의 거리로, 떨어져 있는 동안 양수이고 강체라면 음수가 될 수 없다(§1) — 는 $\phi=0.002$ m, $f_n=0$ N이므로 $\phi f_n=0$이고 쌍은 왼쪽 반직선 위에 있다. 면까지 몰면 $\phi=0$이고, 이제 $f_n$은 음이 아니기만 하면 무엇이든 될 수 있다 — 모델이 힘을 예측하기를 그만두고 제약하기만 시작한 것이다. 그 전환이 어려움의 전부다. 두 경우가 서로 다른 방정식 묶음이므로, 어느 쪽인지 정하는 값은 명령이 아니라 *측정*이다.

**2단계 — 법선력은 얼마인가? (§3).** 강체 모델은 $\phi=0$에서 $f_n\ge0$만 말하므로 답할 수 없다. $\delta=5$ mm 안쪽을 명령하면 강체 모델은 실행 불가능해지니, 비침투를 스프링과 댐퍼, 곧 표의 $k_w$와 $d_c$와 맞바꾸는 페널티 모델을 쓴다. 도구는 처음 닿는 순간부터 5 mm에서 멈출 때까지 $\dot\delta=0.02$ m/s로 다가오므로, 처음 닿을 때는 댐퍼만 $d_c\dot\delta=4\times0.02=0.08$ N을 밀고, 멈추기 직전에는

$$f_n=k_w\,\delta+d_c\,\dot\delta=400\times0.005+4\times0.02=2.00+0.08=2.08\ \mathrm{N}$$

이다. 그래서 정지하면 패널이 받는 힘은 $f_n=2.00$ N이고, 나머지 $0.08$ N은 도구가 아직 다가오는 동안에만 있다. 이 2 N을 붙들어 두자. 아래의 모든 경계가 여기에 비례한다.

**3단계 — 닦는 힘은 얼마까지 견디는가? (§2).** 원뿔의 반각은 $\arctan 0.5=26.5651^\circ\to26.6^\circ$이고, $f_n=2.00$ N에서 허용하는 것은

$$\lVert f_t\rVert\le\mu f_n=0.5\times2.00=1.00\ \mathrm{N}$$

이다. 접선력은 법선력의 $\mu$배까지만 커질 수 있기 때문이다. 아래로 3 N 닦기는 경계의 세 배라 도구가 면을 따라 아래로 미끄러지고, 마찰은 미끄럼에 맞서 경계 위에 앉는다. 마찰은 도구를 면을 따라 위로 $1.00$ N 밀고, 작용·반작용으로 패널은 아래로 $1.00$ N 끌려간다. $f$는 패널에 걸리는 힘이므로(계속 쓰는 대상의 규약) $\hat t_1$ 방향으로 $f_t=+1.00$ N이다. 1 N 닦기는 경계 *위에 정확히* 놓인다. 허용되지만 여유는 0이다. "고착한다"의 정직한 독법이 이것이다. 모델이 허락할 뿐, $\mu$가 1%만 달라져도 버틴다는 말은 모델 어디에도 없다. 2 N 누름 아래 1 N 닦기를 유지하는 힘, 곧 $(x,y)$ 성분으로 $f=(2.00,-1.00)$ N에는 [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §3]]의 정역학대로 관절 토크 $\tau=J^\top f=(-3,-2)$ N·m가 들고, 그 장의 과제 2(e)가 같은 면을 10 N으로 누른다.

**4단계 — 솔버는 무엇을 믿어도 되는가? (§2).** 이차계획으로 남아야 하는 계획기는 둥근 원뿔을 평평한 면들로 바꾸는데, 바로 이 접촉에서 표준적인 두 대체가 서로 반대 방향으로 틀린다. 외접 상자는 미끄러질 $1.414$ N 닦기를 허가하고, 4-생성자 내접 원뿔은 실제 접촉이 버티는 1 N 닦기를 거절하고 $0.707$ N까지만 허용한다. 둘 다 §2가 계속 쓰는 대상 위에서 계산한다. 처음 읽을 때는 두 숫자만 가지고 넘어가라.

**5단계 — 같은 접촉을 물체 렌치로 (§4).** 패널 프레임 원점을 접촉에서 $r_b=0.40$ m 아래인 장착 브래킷에 두면 $r=(0,0.40,0)$ m이고, 1 N 닦기를 포함한 접촉력, 곧 도구가 패널에 가하는 힘은 $f=(2.00,-1.00,0)$ N이다. 물체가 느끼는 것은 **렌치**, 곧 그 힘이 원점에 대해 만드는 모멘트 $m=r\times f$를 힘 자체 위에 쌓은 것이고, 순서는 Modern Robotics를 따른다([[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §6]], 이 페이지 §4). 그러면 $m=r\times f=(0,0,-0.80)$ N·m이므로

$$\mathcal{F}=\begin{pmatrix}m\\ f\end{pmatrix}=(0,\ 0,\ -0.80,\ 2.00,\ -1.00,\ 0)$$

이고, 패널은 아무도 명령하지 않은 $z$축 둘레 0.80 N·m 모멘트를 느낀다. 그것이 생긴 이유는 원점을 $0.40$ m 옮겼기 때문이고 물리적 밀기는 그대로다. 원점을 접촉으로 옮기면 모멘트는 0이 된다.

**6단계 — 그다음 패널을 들어야 하는 파지 (§4).** 손가락 둘이 1.0 kg 패널을 $\pm0.05$ m에서 각각 $f_g=10$ N으로 조인다. 각 원뿔이 $\mu\times10=5$ N의 접선력을 허용하므로 둘이 합쳐 $2\times5=10.0$ N을 버티고, 무게는 $m_pg=1.0\times9.81=9.81$ N이다. 여유는 $0.19$ N, 곧 하중의 $1.9\%$다. 같은 말로, 파지가 딱 버티는 마찰 계수는

$$\mu^\star=\frac{m_pg}{2f_g}=\frac{9.81}{2\times10}=0.4905$$

이다. 두 원뿔이 함께 무게 전체를 져야 하기 때문이다. 명목값 $\mu=0.5$는 $1.9\%$ 차이로 넘긴다. 먼지가 $\mu$를 $0.40$으로 떨어뜨리면 버티는 힘이 8.0 N이 되어 무게보다 1.81 N 모자라고, 패널은 바닥으로 간다. 같은 경계가 현장의 외장 패널도 붙잡는다. 건설 트랙의 20 kg 패널 과제 S1([[05-construction-robotics/site-engineering|2.5]])은 벽에서 진공 컵에 매달리고, [[02-foundations/fluid-power|0.6.3 유체 동력 §9]]는 컵들의 법선력 $1885$ N이 수직 면을 따라 많아야 $0.5\times1885=942$ N을 버틴다고 계산한다. 패널의 $196.2$ N에 대한 $4.80$배이고, 이것도 측정하지 않은 같은 $\mu$의 배수다.

**여섯 단계를 합치면.** 닦기의 여유는 정확히 0이고 파지의 여유는 $1.9\%$인데, *두 경계 모두 같은 $\mu$에서 나온다* — 측정한 적 없이 가정한 수이고, 카메라 속 패널을 1픽셀도 움직이지 않으면서 먼지가 바꾸는 수다. 이 페이지의 모든 양은 제어기가 정하는 $f_n$에 비례하거나, 아무도 관측하지 않은 $\mu$에 비례한다. §7은 그 틈을 측정으로 메우는 이야기이고, §9는 접촉 주장이 뜻을 가지려면 논문이 무엇을 보고해야 하는지에 관한 이야기다.

### 1. 접촉이 문제를 바꾸는 이유

접촉은 보통 **단방향**(unilateral)이다: 물체는 밀 수 있지만 평범한 표면을 통해 당길 수는 없다. 운동은 분리·충격·고착(sticking)·미끄럼(sliding) 사이를 오간다. 그래서 동역학이 하이브리드가 되고 대개 비매끄럽다.

$\phi(q)$를 **간극**이라 하자. 로봇과 물체가 컨피규레이션 $q$에 있을 때 두 표면의 가장 가까운 두 점 사이 거리이고(탁자 위 손끝이라면 그냥 탁자 위 높이), 떨어져 있으면 양수, 닿으면 0이다. 실제로는 충돌 기하 라이브러리가 두 형상과 자세로부터 계산한다. 간극 $\phi(q)\ge 0$와 법선력 $f_n\ge 0$에 대해 이상적 강체 접촉은

$$\phi(q)f_n=0$$

으로 요약된다. 떨어져 있으면 힘이 0이고, 법선력이 양수면 간극이 닫혀 있다. 이 complementarity는 이상화된 모델이지 재료 변형의 문자 그대로의 기술이 아니다.

**강체 단방향 접촉의 세 조건.** 이 모델은 두 스칼라, 곧 간극 $\phi(q)$와 법선력 $f_n$(접촉 법선 방향의 힘 성분으로, 두 표면이 서로 밀어낼 때 양수)에 대한 조건들의 묶음이다. 세 조건이 모두 성립할 때 **complementarity 조건**(상보성 조건)을 만족한다고 한다.

- **비침투**: 두 물체는 겹치지 않으므로 간극이 음수일 수 없다.
$$\phi(q)\ge 0$$
- **단방향성**: 표면은 밀 수만 있고 당길 수 없으므로 법선력이 음수일 수 없다.
$$f_n\ge 0$$
- **complementarity**: 힘은 닫힌 간극을 통해서만 작용하므로 둘 중 많아야 하나만 0이 아니다.
$$\phi(q)\,f_n=0$$

셋을 한데 묶어 $0\le\phi(q)\perp f_n\ge 0$로 쓰고, $\perp$는 "곱이 0"이라는 뜻이다. 떨어져 있고 $f_n=0$인 경우와 닿아 있고 $f_n\ge0$인 경우가 서로 다른 방정식 묶음이므로 동역학이 **접촉 모드** 사이를 전환하고, 이것이 접촉을 하이브리드·비매끄럽게 만든다. 접촉점마다 이 조건을 쌓으면 시뮬레이션 한 스텝이 **선형 상보성 문제**(LCP)가 되고, 강체 시뮬레이터가 푸는 것이 이 형태다([[06-research-practice/simulators-benchmarks-datasets|연구 실무 7. 시뮬레이터·벤치마크·데이터셋]]). 아래 메모가 그것을 풀어 쓰고 탁자 위 블록 하나로 풀어 보며, 이 페이지의 깊이 목표는 솔버를 두 번째 읽기로 미룬다.

> [!example] 계산 예제 · Worked example
> 탁자 위 2 mm에 들고 있는 0.1 kg 블록은 $\phi=0.002$ m, $f_n=0$이므로 $\phi f_n=0$ ✓. 내려놓고 정지하면 $\phi=0$, $f_n=mg=0.1\times9.81=0.981$ N이고 역시 $\phi f_n=0$ ✓.
> **비예**: $\phi=0.001$ m에서 $f_n=0.5$ N은 complementarity 위반(열린 간극을 가로지르는 힘), $f_n=-0.5$ N은 단방향성 위반(탁자가 블록을 끌어당김), $\phi<0$은 비침투 위반이다. 페널티 모델(§3)은 마지막 것을 일부러 허용한다.

> [!note]- 더 깊이 · Deeper
> **시뮬레이터가 푸는 방식: LCP.** LCP는 모델이 아니라 *문제*다. 정사각 행렬 $M$과 벡터 $q$가 주어졌을 때(관례적인 글자이고, 이 $q$는 컨피규레이션이 아니다) 다음을 만족하는 벡터 $z$와 $w$를 찾는다.
>
> $$z\ge0,\qquad w=Mz+q\ge0,\qquad z^\top w=0$$
>
> — 위의 세 조건과 같은 모양이고, 접촉마다 쌍 $(z_i,w_i)$가 하나씩 있다. 시간 적분 시뮬레이터에서 $z_i$는 한 스텝 동안 접촉 $i$가 받는 법선 충격량, $w_i$는 스텝이 끝난 뒤의 법선 속도다. 간극이 한 번 닫히면 조건이 위치에서 속도로 옮겨 가기 때문이다. 두 표면은 떨어지거나($w_i>0$, 충격량 없음) 붙어 있거나($w_i=0$, 충격량 $z_i\ge0$) 둘 중 하나이고, 둘 다일 수는 없다.
>
> **같은 블록을 LCP로**, $h=0.01$ s 한 스텝: 스텝 뒤의 속도는 $w=v-gh+z/m$이므로 $M=1/m=10\ \mathrm{kg^{-1}}$, $q=v-gh=0-0.0981=-0.0981$ m/s다. $z=0$이면 $w=q<0$, 곧 블록이 탁자 속으로 가라앉으므로 해는 $w=0$, $z=-q/M=0.00981$ N·s다 — 평균 힘으로 $z/h=0.981$ N $=mg$, 위의 정지 힘을 솔버가 찾아낸 것이다. **비예**: 위로 $v=0.5$ m/s로 움직이는 블록은 $q=0.4019>0$이므로 LCP는 $z=0$, $w=0.4019$ m/s를 돌려주고 블록은 떠난다. 등식 $w=0$만 풀면 대신 $z=-0.0402$ N·s, 곧 탁자가 블록을 끌어내리는 답이 나온다. 부등식 둘이 빠진 등식은 LCP가 아니다.

### 2. 법선력과 마찰

접촉의 마찰 계수는 닦기가 고착하는지, 쥔 패널이 미끄러지는지를 정하는 수인데, 아무도 재지 않는 수이기도 하다. 쥔 패널의 먼지는 시각적 자세를 거의 바꾸지 않고 쓸 수 있는 마찰을 바꿀 수 있으므로, $\mu$를 안다고 취급하는 계획기는 접촉 여유를 과대평가할 수 있다. 이 절은 접촉 하나가 견딜 수 있는 것의 경계를 긋고, 그 경계를 솔버가 다루기 좋게 근사한 것들이 각각 어느 쪽으로 틀리는지 말한다.

1차원에서 이것은 [[02-foundations/basic-mechanics|0.6.1 §4]]의 Coulomb 마찰이다(되짚기). 고착한 접촉은 멈춰 있는 데 필요한 접선력을 법선력의 $\mu$배까지 무엇이든 내고, 미끄러지는 접촉은 정확히 그만큼으로 미끄럼에 맞선다. 여기서는 접선력이 면 안의 벡터이므로 경계는

$$\lVert f_t\rVert\le \mu f_n$$

로 읽힌다. $f_n$은 법선력, $f_t$는 접선력, $\mu$는 마찰 계수다. 경계 안의 힘은 고착과 양립할 수 있고, 경계 위의 힘은 미끄러지기 직전을, 경계를 넘는 요구는 실제 미끄럼을 뜻한다. 이 경계는 *힘의 실행 가능성 경계*다 — 실제로 고착하는지 미끄러지는지는 상대 운동과 접촉 법칙에도 의존한다.

**마찰 원뿔과 Coulomb 법칙, 부분마다 이름을 붙여.** 접촉력 $f\in\mathbb{R}^3$ — 계속 쓰는 대상에서처럼 도구가 패널에 가하는 힘 — 를 법선 성분 $f_n$(단위 법선 방향의 스칼라)과 접선 성분 $f_t\in\mathbb{R}^2$(접촉 평면 안)로 나누고, $f$가 작용하는 물체가 다른 물체에 대해 그 평면 안에서 미끄러지는 속도를 $v_t$라 하자. 여기서는 도구에 대한 패널의 속도다. **마찰 원뿔**은 모델이 허용하는 접촉력의 집합이다.

$$FC=\{\,f:\ f_n\ge 0,\ \lVert f_t\rVert\le\mu f_n\,\}$$

그래서 조건은 둘이다. **단방향성**($f_n\ge0$, §1과 같음)과 **Coulomb 경계**($\lVert f_t\rVert\le\mu f_n$). 이 경계는 접선 대 법선의 비가 $\mu$가 될 때까지 힘이 법선에서 기울 수 있다는 뜻이므로, 원뿔은 법선을 축으로 반각 $\arctan\mu$인 원형 원뿔이다. **Coulomb 법칙**은 여기에 힘이 어느 경계에 놓이는지를 더한다.

- **고착**($v_t=0$): $FC$ 안의 어떤 $f$든 허용되고, $f_t$는 접촉을 멈춰 두는 데 필요한 값이 된다.
- **미끄럼**($v_t\ne0$): 마찰은 에너지를 소산하므로 힘은 원뿔 표면에 놓이고 미끄럼과 반대 방향이다.
$$f_t=-\mu f_n\,\frac{v_t}{\lVert v_t\rVert}$$
  계속 쓰는 대상에서는 도구가 면을 따라 아래로 미끄러지므로 패널은 도구에 대해 위로 움직이고, $v_t$는 $-\hat t_1$ 방향이며 $f_t=+\mu f_n\hat t_1$이다. 3단계에서 본 대로 패널이 아래로 끌려간다.

$\mu$ 하나만 쓰면 0.6.1 §4의 정지 마찰 계수 $\mu_s$와 운동 마찰 계수 $\mu_k$가 같다고 가정한 것이다.

**선형화한 마찰 원뿔, 그리고 어느 쪽으로 틀리는가.** 경계 $\lVert f_t\rVert\le\mu f_n$은 *2차* 원뿔이다. 제약이 노름이지 선형 부등식들이 아니다. 그래서 이차계획법이 필요한 최적화기는([[02-foundations/optimization|4. 최적화 §5]]) 이것을 **다면 원뿔**(polyhedral cone), 곧 유한한 개수의 평평한 면으로 둘러싸인 원뿔로 바꾼다. 표준적인 대체가 둘이고, 둘은 서로 반대쪽에서 근사하며, 양쪽을 모두 "마찰 피라미드"라고 부르는 순간 오차의 방향이 사라진다. 계속 쓰는 대상이 P2가 평면인데도 접선을 둘 두는 이유가 이것이다. 접선이 하나면 원뿔은 모서리가 정확히 둘인 쐐기이고 다면체가 그것을 오차 없이 나타내므로, 아래의 질문 전체 — 접촉 문헌의 최적화기 절반이 사는 곳 — 가 사라져 버린다.

- **외접 상자 피라미드**는 접선 축을 하나씩 따로 묶는다. $|f_{t,1}|\le\mu f_n$, $|f_{t,2}|\le\mu f_n$ — 축마다 두 면씩 네 면이다. 참 원뿔을 **포함하므로** 미끄러질 힘까지 허용한다. 모서리는 참 경계의 $\sqrt2$배에 닿아 $41.4\%$ 후하다. [[04-robotics/convex-mpc-legged|8. Convex MPC]]가 네 번째 모델링 수에서 쓰는 형태가 이것이고, 계수를 $\mu/\sqrt2$로 줄이는 것이 그 페이지가 오차를 되사는 방법이다.
- **내접 다면 원뿔**은 대신 법선 둘레에 고르게 놓인 $m$개의 생성자 반직선으로 *생성*되며, 각 반직선은 참 원뿔의 표면 위에 있다. 볼록한 원뿔 위 반직선들의 음이 아닌 결합은 원뿔을 벗어날 수 없으므로, 이 집합이 허용하는 힘은 모두 참 원뿔 **안**에 있다. 대가는 버리는 마찰이다. 유효 계수가 $\mu\cos(\pi/m)$이 되어, $m=4$에서 $0.354$($\mu$의 $29.3\%$를 버림), $m=8$에서 $0.462$($7.6\%$), $m=16$에서 $0.490$($1.9\%$)이다. 가장 불리한 방향에서 원뿔이 허용하는 최대 접선력의 손실이다. 아래 메모가 생성자를 풀어 쓰고 면적으로 잰 손실을 함께 준다.

> [!note]- 더 깊이 · Deeper
> **생성자, 그리고 손실을 세는 두 방법.** 내접 원뿔은 생성자들이 생성하므로, 허용하는 모든 힘은
>
> $$f=\sum_{j=1}^{m}\lambda_j\,g_j,\qquad \lambda_j\ge0,\qquad g_j=\hat n+\mu\left(\cos\tfrac{(2j-1)\pi}{m}\,\hat t_1+\sin\tfrac{(2j-1)\pi}{m}\,\hat t_2\right)$$
>
> 꼴이다. $\lambda_j$는 반직선 $j$에 걸리는 음이 아닌 가중치이고 $m$은 모델러가 고르는 면의 수다. 각도를 반 칸 어긋나게 두었으므로 각 접선 축 위에는 반직선이 아니라 면의 한가운데가 오고, 그래서 닦기 방향 $\hat t_1$ 자체가 이 원뿔의 가장 불리한 방향이다. [[04-robotics/grasping|15. 파지 §2]]는 생성자를 축 위에 둔다(각도 $2\pi j/m$). 그러면 4-생성자 원뿔이 $\hat t_1$ 방향 1 N 닦기를 온전히 버티고 $29.3\%$는 $45^\circ$ 방향에서 잃는다. 최악의 계수 $\mu\cos(\pi/m)$, 곧 내접 다각형의 내접원 반지름은 두 배치에서 같고, 어느 방향이 그 값을 받는지만 다르다. 대신 다각형이 남기는 접선 원판의 *면적*, 곧 원판의 $\tfrac{m}{2\pi}\sin\tfrac{2\pi}{m}$로 재면 $m=4$, $8$, $16$에서 손실은 $36.3\%$, $10.0\%$, $2.6\%$다. 파지 §2는 둘을 함께 적고, 둘 중 어느 것인지 밝히지 않은 선형화 손실은 다른 손실과 비교할 수 없다.

**계속 쓰는 대상에서 — '대상으로 한 번 끝까지'의 4단계.** $f_n=2.00$ N에서 참 경계는 모든 방향으로 $1.00$ N이다. 외접 상자의 모서리는 $\sqrt{1.00^2+1.00^2}=1.414$ N을 허용해 참 경계보다 $41.4\%$ 크므로, 미끄러질 닦기를 허가해 준다. 4-생성자 내접 원뿔은 $\hat t_1$ 방향으로 $0.354\times2.00=0.707$ N까지만 허용하므로, 실제 접촉이 허용하는 1 N 닦기를 거절한다. 생성자가 여덟이면 $0.924$ N, 열여섯이면 $0.981$ N으로, 경계보다 $7.6\%$와 $1.9\%$ 모자란다.

$m=4$에서는 내접 원뿔의 계수 $\mu\cos(\pi/4)$와 줄인 상자의 $\mu/\sqrt2$가 같은 수 $0.354$가 되고, 그림처럼 반직선을 접선 축과 $45^\circ$로 놓으면 4-생성자 원뿔이 곧 줄인 상자다. 두 구성이 그렇게 쉽게 헷갈리는 이유다. 그래도 온전한 $\mu$의 상자와 내접 원뿔은 서로 다른 집합이고, 요점은 오차의 방향이다. **외접은 파지에 낙관적이고 내접은 비관적이며, 둘 다 원뿔은 아니다.** 어느 쪽을 풀었는지가, 그 계획기가 버틸 수 없는 접촉을 약속하는지 버틸 수 있는 접촉을 거절하는지를 정한다.

> [!example] 계산 예제 · Worked example
> $\mu=0.5$이면 반각은 $\arctan0.5=26.6°$다. $f_n=10$ N이면 원뿔은 $\lVert f_t\rVert\le5$ N을 허용한다. 4 N 접선 하중은 고착할 수 있고, 6 N 요구는 그럴 수 없다.
> **비예**: $f_n=-2$ N은 $f_t$가 아무리 작아도 어떤 $\mu$에서든 원뿔 밖이다. 표면은 당길 수 없기 때문이다. 그리고 원형 원뿔은 위의 두 다면 원뿔 어느 쪽과도 같은 집합이 아니다. 솔버가 보고하는 마찰 여유가 제 면에 대한 여유인 이유가 그것이다.

**여기서 얻는 독법.** μ를 어떻게 얻고 물체를 놓치기 전에 미끄러짐 피드백으로 잘못된 가정을 고칠 수 있는지 묻는다. 힘 경계는 가능한 실패 기전을 설명하지만 실제 접촉 상태의 관찰을 대신하지는 않는다.

### 3. 강체 모델과 유연 모델

결과가 어떤 접촉 모델 아래서 나왔는지가 중요하다. 겉보기 제어 개선이 더 관대한 시뮬레이션 접촉에서 올 수 있기 때문이다. 순응적인 벽은 단단한 표면에서라면 힘 급증을 만들 닦기 경로 오차를 흡수할 수 있다. 쓰이는 모델은 세 갈래다.

| 모델 | 유용한 경우 | 주된 한계 |
|---|---|---|
| 강체 접촉 | 변형이 과제 스케일 대비 작을 때 | 충격·모드 전환이 비매끄러움 |
| 페널티/유연 접촉 | 시뮬레이션에 연속적 침투력이 필요할 때 | 강성·감쇠의 동정이 어려움 |
| 학습/잔차 모델 | 반복 가능한 불일치가 데이터에 남을 때 | 외삽과 물리적 일관성 |

**페널티 모델을 풀어 쓰면.** 페널티(유연) 접촉은 §1의 비침투 조건을 버리고, 두 물체가 작은 **침투 깊이** $\delta=\max(0,-\phi)$만큼 겹치게 둔 뒤 스프링과 댐퍼처럼 되민다. [[02-foundations/basic-mechanics|0.6.1 §3]]의 한쪽으로만 미는 스프링, 곧 밀기만 하므로 그 절이 선형 스프링의 비예로 드는 P3 자신의 벽에 댐퍼를 곁들인 것이다.

$$f_n=\max\!\big(0,\ k\,\delta+d\,\dot\delta\big)$$

$k$(접촉 강성, N/m)는 주어진 겹침이 만드는 힘의 크기를, $d$(접촉 감쇠, N·s/m)는 겹침 속도 $\dot\delta$에 대한 저항을 정하고, 모델이 절대 당겨서는 안 되므로 바깥의 $\max$가 단방향성을 지킨다. 예: $k=10^4$ N/m, 정지 상태 1 mm 겹침이면 $f_n=10^4\times0.001=10$ N이다. 강체 모델이 전환하는 곳에서 연속적이라 시뮬레이터가 선호하고, 그 대가는 $k$와 $d$가 측정된 재료 상수가 아니라 수치적 선택이라는 점이다. [[06-research-practice/simulators-benchmarks-datasets|연구 실무 7. 시뮬레이터·벤치마크·데이터셋 §3]]의 랩이 P3 핸들 위에서 그 선택의 값을 매긴다. $k$가 가장 큰 안정 스텝을 정하고(반암시적 오일러는 $\Delta t<2\sqrt{m/k}$), 감쇠가 가벼운 접촉에서 명시적 오일러는 $d\ge k\,\Delta t$일 때만 안정하다. **학습 잔차**는 $x_{t+1}=f_{\text{phys}}(x_t,u_t)+r_\theta(x_t,u_t)$ 꼴이다. $f_{\text{phys}}$는 물리 모델의 예측, $r_\theta$는 파라미터 $\theta$로 맞춘 보정이다.

시뮬레이터의 접촉 파라미터는 대개 수치적 타협이다. 한 시뮬레이터 설정에서의 성공이 실제 재료 변동에 대한 강건성의 증거는 아니다.

학습 잔차(물리 기반 모델이 설명하지 못하고 남긴 실제 동역학의 몫에 맞춘 모델)는 반복 불일치를 고치지만 학습 관측이 보정을 제약하는 범위 안에서만 근거가 있다. **여기서 얻는 독법.** 접촉 법칙, 파라미터 식별, 수치 설정을 나눈다. 편한 설정 하나의 성공보다 관련 물리 반응과의 검증을 찾는다.

### 4. 파지와 렌치의 언어

조임이 패널을 버틸까? 두 손가락이 양쪽에서 누르면 알짜 힘은 전혀 없는데도 파지는 패널의 무게를 질 수 있고, 이 절은 그 이유를 말할 언어를 준다. 접촉력 하나가 만드는 렌치, 그것들을 더하는 grasp map, 그리고 그 위에 서는 두 closure다.

접촉력은 물체에 힘과 모멘트를 만들고, 이 둘을 6차원 벡터 하나로 쌓은 것이 **렌치**(wrench)다. 정의 조건은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §6]]에 있고, [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장]]이 관절 토크로 옮긴다. 두 줄로 되짚으면, 고른 물체 원점에서 $r$만큼 떨어진 곳에 가해진 힘 $f$는 렌치 $(r\times f,\ f)$를 만들고, Modern Robotics의 순서대로 모멘트가 위에 온다. 원점을 옮기면 물리적 밀기는 그대로여도 모멘트 좌표가 달라지므로, 힘과 모멘트를 더하기 전에 모든 접촉을 공통 프레임 하나로 표현해야 한다. 예: $r=(0.2,0,0)$ m에 $f=(0,0,-10)$ N이면 $m=r\times f=(0,2,0)$ N·m이고, 물체는 $-z$ 방향으로 10 N과 $y$축 둘레 2 N·m 모멘트를 느낀다.

**Grasp map**은 모든 접촉력을 더해 물체 렌치 하나로 만드는 행렬이다. 그 위에 두 가지 closure 개념이 선다.

- **Form closure**는 명시된 접촉 모델 아래 기하만으로 물체를 고정한다.
- **Force closure**는 허용 접촉력(대개 마찰 포함)으로 임의 외부 렌치에 저항한다.

필요한 접촉 수는 차원, 마찰·접촉 가정, 일반 위치 조건에 의존한다. 일반 위치 조건이란 접촉 법선들이 우연히 한 줄로 늘어서는 것 같은 퇴화한 배치가 없다고 가정한다는 뜻이다.

**Grasp map과 두 closure를 식으로.**

- **Grasp map** $G$는 점접촉 $k$개의 렌치를 더한다. 접촉력을 모두 물체 프레임으로 표현해 $f_c=(f_1,\dots,f_k)\in\mathbb{R}^{3k}$로 쌓으면, 각 열 블록 $G_i$가 $f_i$를 그 렌치로 바꾸므로
$$\mathcal{F}_{\text{obj}}=G\,f_c=\sum_{i=1}^{k}\begin{pmatrix}r_i\times f_i\\ f_i\end{pmatrix}$$
  이고 $G$는 $6\times3k$ 행렬이다. 힘에 대해 선형이므로 closure 질문이 원뿔과 생성(span)의 질문이 된다.
- **Force closure**: 모든 외부 렌치 $\mathcal{F}_{\text{ext}}$에 대해 그것을 상쇄하는 허용 접촉력이 있다. 허용이란 각 $f_i$가 자기 마찰 원뿔 $FC_i$(§2) 안에 있다는 뜻이다.
$$\forall\,\mathcal{F}_{\text{ext}}\in\mathbb{R}^6\ \ \exists\, f_i\in FC_i:\quad G\,f_c=-\mathcal{F}_{\text{ext}}$$
  원뿔은 양의 배율에 닫혀 있으므로, 이는 원뿔들의 $G$에 의한 상이 $\mathbb{R}^6$ 전체라는 말과 같다.
- **Form closure**(1차): 같은 명제를 **마찰 없는** 접촉으로 쓴 것이다. 각 $f_i=\lambda_i n_i$이고 $\lambda_i\ge0$, $n_i$는 안쪽 법선이다. 법선 렌치들이 $\mathbb{R}^6$을 양의 계수로 생성해야 한다(모든 렌치가 그것들의 음이 아닌 결합). 평면에서 최소 4개, 공간에서 최소 7개의 접촉이 필요하고, 그 개수와 단서는 [[04-robotics/grasping|파지 §3]]에 있다.

두 손가락이 패널을 조이는 상황을 보자. 반대 방향 힘은 합성 물체 렌치가 0이어도 접촉의 압축 예압을 유지할 수 있다. [[02-foundations/basic-mechanics|0.6.1 §3]]의 예압, 곧 하중이 그것을 되돌리기 전까지 한쪽으로만 미는 접촉을 붙여 두는 힘이다. 그 예압이 이후 외란에 대한 마찰력을 제공한다. 따라서 합성 렌치가 0이라고 접촉력이 없는 것은 아니다. 세게 조인다고 force closure가 성립하는 것도 아니다. 허용 접촉력들이 마찰과 단방향 접촉 조건 아래 필요한 모든 방향의 외란에 대응해야 한다. 액추에이터 한계가 유한하면 실제로 버틸 하중 집합도 유한하다.

> [!example] 계산 예제 · Worked example
> 손가락이 $r_1=(-0.05,0,0)$ m와 $r_2=(0.05,0,0)$ m에서 $f_1=(10,0,0)$ N, $f_2=(-10,0,0)$ N으로 조인다. 합력은 $(0,0,0)$이고 두 모멘트도 0이다($r_i\parallel f_i$). 그래서 각 접촉에 10 N이 걸려 있어도 $G f_c=0$이다. $\mu=0.5$이면 각 원뿔이 접선력을 $0.5\times10=5$ N까지 허용하므로, 이 조임에서 두 손가락은 수직 하중을 $2\times5=10$ N까지 버틴다.
> **비예**: 같은 조임이라도 마찰 없는 손가락($\mu=0$)은 허용되는 힘이 전부 $x$ 방향이라 수직 하중을 전혀 버티지 못한다. 아무리 세게 조여도 force closure가 아니다.

> [!question] closure의 보장 확인 · Check what closure promises
> force closure이면 선택한 파지로 무거운 패널을 들 수 있는가? **답:** 그것만으로는 부족하다. closure는 접촉 모델 아래의 능력이다. 선택한 힘에서 실제 하중이 마찰·액추에이터·재료 한계 안에도 들어야 한다.

### 5. 위치, 힘, 임피던스, 어드미턴스

뻣뻣한 위치 루프는 벽이 모델이 말하는 자리에서 벗어난 밀리미터마다 그것을 힘으로 바꾼다 — §6이 센티미터당 100 N으로 값을 매긴다. 그래서 접촉 과제는 무엇을 조절할지 골라야 한다. 자세인가, 힘인가, 둘 사이의 관계인가. 그 선택을 네 모드가 나눠 맡는다.

| 모드 | 조절 대상 |
|---|---|
| 위치 제어 | 자세 또는 궤적 오차 |
| 힘 제어 | 측정된 접촉력 |
| 임피던스 제어 | 운동 오차 → 힘의 원하는 관계 |
| 어드미턴스 제어 | 측정 힘 → 운동 응답의 원하는 관계 |

임피던스는 단순히 "위치와 힘을 동시에 제어"하는 것이 아니다. 상호작용 거동을 — 대개 가상 질량-스프링-댐퍼로 — *형성*한다. 풀어 쓰면 제어기가 명령하는 것은 기준점에 매단 스프링과 댐퍼이고, 관성 항은 대부분의 구현처럼 뺐다. 그래서 만들어지는 힘은 변위와 속도만으로 정해진다:

$$F = K_d(x_d - x) + D_d(\dot x_d - \dot x)$$

이고, $K_d$(강성, N/m)와 $D_d$(감쇠, N·s/m)가 *설계* 변수이며 — 아래 첨자 $d$는 *원하는*(desired)이라는 뜻으로 [[04-robotics/force-compliance-control|13]]과 용어집이 쓰는 대로이고, 환경의 강성은 $K_e$로 따로 둔다 — 실제로 나타나는 힘은 환경이 도구를 $x_d$에서 얼마나 밀어냈는가에 달려 있다. 위치 제어는 $K_d \to \infty$의 극한이고, 힘 제어는 $F$를 직접 조절하며 $x$는 가야 할 곳으로 가게 둔다. 어드미턴스는 강성 높고 정확한 위치 제어 로봇이 측정 힘을 유연한 운동 명령으로 바꿀 때 유용하다. 물리 소자로서의 스프링과 댐퍼, 그리고 가장 무른 요소가 이기게 만드는 직렬 규칙은 [[02-foundations/basic-mechanics|0.6.1 §3–§4]]에 있고, 같은 계수를 제어기의 설계 변수로 — 강성, 그 역수인 **컴플라이언스**, 그리고 감쇠 — 실제 환경 강성의 눈금과 함께 다루는 곳은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §1]]이다.

**네 모드를 제어 법칙으로.** 표의 각 행은 피드백이 무엇에 작용하는지를 다르게 고른 것이다. $x_d$는 기준 자세, $F$는 로봇이 환경에 가하는 힘(그래서 로봇이 받는 힘은 $F_{ext}=-F$), $F_d$는 원하는 힘, $F_m$은 측정 힘이다.

- **위치 제어**는 자세 오차만 되먹이고 접촉력은 결과로 따라온다: 높은 게인 $K_p,K_v$로 $u=K_p(x_d-x)+K_v(\dot x_d-\dot x)$([[04-robotics/control-theory-ce397|제어 이론 §7]]의 PD 법칙).
- **힘 제어**는 힘 오차를 되먹이고, 흔히 비례-적분 법칙을 쓰며, 위치는 결과로 따라온다: $F=F_d+K_f(F_d-F_m)+K_i\int(F_d-F_m)\,dt$.
- **임피던스 제어**는 위의 스프링-댐퍼, 곧 운동 오차에서 힘으로 가는 사상을 구현한다. 관성 항까지 넣은 전체 목표 동역학은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §2]]에 있다.
- **어드미턴스 제어**는 반대 방향의 사상, 곧 측정 힘에서 운동으로 간다. 가상 동역학을 적분해 운동 기준 $x_c$를 얻고 그것을 내부 위치 루프에 넘긴다.
$$M_d\ddot x_c+D_d\,(\dot x_c-\dot x_d)+K_d\,(x_c-x_d)=F_{ext}$$
  측정 힘이 기준을 움직이므로 로봇은 밀리는 쪽으로 물러나고, $M_d$는 그때 적분하는 가상 질량이다.

> [!example] 계산 예제 · Worked example
> $K_d=200$ N/m, $D_d=20$ N·s/m인 임피던스에서 도구가 기준보다 1 cm 못 미친 채($x_d-x=0.01$ m) 정지해 있으면 $F=200\times0.01=2$ N이다. 대신 도구가 $0.05$ m/s로 밀려나는 중이면($\dot x_d-\dot x=0.05$) 댐퍼가 $20\times0.05=1$ N을 더해 $F=3$ N이 된다. **비예**: 뻣뻣한 PD 위치 루프도 형식상 $K_d=K_p$인 임피던스지만, $K_p=10^5$ N/m에서 같은 1 cm가 1000 N을 요구하므로 "유연하다"고 부르면 틀린다. 유연함을 정하는 것은 법칙의 구조가 아니라 숫자다.

### 6. 시나리오: 벽 닦기

순수 위치 제어기가 도구를 추정 벽면보다 2 cm 안쪽으로 명령한다. 접촉 강성이 높아 벽 위치의 1 cm 오차가 완전히 다른 힘을 만들 수 있다. **숫자로 보면**: *유연하게 장착된* 도구가 벽에 $K_e = 10^4$ N/m로 닿으면 — 환경의 강성이고, 아래 첨자 $e$는 13의 것이다 — 1 cm 위치 오차가 $10^4 \times 0.01 = 100$ N이 된다. 표면을 파거나 힘 제한을 걸기에 충분하고, 3 cm 오차라면 팔이 낼 수조차 없을 300 N을 요구한다. 이 강성은 의도적으로 무른 쪽을 고른 값이다. 실제 팔에 단 맨 도구가 강철에 닿으면 최대 한 자릿수쯤 더 단단하고 — 도구·센서·팔·부재의 직렬 강성으로 약 $10^5$ N/m — 그때는 같은 1 cm 오차가 약 $10^3$ N을 요구해서 오차가 닫히기 한참 전에 힘이 발산한다. $10^7$ N/m의 재료 강성에 다가가는 것은 강체 지그 위의 맨 압자뿐이고, 강성 눈금은 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §1]]에 표로 있다. 계속 쓰는 대상의 패널은 $k_w=400$ N/m(이 표기로는 그 패널의 $K_e$)로 이 눈금 전체보다 아래에 있고, 그래서 5 mm 누름이 2 N밖에 들지 않는다.

이제 §5의 나머지 세 모드를 같은 1 cm 오차에 대 보자. **임피던스**: 대신 제어기의 강성을 $K_d = 200$ N/m로 두면 같은 오차가 요구하는 힘은 약 2 N이다. 가상 스프링과 벽이 직렬로 작용하므로 정확히는 $1/(1/200+1/10^4)=196$ N/m에서 $1.96$ N이다. 접촉 작업을 유연하게 돌리는 이유는 어떤 제어 이론이 아니라 이 비율이다. **어드미턴스**는 같은 힘에 반대쪽에서 닿는다. 뻣뻣한 위치 루프는 그대로 두고, 손목 센서가 벽의 밀기를 재고, 어드미턴스 법칙이 $K_d(x_d-x_c)$가 그것과 맞을 때까지 기준을 물린다. 그래서 같은 $K_d=200$ N/m에서 도구가 벽 안으로 $0.2$ mm 들어간 채 같은 $1.96$ N에 자리 잡는다. 다만 힘을 재고 안쪽 위치 루프가 따라가는 만큼만 빠르게 물러설 수 있으므로, 착지의 처음 몇 밀리초는 여전히 뻣뻣한 팔이 받는다. 그 안에 1 kHz 샘플이 몇 개나 들어가는지는 [[04-robotics/force-compliance-control|13. §5]]가 센다. **힘 제어**는 법선력을 직접 조절해 벽이 어디에 있든 2 N을 내지만, 접선 운동과 안정성 처리가 따로 필요하다. 최선의 구조는 액추에이터 대역폭, 센싱, 표면 변동, 안전 한계에 달려 있다.

### 7. 힘, 촉각, 재료 상태

'대상으로 한 번 끝까지'는 아무도 관측하지 않은 $\mu$에서, 그리고 §1의 어느 방정식이 성립할지를 정하는 접촉의 모드 — 떨어짐, 고착, 미끄럼 — 에서 끝났다. 이 절은 센싱이 그 상태에 대해 무엇을 알려 줄 수 있는지를 다루고, 모든 접촉 제어기가 받아 쓰는 추정 하나로 끝난다.

- 손목 힘/토크 센서는 합성 렌치를 재지만 전체 압력 분포는 못 잰다.
- 촉각 어레이는 접촉 위치, 압력, 전단, 미끄럼 신호를 추정할 수 있다. *초기 미끄러짐*, 곧 물체가 움직이기 전에 접촉 패치의 가장자리가 미끄러지고 가운데는 아직 고착한 상태도 여기에 든다([[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱 §3]]).
- **고유수용감각**(proprioception)은 로봇 자신의 상태를 잰다(각도·속도를 재는 관절 엔코더, 토크를 재는 모터 전류, 몸통 자세·가속도를 재는 관성 측정 장치(IMU)). **외수용감각**(exteroception)은 로봇 바깥 세계를 잰다(카메라, 라이다, 깊이 센서). 손목 F/T 센서와 촉각 피부는 그 사이에 있다. 로봇 위에 달려 있지만 보고하는 것은 외부 접촉이다.
- 비전은 전역 기하를 보고, 촉각은 국소 접촉의 모호성을 푼다. [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱 §1]]의 논증이고, 그 절이 숫자를 붙인다. 접선 하중이 마찰 경계의 절반일 때 손끝 접촉 패치의 $37\%$가 이미 미끄러지는데 물체는 $0$ mm 움직였으므로, 어떤 카메라도 그것을 볼 수 없다.

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
> **예.** 계속 쓰는 대상의 숫자가 세 모드를 가른다. $f_n\approx0$ N이면 *떨어짐*. $f_n=2$ N에 $\lVert f_t\rVert=1$ N이고 접선 운동이 없으면 *고착*. 같은 2 N인데 도구가 움직이면서 $\lVert f_t\rVert$가 $\mu f_n=1$ N 경계에 붙어 있으면 *미끄럼*이다. 뒤 두 경우는 힘의 크기가 똑같고, 운동 또는 $f_t$가 더 오르기를 멈췄다는 사실만이 둘을 가른다.
>
> **비예.** "궤적이 도구를 패널 안 5 mm로 보내라고 했으니 접촉 중이다"는 추정이 아니라 명령에 이름표만 바꿔 붙인 것이고, 패널이 잘못된 자리에 있어 접촉이 없음이 보장되는 바로 그 순간에 접촉이라고 보고한다. 맨 힘 임계값도 경계 하나의 *검출기*이지 모드 집합 위의 추정기가 아니다. 미끄럼을 보고하지 못한다.
>
> **왜 중요한가.** [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]]의 모든 제어기가 모드마다 다른 방정식 묶음이다. 그 §3의 선택 행렬은 접촉이 어느 방향을 막는지 알아야 하고, 그 §5의 충격 논증은 모드가 바뀐 뒤에야 시작된다. 어떤 시스템이 "접촉을 다룬다"는 주장은, 논문이 그 이름을 쓰든 안 쓰든, 이 추정에 관한 주장이다.

계속 쓰는 대상 자신의 접촉을 세 모드 모두로 따라가 보면, 정의가 샘플 하나가 아니라 창을 필요로 하는 이유가 보인다.

<svg viewBox="0 0 560 350" style="max-width:100%;height:auto" role="img" aria-label="계속 쓰는 대상의 시간 궤적: 법선력은 0.10 s에 처음 닿으며 0.08 N으로 뛰고, 다가오는 동안 2.08 N까지 올랐다가 0.35 s부터 2.00 N에 머문다; 접선력은 요구 경사를 따라 1.0 s에 1.00 N 경계에 닿고 1.3 s까지 거기서 고착하며, 요구가 2 N으로 오르는 동안 1.00 N에 고정된 채 도구가 미끄러진다; 미끄럼 속도는 1.3 s까지 0이다; 모드 띠는 떨어짐, 닿아서 고착, 닿아서 미끄럼; 창 w 두 개가 같은 1 N 힘의 고착과 미끄럼을 보인다; 아래에는 패널이 2 mm 멀리 있을 때 명령 기반 접촉 표시가 측정 힘보다 0.1 s 먼저 켜진다">
  <defs><marker id="cstAk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor">
    <text x="12" y="18" font-size="12" font-weight="600" fill-opacity="0.85">접촉 하나, 모드 셋: 계속 쓰는 대상의 궤적</text>
    <rect x="118.2" y="30.0" width="266.4" height="202.0" fill="currentColor" fill-opacity="0.05"/>
    <rect x="384.6" y="30.0" width="155.4" height="202.0" fill="currentColor" fill-opacity="0.13"/>
    <line x1="118.2" y1="30.0" x2="118.2" y2="254.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" stroke-dasharray="3 3"/>
    <line x1="384.6" y1="30.0" x2="384.6" y2="254.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" stroke-dasharray="3 3"/>
    <line x1="96.0" y1="92.0" x2="540.0" y2="92.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="96.0" y1="92.0" x2="96.0" y2="34.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="92.0" y1="67.0" x2="96.0" y2="67.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="70.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">1</text>
    <line x1="92.0" y1="42.0" x2="96.0" y2="42.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="45.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">2</text>
    <text x="89.0" y="95.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">0</text>
    <text x="12" y="62.0" font-size="11" xml:space="preserve">f<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> (N)</tspan></text>
    <line x1="96.0" y1="170.0" x2="540.0" y2="170.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="96.0" y1="170.0" x2="96.0" y2="112.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="92.0" y1="145.0" x2="96.0" y2="145.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="148.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">1</text>
    <line x1="92.0" y1="120.0" x2="96.0" y2="120.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="123.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">2</text>
    <text x="89.0" y="173.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">0</text>
    <text x="12" y="140.0" font-size="11" xml:space="preserve">‖f<tspan dy="3.1" font-size="11">t</tspan><tspan dy="-3.1">‖ (N)</tspan></text>
    <line x1="96.0" y1="226.0" x2="540.0" y2="226.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <line x1="96.0" y1="226.0" x2="96.0" y2="186.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="89.0" y="229.5" font-size="10.5" text-anchor="end" fill-opacity="0.85">0</text>
    <text x="12" y="204.0" font-size="11" xml:space="preserve">‖v<tspan dy="3.1" font-size="11">t</tspan><tspan dy="-3.1">‖</tspan></text>
    <text x="12" y="217.0" font-size="10.5" fill-opacity="0.8">(모양만)</text>
    <path d="M 96.0 92.0 L 118.2 92.0 L 118.2 90.0 L 173.7 40.0 L 173.7 42.0 L 540.0 42.0" fill="none" stroke="currentColor" stroke-width="2"/>
    <text x="124.2" y="105.0" font-size="10.5" fill-opacity="0.85">처음 닿을 때 댐퍼의 0.08 N 계단</text>
    <text x="181.7" y="37.0" font-size="10.5" fill-opacity="0.85">다가오는 동안 2.08 N, 정지하면 2.00 N</text>
    <line x1="173.7" y1="145.0" x2="540.0" y2="145.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" stroke-dasharray="1.5 2.5"/>
    <text x="211.4" y="141.0" font-size="10.5" fill-opacity="0.85" xml:space="preserve">μf<tspan dy="3.1" font-size="10.5">n</tspan><tspan dy="-3.1"> = 1.00 N</tspan></text>
    <path d="M 207.0 170.0 L 318.0 145.0 L 384.6 145.0 L 495.6 120.0 L 540.0 120.0" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="5 3"/>
    <text x="491.6" y="115.0" font-size="10.5" text-anchor="end" fill-opacity="0.85">요구</text>
    <path d="M 96.0 170.0 L 207.0 170.0 L 318.0 145.0 L 540.0 145.0" fill="none" stroke="currentColor" stroke-width="2"/>
    <text x="457.9" y="159.0" font-size="10.5" fill-opacity="0.85">1.00 N에 고정</text>
    <path d="M 96.0 226.0 L 384.6 226.0 L 385.7 222.9 L 386.8 220.2 L 387.9 217.8 L 389.0 215.7 L 390.1 213.8 L 391.3 212.2 L 392.4 210.7 L 393.5 209.5 L 394.6 208.3 L 395.7 207.3 L 396.8 206.4 L 397.9 205.7 L 399.0 205.0 L 400.1 204.4 L 401.2 203.8 L 402.4 203.4 L 403.5 202.9 L 404.6 202.6 L 405.7 202.3 L 406.8 202.0 L 407.9 201.7 L 409.0 201.5 L 410.1 201.3 L 411.2 201.1 L 412.4 201.0 L 413.5 200.8 L 414.6 200.7 L 415.7 200.6 L 416.8 200.5 L 417.9 200.4 L 419.0 200.4 L 420.1 200.3 L 421.2 200.2 L 422.3 200.2 L 423.5 200.2 L 424.6 200.1 L 425.7 200.1 L 426.8 200.1 L 427.9 200.0 L 429.0 200.0 L 540.0 200.0" fill="none" stroke="currentColor" stroke-width="2"/>
    <rect x="329.1" y="135.0" width="44.4" height="95.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="2 2"/>
    <text x="369.5" y="221.0" font-size="10.5" text-anchor="end">w</text>
    <rect x="406.8" y="135.0" width="44.4" height="95.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="2 2"/>
    <text x="447.2" y="221.0" font-size="10.5" text-anchor="end">w</text>
    <rect x="96.0" y="236.0" width="22.2" height="16" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <rect x="118.2" y="236.0" width="266.4" height="16" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <rect x="384.6" y="236.0" width="155.4" height="16" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="92.0" y="248.0" font-size="10.5" text-anchor="end">떨어짐</text>
    <text x="251.4" y="248.0" font-size="10.5" text-anchor="middle">닿아서 고착</text>
    <text x="462.3" y="248.0" font-size="10.5" text-anchor="middle">닿아서 미끄럼</text>
    <line x1="96.0" y1="256.0" x2="96.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="96.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">0</text>
    <line x1="207.0" y1="256.0" x2="207.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="207.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">0.5</text>
    <line x1="318.0" y1="256.0" x2="318.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="318.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">1</text>
    <line x1="429.0" y1="256.0" x2="429.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="429.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">1.5</text>
    <line x1="540.0" y1="256.0" x2="540.0" y2="260.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="540.0" y="271.0" font-size="10.5" text-anchor="middle" fill-opacity="0.85">2</text>
    <text x="540.0" y="284.0" font-size="10.5" text-anchor="end" fill-opacity="0.85">시간 (s)</text>
    <text x="12" y="292.0" font-size="10.5" fill-opacity="0.85">패널이 믿은 곳보다 2 mm 멀리 있다면:</text>
    <rect x="118.2" y="300.0" width="177.6" height="9" fill="currentColor" fill-opacity="0.35"/>
    <rect x="140.4" y="316.0" width="155.4" height="9" fill="currentColor" fill-opacity="0.8"/>
    <text x="306.9" y="308.5" font-size="10.5">명령이 “접촉 중”이라 함</text>
    <text x="306.9" y="324.5" font-size="10.5" xml:space="preserve">측정한 f<tspan dy="3.1" font-size="10.5">n</tspan><tspan dy="-3.1"> &gt; 0</tspan></text>
    <line x1="118.2" y1="332.0" x2="140.4" y2="332.0" stroke="currentColor" stroke-width="1"/>
    <path d="M 118.2 328.0 L 118.2 336.0 M 140.4 328.0 L 140.4 336.0" fill="none" stroke="currentColor" stroke-width="1"/>
    <text x="146.8" y="336.0" font-size="10.5" fill-opacity="0.85">거짓 접촉 0.1 s</text>
  </g>
</svg>

계속 쓰는 대상을 누르고 닦은 궤적이다. 도구는 $0.10$ s에 닿고 그때 댐퍼만으로 $0.08$ N의 계단이 생기며, 법선력은 다가오는 동안 $2.08$ N까지 오른 뒤 $0.35$ s부터 $2.00$ N에 머문다. 접선력은 닦기 요구를 따라 $1.0$ s에 $\mu f_n=1.00$ N 경계에 닿고 $1.3$ s까지 거기서 고착하며, 요구가 2 N으로 오르는 동안 $1.00$ N에 고정된 채 도구가 미끄러지고, 모양만 그린 미끄럼 속도 $\lVert v_t\rVert$가 0에서 오른다. 두 창 $w$ 안에서 힘은 똑같이 1 N이고, 고착과 미끄럼을 가르는 것은 운동, 또는 더 오르기를 멈춘 힘에서 요구가 멀어지는 모습뿐이다. 아래는 비예의 명령 기반 표시로, 패널이 믿은 곳보다 2 mm 멀리 있다면 $0.10$ s부터 "접촉 중"이라 하는데, 이는 어떤 힘이 측정되기보다 $0.1$ s 이르다.

로프, 천, 흙, 젖은 콘크리트, 케이블, 벌크 재료는 고차원의 변하는 상태를 갖는다. 이력과 관측 안 되는 재료 성질에 의존해 표현과 예측이 어렵다.

### 8. 학습과 sim-to-real

논문 부록의 무작위화 표가 곧 그 강건성 주장의 범위이고, 이 절은 그 표를 읽는 법이다. 학습이 접촉에 대해 무엇을 추정할 수 있는지, 그리고 무작위화 범위가 무엇을 사 주고 무엇을 사 주지 못하는지.

학습은 잔차 동역학, 접촉 상태, 마찰/재료 성질, 파지 점수, 촉각 조건부 정책을 추정할 수 있다. 도메인 무작위화(domain randomization, [[05-construction-robotics/sim-to-real|건설 7.5 Sim-to-Real §2]]가 목적함수와 함께 정의하고, [[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]]이 쓰이는 모습을 보인다)는 학습 조건을 넓히지만, 선택한 무작위화 분포가 곧 "어떤 변동까지 커버했는가"를 정의한다. 시뮬레이터의 특권 정보(privileged state, [[05-construction-robotics/sim-to-real|건설 7.5 §2]])는 학습을 돕지만 배포 시에는 없다 — 정책이 시험 시점에 그것을 무엇으로 대체하는지 확인하라. 밀기 과제 하나에 셋이 다 들어간다. 잔차 동역학 네트워크는 시뮬레이터가 예측한 다음 상태와 실제 다음 상태의 차이를 배우고, 도메인 무작위화는 에피소드마다 μ와 물체 질량을 새로 뽑으며, 정책은 시뮬레이터의 정확한 물체 자세로 학습하지만 배포 때는 카메라로 추정한 자세만 쓴다.

**계속 쓰는 대상으로 계산: 무작위화 범위가 사 주는 것.** $\mu$를 표의 $0.5$를 가운데 둔 $[0.25,0.75]$에서 균일하게 뽑자. '대상으로 한 번 끝까지'의 $f_n=2.00$ N에서 마찰 경계 $\mu f_n$은 $0.50$에서 $1.50$ N까지 걸치므로, 1 N 닦기는 $\mu\ge0.5$인 정확히 절반의 에피소드에서 고착하고 나머지 절반에서 미끄러진다. 모든 에피소드에서 성공해야 하는 정책은 더 세게 누르는 법을 배운다. $\mu=0.25$에서 1 N을 버티려면 $f_n\ge1/0.25=4.00$ N이 필요하고, 이는 면에서 5 mm가 아니라 $\delta=4.00/400=10$ mm 들어간 것이다. 강건성은 더 센 누름으로 산 것이고, 그것도 범위 안에서만이다. $\mu=0.15$인 젖은 패널은 그 누름에서 $0.15\times4.00=0.60$ N만 버티고, 닦기는 미끄러진다. 접촉 모델에도 같은 함정이 숨어 있다. 페널티 강성이 $400$ N/m인 시뮬레이터(§3)에서 면 너머 5 mm를 명령하도록 배운 정책은 그 시뮬레이터 안에서만 2 N 누름을 배운 것이고, 열 배 단단한 패널에서는 같은 5 mm가 $4000\times0.005=20$ N을 요구한다.

**여기서 얻는 독법.** 배포 환경의 $\mu$, 질량, 접촉 강성이 그 범위 안에 있는지, 그리고 정책이 힘을 내는지 위치 오프셋을 내는지 확인하라. 위치 오프셋은 시뮬레이터가 고른 강성을 거쳐야만 힘이 되기 때문이다. 실제 접촉 강성이 얼마나 넓게 퍼지는지는 [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §1]]에 표로 있다.

### 9. 평가와 논문 표현

성공률 상승만으로는 이득이 촉각 센싱, 더 나은 제어, 안전한 힘 한계, 쉬운 접촉 조건 중 어디서 왔는지 알 수 없다. 그래서 접촉 논문은 그것을 추적할 수 있을 만큼 보고해야 한다. 센싱·제어기·재료·초기화에 걸친 짝지은 베이스라인과 절제 실험, 그리고 비교할 수 있을 만큼 정의한 힘 지표다.

과제 성공, 최대/평균 힘, 힘 추종 오차, 미끄럼/낙하율, 물체·표면 손상, 회복, 안전 위반, 재료·마찰에 걸친 강건성을 재라. "Contact-rich", "compliant", "robust"는 명시적 과제·교란 정의를 요구하는 주장이다.

**네 가지 힘 지표의 정의.** 각각 종류가 다른 수이고, 각각 자기 방식으로 실패한다.

- **최대 접촉력** $F_{\max}=\max_t\lVert f(t)\rVert$, 접촉 구간 전체에 대해, 단위는 뉴턴. *표본으로 잡은* 최댓값이라 센서 속도만큼만 참이다. 1 kHz 채널이 1.4 ms 충격을 보면 사건 안에 샘플이 한 개쯤 들어가므로([[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §5]]) 보고된 최댓값이 실제보다 한참 낮을 수 있다. 같은 구간의 **평균 힘**이 짝인 수이고, 평균만 보고하면 최댓값이 존재하는 이유를 정확히 가린다.
- **힘 추종 오차**, 접촉 구간 $[0,T]$에서 명령한 법선력과 측정한 법선력 차이의 제곱평균제곱근, 단위는 뉴턴:

$$e_{\mathrm{RMS}}=\sqrt{\frac{1}{T}\int_0^T\big(f_d(t)-f_m(t)\big)^2\,dt}$$

  $f_d$는 명령한 힘, $f_m$은 측정한 힘, $T$는 접촉의 길이다 — 시행의 길이가 아니다. 시행 전체로 바꿔 넣으면 자유 공간의 몇 초가 평균에 섞여 제어기를 좋아 보이게 만든다. 계속 쓰는 대상의 예: 명령 $f_d=2$ N을 $2.0,\ 2.3,\ 1.8,\ 2.1$ N으로 측정하면 오차가 $0,\ -0.3,\ 0.2,\ -0.1$ N이므로 $e_{\mathrm{RMS}}=\sqrt{0.035}=0.187$ N, 목표의 $9.4\%$다. 평균 절대 오차는 $0.150$ N밖에 되지 않는다. RMS가 0.3 N짜리 한 번의 튐에 더 무겁게 값을 매기고, 힘 한계를 두고 이야기할 때 정직한 쪽이 그래서 RMS다.
- **미끄럼률**과 **낙하율**: 제어기가 고착을 명령한 동안 접선 운동이 일어난 접촉 시간의 비율, 그리고 목표에 닿기 전에 물체가 손을 떠난 파지 시행의 비율. 둘 다 비율이므로 시행 수를 옆에 적지 않으면 뜻이 없고, 둘 다 *명령한* 의도를 기준으로 재므로 §7의 접촉 상태 추정을 전제한다.

**비예.** 센서 속도 없는 최대 힘, 시행 전체로 잰 RMS 오차, $n$ 없는 미끄럼률은 남의 숫자와 비교할 수 없는 수를 보고하는 세 가지 서로 다른 방법이다.

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
2. $\mu=0.6$에서 3 N의 접선 요구가 4 N의 법선력을 만난다. 단순 원뿔은 고착을 허용하는가? 같은 요구가 $\mu=0.48$에서는 법선력이 얼마나 필요한가?
3. 인식이 완벽해도 한 마찰 계수로 학습한 정책이 실패할 수 있는 이유는?
4. 촉각 정책의 절제 실험에서 무엇을 고정해야 하는가?
5. 어떤 계획기가 자기 파지에 마찰 여유가 남는다고 보고한다. 접촉마다 외접 상자 피라미드로 제약했다. 그 여유는 어느 쪽으로 틀렸고, 모서리에서 얼마나 틀렸는가?
6. 명령한 자세가 표면보다 안쪽이면 언제나 "접촉 중"이라고 기록하는 시스템이 있다. 접촉 상태 추정의 두 정의 조건 중 무엇을 어기며, 가장 나쁜 순간에 무엇이라고 보고하는가?

> [!tip]- 정답 · Answers
> 1. 작은 자세·모델 오차가 큰 힘과 불안정을 만들 수 있다.
> 2. 아니다: $3>0.6\times4=2.4$ N이므로 접촉은 미끄러진다. $\mu=0.48$에서는 $f_n\ge3/0.48=6.25$ N이 필요하다.
> 3. 실행 가능한 힘, 미끄럼 전이, 동역학이 달라진다.
> 4. 시연, 모델 용량, 제어기, 초기화, 재료, 평가 프로토콜 — 나머지를 쉽게 만들지 않으면서 촉각 정보만 제거·대체해야 한다.
> 5. 낙관적인 쪽으로 틀렸다. 상자 피라미드는 참 원뿔을 포함하므로 미끄러질 접선력까지 허가하고, 모서리에서는 참 경계의 $\sqrt2$배, 곧 $41.4\%$ 후하다. 내접 다면 원뿔은 반대쪽으로 틀려 여유를 과소평가했을 것이다.
> 6. (ii)번, 곧 추정이 명령이 아니라 측정에서 나와야 한다는 조건이다. 패널이 잘못된 자리에 있어 접촉이 없음이 보장되는 바로 그 순간에 접촉이라고 보고한다 — 그 추정이 존재하는 이유였던 경우다.

### 과제 · Problem set

Tier B. 계속 쓰는 대상에서 **항목 두 개만 바꾼다**. 명령 침투량이 $\delta=8\,\mathrm{mm}$가 되고, 패널의 먼지가 마찰 계수를 $\mu=0.35$로 떨어뜨린다. 나머지 — $\theta=(0^\circ,90^\circ)$의 **P2**, $x=1\,\mathrm{m}$의 패널, $k_w=400\,\mathrm{N/m}$, $m_p=1.0\,\mathrm{kg}$, $\pm0.05\,\mathrm{m}$에서의 $f_g=10\,\mathrm N$ 두 손가락 조임 — 은 그대로다([[02-foundations/lab-plants|0.6]]). 이 페이지와 선수 지식, 객체 카탈로그만 쓴다. 시뮬레이터 없음.

1. **그리기.** 위의 그림의 세 패널을 모두 새 숫자로 다시 그린다. 오른쪽 패널의 닫힌 곡선 셋은 이제 새 $f_n$에서 $\mu=0.35$로 그려야 하고, 1 N 닦기 화살표도 같은 축척으로 그려야 한다 — 셋 중 어느 집합이 그것을 품는지를 그림이 보여 주어야 한다.
2. **유도.** (a) $\delta=8\,\mathrm{mm}$에서 정지 상태의 $f_n$. (b) 원뿔 반각과 고착할 수 있는 최대 접선력. (c) $1\,\mathrm{N}$ 닦기는 아직 고착하는가, 여유는 얼마인가? (d) 4-생성자 내접 원뿔의 유효 계수와 *그것이* 허가하는 최대 닦기. (e) 이제 두 손가락에 필요한 조임 $f_g$와, 바꾸지 않은 10 N 조임이 버티는 힘.
3. **해석.** 여기서 가능한 실패는 둘 — 닦기의 미끄럼과 패널의 낙하 — 인데 하나만 일어났다. 어느 쪽이고, 같은 $30\%$의 $\mu$ 손실이 왜 두 경계를 반대 방향으로 움직였는가? 패널이 바닥에 닿기 전에 알려 주었을 측정 하나를 이름 붙이고, 이 페이지의 어느 절이 그것을 정의하는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - **왼쪽, $x$–$y$ 평면의 팔, 실제 비율**: 원점에 P2 베이스, 링크 1이 $+x$로 뻗어 엘보가 $(1,0)$, 링크 2가 올라가 말단이 $(1,1)$. 패널 면 $x=1$은 그 평면 뒤로 물러서 — 오른쪽 위로 비껴 기운 직사각형으로 — 그려 전완 위에 놓이지 않게 하고, L자 도구가 말단에서 면 앞쪽으로 비켜 뒤로 뻗어 짧은 발로 $\hat n$ 방향으로 면을 누르게 한다.
> - **도구가 면에 닿는 자리의 접촉 프레임**: $\hat n$은 $+x$로 면 안쪽, $\hat t_1$은 $-y$로 면을 따라 닦는 방향.
> - **떼어 그린 접촉력**: 도구가 패널을 미는 $f$는 면에서 끝나는 화살표 하나로, 패널이 도구를 되미는 $-f$는 그 옆에 반대로 향한 두 번째 화살표로.
> - **도구 끝과 면 사이의 작은 스프링**: $k_w$를 적고 명령한 $\delta$만큼 눌린 모습으로 그리되, 비율보다 훨씬 크게 그리고 그렇게 그렸다고 적어 둔다. 1 m짜리 팔에서 몇 밀리미터는 눈에 보이지 않는다.
> - **오른쪽, 접촉 프레임 안의 원뿔**: 법선 축 $\hat n$을 세로로, 접선 평면 $(\hat t_1,\hat t_2)$을 가로로 두되, 프레임이 오른손 좌표계로 남도록 $\hat t_2$는 지면 안쪽으로 들어가게 그린다. 위로 열린 원형 원뿔의 반각 $\arctan\mu$를 각으로 표시한다.
> - **접선 평면 위의 닫힌 곡선 셋, 누름이 만드는 $f_n$에서 동심으로**: 반지름 $\mu f_n$인 참 원, 그 바깥으로 네 점에서 원에 접하는 외접 상자 피라미드의 정사각형, 그 안쪽으로 네 꼭짓점이 원 *위에* 놓이는 4-생성자 내접 원뿔의 정사각형.
> - **명령한 닦기 힘은 같은 축척, 실제 길이의 화살표 하나로**: 셋 중 어느 집합이 그것을 품는지 그림이 보여 주어야 한다.
> - **아래, 간극 축**: $\phi$에 대한 수평선을 긋고 0을 표시한다. 0의 왼쪽 반직선($\phi>0$, 떨어짐)에는 $f_n=0$, $\phi=0$의 세로 반직선에는 $f_n\ge0$이라고 적고, 점 둘을 찍는다. 닿기 전에 하나, 그리고 §3의 페널티 모델은 허용하고 §1의 강체 모델은 금지하는 명령 침투에 하나.
> - **쌍 $(\phi,f_n)$은 결코 두 반직선을 벗어나지 못한다** — 그 그림이 곧 complementarity다.

> [!tip]- 정답 · Solutions
> 1. 왼쪽에서는 힘의 쌍이 이제 패널에 걸리는 $f=(3.20,-1.00)\,\mathrm N$과 도구에 걸리는 $-f$이고, 그것을 유지하는 데 $\tau=J^\top f=(-4.20,-3.20)\,\mathrm{N{\cdot}m}$가 든다. 스프링은 $8\,\mathrm{mm}$ 눌린다. 오른쪽에서는 원뿔이 더 좁아지지만($26.6^\circ$ 대신 $19.3^\circ$) 접선 평면 위의 원은 *더 커진다*. $\mu$가 떨어진 것보다 $f_n$이 더 빨리 올랐기 때문이다. 4-생성자 정사각형의 꼭짓점은 여전히 원 위에 있고, 상자 피라미드의 정사각형은 여전히 원에 외접한다. 1 N 닦기는 이제 $1.12\,\mathrm N$ 원 안에서 끝나지만, 평평한 변이 $0.792\,\mathrm N$인 내접 정사각형 밖에 여전히 있다. 아래에서는 침투 점이 같은 $0.4\,\mathrm{N/mm}$ 페널티 선 위의 $-8\,\mathrm{mm}$, $3.20\,\mathrm N$으로 옮겨 간다.
> 2. (a) 정지 상태 $f_n=400\times0.008=3.20\,\mathrm{N}$. 아직 다가오는 동안에만 $d_c\dot\delta$를 더한다. (b) $\arctan0.35=19.29^\circ$, 그리고 $\lVert f_t\rVert\le0.35\times3.20=1.12\,\mathrm{N}$. (c) 고착한다. $1.00<1.12$이고 여유는 $0.12\,\mathrm{N}$이라 경계의 $89.3\%$를 쓴다 — 경계 위에 정확히 있던 것에서 경계 안쪽으로 들어왔다. 더 깊이 누른 것이 먼지가 빼앗은 것보다 더 많은 마찰을 샀기 때문이다. (d) $\mu\cos(\pi/4)=0.35\times0.7071=0.2475$이므로 $0.2475\times3.20=0.792\,\mathrm{N}$까지만 허용한다. 보수적인 모델이 실제 접촉이 버티는 바로 그 닦기를 *거절*한다. (e) $f_g\ge m_pg/(2\mu)=9.81/0.70=14.01\,\mathrm{N}$이 필요한데, 바꾸지 않은 10 N 조임은 $2\times0.35\times10=7.00\,\mathrm{N}$을 버틴다 — 패널 무게 $9.81\,\mathrm{N}$보다 $2.81\,\mathrm{N}$ 모자란다.
> 3. 패널이 떨어지고 닦기는 멀쩡하다. 두 경계 모두 $\mu f_n$이고 $\mu$의 같은 $30\%$를 잃었지만, 닦기 쪽은 명령이 법선력을 $2.00$에서 $3.20\,\mathrm{N}$으로 올려 주었다 — $1.6\times0.7=1.12$로 먼지를 갚고도 남는 $60\%$의 이득이다 — 반면 파지 쪽의 법선력은 조임이 정하고 있어 그런 보상이 없었다, $1.0\times0.7=0.70$. 교훈은 마찰 여유가 *곱* $\mu f_n$에 대한 여유이고, 둘 중 더 세게 누른 쪽은 하나뿐이었다는 것이다. 이것을 잡았을 측정은 접촉 상태 추정(§7)이다. 제어기가 고착을 명령한 동안 손가락이 미끄러지는 것은 모드 변화이고, 접선력이 경계에 붙어 버린 데서 보이며, 패널이 손을 떠나기 전에 일어난다. 패널의 자세를 보는 카메라는 이미 떨어지기 시작할 때까지 아무것도 보지 못한다 — [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱 §1]]의 논증이다. 촉각 손가락이라면 패치 가장자리의 초기 미끄러짐으로 더 일찍 경고할 수 있다([[04-robotics/tactile-visuotactile|14. §3]]).

### 출처

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation (Tedrake) — 힘 제어·접촉 관련 장](https://manipulation.csail.mit.edu/)
- [Modern Robotics 코스 위키 — 12장 영상·소프트웨어](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)
