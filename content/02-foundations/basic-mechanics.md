---
title: "0.6.1 Basic Mechanics: Forces, Springs, Damping and Energy"
tags: [foundations, physics, mechanics]
study-depth: Working
depth-goal: "On P3's handle pushed into its wall and on P2 at its catalog pose, draw the free-body diagram, write the equation of motion, and compute the natural frequency, damping ratio, time constant, overshoot, settling time and energy ledger, and the torques, moments of inertia and holding torques, with every unit checked."
mastery-when: "Raise only if mechanical modelling itself — a new actuator, contact model or mechanism — becomes the contribution; the robotics pages above this one carry the depth."
wiki-support: Working
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 Engineering Math]] — derivatives (§1), exponentials (§6), complex numbers (§7) and linear ODEs up to the second-order one (§8), used here without being re-taught · plants **P3** and **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled).
> [[02-foundations/engineering-math|0.5 공업수학]] — 미분(§1), 지수(§6), 복소수(§7), 2차까지의 선형 미분방정식(§8). 여기서는 다시 가르치지 않고 쓴다 · [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3**와 **P2**.

## English

*Stands on [[02-foundations/engineering-math|0.5 Engineering Math]] for the derivative, the exponential, complex roots and the second-order equation, and on [[02-foundations/lab-plants|0.6 Lab Plants]] for its two plants. The first page that opens **P3** and **P2** as physics rather than as numbers: P3's handle for force, springs, damping, oscillation and energy, P2's arm for torque, inertia and the holding torque. Control, force control, haptic rendering and actuators all write these same equations with more on top.*

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] — perception, object and scene understanding, grasping, motion and task planning, manipulation, contact, force and tactile feedback, learning and adaptation, task completion — this page is the physical floor under the contact-and-force and actuation layers: in *"Install that panel on the frame"* it is the moment the panel's hole meets the pin and the arm must be soft (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it a contact's numbers mislead: a panel meant to be pressed with $10\,\mathrm N$ takes a $22.4\,\mathrm N$ hit when the tool arrives at $5\,\mathrm{cm/s}$ ([[04-robotics/force-compliance-control|13. §5]]), and P3's handle pushed with $0.4\,\mathrm N$ strikes its wall with $0.692\,\mathrm N$, and a statics answer shows neither. The natural frequency, damping ratio, energy ledger and gear trade taught here are the working language of [[04-robotics/control-theory-ce397|5. Control Theory §5]], [[04-robotics/actuators-drives|10.5 §4]], [[04-robotics/force-compliance-control|13. §2]] and [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]], and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) the page sits in block 1, the foundations floor, taken where a civil-engineering degree left dynamics out. After it you can write a contact's equation of motion from a free-body diagram and read off whether it rings, how hard it hits and how long it takes to settle.

> [!note] First pass · 처음이라면
> Two sessions of about ninety minutes each. **Session 1, the handle:** the Running object and the picture, then §1–§5 in order, which build one situation — P3's handle pushed into its wall — a law at a time: units, the free-body diagram, the spring, the damper and friction, the mass–spring–damper. Slow down in §5 if *damping ratio* or *time constant* is new, and end the session by computing $\omega_n$, $\zeta$ and $\tau$ for the bare handle yourself and checking them against §5. **Session 2, energy and rotation:** §6 and the Worked case after it, which puts §1–§6 on one set of numbers; then §7–§9 on P2 (§8 is a quick read if statics is familiar); run the lab of §10 and answer the Self-check before opening the answers. The collapsed *Deeper* notes can wait for a second reading; §11 says where the page stops.

### Running object · 이 페이지의 대상

**P3** and **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], at the numbers the catalog freezes; this page changes none of them. P3's handle carries the translation half of the page — force, springs, damping, oscillation, energy — and P2's arm the rotation half: torque, moment of inertia, the holding torque, gears.

| Symbol | Value | What it is, and where this page uses it |
|---|---:|---|
| $m$ | $0.04\,\mathrm{kg}$ | P3's effective mass at the handle (§2) |
| $b$ | $0.8\,\mathrm{N{\cdot}s/m}$ | P3's physical viscous damping (§4) |
| $k_w$, $x_w$ | $400\,\mathrm{N/m}$, $0.030\,\mathrm{m}$ | P3's virtual wall and where it starts; $+x$ is into the wall (§3) |
| $k_h$, $b_h$ | $400\,\mathrm{N/m}$, $8\,\mathrm{N{\cdot}s/m}$ | the hand's stiffness and damping when it grips the handle (§3, §5) |
| $r_m$, $r_s$ | $0.010$, $0.050\,\mathrm{m}$ | P3's capstan: motor pulley and sector radii (§9) |
| $L_1=L_2$, $m_1=m_2$ | $1\,\mathrm{m}$, $1\,\mathrm{kg}$ | P2's unit links, and its point masses at the elbow and the tip (§7) |
| $\theta$, $g$ | $(0^\circ,90^\circ)$, $9.81\,\mathrm{m/s^2}$ along $-y$ | P2's catalog pose, elbow at $(1,0)$ and tip at $(1,1)\,\mathrm{m}$ (§7, §8) |
| $n$ | $100$ | the gear ratio of each of P2's joint drives, frozen on [[04-robotics/actuators-drives\|10.5]] (§9) |

Three numbers this page adds and freezes. They are this page's own course numbers, chosen to make the arithmetic visible, not measurements of any device:

| Symbol | Value | What it is |
|---|---:|---|
| $F$ | $0.4\,\mathrm{N}$ | a steady push on the handle, into the wall, starting at $t=0$ with the handle at rest on the wall's surface — the force the catalog wall returns at $1\,\mathrm{mm}$ |
| $f_c$ | $0.02\,\mathrm{N}$ | sliding (Coulomb) friction in the handle's guide; used only in §4 |
| $f_s$ | $0.05\,\mathrm{N}$ | breakaway (static) friction in the same guide; used only in §4 |

Two modelling choices, stated once. P3's catalog model has no gravity term along its axis — [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] writes it $m\ddot x+b\dot x=F_h+F_a$ — so this page takes the axis to be horizontal, with the handle's weight and the guide's reaction cancelling across it; the depth $y=x-x_w$ measures how far the handle is inside the wall. P2 stands in a vertical plane, as on [[02-foundations/manipulator-kinematics-dynamics|10]] and 10.5, and wherever it is treated as one body turning about the shoulder, its elbow is locked at $90^\circ$.

*Scope: this page teaches the mechanics a robotics researcher uses daily — SI units and dimensional checks, Newton's laws and the free-body diagram, springs in series, in parallel and with preload, real parts as springs, viscous damping and Coulomb friction, the mass–spring–damper with its natural frequency, damping ratio and time constant, work, energy and power, torque, moment of inertia and angular momentum, statics and the holding torque, and levers and gears — on P3 and P2. It does not teach the response numbers and frequency response of feedback systems ([[04-robotics/control-theory-ce397|5. Control Theory]]), the dynamics of a multi-joint arm ([[02-foundations/manipulator-kinematics-dynamics|10]]), motors and gearbox losses ([[04-robotics/actuators-drives|10.5]]), rendered impedance and contact ([[04-robotics/force-compliance-control|13]]) or the sampled virtual wall ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]); §11 lists what else is left out.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 376" style="max-width:100%;height:auto" role="img" aria-label="P3's handle pushed into its virtual wall by a steady 0.4 N. Top left, the model: the 0.04 kg handle with the 400 N/m wall spring and the 0.8 N·s/m device damper. Top right, its free-body diagram at the first peak: 0.4 N in, 0.692 N back, no damper force, net −0.2917 N. Bottom, the depth y against time: the bare handle rings up to 1.729 mm at 31.6 ms inside a 100 ms envelope and settles at 384 ms; gripped by the hand it overshoots 2.0 percent and settles at 37 ms.">
  <defs><marker id="bmA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18">P3’s handle pushed into its virtual wall by a steady F = 0.4 N</text>
    <text x="12" y="40" opacity="0.85">the model: handle, wall spring and damper</text>
    <text x="286" y="40" opacity="0.85">free body at the first peak, t = 31.6 ms</text>
  </g>
  <polyline points="16,84 66,84" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#bmA)"/>
  <rect x="68" y="60" width="56" height="48" rx="2" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="124,72 138,72 142.5,65 151.5,79 160.5,65 169.5,79 178.5,65 187.5,79 196.5,65 205.5,79 210,72 224,72" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <line x1="124" y1="98" x2="176" y2="98"/><line x1="176" y1="91" x2="176" y2="105"/>
    <polyline points="164,88 196,88 196,108 164,108"/><line x1="196" y1="98" x2="224" y2="98"/>
    <line x1="224" y1="62" x2="224" y2="112"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="224" y1="64" x2="232" y2="58"/><line x1="224" y1="72" x2="232" y2="66"/><line x1="224" y1="80" x2="232" y2="74"/><line x1="224" y1="88" x2="232" y2="82"/><line x1="224" y1="96" x2="232" y2="90"/><line x1="224" y1="104" x2="232" y2="98"/></g>
  <polyline points="68,140 112,140" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#bmA)"/>
  <g font-size="11" fill="currentColor">
    <text x="18" y="76">F = 0.4 N</text>
    <text x="96" y="81" text-anchor="middle">m</text>
    <text x="96" y="97" text-anchor="middle" font-size="10.5">0.04 kg</text>
    <text x="150" y="56" text-anchor="middle">wall spring k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> = 400 N/m</tspan></text>
    <text x="160" y="126" text-anchor="middle">device damper b = 0.8 N·s/m</text>
    <text x="116" y="144">y: depth past x<tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> = 0.030 m</tspan></text>
  </g>
  <rect x="392" y="62" width="40" height="36" rx="2" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="352,80 391,80" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#bmA)"/>
  <polyline points="501.2,80 433,80" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#bmA)"/>
  <g font-size="11" fill="currentColor">
    <text x="412" y="84" text-anchor="middle">m</text>
    <text x="386" y="72" text-anchor="end">F = 0.4 N</text>
    <text x="438" y="72">k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> y = 0.692 N</tspan></text>
    <text x="412" y="116" text-anchor="middle">b ẏ = 0: ẏ = 0 at a peak</text>
    <text x="412" y="136" text-anchor="middle">ΣF = 0.4 − 0.6917 = −0.2917 N</text>
    <text x="412" y="152" text-anchor="middle">ÿ = ΣF/m = −7.29 m/s²</text>
    <text x="12" y="176">depth y (mm) against time t (ms), from the moment the push starts</text>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <line x1="60" y1="336" x2="546" y2="336"/><line x1="60" y1="336" x2="60" y2="190"/>
    <line x1="180" y1="336" x2="180" y2="340"/><line x1="300" y1="336" x2="300" y2="340"/><line x1="420" y1="336" x2="420" y2="340"/><line x1="540" y1="336" x2="540" y2="340"/>
    <line x1="56" y1="301" x2="60" y2="301"/><line x1="56" y1="266" x2="60" y2="266"/><line x1="56" y1="231" x2="60" y2="231"/><line x1="56" y1="196" x2="60" y2="196"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="60" y="350" text-anchor="middle">0</text><text x="180" y="350" text-anchor="middle">100</text><text x="300" y="350" text-anchor="middle">200</text><text x="420" y="350" text-anchor="middle">300</text><text x="540" y="350" text-anchor="middle">400</text>
    <text x="300" y="368" text-anchor="middle">t (ms)</text>
    <text x="54" y="340" text-anchor="end">0</text><text x="54" y="305" text-anchor="end">0.5</text><text x="54" y="270" text-anchor="end">1.0</text><text x="54" y="235" text-anchor="end">1.5</text><text x="54" y="200" text-anchor="end">2.0</text>
  </g>
  <line x1="60" y1="266" x2="546" y2="266" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
  <polyline points="60.0,195.6 66.0,199.1 72.0,202.3 78.0,205.4 84.0,208.4 90.0,211.2 96.0,213.9 102.0,216.4 108.0,218.8 114.0,221.1 120.0,223.3 126.0,225.4 132.0,227.4 138.0,229.3 144.0,231.1 150.0,232.8 156.0,234.4 162.0,235.9 168.0,237.4 174.0,238.8 180.0,240.1 186.0,241.4 192.0,242.6 198.0,243.7 204.0,244.8 210.0,245.8 216.0,246.8 222.0,247.8 228.0,248.7 234.0,249.5 240.0,250.3 246.0,251.1 252.0,251.8 258.0,252.5 264.0,253.1 270.0,253.8 276.0,254.4 282.0,254.9 288.0,255.5 294.0,256.0 300.0,256.5 306.0,256.9 312.0,257.4 318.0,257.8 324.0,258.2 330.0,258.6 336.0,258.9 342.0,259.3 348.0,259.6 354.0,259.9 360.0,260.2 366.0,260.5 372.0,260.8 378.0,261.0 384.0,261.3 390.0,261.5 396.0,261.7 402.0,261.9 408.0,262.1 414.0,262.3 420.0,262.5 426.0,262.7 432.0,262.8 438.0,263.0 444.0,263.1 450.0,263.3 456.0,263.4 462.0,263.5 468.0,263.7 474.0,263.8 480.0,263.9 486.0,264.0 492.0,264.1 498.0,264.2 504.0,264.3 510.0,264.3 516.0,264.4 522.0,264.5 528.0,264.6 534.0,264.6 540.0,264.7" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.5"/>
  <polyline points="60.0,336.4 66.0,332.9 72.0,329.7 78.0,326.6 84.0,323.6 90.0,320.8 96.0,318.1 102.0,315.6 108.0,313.2 114.0,310.9 120.0,308.7 126.0,306.6 132.0,304.6 138.0,302.7 144.0,300.9 150.0,299.2 156.0,297.6 162.0,296.1 168.0,294.6 174.0,293.2 180.0,291.9 186.0,290.6 192.0,289.4 198.0,288.3 204.0,287.2 210.0,286.2 216.0,285.2 222.0,284.2 228.0,283.3 234.0,282.5 240.0,281.7 246.0,280.9 252.0,280.2 258.0,279.5 264.0,278.9 270.0,278.2 276.0,277.6 282.0,277.1 288.0,276.5 294.0,276.0 300.0,275.5 306.0,275.1 312.0,274.6 318.0,274.2 324.0,273.8 330.0,273.4 336.0,273.1 342.0,272.7 348.0,272.4 354.0,272.1 360.0,271.8 366.0,271.5 372.0,271.2 378.0,271.0 384.0,270.7 390.0,270.5 396.0,270.3 402.0,270.1 408.0,269.9 414.0,269.7 420.0,269.5 426.0,269.3 432.0,269.2 438.0,269.0 444.0,268.9 450.0,268.7 456.0,268.6 462.0,268.5 468.0,268.3 474.0,268.2 480.0,268.1 486.0,268.0 492.0,267.9 498.0,267.8 504.0,267.7 510.0,267.7 516.0,267.6 522.0,267.5 528.0,267.4 534.0,267.4 540.0,267.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.5"/>
  <polyline points="60.0,336.0 61.2,335.7 62.4,334.6 63.6,332.9 64.8,330.6 66.0,327.7 67.2,324.2 68.4,320.3 69.6,315.8 70.8,311.0 72.0,305.8 73.2,300.4 74.4,294.6 75.6,288.8 76.8,282.8 78.0,276.8 79.2,270.7 80.4,264.8 81.6,259.0 82.8,253.3 84.0,247.9 85.2,242.8 86.4,238.0 87.6,233.6 88.8,229.6 90.0,226.1 91.2,223.0 92.4,220.4 93.6,218.3 94.8,216.7 96.0,215.6 97.2,215.0 98.4,215.0 99.6,215.5 100.8,216.4 102.0,217.9 103.2,219.7 104.4,222.0 105.6,224.7 106.8,227.8 108.0,231.1 109.2,234.8 110.4,238.6 111.6,242.7 112.8,246.9 114.0,251.2 115.2,255.6 116.4,260.0 117.6,264.4 118.8,268.7 120.0,272.9 121.2,276.9 122.4,280.8 123.6,284.4 124.8,287.8 126.0,290.9 127.2,293.7 128.4,296.1 129.6,298.2 130.8,300.0 132.0,301.4 133.2,302.4 134.4,303.0 135.6,303.2 136.8,303.1 138.0,302.6 139.2,301.8 140.4,300.6 141.6,299.1 142.8,297.3 144.0,295.2 145.2,292.9 146.4,290.3 147.6,287.6 148.8,284.7 150.0,281.7 151.2,278.6 152.4,275.4 153.6,272.2 154.8,269.0 156.0,265.8 157.2,262.7 158.4,259.7 159.6,256.8 160.8,254.1 162.0,251.5 163.2,249.1 164.4,247.0 165.6,245.0 166.8,243.3 168.0,241.9 169.2,240.8 170.4,239.9 171.6,239.3 172.8,238.9 174.0,238.9 175.2,239.1 176.4,239.5 177.6,240.3 178.8,241.2 180.0,242.4 181.2,243.8 182.4,245.4 183.6,247.2 184.8,249.1 186.0,251.1 187.2,253.3 188.4,255.5 189.6,257.8 190.8,260.1 192.0,262.5 193.2,264.8 194.4,267.1 195.6,269.3 196.8,271.5 198.0,273.6 199.2,275.5 200.4,277.3 201.6,279.0 202.8,280.5 204.0,281.8 205.2,283.0 206.4,283.9 207.6,284.7 208.8,285.3 210.0,285.6 211.2,285.8 212.4,285.7 213.6,285.5 214.8,285.1 216.0,284.5 217.2,283.7 218.4,282.8 219.6,281.7 220.8,280.5 222.0,279.1 223.2,277.7 224.4,276.2 225.6,274.6 226.8,272.9 228.0,271.3 229.2,269.5 230.4,267.8 231.6,266.2 232.8,264.5 234.0,262.9 235.2,261.3 236.4,259.9 237.6,258.5 238.8,257.2 240.0,256.0 241.2,255.0 242.4,254.1 243.6,253.3 244.8,252.7 246.0,252.2 247.2,251.8 248.4,251.6 249.6,251.6 250.8,251.7 252.0,251.9 253.2,252.2 254.4,252.7 255.6,253.4 256.8,254.1 258.0,254.9 259.2,255.8 260.4,256.9 261.6,257.9 262.8,259.1 264.0,260.2 265.2,261.5 266.4,262.7 267.6,263.9 268.8,265.2 270.0,266.4 271.2,267.6 272.4,268.8 273.6,269.9 274.8,270.9 276.0,271.9 277.2,272.8 278.4,273.6 279.6,274.3 280.8,274.9 282.0,275.5 283.2,275.9 284.4,276.2 285.6,276.4 286.8,276.5 288.0,276.5 289.2,276.4 290.4,276.2 291.6,275.9 292.8,275.5 294.0,275.0 295.2,274.4 296.4,273.8 297.6,273.1 298.8,272.3 300.0,271.5 301.2,270.7 302.4,269.8 303.6,268.9 304.8,268.0 306.0,267.1 307.2,266.2 308.4,265.3 309.6,264.5 310.8,263.6 312.0,262.9 313.2,262.1 314.4,261.4 315.6,260.8 316.8,260.2 318.0,259.7 319.2,259.3 320.4,259.0 321.6,258.7 322.8,258.5 324.0,258.4 325.2,258.3 326.4,258.4 327.6,258.5 328.8,258.7 330.0,258.9 331.2,259.2 332.4,259.6 333.6,260.0 334.8,260.5 336.0,261.1 337.2,261.6 338.4,262.2 339.6,262.8 340.8,263.5 342.0,264.1 343.2,264.8 344.4,265.5 345.6,266.1 346.8,266.8 348.0,267.4 349.2,268.0 350.4,268.5 351.6,269.1 352.8,269.5 354.0,270.0 355.2,270.4 356.4,270.7 357.6,271.0 358.8,271.2 360.0,271.4 361.2,271.5 362.4,271.6 363.6,271.6 364.8,271.5 366.0,271.4 367.2,271.3 368.4,271.1 369.6,270.8 370.8,270.5 372.0,270.2 373.2,269.8 374.4,269.4 375.6,269.0 376.8,268.6 378.0,268.1 379.2,267.6 380.4,267.1 381.6,266.7 382.8,266.2 384.0,265.7 385.2,265.3 386.4,264.8 387.6,264.4 388.8,264.0 390.0,263.6 391.2,263.3 392.4,263.0 393.6,262.7 394.8,262.5 396.0,262.3 397.2,262.1 398.4,262.0 399.6,261.9 400.8,261.9 402.0,261.9 403.2,262.0 404.4,262.1 405.6,262.2 406.8,262.4 408.0,262.6 409.2,262.8 410.4,263.0 411.6,263.3 412.8,263.6 414.0,263.9 415.2,264.3 416.4,264.6 417.6,265.0 418.8,265.3 420.0,265.7 421.2,266.0 422.4,266.4 423.6,266.7 424.8,267.0 426.0,267.3 427.2,267.6 428.4,267.8 429.6,268.1 430.8,268.3 432.0,268.5 433.2,268.6 434.4,268.8 435.6,268.9 436.8,268.9 438.0,269.0 439.2,269.0 440.4,269.0 441.6,268.9 442.8,268.8 444.0,268.7 445.2,268.6 446.4,268.4 447.6,268.3 448.8,268.1 450.0,267.9 451.2,267.6 452.4,267.4 453.6,267.2 454.8,266.9 456.0,266.6 457.2,266.4 458.4,266.1 459.6,265.9 460.8,265.6 462.0,265.4 463.2,265.2 464.4,265.0 465.6,264.8 466.8,264.6 468.0,264.4 469.2,264.3 470.4,264.1 471.6,264.0 472.8,263.9 474.0,263.9 475.2,263.8 476.4,263.8 477.6,263.8 478.8,263.9 480.0,263.9 481.2,264.0 482.4,264.1 483.6,264.2 484.8,264.3 486.0,264.4 487.2,264.6 488.4,264.7 489.6,264.9 490.8,265.1 492.0,265.2 493.2,265.4 494.4,265.6 495.6,265.8 496.8,266.0 498.0,266.2 499.2,266.3 500.4,266.5 501.6,266.7 502.8,266.8 504.0,267.0 505.2,267.1 506.4,267.2 507.6,267.3 508.8,267.4 510.0,267.5 511.2,267.5 512.4,267.6 513.6,267.6 514.8,267.6 516.0,267.6 517.2,267.5 518.4,267.5 519.6,267.5 520.8,267.4 522.0,267.3 523.2,267.2 524.4,267.1 525.6,267.0 526.8,266.9 528.0,266.8 529.2,266.6 530.4,266.5 531.6,266.4 532.8,266.2 534.0,266.1 535.2,266.0 536.4,265.8 537.6,265.7 538.8,265.6 540.0,265.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="60.0,336.0 61.2,335.3 62.4,333.6 63.6,331.0 64.8,327.7 66.0,324.0 67.2,319.9 68.4,315.7 69.6,311.5 70.8,307.2 72.0,303.1 73.2,299.1 74.4,295.3 75.6,291.7 76.8,288.4 78.0,285.3 79.2,282.5 80.4,280.0 81.6,277.7 82.8,275.6 84.0,273.8 85.2,272.2 86.4,270.8 87.6,269.6 88.8,268.6 90.0,267.7 91.2,267.0 92.4,266.4 93.6,265.9 94.8,265.5 96.0,265.2 97.2,264.9 98.4,264.8 99.6,264.7 100.8,264.6 102.0,264.6 103.2,264.6 104.4,264.6 105.6,264.6 106.8,264.7 108.0,264.8 109.2,264.9 110.4,265.0 111.6,265.0 112.8,265.1 114.0,265.2 115.2,265.3 116.4,265.4 117.6,265.4 118.8,265.5 120.0,265.6 121.2,265.6 122.4,265.7 123.6,265.7 124.8,265.8 126.0,265.8 127.2,265.9 128.4,265.9 129.6,265.9 130.8,265.9 132.0,266.0 133.2,266.0 134.4,266.0 135.6,266.0 136.8,266.0 138.0,266.0 139.2,266.0 140.4,266.0 141.6,266.0 142.8,266.0 144.0,266.0 145.2,266.0 146.4,266.0 147.6,266.0 148.8,266.0 150.0,266.0 151.2,266.0 152.4,266.0 153.6,266.0 154.8,266.0 156.0,266.0 157.2,266.0 158.4,266.0 159.6,266.0 160.8,266.0 162.0,266.0 163.2,266.0 164.4,266.0 165.6,266.0 166.8,266.0 168.0,266.0 169.2,266.0 170.4,266.0 171.6,266.0 172.8,266.0 174.0,266.0 175.2,266.0 176.4,266.0 177.6,266.0 178.8,266.0 180.0,266.0 181.2,266.0 182.4,266.0 183.6,266.0 184.8,266.0 186.0,266.0 187.2,266.0 188.4,266.0 189.6,266.0 190.8,266.0 192.0,266.0 193.2,266.0 194.4,266.0 195.6,266.0 196.8,266.0 198.0,266.0 199.2,266.0 200.4,266.0 201.6,266.0 202.8,266.0 204.0,266.0 205.2,266.0 206.4,266.0 207.6,266.0 208.8,266.0 210.0,266.0 211.2,266.0 212.4,266.0 213.6,266.0 214.8,266.0 216.0,266.0 217.2,266.0 218.4,266.0 219.6,266.0 220.8,266.0 222.0,266.0 223.2,266.0 224.4,266.0 225.6,266.0 226.8,266.0 228.0,266.0 229.2,266.0 230.4,266.0 231.6,266.0 232.8,266.0 234.0,266.0 235.2,266.0 236.4,266.0 237.6,266.0 238.8,266.0 240.0,266.0" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <circle cx="97.9" cy="215" r="3" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" opacity="0.8">
    <line x1="520.6" y1="262" x2="520.6" y2="336"/><line x1="104.4" y1="262" x2="104.4" y2="336"/>
  </g>
  <line x1="236" y1="292" x2="256" y2="292" stroke="currentColor" stroke-width="1.8"/>
  <line x1="236" y1="308" x2="256" y2="308" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <g font-size="11" fill="currentColor">
    <text x="106" y="206">first peak 1.729 mm at 31.6 ms: 0.692 N on the wall</text>
    <text x="260" y="248">envelope: τ = 2m/b = 100 ms</text>
    <text x="544" y="258" text-anchor="end">y<tspan dy="3" font-size="10">ss</tspan><tspan dy="-3"> = F/k</tspan><tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> = 1.0 mm</tspan></text>
    <text x="262" y="296">bare handle: ζ = 0.10, overshoot 72.9 %</text>
    <text x="262" y="312">gripped, + k<tspan dy="3" font-size="10">h</tspan><tspan dy="-3"> and b</tspan><tspan dy="3" font-size="10">h</tspan><tspan dy="-3">: ζ = 0.78, 2.0 %</tspan></text>
    <text x="108" y="328">gripped settles at 37 ms</text>
    <text x="516" y="328" text-anchor="end">bare settles at 384 ms</text>
  </g>
</svg>

P3's handle pushed from rest by a steady $F=0.4\,\mathrm{N}$ into its $400\,\mathrm{N/m}$ wall, with its own $0.8\,\mathrm{N{\cdot}s/m}$ damper: the model, the free-body diagram at the first peak — $0.692\,\mathrm{N}$ back against $0.4\,\mathrm{N}$ in, no damper force, so $\ddot y=-7.29\,\mathrm{m/s^2}$ — and the depth against time. Bare, the handle rings at a damping ratio of $0.10$, peaks at $1.729\,\mathrm{mm}$ after $31.6\,\mathrm{ms}$ inside an envelope whose time constant is $100\,\mathrm{ms}$, and settles into a $2\%$ band at $384\,\mathrm{ms}$. Gripped by the hand, whose spring and damper add to the wall's and the device's, it overshoots $2.0\%$ and settles at $37\,\mathrm{ms}$; both end at $1.0\,\mathrm{mm}$ with $0.4\,\mathrm{N}$ on the wall.

### 1. Quantities, units and dimensional checks

Most wrong numbers in a derivation or a line of code are unit slips, and this section is the check that catches them before they spread. A physical quantity is a number times a unit, and the number alone means nothing: P3's wall is $400\,\mathrm{N/m}$, which is also $0.4\,\mathrm{N/mm}$ and $400\,\mathrm{kg/s^2}$ — one stiffness written three ways. This wiki computes in SI, the International System of Units, whose three mechanical base units are the kilogram, the metre and the second; every other mechanical unit is a product of powers of those three. The NIST guide to the SI tabulates the derived units that have special names (its Table 3), and four of them carry this page:

| Quantity | SI unit | In base units | On P3 or P2 |
|---|---|---|---|
| force | newton, $\mathrm{N}$ | $\mathrm{kg\,m\,s^{-2}}$ | the push, $F=0.4\,\mathrm{N}$ |
| energy, work | joule, $\mathrm{J}=\mathrm{N\,m}$ | $\mathrm{kg\,m^2\,s^{-2}}$ | $0.2\,\mathrm{mJ}$ stored in the wall at $1\,\mathrm{mm}$ (§6) |
| power | watt, $\mathrm{W}=\mathrm{J/s}$ | $\mathrm{kg\,m^2\,s^{-3}}$ | $8\,\mathrm{mW}$ into the damper at $0.1\,\mathrm{m/s}$ (§4) |
| pressure, stress | pascal, $\mathrm{Pa}=\mathrm{N/m^2}$ | $\mathrm{kg\,m^{-1}\,s^{-2}}$ | steel's elastic modulus, $200\,\mathrm{GPa}$ (§3) |

