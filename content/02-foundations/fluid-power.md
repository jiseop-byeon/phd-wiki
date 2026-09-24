---
title: "0.6.3 Fluid Power: Hydraulics, Pneumatics and Vacuum"
tags: [foundations, physics, hydraulics]
study-depth: Working
depth-goal: "On the page's boom cylinder and vacuum lifter, turn a pump flow and a pressure into force, speed, power, heat, stiffness and a holding margin, and check a hydraulic or vacuum claim against that arithmetic."
mastery-when: "Raise when a hydraulic machine or a vacuum gripper is the hardware the thesis builds on, or when modelling a hydraulic actuator becomes the contribution."
wiki-support: Working
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 Engineering Math §1, §8]] (derivatives; first- and second-order linear ODEs and the natural frequency $\omega_n=\sqrt{k/m}$) · [[02-foundations/lab-plants|0.6 Lab Plants]] (the catalog, and the rule that a page freezes its own object when no plant fits)
> [[02-foundations/engineering-math|0.5 공업수학 §1, §8]](미분, 1차·2차 선형 미분방정식과 고유 진동수 $\omega_n=\sqrt{k/m}$) · [[02-foundations/lab-plants|0.6 Lab Plants]](카탈로그, 그리고 맞는 장치가 없으면 페이지가 자기 대상을 고정한다는 규칙)

## English

*Stands on [[02-foundations/engineering-math|0.5 Engineering Math §8]] for linear ODEs and the natural frequency $\omega_n=\sqrt{k/m}$, and on [[02-foundations/lab-plants|0.6 Lab Plants]], whose six plants include nothing hydraulic, so this page freezes two objects of its own. It is the floor under the construction track's machine and panel: the valve latency that [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]] prices on S2, and the suction grip whose pressure [[05-construction-robotics/site-engineering|2.5 Site Robotics §3]] monitors on S1.*

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] — perception, object and scene understanding, grasping, motion and task planning, manipulation, contact, force and tactile feedback, learning and adaptation, task completion — this page is the physical floor under the actuation and grasping layers of heavy machines: in *"Install that panel on the frame"* it is the hydraulic machine that lifts the panel and the vacuum grip that holds it (its place is marked on the [[physical-ai-map|Physical AI Map]]). Claims about either can be checked only with this arithmetic: a boom cylinder that can push $196\,\mathrm{kN}$ turns $42\%$ of its pump's power into heat in its valve at full speed, and four suction cups holding S1's $20\,\mathrm{kg}$ panel at a safety factor of $4.8$ keep the required factor of $2$ for only $41\,\mathrm s$ once their pump stops. The oil spring is part of the $0.15\,\mathrm s$ valve-to-motion latency that [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]] prices on S2 and [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §1]] lists as a gap, suction pressure is what [[05-construction-robotics/site-engineering|2.5 Site Robotics §3]] monitors while S1's panel is acquired, and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) the page sits in block 1, the foundations floor, taken where a civil-engineering degree left fluid power out. After it you can turn a pump's flow and pressure into force, speed, heat, stiffness and a holding margin, and check a spec sheet against them.

> [!note] First pass · 처음이라면
> Two sessions of about seventy-five minutes each. **Session 1, oil:** the Running object and the picture — a boom cylinder raising an excavator's arm, four suction cups holding S1's facade panel — then §1–§5: pressure, force, flow and power, the four ideas every hydraulic sentence is made of, and the circuit that joins them. End it by saying in your own words why the pump sets the flow and the load sets the pressure. **Session 2, springs and vacuum:** §6–§7 (losses and the oil spring), §8 (why air is soft) and §9–§10 (vacuum), then the Worked case, which derives every number in the picture, and §11, which ties the oil spring to the valve latency the construction pages price. Finish with the Self-check and the Interpret item of the problem set; §12 lists what is left out.

### Running object · 이 페이지의 대상

No plant in [[02-foundations/lab-plants|0.6 Lab Plants]] is hydraulic or pneumatic — P1 to P6 are a network, an arm, a handle, a heater, a range sensor and a cart — so this page freezes two objects of its own. Their numbers are **course numbers**: sized for a 5-tonne-class machine and a 20 kg panel, frozen here, and not measurements or specifications of any product. No other page changes them.

**H1 — a boom cylinder and its circuit.** One double-acting cylinder raises the boom of an excavator of S2's class, the 5-tonne-class machine of [[05-construction-robotics/site-engineering|2.5 Site Robotics]]. A fixed-displacement pump feeds it through a directional valve, a relief valve caps the pressure, and the oil returns to a tank. The arm, the bucket and a full bucket of soil are lumped into one point mass at the bucket tip, as P2's links are point masses.

| Symbol | Value | What it is |
|---|---:|---|
| $D,\ d,\ s$ | $100\,\mathrm{mm}$, $60\,\mathrm{mm}$, $0.80\,\mathrm{m}$ | bore (piston diameter), rod diameter, stroke |
| $V_d,\ N$ | $25\,\mathrm{cm^3/rev}$, $2400\,\mathrm{rev/min}$ | pump displacement and shaft speed, so $Q=60\,\mathrm{L/min}=1.0\times10^{-3}\,\mathrm{m^3/s}$, leakage neglected (§5) |
| $p_r$ | $25\,\mathrm{MPa}$ | relief-valve setting (§5) |
| $A_v,\ C_d$ | $20\,\mathrm{mm^2}$, $0.65$ | the directional valve at full command: the opening of each metering edge, P→A and B→T, and its discharge coefficient (§6) |
| $L_h,\ d_h$ | $3.0\,\mathrm{m}$, $20\,\mathrm{mm}$ | length and bore of each of the two hoses from valve to cylinder |
| $\rho,\ \eta$ | $870\,\mathrm{kg/m^3}$, $0.040\,\mathrm{Pa{\cdot}s}$ | the oil's density and viscosity at working temperature |
| $\beta_e$ | $1.0\,\mathrm{GPa}$ | effective bulk modulus of oil, hose and any undissolved air together (§7) |
| $c,\ V_o$ | $1900\,\mathrm{J/(kg{\cdot}K)}$, $50\,\mathrm{L}$ | the oil's specific heat, and the oil in tank and lines (§4) |
| $m_a,\ n$ | $600\,\mathrm{kg}$, $6$ | arm, bucket and soil lumped at the tip; at the pose used the tip rises $n$ times as fast as the rod extends |

**V1 — a vacuum lifter for S1's panel.** Four suction cups on the face of the facade panel of [[05-construction-robotics/site-engineering|2.5]]'s S1 — $m=20\,\mathrm{kg}$, weight $196\,\mathrm{N}$ — placed symmetrically about its centre of mass, where [[05-construction-robotics/hrc-worker-centered|6. HRC]] puts the grip, so the weight puts no moment on the pattern. A vacuum pump evacuates the cups and a small reservoir joined to them through a check valve (a non-return valve), which keeps the vacuum on the cups' side if the pump stops.

| Symbol | Value | What it is |
|---|---:|---|
| $n_c,\ D_c$ | $4$, $100\,\mathrm{mm}$ | number of cups, and the diameter of each cup's seal line |
| $\Delta p_w$ | $60\,\mathrm{kPa}$ | working vacuum: the cups' inside held $60\,\mathrm{kPa}$ below the atmosphere (§1, §9) |
| $\mu$ | $0.5$ | friction coefficient between cup rim and panel face (§9) |
| $S$ | $2$ | required safety factor (§9) |
| $V_s,\ Q_L$ | $2.0\,\mathrm{L}$, $1.0\,\mathrm{L/min}$ | volume sealed behind the check valve, and the leak into it, measured at atmospheric pressure (§10) |
| $p_{\text{atm}}$ | $101.325\,\mathrm{kPa}$ | the atmosphere's absolute pressure, the standard value |

Three modelling choices, stated once. **Gravity is the only load**: the boom rises at steady speed, so the rod carries the tip's weight through the lever and nothing else; digging forces are 3's subject. **The lever is ideal**: at the pose used the tip moves straight up, $n=6$ times as fast as the rod, and the pins lose nothing. **The panel hangs with its face vertical**, as it does at the wall during S1's hold, so the cups carry its weight by friction; a panel lying flat is §9's easier case. H1's bore and V1's cups share one circle, $100\,\mathrm{mm}$, on purpose: §9 puts the two pressures on the same area.

*Scope: this page teaches the physics of fluid power that a reader of construction and robotics papers needs — pressure and its units, force from pressure on a cylinder's two areas, flow and speed, hydraulic power, efficiency and heat, the basic circuit, orifice losses, compressibility and the oil spring, why air is soft, and holding with vacuum — worked on H1 and V1. It does not teach valve or pump design, valve dynamics beyond one lumped delay, load-sensing and electro-hydraulic control, hydraulic fluids and contamination, or pneumatic circuit design; §12 says where the nearest of these live. S2's latency is priced in [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]], and the control of a second-order plant belongs to [[04-robotics/control-theory-ce397|5. Control Theory]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 562" style="max-width:100%;height:auto" role="img" aria-label="Top: H1's boom cylinder at mid-stroke fed through a directional valve at full command. The pump's 60 L/min at 7.75 MPa loses 2.57 MPa across the valve's P to A edge, the cap side is at 5.17 MPa, the rod side returns 38.4 L/min at 1.05 MPa, and the rod pushes the 35.3 kN load at 0.127 m/s; the 25 MPa relief stays shut. A bar splits the pump's 7.75 MPa into 4.50 for the load, 0.67 against the back-pressure and 2.57 in the valve, against the 25 MPa relief. Bottom: V1's four 100 mm cups on S1's vertical panel; their friction capacity rises in proportion to the vacuum, 942 N at the working 60 kPa, safety factor 4.8, up to 1592 N at the atmosphere; S = 2 is reached at 25.0 kPa, 41 s after the pump stops.">
  <defs><marker id="fpA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" font-weight="600" fill="currentColor">H1 raising the boom at full command</text>
  <text x="250" y="40" font-size="11" fill="currentColor">bore 100, rod 60 mm, stroke 0.80 m</text>
  <rect x="250" y="57.5" width="200" height="25" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <rect x="251.5" y="59" width="95.5" height="22" fill="currentColor" fill-opacity="0.22"/>
  <rect x="347" y="57.5" width="6" height="25" fill="currentColor"/>
  <rect x="353" y="62.5" width="187" height="15" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <circle cx="540" cy="70" r="4" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="548,90.5 508,90.5" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpA)"/>
  <text x="548" y="104.5" font-size="11" text-anchor="end" fill="currentColor">F<tspan dy="3" font-size="10">L</tspan><tspan dy="-3"> = 35.3 kN</tspan></text>
  <polyline points="458,50.5 498,50.5" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#fpA)"/>
  <text x="458" y="40" font-size="11" fill="currentColor">v = 0.127 m/s</text>
  <polyline points="200,150 200,112 262,112 262,82.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <polyline points="236,150 236,126 438,126 438,82.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="262,100 262,90" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpA)"/>
  <polyline points="398,126 378,126" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpA)"/>
  <text x="268" y="100" font-size="11" fill="currentColor">cap 5.17 MPa</text>
  <text x="268" y="112" font-size="10" fill="currentColor">60 L/min in</text>
  <text x="444" y="142" font-size="11" fill="currentColor">rod 1.05 MPa</text>
  <text x="444" y="154" font-size="10" fill="currentColor">38.4 L/min out</text>
  <rect x="182" y="150" width="72" height="36" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="200,182 200,156" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#fpA)"/>
  <polyline points="236,154 236,180" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#fpA)"/>
  <text x="187" y="164" font-size="10" fill="currentColor">A</text>
  <text x="242" y="164" font-size="10" fill="currentColor">B</text>
  <text x="187" y="182" font-size="10" fill="currentColor">P</text>
  <text x="242" y="182" font-size="10" fill="currentColor">T</text>
  <text x="264" y="160" font-size="11" fill="currentColor">valve at full command</text>
  <text x="264" y="174" font-size="11" fill="currentColor">P→A drop 2.57 MPa</text>
  <text x="264" y="188" font-size="11" fill="currentColor">B→T drop 1.05 MPa</text>
  <polyline points="200,222 200,186" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="200" cy="236" r="14" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <path d="M 194 240 L 200 229 L 206 240 Z" fill="currentColor"/>
  <polyline points="200,250 200,262" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="180" y="234" font-size="11" text-anchor="end" fill="currentColor">pump</text>
  <text x="180" y="247" font-size="11" text-anchor="end" fill="currentColor">60 L/min</text>
  <text x="194" y="205" font-size="11" text-anchor="end" fill="currentColor">7.75 MPa</text>
  <polyline points="236,186 236,262" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="200,212 128,212" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <rect x="104" y="202" width="24" height="30" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="116,228 116,208" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#fpA)"/>
  <path d="M 104 217 L 99 214 L 93 220 L 87 214 L 81 220 L 76 217" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="116,232 116,262" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 3"/>
  <text x="12" y="190" font-size="11" fill="currentColor">relief 25 MPa</text>
  <text x="12" y="203" font-size="10" fill="currentColor">shut: 7.75 &lt; 25</text>
  <polyline points="96,262 96,282 330,282 330,262" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="98,270 328,270" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <text x="338" y="278" font-size="11" fill="currentColor">tank, 0 MPa gauge</text>
  <text x="12" y="304" font-size="11" fill="currentColor">where the pump's 7.75 MPa goes, against the 25 MPa relief</text>
  <rect x="40" y="324" width="89.9" height="14" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8"/>
  <rect x="129.9" y="324" width="13.5" height="14" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="0.8"/>
  <rect x="143.4" y="324" width="51.5" height="14" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.8"/>
  <rect x="194.9" y="324" width="345.1" height="14" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <polyline points="540,318 540,344" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="40,338 40,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="353" font-size="10" text-anchor="middle" fill="currentColor">0</text>
  <polyline points="140,338 140,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="353" font-size="10" text-anchor="middle" fill="currentColor">5</text>
  <polyline points="240,338 240,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="353" font-size="10" text-anchor="middle" fill="currentColor">10</text>
  <polyline points="340,338 340,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="353" font-size="10" text-anchor="middle" fill="currentColor">15</text>
  <polyline points="440,338 440,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="440" y="353" font-size="10" text-anchor="middle" fill="currentColor">20</text>
  <polyline points="540,338 540,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="540" y="353" font-size="10" text-anchor="end" fill="currentColor">relief 25 MPa</text>
  <text x="85" y="320" font-size="10" text-anchor="middle" fill="currentColor">load 4.50</text>
  <text x="200.9" y="335" font-size="10" fill="currentColor">← valve 2.57, back-pressure 0.67</text>
  <text x="12" y="370" font-size="11" fill="currentColor">7.75 kW in, 4.50 kW to the arm (58 %), 3.25 kW heat</text>
  <polyline points="8,382 552,382" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="12" y="400" font-size="12" font-weight="600" fill="currentColor">V1 holding S1's panel, face vertical</text>
  <rect x="20" y="412" width="84" height="92" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="44" cy="432" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="44" cy="468" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="80" cy="432" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="80" cy="468" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="62" cy="450" r="2.5" fill="currentColor"/>
  <polyline points="62,450 62,494" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpA)"/>
  <text x="67" y="492" font-size="10" fill="currentColor">196 N</text>
  <text x="20" y="520" font-size="11" fill="currentColor">S1 panel, 20 kg</text>
  <text x="20" y="533" font-size="11" fill="currentColor">4 cups Ø100 mm</text>
  <text x="20" y="546" font-size="11" fill="currentColor">μ = 0.5</text>
  <polyline points="220,510 544,510" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#fpA)"/>
  <polyline points="220,510 220,404" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#fpA)"/>
  <text transform="translate(212,455) rotate(-90)" font-size="10" text-anchor="middle" fill="currentColor">μ·n·Δp·A (N)</text>
  <polyline points="220,510 220,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="220" y="524" font-size="10" text-anchor="middle" fill="currentColor">0</text>
  <polyline points="292.7,510 292.7,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="292.7" y="524" font-size="10" text-anchor="middle" fill="currentColor">25</text>
  <polyline points="365.5,510 365.5,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="365.5" y="524" font-size="10" text-anchor="middle" fill="currentColor">50</text>
  <polyline points="438.2,510 438.2,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="438.2" y="524" font-size="10" text-anchor="middle" fill="currentColor">75</text>
  <polyline points="510.9,510 510.9,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="510.9" y="524" font-size="10" text-anchor="middle" fill="currentColor">100</text>
  <text x="380" y="537" font-size="11" text-anchor="middle" fill="currentColor">vacuum Δp below the atmosphere (kPa)</text>
  <polyline points="220,484.6 540,484.6" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <polyline points="220,497.3 540,497.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <text x="540" y="481.6" font-size="10" text-anchor="end" fill="currentColor">S = 2 (392 N)</text>
  <text x="540" y="494.3" font-size="10" text-anchor="end" fill="currentColor">S = 1 (196 N)</text>
  <polyline points="220,510 514.8,407" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="514.8,407 514.8,510" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/>
  <circle cx="394.5" cy="449" r="3.5" fill="currentColor"/>
  <text x="386.5" y="443" font-size="11" text-anchor="end" fill="currentColor">60 kPa: 942 N, S = 4.8</text>
  <circle cx="514.8" cy="407" r="3.5" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="506.8" y="404" font-size="11" text-anchor="end" fill="currentColor">atmosphere: 1592 N, S = 8.1</text>
  <circle cx="292.7" cy="484.6" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="256.3" cy="497.3" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="287.7" y="479.6" font-size="10" text-anchor="end" fill="currentColor">25.0</text>
  <text x="251.3" y="492.3" font-size="10" text-anchor="end" fill="currentColor">12.5</text>
  <text x="220" y="554" font-size="11" fill="currentColor">pump off: 60 → 25.0 kPa in 41 s, → 12.5 kPa in 56 s</text>
</svg>

H1 raising the boom at full command and V1 holding S1's panel, both drawn from the Worked case's numbers. Top: the pump's $60\,\mathrm{L/min}$ reaches the cap side through the valve's P→A edge, which takes $2.57\,\mathrm{MPa}$, the rod side returns $38.4\,\mathrm{L/min}$ through B→T at $1.05\,\mathrm{MPa}$, and the bar splits the pump's $7.75\,\mathrm{MPa}$ into $4.50$ for the load, $0.67$ against the back-pressure and $2.57$ in the valve, far under the $25\,\mathrm{MPa}$ relief, so that $4.50$ of the $7.75\,\mathrm{kW}$ reach the arm. Bottom: on the vertical panel the cups' friction capacity rises in proportion to the vacuum and stops at the atmosphere's $1592\,\mathrm{N}$; the working $60\,\mathrm{kPa}$ gives $942\,\mathrm{N}$, a safety factor of $4.8$, and after the pump stops the leak brings the vacuum to the $S=2$ level, $25.0\,\mathrm{kPa}$, in $41\,\mathrm{s}$.

### 1. Pressure, its zero, and Pascal's principle

*In one sentence:* pressure is force per unit area, a number that means nothing without its zero, and in a confined fluid at rest a change of it reaches every wetted surface at once — three facts that every hydraulic and vacuum calculation on this page stands on.

A fluid at rest cannot hold a shear stress; pushed sideways, it flows. The only force it can put on a wall is therefore perpendicular to the wall, a push, and how hard it pushes on a patch of wall grows with the patch. What belongs to the fluid, and not to the patch, is the push per unit area.

> **Pressure, defined.** **Pressure** is a *scalar property of a fluid at a point*: the normal force the fluid exerts per unit area of any surface through that point. Four defining conditions. Only the **normal** component counts, since a fluid at rest carries no shear. It is taken **per unit area**, on a patch small enough that the pressure is the same all over it. At a point in a fluid at rest it is the **same in every direction**, which is why it has no direction of its own (OpenStax 14.1: pressure is a scalar). And a value means something only with its **zero**: absolute pressure is counted from a perfect vacuum, gauge pressure from the local atmosphere.
>
> $$p=\frac{F_\perp}{A},\qquad p_{\text{abs}}=p_g+p_{\text{atm}}$$
>
> where $F_\perp$ is the normal force on the area $A$, $p_g$ the gauge pressure and $p_{\text{atm}}$ the atmosphere's absolute pressure (OpenStax 14.2 gives the second relation). The unit is the pascal, $1\,\mathrm{Pa}=1\,\mathrm{N/m^2}$, and since that is small — a sheet of $80\,\mathrm{g/m^2}$ paper lying flat presses with $0.08\times9.81=0.78\,\mathrm{Pa}$ — hydraulics works in MPa and bar, $1\,\mathrm{bar}=10^5\,\mathrm{Pa}$, and some catalogues in psi, $1\,\mathrm{psi}=6894.757\,\mathrm{Pa}$ (NIST SI guide, Appendix B.8).
>
> - **Example**: H1's relief setting, $p_r=25\,\mathrm{MPa}$ gauge, is $250\,\mathrm{bar}$ or $3626\,\mathrm{psi}$. V1's working vacuum, $60\,\mathrm{kPa}$ below the atmosphere, is the gauge pressure $p_g=-60\,\mathrm{kPa}$ and the absolute pressure $101.325-60=41.3\,\mathrm{kPa}$.
> - **Non-example**: "a vacuum of $150\,\mathrm{kPa}$". A gauge pressure can fall only as far as $-p_{\text{atm}}$, where the absolute pressure reaches zero (OpenStax 14.2), because a fluid can push but not pull; no pump can go further. This is the ceiling of §9.
> - **Non-example**: "$60\,\mathrm{kPag}$". A unit symbol carries no information about the quantity (NIST SI guide §7.4), so the zero is named with the quantity — "the gauge pressure $p_g=-60\,\mathrm{kPa}$" — and not glued to the unit.
> - **Why it matters**: hydraulic forces are computed with gauge pressure, since the atmosphere presses on both sides of a piston and cancels, while gas laws need absolute pressure (§8, §10). The wrong zero is an error of about $101\,\mathrm{kPa}$: $0.4\%$ of $25\,\mathrm{MPa}$, and more than the whole signal of a vacuum lifter.

Because a fluid at rest pushes equally in every direction at a point, and because its pressure changes with height only through the weight of the fluid above, $p=p_0+\rho gh$ (OpenStax 14.1), raising the pressure at one point of a closed body of oil raises it everywhere the oil reaches.

> **Pascal's principle, defined.** **Pascal's principle** is a *statement about a confined fluid at rest*: a change of pressure applied anywhere in it is transmitted undiminished to every part of the fluid and to the walls of its container (OpenStax 14.3). Three defining conditions. The fluid is **enclosed**, so the pressure has nowhere to go but onto the walls. It is **at rest**, or moving so slowly that no pressure is spent pushing it through restrictions (§6). And the **height** differences are small, or accounted for by $\rho gh$. Under these conditions two pistons of areas $A_1$ and $A_2$ on the same fluid carry forces in the ratio of their areas,
>
> $$\frac{F_1}{A_1}=\frac{F_2}{A_2}$$
>
> since both forces are the one pressure times their own area. Force can be multiplied this way but work cannot: the larger piston moves less, in the ratio of the areas, because the volume one piston pushes in is the volume the other makes room for.
>
> - **Example**: H1's pump line and cap chamber hold one body of oil, so the $25\,\mathrm{MPa}$ the relief allows acts on the whole cap face, $7854\,\mathrm{mm^2}$, as $196\,\mathrm{kN}$ — the weight of twenty tonnes — while $3\,\mathrm{m}$ of height between tank and cylinder is worth only $\rho gh=870\times9.81\times3=25.6\,\mathrm{kPa}$, $0.1\%$ of it.
> - **Non-example**: oil flowing through H1's valve at full command. It is not at rest, and the P→A edge takes $2.57\,\mathrm{MPa}$ out of the pressure on the way (§6), so the cap chamber sees $5.17\,\mathrm{MPa}$ while the pump works at $7.75\,\mathrm{MPa}$. Pascal holds from the pump to the valve and from the valve to the piston, but not across the valve.
> - **Why it matters**: it is why a hose can carry a force around corners to wherever the actuator is, and why a hydraulic machine is a force multiplier — which, since it cannot multiply work, makes it a speed divider as well (§3).

### 2. Force from pressure: a cylinder has two areas

A cylinder's rated force is a pressure times an area, but a double-acting cylinder has two areas, so it pushes and pulls with different forces, and a rating that does not say which is not a rating. A double-acting cylinder is a barrel divided by a piston, with a port at each end, so either side can be put under pressure. On the cap side — the end without the rod — the oil pushes on the whole piston face. On the rod side it pushes only on the ring the rod leaves free, the annulus.

