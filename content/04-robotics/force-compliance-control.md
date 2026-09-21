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

> [!note] Prerequisites · 선수 지식
> You need the manipulator equation and the operational-space inertia $\Lambda$ ([[02-foundations/manipulator-kinematics-dynamics|10. §2, §6]]), friction and contact modes ([[04-robotics/contact-force-tactile|Contact, Force & Tactile §2–3]]), and closed-loop stability and bandwidth ([[04-robotics/control-theory-ce397|Control Theory §5, §7]]).
> 매니퓰레이터 방정식과 작업 공간 관성 $\Lambda$([[02-foundations/manipulator-kinematics-dynamics|10. §2, §6]]), 마찰과 접촉 모드([[04-robotics/contact-force-tactile|접촉·힘·촉각 §2–3]]), 폐루프 안정성과 대역폭([[04-robotics/control-theory-ce397|제어 이론 §5, §7]])이 필요하다.

## English

*The centre of group H and a Mastery page. Stands on [[04-robotics/contact-force-tactile|9. Contact]], [[04-robotics/control-theory-ce397|5]] and [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Dynamics]].
Contact turns position error into force, so control stops being a choice between the two and becomes a choice of the relation between them.*

> [!note] First pass · 처음이라면
> Read the running object and the worked case below — they are the one calculation this page
> owes you, and they end on the single ratio that decides the whole argument. Then §1, why
> stiff position tracking becomes dangerous in contact, with the stiffness numbers, then §2
> for impedance versus admittance, then §7. §3 to §5 are what you read
> when you are actually choosing a controller rather than reading about one.

### Running object: P2, the panel, and one target impedance

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at the frozen pose $\theta=(0^\circ,90^\circ)$, tip at $(1,1)\,\mathrm{m}$, carrying a tool that seats down onto a panel lying under the tip (the forearm passes in front of the panel, out of the drawing plane, so only the tip touches it). This is the same arm, tool and panel as the running object of [[04-robotics/contact-force-tactile|9. Contact, Force & Tactile Interaction]], turned through a right angle: there the panel stands up and the question is friction, here it lies flat and the question is what *relation* the controller puts between motion and force. Every number in §1–§5 comes from this table.

| Symbol | Value | What it is |
|---|---:|---|
| $\theta$ | $(0^\circ,90^\circ)$ | P2's frozen pose, tip at $(1,1)$ m, elbow at $(1,0)$ |
| $J$ | $\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ | position Jacobian at that pose, frozen in 0.6 |
| $\Lambda$ | $\mathrm{diag}(1,2)\ \mathrm{kg}$ | operational-space inertia: $\Lambda_x=1$, $\Lambda_y=2$ kg |
| $F$ | $(0,-10)\ \mathrm{N}$ | the press commanded on the panel |
| $M_d$ | $2\ \mathrm{kg}$ | target inertia, chosen equal to $\Lambda_y$ |
| $K_d$ | $500\ \mathrm{N/m}$ | target stiffness |
| $D_d$ | $63.2\ \mathrm{N\cdot s/m}$ | target damping, the critically damped value for that $M_d,K_d$ |
| $K_e$ | $10^5\ \mathrm{N/m}$ | the series stiffness a force controller identifies here — row 3 of §1's table |
| $v$ | $0.05\ \mathrm{m/s}$ | approach speed at the instant of first touch |
| $f_s$ | $1\ \mathrm{kHz}$ | control rate |

$K_e$ is the series stiffness of tool, sensor, arm structure and panel taken together, not the panel's material stiffness; §1 is entirely about the difference, and §5 shows what each choice of row costs.

*Scope: this page teaches how to choose and size the relation between motion and force at one contact — impedance, admittance, the hybrid split, the operational-space implementation of both, and the passive compliance that acts below all of them — on one named arm. It does not teach the contact mechanics the controller is acting on (complementarity, friction cones and their linearizations, closure: [[04-robotics/contact-force-tactile|9. Contact, Force & Tactile Interaction §1–§4]]), the sampled-data limit on how stiff a virtual wall can be rendered ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]]), or how the policy in §6 is trained ([[03-deep-learning/vla/index|VLA]]).*

### Homework diagram: the two causalities over one panel, with the clock underneath

Draw it once; the problem set asks for the same drawing on the other axis.

<svg viewBox="0 0 560 594" style="max-width:100%;height:auto" role="img" aria-label="Top: P2 at theta (0, 90 degrees) pressing a panel under its tip with 10 N, the equal and opposite reaction, and the virtual 500 N/m spring in series with the real 100,000 N/m one; middle: impedance and admittance block diagrams sharing the arm-and-panel block, the torque interface and the force sensor shaded; bottom: on one millisecond axis, the 14 ms impact half-sine against one 397 ms period of the target behaviour, with 1 kHz sample ticks">
  <defs><marker id="fccA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor">
    <text x="12" y="18" font-size="12" fill-opacity="0.85" font-weight="600">arm and panel (x–y plane, to scale)</text>
    <line x1="34.4" y1="193" x2="65.6" y2="193" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <path d="M 36.2 193 L 31.2 199 M 41.5 193 L 36.5 199 M 46.8 193 L 41.8 199 M 52.1 193 L 47.1 199 M 57.4 193 L 52.4 199 M 62.7 193 L 57.7 199" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
    <path d="M 50 184 L 43 193 L 57 193 Z" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
    <rect x="114.4" y="92" width="57" height="6.4" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1" stroke-opacity="0.75"/>
    <path d="M 116.2 98.4 L 121.2 93.5 M 121.2 98.4 L 126.2 93.5 M 126.2 98.4 L 131.2 93.5 M 131.2 98.4 L 136.2 93.5 M 136.2 98.4 L 141.2 93.5 M 141.2 98.4 L 146.2 93.5 M 146.2 98.4 L 151.2 93.5 M 151.2 98.4 L 156.2 93.5 M 156.2 98.4 L 161.2 93.5 M 161.2 98.4 L 166.2 93.5 M 166.2 98.4 L 171.2 93.5" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
    <line x1="50" y1="184" x2="142" y2="184" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="142" y1="184" x2="142" y2="92" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <circle cx="50" cy="184" r="4.5" fill="currentColor"/>
    <circle cx="142" cy="184" r="4" fill="currentColor"/>
    <circle cx="142" cy="92" r="4.5" fill="currentColor"/>
    <line x1="153" y1="94" x2="153" y2="132" stroke="currentColor" stroke-width="1.8" marker-end="url(#fccA)"/>
    <line x1="142" y1="86" x2="142" y2="48" stroke="currentColor" stroke-width="1.8" marker-end="url(#fccA)"/>
    <text x="160" y="120" font-size="11">F = (0, −10) N</text>
    <text x="160" y="134" font-size="11" fill-opacity="0.85">on the panel</text>
    <text x="150" y="60" font-size="11">reaction +10 N</text>
    <text x="150" y="74" font-size="11" fill-opacity="0.85">on the robot</text>
    <text x="42" y="214" font-size="11">base (0, 0)</text>
    <text x="146" y="214" font-size="11" text-anchor="middle">elbow (1, 0)</text>
    <text x="134" y="82" font-size="11" text-anchor="end">tip (1, 1)</text>
    <text x="96" y="176" font-size="11" text-anchor="middle" fill-opacity="0.85">P2, θ = (0°, 90°)</text>
    <text x="110.4" y="104" font-size="11" text-anchor="end" fill-opacity="0.85">panel face</text>
    <line x1="314" y1="34" x2="338" y2="34" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 315 34 L 319 29 M 320.5 34 L 324.5 29 M 326 34 L 330 29 M 331.5 34 L 335.5 29 M 337 34 L 341 29" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
    <path d="M 326 34 L 326 38 L 319 40.3 L 333 45 L 319 49.7 L 333 54.3 L 319 59 L 333 63.7 L 319 68.3 L 333 73 L 319 77.7 L 333 82.3 L 319 87 L 333 91.7 L 326 94 L 326 98" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
    <rect x="317" y="98" width="18" height="4" fill="currentColor" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>
    <path d="M 326 102 L 326 102.6 L 319 102.8 L 333 103.1 L 319 103.4 L 333 103.7 L 319 104 L 333 104.3 L 319 104.7 L 333 105 L 319 105.3 L 333 105.6 L 319 105.9 L 333 106.2 L 326 106.4 L 326 107" fill="none" stroke="currentColor" stroke-width="0.9" stroke-linejoin="round"/>
    <line x1="314" y1="107" x2="338" y2="107" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 315 112 L 319 107 M 320.5 112 L 324.5 107 M 326 112 L 330 107 M 331.5 112 L 335.5 107 M 337 112 L 341 107" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
    <text x="344" y="38" font-size="11" fill-opacity="0.8">reference</text>
    <text x="344" y="62" font-size="11" xml:space="preserve">virtual K<tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1"> = 500 N/m</tspan></text>
    <text x="344" y="76" font-size="11" fill-opacity="0.85">gives 20 mm</text>
    <text x="344" y="108" font-size="11" xml:space="preserve">real K<tspan dy="3.1" font-size="11">e</tspan><tspan dy="-3.1"> = 10</tspan><tspan dy="-4.2" font-size="11">5</tspan><tspan dy="4.2"> N/m</tspan></text>
    <text x="344" y="122" font-size="11" fill-opacity="0.85">gives 0.1 mm</text>
    <text x="314" y="146" font-size="11">in series, same 10 N: ratio 200</text>
    <line x1="148" y1="91" x2="312" y2="100" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45" stroke-dasharray="2 3"/>
    <line x1="8" y1="216" x2="552" y2="216" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
    <text x="12" y="234" font-size="12" fill-opacity="0.85" font-weight="600">impedance — measure motion, command force</text>
    <rect x="428" y="258" width="120" height="92" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
    <text x="488" y="290" font-size="12" text-anchor="middle">arm + panel</text>
    <text x="488" y="307" font-size="11" text-anchor="middle" xml:space="preserve">Λ<tspan dy="3.1" font-size="11">y</tspan><tspan dy="-3.1"> = 2 kg</tspan></text>
    <text x="488" y="326" font-size="11" text-anchor="middle" xml:space="preserve">K<tspan dy="3.1" font-size="11">e</tspan><tspan dy="-3.1"> = 10</tspan><tspan dy="-4.2" font-size="11">5</tspan><tspan dy="4.2"> N/m</tspan></text>
    <rect x="12" y="258" width="88" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="56" y="273" font-size="11" text-anchor="middle">measure y, ẏ</text>
    <text x="56" y="287" font-size="11" text-anchor="middle">at the tip</text>
    <rect x="124" y="258" width="132" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="190" y="273" font-size="11" text-anchor="middle">target impedance</text>
    <text x="190" y="287" font-size="11" text-anchor="middle" xml:space="preserve">M<tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1">ë + D</tspan><tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1">ė + K</tspan><tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1">e</tspan></text>
    <rect x="276" y="258" width="100" height="36" rx="3" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>
    <text x="326" y="273" font-size="11" text-anchor="middle" xml:space="preserve">τ = J<tspan dy="-4.2" font-size="11">T</tspan><tspan dy="4.2">F</tspan></text>
    <text x="326" y="287" font-size="11" text-anchor="middle">torque interface</text>
    <line x1="100" y1="276" x2="122" y2="276" stroke="currentColor" stroke-width="1.3" marker-end="url(#fccA)"/>
    <text x="112" y="270" font-size="11" text-anchor="middle">e, ė</text>
    <line x1="256" y1="276" x2="274" y2="276" stroke="currentColor" stroke-width="1.3" marker-end="url(#fccA)"/>
    <text x="266" y="270" font-size="11" text-anchor="middle">F</text>
    <line x1="376" y1="276" x2="426" y2="276" stroke="currentColor" stroke-width="1.3" marker-end="url(#fccA)"/>
    <text x="402" y="270" font-size="11" text-anchor="middle">τ</text>
    <rect x="12" y="314" width="88" height="36" rx="3" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>
    <text x="56" y="329" font-size="11" text-anchor="middle" xml:space="preserve">F<tspan dy="3.1" font-size="11">y</tspan><tspan dy="-3.1"> at the wrist</tspan></text>
    <text x="56" y="343" font-size="11" text-anchor="middle">force sensor</text>
    <rect x="124" y="314" width="132" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="190" y="329" font-size="11" text-anchor="middle">integrate virtual</text>
    <text x="190" y="343" font-size="11" text-anchor="middle" xml:space="preserve">dynamics → y<tspan dy="3.1" font-size="11">c</tspan></text>
    <rect x="276" y="314" width="100" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="326" y="329" font-size="11" text-anchor="middle">inner position</text>
    <text x="326" y="343" font-size="11" text-anchor="middle">loop</text>
    <line x1="100" y1="332" x2="122" y2="332" stroke="currentColor" stroke-width="1.3" marker-end="url(#fccA)"/>
    <text x="112" y="326" font-size="11" text-anchor="middle" xml:space="preserve">F<tspan dy="3.1" font-size="11">y</tspan></text>
    <line x1="256" y1="332" x2="274" y2="332" stroke="currentColor" stroke-width="1.3" marker-end="url(#fccA)"/>
    <text x="266" y="326" font-size="11" text-anchor="middle" xml:space="preserve">y<tspan dy="3.1" font-size="11">c</tspan></text>
    <line x1="376" y1="332" x2="426" y2="332" stroke="currentColor" stroke-width="1.3" marker-end="url(#fccA)"/>
    <text x="402" y="326" font-size="11" text-anchor="middle">τ</text>
    <path d="M 488.0 258.0 L 488.0 248.0 L 56.0 248.0 L 56.0 256.0" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" marker-end="url(#fccA)"/>
    <text x="300" y="244" font-size="11" fill-opacity="0.85">tip motion</text>
    <path d="M 488.0 350.0 L 488.0 360.0 L 56.0 360.0 L 56.0 352.0" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" marker-end="url(#fccA)"/>
    <text x="300" y="373" font-size="11" fill-opacity="0.85">contact force</text>
    <text x="12" y="390" font-size="12" fill-opacity="0.85" font-weight="600">admittance — measure force, command motion</text>
    <text x="548" y="390" font-size="11" text-anchor="end" fill-opacity="0.8">shaded: the block each one cannot fake</text>
    <line x1="8" y1="408" x2="552" y2="408" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
    <text x="12" y="424" font-size="12" fill-opacity="0.85" font-weight="600">the clock, 0 to 400 ms, both lengths on one scale</text>
    <text x="548" y="424" font-size="12" text-anchor="end" xml:space="preserve">T / t<tspan dy="3.4" font-size="11">contact</tspan><tspan dy="-3.4"> = 28.3</tspan></text>
    <path d="M 60.0 439.0 L 540.0 439.0" fill="none" stroke="currentColor" stroke-width="6" stroke-opacity="0.75" stroke-dasharray="0.45 0.75"/>
    <text x="54" y="443" font-size="11" text-anchor="end" fill-opacity="0.85">1 kHz</text>
    <line x1="60" y1="526" x2="540" y2="526" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4"/>
    <line x1="60" y1="566" x2="540" y2="566" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <path d="M 60 566 L 60 570 M 180 566 L 180 570 M 300 566 L 300 570 M 420 566 L 420 570 M 540 566 L 540 570" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
    <text x="60" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">0</text>
    <text x="180" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">100</text>
    <text x="300" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">200</text>
    <text x="420" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">300</text>
    <text x="540" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">400</text>
    <text x="12" y="582" font-size="11" fill-opacity="0.85">t (ms)</text>
    <path d="M 60 526 L 63 525 L 66 524 L 68.9 522.9 L 71.9 521.9 L 74.9 520.9 L 77.9 519.9 L 80.9 518.9 L 83.8 518 L 86.8 517 L 89.8 516.1 L 92.8 515.1 L 95.8 514.2 L 98.7 513.3 L 101.7 512.4 L 104.7 511.6 L 107.7 510.7 L 110.7 509.9 L 113.6 509.1 L 116.6 508.4 L 119.6 507.6 L 122.6 506.9 L 125.6 506.2 L 128.5 505.6 L 131.5 505 L 134.5 504.4 L 137.5 503.8 L 140.5 503.3 L 143.5 502.8 L 146.4 502.4 L 149.4 502 L 152.4 501.6 L 155.4 501.3 L 158.4 501 L 161.3 500.7 L 164.3 500.5 L 167.3 500.3 L 170.3 500.2 L 173.3 500.1 L 176.2 500 L 179.2 500 L 182.2 500 L 185.2 500.1 L 188.2 500.2 L 191.1 500.3 L 194.1 500.5 L 197.1 500.7 L 200.1 501 L 203.1 501.3 L 206 501.6 L 209 502 L 212 502.4 L 215 502.8 L 218 503.3 L 220.9 503.8 L 223.9 504.4 L 226.9 505 L 229.9 505.6 L 232.9 506.2 L 235.8 506.9 L 238.8 507.6 L 241.8 508.4 L 244.8 509.1 L 247.8 509.9 L 250.7 510.7 L 253.7 511.6 L 256.7 512.4 L 259.7 513.3 L 262.7 514.2 L 265.6 515.1 L 268.6 516.1 L 271.6 517 L 274.6 518 L 277.6 518.9 L 280.5 519.9 L 283.5 520.9 L 286.5 521.9 L 289.5 522.9 L 292.5 524 L 295.4 525 L 298.4 526 L 301.4 527 L 304.4 528 L 307.4 529.1 L 310.4 530.1 L 313.3 531.1 L 316.3 532.1 L 319.3 533.1 L 322.3 534 L 325.3 535 L 328.2 535.9 L 331.2 536.9 L 334.2 537.8 L 337.2 538.7 L 340.2 539.6 L 343.1 540.4 L 346.1 541.3 L 349.1 542.1 L 352.1 542.9 L 355.1 543.6 L 358 544.4 L 361 545.1 L 364 545.8 L 367 546.4 L 370 547 L 372.9 547.6 L 375.9 548.2 L 378.9 548.7 L 381.9 549.2 L 384.9 549.6 L 387.8 550 L 390.8 550.4 L 393.8 550.7 L 396.8 551 L 399.8 551.3 L 402.7 551.5 L 405.7 551.7 L 408.7 551.8 L 411.7 551.9 L 414.7 552 L 417.6 552 L 420.6 552 L 423.6 551.9 L 426.6 551.8 L 429.6 551.7 L 432.5 551.5 L 435.5 551.3 L 438.5 551 L 441.5 550.7 L 444.5 550.4 L 447.4 550 L 450.4 549.6 L 453.4 549.2 L 456.4 548.7 L 459.4 548.2 L 462.4 547.6 L 465.3 547 L 468.3 546.4 L 471.3 545.8 L 474.3 545.1 L 477.3 544.4 L 480.2 543.6 L 483.2 542.9 L 486.2 542.1 L 489.2 541.3 L 492.2 540.4 L 495.1 539.6 L 498.1 538.7 L 501.1 537.8 L 504.1 536.9 L 507.1 535.9 L 510 535 L 513 534 L 516 533.1 L 519 532.1 L 522 531.1 L 524.9 530.1 L 527.9 529.1 L 530.9 528 L 533.9 527 L 536.9 526" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <line x1="536.9" y1="561" x2="536.9" y2="571" stroke="currentColor" stroke-width="1.4"/>
    <line x1="536.9" y1="526" x2="536.9" y2="561" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4" stroke-dasharray="2 2"/>
    <text x="100.8" y="548" font-size="11" xml:space="preserve">one period of the target: T = 2π/ω<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 397 ms</tspan></text>
    <path d="M 60 526 L 60.4 522.1 L 60.8 518.3 L 61.3 514.5 L 61.7 510.8 L 62.1 507.2 L 62.5 503.7 L 63 500.3 L 63.4 497.1 L 63.8 494.1 L 64.2 491.2 L 64.6 488.6 L 65.1 486.2 L 65.5 484.1 L 65.9 482.2 L 66.3 480.6 L 66.7 479.2 L 67.2 478.2 L 67.6 477.4 L 68 477 L 68.4 476.8 L 68.9 477 L 69.3 477.4 L 69.7 478.2 L 70.1 479.2 L 70.5 480.6 L 71 482.2 L 71.4 484.1 L 71.8 486.2 L 72.2 488.6 L 72.6 491.2 L 73.1 494.1 L 73.5 497.1 L 73.9 500.3 L 74.3 503.7 L 74.8 507.2 L 75.2 510.8 L 75.6 514.5 L 76 518.3 L 76.4 522.1 L 76.9 526" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"/>
    <text x="81.6" y="484" font-size="11">impact: half-sine,</text>
    <text x="81.6" y="498" font-size="11" xml:space="preserve">14 ms, F<tspan dy="3.1" font-size="11">max</tspan><tspan dy="-3.1"> = 22.4 N</tspan></text>
    <rect x="346" y="451" width="192" height="60" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
    <path d="M 346 451 L 346 457 M 355.6 451 L 355.6 457 M 365.2 451 L 365.2 457 M 374.8 451 L 374.8 457 M 384.4 451 L 384.4 457 M 394 451 L 394 457 M 403.6 451 L 403.6 457 M 413.2 451 L 413.2 457 M 422.8 451 L 422.8 457 M 432.4 451 L 432.4 457 M 442 451 L 442 457 M 451.6 451 L 451.6 457 M 461.2 451 L 461.2 457 M 470.8 451 L 470.8 457 M 480.4 451 L 480.4 457 M 490 451 L 490 457 M 499.6 451 L 499.6 457 M 509.2 451 L 509.2 457 M 518.8 451 L 518.8 457 M 528.4 451 L 528.4 457 M 538 451 L 538 457" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.75"/>
    <path d="M 346 508 L 349.4 504.1 L 352.7 500.3 L 356.1 496.5 L 359.5 492.8 L 362.9 489.2 L 366.2 485.7 L 369.6 482.3 L 373 479.1 L 376.3 476.1 L 379.7 473.2 L 383.1 470.6 L 386.5 468.2 L 389.8 466.1 L 393.2 464.2 L 396.6 462.6 L 400 461.2 L 403.3 460.2 L 406.7 459.4 L 410.1 459 L 413.4 458.8 L 416.8 459 L 420.2 459.4 L 423.6 460.2 L 426.9 461.2 L 430.3 462.6 L 433.7 464.2 L 437 466.1 L 440.4 468.2 L 443.8 470.6 L 447.2 473.2 L 450.5 476.1 L 453.9 479.1 L 457.3 482.3 L 460.6 485.7 L 464 489.2 L 467.4 492.8 L 470.8 496.5 L 474.1 500.3 L 477.5 504.1 L 480.9 508" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>
    <path d="M 346 508 L 350.8 507.8 L 355.6 507.6 L 360.4 507.4 L 365.2 507.2 L 370 507 L 374.8 506.8 L 379.6 506.6 L 384.4 506.4 L 389.2 506.2 L 394 505.9 L 398.8 505.7 L 403.6 505.5 L 408.4 505.3 L 413.2 505.1 L 418 504.9 L 422.8 504.7 L 427.6 504.5 L 432.4 504.3 L 437.2 504.1 L 442 503.9 L 446.8 503.7 L 451.6 503.5 L 456.4 503.3 L 461.2 503.1 L 466 502.9 L 470.8 502.7 L 475.6 502.5 L 480.4 502.3 L 485.2 502.1 L 490 501.9 L 494.8 501.7 L 499.6 501.5 L 504.4 501.3 L 509.2 501.1 L 514 500.9 L 518.8 500.7 L 523.6 500.5 L 528.4 500.3 L 533.2 500.1 L 538 499.9" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <text x="340" y="467" font-size="11" text-anchor="end" fill-opacity="0.85">first 20 ms, ×8: one tick</text>
    <text x="340" y="481" font-size="11" text-anchor="end" fill-opacity="0.85">per sample, 14 in the impact</text>
  </g>
</svg>

**Top — the arm and the panel, in the $x$–$y$ plane, to scale.** P2's base at the origin, link 1 along $+x$ to the elbow at $(1,0)$, link 2 up to the tip at $(1,1)$. A horizontal line under the tip for the panel's face (the forearm passes in front of the panel, out of the drawing plane, so only the tip touches it), with the commanded press $F=(0,-10)$ N drawn as a downward arrow at the tip and the reaction on the robot as an upward arrow of the same length. Beside the tip, two small springs in series and labelled: the virtual one, $K_d=500$ N/m, and the real one, $K_e=10^5$ N/m — drawn with the virtual spring's coils stretched out and the real one's compressed almost flat, because that ratio of 200 is the picture's only job.

**Middle — the two block diagrams, one above the other, sharing the same plant block on the right.** Impedance: measure $(y,\dot y)$ at the tip, run it through the target $M_d\ddot e+D_d\dot e+K_de$, get a force, map it with $\tau=J^\top F$, send torque to the arm. Admittance: measure $F_y$ at the wrist, integrate the virtual dynamics to get a motion reference $y_c$, hand $y_c$ to an inner position loop, and let that loop send torque. Shade the one block each architecture cannot fake — the torque interface on the top row, the force sensor on the bottom — and draw the feedback path from the panel back to the measurement in both.

**Bottom — the clock, in milliseconds, on one axis from 0 to 400 ms.** Mark the contact event as a half-sine of width $t_{\text{contact}}=14$ ms starting at $t=0$. On the same axis, draw one full period of the behaviour the controller specified, $T=2\pi/\omega_n=397$ ms, as a sine that has barely left the origin when the impact is already over. Above the clock, 1 kHz sample ticks: about 14 of them fall inside the impact and about 397 inside one period of the target. The two lengths must be drawn to the same scale — that comparison is the lecture.

### Worked case: the target impedance on P2, and the impact it cannot feel

Six steps on the object above. Everything §2 and §5 assert in words is a number here.

**Step 1 — the command, in joint coordinates.** The panel is pressed with $F=(0,-10)$ N, so

$$\tau=J^\top F=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}\begin{pmatrix}0\\-10\end{pmatrix}=\begin{pmatrix}-10\\0\end{pmatrix}\ \mathrm{N\cdot m}$$

and the elbow carries exactly none of it. That is not a rounding: the second column of $J$ is $(-1,0)^\top$, so at this pose moving the elbow alone slides the tip purely in $x$, and a purely vertical force does no work on it. Read the zero as a statement about the pose, not about the arm.

**Step 2 — the mass the panel actually meets.** $\Lambda_y=2$ kg. The arm is $m_1+m_2=2$ kg of metal, and the coincidence is a trap: $\Lambda_x=1$ kg at the *same* pose, from the same 2 kg. Apparent mass is a property of the pose and the direction, which is why §4's operational-space formulation exists and why $M_d=\Lambda_y$ is the target inertia that asks the controller for no inertia shaping at all.

**Step 3 — the static behaviour.** The panel pushes the robot up, so $F_{ext}=+10$ N, and at equilibrium the target reduces to its spring term:

$$e=\frac{F_{ext}}{K_d}=\frac{10}{500}=0.020\ \mathrm{m}$$

Two centimetres of steady-state error that the controller will never remove, and in contact that is the specification, not a failure. Unconstrained, the same 10 N would instead give $a_y=-10/2=-5\ \mathrm{m/s^2}$.

**Step 4 — the dynamic behaviour.** Reading the target as a second-order system,

$$\omega_n=\sqrt{K_d/M_d}=\sqrt{500/2}=15.81\ \mathrm{rad/s}=2.52\ \mathrm{Hz},\qquad D_d\big|_{\zeta=1}=2\sqrt{K_dM_d}=63.2\ \mathrm{N\cdot s/m}$$

because those are the standard second-order parameters ([[04-robotics/control-theory-ce397|5. Control Theory §5]]). At $\zeta=0.7$ instead, $D_d=44.3$ N·s/m. Sanity check on the damper: at $0.05$ m/s the critically damped $D_d$ contributes $63.2\times0.05=3.16$ N, a third of the press — damping is not a small correction here.

**Step 5 — whose compliance is it, in steady contact?** At the commanded 10 N the panel and structure yield $10/K_e=10/10^5=0.1$ mm while the virtual spring yields 20 mm. The controller therefore supplies $20/20.1=99.5\%$ of the total give, which is the stiffness ratio $K_e/K_d=200$ read as $200/201$. So in *sustained* contact the word "compliant" refers to the controller, and it is honest.

**Step 6 — and in the impact, whose is it?** Now arrive at $v=5$ cm/s against $K_e=10^5$ N/m. From §5's half-sine model,

$$F_{\max}=v\sqrt{\Lambda_yK_e}=0.05\sqrt{2\times10^5}=22.4\ \mathrm{N},\qquad t_{\text{contact}}=\pi\sqrt{\Lambda_y/K_e}=0.01405\ \mathrm{s}$$

so 22.4 N arrives and leaves inside 14.05 ms, and a 1 kHz loop gets about 14 samples in it. Compare that with one period of the behaviour the controller specified, $T=2\pi/\omega_n=0.397$ s:

$$\frac{T}{t_{\text{contact}}}=\frac{0.397}{0.01405}=28.3$$

**The whole impact is over in one twenty-eighth of a single period of the target dynamics**, so the behaviour the controller specified has barely started to respond by the time the event has finished. The energy argument says the same thing without the frequency domain: the tool carries $\tfrac12\Lambda_yv^2=\tfrac12(2)(0.05)^2=2.5$ mJ, the $K_d=500$ N/m virtual spring would have to compress $\sqrt{2E/K_d}=3.16$ mm to absorb it, and the tool only penetrates $\sqrt{2E/K_e}=0.22$ mm before the structure has stopped it — $7.1\%$ of the distance the commanded spring needed. The structure took the entire 2.5 mJ and gave it back.

**What that ratio means, and what changes it.** Against the compliant wrist ($K_e=10^4$) the ratio falls to $8.9$, and against the idealised material row ($10^7$) it rises to $283$. It is never anywhere near 1. Nor is 28 a tuning failure you could gain your way out of: setting $T=t_{\text{contact}}$ means $2\pi/\omega_n=\pi\sqrt{\Lambda_y/K_e}$, so $\omega_n=2\sqrt{K_e/\Lambda_y}$ and, with $M_d=\Lambda_y$,

$$K_d=4K_e=4\times10^5\ \mathrm{N/m}$$

which is 800 times the stiffness chosen here and far past what a 1 kHz loop can render against a stiff surface ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]]). The other direction — lowering $K_e$ — is a mechanical change, not a control one, which is the whole of §5's passive-compliance argument. So this is §5's claim as arithmetic: **the controller owns sustained contact and owns essentially none of the impact**, and a paper that reports a compliance gain while showing only steady contact has reported the easy half. RS1, the running study of Research Practice, compares impedance control on this arm against position control with a force-threshold stop, on a 400 N/m panel where the same half-sine lasts $\pi\sqrt{2/400}=0.222$ s; row 5 of the worked case in [[06-research-practice/research-questions-claims|1. Research Questions & Claims]] sets that against these 14 ms to show why its result does not transfer to a stiff panel.

