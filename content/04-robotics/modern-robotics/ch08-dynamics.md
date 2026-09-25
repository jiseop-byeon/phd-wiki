---
title: "MR Ch.08 — Dynamics of Open Chains"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.8** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the equation of motion of [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §2–§5]] — this page is MR's energy route to the same three terms — with Lagrange's equation $\frac{d}{dt}\frac{\partial L}{\partial\dot\theta} - \frac{\partial L}{\partial\theta} = \tau$, $L = \mathcal{K} - U$, Newton's second law rewritten in energy terms and checked on one mass in [[02-foundations/manipulator-kinematics-dynamics|10. §2]], and the Christoffel symbols of [[02-foundations/manipulator-kinematics-dynamics|10. §4]]. This page applies Lagrange's equation to the arm but does not derive it, and Newton's second law alone will not carry you through Step 4 of the worked case. Also: positive-definite matrices ([[02-foundations/linear-algebra|1. Linear Algebra §3]]); torque, moment of inertia and the holding torque as plain physics ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §7–§8]]); and, for §2's non-example only, the Jacobian of [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]]. The plant is **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled; P2 is the catalog's planar two-link arm).
> [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §2–§5]]의 운동 방정식이 필요하다. 이 페이지는 같은 세 항에 이르는 MR의 에너지 경로다. 뉴턴 제2법칙을 에너지로 다시 쓰고 [[02-foundations/manipulator-kinematics-dynamics|10. §2]]에서 질량 하나로 검산한 라그랑주 방정식 $\frac{d}{dt}\frac{\partial L}{\partial\dot\theta} - \frac{\partial L}{\partial\theta} = \tau$, $L = \mathcal{K} - U$와 [[02-foundations/manipulator-kinematics-dynamics|10. §4]]의 크리스토펠 기호도 쓴다. 이 페이지는 라그랑주 방정식을 팔에 적용할 뿐 유도하지 않으며, 뉴턴 제2법칙만으로는 '대상으로 한 번 끝까지'의 4단계를 따라갈 수 없다. 그 밖에 양정부호 행렬([[02-foundations/linear-algebra|1. 선형대수 §3]]), 물리로서의 토크, 관성 모멘트, 유지 토크([[02-foundations/basic-mechanics|0.6.1 기초 역학 §7–§8]]), 그리고 §2의 비예에만 쓰는 [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안. 장치는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**다(장치(plant)는 제어 공학에서 제어 대상 시스템을 부르는 말이고, P2는 카탈로그의 평면 2링크 팔이다).

## English

**Core question**: what torques produce what accelerations?

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this chapter is the manipulation layer's equation of motion, standing on the mathematics floor that [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] laid, and in *"install that panel on the frame"* it serves *move the component* — the torque it takes to hold the arm and to carry it through a move (its chip sits in the manipulation band of the [[physical-ai-map|Physical AI Map]]). A controller tuned on a still arm meets the difference first: **P2**, the catalog's planar two-link arm ([[02-foundations/lab-plants|0.6]]), holds the catalog pose on $g = (19.62,\ 0)\,\mathrm{N{\cdot}m}$, but passing through it at $\dot\theta = (1,-1)\,\mathrm{rad/s}$ the same command leaves the elbow accelerating at $1\,\mathrm{rad/s^2}$, and holding the speed takes $1\,\mathrm{N{\cdot}m}$ more at each joint — at the elbow too, which statically carried nothing (Steps 5–6). Later pages use it section by section — [[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9 §2]] reads it to say why a jump in acceleration is a jump in torque, [[04-robotics/modern-robotics/ch11-robot-control|MR ch.11 §2]] feeds it forward as computed torque, [[04-robotics/actuators-drives|10.5 Actuators & Drives §4]] adds a geared rotor's inertia to its $M$, [[04-robotics/system-identification|5.5 System Identification §9]] fits its parameters from torques and [[04-robotics/capstone-panel-contact|26. Capstone]] runs it in the loop — in block 2 of the dissertation path ([[07-research-program/index|7. Research Program §8]], robotics sessions 19–21). After it you can derive $M$, $c$ and $g$ of P2 from its energies, read the equation both ways at any state, and name the term a simulator or controller leaves out.

> [!note] First pass · 처음이라면
> About three 60–90-minute sessions, robotics 19–21. **Session 1:** the Running object, the picture and Steps 1–4 of the Worked case — $M$ read off the kinetic energy, $g$ off the potential, $c$ from how $M$ changes — checking each line against [[02-foundations/manipulator-kinematics-dynamics|10. §3–§5]], where you met the same three terms by the Jacobian route; then Step 7, the arm at rest. End with the at-rest check by hand: $\tau = g(\theta)$ at the catalog pose, and forward dynamics fed that torque holds the arm still. **Session 2:** Steps 5 and 6, one moving state read both ways, with the figure that draws Step 6 as forces; then §1–§3. **Session 3:** the self-check and the problem set.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's planar two-link arm, with its mass properties switched on: unit links $L_1 = L_2 = 1\,\mathrm{m}$, point masses $m_1 = m_2 = 1\,\mathrm{kg}$ at the distal end of each link, and, because this chapter needs weight, the arm standing in the vertical plane with $g = 9.81\,\mathrm{m/s^2}$ acting in $-\hat y$. The catalog freezes the pose $\theta = (0^\circ, 90^\circ)$ — elbow at $(1,0)$, forearm straight up, tip at $(1,1)$ — and the mass matrix $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ there.

That matrix is quoted everywhere else in the wiki; on this page it is *derived*, and so are the other two terms of the equation of motion.

*Scope: this page teaches the joint-space equation of motion — where $M$, $c$ and $g$ come from, what each one does on P2, and the two directions the equation is read in. It does not teach the operational-space form or the $O(n)$ recursive implementation, and it does not recompute the catalog's $\Lambda = \mathrm{diag}(1,2)$; those live on [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §6]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 390" style="max-width:100%;height:auto" role="img" aria-label="P2 in the vertical plane at the catalog pose (0°, 90°) and, lighter, the straight pose (0°, 0°): point masses, equal 9.81 N weights, shoulder moment arms 1 m and 1 m against 1 m and 2 m, and the equation of motion circled at rest and while moving">
  <defs><marker id="ar8e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="ar8eL" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="0.9" stroke-dasharray="6 3 1.5 3" opacity="0.5"><line x1="62" y1="27.8" x2="62" y2="149.4"/><line x1="62" y1="183.6" x2="62" y2="245"/></g>
  <polygon points="62,160 52,175 72,175" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.6"><line x1="50" y1="180" x2="54" y2="175"/><line x1="55" y1="180" x2="59" y2="175"/><line x1="60" y1="180" x2="64" y2="175"/><line x1="65" y1="180" x2="69" y2="175"/><line x1="70" y1="180" x2="74" y2="175"/></g>
  <line x1="180" y1="160" x2="298" y2="160" stroke="currentColor" stroke-width="7" stroke-opacity="0.2" stroke-dasharray="10 5"/>
  <g stroke="currentColor" stroke-width="7" stroke-opacity="0.42" stroke-linecap="round" fill="none"><line x1="62" y1="160" x2="180" y2="160"/><line x1="180" y1="160" x2="180" y2="42"/></g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.9"><line x1="62" y1="42" x2="180" y2="42" stroke-dasharray="4 3"/><line x1="62" y1="38" x2="62" y2="46"/><line x1="180" y1="38" x2="180" y2="46"/></g>
  <text x="121" y="37" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.9">1 m</text>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.9"><line x1="62" y1="186" x2="180" y2="186" stroke-dasharray="4 3"/><line x1="62" y1="182" x2="62" y2="190"/><line x1="180" y1="182" x2="180" y2="190"/></g>
  <text x="121" y="181" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.9">1 m</text>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.55"><line x1="62" y1="235.5" x2="298" y2="235.5" stroke-dasharray="4 3"/><line x1="62" y1="231.5" x2="62" y2="239.5"/><line x1="298" y1="231.5" x2="298" y2="239.5"/></g>
  <text x="239" y="230.5" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.55">2 m</text>
  <line x1="298" y1="219" x2="298" y2="240.2" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 2.5" opacity="0.55"/>
  <g stroke="currentColor" stroke-width="1.8" marker-end="url(#ar8e)"><line x1="180" y1="167" x2="180" y2="219"/><line x1="180" y1="49" x2="180" y2="101"/></g>
  <g stroke="currentColor" stroke-width="1.6" opacity="0.5" marker-end="url(#ar8eL)"><line x1="298" y1="166" x2="298" y2="219"/></g>
  <circle cx="62" cy="160" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="180" cy="160" r="7" fill="currentColor"/>
  <circle cx="180" cy="42" r="7" fill="currentColor"/>
  <circle cx="298" cy="160" r="6" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6"/>
  <path d="M86.1 150.3 L85 147.9 L83.7 145.7 L82.2 143.6 L80.5 141.7 L78.6 140 L76.5 138.4 L74.3 137.1 L72 136 L69.6 135.1 L67.1 134.5 L64.6 134.1 L62 134 L59.4 134.1 L56.9 134.5 L54.4 135.1 L52 136 L49.7 137.1 L47.5 138.4 L45.4 140 L43.5 141.7 L41.8 143.6 L40.3 145.7 L39 147.9 L37.9 150.3" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#ar8e)"/>
  <path d="M203.3 154.2 L203 153.2 L202.7 152.1 L202.3 151.1 L201.9 150.1 L201.4 149.1 L200.9 148.2 L200.3 147.3 L199.7 146.3 L199.1 145.5 L198.4 144.6 L197.7 143.8 L197 143 L196.2 142.3 L195.4 141.6 L194.5 140.9 L193.7 140.3 L192.7 139.7 L191.8 139.1 L190.9 138.6 L189.9 138.1 L188.9 137.7 L187.9 137.3 L186.8 137 L185.8 136.7" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#ar8e)"/>
  <g fill="currentColor">
  <text x="30.1" y="139.9" font-size="12" text-anchor="middle">τ<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="214.2" y="136.4" font-size="12" text-anchor="middle">τ<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="168" y="34" font-size="11" text-anchor="end">m<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="190" y="180" font-size="11">m<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="189" y="75" font-size="11">9.81 N</text>
  <text x="187" y="209.6" font-size="11">9.81 N</text>
  <text x="290.9" y="29.5" font-size="11" text-anchor="end">g = 9.81 m/s²</text>
  <text x="171.7" y="110.4" font-size="11" text-anchor="end">arm from elbow: 0</text>
  <text x="192" y="46" font-size="11">(0°, 90°)</text>
  </g>
  <text x="305" y="209.6" font-size="11" fill="currentColor" opacity="0.6">9.81 N</text>
  <text x="255.5" y="150.6" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.6">(0°, 0°)</text>
  <line x1="300.4" y1="12.4" x2="300.4" y2="36.4" stroke="currentColor" stroke-width="1.4" marker-end="url(#ar8e)"/>
  <g fill="currentColor">
  <text x="352" y="26" font-size="11.5" font-weight="bold">catalog θ = (0°, 90°) · solid</text>
  <text x="352" y="52" font-size="11">M =</text>
  </g>
  <g fill="currentColor">
  <path d="M384 36 L380 36 L380 66 L384 66" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M416 36 L420 36 L420 66 L416 66" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="392" y="47" font-size="11" text-anchor="middle">3</text>
  <text x="408" y="47" font-size="11" text-anchor="middle">1</text>
  <text x="392" y="61" font-size="11" text-anchor="middle">1</text>
  <text x="408" y="61" font-size="11" text-anchor="middle">1</text>
  </g>
  <g fill="currentColor">
  <text x="426" y="52" font-size="11">kg·m²</text>
  <text x="352" y="86" font-size="11">g = (19.62, 0) N·m</text>
  <text x="352" y="103" font-size="11">arms from shoulder: 1 m, 1 m</text>
  </g>
  <g fill="currentColor" opacity="0.62">
  <text x="352" y="142" font-size="11.5" font-weight="bold">straight θ = (0°, 0°) · light</text>
  <text x="352" y="168" font-size="11">M =</text>
  <path d="M384 152 L380 152 L380 182 L384 182" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M416 152 L420 152 L420 182 L416 182" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="392" y="163" font-size="11" text-anchor="middle">5</text>
  <text x="408" y="163" font-size="11" text-anchor="middle">2</text>
  <text x="392" y="177" font-size="11" text-anchor="middle">2</text>
  <text x="408" y="177" font-size="11" text-anchor="middle">1</text>
  <text x="426" y="168" font-size="11">kg·m²</text>
  <text x="352" y="202" font-size="11">g = (29.43, 9.81) N·m</text>
  <text x="352" y="219" font-size="11">arms from shoulder: 1 m, 2 m</text>
  </g>
  <g fill="currentColor">
  <text x="14" y="276" font-size="11" font-weight="bold">held at rest</text>
  <text x="14" y="291" font-size="11">θ̇ = 0</text>
  <text x="14" y="305" font-size="11">θ̈ = 0</text>
  <text x="200" y="284" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="284" font-size="12.5" text-anchor="end">M(θ)θ̈</text>
  <text x="287" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="284" font-size="12.5" text-anchor="end">c(θ, θ̇)</text>
  <text x="372" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="405" y="284" font-size="12.5" text-anchor="middle">g(θ)</text>
  <text x="434" y="284" font-size="12">= (19.62, 0) N·m</text>
  </g>
  <ellipse cx="405" cy="280" rx="19" ry="12" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g fill="currentColor">
  <text x="14" y="324" font-size="11" font-weight="bold">moving through</text>
  <text x="14" y="339" font-size="11">θ̇ = (1, −1) rad/s</text>
  <text x="14" y="353" font-size="11">θ̈ = 0</text>
  <text x="200" y="332" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="332" font-size="12.5" text-anchor="end">M(θ)θ̈</text>
  <text x="287" y="332" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="332" font-size="12.5" text-anchor="end">c(θ, θ̇)</text>
  <text x="372" y="332" font-size="12.5" text-anchor="middle">+</text>
  <text x="405" y="332" font-size="12.5" text-anchor="middle">g(θ)</text>
  <text x="434" y="332" font-size="12">= (20.62, 1) N·m</text>
  </g>
  <ellipse cx="330" cy="328" rx="31" ry="12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 2.5"/>
  <ellipse cx="405" cy="328" rx="22" ry="13" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 2.5"/>
  <text x="14" y="376" font-size="11" fill="currentColor" opacity="0.85">only the moving row circles c: c = (1, 1) N·m, 1 N·m more at each joint</text>
</svg>

Plant **P2** in the vertical plane, solid at the catalog pose $(0^\circ, 90^\circ)$ and lighter at the straight pose $(0^\circ, 0^\circ)$, with a $1\,\mathrm{kg}$ point mass and a $9.81\,\mathrm{N}$ weight at the end of each link. The horizontal moment arms from the shoulder are $1$ and $1\,\mathrm{m}$ at the catalog pose (mass 2 sits right above the elbow, arm $0$ there) against $1$ and $2\,\mathrm{m}$ when straight — so $g$ rises from $(19.62,\ 0)$ to $(29.43,\ 9.81)\,\mathrm{N\,m}$ and $M$ from $\begin{pmatrix}3&1\\1&1\end{pmatrix}$ to $\begin{pmatrix}5&2\\2&1\end{pmatrix}\,\mathrm{kg\,m^2}$. At the catalog pose, holding still takes only $g$, $\tau = (19.62,\ 0)\,\mathrm{N\,m}$, while moving through at $\dot\theta = (1,-1)\,\mathrm{rad/s}$ adds $c = (1,1)$, for $\tau = (20.62,\ 1)\,\mathrm{N\,m}$.

### Worked case · 대상으로 한 번 끝까지

Page 10 built these three terms at this pose already — $M$ by the Jacobian route in [[02-foundations/manipulator-kinematics-dynamics|10. §3]], the velocity terms from their Christoffel formula in §4, and $g$ with a free-body check in §5. Steps 1–4 reach all three by MR's energy route instead, from the two energies alone: check each line against 10. One notation map first, because the two pages letter things differently: this page's vector $c(\theta, \dot\theta)$ is 10's product $C(\theta,\dot\theta)\,\dot\theta$ (only the product is unique, 10 §2); its $\Gamma_{ijk}$ are 10's $c_{ijk}$ (the letter $c$ is taken here by the vector); and its $\mathcal{K}$ and $U$ are 10's $T$ and $V$. The one equation the steps apply is Lagrange's equation, checked against Newton's second law on one mass in [[02-foundations/manipulator-kinematics-dynamics|10. §2]]:

$$\frac{d}{dt}\frac{\partial\mathcal{K}}{\partial\dot\theta_i} - \frac{\partial\mathcal{K}}{\partial\theta_i} + \frac{\partial U}{\partial\theta_i} = \tau_i, \qquad i = 1, 2$$

with $\mathcal{K}$ the kinetic and $U$ the potential energy, so Steps 1–2 build $\mathcal{K}$, Step 3 differentiates $U$, and Step 4 collects what differentiating $\mathcal{K}$ leaves over.

**Step 1 — kinetic energy, written out.** Write $c_1 = \cos\theta_1$, $s_1 = \sin\theta_1$, $c_{12} = \cos(\theta_1{+}\theta_2)$ and $s_{12} = \sin(\theta_1{+}\theta_2)$. Mass 1 sits at $(L_1c_1,\ L_1s_1)$ and mass 2 at the tip, $(L_1c_1 + L_2c_{12},\ L_1s_1 + L_2s_{12})$, so differentiating in time gives

$$v_1 = L_1\dot\theta_1\,(-s_1,\ c_1), \qquad v_2 = L_1\dot\theta_1\,(-s_1,\ c_1) + L_2(\dot\theta_1{+}\dot\theta_2)\,(-s_{12},\ c_{12})$$

— these are 10 §3's $J_1\dot\theta$ and $J_2\dot\theta$ — and squaring them gives

$$|v_1|^2 = L_1^2\dot\theta_1^2, \qquad |v_2|^2 = L_1^2\dot\theta_1^2 + L_2^2(\dot\theta_1{+}\dot\theta_2)^2 + 2L_1L_2\,\dot\theta_1(\dot\theta_1{+}\dot\theta_2)\cos\theta_2$$

because the cross term of the two link velocities carries $c_1c_{12} + s_1s_{12} = \cos\theta_2$ — the *relative* elbow angle, and nothing else. With the catalog's unit links and unit masses, $2\mathcal{K} = |v_1|^2 + |v_2|^2$ collects into

$$2\mathcal{K} = (3 + 2\cos\theta_2)\,\dot\theta_1^2 + 2(1 + \cos\theta_2)\,\dot\theta_1\dot\theta_2 + \dot\theta_2^2.$$

**Step 2 — read $M$ off the quadratic form.** Matching $2\mathcal{K} = \dot\theta^\top M\dot\theta$ (the quadratic form that defines the mass matrix, §2) term by term, the $\dot\theta_1^2$ coefficient is $M_{11}$, the $\dot\theta_2^2$ coefficient is $M_{22}$, and the $\dot\theta_1\dot\theta_2$ coefficient is $2M_{12}$ because symmetry splits it between the two off-diagonal entries:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

and only $\theta_2$ appears, since turning the whole arm about the shoulder cannot change how mass is distributed about its own axes. At the catalog pose $\cos\theta_2 = 0$, so $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ — the catalog matrix, now derived rather than quoted, and 10 §3's again. Its eigenvalues are $2 \pm \sqrt2 = 3.4142$ and $0.5858\ \mathrm{kg\,m^2}$, both positive, and their ratio $5.83$ is how much heavier the arm's heaviest direction is than its lightest. Straighten to $\theta_2 = 0$ and $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$, whose eigenvalues are $3 \pm 2\sqrt2 = 5.8284$ and $0.1716$, a ratio of $34.0$: extending the arm does not merely make it heavier, it makes it far more *unevenly* heavy.

**Step 3 — gravity, from the potential.** The potential energy is $U = g(m_1y_1 + m_2y_2) = g\,(2\sin\theta_1 + \sin(\theta_1{+}\theta_2))$ with the catalog numbers, and the gravity vector is its gradient, the $\partial U/\partial\theta$ term of Lagrange's equation:

$$g(\theta) = \frac{\partial U}{\partial \theta} = \bigl(\,g(2\cos\theta_1 + \cos(\theta_1{+}\theta_2)),\ \ g\cos(\theta_1{+}\theta_2)\,\bigr)$$

where each cosine is a horizontal moment arm read straight off the picture. At the catalog pose $\cos\theta_1 = 1$ and $\cos(\theta_1{+}\theta_2) = 0$, giving $g = (19.62,\ 0)\,\mathrm{N\,m}$: the shoulder holds both masses at $1\,\mathrm{m}$, and the elbow holds nothing because its mass is directly overhead — the same numbers as 10 §5's free-body check and [[02-foundations/basic-mechanics|0.6.1 §8]]'s holding torque. At the straight pose the same formula gives $(29.43,\ 9.81)$ — half again as much at the shoulder.

**Step 4 — Coriolis, from how $M$ changes.** The velocity-product term comes from differentiating $M(\theta)$ inside the Lagrange equation; collecting it with the Christoffel symbols $\Gamma_{ijk} = \tfrac12(\partial M_{ij}/\partial\theta_k + \partial M_{ik}/\partial\theta_j - \partial M_{jk}/\partial\theta_i)$ of [[02-foundations/manipulator-kinematics-dynamics|10. §4]] (there $c_{ijk}$, whose substitution 10 only asserts) and using $c_i = \sum_{j,k}\Gamma_{ijk}\dot\theta_j\dot\theta_k$, only $\partial M/\partial\theta_2 \propto \sin\theta_2$ survives. Explicitly, the only nonzero derivatives are $\partial M_{11}/\partial\theta_2 = -2\sin\theta_2$ and $\partial M_{12}/\partial\theta_2 = \partial M_{21}/\partial\theta_2 = -\sin\theta_2$, because nothing depends on $\theta_1$ and $M_{22}$ is constant. So, for instance, $\Gamma_{122} = \tfrac12(\partial M_{12}/\partial\theta_2 + \partial M_{12}/\partial\theta_2 - \partial M_{22}/\partial\theta_1) = -\sin\theta_2$ and $\Gamma_{212} = \tfrac12(\partial M_{21}/\partial\theta_2 + \partial M_{22}/\partial\theta_1 - \partial M_{12}/\partial\theta_2) = 0$, and all eight symbols are

$$\Gamma_{112} = \Gamma_{121} = \Gamma_{122} = -\sin\theta_2, \qquad \Gamma_{211} = \sin\theta_2, \qquad \Gamma_{111} = \Gamma_{212} = \Gamma_{221} = \Gamma_{222} = 0$$

so that $c_1 = \Gamma_{112}\dot\theta_1\dot\theta_2 + \Gamma_{121}\dot\theta_2\dot\theta_1 + \Gamma_{122}\dot\theta_2^2$ and $c_2 = \Gamma_{211}\dot\theta_1^2$, which is

$$c(\theta, \dot\theta) = \bigl(\,-\sin\theta_2\,\dot\theta_2(2\dot\theta_1 + \dot\theta_2),\ \ \sin\theta_2\,\dot\theta_1^2\,\bigr)$$

which is quadratic in $\dot\theta$ and proportional to $\sin\theta_2$ — 10 §4's vector with $h = -\sin\theta_2$. Two consequences follow immediately and both get used below: $c$ vanishes identically whenever the arm is still, and it vanishes identically at $\theta_2 = 0$ or $180^\circ$ **whatever the velocity**, because a straight or folded elbow is where $M$ momentarily stops changing. The catalog pose $\theta_2 = 90^\circ$ is the opposite extreme, $|\sin\theta_2| = 1$: it is the most strongly velocity-coupled pose this arm has.

**Step 5 — one numerical case, end to end.** Put P2 at the catalog pose and set it *moving*: $\dot\theta = (1, -1)\,\mathrm{rad/s}$, shoulder opening while the elbow straightens. Command exactly the gravity torque, $\tau = g = (19.62,\ 0)$, which is what a naive "gravity compensation" controller does.

- Coriolis and centripetal: $c_1 = -1\cdot(-1)\bigl(2(1) + (-1)\bigr) = 1$ and $c_2 = 1\cdot(1)^2 = 1$, so $c = (1,\ 1)\,\mathrm{N\,m}$.
- Net: $\tau - c - g = (19.62, 0) - (1,1) - (19.62, 0) = (-1,\ -1)\,\mathrm{N\,m}$.
- Inverse mass matrix: $\det M = 3 - 1 = 2$, so $M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}$.
- Forward dynamics (the equation of motion solved for $\ddot\theta$, §3): $\ddot\theta = M^{-1}(\tau - c - g) = (0,\ -1)\,\mathrm{rad/s^2}$.

