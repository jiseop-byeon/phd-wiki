---
title: 10. Manipulator Kinematics & Dynamics
tags: [foundations, robotics, manipulation]
study-depth: Mastery
wiki-support: Working
depth-goal: "Read, write, and manipulate the manipulator equation on plant P2; convert between joint-space and task-space dynamics; complete this page's problem set from the wiki; predict how a configuration changes what a controller feels."
mastery-when: "This page is on the manipulation track's critical path — Mastery here is the prerequisite for defending any force-control or contact-rich manipulation claim."
---

> [!abstract] Depth target · 깊이 목표
> **Mastery** — the manipulator equation and the operational-space bridge are the closest
> dependency of contact-rich manipulation, so this is one of the few pages the
> [[07-research-program/index|research program]] promotes past Working. The page itself
> gets you to Working; Mastery needs the textbook and a simulator, named in §8.
> **Mastery** — 매니퓰레이터 방정식과 작업공간(operational space)으로 잇는 다리는 접촉이 많은 조작의 가장 가까운 의존
> 층이므로, [[07-research-program/index|연구 프로그램]]이 Working 위로 올리는 몇 안 되는
> 페이지다. 이 페이지 자체는 Working까지 데려다주고, Mastery는 §8의 교재와 시뮬레이터가 필요하다.

> [!note] Prerequisites · 선수 지식
> Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled; the $J$ and $M$ are frozen there), matrix inverses and positive definiteness ([[02-foundations/linear-algebra|1. Linear Algebra §3]]), partial derivatives and the chain rule ([[02-foundations/calculus-backprop|2. Calculus §1–§2]]), and the mechanics a civil-engineering degree may have left thin — the mass–spring–damper with its natural frequency and damping ratio, work and energy, torque and moment of inertia, and the holding torque of statics ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §5–§8]]). Forward kinematics, the Jacobian and $\tau = J^\top\mathcal{F}$ are not assumed: §1 derives them for P2, and §3 builds the mass matrix from them.
> [[02-foundations/lab-plants|0.6]]의 장치 **P2**(*장치*는 제어에서 제어 대상인 시스템을 부르는 말이고, $J$와 $M$은 거기에 고정되어 있다), 역행렬과 양정치성([[02-foundations/linear-algebra|1. 선형대수 §3]]), 편미분과 연쇄 법칙([[02-foundations/calculus-backprop|2. 미적분 §1–§2]]), 그리고 토목 학위가 얇게 남겨 두었을 수 있는 역학 — 고유 진동수와 감쇠비를 가진 질량–스프링–댐퍼, 일과 에너지, 토크와 관성 모멘트, 정역학의 유지 토크([[02-foundations/basic-mechanics|0.6.1 기초 역학 §5–§8]]). 순기구학, 야코비안, $\tau = J^\top\mathcal{F}$는 전제하지 않는다. §1이 P2에 대해 유도하고, §3이 그것으로 질량 행렬을 만든다.

## English

*Stands on [[02-foundations/linear-algebra|1. Linear Algebra]] and the P2 catalog; the forward kinematics, Jacobian and $\tau=J^\top\mathcal{F}$ it needs are derived for P2 in §1, and the Modern Robotics chapter summaries ([[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]] and [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]]) teach them for any arm — read them alongside.
It adds the one piece of physics contact needs, and closes the track into [[04-robotics/force-compliance-control|13. Force & Compliance Control]].*

This page does **not** teach forward kinematics, inverse kinematics, or the Jacobian in general —
the *Modern Robotics* chapter summaries do that, with worked 2R examples, and §1 derives only the P2 cases the dynamics needs.
It exists because those chapters stop at the place the manipulation track most needs to
continue: **dynamics**, and the equation that carries joint-space dynamics into the task
space where contact actually happens.

The whole page is really one question: *when a controller commands a motion or a force at
the end-effector, what does the arm's own mass do to that command?*

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]], this page is the mathematics floor right under the manipulation layer and the contact, force and tactile-feedback layer (its chip sits on the [[physical-ai-map|Physical AI Map]], on the dissertation path), and in *"install that panel on the frame"* it serves *move the component* — holding and accelerating an arm whose effective mass changes with its pose — and *perform the fitting*, where the tip's apparent mass decides what a push does; and through §2's torque residual — measured minus modelled torque — it gives the robot a way to *detect contact*. Without it a force controller is tuned blind: P2's shoulder needs $19.62\,\mathrm{N{\cdot}m}$ just to hold still, joint 1 is five times harder to accelerate with the arm straight than folded, and the tip feels $1\,\mathrm{kg}$ pushed sideways but $2\,\mathrm{kg}$ pushed up, so one impedance gain — the stiffness and damping a force controller gives the tip ([[04-robotics/force-compliance-control|13. §2]]) — behaves differently in each direction. Later pages build on this one section by section — [[04-robotics/force-compliance-control|13. Force & Compliance Control]] on this page's §2, §3, §6 and §8, [[04-robotics/capstone-panel-contact|26. Capstone]] on §6's apparent-mass matrix $\Lambda$ at the panel, [[04-robotics/actuators-drives|10.5 Actuators & Drives]] on §3, §5 and §6, and [[04-robotics/system-identification|5.5 System Identification]] on the parameters of §2 and §7 — and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) this page is block 1 itself, right after the [[02-foundations/overview#Gate check — are the foundations done?|foundations gate]], whose optional question 15 asks for its $\Lambda$; its task-space bridge feeds block 3, robotics 12, 13 and 15 — demonstrations, impedance and grasping. After it you can use the manipulator equation on P2 in both directions, compute $\Lambda$ from $J$ and $M$, and predict whether a contact will feel stiff or soft in a given direction.

> [!note] First pass · 처음이라면
> About three sessions of 60–90 minutes. **Session 1:** the Running object and the picture, §1 (the three kinematic facts, derived for P2), and §2 up to its three cases of holding, moving and touching. **Session 2:** §3, deriving the mass matrix by hand; §4, where fast motion couples the joints; and §5 through the gravity check. **Session 3:** §6 — where $\Lambda$ comes from, the worked 2R, the two consequences and the sweep — which is the reason this page is on the critical path; then self-checks 1–3, problem 2 and the optional question 15 of the [[02-foundations/overview#Gate check — are the foundations done?|gate check]]. §5's computed torque, §7 and every collapsed *Deeper* note are for when a paper's dynamics claims start to matter, and §8 is the checklist for reading one.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's planar two-link arm, now with its masses: links $L_1=L_2=1\,\mathrm m$, massless rods with a $1\,\mathrm{kg}$ point mass at the far end of each, joint angles measured from the $x$-axis and the elbow's relative to the first link. The page stands it in a **vertical plane**, so gravity $g=9.81\,\mathrm{m/s^2}$ acts along $-y$, and works at the catalog pose $\theta=(0^\circ,90^\circ)$ — upper arm horizontal, forearm straight up, tip at $(1,1)\,\mathrm m$ — where the catalog freezes $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ and $M=\begin{pmatrix}3&1\\1&1\end{pmatrix}$. §3 and §6 also move the elbow through $0^\circ$ to $180^\circ$, and the problem set to $45^\circ$.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 370" style="max-width:100%;height:auto" role="img" aria-label="P2 at elbow ninety degrees in a vertical plane: two one-kilogram point masses with their weights, shoulder torque 19.62 newton-metres from a one-metre moment arm and zero at the elbow, the contact force pair drawn on tip and panel separately, and the apparent-mass ellipse diag(1, 2) kg">
  <defs><marker id="aMk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <line x1="30" y1="30" x2="30" y2="76" stroke="currentColor" stroke-width="1.6" marker-end="url(#aMk)"/>
  <text x="40" y="50" font-size="11" fill="currentColor">g = 9.81 m/s²</text>
  <text x="40" y="64" font-size="11" fill="currentColor" fill-opacity="0.75">down is −y</text>
  <line x1="26" y1="306" x2="52" y2="306" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" marker-end="url(#aMk)"/>
  <line x1="26" y1="306" x2="26" y2="280" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" marker-end="url(#aMk)"/>
  <text x="56" y="310" font-size="11" fill="currentColor" fill-opacity="0.85">x</text>
  <text x="32" y="284" font-size="11" fill="currentColor" fill-opacity="0.85">y</text>
  <path d="M100 206 L89 222 L111 222 Z" stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.7" stroke-linejoin="round"/>
  <line x1="80" y1="222" x2="120" y2="222" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <line x1="82" y1="222" x2="76" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="91" y1="222" x2="85" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="100" y1="222" x2="94" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="109" y1="222" x2="103" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="118" y1="222" x2="112" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="100" y1="206" x2="250" y2="206" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <line x1="250" y1="206" x2="250" y2="56" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <circle cx="100" cy="206" r="6.5" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.0"/>
  <circle cx="250" cy="206" r="10" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="250" cy="206" r="5.5" stroke="none" fill="currentColor"/>
  <circle cx="250" cy="56" r="5.5" stroke="none" fill="currentColor"/>
  <text x="88" y="210" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">(0, 0)</text>
  <text x="250" y="42" font-size="11" fill="currentColor" text-anchor="middle">tip (1, 1)</text>
  <text x="238" y="60" font-size="11" fill="currentColor" text-anchor="end">1 kg</text>
  <text x="236" y="197" font-size="11" fill="currentColor" text-anchor="end">1 kg</text>
  <text x="236" y="230" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">elbow (1, 0)</text>
  <line x1="250" y1="212" x2="250" y2="255.1" stroke="currentColor" stroke-width="1.6" marker-end="url(#aMk)"/>
  <text x="258" y="253.1" font-size="11" fill="currentColor">9.81 N</text>
  <line x1="250" y1="62" x2="250" y2="105.1" stroke="currentColor" stroke-width="1.6" marker-end="url(#aMk)"/>
  <text x="258" y="97.1" font-size="11" fill="currentColor">9.81 N</text>
  <line x1="250" y1="108.1" x2="250" y2="196" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9" stroke-dasharray="2 3"/>
  <text x="240" y="112" font-size="11" fill="currentColor" text-anchor="end">elbow offset 0:</text>
  <text x="240" y="127" font-size="11" fill="currentColor" text-anchor="end">the tip's weight line</text>
  <text x="240" y="142" font-size="11" fill="currentColor" text-anchor="end">passes through its axis</text>
  <line x1="100" y1="232" x2="100" y2="287.1" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="250" y1="258.1" x2="250" y2="287.1" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="101" y1="281.1" x2="249" y2="281.1" stroke="currentColor" stroke-width="1.1"/>
  <path d="M108 277.6 L101 281.1 L108 284.6" stroke="currentColor" stroke-width="1.1" fill="none" stroke-linejoin="round"/>
  <path d="M242 277.6 L249 281.1 L242 284.6" stroke="currentColor" stroke-width="1.1" fill="none" stroke-linejoin="round"/>
  <text x="175" y="276.1" font-size="11" fill="currentColor" text-anchor="middle">1 m to both weight lines</text>
  <path d="M 124.4 197.1 A 26 26 0 0 0 75.6 197.1" stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aMk)"/>
  <text x="56" y="156" font-size="11" fill="currentColor">τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= 2 · 9.81 · 1</tspan></text>
  <text x="56" y="171" font-size="11" fill="currentColor">= 19.62 N·m</text>
  <path d="M 262.9 221.3 A 20 20 0 0 0 265.3 193.1" stroke="currentColor" stroke-width="1.3" fill="none" stroke-opacity="0.8" stroke-dasharray="3 3"/>
  <text x="275" y="202" font-size="11" fill="currentColor">τ<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= 0</tspan></text>
  <rect x="322" y="12" width="230" height="146" rx="4" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="276" y1="56" x2="320" y2="56" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="1 3"/>
  <text x="332" y="31" font-size="12" fill="currentColor">apparent mass at the tip</text>
  <ellipse cx="374" cy="98" rx="24" ry="48" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.1"/>
  <line x1="374" y1="98" x2="398" y2="98" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <line x1="374" y1="98" x2="374" y2="50" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="386" y="113" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <text x="370" y="78" font-size="11" fill="currentColor" text-anchor="end">2</text>
  <text x="418" y="64" font-size="12" fill="currentColor">Λ = diag(1, 2) kg</text>
  <text x="418" y="86" font-size="11" fill="currentColor">push sideways: 1 kg</text>
  <text x="418" y="102" font-size="11" fill="currentColor">push up: 2 kg</text>
  <text x="418" y="124" font-size="11" fill="currentColor" fill-opacity="0.8">an ellipse in kg,</text>
  <text x="418" y="139" font-size="11" fill="currentColor" fill-opacity="0.8">not in velocity</text>
  <rect x="322" y="170" width="230" height="150" rx="4" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="332" y="189" font-size="12" fill="currentColor">contact at the tip, drawn apart</text>
  <circle cx="440" cy="222" r="5.5" stroke="none" fill="currentColor"/>
  <text x="440" y="211" font-size="11" fill="currentColor" text-anchor="middle">tip</text>
  <line x1="380" y1="284" x2="500" y2="284" stroke="currentColor" stroke-width="1.6"/>
  <line x1="384" y1="284" x2="377" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="398" y1="284" x2="391" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="412" y1="284" x2="405" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="426" y1="284" x2="419" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="440" y1="284" x2="433" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="454" y1="284" x2="447" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="468" y1="284" x2="461" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="482" y1="284" x2="475" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="496" y1="284" x2="489" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="374" y="288" font-size="11" fill="currentColor" text-anchor="end">panel</text>
  <line x1="433" y1="239" x2="433" y2="283" stroke="currentColor" stroke-width="1.8" marker-end="url(#aMk)"/>
  <line x1="447" y1="278" x2="447" y2="234" stroke="currentColor" stroke-width="1.8" marker-end="url(#aMk)"/>
  <text x="425" y="244" font-size="11" fill="currentColor" text-anchor="end">commanded,</text>
  <text x="425" y="259" font-size="11" fill="currentColor" text-anchor="end">on the panel</text>
  <text x="425" y="274" font-size="11" fill="currentColor" text-anchor="end">(0, −10) N</text>
  <text x="455" y="244" font-size="11" fill="currentColor">reaction,</text>
  <text x="455" y="259" font-size="11" fill="currentColor">on the tip</text>
  <text x="455" y="274" font-size="11" fill="currentColor">(0, +10) N</text>
  <text x="332" y="308" font-size="11" fill="currentColor" fill-opacity="0.8">same length, opposite bodies</text>
  <text x="12" y="342" font-size="11" fill="currentColor" fill-opacity="0.85">● 1 kg point mass · ○ joint axis · rods massless · all force arrows to one scale</text>
  <text x="12" y="358" font-size="11" fill="currentColor" fill-opacity="0.85">A moment arm is a weight line's horizontal offset from the joint axis, not a link length.</text>
</svg>

Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at $\theta=(0^\circ,90^\circ)$, standing in a vertical plane so that gravity, $9.81\,\mathrm{m/s^2}$ along $-y$, is on the page: $1\,\mathrm{kg}$ point masses at the elbow $(1,0)$ and the tip $(1,1)$, each weighing $9.81\,\mathrm{N}$, both hang $1\,\mathrm{m}$ to the right of the shoulder axis, so $\tau_1=2\cdot9.81\cdot1=19.62\ \mathrm{N{\cdot}m}$, while the tip's weight line passes through the elbow axis and $\tau_2=0$. Drawn apart at the tip, the commanded $(0,-10)\,\mathrm{N}$ acts on the panel and its reaction $(0,+10)\,\mathrm{N}$ on the tip — same length, opposite bodies. The boxed ellipse is the apparent mass at the tip, $\Lambda=\mathrm{diag}(1,2)\ \mathrm{kg}$: the $2\,\mathrm{kg}$ arm feels like $1\,\mathrm{kg}$ pushed sideways and $2\,\mathrm{kg}$ pushed up — an ellipse in mass, not in velocity.

### 1. What kinematics already gave us

Dynamics has to know three things about the arm before it can say anything about force: where the tip is, how fast it moves when the joints turn, and what a push at the tip costs each joint. They are used constantly below, so they are stated in one place:

| Result | Statement | Source |
|---|---|---|
| Forward kinematics | joint angles $\theta \mapsto$ end-effector pose $T(\theta)$ | [[04-robotics/modern-robotics/ch04-forward-kinematics\|MR ch.4]] |
| Velocity kinematics | $v = J(\theta)\,\dot\theta$ — joint rates map to tip velocity | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR ch.5 §1]] |
| Statics duality | $\tau = J^\top(\theta)\,\mathcal{F}$ — the same matrix maps wrenches back to torques | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR ch.5 §3]] |

In the third row $\mathcal{F}$ is a **wrench**: the force the tip applies to its surroundings, together with the moment it applies in 3D — for planar P2 simply a force 2-vector in newtons, like the $(0,-10)\,\mathrm N$ pressed on the panel in the picture.

**For P2, all three take a few lines.** Write $\theta_{12}=\theta_1+\theta_2$, $c_1=\cos\theta_1$, $s_{12}=\sin\theta_{12}$ and so on. The elbow and the tip sit at
$$p_1=L_1\,(c_1,\ s_1),\qquad p_2=p_1+L_2\,(c_{12},\ s_{12})$$
which is the forward kinematics, since each link adds its length along its own absolute angle (P2's tool is at $p_2$). Differentiating in time with the chain rule gives $v=J(\theta)\,\dot\theta$, where the columns of $J=\partial p_2/\partial\theta$ are $\partial p_2/\partial\theta_1=(-L_1s_1-L_2s_{12},\ L_1c_1+L_2c_{12})$ and $\partial p_2/\partial\theta_2=(-L_2s_{12},\ L_2c_{12})$. At $\theta=(0°,90°)$ they are $(-1,1)$ and $(-1,0)$, the catalog's $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$. The duality follows from power. Set the arm's own mass aside for a moment (its inertia and weight become §2's $M$ and $g$): a massless arm stores no energy, so the power the motors put in, $\tau^\top\dot\theta$, equals the power the tip delivers, $\mathcal{F}^\top v=\mathcal{F}^\top J\dot\theta$, for every $\dot\theta$; hence $\tau=J^\top\mathcal{F}$. Pressing down with $\mathcal{F}=(0,-10)$ N at this pose takes $\tau=(-10,\ 0)$ N·m.

Everything on this page is what happens when you add **mass** to that picture.

The distinction matters because a reachable motion is not necessarily a motion the actuators can produce under load. For example, a pose solver can place a drywall sheet geometrically while ignoring the effort needed to accelerate and hold it. **The reading this gives you.** Identify whether a paper establishes pose feasibility, velocity feasibility, static support, or dynamic execution. Each adds a different condition; solving the earlier problem does not silently solve the later one.

### 2. The manipulator equation

*In one sentence:* the torque each joint motor must supply is what it takes to accelerate an arm whose effective mass changes with its pose, plus what the joints' motions do to one another, plus the arm's weight — and a contact adds a push of its own that no one commanded.

*If you need only one thing from this section:* the same equation runs both ways — $\tau = M\ddot\theta + C\dot\theta + g$ gives the torque a motion needs, and $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$ the motion a torque produces, at every pose since $M$ is always invertible; the end of the section works it on P2, which at $\theta=(0°,90°)$ with the motors off starts to fall at $\ddot\theta=(-9.81,\ 9.81)$ rad/s².

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau$$

This is the **equation of motion** of an $n$-joint rigid arm: $n$ coupled second-order differential equations, one torque balance per joint, so every term has units of torque (N·m for a revolute joint). $\theta \in \mathbb{R}^n$ holds the joint angles and $\dot\theta$, $\ddot\theta$ their velocities and accelerations; $M(\theta)$ and $C(\theta,\dot\theta)$ are $n \times n$ matrices; $g(\theta)$ and $\tau$ are $n$-vectors of torques. For the 2R arm below, $n = 2$.

**Where the shape comes from.** This is not three physical effects bolted together — it is
one derivative of one energy. Write the Lagrangian $L = T - V$ with kinetic energy
$T = \tfrac12\dot\theta^\top M(\theta)\dot\theta$ and potential $V(\theta)$, and apply
Lagrange's equation $\frac{d}{dt}\frac{\partial L}{\partial\dot\theta} - \frac{\partial L}{\partial\theta} = \tau$. It holds joint by joint, so the single scalar function $L$ generates all $n$ equations:
$$\frac{d}{dt}\frac{\partial L}{\partial \dot\theta_i} - \frac{\partial L}{\partial \theta_i} = \tau_i, \qquad i = 1, \dots, n$$
You do not need a mechanics course to trust it: it is Newton's second law rewritten in energy terms.
For one mass on a line, $L = \tfrac12 m\dot x^2 - V(x)$, so $\frac{d}{dt}\frac{\partial L}{\partial\dot x} = \frac{d}{dt}(m\dot x)$ is the rate of change of momentum and $\frac{\partial L}{\partial x} = -\partial V/\partial x$ is the force the energy landscape (gravity, say) exerts; the equation says momentum changes by the applied force plus that force, i.e. $m\ddot x = F - \partial V/\partial x$.
With joint angles in place of $x$ the same bookkeeping works, and [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8]] carries it out in full.
Back to the arm: the first term gives $\frac{d}{dt}\big(M\dot\theta\big) = M\ddot\theta + \dot M\dot\theta$;
the second contributes $-\frac{\partial T}{\partial\theta}$ and $\frac{\partial V}{\partial\theta}$.
Collect them: $M\ddot\theta$ is the first piece, the velocity-quadratic leftovers
$\dot M\dot\theta - \frac{\partial T}{\partial\theta}$ are what gets *named* $C(\theta,\dot\theta)\dot\theta$,
and $\frac{\partial V}{\partial\theta}$ is $g(\theta)$.

