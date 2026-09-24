---
title: "0.6.2 Basic Circuits and Electronics"
tags: [foundations, physics, electronics]
study-depth: Working
depth-goal: "On P6's cart, turn a push in newtons into amperes, volts, a duty cycle and a battery current, and back into microvolts and ADC counts; size a divider, an RC filter and an amplifier gain; and say why an inductive load needs a freewheeling path and why an emergency stop must cut power."
mastery-when: "Raise to Mastery when the thesis builds or instruments hardware — a sensor chain, a motor drive or a safety circuit — whose electrical design carries the result."
wiki-support: Working
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §1]] (derivatives) · [[02-foundations/engineering-math|0.5 §4]] (a 2×2 linear system) · [[02-foundations/engineering-math|0.5 §4.5]] (linearity) · [[02-foundations/engineering-math|0.5 §6]] ($e^x$) · [[02-foundations/engineering-math|0.5 §7]] (complex numbers) · [[02-foundations/engineering-math|0.5 §8]] (first-order ODEs) · [[02-foundations/engineering-math|0.5 §9]] (transfer functions, frequency response) · plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]]
> [[02-foundations/engineering-math|0.5 §1]](미분) · [[02-foundations/engineering-math|0.5 §4]](2×2 연립 일차방정식) · [[02-foundations/engineering-math|0.5 §4.5]](선형성) · [[02-foundations/engineering-math|0.5 §6]]($e^x$) · [[02-foundations/engineering-math|0.5 §7]](복소수) · [[02-foundations/engineering-math|0.5 §8]](1차 상미분방정식) · [[02-foundations/engineering-math|0.5 §9]](전달함수, 주파수 응답) · [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6**

## English

*Stands on [[02-foundations/engineering-math|0.5 Engineering Math]] — the derivative, the first-order ODE and its exponential, complex numbers — and on plant **P6** of [[02-foundations/lab-plants|0.6 Lab Plants]], whose controller "commands a motor at 200 Hz" without saying what lies between the command and the motor. The first use of P6's electronics. Its motor is the one [[04-robotics/actuators-drives|10.5 Actuators & Drives]] freezes for P2, so the two pages agree number for number, and its sensing chain is the floor under [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] and [[02-foundations/signal-processing|6. Signal Processing]].*

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] — perception, object and scene understanding, grasping, motion and task planning, manipulation, contact, force and tactile feedback, learning and adaptation, task completion — this page is the physical floor under the actuation and sensing layers: in *"Install that panel on the frame"* it is the drive that moves the panel and the force sensor that feels it touch (its place is marked on the [[physical-ai-map|Physical AI Map]]). A robot's motor and force sensor are circuits before they are signals, and circuit mistakes pass for control or learning failures: a sensor ground shared with the motor's return turns $2.0\,\mathrm A$ into a phantom $0.25\,\mathrm N$ on P6's load cell, and an emergency stop sent as a message fails exactly when the software does. The winding, duty cycle, bridge and sampler taught here carry into [[04-robotics/actuators-drives|10.5 §5]], [[04-robotics/sensor-models|3.2 Sensor Models §4]], [[02-foundations/signal-processing|6. Signal Processing §2]] and [[04-robotics/force-compliance-control|13. §2]], and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) the page sits in block 1, the foundations floor, taken where a civil-engineering degree left electricity out. After it you can follow a force from newtons to amperes, volts and a duty cycle and back to ADC counts, and size the divider, filter and gain in between.

> [!note] First pass · 처음이라면
> Two sessions of about ninety minutes each. The picture is the whole page as one loop, so look at it first and come back to it after each section. **Session 1, the power path:** §1–§4 — units, Ohm's law, Kirchhoff's laws and the divider, the capacitor and the inductor — then §6–§7, how a 24 V battery becomes a steady 2.0 A in a motor. End it by explaining to yourself why the battery supplies only 0.167 A while the winding carries 2.0 A (Self-check 2). **Session 2, the sensing path:** §5 (the filter) and §8–§10 (amplifier, bridge, ADC), then the Worked case, which follows one 10 N push out through the motor and back in through the load cell; read §11 before you wire anything, run the lab of §12, and answer the rest of the Self-check. The collapsed *Deeper* note can wait for a second reading.

### Running object · 이 페이지의 대상

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]]: a cart on a line, its position in metres, an encoder at $2048$ counts/m, and a controller that samples the encoder and commands a motor at $200\,\mathrm{Hz}$. The catalog stops at the word *motor*. This page fills in what a real cart carries between its battery and its controller, and freezes it: a battery, a fuse and an emergency stop; an H-bridge that drives the motor by pulse-width modulation; the motor, which turns a belt pulley that moves the cart; and a sensor the catalog does not have — a strain-gauge load cell between the cart and its tool, read through an instrumentation amplifier, an RC filter and an analog-to-digital converter (ADC). The task is the robotics running task in one dimension: the cart drives its tool against a panel and holds a push.

**The motor is 10.5's.** Its winding, torque constant, current limit and supply are the numbers [[04-robotics/actuators-drives|10.5 Actuators & Drives]] freezes for each joint of P2, so a current or a voltage computed here is the same number there. Everything else in the table is this page's own: course numbers of a realistic order, chosen for this page, and not the measurement or the datasheet value of any product.

| Symbol | Value | What it is |
|---|---:|---|
| $V_s$ | $24\,\mathrm V$ | battery voltage; 10.5's supply (§1) |
| $Q$ | $5.0\,\mathrm{Ah}$ | battery capacity on the label (§1) |
| $r_b$ | $0.050\,\Omega$ | battery internal resistance (§11) |
| fuse | $15\,\mathrm A$ | in the battery's positive lead (§11) |
| $R$, $L$ | $1.0\,\Omega$, $1.0\,\mathrm{mH}$ | winding resistance and inductance; 10.5 (§4, §7) |
| $k_t$, $k_e$ | $0.10\,\mathrm{N{\cdot}m/A}$, $0.10\,\mathrm{V{\cdot}s/rad}$ | torque and back-EMF constants; 10.5 (§7) |
| $I_{\max}$ | $10\,\mathrm A$ | the drive's current limit; 10.5 (§7) |
| $f_{\text{PWM}}$ | $20\,\mathrm{kHz}$, so $T=50\,\mu\mathrm s$ | switching frequency of the H-bridge (§6) |
| $R_{\text{on}}$, $V_F$ | $10\,\mathrm{m\Omega}$, $0.7\,\mathrm V$ | a conducting MOSFET's resistance; a conducting diode's drop (§6) |
| $r_p$ | $0.020\,\mathrm m$ | belt-pulley radius (§7) |
| $F_{\text{roll}}$ | $2.0\,\mathrm N$ | rolling resistance while the cart cruises (§7) |
| encoder | $2048$ counts/m | P6's catalog number; read by a counter, not an ADC (§10) |
| load cell | $50\,\mathrm N$ rated, $2.0\,\mathrm{mV/V}$ | a full bridge of four $350\,\Omega$ foil gauges, gauge factor $2.0$ (§9) |
| $V_{ex}$ | $5.0\,\mathrm V$ | bridge excitation (§9) |
| $G$ | $400$ | instrumentation-amplifier gain (§8); swept in §10 |
| $A$ | $10^5$ | open-loop gain of each op-amp (§8) |
| $R_f$, $C_f$ | $3.3\,\mathrm{k\Omega}$, $1.0\,\mu\mathrm F$ | anti-alias RC filter before the ADC (§5); swept in §12 |
| ADC | $12$ bits, $V_{\text{ref}}=4.096\,\mathrm V$ | sampled at $200\,\mathrm{Hz}$, P6's control rate (§10) |
| battery monitor | $100\,\mathrm{k\Omega}$ over $15\,\mathrm{k\Omega}$ | the divider that scales the battery for the ADC (§3) |

Two modelling choices, stated once. The switches are ideal apart from $R_{\text{on}}$ and $V_F$, and the belt drive from motor to cart is lossless: this page is about the circuit, and the friction and inertia of a drive train belong to [[04-robotics/actuators-drives|10.5]]. With a lossless belt a torque $\tau$ pushes the cart with $\tau/r_p$, so the drive's $10\,\mathrm A$ limit is a push of $0.10\cdot10/0.020=50\,\mathrm N$ — the load cell's rating, so the sensor can read everything the motor can do. The $2.0\,\mathrm{mV/V}$ and the $350\,\Omega$ gauges are of the kind load-cell and strain-gauge makers describe (Sources), and none of these values is taken from a datasheet.