Three more have no special name and appear on every line below: stiffness in $\mathrm{N/m}=\mathrm{kg\,s^{-2}}$, damping in $\mathrm{N{\cdot}s/m}=\mathrm{kg\,s^{-1}}$ and torque in $\mathrm{N{\cdot}m}$. Angles are in radians, and the radian is a special name for the number one — a metre of arc per metre of radius (the guide's §4.2.1) — so an angular speed in $\mathrm{rad/s}$ is dimensionally $\mathrm{s^{-1}}$, and $100\,\mathrm{rad/s}$ is $100\cdot60/(2\pi)=955$ revolutions per minute.

The unit tells you what a number is; the *dimension* — which powers of mass, length and time it is made of — tells you what it can be added to. That gives a test every equation must pass before it is believed.

> **Dimensional homogeneity, defined.** **Dimensional homogeneity** is a *property of an equation*: a necessary condition that any physically meaningful equation satisfies, whatever units it is later evaluated in. Three defining conditions, the first two as OpenStax states the rule. Every term that is **added, subtracted or equated** carries the same dimension, since a force cannot be added to a velocity. And the argument of every **exponential, logarithm or trigonometric function** is a pure number, because $e^x=1+x+x^2/2+\dots$ would otherwise add quantities of different dimension. A third condition keeps the check honest about what it proves: passing it is **necessary, not sufficient**, since a dimensionless factor — a 2, a $\pi$ — can still be wrong.
>
> $$[m\ddot y]=[b\dot y]=[ky]=[F]=\mathrm{kg\,m\,s^{-2}}=\mathrm{N}$$
>
> where $[\cdot]$ reads "the dimension of", $m$ is a mass, $b$ a damping coefficient, $k$ a stiffness and $y$ a displacement — so the equation of motion of §5 is homogeneous, because $b$ in $\mathrm{kg/s}$ times $\dot y$ in $\mathrm{m/s}$, and $k$ in $\mathrm{kg/s^2}$ times $y$ in $\mathrm{m}$, both come out in newtons.
> - **Example**: P3's damping ratio (§5), $\zeta=b/(2\sqrt{km})$, has dimension $(\mathrm{kg/s})/\sqrt{(\mathrm{kg/s^2})\,\mathrm{kg}}=(\mathrm{kg/s})/(\mathrm{kg/s})=1$, so it may sit in an exponent: in $e^{-\zeta\omega_nt}$ the product $\zeta\omega_nt$ is $1\times\mathrm{s^{-1}}\times\mathrm{s}$, a pure number, as the second condition demands.
> - **Non-example**: $\zeta=b/\sqrt{km}$. It is exactly as homogeneous as the right formula and twice as large — P3 would read $0.2$ instead of $0.1$. The check cannot see a missing 2.
> - **Non-example**: a torque and an energy. $19.62\,\mathrm{N{\cdot}m}$ of holding torque and $19.62\,\mathrm{J}$ of work have the same dimension, $\mathrm{kg\,m^2\,s^{-2}}$, and are different quantities; the NIST guide writes the unit of a moment of force as the newton metre, not the joule, to keep them apart (its §4.2.2). Equal dimensions are needed before two terms may be added, but they do not prove the terms are the same kind of thing.
> - **Why it matters**: it is the cheapest test a derivation or a line of code can pass, and it catches this page's commonest slip — millimetres in a formula whose stiffness is in N/m, which puts the wall's energy at $1\,\mathrm{mm}$ at $\tfrac12\cdot400\cdot1^2=200$ instead of $\tfrac12\cdot400\cdot(10^{-3})^2=2\times10^{-4}\,\mathrm{J}$, a factor of $10^6$.

The page runs the check on every new formula. Three of them, since they recur in every section below:

$$[\omega_n]=\Big[\sqrt{k/m}\Big]=\sqrt{\frac{\mathrm{kg\,s^{-2}}}{\mathrm{kg}}}=\mathrm{s^{-1}},\qquad \Big[\frac mb\Big]=\frac{\mathrm{kg}}{\mathrm{kg\,s^{-1}}}=\mathrm{s},\qquad [b\dot y^2]=\mathrm{kg\,s^{-1}}\cdot\mathrm{m^2\,s^{-2}}=\mathrm{W}$$

so the natural frequency of §5 is a rate, the time constant a time and the damper's power a power, since each side reduces to the same base units. Three more slips the units catch, each on this page's numbers:

- **Mass is not weight.** P2's point masses are $1\,\mathrm{kg}$ each; each *weighs* $1\cdot9.81=9.81\,\mathrm{N}$. A kilogram in a force balance is a missing $g$.
- **Newtons are not newton-metres.** Held at its catalog pose, P2 needs $19.62\,\mathrm{N}$ of force from its base and $19.62\,\mathrm{N{\cdot}m}$ of torque at its shoulder (§8). The digits agree only because the lever arm is $1\,\mathrm{m}$.
- **Revolutions are not radians.** A motor turning P2's joint through the $n=100$ gearbox at $1\,\mathrm{rad/s}$ spins at $100\,\mathrm{rad/s}$, which a datasheet would print as $955\,\mathrm{rpm}$; a formula expecting one and fed the other is off by $2\pi/60$.

### 2. Force, Newton's laws and the free-body diagram

To predict how anything moves you first need every force on it; Newton's laws turn those forces into motion, and the free-body diagram makes sure none is missed or counted twice. A **force** is a push or a pull on a body: a vector, with a size in newtons and a direction. Newton's three laws connect forces to motion, and OpenStax states them for exactly the use this page makes of them. In substance:

1. A body on which the net external force is zero keeps its velocity: at rest it stays at rest, and moving it keeps moving in a straight line at constant speed.
2. The net external force equals mass times acceleration, $\sum\vec F=m\vec a$, in an inertial frame; one newton is the force that gives one kilogram an acceleration of one metre per second squared, $1\,\mathrm{N}=1\,\mathrm{kg\,m/s^2}$.
3. Forces come in pairs. If body A pushes on body B, B pushes on A with a force equal in size and opposite in direction, $\vec F_{AB}=-\vec F_{BA}$, and because the two act on different bodies they never cancel inside one body's equation.

If you learned free-body diagrams in statics, the drawing does not change. Statics writes $\sum\vec F=0$ because its bodies do not accelerate; dynamics keeps the same diagram and writes $\sum\vec F=m\vec a$, so whatever the forces leave unbalanced is spent accelerating the body. Every instant of the ringing in the picture is such an imbalance between the push, the wall and the damper.

The second law is the working one, and it has to know which forces act on which body. That bookkeeping has a name and a drawing.

> **Free-body diagram, defined.** A **free-body diagram** is a *drawing of one chosen body cut free from everything it touches*, with every external force on it drawn as an arrow — the modelling step that turns a physical set-up into Newton's second law. Four defining conditions. **One body**, or one chosen system, is isolated, and everything it touches is replaced by the force it exerts. **Every external force** on that body is drawn with its direction at the point where it acts: contact forces wherever the body touches something, and field forces such as weight. **Nothing else** is drawn — not the forces the body exerts on others, which belong in their diagrams by the third law, not internal forces, and not $m\ddot y$, which is the result of the forces rather than one of them. And an **axis with a positive direction** is chosen, so that every arrow becomes a signed component.
>
> $$\sum F_x=m\,a_x:\qquad F-k_w\,y-b\,\dot y=m\,\ddot y$$
>
> where the left side adds the $x$-components of the drawn forces and the right side is mass times acceleration along the same axis — on P3 the push $F$, the wall's $-k_wy$ (for $y>0$) and the damper's $-b\dot y$, because those are the only forces with a component along $x$.
> - **Example**: P3 at the first peak, the top right of the picture. There $\dot y=0$, so the damper pushes nothing; the wall pushes back $400\times1.729\times10^{-3}=0.692\,\mathrm{N}$ against the $0.4\,\mathrm{N}$ push, so $\sum F_x=0.4-0.6917=-0.2917\,\mathrm{N}$ and $\ddot y=-0.2917/0.04=-7.29\,\mathrm{m/s^2}$: the handle is momentarily still and already being thrown back out.
> - **Non-example**: the same diagram with a fourth arrow, $m\ddot y$, drawn "to balance" it. With that arrow the forces sum to zero, the law reads $0=0$, and the acceleration has vanished from the problem — or, if it is also kept on the right-hand side, the mass is counted twice.
> - **Non-example**: the handle's diagram carrying the $0.4\,\mathrm{N}$ the handle exerts **on the hand**. That force acts on the hand; it is the push's third-law partner, and the two never appear in one diagram.
> - **Why it matters**: every equation of motion above this page begins with one — the state-space model of [[04-robotics/control-theory-ce397|5. Control Theory §2]], the manipulator equation of [[02-foundations/manipulator-kinematics-dynamics|10. §2]], the target impedance of [[04-robotics/force-compliance-control|13. §2]] — and a missing or doubled arrow there is a wrong model before any control is designed.

Carried out on P3, the diagram gives the handle's equation of motion. The handle's weight, $0.04\cdot9.81=0.39\,\mathrm{N}$, and the guide's reaction act across the axis and cancel; along it act the push, the wall and the damper, so

$$m\,\ddot y+b\,\dot y+k_w\,y=F\qquad(y>0)$$

because $x_w$ is a constant, so $\dot y=\dot x$ and $\ddot y=\ddot x$, and moving the two opposing forces to the left leaves the one driving force on the right. Three instants read straight off it. At $t=0$ the handle rests on the surface, $y=\dot y=0$, so only the push acts and $\ddot y=F/m=0.4/0.04=10\,\mathrm{m/s^2}$, about one $g$. At the first peak $\ddot y=-7.29\,\mathrm{m/s^2}$, the box's example. At the end $\dot y=\ddot y=0$ and the wall pushes back exactly $0.4\,\mathrm{N}$ — equilibrium, the first law.

**The third law, and what a force sensor sees.** The handle pushes back on the hand with exactly the force the hand pushes it with. Only when the handle is not accelerating is that also the wall's force: at the first peak the wall pushes $0.692\,\mathrm{N}$ while the hand still pushes $0.4\,\mathrm{N}$, and the difference, $0.292\,\mathrm{N}$, is $m\ddot y$ — what it takes to stop and turn $40\,\mathrm{g}$ of handle. A force sensor in the grip and one in the wall would disagree by exactly $m\ddot y$ while the handle rings and agree once it has settled, so a force read during a transient is not the steady contact force. [[04-robotics/force-compliance-control|13. §5]] prices the same inertia in an impact, where arriving at $5\,\mathrm{cm/s}$ puts a $22.4\,\mathrm{N}$ peak on a panel the controller means to press with $10\,\mathrm{N}$.

### 3. Springs: stiffness, series and parallel, preload

Everything that gives under load — a contact, a grip, a cable, a beam — pushes back like a spring, and predicting how far it gives takes its stiffness and the rule for combining two of them. A spring is the simplest thing that turns a displacement into a force. P3 has two — the wall its motor renders and, when a person grips the handle, the hand — and every stiffness on the robotics pages is the same object with a different number.

> **Linear spring, defined.** A **linear spring** is an *idealized two-ended element* whose force depends only on how far its length differs from its free length, in proportion. Four defining conditions. The force is **proportional** to the deflection, so twice the deflection gives twice the force — additivity and homogeneity in the sense of [[02-foundations/engineering-math|0.5 §4.5]]. It is **restoring**: the force on whatever deflects it points back toward the free length, hence the minus sign. It is **conservative**: it stores the work done on it and returns all of it, with no mass and no loss. And it is **two-sided**: it pulls when stretched as readily as it pushes when compressed, over the whole range in use.
>
> $$F=-k\,(x-x_0),\qquad U=\tfrac12\,k\,(x-x_0)^2$$
>
> where $F$ is the force the spring exerts on the body at $x$, $x_0$ the position at which the spring has its free length, $k$ the **stiffness** in $\mathrm{N/m}$ and $U$ the stored energy in joules — the energy because the work done against the force over a deflection $\delta$ is $\int_0^\delta ks\,ds=\tfrac12k\delta^2$. The reciprocal $1/k$ is the compliance, defined with the rest of that vocabulary in [[04-robotics/force-compliance-control|13. §1]].
> - **Example**: the hand, $k_h=400\,\mathrm{N/m}$. Held $1\,\mathrm{mm}$ away from where it aims, it pulls back with $400\cdot10^{-3}=0.4\,\mathrm{N}$ and stores $\tfrac12\cdot400\cdot(10^{-3})^2=0.2\,\mathrm{mJ}$.
> - **Non-example**: P3's virtual wall taken as a whole. Inside it, $F_a=-k_w(x-x_w)$ is a linear spring with $x_0=x_w$; but it only pushes — $F_a=0$ for $x\le x_w$ — so pulling the handle $1\,\mathrm{mm}$ out of the wall draws $0\,\mathrm{N}$, not $0.4\,\mathrm{N}$, and superposition fails across the surface. A real contact is one-sided in the same way, and its stiffness also rises with the load ([[04-robotics/force-compliance-control|13. §1]]).
> - **Why it matters**: every stiffness on the robotics pages — 13's target and environment stiffnesses, 24.4's $k_w$ — is this $k$, and the proportionality is what gives a mass on a spring one natural frequency whatever the amplitude (§5).

Two springs acting on one body can always be replaced by one, and which rule does it is the first place where a drawing misleads.

> **Springs in series and in parallel, defined.** **Parallel** and **series** are *two rules for replacing two springs by one equivalent spring*, and which one applies is decided by what the two springs share, not by how they are drawn. Two defining conditions, one per rule. Springs are **in parallel** when they share one deflection — attached between the same moving point and the same ground — so their forces add. Springs are **in series** when they carry one force — the end of one is the start of the next, with nothing else attached between them — so their deflections add, and with them their compliances.
>
> $$k_{\parallel}=k_1+k_2,\qquad \frac{1}{k_{\text{series}}}=\frac{1}{k_1}+\frac{1}{k_2}$$
>
> which follow in one line each, because in parallel $F=k_1\delta+k_2\delta=(k_1+k_2)\,\delta$ and in series $\delta=F/k_1+F/k_2$ — so a parallel pair is stiffer than either spring, and a series pair softer than either.
> - **Example**: the hand gripping P3 in its wall. For the handle's own motion, with the hand's aim point held still, the hand's spring and the wall both deflect by the handle's $y$: parallel, $400+400=800\,\mathrm{N/m}$, the $800$ in 24.4's characteristic polynomial. For the question "how far past the surface must the hand aim to press the wall with $0.4\,\mathrm{N}$", that one force runs through both springs in turn: series, $1/(1/400+1/400)=200\,\mathrm{N/m}$, so the aim moves $0.4/200=0.002\,\mathrm{m}$ — 24.4's aim point at $0.032\,\mathrm{m}$, $2\,\mathrm{mm}$ past the surface at $0.030$.
> - **Non-example**: "hand, handle and wall sit in a row, so they are in series." The drawing is a row, but for the handle's motion the two springs share its deflection; the series value would put P3's natural frequency at $\sqrt{200/0.04}=70.7$ instead of $\sqrt{800/0.04}=141.4\,\mathrm{rad/s}$.
> - **Why it matters**: the series rule is why the softest element in a chain sets its stiffness — the argument [[04-robotics/force-compliance-control|13. §1]] runs on a controller, a tool and a panel — and the parallel rule is why a firm grip both stiffens and steadies a haptic handle (§5).

A spring that is already carrying force at its working point behaves differently at the edges of its range, and one more word covers that.

> **Preload, defined.** **Preload** is a *force already carried by a spring or a contact at its operating point*, set by assembly or by a steady push before any working load arrives. Three defining conditions. The element is **not at its free length** at the operating point, so it carries a force $F_0$ with no working load on it. Its force–deflection line is **shifted, not tilted**: about the operating point it still has its stiffness $k$. And a **one-sided** element — a contact, a cable, a bolted joint — stays engaged only while the working load has not undone the preload; beyond that it opens, and its stiffness drops to zero.
>
> $$F=F_0+k\,\delta\qquad\text{while}\quad F_0+k\,\delta>0$$
>
> where $F$ is the force the element carries, $\delta$ the deflection from the operating point and $F_0$ the preload. The condition is there because a one-sided element can push but not pull, so it acts as an ordinary two-sided spring for any disturbance small enough to keep $F$ positive, and as nothing at all beyond it.
> - **Example**: P3 held in its wall by the steady $0.4\,\mathrm{N}$ push rests at $y=1\,\mathrm{mm}$, and the one-sided wall carries a preload $F_0=0.4\,\mathrm{N}$. A pull on the handle then meets the full $400\,\mathrm{N/m}$, as if the wall were two-sided, until the pull reaches $0.4\,\mathrm{N}$ and brings the handle back to $y=0$; any more and the contact opens.
> - **Non-example**: "preload makes a spring stiffer." A single linear spring has the same $k$ at any preload: P3's handle answers a small extra push at $400\,\mathrm{N/m}$ whether it is pressed with $0.1$ or with $0.4\,\mathrm{N}$. What preload buys is the range over which that stiffness is there at all — and, for a contact whose stiffness rises with load, a steeper local slope.
> - **Why it matters**: it is how a mechanism is made free of play — a tensioned capstan cable, a preloaded bearing, a bolted joint that must not open, as in the pretensioned bolts of steel structures — and how a pressed contact is kept closed through a disturbance, which is the hold phase of every pressing task.

**Real parts are springs too.** A bar pulled along its axis stretches in proportion to the load while the material stays elastic, which OpenStax writes with Young's modulus as $F=YA\,\Delta L/L_0$; this page writes the modulus $E$, as 13 does, and read as a spring the bar is

$$k=\frac{E\,A}{L_0}$$

because the force per unit stretch is the modulus $E$ times the cross-section $A$ over the length $L_0$ — a stiff material, a thick bar and a short one each make a stiffer spring. OpenStax tabulates $E=200\,\mathrm{GPa}$ for steel and $70\,\mathrm{GPa}$ for aluminium. A steel wire $0.5\,\mathrm{mm}$ across and $0.1\,\mathrm{m}$ long — a page-local illustration, taken as solid steel — has $A=\pi(0.25\times10^{-3})^2=1.96\times10^{-7}\,\mathrm{m^2}$ and $k=3.93\times10^5\,\mathrm{N/m}$. Put in series with P3's $400\,\mathrm{N/m}$ wall it changes nothing a hand could feel, $1/(1/400+1/393{,}000)=399.6\,\mathrm{N/m}$; put in series with the $10^5\,\mathrm{N/m}$ that [[04-robotics/force-compliance-control|13. §1]] says a force controller identifies against a stiff panel, the same wire takes the chain down to $7.97\times10^4\,\mathrm{N/m}$, a fifth softer. A beam in bending is a spring as well — the cantilever's tip stiffness $3EI/L^3$ is the civil engineer's first one — and a contact is a spring whose stiffness grows with load, Hertz's result, which 13 §1 works for a steel ball on steel.

### 4. Damping and friction: the viscous damper, Coulomb friction and stiction

A spring stores energy and gives it back, so a handle on springs alone would ring for ever. Two kinds of force take energy out, and they behave so differently that treating one as the other is among the commonest modelling errors made about a robot's joint.

In plain words, a **viscous damper** is a car's shock absorber or a door closer: a piston forcing oil through small holes, which barely resists a slow push and resists a fast one hard, because its force grows with speed, not with position. **Friction** is a book dragged across a table: the force hardly depends on how fast you drag it, and starting it takes a little more than keeping it going. P3's $b$ lumps into one number whatever resists the handle in proportion to its speed; this page's $f_c$ and $f_s$ add the second kind.

> **Viscous damper, defined.** A **viscous damper**, or dashpot, is an *idealized two-ended element* whose force depends only on how fast its ends move apart or together, in proportion. Three defining conditions. The force is **proportional to the relative velocity**, so the element is linear. It **opposes** that velocity, so the power it absorbs, $b\dot x^2$, is never negative: it only ever removes energy. And it **stores nothing** — it has no free length and no mass — so at rest it exerts no force at all, wherever its ends are.
>
> $$F_d=-b\,\dot x,\qquad P_d=b\,\dot x^2\ge0$$
>
> where $F_d$ is the force on the body, $\dot x$ the relative velocity of the damper's ends, $b$ the damping coefficient in $\mathrm{N{\cdot}s/m}$ and $P_d$ the power turned into heat, in watts — never negative, because it is $b$ times a square.
> - **Example**: P3's $b=0.8\,\mathrm{N{\cdot}s/m}$. At $0.1\,\mathrm{m/s}$ it pushes back $0.8\cdot0.1=0.08\,\mathrm{N}$ and absorbs $0.8\cdot0.1^2=8\,\mathrm{mW}$, which is $8\,\mathrm{\mu J}$ in every $1\,\mathrm{ms}$ sample period — the dissipation [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]] sets against a sampled wall's energy leak.
> - **Non-example**: "the damper will hold the handle in the wall." At rest $\dot x=0$ and the damper pushes nothing, whatever the position: it can slow the handle but never hold it, which is why a target impedance needs a spring as well as a damper ([[04-robotics/force-compliance-control|13. §1]] makes the same point).
> - **Why it matters**: it is the one linear element that removes energy, so it is what makes a spring's oscillation die away (§5), and every passivity argument above this page is an account of how much of it there is.

The damper alone already has a motion worth knowing. Release P3's handle in free space at $v_0=0.1\,\mathrm{m/s}$ with nothing but its damper acting, and the free-body diagram leaves $m\dot v=-bv$ — the first-order equation of [[02-foundations/engineering-math|0.5 §8]] with $a=-b/m=-20\,\mathrm{s^{-1}}$ — so

$$v(t)=v_0\,e^{-t\,b/m},\qquad \int_0^\infty v\,dt=v_0\,\frac mb$$

because the solution of $\dot v=av$ is $v_0e^{at}$, and the integral of that exponential is $v_0/|a|$. The handle loses $63\%$ of its speed every $m/b=50\,\mathrm{ms}$, glides $0.1\cdot0.05=5\,\mathrm{mm}$ in all, and never quite stops.

> **Coulomb friction and stiction, defined.** **Coulomb friction** is a *model of the tangential force at a sliding contact*: while the surfaces slide, the force has a fixed size and opposes the sliding; while they stick, it is whatever force keeps them stuck, up to a limit. **Stiction** — static friction — names that limit, and the fact that it exceeds the sliding value. Three defining conditions, following OpenStax's statement of the two laws. **Sliding**: the size is $f_c=\mu_kN$, set by the normal force $N$ and the two materials, and nearly independent of the speed and of the contact area. **Sticking**: at zero sliding speed the friction force takes whatever value up to $f_s=\mu_sN$ the other forces call for, so it can balance them exactly. **Breakaway exceeds sliding**: $\mu_s>\mu_k$, so it takes more force to start the motion than to keep it going.
>
> $$F_f=-f_c\,\mathrm{sgn}(\dot x)\ \ \text{if}\ \dot x\ne0,\qquad |F_f|\le f_s\ \ \text{if}\ \dot x=0$$
>
> where $F_f$ is the friction force on the moving body, $\mathrm{sgn}$ the sign of the sliding velocity, and $f_c$ and $f_s$ the sliding and breakaway forces in newtons, $\mu_k$ and $\mu_s$ the kinetic and static coefficients. The first case says that a sliding contact always opposes its own motion with the same force; the second says that a stuck contact supplies whatever the other forces need, up to $f_s$ — which is why it has an inequality where the first has an equation.
> - **Example**: this page's $f_c=0.02$ and $f_s=0.05\,\mathrm{N}$ on P3's guide. Flicked at $0.1\,\mathrm{m/s}$ with the wall and the damper taken away, the handle decelerates at $f_c/m=0.02/0.04=0.5\,\mathrm{m/s^2}$ and stops dead after $0.1/0.5=0.2\,\mathrm{s}$ and $0.1^2/(2\cdot0.5)=0.01\,\mathrm{m}$ — twice as far as the damper let it glide, and in a finite time the damper never reaches.
> - **Non-example**: "friction is a damper with $b=f_c/|v|$." That equivalent coefficient is $0.2\,\mathrm{N{\cdot}s/m}$ at $0.1\,\mathrm{m/s}$, $20$ at $1\,\mathrm{mm/s}$ and unbounded at rest; the paragraph after the code below lists what that does to the handle.
> - **Why it matters**: it sets the smallest force a mechanism can resolve and the floor a person must push through to move it — the $f_c$ in the backdrivability of [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §1]] — and, with the encoder's resolution, it sets how stiff a quantized virtual wall may be rendered passively ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]).

What friction does to the handle in its wall is exact and short enough to compute by hand, and the code below does it. Take the damper away, keep the wall and the steady push, and add this page's friction. Each half-swing is then an undamped oscillation about a shifted centre: while the handle moves into the wall, friction adds to the wall's resistance, so push, spring and friction balance at $(F-f_c)/k_w=0.95\,\mathrm{mm}$; on the way out they balance at $(F+f_c)/k_w=1.05\,\mathrm{mm}$. A half-swing of a spring ends mirrored about its centre, so each turning point is the last one reflected, and the handle sticks at the first turning point where static friction can hold the difference between push and spring.

```python
import numpy as np

# P3 in its wall under the page's steady push, device damper removed, this page's Coulomb friction
m, kw, F = 0.04, 400.0, 0.4          # kg, N/m, N
fc, fs = 0.02, 0.05                  # N: sliding (Coulomb) friction, and breakaway (static) friction
y, turns = 0.0, []                   # start at rest on the wall's surface
while abs(F - kw*y) > fs:            # static friction cannot hold the net force: the handle slides
    s = 1.0 if F > kw*y else -1.0    # the way it starts to move
    centre = (F - s*fc)/kw           # push, spring and sliding friction balance here
    y = 2*centre - y                 # a half-swing of a spring ends mirrored about its centre
    turns.append(y)
half = np.pi*np.sqrt(m/kw)           # friction does not change the swing's duration
print("turning points (mm):", " ".join(f"{1e3*v:.2f}" for v in turns))
print(f"stuck at {1e3*y:.2f} mm after {len(turns)} half-swings, {len(turns)*half:.3f} s; "
      f"spring {kw*y:.3f} N against the {F} N push, friction holds {abs(F - kw*y):.3f} N")
```

It prints the turning points $1.90$, $0.20$, $1.70$, $0.40$, $1.50$, $0.60$, $1.30$, $0.80$ and $1.10\,\mathrm{mm}$, and the handle sticks at $1.10\,\mathrm{mm}$ after nine half-swings, $0.283\,\mathrm{s}$: the wall pushes $0.440\,\mathrm{N}$ against the $0.4\,\mathrm{N}$ push, and static friction holds the $0.040\,\mathrm{N}$ between them. **That is why friction is not a damper.** Four differences, all visible in those numbers:

- **Its force does not scale with speed.** A damper's force shrinks as the motion slows; friction's stays at $f_c$ until the motion stops, which is why its equivalent $b=f_c/|v|$ runs from $0.2$ to unbounded.
- **It holds the body away from equilibrium.** The handle stopped $0.1\,\mathrm{mm}$ past the point where push and spring balance. Anywhere within $\pm f_s/k_w=\pm0.125\,\mathrm{mm}$ of it can be a resting place — about two of P3's $61.4\,\mathrm{\mu m}$ encoder counts ([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §4]]). A damper holds nothing anywhere.
- **It decays the swing linearly and stops it dead.** Measured from the balance point $F/k_w$, every half-swing is $2f_c/k_w=0.1\,\mathrm{mm}$ smaller than the last, because the work friction takes over a half-swing, $f_c$ times its length $A_1+A_2$, equals the fall in $\tfrac12k_w(y-F/k_w)^2$ between its two turning points, $\tfrac12k_w(A_1^2-A_2^2)$, and dividing by $A_1+A_2$ leaves $A_1-A_2=2f_c/k_w$. A damper instead shrinks each swing by the same *fraction*, and never reaches zero.
- **It is not linear.** Double the push and the friction does not double, so superposition fails ([[02-foundations/engineering-math|0.5 §4.5]]), and the damping ratio of §5, defined for a linear damper, does not exist for a handle with friction alone.

It also pays for energy differently: a damper takes $b\dot x^2$, quadratic in speed, and friction $f_c|\dot x|$, linear in it, so friction dominates slow motion and a damper fast motion; on P3 the two take energy at the same rate at $f_c/b=0.02/0.8=0.025\,\mathrm{m/s}$. A real joint has both, and a model with only the damper will predict a return to the set point that the hardware, stopping in its dead band, never makes.

### 5. The mass–spring–damper: natural frequency, damping ratio, time constant

A mass on a spring does not simply move to where the spring balances the push: it overshoots and rings, and whether a contact rings, how hard and for how long is what this section computes. First the story, in words. Pushed into the wall, the handle gains speed until, at $1\,\mathrm{mm}$, the spring's force equals the push — but by then the handle is moving, and its inertia carries it past. Deeper in, the spring pushes back harder than the push, slows the handle, stops it and throws it back out, and on the way out it overshoots the other way. In every swing the damper takes some energy, so each swing is smaller than the last, and the handle rings down to rest at $1\,\mathrm{mm}$. Two numbers decide that story: how fast it swings, set by the spring against the mass, and how quickly the swings die, set by the damper against both.

Put the three elements of §2–§4 together — a mass, a spring, a damper — and the free-body diagram of §2 gives the equation every oscillating thing in robotics obeys,

$$m\ddot y+b\dot y+ky=F$$

because the spring's force opposes the deflection and the damper's its rate, while the push drives both. [[02-foundations/engineering-math|0.5 §8]] solves it: a particular solution, the constant $y_{ss}=F/k$ at which the spring alone balances the push, plus a homogeneous part built from exponentials $e^{st}$. Substituting $e^{st}$ into the equation with $F=0$ divides out the exponential and leaves the characteristic equation

$$ms^2+bs+k=0\quad\Longrightarrow\quad s=\frac{-b\pm\sqrt{b^2-4mk}}{2m}$$

so everything the free response can do is decided by the sign of $b^2-4mk$: complex roots ring, real roots creep. Two numbers summarize it. The first is the **natural frequency** $\omega_n=\sqrt{k/m}$, the rate at which the mass would oscillate with no damper at all, defined with the three regimes in [[02-foundations/engineering-math|0.5 §8]]. For P3 in its wall it is $\sqrt{400/0.04}=100\,\mathrm{rad/s}$, which is $15.9\,\mathrm{Hz}$ and a period of $62.8\,\mathrm{ms}$. The second decides the regime.

> **Damping ratio and critical damping, defined.** The **damping ratio** $\zeta$ is a *dimensionless number of a mass–spring–damper*: its actual damping divided by the **critical damping** $b_c$, the least damping at which it no longer oscillates. Three defining conditions. It belongs to a **linear second-order system with both a mass and a spring**, $m>0$ and $k>0$ — a mass on a damper with no spring has no $\zeta$. The critical value is where the two roots of $ms^2+bs+k=0$ **stop being complex**, the discriminant $b^2-4mk$ reaching zero, so $b_c=2\sqrt{km}$. And the ratio sorts the response into the three regimes of [[02-foundations/engineering-math|0.5 §8]]: $0<\zeta<1$ rings inside a decaying envelope, $\zeta=1$ returns fastest of all without crossing, $\zeta>1$ creeps back on two real roots.
>
> $$\zeta=\frac{b}{b_c}=\frac{b}{2\sqrt{km}},\qquad s_{1,2}=-\zeta\omega_n\pm\omega_n\sqrt{\zeta^2-1}$$
>
> where $b$ is the damping coefficient, $k$ the stiffness, $m$ the mass and $s_{1,2}$ the two roots whose exponentials $e^{st}$ make up the free response — the second form follows from the first by dividing the characteristic equation by $m$ and writing $b/m=2\zeta\omega_n$ and $k/m=\omega_n^2$.
> - **Example**: P3 in its wall: $b_c=2\sqrt{400\cdot0.04}=8.0\,\mathrm{N{\cdot}s/m}$, so its own $b=0.8$ gives $\zeta=0.8/8=0.10$. Gripped, $b_c=2\sqrt{800\cdot0.04}=11.3$ and $b+b_h=8.8$ give $\zeta=0.78$. The hand's own $b_h=8\,\mathrm{N{\cdot}s/m}$ happens to be exactly the bare handle's critical damping.
> - **Non-example**: "critical damping settles fastest." It is the fastest return *without overshoot*. Into a $2\%$ band the lab's $\zeta=0.78$ row settles in $36.1\,\mathrm{ms}$ against $58.3\,\mathrm{ms}$ at $\zeta=1$, because a response allowed to overshoot by up to the band's width gets there sooner (§10).
> - **Why it matters**: one number, from $m$, $b$ and $k$ alone, predicts whether a contact rings, and it is the number [[04-robotics/control-theory-ce397|5. Control Theory §5]] turns into overshoot and settling time and [[04-robotics/force-compliance-control|13. §2]] asks a target impedance to have.

P3 shows all three regimes with the wall at $400\,\mathrm{N/m}$ and only $b$ changed:

| $b$ ($\mathrm{N{\cdot}s/m}$) | $\zeta$ | roots $s_{1,2}$ ($\mathrm{s^{-1}}$) | what the handle does |
|---:|---:|---|---|
| $0.8$ | $0.10$ | $-10\pm99.5j$ | rings at $99.5\,\mathrm{rad/s}$, a period of $63.1\,\mathrm{ms}$, inside an envelope $e^{-10t}$ |
| $8.0$ | $1.00$ | $-100$, $-100$ | the fastest return without crossing $y_{ss}$ |
| $16.0$ | $2.00$ | $-26.8$, $-373.2$ | creeps back on the slow root; the fast one has fallen to $2.4\%$ within $10\,\mathrm{ms}$ |

**The step response and its overshoot.** For $0<\zeta<1$, starting at rest at $y=0$, 0.5 §8's recipe with $y(0)=\dot y(0)=0$ gives

$$y(t)=y_{ss}\Big[1-e^{-\zeta\omega_nt}\Big(\cos\omega_dt+\frac{\zeta}{\sqrt{1-\zeta^2}}\sin\omega_dt\Big)\Big],\qquad \omega_d=\omega_n\sqrt{1-\zeta^2}$$

because the complex roots $-\zeta\omega_n\pm j\omega_d$ turn $e^{st}$ into a decaying cosine and sine by Euler's formula, and the two constants in front of them are fixed by the starting position and velocity. Its velocity, $\dot y=y_{ss}\,\omega_n(1-\zeta^2)^{-1/2}e^{-\zeta\omega_nt}\sin\omega_dt$, first returns to zero at $t_p=\pi/\omega_d$, where the cosine is $-1$ and the sine $0$, so the first peak is

$$y_{\max}=y_{ss}\big(1+e^{-\pi\zeta/\sqrt{1-\zeta^2}}\big)$$

and the **overshoot**, the peak's excess over $y_{ss}$ as a fraction of it, is $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ — a function of $\zeta$ alone. For the bare handle $M_p=0.729$ at $t_p=\pi/99.5=31.6\,\mathrm{ms}$. The **2% settling time** $t_s$ is the time after which the response stays within $\pm2\%$ of $y_{ss}$; both numbers are what the lab of §10 prints, and [[04-robotics/control-theory-ce397|5. Control Theory §5]] reads them off a plot.

The envelope $e^{-\zeta\omega_nt}$ has a rate, and its reciprocal is the page's last definition for the handle.

> **Time constant, defined.** A **time constant** $\tau$ is a *time*: the reciprocal of the decay rate of an exponential, the time over which it falls by a factor $e$. Three defining conditions. The quantity — a response, or the envelope of an oscillating one — **decays as $e^{-t/\tau}$**. In one $\tau$ it covers $1-e^{-1}=63\%$ of its way to the final value, and in $\ln50=3.9$ time constants it comes within $2\%$ of it. And when several decaying terms are present, the one that governs the approach to rest is the **slowest**, $\tau=1/|\mathrm{Re}\,s_{\text{slow}}|$, since the faster terms have died out first.
>
> $$\tau=\frac{1}{|\mathrm{Re}\,s_{\text{slow}}|}:\qquad \tau=\frac mb\ \ (k=0),\qquad \tau=\frac{1}{\zeta\omega_n}=\frac{2m}{b}\ \ (0<\zeta\le1),\qquad \tau=\frac{1}{\omega_n\big(\zeta-\sqrt{\zeta^2-1}\big)}\ \ (\zeta>1)$$
>
> where $s_{\text{slow}}$ is the root nearest zero, because the slowest term is the last to die out: the first case is the mass and damper alone (§4), the second the envelope of a ringing or critically damped response, and the third the slower of two real roots.
> - **Example**: P3 coasting free, $\tau=m/b=50\,\mathrm{ms}$. In its wall, the envelope has $\tau=2m/b=100\,\mathrm{ms}$, and $3.9\tau=391\,\mathrm{ms}$ estimates the $384\,\mathrm{ms}$ the lab finds for its $2\%$ settling. Critically damped, $\tau=1/\omega_n=10\,\mathrm{ms}$.
> - **Non-example**: the period. The bare handle rings with a period of $63.1\,\mathrm{ms}$ and decays with $\tau=100\,\mathrm{ms}$ — two separate numbers. Stiffening the wall shortens the period and leaves $2m/b$ alone, as the problem set's Do item shows.
> - **Why it matters**: it is what a settling time is made of — [[04-robotics/control-theory-ce397|5. Control Theory §5]] uses $4/(\zeta\omega_n)$ — and it is how [[04-robotics/actuators-drives|10.5 §5]] compares a motor's electrical and mechanical speeds.

A ringing trace also measures its own damping: tap the handle in its wall, read two successive peaks, and $\zeta$ follows. The note below shows how; it is a first case of system identification.

> [!note]- Deeper · 더 깊이
> **Reading $\zeta$ off a trace.** Successive peaks of a ringing response exceed $y_{ss}$ by amounts that shrink by the same factor every period, $e^{2\pi\zeta/\sqrt{1-\zeta^2}}$, since the envelope decays by $e^{-\zeta\omega_n\cdot2\pi/\omega_d}$ in one. The bare handle's peaks sit $0.729$, $0.388$, $0.206$ and $0.110\,\mathrm{mm}$ above its final $1\,\mathrm{mm}$, each $1.880$ times the next; $\ln1.880=0.631=2\pi\zeta/\sqrt{1-\zeta^2}$ returns $\zeta=0.10$. Tapping the handle in its wall and reading two peaks therefore measures the device's damping — a first case of estimating a model's parameters from its measured response, the subject of [[04-robotics/system-identification|5.5 System Identification]].

### 6. Work, energy and power

Following the forces instant by instant, as §5 did, gives the path of a motion but not its bill: how much work went in, how much is stored and how much became heat. Energy keeps that account, and it answers some questions — how much a damper takes, how hard a bounce comes back — without solving anything.

The **work** a force does on a body is the integral of the force along the path, $W=\int\vec F\cdot d\vec x$, and the **kinetic energy** of a mass $m$ moving at speed $v$ is $\tfrac12mv^2$; the work–energy theorem says the net work done on a body equals the change in its kinetic energy. A spring's force can be undone: the work it does depends only on where it starts and ends, so it has a **potential energy**, $\tfrac12ky^2$ for a spring measured from its free length, as gravity has $mgh$. OpenStax calls such forces conservative — their work around any closed path is zero — and a damper's or friction's non-conservative, since the energy they take cannot be got back.

> **Mechanical power and work, defined.** **Power** is a *rate*: the rate at which a force, or a torque, transfers energy to the body it acts on; **work** is the energy so transferred over an interval, the time integral of power. Three defining conditions. It pairs a force with the **velocity of the point where that force acts**, counting only the **aligned component** — a dot product — so a force across the motion does no work. Its **sign** says which way the energy goes: positive into the body, negative out of it. And for a **torque on a turning body** the pair is torque and angular velocity.
>
> $$P=\vec F\cdot\vec v=\tau\,\omega,\qquad W=\int P\,dt=\int\vec F\cdot d\vec x$$
>
> where $P$ is in watts, $\vec F$ the force and $\vec v$ the velocity of its point of application, $\tau$ the torque and $\omega$ the angular velocity about the same axis, and $W$ in joules — the second form of $W$ follows from $d\vec x=\vec v\,dt$.
> - **Example**: P2's shoulder turning up at $1\,\mathrm{rad/s}$ at the catalog pose while supplying its $19.62\,\mathrm{N{\cdot}m}$: $P=\tau\omega=19.62\,\mathrm{W}$. Check it on the masses: both sit on the horizontal $1\,\mathrm{m}$ from the axis, so both rise at $1\,\mathrm{m/s}$, and gravity's energy grows at $2\cdot9.81\cdot1=19.62\,\mathrm{W}$ — the same number from the other end.
> - **Non-example**: "holding the arm up costs power." With $\omega=0$ the mechanical power is zero and the arm gains no energy; the $6.01\,\mathrm{W}$ that 10.5's motor burns to hold P2 there (10.5's Worked case, with [[04-robotics/actuators-drives|10.5 §6]] on why a hold is all heat) is electrical loss in the winding, which a brake would not pay.
> - **Non-example**: the guide's reaction on P3's handle. It is perpendicular to the motion, so $\vec F\cdot\vec v=0$ and it does no work, however large it is.
> - **Why it matters**: power is what a transmission conserves (§9) and what every passivity argument counts — [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]] sets a sampled wall's leak against the damper's $bv^2T$ — and the ratio of power out to power in is a machine's **efficiency**, $\eta=P_{\text{out}}/P_{\text{in}}$, which 10.5 defines for a gearbox.