### 1. Why stiff position tracking becomes dangerous in contact

A position controller's job is to drive position error to zero, and it does so with whatever
force that requires. In free space this is exactly right. In contact it is a specification
for breaking things, because the environment now decides what position error means.

Take the wall from [[04-robotics/contact-force-tactile|Contact, Force & Tactile §6]]:
a **compliantly mounted** tool meeting a surface at roughly $K_e = 10^4$ N/m, commanded 1 cm
past it.

$$F = K_e\,\Delta x = 10^4 \times 0.01 = 100\ \text{N}$$

The controller does not "decide" to push with 100 N. That force is simply what closing a 1 cm
error against that stiffness costs. A compliant controller rendering $K = 200$ N/m in the same
situation produces $200 \times 0.01 = 2$ N. It holds a 1 cm error it never resolves. In contact
that is the correct behaviour, not a failure.

> [!info] Definition · 정의 — stiffness, compliance, damping
> **What kind of things they are.** Three *coefficients* of a linear mechanical relation at one port, each with its own units, each answering a different question about the same contact. They are properties of a relation, not of a part — which is the condition people drop.
>
> - **Stiffness** $K$, in N/m: force per unit displacement, $F=K\,\Delta x$. It answers "what does this much position error cost me in force?"
> - **Compliance** $C=1/K$, in m/N: displacement per unit force. The same content with the question inverted — "how far does this much force move it?" The wall above, $K_e=10^4$ N/m, has $C=10^{-4}$ m/N, that is $0.1$ mm per newton; the $K=200$ N/m controller has $C=5\times10^{-3}$ m/N, $5$ mm per newton.
> - **Damping** $D$, in N·s/m: force per unit *velocity*, $F=D\,\dot x$. It is not a weaker spring. It produces no force at all once the motion stops, which is why a damper cannot hold a position and a spring cannot dissipate energy — and why §2's target needs both terms.
>
> **The defining condition, and why compliance is the useful one.** Because these describe a relation across a chain, the coefficients of elements **in series** combine through *compliance*, which simply adds:
>
> $$C_{eq}=C_1+C_2\quad\Longleftrightarrow\quad \frac{1}{K_{eq}}=\frac{1}{K_1}+\frac{1}{K_2}$$
>
> since the same force passes through both elements and their deflections add. For $C_1=10^{-5}$ and $C_2=10^{-7}$ m/N the sum is $1.010\times10^{-5}$ m/N, so $K_{eq}=9.90\times10^{4}$ N/m and the softer element contributed $99.0\%$ of the yielding. "The softest element wins" is that arithmetic, not a slogan, and §5 runs the whole impact argument on it.
>
> **Example.** The running object in sustained contact: $K_d=500$ N/m in series with $K_e=10^5$ N/m gives $C_{eq}=2\times10^{-3}+10^{-5}=2.01\times10^{-3}$ m/N, so the controller supplies $99.5\%$ of the give at the tip.
>
> **Non-examples.** "A compliant controller", with no number, is not a specification — $K_d=10^5$ N/m is also a rendered stiffness. And a *scalar* stiffness is not a specification for a directional device: a remote-centre compliance is about $10^4$ N/m laterally and $10^6$ N/m axially (§5), so one number for it is wrong in one of the two directions by two orders of magnitude.
>
> **Why it matters.** Every row of the table below, every $K_d$ in §2, the selection of which direction is stiff in §3, and the impact arithmetic in §5 are these same three coefficients. A contact claim with none of them reported is a claim with no units.

Keep a scale of environment stiffness. It spans five orders of magnitude, and papers name the
contact rather than the number. The same control law is safe at one end and impossible at the
other:

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

**Where the fourth row comes from: Hertzian contact.** Two elastic bodies touching at a point do not behave like a linear spring. For a sphere of radius $R$ pressed a depth $\delta$ into a flat, Hertz's solution gives

$$F=\tfrac43\,E^*\sqrt{R}\,\delta^{3/2},\qquad k=\frac{dF}{d\delta}=\frac{3F}{2\delta}$$

where $E^*$ is the combined elastic modulus, $1/E^*=(1-\nu_1^2)/E_1+(1-\nu_2^2)/E_2$, with Young's moduli $E_i$ and Poisson ratios $\nu_i$. The contact area grows as the bodies press together, so the local stiffness $k$ rises with load and a single $K_e$ is only a linearization at one force. For a 5 mm-radius steel ball on steel ($E=200$ GPa, $\nu=0.3$, so $E^*=110$ GPa), 10 N indents $0.98\ \mu$m with $k=1.5\times10^7$ N/m, and 100 N indents $4.5\ \mu$m with $k=3.3\times10^7$ N/m, both inside the fourth row.

The example above sits in the second row. **Commanding an unreachable penetration with high
closed-loop stiffness is dangerous.** The table is a local-linearization risk scale. It is not a
force prediction at 1 cm: extrapolating $10^7$ N/m gives $10^5$ N. Actual force is limited by the
series-equivalent controller, robot, tool, and environment stiffnesses, and by saturation. §5
uses the same two rows to compute impact forces. Always read a claim about "a stiff contact"
back to a row of this table.

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="a logarithmic stiffness axis from ten squared to ten to the eighth newtons per metre with the force a one centimetre error produces at three of them">
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="24" y="18">force produced by a 1 cm position error</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.6">
    <line x1="70" y1="112" x2="520" y2="112"/>
    <line x1="70.0" y1="112" x2="70.0" y2="120"/><line x1="145.0" y1="112" x2="145.0" y2="120"/><line x1="220.0" y1="112" x2="220.0" y2="120"/><line x1="295.0" y1="112" x2="295.0" y2="120"/><line x1="370.0" y1="112" x2="370.0" y2="120"/><line x1="445.0" y1="112" x2="445.0" y2="120"/><line x1="520.0" y1="112" x2="520.0" y2="120"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.7" text-anchor="middle">
    <text x="70.0" y="134">10²</text><text x="145.0" y="134">10³</text><text x="220.0" y="134">10⁴</text><text x="295.0" y="134">10⁵</text><text x="370.0" y="134">10⁶</text><text x="445.0" y="134">10⁷</text><text x="520.0" y="134">10⁸</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.6">
    <text x="70" y="150">foam, card</text>
    <text x="230" y="150">what a force controller identifies</text>
    <text x="470" y="150">Hertzian</text>
  </g>
  <g><line x1="92.6" y1="96" x2="92.6" y2="112" stroke="currentColor" stroke-width="1" opacity="0.45"/><circle cx="92.6" cy="96" r="4" fill="currentColor"/><line x1="220.0" y1="70" x2="220.0" y2="112" stroke="currentColor" stroke-width="1" opacity="0.45"/><circle cx="220.0" cy="70" r="4" fill="currentColor"/><line x1="445.0" y1="44" x2="445.0" y2="112" stroke="currentColor" stroke-width="1" opacity="0.45"/><circle cx="445.0" cy="44" r="4" fill="currentColor"/></g>
  <g font-size="10.5" fill="currentColor"><text x="101.6" y="100">2 N</text><text x="101.6" y="112" font-size="9" opacity="0.75">a compliant controller</text><text x="229.0" y="74">100 N</text><text x="229.0" y="86" font-size="9" opacity="0.75">compliantly mounted tool (row 2)</text><text x="436.0" y="48" text-anchor="end">100,000 N</text><text x="436.0" y="60" font-size="9" opacity="0.75" text-anchor="end">steel on steel, local material contact</text></g>
  <g font-size="9.5" fill="currentColor" opacity="0.75">
    <text x="24" y="170">environment stiffness K&#7497; (N/m), log scale</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="200">The controller does not decide to push with 100 N; that is simply what closing a 1 cm error</text>
    <text x="24" y="216">costs at that stiffness. Five orders of magnitude separate the rows, so the same control law is</text>
    <text x="24" y="232">safe at one end and impossible at the other &#8212; and a position controller aimed at structure</text>
    <text x="24" y="248">diverges in force long before the error closes. Read every &#8220;stiff contact&#8221; claim back to a row.</text>
  </g>
</svg>

**Contact couples position and force.** Against an ideal rigid wall, the natural constraint is zero normal velocity. This holds while contact is maintained. The controller may choose a normal force target. Tangential motion remains available, subject to friction. In compliant contact, normal displacement and force are related by the contact mechanics. So independent, arbitrary position and force targets along the same constrained direction can conflict. Hybrid control (§3) selects complementary motion and force objectives: some directions track position, the others track force. Impedance control (§2) instead chooses their relation, like a virtual spring between them.

The stiffness plot is a simplified local linear comparison. It does not predict that an actuator can generate unlimited force. Real torque limits, structural compliance and contact nonlinearity bound or change the response. A low-gain position-based controller can also render compliance. The danger is demanding an unreachable position with excessive stiffness or integral action.

### 2. Impedance and admittance — the same idea, opposite causality

Both describe a desired relation between motion and interaction force. Fix a reference $x_d$. Define the displacement $e=x-x_d$, and let $F_{ext}$ be the force **on the robot**. A one-axis target is

$$M_d\ddot e+D_d\dot e+K_de=F_{ext}.$$

Here $M_d$, $D_d$, and $K_d$ are desired inertia, damping, and stiffness. This equation is a desired closed-loop behavior. It is not automatically the torque command of a real arm. Read it as a virtual mechanical system. An external push first accelerates the mass. Damping resists the motion. The spring pulls it back toward the reference. At static equilibrium the velocity and acceleration vanish, leaving $K_de=F_{ext}$. Low stiffness permits a larger displacement under the same force. The hardware decides which of the two causalities you can build. The deciding factors are transmission friction, reflected inertia, and whether force is sensed or commanded. [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 Haptic Device Design & Kinematics]] traces that chain from Cartesian force to motor current.

**Impedance, defined term by term.** An **impedance** is a dynamic map from motion to force, and **impedance control** is any controller whose closed loop is designed to make the robot's response to an external force obey a chosen impedance. The target has three named terms, each a force:

- **Inertia term** $M_d\ddot e$: resists acceleration, with $M_d$ (kg) the apparent mass the environment should feel.
- **Damping term** $D_d\dot e$: resists velocity, with $D_d$ (N·s/m) dissipating energy.
- **Stiffness term** $K_de$: pulls back toward the reference, with $K_d$ (N/m) the virtual spring.

In the Laplace domain, with velocity $V(s)=sE(s)$, the same target is a transfer function from velocity to force, and an **admittance** is its inverse, from force to motion:

$$Z(s)=\frac{F_{ext}(s)}{V(s)}=M_ds+D_d+\frac{K_d}{s},\qquad Y(s)=\frac{1}{Z(s)}$$

so an impedance controller measures motion and outputs force, and an admittance controller measures force and outputs motion, which is the causality the section title refers to. Reading the target as a mass-spring-damper gives its natural frequency $\omega_n=\sqrt{K_d/M_d}$ and damping ratio $\zeta=D_d/(2\sqrt{K_dM_d})$, since those are the standard second-order parameters ([[04-robotics/control-theory-ce397|Control Theory §5]]). The admittance side has a second, time-domain target of its own — the virtual dynamics the controller integrates to produce the motion reference $x_c$ it hands to the inner loop — written out term by term in [[04-robotics/contact-force-tactile|9. Contact, Force & Tactile Interaction §5]].

> [!example] Worked example · 계산 예제
> $M_d=2$ kg, $K_d=500$ N/m. A steady 10 N push settles at $e=F_{ext}/K_d=10/500=0.02$ m. The natural frequency is $\sqrt{500/2}=15.8$ rad/s, and critical damping ($\zeta=1$) needs $D_d=2\sqrt{500\times2}=63.2$ N·s/m.
> **Those numbers are plant P2 in $y$.** Catalog pose $\theta=(0^\circ,90^\circ)$ has $\Lambda=\mathrm{diag}(1,2)$ ([[02-foundations/lab-plants|0.6]] and [[02-foundations/manipulator-kinematics-dynamics|10]]), so $\Lambda_y=2\,\mathrm{kg}$ is the apparent mass at the tip in $y$, not the $2\,\mathrm{kg}$ of metal. Command $F=(0,-10)$ on the panel: $\tau=J^\top F=(-10,0)\,\mathrm{N{\cdot}m}$. The panel pushes the robot in $+y$, so $F_{ext}=+10\,\mathrm{N}$ and the $0.02\,\mathrm{m}$ deflection is in $+y$. Unconstrained, $a_y=-10/2=-5\,\mathrm{m/s}^2$. Against steel the *position* is set by the wall: impedance still commands the $10\,\mathrm{N}$; admittance commands motion and a delayed force error becomes a shove into the wall. The problem set is this example as two block diagrams.
> **Non-examples**: a controller that holds $F=F_d$ regardless of motion specifies no relation between motion and force, so it is force control, not an impedance. And "soft" is not part of the definition: $K_d=10^5$ N/m is a perfectly valid, very stiff impedance.

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

The diagram shows **two common implementations**, not hardware requirements for every controller carrying these names:

- **Torque-based impedance** computes restoring forces from motion error and maps them to joint torques. A responsive torque interface helps render the desired behavior. Low mechanical friction and backdrivability also help; a backdrivable joint can be turned by an external push without the motor and gearbox resisting it. They are not the definition of impedance. Stiffness is selected for the task; it is not “soft by default.” How far a geared joint is from backdrivable, with each motor-side impedance reaching the joint multiplied by $n^2$, is [[04-robotics/actuators-drives|10.5 Actuators & Drives §7]].
- **Admittance** takes measured or estimated external force and integrates a virtual dynamic model to generate a motion reference. An inner motion controller tracks that reference. This is useful on robots exposing position or velocity commands. Its achievable behavior depends on the inner loop as well as the outer force feedback.

| Architecture | Useful starting point | What must be checked |
|---|---|---|
| Torque-based impedance | Shape the arm's response to displacement | Torque bandwidth, dynamics compensation, gains, saturation |
| Admittance with an inner motion loop | Turn force feedback into a motion reference | Sensor/estimator delay, inner-loop tracking, virtual dynamics, contact stiffness |