> **Effective areas of a cylinder, defined.** The **effective areas** of a double-acting cylinder are *two geometric constants* set by its bore and rod: the cap area $A_{\text{cap}}$, on which oil pressure acts to extend it, and the annulus area $A_{\text{ann}}$, on which it acts to retract it. Three defining conditions. The cap area is the **full bore**. The annulus is the **bore minus the rod**, because the rod's cross-section is not wetted on that side. And the net force on the piston is the **difference** of the two pressure forces, because both chambers push at once. Their ratio, the **area ratio** $\varphi$, is always greater than one.
>
> $$A_{\text{cap}}=\frac{\pi D^2}{4},\qquad A_{\text{ann}}=\frac{\pi(D^2-d^2)}{4},\qquad F=p_{\text{cap}}A_{\text{cap}}-p_{\text{rod}}A_{\text{ann}},\qquad \varphi=\frac{A_{\text{cap}}}{A_{\text{ann}}}$$
>
> where $D$ is the bore, $d$ the rod diameter, $p_{\text{cap}}$ and $p_{\text{rod}}$ the gauge pressures in the two chambers, and $F$ the net outward force on the rod, seal friction neglected — so a cylinder is a force source whose force is set by two pressures, not by where the rod is.
>
> - **Example**: H1. $A_{\text{cap}}=\pi(0.1\,\mathrm m)^2/4=7.854\times10^{-3}\,\mathrm{m^2}$, $A_{\text{ann}}=\pi(0.1^2-0.06^2)\,\mathrm{m^2}/4=5.027\times10^{-3}\,\mathrm{m^2}$, $\varphi=1.5625$. At the relief pressure it pushes $25\times10^6\times7.854\times10^{-3}=196.3\,\mathrm{kN}$ and pulls $125.7\,\mathrm{kN}$.
> - **Non-example**: "the rod side is blocked, so it is safe." Push with $25\,\mathrm{MPa}$ on the cap while the rod side is trapped and nothing loads the rod, and the rod side must balance the cap: $p_{\text{rod}}=\varphi\,p_{\text{cap}}=1.5625\times25=39.1\,\mathrm{MPa}$, above the relief setting, which guards only the pump line. A cylinder can multiply its own pressure.
> - **Why it matters**: the same pump pressure gives two different forces, and (§3) the same pump flow two different speeds, so a claim about a cylinder has to say which way it moves. And nothing in the formula says where the rod is: a cylinder is a force source, and its position is what the flow adds up to over time (§3).

**What the rod has to carry.** H1's load is not at the rod but at the bucket tip, $m_a=600\,\mathrm{kg}$ riding $n=6$ times as fast as the rod. A lever that loses nothing passes power through unchanged, so the rod force times the rod speed equals the tip's weight times the tip speed,

$$F_L\,v=m_ag\,(n\,v)\quad\Rightarrow\quad F_L=n\,m_ag=6\times600\times9.81=35.3\,\mathrm{kN}$$

and the cap must hold $p_{\text{hold}}=F_L/A_{\text{cap}}=35\,316/7.854\times10^{-3}=4.50\,\mathrm{MPa}$ with the rod side open to the tank: $18\%$ of the relief setting. The same power argument will give the arm's mass as the rod feels it in §7. Lowering the boom is a retraction with gravity helping: the load now pushes the rod in, and what holds the speed is the throttling of the oil leaving the cap side, not the pump — the valve's outlet edge is doing the braking (§6).

### 3. Flow and speed: the time to stroke

How fast the boom rises and how long a stroke takes are set by the pump's flow, not by its pressure. A pump does not push with a force; it delivers volume. What a cylinder does with that volume is fixed by its geometry: the piston must move far enough to make room for it.

> **Volumetric flow rate, defined.** The **volumetric flow rate** $Q$ is a *rate*: the volume of fluid crossing a section per unit time (OpenStax 14.5), in $\mathrm{m^3/s}$, and in hydraulics usually in L/min, where $1\,\mathrm{L/min}=1.667\times10^{-5}\,\mathrm{m^3/s}$. Three defining conditions for using it as this page does. The fluid is treated as **incompressible**, so volume is conserved; the passages are **sealed**, so no volume leaves by leakage; and the flow is **steady**, so what enters a chain of passages leaves it at the same rate. Then continuity holds — the same $Q$ passes every section in series — and at a section of area $A$ the mean speed is
>
> $$v=\frac{Q}{A}$$
>
> because the volume $Q\,\Delta t$ that crosses in a time $\Delta t$ fills a length $v\,\Delta t$ of the section.
>
> - **Example**: H1 extending. The pump's $1.0\times10^{-3}\,\mathrm{m^3/s}$ into the cap area $7.854\times10^{-3}\,\mathrm{m^2}$ moves the rod at $0.127\,\mathrm{m/s}$, so the $0.80\,\mathrm{m}$ stroke takes $6.28\,\mathrm{s}$. Retracting, the same flow into the annulus gives $0.199\,\mathrm{m/s}$ and $4.02\,\mathrm{s}$: the speed ratio is $\varphi=1.5625$ again, the other way round.
> - **Non-example**: "the return line carries the pump flow." Retracting, the cap side empties at $0.199\times7.854\times10^{-3}=1.5625\times10^{-3}\,\mathrm{m^3/s}$, $93.75\,\mathrm{L/min}$, which is $\varphi$ times the pump's $60$; extending, the rod side returns only $38.4\,\mathrm{L/min}$. A valve and a return line sized for the pump are undersized for a retracting cylinder.
> - **Why it matters**: flow sets speed and pressure sets force, and the two stay independent until power (§4) or the relief valve (§5) ties them together. To make a cylinder faster you need more flow, not more pressure.

The time to stroke is the swept volume over the flow, $t=sA/Q$: H1's cap side sweeps $0.80\times7.854\times10^{-3}=6.28\times10^{-3}\,\mathrm{m^3}$, $6.28\,\mathrm{L}$, which the pump's $1.0\,\mathrm{L/s}$ fills in $6.28\,\mathrm{s}$. At the tip the lever multiplies the speed by $n$: the arm rises at $6\times0.127=0.764\,\mathrm{m/s}$. As long as the pressure the load needs stays below the relief setting, a fixed pump gives the same speed whatever the load, since the load changes the pressure, not the volume per second. Read the other way, the cylinder is an integrator: its position is the flow it has received, $x(t)=x(0)+\frac{1}{A}\int_0^tQ\,dt$, so a valve that sets flow sets speed, and holding a position against a changing load needs a loop closed on position, the integrator-in-a-loop that 0.5 draws for P4 ([[02-foundations/engineering-math|0.5 §8]]). The one assumption to keep in view is incompressibility: §7 relaxes it, and it is exactly what the first tens of milliseconds of a movement violate (§11).

### 4. Hydraulic power, efficiency and heat

A hydraulic machine's pump puts out kilowatts, and where they go — to the load, or into hot oil — is this section's question. Force and speed multiply to mechanical power, and for a cylinder both come from the oil: $F\,v=(pA)(Q/A)=pQ$. The area cancels, which says that the power is carried by the oil itself. Pressure has the units of energy per volume, $1\,\mathrm{Pa}=1\,\mathrm{N/m^2}=1\,\mathrm{J/m^3}$, so a flow of volume per second at a pressure is a flow of energy per second; OpenStax's College Physics writes $pQ$ as the power supplied to a fluid by a pump (College Physics 2e §12.3).

> **Hydraulic power, defined.** **Hydraulic power** is a *rate of energy transfer* carried by a flowing liquid: the pressure difference across an element times the flow through it. Three defining conditions. The pressure is a **difference**, taken between the element's inlet and outlet — for a pump, its outlet against the tank. The flow is the one **through** that element. And the liquid is treated as incompressible, so that pressure is energy per unit volume and nothing is stored in squeezing it.
>
> $$P=\Delta p\,Q$$
>
> where $P$ is in watts when $\Delta p$ is in pascals and $Q$ in $\mathrm{m^3/s}$ — and for a cylinder it equals the mechanical power, since $F\,v=pQ$.
>
> - **Example**: H1 raising the arm at full flow: $p_{\text{hold}}Q=4.50\times10^6\times1.0\times10^{-3}=4.50\,\mathrm{kW}$ into the cap, equal to $F_Lv=35\,316\times0.1273$ and to the tip's weight times its speed, $5886\times0.764$ — the same $4.50\,\mathrm{kW}$ counted three ways.
> - **Non-example**: pressure alone. H1 holding the arm still at $4.50\,\mathrm{MPa}$ has $Q=0$ into the cylinder and delivers no power however high the pressure; and a pump at $25\,\mathrm{MPa}$ whose whole flow crosses the relief valve delivers $25\,\mathrm{kW}$ to nothing but heat (§5).
> - **Why it matters**: every pressure drop the flow passes through is a power $\Delta p\,Q$ turned into heat, so a circuit's efficiency can be read off its pressures, and its cooling need off its losses.

**Efficiency and heat.** The efficiency of a circuit is the power that reaches the load over the power the pump puts in, $\eta=P_{\text{out}}/P_{\text{in}}$; the rest is heat, and it is found by walking the flow path and multiplying each pressure drop by the flow through it. The heat warms the oil. With no cooling, $Q_{\text{heat}}=mc\,\Delta T$ (OpenStax University Physics Vol. 2 §1.4) gives the warming rate

$$\frac{dT}{dt}=\frac{P_{\text{heat}}}{\rho V_o\,c}$$

since the oil's heat capacity, its mass $\rho V_o$ times its specific heat $c$, absorbs the power. H1's $50\,\mathrm{L}$ of oil weigh $43.5\,\mathrm{kg}$ and take $82.7\,\mathrm{kJ}$ per kelvin at $c=1900\,\mathrm{J/(kg{\cdot}K)}$ — a course value, a little under half of the $4186\,\mathrm{J/(kg{\cdot}K)}$ that OpenStax's table gives water — so the $25\,\mathrm{kW}$ of a relief valve blowing at stall warms them by $0.30\,\mathrm{K/s}$, $18\,\mathrm{K}$ a minute. A machine that stalls against its relief valve for a minute is heating its oil, not moving its load. The Worked case finds H1's efficiency at full flow, where the valve, not the relief, makes the heat.

**At the pump's shaft.** The same power enters as torque times shaft speed. The pump moves the volume $V_d$ per revolution against the pressure $p$, so one revolution does the work $pV_d$, and one revolution is $2\pi$ radians, so

$$\tau=\frac{p\,V_d}{2\pi}$$

because work per radian is torque. At H1's relief setting that is $25\times10^6\times25\times10^{-6}/(2\pi)=99.5\,\mathrm{N{\cdot}m}$, and at $2400\,\mathrm{rev/min}$, $251.3\,\mathrm{rad/s}$, the engine supplies $99.5\times251.3=25.0\,\mathrm{kW}$: the stalled relief valve's heat, seen as a load on the engine.

### 5. The circuit in one picture: pump, relief valve, directional valve, cylinder, tank

*In one sentence:* the pump delivers flow, the load and the losses decide the pressure, the relief valve caps it, the directional valve decides where the flow goes, and the tank takes back what returns — five parts with one job each.

A hydraulic schematic reads as a tangle of lines until each part's single job is known, so take them in the order the oil meets them. Read the top of the picture starting at the tank. The pump draws oil from the tank and pushes a fixed volume per revolution into the pressure line. The relief valve sits on that line, shut. The directional valve connects the pressure line, port P, to one cylinder port and the other cylinder port to the tank line, port T — at full extend command P to A and B to T. The cylinder turns pressure into force (§2) and flow into speed (§3), and the oil it pushes out of the rod side returns through the valve to the tank, which is open to the atmosphere and so sits at zero gauge pressure.

> **Positive-displacement pump, defined.** A **positive-displacement pump** is a *flow source*: a machine that traps a fixed volume of oil per revolution of its shaft and pushes it out, whatever pressure it meets downstream, up to what its drive and casing can bear. Three defining conditions. Its delivery is **fixed by displacement and speed**. The **pressure is set downstream**, by the load and the losses the flow must pass, not by the pump. And the **power** it draws is whatever that pressure times its flow comes to, which the engine or motor behind it must supply.
>
> $$Q=V_d\,N$$
>
> where $V_d$ is the displacement per revolution and $N$ the shaft speed; internal leakage, which would lower $Q$ as the pressure rises, is neglected here, so the pump is a pure flow source.
>
> - **Example**: H1's pump, $25\,\mathrm{cm^3}\times2400\,\mathrm{rev/min}=60\,000\,\mathrm{cm^3/min}=60\,\mathrm{L/min}=1.0\times10^{-3}\,\mathrm{m^3/s}$ — the same whether the line is at $4.5$ or at $7.75\,\mathrm{MPa}$.
> - **Non-example**: "the pump makes $25\,\mathrm{MPa}$." It makes $60\,\mathrm{L/min}$. With the arm rising freely the line is at $7.75\,\mathrm{MPa}$, and it reaches $25\,\mathrm{MPa}$ only when something stops the flow: the end of the stroke, or a load the cylinder cannot move.
> - **Why it matters**: a fixed pump with nowhere to send its flow raises the pressure until something gives, which is why the next part is not optional.

> **Relief valve, defined.** A **relief valve** is a *pressure limiter*: a normally closed valve between the pressure line and the tank that opens when the pressure at its inlet reaches its setting and passes as much flow to the tank as it must to hold the pressure there. Three defining conditions. It is **closed below its setting**, so in normal work it passes nothing. It **opens at the setting**. And whatever flow it passes, it passes **at the setting**, across the whole difference between the pressure line and the tank.
>
> $$p\le p_r,\qquad P_{\text{heat}}=p_r\,Q_r$$
>
> where $p_r$ is the setting and $Q_r$ the flow crossing the valve, so its heat is §4's $\Delta p\,Q$ with $\Delta p=p_r$.
>
> - **Example**: H1 at the end of its stroke with the valve still commanded. The rod can go no further, all $60\,\mathrm{L/min}$ crosses the relief valve at $25\,\mathrm{MPa}$, and $25\,\mathrm{kW}$ becomes heat, the $18\,\mathrm{K}$ a minute of §4.
> - **Non-example**: the relief valve as what sets the working pressure. In the Worked case it never opens: the load and the valve's losses need only $7.75\,\mathrm{MPa}$. It sets the ceiling, not the level.
> - **Why it matters**: it is the circuit's force limit — $p_rA_{\text{cap}}=196\,\mathrm{kN}$ is all H1 can ever push — and, whenever it is open, the circuit's largest heat source.

The directional valve is the part a controller commands. H1's has four ports and three positions: extend (P to A, B to T), retract (P to B, A to T), and a centre in which the cylinder ports are blocked, so the cylinder holds on its trapped oil (§7 says how stiffly), while P is joined to T, so the pump's flow goes home to the tank at low pressure instead of over the relief valve. A proportional valve, as the [[glossary|Glossary]] defines it, opens its edges gradually with its command, and that is how a valve sets a speed: it is a variable orifice, whose law is §6's. Whatever the directional valve does, it does by routing and throttling flow; it adds no energy, and every bit of throttling it does is heat.

### 6. Pressure drop: orifices and hoses

Pascal's principle is a law of oil at rest. Oil that flows loses pressure wherever it is squeezed through a restriction, and a valve is built of restrictions on purpose. Take a sharp-edged opening of area $A_o$ in a wall, with the pressure $p_1$ upstream and $p_2$ downstream. Upstream the oil approaches slowly through a wide passage; in the opening it is accelerated into a jet. Over so short a distance friction does little, so Bernoulli's equation at constant height carries the oil from the slow side into the jet (OpenStax 14.6):

$$p_1+\tfrac12\rho v_1^2=p_2+\tfrac12\rho v_2^2$$

and since $v_1\ll v_2$, the jet speed is $v_2=\sqrt{2(p_1-p_2)/\rho}$. The jet contracts to a section smaller than the opening, and the real flow runs a little slower than the ideal one, so the flow is $Q=C_dA_ov_2$ with a discharge coefficient $C_d<1$ that absorbs both. Downstream, the jet does not slow back into pressure: it breaks up in turbulence, and its kinetic energy becomes heat. That is why the drop stays lost, and why Bernoulli's equation applies from the slow side into the jet but not across the whole orifice.

> **Orifice equation, defined.** The **orifice equation** is a *flow law for a short restriction*: the flow through it grows as the square root of the pressure drop across it. Four defining conditions. The restriction is **short**, so friction along it is negligible and Bernoulli's equation carries the oil into the jet. The upstream speed is **small** beside the jet's. The jet is **turbulent** downstream, so its energy is not recovered. And a measured **discharge coefficient** $C_d$ accounts for the jet's contraction and losses.
>
> $$Q=C_d\,A_o\sqrt{\frac{2\,\Delta p}{\rho}}\qquad\Longleftrightarrow\qquad \Delta p=\frac{\rho}{2}\Big(\frac{Q}{C_d\,A_o}\Big)^2$$
>
> where $A_o$ is the opening, $\rho$ the oil's density and $\Delta p=p_1-p_2$ the drop — so the drop grows as the square of the flow.
>
> - **Example**: H1's valve at full command, $A_o=20\,\mathrm{mm^2}$ and $C_d=0.65$. The jet runs at $Q/(C_dA_o)=76.9\,\mathrm{m/s}$, and the P→A edge takes $\Delta p=\tfrac12\times870\times76.9^2=2.57\,\mathrm{MPa}$ at $60\,\mathrm{L/min}$; the B→T edge, passing $38.4\,\mathrm{L/min}$, takes $(38.4/60)^2=0.41$ of that, $1.05\,\mathrm{MPa}$. Treated as a round hole of the same area, the jet's Reynolds number is $N_R=2\rho vr/\eta=8443$, above the $3000$ beyond which OpenStax 14.7 calls flow turbulent.
> - **Non-example**: a long hose. H1's $3\,\mathrm{m}$ of $20\,\mathrm{mm}$ bore carry the $60\,\mathrm{L/min}$ at $3.18\,\mathrm{m/s}$ with $N_R=1385$, below OpenStax's $2000$, so the flow is laminar and its loss follows Poiseuille's law instead (OpenStax 14.7): in proportion to the flow, and to the length over the fourth power of the radius.
> - **Why it matters**: a directional valve controls speed by being a variable orifice, and it pays for control in pressure — at the cap, $2.57\,\mathrm{MPa}$ is $20.2\,\mathrm{kN}$ of force the load never sees — and in heat, §4's $\Delta p\,Q$. Because the drop goes as $Q^2$, twice the flow through the same valve costs four times the pressure.

**What restrictions cost.** In force: at full flow the pump can spend its $25\,\mathrm{MPa}$ only on what is left after the valve, so the largest load H1 can lift at full speed before the relief valve opens is $(25-2.574)\times10^6\times7.854\times10^{-3}-1.054\times10^6\times5.027\times10^{-3}=170.8\,\mathrm{kN}$, not the $196\,\mathrm{kN}$ it can hold still. In response: a restriction that eats pressure at a given flow passes less flow at a given pressure, so a small valve makes a slow machine. Hoses cost in two ways. Their friction grows with length and, in laminar flow, as the inverse fourth power of the radius — halving the bore makes the resistance sixteen times larger (OpenStax 14.7) — so a hose one size too small is a heat source; at H1's size the valve's drops are the ones that matter. And every litre of hose is oil that must be compressed before the piston moves, which is what §7 prices.

### 7. Compressibility: the oil column is a spring

*In one sentence:* oil is nearly incompressible, but nearly is enough — a column of it is a spring whose stiffness grows with the square of the piston area and falls with the volume of oil behind it, and with the arm's mass it makes a mass–spring that rings at a few hertz.

So far the oil has been treated as incompressible. Squeeze it hard enough and it gives a little, and a little oil giving a little is what sits between a valve's command and the load.

> **Bulk modulus, defined.** The **bulk modulus** $\beta$ of a fluid is a *material stiffness under uniform pressure*: the pressure rise per unit fractional loss of volume. Three defining conditions. The compression is **uniform**, the same pressure on every face, so only the volume changes, not the shape. The modulus is a **local slope**, taken at one pressure and temperature, because it changes with both. And for a gas it depends on **how fast** the squeeze is, since a slow squeeze stays at the surroundings' temperature and a fast one heats the gas.
>
> $$\beta=-V\,\frac{dp}{dV}$$
>
> where $V$ is the volume and $dp/dV$ the slope of pressure against volume; the minus sign makes $\beta$ positive because the volume falls as the pressure rises (OpenStax 12.3 writes the same ratio with finite changes).
>
> - **Example**: H1's oil, $\beta_e=1.0\,\mathrm{GPa}$. At the relief's $25\,\mathrm{MPa}$ it has lost $25\times10^6/10^9=2.5\%$ of its volume, and at the holding $4.50\,\mathrm{MPa}$, $0.45\%$. For scale, OpenStax's table lists water at $2.2\,\mathrm{GPa}$ and steel at $160\,\mathrm{GPa}$.
> - **Non-example**: air "with a bulk modulus" like a liquid's. For an ideal gas at constant temperature $pV$ is constant (the ideal gas law, OpenStax University Physics Vol. 2 §2.1), so $dp/dV=-p/V$ and $\beta=p$: the modulus *is* the absolute pressure — $0.7\,\mathrm{MPa}$ in air at $0.6\,\mathrm{MPa}$ gauge — and for a squeeze too fast to shed its heat, $pV^\gamma$ is constant and $\beta=\gamma p=1.4p$ (Vol. 2 §3.6). Not a constant of the material at all, and about $1400$ times softer than H1's oil.
> - **Why it matters**: every litre of oil between the valve and the piston is a spring and $\beta$ sets its rate, so how stiff a hydraulic joint is, how fast its pressure can rise and how quickly it can be controlled all come back to this one number.

**The spring.** Block both ports of a cylinder and push the rod in by a small $x$. The cap chamber's oil, of volume $V$, loses the volume $Ax$, so by the definition its pressure rises by $\Delta p=\beta Ax/V$, and that pressure pushes back on the piston with $A\,\Delta p$:

$$\Delta F=\frac{\beta A^2}{V}\,x$$

so the trapped oil is a spring whose rate grows with the square of the area and falls with the volume of oil behind it. A civil engineer has met this spring before: write the oil's volume as a column, $V=AL$, and the rate is $\beta A/L$, the axial stiffness $EA/L$ of a bar with the bulk modulus in place of Young's modulus. H1's cap side, chamber and hose together, is equivalent to a column $V_{\text{cap}}/A_{\text{cap}}=0.52\,\mathrm m$ long, and a steel bar of the same section and length would be $E/\beta=200$ times stiffer.

> **Hydraulic spring rate, defined.** The **hydraulic spring rate** of a cylinder is a *stiffness*, in N/m: the force needed per unit displacement of the rod when the oil in its chambers is trapped. Three defining conditions. The oil is **trapped** — the valve closed and no leakage — so a displacement can only compress it. The displacement is **small**, so the pressure change is proportional to the volume change, with $\beta$ setting the proportion. And each chamber acts with its **own area and volume**, the hose up to the valve included; when both are trapped the two rates add, because a push squeezes one chamber and relieves the other, and both changes push back.
>
> $$k_h=\beta\Big(\frac{A_{\text{cap}}^2}{V_{\text{cap}}}+\frac{A_{\text{ann}}^2}{V_{\text{rod}}}\Big)$$
>
> where $V_{\text{cap}}$ and $V_{\text{rod}}$ are the volumes of oil on each side of the piston, chamber plus hose.
>
> - **Example**: H1 at mid-stroke. Each hose holds $\pi(0.02\,\mathrm m)^2/4\times3\,\mathrm m=0.94\,\mathrm{L}$, so $V_{\text{cap}}=3.14+0.94=4.08\,\mathrm{L}$ and $V_{\text{rod}}=2.01+0.94=2.95\,\mathrm{L}$, and $k_h=10^9\,(6.169\times10^{-5}/4.084\times10^{-3}+2.527\times10^{-5}/2.953\times10^{-3})=15.1+8.6=23.7\,\mathrm{MN/m}$. A $1\,\mathrm{kN}$ change of load moves the rod $0.042\,\mathrm{mm}$.
> - **Non-example**: the same cylinder with air at $0.7\,\mathrm{MPa}$ absolute. With $\beta=p$ its rate is $16.6\,\mathrm{kN/m}$, and the same $1\,\mathrm{kN}$ moves it $60\,\mathrm{mm}$. A second non-example is $k_h$ with one side open to the tank: that chamber's spring is gone, and H1 extending has only its cap side's $15.1\,\mathrm{MN/m}$.
> - **Why it matters**: the oil spring and the mass the rod moves form a mass–spring with the natural frequency of [[02-foundations/engineering-math|0.5 §8]], $\omega_n=\sqrt{k/m}$, and no controller acting through the oil can make the arm respond much faster than that.

**The mass on the spring.** The rod does not feel $600\,\mathrm{kg}$. The arm's mass rides at the tip, $n=6$ times as fast as the rod, so its kinetic energy $\tfrac12m_a(nv)^2=\tfrac12(n^2m_a)v^2$ is that of a mass $m_r=n^2m_a=21\,600\,\mathrm{kg}$ moving with the rod — the same $n^2$ that [[04-robotics/actuators-drives|10.5 Actuators & Drives §4]] finds for a motor behind a gearbox. On H1's oil spring that mass rings at