Two things follow that are worth more than the derivation itself. First, **$C$ exists only
because $M$ depends on $\theta$** — if the inertia matrix were constant, $\dot M = 0$ and
$\partial T/\partial\theta = 0$, and the Coriolis term would vanish outright. It is not an
extra force; it is the bookkeeping cost of a configuration-dependent mass. Second, $C$ is
**not unique**: only the product $C\dot\theta$ is determined, so different books write
different $C$ matrices for the same robot. Which one papers pick, and the energy identity their stability proofs rest on, need §4's $C$, so they are in the *Deeper* note at the end of §4.

Four terms, each with a distinct physical job:

- **$M(\theta)$ — the mass (inertia) matrix.** Symmetric and positive definite, so it is
  always invertible — which is why $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$ is always
  well defined. The essential fact is the argument: $M$ **depends on the configuration**.
  An arm is not a constant mass; it is a mass whose value changes as it moves.
  Both properties come from kinetic energy. Symmetric means $M = M^\top$. Positive definite means
$$\dot\theta^\top M(\theta)\,\dot\theta > 0 \quad \text{for every } \dot\theta \ne 0$$
  because $\tfrac12\dot\theta^\top M\dot\theta$ is the kinetic energy $T$, and any real motion of bodies with mass has positive kinetic energy ([[02-foundations/linear-algebra|1. Linear Algebra §3]]). For the 2R arm of §3, $M_{22} = 1 > 0$ and $\det M = 1 + \sin^2\theta_2 \ge 1$, so $M$ is positive definite at every configuration; at $\theta_2 = 90°$ the motion $\dot\theta = (1, -1)$ rad/s has $T = 1$ J. Non-example: $\begin{pmatrix}1&2\\2&1\end{pmatrix}$ is symmetric, but $\dot\theta = (1,-1)$ gives $\dot\theta^\top A\dot\theta = -2$, a negative "kinetic energy", so no physical arm has this mass matrix.
- **$C(\theta,\dot\theta)\,\dot\theta$ — Coriolis and centrifugal terms.** Quadratic in
  velocity. These are *not* friction. They are the coupling that makes one joint's motion
  exert torque on another, and they vanish at rest.
- **$g(\theta)$ — gravity.** Configuration-dependent, velocity-independent. The term a
  robot fights while holding still.
- **$\tau$ — joint torques**, what the motors actually command.

When the end-effector touches something, an external wrench $\mathcal{F}_{\text{ext}}$
enters through the statics duality:

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau + J^\top(\theta)\,\mathcal{F}_{\text{ext}}$$

That added term is the entire reason contact is a control problem rather than a planning
problem: the environment gets to inject torques the controller did not command.

**Use the equation in both directions.** In inverse dynamics, you specify a desired acceleration and compute the torque needed at the current position and velocity. In forward dynamics, you specify the torque and solve for the resulting acceleration. A simulator usually needs the latter; a model-based tracking controller often uses the former. The same equation serves both because the unknown changes. Written out,
$$\text{inverse: } \tau = M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta), \qquad \text{forward: } \ddot\theta = M(\theta)^{-1}\big(\tau - C(\theta,\dot\theta)\,\dot\theta - g(\theta)\big)$$
and the forward form exists at every state since $M$ is invertible. Example, using $M$ from §3 and $g$ from §5: the 2R arm at $\theta = (0°, 90°)$, at rest, with the motors switched off ($\tau = 0$) has $\ddot\theta = -M^{-1}g = (-9.81,\ 9.81)$ rad/s², so the shoulder starts to drop while $\theta_2$ grows just as fast: $\theta_1+\theta_2$ does not change at first, the forearm stays upright, and both masses start in free fall.

Start by holding the arm still without contact. Both velocity and acceleration vanish, so the ideal model requires $\tau=g(\theta)$. Next imagine motion at constant joint velocity: acceleration is zero but $C\dot\theta$ can remain, because geometry changes as the joints move. Finally add contact: the external wrench may support some of the load or oppose motion, depending on its sign and frame. Gravity compensation alone does not cancel an unknown contact force. These three cases let you check a dynamics implementation before attempting a long trajectory.

> [!question] Read a torque residual · 토크 잔차 읽기
> If measured torque differs from the model, is that necessarily contact? **Answer:** no. Friction, payload error, motor calibration and timing errors can also produce a residual. Inferring contact from torque requires accounting for these alternatives.

### 3. Worked example — the 2R arm's mass matrix

Take plant P2, the planar 2R arm of §1, with point masses at the end of each link:
$m_1 = m_2 = 1$ kg, $L_1 = L_2 = 1$ m. The mass matrix is, by definition, the matrix that writes the kinetic energy as
$T = \tfrac12\dot\theta^\top M(\theta)\dot\theta$, so build $T$ mass by mass, in three steps. (With the elbow locked, the same arm is one rigid body turning about the shoulder — a torque on a moment of inertia — in [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §7]].)

1. **Each mass's velocity Jacobian.** Differentiate each position of §1 in time. The elbow mass moves with $v_1=J_1\dot\theta$ and the tip mass with $v_2=J_2\dot\theta$, where
   $$J_1=\begin{pmatrix}-L_1s_1&0\\L_1c_1&0\end{pmatrix},\qquad J_2=\begin{pmatrix}-L_1s_1-L_2s_{12}&-L_2s_{12}\\L_1c_1+L_2c_{12}&L_2c_{12}\end{pmatrix}$$
   so $J_1$'s second column is zero, because turning the elbow does not move the elbow mass, and $J_2$ is §1's tip Jacobian.
2. **Add the kinetic energies.** A point mass has kinetic energy $\tfrac12 m\lVert v\rVert^2$ and nothing else, and $\lVert J\dot\theta\rVert^2=\dot\theta^\top J^\top J\,\dot\theta$, so
   $$T=\tfrac12\dot\theta^\top\big(m_1J_1^\top J_1+m_2J_2^\top J_2\big)\dot\theta \quad\Longrightarrow\quad M(\theta)=m_1J_1^\top J_1+m_2J_2^\top J_2$$
3. **Simplify.** $J_1^\top J_1=\mathrm{diag}(L_1^2,\ 0)$. In $J_2^\top J_2$ the $(1,1)$ entry is $(L_1s_1+L_2s_{12})^2+(L_1c_1+L_2c_{12})^2=L_1^2+L_2^2+2L_1L_2\,(c_1c_{12}+s_1s_{12})$, and $c_1c_{12}+s_1s_{12}=\cos(\theta_{12}-\theta_1)=\cos\theta_2$. The same identity makes the $(1,2)$ entry $L_2^2+L_1L_2\cos\theta_2$, and the $(2,2)$ entry is $L_2^2$. Adding the two masses:

$$M(\theta) = \begin{pmatrix} (m_1{+}m_2)L_1^2 + m_2L_2^2 + 2m_2L_1L_2\cos\theta_2 & m_2(L_2^2 + L_1L_2\cos\theta_2) \\ m_2(L_2^2 + L_1L_2\cos\theta_2) & m_2L_2^2 \end{pmatrix}$$

Check it at the catalog pose $\theta=(0°,90°)$: there $J_1=\begin{pmatrix}0&0\\1&0\end{pmatrix}$ and $J_2=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$, so $M=\mathrm{diag}(1,0)+\begin{pmatrix}2&1\\1&1\end{pmatrix}=\begin{pmatrix}3&1\\1&1\end{pmatrix}$, the catalog's $M$. The same matrix comes out of the Lagrangian route of §2, which [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8]] carries through on this arm; *Modern Robotics* ch.8 then handles links whose mass is spread out, where each link also carries rotational kinetic energy about its centre of mass.

Read the entries. A diagonal term is the effective inertia associated with one joint's
velocity while the other is held fixed; it can include the masses and inertias of several
downstream links, not only that joint's "own" link. The off-diagonal $\cos\theta_2$ term is
coupling, and it exists because link 2's mass moves when joint 1 turns — so the inertia one
joint feels depends on where the other joint is.

With the numbers above, substitute $m_1 = m_2 = 1$ and $L_1 = L_2 = 1$ and $M$ depends on $\theta_2$ alone:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

Evaluate at three configurations:

| $\theta_2$ | shape | $M_{11}$ | $M$ |
|---:|---|---:|---|
| $0°$ | straight out | $5$ | $\begin{pmatrix}5&2\\2&1\end{pmatrix}$ |
| $90°$ | elbow square | $3$ | $\begin{pmatrix}3&1\\1&1\end{pmatrix}$ |
| $180°$ | folded back | $1$ | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ |

The $M_{11}$ column has a one-line physical reading. Turning joint 1 alone swings each mass on a circle about the shoulder, so $M_{11}=m_1r_1^2+m_2r_2^2$ with $r$ each mass's distance from joint 1. The elbow mass is always $1$ m out and the tip mass is $2$, $\sqrt2$ and $0$ m out in the three poses, which gives $1+4=5$, $1+2=3$ and $1+0=1$.

<svg viewBox="0 0 560 200" style="max-width:100%;height:auto" role="img" aria-label="the same two-link arm at three elbow angles: the tip mass 2, root 2 and 0 metres from the shoulder, so joint-one inertia falls from five to three to one">
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">
    <line x1="60" y1="120" x2="100" y2="120"/><line x1="100" y1="120" x2="140" y2="120"/>
    <line x1="240" y1="120" x2="280" y2="120"/><line x1="280" y1="120" x2="280" y2="80"/>
    <line x1="420" y1="120" x2="460" y2="120"/><line x1="460" y1="134" x2="420" y2="134"/>
    <path d="M 466 120 A 8 8 0 0 1 466 134" stroke-width="1.1" opacity="0.6"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" fill="none" opacity="0.8">
    <line x1="60" y1="104" x2="140" y2="104"/><line x1="60" y1="99" x2="60" y2="109"/><line x1="140" y1="99" x2="140" y2="109"/>
    <line x1="240" y1="120" x2="280" y2="80"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="120" r="4.5"/><circle cx="100" cy="120" r="4"/><circle cx="140" cy="120" r="5" fill-opacity="0.55"/>
    <circle cx="240" cy="120" r="4.5"/><circle cx="280" cy="120" r="4"/><circle cx="280" cy="80" r="5" fill-opacity="0.55"/>
    <circle cx="420" cy="120" r="4.5"/><circle cx="460" cy="120" r="4"/><circle cx="420" cy="134" r="5" fill-opacity="0.55"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="50">θ<tspan dy="3.5">2</tspan><tspan dx="3" dy="-3.5">= 0° · straight</tspan></text>
    <text x="280" y="50">θ<tspan dy="3.5">2</tspan><tspan dx="3" dy="-3.5">= 90°</tspan></text>
    <text x="460" y="50">θ<tspan dy="3.5">2</tspan><tspan dx="3" dy="-3.5">= 180° · folded</tspan></text>
    <text x="460" y="68" font-size="10.5" opacity="0.75">drawn offset; the links overlap</text>
    <text x="100" y="96">r = 2 m</text>
    <text x="248" y="92" text-anchor="end">r = √2 m</text>
    <text x="400" y="138" text-anchor="end">r = 0</text>
    <text x="100" y="160" font-size="12">M<tspan dy="3.5">11</tspan><tspan dx="3" dy="-3.5">= 1 + 2² = 5</tspan></text>
    <text x="280" y="160" font-size="12">M<tspan dy="3.5">11</tspan><tspan dx="3" dy="-3.5">= 1 + (√2)² = 3</tspan></text>
    <text x="460" y="160" font-size="12">M<tspan dy="3.5">11</tspan><tspan dx="3" dy="-3.5">= 1 + 0² = 1</tspan></text>
  </g>
</svg>

The same arm at three elbow angles. Turning joint 1 alone swings each $1\,\mathrm{kg}$ mass on a circle about the shoulder, so $M_{11}=m_1r_1^2+m_2r_2^2$: the elbow mass is always $r_1=1\,\mathrm m$ out and the tip mass $r_2=2$, $\sqrt2$ and $0\,\mathrm m$, giving $5$, $3$ and $1$ — with the same $2\,\mathrm{kg}$ of metal, joint 1 is five times harder to accelerate straight out than folded.

The number to carry away is that **ratio of five**. The inertia a joint controller fights
is not a property of the robot; it is a property of the robot's current pose. A gain that
is well tuned with the arm folded is badly detuned with the arm extended — which is the
first reason independent-joint PID is a compromise rather than a solution.

### 4. Coriolis and centrifugal terms — why fast motion couples the joints

Swing one joint fast and another feels a torque, though nothing touches the arm — which is why a controller tuned at low speed misbehaves at high speed. This section names those velocity terms, puts P2's numbers in them, and shows that they are nothing more exotic than the pull of a whirling mass.

For this arm, writing $h = -m_2L_1L_2\sin\theta_2$, the velocity-quadratic term is

$$C(\theta,\dot\theta)\,\dot\theta = \begin{pmatrix} h\,\dot\theta_2^2 + 2h\,\dot\theta_1\dot\theta_2 \\ -h\,\dot\theta_1^2 \end{pmatrix}$$

**Which terms are which, and where $C$ comes from.** In row $i$, a term in a single joint's speed squared, $\dot\theta_j^2$, is **centrifugal**; a term in a product $\dot\theta_j\dot\theta_k$ with $j \ne k$ is **Coriolis**. Above, $h\,\dot\theta_2^2$ and $-h\,\dot\theta_1^2$ are centrifugal and $2h\,\dot\theta_1\dot\theta_2$ is Coriolis. The standard $C$, the one that makes $\dot M - 2C$ skew-symmetric, is built from derivatives of $M$ through the *Christoffel symbols* $c_{ijk}$:
$$c_{ijk} = \tfrac12\left(\frac{\partial M_{ij}}{\partial\theta_k} + \frac{\partial M_{ik}}{\partial\theta_j} - \frac{\partial M_{jk}}{\partial\theta_i}\right), \qquad C_{ij}(\theta,\dot\theta) = \sum_{k=1}^{n} c_{ijk}\,\dot\theta_k$$
so a constant $M$ gives $C = 0$, as §2 said. For the 2R arm only $M_{11}$ and $M_{12}$ vary, with $\partial M_{11}/\partial\theta_2 = 2h$ and $\partial M_{12}/\partial\theta_2 = h$. Substituting reproduces the vector above, and $\dot M - 2C = \begin{pmatrix}0 & -h(2\dot\theta_1 + \dot\theta_2)\\ h(2\dot\theta_1 + \dot\theta_2) & 0\end{pmatrix}$, skew-symmetric as promised.

Put in numbers. At $\theta_2 = 90°$, $h = -1\cdot1\cdot1\cdot\sin 90° = -1$. Suppose joint 1
is commanded to **hold still** ($\dot\theta_1 = 0$) while joint 2 swings at
$\dot\theta_2 = 2$ rad/s. The first row gives

$$h\,\dot\theta_2^2 = (-1)(2)^2 = -4 \ \text{N}\cdot\text{m}$$

With joint 2 swinging at a constant rate ($\ddot\theta_2 = 0$), joint 1 must supply an extra $-4$ N·m *just to stay where it is*, on top of whatever gravity needs (§5 computes that part). Nothing is touching the robot;
this is the arm's own moving mass pushing back through the linkage. Double the speed and
it quadruples to $-16$ N·m, because the term is quadratic in velocity.

**The same $-4$ N·m as plain statics.** With joint 1 held, the tip mass moves on a circle of radius $L_2=1\,\mathrm m$ about the elbow at $2\,\mathrm{rad/s}$, so the forearm must pull it inward with the centripetal force $m_2\dot\theta_2^2L_2=1\cdot2^2\cdot1=4\,\mathrm N$. By Newton's third law ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §2]]) the mass pulls the elbow outward along the forearm with the same $4\,\mathrm N$ — straight up at this pose — and that force acts $1\,\mathrm m$ to the right of the shoulder, so its moment about joint 1 is $(1,0)\times(0,4)=+4\,\mathrm{N{\cdot}m}$ and joint 1 must supply $-4\,\mathrm{N{\cdot}m}$ to stay put. Joint 2 feels nothing, because the pull passes through its axis: the second row, $-h\dot\theta_1^2$, is zero.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="P2 at elbow ninety degrees with joint 2 swinging at 2 rad/s and joint 1 held: the tip mass moves on a circle about the elbow at 2 m/s, the forearm pulls it inward with 4 N, it pulls the elbow outward along the forearm with 4 N, that pull acts 1 m from the shoulder, so joint 1 must supply minus 4 newton-metres while joint 2 feels nothing">
  <defs><marker id="aCor" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <line x1="80.0" y1="222.0" x2="220.0" y2="222.0" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <line x1="220.0" y1="222.0" x2="220.0" y2="82.0" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <path d="M 263.3 88.9 A 140.0 140.0 0 0 0 103.9 143.7" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6" stroke-dasharray="4 4"/>
  <circle cx="80.0" cy="222.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="220.0" cy="222.0" r="10" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="220.0" cy="222.0" r="5.5" fill="currentColor"/>
  <circle cx="220.0" cy="82.0" r="5.5" fill="currentColor"/>
  <line x1="212.0" y1="82.0" x2="168.0" y2="82.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#aCor)"/>
  <text x="190.0" y="73.0" font-size="12" fill="currentColor" text-anchor="middle">v = 2 m/s</text>
  <line x1="228.0" y1="90.0" x2="228.0" y2="134.0" stroke="currentColor" stroke-width="2" marker-end="url(#aCor)"/>
  <text x="236.0" y="106.0" font-size="12" fill="currentColor">4 N on the tip mass,</text>
  <text x="236.0" y="121.0" font-size="12" fill="currentColor">inward, m ω² r = 1·2²·1</text>
  <line x1="228.0" y1="210.0" x2="228.0" y2="166.0" stroke="currentColor" stroke-width="2" marker-end="url(#aCor)"/>
  <text x="236.0" y="178.0" font-size="12" fill="currentColor">4 N on the elbow,</text>
  <text x="236.0" y="193.0" font-size="12" fill="currentColor">outward along the forearm</text>
  <line x1="80.0" y1="232.0" x2="80.0" y2="261.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="220.0" y1="234.0" x2="220.0" y2="261.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="81.0" y1="256.0" x2="219.0" y2="256.0" stroke="currentColor" stroke-width="1.1"/>
  <path d="M88.0 252.5 L81.0 256.0 L88.0 259.5" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <path d="M212.0 252.5 L219.0 256.0 L212.0 259.5" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="150.0" y="273.0" font-size="12" fill="currentColor" text-anchor="middle">1 m: the pull's lever arm about the shoulder</text>
  <path d="M 57.4 213.8 A 24.0 24.0 0 0 1 102.6 213.8" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#aCor)"/>
  <text x="22.0" y="172.0" font-size="12" fill="currentColor">τ<tspan dy="3" font-size="10">1</tspan><tspan dx="3" dy="-3">= −4 N·m</tspan></text>
  <text x="22.0" y="187.0" font-size="11" fill="currentColor" fill-opacity="0.85">holds joint 1 still</text>
  <text x="236.0" y="226.0" font-size="11" fill="currentColor" fill-opacity="0.85">τ₂ = 0: the pull passes through the elbow axis</text>
</svg>

Joint 2 swings at $2\,\mathrm{rad/s}$ while joint 1 is held: the tip mass moves on its circle about the elbow (dashed) at $2\,\mathrm{m/s}$, the forearm pulls it inward with $4\,\mathrm N$, and the reaction pulls the elbow outward with $4\,\mathrm N$ at a lever arm of $1\,\mathrm m$ about the shoulder. That $+4\,\mathrm{N{\cdot}m}$ is what $h\dot\theta_2^2=(-1)(2)^2=-4\,\mathrm{N{\cdot}m}$ cancels, and the pull passes through the elbow axis, so $\tau_2=0$.

This is the second reason independent-joint control degrades with speed, and it is why
papers that report good tracking at low speed are making a weaker claim than they appear
to: at low speed the hardest terms in the equation are nearly zero.

