---
title: 10.5 Actuators & Drives
tags: [robotics, actuation, control]
study-depth: Literacy
wiki-support: Working
depth-goal: "On P2's shoulder with this page's frozen drive, turn a joint torque into current, voltage, heat and temperature rise, add the rotor to the mass matrix, run the cascade lab, and name which limit — thermal, current or voltage — closes each end of the gear-ratio range."
mastery-when: "Raise to Working when a paper or the thesis reads motor current as joint torque, chooses a gear ratio, or claims a backdrivable arm; Mastery only if actuator design becomes the contribution."
---

> [!note] Prerequisites · 선수 지식
> Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled), with its mass matrix and gravity torque from [[02-foundations/manipulator-kinematics-dynamics|10. §3 and §5]]. The integrators of [[02-foundations/lab-kernel|0.7 Lab Kernel]]. Second-order parameters, bandwidth, and PID with anti-windup from [[04-robotics/control-theory-ce397|5. Control Theory §5, §5.5 and §7]]. The gear ratio, reflected inertia and backdrivability are defined on this page (§2, §4, §7), so no later page is needed; the capstan version of all three, on a haptic handle, is optional further reading in the haptics track.
> [[02-foundations/lab-plants|0.6]]의 장치 **P2**, 그리고 [[02-foundations/manipulator-kinematics-dynamics|10. §3과 §5]]의 질량 행렬·중력 토크. [[02-foundations/lab-kernel|0.7 Lab Kernel]]의 적분기. [[04-robotics/control-theory-ce397|5. 제어 이론 §5, §5.5, §7]]의 2차계 파라미터, 대역폭, anti-windup이 있는 PID. 감속비, 반사 관성, 역구동성은 이 페이지(§2, §4, §7)에서 정의하므로 뒤쪽 페이지는 필요 없다. 셋 모두의 캡스턴 판(햅틱 손잡이 위)은 햅틱 트랙에서 골라 더 읽을 거리다.

## English

*Stands on [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] for P2's $M$ and $g$, and on [[04-robotics/control-theory-ce397|5. Control Theory]] for PD, bandwidth and anti-windup. Sits beside [[04-robotics/robot-systems-deployment|10. Robot Systems §2]], which lists actuators as part of embodiment without opening one. A later use of plant **P2**, now with a motor and a gearbox at each joint.*

> [!note] First pass · 처음이라면
> Read the Running object, the picture and the Worked case: one joint torque turned into amps, volts, watts and kelvin, and one entry of P2's mass matrix changed by a rotor you never see. Then §1 for the two equations, §3 for the torque–speed line, §4 for reflected inertia and §6 for why heat, not current, decides what a joint can hold. §2, §5 and §7 are what you open when you are choosing a drive rather than reading about one; §8 is the lab and §9 the reading checklist.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], standing in the vertical plane with $g=9.81\,\mathrm{m/s^2}$ along $-y$, at its frozen pose $\theta=(0^\circ,90^\circ)$: elbow at $(1,0)$, forearm straight up, tip at $(1,1)\,\mathrm{m}$. Two of its numbers carry the whole page, both derived on [[02-foundations/manipulator-kinematics-dynamics|10. §3 and §5]]: the shoulder's mass-matrix entry $M_{11}=3\,\mathrm{kg{\cdot}m^2}$ and the shoulder's gravity torque $g_1=19.62\,\mathrm{N{\cdot}m}$. The elbow's gravity torque is $0$ at this pose, because the forearm mass sits directly above the elbow.

Each joint now gets a **drive**: a DC motor, the amplifier that feeds it, and a gearbox between the motor and the link. The catalog has no drive, so this page specifies one completely and freezes it. The values are **illustrative** — the right order of magnitude for a small arm joint, chosen for this page, and not taken from any product's datasheet.

| Symbol | Value | What it is |
|---|---:|---|
| $R$ | $1.0\,\Omega$ | winding resistance (§1) |
| $L$ | $1.0\,\mathrm{mH}$ | winding inductance (§1) |
| $k_t$ | $0.10\,\mathrm{N{\cdot}m/A}$ | torque constant (§1) |
| $k_e$ | $0.10\,\mathrm{V{\cdot}s/rad}$ | back-EMF constant; the same number as $k_t$, as §1 derives |
| $J_m$ | $1.0\times10^{-4}\,\mathrm{kg{\cdot}m^2}$ | rotor inertia about the motor axis, gearbox input stage included |
| $b$ | $1.0\times10^{-5}\,\mathrm{N{\cdot}m{\cdot}s/rad}$ | viscous friction at the motor shaft (bearings) |
| $n$ | $100$; swept from $30$ to $300$ in §8 | gear ratio, motor turns per joint turn (§2) |
| $\eta$ | $0.80$ | gearbox efficiency with the motor driving (§2) |
| $V_s$ | $24\,\mathrm{V}$ | supply voltage (§3) |
| $I_{\max}$ | $10\,\mathrm{A}$ | amplifier current limit (§3) |
| $R_{th}$ | $10\,\mathrm{K/W}$ | winding-to-ambient thermal resistance, one-node model (§6) |
| $\Delta T_{\max}$ | $100\,\mathrm{K}$ | allowed winding temperature rise above ambient (§6) |
| $\tau_{th}$ | $60\,\mathrm{s}$ | thermal time constant of that node (§6) |

Three modelling choices, stated once. **The two drives are identical**, one at each joint. **A drive adds only its rotor's spin inertia** to the arm: its mass is counted inside the catalog's point masses, so the shoulder drive, bolted to the base, adds no mass, and the elbow drive's mass is part of the $1\,\mathrm{kg}$ at the elbow. **The electrical model is a brushed DC motor's**; a brushless motor under its current controller obeys equations of the same form, and *Modern Robotics* §8.9.1 makes the same simplification. In the lab (§8) the elbow drive holds the elbow at $90^\circ$ and only the shoulder moves, so the shoulder sees exactly $M_{11}$ and $g_1(\theta_1)=9.81\,(2\cos\theta_1-\sin\theta_1)\,\mathrm{N{\cdot}m}$, which is page 10's $g_1$ with $\theta_2$ held at $90^\circ$.

*Scope: this page teaches one geared DC drive on one joint of P2 — its electrical and mechanical equations, the torque–speed line, reflected inertia and what it does to the mass matrix, the two time constants that justify a current loop, the thermal and current limits, backdrivability, and the gear-ratio trade that ties them together. It does not teach motor design (magnetics, windings, commutation), power electronics (PWM bridges, field-oriented control), hydraulic actuation, joint flexibility or friction identification; the PWM bridge that drives this motor, and the motor as a circuit, are [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics §6–§7]], and the hydraulic cylinders of the construction machines are [[02-foundations/fluid-power|0.6.3 Fluid Power]]. The controller that uses a backdrivable, torque-controlled drive for contact is [[04-robotics/force-compliance-control|13. Force & Compliance Control]], and the capstan version of the same trade, on a haptic handle, is [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]], later in the haptics track and not needed here.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="joint torque against joint speed for P2's shoulder drive at gear ratio 100: current limit, voltage line, thermal line, the hold point and the lift's demand loop">
  <path d="M70 240 L70 80 L312.3 80 L485.4 240 Z" fill="currentColor" fill-opacity="0.07"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none">
    <line x1="70" y1="240" x2="530" y2="240"/><line x1="70" y1="240" x2="70" y2="48"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45">
    <line x1="156.5" y1="240" x2="156.5" y2="245"/><line x1="243.1" y1="240" x2="243.1" y2="245"/><line x1="329.6" y1="240" x2="329.6" y2="245"/><line x1="416.2" y1="240" x2="416.2" y2="245"/><line x1="502.7" y1="240" x2="502.7" y2="245"/>
    <line x1="65" y1="200" x2="70" y2="200"/><line x1="65" y1="160" x2="70" y2="160"/><line x1="65" y1="120" x2="70" y2="120"/><line x1="65" y1="80" x2="70" y2="80"/>
  </g>
  <g stroke="currentColor" fill="none">
    <line x1="70" y1="80" x2="312.3" y2="80" stroke-width="2.2"/>
    <line x1="312.3" y1="80" x2="485.4" y2="240" stroke-width="2.2"/>
    <line x1="312.3" y1="80" x2="290.7" y2="60" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.6"/>
    <line x1="70" y1="189.4" x2="430.7" y2="189.4" stroke-width="1.3" stroke-dasharray="7 4" opacity="0.85"/>
    <path d="M70.0 196.2L71.9 187.9L77.3 180.9L85.6 175.1L96.3 170.5L108.8 166.9L122.8 164.3L137.6 162.6L153.1 161.9L168.7 161.9L184.1 162.6L199.0 164.1L213.1 166.1L226.2 168.7L238.0 171.8L248.3 175.3L256.9 179.2L263.8 183.3L268.8 187.7L271.8 192.3L272.8 196.9L271.8 201.6L268.8 206.2L263.8 210.8L256.9 215.1L248.3 219.1L238.0 222.9L226.2 226.2L213.1 229.1L199.0 231.4L184.1 233.1L168.7 234.1L153.1 234.3L137.6 233.7L122.8 232.2L108.8 229.8L96.3 226.3L85.6 221.7L77.3 216.0L71.9 209.0L70.0 200.8" stroke-width="1.8"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none"><polyline points="199,160.2 207,164.4 199,168.6"/><polyline points="207,227 199,231.2 207,235.4"/></g>
  <circle cx="70" cy="200.8" r="4.2" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
    <text x="540" y="22" text-anchor="end">P2 shoulder drive · n = 100 · Vs = 24 V</text>
    <text x="12" y="40">joint torque η·n·kt·i (N·m)</text>
    <text x="300" y="276" text-anchor="middle">joint speed (rad/s)</text>
    <text x="70" y="257" text-anchor="middle">0</text><text x="156.5" y="257" text-anchor="middle">0.5</text><text x="243.1" y="257" text-anchor="middle">1.0</text><text x="329.6" y="257" text-anchor="middle">1.5</text><text x="416.2" y="257" text-anchor="middle">2.0</text><text x="502.7" y="257" text-anchor="middle">2.5</text>
    <text x="61" y="244" text-anchor="end">0</text><text x="61" y="204" text-anchor="end">20</text><text x="61" y="164" text-anchor="end">40</text><text x="61" y="124" text-anchor="end">60</text><text x="61" y="84" text-anchor="end">80</text>
    <text x="86" y="73">current limit: 80 N·m at 10 A</text>
    <text x="298" y="57" opacity="0.8">on to 192 N·m at stall (off scale)</text>
    <text x="420" y="140">voltage line</text>
    <text x="420" y="154">τ = 192 − 80·(speed)</text>
    <text x="548" y="229" text-anchor="end">no-load 2.4</text>
    <text x="300" y="206" font-size="10.5">thermal limit 25.3</text>
    <text x="100" y="151">the lift: 0.5 rad in 0.8 s</text>
    <text x="84" y="216">← H: hold, 19.62 N·m, 2.45 A</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="12" y="294">The lift's loop stays inside the region; H is below the thermal line, so the hold can last.</text>
    <text x="12" y="308">At n = 200 the voltage line ends at 1.2 rad/s and the lift's 1.17 rad/s peak runs into it.</text>
  </g>
</svg>

The operating region of P2's shoulder on the $n=100$ drive, in joint units: the current limit flat at $80\,\mathrm{N{\cdot}m}$, the voltage line $\tau=192-80\,\dot\theta$ falling from its corner at $1.4\,\mathrm{rad/s}$ to the no-load speed $2.4\,\mathrm{rad/s}$, and the dashed thermal line at the continuous torque $25.3\,\mathrm{N{\cdot}m}$, above which the drive can stay only for seconds. The hold point H, $19.62\,\mathrm{N{\cdot}m}$ at $2.45\,\mathrm{A}$, sits under the thermal line, and the lift of §8 — the shoulder raised $0.5\,\mathrm{rad}$ in $0.8\,\mathrm{s}$ — traces a loop that climbs to $39.1\,\mathrm{N{\cdot}m}$ while it accelerates, passes $1.17\,\mathrm{rad/s}$ at $21.5\,\mathrm{N{\cdot}m}$ at mid-move, and ends at H without leaving the region.

### Worked case · 대상으로 한 번 끝까지

Hold P2 at its frozen pose through the $n=100$ drive, and follow one number, the shoulder's gravity torque, down to the winding and back out as heat. Then see what the drive did to the mass matrix. Six steps.

**Step 1 — what the joint must supply.** At rest the manipulator equation of [[02-foundations/manipulator-kinematics-dynamics|10. §5]] leaves $\tau=g(\theta)$, so the shoulder must supply $g_1=19.62\,\mathrm{N{\cdot}m}$ and the elbow nothing.

**Step 2 — through the gearbox.** With the motor driving, the gearbox multiplies torque by $\eta n$ (§2), so the motor must make

$$\tau_m=\frac{g_1}{\eta n}=\frac{19.62}{0.8\cdot100}=0.2453\,\mathrm{N{\cdot}m}$$

because $n=100$ divides the torque and $1/\eta=1.25$ adds a quarter on top: a lossless gearbox would need $0.1962$, and the other $0.0491\,\mathrm{N{\cdot}m}$ is the gearbox's cut. Strictly, this is the torque that *lifts* the arm through the pose; a gearbox at rest transmits no power, and §2 says why a stopped joint can be held with less. Drives are sized for lifting.

**Step 3 — the current.** Torque is current times the torque constant (§1), so

$$i=\frac{\tau_m}{k_t}=\frac{0.2453}{0.10}=2.4525\,\mathrm{A}$$

which is $24.5\%$ of the amplifier's $10\,\mathrm{A}$ and $77.6\%$ of the $3.162\,\mathrm{A}$ the winding can carry continuously — the current whose heat $i^2R$, flowing out through $R_{th}$, holds the winding exactly at its allowed $100\,\mathrm{K}$ rise, $\sqrt{100/(10\cdot1.0)}$ (§6 derives it).

**Step 4 — the voltage.** The terminal voltage splits three ways, $V=Ri+L\,di/dt+k_e\omega_m$: the resistance's drop, the inductance's drop and the back-EMF of the spinning rotor (§1). Nothing turns, so there is no back-EMF, and the current is steady, so there is no inductive drop; that leaves only $V=Ri=2.45\,\mathrm{V}$ of the $24\,\mathrm{V}$ supply.

**Step 5 — the heat.** The supply delivers $Vi=6.01\,\mathrm{W}$ and the arm does no work, so every one of those watts is heat, $P=i^2R=2.4525^2\cdot1.0=6.01\,\mathrm{W}$. Through the thermal resistance the winding settles at

$$\Delta T=R_{th}\,P=10\cdot6.01=60.1\,\mathrm{K}$$

above ambient, since in steady state the heat flowing out through $R_{th}$ must equal the heat being made. That is $85\,^\circ\mathrm{C}$ in a $25\,^\circ\mathrm{C}$ room and $60\%$ of the $100\,\mathrm{K}$ budget. **So yes, this drive holds P2 indefinitely** — at $78\%$ of its continuous torque but only $60\%$ of its heat budget, and the two percentages differ because heat goes as the square of current: $0.776^2=0.602$.

**Step 6 — what the drive did to the mass matrix.** The shoulder rotor turns $n=100$ times for each turn of link 1, so its kinetic energy is $\tfrac12J_m(n\dot\theta_1)^2$ and it adds $n^2J_m=10^4\cdot10^{-4}=1.0\,\mathrm{kg{\cdot}m^2}$ to $M_{11}$ (§4). The identical elbow drive adds the same to $M_{22}$ and $nJ_m=0.01$ to the off-diagonal entry:

$$M=\begin{pmatrix}3&1\\1&1\end{pmatrix}\ \longrightarrow\ \begin{pmatrix}4.0001&1.01\\1.01&2\end{pmatrix}\ \mathrm{kg{\cdot}m^2}$$

where the $0.0001$ is the elbow rotor riding along on link 1. Every entry is kinetic energy per squared joint rate, so the gearbox's losses do not appear in it. A rotor with $1/30{,}000$ of the shoulder's inertia has become a third of it, and at the elbow the drive has doubled the arm.

The problem set repeats these six steps at the pose where gravity is largest, and at another gear ratio.

### 1. Two equations, one motor

A DC motor is one electrical circuit and one rotating body, coupled by two constants. Write the circuit with Kirchhoff's voltage law, because the voltage the amplifier puts across the terminals has only three places to go — the winding's resistance, the change of current through its inductance, and the voltage the spinning rotor induces:

$$V=R\,i+L\,\frac{di}{dt}+k_e\,\omega_m$$

Write the rotor with Newton's second law for rotation, because the magnetic torque has three jobs too — it accelerates the rotor, turns the bearings, and whatever is left goes into the gearbox:

$$J_m\,\dot\omega_m=k_t\,i-b\,\omega_m-\tau_{in}$$

where $\omega_m$ is the motor speed, $i$ the winding current and $\tau_{in}$ the torque the motor shaft delivers into the gearbox, which §2 turns into the load. The two equations share $i$ and $\omega_m$, so the coupling runs both ways: current makes torque, and speed makes voltage.

> **The winding, defined.** The **winding** is the copper coil that carries the motor's current, and electrically it is a *series resistor–inductor pair* — two lumped parameters of the motor, not properties of the load or the controller. Two defining conditions, one per parameter. The **resistance** $R$ turns current into heat at the rate $i^2R$ and sets the current a stalled motor draws, $V/R$. The **inductance** $L$ stores the energy $\tfrac12Li^2$ and opposes changes in current, so current cannot jump when the voltage does; how long it takes is the electrical time constant of §5.
>
> $$V_R=R\,i,\qquad V_L=L\,\frac{di}{dt},\qquad P_{\text{heat}}=i^2R$$
>
> where $V_R$ and $V_L$ are the voltage drops across the two, $i$ the current and $P_{\text{heat}}$ the power dissipated — so $R$ is the only one of the pair that costs energy, because an inductor gives back what it stores.
> - **Example**: the frozen drive. $R=1.0\,\Omega$ means the Worked case's $2.4525\,\mathrm{A}$ costs $6.01\,\mathrm{W}$ of heat, and $L=1.0\,\mathrm{mH}$ means changing the current by $1\,\mathrm{A}$ in $1\,\mathrm{ms}$ takes $1\,\mathrm{V}$.
> - **Non-example**: "the motor's resistance is what limits its torque." A stalled motor on $24\,\mathrm{V}$ would draw $V_s/R=24\,\mathrm{A}$, but the amplifier stops at $10\,\mathrm{A}$ and the heat budget at $3.16\,\mathrm{A}$ continuous. Resistance sets the heat; the two limits of §3 and §6 set the torque.
> - **Why it matters**: $R$ is the heat term and $L$ the delay term. Every thermal number on this page comes from the first, and the reason a current loop can be fast but never instant comes from the second.

> **Torque constant and back-EMF constant, defined.** The **torque constant** $k_t$ and the **back-EMF constant** $k_e$ are *two proportionality constants of a permanent-magnet motor*, set by its magnets and its winding — not by the amplifier, the gearbox or the load. Three defining conditions. Torque is **proportional to current**, $\tau_m=k_ti$, for as long as the iron is not magnetically saturated (at very large currents $k_t$ falls). The voltage the winding develops is **proportional to speed**, $e=k_e\omega_m$, and it **opposes** the current that drives the motor forward, which is why it is called *back* EMF. And in SI units the two are **the same number**, because the electrical power the winding delivers against $e$ is exactly the mechanical power the rotor produces, $e\,i=\tau_m\omega_m$, so $k_e\omega_m i=k_t i\omega_m$.
>
> $$\tau_m=k_t\,i,\qquad e=k_e\,\omega_m,\qquad e\,i=\tau_m\,\omega_m\ \Rightarrow\ k_t=k_e$$
>
> where $\tau_m$ is the motor torque in $\mathrm{N{\cdot}m}$, $i$ the current in A, $\omega_m$ the motor speed in rad/s and $e$ the induced voltage in V — and the units agree too, since $1\,\mathrm{N{\cdot}m/A}=1\,\mathrm{J/(A{\cdot}rad)}=1\,\mathrm{V{\cdot}s/rad}$.
> - **Example**: the frozen drive, $k_t=k_e=0.10$. The Worked case's $2.4525\,\mathrm{A}$ makes $0.2453\,\mathrm{N{\cdot}m}$. At the lift's mid-move speed, $1.17\,\mathrm{rad/s}$ at the joint and so $117\,\mathrm{rad/s}$ at the motor, the winding develops $11.7\,\mathrm{V}$ of back-EMF.
> - **Non-example**: a datasheet quoting $10.5\,\mathrm{V}$ per $1000\,\mathrm{rpm}$, or its inverse, $95\,\mathrm{rpm/V}$. That is this same motor, since $0.10\,\mathrm{V{\cdot}s/rad}\times\tfrac{2\pi}{60}\times1000=10.47\,\mathrm{V/krpm}$; reading $10.5$ as $k_t$ in $\mathrm{N{\cdot}m/A}$ is an error of a factor $104.7$.
> - **Non-example**: "a motor with twice the $k_t$ is twice as good." Rewind the same motor with twice the turns of half-section wire: $k_t$ doubles and $R$ quadruples (twice the length, half the cross-section), so the heat for a given torque, $\tau_m^2R/k_t^2$, does not change. $k_t$ trades current for voltage; the magnetics and the copper decide torque per watt.
> - **Why it matters**: the first equation is why every drive closes a loop on *current* rather than voltage — current is torque — and the second is why speed costs voltage, which is the whole of §3's speed limit and of §7's shorted-motor brake.

The identity $k_t=k_e$ is the motor's power ledger: every watt that crosses the back-EMF on the electrical side, $e\,i$, reappears on the mechanical side as $\tau_m\omega_m$. §8 closes that ledger watt by watt at one instant of its lift, once the gearbox and the simulation that produce the numbers are in place.

### 2. The gearbox: ratio, efficiency, and the load seen from the motor

A lever or a gear trades force for distance, and the reflected inertia $n^2J_m$ follows from the rotor's kinetic energy; [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §9]] works both on P2's gearbox at the lossless ideal. This section adds the gearbox's efficiency and the load as the motor sees it.