$$\omega_n=\sqrt{\frac{k_h}{m_r}}=\sqrt{\frac{2.366\times10^7}{21\,600}}=33.1\,\mathrm{rad/s}$$

so at $5.27\,\mathrm{Hz}$: a heavy arm on a stiff spring still makes a slow oscillator, and a controller that tries to move it much faster than a few hertz excites it. Line length is where this bites. Without hoses the chambers alone give $32.2\,\mathrm{MN/m}$ and $6.15\,\mathrm{Hz}$; with $10\,\mathrm{m}$ hoses, $14.7\,\mathrm{MN/m}$ and $4.15\,\mathrm{Hz}$. [[04-robotics/control-theory-ce397|5. Control Theory §2]] writes such a mass–spring in state space, and its §5 turns $\omega_n$ and the damping into the rise times and overshoots papers quote.

**Why $\beta_e$ is set below a liquid's.** An effective modulus includes everything the pressure squeezes. A hose wall stretches, which adds volume under pressure. And undissolved air counts for far more than its share, because volumes under one pressure add: the whole volume $V$ loses $\Delta V=V_\ell\,\Delta p/\beta_\ell+V_g\,\Delta p/\beta_g$, so $1/\beta_e=(V_\ell/V)/\beta_\ell+(V_g/V)/\beta_g$, with $\beta_g=p$ for the gas. Take a liquid as stiff as water, $2.2\,\mathrm{GPa}$, at $5\,\mathrm{MPa}$: a gas fraction of $0.1\%$ brings it down to $1.53\,\mathrm{GPa}$, and $1\%$ to $0.41\,\mathrm{GPa}$. That is why H1 freezes a round $1.0\,\mathrm{GPa}$ for oil and hose together, and why bleeding the air out of a hydraulic system is a stiffness question before it is a maintenance one.

### 8. Air is soft: pneumatics and where it is used

Robots grip with air and dig with oil, and the reason is a single number, the bulk modulus. §7's non-example is the whole of pneumatics in one line. A gas's bulk modulus is its absolute pressure, so air at a supply of $0.6\,\mathrm{MPa}$ gauge — a course value for this section — is about $1400$ times softer than H1's oil, and the supply pressure itself is some $40$ times lower than H1's relief setting: on H1's $100\,\mathrm{mm}$ bore it pushes $0.6\times10^6\times7.854\times10^{-3}=4.7\,\mathrm{kN}$, against $196\,\mathrm{kN}$ in oil at $25\,\mathrm{MPa}$. A pneumatic cylinder is weaker for its size and has a soft spring built in.

**A gripper finger, in numbers.** Drive a finger with a $20\,\mathrm{mm}$ bore cylinder from a regulated $0.6\,\mathrm{MPa}$ supply, a course example. It closes with $0.6\times10^6\times\pi(0.02\,\mathrm m)^2/4=188\,\mathrm N$, and if the part turns out $2\,\mathrm{mm}$ wider than expected, the finger stops $2\,\mathrm{mm}$ earlier with the same $188\,\mathrm N$, because the regulator holds the pressure and the force is pressure times area wherever the piston is. A finger driven to a position would instead press on until something gave.

That spring decides where air is used. **Position under load**: an air cylinder cannot hold a point in the middle of its stroke while the load changes, because the air gives — $60\,\mathrm{mm}$ per kilonewton in §7's example — so pneumatic actuators are usually run from end to end, against hard stops, and their job is to open and close rather than to track. **Force without a sensor**: a gripper finger on air pushes with pressure times area wherever it happens to stop, so it closes on a part of uncertain size with a known force, and a collision it cannot see costs less; the softness is the feature. **Soft actuators** take this further: an elastomer body with internal chambers bends or wraps around an object when inflated, and its compliance, not a linkage, decides its shape. **Vacuum from compressed air**: many suction grippers make their vacuum with an ejector, in which a compressed-air jet through a nozzle drags air out of the cups — Schmalz states that ejectors work on the Venturi principle — so a pneumatic supply is also what feeds a vacuum gripper like V1's.

One caution carries over from §1: a gas law needs absolute pressure, so a gauge reading has to have the atmosphere added before it goes into $pV=nRT$ — $0.6\,\mathrm{MPa}$ gauge is $0.70\,\mathrm{MPa}$ in the law, and a stiffness computed from the gauge value would be $14\%$ too soft. This page does not size pneumatic circuits (§12).

### 9. Vacuum: holding a panel with the atmosphere

*In one sentence:* a suction cup does not pull — the atmosphere pushes the panel onto it with the pressure difference times the sealed area, a force capped by the atmosphere itself — and a vertical panel hangs on that force only through friction.

Seal a cup on the panel's face and lower the pressure inside it by $\Delta p$. Outside, the atmosphere keeps pushing on the panel with $p_{\text{atm}}$; inside the seal the remaining air pushes back with only $p_{\text{atm}}-\Delta p$. The net push, $\Delta p$ over the area inside the seal, presses panel and cup together. Nothing inside the cup pulls, since a fluid can push but not pull (§1).

> **Vacuum holding force, defined.** The **holding force** of a suction cup is a *pressure force*: the difference between the atmosphere's pressure and the cup's inside pressure times the area inside its seal line (Schmalz writes $F=\Delta p\times A$ with the effective suction area). Four defining conditions. The cup is **sealed**, so the difference is held rather than leaked away. The area is the **effective** one, inside the seal line as the cup deforms under load, not the cup's outside diameter. The force acts **normal** to the surface, pressing panel and cup together; along the surface a cup holds only by friction, the normal force times the friction coefficient. And it is capped by the **atmosphere**, since the difference can never exceed $p_{\text{atm}}$.
>
> $$F_n=n_c\,\Delta p\,A_c,\qquad F_t\le\mu\,F_n,\qquad \Delta p\le p_{\text{atm}}$$
>
> where $n_c$ is the number of cups, $A_c$ each cup's effective area, $F_n$ the total normal force and $F_t$ the largest force the cups can carry along the face.
>
> - **Example**: V1 at $60\,\mathrm{kPa}$, about the relative vacuum of $60\%$ at which Schmalz quotes holding forces. Each cup presses with $60\times10^3\times7.854\times10^{-3}=471\,\mathrm{N}$ and the four with $1885\,\mathrm{N}$; with the face vertical they carry at most $0.5\times1885=942\,\mathrm{N}$ along it. The same $100\,\mathrm{mm}$ circle carries $196\,\mathrm{kN}$ as H1's cap at $25\,\mathrm{MPa}$: the law is the same and the pressures are $417$ times apart.
> - **Non-example**: "a stronger pump will hold more." At a perfect vacuum the four cups press with $4\times101\,325\times7.854\times10^{-3}=3183\,\mathrm{N}$ and carry $1592\,\mathrm{N}$ along a vertical face — $162\,\mathrm{kg}$ with no margin at all — and no pump can add a newton to it; only more or larger cups can. On a site $1000\,\mathrm{m}$ up, OpenStax's exponential atmosphere, $p=p_0e^{-y/8800\,\mathrm m}$, lowers even that ceiling to $89\%$ (OpenStax 14.1).
> - **Why it matters**: the atmosphere does the holding, so the lifter's capacity is set by area, vacuum and friction, and a vertical hold — S1's at the wall — has only $\mu=0.5$ of the capacity a flat lift has.

The friction coefficient in that formula is the weak number. Schmalz gives reference values — $0.2$ to $0.3$ on wet surfaces, $0.5$ on wood, metal, glass and stone, $0.6$ on rough ones — and insists that $\mu$ be found by tests. [[04-robotics/grasping|15. Grasping §2]] draws the friction cone this rests on, and its §6 makes the site version of the same warning: on a construction site nobody measures $\mu$, and it changes within a shift.

> **Safety factor of a vacuum hold, defined.** The **safety factor** $S$ of a vacuum hold is a *ratio of capacity to demand*: the force the cups can carry in the direction the load acts, over the force the load puts on them. Three defining conditions. Capacity and demand are taken **in the same direction** — normal pull for a flat part lifted straight up, friction for a vertical one. The capacity is computed at the **lowest vacuum** the lifter is allowed to reach, not at the pump's best. And the demand includes the load's **acceleration** as well as its weight, since the cups must also start and stop it; Schmalz writes the demand as $m(g+a)$. The required value is fixed before the lift: Schmalz uses at least $1.5$ for smooth, dense parts and $2.0$ or more for critical, porous, rough or oiled ones, and one lifter maker's summary of EN 13155 says lifters are dimensioned with a factor of two (Aerolift).
>
> $$S_{\text{vert}}=\frac{\mu\,n_c\,\Delta p\,A_c}{m\,(g+a)},\qquad S_{\text{flat}}=\frac{n_c\,\Delta p\,A_c}{m\,(g+a)}$$
>
> since along a vertical face the cups hold by friction, and under a flat part lifted straight up they hold by their normal force alone.
>
> - **Example**: V1 on S1's vertical panel at rest, $a=0$: $S=942/196.2=4.80$; laid flat, $1885/196.2=9.61$. The vacuum at which the vertical hold falls to the required $S=2$ is $\Delta p_{\min}=2\times196.2/(0.5\times4\times7.854\times10^{-3})=25.0\,\mathrm{kPa}$, and to $S=1$, $12.5\,\mathrm{kPa}$.
> - **Non-example**: a factor computed at the pump's best vacuum on a clean test plate. It says nothing about the level the lifter holds on a porous panel, or after its pump has stopped, which is where the factor is spent.
> - **Why it matters**: the minimum vacuum, not the working one, is the number a monitor must trip on — which is why S1 names suction pressure as the variable monitored while acquiring ([[05-construction-robotics/site-engineering|2.5 §3]]).

### 10. Leaks, reservoirs and the lifter inside S1's safe state

A lifter's margin is spent in two ways that §9's formulas do not show: a surface that lets air in, and a pump that stops. Both are questions of time, and the ideal gas law answers them.

**What a leak does.** A cup on a porous panel, or with its rim across a groove, lets outside air in all the time. While the pump runs it must remove that air as fast as it enters, and the vacuum settles where the two balance — lower on a leakier surface; for porous, permeable parts Schmalz recommends a suction trial with the original part. When the pump stops, the check valve keeps the reservoir from venting back through the pump, and the vacuum decays at the leak's pace. Model the leak as a steady inflow of outside air, $Q_L$ measured at atmospheric pressure — a course model; a real leak's rate changes with the vacuum and must be measured. By the ideal gas law at constant temperature, $pV_s=Nk_BT$ (Vol. 2 §2.1), the inflow adds to the air in $V_s$ what occupied $Q_L$ per second at $p_{\text{atm}}$, so the absolute pressure inside rises at

$$\frac{dp_{\text{abs}}}{dt}=\frac{p_{\text{atm}}\,Q_L}{V_s}$$

and the vacuum falls at the same rate. For V1, $101\,325\times(1.0\times10^{-3}/60)/2.0\times10^{-3}=844\,\mathrm{Pa/s}$: from $60\,\mathrm{kPa}$ to the $S=2$ level of $25.0\,\mathrm{kPa}$ in $41.5\,\mathrm{s}$, and to $S=1$ in $56.3\,\mathrm{s}$. A porous panel leaking $20\,\mathrm{L/min}$ gets there in $2.1\,\mathrm{s}$.

**The lifter inside S1's safe state.** In S1's hold/fasten phase the safe state is *freeze*: brakes set, no powered motion, the panel carried by the brakes rather than by the servo loop, so that it still holds if servo power is lost ([[05-construction-robotics/site-engineering|2.5 §3]]). With V1 as the gripper the brakes carry the arm, and the cups carry the panel on the arm, so the freeze is safe exactly as long as the cups hold without their pump: on these numbers, $41\,\mathrm{s}$ at $S\ge2$. That is enough to lower the panel — acquire's safe state is *lower and regrasp* — and far short of the five minutes that EN 13155 asks of a crane's vacuum lifter after a power failure, together with a non-return valve and a visible and audible low-vacuum alarm, in Aerolift's summary. A robot's gripper is not a crane attachment, but 2.5's third condition asks the same question — does the state hold without the function that failed? — and the answer for V1 is a number of seconds. The monitor follows from the same numbers: a vacuum switch set at the $S=2$ level, $25.0\,\mathrm{kPa}$, trips $41\,\mathrm s$ after the pump fails on a sound panel and about $2\,\mathrm s$ after on a porous one, and from its trip the system has only the $15\,\mathrm s$ down to $S=1$ to leave the phase.

### Worked case · 대상으로 한 번 끝까지

Raise the boom at full command, then hold S1's panel on V1. Eight steps, every number from the Running object and every law from §1–§10. These are course computations on frozen objects, not measurements of a machine.

**Step 1 — the areas.** $A_{\text{cap}}=\pi(0.1\,\mathrm m)^2/4=7.854\times10^{-3}\,\mathrm{m^2}$, $A_{\text{ann}}=\pi(0.1^2-0.06^2)\,\mathrm{m^2}/4=5.027\times10^{-3}\,\mathrm{m^2}$, and $\varphi=1.5625$ (§2).

**Step 2 — the pressure the load asks for.** By §2's lever, $F_L=n\,m_ag=6\times600\times9.81=35\,316\,\mathrm N$, so the cap must hold $p_{\text{hold}}=35\,316/7.854\times10^{-3}=4.497\,\mathrm{MPa}$ against a rod side at tank pressure.

**Step 3 — speed and time.** $v=Q/A_{\text{cap}}=1.0\times10^{-3}/7.854\times10^{-3}=0.1273\,\mathrm{m/s}$, the tip rises at $0.764\,\mathrm{m/s}$, the stroke takes $0.80/0.1273=6.28\,\mathrm s$, and the rod side returns $vA_{\text{ann}}=6.40\times10^{-4}\,\mathrm{m^3/s}=38.4\,\mathrm{L/min}$ (§3).

**Step 4 — the valve's two edges.** By the orifice equation (§6), P→A passes $60\,\mathrm{L/min}$ at $\Delta p_{PA}=\tfrac12\times870\times\big(1.0\times10^{-3}/(0.65\times20\times10^{-6})\big)^2=2.574\,\mathrm{MPa}$, and B→T passes $38.4\,\mathrm{L/min}$ at $\Delta p_{BT}=0.4096\times2.574=1.054\,\mathrm{MPa}$.

**Step 5 — the pressures.** The tank is at zero gauge, so the rod side sits at $p_B=\Delta p_{BT}=1.054\,\mathrm{MPa}$, and at steady speed the forces on the piston balance:

$$p_A\,A_{\text{cap}}=F_L+p_B\,A_{\text{ann}}\quad\Rightarrow\quad p_A=p_{\text{hold}}+\frac{p_B}{\varphi}=4.497+0.675=5.171\,\mathrm{MPa}$$

because the back-pressure pushes on the annulus, which is $1/\varphi$ of the cap. The pump works at $p_P=p_A+\Delta p_{PA}=5.171+2.574=7.745\,\mathrm{MPa}$, under the $25\,\mathrm{MPa}$ setting, so the relief valve stays shut and the pump's whole flow reaches the cylinder (§5).

**Step 6 — power, efficiency and heat.** The pump puts in $p_PQ=7.745\,\mathrm{kW}$; the arm receives $F_Lv=4.497\,\mathrm{kW}$; $\eta=4.497/7.745=58.1\%$. The other $3.249\,\mathrm{kW}$ is the valve's: $2.574\,\mathrm{MPa}\times1.0\times10^{-3}\,\mathrm{m^3/s}=2.574\,\mathrm{kW}$ at P→A and $1.054\,\mathrm{MPa}\times6.40\times10^{-4}\,\mathrm{m^3/s}=0.675\,\mathrm{kW}$ at B→T (§4). With no cooling it warms the $43.5\,\mathrm{kg}$ of oil at $3249/(43.5\times1900)=0.039\,\mathrm{K/s}$, $2.4\,\mathrm K$ a minute; at the end of the stroke the relief valve takes all $25\,\mathrm{kW}$ and the rate is $18\,\mathrm K$ a minute.

**Step 7 — V1's hold.** $F_n=4\times60\times10^3\times7.854\times10^{-3}=1885\,\mathrm N$; along the vertical face, $\mu F_n=942\,\mathrm N$ against the panel's $196.2\,\mathrm N$, so $S=4.80$ (§9). The vertical hold falls to the required $S=2$ at $\Delta p_{\min}=25.0\,\mathrm{kPa}$, and the atmosphere caps it at $1592\,\mathrm N$, $S=8.1$.

**Step 8 — V1 after its pump stops.** $dp_{\text{abs}}/dt=101\,325\times1.667\times10^{-5}/2.0\times10^{-3}=844\,\mathrm{Pa/s}$, so the vacuum falls from $60$ to $25.0\,\mathrm{kPa}$ in $(60\,000-24\,981)/844=41.5\,\mathrm s$ and to $12.5\,\mathrm{kPa}$, where $S=1$, in $56.3\,\mathrm s$. Five minutes at $S\ge2$ would need $V_s=300\times101\,325\times1.667\times10^{-5}/35\,019=14.5\,\mathrm L$, or a leak of $0.14\,\mathrm{L/min}$ with the $2\,\mathrm L$ reservoir (§10).

**What the case says.** The pump runs at under a third of its relief setting, and still $42\%$ of its power becomes heat in the valve: a throttled circuit buys its control with pressure, and the price grows as the square of the flow. The lifter has a generous static margin, $4.8$ against a required $2$, and a thin margin in time: under a minute without its pump. Neither number is visible on a spec sheet that quotes only "pushes $196\,\mathrm{kN}$" and "holds $1885\,\mathrm N$".

### 11. Valve response and the latency the construction pages price

S2 freezes a valve-to-motion latency, $\tau_h=0.15\,\mathrm s$ ([[05-construction-robotics/site-engineering|2.5 Site Robotics]]), and [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]] turns it into a latency overshoot, $e_{\text{lat}}=v\tau_h$: a tip closing on the grade at $0.3\,\mathrm{m/s}$ ends $45\,\mathrm{mm}$ past it. That section names what sits between command and motion: the valve's travel through its dead zone, the pressure build-up, and the compliance of oil and hoses. The last two are this page's physics and can be priced on H1.

**Building pressure.** A chamber whose pressure must rise by $\Delta p$ before the load moves needs the extra volume $V\Delta p/\beta$ pushed into it — §7's definition read backwards — and the valve delivers volume at the rate $Q$, so

$$t_p=\frac{V\,\Delta p}{\beta\,Q}$$

since nothing moves until that volume has arrived. For H1 at mid-stroke, starting to lift an arm that rests on the ground with its cap chamber at tank pressure: $4.084\times10^{-3}\times4.497\times10^6/(10^9\times1.0\times10^{-3})=18.4\,\mathrm{ms}$ before the rod can move at all.

**Accelerating through the oil spring.** Once the rod moves, the flow into the cap side both compresses the oil and moves the piston, $(V/\beta)\,\dot p=Q-Av$, while the pressure above $p_{\text{hold}}$ accelerates the reflected mass, $m_r\dot v=A(p-p_{\text{hold}})$. Differentiating the second and substituting the first gives

$$\ddot v+\omega_c^2\,v=\omega_c^2\,\frac{Q}{A_{\text{cap}}},\qquad \omega_c^2=\frac{\beta A_{\text{cap}}^2}{V_{\text{cap}}\,m_r}$$

so, with the rod side open to the tank and the rod starting from rest at $p_{\text{hold}}$, the speed follows the particular-plus-homogeneous solution of [[02-foundations/engineering-math|0.5 §8]], $v(t)=(Q/A_{\text{cap}})(1-\cos\omega_ct)$. With the cap side's spring alone, $\omega_c=26.4\,\mathrm{rad/s}$ ($4.21\,\mathrm{Hz}$), and the rod first reaches the commanded $0.127\,\mathrm{m/s}$ after a quarter period, $\pi/(2\omega_c)=59.4\,\mathrm{ms}$, then overshoots; this model has no damping, and a real circuit's friction and leakage supply it.

**What that says about $\tau_h$.** Even behind a valve that opened instantly, H1's oil costs $18\,\mathrm{ms}$ of build-up from rest on the ground and a $59\,\mathrm{ms}$ rise to speed. Neither is a pure delay like S2's $\tau_h$, but both are a part of the lag that no faster valve removes, since they are set by $\beta$, the area, the oil volume and the mass; on these course numbers the rest of S2's $0.15\,\mathrm s$ would have to come from the valve itself — its pilot stage and its spool's travel through the dead zone, which the [[glossary|Glossary]] defines and this page does not model. The lever also divides distances: if the boom alone drove that pass at H1's pose, 3's $45\,\mathrm{mm}$ at the tip would be $45/6=7.5\,\mathrm{mm}$ at H1's rod, which then moves at $0.3/6=0.05\,\mathrm{m/s}$, its cap side passing $0.05\times7.854\times10^{-3}\,\mathrm{m^3/s}=23.6\,\mathrm{L/min}$ through the valve. A simulator that leaves this lag out has the hydraulic-delay gap that [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §1]] lists in its first row, among the dynamics gaps.

### 12. What this page does not cover

- **Valves and pumps from the inside**: spool geometry and overlap, pilot stages, pressure compensators, variable-displacement and load-sensing pumps. The construction pages treat the valve as one lumped latency ([[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]]), and so does §11.
- **Controlling a hydraulic arm**: servo-valve dynamics, pressure and force control, and learned actuator models. A mass–spring under feedback is [[04-robotics/control-theory-ce397|5. Control Theory]], whose own §9 names valve dead zones among the effects that break linear guarantees; the learned models are 3's.
- **Fluids**: viscosity changing with temperature, contamination and filtration, cavitation, and air beyond §7's gas fraction.
- **Pneumatic circuits**: the flow of a compressible gas through orifices, valves and ejectors, and the energy stored in a pressurized volume; §8 gives only the stiffness.
- **Accumulators, hydraulic motors and hydrostatic drives**, and the tracks and swing drive of a whole machine.
- **Standards**: what the safety standards for fluid-power systems and lifting attachments require. §10 quotes one maker's summary of EN 13155 and does not read the standard; robot safety is [[04-robotics/hri-safety|11. HRI & Safety]].
- **The mechanics and the electricity around it**: the mass on a spring that the oil column makes, and the levers a boom works through, are [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §5 and §9]]; the electric drive a hydraulic machine stands in for, with power as voltage times current, is [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics §1 and §7]].

### After reading

- [ ] Convert a pressure between Pa, bar and psi and between gauge and absolute, and say which zero a calculation needs.
- [ ] Compute a cylinder's push and pull, its extend and retract speeds and its stroke times from bore, rod, pressure and flow.
- [ ] Find the pressures around a simple circuit at full command — pump, valve edges, both chambers — and its efficiency and heat.
- [ ] Estimate an orifice's pressure drop from its area and flow, and say why the drop grows as the square of the flow.
- [ ] Compute a cylinder's hydraulic spring rate and the natural frequency with the mass it moves, and say what a longer hose does to both.
- [ ] Say in one formula why air is soft, and name where that softness is useful.
- [ ] Compute a vacuum lifter's holding force, safety factor and minimum vacuum for a flat and a vertical part, and how long it holds after its pump stops.

### Self-check

1. A gauge on V1 reads $-60\,\mathrm{kPa}$. What is the absolute pressure in the cups, and why can no vacuum pump make that gauge read $-150\,\mathrm{kPa}$?
2. H1 gets the same $60\,\mathrm{L/min}$ to extend and to retract. Which way is faster, which stronger, by what factor — and why is force times speed at one pressure the same both ways?
3. The directional valve stays commanded after H1's rod reaches the end of its stroke. Where does the pump's flow go, at what pressure, and what happens to the oil?
4. Why does a longer hose make H1 both softer and slower to respond, though it barely changes the force?
5. Why is air soft and oil stiff — in one formula each?
6. S1's hold/fasten safe state is freeze, brakes set. If V1 holds the panel, what else must be true for freeze to be safe?