*Scope: this page teaches the circuit physics a robot's electronics run on, on one cart: charge, current, voltage, power and energy; resistors, Kirchhoff's laws, dividers and loading; capacitors, inductors and their time constants; the RC low-pass filter; switches, pulse-width modulation and the H-bridge with its freewheeling path; the DC motor as a circuit element; op-amps and the instrumentation amplifier; the Wheatstone bridge and the strain-gauge load cell; the ADC; and grounding, noise and electrical safety. It does not teach semiconductor physics, AC power, power-supply design, brushless-motor commutation or communication buses (§13 lists what else it leaves out). Frequency response and sampling in depth are [[02-foundations/signal-processing|6. Signal Processing]], the noise models of P6's sensors are [[04-robotics/sensor-models|3.2 Sensor Models & Noise]], the drive's thermal, speed and current limits are [[04-robotics/actuators-drives|10.5 Actuators & Drives]], and the safety vocabulary is [[04-robotics/hri-safety|11. HRI & Safety]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 404" style="max-width:100%;height:auto" role="img" aria-label="P6's cart electronics as one loop during a 10 N push: battery, fuse and emergency stop feeding an H-bridge whose on path runs through Q1 and Q4 and whose freewheel path runs through Q2 and Q4; an inset of the winding voltage pulses and the 2.0 A current with its 0.092 A ripple; the motor turning a pulley that pushes the cart and its load cell against a panel; and the load-cell bridge, instrumentation amplifier, RC filter, ADC and controller that read 800 counts and set the duty">
  <defs><marker id="bceA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="10" y="16" font-size="12" font-weight="600" fill="currentColor">P6's electronics, holding the 10 N push</text>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <polyline points="34,100 34,46 78,46"/><polyline points="106,46 132,46"/><polyline points="158,46 330,46 330,66"/>
    <polyline points="34,108 34,176 330,176 330,156"/>
    <line x1="22" y1="100" x2="46" y2="100" stroke-width="2"/><line x1="28" y1="108" x2="40" y2="108" stroke-width="3"/>
    <rect x="78" y="41" width="28" height="10" rx="2"/><line x1="78" y1="46" x2="106" y2="46" stroke-width="0.8"/>
    <line x1="130" y1="42" x2="160" y2="42" stroke-width="1.8"/>
    <polyline points="210,46 210,66"/><polyline points="210,90 210,132"/><polyline points="210,156 210,176"/>
    <polyline points="330,90 330,132"/>
    <rect x="199" y="66" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <rect x="199" y="132" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <rect x="319" y="66" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <rect x="319" y="132" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <polyline points="210,60 190,60 190,70"/><polyline points="190,84 190,96 210,96"/>
    <line x1="184" y1="70" x2="196" y2="70" stroke-width="1.4"/>
    <path d="M 190 70 L 184 84 L 196 84 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="210,126 190,126 190,136"/><polyline points="190,150 190,162 210,162"/>
    <line x1="184" y1="136" x2="196" y2="136" stroke-width="1.4"/>
    <path d="M 190 136 L 184 150 L 196 150 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="330,60 350,60 350,70"/><polyline points="350,84 350,96 330,96"/>
    <line x1="344" y1="70" x2="356" y2="70" stroke-width="1.4"/>
    <path d="M 350 70 L 344 84 L 356 84 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="330,126 350,126 350,136"/><polyline points="350,150 350,162 330,162"/>
    <line x1="344" y1="136" x2="356" y2="136" stroke-width="1.4"/>
    <path d="M 350 136 L 344 150 L 356 150 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="210,111 244,111"/><polyline points="296,111 330,111"/>
    <rect x="244" y="101" width="52" height="20" rx="4" fill="currentColor" fill-opacity="0.08"/>
  </g>
  <g fill="currentColor"><circle cx="132" cy="46" r="2.2"/><circle cx="158" cy="46" r="2.2"/><circle cx="210" cy="111" r="2.4"/><circle cx="330" cy="111" r="2.4"/></g>
  <polyline points="228,54 228,95 308,95 308,170" fill="none" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.8" marker-end="url(#bceA)"/>
  <polyline points="234,166 234,127 314,127" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#bceA)"/>
  <polyline points="314,127 314,166 238,166" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#bceA)"/>
  <line x1="270" y1="121" x2="270" y2="226" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <g font-size="11" fill="currentColor">
    <text x="52" y="96">battery</text><text x="52" y="110">24 V · 5.0 Ah</text>
    <text x="52" y="134" font-size="10">battery current</text><text x="52" y="147" font-size="10">0.167 A, 4.0 W</text>
    <text x="92" y="34" text-anchor="middle">fuse 15 A</text><text x="145" y="64" text-anchor="middle" font-size="10">E-stop (NC)</text>
    <text x="34" y="192">0 V (ground)</text>
    <text x="210" y="82" text-anchor="middle" font-size="10">Q1</text><text x="210" y="148" text-anchor="middle" font-size="10">Q2</text>
    <text x="330" y="82" text-anchor="middle" font-size="10">Q3</text><text x="330" y="148" text-anchor="middle" font-size="10">Q4</text>
    <text x="270" y="115" text-anchor="middle">M</text>
    <text x="238" y="89" font-size="10">1.0 Ω · 1.0 mH</text>
    <text x="276" y="199" font-size="10">solid: on, 4.17 µs of 50 µs (Q1, Q4)</text><text x="276" y="211" font-size="10">dashed: freewheel, 45.8 µs (Q2, Q4)</text>
  </g>
  <rect x="370" y="26" width="182" height="166" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.9"/>
  <polyline points="384.0,80.0 384.0,58.0 388.8,58.0 388.8,80.0 441.0,80.0 441.0,58.0 445.8,58.0 445.8,80.0 498.0,80.0" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="384.0,164.3 385.2,152.0 386.4,139.8 387.6,127.6 388.8,115.4 394.0,120.4 399.2,125.3 404.4,130.3 409.6,135.2 414.9,140.1 420.1,145.0 425.3,149.8 430.6,154.7 435.8,159.5 441.0,164.3 441.0,164.3 442.2,152.0 443.4,139.8 444.6,127.6 445.8,115.4 451.0,120.4 456.2,125.3 461.4,130.3 466.6,135.2 471.9,140.1 477.1,145.0 482.3,149.8 487.6,154.7 492.8,159.5 498.0,164.3" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="384.0" y1="115.4" x2="498.0" y2="115.4" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 2.5" stroke-opacity="0.5"/>
  <line x1="384.0" y1="140.0" x2="498.0" y2="140.0" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4 3" stroke-opacity="0.75"/>
  <line x1="384.0" y1="164.3" x2="498.0" y2="164.3" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 2.5" stroke-opacity="0.5"/>
  <line x1="384.0" y1="80" x2="498.0" y2="80" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.4"/>
  <g stroke="currentColor" stroke-width="0.9"><line x1="384.0" y1="176" x2="384.0" y2="180"/><line x1="441.0" y1="176" x2="441.0" y2="180"/><line x1="498.0" y1="176" x2="498.0" y2="180"/></g>
  <g font-size="10" fill="currentColor">
    <text x="378" y="40" font-size="11">winding, two PWM periods</text>
    <text x="386" y="53">v: 24 V for 4.17 µs</text>
    <text x="502" y="62">24 V</text><text x="502" y="84">0 V</text>
    <text x="386" y="103">i: ripple 0.092 A p-p</text>
    <text x="502" y="118.9">2.046 A</text>
    <text x="502" y="143.5">mean 2.0</text>
    <text x="502" y="167.8">1.954 A</text>
    <text x="384.0" y="188" text-anchor="middle">0</text><text x="441.0" y="188" text-anchor="middle">50</text><text x="498.0" y="188" text-anchor="middle">100 µs</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <circle cx="270" cy="238" r="12"/>
    <line x1="270" y1="226" x2="400" y2="226"/><line x1="270" y1="250" x2="392" y2="250" stroke-opacity="0.5"/>
    <rect x="400" y="216" width="60" height="26" rx="3" fill="currentColor" fill-opacity="0.08"/>
    <circle cx="412" cy="246" r="4"/><circle cx="448" cy="246" r="4"/>
    <line x1="380" y1="251" x2="500" y2="251" stroke-width="1" stroke-opacity="0.6"/>
    <rect x="460" y="222" width="14" height="14" fill="currentColor" fill-opacity="0.25"/>
    <line x1="474" y1="229" x2="502" y2="229" stroke-width="2.4"/>
    <line x1="504" y1="206" x2="504" y2="262" stroke-width="2.4"/>
    <path d="M 504 212 L 512 206 M 504 220 L 512 214 M 504 228 L 512 222 M 504 236 L 512 230 M 504 244 L 512 238 M 504 252 L 512 246 M 504 260 L 512 254" stroke-width="0.8" stroke-opacity="0.6"/>
  </g>
  <circle cx="270" cy="238" r="1.6" fill="currentColor"/>
  <line x1="480" y1="219" x2="499" y2="219" stroke="currentColor" stroke-width="1.3" marker-end="url(#bceA)"/>
  <line x1="467" y1="236" x2="506" y2="287" stroke="currentColor" stroke-width="1.1" stroke-dasharray="1.5 2.5"/>
  <g font-size="11" fill="currentColor">
    <text x="254" y="235" text-anchor="end" xml:space="preserve">pulley r<tspan dy="3" font-size="10">p</tspan><tspan dy="-3"> = 20 mm</tspan></text>
    <text x="254" y="250" text-anchor="end">τ = 0.20 N·m</text>
    <text x="292" y="244" xml:space="preserve">F = k<tspan dy="3" font-size="10">t</tspan><tspan dy="-3">i / r</tspan><tspan dy="3" font-size="10">p</tspan><tspan dy="-3"> = 10 N</tspan></text>
    <text x="430" y="233" text-anchor="middle" font-size="10">cart</text>
    <text x="467" y="213" text-anchor="middle" font-size="10">load cell</text>
    <text x="516" y="232" font-size="10">panel</text>
    <text x="482" y="266" text-anchor="end" font-size="10">strain</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <path d="M 510 288 L 540 318 L 510 348 L 480 318 Z"/>
    <rect x="487.0" y="299.5" width="16" height="7" transform="rotate(-45 495.0 303.0)" fill="currentColor" fill-opacity="0.15"/>
    <rect x="517.0" y="299.5" width="16" height="7" transform="rotate(45 525.0 303.0)" fill="currentColor" fill-opacity="0.15"/>
    <rect x="487.0" y="329.5" width="16" height="7" transform="rotate(45 495.0 333.0)" fill="currentColor" fill-opacity="0.15"/>
    <rect x="517.0" y="329.5" width="16" height="7" transform="rotate(-45 525.0 333.0)" fill="currentColor" fill-opacity="0.15"/>
    <line x1="510" y1="348" x2="510" y2="354"/><line x1="502" y1="354" x2="518" y2="354"/><line x1="505" y1="357" x2="515" y2="357"/><line x1="508" y1="360" x2="512" y2="360"/>
    <polyline points="480,318 462,318 462,306 446,306"/>
    <polyline points="540,318 552,318 552,368 458,368 458,330 446,330"/>
    <path d="M 446 296 L 446 340 L 398 318 Z" fill="currentColor" fill-opacity="0.06"/>
    <polyline points="398,318 348,318"/><rect x="320" y="313" width="28" height="10" fill="currentColor" fill-opacity="0.1"/><polyline points="320,318 280,318"/>
    <polyline points="304,318 304,330"/><line x1="294" y1="330" x2="314" y2="330" stroke-width="2"/><line x1="294" y1="336" x2="314" y2="336" stroke-width="2"/><polyline points="304,336 304,344"/>
    <line x1="296" y1="344" x2="312" y2="344"/><line x1="299" y1="347" x2="309" y2="347"/><line x1="302" y1="350" x2="306" y2="350"/>
    <rect x="214" y="298" width="66" height="40" rx="3" fill="currentColor" fill-opacity="0.06"/>
    <rect x="10" y="292" width="152" height="56" rx="3" fill="currentColor" fill-opacity="0.06"/>
  </g>
  <g fill="currentColor"><circle cx="304" cy="318" r="2.2"/></g>
  <line x1="214" y1="318" x2="165" y2="318" stroke="currentColor" stroke-width="1.3" marker-end="url(#bceA)"/>
  <polyline points="80,292 80,206 196,206 196,186" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="6 3" marker-end="url(#bceA)"/>
  <g font-size="10" fill="currentColor">
    <text x="518" y="290" font-size="11">5.0 V</text>
    <text x="452" y="290">2.0 mV</text>
    <text x="422" y="356" text-anchor="middle">in-amp</text>
    <text x="424" y="322" text-anchor="middle">× 400</text>
    <text x="440" y="310" text-anchor="middle">+</text><text x="440" y="334" text-anchor="middle">−</text>
    <text x="373" y="311" text-anchor="middle">0.80 V</text>
    <text x="334" y="308" text-anchor="middle">3.3 kΩ</text>
    <text x="304" y="364" text-anchor="middle">1.0 µF</text>
    <text x="304" y="377" text-anchor="middle" xml:space="preserve">f<tspan dy="3" font-size="10">c</tspan><tspan dy="-3"> = 48 Hz</tspan></text>
    <text x="247" y="315" text-anchor="middle" font-size="11">ADC</text><text x="247" y="330" text-anchor="middle">12 bit</text>
    <text x="247" y="352" text-anchor="middle">1 mV/count</text>
    <text x="190" y="312" text-anchor="middle">800</text>
    <text x="86" y="308" text-anchor="middle" font-size="11">controller, 200 Hz</text><text x="86" y="323" text-anchor="middle">800 counts → 10.0 N</text><text x="86" y="338" text-anchor="middle">asks 2.0 A → D = 8.33 %</text>
    <text x="88" y="221">duty 8.33 % at 20 kHz → gates</text>
    <text x="510" y="385" text-anchor="middle">bridge 4 × 350 Ω</text><text x="510" y="398" text-anchor="middle">2.0 mV/V at 50 N</text>
  </g>
</svg>

P6's electronics as one loop, holding the Worked case's $10\,\mathrm N$ push. Top: the battery feeds the H-bridge through the fuse and the emergency stop; Q1 and Q4 put $24\,\mathrm V$ across the winding for $4.17\,\mu\mathrm s$ of every $50\,\mu\mathrm s$ (solid path), and for the other $45.8\,\mu\mathrm s$ the current freewheels through Q2 and Q4 (dashed path), so the winding carries $2.0\,\mathrm A$ with a $0.092\,\mathrm A$ ripple (inset) while the battery supplies only $0.167\,\mathrm A$. Bottom: the push strains the load cell's bridge to $2.0\,\mathrm{mV}$, the amplifier makes it $0.80\,\mathrm V$, the RC filter passes it, the ADC reports $800$ counts, and the controller reads $10.0\,\mathrm N$ and sets the duty that closes the loop.

### 1. Charge, current, voltage, power and energy

A circuit is analysed with three quantities that are easy to blur, and blurring them produces the classic errors — a motor that "uses up current", a runtime read off ampere-hours alone. Every quantity on this page is one of three things: how much charge moves, how much energy each unit of charge carries, or their product, power. Charge $q$ is counted in coulombs, and nature fixes its grain: one electron carries $e=1.602176634\times10^{-19}\,\mathrm C$, a value the SI makes exact (NIST), so a coulomb is $6.24\times10^{18}$ electrons.

If electricity is new, one picture carries a long way: a circuit is a closed loop of pipe full of water. Voltage plays pressure — the push behind each unit of what flows — and current plays the volume flow; a battery is a pump that holds a fixed pressure difference across itself, a wire is a wide pipe, and a resistor is a narrow one that turns pressure into heat. Power is pressure times flow in both worlds: what fluid power writes $pQ$, this page writes $vi$. The picture is weakest at the capacitor and the inductor, and §4 gives a better one for those.

> **Current, voltage and power, defined.** **Current**, **voltage** and **power** are *three rates of one flow* — charge per time, energy per charge and energy per time — and each belongs to a place in the circuit rather than to the circuit as a whole: current to a branch, voltage to a pair of points, power to an element. Three defining conditions, one per quantity. Current $i$ is the rate at which charge crosses a chosen cross-section, counted positive along a chosen arrow; *conventional* current is the direction positive charge would move, so the electrons in a wire drift against it (OpenStax). Voltage $v$ is a **difference** between two points, the energy one coulomb gains or gives up in going from one to the other; "the voltage at a node" always means relative to a reference node, the ground of §11. And the power an element absorbs is the voltage across it times the current through it, counted positive when the current enters its $+$ terminal, which follows from the first two by the chain rule of [[02-foundations/engineering-math|0.5 §1]]:
>
> $$i=\frac{dq}{dt},\qquad v=\frac{dw}{dq},\qquad p=\frac{dw}{dt}=\frac{dw}{dq}\,\frac{dq}{dt}=v\,i$$
>
> where $w$ is the energy delivered to the element in joules — so the units are $1\,\mathrm A=1\,\mathrm{C/s}$, $1\,\mathrm V=1\,\mathrm{J/C}$ and $1\,\mathrm W=1\,\mathrm{J/s}=1\,\mathrm{V{\cdot}A}$.
> - **Example**: the winding during the push. $i=2.0\,\mathrm A$ is $2.0$ coulombs, $1.25\times10^{19}$ electrons, through it every second; $v=2.0\,\mathrm V$ across it means each coulomb leaves $2.0\,\mathrm J$ there; so it absorbs $p=4.0\,\mathrm W$.
> - **Non-example**: "the motor uses up current." Charge is conserved, so the $2.0\,\mathrm A$ that enters the winding leaves it (§3); what the winding takes is energy, $2.0\,\mathrm J$ from every coulomb that passes. And "the motor gets $24\,\mathrm V$ because the battery is $24\,\mathrm V$": the battery's $24\,\mathrm V$ is between its own two terminals, and during the push the drive puts an average of only $2.0\,\mathrm V$ across the motor (§6).
> - **Why it matters**: power is where the circuit meets everything else — heat in a resistor (§2), force times speed at the cart (§7) — and energy is what a battery holds.

A battery's label gives its charge in ampere-hours, $1\,\mathrm{A{\cdot}h}=3600\,\mathrm C$ exactly (NIST), and its energy is that charge times its voltage, in watt-hours, $1\,\mathrm{W{\cdot}h}=3600\,\mathrm J$:

$$E=V_s\,Q=24\,\mathrm V\times5.0\,\mathrm{Ah}=120\,\mathrm{Wh}=432\,\mathrm{kJ}$$

since $5.0\times3600=18{,}000\,\mathrm C$, each carrying $24\,\mathrm J$, is $432\,\mathrm{kJ}$. Runtime is a question about energy, not charge, because the drive converts one current into another: during the push the motor carries $2.0\,\mathrm A$ while the battery supplies $0.167\,\mathrm A$ (Worked case). What the two sides share is power, $4.0\,\mathrm W$ each, so the label's $120\,\mathrm{Wh}$ holds the push for $120/4.0=30\,\mathrm h$ and the cruise of §7, at $1.16\,\mathrm W$, for $103\,\mathrm h$. That is the motor's share only — the controller and the sensors draw on the same battery — and how much of the label is usable depends on the battery, which this page does not model.

Every unit on this page is an SI unit with a special name, and writing each in terms of the others (NIST SP 811, Table 3) turns two products of circuit parameters into times:

| Unit | Symbol | In other SI units | Quantity |
|---|---|---|---|
| coulomb | C | A·s | charge |
| volt | V | W/A, or J/C | voltage |
| ohm | Ω | V/A | resistance (§2) |
| farad | F | C/V | capacitance (§4) |
| henry | H | Wb/A, or V·s/A | inductance (§4) |

$$1\,\Omega\cdot1\,\mathrm F=\frac{\mathrm V}{\mathrm A}\cdot\frac{\mathrm{A{\cdot}s}}{\mathrm V}=1\,\mathrm s,\qquad \frac{1\,\mathrm H}{1\,\Omega}=\frac{\mathrm{V{\cdot}s/A}}{\mathrm{V/A}}=1\,\mathrm s$$

so a resistance times a capacitance and an inductance over a resistance are both times — the two time constants of §4 — and the same bookkeeping gives $1\,\mathrm{N{\cdot}m/A}=1\,\mathrm{J/(A{\cdot}rad)}=1\,\mathrm{V{\cdot}s/rad}$, which is why [[04-robotics/actuators-drives|10.5 §1]] can write $k_t=k_e$ in SI units.

### 2. Resistors: Ohm's law, heat, series and parallel

Every wire, winding and switch on the cart resists the current through it, and what that costs in voltage and in heat is this section's question. A resistor turns electrical energy into heat at a rate set by the current through it. The relation between its voltage and its current is the simplest law in circuits, and every loop below uses it.

> **Resistance and Ohm's law, defined.** **Resistance** is a *property of a two-terminal element*, the ratio of the voltage across it to the current through it, in ohms; **Ohm's law** is the claim that this ratio is a constant, which is what makes the element a *resistor*. Three defining conditions. It is **linear**: doubling the current doubles the voltage, in either direction — additivity and homogeneity in the sense of [[02-foundations/engineering-math|0.5 §4.5]]. It is **memoryless**: the voltage now depends only on the current now, which is what separates a resistor from the storage elements of §4. And it holds **at a fixed temperature**: a metal's resistance rises as $R=R_0(1+\alpha\,\Delta T)$, with $\alpha=0.0039$ per kelvin for copper (OpenStax). Geometry sets the value: a conductor of resistivity $\rho$, length $\ell$ and cross-section $A_c$ has $R=\rho\ell/A_c$, with $\rho=1.68\times10^{-8}\,\Omega{\cdot}\mathrm m$ for copper at $20\,^\circ\mathrm C$ (OpenStax).
>
> $$v=R\,i,\qquad p=v\,i=i^2R=\frac{v^2}{R},\qquad R=\frac{\rho\,\ell}{A_c}$$
>
> where the power forms follow from putting $v=Ri$ into §1's $p=vi$, so every watt a resistor absorbs leaves it as heat.
> - **Example**: the winding, $R=1.0\,\Omega$. The push's $2.0\,\mathrm A$ needs $2.0\,\mathrm V$ and makes $4.0\,\mathrm W$ of heat, and the same winding $60\,\mathrm K$ hotter is $1.0\,(1+0.0039\cdot60)=1.234\,\Omega$ — why [[04-robotics/actuators-drives|10.5 §6]] folds a rising $R$ into its heat budget. A battery lead of $0.6\,\mathrm m$ of $1.0\,\mathrm{mm^2}$ copper is $1.68\times10^{-8}\cdot0.6/10^{-6}=10.1\,\mathrm{m\Omega}$: at the drive's $10\,\mathrm A$ it drops $0.10\,\mathrm V$ and warms by $1.0\,\mathrm W$.
> - **Non-example**: a diode. Its current grows exponentially with its voltage, $I=I_0\big(e^{eV/k_BT}-1\big)$ (OpenStax), so no single ratio $v/i$ describes it; ask for "its resistance" and the answer depends on the current you ask at. §6 uses it as a one-way valve instead.
> - **Why it matters**: $i^2R$ is where every loss on the cart comes from — winding, wires, switches — and $v=Ri$ is the element law in every equation of §3.

**Series and parallel.** Two elements are in *series* when the same current must pass through both; their voltages then add, so their resistances add. They are in *parallel* when they share both terminals; their currents then add at one voltage, so their conductances $1/R$ add (OpenStax):

$$R_{\text{series}}=R_1+R_2+\cdots,\qquad \frac{1}{R_{\text{parallel}}}=\frac{1}{R_1}+\frac{1}{R_2}+\cdots$$

because in series each resistor drops $iR_k$ of a shared $i$, and in parallel each carries $v/R_k$ at a shared $v$. The load cell's bridge (§9) is both at once. Each side is two $350\,\Omega$ gauges in series, $700\,\Omega$, and the two sides are in parallel across the $5.0\,\mathrm V$ excitation, $350\,\Omega$ in all — a parallel pair is always smaller than either member. The bridge draws $5.0/350=14.3\,\mathrm{mA}$ and turns $5.0^2/350=71\,\mathrm{mW}$ into heat, $17.9\,\mathrm{mW}$ in each gauge; that self-heating is one reason to prefer the higher of the common gauge resistances, $120$, $350$ and $1000\,\Omega$ (Micro-Measurements). In the H-bridge of §6 every current path runs through two switches in series, $2R_{\text{on}}=20\,\mathrm{m\Omega}$, and at the push's $2.0\,\mathrm A$ they waste $2.0^2\cdot0.020=0.08\,\mathrm W$, two percent of the winding's $4.0\,\mathrm W$.

### 3. Kirchhoff's laws, the divider and one nodal analysis

*In one sentence:* charge is conserved at every node and energy around every loop, and those two laws with §2's $v=Ri$ turn any resistor circuit into linear equations, whose first lesson is that a source can only be read faithfully by a load that draws almost nothing from it.

> **Kirchhoff's laws, defined.** **Kirchhoff's current law** (KCL) and **voltage law** (KVL) are *two conservation laws written for a circuit* — statements about the whole network, true whatever its elements are. Three defining conditions. **KCL**: at every node the currents leaving sum to zero, because charge is conserved and a node stores none (OpenStax's junction rule). **KVL**: around every closed loop the voltages sum to zero, because a coulomb carried once around the loop comes back with the energy it started with (OpenStax's loop rule). And the circuit must be **lumped**: small against the wavelength of its fastest signal, so that each wire carries one current and each node has one voltage. An electromagnetic wave at $20\,\mathrm{kHz}$ is $15\,\mathrm{km}$ long and the cart is well inside that, but KVL does fail where a changing magnetic flux threads a loop — the ground loop of §11.
>
> $$\sum_{\text{branches at a node}} i_k=0,\qquad \sum_{\text{elements around a loop}} v_k=0$$
>
> where each current is counted as leaving its node and each voltage in the direction the loop is walked, so a law is one equation per node or per loop.
> - **Example**: the H-bridge during an on-interval (§6). KVL around battery, Q1, winding and Q4 gives $24=v_{Q1}+v_{\text{winding}}+v_{Q4}$, so with $R_{\text{on}}$ neglected the winding sees the whole $24\,\mathrm V$. KCL at the battery terminal, averaged over a $50\,\mu\mathrm s$ period in which that terminal carries the winding's $2.0\,\mathrm A$ for $8.33\%$ of the time and nothing otherwise, gives the battery current, $0.167\,\mathrm A$.
> - **Non-example**: "less current comes out of the motor than goes in, because the motor uses some." KCL says the two are equal at every instant. What the motor keeps is energy, which shows up as a voltage — the joules each coulomb leaves behind (§1).
> - **Why it matters**: KCL at every node and $v=Ri$ in every branch are all of DC circuit analysis; nodal analysis, below, is nothing but KCL written once per unknown node.

**The divider and its load.** Two resistors in series across a source form the circuit that nearly every sensor reading passes through at least once.

> **Voltage divider, defined.** A **voltage divider** is *a series pair of resistors across a source, read across one of them*, and its law is a statement about what it outputs **when nothing draws current from its midpoint**. Three defining conditions. The two resistors carry the **same current**, because they are in series and the output takes none. The output is then the **fraction** $R_2/(R_1+R_2)$ of the source, whatever the source. And once a **load** $R_L$ draws current from the midpoint the first condition fails and the output falls — by exactly the factor that makes the loaded divider behave like its unloaded output voltage behind an **output resistance** $R_{\text{out}}=R_1\parallel R_2$.
>
> $$v_{\text{out}}=V\,\frac{R_2}{R_1+R_2},\qquad v_{\text{loaded}}=v_{\text{out}}\,\frac{R_L}{R_L+R_{\text{out}}},\qquad R_{\text{out}}=\frac{R_1R_2}{R_1+R_2}$$
>
> since KCL at the midpoint, $(V-v)/R_1=v/R_2+v/R_L$, solves to exactly this product — multiply both forms out over the common denominator $R_1R_2+R_1R_L+R_2R_L$ to check.
> - **Example**: P6's battery monitor, $100\,\mathrm{k\Omega}$ over $15\,\mathrm{k\Omega}$, puts the $24\,\mathrm V$ battery at $3.130\,\mathrm V$, inside the ADC's $4.096\,\mathrm V$ range (§10), at a cost of $0.209\,\mathrm{mA}$ — $5.0\,\mathrm{mW}$ — drawn from the battery for as long as it is connected.
> - **Non-example**: the same divider read by an input of $100\,\mathrm{k\Omega}$. Its output resistance is $13.0\,\mathrm{k\Omega}$, so the reading falls to $2.769\,\mathrm V$, $11.5\%$ low, and firmware that assumes the unloaded ratio reports a $21.2\,\mathrm V$ battery. "The ratio is set by the two resistors" is true only of an unloaded divider; an input of $10\,\mathrm{M\Omega}$ loses $0.13\%$.
> - **Why it matters**: every sensor is a source with an output resistance and every input is a load, and the fraction of the signal lost is about $R_{\text{out}}/R_L$ — which is why §8 reads the load cell through an amplifier whose inputs draw almost nothing.

**One nodal analysis: the load cell's bridge, loaded.** The bridge of §9 is two dividers side by side across one excitation, and its output is the difference between their midpoints. Connect a load $R_L$ across that output — a meter, or an amplifier's input — and the midpoints stop being independent: current flows from one to the other through $R_L$, so each divider loads the other. Nodal analysis handles this without cleverness. Take the bridge's bottom as the reference node, name the two unknown node voltages $v_A$ and $v_B$, and write KCL at each, every current leaving through a resistor as its node's voltage minus the far end's, over the resistance:

$$\frac{v_A-V_{ex}}{R_1}+\frac{v_A}{R_2}+\frac{v_A-v_B}{R_L}=0,\qquad \frac{v_B-V_{ex}}{R_3}+\frac{v_B}{R_4}+\frac{v_B-v_A}{R_L}=0$$

so the loaded bridge is two linear equations in two unknowns, a $2\times2$ system solved as in [[02-foundations/engineering-math|0.5 §4]]. During the push each gauge has changed by $x=\Delta R/R=4\times10^{-4}$, one diagonal pair stretched and the other compressed (§9). The listing solves the system for five loads and sets the result beside the divider rule above, with $R_{\text{out}}$ now the two halves' $R\parallel R$ in series.

```python
import numpy as np

# P6's load cell during the 10 N push, as a full bridge loaded by R_L across its output (nodal analysis)
Vex, Rb = 5.0, 350.0                          # excitation (V), each arm (ohm)
x = 2.0e-3*10.0/50.0                          # dR/R of each gauge at 10 N; rated 2.0 mV/V at 50 N
R1, R2 = Rb*(1 - x), Rb*(1 + x)               # left divider: top and bottom arms, node A between them
R3, R4 = Rb*(1 + x), Rb*(1 - x)               # right divider: top and bottom arms, node B between them

def bridge(RL):
    """(vA, vB) from KCL at A and B: the currents leaving each node through its resistors sum to zero."""
    G = np.array(((1/R1 + 1/R2 + 1/RL, -1/RL),
                  (-1/RL, 1/R3 + 1/R4 + 1/RL)))
    b = np.array((Vex/R1, Vex/R3))
    return np.linalg.solve(G, b)

v_open = Vex*(R2/(R1 + R2) - R4/(R3 + R4))    # the two unloaded dividers, subtracted
R_out = R1*R2/(R1 + R2) + R3*R4/(R3 + R4)     # R1||R2 in series with R3||R4
print(f"unloaded v_o = {1e3*v_open:.4f} mV, R_out = {R_out:.2f} ohm")
print("     R_L     vA (V)     vB (V)  v_o (mV)  lost (%)  divider rule (mV)")
for RL in (1e3, 1e4, 1e5, 1e6, 1e9):
    vA, vB = bridge(RL)
    lost = 100*(1 - (vA - vB)/v_open)
    print(f"{RL:8.0e} {vA:10.6f} {vB:10.6f} {1e3*(vA - vB):9.4f} {lost:9.3g} {1e3*v_open*RL/(RL + R_out):18.4f}")
```

| $R_L$ | $v_A$ (V) | $v_B$ (V) | $v_o$ (mV) | lost (%) | divider rule (mV) |
|---:|---:|---:|---:|---:|---:|
| $10^3\,\Omega$ | 2.500741 | 2.499259 | 1.4815 | 25.9 | 1.4815 |
| $10^4\,\Omega$ | 2.500966 | 2.499034 | 1.9324 | 3.38 | 1.9324 |
| $10^5\,\Omega$ | 2.500997 | 2.499003 | 1.9930 | 0.349 | 1.9930 |
| $10^6\,\Omega$ | 2.501000 | 2.499000 | 1.9993 | 0.035 | 1.9993 |
| $10^9\,\Omega$ | 2.501000 | 2.499000 | 2.0000 | 3.5e-05 | 2.0000 |

Unloaded, the bridge gives $2.0000\,\mathrm{mV}$ from an output resistance of $350.00\,\Omega$. Loaded, the nodal solution and the one-line rule agree to every printed digit, and that is the practical content of this subsection: seen from its output, the bridge *is* a $2.0\,\mathrm{mV}$ source behind $350\,\Omega$. A $10\,\mathrm{k\Omega}$ meter reads $3.4\%$ low and a $1\,\mathrm{k\Omega}$ load loses a quarter of the signal, while an input of $1\,\mathrm{G\Omega}$, the class of the amplifier inputs in §8, loses $3.5\times10^{-7}$ of it.

### 4. Capacitors and inductors: what they store, and what cannot jump

*In one sentence:* a capacitor's voltage and an inductor's current are stored energies, so neither can change in no time, and that one fact sets every time constant on the cart and every freewheeling path in its drive.

> **Capacitor and inductor, defined.** A **capacitor** and an **inductor** are *two-terminal elements that store energy* — a capacitor in the electric field between two conductors, an inductor in the magnetic field of a coil — each defined by a law that ties one of its variables to the rate of change of the other. Four defining conditions. In a capacitor **current follows the rate of change of voltage**, $i=C\,dv/dt$, with a constant capacitance $C$ in farads. In an inductor **voltage follows the rate of change of current**, $v=L\,di/dt$, with a constant inductance $L$ in henries, and the induced voltage opposes the change — Lenz's law, in OpenStax's $\varepsilon=-L\,dI/dt$. Each **stores** energy, $\tfrac12Cv^2$ and $\tfrac12Li^2$ (OpenStax), and an ideal one gives all of it back. And so each is **continuous** in its stored variable: a jump in a capacitor's voltage or an inductor's current would change a stored energy in zero time, which takes infinite power.
>
> $$i=C\,\frac{dv}{dt},\quad E_C=\tfrac12Cv^2;\qquad v=L\,\frac{di}{dt},\quad E_L=\tfrac12Li^2$$
>
> where $v$ and $i$ are the element's own voltage and current — so a capacitor passes no current at a steady voltage, an inductor drops no voltage at a steady current, and each resists only change.
> - **Example**: the filter capacitor at the push's $0.80\,\mathrm V$ stores $\tfrac12\cdot10^{-6}\cdot0.80^2=0.32\,\mu\mathrm J$; the winding at $2.0\,\mathrm A$ stores $\tfrac12\cdot10^{-3}\cdot2.0^2=2.0\,\mathrm{mJ}$, six thousand times more. Raising the winding's current by $0.092\,\mathrm A$ in $4.17\,\mu\mathrm s$ takes $L\,di/dt=10^{-3}\cdot0.092/(4.17\times10^{-6})=22\,\mathrm V$ — §6's ripple, seen from the inductor.
> - **Non-example**: "open the switch and the motor current stops." It cannot stop at once. Forcing $2.0\,\mathrm A$ to zero in $100\,\mathrm{ns}$ asks for $L\,di/dt=10^{-3}\cdot2.0/10^{-7}=20{,}000\,\mathrm V$, and that voltage appears across whatever broke the circuit — the switch — until something gives, usually the switch. §6 gives the current a path instead.
> - **Why it matters**: continuity is the initial condition of every transient on this page: a capacitor starts where it was, an inductor keeps its current for the first instant, and the circuit's time constant does the rest.

**A mechanical reading.** A reader who knows the mass–spring–damper already knows these elements. Read voltage as force and current as a velocity $u$, and an inductor is a mass — $v=L\,di/dt$ against $F=m\,du/dt$, storing $\tfrac12Li^2$ as a mass stores $\tfrac12mu^2$ — a resistor is a damper, and a capacitor is a spring whose compliance is $C$. The winding under a voltage step, $L\,di/dt+Ri=v$, is then a mass pushed through a damper, and its time constant $L/R=1.0\,\mathrm{ms}$ is the $m/b$ of a coasting mass. Continuity reads the same way: an inductor's current cannot jump for the reason a mass's velocity cannot, and stopping it dead takes an unbounded voltage as stopping a mass dead takes an unbounded force.

With one storage element and resistance the circuit is first order, the case [[02-foundations/engineering-math|0.5 §8]] solves. Charge the filter capacitor through $R_f$ from an input that steps to $V$: KVL gives $V=R_fi+v$, and $i=C_f\,dv/dt$, so

$$R_fC_f\,\frac{dv}{dt}+v=V\quad\Longrightarrow\quad v(t)=V\big(1-e^{-t/R_fC_f}\big)$$

because this is 0.5 §8's first-order equation with $a=-1/(R_fC_f)$, started from $v(0)=0$ as continuity demands. The winding under a voltage step is the same equation with the roles exchanged: $V=Ri+L\,di/dt$, so $i(t)=(V/R)\big(1-e^{-tR/L}\big)$, started from $i(0)=0$.

> **Time constant, defined.** The **time constant** $\tau$ is *a time*, a property of a first-order circuit — one storage element with resistance, driven by sources held constant — that says how fast it moves from one steady state to the next. Three defining conditions. The circuit is **first order**, so every voltage and current in it relaxes as one exponential. Each $\tau$ closes **$1-e^{-1}=63.2\%$ of the remaining gap** (OpenStax), whatever the gap. And the value is **$RC$ for a capacitor and $L/R$ for an inductor**, with $R$ the resistance the storage element sees.
>
> $$x(t)=x_\infty+\big(x(0)-x_\infty\big)\,e^{-t/\tau},\qquad \tau=RC\quad\text{or}\quad\tau=\frac{L}{R}$$
>
> where $x$ is any voltage or current in the circuit, $x(0)$ its value just after the change and $x_\infty$ its new steady value — so one number times every transient in the circuit, and both forms of $\tau$ are times, by §1's unit check.
> - **Example**: the anti-alias filter, $3.3\,\mathrm{k\Omega}\cdot1.0\,\mu\mathrm F=3.3\,\mathrm{ms}$. A step reaches $63\%$ at $3.3\,\mathrm{ms}$, $90\%$ at $\tau\ln10=7.6\,\mathrm{ms}$ and $99\%$ at $\tau\ln100=15.2\,\mathrm{ms}$. The winding, $1.0\,\mathrm{mH}/1.0\,\Omega=1.0\,\mathrm{ms}$, is the electrical time constant of [[04-robotics/actuators-drives|10.5 §5]].
> - **Non-example**: "the filter is done after one time constant." After $\tau$ it is still $37\%$ short, and it never finishes. Choose the tolerance first and the time follows: within $1\%$ takes $4.6\tau$, and within one count of an $800$-count step takes $\tau\ln800=6.7\tau$.
> - **Why it matters**: $\tau$ is the number to set against every other clock on the cart — the $50\,\mu\mathrm s$ PWM period against the winding's $1.0\,\mathrm{ms}$ (§6), the $5\,\mathrm{ms}$ control tick against the filter's $3.3\,\mathrm{ms}$ (§12).

### 5. The RC low-pass filter

The load cell's signal reaches the ADC with switching interference and tool vibration riding on it, which the sampler would misread; an RC filter removes the fast part, and this section says how much it removes and what it costs. Between the amplifier and the ADC sits $R_f$ in series and $C_f$ to ground, the output taken across $C_f$. §4 gave its step response; its response to a sinusoid follows from treating the capacitor as a resistance that depends on frequency. Drive it with $v=Ve^{j\omega t}$, the rotating phasor of [[02-foundations/engineering-math|0.5 §7]], and $i=C\,dv/dt=j\omega C\,v$, so the ratio $v/i$ is the complex **impedance** $Z_C=1/(j\omega C)$. The divider of §3 with $Z_C$ in the place of $R_2$ gives the filter's frequency response

$$H(j\omega)=\frac{Z_C}{R_f+Z_C}=\frac{1}{1+j\omega R_fC_f}$$

because the same current flows through $R_f$ and $C_f$ when the ADC draws none. It is [[02-foundations/engineering-math|0.5 §9]]'s transfer function $1/(1+sR_fC_f)$ at $s=j\omega$, a single pole at $s=-1/(R_fC_f)=-303\,\mathrm{s^{-1}}$ — the same one-pole low-pass as that section's example $1/(s+3)$, with the pole moved from $3$ to $303$.

> **Cutoff frequency, defined.** The **cutoff frequency** $f_c$ of a low-pass filter is *a frequency*, a property of the filter: the one at which its gain has fallen to $1/\sqrt2$ of its low-frequency value, $-3\,\mathrm{dB}$, where it passes half the power. Three defining conditions. It is defined for a **steady sinusoid**, after §4's transient has died away. For the first-order RC the gain and the phase then follow **one formula** at every frequency, so $f_c$ sets the whole response. And that formula holds only when the filter is **driven by a low output resistance and read by a high input resistance** — otherwise the source adds to $R_f$, the load becomes a divider of its own, and the cutoff moves (§3).
>
> $$f_c=\frac{1}{2\pi R_fC_f},\qquad \lvert H(f)\rvert=\frac{1}{\sqrt{1+(f/f_c)^2}},\qquad \angle H(f)=-\arctan\frac{f}{f_c}$$
>
> which is the magnitude and angle of $1/(1+j\,f/f_c)$, since $\omega R_fC_f=f/f_c$ — so at $f=f_c$ the gain is $1/\sqrt2=0.707$ and the phase $-45^\circ$.
> - **Example**: $3.3\,\mathrm{k\Omega}$ and $1.0\,\mu\mathrm F$ give $f_c=48.2\,\mathrm{Hz}$. The listing below evaluates it where P6 needs it: slow changes of the push pass whole, the ADC's Nyquist frequency of $100\,\mathrm{Hz}$ passes at $0.434$, and the PWM's $20\,\mathrm{kHz}$ at $0.00241$.
> - **Non-example**: "above the cutoff nothing gets through." Twice the cutoff still passes $1/\sqrt5\approx45\%$. A first-order filter falls only as $f_c/f$ well above $f_c$ — a factor of ten per decade, $-20\,\mathrm{dB}$ per decade — and the table's $0.0482$ at $1\,\mathrm{kHz}$ is $48.2/1000$ to three digits.
> - **Why it matters**: one number says what a filter removes, and through the phase what it costs in delay: well below $f_c$ the phase is about $-2\pi f\tau$, a pure delay of $\tau=3.3\,\mathrm{ms}$, added to every force reading the controller acts on.

```python
import math

Rf, Cf = 3.3e3, 1.0e-6                        # the anti-alias filter: ohm, farad
tau = Rf*Cf
fc = 1/(2*math.pi*tau)
print(f"tau = {1e3*tau:.2f} ms, f_c = {fc:.2f} Hz")
print("    f (Hz)      |H|  gain (dB)  phase (deg)")
for f in (1.0, 10.0, fc, 100.0, 1000.0, 20000.0):
    H = 1/(1 + 1j*2*math.pi*f*tau)            # the divider R_f, 1/(j w C_f) with complex impedances
    print(f"{f:10.2f} {abs(H):8.5f} {20*math.log10(abs(H)):10.3f} {math.degrees(math.atan2(H.imag, H.real)):12.2f}")
```

| $f$ (Hz) | $\lvert H\rvert$ | gain (dB) | phase (°) | what sits there on P6 |
|---:|---:|---:|---:|---|
| 1.00 | 0.99979 | −0.002 | −1.19 | a slow change of the push |
| 10.00 | 0.97917 | −0.183 | −11.71 | |
| 48.23 | 0.70711 | −3.010 | −45.00 | the cutoff |
| 100.00 | 0.43441 | −7.242 | −64.25 | the Nyquist frequency of the $200\,\mathrm{Hz}$ ADC |
| 1000.00 | 0.04817 | −26.344 | −87.24 | |
| 20000.00 | 0.00241 | −52.355 | −89.86 | the PWM |

Three readings of the table. The phase at $1\,\mathrm{Hz}$, $-1.19^\circ$, is $1.19/360$ of a second, $3.30\,\mathrm{ms}$ — exactly the delay $\tau$ the box predicts; at $10\,\mathrm{Hz}$ it is still $3.25\,\mathrm{ms}$. The $100\,\mathrm{Hz}$ row shows what one RC cannot do: content above the ADC's Nyquist frequency folds into the readings (§10), and a first-order filter low enough to stop it would delay the push by far more than a control tick; §12 measures that trade, and the sharper filters that ease it are [[02-foundations/signal-processing|6. Signal Processing §4]]'s subject. And sampled every $T$, the RC's step response shrinks the remaining gap by $\alpha=e^{-T/\tau}$ per sample, $e^{-5/3.3}=0.220$ at P6's $5\,\mathrm{ms}$: the exponential smoother that 6. §4 writes as $y[n]=\alpha\,y[n-1]+(1-\alpha)\,x[n]$ is this circuit, in code.

### 6. Switches: diodes, MOSFETs, PWM and the H-bridge

*In one sentence:* the drive never makes $2.0\,\mathrm V$ — it switches the full $24\,\mathrm V$ on and off twenty thousand times a second, the winding's inductance averages the pulses into a nearly steady current, and a diode or a switched-on transistor carries that current whenever a switch opens.

**The two switches.** A **diode** is a one-way valve for current (OpenStax; Toshiba). Forward, its current grows as $I_0(e^{eV/k_BT}-1)$, so at $300\,\mathrm K$ each tenfold rise in current costs only $(k_BT/e)\ln10=0.0259\times2.303=59.5\,\mathrm{mV}$ more voltage, with $k_B$ and $e$ the exact SI constants (NIST); over the currents a circuit uses, a conducting silicon diode therefore behaves as a nearly fixed drop, which this page takes as $V_F=0.7\,\mathrm V$, a course number. Reversed, it blocks. A **MOSFET** is a switch controlled by a voltage: a gate-to-source voltage above a threshold forms a conducting channel between drain and source, and the switch is on, with a small resistance $R_{DS(\text{on})}=V_{DS}/I_D$ that makers specify at a stated gate voltage (Toshiba) — $10\,\mathrm{m\Omega}$ here; without the gate voltage it is off. A power MOSFET also contains a diode between its source and drain, which its datasheet lists with its own current and forward voltage (Toshiba); in the bridge below each one points from the low rail toward the high one.

A switch wastes little in either state — on, $i^2R_{\text{on}}$ with a tiny $R_{\text{on}}$; off, no current at all — and that is the whole reason drives switch. The alternative, a transistor used as a variable resistor in series with the motor, would drop the unwanted $22\,\mathrm V$ at $2.0\,\mathrm A$ and burn $44\,\mathrm W$ to deliver the push's $4.0$.

> **PWM, defined.** **Pulse-width modulation** (PWM) is *a way of making an adjustable average voltage from a fixed supply by switching*, set by two numbers: the switching period $T$, or frequency $f=1/T$, and the **duty cycle** $D$, the fraction of each period the supply is connected. Three defining conditions. The load sees **two levels**, $V_s$ for $DT$ and $0$ for $(1-D)T$, in the scheme this page uses. The **average** is set by the duty alone, $\bar v=DV_s$. And the load must **filter** the pulses: the period must be short against the load's own time constant, $T\ll L/R$, so that the current follows the average and only ripples around it.
>
> $$\bar v=D\,V_s,\qquad \Delta i_{pp}\approx\frac{V_s\,D\,(1-D)}{L\,f}$$
>
> since during the on-time the inductance sees $V_s$ minus the average it is holding, $L\,di/dt\approx V_s-\bar v=(1-D)V_s$, for a time $DT$ — so the ripple depends on the supply, the duty, $L$ and $f$, and not on the load current or the back-EMF.
> - **Example**: the push. $\bar v=2.0\,\mathrm V$ needs $D=2.0/24=8.33\%$, $4.17\,\mu\mathrm s$ on in every $50\,\mu\mathrm s$. The current ripples by $24\cdot0.0833\cdot0.917/(10^{-3}\cdot20{,}000)=0.0917\,\mathrm A$ peak to peak, $4.6\%$ of $2.0\,\mathrm A$; at a stall that fraction is $(1-D)\,T/\tau_e$, the period over the winding's time constant.
> - **Non-example**: "a duty cycle sets a force" — the warning [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]] puts in its title. The duty sets an average *voltage*; the current, and so the force, follow from $\bar v=Ri+e$ (§7). The same $8.33\%$ that holds a $10\,\mathrm N$ push at rest, applied while the cart cruises at $0.5\,\mathrm{m/s}$ with $2.5\,\mathrm V$ of back-EMF, gives $i=(2.0-2.5)/1.0=-0.5\,\mathrm A$: the motor brakes the cart and charges the battery.
> - **Why it matters**: it is how an electric drive turns a battery into a controllable voltage while wasting almost nothing, and its frequency is a trade — the ripple falls as $1/f$ (§12), each switching edge costs a little energy so the switches' losses grow with $f$, and below about $20\,\mathrm{kHz}$ the winding sings at a pitch people hear, since normal hearing spans $20\,\mathrm{Hz}$ to $20\,\mathrm{kHz}$ (OpenStax).

**The H-bridge.** One switch can connect the motor to the supply; making it push *and* pull needs four.

> **H-bridge and freewheeling path, defined.** An **H-bridge** is *a four-switch circuit*: two legs across the supply, each a high-side and a low-side switch, with the load between the legs' midpoints as the bar of an H. It can put $+V_s$, $-V_s$ or $0$ across the load, and with an inductive load it must also give the load's current a **freewheeling path** — somewhere to go when a switch opens. Three defining conditions. **Diagonal pairs** drive: Q1 with Q4 puts $+V_s$ across the load, Q2 with Q3 puts $-V_s$. **Never both switches of one leg** conduct at once, because that shorts the supply through $2R_{\text{on}}$, so the controller leaves a brief *dead time* between turning one off and the other on. And **every switch has a diode across it**, pointing toward the positive rail, so that when a switch interrupts an inductive current the current carries on through the diode of the other switch in the same leg — or through that switch itself, turned on after the dead time, which is called synchronous freewheeling.
>
> $$v_{\text{load}}\in\{+V_s,\ 0,\ -V_s\},\qquad \text{while freewheeling:}\quad L\,\frac{di}{dt}=-\big(R\,i+e+v_{\text{path}}\big)$$
>
> where $e$ is the motor's back-EMF (§7) and $v_{\text{path}}$ the drop of the freewheeling path — $2iR_{\text{on}}=0.04\,\mathrm V$ through the two switched-on MOSFETs at $2.0\,\mathrm A$, about $V_F=0.7\,\mathrm V$ more when one of them conducts through its diode — so the current decays slowly through the path instead of being forced to zero.
> - **Example**: the push, drawn at the top of the page. On-time: Q1 and Q4 put $+24\,\mathrm V$ across the winding and the current comes from the battery. Off-time: Q1 opens, Q4 stays on and Q2 turns on after the dead time, so the winding's $2.0\,\mathrm A$ circulates through Q2 and Q4 with almost no voltage across it and falls by only $0.0917\,\mathrm A$ in the $45.8\,\mu\mathrm s$ before Q1 closes again, because that interval is $4.6\%$ of $\tau_e$. A shoot-through, by contrast — Q1 and Q2 on together — would put $24\,\mathrm V$ across $20\,\mathrm{m\Omega}$ and ask for $1200\,\mathrm A$.
> - **Non-example**: one transistor in series with the motor and no diode, the circuit a first attempt often uses. It can switch the motor on, but opening it at $2.0\,\mathrm A$ in $100\,\mathrm{ns}$ asks for $20{,}000\,\mathrm V$ (§4), and the transistor meets that voltage first.
> - **Why it matters**: the freewheeling path is what makes switching an inductor survivable, and the same diodes are the path by which a motor turned from outside drives current back toward the supply — the physics under the shorted-winding brake of [[04-robotics/actuators-drives|10.5 §7]].

Why a drive switches the freewheeling transistor on, rather than leaving the current to its diode, is a question of watts; the note below prices it.

> [!note]- Deeper · 더 깊이
> **Diode or switch in the freewheeling path.** If the off-time current runs through Q2's diode instead of through Q2 switched on, the winding sees $-0.7\,\mathrm V$ rather than $0$ for $91\%$ of each period. Holding $2.0\,\mathrm A$ then needs $DV_s-(1-D)V_F=Ri$, so $D=(2.0+0.7)/(24+0.7)=10.9\%$ instead of $8.33\%$, and the diode dissipates $V_Fi(1-D)=0.7\cdot2.0\cdot0.891=1.25\,\mathrm W$ against $i^2R_{\text{on}}(1-D)=0.037\,\mathrm W$ in a switched-on Q2 — which is why drives switch the freewheeling transistor on.

### 7. The DC motor as a circuit element

To command a force you have to know the current, voltage and duty it takes, and the motor's circuit equation is where they come from. Seen from its two terminals, the motor is §2's resistor, §4's inductor and a voltage source in series: the winding's $R$ and $L$, and the **back-EMF** $e=k_e\omega_m$ that the turning rotor induces in the winding, opposing the current that drives it forward. KVL around it gives its one electrical equation, and its torque is proportional to its current:

$$v=R\,i+L\,\frac{di}{dt}+k_e\,\omega_m,\qquad \tau_m=k_t\,i$$

because the terminal voltage has three places to go — the resistance, the changing current in the inductance and the back-EMF — while the magnets turn each ampere into $k_t$ newton-metres. [[04-robotics/actuators-drives|10.5 §1]] defines $k_t$ and $k_e$ and shows that in SI units they are the same number, since the electrical power the winding gives up against the back-EMF, $e\,i$, is the mechanical power the rotor makes, $\tau_m\omega_m$; this page uses that result. On P6 the belt pulley converts in both directions: a motor torque $\tau_m$ pushes the cart with $F=\tau_m/r_p$, and a cart speed $v_c$ turns the motor at $\omega_m=v_c/r_p$, so

$$F=\frac{k_t}{r_p}\,i=5.0\,\mathrm{\tfrac{N}{A}}\cdot i,\qquad e=\frac{k_e}{r_p}\,v_c=5.0\,\mathrm{\tfrac{V}{m/s}}\cdot v_c$$

since $0.10/0.020=5.0$ in both. Three operating points of the cart, each one line of these equations:

- **The push, at rest.** $\omega_m=0$ and the current is steady, so $v=Ri$: $10\,\mathrm N$ needs $2.0\,\mathrm A$ and $2.0\,\mathrm V$, and all $4.0\,\mathrm W$ become heat, because nothing moves. This is the Worked case.
- **Cruising at $0.5\,\mathrm{m/s}$** against the $2.0\,\mathrm N$ of rolling resistance. The motor turns at $25\,\mathrm{rad/s}$ ($239\,\mathrm{rpm}$) and its back-EMF is $2.5\,\mathrm V$; the force needs $0.40\,\mathrm A$, so $v=0.40+2.5=2.9\,\mathrm V$ and $D=12.1\%$. The power ledger closes: the drive delivers $2.9\cdot0.40=1.16\,\mathrm W$, of which $0.40^2\cdot1.0=0.16\,\mathrm W$ heats the winding and $e\,i=2.5\cdot0.40=1.0\,\mathrm W$ crosses the back-EMF — exactly the $F\,v_c=2.0\cdot0.5=1.0\,\mathrm W$ the cart spends against rolling resistance. $86\%$ of the electrical power becomes motion, and the battery supplies $0.121\cdot0.40=0.048\,\mathrm A$.
- **A stall on the full supply.** $24\,\mathrm V$ at $\omega_m=0$ would drive $24/1.0=24\,\mathrm A$, which the drive does not allow: it holds the current at its $10\,\mathrm A$ limit by lowering the duty ([[04-robotics/actuators-drives|10.5 §3]]), so the hardest the cart can push is $5.0\cdot10=50\,\mathrm N$. The winding cannot hold even that for long: [[04-robotics/actuators-drives|10.5 §6]]'s heat budget allows $3.16\,\mathrm A$ continuously, a push of $15.8\,\mathrm N$, so the $10\,\mathrm N$ push can last indefinitely and a $50\,\mathrm N$ one only for seconds — if the motor is cooled as 10.5 assumes.

Two more consequences of the same equation. The voltage the drive can spend on speed is what is left after $Ri$: on $24\,\mathrm V$ the unloaded motor tops out at $V_s/k_e=240\,\mathrm{rad/s}$, a cart speed of $4.8\,\mathrm{m/s}$, and 10.5 §3 draws the whole torque–speed line. And the inductance makes current slow to change: after a voltage step the current covers $63\%$ of the way to its new value in $\tau_e=1.0\,\mathrm{ms}$, which is why a drive closes a fast loop on current and the controller asks for current rather than for voltage ([[04-robotics/actuators-drives|10.5 §5]]). At $20\,\mathrm{kHz}$ that current loop sees the PWM as a smooth voltage, because the switching period is a twentieth of $\tau_e$.

### 8. Op-amps: two rules and three amplifiers

The load cell's signal is $2.0\,\mathrm{mV}$ and the ADC's step is $1.0\,\mathrm{mV}$ (§10), so the signal must be multiplied by hundreds before it is read. The part that does it is the operational amplifier, and three circuits built from it cover almost every sensor on a robot.

> **Ideal op-amp, defined.** An **operational amplifier** is *a differential amplifier with enormous gain*: its output voltage is a gain $A$ times the difference between its two inputs, and its inputs draw almost no current. The **ideal op-amp** is the model that sends $A$ to infinity, and its two rules are what that model implies **inside a negative-feedback circuit**. Three defining conditions. The output is $v_{\text{out}}=A(v_+-v_-)$ with $A$ very large — $10^5$ here, the order Toshiba's tutorial uses. The **inputs draw no current**. And **negative feedback** returns part of the output to the $-$ input, so the circuit settles where $v_+-v_-=v_{\text{out}}/A$, almost zero: the two inputs sit at almost the same voltage without being connected, which is called a **virtual short** (Toshiba) — as long as the output stays inside its supply range.
>
> $$v_{\text{out}}=A\,(v_+-v_-)\quad\Longrightarrow\quad v_+-v_-=\frac{v_{\text{out}}}{A}\;\approx\;0,\qquad i_+=i_-\approx0$$
>
> since a finite output divided by a huge gain leaves almost no input difference — the two rules, *no voltage between the inputs and no current into them*, with which every circuit below is solved by KCL at the $-$ input.
> - **Example**: a gain-$400$ amplifier putting out the push's $0.80\,\mathrm V$ needs only $0.80/10^5=8\,\mu\mathrm V$ between its op-amp's inputs. Against the $2.0\,\mathrm{mV}$ it amplifies that is $0.4\%$, the same $0.4\%$ as the gain error below: it is the price of $A$ being finite.
> - **Non-example**: an op-amp with no feedback. The bridge's $2.0\,\mathrm{mV}$ times $10^5$ asks for $200\,\mathrm V$, the output slams into its supply, and neither rule holds; used that way it is a comparator, a one-bit ADC. Nor is a virtual short a real one: no current flows between the inputs.
> - **Why it matters**: with the two rules, designing an amplifier is two lines of KCL, and its gain is set by a ratio of resistors, not by the ill-controlled $A$.

**Inverting amplifier.** Ground $v_+$; the virtual short puts $v_-$ at $0\,\mathrm V$ as well. KCL at $v_-$, with no current into the op-amp, says the current arriving through $R_{\text{in}}$ leaves through the feedback resistor $R_{\text{fb}}$: $v_{\text{in}}/R_{\text{in}}+v_{\text{out}}/R_{\text{fb}}=0$, so $v_{\text{out}}=-(R_{\text{fb}}/R_{\text{in}})\,v_{\text{in}}$. Its input resistance is $R_{\text{in}}$ — a load, in the sense of §3.

**Non-inverting amplifier.** Put $v_{\text{in}}$ on $v_+$ and feed $v_-$ from a divider across the output, $R_{\text{fb}}$ over $R_g$; the virtual short makes the divider's output equal $v_{\text{in}}$, $v_{\text{out}}R_g/(R_g+R_{\text{fb}})=v_{\text{in}}$, so

$$G=\frac{v_{\text{out}}}{v_{\text{in}}}=1+\frac{R_{\text{fb}}}{R_g},\qquad G_{\text{actual}}=\frac{G}{1+G/A}$$

and since $v_+$ draws no current, this amplifier hardly loads its source at all. The second form keeps $A$ finite: for $G=400$ it gives $398.4$, $0.40\%$ low — a gain error that calibration against a known load removes.

**The instrumentation amplifier, in one paragraph.** The bridge's two outputs sit at $2.501$ and $2.499\,\mathrm V$: the $2.0\,\mathrm{mV}$ worth reading rides on $2.5\,\mathrm V$ common to both. A non-inverting amplifier of gain $400$ on either output would try to reach $1000\,\mathrm V$. The instrumentation amplifier amplifies only the difference. Its first stage is two non-inverting amplifiers that share one gain resistor $R_G$ between their $-$ inputs: the virtual shorts copy $v_A$ and $v_B$ onto the two ends of $R_G$, the current $(v_A-v_B)/R_G$ must continue through both feedback resistors $R_{\text{fb}}$ because no op-amp input takes any of it, and so the two first-stage outputs differ by $(v_A-v_B)(1+2R_{\text{fb}}/R_G)$ while the common $2.5\,\mathrm V$ passes through at a gain of one. The second stage, a unity-gain difference amplifier, subtracts the two outputs and with them the common part. With $R_{\text{fb}}=20\,\mathrm{k\Omega}$, $G=400$ needs $R_G=2R_{\text{fb}}/(G-1)=100.25\,\Omega$; during the push the first stage outputs $2.900$ and $2.100\,\mathrm V$ and the second $0.800\,\mathrm V$. Both bridge wires land on op-amp inputs, which draw almost no current, so the bridge is not loaded (the $1\,\mathrm{G\Omega}$ row of §3's table). How completely the common $2.5\,\mathrm V$ is removed depends on how well the second stage's resistors match, the figure an instrumentation amplifier's datasheet calls its common-mode rejection.