So cancelling gravity on a *moving* arm leaves the shoulder with exactly zero acceleration and the elbow straightening faster, at $1\,\mathrm{rad/s^2}$. All of that comes from the velocity term $c$ — its Coriolis part $(2, 0)$ and centripetal part $(-1, 1)$, split in §1 — since at rest the same command would produce $\ddot\theta = 0$ and nothing would happen at all. A controller tuned on a stationary arm and tested on a moving one meets this difference first.

**Step 6 — the same line read backwards.** Ask instead for $\ddot\theta = 0$ at that same state — hold the velocity steady through the pose. Inverse dynamics (the same equation evaluated for $\tau$, §3) gives $\tau = c + g = (20.62,\ 1)\,\mathrm{N\,m}$: one extra newton-metre at *each* joint over the static hold, including at the elbow, which statically needed nothing. Where does a torque at an unloaded joint come from? With $\dot\theta = (1,-1)$ the forearm does not turn, since $\dot\theta_1 + \dot\theta_2 = 0$: the elbow carries it round the shoulder, so both masses move up at $1\,\mathrm{m/s}$ and, circling at $1\,\mathrm{rad/s}$, both accelerate at $(-1, 0)\,\mathrm{m/s^2}$ toward the centres of their circles. To bend the tip mass's path the forearm must pull it $1\,\mathrm{N}$ sideways on top of the $9.81\,\mathrm{N}$ that holds its weight, and that $1\,\mathrm{N}$ acts $1\,\mathrm{m}$ above both joint axes: $c = (1, 1)$. The elbow mass's own sideways $1\,\mathrm{N}$ acts along link 1, through the shoulder's axis, and adds nothing. This velocity coupling is exactly what a feedforward term supplies in [[04-robotics/modern-robotics/ch11-robot-control|ch.11]] — torque computed from the model and sent to the motors before any tracking error appears, where feedback only reacts once the error is there; §3 redoes the same sweep as MR's Newton–Euler.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="P2 at the catalog pose moving at θ̇ = (1, −1): the forearm translates without turning, so both masses move up at 1 m/s and accelerate at (−1, 0) m/s²; the forearm pulls the tip mass 1 N sideways, 1 m above both joint axes, giving c = (1, 1) N·m and τ = (20.62, 1) N·m.">
  <defs><marker id="mr08s6e" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="161.7,282.5 162.5,280.7 163.3,279.0 164.0,277.2 164.7,275.4 165.4,273.6 166.0,271.8 166.6,270.0 167.2,268.2 167.7,266.3 168.3,264.5 168.7,262.6 169.2,260.7 169.6,258.9 170.0,257.0 170.3,255.1 170.6,253.2 170.9,251.3 171.2,249.4 171.4,247.5 171.6,245.6 171.7,243.7 171.8,241.8 171.9,239.8 172.0,237.9 172.0,236.0 172.0,234.1 171.9,232.2 171.8,230.2 171.7,228.3 171.6,226.4 171.4,224.5 171.2,222.6 170.9,220.7 170.6,218.8 170.3,216.9 170.0,215.0 169.6,213.1 169.2,211.3 168.7,209.4 168.3,207.5 167.7,205.7 167.2,203.8 166.6,202.0 166.0,200.2 165.4,198.4 164.7,196.6 164.0,194.8 163.3,193.0 162.5,191.3 161.7,189.5 160.9,187.8 160.0,186.1 159.1,184.4 158.2,182.7 157.3,181.0 156.3,179.3 155.3,177.7 154.3,176.1 153.2,174.5 152.1,172.9 151.0,171.3 149.8,169.8 148.7,168.3 147.5,166.8 146.3,165.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.55"/>
  <polyline points="161.7,172.5 162.5,170.7 163.3,169.0 164.0,167.2 164.7,165.4 165.4,163.6 166.0,161.8 166.6,160.0 167.2,158.2 167.7,156.3 168.3,154.5 168.7,152.6 169.2,150.7 169.6,148.9 170.0,147.0 170.3,145.1 170.6,143.2 170.9,141.3 171.2,139.4 171.4,137.5 171.6,135.6 171.7,133.7 171.8,131.8 171.9,129.8 172.0,127.9 172.0,126.0 172.0,124.1 171.9,122.2 171.8,120.2 171.7,118.3 171.6,116.4 171.4,114.5 171.2,112.6 170.9,110.7 170.6,108.8 170.3,106.9 170.0,105.0 169.6,103.1 169.2,101.3 168.7,99.4 168.3,97.5 167.7,95.7 167.2,93.8 166.6,92.0 166.0,90.2 165.4,88.4 164.7,86.6 164.0,84.8 163.3,83.0 162.5,81.3 161.7,79.5 160.9,77.8 160.0,76.1 159.1,74.4 158.2,72.7 157.3,71.0 156.3,69.3 155.3,67.7 154.3,66.1 153.2,64.5 152.1,62.9 151.0,61.3 149.8,59.8 148.7,58.3 147.5,56.8 146.3,55.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.55"/>
  <polyline points="62.0,236.0 152.1,172.9 152.1,62.9" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" opacity="0.15"/>
  <polyline points="62.0,236.0 172.0,236.0 172.0,126.0" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.42"/>
  <circle cx="62.0" cy="236.0" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="172.0" cy="236.0" r="7" fill="currentColor"/><circle cx="172.0" cy="126.0" r="7" fill="currentColor"/>
  <line x1="184.0" y1="236.0" x2="184.0" y2="181.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr08s6e)"/>
  <line x1="184.0" y1="126.0" x2="184.0" y2="71.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr08s6e)"/>
  <line x1="164.0" y1="126.0" x2="117.0" y2="126.0" stroke="currentColor" stroke-width="2.4" marker-end="url(#mr08s6e)"/>
  <line x1="164.0" y1="249.0" x2="117.0" y2="249.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr08s6e)" opacity="0.8"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.8"><line x1="30" y1="236.0" x2="30" y2="126.0"/><line x1="25" y1="236.0" x2="35" y2="236.0"/><line x1="25" y1="126.0" x2="35" y2="126.0"/></g>
  <line x1="35" y1="126.0" x2="111.0" y2="126.0" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.6"/>
  <line x1="30" y1="241.0" x2="30" y2="279.0" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.6"/>
  <g font-size="11" fill="currentColor">
    <text x="24" y="185.0" text-anchor="end">1 m</text>
    <text x="190.0" y="191.0">v</text>
    <text x="190.0" y="81.0">v</text>
    <text x="121.0" y="119.0">a</text>
    <text x="121.0" y="264.0">a</text>
    <text x="144.1" y="48.9" text-anchor="end" opacity="0.6">a moment later,</text>
    <text x="144.1" y="62.9" text-anchor="end" opacity="0.6">still upright</text>
    <text x="8" y="291.0" opacity="0.8">height of both joint axes</text>
  </g>
  <line x1="290" y1="14" x2="290" y2="288" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="300" y="28" font-size="12">Step 6, drawn as forces</text>
    <text x="300" y="46" opacity="0.8">θ = (0°, 90°), θ̇ = (1, −1) rad/s, θ̈ = 0</text>
    <text x="300" y="70" opacity="1">the forearm does not turn: θ̇₁ + θ̇₂ = 0</text>
    <text x="300" y="88" opacity="1">both masses: v = (0, 1) m/s,</text>
    <text x="300" y="106" opacity="1">a = (−1, 0) m/s², toward each centre</text>
    <text x="300" y="122" opacity="0.75">(dotted: the circles about (0, 0) and (0, 1))</text>
    <text x="300" y="146" opacity="1">forearm on the tip mass: (−1, 9.81) N,</text>
    <text x="300" y="164" opacity="1">9.81 N up holds its weight → g</text>
    <text x="300" y="182" opacity="1">1 N sideways bends its path → c</text>
    <text x="300" y="206" opacity="1">that 1 N acts 1 m above both axes:</text>
    <text x="300" y="224" opacity="1">c = (1 · 1, 1 · 1) = (1, 1) N·m</text>
    <text x="300" y="248" opacity="0.85">the elbow mass's 1 N passes the shoulder: 0</text>
    <text x="300" y="274" opacity="1" font-size="12">τ = g + c = (20.62, 1) N·m</text>
  </g>
