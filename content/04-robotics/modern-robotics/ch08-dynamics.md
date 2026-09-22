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
> You need the Jacobian from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]], positive-definite matrices ([[02-foundations/linear-algebra|1. Linear Algebra §3]]), and Lagrange's equation $\frac{d}{dt}\frac{\partial L}{\partial\dot\theta} - \frac{\partial L}{\partial\theta} = \tau$ with $L = \mathcal{K} - U$, Newton's second law rewritten in energy terms ([[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §2]]), together with the Christoffel symbols it produces ([[02-foundations/manipulator-kinematics-dynamics|10. §4]]). This page applies Lagrange's equation to P2 but does not derive it, and Newton's second law alone will not carry you through Step 4 of the worked case. The plant is **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]].
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안, [[02-foundations/linear-algebra|PSD 행렬]], 그리고 뉴턴 제2법칙을 에너지로 다시 쓴 라그랑주 방정식 $\frac{d}{dt}\frac{\partial L}{\partial\dot\theta} - \frac{\partial L}{\partial\theta} = \tau$, $L = \mathcal{K} - U$ ([[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §2]])와 거기서 나오는 크리스토펠 기호([[02-foundations/manipulator-kinematics-dynamics|10. §4]])가 필요하다. 이 페이지는 라그랑주 방정식을 P2에 적용할 뿐 유도하지 않으며, 뉴턴 제2법칙만으로는 '대상으로 한 번 끝까지'의 4단계를 따라갈 수 없다. 장치는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**다.

## English

**Core question**: what torques produce what accelerations?

> [!note] First pass · 처음이라면
> Read the running plant, the picture, and Steps 1–3 of the worked case — $M$ read off the kinetic energy, $g$ off the potential — then §1 and §2. Step 4 (Coriolis from the Christoffel symbols) leans on Lagrange's equation from 10. §2 and §4: if that is new, take Step 4's formula on trust the first time and read Steps 5–7, which use it in both directions. §3's two derivations and the wiki connections are second pass.

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] with its mass properties switched on: unit links $L_1 = L_2 = 1\,\mathrm{m}$, point masses $m_1 = m_2 = 1\,\mathrm{kg}$ at the distal end of each link, and, because this chapter needs weight, the arm standing in the vertical plane with $g = 9.81\,\mathrm{m/s^2}$ acting in $-\hat y$. The catalog freezes the pose $\theta = (0^\circ, 90^\circ)$ — elbow at $(1,0)$, forearm straight up, tip at $(1,1)$ — and the mass matrix $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ there.

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
  <text x="14" y="291" font-size="11">θ = 0</text><circle cx="16.9" cy="281.5" r="0.8" fill="currentColor"/>
  <text x="14" y="305" font-size="11">θ = 0</text><circle cx="15.4" cy="295.5" r="0.8" fill="currentColor"/><circle cx="18.3" cy="295.5" r="0.8" fill="currentColor"/>
  <text x="200" y="284" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="284" font-size="12.5" text-anchor="end">M(θ)θ</text>
  <circle cx="267.1" cy="273.2" r="0.9" fill="currentColor"/><circle cx="270.4" cy="273.2" r="0.9" fill="currentColor"/>
  <text x="287" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="284" font-size="12.5" text-anchor="end">c(θ, θ</text>
  <text x="349" y="284" font-size="12.5">)</text>
  <circle cx="345.8" cy="273.2" r="0.9" fill="currentColor"/>
  <text x="372" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="405" y="284" font-size="12.5" text-anchor="middle">g(θ)</text>
  <text x="434" y="284" font-size="12">= (19.62, 0) N·m</text>
  </g>
  <ellipse cx="405" cy="280" rx="19" ry="12" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g fill="currentColor">
  <text x="14" y="324" font-size="11" font-weight="bold">moving through</text>
  <text x="14" y="339" font-size="11">θ = (1, −1) rad/s</text><circle cx="16.9" cy="329.5" r="0.8" fill="currentColor"/>
  <text x="14" y="353" font-size="11">θ = 0</text><circle cx="15.4" cy="343.5" r="0.8" fill="currentColor"/><circle cx="18.3" cy="343.5" r="0.8" fill="currentColor"/>
  <text x="200" y="332" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="332" font-size="12.5" text-anchor="end">M(θ)θ</text>
  <circle cx="267.1" cy="321.2" r="0.9" fill="currentColor"/><circle cx="270.4" cy="321.2" r="0.9" fill="currentColor"/>
  <text x="287" y="332" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="332" font-size="12.5" text-anchor="end">c(θ, θ</text>
  <text x="349" y="332" font-size="12.5">)</text>
  <circle cx="345.8" cy="321.2" r="0.9" fill="currentColor"/>
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

Everything below is P2's own numbers, in order, with nothing quoted that is not first derived. The one equation the steps apply is Lagrange's equation, derived from Newton's second law on [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §2]]:

$$\frac{d}{dt}\frac{\partial\mathcal{K}}{\partial\dot\theta_i} - \frac{\partial\mathcal{K}}{\partial\theta_i} + \frac{\partial U}{\partial\theta_i} = \tau_i, \qquad i = 1, 2$$

with $\mathcal{K}$ the kinetic and $U$ the potential energy, so Steps 1–2 build $\mathcal{K}$, Step 3 differentiates $U$, and Step 4 collects what differentiating $\mathcal{K}$ leaves over.

**Step 1 — kinetic energy, written out.** Mass 1 sits at $(L_1c_1,\ L_1s_1)$ and mass 2 at the tip, so differentiating and squaring gives

$$|v_1|^2 = L_1^2\dot\theta_1^2, \qquad |v_2|^2 = L_1^2\dot\theta_1^2 + L_2^2(\dot\theta_1{+}\dot\theta_2)^2 + 2L_1L_2\,\dot\theta_1(\dot\theta_1{+}\dot\theta_2)\cos\theta_2$$

because the cross term of the two link velocities carries $\cos\theta_1\cos(\theta_1{+}\theta_2) + \sin\theta_1\sin(\theta_1{+}\theta_2) = \cos\theta_2$ — the *relative* elbow angle, and nothing else. With the catalog's unit links and unit masses, $2\mathcal{K} = |v_1|^2 + |v_2|^2$ collects into

$$2\mathcal{K} = (3 + 2\cos\theta_2)\,\dot\theta_1^2 + 2(1 + \cos\theta_2)\,\dot\theta_1\dot\theta_2 + \dot\theta_2^2.$$