A stiff wall makes small motions produce large force changes. In an admittance loop, delayed force feedback can therefore generate an excessive corrective motion and oscillation. It **can** be stabilized with suitable dynamics, bandwidth and hardware. Stiffness alone does not prove failure. Conversely, impedance can track motion in free space. The practical question is which desired behavior the complete robot can render in the operating conditions.

> [!warning] Architecture and stiffness · 구조와 강성
> A wrist force sensor does not identify the control architecture: inspect where its signal enters and what the controller commands. Also, two passive linear springs **in series** satisfy $1/K_{eq}=1/K_1+1/K_2$; their stiffnesses do not add. That follows because the same force $F$ passes through both springs and their deflections add, $F/K_{eq}=F/K_1+F/K_2$. For $K_1=10^5$ and $K_2=10^7$ N/m, $K_{eq}=9.90\times10^4$ N/m, so the softer spring sets the series stiffness (§5 uses exactly this). Feedback stability requires a dynamic model, not just this static equivalent. Connect the control diagram to [[02-foundations/manipulator-kinematics-dynamics|10. §8]].

> [!question] Check the model · 모델 확인
> If the robot settles under a steady external force, which terms remain? **Answer:** only the spring term in this fixed-reference model. If the measured response oscillates, inspect inertia, damping, feedback delay and tracking; the static spring equation alone cannot explain it.

For a derivation from a point-mass robot to torque commands, see [MIT's manipulator-control notes](https://manipulation.mit.edu/force.html). Distinguish the desired interaction equation from the implementation that attempts to realize it.

### 3. Hybrid position/force control

Mason's constraint analysis says which directions belong to the environment. Raibert and
Craig's 1981 architecture is how you act on that: choose a task frame, and a diagonal
**selection matrix** $S$ of ones and zeros that assigns each direction to one controller.

$$\tau = J^\top\left[\,S\,\mathcal{F}_{\text{pos}} + (I - S)\,\mathcal{F}_{\text{force}}\right]$$

This means that $S$ keeps the task-wrench components assigned to position control, $I-S$ keeps the
complementary force-controlled components, and $J^\top$ maps their combined task wrench to
joint torque. The symbols describe the ideal task-space split; an implementation still has
to handle dynamics, saturation, and model error.

Position control runs in the $S$ directions and force control in the complementary ones. In
the ideal model those projected objectives do not address the same axis. For sliding a tool along a
surface: position control in the two tangential directions, force control along the normal.

**Natural and artificial constraints, and the selection matrix, defined.** Mason's analysis works in a **task frame**, a coordinate frame at the contact with axes along the surface normal and tangents, and splits each of its six directions (three translations, three rotations) twice:

- **Natural constraints** are what the contact imposes whatever the controller does. Along a direction the surface blocks, velocity is zero; along a direction it leaves free, an ideal frictionless contact transmits no force.
- **Artificial constraints** are the targets the controller adds in the complementary slots: a desired force where motion is blocked, a desired position or velocity where motion is free.

Each direction gets exactly one natural and one artificial constraint, so no axis carries both a position target and a force target. The **selection matrix** records the split, with one entry per task-frame direction:

$$S=\mathrm{diag}(s_1,\dots,s_6),\qquad s_j=\begin{cases}1 & \text{direction } j \text{ is free, so position-controlled}\\ 0 & \text{direction } j \text{ is blocked, so force-controlled}\end{cases}$$

and in the control law $\mathcal{F}_{\text{pos}}$ is the wrench a position controller outputs (for example PD on pose error) and $\mathcal{F}_{\text{force}}$ the wrench a force controller outputs (for example PI on force error), both in the task frame.

> [!example] Worked example · 계산 예제
> Wiping a table, translations only, $z$ along the normal. Natural: $v_z=0$, $f_x=f_y=0$. Artificial: a desired tangential velocity along $x$ and $y$, and a desired pressing force along $z$. So $S=\mathrm{diag}(1,1,0)$. If the position loop asks for $\mathcal{F}_{\text{pos}}=(3,-1,7)$ N and the force loop for $\mathcal{F}_{\text{force}}=(0.5,0.2,-10)$ N, the command is $S\mathcal{F}_{\text{pos}}+(I-S)\mathcal{F}_{\text{force}}=(3,-1,-10)$ N: the position loop's 7 N along the normal is discarded.
> **Non-example**: $S$ is diagonal only in the task frame. If the table is actually tilted $10°$ about $x$, the correct matrix in world axes is $RSR^\top$, whose $y$–$z$ block is $\begin{pmatrix}0.970&0.171\\0.171&0.030\end{pmatrix}$. Using $\mathrm{diag}(1,1,0)$ in world axes instead lets the force loop act partly along the surface, which is the orientation-error failure described next.

This is the architecture that made constrained-manipulation tasks *specifiable*, and its
limitation is the same as its premise — it assumes you know the task frame and the contact
geometry. When the task frame is accurate and the model is adequate, the split is clean and
comparatively easy to tune. A 3 mm **translation** error makes contact occur early, late, or at the wrong point; it
does not by itself rotate the surface normal. An orientation or local-shape error rotates the
true normal, so the nominal selection matrix mixes tangential motion and normal force. Both
errors are common ways construction geometry breaks a factory controller, but their mechanisms differ.

### 4. Operational-space control

Khatib's 1987 formulation is what makes the previous two sections implementable on a real
arm rather than on a point mass. Control is written directly in task coordinates using the
operational-space inertia from [[02-foundations/manipulator-kinematics-dynamics|10. §6]]:

$$\mathcal{F} = \Lambda(\theta)\,\ddot x_d + \mu(\theta,\dot\theta) + p(\theta), \qquad \tau = J^\top\mathcal{F}$$

with $\Lambda=(JM^{-1}J^\top)^{-1}$ the operational-space inertia (the mass the tip appears to have, $M$ being the joint-space mass matrix), $\ddot x_d$ the commanded tip acceleration, and $\mu$ and $p$ the task-space Coriolis and gravity terms. Read it as the arm's equation of motion rewritten in tip coordinates and then solved for the force that would produce the desired tip acceleration; $J^\top$ maps that force back to joint torques. Two consequences that matter:

- The arm's configuration-dependent inertia is **compensated**, so a commanded task-space
  behaviour is the same in every pose. Without this, the factor-of-five inertia change from
  [[02-foundations/manipulator-kinematics-dynamics|10. §3]] shows up directly as a
  pose-dependent change in the contact behaviour you thought you had specified.
- Redundancy resolution becomes a **null-space projection** (the null space of $J$ is the set of joint motions $\{\dot\theta: J\dot\theta=0\}$ that leave the tip still, [[02-foundations/linear-algebra|1. Linear Algebra §2]]): a redundant arm can satisfy a
  secondary objective — stay away from joint limits, keep the elbow clear of a worker —
  using motion that produces no task-space force. For a mobile manipulator on a site with
  people in it, this is the mechanism, not a nicety.

**The projector, written out.** "Null-space" is used loosely across the literature, so it is
worth seeing the object. In plain terms, the projector is a filter on the secondary torque: it
lets $\tau_0$ move the arm only in ways the task does not feel. The thing to watch is *when* the
task does not feel it — only at rest (static), or also while the arm is moving (transient).
Different projectors differ exactly there, and the two answers have names. **Statically consistent** means no leftover task force once the arm has stopped moving. **Dynamically consistent** means the task also feels nothing while the arm is still moving. With $\bar J = M^{-1}J^\top\Lambda$ the dynamically-consistent
inverse of the Jacobian, the secondary torque is filtered through

$$\tau = J^\top\mathcal{F} \;+\; \underbrace{\left(I - J^\top\bar J^{\,\top}\right)}_{\text{null-space projector } N^\top}\tau_0$$

where $\tau_0$ is whatever the secondary objective asks for. The projector's job is that
**$\tau_0$ cannot disturb the task**. Be precise about *which* disturbance, because this is
commonly stated backwards: a projector built from the plain Moore–Penrose pseudo-inverse ([[02-foundations/linear-algebra|1. Linear Algebra §4.5]]) is
already **statically consistent** — in steady state the secondary torque produces no task
force at all. What it does not do is prevent the task from *accelerating* during the
transient, because $JM^{-1}N^\top\tau_0 \neq 0$ for the Moore–Penrose $N^\top$ when $M \neq I$. **Dynamic consistency buys
the transient, not the static force**. Among projectors of this form, only the inertia-weighted
inverse $\bar J$ makes $JM^{-1}N^\top = 0$ (Khatib 1987, restated in Dietrich, Ott &
Albu-Schäffer, *IJRR* 2015, §3.3.1). That survey defines static consistency as no interfering
force in any static equilibrium and shows every weighting matrix has it (§3.2); dynamic consistency
adds no interfering acceleration at any time (§3.3). It also gives a differently structured
projector, $M(I - J^{+}J)M^{-1}$, that is dynamically consistent too but not load-independent
(§3.3.2).

**What makes it a projector, and a three-joint check.** A **projector** is a matrix $P$ with $P^2=P$, so applying it twice changes nothing more; $N^\top$ qualifies because $J\bar J=JM^{-1}J^\top\Lambda=I$ gives $(J^\top\bar J^{\,\top})^2=J^\top\bar J^{\,\top}$. The two consistency properties are two conditions on it:

- **Static consistency**: at rest, the filtered torque produces no task force, so its least-squares task force $J^{+\top}N^\top\tau_0$ is zero.
- **Dynamic consistency**: at every instant, the filtered torque produces no task acceleration, which is the condition below.
$$J\,M^{-1}N^\top=0$$

> [!example] Worked example · 계산 예제
> Three joints, one task direction: $M=\mathrm{diag}(2,1,1)$, $J=(1,1,1)$, secondary torque $\tau_0=(1,0,0)$. Then $\Lambda=(JM^{-1}J^\top)^{-1}=1/2.5=0.4$ and $\bar J=M^{-1}J^\top\Lambda=(0.2,0.4,0.4)$, so $N^\top\tau_0=(0.8,-0.2,-0.2)$ and the task acceleration $JM^{-1}N^\top\tau_0=0.4-0.2-0.2=0$. With the Moore–Penrose inverse $J^+=(1/3,1/3,1/3)$ instead, $N^\top\tau_0=(2/3,-1/3,-1/3)$: its task force $J^{+\top}N^\top\tau_0=0$ (statically consistent), but $JM^{-1}N^\top\tau_0=1/3-1/3-1/3=-1/3\neq0$, so the task accelerates during the transient. That is the non-example the paragraph above warns about.

**Task priority, and whole-body control.** Stack more than two objectives and this becomes a
hierarchy: each level is projected into the null space of all levels above it, so a lower
priority can never fight a higher one. That is the classical form. The modern form solves the
same problem as a **quadratic program** (QP: minimize a quadratic cost under linear equality and inequality constraints; defined with its standard form in [[02-foundations/optimization|4. Optimization §5]]) at every control step —

- minimize the weighted task errors,
- subject to joint-position, velocity and torque limits, friction cones at the contacts, and
  balance or base-stability constraints.

**The whole-body QP, written out.** With $q$ the generalized coordinates (floating base plus joints), the decision variables are the accelerations $\ddot q$, joint torques $\tau$ and contact forces $f$:

$$\min_{\ddot q,\,\tau,\,f}\ \sum_i w_i\,\lVert J_i\ddot q+\dot J_i\dot q-\ddot x_i^{\text{des}}\rVert^2\quad\text{s.t.}\quad M\ddot q+h=S_a^\top\tau+J_c^\top f,\ \ f\in FC,\ \ \tau_{\min}\le\tau\le\tau_{\max}$$

Here each task $i$ has Jacobian $J_i$, desired acceleration $\ddot x_i^{\text{des}}$ (typically a PD law on that task's error) and weight $w_i$; $M$ is the mass matrix and $h$ collects Coriolis and gravity terms; $S_a$ selects the actuated joints, since a floating base has no motor; $J_c$ is the contact Jacobian; and $FC$ the friction cones of [[04-robotics/contact-force-tactile|Contact, Force & Tactile §2]]. At the current state $q,\dot q$ the dynamics are linear in $(\ddot q,\tau,f)$ and the cost is quadratic, so once the cones are replaced by the polyhedral cones of [[04-robotics/contact-force-tactile|Contact, Force & Tactile §2]] the problem is a convex QP that re-solves every control step. Which polyhedral cone matters to the answer, not only to the solve time: the outer box pyramid lets the QP authorise contact forces that slip, the inner generator cone makes it refuse forces the contact would have carried, and that section gives both the formula and the size of each error.

**This QP is what "whole-body control" names.** The reason the field moved to it is not
elegance: strict null-space priority cannot express *inequality* constraints, and joint
limits, torque saturation and contact friction are all inequalities. A humanoid or a mobile
manipulator that must respect all of them simultaneously is solving a QP, and the priority
hierarchy survives inside it as constraint weights or as a cascade of QPs.

For the mobile-manipulation case — where the "arm" includes a driveable base — the same QP
absorbs base and arm degrees of freedom into one problem, which is the formal version of the
base-placement choice in [[04-robotics/navigation-mobile-manipulation|16. §3]].

### 5. Contact transitions — where the theory earns its keep

Steady contact is the easy part. The hard part is the microsecond the robot arrives, and
the argument here is quantitative rather than rhetorical.

Assume an undamped one-axis linear impact, constant apparent mass, a linear spring, and fully stored-and-returned energy. The end-effector's apparent mass $\Lambda$ meets stiffness $K$ at approach speed $v$, giving a half-sine contact with

$$F_{\max} = v\sqrt{\Lambda K}, \qquad t_{\text{contact}} = \pi\sqrt{\Lambda/K}$$

Both follow from the model in one step each, and they are worth deriving because the
*shape* of the answer is the lesson. All the kinetic energy goes into the spring at maximum
compression, $\tfrac12 \Lambda v^2 = \tfrac12 K \Delta x^2$, so
$\Delta x = v\sqrt{\Lambda/K}$ and the peak force is
$F_{\max} = K\Delta x = v\sqrt{\Lambda K}$. The duration is half a period of that same
mass–spring oscillator: $\omega = \sqrt{K/\Lambda}$, so $T/2 = \pi\sqrt{\Lambda/K}$.

Read the two square roots against each other. Peak force scales as $\sqrt{K}$ and duration
as $1/\sqrt{K}$, so **making the interface a hundred times stiffer multiplies the force by
ten and divides the contact time by ten** — in this model the impulse is conserved and only its shape
changes. Mechanical compliance moves both numbers directly; pre-impact control can most directly reduce $v$. For measured impacts, check the force-time trace and identified equivalent $\Lambda,K,D$.

Take the $\Lambda = 2$ kg from [[02-foundations/manipulator-kinematics-dynamics|10. §6]] and
a gentle approach at $v = 5$ cm/s. That $\Lambda$ is the bare arm's: geared drives add their rotors' reflected inertia, and with the frozen drive of [[04-robotics/actuators-drives|10.5 Actuators & Drives §4]] at a gear ratio of 100 the same $10^5\,\mathrm{N/m}$ touchdown peaks at $29.5\,\mathrm{N}$ instead of $22.4$.

| Interface | $K$ (N/m) | $F_{\max}$ | contact duration | 1 kHz samples inside the contact |
|---|---:|---:|---:|---:|
| bare tool on a real arm — the series stiffness §1 says a controller identifies | $10^5$ | **22 N** | **14 ms** | about 14 |
| compliant wrist in series | $10^4$ | **7.1 N** | **44 ms** | about 44 |
| local material contact alone, arm structure removed — §1's fourth row | $10^7$ | **224 N** | **1.4 ms** | about 1 |

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="the idealised material-only contact drawn to scale as a needle-thin spike about one control sample wide, against the compliant contact as a broad flat bump">
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
    <text x="20" y="218">Both axes are to scale. The idealised material-only contact (the table's last row) is the needle</text>
    <text x="20" y="234">at the left: 1.4 ms wide, so a 1 kHz loop gets about one sample inside it. The compliant contact is</text>
    <text x="20" y="250">the broad bump: barely visible on that force axis, long enough for about 44 samples.</text>
  </g>
</svg>

Read the table rather than the picture, and read the last row against §1. The arm's own
structure sits in series with the material and the softer element wins: $10^5$ against $10^7$
gives $9.9\times10^4$. So a bare tool on a real arm gets about **fourteen** samples inside the
contact, not one — regulable, but barely, at three times the compliant wrist's peak force.
The bottom row is the idealisation you would approach only with a bare indenter on a rigid
fixture; there a 1 kHz controller sees roughly **one sample**, arriving as late as 1 ms in,
possibly after the peak has passed, and no control law fixes that because the information
arrives after the event. The figure draws the idealised row and the compliant wrist, not the bare-tool row.

Put a compliant element in series and both numbers move, in opposite directions and by the
same factor: $F_{\max} \propto \sqrt{K}$ and $t_{\text{contact}} \propto 1/\sqrt{K}$, so
softening from the structural $10^5$ to $10^4$ buys $\sqrt{10} \approx 3.2\times$ in each, and against the bottom row's idealisation $\sqrt{1000} \approx 32\times$. The force becomes
something the arm can survive *and* the event becomes long enough to regulate. The same approach run end to end on P2, switching to impedance before contact, pressing a compliantly mounted panel and sweeping $K_d$ against the approach speed, is [[04-robotics/capstone-panel-contact|26. Capstone]].

The lesson generalises past the arithmetic: **passive compliance is not a cheap substitute
for active control; it is the only thing that acts at contact bandwidth.** Whitney's 1982
quasi-static analysis of compliantly supported insertion is the mature version of this
idea — it derives, for chamfered and chamferless peg-in-hole, the conditions under which
misalignment causes wedging or jamming, and turns them into
design inequalities the support compliance must satisfy.

**Wedging and jamming, which are not the same failure.** Both end with the peg stopped part
of the way in, and they take opposite fixes, so a paper that reports "the insertion failed"
without saying which has reported nothing actionable.

- **Wedging** is a *geometric* lock. The peg touches both walls of the hole at two points whose
  normals oppose each other, and the two contact forces can then balance each other for any
  axial push. Its defining conditions are two-point contact with opposing normals, reached
  while the peg is still tilted — so it is entered by inserting at too large an angle too
  early, and once it holds, **pushing harder does not help**, because extra push raises both
  contact forces together. The fix is geometric: a chamfer, a smaller initial angle, or
  compliance that straightens the peg before the second contact forms.
- **Jamming** is a *wrench* condition. Contact is perfectly ordinary, but the applied
  combination of force and moment falls outside the cone of wrenches that produce insertion,
  so friction at the contacts absorbs all of it and the peg stops. Its defining condition is
  therefore a statement about the applied wrench and the friction cones ([[04-robotics/contact-force-tactile|Contact, Force & Tactile §2]]), not
  about geometry, and the fix is to change the applied wrench: less lateral force, less
  moment, more axial push. Non-example: a peg that stops because the hole is undersized is
  neither — that is interference, and no wrench inside any cone gets it in.

The practical difference is that **jamming is fixed by whatever supplies the right wrench, and
a compliance placed at the right point supplies it automatically.**

**Remote-centre compliance, defined.** An **RCC** is a *passive mechanical element* placed
between wrist and tool, whose **compliance centre** — the single point at which an applied
force produces translation with no rotation, and an applied moment produces rotation with no
translation — is located at the *tip of the part*. That one placement condition is the whole
device. It decouples the two errors: a lateral misalignment then produces lateral motion, and
an angular misalignment produces rotation about the tip, instead of each error generating the
other and driving the peg toward the wedging geometry above. It has no sensor and no loop, so
it acts at the speed of the material. **Non-example**: a soft spring in the wrist is compliant
but its compliance centre is at the *wrist*, where a lateral force also rotates the peg — that
is compliance without an RCC, and it makes the coupling worse, not better.
It solves the insertion problem in aluminium, with no sensor and no latency.

All of this assumes you know a transition happened. Detecting it is a separate estimation
problem, defined with its mode set and its failure cases in [[04-robotics/contact-force-tactile|Contact, Force & Tactile §7]]; the
argument here starts one sample after that estimate has fired.

Colgate and Hogan's 1988 result is the theoretical boundary of the active alternative: for
linear time-invariant systems, a manipulator is stable when coupled to *every* passive
environment if and only if its driving-point impedance is passive. Here a passive system can store and return energy but never generate it, and the driving-point impedance is the force-versus-velocity relation the environment sees when it pushes on the robot at the contact point. That converts
contact stability from a per-experiment tuning question into a frequency-domain test, and
it says something uncomfortable — with non-collocated or unmodelled dynamics there is a **limit** to how far a controller can reduce the apparent inertia. The ceiling on renderable stiffness is a separate limit, set by sampling, delay and quantization ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]). The controller cannot pretend the
arm's mass away.

**Passivity and the driving-point impedance, as formulas.** Treat the contact point as a **port**: the environment applies force $F(t)$ to the robot there, and the robot moves with velocity $v(t)$ at the same point, so $F\,v$ is the power flowing into the robot. The system is **passive** when it can never return more energy through the port than it held at the start; with $E_0\ge0$ its initially stored energy,

$$\int_0^t F(\tau)\,v(\tau)\,d\tau\ \ge\ -E_0\quad\text{for every } t \text{ and every input}$$

so the net energy that has flowed in never drops below minus what was stored (the storage-function form is in [[04-robotics/control-theory-ce397|Control Theory §4]]). The **driving-point impedance** is the transfer function from velocity to force at that one point, $Z(s)=F(s)/V(s)$, "driving point" meaning force and velocity are measured at the same place. For a linear time-invariant system, passivity is equivalent to $Z(s)$ being **positive real**, which has two conditions: $Z$ has no poles in the open right half-plane (any on the imaginary axis are simple, with positive residue), and

$$\mathrm{Re}\,Z(j\omega)\ge0\quad\text{for all }\omega$$

because a sinusoidal velocity of amplitude $V_0$ at frequency $\omega$ makes the port absorb average power $\tfrac12V_0^2\,\mathrm{Re}\,Z(j\omega)$. Colgate and Hogan's theorem then reads: the robot is stable against every passive environment if and only if its $Z$ is positive real.

> [!example] Worked example · 계산 예제
> The ideal §2 target $Z(s)=M_ds+D_d+K_d/s$ has $M_dj\omega$ and $K_d/(j\omega)$ purely imaginary, so $\mathrm{Re}\,Z(j\omega)=D_d$ at every frequency: it is passive exactly when $D_d\ge0$ ($M_d=2$, $D_d=20$, $K_d=500$ gives $20$ N·s/m at every $\omega$).
> **Non-example**: the same spring rendered with a 1 ms delay, $Z(s)=K_de^{-sT}/s$, has $\mathrm{Re}\,Z(j\omega)=-K_d\sin(\omega T)/\omega$. With $K_d=1000$ N/m, $T=0.001$ s and $\omega=100$ rad/s that is $-0.998$ N·s/m: the delayed spring pumps energy into the contact, and only enough physical damping can pay it back ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]).

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
  contact-rich tasks. The finding that matters: with the learning setup held fixed, the action space changed
  sample efficiency, energy use, safety and transfer, not just final score.