> **Gear ratio, defined.** The **gear ratio** $n$ of a transmission is a *ratio of speeds*, motor turns per joint turn, and a *kinematic* number: it is fixed by the geometry of the teeth, not by the load, the speed, the direction of power flow or the losses. Two defining conditions. The motor and joint speeds are **locked in proportion** at every instant, $\omega_m=n\dot\theta$, because meshing teeth cannot slip. And for a train of simple meshing stages the ratio is **set by tooth counts**: in each stage the driven gear's count over the driving gear's, multiplied across the stages.
>
> $$n=\frac{\omega_m}{\dot\theta}=\prod_{k}\frac{N_{\text{driven},k}}{N_{\text{driving},k}}$$
>
> where $\omega_m$ is the motor speed, $\dot\theta$ the joint speed and $N_{\text{driven},k}$, $N_{\text{driving},k}$ the tooth counts of stage $k$ — so a reduction, the usual robot case, has $n>1$.
> - **Example**: the frozen drive's $n=100$ could be two stages of a 12-tooth pinion driving a 120-tooth gear, $10\times10$; the motor's $240\,\mathrm{rad/s}$ no-load speed becomes $2.4\,\mathrm{rad/s}$ at the joint.
> - **Non-example**: "a $100{:}1$ gearbox multiplies torque by $100$." The speed ratio is exact, but the torque ratio is $\eta n=80$ here, because the gearbox takes its cut of the power — the efficiency defined next.
> - **Why it matters**: $n$ enters speed and torque to the first power and everything the motor side contributes at the joint squared — reflected inertia (§4), holding heat (§6), backdrivability (§7) — so choosing it is the drive's main design decision (§8).

A capstan cable drive has a ratio of the same kind, set by drum radii instead of tooth counts; the haptics track's [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]] works that case, and nothing on this page needs it. *Modern Robotics* §8.9.1 notes that robot joints often use ratios of $100$ or more, because a motor that spins fast with little torque has to be traded down to a joint that turns slowly with a lot. What a real gearbox adds to the kinematics is loss.

> **Gearbox efficiency, defined.** The **efficiency** $\eta$ of a gearbox is a *ratio of powers* — output over input, a number between $0$ and $1$ — and a property of the gearbox *at an operating condition*: it varies with load, speed and temperature, and it is not a torque ratio until the kinematics make it one. Three defining conditions. It is a **power** ratio, $\eta=P_{\text{out}}/P_{\text{in}}$. Because the kinematic ratio is exact, $\omega_m=n\dot\theta$, it becomes a **torque** ratio, $\tau_{\text{out}}=\eta n\,\tau_{in}$. And it is declared for **one direction of power flow**, the motor driving the load; when the load drives the motor the loss sits on the other side, $\tau_{in}=\eta_b\,\tau_{\text{out}}/n$, with a backward efficiency $\eta_b$ that is usually lower and that reaches zero in a self-locking gearbox.
>
> $$\eta=\frac{P_{\text{out}}}{P_{\text{in}}}=\frac{\tau_{\text{out}}\,\dot\theta}{\tau_{in}\,\omega_m}=\frac{\tau_{\text{out}}}{n\,\tau_{in}}\qquad(\text{motor driving},\ \omega_m=n\dot\theta)$$
>
> where $\tau_{in}$ and $\omega_m$ are the torque and speed at the gearbox input (the motor shaft) and $\tau_{\text{out}}$ and $\dot\theta$ those at the output (the joint) — and the last form follows because $\omega_m/\dot\theta=n$ cancels the speeds.
> - **Example**: the Worked case. The joint needs $19.62\,\mathrm{N{\cdot}m}$, so the motor side needs $19.62/(0.8\cdot100)=0.2453\,\mathrm{N{\cdot}m}$ instead of the lossless $0.1962$ — a quarter more current and, since heat goes as current squared, $1/\eta^2=1.5625$ times the heat.
> - **Non-example**: reading $\eta$ at a standstill. A gearbox at rest transmits no power, so the ratio is undefined there; what holds a stopped arm is static friction, which supports any torque in a band. At rest the motor can hold the arm with anything from $\eta_b\,g_1/n$, just enough to stop it sagging, to $g_1/(\eta n)$, enough to lift it, and where the drive settles depends on the direction it arrived from. Sizing uses the second, because a drive that can only stop the arm falling cannot put it back.
> - **Why it matters**: every load-side torque, current and heat on this page carries a $1/\eta$ in the driving direction, and backdrivability (§7) is decided by $\eta_b$, which the forward efficiency does not tell you.

Now carry the load through. On the link side the gearbox must supply whatever the joint demands, $\tau_{\text{load}}$; for P2's shoulder with the elbow held, $\tau_{\text{load}}=M_{11}\ddot\theta_1+g_1(\theta_1)$. With the motor driving, $\tau_{\text{load}}=\eta n\,\tau_{in}$, so $\tau_{in}=\tau_{\text{load}}/(n\eta)$, and putting that into §1's rotor equation gives the drive's mechanical equation,

$$J_m\,\dot\omega_m=k_t\,i-\frac{\tau_{\text{load}}}{n\eta}-b\,\omega_m$$

because the torque that reaches the gearbox input is whatever the magnetic torque has left after accelerating the rotor and turning the bearings. Read it at the joint by putting $\omega_m=n\dot\theta_1$ and multiplying through by $n$:

$$\Big(n^2J_m+\frac{M_{11}}{\eta}\Big)\ddot\theta_1=n\,k_t\,i-n^2b\,\dot\theta_1-\frac{g_1(\theta_1)}{\eta}$$

so the joint's inertia, as the motor has to push it, is $J_{eq}=n^2J_m+M_{11}/\eta$, which is $1.0+3.75=4.75\,\mathrm{kg{\cdot}m^2}$ on the $n=100$ drive: the rotor enters at the energy value of §4, and the link and its gravity enter divided by $\eta$, because only what passes through the gearbox pays its toll. The right-hand side is written in *ideal-gear* units — $nk_ti$ is the torque a lossless gearbox would deliver — and the lab's controller asks for torque in the same units. Setting $\dot\theta_1=\ddot\theta_1=0$ gives $i=g_1/(\eta nk_t)$, the Worked case's Steps 2 and 3 in one line, and the lab's line `acc = ...` is this equation solved for $\ddot\theta_1$.

One regime condition, stated once: this is the equation of the motor *driving* the load. In §8's lift the link torque $M_{11}\ddot\theta_1+g_1$ stays positive while the arm rises — its smallest value in any row is $0.86\,\mathrm{N{\cdot}m}$, at $n=30$ — so power flows from motor to link for the whole rise, the direction the equation describes. The only reverse flow is the settle-back after each row's small overshoot at the end of the move, where the equation puts the loss on the wrong side; §8 says what that changes.

### 3. The torque–speed line, and what the gear ratio does to it

Two limits bound everything a drive can do, and both are electrical.

> **Supply voltage and current limit, defined.** The **supply voltage** $V_s$ and the **current limit** $I_{\max}$ are the *two bounds on what the amplifier can apply to the winding* — limits of the drive, not properties of the motor alone. Two defining conditions, one per bound. The terminal voltage is bounded, $|V|\le V_s$, because an amplifier can only switch the supply it is given across the winding. The current is bounded, $|i|\le I_{\max}$, because the amplifier, and well above that the motor's magnets and iron, must be protected; the amplifier enforces it by lowering the voltage whenever the current reaches the limit.
>
> $$|V|\le V_s,\qquad |i|\le I_{\max}\quad\Longrightarrow\quad |\tau_m|\le k_tI_{\max},\qquad \omega_m\le\frac{V_s-R\,i}{k_e}$$
>
> where the implications follow from §1: current is torque, so the current limit is a torque limit; and in steady state $V=Ri+k_e\omega_m$, so the voltage limit is a speed limit that tightens as the current, and with it the $Ri$ drop, rises.
> - **Example**: the frozen drive: $k_tI_{\max}=1.0\,\mathrm{N{\cdot}m}$ at the motor, and the fastest the unloaded motor can turn on $24\,\mathrm{V}$ is $240\,\mathrm{rad/s}$.
> - **Non-example**: "a 24 V motor." A motor has no supply voltage of its own; the number on its label is the voltage its winding was designed around. Running the same motor on $48\,\mathrm{V}$ doubles its no-load speed without changing its torque constant or its heat per newton-metre, and the problem set does exactly that.
> - **Why it matters**: $I_{\max}$ caps torque and $V_s$ caps speed, and a gear ratio can trade one for the other but cannot lift both — which is why the lab's sweep fails at both ends.

Inside those limits, the steady operating points of a motor at one voltage lie on a line.

> **Torque–speed line, defined.** The **torque–speed line** of a DC motor is a *boundary in the torque–speed plane*: the steady operating points reachable at one terminal voltage. It belongs to the motor and the voltage, not to the load or the controller, and it has two named ends. Three defining conditions. **Steady state**, so the current is not changing and the inductance drops out; **a fixed terminal voltage**, normally the supply $V_s$ at its limit; and **linear magnetics with friction neglected**, so $k_t$ and $k_e$ are constants.
>
> $$\tau_m=\frac{k_t}{R}\big(V-k_e\,\omega_m\big)=\tau_{\text{stall}}\Big(1-\frac{\omega_m}{\omega_0}\Big),\qquad \omega_0=\frac{V}{k_e},\qquad \tau_{\text{stall}}=\frac{k_tV}{R}$$
>
> which is §1's winding equation with $di/dt=0$, solved for $i=(V-k_e\omega_m)/R$ and multiplied by $k_t$ — so the line falls because every radian per second of speed spends $k_e$ volts of the supply on back-EMF. Its ends are the **no-load speed** $\omega_0$, where back-EMF has used the whole supply and no current, so no torque, remains, and the **stall torque** $\tau_{\text{stall}}$, at zero speed, where nothing but $R$ limits the current.
> - **Example**: the frozen drive on $V_s=24\,\mathrm{V}$: $\omega_0=240\,\mathrm{rad/s}$ ($2292\,\mathrm{rpm}$) and $\tau_{\text{stall}}=2.4\,\mathrm{N{\cdot}m}$ at $24\,\mathrm{A}$. The current limit cuts the line at $1.0\,\mathrm{N{\cdot}m}$, and the corner where the two meet is at $\omega_m=(V_s-RI_{\max})/k_e=140\,\mathrm{rad/s}$.
> - **Non-example**: "the stall torque is the motor's torque rating." Stall is the point where every watt is heat — $24\,\mathrm{A}$ through $1\,\Omega$ is $576\,\mathrm{W}$, in a winding whose continuous budget is $10\,\mathrm{W}$ — and this amplifier cannot even reach it. The rating that means *indefinitely* is §6's continuous torque.
> - **Why it matters**: a gear ratio moves this line, torque up by $\eta n$ and speed down by $n$, so the whole sizing trade fits in one picture, the one at the top of the page.

At the joint, $\tau_j=\eta n\tau_m$ and $\dot\theta=\omega_m/n$, so the same line reads

$$\tau_j=\frac{\eta nk_t}{R}\big(V_s-k_en\,\dot\theta\big)$$

because the gearbox multiplies the motor's torque by $\eta n$ and divides its speed by $n$. Three things move with $n$, and not at the same rate. The current limit $\eta nk_tI_{\max}$ rises as $n$; the no-load speed $V_s/(k_en)$ falls as $1/n$; and the slope of the voltage line, $\eta n^2k_tk_e/R$, steepens as $n^2$. On the $n=100$ drive those are $80\,\mathrm{N{\cdot}m}$, $2.4\,\mathrm{rad/s}$ and $80\,\mathrm{N{\cdot}m}$ per rad/s — the line $\tau_j=192-80\,\dot\theta$ of the picture at the top of the page. Double the ratio and the region doubles in height and halves in width: $160\,\mathrm{N{\cdot}m}$ and $1.2\,\mathrm{rad/s}$ at $n=200$.

Now place the lift on it. At mid-move the lift asks for $1.17\,\mathrm{rad/s}$ against about $21.4\,\mathrm{N{\cdot}m}$ of gravity. At $n=100$ the voltage line offers $192-80\cdot1.17=98\,\mathrm{N{\cdot}m}$ there, capped at $80$ by the current: ample. At $n=200$ the same speed spends $0.1\cdot200\cdot1.17=23.4\,\mathrm{V}$ on back-EMF alone, and the line offers $9.0\,\mathrm{N{\cdot}m}$ against the $21.8$ the lift needs, so that row of §8's sweep must hit the supply.

### 4. Reflected inertia at a revolute joint, and why it can dominate

> **Reflected inertia, defined.** The **reflected inertia** of a motor behind a transmission is *the inertia its rotor contributes at the output* — a property of the rotor and the ratio alone, not of the load, the controller or whether the drive is powered. Three defining conditions. It is fixed by **equal kinetic energy**: it is the inertia that, turning at the output's speed, stores what the rotor stores at its own speed. It **grows as the square of the ratio**, because the rotor turns $n$ times as fast as the output and kinetic energy goes as speed squared. And it is **present with the power off**, because it is mass in motion, not a control effect. At a revolute joint the derivation is one line: the shoulder's stator is bolted to the base and its rotor turns at $\omega_m=n\dot\theta_1$, so
>
> $$\tfrac12J_m\,\omega_m^2=\tfrac12J_m\,(n\dot\theta_1)^2=\tfrac12\,\big(n^2J_m\big)\,\dot\theta_1^2\quad\Longrightarrow\quad J_{\text{refl}}=n^2J_m$$
>
> which is the kinetic energy of an inertia $n^2J_m$ turning at the joint's own speed, with $J_m$ the rotor inertia and $\dot\theta_1$ the joint speed.
> - **Example**: the frozen drive at $n=100$: $10^4\cdot10^{-4}=1.0\,\mathrm{kg{\cdot}m^2}$ at the shoulder, a third of the arm's own $M_{11}=3$ — the Worked case's Step 6.
> - **Non-example**: the $J=J_m+M_{11}/(\eta n^2)$ of §5. That is the reflection the other way, the *link* seen from the *motor* shaft, divided by $n^2$ and taxed by $\eta$ because it passes through the gearbox; it is the right inertia for the motor's time constant and the wrong one for the arm's mass matrix.
> - **Why it matters**: it is the one drive parameter that changes the arm's dynamics and not only its limits. It enters the mass matrix, the tip's apparent mass and the impact force below, and past a ratio this section computes it outweighs the arm itself.

That is what the rotor adds to $M_{11}$, exactly and with no efficiency in it, because the mass matrix is kinetic energy and friction stores none. *Modern Robotics* §8.9.2 calls it apparent inertia and derives it the same way; the capstan version is optional further reading in [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]].

The elbow drive is subtler, because its stator rides on link 1. Its rotor's absolute speed is $\dot\theta_1+n\dot\theta_2$, and squaring that splits the rotor's energy three ways,

$$\tfrac12J_m(\dot\theta_1+n\dot\theta_2)^2=\tfrac12J_m\dot\theta_1^2+nJ_m\,\dot\theta_1\dot\theta_2+\tfrac12n^2J_m\dot\theta_2^2$$

so, reading the coefficients off the quadratic form as [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8 §2]] does, it adds $J_m$ to $M_{11}$, $nJ_m$ to $M_{12}$ and $n^2J_m$ to $M_{22}$ — the Worked case's matrix, with its $4.0001$ and its $1.01$.

**Why it can dominate.** The rotor is tiny and $n^2$ is huge, and the contest between them is one ratio,

$$\frac{n^2J_m}{M_{ii}}=1\quad\Longleftrightarrow\quad n=\sqrt{M_{ii}/J_m}$$

since that is where the rotor's reflected inertia equals the arm's own at joint $i$. On the frozen drive the shoulder reaches parity at $n=\sqrt{3/10^{-4}}=173$ and the elbow at $n=\sqrt{1/10^{-4}}=100$, so the elbow of the $n=100$ arm sits exactly at parity, and at $n=300$ the shoulder's rotor is $9\,\mathrm{kg{\cdot}m^2}$, three times the arm. Three consequences follow.

- **The mass matrix becomes more diagonal.** Coupling, measured as $M_{12}/\sqrt{M_{11}M_{22}}$, falls from $0.577$ on the bare arm to $0.357$ at $n=100$ and $0.094$ at $n=300$; *Modern Robotics* §8.9.2 makes the same observation, that at high ratio each joint feels mostly its own rotor. The configuration dependence that [[02-foundations/manipulator-kinematics-dynamics|10. §3]] measured as a ratio of five shrinks with it: $M_{11}$ runs from $1$ folded to $5$ straight on the bare arm, from $2$ to $6$ at $n=100$, and from $10$ to $14$ at $n=300$, a ratio of $1.4$. A fixed-gain joint controller meets a nearly constant inertia on a highly geared arm, and pays for it elsewhere.
- **The tip gets heavier, and impacts get harder.** A push straight up at the tip meets the reciprocal of the $yy$ entry of $JM^{-1}J^\top$, the inverse-mass reading of [[02-foundations/manipulator-kinematics-dynamics|10. §6]]: $2.0\,\mathrm{kg}$ on the bare arm, $3.49\,\mathrm{kg}$ with the $n=100$ drives, $11.9\,\mathrm{kg}$ at $n=300$. Since peak impact force goes as the square root of that mass, the $5\,\mathrm{cm/s}$ touchdown of [[04-robotics/force-compliance-control|13. §5]] rises from $22.4\,\mathrm{N}$ to $29.5\,\mathrm{N}$ at $n=100$ and $54.5\,\mathrm{N}$ at $n=300$ — and an impact that is over in milliseconds leaves the controller no time to hide that inertia, which is there with the power off.
- **Inertia matching: where more ratio stops buying acceleration.** Leaving gravity aside, the motor torque needed per unit of joint acceleration comes from the joint equation of §2 divided by $n$,

  $$\tau_m=\Big(nJ_m+\frac{M_{11}}{\eta n}\Big)\ddot\theta_1\quad\Longrightarrow\quad n^\ast=\sqrt{\frac{M_{11}}{\eta J_m}}$$

  because setting its derivative in $n$ to zero leaves $J_m=M_{11}/(\eta n^2)$. At $n^\ast=193.6$ the rotor's $n^{\ast2}J_m=3.75$ equals the link's $M_{11}/\eta$: below it the link dominates and more ratio helps, above it the motor spends the extra on its own rotor. The minimum, $2\sqrt{J_mM_{11}/\eta}=0.0387\,\mathrm{N{\cdot}m}$ per rad/s², is shallow — $0.0475$ at $n=100$ and $0.0425$ at $n=300$ — which is why gravity (§6) and speed (§3), not inertia matching, usually decide the ratio.

### 5. Two time constants, and why the current loop comes first

A motor has two speeds of its own, one per equation of §1, and how far apart they are decides how its controller is built. The electrical one, $L/R$, is also why a PWM drive leaves only a small ripple in the winding's current, which the lab of [[02-foundations/basic-circuits-electronics|0.6.2 §12]] sweeps.

> **Electrical and mechanical time constants, defined.** A **time constant** is the *time* a first-order response takes to cover $1-e^{-1}=63\%$ of a step — the reciprocal of one real pole. A motor has two, one per equation of §1, and each is defined with the other subsystem held out of the way. The **electrical time constant** $\tau_e=L/R$ is how fast current settles after a voltage step with the rotor held still. The **mechanical time constant** $\tau_{\text{mech}}=JR/(k_tk_e)$ is how fast speed settles after a voltage step with $L$ neglected, where back-EMF acts as a damper $k_tk_e/R$ and $J$ is *everything* the motor accelerates, referred to its shaft.
>
> $$\tau_e=\frac{L}{R},\qquad \tau_{\text{mech}}=\frac{J\,R}{k_t\,k_e},\qquad J=J_m+\frac{M_{11}}{\eta\,n^2}$$
>
> where the mechanical one comes from putting $i=(V-k_e\omega_m)/R$ into $J\dot\omega_m=k_ti$: that gives $J\dot\omega_m=k_tV/R-(k_tk_e/R)\,\omega_m$, a first-order lag whose pole is $k_tk_e/(JR)$.
> - **Example**: the frozen drive. $\tau_e=1.0\,\mathrm{ms}$. The rotor alone gives $\tau_{\text{mech}}=10\,\mathrm{ms}$; with P2's shoulder on the $n=100$ gearbox, $J=10^{-4}+3/(0.8\cdot10^4)=4.75\times10^{-4}\,\mathrm{kg{\cdot}m^2}$ and $\tau_{\text{mech}}=47.5\,\mathrm{ms}$.
> - **Non-example**: "the current loop's bandwidth is $R/L$." $R/L=1000\,\mathrm{rad/s}$ is where the *uncontrolled* winding's pole sits. A PI current loop cancels that pole and closes wherever its gain puts it — $2000\,\mathrm{rad/s}$ here — up to limits set by the switching and sampling rate and by the voltage left over, not by $L/R$.
> - **Why it matters**: $\tau_{\text{mech}}$ can never fall below the rotor-alone $J_mR/(k_tk_e)=10\,\mathrm{ms}$, whatever the gear ratio or the load, so current settles at least ten times faster than speed can change. That separation is the licence for the cascade below.

A **cascade** closes the fast loop inside the slow one: the inner loop regulates current, and so torque, and the outer loop regulates position by asking the inner one for current. The inner loop here is a PI controller whose zero cancels the winding's pole,

$$C_i(s)=K_{pi}+\frac{K_{ii}}{s},\qquad \frac{K_{ii}}{K_{pi}}=\frac{R}{L}\ \Longrightarrow\ \frac{i}{i_{\text{ref}}}=\frac{\omega_{ci}}{s+\omega_{ci}},\qquad \omega_{ci}=\frac{K_{pi}}{L}$$

because the loop gain $C_i(s)\cdot1/(Ls+R)$ collapses to $K_{pi}/(Ls)$ once the zero sits on the pole, and the back-EMF is a slow disturbance the integrator removes. With $\omega_{ci}=2000\,\mathrm{rad/s}$ ($318\,\mathrm{Hz}$), $K_{pi}=L\omega_{ci}=2\,\mathrm{V/A}$ and $K_{ii}=R\omega_{ci}=2000\,\mathrm{V/(A{\cdot}s)}$, run at $20\,\mathrm{kHz}$ with the conditional-integration anti-windup of [[04-robotics/control-theory-ce397|5. Control Theory §7]]. The outer PD runs at $1\,\mathrm{kHz}$ and is tuned to $20\,\mathrm{rad/s}$, a hundred times slower, so it sees the inner loop as a torque source — the separation the box licenses, with room to spare.