**Step 2 — read $M$ off the quadratic form.** Matching $2\mathcal{K} = \dot\theta^\top M\dot\theta$ (the quadratic form that defines the mass matrix, §2) term by term, the $\dot\theta_1^2$ coefficient is $M_{11}$, the $\dot\theta_2^2$ coefficient is $M_{22}$, and the $\dot\theta_1\dot\theta_2$ coefficient is $2M_{12}$ because symmetry splits it between the two off-diagonal entries:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

and only $\theta_2$ appears, since turning the whole arm about the shoulder cannot change how mass is distributed about its own axes. At the catalog pose $\cos\theta_2 = 0$, so $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ — the catalog matrix, now earned. Its eigenvalues are $2 \pm \sqrt2 = 3.4142$ and $0.5858\ \mathrm{kg\,m^2}$, both positive, and their ratio $5.83$ is how much heavier the arm's heaviest direction is than its lightest. Straighten to $\theta_2 = 0$ and $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$, whose eigenvalues are $3 \pm 2\sqrt2 = 5.8284$ and $0.1716$, a ratio of $34.0$: extending the arm does not merely make it heavier, it makes it far more *unevenly* heavy.

**Step 3 — gravity, from the potential.** The potential energy is $U = g(m_1y_1 + m_2y_2) = g\,(2\sin\theta_1 + \sin(\theta_1{+}\theta_2))$ with the catalog numbers, and the gravity vector is its gradient, the $\partial U/\partial\theta$ term of Lagrange's equation:

$$g(\theta) = \frac{\partial U}{\partial \theta} = \bigl(\,g(2\cos\theta_1 + \cos(\theta_1{+}\theta_2)),\ \ g\cos(\theta_1{+}\theta_2)\,\bigr)$$

where each cosine is a horizontal moment arm read straight off the picture. At the catalog pose $\cos\theta_1 = 1$ and $\cos(\theta_1{+}\theta_2) = 0$, giving $g = (19.62,\ 0)\,\mathrm{N\,m}$: the shoulder holds both masses at $1\,\mathrm{m}$, and the elbow holds nothing because its mass is directly overhead. At the straight pose the same formula gives $(29.43,\ 9.81)$ — half again as much at the shoulder.

**Step 4 — Coriolis, from how $M$ changes.** The velocity-product term comes from differentiating $M(\theta)$ inside the Lagrange equation; collecting it with the Christoffel symbols $\Gamma_{ijk} = \tfrac12(\partial M_{ij}/\partial\theta_k + \partial M_{ik}/\partial\theta_j - \partial M_{jk}/\partial\theta_i)$ of [[02-foundations/manipulator-kinematics-dynamics|10. §4]] and using $c_i = \sum_{j,k}\Gamma_{ijk}\dot\theta_j\dot\theta_k$, only $\partial M/\partial\theta_2 \propto \sin\theta_2$ survives. Explicitly, the only nonzero derivatives are $\partial M_{11}/\partial\theta_2 = -2\sin\theta_2$ and $\partial M_{12}/\partial\theta_2 = \partial M_{21}/\partial\theta_2 = -\sin\theta_2$, because nothing depends on $\theta_1$ and $M_{22}$ is constant. So, for instance, $\Gamma_{122} = \tfrac12(\partial M_{12}/\partial\theta_2 + \partial M_{12}/\partial\theta_2 - \partial M_{22}/\partial\theta_1) = -\sin\theta_2$ and $\Gamma_{212} = \tfrac12(\partial M_{21}/\partial\theta_2 + \partial M_{22}/\partial\theta_1 - \partial M_{12}/\partial\theta_2) = 0$, and all eight symbols are

$$\Gamma_{112} = \Gamma_{121} = \Gamma_{122} = -\sin\theta_2, \qquad \Gamma_{211} = \sin\theta_2, \qquad \Gamma_{111} = \Gamma_{212} = \Gamma_{221} = \Gamma_{222} = 0$$

so that $c_1 = \Gamma_{112}\dot\theta_1\dot\theta_2 + \Gamma_{121}\dot\theta_2\dot\theta_1 + \Gamma_{122}\dot\theta_2^2$ and $c_2 = \Gamma_{211}\dot\theta_1^2$, which is

$$c(\theta, \dot\theta) = \bigl(\,-\sin\theta_2\,\dot\theta_2(2\dot\theta_1 + \dot\theta_2),\ \ \sin\theta_2\,\dot\theta_1^2\,\bigr)$$

which is quadratic in $\dot\theta$ and proportional to $\sin\theta_2$. Two consequences follow immediately and both get used below: $c$ vanishes identically whenever the arm is still, and it vanishes identically at $\theta_2 = 0$ or $180^\circ$ **whatever the velocity**, because a straight or folded elbow is where $M$ momentarily stops changing. The catalog pose $\theta_2 = 90^\circ$ is the opposite extreme, $|\sin\theta_2| = 1$: it is the most strongly velocity-coupled pose this arm has.

**Step 5 — one numerical case, end to end.** Put P2 at the catalog pose and set it *moving*: $\dot\theta = (1, -1)\,\mathrm{rad/s}$, shoulder opening while the elbow straightens. Command exactly the gravity torque, $\tau = g = (19.62,\ 0)$, which is what a naive "gravity compensation" controller does.

- Coriolis: $c_1 = -1\cdot(-1)\bigl(2(1) + (-1)\bigr) = 1$ and $c_2 = 1\cdot(1)^2 = 1$, so $c = (1,\ 1)\,\mathrm{N\,m}$.
- Net: $\tau - c - g = (19.62, 0) - (1,1) - (19.62, 0) = (-1,\ -1)\,\mathrm{N\,m}$.
- Inverse mass matrix: $\det M = 3 - 1 = 2$, so $M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}$.
- Forward dynamics (the equation of motion solved for $\ddot\theta$, §3): $\ddot\theta = M^{-1}(\tau - c - g) = (0,\ -1)\,\mathrm{rad/s^2}$.

So cancelling gravity on a *moving* arm leaves the shoulder with exactly zero acceleration and the elbow straightening faster, at $1\,\mathrm{rad/s^2}$. Every bit of that is the Coriolis term: at rest the same command would produce $\ddot\theta = 0$ and nothing would happen at all. A controller tuned on a stationary arm and tested on a moving one meets this difference first.