- **Bogdanovic, Khadiv & Righetti, RA-L 2020** — *Learning Variable Impedance Control for
  Contact Sensitive Tasks*. Same question in **joint space**: the policy outputs desired
  position *and* impedance gains. Its contribution is the robustness axis — it varies contact
  uncertainty deliberately and shows where torque control and position control each fail,
  while a learned variable-impedance action space degrades gracefully.

Read them against §2: choosing an action space helps determine where on the
impedance–admittance causality spectrum the learned layer sits. A policy that emits positions
inherits whatever compliance, gains and force feedback its lower-level controller and
hardware provide; position commands alone do not identify a stiff interface. A torque policy
has more direct authority but must either learn or be wrapped by stabilising inner-loop
behaviour. A policy that emits impedance parameters asks a classical controller to render a
specified relation at high rate. These are architectural choices, not three universal points
on a single soft-to-stiff scale.

> [!tip] Why this matters for a demonstration-collection thesis
> If the contribution is force-bearing demonstration data, the action space question arrives
> twice: once for what the *teleoperator* commands during collection, and once for what the
> *policy* emits at deployment. They do not have to match, and the mismatch is a design
> decision that most papers leave implicit.

#### The convergence, and the interface it is settling on

Several recent systems point in the same direction, although it is not yet a settled or
one-way convergence: **a VLA can act as a slower semantic layer that parameterises a
classical high-rate inner loop.** This is one increasingly visible way to combine learned
task reasoning with established contact-control machinery.

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
position-controlled and largely force-blind. The cited systems show that some groups
deploying VLAs on contact-rich tasks have found impedance, admittance, or passivity layers
useful; they do not establish that every system needs the same interface.

> [!note] The prediction worth recording
> If the merge completes, **the interface will be compliance parameters, not positions.**
> That is the thing to watch, and it is the reason this page sits at Mastery in a research
> programme whose contribution is contact-rich manipulation.

### 7. Reading force control in a paper

| Question | What a wrong answer hides |
|---|---|
| Impedance or admittance? What is the inner loop? | Identify the rendered compliance and its tested stiffness/bandwidth range |
| Was it tested against a **stiff** environment? | Foam and free space hide the instability entirely |
| Are $M_d, D_d, K_d$ reported, with units? | "Compliant" without numbers is not a specification |
| Contact **transition** shown, or only steady contact? | The transition is where §5 says the difficulty lives |
| Control rate, sensor rate, contact duration and **bandwidth** (the frequency range over which the closed loop still follows its reference, [[04-robotics/control-theory-ce397\|5. Control Theory §5.5]])? | Millisecond impact peaks may be dominated by mechanics before feedback reacts; sustained contact can still be regulated at much lower rates. Compare rates with the phenomenon being claimed — the worked case does it in one ratio. |
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
- [ ] Give stiffness, compliance and damping with their units, and say which of the three adds in series.
- [ ] Explain how impedance and admittance generate commands, and what limits their behavior in stiff contact.
- [ ] Write the selection-matrix form of hybrid control and give a task for it.
- [ ] Compute $F_{\max}$ and contact duration for a given $\Lambda$, $K$, $v$, and say how many control samples land inside.
- [ ] Compare the contact duration with one period of the target impedance, and say what the ratio implies about who owns the impact.
- [ ] Distinguish wedging from jamming, and say what an RCC's compliance centre has to be placed on.
- [ ] Explain what Colgate and Hogan's passivity condition forbids.

> [!tip] Going deeper · 더 깊이
> Siciliano, Sciavicco, Villani & Oriolo, *Robotics: Modelling, Planning and Control* (Springer, 2009) ch.9 is the standard textbook treatment of §2–§4 — impedance, admittance, hybrid force/position and operational-space control, derived rather than described. Tedrake's free [*Robotic Manipulation*](https://manipulation.csail.mit.edu/) covers the same control ideas as they are actually deployed on modern hardware, which is closer to how the papers here are written. Neither covers §6: where a learned policy sits relative to these controllers is a current question, not settled material.

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
6. Two elements in series, $10^5$ and $10^7$ N/m. Which of stiffness or compliance do you add,
   what is the result, and what fraction of the total yielding belongs to the softer element?
7. An insertion stops part-way in. Pushing harder changes nothing. Wedging or jamming, and
   what does your answer rule out as a fix?

> [!tip]- Answers
> 1. The hardware and symptom alone do not determine the architecture. If force feedback generates position references, it is an admittance implementation. Higher contact stiffness can amplify the effect of delay and insufficient damping; check the actual loops, gains and timing before assigning the cause. Stable behavior on foam does not establish stable behavior on steel.
> 2. $F_{\max} = v\sqrt{\Lambda K}$ is linear in $v$, so the peak force doubles in every row: 22 → 45 N for the bare tool on a real arm, 224 → 447 N for the idealised material contact. The duration $\pi\sqrt{\Lambda/K}$ does not contain $v$ at all, so it stays at 14 ms and 1.4 ms respectively. Approaching faster buys you nothing in reaction time and costs you proportionally in force — which is why approach-speed limits, not better control, are the usual fix.
> 3. Because it places the compliance centre at the tip of the peg, so a lateral misalignment produces lateral compliance and an angular misalignment produces rotation about the tip, instead of each error generating the other. The correction is mechanical, so it happens at the speed of the material rather than the speed of a control loop — and §5 shows the control loop is too slow to have helped anyway.
> 4. At minimum, that the policy chose useful position references. The system may still realise compliance through a lower-level impedance/admittance or force loop and passive hardware, so inspect that stack. A 10 Hz outer policy cannot react to the millisecond impact peak itself, but it can adapt references for slower sustained contact. The strongest supported claim depends on which layer produced the measured force behaviour.
> 5. Because the architecture assigns force control to a direction it believes is normal to the surface, and that belief comes from a model. On a construction site the part is where it was placed, not where the drawing says: a few millimetres of position error makes contact early, late or at the wrong point, and a couple of degrees of orientation or surface-shape error rotates the true normal, so force control now acts partly along the surface and position control partly into it, which is exactly the fighting the architecture was designed to avoid. It is the difference between a fixtured factory cell and [[05-construction-robotics/assembly-fabrication|construction assembly]].
> 6. Compliance adds: $C_{eq}=10^{-5}+10^{-7}=1.010\times10^{-5}$ m/N, so $K_{eq}=9.90\times10^{4}$ N/m. The softer element supplies $99.0\%$ of the yielding, which is why the series number sits essentially on top of $10^5$ and why a controller identifies the structure rather than the material.
> 7. Wedging. It is the geometric lock, two-point contact with opposing normals, and its signature is exactly that extra axial push raises both contact forces together and changes nothing. That rules out "push harder" and rules out re-aiming the applied wrench, which is the *jamming* fix; what is left is geometry — chamfer, smaller entry angle, or compliance that straightens the peg before the second contact forms.

### Problem set · 과제

Tier B. Using only this page, its prerequisites and the object catalog. The running object with **three entries changed**: the press goes sideways into a standing panel, $F=(-8,0)\,\mathrm{N}$, so the axis is now $x$ and the apparent mass, which $M_d$ is again set equal to, is $\Lambda_x=1\,\mathrm{kg}$; the target stiffness is $K_d=2000\,\mathrm{N/m}$ at $\zeta=0.7$; and the approach speed doubles to $v=0.10\,\mathrm{m/s}$. P2 stays at $\theta=(0^\circ,90^\circ)$ and $K_e$ stays at $10^5\,\mathrm{N/m}$ ([[02-foundations/lab-plants|0.6]]). The Euler loop lives on [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] — do not start a second simulator.

1. **Draw.** All three panels of the homework diagram on the new axis: the arm with the panel now standing at $x=1\,\mathrm{m}$ (the same panel as [[04-robotics/contact-force-tactile|9. Contact, Force & Tactile Interaction]]'s running object), the two block diagrams rewritten for $x$, and the clock with the new impact width against the new target period, both to the same scale.
2. **Derive.** (a) $\tau=J^\top F$ for $F=(-8,0)$, and say what is different from the vertical case and why. (b) The static deflection under the $8\,\mathrm{N}$ reaction. (c) $\omega_n$, the critically damped $D_d$, and the $D_d$ at $\zeta=0.7$. (d) $F_{\max}$ and $t_{\text{contact}}$ against $K_e=10^5\,\mathrm{N/m}$ at $v=0.10\,\mathrm{m/s}$, with the number of 1 kHz samples inside. (e) The ratio of one target period to the contact duration.
3. **Interpret.** The peak force rose from the worked case's $22.4$ to $31.6\,\mathrm{N}$ while the apparent mass *halved*. Account for the factor exactly. Then: the period-to-contact ratio fell from $28.3$ to $14.1$ — did stiffening the target actually buy any authority over the impact, and what would $K_d$ have to be for the answer to be yes?

> [!tip]- Solutions
> 1. Same arm, same pose; the panel is now the vertical one at $x=1\,\mathrm{m}$, the press arrow points in $-x$, and the springs in series are read along $x$. The clock now shows a $9.93\,\mathrm{ms}$ impact against a $140\,\mathrm{ms}$ period.
> 2. (a) $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$ and $\tau=(8,8)\,\mathrm{N{\cdot}m}$. **Both** joints now carry the load, where the vertical press loaded only the shoulder: at this pose the elbow's own motion moves the tip purely in $x$, so an $x$ force does work on it and a $y$ force does not. (b) $e=8/2000=0.004\,\mathrm{m}$, $4\,\mathrm{mm}$. (c) $\omega_n=\sqrt{2000/1}=44.72\,\mathrm{rad/s}$; $D_d\big|_{\zeta=1}=2\sqrt{2000\cdot1}=89.4\,\mathrm{N{\cdot}s/m}$; $D_d\big|_{\zeta=0.7}=62.6\,\mathrm{N{\cdot}s/m}$. (d) $F_{\max}=0.10\sqrt{1\times10^{5}}=31.6\,\mathrm{N}$ and $t_{\text{contact}}=\pi\sqrt{1/10^{5}}=9.93\,\mathrm{ms}$, so about $10$ samples at 1 kHz — four fewer than the vertical case. (e) $T=2\pi/44.72=0.1405\,\mathrm{s}$, so $T/t_{\text{contact}}=0.1405/0.00993=14.1$.
> 3. The factor is $\sqrt{\Lambda_x/\Lambda_y}\times(v'/v)=\sqrt{1/2}\times2=1.414$, and $22.36\times1.414=31.6\,\mathrm{N}$. Halving the apparent mass bought $\sqrt{1/2}=0.707$ of the peak, and doubling the approach speed spent $2$ — speed is linear in $F_{\max}$ and mass is only square-root, so the speed knob won. That is the general lesson: approach-speed limits, not lighter poses, are what reduce impact force. And no, stiffening the target bought nothing over the impact: the ratio fell from $28.3$ to $14.1$ only because $\omega_n$ rose, and $14.1$ is still an impact that begins and ends inside a fourteenth of one period. Matching them needs $K_d=4K_e=4\times10^{5}\,\mathrm{N/m}$, two hundred times the $2000$ asked for here and far beyond what a 1 kHz loop renders against a stiff surface ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]). The impact still belongs to the mechanics.

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

*H군의 중심이자 Mastery 페이지다. [[04-robotics/contact-force-tactile|9. 접촉]]·[[04-robotics/control-theory-ce397|5]]번과 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 동역학]] 위에 선다.
접촉이 위치 오차를 힘으로 바꾸므로, 제어는 둘 중 하나를 고르는 일이 아니라 둘 사이의 관계를 고르는 일이 된다.*

> [!note] 처음이라면 · First pass
> 먼저 아래의 계속 쓰는 대상과 계산 예제를 읽어라. 이 페이지가 갚아야 할 계산 하나이고, 논증 전체를 결정하는 비 하나로 끝난다. 그다음 §1 — 뻣뻣한 위치 추종이 접촉에서 왜 위험해지는지, 강성 숫자까지 — 그다음 임피던스 대 어드미턴스인 §2, 그다음 §7. §3~§5는 제어기에 관해 읽는 것이 아니라 실제로 고를 때 읽는다.

### 계속 쓰는 대상: P2, 패널, 그리고 목표 임피던스 하나 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**를 고정 자세 $\theta=(0^\circ,90^\circ)$에 두면 말단이 $(1,1)\,\mathrm{m}$에 있고, 거기 달린 공구가 말단 아래 눕힌 패널에 내려앉는다(전완은 그림 평면 밖, 패널 앞으로 지나가므로 패널에 닿는 것은 말단뿐이다). [[04-robotics/contact-force-tactile|9. 접촉·힘·촉각]]의 계속 쓰는 대상과 같은 팔, 같은 공구, 같은 패널을 직각으로 돌려 놓은 것이다. 거기서는 패널이 서 있고 묻는 것이 마찰이라면, 여기서는 패널이 누워 있고 묻는 것은 제어기가 운동과 힘 사이에 두는 *관계*다. §1~§5의 모든 숫자가 이 표에서 나온다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $\theta$ | $(0^\circ,90^\circ)$ | P2의 고정 자세. 말단 $(1,1)$ m, 엘보 $(1,0)$ |
| $J$ | $\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ | 그 자세의 위치 야코비안, 0.6에서 고정 |
| $\Lambda$ | $\mathrm{diag}(1,2)\ \mathrm{kg}$ | 작업공간 관성: $\Lambda_x=1$, $\Lambda_y=2$ kg |
| $F$ | $(0,-10)\ \mathrm{N}$ | 패널에 명령한 누름 |
| $M_d$ | $2\ \mathrm{kg}$ | 목표 관성. $\Lambda_y$와 같게 골랐다 |
| $K_d$ | $500\ \mathrm{N/m}$ | 목표 강성 |
| $D_d$ | $63.2\ \mathrm{N\cdot s/m}$ | 그 $M_d,K_d$에서 임계 감쇠가 되는 목표 감쇠 |
| $K_e$ | $10^5\ \mathrm{N/m}$ | 여기서 힘 제어기가 식별하는 직렬 강성 — §1 표의 셋째 행 |
| $v$ | $0.05\ \mathrm{m/s}$ | 처음 닿는 순간의 접근 속도 |
| $f_s$ | $1\ \mathrm{kHz}$ | 제어 주기 |

$K_e$는 공구·센서·팔 구조·패널을 합친 직렬 강성이지 패널의 재료 강성이 아니다. §1은 통째로 그 차이에 관한 절이고, §5는 어느 행을 고르는가가 무엇을 치르게 하는지 보여 준다.

*범위: 이 페이지는 접촉 하나에서 운동과 힘의 관계를 고르고 크기를 정하는 법을 이름 붙인 팔 하나 위에서 가르친다 — 임피던스, 어드미턴스, 하이브리드 분할, 그 둘의 작업공간 구현, 그리고 그 모두의 아래에서 작동하는 수동 컴플라이언스. 제어기가 상대하는 접촉 역학 자체(complementarity, 마찰 원뿔과 그 선형화, closure: [[04-robotics/contact-force-tactile|9. 접촉·힘·촉각 §1~§4]]), 가상 벽을 얼마나 단단하게 구현할 수 있는지의 샘플링 한계([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]), §6의 정책을 어떻게 학습시키는지([[03-deep-learning/vla/index|VLA]])는 가르치지 않는다.*

### 과제가 그릴 그림: 패널 하나 위의 두 인과와 그 아래의 시계 · Homework diagram

한 번 그려 두면 과제는 같은 그림을 다른 축에서 묻는다.