Where the licence expires is voltage. The current loop can only move current by spending voltage on $L\,di/dt$, and what it has to spend is $V_s-Ri-k_en\dot\theta$. At the lift's mid-move speed on the $n=200$ drive the back-EMF alone is $23.4\,\mathrm{V}$ of the $24$, so the current loop loses its authority exactly when the joint is fastest. That is the mechanism behind the $V_s$ flags in §8: speed saturation is the current loop running out of voltage.

### 6. Continuous versus peak: heat decides

Holding a load does no mechanical work (the energy ledger of [[02-foundations/basic-mechanics|0.6.1 §6]]), so a drive that holds still turns all of its electrical power into heat — and heat, not current, is what a winding cannot survive. The winding heats at $i^2R$ and loses heat to its surroundings through a thermal resistance; in the simplest, one-node model its temperature rise $\Delta T$ obeys

$$C_{th}\,\frac{d\,\Delta T}{dt}=i^2R-\frac{\Delta T}{R_{th}}\quad\Longrightarrow\quad \Delta T(t)=R_{th}\,i^2R\,\big(1-e^{-t/\tau_{th}}\big),\qquad \tau_{th}=R_{th}C_{th}$$

because the heat stored in the winding's thermal capacity $C_{th}$ is the heat made minus the heat that flows out, and the solution starts at ambient. Steady state is $\Delta T=R_{th}\,i^2R$, and requiring that to stay under the allowed rise gives the continuous rating.

> **Continuous and peak torque, defined.** The **continuous torque** and the **peak torque** are *two torque ratings of a drive, each set by a different physics*. Continuous is a **thermal** rating: the torque whose $i^2R$ heat, through the thermal resistance, holds the winding exactly at its allowed rise in steady state — a property of motor, cooling and ambient together. Peak is a **current** rating: the torque at the current limit, available only for a time the thermal time constant sets. Two defining conditions, one per rating, and a third that ties them: a torque above the continuous rating must be quoted **with a duration**.
>
> $$\tau_{\text{cont}}=k_t\sqrt{\frac{\Delta T_{\max}}{R_{th}R}},\qquad \tau_{\text{peak}}=k_tI_{\max}$$
>
> $$t_{\text{allowed}}=-\tau_{th}\ln\!\Big(1-\frac{\Delta T_{\max}}{R_{th}\,i^2R}\Big)$$
>
> where the first comes from setting $R_{th}i^2R=\Delta T_{\max}$ and solving it for $k_ti$, and the last from solving $\Delta T(t)=\Delta T_{\max}$ on the curve above for a start at ambient — defined only when $R_{th}i^2R>\Delta T_{\max}$, since otherwise the limit is never reached.
> - **Example**: the frozen drive: $I_{\text{cont}}=\sqrt{100/(10\cdot1)}=3.162\,\mathrm{A}$, so $\tau_{\text{cont}}=0.316\,\mathrm{N{\cdot}m}$ and $\tau_{\text{peak}}=1.0\,\mathrm{N{\cdot}m}$; at the $n=100$ joint, $25.3$ and $80\,\mathrm{N{\cdot}m}$. At the full $10\,\mathrm{A}$ the winding makes $100\,\mathrm{W}$ and reaches its limit after $t=-60\ln(1-100/1000)=6.3\,\mathrm{s}$.
> - **Non-example**: the same hold at $n=50$. It needs $4.905\,\mathrm{A}$, above continuous and far below peak, so the arm *does* stay up — for $-60\ln(1-100/240.6)=32.2\,\mathrm{s}$, after which the winding is at its limit and still rising. "It held the arm in the demo" is a statement about the first half-minute.
> - **Why it matters**: a static pose costs $i^2R$ and $i$ falls as $1/n$, so holding heat falls as $1/n^2$ — the gear ratio is the cheapest cooling a joint has. The continuous hold of P2 needs $n\ge g_1/(\eta k_tI_{\text{cont}})=77.6$.

**Moves are judged by their RMS.** The lift's loop in the picture at the top of the page spends a good part of its length above the thermal line, and that is allowed: heat integrates $i^2$, so over a duty cycle short against $\tau_{th}$ what the thermal line bounds is the root-mean-square current, $I_{\text{rms}}=\sqrt{\tfrac1T\int_0^Ti^2\,dt}\le I_{\text{cont}}$. The lift's demand, repeated back to back, has $I_{\text{rms}}=3.11\,\mathrm{A}$, which is $98\%$ of continuous; add a $4.2\,\mathrm{s}$ hold after each lift and the five-second cycle falls to $2.57\,\mathrm{A}$.

**The resistance moves with the heat.** Copper's resistance rises about $0.39\%$ per kelvin, so a hot winding makes more heat at the same current. Folding that into the Worked case, the hold's rise solves $\Delta T=R_{th}i^2R_0(1+\alpha\Delta T)$, so $\Delta T=60.1/(1-0.0039\cdot60.1)=78.6\,\mathrm{K}$ — still inside the budget, but a rise $31\%$ larger than the constant-$R$ estimate. The rest of this page holds $R$ fixed.

### 7. Backdrivability at a geared joint

> **Backdrivability, defined.** **Backdrivability** is *how easily a push at the output moves a transmission and the motor behind it* — a property of the mechanism, not of a controller. Three defining conditions. It is **measured at the output**, as the torque (on a linear axis, the force) a push must supply to move the joint over and above what the link's own inertia and gravity take. It is **quoted with a motion**, the speed and acceleration it was measured at, because its terms scale with both. And it is **passive**: the drive is unpowered, with the state of its windings, open or shorted, stated, because a controller can hide friction slowly but not within the milliseconds of an impact. At a geared joint each motor-side impedance — the rotor's inertia, the bearings' viscous friction and, if the windings are shorted, the electrical damping of §1's back-EMF — is a torque proportional to motor motion, and because both the motion and the torque are scaled by $n$ on the way through, each arrives multiplied by $n^2$:
>
> $$\tau_{\text{bd}}=n^2J_m\,\ddot\theta+n^2b\,\dot\theta+\tau_{\text{gear}}\qquad\Big(+\;n^2\frac{k_tk_e}{R}\,\dot\theta\ \ \text{if the windings are shorted}\Big)$$
>
> where $\dot\theta$ and $\ddot\theta$ are the joint speed and acceleration of the push, $\tau_{\text{gear}}$ is the gearbox's own friction, and the gearbox is taken as ideal (the paragraph below adds its losses).
> - **Example**: P2's shoulder on the $n=100$ drive, open windings, pushed at $1\,\mathrm{rad/s^2}$ through $0.5\,\mathrm{rad/s}$: $\tau_{\text{bd}}=1.0+0.05=1.05\,\mathrm{N{\cdot}m}$ before gearbox friction (the first bullet below).
> - **Non-example**: "the joint is torque-controlled, so it is backdrivable." That is active compliance, which the definition excludes: it needs power and a loop, and it cannot act within an impact, where the passive $n^2J_m$ is what the environment meets.
> - **Why it matters**: it decides whether a person can move the arm by hand, how hard an impact is, and whether current can be read as torque — the paragraph after the bullets.

In that formula $\tau_{\text{bd}}$ is the torque a push at the joint must supply on top of the link's own inertia and gravity, for an ideal gearbox, and $\tau_{\text{gear}}$ is the gearbox's own friction — which the single $\eta$ of §2 does not describe at light load and which tends to grow with ratio (*Modern Robotics* §8.9.4). A lossy gearbox also divides the motor-side terms by its backward efficiency $\eta_b$, and a gearbox whose $\eta_b$ reaches zero cannot be backdriven at all; a self-locking worm gear is that extreme.

- **Open windings, a person pushing.** Accelerating P2's shoulder at $1\,\mathrm{rad/s^2}$ through $0.5\,\mathrm{rad/s}$ costs the push $1.0+0.05=1.05\,\mathrm{N{\cdot}m}$ for the $n=100$ drive before any gearbox friction, on top of the arm's own $M_{11}\ddot\theta=3\,\mathrm{N{\cdot}m}$ — a third more. At $n=300$ the drive's share is $9.45\,\mathrm{N{\cdot}m}$, three times the arm.
- **Shorted windings, the arm released.** Some drives short the windings when disabled (dynamic braking); the back-EMF then drives a braking current, and at the joint the damping is $n^2k_tk_e/R=100\,\mathrm{N{\cdot}m{\cdot}s/rad}$ at $n=100$. Released at its pose, P2 sinks at the speed where that damping balances gravity, $19.62/100=0.196\,\mathrm{rad/s}$ or about $11^\circ/\mathrm{s}$ (ideal gearbox, after a brief transient), and at $0.0218\,\mathrm{rad/s}$ at $n=300$. A shorted motor is a brake that works only while the joint moves: it slows the arm and never stops it.

**What this means for reading current as torque.** A drive that estimates its joint torque from its current, $\hat\tau=\eta nk_ti$, is assuming the rotor and friction terms away. At the lift's peak acceleration, $4.51\,\mathrm{rad/s^2}$, the link needs $35.5\,\mathrm{N{\cdot}m}$; the current-based estimate reads $39.1$ at $n=100$, $10\%$ high, and $68.3$ at $n=300$, $93\%$ high, because the rotor's $n^2J_m\ddot\theta$ is in the current and not in the link. Low-ratio drives keep that error small and pay in holding heat, which is §6's trade seen from the sensing side. Wensing et al. (2017) build a legged robot's actuators around this choice, controlling force collocated at the joint and quantifying backdrivability at impact with the impact mitigation factor defined below. The torque-based impedance control of [[04-robotics/force-compliance-control|13. §2]] is helped by exactly this kind of drive — a responsive torque interface on a backdrivable joint — and that page's admittance branch is the one written for robots that expose only position or velocity commands.

> **Impact mitigation factor, defined.** The **impact mitigation factor** (IMF) of Wensing et al. (2017) is a *dimensionless score of backdrivability at impact* for a floating-base robot, such as a legged one — a property of its masses and reflected rotor inertias at one contact point and one configuration, not of its controller. Two inertias define it: $\Lambda$, the inertia felt at the contact point with the joints free to move (reflected rotor inertias included), and $\Lambda_L$, the same with every joint locked, so the robot lands as one rigid body. At equal impact velocity the free robot takes the impulse $\Lambda\Lambda_L^{-1}$ times the locked one, so $I-\Lambda\Lambda_L^{-1}$ is the part the free joints remove, and the factor is its determinant:
>
> $$\xi=\det\!\big(I-\Lambda\,\Lambda_L^{-1}\big),\qquad 0\le\xi\le1$$
>
> where $\xi=1$ means the free dynamics remove the whole impulse and $\xi\to0$ as $\Lambda\to\Lambda_L$, the joints behaving as if locked; $\Lambda$ and $\Lambda_L$ are operational-space inertias in the sense of [[02-foundations/manipulator-kinematics-dynamics|10. §6]], matrices over the contact's directions and plain masses for a single direction.
> - **Example**: a one-dimensional hopper, a body of $m_b=10\,\mathrm{kg}$ on a foot of $m_f=1\,\mathrm{kg}$, with the actuator's rotor reflected to the leg joint between them as a mass $m_r$. Locked, the foot lands with $\Lambda_L=11\,\mathrm{kg}$. Free, it lands with $\Lambda=m_f+m_bm_r/(m_b+m_r)$, the foot plus body and rotor in series: $1\,\mathrm{kg}$ and $\xi=1-1/11=0.91$ for a direct drive ($m_r=0$), $6\,\mathrm{kg}$ and $\xi=1-6/11=0.45$ for a geared drive with $m_r=10\,\mathrm{kg}$.
> - **Non-example**: P2. Its base is bolted to the ground, so locking its joints makes the tip immovable, $\Lambda_L^{-1}=0$ and $\xi=1$ for every drive, which says nothing. For a fixed-base arm the comparison is the tip mass of §4 directly — $2.0$, $3.49$ and $11.9\,\mathrm{kg}$.
> - **Why it matters**: normalised by the locked robot, it puts legged robots of different sizes and gear ratios on one scale, and it rises as the gear ratio falls, which is the quantitative case for the low-ratio drives of the MIT Cheetah.

### 8. The lab: a cascade on P2's shoulder, and the gear-ratio sweep

The task is the lift: P2's shoulder, elbow held at $90^\circ$, raised from $\theta_1=-0.5\,\mathrm{rad}$ to the frozen pose $\theta_1=0$ along a quintic time scaling of $T=0.8\,\mathrm{s}$ ([[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9 §2]]; peak speed $1.875\,\Delta\theta/T=1.17\,\mathrm{rad/s}$ and peak acceleration $5.77\,\Delta\theta/T^2=4.51\,\mathrm{rad/s^2}$), then held. The lift is deliberately faster than the actuator limits [[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]] freezes for P2 ($0.8\,\mathrm{rad/s}$, $2\,\mathrm{rad/s^2}$): those are a specification a planner stays inside, and this lab asks what one particular drive can do beyond them — at $n=100$ it has headroom, and at $n=200$ the $1.17\,\mathrm{rad/s}$ peak meets the voltage line. The controller is §5's cascade. A PD position loop at $1\,\mathrm{kHz}$ with gravity feedforward asks for torque in ideal-gear units, so its feedforward is $g_1/\eta$; it is designed once, for $n=100$ — $20\,\mathrm{rad/s}$ and critically damped on $J_{eq}=4.75$ — and kept for every ratio, as a controller tuned for one gearbox would be. Inside it runs the PI current loop at $20\,\mathrm{kHz}$ with the limits $V_s$ and $I_{\max}$. The plant is §1–§2: the winding equation stepped with explicit Euler and the joint with semi-implicit Euler ([[02-foundations/lab-kernel|0.7 §2 and §3]]), both at the current loop's $50\,\mu\mathrm{s}$. Velocity is measured perfectly and the PWM is replaced by its average voltage, two idealizations that flatter the loop.

```python
import numpy as np

# P2's shoulder in the vertical plane, elbow held at 90 deg, driven through this page's frozen drive
R, L, kt, ke = 1.0, 1.0e-3, 0.10, 0.10    # ohm, H, N*m/A, V*s/rad
Jm, b, eta = 1.0e-4, 1.0e-5, 0.80         # rotor kg*m^2, motor friction N*m*s/rad, gearbox efficiency
Vs, Imax = 24.0, 10.0                     # supply voltage (V), amplifier current limit (A)
Rth, dTmax, tau_th = 10.0, 100.0, 60.0    # thermal resistance K/W, allowed rise K, thermal time constant s
M11 = 3.0                                 # P2's shoulder entry of M at theta2 = 90 deg (kg*m^2)
def g1(th): return 9.81*(2*np.cos(th) - np.sin(th))   # P2's shoulder gravity torque, elbow at 90 deg

th0, th1, Tm = -0.5, 0.0, 0.8             # the lift: 0.5 rad in 0.8 s, ending at P2's frozen pose
Ti, Tp, t_end = 5e-5, 1e-3, 2.0           # current loop 20 kHz, position loop 1 kHz, run length
Kpi, Kii = L*2000.0, R*2000.0             # PI current loop: cancels R/L, closes at 2000 rad/s
J100 = 100**2*Jm + M11/eta                # PD designed once, for n = 100: 20 rad/s, critically damped,
Kp, Kd = J100*20.0**2, 2*J100*20.0        # then kept unchanged for every gear ratio in the sweep

def ref(t):                               # quintic (minimum-jerk) time scaling
    s = min(t/Tm, 1.0); d = th1 - th0
    return th0 + d*(10*s**3 - 15*s**4 + 6*s**5), d*(30*s**2 - 60*s**3 + 30*s**4)/Tm

def run(n):
    Jeq = n*n*Jm + M11/eta                # inertia the motor accelerates, referred to the joint
    th, w = th0, 0.0
    i = min(g1(th0)/(eta*n*kt), Imax); z = R*i; i_ref = i    # start at rest, holding th0
    Vpk = epk = t_done = 0.0; hitI = hitV = False
    for k in range(int(round(t_end/Ti))):
        t = k*Ti
        if k % int(round(Tp/Ti)) == 0:                        # position loop: PD + gravity feedforward
            r, rd = ref(t)
            u = Kp*(r - th) + Kd*(rd - w) + g1(th)/eta        # joint torque in ideal-gear units, n*kt*i
            hitI |= abs(u/(n*kt)) > Imax
            i_ref = np.clip(u/(n*kt), -Imax, Imax)
            epk = max(epk, abs(r - th))
        e = i_ref - i                                         # current loop: PI with anti-windup
        v = Kpi*e + z
        V = np.clip(v, -Vs, Vs); hitV |= abs(v) > Vs
        if abs(v) < Vs or e*v < 0: z += Kii*e*Ti
        di = (V - R*i - ke*n*w)/L                             # winding: V = R i + L di/dt + ke n w
        acc = (n*kt*i - n*n*b*w - g1(th)/eta)/Jeq             # rotor, gearbox and link in one line
        i += Ti*di; w += Ti*acc; th += Ti*w                   # explicit Euler on i, semi-implicit on w, th
        Vpk = max(Vpk, abs(V))
        if abs(th1 - th) > 2e-3: t_done = t                   # last instant more than 2 mrad from the target
    dT = Rth*R*i*i                                            # steady winding rise if the hold lasts
    t_hold = -tau_th*np.log(1 - dTmax/dT) if dT > dTmax else np.inf
    return n*n*Jm/Jeq, Vs/(ke*n), i, dT, t_hold, Vpk, 1e3*epk, t_done, hitI, hitV

print("  n  rotor  w0/n  i_hold    dT   t_hold  V_pk  e_pk  t_done  I_sat V_sat")
for n in (30, 50, 80, 100, 150, 200, 300):
    s, w0n, ih, dT, th_, Vpk, epk, td, hI, hV = run(n)
    print(f"{n:3d} {s:6.3f} {w0n:5.2f} {ih:7.3f} {dT:6.1f} {th_:7.1f} {Vpk:5.1f} {epk:6.1f} {td:6.3f}  {hI!s:5} {hV!s:5}")
```

**The sweep.** Seven gear ratios, everything else frozen. "Rotor share" is $n^2J_m/J_{eq}$; "hold rise" is the steady winding rise at the final current; "done at" is the last instant the arm was more than $2\,\mathrm{mrad}$ from the target, against a reference that itself ends at $0.8\,\mathrm{s}$.

| $n$ | rotor share | $\omega_0/n$ (rad/s) | hold current (A) | hold rise (K) | peak voltage (V) | peak error (mrad) | done at (s) | limit reached |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 30 | 0.023 | 8.00 | 8.175 | 668.3 | 12.5 | 340.7 | 1.392 | $I_{\max}$ in the lift; thermal, hold lasts 9.7 s |
| 50 | 0.062 | 4.80 | 4.905 | 240.6 | 13.2 | 8.3 | 0.898 | thermal, hold lasts 32.2 s |
| 80 | 0.146 | 3.00 | 3.066 | 94.0 | 13.8 | 9.2 | 0.905 | none (94 of 100 K) |
| 100 | 0.211 | 2.40 | 2.453 | 60.1 | 15.3 | 10.0 | 0.911 | none |
| 150 | 0.375 | 1.60 | 1.635 | 26.7 | 20.6 | 13.1 | 0.927 | none |
| 200 | 0.516 | 1.20 | 1.226 | 15.0 | 24.0 | 19.5 | 0.944 | $V_s$ |
| 300 | 0.706 | 0.80 | 0.818 | 6.7 | 24.0 | 118.3 | 1.124 | $V_s$ |

**Reading the sweep.** Four things the equations could not have told you on their own.

- **Holding current falls as $1/n$ and holding heat as $1/n^2$.** Across a tenfold ratio the hold current goes from $8.175$ to $0.818\,\mathrm{A}$ and the steady rise from $668$ to $6.7\,\mathrm{K}$, a hundredfold. The two rows below $n=77.6$ hold P2 only for a while, $9.7$ and $32.2\,\mathrm{s}$ from ambient, and $n=30$ cannot even lift it on schedule: $I_{\max}$ caps that joint at $24\,\mathrm{N{\cdot}m}$ against $21.9$ of gravity, leaving about $2\,\mathrm{N{\cdot}m}$ to accelerate the arm, so it trails the reference by up to $0.34\,\mathrm{rad}$ ($19.5^\circ$) and arrives about $0.6\,\mathrm{s}$ late.
- **The rotor takes over the joint.** The rotor's share of $J_{eq}$ climbs from $2\%$ to $71\%$, and with the PD fixed at the $n=100$ design the peak error climbs with it — $8.3$, $9.2$, $10.0$, $13.1\,\mathrm{mrad}$ through the rows no limit touches — because a heavier joint on the same gains is a slower, less damped loop; at $n=300$ its damping ratio is $0.61$.
- **Speed runs out at the top.** The joint's no-load speed $\omega_0/n$ falls toward the lift's $1.17\,\mathrm{rad/s}$, and with the $Ri$ drop the supply is first touched at $n=178$. At $n=200$ the loop rides the $24\,\mathrm{V}$ limit for $0.21\,\mathrm{s}$ around mid-move, but the speed it can reach there, $1.13\,\mathrm{rad/s}$, is only just short of the reference's $1.17$, so the error grows only to $19.5\,\mathrm{mrad}$. At $n=300$ it rides the limit for $0.49\,\mathrm{s}$ and the joint tops out at $0.77\,\mathrm{rad/s}$ — the voltage line's speed at the holding current, $(24-0.9)/(0.1\cdot300)$ — so the arm trails by $118\,\mathrm{mrad}$ and finishes $0.32\,\mathrm{s}$ late.
- **The window, and what the model gets wrong at its edges.** Heat closes it below $n\approx78$ and the supply above $n\approx178$; $n=100$ sits inside with a $60\,\mathrm{K}$ hold and $8.7\,\mathrm{V}$ of headroom. Every row but $n=30$ ends slightly past the target — up to $16\,\mathrm{mrad}$, at $n=200$ — and settles back at under $0.12\,\mathrm{rad/s}$. In that settle-back the link drives the gearbox, where §2's single $\eta$ puts the loss on the wrong side; a real gearbox's static friction could stop the arm before it settles, held by less current than the table shows. The table's hold currents are the lifting values $g_1/(\eta nk_t)$, the ones a drive is sized by.