</svg>

Step 6 drawn as forces at the catalog pose, to scale: the forearm translates without turning, so both masses move up at $1\,\mathrm{m/s}$ and accelerate at $(-1, 0)\,\mathrm{m/s^2}$ (arrows at half a metre per unit), and the forearm's push on the tip mass, $(-1,\ 9.81)\,\mathrm{N}$, splits into the $9.81\,\mathrm{N}$ that holds its weight ($g$) and the $1\,\mathrm{N}$ that bends its path ($c$). That $1\,\mathrm{N}$ acts $1\,\mathrm{m}$ above both joint axes, so $c = (1, 1)\,\mathrm{N{\cdot}m}$ and $\tau = g + c = (20.62,\ 1)\,\mathrm{N{\cdot}m}$.

**Step 7 — at rest, only $g$ survives.** Set $\dot\theta = 0$. Then $c = 0$ by step 4 and the equation collapses to $\tau = M\ddot\theta + g$. Holding still means $\ddot\theta = 0$ and $\tau = g = (19.62,\ 0)$; feed that to forward dynamics and $\ddot\theta = M^{-1}(\tau - g) = 0$, so the simulator's next step does nothing. This is the state the problem set draws at another pose, and the one every other pose on this page should be compared against.

### 1. Where the three terms come from — one link, then two

A pendulum needs only inertia times acceleration plus gravity. Add a second link and the inertia starts to depend on the pose and a velocity term turns on — that is the whole jump from "one equation" to "why multi-link dynamics are hard", and this section names the three terms the jump leaves.

**The equation of motion**, everything in one line:

$$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$

with the mass matrix (configuration-dependent inertia), the Coriolis and centripetal terms (velocity products), and gravity. The three add rather than compete because each is a separate demand on the same actuators: $M\ddot\theta$ is what it costs to change speed, $c$ is what it costs to be moving at all in a shape that is changing, and $g$ is what it costs simply to exist against gravity.