**Step 6 — the same line read backwards.** Ask instead for $\ddot\theta = 0$ at that same state — hold the velocity steady through the pose. Inverse dynamics (the same equation evaluated for $\tau$, §3) gives $\tau = c + g = (20.62,\ 1)\,\mathrm{N\,m}$: one extra newton-metre at *each* joint over the static hold, including at the elbow, which statically needed nothing. That $1\,\mathrm{N\,m}$ at an unloaded joint is the signature of velocity coupling, and it is exactly what a feedforward term supplies in [[04-robotics/modern-robotics/ch11-robot-control|ch.11]].

**Step 7 — at rest, only $g$ survives.** Set $\dot\theta = 0$. Then $c = 0$ by step 4 and the equation collapses to $\tau = M\ddot\theta + g$. Holding still means $\ddot\theta = 0$ and $\tau = g = (19.62,\ 0)$; feed that to forward dynamics and $\ddot\theta = M^{-1}(\tau - g) = 0$, so the simulator's next step does nothing. This is the state the problem set draws, and the one every other pose on this page should be compared against.

### 1. Where the three terms come from — one link, then two

**The equation of motion**, everything in one line:

$$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$

with the mass matrix (configuration-dependent inertia), the Coriolis and centripetal terms (velocity products), and gravity. The three add rather than compete because each is a separate demand on the same actuators: $M\ddot\theta$ is what it costs to change speed, $c$ is what it costs to be moving at all in a shape that is changing, and $g$ is what it costs simply to exist against gravity.

**A pendulum has only two of them.** With mass $m$, length $l$ and angle $\theta$ from vertical, $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$.