**The power ledger at one instant.** §1's identity $k_t=k_e$, closed watt by watt on the $n=100$ run. At $t=0.40\,\mathrm{s}$ the joint turns at $1.226\,\mathrm{rad/s}$, the current is $2.824\,\mathrm{A}$ and the amplifier applies $15.05\,\mathrm{V}$ (print $\dot\theta$, $i$ and $V$ inside `run` at step `k == 8000` to see them). The supply delivers $Vi=42.5\,\mathrm{W}$: $i^2R=8.0\,\mathrm{W}$ heats the winding, $0.1\,\mathrm{W}$ comes back out of the inductance as the current falls, and $e\,i=k_en\dot\theta\,i=0.1\cdot100\cdot1.226\cdot2.824=34.6\,\mathrm{W}$ crosses the back-EMF. On the mechanical side $k_ti\,\omega_m$ is the same $34.6\,\mathrm{W}$ — that equality *is* $k_t=k_e$ — of which $0.5\,\mathrm{W}$ spins up the rotor and turns its bearings, and the remaining $34.1\,\mathrm{W}$ enters the gearbox, which keeps $1-\eta=20\%$ of it, $6.8\,\mathrm{W}$, and passes $27.3\,\mathrm{W}$ to the link to lift it and speed it up. Sixty-four percent of what left the supply did the job.

### 9. Reading actuator claims in a paper

| The paper says | Ask |
|---|---|
| "rated torque" or "maximum torque" | Continuous or peak? At what ambient, cooling and duty, and for how long does the peak last? |
| "payload of so many kilograms" | At which pose, which sets the moment arm, held for how long, and at what speed? A payload quoted folded is a different arm at full reach. |
| "joint torque estimated from motor current" | The gear ratio, the gearbox efficiency in both directions, the friction model, and whether the rotor's $n^2J_m\ddot\theta$ was removed during acceleration. |
| "backdrivable" or "transparent" | The backdrive torque with speed and acceleration stated (§7), the power state — open or shorted windings — and the reflected inertia $n^2J_m$. |
| "high-bandwidth torque control" | Current-loop bandwidth is not joint-torque bandwidth: friction, gear compliance and the rotor sit between the two. |
| "maximum speed" | At what supply voltage and what load? The voltage line moves with both. |

### After reading

- [ ] Write the winding and rotor equations of a DC motor, and say why $k_t=k_e$ in SI units.
- [ ] Turn a joint torque into motor torque, current, voltage, heat and temperature rise for a given $n$ and $\eta$.
- [ ] Draw a joint's torque–speed region for a gear ratio, and place a hold and a move on it.
- [ ] Add a geared rotor to a mass matrix, and say at what ratio it matches the arm.
- [ ] Say why the current loop comes first, with both time constants in numbers.
- [ ] Distinguish continuous from peak torque, and compute how long a hold above the continuous rating lasts.
- [ ] Explain what a gear ratio does to backdrivability and to reading current as torque.

### Self-check

1. You double the gear ratio of a joint that is holding a load at rest. What happens to the holding current, the holding heat, the rotor's reflected inertia, and the joint's no-load speed?
2. A datasheet gives a back-EMF constant of $10.5\,\mathrm{V/krpm}$. What is the torque constant in $\mathrm{N{\cdot}m/A}$, and why is no second measurement needed?
3. Why can the current loop be designed as though the arm were not there, and the position loop as though the current loop were instant?
4. A demo shows a joint holding a heavy tool out at arm's length for ten seconds. What single number would you ask for before believing the joint can do it all day?
5. Why does a highly geared arm with shorted windings sink slowly when released, instead of falling — and why can it never hold still that way?

> [!tip]- Answers
> 1. Holding current halves, since $i=g_1/(\eta nk_t)$; holding heat falls to a quarter, since it goes as $i^2$; reflected inertia quadruples, since it goes as $n^2$; and the joint's no-load speed halves, since it is $V_s/(k_en)$. One knob, four answers — which is why the sweep in §8 has a window rather than a best end.
> 2. Convert units: $10.5\,\mathrm{V}$ per $1000\,\mathrm{rpm}$ is $10.5/(1000\cdot2\pi/60)=0.100\,\mathrm{V{\cdot}s/rad}$, and in SI the torque constant is the same number, $0.100\,\mathrm{N{\cdot}m/A}$. No second measurement is needed because $k_t=k_e$ is a statement of power conservation, $e\,i=\tau_m\omega_m$, not a property of one motor.
> 3. Because their time scales are far apart. The winding settles in $\tau_e=L/R=1\,\mathrm{ms}$ and the closed current loop in $0.5\,\mathrm{ms}$, while speed cannot settle faster than the rotor-alone $10\,\mathrm{ms}$ and the position loop is tuned to $20\,\mathrm{rad/s}$ against the current loop's $2000$. Each loop sees the other as either frozen or instant. The licence expires when the voltage runs out.
> 4. The continuous torque at that pose, or equivalently the steady winding rise: the hold current against $I_{\text{cont}}$. Ten seconds is inside the thermal time constant; the frozen drive at $n=50$ would pass a ten-second demo of P2 and reach its limit at $32\,\mathrm{s}$.
> 5. Shorting the windings lets the back-EMF drive a current that brakes the rotor, a damping of $k_tk_e/R$ at the motor and $n^2$ times that at the joint — $100\,\mathrm{N{\cdot}m{\cdot}s/rad}$ at $n=100$, so P2 sinks at about $0.2\,\mathrm{rad/s}$. The braking torque is proportional to speed, so it vanishes when the joint stops: it can slow a fall but never hold a pose.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and the object catalog: P2 and the frozen drive as in the Running object, with the changes each item names.

1. **Draw.** The picture above, for the $n=200$ drive: its current limit, its voltage line with both ends, its thermal line, and the hold point H. Then add the lift's mid-move demand, $1.17\,\mathrm{rad/s}$ at $21.8\,\mathrm{N{\cdot}m}$, and say which boundary it crosses.
2. **Derive.** (a) P2 at the pose where the shoulder's gravity torque is largest, $\theta=(-26.57^\circ,\,90^\circ)$, with $g_1=9.81\sqrt5=21.94\,\mathrm{N{\cdot}m}$ (differentiate $2\cos\theta_1-\sin\theta_1$ to find it), on the $n=100$ drive: the motor torque, current, voltage, heat and steady rise. Does it hold indefinitely? (b) The smallest whole gear ratio that holds that pose continuously. (c) At $n=160$, the mass matrix at $\theta_2=90^\circ$ with both drives, and its coupling $M_{12}/\sqrt{M_{11}M_{22}}$. (d) Derive the ratio $n^\ast$ that minimizes the motor torque per unit of shoulder acceleration, gravity aside; evaluate it, and show that at $n^\ast$ the rotor's $n^2J_m$ equals $M_{11}/\eta$. (e) The mechanical time constant at $n=200$, and its ratio to $\tau_e$.
3. **Do.** Replace `run` in the lab code of §8 with the template below, fill every `?`, set `Vs = 48.0`, and rerun the seven-ratio sweep. Report which rows change and which do not, and explain why the $n=300$ row's peak error falls while its "done at" gets later.

```python
# Tier A template: paste over run() in the lab code of §8, set Vs = 48.0, fill every ?, rerun the sweep.
def run(n):
    Jeq = ?                                                   # rotor at its energy value + link through the gearbox
    th, w = th0, 0.0
    i = min(g1(th0)/(eta*n*kt), Imax); z = R*i; i_ref = i
    Vpk = epk = t_done = 0.0; hitI = hitV = False
    for k in range(int(round(t_end/Ti))):
        t = k*Ti
        if k % int(round(Tp/Ti)) == 0:
            r, rd = ref(t)
            u = Kp*(r - th) + Kd*(rd - w) + ?                 # gravity feedforward, in ideal-gear units
            hitI |= abs(u/(n*kt)) > Imax
            i_ref = ?                                         # current request, clipped to the amplifier
            epk = max(epk, abs(r - th))
        e = i_ref - i
        v = Kpi*e + z
        V = np.clip(v, -Vs, Vs); hitV |= abs(v) > Vs
        if abs(v) < Vs or e*v < 0: z += Kii*e*Ti
        di = ?                                                # winding equation solved for di/dt
        acc = ?                                               # joint equation solved for the acceleration
        i += Ti*di; w += Ti*acc; th += Ti*w
        Vpk = max(Vpk, abs(V))
        if abs(th1 - th) > 2e-3: t_done = t
    dT = ?                                                    # steady winding rise at the final current
    t_hold = -tau_th*np.log(1 - dTmax/dT) if dT > dTmax else np.inf
    return n*n*Jm/Jeq, Vs/(ke*n), i, dT, t_hold, Vpk, 1e3*epk, t_done, hitI, hitV
```

> [!note]- How to draw it · 그리는 법
> - **The axes are joint quantities**: joint speed $\dot\theta_1$ across, and the torque the drive delivers to the link, $\eta nk_ti$, up. A plot in motor units would hide the only knob this page turns.
> - **The current limit is a flat line** at $\eta nk_tI_{\max}$, because the amplifier caps current and current is torque.
> - **The voltage line slopes down** from its corner on the current limit, at $(V_s-RI_{\max})/(k_en)$, to the joint's no-load speed $V_s/(k_en)$; label both ends. Carried on, it would reach $\eta nk_tV_s/R$ at zero speed, but the current limit cuts it first (§3).
> - **The thermal line is dashed**, at the continuous torque $\eta nk_tI_{\text{cont}}$ with $I_{\text{cont}}=3.162\,\mathrm{A}$: the region above it is open only for seconds (§6).
> - **H sits on the torque axis** at $g_1=19.62\,\mathrm{N{\cdot}m}$ whatever the ratio; label it with its current $g_1/(\eta nk_t)$ and check which side of the thermal line it falls on.
> - **A move is drawn as the loop its demand traces**, as the picture draws the lift: up from gravity while it accelerates, through mid-move, down while it brakes, into H. A single demand point is judged by the boundary it lies beyond — above the flat line is the current limit, past the sloping line the voltage limit.
> - **Check the scaling**: the current limit rises as $n$, the no-load speed falls as $1/n$ and the voltage line's slope steepens as $n^2$ (§3), so doubling the ratio must make the region twice as tall and half as wide.

> [!tip]- Solutions
> 1. Current limit $\eta nk_tI_{\max}=0.8\cdot200\cdot0.1\cdot10=160\,\mathrm{N{\cdot}m}$. Voltage line $\tau_j=(0.8\cdot200\cdot0.1/1)(24-0.1\cdot200\,\dot\theta)=384-320\,\dot\theta$, from the corner at $(384-160)/320=0.7\,\mathrm{rad/s}$ down to the no-load speed $1.2\,\mathrm{rad/s}$. Thermal line $0.8\cdot200\cdot0.1\cdot3.162=50.6\,\mathrm{N{\cdot}m}$, meeting the voltage line at $1.042\,\mathrm{rad/s}$. H at $19.62\,\mathrm{N{\cdot}m}$, now $1.226\,\mathrm{A}$. The region is twice as tall and half as wide as at $n=100$. The mid-move demand lies outside it, through the voltage line: at $1.17\,\mathrm{rad/s}$ the line offers $384-320\cdot1.1719=9.0\,\mathrm{N{\cdot}m}$ against the $21.8$ needed.
> 2. (a) $\tau_m=21.94/(0.8\cdot100)=0.2742\,\mathrm{N{\cdot}m}$, $i=2.742\,\mathrm{A}$, $V=Ri=2.74\,\mathrm{V}$, $P=i^2R=7.52\,\mathrm{W}$, $\Delta T=R_{th}P=75.2\,\mathrm{K}$. Under $100\,\mathrm{K}$, so yes, indefinitely, at $75\%$ of the heat budget. (b) $n\ge21.94/(0.8\cdot0.1\cdot3.162)=86.7$, so $n=87$. (c) $n^2J_m=2.56$ and $nJ_m=0.016$, so $M=\begin{pmatrix}5.5601&1.016\\1.016&3.56\end{pmatrix}$ and the coupling is $1.016/\sqrt{5.5601\cdot3.56}=0.228$, against $0.577$ bare. (d) $\tau_m=(nJ_m+M_{11}/(\eta n))\ddot\theta_1$; setting $d/dn$ to zero gives $J_m-M_{11}/(\eta n^2)=0$, so $n^\ast=\sqrt{M_{11}/(\eta J_m)}=\sqrt{3/(0.8\cdot10^{-4})}=193.6$, and there $n^{\ast2}J_m=3.75=M_{11}/\eta$. (e) $J=10^{-4}+3/(0.8\cdot4\cdot10^4)=1.9375\times10^{-4}\,\mathrm{kg{\cdot}m^2}$, so $\tau_{\text{mech}}=JR/(k_tk_e)=19.4\,\mathrm{ms}$, $19$ times $\tau_e$ — still clear of the ten-times floor.
> 3. Blanks: `Jeq = n*n*Jm + M11/eta`, `g1(th)/eta`, `i_ref = np.clip(u/(n*kt), -Imax, Imax)`, `di = (V - R*i - ke*n*w)/L`, `acc = (n*kt*i - n*n*b*w - g1(th)/eta)/Jeq`, `dT = Rth*R*i*i`. At $48\,\mathrm{V}$ the rows $n=30$ to $150$ are unchanged except that $\omega_0/n$ doubles ($16.00$, $9.60$, $6.00$, $4.80$, $3.20$): the voltage never bound there, and the thermal rows keep their $9.7$ and $32.2\,\mathrm{s}$, because heat is current and voltage does not touch it. $n=200$ loses its flag (peak $26.8\,\mathrm{V}$, error $17.5\,\mathrm{mrad}$, done at $0.942\,\mathrm{s}$), and so does $n=300$ (peak $41.1\,\mathrm{V}$, error $31.8\,\mathrm{mrad}$, done at $1.169\,\mathrm{s}$). The $n=300$ error falls from $118.3$ to $31.8\,\mathrm{mrad}$ because the joint can now reach the lift's speed; it finishes later, $1.169$ against $1.124\,\mathrm{s}$, because it now overshoots by $30.9\,\mathrm{mrad}$ instead of $13.0$ — the PD designed for $4.75\,\mathrm{kg{\cdot}m^2}$ runs on $12.75$ at a damping ratio of $0.61$, and at $24\,\mathrm{V}$ the voltage limit had been hiding that by capping the speed. Voltage buys speed; it buys neither holding nor a lighter joint.

### Sources

- K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — §8.9 "Actuation, Gearing, and Friction": the DC motor's voltage equation, the speed–torque curve and its current and voltage limits, gearing with efficiency, apparent (reflected) inertia and the more diagonal mass matrix, and gearhead friction. The free preprint is linked from [[04-robotics/modern-robotics-book|the book guide]].
- P. M. Wensing, A. Wang, S. Seok, D. Otten, J. Lang and S. Kim, "Proprioceptive Actuator Design in the MIT Cheetah: Impact Mitigation and High-Bandwidth Physical Interaction for Dynamic Legged Robots," *IEEE Transactions on Robotics*, vol. 33, no. 3, pp. 509–522, 2017. DOI 10.1109/TRO.2016.2640183. Cited for force control collocated at the joints and for the impact mitigation factor, its §III-B3, eqs. (33)–(35).
- Within this wiki: [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] for $M$, $g$ and $\Lambda$; [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8]] for the mass matrix as kinetic energy; [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]] for the same trade on a capstan; [[04-robotics/force-compliance-control|13. Force & Compliance Control]] for what a backdrivable drive is for.
- The drive's values are illustrative, and every number on this page was computed here from them and from P2's catalog values; recompute them rather than trusting them.

## 한국어

*P2(카탈로그의 평면 2링크 팔, [[02-foundations/lab-plants|0.6]])의 $M$과 $g$는 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]] 위에, PD·대역폭·anti-windup은 [[04-robotics/control-theory-ce397|5. 제어 이론]] 위에 선다. 액추에이터를 embodiment의 일부로 꼽기만 하고 열어 보지는 않는 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §2]] 옆에 놓인다. 다시 쓰는 장치는 **P2**. 이제 관절마다 모터와 기어박스가 달려 있다.*

> [!note] 처음이라면 · First pass
> 이 페이지의 대상, 그림, 계산 절을 먼저 읽어라. 관절 토크 하나가 암페어·볼트·와트·켈빈으로 바뀌고, 눈에 보이지 않는 회전자 하나가 P2 질량 행렬의 원소 하나를 바꾼다. 그다음 두 방정식의 §1, 토크–속도 선의 §3, 반사 관성의 §4, 그리고 관절이 무엇을 버틸 수 있는지를 전류가 아니라 열이 정하는 이유인 §6. §2·§5·§7은 구동계에 관해 읽을 때가 아니라 고를 때 연다. §8은 랩, §9는 논문 읽기 점검표다.

### 이 페이지의 대상 · Running object

대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**. 연직면에 세우고 $g=9.81\,\mathrm{m/s^2}$를 $-y$ 방향으로 두며, 고정 자세 $\theta=(0^\circ,90^\circ)$에 놓는다. 팔꿈치는 $(1,0)$, 전완은 똑바로 위, 말단은 $(1,1)\,\mathrm{m}$. 이 페이지 전체를 끌고 가는 숫자는 둘이고, 둘 다 [[02-foundations/manipulator-kinematics-dynamics|10. §3과 §5]]에서 유도했다. 어깨의 질량 행렬 원소 $M_{11}=3\,\mathrm{kg{\cdot}m^2}$와 어깨의 중력 토크 $g_1=19.62\,\mathrm{N{\cdot}m}$다. 이 자세에서 팔꿈치의 중력 토크는 $0$인데, 전완 질량이 팔꿈치 바로 위에 있기 때문이다.

이제 관절마다 **구동계**(drive)가 붙는다. DC 모터, 그 모터에 전력을 주는 증폭기, 그리고 모터와 링크 사이의 기어박스다. 카탈로그에는 구동계가 없으므로 이 페이지가 하나를 완전히 정의하고 고정한다. 값은 **예시용**: 작은 팔 관절에 맞는 크기로 이 페이지가 고른 것이고, 어떤 제품의 데이터시트에서 가져온 것이 아니다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $R$ | $1.0\,\Omega$ | 권선 저항(§1) |
| $L$ | $1.0\,\mathrm{mH}$ | 권선 인덕턴스(§1) |
| $k_t$ | $0.10\,\mathrm{N{\cdot}m/A}$ | 토크 상수(§1) |
| $k_e$ | $0.10\,\mathrm{V{\cdot}s/rad}$ | 역기전력 상수. §1이 유도하듯 $k_t$와 같은 숫자 |
| $J_m$ | $1.0\times10^{-4}\,\mathrm{kg{\cdot}m^2}$ | 모터 축에 대한 회전자 관성. 기어박스 입력단 포함 |
| $b$ | $1.0\times10^{-5}\,\mathrm{N{\cdot}m{\cdot}s/rad}$ | 모터 축의 점성 마찰(베어링) |
| $n$ | $100$. §8에서 $30$부터 $300$까지 바꿔 본다 | 감속비. 관절 한 바퀴당 모터 회전수(§2) |
| $\eta$ | $0.80$ | 모터가 구동할 때의 기어박스 효율(§2) |
| $V_s$ | $24\,\mathrm{V}$ | 공급 전압(§3) |
| $I_{\max}$ | $10\,\mathrm{A}$ | 증폭기 전류 한계(§3) |
| $R_{th}$ | $10\,\mathrm{K/W}$ | 권선–주변 열저항, 단일 노드 모델(§6) |
| $\Delta T_{\max}$ | $100\,\mathrm{K}$ | 허용되는 권선 온도 상승(주변 대비)(§6) |
| $\tau_{th}$ | $60\,\mathrm{s}$ | 그 노드의 열 시정수(§6) |

모델링 선택 셋을 한 번만 적어 둔다. **두 구동계는 똑같고**, 관절마다 하나씩이다. **구동계가 팔에 더하는 것은 회전자의 자전 관성뿐이다.** 구동계의 질량은 카탈로그의 점질량 안에 들어 있다고 본다. 그래서 받침에 볼트로 고정된 어깨 구동계는 질량을 더하지 않고, 팔꿈치 구동계의 질량은 팔꿈치의 $1\,\mathrm{kg}$에 포함된다. **전기 모델은 브러시 DC 모터의 것이다.** 전류 제어기 아래의 브러시리스 모터도 같은 꼴의 식을 따르고, *Modern Robotics* §8.9.1도 같은 단순화를 한다. 랩(§8)에서는 팔꿈치 구동계가 팔꿈치를 $90^\circ$에 붙잡고 어깨만 움직이므로, 어깨는 정확히 $M_{11}$과 $g_1(\theta_1)=9.81\,(2\cos\theta_1-\sin\theta_1)\,\mathrm{N{\cdot}m}$를 본다. 10번 페이지의 $g_1$에서 $\theta_2$를 $90^\circ$로 고정한 것이다.