> **Coriolis and centripetal terms, defined.** The **Coriolis and centripetal terms** $c(\theta, \dot\theta)$ are *a vector of joint torques that depends on configuration and velocity*. Three conditions define them. They are **quadratic in the joint velocities**: every entry is a sum of products $\dot\theta_j\dot\theta_k$, so $c(\theta, a\dot\theta) = a^2c(\theta, \dot\theta)$ and $c = 0$ at rest. They are **generated by $M(\theta)$ alone**: the coefficients are derivatives of the mass matrix, so a constant $M$, like the pendulum's below, gives $c \equiv 0$. And they are **named by the product**: a $\dot\theta_j^2$ term is centripetal (page 10 and many texts call the same term centrifugal), a $\dot\theta_j\dot\theta_k$ term with $j \ne k$ is Coriolis (MR §8.1).
>
> $$c_i(\theta, \dot\theta) = \sum_{j,k}\Gamma_{ijk}(\theta)\,\dot\theta_j\dot\theta_k, \qquad \Gamma_{ijk} = \tfrac12\Bigl(\frac{\partial M_{ij}}{\partial\theta_k} + \frac{\partial M_{ik}}{\partial\theta_j} - \frac{\partial M_{jk}}{\partial\theta_i}\Bigr)$$
>
> where $\Gamma_{ijk}$ are the Christoffel symbols of [[02-foundations/manipulator-kinematics-dynamics|10. §4]] (10's $c_{ijk}$); the form is quadratic because the chain rule turns $\dot M$ into $\sum_k (\partial M/\partial\theta_k)\,\dot\theta_k$, one more velocity beside the one already in $M\dot\theta$.
>
> - **Example**: P2 at the catalog pose moving at $\dot\theta = (1, -1)$. Step 5's $c = (1, 1)\,\mathrm{N\,m}$ is a Coriolis part $(2, 0)$, from $-2\sin\theta_2\,\dot\theta_1\dot\theta_2$, plus a centripetal part $(-1, 1)$.
> - **Non-example**: viscous friction $b\dot\theta$. It also depends on velocity and vanishes at rest, but it is linear: at $\dot\theta = (2, -2)$ friction doubles while $c$ quadruples to $(4, 4)$. A linear model fitted at one speed matches only there and at rest, and is wrong at every other speed along that direction.

> **Gravity vector, defined.** The **gravity vector** $g(\theta)$ is *a vector of joint torques that depends on configuration only*. Three conditions define it. It is **independent of $\dot\theta$ and $\ddot\theta$**, so it is the whole torque needed to hold any pose still. It is **the gradient of one potential energy**, so a single scalar $U(\theta)$ generates every entry. And **joint $i$ feels only the masses beyond it**: turning joint $i$ raises or lowers nothing inboard of it, so $g_i$ sums over the outboard links alone.
>
> $$g(\theta) = \frac{\partial U}{\partial\theta}, \qquad U(\theta) = \sum_k m_k\,g\,y_k(\theta)$$
>
> where $m_k$ and $y_k$ are the mass and height of point mass $k$ and $g = 9.81\,\mathrm{m/s^2}$, the scalar sharing the vector's letter as in MR. On P2, whose joint axes are horizontal, each term is a weight times its signed horizontal offset from the joint's axis, because differentiating a height with respect to such a joint angle returns that offset.
>
> - **Example**: P2 at the catalog pose, $g = (19.62,\ 0)\,\mathrm{N\,m}$: the shoulder carries both masses at $1\,\mathrm{m}$. Straight, $(29.43,\ 9.81)$.
> - **Non-example**: weight times link length. At the catalog pose it charges the elbow $m_2 g L_2 = 9.81\,\mathrm{N\,m}$, but $g_2 = 0$, because the forearm mass sits directly above the elbow; the product is right only when the link lies horizontal, as in the straight pose. A gravity-compensation term built this way pushes a joint that needs nothing.

**A pendulum has only two of them.** With mass $m$, length $l$ and angle $\theta$ from vertical, $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$.

- $M = ml^2$ is the inertia, and it is constant.
- $g(\theta) = mgl\sin\theta$ is the gravity torque, and it depends on configuration.
- The Coriolis term $c$ is *zero* because $M$ does not depend on $\theta$. (A one-joint system with configuration-dependent inertia would still have $c = \tfrac12 M'(\theta)\dot\theta^2$.)

On P2 the worked case put numbers on both halves of the jump a second link makes: $M_{11}$ falls from $5$ to $3\ \mathrm{kg\,m^2}$ between the straight and catalog poses because the forearm mass moves closer to the shoulder axis, so the same shoulder acceleration needs $40\,\%$ less torque; and the off-diagonal entry, $2$ then $1$, is coupling — accelerating one joint pushes on the other. The pendulum had neither effect.

### 2. The mass matrix, defined

A simulator inverts $M$ at every step, a computed-torque controller multiplies by it, and it is the reason gains that work at one pose fail at another: a controller designed as though $M$ were the identity is designing for a robot that does not exist. So it deserves an exact definition.

A **mass matrix** $M(\theta)$ is the $n \times n$ matrix that turns joint velocities into kinetic energy at a given configuration. It is not a number attached to the robot; it is a matrix-valued *function of the configuration*, and it has three defining conditions, all of which must hold:

1. it represents the kinetic energy as a quadratic form, $\mathcal{K} = \tfrac12\dot\theta^\top M(\theta)\dot\theta$;
2. it is **symmetric**, $M = M^\top$;
3. it is **positive definite**, $\dot\theta^\top M\dot\theta > 0$ for every nonzero $\dot\theta$ ([[02-foundations/linear-algebra|1. Linear Algebra §3]]).

$$\mathcal{K}(\theta, \dot\theta) = \tfrac12\,\dot\theta^\top M(\theta)\,\dot\theta$$

where $\dot\theta \in \mathbb{R}^n$ is the joint velocity, $M(\theta) \in \mathbb{R}^{n\times n}$ the mass matrix at that configuration, and $\mathcal{K}$ the arm's total kinetic energy in joules — this is the form Step 2 read $M$ off, because the kinetic energy of point masses is a sum of squared speeds, each linear in $\dot\theta$. Condition 3 holds because a moving arm's kinetic energy is positive ([[02-foundations/manipulator-kinematics-dynamics|10. §2]] shows it for P2: $\det M = 1 + \sin^2\theta_2 \ge 1$), and it guarantees that $M^{-1}$ exists, so forward dynamics is solvable at every configuration.

- **Example**: P2's $M(\theta_2)$ from step 2, with $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ at the catalog pose. Symmetric by inspection; positive definite because its eigenvalues $2 \pm \sqrt2$ are both positive; and $\tfrac12(1,-1)M(1,-1)^\top = 1\,\mathrm{J}$ is the kinetic energy of the step 5 motion, a positive number as required.
- **Non-example**: the operational-space inertia $\Lambda = (JM^{-1}J^\top)^{-1} = \mathrm{diag}(1,2)$, also listed in the catalog at this same pose. It is symmetric and positive definite too, and it is *not* the mass matrix: it is the inertia the **tip** feels in task coordinates, so its entries are kilograms rather than $\mathrm{kg\,m^2}$ and it has one entry per task direction rather than per joint. Reading "the arm is twice as heavy in $y$" off $\Lambda$ and then substituting $\Lambda$ into $\tau = M\ddot\theta + \ldots$ is the standard way this page's object gets confused with page 10's.
- **The motors are in it too**: a geared motor adds its rotor's reflected inertia $n^2J_m$ to $M$; with the frozen drive of [[04-robotics/actuators-drives|10.5 Actuators & Drives §4]] at a gear ratio of 100 it already equals the link's own at P2's elbow.

### 3. Forward and inverse dynamics, and the two derivations

**Forward dynamics** ($\tau \to \ddot\theta$) is the equation solved for acceleration, $\ddot\theta = M^{-1}(\tau - c - g)$, and it is what a simulator integrates each step — every physics engine (Isaac, MuJoCo) is this equation plus contacts. **Inverse dynamics** ($\ddot\theta \to \tau$) is the same equation evaluated left to right, and it is what a controller feeds forward ([[04-robotics/modern-robotics/ch11-robot-control|ch.11]]). Steps 5 and 6 of the worked case are the same state read both ways, which is the cheapest way to see that there is only one equation here.

> **Forward and inverse dynamics, defined.** **Forward dynamics** and **inverse dynamics** are *the two computational problems posed on one equation of motion*, told apart by what is unknown. Three conditions define them. **Both need the full state** $(\theta, \dot\theta)$: configuration alone is not enough, because $c$ depends on $\dot\theta$. **Forward dynamics** takes $\tau$ and returns $\ddot\theta$ by solving a linear system in $M$, which always has a solution because $M$ is positive definite (§2). **Inverse dynamics** takes a desired $\ddot\theta$ and returns $\tau$ with no solve at all; the recursive Newton–Euler algorithm (MR §8.3) computes it in one outward and one inward sweep over the links, hence in $O(n)$.
>
> $$\text{forward: } \ddot\theta = M(\theta)^{-1}\bigl(\tau - c(\theta, \dot\theta) - g(\theta)\bigr), \qquad \text{inverse: } \tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$
>
> where the two lines are one equation solved for different unknowns, so at a fixed state each undoes the other.
>
> - **Example**: P2 at the catalog pose with $\dot\theta = (1, -1)$. Inverse dynamics for $\ddot\theta = (1, 0)$ gives $\tau = (3, 1) + (1, 1) + (19.62, 0) = (23.62,\ 2)\,\mathrm{N\,m}$, and forward dynamics of that $\tau$ returns $(1, 0)$.
> - **Non-example**: the static torque $g(\theta)$, which is inverse dynamics evaluated at $\dot\theta = \ddot\theta = 0$ and nothing more. For the request above it answers $(19.62,\ 0)$ and misses $4$ and $2\,\mathrm{N\,m}$: a feedforward that leaves out $M\ddot\theta$ and $c$ hands exactly that much to the feedback gains.

**Two derivations, one answer.** The **Lagrangian** route is energy-based — write $\mathcal{K}$ and $U$, differentiate, and the three terms fall out, which is exactly what the worked case did. The **recursive Newton–Euler** route is force-balance — sweep outward for velocities and accelerations, inward for forces — and it costs $O(n)$ instead of forming $M$ explicitly, which is why it is what simulators and controllers actually run. They agree on every number, and Step 6's state shows it. Outward: both masses accelerate at $(-1, 0)\,\mathrm{m/s^2}$. Inward: the forearm must push the tip mass with $m_2(a_2 + 9.81\,\hat y) = (-1,\ 9.81)\,\mathrm{N}$, whose moment about the elbow, $1\,\mathrm{m}$ below the mass, is $\tau_2 = 1\,\mathrm{N{\cdot}m}$; about the shoulder the tip mass costs $9.81 + 1 = 10.81$ and the elbow mass $9.81$ (its sideways $1\,\mathrm{N}$ passes through the axis), so $\tau_1 = 20.62\,\mathrm{N{\cdot}m}$. That is Step 6's $(20.62,\ 1)$ without forming $M$ or a single Christoffel symbol; the two routes differ only in what they are convenient for.

The task-space version expresses the same structure at the end-effector — the bridge to operational-space control ([[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §6]]) and impedance control ([[04-robotics/force-compliance-control|Force & Compliance Control §2]]).

**Wiki connections**: sim-to-real gaps live in the mismatch of this equation's parameters;
[[01-canonical-papers/notes/5-world-models/dreamer|world models]] *learn* an implicit version of it;
[[04-robotics/convex-mpc-legged|convex MPC]] deliberately simplifies it (single rigid body)
to buy solvability.

### Self-check

1. Explain why the mass matrix $M(\theta)$ depends on configuration, using an extended versus a folded arm.
2. Which of forward and inverse dynamics does a simulator integrate, and which does a controller feed forward?
3. Why is the Coriolis term $c(\theta,\dot\theta)$ quadratic in velocity?
4. P2 is at the catalog pose with $\dot\theta = (2, 0)\,\mathrm{rad/s}$ — shoulder turning, elbow held. What is $c$, and which joint has to supply it?

> [!tip]- Answers
> 1. Rotational inertia depends on how far mass sits from the axis. Extended, the distal links are far out and the same joint acceleration needs much more torque; folded, they are close and it needs less. Inertia is a function of geometry, and geometry is $\theta$. On P2 that is $M_{11} = 3 + 2\cos\theta_2$, which runs from $5$ down to $1\ \mathrm{kg\,m^2}$ as the elbow closes.
> 2. Simulator = forward dynamics ($\tau \to \ddot\theta$), integrated each step; controller feedforward = inverse dynamics ($\ddot\theta \to \tau$).
> 3. Substituting the kinetic energy $\tfrac12\dot\theta^\top M(\theta)\dot\theta$ into the Lagrange equation differentiates $M$ with respect to $\theta$, and the chain rule turns $\partial M/\partial\theta$ into products $\dot\theta_i\dot\theta_j$ — velocity times velocity.
> 4. With $\dot\theta_2 = 0$ the first component is $-\sin\theta_2\cdot 0\cdot(\ldots) = 0$, and the second is $\sin 90^\circ\,\dot\theta_1^2 = 4\,\mathrm{N\,m}$. So $c = (0,\ 4)$: the **elbow** must supply it, even though the elbow is not moving. That is the centripetal term — holding the forearm at a fixed angle while the shoulder swings it round takes torque, and it grows with the square of the shoulder rate.

### Problem set · 과제

Tier B. Same plant **P2** from [[02-foundations/lab-plants|0.6]], same masses, same vertical plane — but the shoulder is raised: the pose is now $\theta = (30^\circ, 60^\circ)$, link 1 at $30^\circ$ and the forearm pointing straight up again, since $\theta_1 + \theta_2 = 90^\circ$. The elbow is at $(0.866,\ 0.5)$ and the tip at $(0.866,\ 1.5)$. Derive every number from the formulas of the worked case; $\Lambda$ is [[02-foundations/manipulator-kinematics-dynamics|10]]'s lab, not this page's.

1. **Draw.** The picture above with $\theta = (30^\circ, 60^\circ)$ as the main copy and the catalog pose as the light second copy: both masses, both weight arrows, and the horizontal moment arms from the shoulder and from the elbow. Mark on the figure which of the three terms of $\tau = M\ddot\theta + c + g$ each pose makes larger.
2. **Derive.** (a) $M$ at this pose from $M(\theta_2)$, with $\det M$, $M^{-1}$ and its two eigenvalues. (b) $g$ at this pose, and why the elbow again holds nothing. (c) $c$ for $\dot\theta = (1,-1)$. (d) At rest, command $\tau = g + (1, 0)\,\mathrm{N\,m}$ — gravity compensation plus one newton-metre at the shoulder only — and give $\ddot\theta$.
3. **Interpret.** The same extra $(1,0)\,\mathrm{N\,m}$ gives $\ddot\theta = (0.5, -0.5)$ at the catalog pose and $(1, -2)$ at the straight pose of the picture. Place (d) between them: as the elbow opens, which grows faster, the shoulder's response or the elbow's parasitic acceleration, and why can one fixed pair of joint gains not be right at all three poses? And why did $g_2$ stay zero although the pose changed?

> [!note]- How to draw it · 그리는 법
> - Both poses on the same axes, the main one solid and the other light, with the shoulder axis at the origin and gravity along $-\hat y$.
> - A filled circle at each point mass, at the distal end of each link, and a $9.81\,\mathrm{N}$ weight arrow straight down from each: two masses, two arrows, the same length.
> - From the shoulder axis, a dashed horizontal to each mass, labelled with its length; from the elbow axis, one to mass 2. Those lengths are the whole gravity calculation.
> - Check each moment arm: it is the horizontal distance from the axis to the mass, not a link length. A mass directly above an axis has arm $0$ about it — at $(30^\circ, 60^\circ)$ the forearm is vertical again, so the tip mass sits over the elbow and both shoulder arms are $\cos30^\circ = 0.866\,\mathrm{m}$, against $1\,\mathrm{m}$ at the catalog pose.
> - Two curved torque arrows, $\tau_1$ at the base and $\tau_2$ at the elbow.
> - Beside the figure, write $\tau = M(\theta)\ddot\theta + c(\theta,\dot\theta) + g(\theta)$ and circle the terms that survive with the arm at rest; on a second line, circle those that survive when it moves through the same pose. The difference between the two circlings is what this chapter is for.

> [!tip]- Solutions
> 1. At $(30^\circ, 60^\circ)$ both masses sit $0.866\,\mathrm{m}$ right of the shoulder axis and the tip mass sits over the elbow, so both shoulder arms are $0.866$ against the catalog pose's $1$ and $1\,\mathrm{m}$, and the elbow arm is $0$ in both. The catalog pose therefore makes $g$ larger ($19.62$ against $16.99\,\mathrm{N\,m}$) and $c$ larger (it scales with $\sin\theta_2$: $1$ against $0.866$); $(30^\circ, 60^\circ)$ makes $M$ larger ($M_{11} = 4$ against $3$) and more uneven.
> 2. (a) $\cos60^\circ = 0.5$, so $M = \begin{pmatrix}4&1.5\\1.5&1\end{pmatrix}$, $\det M = 4 - 2.25 = 1.75$, $M^{-1} = \frac{1}{1.75}\begin{pmatrix}1&-1.5\\-1.5&4\end{pmatrix} = \begin{pmatrix}0.571&-0.857\\-0.857&2.286\end{pmatrix}$, eigenvalues $(5 \pm \sqrt{25 - 7})/2 = 4.621$ and $0.379\ \mathrm{kg\,m^2}$, a ratio of $12.2$ — between the catalog pose's $5.83$ and the straight pose's $34.0$. (b) $g = \bigl(9.81(2\cos30^\circ + \cos90^\circ),\ 9.81\cos90^\circ\bigr) = (9.81\times1.732,\ 0) = (16.99,\ 0)\,\mathrm{N\,m}$. The elbow holds nothing again because $g_2$ depends on $\theta_1 + \theta_2$, the forearm's absolute angle, which is $90^\circ$ here as at the catalog pose; $M$ depends on $\theta_2$ alone, which did change. (c) $c = \bigl(-\sin60^\circ\cdot(-1)(2 - 1),\ \sin60^\circ\cdot1^2\bigr) = (0.866,\ 0.866)\,\mathrm{N\,m}$, $0.866$ of the catalog pose's $(1, 1)$. (d) $\ddot\theta = M^{-1}(1, 0)^\top = (0.571,\ -0.857)\,\mathrm{rad/s^2}$.
> 3. As the elbow opens from $90^\circ$ through $60^\circ$ to $0^\circ$, the shoulder's response grows $0.5 \to 0.571 \to 1$, twice over the whole range, while the elbow's parasitic acceleration grows $-0.5 \to -0.857 \to -2$, four times: the coupling changes faster. A fixed gain pair is tuned for one inertia and meets another, so the same commanded torque produces a different shoulder response and a different unrequested elbow motion at each pose — the argument for multiplying by $M(\theta)$ instead of hoping, and the reason [[04-robotics/modern-robotics/ch11-robot-control|ch.11]] opens with computed torque. $g_2$ stayed zero because gravity on the elbow depends only on the forearm's absolute angle, and raising the shoulder by $30^\circ$ while closing the elbow by $30^\circ$ left the forearm upright.

## 한국어

**핵심 질문**: 어떤 토크가 어떤 가속도를 만드는가?

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 장은 조작 층의 운동 방정식이고, [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학]]이 깐 수학 바닥 위에 선다. "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계, 곧 팔을 붙들고 이동 내내 끌고 가는 데 드는 토크를 받친다. 이 페이지의 칩은 [[physical-ai-map|피지컬 AI 지도]]의 조작 띠에 있다. 멈춘 팔에서 조율한 제어기가 가장 먼저 만나는 차이가 여기 있다. 카탈로그의 평면 2링크 팔 **P2**([[02-foundations/lab-plants|0.6]])는 카탈로그 자세를 $g = (19.62,\ 0)\,\mathrm{N{\cdot}m}$로 버티지만, $\dot\theta = (1,-1)\,\mathrm{rad/s}$로 그 자세를 지나갈 때 같은 명령을 주면 엘보가 $1\,\mathrm{rad/s^2}$로 가속하고, 속도를 유지하려면 관절마다 $1\,\mathrm{N{\cdot}m}$가 더 든다. 정지 상태에서는 아무것도 지지 않던 엘보에도 든다(5–6단계). 뒤 페이지들이 절 단위로 이것을 쓴다. [[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장 §2]]는 이것으로 가속도가 튀면 토크가 튀는 이유를 말하고, [[04-robotics/modern-robotics/ch11-robot-control|MR 11장 §2]]는 이것을 계산 토크로 피드포워드하며, [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §4]]는 기어 달린 회전자의 관성을 $M$에 더하고, [[04-robotics/system-identification|5.5 시스템 식별 §9]]는 그 파라미터를 토크에서 맞추며, [[04-robotics/capstone-panel-contact|26. 캡스톤]]은 이것을 루프 안에서 돌린다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 2, 로보틱스 19–21회차다. 이 페이지를 마치면 P2의 $M$, $c$, $g$를 에너지에서 유도하고, 어떤 상태에서든 방정식을 양방향으로 읽고, 시뮬레이터나 제어기가 빠뜨린 항을 짚을 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 세 번쯤, 로보틱스 19–21회차다. **첫 회차:** 이 페이지의 대상, 그림, '대상으로 한 번 끝까지'의 1–4단계. 운동 에너지에서 $M$을, 퍼텐셜에서 $g$를, $M$의 변화에서 $c$를 읽는데, 같은 세 항을 야코비안 경로로 만났던 [[02-foundations/manipulator-kinematics-dynamics|10. §3–§5]]와 줄마다 견준다. 이어서 정지한 팔인 7단계. 끝으로 정지 상태를 손으로 확인한다. 카탈로그 자세의 $\tau = g(\theta)$, 그리고 그 토크를 넣은 순동역학이 팔을 그대로 붙잡아 두는지. **둘째 회차:** 움직이는 한 상태를 양방향으로 읽는 5–6단계와 6단계를 힘으로 그린 그림, 이어서 §1–§3. **셋째 회차:** 스스로 점검과 과제.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그의 평면 2링크 팔에 질량 성질을 켠 것이다. 단위 링크 $L_1 = L_2 = 1\,\mathrm{m}$, 각 링크 말단에 점질량 $m_1 = m_2 = 1\,\mathrm{kg}$, 그리고 이 장은 무게가 필요하므로 팔을 연직 평면에 세우고 $g = 9.81\,\mathrm{m/s^2}$가 $-\hat y$로 작용한다. 카탈로그가 고정한 자세는 $\theta = (0^\circ, 90^\circ)$ — 엘보 $(1,0)$, 전완은 곧장 위, 말단 $(1,1)$ — 이고 거기서 질량 행렬은 $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$이다.

위키의 다른 곳은 이 행렬을 인용한다. 이 페이지에서는 그것을 *유도*하고, 운동 방정식의 나머지 두 항도 함께 유도한다.

*범위: 이 페이지는 관절 공간 운동 방정식을 가르친다. $M$, $c$, $g$가 어디서 오는지, P2에서 각각 무슨 일을 하는지, 그리고 이 방정식을 읽는 두 방향이다. 작업 공간 형태나 $O(n)$ 재귀 구현은 가르치지 않고, 카탈로그의 $\Lambda = \mathrm{diag}(1,2)$도 다시 구하지 않는다. 그것들은 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §6]]에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 390" style="max-width:100%;height:auto" role="img" aria-label="연직 평면에 선 P2: 카탈로그 자세 (0°, 90°)와 얇게 그린 곧게 편 자세 (0°, 0°), 점질량, 같은 9.81 N 무게, 어깨 모멘트 팔 1 m·1 m 대 1 m·2 m, 그리고 정지와 움직임에서 동그라미 친 운동 방정식">
  <defs><marker id="ar8k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="ar8kL" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="0.9" stroke-dasharray="6 3 1.5 3" opacity="0.5"><line x1="62" y1="27.8" x2="62" y2="149.4"/><line x1="62" y1="183.6" x2="62" y2="245"/></g>
  <polygon points="62,160 52,175 72,175" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.6"><line x1="50" y1="180" x2="54" y2="175"/><line x1="55" y1="180" x2="59" y2="175"/><line x1="60" y1="180" x2="64" y2="175"/><line x1="65" y1="180" x2="69" y2="175"/><line x1="70" y1="180" x2="74" y2="175"/></g>
  <line x1="180" y1="160" x2="298" y2="160" stroke="currentColor" stroke-width="7" stroke-opacity="0.2" stroke-dasharray="10 5"/>
  <g stroke="currentColor" stroke-width="7" stroke-opacity="0.42" stroke-linecap="round" fill="none"><line x1="62" y1="160" x2="180" y2="160"/><line x1="180" y1="160" x2="180" y2="42"/></g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.9"><line x1="62" y1="42" x2="180" y2="42" stroke-dasharray="4 3"/><line x1="62" y1="38" x2="62" y2="46"/><line x1="180" y1="38" x2="180" y2="46"/></g>
  <text x="121" y="37" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.9">1 m</text>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.9"><line x1="62" y1="186" x2="180" y2="186" stroke-dasharray="4 3"/><line x1="62" y1="182" x2="62" y2="190"/><line x1="180" y1="182" x2="180" y2="190"/></g>
  <text x="121" y="181" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.9">1 m</text>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.55"><line x1="62" y1="235.5" x2="298" y2="235.5" stroke-dasharray="4 3"/><line x1="62" y1="231.5" x2="62" y2="239.5"/><line x1="298" y1="231.5" x2="298" y2="239.5"/></g>
  <text x="239" y="230.5" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.55">2 m</text>
  <line x1="298" y1="219" x2="298" y2="240.2" stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 2.5" opacity="0.55"/>
  <g stroke="currentColor" stroke-width="1.8" marker-end="url(#ar8k)"><line x1="180" y1="167" x2="180" y2="219"/><line x1="180" y1="49" x2="180" y2="101"/></g>
  <g stroke="currentColor" stroke-width="1.6" opacity="0.5" marker-end="url(#ar8kL)"><line x1="298" y1="166" x2="298" y2="219"/></g>
  <circle cx="62" cy="160" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="180" cy="160" r="7" fill="currentColor"/>
  <circle cx="180" cy="42" r="7" fill="currentColor"/>
  <circle cx="298" cy="160" r="6" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6"/>
  <path d="M86.1 150.3 L85 147.9 L83.7 145.7 L82.2 143.6 L80.5 141.7 L78.6 140 L76.5 138.4 L74.3 137.1 L72 136 L69.6 135.1 L67.1 134.5 L64.6 134.1 L62 134 L59.4 134.1 L56.9 134.5 L54.4 135.1 L52 136 L49.7 137.1 L47.5 138.4 L45.4 140 L43.5 141.7 L41.8 143.6 L40.3 145.7 L39 147.9 L37.9 150.3" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#ar8k)"/>
  <path d="M203.3 154.2 L203 153.2 L202.7 152.1 L202.3 151.1 L201.9 150.1 L201.4 149.1 L200.9 148.2 L200.3 147.3 L199.7 146.3 L199.1 145.5 L198.4 144.6 L197.7 143.8 L197 143 L196.2 142.3 L195.4 141.6 L194.5 140.9 L193.7 140.3 L192.7 139.7 L191.8 139.1 L190.9 138.6 L189.9 138.1 L188.9 137.7 L187.9 137.3 L186.8 137 L185.8 136.7" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#ar8k)"/>
  <g fill="currentColor">
  <text x="30.1" y="139.9" font-size="12" text-anchor="middle">τ<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="214.2" y="136.4" font-size="12" text-anchor="middle">τ<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="168" y="34" font-size="11" text-anchor="end">m<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="190" y="180" font-size="11">m<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="189" y="75" font-size="11">9.81 N</text>
  <text x="187" y="209.6" font-size="11">9.81 N</text>
  <text x="290.9" y="29.5" font-size="11" text-anchor="end">g = 9.81 m/s²</text>
  <text x="171.7" y="110.4" font-size="11" text-anchor="end">엘보에서의 팔: 0</text>
  <text x="192" y="46" font-size="11">(0°, 90°)</text>
  </g>
  <text x="305" y="209.6" font-size="11" fill="currentColor" opacity="0.6">9.81 N</text>
  <text x="255.5" y="150.6" font-size="11" text-anchor="middle" fill="currentColor" opacity="0.6">(0°, 0°)</text>
  <line x1="300.4" y1="12.4" x2="300.4" y2="36.4" stroke="currentColor" stroke-width="1.4" marker-end="url(#ar8k)"/>
  <g fill="currentColor">
  <text x="352" y="26" font-size="11.5" font-weight="bold">카탈로그 θ = (0°, 90°) · 실선</text>
  <text x="352" y="52" font-size="11">M =</text>
  </g>
  <g fill="currentColor">
  <path d="M384 36 L380 36 L380 66 L384 66" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M416 36 L420 36 L420 66 L416 66" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="392" y="47" font-size="11" text-anchor="middle">3</text>
  <text x="408" y="47" font-size="11" text-anchor="middle">1</text>
  <text x="392" y="61" font-size="11" text-anchor="middle">1</text>
  <text x="408" y="61" font-size="11" text-anchor="middle">1</text>
  </g>
  <g fill="currentColor">
  <text x="426" y="52" font-size="11">kg·m²</text>
  <text x="352" y="86" font-size="11">g = (19.62, 0) N·m</text>
  <text x="352" y="103" font-size="11">어깨에서의 팔: 1 m, 1 m</text>
  </g>
  <g fill="currentColor" opacity="0.62">
  <text x="352" y="142" font-size="11.5" font-weight="bold">곧게 편 θ = (0°, 0°) · 얇게</text>
  <text x="352" y="168" font-size="11">M =</text>
  <path d="M384 152 L380 152 L380 182 L384 182" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M416 152 L420 152 L420 182 L416 182" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="392" y="163" font-size="11" text-anchor="middle">5</text>
  <text x="408" y="163" font-size="11" text-anchor="middle">2</text>
  <text x="392" y="177" font-size="11" text-anchor="middle">2</text>
  <text x="408" y="177" font-size="11" text-anchor="middle">1</text>
  <text x="426" y="168" font-size="11">kg·m²</text>
  <text x="352" y="202" font-size="11">g = (29.43, 9.81) N·m</text>
  <text x="352" y="219" font-size="11">어깨에서의 팔: 1 m, 2 m</text>
  </g>
  <g fill="currentColor">
  <text x="14" y="276" font-size="11" font-weight="bold">정지 유지</text>
  <text x="14" y="291" font-size="11">θ̇ = 0</text>
  <text x="14" y="305" font-size="11">θ̈ = 0</text>
  <text x="200" y="284" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="284" font-size="12.5" text-anchor="end">M(θ)θ̈</text>
  <text x="287" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="284" font-size="12.5" text-anchor="end">c(θ, θ̇)</text>
  <text x="372" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="405" y="284" font-size="12.5" text-anchor="middle">g(θ)</text>
  <text x="434" y="284" font-size="12">= (19.62, 0) N·m</text>
  </g>
  <ellipse cx="405" cy="280" rx="19" ry="12" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g fill="currentColor">
  <text x="14" y="324" font-size="11" font-weight="bold">지나가며 움직임</text>
  <text x="14" y="339" font-size="11">θ̇ = (1, −1) rad/s</text>
  <text x="14" y="353" font-size="11">θ̈ = 0</text>
  <text x="200" y="332" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="332" font-size="12.5" text-anchor="end">M(θ)θ̈</text>
  <text x="287" y="332" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="332" font-size="12.5" text-anchor="end">c(θ, θ̇)</text>
  <text x="372" y="332" font-size="12.5" text-anchor="middle">+</text>
  <text x="405" y="332" font-size="12.5" text-anchor="middle">g(θ)</text>
  <text x="434" y="332" font-size="12">= (20.62, 1) N·m</text>
  </g>
  <ellipse cx="330" cy="328" rx="31" ry="12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 2.5"/>
  <ellipse cx="405" cy="328" rx="22" ry="13" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 2.5"/>
  <text x="14" y="376" font-size="11" fill="currentColor" opacity="0.85">움직이는 줄에만 c에 동그라미가 있다: c = (1, 1) N·m, 관절마다 1 N·m씩 더</text>