### 9. The Wheatstone bridge and the strain-gauge load cell

A force sensor has to turn newtons into volts, and the strain gauge does it with a resistance change far too small to measure directly — the problem the bridge solves. A **strain gauge** is a thin metal-foil resistor bonded to a part that bends: stretch the part and the foil grows longer and thinner, so its resistance rises by §2's $R=\rho\ell/A_c$; compress it and the resistance falls. The fractional change is proportional to the strain $\varepsilon$, the fractional stretch, through a **gauge factor** $K$ that is nominally $2$ for foil gauges (Micro-Measurements):

$$\frac{\Delta R}{R}=K\,\varepsilon$$

so a gauge strained by $1000$ microstrain, $\varepsilon=10^{-3}$, changes by $0.2\%$. A **load cell** is a machined flexure carrying four such gauges, placed so that a force stretches two of them and compresses the other two. In P6's, the rated $50\,\mathrm N$ strains the gauges by $1000\,\mu\varepsilon$, so each $350\,\Omega$ gauge moves by $0.70\,\Omega$; the push's $10\,\mathrm N$ moves it by $0.14\,\Omega$, and one newton by $14\,\mathrm{m\Omega}$, four parts in a hundred thousand. Measuring that as a resistance would need an ohmmeter good to $4\times10^{-5}$. The bridge measures the change instead.

> **Wheatstone bridge, defined.** A **Wheatstone bridge** is *a four-resistor circuit* — two voltage dividers across one excitation, the output taken between their midpoints — that outputs **zero when balanced** and a voltage **proportional to small resistance changes** when not. Four defining conditions. Both dividers hang from the **same excitation** $V_{ex}$, so its value multiplies the output. The output is the **difference of two divider ratios**, zero when $R_2/R_1=R_4/R_3$. With arms that change by small fractions $\pm x$ the output is **linear in the change**: exactly $V_{ex}x$ for a full bridge whose four arms change in opposite pairs, and about $V_{ex}x/4$ with a single active arm, the quarter bridge — Micro-Measurements writes both as $V_{ex}K\varepsilon N/4$ for $N$ active arms. And it must be **read without loading**, since its output resistance is about one arm's $R$ (§3's table).
>
> $$v_o=V_{ex}\Big(\frac{R_2}{R_1+R_2}-\frac{R_4}{R_3+R_4}\Big)=V_{ex}\,\frac{N}{4}\,K\,\varepsilon\quad(N=4,\ \text{full bridge})$$
>
> because with $R_1=R_4=R(1-x)$ and $R_2=R_3=R(1+x)$ the first ratio is $(1+x)/2$ and the second $(1-x)/2$, so $v_o=V_{ex}x=V_{ex}K\varepsilon$ with nothing neglected; a quarter bridge's $V_{ex}x/(2(2+x))$ is the same law only for small $x$.
> - **Example**: P6's load cell during the push: $x=K\varepsilon=4\times10^{-4}$, so $v_o=5.0\cdot4\times10^{-4}=2.0\,\mathrm{mV}$, riding on $2.5\,\mathrm V$ at both output terminals.
> - **Non-example**: a single active gauge in a quarter bridge, on a part that warms. The foil's resistance also changes with temperature, and one warm gauge reads as strain. In the full bridge a change common to all four arms — every arm times $(1+\delta)$ — leaves both divider ratios, and so the output, exactly unchanged: four gauges side by side on one flexure cancel the warming they share, one argument for building load cells as full bridges.
> - **Why it matters**: the bridge turns a resistance change too small to measure into a voltage that starts from zero, so an amplifier can multiply the change without multiplying the $350\,\Omega$ it rides on.

**Rated output in mV/V.** Load-cell makers quote sensitivity as the output per volt of excitation at the rated load (Massload), so P6's $2.0\,\mathrm{mV/V}$ means $2.0\,\mathrm{mV}$ for each volt of excitation at $50\,\mathrm N$:

$$v_o=S\,V_{ex}\,\frac{F}{F_{\text{rated}}}=2.0\,\mathrm{\tfrac{mV}{V}}\times5.0\,\mathrm V\times\frac{F}{50\,\mathrm N},\qquad \text{so } 200\,\mu\mathrm V\text{ per newton}$$

because the bridge is linear in the load. That is what a newton is worth here: $200\,\mu\mathrm V$, with $2.0\,\mathrm{mV}$ for the push and $10\,\mathrm{mV}$ at the rating. And since the output is proportional to the excitation, any drift in $V_{ex}$ is a drift in every reading; a design that derives the ADC's reference from the same excitation cancels it, and is called ratiometric.

**Why the bridge needs an amplifier.** Two reasons, one for each thing §8's instrumentation amplifier does. The signal is small: at the ADC's $1.0\,\mathrm{mV}$ per count (§10) the whole $50\,\mathrm N$ range would be $10$ counts and a newton a fifth of one. And the signal is a *difference* riding on $2.5\,\mathrm V$, while the ADC measures against ground, so it must be handed $v_A-v_B$ and not either one. The gain of $400$ makes a newton $80\,\mathrm{mV}$, or $80$ counts, and hands the ADC the difference alone. Raising the excitation raises the signal too — $10\,\mathrm V$ would double it — but the gauges' heat goes as $V_{ex}^2$, $17.9\,\mathrm{mW}$ per gauge at $5\,\mathrm V$ and $71\,\mathrm{mW}$ at $10\,\mathrm V$, and a warm gauge drifts. The same bridge reads a piezoresistive tactile element in [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing §2.5]].

### 10. From analog to digital: the ADC

The controller runs on numbers. An ADC turns a voltage into one, $200$ times a second on P6, and the conversion loses two things: values between two codes, and everything that happens between two samples.

> **ADC resolution, defined.** The **resolution** of an analog-to-digital converter is *a voltage*, the step one count stands for — its **least significant bit** (LSB) — and a property of the converter and its reference, not of the signal. Four defining conditions. An $n$-bit converter has **$2^n$ codes**, $0$ to $2^n-1$. They divide an input range from $0$ to the **reference** $V_{\text{ref}}$ into equal steps of one LSB. The ideal converter reports the **nearest code**, so its rounding error stays within $\pm\tfrac12$ LSB, and it **clips**: an input below $0$ reads $0$ and an input beyond the top code reads the top code. And it **samples**: each code is the input at one instant, one every $1/f_s$.
>
> $$\text{LSB}=\frac{V_{\text{ref}}}{2^n},\qquad \text{code}=\min\Big(\max\big(\operatorname{round}(v/\text{LSB}),\,0\big),\,2^n-1\Big),\qquad \lvert e_q\rvert\le\tfrac12\,\text{LSB}$$
>
> where $v$ is the input voltage — so an input of exactly $k$ LSB reads $k$, and every other input inside the range is off by less than half a step.
> - **Example**: P6's $12$ bits over $4.096\,\mathrm V$ give $4.096/4096=1.000\,\mathrm{mV}$ per count; the push's $0.80\,\mathrm V$ reads $800$, and the unamplified bridge's $2.0\,\mathrm{mV}$ would read $2$.
> - **Non-example**: "a 12-bit converter measures force to one part in 4096." Only a signal that fills the range does. Without the amplifier the $50\,\mathrm N$ range spans $10$ counts, $5\,\mathrm N$ each; and more bits alone do not rescue it — $16$ bits on the same reference is $62.5\,\mu\mathrm V$ per count, and an unamplified newton is still only $3.2$ counts.
> - **Why it matters**: the LSB, turned into the measured unit, is the resolution of the whole chain — $1\,\mathrm{mV}$ over $80\,\mathrm{mV/N}$ is $12.5\,\mathrm{mN}$ per count here — and the rounding adds up to $\pm6.25\,\mathrm{mN}$, or $\text{LSB}/\sqrt{12}=3.6\,\mathrm{mN}$ RMS when it behaves as noise. When it does is the question of [[04-robotics/sensor-models|3.2 Sensor Models & Noise §4]], and the six decibels of signal-to-noise per bit are [[02-foundations/signal-processing|6. Signal Processing §2]]'s.

**Choosing the gain.** From newtons to counts the chain is three multiplications — $200\,\mu\mathrm V/\mathrm N$ from the bridge, $G$ from the amplifier, $1/\text{LSB}$ from the ADC — and the gain is the only free one. Too little and a newton is a fraction of a count; too much and the ADC clips before the load cell's rating. The listing tabulates both ends.

```python
S, F_rated, Vex = 2.0e-3, 50.0, 5.0           # rated output (V per V), rated force (N), excitation (V)
nbits, Vref = 12, 4.096                       # the ADC: bits, reference (V)
LSB = Vref/2**nbits                           # volts per count

def code(v):
    """An ideal ADC: the nearest code, clipped to 0 ... 2**nbits - 1."""
    return min(max(round(v/LSB), 0), 2**nbits - 1)

print(f"LSB = {1e3*LSB:.3f} mV")
print("    G  at 10 N (V)  code at 10 N  counts/N  mN/count  clips at (N)")
for G in (1, 10, 100, 200, 400, 409, 500, 1000):
    per_N = G*S*Vex/F_rated                   # volts at the ADC per newton
    print(f"{G:5d} {10*per_N:12.4f} {code(10*per_N):13d} {per_N/LSB:9.2f} {1e3*LSB/per_N:9.2f} {(2**nbits - 1)*LSB/per_N:13.2f}")
```

| $G$ | at 10 N (V) | code at 10 N | counts/N | mN/count | clips at (N) |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.0020 | 2 | 0.20 | 5000.00 | 20475.00 |
| 10 | 0.0200 | 20 | 2.00 | 500.00 | 2047.50 |
| 100 | 0.2000 | 200 | 20.00 | 50.00 | 204.75 |
| 200 | 0.4000 | 400 | 40.00 | 25.00 | 102.37 |
| 400 | 0.8000 | 800 | 80.00 | 12.50 | 51.19 |
| 409 | 0.8180 | 818 | 81.80 | 12.22 | 50.06 |
| 500 | 1.0000 | 1000 | 100.00 | 10.00 | 40.95 |
| 1000 | 2.0000 | 2000 | 200.00 | 5.00 | 20.47 |

The window is $G\le409$, the largest gain that keeps the rated $50\,\mathrm N$ below the top code of $4095$. P6's $G=400$ sits just inside it, at $80$ counts per newton and $12.5\,\mathrm{mN}$ per count, with the ADC clipping at $51.2\,\mathrm N$ — just above both the load cell's rating and the drive's $50\,\mathrm N$ maximum push (§7). $G=500$ reads finer, $10\,\mathrm{mN}$ per count, and goes blind at $40.95\,\mathrm N$, a push the motor can still make. At $G=1$ the push is two counts.

**What sampling folds.** The ADC samples at P6's $200\,\mathrm{Hz}$, so its Nyquist frequency is $100\,\mathrm{Hz}$, and content above that does not vanish — it reappears at a lower frequency, $f_{\text{alias}}=\lvert f-kf_s\rvert$ with $k$ the integer nearest to $f/f_s$, which [[02-foundations/signal-processing|6. Signal Processing §2]] derives. On P6 this is not abstract. The PWM's $20\,\mathrm{kHz}$ is exactly $100$ times $200\,\mathrm{Hz}$, so switching interference on the signal line aliases to $0\,\mathrm{Hz}$: a constant offset in the force reading, a phantom push. If the PWM clock drifts to $20.01\,\mathrm{kHz}$, the phantom becomes a $10\,\mathrm{Hz}$ wobble, in the band where contact happens. And a tool that rings at $170\,\mathrm{Hz}$ when it touches the panel is read as a $30\,\mathrm{Hz}$ oscillation, the example 6. §2 draws. No processing after the sampler can undo a fold, because the true and the folded tone produce identical samples; only a filter before it can, which is what the RC of §5 is for. It cuts $20\,\mathrm{kHz}$ to $0.24\%$ and $170\,\mathrm{Hz}$ to $27\%$, and §12 measures what that costs.

**The encoder needs no ADC.** P6's encoder is already digital: two square-wave channels a quarter-cycle apart, whose edges a hardware counter adds up with their direction. Its resolution is geometric, $1/2048\,\mathrm m=0.488\,\mathrm{mm}$ per count, and at $0.5\,\mathrm{m/s}$ it delivers $1024$ counts a second. Its quantization is [[04-robotics/sensor-models|3.2 §4]]'s subject; its electrical weakness is §11's — a noise spike on a channel is a count that never averages away.

### Worked case · 대상으로 한 번 끝까지

The cart has driven its tool against the panel and holds it there with $F=10\,\mathrm N$. Nothing moves, so the motor has no back-EMF. Follow that one number out through the power path and back in through the sensing path; every step is a law from §1–§10 with the frozen numbers.

**Step 1 — force to current (§7).** The belt turns the push into a motor torque $\tau_m=Fr_p=10\cdot0.020=0.20\,\mathrm{N{\cdot}m}$, and torque is current times the torque constant, so

$$i=\frac{F\,r_p}{k_t}=\frac{10\cdot0.020}{0.10}=2.0\,\mathrm A$$

because a lossless belt passes the torque through unchanged.

**Step 2 — current to voltage (§2, §7).** At rest $e=0$, and a steady current drops nothing across $L$, so the winding needs only its resistive drop, $v=Ri=1.0\cdot2.0=2.0\,\mathrm V$.

**Step 3 — voltage to duty (§6).** $D=v/V_s=2.0/24=0.0833$: Q1 and Q4 conduct for $4.17\,\mu\mathrm s$ of every $50\,\mu\mathrm s$, and for the other $45.8\,\mu\mathrm s$ the current freewheels through Q2 and Q4.

**Step 4 — ripple and battery current (§3, §4, §6).** The current ripples by

$$\Delta i_{pp}=\frac{V_sD(1-D)}{Lf}=\frac{24\cdot0.0833\cdot0.917}{10^{-3}\cdot20{,}000}=0.0917\,\mathrm A$$

since the $50\,\mu\mathrm s$ period is a twentieth of $\tau_e=1.0\,\mathrm{ms}$ — $4.6\%$ of $2.0\,\mathrm A$, between $1.954$ and $2.046\,\mathrm A$ (the inset). The battery supplies current only during the on-time, $2.0\cdot0.0833=0.167\,\mathrm A$ on average, and $24\cdot0.167=4.0\,\mathrm W$ is exactly the winding's $i^2R=4.0\,\mathrm W$: the push does no work, so every watt is heat (the switches' $0.08\,\mathrm W$ left aside). At that rate the $120\,\mathrm{Wh}$ battery holds the push for $30\,\mathrm h$.

**Step 5 — force to bridge output (§9).** $v_o=SV_{ex}F/F_{\text{rated}}=2.0\,\mathrm{mV/V}\cdot5.0\,\mathrm V\cdot10/50=2.0\,\mathrm{mV}$, $200\,\mu\mathrm V$ per newton; each gauge has moved by $0.14\,\Omega$ of its $350$.

**Step 6 — the amplifier (§8).** $G\,v_o=400\cdot2.0\,\mathrm{mV}=0.80\,\mathrm V$, with the $2.5\,\mathrm V$ common to both bridge outputs rejected and the bridge unloaded.

**Step 7 — the filter (§4, §5).** A steady voltage passes an RC low-pass unchanged, $\lvert H(0)\rvert=1$, so $0.80\,\mathrm V$ reaches the ADC once the filter has settled — $90\%$ of the way within $7.6\,\mathrm{ms}$ of the push starting — while the PWM's $20\,\mathrm{kHz}$ is cut to $0.24\%$.

**Step 8 — the ADC (§10).** $0.80\,\mathrm V/1.000\,\mathrm{mV}=800$ counts; the controller divides by $80$ counts per newton and reads $10.0\,\mathrm N$, give or take $6.25\,\mathrm{mN}$ of rounding.

Two estimates of one force now sit in the controller: $800$ counts say $10.0\,\mathrm N$, and the current it commanded says $k_ti/r_p=10\,\mathrm N$. They agree only because this page's belt is lossless. [[04-robotics/actuators-drives|10.5 §7]] shows how far a current-based force estimate drifts once friction and the rotor's inertia sit in the path, and that is why the cart carries a load cell: to measure what the current cannot. The problem set repeats the loop with the cart cruising instead of pushing, and with a different ADC.

### 11. Grounding, noise and safety

*In one sentence:* a voltage is only ever measured between two points and a wire is a resistor, so a motor current that shares a wire with a sensor becomes a phantom force — and the one safety function that must not depend on any wiring or software working is the stop, which has to cut power rather than ask for it.

**Ground is a choice of reference.** Every voltage on this page is a difference (§1), and "ground" names the node the others are measured from — on P6, the battery's negative terminal. The trouble is that ground is not one point but a network of wires, and §2 says each of them is a resistor.

**Shared returns make phantom forces.** Suppose the motor's return current and the amplifier's ground share $0.6\,\mathrm m$ of §2's $1.0\,\mathrm{mm^2}$ lead, $10.1\,\mathrm{m\Omega}$, on their way to the battery. During the push the motor's $2.0\,\mathrm A$ puts $2.0\cdot0.0101=20\,\mathrm{mV}$ across that shared stretch, so the amplifier's "0 V" sits $20\,\mathrm{mV}$ away from the ADC's. The ADC reads the amplifier's output plus that difference: $20$ counts, a phantom $0.25\,\mathrm N$ that appears only while the motor pushes, grows with its current, and passes straight through the RC filter, because it is not noise but a steady voltage. The fix is wiring, not filtering: a **star ground**, in which the motor current returns to the battery on its own wire and the sensitive grounds meet at one point that no large current crosses.

**Loops pick up flux.** When two boards are joined by two ground paths — a cable's ground wire and a metal frame, say — the paths form a loop. A changing magnetic flux through it — such as the field of the H-bridge's supply leads, whose current jumps between $0$ and $2.0\,\mathrm A$ twenty thousand times a second while the motor leads carry only the $0.09\,\mathrm A$ ripple — induces a voltage around the loop, the one place §3's KVL fails, and that voltage drives a current round the loop and a drop along each of its wires. The remedies are geometric: one ground path between any two boards, each pair of supply and motor leads twisted together so that their opposite currents' fields cancel, and small loop areas.

**Edges couple through stray capacitance.** The H-bridge's switching midpoint jumps by $24\,\mathrm V$ at every edge. Through a stray capacitance of only $1\,\mathrm{pF}$ to a nearby signal wire, an edge lasting $50\,\mathrm{ns}$ drives $i=C\,dv/dt=10^{-12}\cdot24/(50\times10^{-9})=0.48\,\mathrm{mA}$ into it (§4, with course numbers for both) — brief, but through the bridge's $350\,\Omega$ a spike of about $0.17\,\mathrm V$. What couples equally into both bridge wires is common to the pair, and the instrumentation amplifier rejects it (§8); a braided shield around the load-cell cable, grounded at one end, carries the rest past the signal, and the RC removes what is left before the ADC samples (§12). On an encoder line the same spike is worse, because the counter takes it as an edge.

**Current limit and fuse are different protections.** The drive's $10\,\mathrm A$ limit is a control action — electronics that measure the current and lower the duty — and it protects the motor only while those electronics work. A fuse is the physical last resort for the fault no electronics handle, a short circuit, a low-resistance path across the source (OpenStax). Across the battery's own $0.050\,\Omega$, a dead short draws $24/0.050=480\,\mathrm A$ and heats the battery at $480^2\cdot0.050=11.5\,\mathrm{kW}$. A fuse opens the circuit when the current is excessive (OpenStax); P6's $15\,\mathrm A$ sits above the highest current normal operation draws, the drive's $10\,\mathrm A$, and the lead it protects must carry more than the fuse's rating without overheating.

**An emergency stop cuts power; it does not send a message.** A stop request in software needs the button's input, the network, the controller's code and the drive's firmware all to work at the moment something is going wrong, and [[04-robotics/robot-systems-deployment|10. Robot Systems §7]] shows how a silent node leaves the last command live. A hardware emergency stop needs none of them. It is a chain of normally closed contacts in series with the coil of a contactor in the drive's supply lead: pressing any button opens the chain, the contactor drops out, and the H-bridge loses its supply. Because the contacts are normally closed, a broken wire stops the machine too, and makers add direct opening action, a rigid link that forces the contacts apart even if they have welded (IDEC). On P6 what follows is §4 and §6: the $2.0\,\mathrm{mJ}$ stored in the winding drains through the bridge's diodes instead of arcing across the opening contact, the cart coasts, and mechanics — or a drive that shorts the windings to brake ([[04-robotics/actuators-drives|10.5 §7]]) — brings it to rest. Where the emergency stop sits among the other safety functions is [[04-robotics/hri-safety|11. HRI & Safety §6]].

### 12. The lab: PWM ripple, and the anti-alias trade

Two loops, each with a sweep. Both step their circuit exactly rather than with a small-step integrator: across an interval in which the input is held constant, a first-order circuit follows §4's exponential exactly, so the update $x\leftarrow x_\infty+(x-x_\infty)e^{-\Delta t/\tau}$ has no step-size error. [[02-foundations/lab-kernel|0.7 Lab Kernel]], next in the track, names the approximate integrators the other labs use.

**Part A — the winding under PWM.** The push at rest: the winding driven at the Worked case's duty from a standing start, one switching period at a time, for PWM frequencies from $0.5$ to $50\,\mathrm{kHz}$. The listing reports the last period's current extremes, its ripple beside §6's small-ripple formula, and its time-averaged current.

```python
import math

# Part A: the winding under PWM during the push (at rest, no back-EMF), stepped exactly interval by interval
Vs, R, L = 24.0, 1.0, 1.0e-3                   # supply (V); winding (ohm, H): 10.5's frozen drive
tau_e = L/R                                    # electrical time constant (s)
D = 2.0*R/Vs                                   # the push's duty: D*Vs = R*i for i = 2.0 A

def settle(i, v, dt):
    """Exact RL current after a voltage v is held for dt: it relaxes toward v/R with time constant L/R."""
    return v/R + (i - v/R)*math.exp(-dt/tau_e)

def mean_over(i, v, dt):
    """Time average of that same exact current over the interval."""
    return v/R + (i - v/R)*tau_e*(1 - math.exp(-dt/tau_e))/dt

def pwm_run(f, t_end=0.020):
    """Start from rest; return the last period's i_min, i_max and mean, and when the mean first passed 90 %."""
    T, i, t, t90 = 1/f, 0.0, 0.0, None
    while t < t_end - 1e-12:
        i_min = i
        m_on = mean_over(i, Vs, D*T)
        i = settle(i, Vs, D*T)                 # Q1 and Q4 on: +Vs across the winding
        i_max = i
        m_off = mean_over(i, 0.0, (1 - D)*T)
        i = settle(i, 0.0, (1 - D)*T)          # Q1 off: the current freewheels through Q2 and Q4
        t += T
        mean = D*m_on + (1 - D)*m_off
        if t90 is None and mean >= 0.9*D*Vs/R:
            t90 = t
    return i_min, i_max, mean, t90

print("f_PWM (kHz)  on (us)  i_min (A)  i_max (A)  ripple (A)  Vs*D*(1-D)/(L*f) (A)  mean (A)  hearing band")
for f in (500, 1e3, 2e3, 5e3, 10e3, 20e3, 50e3):
    i_min, i_max, mean, t90 = pwm_run(f)
    band = "inside" if f < 20e3 else ("at the edge" if f == 20e3 else "above")
    print(f"{f/1e3:10.1f} {1e6*D/f:8.2f} {i_min:10.4f} {i_max:10.4f} {i_max - i_min:11.4f}"
          f" {Vs*D*(1 - D)/(L*f):21.4f} {mean:9.4f}  {band}")
print(f"at 20 kHz the mean current passes 90 % of 2.0 A at {1e3*pwm_run(20e3)[3]:.2f} ms; "
      f"2.303 L/R = {1e3*2.303*tau_e:.2f} ms")
```

| $f_{\text{PWM}}$ (kHz) | on (µs) | $i_{\min}$ (A) | $i_{\max}$ (A) | ripple (A) | $V_sD(1-D)/(Lf)$ (A) | mean (A) | against the $20\,\mathrm{Hz}$–$20\,\mathrm{kHz}$ of hearing |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.5 | 166.67 | 0.6813 | 4.2611 | 3.5799 | 3.6667 | 2.0000 | inside |
| 1.0 | 83.33 | 1.2138 | 3.0357 | 1.8219 | 1.8333 | 2.0000 | inside |
| 2.0 | 41.67 | 1.5741 | 2.4893 | 0.9152 | 0.9167 | 2.0000 | inside |
| 5.0 | 16.67 | 1.8218 | 2.1884 | 0.3666 | 0.3667 | 2.0000 | inside |
| 10.0 | 8.33 | 1.9096 | 2.0929 | 0.1833 | 0.1833 | 2.0000 | inside |
| 20.0 | 4.17 | 1.9545 | 2.0462 | 0.0917 | 0.0917 | 2.0000 | at the edge |
| 50.0 | 1.67 | 1.9817 | 2.0184 | 0.0367 | 0.0367 | 2.0000 | above |

At $20\,\mathrm{kHz}$ the mean current passes $90\%$ of $2.0\,\mathrm A$ at $2.35\,\mathrm{ms}$, against $2.303\,L/R=2.30\,\mathrm{ms}$ for a smooth voltage step. Three readings:

- **The duty sets the mean exactly, and the frequency sets only the ripple.** Every row averages $2.0000\,\mathrm A$, because in periodic steady state the inductor's voltage averages to zero, leaving $R\,\bar i=DV_s$ at any frequency.
- **The ripple halves each time the frequency doubles**, and the small-ripple formula is good to three digits once the period is short against $\tau_e$. At $0.5\,\mathrm{kHz}$, where the period is twice $\tau_e$, the current swings from $0.68$ to $4.26\,\mathrm A$ — a push that shakes the cart at $500\,\mathrm{Hz}$ and a winding that hums — and the formula overstates the ripple by $2.4\%$.
- **The choice of $20\,\mathrm{kHz}$ is where two costs meet**: a ripple of $4.6\%$, and a fundamental at the top of the band OpenStax gives for human hearing. Going higher shrinks the ripple further but multiplies the switching edges, each of which costs the switches a little energy (§6). The start-up time barely moves with frequency: it is the winding's, not the drive's.

**Part B — what the ADC reads.** The sensing chain during the push, with two unwanted signals on the line into the ADC: $\pm10\,\mathrm{mV}$ of $20\,\mathrm{kHz}$ switching pickup, and a $170\,\mathrm{Hz}$ ring of the tool worth $\pm0.5\,\mathrm N$ — both course numbers, sized to make their effects visible. The RC filter is stepped exactly every $2.5\,\mu\mathrm s$, the ADC samples every $5\,\mathrm{ms}$, and the sweep changes $R_f$ with $C_f=1.0\,\mu\mathrm F$ held. It reports the filter's gain at the two unwanted frequencies, the peak-to-peak wobble and the average offset of the readings once settled, and the first reading of at least $9\,\mathrm N$ after the push begins.

```python
# Part B: what the ADC reads during the push, with and without the anti-alias filter
LSB = 4.096/2**12                              # volts per count
per_N = 400*2.0e-3*5.0/50.0                    # volts at the ADC per newton (G = 400)
f_pwm, f_s, f_ring = 20e3, 200.0, 170.0        # switching, sampling and tool-ring frequencies (Hz)
n_per = 20                                     # simulation steps per PWM period
dt = 1/(f_pwm*n_per)                           # 2.5 us
n_smp = round(1/(f_s*dt))                      # steps between two ADC samples
a_pwm, a_ring = 0.010, 0.5                     # +-10 mV of switching pickup (V), +-0.5 N of ring (N)

def adc(v):
    return min(max(round(v/LSB), 0), 2**12 - 1)

def readings(Rf, Cf=1.0e-6, t_end=0.160):
    """Push from just after the first sample; RC stepped exactly; one reading in newtons every 5 ms."""
    decay = math.exp(-dt/(Rf*Cf)) if Rf > 0 else 0.0
    y, out = 0.0, []
    for k in range(round(t_end/dt)):
        push = 10*per_N if k > 0 else 0.0
        pickup = a_pwm if k % n_per < n_per//2 else -a_pwm
        ring = a_ring*per_N*math.sin(2*math.pi*f_ring*k*dt)
        x = push + pickup + ring
        y = x + (y - x)*decay                  # exact RC update for an input held over dt
        if k % n_smp == 0:
            out.append(adc(y)*LSB/per_N)
    return out

print("  R_f (ohm)  f_c (Hz)  |H| at 170 Hz  |H| at 20 kHz  wobble (N p-p)  offset (mN)  first >= 9 N (ms)")
for Rf in (0.0, 100.0, 330.0, 1000.0, 3300.0, 10000.0):
    out = readings(Rf)
    late = out[12:]                            # 60 to 155 ms: 20 readings, three whole periods of 30 Hz
    first = next(n for n, F in enumerate(out) if F >= 9.0)*1e3/f_s
    w = 2*math.pi*Rf*1e-6
    fc = 1/w if Rf > 0 else math.inf
    print(f"{Rf:11.0f} {fc:9.1f} {1/math.hypot(1, w*f_ring):14.4f} {1/math.hypot(1, w*f_pwm):14.5f}"
          f" {max(late) - min(late):15.3f} {1e3*(sum(late)/len(late) - 10):12.1f} {first:18.1f}")
```