*범위: 이 페이지는 P2의 한 관절에 달린 기어 달린 DC 구동계 하나를 가르친다. 전기 방정식과 기계 방정식, 토크–속도 선, 반사 관성과 그것이 질량 행렬에 하는 일, 전류 루프를 정당화하는 두 시정수, 열 한계와 전류 한계, 역구동성, 그리고 이것들을 한데 묶는 감속비의 맞바꿈이다. 모터 설계(자기 회로, 권선, 정류), 전력 전자(PWM 브리지, field-oriented control), 유압 구동, 관절 유연성, 마찰 동정은 가르치지 않는다. 이 모터를 모는 PWM 브리지와 회로로 본 모터는 [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자 §6–§7]]이, 건설 기계의 유압 실린더는 [[02-foundations/fluid-power|0.6.3 유체 동력]]이 다룬다. 역구동 가능한 토크 제어 구동계를 접촉에 쓰는 제어기는 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]이고, 같은 맞바꿈의 캡스턴 판, 즉 햅틱 핸들 위의 이야기는 햅틱 트랙 뒤쪽의 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]이며 여기에는 필요 없다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="기어비 100에서 P2 어깨 구동계의 관절 토크 대 관절 속도: 전류 한계, 전압선, 열 한계선, 유지점, 들어올리기의 요구 고리">
  <path d="M70 240 L70 80 L312.3 80 L485.4 240 Z" fill="currentColor" fill-opacity="0.07"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none">
    <line x1="70" y1="240" x2="530" y2="240"/><line x1="70" y1="240" x2="70" y2="48"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45">
    <line x1="156.5" y1="240" x2="156.5" y2="245"/><line x1="243.1" y1="240" x2="243.1" y2="245"/><line x1="329.6" y1="240" x2="329.6" y2="245"/><line x1="416.2" y1="240" x2="416.2" y2="245"/><line x1="502.7" y1="240" x2="502.7" y2="245"/>
    <line x1="65" y1="200" x2="70" y2="200"/><line x1="65" y1="160" x2="70" y2="160"/><line x1="65" y1="120" x2="70" y2="120"/><line x1="65" y1="80" x2="70" y2="80"/>
  </g>
  <g stroke="currentColor" fill="none">
    <line x1="70" y1="80" x2="312.3" y2="80" stroke-width="2.2"/>
    <line x1="312.3" y1="80" x2="485.4" y2="240" stroke-width="2.2"/>
    <line x1="312.3" y1="80" x2="290.7" y2="60" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.6"/>
    <line x1="70" y1="189.4" x2="430.7" y2="189.4" stroke-width="1.3" stroke-dasharray="7 4" opacity="0.85"/>
    <path d="M70.0 196.2L71.9 187.9L77.3 180.9L85.6 175.1L96.3 170.5L108.8 166.9L122.8 164.3L137.6 162.6L153.1 161.9L168.7 161.9L184.1 162.6L199.0 164.1L213.1 166.1L226.2 168.7L238.0 171.8L248.3 175.3L256.9 179.2L263.8 183.3L268.8 187.7L271.8 192.3L272.8 196.9L271.8 201.6L268.8 206.2L263.8 210.8L256.9 215.1L248.3 219.1L238.0 222.9L226.2 226.2L213.1 229.1L199.0 231.4L184.1 233.1L168.7 234.1L153.1 234.3L137.6 233.7L122.8 232.2L108.8 229.8L96.3 226.3L85.6 221.7L77.3 216.0L71.9 209.0L70.0 200.8" stroke-width="1.8"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none"><polyline points="199,160.2 207,164.4 199,168.6"/><polyline points="207,227 199,231.2 207,235.4"/></g>
  <circle cx="70" cy="200.8" r="4.2" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
    <text x="540" y="22" text-anchor="end">P2 어깨 구동계 · n = 100 · Vs = 24 V</text>
    <text x="12" y="40">관절 토크 η·n·kt·i (N·m)</text>
    <text x="300" y="276" text-anchor="middle">관절 속도 (rad/s)</text>
    <text x="70" y="257" text-anchor="middle">0</text><text x="156.5" y="257" text-anchor="middle">0.5</text><text x="243.1" y="257" text-anchor="middle">1.0</text><text x="329.6" y="257" text-anchor="middle">1.5</text><text x="416.2" y="257" text-anchor="middle">2.0</text><text x="502.7" y="257" text-anchor="middle">2.5</text>
    <text x="61" y="244" text-anchor="end">0</text><text x="61" y="204" text-anchor="end">20</text><text x="61" y="164" text-anchor="end">40</text><text x="61" y="124" text-anchor="end">60</text><text x="61" y="84" text-anchor="end">80</text>
    <text x="86" y="73">전류 한계: 10 A에서 80 N·m</text>
    <text x="298" y="57" opacity="0.8">정지 토크 192 N·m까지 이어짐 (축 밖)</text>
    <text x="420" y="140">전압선</text>
    <text x="420" y="154">τ = 192 − 80·(속도)</text>
    <text x="548" y="229" text-anchor="end">무부하 2.4</text>
    <text x="300" y="206" font-size="10.5">열 한계 25.3</text>
    <text x="100" y="151">들어올리기: 0.8 s 동안 0.5 rad</text>
    <text x="84" y="216">← H: 유지, 19.62 N·m, 2.45 A</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="12" y="294">들어올리기의 고리는 영역 안에 있고, H는 열 한계선 아래라 유지가 계속될 수 있다.</text>
    <text x="12" y="308">n = 200이면 전압선이 1.2 rad/s에서 끝나고, 1.17 rad/s 최고 속도가 그 선에 부딪힌다.</text>
  </g>
</svg>

$n=100$ 구동계를 단 P2 어깨의 운전 영역을 관절 단위로 그렸다. 전류 한계는 $80\,\mathrm{N{\cdot}m}$의 수평선, 전압선 $\tau=192-80\,\dot\theta$는 $1.4\,\mathrm{rad/s}$의 모서리에서 무부하 속도 $2.4\,\mathrm{rad/s}$까지 내려가고, 점선의 열 한계선은 연속 토크 $25.3\,\mathrm{N{\cdot}m}$에 있어 그 위에는 몇 초 동안만 머물 수 있다. 유지점 H($19.62\,\mathrm{N{\cdot}m}$, $2.45\,\mathrm{A}$)는 열 한계선 아래에 있고, §8의 들어올리기 — 어깨를 $0.8\,\mathrm{s}$에 $0.5\,\mathrm{rad}$ 올리는 동작 — 는 가속하는 동안 $39.1\,\mathrm{N{\cdot}m}$까지 오르고 중간에서 $1.17\,\mathrm{rad/s}$, $21.5\,\mathrm{N{\cdot}m}$를 지나 H에서 끝나는 고리를 그리며, 영역을 벗어나지 않는다.

### 대상으로 한 번 끝까지 · Worked case

$n=100$ 구동계로 P2를 고정 자세에 붙잡고, 숫자 하나 — 어깨의 중력 토크 — 를 권선까지 따라 내려갔다가 열이 되어 나오는 데까지 따라간다. 그다음 구동계가 질량 행렬에 무슨 일을 했는지 본다. 여섯 단계.

**1단계 — 관절이 내야 하는 것.** 정지 상태에서 [[02-foundations/manipulator-kinematics-dynamics|10. §5]]의 매니퓰레이터 방정식은 $\tau=g(\theta)$만 남기므로, 어깨는 $g_1=19.62\,\mathrm{N{\cdot}m}$를 내야 하고 팔꿈치는 아무것도 내지 않는다.

**2단계 — 기어박스를 거쳐.** 모터가 구동할 때 기어박스는 토크를 $\eta n$배 한다(§2). 그래서 모터가 만들어야 하는 토크는

$$\tau_m=\frac{g_1}{\eta n}=\frac{19.62}{0.8\cdot100}=0.2453\,\mathrm{N{\cdot}m}$$

이다. $n=100$이 토크를 나누고 $1/\eta=1.25$가 4분의 1을 얹기 때문이다. 손실 없는 기어박스라면 $0.1962$면 되고, 나머지 $0.0491\,\mathrm{N{\cdot}m}$는 기어박스의 몫이다. 엄밀히 말해 이것은 팔을 그 자세로 *들어 올리는* 토크다. 정지한 기어박스는 일률을 전달하지 않으며, 멈춘 관절을 더 적은 토크로 붙잡을 수 있는 이유는 §2가 말한다. 구동계는 들어 올리기를 기준으로 고른다.

**3단계 — 전류.** 토크는 전류 곱하기 토크 상수이므로(§1)

$$i=\frac{\tau_m}{k_t}=\frac{0.2453}{0.10}=2.4525\,\mathrm{A}$$

이고, 이것은 증폭기의 $10\,\mathrm{A}$의 $24.5\%$, 권선이 연속으로 흘릴 수 있는 $3.162\,\mathrm{A}$의 $77.6\%$다. 연속 전류란 그 열 $i^2R$이 $R_{th}$를 거쳐 빠져나가며 권선을 허용 상승 $100\,\mathrm{K}$에 딱 맞춰 두는 전류, $\sqrt{100/(10\cdot1.0)}$이다(유도는 §6).

**4단계 — 전압.** 단자 전압은 세 곳으로 나뉜다. $V=Ri+L\,di/dt+k_e\omega_m$, 곧 저항의 강하, 인덕턴스의 강하, 도는 회전자의 역기전력이다(§1). 아무것도 돌지 않으니 역기전력이 없고, 전류가 일정하니 인덕턴스에 걸리는 전압도 없다. 그래서 $24\,\mathrm{V}$ 공급 중 $V=Ri=2.45\,\mathrm{V}$만 남는다.

**5단계 — 열.** 공급은 $Vi=6.01\,\mathrm{W}$를 내고 팔은 아무 일도 하지 않으므로, 그 와트가 전부 열이 된다. $P=i^2R=2.4525^2\cdot1.0=6.01\,\mathrm{W}$. 열저항을 거쳐 권선은

$$\Delta T=R_{th}\,P=10\cdot6.01=60.1\,\mathrm{K}$$

만큼 주변보다 뜨거운 곳에 자리 잡는다. 정상 상태에서는 $R_{th}$를 거쳐 빠져나가는 열이 만들어지는 열과 같아야 하기 때문이다. $25\,^\circ\mathrm{C}$ 방이라면 $85\,^\circ\mathrm{C}$이고, $100\,\mathrm{K}$ 예산의 $60\%$다. **그러니 이 구동계는 P2를 무기한 붙잡는다.** 연속 토크의 $78\%$를 쓰지만 열 예산은 $60\%$만 쓰는데, 두 비율이 다른 것은 열이 전류의 제곱으로 가기 때문이다. $0.776^2=0.602$.

**6단계 — 구동계가 질량 행렬에 한 일.** 어깨 회전자는 링크 1이 한 바퀴 돌 때 $n=100$바퀴 돌므로, 운동 에너지가 $\tfrac12J_m(n\dot\theta_1)^2$이고 $M_{11}$에 $n^2J_m=10^4\cdot10^{-4}=1.0\,\mathrm{kg{\cdot}m^2}$를 더한다(§4). 똑같은 팔꿈치 구동계는 $M_{22}$에 같은 양을, 비대각 원소에 $nJ_m=0.01$을 더한다.

$$M=\begin{pmatrix}3&1\\1&1\end{pmatrix}\ \longrightarrow\ \begin{pmatrix}4.0001&1.01\\1.01&2\end{pmatrix}\ \mathrm{kg{\cdot}m^2}$$

여기서 $0.0001$은 링크 1에 올라타 함께 도는 팔꿈치 회전자다. 모든 원소는 관절 속도 제곱당 운동 에너지이므로 기어박스의 손실은 여기에 나타나지 않는다. 어깨 관성의 $1/30{,}000$밖에 안 되는 회전자가 그 3분의 1이 되었고, 팔꿈치에서는 구동계가 팔을 두 배로 만들었다.

과제는 이 여섯 단계를 중력이 가장 큰 자세와 다른 감속비에서 되풀이한다.

### 1. 방정식 둘, 모터 하나

DC 모터는 전기 회로 하나와 회전체 하나이고, 둘을 상수 두 개가 잇는다. 회로는 키르히호프 전압 법칙으로 쓴다. 증폭기가 단자에 건 전압은 권선의 저항, 인덕턴스를 지나는 전류의 변화, 그리고 도는 회전자가 유도하는 전압에 나뉘어 쓰인다.

$$V=R\,i+L\,\frac{di}{dt}+k_e\,\omega_m$$

회전자는 회전에 대한 뉴턴 제2법칙으로 쓴다. 자기 토크가 회전자를 가속하고, 베어링을 돌리고, 남는 것이 기어박스로 들어간다.

$$J_m\,\dot\omega_m=k_t\,i-b\,\omega_m-\tau_{in}$$

$\omega_m$은 모터 속도, $i$는 권선 전류, $\tau_{in}$은 모터 축이 기어박스로 넘기는 토크이고, §2가 그것을 부하로 바꾼다. 두 식은 $i$와 $\omega_m$을 공유하므로 결합은 양방향이다. 전류가 토크를 만들고, 속도가 전압을 만든다.

> **권선의 정의.** **권선**(winding)은 모터의 전류를 나르는 구리 코일이고, 전기적으로는 *직렬 저항–인덕터 쌍*이다. 모터의 집중 파라미터 둘이지 부하나 제어기의 성질이 아니다. 정의 조건은 파라미터마다 하나씩, 둘이다. **저항** $R$은 전류를 $i^2R$의 비율로 열로 바꾸고, 멈춘 모터가 끌어가는 전류 $V/R$을 정한다. **인덕턴스** $L$은 에너지 $\tfrac12Li^2$을 저장하고 전류의 변화에 맞서므로, 전압이 뛰어도 전류는 뛰지 못한다. 그 걸리는 시간이 §5의 전기적 시정수다.
>
> $$V_R=R\,i,\qquad V_L=L\,\frac{di}{dt},\qquad P_{\text{heat}}=i^2R$$
>
> $V_R$과 $V_L$은 두 소자에 걸리는 전압 강하, $i$는 전류, $P_{\text{heat}}$는 소산되는 일률이다. 그러니 쌍 가운데 에너지를 쓰는 것은 $R$뿐이다. 인덕터는 저장한 것을 돌려주기 때문이다.
> - **예**: 고정한 구동계. $R=1.0\,\Omega$이므로 계산 절의 $2.4525\,\mathrm{A}$는 $6.01\,\mathrm{W}$의 열이 들고, $L=1.0\,\mathrm{mH}$이므로 전류를 $1\,\mathrm{ms}$에 $1\,\mathrm{A}$ 바꾸려면 $1\,\mathrm{V}$가 든다.
> - **비예**: "모터의 저항이 토크를 제한한다." $24\,\mathrm{V}$에서 멈춘 모터는 $V_s/R=24\,\mathrm{A}$를 끌어가겠지만, 증폭기는 $10\,\mathrm{A}$에서, 열 예산은 연속 $3.16\,\mathrm{A}$에서 멈춘다. 저항은 열을 정하고, 토크는 §3과 §6의 두 한계가 정한다.
> - **왜 중요한가**: $R$은 열의 항이고 $L$은 지연의 항이다. 이 페이지의 열 숫자는 모두 앞의 것에서 나오고, 전류 루프가 빠를 수는 있어도 즉각일 수 없는 이유는 뒤의 것에서 나온다.

> **토크 상수와 역기전력 상수의 정의.** **토크 상수** $k_t$와 **역기전력 상수** $k_e$는 *영구자석 모터의 비례 상수 둘*이고, 자석과 권선이 정한다. 증폭기나 기어박스나 부하가 정하는 것이 아니다. 정의 조건 셋. 토크는 **전류에 비례한다**, $\tau_m=k_ti$. 철심이 자기 포화하지 않는 동안에만 그렇다(아주 큰 전류에서는 $k_t$가 떨어진다). 권선에 생기는 전압은 **속도에 비례하고**, $e=k_e\omega_m$, 모터를 앞으로 미는 전류에 **맞선다**. *역*기전력이라는 이름이 그래서 붙었다. 그리고 SI 단위에서 둘은 **같은 숫자다**. 권선이 $e$에 맞서 넘겨주는 전기 일률이 정확히 회전자가 내는 기계 일률이기 때문이다. $e\,i=\tau_m\omega_m$이므로 $k_e\omega_m i=k_t i\omega_m$.
>
> $$\tau_m=k_t\,i,\qquad e=k_e\,\omega_m,\qquad e\,i=\tau_m\,\omega_m\ \Rightarrow\ k_t=k_e$$
>
> $\tau_m$은 $\mathrm{N{\cdot}m}$ 단위의 모터 토크, $i$는 A 단위의 전류, $\omega_m$은 rad/s 단위의 모터 속도, $e$는 V 단위의 유도 전압이다. 단위도 맞는다. $1\,\mathrm{N{\cdot}m/A}=1\,\mathrm{J/(A{\cdot}rad)}=1\,\mathrm{V{\cdot}s/rad}$.
> - **예**: 고정한 구동계, $k_t=k_e=0.10$. 계산 절의 $2.4525\,\mathrm{A}$는 $0.2453\,\mathrm{N{\cdot}m}$를 만든다. 들어올리기의 중간 속도, 관절에서 $1.17\,\mathrm{rad/s}$이니 모터에서 $117\,\mathrm{rad/s}$일 때 권선에는 $11.7\,\mathrm{V}$의 역기전력이 생긴다.
> - **비예**: $1000\,\mathrm{rpm}$당 $10.5\,\mathrm{V}$, 또는 그 역수 $95\,\mathrm{rpm/V}$를 적은 데이터시트. 이것은 바로 이 모터다. $0.10\,\mathrm{V{\cdot}s/rad}\times\tfrac{2\pi}{60}\times1000=10.47\,\mathrm{V/krpm}$이기 때문이다. $10.5$를 $\mathrm{N{\cdot}m/A}$ 단위의 $k_t$로 읽으면 $104.7$배 틀린다.
> - **비예**: "$k_t$가 두 배인 모터는 두 배 좋다." 같은 모터를 단면이 절반인 전선으로 두 배 감아 다시 만들면 $k_t$는 두 배, $R$은 네 배가 된다(길이 두 배, 단면 절반). 그래서 주어진 토크에 드는 열 $\tau_m^2R/k_t^2$은 그대로다. $k_t$는 전류와 전압을 맞바꿀 뿐이고, 와트당 토크는 자기 회로와 구리가 정한다.
> - **왜 중요한가**: 첫 식은 모든 구동계가 전압이 아니라 *전류*에 루프를 닫는 이유다 — 전류가 곧 토크다. 둘째 식은 속도가 전압을 먹는 이유이고, 이것이 §3의 속도 한계 전부이자 §7에서 단락된 모터가 브레이크가 되는 이유다.

$k_t=k_e$라는 등식은 모터의 일률 장부다. 전기 쪽에서 역기전력을 건너가는 와트 $e\,i$는 모두 기계 쪽에서 $\tau_m\omega_m$으로 다시 나타난다. 기어박스와, 숫자를 내는 시뮬레이션이 갖춰진 뒤 §8이 들어올리기의 한 순간에서 그 장부를 와트 단위로 맞춘다.

### 2. 기어박스: 감속비, 효율, 그리고 모터에서 본 부하

지렛대와 기어는 힘을 거리와 맞바꾸고, 반사 관성 $n^2J_m$은 회전자의 운동 에너지에서 나온다. [[02-foundations/basic-mechanics|0.6.1 기초 역학 §9]]가 둘을 손실 없는 이상 조건에서 P2의 기어박스 위에 계산한다. 이 절은 기어박스의 효율과 모터가 보는 부하를 더한다.

> **감속비의 정의.** 전동 장치의 **감속비**(gear ratio) $n$은 *속도의 비*, 곧 관절 한 바퀴당 모터 회전수이고, *기구학적인* 숫자다. 이의 기하가 정하며 부하, 속도, 일률이 흐르는 방향, 손실과는 무관하다. 정의 조건 둘. 모터와 관절의 속도는 매 순간 **비례로 묶여** 있다, $\omega_m=n\dot\theta$. 맞물린 이는 미끄러지지 않기 때문이다. 그리고 단순히 맞물리는 단들로 된 기어열이라면 그 비는 **잇수가 정한다**. 단마다 구동되는 기어의 잇수를 구동하는 기어의 잇수로 나누고, 단들에 걸쳐 곱한다.
>
> $$n=\frac{\omega_m}{\dot\theta}=\prod_{k}\frac{N_{\text{driven},k}}{N_{\text{driving},k}}$$
>
> $\omega_m$은 모터 속도, $\dot\theta$는 관절 속도, $N_{\text{driven},k}$와 $N_{\text{driving},k}$는 $k$번째 단의 잇수다. 그래서 로봇에서 흔한 감속은 $n>1$이다.
> - **예**: 고정한 구동계의 $n=100$은 12개 이의 피니언이 120개 이의 기어를 돌리는 단 두 개, $10\times10$일 수 있다. 모터의 무부하 속도 $240\,\mathrm{rad/s}$가 관절에서는 $2.4\,\mathrm{rad/s}$가 된다.
> - **비예**: "$100{:}1$ 기어박스는 토크를 $100$배 한다." 속도의 비는 정확하지만 토크의 비는 여기서 $\eta n=80$이다. 기어박스가 일률에서 제 몫을 떼어 가기 때문이고, 그것이 다음에 정의하는 효율이다.
> - **왜 중요한가**: $n$은 속도와 토크에는 1제곱으로, 모터 쪽이 관절에 보태는 모든 것에는 제곱으로 들어간다 — 반사 관성(§4), 유지 열(§6), 역구동성(§7). 그래서 $n$을 고르는 것이 구동계 설계의 핵심 결정이다(§8).

캡스턴 케이블 구동도 같은 종류의 비를 가지며, 잇수 대신 드럼 반지름이 정한다. 햅틱 트랙의 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]]이 그 경우를 다루고, 이 페이지에는 필요 없다. *Modern Robotics* §8.9.1은 로봇 관절이 흔히 $100$ 이상의 감속비를 쓴다고 적는다. 빠르게 돌지만 토크가 작은 모터를, 느리게 돌지만 토크가 큰 관절로 맞바꿔야 하기 때문이다. 실제 기어박스가 기구학에 더하는 것은 손실이다.