</svg>

연직 평면의 장치 **P2**, 실선은 카탈로그 자세 $(0^\circ, 90^\circ)$, 얇은 선은 곧게 편 자세 $(0^\circ, 0^\circ)$이고, 각 링크 끝에 $1\,\mathrm{kg}$ 점질량과 $9.81\,\mathrm{N}$ 무게가 있다. 어깨에서의 수평 모멘트 팔은 카탈로그 자세에서 $1$과 $1\,\mathrm{m}$(엘보에서는 $0$), 곧게 펴면 $1$과 $2\,\mathrm{m}$이므로 $g$는 $(19.62,\ 0)$에서 $(29.43,\ 9.81)\,\mathrm{N\,m}$로, $M$은 $\begin{pmatrix}3&1\\1&1\end{pmatrix}$에서 $\begin{pmatrix}5&2\\2&1\end{pmatrix}\,\mathrm{kg\,m^2}$로 커진다. 카탈로그 자세에서 정지해 버티는 데는 $g$만, 곧 $\tau = (19.62,\ 0)\,\mathrm{N\,m}$가 들고, $\dot\theta = (1,-1)\,\mathrm{rad/s}$로 지나가며 움직이면 $c = (1,1)$이 더해져 $\tau = (20.62,\ 1)\,\mathrm{N\,m}$가 된다.

### 대상으로 한 번 끝까지 · Worked case

10번 페이지가 이 자세에서 세 항을 이미 만들었다. $M$은 [[02-foundations/manipulator-kinematics-dynamics|10. §3]]에서 야코비안 경로로, 속도 항은 §4에서 크리스토펠 공식으로, $g$는 §5에서 자유물체도 검산과 함께. 1–4단계는 대신 MR의 에너지 경로로, 두 에너지만으로 세 항에 이른다. 줄마다 10과 견주어라. 먼저 기호 대응 하나. 두 페이지가 글자를 다르게 쓰기 때문이다. 이 페이지의 벡터 $c(\theta, \dot\theta)$는 10의 곱 $C(\theta,\dot\theta)\,\dot\theta$이고(곱만 유일하다, 10 §2), 이 페이지의 $\Gamma_{ijk}$는 10의 $c_{ijk}$이며(여기서는 글자 $c$를 벡터가 쓴다), 이 페이지의 $\mathcal{K}$와 $U$는 10의 $T$와 $V$다. 각 단계가 적용하는 방정식은 하나, [[02-foundations/manipulator-kinematics-dynamics|10. §2]]에서 질량 하나로 뉴턴 제2법칙과 견주어 확인한 라그랑주 방정식이다:

$$\frac{d}{dt}\frac{\partial\mathcal{K}}{\partial\dot\theta_i} - \frac{\partial\mathcal{K}}{\partial\theta_i} + \frac{\partial U}{\partial\theta_i} = \tau_i, \qquad i = 1, 2$$

여기서 $\mathcal{K}$는 운동 에너지, $U$는 퍼텐셜 에너지다. 그래서 1–2단계는 $\mathcal{K}$를 만들고, 3단계는 $U$를 미분하고, 4단계는 $\mathcal{K}$를 미분하고 남는 것을 모은다.

**1단계 — 운동 에너지를 펼쳐 쓴다.** $c_1 = \cos\theta_1$, $s_1 = \sin\theta_1$, $c_{12} = \cos(\theta_1{+}\theta_2)$, $s_{12} = \sin(\theta_1{+}\theta_2)$로 쓰자. 질량 1은 $(L_1c_1,\ L_1s_1)$에, 질량 2는 말단 $(L_1c_1 + L_2c_{12},\ L_1s_1 + L_2s_{12})$에 있으므로 시간으로 미분하면

$$v_1 = L_1\dot\theta_1\,(-s_1,\ c_1), \qquad v_2 = L_1\dot\theta_1\,(-s_1,\ c_1) + L_2(\dot\theta_1{+}\dot\theta_2)\,(-s_{12},\ c_{12})$$

이다. 10 §3의 $J_1\dot\theta$와 $J_2\dot\theta$다. 이것을 제곱하면

$$|v_1|^2 = L_1^2\dot\theta_1^2, \qquad |v_2|^2 = L_1^2\dot\theta_1^2 + L_2^2(\dot\theta_1{+}\dot\theta_2)^2 + 2L_1L_2\,\dot\theta_1(\dot\theta_1{+}\dot\theta_2)\cos\theta_2$$

가 된다. 두 링크 속도의 교차항이 $c_1c_{12} + s_1s_{12} = \cos\theta_2$를 남기기 때문이다. *상대* 엘보 각이고, 그 외에는 아무것도 아니다. 카탈로그의 단위 링크와 단위 질량을 넣으면 $2\mathcal{K} = |v_1|^2 + |v_2|^2$가

$$2\mathcal{K} = (3 + 2\cos\theta_2)\,\dot\theta_1^2 + 2(1 + \cos\theta_2)\,\dot\theta_1\dot\theta_2 + \dot\theta_2^2$$

으로 모인다.