| $R_f$ (Ω) | $f_c$ (Hz) | $\lvert H\rvert$ at 170 Hz | $\lvert H\rvert$ at 20 kHz | wobble (N p-p) | offset (mN) | first ≥ 9 N (ms) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 (no filter) | ∞ | 1.0000 | 1.00000 | 1.000 | 125.0 | 5.0 |
| 100 | 1591.5 | 0.9943 | 0.07933 | 1.000 | −12.5 | 5.0 |
| 330 | 482.3 | 0.9431 | 0.02411 | 0.937 | −2.5 | 5.0 |
| 1000 | 159.2 | 0.6834 | 0.00796 | 0.675 | −0.6 | 5.0 |
| 3300 | 48.2 | 0.2729 | 0.00241 | 0.275 | −0.6 | 10.0 |
| 10000 | 15.9 | 0.0932 | 0.00080 | 0.113 | −4.4 | 25.0 |

Four readings:

- **Without a filter the PWM becomes a force.** The ADC samples at the same point of every switching period, so the $+10\,\mathrm{mV}$ it happens to catch reads as a steady $+125\,\mathrm{mN}$ — ten counts of phantom push that averaging cannot remove, because it does not vary. Any of the filters removes it to within a count; what remains in the offset column is rounding, and in the last row the filter's own settling tail.
- **The ring is subtler.** The tool's $170\,\mathrm{Hz}$ reaches the readings as a $30\,\mathrm{Hz}$ wobble of $1.0\,\mathrm N$ peak to peak — a vibration the controller would chase — and only a cutoff well below $170\,\mathrm{Hz}$ shrinks it: $0.675\,\mathrm N$ at $159\,\mathrm{Hz}$, $0.275$ at P6's $48\,\mathrm{Hz}$, $0.113$ at $16\,\mathrm{Hz}$, each within two counts of the unfiltered $1.0\,\mathrm N$ times that row's $\lvert H\rvert$ at $170\,\mathrm{Hz}$.
- **Every cut costs time.** The first reading of the push arrives one tick after it starts for every cutoff down to $159\,\mathrm{Hz}$; P6's filter costs one more tick, $10\,\mathrm{ms}$, and the $16\,\mathrm{Hz}$ filter four more, $25\,\mathrm{ms}$ — five ticks of P6's $5\,\mathrm{ms}$ clock before the controller sees the push it is making.
- **So a single RC is a compromise**, and $3.3\,\mathrm{k\Omega}$ is P6's: it removes the phantom completely and three quarters of the aliased ring for one tick of delay. Doing better on both at once takes a sharper filter or a faster ADC followed by digital filtering — [[02-foundations/signal-processing|6. Signal Processing §2 and §4]].

### 13. What this page does not cover

- **Semiconductor physics.** Why a p–n junction conducts one way and how a MOSFET's channel forms are taken as given; the switches here are models with an $R_{\text{on}}$ and a $V_F$.
- **AC power**: phasors beyond the one filter of §5, power factor, transformers, mains wiring.
- **Power conversion**: switch-mode supplies — a PWM leg feeding an inductor is already a step-down converter in disguise — battery chemistry, charging and state of charge.
- **The drive's internals**: current sensing, the current loop and the motor's thermal limits are [[04-robotics/actuators-drives|10.5 §5 and §6]]; brushless commutation and field-oriented control are beyond the wiki.
- **Signals in depth**: sampling theory, digital filters and the signal-to-noise ratio per bit are [[02-foundations/signal-processing|6. Signal Processing]]; when quantization is noise and how each sensor on P6 is modelled is [[04-robotics/sensor-models|3.2 Sensor Models & Noise]].
- **Communication and timing**: serial buses and fieldbuses, and the latency budget they spend, belong to [[04-robotics/robot-systems-deployment|10. Robot Systems §3]].
- **Safety engineering**: risk assessment, safety-rated control and the standards that govern them are [[04-robotics/hri-safety|11. HRI & Safety §6]]; §11 gives only the electrical reasoning.
- **The mechanical and fluid twins**: a capacitor and an inductor store energy as a spring and a mass do, and a resistor spends it as a damper does — the mass–spring–damper of [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §4–§5]]; power carried as pressure times flow rather than voltage times current is [[02-foundations/fluid-power|0.6.3 Fluid Power §4]].

### After reading

- [ ] Turn a battery's label into coulombs, joules and a runtime at a given power, and say why the runtime comes from the joules.
- [ ] Use Ohm's law, series and parallel, and $p=i^2R$ on a sensor, a wire or a winding.
- [ ] Write KCL at the nodes of a small circuit and solve it; give a divider's output and what a load does to it.
- [ ] Say what a capacitor and an inductor store and which of their variables cannot jump, and compute $RC$ and $L/R$.
- [ ] Give an RC filter's cutoff, its gain and phase at any frequency, and the delay it adds.
- [ ] Explain PWM and its ripple, trace an H-bridge's on and freewheeling paths, and say why an inductive load needs the second.
- [ ] Write the DC motor's circuit equation and close its power ledger at an operating point.
- [ ] Derive the inverting, non-inverting and instrumentation-amplifier gains from the two op-amp rules, and say why a bridge needs the last.
- [ ] Turn newtons into bridge microvolts, amplifier volts and ADC counts, and choose a gain.
- [ ] Say what an ADC's sampling folds, why the filter must come before it, and what the filter costs.
- [ ] Wire a star ground, and say why an emergency stop must cut power.

### Self-check

1. P6's battery is labelled $24\,\mathrm V$, $5.0\,\mathrm{Ah}$. How many coulombs and how many joules is that, and why does the push's runtime come from the joules rather than the coulombs?
2. During the push the winding carries $2.0\,\mathrm A$, yet the battery supplies $0.167\,\mathrm A$. Which laws make these consistent, and where does the difference come from?
3. What happens at the instant Q1 opens if the H-bridge has no freewheeling path, and where does the winding's current go in the bridge as drawn?
4. Why can a non-inverting amplifier of gain $400$ not read the load cell, when an instrumentation amplifier of the same gain can?
5. The PWM runs at exactly $100$ times the ADC's sample rate. What does its interference look like in the force readings, and what changes if the PWM drifts to $20.01\,\mathrm{kHz}$?
6. A lab-mate proposes to implement P6's emergency stop as a message that sets the duty to zero. Name two failures that design has and a chain of normally closed contacts in the supply lead does not.

> [!tip]- Answers
> 1. $5.0\,\mathrm{Ah}\times3600=18{,}000\,\mathrm C$, and $18{,}000\,\mathrm C\times24\,\mathrm{J/C}=432\,\mathrm{kJ}=120\,\mathrm{Wh}$. The drive converts current: the motor carries $2.0\,\mathrm A$ while the battery supplies $0.167\,\mathrm A$, so no single current links the two sides; power does — $4.0\,\mathrm W$ on both — so the runtime is energy over power, $120/4.0=30\,\mathrm h$.
> 2. KCL, averaged over a period: the battery carries the winding's $2.0\,\mathrm A$ only during the $8.33\%$ on-time and nothing while the current freewheels, so it averages $0.167\,\mathrm A$. And energy: $24\,\mathrm V\times0.167\,\mathrm A=4.0\,\mathrm W=2.0\,\mathrm V\times2.0\,\mathrm A$. The drive trades voltage for current the way a gearbox trades speed for torque; the winding's inductance, which holds the current through the off-time, is what makes the trade possible.
> 3. The winding insists on keeping its $2.0\,\mathrm A$ for the first instant (§4), so forcing it to zero in $100\,\mathrm{ns}$ puts about $L\,di/dt=20{,}000\,\mathrm V$ across the opening switch, which fails. In the bridge as drawn, Q4 stays on and Q2 turns on after the dead time — its diode carrying the current during the dead time itself — so the current circulates through Q2, the winding and Q4 with almost no voltage across the winding and decays only slowly, by $0.092\,\mathrm A$ in $45.8\,\mu\mathrm s$.
> 4. Because the $2.0\,\mathrm{mV}$ worth reading rides on $2.5\,\mathrm V$ common to both bridge outputs. A non-inverting amplifier amplifies one output against ground, so it would try to put out $400\times2.5\,\mathrm V=1000\,\mathrm V$ and saturate. The instrumentation amplifier's first stage passes the common $2.5\,\mathrm V$ at a gain of one while multiplying the difference by $400$, and its difference stage removes the common part — and both of its inputs draw almost no current, so the bridge is not loaded.
> 5. A constant offset: sampling $20\,\mathrm{kHz}$ at $200\,\mathrm{Hz}$ folds it to $\lvert20{,}000-100\cdot200\rvert=0\,\mathrm{Hz}$, so each reading catches the interference at the same phase and the lab's unfiltered chain reads a steady phantom $125\,\mathrm{mN}$. At $20.01\,\mathrm{kHz}$ the fold lands at $10\,\mathrm{Hz}$ and the phantom becomes a slow wobble, inside the band where contact happens. Only a filter before the ADC prevents either.
> 6. It depends on everything a message passes through — the button's input, the network, the controller's code and the drive's firmware — any of which can be what is failing; and a silent or crashed node leaves the last command live rather than stopping ([[04-robotics/robot-systems-deployment|10. Robot Systems §7]]). A contact chain in series with the contactor coil needs nothing to work: pressing a button, or a broken wire, opens it and removes the H-bridge's supply, and direct opening action forces the contacts apart even if they have welded.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and the object catalog: P6 and this page's frozen electronics, with the changes each item names.

1. **Draw.** The picture above for the cart **cruising** at $0.5\,\mathrm{m/s}$ against its $2.0\,\mathrm N$ of rolling resistance, out of contact with the panel: the power path with the current, the back-EMF, the average voltage, the duty and the battery current; the two current paths of one PWM period; the inset of $v(t)$ and $i(t)$ with the ripple's two extremes; and the sensing path with what each block reads. Say which numbers on the picture changed from the push, which vanished, and why.
2. **Derive.** (a) A new ADC: $16$ bits with $V_{\text{ref}}=2.5\,\mathrm V$, and the bridge excited at $10\,\mathrm V$. Give the LSB, the largest whole gain that keeps the rated $50\,\mathrm N$ inside the range, and at that gain the counts per newton and the newtons per count; then say what the higher excitation costs each gauge in heat. (b) The battery monitor read by an input of $1\,\mathrm{M\Omega}$: the voltage at the ADC, its code, and the battery voltage reported by firmware that assumes the unloaded ratio. (c) The shared ground of §11 while the cart cruises: the phantom force it adds, in counts and in newtons. (d) A drive with no freewheeling path opens the cruise current in $100\,\mathrm{ns}$: the voltage across its switch, and the energy the winding held.
3. **Do.** Bipolar PWM switches the two legs in anti-phase — Q1 with Q4 for $DT$, then Q2 with Q3 for the rest — so the winding sees $+V_s$ and $-V_s$ instead of $+V_s$ and $0$. Paste the template below after Part A of §12's lab, fill every `?`, and run it. Report the ripple at $20\,\mathrm{kHz}$ against Part A's, the frequency at which bipolar PWM matches unipolar PWM's $20\,\mathrm{kHz}$ ripple, and the reason bipolar ripples more at this duty.

```python
# Tier A template (Do): bipolar PWM for the push. Paste after Part A of the lab (it reuses settle, Vs, R, L), fill every ?.
D_bi = ?                                       # duty whose average (2*D - 1)*Vs holds 2.0 A at rest
m = 2.0*R/Vs                                   # the average voltage as a fraction of Vs

def pwm_run_bipolar(f, t_end=0.020):
    T, i, t = 1/f, 0.0, 0.0
    while t < t_end - 1e-12:
        i_min = i
        i = settle(i, ?, D_bi*T)               # Q1 and Q4 on
        i_max = i
        i = settle(i, ?, (1 - D_bi)*T)         # Q2 and Q3 on
        t += T
    return i_min, i_max

print("f_PWM (kHz)  i_min (A)  i_max (A)  ripple (A)  small-ripple formula (A)")
for f in (500, 1e3, 2e3, 5e3, 10e3, 20e3, 50e3, 130e3):
    i_min, i_max = pwm_run_bipolar(f)
    approx = ?                                 # derive it as §6 derives the unipolar one, in terms of Vs, m, L and f
    print(f"{f/1e3:10.1f} {i_min:10.4f} {i_max:10.4f} {i_max - i_min:11.4f} {approx:25.4f}")
```

> [!note]- How to draw it · 그리는 법
> - **Keep the loop's shape**: power path along the top, the belt and the cart in the middle, the sensing path along the bottom, the controller closing the loop on the left. Only the numbers change.
> - **Put the back-EMF in the motor.** Cruising, the winding is $R$, $L$ and a source $e=k_ev_c/r_p=2.5\,\mathrm V$ opposing the current; label all three, with the average voltage $\bar v=Ri+e$ beside them.
> - **Draw both current paths in the same direction through the winding**, solid for the on-time through Q1 and Q4, dashed for the freewheel through Q2 and Q4, and label each with its duration at the new duty.
> - **The inset is the push's inset at a new duty.** The ripple is $V_sD(1-D)/(Lf)$ whatever the back-EMF, so compute it from the new $D$; mark both extremes and the mean, and check the minimum stays above zero, which means the current never stops.
> - **The sensing path reads the contact force, not the motor's.** Out of contact the load cell sees nothing, so every block downstream reads zero, and a code of $0$ is also where a unipolar ADC hides small negative offsets — say so on the drawing.
> - **Close the ledger on the picture**: battery current and power, winding heat, the power crossing the back-EMF, and the mechanical $F\,v_c$ it must equal.

> [!tip]- Solutions
> 1. Back-EMF $e=5.0\cdot0.5=2.5\,\mathrm V$ ($25\,\mathrm{rad/s}$ at the motor); current $i=2.0/5.0=0.40\,\mathrm A$; average voltage $\bar v=0.40+2.5=2.9\,\mathrm V$; duty $2.9/24=12.08\%$, on $6.04\,\mu\mathrm s$ and freewheeling $43.96\,\mu\mathrm s$ of each $50\,\mu\mathrm s$. Ripple $24\cdot0.1208\cdot0.8792/(10^{-3}\cdot20{,}000)=0.1275\,\mathrm A$, so the current runs between $0.337$ and $0.464\,\mathrm A$ (the exact periodic solution) and never stops. Battery current $0.1208\cdot0.40=0.048\,\mathrm A$, $1.16\,\mathrm W$; winding heat $0.16\,\mathrm W$; $e\,i=1.0\,\mathrm W=F\,v_c=2.0\cdot0.5$. The sensing path reads $0\,\mathrm N$, $0\,\mathrm{mV}$, $0\,\mathrm V$ and code $0$. What changed: a back-EMF appeared and takes $2.5$ of the $2.9\,\mathrm V$; the current fell to a fifth; the ripple *grew*, from $0.092$ to $0.128\,\mathrm A$, because $D(1-D)$ grew from $0.076$ to $0.106$, and relative to the smaller current it is $32\%$ rather than $4.6\%$. What vanished: the force, the bridge output and the counts — a load cell measures contact, and the current now pays for rolling resistance it cannot see.
> 2. (a) $\text{LSB}=2.5/65{,}536=38.15\,\mu\mathrm V$. At $10\,\mathrm V$ the rated output is $20\,\mathrm{mV}$, so the gain must keep $20\,\mathrm{mV}\cdot G\le65{,}535\cdot38.15\,\mu\mathrm V=2.49996\,\mathrm V$: $G\le124.998$, so $G=124$. Then a newton is $400\,\mu\mathrm V\cdot124=49.6\,\mathrm{mV}$, $1300.2$ counts, and a count is $0.769\,\mathrm{mN}$ — sixteen times finer than the page's $12.5\,\mathrm{mN}$ — with clipping at $50.40\,\mathrm N$. Each gauge now has $5\,\mathrm V$ across it and dissipates $5^2/350=71.4\,\mathrm{mW}$, four times the page's $17.9\,\mathrm{mW}$. (b) $15\,\mathrm{k\Omega}\parallel1\,\mathrm{M\Omega}=14.78\,\mathrm{k\Omega}$, so $v=24\cdot14.78/114.78=3.090\,\mathrm V$, code $3090$, and firmware dividing by the unloaded $0.1304$ reports $23.69\,\mathrm V$, $1.3\%$ low. (c) $0.40\,\mathrm A\cdot10.1\,\mathrm{m\Omega}=4.0\,\mathrm{mV}$, $4$ counts, a phantom $0.050\,\mathrm N$ that appears whenever the cart moves. (d) $L\,di/dt=10^{-3}\cdot0.40/10^{-7}=4000\,\mathrm V$, from a stored $\tfrac12\cdot10^{-3}\cdot0.40^2=80\,\mu\mathrm J$.
> 3. Blanks: `D_bi = (1 + 2.0*R/Vs)/2`, which is $0.5417$ because $(2D-1)V_s=2.0\,\mathrm V$; the voltages `Vs` and `-Vs`; and `approx = Vs*(1 - m**2)/(2*L*f)`, derived as in §6 — during the on-time the inductance sees $V_s-\bar v=V_s(1-m)$ for $D_{\text{bi}}T=(1+m)T/2$, so $\Delta i\approx V_s(1-m)(1+m)/(2Lf)$. The sweep gives a ripple of $0.5958\,\mathrm A$ at $20\,\mathrm{kHz}$ ($1.702$ to $2.298\,\mathrm A$), $6.5$ times Part A's $0.0917$, with the formula exact to four digits; the $130\,\mathrm{kHz}$ row returns $0.0917\,\mathrm A$, so bipolar PWM needs $6.5$ times the frequency — and $6.5$ times the switching edges — to ripple as little. The reason is volt-seconds: unipolar PWM spends the off-time at $0\,\mathrm V$, only $2\,\mathrm V$ away from the $2\,\mathrm V$ the winding holds, while bipolar PWM drives the winding between $+24$ and $-24\,\mathrm V$ for the whole period, $22\,\mathrm V$ and $26\,\mathrm V$ away, so each half-period moves the current far more. Bipolar's merit is elsewhere: its average $(2D-1)V_s$ passes smoothly through zero at $D=50\%$, so reversing the push needs no change of switching pattern.

### Sources

- OpenStax, *University Physics Volume 2* (https://openstax.org/books/university-physics-volume-2, read as HTML) — §7.2 the volt as a joule per coulomb; §8.3 and §14.3 the stored energies $\tfrac12CV^2$ and $\tfrac12LI^2$; §9.1 current and its conventional direction; §9.3 resistivity and its temperature coefficient (copper $1.68\times10^{-8}\,\Omega{\cdot}\mathrm m$ and $0.0039\,/^\circ\mathrm C$); §9.5 $P=IV=I^2R=V^2/R$; §10.2–10.3 series and parallel resistors and Kirchhoff's rules from charge and energy conservation; §10.5 and §14.4 the time constants $RC$ and $L/R$; §10.6 short circuits and fuses; §14.2 self-inductance, $\varepsilon=-L\,dI/dt$.
- OpenStax, *University Physics Volume 3*, §9.7 Semiconductor Devices — the diode as a one-way valve and its current law $I=I_0(e^{eV/k_BT}-1)$.
- OpenStax, *College Physics 2e*, §17.6 Hearing — normal human hearing from $20$ to $20{,}000\,\mathrm{Hz}$.
- NIST: the CODATA values of the elementary charge, $1.602176634\times10^{-19}\,\mathrm C$, and the Boltzmann constant, $1.380649\times10^{-23}\,\mathrm{J/K}$, both exact (physics.nist.gov/cuu/Constants); *NIST Guide to the SI* (SP 811), Chapter 4, Table 3, for the named derived units in terms of each other, and Appendix B.8 for the exact factors $1\,\mathrm{A{\cdot}h}=3.6\times10^3\,\mathrm C$ and $1\,\mathrm{W{\cdot}h}=3.6\times10^3\,\mathrm J$.
- Micro-Measurements (Vishay Precision Group), StrainBlog: "Crossing Over the Wheatstone Bridge" (strainblog.micro-measurements.com/content/crossing-over-wheatstone-bridge) — the bridge output $V_{\text{out}}=KV\varepsilon N/4$ and the nominal gauge factor of $2$; "Strain Sensor Resistances Explained" (strainblog.micro-measurements.com/tips/strain-sensor-resistances-explained) — $120$, $350$ and $1000\,\Omega$ gauges, and higher resistance reducing self-heating.
- Massload Technologies, "What Is mV/V in Load Cells?" (www.massload.com/what-is-mv-v-in-load-cells-an-introductory-guide/) — the definition of rated output per volt of excitation at rated capacity, the output formula, and $1$ to $3\,\mathrm{mV/V}$ as the usual range.
- Toshiba Electronic Devices & Storage, e-learning and FAQ pages (https://toshiba.semicon-storage.com) — the op-amp's virtual short, with an example open-loop gain of $100{,}000$ and no current into the inputs; the MOSFET's gate-formed channel, its $R_{DS(ON)}=V_{DS}/I_D$ at a stated gate voltage, and its body diode; a rectifier diode's one-way conduction.
- IDEC, "Emergency Stop Switches" safety guide (www.idec.com/en-us/solutions/safety/guide/safety02) — normally closed contacts so that a circuit fault stops the machine, and direct opening action forcing welded contacts apart.
- Within this wiki: [[02-foundations/engineering-math|0.5 Engineering Math]] for the mathematics; [[02-foundations/lab-plants|0.6 Lab Plants]] for P6; [[04-robotics/actuators-drives|10.5 Actuators & Drives]] for the motor's frozen constants and everything the drive does beyond this page; [[02-foundations/signal-processing|6. Signal Processing]] and [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] for what happens to the samples next.
- Every other number on this page — the battery, fuse, belt, rolling resistance, load cell, amplifier, filter, ADC, pickup and ring — is a course number chosen here and computed with the page's own code or by hand; recompute rather than trust.

## 한국어

*[[02-foundations/engineering-math|0.5 공업수학]] — 도함수, 1차 상미분방정식과 그 지수 함수, 복소수 — 과 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6** 위에 선다. P6의 제어기는 "모터를 200 Hz로 명령한다"고만 하고 명령과 모터 사이에 무엇이 있는지는 말하지 않는다. P6의 전자 회로를 처음 여는 페이지다. 모터는 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]가 P2에 고정한 바로 그 모터라서 두 페이지의 숫자가 하나하나 맞고, 센싱 체인은 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]과 [[02-foundations/signal-processing|6. 신호처리]] 밑에 깔리는 바닥이다.*

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택 — 인식, 물체·장면 이해, 파지, 모션·과제 계획, 조작, 접촉·힘·촉각 피드백, 학습과 적응, 작업 완료 — 에서 이 페이지는 구동 층과 센싱 층 밑의 물리적 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). "*저 패널을 프레임에 설치해*"에서는 패널을 옮기는 구동계와, 패널이 닿는 것을 느끼는 힘 센서다. 로봇의 모터와 힘 센서는 신호이기 전에 회로이고, 회로에서 저지른 실수는 제어나 학습의 실패처럼 보인다. 모터 귀환선을 함께 쓰는 센서 접지는 $2.0\,\mathrm A$를 P6 로드셀의 유령 힘 $0.25\,\mathrm N$으로 바꾸고, 메시지로 보내는 비상 정지는 바로 소프트웨어가 멈출 때 실패한다. 여기서 배우는 권선, 듀티비, 브리지, 샘플러는 [[04-robotics/actuators-drives|10.5 §5]], [[04-robotics/sensor-models|3.2 센서 모델 §4]], [[02-foundations/signal-processing|6. 신호처리 §2]], [[04-robotics/force-compliance-control|13. §2]]로 이어지고, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지는 블록 1, 곧 토목 학위가 비워 둔 전기를 메우는 기초의 바닥에 놓인다. 이 페이지를 마치면 힘 하나를 뉴턴에서 암페어, 볼트, 듀티비를 거쳐 ADC 카운트까지 따라가고, 그 사이의 분배기, 필터, 이득의 크기를 정할 수 있다.

> [!note] 처음이라면 · First pass
> 한 번에 90분 안팎, 두 번이면 된다. 그림은 페이지 전체를 루프 하나로 그린 것이니 먼저 보고, 절을 하나 읽을 때마다 다시 돌아온다. **첫 번째, 전력 경로:** §1–§4 — 단위, 옴의 법칙, 키르히호프 법칙과 분배기, 커패시터와 인덕터 — 를 읽고, 24 V 배터리가 어떻게 모터 속 한결같은 2.0 A가 되는지 §6–§7에서 읽는다. 권선이 2.0 A를 흘리는데 배터리는 왜 0.167 A만 내는지 스스로 설명해 보는 것으로 첫 번째를 끝낸다(스스로 점검 2). **두 번째, 센싱 경로:** §5(필터)와 §8–§10(증폭기, 브리지, ADC)을 읽고, 10 N 밀기 하나를 모터로 내보냈다가 로드셀로 다시 읽어 들이는 계산 절로 간다. 무엇이든 배선하기 전에는 §11을 읽고, §12의 실습을 돌린 뒤 스스로 점검의 나머지에 답한다. 접힌 *더 깊이* 상자는 두 번째 읽을 때로 미뤄도 된다.

### 이 페이지의 대상 · Running object

대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**이다. 직선 위의 카트로, 위치는 미터 단위, 엔코더는 $2048$ counts/m이고, 제어기가 엔코더를 샘플해 모터를 $200\,\mathrm{Hz}$로 명령한다. 카탈로그는 *모터*라는 낱말에서 멈춘다. 이 페이지는 실제 카트가 배터리와 제어기 사이에 싣고 다니는 것을 채워 넣고 고정한다. 배터리, 퓨즈, 비상 정지. 펄스 폭 변조로 모터를 구동하는 H-브리지. 벨트 풀리를 돌려 카트를 움직이는 모터. 그리고 카탈로그에 없는 센서 하나 — 카트와 공구 사이의 스트레인 게이지 로드셀로, 계장 증폭기, RC 필터, 아날로그-디지털 변환기(ADC)를 거쳐 읽는다. 과제는 로보틱스 관통 과제의 1차원 판이다. 카트가 공구를 패널에 대고 밀기를 유지한다.

**모터는 10.5의 것이다.** 권선, 토크 상수, 전류 한계, 공급 전압은 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]가 P2의 관절마다 고정한 숫자이므로, 여기서 계산한 전류나 전압은 그 페이지에서도 같은 숫자다. 표의 나머지는 이 페이지의 것이다. 현실적인 크기로 이 페이지가 고른 강의용 숫자이며, 어떤 제품의 측정값이나 데이터시트 값도 아니다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $V_s$ | $24\,\mathrm V$ | 배터리 전압. 10.5의 공급 전압(§1) |
| $Q$ | $5.0\,\mathrm{Ah}$ | 라벨에 적힌 배터리 용량(§1) |
| $r_b$ | $0.050\,\Omega$ | 배터리 내부 저항(§11) |
| 퓨즈 | $15\,\mathrm A$ | 배터리 양극 도선에(§11) |
| $R$, $L$ | $1.0\,\Omega$, $1.0\,\mathrm{mH}$ | 권선 저항과 인덕턴스. 10.5(§4, §7) |
| $k_t$, $k_e$ | $0.10\,\mathrm{N{\cdot}m/A}$, $0.10\,\mathrm{V{\cdot}s/rad}$ | 토크 상수와 역기전력 상수. 10.5(§7) |
| $I_{\max}$ | $10\,\mathrm A$ | 구동계의 전류 한계. 10.5(§7) |
| $f_{\text{PWM}}$ | $20\,\mathrm{kHz}$, 곧 $T=50\,\mu\mathrm s$ | H-브리지의 스위칭 주파수(§6) |
| $R_{\text{on}}$, $V_F$ | $10\,\mathrm{m\Omega}$, $0.7\,\mathrm V$ | 켜진 MOSFET의 저항, 도통 중인 다이오드의 전압 강하(§6) |
| $r_p$ | $0.020\,\mathrm m$ | 벨트 풀리 반지름(§7) |
| $F_{\text{roll}}$ | $2.0\,\mathrm N$ | 순항 중 구름 저항(§7) |
| 엔코더 | $2048$ counts/m | P6의 카탈로그 숫자. ADC가 아니라 카운터가 읽는다(§10) |
| 로드셀 | 정격 $50\,\mathrm N$, $2.0\,\mathrm{mV/V}$ | $350\,\Omega$ 포일 게이지 넷의 풀 브리지, 게이지율 $2.0$(§9) |
| $V_{ex}$ | $5.0\,\mathrm V$ | 브리지 여기 전압(§9) |
| $G$ | $400$ | 계장 증폭기 이득(§8). §10에서 바꿔 본다 |
| $A$ | $10^5$ | 연산 증폭기 하나하나의 개루프 이득(§8) |
| $R_f$, $C_f$ | $3.3\,\mathrm{k\Omega}$, $1.0\,\mu\mathrm F$ | ADC 앞의 안티에일리어스 RC 필터(§5). §12에서 바꿔 본다 |
| ADC | $12$비트, $V_{\text{ref}}=4.096\,\mathrm V$ | P6의 제어 주기인 $200\,\mathrm{Hz}$로 샘플(§10) |
| 배터리 모니터 | $100\,\mathrm{k\Omega}$ 위에 $15\,\mathrm{k\Omega}$ | 배터리 전압을 ADC 범위로 줄이는 분배기(§3) |

모델링 선택 둘을 한 번만 적어 둔다. 스위치는 $R_{\text{on}}$과 $V_F$를 빼면 이상적이고, 모터에서 카트로 가는 벨트 구동은 손실이 없다. 이 페이지는 회로에 관한 페이지이고, 구동 계통의 마찰과 관성은 [[04-robotics/actuators-drives|10.5]]의 몫이다. 손실 없는 벨트에서 토크 $\tau$는 카트를 $\tau/r_p$로 밀므로, 구동계의 $10\,\mathrm A$ 한계는 $0.10\cdot10/0.020=50\,\mathrm N$의 밀기다. 로드셀의 정격과 같아서, 모터가 낼 수 있는 힘은 센서가 모두 읽을 수 있다. $2.0\,\mathrm{mV/V}$와 $350\,\Omega$ 게이지는 로드셀과 스트레인 게이지 제조사가 설명하는 종류의 값이며(출처), 어느 값도 데이터시트에서 가져오지 않았다.