> **기어박스 효율의 정의.** 기어박스의 **효율** $\eta$는 *일률의 비*다. 출력 나누기 입력, $0$과 $1$ 사이의 수이고, *운전 조건에서의* 기어박스 성질이다. 부하·속도·온도에 따라 변하며, 기구학이 그렇게 만들기 전까지는 토크 비가 아니다. 정의 조건 셋. **일률의 비다**: $\eta=P_{\text{out}}/P_{\text{in}}$. 기구학적 비가 정확하므로, $\omega_m=n\dot\theta$, **토크의 비가 된다**: $\tau_{\text{out}}=\eta n\,\tau_{in}$. 그리고 **일률이 흐르는 한 방향**, 즉 모터가 부하를 구동하는 방향에 대해 선언한다. 부하가 모터를 구동하면 손실이 반대편에 앉는다. $\tau_{in}=\eta_b\,\tau_{\text{out}}/n$이고, 역방향 효율 $\eta_b$는 보통 더 낮으며 자체 잠김(self-locking) 기어박스에서는 0에 이른다.
>
> $$\eta=\frac{P_{\text{out}}}{P_{\text{in}}}=\frac{\tau_{\text{out}}\,\dot\theta}{\tau_{in}\,\omega_m}=\frac{\tau_{\text{out}}}{n\,\tau_{in}}\qquad(\text{모터 구동},\ \omega_m=n\dot\theta)$$
>
> $\tau_{in}$과 $\omega_m$은 기어박스 입력(모터 축)의 토크와 속도, $\tau_{\text{out}}$과 $\dot\theta$는 출력(관절)의 것이다. 마지막 꼴은 $\omega_m/\dot\theta=n$이 속도를 지워서 나온다.
> - **예**: 계산 절. 관절에 $19.62\,\mathrm{N{\cdot}m}$가 필요하므로 모터 쪽에는 손실 없는 $0.1962$ 대신 $19.62/(0.8\cdot100)=0.2453\,\mathrm{N{\cdot}m}$가 필요하다. 전류는 4분의 1 더, 열은 전류의 제곱으로 가므로 $1/\eta^2=1.5625$배다.
> - **비예**: 정지 상태에서 $\eta$를 읽는 것. 멈춘 기어박스는 일률을 전달하지 않으므로 그 비는 거기서 정의되지 않는다. 멈춘 팔을 붙잡는 것은 정지 마찰이고, 정지 마찰은 한 띠 안의 어떤 토크든 버틴다. 정지 상태에서 모터는 처지는 것을 겨우 막는 $\eta_b\,g_1/n$부터 들어 올릴 수 있는 $g_1/(\eta n)$까지 무엇으로든 팔을 붙잡을 수 있고, 구동계가 어디에 자리 잡는지는 어느 방향에서 도착했는지에 달려 있다. 고를 때는 뒤의 것을 쓴다. 팔이 떨어지는 것만 막을 수 있는 구동계는 팔을 되돌려 놓지 못하기 때문이다.
> - **왜 중요한가**: 이 페이지의 부하 쪽 토크·전류·열은 구동 방향에서 모두 $1/\eta$를 달고 다니고, 역구동성(§7)은 정방향 효율이 알려 주지 않는 $\eta_b$가 정한다.

이제 부하를 끝까지 옮겨 보자. 링크 쪽에서 기어박스는 관절이 요구하는 것, $\tau_{\text{load}}$를 내야 한다. 팔꿈치를 붙잡은 P2의 어깨라면 $\tau_{\text{load}}=M_{11}\ddot\theta_1+g_1(\theta_1)$다. 모터가 구동할 때 $\tau_{\text{load}}=\eta n\,\tau_{in}$이므로 $\tau_{in}=\tau_{\text{load}}/(n\eta)$이고, 이것을 §1의 회전자 식에 넣으면 구동계의 기계 방정식이 나온다.

$$J_m\,\dot\omega_m=k_t\,i-\frac{\tau_{\text{load}}}{n\eta}-b\,\omega_m$$

기어박스 입력에 닿는 토크는 자기 토크가 회전자를 가속하고 베어링을 돌리고 남은 것이기 때문이다. $\omega_m=n\dot\theta_1$을 넣고 양변에 $n$을 곱해 관절에서 읽으면

$$\Big(n^2J_m+\frac{M_{11}}{\eta}\Big)\ddot\theta_1=n\,k_t\,i-n^2b\,\dot\theta_1-\frac{g_1(\theta_1)}{\eta}$$

이다. 그러니 모터가 밀어야 하는 관절의 관성은 $J_{eq}=n^2J_m+M_{11}/\eta$이고, $n=100$ 구동계에서는 $1.0+3.75=4.75\,\mathrm{kg{\cdot}m^2}$다. 회전자는 §4의 에너지 값으로 들어오고, 링크와 그 중력은 $\eta$로 나뉘어 들어온다. 기어박스를 지나는 것만 통행료를 내기 때문이다. 우변은 *이상 기어* 단위로 쓰였다 — $nk_ti$는 손실 없는 기어박스가 전달할 토크다 — 그리고 랩의 제어기도 같은 단위로 토크를 요구한다. $\dot\theta_1=\ddot\theta_1=0$으로 두면 $i=g_1/(\eta nk_t)$, 계산 절의 2·3단계가 한 줄로 나오고, 랩의 `acc = ...` 줄은 이 식을 $\ddot\theta_1$에 대해 푼 것이다.

적용 영역 조건 하나를 한 번만 적어 둔다. 이것은 모터가 부하를 *구동하는* 식이다. §8의 들어올리기에서 링크 토크 $M_{11}\ddot\theta_1+g_1$은 팔이 올라가는 동안 양수로 남는다 — 모든 행을 통틀어 가장 작은 값이 $n=30$의 $0.86\,\mathrm{N{\cdot}m}$다 — 그래서 올라가는 내내 일률은 모터에서 링크로 흐르고, 이것이 식이 기술하는 방향이다. 거꾸로 흐르는 것은 각 행이 동작 끝에서 조금 넘어섰다가 되돌아오는 구간뿐이고, 거기서는 식이 손실을 엉뚱한 쪽에 둔다. 그것이 무엇을 바꾸는지는 §8이 말한다.

### 3. 토크–속도 선, 그리고 감속비가 그것에 하는 일

구동계가 할 수 있는 모든 것을 두 한계가 묶고, 둘 다 전기적이다.

> **공급 전압과 전류 한계의 정의.** **공급 전압** $V_s$와 **전류 한계** $I_{\max}$는 *증폭기가 권선에 가할 수 있는 것의 두 경계*다. 구동계의 한계이지 모터 혼자의 성질이 아니다. 정의 조건은 경계마다 하나씩, 둘이다. 단자 전압에는 경계가 있다, $|V|\le V_s$. 증폭기는 받은 공급을 권선에 스위칭해 걸 수 있을 뿐이기 때문이다. 전류에도 경계가 있다, $|i|\le I_{\max}$. 증폭기를, 그리고 그보다 훨씬 위에서는 모터의 자석과 철심을 보호해야 하기 때문이다. 증폭기는 전류가 한계에 닿을 때마다 전압을 낮춰 이것을 지킨다.
>
> $$|V|\le V_s,\qquad |i|\le I_{\max}\quad\Longrightarrow\quad |\tau_m|\le k_tI_{\max},\qquad \omega_m\le\frac{V_s-R\,i}{k_e}$$
>
> 화살표 뒤는 §1에서 나온다. 전류가 토크이므로 전류 한계는 토크 한계다. 그리고 정상 상태에서 $V=Ri+k_e\omega_m$이므로 전압 한계는 속도 한계이고, 전류가, 따라서 $Ri$ 강하가 커질수록 조여진다.
> - **예**: 고정한 구동계. 모터에서 $k_tI_{\max}=1.0\,\mathrm{N{\cdot}m}$이고, 부하 없는 모터가 $24\,\mathrm{V}$로 낼 수 있는 가장 빠른 속도는 $240\,\mathrm{rad/s}$다.
> - **비예**: "24 V 모터." 모터에는 자기 공급 전압이 없다. 명판의 숫자는 권선을 설계할 때 기준으로 삼은 전압이다. 같은 모터를 $48\,\mathrm{V}$로 돌리면 토크 상수도, 뉴턴미터당 열도 그대로인 채 무부하 속도가 두 배가 되고, 과제가 바로 그것을 한다.
> - **왜 중요한가**: $I_{\max}$는 토크를, $V_s$는 속도를 막는다. 감속비는 하나를 다른 하나와 맞바꿀 수는 있어도 둘을 함께 올리지는 못한다. 랩의 스윕이 양 끝에서 실패하는 이유다.

그 한계 안에서, 한 전압에서 모터의 정상 운전점은 선 하나 위에 놓인다.

> **토크–속도 선의 정의.** DC 모터의 토크–속도 선(**torque–speed line**)은 *토크–속도 평면의 경계*다. 한 단자 전압에서 도달할 수 있는 정상 운전점들이다. 모터와 전압에 속하지 부하나 제어기에 속하지 않고, 이름 붙은 끝이 둘 있다. 정의 조건 셋. **정상 상태**: 전류가 변하지 않아 인덕턴스가 빠진다. **고정된 단자 전압**: 보통은 한계에 닿은 공급 $V_s$다. 그리고 **선형 자기 회로, 마찰 무시**: 그래서 $k_t$와 $k_e$가 상수다.
>
> $$\tau_m=\frac{k_t}{R}\big(V-k_e\,\omega_m\big)=\tau_{\text{stall}}\Big(1-\frac{\omega_m}{\omega_0}\Big),\qquad \omega_0=\frac{V}{k_e},\qquad \tau_{\text{stall}}=\frac{k_tV}{R}$$
>
> 이것은 §1의 권선 방정식에서 $di/dt=0$으로 두고 $i=(V-k_e\omega_m)/R$로 푼 뒤 $k_t$를 곱한 것이다. 그래서 선이 내려가는 것은 속도 1 rad/s마다 공급 가운데 $k_e$볼트를 역기전력에 쓰기 때문이다. 양 끝은 **무부하 속도** $\omega_0$ — 역기전력이 공급을 다 써서 전류가, 따라서 토크가 남지 않는 곳 — 와 **정지 토크** $\tau_{\text{stall}}$ — 속도 0에서 $R$ 말고는 전류를 막는 것이 없는 곳 — 이다.
> - **예**: $V_s=24\,\mathrm{V}$의 고정 구동계. $\omega_0=240\,\mathrm{rad/s}$($2292\,\mathrm{rpm}$), $\tau_{\text{stall}}=2.4\,\mathrm{N{\cdot}m}$이고 그때 전류는 $24\,\mathrm{A}$다. 전류 한계가 이 선을 $1.0\,\mathrm{N{\cdot}m}$에서 자르고, 둘이 만나는 모서리는 $\omega_m=(V_s-RI_{\max})/k_e=140\,\mathrm{rad/s}$다.
> - **비예**: "정지 토크가 모터의 토크 정격이다." 정지는 모든 와트가 열인 점이다 — $1\,\Omega$를 지나는 $24\,\mathrm{A}$는 $576\,\mathrm{W}$이고, 연속 예산이 $10\,\mathrm{W}$인 권선에서다 — 그리고 이 증폭기는 거기에 닿지도 못한다. *무기한*을 뜻하는 정격은 §6의 연속 토크다.
> - **왜 중요한가**: 감속비가 이 선을 옮긴다. 토크는 $\eta n$배 위로, 속도는 $n$분의 1로. 그래서 고르는 일의 맞바꿈 전체가 그림 하나, 맨 위의 그림에 들어간다.

관절에서는 $\tau_j=\eta n\tau_m$, $\dot\theta=\omega_m/n$이므로 같은 선이

$$\tau_j=\frac{\eta nk_t}{R}\big(V_s-k_en\,\dot\theta\big)$$

로 읽힌다. 기어박스가 모터의 토크를 $\eta n$배 하고 속도를 $n$으로 나누기 때문이다. $n$과 함께 세 가지가 움직이는데, 같은 속도로 움직이지 않는다. 전류 한계 $\eta nk_tI_{\max}$는 $n$에 비례해 오르고, 무부하 속도 $V_s/(k_en)$는 $1/n$로 떨어지고, 전압선의 기울기 $\eta n^2k_tk_e/R$는 $n^2$로 가팔라진다. $n=100$ 구동계에서 그 값은 $80\,\mathrm{N{\cdot}m}$, $2.4\,\mathrm{rad/s}$, rad/s당 $80\,\mathrm{N{\cdot}m}$이고, 맨 위 그림의 선 $\tau_j=192-80\,\dot\theta$다. 감속비를 두 배로 하면 영역은 높이가 두 배, 폭이 절반이 된다. $n=200$에서 $160\,\mathrm{N{\cdot}m}$, $1.2\,\mathrm{rad/s}$.

이제 그 위에 들어올리기를 놓아 보자. 동작 중간에 들어올리기는 약 $21.4\,\mathrm{N{\cdot}m}$의 중력을 거슬러 $1.17\,\mathrm{rad/s}$를 요구한다. $n=100$에서 전압선은 거기서 $192-80\cdot1.17=98\,\mathrm{N{\cdot}m}$를 주고, 전류가 그것을 $80$에서 막는다. 넉넉하다. $n=200$에서는 같은 속도가 역기전력에만 $0.1\cdot200\cdot1.17=23.4\,\mathrm{V}$를 쓰고, 선이 주는 것은 들어올리기에 필요한 $21.8$에 대해 $9.0\,\mathrm{N{\cdot}m}$뿐이다. 그러니 §8 스윕의 그 행은 공급에 닿을 수밖에 없다.

### 4. 회전 관절의 반사 관성, 그리고 그것이 지배할 수 있는 이유

> **반사 관성의 정의.** 전동 장치 뒤에 있는 모터의 **반사 관성**(reflected inertia)은 *그 회전자가 출력에 기여하는 관성*이다. 회전자와 비만의 성질이고, 부하나 제어기, 구동계에 전원이 들어와 있는지와는 무관하다. 정의 조건 셋. **운동 에너지가 같다.** 출력의 속도로 돌면서 회전자가 제 속도로 도는 만큼의 에너지를 저장하는 관성이다. **비의 제곱으로 자란다.** 회전자는 출력의 $n$배로 돌고 운동 에너지는 속도의 제곱으로 가기 때문이다. 그리고 **전원이 꺼져도 있다.** 제어의 효과가 아니라 움직이는 질량이기 때문이다. 회전 관절에서는 유도가 한 줄이다. 어깨의 고정자는 받침에 볼트로 고정되어 있고 회전자는 $\omega_m=n\dot\theta_1$로 도므로
>
> $$\tfrac12J_m\,\omega_m^2=\tfrac12J_m\,(n\dot\theta_1)^2=\tfrac12\,\big(n^2J_m\big)\,\dot\theta_1^2\quad\Longrightarrow\quad J_{\text{refl}}=n^2J_m$$
>
> 이고, 이것은 관절 자신의 속도로 도는 관성 $n^2J_m$의 운동 에너지다. $J_m$은 회전자 관성, $\dot\theta_1$은 관절 속도다.
> - **예**: $n=100$인 고정 구동계. 어깨에서 $10^4\cdot10^{-4}=1.0\,\mathrm{kg{\cdot}m^2}$로, 팔 자신의 $M_{11}=3$의 3분의 1이다 — 계산 절의 6단계.
> - **비예**: §5의 $J=J_m+M_{11}/(\eta n^2)$. 이것은 반대 방향의 반사, 곧 *모터* 축에서 본 *링크*이고, $n^2$로 나뉘며 기어박스를 지나므로 $\eta$의 세금이 붙는다. 모터의 시정수에는 맞는 관성이지만 팔의 질량 행렬에는 틀린 관성이다.
> - **왜 중요한가**: 구동계 파라미터 가운데 팔의 한계만이 아니라 동역학 자체를 바꾸는 유일한 것이다. 질량 행렬, 말단의 겉보기 질량, 아래의 충돌 힘에 들어가고, 이 절이 계산하는 비를 넘으면 팔 자체보다 무거워진다.

회전자가 $M_{11}$에 더하는 것이 정확히 이것이고, 효율은 들어 있지 않다. 질량 행렬은 운동 에너지이고 마찰은 아무것도 저장하지 않기 때문이다. *Modern Robotics* §8.9.2는 이것을 겉보기 관성(apparent inertia)이라 부르고 같은 방식으로 유도한다. 캡스턴 판은 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §3]]에서 골라 더 읽을 수 있다.

팔꿈치 구동계는 더 미묘한데, 고정자가 링크 1에 올라타 있기 때문이다. 회전자의 절대 속도는 $\dot\theta_1+n\dot\theta_2$이고, 이것을 제곱하면 회전자의 에너지가 셋으로 갈라진다.

$$\tfrac12J_m(\dot\theta_1+n\dot\theta_2)^2=\tfrac12J_m\dot\theta_1^2+nJ_m\,\dot\theta_1\dot\theta_2+\tfrac12n^2J_m\dot\theta_2^2$$

그래서 [[04-robotics/modern-robotics/ch08-dynamics|MR 8장 §2]]처럼 이차형식에서 계수를 읽으면, $M_{11}$에 $J_m$, $M_{12}$에 $nJ_m$, $M_{22}$에 $n^2J_m$을 더한다. $4.0001$과 $1.01$이 있는 계산 절의 행렬이다.

**왜 지배할 수 있는가.** 회전자는 작고 $n^2$은 크며, 둘의 겨루기는 비 하나로 정해진다.

$$\frac{n^2J_m}{M_{ii}}=1\quad\Longleftrightarrow\quad n=\sqrt{M_{ii}/J_m}$$

관절 $i$에서 회전자의 반사 관성이 팔 자신의 관성과 같아지는 곳이 거기이기 때문이다. 고정한 구동계에서 어깨는 $n=\sqrt{3/10^{-4}}=173$에서, 팔꿈치는 $n=\sqrt{1/10^{-4}}=100$에서 동등해진다. 그러니 $n=100$ 팔의 팔꿈치는 정확히 동등점에 있고, $n=300$에서 어깨 회전자는 팔의 세 배인 $9\,\mathrm{kg{\cdot}m^2}$다. 세 가지 결과가 따른다.

- **질량 행렬이 더 대각이 된다.** 결합을 $M_{12}/\sqrt{M_{11}M_{22}}$로 재면, 맨 팔의 $0.577$에서 $n=100$의 $0.357$, $n=300$의 $0.094$로 떨어진다. *Modern Robotics* §8.9.2도 같은 관찰을 한다. 감속비가 크면 각 관절은 주로 자기 회전자를 느낀다. [[02-foundations/manipulator-kinematics-dynamics|10. §3]]이 다섯 배로 잰 자세 의존성도 함께 줄어든다. $M_{11}$은 맨 팔에서 접힌 $1$부터 편 $5$까지, $n=100$에서 $2$부터 $6$까지, $n=300$에서 $10$부터 $14$까지 움직여 비가 $1.4$다. 감속비가 큰 팔에서는 고정 이득 관절 제어기가 거의 일정한 관성을 만나고, 대가는 다른 데서 치른다.
- **말단이 무거워지고, 충돌이 세진다.** 말단을 똑바로 위로 미는 힘이 만나는 질량은 $JM^{-1}J^\top$의 $yy$ 원소의 역수이고, [[02-foundations/manipulator-kinematics-dynamics|10. §6]]의 "미는 힘이 느끼는 질량의 역수"라는 읽기다. 맨 팔에서 $2.0\,\mathrm{kg}$, $n=100$ 구동계로 $3.49\,\mathrm{kg}$, $n=300$에서 $11.9\,\mathrm{kg}$. 최대 충돌력은 그 질량의 제곱근으로 가므로, [[04-robotics/force-compliance-control|13. §5]]의 $5\,\mathrm{cm/s}$ 착지는 $22.4\,\mathrm{N}$에서 $n=100$의 $29.5\,\mathrm{N}$, $n=300$의 $54.5\,\mathrm{N}$로 오른다. 몇 밀리초 만에 끝나는 충돌에서는 제어기가 이 관성을 가릴 시간이 없고, 관성은 전원이 꺼져도 있다.
- **관성 정합: 감속비를 더 올려도 가속이 늘지 않는 곳.** 중력을 빼면, 관절 가속도 한 단위에 필요한 모터 토크는 §2의 관절 방정식을 $n$으로 나눈 데서 나온다.

  $$\tau_m=\Big(nJ_m+\frac{M_{11}}{\eta n}\Big)\ddot\theta_1\quad\Longrightarrow\quad n^\ast=\sqrt{\frac{M_{11}}{\eta J_m}}$$

  $n$에 대한 도함수를 0으로 두면 $J_m=M_{11}/(\eta n^2)$이 남기 때문이다. $n^\ast=193.6$에서 회전자의 $n^{\ast2}J_m=3.75$가 링크의 $M_{11}/\eta$와 같다. 그 아래에서는 링크가 지배하므로 감속비를 올리면 도움이 되고, 그 위에서는 모터가 늘어난 몫을 자기 회전자에 쓴다. 최솟값 $2\sqrt{J_mM_{11}/\eta}=0.0387\,\mathrm{N{\cdot}m}$(rad/s²당)은 얕다 — $n=100$에서 $0.0475$, $n=300$에서 $0.0425$ — 그래서 감속비는 보통 관성 정합이 아니라 중력(§6)과 속도(§3)가 정한다.

### 5. 두 시정수, 그리고 전류 루프가 먼저인 이유

모터에는 §1의 방정식마다 하나씩, 자기만의 속도가 둘 있고, 둘이 얼마나 떨어져 있는지가 제어기를 어떻게 짤지를 정한다. 전기적 속도 $L/R$은 PWM 구동이 권선 전류에 작은 리플만 남기는 이유이기도 하고, [[02-foundations/basic-circuits-electronics|0.6.2 §12]]의 실습이 그것을 스윕한다.