> [!note]- Deeper · 더 깊이
> **The skew-symmetry property, and the passivity step it buys.** Papers pick the factorization of $C$ that makes $\dot M - 2C$ skew-symmetric (a matrix $A$ with $A^\top = -A$, so $x^\top A x = 0$ for every $x$; see [[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §1]]) — for the 2R arm the Christoffel $C$ above, whose $\dot M-2C$ was checked skew-symmetric — because that identity is what most stability proofs use. Along any motion the kinetic energy changes at the rate $\frac{d}{dt}\big(\tfrac12\dot\theta^\top M\dot\theta\big)=\dot\theta^\top M\ddot\theta+\tfrac12\dot\theta^\top\dot M\dot\theta$, and substituting $M\ddot\theta=\tau-C\dot\theta-g$ from the manipulator equation gives
> $$\frac{d}{dt}\Big(\tfrac12\dot\theta^\top M\dot\theta\Big)=\dot\theta^\top(\tau-g)+\tfrac12\dot\theta^\top(\dot M-2C)\,\dot\theta=\dot\theta^\top(\tau-g)$$
> because the skew-symmetric middle term is zero. So the velocity terms do no work: kinetic energy changes only by the power of the motors and of gravity. A system that can store and dissipate energy but never create it is called **passive**, and this identity is the passivity step of a **Lyapunov** stability proof — an argument that an energy-like quantity can only fall, so the motion must settle. With the $C$ above, at $\theta=(0°,90°)$ and $\dot\theta=(1,2)$ rad/s, $\tfrac12\dot\theta^\top\dot M\dot\theta=-6$ and $\dot\theta^\top C\dot\theta=-6$, so the two cancel.

### 5. Gravity, inverse dynamics, and computed torque

An arm that nobody holds falls — P2 released at the catalog pose starts to drop at $9.81\,\mathrm{rad/s^2}$ (§2) — so much of a controller's torque goes into simply holding the arm up, and it gets that torque right only if it knows where the weight is. This section derives the holding torque from the potential energy, checks it against a free-body diagram, and then uses the whole equation to cancel the arm's own dynamics: computed torque.

Gravity comes from differentiating the potential energy (the holding torque as plain statics, a weight times its lever arm, is [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §8]]): entry $i$ of $g(\theta)$ is the rate at which potential energy grows as joint $i$ turns,
$$g(\theta) = \frac{\partial V}{\partial\theta}, \qquad V(\theta) = m_1 g L_1\sin\theta_1 + m_2 g\,(L_1\sin\theta_1 + L_2\sin\theta_{12})$$
where each term is a weight times its height above joint 1, with angles measured from the horizontal and $\theta_{12} = \theta_1 + \theta_2$, so differentiating gives, for the same arm
($g = 9.81$ m/s²):

$$g_1(\theta) = (m_1{+}m_2)\,g\,L_1\cos\theta_1 + m_2\,g\,L_2\cos\theta_{12}, \qquad g_2(\theta) = m_2\,g\,L_2\cos\theta_{12}$$

with $\theta_{12} = \theta_1 + \theta_2$. At $\theta = (0°, 90°)$ the forearm points
straight up, so $\cos\theta_{12} = 0$ and

$$g_1 = 2(9.81)(1) + 0 = 19.62\ \text{N}\cdot\text{m}, \qquad g_2 = 0$$

Check it physically: both masses sit one metre horizontally from joint 1, so the shoulder
carries $2 \times 9.81 \times 1$; the forearm mass is directly above joint 2, zero lever
arm, so the elbow carries nothing. The equation and the free-body diagram agree — always
do this check, because a sign error in $g(\theta)$ is the single most common dynamics bug.

Combine this with §4's example at the same pose: if the arm moves in this vertical plane and joint 2 swings at 2 rad/s, joint 1 needs gravity plus the Coriolis term, $19.62 - 4 = 15.62$ N·m, just to hold still.

Reading the manipulator equation **right to left** — given a desired motion, what torque
does it require? — is **inverse dynamics**, and it is the basis of model-based control:

$$\tau = M(\theta)\,\ddot\theta_{\text{des}} + C(\theta,\dot\theta)\,\dot\theta + g(\theta)$$

Add feedback on the error and you have **computed-torque control**: the model cancels the
arm's own nonlinearity, and a simple linear controller handles what the model got wrong.
That is the honest description of the method — its performance is exactly as good as the
parameters in §7, which is why it is rarely used raw on real hardware.

With tracking error $e = \theta_{\text{des}} - \theta$ and gain matrices $K_p$ and $K_d$, the controller is
$$\tau = M(\theta)\big(\ddot\theta_{\text{des}} + K_d\,\dot e + K_p\,e\big) + C(\theta,\dot\theta)\,\dot\theta + g(\theta)$$
Substituting it into the manipulator equation gives $M(\theta)(\ddot e + K_d\dot e + K_p e) = 0$, and since $M$ is invertible, $\ddot e + K_d\dot e + K_p e = 0$ when the model is exact: every joint becomes an independent linear mass-spring-damper, whatever the pose. Matching that error equation to the standard second-order form $\ddot e+2\zeta\omega_n\dot e+\omega_n^2e=0$ names the two numbers that describe its response ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §5]] defines both, with the three regimes): the **natural frequency** $\omega_n=\sqrt{K_p}$, how fast the error is pulled back, and the **damping ratio** $\zeta=K_d/(2\sqrt{K_p})$, whether it overshoots ($\zeta<1$ oscillates, $\zeta>1$ creeps back, and $\zeta=1$, called critically damped, is the fastest return without overshoot). With $K_p = 100$ and $K_d = 20$ per joint, $\omega_n=\sqrt{100} = 10$ rad/s and $\zeta=20/(2\sqrt{100}) = 1$, critically damped ([[04-robotics/control-theory-ce397|5. Control Theory §7]] designs such gains). Non-example: independent-joint PD, $\tau = K_p e + K_d\dot e$ with no model, leaves $M(\theta)$ in the closed loop, so §3's factor-of-five inertia change alters how fast and how damped its response is.

### 6. Operational-space dynamics — the bridge to force control

*In one sentence:* seen from the tool tip, the arm behaves like a mass that is heavier in some directions than in others and that changes as the arm moves, and that apparent mass decides how a push at the tip turns into motion.

*If you need only one thing from this section:* the operational-space inertia $\Lambda=(JM^{-1}J^\top)^{-1}$, which for P2 at $\theta=(0°,90°)$ is $\mathrm{diag}(1,2)$ kg — pushed sideways the tip feels like 1 kg and pushed up like 2 kg, although the arm carries 2 kg of mass; it is worked for the 2R arm right after the full task-space equation.

Everything so far lives in joint space. Contact does not: contact happens at the
end-effector, in task space. The transformation is the single most important equation on
this page.

Task space here means Khatib's *operational space* — coordinates of the end-effector pose — not the *workspace*, the volume the arm can reach.

**Where $\Lambda$ comes from: three maps in a row.** Hold the arm at rest and set gravity and the velocity terms aside for a moment. A tip force $\mathcal{F}$ becomes joint torque through $J^\top$ (§1), joint torque becomes joint acceleration through $M^{-1}$ (§2's forward dynamics), and $J$ carries that acceleration back to the tip; since at rest $\dot v=J\ddot\theta$ exactly,
$$\dot v = J\ddot\theta = J M^{-1} J^\top \mathcal{F}$$
so the product $JM^{-1}J^\top$ answers "how much tip acceleration does this force produce here?", and its inverse answers the reverse question — which force a tip acceleration takes, $\mathcal{F}=\Lambda\dot v$ — with the end-effector's effective mass

$$\Lambda(\theta) = \left(J(\theta)\,M^{-1}(\theta)\,J^\top(\theta)\right)^{-1}$$

$\Lambda$ is the **operational-space inertia matrix** — the mass the end-effector *appears*
to have, seen from outside, in each task-space direction. A task-space force command then
becomes joint torques by $\tau = J^\top \mathcal{F}$, which is why the statics duality from
MR ch.5 turns out to be the load-bearing result of the whole manipulation track.

**The full task-space equation, every term named.** Substituting $\tau = J^\top\mathcal{F}$ into the forward dynamics and using $\dot v = J\ddot\theta + \dot J\dot\theta$ gives, for a square invertible $J$,
$$\mathcal{F} = \Lambda(\theta)\,\dot v + \Lambda(\theta)\big(J M^{-1} C\,\dot\theta - \dot J\,\dot\theta\big) + \Lambda(\theta)\,J M^{-1} g(\theta)$$
where $v$ is the end-effector velocity, $\dot v$ its acceleration and $\mathcal{F}$ the force (wrench) applied at the tip. So a tip force has three jobs: accelerate the apparent mass $\Lambda$, cancel the velocity terms as seen at the tip, and hold up gravity as seen at the tip. This is MR's eq. 8.90, $\mathcal{F} = \Lambda\dot v + \eta$, with $\eta$ written out.

**Worked out for the 2R arm** at $\theta = (0°, 90°)$. From §1, the tip Jacobian there
is $J = \begin{pmatrix}-1 & -1\\ 1 & 0\end{pmatrix}$, and from §3,
$M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ with $\det M = 2$, so

$$M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}, \qquad JM^{-1} = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}$$

$$JM^{-1}J^\top = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}\begin{pmatrix}-1&1\\-1&0\end{pmatrix} = \begin{pmatrix}1&0\\0&0.5\end{pmatrix} \quad\Longrightarrow\quad \Lambda = \begin{pmatrix}1&0\\0&2\end{pmatrix}$$

The gravity term checks the same way. At rest here, $\Lambda J M^{-1} g = J^{-\top} g$, the tip force whose torques $J^\top\mathcal{F}$ equal $g = (19.62, 0)$ N·m from §5, which is $\mathcal{F} = (0,\ 19.62)$ N: straight up and equal to the arm's full 2 kg weight. That is right because the tip, like both masses, is 1 m horizontally from joint 1, and it is directly above joint 2, like the forearm mass.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="two ellipses at the same tip of P2 at elbow ninety degrees: the velocity ellipse of J J transpose with semi-axes 1.62 and 0.62 metres per second, its long axis tilted to minus 31.7 degrees, and the apparent-mass ellipse of Lambda, 1 kilogram sideways and 2 kilograms up, upright">
  <text x="150.0" y="24" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">velocity ellipse, J J<tspan dy="-5" font-size="10">T</tspan></text>
  <text x="150.0" y="42.0" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="middle">tip speed from unit joint speed</text>
  <ellipse cx="150.0" cy="128.0" rx="84.1" ry="32.1" transform="rotate(31.7 150.0 128.0)" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.4"/>
  <line x1="150.0" y1="128.0" x2="221.6" y2="172.2" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <line x1="150.0" y1="128.0" x2="166.9" y2="100.7" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="225.6" y="186.2" font-size="11" fill="currentColor">1.62 m/s</text>
  <text x="170.0" y="95.0" font-size="11" fill="currentColor">0.62 m/s</text>
  <line x1="50.0" y1="128.0" x2="250.0" y2="128.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <line x1="150.0" y1="54.0" x2="150.0" y2="218.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <circle cx="150.0" cy="128.0" r="3.5" fill="currentColor"/>
  <text x="150.0" y="232.0" font-size="11" fill="currentColor" text-anchor="middle">long axis at −31.7°</text>
  <text x="420.0" y="24" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">apparent-mass ellipse, Λ</text>
  <text x="420.0" y="42.0" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="middle">mass a push at the tip feels</text>
  <ellipse cx="420.0" cy="128.0" rx="38.0" ry="76.0" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.4"/>
  <line x1="420.0" y1="128.0" x2="458.0" y2="128.0" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <line x1="420.0" y1="128.0" x2="420.0" y2="52.0" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="462.0" y="146.0" font-size="11" fill="currentColor">1 kg sideways</text>
  <text x="448.0" y="62.0" font-size="11" fill="currentColor">2 kg up</text>
  <line x1="320.0" y1="128.0" x2="520.0" y2="128.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <line x1="420.0" y1="54.0" x2="420.0" y2="218.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <circle cx="420.0" cy="128.0" r="3.5" fill="currentColor"/>
  <text x="420.0" y="232.0" font-size="11" fill="currentColor" text-anchor="middle">upright</text>
  <text x="280" y="254" font-size="12" fill="currentColor" text-anchor="middle">same arm, same pose, same J: two different shapes, not one shape rescaled</text>
</svg>

The same tip at the same pose, drawn two ways. The velocity ellipse of $JJ^\top$ — the tip speeds that unit joint speed can produce — has semi-axes $1.62$ and $0.62\,\mathrm{m/s}$ with its long axis tilted to $-31.7^\circ$, while the apparent-mass ellipse of $\Lambda=\mathrm{diag}(1,2)$ is upright, $1\,\mathrm{kg}$ sideways and $2\,\mathrm{kg}$ up: two shapes, not one shape rescaled, because each assumes a different input (the *Deeper* note below compares three).

Read the result. The arm carries 2 kg of actual mass, but pushed sideways at the tip it
behaves like **1 kg**, and pushed vertically like **2 kg** — a factor of two, in the same
configuration, from geometry alone. Two consequences that the force-control literature
assumes you have absorbed:

- **Impact force is direction-dependent.** Striking a rigid surface at the same speed
  transfers twice the momentum in the heavy direction. A gripper that inserts safely
  along one axis can damage the part along another.
- **A single stiffness gain is never uniformly right.** The closed-loop behaviour of an
  impedance controller ([[04-robotics/force-compliance-control|13. Force & Compliance Control §2]]) depends on $\Lambda$, so identical gains give different effective
  dynamics in different directions and different poses.

**The sweep: the same arm at every elbow angle.** One pose says little about a controller that has to work across the whole workspace, so sweep the elbow. The loop below keeps $\theta_1=0$, builds $M$ from §3 and $J$ from §1 at each $\theta_2$, and prints $M_{11}$, $\det J$ and the two eigenvalues of $\Lambda$ — the apparent masses along the tip's lightest and heaviest directions.

```python
# P2's apparent mass at the tip across the elbow's range (theta1 = 0, arm in a vertical plane).
import numpy as np
print("theta2   M11  det J   Lambda eigenvalues (kg)")
for deg in range(10, 171, 20):
    q2 = np.radians(deg)
    c, s = np.cos(q2), np.sin(q2)
    M = np.array(((3 + 2*c, 1 + c), (1 + c, 1.0)))          # §3, m1 = m2 = 1 kg, L1 = L2 = 1 m
    J = np.array(((-s, -s), (1 + c, c)))                     # §1 at theta1 = 0
    Lam = np.linalg.inv(J @ np.linalg.inv(M) @ J.T)          # this section
    lo, hi = np.linalg.eigvalsh(Lam)
    print(f"{deg:6d} {M[0, 0]:5.2f} {np.linalg.det(J):6.3f} {lo:8.3f} {hi:8.3f}")
```

| $\theta_2$ (°) | $M_{11}$ | $\det J$ | lightest (kg) | heaviest (kg) |
|---:|---:|---:|---:|---:|
| 10 | 4.97 | 0.174 | 1.000 | 34.163 |
| 30 | 4.73 | 0.500 | 1.000 | 5.000 |
| 50 | 4.29 | 0.766 | 1.000 | 2.704 |
| 70 | 3.68 | 0.940 | 1.000 | 2.132 |
| 90 | 3.00 | 1.000 | 1.000 | 2.000 |
| 110 | 2.32 | 0.940 | 1.000 | 2.132 |
| 130 | 1.71 | 0.766 | 1.000 | 2.704 |
| 150 | 1.27 | 0.500 | 1.000 | 5.000 |
| 170 | 1.03 | 0.174 | 1.000 | 34.163 |

Three readings. The lightest direction always weighs exactly $1\,\mathrm{kg}$, the tip's own point mass: it moves with the tip whichever way the tip is pushed, and a push across the forearm only swings the forearm about the elbow, leaving the elbow mass still. Along the forearm the elbow mass must move too, $1/\lvert\sin\theta_2\rvert$ times as fast as the tip, so the heaviest direction weighs $1+1/\sin^2\theta_2$ kg: $2$ at $90^\circ$, $5$ at $30^\circ$ and $150^\circ$, $34.2$ at $10^\circ$ and $170^\circ$, without bound as $\det J=\sin\theta_2$ goes to zero. And $M_{11}$, joint 1's own inertia, falls steadily from about $5$ to about $1$ while $\Lambda$ is symmetric about $90^\circ$: the joint-space and the task-space pictures of one arm answer different questions. The Mastery test of §8 is in this table: push a contact along the heavy direction near a singularity and it meets a heavy tip, so it strikes harder.

> [!note]- Deeper · 더 깊이
> **Three matrices called "the ellipsoid".** The relationship to MR ch.5's manipulability ellipsoid is qualitative, not a matrix
> reciprocal. Three different matrices get called "the ellipsoid", and each assumes a different input:
>
> | Construction | Shape matrix | Input it assumes | Question it answers | 2R arm at $(0°, 90°)$ |
> |---|---|---|---|---|
> | Kinematic manipulability (MR ch.5) | $JJ^\top$ | unit joint-velocity norm | which tip velocities are easy to reach? | $\begin{pmatrix}2&-1\\-1&1\end{pmatrix}$ |
> | Operational inertia (this section) | $JM^{-1}J^\top$ | a task wrench, after dynamic compensation | how much tip acceleration does a tip force produce? | $\begin{pmatrix}1&0\\0&0.5\end{pmatrix}$ |
> | Dynamic acceleration ellipsoid | $JM^{-2}J^\top$ | unit **Euclidean joint-torque** norm | which tip accelerations can unit motor torque produce? | $\begin{pmatrix}1&0.5\\0.5&0.5\end{pmatrix}$ |
>
> The last column shows the point: at one pose the three matrices have different shapes, not just different scales. They coincide only
> under special inertia and metric choices. Near a singularity all three reveal a lost task
> direction, but do not call their axis lengths exact reciprocals without stating the norm.
>
> **When the inverse is safe.** These caveats protect you from inverting a matrix that is singular or nearly so and trusting the huge numbers that come out.
>
> The ordinary inverse requires a full-row-rank task Jacobian and a positive-definite joint inertia matrix. A configuration is **singular** when the Jacobian loses rank, so some tip velocity cannot be produced by any joint rates ([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §4]]); for an $m$-dimensional task,
> $$\operatorname{rank} J(\theta) < m$$
> For this 2R arm $\det J = L_1L_2\sin\theta_2$, so it is singular at $\theta_2 = 0°$ and $180°$ (straight or folded) and has $\det J = 1$ at the $90°$ pose used above. Near a singular configuration, inspect which task direction is lost instead of blindly inverting a poorly conditioned matrix. Reducing the task or using a regularized solve changes what can be commanded. It does not restore a physically unavailable direction. The acceleration map here also assumes the remaining terms have been accounted for. Differentiating a moving Jacobian introduces $\dot J\dot\theta$: since $\dot v = J\ddot\theta + \dot J\dot\theta$, the full task-space equation carries an extra velocity term $\Lambda\dot J\dot\theta$ next to the mapped Coriolis and gravity terms. It is zero when the arm is at rest, which is why the local reading above may drop it, but an operational-space controller tracking fast motion must include it in its model compensation.

### 7. Where the parameters come from — and the sim-to-real gap

Every symbol in §2 hides a number that someone had to measure: link masses, centres of
mass, inertia tensors, joint friction, motor constants, gear elasticity. The motor constants, and the rotor inertia a gearbox adds to $M$, are [[04-robotics/actuators-drives|10.5 Actuators & Drives]]. A 20% error at the far end is already enough to feel: make P2's tip mass $1.2\,\mathrm{kg}$ — a cable loom and a cover — and the $19.62\,\mathrm{N{\cdot}m}$ holding torque of §5 becomes $9.81\,(1+1.2)=21.58\,\mathrm{N{\cdot}m}$, a $2\,\mathrm{N{\cdot}m}$ error that a gravity-compensated arm shows as a steady sag. Three honest
observations:

1. **CAD values are wrong at the margins.** Cabling, covers, and the actual tool are
   rarely in the CAD model, and they are exactly what sits farthest from the joints, where
   they matter most.
2. **Friction is the worst-modelled term** and it is not in the ideal equation at all. Real
   controllers carry a friction model that is fitted, not derived. Where that fitting is named
   and its failure mode stated is
   [[05-construction-robotics/sim-to-real|Sim-to-Real §2]]: system identification fits simulator
   parameters to measured trajectories, and can overfit one machine and one operating condition.
3. **These parameter mismatches are one major dynamics-side source of the sim-to-real gap.**
   Perception, timing, interfaces, contact, actuators, and task distributions can also dominate.
   Use synchronized logs and ablations to isolate the first failing layer
   ([[06-research-practice/failure-analysis-system-evaluation|Failure Analysis & System Evaluation]]).

For construction manipulation there is a fourth: the **payload is unknown and large**.
A grasped panel or bolt changes $M(\theta)$ and $g(\theta)$ by an amount comparable to the
arm's own links, and unlike a factory setting you do not get to hard-code its mass. The arm can identify it from its own torques instead: they are linear in a few base inertial parameters, $\tau=Y\pi$, which is how [[04-robotics/system-identification|5.5 System Identification §9]] recovers a $3\,\mathrm{kg}$ payload by least squares.

### 8. Reading dynamics in a paper, and the path to Mastery

When a manipulation paper mentions dynamics, these are the questions that separate a real
claim from decoration:

- Is the controller **torque-level** or does it command positions to a vendor controller?
  For a position interface, evaluate compliance over the whole closed loop, including the
  inner loop's stiffness, bandwidth, delay, and the environment stiffness.
- Are $M$, $C$, $g$ **modelled, learned, or ignored**? "Gravity compensation" alone is a
  much weaker statement than full inverse dynamics.
- At what **speed** were the results collected? Section 4 says the hard terms are quadratic
  in velocity, so slow demonstrations hide model error.
- Is the **payload** in the model?

Reaching Mastery from here needs three things this page cannot give you:

| Need | Where |
|---|---|
| Full derivations (Lagrangian and Newton–Euler, recursive algorithms) | *Modern Robotics* ch.8, and [[04-robotics/modern-robotics-book\|the book guide]] |
| Task-space control theory | Khatib's operational-space formulation; then [[04-robotics/control-theory-ce397\|Control Theory]] |
| Hands-on parameter sense | any rigid-body dynamics simulator — change a link mass by 20% and watch a tuned controller degrade |

The Mastery test for this page: given an arm, a configuration, and a direction, predict
whether a contact will feel stiff or soft — and be right.

### After reading

- [ ] Write the manipulator equation from memory and say what each term does.
- [ ] Explain why $M$ has an argument, with the factor-of-five example.
- [ ] Compute $\Lambda$ from $J$ and $M$ and interpret the result physically.
- [ ] Tell the velocity ellipse of $JJ^\top$ from the apparent-mass ellipse of $\Lambda$ by the input each assumes (§6's figure; its *Deeper* note adds the unit-torque ellipse).
- [ ] Name the worst-modelled term in the manipulator equation (friction) and say why, and name two non-dynamics sources that can dominate the sim-to-real gap.

> [!tip] Going deeper · 더 깊이
> [*Modern Robotics*](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) ch.8 is the derivation this page compresses, and the task-space inertia of §6 is the book's §8.6 (eq. 8.90), where its chapter notes credit Khatib's operational-space formulation. Control built on it is §11.4.3 (task-space motion control with torque inputs); §11.3.3 is the kinematic, velocity-input version, and §11.6 is hybrid motion–force control, a different thing. Read ch.8 for the Newton–Euler recursion, which is how the manipulator equation is actually computed rather than how it is written. What the book does not give you is §7 — where the parameters come from, and why identified ones and CAD ones disagree — because that is an experimental question, not a derivation.

### Self-check

1. $M(\theta)$ is positive definite. Why does that matter for simulation?
2. The arm is at $\theta_2 = 0°$ (straight). Compute $M$, and $h$, and say what the
   Coriolis term does there.
3. At $\theta=(0°,90°)$ the apparent mass is 1 kg sideways and 2 kg vertically, but the
   arm weighs 2 kg. How can the apparent mass be *less* than the real mass?
4. A paper reports excellent force tracking with a position-controlled industrial arm and
   a wrist force sensor. What should you check?
5. A robot grasps a 3 kg panel. Which terms of the manipulator equation change?

> [!tip]- Answers
> 1. Positive definite implies invertible, so $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$ always has a unique solution — a simulator can always integrate forward one step. It also means the kinetic energy $\tfrac12\dot\theta^\top M\dot\theta$ is strictly positive for any nonzero motion, which is what makes energy-based stability arguments work.
> 2. $\cos 0° = 1$, so $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$. And $h = -\sin 0° = 0$, so the entire Coriolis/centrifugal term vanishes at this configuration regardless of speed. It is a genuine special case, not a general fact — swing the elbow off $0°$ or $180°$ and the coupling returns.
> 3. Because the tip is not rigidly attached to all of that mass — the arm can respond to a sideways push by rotating, so only part of the inertia resists. Apparent mass measures resistance *at the tip in one direction*, not the amount of metal. In the singular limit the opposite happens and $\Lambda$ grows without bound along the lost direction.
> 4. Whether the arm is actually torque-controlled underneath. With a stiff position-controlled inner loop, the force "control" is an outer loop commanding small positions, which is admittance control — measure the force, command a motion, the reverse causality of impedance control ([[04-robotics/force-compliance-control|13. §2]]) — with the vendor's stiffness in the way; it can work, but its stability depends on the environment being soft, and the claim should be tested against a rigid surface. See [[04-robotics/contact-force-tactile|Contact, Force & Tactile §5]].
> 5. $M(\theta)$ and $g(\theta)$ both change substantially, since the payload adds mass at the far end where the lever arm is longest, and $C$ changes with $M$. The panel more than doubles the moving mass in this example, so a controller tuned unloaded will be badly wrong loaded — the reason payload-aware or adaptive control matters in construction more than in a factory with a known part.

### Problem set · 과제

Tier A (dynamics half of **P2**: §6's sweep is the lab, and item 3 runs a variant of it; the velocity loop is on [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5]] — do not start a second time-stepper here). Numbers frozen in [[02-foundations/lab-plants|0.6]]: at $\theta=(0^\circ,90^\circ)$,

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix},\quad M=\begin{pmatrix}3&1\\1&1\end{pmatrix},\quad \Lambda=\mathrm{diag}(1,2),\quad g=(19.62,\ 0)\,\mathrm{N{\cdot}m}$$

Items 1 and 2 move the elbow to $45^\circ$, where nothing is catalogued: check each formula first by getting these numbers back at $90^\circ$.

1. **Draw.** The picture above with the elbow opened to $\theta=(0^\circ,45^\circ)$, still in the vertical plane with $g$ in $-y$: both point masses with their weight arrows, the horizontal moment arm from each joint to each weight line, $g(\theta)$ as shoulder and elbow torques, and a panel force of $10\,\mathrm{N}$ *on the panel* in $-y$ under the tip. Write Newton's third law for the force *on the tip*. Which torque that is $0$ in the picture above is not $0$ here?
2. **Derive.** At rest at item 1's pose, $\theta=(0^\circ,45^\circ)$. (a) Build $J$ from §1 and $M$ from §3 there. (b) The holding torque $g(\theta)$ of §5, and the torque while commanding $F_\text{cmd}=(0,-10)\,\mathrm{N}$ on the panel, $\tau=g+J^\top F_\text{cmd}$. Which joint does the push almost relieve, and why? (c) $\Lambda=(JM^{-1}J^\top)^{-1}$, its two eigenvalues and the directions they belong to. (d) The tip wrench that produces $\dot v=(0,1)\,\mathrm{m/s}^2$ with the velocity terms zero, $\mathcal{F}=\Lambda\dot v$, and its joint torques $J^\top\mathcal{F}$. Why does a straight-up acceleration need a force that is not straight up?
3. **Do.** Clamp a $1\,\mathrm{kg}$ tool at the tip, so the tip mass becomes $m_2=2\,\mathrm{kg}$. Fill `?` in the template — the loaded mass matrix of §3 and $\Lambda$ of §6 — and run the sweep. Report $\Lambda$'s two eigenvalues at $90^\circ$, how much the tool added along each direction and why, and whether the loaded arm's heavy direction still grows without bound toward $0^\circ$ and $180^\circ$.

```python
# Loaded P2: a 1 kg tool at the tip, so m2 = 2 kg. Fill ?, then run.
import numpy as np
m1, m2 = 1.0, 2.0
print("theta2   M11   Lambda eigenvalues (kg)")
for deg in range(10, 171, 20):
    q2 = np.radians(deg)
    c, s = np.cos(q2), np.sin(q2)
    M = ?                                    # §3's mass matrix with m1, m2 and L1 = L2 = 1
    J = np.array(((-s, -s), (1 + c, c)))     # §1 at theta1 = 0, unchanged by the tool
    Lam = ?                                  # §6
    lo, hi = np.linalg.eigvalsh(Lam)
    print(f"{deg:6d} {M[0, 0]:5.2f} {lo:8.3f} {hi:8.3f}")
```

> [!note]- How to draw it · 그리는 법
> - The arm to scale in the vertical plane: base at the origin, link 1 along $+x$ to the elbow at $(1,0)$, link 2 at $45^\circ$ up and out to the tip at $(1.707,\ 0.707)$, and a gravity arrow along $-y$ in the margin so the page has an unambiguous down.
> - Links as massless rods, with a filled $1\,\mathrm{kg}$ dot at the *distal end* of each and a $9.81\,\mathrm{N}$ weight arrow straight down from it: the catalog's point-mass convention is what makes every number come out, and a mass drawn at a link's centre gives a different arm.
> - For each joint, draw and label the horizontal distance from its axis to each weight line: those offsets, not the link lengths, are the moment arms. The tip's weight line no longer passes through the elbow axis, and the gap between them is the new number.
> - Write the gravity torques as curved arrows at the joints, both with values: the elbow's is what the picture above had as $0$.
> - The panel as a horizontal surface under the tip (the forearm passes in front of it, out of the drawing plane, so only the tip touches it); the commanded force as a down arrow *onto the panel*, and its reaction as an up arrow of the same length *onto the tip*, offset so the two read as a pair and not one arrow drawn twice.
> - Label which body each force acts on: nearly every sign error later in the track is this pair, and it does not change with the pose.
> - If you add the apparent-mass ellipse, draw item 2's at the tip: semi-axes of $1$ and $3\,\mathrm{kg}$, the short one across the forearm and the long one along it, so at this pose the ellipse leans at $45^\circ$ with the forearm instead of standing upright as in the picture above. It is not the manipulability ellipse of [[02-foundations/linear-algebra|1. Linear Algebra §4.5]] — that one lives in velocity, this one in mass, and §6 draws the two side by side at the frozen pose.

> [!tip]- Solutions
> 1. Elbow at $(1,0)$, tip at $(1+\cos45^\circ,\ \sin45^\circ)=(1.707,\ 0.707)$, masses at those two points. Moment arms: about the shoulder, $1$ m to the elbow mass and $1.707$ m to the tip mass; about the elbow, $0.707$ m to the tip mass. Holding torques $g(\theta)=(9.81(1+1.707),\ 9.81\times0.707)=(26.56,\ 6.94)\,\mathrm{N{\cdot}m}$. The elbow torque, $0$ at the frozen pose because the tip hung straight above the elbow, is now $6.94\,\mathrm{N{\cdot}m}$: the forearm leans out and its weight line leaves the elbow axis. Force on the panel $(0,-10)$ $\Rightarrow$ force on the tip $(0,+10)$, the same pair as before, because Newton's third law does not depend on the pose.
> 2. (a) With $c=s=0.707$: $J=\begin{pmatrix}-0.707&-0.707\\1.707&0.707\end{pmatrix}$, $\det J=\sin45^\circ=0.707$, and $M=\begin{pmatrix}4.414&1.707\\1.707&1\end{pmatrix}$, $\det M=1+\sin^2 45^\circ=1.5$. (b) $g=(26.56,\ 6.94)\,\mathrm{N{\cdot}m}$, item 1's torques. $J^\top F_\text{cmd}=(-17.07,\ -7.07)$, so $\tau=(9.49,\ -0.13)\,\mathrm{N{\cdot}m}$: the push almost relieves the elbow, because about the elbow the panel's $10\,\mathrm N$ reaction and the tip's $9.81\,\mathrm N$ weight act on the same vertical line, $0.707\,\mathrm m$ out, and nearly cancel; the $0.19\,\mathrm N$ left over needs $-0.13\,\mathrm{N{\cdot}m}$ from the elbow motor. (c) $JM^{-1}J^\top=\tfrac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$, so $\Lambda=\begin{pmatrix}2&1\\1&2\end{pmatrix}\,\mathrm{kg}$, with eigenvalues $1$ and $3\,\mathrm{kg}$: $1\,\mathrm{kg}$ across the forearm, along $(-0.707,\ 0.707)$, and $3\,\mathrm{kg}=1+1/\sin^2 45^\circ$ along it, $(0.707,\ 0.707)$ — §6's readings at a pose the sweep skips. (d) $\mathcal{F}=\Lambda(0,1)=(1,\ 2)\,\mathrm N$ and $J^\top\mathcal{F}=(2.71,\ 0.71)\,\mathrm{N{\cdot}m}$. The upward acceleration splits into $0.707$ along the forearm and $0.707$ across it; the first meets $3\,\mathrm{kg}$ and the second $1\,\mathrm{kg}$, so the force $3(0.707)(0.707,\ 0.707)+1(0.707)(-0.707,\ 0.707)=(1,\ 2)$ leans $26.6^\circ$ from the vertical toward the forearm. Force and acceleration are parallel only along $\Lambda$'s two axes; at the catalog pose those axes were $x$ and $y$, so there $(0,1)\,\mathrm{m/s^2}$ took the upright $(0,\ 2)\,\mathrm N$.
> 3. `M = np.array(((m1 + 2*m2 + 2*m2*c, m2*(1 + c)), (m2*(1 + c), m2)))`, §3's matrix with $L_1=L_2=1$, and `Lam = np.linalg.inv(J @ np.linalg.inv(M) @ J.T)`. The run prints
>
>    | $\theta_2$ (°) | $M_{11}$ | lightest (kg) | heaviest (kg) |
>    |---:|---:|---:|---:|
>    | 10 | 8.94 | 2.000 | 35.163 |
>    | 30 | 8.46 | 2.000 | 6.000 |
>    | 50 | 7.57 | 2.000 | 3.704 |
>    | 70 | 6.37 | 2.000 | 3.132 |
>    | 90 | 5.00 | 2.000 | 3.000 |
>    | 110 | 3.63 | 2.000 | 3.132 |
>    | 130 | 2.43 | 2.000 | 3.704 |
>    | 150 | 1.54 | 2.000 | 6.000 |
>    | 170 | 1.06 | 2.000 | 35.163 |
>
>    At $90^\circ$ the eigenvalues are $2$ and $3\,\mathrm{kg}$ against the bare arm's $1$ and $2$: the tool added exactly $1\,\mathrm{kg}$ along every direction, at every angle, because a point mass at the tip moves with the tip. With $J$ square and invertible, $\Lambda=J^{-\top}MJ^{-1}$, and the tool adds $m\,J^\top J$ to $M$, hence $m\,I$ to $\Lambda$. The heavy direction still blows up toward $0^\circ$ and $180^\circ$ ($35.2\,\mathrm{kg}$ at $10^\circ$), because the singularity is in $J$, which no payload changes. A $10\,\mathrm N$ vertical contact at $90^\circ$ now accelerates the unconstrained tip at $10/3=3.3\,\mathrm{m/s^2}$ instead of $5$.

### Sources

- *Modern Robotics* (Lynch & Park) ch.8 (dynamics) and ch.11 (control) — see [[04-robotics/modern-robotics-book|the book guide]] for the free official PDF. The mass-matrix form in §3, derived here from the two point masses' velocity Jacobians, is the standard planar 2R result; ch.8 reaches it by the Lagrangian route.
- O. Khatib, "A unified approach for motion and force control of robot manipulators: The operational space formulation," *IEEE Journal on Robotics and Automation*, vol. 3, no. 1, pp. 43–53, 1987 — the origin of $\Lambda$ and of task-space control. (The journal is "Journal *on*", not "of".)
- The numeric examples on this page were computed here from the stated masses and lengths, not quoted from a source; recompute them rather than trusting them.

## 한국어

*[[02-foundations/linear-algebra|1. 선형대수]]와 [[02-foundations/lab-plants|0.6 Lab Plants]]의 P2 카탈로그 위에 선다. 필요한 순기구학, 야코비안, $\tau=J^\top\mathcal{F}$는 §1이 P2에 대해 유도하고, Modern Robotics 챕터 요약([[04-robotics/modern-robotics/ch04-forward-kinematics|4장]]과 [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]])이 임의의 팔에 대해 가르친다 — 함께 읽어라.
이 페이지는 접촉이 요구하는 물리 한 조각을 더하며, [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]로 트랙을 닫는다.*

이 페이지는 순기구학·역기구학·야코비안을 일반적으로 **가르치지 않는다** — *Modern Robotics* 챕터
요약이 2R 계산 예제와 함께 그 일을 하고, §1은 동역학에 필요한 P2의 경우만 유도한다. 이 페이지가 존재하는 이유는, 그 챕터들이
매니퓰레이션 트랙에서 가장 이어져야 할 지점에서 멈추기 때문이다: **동역학**, 그리고 관절
공간 동역학을 실제로 접촉이 일어나는 작업공간으로 옮기는 방정식.