*범위: 이 페이지는 로봇의 전자 회로가 기대는 회로 물리를 카트 하나 위에서 가르친다. 전하·전류·전압·전력·에너지, 저항·키르히호프 법칙·분배기와 부하 효과, 커패시터·인덕터와 그 시정수, RC 저역통과 필터, 스위치·펄스 폭 변조·환류 경로를 가진 H-브리지, 회로 소자로서의 DC 모터, 연산 증폭기와 계장 증폭기, 휘트스톤 브리지와 스트레인 게이지 로드셀, ADC, 그리고 접지·잡음·전기 안전이다. 반도체 물리, 교류 전력, 전원 설계, 브러시리스 모터의 정류, 통신 버스는 가르치지 않는다(빠진 것의 목록은 §13). 주파수 응답과 샘플링을 깊이 다루는 곳은 [[02-foundations/signal-processing|6. 신호처리]], P6 센서들의 잡음 모델은 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]], 구동계의 열·속도·전류 한계는 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]], 안전 용어는 [[04-robotics/hri-safety|11. HRI와 안전]]이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 404" style="max-width:100%;height:auto" role="img" aria-label="10 N을 미는 동안 P6 카트의 전자 회로를 루프 하나로: 배터리, 퓨즈, 비상 정지가 H-브리지에 전원을 주고, 켜짐 경로는 Q1과 Q4를, 환류 경로는 Q2와 Q4를 지난다. 삽도는 권선의 전압 펄스와 리플 0.092 A를 가진 2.0 A 전류. 모터가 풀리를 돌려 카트와 로드셀을 패널에 밀고, 로드셀 브리지, 계장 증폭기, RC 필터, ADC, 제어기가 800 카운트를 읽어 duty를 정한다">
  <defs><marker id="bceAk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="10" y="16" font-size="12" font-weight="600" fill="currentColor">10 N을 밀고 있는 P6의 전자 회로</text>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <polyline points="34,100 34,46 78,46"/><polyline points="106,46 132,46"/><polyline points="158,46 330,46 330,66"/>
    <polyline points="34,108 34,176 330,176 330,156"/>
    <line x1="22" y1="100" x2="46" y2="100" stroke-width="2"/><line x1="28" y1="108" x2="40" y2="108" stroke-width="3"/>
    <rect x="78" y="41" width="28" height="10" rx="2"/><line x1="78" y1="46" x2="106" y2="46" stroke-width="0.8"/>
    <line x1="130" y1="42" x2="160" y2="42" stroke-width="1.8"/>
    <polyline points="210,46 210,66"/><polyline points="210,90 210,132"/><polyline points="210,156 210,176"/>
    <polyline points="330,90 330,132"/>
    <rect x="199" y="66" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <rect x="199" y="132" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <rect x="319" y="66" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <rect x="319" y="132" width="22" height="24" rx="2" fill="currentColor" fill-opacity="0.06"/>
    <polyline points="210,60 190,60 190,70"/><polyline points="190,84 190,96 210,96"/>
    <line x1="184" y1="70" x2="196" y2="70" stroke-width="1.4"/>
    <path d="M 190 70 L 184 84 L 196 84 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="210,126 190,126 190,136"/><polyline points="190,150 190,162 210,162"/>
    <line x1="184" y1="136" x2="196" y2="136" stroke-width="1.4"/>
    <path d="M 190 136 L 184 150 L 196 150 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="330,60 350,60 350,70"/><polyline points="350,84 350,96 330,96"/>
    <line x1="344" y1="70" x2="356" y2="70" stroke-width="1.4"/>
    <path d="M 350 70 L 344 84 L 356 84 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="330,126 350,126 350,136"/><polyline points="350,150 350,162 330,162"/>
    <line x1="344" y1="136" x2="356" y2="136" stroke-width="1.4"/>
    <path d="M 350 136 L 344 150 L 356 150 Z" fill="currentColor" fill-opacity="0.25"/>
    <polyline points="210,111 244,111"/><polyline points="296,111 330,111"/>
    <rect x="244" y="101" width="52" height="20" rx="4" fill="currentColor" fill-opacity="0.08"/>
  </g>
  <g fill="currentColor"><circle cx="132" cy="46" r="2.2"/><circle cx="158" cy="46" r="2.2"/><circle cx="210" cy="111" r="2.4"/><circle cx="330" cy="111" r="2.4"/></g>
  <polyline points="228,54 228,95 308,95 308,170" fill="none" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.8" marker-end="url(#bceAk)"/>
  <polyline points="234,166 234,127 314,127" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#bceAk)"/>
  <polyline points="314,127 314,166 238,166" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#bceAk)"/>
  <line x1="270" y1="121" x2="270" y2="226" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 2.5"/>
  <g font-size="11" fill="currentColor">
    <text x="52" y="96">배터리</text><text x="52" y="110">24 V · 5.0 Ah</text>
    <text x="52" y="134" font-size="10">배터리 전류</text><text x="52" y="147" font-size="10">0.167 A, 4.0 W</text>
    <text x="92" y="34" text-anchor="middle">퓨즈 15 A</text><text x="145" y="64" text-anchor="middle" font-size="10">비상 정지(NC)</text>
    <text x="34" y="192">0 V(접지)</text>
    <text x="210" y="82" text-anchor="middle" font-size="10">Q1</text><text x="210" y="148" text-anchor="middle" font-size="10">Q2</text>
    <text x="330" y="82" text-anchor="middle" font-size="10">Q3</text><text x="330" y="148" text-anchor="middle" font-size="10">Q4</text>
    <text x="270" y="115" text-anchor="middle">M</text>
    <text x="238" y="89" font-size="10">1.0 Ω · 1.0 mH</text>
    <text x="276" y="199" font-size="10">실선: 켜짐, 50 µs 중 4.17 µs (Q1, Q4)</text><text x="276" y="211" font-size="10">점선: 환류, 45.8 µs (Q2, Q4)</text>
  </g>
  <rect x="370" y="26" width="182" height="166" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.9"/>
  <polyline points="384.0,80.0 384.0,58.0 388.8,58.0 388.8,80.0 441.0,80.0 441.0,58.0 445.8,58.0 445.8,80.0 498.0,80.0" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="384.0,164.3 385.2,152.0 386.4,139.8 387.6,127.6 388.8,115.4 394.0,120.4 399.2,125.3 404.4,130.3 409.6,135.2 414.9,140.1 420.1,145.0 425.3,149.8 430.6,154.7 435.8,159.5 441.0,164.3 441.0,164.3 442.2,152.0 443.4,139.8 444.6,127.6 445.8,115.4 451.0,120.4 456.2,125.3 461.4,130.3 466.6,135.2 471.9,140.1 477.1,145.0 482.3,149.8 487.6,154.7 492.8,159.5 498.0,164.3" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="384.0" y1="115.4" x2="498.0" y2="115.4" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 2.5" stroke-opacity="0.5"/>
  <line x1="384.0" y1="140.0" x2="498.0" y2="140.0" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4 3" stroke-opacity="0.75"/>
  <line x1="384.0" y1="164.3" x2="498.0" y2="164.3" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 2.5" stroke-opacity="0.5"/>
  <line x1="384.0" y1="80" x2="498.0" y2="80" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.4"/>
  <g stroke="currentColor" stroke-width="0.9"><line x1="384.0" y1="176" x2="384.0" y2="180"/><line x1="441.0" y1="176" x2="441.0" y2="180"/><line x1="498.0" y1="176" x2="498.0" y2="180"/></g>
  <g font-size="10" fill="currentColor">
    <text x="378" y="40" font-size="11">권선, PWM 두 주기</text>
    <text x="386" y="53">v: 4.17 µs 동안 24 V</text>
    <text x="502" y="62">24 V</text><text x="502" y="84">0 V</text>
    <text x="386" y="103">i: 리플 0.092 A p-p</text>
    <text x="502" y="118.9">2.046 A</text>
    <text x="502" y="143.5">평균 2.0</text>
    <text x="502" y="167.8">1.954 A</text>
    <text x="384.0" y="188" text-anchor="middle">0</text><text x="441.0" y="188" text-anchor="middle">50</text><text x="498.0" y="188" text-anchor="middle">100 µs</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <circle cx="270" cy="238" r="12"/>
    <line x1="270" y1="226" x2="400" y2="226"/><line x1="270" y1="250" x2="392" y2="250" stroke-opacity="0.5"/>
    <rect x="400" y="216" width="60" height="26" rx="3" fill="currentColor" fill-opacity="0.08"/>
    <circle cx="412" cy="246" r="4"/><circle cx="448" cy="246" r="4"/>
    <line x1="380" y1="251" x2="500" y2="251" stroke-width="1" stroke-opacity="0.6"/>
    <rect x="460" y="222" width="14" height="14" fill="currentColor" fill-opacity="0.25"/>
    <line x1="474" y1="229" x2="502" y2="229" stroke-width="2.4"/>
    <line x1="504" y1="206" x2="504" y2="262" stroke-width="2.4"/>
    <path d="M 504 212 L 512 206 M 504 220 L 512 214 M 504 228 L 512 222 M 504 236 L 512 230 M 504 244 L 512 238 M 504 252 L 512 246 M 504 260 L 512 254" stroke-width="0.8" stroke-opacity="0.6"/>
  </g>
  <circle cx="270" cy="238" r="1.6" fill="currentColor"/>
  <line x1="480" y1="219" x2="499" y2="219" stroke="currentColor" stroke-width="1.3" marker-end="url(#bceAk)"/>
  <line x1="467" y1="236" x2="506" y2="287" stroke="currentColor" stroke-width="1.1" stroke-dasharray="1.5 2.5"/>
  <g font-size="11" fill="currentColor">
    <text x="254" y="235" text-anchor="end" xml:space="preserve">풀리 r<tspan dy="3" font-size="10">p</tspan><tspan dy="-3"> = 20 mm</tspan></text>
    <text x="254" y="250" text-anchor="end">τ = 0.20 N·m</text>
    <text x="292" y="244" xml:space="preserve">F = k<tspan dy="3" font-size="10">t</tspan><tspan dy="-3">i / r</tspan><tspan dy="3" font-size="10">p</tspan><tspan dy="-3"> = 10 N</tspan></text>
    <text x="430" y="233" text-anchor="middle" font-size="10">카트</text>
    <text x="467" y="213" text-anchor="middle" font-size="10">로드셀</text>
    <text x="516" y="232" font-size="10">패널</text>
    <text x="482" y="266" text-anchor="end" font-size="10">변형</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <path d="M 510 288 L 540 318 L 510 348 L 480 318 Z"/>
    <rect x="487.0" y="299.5" width="16" height="7" transform="rotate(-45 495.0 303.0)" fill="currentColor" fill-opacity="0.15"/>
    <rect x="517.0" y="299.5" width="16" height="7" transform="rotate(45 525.0 303.0)" fill="currentColor" fill-opacity="0.15"/>
    <rect x="487.0" y="329.5" width="16" height="7" transform="rotate(45 495.0 333.0)" fill="currentColor" fill-opacity="0.15"/>
    <rect x="517.0" y="329.5" width="16" height="7" transform="rotate(-45 525.0 333.0)" fill="currentColor" fill-opacity="0.15"/>
    <line x1="510" y1="348" x2="510" y2="354"/><line x1="502" y1="354" x2="518" y2="354"/><line x1="505" y1="357" x2="515" y2="357"/><line x1="508" y1="360" x2="512" y2="360"/>
    <polyline points="480,318 462,318 462,306 446,306"/>
    <polyline points="540,318 552,318 552,368 458,368 458,330 446,330"/>
    <path d="M 446 296 L 446 340 L 398 318 Z" fill="currentColor" fill-opacity="0.06"/>
    <polyline points="398,318 348,318"/><rect x="320" y="313" width="28" height="10" fill="currentColor" fill-opacity="0.1"/><polyline points="320,318 280,318"/>
    <polyline points="304,318 304,330"/><line x1="294" y1="330" x2="314" y2="330" stroke-width="2"/><line x1="294" y1="336" x2="314" y2="336" stroke-width="2"/><polyline points="304,336 304,344"/>
    <line x1="296" y1="344" x2="312" y2="344"/><line x1="299" y1="347" x2="309" y2="347"/><line x1="302" y1="350" x2="306" y2="350"/>
    <rect x="214" y="298" width="66" height="40" rx="3" fill="currentColor" fill-opacity="0.06"/>
    <rect x="10" y="292" width="152" height="56" rx="3" fill="currentColor" fill-opacity="0.06"/>
  </g>
  <g fill="currentColor"><circle cx="304" cy="318" r="2.2"/></g>
  <line x1="214" y1="318" x2="165" y2="318" stroke="currentColor" stroke-width="1.3" marker-end="url(#bceAk)"/>
  <polyline points="80,292 80,206 196,206 196,186" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="6 3" marker-end="url(#bceAk)"/>
  <g font-size="10" fill="currentColor">
    <text x="518" y="290" font-size="11">5.0 V</text>
    <text x="452" y="290">2.0 mV</text>
    <text x="422" y="356" text-anchor="middle">계장 증폭기</text>
    <text x="424" y="322" text-anchor="middle">× 400</text>
    <text x="440" y="310" text-anchor="middle">+</text><text x="440" y="334" text-anchor="middle">−</text>
    <text x="373" y="311" text-anchor="middle">0.80 V</text>
    <text x="334" y="308" text-anchor="middle">3.3 kΩ</text>
    <text x="304" y="364" text-anchor="middle">1.0 µF</text>
    <text x="304" y="377" text-anchor="middle" xml:space="preserve">f<tspan dy="3" font-size="10">c</tspan><tspan dy="-3"> = 48 Hz</tspan></text>
    <text x="247" y="315" text-anchor="middle" font-size="11">ADC</text><text x="247" y="330" text-anchor="middle">12비트</text>
    <text x="247" y="352" text-anchor="middle">1 mV/카운트</text>
    <text x="190" y="312" text-anchor="middle">800</text>
    <text x="86" y="308" text-anchor="middle" font-size="11">제어기, 200 Hz</text><text x="86" y="323" text-anchor="middle">800 카운트 → 10.0 N</text><text x="86" y="338" text-anchor="middle">2.0 A 요청 → D = 8.33 %</text>
    <text x="88" y="221">duty 8.33 %, 20 kHz → 게이트</text>
    <text x="510" y="385" text-anchor="middle">브리지 4 × 350 Ω</text><text x="510" y="398" text-anchor="middle">50 N에서 2.0 mV/V</text>
  </g>
</svg>

계산 절의 $10\,\mathrm N$ 밀기를 유지하는 P6의 전자 회로를 루프 하나로 그렸다. 위: 배터리가 퓨즈와 비상 정지를 거쳐 H-브리지에 전원을 대고, Q1과 Q4가 $50\,\mu\mathrm s$마다 $4.17\,\mu\mathrm s$ 동안 권선에 $24\,\mathrm V$를 걸며(실선 경로), 나머지 $45.8\,\mu\mathrm s$ 동안 전류는 Q2와 Q4를 지나 환류하므로(점선 경로), 권선은 $0.092\,\mathrm A$의 리플(삽도)을 얹은 $2.0\,\mathrm A$를 흘리지만 배터리는 $0.167\,\mathrm A$만 낸다. 아래: 밀기가 로드셀을 변형시켜 브리지 출력이 $2.0\,\mathrm{mV}$가 되고, 증폭기가 이를 $0.80\,\mathrm V$로 만들고, RC 필터가 통과시키고, ADC가 $800$ 카운트를 보고하고, 제어기가 $10.0\,\mathrm N$을 읽어 루프를 닫는 duty를 정한다.

### 1. 전하, 전류, 전압, 전력, 에너지

회로는 흐리기 쉬운 세 양으로 해석하고, 그것들을 흐리면 전형적인 실수가 나온다. "전류를 써서 없애는" 모터, 암페어시만 보고 읽은 작동 시간. 이 페이지의 모든 양은 셋 중 하나다. 전하가 얼마나 움직이는가, 전하 한 단위가 에너지를 얼마나 싣는가, 그리고 그 둘의 곱인 전력이다. 전하 $q$는 쿨롱으로 세고, 그 알갱이는 자연이 정해 두었다. 전자 하나가 $e=1.602176634\times10^{-19}\,\mathrm C$를 싣고 SI는 이 값을 정확한 값으로 정한다(NIST). 그러니 1쿨롱은 전자 $6.24\times10^{18}$개다.

전기가 처음이라면 그림 하나가 멀리까지 데려다준다. 회로는 물이 가득 찬 닫힌 관의 고리다. 전압은 압력 — 흐르는 것 한 단위를 미는 힘 — 의 자리에, 전류는 체적 유량의 자리에 선다. 배터리는 양단에 일정한 압력 차를 유지하는 펌프, 도선은 넓은 관, 저항은 압력을 열로 바꾸는 좁은 관이다. 전력은 두 세계 모두에서 압력 곱하기 유량이다. 유체 동력이 $pQ$로 쓰는 것을 이 페이지는 $vi$로 쓴다. 이 그림은 커패시터와 인덕터에서 가장 약하고, §4가 그 둘에 더 나은 그림을 준다.

> **전류, 전압, 전력의 정의.** **전류**(current), **전압**(voltage), **전력**(power)은 *한 흐름의 세 가지 비율*이다. 시간당 전하, 전하당 에너지, 시간당 에너지. 그리고 셋 모두 회로 전체가 아니라 회로 안의 한 자리에 속한다. 전류는 가지(branch)에, 전압은 두 점의 쌍에, 전력은 소자 하나에 속한다. 정의 조건은 양마다 하나씩, 셋이다. 전류 $i$는 정해 둔 단면을 전하가 지나가는 비율이고, 정해 둔 화살표 방향을 양으로 센다. *관례상의* 전류는 양전하가 움직일 방향이므로, 도선 속 전자는 그 반대로 흘러간다(OpenStax). 전압 $v$는 두 점 사이의 **차이**, 곧 1쿨롱이 한 점에서 다른 점으로 가며 얻거나 내놓는 에너지다. "어떤 노드의 전압"은 언제나 기준 노드, 곧 §11의 접지에 대한 값이다. 그리고 소자가 흡수하는 전력은 그 양단 전압과 그 속을 지나는 전류의 곱이며, 전류가 $+$ 단자로 들어갈 때를 양으로 센다. 이것은 앞의 둘에서 [[02-foundations/engineering-math|0.5 §1]]의 연쇄 법칙으로 나온다.
>
> $$i=\frac{dq}{dt},\qquad v=\frac{dw}{dq},\qquad p=\frac{dw}{dt}=\frac{dw}{dq}\,\frac{dq}{dt}=v\,i$$
>
> $w$는 소자에 전달된 에너지(줄)다. 그래서 단위는 $1\,\mathrm A=1\,\mathrm{C/s}$, $1\,\mathrm V=1\,\mathrm{J/C}$, $1\,\mathrm W=1\,\mathrm{J/s}=1\,\mathrm{V{\cdot}A}$이다.
> - **예**: 밀기 중의 권선. $i=2.0\,\mathrm A$는 매초 $2.0$쿨롱, 곧 전자 $1.25\times10^{19}$개가 권선을 지난다는 뜻이다. 양단의 $v=2.0\,\mathrm V$는 지나가는 1쿨롱마다 $2.0\,\mathrm J$을 거기 두고 간다는 뜻이다. 그래서 권선은 $p=4.0\,\mathrm W$를 흡수한다.
> - **비예**: "모터가 전류를 써서 없앤다." 전하는 보존되므로 권선에 들어간 $2.0\,\mathrm A$는 그대로 나온다(§3). 권선이 가져가는 것은 에너지, 지나가는 1쿨롱마다 $2.0\,\mathrm J$이다. 또 하나. "배터리가 $24\,\mathrm V$이니 모터도 $24\,\mathrm V$를 받는다." 배터리의 $24\,\mathrm V$는 배터리 자신의 두 단자 사이 값이고, 밀기 중에 구동계가 모터 양단에 거는 것은 평균 $2.0\,\mathrm V$뿐이다(§6).
> - **왜 중요한가**: 전력은 회로가 나머지 모든 것과 만나는 자리다. 저항 속의 열(§2), 카트에서의 힘 곱하기 속도(§7). 그리고 에너지는 배터리가 담고 있는 것이다.

배터리 라벨은 전하를 암페어시로 적는다. $1\,\mathrm{A{\cdot}h}=3600\,\mathrm C$이고 정확한 값이다(NIST). 배터리의 에너지는 그 전하에 전압을 곱한 것으로, 와트시로 적는다. $1\,\mathrm{W{\cdot}h}=3600\,\mathrm J$이다.

$$E=V_s\,Q=24\,\mathrm V\times5.0\,\mathrm{Ah}=120\,\mathrm{Wh}=432\,\mathrm{kJ}$$

$5.0\times3600=18{,}000\,\mathrm C$가 저마다 $24\,\mathrm J$을 싣고 있으니 $432\,\mathrm{kJ}$이기 때문이다. 작동 시간은 전하가 아니라 에너지의 문제다. 구동계가 전류를 다른 전류로 바꾸기 때문이다. 밀기 중에 모터는 $2.0\,\mathrm A$를 흘리지만 배터리는 $0.167\,\mathrm A$를 낸다(계산 절). 두 쪽이 공유하는 것은 전력, 양쪽 모두 $4.0\,\mathrm W$이다. 그래서 라벨의 $120\,\mathrm{Wh}$는 밀기를 $120/4.0=30\,\mathrm h$ 동안, §7의 순항($1.16\,\mathrm W$)을 $103\,\mathrm h$ 동안 버틴다. 이것은 모터 몫만의 계산이다. 제어기와 센서도 같은 배터리에서 전력을 끌어가고, 라벨 가운데 실제로 쓸 수 있는 양은 배터리에 달려 있는데, 이 페이지는 배터리를 모델링하지 않는다.

이 페이지의 단위는 모두 고유한 이름을 가진 SI 단위이고, 서로를 써서 풀어 쓰면(NIST SP 811, 표 3) 회로 파라미터의 곱 둘이 시간이 된다.

| 단위 | 기호 | 다른 SI 단위로 | 양 |
|---|---|---|---|
| 쿨롱 | C | A·s | 전하 |
| 볼트 | V | W/A 또는 J/C | 전압 |
| 옴 | Ω | V/A | 저항(§2) |
| 패럿 | F | C/V | 커패시턴스(§4) |
| 헨리 | H | Wb/A 또는 V·s/A | 인덕턴스(§4) |

$$1\,\Omega\cdot1\,\mathrm F=\frac{\mathrm V}{\mathrm A}\cdot\frac{\mathrm{A{\cdot}s}}{\mathrm V}=1\,\mathrm s,\qquad \frac{1\,\mathrm H}{1\,\Omega}=\frac{\mathrm{V{\cdot}s/A}}{\mathrm{V/A}}=1\,\mathrm s$$

그래서 저항 곱하기 커패시턴스와 인덕턴스 나누기 저항은 둘 다 시간이다. §4의 두 시정수다. 같은 셈으로 $1\,\mathrm{N{\cdot}m/A}=1\,\mathrm{J/(A{\cdot}rad)}=1\,\mathrm{V{\cdot}s/rad}$이 되고, [[04-robotics/actuators-drives|10.5 §1]]이 SI 단위에서 $k_t=k_e$라고 쓸 수 있는 이유가 이것이다.

### 2. 저항: 옴의 법칙, 열, 직렬과 병렬

카트의 도선, 권선, 스위치는 모두 지나는 전류에 맞서고, 그것이 전압과 열로 얼마를 치르게 하는지가 이 절의 물음이다. 저항은 전기 에너지를 열로 바꾸고, 그 비율은 흐르는 전류가 정한다. 저항의 전압과 전류 사이의 관계는 회로에서 가장 단순한 법칙이고, 아래의 모든 루프가 그것을 쓴다.

> **저항과 옴의 법칙의 정의.** **저항**(resistance)은 *두 단자 소자의 성질*로, 소자 양단의 전압과 소자를 지나는 전류의 비이며 단위는 옴이다. **옴의 법칙**(Ohm's law)은 이 비가 상수라는 주장이고, 소자를 *저항기*로 만드는 것이 바로 그 주장이다. 정의 조건 셋. **선형**이다. 전류를 두 배로 하면 어느 방향이든 전압이 두 배가 된다. [[02-foundations/engineering-math|0.5 §4.5]]의 뜻에서 가법성과 동차성이다. **기억이 없다**. 지금의 전압은 지금의 전류에만 달려 있고, 이것이 저항을 §4의 저장 소자와 가른다. 그리고 **온도가 고정된** 동안 성립한다. 금속의 저항은 $R=R_0(1+\alpha\,\Delta T)$로 오르고, 구리는 켈빈당 $\alpha=0.0039$이다(OpenStax). 값은 형상이 정한다. 비저항 $\rho$, 길이 $\ell$, 단면적 $A_c$인 도체는 $R=\rho\ell/A_c$이고, 구리는 $20\,^\circ\mathrm C$에서 $\rho=1.68\times10^{-8}\,\Omega{\cdot}\mathrm m$이다(OpenStax).
>
> $$v=R\,i,\qquad p=v\,i=i^2R=\frac{v^2}{R},\qquad R=\frac{\rho\,\ell}{A_c}$$
>
> 전력의 세 꼴은 §1의 $p=vi$에 $v=Ri$를 넣은 것이다. 그래서 저항이 흡수한 와트는 모두 열이 되어 나간다.
> - **예**: 권선, $R=1.0\,\Omega$. 밀기의 $2.0\,\mathrm A$에는 $2.0\,\mathrm V$가 들고 열 $4.0\,\mathrm W$가 난다. 같은 권선이 $60\,\mathrm K$ 뜨거워지면 $1.0\,(1+0.0039\cdot60)=1.234\,\Omega$이 되는데, [[04-robotics/actuators-drives|10.5 §6]]이 열 예산에 오르는 $R$을 넣는 이유다. $1.0\,\mathrm{mm^2}$ 구리선 $0.6\,\mathrm m$로 된 배터리 도선은 $1.68\times10^{-8}\cdot0.6/10^{-6}=10.1\,\mathrm{m\Omega}$이다. 구동계의 $10\,\mathrm A$에서 $0.10\,\mathrm V$가 떨어지고 $1.0\,\mathrm W$만큼 데워진다.
> - **비예**: 다이오드. 전류가 전압에 따라 지수적으로 커지므로, $I=I_0\big(e^{eV/k_BT}-1\big)$(OpenStax), 비 $v/i$ 하나로는 묘사되지 않는다. "다이오드의 저항"을 물으면 어느 전류에서 묻느냐에 따라 답이 달라진다. §6은 다이오드를 대신 한 방향 밸브로 쓴다.
> - **왜 중요한가**: 카트의 모든 손실은 $i^2R$에서 나온다. 권선, 도선, 스위치. 그리고 §3의 모든 식에 들어가는 소자 법칙이 $v=Ri$이다.

**직렬과 병렬.** 두 소자를 같은 전류가 반드시 모두 지나야 하면 *직렬*이다. 그러면 전압이 더해지므로 저항이 더해진다. 두 단자를 모두 공유하면 *병렬*이다. 그러면 한 전압에서 전류가 더해지므로 컨덕턴스 $1/R$이 더해진다(OpenStax).

$$R_{\text{series}}=R_1+R_2+\cdots,\qquad \frac{1}{R_{\text{parallel}}}=\frac{1}{R_1}+\frac{1}{R_2}+\cdots$$

직렬에서는 저항마다 공유하는 $i$에서 $iR_k$씩 떨어뜨리고, 병렬에서는 저항마다 공유하는 $v$에서 $v/R_k$씩 흘리기 때문이다. 로드셀의 브리지(§9)는 둘 다다. 한쪽 변은 $350\,\Omega$ 게이지 둘의 직렬로 $700\,\Omega$이고, 두 변은 $5.0\,\mathrm V$ 여기 전압에 병렬로 걸려 전체 $350\,\Omega$이다. 병렬 한 쌍은 언제나 어느 쪽 하나보다도 작다. 브리지는 $5.0/350=14.3\,\mathrm{mA}$를 끌어가고 $5.0^2/350=71\,\mathrm{mW}$를 열로 바꾸며, 게이지 하나에 $17.9\,\mathrm{mW}$씩이다. 흔한 게이지 저항 $120$, $350$, $1000\,\Omega$ 가운데 높은 쪽을 고르는 이유 가운데 하나가 이 자체 발열이다(Micro-Measurements). §6의 H-브리지에서는 모든 전류 경로가 스위치 둘을 직렬로 지나므로 $2R_{\text{on}}=20\,\mathrm{m\Omega}$이고, 밀기의 $2.0\,\mathrm A$에서 $2.0^2\cdot0.020=0.08\,\mathrm W$를 버린다. 권선의 $4.0\,\mathrm W$의 2퍼센트다.

### 3. 키르히호프 법칙, 분배기, 그리고 노드 해석 하나

*한 문장으로:* 전하는 모든 노드에서, 에너지는 모든 루프를 돌며 보존되고, 이 두 법칙이 §2의 $v=Ri$와 함께 어떤 저항 회로든 일차방정식으로 바꾸는데, 그 첫 교훈은 신호원을 충실히 읽으려면 거기서 거의 아무것도 끌어가지 않는 부하로 읽어야 한다는 것이다.

> **키르히호프 법칙의 정의.** **키르히호프 전류 법칙**(KCL)과 **전압 법칙**(KVL)은 *회로에 대해 쓴 보존 법칙 둘*이다. 소자가 무엇이든 성립하는, 망 전체에 관한 진술이다. 정의 조건 셋. **KCL**: 모든 노드에서 나가는 전류의 합은 0이다. 전하는 보존되고 노드는 전하를 쌓아 두지 않기 때문이다(OpenStax의 접합점 규칙). **KVL**: 모든 닫힌 루프를 돌며 전압의 합은 0이다. 루프를 한 바퀴 돈 1쿨롱은 출발할 때의 에너지를 그대로 가지고 돌아오기 때문이다(OpenStax의 고리 규칙). 그리고 회로는 **집중 정수**(lumped)여야 한다. 가장 빠른 신호의 파장보다 작아서 도선마다 전류 하나, 노드마다 전압 하나가 정해져야 한다. $20\,\mathrm{kHz}$의 전자기파는 길이가 $15\,\mathrm{km}$이니 카트는 한참 안쪽이지만, 변하는 자기 선속이 루프를 꿰는 곳에서는 KVL이 실제로 깨진다. §11의 접지 루프다.
>
> $$\sum_{\text{branches at a node}} i_k=0,\qquad \sum_{\text{elements around a loop}} v_k=0$$
>
> 전류는 모두 노드에서 나가는 쪽으로, 전압은 루프를 도는 방향으로 센다. 그래서 법칙 하나가 노드 하나나 루프 하나마다 식 하나다.
> - **예**: 켜짐 구간의 H-브리지(§6). 배터리, Q1, 권선, Q4를 도는 KVL은 $24=v_{Q1}+v_{\text{winding}}+v_{Q4}$를 주므로, $R_{\text{on}}$을 무시하면 권선이 $24\,\mathrm V$를 모두 받는다. 배터리 단자의 KCL을 $50\,\mu\mathrm s$ 한 주기에 걸쳐 평균하면, 그 단자는 시간의 $8.33\%$ 동안만 권선의 $2.0\,\mathrm A$를 나르고 나머지 동안은 아무것도 나르지 않으므로, 배터리 전류 $0.167\,\mathrm A$가 나온다.
> - **비예**: "모터가 일부를 쓰므로 모터에서 나오는 전류는 들어가는 전류보다 적다." KCL은 매 순간 둘이 같다고 말한다. 모터가 가져가는 것은 에너지이고, 그것은 전압으로 나타난다. 1쿨롱마다 두고 가는 줄이다(§1).
> - **왜 중요한가**: 모든 노드의 KCL과 모든 가지의 $v=Ri$가 직류 회로 해석의 전부다. 아래의 노드 해석은 미지 노드마다 KCL을 한 번씩 쓴 것일 뿐이다.

**분배기와 그 부하.** 신호원에 직렬로 건 저항 둘은 거의 모든 센서 판독이 적어도 한 번은 지나가는 회로다.

> **전압 분배기의 정의.** **전압 분배기**(voltage divider)는 *신호원에 직렬로 건 저항 한 쌍을 그중 하나의 양단에서 읽는 것*이고, 그 법칙은 **중점에서 아무것도 전류를 끌어가지 않을 때** 무엇을 내놓느냐에 관한 진술이다. 정의 조건 셋. 두 저항은 **같은 전류**를 흘린다. 직렬이고 출력이 전류를 가져가지 않기 때문이다. 그러면 출력은 신호원이 무엇이든 그것의 **비율** $R_2/(R_1+R_2)$이다. 그리고 **부하** $R_L$이 중점에서 전류를 끌어가는 순간 첫 조건이 깨지고 출력이 떨어진다. 떨어지는 비율은 정확히, 부하가 걸린 분배기가 무부하 출력 전압 뒤에 **출력 저항** $R_{\text{out}}=R_1\parallel R_2$을 둔 것처럼 행동하게 만드는 값이다.
>
> $$v_{\text{out}}=V\,\frac{R_2}{R_1+R_2},\qquad v_{\text{loaded}}=v_{\text{out}}\,\frac{R_L}{R_L+R_{\text{out}}},\qquad R_{\text{out}}=\frac{R_1R_2}{R_1+R_2}$$
>
> 중점의 KCL, $(V-v)/R_1=v/R_2+v/R_L$을 풀면 정확히 이 곱이 되기 때문이다. 두 꼴을 공통 분모 $R_1R_2+R_1R_L+R_2R_L$ 위로 풀어 써서 확인할 수 있다.
> - **예**: P6의 배터리 모니터, $100\,\mathrm{k\Omega}$ 위에 $15\,\mathrm{k\Omega}$. $24\,\mathrm V$ 배터리를 $3.130\,\mathrm V$로 만들어 ADC의 $4.096\,\mathrm V$ 범위(§10) 안에 넣고, 그 대가로 연결되어 있는 내내 배터리에서 $0.209\,\mathrm{mA}$, 곧 $5.0\,\mathrm{mW}$를 끌어간다.
> - **비예**: 같은 분배기를 입력 저항 $100\,\mathrm{k\Omega}$로 읽는 것. 출력 저항이 $13.0\,\mathrm{k\Omega}$이므로 읽은 값은 $2.769\,\mathrm V$로 $11.5\%$ 낮아지고, 무부하 비율을 가정한 펌웨어는 배터리를 $21.2\,\mathrm V$로 보고한다. "비율은 두 저항이 정한다"는 말은 무부하 분배기에만 맞다. 입력 저항이 $10\,\mathrm{M\Omega}$이면 $0.13\%$를 잃는다.
> - **왜 중요한가**: 모든 센서는 출력 저항을 가진 신호원이고 모든 입력은 부하이며, 잃는 신호의 비율은 대략 $R_{\text{out}}/R_L$이다. §8이 로드셀을 입력이 거의 아무것도 끌어가지 않는 증폭기로 읽는 이유다.

**노드 해석 하나: 부하가 걸린 로드셀 브리지.** §9의 브리지는 여기 전압 하나에 나란히 건 분배기 둘이고, 출력은 두 중점의 차이다. 그 출력에 부하 $R_L$ — 계측기든 증폭기의 입력이든 — 을 걸면 두 중점은 더 이상 서로 독립이 아니다. $R_L$을 거쳐 한쪽에서 다른 쪽으로 전류가 흐르므로, 분배기가 서로에게 부하가 된다. 노드 해석은 재주 없이 이것을 처리한다. 브리지의 바닥을 기준 노드로 잡고, 미지의 노드 전압 둘을 $v_A$, $v_B$로 부른 뒤, 각 노드에서 KCL을 쓴다. 저항을 지나 나가는 전류는 모두 (그 노드의 전압 빼기 반대쪽 끝의 전압) 나누기 저항이다.

$$\frac{v_A-V_{ex}}{R_1}+\frac{v_A}{R_2}+\frac{v_A-v_B}{R_L}=0,\qquad \frac{v_B-V_{ex}}{R_3}+\frac{v_B}{R_4}+\frac{v_B-v_A}{R_L}=0$$

그래서 부하가 걸린 브리지는 미지수 둘의 일차방정식 둘, [[02-foundations/engineering-math|0.5 §4]]처럼 푸는 $2\times2$ 연립이다. 밀기 중에 게이지는 저마다 $x=\Delta R/R=4\times10^{-4}$만큼 변해 있고, 한 대각선 쌍은 늘어나고 다른 쌍은 줄어든다(§9). 영어 절의 코드는 부하 다섯 가지에 대해 이 연립을 풀고 결과를 위의 분배기 규칙과 나란히 놓는다. 이때 $R_{\text{out}}$은 두 반쪽의 $R\parallel R$을 직렬로 이은 것이다.

| $R_L$ | $v_A$ (V) | $v_B$ (V) | $v_o$ (mV) | 잃은 비율 (%) | 분배기 규칙 (mV) |
|---:|---:|---:|---:|---:|---:|
| $10^3\,\Omega$ | 2.500741 | 2.499259 | 1.4815 | 25.9 | 1.4815 |
| $10^4\,\Omega$ | 2.500966 | 2.499034 | 1.9324 | 3.38 | 1.9324 |
| $10^5\,\Omega$ | 2.500997 | 2.499003 | 1.9930 | 0.349 | 1.9930 |
| $10^6\,\Omega$ | 2.501000 | 2.499000 | 1.9993 | 0.035 | 1.9993 |
| $10^9\,\Omega$ | 2.501000 | 2.499000 | 2.0000 | 3.5e-05 | 2.0000 |

무부하에서 브리지는 출력 저항 $350.00\,\Omega$ 뒤에서 $2.0000\,\mathrm{mV}$를 낸다. 부하를 걸면 노드 해석의 해와 한 줄짜리 규칙이 찍힌 자리까지 모두 일치하는데, 이 절의 실용적인 내용이 바로 그것이다. 출력 쪽에서 보면 브리지는 $350\,\Omega$ 뒤에 선 $2.0\,\mathrm{mV}$ 신호원 *그 자체*다. $10\,\mathrm{k\Omega}$ 계측기는 $3.4\%$ 낮게 읽고 $1\,\mathrm{k\Omega}$ 부하는 신호의 4분의 1을 잃지만, §8의 증폭기 입력 급인 $1\,\mathrm{G\Omega}$ 입력은 $3.5\times10^{-7}$만 잃는다.

### 4. 커패시터와 인덕터: 무엇을 저장하고, 무엇이 뛰지 못하는가

*한 문장으로:* 커패시터의 전압과 인덕터의 전류는 저장된 에너지이므로 어느 쪽도 순식간에 바뀌지 못하고, 이 사실 하나가 카트의 모든 시정수와 구동계의 모든 환류 경로를 정한다.

> **커패시터와 인덕터의 정의.** **커패시터**(capacitor)와 **인덕터**(inductor)는 *에너지를 저장하는 두 단자 소자*다. 커패시터는 두 도체 사이의 전기장에, 인덕터는 코일의 자기장에 저장하며, 각자 한 변수를 다른 변수의 변화율에 묶는 법칙으로 정의된다. 정의 조건 넷. 커패시터에서는 **전류가 전압의 변화율을 따른다**, $i=C\,dv/dt$, 커패시턴스 $C$는 상수이고 단위는 패럿이다. 인덕터에서는 **전압이 전류의 변화율을 따른다**, $v=L\,di/dt$, 인덕턴스 $L$은 상수이고 단위는 헨리이며, 유도된 전압은 변화에 맞선다. OpenStax가 $\varepsilon=-L\,dI/dt$로 쓰는 렌츠의 법칙이다. 둘 다 에너지를 **저장한다**, $\tfrac12Cv^2$와 $\tfrac12Li^2$(OpenStax). 이상적인 소자는 저장한 것을 모두 돌려준다. 그리고 그래서 둘 다 저장 변수가 **연속**이다. 커패시터의 전압이나 인덕터의 전류가 뛰면 저장된 에너지가 0초 만에 바뀌어야 하고, 그러려면 무한한 전력이 필요하다.
>
> $$i=C\,\frac{dv}{dt},\quad E_C=\tfrac12Cv^2;\qquad v=L\,\frac{di}{dt},\quad E_L=\tfrac12Li^2$$
>
> $v$와 $i$는 그 소자 자신의 전압과 전류다. 그래서 커패시터는 일정한 전압에서 전류를 흘리지 않고, 인덕터는 일정한 전류에서 전압을 떨어뜨리지 않으며, 둘 다 변화에만 맞선다.
> - **예**: 밀기의 $0.80\,\mathrm V$에서 필터 커패시터는 $\tfrac12\cdot10^{-6}\cdot0.80^2=0.32\,\mu\mathrm J$를 저장하고, $2.0\,\mathrm A$의 권선은 $\tfrac12\cdot10^{-3}\cdot2.0^2=2.0\,\mathrm{mJ}$로 그 6천 배를 저장한다. 권선의 전류를 $4.17\,\mu\mathrm s$ 동안 $0.092\,\mathrm A$ 올리려면 $L\,di/dt=10^{-3}\cdot0.092/(4.17\times10^{-6})=22\,\mathrm V$가 든다. 인덕터 쪽에서 본 §6의 리플이다.
> - **비예**: "스위치를 열면 모터 전류가 멈춘다." 한순간에는 멈추지 못한다. $2.0\,\mathrm A$를 $100\,\mathrm{ns}$ 만에 0으로 만들려면 $L\,di/dt=10^{-3}\cdot2.0/10^{-7}=20{,}000\,\mathrm V$가 필요하고, 그 전압은 회로를 끊은 것 — 스위치 — 의 양단에 나타나 무언가가 버티지 못할 때까지 남는데, 보통 버티지 못하는 것은 스위치다. §6은 그 대신 전류에 길을 준다.
> - **왜 중요한가**: 연속성은 이 페이지의 모든 과도 응답의 초기 조건이다. 커패시터는 있던 전압에서 시작하고, 인덕터는 첫 순간 전류를 그대로 지니며, 나머지는 회로의 시정수가 맡는다.

**역학으로 읽기.** 질량–스프링–댐퍼를 아는 독자는 이 소자들을 이미 안다. 전압을 힘으로, 전류를 속도 $u$로 읽으면 인덕터는 질량이다 — $F=m\,du/dt$에 맞서는 $v=L\,di/dt$이고, 질량이 $\tfrac12mu^2$를 저장하듯 $\tfrac12Li^2$를 저장한다. 저항은 댐퍼이고, 커패시터는 컴플라이언스가 $C$인 스프링이다. 그러면 전압 계단을 받은 권선 $L\,di/dt+Ri=v$는 댐퍼를 거스르며 밀리는 질량이고, 그 시정수 $L/R=1.0\,\mathrm{ms}$는 미끄러지는 질량의 $m/b$다. 연속성도 같게 읽힌다. 인덕터의 전류가 뛰지 못하는 것은 질량의 속도가 뛰지 못하는 것과 같은 이유이고, 그것을 한순간에 세우려면 질량을 한순간에 세울 때 무한한 힘이 들듯 무한한 전압이 든다.

저장 소자 하나와 저항이 있으면 회로는 1차이고, [[02-foundations/engineering-math|0.5 §8]]이 푸는 경우다. 필터 커패시터를 $R_f$를 거쳐 $V$로 계단처럼 뛰는 입력으로 충전해 보자. KVL은 $V=R_fi+v$를 주고 $i=C_f\,dv/dt$이므로

$$R_fC_f\,\frac{dv}{dt}+v=V\quad\Longrightarrow\quad v(t)=V\big(1-e^{-t/R_fC_f}\big)$$

이것이 $a=-1/(R_fC_f)$인 0.5 §8의 1차 방정식이고, 연속성이 요구하는 대로 $v(0)=0$에서 출발하기 때문이다. 전압 계단을 받은 권선도 역할만 바뀐 같은 방정식이다. $V=Ri+L\,di/dt$이므로 $i(t)=(V/R)\big(1-e^{-tR/L}\big)$이고, $i(0)=0$에서 출발한다.

> **시정수의 정의.** **시정수**(time constant) $\tau$는 *시간*이고, 1차 회로 — 저장 소자 하나와 저항, 일정하게 유지되는 전원 — 의 성질로서 그 회로가 한 정상 상태에서 다음 정상 상태로 얼마나 빨리 옮겨 가는지를 말한다. 정의 조건 셋. 회로가 **1차**여서 그 안의 모든 전압과 전류가 지수 함수 하나로 이완한다. $\tau$마다 **남은 간격의 $1-e^{-1}=63.2\%$를 메운다**(OpenStax). 간격이 얼마든 그렇다. 그리고 값은 **커패시터면 $RC$, 인덕터면 $L/R$이고**, $R$은 저장 소자가 보는 저항이다.
>
> $$x(t)=x_\infty+\big(x(0)-x_\infty\big)\,e^{-t/\tau},\qquad \tau=RC\quad\text{or}\quad\tau=\frac{L}{R}$$
>
> $x$는 회로 안의 아무 전압이나 전류, $x(0)$은 변화 직후의 값, $x_\infty$는 새 정상값이다. 그래서 숫자 하나가 회로의 모든 과도 응답의 시간을 재고, §1의 단위 확인에 따라 두 꼴의 $\tau$는 모두 시간이다.
> - **예**: 안티에일리어스 필터, $3.3\,\mathrm{k\Omega}\cdot1.0\,\mu\mathrm F=3.3\,\mathrm{ms}$. 계단 입력은 $3.3\,\mathrm{ms}$에 $63\%$, $\tau\ln10=7.6\,\mathrm{ms}$에 $90\%$, $\tau\ln100=15.2\,\mathrm{ms}$에 $99\%$에 닿는다. 권선의 $1.0\,\mathrm{mH}/1.0\,\Omega=1.0\,\mathrm{ms}$는 [[04-robotics/actuators-drives|10.5 §5]]의 전기적 시정수다.
> - **비예**: "시정수 하나가 지나면 필터는 끝난다." $\tau$ 뒤에도 $37\%$가 모자라고, 끝나는 일은 없다. 허용 오차를 먼저 정하면 시간은 따라 나온다. $1\%$ 안까지는 $4.6\tau$, $800$ 카운트짜리 계단에서 1카운트 안까지는 $\tau\ln800=6.7\tau$이다.
> - **왜 중요한가**: $\tau$는 카트의 다른 모든 시계와 견줄 숫자다. 권선의 $1.0\,\mathrm{ms}$에 대한 $50\,\mu\mathrm s$ PWM 주기(§6), 필터의 $3.3\,\mathrm{ms}$에 대한 $5\,\mathrm{ms}$ 제어 주기(§12).

### 5. RC 저역통과 필터

로드셀 신호는 스위칭 간섭과 공구의 진동을 얹은 채 ADC에 닿고, 샘플러는 그것을 잘못 읽는다. RC 필터가 빠른 부분을 걷어 내며, 이 절은 얼마나 걷어 내고 그 값이 얼마인지 말한다. 증폭기와 ADC 사이에 $R_f$가 직렬로, $C_f$가 접지로 들어가고, 출력은 $C_f$ 양단에서 뽑는다. 계단 응답은 §4가 주었다. 정현파에 대한 응답은 커패시터를 주파수에 따라 달라지는 저항처럼 다루면 나온다. [[02-foundations/engineering-math|0.5 §7]]의 회전하는 페이저 $v=Ve^{j\omega t}$로 구동하면 $i=C\,dv/dt=j\omega C\,v$이므로, 비 $v/i$는 복소 **임피던스** $Z_C=1/(j\omega C)$이다. §3의 분배기에서 $R_2$ 자리에 $Z_C$를 넣으면 필터의 주파수 응답이 나온다.

$$H(j\omega)=\frac{Z_C}{R_f+Z_C}=\frac{1}{1+j\omega R_fC_f}$$

ADC가 전류를 끌어가지 않으면 $R_f$와 $C_f$에 같은 전류가 흐르기 때문이다. 이것은 [[02-foundations/engineering-math|0.5 §9]]의 전달함수 $1/(1+sR_fC_f)$에 $s=j\omega$를 넣은 것으로, 극점이 $s=-1/(R_fC_f)=-303\,\mathrm{s^{-1}}$ 하나다. 그 절의 예 $1/(s+3)$과 같은 단극 저역통과이고, 극점만 $3$에서 $303$으로 옮겼다.

> **차단 주파수의 정의.** 저역통과 필터의 **차단 주파수**(cutoff frequency) $f_c$는 *주파수*이고 필터의 성질이다. 이득이 저주파 값의 $1/\sqrt2$, 곧 $-3\,\mathrm{dB}$로 떨어져 전력의 절반만 통과시키는 주파수다. 정의 조건 셋. **정상 상태의 정현파**, 곧 §4의 과도 응답이 사라진 뒤에 대해 정의한다. 1차 RC에서는 그러면 이득과 위상이 모든 주파수에서 **식 하나**를 따르므로 $f_c$가 응답 전체를 정한다. 그리고 그 식은 필터를 **낮은 출력 저항이 구동하고 높은 입력 저항이 읽을 때만** 성립한다. 그렇지 않으면 신호원이 $R_f$에 더해지고 부하가 제 나름의 분배기가 되어 차단 주파수가 움직인다(§3).
>
> $$f_c=\frac{1}{2\pi R_fC_f},\qquad \lvert H(f)\rvert=\frac{1}{\sqrt{1+(f/f_c)^2}},\qquad \angle H(f)=-\arctan\frac{f}{f_c}$$
>
> $\omega R_fC_f=f/f_c$이므로 이것은 $1/(1+j\,f/f_c)$의 크기와 각이다. 그래서 $f=f_c$에서 이득은 $1/\sqrt2=0.707$, 위상은 $-45^\circ$이다.
> - **예**: $3.3\,\mathrm{k\Omega}$와 $1.0\,\mu\mathrm F$는 $f_c=48.2\,\mathrm{Hz}$를 준다. 영어 절의 코드는 P6이 필요로 하는 곳에서 이것을 계산한다. 밀기의 느린 변화는 온전히 지나가고, ADC의 나이퀴스트 주파수 $100\,\mathrm{Hz}$는 $0.434$로, PWM의 $20\,\mathrm{kHz}$는 $0.00241$로 지나간다.
> - **비예**: "차단 주파수 위로는 아무것도 지나가지 않는다." 차단 주파수의 두 배에서도 $1/\sqrt5\approx45\%$가 지나간다. 1차 필터는 $f_c$보다 한참 위에서 $f_c/f$로만 떨어진다. 10배마다 10분의 1, 곧 디케이드당 $-20\,\mathrm{dB}$이고, 표에서 $1\,\mathrm{kHz}$의 $0.0482$는 세 자리까지 $48.2/1000$이다.
> - **왜 중요한가**: 숫자 하나가 필터가 무엇을 걷어 내는지, 그리고 위상을 통해 지연으로 무엇을 치르는지를 말해 준다. $f_c$보다 한참 아래에서 위상은 약 $-2\pi f\tau$이고, 이것은 순수한 지연 $\tau=3.3\,\mathrm{ms}$로서 제어기가 쓰는 모든 힘 판독에 더해진다.

| $f$ (Hz) | $\lvert H\rvert$ | 이득 (dB) | 위상 (°) | P6에서 그 자리에 있는 것 |
|---:|---:|---:|---:|---|
| 1.00 | 0.99979 | −0.002 | −1.19 | 밀기의 느린 변화 |
| 10.00 | 0.97917 | −0.183 | −11.71 | |
| 48.23 | 0.70711 | −3.010 | −45.00 | 차단 주파수 |
| 100.00 | 0.43441 | −7.242 | −64.25 | $200\,\mathrm{Hz}$ ADC의 나이퀴스트 주파수 |
| 1000.00 | 0.04817 | −26.344 | −87.24 | |
| 20000.00 | 0.00241 | −52.355 | −89.86 | PWM |

표를 세 가지로 읽는다. $1\,\mathrm{Hz}$의 위상 $-1.19^\circ$는 1초의 $1.19/360$, 곧 $3.30\,\mathrm{ms}$로 상자가 예측한 지연 $\tau$ 그대로이고, $10\,\mathrm{Hz}$에서도 여전히 $3.25\,\mathrm{ms}$이다. $100\,\mathrm{Hz}$ 행은 RC 하나가 못 하는 일을 보여 준다. ADC의 나이퀴스트 주파수보다 높은 성분은 판독 속으로 접혀 들어오고(§10), 그것을 막을 만큼 낮은 1차 필터는 밀기를 제어 주기 하나보다 훨씬 길게 늦춘다. 그 맞바꿈을 재는 것이 §12이고, 그것을 덜어 주는 더 가파른 필터는 [[02-foundations/signal-processing|6. 신호처리 §4]]의 주제다. 그리고 $T$마다 샘플하면 RC의 계단 응답은 샘플마다 남은 간격을 $\alpha=e^{-T/\tau}$배로 줄인다. P6의 $5\,\mathrm{ms}$에서는 $e^{-5/3.3}=0.220$이다. 6. §4가 $y[n]=\alpha\,y[n-1]+(1-\alpha)\,x[n]$으로 쓰는 지수 평활기는 이 회로를 코드로 쓴 것이다.

### 6. 스위치: 다이오드, MOSFET, PWM, H-브리지

*한 문장으로:* 구동계는 $2.0\,\mathrm V$를 만드는 일이 없다. $24\,\mathrm V$ 전체를 1초에 2만 번 켰다 껐다 하고, 권선의 인덕턴스가 그 펄스를 거의 한결같은 전류로 평균하며, 스위치가 열릴 때마다 다이오드나 켜 둔 트랜지스터가 그 전류를 이어 나른다.

**두 가지 스위치.** **다이오드**(diode)는 전류의 한 방향 밸브다(OpenStax, Toshiba). 순방향에서 전류는 $I_0(e^{eV/k_BT}-1)$로 커지므로, $300\,\mathrm K$에서 전류를 10배 늘리는 데 드는 전압은 $(k_BT/e)\ln10=0.0259\times2.303=59.5\,\mathrm{mV}$뿐이다. $k_B$와 $e$는 SI의 정확한 상수다(NIST). 그래서 회로가 쓰는 전류 범위에서 도통 중인 실리콘 다이오드는 거의 고정된 전압 강하처럼 행동하고, 이 페이지는 그것을 강의용 숫자 $V_F=0.7\,\mathrm V$로 둔다. 역방향이면 막는다. **MOSFET**은 전압으로 여닫는 스위치다. 게이트–소스 전압이 문턱을 넘으면 드레인과 소스 사이에 도통 채널이 생겨 스위치가 켜지고, 작은 저항 $R_{DS(\text{on})}=V_{DS}/I_D$를 가진다. 제조사는 이 값을 정해진 게이트 전압에서 적는다(Toshiba). 여기서는 $10\,\mathrm{m\Omega}$이다. 게이트 전압을 빼면 꺼진다. 전력용 MOSFET은 소스와 드레인 사이에 다이오드도 품고 있고, 데이터시트는 그 다이오드의 전류와 순방향 전압을 따로 적는다(Toshiba). 아래 브리지에서 그 다이오드들은 모두 낮은 레일에서 높은 레일 쪽을 향한다.

스위치는 어느 상태에서든 거의 버리지 않는다. 켜지면 아주 작은 $R_{\text{on}}$에서 $i^2R_{\text{on}}$, 꺼지면 전류가 아예 없다. 구동계가 스위칭을 하는 이유가 이것 하나다. 대안, 곧 트랜지스터를 모터와 직렬로 둔 가변 저항처럼 쓰는 방식은 원치 않는 $22\,\mathrm V$를 $2.0\,\mathrm A$에서 떨어뜨려 밀기의 $4.0\,\mathrm W$를 내려고 $44\,\mathrm W$를 태운다.

> **PWM의 정의.** **펄스 폭 변조**(PWM)는 *고정된 전원에서 스위칭으로 조절 가능한 평균 전압을 만드는 방법*이고, 숫자 둘로 정해진다. 스위칭 주기 $T$(곧 주파수 $f=1/T$), 그리고 주기 가운데 전원이 연결된 비율인 **듀티비** $D$다. 정의 조건 셋. 부하는 **두 레벨**을 본다. 이 페이지가 쓰는 방식에서는 $DT$ 동안 $V_s$, $(1-D)T$ 동안 $0$이다. **평균**은 듀티비만이 정한다, $\bar v=DV_s$. 그리고 부하가 펄스를 **걸러야** 한다. 주기가 부하 자신의 시정수보다 짧아서, $T\ll L/R$, 전류가 평균을 따라가고 그 둘레에서 조금만 출렁여야 한다.
>
> $$\bar v=D\,V_s,\qquad \Delta i_{pp}\approx\frac{V_s\,D\,(1-D)}{L\,f}$$
>
> 켜짐 구간 동안 인덕턴스는 $V_s$에서 자신이 유지하고 있는 평균을 뺀 만큼, $L\,di/dt\approx V_s-\bar v=(1-D)V_s$를 $DT$ 동안 보기 때문이다. 그래서 리플은 전원, 듀티비, $L$, $f$에 달려 있고 부하 전류나 역기전력에는 달려 있지 않다.
> - **예**: 밀기. $\bar v=2.0\,\mathrm V$에는 $D=2.0/24=8.33\%$가 필요하다. $50\,\mu\mathrm s$마다 $4.17\,\mu\mathrm s$ 켜진다. 전류는 $24\cdot0.0833\cdot0.917/(10^{-3}\cdot20{,}000)=0.0917\,\mathrm A$ 피크–피크로 출렁이고, $2.0\,\mathrm A$의 $4.6\%$다. 정지 상태에서 이 비율은 $(1-D)\,T/\tau_e$, 곧 권선의 시정수에 대한 주기의 비다.
> - **비예**: "듀티비가 힘을 정한다." [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]]이 제목에 적어 둔 경고다. 듀티비가 정하는 것은 평균 *전압*이고, 전류와 그래서 힘은 $\bar v=Ri+e$(§7)에서 따라 나온다. 정지 상태에서 $10\,\mathrm N$ 밀기를 유지하는 바로 그 $8.33\%$를, 카트가 역기전력 $2.5\,\mathrm V$를 가지고 $0.5\,\mathrm{m/s}$로 순항할 때 걸면 $i=(2.0-2.5)/1.0=-0.5\,\mathrm A$가 된다. 모터가 카트를 제동하고 배터리를 충전한다.
> - **왜 중요한가**: 전기 구동계가 거의 아무것도 버리지 않으면서 배터리를 조절 가능한 전압으로 바꾸는 방법이 이것이고, 그 주파수는 맞바꿈이다. 리플은 $1/f$로 줄고(§12), 스위칭 에지마다 약간의 에너지가 들어서 스위치 손실은 $f$와 함께 늘며, 약 $20\,\mathrm{kHz}$ 아래에서는 권선이 사람이 듣는 음높이로 운다. 정상 청력의 범위는 $20\,\mathrm{Hz}$에서 $20\,\mathrm{kHz}$이기 때문이다(OpenStax).

**H-브리지.** 스위치 하나로도 모터를 전원에 이을 수 있다. 밀기*와* 당기기를 모두 하려면 넷이 필요하다.

> **H-브리지와 환류 경로의 정의.** **H-브리지**(H-bridge)는 *스위치 넷으로 된 회로*다. 전원 양단에 다리 둘을 두고, 다리마다 하이사이드와 로우사이드 스위치가 하나씩 있으며, 부하는 두 다리의 중점 사이에 H의 가로대처럼 놓인다. 부하 양단에 $+V_s$, $-V_s$, $0$을 걸 수 있고, 유도성 부하라면 그 전류에 **환류 경로**(freewheeling path) — 스위치가 열릴 때 갈 곳 — 도 주어야 한다. 정의 조건 셋. **대각선 쌍**이 구동한다. Q1과 Q4는 부하에 $+V_s$를, Q2와 Q3는 $-V_s$를 건다. **한 다리의 두 스위치는 절대 동시에** 켜지지 않는다. 켜지면 전원이 $2R_{\text{on}}$을 통해 단락되므로, 제어기는 한쪽을 끄고 다른 쪽을 켜기 사이에 짧은 *데드 타임*을 둔다. 그리고 **모든 스위치에 다이오드가 병렬로** 붙어 양의 레일 쪽을 향한다. 그래서 스위치가 유도성 전류를 끊으면 그 전류는 같은 다리의 다른 스위치에 붙은 다이오드를 지나 계속 흐른다. 또는 데드 타임 뒤에 켠 그 스위치 자체를 지나 흐르는데, 이것을 동기 환류라고 부른다.
>
> $$v_{\text{load}}\in\{+V_s,\ 0,\ -V_s\},\qquad \text{while freewheeling:}\quad L\,\frac{di}{dt}=-\big(R\,i+e+v_{\text{path}}\big)$$
>
> $e$는 모터의 역기전력(§7), $v_{\text{path}}$는 환류 경로의 전압 강하다. $2.0\,\mathrm A$에서 켜 둔 MOSFET 둘을 지나면 $2iR_{\text{on}}=0.04\,\mathrm V$이고, 그중 하나를 다이오드로 지나면 약 $V_F=0.7\,\mathrm V$가 더해진다. 그래서 전류는 억지로 0이 되지 않고 경로를 지나며 천천히 줄어든다.
> - **예**: 페이지 맨 위에 그린 밀기. 켜짐 구간: Q1과 Q4가 권선에 $+24\,\mathrm V$를 걸고 전류는 배터리에서 온다. 꺼짐 구간: Q1이 열리고 Q4는 켜진 채로 있으며 Q2가 데드 타임 뒤에 켜진다. 그래서 권선의 $2.0\,\mathrm A$는 양단에 거의 전압 없이 Q2와 Q4를 돌고, Q1이 다시 닫히기 전 $45.8\,\mu\mathrm s$ 동안 $0.0917\,\mathrm A$밖에 줄지 않는다. 그 구간이 $\tau_e$의 $4.6\%$이기 때문이다. 반대로 관통 단락(shoot-through), 곧 Q1과 Q2가 함께 켜지면 $20\,\mathrm{m\Omega}$ 양단에 $24\,\mathrm V$가 걸려 $1200\,\mathrm A$를 요구한다.
> - **비예**: 모터와 직렬로 트랜지스터 하나만 두고 다이오드는 없는 회로. 처음 시도할 때 흔히 쓰는 회로다. 모터를 켤 수는 있지만, $2.0\,\mathrm A$에서 $100\,\mathrm{ns}$ 만에 열면 $20{,}000\,\mathrm V$를 요구하고(§4), 그 전압을 가장 먼저 맞는 것이 트랜지스터다.
> - **왜 중요한가**: 인덕터를 스위칭하고도 살아남게 해 주는 것이 환류 경로이고, 바깥에서 돌려진 모터가 전류를 전원 쪽으로 되돌려 보내는 길도 같은 다이오드다. [[04-robotics/actuators-drives|10.5 §7]]의 단락 권선 제동 밑에 있는 물리가 이것이다.

구동계가 환류 전류를 다이오드에 맡기지 않고 환류용 트랜지스터를 켜 두는 이유는 와트의 문제다. 아래 상자가 그 값을 매긴다.

> [!note]- 더 깊이 · Deeper
> **환류 경로에 다이오드냐 스위치냐.** 꺼짐 구간의 전류가 켜 둔 Q2가 아니라 Q2의 다이오드를 지나면, 권선은 각 주기의 $91\%$ 동안 $0$이 아니라 $-0.7\,\mathrm V$를 본다. 그러면 $2.0\,\mathrm A$를 유지하는 데 $DV_s-(1-D)V_F=Ri$가 필요해서 $D=(2.0+0.7)/(24+0.7)=10.9\%$가 되고($8.33\%$ 대신), 다이오드는 $V_Fi(1-D)=0.7\cdot2.0\cdot0.891=1.25\,\mathrm W$를 소산한다. 켜 둔 Q2라면 $i^2R_{\text{on}}(1-D)=0.037\,\mathrm W$다. 구동계가 환류용 트랜지스터를 켜 두는 이유가 이것이다.

### 7. 회로 소자로서의 DC 모터

힘을 명령하려면 그 힘에 드는 전류, 전압, 듀티비를 알아야 하고, 그것들이 나오는 곳이 모터의 회로 방정식이다. 두 단자에서 보면 모터는 §2의 저항, §4의 인덕터, 전압원 하나를 직렬로 이은 것이다. 권선의 $R$과 $L$, 그리고 도는 회전자가 권선에 유도하는 **역기전력**(back-EMF) $e=k_e\omega_m$으로, 모터를 앞으로 돌리는 전류에 맞선다. 모터를 한 바퀴 도는 KVL이 모터의 전기 방정식 하나를 주고, 토크는 전류에 비례한다.

$$v=R\,i+L\,\frac{di}{dt}+k_e\,\omega_m,\qquad \tau_m=k_t\,i$$

단자 전압이 갈 곳은 셋 — 저항, 인덕턴스 속에서 변하는 전류, 역기전력 — 이고, 자석이 암페어마다 $k_t$ 뉴턴미터를 만들기 때문이다. [[04-robotics/actuators-drives|10.5 §1]]은 $k_t$와 $k_e$를 정의하고 SI 단위에서 둘이 같은 숫자임을 보인다. 권선이 역기전력에 맞서 내놓는 전기 일률 $e\,i$가 회전자가 만드는 기계 일률 $\tau_m\omega_m$이기 때문이다. 이 페이지는 그 결과를 쓴다. P6에서 벨트 풀리는 양방향으로 바꿔 준다. 모터 토크 $\tau_m$은 카트를 $F=\tau_m/r_p$로 밀고, 카트 속도 $v_c$는 모터를 $\omega_m=v_c/r_p$로 돌린다. 그래서

$$F=\frac{k_t}{r_p}\,i=5.0\,\mathrm{\tfrac{N}{A}}\cdot i,\qquad e=\frac{k_e}{r_p}\,v_c=5.0\,\mathrm{\tfrac{V}{m/s}}\cdot v_c$$

두 경우 모두 $0.10/0.020=5.0$이기 때문이다. 카트의 운전점 셋, 저마다 이 식의 한 줄이다.

- **정지 상태의 밀기.** $\omega_m=0$이고 전류가 일정하므로 $v=Ri$이다. $10\,\mathrm N$에는 $2.0\,\mathrm A$와 $2.0\,\mathrm V$가 들고, 아무것도 움직이지 않으니 $4.0\,\mathrm W$는 모두 열이 된다. 이것이 계산 절이다.
- **$2.0\,\mathrm N$의 구름 저항을 이기며 $0.5\,\mathrm{m/s}$로 순항.** 모터는 $25\,\mathrm{rad/s}$($239\,\mathrm{rpm}$)로 돌고 역기전력은 $2.5\,\mathrm V$이다. 힘에는 $0.40\,\mathrm A$가 필요하므로 $v=0.40+2.5=2.9\,\mathrm V$, $D=12.1\%$이다. 전력 장부가 맞아떨어진다. 구동계가 내는 $2.9\cdot0.40=1.16\,\mathrm W$ 가운데 $0.40^2\cdot1.0=0.16\,\mathrm W$는 권선을 데우고, $e\,i=2.5\cdot0.40=1.0\,\mathrm W$는 역기전력을 건너간다. 카트가 구름 저항에 쓰는 $F\,v_c=2.0\cdot0.5=1.0\,\mathrm W$와 정확히 같다. 전기 일률의 $86\%$가 운동이 되고, 배터리는 $0.121\cdot0.40=0.048\,\mathrm A$를 낸다.
- **전체 전원에서의 정지(stall).** $\omega_m=0$에서 $24\,\mathrm V$를 걸면 $24/1.0=24\,\mathrm A$가 흐르려 하지만, 구동계가 허락하지 않는다. 듀티비를 낮춰 전류를 $10\,\mathrm A$ 한계에 붙잡으므로([[04-robotics/actuators-drives|10.5 §3]]), 카트가 낼 수 있는 가장 센 밀기는 $5.0\cdot10=50\,\mathrm N$이다. 권선은 그것도 오래 버티지 못한다. [[04-robotics/actuators-drives|10.5 §6]]의 열 예산은 연속 $3.16\,\mathrm A$, 곧 $15.8\,\mathrm N$ 밀기만 허락하므로, $10\,\mathrm N$ 밀기는 무기한 이어질 수 있지만 $50\,\mathrm N$은 몇 초뿐이다. 모터를 10.5가 가정한 대로 식힌다면 그렇다.

같은 식에서 따라 나오는 것이 둘 더 있다. 구동계가 속도에 쓸 수 있는 전압은 $Ri$를 빼고 남은 것이다. $24\,\mathrm V$에서 무부하 모터의 최고 속도는 $V_s/k_e=240\,\mathrm{rad/s}$, 카트 속도로 $4.8\,\mathrm{m/s}$이고, 토크–속도 선 전체는 10.5 §3이 그린다. 그리고 인덕턴스 때문에 전류는 천천히 바뀐다. 전압 계단 뒤 전류는 $\tau_e=1.0\,\mathrm{ms}$에 새 값까지의 $63\%$를 간다. 구동계가 전류에 빠른 루프를 닫고 제어기가 전압이 아니라 전류를 요청하는 이유가 이것이다([[04-robotics/actuators-drives|10.5 §5]]). $20\,\mathrm{kHz}$에서 그 전류 루프는 PWM을 매끈한 전압으로 본다. 스위칭 주기가 $\tau_e$의 20분의 1이기 때문이다.

### 8. 연산 증폭기: 규칙 둘과 증폭기 셋

로드셀의 신호는 $2.0\,\mathrm{mV}$이고 ADC의 한 계단은 $1.0\,\mathrm{mV}$(§10)이므로, 신호를 읽기 전에 수백 배로 키워야 한다. 그 일을 하는 부품이 연산 증폭기이고, 그것으로 만든 회로 셋이 로봇의 거의 모든 센서를 감당한다.

> **이상적 연산 증폭기의 정의.** **연산 증폭기**(operational amplifier)는 *이득이 엄청나게 큰 차동 증폭기*다. 출력 전압은 두 입력의 차이에 이득 $A$를 곱한 것이고, 입력은 전류를 거의 끌어가지 않는다. **이상적 연산 증폭기**(ideal op-amp)는 $A$를 무한대로 보낸 모델이고, 그 규칙 둘은 이 모델이 **음되먹임 회로 안에서** 뜻하는 것이다. 정의 조건 셋. 출력은 $v_{\text{out}}=A(v_+-v_-)$이고 $A$는 아주 크다. 여기서는 $10^5$으로, Toshiba의 강의 자료가 쓰는 크기다. **입력은 전류를 끌어가지 않는다**. 그리고 **음되먹임**이 출력의 일부를 $-$ 입력으로 되돌려, 회로는 $v_+-v_-=v_{\text{out}}/A$, 거의 0인 곳에 자리 잡는다. 두 입력이 이어져 있지 않은데도 거의 같은 전압에 있는 것이고, 이것을 **가상 단락**(virtual short)이라 부른다(Toshiba). 출력이 전원 범위 안에 머무는 동안에 한해서다.
>
> $$v_{\text{out}}=A\,(v_+-v_-)\quad\Longrightarrow\quad v_+-v_-=\frac{v_{\text{out}}}{A}\;\approx\;0,\qquad i_+=i_-\approx0$$
>
> 유한한 출력을 엄청난 이득으로 나누면 입력 차이가 거의 남지 않기 때문이다. 이것이 규칙 둘, *입력 사이에 전압이 없고 입력으로 전류가 들어가지 않는다*이고, 아래의 모든 회로는 이 규칙으로 $-$ 입력에서 KCL을 써서 푼다.
> - **예**: 밀기의 $0.80\,\mathrm V$를 내는 이득 $400$짜리 증폭기는 연산 증폭기 입력 사이에 $0.80/10^5=8\,\mu\mathrm V$만 있으면 된다. 증폭하는 $2.0\,\mathrm{mV}$에 대면 $0.4\%$이고, 아래의 이득 오차와 같은 $0.4\%$이다. $A$가 유한한 값을 치르는 것이다.
> - **비예**: 되먹임이 없는 연산 증폭기. 브리지의 $2.0\,\mathrm{mV}$에 $10^5$을 곱하면 $200\,\mathrm V$를 요구하고, 출력은 전원에 부딪히며, 어느 규칙도 성립하지 않는다. 그렇게 쓰면 비교기, 곧 1비트 ADC다. 또 가상 단락은 진짜 단락이 아니다. 두 입력 사이로 전류는 흐르지 않는다.
> - **왜 중요한가**: 규칙 둘만 있으면 증폭기 설계가 KCL 두 줄이 되고, 이득은 들쭉날쭉한 $A$가 아니라 저항의 비가 정한다.

**반전 증폭기.** $v_+$를 접지하면 가상 단락이 $v_-$도 $0\,\mathrm V$에 둔다. 연산 증폭기로 들어가는 전류가 없으니, $v_-$에서의 KCL은 $R_{\text{in}}$으로 들어온 전류가 되먹임 저항 $R_{\text{fb}}$로 나간다고 말한다. $v_{\text{in}}/R_{\text{in}}+v_{\text{out}}/R_{\text{fb}}=0$이므로 $v_{\text{out}}=-(R_{\text{fb}}/R_{\text{in}})\,v_{\text{in}}$이다. 입력 저항은 $R_{\text{in}}$으로, §3의 뜻에서 부하다.

**비반전 증폭기.** $v_{\text{in}}$을 $v_+$에 넣고, $v_-$는 출력 양단에 건 분배기($R_{\text{fb}}$ 위에 $R_g$)에서 받는다. 가상 단락이 분배기의 출력을 $v_{\text{in}}$과 같게 만드므로, $v_{\text{out}}R_g/(R_g+R_{\text{fb}})=v_{\text{in}}$이고

$$G=\frac{v_{\text{out}}}{v_{\text{in}}}=1+\frac{R_{\text{fb}}}{R_g},\qquad G_{\text{actual}}=\frac{G}{1+G/A}$$

그리고 $v_+$는 전류를 끌어가지 않으므로, 이 증폭기는 신호원에 거의 부하를 주지 않는다. 둘째 꼴은 $A$를 유한하게 둔 것이다. $G=400$이면 $398.4$로 $0.40\%$ 낮다. 알려진 하중으로 교정하면 없어지는 이득 오차다.

**계장 증폭기, 한 문단으로.** 브리지의 두 출력은 $2.501\,\mathrm V$와 $2.499\,\mathrm V$에 있다. 읽을 가치가 있는 $2.0\,\mathrm{mV}$는 둘에 공통인 $2.5\,\mathrm V$ 위에 얹혀 있다. 어느 한 출력에 이득 $400$짜리 비반전 증폭기를 걸면 $1000\,\mathrm V$에 닿으려 할 것이다. 계장 증폭기는 차이만 키운다. 첫 단은 비반전 증폭기 둘이 두 $-$ 입력 사이에 이득 저항 $R_G$ 하나를 나눠 쓰는 구조다. 가상 단락이 $v_A$와 $v_B$를 $R_G$의 두 끝에 복사하고, 어느 연산 증폭기 입력도 전류를 가져가지 않으므로 전류 $(v_A-v_B)/R_G$는 두 되먹임 저항 $R_{\text{fb}}$를 그대로 지나야 한다. 그래서 첫 단의 두 출력은 $(v_A-v_B)(1+2R_{\text{fb}}/R_G)$만큼 차이 나고, 공통의 $2.5\,\mathrm V$는 이득 1로 그냥 지나간다. 둘째 단은 이득 1의 차동 증폭기로 두 출력을 빼면서 공통 부분도 함께 뺀다. $R_{\text{fb}}=20\,\mathrm{k\Omega}$이면 $G=400$에 $R_G=2R_{\text{fb}}/(G-1)=100.25\,\Omega$이 필요하고, 밀기 중에 첫 단은 $2.900\,\mathrm V$와 $2.100\,\mathrm V$를, 둘째 단은 $0.800\,\mathrm V$를 낸다. 브리지의 두 선은 모두 전류를 거의 끌어가지 않는 연산 증폭기 입력에 닿으므로 브리지에는 부하가 걸리지 않는다(§3 표의 $1\,\mathrm{G\Omega}$ 행). 공통의 $2.5\,\mathrm V$가 얼마나 완전히 빠지는지는 둘째 단 저항들이 얼마나 잘 맞느냐에 달려 있고, 계장 증폭기의 데이터시트는 그것을 동상 제거비(common-mode rejection)로 적는다.

### 9. 휘트스톤 브리지와 스트레인 게이지 로드셀

힘 센서는 뉴턴을 볼트로 바꿔야 하고, 스트레인 게이지는 그 일을 직접 재기에는 너무 작은 저항 변화로 한다. 브리지가 푸는 문제가 그것이다. **스트레인 게이지**(strain gauge)는 휘는 부품에 붙인 얇은 금속 포일 저항이다. 부품이 늘어나면 포일이 길고 가늘어져 §2의 $R=\rho\ell/A_c$에 따라 저항이 오르고, 눌리면 내린다. 변화율은 변형률 $\varepsilon$, 곧 늘어난 비율에 비례하고, 비례 상수인 **게이지율**(gauge factor) $K$는 포일 게이지에서 명목상 $2$이다(Micro-Measurements).

$$\frac{\Delta R}{R}=K\,\varepsilon$$

그래서 $1000$ 마이크로스트레인, $\varepsilon=10^{-3}$만큼 변형된 게이지는 $0.2\%$ 변한다. **로드셀**(load cell)은 이런 게이지 넷을 붙인 가공된 탄성체로, 힘이 둘을 늘이고 나머지 둘을 누르도록 배치되어 있다. P6의 로드셀에서 정격 $50\,\mathrm N$은 게이지를 $1000\,\mu\varepsilon$만큼 변형시키므로, $350\,\Omega$ 게이지 하나가 $0.70\,\Omega$ 움직인다. 밀기의 $10\,\mathrm N$은 $0.14\,\Omega$, 1뉴턴은 $14\,\mathrm{m\Omega}$, 10만분의 4다. 이것을 저항으로 재려면 $4\times10^{-5}$까지 맞는 저항계가 필요하다. 브리지는 그 대신 변화를 잰다.

> **휘트스톤 브리지의 정의.** **휘트스톤 브리지**(Wheatstone bridge)는 *저항 넷으로 된 회로* — 여기 전압 하나에 건 전압 분배기 둘로, 출력은 두 중점 사이에서 뽑는다 — 이고, **균형일 때 0**을 내고 균형이 깨지면 **작은 저항 변화에 비례하는** 전압을 낸다. 정의 조건 넷. 두 분배기는 **같은 여기 전압** $V_{ex}$에 걸려 있어서, 그 값이 출력에 곱해진다. 출력은 **두 분배비의 차이**이고, $R_2/R_1=R_4/R_3$이면 0이다. 팔들이 작은 비율 $\pm x$만큼 변하면 출력은 **변화에 선형**이다. 네 팔이 반대 쌍으로 변하는 풀 브리지에서는 정확히 $V_{ex}x$이고, 능동 팔이 하나뿐인 쿼터 브리지에서는 약 $V_{ex}x/4$이다. Micro-Measurements는 둘을 능동 팔 $N$개에 대해 $V_{ex}K\varepsilon N/4$로 함께 쓴다. 그리고 **부하 없이 읽어야** 한다. 출력 저항이 대략 팔 하나의 $R$이기 때문이다(§3의 표).
>
> $$v_o=V_{ex}\Big(\frac{R_2}{R_1+R_2}-\frac{R_4}{R_3+R_4}\Big)=V_{ex}\,\frac{N}{4}\,K\,\varepsilon\quad(N=4,\ \text{full bridge})$$
>
> $R_1=R_4=R(1-x)$, $R_2=R_3=R(1+x)$이면 첫 비는 $(1+x)/2$, 둘째 비는 $(1-x)/2$이므로 아무것도 버리지 않고 $v_o=V_{ex}x=V_{ex}K\varepsilon$이기 때문이다. 쿼터 브리지의 $V_{ex}x/(2(2+x))$는 $x$가 작을 때만 같은 법칙이다.
> - **예**: 밀기 중의 P6 로드셀. $x=K\varepsilon=4\times10^{-4}$이므로 $v_o=5.0\cdot4\times10^{-4}=2.0\,\mathrm{mV}$이고, 두 출력 단자 모두에서 $2.5\,\mathrm V$ 위에 얹혀 있다.
> - **비예**: 데워지는 부품 위, 쿼터 브리지 속의 능동 게이지 하나. 포일의 저항은 온도에 따라서도 변하므로 데워진 게이지 하나는 변형으로 읽힌다. 풀 브리지에서는 네 팔에 공통인 변화 — 모든 팔에 $(1+\delta)$를 곱하는 것 — 가 두 분배비를, 그래서 출력을 정확히 그대로 둔다. 한 탄성체 위에 나란히 붙은 게이지 넷은 함께 겪는 온기를 상쇄하고, 로드셀을 풀 브리지로 짓는 이유 가운데 하나가 이것이다.
> - **왜 중요한가**: 브리지는 재기에 너무 작은 저항 변화를 0에서 출발하는 전압으로 바꾸어, 증폭기가 그 변화가 얹힌 $350\,\Omega$은 키우지 않고 변화만 키울 수 있게 한다.

**mV/V로 적는 정격 출력.** 로드셀 제조사는 감도를 정격 하중에서 여기 전압 1볼트당 출력으로 적는다(Massload). 그러니 P6의 $2.0\,\mathrm{mV/V}$는 $50\,\mathrm N$에서 여기 전압 1볼트마다 $2.0\,\mathrm{mV}$라는 뜻이다.

$$v_o=S\,V_{ex}\,\frac{F}{F_{\text{rated}}}=2.0\,\mathrm{\tfrac{mV}{V}}\times5.0\,\mathrm V\times\frac{F}{50\,\mathrm N},\qquad \text{so } 200\,\mu\mathrm V\text{ per newton}$$

브리지가 하중에 선형이기 때문이다. 여기서 1뉴턴의 값어치는 $200\,\mu\mathrm V$이고, 밀기는 $2.0\,\mathrm{mV}$, 정격은 $10\,\mathrm{mV}$이다. 그리고 출력이 여기 전압에 비례하므로, $V_{ex}$가 흔들리면 모든 판독이 흔들린다. ADC의 기준 전압을 같은 여기 전압에서 끌어오는 설계는 그것을 상쇄하고, 비례식(ratiometric) 설계라고 부른다.

**브리지에 증폭기가 필요한 이유.** §8의 계장 증폭기가 하는 일 하나마다 이유가 하나씩, 둘이다. 신호가 작다. ADC의 카운트당 $1.0\,\mathrm{mV}$(§10)에서는 $50\,\mathrm N$ 범위 전체가 $10$ 카운트이고 1뉴턴은 카운트의 5분의 1이다. 그리고 신호는 $2.5\,\mathrm V$ 위에 얹힌 *차이*인데 ADC는 접지를 기준으로 재므로, ADC에는 둘 중 어느 하나가 아니라 $v_A-v_B$를 건네야 한다. 이득 $400$은 1뉴턴을 $80\,\mathrm{mV}$, 곧 $80$ 카운트로 만들고 ADC에 차이만 건넨다. 여기 전압을 올려도 신호는 커진다. $10\,\mathrm V$면 두 배다. 하지만 게이지의 열은 $V_{ex}^2$로 가서, 게이지 하나에 $5\,\mathrm V$에서 $17.9\,\mathrm{mW}$, $10\,\mathrm V$에서 $71\,\mathrm{mW}$이고, 데워진 게이지는 읽음이 흘러간다(드리프트). 같은 브리지가 [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱 §2.5]]에서 압저항 촉각 소자를 읽는다.