**The ledger for the pushed handle.** Multiply the equation of motion of §5 by $\dot y$ and integrate from the start: each term becomes the rate of one entry, because $m\ddot y\dot y$ is the derivative of $\tfrac12m\dot y^2$, $k_wy\dot y$ that of $\tfrac12k_wy^2$ and $F\dot y$ that of $Fy$ for a steady $F$. So at every instant

$$F\,y=\tfrac12m\dot y^2+\tfrac12k_wy^2+\int_0^tb\,\dot y^2\,dt'$$

where the left side is the work the push has done, and the right side the kinetic energy, the spring's energy and the heat the damper has made so far. At the first peak the push has done $0.4\times1.729\times10^{-3}=0.692\,\mathrm{mJ}$ of work, the wall holds $\tfrac12\cdot400\cdot(1.729\times10^{-3})^2=0.598\,\mathrm{mJ}$ and the damper has taken $0.094\,\mathrm{mJ}$. At the end, $\dot y=0$ and $y=F/k_w$, so the work is $F^2/k_w=0.4\,\mathrm{mJ}$ and the spring holds $F^2/(2k_w)=0.2\,\mathrm{mJ}$: **the damper takes exactly half of the push's work, whatever $b$ is**, provided $b>0$ so that the motion dies out. The coefficient decides how fast and in how many swings the bill is paid, never how large it is — the lab of §10 shows it row by row.

**A bounce.** The handle arriving at the wall's surface at $0.1\,\mathrm{m/s}$ carries $\tfrac12\cdot0.04\cdot0.1^2=0.2\,\mathrm{mJ}$. Without its damper, the wall would absorb that at the depth where $\tfrac12k_wy^2=0.2\,\mathrm{mJ}$, which is $v\sqrt{m/k_w}=1\,\mathrm{mm}$, and throw it back out at full speed. With the damper, the free response of §5 started from $y=0$ at speed $v_0$ is $y=(v_0/\omega_d)\,e^{-\zeta\omega_nt}\sin\omega_dt$; it reaches only $0.863\,\mathrm{mm}$ and returns to the surface after half a damped period, $31.6\,\mathrm{ms}$, where the sine is zero again, at $0.1\times0.729=0.0729\,\mathrm{m/s}$ — the same factor $e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ as the overshoot. It keeps $0.729^2=53\%$ of its energy, and its damper, which keeps acting outside the wall, takes the rest over the next $0.0729\cdot0.05=3.6\,\mathrm{mm}$ of glide. Where the damping sits is part of the model, as the note below shows.

> [!note]- Deeper · 더 깊이
> **The same damper inside the wall.** [[06-research-practice/simulators-benchmarks-datasets|7. Simulators §3]]'s drop cell removes the device damper and puts the same $0.8\,\mathrm{N{\cdot}s/m}$ inside the wall's force law instead. That law lets go of the handle as soon as the contact force reaches zero, a little before the handle is back at the surface, because on the way out the damping term already pulls the force down; the damper cannot tug the handle back, and the bounce keeps an energy ratio of $0.554$ rather than $0.729^2=0.532$. Same $k$, same damping coefficient, same $\zeta$: two contact models, two answers.

**Rotation and efficiency.** A torque does work at the rate $\tau\omega$, as the box's example on P2 shows, and no real transmission passes all of it: through the $\eta=0.80$ gearbox 10.5 freezes for P2's joints, lifting at $1\,\mathrm{rad/s}$ takes $19.62/0.8=24.5\,\mathrm{W}$ at the motor, and $4.9\,\mathrm{W}$ becomes heat in the gears.

### Worked case · 대상으로 한 번 끝까지

One situation, carried from the free-body diagram to the energy ledger on the catalog numbers. P3's handle rests on its wall's surface, $y=0$, and at $t=0$ the steady push $F=0.4\,\mathrm{N}$ starts. Where does the handle end up, how does it get there, and what does the damper take? Then the same end point reached through a gripping hand. Seven steps; the lab of §10 recomputes the response numbers.

**Step 1 — the law.** The free-body diagram of §2 gives, because the push, the wall and the damper are the only forces along the axis,

$$m\ddot y+b\dot y+k_wy=F:\qquad 0.04\,\ddot y+0.8\,\dot y+400\,y=0.4$$

in newtons, valid while the handle is in the wall. It never leaves it: the lowest point after the first peak is $y_{ss}(1-M_p^2)=0.468\,\mathrm{mm}$ (Step 4 gives $M_p$), so the wall's one-sided switch never opens and the equation is linear throughout.

**Step 2 — where it ends.** At rest $\ddot y=\dot y=0$, and the equation loses its first two terms because a still handle needs no force to accelerate and meets none from its damper, so the wall alone balances the push:

$$y_{ss}=\frac{F}{k_w}=\frac{0.4}{400}=1.0\times10^{-3}\,\mathrm{m}$$

one millimetre into the wall, at $x=0.031\,\mathrm{m}$, with $0.4\,\mathrm{N}$ on the wall — a statics answer that does not depend on $m$ or $b$ at all.

**Step 3 — how fast, and how damped.** From §5, $\omega_n=\sqrt{k_w/m}=\sqrt{400/0.04}=100\,\mathrm{rad/s}$, the critical damping is $b_c=2\sqrt{k_wm}=2\sqrt{16}=8.0\,\mathrm{N{\cdot}s/m}$, and, because the damping ratio is the actual damping over the critical one,

$$\zeta=\frac{b}{b_c}=\frac{0.8}{8.0}=0.10$$

so the handle is underdamped: it rings, at $\omega_d=100\sqrt{1-0.01}=99.5\,\mathrm{rad/s}$, a period of $63.1\,\mathrm{ms}$.

**Step 4 — the first peak.** The velocity first returns to zero at $t_p=\pi/\omega_d=\pi/99.5=31.6\,\mathrm{ms}$, and because a peak is where the velocity is zero, §5's overshoot formula applies there and gives

$$M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}=e^{-0.3157}=0.729,\qquad y_{\max}=1.729\,\mathrm{mm}$$

so the wall pushes back $400\times1.729\times10^{-3}=0.692\,\mathrm{N}$ — $73\%$ more than the push — and, the damper being silent at $\dot y=0$, the handle accelerates at $(0.4-0.6917)/0.04=-7.29\,\mathrm{m/s^2}$: the free-body diagram of the picture.

**Step 5 — how long.** The envelope's time constant is $\tau=2m/b=2\cdot0.04/0.8=0.1\,\mathrm{s}$, and it falls inside $2\%$ after $\ln50\cdot\tau=0.391\,\mathrm{s}$. The exact last exit from the $2\%$ band, which the lab finds, is $0.384\,\mathrm{s}$ — about six periods of ringing for a push that ends one millimetre deep.

**Step 6 — the ledger.** When it has settled, the push has done $Fy_{ss}=0.4\times10^{-3}=0.4\,\mathrm{mJ}$ of work, the wall holds $\tfrac12k_wy_{ss}^2=\tfrac12\cdot400\cdot10^{-6}=0.2\,\mathrm{mJ}$, and the damper has turned the other $0.2\,\mathrm{mJ}$ into heat. At the first peak the same ledger read $0.692$ in, $0.598$ stored and $0.094\,\mathrm{mJ}$ dissipated, with the handle momentarily still (§6).

**Step 7 — the hand grips.** Now let a hand hold the handle, aiming at $x_d=0.032\,\mathrm{m}$, $2\,\mathrm{mm}$ past the surface, with the catalog's $k_h=400\,\mathrm{N/m}$ and $b_h=8\,\mathrm{N{\cdot}s/m}$, the handle again starting at rest on the surface. Because the hand's spring and damper act on the handle's own motion — in parallel with the wall and the device (§3) — the free-body diagram gains their two terms and gives

$$m\ddot y+(b+b_h)\dot y+(k_w+k_h)\,y=k_h(x_d-x_w):\qquad 0.04\,\ddot y+8.8\,\dot y+800\,y=0.8$$

where the right side is the hand's pull at $y=0$, $400\times0.002=0.8\,\mathrm{N}$. It ends at $y_{ss}=0.8/800=1.0\,\mathrm{mm}$ — the same point, with $0.4\,\mathrm{N}$ on the wall and $0.4\,\mathrm{N}$ from the hand, 24.4's equilibrium — but it gets there differently: $\omega_n=\sqrt{800/0.04}=141.4\,\mathrm{rad/s}$, $b_c=2\sqrt{800\cdot0.04}=11.3\,\mathrm{N{\cdot}s/m}$ and $\zeta=8.8/11.31=0.78$, so it overshoots only $2.05\%$, to $1.020\,\mathrm{mm}$ and $0.408\,\mathrm{N}$, and is inside the $2\%$ band for good at $37.0\,\mathrm{ms}$, just after its peak at $35.3\,\mathrm{ms}$ pokes out of it. The hand's spring gives up $\tfrac12\cdot400\cdot(0.002^2-0.001^2)=0.6\,\mathrm{mJ}$, the wall stores $0.2$, and $0.4\,\mathrm{mJ}$ is dissipated. Both dampers see the same $\dot y$, so they split that bill in proportion to their coefficients: the device's takes $b/(b+b_h)=0.8/8.8=9.1\%$, and the hand $91\%$.

**What the case says.** The handle alone is a lightly damped oscillator: pushed with $0.4\,\mathrm{N}$, it hits the wall with $0.692\,\mathrm{N}$ and rings for a third of a second, and nothing in the statics answer — $1\,\mathrm{mm}$, $0.4\,\mathrm{N}$ — gives that away; only $\zeta$ does. A grip changes the dynamics and leaves the end point where it was, and it does nine-tenths of the damping — which is why [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]] will not let a virtual wall's stability be credited to the person holding it.

### 7. Rotation: torque, moment of inertia and angular momentum

A robot's joints turn rather than slide, so the laws above must be rewritten for rotation: what twists a joint, and what resists its angular acceleration. A body turning about a fixed axis obeys the rotational twin of each law above: torque plays force, the moment of inertia plays mass, and angular velocity plays velocity. For a rigid body about a fixed axis, OpenStax writes Newton's second law as

$$\sum\tau=I\,\alpha$$

where $\alpha=\ddot\theta$ is the angular acceleration in $\mathrm{rad/s^2}$ — because each bit of mass $dm$ at distance $r$ from the axis accelerates at $r\alpha$ along its circle, needs a tangential force $dm\,r\alpha$, and so a torque $r\cdot dm\,r\alpha$, and adding those up over the body gives $\big(\int r^2dm\big)\alpha$. The two quantities in it get a definition each.

> **Torque, defined.** The **torque**, or moment, of a force about a point is a *vector*: the force's tendency to turn a body about that point, the rotational counterpart of the force itself. Three defining conditions. It is taken **about a stated point** or axis, and changes when the point does. It is the cross product of the **position vector** $\vec r$, from that point to where the force acts, with the force, so only the component of the force perpendicular to $\vec r$ turns anything, and its size is the force times its **lever arm** $r_\perp$, the perpendicular distance from the axis to the force's line of action. And in the plane its **sign** follows the right-hand rule: counterclockwise is positive.
>
> $$\vec\tau=\vec r\times\vec F,\qquad \tau_z=r_xF_y-r_yF_x=\pm F\,r_\perp$$
>
> where $\tau_z$ is the component along the axis out of the plane, in $\mathrm{N{\cdot}m}$, and $r_\perp=r\sin\theta$ with $\theta$ the angle between $\vec r$ and $\vec F$ — the middle form is the cross product written out for two plane vectors, because for vectors in the plane only the component out of the plane survives.
> - **Example**: P2 at its catalog pose, about the shoulder. Each $1\,\mathrm{kg}$ mass weighs $9.81\,\mathrm{N}$ and sits $1\,\mathrm{m}$ to the right of the axis, so the weights' torque is $\tau_z=1\cdot(-9.81)+1\cdot(-9.81)=-19.62\,\mathrm{N{\cdot}m}$, clockwise; the shoulder must supply $+19.62\,\mathrm{N{\cdot}m}$ to hold the arm. About the elbow, the tip's weight acts along a vertical line through the elbow itself, $r_\perp=0$, and the elbow needs nothing.
> - **Non-example**: "torque is weight times link length." At $\theta=(30^\circ,90^\circ)$ the links are still $1\,\mathrm{m}$ long, but the lever arms are the horizontal distances $\cos30^\circ=0.866$ and $\cos30^\circ-\sin30^\circ=0.366\,\mathrm{m}$, so the weights' torque is $9.81\,(0.866+0.366)=12.09\,\mathrm{N{\cdot}m}$, not $19.62$.
> - **Why it matters**: joints are driven, sensed and limited in torque, and the gravity term of the manipulator equation ([[02-foundations/manipulator-kinematics-dynamics|10. §5]]) is this sum taken over every link at every pose.

> **Moment of inertia, defined.** The **moment of inertia** $I$ of a body about an axis is a *scalar property of how its mass is spread around that axis* — the rotational counterpart of mass, the $I$ in $\sum\tau=I\alpha$. Three defining conditions, and one rule for moving the axis. It is taken **about a stated axis**, and a different axis gives a different number. Each bit of mass counts with the **square of its perpendicular distance** to that axis, not with its distance along a link. The body must be **rigid** about that axis, its distances fixed while it turns — for P2, the elbow locked. And the rule for moving the axis is the **parallel-axis theorem**: about any axis parallel to one through the centre of mass, add the whole mass times the square of the distance between the two axes.
>
> $$I=\sum_im_i\,r_i^2=\int r^2\,dm,\qquad I_{\text{axis}}=I_{\text{cm}}+m\,d^2$$
>
> where $r_i$ is the perpendicular distance of mass $m_i$ from the axis, $I_{\text{cm}}$ the moment of inertia about the parallel axis through the centre of mass and $d$ the distance between the two axes, in $\mathrm{kg{\cdot}m^2}$ — the theorem holding because, measured from the centre of mass, the first moment $\int\vec r\,dm$ is zero, so the cross term drops out of $\int|\vec r+\vec d|^2dm$.
> - **Example**: P2, elbow locked at $90^\circ$, about the shoulder: the elbow mass is $1\,\mathrm{m}$ away and the tip mass $\sqrt2\,\mathrm{m}$, so $I=1\cdot1^2+1\cdot(\sqrt2)^2=3\,\mathrm{kg{\cdot}m^2}$ — the entry $M_{11}=3$ that [[02-foundations/manipulator-kinematics-dynamics|10. §3]] derives. The point mass at the tip is the parallel-axis theorem with $I_{\text{cm}}=0$ and $d=\sqrt2\,\mathrm{m}$.
> - **Non-example**: the same arm built from uniform $1\,\mathrm{kg}$, $1\,\mathrm{m}$ rods. By the theorem, link 1 gives $\tfrac1{12}+0.5^2=\tfrac13$ and the forearm $\tfrac1{12}+1.25=\tfrac43\,\mathrm{kg{\cdot}m^2}$, so $I=1.667$, not $3$: the same two kilograms, spread nearer the axis, are $44\%$ easier to swing. Mass alone does not say how hard a body is to turn.
> - **Why it matters**: it sets how much torque an angular acceleration costs, it is what a gear multiplies by $n^2$ (§9), and for a jointed arm it grows into the configuration-dependent mass matrix of [[02-foundations/manipulator-kinematics-dynamics|10. §3]].

The two definitions measure distance differently, and the difference is the whole of the picture below: the moment of inertia uses each mass's distance *from the axis*, the torque of a weight its *horizontal* distance from it.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="P2 with its elbow locked at 90 degrees, at the catalog pose and turned 30 degrees about the shoulder. At the catalog pose both 9.81 N weights hang 1 m from the shoulder's vertical line, so the holding torque is 19.62 N·m, and the tip's weight passes through the elbow, so the elbow needs none; the tip is root 2 m from the shoulder and the moment of inertia is 3 kg·m². Turned 30 degrees the lever arms shrink to 0.866 m and 0.366 m and the holding torque to 12.09 N·m, while the distances, and so the moment of inertia, are unchanged.">
  <defs><marker id="bmB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="54.0" y1="214.0" x2="60.0" y2="208.0"/><line x1="62.0" y1="214.0" x2="68.0" y2="208.0"/><line x1="70.0" y1="214.0" x2="76.0" y2="208.0"/><line x1="78.0" y1="214.0" x2="84.0" y2="208.0"/><line x1="86.0" y1="214.0" x2="92.0" y2="208.0"/><line x1="52.0" y1="208.0" x2="88.0" y2="208.0"/><line x1="314.0" y1="214.0" x2="320.0" y2="208.0"/><line x1="322.0" y1="214.0" x2="328.0" y2="208.0"/><line x1="330.0" y1="214.0" x2="336.0" y2="208.0"/><line x1="338.0" y1="214.0" x2="344.0" y2="208.0"/><line x1="346.0" y1="214.0" x2="352.0" y2="208.0"/><line x1="312.0" y1="208.0" x2="348.0" y2="208.0"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.6" fill="none">
    <line x1="70" y1="200" x2="70" y2="72"/><line x1="70" y1="200" x2="170" y2="100"/>
    <line x1="330" y1="252" x2="330" y2="150"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" opacity="0.7">
    <line x1="416.6" y1="196" x2="416.6" y2="230"/><line x1="366.6" y1="110" x2="366.6" y2="248"/>
  </g>
  <g stroke="currentColor" stroke-width="3" stroke-linecap="round">
    <line x1="70.0" y1="200.0" x2="170.0" y2="200.0"/><line x1="170.0" y1="200.0" x2="170.0" y2="100.0"/>
    <line x1="330.0" y1="200.0" x2="416.6" y2="150.0"/><line x1="416.6" y1="150.0" x2="366.6" y2="63.4"/>
  </g>
  <g fill="currentColor"><circle cx="170.0" cy="200.0" r="7"/><circle cx="170.0" cy="100.0" r="7"/><circle cx="416.6" cy="150.0" r="7"/><circle cx="366.6" cy="63.4" r="7"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="70" cy="200" r="5"/><circle cx="330" cy="200" r="5"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <polyline points="170,209 170,246" marker-end="url(#bmB)"/><polyline points="170,109 170,146" marker-end="url(#bmB)"/>
    <polyline points="416.6,159 416.6,194" marker-end="url(#bmB)"/><polyline points="366.6,72 366.6,108" marker-end="url(#bmB)"/>
    <path d="M 58.5 183.6 A 20 20 0 0 0 58.5 216.4" marker-end="url(#bmB)"/><path d="M 318.5 183.6 A 20 20 0 0 0 318.5 216.4" marker-end="url(#bmB)"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.1">
    <polyline points="120,80 72,80" marker-end="url(#bmB)"/><polyline points="120,80 168,80" marker-end="url(#bmB)"/>
    <polyline points="373.3,230 332,230" marker-end="url(#bmB)"/><polyline points="373.3,230 414.6,230" marker-end="url(#bmB)"/>
    <polyline points="348.3,248 332,248" marker-end="url(#bmB)"/><polyline points="348.3,248 364.6,248" marker-end="url(#bmB)"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18">θ = (0°, 90°), the catalog pose</text>
    <text x="12" y="34">hold τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"> = 9.81·1 + 9.81·1 = 19.62 N·m</tspan></text>
    <text x="12" y="50">I = 1·1² + 1·(√2)² = 3 kg·m²</text>
    <text x="120" y="74" text-anchor="middle">lever arm 1 m for both</text>
    <text x="80" y="140">r = √2 m</text>
    <text x="180" y="100">9.81 N</text>
    <text x="180" y="128">line through the elbow:</text>
    <text x="180" y="142">τ<tspan dy="3" font-size="10">2</tspan><tspan dy="-3"> = 0</tspan></text>
    <text x="176" y="242">9.81 N</text>
    <text x="30" y="192" text-anchor="middle">τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"></tspan></text>
    <text x="290" y="192" text-anchor="middle">τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"></tspan></text>
    <text x="300" y="18">θ = (30°, 90°), elbow still at 90°</text>
    <text x="300" y="34">hold τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"> = 9.81 (0.866 + 0.366) = 12.09 N·m</tspan></text>
    <text x="300" y="50">r still 1 and √2 m: I = 3 kg·m²</text>
    <text x="422.6" y="234">0.866 m</text>
    <text x="372.6" y="252">0.366 m</text>
    <text x="428.6" y="186">9.81 N</text>
    <text x="360.6" y="96" text-anchor="end">9.81 N</text>
  </g>
</svg>

P2 with its elbow locked at $90^\circ$, at the catalog pose and turned $30^\circ$ about the shoulder. Turning the arm leaves the distances from the axis, $1$ and $\sqrt2\,\mathrm{m}$, unchanged, so the moment of inertia stays $3\,\mathrm{kg{\cdot}m^2}$; it shrinks the weights' lever arms from $1$ and $1\,\mathrm{m}$ to $0.866$ and $0.366\,\mathrm{m}$, so the holding torque falls from $19.62$ to $12.09\,\mathrm{N{\cdot}m}$.

The code evaluates both definitions on P2 — the cross product for the torque, the sum of $mr^2$ for the inertia — at the two poses of the picture, and the uniform-rod arm by the parallel-axis theorem.

```python
# P2 with its elbow locked at 90 deg: one rigid body turning about the shoulder axis
g = 9.81
mass = (1.0, 1.0)                                     # kg: point masses at the elbow and at the tip

def points(t1, t2=np.pi/2):
    """Positions (m) of the elbow and tip masses for unit links, angles in rad."""
    elbow = np.array((np.cos(t1), np.sin(t1)))
    return elbow, elbow + np.array((np.cos(t1 + t2), np.sin(t1 + t2)))

def moment(r, f):
    """z-component of r x f in the plane: positive turns counterclockwise."""
    return r[0]*f[1] - r[1]*f[0]

for deg in (0.0, 30.0):
    pts = points(np.radians(deg))
    I = sum(mi*float(p @ p) for mi, p in zip(mass, pts))              # sum of m r^2
    tau = sum(moment(p, (0.0, -mi*g)) for mi, p in zip(mass, pts))    # the weights' moment
    print(f"theta1 = {deg:4.1f} deg: I = {I:.3f} kg*m^2, weights' moment {tau:+.3f} N*m, "
          f"holding torque {-tau:+.3f} N*m")

# the same arm built from uniform 1 kg, 1 m rods, by the parallel-axis theorem
I_cm = 1.0*1.0**2/12                                  # a thin rod about its own centre, kg*m^2
c1, c2 = np.array((0.5, 0.0)), np.array((1.0, 0.5))   # the rods' centres at theta = (0, 90 deg)
I_rods = (I_cm + 1.0*float(c1 @ c1)) + (I_cm + 1.0*float(c2 @ c2))
tau_rods = moment(c1, (0.0, -g)) + moment(c2, (0.0, -g))
print(f"uniform rods: I = {I_rods:.4f} kg*m^2, weights' moment {tau_rods:+.3f} N*m")
```

It prints $I=3.000\,\mathrm{kg{\cdot}m^2}$ at both angles, the weights' moment $-19.620$ and $-12.086\,\mathrm{N{\cdot}m}$ (holding torques $+19.620$ and $+12.086$), and for the rod arm $I=1.6667\,\mathrm{kg{\cdot}m^2}$ and $-14.715\,\mathrm{N{\cdot}m}$: rods also put their weight nearer the shoulder, so they are easier to hold as well as to swing.

**Angular momentum, in one paragraph.** A body turning about a fixed axis at angular velocity $\omega$ carries the **angular momentum** $L=I\omega$, in $\mathrm{kg{\cdot}m^2/s}$, and the net external torque is its rate of change, $\sum\tau=dL/dt$ — the rotational form of $\sum F=dp/dt$, as OpenStax states it. P2 swinging about its shoulder at $1\,\mathrm{rad/s}$ with the elbow locked carries $L=3\times1=3\,\mathrm{kg{\cdot}m^2/s}$ and $\tfrac12I\omega^2=1.5\,\mathrm{J}$; stopping it in $0.5\,\mathrm{s}$ takes an average $3/0.5=6\,\mathrm{N{\cdot}m}$ on top of whatever holds it against gravity. Momentum is what makes a heavy machine hard to stop — the reason [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]] treats the inertia of S2, the construction track's 5-tonne trench excavator ([[05-construction-robotics/site-engineering|2.5]]), as a problem of its own — and it is conserved only while no external torque acts, which a fixed-base arm never enjoys.

### 8. Statics: equilibrium and the holding torque

A robot that only holds a pose still has to supply whatever torque gravity demands at every joint, and statics is how that torque is computed. Statics is §2 and §7 with every acceleration set to zero. OpenStax states the two conditions for a body at rest as

$$\sum\vec F=0,\qquad \sum\vec\tau=0\ \ \text{about any point}$$

because a body at rest has $\vec a=0$ and $\alpha=0$; and the torque sum may be taken about whatever point is convenient, since once the forces sum to zero, moving the reference point by $\vec d$ changes the total torque by $-\vec d\times\sum\vec F=0$. The robotics pages need one product of this section above all: the **holding torque**, the torque a joint must supply to keep a pose against gravity.

**P2 at its catalog pose.** Draw the whole arm as one free body: the two weights, $9.81\,\mathrm{N}$ each, downward at $(1,0)$ and $(1,1)$; the base's force $\vec R$ on the arm at the shoulder; and the shoulder motor's torque $\tau_1$ on link 1. The force balance gives $R_y=2\cdot9.81=19.62\,\mathrm{N}$ upward, and the torque balance about the shoulder gives $\tau_1-9.81\cdot1-9.81\cdot1=0$, so $\tau_1=+19.62\,\mathrm{N{\cdot}m}$, counterclockwise. The check about another point costs one line: about the elbow, $R_y$ acts $1\,\mathrm{m}$ to its left and contributes $(0-1)\cdot19.62=-19.62\,\mathrm{N{\cdot}m}$, both weights act on lines through the elbow and contribute nothing, and $\tau_1$ — a couple, the same about every point — contributes $+19.62$: zero, as it must be. The forearm alone is a free body too: its weight, $9.81\,\mathrm{N}$ at the tip, and the elbow's $9.81\,\mathrm{N}$ upward on it act along one vertical line, so the elbow's holding torque is $\tau_2=0$.

**Over the pose.** With the elbow held at $90^\circ$ and the shoulder at $\theta_1$, the elbow mass sits at a horizontal distance $\cos\theta_1$ from the shoulder and the tip mass at $\cos\theta_1-\sin\theta_1$, and because each weight's torque is $9.81\,\mathrm{N}$ times its horizontal distance,

$$\tau_1(\theta_1)=9.81\,\big(2\cos\theta_1-\sin\theta_1\big)\ \mathrm{N{\cdot}m}$$

which is $19.62$ at $\theta_1=0$, $12.09$ at $30^\circ$ (the code of §7), and largest where its derivative $-9.81\,(2\sin\theta_1+\cos\theta_1)$ is zero: $\tan\theta_1=-\tfrac12$, $\theta_1=-26.57^\circ$, where $\tau_1=9.81\sqrt5=21.94\,\mathrm{N{\cdot}m}$. A joint sized for the catalog pose alone is $11\%$ short of the worst one, and [[04-robotics/actuators-drives|10.5]] checks its drive at both.

**A load at the tip.** A payload hanging from the tip adds its weight times its lever arm. Were P2 to hold the construction track's facade panel, S1's $20\,\mathrm{kg}$ ([[05-construction-robotics/site-engineering|2.5]]), at its tip in the catalog pose, the shoulder would need $19.62+20\cdot9.81\cdot1=215.8\,\mathrm{N{\cdot}m}$, eleven times its own hold — and the elbow still nothing, because the tip is directly above it. Where a load hangs matters as much as what it weighs.

**P3 held in its wall.** The statics of the gripped handle is the Worked case's Step 7 with the motion gone: the hand's pull $k_h(x_d-x)$ equals the wall's push $k_w(x-x_w)$, which puts the handle at $x=0.031\,\mathrm{m}$ with $0.4\,\mathrm{N}$ on each side — and the hand, by the third law, feels the wall's $0.4\,\mathrm{N}$ through the handle.

### 9. Levers and gears: ratio, torque, speed and reflected inertia

Motors are fast and weak while joints must be slow and strong; a lever or a gear makes that trade, and this section counts what it costs. A **lever** is a rigid bar turning about a pivot. With a force $F_{\text{in}}$ at distance $a$ from the pivot and a load $F_{\text{out}}$ at distance $c$, the torque balance of §8 gives $F_{\text{in}}\,a=F_{\text{out}}\,c$; and because the bar is rigid, the two points move through arcs in the same ratio, $s_{\text{in}}/s_{\text{out}}=a/c$. So

$$\frac{F_{\text{out}}}{F_{\text{in}}}=\frac{a}{c}=\frac{s_{\text{in}}}{s_{\text{out}}},\qquad F_{\text{in}}\,s_{\text{in}}=F_{\text{out}}\,s_{\text{out}}$$

— force is traded for distance, and the work in equals the work out. A pair of gears, or a pulley winding a cable onto a drum, is a lever that keeps turning: the ratio is fixed by the geometry — tooth counts, radii — and the trade is the same, torque multiplied by the ratio and speed divided by it, with the power $\tau\omega$ unchanged when nothing is lost. The **gear ratio** is defined completely, with its two conditions, in [[04-robotics/actuators-drives|10.5 §2]], and the **efficiency** that a real gearbox subtracts from the torque there too; here are the two transmissions of this page's plants.

**P3's capstan.** A motor pulley of radius $r_m=0.010\,\mathrm{m}$ winds a cable onto a sector of radius $r_s=0.050\,\mathrm{m}$, so the sector turns $r_m/r_s=1/5$ as fast as the motor with $5$ times its torque. The handle rides at the sector's rim, so it moves $r_s\theta_s=r_m\theta_m$ and the force on it is $F=\tau_m/r_m$ — the sector radius cancels out of the handle's map, a subtlety [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]] develops. Rendering the wall's $0.4\,\mathrm{N}$ at $1\,\mathrm{mm}$ takes the motor $\tau_m=0.4\cdot0.010=0.004\,\mathrm{N{\cdot}m}$, and that millimetre is $0.001/0.010=0.1\,\mathrm{rad}$, $5.7^\circ$, of motor rotation.

**P2's joint gearbox.** With $n=100$, the catalog hold's $19.62\,\mathrm{N{\cdot}m}$ is $0.1962\,\mathrm{N{\cdot}m}$ at the motor, ideally, and the joint turning at $1\,\mathrm{rad/s}$ spins the motor at $100\,\mathrm{rad/s}$ ($955\,\mathrm{rpm}$), with $19.62\,\mathrm{W}$ flowing through both sides; 10.5 adds the gearbox's loss and needs $0.2453\,\mathrm{N{\cdot}m}$ at the motor.

**What the ratio does to inertia.** A ratio multiplies torque once but inertia twice, and the kinetic energy shows why. A rotor of inertia $J_m$ turning at $\omega_m=n\omega$ stores

$$\tfrac12J_m\,\omega_m^2=\tfrac12J_m(n\omega)^2=\tfrac12\big(n^2J_m\big)\,\omega^2$$

which is the energy of an inertia $n^2J_m$ turning at the joint's own speed — so the joint feels the rotor as $n^2J_m$, its **reflected inertia**, defined in [[04-robotics/actuators-drives|10.5 §4]]. With the rotor 10.5 freezes for P2's drives, $J_m=1.0\times10^{-4}\,\mathrm{kg{\cdot}m^2}$, that is $10^4\cdot10^{-4}=1.0\,\mathrm{kg{\cdot}m^2}$ at the shoulder, a third of the arm's own $I=3$ from a part you cannot see from outside. On P3 the same energy argument with $\omega_m=\dot x/r_m$ gives the rotor's apparent mass at the handle, $J_m/r_m^2$: with the rotor 24.3 freezes for P3, $1.0\times10^{-6}\,\mathrm{kg{\cdot}m^2}$, it is $10^{-6}/10^{-4}=0.010\,\mathrm{kg}$, a quarter of the handle's $0.04\,\mathrm{kg}$.

| Transmission | Ratio | Torque (or force), ideal | Speed | Rotor as felt at the output |
|---|---:|---|---|---|
| P2 joint gearbox | $n=100$ | $\times100$: $0.1962\to19.62\,\mathrm{N{\cdot}m}$ | $\div100$: $100\to1\,\mathrm{rad/s}$ | $n^2J_m=1.0\,\mathrm{kg{\cdot}m^2}$ |
| P3 capstan, motor to handle | $x=r_m\theta_m$ | $F=\tau_m/r_m$: $0.004\,\mathrm{N{\cdot}m}\to0.4\,\mathrm{N}$ | $\dot x=r_m\omega_m$ | $J_m/r_m^2=0.010\,\mathrm{kg}$ |

The trade is the whole design problem of a drive: a larger ratio buys torque in proportion and pays in inertia in proportion to the *square*, and a real gearbox adds friction and backlash on top. 10.5 works that trade on P2's shoulder across ratios from $30$ to $300$, and 24.3 on P3's capstan.

### 10. The lab: the handle pushed into its wall, swept over damping

The Worked case with one knob turned. The handle is pushed from rest into its $400\,\mathrm{N/m}$ wall by the steady $0.4\,\mathrm{N}$, and the damping $b$ takes eight values from P3's own $0.8$ up to $32\,\mathrm{N{\cdot}s/m}$, so that $\zeta$ runs from $0.1$ to $4$; the gripped handle of Step 7 is the last line. The response is §5's closed form evaluated every $10\,\mathrm{\mu s}$ for $1.5\,\mathrm{s}$ — not a simulation, so no integrator stands between the physics and the table; [[02-foundations/lab-kernel|0.7 Lab Kernel]] steps the same equation with Euler's methods. For each row the code prints the damping ratio; the slowest time constant $1/|\mathrm{Re}\,s_{\text{slow}}|$ of §5; the overshoot and the peak force on the wall; the $2\%$ settling time, taken as the first sample after which the depth stays within $\pm2\%$ of $y_{ss}$; and the energy the damper has dissipated by then, $\int b\dot y^2dt$ summed by the trapezoid rule — the Riemann sum of [[02-foundations/engineering-math|0.5 §3]] with each slice's two ends averaged. A last check closes §6's ledger — work in, minus kinetic and spring energy, minus heat — in every row.