**2단계 — 이차형식에서 $M$을 읽는다.** $2\mathcal{K} = \dot\theta^\top M\dot\theta$(질량 행렬을 정의하는 이차형식, §2)와 항별로 맞추면 $\dot\theta_1^2$의 계수가 $M_{11}$, $\dot\theta_2^2$의 계수가 $M_{22}$, $\dot\theta_1\dot\theta_2$의 계수는 대칭성이 두 비대각 성분에 나누어 주므로 $2M_{12}$다:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

여기에 $\theta_2$만 나온다. 어깨 둘레로 팔 전체를 돌리는 것은 질량이 각 축에 대해 어떻게 분포하는지를 바꿀 수 없기 때문이다. 카탈로그 자세에서는 $\cos\theta_2 = 0$이므로 $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ — 이제 인용이 아니라 유도해 얻은 카탈로그 행렬이고, 10 §3의 것과 같다. 고윳값은 $2 \pm \sqrt2 = 3.4142$와 $0.5858\ \mathrm{kg\,m^2}$로 둘 다 양수이고, 그 비 $5.83$이 이 팔의 가장 무거운 방향이 가장 가벼운 방향보다 몇 배 무거운지를 말한다. $\theta_2 = 0$으로 곧게 펴면 $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$이고 고윳값은 $3 \pm 2\sqrt2 = 5.8284$와 $0.1716$, 비가 $34.0$이다. 팔을 뻗으면 그냥 무거워지는 것이 아니라 훨씬 더 *고르지 않게* 무거워진다.

**3단계 — 중력을 퍼텐셜에서.** 퍼텐셜 에너지는 $U = g(m_1y_1 + m_2y_2) = g\,(2\sin\theta_1 + \sin(\theta_1{+}\theta_2))$이고(카탈로그 숫자), 중력 벡터는 그 기울기, 곧 라그랑주 방정식의 $\partial U/\partial\theta$ 항이다:

$$g(\theta) = \frac{\partial U}{\partial \theta} = \bigl(\,g(2\cos\theta_1 + \cos(\theta_1{+}\theta_2)),\ \ g\cos(\theta_1{+}\theta_2)\,\bigr)$$

각 코사인이 그림에서 바로 읽히는 수평 모멘트 팔이다. 카탈로그 자세에서는 $\cos\theta_1 = 1$, $\cos(\theta_1{+}\theta_2) = 0$이므로 $g = (19.62,\ 0)\,\mathrm{N\,m}$이다. 어깨는 두 질량을 $1\,\mathrm{m}$에서 들고, 엘보는 질량이 바로 위에 있어 아무것도 들지 않는다. 10 §5의 자유물체도 검산, [[02-foundations/basic-mechanics|0.6.1 §8]]의 유지 토크와 같은 숫자다. 곧게 편 자세에서는 같은 식이 $(29.43,\ 9.81)$을 준다. 어깨 쪽이 절반만큼 더 든다.

**4단계 — 코리올리를 $M$의 변화에서.** 속도 곱 항은 라그랑주 방정식 안에서 $M(\theta)$를 미분할 때 나온다. [[02-foundations/manipulator-kinematics-dynamics|10. §4]]의 크리스토펠 기호 $\Gamma_{ijk} = \tfrac12(\partial M_{ij}/\partial\theta_k + \partial M_{ik}/\partial\theta_j - \partial M_{jk}/\partial\theta_i)$(10에서는 $c_{ijk}$이고, 10은 대입하면 같은 벡터가 나온다고 말만 한다)로 모으고 $c_i = \sum_{j,k}\Gamma_{ijk}\dot\theta_j\dot\theta_k$를 쓰면, $\partial M/\partial\theta_2 \propto \sin\theta_2$만 살아남는다. 구체적으로 0이 아닌 도함수는 $\partial M_{11}/\partial\theta_2 = -2\sin\theta_2$와 $\partial M_{12}/\partial\theta_2 = \partial M_{21}/\partial\theta_2 = -\sin\theta_2$뿐이다. $\theta_1$에 의존하는 것이 없고 $M_{22}$는 상수이기 때문이다. 그래서 예를 들어 $\Gamma_{122} = \tfrac12(\partial M_{12}/\partial\theta_2 + \partial M_{12}/\partial\theta_2 - \partial M_{22}/\partial\theta_1) = -\sin\theta_2$, $\Gamma_{212} = \tfrac12(\partial M_{21}/\partial\theta_2 + \partial M_{22}/\partial\theta_1 - \partial M_{12}/\partial\theta_2) = 0$이고, 여덟 기호 전부는

$$\Gamma_{112} = \Gamma_{121} = \Gamma_{122} = -\sin\theta_2, \qquad \Gamma_{211} = \sin\theta_2, \qquad \Gamma_{111} = \Gamma_{212} = \Gamma_{221} = \Gamma_{222} = 0$$

이다. 따라서 $c_1 = \Gamma_{112}\dot\theta_1\dot\theta_2 + \Gamma_{121}\dot\theta_2\dot\theta_1 + \Gamma_{122}\dot\theta_2^2$, $c_2 = \Gamma_{211}\dot\theta_1^2$이고, 곧

$$c(\theta, \dot\theta) = \bigl(\,-\sin\theta_2\,\dot\theta_2(2\dot\theta_1 + \dot\theta_2),\ \ \sin\theta_2\,\dot\theta_1^2\,\bigr)$$

가 된다. $\dot\theta$의 이차식이고 $\sin\theta_2$에 비례하며, $h = -\sin\theta_2$로 둔 10 §4의 벡터와 같다. 곧바로 따라 나오는 결론이 둘이고 아래에서 둘 다 쓴다. 팔이 멈춰 있으면 $c$는 항등적으로 0이다. 그리고 $\theta_2 = 0$이나 $180^\circ$에서는 **속도가 무엇이든** 항등적으로 0이다. 곧게 펴거나 접은 엘보가 바로 $M$이 순간적으로 변하기를 멈추는 자리이기 때문이다. 카탈로그 자세 $\theta_2 = 90^\circ$는 정반대 극단인 $|\sin\theta_2| = 1$로, 이 팔이 가질 수 있는 가장 강하게 속도 결합된 자세다.

**5단계 — 수치 한 건을 끝까지.** P2를 카탈로그 자세에 두고 *움직이게* 한다. $\dot\theta = (1, -1)\,\mathrm{rad/s}$, 어깨는 열리고 엘보는 펴진다. 명령은 정확히 중력 토크 $\tau = g = (19.62,\ 0)$, 순진한 "중력 보상" 제어기가 하는 일 그대로다.

- 코리올리·원심: $c_1 = -1\cdot(-1)\bigl(2(1) + (-1)\bigr) = 1$, $c_2 = 1\cdot(1)^2 = 1$이므로 $c = (1,\ 1)\,\mathrm{N\,m}$.
- 남는 토크: $\tau - c - g = (19.62, 0) - (1,1) - (19.62, 0) = (-1,\ -1)\,\mathrm{N\,m}$.
- 역질량 행렬: $\det M = 3 - 1 = 2$이므로 $M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}$.
- 순동역학(운동 방정식을 $\ddot\theta$에 대해 푼 것, §3): $\ddot\theta = M^{-1}(\tau - c - g) = (0,\ -1)\,\mathrm{rad/s^2}$.

즉 *움직이는* 팔에서 중력만 상쇄하면 어깨 가속도는 정확히 0이고 엘보는 $1\,\mathrm{rad/s^2}$로 더 빨리 펴진다. 이것은 전부 속도 항 $c$ — §1에서 가르는 코리올리 몫 $(2, 0)$과 원심 몫 $(-1, 1)$ — 에서 나온다. 정지 상태였다면 같은 명령이 $\ddot\theta = 0$을 내고 아무 일도 일어나지 않았을 것이기 때문이다. 멈춰 있는 팔에서 조율한 제어기를 움직이는 팔에 올리면 가장 먼저 만나는 차이가 이것이다.

**6단계 — 같은 줄을 반대로 읽는다.** 같은 상태에서 이번에는 $\ddot\theta = 0$을 요구한다. 속도를 유지한 채 그 자세를 지나가라는 뜻이다. 역동역학(같은 방정식을 $\tau$에 대해 계산한 것, §3)은 $\tau = c + g = (20.62,\ 1)\,\mathrm{N\,m}$을 준다. 정지 유지보다 *각* 관절에 $1\,\mathrm{N\,m}$씩 더 드는데, 정역학적으로는 아무것도 필요 없던 엘보에도 든다. 부하가 없던 관절의 토크는 어디서 오는가? $\dot\theta = (1,-1)$이면 $\dot\theta_1 + \dot\theta_2 = 0$이라 전완이 돌지 않는다. 엘보가 전완을 어깨 둘레로 실어 나를 뿐이다. 그래서 두 질량 모두 $1\,\mathrm{m/s}$로 위로 움직이고, $1\,\mathrm{rad/s}$로 원을 돌므로 두 질량 모두 제 원의 중심 쪽으로 $(-1, 0)\,\mathrm{m/s^2}$로 가속한다. 말단 질량의 경로를 꺾으려면 전완이 그 무게를 드는 $9.81\,\mathrm{N}$에 더해 옆으로 $1\,\mathrm{N}$을 당겨야 하고, 그 $1\,\mathrm{N}$은 두 관절 축보다 $1\,\mathrm{m}$ 위에 작용한다. 그래서 $c = (1, 1)$이다. 엘보 질량이 받는 옆 방향 $1\,\mathrm{N}$은 링크 1을 따라 어깨 축을 지나므로 아무것도 더하지 않는다. 이 속도 결합이 [[04-robotics/modern-robotics/ch11-robot-control|11장]]에서 피드포워드 항, 곧 추종 오차가 생기기 전에 모델로 계산해 모터에 미리 보내는 토크가 공급하는 것이다(피드백은 오차가 생긴 뒤에야 반응한다). §3은 같은 훑기를 MR의 뉴턴–오일러로 다시 한다.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="카탈로그 자세에서 θ̇ = (1, −1)로 움직이는 P2: 전완은 돌지 않고 평행이동하므로 두 질량이 모두 위로 1 m/s로 움직이고 (−1, 0) m/s²로 가속한다. 전완은 말단 질량을 옆으로 1 N 당기고, 그 힘이 두 관절 축보다 1 m 위에 작용해 c = (1, 1) N·m, τ = (20.62, 1) N·m가 된다.">
  <defs><marker id="mr08s6k" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="161.7,282.5 162.5,280.7 163.3,279.0 164.0,277.2 164.7,275.4 165.4,273.6 166.0,271.8 166.6,270.0 167.2,268.2 167.7,266.3 168.3,264.5 168.7,262.6 169.2,260.7 169.6,258.9 170.0,257.0 170.3,255.1 170.6,253.2 170.9,251.3 171.2,249.4 171.4,247.5 171.6,245.6 171.7,243.7 171.8,241.8 171.9,239.8 172.0,237.9 172.0,236.0 172.0,234.1 171.9,232.2 171.8,230.2 171.7,228.3 171.6,226.4 171.4,224.5 171.2,222.6 170.9,220.7 170.6,218.8 170.3,216.9 170.0,215.0 169.6,213.1 169.2,211.3 168.7,209.4 168.3,207.5 167.7,205.7 167.2,203.8 166.6,202.0 166.0,200.2 165.4,198.4 164.7,196.6 164.0,194.8 163.3,193.0 162.5,191.3 161.7,189.5 160.9,187.8 160.0,186.1 159.1,184.4 158.2,182.7 157.3,181.0 156.3,179.3 155.3,177.7 154.3,176.1 153.2,174.5 152.1,172.9 151.0,171.3 149.8,169.8 148.7,168.3 147.5,166.8 146.3,165.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.55"/>
  <polyline points="161.7,172.5 162.5,170.7 163.3,169.0 164.0,167.2 164.7,165.4 165.4,163.6 166.0,161.8 166.6,160.0 167.2,158.2 167.7,156.3 168.3,154.5 168.7,152.6 169.2,150.7 169.6,148.9 170.0,147.0 170.3,145.1 170.6,143.2 170.9,141.3 171.2,139.4 171.4,137.5 171.6,135.6 171.7,133.7 171.8,131.8 171.9,129.8 172.0,127.9 172.0,126.0 172.0,124.1 171.9,122.2 171.8,120.2 171.7,118.3 171.6,116.4 171.4,114.5 171.2,112.6 170.9,110.7 170.6,108.8 170.3,106.9 170.0,105.0 169.6,103.1 169.2,101.3 168.7,99.4 168.3,97.5 167.7,95.7 167.2,93.8 166.6,92.0 166.0,90.2 165.4,88.4 164.7,86.6 164.0,84.8 163.3,83.0 162.5,81.3 161.7,79.5 160.9,77.8 160.0,76.1 159.1,74.4 158.2,72.7 157.3,71.0 156.3,69.3 155.3,67.7 154.3,66.1 153.2,64.5 152.1,62.9 151.0,61.3 149.8,59.8 148.7,58.3 147.5,56.8 146.3,55.3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.55"/>
  <polyline points="62.0,236.0 152.1,172.9 152.1,62.9" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" opacity="0.15"/>
  <polyline points="62.0,236.0 172.0,236.0 172.0,126.0" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" opacity="0.42"/>
  <circle cx="62.0" cy="236.0" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="172.0" cy="236.0" r="7" fill="currentColor"/><circle cx="172.0" cy="126.0" r="7" fill="currentColor"/>
  <line x1="184.0" y1="236.0" x2="184.0" y2="181.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr08s6k)"/>
  <line x1="184.0" y1="126.0" x2="184.0" y2="71.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr08s6k)"/>
  <line x1="164.0" y1="126.0" x2="117.0" y2="126.0" stroke="currentColor" stroke-width="2.4" marker-end="url(#mr08s6k)"/>
  <line x1="164.0" y1="249.0" x2="117.0" y2="249.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#mr08s6k)" opacity="0.8"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.8"><line x1="30" y1="236.0" x2="30" y2="126.0"/><line x1="25" y1="236.0" x2="35" y2="236.0"/><line x1="25" y1="126.0" x2="35" y2="126.0"/></g>
  <line x1="35" y1="126.0" x2="111.0" y2="126.0" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.6"/>
  <line x1="30" y1="241.0" x2="30" y2="279.0" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.6"/>
  <g font-size="11" fill="currentColor">
    <text x="24" y="185.0" text-anchor="end">1 m</text>
    <text x="190.0" y="191.0">v</text>
    <text x="190.0" y="81.0">v</text>
    <text x="121.0" y="119.0">a</text>
    <text x="121.0" y="264.0">a</text>
    <text x="144.1" y="48.9" text-anchor="end" opacity="0.6">조금 뒤에도</text>
    <text x="144.1" y="62.9" text-anchor="end" opacity="0.6">전완은 수직</text>
    <text x="8" y="291.0" opacity="0.8">두 관절 축의 높이</text>
  </g>
  <line x1="290" y1="14" x2="290" y2="288" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <g font-size="11" fill="currentColor">
    <text x="300" y="28" font-size="12">6단계를 힘으로 그리면</text>
    <text x="300" y="46" opacity="0.8">θ = (0°, 90°), θ̇ = (1, −1) rad/s, θ̈ = 0</text>
    <text x="300" y="70" opacity="1">전완은 돌지 않는다: θ̇₁ + θ̇₂ = 0</text>
    <text x="300" y="88" opacity="1">두 질량 모두 v = (0, 1) m/s,</text>
    <text x="300" y="106" opacity="1">a = (−1, 0) m/s², 각 원의 중심 쪽</text>
    <text x="300" y="122" opacity="0.75">(점선: 중심 (0, 0)과 (0, 1)인 두 원)</text>
    <text x="300" y="146" opacity="1">전완이 말단 질량을 미는 힘 (−1, 9.81) N:</text>
    <text x="300" y="164" opacity="1">위로 9.81 N은 무게를 든다 → g</text>
    <text x="300" y="182" opacity="1">옆으로 1 N은 경로를 꺾는다 → c</text>
    <text x="300" y="206" opacity="1">그 1 N은 두 관절 축보다 1 m 위:</text>
    <text x="300" y="224" opacity="1">c = (1 · 1, 1 · 1) = (1, 1) N·m</text>
    <text x="300" y="248" opacity="0.85">엘보 질량의 1 N은 어깨 축을 지난다: 0</text>
    <text x="300" y="274" opacity="1" font-size="12">τ = g + c = (20.62, 1) N·m</text>
  </g>