페이지 전체가 사실 하나의 질문이다: *제어기가 말단에서 운동이나 힘을 명령할 때, 팔 자신의
질량은 그 명령에 무슨 짓을 하는가?*

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 조작 층과 접촉·힘·촉각 피드백 층 바로 밑의 수학 바닥이다([[physical-ai-map|피지컬 AI 지도]]에서 학위논문 경로 위에 놓인 칩이다). "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계, 곧 자세에 따라 유효 질량이 바뀌는 팔을 붙들고 가속하는 일과, 말단의 겉보기 질량이 밀기의 결과를 정하는 *끼움을 수행하는* 단계를 받치며, §2의 토크 잔차, 곧 측정 토크에서 모델 토크를 뺀 값으로는 로봇이 *접촉을 감지하는* 방법도 된다. 이것 없이는 힘 제어기를 눈을 감고 튜닝하는 셈이다. P2의 어깨는 가만히 있는 데만 $19.62\,\mathrm{N{\cdot}m}$가 들고, 관절 1은 팔을 곧게 뻗었을 때 접었을 때보다 가속하기가 다섯 배 어려우며, 말단은 옆으로 밀면 $1\,\mathrm{kg}$, 위로 밀면 $2\,\mathrm{kg}$처럼 느껴져서, 임피던스 게인 하나 — 힘 제어기가 말단에 주는 강성과 감쇠([[04-robotics/force-compliance-control|13. §2]]) — 가 방향마다 다르게 행동한다. 뒤 페이지들은 이 페이지를 절 단위로 가져다 쓴다. [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]는 이 페이지의 §2, §3, §6, §8을, [[04-robotics/capstone-panel-contact|26. 캡스톤]]은 패널에서의 §6 겉보기 질량 행렬 $\Lambda$를, [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]는 §3, §5, §6을, [[04-robotics/system-identification|5.5 시스템 식별]]은 §2와 §7의 파라미터를 쓴다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지는 [[02-foundations/overview#통과 점검 — 기초는 끝났는가|기초 통과 점검]] 바로 뒤의 블록 1 그 자체이고(통과 점검의 선택 문제 15번이 이 페이지의 $\Lambda$를 묻는다), 작업공간으로 잇는 다리는 블록 3, 곧 로보틱스 12, 13, 15의 시연·임피던스·파지로 이어진다. 이 페이지를 마치면 P2 위에서 매니퓰레이터 방정식을 양쪽 방향으로 쓰고, $J$와 $M$에서 $\Lambda$를 계산하고, 주어진 방향에서 접촉이 뻣뻣하게 느껴질지 무르게 느껴질지 예측할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 세 번쯤 든다. **첫 회차:** 이 페이지의 대상과 그림, §1(P2에 대해 유도한 기구학의 세 사실), 그리고 멈춤·운동·접촉의 세 경우까지의 §2. **둘째 회차:** 질량 행렬을 손으로 유도하는 §3, 빠른 운동이 관절을 결합시키는 §4, 중력 검산까지의 §5. **셋째 회차:** $\Lambda$가 어디서 오는지·2R 계산·두 귀결·스윕까지의 §6을 읽는다. 이 페이지가 임계 경로에 있는 이유가 §6이다. 그다음 스스로 점검 1–3번, 과제 2번, [[02-foundations/overview#통과 점검 — 기초는 끝났는가|통과 점검]]의 선택 문제 15번을 푼다. §5의 계산 토크, §7, 접힌 *더 깊이* 메모는 논문의 동역학 주장이 중요해질 때 읽고, §8은 그런 논문을 읽을 때의 점검표다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그의 평면 2링크 팔에 이번에는 질량을 단다. 링크는 $L_1=L_2=1\,\mathrm m$인 질량 없는 막대이고 각 링크의 먼 끝에 $1\,\mathrm{kg}$ 점질량이 있으며, 관절각은 $x$축에서 재고 엘보 각은 첫 링크에 대해 잰다. 이 페이지는 팔을 **연직면**에 세워 중력 $g=9.81\,\mathrm{m/s^2}$가 $-y$ 방향으로 작용하게 하고, 카탈로그 자세 $\theta=(0^\circ,90^\circ)$ — 윗팔은 수평, 아래팔은 똑바로 위, 말단은 $(1,1)\,\mathrm m$ — 에서 계산한다. 카탈로그는 이 자세의 $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$와 $M=\begin{pmatrix}3&1\\1&1\end{pmatrix}$를 고정해 둔다. §3과 §6은 엘보를 $0^\circ$에서 $180^\circ$까지 옮기고, 과제는 $45^\circ$로 옮긴다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 370" style="max-width:100%;height:auto" role="img" aria-label="연직면에서 엘보 90도인 P2: 1 kg 점질량 둘과 무게, 모멘트 팔 1 m에서 나오는 어깨 토크 19.62 N·m와 엘보의 0, 말단과 패널에 따로 그린 접촉력 쌍, 겉보기 질량 타원 diag(1, 2) kg">
  <defs><marker id="aMkK" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <line x1="30" y1="30" x2="30" y2="76" stroke="currentColor" stroke-width="1.6" marker-end="url(#aMkK)"/>
  <text x="40" y="50" font-size="11" fill="currentColor">g = 9.81 m/s²</text>
  <text x="40" y="64" font-size="11" fill="currentColor" fill-opacity="0.75">아래가 −y</text>
  <line x1="26" y1="306" x2="52" y2="306" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" marker-end="url(#aMkK)"/>
  <line x1="26" y1="306" x2="26" y2="280" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" marker-end="url(#aMkK)"/>
  <text x="56" y="310" font-size="11" fill="currentColor" fill-opacity="0.85">x</text>
  <text x="32" y="284" font-size="11" fill="currentColor" fill-opacity="0.85">y</text>
  <path d="M100 206 L89 222 L111 222 Z" stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.7" stroke-linejoin="round"/>
  <line x1="80" y1="222" x2="120" y2="222" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <line x1="82" y1="222" x2="76" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="91" y1="222" x2="85" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="100" y1="222" x2="94" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="109" y1="222" x2="103" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="118" y1="222" x2="112" y2="229" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="100" y1="206" x2="250" y2="206" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <line x1="250" y1="206" x2="250" y2="56" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <circle cx="100" cy="206" r="6.5" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.0"/>
  <circle cx="250" cy="206" r="10" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="250" cy="206" r="5.5" stroke="none" fill="currentColor"/>
  <circle cx="250" cy="56" r="5.5" stroke="none" fill="currentColor"/>
  <text x="88" y="210" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">(0, 0)</text>
  <text x="250" y="42" font-size="11" fill="currentColor" text-anchor="middle">말단 (1, 1)</text>
  <text x="238" y="60" font-size="11" fill="currentColor" text-anchor="end">1 kg</text>
  <text x="236" y="197" font-size="11" fill="currentColor" text-anchor="end">1 kg</text>
  <text x="236" y="230" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">엘보 (1, 0)</text>
  <line x1="250" y1="212" x2="250" y2="255.1" stroke="currentColor" stroke-width="1.6" marker-end="url(#aMkK)"/>
  <text x="258" y="253.1" font-size="11" fill="currentColor">9.81 N</text>
  <line x1="250" y1="62" x2="250" y2="105.1" stroke="currentColor" stroke-width="1.6" marker-end="url(#aMkK)"/>
  <text x="258" y="97.1" font-size="11" fill="currentColor">9.81 N</text>
  <line x1="250" y1="108.1" x2="250" y2="196" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9" stroke-dasharray="2 3"/>
  <text x="240" y="112" font-size="11" fill="currentColor" text-anchor="end">엘보 간격 0:</text>
  <text x="240" y="127" font-size="11" fill="currentColor" text-anchor="end">말단의 무게선이</text>
  <text x="240" y="142" font-size="11" fill="currentColor" text-anchor="end">엘보 축을 지난다</text>
  <line x1="100" y1="232" x2="100" y2="287.1" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="250" y1="258.1" x2="250" y2="287.1" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="101" y1="281.1" x2="249" y2="281.1" stroke="currentColor" stroke-width="1.1"/>
  <path d="M108 277.6 L101 281.1 L108 284.6" stroke="currentColor" stroke-width="1.1" fill="none" stroke-linejoin="round"/>
  <path d="M242 277.6 L249 281.1 L242 284.6" stroke="currentColor" stroke-width="1.1" fill="none" stroke-linejoin="round"/>
  <text x="175" y="276.1" font-size="11" fill="currentColor" text-anchor="middle">두 무게선까지 1 m</text>
  <path d="M 124.4 197.1 A 26 26 0 0 0 75.6 197.1" stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aMkK)"/>
  <text x="56" y="156" font-size="11" fill="currentColor">τ<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= 2 · 9.81 · 1</tspan></text>
  <text x="56" y="171" font-size="11" fill="currentColor">= 19.62 N·m</text>
  <path d="M 262.9 221.3 A 20 20 0 0 0 265.3 193.1" stroke="currentColor" stroke-width="1.3" fill="none" stroke-opacity="0.8" stroke-dasharray="3 3"/>
  <text x="275" y="202" font-size="11" fill="currentColor">τ<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= 0</tspan></text>
  <rect x="322" y="12" width="230" height="146" rx="4" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="276" y1="56" x2="320" y2="56" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="1 3"/>
  <text x="332" y="31" font-size="12" fill="currentColor">말단의 겉보기 질량</text>
  <ellipse cx="374" cy="98" rx="24" ry="48" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.1"/>
  <line x1="374" y1="98" x2="398" y2="98" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <line x1="374" y1="98" x2="374" y2="50" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="386" y="113" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <text x="370" y="78" font-size="11" fill="currentColor" text-anchor="end">2</text>
  <text x="418" y="64" font-size="12" fill="currentColor">Λ = diag(1, 2) kg</text>
  <text x="418" y="86" font-size="11" fill="currentColor">옆으로 밀면 1 kg</text>
  <text x="418" y="102" font-size="11" fill="currentColor">위로 밀면 2 kg</text>
  <text x="418" y="124" font-size="11" fill="currentColor" fill-opacity="0.8">kg의 타원이다.</text>
  <text x="418" y="139" font-size="11" fill="currentColor" fill-opacity="0.8">속도의 타원이 아니다</text>
  <rect x="322" y="170" width="230" height="150" rx="4" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="332" y="189" font-size="12" fill="currentColor">말단의 접촉, 떼어 그림</text>
  <circle cx="440" cy="222" r="5.5" stroke="none" fill="currentColor"/>
  <text x="440" y="211" font-size="11" fill="currentColor" text-anchor="middle">말단</text>
  <line x1="380" y1="284" x2="500" y2="284" stroke="currentColor" stroke-width="1.6"/>
  <line x1="384" y1="284" x2="377" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="398" y1="284" x2="391" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="412" y1="284" x2="405" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="426" y1="284" x2="419" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="440" y1="284" x2="433" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="454" y1="284" x2="447" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="468" y1="284" x2="461" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="482" y1="284" x2="475" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="496" y1="284" x2="489" y2="292" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="374" y="288" font-size="11" fill="currentColor" text-anchor="end">패널</text>
  <line x1="433" y1="239" x2="433" y2="283" stroke="currentColor" stroke-width="1.8" marker-end="url(#aMkK)"/>
  <line x1="447" y1="278" x2="447" y2="234" stroke="currentColor" stroke-width="1.8" marker-end="url(#aMkK)"/>
  <text x="425" y="244" font-size="11" fill="currentColor" text-anchor="end">명령된 힘,</text>
  <text x="425" y="259" font-size="11" fill="currentColor" text-anchor="end">패널에</text>
  <text x="425" y="274" font-size="11" fill="currentColor" text-anchor="end">(0, −10) N</text>
  <text x="455" y="244" font-size="11" fill="currentColor">반작용,</text>
  <text x="455" y="259" font-size="11" fill="currentColor">말단에</text>
  <text x="455" y="274" font-size="11" fill="currentColor">(0, +10) N</text>
  <text x="332" y="308" font-size="11" fill="currentColor" fill-opacity="0.8">같은 길이, 다른 물체</text>
  <text x="12" y="342" font-size="11" fill="currentColor" fill-opacity="0.85">● 1 kg 점질량 · ○ 관절 축 · 막대는 질량 없음 · 힘 화살표는 모두 같은 축척</text>
  <text x="12" y="358" font-size="11" fill="currentColor" fill-opacity="0.85">모멘트 팔은 링크 길이가 아니라 관절 축에서 무게선까지의 수평 간격이다.</text>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 P2를 $\theta=(0^\circ,90^\circ)$에서 연직면에 세워 중력($-y$ 방향 $9.81\,\mathrm{m/s^2}$)이 지면 위에 놓이게 한 것으로, 엘보 $(1,0)$과 말단 $(1,1)$의 $1\,\mathrm{kg}$ 점질량은 무게가 각각 $9.81\,\mathrm{N}$이고 둘 다 어깨 축에서 오른쪽으로 수평 $1\,\mathrm{m}$ 떨어져 있어 $\tau_1=2\cdot9.81\cdot1=19.62\ \mathrm{N{\cdot}m}$이며, 말단의 무게 작용선은 엘보 축을 지나므로 $\tau_2=0$이다. 말단의 접촉력 쌍은 떼어 그려서, 명령한 $(0,-10)\,\mathrm{N}$은 패널에, 그 반작용 $(0,+10)\,\mathrm{N}$은 말단에 작용하며 길이는 같고 받는 물체만 반대다. 상자 안의 타원은 말단의 겉보기 질량 $\Lambda=\mathrm{diag}(1,2)\ \mathrm{kg}$로, $2\,\mathrm{kg}$짜리 팔이 옆으로 밀면 $1\,\mathrm{kg}$, 위로 밀면 $2\,\mathrm{kg}$처럼 느껴진다는 뜻이며 속도가 아니라 질량의 타원이다.

### 1. 기구학이 이미 준 것

동역학이 힘에 대해 무엇이든 말하려면 팔에 대해 세 가지를 먼저 알아야 한다. 말단이 어디 있는지, 관절이 돌 때 말단이 얼마나 빨리 움직이는지, 말단을 미는 힘이 관절마다 얼마의 토크를 요구하는지다. 아래에서 계속 쓰이므로 한자리에 적어 둔다:

| 결과 | 내용 | 출처 |
|---|---|---|
| 순기구학 | 관절각 $\theta \mapsto$ 말단 자세 $T(\theta)$ | [[04-robotics/modern-robotics/ch04-forward-kinematics\|MR 4장]] |
| 속도 기구학 | $v = J(\theta)\,\dot\theta$ — 관절 속도가 끝점 속도로 | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR 5장 §1]] |
| 정역학 쌍대성 | $\tau = J^\top(\theta)\,\mathcal{F}$ — 같은 행렬이 렌치를 토크로 되돌린다 | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR 5장 §3]] |

셋째 행의 $\mathcal{F}$는 **렌치**(wrench), 곧 말단이 주변에 가하는 힘이고 3D에서는 그 모멘트까지 함께 담는다. 평면의 P2에서는 그림에서 패널에 가한 $(0,-10)\,\mathrm N$처럼 뉴턴 단위의 힘 2차원 벡터일 뿐이다.

**P2라면 셋 모두 몇 줄이면 된다.** $\theta_{12}=\theta_1+\theta_2$, $c_1=\cos\theta_1$, $s_{12}=\sin\theta_{12}$ 등으로 쓰자. 엘보와 말단은
$$p_1=L_1\,(c_1,\ s_1),\qquad p_2=p_1+L_2\,(c_{12},\ s_{12})$$
에 있고, 각 링크가 자기 절대 각도 방향으로 길이만큼 더해지므로 이것이 순기구학이다(P2의 도구는 $p_2$에 있다). 연쇄 법칙으로 시간 미분하면 $v=J(\theta)\,\dot\theta$이고, $J=\partial p_2/\partial\theta$의 열은 $\partial p_2/\partial\theta_1=(-L_1s_1-L_2s_{12},\ L_1c_1+L_2c_{12})$와 $\partial p_2/\partial\theta_2=(-L_2s_{12},\ L_2c_{12})$다. $\theta=(0°,90°)$에서 이 열은 $(-1,1)$과 $(-1,0)$, 곧 카탈로그의 $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$이다. 쌍대성은 일률에서 나온다. 팔 자신의 질량은 잠시 제쳐 두자(그 관성과 무게는 §2의 $M$과 $g$가 된다). 질량 없는 팔은 에너지를 저장하지 않으므로, 모터가 넣는 일률 $\tau^\top\dot\theta$가 말단이 내보내는 일률 $\mathcal{F}^\top v=\mathcal{F}^\top J\dot\theta$와 모든 $\dot\theta$에서 같다. 따라서 $\tau=J^\top\mathcal{F}$다. 이 자세에서 $\mathcal{F}=(0,-10)$ N으로 누르려면 $\tau=(-10,\ 0)$ N·m가 든다.

이 페이지 전체는 그 그림에 **질량**을 더하면 무슨 일이 일어나는가이다.

도달 가능한 동작도 부하 아래 구동기가 만들 수 있는 동작은 아닐 수 있다. 자세 해법은 드라이월 시트를 기하적으로 놓으면서 가속하고 유지할 노력을 무시할 수 있다. **여기서 얻는 독법.** 논문이 자세 가능성, 속도 가능성, 정적 지지, 동적 실행 중 무엇을 확립하는지 본다. 각각 다른 조건을 추가하므로 앞 문제를 풀어도 뒤 문제가 자동으로 풀리지는 않는다.

### 2. 매니퓰레이터 방정식

*한 문장으로:* 관절 모터마다 내야 하는 토크는 자세에 따라 유효 질량이 바뀌는 팔을 가속하는 몫, 관절들의 운동이 서로에게 미치는 몫, 팔의 무게를 버티는 몫을 더한 것이고, 접촉은 아무도 명령하지 않은 밀기를 하나 더 보탠다.

*이 절에서 하나만 가져간다면:* 같은 방정식이 양쪽으로 쓰인다는 것 — $\tau = M\ddot\theta + C\dot\theta + g$는 운동에 필요한 토크를, $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$는 토크가 만드는 운동을 주고, $M$은 언제나 가역이므로 모든 자세에서 성립한다. 이 절 끝에서 P2로 계산하는데, $\theta=(0°,90°)$에서 모터를 끄면 $\ddot\theta=(-9.81,\ 9.81)$ rad/s²로 떨어지기 시작한다.

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau$$

이것은 관절이 $n$개인 강체 팔의 **운동 방정식**(equation of motion)이다. 관절마다 토크 균형 하나씩, 서로 결합된 2계 미분방정식 $n$개이므로 모든 항의 단위가 토크다(회전 관절이면 N·m). $\theta \in \mathbb{R}^n$은 관절각, $\dot\theta$와 $\ddot\theta$는 그 속도와 가속도이고, $M(\theta)$와 $C(\theta,\dot\theta)$는 $n \times n$ 행렬, $g(\theta)$와 $\tau$는 토크의 $n$차원 벡터다. 아래 2R 팔에서는 $n = 2$다.

**이 모양이 어디서 오는가.** 세 가지 물리 효과를 나사로 붙인 것이 아니라, 에너지 하나를 한 번
미분한 것이다. 운동에너지 $T = \tfrac12\dot\theta^\top M(\theta)\dot\theta$와 위치에너지
$V(\theta)$로 라그랑지안 $L = T - V$를 쓰고, 라그랑주 방정식
$\frac{d}{dt}\frac{\partial L}{\partial\dot\theta} - \frac{\partial L}{\partial\theta} = \tau$를
적용한다. 이 식은 관절마다 성립하므로 스칼라 함수 $L$ 하나가 방정식 $n$개를 모두 만든다:
$$\frac{d}{dt}\frac{\partial L}{\partial \dot\theta_i} - \frac{\partial L}{\partial \theta_i} = \tau_i, \qquad i = 1, \dots, n$$
역학 과목을 따로 듣지 않아도 믿을 수 있다: 이것은 뉴턴 제2법칙을 에너지 언어로 다시 쓴 것이다.
직선 위 질량 하나라면 $L = \tfrac12 m\dot x^2 - V(x)$이므로 $\frac{d}{dt}\frac{\partial L}{\partial\dot x} = \frac{d}{dt}(m\dot x)$는 운동량의 변화율이고, $\frac{\partial L}{\partial x} = -\partial V/\partial x$는 에너지 지형(예컨대 중력)이 가하는 힘이다. 방정식은 운동량이 가한 힘과 그 힘의 합만큼 변한다는 말, 곧 $m\ddot x = F - \partial V/\partial x$다.
$x$ 대신 관절각을 넣어도 같은 장부 정리가 통하며, [[04-robotics/modern-robotics/ch08-dynamics|MR 8장]]이 전 과정을 보여 준다.
다시 팔로 돌아오면, 첫 항이 $\frac{d}{dt}\big(M\dot\theta\big) = M\ddot\theta + \dot M\dot\theta$를 주고,
둘째 항이 $-\frac{\partial T}{\partial\theta}$와 $\frac{\partial V}{\partial\theta}$를 낸다.
모으면 $M\ddot\theta$가 첫 조각이고, 속도에 이차인 나머지
$\dot M\dot\theta - \frac{\partial T}{\partial\theta}$가 $C(\theta,\dot\theta)\dot\theta$라고
*이름 붙는* 것이며, $\frac{\partial V}{\partial\theta}$가 $g(\theta)$다.

유도 자체보다 값어치 있는 두 가지가 따라 나온다. 첫째, **$C$는 오직 $M$이 $\theta$에 의존하기
때문에 존재한다** — 관성 행렬이 상수라면 $\dot M = 0$이고 $\partial T/\partial\theta = 0$이라
코리올리 항은 통째로 사라진다. 추가된 힘이 아니라 *자세에 따라 변하는 질량을 쓰는 장부상의
대가*다. 둘째, $C$는 **유일하지 않다**. 결정되는 것은 곱 $C\dot\theta$뿐이라서 책마다 같은
로봇에 다른 $C$ 행렬을 쓴다. 논문들이 그중 무엇을 고르는지, 그리고 그 선택이 떠받치는 안정성 증명의 에너지 항등식은 §4의 $C$가 있어야 하므로 §4 끝의 *더 깊이* 메모에 있다.

네 항이고, 각각 다른 물리적 역할을 한다:

- **$M(\theta)$ — 질량(관성) 행렬.** 대칭이고 양정치이므로 항상 가역이다 — 그래서
  $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$가 언제나 잘 정의된다. 핵심은 괄호 안의
  인자다: $M$은 **자세에 의존한다**. 팔은 상수 질량이 아니라, 움직이면서 값이 변하는
  질량이다.
  두 성질 모두 운동에너지에서 온다. 대칭은 $M = M^\top$이라는 뜻이다. 양정치는 다음을 뜻한다:
$$\dot\theta^\top M(\theta)\,\dot\theta > 0 \quad \text{for every } \dot\theta \ne 0$$
  $\tfrac12\dot\theta^\top M\dot\theta$가 운동에너지 $T$이고, 질량이 있는 물체의 실제 운동은 언제나 운동에너지가 양수이기 때문이다([[02-foundations/linear-algebra|1. 선형대수 §3]]). §3의 2R 팔에서는 $M_{22} = 1 > 0$이고 $\det M = 1 + \sin^2\theta_2 \ge 1$이므로 모든 자세에서 $M$이 양정치다. $\theta_2 = 90°$에서 운동 $\dot\theta = (1, -1)$ rad/s의 운동에너지는 $T = 1$ J이다. 반례: $\begin{pmatrix}1&2\\2&1\end{pmatrix}$은 대칭이지만 $\dot\theta = (1,-1)$에서 $\dot\theta^\top A\dot\theta = -2$, 즉 음의 "운동에너지"가 나오므로 어떤 실제 팔도 이런 질량 행렬을 갖지 않는다.
- **$C(\theta,\dot\theta)\,\dot\theta$ — 코리올리·원심 항.** 속도의 이차식이다. 마찰이
  *아니다*. 한 관절의 운동이 다른 관절에 토크를 가하게 만드는 결합이며, 정지 상태에서 0이 된다.
- **$g(\theta)$ — 중력.** 자세 의존, 속도 무관. 로봇이 가만히 있을 때도 싸우는 항.
- **$\tau$ — 관절 토크**, 모터가 실제로 명령하는 것.

말단이 무언가에 닿으면 외부 렌치 $\mathcal{F}_{\text{ext}}$가 정역학 쌍대성을 통해 들어온다:

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau + J^\top(\theta)\,\mathcal{F}_{\text{ext}}$$

이 추가 항이 접촉을 계획 문제가 아니라 제어 문제로 만드는 이유 전부다: 환경이 제어기가
명령하지 않은 토크를 주입할 수 있게 된다.

**방정식을 양쪽 방향으로 쓴다.** 역동역학은 원하는 가속도를 정하고 현재 위치·속도에서 필요한 토크를 구한다. 순동역학은 토크를 정하고 생길 가속도를 푼다. 시뮬레이터는 보통 후자를, 모델 기반 추종 제어기는 흔히 전자를 쓴다. 같은 방정식에서 미지수만 달라진다. 식으로 쓰면
$$\text{inverse: } \tau = M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta), \qquad \text{forward: } \ddot\theta = M(\theta)^{-1}\big(\tau - C(\theta,\dot\theta)\,\dot\theta - g(\theta)\big)$$
이고, $M$이 가역이므로 순동역학 형태는 모든 상태에서 존재한다. §3의 $M$과 §5의 $g$로 예를 들면: $\theta = (0°, 90°)$에서 정지해 있고 모터를 끈($\tau = 0$) 2R 팔은 $\ddot\theta = -M^{-1}g = (-9.81,\ 9.81)$ rad/s²이다. 그래서 어깨는 떨어지기 시작하고 $\theta_2$는 같은 빠르기로 커진다. 처음 순간에는 $\theta_1+\theta_2$가 변하지 않아 아래팔이 곧게 선 채로 남고, 두 질량 모두 자유낙하로 출발한다.

먼저 비접촉 상태로 팔을 정지시킨다. 속도·가속도가 모두 0이므로 이상적 모델은 $\tau=g(\theta)$를 요구한다. 다음으로 관절 속도를 일정하게 유지한다. 가속도는 0이어도 기하가 변하므로 $C\dot\theta$는 남을 수 있다. 마지막으로 접촉을 더한다. 외력은 부호와 프레임에 따라 하중을 받치거나 운동을 방해한다. 중력 보상만으로 미지의 접촉력을 없앨 수는 없다. 긴 궤적 전에 이 세 경우로 동역학 구현을 점검할 수 있다.