```python
import numpy as np

# P3's handle pushed into its virtual wall: catalog m, b, k_w, and this page's steady push F
m, b0, kw, F = 0.04, 0.8, 400.0, 0.4             # kg, N*s/m, N/m, N

def response(m, b, k, F, t):
    """y(t), v(t) of m*y'' + b*y' + k*y = F, starting at rest at y = 0 (closed form, 0.5 §8)."""
    wn, z, yss = np.sqrt(k/m), b/(2*np.sqrt(k*m)), F/k
    if z < 1:                                    # underdamped: a cosine inside a decaying envelope
        wd = wn*np.sqrt(1 - z*z); e = np.exp(-z*wn*t)
        y = yss*(1 - e*(np.cos(wd*t) + z/np.sqrt(1 - z*z)*np.sin(wd*t)))
        v = yss*wn/np.sqrt(1 - z*z)*e*np.sin(wd*t)
    elif z == 1:                                 # critically damped: one repeated real root
        e = np.exp(-wn*t)
        y = yss*(1 - (1 + wn*t)*e); v = yss*wn*wn*t*e
    else:                                        # overdamped: two real roots, one slow and one fast
        r = np.sqrt(z*z - 1); s1, s2 = -wn*(z - r), -wn*(z + r)
        y = yss*(1 + (s2*np.exp(s1*t) - s1*np.exp(s2*t))/(s1 - s2))
        v = yss*s1*s2*(np.exp(s1*t) - np.exp(s2*t))/(s1 - s2)
    return y, v

def metrics(m, b, k, F, t_end=1.5, dt=1e-5):
    """Damping ratio, slowest time constant, overshoot, peak depth, 2 % settling time,
    the energy the damper has dissipated by then, and what is left of the energy ledger."""
    wn, z, yss = np.sqrt(k/m), b/(2*np.sqrt(k*m)), F/k
    tau = 1/(z*wn) if z <= 1 else 1/(wn*(z - np.sqrt(z*z - 1)))    # 1/|slowest root|
    t = np.arange(0.0, t_end, dt)
    y, v = response(m, b, k, F, t)
    over = max(float(y.max()) - yss, 0.0)/yss
    i = int(np.nonzero(np.abs(y - yss) > 0.02*yss)[0][-1]) + 1     # from here on inside +-2 %
    p = b*v[:i + 1]**2                                             # power into the damper, W
    e_diss = float(np.sum(p[1:] + p[:-1]))*dt/2                    # trapezoid rule, J
    ledger = F*y[i] - 0.5*m*v[i]**2 - 0.5*k*y[i]**2 - e_diss       # work in - stored - dissipated
    return z, tau, over, float(y.max()), t[i], e_diss, ledger

print("    b   zeta    tau  overshoot  wall F_peak    t_s  E_diss")
worst = 0.0
for b in (0.8, 2.0, 4.0, 5.6, 6.24, 8.0, 16.0, 32.0):
    z, tau, over, ymax, ts, ed, led = metrics(m, b, kw, F)
    worst = max(worst, abs(led))
    print(f"{b:5.2f} {z:6.2f} {1e3*tau:6.1f} {100*over:9.2f} {kw*ymax:12.3f} {1e3*ts:6.1f} {1e3*ed:7.4f}")
print(f"F^2/(2 k_w) = {1e3*F*F/(2*kw):.4f} mJ; energy ledger closes in every row: {worst < 1e-9}")

# the hand grips: its spring and damper act on the handle's own displacement, so they add
kh, bh, xd, xw = 400.0, 8.0, 0.032, 0.030        # catalog hand, and an aim point 2 mm into the wall
z, tau, over, ymax, ts, ed, led = metrics(m, b0 + bh, kw + kh, kh*(xd - xw))
print(f"gripped: zeta {z:.3f}, tau {1e3*tau:.1f} ms, overshoot {100*over:.2f} %, wall F_peak "
      f"{kw*ymax:.3f} N, t_s {1e3*ts:.1f} ms, dissipated {1e3*ed:.4f} mJ, "
      f"device damper's share {b0/(b0 + bh):.3f}")
```

**The sweep.** Eight damping values on the $400\,\mathrm{N/m}$ wall, everything else frozen; the printed columns, with units:

| $b$ ($\mathrm{N{\cdot}s/m}$) | $\zeta$ | $\tau$ (ms) | overshoot (%) | peak wall force (N) | $t_s$ (ms) | dissipated by $t_s$ (mJ) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.80 | 0.10 | 100.0 | 72.92 | 0.692 | 383.8 | 0.1999 |
| 2.00 | 0.25 | 40.0 | 44.43 | 0.578 | 141.2 | 0.1998 |
| 4.00 | 0.50 | 20.0 | 16.30 | 0.465 | 80.8 | 0.1999 |
| 5.60 | 0.70 | 14.3 | 4.60 | 0.418 | 59.8 | 0.1998 |
| 6.24 | 0.78 | 12.8 | 1.99 | 0.408 | 36.1 | 0.1988 |
| 8.00 | 1.00 | 10.0 | 0.00 | 0.400 | 58.3 | 0.1999 |
| 16.00 | 2.00 | 37.3 | 0.00 | 0.400 | 148.8 | 0.1999 |
| 32.00 | 4.00 | 78.7 | 0.00 | 0.400 | 309.3 | 0.1999 |

The code also prints $F^2/(2k_w)=0.2000\,\mathrm{mJ}$, confirms that the ledger closes in every row, and gives the gripped handle: $\zeta=0.778$, $\tau=9.1\,\mathrm{ms}$, overshoot $2.05\%$, a peak wall force of $0.408\,\mathrm{N}$, $t_s=37.0\,\mathrm{ms}$, $0.3998\,\mathrm{mJ}$ dissipated, and a device-damper share of $0.091$.

**Reading the sweep.** Four things the formulas of §5 and §6 predicted, and one they did not make obvious.

- **Damping buys down the overshoot, and the force spike with it.** From $72.9\%$ at $\zeta=0.1$ to none from $\zeta=1$ on, so the wall's peak force falls from $0.692$ to $0.400\,\mathrm{N}$. A person pressing the bare handle into its wall with $0.4\,\mathrm{N}$ meets $0.692\,\mathrm{N}$ for an instant — the "bounce" a lightly damped wall feels like.
- **The time constant is shortest at critical damping,** $10\,\mathrm{ms}$, and grows on both sides: as $2m/b$ below it, and as the slow root drifts toward zero above it ($37.3$ and $78.7\,\mathrm{ms}$).
- **Settling has a minimum, and it is not at $\zeta=1$.** $383.8\,\mathrm{ms}$ at $\zeta=0.1$ falls to $36.1\,\mathrm{ms}$ at $\zeta=0.78$ and rises again — $58.3$ at $1$, $148.8$ at $2$, $309.3$ at $4$: too little damping rings, too much creeps. The fastest entry into a $2\%$ band belongs to the $\zeta$ whose overshoot just fits inside the band, $1.99\%$ at $0.78$; at $\zeta=0.7$ the $4.60\%$ overshoot leaves the band, has to come back, and costs $59.8\,\mathrm{ms}$. The metric is jumpy there: the gripped handle's $2.05\%$ peak pokes $0.05$ points out of the band and takes $37.0\,\mathrm{ms}$, where a grip giving $\zeta=0.780$ instead of $0.778$ would settle in $25.5\,\mathrm{ms}$. That jump is why [[04-robotics/control-theory-ce397|5. Control Theory §5]] treats $4/(\zeta\omega_n)$ as an estimate rather than a measurement.
- **The damper's bill is the same in every row.** Between $0.1988$ and $0.1999\,\mathrm{mJ}$ by the settling time, against $F^2/(2k_w)=0.2000\,\mathrm{mJ}$ at the end: half of the push's $0.4\,\mathrm{mJ}$, as §6 proved without solving anything. $b$ decides how fast the bill is paid, never its size; the shortfalls are energy still moving at $t_s$, largest in the $\zeta=0.78$ row, which is declared settled while still in motion.
- **The grip.** The last line repeats Step 7: of the $0.4\,\mathrm{mJ}$ the gripped handle dissipates, the device's own damper supplies $9.1\%$.

### 11. What this page does not cover

- **Frequency response and resonance.** How the handle answers a sinusoidal push — a peak near $\omega_n$ that a small $\zeta$ sharpens — is the transfer function of [[04-robotics/control-theory-ce397|5. Control Theory]] and the filters of [[02-foundations/signal-processing|6. Signal Processing]].
- **Stepping the equations in code.** The lab evaluates closed forms. [[02-foundations/lab-kernel|0.7 Lab Kernel]] steps the same equation with Euler's methods, and [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] shows what sampling a wall does to its energy.
- **Many bodies.** A jointed arm's inertia depends on its pose and couples its joints ([[02-foundations/manipulator-kinematics-dynamics|10]]); this page locked P2's elbow to keep one rigid body.
- **Actuators.** Motors, gearbox losses, heat and current limits are [[04-robotics/actuators-drives|10.5]]; electric circuits and fluid power are outside this page, and are its two siblings: [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics §7]] turns this page's torque and power into a motor's current and voltage, and [[02-foundations/fluid-power|0.6.3 Fluid Power §7]] treats an oil column as a spring of §3's kind.
- **Contact and its control.** Contact stiffness, impact and impedance control are [[04-robotics/force-compliance-control|13]], and friction cones and contact modes [[04-robotics/contact-force-tactile|9. Contact, Force & Tactile]].
- **Richer friction.** This page stops at viscous plus Coulomb friction; the bristle models of the LuGre family appear in [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7]].
- **Continuum and structural mechanics.** Stress fields, the vibration of beams and plates, and fatigue belong to structural mechanics; this page uses only a bar's and a cantilever's stiffness. A cantilever camera bracket sized by the tilt it allows and the frequency it rings at — §5's mass on a spring — is [[02-foundations/tools/mechanical-design-fabrication|12.9 Mechanical Design and Fabrication §6]].

### After reading

- [ ] Check an equation's dimensions, and say why a check that passes can still be wrong.
- [ ] Draw a free-body diagram with every external force and nothing else, and write Newton's second law from it.
- [ ] Combine two springs by what they share, series or parallel, and say what a preload changes and what it does not.
- [ ] Tell a viscous damper from Coulomb friction by four behaviours, with numbers.
- [ ] From $m$, $b$ and $k$, compute $\omega_n$, $\zeta$, the time constant, the overshoot and a settling estimate, and name the regime.
- [ ] Close an energy ledger — work in, energy stored, energy dissipated — and say why the damper's share of a steady push is half.
- [ ] Compute a torque, a moment of inertia with the parallel-axis theorem and a holding torque, and carry a torque and an inertia through a gear ratio.

### Self-check

1. P3's damping is $0.8\,\mathrm{N{\cdot}s/m}$. Write it in base SI units, and show that $\zeta=b/(2\sqrt{km})$ is a pure number.
2. A damper cannot hold the handle in its wall. Can friction? Where can §4's friction-only handle come to rest?
3. The hand and the wall act on P3's handle. For the handle's vibration they are in parallel; for the hand's aim they are in series. How can both be true?
4. You push a spring–damper from rest with a steady force until it settles. What fraction of your work does the damper dissipate, and why does the size of $b$ not matter?
5. Why does P2's elbow need no holding torque at the catalog pose, while its shoulder needs $19.62\,\mathrm{N{\cdot}m}$?
6. You double a gearbox's ratio. What happens, ideally, to the output torque, the output speed and the rotor's reflected inertia?

> [!tip]- Answers
> 1. $0.8\,\mathrm{N{\cdot}s/m}=0.8\,(\mathrm{kg\,m\,s^{-2}})\,\mathrm{s}/\mathrm{m}=0.8\,\mathrm{kg/s}$. Then $\zeta$ has dimension $(\mathrm{kg/s})/\sqrt{(\mathrm{kg/s^2})\cdot\mathrm{kg}}=(\mathrm{kg/s})/(\mathrm{kg/s})=1$.
> 2. Yes: static friction supplies any force up to $f_s$, so the handle can rest anywhere within $\pm f_s/k_w=\pm0.125\,\mathrm{mm}$ of the balance point at $1\,\mathrm{mm}$; §4's run stopped at $1.10\,\mathrm{mm}$. A damper's force is zero at rest, so it holds nothing.
> 3. Series and parallel are decided by what the springs share, not by the drawing. For the handle's motion both deflect by the same $y$: parallel, $800\,\mathrm{N/m}$, $\omega_n=141.4\,\mathrm{rad/s}$. For the force the hand produces by moving its aim, the same $0.4\,\mathrm{N}$ passes through both: series, $200\,\mathrm{N/m}$, so the aim sits $2\,\mathrm{mm}$ past the surface.
> 4. Half. At the end the work is $Fy_{ss}=F^2/k$ and the spring holds $F^2/(2k)$, so the other $F^2/(2k)$ went into the damper. $b$ changes only how fast and in how many swings that happens, which the lab shows as a constant $0.2\,\mathrm{mJ}$ column.
> 5. The forearm is vertical, so the tip mass's weight acts along a line through the elbow: its lever arm is zero. About the shoulder both weights act $1\,\mathrm{m}$ from the axis: $2\cdot9.81\cdot1=19.62\,\mathrm{N{\cdot}m}$.
> 6. The torque doubles, the speed halves, and the reflected inertia quadruples, because it goes as $n^2$ (§9): the torque trade is linear and the inertia penalty quadratic.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and the object catalog: P3 and P2 as in the Running object, with this page's push $F=0.4\,\mathrm{N}$ and friction, and the changes each item names.

1. **Draw.** The picture for a stiffer wall, $k_w=1600\,\mathrm{N/m}$, with the bare handle and the same push: the model with the new wall; the free-body diagram at the first peak with each force's value; and the depth against time with the final depth, the first peak (depth, time, wall force), the envelope with its time constant, and the settling time.
2. **Derive.** (a) For the $1600\,\mathrm{N/m}$ wall: $y_{ss}$, $\omega_n$, $b_c$, $\zeta$, $\omega_d$, $t_p$, $M_p$, the peak wall force and the acceleration at the peak, the envelope's time constant, the $\ln50$ settling estimate, and the energy ledger at the end. (b) With this page's friction and no damper, the dead band $\pm f_s/k_w$ on that wall, in micrometres and in P3's $61.4\,\mathrm{\mu m}$ encoder counts, and the step $2f_c/k_w$ by which each half-swing shrinks. (c) P2 carries a $0.5\,\mathrm{kg}$ tool at its tip, a point mass, with the elbow locked at $90^\circ$: its moment of inertia about the shoulder, the holding torques $\tau_1$ and $\tau_2$ at the catalog pose, and the motor torque through an ideal $n=100$ gearbox. (d) At which shoulder angle is the loaded arm's holding torque largest, and how large is it?
3. **Do.** Replace `response` in §10's lab with the template below, fill every `?`, and run the wall-stiffness sweep underneath it at P3's own $b$. Report which columns change with $k_w$ and which do not, and explain from §5 why the time constant is the same in every row while the overshoot grows.

```python
# Tier A template: paste over response() in the lab of §10, fill every ?, then run the sweep below.
def response(m, b, k, F, t):
    wn, z, yss = ?, ?, ?                         # natural frequency, damping ratio, final depth
    if z < 1:
        wd = ?; e = np.exp(-z*wn*t)              # the ringing (damped) frequency
        y = ?                                    # the underdamped step response of §5
        v = yss*wn/np.sqrt(1 - z*z)*e*np.sin(wd*t)
    elif z == 1:
        e = np.exp(-wn*t)
        y = yss*(1 - (1 + wn*t)*e); v = yss*wn*wn*t*e
    else:
        r = np.sqrt(z*z - 1); s1, s2 = -wn*(z - r), -wn*(z + r)
        y = yss*(1 + (s2*np.exp(s1*t) - s1*np.exp(s2*t))/(s1 - s2))
        v = yss*s1*s2*(np.exp(s1*t) - np.exp(s2*t))/(s1 - s2)
    return y, v

print("   k_w   zeta    tau  overshoot  F_peak    t_s  E_diss  F^2/2k")
for k in (100.0, 200.0, 400.0, 800.0, 1600.0):  # the wall-stiffness knob, P3's own damper
    z, tau, over, ymax, ts, ed, led = metrics(m, b0, k, F)
    print(f"{k:6.0f} {z:6.3f} {1e3*tau:6.1f} {100*over:9.1f} {k*ymax:7.3f} {1e3*ts:6.1f} {1e3*ed:7.4f} {?:7.4f}")
```

> [!note]- How to draw it · 그리는 법
> - **The model** keeps the block, the push arrow $F=0.4\,\mathrm{N}$ and the damper $b=0.8\,\mathrm{N{\cdot}s/m}$; only the wall spring's label changes, to $k_w=1600\,\mathrm{N/m}$. Mark the depth $y$ from the wall's surface, positive into the wall.
> - **The free-body diagram at the first peak** has three horizontal forces and nothing else: the push, $0.4\,\mathrm{N}$ into the wall; the wall, $k_wy_{\max}=0.742\,\mathrm{N}$ back; and the damper, zero, because $\dot y=0$ at a peak. No $m\ddot y$ arrow: write $\sum F=0.4-0.7418=-0.3418\,\mathrm{N}$ and $\ddot y=-8.54\,\mathrm{m/s^2}$ beside the diagram instead.
> - **The time plot** starts at $y=0$ with zero slope, since the handle starts at rest. Draw a dotted line at $y_{ss}=0.25\,\mathrm{mm}$ and the first peak at $0.464\,\mathrm{mm}$ and $15.7\,\mathrm{ms}$; later peaks follow every $2\pi/\omega_d=31.5\,\mathrm{ms}$, their excess over $y_{ss}$ shrinking by the factor $e^{2\pi\zeta/\sqrt{1-\zeta^2}}=1.37$ each time.
> - **The envelope** is $y_{ss}\big(1\pm e^{-t/\tau}/\sqrt{1-\zeta^2}\big)$ with $\tau=2m/b=100\,\mathrm{ms}$ — the same time constant as the $400\,\mathrm{N/m}$ wall's, which is the point of the variant: the stiffer wall rings twice as fast inside the same envelope.
> - **The settling mark** goes where the lab puts it, near $380\,\mathrm{ms}$, beside the estimate $\ln50\cdot\tau=391\,\mathrm{ms}$.
> - **Scale** the depth axis to the new numbers: everything is a quarter of the picture's depth, so a copy of the picture's axis would squash the response flat.

> [!tip]- Solutions
> 1. The drawing of item 1 carries the numbers of item 2(a): the final depth $0.25\,\mathrm{mm}$, the first peak $0.464\,\mathrm{mm}$ at $15.7\,\mathrm{ms}$ with $0.742\,\mathrm{N}$ on the wall, the free-body diagram's $0.4\,\mathrm{N}$ in and $0.742\,\mathrm{N}$ back with no damper force, the envelope's $\tau=100\,\mathrm{ms}$ and a settling time near $380\,\mathrm{ms}$. The stiffer wall ends shallower and rings faster and harder — overshoot $85\%$ against $73\%$ — and settles no sooner.
> 2. (a) $y_{ss}=0.4/1600=0.25\,\mathrm{mm}$. $\omega_n=\sqrt{1600/0.04}=200\,\mathrm{rad/s}$ ($31.8\,\mathrm{Hz}$). $b_c=2\sqrt{1600\cdot0.04}=16\,\mathrm{N{\cdot}s/m}$, so $\zeta=0.8/16=0.05$. $\omega_d=200\sqrt{1-0.0025}=199.75\,\mathrm{rad/s}$, $t_p=\pi/199.75=15.7\,\mathrm{ms}$. $M_p=e^{-\pi\cdot0.05/\sqrt{0.9975}}=0.854$, so $y_{\max}=0.464\,\mathrm{mm}$, the wall pushes $1600\cdot0.464\times10^{-3}=0.742\,\mathrm{N}$, and $\ddot y=(0.4-0.7418)/0.04=-8.54\,\mathrm{m/s^2}$. $\tau=2m/b=0.1\,\mathrm{s}$ as before, and $\ln50\cdot\tau=0.391\,\mathrm{s}$ (the Do item's run gives $380.1\,\mathrm{ms}$). Ledger: work $0.4\cdot0.25\times10^{-3}=0.1\,\mathrm{mJ}$, stored $\tfrac12\cdot1600\cdot(0.25\times10^{-3})^2=0.05\,\mathrm{mJ}$, dissipated $0.05\,\mathrm{mJ}$ — half, again. (b) $f_s/k_w=0.05/1600=31.25\,\mathrm{\mu m}$, about half an encoder count, so the encoder cannot even report where in the band the handle stuck; each half-swing shrinks by $2\cdot0.02/1600=25\,\mathrm{\mu m}$. (c) $I=1\cdot1^2+1\cdot(\sqrt2)^2+0.5\cdot(\sqrt2)^2=4\,\mathrm{kg{\cdot}m^2}$. $\tau_1=9.81\,(1+1+0.5)\cdot1=24.525\,\mathrm{N{\cdot}m}$; $\tau_2=0$, since the tool also hangs on the vertical line through the elbow. At the motor, $24.525/100=0.245\,\mathrm{N{\cdot}m}$. (d) With the elbow at $90^\circ$ the elbow mass is $\cos\theta_1$ from the shoulder's vertical and the tip's $1.5\,\mathrm{kg}$ at $\cos\theta_1-\sin\theta_1$, so $\tau_1=9.81\,(2.5\cos\theta_1-1.5\sin\theta_1)$. Its derivative vanishes at $\tan\theta_1=-1.5/2.5=-0.6$, $\theta_1=-30.96^\circ$, where $\tau_1=9.81\sqrt{2.5^2+1.5^2}=28.60\,\mathrm{N{\cdot}m}$ — the worst pose moves $4.4^\circ$ lower than the unloaded arm's $-26.57^\circ$, because the extra mass sits at the tip.
> 3. The blanks: `wn, z, yss = np.sqrt(k/m), b/(2*np.sqrt(k*m)), F/k`, `wd = wn*np.sqrt(1 - z*z)`, `y = yss*(1 - e*(np.cos(wd*t) + z/np.sqrt(1 - z*z)*np.sin(wd*t)))`, and `1e3*F*F/(2*k)` in the last column. The run prints
>
>    | $k_w$ (N/m) | $\zeta$ | $\tau$ (ms) | overshoot (%) | peak wall force (N) | $t_s$ (ms) | dissipated (mJ) | $F^2/(2k_w)$ (mJ) |
>    |---:|---:|---:|---:|---:|---:|---:|---:|
>    | 100 | 0.200 | 100.0 | 52.7 | 0.611 | 392.0 | 0.7996 | 0.8000 |
>    | 200 | 0.141 | 100.0 | 63.8 | 0.655 | 370.2 | 0.3997 | 0.4000 |
>    | 400 | 0.100 | 100.0 | 72.9 | 0.692 | 383.8 | 0.1999 | 0.2000 |
>    | 800 | 0.071 | 100.0 | 80.0 | 0.720 | 382.1 | 0.0999 | 0.1000 |
>    | 1600 | 0.050 | 100.0 | 85.4 | 0.742 | 380.1 | 0.0500 | 0.0500 |
>
>    The time constant does not move, because the envelope's decay rate is $\zeta\omega_n=\frac{b}{2\sqrt{km}}\sqrt{\frac km}=\frac{b}{2m}$, in which $k$ cancels; the settling time therefore stays near the $391\,\mathrm{ms}$ estimate, between $370$ and $392\,\mathrm{ms}$, wandering only with where the last swing crosses the band's edge. The overshoot grows because $\zeta=b/(2\sqrt{km})$ falls as $1/\sqrt k$, and the peak force climbs toward the undamped limit $2F=0.8\,\mathrm{N}$. The dissipated energy halves each time $k_w$ doubles, because a stiffer wall stores less at the same force and so there is less to dissipate: stiffness chooses the ringing and the energy, and only damping chooses how long it lasts.

### Sources

- OpenStax, *University Physics Volume 1* (https://openstax.org/books/university-physics-volume-1, read as HTML) — §1.4 dimensional consistency and why passing it does not prove an equation right; §5.2–5.7 Newton's laws and free-body diagrams (external forces only, no net-force arrow, never both forces of a pair); §6.2 friction ($f_s\le\mu_sN$, $f_k=\mu_kN$, nearly independent of speed and contact area, $\mu_k<\mu_s$); §7.1–7.4 and §8.1–8.2 work, the work–energy theorem, power, the spring's potential energy and conservative forces; §10.5–10.8 and §11.2 moments of inertia and the parallel-axis theorem, torque, $\sum\tau=I\alpha$, $P=\tau\omega$ and $L=I\omega$; §12.1 and §12.3 static equilibrium and Young's modulus (steel $20.0\times10^{10}\,\mathrm{Pa}$, aluminium $7.0\times10^{10}\,\mathrm{Pa}$); §15.1 and §15.5 simple harmonic motion, $F_D=-bv$ and critical damping at $b=\sqrt{4mk}$.
- NIST, *Guide for the Use of the International System of Units (SI)*, SP 811, Chapter 4 (https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes) — Table 3's named derived units, the radian as $\mathrm{m/m}=1$ (§4.2.1), and the newton metre rather than the joule for a moment of force (§4.2.2).
- Within this wiki: [[02-foundations/engineering-math|0.5 Engineering Math]] for linearity and the second-order equation (§4.5, §8); [[02-foundations/lab-plants|0.6 Lab Plants]] for P2 and P3; [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] for P3's closed-loop polynomial and its equilibrium with the hand; [[02-foundations/manipulator-kinematics-dynamics|10]] for P2's $M_{11}$ and $g_1$; [[04-robotics/actuators-drives|10.5]] and [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]] for the rotor inertias used in §9.
- The push $F$, the friction $f_c$ and $f_s$, the steel wire of §3 and the tool of the problem set are this page's own course numbers, and every number on the page was computed here from them and from the catalog; the lab recomputes the step-response numbers. Recompute them rather than trusting them.

## 한국어

*[[02-foundations/engineering-math|0.5 공업수학]]의 미분, 지수, 복소근, 2차 방정식과 [[02-foundations/lab-plants|0.6 Lab Plants]]의 두 장치 위에 선다. **P3**와 **P2**를 숫자가 아니라 물리로 처음 여는 페이지다. P3의 핸들로 힘, 스프링, 감쇠, 진동, 에너지를 다루고, P2의 팔로 토크, 관성, 유지 토크를 다룬다. 제어, 힘 제어, 햅틱 렌더링, 액추에이터는 모두 이 방정식들 위에 무언가를 더해서 쓴다.*

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택 — 인식, 물체·장면 이해, 파지, 모션·과제 계획, 조작, 접촉·힘·촉각 피드백, 학습과 적응, 작업 완료 — 에서 이 페이지는 접촉·힘 층과 구동 층 밑의 물리적 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). "*저 패널을 프레임에 설치해*"에서는 패널의 구멍이 핀에 닿아 팔이 물러져야 하는 순간이다. 이것 없이는 접촉의 숫자가 사람을 속인다. $10\,\mathrm N$으로 누르려던 패널은 공구가 $5\,\mathrm{cm/s}$로 닿는 순간 $22.4\,\mathrm N$을 맞고([[04-robotics/force-compliance-control|13. §5]]), $0.4\,\mathrm N$으로 민 P3의 핸들은 벽을 $0.692\,\mathrm N$으로 때리는데, 정역학의 답에는 어느 쪽도 보이지 않는다. 여기서 배우는 고유 진동수, 감쇠비, 에너지 장부, 기어의 맞바꿈은 [[04-robotics/control-theory-ce397|5. 제어 이론 §5]], [[04-robotics/actuators-drives|10.5 §4]], [[04-robotics/force-compliance-control|13. §2]], [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]가 쓰는 말이고, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지는 블록 1, 곧 토목 학위가 비워 둔 동역학을 메우는 기초의 바닥에 놓인다. 이 페이지를 마치면 자유물체도에서 접촉의 운동 방정식을 쓰고, 그것이 울리는지, 얼마나 세게 때리는지, 가라앉는 데 얼마나 걸리는지를 읽어 낼 수 있다.

> [!note] 처음이라면 · First pass
> 한 번에 90분 안팎, 두 번이면 된다. **첫 번째, 핸들:** 이 페이지의 대상과 그림을 읽고 §1–§5를 차례로 읽는다. 다섯 절은 한 장면, 곧 벽으로 밀려 들어가는 P3의 핸들을 법칙 하나씩 쌓아 세운다 — 단위, 자유물체도, 스프링, 댐퍼와 마찰, 질량–스프링–댐퍼. *감쇠비*나 *시정수*라는 말이 처음이라면 §5에서 속도를 늦추고, 맨 핸들의 $\omega_n$, $\zeta$, $\tau$를 직접 계산해 §5와 맞춰 보는 것으로 첫 번째를 끝낸다. **두 번째, 에너지와 회전:** §6과 그 뒤의 계산 절을 읽는다. 계산 절이 §1–§6을 숫자 한 벌 위에 모두 올린다. 이어 P2의 §7–§9를 읽고(정역학이 익숙하다면 §8은 금방 읽힌다), §10의 랩을 돌린 뒤 정답을 펼치기 전에 스스로 점검에 답한다. 접힌 *더 깊이* 상자는 두 번째 읽을 때로 미뤄도 되고, §11은 이 페이지가 어디서 멈추는지 말한다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P3**와 **P2**를 카탈로그가 고정한 숫자 그대로 쓴다. 이 페이지는 그 숫자를 하나도 바꾸지 않는다. P3의 핸들이 페이지의 병진 절반 — 힘, 스프링, 감쇠, 진동, 에너지 — 을 맡고, P2의 팔이 회전 절반 — 토크, 관성 모멘트, 유지 토크, 기어 — 을 맡는다.

| 기호 | 값 | 무엇이고, 이 페이지 어디서 쓰는가 |
|---|---:|---|
| $m$ | $0.04\,\mathrm{kg}$ | P3 핸들의 유효 질량 (§2) |
| $b$ | $0.8\,\mathrm{N{\cdot}s/m}$ | P3의 물리적 점성 감쇠 (§4) |
| $k_w$, $x_w$ | $400\,\mathrm{N/m}$, $0.030\,\mathrm{m}$ | P3의 가상 벽과 그 시작 위치. $+x$가 벽 안쪽 (§3) |
| $k_h$, $b_h$ | $400\,\mathrm{N/m}$, $8\,\mathrm{N{\cdot}s/m}$ | 손이 핸들을 쥘 때의 강성과 감쇠 (§3, §5) |
| $r_m$, $r_s$ | $0.010$, $0.050\,\mathrm{m}$ | P3의 캡스턴: 모터 풀리와 섹터의 반지름 (§9) |
| $L_1=L_2$, $m_1=m_2$ | $1\,\mathrm{m}$, $1\,\mathrm{kg}$ | P2의 단위 링크, 그리고 팔꿈치와 말단의 점질량 (§7) |
| $\theta$, $g$ | $(0^\circ,90^\circ)$, $-y$ 방향 $9.81\,\mathrm{m/s^2}$ | P2의 카탈로그 자세. 팔꿈치 $(1,0)$, 말단 $(1,1)\,\mathrm{m}$ (§7, §8) |
| $n$ | $100$ | P2의 관절 구동계마다 달린 감속비. [[04-robotics/actuators-drives\|10.5]]가 고정한다 (§9) |

이 페이지가 더해서 고정하는 숫자 셋. 계산이 보이도록 고른 이 페이지만의 교육용 숫자이고, 어떤 장치를 잰 값이 아니다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $F$ | $0.4\,\mathrm{N}$ | 핸들을 벽 안쪽으로 미는 일정한 힘. 핸들이 벽 표면에 멈춰 있는 $t=0$에 시작한다 — 카탈로그 벽이 $1\,\mathrm{mm}$에서 되미는 힘과 같다 |
| $f_c$ | $0.02\,\mathrm{N}$ | 핸들 가이드의 미끄럼(쿨롱) 마찰. §4에서만 쓴다 |
| $f_s$ | $0.05\,\mathrm{N}$ | 같은 가이드의 이탈(정지) 마찰. §4에서만 쓴다 |

모델링 선택 둘을 한 번만 밝힌다. P3의 카탈로그 모델에는 축 방향 중력 항이 없다 — [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]는 이를 $m\ddot x+b\dot x=F_h+F_a$로 쓴다 — 그래서 이 페이지는 축이 수평이라고 두고, 핸들의 무게와 가이드의 반력은 축에 수직으로 서로 상쇄된다고 본다. 깊이 $y=x-x_w$는 핸들이 벽 안으로 얼마나 들어갔는지를 잰다. P2는 [[02-foundations/manipulator-kinematics-dynamics|10]]과 10.5처럼 연직면에 서 있고, 어깨를 도는 한 물체로 다룰 때는 언제나 팔꿈치를 $90^\circ$에 잠근다.