<svg viewBox="0 0 560 594" style="max-width:100%;height:auto" role="img" aria-label="위: θ = (0, 90도)의 P2가 말단 아래 패널을 누르는 10 N과 크기가 같은 반력, 직렬로 이어진 500 N/m 가상 스프링과 100,000 N/m 실제 스프링; 가운데: 팔과 패널 블록을 공유하는 임피던스와 어드미턴스 블록선도, 토크 인터페이스와 힘 센서에 음영; 아래: 밀리초 축 하나 위의 14 ms 충격 반주기 사인과 목표 거동의 397 ms 한 주기, 1 kHz 샘플 눈금">
  <defs><marker id="fcckA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor">
    <text x="12" y="18" font-size="12" fill-opacity="0.85" font-weight="600">팔과 패널 (x–y 평면, 실제 비율)</text>
    <line x1="34.4" y1="193" x2="65.6" y2="193" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <path d="M 36.2 193 L 31.2 199 M 41.5 193 L 36.5 199 M 46.8 193 L 41.8 199 M 52.1 193 L 47.1 199 M 57.4 193 L 52.4 199 M 62.7 193 L 57.7 199" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
    <path d="M 50 184 L 43 193 L 57 193 Z" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
    <rect x="114.4" y="92" width="57" height="6.4" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1" stroke-opacity="0.75"/>
    <path d="M 116.2 98.4 L 121.2 93.5 M 121.2 98.4 L 126.2 93.5 M 126.2 98.4 L 131.2 93.5 M 131.2 98.4 L 136.2 93.5 M 136.2 98.4 L 141.2 93.5 M 141.2 98.4 L 146.2 93.5 M 146.2 98.4 L 151.2 93.5 M 151.2 98.4 L 156.2 93.5 M 156.2 98.4 L 161.2 93.5 M 161.2 98.4 L 166.2 93.5 M 166.2 98.4 L 171.2 93.5" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
    <line x1="50" y1="184" x2="142" y2="184" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <line x1="142" y1="184" x2="142" y2="92" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
    <circle cx="50" cy="184" r="4.5" fill="currentColor"/>
    <circle cx="142" cy="184" r="4" fill="currentColor"/>
    <circle cx="142" cy="92" r="4.5" fill="currentColor"/>
    <line x1="153" y1="94" x2="153" y2="132" stroke="currentColor" stroke-width="1.8" marker-end="url(#fcckA)"/>
    <line x1="142" y1="86" x2="142" y2="48" stroke="currentColor" stroke-width="1.8" marker-end="url(#fcckA)"/>
    <text x="160" y="120" font-size="11">F = (0, −10) N</text>
    <text x="160" y="134" font-size="11" fill-opacity="0.85">패널이 받는 힘</text>
    <text x="150" y="60" font-size="11">반력 +10 N</text>
    <text x="150" y="74" font-size="11" fill-opacity="0.85">로봇이 받는 힘</text>
    <text x="42" y="214" font-size="11">베이스 (0, 0)</text>
    <text x="146" y="214" font-size="11" text-anchor="middle">엘보 (1, 0)</text>
    <text x="134" y="82" font-size="11" text-anchor="end">말단 (1, 1)</text>
    <text x="96" y="176" font-size="11" text-anchor="middle" fill-opacity="0.85">P2, θ = (0°, 90°)</text>
    <text x="110.4" y="104" font-size="11" text-anchor="end" fill-opacity="0.85">패널 면</text>
    <line x1="314" y1="34" x2="338" y2="34" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 315 34 L 319 29 M 320.5 34 L 324.5 29 M 326 34 L 330 29 M 331.5 34 L 335.5 29 M 337 34 L 341 29" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
    <path d="M 326 34 L 326 38 L 319 40.3 L 333 45 L 319 49.7 L 333 54.3 L 319 59 L 333 63.7 L 319 68.3 L 333 73 L 319 77.7 L 333 82.3 L 319 87 L 333 91.7 L 326 94 L 326 98" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
    <rect x="317" y="98" width="18" height="4" fill="currentColor" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>
    <path d="M 326 102 L 326 102.6 L 319 102.8 L 333 103.1 L 319 103.4 L 333 103.7 L 319 104 L 333 104.3 L 319 104.7 L 333 105 L 319 105.3 L 333 105.6 L 319 105.9 L 333 106.2 L 326 106.4 L 326 107" fill="none" stroke="currentColor" stroke-width="0.9" stroke-linejoin="round"/>
    <line x1="314" y1="107" x2="338" y2="107" stroke="currentColor" stroke-width="1.4"/>
    <path d="M 315 112 L 319 107 M 320.5 112 L 324.5 107 M 326 112 L 330 107 M 331.5 112 L 335.5 107 M 337 112 L 341 107" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
    <text x="344" y="38" font-size="11" fill-opacity="0.8">기준</text>
    <text x="344" y="62" font-size="11" xml:space="preserve">가상 K<tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1"> = 500 N/m</tspan></text>
    <text x="344" y="76" font-size="11" fill-opacity="0.85">20 mm 물러남</text>
    <text x="344" y="108" font-size="11" xml:space="preserve">실제 K<tspan dy="3.1" font-size="11">e</tspan><tspan dy="-3.1"> = 10</tspan><tspan dy="-4.2" font-size="11">5</tspan><tspan dy="4.2"> N/m</tspan></text>
    <text x="344" y="122" font-size="11" fill-opacity="0.85">0.1 mm 물러남</text>
    <text x="314" y="146" font-size="11">직렬, 같은 10 N: 비 200</text>
    <line x1="148" y1="91" x2="312" y2="100" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45" stroke-dasharray="2 3"/>
    <line x1="8" y1="216" x2="552" y2="216" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
    <text x="12" y="234" font-size="12" fill-opacity="0.85" font-weight="600">임피던스 — 운동을 재고 힘을 명령</text>
    <rect x="428" y="258" width="120" height="92" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
    <text x="488" y="290" font-size="12" text-anchor="middle">팔 + 패널</text>
    <text x="488" y="307" font-size="11" text-anchor="middle" xml:space="preserve">Λ<tspan dy="3.1" font-size="11">y</tspan><tspan dy="-3.1"> = 2 kg</tspan></text>
    <text x="488" y="326" font-size="11" text-anchor="middle" xml:space="preserve">K<tspan dy="3.1" font-size="11">e</tspan><tspan dy="-3.1"> = 10</tspan><tspan dy="-4.2" font-size="11">5</tspan><tspan dy="4.2"> N/m</tspan></text>
    <rect x="12" y="258" width="88" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="56" y="273" font-size="11" text-anchor="middle">말단에서</text>
    <text x="56" y="287" font-size="11" text-anchor="middle">y, ẏ 측정</text>
    <rect x="124" y="258" width="132" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="190" y="273" font-size="11" text-anchor="middle">목표 임피던스</text>
    <text x="190" y="287" font-size="11" text-anchor="middle" xml:space="preserve">M<tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1">ë + D</tspan><tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1">ė + K</tspan><tspan dy="3.1" font-size="11">d</tspan><tspan dy="-3.1">e</tspan></text>
    <rect x="276" y="258" width="100" height="36" rx="3" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>
    <text x="326" y="273" font-size="11" text-anchor="middle" xml:space="preserve">τ = J<tspan dy="-4.2" font-size="11">T</tspan><tspan dy="4.2">F</tspan></text>
    <text x="326" y="287" font-size="11" text-anchor="middle">토크 인터페이스</text>
    <line x1="100" y1="276" x2="122" y2="276" stroke="currentColor" stroke-width="1.3" marker-end="url(#fcckA)"/>
    <text x="112" y="270" font-size="11" text-anchor="middle">e, ė</text>
    <line x1="256" y1="276" x2="274" y2="276" stroke="currentColor" stroke-width="1.3" marker-end="url(#fcckA)"/>
    <text x="266" y="270" font-size="11" text-anchor="middle">F</text>
    <line x1="376" y1="276" x2="426" y2="276" stroke="currentColor" stroke-width="1.3" marker-end="url(#fcckA)"/>
    <text x="402" y="270" font-size="11" text-anchor="middle">τ</text>
    <rect x="12" y="314" width="88" height="36" rx="3" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>
    <text x="56" y="329" font-size="11" text-anchor="middle" xml:space="preserve">손목에서 F<tspan dy="3.1" font-size="11">y</tspan></text>
    <text x="56" y="343" font-size="11" text-anchor="middle">힘 센서</text>
    <rect x="124" y="314" width="132" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="190" y="329" font-size="11" text-anchor="middle">가상 동역학</text>
    <text x="190" y="343" font-size="11" text-anchor="middle" xml:space="preserve">적분 → y<tspan dy="3.1" font-size="11">c</tspan></text>
    <rect x="276" y="314" width="100" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="326" y="329" font-size="11" text-anchor="middle">내부 위치</text>
    <text x="326" y="343" font-size="11" text-anchor="middle">루프</text>
    <line x1="100" y1="332" x2="122" y2="332" stroke="currentColor" stroke-width="1.3" marker-end="url(#fcckA)"/>
    <text x="112" y="326" font-size="11" text-anchor="middle" xml:space="preserve">F<tspan dy="3.1" font-size="11">y</tspan></text>
    <line x1="256" y1="332" x2="274" y2="332" stroke="currentColor" stroke-width="1.3" marker-end="url(#fcckA)"/>
    <text x="266" y="326" font-size="11" text-anchor="middle" xml:space="preserve">y<tspan dy="3.1" font-size="11">c</tspan></text>
    <line x1="376" y1="332" x2="426" y2="332" stroke="currentColor" stroke-width="1.3" marker-end="url(#fcckA)"/>
    <text x="402" y="326" font-size="11" text-anchor="middle">τ</text>
    <path d="M 488.0 258.0 L 488.0 248.0 L 56.0 248.0 L 56.0 256.0" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" marker-end="url(#fcckA)"/>
    <text x="300" y="244" font-size="11" fill-opacity="0.85">말단 운동</text>
    <path d="M 488.0 350.0 L 488.0 360.0 L 56.0 360.0 L 56.0 352.0" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" marker-end="url(#fcckA)"/>
    <text x="300" y="373" font-size="11" fill-opacity="0.85">접촉력</text>
    <text x="12" y="390" font-size="12" fill-opacity="0.85" font-weight="600">어드미턴스 — 힘을 재고 운동을 명령</text>
    <text x="548" y="390" font-size="11" text-anchor="end" fill-opacity="0.8">음영: 각 구조가 흉내 낼 수 없는 블록</text>
    <line x1="8" y1="408" x2="552" y2="408" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
    <text x="12" y="424" font-size="12" fill-opacity="0.85" font-weight="600">시계, 0에서 400 ms, 두 길이를 같은 축척으로</text>
    <text x="548" y="424" font-size="12" text-anchor="end" xml:space="preserve">T / t<tspan dy="3.4" font-size="11">contact</tspan><tspan dy="-3.4"> = 28.3</tspan></text>
    <path d="M 60.0 439.0 L 540.0 439.0" fill="none" stroke="currentColor" stroke-width="6" stroke-opacity="0.75" stroke-dasharray="0.45 0.75"/>
    <text x="54" y="443" font-size="11" text-anchor="end" fill-opacity="0.85">1 kHz</text>
    <line x1="60" y1="526" x2="540" y2="526" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4"/>
    <line x1="60" y1="566" x2="540" y2="566" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
    <path d="M 60 566 L 60 570 M 180 566 L 180 570 M 300 566 L 300 570 M 420 566 L 420 570 M 540 566 L 540 570" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
    <text x="60" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">0</text>
    <text x="180" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">100</text>
    <text x="300" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">200</text>
    <text x="420" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">300</text>
    <text x="540" y="582" font-size="11" text-anchor="middle" fill-opacity="0.85">400</text>
    <text x="12" y="582" font-size="11" fill-opacity="0.85">t (ms)</text>
    <path d="M 60 526 L 63 525 L 66 524 L 68.9 522.9 L 71.9 521.9 L 74.9 520.9 L 77.9 519.9 L 80.9 518.9 L 83.8 518 L 86.8 517 L 89.8 516.1 L 92.8 515.1 L 95.8 514.2 L 98.7 513.3 L 101.7 512.4 L 104.7 511.6 L 107.7 510.7 L 110.7 509.9 L 113.6 509.1 L 116.6 508.4 L 119.6 507.6 L 122.6 506.9 L 125.6 506.2 L 128.5 505.6 L 131.5 505 L 134.5 504.4 L 137.5 503.8 L 140.5 503.3 L 143.5 502.8 L 146.4 502.4 L 149.4 502 L 152.4 501.6 L 155.4 501.3 L 158.4 501 L 161.3 500.7 L 164.3 500.5 L 167.3 500.3 L 170.3 500.2 L 173.3 500.1 L 176.2 500 L 179.2 500 L 182.2 500 L 185.2 500.1 L 188.2 500.2 L 191.1 500.3 L 194.1 500.5 L 197.1 500.7 L 200.1 501 L 203.1 501.3 L 206 501.6 L 209 502 L 212 502.4 L 215 502.8 L 218 503.3 L 220.9 503.8 L 223.9 504.4 L 226.9 505 L 229.9 505.6 L 232.9 506.2 L 235.8 506.9 L 238.8 507.6 L 241.8 508.4 L 244.8 509.1 L 247.8 509.9 L 250.7 510.7 L 253.7 511.6 L 256.7 512.4 L 259.7 513.3 L 262.7 514.2 L 265.6 515.1 L 268.6 516.1 L 271.6 517 L 274.6 518 L 277.6 518.9 L 280.5 519.9 L 283.5 520.9 L 286.5 521.9 L 289.5 522.9 L 292.5 524 L 295.4 525 L 298.4 526 L 301.4 527 L 304.4 528 L 307.4 529.1 L 310.4 530.1 L 313.3 531.1 L 316.3 532.1 L 319.3 533.1 L 322.3 534 L 325.3 535 L 328.2 535.9 L 331.2 536.9 L 334.2 537.8 L 337.2 538.7 L 340.2 539.6 L 343.1 540.4 L 346.1 541.3 L 349.1 542.1 L 352.1 542.9 L 355.1 543.6 L 358 544.4 L 361 545.1 L 364 545.8 L 367 546.4 L 370 547 L 372.9 547.6 L 375.9 548.2 L 378.9 548.7 L 381.9 549.2 L 384.9 549.6 L 387.8 550 L 390.8 550.4 L 393.8 550.7 L 396.8 551 L 399.8 551.3 L 402.7 551.5 L 405.7 551.7 L 408.7 551.8 L 411.7 551.9 L 414.7 552 L 417.6 552 L 420.6 552 L 423.6 551.9 L 426.6 551.8 L 429.6 551.7 L 432.5 551.5 L 435.5 551.3 L 438.5 551 L 441.5 550.7 L 444.5 550.4 L 447.4 550 L 450.4 549.6 L 453.4 549.2 L 456.4 548.7 L 459.4 548.2 L 462.4 547.6 L 465.3 547 L 468.3 546.4 L 471.3 545.8 L 474.3 545.1 L 477.3 544.4 L 480.2 543.6 L 483.2 542.9 L 486.2 542.1 L 489.2 541.3 L 492.2 540.4 L 495.1 539.6 L 498.1 538.7 L 501.1 537.8 L 504.1 536.9 L 507.1 535.9 L 510 535 L 513 534 L 516 533.1 L 519 532.1 L 522 531.1 L 524.9 530.1 L 527.9 529.1 L 530.9 528 L 533.9 527 L 536.9 526" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <line x1="536.9" y1="561" x2="536.9" y2="571" stroke="currentColor" stroke-width="1.4"/>
    <line x1="536.9" y1="526" x2="536.9" y2="561" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4" stroke-dasharray="2 2"/>
    <text x="100.8" y="548" font-size="11" xml:space="preserve">목표 거동의 한 주기: T = 2π/ω<tspan dy="3.1" font-size="11">n</tspan><tspan dy="-3.1"> = 397 ms</tspan></text>
    <path d="M 60 526 L 60.4 522.1 L 60.8 518.3 L 61.3 514.5 L 61.7 510.8 L 62.1 507.2 L 62.5 503.7 L 63 500.3 L 63.4 497.1 L 63.8 494.1 L 64.2 491.2 L 64.6 488.6 L 65.1 486.2 L 65.5 484.1 L 65.9 482.2 L 66.3 480.6 L 66.7 479.2 L 67.2 478.2 L 67.6 477.4 L 68 477 L 68.4 476.8 L 68.9 477 L 69.3 477.4 L 69.7 478.2 L 70.1 479.2 L 70.5 480.6 L 71 482.2 L 71.4 484.1 L 71.8 486.2 L 72.2 488.6 L 72.6 491.2 L 73.1 494.1 L 73.5 497.1 L 73.9 500.3 L 74.3 503.7 L 74.8 507.2 L 75.2 510.8 L 75.6 514.5 L 76 518.3 L 76.4 522.1 L 76.9 526" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"/>
    <text x="81.6" y="484" font-size="11">충격: 반주기 사인,</text>
    <text x="81.6" y="498" font-size="11" xml:space="preserve">14 ms, F<tspan dy="3.1" font-size="11">max</tspan><tspan dy="-3.1"> = 22.4 N</tspan></text>
    <rect x="346" y="451" width="192" height="60" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
    <path d="M 346 451 L 346 457 M 355.6 451 L 355.6 457 M 365.2 451 L 365.2 457 M 374.8 451 L 374.8 457 M 384.4 451 L 384.4 457 M 394 451 L 394 457 M 403.6 451 L 403.6 457 M 413.2 451 L 413.2 457 M 422.8 451 L 422.8 457 M 432.4 451 L 432.4 457 M 442 451 L 442 457 M 451.6 451 L 451.6 457 M 461.2 451 L 461.2 457 M 470.8 451 L 470.8 457 M 480.4 451 L 480.4 457 M 490 451 L 490 457 M 499.6 451 L 499.6 457 M 509.2 451 L 509.2 457 M 518.8 451 L 518.8 457 M 528.4 451 L 528.4 457 M 538 451 L 538 457" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.75"/>
    <path d="M 346 508 L 349.4 504.1 L 352.7 500.3 L 356.1 496.5 L 359.5 492.8 L 362.9 489.2 L 366.2 485.7 L 369.6 482.3 L 373 479.1 L 376.3 476.1 L 379.7 473.2 L 383.1 470.6 L 386.5 468.2 L 389.8 466.1 L 393.2 464.2 L 396.6 462.6 L 400 461.2 L 403.3 460.2 L 406.7 459.4 L 410.1 459 L 413.4 458.8 L 416.8 459 L 420.2 459.4 L 423.6 460.2 L 426.9 461.2 L 430.3 462.6 L 433.7 464.2 L 437 466.1 L 440.4 468.2 L 443.8 470.6 L 447.2 473.2 L 450.5 476.1 L 453.9 479.1 L 457.3 482.3 L 460.6 485.7 L 464 489.2 L 467.4 492.8 L 470.8 496.5 L 474.1 500.3 L 477.5 504.1 L 480.9 508" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>
    <path d="M 346 508 L 350.8 507.8 L 355.6 507.6 L 360.4 507.4 L 365.2 507.2 L 370 507 L 374.8 506.8 L 379.6 506.6 L 384.4 506.4 L 389.2 506.2 L 394 505.9 L 398.8 505.7 L 403.6 505.5 L 408.4 505.3 L 413.2 505.1 L 418 504.9 L 422.8 504.7 L 427.6 504.5 L 432.4 504.3 L 437.2 504.1 L 442 503.9 L 446.8 503.7 L 451.6 503.5 L 456.4 503.3 L 461.2 503.1 L 466 502.9 L 470.8 502.7 L 475.6 502.5 L 480.4 502.3 L 485.2 502.1 L 490 501.9 L 494.8 501.7 L 499.6 501.5 L 504.4 501.3 L 509.2 501.1 L 514 500.9 L 518.8 500.7 L 523.6 500.5 L 528.4 500.3 L 533.2 500.1 L 538 499.9" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <text x="340" y="467" font-size="11" text-anchor="end" fill-opacity="0.85">처음 20 ms, ×8: 눈금 하나가</text>
    <text x="340" y="481" font-size="11" text-anchor="end" fill-opacity="0.85">샘플 하나, 충격 안에 14개</text>
  </g>
</svg>

**위 — 팔과 패널, $x$–$y$ 평면, 실제 비율.** 원점에 P2 베이스, 링크 1이 $+x$로 뻗어 엘보가 $(1,0)$, 링크 2가 올라가 말단이 $(1,1)$. 말단 아래에 패널 면의 수평선을 긋고(전완은 그림 평면 밖, 패널 앞으로 지나가므로 패널에 닿는 것은 말단뿐이다), 명령한 누름 $F=(0,-10)$ N을 말단에서 아래로 향한 화살표로, 로봇이 받는 반력을 같은 길이의 위 화살표로 그린다. 말단 옆에 직렬 스프링 둘을 그려 이름을 붙인다. 가상 스프링 $K_d=500$ N/m와 실제 스프링 $K_e=10^5$ N/m를, 가상 쪽 코일은 길게 늘이고 실제 쪽은 거의 납작하게 그린다. 이 그림이 할 일은 그 200이라는 비를 보여 주는 것 하나다.

**가운데 — 블록선도 둘을 위아래로, 오른쪽 플랜트 블록은 공유.** 임피던스: 말단에서 $(y,\dot y)$를 재고 목표 $M_d\ddot e+D_d\dot e+K_de$에 통과시켜 힘을 얻은 뒤 $\tau=J^\top F$로 옮겨 팔에 토크를 보낸다. 어드미턴스: 손목에서 $F_y$를 재고 가상 동역학을 적분해 운동 기준 $y_c$를 얻어 내부 위치 루프에 넘기고, 그 루프가 토크를 보낸다. 각 구조가 흉내 낼 수 없는 블록 — 위 행은 토크 인터페이스, 아래 행은 힘 센서 — 을 음영으로 칠하고, 패널에서 측정으로 돌아오는 되먹임 경로를 양쪽에 다 그린다.

**아래 — 시계, 밀리초 단위로 0에서 400 ms까지 한 축.** 접촉 사건을 $t=0$에서 시작하는 폭 $t_{\text{contact}}=14$ ms의 반주기 사인으로 표시한다. 같은 축 위에, 제어기가 명세한 거동의 한 주기 $T=2\pi/\omega_n=397$ ms를, 충격이 이미 끝났을 때 원점을 겨우 떠난 사인으로 그린다. 시계 위에는 1 kHz 샘플 눈금: 충격 안에 약 14개, 목표의 한 주기 안에 약 397개가 들어간다. 두 길이를 같은 축척으로 그려야 한다 — 그 비교가 곧 강의다.

### 대상으로 한 번 끝까지: P2의 목표 임피던스와 그것이 느낄 수 없는 충격 · Worked case

위의 대상에서 여섯 단계를 밟는다. §2와 §5가 말로 주장하는 모든 것이 여기서는 숫자다.

**1단계 — 명령을 관절 좌표로.** 패널을 $F=(0,-10)$ N으로 누르므로

$$\tau=J^\top F=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}\begin{pmatrix}0\\-10\end{pmatrix}=\begin{pmatrix}-10\\0\end{pmatrix}\ \mathrm{N\cdot m}$$

이고 엘보는 하나도 지지 않는다. 반올림이 아니다. $J$의 둘째 열이 $(-1,0)^\top$이라 이 자세에서 엘보만 움직이면 말단이 순수하게 $x$로 미끄러지고, 순수하게 수직인 힘은 거기에 일을 하지 않는다. 이 0은 팔에 관한 진술이 아니라 자세에 관한 진술이다.

**2단계 — 패널이 실제로 만나는 질량.** $\Lambda_y=2$ kg이다. 팔의 쇳덩이도 $m_1+m_2=2$ kg이라 이 일치가 함정이다. *같은* 자세에서 같은 2 kg으로부터 $\Lambda_x=1$ kg이 나온다. 겉보기 질량은 자세와 방향의 성질이고, §4의 작업공간 정식화가 존재하는 이유이자 $M_d=\Lambda_y$가 제어기에게 관성 성형을 전혀 요구하지 않는 목표 관성인 이유다.

**3단계 — 정적 거동.** 패널이 로봇을 위로 밀므로 $F_{ext}=+10$ N이고, 평형에서 목표 식은 스프링 항만 남는다.

$$e=\frac{F_{ext}}{K_d}=\frac{10}{500}=0.020\ \mathrm{m}$$

제어기가 끝내 없애지 않을 정상상태 오차 2 cm이고, 접촉에서는 그것이 실패가 아니라 명세다. 구속이 없으면 같은 10 N이 대신 $a_y=-10/2=-5\ \mathrm{m/s^2}$을 만든다.

**4단계 — 동적 거동.** 목표를 2차계로 읽으면

$$\omega_n=\sqrt{K_d/M_d}=\sqrt{500/2}=15.81\ \mathrm{rad/s}=2.52\ \mathrm{Hz},\qquad D_d\big|_{\zeta=1}=2\sqrt{K_dM_d}=63.2\ \mathrm{N\cdot s/m}$$

이다. 표준 2차계 파라미터이기 때문이다([[04-robotics/control-theory-ce397|5. 제어 이론 §5]]). $\zeta=0.7$이면 대신 $D_d=44.3$ N·s/m다. 댐퍼를 한번 점검하면, $0.05$ m/s에서 임계 감쇠 $D_d$가 내는 힘은 $63.2\times0.05=3.16$ N으로 누름의 3분의 1이다. 여기서 감쇠는 작은 보정이 아니다.

**5단계 — 지속 접촉에서 컴플라이언스는 누구 것인가?** 명령한 10 N에서 패널과 구조가 물러나는 양은 $10/K_e=10/10^5=0.1$ mm이고 가상 스프링이 물러나는 양은 20 mm다. 그래서 제어기가 전체 물러남의 $20/20.1=99.5\%$를 공급하는데, 이는 강성비 $K_e/K_d=200$을 $200/201$로 읽은 값이다. 그러니 *지속* 접촉에서 "유연하다"는 말은 제어기를 가리키고, 그 말은 정직하다.

**6단계 — 그러면 충격에서는?** 이제 $v=5$ cm/s로 $K_e=10^5$ N/m에 도착한다. §5의 반주기 사인 모델에서

$$F_{\max}=v\sqrt{\Lambda_yK_e}=0.05\sqrt{2\times10^5}=22.4\ \mathrm{N},\qquad t_{\text{contact}}=\pi\sqrt{\Lambda_y/K_e}=0.01405\ \mathrm{s}$$

이므로 22.4 N이 14.05 ms 안에 왔다가 가고, 1 kHz 루프는 그 안에 샘플을 약 14개 얻는다. 이것을 제어기가 명세한 거동의 한 주기 $T=2\pi/\omega_n=0.397$ s와 비교하면

$$\frac{T}{t_{\text{contact}}}=\frac{0.397}{0.01405}=28.3$$

**충격 전체가 목표 동역학 한 주기의 28분의 1 안에 끝난다.** 그래서 제어기가 명세한 거동은 사건이 끝날 때까지 반응을 시작조차 제대로 하지 못한다. 주파수 영역을 쓰지 않고 에너지로 말해도 같다. 공구가 지닌 에너지는 $\tfrac12\Lambda_yv^2=\tfrac12(2)(0.05)^2=2.5$ mJ이고, $K_d=500$ N/m 가상 스프링이 그것을 흡수하려면 $\sqrt{2E/K_d}=3.16$ mm를 눌려야 하는데, 공구는 구조가 멈춰 세우기 전에 $\sqrt{2E/K_e}=0.22$ mm밖에 들어가지 못한다 — 명령한 스프링에 필요했던 거리의 $7.1\%$다. 2.5 mJ 전부를 구조가 받아서 돌려주었다.

**그 비가 뜻하는 것과 무엇이 그것을 바꾸는가.** 유연 손목($K_e=10^4$)을 상대로는 비가 $8.9$로 내려가고, 이상화된 재료 행($10^7$)을 상대로는 $283$으로 오른다. 1 근처에 가는 일은 결코 없다. 28은 게인으로 벗어날 수 있는 튜닝 실패도 아니다. $T=t_{\text{contact}}$로 두면 $2\pi/\omega_n=\pi\sqrt{\Lambda_y/K_e}$, 곧 $\omega_n=2\sqrt{K_e/\Lambda_y}$이므로 $M_d=\Lambda_y$에서

$$K_d=4K_e=4\times10^5\ \mathrm{N/m}$$

이고, 이는 여기서 고른 강성의 800배이며 1 kHz 루프가 단단한 표면을 상대로 구현할 수 있는 범위를 한참 넘는다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]). 반대 방향, 곧 $K_e$를 낮추는 것은 제어가 아니라 기계의 변경이고, 그것이 §5의 수동 컴플라이언스 논증 전체다. 그러니 이것이 §5의 주장을 산수로 쓴 것이다. **제어기는 지속 접촉을 소유하고 충격은 사실상 하나도 소유하지 않는다.** 컴플라이언스 개선을 보고하면서 정상 접촉만 보여 주는 논문은 쉬운 절반을 보고한 것이다. Research Practice의 관통 연구 RS1은 이 팔 위의 임피던스 제어를 힘 문턱 정지가 붙은 위치 제어와 400 N/m 패널에서 비교하는데, 같은 반주기 사인 모델에서 그 접촉은 $\pi\sqrt{2/400}=0.222$ s 이어진다. [[06-research-practice/research-questions-claims|1. 연구 질문과 주장]] worked case의 5행은 그것을 이 14 ms와 나란히 놓아, 그 결과가 단단한 패널로 옮겨 가지 않는 이유를 보인다.