### 10. 아날로그에서 디지털로: ADC

제어기는 숫자로 돈다. ADC는 전압을 숫자로 바꾸고, P6에서는 1초에 $200$번 바꾼다. 이 변환은 두 가지를 잃는다. 두 코드 사이의 값, 그리고 두 샘플 사이에 일어나는 모든 일이다.

> **ADC 분해능의 정의.** 아날로그-디지털 변환기의 **분해능**(resolution)은 *전압*이다. 한 카운트가 나타내는 계단, 곧 **최하위 비트**(LSB)이고, 신호가 아니라 변환기와 그 기준 전압의 성질이다. 정의 조건 넷. $n$비트 변환기에는 $0$부터 $2^n-1$까지 **코드 $2^n$개**가 있다. 코드들은 $0$부터 **기준 전압** $V_{\text{ref}}$까지의 입력 범위를 한 LSB씩 같은 계단으로 나눈다. 이상적인 변환기는 **가장 가까운 코드**를 보고하므로 반올림 오차가 $\pm\tfrac12$ LSB 안에 머물고, **잘라 낸다**. $0$보다 낮은 입력은 $0$으로, 맨 위 코드를 넘는 입력은 맨 위 코드로 읽는다. 그리고 **샘플한다**. 각 코드는 한 순간의 입력이고, $1/f_s$마다 하나다.
>
> $$\text{LSB}=\frac{V_{\text{ref}}}{2^n},\qquad \text{code}=\min\Big(\max\big(\operatorname{round}(v/\text{LSB}),\,0\big),\,2^n-1\Big),\qquad \lvert e_q\rvert\le\tfrac12\,\text{LSB}$$
>
> $v$는 입력 전압이다. 그래서 정확히 $k$ LSB인 입력은 $k$로 읽히고, 범위 안의 다른 모든 입력은 반 계단보다 적게 틀린다.
> - **예**: $4.096\,\mathrm V$에 걸친 P6의 $12$비트는 카운트당 $4.096/4096=1.000\,\mathrm{mV}$이다. 밀기의 $0.80\,\mathrm V$는 $800$으로 읽히고, 증폭하지 않은 브리지의 $2.0\,\mathrm{mV}$는 $2$로 읽힐 것이다.
> - **비예**: "12비트 변환기는 힘을 4096분의 1까지 잰다." 범위를 채우는 신호만 그렇다. 증폭기가 없으면 $50\,\mathrm N$ 범위가 $10$ 카운트, 카운트당 $5\,\mathrm N$이다. 비트만 늘려서는 구하지 못한다. 같은 기준 전압의 $16$비트는 카운트당 $62.5\,\mu\mathrm V$이고, 증폭하지 않은 1뉴턴은 여전히 $3.2$ 카운트뿐이다.
> - **왜 중요한가**: 측정 단위로 바꾼 LSB가 체인 전체의 분해능이다. 여기서는 $1\,\mathrm{mV}$를 $80\,\mathrm{mV/N}$으로 나눈 카운트당 $12.5\,\mathrm{mN}$이다. 반올림은 최대 $\pm6.25\,\mathrm{mN}$을 더하고, 잡음처럼 행동할 때는 $\text{LSB}/\sqrt{12}=3.6\,\mathrm{mN}$ RMS를 더한다. 언제 잡음처럼 행동하는지는 [[04-robotics/sensor-models|3.2 센서 모델과 잡음 §4]]의 질문이고, 비트당 6데시벨의 신호 대 잡음비는 [[02-foundations/signal-processing|6. 신호처리 §2]]의 것이다.