*범위: 이 페이지는 로보틱스 연구자가 매일 쓰는 역학을 P3와 P2 위에서 가르친다 — SI 단위와 차원 점검, 뉴턴의 법칙과 자유물체도, 직렬·병렬·예압 스프링, 스프링으로서의 실제 부품, 점성 감쇠와 쿨롱 마찰, 고유 진동수·감쇠비·시정수를 가진 질량–스프링–댐퍼, 일·에너지·일률, 토크·관성 모멘트·각운동량, 정역학과 유지 토크, 지렛대와 기어. 피드백 시스템의 응답 숫자와 주파수 응답([[04-robotics/control-theory-ce397|5. 제어 이론]]), 다관절 팔의 동역학([[02-foundations/manipulator-kinematics-dynamics|10]]), 모터와 기어박스 손실([[04-robotics/actuators-drives|10.5]]), 구현된 임피던스와 접촉([[04-robotics/force-compliance-control|13]]), 샘플된 가상 벽([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]])은 가르치지 않는다. 그 밖에 빠진 것은 §11이 적는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 376" style="max-width:100%;height:auto" role="img" aria-label="P3의 핸들을 일정한 0.4 N으로 가상 벽에 밀어 넣은 모습. 왼쪽 위는 모델: 0.04 kg 핸들, 400 N/m 벽 스프링, 0.8 N·s/m 장치 댐퍼. 오른쪽 위는 첫 정점에서의 자유물체도: 들어가는 0.4 N, 되미는 0.692 N, 댐퍼 힘 0, 합력 −0.2917 N. 아래는 깊이 y 대 시간: 맨 핸들은 100 ms 포락선 안에서 31.6 ms에 1.729 mm까지 울리고 384 ms에 정착하며, 손으로 쥐면 2.0 퍼센트 넘어섰다가 37 ms에 정착한다.">
  <defs><marker id="bmAk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18">일정한 F = 0.4 N으로 가상 벽에 밀어 넣은 P3의 핸들</text>
    <text x="12" y="40" opacity="0.85">모델: 핸들, 벽 스프링, 댐퍼</text>
    <text x="286" y="40" opacity="0.85">첫 정점의 자유물체도, t = 31.6 ms</text>
  </g>
  <polyline points="16,84 66,84" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#bmAk)"/>
  <rect x="68" y="60" width="56" height="48" rx="2" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="124,72 138,72 142.5,65 151.5,79 160.5,65 169.5,79 178.5,65 187.5,79 196.5,65 205.5,79 210,72 224,72" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <line x1="124" y1="98" x2="176" y2="98"/><line x1="176" y1="91" x2="176" y2="105"/>
    <polyline points="164,88 196,88 196,108 164,108"/><line x1="196" y1="98" x2="224" y2="98"/>
    <line x1="224" y1="62" x2="224" y2="112"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="224" y1="64" x2="232" y2="58"/><line x1="224" y1="72" x2="232" y2="66"/><line x1="224" y1="80" x2="232" y2="74"/><line x1="224" y1="88" x2="232" y2="82"/><line x1="224" y1="96" x2="232" y2="90"/><line x1="224" y1="104" x2="232" y2="98"/></g>
  <polyline points="68,140 112,140" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#bmAk)"/>
  <g font-size="11" fill="currentColor">
    <text x="18" y="76">F = 0.4 N</text>
    <text x="96" y="81" text-anchor="middle">m</text>
    <text x="96" y="97" text-anchor="middle" font-size="10.5">0.04 kg</text>
    <text x="150" y="56" text-anchor="middle">벽 스프링 k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> = 400 N/m</tspan></text>
    <text x="160" y="126" text-anchor="middle">장치 댐퍼 b = 0.8 N·s/m</text>
    <text x="116" y="144">y: x<tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> = 0.030 m</tspan>를 지난 깊이</text>
  </g>
  <rect x="392" y="62" width="40" height="36" rx="2" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="352,80 391,80" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#bmAk)"/>
  <polyline points="501.2,80 433,80" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#bmAk)"/>
  <g font-size="11" fill="currentColor">
    <text x="412" y="84" text-anchor="middle">m</text>
    <text x="386" y="72" text-anchor="end">F = 0.4 N</text>
    <text x="438" y="72">k<tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> y = 0.692 N</tspan></text>
    <text x="412" y="116" text-anchor="middle">b ẏ = 0: 정점에서 ẏ = 0</text>
    <text x="412" y="136" text-anchor="middle">ΣF = 0.4 − 0.6917 = −0.2917 N</text>
    <text x="412" y="152" text-anchor="middle">ÿ = ΣF/m = −7.29 m/s²</text>
    <text x="12" y="176">깊이 y (mm) 대 시간 t (ms), 미는 순간부터</text>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <line x1="60" y1="336" x2="546" y2="336"/><line x1="60" y1="336" x2="60" y2="190"/>
    <line x1="180" y1="336" x2="180" y2="340"/><line x1="300" y1="336" x2="300" y2="340"/><line x1="420" y1="336" x2="420" y2="340"/><line x1="540" y1="336" x2="540" y2="340"/>
    <line x1="56" y1="301" x2="60" y2="301"/><line x1="56" y1="266" x2="60" y2="266"/><line x1="56" y1="231" x2="60" y2="231"/><line x1="56" y1="196" x2="60" y2="196"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="60" y="350" text-anchor="middle">0</text><text x="180" y="350" text-anchor="middle">100</text><text x="300" y="350" text-anchor="middle">200</text><text x="420" y="350" text-anchor="middle">300</text><text x="540" y="350" text-anchor="middle">400</text>
    <text x="300" y="368" text-anchor="middle">t (ms)</text>
    <text x="54" y="340" text-anchor="end">0</text><text x="54" y="305" text-anchor="end">0.5</text><text x="54" y="270" text-anchor="end">1.0</text><text x="54" y="235" text-anchor="end">1.5</text><text x="54" y="200" text-anchor="end">2.0</text>
  </g>
  <line x1="60" y1="266" x2="546" y2="266" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
  <polyline points="60.0,195.6 66.0,199.1 72.0,202.3 78.0,205.4 84.0,208.4 90.0,211.2 96.0,213.9 102.0,216.4 108.0,218.8 114.0,221.1 120.0,223.3 126.0,225.4 132.0,227.4 138.0,229.3 144.0,231.1 150.0,232.8 156.0,234.4 162.0,235.9 168.0,237.4 174.0,238.8 180.0,240.1 186.0,241.4 192.0,242.6 198.0,243.7 204.0,244.8 210.0,245.8 216.0,246.8 222.0,247.8 228.0,248.7 234.0,249.5 240.0,250.3 246.0,251.1 252.0,251.8 258.0,252.5 264.0,253.1 270.0,253.8 276.0,254.4 282.0,254.9 288.0,255.5 294.0,256.0 300.0,256.5 306.0,256.9 312.0,257.4 318.0,257.8 324.0,258.2 330.0,258.6 336.0,258.9 342.0,259.3 348.0,259.6 354.0,259.9 360.0,260.2 366.0,260.5 372.0,260.8 378.0,261.0 384.0,261.3 390.0,261.5 396.0,261.7 402.0,261.9 408.0,262.1 414.0,262.3 420.0,262.5 426.0,262.7 432.0,262.8 438.0,263.0 444.0,263.1 450.0,263.3 456.0,263.4 462.0,263.5 468.0,263.7 474.0,263.8 480.0,263.9 486.0,264.0 492.0,264.1 498.0,264.2 504.0,264.3 510.0,264.3 516.0,264.4 522.0,264.5 528.0,264.6 534.0,264.6 540.0,264.7" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.5"/>
  <polyline points="60.0,336.4 66.0,332.9 72.0,329.7 78.0,326.6 84.0,323.6 90.0,320.8 96.0,318.1 102.0,315.6 108.0,313.2 114.0,310.9 120.0,308.7 126.0,306.6 132.0,304.6 138.0,302.7 144.0,300.9 150.0,299.2 156.0,297.6 162.0,296.1 168.0,294.6 174.0,293.2 180.0,291.9 186.0,290.6 192.0,289.4 198.0,288.3 204.0,287.2 210.0,286.2 216.0,285.2 222.0,284.2 228.0,283.3 234.0,282.5 240.0,281.7 246.0,280.9 252.0,280.2 258.0,279.5 264.0,278.9 270.0,278.2 276.0,277.6 282.0,277.1 288.0,276.5 294.0,276.0 300.0,275.5 306.0,275.1 312.0,274.6 318.0,274.2 324.0,273.8 330.0,273.4 336.0,273.1 342.0,272.7 348.0,272.4 354.0,272.1 360.0,271.8 366.0,271.5 372.0,271.2 378.0,271.0 384.0,270.7 390.0,270.5 396.0,270.3 402.0,270.1 408.0,269.9 414.0,269.7 420.0,269.5 426.0,269.3 432.0,269.2 438.0,269.0 444.0,268.9 450.0,268.7 456.0,268.6 462.0,268.5 468.0,268.3 474.0,268.2 480.0,268.1 486.0,268.0 492.0,267.9 498.0,267.8 504.0,267.7 510.0,267.7 516.0,267.6 522.0,267.5 528.0,267.4 534.0,267.4 540.0,267.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.5"/>
  <polyline points="60.0,336.0 61.2,335.7 62.4,334.6 63.6,332.9 64.8,330.6 66.0,327.7 67.2,324.2 68.4,320.3 69.6,315.8 70.8,311.0 72.0,305.8 73.2,300.4 74.4,294.6 75.6,288.8 76.8,282.8 78.0,276.8 79.2,270.7 80.4,264.8 81.6,259.0 82.8,253.3 84.0,247.9 85.2,242.8 86.4,238.0 87.6,233.6 88.8,229.6 90.0,226.1 91.2,223.0 92.4,220.4 93.6,218.3 94.8,216.7 96.0,215.6 97.2,215.0 98.4,215.0 99.6,215.5 100.8,216.4 102.0,217.9 103.2,219.7 104.4,222.0 105.6,224.7 106.8,227.8 108.0,231.1 109.2,234.8 110.4,238.6 111.6,242.7 112.8,246.9 114.0,251.2 115.2,255.6 116.4,260.0 117.6,264.4 118.8,268.7 120.0,272.9 121.2,276.9 122.4,280.8 123.6,284.4 124.8,287.8 126.0,290.9 127.2,293.7 128.4,296.1 129.6,298.2 130.8,300.0 132.0,301.4 133.2,302.4 134.4,303.0 135.6,303.2 136.8,303.1 138.0,302.6 139.2,301.8 140.4,300.6 141.6,299.1 142.8,297.3 144.0,295.2 145.2,292.9 146.4,290.3 147.6,287.6 148.8,284.7 150.0,281.7 151.2,278.6 152.4,275.4 153.6,272.2 154.8,269.0 156.0,265.8 157.2,262.7 158.4,259.7 159.6,256.8 160.8,254.1 162.0,251.5 163.2,249.1 164.4,247.0 165.6,245.0 166.8,243.3 168.0,241.9 169.2,240.8 170.4,239.9 171.6,239.3 172.8,238.9 174.0,238.9 175.2,239.1 176.4,239.5 177.6,240.3 178.8,241.2 180.0,242.4 181.2,243.8 182.4,245.4 183.6,247.2 184.8,249.1 186.0,251.1 187.2,253.3 188.4,255.5 189.6,257.8 190.8,260.1 192.0,262.5 193.2,264.8 194.4,267.1 195.6,269.3 196.8,271.5 198.0,273.6 199.2,275.5 200.4,277.3 201.6,279.0 202.8,280.5 204.0,281.8 205.2,283.0 206.4,283.9 207.6,284.7 208.8,285.3 210.0,285.6 211.2,285.8 212.4,285.7 213.6,285.5 214.8,285.1 216.0,284.5 217.2,283.7 218.4,282.8 219.6,281.7 220.8,280.5 222.0,279.1 223.2,277.7 224.4,276.2 225.6,274.6 226.8,272.9 228.0,271.3 229.2,269.5 230.4,267.8 231.6,266.2 232.8,264.5 234.0,262.9 235.2,261.3 236.4,259.9 237.6,258.5 238.8,257.2 240.0,256.0 241.2,255.0 242.4,254.1 243.6,253.3 244.8,252.7 246.0,252.2 247.2,251.8 248.4,251.6 249.6,251.6 250.8,251.7 252.0,251.9 253.2,252.2 254.4,252.7 255.6,253.4 256.8,254.1 258.0,254.9 259.2,255.8 260.4,256.9 261.6,257.9 262.8,259.1 264.0,260.2 265.2,261.5 266.4,262.7 267.6,263.9 268.8,265.2 270.0,266.4 271.2,267.6 272.4,268.8 273.6,269.9 274.8,270.9 276.0,271.9 277.2,272.8 278.4,273.6 279.6,274.3 280.8,274.9 282.0,275.5 283.2,275.9 284.4,276.2 285.6,276.4 286.8,276.5 288.0,276.5 289.2,276.4 290.4,276.2 291.6,275.9 292.8,275.5 294.0,275.0 295.2,274.4 296.4,273.8 297.6,273.1 298.8,272.3 300.0,271.5 301.2,270.7 302.4,269.8 303.6,268.9 304.8,268.0 306.0,267.1 307.2,266.2 308.4,265.3 309.6,264.5 310.8,263.6 312.0,262.9 313.2,262.1 314.4,261.4 315.6,260.8 316.8,260.2 318.0,259.7 319.2,259.3 320.4,259.0 321.6,258.7 322.8,258.5 324.0,258.4 325.2,258.3 326.4,258.4 327.6,258.5 328.8,258.7 330.0,258.9 331.2,259.2 332.4,259.6 333.6,260.0 334.8,260.5 336.0,261.1 337.2,261.6 338.4,262.2 339.6,262.8 340.8,263.5 342.0,264.1 343.2,264.8 344.4,265.5 345.6,266.1 346.8,266.8 348.0,267.4 349.2,268.0 350.4,268.5 351.6,269.1 352.8,269.5 354.0,270.0 355.2,270.4 356.4,270.7 357.6,271.0 358.8,271.2 360.0,271.4 361.2,271.5 362.4,271.6 363.6,271.6 364.8,271.5 366.0,271.4 367.2,271.3 368.4,271.1 369.6,270.8 370.8,270.5 372.0,270.2 373.2,269.8 374.4,269.4 375.6,269.0 376.8,268.6 378.0,268.1 379.2,267.6 380.4,267.1 381.6,266.7 382.8,266.2 384.0,265.7 385.2,265.3 386.4,264.8 387.6,264.4 388.8,264.0 390.0,263.6 391.2,263.3 392.4,263.0 393.6,262.7 394.8,262.5 396.0,262.3 397.2,262.1 398.4,262.0 399.6,261.9 400.8,261.9 402.0,261.9 403.2,262.0 404.4,262.1 405.6,262.2 406.8,262.4 408.0,262.6 409.2,262.8 410.4,263.0 411.6,263.3 412.8,263.6 414.0,263.9 415.2,264.3 416.4,264.6 417.6,265.0 418.8,265.3 420.0,265.7 421.2,266.0 422.4,266.4 423.6,266.7 424.8,267.0 426.0,267.3 427.2,267.6 428.4,267.8 429.6,268.1 430.8,268.3 432.0,268.5 433.2,268.6 434.4,268.8 435.6,268.9 436.8,268.9 438.0,269.0 439.2,269.0 440.4,269.0 441.6,268.9 442.8,268.8 444.0,268.7 445.2,268.6 446.4,268.4 447.6,268.3 448.8,268.1 450.0,267.9 451.2,267.6 452.4,267.4 453.6,267.2 454.8,266.9 456.0,266.6 457.2,266.4 458.4,266.1 459.6,265.9 460.8,265.6 462.0,265.4 463.2,265.2 464.4,265.0 465.6,264.8 466.8,264.6 468.0,264.4 469.2,264.3 470.4,264.1 471.6,264.0 472.8,263.9 474.0,263.9 475.2,263.8 476.4,263.8 477.6,263.8 478.8,263.9 480.0,263.9 481.2,264.0 482.4,264.1 483.6,264.2 484.8,264.3 486.0,264.4 487.2,264.6 488.4,264.7 489.6,264.9 490.8,265.1 492.0,265.2 493.2,265.4 494.4,265.6 495.6,265.8 496.8,266.0 498.0,266.2 499.2,266.3 500.4,266.5 501.6,266.7 502.8,266.8 504.0,267.0 505.2,267.1 506.4,267.2 507.6,267.3 508.8,267.4 510.0,267.5 511.2,267.5 512.4,267.6 513.6,267.6 514.8,267.6 516.0,267.6 517.2,267.5 518.4,267.5 519.6,267.5 520.8,267.4 522.0,267.3 523.2,267.2 524.4,267.1 525.6,267.0 526.8,266.9 528.0,266.8 529.2,266.6 530.4,266.5 531.6,266.4 532.8,266.2 534.0,266.1 535.2,266.0 536.4,265.8 537.6,265.7 538.8,265.6 540.0,265.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="60.0,336.0 61.2,335.3 62.4,333.6 63.6,331.0 64.8,327.7 66.0,324.0 67.2,319.9 68.4,315.7 69.6,311.5 70.8,307.2 72.0,303.1 73.2,299.1 74.4,295.3 75.6,291.7 76.8,288.4 78.0,285.3 79.2,282.5 80.4,280.0 81.6,277.7 82.8,275.6 84.0,273.8 85.2,272.2 86.4,270.8 87.6,269.6 88.8,268.6 90.0,267.7 91.2,267.0 92.4,266.4 93.6,265.9 94.8,265.5 96.0,265.2 97.2,264.9 98.4,264.8 99.6,264.7 100.8,264.6 102.0,264.6 103.2,264.6 104.4,264.6 105.6,264.6 106.8,264.7 108.0,264.8 109.2,264.9 110.4,265.0 111.6,265.0 112.8,265.1 114.0,265.2 115.2,265.3 116.4,265.4 117.6,265.4 118.8,265.5 120.0,265.6 121.2,265.6 122.4,265.7 123.6,265.7 124.8,265.8 126.0,265.8 127.2,265.9 128.4,265.9 129.6,265.9 130.8,265.9 132.0,266.0 133.2,266.0 134.4,266.0 135.6,266.0 136.8,266.0 138.0,266.0 139.2,266.0 140.4,266.0 141.6,266.0 142.8,266.0 144.0,266.0 145.2,266.0 146.4,266.0 147.6,266.0 148.8,266.0 150.0,266.0 151.2,266.0 152.4,266.0 153.6,266.0 154.8,266.0 156.0,266.0 157.2,266.0 158.4,266.0 159.6,266.0 160.8,266.0 162.0,266.0 163.2,266.0 164.4,266.0 165.6,266.0 166.8,266.0 168.0,266.0 169.2,266.0 170.4,266.0 171.6,266.0 172.8,266.0 174.0,266.0 175.2,266.0 176.4,266.0 177.6,266.0 178.8,266.0 180.0,266.0 181.2,266.0 182.4,266.0 183.6,266.0 184.8,266.0 186.0,266.0 187.2,266.0 188.4,266.0 189.6,266.0 190.8,266.0 192.0,266.0 193.2,266.0 194.4,266.0 195.6,266.0 196.8,266.0 198.0,266.0 199.2,266.0 200.4,266.0 201.6,266.0 202.8,266.0 204.0,266.0 205.2,266.0 206.4,266.0 207.6,266.0 208.8,266.0 210.0,266.0 211.2,266.0 212.4,266.0 213.6,266.0 214.8,266.0 216.0,266.0 217.2,266.0 218.4,266.0 219.6,266.0 220.8,266.0 222.0,266.0 223.2,266.0 224.4,266.0 225.6,266.0 226.8,266.0 228.0,266.0 229.2,266.0 230.4,266.0 231.6,266.0 232.8,266.0 234.0,266.0 235.2,266.0 236.4,266.0 237.6,266.0 238.8,266.0 240.0,266.0" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <circle cx="97.9" cy="215" r="3" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" opacity="0.8">
    <line x1="520.6" y1="262" x2="520.6" y2="336"/><line x1="104.4" y1="262" x2="104.4" y2="336"/>
  </g>
  <line x1="236" y1="292" x2="256" y2="292" stroke="currentColor" stroke-width="1.8"/>
  <line x1="236" y1="308" x2="256" y2="308" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <g font-size="11" fill="currentColor">
    <text x="106" y="206">첫 정점 31.6 ms에 1.729 mm: 벽 힘 0.692 N</text>
    <text x="260" y="248">포락선: τ = 2m/b = 100 ms</text>
    <text x="544" y="258" text-anchor="end">y<tspan dy="3" font-size="10">ss</tspan><tspan dy="-3"> = F/k</tspan><tspan dy="3" font-size="10">w</tspan><tspan dy="-3"> = 1.0 mm</tspan></text>
    <text x="262" y="296">맨 핸들: ζ = 0.10, 오버슈트 72.9 %</text>
    <text x="262" y="312">쥔 핸들, + k<tspan dy="3" font-size="10">h</tspan><tspan dy="-3">, b</tspan><tspan dy="3" font-size="10">h</tspan><tspan dy="-3">: ζ = 0.78, 2.0 %</tspan></text>
    <text x="108" y="328">쥔 핸들 정착 37 ms</text>
    <text x="516" y="328" text-anchor="end">맨 핸들 정착 384 ms</text>
  </g>
</svg>

정지한 P3의 핸들을 일정한 $F=0.4\,\mathrm{N}$으로, 자기 댐퍼 $0.8\,\mathrm{N{\cdot}s/m}$와 함께 $400\,\mathrm{N/m}$ 벽에 밀어 넣은 모델, 첫 정점에서의 자유물체도 — 들어가는 $0.4\,\mathrm{N}$에 맞서 $0.692\,\mathrm{N}$이 되밀고 댐퍼 힘은 없으므로 $\ddot y=-7.29\,\mathrm{m/s^2}$ — 그리고 시간에 따른 깊이다. 맨 핸들은 감쇠비 $0.10$으로 울리며, 시정수 $100\,\mathrm{ms}$인 포락선 안에서 $31.6\,\mathrm{ms}$에 $1.729\,\mathrm{mm}$까지 갔다가 $384\,\mathrm{ms}$에 $2\%$ 띠 안에 정착한다. 손으로 쥐면 손의 스프링과 댐퍼가 벽과 장치의 것에 더해져 $2.0\%$만 넘어서고 $37\,\mathrm{ms}$에 정착하며, 둘 다 $1.0\,\mathrm{mm}$ 깊이, 벽에 $0.4\,\mathrm{N}$으로 끝난다.

### 1. 물리량, 단위, 차원 점검

유도나 코드 한 줄에서 나오는 틀린 숫자는 대부분 단위 실수이고, 이 절은 그것이 퍼지기 전에 잡는 점검이다. 물리량은 숫자 곱하기 단위이고, 숫자만으로는 아무 뜻이 없다. P3의 벽은 $400\,\mathrm{N/m}$인데, 이는 $0.4\,\mathrm{N/mm}$이기도 하고 $400\,\mathrm{kg/s^2}$이기도 하다 — 강성 하나를 세 가지로 쓴 것이다. 이 위키는 국제단위계 SI로 계산한다. 역학의 기본 단위는 킬로그램, 미터, 초 셋이고, 다른 역학 단위는 모두 이 셋의 거듭제곱을 곱한 것이다. NIST의 SI 지침은 고유한 이름을 가진 유도 단위를 표로 정리하는데(표 3), 그중 넷이 이 페이지를 떠받친다.

| 물리량 | SI 단위 | 기본 단위로 | P3나 P2에서 |
|---|---|---|---|
| 힘 | 뉴턴, $\mathrm{N}$ | $\mathrm{kg\,m\,s^{-2}}$ | 미는 힘 $F=0.4\,\mathrm{N}$ |
| 에너지, 일 | 줄, $\mathrm{J}=\mathrm{N\,m}$ | $\mathrm{kg\,m^2\,s^{-2}}$ | 벽이 $1\,\mathrm{mm}$에서 저장하는 $0.2\,\mathrm{mJ}$ (§6) |
| 일률 | 와트, $\mathrm{W}=\mathrm{J/s}$ | $\mathrm{kg\,m^2\,s^{-3}}$ | $0.1\,\mathrm{m/s}$에서 댐퍼로 들어가는 $8\,\mathrm{mW}$ (§4) |
| 압력, 응력 | 파스칼, $\mathrm{Pa}=\mathrm{N/m^2}$ | $\mathrm{kg\,m^{-1}\,s^{-2}}$ | 강철의 탄성 계수 $200\,\mathrm{GPa}$ (§3) |

고유한 이름은 없지만 아래 모든 줄에 나오는 단위가 셋 더 있다. 강성은 $\mathrm{N/m}=\mathrm{kg\,s^{-2}}$, 감쇠는 $\mathrm{N{\cdot}s/m}=\mathrm{kg\,s^{-1}}$, 토크는 $\mathrm{N{\cdot}m}$이다. 각은 라디안으로 재고, 라디안은 숫자 1에 붙인 특별한 이름이다 — 반지름 1미터당 호 1미터(지침의 §4.2.1). 그래서 $\mathrm{rad/s}$ 단위의 각속도는 차원으로 $\mathrm{s^{-1}}$이고, $100\,\mathrm{rad/s}$는 분당 $100\cdot60/(2\pi)=955$ 회전이다.

단위는 숫자가 무엇인지를 말하고, *차원* — 질량, 길이, 시간의 어떤 거듭제곱으로 이루어졌는가 — 은 무엇과 더할 수 있는지를 말한다. 여기서 모든 방정식이 믿어지기 전에 통과해야 하는 시험이 나온다.

> **차원 동차성의 정의.** **차원 동차성**(dimensional homogeneity)은 *방정식의 성질*이다. 물리적으로 뜻이 있는 방정식이라면 나중에 어떤 단위로 계산하든 만족하는 필요조건이다. 정의 조건은 셋이고, 앞의 둘은 OpenStax가 규칙을 말하는 대로다. **더하고, 빼고, 등호로 잇는** 모든 항은 같은 차원을 가진다. 힘을 속도에 더할 수는 없기 때문이다. 그리고 모든 **지수, 로그, 삼각함수**의 인자는 순수한 수다. 그렇지 않으면 $e^x=1+x+x^2/2+\dots$가 차원이 다른 양들을 더하게 되기 때문이다. 셋째 조건은 이 점검이 무엇을 증명하는지를 정직하게 한다. 통과는 **필요조건일 뿐 충분조건이 아니다**. 차원 없는 계수 — 2 하나, $\pi$ 하나 — 는 여전히 틀릴 수 있기 때문이다.
>
> $$[m\ddot y]=[b\dot y]=[ky]=[F]=\mathrm{kg\,m\,s^{-2}}=\mathrm{N}$$
>
> $[\cdot]$는 "~의 차원"으로 읽고, $m$은 질량, $b$는 감쇠 계수, $k$는 강성, $y$는 변위다. 그러므로 §5의 운동 방정식은 동차적이다. $\mathrm{kg/s}$인 $b$에 $\mathrm{m/s}$인 $\dot y$를 곱한 것과, $\mathrm{kg/s^2}$인 $k$에 $\mathrm{m}$인 $y$를 곱한 것이 둘 다 뉴턴이 되기 때문이다.
> - **예**: P3의 감쇠비(§5) $\zeta=b/(2\sqrt{km})$의 차원은 $(\mathrm{kg/s})/\sqrt{(\mathrm{kg/s^2})\,\mathrm{kg}}=(\mathrm{kg/s})/(\mathrm{kg/s})=1$이다. 그래서 지수 안에 들어갈 수 있다. $e^{-\zeta\omega_nt}$에서 곱 $\zeta\omega_nt$는 $1\times\mathrm{s^{-1}}\times\mathrm{s}$, 둘째 조건이 요구하는 순수한 수다.
> - **비예**: $\zeta=b/\sqrt{km}$. 올바른 식과 똑같이 동차적이면서 두 배 크다 — P3가 $0.1$ 대신 $0.2$로 읽힌다. 점검은 빠진 2를 보지 못한다.
> - **비예**: 토크와 에너지. 유지 토크 $19.62\,\mathrm{N{\cdot}m}$와 일 $19.62\,\mathrm{J}$은 차원이 같지만($\mathrm{kg\,m^2\,s^{-2}}$) 서로 다른 양이다. NIST 지침은 둘을 구별하려고 힘의 모멘트의 단위를 줄이 아니라 뉴턴미터로 쓴다(지침의 §4.2.2). 두 항을 더하려면 차원이 같아야 하지만, 차원이 같다고 같은 종류의 양이라는 증명이 되지는 않는다.
> - **왜 중요한가**: 유도나 코드 한 줄이 통과할 수 있는 가장 싼 시험이고, 이 페이지에서 가장 흔한 실수를 잡는다. 강성이 N/m인 식에 밀리미터를 넣으면 $1\,\mathrm{mm}$에서 벽의 에너지가 $\tfrac12\cdot400\cdot(10^{-3})^2=2\times10^{-4}\,\mathrm{J}$ 대신 $\tfrac12\cdot400\cdot1^2=200$이 된다. $10^6$배다.

이 페이지는 새 식이 나올 때마다 이 점검을 돌린다. 아래 모든 절에 되풀이해 나오는 셋은 다음과 같다.

$$[\omega_n]=\Big[\sqrt{k/m}\Big]=\sqrt{\frac{\mathrm{kg\,s^{-2}}}{\mathrm{kg}}}=\mathrm{s^{-1}},\qquad \Big[\frac mb\Big]=\frac{\mathrm{kg}}{\mathrm{kg\,s^{-1}}}=\mathrm{s},\qquad [b\dot y^2]=\mathrm{kg\,s^{-1}}\cdot\mathrm{m^2\,s^{-2}}=\mathrm{W}$$

그러므로 §5의 고유 진동수는 빠르기, 시정수는 시간, 댐퍼의 일률은 일률이다. 양변이 같은 기본 단위로 줄어들기 때문이다. 단위가 잡아내는 실수가 셋 더 있고, 모두 이 페이지의 숫자에서 나온다.

- **질량은 무게가 아니다.** P2의 점질량은 각각 $1\,\mathrm{kg}$이고, 각각의 *무게*는 $1\cdot9.81=9.81\,\mathrm{N}$이다. 힘의 평형식에 킬로그램이 있으면 $g$가 빠진 것이다.
- **뉴턴은 뉴턴미터가 아니다.** 카탈로그 자세의 P2는 받침에서 $19.62\,\mathrm{N}$의 힘을, 어깨에서 $19.62\,\mathrm{N{\cdot}m}$의 토크를 받아야 한다(§8). 숫자가 같은 것은 모멘트 팔이 $1\,\mathrm{m}$이기 때문일 뿐이다.
- **회전수는 라디안이 아니다.** P2의 관절을 $n=100$ 기어박스를 거쳐 $1\,\mathrm{rad/s}$로 돌리는 모터는 $100\,\mathrm{rad/s}$로 돌고, 데이터시트는 이를 $955\,\mathrm{rpm}$으로 적는다. 한쪽을 기대하는 식에 다른 쪽을 넣으면 $2\pi/60$배 틀린다.

### 2. 힘, 뉴턴의 법칙, 자유물체도

무엇이 어떻게 움직일지 예측하려면 먼저 그것에 작용하는 힘을 모두 알아야 한다. 뉴턴의 법칙이 그 힘들을 운동으로 바꾸고, 자유물체도가 어느 힘도 빠지거나 두 번 세어지지 않게 한다. **힘**은 물체를 미는 것 또는 당기는 것이다. 크기(뉴턴)와 방향을 가진 벡터다. 뉴턴의 세 법칙이 힘과 운동을 잇고, OpenStax는 이 페이지가 쓰는 바로 그 용도로 법칙을 정리한다. 요지는 이렇다.

1. 알짜 외력이 0인 물체는 속도를 유지한다. 멈춰 있으면 계속 멈춰 있고, 움직이면 같은 빠르기로 직선을 따라 계속 움직인다.
2. 관성 좌표계에서 알짜 외력은 질량 곱하기 가속도다, $\sum\vec F=m\vec a$. 1뉴턴은 1킬로그램에 $1\,\mathrm{m/s^2}$의 가속도를 주는 힘이다, $1\,\mathrm{N}=1\,\mathrm{kg\,m/s^2}$.
3. 힘은 짝으로 온다. 물체 A가 물체 B를 밀면 B는 크기가 같고 방향이 반대인 힘으로 A를 민다, $\vec F_{AB}=-\vec F_{BA}$. 두 힘은 서로 다른 물체에 작용하므로 한 물체의 방정식 안에서 결코 상쇄되지 않는다.

정역학에서 자유물체도를 배웠다면 그림은 바뀌지 않는다. 정역학은 물체가 가속하지 않으므로 $\sum\vec F=0$을 쓰고, 동역학은 같은 그림으로 $\sum\vec F=m\vec a$를 쓴다. 힘들이 서로 맞비기지 못하고 남긴 몫이 물체를 가속하는 데 쓰인다. 그림 속 울림의 매 순간이 미는 힘, 벽, 댐퍼 사이의 그런 어긋남이다.

실제 계산에 쓰는 것은 둘째 법칙이고, 그 법칙을 쓰려면 어떤 힘이 어느 물체에 작용하는지부터 알아야 한다. 그 정리에는 이름과 그림이 있다.

> **자유물체도의 정의.** **자유물체도**(free-body diagram)는 *고른 물체 하나를 닿아 있는 모든 것에서 떼어 낸 그림*이다. 그 물체에 작용하는 모든 외력을 화살표로 그린다. 물리적 장치를 뉴턴의 둘째 법칙으로 바꾸는 모델링 단계다. 정의 조건 넷. **물체 하나**, 또는 고른 계 하나를 떼어 내고, 그것이 닿는 모든 것을 그것이 가하는 힘으로 바꾼다. 그 물체에 작용하는 **모든 외력**을 작용하는 점에서 방향과 함께 그린다. 물체가 무언가에 닿는 곳마다의 접촉력, 그리고 무게 같은 장(field)의 힘이다. **그 밖에는 아무것도** 그리지 않는다 — 물체가 남에게 가하는 힘(셋째 법칙에 따라 그쪽 그림에 속한다)도, 내력도, $m\ddot y$도. $m\ddot y$는 힘들 가운데 하나가 아니라 힘들의 결과다. 그리고 **양의 방향을 가진 축**을 정해서, 화살표마다 부호 있는 성분이 되게 한다.
>
> $$\sum F_x=m\,a_x:\qquad F-k_w\,y-b\,\dot y=m\,\ddot y$$
>
> 왼쪽은 그린 힘들의 $x$ 성분의 합, 오른쪽은 같은 축 방향의 질량 곱하기 가속도다. P3에서는 미는 힘 $F$, 벽의 $-k_wy$($y>0$일 때), 댐퍼의 $-b\dot y$다. $x$ 방향 성분을 가진 힘은 그 셋뿐이기 때문이다.
> - **예**: 그림 오른쪽 위, 첫 정점에서의 P3. 거기서 $\dot y=0$이므로 댐퍼는 아무것도 밀지 않는다. 벽은 $0.4\,\mathrm{N}$의 미는 힘에 맞서 $400\times1.729\times10^{-3}=0.692\,\mathrm{N}$으로 되밀므로 $\sum F_x=0.4-0.6917=-0.2917\,\mathrm{N}$, $\ddot y=-0.2917/0.04=-7.29\,\mathrm{m/s^2}$다. 핸들은 한순간 멈춰 있지만 이미 밖으로 튕겨 나가는 중이다.
> - **비예**: 같은 그림에 넷째 화살표 $m\ddot y$를 "균형을 맞추려고" 그린 것. 그 화살표가 있으면 힘의 합이 0이 되어 법칙이 $0=0$이 되고, 가속도가 문제에서 사라진다 — 오른쪽에도 그대로 두면 질량을 두 번 센다.
> - **비예**: 핸들의 그림에 핸들이 **손에** 가하는 $0.4\,\mathrm{N}$을 그린 것. 그 힘은 손에 작용한다. 미는 힘의 셋째 법칙 짝이고, 둘은 결코 한 그림에 함께 나오지 않는다.
> - **왜 중요한가**: 이 페이지 위의 모든 운동 방정식이 여기서 시작한다 — [[04-robotics/control-theory-ce397|5. 제어 이론 §2]]의 상태공간 모델, [[02-foundations/manipulator-kinematics-dynamics|10. §2]]의 매니퓰레이터 방정식, [[04-robotics/force-compliance-control|13. §2]]의 목표 임피던스. 거기서 화살표 하나가 빠지거나 겹치면 제어를 설계하기도 전에 모델이 틀린 것이다.

P3에 적용하면 이 그림이 핸들의 운동 방정식을 준다. 핸들의 무게 $0.04\cdot9.81=0.39\,\mathrm{N}$과 가이드의 반력은 축에 수직으로 작용해 상쇄된다. 축을 따라서는 미는 힘, 벽, 댐퍼가 작용하므로

$$m\,\ddot y+b\,\dot y+k_w\,y=F\qquad(y>0)$$

이다. $x_w$가 상수라서 $\dot y=\dot x$, $\ddot y=\ddot x$이고, 맞서는 두 힘을 왼쪽으로 옮기면 구동하는 힘 하나가 오른쪽에 남기 때문이다. 세 순간이 이 식에서 바로 읽힌다. $t=0$에 핸들은 표면에 멈춰 있고 $y=\dot y=0$이므로 미는 힘만 작용해 $\ddot y=F/m=0.4/0.04=10\,\mathrm{m/s^2}$, 약 $1g$다. 첫 정점에서는 상자의 예처럼 $\ddot y=-7.29\,\mathrm{m/s^2}$다. 끝에서는 $\dot y=\ddot y=0$이고 벽이 정확히 $0.4\,\mathrm{N}$으로 되민다 — 평형, 첫째 법칙이다.

**셋째 법칙, 그리고 힘 센서가 보는 것.** 핸들은 손이 미는 바로 그 힘으로 손을 되민다. 그것이 벽의 힘과도 같은 것은 핸들이 가속하지 않을 때뿐이다. 첫 정점에서 벽은 $0.692\,\mathrm{N}$으로 미는데 손은 여전히 $0.4\,\mathrm{N}$으로 밀고, 그 차이 $0.292\,\mathrm{N}$이 $m\ddot y$, 곧 $40\,\mathrm{g}$의 핸들을 세워 되돌리는 데 드는 힘이다. 손잡이의 힘 센서와 벽의 힘 센서는 핸들이 울리는 동안 정확히 $m\ddot y$만큼 어긋나고 정착하면 일치한다. 그러니 과도 상태에서 읽은 힘은 정상 접촉력이 아니다. [[04-robotics/force-compliance-control|13. §5]]는 같은 관성의 값을 충돌에서 매긴다. 제어기가 $10\,\mathrm{N}$으로 누르려는 패널에 $5\,\mathrm{cm/s}$로 도착하면 $22.4\,\mathrm{N}$의 정점이 걸린다.

### 3. 스프링: 강성, 직렬과 병렬, 예압

하중을 받아 물러서는 모든 것 — 접촉, 쥔 손, 케이블, 보 — 은 스프링처럼 되민다. 얼마나 물러설지 예측하려면 그 강성과, 둘을 합치는 규칙이 필요하다. 스프링은 변위를 힘으로 바꾸는 가장 단순한 것이다. P3에는 둘이 있다 — 모터가 구현하는 벽, 그리고 사람이 핸들을 쥐었을 때의 손. 로보틱스 페이지의 모든 강성은 숫자만 다른 같은 대상이다.