### 1. 뻣뻣한 위치 추종이 접촉에서 위험해지는 이유

위치 제어기의 일은 위치 오차를 0으로 모는 것이고, 그러기 위해 필요한 힘이 얼마든 그것을 쓴다.
자유 공간에서는 정확히 옳다. 접촉에서는 물건을 부수라는 명세가 된다. 이제 위치 오차가 무엇을
뜻하는지를 환경이 결정하기 때문이다.

[[04-robotics/contact-force-tactile|접촉·힘·촉각 §6]]의 벽을 보자: **유연하게 장착된** 도구가
대략 $K_e = 10^4$ N/m인 표면에 닿는데, 표면보다 1 cm 안쪽을 명령했다.

$$F = K_e\,\Delta x = 10^4 \times 0.01 = 100\ \text{N}$$

제어기가 100 N으로 밀기로 "결정"한 것이 아니다. 그 강성에 대해 1 cm 오차를 닫는 비용이 그저
그것일 뿐이다. 같은 상황에서 $K = 200$ N/m를 구현하는 유연한 제어기는 $200 \times 0.01 = 2$ N을
낸다. 이 제어기는 끝내 해소하지 않는 1 cm 오차를 유지한다. 접촉에서는 이것이 실패가 아니라 올바른 거동이다.

> [!info] 정의 · Definition — 강성, 컴플라이언스, 감쇠
> **어떤 종류의 것인가.** 한 포트에서의 선형 역학 관계를 이루는 *계수* 셋이다. 각각 단위가 다르고, 같은 접촉에 대해 서로 다른 질문에 답한다. 부품이 아니라 관계의 성질이라는 점이 사람들이 빠뜨리는 조건이다.
>
> - **강성** $K$, 단위 N/m: 단위 변위당 힘, $F=K\,\Delta x$. "이만큼의 위치 오차가 힘으로 얼마인가?"에 답한다.
> - **컴플라이언스** $C=1/K$, 단위 m/N: 단위 힘당 변위. 같은 내용을 질문만 뒤집은 것이다 — "이만큼의 힘이면 얼마나 움직이는가?" 위의 벽 $K_e=10^4$ N/m은 $C=10^{-4}$ m/N, 곧 뉴턴당 $0.1$ mm다. $K=200$ N/m 제어기는 $C=5\times10^{-3}$ m/N, 곧 뉴턴당 $5$ mm다.
> - **감쇠** $D$, 단위 N·s/m: 단위 *속도*당 힘, $F=D\,\dot x$. 약한 스프링이 아니다. 운동이 멈추면 힘을 전혀 내지 않고, 그래서 댐퍼는 위치를 지킬 수 없고 스프링은 에너지를 소산할 수 없다 — §2의 목표식에 두 항이 다 필요한 이유다.
>
> **정의 조건, 그리고 컴플라이언스가 쓸모 있는 이유.** 이 계수들이 사슬 전체에 걸친 관계를 기술하므로, **직렬**로 놓인 요소들은 *컴플라이언스*로 결합하고 컴플라이언스는 그냥 더해진다.
>
> $$C_{eq}=C_1+C_2\quad\Longleftrightarrow\quad \frac{1}{K_{eq}}=\frac{1}{K_1}+\frac{1}{K_2}$$
>
> 같은 힘이 두 요소를 모두 지나가고 변형이 더해지기 때문이다. $C_1=10^{-5}$, $C_2=10^{-7}$ m/N이면 합이 $1.010\times10^{-5}$ m/N이므로 $K_{eq}=9.90\times10^{4}$ N/m이고, 더 무른 요소가 물러남의 $99.0\%$를 담당한다. "가장 무른 요소가 이긴다"는 그 산수이지 구호가 아니고, §5는 충격 논증 전체를 그 위에서 돌린다.
>
> **예.** 계속 쓰는 대상의 지속 접촉: $K_d=500$ N/m과 $K_e=10^5$ N/m이 직렬이면 $C_{eq}=2\times10^{-3}+10^{-5}=2.01\times10^{-3}$ m/N이므로 말단에서 물러남의 $99.5\%$를 제어기가 공급한다.
>
> **반례.** 숫자 없는 "유연한 제어기"는 명세가 아니다. $K_d=10^5$ N/m도 구현된 강성이다. 그리고 방향성이 있는 장치에 *스칼라* 강성 하나는 명세가 아니다. Remote-centre compliance는 측면으로 약 $10^4$ N/m, 축 방향으로 약 $10^6$ N/m이므로(§5), 수 하나로 적으면 두 방향 중 하나에서 두 자릿수만큼 틀린다.
>
> **왜 중요한가.** 아래 표의 모든 행, §2의 모든 $K_d$, §3에서 어느 방향을 단단하게 둘지 고르는 일, §5의 충격 산수가 전부 이 세 계수다. 셋 중 아무것도 보고하지 않은 접촉 주장은 단위가 없는 주장이다.

환경 강성의 눈금을 갖고 있어야 한다. 환경 강성은 다섯 자릿수에 걸쳐 있고, 논문은 숫자 대신 접촉을
이름으로 부른다. 같은 제어 법칙이 한쪽 끝에서는 안전하고 반대쪽 끝에서는 불가능하다:

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

**넷째 행의 출처: 헤르츠 접촉.** 한 점에서 닿은 두 탄성체는 선형 스프링처럼 거동하지 않는다. 반지름 $R$인 구를 평면에 깊이 $\delta$만큼 누르면 Hertz의 해는 다음과 같다.

$$F=\tfrac43\,E^*\sqrt{R}\,\delta^{3/2},\qquad k=\frac{dF}{d\delta}=\frac{3F}{2\delta}$$

$E^*$는 합성 탄성계수로 $1/E^*=(1-\nu_1^2)/E_1+(1-\nu_2^2)/E_2$이고, $E_i$는 영률, $\nu_i$는 푸아송 비다. 누를수록 접촉 면적이 커지므로 국소 강성 $k$는 하중과 함께 오르고, 스칼라 $K_e$ 하나는 한 힘에서의 선형화일 뿐이다. 반지름 5 mm 강구가 강판에 닿을 때($E=200$ GPa, $\nu=0.3$이므로 $E^*=110$ GPa) 10 N은 $0.98\ \mu$m를 누르고 $k=1.5\times10^7$ N/m, 100 N은 $4.5\ \mu$m를 누르고 $k=3.3\times10^7$ N/m이다. 둘 다 넷째 행 안이다.

위 예는 둘째 행에 있다. **도달 불가능한 침투 위치를 높은 폐루프 강성으로 명령하면 위험하다.**
이 표는 국소 선형화를 외삽한 위험 규모다. 1 cm에서의 실제 힘 예측은 아니다:
$10^7$ N/m를 그대로 쓰면 $10^5$ N이 나온다. 실제 힘은 제어기·로봇·툴·환경의 직렬 등가강성과 포화로 제한된다. §5도 같은 두 행으로 충격력을 계산한다. "단단한 접촉"이라는 주장은 언제나
이 표의 어느 행인지로 되읽어야 한다.

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="10의 2승부터 8승까지 로그 눈금의 환경 강성 축과, 그중 세 곳에서 1 cm 오차가 만드는 힘">
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="24" y="18">1 cm 위치 오차가 만드는 힘</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.6">
    <line x1="70" y1="112" x2="520" y2="112"/>
    <line x1="70.0" y1="112" x2="70.0" y2="120"/><line x1="145.0" y1="112" x2="145.0" y2="120"/><line x1="220.0" y1="112" x2="220.0" y2="120"/><line x1="295.0" y1="112" x2="295.0" y2="120"/><line x1="370.0" y1="112" x2="370.0" y2="120"/><line x1="445.0" y1="112" x2="445.0" y2="120"/><line x1="520.0" y1="112" x2="520.0" y2="120"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.7" text-anchor="middle">
    <text x="70.0" y="134">10²</text><text x="145.0" y="134">10³</text><text x="220.0" y="134">10⁴</text><text x="295.0" y="134">10⁵</text><text x="370.0" y="134">10⁶</text><text x="445.0" y="134">10⁷</text><text x="520.0" y="134">10⁸</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.6">
    <text x="70" y="150">폼, 판지</text>
    <text x="230" y="150">힘 제어기가 식별하는 값</text>
    <text x="470" y="150">헤르츠 접촉</text>
  </g>
  <g><line x1="92.6" y1="96" x2="92.6" y2="112" stroke="currentColor" stroke-width="1" opacity="0.45"/><circle cx="92.6" cy="96" r="4" fill="currentColor"/><line x1="220.0" y1="70" x2="220.0" y2="112" stroke="currentColor" stroke-width="1" opacity="0.45"/><circle cx="220.0" cy="70" r="4" fill="currentColor"/><line x1="445.0" y1="44" x2="445.0" y2="112" stroke="currentColor" stroke-width="1" opacity="0.45"/><circle cx="445.0" cy="44" r="4" fill="currentColor"/></g>
  <g font-size="10.5" fill="currentColor"><text x="101.6" y="100">2 N</text><text x="101.6" y="112" font-size="9" opacity="0.75">유연하게 만든 제어기</text><text x="229.0" y="74">100 N</text><text x="229.0" y="86" font-size="9" opacity="0.75">유연하게 장착한 공구(둘째 행)</text><text x="436.0" y="48" text-anchor="end">100,000 N</text><text x="436.0" y="60" font-size="9" opacity="0.75" text-anchor="end">강철 대 강철, 국소 재료 접촉</text></g>
  <g font-size="9.5" fill="currentColor" opacity="0.75">
    <text x="24" y="170">환경 강성 K&#7497; (N/m), 로그 눈금</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="200">제어기가 100 N으로 밀기로 결정한 것이 아니다. 그 강성에서 1 cm 오차를 닫는 비용이 그저</text>
    <text x="24" y="216">그것일 뿐이다. 행 사이가 다섯 자릿수라서 같은 제어 법칙이 한쪽 끝에서는 안전하고 반대쪽</text>
    <text x="24" y="232">끝에서는 불가능하다 &#8212; 구조물에 겨눈 위치 제어기는 오차가 닫히기 한참 전에 힘이 발산한다.</text>
    <text x="24" y="248">&#8220;단단한 접촉&#8221;이라는 주장은 언제나 이 축의 어느 자리인지로 되읽어라.</text>
  </g>
</svg>

**접촉은 위치와 힘을 결합한다.** 이상적인 강체 벽에서 자연 제약은 법선 속도가 0이라는 것이다. 이는 접촉이 유지되는 동안 성립한다. 제어기는 법선 힘의 목표를 고를 수 있다. 접선 운동은 마찰의 제약 아래 가능하다. 유연한 접촉에서는 법선 변위와 힘이 접촉 역학으로 연결된다. 따라서 같은 구속 방향에 독립적이고 임의적인 위치·힘 목표를 동시에 주면 충돌할 수 있다. 하이브리드 제어(§3)는 상보적인 운동·힘 목표를 고른다. 어떤 방향은 위치를, 나머지 방향은 힘을 추종한다. 임피던스 제어(§2)는 대신 둘 사이에 가상 스프링을 두듯 둘의 관계를 정한다.

강성 그림은 단순한 국소 선형 비교다. 그것은 액추에이터가 무한한 힘을 낸다는 예측이 아니다. 실제 토크 한계·구조 유연성·접촉 비선형성이 반응을 제한하거나 바꾼다. 낮은 게인의 위치 기반 제어기도 컴플라이언스를 구현할 수 있다. 위험은 도달할 수 없는 위치를 과도한 강성이나 적분 동작으로 요구할 때 생긴다.

### 2. 임피던스와 어드미턴스 — 같은 발상, 반대 인과

둘 다 운동과 상호작용 힘 사이의 원하는 관계를 정한다. 고정 기준 $x_d$를 둔다. 변위 $e=x-x_d$를 정의하고, $F_{ext}$를 **로봇에 가해지는** 외력이라 하자. 한 축의 목표 거동은 다음과 같다.

$$M_d\ddot e+D_d\dot e+K_de=F_{ext}.$$

$M_d$, $D_d$, $K_d$는 원하는 관성·감쇠·강성이다. 이 식은 원하는 폐루프 거동이다. 실제 팔에 보낼 토크 명령 자체는 아니다. 가상 기계로 읽으면 쉽다. 외력이 먼저 질량을 가속한다. 감쇠가 운동을 억제한다. 스프링이 기준 위치로 되돌린다. 정적 평형에서는 속도와 가속도가 사라져 $K_de=F_{ext}$만 남는다. 같은 힘이면 낮은 강성에서 변위가 더 크다. 두 인과 중 무엇을 만들 수 있는지는 하드웨어가 정한다. 결정 요인은 전동 마찰, 반사 관성, 그리고 힘을 재는지 명령하는지다. [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 햅틱 장치 설계와 기구학]]이 직교 힘에서 모터 전류까지 그 사슬을 따라간다.

**임피던스를 항마다 정의하면.** **임피던스**는 운동에서 힘으로 가는 동적 사상이고, **임피던스 제어**는 외력에 대한 로봇의 응답이 고른 임피던스를 따르도록 폐루프를 설계한 모든 제어기다. 목표 거동에는 이름 붙은 세 항이 있고, 각각이 힘이다.

- **관성 항** $M_d\ddot e$: 가속에 저항한다. $M_d$(kg)는 환경이 느껴야 할 겉보기 질량이다.
- **감쇠 항** $D_d\dot e$: 속도에 저항한다. $D_d$(N·s/m)가 에너지를 소산한다.
- **강성 항** $K_de$: 기준 쪽으로 끌어당긴다. $K_d$(N/m)는 가상 스프링이다.

라플라스 영역에서 속도 $V(s)=sE(s)$로 쓰면 같은 목표가 속도에서 힘으로 가는 전달함수가 되고, **어드미턴스**는 그 역, 곧 힘에서 운동으로 가는 사상이다.

$$Z(s)=\frac{F_{ext}(s)}{V(s)}=M_ds+D_d+\frac{K_d}{s},\qquad Y(s)=\frac{1}{Z(s)}$$

그래서 임피던스 제어기는 운동을 재고 힘을 내며, 어드미턴스 제어기는 힘을 재고 운동을 낸다. 절 제목의 인과가 이것이다. 목표를 질량-스프링-댐퍼로 읽으면 표준 2차계 파라미터인 고유 진동수 $\omega_n=\sqrt{K_d/M_d}$와 감쇠비 $\zeta=D_d/(2\sqrt{K_dM_d})$가 나온다([[04-robotics/control-theory-ce397|제어 이론 §5]]). 어드미턴스 쪽에는 자기만의 시간 영역 목표식이 따로 있다 — 제어기가 적분해서 내부 루프에 넘길 운동 기준 $x_c$를 만드는 가상 동역학이고, 항마다 풀어 쓴 곳은 [[04-robotics/contact-force-tactile|9. 접촉·힘·촉각 §5]]다.

> [!example] 계산 예제 · Worked example
> $M_d=2$ kg, $K_d=500$ N/m. 일정한 10 N 밀기는 $e=F_{ext}/K_d=10/500=0.02$ m에서 멈춘다. 고유 진동수는 $\sqrt{500/2}=15.8$ rad/s이고, 임계 감쇠($\zeta=1$)에는 $D_d=2\sqrt{500\times2}=63.2$ N·s/m가 필요하다.
> **그 숫자가 $y$에서의 장치 P2다.** 카탈로그 자세 $\theta=(0^\circ,90^\circ)$의 $\Lambda=\mathrm{diag}(1,2)$([[02-foundations/lab-plants|0.6]], [[02-foundations/manipulator-kinematics-dynamics|10]])이므로 $\Lambda_y=2\,\mathrm{kg}$은 말단에서 $y$로 보이는 겉보기 질량이지 금속 $2\,\mathrm{kg}$이 아니다. 패널에 $F=(0,-10)$: $\tau=J^\top F=(-10,0)\,\mathrm{N{\cdot}m}$. 패널이 로봇을 $+y$로 밀므로 $F_{ext}=+10\,\mathrm{N}$이고 $0.02\,\mathrm{m}$ 처짐은 $+y$다. 구속이 없으면 $a_y=-5\,\mathrm{m/s}^2$. 강철에 대해서는 벽을 위치가 정한다. 임피던스는 여전히 $10\,\mathrm{N}$을 명령하고, 어드미턴스는 운동을 명령해 늦은 힘 오차가 벽으로의 밀침이 된다. 과제는 이 예제를 블록선도 둘로 묻는 것이다.
> **반례**: 운동과 상관없이 $F=F_d$를 유지하는 제어기는 운동과 힘 사이의 관계를 정하지 않으므로 임피던스가 아니라 힘 제어다. 또 "무름"은 정의에 들어 있지 않다. $K_d=10^5$ N/m도 아주 단단하지만 온전한 임피던스다.

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

그림은 **흔한 두 구현**이다. 같은 이름을 쓰는 모든 제어기의 필수 하드웨어 조건은 아니다.

- **토크 기반 임피던스**는 운동 오차에서 복원력을 계산하고 관절 토크로 변환한다. 반응이 빠른 토크 인터페이스가 유리하다. 작은 기계 마찰과 역구동 가능성(backdrivability)도 도움이 된다. 역구동 가능한 관절은 모터와 감속기의 저항 없이 외부에서 밀어 돌릴 수 있다. 그러나 그것이 임피던스의 정의는 아니다. 강성은 과제에 맞게 고른다. 항상 “기본적으로 무른” 것은 아니다. 기어 달린 관절이 얼마나 역구동하기 어려운지, 곧 모터 쪽 임피던스마다 $n^2$가 곱해져 관절에 닿는다는 것은 [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §7]]에 있다.
- **어드미턴스**는 측정·추정한 외력을 가상 동역학에 넣고 적분해 운동 기준을 만든다. 내부 운동 제어기가 그 기준을 추종한다. 위치·속도 명령을 받는 로봇에 유용하다. 실제 거동은 외부 힘 피드백과 내부 루프 양쪽에 달렸다.

| 구조 | 유용한 출발점 | 확인할 조건 |
|---|---|---|
| 토크 기반 임피던스 | 변위에 대한 팔의 반응을 설계 | 토크 대역폭, 동역학 보상, 게인, 포화 |
| 내부 운동 루프를 둔 어드미턴스 | 힘 피드백을 운동 기준으로 변환 | 센서·추정 지연, 내부 추종, 가상 동역학, 접촉 강성 |

단단한 벽에서는 작은 운동이 큰 힘 변화를 만든다. 어드미턴스 루프의 힘 피드백이 늦으면 보정 운동이 과해져 진동할 수 있다. 그러나 적절한 동역학·대역폭·하드웨어로 안정화할 수 있다. 강성만으로 실패를 단정할 수 없다. 반대로 임피던스도 자유 공간의 운동을 추종할 수 있다. 핵심은 전체 로봇이 해당 조건에서 어떤 거동을 실제로 구현할 수 있느냐다.

> [!warning] 구조와 강성 · Architecture and stiffness
> 손목 힘 센서만으로 제어 구조를 판정하지 않는다. 신호가 어디에 들어가며 무엇을 명령하는지 본다. 또한 수동 선형 스프링 두 개가 **직렬**이면 $1/K_{eq}=1/K_1+1/K_2$다. 강성을 더하는 것이 아니다. 같은 힘 $F$가 두 스프링을 모두 지나고 변형이 더해지므로 $F/K_{eq}=F/K_1+F/K_2$이기 때문이다. $K_1=10^5$, $K_2=10^7$ N/m이면 $K_{eq}=9.90\times10^4$ N/m로, 더 무른 스프링이 직렬 강성을 정한다(§5가 바로 이것을 쓴다). 피드백 안정성은 이 정적 등가식만으로 판단할 수 없고 동적 모델이 필요하다. 제어 블록을 [[02-foundations/manipulator-kinematics-dynamics|10. §8]]과 연결한다.

> [!question] 모델 확인 · Check the model
> 일정 외력 아래 로봇이 정지하면 어떤 항이 남는가? **답:** 고정 기준 모델의 스프링 항만 남는다. 실제 반응이 진동하면 관성·감쇠·피드백 지연·추종을 살펴본다. 정적 스프링 식만으로 진동을 설명할 수 없다.