</svg>

6단계를 카탈로그 자세에서 축척대로 힘으로 그렸다. 전완이 돌지 않고 평행이동하므로 두 질량이 모두 $1\,\mathrm{m/s}$로 위로 움직이고 $(-1, 0)\,\mathrm{m/s^2}$로 가속하며(화살표는 단위당 반 미터), 전완이 말단 질량을 미는 힘 $(-1,\ 9.81)\,\mathrm{N}$은 무게를 드는 $9.81\,\mathrm{N}$($g$)과 경로를 꺾는 $1\,\mathrm{N}$($c$)으로 갈린다. 그 $1\,\mathrm{N}$이 두 관절 축보다 $1\,\mathrm{m}$ 위에 작용하므로 $c = (1, 1)\,\mathrm{N{\cdot}m}$, $\tau = g + c = (20.62,\ 1)\,\mathrm{N{\cdot}m}$다.

**7단계 — 정지하면 $g$만 남는다.** $\dot\theta = 0$으로 두면 4단계에 의해 $c = 0$이고 방정식은 $\tau = M\ddot\theta + g$로 줄어든다. 가만히 있으라는 것은 $\ddot\theta = 0$이므로 $\tau = g = (19.62,\ 0)$이다. 이것을 순동역학에 넣으면 $\ddot\theta = M^{-1}(\tau - g) = 0$이라 시뮬레이터의 다음 스텝은 아무것도 하지 않는다. 과제가 다른 자세에서 그리는 상태이고, 이 페이지의 다른 모든 자세를 견주어야 할 기준이다.

### 1. 세 항이 어디서 오는가 — 1링크, 그다음 2링크

진자에는 관성 곱하기 가속도와 중력만 있으면 된다. 링크를 하나 더 붙이면 관성이 자세에 의존하기 시작하고 속도 항이 켜진다. 그것이 "한 방정식"에서 "다링크 동역학이 왜 어려운가"로 가는 도약 전부이고, 이 절은 그 도약이 남기는 세 항에 이름을 붙인다.

**운동 방정식**, 전부가 한 줄에:

$$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$

질량 행렬(자세 의존 관성), 코리올리·원심 항(속도 곱), 중력이다. 셋이 경쟁하지 않고 더해지는 이유는 같은 액추에이터에 걸리는 서로 다른 요구이기 때문이다. $M\ddot\theta$는 속도를 바꾸는 데 드는 토크, $c$는 모양이 변하는 중에 움직이고 있다는 것 자체에 드는 토크, $g$는 그저 중력에 맞서 버티는 데 드는 토크다.

> **코리올리·원심 항의 정의.** **코리올리·원심 항**(Coriolis and centripetal terms) $c(\theta, \dot\theta)$는 *자세와 속도에 의존하는 관절 토크 벡터*다. 정의 조건 셋. **관절 속도의 이차식이다**: 각 성분이 곱 $\dot\theta_j\dot\theta_k$의 합이므로 $c(\theta, a\dot\theta) = a^2c(\theta, \dot\theta)$이고, 정지해 있으면 $c = 0$이다. **$M(\theta)$만으로 생긴다**: 계수가 질량 행렬의 도함수이므로, 아래 진자처럼 $M$이 상수면 $c \equiv 0$이다. 그리고 **곱의 모양으로 이름이 붙는다**: $\dot\theta_j^2$ 항은 원심 항이고, $j \ne k$인 $\dot\theta_j\dot\theta_k$ 항은 코리올리 항이다(MR §8.1). 같은 제곱 항을 MR은 centripetal(구심)이라 부르고, 10번 페이지와 많은 책은 centrifugal(원심)이라 부른다.
>
> $$c_i(\theta, \dot\theta) = \sum_{j,k}\Gamma_{ijk}(\theta)\,\dot\theta_j\dot\theta_k, \qquad \Gamma_{ijk} = \tfrac12\Bigl(\frac{\partial M_{ij}}{\partial\theta_k} + \frac{\partial M_{ik}}{\partial\theta_j} - \frac{\partial M_{jk}}{\partial\theta_i}\Bigr)$$
>
> 여기서 $\Gamma_{ijk}$는 [[02-foundations/manipulator-kinematics-dynamics|10. §4]]의 크리스토펠 기호(10의 $c_{ijk}$)다. 이차식이 되는 것은 연쇄법칙이 $\dot M$을 $\sum_k (\partial M/\partial\theta_k)\,\dot\theta_k$로 바꾸어, $M\dot\theta$에 이미 있던 속도 옆에 속도 하나를 더 세우기 때문이다.
>
> - **예**: 카탈로그 자세에서 $\dot\theta = (1, -1)$로 움직이는 P2. 5단계의 $c = (1, 1)\,\mathrm{N\,m}$은 $-2\sin\theta_2\,\dot\theta_1\dot\theta_2$에서 나온 코리올리 몫 $(2, 0)$과 원심 몫 $(-1, 1)$의 합이다.
> - **비예**: 점성 마찰 $b\dot\theta$. 이것도 속도에 의존하고 정지하면 사라지지만 선형이다. $\dot\theta = (2, -2)$에서 마찰은 두 배가 되는데 $c$는 네 배인 $(4, 4)$가 된다. 한 속도에서 맞춘 선형 모형은 그 속도와 정지 상태에서만 맞고, 같은 방향의 다른 속도에서는 모두 틀린다.

> **중력 벡터의 정의.** **중력 벡터**(gravity vector) $g(\theta)$는 *자세에만 의존하는 관절 토크 벡터*다. 정의 조건 셋. **$\dot\theta$와 $\ddot\theta$에 의존하지 않는다.** 그래서 어떤 자세든 가만히 붙들어 두는 데 드는 토크 전부다. **하나의 퍼텐셜 에너지의 기울기다.** 스칼라 $U(\theta)$ 하나가 모든 성분을 만든다. 그리고 **관절 $i$는 자기보다 바깥의 질량만 느낀다**: 관절 $i$를 돌려도 그 안쪽은 아무것도 오르내리지 않으므로, $g_i$는 바깥 링크들에 대해서만 더한다.
>
> $$g(\theta) = \frac{\partial U}{\partial\theta}, \qquad U(\theta) = \sum_k m_k\,g\,y_k(\theta)$$
>
> 여기서 $m_k$와 $y_k$는 점질량 $k$의 질량과 높이, $g = 9.81\,\mathrm{m/s^2}$이다. 스칼라가 벡터와 같은 글자를 쓰는 것은 MR의 관례다. 관절 축이 수평인 P2에서는 각 항이 무게 곱하기 관절 축에서의 부호 있는 수평 거리인데, 그런 관절 각으로 높이를 미분하면 바로 그 거리가 나오기 때문이다.
>
> - **예**: 카탈로그 자세의 P2는 $g = (19.62,\ 0)\,\mathrm{N\,m}$이다. 어깨가 두 질량을 모두 $1\,\mathrm{m}$에서 든다. 곧게 펴면 $(29.43,\ 9.81)$이다.
> - **비예**: 무게 곱하기 링크 길이. 카탈로그 자세에서 이렇게 하면 엘보에 $m_2 g L_2 = 9.81\,\mathrm{N\,m}$을 매기지만, 전완 질량이 엘보 바로 위에 있으므로 $g_2 = 0$이다. 이 곱은 곧게 편 자세처럼 링크가 수평일 때만 맞는다. 이렇게 만든 중력 보상 항은 아무것도 필요 없는 관절을 민다.

**진자에는 셋 중 둘만 있다.** 질량 $m$, 길이 $l$, 연직에서의 각 $\theta$이면 $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$다.

- $M = ml^2$는 관성이고, 상수다.
- $g(\theta) = mgl\sin\theta$는 중력 토크이고, 자세에 의존한다.
- 코리올리 항 $c$는 *0*이다. $M$이 $\theta$에 의존하지 않기 때문이다. (관성이 자세에 의존하는 1관절 계라면 $c = \tfrac12 M'(\theta)\dot\theta^2$가 남는다.)

P2에서는 '대상으로 한 번 끝까지'가 둘째 링크가 만드는 도약의 양쪽에 숫자를 붙였다. 곧게 편 자세와 카탈로그 자세 사이에서 $M_{11}$이 $5$에서 $3\ \mathrm{kg\,m^2}$으로 떨어지는데, 전완 질량이 어깨 축에 가까워지기 때문이고, 같은 어깨 가속도에 토크가 $40\,\%$ 덜 든다. 비대각 성분 $2$ 그리고 $1$은 결합이다. 한 관절을 가속하면 다른 관절이 밀린다. 진자에는 둘 다 없었다.

### 2. 질량 행렬의 정의

시뮬레이터는 매 스텝 $M$의 역행렬을 구하고, 계산 토크 제어기는 $M$을 곱하며, 한 자세에서 맞던 이득이 다른 자세에서 깨지는 이유도 $M$이다. $M$이 항등행렬인 셈 치고 설계한 제어기는 존재하지 않는 로봇을 위해 설계한 것이다. 그래서 정확한 정의가 필요하다.

**질량 행렬** $M(\theta)$는 주어진 자세에서 관절 속도를 운동 에너지로 바꾸는 $n \times n$ 행렬이다. 로봇에 붙은 숫자가 아니라 *자세의 함수*인 행렬값 함수이고, 정의 조건이 셋이며 셋 다 성립해야 한다:

1. 운동 에너지를 이차형식으로 나타낸다, $\mathcal{K} = \tfrac12\dot\theta^\top M(\theta)\dot\theta$;
2. **대칭**이다, $M = M^\top$;
3. **양정부호**다, 0이 아닌 모든 $\dot\theta$에 대해 $\dot\theta^\top M\dot\theta > 0$ ([[02-foundations/linear-algebra|1. 선형대수 §3]]).

$$\mathcal{K}(\theta, \dot\theta) = \tfrac12\,\dot\theta^\top M(\theta)\,\dot\theta$$

여기서 $\dot\theta \in \mathbb{R}^n$은 관절 속도, $M(\theta) \in \mathbb{R}^{n\times n}$은 그 자세의 질량 행렬, $\mathcal{K}$는 팔 전체의 운동 에너지(줄)다. 2단계가 $M$을 읽어 낸 형태가 이것인데, 점질량의 운동 에너지는 속력 제곱의 합이고 각 속도가 $\dot\theta$에 선형이기 때문이다. 3번은 움직이는 팔의 운동 에너지가 양수이기 때문에 성립하고([[02-foundations/manipulator-kinematics-dynamics|10. §2]]가 P2에서 $\det M = 1 + \sin^2\theta_2 \ge 1$로 보여 준다), $M^{-1}$의 존재를 보장하므로 모든 자세에서 순동역학이 풀린다.

- **예**: 2단계의 P2 $M(\theta_2)$, 카탈로그 자세에서 $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$. 보기만 해도 대칭이고, 고윳값 $2 \pm \sqrt2$가 둘 다 양수라 양정부호이며, $\tfrac12(1,-1)M(1,-1)^\top = 1\,\mathrm{J}$이 5단계 운동의 운동 에너지로 요구대로 양수다.
- **비예**: 같은 자세에서 카탈로그가 함께 적어 둔 작업 공간 관성 $\Lambda = (JM^{-1}J^\top)^{-1} = \mathrm{diag}(1,2)$. 이것도 대칭이고 양정부호지만 질량 행렬이 *아니다*. **말단**이 작업 좌표에서 느끼는 관성이라 성분의 단위가 $\mathrm{kg\,m^2}$이 아니라 킬로그램이고, 관절마다가 아니라 과제 방향마다 하나씩이다. $\Lambda$에서 "팔이 $y$에서 두 배 무겁다"를 읽고 나서 그 $\Lambda$를 $\tau = M\ddot\theta + \ldots$에 대입하는 것이, 이 페이지의 대상이 10번 페이지의 대상과 섞이는 표준적인 방식이다.
- **모터도 그 안에 있다**: 기어 달린 모터는 회전자의 반사 관성 $n^2J_m$을 $M$에 보탠다. [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §4]]의 고정 구동계를 감속비 100으로 달면 P2의 엘보에서 이미 링크 자신의 것과 같다.

### 3. 순동역학과 역동역학, 그리고 유도 두 가지

**순동역학**($\tau \to \ddot\theta$)은 가속도에 대해 푼 방정식 $\ddot\theta = M^{-1}(\tau - c - g)$이고, 시뮬레이터가 매 스텝 적분하는 것이다. 모든 물리 엔진(Isaac, MuJoCo)이 이 방정식 + 접촉이다. **역동역학**($\ddot\theta \to \tau$)은 같은 방정식을 왼쪽에서 오른쪽으로 계산한 것이고, 제어기가 피드포워드로 공급하는 것이다([[04-robotics/modern-robotics/ch11-robot-control|11장]]). '대상으로 한 번 끝까지'의 5단계와 6단계가 같은 상태를 양방향으로 읽은 것이며, 여기 방정식이 하나뿐임을 보는 가장 싼 방법이다.