> **선형 스프링의 정의.** **선형 스프링**은 *양 끝을 가진 이상화된 요소*로, 그 힘은 길이가 자유 길이와 얼마나 다른지에만, 그리고 그에 비례해서 달려 있다. 정의 조건 넷. 힘은 변형에 **비례한다**. 변형이 두 배면 힘도 두 배다 — [[02-foundations/engineering-math|0.5 §4.5]]의 뜻에서 가법성과 동차성이다. **복원력이다**. 스프링을 변형시키는 쪽에 가하는 힘은 자유 길이 쪽을 향한다. 그래서 음의 부호가 붙는다. **보존적이다**. 받은 일을 저장했다가 전부 돌려주며, 질량도 손실도 없다. 그리고 **양쪽으로 작용한다**. 쓰는 범위 전체에서 압축되면 미는 만큼 늘어나면 당긴다.
>
> $$F=-k\,(x-x_0),\qquad U=\tfrac12\,k\,(x-x_0)^2$$
>
> $F$는 위치 $x$의 물체에 스프링이 가하는 힘, $x_0$는 스프링이 자유 길이에 있는 위치, $k$는 $\mathrm{N/m}$ 단위의 **강성**, $U$는 줄 단위의 저장 에너지다. 에너지가 이렇게 되는 것은 변형 $\delta$에 걸쳐 힘에 맞서 한 일이 $\int_0^\delta ks\,ds=\tfrac12k\delta^2$이기 때문이다. 역수 $1/k$가 컴플라이언스이고, 그 어휘의 나머지와 함께 [[04-robotics/force-compliance-control|13. §1]]에서 정의된다.
> - **예**: 손, $k_h=400\,\mathrm{N/m}$. 겨누는 곳에서 $1\,\mathrm{mm}$ 떨어져 붙잡히면 $400\cdot10^{-3}=0.4\,\mathrm{N}$으로 끌어당기고 $\tfrac12\cdot400\cdot(10^{-3})^2=0.2\,\mathrm{mJ}$을 저장한다.
> - **비예**: 전체로서의 P3 가상 벽. 벽 안에서 $F_a=-k_w(x-x_w)$는 $x_0=x_w$인 선형 스프링이다. 하지만 밀기만 한다 — $x\le x_w$이면 $F_a=0$ — 그래서 핸들을 벽 밖으로 $1\,\mathrm{mm}$ 당겨도 $0.4\,\mathrm{N}$이 아니라 $0\,\mathrm{N}$이고, 표면을 가로지르면 중첩이 깨진다. 실제 접촉도 같은 식으로 한쪽으로만 작용하고, 그 강성은 하중과 함께 커지기까지 한다([[04-robotics/force-compliance-control|13. §1]]).
> - **왜 중요한가**: 로보틱스 페이지의 모든 강성 — 13의 목표 강성과 환경 강성, 24.4의 $k_w$ — 이 이 $k$이고, 비례성 덕분에 스프링에 매단 질량은 진폭과 상관없이 고유 진동수 하나를 가진다(§5).

한 물체에 작용하는 두 스프링은 언제나 하나로 바꿀 수 있다. 어느 규칙으로 바꾸는지가 그림이 처음으로 사람을 속이는 곳이다.

> **직렬 스프링과 병렬 스프링의 정의.** **병렬**과 **직렬**은 *두 스프링을 등가 스프링 하나로 바꾸는 두 규칙*이다. 어느 쪽이 맞는지는 그림 모양이 아니라 두 스프링이 무엇을 공유하는지가 정한다. 정의 조건은 규칙마다 하나씩, 둘이다. 두 스프링이 변형 하나를 공유하면 — 같은 움직이는 점과 같은 바닥 사이에 걸려 있으면 — **병렬**이고, 힘이 더해진다. 두 스프링이 힘 하나를 나르면 — 한쪽의 끝이 다른 쪽의 시작이고 그 사이에 다른 것이 붙어 있지 않으면 — **직렬**이고, 변형이 더해지며 그와 함께 컴플라이언스가 더해진다.
>
> $$k_{\parallel}=k_1+k_2,\qquad \frac{1}{k_{\text{series}}}=\frac{1}{k_1}+\frac{1}{k_2}$$
>
> 각각 한 줄로 나온다. 병렬이면 $F=k_1\delta+k_2\delta=(k_1+k_2)\,\delta$이고, 직렬이면 $\delta=F/k_1+F/k_2$이기 때문이다. 그래서 병렬 쌍은 어느 한쪽보다 단단하고, 직렬 쌍은 어느 한쪽보다 무르다.
> - **예**: 벽 안의 P3를 쥔 손. 손의 겨눔점을 고정한 채 핸들 자신의 운동을 보면, 손의 스프링과 벽이 둘 다 핸들의 $y$만큼 변형한다. 병렬이고 $400+400=800\,\mathrm{N/m}$, 24.4의 특성 다항식에 있는 그 $800$이다. "손이 표면 너머 얼마나 겨눠야 벽을 $0.4\,\mathrm{N}$으로 누르는가"라는 물음에서는 그 힘 하나가 두 스프링을 차례로 지난다. 직렬이고 $1/(1/400+1/400)=200\,\mathrm{N/m}$이므로 겨눔점은 $0.4/200=0.002\,\mathrm{m}$ 움직인다 — 24.4의 겨눔점 $0.032\,\mathrm{m}$, 표면 $0.030$에서 $2\,\mathrm{mm}$ 너머다.
> - **비예**: "손, 핸들, 벽이 한 줄로 놓였으니 직렬이다." 그림은 한 줄이지만 핸들의 운동에서는 두 스프링이 그 변형을 공유한다. 직렬 값을 쓰면 P3의 고유 진동수가 $\sqrt{800/0.04}=141.4$ 대신 $\sqrt{200/0.04}=70.7\,\mathrm{rad/s}$가 된다.
> - **왜 중요한가**: 직렬 규칙은 사슬에서 가장 무른 요소가 강성을 정하는 이유다 — [[04-robotics/force-compliance-control|13. §1]]이 제어기, 공구, 패널로 펼치는 논증이다. 병렬 규칙은 단단히 쥐는 것이 햅틱 핸들을 단단하게 하고 동시에 차분하게 하는 이유다(§5).

작동점에서 이미 힘을 지고 있는 스프링은 범위의 가장자리에서 다르게 행동하고, 그것을 말하는 낱말이 하나 더 있다.

> **예압의 정의.** **예압**(preload)은 *작동점에서 스프링이나 접촉이 이미 지고 있는 힘*이다. 조립으로, 또는 작업 하중이 오기 전의 일정한 누름으로 정해진다. 정의 조건 셋. 요소는 작동점에서 **자유 길이에 있지 않다**. 그래서 작업 하중이 없어도 힘 $F_0$를 진다. 힘–변형 선은 **평행 이동할 뿐 기울지 않는다**. 작동점 주변에서 강성은 여전히 $k$다. 그리고 **한쪽으로만** 작용하는 요소 — 접촉, 케이블, 볼트 이음 — 는 작업 하중이 예압을 다 없애지 않는 동안에만 물려 있다. 그 너머에서는 열리고 강성이 0으로 떨어진다.
>
> $$F=F_0+k\,\delta\qquad(F_0+k\,\delta>0\ \text{인 동안})$$
>
> $F$는 요소가 지는 힘, $\delta$는 작동점으로부터의 변형, $F_0$는 예압이다. 조건이 붙는 것은 한쪽으로만 작용하는 요소가 밀 수는 있어도 당길 수는 없기 때문이다. 그러므로 요소는 $F$를 양수로 유지할 만큼 작은 교란에 대해서는 보통의 양방향 스프링으로, 그 너머에서는 아무것도 아닌 것으로 행동한다.
> - **예**: 일정한 $0.4\,\mathrm{N}$으로 벽에 눌린 P3는 $y=1\,\mathrm{mm}$에 멈춰 있고, 한쪽으로만 작용하는 벽은 예압 $F_0=0.4\,\mathrm{N}$을 진다. 이제 핸들을 당기면, 당기는 힘이 $0.4\,\mathrm{N}$에 이르러 핸들을 $y=0$으로 되돌릴 때까지 벽이 양방향인 것처럼 온전한 $400\,\mathrm{N/m}$으로 맞선다. 그보다 더 당기면 접촉이 열린다.
> - **비예**: "예압이 스프링을 단단하게 만든다." 선형 스프링 하나는 어떤 예압에서도 같은 $k$를 가진다. P3의 핸들은 $0.1\,\mathrm{N}$으로 눌리든 $0.4\,\mathrm{N}$으로 눌리든 작은 추가 밀기에 $400\,\mathrm{N/m}$으로 답한다. 예압이 사는 것은 그 강성이 존재하는 범위 — 그리고 강성이 하중과 함께 커지는 접촉이라면 더 가파른 국소 기울기다.
> - **왜 중요한가**: 기구에서 유격을 없애는 방법이다 — 장력을 건 캡스턴 케이블, 예압을 준 베어링, 강구조의 고장력 볼트처럼 열리면 안 되는 볼트 이음. 그리고 눌린 접촉을 교란 동안 닫힌 채로 두는 방법이고, 누르는 모든 작업의 지지 단계가 바로 그것이다.

**실제 부품도 스프링이다.** 축 방향으로 당긴 봉은 재료가 탄성 범위에 있는 동안 하중에 비례해 늘어나고, OpenStax는 이를 영률로 $F=YA\,\Delta L/L_0$라 쓴다. 이 페이지는 13처럼 계수를 $E$로 쓴다. 스프링으로 읽으면 봉은

$$k=\frac{E\,A}{L_0}$$

이다. 단위 늘음당 힘이 계수 $E$ 곱하기 단면적 $A$ 나누기 길이 $L_0$이기 때문이다 — 단단한 재료, 굵은 봉, 짧은 봉은 저마다 더 단단한 스프링이 된다. OpenStax의 표는 강철 $E=200\,\mathrm{GPa}$, 알루미늄 $70\,\mathrm{GPa}$를 준다. 지름 $0.5\,\mathrm{mm}$, 길이 $0.1\,\mathrm{m}$의 강철선 — 이 페이지만의 예시이고 속이 찬 강철로 본다 — 은 $A=\pi(0.25\times10^{-3})^2=1.96\times10^{-7}\,\mathrm{m^2}$, $k=3.93\times10^5\,\mathrm{N/m}$다. P3의 $400\,\mathrm{N/m}$ 벽과 직렬로 두면 손이 느낄 만한 것은 아무것도 바뀌지 않는다, $1/(1/400+1/393{,}000)=399.6\,\mathrm{N/m}$. 그러나 [[04-robotics/force-compliance-control|13. §1]]이 말하는, 힘 제어기가 단단한 패널에 대해 식별하는 $10^5\,\mathrm{N/m}$과 직렬로 두면 같은 선이 사슬을 $7.97\times10^4\,\mathrm{N/m}$로, 5분의 1만큼 무르게 만든다. 굽힘을 받는 보도 스프링이다 — 외팔보 끝의 강성 $3EI/L^3$은 토목 공학자가 처음 만나는 스프링이다 — 그리고 접촉은 하중과 함께 강성이 커지는 스프링이다. 헤르츠의 결과이고, 13 §1이 강철 위의 강철 공으로 계산한다.

### 4. 감쇠와 마찰: 점성 댐퍼, 쿨롱 마찰, 정지 마찰

스프링은 에너지를 저장했다가 돌려주므로, 스프링만 달린 핸들은 영원히 울린다. 에너지를 빼내는 힘은 두 종류이고, 둘은 너무 다르게 행동해서 하나를 다른 하나로 다루는 것이 로봇 관절을 모델링할 때 가장 흔한 실수 가운데 하나다.

쉬운 말로 하면, **점성 댐퍼**는 자동차의 쇼크 업소버나 문 닫힘 장치다. 피스톤이 기름을 작은 구멍으로 밀어내는 장치여서, 천천히 밀면 거의 버티지 않고 빨리 밀면 세게 버틴다. 힘이 위치가 아니라 속도와 함께 커지기 때문이다. **마찰**은 탁자 위로 끄는 책이다. 필요한 힘은 얼마나 빨리 끄는지에 거의 달려 있지 않고, 움직이기 시작할 때는 계속 끌 때보다 조금 더 든다. P3의 $b$는 핸들의 속도에 비례해 버티는 것을 모두 숫자 하나로 묶은 것이고, 이 페이지의 $f_c$와 $f_s$가 둘째 종류를 더한다.

> **점성 댐퍼의 정의.** **점성 댐퍼**(viscous damper), 곧 대시포트는 *양 끝을 가진 이상화된 요소*로, 그 힘은 양 끝이 얼마나 빨리 멀어지거나 가까워지는지에만, 그리고 그에 비례해서 달려 있다. 정의 조건 셋. 힘은 **상대 속도에 비례한다**. 그래서 요소는 선형이다. 그 속도에 **맞선다**. 그래서 흡수하는 일률 $b\dot x^2$는 결코 음수가 아니다. 에너지를 빼내기만 한다. 그리고 **아무것도 저장하지 않는다** — 자유 길이도 질량도 없다 — 그래서 멈춰 있으면 양 끝이 어디에 있든 힘을 전혀 내지 않는다.
>
> $$F_d=-b\,\dot x,\qquad P_d=b\,\dot x^2\ge0$$
>
> $F_d$는 물체에 가하는 힘, $\dot x$는 댐퍼 양 끝의 상대 속도, $b$는 $\mathrm{N{\cdot}s/m}$ 단위의 감쇠 계수, $P_d$는 열로 바뀌는 와트 단위의 일률이다. $b$ 곱하기 제곱이므로 결코 음수가 아니다.
> - **예**: P3의 $b=0.8\,\mathrm{N{\cdot}s/m}$. $0.1\,\mathrm{m/s}$에서 $0.8\cdot0.1=0.08\,\mathrm{N}$으로 되밀고 $0.8\cdot0.1^2=8\,\mathrm{mW}$를 흡수한다. $1\,\mathrm{ms}$ 샘플 주기마다 $8\,\mathrm{\mu J}$이고, [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]가 샘플된 벽의 에너지 누설과 맞세우는 바로 그 소산이다.
> - **비예**: "댐퍼가 핸들을 벽 안에 붙잡아 줄 것이다." 멈춰 있으면 $\dot x=0$이고 댐퍼는 위치가 어디든 아무것도 밀지 않는다. 핸들을 늦출 수는 있어도 붙잡을 수는 없다. 목표 임피던스에 댐퍼뿐 아니라 스프링도 필요한 이유이고, [[04-robotics/force-compliance-control|13. §1]]도 같은 말을 한다.
> - **왜 중요한가**: 에너지를 빼내는 유일한 선형 요소이므로 스프링의 진동을 잦아들게 하는 것이 이것이고(§5), 이 페이지 위의 모든 수동성 논증은 이것이 얼마나 있는지에 대한 장부다.

댐퍼 혼자서도 알아 둘 만한 운동이 있다. 자유 공간에서 댐퍼만 작용하는 채로 P3의 핸들을 $v_0=0.1\,\mathrm{m/s}$로 놓으면, 자유물체도는 $m\dot v=-bv$를 남긴다 — [[02-foundations/engineering-math|0.5 §8]]의 1차 방정식에서 $a=-b/m=-20\,\mathrm{s^{-1}}$인 경우다 — 그러므로

$$v(t)=v_0\,e^{-t\,b/m},\qquad \int_0^\infty v\,dt=v_0\,\frac mb$$

다. $\dot v=av$의 해가 $v_0e^{at}$이고, 그 지수 함수의 적분이 $v_0/|a|$이기 때문이다. 핸들은 $m/b=50\,\mathrm{ms}$마다 속도의 $63\%$를 잃고, 모두 합쳐 $0.1\cdot0.05=5\,\mathrm{mm}$를 미끄러지며, 완전히 멈추지는 않는다.

> **쿨롱 마찰과 정지 마찰의 정의.** **쿨롱 마찰**(Coulomb friction)은 *미끄러지는 접촉의 접선력에 대한 모델*이다. 두 면이 미끄러지는 동안 힘은 크기가 일정하고 미끄럼에 맞선다. 붙어 있는 동안에는 붙어 있게 하는 데 필요한 힘이 무엇이든 그것이며, 한계까지만 그렇다. **스틱션**(stiction), 곧 정지 마찰은 그 한계와, 그것이 미끄럼 값보다 크다는 사실을 가리킨다. 정의 조건은 OpenStax가 두 법칙을 말하는 대로 셋이다. **미끄럼**: 크기는 $f_c=\mu_kN$으로, 법선력 $N$과 두 재료가 정하며 속도와 접촉 면적에 거의 무관하다. **붙음**: 미끄럼 속도가 0이면 마찰력은 다른 힘들이 요구하는 값을 $f_s=\mu_sN$까지 무엇이든 가지므로 그 힘들과 정확히 균형을 이룰 수 있다. **이탈이 미끄럼보다 크다**: $\mu_s>\mu_k$이므로 운동을 시작하는 데 계속하는 것보다 큰 힘이 든다.
>
> $$F_f=-f_c\,\mathrm{sgn}(\dot x)\ \ (\dot x\ne0),\qquad |F_f|\le f_s\ \ (\dot x=0)$$
>
> $F_f$는 움직이는 물체에 작용하는 마찰력, $\mathrm{sgn}$은 미끄럼 속도의 부호, $f_c$와 $f_s$는 뉴턴 단위의 미끄럼 힘과 이탈 힘, $\mu_k$와 $\mu_s$는 운동 마찰 계수와 정지 마찰 계수다. 첫째 경우는 미끄러지는 접촉이 늘 같은 힘으로 자기 운동에 맞선다는 말이고, 둘째 경우는 붙은 접촉이 다른 힘들이 필요로 하는 것을 $f_s$까지 무엇이든 댄다는 말이다 — 첫째는 등식인데 둘째가 부등식인 이유다.
> - **예**: P3의 가이드에 준 이 페이지의 $f_c=0.02$, $f_s=0.05\,\mathrm{N}$. 벽과 댐퍼를 치운 채 $0.1\,\mathrm{m/s}$로 튕기면 핸들은 $f_c/m=0.02/0.04=0.5\,\mathrm{m/s^2}$로 감속해 $0.1/0.5=0.2\,\mathrm{s}$ 뒤, $0.1^2/(2\cdot0.5)=0.01\,\mathrm{m}$를 가서 뚝 멈춘다 — 댐퍼가 미끄러지게 둔 거리의 두 배이고, 댐퍼로는 결코 닿지 못하는 유한한 시간이다.
> - **비예**: "마찰은 $b=f_c/|v|$인 댐퍼다." 그 등가 계수는 $0.1\,\mathrm{m/s}$에서 $0.2\,\mathrm{N{\cdot}s/m}$, $1\,\mathrm{mm/s}$에서 $20$, 멈추면 무한대다. 그것이 핸들에 무슨 일을 하는지는 아래 코드 뒤의 문단이 적는다.
> - **왜 중요한가**: 기구가 구별해 낼 수 있는 가장 작은 힘, 곧 힘 분해능과, 사람이 기구를 움직이려면 넘어야 하는 바닥을 정한다 — [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §1]]의 역구동성에 있는 $f_c$다. 그리고 엔코더 해상도와 함께, 양자화된 가상 벽을 수동적으로 얼마나 단단하게 구현할 수 있는지를 정한다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]).

벽 안의 핸들에 마찰이 하는 일은 손으로 계산할 수 있을 만큼 정확하고 짧아서, 아래 코드가 그것을 한다. 댐퍼를 치우고, 벽과 일정한 미는 힘은 두고, 이 페이지의 마찰을 더한다. 그러면 반 진동 하나하나가 옮겨진 중심 주위의 감쇠 없는 진동이다. 핸들이 벽 안으로 가는 동안에는 마찰이 벽의 저항에 더해지므로 미는 힘, 스프링, 마찰이 $(F-f_c)/k_w=0.95\,\mathrm{mm}$에서 균형을 이루고, 나오는 길에는 $(F+f_c)/k_w=1.05\,\mathrm{mm}$에서 균형을 이룬다. 스프링의 반 진동은 중심에 대해 거울상으로 끝나므로 전환점마다 앞의 전환점을 뒤집은 것이고, 핸들은 미는 힘과 스프링의 차이를 정지 마찰이 감당할 수 있는 첫 전환점에서 붙는다.

(코드는 영어 절에 한 번만 싣는다.)

코드는 전환점 $1.90$, $0.20$, $1.70$, $0.40$, $1.50$, $0.60$, $1.30$, $0.80$, $1.10\,\mathrm{mm}$를 출력하고, 핸들은 반 진동 아홉 번, $0.283\,\mathrm{s}$ 뒤에 $1.10\,\mathrm{mm}$에 붙는다. 벽은 $0.4\,\mathrm{N}$의 미는 힘에 맞서 $0.440\,\mathrm{N}$으로 밀고, 그 사이의 $0.040\,\mathrm{N}$을 정지 마찰이 감당한다. **그래서 마찰은 댐퍼가 아니다.** 다른 점 넷이 모두 그 숫자들에 보인다.

- **힘이 속도에 비례하지 않는다.** 댐퍼의 힘은 운동이 느려지면 줄지만 마찰의 힘은 운동이 멈출 때까지 $f_c$에 머문다. 등가 $b=f_c/|v|$가 $0.2$에서 무한대까지 가는 이유다.
- **물체를 평형에서 벗어난 곳에 붙잡는다.** 핸들은 미는 힘과 스프링이 균형을 이루는 점을 $0.1\,\mathrm{mm}$ 지나서 멈췄다. 그 점에서 $\pm f_s/k_w=\pm0.125\,\mathrm{mm}$ 안이면 어디든 쉬는 곳이 될 수 있다 — P3의 $61.4\,\mathrm{\mu m}$ 엔코더 카운트로 약 두 개다([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §4]]). 댐퍼는 어디서도 아무것도 붙잡지 못한다.
- **진동을 선형으로 줄이고 뚝 멈춘다.** 균형점 $F/k_w$에서 재면 반 진동마다 $2f_c/k_w=0.1\,\mathrm{mm}$씩 작아진다. 반 진동 동안 마찰이 가져가는 일, 곧 $f_c$ 곱하기 그 길이 $A_1+A_2$가 두 전환점 사이 $\tfrac12k_w(y-F/k_w)^2$의 감소량 $\tfrac12k_w(A_1^2-A_2^2)$과 같고, $A_1+A_2$로 나누면 $A_1-A_2=2f_c/k_w$가 남기 때문이다. 댐퍼는 대신 진동마다 같은 *비율*로 줄이고, 결코 0에 닿지 않는다.
- **선형이 아니다.** 미는 힘을 두 배로 해도 마찰은 두 배가 되지 않으므로 중첩이 깨지고([[02-foundations/engineering-math|0.5 §4.5]]), 선형 댐퍼에 대해 정의된 §5의 감쇠비는 마찰만 있는 핸들에는 존재하지 않는다.

에너지를 치르는 방식도 다르다. 댐퍼는 속도에 이차인 $b\dot x^2$를, 마찰은 속도에 선형인 $f_c|\dot x|$를 가져가므로, 느린 운동은 마찰이, 빠른 운동은 댐퍼가 지배한다. P3에서 둘이 같은 빠르기로 에너지를 가져가는 속도는 $f_c/b=0.02/0.8=0.025\,\mathrm{m/s}$다. 실제 관절에는 둘 다 있고, 댐퍼만 있는 모델은 하드웨어가 불감대에 멈춰 결코 하지 않는 설정점 복귀를 예측한다.

### 5. 질량–스프링–댐퍼: 고유 진동수, 감쇠비, 시정수

스프링 위의 질량은 스프링이 미는 힘과 맞비기는 곳으로 곧장 가지 않는다. 지나쳤다가 울린다. 접촉이 울리는지, 얼마나 세게, 얼마나 오래 울리는지를 이 절이 계산한다. 먼저 이야기로. 벽에 밀린 핸들은 속도를 얻다가 $1\,\mathrm{mm}$에서 스프링의 힘이 미는 힘과 같아진다. 그러나 그때 핸들은 이미 움직이고 있어서 관성이 그것을 더 데려간다. 더 깊은 곳에서는 스프링이 미는 힘보다 세게 되밀어 핸들을 늦추고, 세우고, 밖으로 되던지며, 나오는 길에도 반대쪽으로 지나친다. 흔들릴 때마다 댐퍼가 에너지를 조금씩 가져가므로 흔들림은 매번 작아지고, 핸들은 울리다가 $1\,\mathrm{mm}$에서 멈춘다. 이 이야기를 정하는 숫자는 둘이다. 얼마나 빨리 흔들리는가는 질량에 맞선 스프링이 정하고, 흔들림이 얼마나 빨리 잦아드는가는 그 둘에 맞선 댐퍼가 정한다.

§2–§4의 세 요소 — 질량, 스프링, 댐퍼 — 를 합치면, §2의 자유물체도가 로보틱스에서 진동하는 모든 것이 따르는 방정식을 준다.

$$m\ddot y+b\dot y+ky=F$$

스프링의 힘은 변형에, 댐퍼의 힘은 변형의 빠르기에 맞서고, 미는 힘이 둘 다를 구동하기 때문이다. [[02-foundations/engineering-math|0.5 §8]]이 이것을 푼다. 특수해, 곧 스프링 혼자 미는 힘과 균형을 이루는 상수 $y_{ss}=F/k$에 지수 함수 $e^{st}$로 만든 동차해를 더한다. $F=0$인 방정식에 $e^{st}$를 넣으면 지수 함수가 나누어 떨어지고 특성 방정식이 남는다.

$$ms^2+bs+k=0\quad\Longrightarrow\quad s=\frac{-b\pm\sqrt{b^2-4mk}}{2m}$$

그러므로 자유 응답이 할 수 있는 모든 것은 $b^2-4mk$의 부호가 정한다. 복소근은 울리고, 실근은 기어서 돌아온다. 두 숫자가 그것을 요약한다. 첫째는 **고유 진동수** $\omega_n=\sqrt{k/m}$, 댐퍼가 전혀 없을 때 질량이 진동할 빠르기이고, 세 영역과 함께 [[02-foundations/engineering-math|0.5 §8]]에서 정의된다. 벽 안의 P3에서는 $\sqrt{400/0.04}=100\,\mathrm{rad/s}$, 곧 $15.9\,\mathrm{Hz}$, 주기 $62.8\,\mathrm{ms}$다. 둘째가 영역을 정한다.

> **감쇠비와 임계 감쇠의 정의.** **감쇠비**(damping ratio) $\zeta$는 *질량–스프링–댐퍼의 무차원 수*다. 실제 감쇠를 **임계 감쇠**(critical damping) $b_c$, 곧 더 이상 진동하지 않게 되는 가장 작은 감쇠로 나눈 것이다. 정의 조건 셋. **질량과 스프링을 둘 다 가진 선형 2차 시스템**, $m>0$이고 $k>0$인 시스템에 속한다 — 스프링 없이 댐퍼에 달린 질량에는 $\zeta$가 없다. 임계값은 $ms^2+bs+k=0$의 두 근이 **복소수이기를 멈추는** 곳, 판별식 $b^2-4mk$가 0에 이르는 곳이므로 $b_c=2\sqrt{km}$다. 그리고 이 비가 응답을 [[02-foundations/engineering-math|0.5 §8]]의 세 영역으로 나눈다. $0<\zeta<1$은 줄어드는 포락선 안에서 울리고, $\zeta=1$은 건너가지 않고 가장 빨리 돌아오며, $\zeta>1$은 두 실근을 타고 기어서 돌아온다.
>
> $$\zeta=\frac{b}{b_c}=\frac{b}{2\sqrt{km}},\qquad s_{1,2}=-\zeta\omega_n\pm\omega_n\sqrt{\zeta^2-1}$$
>
> $b$는 감쇠 계수, $k$는 강성, $m$은 질량, $s_{1,2}$는 그 지수 함수 $e^{st}$가 자유 응답을 이루는 두 근이다. 둘째 꼴은 특성 방정식을 $m$으로 나누고 $b/m=2\zeta\omega_n$, $k/m=\omega_n^2$로 쓰면 첫째 꼴에서 나온다.
> - **예**: 벽 안의 P3. $b_c=2\sqrt{400\cdot0.04}=8.0\,\mathrm{N{\cdot}s/m}$이므로 자기 $b=0.8$이 $\zeta=0.8/8=0.10$을 준다. 손으로 쥐면 $b_c=2\sqrt{800\cdot0.04}=11.3$, $b+b_h=8.8$이 $\zeta=0.78$을 준다. 손의 $b_h=8\,\mathrm{N{\cdot}s/m}$은 공교롭게도 맨 핸들의 임계 감쇠와 정확히 같다.
> - **비예**: "임계 감쇠가 가장 빨리 정착한다." 임계 감쇠는 *오버슈트 없이* 가장 빨리 돌아오는 것이다. $2\%$ 띠 안으로는 랩의 $\zeta=0.78$ 행이 $36.1\,\mathrm{ms}$에 들어오고 $\zeta=1$은 $58.3\,\mathrm{ms}$가 걸린다. 띠의 폭만큼 넘어서도 되는 응답이 더 빨리 도착하기 때문이다(§10).
> - **왜 중요한가**: $m$, $b$, $k$만으로 접촉이 울릴지를 예측하는 숫자 하나이고, [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]가 오버슈트와 정착 시간으로 바꾸는 숫자이며, [[04-robotics/force-compliance-control|13. §2]]가 목표 임피던스에 요구하는 숫자다.

벽을 $400\,\mathrm{N/m}$에 두고 $b$만 바꾸면 P3가 세 영역을 모두 보인다.

| $b$ ($\mathrm{N{\cdot}s/m}$) | $\zeta$ | 근 $s_{1,2}$ ($\mathrm{s^{-1}}$) | 핸들이 하는 일 |
|---:|---:|---|---|
| $0.8$ | $0.10$ | $-10\pm99.5j$ | 포락선 $e^{-10t}$ 안에서 $99.5\,\mathrm{rad/s}$, 주기 $63.1\,\mathrm{ms}$로 울린다 |
| $8.0$ | $1.00$ | $-100$, $-100$ | $y_{ss}$를 건너지 않는 가장 빠른 복귀 |
| $16.0$ | $2.00$ | $-26.8$, $-373.2$ | 느린 근을 타고 기어서 돌아온다. 빠른 근은 $10\,\mathrm{ms}$ 안에 $2.4\%$로 떨어진다 |

**계단 응답과 오버슈트.** $0<\zeta<1$에서 $y=0$에 정지한 채 출발하면, 0.5 §8의 방법에 $y(0)=\dot y(0)=0$을 넣어

$$y(t)=y_{ss}\Big[1-e^{-\zeta\omega_nt}\Big(\cos\omega_dt+\frac{\zeta}{\sqrt{1-\zeta^2}}\sin\omega_dt\Big)\Big],\qquad \omega_d=\omega_n\sqrt{1-\zeta^2}$$

을 얻는다. 복소근 $-\zeta\omega_n\pm j\omega_d$가 오일러 공식에 의해 $e^{st}$를 줄어드는 코사인과 사인으로 바꾸고, 그 앞의 두 상수는 출발 위치와 속도가 정하기 때문이다. 속도 $\dot y=y_{ss}\,\omega_n(1-\zeta^2)^{-1/2}e^{-\zeta\omega_nt}\sin\omega_dt$는 $t_p=\pi/\omega_d$에서 처음 0으로 돌아오고, 거기서 코사인은 $-1$, 사인은 $0$이므로 첫 정점은

$$y_{\max}=y_{ss}\big(1+e^{-\pi\zeta/\sqrt{1-\zeta^2}}\big)$$

이다. **오버슈트**, 곧 정점이 $y_{ss}$를 넘는 양을 $y_{ss}$에 대한 비로 쓴 것은 $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$로, $\zeta$만의 함수다. 맨 핸들은 $t_p=\pi/99.5=31.6\,\mathrm{ms}$에 $M_p=0.729$다. **2% 정착 시간** $t_s$는 그 뒤로 응답이 $y_{ss}$의 $\pm2\%$ 안에 머무는 시각이다. 두 숫자 모두 §10의 랩이 출력하고, [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]가 그래프에서 읽어 낸다.

포락선 $e^{-\zeta\omega_nt}$에는 빠르기가 있고, 그 역수가 핸들에 대한 이 페이지의 마지막 정의다.

> **시정수의 정의.** **시정수**(time constant) $\tau$는 *시간*이다. 지수 함수가 줄어드는 빠르기의 역수, 곧 그것이 $e$배만큼 떨어지는 데 걸리는 시간이다. 정의 조건 셋. 그 양 — 응답, 또는 진동하는 응답의 포락선 — 이 **$e^{-t/\tau}$로 줄어든다**. $\tau$ 하나 동안 최종값까지 갈 길의 $1-e^{-1}=63\%$를 가고, $\ln50=3.9$ 시정수면 $2\%$ 안에 든다. 그리고 줄어드는 항이 여럿 있으면 정지로 다가가는 것을 지배하는 것은 **가장 느린** 항, $\tau=1/|\mathrm{Re}\,s_{\text{slow}}|$다. 빠른 항들은 먼저 사라지기 때문이다.
>
> $$\tau=\frac{1}{|\mathrm{Re}\,s_{\text{slow}}|}:\qquad \tau=\frac mb\ \ (k=0),\qquad \tau=\frac{1}{\zeta\omega_n}=\frac{2m}{b}\ \ (0<\zeta\le1),\qquad \tau=\frac{1}{\omega_n\big(\zeta-\sqrt{\zeta^2-1}\big)}\ \ (\zeta>1)$$
>
> $s_{\text{slow}}$는 0에 가장 가까운 근이다. 가장 느린 항이 가장 늦게 사라지기 때문이다. 첫째 경우는 질량과 댐퍼만 있는 경우(§4), 둘째는 울리는 응답이나 임계감쇠 응답의 포락선, 셋째는 두 실근 가운데 느린 쪽이다.
> - **예**: 자유롭게 미끄러지는 P3는 $\tau=m/b=50\,\mathrm{ms}$. 벽 안에서는 포락선의 $\tau=2m/b=100\,\mathrm{ms}$이고, $3.9\tau=391\,\mathrm{ms}$가 랩이 찾는 $2\%$ 정착 시간 $384\,\mathrm{ms}$를 어림한다. 임계감쇠면 $\tau=1/\omega_n=10\,\mathrm{ms}$다.
> - **비예**: 주기. 맨 핸들은 주기 $63.1\,\mathrm{ms}$로 울리고 $\tau=100\,\mathrm{ms}$로 줄어든다 — 서로 다른 두 숫자다. 벽을 단단하게 하면 주기는 짧아지지만 $2m/b$는 그대로다. 과제의 실행 항목이 그것을 보인다.
> - **왜 중요한가**: 정착 시간을 이루는 재료이고 — [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]는 $4/(\zeta\omega_n)$를 쓴다 — [[04-robotics/actuators-drives|10.5 §5]]가 모터의 전기적 빠르기와 기계적 빠르기를 견주는 방법이다.

울리는 그래프는 제 감쇠도 잰다. 벽 안의 핸들을 톡 치고 연속한 정점 둘을 읽으면 $\zeta$가 나온다. 방법은 아래 상자에 있고, 시스템 식별의 첫 사례다.