**이득 고르기.** 뉴턴에서 카운트까지의 체인은 곱셈 셋이다. 브리지의 $200\,\mu\mathrm V/\mathrm N$, 증폭기의 $G$, ADC의 $1/\text{LSB}$. 이 가운데 자유로운 것은 이득 하나다. 너무 작으면 1뉴턴이 카운트의 일부이고, 너무 크면 ADC가 로드셀의 정격보다 먼저 잘린다. 영어 절의 코드가 양 끝을 표로 만든다.

| $G$ | 10 N에서 (V) | 10 N의 코드 | 카운트/N | mN/카운트 | 잘리는 힘 (N) |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.0020 | 2 | 0.20 | 5000.00 | 20475.00 |
| 10 | 0.0200 | 20 | 2.00 | 500.00 | 2047.50 |
| 100 | 0.2000 | 200 | 20.00 | 50.00 | 204.75 |
| 200 | 0.4000 | 400 | 40.00 | 25.00 | 102.37 |
| 400 | 0.8000 | 800 | 80.00 | 12.50 | 51.19 |
| 409 | 0.8180 | 818 | 81.80 | 12.22 | 50.06 |
| 500 | 1.0000 | 1000 | 100.00 | 10.00 | 40.95 |
| 1000 | 2.0000 | 2000 | 200.00 | 5.00 | 20.47 |

창은 $G\le409$, 정격 $50\,\mathrm N$을 맨 위 코드 $4095$ 아래에 두는 가장 큰 이득까지다. P6의 $G=400$은 그 바로 안쪽에 있어서 1뉴턴에 $80$ 카운트, 카운트당 $12.5\,\mathrm{mN}$이고, ADC는 $51.2\,\mathrm N$에서 잘린다. 로드셀의 정격과 구동계의 최대 밀기 $50\,\mathrm N$(§7)의 바로 위다. $G=500$은 카운트당 $10\,\mathrm{mN}$으로 더 곱게 읽지만 $40.95\,\mathrm N$에서 눈이 먼다. 모터가 아직 낼 수 있는 밀기다. $G=1$이면 밀기는 2카운트다.

**샘플링이 접어 넣는 것.** ADC는 P6의 $200\,\mathrm{Hz}$로 샘플하므로 나이퀴스트 주파수는 $100\,\mathrm{Hz}$이고, 그 위의 성분은 사라지지 않고 더 낮은 주파수로 다시 나타난다. $f_{\text{alias}}=\lvert f-kf_s\rvert$이고 $k$는 $f/f_s$에 가장 가까운 정수이며, [[02-foundations/signal-processing|6. 신호처리 §2]]가 이를 유도한다. P6에서 이것은 추상적인 이야기가 아니다. PWM의 $20\,\mathrm{kHz}$는 정확히 $200\,\mathrm{Hz}$의 $100$배이므로, 신호선에 올라탄 스위칭 간섭은 $0\,\mathrm{Hz}$로 접힌다. 힘 판독의 일정한 오프셋, 곧 유령 밀기다. PWM 클록이 $20.01\,\mathrm{kHz}$로 흘러가면 유령은 $10\,\mathrm{Hz}$의 흔들림이 되는데, 접촉이 일어나는 대역이다. 그리고 패널에 닿을 때 $170\,\mathrm{Hz}$로 우는 공구는 $30\,\mathrm{Hz}$ 진동으로 읽힌다. 6. §2가 그림으로 보이는 예다. 참 성분과 접힌 성분은 같은 샘플을 만들므로 샘플러 뒤의 어떤 처리도 접힘을 되돌리지 못한다. 샘플러 앞의 필터만이 할 수 있고, §5의 RC가 그 일을 한다. $20\,\mathrm{kHz}$를 $0.24\%$로, $170\,\mathrm{Hz}$를 $27\%$로 줄이며, 그 대가는 §12가 잰다.

**엔코더에는 ADC가 필요 없다.** P6의 엔코더는 이미 디지털이다. 4분의 1 주기 어긋난 구형파 채널 둘이고, 하드웨어 카운터가 그 에지를 방향과 함께 더한다. 분해능은 기하학적이어서 카운트당 $1/2048\,\mathrm m=0.488\,\mathrm{mm}$이고, $0.5\,\mathrm{m/s}$에서 1초에 $1024$ 카운트를 낸다. 그 양자화는 [[04-robotics/sensor-models|3.2 §4]]의 주제이고, 전기적인 약점은 §11의 주제다. 채널에 튄 잡음 스파이크 하나는 평균으로도 사라지지 않는 카운트 하나다.

### 대상으로 한 번 끝까지 · Worked case

카트가 공구를 패널에 대고 $F=10\,\mathrm N$으로 붙들고 있다. 아무것도 움직이지 않으므로 모터에는 역기전력이 없다. 이 숫자 하나를 전력 경로로 내보냈다가 센싱 경로로 다시 들여온다. 모든 단계가 §1–§10의 법칙 하나에 고정된 숫자를 넣은 것이다.

**1단계 — 힘에서 전류로(§7).** 벨트가 밀기를 모터 토크 $\tau_m=Fr_p=10\cdot0.020=0.20\,\mathrm{N{\cdot}m}$로 바꾸고, 토크는 전류 곱하기 토크 상수이므로

$$i=\frac{F\,r_p}{k_t}=\frac{10\cdot0.020}{0.10}=2.0\,\mathrm A$$

손실 없는 벨트는 토크를 그대로 넘겨주기 때문이다.

**2단계 — 전류에서 전압으로(§2, §7).** 정지 상태에서 $e=0$이고 일정한 전류는 $L$ 양단에 아무것도 떨어뜨리지 않으므로, 권선에는 저항의 전압 강하만 필요하다. $v=Ri=1.0\cdot2.0=2.0\,\mathrm V$.

**3단계 — 전압에서 듀티비로(§6).** $D=v/V_s=2.0/24=0.0833$. Q1과 Q4가 $50\,\mu\mathrm s$마다 $4.17\,\mu\mathrm s$ 동안 도통하고, 나머지 $45.8\,\mu\mathrm s$ 동안 전류는 Q2와 Q4를 지나 환류한다.

**4단계 — 리플과 배터리 전류(§3, §4, §6).** 전류는

$$\Delta i_{pp}=\frac{V_sD(1-D)}{Lf}=\frac{24\cdot0.0833\cdot0.917}{10^{-3}\cdot20{,}000}=0.0917\,\mathrm A$$

만큼 출렁인다. $50\,\mu\mathrm s$ 주기가 $\tau_e=1.0\,\mathrm{ms}$의 20분의 1이기 때문이다. $2.0\,\mathrm A$의 $4.6\%$로, $1.954$와 $2.046\,\mathrm A$ 사이다(삽도). 배터리는 켜짐 구간에만 전류를 내므로 평균 $2.0\cdot0.0833=0.167\,\mathrm A$이고, $24\cdot0.167=4.0\,\mathrm W$는 권선의 $i^2R=4.0\,\mathrm W$와 정확히 같다. 밀기는 일을 하지 않으므로 모든 와트가 열이다(스위치의 $0.08\,\mathrm W$는 제쳐 둔다). 이 비율이면 $120\,\mathrm{Wh}$ 배터리는 밀기를 $30\,\mathrm h$ 버틴다.

**5단계 — 힘에서 브리지 출력으로(§9).** $v_o=SV_{ex}F/F_{\text{rated}}=2.0\,\mathrm{mV/V}\cdot5.0\,\mathrm V\cdot10/50=2.0\,\mathrm{mV}$, 1뉴턴에 $200\,\mu\mathrm V$이다. 게이지는 저마다 $350\,\Omega$ 가운데 $0.14\,\Omega$ 움직였다.

**6단계 — 증폭기(§8).** $G\,v_o=400\cdot2.0\,\mathrm{mV}=0.80\,\mathrm V$. 두 브리지 출력에 공통인 $2.5\,\mathrm V$는 제거되고 브리지에는 부하가 걸리지 않는다.

**7단계 — 필터(§4, §5).** 일정한 전압은 RC 저역통과를 그대로 지나가므로, $\lvert H(0)\rvert=1$, 필터가 자리 잡으면 ADC에 $0.80\,\mathrm V$가 닿는다. 밀기가 시작되고 $7.6\,\mathrm{ms}$ 안에 $90\%$까지 가고, PWM의 $20\,\mathrm{kHz}$는 $0.24\%$로 줄어든다.

**8단계 — ADC(§10).** $0.80\,\mathrm V/1.000\,\mathrm{mV}=800$ 카운트. 제어기는 이를 1뉴턴당 $80$ 카운트로 나누어 $10.0\,\mathrm N$을 읽고, 반올림 오차는 $6.25\,\mathrm{mN}$ 안이다.

이제 제어기 안에 한 힘에 대한 추정이 둘 있다. $800$ 카운트는 $10.0\,\mathrm N$이라 말하고, 제어기가 명령한 전류는 $k_ti/r_p=10\,\mathrm N$이라 말한다. 둘이 맞는 것은 이 페이지의 벨트가 손실이 없기 때문일 뿐이다. [[04-robotics/actuators-drives|10.5 §7]]은 마찰과 회전자 관성이 경로에 끼면 전류로 추정한 힘이 얼마나 벗어나는지를 보여 주고, 카트가 로드셀을 싣는 이유가 그것이다. 전류가 재지 못하는 것을 재기 위해서다. 과제는 카트가 밀지 않고 순항할 때, 그리고 다른 ADC로 이 루프를 되풀이한다.

### 11. 접지, 잡음, 안전

*한 문장으로:* 전압은 언제나 두 점 사이에서만 재고 도선은 저항이므로, 센서와 도선을 나눠 쓰는 모터 전류는 유령 힘이 되며, 어떤 배선이나 소프트웨어가 제대로 돌아가는 것에도 기대면 안 되는 안전 기능 하나가 정지이고, 정지는 전력을 요청하는 것이 아니라 끊어야 한다.

**접지는 기준을 고르는 일이다.** 이 페이지의 전압은 모두 차이이고(§1), "접지"는 다른 모든 전압을 재는 기준 노드의 이름이다. P6에서는 배터리의 음극 단자다. 문제는 접지가 점 하나가 아니라 도선의 망이고, §2에 따르면 그 도선 하나하나가 저항이라는 데 있다.

**함께 쓰는 귀환선은 유령 힘을 만든다.** 모터의 귀환 전류와 증폭기의 접지가 배터리로 가는 길에 §2의 $1.0\,\mathrm{mm^2}$ 도선 $0.6\,\mathrm m$, 곧 $10.1\,\mathrm{m\Omega}$을 함께 쓴다고 하자. 밀기 중에 모터의 $2.0\,\mathrm A$는 그 공유 구간에 $2.0\cdot0.0101=20\,\mathrm{mV}$를 걸고, 그래서 증폭기의 "0 V"는 ADC의 것에서 $20\,\mathrm{mV}$ 떨어진다. ADC는 증폭기의 출력에 그 차이를 더해 읽는다. $20$ 카운트, 곧 $0.25\,\mathrm N$의 유령 힘으로, 모터가 밀 때만 나타나고, 모터 전류와 함께 커지며, 잡음이 아니라 일정한 전압이라서 RC 필터를 그대로 통과한다. 고치는 방법은 필터가 아니라 배선이다. **스타 접지**(star ground)는 모터 전류가 제 도선으로 배터리에 돌아가게 하고, 민감한 접지들은 큰 전류가 지나지 않는 한 점에서 만나게 한다.

**루프는 자기 선속을 줍는다.** 두 기판이 접지 경로 둘 — 이를테면 케이블의 접지선과 금속 프레임 — 로 이어지면, 두 경로는 루프를 이룬다. 그 루프를 지나는 변하는 자기 선속은 루프를 따라 전압을 유도한다. H-브리지 전원선의 자기장이 그 예로, 그 전류는 1초에 2만 번 $0$과 $2.0\,\mathrm A$ 사이를 뛰는데 모터 선은 $0.09\,\mathrm A$ 리플만 나른다. 이곳이 §3의 KVL이 깨지는 유일한 자리이고, 유도된 전압은 루프를 도는 전류와 루프의 도선 하나하나를 따라 전압 강하를 만든다. 처방은 기하학적이다. 두 기판 사이의 접지 경로는 하나로, 전원선 쌍과 모터선 쌍은 저마다 꼬아서 반대 방향 전류의 자기장이 상쇄되게, 루프 면적은 작게.

**에지는 부유 커패시턴스로 넘어간다.** H-브리지의 스위칭 중점은 에지마다 $24\,\mathrm V$씩 뛴다. 근처 신호선과의 부유 커패시턴스가 겨우 $1\,\mathrm{pF}$이어도, $50\,\mathrm{ns}$ 동안의 에지는 그 선에 $i=C\,dv/dt=10^{-12}\cdot24/(50\times10^{-9})=0.48\,\mathrm{mA}$를 밀어 넣는다(§4, 둘 다 강의용 숫자). 짧지만 브리지의 $350\,\Omega$을 지나면 약 $0.17\,\mathrm V$의 스파이크다. 브리지의 두 선에 똑같이 넘어간 것은 두 선에 공통이므로 계장 증폭기가 제거하고(§8), 한쪽 끝만 접지한 로드셀 케이블의 편조 차폐가 나머지를 신호 옆으로 흘려보내며, 남은 것은 ADC가 샘플하기 전에 RC가 걷어 낸다(§12). 엔코더 선에서는 같은 스파이크가 더 나쁘다. 카운터가 그것을 에지로 받아들이기 때문이다.

**전류 한계와 퓨즈는 서로 다른 보호다.** 구동계의 $10\,\mathrm A$ 한계는 제어 동작, 곧 전류를 재서 듀티비를 낮추는 전자 회로이고, 그 전자 회로가 살아 있는 동안에만 모터를 지킨다. 퓨즈는 어떤 전자 회로도 다루지 못하는 고장, 곧 단락 — 전원 양단의 낮은 저항 경로(OpenStax) — 에 대한 물리적인 최후 수단이다. 배터리 자신의 $0.050\,\Omega$ 양단이 완전히 단락되면 $24/0.050=480\,\mathrm A$가 흐르고 배터리가 $480^2\cdot0.050=11.5\,\mathrm{kW}$로 달아오른다. 퓨즈는 전류가 과할 때 회로를 연다(OpenStax). P6의 $15\,\mathrm A$는 정상 운전이 끌어가는 가장 큰 전류, 곧 구동계의 $10\,\mathrm A$보다 위에 있고, 퓨즈가 지키는 도선은 과열 없이 퓨즈 정격보다 많이 흘릴 수 있어야 한다.