> [!tip]- Answers
> 1. $p_{\text{abs}}=p_g+p_{\text{atm}}=-60+101.3=41.3\,\mathrm{kPa}$. A gauge pressure can fall only to $-p_{\text{atm}}$, where the absolute pressure is zero: a fluid pushes but cannot pull, so there is nothing below a perfect vacuum for a pump to reach.
> 2. Retracting is faster, $0.199$ against $0.127\,\mathrm{m/s}$, and extending is stronger, $196.3$ against $125.7\,\mathrm{kN}$ at $25\,\mathrm{MPa}$ — both by $\varphi=1.5625$. Force is $pA$ and speed $Q/A$, so their product $pQ$ has lost the area: the power a given pressure and flow carry does not depend on which face they act on.
> 3. The rod cannot move, so the cylinder takes no flow; the pressure rises to the relief setting and all $60\,\mathrm{L/min}$ crosses the relief valve at $25\,\mathrm{MPa}$. That is $25\,\mathrm{kW}$, all of it heat — $18\,\mathrm K$ a minute in H1's $50\,\mathrm L$ with no cooling.
> 4. The hose adds oil volume on each side, and the spring rate $\beta A^2/V$ falls with volume, so the arm's natural frequency drops ($6.15\,\mathrm{Hz}$ without hoses, $5.27$ with $3\,\mathrm m$, $4.15$ with $10\,\mathrm m$) and the pressure takes longer to build, $V\Delta p/(\beta Q)$. The force is still $pA$, less the small friction drop of the hose.
> 5. Oil: $\beta=-V\,dp/dV$ is a material constant, about $1\,\mathrm{GPa}$ for H1. Air: from $pV=\text{const}$, $\beta=p$, the absolute pressure itself — $0.7\,\mathrm{MPa}$ at $0.6\,\mathrm{MPa}$ gauge, some $1400$ times softer.
> 6. That the cups keep the panel without their pump, for as long as the freeze may last: a check valve and a reservoir, and a leak small enough that the vacuum stays above the minimum for $S\ge2$ — $41\,\mathrm s$ for V1 as frozen — with the vacuum level monitored so that the phase is left before that time runs out.

### Problem set · 과제

Tier B. Using only this page, its prerequisites and the Running object: H1 and V1 as frozen, with the changes each item names. By hand; no simulator.

1. **Draw.** The picture for H1 fed by a $90\,\mathrm{L/min}$ pump through the same valve, and for V1 on the same panel wet from rain, $\mu=0.25$. Top: the circuit with its flows and pressures at full command, and the bar of the pump's pressure against the $25\,\mathrm{MPa}$ relief. Bottom: the vertical holding capacity against the vacuum, with the $S=1$ and $S=2$ lines, the working point, and the atmosphere's ceiling.
2. **Derive.** (a) H1 at $90\,\mathrm{L/min}$: rod and tip speeds, stroke time, both valve drops, the three pressures, the input and output power, the efficiency, and the oil's warming rate. (b) The largest pump flow at which H1, with this valve at full command, still lifts its arm without the relief valve opening. (c) V1 on the wet panel: the safety factor at $60\,\mathrm{kPa}$, the minimum vacuum for $S=2$, and the time from $60\,\mathrm{kPa}$ to that level after the pump stops. (d) The reservoir $V_s$ that would keep the wet panel at $S\ge1$ for five minutes with the same leak. (e) The rod-side pressure if H1 pushes at $25\,\mathrm{MPa}$ with its rod port blocked and no load, and why the relief valve does not prevent it.
3. **Interpret.** A lab-mate's sheet for the rig says: "The boom cylinder ($100\,\mathrm{mm}$ bore, $60\,\mathrm{mm}$ rod) on our $60\,\mathrm{L/min}$ pump extends at $0.5\,\mathrm{m/s}$ and pushes $25\,\mathrm t$. The four-cup lifter ($100\,\mathrm{mm}$ cups) holds $100\,\mathrm{kg}$, and with a bigger vacuum pump it would hold $200\,\mathrm{kg}$." Check each claim against this page's arithmetic; say which are impossible, which hold only under a condition, and what the sheet would have to state to be checkable.

> [!note]- How to draw it · 그리는 법
> - **Top, the same five parts**: tank, pump, relief valve on the pressure line, the valve at full command (P to A, B to T), and the cylinder at mid-stroke with its load arrow against the motion. Label the flows: $90\,\mathrm{L/min}$ into the cap, $57.6\,\mathrm{L/min}$ out of the rod side.
> - **Label the pressures where they are**: pump line $11.81\,\mathrm{MPa}$, cap $6.01\,\mathrm{MPa}$, rod side $2.37\,\mathrm{MPa}$, tank $0$. The valve's edges take $5.79$ and $2.37\,\mathrm{MPa}$; both are $2.25=(90/60)^2$ times their values at $60\,\mathrm{L/min}$, and drawing them larger by that factor is the point of the item.
> - **The bar on a linear axis from $0$ to $25\,\mathrm{MPa}$**: load $4.50$, back-pressure $1.52$, valve $5.79$, reaching $11.81$; the relief line at $25$. Write the power beside it: $17.7\,\mathrm{kW}$ in, $6.74\,\mathrm{kW}$ to the arm, $38\%$.
> - **Bottom, the capacity line at half the slope**: $\mu n_cA_c=7.85\,\mathrm{N/kPa}$, from the origin to $796\,\mathrm N$ at $101.3\,\mathrm{kPa}$, where it stops.
> - **The two dashed lines are unchanged**, $196\,\mathrm N$ ($S=1$) and $392\,\mathrm N$ ($S=2$), because the panel is the same; what moves is where the capacity line crosses them, $25.0$ and $50.0\,\mathrm{kPa}$.
> - **Mark the working point** at $60\,\mathrm{kPa}$, $471\,\mathrm N$, $S=2.40$, and write the pump-off time to $S=2$ beside it, $11.9\,\mathrm s$. The drawing is wrong if the working point is still at $942\,\mathrm N$, or if the ceiling moves: the atmosphere did not change.

> [!tip]- Solutions
> 1. As in the How-to-draw list. Top: $v=0.191\,\mathrm{m/s}$; pressures $11.81$, $6.01$, $2.37\,\mathrm{MPa}$; drops $5.79$ and $2.37\,\mathrm{MPa}$; $17.7\,\mathrm{kW}$ in, $6.74\,\mathrm{kW}$ out. Bottom: capacity $471\,\mathrm N$ at $60\,\mathrm{kPa}$, $S=2.40$; $S=2$ at $50.0\,\mathrm{kPa}$, $S=1$ at $25.0\,\mathrm{kPa}$; ceiling $796\,\mathrm N$, $S=4.06$.
> 2. (a) $v=1.5\times10^{-3}/7.854\times10^{-3}=0.191\,\mathrm{m/s}$, tip $1.146\,\mathrm{m/s}$, stroke $4.19\,\mathrm s$; return $57.6\,\mathrm{L/min}$. $\Delta p_{PA}=2.25\times2.574=5.791\,\mathrm{MPa}$, $\Delta p_{BT}=2.25\times1.054=2.372\,\mathrm{MPa}$; $p_B=2.372$, $p_A=4.497+2.372/1.5625=6.015$, $p_P=6.015+5.791=11.806\,\mathrm{MPa}$. In $11.806\times1.5=17.71\,\mathrm{kW}$, out $35\,316\times0.191=6.74\,\mathrm{kW}$, $\eta=38.1\%$; heat $10.96\,\mathrm{kW}$ warms the oil at $10\,964/82\,650=0.133\,\mathrm{K/s}$, $8.0\,\mathrm K$ a minute. Half again the flow bought $50\%$ more speed at $3.4$ times the heat. (b) The losses scale as $Q^2$: $p_P=4.497+3.249\,(Q/60)^2\,\mathrm{MPa}$ reaches $25\,\mathrm{MPa}$ at $(Q/60)^2=6.31$, $Q=151\,\mathrm{L/min}$; above that the relief valve opens and the extra flow never reaches the arm. (c) $S=0.25\times1885/196.2=2.40$; $\Delta p_{\min}=2\times196.2/(0.25\times0.031416)=50.0\,\mathrm{kPa}$; $(60\,000-49\,962)/844=11.9\,\mathrm s$. (d) $S=1$ on the wet panel needs $25.0\,\mathrm{kPa}$, so $V_s=300\times101\,325\times1.667\times10^{-5}/35\,019=14.5\,\mathrm L$ — the same volume as the Worked case's dry panel at $S=2$, because halving $\mu$ doubles every minimum vacuum. (e) The piston balances when $p_{\text{rod}}A_{\text{ann}}=p_{\text{cap}}A_{\text{cap}}$, so $p_{\text{rod}}=1.5625\times25=39.1\,\mathrm{MPa}$. The relief valve watches the pump line; the rod side is sealed off from it by the blocked port, so nothing limits that chamber but its own strength.
> 3. "Extends at $0.5\,\mathrm{m/s}$": impossible on $60\,\mathrm{L/min}$. Extending needs $0.5\times7.854\times10^{-3}=3.93\times10^{-3}\,\mathrm{m^3/s}$, $236\,\mathrm{L/min}$, $3.9$ times the pump; the pump gives $0.127\,\mathrm{m/s}$ out and $0.199\,\mathrm{m/s}$ back. (A circuit that routes the rod side's outflow back into the cap side needs the pump to fill only the rod's own volume, $v=Q/A_{\text{rod}}=0.354\,\mathrm{m/s}$, by continuity — still short, and at a push of only $p\,A_{\text{rod}}=70.7\,\mathrm{kN}$ at $25\,\mathrm{MPa}$.) "Pushes $25\,\mathrm t$": $245\,\mathrm{kN}$ needs $31.2\,\mathrm{MPa}$ on the cap, above the $25\,\mathrm{MPa}$ relief, whose ceiling is $196\,\mathrm{kN}$, $20.0\,\mathrm t$. "Holds $100\,\mathrm{kg}$": only flat and only just — $1885/981=1.92$ at $60\,\mathrm{kPa}$, under a factor of $2$ — while on a vertical face the four cups carry $942\,\mathrm N<981\,\mathrm N$ and the panel slips; $S=2$ vertically would need $124.9\,\mathrm{kPa}$, beyond the atmosphere. "$200\,\mathrm{kg}$ with a bigger pump": impossible by §9's ceiling — even a perfect vacuum gives $3183\,\mathrm N$ flat and $1592\,\mathrm N$ vertical, $324$ and $162\,\mathrm{kg}$ with no margin; it takes more cups (seventeen of these, vertically at $60\,\mathrm{kPa}$ and $S=2$). To be checkable the sheet must state the flow and the direction of motion behind a speed, whether a force is at the rod and at what pressure, and, for the lifter, the face's orientation, $\mu$ and surface, the vacuum a rating assumes and the minimum that is monitored, and the safety factor.

### Sources

- OpenStax, *University Physics Volume 1* (https://openstax.org/books/university-physics-volume-1, HTML) — §14.1 pressure as a scalar, $p=p_0+\rho gh$, and the atmosphere falling by $1/e$ every $8800\,\mathrm m$; §14.2 gauge and absolute pressure and the floor $-p_{\text{atm}}$; §14.3 Pascal's principle; §14.5 flow rate and continuity; §14.6 Bernoulli's equation; §14.7 Poiseuille's law and the Reynolds number, laminar below about $2000$ and turbulent above about $3000$; §12.3 the bulk moduli of water ($0.22\times10^{10}\,\mathrm{Pa}$) and steel ($16\times10^{10}\,\mathrm{Pa}$) and steel's Young's modulus ($20.0\times10^{10}\,\mathrm{Pa}$).
- OpenStax, *University Physics Volume 2* (https://openstax.org/books/university-physics-volume-2, HTML) — §1.4 $Q=mc\Delta T$ and water's $4186\,\mathrm{J/(kg{\cdot}K)}$; §2.1 the ideal gas law, in absolute pressure; §3.6 adiabatic compression, $pV^\gamma$ constant with $\gamma=1.4$ for a diatomic gas.
- OpenStax, *College Physics 2e*, [12.3 The Most General Applications of Bernoulli's Equation](https://openstax.org/books/college-physics-2e/pages/12-3-the-most-general-applications-of-bernoullis-equation) — power in fluid flow, $pQ$ as the power supplied to a fluid.
- NIST, *Guide for the Use of the International System of Units (SI)*, SP 811: [chapter 7](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-7-rules-and-style-conventions-expressing-values) — §7.4, no information attached to a unit symbol; [Appendix B.8](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8) — $1\,\mathrm{psi}=6.894\,757\times10^3\,\mathrm{Pa}$, $1\,\mathrm{bar}=10^5\,\mathrm{Pa}$, $1\,\mathrm{atm}=1.013\,25\times10^5\,\mathrm{Pa}$.
- Schmalz, manufacturer's vacuum pages (HTML): [Theoretical Holding Force of a Suction Cup](https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/theoretical-holding-force-of-a-suction-cup) — the load cases $m(g+a)S$ and $(m/\mu)(g+a)S$, safety factors of at least $1.5$ (smooth, dense parts) and $2.0$ (critical, porous, rough, oiled), reference friction coefficients to be confirmed by tests; [Holding force](https://www.schmalz.com/en-us/support/know-how/glossary/holding-force) — $F=\Delta p\times A$, a theoretical value quoted at $60\%$ relative vacuum; [Vacuum Generators](https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/vacuum-generators) — ejectors on the Venturi principle; [Vacuum Generator Selection](https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/vacuum-generator-selection) — a suction trial for porous parts.
- Aerolift, [Standards and safety regulations on vacuum lifting](https://www.aerolift.nl/en/standards-and-safety-regulations-vacuum-lifting/) (a vacuum-lifter maker's summary of EN 13155, HTML) — the load held for five minutes after a power failure, a non-return valve between pump and vacuum tank, a visible and audible alarm when the vacuum reaches the danger range, and dimensioning with a factor of two. The standard itself was not read.
- Within this wiki: [[02-foundations/engineering-math|0.5 §8]] for the ODEs and $\omega_n$; [[05-construction-robotics/site-engineering|2.5 Site Robotics]] for S1 and S2, and its §3 for the safe state; [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving §1]] for the latency overshoot; [[04-robotics/grasping|15. Grasping §2]] and §6 for friction; [[04-robotics/actuators-drives|10.5 §4]] for reflected inertia.
- H1 and V1 are course objects defined on this page, and every number on it was computed here from them, from S1 and S2, and from the sources above.

## 한국어

*[[02-foundations/engineering-math|0.5 공업수학 §8]]의 선형 미분방정식과 고유 진동수 $\omega_n=\sqrt{k/m}$ 위에, 그리고 [[02-foundations/lab-plants|0.6 Lab Plants]] 위에 선다. 0.6의 장치 여섯 가운데 유압 장치는 없으므로 이 페이지는 자기 대상 둘을 고정한다. 건설 트랙의 기계와 패널 밑에 깔리는 바닥이다. [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 §1]]이 S2에서 값을 매기는 밸브 지연도, [[05-construction-robotics/site-engineering|2.5 현장 로보틱스 §3]]이 S1에서 그 압력을 감시하는 흡착 파지도 이 페이지의 물리 위에 있다.*

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택 — 인식, 물체·장면 이해, 파지, 모션·과제 계획, 조작, 접촉·힘·촉각 피드백, 학습과 적응, 작업 완료 — 에서 이 페이지는 중장비의 구동 층과 파지 층 밑의 물리적 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). "*저 패널을 프레임에 설치해*"에서는 패널을 들어 올리는 유압 기계와 패널을 붙잡는 진공 파지다. 둘에 관한 주장은 이 산수로만 확인된다. $196\,\mathrm{kN}$을 밀 수 있는 붐 실린더는 최고 속도에서 펌프 일률의 $42\%$를 밸브에서 열로 바꾸고, S1의 $20\,\mathrm{kg}$ 패널을 안전율 $4.8$로 붙잡는 흡착 컵 넷은 펌프가 서면 요구 안전율 $2$를 $41\,\mathrm s$밖에 지키지 못한다. 기름 스프링은 [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 §1]]이 S2에서 값을 매기고 [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §1]]이 격차로 꼽는 $0.15\,\mathrm s$ 밸브–움직임 지연의 일부이고, 흡착 압력은 [[05-construction-robotics/site-engineering|2.5 현장 로보틱스 §3]]이 S1의 패널을 집는 동안 감시하는 변수이며, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지는 블록 1, 곧 토목 학위가 비워 둔 유체 동력을 메우는 기초의 바닥에 놓인다. 이 페이지를 마치면 펌프의 유량과 압력을 힘, 속도, 열, 강성, 유지 여유로 바꾸고, 사양서를 그 숫자로 따져 볼 수 있다.

> [!note] 처음이라면 · First pass
> 한 번에 75분 안팎, 두 번이면 된다. **첫 번째, 기름:** 이 페이지의 대상과 그림 — 굴착기 팔을 들어 올리는 붐 실린더 하나, S1의 외장 패널을 붙잡은 흡착 컵 넷 — 을 보고 §1–§5를 읽는다. 유압에 관한 모든 문장을 이루는 네 가지, 곧 압력·힘·유량·일률, 그리고 그것들을 잇는 회로다. 펌프는 유량을 정하고 하중은 압력을 정한다는 것을 제 말로 설명해 보는 것으로 첫 번째를 끝낸다. **두 번째, 스프링과 진공:** §6–§7(손실과 기름 스프링), §8(공기가 무른 이유), §9–§10(진공)을 읽고, 그림의 숫자를 모두 유도하는 계산 절, 그리고 기름 스프링을 건설 페이지가 값을 매기는 밸브 지연에 잇는 §11로 간다. 스스로 점검과 과제의 해석 항목으로 마무리한다. §12는 빠진 것을 적는다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]에는 유압이나 공압 장치가 없다. P1부터 P6까지는 신경망, 팔, 핸들, 히터, 거리 센서, 카트다. 그래서 이 페이지는 자기 대상 둘을 고정한다. 숫자는 **교과 숫자**다. 5톤급 기계와 20 kg 패널에 맞는 크기로 골라 여기서 고정했고, 어떤 제품을 재거나 사양에서 옮긴 값이 아니다. 다른 페이지는 이 숫자를 바꾸지 않는다.

**H1 — 붐 실린더와 그 회로.** 복동 실린더 하나가 S2 급 굴착기, 곧 [[05-construction-robotics/site-engineering|2.5 현장 로보틱스]]의 5톤급 기계의 붐을 들어 올린다. 정용량 펌프가 방향 제어 밸브를 거쳐 기름을 보내고, 릴리프 밸브가 압력의 상한을 막으며, 기름은 탱크로 돌아온다. 팔, 버킷, 흙을 가득 담은 버킷은 버킷 날 끝의 점질량 하나로 뭉친다. P2의 링크를 점질량으로 둔 것과 같은 단순화다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $D,\ d,\ s$ | $100\,\mathrm{mm}$, $60\,\mathrm{mm}$, $0.80\,\mathrm{m}$ | 보어(피스톤 지름), 로드 지름, 행정 |
| $V_d,\ N$ | $25\,\mathrm{cm^3/rev}$, $2400\,\mathrm{rev/min}$ | 펌프의 한 바퀴당 배제 용적과 축 회전수. 그래서 $Q=60\,\mathrm{L/min}=1.0\times10^{-3}\,\mathrm{m^3/s}$, 누설은 무시(§5) |
| $p_r$ | $25\,\mathrm{MPa}$ | 릴리프 밸브 설정 압력(§5) |
| $A_v,\ C_d$ | $20\,\mathrm{mm^2}$, $0.65$ | 명령을 끝까지 준 방향 제어 밸브: 계량 모서리 P→A와 B→T 각각의 열림 면적과 유량 계수(§6) |
| $L_h,\ d_h$ | $3.0\,\mathrm{m}$, $20\,\mathrm{mm}$ | 밸브에서 실린더로 가는 호스 두 가닥 각각의 길이와 안지름 |
| $\rho,\ \eta$ | $870\,\mathrm{kg/m^3}$, $0.040\,\mathrm{Pa{\cdot}s}$ | 작동 온도에서 기름의 밀도와 점성 계수 |
| $\beta_e$ | $1.0\,\mathrm{GPa}$ | 기름, 호스, 녹지 않은 공기를 한데 묶은 유효 체적 탄성 계수(§7) |
| $c,\ V_o$ | $1900\,\mathrm{J/(kg{\cdot}K)}$, $50\,\mathrm{L}$ | 기름의 비열, 그리고 탱크와 배관에 든 기름의 양(§4) |
| $m_a,\ n$ | $600\,\mathrm{kg}$, $6$ | 날 끝에 뭉친 팔·버킷·흙. 쓰는 자세에서 날 끝은 로드가 늘어나는 속도의 $n$배로 올라간다 |

**V1 — S1 패널용 진공 리프터.** [[05-construction-robotics/site-engineering|2.5]]의 S1 외장 패널 — $m=20\,\mathrm{kg}$, 무게 $196\,\mathrm{N}$ — 의 면에 붙는 흡착 컵 넷이다. [[05-construction-robotics/hrc-worker-centered|6. HRC]]가 파지점을 두는 무게중심에 대해 대칭으로 놓으므로 무게가 컵 배치에 모멘트를 걸지 않는다. 진공 펌프가 컵과, 컵에 이어진 작은 진공 탱크를 체크 밸브(역지 밸브) 너머로 비우고, 펌프가 서면 체크 밸브가 컵 쪽의 진공을 지킨다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $n_c,\ D_c$ | $4$, $100\,\mathrm{mm}$ | 컵의 개수, 그리고 각 컵의 밀봉선 지름 |
| $\Delta p_w$ | $60\,\mathrm{kPa}$ | 작동 진공도: 컵 안을 대기보다 $60\,\mathrm{kPa}$ 낮게 유지(§1, §9) |
| $\mu$ | $0.5$ | 컵 테두리와 패널 면 사이의 마찰 계수(§9) |
| $S$ | $2$ | 요구 안전율(§9) |
| $V_s,\ Q_L$ | $2.0\,\mathrm{L}$, $1.0\,\mathrm{L/min}$ | 체크 밸브 안쪽에 갇힌 부피, 그리고 그리로 새어 드는 누설량(대기압에서 잰 부피)(§10) |
| $p_{\text{atm}}$ | $101.325\,\mathrm{kPa}$ | 대기의 절대 압력, 표준값 |

모델링 선택 셋을 한 번만 적는다. **하중은 중력뿐이다**: 붐은 일정한 속도로 올라가므로 로드는 지렛대를 거친 날 끝의 무게만 진다. 굴착력은 3번 페이지의 주제다. **지렛대는 이상적이다**: 쓰는 자세에서 날 끝은 똑바로 위로, 로드의 $n=6$배 속도로 움직이고 핀에서 잃는 것이 없다. **패널은 면이 연직인 채로 매달린다**: S1의 지지 단계에서 벽 앞에 설 때처럼. 그래서 컵은 무게를 마찰로 진다. 눕혀 드는 패널은 §9의 더 쉬운 경우다. H1의 보어와 V1의 컵은 일부러 같은 $100\,\mathrm{mm}$ 원을 쓴다. §9가 두 압력을 같은 면적 위에 올려놓기 위해서다.