> [!question] 토크 잔차 읽기 · Read a torque residual
> 측정 토크와 모델의 차이가 반드시 접촉인가? **답:** 아니다. 마찰, 하중 오차, 모터 보정, 시점 오차도 잔차를 만든다. 토크로 접촉을 추정하려면 이 대안들을 고려해야 한다.

### 3. 계산 예제 — 2R 팔의 질량 행렬

§1의 평면 2R 팔, 곧 장치 P2에 각 링크 끝의 점질량을 둔다: $m_1 = m_2 = 1$ kg, $L_1 = L_2 = 1$ m.
질량 행렬은 정의상 운동 에너지를 $T = \tfrac12\dot\theta^\top M(\theta)\dot\theta$로 쓰게 하는 행렬이므로, $T$를 질량 하나씩 세 단계로 쌓는다. (엘보를 잠그면 같은 팔은 어깨 둘레로 도는 강체 하나, 곧 관성 모멘트에 걸린 토크가 되고, 그것을 계산한 곳이 [[02-foundations/basic-mechanics|0.6.1 기초 역학 §7]]이다.)

1. **질량마다의 속도 야코비안.** §1의 각 위치를 시간으로 미분한다. 엘보 질량은 $v_1=J_1\dot\theta$로, 말단 질량은 $v_2=J_2\dot\theta$로 움직이고,
   $$J_1=\begin{pmatrix}-L_1s_1&0\\L_1c_1&0\end{pmatrix},\qquad J_2=\begin{pmatrix}-L_1s_1-L_2s_{12}&-L_2s_{12}\\L_1c_1+L_2c_{12}&L_2c_{12}\end{pmatrix}$$
   이다. 엘보를 돌려도 엘보 질량은 움직이지 않으므로 $J_1$의 둘째 열은 0이고, $J_2$는 §1의 말단 야코비안이다.
2. **운동 에너지를 더한다.** 점질량의 운동 에너지는 $\tfrac12 m\lVert v\rVert^2$가 전부이고 $\lVert J\dot\theta\rVert^2=\dot\theta^\top J^\top J\,\dot\theta$이므로
   $$T=\tfrac12\dot\theta^\top\big(m_1J_1^\top J_1+m_2J_2^\top J_2\big)\dot\theta \quad\Longrightarrow\quad M(\theta)=m_1J_1^\top J_1+m_2J_2^\top J_2$$
3. **정리한다.** $J_1^\top J_1=\mathrm{diag}(L_1^2,\ 0)$이다. $J_2^\top J_2$의 $(1,1)$ 성분은 $(L_1s_1+L_2s_{12})^2+(L_1c_1+L_2c_{12})^2=L_1^2+L_2^2+2L_1L_2\,(c_1c_{12}+s_1s_{12})$이고, $c_1c_{12}+s_1s_{12}=\cos(\theta_{12}-\theta_1)=\cos\theta_2$다. 같은 항등식으로 $(1,2)$ 성분은 $L_2^2+L_1L_2\cos\theta_2$가 되고, $(2,2)$ 성분은 $L_2^2$다. 두 질량의 몫을 더하면

$$M(\theta) = \begin{pmatrix} (m_1{+}m_2)L_1^2 + m_2L_2^2 + 2m_2L_1L_2\cos\theta_2 & m_2(L_2^2 + L_1L_2\cos\theta_2) \\ m_2(L_2^2 + L_1L_2\cos\theta_2) & m_2L_2^2 \end{pmatrix}$$

카탈로그 자세 $\theta=(0°,90°)$에서 검산하자. 거기서 $J_1=\begin{pmatrix}0&0\\1&0\end{pmatrix}$, $J_2=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$이므로 $M=\mathrm{diag}(1,0)+\begin{pmatrix}2&1\\1&1\end{pmatrix}=\begin{pmatrix}3&1\\1&1\end{pmatrix}$, 카탈로그의 $M$이다. §2의 라그랑주 경로로도 같은 행렬이 나오며, [[04-robotics/modern-robotics/ch08-dynamics|MR 8장]]이 바로 이 팔에서 그 경로를 끝까지 밟는다. *Modern Robotics* 8장은 이어서 질량이 퍼져 있는 링크를 다루는데, 그때는 링크마다 질량 중심 둘레의 회전 운동 에너지가 더해진다.

원소를 읽어라. 대각 항은 다른 관절을 고정했을 때 한 관절 속도에 대응하는 유효 관성으로,
그 관절의 "자기" 링크뿐 아니라 여러 하류 링크의 질량과 관성을 포함할 수 있다. 비대각의
$\cos\theta_2$ 항은 결합이다. 관절 1이 돌면 링크 2의 질량이 움직이기 때문에 생기고, 그래서
한 관절이 느끼는 관성은 다른 관절이 어디 있는지에 달린다.

위 숫자 $m_1 = m_2 = 1$, $L_1 = L_2 = 1$을 대입하면 $M$은 $\theta_2$에만 의존한다:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

세 자세에서 계산하면:

| $\theta_2$ | 모양 | $M_{11}$ | $M$ |
|---:|---|---:|---|
| $0°$ | 곧게 뻗음 | $5$ | $\begin{pmatrix}5&2\\2&1\end{pmatrix}$ |
| $90°$ | 팔꿈치 직각 | $3$ | $\begin{pmatrix}3&1\\1&1\end{pmatrix}$ |
| $180°$ | 접힘 | $1$ | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ |

$M_{11}$ 열은 한 줄로 물리적으로 읽힌다. 관절 1만 돌리면 각 질량이 어깨 둘레의 원을 그리므로, 관절 1에서 각 질량까지의 거리를 $r$이라 할 때 $M_{11}=m_1r_1^2+m_2r_2^2$다. 엘보 질량은 늘 $1$ m 밖에 있고 말단 질량은 세 자세에서 $2$, $\sqrt2$, $0$ m 밖에 있으므로 $1+4=5$, $1+2=3$, $1+0=1$이다.

<svg viewBox="0 0 560 200" style="max-width:100%;height:auto" role="img" aria-label="같은 2링크 팔의 세 팔꿈치 각도: 말단 질량이 어깨에서 2, 루트 2, 0 m 떨어져 있어 1번 관절 관성이 5에서 3, 1로 줄어든다">
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">
    <line x1="60" y1="120" x2="100" y2="120"/><line x1="100" y1="120" x2="140" y2="120"/>
    <line x1="240" y1="120" x2="280" y2="120"/><line x1="280" y1="120" x2="280" y2="80"/>
    <line x1="420" y1="120" x2="460" y2="120"/><line x1="460" y1="134" x2="420" y2="134"/>
    <path d="M 466 120 A 8 8 0 0 1 466 134" stroke-width="1.1" opacity="0.6"/>
  </g>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" fill="none" opacity="0.8">
    <line x1="60" y1="104" x2="140" y2="104"/><line x1="60" y1="99" x2="60" y2="109"/><line x1="140" y1="99" x2="140" y2="109"/>
    <line x1="240" y1="120" x2="280" y2="80"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="120" r="4.5"/><circle cx="100" cy="120" r="4"/><circle cx="140" cy="120" r="5" fill-opacity="0.55"/>
    <circle cx="240" cy="120" r="4.5"/><circle cx="280" cy="120" r="4"/><circle cx="280" cy="80" r="5" fill-opacity="0.55"/>
    <circle cx="420" cy="120" r="4.5"/><circle cx="460" cy="120" r="4"/><circle cx="420" cy="134" r="5" fill-opacity="0.55"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="50">θ<tspan dy="3.5">2</tspan><tspan dx="3" dy="-3.5">= 0° · 곧게 뻗음</tspan></text>
    <text x="280" y="50">θ<tspan dy="3.5">2</tspan><tspan dx="3" dy="-3.5">= 90°</tspan></text>
    <text x="460" y="50">θ<tspan dy="3.5">2</tspan><tspan dx="3" dy="-3.5">= 180° · 접힘</tspan></text>
    <text x="460" y="68" font-size="10.5" opacity="0.75">겹쳐서 보이도록 어긋나게 그렸다</text>
    <text x="100" y="96">r = 2 m</text>
    <text x="248" y="92" text-anchor="end">r = √2 m</text>
    <text x="400" y="138" text-anchor="end">r = 0</text>
    <text x="100" y="160" font-size="12">M<tspan dy="3.5">11</tspan><tspan dx="3" dy="-3.5">= 1 + 2² = 5</tspan></text>
    <text x="280" y="160" font-size="12">M<tspan dy="3.5">11</tspan><tspan dx="3" dy="-3.5">= 1 + (√2)² = 3</tspan></text>
    <text x="460" y="160" font-size="12">M<tspan dy="3.5">11</tspan><tspan dx="3" dy="-3.5">= 1 + 0² = 1</tspan></text>
  </g>
</svg>

같은 팔을 세 팔꿈치 각도로 그린 것이다. 관절 1만 돌리면 각 $1\,\mathrm{kg}$ 질량이 어깨 둘레의 원을 그리므로 $M_{11}=m_1r_1^2+m_2r_2^2$이고, 엘보 질량은 늘 $r_1=1\,\mathrm m$, 말단 질량은 $r_2=2$, $\sqrt2$, $0\,\mathrm m$ 밖에 있어 $5$, $3$, $1$이 나온다. 같은 $2\,\mathrm{kg}$의 금속인데도 곧게 뻗었을 때 관절 1을 가속하기가 접었을 때보다 다섯 배 어렵다.

가져갈 숫자는 그 **5배**다. 관절 제어기가 싸우는 관성은 로봇의 속성이 아니라 로봇의 현재
자세의 속성이다. 팔을 접은 상태에서 잘 튜닝된 게인은 팔을 뻗은 상태에서 잘못 튜닝된
게인이다 — 독립 관절 PID가 해답이 아니라 타협인 첫 번째 이유다.

### 4. 코리올리·원심 항 — 빠른 운동이 관절을 결합시키는 이유

한 관절을 빠르게 휘두르면 팔에 닿은 것이 아무것도 없는데도 다른 관절이 토크를 느낀다. 저속에서 튜닝한 제어기가 고속에서 어긋나는 이유다. 이 절은 그 속도 항들에 이름을 붙이고 P2의 숫자를 넣은 뒤, 그것이 도는 질량이 당기는 힘 이상의 신기한 것이 아님을 보인다.

이 팔에서 $h = -m_2L_1L_2\sin\theta_2$로 두면 속도 이차 항은

$$C(\theta,\dot\theta)\,\dot\theta = \begin{pmatrix} h\,\dot\theta_2^2 + 2h\,\dot\theta_1\dot\theta_2 \\ -h\,\dot\theta_1^2 \end{pmatrix}$$

**어느 항이 무엇이고, $C$는 어디서 오는가.** $i$번째 행에서 한 관절 속도의 제곱 $\dot\theta_j^2$에 비례하는 항이 **원심** 항이고, $j \ne k$인 곱 $\dot\theta_j\dot\theta_k$에 비례하는 항이 **코리올리** 항이다. 위에서 $h\,\dot\theta_2^2$와 $-h\,\dot\theta_1^2$는 원심 항, $2h\,\dot\theta_1\dot\theta_2$는 코리올리 항이다. $\dot M - 2C$를 반대칭으로 만드는 표준 $C$는 *크리스토펠 기호*(Christoffel symbols) $c_{ijk}$를 통해 $M$의 도함수로 만든다:
$$c_{ijk} = \tfrac12\left(\frac{\partial M_{ij}}{\partial\theta_k} + \frac{\partial M_{ik}}{\partial\theta_j} - \frac{\partial M_{jk}}{\partial\theta_i}\right), \qquad C_{ij}(\theta,\dot\theta) = \sum_{k=1}^{n} c_{ijk}\,\dot\theta_k$$
그래서 §2에서 말한 대로 $M$이 상수면 $C = 0$이다. 2R 팔에서는 $M_{11}$과 $M_{12}$만 변하고 $\partial M_{11}/\partial\theta_2 = 2h$, $\partial M_{12}/\partial\theta_2 = h$이다. 대입하면 위의 벡터가 그대로 나오고, $\dot M - 2C = \begin{pmatrix}0 & -h(2\dot\theta_1 + \dot\theta_2)\\ h(2\dot\theta_1 + \dot\theta_2) & 0\end{pmatrix}$로 약속대로 반대칭이다.

숫자를 넣자. $\theta_2 = 90°$에서 $h = -1\cdot1\cdot1\cdot\sin 90° = -1$이다. 1번 관절은
**가만히 있으라**($\dot\theta_1 = 0$)고 명령받았고, 2번 관절이 $\dot\theta_2 = 2$ rad/s로
휘두른다고 하자. 첫 행은

$$h\,\dot\theta_2^2 = (-1)(2)^2 = -4 \ \text{N}\cdot\text{m}$$

2번 관절이 일정한 속도로 휘두른다면($\ddot\theta_2 = 0$), 1번 관절은 중력에 필요한 토크에 더해 *제자리에 있기 위해서만* $-4$ N·m를 더 내야 한다(중력 몫은 §5에서 계산한다). 로봇에 닿은 것은 아무것도 없다.
이것은 팔 자신의 움직이는 질량이 링크를 통해 되미는 힘이다. 속도를 두 배로 하면 항이 속도의
이차식이므로 $-16$ N·m로 네 배가 된다.

**같은 $-4$ N·m를 순수한 정역학으로.** 관절 1을 붙들어 두면 말단 질량은 엘보 둘레의 반지름 $L_2=1\,\mathrm m$인 원을 $2\,\mathrm{rad/s}$로 돌므로, 아래팔이 그것을 구심력 $m_2\dot\theta_2^2L_2=1\cdot2^2\cdot1=4\,\mathrm N$으로 안쪽으로 당겨야 한다. 뉴턴 제3법칙([[02-foundations/basic-mechanics|0.6.1 기초 역학 §2]])에 따라 질량은 같은 $4\,\mathrm N$으로 엘보를 아래팔을 따라 바깥으로 — 이 자세에서는 똑바로 위로 — 당기고, 그 힘은 어깨에서 오른쪽으로 $1\,\mathrm m$ 떨어져 작용한다. 그래서 관절 1에 대한 모멘트가 $(1,0)\times(0,4)=+4\,\mathrm{N{\cdot}m}$이고, 관절 1은 제자리에 있으려면 $-4\,\mathrm{N{\cdot}m}$를 내야 한다. 관절 2는 아무것도 느끼지 않는다. 그 힘이 관절 2의 축을 지나기 때문이고, 둘째 행 $-h\dot\theta_1^2$가 0인 것이 그것이다.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="엘보 90도의 P2에서 관절 2가 2 rad/s로 휘돌고 관절 1은 멈춰 있다: 말단 질량은 엘보 둘레 원을 2 m/s로 돌고, 아래팔이 그것을 4 N으로 안쪽으로 당기며, 그 반작용 4 N이 엘보를 아래팔을 따라 바깥으로 당기고, 그 힘은 어깨에서 1 m 떨어져 작용하므로 관절 1은 −4 N·m를 내야 하고 관절 2는 아무것도 느끼지 않는다">
  <defs><marker id="aCork" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <line x1="80.0" y1="222.0" x2="220.0" y2="222.0" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <line x1="220.0" y1="222.0" x2="220.0" y2="82.0" stroke="currentColor" stroke-width="7" stroke-opacity="0.22" stroke-linecap="round"/>
  <path d="M 263.3 88.9 A 140.0 140.0 0 0 0 103.9 143.7" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6" stroke-dasharray="4 4"/>
  <circle cx="80.0" cy="222.0" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="220.0" cy="222.0" r="10" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="220.0" cy="222.0" r="5.5" fill="currentColor"/>
  <circle cx="220.0" cy="82.0" r="5.5" fill="currentColor"/>
  <line x1="212.0" y1="82.0" x2="168.0" y2="82.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#aCork)"/>
  <text x="190.0" y="73.0" font-size="12" fill="currentColor" text-anchor="middle">v = 2 m/s</text>
  <line x1="228.0" y1="90.0" x2="228.0" y2="134.0" stroke="currentColor" stroke-width="2" marker-end="url(#aCork)"/>
  <text x="236.0" y="106.0" font-size="12" fill="currentColor">말단 질량에 4 N,</text>
  <text x="236.0" y="121.0" font-size="12" fill="currentColor">안쪽으로: m ω² r = 1·2²·1</text>
  <line x1="228.0" y1="210.0" x2="228.0" y2="166.0" stroke="currentColor" stroke-width="2" marker-end="url(#aCork)"/>
  <text x="236.0" y="178.0" font-size="12" fill="currentColor">엘보에 4 N,</text>
  <text x="236.0" y="193.0" font-size="12" fill="currentColor">아래팔을 따라 바깥으로</text>
  <line x1="80.0" y1="232.0" x2="80.0" y2="261.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="220.0" y1="234.0" x2="220.0" y2="261.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="81.0" y1="256.0" x2="219.0" y2="256.0" stroke="currentColor" stroke-width="1.1"/>
  <path d="M88.0 252.5 L81.0 256.0 L88.0 259.5" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <path d="M212.0 252.5 L219.0 256.0 L212.0 259.5" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="150.0" y="273.0" font-size="12" fill="currentColor" text-anchor="middle">1 m: 어깨에 대한 그 힘의 모멘트 팔</text>
  <path d="M 57.4 213.8 A 24.0 24.0 0 0 1 102.6 213.8" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#aCork)"/>
  <text x="22.0" y="172.0" font-size="12" fill="currentColor">τ<tspan dy="3" font-size="10">1</tspan><tspan dx="3" dy="-3">= −4 N·m</tspan></text>
  <text x="22.0" y="187.0" font-size="11" fill="currentColor" fill-opacity="0.85">관절 1을 제자리에 붙든다</text>
  <text x="236.0" y="226.0" font-size="11" fill="currentColor" fill-opacity="0.85">τ₂ = 0: 그 힘은 엘보 축을 지난다</text>
</svg>

관절 1은 멈춰 있고 관절 2가 $2\,\mathrm{rad/s}$로 휘돈다. 말단 질량은 엘보 둘레의 원(점선)을 $2\,\mathrm{m/s}$로 돌고, 아래팔이 그것을 $4\,\mathrm N$으로 안쪽으로 당기며, 그 반작용이 엘보를 $4\,\mathrm N$으로 바깥으로 당기는데 그 힘의 어깨에 대한 모멘트 팔이 $1\,\mathrm m$다. $h\dot\theta_2^2=(-1)(2)^2=-4\,\mathrm{N{\cdot}m}$가 상쇄하는 것이 이 $+4\,\mathrm{N{\cdot}m}$이고, 그 힘은 엘보 축을 지나므로 $\tau_2=0$이다.

독립 관절 제어가 속도에 따라 나빠지는 두 번째 이유이고, 저속에서 좋은 추종 성능을 보고하는
논문이 보이는 것보다 약한 주장을 하고 있는 이유이기도 하다: 저속에서는 방정식의 어려운 항들이
거의 0이다.

> [!note]- 더 깊이 · Deeper
> **반대칭 성질, 그리고 그것이 사 주는 수동성 단계.** 논문들은 $\dot M - 2C$가 반대칭(skew-symmetric, $A^\top = -A$인 행렬이라 모든 $x$에 대해 $x^\top A x = 0$; [[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §1]] 참고)이 되는 $C$의 분해를 고른다. 2R 팔에서는 위의 크리스토펠 $C$이고, 그 $\dot M-2C$가 반대칭임을 위에서 확인했다. 대부분의 안정성 증명이 그 항등식을 쓰기 때문이다. 어떤 운동에서든 운동에너지의 변화율은 $\frac{d}{dt}\big(\tfrac12\dot\theta^\top M\dot\theta\big)=\dot\theta^\top M\ddot\theta+\tfrac12\dot\theta^\top\dot M\dot\theta$이고, 매니퓰레이터 방정식의 $M\ddot\theta=\tau-C\dot\theta-g$를 대입하면
> $$\frac{d}{dt}\Big(\tfrac12\dot\theta^\top M\dot\theta\Big)=\dot\theta^\top(\tau-g)+\tfrac12\dot\theta^\top(\dot M-2C)\,\dot\theta=\dot\theta^\top(\tau-g)$$
> 가 된다. 가운데 반대칭 항이 0이기 때문이다. 그래서 속도 항은 일을 하지 않는다. 운동에너지는 모터와 중력의 일률만큼만 변한다. 에너지를 저장하고 흩뜨릴 수는 있어도 만들어 내지는 못하는 시스템을 **수동적**(passive)이라 하고, 이 항등식이 **리아푸노프** 안정성 증명, 곧 에너지 같은 양이 줄어들 수밖에 없으니 운동이 가라앉는다는 논증의 수동성 단계다. 위의 $C$로 $\theta=(0°,90°)$, $\dot\theta=(1,2)$ rad/s에서 계산하면 $\tfrac12\dot\theta^\top\dot M\dot\theta=-6$, $\dot\theta^\top C\dot\theta=-6$이라 둘이 상쇄된다.

### 5. 중력, 역동역학, 계산 토크