> **순동역학과 역동역학의 정의.** **순동역학**(forward dynamics)과 **역동역학**(inverse dynamics)은 *하나의 운동 방정식 위에 세운 두 계산 문제*이고, 무엇이 미지수인지로 갈린다. 정의 조건 셋. **둘 다 온전한 상태가 필요하다**: $c$가 $\dot\theta$에 의존하므로 자세 $\theta$만으로는 모자라고 $(\theta, \dot\theta)$가 있어야 한다. **순동역학**은 $\tau$를 받아 $M$에 대한 선형 연립방정식을 풀어 $\ddot\theta$를 돌려준다. $M$이 양정부호이므로 해가 늘 있다(§2). **역동역학**은 원하는 $\ddot\theta$를 받아 연립방정식을 풀지 않고 $\tau$를 돌려준다. 재귀 뉴턴–오일러 알고리즘(MR §8.3)이 링크를 바깥으로 한 번, 안쪽으로 한 번 훑어 계산하므로 $O(n)$이다.
>
> $$\text{forward: } \ddot\theta = M(\theta)^{-1}\bigl(\tau - c(\theta, \dot\theta) - g(\theta)\bigr), \qquad \text{inverse: } \tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$
>
> 두 줄은 미지수만 다르게 푼 한 방정식이므로, 같은 상태에서 서로를 되돌린다.
>
> - **예**: 카탈로그 자세에서 $\dot\theta = (1, -1)$인 P2. $\ddot\theta = (1, 0)$에 대한 역동역학은 $\tau = (3, 1) + (1, 1) + (19.62, 0) = (23.62,\ 2)\,\mathrm{N\,m}$이고, 그 $\tau$를 순동역학에 넣으면 $(1, 0)$이 돌아온다.
> - **비예**: 정적 토크 $g(\theta)$. 이것은 $\dot\theta = \ddot\theta = 0$에서 계산한 역동역학일 뿐 그 이상이 아니다. 위의 요청에 대해 $(19.62,\ 0)$을 답해 $4$와 $2\,\mathrm{N\,m}$을 빠뜨린다. $M\ddot\theta$와 $c$를 뺀 피드포워드는 정확히 그만큼을 피드백 이득에 떠넘긴다.

**유도는 둘, 답은 하나.** **라그랑주** 경로는 에너지 기반이다. $\mathcal{K}$와 $U$를 쓰고 미분하면 세 항이 떨어져 나오는데, '대상으로 한 번 끝까지'가 한 일이 정확히 그것이다. **재귀 뉴턴–오일러** 경로는 힘 평형이다. 바깥쪽으로 훑어 속도와 가속도를, 안쪽으로 훑어 힘을 구하고, $M$을 명시적으로 만들지 않아 $O(n)$이다. 시뮬레이터와 제어기가 실제로 돌리는 쪽이 이것이다. 두 경로는 모든 숫자에서 일치하고, 6단계의 상태가 그것을 보여 준다. 바깥으로: 두 질량 모두 $(-1, 0)\,\mathrm{m/s^2}$로 가속한다. 안으로: 전완은 말단 질량을 $m_2(a_2 + 9.81\,\hat y) = (-1,\ 9.81)\,\mathrm{N}$으로 밀어야 하고, 질량보다 $1\,\mathrm{m}$ 아래에 있는 엘보에 대한 그 모멘트가 $\tau_2 = 1\,\mathrm{N{\cdot}m}$다. 어깨에 대해서는 말단 질량이 $9.81 + 1 = 10.81$, 엘보 질량이 $9.81$(옆 방향 $1\,\mathrm{N}$은 축을 지난다)을 들게 하므로 $\tau_1 = 20.62\,\mathrm{N{\cdot}m}$다. $M$도, 크리스토펠 기호 하나도 만들지 않고 6단계의 $(20.62,\ 1)$이 나왔다. 두 경로는 무엇에 편한가에서만 다르다.

작업 공간 버전은 같은 구조를 말단에서 표현한다. operational-space 제어([[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §6]])와 임피던스 제어([[04-robotics/force-compliance-control|힘·컴플라이언스 제어 §2]])로 가는 다리다.

**위키 연결**: sim-to-real 격차는 이 방정식의 파라미터 불일치에 살고,
[[01-canonical-papers/notes/5-world-models/dreamer|월드모델]]은 이것의 암시적 버전을 *학습*하며,
[[04-robotics/convex-mpc-legged|convex MPC]]는 풀림성을 사려고 이를 의도적으로
단순화(단일 강체)한다.

### 스스로 점검

1. 질량 행렬 $M(\theta)$가 자세에 의존하는 이유를 팔을 뻗은 상태와 접은 상태의 관성으로 설명하라.
2. 순동역학과 역동역학 중 시뮬레이터가 적분하는 것은 어느 쪽이고, 제어기가 피드포워드로 쓰는 것은 어느 쪽인가?
3. 코리올리 항 $c(\theta, \dot\theta)$는 왜 속도의 이차식인가?
4. P2가 카탈로그 자세에서 $\dot\theta = (2, 0)\,\mathrm{rad/s}$다. 어깨는 돌고 엘보는 붙들려 있다. $c$는 얼마이고, 어느 관절이 그것을 내야 하는가?

> [!tip]- 정답
> 1. 회전 관성은 질량이 축에서 얼마나 떨어져 있는지에 달렸다. 팔을 뻗으면 말단 링크가 멀리 나가 같은 관절 가속도에 훨씬 큰 토크가 들고, 접으면 가까워져 덜 든다. 관성이 기하의 함수이고 기하가 곧 $\theta$다. P2에서는 $M_{11} = 3 + 2\cos\theta_2$가 엘보가 닫힐수록 $5$에서 $1\ \mathrm{kg\,m^2}$까지 내려간다.
> 2. 시뮬레이터 = 순동역학($\tau \to \ddot\theta$)을 매 스텝 적분한다. 제어기 피드포워드 = 역동역학($\ddot\theta \to \tau$)이다.
> 3. 운동 에너지 $\tfrac12\dot\theta^\top M(\theta)\dot\theta$를 라그랑주 방정식에 넣으면 $M$을 $\theta$로 미분하게 되고, 연쇄법칙이 $\partial M/\partial\theta$를 $\dot\theta_i\dot\theta_j$ 곱으로 바꾼다. 속도 곱하기 속도다.
> 4. $\dot\theta_2 = 0$이므로 첫 성분은 $-\sin\theta_2\cdot 0\cdot(\ldots) = 0$이고, 둘째 성분은 $\sin 90^\circ\,\dot\theta_1^2 = 4\,\mathrm{N\,m}$이다. 즉 $c = (0,\ 4)$이고, 움직이지도 않는 **엘보**가 그것을 내야 한다. 원심 항이다. 어깨가 휘두르는 동안 전완을 고정된 각으로 붙들고 있는 데 토크가 들고, 그 값은 어깨 속도의 제곱으로 커진다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 같은 장치 **P2**, 같은 질량, 같은 연직 평면. 다만 어깨를 들어 올린다. 자세는 이제 $\theta = (30^\circ, 60^\circ)$, 링크 1은 $30^\circ$이고 $\theta_1 + \theta_2 = 90^\circ$이므로 전완은 다시 곧장 위를 향한다. 엘보는 $(0.866,\ 0.5)$, 말단은 $(0.866,\ 1.5)$에 있다. 모든 숫자를 '대상으로 한 번 끝까지'의 식에서 유도하라. $\Lambda$는 이 페이지가 아니라 [[02-foundations/manipulator-kinematics-dynamics|10]]의 랩이다.

1. **그리기.** 위의 그림에서 $\theta = (30^\circ, 60^\circ)$를 주 그림으로, 카탈로그 자세를 얇은 둘째 벌로 그린다. 질량 둘, 무게 화살표 둘, 그리고 어깨와 엘보에서의 수평 모멘트 팔. $\tau = M\ddot\theta + c + g$의 세 항 중 어느 자세가 어느 항을 크게 만드는지 그림 위에 표시하라.
2. **유도.** (a) $M(\theta_2)$에서 이 자세의 $M$, 그리고 $\det M$, $M^{-1}$, 고윳값 둘. (b) 이 자세의 $g$, 그리고 엘보가 이번에도 아무것도 들지 않는 이유. (c) $\dot\theta = (1,-1)$의 $c$. (d) 정지 상태에서 $\tau = g + (1, 0)\,\mathrm{N\,m}$을 명령하고(중력 보상에 어깨에만 1뉴턴미터) $\ddot\theta$를 구하라.
3. **해석.** 같은 추가 토크 $(1,0)\,\mathrm{N\,m}$은 카탈로그 자세에서 $\ddot\theta = (0.5, -0.5)$를, 그림의 곧게 편 자세에서 $(1, -2)$를 준다. (d)를 그 사이에 놓아라. 엘보가 열릴수록 어깨의 반응과 엘보의 기생 가속도 중 어느 쪽이 더 빨리 커지는가? 고정된 관절 이득 한 쌍이 세 자세 모두에서 옳을 수 없는 이유는? 그리고 자세가 바뀌었는데도 $g_2$가 0에 머문 이유는?

> [!note]- 그리는 법 · How to draw it
> - 두 자세를 같은 축 위에 그린다. 주 자세는 실선, 다른 자세는 얇게. 어깨 축은 원점, 중력은 $-\hat y$ 방향이다.
> - 각 링크 말단의 점질량 자리에 속을 채운 원을 찍고, 각각에서 $9.81\,\mathrm{N}$ 무게 화살표를 곧장 아래로 내린다. 질량 둘, 화살표 둘, 길이는 같다.
> - 어깨 축에서 각 질량까지 수평 점선을 긋고 길이를 적는다. 엘보 축에서는 질량 2까지 하나. 이 길이들이 중력 계산의 전부다.
> - 모멘트 팔을 확인한다. 링크 길이가 아니라 축에서 질량까지의 수평 거리다. 축 바로 위의 질량은 그 축에 대한 팔이 $0$이다. $(30^\circ, 60^\circ)$에서는 전완이 다시 수직이라 말단 질량이 엘보 바로 위에 있고, 어깨에서의 두 팔은 카탈로그 자세의 $1\,\mathrm{m}$ 대신 $\cos30^\circ = 0.866\,\mathrm{m}$다.
> - 굽은 토크 화살표 둘, 베이스의 $\tau_1$과 엘보의 $\tau_2$.
> - 그림 옆에 $\tau = M(\theta)\ddot\theta + c(\theta,\dot\theta) + g(\theta)$를 적고 팔이 정지했을 때 남는 항에 동그라미를 친다. 둘째 줄에는 같은 자세를 지나가며 움직일 때 남는 항에 동그라미를 친다. 두 동그라미의 차이가 이 장의 존재 이유다.

> [!tip]- 정답
> 1. $(30^\circ, 60^\circ)$에서는 두 질량 모두 어깨 축 오른쪽 $0.866\,\mathrm{m}$에 있고 말단 질량은 엘보 바로 위에 있다. 그래서 어깨에서의 두 팔은 카탈로그 자세의 $1$과 $1\,\mathrm{m}$ 대신 $0.866$이고, 엘보에서의 팔은 둘 다 $0$이다. 따라서 카탈로그 자세가 $g$를 더 크게($19.62$ 대 $16.99\,\mathrm{N\,m}$), $c$를 더 크게($\sin\theta_2$에 비례하므로 $1$ 대 $0.866$) 만들고, $(30^\circ, 60^\circ)$가 $M$을 더 크게($M_{11} = 4$ 대 $3$), 더 고르지 않게 만든다.
> 2. (a) $\cos60^\circ = 0.5$이므로 $M = \begin{pmatrix}4&1.5\\1.5&1\end{pmatrix}$, $\det M = 4 - 2.25 = 1.75$, $M^{-1} = \frac{1}{1.75}\begin{pmatrix}1&-1.5\\-1.5&4\end{pmatrix} = \begin{pmatrix}0.571&-0.857\\-0.857&2.286\end{pmatrix}$, 고윳값은 $(5 \pm \sqrt{25 - 7})/2 = 4.621$과 $0.379\ \mathrm{kg\,m^2}$로 비가 $12.2$다. 카탈로그 자세의 $5.83$과 곧게 편 자세의 $34.0$ 사이다. (b) $g = \bigl(9.81(2\cos30^\circ + \cos90^\circ),\ 9.81\cos90^\circ\bigr) = (9.81\times1.732,\ 0) = (16.99,\ 0)\,\mathrm{N\,m}$. 엘보가 이번에도 아무것도 들지 않는 것은 $g_2$가 전완의 절대 각 $\theta_1 + \theta_2$에 달렸는데 그것이 카탈로그 자세처럼 $90^\circ$이기 때문이다. $M$은 바뀐 $\theta_2$에만 달렸다. (c) $c = \bigl(-\sin60^\circ\cdot(-1)(2 - 1),\ \sin60^\circ\cdot1^2\bigr) = (0.866,\ 0.866)\,\mathrm{N\,m}$, 카탈로그 자세의 $(1, 1)$의 $0.866$배다. (d) $\ddot\theta = M^{-1}(1, 0)^\top = (0.571,\ -0.857)\,\mathrm{rad/s^2}$.
> 3. 엘보가 $90^\circ$에서 $60^\circ$를 거쳐 $0^\circ$로 열리는 동안 어깨의 반응은 $0.5 \to 0.571 \to 1$로 전 구간에서 두 배, 엘보의 기생 가속도는 $-0.5 \to -0.857 \to -2$로 네 배가 된다. 결합 쪽이 더 빨리 변한다. 고정된 이득 쌍은 한 관성에 맞춰 조율해 놓고 다른 관성을 만나므로, 같은 명령 토크가 자세마다 다른 어깨 반응과 다른 요청하지 않은 엘보 운동을 만든다. 요행을 바라는 대신 $M(\theta)$를 곱해야 한다는 논거이고, [[04-robotics/modern-robotics/ch11-robot-control|11장]]이 계산 토크로 시작하는 이유다. $g_2$가 0에 머문 것은 엘보에 걸리는 중력이 전완의 절대 각에만 달렸는데, 어깨를 $30^\circ$ 올리고 엘보를 $30^\circ$ 닫아 전완이 그대로 서 있었기 때문이다.