> **전기적·기계적 시정수의 정의.** **시정수**(time constant)는 1차 응답이 계단의 $1-e^{-1}=63\%$를 가는 데 걸리는 *시간*이다. 실수 극점 하나의 역수다. 모터에는 §1의 방정식마다 하나씩 둘이 있고, 각각은 다른 하위계를 비켜 둔 채 정의한다. **전기적 시정수** $\tau_e=L/R$은 회전자를 붙잡은 채 전압 계단을 줬을 때 전류가 자리 잡는 빠르기다. **기계적 시정수** $\tau_{\text{mech}}=JR/(k_tk_e)$는 $L$을 무시하고 전압 계단을 줬을 때 속도가 자리 잡는 빠르기다. 여기서 역기전력은 댐퍼 $k_tk_e/R$로 작용하고, $J$는 모터가 가속하는 *모든 것*을 모터 축으로 환산한 것이다.
>
> $$\tau_e=\frac{L}{R},\qquad \tau_{\text{mech}}=\frac{J\,R}{k_t\,k_e},\qquad J=J_m+\frac{M_{11}}{\eta\,n^2}$$
>
> 기계적 시정수는 $i=(V-k_e\omega_m)/R$을 $J\dot\omega_m=k_ti$에 넣은 데서 나온다. 그러면 $J\dot\omega_m=k_tV/R-(k_tk_e/R)\,\omega_m$, 극점이 $k_tk_e/(JR)$인 1차 지연이 된다.
> - **예**: 고정한 구동계. $\tau_e=1.0\,\mathrm{ms}$. 회전자만이면 $\tau_{\text{mech}}=10\,\mathrm{ms}$이고, $n=100$ 기어박스에 P2의 어깨를 달면 $J=10^{-4}+3/(0.8\cdot10^4)=4.75\times10^{-4}\,\mathrm{kg{\cdot}m^2}$, $\tau_{\text{mech}}=47.5\,\mathrm{ms}$다.
> - **비예**: "전류 루프의 대역폭은 $R/L$이다." $R/L=1000\,\mathrm{rad/s}$는 *제어하지 않은* 권선의 극점이 있는 곳이다. PI 전류 루프는 그 극점을 상쇄하고 이득이 정하는 곳에서 닫힌다 — 여기서는 $2000\,\mathrm{rad/s}$ — 그리고 그 한계는 스위칭·샘플링 주파수와 남은 전압이 정하지 $L/R$이 정하지 않는다.
> - **왜 중요한가**: $\tau_{\text{mech}}$는 감속비나 부하가 무엇이든 회전자만의 $J_mR/(k_tk_e)=10\,\mathrm{ms}$ 아래로 떨어질 수 없다. 그래서 전류는 속도가 바뀔 수 있는 것보다 적어도 열 배 빨리 자리 잡는다. 그 분리가 아래 캐스케이드의 면허다.

**캐스케이드**(cascade)는 빠른 루프를 느린 루프 안에 닫는다. 안쪽 루프는 전류를, 따라서 토크를 조절하고, 바깥 루프는 안쪽 루프에 전류를 요청해 위치를 조절한다. 여기서 안쪽 루프는 영점이 권선의 극점을 상쇄하는 PI 제어기다.

$$C_i(s)=K_{pi}+\frac{K_{ii}}{s},\qquad \frac{K_{ii}}{K_{pi}}=\frac{R}{L}\ \Longrightarrow\ \frac{i}{i_{\text{ref}}}=\frac{\omega_{ci}}{s+\omega_{ci}},\qquad \omega_{ci}=\frac{K_{pi}}{L}$$

영점이 극점 위에 앉으면 루프 이득 $C_i(s)\cdot1/(Ls+R)$이 $K_{pi}/(Ls)$로 줄어들기 때문이고, 역기전력은 적분기가 없애는 느린 외란이다. $\omega_{ci}=2000\,\mathrm{rad/s}$($318\,\mathrm{Hz}$)로 두면 $K_{pi}=L\omega_{ci}=2\,\mathrm{V/A}$, $K_{ii}=R\omega_{ci}=2000\,\mathrm{V/(A{\cdot}s)}$이고, [[04-robotics/control-theory-ce397|5. 제어 이론 §7]]의 조건부 적분 anti-windup을 달고 $20\,\mathrm{kHz}$로 돈다. 바깥 PD는 $1\,\mathrm{kHz}$로 돌고 $20\,\mathrm{rad/s}$, 즉 백 배 느리게 맞춘다. 그래서 바깥 루프는 안쪽 루프를 토크원으로 본다. 상자가 준 면허를 여유 있게 쓰는 셈이다.

면허가 끝나는 곳은 전압이다. 전류 루프는 $L\,di/dt$에 전압을 써야만 전류를 움직일 수 있고, 쓸 수 있는 것은 $V_s-Ri-k_en\dot\theta$다. $n=200$ 구동계에서 들어올리기의 중간 속도라면 역기전력만으로 $24\,\mathrm{V}$ 중 $23.4\,\mathrm{V}$를 쓰므로, 전류 루프는 관절이 가장 빠를 때 정확히 권한을 잃는다. §8의 $V_s$ 표시 뒤에 있는 메커니즘이 이것이다. 속도 포화는 전류 루프가 전압을 다 쓴 것이다.

### 6. 연속 대 최대: 열이 정한다

부하를 붙잡는 일은 기계적 일을 하지 않으므로([[02-foundations/basic-mechanics|0.6.1 §6]]의 에너지 장부), 가만히 붙잡고 있는 구동계는 전기 일률을 전부 열로 바꾼다. 그리고 권선이 견디지 못하는 것은 전류가 아니라 열이다. 권선은 $i^2R$로 데워지고 열저항을 거쳐 주변으로 열을 잃는다. 가장 단순한 단일 노드 모델에서 온도 상승 $\Delta T$는

$$C_{th}\,\frac{d\,\Delta T}{dt}=i^2R-\frac{\Delta T}{R_{th}}\quad\Longrightarrow\quad \Delta T(t)=R_{th}\,i^2R\,\big(1-e^{-t/\tau_{th}}\big),\qquad \tau_{th}=R_{th}C_{th}$$

를 따른다. 권선의 열용량 $C_{th}$에 쌓이는 열은 만들어진 열에서 빠져나간 열을 뺀 것이고, 해는 주변 온도에서 출발하기 때문이다. 정상 상태는 $\Delta T=R_{th}\,i^2R$이고, 이것이 허용 상승 아래에 머물라고 요구하면 연속 정격이 나온다.

> **연속 토크와 최대 토크의 정의.** **연속 토크**(continuous torque)와 **최대 토크**(peak torque)는 *구동계의 토크 정격 둘이고, 각각 다른 물리가 정한다*. 연속은 **열** 정격이다. 그 $i^2R$ 열이 열저항을 거쳐 권선을 정상 상태에서 정확히 허용 상승에 붙잡아 두는 토크이고, 모터·냉각·주변 온도가 함께 가진 성질이다. 최대는 **전류** 정격이다. 전류 한계에서의 토크이고, 열 시정수가 정하는 시간 동안만 쓸 수 있다. 정의 조건은 정격마다 하나씩 둘이고, 둘을 잇는 셋째가 있다. 연속 정격을 넘는 토크는 **지속 시간과 함께** 말해야 한다.
>
> $$\tau_{\text{cont}}=k_t\sqrt{\frac{\Delta T_{\max}}{R_{th}R}},\qquad \tau_{\text{peak}}=k_tI_{\max}$$
>
> $$t_{\text{allowed}}=-\tau_{th}\ln\!\Big(1-\frac{\Delta T_{\max}}{R_{th}\,i^2R}\Big)$$
>
> 첫 식은 $R_{th}i^2R=\Delta T_{\max}$로 두고 $k_ti$에 대해 푼 것이고, 마지막 식은 주변 온도에서 출발한 위 곡선에서 $\Delta T(t)=\Delta T_{\max}$를 푼 것이다. $R_{th}i^2R>\Delta T_{\max}$일 때만 정의된다. 그렇지 않으면 한계에 영영 닿지 않기 때문이다.
> - **예**: 고정한 구동계. $I_{\text{cont}}=\sqrt{100/(10\cdot1)}=3.162\,\mathrm{A}$이므로 $\tau_{\text{cont}}=0.316\,\mathrm{N{\cdot}m}$, $\tau_{\text{peak}}=1.0\,\mathrm{N{\cdot}m}$이고, $n=100$ 관절에서는 $25.3$과 $80\,\mathrm{N{\cdot}m}$다. 최대 $10\,\mathrm{A}$에서 권선은 $100\,\mathrm{W}$를 만들고 $t=-60\ln(1-100/1000)=6.3\,\mathrm{s}$ 뒤에 한계에 닿는다.
> - **비예**: 같은 유지를 $n=50$에서. $4.905\,\mathrm{A}$가 필요한데 연속보다 크고 최대보다 한참 작으므로, 팔은 *정말로* 떠 있다 — $-60\ln(1-100/240.6)=32.2\,\mathrm{s}$ 동안. 그 뒤 권선은 한계에 있고 여전히 오른다. "시연에서 팔을 붙잡았다"는 처음 30초에 대한 진술이다.
> - **왜 중요한가**: 정지 자세의 비용은 $i^2R$이고 $i$는 $1/n$로 떨어지므로 유지 열은 $1/n^2$로 떨어진다 — 감속비는 관절이 가진 가장 싼 냉각이다. P2를 연속으로 붙잡으려면 $n\ge g_1/(\eta k_tI_{\text{cont}})=77.6$이 필요하다.

**동작은 RMS로 판정한다.** 맨 위의 그림에서 들어올리기의 고리는 길이의 상당 부분을 열 한계선 위에서 보내는데, 그래도 된다. 열은 $i^2$을 적분하므로, $\tau_{th}$에 비해 짧은 듀티 사이클에서 열 한계선이 묶는 것은 제곱평균제곱근 전류, $I_{\text{rms}}=\sqrt{\tfrac1T\int_0^Ti^2\,dt}\le I_{\text{cont}}$다. 들어올리기의 요구를 쉬지 않고 되풀이하면 $I_{\text{rms}}=3.11\,\mathrm{A}$로 연속의 $98\%$이고, 들어올릴 때마다 $4.2\,\mathrm{s}$씩 유지를 붙이면 5초 사이클은 $2.57\,\mathrm{A}$로 떨어진다.

**저항은 열과 함께 움직인다.** 구리의 저항은 켈빈당 약 $0.39\%$ 오르므로, 뜨거운 권선은 같은 전류에서 열을 더 만든다. 이것을 계산 절에 넣으면 유지의 상승은 $\Delta T=R_{th}i^2R_0(1+\alpha\Delta T)$를 풀어 $\Delta T=60.1/(1-0.0039\cdot60.1)=78.6\,\mathrm{K}$가 된다. 여전히 예산 안이지만, 상승이 $R$을 고정한 추정보다 $31\%$ 크다. 이 페이지의 나머지는 $R$을 고정한다.

### 7. 기어 달린 관절의 역구동성

> **역구동성의 정의.** **역구동성**(backdrivability)은 *출력을 미는 힘이 전동 장치와 그 뒤의 모터를 얼마나 쉽게 움직이는가*이고, 제어기가 아니라 메커니즘의 성질이다. 정의 조건 셋. **출력에서 잰다.** 링크 자신의 관성과 중력이 가져가는 몫 위에, 관절을 움직이려고 미는 쪽이 더 내야 하는 토크(직선 축이라면 힘)다. **운동과 함께 말한다.** 그 항들이 속도와 가속도 둘 다에 비례해 커지므로, 잰 속도와 가속도를 밝힌다. 그리고 **수동적이다.** 구동계에는 전원이 없고 권선의 상태(개방인가 단락인가)를 밝힌다. 제어기는 느린 마찰은 감출 수 있어도 충돌의 몇 밀리초 안에서는 그러지 못하기 때문이다. 기어 달린 관절에서 모터 쪽의 임피던스 — 회전자의 관성, 베어링의 점성 마찰, 그리고 권선이 단락되어 있다면 §1의 역기전력이 만드는 전기적 댐핑 — 는 모두 모터의 운동에 비례하는 토크이고, 운동과 토크가 지나가면서 각각 $n$배가 되므로 $n^2$배가 되어 도착한다.
>
> $$\tau_{\text{bd}}=n^2J_m\,\ddot\theta+n^2b\,\dot\theta+\tau_{\text{gear}}\qquad\Big(+\;n^2\frac{k_tk_e}{R}\,\dot\theta\ \ \text{권선 단락 시}\Big)$$
>
> $\dot\theta$와 $\ddot\theta$는 미는 동안의 관절 속도와 가속도, $\tau_{\text{gear}}$는 기어박스 자신의 마찰이고, 기어박스는 이상적이라고 둔다(손실은 아래 문단이 더한다).
> - **예**: $n=100$ 구동계의 P2 어깨, 권선 개방, $0.5\,\mathrm{rad/s}$를 지나며 $1\,\mathrm{rad/s^2}$로 민다. 기어박스 마찰 전에 $\tau_{\text{bd}}=1.0+0.05=1.05\,\mathrm{N{\cdot}m}$다(아래 첫 항목).
> - **비예**: "관절이 토크 제어되므로 역구동 가능하다." 그것은 능동 컴플라이언스이고 정의가 제외하는 것이다. 전원과 루프가 필요하고, 충돌 안에서는 작동하지 못하며, 거기서 환경이 만나는 것은 수동적인 $n^2J_m$이다.
> - **왜 중요한가**: 사람이 손으로 팔을 움직일 수 있는지, 충돌이 얼마나 단단한지, 전류를 토크로 읽을 수 있는지(항목들 뒤의 문단)를 이것이 정한다.

그 식에서 $\tau_{\text{bd}}$는 이상적인 기어박스에서 관절을 미는 쪽이 링크 자신의 관성과 중력 위에 더 내야 하는 토크이고, $\tau_{\text{gear}}$는 기어박스 자신의 마찰이다. 이 마찰은 §2의 $\eta$ 하나로 가벼운 부하에서 기술되지 않고, 감속비와 함께 커지는 경향이 있다(*Modern Robotics* §8.9.4). 손실이 있는 기어박스는 모터 쪽 항들을 역방향 효율 $\eta_b$로 나누기도 하고, $\eta_b$가 0에 이르는 기어박스는 아예 역구동되지 않는다. 자체 잠김 웜 기어가 그 극단이다.

- **권선 개방, 사람이 민다.** P2의 어깨를 $0.5\,\mathrm{rad/s}$를 지나며 $1\,\mathrm{rad/s^2}$로 가속하려면, $n=100$ 구동계에 대해 기어박스 마찰 전에 $1.0+0.05=1.05\,\mathrm{N{\cdot}m}$가 든다. 팔 자신의 $M_{11}\ddot\theta=3\,\mathrm{N{\cdot}m}$ 위에서이니 3분의 1 더다. $n=300$에서는 구동계의 몫이 $9.45\,\mathrm{N{\cdot}m}$로 팔의 세 배다.
- **권선 단락, 팔을 놓는다.** 어떤 구동계는 꺼질 때 권선을 단락한다(동적 제동). 그러면 역기전력이 제동 전류를 흘리고, 관절에서의 댐핑은 $n=100$에서 $n^2k_tk_e/R=100\,\mathrm{N{\cdot}m{\cdot}s/rad}$다. 자세에서 놓인 P2는 그 댐핑이 중력과 맞먹는 속도, $19.62/100=0.196\,\mathrm{rad/s}$ 곧 약 $11^\circ/\mathrm{s}$로 내려앉고(이상적인 기어박스, 짧은 과도 이후), $n=300$에서는 $0.0218\,\mathrm{rad/s}$다. 단락된 모터는 관절이 움직이는 동안에만 듣는 브레이크다. 팔을 늦출 뿐 세우지는 못한다.

**전류를 토크로 읽는다는 것의 의미.** 전류로 관절 토크를 추정하는 구동계, $\hat\tau=\eta nk_ti$는 회전자와 마찰 항을 없는 셈 치고 있다. 들어올리기의 최대 가속도 $4.51\,\mathrm{rad/s^2}$에서 링크에 필요한 것은 $35.5\,\mathrm{N{\cdot}m}$인데, 전류 기반 추정은 $n=100$에서 $39.1$로 $10\%$ 높고, $n=300$에서 $68.3$으로 $93\%$ 높다. 회전자의 $n^2J_m\ddot\theta$는 전류에는 들어 있고 링크에는 없기 때문이다. 감속비가 낮은 구동계는 이 오차를 작게 두고 유지 열로 값을 치른다. §6의 맞바꿈을 센싱 쪽에서 본 것이다. Wensing 외(2017)는 다리 로봇의 액추에이터를 이 선택 위에 짓는다. 힘 제어를 관절에 동위치(collocated)로 두고, 충돌 시의 역구동성을 아래에 정의하는 impact mitigation factor로 잰다. [[04-robotics/force-compliance-control|13. §2]]의 토크 기반 임피던스 제어를 돕는 것이 바로 이런 구동계 — 역구동 가능한 관절 위의 반응 빠른 토크 인터페이스 — 이고, 그 페이지의 어드미턴스 쪽 가지는 위치나 속도 명령만 내주는 로봇을 위해 쓰인 것이다.

> **Impact mitigation factor의 정의.** Wensing 외(2017)의 **impact mitigation factor**(IMF)는 다리 로봇 같은 부유 베이스(floating-base) 로봇의 *충돌 시 역구동성을 재는 무차원 점수*다. 한 접촉점, 한 자세에서 그 질량과 반사된 회전자 관성이 정하는 성질이지 제어기의 성질이 아니다. 관성 둘이 이것을 정의한다. $\Lambda$는 관절이 자유롭게 움직일 때(반사된 회전자 관성 포함) 접촉점에서 느끼는 관성이고, $\Lambda_L$은 모든 관절을 잠가 로봇이 하나의 강체로 착지할 때의 같은 관성이다. 같은 충돌 속도에서 자유로운 로봇은 잠긴 로봇이 받는 충격량의 $\Lambda\Lambda_L^{-1}$배를 받으므로, $I-\Lambda\Lambda_L^{-1}$이 자유로운 관절이 덜어 내는 부분이고, 그 행렬식이 이 지표다.
>
> $$\xi=\det\!\big(I-\Lambda\,\Lambda_L^{-1}\big),\qquad 0\le\xi\le1$$
>
> $\xi=1$이면 자유 동역학이 충격량 전부를 덜어 내고, $\Lambda\to\Lambda_L$이면 $\xi\to0$, 곧 관절이 잠긴 것처럼 군다. $\Lambda$와 $\Lambda_L$은 [[02-foundations/manipulator-kinematics-dynamics|10. §6]]의 뜻의 작업공간 관성으로, 접촉 방향들 위의 행렬이고 방향이 하나라면 그냥 질량이다.
> - **예**: 1차원 호퍼. 질량 $m_b=10\,\mathrm{kg}$인 몸체가 $m_f=1\,\mathrm{kg}$인 발 위에 있고, 둘 사이 다리 관절에 액추에이터 회전자가 질량 $m_r$로 반사되어 있다. 잠그면 발은 $\Lambda_L=11\,\mathrm{kg}$로 착지한다. 풀면 $\Lambda=m_f+m_bm_r/(m_b+m_r)$, 곧 발에 몸체와 회전자를 직렬로 더한 것으로 착지한다. 직접 구동($m_r=0$)이면 $1\,\mathrm{kg}$과 $\xi=1-1/11=0.91$, $m_r=10\,\mathrm{kg}$인 기어 구동이면 $6\,\mathrm{kg}$과 $\xi=1-6/11=0.45$다.
> - **비예**: P2. 베이스가 바닥에 볼트로 고정되어 있으므로 관절을 잠그면 말단은 움직일 수 없고, $\Lambda_L^{-1}=0$이라 어떤 구동계든 $\xi=1$이 되어 아무것도 말해 주지 않는다. 고정 베이스 팔에서는 §4의 말단 질량을 직접 비교한다 — $2.0$, $3.49$, $11.9\,\mathrm{kg}$.
> - **왜 중요한가**: 잠긴 로봇으로 정규화하므로 크기와 감속비가 다른 다리 로봇을 한 척도에 놓고, 감속비가 낮아질수록 커진다. MIT Cheetah가 낮은 감속비 구동계를 쓰는 정량적 근거가 이것이다.

### 8. 랩: P2 어깨의 캐스케이드와 감속비 스윕