아무도 붙들지 않은 팔은 떨어진다. 카탈로그 자세에서 놓은 P2는 $9.81\,\mathrm{rad/s^2}$로 떨어지기 시작한다(§2). 그래서 제어기 토크의 상당 부분은 그냥 팔을 들고 있는 데 쓰이고, 그 토크는 무게가 어디 있는지 알 때만 맞게 낼 수 있다. 이 절은 유지 토크를 위치 에너지에서 유도해 자유물체도로 검산하고, 이어서 방정식 전체로 팔 자신의 동역학을 상쇄한다. 그것이 계산 토크다.

중력은 위치 에너지를 미분해서 나온다(유지 토크를 순수한 정역학, 곧 무게 곱하기 모멘트 팔로 본 것은 [[02-foundations/basic-mechanics|0.6.1 기초 역학 §8]]이다). $g(\theta)$의 $i$번째 원소는 관절 $i$가 돌 때 위치 에너지가 늘어나는 비율이다:
$$g(\theta) = \frac{\partial V}{\partial\theta}, \qquad V(\theta) = m_1 g L_1\sin\theta_1 + m_2 g\,(L_1\sin\theta_1 + L_2\sin\theta_{12})$$
각 항은 무게 곱하기 1번 관절 위의 높이이고, 각도는 수평에서 재며 $\theta_{12} = \theta_1 + \theta_2$다. 그래서 같은 팔에 대해 미분하면 ($g = 9.81$ m/s²):

$$g_1(\theta) = (m_1{+}m_2)\,g\,L_1\cos\theta_1 + m_2\,g\,L_2\cos\theta_{12}, \qquad g_2(\theta) = m_2\,g\,L_2\cos\theta_{12}$$

($\theta_{12} = \theta_1 + \theta_2$). $\theta = (0°, 90°)$에서는 아래팔이 똑바로 위를
향하므로 $\cos\theta_{12} = 0$이고

$$g_1 = 2(9.81)(1) + 0 = 19.62\ \text{N}\cdot\text{m}, \qquad g_2 = 0$$

물리로 검산하라: 두 질량 모두 1번 관절에서 수평으로 1 m 떨어져 있으므로 어깨는
$2 \times 9.81 \times 1$을 진다. 아래팔 질량은 2번 관절 바로 위에 있어 지렛대 팔이 0이므로
팔꿈치는 아무것도 지지 않는다. 방정식과 자유물체도가 일치한다 — 이 검산은 반드시 하라.
$g(\theta)$의 부호 오류가 동역학에서 가장 흔한 버그다.

같은 자세의 §4 예제와 합쳐 보자: 팔이 이 수직 평면에서 움직이고 2번 관절이 2 rad/s로 휘두르면, 1번 관절은 제자리에 있기 위해서만 중력과 코리올리 항을 합친 $19.62 - 4 = 15.62$ N·m가 필요하다.

매니퓰레이터 방정식을 **오른쪽에서 왼쪽으로** 읽는 것 — 원하는 운동이 주어졌을 때 어떤 토크가
필요한가? — 이 **역동역학**이며, 모델 기반 제어의 토대다:

$$\tau = M(\theta)\,\ddot\theta_{\text{des}} + C(\theta,\dot\theta)\,\dot\theta + g(\theta)$$

여기에 오차 피드백을 더하면 **계산 토크 제어**가 된다: 모델이 팔 자신의 비선형성을 상쇄하고,
모델이 틀린 부분은 단순한 선형 제어기가 맡는다. 이것이 이 방법의 정직한 설명이다 — 성능은
§7의 파라미터가 정확한 만큼만 좋으며, 그래서 실기계에서 날것 그대로 쓰이는 일은 드물다.

추종 오차 $e = \theta_{\text{des}} - \theta$와 게인 행렬 $K_p$, $K_d$로 쓰면 제어기는
$$\tau = M(\theta)\big(\ddot\theta_{\text{des}} + K_d\,\dot e + K_p\,e\big) + C(\theta,\dot\theta)\,\dot\theta + g(\theta)$$
이다. 매니퓰레이터 방정식에 대입하면 $M(\theta)(\ddot e + K_d\dot e + K_p e) = 0$이고, $M$이 가역이므로 모델이 정확할 때 $\ddot e + K_d\dot e + K_p e = 0$이다. 자세와 상관없이 모든 관절이 독립된 선형 질량-스프링-댐퍼가 된다. 그 오차 방정식을 표준 2차 꼴 $\ddot e+2\zeta\omega_n\dot e+\omega_n^2e=0$에 맞추면 응답을 기술하는 두 숫자에 이름이 붙는다([[02-foundations/basic-mechanics|0.6.1 기초 역학 §5]]가 세 영역과 함께 둘 다 정의한다). 오차를 얼마나 빨리 끌어당기는지인 **고유 진동수** $\omega_n=\sqrt{K_p}$, 그리고 오버슈트 여부를 정하는 **감쇠비** $\zeta=K_d/(2\sqrt{K_p})$다($\zeta<1$이면 진동하고, $\zeta>1$이면 느리게 기어 돌아오며, 임계 감쇠라 부르는 $\zeta=1$은 오버슈트 없이 가장 빨리 돌아오는 경우다). 관절마다 $K_p = 100$, $K_d = 20$이면 $\omega_n=\sqrt{100} = 10$ rad/s, $\zeta=20/(2\sqrt{100}) = 1$로 임계 감쇠다(이런 게인의 설계는 [[04-robotics/control-theory-ce397|5. 제어 이론 §7]]). 반례: 모델 없는 독립 관절 PD $\tau = K_p e + K_d\dot e$는 폐루프에 $M(\theta)$가 남으므로, §3의 5배 관성 변화가 응답의 빠르기와 감쇠를 바꾼다.

### 6. 작업공간(operational space) 동역학 — 힘 제어로 가는 다리

*한 문장으로:* 공구 끝에서 보면 팔은 어떤 방향으로는 더 무겁고 어떤 방향으로는 더 가벼우며 팔이 움직이면 바뀌는 질량처럼 행동하고, 끝을 미는 힘이 운동으로 바뀌는 방식을 그 겉보기 질량이 정한다.

*이 절에서 하나만 가져간다면:* 작업공간 관성 $\Lambda=(JM^{-1}J^\top)^{-1}$ — P2의 $\theta=(0°,90°)$에서 $\mathrm{diag}(1,2)$ kg이어서, 팔이 실제로 2 kg을 싣고 있는데도 끝은 옆으로 밀면 1 kg, 위로 밀면 2 kg처럼 느껴진다. 완전한 작업공간 방정식 바로 뒤에서 2R 팔로 계산한다.

여기까지는 전부 관절 공간이다. 접촉은 그렇지 않다: 접촉은 말단에서, 작업공간에서 일어난다.
그 변환이 이 페이지에서 가장 중요한 방정식이다.

여기서 말하는 **작업공간**은 Khatib의 *operational space* — 말단의 위치·자세를 좌표로
삼는 공간 — 이지, 팔이 닿을 수 있는 부피를 뜻하는 *workspace*가 아니다. 이 위키는 후자를
**작업 영역**이라 부른다.

**$\Lambda$는 어디서 오는가: 잇따른 사상 셋.** 팔을 정지시키고 중력과 속도 항은 잠시 제쳐 두자. 말단의 힘 $\mathcal{F}$는 $J^\top$를 통해 관절 토크가 되고(§1), 관절 토크는 $M^{-1}$을 통해 관절 가속도가 되며(§2의 순동역학), $J$가 그 가속도를 다시 말단으로 옮긴다. 정지 상태에서는 $\dot v=J\ddot\theta$가 정확히 성립하므로
$$\dot v = J\ddot\theta = J M^{-1} J^\top \mathcal{F}$$
이고, 그래서 곱 $JM^{-1}J^\top$는 "여기서 이 힘이 말단 가속도를 얼마나 만드는가"에 답하며, 그 역은 반대 질문, 곧 말단 가속도 하나에 어떤 힘이 드는가($\mathcal{F}=\Lambda\dot v$)에 답한다. 말단의 유효 질량은

$$\Lambda(\theta) = \left(J(\theta)\,M^{-1}(\theta)\,J^\top(\theta)\right)^{-1}$$

$\Lambda$는 **작업공간 관성 행렬**이다 — 밖에서 볼 때 말단이 각 작업공간 방향에서 *가진
것처럼 보이는* 질량. 그다음 작업공간의 힘 명령은 $\tau = J^\top \mathcal{F}$로 관절 토크가
된다. MR 5장의 정역학 쌍대성이 결국 매니퓰레이션 트랙 전체를 떠받치는 결과인 이유가 이것이다.

**모든 항에 이름을 붙인 완전한 작업공간 방정식.** 순동역학에 $\tau = J^\top\mathcal{F}$를 대입하고 $\dot v = J\ddot\theta + \dot J\dot\theta$를 쓰면, 정사각이고 가역인 $J$에 대해
$$\mathcal{F} = \Lambda(\theta)\,\dot v + \Lambda(\theta)\big(J M^{-1} C\,\dot\theta - \dot J\,\dot\theta\big) + \Lambda(\theta)\,J M^{-1} g(\theta)$$
이다. $v$는 말단 속도, $\dot v$는 그 가속도, $\mathcal{F}$는 끝점에 가하는 힘(렌치)이다. 그래서 끝점 힘에는 세 가지 일이 있다: 겉보기 질량 $\Lambda$를 가속하고, 끝점에서 본 속도 항을 상쇄하고, 끝점에서 본 중력을 떠받친다. MR 식 8.90 $\mathcal{F} = \Lambda\dot v + \eta$에서 $\eta$를 풀어 쓴 것이다.

**계산: 2R 팔, $\theta = (0°, 90°)$.** §1에서 그 자세의 끝점 야코비안은
$J = \begin{pmatrix}-1 & -1\\ 1 & 0\end{pmatrix}$이고, §3에서
$M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$, $\det M = 2$이므로

$$M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}, \qquad JM^{-1} = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}$$

$$JM^{-1}J^\top = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}\begin{pmatrix}-1&1\\-1&0\end{pmatrix} = \begin{pmatrix}1&0\\0&0.5\end{pmatrix} \quad\Longrightarrow\quad \Lambda = \begin{pmatrix}1&0\\0&2\end{pmatrix}$$

중력 항도 같은 방식으로 검산된다. 여기서 정지 상태라면 $\Lambda J M^{-1} g = J^{-\top} g$는 토크 $J^\top\mathcal{F}$가 §5의 $g = (19.62, 0)$ N·m와 같아지는 끝점 힘, 곧 $\mathcal{F} = (0,\ 19.62)$ N이다. 똑바로 위를 향하고 팔 전체 2 kg의 무게와 같다. 끝점이 두 질량처럼 1번 관절에서 수평으로 1 m 떨어져 있고, 아래팔 질량처럼 2번 관절 바로 위에 있기 때문에 맞는 답이다.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="엘보 90도인 P2의 같은 말단에서 두 타원: 반축이 1.62와 0.62 m/s이고 긴 축이 −31.7도로 기운 J J 전치의 속도 타원, 그리고 옆으로 1 kg, 위로 2 kg인 곧게 선 Λ의 겉보기 질량 타원">
  <text x="150.0" y="24" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">속도 타원, J J<tspan dy="-5" font-size="10">T</tspan></text>
  <text x="150.0" y="42.0" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="middle">단위 관절 속도가 내는 말단 속도</text>
  <ellipse cx="150.0" cy="128.0" rx="84.1" ry="32.1" transform="rotate(31.7 150.0 128.0)" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.4"/>
  <line x1="150.0" y1="128.0" x2="221.6" y2="172.2" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <line x1="150.0" y1="128.0" x2="166.9" y2="100.7" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="225.6" y="186.2" font-size="11" fill="currentColor">1.62 m/s</text>
  <text x="170.0" y="95.0" font-size="11" fill="currentColor">0.62 m/s</text>
  <line x1="50.0" y1="128.0" x2="250.0" y2="128.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <line x1="150.0" y1="54.0" x2="150.0" y2="218.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <circle cx="150.0" cy="128.0" r="3.5" fill="currentColor"/>
  <text x="150.0" y="232.0" font-size="11" fill="currentColor" text-anchor="middle">긴 축 −31.7°</text>
  <text x="420.0" y="24" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">겉보기 질량 타원, Λ</text>
  <text x="420.0" y="42.0" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="middle">말단을 미는 힘이 느끼는 질량</text>
  <ellipse cx="420.0" cy="128.0" rx="38.0" ry="76.0" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.4"/>
  <line x1="420.0" y1="128.0" x2="458.0" y2="128.0" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <line x1="420.0" y1="128.0" x2="420.0" y2="52.0" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="462.0" y="146.0" font-size="11" fill="currentColor">옆으로 1 kg</text>
  <text x="448.0" y="62.0" font-size="11" fill="currentColor">위로 2 kg</text>
  <line x1="320.0" y1="128.0" x2="520.0" y2="128.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <line x1="420.0" y1="54.0" x2="420.0" y2="218.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"/>
  <circle cx="420.0" cy="128.0" r="3.5" fill="currentColor"/>
  <text x="420.0" y="232.0" font-size="11" fill="currentColor" text-anchor="middle">곧게 섬</text>
  <text x="280" y="254" font-size="12" fill="currentColor" text-anchor="middle">같은 팔, 같은 자세, 같은 J: 크기만 다른 한 모양이 아니라 서로 다른 두 모양</text>
</svg>

같은 자세의 같은 말단을 두 방식으로 그린 것이다. $JJ^\top$의 속도 타원, 곧 단위 관절 속도가 낼 수 있는 말단 속도는 반축이 $1.62$와 $0.62\,\mathrm{m/s}$이고 긴 축이 $-31.7^\circ$로 기울어 있지만, $\Lambda=\mathrm{diag}(1,2)$의 겉보기 질량 타원은 옆으로 $1\,\mathrm{kg}$, 위로 $2\,\mathrm{kg}$로 곧게 서 있다. 크기만 다른 한 모양이 아니라 서로 다른 두 모양이고, 각각 다른 입력을 가정하기 때문이다(아래 *더 깊이* 메모가 셋을 견준다).

결과를 읽자. 팔에 실린 실제 질량은 2 kg인데, 끝점을 옆으로 밀면 **1 kg**처럼, 위로 밀면
**2 kg**처럼 거동한다 — 같은 자세에서, 순전히 기하 때문에 두 배 차이가 난다. 힘 제어 문헌이
독자가 이미 소화했다고 가정하는 두 귀결:

- **충격력은 방향에 의존한다.** 같은 속도로 단단한 면을 치면 무거운 방향에서 두 배의 운동량이
  전달된다. 한 축으로는 안전하게 삽입하는 그리퍼가 다른 축으로는 부재를 손상시킬 수 있다.
- **하나의 강성 게인이 모든 방향에서 옳을 수 없다.** 임피던스 제어기([[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어 §2]])의 폐루프 거동은
  $\Lambda$에 의존하므로, 같은 게인이 방향과 자세에 따라 다른 유효 동역학을 준다.

**스윕: 모든 팔꿈치 각도에서의 같은 팔.** 자세 하나로는 작업 영역 전체에서 일해야 하는 제어기에 대해 알 수 있는 것이 적으니, 엘보를 훑어 보자. 영어 판의 루프는 $\theta_1=0$으로 두고 각 $\theta_2$에서 §3의 $M$과 §1의 $J$를 만들어 $M_{11}$, $\det J$, 그리고 $\Lambda$의 두 고유값, 곧 말단의 가장 가벼운 방향과 가장 무거운 방향의 겉보기 질량을 출력한다.

| $\theta_2$ (°) | $M_{11}$ | $\det J$ | 가장 가벼운 방향 (kg) | 가장 무거운 방향 (kg) |
|---:|---:|---:|---:|---:|
| 10 | 4.97 | 0.174 | 1.000 | 34.163 |
| 30 | 4.73 | 0.500 | 1.000 | 5.000 |
| 50 | 4.29 | 0.766 | 1.000 | 2.704 |
| 70 | 3.68 | 0.940 | 1.000 | 2.132 |
| 90 | 3.00 | 1.000 | 1.000 | 2.000 |
| 110 | 2.32 | 0.940 | 1.000 | 2.132 |
| 130 | 1.71 | 0.766 | 1.000 | 2.704 |
| 150 | 1.27 | 0.500 | 1.000 | 5.000 |
| 170 | 1.03 | 0.174 | 1.000 | 34.163 |

세 가지로 읽는다. 가장 가벼운 방향은 언제나 정확히 $1\,\mathrm{kg}$, 곧 말단 자신의 점질량이다. 그 질량은 어느 쪽으로 밀든 말단과 함께 움직이고, 아래팔을 가로지르는 방향으로 밀면 아래팔이 엘보 둘레로 돌기만 해서 엘보 질량은 가만히 있다. 아래팔을 따라 밀면 엘보 질량도 말단보다 $1/\lvert\sin\theta_2\rvert$배 빠르게 움직여야 하므로, 가장 무거운 방향은 $1+1/\sin^2\theta_2$ kg이다. $90^\circ$에서 $2$, $30^\circ$와 $150^\circ$에서 $5$, $10^\circ$와 $170^\circ$에서 $34.2$이고, $\det J=\sin\theta_2$가 0으로 갈수록 한없이 커진다. 그리고 관절 1 자신의 관성인 $M_{11}$은 약 $5$에서 약 $1$로 꾸준히 줄지만 $\Lambda$는 $90^\circ$를 중심으로 대칭이다. 같은 팔의 관절 공간 그림과 작업공간 그림은 다른 질문에 답한다. §8의 Mastery 시험이 이 표 안에 있다. 특이 자세 근처에서 무거운 방향으로 접촉을 밀어 넣으면 무거운 말단을 만나고, 그 충돌은 더 세게 친다.

> [!note]- 더 깊이 · Deeper
> **"타원체"라 불리는 행렬 셋.** MR 5장의 가조작성 타원체와의 관계는 정성적이지, 행렬의 정확한 역수 관계는 아니다. 서로 다른 세 행렬이 모두 "타원체"라고 불리며, 각각 다른 입력을 가정한다:
>
> | 구성 | 형상 행렬 | 가정하는 입력 | 답하는 질문 | 2R 팔, $(0°, 90°)$ |
> |---|---|---|---|---|
> | 기구학적 가조작성 (MR 5장) | $JJ^\top$ | 단위 관절속도 노름 | 어떤 끝점 속도를 쉽게 낼 수 있나? | $\begin{pmatrix}2&-1\\-1&1\end{pmatrix}$ |
> | 작업공간 관성 (이 절) | $JM^{-1}J^\top$ | 동역학 보상 뒤의 과제 렌치 | 끝점 힘이 끝점 가속도를 얼마나 만드나? | $\begin{pmatrix}1&0\\0&0.5\end{pmatrix}$ |
> | 동적 가속도 타원체 | $JM^{-2}J^\top$ | 단위 **유클리드 관절토크** 노름 | 단위 모터 토크로 어떤 끝점 가속도를 낼 수 있나? | $\begin{pmatrix}1&0.5\\0.5&0.5\end{pmatrix}$ |
>
> 마지막 열이 요점을 보여 준다: 같은 자세에서 세 행렬은 크기만이 아니라 모양 자체가 다르다. 관성과 노름을 특별하게 고를 때만 서로
> 일치한다. 특이점 근처에서 셋 모두 잃어버린 과제 방향을 드러내지만, 노름을 밝히지 않고 축 길이가
> 정확한 역수라고 부르면 안 된다.
>
> **역행렬이 안전할 때.** 아래 단서들은 특이하거나 거의 특이한 행렬을 뒤집고, 거기서 나온 거대한 숫자를 믿는 일을 막아 준다.
>
> 보통의 역행렬에는 행 전체가 독립인 작업 자코비안과 양의 정부호 관성 행렬이 필요하다. 자코비안의 랭크가 떨어져 어떤 관절 속도로도 만들 수 없는 끝점 속도가 생기는 자세를 **특이** 자세라 한다([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §4]]). $m$차원 작업이라면 다음 조건이다:
> $$\operatorname{rank} J(\theta) < m$$
> 이 2R 팔은 $\det J = L_1L_2\sin\theta_2$이므로 $\theta_2 = 0°$와 $180°$(뻗거나 접힘)에서 특이하고, 위에서 쓴 $90°$ 자세에서는 $\det J = 1$이다. 특이 자세 부근에서는 조건이 나쁜 행렬을 무작정 뒤집기 전에 잃는 작업 방향을 확인한다. 작업 차원을 줄이거나 정규화하면 명령할 수 있는 내용이 바뀐다. 물리적으로 불가능한 방향이 되살아나는 것은 아니다. 이 가속도 해석은 나머지 항을 처리한 경우다. 움직이는 자코비안을 미분하면 $\dot J\dot\theta$도 생긴다: $\dot v = J\ddot\theta + \dot J\dot\theta$이므로 완전한 작업공간 방정식에는 사상된 코리올리·중력 항 옆에 속도 항 $\Lambda\dot J\dot\theta$가 더 붙는다. 팔이 정지해 있으면 0이라 위의 국소 해석에서는 빼도 되지만, 빠른 운동을 추종하는 작업공간 제어기는 모델 보상에 이 항을 넣어야 한다.

### 7. 파라미터는 어디서 오는가 — 그리고 sim-to-real 격차