> [!note]- 더 깊이 · Deeper
> **그래프에서 $\zeta$ 읽기.** 울리는 응답의 연속한 정점들은 $y_{ss}$를 넘는 양이 주기마다 같은 배수 $e^{2\pi\zeta/\sqrt{1-\zeta^2}}$로 줄어든다. 포락선이 한 주기에 $e^{-\zeta\omega_n\cdot2\pi/\omega_d}$만큼 줄기 때문이다. 맨 핸들의 정점은 최종값 $1\,\mathrm{mm}$보다 $0.729$, $0.388$, $0.206$, $0.110\,\mathrm{mm}$ 높고, 각각이 다음 것의 $1.880$배다. $\ln1.880=0.631=2\pi\zeta/\sqrt{1-\zeta^2}$을 풀면 $\zeta=0.10$이 돌아온다. 그러니 벽 안의 핸들을 톡 치고 정점 둘을 읽으면 장치의 감쇠를 잰 것이다 — 측정한 응답에서 모델의 파라미터를 추정하는 첫 사례이고, 그것이 [[04-robotics/system-identification|5.5 시스템 식별]]의 주제다.

### 6. 일, 에너지, 일률

§5처럼 힘을 순간마다 따라가면 운동의 경로는 얻지만 그 청구서는 얻지 못한다. 일이 얼마나 들어갔고, 얼마나 저장되었고, 얼마나 열이 되었는가. 에너지가 그 장부를 적고, 댐퍼가 얼마를 가져가는지, 튕김이 얼마나 세게 돌아오는지 같은 물음에는 아무것도 풀지 않고 답한다.

힘이 물체에 하는 **일**은 경로를 따라 힘을 적분한 것, $W=\int\vec F\cdot d\vec x$이고, 속력 $v$로 움직이는 질량 $m$의 **운동 에너지**는 $\tfrac12mv^2$다. 일–에너지 정리는 물체에 한 알짜 일이 운동 에너지의 변화와 같다고 말한다. 스프링의 힘은 되돌릴 수 있다. 그것이 하는 일은 어디서 시작해 어디서 끝나는지에만 달려 있으므로 **퍼텐셜 에너지**를 가진다. 자유 길이에서 잰 스프링은 $\tfrac12ky^2$, 중력은 $mgh$다. OpenStax는 이런 힘을 보존력 — 어떤 닫힌 경로를 돌아도 한 일이 0 — 이라 부르고, 댐퍼나 마찰의 힘은 비보존력이라 부른다. 그것들이 가져간 에너지는 되찾을 수 없기 때문이다.

> **역학적 일률과 일의 정의.** **일률**(power)은 *빠르기*다. 힘이나 토크가 작용하는 물체에 에너지를 옮기는 빠르기다. **일**(work)은 한 구간 동안 그렇게 옮긴 에너지, 곧 일률의 시간 적분이다. 정의 조건 셋. 힘을 **그 힘이 작용하는 점의 속도**와 짝지우고 **나란한 성분**만 센다 — 내적이다 — 그래서 운동을 가로지르는 힘은 일을 하지 않는다. **부호**가 에너지가 가는 방향을 말한다. 양이면 물체로 들어가고 음이면 나간다. 그리고 **도는 물체의 토크**라면 짝은 토크와 각속도다.
>
> $$P=\vec F\cdot\vec v=\tau\,\omega,\qquad W=\int P\,dt=\int\vec F\cdot d\vec x$$
>
> $P$는 와트, $\vec F$는 힘, $\vec v$는 그 작용점의 속도, $\tau$는 토크, $\omega$는 같은 축에 대한 각속도, $W$는 줄 단위다. $W$의 둘째 꼴은 $d\vec x=\vec v\,dt$에서 나온다.
> - **예**: 카탈로그 자세에서 $19.62\,\mathrm{N{\cdot}m}$를 내며 $1\,\mathrm{rad/s}$로 위로 도는 P2의 어깨. $P=\tau\omega=19.62\,\mathrm{W}$다. 질량으로 검산하면, 둘 다 축에서 수평으로 $1\,\mathrm{m}$ 떨어져 있으므로 둘 다 $1\,\mathrm{m/s}$로 올라가고, 중력 에너지는 $2\cdot9.81\cdot1=19.62\,\mathrm{W}$로 는다 — 반대쪽 끝에서 본 같은 숫자다.
> - **비예**: "팔을 들고 있으면 일률이 든다." $\omega=0$이면 역학적 일률은 0이고 팔은 에너지를 얻지 않는다. 10.5의 모터가 P2를 그 자세로 붙잡으려고 태우는 $6.01\,\mathrm{W}$(10.5의 계산 절. 붙잡기가 왜 모두 열인지는 [[04-robotics/actuators-drives|10.5 §6]])는 권선의 전기적 손실이고, 브레이크라면 치르지 않을 값이다.
> - **비예**: P3 핸들에 가이드가 가하는 반력. 운동에 수직이므로 $\vec F\cdot\vec v=0$이고, 아무리 커도 일을 하지 않는다.
> - **왜 중요한가**: 일률은 전동 장치가 보존하는 양이고(§9) 모든 수동성 논증이 세는 양이다 — [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]는 샘플된 벽의 누설을 댐퍼의 $bv^2T$와 맞세운다. 그리고 나가는 일률 대 들어오는 일률의 비가 기계의 **효율** $\eta=P_{\text{out}}/P_{\text{in}}$이고, 10.5가 기어박스에 대해 그것을 정의한다.

**밀린 핸들의 장부.** §5의 운동 방정식에 $\dot y$를 곱하고 출발부터 적분하면 항마다 장부 항목 하나의 증가율이 된다. $m\ddot y\dot y$는 $\tfrac12m\dot y^2$의 도함수이고, $k_wy\dot y$는 $\tfrac12k_wy^2$의 도함수이며, 일정한 $F$라면 $F\dot y$는 $Fy$의 도함수이기 때문이다. 그래서 매 순간

$$F\,y=\tfrac12m\dot y^2+\tfrac12k_wy^2+\int_0^tb\,\dot y^2\,dt'$$

이다. 왼쪽은 미는 힘이 한 일이고, 오른쪽은 운동 에너지, 스프링의 에너지, 그리고 댐퍼가 지금까지 만든 열이다. 첫 정점에서 미는 힘은 $0.4\times1.729\times10^{-3}=0.692\,\mathrm{mJ}$의 일을 했고, 벽은 $\tfrac12\cdot400\cdot(1.729\times10^{-3})^2=0.598\,\mathrm{mJ}$을 지니며, 댐퍼는 $0.094\,\mathrm{mJ}$을 가져갔다. 끝에서는 $\dot y=0$, $y=F/k_w$이므로 일은 $F^2/k_w=0.4\,\mathrm{mJ}$이고 스프링은 $F^2/(2k_w)=0.2\,\mathrm{mJ}$을 지닌다. **댐퍼는 $b$가 무엇이든 미는 힘이 한 일의 정확히 절반을 가져간다.** 운동이 잦아들도록 $b>0$이기만 하면 된다. 계수는 그 청구서를 얼마나 빨리, 몇 번의 진동에 걸쳐 치르는지를 정할 뿐 크기는 결코 정하지 않는다 — §10의 랩이 행마다 보인다.

**튕김.** 벽의 표면에 $0.1\,\mathrm{m/s}$로 도착하는 핸들은 $\tfrac12\cdot0.04\cdot0.1^2=0.2\,\mathrm{mJ}$을 지닌다. 댐퍼가 없다면 벽은 $\tfrac12k_wy^2=0.2\,\mathrm{mJ}$이 되는 깊이, 곧 $v\sqrt{m/k_w}=1\,\mathrm{mm}$에서 그것을 흡수하고 온전한 속력으로 다시 내던질 것이다. 댐퍼가 있으면 $y=0$에서 속력 $v_0$로 출발한 §5의 자유 응답은 $y=(v_0/\omega_d)\,e^{-\zeta\omega_nt}\sin\omega_dt$다. 이것은 $0.863\,\mathrm{mm}$까지만 가고, 감쇠 주기의 절반인 $31.6\,\mathrm{ms}$ 뒤, 사인이 다시 0이 되는 곳에서 $0.1\times0.729=0.0729\,\mathrm{m/s}$로 표면에 돌아온다 — 오버슈트와 같은 배수 $e^{-\pi\zeta/\sqrt{1-\zeta^2}}$다. 에너지의 $0.729^2=53\%$를 지니고 나가고, 벽 밖에서도 계속 작용하는 댐퍼가 그다음 $0.0729\cdot0.05=3.6\,\mathrm{mm}$를 미끄러지는 동안 나머지를 가져간다. 감쇠가 어디에 있느냐도 모델의 일부다. 아래 상자가 그것을 보인다.

> [!note]- 더 깊이 · Deeper
> **벽 안에 넣은 같은 댐퍼.** [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터 §3]]의 낙하 셀은 장치 댐퍼를 빼고 같은 $0.8\,\mathrm{N{\cdot}s/m}$을 벽의 힘 법칙 안에 넣는다. 그 법칙은 접촉력이 0에 이르자마자, 곧 핸들이 표면에 돌아오기 조금 전에 핸들을 놓아 준다. 나오는 길에는 감쇠 항이 이미 힘을 끌어내리기 때문이다. 그래서 댐퍼가 핸들을 다시 끌어당길 틈이 없고, 튕김의 에너지 비는 $0.729^2=0.532$가 아니라 $0.554$가 된다. 같은 $k$, 같은 감쇠 계수, 같은 $\zeta$인데도 접촉 모델이 둘이면 답도 둘이다.

**회전과 효율.** 토크는 상자의 P2 예처럼 $\tau\omega$의 빠르기로 일을 하고, 실제 전동 장치는 그것을 전부 넘겨주지 못한다. 10.5가 P2의 관절에 고정한 $\eta=0.80$ 기어박스를 거치면 $1\,\mathrm{rad/s}$로 들어 올리는 데 모터에서 $19.62/0.8=24.5\,\mathrm{W}$가 들고, $4.9\,\mathrm{W}$는 기어에서 열이 된다.

### 대상으로 한 번 끝까지 · Worked case

한 장면을 자유물체도에서 에너지 장부까지 카탈로그 숫자로 끌고 간다. P3의 핸들이 벽의 표면 $y=0$에 멈춰 있고, $t=0$에 일정한 미는 힘 $F=0.4\,\mathrm{N}$이 시작된다. 핸들은 어디서 끝나고, 어떻게 거기에 가며, 댐퍼는 무엇을 가져가는가? 그다음 쥔 손을 거쳐 같은 끝점에 이른다. 일곱 단계이고, §10의 랩이 응답 숫자를 다시 계산한다.

**1단계 — 법칙.** 축을 따라 작용하는 힘은 미는 힘, 벽, 댐퍼뿐이므로 §2의 자유물체도가 준다.

$$m\ddot y+b\dot y+k_wy=F:\qquad 0.04\,\ddot y+0.8\,\dot y+400\,y=0.4$$

뉴턴 단위이고, 핸들이 벽 안에 있는 동안 성립한다. 핸들은 벽을 떠나지 않는다. 첫 정점 뒤의 가장 낮은 점이 $y_{ss}(1-M_p^2)=0.468\,\mathrm{mm}$(4단계가 $M_p$를 준다)이므로 벽의 한쪽 스위치는 결코 열리지 않고, 방정식은 내내 선형이다.

**2단계 — 어디서 끝나는가.** 멈추면 $\ddot y=\dot y=0$이고, 멈춘 핸들은 가속에 힘이 들지 않고 댐퍼의 힘도 받지 않으므로 방정식의 앞 두 항이 빠진다. 그래서 벽 혼자 미는 힘과 균형을 이룬다.

$$y_{ss}=\frac{F}{k_w}=\frac{0.4}{400}=1.0\times10^{-3}\,\mathrm{m}$$

벽 안으로 1밀리미터, $x=0.031\,\mathrm{m}$이고 벽에는 $0.4\,\mathrm{N}$이 걸린다 — $m$에도 $b$에도 전혀 달려 있지 않은 정역학의 답이다.

**3단계 — 얼마나 빠르고, 얼마나 감쇠되는가.** §5에서 $\omega_n=\sqrt{k_w/m}=\sqrt{400/0.04}=100\,\mathrm{rad/s}$, 임계 감쇠는 $b_c=2\sqrt{k_wm}=2\sqrt{16}=8.0\,\mathrm{N{\cdot}s/m}$이며, 감쇠비는 실제 감쇠를 임계 감쇠로 나눈 것이므로

$$\zeta=\frac{b}{b_c}=\frac{0.8}{8.0}=0.10$$

이다. 그러므로 핸들은 부족감쇠이고, $\omega_d=100\sqrt{1-0.01}=99.5\,\mathrm{rad/s}$, 주기 $63.1\,\mathrm{ms}$로 울린다.

**4단계 — 첫 정점.** 속도는 $t_p=\pi/\omega_d=\pi/99.5=31.6\,\mathrm{ms}$에 처음 0으로 돌아오고, 정점은 속도가 0인 곳이므로 거기서 §5의 오버슈트 식이

$$M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}=e^{-0.3157}=0.729,\qquad y_{\max}=1.729\,\mathrm{mm}$$

를 준다. 그래서 벽은 $400\times1.729\times10^{-3}=0.692\,\mathrm{N}$으로 되민다 — 미는 힘보다 $73\%$ 크다 — 그리고 $\dot y=0$이라 댐퍼가 조용하므로 핸들은 $(0.4-0.6917)/0.04=-7.29\,\mathrm{m/s^2}$로 가속한다. 그림의 자유물체도다.

**5단계 — 얼마나 오래.** 포락선의 시정수는 $\tau=2m/b=2\cdot0.04/0.8=0.1\,\mathrm{s}$이고, $\ln50\cdot\tau=0.391\,\mathrm{s}$ 뒤에 $2\%$ 안으로 떨어진다. 랩이 찾는 $2\%$ 띠에서의 정확한 마지막 이탈은 $0.384\,\mathrm{s}$다 — 1밀리미터 깊이로 끝나는 밀기 하나에 울림이 여섯 주기쯤이다.

**6단계 — 장부.** 정착하고 나면 미는 힘은 $Fy_{ss}=0.4\times10^{-3}=0.4\,\mathrm{mJ}$의 일을 했고, 벽은 $\tfrac12k_wy_{ss}^2=\tfrac12\cdot400\cdot10^{-6}=0.2\,\mathrm{mJ}$을 지니며, 댐퍼는 나머지 $0.2\,\mathrm{mJ}$을 열로 바꾸었다. 핸들이 한순간 멈춘 첫 정점에서 같은 장부는 들어온 것 $0.692$, 저장된 것 $0.598$, 소산된 것 $0.094\,\mathrm{mJ}$이었다(§6).

**7단계 — 손이 쥔다.** 이제 손이 핸들을 쥐고 표면 너머 $2\,\mathrm{mm}$인 $x_d=0.032\,\mathrm{m}$을 겨눈다. 카탈로그의 $k_h=400\,\mathrm{N/m}$, $b_h=8\,\mathrm{N{\cdot}s/m}$이고, 핸들은 다시 표면에 멈춘 채 출발한다. 손의 스프링과 댐퍼는 핸들 자신의 운동에 작용해 벽과 장치와 병렬이므로(§3), 자유물체도에 그 두 항이 더해져

$$m\ddot y+(b+b_h)\dot y+(k_w+k_h)\,y=k_h(x_d-x_w):\qquad 0.04\,\ddot y+8.8\,\dot y+800\,y=0.8$$

를 준다. 오른쪽은 $y=0$에서 손이 당기는 힘 $400\times0.002=0.8\,\mathrm{N}$이다. 핸들은 $y_{ss}=0.8/800=1.0\,\mathrm{mm}$에서 끝난다 — 같은 점이고, 벽에 $0.4\,\mathrm{N}$, 손에서 $0.4\,\mathrm{N}$, 24.4의 평형이다. 그러나 가는 길이 다르다. $\omega_n=\sqrt{800/0.04}=141.4\,\mathrm{rad/s}$, $b_c=2\sqrt{800\cdot0.04}=11.3\,\mathrm{N{\cdot}s/m}$, $\zeta=8.8/11.31=0.78$이므로 $2.05\%$만, $1.020\,\mathrm{mm}$와 $0.408\,\mathrm{N}$까지만 넘어서고, $35.3\,\mathrm{ms}$의 정점이 띠 밖으로 살짝 튀어나온 직후인 $37.0\,\mathrm{ms}$에 $2\%$ 띠 안에 자리 잡는다. 손의 스프링이 $\tfrac12\cdot400\cdot(0.002^2-0.001^2)=0.6\,\mathrm{mJ}$을 내놓고, 벽이 $0.2$를 저장하고, $0.4\,\mathrm{mJ}$이 소산된다. 두 댐퍼는 같은 $\dot y$를 보므로 그 청구서를 계수에 비례해 나눈다. 장치의 댐퍼가 $b/(b+b_h)=0.8/8.8=9.1\%$, 손이 $91\%$다.

**이 계산이 말하는 것.** 핸들 혼자서는 감쇠가 약한 진동자다. $0.4\,\mathrm{N}$으로 밀면 벽을 $0.692\,\mathrm{N}$으로 때리고 3분의 1초 동안 울리는데, 정역학의 답 — $1\,\mathrm{mm}$, $0.4\,\mathrm{N}$ — 에는 그 기미가 전혀 없다. 그것을 드러내는 것은 $\zeta$뿐이다. 쥐는 것은 끝점을 그대로 둔 채 동역학을 바꾸고, 감쇠의 10분의 9를 맡는다 — 그래서 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]는 가상 벽의 안정성을 그것을 쥔 사람의 공으로 돌리지 못하게 한다.

### 7. 회전: 토크, 관성 모멘트, 각운동량

로봇의 관절은 미끄러지지 않고 돈다. 그래서 위의 법칙들을 회전에 대해 다시 써야 한다. 무엇이 관절을 비트는가, 그리고 무엇이 그 각가속도에 맞서는가. 고정축을 도는 물체는 위의 법칙마다 그 회전판을 따른다. 토크가 힘의 자리에, 관성 모멘트가 질량의 자리에, 각속도가 속도의 자리에 선다. 고정축을 도는 강체에 대해 OpenStax는 뉴턴의 둘째 법칙을

$$\sum\tau=I\,\alpha$$

로 쓴다. $\alpha=\ddot\theta$는 $\mathrm{rad/s^2}$ 단위의 각가속도다 — 축에서 거리 $r$에 있는 질량 조각 $dm$은 원을 따라 $r\alpha$로 가속하므로 접선력 $dm\,r\alpha$, 따라서 토크 $r\cdot dm\,r\alpha$가 필요하고, 물체 전체에 걸쳐 더하면 $\big(\int r^2dm\big)\alpha$가 되기 때문이다. 식 안의 두 양에 정의를 하나씩 준다.

> **토크의 정의.** 한 점에 대한 힘의 **토크**(torque), 곧 모멘트는 *벡터*다. 그 점을 중심으로 물체를 돌리려는 힘의 경향이고, 힘 자체의 회전판이다. 정의 조건 셋. **정한 점**이나 축에 대해 잡으며, 점이 바뀌면 바뀐다. 그 점에서 힘이 작용하는 곳까지의 **위치 벡터** $\vec r$와 힘의 외적이므로, $\vec r$에 수직인 힘의 성분만 무언가를 돌리고, 크기는 힘 곱하기 **모멘트 팔** $r_\perp$, 곧 축에서 힘의 작용선까지의 수직 거리다. 그리고 평면에서 **부호**는 오른손 법칙을 따른다. 반시계 방향이 양이다.
>
> $$\vec\tau=\vec r\times\vec F,\qquad \tau_z=r_xF_y-r_yF_x=\pm F\,r_\perp$$
>
> $\tau_z$는 평면 밖으로 향하는 축 방향 성분이고 단위는 $\mathrm{N{\cdot}m}$, $r_\perp=r\sin\theta$에서 $\theta$는 $\vec r$와 $\vec F$ 사이의 각이다. 가운데 꼴은 평면 벡터 둘의 외적을 풀어 쓴 것이다. 평면 안의 벡터끼리는 평면 밖 성분만 남기 때문이다.
> - **예**: 카탈로그 자세의 P2, 어깨에 대해. $1\,\mathrm{kg}$ 질량은 각각 $9.81\,\mathrm{N}$의 무게를 가지고 축에서 오른쪽으로 $1\,\mathrm{m}$에 있으므로 무게의 토크는 $\tau_z=1\cdot(-9.81)+1\cdot(-9.81)=-19.62\,\mathrm{N{\cdot}m}$, 시계 방향이다. 어깨는 팔을 붙잡으려면 $+19.62\,\mathrm{N{\cdot}m}$를 내야 한다. 팔꿈치에 대해서는 말단의 무게가 팔꿈치 자신을 지나는 연직선을 따라 작용하므로 $r_\perp=0$이고, 팔꿈치는 아무것도 필요 없다.
> - **비예**: "토크는 무게 곱하기 링크 길이다." $\theta=(30^\circ,90^\circ)$에서 링크는 여전히 $1\,\mathrm{m}$이지만 모멘트 팔은 수평 거리 $\cos30^\circ=0.866$과 $\cos30^\circ-\sin30^\circ=0.366\,\mathrm{m}$이므로, 무게의 토크는 $19.62$가 아니라 $9.81\,(0.866+0.366)=12.09\,\mathrm{N{\cdot}m}$다.
> - **왜 중요한가**: 관절은 토크로 구동되고, 토크로 감지되고, 토크로 제한된다. 그리고 매니퓰레이터 방정식의 중력 항([[02-foundations/manipulator-kinematics-dynamics|10. §5]])은 모든 자세에서 모든 링크에 걸쳐 이 합을 취한 것이다.

> **관성 모멘트의 정의.** 축에 대한 물체의 **관성 모멘트**(moment of inertia) $I$는 *그 축 둘레로 질량이 어떻게 퍼져 있는지를 나타내는 스칼라 성질*이다. 질량의 회전판이고, $\sum\tau=I\alpha$의 그 $I$다. 정의 조건 셋, 그리고 축을 옮기는 규칙 하나. **정한 축**에 대해 잡으며, 축이 다르면 숫자도 다르다. 질량 조각 하나하나는 링크를 따라 잰 거리가 아니라 축까지의 **수직 거리의 제곱**으로 센다. 물체는 그 축에 대해 **강체**여서 도는 동안 거리가 고정되어야 한다 — P2라면 팔꿈치를 잠근다. 그리고 축을 옮기는 규칙은 **평행축 정리**다. 질량 중심을 지나는 축에 평행한 어떤 축에 대해서든, 전체 질량 곱하기 두 축 사이 거리의 제곱을 더한다.
>
> $$I=\sum_im_i\,r_i^2=\int r^2\,dm,\qquad I_{\text{axis}}=I_{\text{cm}}+m\,d^2$$
>
> $r_i$는 질량 $m_i$에서 축까지의 수직 거리, $I_{\text{cm}}$은 질량 중심을 지나는 평행축에 대한 관성 모멘트, $d$는 두 축 사이의 거리이고 단위는 $\mathrm{kg{\cdot}m^2}$다. 정리가 성립하는 것은 질량 중심에서 잰 1차 모멘트 $\int\vec r\,dm$이 0이라서 $\int|\vec r+\vec d|^2dm$에서 교차항이 빠지기 때문이다.
> - **예**: 팔꿈치를 $90^\circ$에 잠근 P2, 어깨에 대해. 팔꿈치 질량은 $1\,\mathrm{m}$, 말단 질량은 $\sqrt2\,\mathrm{m}$ 떨어져 있으므로 $I=1\cdot1^2+1\cdot(\sqrt2)^2=3\,\mathrm{kg{\cdot}m^2}$ — [[02-foundations/manipulator-kinematics-dynamics|10. §3]]이 유도하는 원소 $M_{11}=3$이다. 말단의 점질량은 $I_{\text{cm}}=0$, $d=\sqrt2\,\mathrm{m}$인 평행축 정리다.
> - **비예**: 같은 팔을 균일한 $1\,\mathrm{kg}$, $1\,\mathrm{m}$ 막대로 만든 것. 정리에 따라 링크 1은 $\tfrac1{12}+0.5^2=\tfrac13$, 전완은 $\tfrac1{12}+1.25=\tfrac43\,\mathrm{kg{\cdot}m^2}$이므로 $I=3$이 아니라 $1.667$이다. 같은 2킬로그램이 축 가까이 퍼져 있으니 휘두르기가 $44\%$ 쉽다. 질량만으로는 물체를 돌리기가 얼마나 어려운지 알 수 없다.
> - **왜 중요한가**: 각가속도 하나에 토크가 얼마나 드는지를 정하고, 기어가 $n^2$배로 곱하는 것이 이것이며(§9), 관절이 있는 팔에서는 자세에 따라 변하는 [[02-foundations/manipulator-kinematics-dynamics|10. §3]]의 질량 행렬로 자란다.

두 정의는 거리를 다르게 재고, 그 차이가 아래 그림의 전부다. 관성 모멘트는 각 질량이 *축에서* 떨어진 거리를, 무게의 토크는 축에서의 *수평* 거리를 쓴다.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="팔꿈치를 90도로 잠근 P2를 카탈로그 자세와, 어깨를 30도 돌린 자세로 그렸다. 카탈로그 자세에서 9.81 N 무게 둘은 어깨의 연직선에서 1 m 떨어져 매달려 있어 유지 토크가 19.62 N·m이고, 말단의 무게는 팔꿈치를 지나므로 팔꿈치는 토크가 필요 없다. 말단은 어깨에서 루트 2 m 떨어져 있고 관성 모멘트는 3 kg·m²다. 30도 돌리면 모멘트 팔은 0.866 m와 0.366 m로, 유지 토크는 12.09 N·m로 줄지만 거리와 관성 모멘트는 그대로다.">
  <defs><marker id="bmBk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1" opacity="0.7"><line x1="54.0" y1="214.0" x2="60.0" y2="208.0"/><line x1="62.0" y1="214.0" x2="68.0" y2="208.0"/><line x1="70.0" y1="214.0" x2="76.0" y2="208.0"/><line x1="78.0" y1="214.0" x2="84.0" y2="208.0"/><line x1="86.0" y1="214.0" x2="92.0" y2="208.0"/><line x1="52.0" y1="208.0" x2="88.0" y2="208.0"/><line x1="314.0" y1="214.0" x2="320.0" y2="208.0"/><line x1="322.0" y1="214.0" x2="328.0" y2="208.0"/><line x1="330.0" y1="214.0" x2="336.0" y2="208.0"/><line x1="338.0" y1="214.0" x2="344.0" y2="208.0"/><line x1="346.0" y1="214.0" x2="352.0" y2="208.0"/><line x1="312.0" y1="208.0" x2="348.0" y2="208.0"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.6" fill="none">
    <line x1="70" y1="200" x2="70" y2="72"/><line x1="70" y1="200" x2="170" y2="100"/>
    <line x1="330" y1="252" x2="330" y2="150"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="1.5 2.5" opacity="0.7">
    <line x1="416.6" y1="196" x2="416.6" y2="230"/><line x1="366.6" y1="110" x2="366.6" y2="248"/>
  </g>
  <g stroke="currentColor" stroke-width="3" stroke-linecap="round">
    <line x1="70.0" y1="200.0" x2="170.0" y2="200.0"/><line x1="170.0" y1="200.0" x2="170.0" y2="100.0"/>
    <line x1="330.0" y1="200.0" x2="416.6" y2="150.0"/><line x1="416.6" y1="150.0" x2="366.6" y2="63.4"/>
  </g>
  <g fill="currentColor"><circle cx="170.0" cy="200.0" r="7"/><circle cx="170.0" cy="100.0" r="7"/><circle cx="416.6" cy="150.0" r="7"/><circle cx="366.6" cy="63.4" r="7"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="70" cy="200" r="5"/><circle cx="330" cy="200" r="5"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <polyline points="170,209 170,246" marker-end="url(#bmBk)"/><polyline points="170,109 170,146" marker-end="url(#bmBk)"/>
    <polyline points="416.6,159 416.6,194" marker-end="url(#bmBk)"/><polyline points="366.6,72 366.6,108" marker-end="url(#bmBk)"/>
    <path d="M 58.5 183.6 A 20 20 0 0 0 58.5 216.4" marker-end="url(#bmBk)"/><path d="M 318.5 183.6 A 20 20 0 0 0 318.5 216.4" marker-end="url(#bmBk)"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.1">
    <polyline points="120,80 72,80" marker-end="url(#bmBk)"/><polyline points="120,80 168,80" marker-end="url(#bmBk)"/>
    <polyline points="373.3,230 332,230" marker-end="url(#bmBk)"/><polyline points="373.3,230 414.6,230" marker-end="url(#bmBk)"/>
    <polyline points="348.3,248 332,248" marker-end="url(#bmBk)"/><polyline points="348.3,248 364.6,248" marker-end="url(#bmBk)"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="12" y="18">θ = (0°, 90°), 카탈로그 자세</text>
    <text x="12" y="34">유지 τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"> = 9.81·1 + 9.81·1 = 19.62 N·m</tspan></text>
    <text x="12" y="50">I = 1·1² + 1·(√2)² = 3 kg·m²</text>
    <text x="120" y="74" text-anchor="middle">모멘트 팔 둘 다 1 m</text>
    <text x="80" y="140">r = √2 m</text>
    <text x="180" y="100">9.81 N</text>
    <text x="180" y="128">작용선이 팔꿈치를 지남:</text>
    <text x="180" y="142">τ<tspan dy="3" font-size="10">2</tspan><tspan dy="-3"> = 0</tspan></text>
    <text x="176" y="242">9.81 N</text>
    <text x="30" y="192" text-anchor="middle">τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"></tspan></text>
    <text x="290" y="192" text-anchor="middle">τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"></tspan></text>
    <text x="300" y="18">θ = (30°, 90°), 팔꿈치는 그대로 90°</text>
    <text x="300" y="34">유지 τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3"> = 9.81 (0.866 + 0.366) = 12.09 N·m</tspan></text>
    <text x="300" y="50">r은 여전히 1과 √2 m: I = 3 kg·m²</text>
    <text x="422.6" y="234">0.866 m</text>
    <text x="372.6" y="252">0.366 m</text>
    <text x="428.6" y="186">9.81 N</text>
    <text x="360.6" y="96" text-anchor="end">9.81 N</text>
  </g>
</svg>

팔꿈치를 $90^\circ$에 잠근 P2를 카탈로그 자세와 어깨를 $30^\circ$ 돌린 자세로 그렸다. 팔을 돌려도 축에서의 거리 $1$과 $\sqrt2\,\mathrm{m}$는 그대로이므로 관성 모멘트는 $3\,\mathrm{kg{\cdot}m^2}$로 남는다. 무게의 모멘트 팔은 $1$과 $1\,\mathrm{m}$에서 $0.866$과 $0.366\,\mathrm{m}$로 줄므로 유지 토크는 $19.62$에서 $12.09\,\mathrm{N{\cdot}m}$로 떨어진다.

코드는 두 정의를 P2에서 계산한다 — 토크는 외적으로, 관성은 $mr^2$의 합으로 — 그림의 두 자세에서, 그리고 균일한 막대 팔은 평행축 정리로.

(코드는 영어 절에 한 번만 싣는다.)

출력은 두 각에서 모두 $I=3.000\,\mathrm{kg{\cdot}m^2}$, 무게의 모멘트 $-19.620$과 $-12.086\,\mathrm{N{\cdot}m}$(유지 토크 $+19.620$과 $+12.086$), 그리고 막대 팔의 $I=1.6667\,\mathrm{kg{\cdot}m^2}$와 $-14.715\,\mathrm{N{\cdot}m}$다. 막대는 무게도 어깨 가까이 두므로 휘두르기뿐 아니라 붙잡기도 쉽다.

**각운동량, 한 문단으로.** 고정축을 각속도 $\omega$로 도는 물체는 **각운동량** $L=I\omega$($\mathrm{kg{\cdot}m^2/s}$)를 지니고, 알짜 외부 토크는 그 변화율이다, $\sum\tau=dL/dt$ — OpenStax가 말하는 대로 $\sum F=dp/dt$의 회전판이다. 팔꿈치를 잠근 채 어깨를 $1\,\mathrm{rad/s}$로 휘두르는 P2는 $L=3\times1=3\,\mathrm{kg{\cdot}m^2/s}$와 $\tfrac12I\omega^2=1.5\,\mathrm{J}$을 지니고, 그것을 $0.5\,\mathrm{s}$에 세우려면 중력에 맞서 붙잡는 토크 위에 평균 $3/0.5=6\,\mathrm{N{\cdot}m}$가 더 든다. 운동량은 무거운 기계를 세우기 어렵게 만드는 것이다 — [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공 §1]]이 S2, 곧 건설 트랙의 5톤급 트렌치 굴착기([[05-construction-robotics/site-engineering|2.5]])의 관성을 따로 다루는 이유다 — 그리고 외부 토크가 없을 때만 보존되는데, 바닥에 고정된 팔은 그런 호사를 누리지 못한다.

### 8. 정역학: 평형과 유지 토크

자세를 붙잡고만 있는 로봇도 관절마다 중력이 요구하는 토크를 대야 하고, 그 토크를 계산하는 것이 정역학이다. 정역학은 모든 가속도를 0으로 둔 §2와 §7이다. OpenStax는 멈춰 있는 물체의 두 조건을

$$\sum\vec F=0,\qquad \sum\vec\tau=0\ \ (\text{아무 점에 대해서나})$$

로 쓴다. 멈춘 물체는 $\vec a=0$이고 $\alpha=0$이기 때문이다. 그리고 토크의 합은 편한 아무 점에 대해서나 잡아도 된다. 힘의 합이 이미 0이면 기준점을 $\vec d$만큼 옮겨도 전체 토크는 $-\vec d\times\sum\vec F=0$만큼만 바뀌기 때문이다. 로보틱스 페이지가 이 절에서 무엇보다 필요로 하는 것은 **유지 토크**(holding torque), 곧 관절이 중력에 맞서 자세를 지키려고 내야 하는 토크다.

**카탈로그 자세의 P2.** 팔 전체를 한 자유물체로 그린다. 무게 둘, 각 $9.81\,\mathrm{N}$이 $(1,0)$과 $(1,1)$에서 아래로. 받침이 어깨에서 팔에 가하는 힘 $\vec R$. 그리고 어깨 모터가 링크 1에 가하는 토크 $\tau_1$. 힘의 평형은 위쪽으로 $R_y=2\cdot9.81=19.62\,\mathrm{N}$을 주고, 어깨에 대한 토크의 평형은 $\tau_1-9.81\cdot1-9.81\cdot1=0$을 주므로 $\tau_1=+19.62\,\mathrm{N{\cdot}m}$, 반시계 방향이다. 다른 점에 대한 검산은 한 줄이면 된다. 팔꿈치에 대해 $R_y$는 $1\,\mathrm{m}$ 왼쪽에서 작용해 $(0-1)\cdot19.62=-19.62\,\mathrm{N{\cdot}m}$를 보태고, 두 무게는 팔꿈치를 지나는 선 위에서 작용해 아무것도 보태지 않으며, 짝힘(couple)이라 어느 점에 대해서나 같은 $\tau_1$이 $+19.62$를 보탠다. 합은 마땅히 0이다. 전완 혼자도 자유물체다. 말단의 무게 $9.81\,\mathrm{N}$과 팔꿈치가 전완을 위로 받치는 $9.81\,\mathrm{N}$이 한 연직선 위에서 작용하므로 팔꿈치의 유지 토크는 $\tau_2=0$이다.

**자세에 걸쳐.** 팔꿈치를 $90^\circ$에, 어깨를 $\theta_1$에 두면 팔꿈치 질량은 어깨에서 수평으로 $\cos\theta_1$, 말단 질량은 $\cos\theta_1-\sin\theta_1$에 있고, 무게마다의 토크는 $9.81\,\mathrm{N}$ 곱하기 그 수평 거리이므로