과제는 들어올리기다. 팔꿈치를 $90^\circ$에 붙잡은 P2의 어깨를 $\theta_1=-0.5\,\mathrm{rad}$에서 고정 자세 $\theta_1=0$까지 $T=0.8\,\mathrm{s}$의 5차 시간 스케일링으로 올리고([[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장 §2]]; 최대 속도 $1.875\,\Delta\theta/T=1.17\,\mathrm{rad/s}$, 최대 가속도 $5.77\,\Delta\theta/T^2=4.51\,\mathrm{rad/s^2}$), 그다음 붙잡는다. 이 들어올리기는 [[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]이 P2에 고정한 액추에이터 한계($0.8\,\mathrm{rad/s}$, $2\,\mathrm{rad/s^2}$)보다 일부러 빠르다. 그 한계는 계획기가 그 안에 머무는 사양이고, 이 랩은 특정 구동계 하나가 그 너머에서 무엇을 할 수 있는지를 묻는다. $n=100$에서는 여유가 있고, $n=200$에서는 최대 속도 $1.17\,\mathrm{rad/s}$가 전압선에 닿는다. 제어기는 §5의 캐스케이드다. 중력 피드포워드가 있는 $1\,\mathrm{kHz}$ PD 위치 루프가 이상 기어 단위로 토크를 요구하므로 피드포워드는 $g_1/\eta$이고, 한 번 $n=100$에 맞춰 — $J_{eq}=4.75$에서 $20\,\mathrm{rad/s}$, 임계 감쇠 — 설계한 뒤 모든 감속비에 그대로 둔다. 한 기어박스에 맞춘 제어기가 그렇듯이. 그 안에서 $V_s$와 $I_{\max}$ 한계를 가진 $20\,\mathrm{kHz}$ PI 전류 루프가 돈다. 플랜트(제어되는 시스템)는 §1–§2다. 권선 방정식은 명시적 오일러로, 관절은 준음해 오일러로 전진하고([[02-foundations/lab-kernel|0.7 §2와 §3]]), 둘 다 전류 루프의 $50\,\mu\mathrm{s}$로 돈다. 속도는 완벽하게 잰다고 두고 PWM은 평균 전압으로 바꿨는데, 둘 다 루프에 유리한 이상화다.

(코드는 영어 절에 한 번만 싣는다.)

**스윕.** 감속비 일곱 개, 나머지는 모두 고정. "회전자 몫"은 $n^2J_m/J_{eq}$, "유지 상승"은 마지막 전류에서의 정상 권선 상승, "완료 시각"은 팔이 목표에서 $2\,\mathrm{mrad}$보다 멀리 있었던 마지막 순간이다. 기준 궤적 자체는 $0.8\,\mathrm{s}$에 끝난다.

| $n$ | 회전자 몫 | $\omega_0/n$ (rad/s) | 유지 전류 (A) | 유지 상승 (K) | 최대 전압 (V) | 최대 오차 (mrad) | 완료 시각 (s) | 닿은 한계 |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 30 | 0.023 | 8.00 | 8.175 | 668.3 | 12.5 | 340.7 | 1.392 | 들어올리는 중 $I_{\max}$; 열, 유지 9.7 s |
| 50 | 0.062 | 4.80 | 4.905 | 240.6 | 13.2 | 8.3 | 0.898 | 열, 유지 32.2 s |
| 80 | 0.146 | 3.00 | 3.066 | 94.0 | 13.8 | 9.2 | 0.905 | 없음 (100 K 중 94) |
| 100 | 0.211 | 2.40 | 2.453 | 60.1 | 15.3 | 10.0 | 0.911 | 없음 |
| 150 | 0.375 | 1.60 | 1.635 | 26.7 | 20.6 | 13.1 | 0.927 | 없음 |
| 200 | 0.516 | 1.20 | 1.226 | 15.0 | 24.0 | 19.5 | 0.944 | $V_s$ |
| 300 | 0.706 | 0.80 | 0.818 | 6.7 | 24.0 | 118.3 | 1.124 | $V_s$ |

**스윕 읽기.** 식만으로는 말해 줄 수 없었던 네 가지.

- **유지 전류는 $1/n$, 유지 열은 $1/n^2$로 떨어진다.** 감속비가 열 배 되는 동안 유지 전류는 $8.175$에서 $0.818\,\mathrm{A}$로, 정상 상승은 $668$에서 $6.7\,\mathrm{K}$로 백 배 떨어진다. $n=77.6$ 아래의 두 행은 P2를 잠시만, 주변 온도에서 출발해 $9.7\,\mathrm{s}$와 $32.2\,\mathrm{s}$ 동안 붙잡는다. 그리고 $n=30$은 제시간에 들어 올리지도 못한다. $I_{\max}$가 그 관절을 $21.9$의 중력에 대해 $24\,\mathrm{N{\cdot}m}$에서 막아 팔을 가속하는 데 약 $2\,\mathrm{N{\cdot}m}$만 남기므로, 기준 궤적에 최대 $0.34\,\mathrm{rad}$($19.5^\circ$) 뒤처지고 약 $0.6\,\mathrm{s}$ 늦게 도착한다.
- **회전자가 관절을 차지한다.** $J_{eq}$ 가운데 회전자의 몫은 $2\%$에서 $71\%$로 오르고, PD를 $n=100$ 설계에 고정해 두었으니 최대 오차도 함께 오른다 — 어떤 한계도 닿지 않는 행들에서 $8.3$, $9.2$, $10.0$, $13.1\,\mathrm{mrad}$ — 같은 이득의 더 무거운 관절은 더 느리고 덜 감쇠된 루프이기 때문이다. $n=300$에서 그 감쇠비는 $0.61$이다.
- **위쪽에서는 속도가 바닥난다.** 관절 무부하 속도 $\omega_0/n$이 들어올리기의 $1.17\,\mathrm{rad/s}$ 쪽으로 떨어지고, $Ri$ 강하가 더해져 공급에 처음 닿는 것은 $n=178$이다. $n=200$에서 루프는 동작 중간에 $0.21\,\mathrm{s}$ 동안 $24\,\mathrm{V}$ 한계를 타지만, 거기서 낼 수 있는 속도 $1.13\,\mathrm{rad/s}$가 기준의 $1.17$에 조금 못 미칠 뿐이라 오차는 $19.5\,\mathrm{mrad}$까지만 는다. $n=300$에서는 $0.49\,\mathrm{s}$ 동안 한계를 타고 관절은 $0.77\,\mathrm{rad/s}$에서 더 오르지 못한다 — 유지 전류에서의 전압선 속도, $(24-0.9)/(0.1\cdot300)$ — 그래서 팔은 $118\,\mathrm{mrad}$ 뒤처지고 $0.32\,\mathrm{s}$ 늦게 끝난다.
- **창, 그리고 그 가장자리에서 모델이 틀리는 것.** 열이 $n\approx78$ 아래를, 공급이 $n\approx178$ 위를 닫는다. $n=100$은 $60\,\mathrm{K}$ 유지와 $8.7\,\mathrm{V}$의 여유를 가지고 그 안에 있다. $n=30$을 뺀 모든 행이 목표를 조금 넘어서 끝나고 — 최대 $16\,\mathrm{mrad}$, $n=200$에서 — $0.12\,\mathrm{rad/s}$ 미만으로 되돌아온다. 그 되돌아오기에서는 링크가 기어박스를 구동하는데, 거기서 §2의 $\eta$ 하나는 손실을 엉뚱한 쪽에 둔다. 실제 기어박스라면 정지 마찰이 팔을 되돌아오기 전에 세우고, 표보다 적은 전류로 붙잡을 수 있다. 표의 유지 전류는 들어 올리는 값 $g_1/(\eta nk_t)$, 구동계를 고르는 기준이 되는 값이다.

**한 순간의 일률 장부.** §1의 등식 $k_t=k_e$를 $n=100$ 실행에서 와트 단위로 맞춘다. $t=0.40\,\mathrm{s}$에 관절은 $1.226\,\mathrm{rad/s}$로 돌고, 전류는 $2.824\,\mathrm{A}$, 증폭기가 거는 전압은 $15.05\,\mathrm{V}$다(`run` 안에서 `k == 8000`일 때 $\dot\theta$, $i$, $V$를 출력하면 보인다). 공급은 $Vi=42.5\,\mathrm{W}$를 낸다. $i^2R=8.0\,\mathrm{W}$는 권선을 데우고, 전류가 줄면서 인덕턴스에서 $0.1\,\mathrm{W}$가 도로 나오고, $e\,i=k_en\dot\theta\,i=0.1\cdot100\cdot1.226\cdot2.824=34.6\,\mathrm{W}$가 역기전력을 건너간다. 기계 쪽에서 $k_ti\,\omega_m$도 같은 $34.6\,\mathrm{W}$다 — 그 같음이 곧 $k_t=k_e$다. 그중 $0.5\,\mathrm{W}$는 회전자를 가속하고 베어링을 돌리는 데 쓰이고, 나머지 $34.1\,\mathrm{W}$가 기어박스에 들어가 $1-\eta=20\%$인 $6.8\,\mathrm{W}$를 떼이고 $27.3\,\mathrm{W}$가 링크에 닿아 팔을 들어 올리고 빠르게 한다. 공급을 떠난 것의 64퍼센트가 일을 했다.

### 9. 논문의 액추에이터 주장 읽기

| 논문의 말 | 물어볼 것 |
|---|---|
| "정격 토크" 또는 "최대 토크" | 연속인가 최대인가? 주변 온도·냉각·듀티는 무엇이고, 최대는 얼마나 지속되는가? |
| "가반하중 몇 kg" | 모멘트 팔을 정하는 자세는 무엇이고, 얼마나 오래, 어떤 속도로 붙잡는가? 접힌 자세의 가반하중은 다 편 팔에서는 다른 팔의 이야기다. |
| "모터 전류로 관절 토크를 추정" | 감속비, 양방향의 기어박스 효율, 마찰 모델, 그리고 가속 중 회전자의 $n^2J_m\ddot\theta$를 뺐는가. |
| "역구동 가능" 또는 "투명" | 속도와 가속도를 명시한 역구동 토크(§7), 전원 상태 — 권선 개방인가 단락인가 — 그리고 반사 관성 $n^2J_m$. |
| "고대역폭 토크 제어" | 전류 루프 대역폭은 관절 토크 대역폭이 아니다. 마찰, 기어 컴플라이언스, 회전자가 둘 사이에 있다. |
| "최대 속도" | 어떤 공급 전압, 어떤 부하에서인가? 전압선은 둘 다와 함께 움직인다. |

### 읽고 나면 말할 수 있어야 하는 것

- [ ] DC 모터의 권선 방정식과 회전자 방정식을 쓰고, SI 단위에서 $k_t=k_e$인 이유를 말한다.
- [ ] 주어진 $n$과 $\eta$에서 관절 토크를 모터 토크·전류·전압·열·온도 상승으로 바꾼다.
- [ ] 한 감속비에서 관절의 토크–속도 영역을 그리고, 유지와 동작을 그 위에 놓는다.
- [ ] 기어 달린 회전자를 질량 행렬에 더하고, 어느 감속비에서 팔과 같아지는지 말한다.
- [ ] 두 시정수를 숫자로 들어 전류 루프가 먼저인 이유를 말한다.
- [ ] 연속 토크와 최대 토크를 구별하고, 연속 정격을 넘는 유지가 얼마나 가는지 계산한다.
- [ ] 감속비가 역구동성과 전류를 토크로 읽는 일에 무엇을 하는지 설명한다.

### 스스로 점검

1. 정지 상태로 부하를 붙잡고 있는 관절의 감속비를 두 배로 한다. 유지 전류, 유지 열, 회전자의 반사 관성, 관절의 무부하 속도는 각각 어떻게 되는가?
2. 데이터시트가 역기전력 상수를 $10.5\,\mathrm{V/krpm}$로 준다. $\mathrm{N{\cdot}m/A}$ 단위의 토크 상수는 얼마이고, 왜 두 번째 측정이 필요 없는가?
3. 전류 루프는 팔이 없는 것처럼, 위치 루프는 전류 루프가 즉각인 것처럼 설계해도 되는 이유는?
4. 시연에서 관절이 무거운 공구를 팔을 다 뻗은 채 10초 동안 들고 있다. 그 관절이 하루 종일 그렇게 할 수 있다고 믿기 전에 물어볼 숫자 하나는?
5. 권선을 단락한 고감속비 팔을 놓으면 떨어지지 않고 천천히 내려앉는 이유는? 그리고 그 방식으로는 왜 결코 멈춰 있을 수 없는가?

> [!tip]- 정답 · Answers
> 1. 유지 전류는 절반이다, $i=g_1/(\eta nk_t)$이므로. 유지 열은 4분의 1이다, $i^2$으로 가므로. 반사 관성은 네 배다, $n^2$으로 가므로. 관절 무부하 속도는 절반이다, $V_s/(k_en)$이므로. 손잡이 하나에 답이 넷 — §8의 스윕에 가장 좋은 끝이 아니라 창이 있는 이유다.
> 2. 단위를 바꾼다. $1000\,\mathrm{rpm}$당 $10.5\,\mathrm{V}$는 $10.5/(1000\cdot2\pi/60)=0.100\,\mathrm{V{\cdot}s/rad}$이고, SI에서 토크 상수는 같은 숫자 $0.100\,\mathrm{N{\cdot}m/A}$다. 두 번째 측정이 필요 없는 것은 $k_t=k_e$가 모터 하나의 성질이 아니라 일률 보존 $e\,i=\tau_m\omega_m$의 진술이기 때문이다.
> 3. 시간 척도가 멀리 떨어져 있기 때문이다. 권선은 $\tau_e=L/R=1\,\mathrm{ms}$, 닫힌 전류 루프는 $0.5\,\mathrm{ms}$에 자리 잡는데, 속도는 회전자만의 $10\,\mathrm{ms}$보다 빨리 자리 잡을 수 없고 위치 루프는 전류 루프의 $2000$에 대해 $20\,\mathrm{rad/s}$로 맞춘다. 각 루프는 상대를 얼어 있거나 즉각인 것으로 본다. 면허는 전압이 바닥날 때 끝난다.
> 4. 그 자세에서의 연속 토크, 같은 말로 정상 권선 상승이다. 유지 전류를 $I_{\text{cont}}$에 대어 본다. 10초는 열 시정수 안이다. $n=50$의 고정 구동계는 P2의 10초 시연을 통과하고 $32\,\mathrm{s}$에 한계에 닿는다.
> 5. 권선을 단락하면 역기전력이 회전자를 제동하는 전류를 흘린다. 모터에서 $k_tk_e/R$, 관절에서 그 $n^2$배의 댐핑이다 — $n=100$에서 $100\,\mathrm{N{\cdot}m{\cdot}s/rad}$이므로 P2는 약 $0.2\,\mathrm{rad/s}$로 내려앉는다. 제동 토크는 속도에 비례하므로 관절이 멈추면 사라진다. 떨어지는 것을 늦출 수는 있어도 자세를 붙잡을 수는 없다.

### 과제 · Problem set

Tier A. 이 페이지, 그 선수 지식, 대상 카탈로그만으로. P2와 고정 구동계는 이 페이지의 대상과 같고, 각 항목이 말하는 것만 바꾼다.

1. **그리기.** 위의 그림을 $n=200$ 구동계로. 전류 한계, 양 끝을 가진 전압선, 열 한계선, 유지점 H. 그다음 들어올리기의 중간 요구 $1.17\,\mathrm{rad/s}$, $21.8\,\mathrm{N{\cdot}m}$를 더하고, 그것이 어느 경계를 넘는지 말한다.
2. **유도.** (a) 어깨의 중력 토크가 가장 큰 자세 $\theta=(-26.57^\circ,\,90^\circ)$, $g_1=9.81\sqrt5=21.94\,\mathrm{N{\cdot}m}$($2\cos\theta_1-\sin\theta_1$을 미분해 찾는다)의 P2를 $n=100$ 구동계로: 모터 토크, 전류, 전압, 열, 정상 상승. 무기한 붙잡는가? (b) 그 자세를 연속으로 붙잡는 가장 작은 정수 감속비. (c) $n=160$에서, 두 구동계를 단 $\theta_2=90^\circ$의 질량 행렬과 결합 $M_{12}/\sqrt{M_{11}M_{22}}$. (d) 중력을 빼고, 어깨 가속도 한 단위당 모터 토크를 최소로 하는 감속비 $n^\ast$를 유도하고 값을 구한 뒤, $n^\ast$에서 회전자의 $n^2J_m$이 $M_{11}/\eta$와 같음을 보인다. (e) $n=200$에서의 기계적 시정수와 $\tau_e$에 대한 비.
3. **실행.** §8 랩 코드의 `run`을 영어 절의 템플릿으로 바꾸고, `?`를 모두 채우고, `Vs = 48.0`으로 두고, 감속비 일곱 개의 스윕을 다시 돌린다. 어느 행이 바뀌고 어느 행이 그대로인지 보고하고, $n=300$ 행의 최대 오차는 떨어지는데 "완료 시각"은 늦어지는 이유를 설명한다.

> [!note]- 그리는 법 · How to draw it
> - **축은 관절의 양이다.** 가로는 관절 속도 $\dot\theta_1$, 세로는 구동계가 링크에 전달하는 토크 $\eta nk_ti$. 모터 단위로 그리면 이 페이지가 돌리는 유일한 손잡이가 숨는다.
> - **전류 한계는 수평선이다.** $\eta nk_tI_{\max}$에 긋는데, 증폭기가 전류를 막고 전류가 곧 토크이기 때문이다.
> - **전압선은 내려가는 선이다.** 전류 한계 위의 모서리 $(V_s-RI_{\max})/(k_en)$에서 관절 무부하 속도 $V_s/(k_en)$까지 내려가고, 양 끝에 값을 적는다. 계속 늘이면 속도 0에서 $\eta nk_tV_s/R$에 닿겠지만 전류 한계가 먼저 자른다(§3).
> - **열 한계선은 점선이다.** 연속 토크 $\eta nk_tI_{\text{cont}}$($I_{\text{cont}}=3.162\,\mathrm{A}$)에 긋고, 그 위의 영역은 몇 초 동안만 열려 있다(§6).
> - **H는 토크 축 위에 있다.** 감속비와 상관없이 $g_1=19.62\,\mathrm{N{\cdot}m}$에 놓고, 전류 $g_1/(\eta nk_t)$를 적은 뒤 열 한계선의 어느 쪽에 오는지 확인한다.
> - **동작은 그 요구가 그리는 고리로 그린다.** 위의 그림이 들어올리기를 그린 것처럼, 중력에서 출발해 가속하는 동안 오르고, 중간을 지나, 제동하는 동안 내려와 H로 들어간다. 요구 점 하나는 어느 경계 너머에 있는지로 판정한다. 수평선 위면 전류 한계, 기울어진 선 너머면 전압 한계다.
> - **$n$에 대한 비례를 확인한다.** 전류 한계는 $n$에 비례해 오르고, 무부하 속도는 $1/n$로 떨어지고, 전압선의 기울기는 $n^2$로 가팔라진다(§3). 그러니 감속비를 두 배로 하면 영역은 높이가 두 배, 폭이 절반이어야 한다.

> [!tip]- 정답 · Solutions
> 1. 전류 한계 $\eta nk_tI_{\max}=0.8\cdot200\cdot0.1\cdot10=160\,\mathrm{N{\cdot}m}$. 전압선 $\tau_j=(0.8\cdot200\cdot0.1/1)(24-0.1\cdot200\,\dot\theta)=384-320\,\dot\theta$, 모서리 $(384-160)/320=0.7\,\mathrm{rad/s}$에서 무부하 속도 $1.2\,\mathrm{rad/s}$까지. 열 한계선 $0.8\cdot200\cdot0.1\cdot3.162=50.6\,\mathrm{N{\cdot}m}$, 전압선과 $1.042\,\mathrm{rad/s}$에서 만난다. H는 $19.62\,\mathrm{N{\cdot}m}$, 이제 $1.226\,\mathrm{A}$. 영역은 $n=100$보다 높이가 두 배, 폭이 절반이다. 중간 요구는 영역 밖에, 전압선 너머에 있다. $1.17\,\mathrm{rad/s}$에서 선이 주는 것은 필요한 $21.8$에 대해 $384-320\cdot1.1719=9.0\,\mathrm{N{\cdot}m}$뿐이다.
> 2. (a) $\tau_m=21.94/(0.8\cdot100)=0.2742\,\mathrm{N{\cdot}m}$, $i=2.742\,\mathrm{A}$, $V=Ri=2.74\,\mathrm{V}$, $P=i^2R=7.52\,\mathrm{W}$, $\Delta T=R_{th}P=75.2\,\mathrm{K}$. $100\,\mathrm{K}$ 아래이므로 무기한 붙잡고, 열 예산의 $75\%$를 쓴다. (b) $n\ge21.94/(0.8\cdot0.1\cdot3.162)=86.7$이므로 $n=87$. (c) $n^2J_m=2.56$, $nJ_m=0.016$이므로 $M=\begin{pmatrix}5.5601&1.016\\1.016&3.56\end{pmatrix}$이고 결합은 $1.016/\sqrt{5.5601\cdot3.56}=0.228$, 맨 팔의 $0.577$에 대해서다. (d) $\tau_m=(nJ_m+M_{11}/(\eta n))\ddot\theta_1$. $d/dn$을 0으로 두면 $J_m-M_{11}/(\eta n^2)=0$이므로 $n^\ast=\sqrt{M_{11}/(\eta J_m)}=\sqrt{3/(0.8\cdot10^{-4})}=193.6$이고, 거기서 $n^{\ast2}J_m=3.75=M_{11}/\eta$. (e) $J=10^{-4}+3/(0.8\cdot4\cdot10^4)=1.9375\times10^{-4}\,\mathrm{kg{\cdot}m^2}$이므로 $\tau_{\text{mech}}=JR/(k_tk_e)=19.4\,\mathrm{ms}$, $\tau_e$의 $19$배 — 열 배라는 바닥에서 여전히 멀다.
> 3. 빈칸은 영어 해와 같다. $48\,\mathrm{V}$에서 $n=30$부터 $150$까지의 행은 $\omega_0/n$이 두 배가 되는 것($16.00$, $9.60$, $6.00$, $4.80$, $3.20$)을 빼고 그대로다. 거기서는 전압이 묶인 적이 없고, 열의 행은 $9.7$과 $32.2\,\mathrm{s}$를 유지한다. 열은 전류이고 전압은 그것을 건드리지 않기 때문이다. $n=200$은 표시를 잃고(최대 $26.8\,\mathrm{V}$, 오차 $17.5\,\mathrm{mrad}$, 완료 $0.942\,\mathrm{s}$), $n=300$도 그렇다(최대 $41.1\,\mathrm{V}$, 오차 $31.8\,\mathrm{mrad}$, 완료 $1.169\,\mathrm{s}$). $n=300$의 오차가 $118.3$에서 $31.8\,\mathrm{mrad}$로 떨어지는 것은 관절이 이제 들어올리기의 속도에 닿을 수 있기 때문이다. 늦게 끝나는 것은, $1.124$ 대신 $1.169\,\mathrm{s}$, 이제 $13.0$ 대신 $30.9\,\mathrm{mrad}$ 넘어서기 때문이다. $4.75\,\mathrm{kg{\cdot}m^2}$에 맞춘 PD가 $12.75$ 위에서 감쇠비 $0.61$로 돌고, $24\,\mathrm{V}$에서는 전압 한계가 속도를 막아 그것을 가리고 있었다. 전압은 속도를 산다. 유지도, 더 가벼운 관절도 사지 못한다.

### 출처

- K. M. Lynch and F. C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017 — §8.9 "Actuation, Gearing, and Friction": DC 모터의 전압 방정식, 전류·전압 한계를 가진 속도–토크 곡선, 효율을 가진 기어, 겉보기(반사) 관성과 더 대각이 되는 질량 행렬, 기어헤드 마찰. 무료 프리프린트는 [[04-robotics/modern-robotics-book|책 안내]]에 링크되어 있다.
- P. M. Wensing, A. Wang, S. Seok, D. Otten, J. Lang and S. Kim, "Proprioceptive Actuator Design in the MIT Cheetah: Impact Mitigation and High-Bandwidth Physical Interaction for Dynamic Legged Robots," *IEEE Transactions on Robotics*, vol. 33, no. 3, pp. 509–522, 2017. DOI 10.1109/TRO.2016.2640183. 관절에 동위치로 둔 힘 제어와 impact mitigation factor(§III-B3, 식 (33)–(35))를 인용한다.
- 위키 안: $M$·$g$·$\Lambda$는 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]], 운동 에너지로서의 질량 행렬은 [[04-robotics/modern-robotics/ch08-dynamics|MR 8장]], 캡스턴 위의 같은 맞바꿈은 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]], 역구동 가능한 구동계가 무엇에 쓰이는지는 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]].
- 구동계의 값은 예시용이고, 이 페이지의 모든 숫자는 그 값과 P2의 카탈로그 값으로 여기서 계산했다. 믿지 말고 다시 계산하라.