- $M = ml^2$ is the inertia, and it is constant.
- $g(\theta) = mgl\sin\theta$ is the gravity torque, and it depends on configuration.
- The Coriolis term $c$ is *zero* because $M$ does not depend on $\theta$. (A one-joint system with configuration-dependent inertia would still have $c = \tfrac12 M'(\theta)\dot\theta^2$.)

Add a second link and $M$ becomes $\theta$-dependent and $c$ turns on — that is the whole jump from "one equation" to "why multi-link dynamics are hard." On P2 the worked case above put numbers on both halves of that jump: $M_{11}$ falls from $5$ to $3\ \mathrm{kg\,m^2}$ between the straight and catalog poses because the forearm mass moves closer to the shoulder axis, so the same shoulder acceleration needs $40\,\%$ less torque; and the off-diagonal entry, $2$ then $1$, is coupling — accelerating one joint pushes on the other. The pendulum had neither effect.

### 2. The mass matrix, defined

A **mass matrix** $M(\theta)$ is the $n \times n$ matrix that turns joint velocities into kinetic energy at a given configuration. It is not a number attached to the robot; it is a matrix-valued *function of the configuration*, and it has three defining conditions, all of which must hold:

1. it represents the kinetic energy as a quadratic form, $\mathcal{K} = \tfrac12\dot\theta^\top M(\theta)\dot\theta$;
2. it is **symmetric**, $M = M^\top$;
3. it is **positive definite**, $\dot\theta^\top M\dot\theta > 0$ for every nonzero $\dot\theta$ ([[02-foundations/linear-algebra|1. Linear Algebra §3]]).

$$\mathcal{K}(\theta, \dot\theta) = \tfrac12\,\dot\theta^\top M(\theta)\,\dot\theta$$

where $\dot\theta \in \mathbb{R}^n$ is the joint velocity, $M(\theta) \in \mathbb{R}^{n\times n}$ the mass matrix at that configuration, and $\mathcal{K}$ the arm's total kinetic energy in joules. Condition 3 is not a modelling convenience: a moving arm's kinetic energy can never be zero or negative, so the quadratic form behaves exactly like $x^2$ does for a scalar. Positive definiteness is also what guarantees $M^{-1}$ exists, which is what makes forward dynamics solvable at every configuration.

- **Example**: P2's $M(\theta_2)$ from step 2, with $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ at the catalog pose. Symmetric by inspection; positive definite because its eigenvalues $2 \pm \sqrt2$ are both positive; and $\tfrac12(1,-1)M(1,-1)^\top = 1\,\mathrm{J}$ is the kinetic energy of the step 5 motion, a positive number as required.
- **Non-example**: the operational-space inertia $\Lambda = (JM^{-1}J^\top)^{-1} = \mathrm{diag}(1,2)$, also listed in the catalog at this same pose. It is symmetric and positive definite too, and it is *not* the mass matrix: it is the inertia the **tip** feels in task coordinates, so its entries are kilograms rather than $\mathrm{kg\,m^2}$ and it has one entry per task direction rather than per joint. Reading "the arm is twice as heavy in $y$" off $\Lambda$ and then substituting $\Lambda$ into $\tau = M\ddot\theta + \ldots$ is the standard way this page's object gets confused with page 10's.
- **Why it matters**: $M$ is what a simulator inverts every step, what a computed-torque controller multiplies by, and the reason gains that work at one pose fail at another. A controller designed as though $M$ were the identity is designing for a robot that does not exist. A geared motor adds to $M$ as well, its rotor's reflected inertia $n^2J_m$: with the frozen drive of [[04-robotics/actuators-drives|10.5 Actuators & Drives §4]] at a gear ratio of 100 it already equals the link's own at P2's elbow.

### 3. Forward and inverse dynamics, and the two derivations

**Two derivations, one answer.** The **Lagrangian** route is energy-based — write $\mathcal{K}$ and $U$, differentiate, and the three terms fall out, which is exactly what the worked case did. The **recursive Newton–Euler** route is force-balance — sweep outward for velocities and accelerations, inward for forces — and it costs $O(n)$ instead of forming $M$ explicitly, which is why it is what simulators and controllers actually run. They agree on every number; they differ in what they are convenient for.

**Forward dynamics** ($\tau \to \ddot\theta$) is the equation solved for acceleration, $\ddot\theta = M^{-1}(\tau - c - g)$, and it is what a simulator integrates each step — every physics engine (Isaac, MuJoCo) is this equation plus contacts. **Inverse dynamics** ($\ddot\theta \to \tau$) is the same equation evaluated left to right, and it is what a controller feeds forward ([[04-robotics/modern-robotics/ch11-robot-control|ch.11]]). Steps 5 and 6 of the worked case are the same state read both ways, which is the cheapest way to see that there is only one equation here.

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

Tier B. Same plant **P2** from [[02-foundations/lab-plants|0.6]], same masses, same vertical plane — but the arm is **straightened**: the pose is now $\theta = (0^\circ, 0^\circ)$, both links along $+\hat x$, masses at $(1,0)$ and $(2,0)$. Derive every number from the formulas of the worked case; do not recompute $\Lambda$, that lab is [[02-foundations/manipulator-kinematics-dynamics|10]].

1. **Draw.** The picture above, with the straight pose as the main copy: both masses, both weight arrows, and the two horizontal moment arms from the shoulder now $1\,\mathrm{m}$ and $2\,\mathrm{m}$. Keep the catalog pose as the light second copy and mark, on the figure, which of the three terms of $\tau = M\ddot\theta + c + g$ each pose makes larger.
2. **Derive.** (a) $M$ at this pose from $M(\theta_2)$, with $\det M$, $M^{-1}$, and its two eigenvalues. (b) $g$ at this pose. (c) $c$ for $\dot\theta = (1,-1)$, and then the stronger claim: show that $c = 0$ here for *every* $\dot\theta$, and name the pose in this family that maximizes $c$ for a given $\dot\theta$. (d) Command $\tau = g + (1, 0)\,\mathrm{N\,m}$ — gravity compensation plus one newton-metre at the shoulder only — and give $\ddot\theta$.
3. **Interpret.** The same extra $(1,0)\,\mathrm{N\,m}$ at the catalog pose gives $\ddot\theta = (0.5, -0.5)$. Straightening the arm therefore changed both the shoulder's response and the elbow's parasitic acceleration. Which one changed by more, and say in one sentence why a fixed pair of joint gains cannot be right at both poses.

> [!note]- How to draw it · 그리는 법
> - Both poses on the same axes, the main one solid and the other light, with the shoulder axis at the origin and gravity along $-\hat y$.
> - A filled circle at each point mass, at the distal end of each link, and a $9.81\,\mathrm{N}$ weight arrow straight down from each: two masses, two arrows, the same length.
> - From the shoulder axis, a dashed horizontal to each mass, labelled with its length; from the elbow axis, one to mass 2. Those lengths are the whole gravity calculation.
> - Check each moment arm: it is the horizontal distance from the axis to the mass, not a link length. A mass directly above an axis has arm $0$ about it — in the picture above the forearm mass sits over the elbow, so both shoulder arms there are $1\,\mathrm{m}$.
> - Two curved torque arrows, $\tau_1$ at the base and $\tau_2$ at the elbow.
> - Beside the figure, write $\tau = M(\theta)\ddot\theta + c(\theta,\dot\theta) + g(\theta)$ and circle the terms that survive with the arm at rest; on a second line, circle those that survive when it moves through the same pose. The difference between the two circlings is what this chapter is for.

> [!tip]- Solutions
> 1. Straight pose: moment arms $1$ and $2\,\mathrm{m}$, so gravity is much larger; the mass matrix is larger too; the Coriolis term is smaller (it is zero). The catalog pose is the one that maximizes $c$.
> 2. (a) $\cos 0^\circ = 1$, so $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$, $\det M = 5 - 4 = 1$, $M^{-1} = \begin{pmatrix}1&-2\\-2&5\end{pmatrix}$, eigenvalues $3 \pm 2\sqrt2 = 5.8284$ and $0.1716\ \mathrm{kg\,m^2}$ — still positive definite, but a condition ratio of $34.0$ against $5.83$ at the catalog pose. (b) $g = (9.81(2 + 1),\ 9.81) = (29.43,\ 9.81)\,\mathrm{N\,m}$; the shoulder torque is $1.5\times$ the catalog value, and the elbow now carries its mass at a full metre instead of zero. (c) $\sin 0^\circ = 0$, so both components of $c$ carry a factor of zero and $c = (0,0)$ — for $\dot\theta = (1,-1)$ and for every other $\dot\theta$, since $\sin\theta_2$ multiplies the whole vector. The maximum is at $|\sin\theta_2| = 1$, i.e. $\theta_2 = \pm 90^\circ$: the catalog pose. (d) $\ddot\theta = M^{-1}(1,0)^\top = (1,\ -2)\,\mathrm{rad/s^2}$.
> 3. The shoulder response doubled ($0.5 \to 1$) while the elbow's parasitic acceleration quadrupled ($-0.5 \to -2$), so the coupling changed by more — four-fold against two-fold. A fixed gain pair is therefore tuned for one inertia and meets another: the same commanded torque produces twice the shoulder acceleration and four times the unrequested elbow acceleration at the far end of the workspace, which is the argument for multiplying by $M(\theta)$ instead of hoping, and the reason [[04-robotics/modern-robotics/ch11-robot-control|ch.11]] opens with computed torque.

## 한국어

**핵심 질문**: 어떤 토크가 어떤 가속도를 만드는가?

> [!note] 처음이라면 · First pass
> 이 페이지의 장치, 그림, 그리고 '대상으로 한 번 끝까지'의 1–3단계(운동 에너지에서 읽은 $M$, 퍼텐셜에서 읽은 $g$)를 읽고, 이어서 §1과 §2를 읽어라. 4단계(크리스토펠 기호에서 나온 코리올리)는 10. §2와 §4의 라그랑주 방정식에 기댄다. 그것이 처음이라면 첫 읽기에서는 4단계의 식을 믿고 넘어가, 그 식을 양방향으로 쓰는 5–7단계를 읽어라. §3의 유도 두 가지와 위키 연결은 두 번째 읽기다.

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**에 질량 성질을 켠 것이다. 단위 링크 $L_1 = L_2 = 1\,\mathrm{m}$, 각 링크 말단에 점질량 $m_1 = m_2 = 1\,\mathrm{kg}$, 그리고 이 장은 무게가 필요하므로 팔을 연직 평면에 세우고 $g = 9.81\,\mathrm{m/s^2}$가 $-\hat y$로 작용한다. 카탈로그가 고정한 자세는 $\theta = (0^\circ, 90^\circ)$ — 엘보 $(1,0)$, 전완은 곧장 위, 말단 $(1,1)$ — 이고 거기서 질량 행렬은 $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$이다.

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
  <text x="14" y="291" font-size="11">θ = 0</text><circle cx="16.9" cy="281.5" r="0.8" fill="currentColor"/>
  <text x="14" y="305" font-size="11">θ = 0</text><circle cx="15.4" cy="295.5" r="0.8" fill="currentColor"/><circle cx="18.3" cy="295.5" r="0.8" fill="currentColor"/>
  <text x="200" y="284" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="284" font-size="12.5" text-anchor="end">M(θ)θ</text>
  <circle cx="267.1" cy="273.2" r="0.9" fill="currentColor"/><circle cx="270.4" cy="273.2" r="0.9" fill="currentColor"/>
  <text x="287" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="284" font-size="12.5" text-anchor="end">c(θ, θ</text>
  <text x="349" y="284" font-size="12.5">)</text>
  <circle cx="345.8" cy="273.2" r="0.9" fill="currentColor"/>
  <text x="372" y="284" font-size="12.5" text-anchor="middle">+</text>
  <text x="405" y="284" font-size="12.5" text-anchor="middle">g(θ)</text>
  <text x="434" y="284" font-size="12">= (19.62, 0) N·m</text>
  </g>
  <ellipse cx="405" cy="280" rx="19" ry="12" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <g fill="currentColor">
  <text x="14" y="324" font-size="11" font-weight="bold">지나가며 움직임</text>
  <text x="14" y="339" font-size="11">θ = (1, −1) rad/s</text><circle cx="16.9" cy="329.5" r="0.8" fill="currentColor"/>
  <text x="14" y="353" font-size="11">θ = 0</text><circle cx="15.4" cy="343.5" r="0.8" fill="currentColor"/><circle cx="18.3" cy="343.5" r="0.8" fill="currentColor"/>
  <text x="200" y="332" font-size="12.5" text-anchor="middle">τ =</text>
  <text x="272" y="332" font-size="12.5" text-anchor="end">M(θ)θ</text>
  <circle cx="267.1" cy="321.2" r="0.9" fill="currentColor"/><circle cx="270.4" cy="321.2" r="0.9" fill="currentColor"/>
  <text x="287" y="332" font-size="12.5" text-anchor="middle">+</text>
  <text x="349" y="332" font-size="12.5" text-anchor="end">c(θ, θ</text>
  <text x="349" y="332" font-size="12.5">)</text>
  <circle cx="345.8" cy="321.2" r="0.9" fill="currentColor"/>
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

아래는 전부 P2 자신의 숫자이고, 순서대로이며, 먼저 유도하지 않고 인용하는 것은 하나도 없다. 각 단계가 적용하는 방정식은 하나, [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §2]]에서 뉴턴 제2법칙으로부터 유도한 라그랑주 방정식이다:

$$\frac{d}{dt}\frac{\partial\mathcal{K}}{\partial\dot\theta_i} - \frac{\partial\mathcal{K}}{\partial\theta_i} + \frac{\partial U}{\partial\theta_i} = \tau_i, \qquad i = 1, 2$$

여기서 $\mathcal{K}$는 운동 에너지, $U$는 퍼텐셜 에너지다. 그래서 1–2단계는 $\mathcal{K}$를 만들고, 3단계는 $U$를 미분하고, 4단계는 $\mathcal{K}$를 미분하고 남는 것을 모은다.

**1단계 — 운동 에너지를 펼쳐 쓴다.** 질량 1은 $(L_1c_1,\ L_1s_1)$에, 질량 2는 말단에 있으므로 미분해 제곱하면

$$|v_1|^2 = L_1^2\dot\theta_1^2, \qquad |v_2|^2 = L_1^2\dot\theta_1^2 + L_2^2(\dot\theta_1{+}\dot\theta_2)^2 + 2L_1L_2\,\dot\theta_1(\dot\theta_1{+}\dot\theta_2)\cos\theta_2$$

가 된다. 두 링크 속도의 교차항이 $\cos\theta_1\cos(\theta_1{+}\theta_2) + \sin\theta_1\sin(\theta_1{+}\theta_2) = \cos\theta_2$를 남기기 때문이다. *상대* 엘보 각이고, 그 외에는 아무것도 아니다. 카탈로그의 단위 링크와 단위 질량을 넣으면 $2\mathcal{K} = |v_1|^2 + |v_2|^2$가

$$2\mathcal{K} = (3 + 2\cos\theta_2)\,\dot\theta_1^2 + 2(1 + \cos\theta_2)\,\dot\theta_1\dot\theta_2 + \dot\theta_2^2$$

으로 모인다.

**2단계 — 이차형식에서 $M$을 읽는다.** $2\mathcal{K} = \dot\theta^\top M\dot\theta$(질량 행렬을 정의하는 이차형식, §2)와 항별로 맞추면 $\dot\theta_1^2$의 계수가 $M_{11}$, $\dot\theta_2^2$의 계수가 $M_{22}$, $\dot\theta_1\dot\theta_2$의 계수는 대칭성이 두 비대각 성분에 나누어 주므로 $2M_{12}$다:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

여기에 $\theta_2$만 나온다. 어깨 둘레로 팔 전체를 돌리는 것은 질량이 각 축에 대해 어떻게 분포하는지를 바꿀 수 없기 때문이다. 카탈로그 자세에서는 $\cos\theta_2 = 0$이므로 $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ — 이제 인용이 아니라 벌어서 얻은 카탈로그 행렬이다. 고윳값은 $2 \pm \sqrt2 = 3.4142$와 $0.5858\ \mathrm{kg\,m^2}$로 둘 다 양수이고, 그 비 $5.83$이 이 팔의 가장 무거운 방향이 가장 가벼운 방향보다 몇 배 무거운지를 말한다. $\theta_2 = 0$으로 곧게 펴면 $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$이고 고윳값은 $3 \pm 2\sqrt2 = 5.8284$와 $0.1716$, 비가 $34.0$이다. 팔을 뻗으면 그냥 무거워지는 것이 아니라 훨씬 더 *고르지 않게* 무거워진다.

**3단계 — 중력을 퍼텐셜에서.** 퍼텐셜 에너지는 $U = g(m_1y_1 + m_2y_2) = g\,(2\sin\theta_1 + \sin(\theta_1{+}\theta_2))$이고(카탈로그 숫자), 중력 벡터는 그 기울기, 곧 라그랑주 방정식의 $\partial U/\partial\theta$ 항이다:

$$g(\theta) = \frac{\partial U}{\partial \theta} = \bigl(\,g(2\cos\theta_1 + \cos(\theta_1{+}\theta_2)),\ \ g\cos(\theta_1{+}\theta_2)\,\bigr)$$

각 코사인이 그림에서 바로 읽히는 수평 모멘트 팔이다. 카탈로그 자세에서는 $\cos\theta_1 = 1$, $\cos(\theta_1{+}\theta_2) = 0$이므로 $g = (19.62,\ 0)\,\mathrm{N\,m}$이다. 어깨는 두 질량을 $1\,\mathrm{m}$에서 들고, 엘보는 질량이 바로 위에 있어 아무것도 들지 않는다. 곧게 편 자세에서는 같은 식이 $(29.43,\ 9.81)$을 준다. 어깨 쪽이 절반만큼 더 든다.