$$\tau_1(\theta_1)=9.81\,\big(2\cos\theta_1-\sin\theta_1\big)\ \mathrm{N{\cdot}m}$$

이다. $\theta_1=0$에서 $19.62$, $30^\circ$에서 $12.09$(§7의 코드)이고, 도함수 $-9.81\,(2\sin\theta_1+\cos\theta_1)$이 0인 곳, 곧 $\tan\theta_1=-\tfrac12$, $\theta_1=-26.57^\circ$에서 가장 커서 $\tau_1=9.81\sqrt5=21.94\,\mathrm{N{\cdot}m}$다. 카탈로그 자세만 보고 고른 관절은 최악의 자세에서 $11\%$ 모자라고, [[04-robotics/actuators-drives|10.5]]는 두 자세 모두에서 구동계를 점검한다.

**말단의 하중.** 말단에 매단 페이로드는 무게 곱하기 모멘트 팔을 더한다. P2가 건설 트랙의 외장 패널, S1의 $20\,\mathrm{kg}$([[05-construction-robotics/site-engineering|2.5]])을 카탈로그 자세의 말단에 든다면 어깨에는 $19.62+20\cdot9.81\cdot1=215.8\,\mathrm{N{\cdot}m}$, 자기 유지 토크의 열한 배가 든다 — 그리고 팔꿈치는 여전히 아무것도 필요 없다. 말단이 팔꿈치 바로 위에 있기 때문이다. 하중이 어디에 매달리는지가 무게만큼이나 중요하다.

**벽 안에 붙잡힌 P3.** 쥔 핸들의 정역학은 운동을 뺀 계산 절 7단계다. 손이 당기는 힘 $k_h(x_d-x)$가 벽이 미는 힘 $k_w(x-x_w)$와 같아서 핸들은 $x=0.031\,\mathrm{m}$에 양쪽 $0.4\,\mathrm{N}$으로 놓인다 — 그리고 손은 셋째 법칙에 따라 벽의 $0.4\,\mathrm{N}$을 핸들을 통해 느낀다.

### 9. 지렛대와 기어: 비, 토크, 속도, 반사 관성

모터는 빠르고 약한데 관절은 느리고 강해야 한다. 지렛대나 기어가 그 맞바꿈을 하고, 이 절은 그 값을 센다. **지렛대**는 받침점을 중심으로 도는 강체 막대다. 받침점에서 $a$ 거리에 힘 $F_{\text{in}}$, $c$ 거리에 하중 $F_{\text{out}}$이 있으면 §8의 토크 평형이 $F_{\text{in}}\,a=F_{\text{out}}\,c$를 주고, 막대가 강체이므로 두 점은 같은 비로 호를 그린다, $s_{\text{in}}/s_{\text{out}}=a/c$. 그러므로

$$\frac{F_{\text{out}}}{F_{\text{in}}}=\frac{a}{c}=\frac{s_{\text{in}}}{s_{\text{out}}},\qquad F_{\text{in}}\,s_{\text{in}}=F_{\text{out}}\,s_{\text{out}}$$

— 힘을 거리와 맞바꾸고, 들어간 일과 나온 일이 같다. 기어 한 쌍, 또는 케이블을 드럼에 감는 풀리는 계속 도는 지렛대다. 비는 기하 — 잇수, 반지름 — 가 정하고 맞바꿈은 같다. 토크는 비만큼 곱해지고 속도는 비만큼 나뉘며, 잃는 것이 없으면 일률 $\tau\omega$는 그대로다. **감속비**(gear ratio)는 두 조건과 함께 [[04-robotics/actuators-drives|10.5 §2]]에서 온전히 정의되고, 실제 기어박스가 토크에서 빼는 **효율**도 거기서 정의된다. 여기서는 이 페이지의 두 장치가 가진 전동 장치 둘을 본다.

**P3의 캡스턴.** 반지름 $r_m=0.010\,\mathrm{m}$의 모터 풀리가 반지름 $r_s=0.050\,\mathrm{m}$의 섹터에 케이블을 감으므로, 섹터는 모터의 $r_m/r_s=1/5$ 빠르기로 돌며 모터 토크의 $5$배를 낸다. 핸들은 섹터의 테두리에 붙어 움직이므로 $r_s\theta_s=r_m\theta_m$만큼 가고, 핸들에 걸리는 힘은 $F=\tau_m/r_m$이다 — 섹터 반지름이 핸들의 사상에서 소거되며, [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]]이 이 미묘한 점을 펼친다. 벽이 $1\,\mathrm{mm}$에서 내는 $0.4\,\mathrm{N}$을 구현하려면 모터가 $\tau_m=0.4\cdot0.010=0.004\,\mathrm{N{\cdot}m}$를 내야 하고, 그 1밀리미터는 모터 회전으로 $0.001/0.010=0.1\,\mathrm{rad}$, $5.7^\circ$다.

**P2의 관절 기어박스.** $n=100$이면 카탈로그 유지의 $19.62\,\mathrm{N{\cdot}m}$가 이상적으로 모터에서 $0.1962\,\mathrm{N{\cdot}m}$이고, $1\,\mathrm{rad/s}$로 도는 관절은 모터를 $100\,\mathrm{rad/s}$($955\,\mathrm{rpm}$)로 돌리며, 양쪽 모두에 $19.62\,\mathrm{W}$가 흐른다. 10.5는 기어박스의 손실을 더해 모터에서 $0.2453\,\mathrm{N{\cdot}m}$가 필요하다고 계산한다.

**비가 관성에 하는 일.** 비는 토크를 한 번 곱하지만 관성은 두 번 곱하고, 운동 에너지가 그 이유를 보인다. $\omega_m=n\omega$로 도는 관성 $J_m$의 회전자는

$$\tfrac12J_m\,\omega_m^2=\tfrac12J_m(n\omega)^2=\tfrac12\big(n^2J_m\big)\,\omega^2$$

을 저장하는데, 이는 관절 자신의 속도로 도는 관성 $n^2J_m$의 에너지다 — 그래서 관절은 회전자를 $n^2J_m$으로 느낀다. 이것이 [[04-robotics/actuators-drives|10.5 §4]]에서 정의되는 **반사 관성**(reflected inertia)이다. 10.5가 P2의 구동계에 고정한 회전자 $J_m=1.0\times10^{-4}\,\mathrm{kg{\cdot}m^2}$로 하면 어깨에서 $10^4\cdot10^{-4}=1.0\,\mathrm{kg{\cdot}m^2}$, 겉에서는 보이지 않는 부품이 팔 자신의 $I=3$의 3분의 1이다. P3에서는 같은 에너지 논증에 $\omega_m=\dot x/r_m$을 넣어 핸들에서의 회전자의 겉보기 질량 $J_m/r_m^2$을 얻는다. 24.3이 P3에 고정한 회전자 $1.0\times10^{-6}\,\mathrm{kg{\cdot}m^2}$로 하면 $10^{-6}/10^{-4}=0.010\,\mathrm{kg}$, 핸들의 $0.04\,\mathrm{kg}$의 4분의 1이다.

| 전동 장치 | 비 | 토크(또는 힘), 이상적 | 속도 | 출력에서 느끼는 회전자 |
|---|---:|---|---|---|
| P2 관절 기어박스 | $n=100$ | $\times100$: $0.1962\to19.62\,\mathrm{N{\cdot}m}$ | $\div100$: $100\to1\,\mathrm{rad/s}$ | $n^2J_m=1.0\,\mathrm{kg{\cdot}m^2}$ |
| P3 캡스턴, 모터에서 핸들로 | $x=r_m\theta_m$ | $F=\tau_m/r_m$: $0.004\,\mathrm{N{\cdot}m}\to0.4\,\mathrm{N}$ | $\dot x=r_m\omega_m$ | $J_m/r_m^2=0.010\,\mathrm{kg}$ |

이 맞바꿈이 구동계 설계 문제의 전부다. 비를 키우면 토크는 비례해서 얻고 관성은 *제곱*에 비례해서 치르며, 실제 기어박스는 그 위에 마찰과 백래시를 더한다. 10.5가 P2의 어깨에서 감속비 $30$부터 $300$까지 그 맞바꿈을 풀고, 24.3이 P3의 캡스턴에서 푼다.

### 10. 랩: 벽에 밀어 넣은 핸들, 감쇠 스윕

계산 절에서 한 가지만 바꾼 것이다. 정지한 핸들을 일정한 $0.4\,\mathrm{N}$으로 $400\,\mathrm{N/m}$ 벽에 밀어 넣고, 감쇠 $b$를 P3 자신의 $0.8$부터 $32\,\mathrm{N{\cdot}s/m}$까지 여덟 값으로 바꿔 $\zeta$가 $0.1$에서 $4$까지 가게 한다. 마지막 줄은 7단계의 쥔 핸들이다. 응답은 §5의 닫힌 해를 $1.5\,\mathrm{s}$ 동안 $10\,\mathrm{\mu s}$마다 계산한 것이다 — 시뮬레이션이 아니므로 물리와 표 사이에 적분기가 끼지 않는다. 같은 방정식을 오일러 방법으로 전진시키는 것은 [[02-foundations/lab-kernel|0.7 Lab Kernel]]이다. 코드는 행마다 감쇠비, §5의 가장 느린 시정수 $1/|\mathrm{Re}\,s_{\text{slow}}|$, 오버슈트와 벽에 걸리는 최대 힘, $2\%$ 정착 시간 — 그 뒤로 깊이가 $y_{ss}$의 $\pm2\%$ 안에 머무는 첫 샘플로 잡는다 — 그리고 그때까지 댐퍼가 소산한 에너지 $\int b\dot y^2dt$를 출력한다. 마지막 적분은 사다리꼴 공식, 곧 [[02-foundations/engineering-math|0.5 §3]]의 리만 합에서 조각마다 양 끝을 평균한 것으로 더한다. 끝으로 §6의 장부 — 들어온 일에서 운동 에너지와 스프링 에너지와 열을 뺀 것 — 가 모든 행에서 닫히는지 점검한다.

(코드는 영어 절에 한 번만 싣는다.)

**스윕.** $400\,\mathrm{N/m}$ 벽 위의 감쇠 값 여덟, 나머지는 모두 고정이다. 출력된 열을 단위와 함께 옮기면 이렇다.

| $b$ ($\mathrm{N{\cdot}s/m}$) | $\zeta$ | $\tau$ (ms) | 오버슈트 (%) | 벽의 최대 힘 (N) | $t_s$ (ms) | $t_s$까지 소산 (mJ) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.80 | 0.10 | 100.0 | 72.92 | 0.692 | 383.8 | 0.1999 |
| 2.00 | 0.25 | 40.0 | 44.43 | 0.578 | 141.2 | 0.1998 |
| 4.00 | 0.50 | 20.0 | 16.30 | 0.465 | 80.8 | 0.1999 |
| 5.60 | 0.70 | 14.3 | 4.60 | 0.418 | 59.8 | 0.1998 |
| 6.24 | 0.78 | 12.8 | 1.99 | 0.408 | 36.1 | 0.1988 |
| 8.00 | 1.00 | 10.0 | 0.00 | 0.400 | 58.3 | 0.1999 |
| 16.00 | 2.00 | 37.3 | 0.00 | 0.400 | 148.8 | 0.1999 |
| 32.00 | 4.00 | 78.7 | 0.00 | 0.400 | 309.3 | 0.1999 |

코드는 $F^2/(2k_w)=0.2000\,\mathrm{mJ}$도 출력하고, 장부가 모든 행에서 닫힘을 확인하고, 쥔 핸들의 값을 준다. $\zeta=0.778$, $\tau=9.1\,\mathrm{ms}$, 오버슈트 $2.05\%$, 벽의 최대 힘 $0.408\,\mathrm{N}$, $t_s=37.0\,\mathrm{ms}$, 소산 $0.3998\,\mathrm{mJ}$, 장치 댐퍼의 몫 $0.091$이다.

**스윕 읽기.** §5와 §6의 식이 예측한 넷, 그리고 식이 뻔히 보여 주지 않은 하나.

- **감쇠는 오버슈트를, 그리고 그와 함께 힘의 튐을 줄인다.** $\zeta=0.1$의 $72.9\%$에서 $\zeta=1$부터는 없음까지 가므로, 벽의 최대 힘은 $0.692$에서 $0.400\,\mathrm{N}$으로 떨어진다. 맨 핸들을 $0.4\,\mathrm{N}$으로 벽에 누르는 사람은 한순간 $0.692\,\mathrm{N}$을 만난다 — 감쇠가 약한 벽이 주는 "튕김"의 느낌이다.
- **시정수는 임계 감쇠에서 가장 짧고**, $10\,\mathrm{ms}$, 양쪽으로 길어진다. 아래로는 $2m/b$로, 위로는 느린 근이 0 쪽으로 다가가면서($37.3$과 $78.7\,\mathrm{ms}$).
- **정착에는 최소가 있고, 그것은 $\zeta=1$이 아니다.** $\zeta=0.1$의 $383.8\,\mathrm{ms}$가 $\zeta=0.78$의 $36.1\,\mathrm{ms}$까지 떨어졌다가 다시 오른다 — $1$에서 $58.3$, $2$에서 $148.8$, $4$에서 $309.3$. 감쇠가 너무 적으면 울리고, 너무 많으면 긴다. $2\%$ 띠 안으로 가장 빨리 들어가는 것은 오버슈트가 띠 안에 딱 들어가는 $\zeta$, 곧 $0.78$의 $1.99\%$다. $\zeta=0.7$에서는 $4.60\%$ 오버슈트가 띠를 벗어났다가 돌아와야 해서 $59.8\,\mathrm{ms}$가 든다. 그 근처에서 이 지표는 들쭉날쭉하다. 쥔 핸들의 $2.05\%$ 정점은 띠 밖으로 $0.05$포인트 튀어나와 $37.0\,\mathrm{ms}$가 걸리는데, 쥐기가 $0.778$ 대신 $\zeta=0.780$을 주었다면 $25.5\,\mathrm{ms}$에 정착했을 것이다. 그 뜀 때문에 [[04-robotics/control-theory-ce397|5. 제어 이론 §5]]는 $4/(\zeta\omega_n)$를 측정이 아니라 어림으로 다룬다.
- **댐퍼의 청구서는 모든 행에서 같다.** 정착 시각까지 $0.1988$에서 $0.1999\,\mathrm{mJ}$ 사이이고, 끝에서는 $F^2/(2k_w)=0.2000\,\mathrm{mJ}$ — §6이 아무것도 풀지 않고 증명한 대로 미는 힘의 $0.4\,\mathrm{mJ}$의 절반이다. $b$는 청구서를 얼마나 빨리 치르는지를 정할 뿐 크기는 결코 정하지 않는다. 모자라는 몫은 $t_s$에 아직 움직이는 에너지이고, 여전히 움직이는 중에 정착으로 판정되는 $\zeta=0.78$ 행에서 가장 크다.
- **쥐기.** 마지막 줄이 7단계를 되풀이한다. 쥔 핸들이 소산하는 $0.4\,\mathrm{mJ}$ 가운데 장치 자신의 댐퍼가 내는 것은 $9.1\%$다.

### 11. 이 페이지가 다루지 않는 것

- **주파수 응답과 공진.** 핸들이 사인파 밀기에 어떻게 답하는지 — 작은 $\zeta$가 뾰족하게 만드는 $\omega_n$ 근처의 봉우리 — 는 [[04-robotics/control-theory-ce397|5. 제어 이론]]의 전달함수와 [[02-foundations/signal-processing|6. 신호처리]]의 필터가 다룬다.
- **코드로 방정식을 전진시키기.** 랩은 닫힌 해를 계산한다. 같은 방정식을 오일러 방법으로 전진시키는 것은 [[02-foundations/lab-kernel|0.7 Lab Kernel]]이고, 벽을 샘플하면 그 에너지에 무슨 일이 생기는지는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]가 보인다.
- **여러 물체.** 관절이 있는 팔의 관성은 자세에 따라 변하고 관절들을 서로 묶는다([[02-foundations/manipulator-kinematics-dynamics|10]]). 이 페이지는 강체 하나로 두려고 P2의 팔꿈치를 잠갔다.
- **액추에이터.** 모터, 기어박스 손실, 열, 전류 한계는 [[04-robotics/actuators-drives|10.5]]가 다룬다. 전기 회로와 유압·공압은 이 페이지 밖이고, 이 페이지의 두 자매 페이지다. [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자 §7]]은 이 페이지의 토크와 일률을 모터의 전류와 전압으로 바꾸고, [[02-foundations/fluid-power|0.6.3 유체 동력 §7]]은 기름 기둥을 §3과 같은 종류의 스프링으로 다룬다.
- **접촉과 그 제어.** 접촉 강성, 충돌, 임피던스 제어는 [[04-robotics/force-compliance-control|13]]이, 마찰 원뿔과 접촉 모드는 [[04-robotics/contact-force-tactile|9. 접촉·힘·촉각]]이 다룬다.
- **더 풍부한 마찰.** 이 페이지는 점성과 쿨롱 마찰에서 멈춘다. LuGre 계열의 강모 모델은 [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7]]에 나온다.
- **연속체 역학과 구조 역학.** 응력장, 보와 판의 진동, 피로는 구조 역학의 몫이다. 이 페이지는 봉과 외팔보의 강성만 쓴다. 허용하는 기울기와 떠는 진동수로 크기를 정하는 외팔보 카메라 브래킷 — §5의 스프링 위 질량 — 은 [[02-foundations/tools/mechanical-design-fabrication|12.9 실험을 위한 기계 설계와 제작 §6]]이다.

### 읽고 나면

- [ ] 방정식의 차원을 점검하고, 통과한 점검도 여전히 틀릴 수 있는 이유를 말한다.
- [ ] 모든 외력을, 그리고 그것만을 담은 자유물체도를 그리고 거기서 뉴턴의 둘째 법칙을 쓴다.
- [ ] 두 스프링을 무엇을 공유하는지에 따라 직렬이나 병렬로 합치고, 예압이 바꾸는 것과 바꾸지 않는 것을 말한다.
- [ ] 점성 댐퍼와 쿨롱 마찰을 숫자와 함께 네 가지 행동으로 구별한다.
- [ ] $m$, $b$, $k$에서 $\omega_n$, $\zeta$, 시정수, 오버슈트, 정착 어림을 계산하고 영역의 이름을 댄다.
- [ ] 에너지 장부 — 들어온 일, 저장된 에너지, 소산된 에너지 — 를 닫고, 일정한 밀기에서 댐퍼의 몫이 절반인 이유를 말한다.
- [ ] 토크, 평행축 정리를 쓴 관성 모멘트, 유지 토크를 계산하고, 토크와 관성을 감속비 너머로 옮긴다.

### 스스로 점검

1. P3의 감쇠는 $0.8\,\mathrm{N{\cdot}s/m}$다. 이것을 SI 기본 단위로 쓰고, $\zeta=b/(2\sqrt{km})$가 순수한 수임을 보여라.
2. 댐퍼는 핸들을 벽 안에 붙잡지 못한다. 마찰은 할 수 있는가? §4의 마찰만 있는 핸들은 어디에서 멈출 수 있는가?
3. 손과 벽이 P3의 핸들에 작용한다. 핸들의 진동에서는 병렬이고, 손의 겨눔에서는 직렬이다. 어떻게 둘 다 참일 수 있는가?
4. 스프링–댐퍼를 정지 상태에서 일정한 힘으로 밀어 정착할 때까지 둔다. 네가 한 일의 몇 분의 몇을 댐퍼가 소산하고, 왜 $b$의 크기는 상관없는가?
5. 카탈로그 자세에서 P2의 팔꿈치는 왜 유지 토크가 필요 없고, 어깨는 $19.62\,\mathrm{N{\cdot}m}$가 필요한가?
6. 기어박스의 비를 두 배로 한다. 이상적으로 출력 토크, 출력 속도, 회전자의 반사 관성은 어떻게 되는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $0.8\,\mathrm{N{\cdot}s/m}=0.8\,(\mathrm{kg\,m\,s^{-2}})\,\mathrm{s}/\mathrm{m}=0.8\,\mathrm{kg/s}$. 그러면 $\zeta$의 차원은 $(\mathrm{kg/s})/\sqrt{(\mathrm{kg/s^2})\cdot\mathrm{kg}}=(\mathrm{kg/s})/(\mathrm{kg/s})=1$이다.
> 2. 그렇다. 정지 마찰은 $f_s$까지 어떤 힘이든 내므로, 핸들은 $1\,\mathrm{mm}$의 균형점에서 $\pm f_s/k_w=\pm0.125\,\mathrm{mm}$ 안이면 어디서든 멈출 수 있다. §4의 실행은 $1.10\,\mathrm{mm}$에서 멈췄다. 댐퍼의 힘은 멈추면 0이므로 아무것도 붙잡지 못한다.
> 3. 직렬과 병렬은 그림이 아니라 스프링들이 무엇을 공유하는지가 정한다. 핸들의 운동에서는 둘이 같은 $y$만큼 변형하므로 병렬, $800\,\mathrm{N/m}$, $\omega_n=141.4\,\mathrm{rad/s}$다. 손이 겨눔점을 옮겨 만드는 힘에서는 같은 $0.4\,\mathrm{N}$이 둘을 지나므로 직렬, $200\,\mathrm{N/m}$이고, 그래서 겨눔점은 표면 너머 $2\,\mathrm{mm}$에 있다.
> 4. 절반. 끝에서 일은 $Fy_{ss}=F^2/k$이고 스프링은 $F^2/(2k)$를 지니므로, 나머지 $F^2/(2k)$가 댐퍼로 갔다. $b$는 그것이 얼마나 빨리, 몇 번의 진동에 걸쳐 일어나는지만 바꾸고, 랩은 이를 $0.2\,\mathrm{mJ}$로 일정한 열로 보인다.
> 5. 전완이 연직이므로 말단 질량의 무게는 팔꿈치를 지나는 선을 따라 작용한다. 모멘트 팔이 0이다. 어깨에 대해서는 두 무게가 모두 축에서 $1\,\mathrm{m}$에서 작용한다, $2\cdot9.81\cdot1=19.62\,\mathrm{N{\cdot}m}$.
> 6. 토크는 두 배, 속도는 절반, 반사 관성은 네 배다. $n^2$로 가기 때문이다(§9). 토크의 맞바꿈은 선형이고 관성의 대가는 이차다.

### 과제 · Problem set

Tier A. 이 페이지, 그 선수 지식, 대상 카탈로그만으로. P3와 P2는 이 페이지의 대상과 같고, 이 페이지의 미는 힘 $F=0.4\,\mathrm{N}$과 마찰을 쓰며, 각 항목이 말하는 것만 바꾼다.

1. **그리기.** 더 단단한 벽 $k_w=1600\,\mathrm{N/m}$에 맨 핸들과 같은 미는 힘으로 그림을 다시 그린다. 새 벽을 넣은 모델, 힘마다 값을 적은 첫 정점의 자유물체도, 그리고 최종 깊이, 첫 정점(깊이, 시각, 벽의 힘), 시정수를 적은 포락선, 정착 시간을 표시한 시간에 따른 깊이.
2. **유도.** (a) $1600\,\mathrm{N/m}$ 벽에서 $y_{ss}$, $\omega_n$, $b_c$, $\zeta$, $\omega_d$, $t_p$, $M_p$, 벽의 최대 힘과 정점에서의 가속도, 포락선의 시정수, $\ln50$ 정착 어림, 그리고 끝에서의 에너지 장부. (b) 이 페이지의 마찰을 두고 댐퍼를 없앴을 때, 그 벽에서의 불감대 $\pm f_s/k_w$를 마이크로미터와 P3의 $61.4\,\mathrm{\mu m}$ 엔코더 카운트로, 그리고 반 진동마다 줄어드는 폭 $2f_c/k_w$. (c) P2가 말단에 $0.5\,\mathrm{kg}$ 공구(점질량)를 들고 팔꿈치를 $90^\circ$에 잠갔다. 어깨에 대한 관성 모멘트, 카탈로그 자세의 유지 토크 $\tau_1$과 $\tau_2$, 이상적인 $n=100$ 기어박스를 거친 모터 토크. (d) 짐을 든 팔의 유지 토크는 어깨 각이 얼마일 때 가장 크고, 얼마나 큰가?
3. **실행.** §10 랩의 `response`를 영어 절의 템플릿으로 바꾸고, `?`를 모두 채우고, 그 아래의 벽 강성 스윕을 P3 자신의 $b$로 돌린다. $k_w$와 함께 바뀌는 열과 바뀌지 않는 열을 보고하고, 오버슈트는 커지는데 시정수는 모든 행에서 같은 이유를 §5에서 설명한다.

> [!note]- 그리는 법 · How to draw it
> - **모델**은 블록, 미는 힘 화살표 $F=0.4\,\mathrm{N}$, 댐퍼 $b=0.8\,\mathrm{N{\cdot}s/m}$를 그대로 두고 벽 스프링의 이름표만 $k_w=1600\,\mathrm{N/m}$로 바꾼다. 깊이 $y$는 벽의 표면에서, 벽 안쪽을 양으로 잰다.
> - **첫 정점의 자유물체도**에는 수평 힘 셋만 있다. 벽 안으로 미는 $0.4\,\mathrm{N}$, 되미는 벽의 $k_wy_{\max}=0.742\,\mathrm{N}$, 그리고 정점에서 $\dot y=0$이라 0인 댐퍼. $m\ddot y$ 화살표는 없다. 대신 그림 옆에 $\sum F=0.4-0.7418=-0.3418\,\mathrm{N}$과 $\ddot y=-8.54\,\mathrm{m/s^2}$를 적는다.
> - **시간 그래프**는 $y=0$에서 기울기 0으로 출발한다. 핸들이 정지 상태에서 출발하기 때문이다. $y_{ss}=0.25\,\mathrm{mm}$에 점선을 긋고, 첫 정점을 $0.464\,\mathrm{mm}$, $15.7\,\mathrm{ms}$에 찍는다. 이후 정점은 $2\pi/\omega_d=31.5\,\mathrm{ms}$마다 오고, $y_{ss}$를 넘는 양이 매번 $e^{2\pi\zeta/\sqrt{1-\zeta^2}}=1.37$배씩 줄어든다.
> - **포락선**은 $\tau=2m/b=100\,\mathrm{ms}$인 $y_{ss}\big(1\pm e^{-t/\tau}/\sqrt{1-\zeta^2}\big)$다 — $400\,\mathrm{N/m}$ 벽과 같은 시정수이고, 그것이 이 변형의 요점이다. 더 단단한 벽은 같은 포락선 안에서 두 배 빨리 울린다.
> - **정착 표시**는 랩이 놓는 $380\,\mathrm{ms}$ 근처에, 어림 $\ln50\cdot\tau=391\,\mathrm{ms}$ 옆에 둔다.
> - **깊이 축의 눈금**을 새 숫자에 맞춘다. 모든 것이 그림 깊이의 4분의 1이므로, 그림의 축을 그대로 쓰면 응답이 납작하게 눌린다.

> [!tip]- 정답 · Solutions
> 1. 1번의 그림에는 2(a)의 숫자가 들어간다. 최종 깊이 $0.25\,\mathrm{mm}$, $15.7\,\mathrm{ms}$에 $0.464\,\mathrm{mm}$인 첫 정점과 벽의 $0.742\,\mathrm{N}$, 들어가는 $0.4\,\mathrm{N}$과 되미는 $0.742\,\mathrm{N}$에 댐퍼 힘이 없는 자유물체도, 포락선의 $\tau=100\,\mathrm{ms}$, $380\,\mathrm{ms}$ 근처의 정착 시간. 더 단단한 벽은 더 얕게 끝나고 더 빠르고 세게 울리며 — 오버슈트 $73\%$ 대신 $85\%$ — 더 일찍 정착하지 않는다.
> 2. (a) $y_{ss}=0.4/1600=0.25\,\mathrm{mm}$. $\omega_n=\sqrt{1600/0.04}=200\,\mathrm{rad/s}$($31.8\,\mathrm{Hz}$). $b_c=2\sqrt{1600\cdot0.04}=16\,\mathrm{N{\cdot}s/m}$이므로 $\zeta=0.8/16=0.05$. $\omega_d=200\sqrt{1-0.0025}=199.75\,\mathrm{rad/s}$, $t_p=\pi/199.75=15.7\,\mathrm{ms}$. $M_p=e^{-\pi\cdot0.05/\sqrt{0.9975}}=0.854$이므로 $y_{\max}=0.464\,\mathrm{mm}$, 벽은 $1600\cdot0.464\times10^{-3}=0.742\,\mathrm{N}$으로 밀고, $\ddot y=(0.4-0.7418)/0.04=-8.54\,\mathrm{m/s^2}$. $\tau=2m/b=0.1\,\mathrm{s}$로 전과 같고 $\ln50\cdot\tau=0.391\,\mathrm{s}$(실행 항목의 결과는 $380.1\,\mathrm{ms}$). 장부: 일 $0.4\cdot0.25\times10^{-3}=0.1\,\mathrm{mJ}$, 저장 $\tfrac12\cdot1600\cdot(0.25\times10^{-3})^2=0.05\,\mathrm{mJ}$, 소산 $0.05\,\mathrm{mJ}$ — 이번에도 절반이다. (b) $f_s/k_w=0.05/1600=31.25\,\mathrm{\mu m}$로 엔코더 카운트의 약 절반이라, 엔코더는 핸들이 띠의 어디에 붙었는지조차 알려 주지 못한다. 반 진동마다 $2\cdot0.02/1600=25\,\mathrm{\mu m}$씩 줄어든다. (c) $I=1\cdot1^2+1\cdot(\sqrt2)^2+0.5\cdot(\sqrt2)^2=4\,\mathrm{kg{\cdot}m^2}$. $\tau_1=9.81\,(1+1+0.5)\cdot1=24.525\,\mathrm{N{\cdot}m}$. 공구도 팔꿈치를 지나는 연직선에 매달리므로 $\tau_2=0$. 모터에서는 $24.525/100=0.245\,\mathrm{N{\cdot}m}$. (d) 팔꿈치를 $90^\circ$에 두면 팔꿈치 질량은 어깨의 연직선에서 $\cos\theta_1$, 말단의 $1.5\,\mathrm{kg}$은 $\cos\theta_1-\sin\theta_1$에 있으므로 $\tau_1=9.81\,(2.5\cos\theta_1-1.5\sin\theta_1)$. 도함수는 $\tan\theta_1=-1.5/2.5=-0.6$, $\theta_1=-30.96^\circ$에서 0이 되고, 거기서 $\tau_1=9.81\sqrt{2.5^2+1.5^2}=28.60\,\mathrm{N{\cdot}m}$다 — 늘어난 질량이 말단에 있으므로 최악의 자세가 짐 없는 팔의 $-26.57^\circ$보다 $4.4^\circ$ 낮아진다.
> 3. 빈칸: `wn, z, yss = np.sqrt(k/m), b/(2*np.sqrt(k*m)), F/k`, `wd = wn*np.sqrt(1 - z*z)`, `y = yss*(1 - e*(np.cos(wd*t) + z/np.sqrt(1 - z*z)*np.sin(wd*t)))`, 그리고 마지막 열의 `1e3*F*F/(2*k)`. 실행하면 다음이 출력된다.
>
>    | $k_w$ (N/m) | $\zeta$ | $\tau$ (ms) | 오버슈트 (%) | 벽의 최대 힘 (N) | $t_s$ (ms) | 소산 (mJ) | $F^2/(2k_w)$ (mJ) |
>    |---:|---:|---:|---:|---:|---:|---:|---:|
>    | 100 | 0.200 | 100.0 | 52.7 | 0.611 | 392.0 | 0.7996 | 0.8000 |
>    | 200 | 0.141 | 100.0 | 63.8 | 0.655 | 370.2 | 0.3997 | 0.4000 |
>    | 400 | 0.100 | 100.0 | 72.9 | 0.692 | 383.8 | 0.1999 | 0.2000 |
>    | 800 | 0.071 | 100.0 | 80.0 | 0.720 | 382.1 | 0.0999 | 0.1000 |
>    | 1600 | 0.050 | 100.0 | 85.4 | 0.742 | 380.1 | 0.0500 | 0.0500 |
>
>    시정수가 움직이지 않는 것은 포락선의 감소율이 $\zeta\omega_n=\frac{b}{2\sqrt{km}}\sqrt{\frac km}=\frac{b}{2m}$로, 그 안에서 $k$가 소거되기 때문이다. 그래서 정착 시간도 $391\,\mathrm{ms}$ 어림 근처, $370$에서 $392\,\mathrm{ms}$ 사이에 머물고, 마지막 진동이 띠의 가장자리를 어디서 건너는지에 따라서만 오간다. 오버슈트가 커지는 것은 $\zeta=b/(2\sqrt{km})$가 $1/\sqrt k$로 떨어지기 때문이고, 최대 힘은 감쇠 없는 극한 $2F=0.8\,\mathrm{N}$ 쪽으로 오른다. 소산 에너지는 $k_w$가 두 배가 될 때마다 절반이 된다. 더 단단한 벽은 같은 힘에서 덜 저장하므로 소산할 것도 적기 때문이다. 강성은 울림과 에너지를 고르고, 그것이 얼마나 오래 가는지는 감쇠만이 고른다.

### 출처

- OpenStax, *University Physics Volume 1*(https://openstax.org/books/university-physics-volume-1, HTML로 읽음) — §1.4 차원 일관성과, 그 점검을 통과해도 식이 옳다는 증명은 아니라는 점; §5.2–5.7 뉴턴의 법칙과 자유물체도(외력만, 알짜 힘 화살표 없이, 짝의 두 힘을 함께 그리지 않음); §6.2 마찰($f_s\le\mu_sN$, $f_k=\mu_kN$, 속도와 접촉 면적에 거의 무관, $\mu_k<\mu_s$); §7.1–7.4와 §8.1–8.2 일, 일–에너지 정리, 일률, 스프링의 퍼텐셜 에너지와 보존력; §10.5–10.8과 §11.2 관성 모멘트와 평행축 정리, 토크, $\sum\tau=I\alpha$, $P=\tau\omega$, $L=I\omega$; §12.1과 §12.3 정적 평형과 영률(강철 $20.0\times10^{10}\,\mathrm{Pa}$, 알루미늄 $7.0\times10^{10}\,\mathrm{Pa}$); §15.1과 §15.5 단순 조화 운동, $F_D=-bv$, $b=\sqrt{4mk}$의 임계 감쇠.
- NIST, *Guide for the Use of the International System of Units (SI)*, SP 811, 4장(https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes) — 표 3의 고유 이름을 가진 유도 단위, $\mathrm{m/m}=1$인 라디안(§4.2.1), 힘의 모멘트의 단위를 줄이 아니라 뉴턴미터로 쓴다는 점(§4.2.2).
- 위키 안: 선형성과 2차 방정식은 [[02-foundations/engineering-math|0.5 공업수학]](§4.5, §8), P2와 P3는 [[02-foundations/lab-plants|0.6 Lab Plants]], P3의 폐루프 다항식과 손과의 평형은 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]], P2의 $M_{11}$과 $g_1$은 [[02-foundations/manipulator-kinematics-dynamics|10]], §9에서 쓴 회전자 관성은 [[04-robotics/actuators-drives|10.5]]와 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]].
- 미는 힘 $F$, 마찰 $f_c$와 $f_s$, §3의 강철선, 과제의 공구는 이 페이지만의 교육용 숫자이고, 이 페이지의 모든 숫자는 그것들과 카탈로그로부터 여기서 계산했다. 랩이 계단 응답의 숫자를 다시 계산한다. 믿지 말고 다시 계산하라.
