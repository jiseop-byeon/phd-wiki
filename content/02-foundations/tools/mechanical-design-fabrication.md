---
title: "12.9 Mechanical Design and Fabrication for Experiments"
tags: [foundations, tools, fabrication]
study-depth: Working
wiki-support: Working
depth-goal: "On the camera bracket B-60 and the pin fixture F-50, fully constrain a sketch, say what a STEP and an STL file keep, compute a fit from ISO 286 deviations, choose a print orientation, a hole allowance and a fastener, size a sensor bracket by its tilt at the target and its natural frequency, and locate a part 3-2-1 with its worst-case locating error."
mastery-when: "Raise when the dissertation's evidence rests on hardware you build: a fixture whose repeatability bounds a measured error, or a sensor mount whose stiffness enters a calibration."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]] (**P2**: its unit links, its catalog pose and the tip's apparent mass $\Lambda=\mathrm{diag}(1,2)$ kg), [[02-foundations/engineering-math|0.5 Engineering Math §8]] (a mass on a spring: $\omega_n=\sqrt{k/m}$ and the damping ratio $\zeta$) and [[02-foundations/signal-processing|6. Signal Processing §2]] (sampling and aliasing). The beam theory and statics of a civil-engineering degree — cantilever deflection, second moment of area, bending stress — are used and not re-derived. The construction track's S1 pin and hole are borrowed as numbers, not as a prerequisite.
> [[02-foundations/lab-plants|0.6 Lab Plants]](**P2**: 단위 링크, 카탈로그 자세, 말단의 겉보기 질량 $\Lambda=\mathrm{diag}(1,2)$ kg), [[02-foundations/engineering-math|0.5 공학수학 §8]](스프링에 매단 질량: $\omega_n=\sqrt{k/m}$와 감쇠비 $\zeta$), [[02-foundations/signal-processing|6. 신호처리 §2]](샘플링과 앨리어싱). 토목공학 학위의 보 이론과 정역학 — 캔틸레버 처짐, 단면 2차 모멘트, 휨응력 — 은 다시 유도하지 않고 쓴다. 건설 트랙 S1의 핀과 구멍은 숫자로 빌려 올 뿐 선수 지식이 아니다.

## English

*Stands on [[02-foundations/lab-plants|0.6 Lab Plants]] for **P2**, and on the beam theory and statics of a civil-engineering degree, which it uses rather than teaches. Here P2 is a machine to build on, not to model: a camera bracket for its tool, and a fixture that holds a mock-up of the construction track's locating pin in the same place every trial.*

> [!note] Why this matters · 왜 배우는가
> This page is part of the floor beneath the physical-AI stack of [[07-research-program/index|research program §5]] — the tools, here the hardware an experiment stands on (its place is marked on the [[physical-ai-map|Physical AI Map]]). In that section's worked instance, "Install that panel on the frame", it serves the steps that identify the frame and perform the fitting: the camera bracket decides where the robot believes the pin is, and the fixture decides where the pin actually is, trial after trial. Get either wrong and the experiment measures the rig instead of the robot: B-60 printed 6 mm thick puts the seen pin $0.654$ mm off, more than S1's whole $0.5$ mm tool allocation, and a pin block held by its screws alone lands up to $0.300$ mm apart from one trial to the next. To test S1 on the laboratory rung of [[05-construction-robotics/site-engineering|2.5 §5]]'s ladder, [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] and [[05-construction-robotics/imitating-contact|10. Imitating Contact]] need exactly this rig — a camera fixed to the tool and a pin that returns to the same place every trial — while [[04-robotics/geometric-perception-calibration|3.5 §5]] calibrates the camera the bracket holds and [[06-research-practice/experimental-design-reproducibility|research practice 2 §7]] asks every run for its hardware revision; the page sits outside the seven blocks of the dissertation path ([[07-research-program/index|research program §8]]), so take it when the experiment needs its rig, at the latest before the first mock-up trial of block 6 or 7. After it you can size a sensor bracket by its tilt at the target and its ringing, print it the right way up with holes that fit, and build a fixture that puts the part back within 14 µm every trial.

> [!note] First pass · 처음이라면
> Two sessions of about 90 minutes. **Session 1 — the bracket.** The Running object and the picture — two parts, and the three bars that matter, $0.654$, $0.276$ and $0.014$ mm — then §6 and the Worked case's steps 1, 2 and 4 with a calculator: why 65 µm of sag becomes $0.654$ mm at the pin, and why the camera sees the ringing at 5 Hz. End with Self-check 1 and 4. **Session 2 — the fixture.** §3 and §7, then step 5: what a fit is, and why pins locate and screws do not. End with Self-check 3 and 5. After that: §4 and §5 with step 3 before your first print (orientation, the hole allowance, inserts; Self-check 2), §1–§2 when you open a CAD program, §8 the day you need a laser cutter, a machinist or a frame, and the problem set last. The *Deeper* callouts can wait for a second pass.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the planar 2R arm with unit links, standing in the vertical plane; at its catalog pose $\theta=(0^\circ,90^\circ)$ the forearm points straight up and the tip's apparent mass is $\Lambda=\mathrm{diag}(1,2)$ kg — gets two pieces of experiment hardware. No catalog entry is a part to be made, so this page freezes both; every number in the two tables is this page's own course number, not a measurement or a datasheet value.

**B-60, the camera bracket.** A printed PLA arm, clamped to P2's tool by two M3 screws, carries a monocular camera 60 mm out. The arm leaves the tool at right angles in P2's plane, and the camera looks along the tool at S1's pin during the approach. It is a second camera, not the stereo wrist rig of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]], whose mount that page treats as rigid.

| Symbol | Value | What it is |
|---|---:|---|
| $m$ | $0.10$ kg | the camera, lumped at the arm's end |
| $L$ | $60$ mm | clamp face to the camera's centre of mass |
| $b\times h$ | $20\times6$ mm | the arm's section; $h$ is the bending direction |
| $E_\parallel,\ E_\perp$ | $3.0$, $2.4$ GPa | printed PLA's modulus along its roads (the printed strands, §4), and across its layers |
| $\sigma_\parallel,\ \sigma_\perp$ | $50$, $12$ MPa | its tensile strength in the same two directions |
| $\zeta$ | $0.02$ | the bracket's damping ratio |
| $D_w$ | $0.40$ m | camera to the pin while the camera guides the approach |
| $f_s$ | $50$ Hz | the camera's frame rate, P6's vision rate |
| $e_{\max}$ | $0.5$ mm | what the bracket may cost at the pin: S1's whole tool allocation |

**F-50, the pin fixture.** A steel mock-up of S1's locating pin as [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] freezes it — 16 mm across, with a tapered nose that captures up to 4 mm of radial error — is pressed into an aluminium block $80\times40$ mm. The block sits on a base plate bolted to the bench, placed by the plate's top face and two locating pins 50 mm apart — one round, and one diamond, relieved on two sides so that it locates in one direction only (§7) — with S1's pin midway; two M6 screws hold it down.

| Symbol | Value | What it is |
|---|---:|---|
| $d,\ D$ | $16$, $18$ mm | S1's pin and hole; $1$ mm of radial clearance when centred (construction 9) |
| $r_c$ | $4$ mm | the radial error the pin's nose captures (construction 9) |
| locating pins | $\varnothing6$ mm, H7 holes on g6 pins (a sliding fit, §3) | one round, one diamond, $s=50$ mm apart |
| clamp screws | M6 in $6.6$ mm holes | two, pulling the block down onto the plate |
| pin in block | $\pm0.05$ mm | where machining puts S1's pin relative to the locating holes |

One more number belongs to the printer: it makes a vertical hole $0.2$ mm smaller than the model says. This bench mock-up — one pin, not a full-size panel — stands on the laboratory rung of [[05-construction-robotics/site-engineering|2.5]]'s evidence ladder, which measures the arm, tool and part terms of S1's error budget; the fixture must keep its own error out of them.

*Scope: this page teaches what a researcher needs to get a working bracket or fixture on the first or second print — design intent in parametric CAD, the STEP and STL formats, fits, print orientation and hole allowances, fasteners and inserts, a stiffness check for a sensor mount, and 3-2-1 locating. It does not teach beam theory, finite-element analysis, full geometric tolerancing or machining as a trade. Calibrating the camera is [[04-robotics/geometric-perception-calibration|3.5 §5]]; describing the rig to ROS is [[04-robotics/ros2/describing-a-robot|25.6 §4]]; the trial protocol the fixture serves is [[06-research-practice/experimental-design-reproducibility|research practice 2]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="Three panels. (a) B-60, a printed arm 60 mm long and 6 mm thick clamped to P2's tool, carrying a 0.10 kg camera that looks along the tool at S1's pin 400 mm away; sag and tilt drawn 150 times enlarged: 65 micrometres of sag, 1.64 milliradians of tilt. (b) F-50 in plan: a pin block 80 by 40 mm on a base plate, located by the plate face, a round pin and a diamond pin 50 mm apart, and clamped by two M6 screws in 6.6 mm holes, with S1's 16 mm pin midway. (c) Error at the pin in millimetres: B-60 as frozen 0.654, printed upright 0.818, with an 8 mm arm 0.276; F-50 on its pins 0.014, on screws only 0.300; against the 0.5 mm allowance, a 0.1 mm radial precise fit and S1's 1.0 mm radial clearance.">
<text x="12" y="18" font-size="12" fill="currentColor" font-weight="600">(a) B-60 on P2&#8217;s tool (sag, tilt ×150)</text>
<rect x="20" y="34" width="32" height="96" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="146" font-size="10.5" fill="currentColor" text-anchor="middle">P2&#8217;s tool</text>
<line x1="26" y1="58.0" x2="52" y2="58.0" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="26" y1="70.0" x2="52" y2="70.0" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
<rect x="52.0" y="58.0" width="120.0" height="12.0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
<polyline points="52.0,64.0 56.0,64.0 60.0,64.1 64.0,64.3 68.0,64.5 72.0,64.8 76.0,65.1 80.0,65.5 84.0,65.9 88.0,66.4 92.0,66.9 96.0,67.5 100.0,68.1 104.0,68.7 108.0,69.4 112.0,70.1 116.0,70.9 120.0,71.7 124.0,72.5 128.0,73.3 132.0,74.2 136.0,75.1 140.0,76.0 144.0,76.9 148.0,77.8 152.0,78.8 156.0,79.7 160.0,80.7 164.0,81.7 168.0,82.6 172.0,83.6" fill="none" stroke="currentColor" stroke-width="12" stroke-opacity="0.35"/>
<polyline points="52.0,64.0 56.0,64.0 60.0,64.1 64.0,64.3 68.0,64.5 72.0,64.8 76.0,65.1 80.0,65.5 84.0,65.9 88.0,66.4 92.0,66.9 96.0,67.5 100.0,68.1 104.0,68.7 108.0,69.4 112.0,70.1 116.0,70.9 120.0,71.7 124.0,72.5 128.0,73.3 132.0,74.2 136.0,75.1 140.0,76.0 144.0,76.9 148.0,77.8 152.0,78.8 156.0,79.7 160.0,80.7 164.0,81.7 168.0,82.6 172.0,83.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
<g transform="rotate(14.05 172.0 83.6)"><rect x="160.0" y="89.6" width="24" height="18" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/></g>
<rect x="160.0" y="70.0" width="24" height="18" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" stroke-opacity="0.7"/>
<line x1="172.0" y1="88.0" x2="172.0" y2="196.0" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="166.2" y1="106.9" x2="143.9" y2="196.0" stroke="currentColor" stroke-width="1.3"/>
<line x1="143.9" y1="199.0" x2="172.0" y2="199.0" stroke="currentColor" stroke-width="1"/>
<line x1="143.9" y1="195.0" x2="143.9" y2="203.0" stroke="currentColor" stroke-width="1"/>
<line x1="172.0" y1="195.0" x2="172.0" y2="203.0" stroke="currentColor" stroke-width="1"/>
<text x="138.9" y="203.0" font-size="10.5" fill="currentColor" text-anchor="end">e = D_w θ = 0.654 mm</text>
<rect x="156.0" y="206.0" width="32" height="10" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
<text x="194.0" y="215.0" font-size="10.5" fill="currentColor">S1&#8217;s pin</text>
<text x="180.0" y="146" font-size="10.5" fill="currentColor">D_w = 400 mm</text>
<text x="180.0" y="160" font-size="10.5" fill="currentColor">(not to scale)</text>
<text x="112.0" y="52.0" font-size="10.5" fill="currentColor" text-anchor="middle">L = 60 mm, h = 6 mm</text>
<text x="190.0" y="86" font-size="10.5" fill="currentColor">δ = 65 µm</text>
<text x="190.0" y="100" font-size="10.5" fill="currentColor">θ = 1.64 mrad</text>
<text x="12" y="238" font-size="10.5" fill="currentColor">camera 0.10 kg, looking along the tool</text>
<text x="290" y="18" font-size="12" fill="currentColor" font-weight="600">(b) F-50 on its base plate, plan (1.6 px/mm)</text>
<rect x="308.0" y="40.0" width="224.0" height="144.0" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
<rect x="356.0" y="80.0" width="128.0" height="64.0" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.3"/>
<circle cx="420.0" cy="112.0" r="12.8" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="1.2"/>
<circle cx="380.0" cy="112.0" r="4.8" fill="currentColor" stroke="currentColor" stroke-width="1"/>
<circle cx="460.0" cy="112.0" r="4.8" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="1.5 1.5"/>
<path d="M460.0 107.2 L461.6 112.0 L460.0 116.8 L458.4 112.0 Z" fill="currentColor" stroke="currentColor" stroke-width="1"/>
<text x="380.0" y="103.0" font-size="10" fill="currentColor" text-anchor="middle">round</text>
<text x="460.0" y="103.0" font-size="10" fill="currentColor" text-anchor="middle">diamond</text>
<circle cx="400.8" cy="92.8" r="5.3" fill="none" stroke="currentColor" stroke-width="1"/>
<circle cx="400.8" cy="92.8" r="4.8" fill="none" stroke="currentColor" stroke-width="0.8"/>
<line x1="397.8" y1="92.8" x2="403.8" y2="92.8" stroke="currentColor" stroke-width="0.8"/><line x1="400.8" y1="89.8" x2="400.8" y2="95.8" stroke="currentColor" stroke-width="0.8"/>
<circle cx="439.2" cy="131.2" r="5.3" fill="none" stroke="currentColor" stroke-width="1"/>
<circle cx="439.2" cy="131.2" r="4.8" fill="none" stroke="currentColor" stroke-width="0.8"/>
<line x1="436.2" y1="131.2" x2="442.2" y2="131.2" stroke="currentColor" stroke-width="0.8"/><line x1="439.2" y1="128.2" x2="439.2" y2="134.2" stroke="currentColor" stroke-width="0.8"/>
<line x1="380.0" y1="156.8" x2="460.0" y2="156.8" stroke="currentColor" stroke-width="1"/>
<line x1="380.0" y1="152.8" x2="380.0" y2="160.8" stroke="currentColor" stroke-width="1"/><line x1="460.0" y1="152.8" x2="460.0" y2="160.8" stroke="currentColor" stroke-width="1"/>
<line x1="380.0" y1="118.8" x2="380.0" y2="152.8" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2 2"/><line x1="460.0" y1="118.8" x2="460.0" y2="152.8" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2 2"/>
<text x="420.0" y="170.8" font-size="10.5" fill="currentColor" text-anchor="middle">s = 50 mm</text>
<text x="420.0" y="74.0" font-size="10.5" fill="currentColor" text-anchor="middle">pin block 80 × 40 mm, S1&#8217;s Ø16 pin midway</text>
<text x="290" y="198.0" font-size="10.5" fill="currentColor">plate face 3 + round pin 2 + diamond pin 1 = 6</text>
<text x="290" y="212.0" font-size="10.5" fill="currentColor">M6 clamp screws in 6.6 holes locate nothing</text>
<text x="12" y="264.0" font-size="12" fill="currentColor" font-weight="600">(c) what each costs at the pin (mm)</text>
<text x="184.0" y="289.0" font-size="10.5" fill="currentColor" text-anchor="end">B-60, h 6 mm, flat</text>
<rect x="190.0" y="278.0" width="228.9" height="14" fill="currentColor" fill-opacity="0.55"/>
<text x="423.9" y="289.0" font-size="10.5" fill="currentColor">0.654</text>
<text x="184.0" y="312.0" font-size="10.5" fill="currentColor" text-anchor="end">B-60, h 6 mm, upright</text>
<rect x="190.0" y="301.0" width="286.1" height="14" fill="currentColor" fill-opacity="0.55"/>
<text x="481.1" y="312.0" font-size="10.5" fill="currentColor">0.818</text>
<text x="184.0" y="335.0" font-size="10.5" fill="currentColor" text-anchor="end">B-60, h 8 mm, flat</text>
<rect x="190.0" y="324.0" width="96.6" height="14" fill="currentColor" fill-opacity="0.55"/>
<text x="291.6" y="335.0" font-size="10.5" fill="currentColor">0.276</text>
<text x="184.0" y="358.0" font-size="10.5" fill="currentColor" text-anchor="end">F-50 on H7/g6 pins</text>
<rect x="190.0" y="347.0" width="4.8" height="14" fill="currentColor" fill-opacity="0.3"/>
<text x="199.8" y="358.0" font-size="10.5" fill="currentColor">0.014</text>
<text x="184.0" y="381.0" font-size="10.5" fill="currentColor" text-anchor="end">F-50 on screws only</text>
<rect x="190.0" y="370.0" width="105.0" height="14" fill="currentColor" fill-opacity="0.3"/>
<text x="300.0" y="381.0" font-size="10.5" fill="currentColor">0.300</text>
<line x1="190.0" y1="393.0" x2="540.0" y2="393.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
<line x1="190.0" y1="393.0" x2="190.0" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="190.0" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="277.5" y1="393.0" x2="277.5" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="277.5" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.25</text>
<line x1="365.0" y1="393.0" x2="365.0" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="365.0" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.5</text>
<line x1="452.5" y1="393.0" x2="452.5" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="452.5" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.75</text>
<line x1="540.0" y1="393.0" x2="540.0" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="540.0" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<line x1="365.0" y1="272.0" x2="365.0" y2="393.0" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
<line x1="225.0" y1="272.0" x2="225.0" y2="393.0" stroke="currentColor" stroke-width="1.1" stroke-dasharray="1.5 3"/>
<line x1="540.0" y1="272.0" x2="540.0" y2="393.0" stroke="currentColor" stroke-width="1.1" stroke-dasharray="1.5 3"/>
<text x="225.0" y="423.0" font-size="10.5" fill="currentColor" text-anchor="middle">precise fit 0.1</text>
<text x="540.0" y="423.0" font-size="10.5" fill="currentColor" text-anchor="end">S1 radial clearance 1.0</text>
<text x="365.0" y="437.0" font-size="10.5" fill="currentColor" text-anchor="middle">allowance 0.5 (S1&#8217;s tool term)</text>
</svg>

The rig's two parts and what each costs at S1's pin. The camera turns with the arm's end slope, so B-60's 65 µm of sag costs $0.654$ mm at the pin $0.40$ m away, over the $0.5$ mm allowance; an 8 mm arm brings it to $0.276$ mm, and printing the 6 mm arm standing on its end makes it $0.818$ mm. F-50's block, put back on its pins, moves at most $0.014$ mm; held by its screws alone it can move $0.300$ mm, almost a third of S1's $1$ mm radial clearance and three times a precise fit's $0.1$ mm.

### 1. Design intent and the parametric model

**The problem.** A part for an experiment is redesigned more often than it is made — after the first print the camera must sit 20 mm further out, or the holes are too small. If the part was drawn as fixed lines, every change is a redraw, and a redraw is where a hole ends up 20 mm from the tapped hole it was meant to meet.

**The idea.** Write the part as a recipe whose numbers have names, and measure every dimension from the thing it must fit. In a parametric CAD program a **sketch** is a 2D profile; **constraints** pin it down — geometric ones (horizontal, concentric) and dimensions (this length is `L`); **features** turn sketches into solid (extrude 6 mm, cut a hole) and are kept as an ordered history, so changing `L` replays the history with the new number. An **assembly** places parts with **mates**, which remove degrees of freedom as a locator does in §7: a concentric mate leaves a pin free only to slide along and turn about its axis, and a face-to-face mate stops the slide.

> **Parametric model, defined.** A **parametric model** is a *recipe for a solid*, not the solid: an ordered list of features whose sketches are fixed by constraints and whose dimensions are named parameters. Four defining conditions. The geometry is **regenerated from an ordered feature history**, each feature referencing geometry that exists before it. Every sketch is **fully constrained** — nothing in it can move without breaking a constraint — which the count below turns into a number. The dimensions that matter are **named parameters**, so a change is made once and reaches every feature that uses it. And each dimension is **measured from the feature that carries the function** — the face that mates, the hole that locates — which is what *design intent* means in practice.
>
> $$\mathrm{DOF}=\sum_i n_i-\sum_j r_j=0$$
>
> where $n_i$ counts the coordinates that fix sketch entity $i$ — 2 for a point, 4 for a line segment, since it has two endpoints, 3 for a circle — and $r_j$ the equations constraint $j$ imposes: 2 for making two points coincide, 1 for horizontal, vertical, tangent or equal, 1 per dimension, 2 for fixing a point to the origin. The sketch is fully constrained when the count reaches zero, so a sketcher's "degrees of freedom left" is this sum.
>
> - **Example**: B-60's outline from above, an $80\times20$ mm rectangle (20 mm clamped, 60 mm of arm). Four segments bring 16; four coincident corners remove 8, two horizontals and two verticals 4, length and width 2, a corner fixed at the origin 2: DOF $=0$. Each clamp hole adds a circle, 3, and removes 3 — its diameter, the expression `clearance_m3 + hole_allowance`, and two distances from the clamp end and one edge.
> - **Non-example**: the same holes dimensioned from the camera end. The count is still zero, but lengthening the arm to 80 mm now slides the clamp holes 20 mm off the tool's tapped holes. Zero is necessary; the references carry the intent.
> - **Why it matters**: rig hardware is revised between the pilot and the study, and a model that regenerates correctly from one changed number gets revised instead of patched with a drill.

**On B-60.** The clamp holes are dimensioned from the clamp end, because the tool's tapped holes are what they must meet; the camera's holes from the far end, where the camera sits; and the arm length $L$ is one parameter between them, so §6's question — how long may the arm be? — becomes one number. The printer's hole allowance (§4) is one more parameter, used by every printed hole.

**The trap: losing the recipe.** A STEP or STL exported from the model (§2) is a snapshot without its parameters. Keep the native file, the exports and a revision name — "B-60 r2: arm 8 mm" — with the experiment's code, in its repository ([[02-foundations/tools/git-research-code|12.2 Git for Research Code]]), since research practice's artifact checklist asks every run for its hardware revision ([[06-research-practice/experimental-design-reproducibility|2. §7]]). The same model also gives the mass, centre of mass and inertia tensor a URDF's `<inertial>` asks for ([[04-robotics/ros2/describing-a-robot|25.6 §4]]).

### 2. What leaves the CAD program: STEP, STL, and why a mesh is not a solid

**The problem.** The model has to leave the CAD program — for a printer, a machinist, a URDF — and each wants a different file; send the wrong one and the part comes back wrong in a way nobody notices until it does not fit.

**The idea.** One kind of file keeps the exact solid — a hole is a cylinder of radius 9 mm — for people who cut metal or edit geometry. The other keeps a skin of flat triangles — the hole is a polygon — for printers and viewers. **STEP** (ISO 10303; `.stp`, `.step`) is the exact kind: its solids are boundary representations bounded by exact planes, cylinders and B-spline surfaces (Open CASCADE), and NIST describes STEP files as carrying parts, assemblies and tolerances. **STL** is the triangle kind, the mesh format of 3D printing: only the surface, as triangles each with a normal and three vertices (Library of Congress), and no unit — Autodesk's documentation calls it unitless — so whatever reads it must assume one.

> **Tessellated mesh, defined.** A **tessellated mesh** is a *surface of flat triangles standing in for the exact boundary of a solid* — an approximation of the boundary, not a description of the solid. Three defining conditions. It is **faceted**: every curved face becomes flat triangles with their vertices on the true surface, so between vertices the mesh cuts inside a convex curve and, around a hole, into the hole. It is **closed and consistently oriented** only if every triangle shares whole edges with its neighbours and lists its vertices the same way round, which the format does not enforce (Deeper, below). And it is **dimensionless**: its numbers carry no unit.
>
> $$\Delta D=D\,\big(1-\cos(\pi/n)\big)$$
>
> where $\Delta D$ is how much smaller than its diameter $D$ a hole meshed with $n$ segments is across the flats of its polygon, since each vertex sits on the circle and each flat is a chord that cuts inside it.
>
> - **Example**: the mock-up's hole plate — a 40 mm disc, 6 mm thick, with S1's 18 mm hole — exported at 16, 32 and 64 segments per circle is 128, 256 and 512 triangles, and a hole $17.654$, $17.913$ and $17.978$ mm across its flats: at 16 segments, $\Delta D=18(1-\cos11.25^\circ)=0.346$ mm.
> - **Non-example**: the plate's STEP file. Its hole is a cylinder with no segment count at all; a machinist sent the 16-segment STL instead gets a hole $0.346$ mm small, and numbers with no unit to read them in.
> - **Why it matters**: a mesh is what a slicer prints and what a URDF draws, so its segment count adds to the printed-hole errors of §4, and its missing unit is why a part designed in inches or metres arrives 25.4 or 1,000 times too small in a program that assumes millimetres.

**The trap: the wrong file to the wrong reader.** A machine shop or another CAD program gets STEP, with a drawing for the fits and datums (§3, §7). A slicer gets STL, exported fine enough that $\Delta D$ is small beside the printer's own hole error — for the 18 mm hole to lose at most $0.02$ mm, $1-\cos(\pi/n)\le0.02/18$, so at least 67 segments. Version control gets the native file too. And a URDF's collision geometry never gets a fine CAD mesh ([[04-robotics/ros2/describing-a-robot|25.6 §4]]).

> [!note]- Deeper · 더 깊이
> **The formats in detail.** A STEP file is plain text in the exchange structure of ISO 10303's Part 21, and its application protocol sets what it may hold; AP242, published in 2014, combined and extended AP203 and AP214 and is the one to ask for when exporting CAD data (Library of Congress; STEP Tools). A binary STL — a binary record in the sense of [[02-foundations/tools/config-data-formats|12.4 Config and Data Formats §7]] — is an 80-byte header, the triangle count as a 32-bit little-endian integer, then per triangle twelve 32-bit floats — the unit normal and three vertices — and a two-byte attribute field that should be zero — $84+50N_\triangle$ bytes for $N_\triangle$ triangles, so the hole plate at 16, 32 and 64 segments is 6,484, 12,884 and 25,684 bytes. Its two rules: each triangle lists its vertices counterclockwise seen from outside (the right-hand rule), and shares a whole edge with each neighbour (the vertex-to-vertex rule) (Library of Congress). The listing builds the hole plate as a binary STL in memory, checks the byte count against $84+50N_\triangle$ and the two rules by counting directed edges, and computes the mesh's volume from its triangles — positive, so the normals point out.
>
> ```python
> import io, math, struct
> from collections import Counter
> import numpy as np
>
> def ring_plate(R, r, h, n):
>     """Triangles of a round plate of outer radius R and thickness h with a central hole of radius r,
>     tessellated with n segments per circle (vertices on the circles)."""
>     a = 2 * np.pi * np.arange(n) / n
>     o0 = np.stack([R * np.cos(a), R * np.sin(a), np.zeros(n)], 1); o1 = o0 + [0, 0, h]
>     i0 = np.stack([r * np.cos(a), r * np.sin(a), np.zeros(n)], 1); i1 = i0 + [0, 0, h]
>     tris = []
>     for k in range(n):
>         j = (k + 1) % n
>         tris += [(o0[k], o0[j], o1[j]), (o0[k], o1[j], o1[k])]      # outer wall, normals point out
>         tris += [(i0[k], i1[j], i0[j]), (i0[k], i1[k], i1[j])]      # hole wall, normals point into the hole
>         tris += [(o1[k], o1[j], i1[j]), (o1[k], i1[j], i1[k])]      # top face, normal +z
>         tris += [(o0[k], i0[j], o0[j]), (o0[k], i0[k], i0[j])]      # bottom face, normal -z
>     return np.array(tris)                                           # shape (triangles, 3 vertices, 3 coordinates)
>
> def binary_stl(tris):
>     """Binary STL: 80-byte header, uint32 count, then 50 bytes per triangle (12 float32 + uint16)."""
>     buf = io.BytesIO()
>     buf.write(b"mock-up hole plate".ljust(80, b" "))
>     buf.write(struct.pack("<I", len(tris)))
>     for v0, v1, v2 in tris:
>         nrm = np.cross(v1 - v0, v2 - v0); nrm = nrm / np.linalg.norm(nrm)
>         buf.write(struct.pack("<12fH", *nrm, *v0, *v1, *v2, 0))
>     return buf.getvalue()
>
> def closed_and_oriented(tris):
>     """Vertex-to-vertex rule with consistent winding: every directed edge appears once, and its reverse once."""
>     key = lambda p: tuple(np.round(p, 9))
>     edges = Counter((key(t[i]), key(t[(i + 1) % 3])) for t in tris for i in range(3))
>     return all(c == 1 and edges.get((b, a), 0) == 1 for (a, b), c in edges.items())
>
> R, r, h = 20.0, 9.0, 6.0                                            # mm: S1's 18 mm hole in a 40 mm plate, 6 mm thick
> exact = math.pi * (R**2 - r**2) * h
> for n in (16, 32, 64):
>     tris = ring_plate(R, r, h, n)
>     data = binary_stl(tris)
>     vol = np.einsum("ij,ij->i", tris[:, 0], np.cross(tris[:, 1], tris[:, 2])).sum() / 6
>     flats = 2 * r * math.cos(math.pi / n)                           # hole size across flats, the smallest a pin meets
>     print(f"n={n:3d}  triangles={len(tris):4d}  bytes={len(data):6d}  84+50N={84 + 50 * len(tris):6d}  "
>           f"closed={closed_and_oriented(tris)}  hole across flats={flats:.3f} mm  volume={vol:.1f} of {exact:.1f} mm^3")
> ```
>
> Its output as run for this page (macOS, Python 3.12, NumPy 2.0.2; the numbers do not depend on the machine):
>
> ```text
> n= 16  triangles= 128  bytes=  6484  84+50N=  6484  closed=True  hole across flats=17.654 mm  volume=5859.6 of 6013.0 mm^3
> n= 32  triangles= 256  bytes= 12884  84+50N= 12884  closed=True  hole across flats=17.913 mm  volume=5974.4 of 6013.0 mm^3
> n= 64  triangles= 512  bytes= 25684  84+50N= 25684  closed=True  hole across flats=17.978 mm  volume=6003.4 of 6013.0 mm^3
> ```
>
> The mesh holds less volume than the solid at every $n$, because the outer edge loses more to its chords than the hole gives back. An export dialog asks for a chord height or an angle rather than $n$, and either fixes it; at 67 segments the plate is 536 triangles, 26,884 bytes.

### 3. Tolerances and fits

**The problem.** A 6 mm pin and a 6 mm hole: will the pin slide in, stick, or rattle? The drawing says 6 and 6, and the answer is none of those until you know how far each part may be from 6.

**The idea.** No part is made to an exact size, so every dimension on a drawing is a range: a 6 mm hole reamed to H7 is anywhere from $6.000$ to $6.012$ mm, a 6 mm pin ground to g6 anywhere from $5.988$ to $5.996$ mm. How they go together is decided by the tightest pair — smallest hole, largest pin — and the loosest.

> **Fit, defined.** A **fit** is the *relation between a hole's tolerance zone and a shaft's*: the whole range of clearance the pair can have, not the gap of one pair on the bench. Three kinds, set by the two ends of that range. A **clearance fit** leaves a gap in every combination; an **interference fit** leaves overlap in every combination, so the shaft must be pressed in; a **transition fit** is everything between — a small gap or a small overlap, depending on which two parts meet.
>
> $$c_{\min}=D_{\min}-d_{\max},\qquad c_{\max}=D_{\max}-d_{\min}$$
>
> where $D$ is the hole's size and $d$ the shaft's, so the fit is clearance when $c_{\min}\ge0$ and $c_{\max}>0$, interference when $c_{\max}\le0$, and transition when $c_{\min}<0<c_{\max}$.
>
> - **Example**: F-50's round locating pin. ISO 286 gives a 6 mm H7 hole $+12/0$ µm and a g6 pin $-4/-12$ µm, so $c_{\min}=0-(-4)=4$ µm and $c_{\max}=12-(-12)=24$ µm: a clearance fit. The block lifts off and drops back by hand, and its hole's centre sits at most 12 µm from the pin's (§7).
> - **Non-example**: "a 16 mm pin in a 16 mm hole". Equal nominal sizes say nothing: at 16 mm, H7/g6 is a clearance fit of 6 to 35 µm and H7/p6 an interference fit of 0 to 29 µm. S1's pair is named by its clearance instead — 18 on 16, $\Delta=2$ mm, a bolt-clearance fit ([[05-construction-robotics/construction-manipulation|construction 9]]).
> - **Why it matters**: a fixture's repeatability is its locators' clearance range, and a pressed pin's grip is its seat's interference range; a design that assumes one measured gap is designed for the part that happened to be measured.

**Reading ISO 286.** The code for a tolerance zone is a letter and a number. The number is the grade — twenty of them, IT01 to IT18 (RoyMech) — and sets how wide the zone is for a size range: from 3 to 6 mm, IT7 is 12 µm and IT6 8 µm. The letter says where the zone sits against the nominal size, capital for holes and lower case for shafts; an H hole's lower limit is the nominal size itself, which is why most fits are built on H holes. The common ones read like a menu: H7/g6 sliding, H7/h6 locational clearance, H7/k6 location with slight interference, H7/p6 locational interference. At 6 mm, H7/k6 runs from 9 µm of interference to 11 µm of clearance, a transition fit. Read the numbers from the tables, never from memory: the zones change from one size range to the next.

**The trap: a printed hole is not a fit.** This page's printer makes a vertical hole $0.2$ mm under its model (§4) — $0.2/0.012=17$ times the whole H7 zone of a 6 mm hole — so no printed hole is an ISO fit as it comes off the printer. Where a printed part must sit on a pin, drill or ream the hole after printing, press in a metal bushing, or give up the fit and design a clearance, as S1's 2 mm does.

### 4. FDM printing: layers, orientation, holes and materials

**The problem.** First prints fail in three predictable ways: the part snaps along a layer line, a hole comes out too small for its screw, or the part is floppier than its outline suggests. All three come from how the part is built.

**The idea.** A fused-deposition (FDM) printer builds a part as a stack of layers, each drawn by a hot nozzle as plastic strands called **roads**: **perimeters** (walls) around every outline, **top and bottom skins** where the part has faces, and sparse **infill** inside; the **slicer** turns the mesh into these toolpaths. Each road welds to the layer below while both are hot, and the weld is weaker than the road: the part is strong along its layers and weak between them, like veneers glued face to face. Protolabs Network's design guide puts the in-plane tensile strength at typically four to five times that along the build axis Z; this page's 50 and 12 MPa sit in that range.

> **Print anisotropy, defined.** **Print anisotropy** is a *property of a printed part, not of its filament*: the part's stiffness and strength depend on the direction of the stress relative to its layers. Three defining conditions. The part is **built from roads within layers**, each layer bonded to the one below only by partial re-melting. The **interlayer bond is weaker than the road**, so a stress that pulls the layers apart breaks the part at a fraction of the stress it carries along the roads, and the stiffness across the layers is lower too. And the **direction is chosen at slicing**, by whoever prints the part: the same CAD file makes a different part lying flat than standing on end.
>
> $$u=\frac{\sigma}{\sigma_{\text{allow}}},\qquad \sigma=\frac{M}{bh^2/6}$$
>
> where $u$ is the utilisation, $\sigma$ the bending stress at the arm's root, $M$ the root moment and $bh^2/6$ the section modulus, so the same $\sigma$ gives a different $u$ depending on whether $\sigma_{\text{allow}}$ is $\sigma_\parallel$ (the stress runs in the plane of the layers) or $\sigma_\perp$ (it pulls them apart).
>
> - **Example**: B-60 under a hard move of P2's — the shoulder driven at its current limit (Worked case, step 3) — carries $\sigma=2.00$ MPa at the root. Printed flat, $u=2.00/50=0.04$; printed standing on its end, every layer interface lies across the arm and $u=2.00/12=0.17$, while the modulus drops from $3.0$ to $2.4$ GPa and the arm sags 25% more.
> - **Non-example**: taking the filament's datasheet strength as the part's. It describes material pulled along its length — the one direction in which a standing print is never loaded.
> - **Why it matters**: orientation is decided after the design is finished, by a person or a slicer default that does not know where the load goes, so the drawing or the file name has to say it.

**How to orient a part.** Four rules, in order. Put tension and bending in the plane of the layers — the guide's advice is to orient a part so that its layers run along the force. Put holes that must be round with their axes vertical: a vertical hole is a circle in every layer, while a horizontal hole's top must bridge across, and the guide reports that bridges over 5 mm sag. Keep overhangs within about 45° of vertical, the guide's usual limit before supports are needed. And put the face that must be flat — a clamp face, a datum (§7) — on the bed. B-60 lies flat: $80\times20$ mm face down, bending stress in the layers, screw holes vertical, clamp face on the bed.

**Holes come out small, so measure the allowance once.** A printed vertical hole is undersized for two reasons that add: the mesh has already cut the circle into chords (§2), and as the nozzle lays the hole's perimeter it presses the fresh road onto the layer below, flattening it wider and into the hole. How much depends on the printer, slicer, hole size and material, and where a diameter is critical the guide's advice is to print it undersized and drill it to size (Protolabs Network). So print a test strip with holes of 3, 4, 6 and 10 mm, measure them with a pin gauge or a drill's shank, and put the difference into §1's `hole_allowance`. This page's printer loses $0.2$ mm, so B-60's M3 clearance holes are modelled at $3.4+0.2=3.6$ mm to come out at 3.4.

**Materials.** Four materials cover most research hardware; the table is qualitative, from Prusa's material guides, with no numbers that are not theirs.

| Material | Printing | Heat | Toughness | Moisture and fumes | Prusa's typical use |
|---|---|---|---|---|---|
| PLA | the easiest; hardly warps | softens and deforms above 60 °C | brittle: breaks along layers or into shards on impact | degrades in UV light | detailed models and quick prototypes |
| PETG | easy; strings; bonds strongly to the bed | interior and most exterior use below 80 °C | tough and durable; good layer adhesion | resists water and humidity | mechanical parts, holders, clamps |
| ABS | warps a lot; needs an enclosure | good high-temperature resistance | tenacious; for mechanically stressed parts | styrene fumes: print in a ventilated room | technical parts needing heat and mechanical resistance |
| Nylon (PA) | warps; an enclosure helps a lot | high-temperature resistance | great mechanical resistance, abrasion-resistant | highly hygroscopic — up to 10% water by weight if stored badly, so dry it; strong odour and ultrafine particles: ventilate | technical parts needing heat, chemical and mechanical resistance |

**The traps: heat, creep, infill.** PLA softens above 60 °C, which a bracket beside a motor or in a car in summer can reach. Under sustained load a plastic *creeps* — keeps deforming slowly — the reason insert makers give for a metal thread (§5), so B-60's sag grows over weeks and its calibration drifts with it. And sparse infill leaves a part much less stiff than its outline, because bending is carried by the outer fibres, which are then only the skins and walls: print a stiffness part solid.

> [!note]- Deeper · 더 깊이
> How much infill costs. With sparse infill and skins of thickness $t$ top and bottom, B-60's section is nearly a hollow box, so if the infill itself is ignored $I\approx b\,\big(h^3-(h-2t)^3\big)/12$. For skins of $t=0.8$ mm, four layers of 0.2 mm, that is $20\,(6^3-4.4^3)/12=218.0$ mm⁴ against 360 mm⁴ solid: 61% of the stiffness, and a 65% larger sag and tilt for the same outline and material.

### 5. Fasteners: clearance holes, printed threads, inserts and preload

**The problem.** The camera has to come off B-60 and go back many times, and the bracket has to stay put on the tool. A screw driven straight into printed plastic does neither for long.

**The idea.** A screw joins two parts by clamping them. It passes through a **clearance hole** in the part under its head — larger than the screw, so it never engages it — and pulls on a **thread** in the other part: a tapped hole in metal, a nut, or a metal insert. (Metric screws are named by their major diameter: an M3 is 3 mm across its thread.) The screw clamps but does not locate, since the clearance lets the parts shift until the clamp takes hold (§7). B-60's clamp end therefore needs no thread: two M3 screws pass through it into tapped holes in P2's tool.

**Why a printed thread strips, and what an insert does.** A screw driven into a printed hole cuts its own thread in the plastic, and that thread fails three ways: it strips when tightened as a metal thread would be, it wears each time the screw comes out, and it creeps under load, so the joint loosens. Insert makers give exactly these reasons for a metal thread: it lets the proper installation torque be applied without stripping the threads that a screw in the plastic would strip, and gives creep resistance along the thread's whole load path (SPIROL). A **heat-set insert** is a knurled brass sleeve with an internal thread. Heated and pressed into a hole of its maker's specified size, it melts the plastic around it, which flows into the knurls and re-solidifies; SPIROL's conditions are the proper hole size, enough wall around the insert, and enough melting to fill its voids. B-60 takes two at its far end for the camera's screws.

**Preload, in one paragraph.** What holds a clamped joint is the **preload** — the tension a tightened screw holds, and the equal force pressing the parts together — and it is set by the tightening torque, most of which is lost to friction: Bolt Science puts the share that actually stretches the bolt at typically 10 to 15%, with about half spent under the head. The working rule lumps the friction into one nut factor $K$, about 0.2 for dry steel (Engineering ToolBox):

$$F=\frac{T}{K\,d}$$

so the preload $F$ follows from the torque $T$ and the nominal diameter $d$; and because $K$ moves with lubrication and surfaces, a torque wrench's preloads spread by a factor of 1.6, largest to smallest (Bolt Science). On B-60, an M3 clamp screw at $0.5$ N·m gives $F=0.5/(0.2\times0.003)=833$ N, about 850 times the camera's $0.98$ N weight. But the head bears on printed plastic over an annulus 5.5 mm outside and 3.4 mm inside (this page's numbers), $14.7$ mm²: a pressure of $833/14.7=56.8$ MPa, above even the 50 MPa this page gives printed PLA along its roads, so the plastic under the head can crush and will creep, and the preload goes with it. A 7 mm washer doubles the area to $29.4$ mm² and halves the pressure to $28.3$ MPa; a gentler torque does the rest. The trap is "tight" by feel into a printed thread: a preload nobody knows, held by a thread that will strip or creep.

### 6. Stiffness and mass of a sensor bracket

*In one sentence:* a sensor bracket is sized by its stiffness — the angle it lets the sensor turn between calibration and use, and the frequency at which it rings — and its strength is almost never the limit.

**The problem.** A camera calibrated on Monday reports the pin half a millimetre off on Tuesday, and after every fast move its image shivers for a moment. Nothing broke; the bracket bent, and then vibrated.

**The idea.** What the camera sees depends on its *angle*, not on how far its end sagged: a tiny tilt, multiplied by the distance to the target, is a large error there. And the bracket with its camera is a mass on a spring, which rings after a sudden stop. The beam theory is the owner's — a cantilever of length $L$ with a tip load $F$ deflects $\delta=FL^3/(3EI)$, turns its end through $\theta=FL^2/(2EI)=3\delta/(2L)$, and has a tip stiffness $k=3EI/L^3$ — and what is new is what a camera does with it.

> **Pointing error, defined.** The **pointing error** of a mounted sensor is a *length at the target*: how far the point the sensor sees moves when its mount deforms between calibration and use. Three defining conditions. The sensor is **rigid and turns with the end of its mount**, so its line of sight swings through the mount's end slope. What counts is the **change between the calibrated pose and the used pose**, since a calibration absorbs whatever deformation was there when it was made. And the angles are **small**, so a tilt $\theta$ moves the seen point by $D\theta$.
>
> $$e=\delta_\perp+D\,\theta$$
>
> where $e$ is the error at the target, $D$ the distance to it, $\theta$ the change of the mount's end slope and $\delta_\perp$ the part of the end's displacement that lies across the line of sight. B-60 looks along the tool with its arm at right angles, so its sag runs along the line of sight and $\delta_\perp=0$; a camera looking along its arm would have $\delta_\perp=\delta$.
>
> - **Example**: B-60 calibrated with its arm vertical — the camera's weight along the arm, so no bending — and used with the arm horizontal, as when P2's tool turns from horizontal to pointing down at the pin. The tilt that appears, $\theta_g=1.635$ mrad, puts the seen point $e=0.40\ \mathrm{m}\times1.635\times10^{-3}=0.654$ mm off, over the $0.5$ mm allowance (Worked case, steps 1–2); the slope's lever, $3D/(2L)=10$, makes that ten times the 65 µm sag.
> - **Non-example**: the same sag when the camera is calibrated and used in the same orientation. The calibration measured it along with everything else, so it costs nothing — and checking $\delta=FL^3/(3EI)$ against a limit, as a serviceability check would, says nothing about the case that does cost.
> - **Why it matters**: a mount's tilt is a rotation error in the hand–eye transform that changes with pose, and [[04-robotics/geometric-perception-calibration|3.5 §3]] shows what a rotation error does: it grows with range, where a translation error stays constant.

> **First natural frequency of a bracket, defined.** The **first natural frequency** of a sensor bracket is the *rate at which the sensor, displaced and let go, oscillates on its mount* — a property of the mount and its load, not of the arm's controller. Four defining conditions. **One mode dominates**: the sensor's mass, lumped at the end, is large against the arm's own, so the bracket behaves as one mass on one spring. The deformation is **linear-elastic**. The **base is much stiffer than the bracket**, so the tool does not move with it; a compliant clamp or a relaxed screw puts the frequency below the formula's. And the **damping is small**, so the oscillation happens at nearly the natural frequency and dies slowly.
>
> $$f_n=\frac{1}{2\pi}\sqrt{\frac{k}{m}}=\frac{1}{2\pi}\sqrt{\frac{g}{\delta_g}}$$
>
> where $k=3EI/L^3$ is the tip stiffness, $m$ the sensor's mass and $\delta_g$ the sag under the sensor's own weight; the second form holds because $k=mg/\delta_g$, so a bracket's frequency can be read off its static sag — the idea behind a floor-vibration check, here with the whole mass at the tip.
>
> - **Example**: B-60, $\delta_g=65.4$ µm, so $f_n=\frac{1}{2\pi}\sqrt{9.81/(65.4\times10^{-6})}=61.64$ Hz; with an 8 mm arm, $94.90$ Hz.
> - **Non-example**: the natural frequency of the arm's control loop. The capstone's computed-torque loop gives each joint's error $\omega_n=10$ rad/s, $1.59$ Hz ([[04-robotics/capstone-panel-contact|26. Capstone]]) — the rate at which P2 moves the bracket, not one at which the bracket rings.
> - **Why it matters**: the bracket's frequency decides how the image shakes after every stop, and what a camera sampling at 50 Hz makes of the shake.

**What a camera makes of the ringing.** Slow arm motion is harmless: the capstone's loop moves the bracket at $1.59$ Hz, sixty times below an 8 mm B-60's $94.90$ Hz, so the bracket simply follows. A hard stop is not: it leaves the camera swinging from its bent position at $f_n$, decaying as $e^{-\zeta\omega_nt}$. And the camera samples at $f_s=50$ Hz, so it sees a vibration at $f_n$ at the alias $|f_n-kf_s|$ ([[02-foundations/signal-processing|6. §2]]): the 8 mm arm's $94.90$ Hz appears at $|94.90-2\times50|=5.10$ Hz, a slow wander of the pin across the image that a tracker cannot tell from the pin moving — about 12 frames of it after a stop as hard as step 3's start (Worked case, step 4).

**Making a bracket stiffer.** The formulas rank the knobs. The tilt goes as $L^2/(Eh^3)$, so thickness is the strongest — from 6 to 8 mm cuts it by $(6/8)^3=0.42$ — then length, then material. A rib or a flange turns the section into a T or an L and multiplies $I$ for little mass. A lighter sensor lowers the tilt in proportion and raises $f_n$ by the square root. And the joint is part of the bracket: two screws in crept plastic (§5) make a hinge the beam formula cannot see.

> [!note]- Deeper · 더 깊이
> Two refinements. The arm's own mass adds $33/140$ of itself to $m$ — Rayleigh's estimate with the tip-load shape $y(\xi)=(3\xi^2-\xi^3)/2$, whose squared mean over the arm is $33/140=0.2357$, as the Worked case's listing checks. The 60 mm free length of an 8 mm arm is $11.9$ g of PLA at a course $1.24$ g/cm³, which adds $2.8$ g to the camera's 100 g and lowers $f_n$ by 1.4%. And forced at a frequency $f$, the lightly damped mass on a spring of [[02-foundations/engineering-math|0.5 §8]] is amplified by $1/(1-r^2)$ with $r=f/f_n$: at the capstone's $1.59$ Hz the 8 mm arm amplifies by $1.0003$, a static load, while near $r=1$ it resonates — which is why a bracket must not share its frequency with a fan, a motor's cogging or a gear mesh.

### 7. Fixtures and datums: locating a part the same way every trial

**The problem.** The mock-up's pin block is lifted off to clear a jam and put back fifty times in a study. If it lands 0.3 mm from where it was, every later trial carries 0.3 mm of error the robot did not cause, and the experiment measures the fixture.

**The idea.** Research practice calls running the same setup again *repeatability* and asks every result to name its hardware ([[06-research-practice/experimental-design-reproducibility|2. §6–§7]]); a fixture decides the hardware's share of it. To put a part back in the same place, touch it at exactly as many points as it has ways to move, no more and no fewer, and push it firmly against them. Its **datums** are the faces, axes or points it is located from, named in the order it meets them: set down on the primary, slid against the secondary, pushed into the tertiary. Screws pull it down; they do not decide where it lands.

> **3-2-1 locating, defined.** **3-2-1 locating** is the *rule for locating a rigid part with exactly as many contacts as it has degrees of freedom* — a counting rule for locators, which the clamps then serve. Four defining conditions. A rigid part has **six degrees of freedom**, three translations and three rotations; counted by direction, plus and minus along and about each axis, Carr Lane's fixture-design guide counts twelve. **Three contacts on the primary surface** remove the translation normal to it and the two tilts, **two on the secondary** remove a translation and the rotation about the primary's normal, and **one on the tertiary** removes the last translation: six locators, one degree of freedom each, stopping nine of the twelve directions. The **clamps push the part onto the locators**, stopping the other three without moving it off them. And **no locator is redundant**: a seventh contact either fights one of the six or makes the position depend on which contacts happen to touch. A flat part located by a face, a round pin and a diamond pin makes the same count: the face 3, the round pin in its hole 2, and the diamond pin, relieved to locate in one direction only, 1.
>
> $$\theta_{\max}=\frac{c_1+c_2}{2s},\qquad e_\perp(x)\le\frac{c_1}{2}\Big|1-\frac{x}{s}\Big|+\frac{c_2}{2}\Big|\frac{x}{s}\Big|$$
>
> where $c_1$ and $c_2$ are the largest diametral clearances at the round and the diamond pin, $s$ their spacing, $\theta_{\max}$ the largest rotation they allow, and $e_\perp(x)$ the largest shift across the pin line of a point a distance $x$ from the round pin. Between the pins that shift is a weighted mean of the two pins' own shifts, and beyond them it grows with $x$; along the line only the round pin acts, so the shift along it is at most $c_1/2$.
>
> - **Example**: F-50. H7/g6 on 6 mm pins gives $c_1=c_2=24$ µm (§3), so $\theta_{\max}=0.48$ mrad, and S1's pin, midway at $x=25$ mm, moves at most $12\,(1-0.5)+12\,(0.5)=12$ µm across the line and 12 µm along it — $13.9$ µm together, searched over every seating (Worked case, step 5).
> - **Non-example**: two round pins in two holes. The block's hole spacing and the plate's pin spacing each have their own tolerance, so when they differ by more than the clearance the block will not go on, and when they differ by less its position depends on which way it was pushed. That is why the second pin is a diamond: one round and one diamond pin locate from two holes without binding (Carr Lane). Four feet on a flat plate are the same mistake turned vertical: the part rocks on three of them.
> - **Why it matters**: the fixture's locating error enters every trial, and the equation says where to spend on it — spread the locators, as far apart as practical in Carr Lane's words, and put what you care about between them.

**The trap: bolts clamp, pins locate.** Hold F-50's block with its two M6 screws alone, in 6.6 mm clearance holes, and each time it is put back it can land anywhere in $0.3$ mm of play: S1's pin moves up to $0.300$ mm. On its pins it moves $0.014$ mm. The screws are still needed — they pull the block onto the plate's face, its primary datum — but they locate nothing, and their force must press the block into its locators, never across them.

**Repeatability, not accuracy.** The pin's machined position in the block, $\pm0.05$ mm, and the plate's place on the bench are fixed errors: the same every trial, measured once by touching the pin off with the robot, then gone from the budget. What the fixture must bound is what changes between trials — the pins' clearance — and any joint that comes apart between sessions needs locating pins of its own. On [[05-construction-robotics/site-engineering|2.5 §5]]'s ladder the mock-up measures the arm, tool and part terms of S1's budget; the fixture's per-trial error is the one term it adds.

### Worked case · 대상으로 한 번 끝까지

Five steps on the rig's own numbers: four on B-60, one on F-50. They use the beam formulas of §6, the definitions of §3, §4, §6 and §7, and three numbers of P2's; the listing after step 5 prints every number.

**Step 1 — the sag and the tilt.** B-60's arm is $20\times6$ mm, so $I=bh^3/12=20\times6^3/12=360$ mm⁴, and printed flat its modulus is $E_\parallel=3000$ N/mm². Its tip stiffness is $k=3EI/L^3=3\times3000\times360/60^3=15.0$ N/mm. The camera's weight, $mg=0.981$ N, sags the tip $\delta_g=0.981/15.0=0.0654$ mm and turns it through $\theta_g=3\delta_g/(2L)=3\times0.0654/120=1.635$ mrad.

**Step 2 — the cost at the pin, and the fix.** Calibrated with the arm vertical and used with it horizontal (§6), the camera turns by $\theta_g$. Its sag runs along its line of sight, so $\delta_\perp=0$ and the whole error is the tilt's:

$$e=D_w\,\theta_g=400\ \mathrm{mm}\times1.635\times10^{-3}=0.654\ \mathrm{mm}$$

because a tilt swings the line of sight about the camera, and 400 mm away the swing is 400 mm times the angle: 31% over the $0.5$ mm allowance. The tilt goes as $h^{-3}$, so the thinnest arm that meets it is $h=6\,(0.654/0.5)^{1/3}=6.56$ mm. Take 8 mm rather than 6.56, because the clamp joint and the creep of §4 and §5 add compliance the formula leaves out. Then $I=853.3$ mm⁴, $k=35.56$ N/mm, $\delta_g=27.6$ µm, $\theta_g=0.690$ mrad and $e=0.276$ mm, 45% under the allowance.

**Step 3 — orientation and strength.** Printed standing on its end, the arm's stress runs across its layers and its modulus is $E_\perp=2.4$ GPa, so every deflection grows by $3.0/2.4=1.25$: the 6 mm arm's error becomes $0.818$ mm and the 8 mm arm's $0.345$ mm, still inside the allowance. Now a hard load. At P2's catalog pose, with the forearm up and B-60 horizontal, let the shoulder drive push at its current limit of 80 N·m ([[04-robotics/actuators-drives|10.5 §3]]) with the elbow unpowered: less the $19.62$ N·m that holds the arm against gravity, it pushes the tip — 1 m out from the shoulder — upward with $60.38$ N. The tip's apparent mass in $y$ is $\Lambda_y=2$ kg (0.6), so

$$a=\frac{60.38\ \mathrm{N}}{2\ \mathrm{kg}}=30.19\ \mathrm{m/s^2},\qquad a+g=40.00\ \mathrm{m/s^2}=4.08\,g$$

since the camera feels gravity and the acceleration together. The root moment is $0.10\times40.00\times0.060=0.240$ N·m and the stress $0.240/(bh^2/6)$: $2.00$ MPa for the 6 mm arm, $1.12$ MPa for the 8 mm. Against $\sigma_\parallel=50$ MPa the margins are 25 and 44; against $\sigma_\perp=12$ MPa, 6.0 and 10.7. Stiffness sized the arm; strength never came close. Printing it standing costs 20% of its stiffness — 25% more deflection — and a factor of $50/12=4.2$ of its strength margin, which matters when the arm is knocked, not while it holds a camera.

**Step 4 — the ringing, and what the camera sees.** The 8 mm arm's natural frequency is $f_n=\frac{1}{2\pi}\sqrt{9.81/(27.6\times10^{-6})}=94.90$ Hz. A stop as hard as step 3's start changes the felt acceleration by $30.19$ m/s² almost at once, and a lightly damped mass on a spring that has its load changed suddenly swings about its new rest position with an amplitude equal to the change in its static deflection. The camera therefore rings with a tilt of $(30.19/9.81)\times0.690=2.12$ mrad, $0.849$ mm at the pin. With $\zeta=0.02$ the ringing decays as $e^{-\zeta\omega_nt}$, where $\zeta\omega_n=0.02\times2\pi\times94.90=11.93$ s⁻¹, so it falls under $0.05$ mm after

$$t=\frac{\ln(0.849/0.05)}{11.93\ \mathrm{s^{-1}}}=0.237\ \mathrm{s}=11.9\ \text{frames at }50\ \mathrm{Hz}$$

because each frame lasts 20 ms. During those frames the camera sees the $94.90$ Hz ringing at $|94.90-2\times50|=5.10$ Hz, a slow wander of the pin that a tracker will report as motion: discard the first 12 frames after a hard stop, or stop less hard.

**Step 5 — F-50's locating error.** The block sits on the plate's face (3 contacts), the round pin (2) and the diamond pin (1): six, none redundant. Each pin fits its hole H7/g6, so $c_1=c_2=24$ µm at most (§3), and the block can turn by at most

$$\theta_{\max}=\frac{24+24}{2\times50\,000}=0.48\ \mathrm{mrad}$$

because each hole can sit up to half its clearance off its pin, on opposite sides. S1's pin, midway, moves at most 12 µm across the pin line and 12 µm along it, but $13.9$ µm the two together (listing), not $12\sqrt2=17$ µm, because the round pin's clearance is a circle: a hole centre that sits the full 12 µm off along the line cannot also sit off across it, and the diamond pin alone then moves the midpoint only 6 µm across; held by the M6 screws alone, $0.300$ mm. Set these against S1. Its hole's radial clearance is $(18-16)/2=1$ mm, so the pins use 1.4% of it and the screws 30%. Against the precise fit that construction 9's Step 5 considers, $\Delta=0.2$ mm and $0.1$ mm radial, the pins use 14% and the screws three times the whole clearance: with screws alone, the fixture would decide whether the pin enters. The pin's machined position in the block, $\pm0.05$ mm, is the same in every trial; touch it off once with the robot and it leaves the budget.

The listing, run after the one in §2 as the same notebook:

```python
import math
import numpy as np

G = 9.81                                        # m/s^2
CAM, L, B, DW = 0.10, 0.060, 0.020, 0.40        # B-60: camera kg, arm length m, width m, working distance m
E_ALONG, E_ACROSS = 3.0e9, 2.4e9                # Pa, printed PLA along its roads / across its layers
S_ALONG, S_ACROSS = 50e6, 12e6                  # Pa, tensile strength in the same two directions
ALLOW, ZETA, FPS = 0.5e-3, 0.02, 50             # m at the pin; damping ratio; camera frame rate

def arm(h, E, L=L, m=CAM):
    """Tip-loaded cantilever carrying the camera: stiffness, sag, end slope, error at the pin, natural frequency."""
    I = B * h**3 / 12
    k = 3 * E * I / L**3
    sag = m * G / k
    slope = 1.5 * sag / L                       # = m g L^2 / (2 E I)
    return dict(I=I, k=k, sag=sag, slope=slope, e=DW * slope, fn=math.sqrt(k / m) / (2 * math.pi))

for h, E, label in ((0.006, E_ALONG, "h 6 mm, flat"), (0.006, E_ACROSS, "h 6 mm, upright"),
                    (0.008, E_ALONG, "h 8 mm, flat"), (0.008, E_ACROSS, "h 8 mm, upright")):
    r = arm(h, E)
    print(f"{label:16s} I={r['I']*1e12:6.1f} mm^4  k={r['k']/1e3:6.2f} N/mm  sag={r['sag']*1e6:5.1f} um  "
          f"slope={r['slope']*1e3:.3f} mrad  e={r['e']*1e3:.3f} mm  fn={r['fn']:.2f} Hz")
print(f"thinnest arm for e = 0.5 mm: {6 * (arm(0.006, E_ALONG)['e'] / ALLOW) ** (1 / 3):.2f} mm")

# a hard move of P2's: shoulder at its 80 N m current limit (10.5), catalog pose, elbow unpowered
M = np.array(((3.0, 1.0), (1.0, 1.0)))
J = np.array(((-1.0, -1.0), (1.0, 0.0)))
a = (J @ np.linalg.solve(M, np.array((80.0 - 19.62, 0.0))))[1]
print(f"tip acceleration {a:.2f} m/s^2 upward; the camera feels {a + G:.2f} m/s^2 = {(a + G) / G:.2f} g")
for h in (0.006, 0.008):
    sigma = CAM * (a + G) * L / (B * h**2 / 6)
    print(f"h {h*1e3:.0f} mm: root stress {sigma/1e6:.2f} MPa, margin {S_ALONG/sigma:.1f} flat, {S_ACROSS/sigma:.1f} upright")

r = arm(0.008, E_ALONG)
amp = (a / G) * r["e"]                          # ringing after a stop as hard as that start, seen at the pin
t = math.log(amp / 0.05e-3) / (ZETA * 2 * math.pi * r["fn"])
print(f"h 8 mm: ringing {amp*1e3:.3f} mm at the pin, under 0.05 mm after {t:.3f} s = {t*FPS:.1f} frames, "
      f"seen at {abs(r['fn'] - round(r['fn'] / FPS) * FPS):.2f} Hz by the camera")
f_loop = 10 / (2 * math.pi)                     # the capstone's joint loop, omega_n = 10 rad/s
print(f"P2's own motion at {f_loop:.2f} Hz: amplification {1 / (1 - (f_loop / r['fn'])**2):.4f}")
x = (np.arange(100000) + 0.5) / 100000          # Rayleigh: the tip-load shape, squared and averaged
print(f"share of the arm's mass that rides with the camera: {np.mean(((3 * x**2 - x**3) / 2)**2):.4f} (33/140 = {33/140:.4f})")

def worst_shift(c1, c2, s, x, diamond=True, n=3601):
    """Largest move of a point x along the pin line when a block is lifted off and put back.
    Hole 1 on the round pin: its centre anywhere within c1/2. Hole 2, a distance s away: within c2/2 across
    the line only (diamond pin), or in every direction (a round clearance). Rigid block, small rotations."""
    best = 0.0
    for phi in np.linspace(0, 2 * np.pi, n):
        t, u1 = c1 / 2 * np.cos(phi), c1 / 2 * np.sin(phi)          # hole 1: along, across
        lim = c2 / 2 if diamond else math.sqrt(max((c2 / 2)**2 - t * t, 0.0))
        for u2 in (-lim, lim):                                      # hole 2: across
            best = max(best, math.hypot(t, u1 * (1 - x / s) + u2 * x / s))
    return best

print(f"S1's pin midway, block on its pins: {worst_shift(24e-6, 24e-6, 0.050, 0.025)*1e6:.1f} um")
print(f"S1's pin midway, M6 screws only:   {worst_shift(0.6e-3, 0.6e-3, 0.050, 0.025, diamond=False)*1e3:.3f} mm")
```

Its output as run for this page (macOS, Python 3.12, NumPy 2.0.2):

```text
h 6 mm, flat     I= 360.0 mm^4  k= 15.00 N/mm  sag= 65.4 um  slope=1.635 mrad  e=0.654 mm  fn=61.64 Hz
h 6 mm, upright  I= 360.0 mm^4  k= 12.00 N/mm  sag= 81.8 um  slope=2.044 mrad  e=0.818 mm  fn=55.13 Hz
h 8 mm, flat     I= 853.3 mm^4  k= 35.56 N/mm  sag= 27.6 um  slope=0.690 mrad  e=0.276 mm  fn=94.90 Hz
h 8 mm, upright  I= 853.3 mm^4  k= 28.44 N/mm  sag= 34.5 um  slope=0.862 mrad  e=0.345 mm  fn=84.88 Hz
thinnest arm for e = 0.5 mm: 6.56 mm
tip acceleration 30.19 m/s^2 upward; the camera feels 40.00 m/s^2 = 4.08 g
h 6 mm: root stress 2.00 MPa, margin 25.0 flat, 6.0 upright
h 8 mm: root stress 1.12 MPa, margin 44.4 flat, 10.7 upright
h 8 mm: ringing 0.849 mm at the pin, under 0.05 mm after 0.237 s = 11.9 frames, seen at 5.10 Hz by the camera
P2's own motion at 1.59 Hz: amplification 1.0003
share of the arm's mass that rides with the camera: 0.2357 (33/140 = 0.2357)
S1's pin midway, block on its pins: 13.9 um
S1's pin midway, M6 screws only:   0.300 mm
```

### 8. Other processes, and working safely in the shop

**The problem.** A printer cannot make everything: a flat plate with an accurate hole, a metal block with reamed pin holes, a stiff base for the rig. Three other processes cover most of the rest, each with one number to get right.

**Laser cutting** cuts flat sheet — acrylic, plywood — along a 2D path, quickly and repeatably. The beam burns away a strip, the **kerf**, and the cut edge lies half a kerf from the path on each side, so a hole cut on its nominal path comes out one kerf too large and an outline one kerf too small: offset holes inward and outlines outward by half the kerf. A Stanford lab's notes give kerfs of 0.2 to 0.25 mm on acrylic and plywood; at $0.2$ mm, S1's 18 mm hole cut on its nominal path would be $18.2$ mm. Never cut PVC: it gives off hydrogen chloride, which MIT's safety office calls extremely dangerous, and which Epilog, a laser maker, warns damages the machine irreversibly.

**CNC machining** removes metal from a block under program control; it is how F-50's block and plate are made, with the holes that must fit drilled undersize and reamed. The machinist needs the STEP file for the geometry and a drawing for what the STEP does not say — the fits, the datums, the tolerances that matter (§3, §7). Each re-clamping to reach another face is a new setup with its own locating error, so a part machined from one side is cheaper and more accurate.

**Aluminium extrusion frames** are T-slot profiles joined by brackets and slot nuts — a rig's base, a camera gantry — built in an afternoon and rebuilt next month. Their members are beams: a 600 mm member simply supported, with $I=7\times10^4$ mm⁴ and $E=70$ GPa (course numbers for a mid-size profile), deflects $FL^3/(48EI)=100\times600^3/(48\times70\,000\times70\,000)=0.092$ mm under 100 N at midspan. The joints, not the members, are usually where a frame's compliance lives — B-60's clamp again.

**Working safely.** Take the lab's training for each machine before using it. Never wear gloves near rotating machinery such as drills and lathes, and keep loose clothing, long hair and jewellery away from it: the UK's Health and Safety Executive says that many serious workshop accidents could have been avoided had gloves not been worn near such machines. Never leave a laser cutter running unattended, keep an extinguisher beside it, and never cut PVC (MIT). Print ABS and nylon with ventilation or in an enclosure, because Prusa's guides warn of styrene fumes from ABS and ultrafine particles from nylon. A heat-set insert goes in with a tool hot enough to melt plastic: let the tool and the part cool before handling them.

### 9. What this page does not cover

Finite-element analysis, for brackets whose shape beam theory cannot describe; the full language of geometric tolerancing on engineering drawings, beyond the fits of §3 and the datums of §7; other processes — resin printing, injection moulding, sheet metal, welding; wiring and cable management; and the calibration of the camera B-60 holds, which is [[04-robotics/geometric-perception-calibration|3.5 §5]]. Actuators and their drives are [[04-robotics/actuators-drives|10.5]]; describing the finished rig to ROS — its meshes, frames and inertias — is [[04-robotics/ros2/describing-a-robot|25.6]].

### After reading

- [ ] Count a sketch's degrees of freedom to zero, and choose references that carry the design intent.
- [ ] Say which file a machinist, a slicer and version control each need, and what a coarse STL export does to a hole.
- [ ] Compute a fit's clearance range from ISO 286 deviations and classify it; say why a printed hole is not a fit.
- [ ] Choose a print orientation for a loaded part, measure and apply a hole allowance, and pick a material from the table.
- [ ] Choose a clearance hole, a tapped hole or an insert; compute a preload from a torque and check the pressure under the head.
- [ ] Compute a sensor bracket's tilt, its pointing error at the target, its natural frequency, and what a camera sees of its ringing.
- [ ] Locate a part 3-2-1 with a face, a round pin and a diamond pin, compute its worst-case locating error, and spot a redundant locator.
- [ ] State the shop rules for rotating machinery, the laser cutter and printing fumes.

### Self-check

1. B-60 sags 65 µm under its camera. Why is its error at the pin ten times that, and when is it zero?
2. You model a 6 mm hole for a g6 locating pin at exactly 6.0 mm and print it. What do you get, and how do you get a sliding fit?
3. A block located by two round pins in two reamed holes sometimes jams and otherwise sits in one of two places. Why, and what is the fix?
4. The 8 mm arm rings at $94.90$ Hz and the camera runs at 50 Hz. What does a tracker see after a hard stop, and what do you do about it?
5. Why do F-50's M6 screws not locate the block, and how far could S1's pin move if they were all that held it?

> [!tip]- Answers
> 1. The camera turns with the arm's end slope, $\theta=3\delta/(2L)$, and the slope acts over the $0.40$ m to the pin: $e=D\theta=(3D/2L)\,\delta=10\delta$. It is zero when the camera is calibrated and used in the same orientation, since the calibration then includes the sag; only the change costs.
> 2. The printer makes it about $5.8$ mm, so a pin of $5.988$–$5.996$ mm will not go in, or cracks the part if forced. The printer's error is 17 times the whole H7 zone, so no model size fixes it: print the hole undersize and drill or ream it to H7, $6.000$–$6.012$ mm, or press in a metal bushing; H7 on g6 then gives 4 to 24 µm of clearance.
> 3. Two round pins over-constrain the block in its plane: its hole spacing and the plate's pin spacing each have a tolerance, and the difference is taken up by jamming or by whichever side the block was pushed to. Make one pin a diamond, relieved to locate only across the line between the pins.
> 4. Sampled at 50 Hz, the $94.90$ Hz ringing appears at $|94.90-2\times50|=5.10$ Hz, a slow wander of the pin that looks like motion. After a stop as hard as step 3's start it begins at $0.849$ mm and, with $\zeta=0.02$, takes $0.237$ s — about 12 frames — to fall under $0.05$ mm: discard those frames, stop less hard, or stiffen the bracket.
> 5. They pass through 6.6 mm clearance holes, so the block can sit anywhere in $0.3$ mm of play and they clamp it wherever it landed: S1's pin can move $0.300$ mm per re-seating — 30% of its hole's radial clearance, three times a $0.2$ mm precise fit's — against $0.014$ mm on the pins.

### Problem set · 과제

Tier B. Using only this page, its prerequisites and the catalog; no simulator. Three knobs move. B-60 is rebuilt as **B-80**: the same 20 mm-wide arm printed flat, now 80 mm from the clamp face to the camera, in PETG with $E_\parallel=2.0$ GPa (a course number); the camera, the allowance, the working distance, the damping and the frame rate are unchanged. And F-50 becomes a rail carrying a second mock-up pin 400 mm beyond the first — S1's hole spacing — at $x=425$ mm from the round pin, still located by its round and diamond pins 50 mm apart.

1. **Draw.** The picture for the variant: (a) B-80 at $h=8$ mm, sag and tilt magnified by one stated factor, with both sight lines and the error at the pin; (b) the rail in plan, to scale, with both S1 pins, the locating pins as built, and the diamond pin where you would move it; (c) bars for B-80 at 8 mm and at your thickness from 2(a), and for the second pin on its pins and on screws alone, against the $0.5$ mm allowance and S1's 4 mm lead-in.
2. **Derive.** (a) B-80 at $h=8$ mm: $I$, $k$, $\delta_g$, $\theta_g$ and $e$; the thinnest arm that meets $0.5$ mm; $e$ at the next whole millimetre. (b) $f_n$ at 8 mm and at your thickness, and the frequency at which the 50 Hz camera sees each; the frames after a $30.19$ m/s² stop until the ringing at the pin is under $0.05$ mm, at your thickness. (c) The second pin's worst-case shift across the pin line, on the pins and on M6 screws alone; then with the diamond pin moved 25 mm past the second S1 pin ($s=450$ mm), with $\theta_{\max}$ for that layout. (d) F-50's round pin comes back ground k6 instead of g6: the fit's range at 6 mm, and what the person resetting the fixture between trials will notice.
3. **Interpret.** A lab-mate posts these design notes for the group's first mock-up rig. Name every problem, the symptom it will produce and the fix, citing the section; then estimate what the calibration step costs at the pin for this arm printed solid, and compare it with S1's 4 mm lead-in.

```text
Pin mock-up rig, v1 - notes for the group
Camera mount: PLA, 15% infill, printed standing on its end so it needs no supports.
  Arm 100 x 20 x 5 mm (5 mm in the bending direction); camera 0.10 kg, looking along the tool.
  Camera held by two M2 screws driven straight into the printed arm.
  Clamp holes for the M3 screws modelled at 3.0 mm - the screws cut their own way in.
  Hand-eye calibrated once with the tool pointing up at a board above the arm; trials run with the tool pointing down at the pin.
Pin fixture: pin block on four rubber feet on the base plate, located by two round 6 mm dowels in two reamed holes, held by two M6 screws.
```

> [!note]- How to draw it · 그리는 법
> - Panel (a): the arm to a stated scale (2 px per mm fits 80 mm), sag and tilt magnified by one factor written in the title, the working distance broken and marked "not to scale"; two sight lines from the lens — dashed at calibration, solid now — and the gap between them at the pin labelled $e=D_w\theta_g$ with its number.
> - Panel (b) to scale, about 0.5 px per mm for the 475 mm from the round pin to past the second S1 pin: both S1 pins as 16 mm circles, the locating pins as built, and the moved diamond pin dashed.
> - Panel (c) on one axis in millimetres, broken or logarithmic because the screws-only bar passes S1's 4 mm lead-in; the allowance and the lead-in as vertical lines, and the alias written beside each $f_n$ — a frequency near a multiple of 50 Hz looks harmless in a figure and is not.

> [!tip]- Solutions
> 1. (a) At 8 mm, $\delta_g=98.1$ µm and $\theta_g=1.839$ mrad, drawn at $\times150$ as a $15.8^\circ$ tilt; the gap at the pin is $e=0.736$ mm, past the $0.5$ mm line, and at 10 mm $e=0.377$ mm, inside it. (b) As built, the second S1 pin is 375 mm beyond the diamond pin, outside the pair, where rotation grows the shift; with $s=450$ mm both S1 pins sit between the locators. (c) Bars: $0.736$ and $0.377$ mm for B-80; $0.192$ mm on the pins and $4.800$ mm on screws alone for the second pin, the latter past the 4 mm lead-in; $0.017$ mm with the diamond pin moved.
> 2. (a) $I=20\times8^3/12=853.3$ mm⁴, $k=3\times2000\times853.3/80^3=10.00$ N/mm, $\delta_g=0.981/10.00=0.0981$ mm, $\theta_g=3\times0.0981/160=1.839$ mrad, $e=400\times1.839\times10^{-3}=0.736$ mm: over. The tilt goes as $h^{-3}$, so $h\ge8\,(0.736/0.5)^{1/3}=9.10$ mm; at 10 mm, $e=0.377$ mm. (b) $f_n=\frac{1}{2\pi}\sqrt{10\,000/0.10}=50.33$ Hz at 8 mm, seen at $0.33$ Hz — a drift a tracker cannot tell from the pin moving, the worst place a bracket can ring — and $70.34$ Hz at 10 mm, seen at $|70.34-50|=20.34$ Hz. At 10 mm the ringing starts at $(30.19/9.81)\times0.377=1.159$ mm and $\zeta\omega_n=0.02\times2\pi\times70.34=8.84$ s⁻¹, so it needs $\ln(1.159/0.05)/8.84=0.356$ s, 17.8 frames — 18. (c) As built, $x=425$, $s=50$: $e_\perp\le12\,|1-8.5|+12\times8.5=192$ µm on the pins. On screws alone both holes are round with $0.3$ mm of play, and the same weighting gives $300\times(7.5+8.5)=4\,800$ µm, $4.800$ mm — more than the 4 mm lead-in, so the fixture alone could put the second hole outside the pin's capture. With $s=450$ mm, $\theta_{\max}=48/(2\times450\,000)=0.053$ mrad, both S1 pins lie between the locators, and the Worked case's `worst_shift` gives $12.2$ and $16.5$ µm. (d) H7 $+12/0$ against k6 $+9/+1$: $c_{\min}=0-9=-9$ µm and $c_{\max}=12-1=11$ µm, a transition fit. Some block–pin pairs now interfere by up to 9 µm: the block has to be pressed on and levered off, it no longer drops on by hand, and each forced reset marks the hole — the opposite of a repeatable seat.
> 3. Seven problems. (i) *Standing print* (§4): bending pulls the layers apart ($E_\perp$, $\sigma_\perp$), so it sags more and snaps at a layer line; print it flat. (ii) *15% infill* (§4): only skins and walls carry the bending; print it solid. (iii) *M2 screws into plastic* (§5): threads strip and creep and the camera shifts; use heat-set inserts. (iv) *M3 holes at 3.0 mm* (§4, §5): they print near $2.8$ mm, so the screws thread into the bracket and hold it through plastic threads instead of clamping it; model $3.4+0.2=3.6$ mm or drill to 3.4. (v) *Calibrated up, used down* (§6): a 180° turn reverses the weight across the arm, so the tilt changes by $2\theta_g$. (vi) *Four rubber feet* (§7): one support too many, on a surface that is not a locator, so the block rocks and sinks; use the plate's face or three hard pads. (vii) *Two round dowels* (§7): a redundant locator; make one a diamond pin. The estimate for (v), solid and standing: $I=20\times5^3/12=208.3$ mm⁴, $\theta_g=0.981\times100^2/(2\times2400\times208.3)=9.81$ mrad, and $2\theta_g$ costs $0.40\ \mathrm{m}\times2\times9.81\times10^{-3}=7.85$ mm at the pin — nearly twice the 4 mm lead-in before any other error.

### Sources

- Library of Congress, format descriptions of [STEP (ISO 10303-21)](https://www.loc.gov/preservation/digital/formats/fdd/fdd000448.shtml), [STL](https://www.loc.gov/preservation/digital/formats/fdd/fdd000504.shtml) and [binary STL](https://www.loc.gov/preservation/digital/formats/fdd/fdd000505.shtml) — Part 21, AP242; STL's triangles, rules and bytes.
- STEP Tools, [ISO 10303 STEP Standards](https://www.steptools.com/stds/step/) — AP242 replaces AP203 and AP214 for CAD data.
- Open Cascade, [STEP Translator](https://occt3d.com/dev/doc/overview/html/occt_user_guides__step.html) — B-rep solids and exact surfaces in STEP.
- NIST, [STEP File Analyzer and Viewer](https://www.nist.gov/services-resources/software/step-file-analyzer-and-viewer) — parts, assemblies, PMI.
- Autodesk, [STL import options](https://help.autodesk.com/cloudhelp/2020/ENU/Alias-Reference/files/GUID-B7BF855B-724D-46E4-8FE3-185737BB9D31.htm) — STL is unitless.
- RoyMech, [ISO 286 limits and fits](https://www.roymech.co.uk/Useful_Tables/ISO_Tolerances/), [hole](https://www.roymech.co.uk/Useful_Tables/ISO_Tolerances/ISO_286_2H.html) and [shaft](https://www.roymech.co.uk/Useful_Tables/ISO_Tolerances/ISO_286_2s.html) tables — grades, fits, every deviation used.
- Carr Lane, [Locating & Clamping Principles](https://www.carrlane.com/engineering-resources/fixture-design-principles/locating-clamping-principles), [Round & Diamond Pins](https://www.carrlane.com/product/locating-pins/locating-pins/round-diamond-pins) — 3-2-1, clamps, spacing, redundancy.
- SPIROL, [Threaded Inserts for Plastics](https://www.spirol.com/product/threaded-inserts-for-plastics/), [Heat / Ultrasonic Inserts](https://www.spirol.com/product/threaded-inserts-for-plastics/heat-ultrasonic-inserts/) — metal threads in plastic.
- Protolabs Network, [part orientation](https://www.hubs.com/knowledge-base/how-does-part-orientation-affect-3d-print/), [designing for FDM](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) — anisotropy, overhangs, bridges, holes.
- Prusa Knowledge Base, [PLA](https://help.prusa3d.com/article/pla_2062), [PETG](https://help.prusa3d.com/article/petg_2059), [ABS](https://help.prusa3d.com/article/abs_2058), [nylon](https://help.prusa3d.com/article/polyamide-nylon_167188) — §4's table.
- Engineering ToolBox, [Bolt Torque Calculator](https://www.engineeringtoolbox.com/bolt-torque-load-calculator-d_2065.html) — $T=KFd$, $K=0.2$.
- Bolt Science, [head or nut](https://www.boltscience.com/pages/nutorbolttightening.htm), [preload variation](https://www.boltscience.com/pages/basics9.htm) — 10–15% of torque; factor 1.6.
- Stanford BDML, [offset for kerf](http://bdml.stanford.edu/pmwiki/index.php/Main/AddingOffsetForKerf) — kerf and its half offset.
- MIT EHS, [Laser Cutter Safety](https://ehs.mit.edu/workplace-safety-program/laser-cutter-safety/); Epilog, [unsafe materials](https://www.epiloglaser.com/how-it-works/faq/laser-machine-unsafe-materials/) — PVC, supervision.
- UK HSE, [Getting started](https://www.hse.gov.uk/engineering/getting-started.htm) — gloves and rotating machinery.

## 한국어

*[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 그리고 토목공학 학위의 보 이론과 정역학 위에 선다. 이 페이지는 그것들을 가르치지 않고 가져다 쓴다. 여기서 P2는 모델링할 대상이 아니라 무언가를 달아서 쓸 기계다. 공구에 다는 카메라 브래킷, 그리고 건설 트랙의 위치 결정 핀 목업을 매 시행 같은 자리에 붙잡아 두는 고정구를 만든다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]가 그리는 피지컬 AI 스택 아래의 바닥, 곧 도구 가운데 실험이 딛고 서는 하드웨어에 속한다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 그 절의 사례 "저 패널을 프레임에 설치해"에서 이 페이지가 맡는 것은 프레임을 알아보는 단계와 끼움을 해내는 단계다. 카메라 브래킷은 로봇이 핀이 어디 있다고 믿는지를, 고정구는 핀이 실제로 어디 있는지를 시행마다 정한다. 둘 중 하나라도 틀리면 실험은 로봇이 아니라 리그를 잰다. 6 mm 두께로 출력한 B-60은 보이는 핀을 $0.654$ mm 옮겨 S1의 공구 할당 $0.5$ mm 전부를 넘기고, 나사만으로 잡은 핀 블록은 시행마다 $0.300$ mm까지 다른 자리에 앉는다. S1을 [[05-construction-robotics/site-engineering|2.5 §5]] 사다리의 실험실 단에서 시험하려면 [[05-construction-robotics/construction-manipulation|9. 건설 조작]]과 [[05-construction-robotics/imitating-contact|10. 접촉 모방]]에 바로 이런 리그 — 공구에 고정한 카메라와 매 시행 같은 자리로 돌아오는 핀 — 가 필요하고, [[04-robotics/geometric-perception-calibration|3.5 §5]]는 브래킷이 든 카메라를 보정하며, [[06-research-practice/experimental-design-reproducibility|연구 실무 2 §7]]은 모든 실행에 하드웨어 개정을 적으라고 한다. 이 페이지는 학위논문 경로([[07-research-program/index|연구 프로그램 §8]])의 일곱 블록 밖에 있으니, 실험에 리그가 필요해질 때, 늦어도 블록 6이나 7의 첫 목업 시행 전에 읽는다. 읽고 나면 대상에서의 기울기와 진동으로 센서 브래킷의 크기를 정하고, 구멍이 맞도록 알맞은 방향으로 출력하고, 매 시행 부품을 14 µm 안으로 되돌려 놓는 고정구를 만들 수 있다.

> [!note] 처음이라면 · First pass
> 약 90분씩 두 번. **1회차 — 브래킷.** 이 페이지의 대상과 그림 — 부품 둘, 그리고 중요한 막대 셋, $0.654$, $0.276$, $0.014$ mm — 을 보고, §6을 읽은 뒤 계산기를 들고 계산 절의 1, 2, 4단계를 푼다. 65 µm의 처짐이 왜 핀에서 $0.654$ mm가 되는지, 카메라가 진동을 왜 5 Hz로 보는지. 스스로 점검 1번과 4번으로 마친다. **2회차 — 고정구.** §3과 §7을 읽고 5단계를 푼다. 끼워맞춤이 무엇인지, 왜 핀은 위치를 정하고 나사는 못 정하는지. 스스로 점검 3번과 5번으로 마친다. 그다음은 필요할 때: §4와 §5, 그리고 3단계는 첫 출력 전에(출력 방향, 구멍 여유, 인서트, 스스로 점검 2번), §1–§2는 CAD 프로그램을 열 때, §8은 레이저 커터나 가공소, 프레임이 필요해지는 날 읽고, 과제는 맨 나중에 한다. *더 깊이* 상자는 두 번째 읽을 때로 미뤄도 된다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2** — 단위 링크의 평면 2R 팔로 수직면에 서 있고, 카탈로그 자세 $\theta=(0^\circ,90^\circ)$에서 전완이 곧게 위를 향하며 말단의 겉보기 질량은 $\Lambda=\mathrm{diag}(1,2)$ kg이다 — 에 실험용 하드웨어 두 가지를 단다. 카탈로그의 어느 항목도 만들어야 할 부품이 아니므로 이 페이지가 둘을 고정한다. 두 표의 숫자는 모두 이 페이지가 정한 교과용 숫자이고, 측정값도 데이터시트 값도 아니다.

**B-60, 카메라 브래킷.** PLA로 출력한 팔을 M3 나사 두 개로 P2의 공구에 물리고, 60 mm 바깥 끝에 단안 카메라를 단다. 팔은 P2의 평면 안에서 공구와 직각으로 뻗고, 카메라는 공구와 나란히 앞을 보며 접근하는 동안 S1의 핀을 지켜본다. 이것은 두 번째 카메라다. [[04-robotics/geometric-perception-calibration|3.5 기하 인식과 보정]]의 스테레오 손목 리그는 장착부를 강체로 다루지만, 여기서는 실제 장착부가 무엇을 더하는지 묻는다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $m$ | $0.10$ kg | 카메라. 팔 끝에 모인 질량으로 본다 |
| $L$ | $60$ mm | 물림면에서 카메라 질량 중심까지 |
| $b\times h$ | $20\times6$ mm | 팔의 단면. $h$가 휘는 방향 |
| $E_\parallel,\ E_\perp$ | $3.0$, $2.4$ GPa | 출력한 PLA의 탄성계수. 로드(출력된 가닥, §4)를 따라서, 그리고 층을 가로질러서 |
| $\sigma_\parallel,\ \sigma_\perp$ | $50$, $12$ MPa | 같은 두 방향의 인장강도 |
| $\zeta$ | $0.02$ | 브래킷의 감쇠비 |
| $D_w$ | $0.40$ m | 카메라가 접근을 이끄는 동안 카메라에서 핀까지 |
| $f_s$ | $50$ Hz | 카메라의 프레임 속도, P6의 비전 속도 |
| $e_{\max}$ | $0.5$ mm | 브래킷이 핀에서 써도 되는 오차: S1의 공구 할당 전부 |

**F-50, 핀 고정구.** [[05-construction-robotics/construction-manipulation|9. 건설 조작]]이 고정한 S1의 위치 결정 핀 — 지름 16 mm, 반경 오차 4 mm까지 붙잡아 주는 테이퍼 코 — 을 강철로 본뜬 목업이 $80\times40$ mm 알루미늄 블록에 압입되어 있다. 블록은 작업대에 볼트로 고정한 베이스판 위에 놓이고, 판의 윗면과 50 mm 떨어진 위치 결정 핀 두 개 — 둥근 핀 하나, 그리고 양옆을 깎아 한 방향으로만 위치를 잡는 다이아몬드 핀 하나(§7) — 가 자리를 정한다. S1의 핀은 두 핀의 한가운데에 있고, M6 나사 두 개가 블록을 눌러 둔다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $d,\ D$ | $16$, $18$ mm | S1의 핀과 구멍. 가운데 놓이면 반경 틈새 $1$ mm (건설 9) |
| $r_c$ | $4$ mm | 핀의 코가 붙잡는 반경 오차 (건설 9) |
| 위치 결정 핀 | $\varnothing6$ mm, g6 핀에 H7 구멍(미끄럼 끼워맞춤, §3) | 둥근 핀과 다이아몬드 핀, 간격 $s=50$ mm |
| 누름 나사 | $6.6$ mm 구멍의 M6 | 둘. 블록을 판 쪽으로 당겨 누른다 |
| 블록 속 핀 | $\pm0.05$ mm | 가공이 위치 결정 구멍에 대해 S1의 핀을 놓는 자리 |

숫자 하나는 프린터의 것이다. 이 프린터는 수직 구멍을 모델보다 $0.2$ mm 작게 뽑는다. 전체 크기 패널이 아니라 핀 하나를 본뜬 이 작업대 목업은 [[05-construction-robotics/site-engineering|2.5]]의 증거 사다리에서 실험실 단에 서고, 그 단은 S1 오차 예산의 팔·공구·부품 항을 잰다. 고정구는 자기 오차를 그 항들에 섞지 말아야 한다.

*범위: 이 페이지는 첫 번째나 두 번째 출력에서 제대로 동작하는 브래킷이나 고정구를 얻는 데 필요한 것을 가르친다 — 파라메트릭 CAD의 설계 의도, STEP과 STL 형식, 끼워맞춤, 출력 방향과 구멍 여유, 체결구와 인서트, 센서 마운트의 강성 점검, 그리고 3-2-1 위치 결정. 보 이론, 유한요소해석, 기하 공차 전반, 직업으로서의 기계 가공은 가르치지 않는다. 카메라 보정은 [[04-robotics/geometric-perception-calibration|3.5 §5]], 리그를 ROS에 기술하는 일은 [[04-robotics/ros2/describing-a-robot|25.6 §4]], 고정구가 섬기는 시행 규약은 [[06-research-practice/experimental-design-reproducibility|연구 실무 2]]에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="세 패널. (a) 두께 6 mm, 길이 60 mm의 출력 팔 B-60이 P2의 공구에 물려 0.10 kg 카메라를 들고, 카메라는 공구를 따라 400 mm 떨어진 S1의 핀을 본다. 처짐과 기울기는 150배로 그렸다: 처짐 65 마이크로미터, 기울기 1.64 밀리라디안. (b) F-50의 평면도: 베이스판 위 80×40 mm 핀 블록을 판 면, 둥근 핀, 50 mm 떨어진 다이아몬드 핀이 위치 결정하고, 6.6 mm 구멍의 M6 나사 둘이 누른다. S1의 16 mm 핀은 두 핀 가운데 있다. (c) 핀에서의 오차(mm): 고정된 B-60 0.654, 세워 출력 0.818, 8 mm 팔 0.276; 핀으로 놓은 F-50 0.014, 나사만 0.300. 허용치 0.5 mm, 반경 0.1 mm의 정밀 끼워맞춤, S1의 반경 틈새 1.0 mm와 견준다.">
<text x="12" y="18" font-size="12" fill="currentColor" font-weight="600">(a) P2 공구 위의 B-60 (처짐·기울기 ×150)</text>
<rect x="20" y="34" width="32" height="96" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="146" font-size="10.5" fill="currentColor" text-anchor="middle">P2 공구</text>
<line x1="26" y1="58.0" x2="52" y2="58.0" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
<line x1="26" y1="70.0" x2="52" y2="70.0" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
<rect x="52.0" y="58.0" width="120.0" height="12.0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
<polyline points="52.0,64.0 56.0,64.0 60.0,64.1 64.0,64.3 68.0,64.5 72.0,64.8 76.0,65.1 80.0,65.5 84.0,65.9 88.0,66.4 92.0,66.9 96.0,67.5 100.0,68.1 104.0,68.7 108.0,69.4 112.0,70.1 116.0,70.9 120.0,71.7 124.0,72.5 128.0,73.3 132.0,74.2 136.0,75.1 140.0,76.0 144.0,76.9 148.0,77.8 152.0,78.8 156.0,79.7 160.0,80.7 164.0,81.7 168.0,82.6 172.0,83.6" fill="none" stroke="currentColor" stroke-width="12" stroke-opacity="0.35"/>
<polyline points="52.0,64.0 56.0,64.0 60.0,64.1 64.0,64.3 68.0,64.5 72.0,64.8 76.0,65.1 80.0,65.5 84.0,65.9 88.0,66.4 92.0,66.9 96.0,67.5 100.0,68.1 104.0,68.7 108.0,69.4 112.0,70.1 116.0,70.9 120.0,71.7 124.0,72.5 128.0,73.3 132.0,74.2 136.0,75.1 140.0,76.0 144.0,76.9 148.0,77.8 152.0,78.8 156.0,79.7 160.0,80.7 164.0,81.7 168.0,82.6 172.0,83.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
<g transform="rotate(14.05 172.0 83.6)"><rect x="160.0" y="89.6" width="24" height="18" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/></g>
<rect x="160.0" y="70.0" width="24" height="18" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" stroke-opacity="0.7"/>
<line x1="172.0" y1="88.0" x2="172.0" y2="196.0" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="166.2" y1="106.9" x2="143.9" y2="196.0" stroke="currentColor" stroke-width="1.3"/>
<line x1="143.9" y1="199.0" x2="172.0" y2="199.0" stroke="currentColor" stroke-width="1"/>
<line x1="143.9" y1="195.0" x2="143.9" y2="203.0" stroke="currentColor" stroke-width="1"/>
<line x1="172.0" y1="195.0" x2="172.0" y2="203.0" stroke="currentColor" stroke-width="1"/>
<text x="138.9" y="203.0" font-size="10.5" fill="currentColor" text-anchor="end">e = D_w θ = 0.654 mm</text>
<rect x="156.0" y="206.0" width="32" height="10" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
<text x="194.0" y="215.0" font-size="10.5" fill="currentColor">S1의 핀</text>
<text x="180.0" y="146" font-size="10.5" fill="currentColor">D_w = 400 mm</text>
<text x="180.0" y="160" font-size="10.5" fill="currentColor">(축척 아님)</text>
<text x="112.0" y="52.0" font-size="10.5" fill="currentColor" text-anchor="middle">L = 60 mm, h = 6 mm</text>
<text x="190.0" y="86" font-size="10.5" fill="currentColor">δ = 65 µm</text>
<text x="190.0" y="100" font-size="10.5" fill="currentColor">θ = 1.64 mrad</text>
<text x="12" y="238" font-size="10.5" fill="currentColor">카메라 0.10 kg, 공구 방향으로 본다</text>
<text x="290" y="18" font-size="12" fill="currentColor" font-weight="600">(b) 베이스판 위의 F-50, 평면 (1.6 px/mm)</text>
<rect x="308.0" y="40.0" width="224.0" height="144.0" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
<rect x="356.0" y="80.0" width="128.0" height="64.0" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.3"/>
<circle cx="420.0" cy="112.0" r="12.8" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="1.2"/>
<circle cx="380.0" cy="112.0" r="4.8" fill="currentColor" stroke="currentColor" stroke-width="1"/>
<circle cx="460.0" cy="112.0" r="4.8" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="1.5 1.5"/>
<path d="M460.0 107.2 L461.6 112.0 L460.0 116.8 L458.4 112.0 Z" fill="currentColor" stroke="currentColor" stroke-width="1"/>
<text x="380.0" y="103.0" font-size="10" fill="currentColor" text-anchor="middle">둥근 핀</text>
<text x="460.0" y="103.0" font-size="10" fill="currentColor" text-anchor="middle">다이아몬드</text>
<circle cx="400.8" cy="92.8" r="5.3" fill="none" stroke="currentColor" stroke-width="1"/>
<circle cx="400.8" cy="92.8" r="4.8" fill="none" stroke="currentColor" stroke-width="0.8"/>
<line x1="397.8" y1="92.8" x2="403.8" y2="92.8" stroke="currentColor" stroke-width="0.8"/><line x1="400.8" y1="89.8" x2="400.8" y2="95.8" stroke="currentColor" stroke-width="0.8"/>
<circle cx="439.2" cy="131.2" r="5.3" fill="none" stroke="currentColor" stroke-width="1"/>
<circle cx="439.2" cy="131.2" r="4.8" fill="none" stroke="currentColor" stroke-width="0.8"/>
<line x1="436.2" y1="131.2" x2="442.2" y2="131.2" stroke="currentColor" stroke-width="0.8"/><line x1="439.2" y1="128.2" x2="439.2" y2="134.2" stroke="currentColor" stroke-width="0.8"/>
<line x1="380.0" y1="156.8" x2="460.0" y2="156.8" stroke="currentColor" stroke-width="1"/>
<line x1="380.0" y1="152.8" x2="380.0" y2="160.8" stroke="currentColor" stroke-width="1"/><line x1="460.0" y1="152.8" x2="460.0" y2="160.8" stroke="currentColor" stroke-width="1"/>
<line x1="380.0" y1="118.8" x2="380.0" y2="152.8" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2 2"/><line x1="460.0" y1="118.8" x2="460.0" y2="152.8" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2 2"/>
<text x="420.0" y="170.8" font-size="10.5" fill="currentColor" text-anchor="middle">s = 50 mm</text>
<text x="420.0" y="74.0" font-size="10.5" fill="currentColor" text-anchor="middle">핀 블록 80 × 40 mm, 가운데 S1 핀 Ø16</text>
<text x="290" y="198.0" font-size="10.5" fill="currentColor">판 면 3 + 둥근 핀 2 + 다이아몬드 핀 1 = 6</text>
<text x="290" y="212.0" font-size="10.5" fill="currentColor">6.6 구멍의 M6 누름 나사는 위치를 정하지 않는다</text>
<text x="12" y="264.0" font-size="12" fill="currentColor" font-weight="600">(c) 핀에서 치르는 값 (mm)</text>
<text x="184.0" y="289.0" font-size="10.5" fill="currentColor" text-anchor="end">B-60, h 6 mm, 눕혀 출력</text>
<rect x="190.0" y="278.0" width="228.9" height="14" fill="currentColor" fill-opacity="0.55"/>
<text x="423.9" y="289.0" font-size="10.5" fill="currentColor">0.654</text>
<text x="184.0" y="312.0" font-size="10.5" fill="currentColor" text-anchor="end">B-60, h 6 mm, 세워 출력</text>
<rect x="190.0" y="301.0" width="286.1" height="14" fill="currentColor" fill-opacity="0.55"/>
<text x="481.1" y="312.0" font-size="10.5" fill="currentColor">0.818</text>
<text x="184.0" y="335.0" font-size="10.5" fill="currentColor" text-anchor="end">B-60, h 8 mm, 눕혀 출력</text>
<rect x="190.0" y="324.0" width="96.6" height="14" fill="currentColor" fill-opacity="0.55"/>
<text x="291.6" y="335.0" font-size="10.5" fill="currentColor">0.276</text>
<text x="184.0" y="358.0" font-size="10.5" fill="currentColor" text-anchor="end">F-50, H7/g6 핀</text>
<rect x="190.0" y="347.0" width="4.8" height="14" fill="currentColor" fill-opacity="0.3"/>
<text x="199.8" y="358.0" font-size="10.5" fill="currentColor">0.014</text>
<text x="184.0" y="381.0" font-size="10.5" fill="currentColor" text-anchor="end">F-50, 나사만</text>
<rect x="190.0" y="370.0" width="105.0" height="14" fill="currentColor" fill-opacity="0.3"/>
<text x="300.0" y="381.0" font-size="10.5" fill="currentColor">0.300</text>
<line x1="190.0" y1="393.0" x2="540.0" y2="393.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
<line x1="190.0" y1="393.0" x2="190.0" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="190.0" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="277.5" y1="393.0" x2="277.5" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="277.5" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.25</text>
<line x1="365.0" y1="393.0" x2="365.0" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="365.0" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.5</text>
<line x1="452.5" y1="393.0" x2="452.5" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="452.5" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">0.75</text>
<line x1="540.0" y1="393.0" x2="540.0" y2="397.0" stroke="currentColor" stroke-width="1"/>
<text x="540.0" y="409.0" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<line x1="365.0" y1="272.0" x2="365.0" y2="393.0" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
<line x1="225.0" y1="272.0" x2="225.0" y2="393.0" stroke="currentColor" stroke-width="1.1" stroke-dasharray="1.5 3"/>
<line x1="540.0" y1="272.0" x2="540.0" y2="393.0" stroke="currentColor" stroke-width="1.1" stroke-dasharray="1.5 3"/>
<text x="225.0" y="423.0" font-size="10.5" fill="currentColor" text-anchor="middle">정밀 끼워맞춤 0.1</text>
<text x="540.0" y="423.0" font-size="10.5" fill="currentColor" text-anchor="end">S1 반경 틈새 1.0</text>
<text x="365.0" y="437.0" font-size="10.5" fill="currentColor" text-anchor="middle">허용치 0.5 (S1의 공구 항)</text>
</svg>

리그의 두 부분과, 각각이 S1의 핀에서 치르는 값. 카메라는 팔 끝의 기울기만큼 돌아가므로 B-60의 처짐 65 µm는 $0.40$ m 떨어진 핀에서 $0.654$ mm가 되어 허용치 $0.5$ mm를 넘는다. 팔을 8 mm로 하면 $0.276$ mm로 내려가고, 6 mm 팔을 세워서 출력하면 $0.818$ mm가 된다. F-50의 블록은 핀에 다시 놓으면 많아야 $0.014$ mm 움직이지만, 나사로만 잡으면 $0.300$ mm까지 움직여 S1의 반경 틈새 $1$ mm의 거의 3분의 1, 정밀 끼워맞춤 $0.1$ mm의 세 배에 이른다.

### 1. 설계 의도와 파라메트릭 모델

**문제.** 실험용 부품은 만들어지는 횟수보다 다시 설계되는 횟수가 많다. 첫 출력을 해 보니 카메라를 20 mm 더 내밀어야 하고, 구멍은 작다. 부품을 고정된 선으로만 그려 두었다면 바꿀 때마다 다시 그려야 하고, 다시 그리다 보면 구멍 하나가 맞춰야 할 탭 구멍에서 20 mm 떨어진 자리에 가 있다.

**핵심 생각.** 부품을 숫자에 이름이 붙은 레시피로 적고, 모든 치수를 그 치수가 맞춰야 할 대상에서 잰다. 파라메트릭 CAD에서 **스케치**(sketch)는 평면 위의 2D 윤곽이다. **구속**(constraint)이 스케치를 붙잡는데, 기하 구속(수평, 동심)과 치수 구속(이 길이는 `L`)이 있다. **피처**(feature)는 스케치를 솔리드로 바꾸고(6 mm 돌출, 구멍 뚫기) 순서 있는 이력으로 남으므로, `L`을 바꾸면 새 숫자로 이력이 다시 재생된다. **어셈블리**(assembly)는 **메이트**(mate)로 부품의 자리를 정한다. 메이트는 §7의 위치결정구처럼 자유도를 없앤다. 동심 메이트를 걸면 핀은 축을 따라 미끄러지고 축 둘레로 도는 것만 남고, 면 맞댐 메이트가 미끄러짐마저 막는다.

> **파라메트릭 모델의 정의.** **파라메트릭 모델**(parametric model)은 솔리드 자체가 아니라 *솔리드를 만드는 레시피*다. 스케치는 구속으로 고정되고 치수는 이름 붙은 파라미터인 피처들의 순서 있는 목록이다. 정의 조건 넷. 형상은 **순서 있는 피처 이력에서 다시 생성**되고, 각 피처는 자기보다 먼저 있는 형상을 참조한다. 모든 스케치는 **완전 구속**되어, 어느 요소도 구속을 깨지 않고는 움직일 수 없다. 아래의 셈이 이것을 숫자로 바꾼다. 중요한 치수는 **이름 붙은 파라미터**여서, 한 번 바꾸면 그 파라미터를 쓰는 모든 피처에 전해진다. 그리고 각 치수는 **기능을 지는 피처에서 잰다** — 맞닿는 면, 위치를 정하는 구멍에서. 실무에서 *설계 의도*라는 말이 뜻하는 것이 이것이다.
>
> $$\mathrm{DOF}=\sum_i n_i-\sum_j r_j=0$$
>
> $n_i$는 스케치 요소 $i$를 정하는 좌표의 수로, 점은 2, 선분은 끝점이 둘이라 4, 원은 3이다. $r_j$는 구속 $j$가 거는 방정식의 수로, 두 점을 일치시키면 2, 수평·수직·접선·같음은 1, 치수 하나에 1, 점을 원점에 고정하면 2다. 셈이 0이 되면 스케치가 완전 구속된 것이므로, 스케처가 보여 주는 "남은 자유도"는 이 합이다.
>
> - **예**: 위에서 본 B-60의 윤곽, $80\times20$ mm 직사각형(물리는 20 mm, 팔 60 mm). 선분 넷이 16을 가져오고, 모서리 일치 넷이 8, 수평 둘과 수직 둘이 4, 길이와 폭이 2, 원점에 고정한 모서리가 2를 없애서 DOF $=0$이다. 물림 구멍마다 원이 3을 더하고 3을 없앤다 — 식 `clearance_m3 + hole_allowance`로 정한 지름, 그리고 물림 끝과 한쪽 가장자리에서 잰 거리 둘.
> - **비예**: 같은 구멍을 카메라 쪽 끝에서 잰 경우. 셈은 여전히 0이지만, 팔을 80 mm로 늘리면 물림 구멍이 20 mm 밀려나 공구의 탭 구멍과 어긋난다. 0은 필요조건일 뿐이고, 의도는 참조가 싣는다.
> - **왜 중요한가**: 리그 하드웨어는 예비 실험과 본 실험 사이에 고쳐진다. 숫자 하나만 바꿔도 올바르게 다시 생성되는 모델이라야 드릴로 땜질하지 않고 실제로 고쳐 쓰게 된다.

**B-60에서.** 물림 구멍은 물림 끝에서 잰다. 그 구멍이 맞춰야 할 상대가 공구의 탭 구멍이기 때문이다. 카메라 구멍은 카메라가 앉는 먼 쪽 끝에서 잰다. 그리고 팔 길이 $L$은 그 사이의 파라미터 하나이므로, §6의 질문 — 팔을 얼마나 길게 해도 되는가 — 이 숫자 하나의 문제가 된다. 프린터의 구멍 여유(§4)도 파라미터 하나로 두고, 출력하는 모든 구멍이 그것을 쓴다.

**함정: 레시피를 잃어버리기.** 모델에서 내보낸 STEP이나 STL(§2)은 파라미터가 빠진 스냅숏이다. 원본 파일, 내보낸 파일, 그리고 "B-60 r2: 팔 8 mm" 같은 개정 이름을 실험 코드와 함께 그 저장소에 둔다([[02-foundations/tools/git-research-code|12.2 연구 코드를 위한 Git]]). 연구 실무의 산출물 체크리스트가 모든 실행에 쓴 하드웨어 개정을 적으라고 하기 때문이다([[06-research-practice/experimental-design-reproducibility|2. §7]]). 같은 모델에서 URDF의 `<inertial>`이 요구하는 질량, 질량 중심, 관성 텐서도 나온다([[04-robotics/ros2/describing-a-robot|25.6 §4]]).

### 2. CAD를 떠나는 파일: STEP, STL, 그리고 메시가 솔리드가 아닌 이유

**문제.** 모델은 CAD 프로그램을 떠나 프린터로, 가공 기술자에게로, URDF로 가야 하고, 받는 쪽마다 원하는 파일이 다르다. 엉뚱한 파일을 보내면 부품이 틀려서 돌아오는데, 맞춰 보기 전까지는 아무도 모른다.

**핵심 생각.** 파일에는 두 종류가 있다. 하나는 정확한 솔리드를 간직한다 — 구멍은 반지름 9 mm의 원통이다. 금속을 깎거나 형상을 고칠 사람을 위한 파일이다. 다른 하나는 표면을 근사하는 평평한 삼각형의 껍데기를 간직한다 — 구멍은 다각형이다. 프린터와 뷰어를 위한 파일이다. **STEP**(ISO 10303, `.stp`, `.step`)이 정확한 쪽이다. 그 솔리드는 정확한 평면, 원통, B-스플라인 곡면으로 둘러싸인 경계 표현이고(Open CASCADE), NIST는 STEP 파일이 부품, 어셈블리, 공차까지 싣는다고 설명한다. **STL**이 삼각형 쪽으로, 3D 프린팅의 메시 형식이다. 표면만을, 법선 하나와 꼭짓점 셋을 가진 삼각형들로 담고(미 의회도서관), 단위가 없다. Autodesk 문서 스스로 단위 없는 형식이라고 부르므로, 읽는 쪽이 단위를 가정해야 한다.

> **테셀레이션 메시의 정의.** **테셀레이션 메시**(tessellated mesh)는 *솔리드의 정확한 경계를 대신하는 평평한 삼각형들의 곡면*이다. 경계의 근사이지 솔리드의 기술이 아니다. 정의 조건 셋. **면으로 쪼개져 있다**: 모든 곡면이 꼭짓점을 참 곡면 위에 둔 평평한 삼각형이 되므로, 꼭짓점 사이에서 메시는 볼록한 곡선의 안쪽을 가르고, 구멍 둘레에서는 구멍 안으로 파고든다. **닫혀 있고 방향이 일관된 것**은 모든 삼각형이 이웃과 변을 통째로 나누고 꼭짓점을 같은 방향으로 적을 때뿐인데, 형식은 그것을 강제하지 않는다(아래의 더 깊이). 그리고 **차원이 없다**: 숫자에 단위가 붙지 않는다.
>
> $$\Delta D=D\,\big(1-\cos(\pi/n)\big)$$
>
> $\Delta D$는 선분 $n$개로 메시화한 구멍이 다각형의 평평한 변 사이에서 지름 $D$보다 얼마나 작은가다. 꼭짓점은 원 위에 있고 각 변은 원 안쪽을 가르는 현이기 때문이다.
>
> - **예**: 목업의 구멍판 — 지름 40 mm, 두께 6 mm 원판에 S1의 18 mm 구멍 — 을 원 하나에 16, 32, 64개의 선분으로 내보내면 삼각형 128, 256, 512개이고, 구멍은 평평한 변 사이에서 $17.654$, $17.913$, $17.978$ mm다. 16개일 때 $\Delta D=18(1-\cos11.25^\circ)=0.346$ mm다.
> - **비예**: 같은 판의 STEP 파일. 그 구멍은 선분 수라는 것이 아예 없는 원통이다. STEP 대신 16선분 STL을 받은 가공 기술자는 $0.346$ mm 작은 구멍과, 읽을 단위가 없는 숫자를 받는다.
> - **왜 중요한가**: 메시는 슬라이서가 출력하고 URDF가 그리는 것이므로, 선분 수는 §4의 출력 구멍 오차에 더해진다. 단위가 없다는 것은 인치나 미터로 설계한 부품이 밀리미터를 가정하는 프로그램에서 25.4배나 1,000배 작게 나타나는 이유다.

**함정: 엉뚱한 사람에게 엉뚱한 파일.** 가공소나 다른 CAD 프로그램에는 STEP을, 끼워맞춤과 데이텀을 적은 도면과 함께 보낸다(§3, §7). 슬라이서에는 프린터 자신의 구멍 오차보다 $\Delta D$가 충분히 작도록 곱게 내보낸 STL을 준다. 18 mm 구멍이 $0.02$ mm 넘게 줄지 않게 하려면 $1-\cos(\pi/n)\le0.02/18$, 곧 선분이 적어도 67개다. 버전 관리에는 원본 파일도 넣는다. 그리고 URDF의 충돌 형상에는 고운 CAD 메시를 절대 쓰지 않는다([[04-robotics/ros2/describing-a-robot|25.6 §4]]).

> [!note]- 더 깊이 · Deeper
> **형식의 속.** STEP 파일은 ISO 10303 Part 21의 교환 구조를 따르는 평문 텍스트이고, 무엇을 담을 수 있는지는 응용 프로토콜이 정한다. 2014년에 나온 AP242가 AP203과 AP214를 합쳐 확장했고, CAD 데이터를 내보낼 때 고를 것이 이것이다(미 의회도서관, STEP Tools). 이진 STL — [[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식 §7]]이 말하는 뜻의 바이너리 레코드 — 은 80바이트 헤더, 32비트 리틀엔디언 정수인 삼각형 개수, 그리고 삼각형마다 32비트 부동소수점 열두 개 — 단위 법선과 꼭짓점 셋 — 와 0이어야 하는 2바이트 속성 필드로 이루어진다. 삼각형 $N_\triangle$개면 $84+50N_\triangle$바이트이므로, 구멍판은 선분 16, 32, 64개에서 6,484, 12,884, 25,684바이트다. 두 규칙이 있다. 각 삼각형은 바깥에서 볼 때 반시계 방향으로 꼭짓점을 적고(오른손 규칙), 이웃마다 변 하나를 통째로 나눈다(꼭짓점 대 꼭짓점 규칙)(미 의회도서관). 영어 절의 코드는 구멍판을 이진 STL로 메모리 안에서 만들고, 바이트 수를 $84+50N_\triangle$과 대조하고, 방향 있는 변을 세어 두 규칙을 확인하고, 삼각형들로 메시의 부피를 계산한다. 부피가 양수라는 것은 법선이 바깥을 향한다는 뜻이다.
>
> 이 페이지를 위해 돌린 출력(macOS, Python 3.12, NumPy 2.0.2, 숫자는 기계와 무관)은 선분 16, 32, 64개에서 삼각형 128, 256, 512개, 바이트 6,484, 12,884, 25,684로 식과 정확히 같고, 세 경우 모두 닫혀 있으며, 구멍은 평평한 변 사이에서 $17.654$, $17.913$, $17.978$ mm, 부피는 정확한 $6013.0$ mm³에 대해 $5859.6$, $5974.4$, $6003.4$ mm³다.
>
> 메시의 부피는 모든 $n$에서 솔리드보다 작다. 바깥 테두리가 현으로 잃는 것이 구멍이 돌려주는 것보다 크기 때문이다. 내보내기 대화상자는 대개 선분 수 대신 현 높이나 각도를 묻는데, 어느 쪽이든 $n$을 정한다. 선분 67개면 판은 삼각형 536개, 26,884바이트다.

### 3. 공차와 끼워맞춤

**문제.** 6 mm 핀과 6 mm 구멍. 핀이 미끄러져 들어갈까, 끼어서 안 들어갈까, 덜걱거릴까? 도면에는 6과 6이라고 적혀 있지만, 각 부품이 6에서 얼마나 벗어나도 되는지 알기 전에는 셋 중 무엇이라고도 말할 수 없다.

**핵심 생각.** 정확한 크기로 만들어지는 부품은 없으므로, 도면의 모든 치수는 범위다. H7로 리밍한 6 mm 구멍은 $6.000$에서 $6.012$ mm 사이 어디든 될 수 있고, g6로 연삭한 6 mm 핀은 $5.988$에서 $5.996$ mm 사이 어디든 될 수 있다. 둘이 어떻게 맞춰지는지는 가장 빡빡한 쌍 — 가장 작은 구멍과 가장 큰 핀 — 과 가장 헐거운 쌍이 정한다.

> **끼워맞춤의 정의.** **끼워맞춤**(fit)은 *구멍의 공차역과 축의 공차역 사이의 관계*다. 작업대 위 한 쌍의 틈이 아니라, 그 쌍이 가질 수 있는 틈새의 전체 범위다. 그 범위의 두 끝이 세 종류를 정한다. **헐거운 끼워맞춤**(clearance fit)은 어느 조합에서나 틈이 남는다. **억지 끼워맞춤**(interference fit)은 어느 조합에서나 겹침이 남아 축을 눌러 넣어야 한다. **중간 끼워맞춤**(transition fit)은 그 사이 전부로, 어떤 두 부품이 만나느냐에 따라 작은 틈이거나 작은 겹침이다.
>
> $$c_{\min}=D_{\min}-d_{\max},\qquad c_{\max}=D_{\max}-d_{\min}$$
>
> $D$는 구멍의 크기, $d$는 축의 크기다. 그래서 $c_{\min}\ge0$이고 $c_{\max}>0$이면 헐거운, $c_{\max}\le0$이면 억지, $c_{\min}<0<c_{\max}$이면 중간 끼워맞춤이다.
>
> - **예**: F-50의 둥근 위치 결정 핀. ISO 286 표에서 6 mm H7 구멍은 $+12/0$ µm, g6 핀은 $-4/-12$ µm이므로 $c_{\min}=0-(-4)=4$ µm, $c_{\max}=12-(-12)=24$ µm, 헐거운 끼워맞춤이다. 블록은 손으로 들어 올렸다 다시 내려놓을 수 있고, 구멍의 중심은 핀의 중심에서 많아야 12 µm 벗어난다(§7).
> - **비예**: "16 mm 구멍에 16 mm 핀". 호칭 치수가 같다는 것은 아무것도 말해 주지 않는다. 16 mm에서 H7/g6는 6–35 µm의 헐거운 끼워맞춤이고 H7/p6는 0–29 µm의 억지 끼워맞춤이다. S1의 쌍은 대신 틈새로 이름을 얻는다 — 16에 18, $\Delta=2$ mm, 볼트 틈새 끼워맞춤이다([[05-construction-robotics/construction-manipulation|건설 9]]).
> - **왜 중요한가**: 고정구의 반복성은 위치결정구의 틈새 범위이고, 압입한 핀이 붙잡는 힘은 자리의 겹침 범위다. 한 번 잰 틈 하나를 가정한 설계는 우연히 잰 부품에 맞춘 설계다.

**ISO 286 읽는 법.** 공차역의 기호는 글자 하나와 숫자 하나다. 숫자는 등급 — IT01부터 IT18까지 스무 개(RoyMech) — 으로, 크기 범위마다 공차역의 폭을 정한다. 3–6 mm에서 IT7은 12 µm, IT6는 8 µm다. 글자는 공차역이 호칭 치수에 대해 어디 앉는지를 정하며, 구멍은 대문자, 축은 소문자다. H 구멍의 아래 한계는 호칭 치수 그 자체이고, 그래서 끼워맞춤 대부분이 H 구멍을 기준으로 짜인다. 흔한 조합은 메뉴처럼 읽힌다. H7/g6 미끄럼, H7/h6 위치 결정 헐거움, H7/k6 약간 억지인 위치 결정, H7/p6 위치 결정 억지. 6 mm에서 H7/k6는 억지 9 µm에서 틈새 11 µm까지의 중간 끼워맞춤이다. 숫자는 기억이 아니라 표에서 읽는다. 공차역이 크기 범위마다 달라지기 때문이다.

**함정: 출력한 구멍은 끼워맞춤이 아니다.** 이 페이지의 프린터는 수직 구멍을 모델보다 $0.2$ mm 작게 뽑는다(§4). 6 mm 구멍의 H7 공차역 전체의 $0.2/0.012=17$배다. 그러니 프린터에서 나온 그대로의 구멍은 어느 것도 ISO 끼워맞춤이 아니다. 출력 부품이 핀에 자리를 맞춰야 한다면 출력 뒤에 드릴이나 리머로 구멍을 다듬거나, 금속 부시를 압입하거나, 끼워맞춤을 포기하고 S1의 2 mm처럼 틈새를 설계한다.

### 4. FDM 출력: 층, 방향, 구멍, 재료

**문제.** 첫 출력은 예측할 수 있는 세 가지로 실패한다. 부품이 층 경계를 따라 부러지거나, 구멍이 나사보다 작게 나오거나, 겉모양보다 훨씬 낭창거린다. 셋 다 부품이 만들어지는 방식에서 온다.

**핵심 생각.** 용융 적층(FDM) 프린터는 부품을 층의 더미로 짓는다. 각 층은 뜨거운 노즐이 그리는 플라스틱 가닥, 곧 **로드**(road)들이다. 모든 윤곽을 두르는 **외벽**(perimeter), 부품의 윗면과 아랫면을 덮는 **상하면 스킨**(skin), 그리고 속을 성기게 채우는 **내부 채움**(infill)이다. 메시를 이런 공구 경로로 바꾸는 프로그램이 **슬라이서**(slicer)다. 각 로드는 아래층과 둘 다 뜨거울 때 용착되는데, 그 용착부는 로드 자체보다 약하다. 그래서 부품은 층을 따라서는 강하고 층 사이로는 약하다. 합판의 베니어를 면끼리 붙여 쌓은 것과 비슷하다. Protolabs Network의 설계 안내서는 층 평면 안의 인장강도를 적층 축 Z 방향의 보통 4–5배로 적고, 이 페이지의 50과 12 MPa도 그 범위 안에 있다.

> **출력 이방성의 정의.** **출력 이방성**(print anisotropy)은 필라멘트가 아니라 *출력한 부품의 성질*이다. 부품의 강성과 강도가 응력의 방향이 층과 이루는 관계에 따라 달라진다. 정의 조건 셋. 부품은 **층 안의 로드들로 지어지고**, 각 층은 아래층과 부분적인 재용융으로만 붙어 있다. **층간 결합은 로드보다 약하다**: 층을 떼어 놓는 방향의 응력은 로드를 따라 받는 응력의 일부만으로도 부품을 부러뜨리고, 층을 가로지르는 강성도 더 낮다. 그리고 **방향은 슬라이싱할 때 정해진다**: 부품을 출력하는 사람이 고르므로, 같은 CAD 파일이 눕혀 뽑을 때와 세워 뽑을 때 다른 부품이 된다.
>
> $$u=\frac{\sigma}{\sigma_{\text{allow}}},\qquad \sigma=\frac{M}{bh^2/6}$$
>
> $u$는 이용률, $\sigma$는 팔 뿌리의 휨응력, $M$은 뿌리 모멘트, $bh^2/6$은 단면계수다. 그래서 같은 $\sigma$라도 $\sigma_{\text{allow}}$가 $\sigma_\parallel$(응력이 층 평면 안을 달림)인지 $\sigma_\perp$(응력이 층을 떼어 놓음)인지에 따라 $u$가 달라진다.
>
> - **예**: 어깨를 전류 한계까지 쓰는 P2의 격한 움직임(계산 절, 3단계)에서 B-60 뿌리의 $\sigma=2.00$ MPa. 눕혀 출력하면 $u=2.00/50=0.04$다. 세워 출력하면 모든 층 경계가 팔을 가로질러 $u=2.00/12=0.17$이 되고, 탄성계수가 $3.0$에서 $2.4$ GPa로 떨어져 팔이 25% 더 처진다.
> - **비예**: 필라멘트 데이터시트의 강도를 부품의 강도로 쓰는 것. 그 값은 재료를 길이 방향으로 당긴 값인데, 세워 출력한 부품은 바로 그 방향으로는 하중을 받지 않는다.
> - **왜 중요한가**: 방향은 설계가 끝난 뒤, 하중이 어디로 가는지 모르는 사람이나 슬라이서 기본값이 정한다. 그러니 도면이나 파일 이름이 방향을 말해 주어야 한다.

**방향 고르는 법.** 순서대로 네 규칙. 인장과 휨은 층 평면 안에 둔다 — 안내서의 조언도 힘을 따라 층이 달리도록 놓으라는 것이다. 둥글어야 하는 구멍은 축을 수직으로 둔다. 수직 구멍은 모든 층에서 원이지만, 수평 구멍의 위쪽은 허공을 건너 다리를 놓아야 하고, 안내서는 5 mm가 넘는 다리가 처진다고 적는다. 돌출부는 수직에서 약 45° 안으로 둔다. 안내서가 서포트 없이 뽑을 수 있다고 보는 보통의 한계다. 그리고 평평해야 하는 면 — 물림면, 데이텀(§7) — 을 베드에 둔다. B-60은 눕힌다. $80\times20$ mm 면을 아래로, 휨응력은 층 안에, 나사 구멍은 수직으로, 물림면은 베드 위로.

**구멍은 작게 나온다. 여유를 한 번 재 둔다.** 출력한 수직 구멍이 작아지는 이유는 둘이고, 둘이 더해진다. 메시가 이미 원을 현으로 잘라 놓았고(§2), 노즐이 구멍의 외벽을 그릴 때 새 로드를 아래층에 눌러 붙이면서 로드가 납작하게 퍼져 구멍 안쪽으로 밀려든다. 얼마나 작아지는지는 프린터, 슬라이서, 구멍 크기, 재료에 따라 다르고, 지름이 중요한 곳이라면 작게 출력한 뒤 드릴로 맞추라는 것이 안내서의 조언이다(Protolabs Network). 그러니 3, 4, 6, 10 mm 구멍을 뚫은 시험편을 출력하고, 핀 게이지나 드릴 자루로 재서, 그 차이를 §1의 `hole_allowance`에 넣는다. 이 페이지의 프린터는 $0.2$ mm를 잃으므로, B-60의 M3 여유 구멍은 $3.4+0.2=3.6$ mm로 모델링해야 3.4로 나온다.

**재료.** 연구용 하드웨어는 대부분 네 재료로 된다. 표는 Prusa의 재료 안내서에서 온 정성적 비교이고, 그들의 숫자 말고는 숫자를 넣지 않았다.

| 재료 | 출력 | 열 | 인성 | 습기와 유해 물질 | Prusa가 드는 쓰임 |
|---|---|---|---|---|---|
| PLA | 가장 쉽다. 거의 뒤틀리지 않는다 | 60 °C 위에서 물러지고 변형된다 | 취성: 충격에 층을 따라 부러지거나 조각난다 | 자외선에 열화된다 | 세밀한 모형, 빠른 시제품 |
| PETG | 쉽다. 실이 늘어진다. 베드에 강하게 붙는다 | 80 °C 아래의 실내와 대부분의 실외 | 질기고 튼튼하다. 층 접착이 좋다 | 물과 습기에 강하다 | 기계 부품, 홀더, 클램프 |
| ABS | 많이 뒤틀린다. 인클로저가 필요하다 | 고온에 잘 견딘다 | 질기다. 기계적 응력을 받는 부품용 | 스티렌 증기: 환기되는 방에서 | 열과 기계적 강도가 필요한 기술 부품 |
| 나일론(PA) | 뒤틀린다. 인클로저가 크게 돕는다 | 고온에 강하다 | 기계적 강도가 매우 좋고 마모에 강하다 | 흡습성이 매우 크다 — 잘못 보관하면 무게의 10%까지 물을 먹으니 말려서 쓴다. 냄새가 강하고 초미세입자가 나온다: 환기한다 | 열·화학·기계적 강도가 필요한 기술 부품 |

**함정: 열, 크리프, 채움.** PLA는 60 °C 위에서 물러지고, 모터 옆이나 여름 차 안의 브래킷은 그 온도에 닿는다. 지속 하중을 받는 플라스틱은 *크리프*(creep)한다 — 하중이 그대로여도 천천히 계속 변형한다. 인서트 제조사가 금속 나사산을 권하는 이유가 이것이고(§5), 그래서 B-60의 처짐은 몇 주에 걸쳐 자라고 보정도 따라서 틀어진다. 그리고 내부 채움이 성기면 부품이 겉모양보다 훨씬 덜 단단하다. 휨은 바깥 섬유가 받는데, 그때 바깥 섬유는 스킨과 외벽뿐이기 때문이다. 강성이 중요한 부품은 속을 꽉 채워 출력한다.

> [!note]- 더 깊이 · Deeper
> 채움이 치르는 값. 채움이 성기고 위아래 스킨의 두께가 $t$이면 B-60의 단면은 거의 속 빈 상자이므로, 채움 자체를 무시하면 $I\approx b\,\big(h^3-(h-2t)^3\big)/12$이다. 스킨이 $t=0.8$ mm(0.2 mm 층 넷)이면 $20\,(6^3-4.4^3)/12=218.0$ mm⁴로, 꽉 찬 단면의 360 mm⁴에 대해 강성의 61%다. 같은 겉모양, 같은 재료인데 처짐과 기울기가 65% 커진다.

### 5. 체결: 여유 구멍, 출력한 나사산, 인서트, 예압

**문제.** 카메라는 B-60에서 여러 번 떼었다 다시 달아야 하고, 브래킷은 공구에 붙어 꿈쩍하지 않아야 한다. 출력한 플라스틱에 곧장 박은 나사는 어느 쪽도 오래 버티지 못한다.

**핵심 생각.** 나사는 두 부품을 조여서 잇는다. 머리 쪽 부품의 **여유 구멍**(clearance hole) — 나사보다 커서 나사가 물리지 않는 구멍 — 을 지나, 다른 부품의 **나사산**을 당긴다. 금속의 탭 구멍, 너트, 금속 인서트가 그 나사산이다. (미터 나사는 호칭 지름으로 부른다. M3는 나사산 바깥지름이 3 mm다.) 나사는 조일 뿐 위치를 정하지 않는다. 조임이 걸리기 전까지는 여유 구멍의 틈만큼 부품이 움직일 수 있기 때문이다(§7). 그래서 B-60의 물림 쪽에는 나사산이 필요 없다. M3 나사 두 개가 그것을 지나 P2 공구의 탭 구멍으로 들어간다.

**출력한 나사산이 뭉개지는 이유와 인서트가 하는 일.** 출력한 구멍에 박은 나사는 플라스틱에 제 나사산을 파는데, 그 나사산은 세 가지로 실패한다. 금속 나사산처럼 조이면 뭉개지고, 나사를 뺄 때마다 닳고, 하중 아래서 크리프해 체결이 풀린다. 인서트 제조사가 금속 나사산을 권하는 이유도 정확히 이것이다. 금속 나사산이면 플라스틱에 박은 나사라면 뭉개졌을 나사산을 뭉개지 않고 제대로 된 체결 토크를 걸 수 있고, 나사산의 하중 경로 전체에서 크리프에 버틴다(SPIROL). **열압입 인서트**(heat-set insert)는 안에 나사산이 있고 겉에 널링이 있는 황동 슬리브다. 제조사가 정한 크기의 구멍에 달궈서 눌러 넣으면 둘레의 플라스틱이 녹아 널링 사이로 흘러들었다가 다시 굳는다. SPIROL이 드는 조건은 알맞은 구멍 크기, 인서트 둘레의 충분한 벽 두께, 인서트의 빈틈을 채울 만큼의 용융이다. B-60은 카메라 나사를 위해 먼 쪽 끝에 인서트 두 개를 넣는다.

**예압, 한 문단으로.** 조인 체결부를 붙잡고 있는 것은 **예압**(preload)이다. 조인 나사가 품고 있는 인장력, 그리고 그와 같은 크기로 두 부품을 눌러 붙이는 힘이다. 예압은 체결 토크로 정해지는데, 토크 대부분은 마찰로 사라진다. Bolt Science는 실제로 볼트를 늘이는 몫을 보통 10–15%로, 머리 아래 마찰에 드는 몫을 약 절반으로 본다. 실용 규칙은 마찰을 모두 너트 계수 $K$ 하나에 몰아넣고, 마른 강철이면 $K$는 약 0.2다(Engineering ToolBox).

$$F=\frac{T}{K\,d}$$

그래서 예압 $F$는 토크 $T$와 호칭 지름 $d$에서 나온다. 그리고 $K$가 윤활과 표면에 따라 움직이므로, 토크 렌치로 조여도 예압은 가장 큰 것이 가장 작은 것의 1.6배까지 퍼진다(Bolt Science). B-60에서 M3 물림 나사를 $0.5$ N·m로 조이면 $F=0.5/(0.2\times0.003)=833$ N로, 카메라 무게 $0.98$ N의 약 850배다. 그런데 나사 머리는 바깥 5.5 mm, 안쪽 3.4 mm의 고리 면적(이 페이지의 숫자) $14.7$ mm²로 출력한 플라스틱을 누른다. 압력은 $833/14.7=56.8$ MPa로, 이 페이지가 출력 PLA의 로드 방향 강도로 준 50 MPa마저 넘는다. 그래서 머리 아래 플라스틱은 눌려 뭉개질 수 있고 크리프는 반드시 일어나며, 예압도 함께 빠져나간다. 7 mm 와셔를 넣으면 면적이 $29.4$ mm²로 두 배가 되어 압력이 $28.3$ MPa로 반이 되고, 나머지는 토크를 줄여 해결한다. 함정은 출력한 나사산에 "손맛으로 꽉" 조이는 것이다. 아무도 모르는 예압을, 뭉개지거나 크리프할 나사산이 떠받치게 된다.

### 6. 센서 브래킷의 강성과 질량

*한 문장으로:* 센서 브래킷은 강성 — 보정할 때와 쓸 때 사이에 센서가 돌아가는 각도, 그리고 브래킷이 떨리는 진동수 — 으로 크기가 정해지고, 강도가 한계가 되는 일은 거의 없다.

**문제.** 월요일에 보정한 카메라가 화요일에는 핀을 0.5 mm 어긋나게 보고, 빠르게 움직였다 멈출 때마다 영상이 잠깐 떨린다. 부러진 것은 없다. 브래킷이 휘었고, 그다음 진동했다.

**핵심 생각.** 카메라가 보는 것은 끝이 얼마나 처졌는지가 아니라 *각도*에 달려 있다. 아주 작은 기울기도 대상까지의 거리를 곱하면 거기서는 큰 오차다. 그리고 카메라를 단 브래킷은 스프링에 매단 질량이라, 갑자기 멈추면 떨린다. 보 이론은 이미 익숙한 것이다 — 길이 $L$의 캔틸레버에 끝 하중 $F$가 걸리면 끝이 $\delta=FL^3/(3EI)$ 처지고, 끝이 $\theta=FL^2/(2EI)=3\delta/(2L)$ 돌아가며, 끝 강성은 $k=3EI/L^3$다. 새로운 것은 카메라가 이것들로 무엇을 하느냐다.

> **조준 오차의 정의.** 장착된 센서의 **조준 오차**(pointing error)는 *대상 위의 길이*다. 보정할 때와 쓸 때 사이에 마운트가 변형되면서 센서가 보는 점이 얼마나 옮겨 가는가다. 정의 조건 셋. 센서는 **강체이고 마운트 끝과 함께 돈다**. 그래서 시선이 마운트 끝의 기울기만큼 흔들린다. 셈에 드는 것은 **보정한 자세와 쓰는 자세 사이의 변화**다. 보정은 그때 있던 변형을 모두 흡수하기 때문이다. 그리고 각도는 **작다**. 그래서 기울기 $\theta$는 보는 점을 $D\theta$만큼 옮긴다.
>
> $$e=\delta_\perp+D\,\theta$$
>
> $e$는 대상에서의 오차, $D$는 대상까지의 거리, $\theta$는 마운트 끝 기울기의 변화, $\delta_\perp$는 끝 변위 가운데 시선을 가로지르는 성분이다. B-60은 팔이 직각으로 뻗은 채 공구 방향을 보므로 처짐이 시선을 따라 생겨 $\delta_\perp=0$이다. 팔 방향을 보는 카메라라면 $\delta_\perp=\delta$다.
>
> - **예**: 팔이 수직일 때 — 카메라 무게가 팔을 따라 걸려 휨이 없을 때 — 보정하고, 팔이 수평일 때 쓰는 B-60. P2의 공구가 수평에서 핀을 향해 아래로 돌아설 때가 그렇다. 새로 생긴 기울기 $\theta_g=1.635$ mrad는 보는 점을 $e=0.40\ \mathrm{m}\times1.635\times10^{-3}=0.654$ mm 옮겨 허용치 $0.5$ mm를 넘는다(계산 절, 1–2단계). 기울기의 지렛대 $3D/(2L)=10$이 그것을 처짐 65 µm의 열 배로 만든다.
> - **비예**: 보정할 때와 쓸 때의 방향이 같은 경우의 같은 처짐. 보정이 다른 것과 함께 그것도 재 두었으므로 값을 치르지 않는다. 그리고 사용성 검토처럼 $\delta=FL^3/(3EI)$를 한계와 비교하는 것은 값을 치르는 경우에 대해 아무것도 말해 주지 않는다.
> - **왜 중요한가**: 마운트의 기울기는 자세에 따라 변하는 손–눈 변환의 회전 오차이고, [[04-robotics/geometric-perception-calibration|3.5 §3]]이 보이듯 회전 오차는 거리와 함께 자란다. 병진 오차는 그대로다.

> **브래킷 1차 고유 진동수의 정의.** 센서 브래킷의 **1차 고유 진동수**(first natural frequency)는 *센서를 밀었다 놓았을 때 마운트 위에서 흔들리는 빠르기*다. 팔의 제어기가 아니라 마운트와 그 짐의 성질이다. 정의 조건 넷. **모드 하나가 지배한다**: 끝에 모인 센서 질량이 팔 자신의 질량보다 커서, 브래킷이 스프링 하나에 매단 질량 하나처럼 움직인다. 변형은 **선형 탄성**이다. **밑단이 브래킷보다 훨씬 단단하다**: 그래서 공구는 함께 움직이지 않는다. 물림부가 무르거나 나사가 풀리면 진동수는 식보다 낮아진다. 그리고 **감쇠가 작다**: 그래서 거의 고유 진동수로 흔들리고 천천히 잦아든다.
>
> $$f_n=\frac{1}{2\pi}\sqrt{\frac{k}{m}}=\frac{1}{2\pi}\sqrt{\frac{g}{\delta_g}}$$
>
> $k=3EI/L^3$는 끝 강성, $m$은 센서 질량, $\delta_g$는 센서 자기 무게에 의한 처짐이다. 둘째 꼴은 $k=mg/\delta_g$이기 때문에 성립하고, 그래서 브래킷의 진동수는 정적 처짐에서 곧바로 읽힌다. 바닥 진동 검토의 발상과 같되, 여기서는 질량이 모두 끝에 있다.
>
> - **예**: B-60은 $\delta_g=65.4$ µm이므로 $f_n=\frac{1}{2\pi}\sqrt{9.81/(65.4\times10^{-6})}=61.64$ Hz이고, 팔이 8 mm면 $94.90$ Hz다.
> - **비예**: 팔 제어 루프의 고유 진동수. 캡스톤의 계산 토크 루프는 관절 오차마다 $\omega_n=10$ rad/s, 곧 $1.59$ Hz를 준다([[04-robotics/capstone-panel-contact|26. 캡스톤]]). 그것은 P2가 브래킷을 움직이는 빠르기이지, 브래킷이 떨리는 진동수가 아니다.
> - **왜 중요한가**: 브래킷의 진동수가 멈출 때마다 영상이 어떻게 떨리는지, 그리고 50 Hz로 샘플링하는 카메라가 그 떨림을 무엇으로 보는지를 정한다.

**카메라가 진동을 보는 방식.** 느린 팔 움직임은 해가 없다. 캡스톤의 루프는 브래킷을 $1.59$ Hz로 움직이는데, 이는 8 mm B-60의 $94.90$ Hz보다 60배 낮아서 브래킷은 그냥 따라간다. 급정지는 다르다. 휘어 있던 자리에서 카메라를 놓아 버리므로 카메라는 $f_n$으로 흔들리고, $e^{-\zeta\omega_nt}$로 잦아든다. 그리고 카메라는 $f_s=50$ Hz로 샘플링하므로 $f_n$의 진동을 앨리어스 $|f_n-kf_s|$에서 본다([[02-foundations/signal-processing|6. §2]]). 8 mm 팔의 $94.90$ Hz는 $|94.90-2\times50|=5.10$ Hz로 나타난다. 영상 속 핀이 천천히 부드럽게 헤매는 모습이라, 추적기는 핀이 실제로 움직인 것과 구별하지 못한다. 3단계의 출발만큼 격한 정지 뒤로 약 12프레임이 그렇다(계산 절, 4단계).

**브래킷을 단단하게 만드는 법.** 식이 손잡이의 순위를 매겨 준다. 기울기는 $L^2/(Eh^3)$로 가므로 두께가 가장 센 손잡이다 — 6 mm에서 8 mm로 가면 $(6/8)^3=0.42$배가 된다 — 그다음이 길이, 그다음이 재료다. 리브나 플랜지를 붙이면 단면이 T나 L이 되어 적은 질량으로 $I$가 몇 배가 된다. 센서가 가벼우면 기울기가 비례해 줄고 $f_n$은 제곱근만큼 오른다. 그리고 체결부도 브래킷의 일부다. 크리프한 플라스틱에 박힌 나사 둘(§5)은 보 공식이 보지 못하는 힌지가 된다.

> [!note]- 더 깊이 · Deeper
> 두 가지 보정. 팔 자신의 질량은 제 몸의 $33/140$만큼 $m$에 더해진다. 끝 하중 처짐 모양 $y(\xi)=(3\xi^2-\xi^3)/2$로 한 레일리 추정이고, 그 모양의 제곱을 팔 전체에 걸쳐 평균하면 $33/140=0.2357$이며, 계산 절의 코드가 이를 확인한다. 8 mm 팔의 자유 길이 60 mm는 교과용 밀도 $1.24$ g/cm³의 PLA로 $11.9$ g이므로, 카메라 100 g에 $2.8$ g을 더해 $f_n$을 1.4% 낮춘다. 그리고 진동수 $f$로 가진하면 [[02-foundations/engineering-math|0.5 §8]]의 감쇠 작은 스프링–질량은 $r=f/f_n$일 때 $1/(1-r^2)$배로 증폭된다. 캡스톤의 $1.59$ Hz에서 8 mm 팔의 증폭은 $1.0003$으로 정하중과 같고, $r=1$ 근처에서는 공진한다. 브래킷이 팬, 모터의 코깅, 기어 맞물림과 진동수를 나누어 가지면 안 되는 이유다.

### 7. 고정구와 데이텀: 매 시행 같은 방식으로 부품 놓기

**문제.** 목업의 핀 블록은 한 연구 동안 걸림을 풀려고 쉰 번쯤 들렸다 다시 놓인다. 놓을 때마다 0.3 mm씩 다른 자리에 앉는다면, 그 뒤의 모든 시행이 로봇 탓이 아닌 0.3 mm의 오차를 싣고, 실험은 고정구를 재게 된다.

**핵심 생각.** 연구 실무는 같은 구성으로 다시 돌리는 것을 *반복성*(repeatability)이라 부르고, 모든 결과에 쓴 하드웨어를 밝히라고 한다([[06-research-practice/experimental-design-reproducibility|2. §6–§7]]). 그 반복성에서 하드웨어의 몫을 정하는 것이 고정구다. 부품을 늘 같은 자리에 되돌리려면, 부품이 움직일 수 있는 방법의 수만큼 — 더도 덜도 아니게 — 점을 대고, 그 점들에 단단히 밀어붙인다. 부품의 **데이텀**(datum)은 부품의 위치를 잡는 기준이 되는 면, 축, 점이고, 부품이 만나는 순서대로 부른다. 제1 데이텀 위에 내려놓고, 제2 데이텀에 대고 밀고, 제3 데이텀에 밀어 넣는다. 나사는 부품을 당겨 누를 뿐, 어디에 앉을지를 정하지 않는다.

> **3-2-1 위치 결정의 정의.** **3-2-1 위치 결정**(3-2-1 locating)은 *강체 부품을 그 자유도와 꼭 같은 수의 접점으로 위치 잡는 규칙*이다. 위치결정구를 세는 규칙이고, 클램프는 그다음에 그것을 돕는다. 정의 조건 넷. 강체 부품의 **자유도는 여섯**, 병진 셋과 회전 셋이다. 방향까지 — 각 축을 따라, 각 축 둘레로 양과 음 — 세면 Carr Lane의 고정구 설계 안내는 열둘로 센다. **제1 면의 접점 셋**은 그 면에 수직인 병진과 두 기울기를, **제2 면의 접점 둘**은 병진 하나와 제1 면 법선 둘레의 회전을, **제3 면의 접점 하나**는 마지막 병진을 없앤다. 위치결정구 여섯이 자유도를 하나씩 없애며 열두 방향 가운데 아홉을 막는다. **클램프는 부품을 위치결정구 쪽으로 민다**: 나머지 세 방향을 막되, 부품을 위치결정구에서 떼어 내지 않는다. 그리고 **중복된 위치결정구가 없다**: 일곱째 접점은 여섯 가운데 하나와 싸우거나, 어느 접점이 마침 닿느냐에 위치가 좌우되게 만든다. 면 하나, 둥근 핀 하나, 다이아몬드 핀 하나로 잡는 평평한 부품도 같은 셈이다. 면이 3, 구멍 속 둥근 핀이 2, 한 방향으로만 위치를 잡도록 옆을 깎아 낸 다이아몬드 핀이 1이다.
>
> $$\theta_{\max}=\frac{c_1+c_2}{2s},\qquad e_\perp(x)\le\frac{c_1}{2}\Big|1-\frac{x}{s}\Big|+\frac{c_2}{2}\Big|\frac{x}{s}\Big|$$
>
> $c_1$과 $c_2$는 둥근 핀과 다이아몬드 핀에서의 가장 큰 지름 틈새, $s$는 두 핀의 간격, $\theta_{\max}$는 그 틈새가 허락하는 가장 큰 회전, $e_\perp(x)$는 둥근 핀에서 $x$만큼 떨어진 점이 핀을 잇는 선을 가로질러 옮겨 가는 최대량이다. 두 핀 사이에서 그 이동은 두 핀 각자의 이동의 가중 평균이고, 핀 바깥에서는 $x$와 함께 자란다. 선을 따르는 방향으로는 둥근 핀만 작용하므로 그 방향 이동은 많아야 $c_1/2$다.
>
> - **예**: F-50. 6 mm 핀의 H7/g6는 $c_1=c_2=24$ µm를 주므로(§3) $\theta_{\max}=0.48$ mrad이고, 한가운데 $x=25$ mm의 S1 핀은 선을 가로질러 많아야 $12\,(1-0.5)+12\,(0.5)=12$ µm, 선을 따라 12 µm 옮겨 간다. 모든 앉음새를 뒤지면 둘을 합쳐 $13.9$ µm다(계산 절, 5단계).
> - **비예**: 구멍 둘에 둥근 핀 둘. 블록의 구멍 간격과 판의 핀 간격에는 저마다 공차가 있어서, 둘의 차이가 틈새보다 크면 블록이 들어가지 않고, 작으면 블록을 어느 쪽으로 밀었느냐에 따라 위치가 달라진다. 둘째 핀이 다이아몬드인 이유가 이것이다. 둥근 핀 하나와 다이아몬드 핀 하나는 구멍 둘에서 걸림 없이 위치를 잡는다(Carr Lane). 평판 위의 다리 넷도 같은 실수를 세로로 한 것이다. 부품이 그중 셋 위에서 달그락거린다.
> - **왜 중요한가**: 고정구의 위치 오차는 모든 시행에 들어가고, 식은 어디에 공을 들여야 하는지 알려 준다. Carr Lane의 말대로 위치결정구를 되도록 멀리 벌리고, 중요한 것은 그 사이에 둔다.

**함정: 볼트는 조이고, 핀이 위치를 정한다.** F-50의 블록을 6.6 mm 여유 구멍의 M6 나사 두 개만으로 잡으면, 다시 놓을 때마다 $0.3$ mm의 놀이 안 어디든 앉을 수 있다. S1의 핀이 $0.300$ mm까지 옮겨 간다. 핀 위에 놓으면 $0.014$ mm다. 나사는 여전히 필요하다 — 블록을 판의 윗면, 곧 제1 데이텀에 당겨 누른다 — 하지만 위치는 정하지 않으며, 그 힘은 블록을 위치결정구 쪽으로 눌러야지 가로질러 밀면 안 된다.

**정확도가 아니라 반복성.** 블록 속 핀의 가공 위치 $\pm0.05$ mm와 작업대 위 판의 자리는 고정 오차다. 매 시행 똑같으므로, 로봇으로 핀을 한 번 짚어 재면 예산에서 사라진다. 고정구가 묶어 두어야 할 것은 시행마다 바뀌는 것 — 핀의 틈새 — 이고, 세션 사이에 분해하는 이음부라면 어디든 제 위치 결정 핀이 있어야 한다. [[05-construction-robotics/site-engineering|2.5 §5]]의 사다리에서 목업은 S1 예산의 팔·공구·부품 항을 재고, 고정구의 시행별 오차는 목업이 더하는 단 하나의 항이다.

### 대상으로 한 번 끝까지 · Worked case

리그 자신의 숫자로 다섯 단계를 간다. 넷은 B-60, 하나는 F-50이다. §6의 보 공식, §3·§4·§6·§7의 정의, 그리고 P2의 숫자 셋만 쓰며, 영어 절의 코드가 모든 숫자를 찍어 확인한다.

**1단계 — 처짐과 기울기.** B-60의 팔은 $20\times6$ mm이므로 $I=bh^3/12=20\times6^3/12=360$ mm⁴이고, 눕혀 출력했으니 탄성계수는 $E_\parallel=3000$ N/mm²다. 끝 강성은 $k=3EI/L^3=3\times3000\times360/60^3=15.0$ N/mm. 카메라 무게 $mg=0.981$ N은 끝을 $\delta_g=0.981/15.0=0.0654$ mm 처지게 하고 $\theta_g=3\delta_g/(2L)=3\times0.0654/120=1.635$ mrad 돌린다.

**2단계 — 핀에서 치르는 값, 그리고 고치기.** 팔이 수직일 때 보정하고 수평일 때 쓰면(§6) 카메라는 $\theta_g$만큼 돌아간다. 처짐은 시선을 따라 생기므로 $\delta_\perp=0$이고, 오차는 모두 기울기에서 온다.

$$e=D_w\,\theta_g=400\ \mathrm{mm}\times1.635\times10^{-3}=0.654\ \mathrm{mm}$$

기울기는 카메라를 중심으로 시선을 흔들고, 400 mm 앞에서 그 흔들림은 400 mm에 각도를 곱한 만큼이기 때문이다. 허용치 $0.5$ mm보다 31% 크다. 기울기는 $h^{-3}$에 비례하므로 허용치를 지키는 가장 얇은 팔은 $h=6\,(0.654/0.5)^{1/3}=6.56$ mm다. 6.56이 아니라 8 mm를 고른다. 물림부와 §4·§5의 크리프가 식에 없는 유연성을 더하기 때문이다. 그러면 $I=853.3$ mm⁴, $k=35.56$ N/mm, $\delta_g=27.6$ µm, $\theta_g=0.690$ mrad, $e=0.276$ mm로 허용치보다 45% 작다.

**3단계 — 출력 방향과 강도.** 세워 출력하면 팔의 응력이 층을 가로질러 흐르고 탄성계수는 $E_\perp=2.4$ GPa이므로, 모든 처짐이 $3.0/2.4=1.25$배가 된다. 6 mm 팔의 오차는 $0.818$ mm, 8 mm 팔은 $0.345$ mm로 여전히 허용치 안이다. 이제 격한 하중 하나. P2의 카탈로그 자세 — 전완이 위를 향하고 B-60이 수평 — 에서 팔꿈치에는 힘을 주지 않고 어깨 구동기만 전류 한계 80 N·m([[04-robotics/actuators-drives|10.5 §3]])로 밀게 하자. 거기서 중력을 버티는 $19.62$ N·m를 빼면, 어깨에서 1 m 떨어진 말단을 위로 $60.38$ N의 힘으로 민다. 말단의 $y$ 방향 겉보기 질량은 $\Lambda_y=2$ kg(0.6)이므로

$$a=\frac{60.38\ \mathrm{N}}{2\ \mathrm{kg}}=30.19\ \mathrm{m/s^2},\qquad a+g=40.00\ \mathrm{m/s^2}=4.08\,g$$

카메라는 중력과 가속도를 함께 느끼기 때문이다. 뿌리 모멘트는 $0.10\times40.00\times0.060=0.240$ N·m, 응력은 $0.240/(bh^2/6)$로 6 mm 팔이 $2.00$ MPa, 8 mm 팔이 $1.12$ MPa다. $\sigma_\parallel=50$ MPa에 대한 여유는 25와 44, $\sigma_\perp=12$ MPa에 대해서는 6.0과 10.7이다. 팔의 크기를 정한 것은 강성이고, 강도는 근처에도 오지 않았다. 세워 출력하면 강성이 20% 줄어 처짐이 25% 늘고, 강도 여유는 $50/12=4.2$분의 1로 줄어든다. 그 손해는 카메라를 들고 있을 때가 아니라 팔이 어딘가에 부딪힐 때 드러난다.

**4단계 — 진동, 그리고 카메라가 보는 것.** 8 mm 팔의 고유 진동수는 $f_n=\frac{1}{2\pi}\sqrt{9.81/(27.6\times10^{-6})}=94.90$ Hz다. 3단계의 출발만큼 격하게 멈추면 느끼는 가속도가 거의 한순간에 $30.19$ m/s² 바뀐다. 감쇠가 작은 스프링–질량은 하중이 갑자기 바뀌면 새 정지 위치를 중심으로, 정적 처짐이 바뀐 만큼의 진폭으로 흔들린다. 그래서 카메라는 $(30.19/9.81)\times0.690=2.12$ mrad의 기울기로 진동한다. 핀에서 $0.849$ mm다. $\zeta=0.02$이면 진동은 $e^{-\zeta\omega_nt}$로 잦아들고 $\zeta\omega_n=0.02\times2\pi\times94.90=11.93$ s⁻¹이므로, $0.05$ mm 아래로 내려가는 데

$$t=\frac{\ln(0.849/0.05)}{11.93\ \mathrm{s^{-1}}}=0.237\ \mathrm{s}=11.9\ \text{frames at }50\ \mathrm{Hz}$$

가 걸린다. 한 프레임이 20 ms이기 때문이다. 그 프레임들 동안 카메라는 $94.90$ Hz의 진동을 $|94.90-2\times50|=5.10$ Hz로 본다. 추적기가 움직임으로 보고할 핀의 느린 헤맴이다. 급정지 뒤의 처음 12프레임은 버리거나, 덜 급하게 멈춘다.

**5단계 — F-50의 위치 오차.** 블록은 판의 윗면(접점 3), 둥근 핀(2), 다이아몬드 핀(1)에 앉는다. 여섯이고 중복이 없다. 두 핀 모두 H7/g6로 구멍에 맞으므로 $c_1=c_2=24$ µm가 최대이고(§3), 블록이 돌 수 있는 최대 각은

$$\theta_{\max}=\frac{24+24}{2\times50\,000}=0.48\ \mathrm{mrad}$$

다. 각 구멍이 제 핀에서 틈새의 절반까지, 서로 반대쪽으로 벗어날 수 있기 때문이다. 한가운데의 S1 핀은 핀을 잇는 선을 가로질러 많아야 12 µm, 선을 따라 12 µm 움직이지만, 둘을 합치면 $12\sqrt2=17$ µm가 아니라 $13.9$ µm다(코드). 둥근 핀의 틈새는 원이어서, 선을 따라 12 µm를 다 벗어난 구멍 중심은 선을 가로질러서는 벗어날 수 없고, 그때 한가운데 점을 가로로 옮기는 것은 다이아몬드 핀 하나뿐이라 6 µm에 그치기 때문이다. 그리고 M6 나사만으로 잡으면 $0.300$ mm다. 이것을 S1에 대 본다. 구멍의 반경 틈새는 $(18-16)/2=1$ mm이므로 핀은 그 1.4%, 나사는 30%를 쓴다. 건설 9의 5단계가 따져 본 정밀 끼워맞춤, $\Delta=0.2$ mm와 반경 $0.1$ mm에 대면 핀은 14%, 나사는 틈새 전체의 세 배를 쓴다. 나사만으로는 핀이 들어가느냐 마느냐를 고정구가 정해 버린다. 블록 속 핀의 가공 위치 $\pm0.05$ mm는 매 시행 같으니, 로봇으로 한 번 짚어 두면 예산에서 빠진다.

영어 절의 코드는 §2의 코드 뒤에 같은 노트북으로 이어 돌아가고, 이 페이지를 위해 돌린 출력(macOS, Python 3.12, NumPy 2.0.2)은 위의 숫자를 모두 그대로 찍는다. 6 mm 눕힘 $0.654$ mm·$61.64$ Hz, 6 mm 세움 $0.818$ mm·$55.13$ Hz, 8 mm 눕힘 $0.276$ mm·$94.90$ Hz, 8 mm 세움 $0.345$ mm·$84.88$ Hz, 가장 얇은 팔 $6.56$ mm, 가속도 $30.19$ m/s²와 느끼는 $40.00$ m/s², 뿌리 응력 $2.00$·$1.12$ MPa, 진동 $0.849$ mm와 $11.9$프레임과 $5.10$ Hz, 팔 움직임의 증폭 $1.0003$, 레일리 몫 $0.2357$, 그리고 핀 위 $13.9$ µm와 나사만 $0.300$ mm다.

### 8. 다른 공정들, 그리고 작업장에서 안전하게

**문제.** 프린터로 모든 것을 만들 수는 없다. 정확한 구멍이 난 평판, 리밍한 핀 구멍이 있는 금속 블록, 리그 전체를 받칠 단단한 받침이 그렇다. 나머지 대부분은 세 공정이 맡고, 공정마다 제대로 잡아야 할 숫자가 하나씩 있다.

**레이저 커팅**은 아크릴이나 합판 같은 판재를 2D 경로를 따라 빠르고 반복성 있게 자른다. 빔은 좁은 띠, 곧 **커프**(kerf)를 태워 없애고, 자른 가장자리는 경로 양쪽으로 커프의 절반만큼 떨어져 생긴다. 그래서 호칭 경로대로 자른 구멍은 커프 하나만큼 커지고, 외곽은 커프 하나만큼 작아진다. 구멍은 안쪽으로, 외곽은 바깥쪽으로 커프의 절반만큼 경로를 옮긴다. 스탠퍼드의 한 연구실 노트는 아크릴과 합판에서 0.2–0.25 mm의 커프를 적는다. $0.2$ mm라면 호칭 경로대로 자른 S1의 18 mm 구멍은 $18.2$ mm가 된다. PVC는 절대 자르지 않는다. 염화수소가 나오는데, MIT의 안전 부서는 이를 극히 위험하다고 하고, 레이저 제조사 Epilog는 같은 기체가 기계를 되돌릴 수 없게 망가뜨린다고 경고한다.

**CNC 가공**은 프로그램에 따라 금속 덩어리를 깎아 낸다. F-50의 블록과 판이 이렇게 만들어지고, 끼워 맞춰야 할 구멍은 작게 뚫은 뒤 리밍한다. 가공 기술자에게는 형상을 위한 STEP 파일과, STEP이 말하지 않는 것 — 끼워맞춤, 데이텀, 중요한 공차(§3, §7) — 을 적은 도면이 필요하다. 다른 면을 깎으려고 다시 물릴 때마다 새 셋업이고 그 셋업마다 제 위치 오차가 있으므로, 한쪽에서만 깎도록 설계한 부품이 더 싸고 더 정확하다.

**알루미늄 압출 프레임**은 T슬롯 프로파일을 브래킷과 슬롯 너트로 이은 것이다. 리그의 받침이나 카메라 갠트리를 오후 한나절에 짜고 다음 달에 다시 짠다. 부재는 보다. 양단 단순 지지된 600 mm 부재가 $I=7\times10^4$ mm⁴, $E=70$ GPa(중간 크기 프로파일의 교과용 숫자)라면, 가운데 100 N에 $FL^3/(48EI)=100\times600^3/(48\times70\,000\times70\,000)=0.092$ mm 처진다. 프레임의 유연성은 대개 부재가 아니라 이음부에 있다 — B-60의 물림부와 같은 교훈이다.

**안전하게 일하기.** 기계마다 연구실의 교육을 먼저 받는다. 드릴이나 선반처럼 도는 기계 근처에서는 절대 장갑을 끼지 않고, 헐렁한 옷, 긴 머리, 장신구를 멀리한다. 영국 보건안전청(HSE)은 이런 기계 옆에서 장갑을 끼지 않았더라면 피할 수 있었던 심각한 작업장 사고가 많다고 적는다. 레이저 커터는 돌아가는 동안 절대 자리를 비우지 않고, 옆에 소화기를 두며, PVC는 자르지 않는다(MIT). ABS와 나일론은 환기하거나 인클로저 안에서 출력한다. Prusa의 안내서가 ABS의 스티렌 증기와 나일론의 초미세입자를 경고하기 때문이다. 열압입 인서트는 플라스틱을 녹일 만큼 뜨거운 도구로 넣으니, 도구와 부품이 식은 뒤에 만진다.

### 9. 이 페이지가 다루지 않는 것

보 이론으로 모양을 기술할 수 없는 브래킷을 위한 유한요소해석, §3의 끼워맞춤과 §7의 데이텀을 넘는 공학 도면의 기하 공차 언어 전체, 다른 공정들 — 레진 출력, 사출 성형, 판금, 용접 — , 배선과 케이블 정리, 그리고 B-60이 든 카메라의 보정([[04-robotics/geometric-perception-calibration|3.5 §5]])은 다루지 않는다. 액추에이터와 구동계는 [[04-robotics/actuators-drives|10.5]], 완성한 리그를 메시·프레임·관성까지 ROS에 기술하는 일은 [[04-robotics/ros2/describing-a-robot|25.6]]에 있다.

### 읽고 나면

- [ ] 스케치의 자유도를 0까지 세고, 설계 의도를 싣는 참조를 고른다.
- [ ] 가공 기술자, 슬라이서, 버전 관리가 각각 어떤 파일을 받아야 하는지, 거친 STL 내보내기가 구멍에 무엇을 하는지 말한다.
- [ ] ISO 286 편차에서 끼워맞춤의 틈새 범위를 계산해 분류하고, 출력한 구멍이 왜 끼워맞춤이 아닌지 말한다.
- [ ] 하중을 받는 부품의 출력 방향을 고르고, 구멍 여유를 재어 적용하고, 표에서 재료를 고른다.
- [ ] 여유 구멍, 탭 구멍, 인서트 가운데 고르고, 토크에서 예압을 계산해 머리 아래 압력을 점검한다.
- [ ] 센서 브래킷의 기울기, 대상에서의 조준 오차, 고유 진동수, 그리고 카메라가 그 진동을 무엇으로 보는지 계산한다.
- [ ] 면, 둥근 핀, 다이아몬드 핀으로 부품을 3-2-1로 잡고, 최악의 위치 오차를 계산하고, 중복된 위치결정구를 찾아낸다.
- [ ] 도는 기계, 레이저 커터, 출력 유해 물질에 대한 작업장 규칙을 말한다.

### 스스로 점검

1. B-60은 카메라 무게로 65 µm 처진다. 핀에서의 오차는 왜 그 열 배이고, 언제 0이 되는가?
2. g6 위치 결정 핀을 위한 6 mm 구멍을 정확히 6.0 mm로 모델링해 출력한다. 무엇이 나오며, 미끄럼 끼워맞춤은 어떻게 얻는가?
3. 리밍한 구멍 둘에 둥근 핀 둘로 잡은 블록이 가끔은 끼고, 그렇지 않을 때는 두 자리 가운데 한 곳에 앉는다. 왜 그렇고, 어떻게 고치는가?
4. 8 mm 팔은 $94.90$ Hz로 진동하고 카메라는 50 Hz로 돈다. 급정지 뒤에 추적기는 무엇을 보며, 어떻게 대처하는가?
5. F-50의 M6 나사는 왜 블록의 위치를 정하지 못하며, 나사만으로 잡으면 S1의 핀은 얼마나 움직일 수 있는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 카메라는 팔 끝의 기울기 $\theta=3\delta/(2L)$만큼 돌고, 그 기울기가 핀까지의 $0.40$ m에 걸려 $e=D\theta=(3D/2L)\,\delta=10\delta$가 된다. 보정할 때와 쓸 때 방향이 같으면 0이다. 그때는 보정이 처짐까지 담고 있으므로, 값을 치르는 것은 둘 사이의 변화뿐이다.
> 2. 프린터가 약 $5.8$ mm로 뽑으므로 $5.988$–$5.996$ mm의 핀은 들어가지 않고, 억지로 넣으면 부품이 갈라진다. 프린터의 오차가 H7 공차역 전체의 17배라 모델 치수로는 고칠 수 없다. 구멍을 작게 출력한 뒤 드릴이나 리머로 H7, 곧 $6.000$–$6.012$ mm로 다듬거나 금속 부시를 압입한다. 그러면 H7/g6가 4–24 µm의 틈새를 준다.
> 3. 둥근 핀 둘은 블록을 평면 안에서 과구속한다. 블록의 구멍 간격과 판의 핀 간격에 저마다 공차가 있어서, 그 차이를 끼임이나 블록을 민 방향이 떠안는다. 핀 하나를 다이아몬드로 바꾸어, 핀을 잇는 선을 가로지르는 방향으로만 위치를 잡게 한다.
> 4. 50 Hz로 샘플링하면 $94.90$ Hz의 진동은 $|94.90-2\times50|=5.10$ Hz로 나타나, 핀이 느리게 헤매는 움직임처럼 보인다. 3단계의 출발만큼 격한 정지 뒤에 $0.849$ mm에서 시작해 $\zeta=0.02$로 $0.237$ s, 약 12프레임 걸려 $0.05$ mm 아래로 내려간다. 그 프레임을 버리거나, 덜 급하게 멈추거나, 브래킷을 단단하게 한다.
> 5. 나사는 6.6 mm 여유 구멍을 지나므로 블록은 $0.3$ mm의 놀이 안 어디든 앉을 수 있고, 나사는 앉은 자리 그대로 조일 뿐이다. S1의 핀은 다시 놓을 때마다 $0.300$ mm까지 움직인다 — 구멍 반경 틈새의 30%, $0.2$ mm 정밀 끼워맞춤 틈새의 세 배다 — 핀 위에서는 $0.014$ mm다.

### 과제 · Problem set

Tier B. 이 페이지, 선수 지식, 카탈로그만 쓰며 시뮬레이터는 없다. 손잡이 셋이 움직인다. B-60을 **B-80**으로 다시 만든다. 눕혀 출력한 같은 폭 20 mm의 팔이지만 물림면에서 카메라까지 80 mm이고, 재료는 $E_\parallel=2.0$ GPa(교과용 숫자)의 PETG다. 카메라, 허용치, 작업 거리, 감쇠, 프레임 속도는 그대로다. 그리고 F-50은 첫 핀에서 400 mm 너머 — S1의 구멍 간격 — , 둥근 핀에서 $x=425$ mm에 두 번째 목업 핀을 단 레일이 되고, 여전히 50 mm 간격의 둥근 핀과 다이아몬드 핀으로 위치를 잡는다.

1. **그리기.** 변형의 그림: (a) $h=8$ mm의 B-80을, 처짐과 기울기를 한 가지 배율로 키워, 두 시선과 핀에서의 오차와 함께; (b) 레일의 평면도를 축척대로, S1 핀 둘, 만든 그대로의 위치 결정 핀, 그리고 옮긴다면 다이아몬드 핀을 둘 자리와 함께; (c) 8 mm와 2(a)에서 고른 두께의 B-80, 그리고 핀 위와 나사만일 때의 두 번째 핀에 대한 막대를, 허용치 $0.5$ mm와 S1의 리드인 4 mm에 대어.
2. **유도.** (a) $h=8$ mm의 B-80: $I$, $k$, $\delta_g$, $\theta_g$, $e$. $0.5$ mm를 지키는 가장 얇은 팔과, 그다음 정수 밀리미터에서의 $e$. (b) 8 mm와 고른 두께에서의 $f_n$, 그리고 50 Hz 카메라가 각각을 보는 진동수. 고른 두께에서 $30.19$ m/s² 급정지 뒤 핀에서의 진동이 $0.05$ mm 아래로 내려갈 때까지의 프레임 수. (c) 두 번째 핀이 핀을 잇는 선을 가로질러 옮겨 가는 최악의 양을 핀 위에서와 M6 나사만으로; 이어 다이아몬드 핀을 두 번째 S1 핀 너머 25 mm로 옮긴 배치($s=450$ mm)에서, 그 배치의 $\theta_{\max}$와 함께. (d) F-50의 둥근 핀이 g6 대신 k6로 연삭되어 왔다. 6 mm에서 이 끼워맞춤의 범위와, 시행 사이에 고정구를 다시 놓는 사람이 알아챌 일.
3. **해석.** 동료가 첫 목업 리그의 설계 메모를 올렸다. 영어 절의 메모를 옮기면 아래와 같다. 문제마다 그것이 낳을 증상과 고치는 법을 절을 들어 말하고, 이 팔을 꽉 채워 출력했을 때 보정 단계가 핀에서 치르는 값을 어림해 S1의 리드인 4 mm와 비교하라.

```text
핀 목업 리그 v1 - 그룹 공유 메모
카메라 마운트: PLA, 채움 15%, 서포트가 필요 없도록 끝을 세워 출력.
  팔 100 x 20 x 5 mm (휘는 방향 5 mm); 카메라 0.10 kg, 공구 방향을 봄.
  카메라는 출력한 팔에 M2 나사 두 개를 곧장 박아 고정.
  M3 나사용 물림 구멍은 3.0 mm로 모델링 - 나사가 알아서 길을 낼 것.
  손-눈 보정은 공구가 팔 위의 보드를 향해 위를 볼 때 한 번; 시행은 공구가 아래의 핀을 향할 때.
핀 고정구: 베이스판 위 고무발 넷에 핀 블록, 리밍한 구멍 둘에 둥근 6 mm 다월 둘로 위치를 잡고, M6 나사 둘로 고정.
```

> [!note]- 그리는 법 · How to draw it
> - 패널 (a): 팔은 정해진 축척(80 mm면 mm당 2 px)으로, 처짐과 기울기는 제목에 적은 배율 하나로 키우고, 작업 거리는 끊어서 "축척 아님"이라고 적는다. 렌즈에서 나가는 시선 둘 — 보정 때는 점선, 지금은 실선 — 을 그리고, 핀에서의 둘의 간격을 숫자와 함께 $e=D_w\theta_g$로 적는다.
> - 패널 (b)는 축척대로. 둥근 핀에서 두 번째 S1 핀 너머까지 475 mm이니 mm당 약 0.5 px다. S1 핀 둘은 16 mm 원으로, 위치 결정 핀은 만든 그대로, 옮긴 다이아몬드 핀은 점선으로.
> - 패널 (c)는 밀리미터 축 하나에. 나사만일 때의 막대가 S1의 리드인 4 mm를 넘으므로 축을 끊거나 로그 축으로 하고 어느 쪽인지 밝힌다. 허용치와 리드인은 세로선으로, 각 $f_n$ 옆에는 앨리어스를 적는다. 50 Hz의 배수 근처의 진동수는 그림에서는 무해해 보이지만 그렇지 않다.

> [!tip]- 정답 · Solutions
> 1. (a) 8 mm에서 $\delta_g=98.1$ µm, $\theta_g=1.839$ mrad이고, $\times150$이면 $15.8^\circ$로 그린다. 핀에서의 간격은 $e=0.736$ mm로 $0.5$ mm 선을 넘고, 10 mm에서는 $e=0.377$ mm로 그 안이다. (b) 만든 그대로면 두 번째 S1 핀은 다이아몬드 핀 너머 375 mm, 핀 쌍의 바깥이라 회전이 이동을 키운다. $s=450$ mm면 두 S1 핀이 모두 위치결정구 사이에 든다. (c) 막대: B-80은 $0.736$과 $0.377$ mm, 두 번째 핀은 핀 위에서 $0.192$ mm, 나사만으로 $4.800$ mm로 리드인 4 mm를 넘고, 다이아몬드 핀을 옮기면 $0.017$ mm다.
> 2. (a) $I=20\times8^3/12=853.3$ mm⁴, $k=3\times2000\times853.3/80^3=10.00$ N/mm, $\delta_g=0.981/10.00=0.0981$ mm, $\theta_g=3\times0.0981/160=1.839$ mrad, $e=400\times1.839\times10^{-3}=0.736$ mm로 넘는다. 기울기가 $h^{-3}$에 비례하므로 $h\ge8\,(0.736/0.5)^{1/3}=9.10$ mm이고, 10 mm에서 $e=0.377$ mm다. (b) 8 mm에서 $f_n=\frac{1}{2\pi}\sqrt{10\,000/0.10}=50.33$ Hz로 $0.33$ Hz에서 보인다 — 추적기가 핀의 움직임과 구별할 수 없는 흐름으로, 브래킷이 진동할 수 있는 가장 나쁜 자리다. 10 mm에서는 $70.34$ Hz로 $|70.34-50|=20.34$ Hz에서 보인다. 10 mm에서 진동은 $(30.19/9.81)\times0.377=1.159$ mm에서 시작하고 $\zeta\omega_n=0.02\times2\pi\times70.34=8.84$ s⁻¹이므로 $\ln(1.159/0.05)/8.84=0.356$ s, 17.8프레임, 곧 18프레임이 걸린다. (c) 만든 그대로 $x=425$, $s=50$이면 핀 위에서 $e_\perp\le12\,|1-8.5|+12\times8.5=192$ µm다. 나사만이면 두 구멍 모두 $0.3$ mm의 놀이가 있는 둥근 구멍이라 같은 가중으로 $300\times(7.5+8.5)=4\,800$ µm, 곧 $4.800$ mm가 되어 리드인 4 mm보다 크다. 고정구 하나 때문에 두 번째 구멍이 핀의 포착 범위 밖으로 갈 수 있다. $s=450$ mm면 $\theta_{\max}=48/(2\times450\,000)=0.053$ mrad이고, 두 S1 핀이 모두 위치결정구 사이에 들어 계산 절의 `worst_shift`가 $12.2$와 $16.5$ µm를 준다. (d) H7 $+12/0$ 대 k6 $+9/+1$: $c_{\min}=0-9=-9$ µm, $c_{\max}=12-1=11$ µm로 중간 끼워맞춤이다. 이제 어떤 블록–핀 쌍은 9 µm까지 겹쳐서, 블록을 눌러 끼우고 지렛대로 떼어 내야 한다. 손으로 얹히지 않고, 억지로 다시 놓을 때마다 구멍에 자국이 남는다 — 반복성 있는 자리와는 정반대다.
> 3. 문제는 일곱. (i) *세워 출력*(§4): 휨이 층을 떼어 놓아($E_\perp$, $\sigma_\perp$) 더 처지고 층 경계에서 부러진다. 눕혀 출력한다. (ii) *채움 15%*(§4): 휨을 스킨과 외벽만 받는다. 꽉 채워 출력한다. (iii) *플라스틱에 박은 M2 나사*(§5): 나사산이 뭉개지고 크리프해 카메라가 밀린다. 열압입 인서트를 쓴다. (iv) *3.0 mm로 모델링한 M3 구멍*(§4, §5): 2.8 mm 근처로 나와 나사가 브래킷에 나사산을 파고, 머리로 조이는 대신 플라스틱 나사산으로 붙잡는다. $3.4+0.2=3.6$ mm로 모델링하거나 3.4로 드릴링한다. (v) *위를 보고 보정, 아래를 보고 사용*(§6): 180° 돌면 팔을 가로지르는 무게가 뒤집혀 기울기가 $2\theta_g$ 바뀐다. (vi) *고무발 넷*(§7): 받침이 하나 많고, 고무는 위치결정 면이 아니어서 블록이 달그락거리고 가라앉는다. 판 윗면이나 단단한 패드 셋에 앉힌다. (vii) *둥근 다월 둘*(§7): 중복된 위치결정구다. 하나를 다이아몬드 핀으로 바꾼다. (v)의 어림, 꽉 채워 세운 경우: $I=20\times5^3/12=208.3$ mm⁴, $\theta_g=0.981\times100^2/(2\times2400\times208.3)=9.81$ mrad이고, $2\theta_g$는 핀에서 $0.40\ \mathrm{m}\times2\times9.81\times10^{-3}=7.85$ mm — 다른 오차가 하나도 없는데도 리드인 4 mm의 거의 두 배다.

### 출처

- 미 의회도서관 형식 설명: [STEP (ISO 10303-21)](https://www.loc.gov/preservation/digital/formats/fdd/fdd000448.shtml), [STL](https://www.loc.gov/preservation/digital/formats/fdd/fdd000504.shtml), [이진 STL](https://www.loc.gov/preservation/digital/formats/fdd/fdd000505.shtml) — Part 21, AP242; STL의 삼각형, 규칙, 바이트.
- STEP Tools, [ISO 10303 STEP Standards](https://www.steptools.com/stds/step/) — CAD 데이터에서 AP242가 AP203과 AP214를 대체.
- Open Cascade, [STEP Translator](https://occt3d.com/dev/doc/overview/html/occt_user_guides__step.html) — STEP의 B-rep 솔리드와 정확한 곡면.
- NIST, [STEP File Analyzer and Viewer](https://www.nist.gov/services-resources/software/step-file-analyzer-and-viewer) — 부품, 어셈블리, PMI.
- Autodesk, [STL import options](https://help.autodesk.com/cloudhelp/2020/ENU/Alias-Reference/files/GUID-B7BF855B-724D-46E4-8FE3-185737BB9D31.htm) — STL에는 단위가 없다.
- RoyMech, [ISO 286 limits and fits](https://www.roymech.co.uk/Useful_Tables/ISO_Tolerances/), [구멍](https://www.roymech.co.uk/Useful_Tables/ISO_Tolerances/ISO_286_2H.html)·[축](https://www.roymech.co.uk/Useful_Tables/ISO_Tolerances/ISO_286_2s.html) 표 — 등급, 끼워맞춤, 여기서 쓴 모든 편차.
- Carr Lane, [Locating & Clamping Principles](https://www.carrlane.com/engineering-resources/fixture-design-principles/locating-clamping-principles), [Round & Diamond Pins](https://www.carrlane.com/product/locating-pins/locating-pins/round-diamond-pins) — 3-2-1, 클램프, 간격, 중복.
- SPIROL, [Threaded Inserts for Plastics](https://www.spirol.com/product/threaded-inserts-for-plastics/), [Heat / Ultrasonic Inserts](https://www.spirol.com/product/threaded-inserts-for-plastics/heat-ultrasonic-inserts/) — 플라스틱 속 금속 나사산.
- Protolabs Network, [출력 방향](https://www.hubs.com/knowledge-base/how-does-part-orientation-affect-3d-print/), [FDM 설계](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) — 이방성, 돌출부, 다리, 구멍.
- Prusa 지식 베이스, [PLA](https://help.prusa3d.com/article/pla_2062), [PETG](https://help.prusa3d.com/article/petg_2059), [ABS](https://help.prusa3d.com/article/abs_2058), [나일론](https://help.prusa3d.com/article/polyamide-nylon_167188) — §4의 표.
- Engineering ToolBox, [Bolt Torque Calculator](https://www.engineeringtoolbox.com/bolt-torque-load-calculator-d_2065.html) — $T=KFd$, $K=0.2$.
- Bolt Science, [머리 또는 너트](https://www.boltscience.com/pages/nutorbolttightening.htm), [예압 편차](https://www.boltscience.com/pages/basics9.htm) — 토크의 10–15%, 계수 1.6.
- 스탠퍼드 BDML, [커프 오프셋](http://bdml.stanford.edu/pmwiki/index.php/Main/AddingOffsetForKerf) — 커프와 절반 오프셋.
- MIT EHS, [Laser Cutter Safety](https://ehs.mit.edu/workplace-safety-program/laser-cutter-safety/), Epilog, [위험 재료](https://www.epiloglaser.com/how-it-works/faq/laser-machine-unsafe-materials/) — PVC, 감시.
- 영국 HSE, [Getting started](https://www.hse.gov.uk/engineering/getting-started.htm) — 장갑과 도는 기계.