**비상 정지는 전력을 끊는다. 메시지를 보내지 않는다.** 소프트웨어의 정지 요청은 무언가 잘못되고 있는 그 순간에 버튼 입력, 네트워크, 제어기의 코드, 구동계의 펌웨어가 모두 제대로 돌아가야 하고, [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §7]]은 조용해진 노드 하나가 마지막 명령을 살려 두는 모습을 보여 준다. 하드웨어 비상 정지는 그중 어느 것도 필요 없다. 구동계 전원선에 든 접촉기(contactor) 코일과 직렬로 이은 상시 닫힘 접점의 사슬이다. 어느 버튼이든 누르면 사슬이 열리고, 접촉기가 떨어지고, H-브리지가 전원을 잃는다. 접점이 상시 닫힘이므로 도선이 끊어져도 기계가 선다. 제조사는 여기에 직접 개로 동작(direct opening action)을 더하는데, 접점이 눌어붙었어도 단단한 연결이 접점을 억지로 떼어 놓는 구조다(IDEC). P6에서 그다음은 §4와 §6이다. 권선에 저장된 $2.0\,\mathrm{mJ}$는 열리는 접점을 가로질러 아크를 일으키는 대신 브리지의 다이오드로 빠지고, 카트는 관성으로 굴러가며, 멈추게 하는 것은 역학 — 또는 권선을 단락해 제동하는 구동계([[04-robotics/actuators-drives|10.5 §7]]) — 이다. 비상 정지가 다른 안전 기능 사이에서 어디에 놓이는지는 [[04-robotics/hri-safety|11. HRI와 안전 §6]]이다.

### 12. 실습: PWM 리플, 그리고 안티에일리어스의 맞바꿈

루프 둘, 각각 스윕 하나. 둘 다 작은 스텝의 적분기가 아니라 정확한 갱신으로 회로를 전진시킨다. 입력이 일정하게 유지되는 구간에서 1차 회로는 §4의 지수 함수를 정확히 따르므로, 갱신 $x\leftarrow x_\infty+(x-x_\infty)e^{-\Delta t/\tau}$에는 스텝 크기 오차가 없다. 다른 실습들이 쓰는 근사 적분기는 트랙의 다음 페이지 [[02-foundations/lab-kernel|0.7 Lab Kernel]]이 이름 붙인다.

**A부 — PWM을 받는 권선.** 정지 상태의 밀기. 권선을 계산 절의 듀티비로, 멈춘 상태에서부터 스위칭 주기 하나씩, $0.5$에서 $50\,\mathrm{kHz}$까지의 PWM 주파수에서 구동한다. 영어 절의 코드는 마지막 주기의 전류 양 끝, §6의 작은 리플 공식과 나란히 놓은 리플, 시간 평균 전류를 보고한다.

| $f_{\text{PWM}}$ (kHz) | 켜짐 (µs) | $i_{\min}$ (A) | $i_{\max}$ (A) | 리플 (A) | $V_sD(1-D)/(Lf)$ (A) | 평균 (A) | 가청 대역 $20\,\mathrm{Hz}$–$20\,\mathrm{kHz}$에 대해 |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.5 | 166.67 | 0.6813 | 4.2611 | 3.5799 | 3.6667 | 2.0000 | 안 |
| 1.0 | 83.33 | 1.2138 | 3.0357 | 1.8219 | 1.8333 | 2.0000 | 안 |
| 2.0 | 41.67 | 1.5741 | 2.4893 | 0.9152 | 0.9167 | 2.0000 | 안 |
| 5.0 | 16.67 | 1.8218 | 2.1884 | 0.3666 | 0.3667 | 2.0000 | 안 |
| 10.0 | 8.33 | 1.9096 | 2.0929 | 0.1833 | 0.1833 | 2.0000 | 안 |
| 20.0 | 4.17 | 1.9545 | 2.0462 | 0.0917 | 0.0917 | 2.0000 | 경계 |
| 50.0 | 1.67 | 1.9817 | 2.0184 | 0.0367 | 0.0367 | 2.0000 | 위 |

$20\,\mathrm{kHz}$에서 평균 전류는 $2.35\,\mathrm{ms}$에 $2.0\,\mathrm A$의 $90\%$를 지난다. 매끈한 전압 계단이라면 $2.303\,L/R=2.30\,\mathrm{ms}$이다. 세 가지로 읽는다.

- **듀티비는 평균을 정확히 정하고, 주파수는 리플만 정한다.** 모든 행의 평균이 $2.0000\,\mathrm A$이다. 주기적 정상 상태에서 인덕터 전압의 평균이 0이 되어, 어느 주파수에서든 $R\,\bar i=DV_s$만 남기 때문이다.
- **주파수가 두 배가 될 때마다 리플은 반이 되고**, 주기가 $\tau_e$보다 충분히 짧으면 작은 리플 공식은 세 자리까지 맞는다. 주기가 $\tau_e$의 두 배인 $0.5\,\mathrm{kHz}$에서는 전류가 $0.68$에서 $4.26\,\mathrm A$까지 오간다. 카트를 $500\,\mathrm{Hz}$로 흔드는 밀기이고 윙윙거리는 권선이다. 공식은 리플을 $2.4\%$ 크게 말한다.
- **$20\,\mathrm{kHz}$는 두 비용이 만나는 곳이다.** 리플 $4.6\%$, 그리고 OpenStax가 사람의 청력으로 주는 대역의 맨 위에 걸친 기본 주파수. 더 올리면 리플은 더 줄지만 스위칭 에지가 늘고, 에지마다 스위치가 약간의 에너지를 치른다(§6). 기동 시간은 주파수에 거의 움직이지 않는다. 구동계가 아니라 권선의 것이기 때문이다.

**B부 — ADC가 읽는 것.** 밀기 중의 센싱 체인에, ADC로 가는 선 위의 원치 않는 신호 둘을 얹는다. $20\,\mathrm{kHz}$ 스위칭 간섭 $\pm10\,\mathrm{mV}$와, $\pm0.5\,\mathrm N$ 상당의 공구의 $170\,\mathrm{Hz}$ 울림이다. 둘 다 효과가 보이도록 크기를 정한 강의용 숫자다. RC 필터는 $2.5\,\mu\mathrm s$마다 정확히 갱신하고, ADC는 $5\,\mathrm{ms}$마다 샘플하며, 스윕은 $C_f=1.0\,\mu\mathrm F$를 둔 채 $R_f$를 바꾼다. 영어 절의 코드는 원치 않는 두 주파수에서의 필터 이득, 자리 잡은 뒤 판독의 피크–피크 흔들림과 평균 오프셋, 그리고 밀기가 시작된 뒤 처음으로 $9\,\mathrm N$ 이상인 판독의 시각을 보고한다.

| $R_f$ (Ω) | $f_c$ (Hz) | 170 Hz의 $\lvert H\rvert$ | 20 kHz의 $\lvert H\rvert$ | 흔들림 (N p-p) | 오프셋 (mN) | 첫 ≥ 9 N 판독 (ms) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 (필터 없음) | ∞ | 1.0000 | 1.00000 | 1.000 | 125.0 | 5.0 |
| 100 | 1591.5 | 0.9943 | 0.07933 | 1.000 | −12.5 | 5.0 |
| 330 | 482.3 | 0.9431 | 0.02411 | 0.937 | −2.5 | 5.0 |
| 1000 | 159.2 | 0.6834 | 0.00796 | 0.675 | −0.6 | 5.0 |
| 3300 | 48.2 | 0.2729 | 0.00241 | 0.275 | −0.6 | 10.0 |
| 10000 | 15.9 | 0.0932 | 0.00080 | 0.113 | −4.4 | 25.0 |

네 가지로 읽는다.

- **필터가 없으면 PWM이 힘이 된다.** ADC가 스위칭 주기마다 같은 지점에서 샘플하므로, 마침 붙잡은 $+10\,\mathrm{mV}$가 일정한 $+125\,\mathrm{mN}$으로 읽힌다. 변하지 않으니 평균으로도 없앨 수 없는, 10카운트의 유령 밀기다. 필터가 하나라도 있으면 1카운트 안으로 줄어든다. 오프셋 열에 남은 것은 반올림이고, 마지막 행에서는 필터 자신의 느린 수렴 꼬리다.
- **울림은 더 교묘하다.** 공구의 $170\,\mathrm{Hz}$는 판독에 피크–피크 $1.0\,\mathrm N$의 $30\,\mathrm{Hz}$ 흔들림으로 나타난다. 제어기가 쫓아갈 진동이다. $170\,\mathrm{Hz}$보다 한참 낮은 차단 주파수만이 그것을 줄인다. $159\,\mathrm{Hz}$에서 $0.675\,\mathrm N$, P6의 $48\,\mathrm{Hz}$에서 $0.275$, $16\,\mathrm{Hz}$에서 $0.113$이고, 각각 필터 없는 $1.0\,\mathrm N$에 그 행의 $170\,\mathrm{Hz}$ $\lvert H\rvert$를 곱한 값과 2카운트 안에서 맞는다.
- **걸러 낼 때마다 시간을 치른다.** 차단 주파수가 $159\,\mathrm{Hz}$까지는 밀기의 첫 판독이 시작 뒤 한 주기 만에 온다. P6의 필터는 한 주기를 더 치러 $10\,\mathrm{ms}$이고, $16\,\mathrm{Hz}$ 필터는 네 주기를 더 치러 $25\,\mathrm{ms}$이다. 제어기가 제가 만들고 있는 밀기를 보기까지 P6의 $5\,\mathrm{ms}$ 시계로 다섯 주기다.
- **그래서 RC 하나는 타협이고**, $3.3\,\mathrm{k\Omega}$이 P6의 타협이다. 유령은 완전히 없애고 접힌 울림은 4분의 3을 없애며, 그 값으로 한 주기의 지연을 치른다. 둘 다 더 잘하려면 더 가파른 필터나, 더 빠른 ADC 뒤의 디지털 필터가 필요하다. [[02-foundations/signal-processing|6. 신호처리 §2와 §4]].

### 13. 이 페이지가 다루지 않는 것

- **반도체 물리.** p–n 접합이 왜 한 방향으로만 도통하는지, MOSFET의 채널이 어떻게 생기는지는 주어진 것으로 둔다. 여기서 스위치는 $R_{\text{on}}$과 $V_F$를 가진 모델이다.
- **교류 전력.** §5의 필터 하나를 넘는 페이저, 역률, 변압기, 상용 전원 배선.
- **전력 변환.** 스위칭 전원 — 인덕터를 구동하는 PWM 다리는 이미 모습을 감춘 강압 변환기다 — 배터리 화학, 충전과 충전 상태.
- **구동계의 속.** 전류 센싱, 전류 루프, 모터의 열 한계는 [[04-robotics/actuators-drives|10.5 §5와 §6]]이고, 브러시리스 정류와 field-oriented control은 이 위키 밖이다.
- **신호를 깊이.** 샘플링 이론, 디지털 필터, 비트당 신호 대 잡음비는 [[02-foundations/signal-processing|6. 신호처리]]이고, 양자화가 언제 잡음인지, P6의 센서가 저마다 어떻게 모델링되는지는 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]이다.
- **통신과 타이밍.** 직렬 버스와 필드버스, 그리고 그것들이 쓰는 지연 예산은 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]의 몫이다.
- **안전 공학.** 위험성 평가, 안전 등급 제어, 그것을 다스리는 표준은 [[04-robotics/hri-safety|11. HRI와 안전 §6]]이다. §11은 전기적인 추론만 준다.
- **기계와 유체의 쌍둥이.** 커패시터와 인덕터는 스프링과 질량처럼 에너지를 저장하고, 저항은 댐퍼처럼 그것을 쓴다 — [[02-foundations/basic-mechanics|0.6.1 기초 역학 §4–§5]]의 질량–스프링–댐퍼다. 전압 곱하기 전류가 아니라 압력 곱하기 유량으로 실려 가는 일률은 [[02-foundations/fluid-power|0.6.3 유체 동력 §4]]다.

### 읽고 나면

- [ ] 배터리 라벨을 쿨롱, 줄, 주어진 전력에서의 작동 시간으로 바꾸고, 작동 시간이 왜 줄에서 나오는지 말한다.
- [ ] 센서, 도선, 권선에 옴의 법칙, 직렬과 병렬, $p=i^2R$을 쓴다.
- [ ] 작은 회로의 노드마다 KCL을 쓰고 푼다. 분배기의 출력과 부하가 그것에 하는 일을 말한다.
- [ ] 커패시터와 인덕터가 무엇을 저장하는지, 어느 변수가 뛰지 못하는지 말하고, $RC$와 $L/R$을 계산한다.
- [ ] RC 필터의 차단 주파수, 아무 주파수에서의 이득과 위상, 그리고 더해지는 지연을 말한다.
- [ ] PWM과 그 리플을 설명하고, H-브리지의 켜짐 경로와 환류 경로를 따라가며, 유도성 부하에 왜 뒤의 것이 필요한지 말한다.
- [ ] DC 모터의 회로 방정식을 쓰고 한 운전점에서 전력 장부를 맞춘다.
- [ ] 연산 증폭기의 두 규칙에서 반전, 비반전, 계장 증폭기의 이득을 유도하고, 브리지에 왜 마지막 것이 필요한지 말한다.
- [ ] 뉴턴을 브리지 마이크로볼트, 증폭기 볼트, ADC 카운트로 바꾸고 이득을 고른다.
- [ ] ADC의 샘플링이 무엇을 접어 넣는지, 필터가 왜 그 앞에 와야 하는지, 필터가 무엇을 치르는지 말한다.
- [ ] 스타 접지로 배선하고, 비상 정지가 왜 전력을 끊어야 하는지 말한다.

### 스스로 점검

1. P6의 배터리 라벨은 $24\,\mathrm V$, $5.0\,\mathrm{Ah}$이다. 몇 쿨롱이고 몇 줄인가? 밀기의 작동 시간은 왜 쿨롱이 아니라 줄에서 나오는가?
2. 밀기 중에 권선은 $2.0\,\mathrm A$를 흘리는데 배터리는 $0.167\,\mathrm A$를 낸다. 어느 법칙들이 이 둘을 맞게 하고, 그 차이는 어디서 오는가?
3. H-브리지에 환류 경로가 없다면 Q1이 열리는 순간 무슨 일이 일어나는가? 그리고 그림의 브리지에서 권선의 전류는 어디로 가는가?
4. 이득 $400$짜리 비반전 증폭기는 왜 로드셀을 읽지 못하는데, 같은 이득의 계장 증폭기는 읽을 수 있는가?
5. PWM이 ADC 샘플링 주파수의 정확히 $100$배로 돈다. 그 간섭은 힘 판독에서 어떤 모습인가? PWM이 $20.01\,\mathrm{kHz}$로 흘러가면 무엇이 바뀌는가?
6. 연구실 동료가 P6의 비상 정지를 듀티비를 0으로 만드는 메시지로 구현하자고 한다. 전원선의 상시 닫힘 접점 사슬에는 없고 그 설계에만 있는 실패 둘을 들어라.

> [!tip]- 스스로 점검 정답 · Answers
> 1. $5.0\,\mathrm{Ah}\times3600=18{,}000\,\mathrm C$이고, $18{,}000\,\mathrm C\times24\,\mathrm{J/C}=432\,\mathrm{kJ}=120\,\mathrm{Wh}$이다. 구동계는 전류를 바꾼다. 모터는 $2.0\,\mathrm A$를 흘리는데 배터리는 $0.167\,\mathrm A$를 내므로, 두 쪽을 잇는 전류는 하나가 아니다. 이어 주는 것은 전력 — 양쪽 모두 $4.0\,\mathrm W$ — 이므로 작동 시간은 에너지 나누기 전력, $120/4.0=30\,\mathrm h$이다.
> 2. 주기에 걸쳐 평균한 KCL. 배터리는 $8.33\%$의 켜짐 구간에만 권선의 $2.0\,\mathrm A$를 나르고 전류가 환류하는 동안에는 아무것도 나르지 않으므로 평균 $0.167\,\mathrm A$이다. 그리고 에너지. $24\,\mathrm V\times0.167\,\mathrm A=4.0\,\mathrm W=2.0\,\mathrm V\times2.0\,\mathrm A$. 구동계는 기어박스가 속도와 토크를 맞바꾸듯 전압과 전류를 맞바꾸고, 꺼짐 구간 내내 전류를 붙들어 주는 권선의 인덕턴스가 그 맞바꿈을 가능하게 한다.
> 3. 권선은 첫 순간 $2.0\,\mathrm A$를 그대로 지니려 하므로(§4), 그것을 $100\,\mathrm{ns}$ 만에 0으로 만들면 열리는 스위치 양단에 약 $L\,di/dt=20{,}000\,\mathrm V$가 걸리고 스위치가 망가진다. 그림의 브리지에서는 Q4가 켜진 채로 있고 Q2가 데드 타임 뒤에 켜진다 — 데드 타임 동안에는 Q2의 다이오드가 전류를 나른다. 그래서 전류는 Q2, 권선, Q4를 돌며 권선 양단에 거의 전압 없이 천천히만 줄어든다. $45.8\,\mu\mathrm s$ 동안 $0.092\,\mathrm A$다.
> 4. 읽을 가치가 있는 $2.0\,\mathrm{mV}$가 두 브리지 출력에 공통인 $2.5\,\mathrm V$ 위에 얹혀 있기 때문이다. 비반전 증폭기는 출력 하나를 접지에 대해 키우므로 $400\times2.5\,\mathrm V=1000\,\mathrm V$를 내려다 포화한다. 계장 증폭기의 첫 단은 공통의 $2.5\,\mathrm V$를 이득 1로 통과시키면서 차이를 $400$배 하고, 차동 단이 공통 부분을 없앤다. 게다가 두 입력 모두 전류를 거의 끌어가지 않으므로 브리지에 부하가 걸리지 않는다.
> 5. 일정한 오프셋이다. $20\,\mathrm{kHz}$를 $200\,\mathrm{Hz}$로 샘플하면 $\lvert20{,}000-100\cdot200\rvert=0\,\mathrm{Hz}$로 접히므로, 판독마다 간섭의 같은 위상을 붙잡고, 실습의 필터 없는 체인은 일정한 유령 $125\,\mathrm{mN}$을 읽는다. $20.01\,\mathrm{kHz}$면 접힌 자리가 $10\,\mathrm{Hz}$가 되어 유령이 느린 흔들림이 되는데, 접촉이 일어나는 대역 안이다. 어느 쪽이든 막을 수 있는 것은 ADC 앞의 필터뿐이다.
> 6. 메시지가 지나가는 모든 것 — 버튼 입력, 네트워크, 제어기의 코드, 구동계의 펌웨어 — 에 기대는데, 그중 어느 것이든 바로 고장 나고 있는 그것일 수 있다. 그리고 조용해지거나 멈춘 노드는 정지 대신 마지막 명령을 살려 둔다([[04-robotics/robot-systems-deployment|10. 로봇 시스템 §7]]). 접촉기 코일과 직렬인 접점 사슬은 아무것도 돌아갈 필요가 없다. 버튼을 누르거나 도선이 끊어지면 사슬이 열려 H-브리지의 전원이 빠지고, 직접 개로 동작은 접점이 눌어붙었어도 억지로 떼어 놓는다.

### 과제 · Problem set

Tier A. 이 페이지, 그 선수 지식, 대상 카탈로그만 쓴다. P6과 이 페이지의 고정 전자 회로를 쓰고, 항목마다 말하는 것만 바꾼다.

1. **그리기.** 위의 그림을, 카트가 패널에 닿지 않은 채 구름 저항 $2.0\,\mathrm N$을 이기며 $0.5\,\mathrm{m/s}$로 **순항**하는 경우로 다시 그린다. 전력 경로에는 전류, 역기전력, 평균 전압, 듀티비, 배터리 전류를, PWM 한 주기의 전류 경로 둘을, 리플의 양 끝을 표시한 $v(t)$와 $i(t)$ 삽도를, 그리고 센싱 경로에는 블록마다 읽는 값을 넣는다. 밀기와 비교해 그림의 어느 숫자가 바뀌고 어느 숫자가 사라졌는지, 그리고 왜 그런지 말한다.
2. **유도.** (a) 새 ADC: $V_{\text{ref}}=2.5\,\mathrm V$인 $16$비트이고, 브리지를 $10\,\mathrm V$로 여기한다. LSB, 정격 $50\,\mathrm N$을 범위 안에 두는 가장 큰 정수 이득, 그 이득에서 1뉴턴당 카운트와 카운트당 뉴턴을 구하고, 높은 여기 전압이 게이지 하나에 열로 무엇을 치르게 하는지 말한다. (b) 배터리 모니터를 입력 저항 $1\,\mathrm{M\Omega}$로 읽을 때: ADC에 걸리는 전압, 그 코드, 무부하 비율을 가정한 펌웨어가 보고하는 배터리 전압. (c) 카트가 순항할 때 §11의 공유 접지: 그것이 더하는 유령 힘을 카운트와 뉴턴으로. (d) 환류 경로가 없는 구동계가 순항 전류를 $100\,\mathrm{ns}$ 만에 끊을 때: 스위치 양단의 전압과 권선이 지녔던 에너지.
3. **실행.** 양극성(bipolar) PWM은 두 다리를 반대 위상으로 스위칭한다. $DT$ 동안 Q1과 Q4, 나머지 동안 Q2와 Q3이므로, 권선은 $+V_s$와 $0$이 아니라 $+V_s$와 $-V_s$를 본다. 영어 절의 템플릿을 §12 실습의 A부 뒤에 붙이고, `?`를 모두 채워 돌린다. $20\,\mathrm{kHz}$의 리플을 A부의 것과 견주고, 양극성 PWM이 단극성 PWM의 $20\,\mathrm{kHz}$ 리플과 같아지는 주파수를 찾고, 이 듀티비에서 양극성이 더 출렁이는 이유를 말한다.

> [!note]- 그리는 법 · How to draw it
> - **루프의 모양은 그대로 둔다.** 위에 전력 경로, 가운데 벨트와 카트, 아래에 센싱 경로, 왼쪽에서 루프를 닫는 제어기. 바뀌는 것은 숫자뿐이다.
> - **모터 안에 역기전력을 넣는다.** 순항 중의 권선은 $R$, $L$, 그리고 전류에 맞서는 전원 $e=k_ev_c/r_p=2.5\,\mathrm V$이다. 셋 모두 적고, 그 옆에 평균 전압 $\bar v=Ri+e$를 적는다.
> - **두 전류 경로를 권선 속에서 같은 방향으로 그린다.** Q1과 Q4를 지나는 켜짐 구간은 실선, Q2와 Q4를 지나는 환류는 점선으로 하고, 새 듀티비에서의 지속 시간을 각각 적는다.
> - **삽도는 밀기의 삽도를 새 듀티비로 그린 것이다.** 리플은 역기전력과 상관없이 $V_sD(1-D)/(Lf)$이므로 새 $D$로 계산한다. 양 끝과 평균을 표시하고, 최솟값이 0보다 위에 머무는지, 곧 전류가 한 번도 멈추지 않는지 확인한다.
> - **센싱 경로는 모터의 힘이 아니라 접촉력을 읽는다.** 접촉이 없으면 로드셀은 아무것도 보지 않으므로 그 아래 모든 블록이 0을 읽는다. 코드 $0$은 단극성 ADC가 작은 음의 오프셋을 숨기는 자리이기도 하다. 그림에 그렇게 적는다.
> - **그림 위에서 장부를 맞춘다.** 배터리 전류와 전력, 권선의 열, 역기전력을 건너가는 전력, 그리고 그것과 같아야 하는 기계적 $F\,v_c$.

> [!tip]- 정답 · Solutions
> 1. 역기전력 $e=5.0\cdot0.5=2.5\,\mathrm V$(모터에서 $25\,\mathrm{rad/s}$), 전류 $i=2.0/5.0=0.40\,\mathrm A$, 평균 전압 $\bar v=0.40+2.5=2.9\,\mathrm V$, 듀티비 $2.9/24=12.08\%$로 $50\,\mu\mathrm s$마다 켜짐 $6.04\,\mu\mathrm s$, 환류 $43.96\,\mu\mathrm s$이다. 리플은 $24\cdot0.1208\cdot0.8792/(10^{-3}\cdot20{,}000)=0.1275\,\mathrm A$이므로 전류는 $0.337$과 $0.464\,\mathrm A$ 사이를 오가고(정확한 주기해) 한 번도 멈추지 않는다. 배터리 전류 $0.1208\cdot0.40=0.048\,\mathrm A$, $1.16\,\mathrm W$. 권선의 열 $0.16\,\mathrm W$. $e\,i=1.0\,\mathrm W=F\,v_c=2.0\cdot0.5$. 센싱 경로는 $0\,\mathrm N$, $0\,\mathrm{mV}$, $0\,\mathrm V$, 코드 $0$을 읽는다. 바뀐 것: 역기전력이 생겨 $2.9\,\mathrm V$ 가운데 $2.5$를 차지하고, 전류는 5분의 1로 줄었으며, 리플은 오히려 $0.092$에서 $0.128\,\mathrm A$로 *커졌다*. $D(1-D)$가 $0.076$에서 $0.106$으로 커졌기 때문이고, 작아진 전류에 대면 $4.6\%$가 아니라 $32\%$이다. 사라진 것: 힘, 브리지 출력, 카운트. 로드셀은 접촉을 재고, 이제 전류가 치르는 구름 저항은 로드셀이 보지 못한다.
> 2. (a) $\text{LSB}=2.5/65{,}536=38.15\,\mu\mathrm V$. $10\,\mathrm V$에서 정격 출력은 $20\,\mathrm{mV}$이므로 이득은 $20\,\mathrm{mV}\cdot G\le65{,}535\cdot38.15\,\mu\mathrm V=2.49996\,\mathrm V$를 지켜야 한다. $G\le124.998$이므로 $G=124$. 그러면 1뉴턴은 $400\,\mu\mathrm V\cdot124=49.6\,\mathrm{mV}$, $1300.2$ 카운트이고, 한 카운트는 $0.769\,\mathrm{mN}$이다. 페이지의 $12.5\,\mathrm{mN}$보다 16배 곱고, $50.40\,\mathrm N$에서 잘린다. 게이지 하나 양단에 이제 $5\,\mathrm V$가 걸려 $5^2/350=71.4\,\mathrm{mW}$를 소산하는데, 페이지의 $17.9\,\mathrm{mW}$의 네 배다. (b) $15\,\mathrm{k\Omega}\parallel1\,\mathrm{M\Omega}=14.78\,\mathrm{k\Omega}$이므로 $v=24\cdot14.78/114.78=3.090\,\mathrm V$, 코드 $3090$이고, 무부하 비율 $0.1304$로 나누는 펌웨어는 $23.69\,\mathrm V$, $1.3\%$ 낮게 보고한다. (c) $0.40\,\mathrm A\cdot10.1\,\mathrm{m\Omega}=4.0\,\mathrm{mV}$, $4$ 카운트, 카트가 움직일 때마다 나타나는 $0.050\,\mathrm N$의 유령 힘. (d) $L\,di/dt=10^{-3}\cdot0.40/10^{-7}=4000\,\mathrm V$이고, 저장되어 있던 에너지는 $\tfrac12\cdot10^{-3}\cdot0.40^2=80\,\mu\mathrm J$이다.
> 3. 빈칸: `D_bi = (1 + 2.0*R/Vs)/2`, 곧 $(2D-1)V_s=2.0\,\mathrm V$이므로 $0.5417$. 전압은 `Vs`와 `-Vs`. 그리고 `approx = Vs*(1 - m**2)/(2*L*f)`로, §6처럼 유도한다. 켜짐 구간 동안 인덕턴스는 $V_s-\bar v=V_s(1-m)$을 $D_{\text{bi}}T=(1+m)T/2$ 동안 보므로 $\Delta i\approx V_s(1-m)(1+m)/(2Lf)$이다. 스윕은 $20\,\mathrm{kHz}$에서 리플 $0.5958\,\mathrm A$($1.702$에서 $2.298\,\mathrm A$)를 주는데, A부의 $0.0917$의 $6.5$배이고 공식과 네 자리까지 맞는다. $130\,\mathrm{kHz}$ 행은 $0.0917\,\mathrm A$를 돌려주므로, 양극성 PWM이 같은 만큼만 출렁이려면 주파수가 — 그리고 스위칭 에지가 — $6.5$배 필요하다. 이유는 볼트–초다. 단극성 PWM은 꺼짐 구간을 $0\,\mathrm V$에서 보내는데, 권선이 유지하는 $2\,\mathrm V$에서 $2\,\mathrm V$밖에 떨어져 있지 않다. 양극성 PWM은 주기 내내 권선을 $+24$와 $-24\,\mathrm V$ 사이로 몰아서 각각 $22\,\mathrm V$와 $26\,\mathrm V$ 떨어져 있으므로, 반 주기마다 전류를 훨씬 많이 움직인다. 양극성의 장점은 다른 데 있다. 평균 $(2D-1)V_s$가 $D=50\%$에서 매끈하게 0을 지나므로, 밀기를 뒤집을 때 스위칭 방식을 바꿀 필요가 없다.

### 출처

- OpenStax, *University Physics Volume 2*(https://openstax.org/books/university-physics-volume-2, HTML로 읽음) — §7.2 볼트는 쿨롱당 줄; §8.3과 §14.3 저장 에너지 $\tfrac12CV^2$와 $\tfrac12LI^2$; §9.1 전류와 그 관례적 방향; §9.3 비저항과 그 온도 계수(구리 $1.68\times10^{-8}\,\Omega{\cdot}\mathrm m$, $0.0039\,/^\circ\mathrm C$); §9.5 $P=IV=I^2R=V^2/R$; §10.2–10.3 저항의 직렬과 병렬, 전하와 에너지 보존에서 나오는 키르히호프 규칙; §10.5와 §14.4 시정수 $RC$와 $L/R$; §10.6 단락과 퓨즈; §14.2 자기 인덕턴스, $\varepsilon=-L\,dI/dt$.
- OpenStax, *University Physics Volume 3*, §9.7 반도체 소자 — 한 방향 밸브로서의 다이오드와 그 전류 법칙 $I=I_0(e^{eV/k_BT}-1)$.
- OpenStax, *College Physics 2e*, §17.6 청각 — 정상 청력 $20$에서 $20{,}000\,\mathrm{Hz}$.
- NIST: 기본 전하 $1.602176634\times10^{-19}\,\mathrm C$와 볼츠만 상수 $1.380649\times10^{-23}\,\mathrm{J/K}$의 CODATA 값, 둘 다 정확한 값(physics.nist.gov/cuu/Constants); *NIST Guide to the SI*(SP 811) 4장 표 3, 고유 이름을 가진 유도 단위를 서로의 말로 쓴 것, 그리고 부록 B.8의 정확한 환산 $1\,\mathrm{A{\cdot}h}=3.6\times10^3\,\mathrm C$, $1\,\mathrm{W{\cdot}h}=3.6\times10^3\,\mathrm J$.
- Micro-Measurements(Vishay Precision Group), StrainBlog: "Crossing Over the Wheatstone Bridge"(strainblog.micro-measurements.com/content/crossing-over-wheatstone-bridge) — 브리지 출력 $V_{\text{out}}=KV\varepsilon N/4$와 명목 게이지율 $2$; "Strain Sensor Resistances Explained"(strainblog.micro-measurements.com/tips/strain-sensor-resistances-explained) — $120$, $350$, $1000\,\Omega$ 게이지, 저항이 높을수록 자체 발열이 줄어든다는 점.
- Massload Technologies, "What Is mV/V in Load Cells?"(www.massload.com/what-is-mv-v-in-load-cells-an-introductory-guide/) — 정격 용량에서 여기 전압 1볼트당 정격 출력의 정의, 출력 공식, 그리고 흔한 범위인 $1$–$3\,\mathrm{mV/V}$.
- Toshiba Electronic Devices & Storage, e-learning과 FAQ 페이지(https://toshiba.semicon-storage.com) — 연산 증폭기의 가상 단락, 예로 든 개루프 이득 $100{,}000$, 입력으로 들어가지 않는 전류; 게이트가 만드는 MOSFET의 채널, 정해진 게이트 전압에서의 $R_{DS(ON)}=V_{DS}/I_D$, 그리고 바디 다이오드; 정류 다이오드의 한 방향 도통.
- IDEC, "Emergency Stop Switches" 안전 가이드(www.idec.com/en-us/solutions/safety/guide/safety02) — 회로 고장이 기계를 세우도록 하는 상시 닫힘 접점, 그리고 눌어붙은 접점을 억지로 떼어 놓는 직접 개로 동작.
- 이 위키 안에서: 수학은 [[02-foundations/engineering-math|0.5 공업수학]], P6은 [[02-foundations/lab-plants|0.6 Lab Plants]], 모터의 고정 상수와 이 페이지 너머 구동계가 하는 모든 일은 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]], 샘플이 그다음에 겪는 일은 [[02-foundations/signal-processing|6. 신호처리]]와 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]].
- 이 페이지의 나머지 숫자 — 배터리, 퓨즈, 벨트, 구름 저항, 로드셀, 증폭기, 필터, ADC, 간섭, 울림 — 는 모두 여기서 고른 강의용 숫자이고, 페이지의 코드나 손으로 계산했다. 믿지 말고 다시 계산하라.