*범위: 이 페이지는 건설·로보틱스 논문을 읽는 사람에게 필요한 유체 동력의 물리 — 압력과 그 단위, 실린더의 두 면적에 걸리는 압력의 힘, 유량과 속도, 유압 동력과 효율과 열, 기본 회로, 오리피스 손실, 압축성과 기름 스프링, 공기가 무른 이유, 진공으로 붙잡기 — 를 H1과 V1 위에서 가르친다. 밸브나 펌프의 설계, 뭉친 지연 하나를 넘는 밸브 동역학, 부하 감응과 전자 유압 제어, 작동유와 오염, 공압 회로 설계는 가르치지 않는다. 그 가운데 가까운 것들이 어디에 있는지는 §12가 말한다. S2의 지연은 [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 §1]]이 값을 매기고, 2차 플랜트의 제어는 [[04-robotics/control-theory-ce397|5. 제어 이론]]의 몫이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 562" style="max-width:100%;height:auto" role="img" aria-label="위: 전개 명령의 방향 제어 밸브를 거쳐 기름을 받는 H1 붐 실린더, 행정 중간. 펌프의 60 L/min, 7.75 MPa는 밸브의 P→A 모서리에서 2.57 MPa를 잃고, 헤드측은 5.17 MPa, 로드측은 1.05 MPa로 38.4 L/min을 돌려보내며, 로드는 35.3 kN의 부하를 0.127 m/s로 민다. 25 MPa 릴리프는 닫혀 있다. 막대 하나가 펌프의 7.75 MPa를 부하 4.50, 배압 0.67, 밸브 2.57로 나누어 25 MPa 릴리프와 견준다. 아래: S1의 연직 패널 위 V1의 100 mm 컵 넷. 마찰 유지 용량은 진공도에 비례해 오르며, 작동 60 kPa에서 942 N으로 안전율 4.8이고, 대기압에서 1592 N으로 멈춘다. 펌프가 선 뒤 41 s에 S = 2가 되는 25.0 kPa에 닿는다.">
  <defs><marker id="fpAk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" font-weight="600" fill="currentColor">H1이 전개 명령으로 붐을 올린다</text>
  <text x="250" y="40" font-size="11" fill="currentColor">보어 100, 로드 60 mm, 행정 0.80 m</text>
  <rect x="250" y="57.5" width="200" height="25" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <rect x="251.5" y="59" width="95.5" height="22" fill="currentColor" fill-opacity="0.22"/>
  <rect x="347" y="57.5" width="6" height="25" fill="currentColor"/>
  <rect x="353" y="62.5" width="187" height="15" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <circle cx="540" cy="70" r="4" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="548,90.5 508,90.5" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpAk)"/>
  <text x="548" y="104.5" font-size="11" text-anchor="end" fill="currentColor">F<tspan dy="3" font-size="10">L</tspan><tspan dy="-3"> = 35.3 kN</tspan></text>
  <polyline points="458,50.5 498,50.5" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#fpAk)"/>
  <text x="458" y="40" font-size="11" fill="currentColor">v = 0.127 m/s</text>
  <polyline points="200,150 200,112 262,112 262,82.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <polyline points="236,150 236,126 438,126 438,82.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="262,100 262,90" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpAk)"/>
  <polyline points="398,126 378,126" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpAk)"/>
  <text x="268" y="100" font-size="11" fill="currentColor">헤드측 5.17 MPa</text>
  <text x="268" y="112" font-size="10" fill="currentColor">60 L/min 유입</text>
  <text x="444" y="142" font-size="11" fill="currentColor">로드측 1.05 MPa</text>
  <text x="444" y="154" font-size="10" fill="currentColor">38.4 L/min 유출</text>
  <rect x="182" y="150" width="72" height="36" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="200,182 200,156" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#fpAk)"/>
  <polyline points="236,154 236,180" fill="none" stroke="currentColor" stroke-width="1.3" marker-end="url(#fpAk)"/>
  <text x="187" y="164" font-size="10" fill="currentColor">A</text>
  <text x="242" y="164" font-size="10" fill="currentColor">B</text>
  <text x="187" y="182" font-size="10" fill="currentColor">P</text>
  <text x="242" y="182" font-size="10" fill="currentColor">T</text>
  <text x="264" y="160" font-size="11" fill="currentColor">전개 명령의 밸브</text>
  <text x="264" y="174" font-size="11" fill="currentColor">P→A 강하 2.57 MPa</text>
  <text x="264" y="188" font-size="11" fill="currentColor">B→T 강하 1.05 MPa</text>
  <polyline points="200,222 200,186" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="200" cy="236" r="14" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <path d="M 194 240 L 200 229 L 206 240 Z" fill="currentColor"/>
  <polyline points="200,250 200,262" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="180" y="234" font-size="11" text-anchor="end" fill="currentColor">펌프</text>
  <text x="180" y="247" font-size="11" text-anchor="end" fill="currentColor">60 L/min</text>
  <text x="194" y="205" font-size="11" text-anchor="end" fill="currentColor">7.75 MPa</text>
  <polyline points="236,186 236,262" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
  <polyline points="200,212 128,212" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <rect x="104" y="202" width="24" height="30" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <polyline points="116,228 116,208" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#fpAk)"/>
  <path d="M 104 217 L 99 214 L 93 220 L 87 214 L 81 220 L 76 217" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="116,232 116,262" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 3"/>
  <text x="12" y="190" font-size="11" fill="currentColor">릴리프 25 MPa</text>
  <text x="12" y="203" font-size="10" fill="currentColor">닫힘: 7.75 &lt; 25</text>
  <polyline points="96,262 96,282 330,282 330,262" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="98,270 328,270" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <text x="338" y="278" font-size="11" fill="currentColor">탱크, 게이지 0 MPa</text>
  <text x="12" y="304" font-size="11" fill="currentColor">펌프의 7.75 MPa가 쓰이는 곳, 릴리프 25 MPa와 견주어</text>
  <rect x="40" y="324" width="89.9" height="14" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.8"/>
  <rect x="129.9" y="324" width="13.5" height="14" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="0.8"/>
  <rect x="143.4" y="324" width="51.5" height="14" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.8"/>
  <rect x="194.9" y="324" width="345.1" height="14" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <polyline points="540,318 540,344" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <polyline points="40,338 40,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="353" font-size="10" text-anchor="middle" fill="currentColor">0</text>
  <polyline points="140,338 140,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="353" font-size="10" text-anchor="middle" fill="currentColor">5</text>
  <polyline points="240,338 240,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="353" font-size="10" text-anchor="middle" fill="currentColor">10</text>
  <polyline points="340,338 340,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="353" font-size="10" text-anchor="middle" fill="currentColor">15</text>
  <polyline points="440,338 440,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="440" y="353" font-size="10" text-anchor="middle" fill="currentColor">20</text>
  <polyline points="540,338 540,342" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="540" y="353" font-size="10" text-anchor="end" fill="currentColor">릴리프 25 MPa</text>
  <text x="85" y="320" font-size="10" text-anchor="middle" fill="currentColor">부하 4.50</text>
  <text x="200.9" y="335" font-size="10" fill="currentColor">← 밸브 2.57, 배압 0.67</text>
  <text x="12" y="370" font-size="11" fill="currentColor">입력 7.75 kW, 팔에 4.50 kW (58 %), 열 3.25 kW</text>
  <polyline points="8,382 552,382" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="12" y="400" font-size="12" font-weight="600" fill="currentColor">V1이 S1 패널을 든다, 면은 연직</text>
  <rect x="20" y="412" width="84" height="92" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="44" cy="432" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="44" cy="468" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="80" cy="432" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="80" cy="468" r="9" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="62" cy="450" r="2.5" fill="currentColor"/>
  <polyline points="62,450 62,494" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#fpAk)"/>
  <text x="67" y="492" font-size="10" fill="currentColor">196 N</text>
  <text x="20" y="520" font-size="11" fill="currentColor">S1 패널, 20 kg</text>
  <text x="20" y="533" font-size="11" fill="currentColor">컵 4개 Ø100 mm</text>
  <text x="20" y="546" font-size="11" fill="currentColor">μ = 0.5</text>
  <polyline points="220,510 544,510" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#fpAk)"/>
  <polyline points="220,510 220,404" fill="none" stroke="currentColor" stroke-width="1.1" marker-end="url(#fpAk)"/>
  <text transform="translate(212,455) rotate(-90)" font-size="10" text-anchor="middle" fill="currentColor">μ·n·Δp·A (N)</text>
  <polyline points="220,510 220,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="220" y="524" font-size="10" text-anchor="middle" fill="currentColor">0</text>
  <polyline points="292.7,510 292.7,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="292.7" y="524" font-size="10" text-anchor="middle" fill="currentColor">25</text>
  <polyline points="365.5,510 365.5,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="365.5" y="524" font-size="10" text-anchor="middle" fill="currentColor">50</text>
  <polyline points="438.2,510 438.2,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="438.2" y="524" font-size="10" text-anchor="middle" fill="currentColor">75</text>
  <polyline points="510.9,510 510.9,514" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="510.9" y="524" font-size="10" text-anchor="middle" fill="currentColor">100</text>
  <text x="380" y="537" font-size="11" text-anchor="middle" fill="currentColor">대기보다 낮춘 진공도 Δp (kPa)</text>
  <polyline points="220,484.6 540,484.6" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <polyline points="220,497.3 540,497.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.8"/>
  <text x="540" y="481.6" font-size="10" text-anchor="end" fill="currentColor">S = 2 (392 N)</text>
  <text x="540" y="494.3" font-size="10" text-anchor="end" fill="currentColor">S = 1 (196 N)</text>
  <polyline points="220,510 514.8,407" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="514.8,407 514.8,510" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/>
  <circle cx="394.5" cy="449" r="3.5" fill="currentColor"/>
  <text x="386.5" y="443" font-size="11" text-anchor="end" fill="currentColor">60 kPa: 942 N, S = 4.8</text>
  <circle cx="514.8" cy="407" r="3.5" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="506.8" y="404" font-size="11" text-anchor="end" fill="currentColor">대기압 한계: 1592 N, S = 8.1</text>
  <circle cx="292.7" cy="484.6" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="256.3" cy="497.3" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="287.7" y="479.6" font-size="10" text-anchor="end" fill="currentColor">25.0</text>
  <text x="251.3" y="492.3" font-size="10" text-anchor="end" fill="currentColor">12.5</text>
  <text x="220" y="554" font-size="11" fill="currentColor">펌프 정지: 60 → 25.0 kPa에 41 s, → 12.5 kPa에 56 s</text>
</svg>

명령을 끝까지 받아 붐을 올리는 H1과 S1의 패널을 붙잡은 V1을, 둘 다 계산 절의 숫자로 그렸다. 위에서는 펌프의 $60\,\mathrm{L/min}$이 밸브의 P→A 모서리에서 $2.57\,\mathrm{MPa}$를 내주고 헤드측에 닿고, 로드측은 B→T를 거쳐 $1.05\,\mathrm{MPa}$로 $38.4\,\mathrm{L/min}$을 돌려보내며, 막대가 펌프의 $7.75\,\mathrm{MPa}$를 부하 $4.50$, 배압 $0.67$, 밸브 $2.57$로 나누는데, $25\,\mathrm{MPa}$ 릴리프에는 한참 못 미치고 $7.75\,\mathrm{kW}$ 가운데 $4.50$이 팔에 닿는다. 아래에서는 연직 패널 위 컵의 마찰 유지 용량이 진공도에 비례해 오르다 대기압의 $1592\,\mathrm{N}$에서 멈추고, 작동 진공 $60\,\mathrm{kPa}$에서는 $942\,\mathrm{N}$으로 안전율이 $4.8$이며, 펌프가 서면 누설이 $41\,\mathrm{s}$ 만에 진공을 $S=2$의 경계인 $25.0\,\mathrm{kPa}$까지 끌어내린다.

### 1. 압력, 그 영점, 그리고 파스칼의 원리

*한 문장으로:* 압력은 단위 면적당 힘이고, 영점 없이는 아무 뜻이 없는 숫자이며, 가둔 채 정지한 유체에서는 그 변화가 젖은 모든 면에 한꺼번에 닿는다 — 이 페이지의 유압과 진공 계산은 모두 이 세 사실 위에 선다.

정지한 유체는 전단 응력을 버티지 못한다. 옆으로 밀면 흘러 버린다. 그러니 유체가 벽에 줄 수 있는 힘은 벽에 수직인 힘, 곧 미는 힘뿐이고, 벽의 한 조각을 얼마나 세게 미는지는 조각이 클수록 커진다. 조각이 아니라 유체에 속하는 양은 단위 면적당 미는 힘이다.

> **압력의 정의.** **압력**(pressure)은 *한 점에서 유체가 갖는 스칼라 성질*이다. 그 점을 지나는 어떤 면이든, 유체가 그 면의 단위 면적마다 가하는 수직력이다. 정의 조건 넷. **수직** 성분만 센다. 정지한 유체는 전단을 싣지 않기 때문이다. **단위 면적당**으로 잡되, 그 안에서 압력이 어디나 같을 만큼 작은 조각에서 잰다. 정지한 유체의 한 점에서는 **모든 방향으로 같다**. 그래서 압력에는 제 방향이 없다(OpenStax 14.1: 압력은 스칼라다). 그리고 값은 **영점**과 함께일 때만 뜻이 있다. 절대 압력은 완전한 진공에서, 게이지 압력은 그 자리의 대기압에서 센다.
>
> $$p=\frac{F_\perp}{A},\qquad p_{\text{abs}}=p_g+p_{\text{atm}}$$
>
> $F_\perp$는 면적 $A$에 걸리는 수직력, $p_g$는 게이지 압력, $p_{\text{atm}}$은 대기의 절대 압력이다(둘째 관계는 OpenStax 14.2). 단위는 파스칼, $1\,\mathrm{Pa}=1\,\mathrm{N/m^2}$이다. 작은 단위여서 — $80\,\mathrm{g/m^2}$ 종이 한 장을 평평하게 놓으면 $0.08\times9.81=0.78\,\mathrm{Pa}$로 누른다 — 유압에서는 MPa와 bar($1\,\mathrm{bar}=10^5\,\mathrm{Pa}$)를, 어떤 카탈로그는 psi($1\,\mathrm{psi}=6894.757\,\mathrm{Pa}$, NIST SI 가이드 부록 B.8)를 쓴다.
>
> - **예**: H1의 릴리프 설정 $p_r=25\,\mathrm{MPa}$(게이지)는 $250\,\mathrm{bar}$, $3626\,\mathrm{psi}$다. V1의 작동 진공, 곧 대기보다 $60\,\mathrm{kPa}$ 낮은 압력은 게이지 압력 $p_g=-60\,\mathrm{kPa}$이고 절대 압력 $101.325-60=41.3\,\mathrm{kPa}$다.
> - **비예**: "$150\,\mathrm{kPa}$의 진공". 게이지 압력은 절대 압력이 0이 되는 $-p_{\text{atm}}$까지만 내려갈 수 있다(OpenStax 14.2). 유체는 밀 수는 있어도 당기지는 못하므로, 어떤 펌프도 그 너머로 가지 못한다. 이것이 §9의 천장이다.
> - **비예**: "$60\,\mathrm{kPag}$". 단위 기호는 양에 대한 정보를 싣지 않는다(NIST SI 가이드 §7.4). 그래서 영점은 단위에 붙이지 않고 양과 함께 부른다 — "게이지 압력 $p_g=-60\,\mathrm{kPa}$".
> - **왜 중요한가**: 유압의 힘은 게이지 압력으로 계산한다. 대기가 피스톤의 양쪽을 똑같이 눌러 상쇄되기 때문이다. 반면 기체 법칙에는 절대 압력이 필요하다(§8, §10). 영점을 틀리면 약 $101\,\mathrm{kPa}$가 어긋나는데, $25\,\mathrm{MPa}$에 대해서는 $0.4\%$지만 진공 리프터에서는 신호 전체보다 크다.

정지한 유체는 한 점에서 모든 방향으로 똑같이 밀고, 압력이 높이에 따라 달라지는 것은 위에 얹힌 유체의 무게, $p=p_0+\rho gh$ 때문뿐이다(OpenStax 14.1). 그러니 닫힌 기름 덩어리의 한 점에서 압력을 올리면 기름이 닿는 모든 곳에서 압력이 오른다.