**4단계 — 코리올리를 $M$의 변화에서.** 속도 곱 항은 라그랑주 방정식 안에서 $M(\theta)$를 미분할 때 나온다. [[02-foundations/manipulator-kinematics-dynamics|10. §4]]의 크리스토펠 기호 $\Gamma_{ijk} = \tfrac12(\partial M_{ij}/\partial\theta_k + \partial M_{ik}/\partial\theta_j - \partial M_{jk}/\partial\theta_i)$로 모으고 $c_i = \sum_{j,k}\Gamma_{ijk}\dot\theta_j\dot\theta_k$를 쓰면, $\partial M/\partial\theta_2 \propto \sin\theta_2$만 살아남는다. 구체적으로 0이 아닌 도함수는 $\partial M_{11}/\partial\theta_2 = -2\sin\theta_2$와 $\partial M_{12}/\partial\theta_2 = \partial M_{21}/\partial\theta_2 = -\sin\theta_2$뿐이다. $\theta_1$에 의존하는 것이 없고 $M_{22}$는 상수이기 때문이다. 그래서 예를 들어 $\Gamma_{122} = \tfrac12(\partial M_{12}/\partial\theta_2 + \partial M_{12}/\partial\theta_2 - \partial M_{22}/\partial\theta_1) = -\sin\theta_2$, $\Gamma_{212} = \tfrac12(\partial M_{21}/\partial\theta_2 + \partial M_{22}/\partial\theta_1 - \partial M_{12}/\partial\theta_2) = 0$이고, 여덟 기호 전부는

$$\Gamma_{112} = \Gamma_{121} = \Gamma_{122} = -\sin\theta_2, \qquad \Gamma_{211} = \sin\theta_2, \qquad \Gamma_{111} = \Gamma_{212} = \Gamma_{221} = \Gamma_{222} = 0$$

이다. 따라서 $c_1 = \Gamma_{112}\dot\theta_1\dot\theta_2 + \Gamma_{121}\dot\theta_2\dot\theta_1 + \Gamma_{122}\dot\theta_2^2$, $c_2 = \Gamma_{211}\dot\theta_1^2$이고, 곧

$$c(\theta, \dot\theta) = \bigl(\,-\sin\theta_2\,\dot\theta_2(2\dot\theta_1 + \dot\theta_2),\ \ \sin\theta_2\,\dot\theta_1^2\,\bigr)$$

가 된다. $\dot\theta$의 이차식이고 $\sin\theta_2$에 비례한다. 곧바로 따라 나오는 결론이 둘이고 아래에서 둘 다 쓴다. 팔이 멈춰 있으면 $c$는 항등적으로 0이다. 그리고 $\theta_2 = 0$이나 $180^\circ$에서는 **속도가 무엇이든** 항등적으로 0이다. 곧게 펴거나 접은 엘보가 바로 $M$이 순간적으로 변하기를 멈추는 자리이기 때문이다. 카탈로그 자세 $\theta_2 = 90^\circ$는 정반대 극단인 $|\sin\theta_2| = 1$로, 이 팔이 가질 수 있는 가장 강하게 속도 결합된 자세다.

**5단계 — 수치 한 건을 끝까지.** P2를 카탈로그 자세에 두고 *움직이게* 한다. $\dot\theta = (1, -1)\,\mathrm{rad/s}$, 어깨는 열리고 엘보는 펴진다. 명령은 정확히 중력 토크 $\tau = g = (19.62,\ 0)$, 순진한 "중력 보상" 제어기가 하는 일 그대로다.

- 코리올리: $c_1 = -1\cdot(-1)\bigl(2(1) + (-1)\bigr) = 1$, $c_2 = 1\cdot(1)^2 = 1$이므로 $c = (1,\ 1)\,\mathrm{N\,m}$.
- 남는 힘: $\tau - c - g = (19.62, 0) - (1,1) - (19.62, 0) = (-1,\ -1)\,\mathrm{N\,m}$.
- 역질량 행렬: $\det M = 3 - 1 = 2$이므로 $M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}$.
- 순동역학(운동 방정식을 $\ddot\theta$에 대해 푼 것, §3): $\ddot\theta = M^{-1}(\tau - c - g) = (0,\ -1)\,\mathrm{rad/s^2}$.

즉 *움직이는* 팔에서 중력만 상쇄하면 어깨 가속도는 정확히 0이고 엘보는 $1\,\mathrm{rad/s^2}$로 더 빨리 펴진다. 전부 코리올리 항이다. 정지 상태였다면 같은 명령이 $\ddot\theta = 0$을 내고 아무 일도 일어나지 않았을 것이다. 멈춰 있는 팔에서 조율한 제어기를 움직이는 팔에 올리면 가장 먼저 만나는 차이가 이것이다.

**6단계 — 같은 줄을 반대로 읽는다.** 같은 상태에서 이번에는 $\ddot\theta = 0$을 요구한다. 속도를 유지한 채 그 자세를 지나가라는 뜻이다. 역동역학(같은 방정식을 $\tau$에 대해 계산한 것, §3)은 $\tau = c + g = (20.62,\ 1)\,\mathrm{N\,m}$을 준다. 정지 유지보다 *각* 관절에 $1\,\mathrm{N\,m}$씩 더 드는데, 정역학적으로는 아무것도 필요 없던 엘보에도 든다. 부하가 없는 관절의 그 $1\,\mathrm{N\,m}$이 속도 결합의 서명이고, [[04-robotics/modern-robotics/ch11-robot-control|11장]]에서 피드포워드 항이 공급하는 것이 정확히 그것이다.

**7단계 — 정지하면 $g$만 남는다.** $\dot\theta = 0$으로 두면 4단계에 의해 $c = 0$이고 방정식은 $\tau = M\ddot\theta + g$로 줄어든다. 가만히 있으라는 것은 $\ddot\theta = 0$이므로 $\tau = g = (19.62,\ 0)$이다. 이것을 순동역학에 넣으면 $\ddot\theta = M^{-1}(\tau - g) = 0$이라 시뮬레이터의 다음 스텝은 아무것도 하지 않는다. 과제가 그리는 상태이고, 이 페이지의 다른 모든 자세를 견주어야 할 기준이다.

### 1. 세 항이 어디서 오는가 — 1링크, 그다음 2링크

**운동 방정식**, 전부가 한 줄에:

$$\tau = M(\theta)\,\ddot\theta + c(\theta, \dot\theta) + g(\theta)$$