점질량 로봇에서 토크 명령까지의 유도는 [MIT 매니퓰레이터 제어 노트](https://manipulation.mit.edu/force.html)를 보라. 원하는 상호작용 식과 그것을 실현하려는 구현을 나눠 읽는다.

### 3. 하이브리드 위치/힘 제어

Mason의 제약 분석이 어느 방향이 환경의 것인지를 말해 준다. Raibert와 Craig의 1981년
아키텍처는 그것을 실행하는 방법이다: 과제 프레임을 고르고, 각 방향을 어느 제어기에 배정할지를
0과 1로 적은 대각 **선택 행렬** $S$를 고른다.

$$\tau = J^\top\left[\,S\,\mathcal{F}_{\text{pos}} + (I - S)\,\mathcal{F}_{\text{force}}\right]$$

$S$는 위치 제어에 배정된 작업공간 렌치 성분만 남기고, $I-S$는 상보적인 힘 제어 성분을
남긴다. $J^\top$은 합쳐진 작업공간 렌치를 관절 토크로 옮긴다. 이 식은 이상적인 작업공간
분할을 나타내며, 실제 구현은 동역학·포화·모델 오차를 별도로 처리해야 한다.

$S$ 방향에서는 위치 제어가, 나머지 방향에서는 힘 제어가 돈다. 이상적인 모델에서는 두 투영
목표가 같은 축을 건드리지 않는다. 표면을 따라 공구를 미끄러뜨린다면: 접선 두 방향은 위치 제어, 법선 방향은
힘 제어.

**자연 제약, 인공 제약, 선택 행렬의 정의.** Mason의 분석은 **과제 프레임**, 곧 접촉점에 두고 축을 표면 법선과 접선에 맞춘 좌표계에서 이루어지며, 그 여섯 방향(병진 셋, 회전 셋)을 두 번 나눈다.

- **자연 제약**은 제어기가 무엇을 하든 접촉이 부과하는 조건이다. 표면이 막는 방향에서는 속도가 0이고, 표면이 열어 둔 방향에서는 이상적인 무마찰 접촉이 힘을 전달하지 못한다.
- **인공 제약**은 제어기가 나머지 자리에 더하는 목표다. 운동이 막힌 곳에는 원하는 힘을, 운동이 자유로운 곳에는 원하는 위치나 속도를 준다.

방향마다 자연 제약 하나와 인공 제약 하나가 정확히 배정되므로, 어느 축도 위치 목표와 힘 목표를 동시에 갖지 않는다. **선택 행렬**은 과제 프레임의 방향마다 원소 하나씩으로 이 분할을 기록한다.

$$S=\mathrm{diag}(s_1,\dots,s_6),\qquad s_j=\begin{cases}1 & \text{direction } j \text{ is free, so position-controlled}\\ 0 & \text{direction } j \text{ is blocked, so force-controlled}\end{cases}$$

($s_j=1$이면 방향 $j$가 자유라서 위치 제어, $0$이면 막혀 있어서 힘 제어.) 제어 법칙의 $\mathcal{F}_{\text{pos}}$는 위치 제어기(예: 자세 오차에 대한 PD)가 내는 렌치, $\mathcal{F}_{\text{force}}$는 힘 제어기(예: 힘 오차에 대한 PI)가 내는 렌치이고, 둘 다 과제 프레임에서 표현한다.

> [!example] 계산 예제 · Worked example
> 탁자 닦기, 병진만, $z$가 법선. 자연 제약: $v_z=0$, $f_x=f_y=0$. 인공 제약: $x$·$y$ 방향의 원하는 접선 속도와 $z$ 방향의 원하는 누르는 힘. 그래서 $S=\mathrm{diag}(1,1,0)$이다. 위치 루프가 $\mathcal{F}_{\text{pos}}=(3,-1,7)$ N을, 힘 루프가 $\mathcal{F}_{\text{force}}=(0.5,0.2,-10)$ N을 요구하면 명령은 $S\mathcal{F}_{\text{pos}}+(I-S)\mathcal{F}_{\text{force}}=(3,-1,-10)$ N이다. 법선 방향으로 위치 루프가 낸 7 N은 버려진다.
> **반례**: $S$는 과제 프레임에서만 대각이다. 탁자가 실제로 $x$축 둘레로 $10°$ 기울어 있으면 월드 축에서 올바른 행렬은 $RSR^\top$이고, 그 $y$–$z$ 블록은 $\begin{pmatrix}0.970&0.171\\0.171&0.030\end{pmatrix}$다. 월드 축에서 그대로 $\mathrm{diag}(1,1,0)$을 쓰면 힘 루프가 부분적으로 표면을 따라 작용한다. 바로 다음에 설명하는 자세 오차 실패다.

구속 조작 과제를 *명세 가능하게* 만든 아키텍처이고, 그 한계는 그 전제와 같다 — 과제 프레임과
접촉 기하를 안다고 가정한다. 과제 프레임이 정확하고 모델이 충분하면 분할이 깔끔하고 비교적
쉽게 튜닝할 수 있다. 3 mm **병진** 오차는 접촉을 너무 일찍·늦게 또는 잘못된 점에서 일으키지만 그 자체로
표면 법선을 회전시키지는 않는다. 자세나 국소 형상 오차가 실제 법선을 돌리면 명목 선택 행렬이
접선 운동과 법선 힘을 섞는다. 둘 다 건설 기하가 공장용 제어기를 깨뜨리는 흔한 방식이지만
기전은 다르다.

### 4. 작업공간(operational space) 제어

Khatib의 1987년 정식화가 앞의 두 절을 점질량이 아니라 실제 팔 위에서 구현 가능하게 만든다.
제어를 [[02-foundations/manipulator-kinematics-dynamics|10. §6]]의 작업 공간 관성을 써서 과제
좌표에서 직접 쓴다:

$$\mathcal{F} = \Lambda(\theta)\,\ddot x_d + \mu(\theta,\dot\theta) + p(\theta), \qquad \tau = J^\top\mathcal{F}$$

($\Lambda=(JM^{-1}J^\top)^{-1}$는 작업 공간 관성으로 말단이 지닌 것처럼 보이는 질량이고 $M$은 관절 공간 질량 행렬, $\ddot x_d$는 명령한 말단 가속도, $\mu$와 $p$는 작업 공간의 코리올리·중력 항). 팔의 운동방정식을 말단 좌표로 다시 쓰고, 원하는 말단 가속도를 만들 힘에 대해 푼 것으로 읽어라. $J^\top$이 그 힘을 관절 토크로 되돌린다. 중요한 귀결 둘:

- 팔의 자세 의존적 관성이 **보상된다.** 그래서 명령한 작업 공간 거동이 모든 자세에서 같아진다.
  이것이 없으면 [[02-foundations/manipulator-kinematics-dynamics|10. §3]]의 5배 관성 변화가
  곧바로, 명세했다고 믿은 접촉 거동의 자세 의존적 변화로 나타난다.
- 여유 자유도 해소가 **영공간 투영**이 된다($J$의 영공간은 말단을 움직이지 않는 관절 운동의 집합 $\{\dot\theta: J\dot\theta=0\}$이다, [[02-foundations/linear-algebra|1. 선형대수 §2]]): 여유 자유도가 있는 팔은 작업 공간 힘을 전혀 만들지
  않는 운동으로 부차 목표 — 관절 한계에서 멀어지기, 팔꿈치를 작업자에게서 비키기 — 를 만족할 수
  있다. 사람이 있는 현장의 모바일 매니퓰레이터에게 이것은 덤이 아니라 기제 그 자체다.

**투영자를 실제로 써 보면.** "영공간"은 문헌에서 느슨하게 쓰이므로 그 대상을 직접 볼 값어치가
있다. 쉽게 말해 투영자는 부차 토크에 거는 필터다. $\tau_0$가 작업이 느끼지 못하는 방식으로만 팔을
움직이게 한다. 지켜볼 것은 작업이 *언제* 그것을 느끼지 못하느냐다. 정지해 있을 때만(정적)인가, 팔이
움직이는 동안에도(과도)인가. 투영자들은 바로 그 지점에서 갈리고, 두 답에는 이름이 있다. 정적 일관성(static consistency)이란 팔이 멈춘 뒤 작업에 남는 힘이 없다는 뜻이다. 동역학적 일관성(dynamic consistency)이란 팔이 아직 움직이는 동안에도 작업이 아무것도 느끼지 못한다는 뜻이다. $\bar J = M^{-1}J^\top\Lambda$를 자코비안의 동역학적으로 일관된 역이라 하면, 부차 토크는
다음을 통과한다:

$$\tau = J^\top\mathcal{F} + \underbrace{\left(I - J^\top\bar J^{\,\top}\right)}_{\text{영공간 투영자 } N^\top}\tau_0$$

여기서 $\tau_0$는 부차 목표가 요구하는 무엇이든 된다. 투영자의 임무는 **$\tau_0$가 작업을
교란할 수 없게** 하는 것이다. 다만 *어떤* 교란인지를 정확히 해야 한다. 이 부분은 거꾸로 서술되는
일이 흔하다: 평범한 Moore–Penrose 유사역행렬([[02-foundations/linear-algebra|1. 선형대수 §4.5]])로 만든 투영자도 이미 **정적으로 일관되다** —
정상 상태에서 부차 토크는 작업 힘을 전혀 만들지 않는다. 그것이 막지 못하는 것은 과도 구간에서
작업이 *가속되는* 것이다. $M \neq I$이면 Moore–Penrose $N^\top$에 대해 $JM^{-1}N^\top\tau_0 \neq 0$이기 때문이다.
**동역학적 일관성이 사는 것은 정적인 힘이 아니라 과도 구간이다**. 이 형태의 투영자 가운데
$JM^{-1}N^\top = 0$을 만드는 것은 관성으로 가중한 역 $\bar J$뿐이다(Khatib 1987, Dietrich,
Ott, Albu-Schäffer, *IJRR* 2015 §3.3.1에서 재진술). 이 서베이는 정적 일관성을 어떤 정적 평형에서도
간섭하는 힘이 없는 것으로 정의하고 모든 가중 행렬이 이를 갖는다고 보인다(§3.2). 동역학적 일관성은
어느 시점에도 간섭하는 가속이 없다는 조건을 더한다(§3.3). 구조가 다른 투영자
$M(I - J^{+}J)M^{-1}$도 동역학적으로 일관되지만 하중 독립성은 없다(§3.3.2).

**무엇이 투영자를 만드는가, 그리고 3관절 확인.** **투영자**는 $P^2=P$인 행렬 $P$로, 두 번 적용해도 더 바뀌는 것이 없다. $J\bar J=JM^{-1}J^\top\Lambda=I$이므로 $(J^\top\bar J^{\,\top})^2=J^\top\bar J^{\,\top}$이고, 따라서 $N^\top$은 투영자다. 두 일관성은 그것에 대한 두 조건이다.

- **정적 일관성**: 정지 상태에서 걸러진 토크가 작업 힘을 만들지 않는다. 곧 최소자승 작업 힘 $J^{+\top}N^\top\tau_0$가 0이다.
- **동역학적 일관성**: 모든 순간에 걸러진 토크가 작업 가속을 만들지 않는다. 아래 조건이 그것이다.
$$J\,M^{-1}N^\top=0$$

> [!example] 계산 예제 · Worked example
> 관절 셋, 작업 방향 하나: $M=\mathrm{diag}(2,1,1)$, $J=(1,1,1)$, 부차 토크 $\tau_0=(1,0,0)$. 그러면 $\Lambda=(JM^{-1}J^\top)^{-1}=1/2.5=0.4$, $\bar J=M^{-1}J^\top\Lambda=(0.2,0.4,0.4)$이므로 $N^\top\tau_0=(0.8,-0.2,-0.2)$이고 작업 가속 $JM^{-1}N^\top\tau_0=0.4-0.2-0.2=0$이다. 대신 Moore–Penrose 역 $J^+=(1/3,1/3,1/3)$을 쓰면 $N^\top\tau_0=(2/3,-1/3,-1/3)$이다. 작업 힘 $J^{+\top}N^\top\tau_0=0$이라 정적으로는 일관되지만, $JM^{-1}N^\top\tau_0=1/3-1/3-1/3=-1/3\neq0$이라 과도 구간에서 작업이 가속된다. 위 문단이 경고한 반례가 이것이다.

**과제 우선순위, 그리고 whole-body control.** 목표를 둘 이상 쌓으면 이것이 계층이 된다: 각
층이 자기 위의 모든 층의 영공간으로 투영되므로, 낮은 우선순위가 높은 것과 다툴 수 없다. 그것이
고전적 형태다. 현대적 형태는 같은 문제를 매 제어 스텝의 **이차 계획법(QP)** 으로 푼다. QP는 선형 등식·부등식 제약 아래 이차 비용을 최소화하는 문제이고, 표준형은 [[02-foundations/optimization|4. 최적화 §5]]에 정의되어 있다 —

- 가중된 과제 오차를 최소화하고,
- 관절 위치·속도·토크 한계, 접촉점의 마찰 원뿔, 균형 또는 베이스 안정성 제약 아래에서.

**전신 QP를 풀어 쓰면.** $q$를 일반화 좌표(부유 베이스와 관절)라 하면 결정 변수는 가속도 $\ddot q$, 관절 토크 $\tau$, 접촉력 $f$다.

$$\min_{\ddot q,\,\tau,\,f}\ \sum_i w_i\,\lVert J_i\ddot q+\dot J_i\dot q-\ddot x_i^{\text{des}}\rVert^2\quad\text{s.t.}\quad M\ddot q+h=S_a^\top\tau+J_c^\top f,\ \ f\in FC,\ \ \tau_{\min}\le\tau\le\tau_{\max}$$

과제 $i$마다 야코비안 $J_i$, 원하는 가속도 $\ddot x_i^{\text{des}}$(보통 그 과제 오차에 대한 PD 법칙), 가중치 $w_i$가 있다. $M$은 질량 행렬, $h$는 코리올리·중력 항을 모은 것이다. 부유 베이스에는 모터가 없으므로 $S_a$가 구동 관절만 고른다. $J_c$는 접촉 야코비안, $FC$는 [[04-robotics/contact-force-tactile|접촉·힘·촉각 §2]]의 마찰 원뿔이다. 현재 상태 $q,\dot q$에서 동역학은 $(\ddot q,\tau,f)$에 선형이고 비용은 이차이므로, 원뿔을 [[04-robotics/contact-force-tactile|접촉·힘·촉각 §2]]의 다면 원뿔로 바꾸면 매 제어 스텝 다시 푸는 볼록 QP가 된다. 어느 다면 원뿔인지는 푸는 속도뿐 아니라 답에도 영향을 준다. 외접 상자 피라미드는 QP가 미끄러질 접촉력을 허가하게 만들고, 내접 생성자 원뿔은 접촉이 버텼을 힘을 거절하게 만든다. 그 절에 두 형태의 식과 각 오차의 크기가 있다.

**이 QP가 "whole-body control"이 가리키는 것이다.** 이 분야가 그리로 옮겨간 이유는 우아함이
아니다: 엄격한 영공간 우선순위는 *부등식* 제약을 표현할 수 없는데, 관절 한계도 토크 포화도
접촉 마찰도 전부 부등식이다. 그것들을 동시에 지켜야 하는 휴머노이드나 모바일 매니퓰레이터는
QP를 풀고 있고, 우선순위 계층은 그 안에서 제약 가중치나 QP의 종속 연쇄로 살아남는다.

모바일 매니퓰레이션의 경우 — "팔"에 주행 가능한 베이스가 포함될 때 — 같은 QP가 베이스와 팔의
자유도를 하나의 문제로 흡수하고, 그것이 [[04-robotics/navigation-mobile-manipulation|16. §3]]의
베이스 배치 선택의 형식적 판본이다.

### 5. 접촉 천이 — 이론이 값을 하는 지점

정상 접촉은 쉬운 부분이다. 어려운 것은 로봇이 도착하는 그 순간이고, 여기서의 논증은 수사가
아니라 정량적이다.

무감쇠 1축 선형 충돌, 일정한 겉보기 질량, 선형 스프링, 완전한 에너지 저장·반환을 가정하자. 말단의 겉보기 질량 $\Lambda$가 접근 속도 $v$로 강성 $K$를 만나면 접촉은 반주기 사인이고

$$F_{\max} = v\sqrt{\Lambda K}, \qquad t_{\text{contact}} = \pi\sqrt{\Lambda/K}$$

둘 다 이 모델에서 한 단계씩이면 나오고, 유도해 볼 값어치가 있다. 답의 *모양*이 곧 교훈이기
때문이다. 최대 압축에서 운동에너지가 전부 스프링으로 간다:
$\tfrac12 \Lambda v^2 = \tfrac12 K \Delta x^2$이므로 $\Delta x = v\sqrt{\Lambda/K}$이고
최대 힘은 $F_{\max} = K\Delta x = v\sqrt{\Lambda K}$다. 지속 시간은 같은 질량–스프링
진동자의 반주기다. $\omega = \sqrt{K/\Lambda}$이므로 $T/2 = \pi\sqrt{\Lambda/K}$.

두 제곱근을 서로 견주어 읽어라. 최대 힘은 $\sqrt{K}$에 비례하고 지속 시간은 $1/\sqrt{K}$에
비례하므로, **접촉면을 백 배 단단하게 만들면 힘은 열 배가 되고 접촉 시간은 십분의 일이 된다** —
이 모델에서는 역적이 보존되고 모양만 바뀐다. 기계적 유연성은 두 숫자를 직접 움직이고, 충돌 전 제어가 가장 직접적으로 줄일 수 있는 값은 $v$다. 실제 충돌에서는 힘-시간 파형과 식별한 등가 $\Lambda,K,D$를 확인해야 한다.

[[02-foundations/manipulator-kinematics-dynamics|10. §6]]의 $\Lambda = 2$ kg와 부드러운
접근 $v = 5$ cm/s를 넣자. 그 $\Lambda$는 맨 팔의 것이다. 기어 달린 구동계는 회전자의 반사 관성을 거기에 더하고, [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §4]]의 고정 구동계를 감속비 100으로 달면 같은 $10^5\,\mathrm{N/m}$ 착지의 정점이 $22.4$가 아니라 $29.5\,\mathrm{N}$이 된다.

| 접촉면 | $K$ (N/m) | $F_{\max}$ | 접촉 지속 | 접촉 중 1 kHz 샘플 수 |
|---|---:|---:|---:|---:|
| 맨 공구가 실제 팔에 — §1이 말한, 제어기가 식별하는 직렬 강성 | $10^5$ | **22 N** | **14 ms** | 약 14개 |
| 유연 손목을 직렬로 | $10^4$ | **7.1 N** | **44 ms** | 약 44개 |
| 재료 접촉만, 팔 구조를 뺀 경우 — §1의 넷째 줄 | $10^7$ | **224 N** | **1.4 ms** | 약 1개 |

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="이상화한 재료만의 접촉이 제어 샘플 하나 폭의 바늘 같은 스파이크로, 유연한 접촉이 넓고 평평한 봉우리로 실제 비례로 그려져 있다">
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
    <text x="20" y="218">두 축 모두 실제 비례다. 이상화한 재료만의 접촉(표의 마지막 줄)이 왼쪽의 바늘이다:</text>
    <text x="20" y="234">폭 1.4 ms라 1 kHz 루프는 그 안에서 샘플을 약 하나 얻는다. 유연한 접촉은 넓은 봉우리다: 같은 힘 축에서는</text>
    <text x="20" y="250">거의 보이지 않고, 샘플이 약 44개 들어올 만큼 길다.</text>
  </g>
</svg>

그림보다 표를 읽되, 마지막 줄은 §1에 비추어 읽어라. 팔의 구조가 재료와 직렬로 놓이고 더 무른
쪽이 이긴다. $10^5$과 $10^7$을 직렬로 두면 $9.9\times10^4$이다. 그래서 맨 공구가 실제 팔에
닿을 때 접촉 안에 들어오는 샘플은 하나가 아니라 **열넷** 정도다. 조절할 수는 있지만 아슬아슬하고,
정점 힘은 유연 손목의 세 배다. 맨 아래 줄은 강체 지그 위의 맨 압자로나 근접할 이상화다. 거기서는
1 kHz 제어기가 **샘플 하나** 정도를 보고 그마저 최대 1 ms 늦게, 정점이 지나간 뒤에 도착할 수
있으며, 어떤 제어 법칙도 그것을 고치지 못한다. 정보가 사건 뒤에 오기 때문이다. 그림이 그린 것은
그 두 극단이지 가운데 줄이 아니다.

유연 요소를 직렬로 넣으면 두 숫자가 반대 방향으로, 같은 배수만큼 움직인다:
$F_{\max} \propto \sqrt{K}$이고 $t_{\text{contact}} \propto 1/\sqrt{K}$이므로 구조 강성 $10^5$에서
$10^4$으로 무르게 하면 각각 $\sqrt{10} \approx 3.2\times$를, 맨 아래 줄의 이상화에 대해서는
$\sqrt{1000} \approx 32\times$를 산다. 힘은 팔이 견딜 만한 것이 되고, *동시에*
사건이 조절할 수 있을 만큼 길어진다. 같은 접근을 P2 위에서 끝까지, 곧 접촉 전에 임피던스로 전환하고 컴플라이언트하게 장착된 패널을 누르며 $K_d$와 접근 속도를 스윕하면서 돌린 것이 [[04-robotics/capstone-panel-contact|26. 캡스톤]]이다.

교훈은 산수 너머로 일반화된다: **수동 컴플라이언스는 능동 제어의 값싼 대체품이 아니라, 접촉
대역폭에서 작동하는 유일한 것이다.** Whitney의 1982년 준정적 분석이 이 발상의 성숙한 판본이다 —
챔퍼가 있는 경우와 없는 경우의 peg-in-hole에 대해, 정렬 오차가 언제 wedging이나 jamming을
일으키는지의 조건을 유도하고, 그것을 지지부 컴플라이언스가 만족해야 할 설계 부등식으로 바꾼다.

**Wedging과 jamming은 같은 실패가 아니다.** 둘 다 부재가 중간까지만 들어가고 멈춘 상태로 끝나지만
처방이 정반대라, 어느 쪽인지 밝히지 않고 "삽입이 실패했다"고 적은 논문은 아무것도 보고하지 않은 것이다.

- **Wedging**은 *기하학적* 잠김이다. 부재가 구멍의 두 벽에 법선이 서로 맞서는 두 점에서 닿고, 그러면
  두 접촉력이 축 방향으로 아무리 밀어도 서로를 상쇄한다. 정의 조건은 둘이다. 법선이 맞서는 2점
  접촉이고, 부재가 아직 기울어 있는 동안 그 접촉이 만들어진다는 것 — 그래서 너무 큰 각도로 너무 일찍
  넣으면 들어가고, 한번 걸리면 **더 세게 밀어도 소용이 없다**. 추가로 미는 힘이 두 접촉력을 함께
  올리기 때문이다. 처방은 기하다. 챔퍼, 더 작은 초기 각도, 또는 두 번째 접촉이 생기기 전에 부재를
  바로 세워 주는 컴플라이언스.
- **Jamming**은 *렌치* 조건이다. 접촉 자체는 지극히 평범한데, 가해진 힘과 모멘트의 조합이 삽입을
  만드는 렌치 원뿔 밖으로 벗어나서 접촉의 마찰이 그것을 전부 흡수하고 부재가 멈춘다. 그래서 정의
  조건은 기하가 아니라 가해진 렌치와 마찰 원뿔에 관한 진술이고([[04-robotics/contact-force-tactile|접촉·힘·촉각 §2]]), 처방은 가해진 렌치를
  바꾸는 것이다. 횡력을 줄이고, 모멘트를 줄이고, 축 방향으로 더 민다. 반례: 구멍이 작아서 멈춘
  부재는 둘 중 어느 것도 아니다. 그것은 간섭이고, 어떤 원뿔 안의 렌치로도 들어가지 않는다.