> **파스칼의 원리의 정의.** **파스칼의 원리**(Pascal's principle)는 *가두어진 채 정지한 유체에 관한 명제*다. 그 안 어디에 가한 압력 변화든 줄지 않고 유체의 모든 부분과 용기의 벽에 전달된다(OpenStax 14.3). 정의 조건 셋. 유체가 **갇혀** 있어 압력이 벽 말고는 갈 데가 없다. 유체가 **정지해** 있거나, 좁은 곳을 밀고 지나가느라 압력을 쓰지 않을 만큼 느리게 움직인다(§6). 그리고 **높이** 차가 작거나 $\rho gh$로 따로 계산한다. 이 조건에서 같은 유체 위의 면적 $A_1$, $A_2$ 피스톤 둘은 면적의 비율대로 힘을 진다.
>
> $$\frac{F_1}{A_1}=\frac{F_2}{A_2}$$
>
> 두 힘 모두 하나의 압력에 제 면적을 곱한 것이기 때문이다. 이렇게 힘은 불릴 수 있어도 일은 불릴 수 없다. 한 피스톤이 밀어 넣은 부피만큼 다른 피스톤이 자리를 내주므로, 큰 피스톤은 면적의 비율만큼 덜 움직인다.
>
> - **예**: H1의 압력 라인과 헤드측 실(chamber)은 한 덩어리의 기름이다. 그래서 릴리프가 허락하는 $25\,\mathrm{MPa}$가 헤드측 면 전체 $7854\,\mathrm{mm^2}$에 걸려 $196\,\mathrm{kN}$ — 20톤의 무게 — 가 된다. 반면 탱크와 실린더 사이 $3\,\mathrm{m}$의 높이는 $\rho gh=870\times9.81\times3=25.6\,\mathrm{kPa}$, 그 $0.1\%$밖에 안 된다.
> - **비예**: 명령을 끝까지 받은 H1의 밸브를 지나 흐르는 기름. 정지해 있지 않고, P→A 모서리가 지나는 길에 압력에서 $2.57\,\mathrm{MPa}$를 떼어 간다(§6). 그래서 펌프가 $7.75\,\mathrm{MPa}$로 일하는 동안 헤드측 실은 $5.17\,\mathrm{MPa}$를 본다. 파스칼의 원리는 펌프에서 밸브까지, 그리고 밸브에서 피스톤까지는 성립하지만 밸브를 가로질러서는 성립하지 않는다.
> - **왜 중요한가**: 호스가 모퉁이를 돌아 구동기가 있는 곳 어디로든 힘을 나를 수 있는 이유이고, 유압 기계가 힘을 불리는 기계인 이유다. 그리고 일은 불리지 못하므로, 같은 이유로 속도를 나누는 기계이기도 하다(§3).

### 2. 압력에서 힘으로: 실린더에는 면적이 둘이다

실린더의 정격 힘은 압력 곱하기 면적인데, 복동 실린더에는 면적이 둘이라 미는 힘과 당기는 힘이 다르다. 어느 쪽인지 말하지 않는 정격은 정격이 아니다. 복동 실린더는 피스톤이 둘로 나눈 통이고, 양 끝에 포트가 있어 어느 쪽이든 압력을 걸 수 있다. 헤드측 — 로드가 없는 쪽 — 에서는 기름이 피스톤 면 전체를 민다. 로드측에서는 로드가 남긴 고리 모양의 면, 곧 환형 면적만 민다.

> **실린더 유효 면적의 정의.** 복동 실린더의 **유효 면적**(effective areas)은 보어와 로드가 정하는 *기하 상수 둘*이다. 기름 압력이 실린더를 늘일 때 누르는 헤드측 면적 $A_{\text{cap}}$과, 줄일 때 누르는 환형 면적 $A_{\text{ann}}$이다. 정의 조건 셋. 헤드측 면적은 **보어 전체**다. 환형 면적은 **보어에서 로드를 뺀 것**이다. 그쪽에서는 로드의 단면이 기름에 젖지 않기 때문이다. 그리고 피스톤에 걸리는 알짜 힘은 두 압력 힘의 **차**다. 두 실이 동시에 밀기 때문이다. 둘의 비, **면적비** $\varphi$는 언제나 1보다 크다.
>
> $$A_{\text{cap}}=\frac{\pi D^2}{4},\qquad A_{\text{ann}}=\frac{\pi(D^2-d^2)}{4},\qquad F=p_{\text{cap}}A_{\text{cap}}-p_{\text{rod}}A_{\text{ann}},\qquad \varphi=\frac{A_{\text{cap}}}{A_{\text{ann}}}$$
>
> $D$는 보어, $d$는 로드 지름, $p_{\text{cap}}$과 $p_{\text{rod}}$는 두 실의 게이지 압력, $F$는 로드를 바깥으로 미는 알짜 힘이다(실 마찰은 무시). 그러니 실린더는 힘의 원천이고, 그 힘을 정하는 것은 로드의 위치가 아니라 두 압력이다.
>
> - **예**: H1. $A_{\text{cap}}=\pi(0.1\,\mathrm m)^2/4=7.854\times10^{-3}\,\mathrm{m^2}$, $A_{\text{ann}}=\pi(0.1^2-0.06^2)\,\mathrm{m^2}/4=5.027\times10^{-3}\,\mathrm{m^2}$, $\varphi=1.5625$. 릴리프 압력에서 $25\times10^6\times7.854\times10^{-3}=196.3\,\mathrm{kN}$으로 밀고 $125.7\,\mathrm{kN}$으로 당긴다.
> - **비예**: "로드측이 막혀 있으니 안전하다." 로드측을 가두고 로드에 아무 하중도 없이 헤드측을 $25\,\mathrm{MPa}$로 밀면, 로드측이 헤드측과 힘의 균형을 맞춰야 한다. $p_{\text{rod}}=\varphi\,p_{\text{cap}}=1.5625\times25=39.1\,\mathrm{MPa}$로 릴리프 설정보다 높다. 릴리프는 압력 라인만 지킨다. 실린더는 제 압력을 불릴 수 있다.
> - **왜 중요한가**: 같은 펌프 압력이 두 가지 힘을 주고, (§3) 같은 펌프 유량이 두 가지 속도를 준다. 그래서 실린더에 관한 주장은 어느 쪽으로 움직이는지를 밝혀야 한다. 그리고 식 어디에도 로드의 위치는 없다. 실린더는 힘의 원천이고, 그 위치는 유량이 시간에 따라 쌓인 결과다(§3).

**로드가 져야 하는 것.** H1의 하중은 로드가 아니라 버킷 날 끝에 있다. $m_a=600\,\mathrm{kg}$이 로드의 $n=6$배 속도로 움직인다. 잃는 것 없는 지렛대는 일률을 그대로 넘겨주므로, 로드 힘 곱하기 로드 속도는 날 끝의 무게 곱하기 날 끝 속도와 같다.

$$F_L\,v=m_ag\,(n\,v)\quad\Rightarrow\quad F_L=n\,m_ag=6\times600\times9.81=35.3\,\mathrm{kN}$$

그래서 로드측이 탱크로 열린 채 헤드측은 $p_{\text{hold}}=F_L/A_{\text{cap}}=35\,316/7.854\times10^{-3}=4.50\,\mathrm{MPa}$를 버텨야 한다. 릴리프 설정의 $18\%$다. 같은 일률 논리가 §7에서 로드가 느끼는 팔의 질량을 준다. 붐을 내리는 것은 중력이 거드는 수축이다. 이제 하중이 로드를 밀어 넣고, 속도를 붙잡는 것은 펌프가 아니라 헤드측에서 빠져나가는 기름을 조르는 일이다 — 밸브의 출구 모서리가 브레이크 노릇을 한다(§6).

### 3. 유량과 속도: 한 행정에 걸리는 시간

붐이 얼마나 빨리 오르고 한 행정에 얼마가 걸리는지는 펌프의 압력이 아니라 유량이 정한다. 펌프는 힘으로 밀지 않는다. 부피를 보낸다. 실린더가 그 부피로 무엇을 하는지는 기하가 정한다. 피스톤은 그 부피가 들어설 자리만큼 움직여야 한다.

> **체적 유량의 정의.** **체적 유량**(volumetric flow rate) $Q$는 *비율*이다. 한 단면을 단위 시간에 지나는 유체의 부피이고(OpenStax 14.5), 단위는 $\mathrm{m^3/s}$, 유압에서는 흔히 L/min이다. $1\,\mathrm{L/min}=1.667\times10^{-5}\,\mathrm{m^3/s}$. 이 페이지처럼 쓰기 위한 정의 조건 셋. 유체를 **비압축성**으로 다루므로 부피가 보존된다. 통로가 **밀봉되어** 있으므로 누설로 빠지는 부피가 없다. 흐름이 **정상 상태**이므로 직렬로 이어진 통로에 들어간 만큼이 같은 비율로 나온다. 그러면 연속 방정식이 성립한다 — 직렬의 모든 단면을 같은 $Q$가 지난다 — 그리고 면적 $A$인 단면에서 평균 속도는
>
> $$v=\frac{Q}{A}$$
>
> 다. 시간 $\Delta t$ 동안 지나간 부피 $Q\,\Delta t$가 그 단면의 길이 $v\,\Delta t$를 채우기 때문이다.
>
> - **예**: 늘어나는 H1. 펌프의 $1.0\times10^{-3}\,\mathrm{m^3/s}$가 헤드측 면적 $7.854\times10^{-3}\,\mathrm{m^2}$로 들어가면 로드는 $0.127\,\mathrm{m/s}$로 움직이고, $0.80\,\mathrm{m}$ 행정에 $6.28\,\mathrm{s}$가 걸린다. 줄어들 때는 같은 유량이 환형 면적으로 들어가 $0.199\,\mathrm{m/s}$, $4.02\,\mathrm{s}$다. 속도비도 $\varphi=1.5625$이고, 방향만 반대다.
> - **비예**: "귀환 라인에는 펌프 유량이 흐른다." 줄어들 때 헤드측은 $0.199\times7.854\times10^{-3}=1.5625\times10^{-3}\,\mathrm{m^3/s}$, 곧 $93.75\,\mathrm{L/min}$으로 비는데, 펌프 $60$의 $\varphi$배다. 늘어날 때 로드측은 $38.4\,\mathrm{L/min}$만 돌려보낸다. 펌프에 맞춰 고른 밸브와 귀환 라인은 줄어드는 실린더에는 작다.
> - **왜 중요한가**: 유량이 속도를, 압력이 힘을 정하고, 일률(§4)이나 릴리프 밸브(§5)가 둘을 묶기 전까지 둘은 따로 논다. 실린더를 빠르게 하려면 압력이 아니라 유량이 더 필요하다.

행정 시간은 쓸고 지나가는 부피를 유량으로 나눈 것, $t=sA/Q$다. H1의 헤드측은 $0.80\times7.854\times10^{-3}=6.28\times10^{-3}\,\mathrm{m^3}$, 곧 $6.28\,\mathrm{L}$를 쓸고, 펌프의 초당 $1.0\,\mathrm{L}$가 그것을 $6.28\,\mathrm{s}$에 채운다. 날 끝에서는 지렛대가 속도를 $n$배로 불려, 팔은 $6\times0.127=0.764\,\mathrm{m/s}$로 올라간다. 하중이 요구하는 압력이 릴리프 설정 아래에 있는 한 정용량 펌프는 하중과 상관없이 같은 속도를 준다. 하중이 바꾸는 것은 압력이지 초당 부피가 아니기 때문이다. 거꾸로 읽으면 실린더는 적분기다. 그 위치는 받은 유량의 누적, $x(t)=x(0)+\frac{1}{A}\int_0^tQ\,dt$이다. 그래서 유량을 정하는 밸브는 속도를 정하고, 변하는 하중에 맞서 위치를 지키려면 위치에 대해 닫은 루프가 필요하다. 0.5가 P4에 대해 그리는, 루프 속의 적분기와 같은 구조다([[02-foundations/engineering-math|0.5 §8]]). 눈여겨볼 가정 하나는 비압축성이다. §7이 그것을 풀고, 움직임의 처음 수십 밀리초가 바로 그 가정을 깬다(§11).

### 4. 유압 동력, 효율, 그리고 열

유압 기계의 펌프는 킬로와트 단위의 일률을 내고, 그것이 어디로 가는지 — 하중인가, 뜨거워지는 기름인가 — 가 이 절의 물음이다. 힘과 속도를 곱하면 기계 일률이고, 실린더에서는 둘 다 기름에서 나온다. $F\,v=(pA)(Q/A)=pQ$. 면적이 약분된다는 것은 일률을 기름 자체가 나른다는 뜻이다. 압력의 단위는 부피당 에너지와 같다, $1\,\mathrm{Pa}=1\,\mathrm{N/m^2}=1\,\mathrm{J/m^3}$. 그러니 어떤 압력에서 초당 부피가 흐르는 것은 초당 에너지가 흐르는 것이다. OpenStax의 College Physics는 $pQ$를 펌프가 유체에 공급하는 일률로 쓴다(College Physics 2e §12.3).

> **유압 동력의 정의.** **유압 동력**(hydraulic power)은 흐르는 액체가 나르는 *에너지 전달률*이다. 한 요소 양단의 압력 차에 그 요소를 지나는 유량을 곱한 것이다. 정의 조건 셋. 압력은 요소의 입구와 출구 사이의 **차**다 — 펌프라면 출구 대 탱크. 유량은 그 요소를 **지나는** 유량이다. 그리고 액체를 비압축성으로 다루므로 압력은 단위 부피당 에너지이고, 짜내는 데 저장되는 것이 없다.
>
> $$P=\Delta p\,Q$$
>
> $\Delta p$가 파스칼, $Q$가 $\mathrm{m^3/s}$이면 $P$는 와트다. 실린더에서는 이것이 기계 일률과 같다. $F\,v=pQ$이기 때문이다.
>
> - **예**: 펌프 유량을 다 받아 팔을 올리는 H1. 헤드측에 $p_{\text{hold}}Q=4.50\times10^6\times1.0\times10^{-3}=4.50\,\mathrm{kW}$가 들어가고, 이것은 $F_Lv=35\,316\times0.1273$과도, 날 끝의 무게 곱하기 그 속도 $5886\times0.764$와도 같다. 같은 $4.50\,\mathrm{kW}$를 세 번 센 것이다.
> - **비예**: 압력만으로는 일률이 아니다. 팔을 $4.50\,\mathrm{MPa}$로 가만히 붙잡은 H1은 실린더로 가는 유량이 $Q=0$이어서, 압력이 아무리 높아도 일률을 내지 않는다. 그리고 유량 전부가 릴리프 밸브를 건너가는 $25\,\mathrm{MPa}$의 펌프는 $25\,\mathrm{kW}$를 오로지 열에 준다(§5).
> - **왜 중요한가**: 흐름이 지나는 모든 압력 강하는 $\Delta p\,Q$만큼의 일률을 열로 바꾼다. 그래서 회로의 효율은 그 압력들에서 읽히고, 냉각 요구는 그 손실에서 읽힌다.

**효율과 열.** 회로의 효율은 부하에 닿는 일률을 펌프가 넣는 일률로 나눈 것, $\eta=P_{\text{out}}/P_{\text{in}}$이다. 나머지는 열이고, 흐름의 길을 따라가며 압력 강하마다 그곳을 지나는 유량을 곱해 찾는다. 열은 기름을 데운다. 냉각이 없으면 $Q_{\text{heat}}=mc\,\Delta T$(OpenStax University Physics 2권 §1.4)가 데워지는 속도를 준다.

$$\frac{dT}{dt}=\frac{P_{\text{heat}}}{\rho V_o\,c}$$

기름의 열용량, 곧 질량 $\rho V_o$ 곱하기 비열 $c$가 그 일률을 받아들이기 때문이다. H1의 기름 $50\,\mathrm{L}$는 $43.5\,\mathrm{kg}$이고, $c=1900\,\mathrm{J/(kg{\cdot}K)}$ — 교과 값으로, OpenStax 표가 물에 주는 $4186\,\mathrm{J/(kg{\cdot}K)}$의 절반이 조금 못 된다 — 에서 켈빈당 $82.7\,\mathrm{kJ}$를 받는다. 그래서 막힌 채 릴리프 밸브로 모두 빠져나가는 $25\,\mathrm{kW}$는 기름을 초당 $0.30\,\mathrm{K}$, 분당 $18\,\mathrm{K}$씩 데운다. 릴리프에 막혀 1분을 버틴 기계는 짐을 옮긴 것이 아니라 기름을 데운 것이다. 펌프 유량을 다 쓸 때 H1의 효율은 계산 절이 찾는데, 그때 열을 내는 것은 릴리프가 아니라 밸브다.

**펌프 축에서.** 같은 일률이 축에서는 토크 곱하기 회전 속도로 들어온다. 펌프는 한 바퀴에 부피 $V_d$를 압력 $p$에 맞서 밀어내므로 한 바퀴의 일은 $pV_d$이고, 한 바퀴는 $2\pi$ 라디안이다. 그래서

$$\tau=\frac{p\,V_d}{2\pi}$$

다. 라디안당 일이 곧 토크이기 때문이다. H1의 릴리프 설정에서 이것은 $25\times10^6\times25\times10^{-6}/(2\pi)=99.5\,\mathrm{N{\cdot}m}$이고, $2400\,\mathrm{rev/min}$, 곧 $251.3\,\mathrm{rad/s}$에서 엔진은 $99.5\times251.3=25.0\,\mathrm{kW}$를 댄다. 막힌 릴리프 밸브의 열이 엔진 쪽에서는 부하로 보이는 것이다.

### 5. 그림 하나로 보는 회로: 펌프, 릴리프 밸브, 방향 제어 밸브, 실린더, 탱크

*한 문장으로:* 펌프는 유량을 보내고, 하중과 손실이 압력을 정하며, 릴리프 밸브가 그 압력의 상한을 막고, 방향 제어 밸브가 흐름이 갈 곳을 정하고, 탱크가 돌아오는 것을 받는다 — 부품 다섯에 일 하나씩.

유압 회로도는 부품마다 맡은 일 하나를 알기 전까지는 엉킨 선으로만 보인다. 그러니 기름이 만나는 순서대로 본다. 그림의 위쪽을 탱크에서부터 읽는다. 펌프는 탱크에서 기름을 빨아 한 바퀴에 정해진 부피씩 압력 라인으로 밀어낸다. 릴리프 밸브는 그 라인에 닫힌 채 앉아 있다. 방향 제어 밸브는 압력 라인, 곧 P 포트를 실린더 포트 하나에 잇고 다른 실린더 포트를 탱크 라인, 곧 T 포트에 잇는다. 늘이는 명령을 끝까지 주면 P에서 A로, B에서 T로. 실린더는 압력을 힘으로(§2), 유량을 속도로(§3) 바꾸고, 로드측에서 밀려난 기름은 밸브를 거쳐 탱크로 돌아간다. 탱크는 대기에 열려 있으므로 게이지 압력 0이다.

> **용적형 펌프의 정의.** **용적형 펌프**(positive-displacement pump)는 *유량의 원천*이다. 축 한 바퀴마다 정해진 부피의 기름을 가두어 밀어내는 기계이고, 구동부와 케이싱이 버티는 한 하류에서 어떤 압력을 만나든 그렇게 한다. 정의 조건 셋. 토출량은 **배제 용적과 회전수로 정해진다**. **압력은 하류가 정한다**. 펌프가 아니라, 하중과 흐름이 지나야 하는 손실이 정한다. 그리고 펌프가 끌어가는 **일률**은 그 압력 곱하기 유량이 되는 만큼이고, 뒤의 엔진이나 모터가 그것을 대야 한다.
>
> $$Q=V_d\,N$$
>
> $V_d$는 한 바퀴당 배제 용적, $N$은 축 회전수다. 압력이 오를수록 $Q$를 줄이는 내부 누설은 여기서 무시하므로, 펌프는 순수한 유량 원천이다.
>
> - **예**: H1의 펌프, $25\,\mathrm{cm^3}\times2400\,\mathrm{rev/min}=60\,000\,\mathrm{cm^3/min}=60\,\mathrm{L/min}=1.0\times10^{-3}\,\mathrm{m^3/s}$. 라인이 $4.5\,\mathrm{MPa}$이든 $7.75\,\mathrm{MPa}$이든 같다.
> - **비예**: "펌프가 $25\,\mathrm{MPa}$를 만든다." 펌프가 만드는 것은 $60\,\mathrm{L/min}$이다. 팔이 막힘없이 올라갈 때 라인은 $7.75\,\mathrm{MPa}$이고, $25\,\mathrm{MPa}$에 이르는 것은 무언가가 흐름을 막을 때뿐이다 — 행정의 끝, 또는 실린더가 움직이지 못하는 하중.
> - **왜 중요한가**: 유량을 보낼 곳이 없는 정용량 펌프는 무언가가 버티지 못할 때까지 압력을 올린다. 다음 부품이 선택이 아닌 이유다.

> **릴리프 밸브의 정의.** **릴리프 밸브**(relief valve)는 *압력 제한기*다. 압력 라인과 탱크 사이의 상시 닫힌 밸브로, 입구 압력이 설정에 닿으면 열려 그 압력을 붙잡는 데 필요한 만큼의 유량을 탱크로 보낸다. 정의 조건 셋. **설정 아래에서는 닫혀 있다**. 그래서 평소 작업에서는 아무것도 흘리지 않는다. **설정에서 열린다**. 그리고 얼마를 흘리든 **설정 압력에서** 흘린다. 압력 라인과 탱크 사이의 차 전부를 건너가면서.
>
> $$p\le p_r,\qquad P_{\text{heat}}=p_r\,Q_r$$
>
> $p_r$은 설정, $Q_r$은 밸브를 건너는 유량이다. 그래서 그 열은 $\Delta p=p_r$로 둔 §4의 $\Delta p\,Q$다.
>
> - **예**: 행정 끝에 닿았는데 밸브 명령이 여전히 들어가 있는 H1. 로드는 더 갈 수 없고, $60\,\mathrm{L/min}$ 전부가 $25\,\mathrm{MPa}$로 릴리프 밸브를 건너며, $25\,\mathrm{kW}$가 열이 된다. §4의 분당 $18\,\mathrm{K}$다.
> - **비예**: 작동 압력을 정하는 것으로서의 릴리프 밸브. 계산 절에서 릴리프는 한 번도 열리지 않는다. 하중과 밸브 손실이 요구하는 것은 $7.75\,\mathrm{MPa}$뿐이다. 릴리프는 수준이 아니라 천장을 정한다.
> - **왜 중요한가**: 회로의 힘의 한계다 — $p_rA_{\text{cap}}=196\,\mathrm{kN}$이 H1이 낼 수 있는 미는 힘의 전부다. 그리고 열려 있을 때는 회로에서 가장 큰 열원이다.

방향 제어 밸브는 제어기가 명령하는 부품이다. H1의 것은 포트 넷, 위치 셋이다. 전개(P에서 A, B에서 T), 수축(P에서 B, A에서 T), 그리고 중립. 중립에서는 실린더 포트가 막혀 실린더가 갇힌 기름 위에 버티고(얼마나 뻣뻣하게인지는 §7이 말한다), P는 T와 이어져 펌프 유량이 릴리프를 넘지 않고 낮은 압력으로 탱크에 돌아간다. 비례 밸브는 [[glossary|용어집]]이 정의하듯 명령에 따라 모서리를 서서히 열고, 밸브가 속도를 정하는 방식이 이것이다. 밸브는 가변 오리피스이고 그 법칙은 §6의 것이다. 방향 제어 밸브가 하는 일은 모두 흐름을 보내고 조르는 일이다. 에너지를 더하지 않으며, 조를 때마다 그만큼이 열이 된다.

### 6. 압력 강하: 오리피스와 호스

파스칼의 원리는 정지한 기름의 법칙이다. 흐르는 기름은 좁은 곳을 비집고 지날 때마다 압력을 잃고, 밸브는 일부러 좁은 곳들로 만든다. 벽에 난 면적 $A_o$의 날카로운 구멍을 생각하자. 상류 압력은 $p_1$, 하류는 $p_2$다. 상류에서 기름은 넓은 통로를 천천히 다가오고, 구멍에서 가속되어 분류(jet)가 된다. 그렇게 짧은 거리에서는 마찰이 하는 일이 적으므로, 같은 높이의 베르누이 방정식이 느린 쪽에서 분류까지 기름을 이어 준다(OpenStax 14.6).

$$p_1+\tfrac12\rho v_1^2=p_2+\tfrac12\rho v_2^2$$

$v_1\ll v_2$이므로 분류 속도는 $v_2=\sqrt{2(p_1-p_2)/\rho}$다. 분류는 구멍보다 좁은 단면으로 수축하고 실제 흐름은 이상적인 흐름보다 조금 느리므로, 유량은 둘을 한데 흡수하는 유량 계수 $C_d<1$을 써서 $Q=C_dA_ov_2$다. 하류에서 분류는 느려지며 압력으로 되돌아가지 않는다. 난류로 부서지고, 그 운동 에너지는 열이 된다. 강하가 잃은 채로 남는 이유이고, 베르누이 방정식이 느린 쪽에서 분류까지는 성립해도 오리피스 전체를 가로질러서는 성립하지 않는 이유다.

> **오리피스 식의 정의.** **오리피스 식**(orifice equation)은 *짧은 좁힘에 대한 유량 법칙*이다. 그곳을 지나는 유량은 양단 압력 강하의 제곱근으로 는다. 정의 조건 넷. 좁힘이 **짧아서** 그 길이를 따른 마찰을 무시할 수 있고, 베르누이 방정식이 기름을 분류까지 데려간다. 상류 속도가 분류에 비해 **작다**. 하류의 분류가 **난류**여서 그 에너지가 회수되지 않는다. 그리고 측정한 **유량 계수** $C_d$가 분류의 수축과 손실을 떠맡는다.
>
> $$Q=C_d\,A_o\sqrt{\frac{2\,\Delta p}{\rho}}\qquad\Longleftrightarrow\qquad \Delta p=\frac{\rho}{2}\Big(\frac{Q}{C_d\,A_o}\Big)^2$$
>
> $A_o$는 열린 면적, $\rho$는 기름의 밀도, $\Delta p=p_1-p_2$는 강하다. 그러니 강하는 유량의 제곱으로 는다.
>
> - **예**: 명령을 끝까지 받은 H1의 밸브, $A_o=20\,\mathrm{mm^2}$, $C_d=0.65$. 분류는 $Q/(C_dA_o)=76.9\,\mathrm{m/s}$로 달리고, P→A 모서리는 $60\,\mathrm{L/min}$에서 $\Delta p=\tfrac12\times870\times76.9^2=2.57\,\mathrm{MPa}$를 떼어 간다. $38.4\,\mathrm{L/min}$을 흘리는 B→T 모서리는 그 $(38.4/60)^2=0.41$배, $1.05\,\mathrm{MPa}$다. 같은 면적의 둥근 구멍으로 치면 분류의 레이놀즈 수는 $N_R=2\rho vr/\eta=8443$으로, OpenStax 14.7이 난류라고 부르는 $3000$을 넘는다.
> - **비예**: 긴 호스. H1의 안지름 $20\,\mathrm{mm}$ 호스 $3\,\mathrm{m}$는 $60\,\mathrm{L/min}$을 $3.18\,\mathrm{m/s}$로 나르고 $N_R=1385$로 OpenStax의 $2000$ 아래다. 그래서 흐름은 층류이고 그 손실은 대신 푸아죄유 법칙을 따른다(OpenStax 14.7). 유량에 비례하고, 길이를 반지름의 네제곱으로 나눈 것에 비례한다.
> - **왜 중요한가**: 방향 제어 밸브는 가변 오리피스가 됨으로써 속도를 제어하고, 그 제어의 값을 압력으로 치른다 — 헤드측에서 $2.57\,\mathrm{MPa}$는 부하가 끝내 보지 못하는 $20.2\,\mathrm{kN}$의 힘이다 — 그리고 §4의 $\Delta p\,Q$만큼 열로도 치른다. 강하가 $Q^2$로 가므로, 같은 밸브로 유량을 두 배로 하면 압력은 네 배가 든다.

**좁힘이 치르게 하는 것.** 힘으로: 펌프 유량을 다 쓸 때 펌프는 $25\,\mathrm{MPa}$ 가운데 밸브를 지나고 남은 것만 쓸 수 있다. 그래서 릴리프가 열리기 전에 H1이 최고 속도로 들 수 있는 가장 큰 하중은 $(25-2.574)\times10^6\times7.854\times10^{-3}-1.054\times10^6\times5.027\times10^{-3}=170.8\,\mathrm{kN}$이고, 가만히 버틸 수 있는 $196\,\mathrm{kN}$이 아니다. 응답으로: 주어진 유량에서 압력을 먹는 좁힘은 주어진 압력에서 유량을 덜 흘리므로, 작은 밸브는 느린 기계를 만든다. 호스는 두 가지로 치르게 한다. 호스의 마찰은 길이에 따라, 그리고 층류에서는 반지름의 네제곱에 반비례해 커진다 — 안지름을 절반으로 하면 저항이 열여섯 배다(OpenStax 14.7). 그래서 한 치수 작은 호스는 열원이다. H1의 크기에서 중요한 것은 밸브의 강하다. 그리고 호스 안의 기름은 한 리터 한 리터가 피스톤이 움직이기 전에 압축되어야 하는 기름이고, 그것을 §7이 값 매긴다.

### 7. 압축성: 기름 기둥은 스프링이다

*한 문장으로:* 기름은 거의 압축되지 않지만 "거의"면 충분하다 — 기름 기둥은 피스톤 면적의 제곱으로 뻣뻣해지고 뒤에 있는 기름의 부피로 물러지는 스프링이며, 팔의 질량과 함께 몇 헤르츠로 우는 질량–스프링을 이룬다.

지금까지 기름을 비압축성으로 다뤘다. 세게 짜면 기름은 조금 물러나고, 조금의 기름이 조금 물러나는 것이 밸브의 명령과 하중 사이에 앉아 있는 것이다.

> **체적 탄성 계수의 정의.** 유체의 **체적 탄성 계수**(bulk modulus) $\beta$는 *균일한 압력 아래의 재료 강성*이다. 부피를 비율로 잃을 때, 그 비율 하나당 오르는 압력이다. 정의 조건 셋. 압축이 **균일하다**. 모든 면에 같은 압력이 걸리므로 모양이 아니라 부피만 바뀐다. 계수는 **국소 기울기**다. 압력과 온도에 따라 바뀌므로 한 압력, 한 온도에서 잡는다. 그리고 기체에서는 짜는 **빠르기**에 달렸다. 느린 짜기는 주변 온도에 머물고, 빠른 짜기는 기체를 데우기 때문이다.
>
> $$\beta=-V\,\frac{dp}{dV}$$
>
> $V$는 부피, $dp/dV$는 부피에 대한 압력의 기울기다. 압력이 오르면 부피가 줄기 때문에 음의 부호가 $\beta$를 양수로 만든다(OpenStax 12.3은 같은 비를 유한한 변화로 쓴다).
>
> - **예**: H1의 기름, $\beta_e=1.0\,\mathrm{GPa}$. 릴리프의 $25\,\mathrm{MPa}$에서 부피의 $25\times10^6/10^9=2.5\%$를, 붙잡는 압력 $4.50\,\mathrm{MPa}$에서 $0.45\%$를 잃는다. 견주어 보면 OpenStax의 표는 물을 $2.2\,\mathrm{GPa}$, 강철을 $160\,\mathrm{GPa}$로 적는다.
> - **비예**: 액체처럼 "체적 탄성 계수를 가진" 공기. 이상 기체는 온도가 일정하면 $pV$가 일정하므로(이상 기체 법칙, OpenStax University Physics 2권 §2.1) $dp/dV=-p/V$이고 $\beta=p$다. 계수가 곧 절대 압력이다 — 게이지 $0.6\,\mathrm{MPa}$의 공기에서 $0.7\,\mathrm{MPa}$. 열을 내보낼 틈 없이 빠른 짜기에서는 $pV^\gamma$가 일정하고 $\beta=\gamma p=1.4p$다(2권 §3.6). 재료의 상수가 전혀 아니고, H1의 기름보다 약 $1400$배 무르다.
> - **왜 중요한가**: 밸브와 피스톤 사이의 기름은 한 리터 한 리터가 스프링이고 $\beta$가 그 강성을 정한다. 그래서 유압 관절이 얼마나 뻣뻣한지, 압력이 얼마나 빨리 오를 수 있는지, 얼마나 빨리 제어될 수 있는지가 모두 이 숫자 하나로 돌아온다.

**스프링.** 실린더의 두 포트를 막고 로드를 작은 $x$만큼 밀어 넣는다. 부피 $V$인 헤드측 기름은 부피 $Ax$를 잃으므로, 정의에 따라 압력이 $\Delta p=\beta Ax/V$ 오르고, 그 압력이 피스톤을 $A\,\Delta p$로 되민다.

$$\Delta F=\frac{\beta A^2}{V}\,x$$

그러니 갇힌 기름은 면적의 제곱으로 뻣뻣해지고 뒤에 있는 기름의 부피로 물러지는 스프링이다. 토목 공학자는 이 스프링을 이미 만났다. 기름의 부피를 기둥으로, $V=AL$로 쓰면 강성은 $\beta A/L$, 곧 영률 자리에 체적 탄성 계수가 들어간 봉의 축 강성 $EA/L$이다. H1의 헤드측은 실과 호스를 합쳐 길이 $V_{\text{cap}}/A_{\text{cap}}=0.52\,\mathrm m$의 기둥과 같고, 같은 단면과 길이의 강철 봉은 $E/\beta=200$배 뻣뻣하다.

> **유압 스프링 강성의 정의.** 실린더의 **유압 스프링 강성**(hydraulic spring rate)은 N/m 단위의 *강성*이다. 실의 기름이 갇혀 있을 때 로드를 단위 길이만큼 움직이는 데 드는 힘이다. 정의 조건 셋. 기름이 **갇혀** 있다 — 밸브는 닫혀 있고 누설이 없다 — 그래서 변위는 기름을 압축할 수밖에 없다. 변위가 **작아서** 압력 변화가 부피 변화에 비례하고, 그 비례를 $\beta$가 정한다. 그리고 실마다 **제 면적과 제 부피**로 작용하며, 부피에는 밸브까지의 호스가 들어간다. 둘 다 갇혀 있으면 두 강성이 더해진다. 한 번 밀면 한 실은 짜이고 다른 실은 풀리는데, 두 변화가 모두 되밀기 때문이다.
>
> $$k_h=\beta\Big(\frac{A_{\text{cap}}^2}{V_{\text{cap}}}+\frac{A_{\text{ann}}^2}{V_{\text{rod}}}\Big)$$
>
> $V_{\text{cap}}$과 $V_{\text{rod}}$는 피스톤 양쪽의 기름 부피, 곧 실 더하기 호스다.
>
> - **예**: 행정 중간의 H1. 호스 한 가닥에 $\pi(0.02\,\mathrm m)^2/4\times3\,\mathrm m=0.94\,\mathrm{L}$가 들므로 $V_{\text{cap}}=3.14+0.94=4.08\,\mathrm{L}$, $V_{\text{rod}}=2.01+0.94=2.95\,\mathrm{L}$이고, $k_h=10^9\,(6.169\times10^{-5}/4.084\times10^{-3}+2.527\times10^{-5}/2.953\times10^{-3})=15.1+8.6=23.7\,\mathrm{MN/m}$다. 하중이 $1\,\mathrm{kN}$ 바뀌면 로드는 $0.042\,\mathrm{mm}$ 움직인다.
> - **비예**: 같은 실린더에 절대 $0.7\,\mathrm{MPa}$의 공기를 채운 것. $\beta=p$로 강성은 $16.6\,\mathrm{kN/m}$이고, 같은 $1\,\mathrm{kN}$에 $60\,\mathrm{mm}$ 움직인다. 둘째 비예는 한쪽이 탱크로 열린 채의 $k_h$다. 그 실의 스프링은 사라지고, 늘어나는 H1에는 헤드측의 $15.1\,\mathrm{MN/m}$만 남는다.
> - **왜 중요한가**: 기름 스프링과 로드가 움직이는 질량은 [[02-foundations/engineering-math|0.5 §8]]의 고유 진동수 $\omega_n=\sqrt{k/m}$를 가진 질량–스프링을 이룬다. 기름을 거쳐 작용하는 어떤 제어기도 팔을 그보다 훨씬 빠르게 반응시키지 못한다.

**스프링 위의 질량.** 로드가 느끼는 것은 $600\,\mathrm{kg}$이 아니다. 팔의 질량은 로드의 $n=6$배 속도로 날 끝에서 움직이므로, 그 운동 에너지 $\tfrac12m_a(nv)^2=\tfrac12(n^2m_a)v^2$은 로드와 함께 움직이는 질량 $m_r=n^2m_a=21\,600\,\mathrm{kg}$의 운동 에너지다. [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §4]]가 기어박스 뒤의 모터에서 찾는 바로 그 $n^2$이다. H1의 기름 스프링 위에서 그 질량은