질량 행렬(자세 의존 관성), 코리올리·원심 항(속도 곱), 중력이다. 셋이 경쟁하지 않고 더해지는 이유는 같은 액추에이터에 걸리는 서로 다른 요구이기 때문이다. $M\ddot\theta$는 속도를 바꾸는 값, $c$는 모양이 변하는 중에 움직이고 있다는 것 자체의 값, $g$는 그저 중력에 맞서 존재하는 값이다.

**진자에는 셋 중 둘만 있다.** 질량 $m$, 길이 $l$, 연직에서의 각 $\theta$이면 $\tau = \underbrace{ml^2}_{M}\,\ddot\theta + \underbrace{mgl\sin\theta}_{g(\theta)}$다.

- $M = ml^2$는 관성이고, 상수다.
- $g(\theta) = mgl\sin\theta$는 중력 토크이고, 자세에 의존한다.
- 코리올리 항 $c$는 *0*이다. $M$이 $\theta$에 의존하지 않기 때문이다. (관성이 자세에 의존하는 1관절 계라면 $c = \tfrac12 M'(\theta)\dot\theta^2$가 남는다.)

링크를 하나 더 붙이면 $M$이 $\theta$ 의존이 되고 $c$가 켜진다 — 그것이 "한 방정식"에서 "다링크 동역학이 왜 어려운가"로 가는 도약 전부다. 위의 계산이 그 도약의 양쪽에 숫자를 붙였다. 곧게 편 자세와 카탈로그 자세 사이에서 $M_{11}$이 $5$에서 $3\ \mathrm{kg\,m^2}$으로 떨어지는데, 전완 질량이 어깨 축에 가까워지기 때문이고, 같은 어깨 가속도에 토크가 $40\,\%$ 덜 든다. 비대각 성분 $2$ 그리고 $1$은 결합이다. 한 관절을 가속하면 다른 관절이 밀린다. 진자에는 둘 다 없었다.

### 2. 질량 행렬의 정의

**질량 행렬** $M(\theta)$는 주어진 자세에서 관절 속도를 운동 에너지로 바꾸는 $n \times n$ 행렬이다. 로봇에 붙은 숫자가 아니라 *자세의 함수*인 행렬값 함수이고, 정의 조건이 셋이며 셋 다 성립해야 한다:

1. 운동 에너지를 이차형식으로 나타낸다, $\mathcal{K} = \tfrac12\dot\theta^\top M(\theta)\dot\theta$;
2. **대칭**이다, $M = M^\top$;
3. **양정부호**다, 0이 아닌 모든 $\dot\theta$에 대해 $\dot\theta^\top M\dot\theta > 0$ ([[02-foundations/linear-algebra|1. 선형대수 §3]]).

$$\mathcal{K}(\theta, \dot\theta) = \tfrac12\,\dot\theta^\top M(\theta)\,\dot\theta$$

여기서 $\dot\theta \in \mathbb{R}^n$은 관절 속도, $M(\theta) \in \mathbb{R}^{n\times n}$은 그 자세의 질량 행렬, $\mathcal{K}$는 팔 전체의 운동 에너지(줄)다. 3번은 모형화의 편의가 아니다. 움직이는 팔의 운동 에너지는 0이거나 음수일 수 없으므로, 이 이차형식은 스칼라의 $x^2$과 정확히 같게 행동한다. 양정부호성은 $M^{-1}$의 존재도 보장하고, 그것이 모든 자세에서 순동역학이 풀린다는 뜻이다.

- **예**: 2단계의 P2 $M(\theta_2)$, 카탈로그 자세에서 $M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$. 보기만 해도 대칭이고, 고윳값 $2 \pm \sqrt2$가 둘 다 양수라 양정부호이며, $\tfrac12(1,-1)M(1,-1)^\top = 1\,\mathrm{J}$이 5단계 운동의 운동 에너지로 요구대로 양수다.
- **반례**: 같은 자세에서 카탈로그가 함께 적어 둔 작업 공간 관성 $\Lambda = (JM^{-1}J^\top)^{-1} = \mathrm{diag}(1,2)$. 이것도 대칭이고 양정부호지만 질량 행렬이 *아니다*. **말단**이 작업 좌표에서 느끼는 관성이라 성분의 단위가 $\mathrm{kg\,m^2}$이 아니라 킬로그램이고, 관절마다가 아니라 과제 방향마다 하나씩이다. $\Lambda$에서 "팔이 $y$에서 두 배 무겁다"를 읽고 나서 그 $\Lambda$를 $\tau = M\ddot\theta + \ldots$에 대입하는 것이, 이 페이지의 대상이 10번 페이지의 대상과 섞이는 표준적인 방식이다.
- **왜 중요한가**: $M$은 시뮬레이터가 매 스텝 역행렬을 구하는 대상이고, 계산 토크 제어기가 곱하는 대상이며, 한 자세에서 맞던 이득이 다른 자세에서 깨지는 이유다. $M$이 항등행렬인 셈 치고 설계한 제어기는 존재하지 않는 로봇을 위해 설계한 것이다. 기어 달린 모터도 $M$에 보탠다. 회전자의 반사 관성 $n^2J_m$이고, [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §4]]의 고정 구동계를 감속비 100으로 달면 P2의 팔꿈치에서 이미 링크 자신의 것과 같다.

### 3. 순동역학과 역동역학, 그리고 유도 두 가지

**유도는 둘, 답은 하나.** **라그랑주** 경로는 에너지 기반이다. $\mathcal{K}$와 $U$를 쓰고 미분하면 세 항이 떨어져 나오는데, 위의 계산이 한 일이 정확히 그것이다. **재귀 뉴턴–오일러** 경로는 힘 평형이다. 바깥쪽으로 훑어 속도와 가속도를, 안쪽으로 훑어 힘을 구하고, $M$을 명시적으로 만들지 않아 $O(n)$이다. 시뮬레이터와 제어기가 실제로 돌리는 쪽이 이것이다. 두 경로는 모든 숫자에서 일치하고, 무엇에 편한가에서만 다르다.

**순동역학**($\tau \to \ddot\theta$)은 가속도에 대해 푼 방정식 $\ddot\theta = M^{-1}(\tau - c - g)$이고, 시뮬레이터가 매 스텝 적분하는 것이다. 모든 물리 엔진(Isaac, MuJoCo)이 이 방정식 + 접촉이다. **역동역학**($\ddot\theta \to \tau$)은 같은 방정식을 왼쪽에서 오른쪽으로 계산한 것이고, 제어기가 피드포워드로 공급하는 것이다([[04-robotics/modern-robotics/ch11-robot-control|11장]]). 계산의 5단계와 6단계가 같은 상태를 양방향으로 읽은 것이며, 여기 방정식이 하나뿐임을 보는 가장 싼 방법이다.

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