§2의 모든 기호 뒤에는 누군가 측정해야 했던 숫자가 있다: 링크 질량, 질량 중심, 관성 텐서,
관절 마찰, 모터 상수, 감속기 탄성. 모터 상수와, 감속기가 $M$에 더하는 회전자 관성은 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]에 있다. 끝 쪽의 20% 오차만으로도 벌써 느껴진다. 케이블 다발과 커버로 P2의 말단 질량이 $1.2\,\mathrm{kg}$가 되면 §5의 유지 토크 $19.62\,\mathrm{N{\cdot}m}$는 $9.81\,(1+1.2)=21.58\,\mathrm{N{\cdot}m}$가 되고, 중력 보상하는 팔은 이 $2\,\mathrm{N{\cdot}m}$의 오차를 한결같은 처짐으로 보인다. 정직한 관찰 셋:

1. **CAD 값은 가장자리에서 틀린다.** 케이블, 커버, 실제 공구는 CAD 모델에 거의 없고, 하필
   그것들이 관절에서 가장 먼 곳 — 가장 크게 작용하는 곳 — 에 있다.
2. **마찰이 가장 나쁘게 모델링된 항**이며 이상적인 방정식에는 아예 없다. 실제 제어기는
   유도된 것이 아니라 피팅된 마찰 모델을 들고 다닌다. 그 피팅에 이름을 붙이고 실패 방식까지
   말하는 곳이 [[05-construction-robotics/sim-to-real|Sim-to-Real §2]]다. 시스템 식별은 측정
   궤적에 시뮬레이터 파라미터를 맞추는 일이고, 기계 하나와 운전 조건 하나에 과적합될 수 있다.
3. **이 파라미터 불일치는 동역학 쪽의 주요 sim-to-real 원인 중 하나다.** 인식, 시간 동기화,
   제어 인터페이스, 접촉, 액추에이터, 과제 분포가 지배적일 수도 있다. 동기화 로그와 절제로
   최초 실패 층을 분리한다([[06-research-practice/failure-analysis-system-evaluation|실패 분석·시스템 평가]]).

건설 조작에는 네 번째가 있다: **페이로드가 알려져 있지 않고 크다.** 잡은 패널이나 볼트는
$M(\theta)$와 $g(\theta)$를 팔 자신의 링크에 견줄 만큼 바꾸며, 공장과 달리 그 질량을
하드코딩할 수 없다. 대신 팔이 자기 토크로 그것을 식별할 수 있다. 토크는 몇 개의 기저 관성 파라미터에 선형이고($\tau=Y\pi$), [[04-robotics/system-identification|5.5 시스템 식별 §9]]가 $3\,\mathrm{kg}$ 페이로드를 최소제곱으로 되찾는 방법이 이것이다.

### 8. 논문에서 동역학 읽기, 그리고 Mastery로 가는 길

매니퓰레이션 논문이 동역학을 언급할 때, 실제 주장과 장식을 가르는 질문들:

- 제어기가 **토크 수준**인가, 아니면 벤더 제어기에 위치를 명령하는가? 위치 인터페이스라면
  내측 루프의 강성·대역폭·지연과 환경 강성을 포함한 전체 폐루프에서 컴플라이언스 주장을 평가한다.
- $M$, $C$, $g$가 **모델링되었나, 학습되었나, 무시되었나**? "중력 보상"만으로는 완전한
  역동역학보다 훨씬 약한 진술이다.
- 결과를 어떤 **속도**에서 얻었나? §4에 따르면 어려운 항들은 속도의 이차식이므로, 느린
  시연은 모델 오차를 숨긴다.
- **페이로드**가 모델에 있는가?

여기서 Mastery에 도달하려면 이 페이지가 줄 수 없는 세 가지가 필요하다:

| 필요한 것 | 어디서 |
|---|---|
| 완전한 유도(라그랑주·뉴턴–오일러, 재귀 알고리즘) | *Modern Robotics* 8장, [[04-robotics/modern-robotics-book\|책 가이드]] |
| 작업공간 제어 이론 | Khatib의 operational-space 정식화, 그다음 [[04-robotics/control-theory-ce397\|제어 이론]] |
| 파라미터 감각 | 강체 동역학 시뮬레이터 아무거나 — 링크 질량을 20% 바꾸고 튜닝된 제어기가 무너지는 것을 볼 것 |

이 페이지의 Mastery 시험: 팔과 자세와 방향이 주어졌을 때 접촉이 뻣뻣하게 느껴질지 무르게
느껴질지 예측하고, 맞히는 것.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 매니퓰레이터 방정식을 외워서 쓰고 각 항이 하는 일을 말한다.
- [ ] $M$에 왜 인자가 붙는지 5배 예제로 설명한다.
- [ ] $J$와 $M$에서 $\Lambda$를 계산하고 물리적으로 해석한다.
- [ ] $JJ^\top$의 속도 타원과 $\Lambda$의 겉보기 질량 타원을 각각이 가정하는 입력으로 구분한다(§6의 그림. 단위 토크 타원은 그 *더 깊이* 메모가 더한다).
- [ ] 매니퓰레이터 방정식에서 가장 부정확하게 모델링되는 항(마찰)을 대고 이유를 말하며, sim-to-real 격차를 지배할 수 있는 동역학 밖의 원인 두 가지를 댄다.

> [!tip] 더 깊이 · Going deeper
> [*Modern Robotics*](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) 8장이 이 페이지가 압축한 유도이고, §6의 작업공간 관성은 책의 8.6절(식 8.90)이며, 8장 주석이 이를 Khatib의 operational space formulation으로 소개한다. 그 위에 세운 제어는 11.4.3절(토크 입력의 task-space motion control)이고, 11.3.3절은 속도 입력의 기구학적 판본이며, 11.6절은 hybrid motion–force control로 다른 주제다. 8장은 뉴턴–오일러 재귀를 위해 읽어라. 매니퓰레이터 방정식이 *쓰이는* 방식이 아니라 실제로 *계산되는* 방식이 그것이다. 책이 주지 않는 것은 §7이다 — 파라미터가 어디서 오는지, 식별한 값과 CAD 값이 왜 어긋나는지. 그것은 유도가 아니라 실험의 문제이기 때문이다.

### 스스로 점검

1. $M(\theta)$는 양정치다. 이것이 시뮬레이션에 왜 중요한가?
2. 팔이 $\theta_2 = 0°$(곧게 뻗음)에 있다. $M$과 $h$를 계산하고, 거기서 코리올리 항이
   무엇을 하는지 말하라.
3. $\theta=(0°,90°)$에서 겉보기 질량이 옆으로 1 kg, 위로 2 kg인데 팔의 무게는 2 kg이다.
   겉보기 질량이 어떻게 실제 질량보다 *작을* 수 있는가?
4. 어떤 논문이 위치 제어 산업용 팔과 손목 힘 센서로 우수한 힘 추종을 보고한다. 무엇을
   확인해야 하는가?
5. 로봇이 3 kg 패널을 잡았다. 매니퓰레이터 방정식의 어느 항이 바뀌는가?

> [!tip]- 정답 · Answers
> 1. 양정치면 가역이므로 $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$가 언제나 유일한 해를 갖는다 — 시뮬레이터가 항상 한 스텝 적분할 수 있다. 또한 0이 아닌 임의의 운동에 대해 운동 에너지 $\tfrac12\dot\theta^\top M\dot\theta$가 순수하게 양수라는 뜻이고, 에너지 기반 안정성 논증이 성립하는 근거가 그것이다.
> 2. $\cos 0° = 1$이므로 $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$. 그리고 $h = -\sin 0° = 0$이므로 이 자세에서는 속도와 무관하게 코리올리·원심 항 전체가 사라진다. 일반적 사실이 아니라 진짜 특수한 경우다 — 팔꿈치를 $0°$나 $180°$에서 벗어나게 하면 결합이 돌아온다.
> 3. 끝점이 그 질량 전부에 강체로 붙어 있지 않기 때문이다 — 옆으로 밀면 팔이 회전해서 응답할 수 있으므로 관성의 일부만 저항한다. 겉보기 질량은 금속의 양이 아니라 *한 방향에서 끝점이 보이는 저항*을 잰다. 특이 극한에서는 반대 현상이 일어나 잃어버린 방향으로 $\Lambda$가 무한히 커진다.
> 4. 팔이 실제로 그 아래에서 토크 제어되는지 확인해야 한다. 뻣뻣한 위치 제어 내부 루프가 있다면 그 힘 "제어"는 작은 위치를 명령하는 외부 루프이고, 이는 벤더의 강성이 사이에 낀 어드미턴스 제어(힘을 재고 운동을 명령하는, 임피던스 제어와 인과가 반대인 제어, [[04-robotics/force-compliance-control|13. §2]])다 — 동작할 수는 있지만 안정성이 환경이 무르다는 데 의존하므로, 주장은 단단한 면에 대해 검증되어야 한다. [[04-robotics/contact-force-tactile|접촉·힘·촉각 §5]]를 보라.
> 5. $M(\theta)$와 $g(\theta)$가 모두 크게 바뀐다. 페이로드가 지렛대 팔이 가장 긴 맨 끝에 질량을 더하기 때문이고, $C$도 $M$을 따라 바뀐다. 이 예에서 패널은 움직이는 질량을 두 배 이상으로 만들므로, 무부하로 튜닝한 제어기는 부하 상태에서 크게 틀린다 — 부품 질량이 알려진 공장보다 건설에서 페이로드 인지 제어나 적응 제어가 더 중요한 이유다.

### 과제 · Problem set

Tier A (**P2**의 동역학 절반. §6의 스윕이 실습이고 3번이 그 변형을 돌린다. 속도 루프는 [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장]]에 있으니 여기서 시간 스테퍼를 하나 더 만들지 마라). [[02-foundations/lab-plants|0.6]]의 숫자, $\theta=(0^\circ,90^\circ)$:

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix},\quad M=\begin{pmatrix}3&1\\1&1\end{pmatrix},\quad \Lambda=\mathrm{diag}(1,2),\quad g=(19.62,\ 0)\,\mathrm{N{\cdot}m}$$

1번과 2번은 엘보를 카탈로그에 없는 $45^\circ$로 옮긴다. 식마다 먼저 $90^\circ$에서 이 숫자들이 다시 나오는지 확인하라.

1. **그리기.** 엘보를 $\theta=(0^\circ,45^\circ)$로 편 위의 그림. 여전히 연직면이고 $g$는 $-y$다. 점질량 둘과 무게 화살표, 관절마다 각 무게 작용선까지의 수평 모멘트 팔, 어깨/엘보 토크 $g(\theta)$, 그리고 말단 아래 패널에 $-y$로 $10\,\mathrm{N}$(*패널에* 가해지는 힘). 말단에 *가해지는* 힘에 뉴턴 3법칙을 써라. 위 그림에서 $0$이던 토크 가운데 여기서 $0$이 아닌 것은 무엇인가?
2. **유도.** 1번의 자세 $\theta=(0^\circ,45^\circ)$에서 정지. (a) 거기서 §1의 $J$와 §3의 $M$을 만든다. (b) §5의 유지 토크 $g(\theta)$와, 패널에 $F_\text{cmd}=(0,-10)\,\mathrm{N}$을 명령할 때의 토크 $\tau=g+J^\top F_\text{cmd}$. 밀기가 어느 관절을 거의 풀어 주며, 왜인가? (c) $\Lambda=(JM^{-1}J^\top)^{-1}$와 그 두 고유값, 그리고 각 고유값의 방향. (d) 속도 항이 0일 때 $\dot v=(0,1)\,\mathrm{m/s}^2$를 만드는 말단 렌치 $\mathcal{F}=\Lambda\dot v$와 그 관절 토크 $J^\top\mathcal{F}$. 똑바로 위로 가속하는데 왜 똑바로 위가 아닌 힘이 드는가?
3. **실행.** 말단에 $1\,\mathrm{kg}$ 공구를 물려 말단 질량을 $m_2=2\,\mathrm{kg}$로 만든다. 영어 템플릿의 `?` — §3의 부하 질량 행렬과 §6의 $\Lambda$ — 를 채우고 스윕을 돌려라. $90^\circ$에서 $\Lambda$의 두 고유값, 공구가 각 방향에 얼마를 더했는지와 그 이유, 그리고 부하가 걸린 팔의 무거운 방향이 여전히 $0^\circ$와 $180^\circ$ 쪽으로 한없이 커지는지 보고하라.

> [!note]- 그리는 법 · How to draw it
> - 팔은 연직면에 실제 비율로 그린다. 베이스는 원점, 링크 1이 $+x$를 따라 엘보 $(1,0)$까지, 링크 2가 $45^\circ$로 바깥 위를 향해 말단 $(1.707,\ 0.707)$까지 가고, 여백에 $-y$ 방향 중력 화살표를 그려 아래쪽을 확정한다.
> - 링크는 질량 없는 막대로 그리고, 각 링크의 *말단 쪽 끝*에 $1\,\mathrm{kg}$짜리 검은 점을 찍어 거기서 아래로 $9.81\,\mathrm{N}$짜리 무게 화살표를 긋는다. 카탈로그의 점질량 규약이 모든 숫자를 만들어 내고, 질량을 링크 중앙에 찍으면 다른 팔이 된다.
> - 관절마다 그 축에서 각 무게 작용선까지의 수평 거리를 그리고 값을 적는다. 모멘트 팔은 링크 길이가 아니라 그 수평 간격이다. 말단의 무게 작용선이 이제 엘보 축을 지나지 않으며, 둘 사이의 간격이 새 숫자다.
> - 중력 토크는 관절의 곡선 화살표로 적고 둘 다 값을 쓴다. 엘보 값은 위 그림에서 $0$이던 것이다.
> - 말단 아래에 패널을 수평면으로 그리고(전완은 도면 평면 밖으로 패널 앞을 지나가므로 패널에 닿는 것은 말단뿐이다), 명령한 힘은 *패널로* 향하는 아래 화살표로, 그 반작용은 같은 길이의 위 화살표로 *말단에* 그린다. 살짝 어긋나게 그려 한 화살표를 두 번 그린 것이 아니라 쌍임이 보이게 한다.
> - 각 힘이 어느 물체에 작용하는지 적는다. 이 트랙 뒷부분의 부호 실수는 거의 전부 이 쌍이고, 이 쌍은 자세에 따라 바뀌지 않는다.
> - 겉보기 질량 타원을 더한다면 2번의 것을 말단에 그린다. 반축은 $1$과 $3\,\mathrm{kg}$이고 짧은 반축은 아래팔을 가로질러, 긴 반축은 아래팔을 따라 놓이므로, 이 자세의 타원은 위 그림처럼 곧게 서지 않고 아래팔과 함께 $45^\circ$ 기운다. 이것은 [[02-foundations/linear-algebra|1. 선형대수 §4.5]]의 조작성 타원이 아니다. 그쪽은 속도에, 이쪽은 질량에 살며, §6이 고정 자세에서 둘을 나란히 그린다.

> [!tip]- 정답 · Solutions
> 1. 엘보 $(1,0)$, 말단 $(1+\cos45^\circ,\ \sin45^\circ)=(1.707,\ 0.707)$이고 질량은 그 두 점에 있다. 모멘트 팔: 어깨에서 엘보 질량까지 $1$ m, 말단 질량까지 $1.707$ m, 엘보에서 말단 질량까지 $0.707$ m. 유지 토크 $g(\theta)=(9.81(1+1.707),\ 9.81\times0.707)=(26.56,\ 6.94)\,\mathrm{N{\cdot}m}$. 고정 자세에서는 말단이 엘보 바로 위에 있어 $0$이던 엘보 토크가 이제 $6.94\,\mathrm{N{\cdot}m}$이다. 전완이 바깥으로 기울어 그 무게 작용선이 엘보 축을 벗어났기 때문이다. 패널에 $(0,-10)$ $\Rightarrow$ 말단에 $(0,+10)$으로, 앞과 같은 쌍이다. 뉴턴 3법칙은 자세에 매이지 않는다.
> 2. (a) $c=s=0.707$이므로 $J=\begin{pmatrix}-0.707&-0.707\\1.707&0.707\end{pmatrix}$, $\det J=\sin45^\circ=0.707$이고 $M=\begin{pmatrix}4.414&1.707\\1.707&1\end{pmatrix}$, $\det M=1+\sin^2 45^\circ=1.5$다. (b) $g=(26.56,\ 6.94)\,\mathrm{N{\cdot}m}$로 1번의 토크다. $J^\top F_\text{cmd}=(-17.07,\ -7.07)$이므로 $\tau=(9.49,\ -0.13)\,\mathrm{N{\cdot}m}$. 밀기가 엘보를 거의 풀어 준다. 엘보에 대해 패널의 반작용 $10\,\mathrm N$과 말단의 무게 $9.81\,\mathrm N$이 $0.707\,\mathrm m$ 밖의 같은 연직선 위에서 작용해 거의 상쇄되고, 남는 $0.19\,\mathrm N$ 때문에 엘보 모터가 $-0.13\,\mathrm{N{\cdot}m}$를 낸다. (c) $JM^{-1}J^\top=\tfrac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$이므로 $\Lambda=\begin{pmatrix}2&1\\1&2\end{pmatrix}\,\mathrm{kg}$이고 고유값은 $1$과 $3\,\mathrm{kg}$다. 아래팔을 가로지르는 $(-0.707,\ 0.707)$ 방향으로 $1\,\mathrm{kg}$, 아래팔을 따르는 $(0.707,\ 0.707)$ 방향으로 $3\,\mathrm{kg}=1+1/\sin^2 45^\circ$로, 스윕이 건너뛴 자세에서 본 §6의 읽기다. (d) $\mathcal{F}=\Lambda(0,1)=(1,\ 2)\,\mathrm N$, $J^\top\mathcal{F}=(2.71,\ 0.71)\,\mathrm{N{\cdot}m}$. 위쪽 가속도는 아래팔을 따라 $0.707$, 가로질러 $0.707$로 나뉜다. 앞의 것은 $3\,\mathrm{kg}$을, 뒤의 것은 $1\,\mathrm{kg}$을 만나므로 힘 $3(0.707)(0.707,\ 0.707)+1(0.707)(-0.707,\ 0.707)=(1,\ 2)$는 연직에서 아래팔 쪽으로 $26.6^\circ$ 기운다. 힘과 가속도는 $\Lambda$의 두 축을 따를 때만 평행하다. 카탈로그 자세에서는 그 축이 $x$와 $y$였으므로 거기서 $(0,1)\,\mathrm{m/s^2}$에는 곧게 선 $(0,\ 2)\,\mathrm N$이면 되었다.
> 3. 빈칸은 영어 해를 보라. 출력은
>
>    | $\theta_2$ (°) | $M_{11}$ | 가장 가벼운 방향 (kg) | 가장 무거운 방향 (kg) |
>    |---:|---:|---:|---:|
>    | 10 | 8.94 | 2.000 | 35.163 |
>    | 30 | 8.46 | 2.000 | 6.000 |
>    | 50 | 7.57 | 2.000 | 3.704 |
>    | 70 | 6.37 | 2.000 | 3.132 |
>    | 90 | 5.00 | 2.000 | 3.000 |
>    | 110 | 3.63 | 2.000 | 3.132 |
>    | 130 | 2.43 | 2.000 | 3.704 |
>    | 150 | 1.54 | 2.000 | 6.000 |
>    | 170 | 1.06 | 2.000 | 35.163 |
>
>    $90^\circ$에서 고유값은 $2$와 $3\,\mathrm{kg}$로, 맨팔의 $1$과 $2$에 비해 공구가 모든 방향, 모든 각도에서 정확히 $1\,\mathrm{kg}$를 더했다. 말단의 점질량은 말단과 함께 움직이기 때문이다. $J$가 정사각이고 가역이면 $\Lambda=J^{-\top}MJ^{-1}$이고, 공구는 $M$에 $m\,J^\top J$를 더하므로 $\Lambda$에는 $m\,I$를 더한다. 무거운 방향은 여전히 $0^\circ$와 $180^\circ$ 쪽으로 폭발한다($10^\circ$에서 $35.2\,\mathrm{kg}$). 특이점은 $J$에 있고, 어떤 페이로드도 $J$를 바꾸지 않기 때문이다. $90^\circ$에서 수직 $10\,\mathrm N$의 접촉은 이제 구속 없는 말단을 $5$가 아니라 $10/3=3.3\,\mathrm{m/s^2}$로 가속한다.

### 출처 · Sources

- *Modern Robotics* (Lynch & Park) 8장(동역학)·11장(제어) — 공식 무료 PDF는 [[04-robotics/modern-robotics-book|책 가이드]]에. §3의 질량 행렬 형태는 여기서 두 점질량의 속도 야코비안으로 유도한 표준 평면 2R 결과이고, 8장은 라그랑주 경로로 같은 결과에 이른다.
- O. Khatib, "A unified approach for motion and force control of robot manipulators: The operational space formulation," *IEEE Journal on Robotics and Automation*, vol. 3, no. 1, pp. 43–53, 1987 — $\Lambda$와 작업공간 제어의 출처. (저널명은 "Journal *on*"이며 "of"가 아니다.)
- 이 페이지의 수치 예제는 명시된 질량과 길이로부터 여기서 직접 계산한 것이며 어느 출처에서 인용한 것이 아니다. 믿지 말고 다시 계산하라.