$$\omega_n=\sqrt{\frac{k_h}{m_r}}=\sqrt{\frac{2.366\times10^7}{21\,600}}=33.1\,\mathrm{rad/s}$$

로, 곧 $5.27\,\mathrm{Hz}$로 운다. 뻣뻣한 스프링 위의 무거운 팔은 여전히 느린 진동자이고, 몇 헤르츠보다 훨씬 빠르게 움직이려는 제어기는 그것을 들뜨게 한다. 배관 길이가 문제가 되는 곳이 여기다. 호스가 없으면 실만으로 $32.2\,\mathrm{MN/m}$, $6.15\,\mathrm{Hz}$이고, $10\,\mathrm{m}$ 호스로는 $14.7\,\mathrm{MN/m}$, $4.15\,\mathrm{Hz}$다. [[04-robotics/control-theory-ce397|5. 제어 이론 §2]]가 이런 질량–스프링을 상태공간으로 쓰고, 그 §5가 $\omega_n$과 감쇠를 논문이 인용하는 상승 시간과 오버슈트로 바꾼다.

**$\beta_e$를 액체의 값보다 낮게 잡는 이유.** 유효 계수에는 압력이 짜는 모든 것이 들어간다. 호스 벽은 늘어나 압력 아래에서 부피를 보탠다. 그리고 녹지 않은 공기는 제 몫보다 훨씬 크게 친다. 한 압력 아래의 부피 변화들은 더해지기 때문이다. 전체 부피 $V$는 $\Delta V=V_\ell\,\Delta p/\beta_\ell+V_g\,\Delta p/\beta_g$를 잃으므로 $1/\beta_e=(V_\ell/V)/\beta_\ell+(V_g/V)/\beta_g$이고, 기체는 $\beta_g=p$다. 물만큼 뻣뻣한 $2.2\,\mathrm{GPa}$의 액체를 $5\,\mathrm{MPa}$에서 보면, 기체가 $0.1\%$만 섞여도 $1.53\,\mathrm{GPa}$로, $1\%$면 $0.41\,\mathrm{GPa}$로 떨어진다. H1이 기름과 호스를 합쳐 둥근 $1.0\,\mathrm{GPa}$를 고정하는 이유이고, 유압 시스템에서 공기를 빼는 일이 정비의 문제이기 전에 강성의 문제인 이유다.

### 8. 공기는 무르다: 공압과 그 쓰임새

로봇은 공기로 쥐고 기름으로 판다. 그 이유는 숫자 하나, 체적 탄성 계수다. §7의 비예가 공압의 전부를 한 줄로 말한다. 기체의 체적 탄성 계수는 그 절대 압력이다. 그래서 게이지 $0.6\,\mathrm{MPa}$로 공급하는 공기 — 이 절의 교과 값 — 는 H1의 기름보다 약 $1400$배 무르고, 공급 압력 자체도 H1의 릴리프 설정보다 40배쯤 낮다. H1의 $100\,\mathrm{mm}$ 보어에서 공기는 $0.6\times10^6\times7.854\times10^{-3}=4.7\,\mathrm{kN}$으로 미는데, $25\,\mathrm{MPa}$의 기름은 $196\,\mathrm{kN}$이다. 공압 실린더는 크기에 비해 약하고, 무른 스프링을 품고 있다.

**그리퍼 손가락, 숫자로.** 조절된 게이지 $0.6\,\mathrm{MPa}$ 공급으로 보어 $20\,\mathrm{mm}$ 실린더가 손가락을 민다고 하자(교과 예). 손가락은 $0.6\times10^6\times\pi(0.02\,\mathrm m)^2/4=188\,\mathrm N$으로 닫히고, 부품이 예상보다 $2\,\mathrm{mm}$ 넓으면 $2\,\mathrm{mm}$ 먼저 같은 $188\,\mathrm N$으로 멈춘다. 조절기가 압력을 붙잡고 있고, 힘은 피스톤이 어디 있든 압력 곱하기 면적이기 때문이다. 위치로 몰아가는 손가락이라면 무언가가 물러설 때까지 계속 눌렀을 것이다.

그 스프링이 공기가 쓰이는 곳을 정한다. **하중 아래의 위치**: 공기 실린더는 하중이 바뀌는 동안 행정 중간의 한 점을 지키지 못한다. 공기가 물러서기 때문이다 — §7의 예에서 킬로뉴턴당 $60\,\mathrm{mm}$. 그래서 공압 구동기는 대개 끝에서 끝까지, 단단한 멈춤쇠에 대고 움직이며, 추종하기보다 열고 닫는 것이 일이다. **센서 없는 힘**: 공기로 미는 그리퍼 손가락은 어디서 멈추든 압력 곱하기 면적으로 민다. 그래서 크기가 불확실한 부품을 정해진 힘으로 쥐고, 보지 못한 충돌의 대가도 적다. 무름이 곧 기능이다. **소프트 액추에이터**는 이것을 더 밀고 나간다. 속에 방이 있는 탄성체가 부풀면 구부러지거나 물체를 감싸고, 그 모양을 링크가 아니라 컴플라이언스가 정한다. **압축 공기로 만드는 진공**: 많은 흡착 그리퍼는 이젝터로 진공을 만든다. 노즐을 지나는 압축 공기 분류가 컵에서 공기를 끌어낸다 — Schmalz는 이젝터가 벤투리 원리로 일한다고 적는다. 그러니 공압 공급은 V1 같은 진공 그리퍼를 먹여 살리는 것이기도 하다.

§1에서 넘어오는 주의 하나. 기체 법칙에는 절대 압력이 필요하므로, 게이지 읽음은 대기압을 더한 뒤에 $pV=nRT$에 넣어야 한다. 게이지 $0.6\,\mathrm{MPa}$는 법칙 안에서 $0.70\,\mathrm{MPa}$이고, 게이지 값으로 계산한 강성은 $14\%$ 무르게 나온다. 이 페이지는 공압 회로의 치수를 정하지 않는다(§12).

### 9. 진공: 대기로 패널을 붙잡기

*한 문장으로:* 흡착 컵은 당기지 않는다 — 대기가 압력 차 곱하기 밀봉 면적으로 패널을 컵에 밀어붙이고, 그 힘의 천장은 대기 자신이다 — 그리고 연직 패널은 그 힘에 마찰을 통해서만 매달린다.

컵을 패널 면에 밀봉하고 안의 압력을 $\Delta p$만큼 낮춘다. 바깥에서는 대기가 여전히 $p_{\text{atm}}$으로 패널을 누르고, 밀봉선 안쪽에서는 남은 공기가 $p_{\text{atm}}-\Delta p$로만 되민다. 알짜로 밀봉선 안 면적에 걸린 $\Delta p$가 패널과 컵을 서로 밀어붙인다. 컵 안의 무엇도 당기지 않는다. 유체는 밀 수는 있어도 당기지 못한다(§1).

> **진공 유지력의 정의.** 흡착 컵의 **유지력**(holding force)은 *압력의 힘*이다. 대기압과 컵 안 압력의 차에 밀봉선 안쪽 면적을 곱한 것이다(Schmalz는 유효 흡착 면적으로 $F=\Delta p\times A$라 쓴다). 정의 조건 넷. 컵이 **밀봉되어** 있어 차가 새어 나가지 않고 유지된다. 면적은 **유효** 면적, 곧 하중을 받아 컵이 변형된 채의 밀봉선 안쪽이지 컵의 바깥지름이 아니다. 힘은 면에 **수직**으로 작용해 패널과 컵을 서로 누른다. 면을 따라서는 컵이 마찰로만, 곧 수직력 곱하기 마찰 계수로만 버틴다. 그리고 천장은 **대기**다. 차는 결코 $p_{\text{atm}}$을 넘을 수 없다.
>
> $$F_n=n_c\,\Delta p\,A_c,\qquad F_t\le\mu\,F_n,\qquad \Delta p\le p_{\text{atm}}$$
>
> $n_c$는 컵의 수, $A_c$는 컵마다의 유효 면적, $F_n$은 전체 수직력, $F_t$는 컵이 면을 따라 질 수 있는 가장 큰 힘이다.
>
> - **예**: $60\,\mathrm{kPa}$의 V1. Schmalz가 유지력을 적을 때 쓰는 상대 진공도 $60\%$와 거의 같은 수준이다. 컵 하나가 $60\times10^3\times7.854\times10^{-3}=471\,\mathrm{N}$, 넷이 $1885\,\mathrm{N}$으로 누르고, 면이 연직이면 그 면을 따라 많아야 $0.5\times1885=942\,\mathrm{N}$을 진다. 같은 $100\,\mathrm{mm}$ 원이 H1의 헤드측으로서는 $25\,\mathrm{MPa}$에서 $196\,\mathrm{kN}$을 진다. 법칙은 같고 압력이 $417$배 다를 뿐이다.
> - **비예**: "더 센 펌프면 더 붙잡는다." 완전한 진공에서 컵 넷은 $4\times101\,325\times7.854\times10^{-3}=3183\,\mathrm{N}$으로 누르고 연직면을 따라 $1592\,\mathrm{N}$을 진다 — 여유 없이 $162\,\mathrm{kg}$ — 그리고 어떤 펌프도 여기에 1뉴턴도 보태지 못한다. 컵을 늘리거나 키울 수 있을 뿐이다. 해발 $1000\,\mathrm{m}$ 현장에서는 OpenStax의 지수형 대기 $p=p_0e^{-y/8800\,\mathrm m}$가 그 천장마저 $89\%$로 낮춘다(OpenStax 14.1).
> - **왜 중요한가**: 붙잡는 것은 대기이므로 리프터의 용량은 면적, 진공도, 마찰이 정하고, 연직 파지 — 벽 앞의 S1 — 는 눕혀 드는 경우의 $\mu=0.5$배 용량밖에 없다.

그 식에서 약한 숫자는 마찰 계수다. Schmalz는 참고 값을 준다 — 젖은 면 $0.2$–$0.3$, 나무·금속·유리·돌 $0.5$, 거친 면 $0.6$ — 그리고 $\mu$는 시험으로 찾아야 한다고 못 박는다. [[04-robotics/grasping|15. 파지 §2]]가 이것이 기대는 마찰 원뿔을 그리고, 그 §6이 같은 경고의 현장 판을 낸다. 건설 현장에서는 아무도 $\mu$를 재지 않고, 그 값은 한 교대 안에서도 바뀐다.

> **진공 파지 안전율의 정의.** 진공 파지의 **안전율**(safety factor) $S$는 *용량 대 요구의 비*다. 하중이 작용하는 방향으로 컵이 질 수 있는 힘을, 하중이 컵에 거는 힘으로 나눈 것이다. 정의 조건 셋. 용량과 요구를 **같은 방향으로** 잡는다 — 곧게 들어 올리는 평평한 부재는 수직으로 당기는 힘, 연직 부재는 마찰. 용량은 펌프의 최고 진공이 아니라 리프터가 내려가도 좋다고 허락된 **가장 낮은 진공**에서 계산한다. 그리고 요구에는 무게와 함께 하중의 **가속**이 들어간다. 컵은 하중을 출발시키고 세우기도 해야 하기 때문이다. Schmalz는 요구를 $m(g+a)$로 쓴다. 요구 값은 들기 전에 정한다. Schmalz는 매끄럽고 치밀한 부재에 최소 $1.5$, 까다롭거나 다공질이거나 거칠거나 기름 묻은 부재에 $2.0$ 이상을 쓰고, 한 리프터 제조사가 요약한 EN 13155는 리프터를 안전율 2로 설계한다고 한다(Aerolift).
>
> $$S_{\text{vert}}=\frac{\mu\,n_c\,\Delta p\,A_c}{m\,(g+a)},\qquad S_{\text{flat}}=\frac{n_c\,\Delta p\,A_c}{m\,(g+a)}$$
>
> 연직 면을 따라서는 컵이 마찰로 버티고, 곧게 들어 올리는 평평한 부재 아래서는 수직력만으로 버티기 때문이다.
>
> - **예**: 멈춰 있는 S1의 연직 패널 위 V1, $a=0$: $S=942/196.2=4.80$. 눕히면 $1885/196.2=9.61$. 연직 파지가 요구 $S=2$로 떨어지는 진공은 $\Delta p_{\min}=2\times196.2/(0.5\times4\times7.854\times10^{-3})=25.0\,\mathrm{kPa}$, $S=1$로는 $12.5\,\mathrm{kPa}$다.
> - **비예**: 깨끗한 시험판 위에서 펌프의 최고 진공으로 계산한 안전율. 다공질 패널에서, 또는 펌프가 선 뒤에 리프터가 붙드는 진공에 대해서는 아무것도 말하지 않는데, 안전율이 쓰이는 곳은 바로 그곳이다.
> - **왜 중요한가**: 감시 장치가 걸려야 하는 숫자는 작동 진공이 아니라 최소 진공이다 — S1이 집기 단계의 감시 변수로 흡착 압력을 꼽는 이유다([[05-construction-robotics/site-engineering|2.5 §3]]).

### 10. 누설, 진공 탱크, 그리고 S1의 안전 상태 안의 리프터

리프터의 여유는 §9의 식에 보이지 않는 두 길로 쓰인다. 공기를 들이는 면, 그리고 서 버리는 펌프다. 둘 다 시간의 문제이고, 이상 기체 법칙이 답한다.

**누설이 하는 일.** 다공질 패널 위의 컵, 또는 테두리가 홈을 가로지르는 컵은 바깥 공기를 끊임없이 들인다. 펌프가 돌면 들어오는 만큼 빨리 그 공기를 빼내야 하고, 진공도는 둘이 균형을 이루는 곳에 자리 잡는다 — 새는 면일수록 낮다. 다공질이고 공기가 통하는 부재에 대해 Schmalz는 원래 부재로 흡착 시험을 해 보라고 권한다. 펌프가 서면 체크 밸브가 탱크의 진공이 펌프를 거쳐 새지 않게 막고, 진공은 누설의 속도로 줄어든다. 누설을 바깥 공기의 일정한 유입, 곧 대기압에서 잰 $Q_L$로 모델링한다. 교과 모델이다. 실제 누설량은 진공도에 따라 바뀌므로 재야 한다. 온도가 일정한 이상 기체 법칙 $pV_s=Nk_BT$(2권 §2.1)에서, 유입은 대기압 $p_{\text{atm}}$에서 초당 $Q_L$을 차지하던 만큼의 공기를 $V_s$에 보태므로 안쪽의 절대 압력은

$$\frac{dp_{\text{abs}}}{dt}=\frac{p_{\text{atm}}\,Q_L}{V_s}$$

의 속도로 오르고, 진공도는 같은 속도로 준다. V1에서는 $101\,325\times(1.0\times10^{-3}/60)/2.0\times10^{-3}=844\,\mathrm{Pa/s}$이다. $60\,\mathrm{kPa}$에서 $S=2$의 경계 $25.0\,\mathrm{kPa}$까지 $41.5\,\mathrm{s}$, $S=1$까지 $56.3\,\mathrm{s}$가 걸린다. 분당 $20\,\mathrm{L}$가 새는 다공질 패널은 $2.1\,\mathrm{s}$면 거기 닿는다.

**S1의 안전 상태 안의 리프터.** S1의 지지·체결 단계에서 안전 상태는 *정지 유지*다. 브레이크를 걸고 동력 운동이 없으며, 패널을 서보 루프가 아니라 브레이크가 받쳐서 서보 동력이 끊겨도 유지된다([[05-construction-robotics/site-engineering|2.5 §3]]). V1이 그리퍼라면 브레이크는 팔을 받치고, 팔 위의 패널은 컵이 받친다. 그러니 정지 유지는 컵이 펌프 없이 버티는 동안만 안전하다. 이 숫자로는 $S\ge2$에서 $41\,\mathrm{s}$다. 패널을 내려놓기에는 넉넉하지만 — 집기 단계의 안전 상태가 *내려놓고 다시 집기*다 — Aerolift의 요약에 따르면 EN 13155가 크레인의 진공 리프터에 요구하는 정전 뒤 5분 유지에는 한참 못 미친다. 같은 요약에 따르면 EN 13155는 역지 밸브와, 눈과 귀로 알리는 저진공 경보도 함께 요구한다. 로봇의 그리퍼는 크레인 부착물이 아니지만 2.5의 셋째 조건은 같은 것을 묻는다 — 그 상태가 고장 난 기능 없이 유지되는가? — 그리고 V1의 답은 몇 초라는 숫자다. 감시도 같은 숫자에서 나온다. $S=2$의 경계 $25.0\,\mathrm{kPa}$에 둔 진공 스위치는 성한 패널에서는 펌프가 선 지 $41\,\mathrm s$ 만에, 다공질 패널에서는 약 $2\,\mathrm s$ 만에 걸리고, 걸린 순간부터 시스템에게는 $S=1$까지의 $15\,\mathrm s$만이 그 단계를 떠날 시간으로 남는다.

### 대상으로 한 번 끝까지 · Worked case

명령을 끝까지 주어 붐을 올리고, 이어 S1의 패널을 V1으로 붙잡는다. 여덟 단계, 숫자는 모두 이 페이지의 대상에서, 법칙은 모두 §1–§10에서 온다. 고정한 대상 위의 교과 계산이지 기계를 잰 값이 아니다.

**1단계 — 면적.** $A_{\text{cap}}=\pi(0.1\,\mathrm m)^2/4=7.854\times10^{-3}\,\mathrm{m^2}$, $A_{\text{ann}}=\pi(0.1^2-0.06^2)\,\mathrm{m^2}/4=5.027\times10^{-3}\,\mathrm{m^2}$, $\varphi=1.5625$(§2).

**2단계 — 하중이 요구하는 압력.** §2의 지렛대로 $F_L=n\,m_ag=6\times600\times9.81=35\,316\,\mathrm N$이므로, 로드측이 탱크 압력인 채 헤드측은 $p_{\text{hold}}=35\,316/7.854\times10^{-3}=4.497\,\mathrm{MPa}$를 버텨야 한다.

**3단계 — 속도와 시간.** $v=Q/A_{\text{cap}}=1.0\times10^{-3}/7.854\times10^{-3}=0.1273\,\mathrm{m/s}$, 날 끝은 $0.764\,\mathrm{m/s}$로 오르고, 행정은 $0.80/0.1273=6.28\,\mathrm s$가 걸리며, 로드측은 $vA_{\text{ann}}=6.40\times10^{-4}\,\mathrm{m^3/s}=38.4\,\mathrm{L/min}$을 돌려보낸다(§3).

**4단계 — 밸브의 두 모서리.** 오리피스 식(§6)으로, P→A는 $60\,\mathrm{L/min}$을 $\Delta p_{PA}=\tfrac12\times870\times\big(1.0\times10^{-3}/(0.65\times20\times10^{-6})\big)^2=2.574\,\mathrm{MPa}$에서 흘리고, B→T는 $38.4\,\mathrm{L/min}$을 $\Delta p_{BT}=0.4096\times2.574=1.054\,\mathrm{MPa}$에서 흘린다.

**5단계 — 압력들.** 탱크는 게이지 0이므로 로드측은 $p_B=\Delta p_{BT}=1.054\,\mathrm{MPa}$에 있고, 일정한 속도에서 피스톤의 힘은 균형을 이룬다.

$$p_A\,A_{\text{cap}}=F_L+p_B\,A_{\text{ann}}\quad\Rightarrow\quad p_A=p_{\text{hold}}+\frac{p_B}{\varphi}=4.497+0.675=5.171\,\mathrm{MPa}$$

배압은 헤드측의 $1/\varphi$인 환형 면적을 누르기 때문이다. 펌프는 $p_P=p_A+\Delta p_{PA}=5.171+2.574=7.745\,\mathrm{MPa}$로 일하고, 이것은 설정 $25\,\mathrm{MPa}$ 아래이므로 릴리프는 닫힌 채 펌프 유량 전부가 실린더에 닿는다(§5).

**6단계 — 일률, 효율, 열.** 펌프가 $p_PQ=7.745\,\mathrm{kW}$를 넣고, 팔은 $F_Lv=4.497\,\mathrm{kW}$를 받으며, $\eta=4.497/7.745=58.1\%$다. 나머지 $3.249\,\mathrm{kW}$는 밸브의 몫이다. P→A에서 $2.574\,\mathrm{MPa}\times1.0\times10^{-3}\,\mathrm{m^3/s}=2.574\,\mathrm{kW}$, B→T에서 $1.054\,\mathrm{MPa}\times6.40\times10^{-4}\,\mathrm{m^3/s}=0.675\,\mathrm{kW}$(§4). 냉각이 없으면 이것이 기름 $43.5\,\mathrm{kg}$을 $3249/(43.5\times1900)=0.039\,\mathrm{K/s}$, 분당 $2.4\,\mathrm K$씩 데운다. 행정 끝에서 릴리프가 $25\,\mathrm{kW}$ 전부를 받으면 분당 $18\,\mathrm K$다.

**7단계 — V1의 파지.** $F_n=4\times60\times10^3\times7.854\times10^{-3}=1885\,\mathrm N$. 연직면을 따라서는 $\mu F_n=942\,\mathrm N$이 패널의 $196.2\,\mathrm N$을 맞으므로 $S=4.80$이다(§9). 연직 파지는 $\Delta p_{\min}=25.0\,\mathrm{kPa}$에서 요구 $S=2$로 떨어지고, 대기가 그 천장을 $1592\,\mathrm N$, $S=8.1$로 막는다.

**8단계 — 펌프가 선 뒤의 V1.** $dp_{\text{abs}}/dt=101\,325\times1.667\times10^{-5}/2.0\times10^{-3}=844\,\mathrm{Pa/s}$이므로, 진공은 $60$에서 $25.0\,\mathrm{kPa}$까지 $(60\,000-24\,981)/844=41.5\,\mathrm s$에, $S=1$이 되는 $12.5\,\mathrm{kPa}$까지 $56.3\,\mathrm s$에 떨어진다. $S\ge2$로 5분을 버티려면 $V_s=300\times101\,325\times1.667\times10^{-5}/35\,019=14.5\,\mathrm L$, 또는 $2\,\mathrm L$ 탱크로 분당 $0.14\,\mathrm L$의 누설이 필요하다(§10).

**이 계산이 말하는 것.** 펌프는 릴리프 설정의 3분의 1도 안 되는 압력에서 돌지만, 그래도 일률의 $42\%$가 밸브에서 열이 된다. 조르는 회로는 제어를 압력으로 사고, 그 값은 유량의 제곱으로 오른다. 리프터의 정적 여유는 넉넉하지만 — 요구 $2$에 대해 $4.8$ — 시간의 여유는 얇다. 펌프 없이 1분이 안 된다. "미는 힘 $196\,\mathrm{kN}$", "유지력 $1885\,\mathrm N$"만 적은 사양서에서는 두 숫자 어느 것도 보이지 않는다.

### 11. 밸브 응답, 그리고 건설 페이지가 값을 매기는 지연

S2는 밸브에서 움직임까지의 지연 $\tau_h=0.15\,\mathrm s$를 고정하고([[05-construction-robotics/site-engineering|2.5 현장 로보틱스]]), [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 §1]]은 그것을 지연 오버슈트 $e_{\text{lat}}=v\tau_h$로 바꾼다. $0.3\,\mathrm{m/s}$로 목표 바닥면에 다가가던 날 끝은 그 면을 $45\,\mathrm{mm}$ 지나쳐 멈춘다. 그 절은 명령과 움직임 사이에 무엇이 있는지 꼽는다. 밸브가 데드존을 지나는 이동, 압력 형성, 기름과 호스의 탄성이다. 뒤의 둘이 이 페이지의 물리이고, H1 위에서 값을 매길 수 있다.

**압력 형성.** 하중이 움직이기 전에 압력이 $\Delta p$ 올라야 하는 실은 여분의 부피 $V\Delta p/\beta$를 받아야 하고 — §7의 정의를 거꾸로 읽은 것 — 밸브는 부피를 $Q$의 속도로 보내므로

$$t_p=\frac{V\,\Delta p}{\beta\,Q}$$