Tier B. [[02-foundations/lab-plants|0.6]]의 같은 장치 **P2**, 같은 질량, 같은 연직 평면. 다만 팔을 **곧게 편다**. 자세는 이제 $\theta = (0^\circ, 0^\circ)$, 두 링크 모두 $+\hat x$, 질량은 $(1,0)$과 $(2,0)$이다. 모든 숫자를 위 계산의 식에서 유도하라. $\Lambda$는 다시 구하지 마라. 그 랩은 [[02-foundations/manipulator-kinematics-dynamics|10]]이다.

1. **그리기.** 위의 그림에서 곧게 편 자세를 주 그림으로 올린다. 질량 둘, 무게 화살표 둘, 그리고 어깨에서의 수평 모멘트 팔이 이제 $1\,\mathrm{m}$과 $2\,\mathrm{m}$. 카탈로그 자세는 얇은 둘째 벌로 남기고, $\tau = M\ddot\theta + c + g$의 세 항 중 어느 자세가 어느 항을 크게 만드는지 그림 위에 표시하라.
2. **유도.** (a) $M(\theta_2)$에서 이 자세의 $M$, 그리고 $\det M$, $M^{-1}$, 고윳값 둘. (b) 이 자세의 $g$. (c) $\dot\theta = (1,-1)$의 $c$, 그다음 더 강한 주장으로 여기서는 *모든* $\dot\theta$에 대해 $c = 0$임을 보이고, 주어진 $\dot\theta$에 대해 $c$를 최대로 만드는 자세를 이 가족 안에서 지목하라. (d) $\tau = g + (1, 0)\,\mathrm{N\,m}$을 명령하고(중력 보상에 어깨에만 1뉴턴미터) $\ddot\theta$를 구하라.
3. **해석.** 같은 추가 토크 $(1,0)\,\mathrm{N\,m}$은 카탈로그 자세에서 $\ddot\theta = (0.5, -0.5)$를 준다. 팔을 곧게 편 것이 어깨의 반응과 엘보의 기생 가속도를 둘 다 바꾼 셈이다. 어느 쪽이 더 크게 바뀌었는가? 그리고 고정된 관절 이득 한 쌍이 두 자세 모두에서 옳을 수 없는 이유를 한 문장으로 쓰라.

> [!note]- 그리는 법 · How to draw it
> - 두 자세를 같은 축 위에 그린다. 주 자세는 실선, 다른 자세는 얇게. 어깨 축은 원점, 중력은 $-\hat y$ 방향이다.
> - 각 링크 말단의 점질량 자리에 속을 채운 원을 찍고, 각각에서 $9.81\,\mathrm{N}$ 무게 화살표를 곧장 아래로 내린다. 질량 둘, 화살표 둘, 길이는 같다.
> - 어깨 축에서 각 질량까지 수평 점선을 긋고 길이를 적는다. 엘보 축에서는 질량 2까지 하나. 이 길이들이 중력 계산의 전부다.
> - 모멘트 팔을 확인한다. 링크 길이가 아니라 축에서 질량까지의 수평 거리다. 축 바로 위의 질량은 그 축에 대한 팔이 $0$이다. 위의 그림에서는 전완 질량이 엘보 바로 위에 있어 어깨에서의 두 팔이 모두 $1\,\mathrm{m}$다.
> - 굽은 토크 화살표 둘, 베이스의 $\tau_1$과 엘보의 $\tau_2$.
> - 그림 옆에 $\tau = M(\theta)\ddot\theta + c(\theta,\dot\theta) + g(\theta)$를 적고 팔이 정지했을 때 남는 항에 동그라미를 친다. 둘째 줄에는 같은 자세를 지나가며 움직일 때 남는 항에 동그라미를 친다. 두 동그라미의 차이가 이 장의 존재 이유다.

> [!tip]- 정답
> 1. 곧게 편 자세: 모멘트 팔이 $1$과 $2\,\mathrm{m}$라 중력이 훨씬 크고, 질량 행렬도 크며, 코리올리 항은 더 작다(0이다). $c$를 최대로 만드는 쪽은 카탈로그 자세다.
> 2. (a) $\cos 0^\circ = 1$이므로 $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$, $\det M = 5 - 4 = 1$, $M^{-1} = \begin{pmatrix}1&-2\\-2&5\end{pmatrix}$, 고윳값 $3 \pm 2\sqrt2 = 5.8284$와 $0.1716\ \mathrm{kg\,m^2}$. 여전히 양정부호지만 조건비가 카탈로그 자세의 $5.83$에 대해 $34.0$이다. (b) $g = (9.81(2 + 1),\ 9.81) = (29.43,\ 9.81)\,\mathrm{N\,m}$. 어깨 토크가 카탈로그 값의 $1.5$배이고, 엘보는 이제 자기 질량을 0이 아니라 1미터에서 든다. (c) $\sin 0^\circ = 0$이므로 $c$의 두 성분 모두 0을 인수로 가져 $c = (0,0)$이다. $\dot\theta = (1,-1)$에서도, 다른 어떤 $\dot\theta$에서도 그렇다. $\sin\theta_2$가 벡터 전체에 곱해지기 때문이다. 최대는 $|\sin\theta_2| = 1$, 즉 $\theta_2 = \pm 90^\circ$인 카탈로그 자세다. (d) $\ddot\theta = M^{-1}(1,0)^\top = (1,\ -2)\,\mathrm{rad/s^2}$.
> 3. 어깨 반응은 두 배가 되었고($0.5 \to 1$) 엘보의 기생 가속도는 네 배가 되었으므로($-0.5 \to -2$) 결합 쪽이 더 크게 바뀌었다. 두 배 대 네 배다. 따라서 고정된 이득 쌍은 한 관성에 맞춰 조율해 놓고 다른 관성을 만난다. 작업 영역 끝에서는 같은 명령 토크가 어깨 가속도를 두 배로, 요청하지도 않은 엘보 가속도를 네 배로 만든다. 요행을 바라는 대신 $M(\theta)$를 곱해야 한다는 논거이고, [[04-robotics/modern-robotics/ch11-robot-control|11장]]이 계산 토크로 시작하는 이유다.