실용적 차이는 이것이다. **Jamming은 올바른 렌치를 공급하는 것이면 무엇이든 고치고, 올바른 자리에
놓인 컴플라이언스는 그것을 자동으로 공급한다.**

**Remote-centre compliance의 정의.** **RCC**는 손목과 공구 사이에 놓는 *수동 기계 요소*이고, 그
**컴플라이언스 중심** — 가해진 힘이 회전 없는 병진만 만들고 가해진 모멘트가 병진 없는 회전만 만드는
단 하나의 점 — 을 *부재의 끝점*에 두는 장치다. 그 배치 조건 하나가 장치의 전부다. 이것이 두 오차를
분리한다. 횡방향 오차는 횡방향 운동을, 각도 오차는 끝점 둘레의 회전을 만들고, 두 오차가 서로를
만들어 내며 부재를 위의 wedging 기하로 몰고 가지 않는다. 센서도 루프도 없으므로 재료의 속도로
작동한다. **반례**: 손목에 넣은 무른 스프링은 유연하지만 컴플라이언스 중심이 *손목*에 있어서 횡력이
부재를 회전까지 시킨다. RCC 없는 컴플라이언스이고, 결합을 줄이는 것이 아니라 키운다.
알루미늄으로, 센서 없이, 지연 없이 삽입 문제를 푼다.

이 모두는 천이가 일어났다는 것을 안다고 전제한다. 그것을 알아내는 일은 별개의 추정 문제이고, 모드
집합과 실패 사례까지 정의한 곳은 [[04-robotics/contact-force-tactile|접촉·힘·촉각 §7]]이다. 여기의 논증은 그 추정이 울린 다음 샘플에서 시작한다.

Colgate와 Hogan의 1988년 결과가 능동적 대안의 이론적 경계다: 선형 시불변 시스템에서, 매니퓰레이터가
*모든* 수동적 환경과 결합해도 안정한 것은 구동점 임피던스가 수동적일 때
그리고 오직 그때뿐이다. 여기서 수동적 시스템은 에너지를 저장했다 돌려줄 수는 있어도 새로 만들어 내지는 못한다. 구동점 임피던스는 환경이 접촉점에서 로봇을 밀 때 보게 되는 힘과 속도의 관계다. 접촉 안정성을 실험마다의 튜닝 문제에서 주파수 영역의 판정으로
바꾸고, 불편한 것을 하나 말해 준다 — 비동위치(non-collocated) 동역학이나 모델링되지 않은 동역학이 있으면 제어기가 겉보기 관성을
줄일 수 있는 데에는 **한계가 있다.** 구현 가능한 강성의 상한은 이와 별개로 샘플링·지연·양자화가 정한다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]). 제어기가 팔의 질량을 없는 척할 수는 없다.

**수동성과 구동점 임피던스를 식으로.** 접촉점을 **포트**로 본다. 환경이 거기서 로봇에 힘 $F(t)$를 가하고 로봇은 같은 점에서 속도 $v(t)$로 움직이므로, $F\,v$가 로봇으로 흘러드는 파워다. 시스템이 처음에 지녔던 것보다 많은 에너지를 포트로 되돌려 줄 수 없을 때 **수동적**이라 한다. 초기 저장 에너지를 $E_0\ge0$라 하면

$$\int_0^t F(\tau)\,v(\tau)\,d\tau\ \ge\ -E_0\quad\text{for every } t \text{ and every input}$$

(모든 시각 $t$와 모든 입력에 대해) 곧 흘러든 순 에너지가 저장량의 음수 아래로 내려가지 않는다(저장 함수 형태는 [[04-robotics/control-theory-ce397|제어 이론 §4]]). **구동점 임피던스**는 그 한 점에서 속도에서 힘으로 가는 전달함수 $Z(s)=F(s)/V(s)$이고, "구동점"은 힘과 속도를 같은 곳에서 잰다는 뜻이다. 선형 시불변 시스템에서 수동성은 $Z(s)$가 **양의 실수 함수**(positive real)인 것과 같고, 조건은 둘이다. $Z$가 열린 오른쪽 반평면에 극점이 없고(허수축 위의 극점은 단순하고 유수가 양수), 그리고

$$\mathrm{Re}\,Z(j\omega)\ge0\quad\text{for all }\omega$$

이다. 진폭 $V_0$, 주파수 $\omega$의 정현 속도가 포트에 평균 파워 $\tfrac12V_0^2\,\mathrm{Re}\,Z(j\omega)$를 흡수시키기 때문이다. 그러면 Colgate–Hogan 정리는 이렇게 읽힌다: 로봇은 $Z$가 양의 실수 함수일 때 그리고 오직 그때만 모든 수동적 환경에 대해 안정하다.

> [!example] 계산 예제 · Worked example
> §2의 이상적 목표 $Z(s)=M_ds+D_d+K_d/s$에서 $M_dj\omega$와 $K_d/(j\omega)$는 순허수이므로 모든 주파수에서 $\mathrm{Re}\,Z(j\omega)=D_d$다. 정확히 $D_d\ge0$일 때 수동적이다($M_d=2$, $D_d=20$, $K_d=500$이면 모든 $\omega$에서 $20$ N·s/m).
> **반례**: 같은 스프링을 1 ms 지연으로 구현하면 $Z(s)=K_de^{-sT}/s$이고 $\mathrm{Re}\,Z(j\omega)=-K_d\sin(\omega T)/\omega$다. $K_d=1000$ N/m, $T=0.001$ s, $\omega=100$ rad/s이면 $-0.998$ N·s/m다. 지연된 스프링이 접촉에 에너지를 퍼 넣고, 충분한 물리적 감쇠만이 그것을 갚을 수 있다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]).

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
  공간과 접촉이 많은 과제에서 정면 비교한다. 중요한 발견은 이것이다: 학습 설정을 고정한 채 **행동 공간**만 바꿔도
  최종 점수만이 아니라 표본 효율, 에너지 사용, 안전성, 전이가 함께 바뀌었다.
- **Bogdanovic, Khadiv & Righetti, RA-L 2020** — *Learning Variable Impedance Control for
  Contact Sensitive Tasks*. 같은 질문을 **관절 공간**에서 던진다: 정책이 목표 위치 *와* 임피던스
  이득을 함께 낸다. 기여는 강건성 축이다 — 접촉 불확실성을 의도적으로 변화시켜 토크 제어와 위치
  제어가 각각 어디서 무너지는지를 보이고, 학습된 가변 임피던스 행동 공간은 완만하게 나빠진다.

§2에 비추어 읽어라. 행동 공간은 학습 층이 임피던스–어드미턴스 인과 구조의 어디에 놓이는지를
정하는 요소다. 위치를 내는 정책의 실제 컴플라이언스는 하위 제어기의 게인·힘 피드백과 하드웨어에
달려 있으므로 위치 명령만으로 뻣뻣하다고 판정할 수 없다. 토크 정책은 더 직접적인 권한을 갖지만
안정화 거동을 배우거나 별도 내부 루프로 둘러싸야 한다. 임피던스 파라미터를 내는 정책은 고전
제어기에 원하는 관계를 고속으로 구현하도록 요청한다. 셋은 단일한 soft-to-stiff 축의 보편적 세
점이 아니라 서로 다른 아키텍처 선택이다.

> [!tip] 시연 수집이 기여인 논문에 이것이 왜 중요한가
> 기여가 힘을 담은 시연 데이터라면 행동 공간 질문이 두 번 온다. 수집 중에 *원격조작자*가 무엇을
> 명령하는가에서 한 번, 배치 시에 *정책*이 무엇을 내는가에서 한 번. 둘이 같을 필요는 없고, 그
> 불일치는 대부분의 논문이 암묵에 두는 설계 결정이다.

#### 수렴, 그리고 그것이 자리 잡아 가는 인터페이스

최근 여러 시스템은 한 방향을 보여 주지만 아직 합의나 일방향 수렴은 아니다. **VLA를 고전적
고속 내부 루프를 매개변수화하는 느린 의미 층으로 쓰는 설계가 늘고 있다.** 다음 사례는 이 선택이
유용할 수 있음을 보이지만 모든 접촉 시스템의 유일한 인터페이스를 확정하지는 않는다.

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
접촉이 많은 과제에 VLA를 배치하는 일부 그룹이 임피던스·어드미턴스·수동성 계층을 유용하게
사용하고 있다는 것이다. 모든 시스템에 같은 인터페이스가 필요하다는 근거는 아니다.

> [!note] 기록해 둘 예측
> 그 합류가 완성된다면 **인터페이스는 위치가 아니라 컴플라이언스 파라미터일 것이다.**
> 그것이 지켜볼 지점이고, 기여가 접촉이 많은 조작인 연구 프로그램에서 이 페이지가 Mastery에 있는
> 이유다.

### 7. 논문에서 힘 제어 읽기

| 질문 | 틀린 답이 감추는 것 |
|---|---|
| 임피던스인가 어드미턴스인가? 내부 루프는 무엇인가? | 구현한 컴플라이언스와 시험한 강성·대역폭 범위를 확인한다 |
| **단단한** 환경에서 검증했는가? | 폼과 자유 공간은 불안정을 통째로 감춘다 |
| $M_d, D_d, K_d$를 단위와 함께 보고했는가? | 숫자 없는 "유연함"은 명세가 아니다 |
| 접촉 **천이**를 보였는가, 정상 접촉만인가? | §5에 따르면 어려움은 천이에 산다 |
| 제어·센서 주기, 접촉 지속 시간, 그리고 **대역폭**(폐루프가 아직 기준을 따라가는 주파수 범위, [[04-robotics/control-theory-ce397\|5. 제어 이론 §5.5]])은? | 밀리초 충격 첨두는 피드백 전 역학이 지배할 수 있지만 지속 접촉은 훨씬 낮은 주기에서도 조절할 수 있다. 주장하는 현상의 시간척도와 비교한다 — 계산 예제가 그 비교를 비 하나로 해 둔다. |
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
- [ ] 강성·컴플라이언스·감쇠를 단위와 함께 말하고, 셋 중 직렬에서 더해지는 것이 무엇인지 말한다.
- [ ] 임피던스·어드미턴스가 명령을 만드는 방식과 단단한 접촉에서의 구현 한계를 설명한다.
- [ ] 하이브리드 제어의 선택 행렬 형태를 쓰고 적합한 과제를 하나 든다.
- [ ] 주어진 $\Lambda$, $K$, $v$에 대해 $F_{\max}$와 접촉 지속을 계산하고 제어 샘플이 몇 개 들어가는지 말한다.
- [ ] 접촉 지속 시간을 목표 임피던스의 한 주기와 비교하고, 그 비가 충격의 주인이 누구인지에 대해 무엇을 뜻하는지 말한다.
- [ ] Wedging과 jamming을 구분하고, RCC의 컴플라이언스 중심을 어디에 놓아야 하는지 말한다.
- [ ] Colgate와 Hogan의 수동성 조건이 무엇을 금지하는지 설명한다.

> [!tip] 더 깊이 · Going deeper
> Siciliano, Sciavicco, Villani, Oriolo의 *Robotics: Modelling, Planning and Control*(Springer, 2009) 9장이 §2~§4의 표준 교과서 판본이다 — 임피던스, 어드미턴스, 하이브리드 힘/위치, 작업공간 제어를 서술이 아니라 유도로 다룬다. Tedrake의 무료 [*Robotic Manipulation*](https://manipulation.csail.mit.edu/)은 같은 제어 발상을 현대 하드웨어에 실제로 올린 형태로 다루는데, 여기 논문들이 쓰인 방식에 더 가깝다. 둘 다 §6은 다루지 않는다. 학습된 정책이 이 제어기들에 대해 어디에 앉는지는 정리된 자료가 아니라 현재 진행 중인 질문이다.

### 스스로 점검

1. 손목 힘 센서를 단 산업용 팔이 폼에 대해서는 5 N을 훌륭하게 유지하는데 강판에 대해서는
   격렬하게 진동한다. 아키텍처와 원인을 대라.
2. 접근 속도가 5에서 10 cm/s로 두 배가 된다. 최대 접촉력과 접촉 지속 시간은 어떻게 되는가?
3. RCC 장치는 왜 센서 하나 없이 peg-in-hole 삽입을 푸는가?
4. 어떤 논문이 학습된 정책으로 "유연한 삽입"을 달성했다고 보고하는데, 정책은 위치 제어되는
   팔에 10 Hz로 말단 위치를 내보낸다. 이 논문이 실제로 뒷받침할 수 있는 가장 강한 주장은?
5. 하이브리드 위치/힘 제어는 기하를 알 때 정확하다. 왜 그것이 하필 건설에서 문제인가?
6. $10^5$과 $10^7$ N/m 두 요소가 직렬이다. 강성과 컴플라이언스 중 무엇을 더하고, 결과는 얼마이며,
   전체 물러남 중 더 무른 요소의 몫은 얼마인가?
7. 삽입이 중간에서 멈췄다. 더 세게 밀어도 달라지는 것이 없다. Wedging인가 jamming인가, 그리고
   그 답은 어떤 처방을 배제하는가?

> [!tip]- 정답 · Answers
> 1. 하드웨어와 증상만으로 구조를 확정할 수 없다. 힘 피드백이 위치 기준을 만든다면 어드미턴스 구현이다. 높은 접촉 강성은 지연과 부족한 감쇠의 영향을 키울 수 있다. 실제 루프·게인·시점을 확인한 뒤 원인을 판정한다. 폼에서 안정적이었다고 강철에서도 안정적이라는 뜻은 아니다.
> 2. $F_{\max} = v\sqrt{\Lambda K}$는 $v$에 선형이므로 모든 행에서 최대 힘이 두 배가 된다: 실제 팔의 맨 공구는 22 → 45 N, 이상화한 재료 접촉은 224 → 447 N. 지속 시간 $\pi\sqrt{\Lambda/K}$에는 $v$가 아예 없으므로 각각 14 ms와 1.4 ms 그대로다. 빨리 접근해도 반응 시간은 하나도 벌지 못하고 힘만 비례해서 치른다 — 더 나은 제어가 아니라 접근 속도 제한이 통상적인 처방인 이유다.
> 3. 컴플라이언스 중심을 peg의 끝점에 놓기 때문이다. 그러면 횡방향 정렬 오차는 횡방향 컴플라이언스를, 각도 오차는 끝점 둘레의 회전을 만들고, 각 오차가 다른 오차를 생성하지 않는다. 보정이 기계적이므로 제어 루프의 속도가 아니라 재료의 속도로 일어난다 — 그리고 §5는 어차피 제어 루프가 도와주기에는 너무 느렸음을 보여준다.
> 4. 최소한 정책이 유용한 위치 기준을 골랐다는 것. 시스템은 하위 임피던스·어드미턴스·힘 루프와 수동 하드웨어로 컴플라이언스를 만들 수도 있으므로 그 스택을 확인해야 한다. 10 Hz 외부 정책은 밀리초 충격 첨두 자체에 반응할 수 없지만 더 느린 지속 접촉을 위한 기준은 바꿀 수 있다. 측정된 힘 거동을 어느 층이 만들었는지에 따라 가장 강한 주장이 달라진다.
> 5. 아키텍처가 표면에 수직이라고 *믿는* 방향에 힘 제어를 배정하는데, 그 믿음이 모델에서 오기 때문이다. 건설 현장에서 부재는 도면이 말하는 곳이 아니라 놓인 곳에 있다: 몇 밀리미터의 위치 오차는 접촉을 이르게, 늦게, 혹은 엉뚱한 점에서 일으키고, 몇 도의 자세나 표면 형상 오차는 실제 법선을 돌려 힘 제어가 부분적으로 표면을 따라, 위치 제어가 부분적으로 표면 안으로 작용하게 만든다. 이것이야말로 그 아키텍처가 피하려고 설계된 바로 그 싸움이다. 지그로 고정된 공장 셀과 [[05-construction-robotics/assembly-fabrication|건설 조립]]의 차이가 이것이다.
> 6. 컴플라이언스를 더한다. $C_{eq}=10^{-5}+10^{-7}=1.010\times10^{-5}$ m/N이므로 $K_{eq}=9.90\times10^{4}$ N/m이고, 더 무른 요소가 물러남의 $99.0\%$를 담당한다. 직렬 값이 사실상 $10^5$ 위에 그대로 앉는 이유이자, 제어기가 재료가 아니라 구조를 식별하는 이유다.
> 7. Wedging이다. 기하학적 잠김, 곧 법선이 맞서는 2점 접촉이고, 축 방향으로 더 밀면 두 접촉력이 함께 올라가 아무것도 달라지지 않는다는 것이 바로 그 징후다. 그래서 "더 세게 밀기"가 배제되고, 가해진 렌치를 다시 겨누는 것 — 이쪽은 *jamming*의 처방이다 — 도 배제된다. 남는 것은 기하다. 챔퍼, 더 작은 진입 각도, 또는 두 번째 접촉이 생기기 전에 부재를 바로 세워 주는 컴플라이언스.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, 객체 카탈로그만 쓴다. 계속 쓰는 대상에서 **항목 셋을 바꾼다**. 누름이 서 있는 패널을 향해 옆으로 가서 $F=(-8,0)\,\mathrm{N}$이 되므로 축이 $x$가 되고 겉보기 질량은 $\Lambda_x=1\,\mathrm{kg}$이다($M_d$도 다시 이 값으로 둔다). 목표 강성은 $\zeta=0.7$에서 $K_d=2000\,\mathrm{N/m}$이다. 접근 속도는 $v=0.10\,\mathrm{m/s}$로 두 배가 된다. P2는 $\theta=(0^\circ,90^\circ)$ 그대로, $K_e$도 $10^5\,\mathrm{N/m}$ 그대로다([[02-foundations/lab-plants|0.6]]). 오일러 루프는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]에 있다. 여기서 시뮬레이터를 하나 더 만들지 마라.

1. **그리기.** 과제 그림의 세 패널을 새 축에서 다시 그린다. 패널이 이제 $x=1\,\mathrm{m}$에 서 있는 팔([[04-robotics/contact-force-tactile|9. 접촉·힘·촉각]]의 계속 쓰는 대상과 같은 패널이다), $x$에 대해 다시 쓴 블록선도 둘, 그리고 새 충격 폭과 새 목표 주기를 같은 축척으로 놓은 시계.
2. **유도.** (a) $F=(-8,0)$의 $\tau=J^\top F$, 그리고 수직 누름과 무엇이 다르며 왜 그런지. (b) $8\,\mathrm{N}$ 반력에서의 정적 처짐. (c) $\omega_n$, 임계 감쇠 $D_d$, 그리고 $\zeta=0.7$의 $D_d$. (d) $v=0.10\,\mathrm{m/s}$로 $K_e=10^5\,\mathrm{N/m}$에 부딪힐 때의 $F_{\max}$와 $t_{\text{contact}}$, 그리고 그 안에 들어가는 1 kHz 샘플 수. (e) 목표 한 주기 대 접촉 지속 시간의 비.
3. **해석.** 겉보기 질량이 *절반*으로 줄었는데 최대 힘은 계산 예제의 $22.4$에서 $31.6\,\mathrm{N}$으로 올랐다. 그 배수를 정확히 설명하라. 그다음: 주기 대 접촉 비가 $28.3$에서 $14.1$로 떨어졌는데, 목표를 단단하게 만든 것이 충격에 대한 권한을 조금이라도 사 주었는가? 그 답이 "그렇다"가 되려면 $K_d$가 얼마여야 하는가?

> [!tip]- 정답 · Solutions
> 1. 같은 팔, 같은 자세. 패널은 이제 $x=1\,\mathrm{m}$의 수직 패널이고, 누름 화살표는 $-x$를 가리키며, 직렬 스프링 둘은 $x$를 따라 읽는다. 시계에는 $9.93\,\mathrm{ms}$ 충격과 $140\,\mathrm{ms}$ 주기가 나온다.
> 2. (a) $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$이고 $\tau=(8,8)\,\mathrm{N{\cdot}m}$. 수직 누름은 어깨만 실었는데 이제 **두 관절이 모두** 하중을 진다. 이 자세에서 엘보의 운동은 말단을 순수하게 $x$로 옮기므로 $x$ 힘은 거기에 일을 하고 $y$ 힘은 하지 않는다. (b) $e=8/2000=0.004\,\mathrm{m}$, 곧 $4\,\mathrm{mm}$. (c) $\omega_n=\sqrt{2000/1}=44.72\,\mathrm{rad/s}$, $D_d\big|_{\zeta=1}=2\sqrt{2000\cdot1}=89.4\,\mathrm{N{\cdot}s/m}$, $D_d\big|_{\zeta=0.7}=62.6\,\mathrm{N{\cdot}s/m}$. (d) $F_{\max}=0.10\sqrt{1\times10^{5}}=31.6\,\mathrm{N}$, $t_{\text{contact}}=\pi\sqrt{1/10^{5}}=9.93\,\mathrm{ms}$이므로 1 kHz에서 약 $10$개 — 수직 경우보다 네 개 적다. (e) $T=2\pi/44.72=0.1405\,\mathrm{s}$이므로 $T/t_{\text{contact}}=0.1405/0.00993=14.1$.
> 3. 배수는 $\sqrt{\Lambda_x/\Lambda_y}\times(v'/v)=\sqrt{1/2}\times2=1.414$이고 $22.36\times1.414=31.6\,\mathrm{N}$이다. 겉보기 질량을 절반으로 줄여 최대 힘의 $\sqrt{1/2}=0.707$을 벌었는데 접근 속도를 두 배로 해서 $2$를 썼다. $F_{\max}$에서 속도는 선형이고 질량은 제곱근일 뿐이라 속도 쪽이 이긴다. 일반 교훈이 그것이다. 충격력을 줄이는 것은 더 가벼운 자세가 아니라 접근 속도 제한이다. 그리고 목표를 단단하게 만든 것은 충격에 대해 아무것도 사 주지 않았다. 비가 $28.3$에서 $14.1$로 내려간 것은 $\omega_n$이 올랐기 때문일 뿐이고, $14.1$도 여전히 한 주기의 14분의 1 안에서 시작하고 끝나는 충격이다. 둘을 맞추려면 $K_d=4K_e=4\times10^{5}\,\mathrm{N/m}$이 필요하고, 이는 여기서 요구한 $2000$의 200배이며 1 kHz 루프가 단단한 표면에 구현하는 범위를 한참 넘는다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]). 충격은 여전히 역학의 것이다.

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