다. 그 부피가 다 들어오기 전에는 아무것도 움직이지 않기 때문이다. 행정 중간의 H1이 헤드측이 탱크 압력인 채 땅에 내려놓은 팔을 들기 시작한다면, $4.084\times10^{-3}\times4.497\times10^6/(10^9\times1.0\times10^{-3})=18.4\,\mathrm{ms}$가 지나야 로드가 조금이라도 움직인다.

**기름 스프링을 거친 가속.** 로드가 움직이기 시작하면 헤드측으로 드는 유량은 기름을 압축하는 데와 피스톤을 움직이는 데로 나뉘고, $(V/\beta)\,\dot p=Q-Av$, 동시에 $p_{\text{hold}}$를 넘는 압력이 반사 질량을 가속한다, $m_r\dot v=A(p-p_{\text{hold}})$. 둘째 식을 미분하고 첫째 식을 넣으면

$$\ddot v+\omega_c^2\,v=\omega_c^2\,\frac{Q}{A_{\text{cap}}},\qquad \omega_c^2=\frac{\beta A_{\text{cap}}^2}{V_{\text{cap}}\,m_r}$$

이다. 그래서 로드측이 탱크로 열려 있고 로드가 $p_{\text{hold}}$에서 정지해 출발하면, 속도는 [[02-foundations/engineering-math|0.5 §8]]의 특수해 더하기 동차해, $v(t)=(Q/A_{\text{cap}})(1-\cos\omega_ct)$를 따른다. 헤드측 스프링만으로 $\omega_c=26.4\,\mathrm{rad/s}$($4.21\,\mathrm{Hz}$)이고, 로드는 4분의 1 주기인 $\pi/(2\omega_c)=59.4\,\mathrm{ms}$ 뒤에야 명령한 $0.127\,\mathrm{m/s}$에 처음 닿고, 그다음 지나친다. 이 모델에는 감쇠가 없고, 실제 회로에서는 마찰과 누설이 그것을 댄다.

**이것이 $\tau_h$에 대해 말하는 것.** 순식간에 열리는 밸브 뒤에서도 H1의 기름은 땅에서 출발할 때 $18\,\mathrm{ms}$의 압력 형성과 속도까지 $59\,\mathrm{ms}$의 상승을 치르게 한다. 둘 다 S2의 $\tau_h$ 같은 순수 지연은 아니지만, 어떤 빠른 밸브로도 없앨 수 없는 지체의 일부다. $\beta$, 면적, 기름 부피, 질량이 정하기 때문이다. 이 교과 숫자로는 S2의 $0.15\,\mathrm s$ 가운데 나머지는 밸브 자신 — 그 파일럿 단과, 스풀이 데드존을 지나는 이동 — 에서 와야 하는데, 이것들은 [[glossary|용어집]]이 정의하고 이 페이지는 모델링하지 않는다. 지렛대는 거리도 나눈다. 그 마무리 굴착을 H1의 자세에서 붐 혼자 몬다면, 3의 날 끝 $45\,\mathrm{mm}$는 H1의 로드에서 $45/6=7.5\,\mathrm{mm}$이고, 그때 로드는 $0.3/6=0.05\,\mathrm{m/s}$로 움직이며 헤드측은 밸브로 $0.05\times7.854\times10^{-3}\,\mathrm{m^3/s}=23.6\,\mathrm{L/min}$을 흘린다. 이 지체를 빠뜨린 시뮬레이터는 [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §1]]이 동역학 격차의 첫 줄에 올린 유압 지연 격차를 갖는다.

### 12. 이 페이지가 다루지 않는 것

- **밸브와 펌프의 속**: 스풀 형상과 겹침, 파일럿 단, 압력 보상기, 가변 용량 펌프와 부하 감응 펌프. 건설 페이지는 밸브를 뭉친 지연 하나로 다루고([[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 §1]]), §11도 그렇다.
- **유압 팔의 제어**: 서보 밸브 동역학, 압력·힘 제어, 학습한 액추에이터 모델. 피드백 아래의 질량–스프링은 [[04-robotics/control-theory-ce397|5. 제어 이론]]이고, 그 페이지의 §9가 선형 보장을 깨는 효과로 밸브 데드존을 꼽는다. 학습한 모델은 3의 것이다.
- **작동유**: 온도에 따른 점성 변화, 오염과 여과, 캐비테이션, 그리고 §7의 기체 분율을 넘는 공기 문제.
- **공압 회로**: 압축성 기체가 오리피스·밸브·이젝터를 지나는 흐름, 가압된 부피에 저장된 에너지. §8은 강성만 다룬다.
- **어큐뮬레이터, 유압 모터, 정유압 구동**, 그리고 기계 전체의 주행과 선회 구동.
- **표준**: 유체 동력 시스템과 인양 부착물에 대해 안전 표준이 요구하는 것. §10은 EN 13155에 대한 한 제조사의 요약을 인용할 뿐 표준 자체를 읽지 않았다. 로봇 안전은 [[04-robotics/hri-safety|11. HRI·안전]]이다.
- **둘레의 역학과 전기**: 기름 기둥이 만드는 스프링 위의 질량과 붐이 거쳐 가는 지렛대는 [[02-foundations/basic-mechanics|0.6.1 기초 역학 §5, §9]]이고, 유압 기계가 대신하는 전기 구동과 전압 곱하기 전류로서의 일률은 [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자 §1, §7]]이다.

### 읽고 나면

- [ ] 압력을 Pa, bar, psi 사이에서, 그리고 게이지와 절대 사이에서 바꾸고, 계산마다 어느 영점이 필요한지 말할 수 있다.
- [ ] 보어, 로드, 압력, 유량에서 실린더의 미는 힘과 당기는 힘, 늘어나고 줄어드는 속도, 행정 시간을 계산할 수 있다.
- [ ] 명령을 끝까지 준 단순 회로의 압력들 — 펌프, 밸브 모서리, 두 실 — 과 그 효율과 열을 찾을 수 있다.
- [ ] 오리피스의 압력 강하를 열린 면적과 유량으로 어림하고, 강하가 왜 유량의 제곱으로 크는지 말할 수 있다.
- [ ] 실린더의 유압 스프링 강성과, 그것이 움직이는 질량과 함께 이루는 고유 진동수를 계산하고, 긴 호스가 둘에 무엇을 하는지 말할 수 있다.
- [ ] 공기가 왜 무른지 식 하나로 말하고, 그 무름이 어디서 쓸모 있는지 꼽을 수 있다.
- [ ] 평평한 부재와 연직 부재에 대해 진공 리프터의 유지력, 안전율, 최소 진공을 계산하고, 펌프가 선 뒤 얼마나 버티는지 계산할 수 있다.

### 스스로 점검

1. V1의 게이지가 $-60\,\mathrm{kPa}$를 가리킨다. 컵 안의 절대 압력은 얼마이고, 어떤 진공 펌프도 그 게이지를 $-150\,\mathrm{kPa}$로 만들 수 없는 이유는?
2. H1이 늘어날 때와 줄어들 때 같은 $60\,\mathrm{L/min}$을 받는다. 어느 쪽이 빠르고 어느 쪽이 세며, 몇 배인가 — 그리고 한 압력에서 힘 곱하기 속도는 왜 양쪽이 같은가?
3. H1의 로드가 행정 끝에 닿은 뒤에도 방향 제어 밸브 명령이 들어가 있다. 펌프 유량은 어디로, 어떤 압력으로 가며, 기름에는 무슨 일이 생기나?
4. 긴 호스는 힘은 거의 바꾸지 않는데 왜 H1을 무르게도, 느리게도 만드나?
5. 공기는 왜 무르고 기름은 왜 뻣뻣한가 — 각각 식 하나로?
6. S1의 지지·체결 단계의 안전 상태는 브레이크를 건 정지 유지다. V1이 패널을 쥐고 있다면, 정지 유지가 안전하려면 무엇이 더 참이어야 하나?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $p_{\text{abs}}=p_g+p_{\text{atm}}=-60+101.3=41.3\,\mathrm{kPa}$. 게이지 압력은 절대 압력이 0이 되는 $-p_{\text{atm}}$까지만 내려간다. 유체는 밀 뿐 당기지 못하므로, 완전한 진공 아래에는 펌프가 닿을 곳이 없다.
> 2. 줄어들 때가 빠르고($0.199$ 대 $0.127\,\mathrm{m/s}$) 늘어날 때가 세다($25\,\mathrm{MPa}$에서 $196.3$ 대 $125.7\,\mathrm{kN}$). 둘 다 $\varphi=1.5625$배다. 힘은 $pA$, 속도는 $Q/A$이므로 그 곱 $pQ$에서 면적이 사라진다. 주어진 압력과 유량이 나르는 일률은 어느 면에 작용하든 같다.
> 3. 로드가 움직이지 못하니 실린더는 유량을 받지 않는다. 압력이 릴리프 설정까지 올라 $60\,\mathrm{L/min}$ 전부가 $25\,\mathrm{MPa}$로 릴리프를 건넌다. $25\,\mathrm{kW}$가 모두 열이고, 냉각이 없으면 H1의 $50\,\mathrm L$에서 분당 $18\,\mathrm K$다.
> 4. 호스는 양쪽에 기름 부피를 보태고, 스프링 강성 $\beta A^2/V$는 부피가 늘수록 준다. 그래서 팔의 고유 진동수가 떨어지고(호스 없이 $6.15\,\mathrm{Hz}$, $3\,\mathrm m$로 $5.27$, $10\,\mathrm m$로 $4.15$) 압력 형성이 길어진다, $V\Delta p/(\beta Q)$. 힘은 여전히 $pA$에서 호스의 작은 마찰 강하를 뺀 것이다.
> 5. 기름: $\beta=-V\,dp/dV$가 재료 상수이고, H1에서 약 $1\,\mathrm{GPa}$. 공기: $pV=\text{const}$에서 $\beta=p$, 절대 압력 그 자체 — 게이지 $0.6\,\mathrm{MPa}$에서 $0.7\,\mathrm{MPa}$로, 약 $1400$배 무르다.
> 6. 정지 유지가 이어질 수 있는 동안 컵이 펌프 없이 패널을 쥐고 있어야 한다. 체크 밸브와 진공 탱크가 있고, 누설이 작아 진공이 $S\ge2$의 최소값 위에 머물러야 하며 — 고정한 V1로는 $41\,\mathrm s$ — 그 시간이 다하기 전에 단계를 떠나도록 진공도를 감시해야 한다.

### 과제 · Problem set

Tier B. 이 페이지, 그 선수 지식, 이 페이지의 대상만 쓴다. H1과 V1은 고정한 그대로이고, 문항마다 밝힌 것만 바꾼다. 손으로 풀고, 시뮬레이터는 없다.

1. **그리기.** 같은 밸브를 거쳐 $90\,\mathrm{L/min}$ 펌프가 먹이는 H1과, 비에 젖은 같은 패널 위의 V1($\mu=0.25$)에 대해 위의 그림을 그려라. 위: 명령을 끝까지 준 회로의 유량과 압력, 그리고 $25\,\mathrm{MPa}$ 릴리프에 견준 펌프 압력의 막대. 아래: 진공도에 대한 연직 유지 용량과 $S=1$, $S=2$ 선, 작동점, 대기의 천장.
2. **유도.** (a) $90\,\mathrm{L/min}$의 H1: 로드와 날 끝의 속도, 행정 시간, 두 밸브 강하, 세 압력, 입력과 출력 일률, 효율, 기름이 데워지는 속도. (b) 이 밸브를 끝까지 연 H1이 릴리프를 열지 않고 팔을 들 수 있는 가장 큰 펌프 유량. (c) 젖은 패널 위의 V1: $60\,\mathrm{kPa}$에서의 안전율, $S=2$를 위한 최소 진공, 펌프가 선 뒤 $60\,\mathrm{kPa}$에서 그 수준까지의 시간. (d) 같은 누설로 젖은 패널을 5분 동안 $S\ge1$로 지킬 진공 탱크 $V_s$. (e) H1이 로드 포트를 막고 하중 없이 $25\,\mathrm{MPa}$로 밀 때의 로드측 압력, 그리고 릴리프가 그것을 막지 못하는 이유.
3. **해석.** 동료의 장비 사양서에 이렇게 적혀 있다. "붐 실린더(보어 $100\,\mathrm{mm}$, 로드 $60\,\mathrm{mm}$)는 우리 $60\,\mathrm{L/min}$ 펌프로 $0.5\,\mathrm{m/s}$로 늘어나고 $25\,\mathrm t$를 민다. 컵 넷짜리 리프터($100\,\mathrm{mm}$ 컵)는 $100\,\mathrm{kg}$을 들고, 더 큰 진공 펌프를 달면 $200\,\mathrm{kg}$을 든다." 각 주장을 이 페이지의 산수로 확인하라. 어느 것이 불가능하고 어느 것이 조건부로만 성립하는지, 그리고 확인할 수 있으려면 사양서가 무엇을 밝혀야 하는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - **위, 같은 다섯 부품**: 탱크, 펌프, 압력 라인 위의 릴리프 밸브, 명령을 끝까지 받은 밸브(P에서 A, B에서 T), 그리고 움직임에 맞서는 하중 화살표를 단 행정 중간의 실린더. 유량을 적는다. 헤드측으로 $90\,\mathrm{L/min}$, 로드측에서 $57.6\,\mathrm{L/min}$.
> - **압력은 그 자리에 적는다**: 압력 라인 $11.81\,\mathrm{MPa}$, 헤드측 $6.01\,\mathrm{MPa}$, 로드측 $2.37\,\mathrm{MPa}$, 탱크 $0$. 밸브의 두 모서리는 $5.79$와 $2.37\,\mathrm{MPa}$를 떼어 간다. 둘 다 $60\,\mathrm{L/min}$일 때의 $2.25=(90/60)^2$배이고, 그 배수만큼 크게 그리는 것이 이 문항의 요점이다.
> - **막대는 $0$에서 $25\,\mathrm{MPa}$까지의 선형 축에**: 부하 $4.50$, 배압 $1.52$, 밸브 $5.79$로 $11.81$에 닿고, 릴리프 선은 $25$에. 옆에 일률을 적는다. 입력 $17.7\,\mathrm{kW}$, 팔에 $6.74\,\mathrm{kW}$, $38\%$.
> - **아래, 기울기가 절반인 용량 선**: $\mu n_cA_c=7.85\,\mathrm{N/kPa}$, 원점에서 $101.3\,\mathrm{kPa}$의 $796\,\mathrm N$까지 가서 멈춘다.
> - **점선 둘은 그대로다**, $196\,\mathrm N$($S=1$)과 $392\,\mathrm N$($S=2$). 패널이 같기 때문이다. 움직이는 것은 용량 선이 그 선들과 만나는 곳, $25.0$과 $50.0\,\mathrm{kPa}$다.
> - **작동점을 찍는다**: $60\,\mathrm{kPa}$, $471\,\mathrm N$, $S=2.40$, 그리고 옆에 펌프가 선 뒤 $S=2$까지의 시간 $11.9\,\mathrm s$. 작동점이 여전히 $942\,\mathrm N$에 있거나 천장이 움직였다면 틀린 그림이다. 대기는 바뀌지 않았다.

> [!tip]- 정답 · Solutions
> 1. 그리는 법의 목록대로. 위: $v=0.191\,\mathrm{m/s}$; 압력 $11.81$, $6.01$, $2.37\,\mathrm{MPa}$; 강하 $5.79$, $2.37\,\mathrm{MPa}$; 입력 $17.7\,\mathrm{kW}$, 출력 $6.74\,\mathrm{kW}$. 아래: $60\,\mathrm{kPa}$에서 용량 $471\,\mathrm N$, $S=2.40$; $S=2$는 $50.0\,\mathrm{kPa}$, $S=1$은 $25.0\,\mathrm{kPa}$; 천장 $796\,\mathrm N$, $S=4.06$.
> 2. (a) $v=1.5\times10^{-3}/7.854\times10^{-3}=0.191\,\mathrm{m/s}$, 날 끝 $1.146\,\mathrm{m/s}$, 행정 $4.19\,\mathrm s$; 귀환 $57.6\,\mathrm{L/min}$. $\Delta p_{PA}=2.25\times2.574=5.791\,\mathrm{MPa}$, $\Delta p_{BT}=2.25\times1.054=2.372\,\mathrm{MPa}$; $p_B=2.372$, $p_A=4.497+2.372/1.5625=6.015$, $p_P=6.015+5.791=11.806\,\mathrm{MPa}$. 입력 $11.806\times1.5=17.71\,\mathrm{kW}$, 출력 $35\,316\times0.191=6.74\,\mathrm{kW}$, $\eta=38.1\%$; 열 $10.96\,\mathrm{kW}$가 기름을 $10\,964/82\,650=0.133\,\mathrm{K/s}$, 분당 $8.0\,\mathrm K$로 데운다. 유량을 절반 더 주어 속도를 $50\%$ 샀고, 그 값은 $3.4$배의 열이다. (b) 손실은 $Q^2$로 는다. $p_P=4.497+3.249\,(Q/60)^2\,\mathrm{MPa}$가 $(Q/60)^2=6.31$, 곧 $Q=151\,\mathrm{L/min}$에서 $25\,\mathrm{MPa}$에 닿는다. 그보다 많으면 릴리프가 열리고 늘린 유량은 팔에 닿지 않는다. (c) $S=0.25\times1885/196.2=2.40$; $\Delta p_{\min}=2\times196.2/(0.25\times0.031416)=50.0\,\mathrm{kPa}$; $(60\,000-49\,962)/844=11.9\,\mathrm s$. (d) 젖은 패널의 $S=1$에는 $25.0\,\mathrm{kPa}$가 필요하므로 $V_s=300\times101\,325\times1.667\times10^{-5}/35\,019=14.5\,\mathrm L$ — 계산 절의 마른 패널 $S=2$와 같은 부피다. $\mu$를 절반으로 하면 모든 최소 진공이 두 배가 되기 때문이다. (e) 피스톤은 $p_{\text{rod}}A_{\text{ann}}=p_{\text{cap}}A_{\text{cap}}$에서 균형을 이루므로 $p_{\text{rod}}=1.5625\times25=39.1\,\mathrm{MPa}$. 릴리프는 압력 라인을 지킨다. 로드측은 막힌 포트로 그것과 떨어져 있어서, 그 실을 막아 주는 것은 실 자신의 강도뿐이다.
> 3. "$0.5\,\mathrm{m/s}$로 늘어난다": $60\,\mathrm{L/min}$으로는 불가능하다. 늘어나려면 $0.5\times7.854\times10^{-3}=3.93\times10^{-3}\,\mathrm{m^3/s}$, $236\,\mathrm{L/min}$, 펌프의 $3.9$배가 필요하다. 펌프는 늘어날 때 $0.127\,\mathrm{m/s}$, 줄어들 때 $0.199\,\mathrm{m/s}$를 준다. (로드측에서 나온 기름을 헤드측으로 되돌리는 회로라면 연속 방정식에 따라 펌프는 로드 자신의 부피만 채우면 되어 $v=Q/A_{\text{rod}}=0.354\,\mathrm{m/s}$ — 그래도 모자라고, 미는 힘은 $25\,\mathrm{MPa}$에서 $p\,A_{\text{rod}}=70.7\,\mathrm{kN}$뿐이다.) "$25\,\mathrm t$를 민다": $245\,\mathrm{kN}$에는 헤드측에 $31.2\,\mathrm{MPa}$가 필요해 $25\,\mathrm{MPa}$ 릴리프를 넘는다. 그 천장은 $196\,\mathrm{kN}$, $20.0\,\mathrm t$다. "$100\,\mathrm{kg}$을 든다": 눕혀서만, 그것도 겨우 — $60\,\mathrm{kPa}$에서 $1885/981=1.92$로 안전율 $2$ 아래 — 이고, 연직면에서는 컵 넷이 $942\,\mathrm N<981\,\mathrm N$을 지므로 패널이 미끄러진다. 연직으로 $S=2$를 내려면 대기압을 넘는 $124.9\,\mathrm{kPa}$가 필요하다. "더 큰 펌프로 $200\,\mathrm{kg}$": §9의 천장 때문에 불가능하다. 완전한 진공도 눕혀서 $3183\,\mathrm N$, 연직으로 $1592\,\mathrm N$ — 여유 없이 $324$와 $162\,\mathrm{kg}$ — 이고, 필요한 것은 더 많은 컵이다(연직, $60\,\mathrm{kPa}$, $S=2$로 이 컵 열일곱 개). 확인할 수 있으려면 사양서는 속도 뒤의 유량과 움직이는 방향, 힘이 로드에서의 값인지와 그 압력, 그리고 리프터에 대해서는 면의 방향, $\mu$와 표면, 정격이 가정하는 진공과 감시하는 최소 진공, 안전율을 밝혀야 한다.

### 출처

- OpenStax, *University Physics Volume 1*(https://openstax.org/books/university-physics-volume-1, HTML) — §14.1 스칼라인 압력, $p=p_0+\rho gh$, $8800\,\mathrm m$마다 $1/e$로 줄어드는 대기압; §14.2 게이지 압력과 절대 압력, 바닥값 $-p_{\text{atm}}$; §14.3 파스칼의 원리; §14.5 유량과 연속 방정식; §14.6 베르누이 방정식; §14.7 푸아죄유 법칙과 레이놀즈 수, 약 $2000$ 아래의 층류와 약 $3000$ 위의 난류; §12.3 물($0.22\times10^{10}\,\mathrm{Pa}$)과 강철($16\times10^{10}\,\mathrm{Pa}$)의 체적 탄성 계수, 강철의 영률($20.0\times10^{10}\,\mathrm{Pa}$).
- OpenStax, *University Physics Volume 2*(https://openstax.org/books/university-physics-volume-2, HTML) — §1.4 $Q=mc\Delta T$와 물의 $4186\,\mathrm{J/(kg{\cdot}K)}$; §2.1 절대 압력으로 쓰는 이상 기체 법칙; §3.6 단열 압축, 2원자 기체에서 $\gamma=1.4$로 $pV^\gamma$ 일정.
- OpenStax, *College Physics 2e*, [12.3 The Most General Applications of Bernoulli's Equation](https://openstax.org/books/college-physics-2e/pages/12-3-the-most-general-applications-of-bernoullis-equation) — 흐름의 일률, 유체에 공급되는 일률로서의 $pQ$.
- NIST, *Guide for the Use of the International System of Units (SI)*, SP 811: [7장](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-7-rules-and-style-conventions-expressing-values) — §7.4 단위 기호에 정보를 붙이지 않음; [부록 B.8](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8) — $1\,\mathrm{psi}=6.894\,757\times10^3\,\mathrm{Pa}$, $1\,\mathrm{bar}=10^5\,\mathrm{Pa}$, $1\,\mathrm{atm}=1.013\,25\times10^5\,\mathrm{Pa}$.
- Schmalz, 제조사의 진공 페이지(HTML): [Theoretical Holding Force of a Suction Cup](https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/theoretical-holding-force-of-a-suction-cup) — 하중 경우 $m(g+a)S$와 $(m/\mu)(g+a)S$, 최소 $1.5$(매끄럽고 치밀한 부재)와 $2.0$(까다롭거나 다공질이거나 거칠거나 기름 묻은 부재)의 안전율, 시험으로 확인해야 하는 마찰 계수 참고값; [Holding force](https://www.schmalz.com/en-us/support/know-how/glossary/holding-force) — 상대 진공도 $60\%$에서 적는 이론값 $F=\Delta p\times A$; [Vacuum Generators](https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/vacuum-generators) — 벤투리 원리로 일하는 이젝터; [Vacuum Generator Selection](https://www.schmalz.com/en/support/know-how/vacuum-knowledge/the-vacuum-system-and-its-components/system-design-calculation-example/vacuum-generator-selection) — 다공질 부재의 흡착 시험.
- Aerolift, [Standards and safety regulations on vacuum lifting](https://www.aerolift.nl/en/standards-and-safety-regulations-vacuum-lifting/)(진공 리프터 제조사가 요약한 EN 13155, HTML) — 정전 뒤 5분 하중 유지, 펌프와 진공 탱크 사이의 역지 밸브, 진공이 위험 범위에 들면 눈과 귀로 알리는 경보, 안전율 2의 설계. 표준 자체는 읽지 않았다.
- 이 위키 안: [[02-foundations/engineering-math|0.5 §8]] — 미분방정식과 $\omega_n$; [[05-construction-robotics/site-engineering|2.5 현장 로보틱스]] — S1과 S2, 그리고 그 §3의 안전 상태; [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 §1]] — 지연 오버슈트; [[04-robotics/grasping|15. 파지 §2]]와 §6 — 마찰; [[04-robotics/actuators-drives|10.5 §4]] — 반사 관성.
- H1과 V1은 이 페이지가 정의한 교과 대상이고, 이 페이지의 모든 숫자는 그것들과 S1, S2, 위의 출처에서 여기서 계산했다.
