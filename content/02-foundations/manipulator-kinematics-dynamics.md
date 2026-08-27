---
title: 10. Manipulator Kinematics & Dynamics
tags: [foundations, robotics, manipulation]
study-depth: Mastery
wiki-support: Working
depth-goal: "Read, write, and manipulate the manipulator equation; convert between joint-space and task-space dynamics; predict how a configuration changes what a controller feels."
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

> [!note] Before you start · 시작 전 점검
> You need forward kinematics and the Jacobian — [[04-robotics/modern-robotics/ch04-forward-kinematics|MR ch.4]] and [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5]], especially $\tau = J^\top\mathcal{F}$ — plus matrix inverses and positive definiteness ([[02-foundations/linear-algebra|1. Linear Algebra §3]]) and partial derivatives ([[02-foundations/calculus-backprop|2. Calculus §1]]).
> 순기구학과 야코비안이 필요하다 — [[04-robotics/modern-robotics/ch04-forward-kinematics|MR 4장]]과 [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장]], 특히 $\tau = J^\top\mathcal{F}$ — 그리고 역행렬과 양정치성([[02-foundations/linear-algebra|1. 선형대수 §3]]), 편미분([[02-foundations/calculus-backprop|2. 미적분 §1]]).

## English

*[[02-foundations/ml-practice|9. ML Practice]] completed the reading tools. This page adds the physics contact needs, and it is the last
page of the track: from here the thread continues in [[04-robotics/force-compliance-control|13. Force & Compliance Control]].*

This page does **not** re-teach forward kinematics, inverse kinematics, or the Jacobian —
the *Modern Robotics* chapter summaries do that, and they do it with worked 2R examples.
It exists because those chapters stop at the place the manipulation track most needs to
continue: **dynamics**, and the equation that carries joint-space dynamics into the task
space where contact actually happens.

The whole page is really one question: *when a controller commands a motion or a force at
the end-effector, what does the arm's own mass do to that command?*

### 1. What kinematics already gave us

Three results are used constantly below, so they are worth stating in one place:

| Result | Statement | Source |
|---|---|---|
| Forward kinematics | joint angles $\theta \mapsto$ end-effector pose $T(\theta)$ | [[04-robotics/modern-robotics/ch04-forward-kinematics\|MR ch.4]] |
| Velocity kinematics | $v = J(\theta)\,\dot\theta$ — joint rates map to tip velocity | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR ch.5 §1]] |
| Statics duality | $\tau = J^\top(\theta)\,\mathcal{F}$ — the same matrix maps wrenches back to torques | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR ch.5 §3]] |

Everything on this page is what happens when you add **mass** to that picture.

### 2. The manipulator equation

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau$$

Four terms, each with a distinct physical job:

- **$M(\theta)$ — the mass (inertia) matrix.** Symmetric and positive definite, so it is
  always invertible — which is why $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$ is always
  well defined. The essential fact is the argument: $M$ **depends on the configuration**.
  An arm is not a constant mass; it is a mass whose value changes as it moves.
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

### 3. Worked example — the 2R arm's mass matrix

Take the planar 2R arm from MR ch.4–5, with point masses at the end of each link:
$m_1 = m_2 = 1$ kg, $L_1 = L_2 = 1$ m. Writing the kinetic energy as
$T = \tfrac12\dot\theta^\top M(\theta)\dot\theta$ and collecting terms gives

$$M(\theta) = \begin{pmatrix} (m_1{+}m_2)L_1^2 + m_2L_2^2 + 2m_2L_1L_2\cos\theta_2 & m_2(L_2^2 + L_1L_2\cos\theta_2) \\ m_2(L_2^2 + L_1L_2\cos\theta_2) & m_2L_2^2 \end{pmatrix}$$

With the numbers above, $M$ depends on $\theta_2$ alone:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

Evaluate at three configurations:

| $\theta_2$ | shape | $M_{11}$ | $M$ |
|---:|---|---:|---|
| $0°$ | straight out | $5$ | $\begin{pmatrix}5&2\\2&1\end{pmatrix}$ |
| $90°$ | elbow square | $3$ | $\begin{pmatrix}3&1\\1&1\end{pmatrix}$ |
| $180°$ | folded back | $1$ | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ |

<svg viewBox="0 0 560 206" style="max-width:100%;height:auto" role="img" aria-label="the same two-link arm at three elbow angles, with joint-one inertia falling from five to three to one">
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">
    <line x1="60" y1="120" x2="100" y2="120"/><line x1="100" y1="120" x2="140" y2="120"/>
    <line x1="240" y1="120" x2="280" y2="120"/><line x1="280" y1="120" x2="280" y2="80"/>
    <line x1="420" y1="120" x2="460" y2="120"/><line x1="460" y1="134" x2="420" y2="134"/>
    <path d="M 466 120 A 8 8 0 0 1 466 134" stroke-width="1.1" opacity="0.6"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="120" r="4.5"/><circle cx="100" cy="120" r="4"/><circle cx="140" cy="120" r="5" fill-opacity="0.55"/>
    <circle cx="240" cy="120" r="4.5"/><circle cx="280" cy="120" r="4"/><circle cx="280" cy="80" r="5" fill-opacity="0.55"/>
    <circle cx="420" cy="120" r="4.5"/><circle cx="460" cy="120" r="4"/><circle cx="420" cy="134" r="5" fill-opacity="0.55"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="50">&#952;&#8322; = 0&#176; &#183; straight</text>
    <text x="280" y="50">&#952;&#8322; = 90&#176;</text>
    <text x="460" y="50">&#952;&#8322; = 180&#176; &#183; folded</text>
    <text x="100" y="160" font-size="12">M&#8321;&#8321; = 5</text>
    <text x="280" y="160" font-size="12">M&#8321;&#8321; = 3</text>
    <text x="460" y="160" font-size="12">M&#8321;&#8321; = 1</text>
    <text x="460" y="176" font-size="9.5" opacity="0.7">drawn offset; the links overlap</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="196">Same arm, same 2 kg of metal. Joint 1 is five times harder to accelerate straight out than folded.</text>
  </g>
</svg>

The number to carry away is that **ratio of five**. The inertia a joint controller fights
is not a property of the robot; it is a property of the robot's current pose. A gain that
is well tuned with the arm folded is badly detuned with the arm extended — which is the
first reason independent-joint PID is a compromise rather than a solution.

### 4. Coriolis and centrifugal terms — why fast motion couples the joints

For this arm, writing $h = -m_2L_1L_2\sin\theta_2$, the velocity-quadratic term is

$$C(\theta,\dot\theta)\,\dot\theta = \begin{pmatrix} h\,\dot\theta_2^2 + 2h\,\dot\theta_1\dot\theta_2 \\ -h\,\dot\theta_1^2 \end{pmatrix}$$

Put in numbers. At $\theta_2 = 90°$, $h = -1\cdot1\cdot1\cdot\sin 90° = -1$. Suppose joint 1
is commanded to **hold still** ($\dot\theta_1 = 0$) while joint 2 swings at
$\dot\theta_2 = 2$ rad/s. The first row gives

$$h\,\dot\theta_2^2 = (-1)(2)^2 = -4 \ \text{N}\cdot\text{m}$$

Joint 1 must supply $-4$ N·m *just to stay where it is*. Nothing is touching the robot;
this is the arm's own moving mass pushing back through the linkage. Double the speed and
it quadruples to $-16$ N·m, because the term is quadratic in velocity.

This is the second reason independent-joint control degrades with speed, and it is why
papers that report good tracking at low speed are making a weaker claim than they appear
to: at low speed the hardest terms in the equation are nearly zero.

### 5. Gravity, inverse dynamics, and computed torque

Gravity comes from differentiating the potential energy. For the same arm
($g = 9.81$ m/s²):

$$g_1(\theta) = (m_1{+}m_2)\,g\,L_1\cos\theta_1 + m_2\,g\,L_2\cos\theta_{12}, \qquad g_2(\theta) = m_2\,g\,L_2\cos\theta_{12}$$

with $\theta_{12} = \theta_1 + \theta_2$. At $\theta = (0°, 90°)$ the forearm points
straight up, so $\cos\theta_{12} = 0$ and

$$g_1 = 2(9.81)(1) + 0 = 19.62\ \text{N}\cdot\text{m}, \qquad g_2 = 0$$

Check it physically: both masses sit one metre horizontally from joint 1, so the shoulder
carries $2 \times 9.81 \times 1$; the forearm mass is directly above joint 2, zero lever
arm, so the elbow carries nothing. The equation and the free-body diagram agree — always
do this check, because a sign error in $g(\theta)$ is the single most common dynamics bug.

Reading the manipulator equation **right to left** — given a desired motion, what torque
does it require? — is **inverse dynamics**, and it is the basis of model-based control:

$$\tau = M(\theta)\,\ddot\theta_{\text{des}} + C(\theta,\dot\theta)\,\dot\theta + g(\theta)$$

Add feedback on the error and you have **computed-torque control**: the model cancels the
arm's own nonlinearity, and a simple linear controller handles what the model got wrong.
That is the honest description of the method — its performance is exactly as good as the
parameters in §7, which is why it is rarely used raw on real hardware.

### 6. Operational-space dynamics — the bridge to force control

Everything so far lives in joint space. Contact does not: contact happens at the
end-effector, in task space. The transformation is the single most important equation on
this page.

Starting from $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$ and differentiating
$v = J\dot\theta$, the end-effector obeys its own second law with an effective mass

$$\Lambda(\theta) = \left(J(\theta)\,M^{-1}(\theta)\,J^\top(\theta)\right)^{-1}$$

$\Lambda$ is the **operational-space inertia matrix** — the mass the end-effector *appears*
to have, seen from outside, in each task-space direction. A task-space force command then
becomes joint torques by $\tau = J^\top \mathcal{F}$, which is why the statics duality from
MR ch.5 turns out to be the load-bearing result of the whole manipulation track.

**Worked out for the 2R arm** at $\theta = (0°, 90°)$. From MR ch.5, the tip Jacobian there
is $J = \begin{pmatrix}-1 & -1\\ 1 & 0\end{pmatrix}$, and from §3,
$M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$ with $\det M = 2$, so

$$M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}, \qquad JM^{-1} = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}$$

$$JM^{-1}J^\top = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}\begin{pmatrix}-1&1\\-1&0\end{pmatrix} = \begin{pmatrix}1&0\\0&0.5\end{pmatrix} \quad\Longrightarrow\quad \Lambda = \begin{pmatrix}1&0\\0&2\end{pmatrix}$$

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="the arm at elbow ninety degrees with an apparent-mass ellipse at the tip, one kilogram sideways and two kilograms vertically">
  <ellipse cx="130" cy="92" rx="26" ry="52" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">
    <line x1="52" y1="172" x2="130" y2="172"/><line x1="130" y1="172" x2="130" y2="92"/>
  </g>
  <g fill="currentColor"><circle cx="52" cy="172" r="4.5"/><circle cx="130" cy="172" r="4"/><circle cx="130" cy="92" r="4.5"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.85" marker-end="url(#arM)">
    <line x1="158" y1="92" x2="192" y2="92"/><line x1="130" y1="38" x2="130" y2="16"/>
  </g>
  <defs><marker id="arM" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor">
    <text x="198" y="96">push sideways: feels like 1 kg</text>
    <text x="140" y="28">push up: feels like 2 kg</text>
    <text x="198" y="126">&#923; = (J M&#8315;&#185; J&#7488;)&#8315;&#185; = diag(1, 2)</text>
    <text x="198" y="144" opacity="0.85">actual mass on the arm: 2 kg total</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="190">The long axis of an apparent-mass ellipse is the HARD direction &#8212; the opposite reading from the</text>
    <text x="20" y="206">manipulability ellipse of MR ch.5, whose long axis is the easy one. They are reciprocal views.</text>
  </g>
</svg>

Read the result. The arm carries 2 kg of actual mass, but pushed sideways at the tip it
behaves like **1 kg**, and pushed vertically like **2 kg** — a factor of two, in the same
configuration, from geometry alone. Two consequences that the force-control literature
assumes you have absorbed:

- **Impact force is direction-dependent.** Striking a rigid surface at the same speed
  transfers twice the momentum in the heavy direction. A gripper that inserts safely
  along one axis can damage the part along another.
- **A single stiffness gain is never uniformly right.** The closed-loop behaviour of an
  impedance controller depends on $\Lambda$, so identical gains give different effective
  dynamics in different directions and different poses.

The relationship to MR ch.5's manipulability ellipsoid is qualitative, not exact — $\Lambda^{-1} = JM^{-1}J^\top$ is the reciprocal of the *dynamic* manipulability ellipsoid, which coincides with ch.5's kinematic $JJ^\top$ only when $M \propto I$. The direction of the statement still holds: that
ellipsoid's long axis is the direction that is *easy to move*, and an apparent-mass
ellipse's long axis is the direction that is *hard to move*. Near a singularity the
manipulability ellipse collapses to a line, and correspondingly $\Lambda$ blows up in that
direction — the arm becomes effectively infinitely heavy along the direction it can no
longer move.

### 7. Where the parameters come from — and the sim-to-real gap

Every symbol in §2 hides a number that someone had to measure: link masses, centres of
mass, inertia tensors, joint friction, motor constants, gear elasticity. Three honest
observations:

1. **CAD values are wrong at the margins.** Cabling, covers, and the actual tool are
   rarely in the CAD model, and they are exactly what sits farthest from the joints, where
   they matter most.
2. **Friction is the worst-modelled term** and it is not in the ideal equation at all. Real
   controllers carry a friction model that is fitted, not derived.
3. **This equation is the sim-to-real gap.** When a policy trained in simulation fails on
   hardware, the mismatch is usually not in the perception; it is in these parameters. That
   is what [[05-construction-robotics/sim-to-real|sim-to-real]] work is largely about, and
   why domain randomization randomizes *these* quantities.

For construction manipulation there is a fourth: the **payload is unknown and large**.
A grasped panel or bolt changes $M(\theta)$ and $g(\theta)$ by an amount comparable to the
arm's own links, and unlike a factory setting you do not get to hard-code its mass.

### 8. Reading dynamics in a paper, and the path to Mastery

When a manipulation paper mentions dynamics, these are the questions that separate a real
claim from decoration:

- Is the controller **torque-level** or does it command positions to a vendor controller?
  Most claims about compliance are meaningless in the second case.
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
- [ ] State why the manipulability and apparent-mass ellipses are reciprocal.
- [ ] Name the term most responsible for sim-to-real failure and say why.

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
> 4. Whether the arm is actually torque-controlled underneath. With a stiff position-controlled inner loop, the force "control" is an outer loop commanding small positions, which is admittance control with the vendor's stiffness in the way — it can work, but its stability depends on the environment being soft, and the claim should be tested against a rigid surface. See [[04-robotics/contact-force-tactile|Contact, Force & Tactile §5]].
> 5. $M(\theta)$ and $g(\theta)$ both change substantially, since the payload adds mass at the far end where the lever arm is longest, and $C$ changes with $M$. The panel more than doubles the moving mass in this example, so a controller tuned unloaded will be badly wrong loaded — the reason payload-aware or adaptive control matters in construction more than in a factory with a known part.

### Sources

- *Modern Robotics* (Lynch & Park) ch.8 (dynamics) and ch.11 (control) — see [[04-robotics/modern-robotics-book|the book guide]] for the free official PDF. The mass-matrix form in §3 is the standard planar 2R result derived there.
- O. Khatib, "A unified approach for motion and force control of robot manipulators: The operational space formulation," *IEEE Journal on Robotics and Automation*, vol. 3, no. 1, pp. 43–53, 1987 — the origin of $\Lambda$ and of task-space control. (The journal is "Journal *on*", not "of".)
- The numeric examples on this page were computed here from the stated masses and lengths, not quoted from a source; recompute them rather than trusting them.

## 한국어

*[[02-foundations/ml-practice|9. ML 실무]]가 읽기 도구를 완성했다. 이 페이지는 접촉이 요구하는 물리를 더하며 트랙의 마지막이다.
여기서부터 그 줄기는 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]로 이어진다.*

이 페이지는 순기구학·역기구학·야코비안을 **다시 가르치지 않는다** — *Modern Robotics* 챕터
요약이 이미 2R 계산 예제와 함께 그 일을 한다. 이 페이지가 존재하는 이유는, 그 챕터들이
매니퓰레이션 트랙에서 가장 이어져야 할 지점에서 멈추기 때문이다: **동역학**, 그리고 관절
공간 동역학을 실제로 접촉이 일어나는 작업 공간으로 옮기는 방정식.

페이지 전체가 사실 하나의 질문이다: *제어기가 말단에서 운동이나 힘을 명령할 때, 팔 자신의
질량은 그 명령에 무슨 짓을 하는가?*

### 1. 기구학이 이미 준 것

아래에서 계속 쓰이는 세 결과를 한자리에 적어 둔다:

| 결과 | 내용 | 출처 |
|---|---|---|
| 순기구학 | 관절각 $\theta \mapsto$ 말단 자세 $T(\theta)$ | [[04-robotics/modern-robotics/ch04-forward-kinematics\|MR 4장]] |
| 속도 기구학 | $v = J(\theta)\,\dot\theta$ — 관절 속도가 끝점 속도로 | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR 5장 §1]] |
| 정역학 쌍대성 | $\tau = J^\top(\theta)\,\mathcal{F}$ — 같은 행렬이 렌치를 토크로 되돌린다 | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR 5장 §3]] |

이 페이지 전체는 그 그림에 **질량**을 더하면 무슨 일이 일어나는가이다.

### 2. 매니퓰레이터 방정식

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau$$

네 항이고, 각각 다른 물리적 역할을 한다:

- **$M(\theta)$ — 질량(관성) 행렬.** 대칭이고 양정치이므로 항상 가역이다 — 그래서
  $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$가 언제나 잘 정의된다. 핵심은 괄호 안의
  인자다: $M$은 **자세에 의존한다**. 팔은 상수 질량이 아니라, 움직이면서 값이 변하는
  질량이다.
- **$C(\theta,\dot\theta)\,\dot\theta$ — 코리올리·원심 항.** 속도의 이차식이다. 마찰이
  *아니다*. 한 관절의 운동이 다른 관절에 토크를 가하게 만드는 결합이며, 정지 상태에서 0이 된다.
- **$g(\theta)$ — 중력.** 자세 의존, 속도 무관. 로봇이 가만히 있을 때도 싸우는 항.
- **$\tau$ — 관절 토크**, 모터가 실제로 명령하는 것.

말단이 무언가에 닿으면 외부 렌치 $\mathcal{F}_{\text{ext}}$가 정역학 쌍대성을 통해 들어온다:

$$M(\theta)\,\ddot\theta + C(\theta,\dot\theta)\,\dot\theta + g(\theta) = \tau + J^\top(\theta)\,\mathcal{F}_{\text{ext}}$$

이 추가 항이 접촉을 계획 문제가 아니라 제어 문제로 만드는 이유 전부다: 환경이 제어기가
명령하지 않은 토크를 주입할 수 있게 된다.

### 3. 계산 예제 — 2R 팔의 질량 행렬

MR 4~5장의 평면 2R 팔에 각 링크 끝의 점질량을 둔다: $m_1 = m_2 = 1$ kg, $L_1 = L_2 = 1$ m.
운동 에너지를 $T = \tfrac12\dot\theta^\top M(\theta)\dot\theta$로 쓰고 항을 모으면

$$M(\theta) = \begin{pmatrix} (m_1{+}m_2)L_1^2 + m_2L_2^2 + 2m_2L_1L_2\cos\theta_2 & m_2(L_2^2 + L_1L_2\cos\theta_2) \\ m_2(L_2^2 + L_1L_2\cos\theta_2) & m_2L_2^2 \end{pmatrix}$$

위 숫자를 넣으면 $M$은 $\theta_2$에만 의존한다:

$$M(\theta_2) = \begin{pmatrix} 3 + 2\cos\theta_2 & 1 + \cos\theta_2 \\ 1 + \cos\theta_2 & 1\end{pmatrix}$$

세 자세에서 계산하면:

| $\theta_2$ | 모양 | $M_{11}$ | $M$ |
|---:|---|---:|---|
| $0°$ | 곧게 뻗음 | $5$ | $\begin{pmatrix}5&2\\2&1\end{pmatrix}$ |
| $90°$ | 팔꿈치 직각 | $3$ | $\begin{pmatrix}3&1\\1&1\end{pmatrix}$ |
| $180°$ | 접힘 | $1$ | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ |

<svg viewBox="0 0 560 206" style="max-width:100%;height:auto" role="img" aria-label="같은 2링크 팔의 세 팔꿈치 각도, 1번 관절 관성이 5에서 3, 1로 줄어든다">
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">
    <line x1="60" y1="120" x2="100" y2="120"/><line x1="100" y1="120" x2="140" y2="120"/>
    <line x1="240" y1="120" x2="280" y2="120"/><line x1="280" y1="120" x2="280" y2="80"/>
    <line x1="420" y1="120" x2="460" y2="120"/><line x1="460" y1="134" x2="420" y2="134"/>
    <path d="M 466 120 A 8 8 0 0 1 466 134" stroke-width="1.1" opacity="0.6"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="120" r="4.5"/><circle cx="100" cy="120" r="4"/><circle cx="140" cy="120" r="5" fill-opacity="0.55"/>
    <circle cx="240" cy="120" r="4.5"/><circle cx="280" cy="120" r="4"/><circle cx="280" cy="80" r="5" fill-opacity="0.55"/>
    <circle cx="420" cy="120" r="4.5"/><circle cx="460" cy="120" r="4"/><circle cx="420" cy="134" r="5" fill-opacity="0.55"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="50">&#952;&#8322; = 0&#176; &#183; 곧게 뻗음</text>
    <text x="280" y="50">&#952;&#8322; = 90&#176;</text>
    <text x="460" y="50">&#952;&#8322; = 180&#176; &#183; 접힘</text>
    <text x="100" y="160" font-size="12">M&#8321;&#8321; = 5</text>
    <text x="280" y="160" font-size="12">M&#8321;&#8321; = 3</text>
    <text x="460" y="160" font-size="12">M&#8321;&#8321; = 1</text>
    <text x="460" y="176" font-size="9.5" opacity="0.7">겹쳐서 보이도록 어긋나게 그렸다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="196">같은 팔, 같은 2 kg. 곧게 뻗었을 때 1번 관절을 가속하기가 접었을 때보다 다섯 배 어렵다.</text>
  </g>
</svg>

가져갈 숫자는 그 **5배**다. 관절 제어기가 싸우는 관성은 로봇의 속성이 아니라 로봇의 현재
자세의 속성이다. 팔을 접은 상태에서 잘 튜닝된 게인은 팔을 뻗은 상태에서 잘못 튜닝된
게인이다 — 독립 관절 PID가 해답이 아니라 타협인 첫 번째 이유다.

### 4. 코리올리·원심 항 — 빠른 운동이 관절을 결합시키는 이유

이 팔에서 $h = -m_2L_1L_2\sin\theta_2$로 두면 속도 이차 항은

$$C(\theta,\dot\theta)\,\dot\theta = \begin{pmatrix} h\,\dot\theta_2^2 + 2h\,\dot\theta_1\dot\theta_2 \\ -h\,\dot\theta_1^2 \end{pmatrix}$$

숫자를 넣자. $\theta_2 = 90°$에서 $h = -1\cdot1\cdot1\cdot\sin 90° = -1$이다. 1번 관절은
**가만히 있으라**($\dot\theta_1 = 0$)고 명령받았고, 2번 관절이 $\dot\theta_2 = 2$ rad/s로
휘두른다고 하자. 첫 행은

$$h\,\dot\theta_2^2 = (-1)(2)^2 = -4 \ \text{N}\cdot\text{m}$$

1번 관절은 *제자리에 있기 위해서만* $-4$ N·m를 내야 한다. 로봇에 닿은 것은 아무것도 없다.
이것은 팔 자신의 움직이는 질량이 링크를 통해 되미는 힘이다. 속도를 두 배로 하면 항이 속도의
이차식이므로 $-16$ N·m로 네 배가 된다.

독립 관절 제어가 속도에 따라 나빠지는 두 번째 이유이고, 저속에서 좋은 추종 성능을 보고하는
논문이 보이는 것보다 약한 주장을 하고 있는 이유이기도 하다: 저속에서는 방정식의 어려운 항들이
거의 0이다.

### 5. 중력, 역동역학, 계산 토크

중력은 위치 에너지를 미분해서 나온다. 같은 팔에 대해 ($g = 9.81$ m/s²):

$$g_1(\theta) = (m_1{+}m_2)\,g\,L_1\cos\theta_1 + m_2\,g\,L_2\cos\theta_{12}, \qquad g_2(\theta) = m_2\,g\,L_2\cos\theta_{12}$$

($\theta_{12} = \theta_1 + \theta_2$). $\theta = (0°, 90°)$에서는 아래팔이 똑바로 위를
향하므로 $\cos\theta_{12} = 0$이고

$$g_1 = 2(9.81)(1) + 0 = 19.62\ \text{N}\cdot\text{m}, \qquad g_2 = 0$$

물리로 검산하라: 두 질량 모두 1번 관절에서 수평으로 1 m 떨어져 있으므로 어깨는
$2 \times 9.81 \times 1$을 진다. 아래팔 질량은 2번 관절 바로 위에 있어 지렛대 팔이 0이므로
팔꿈치는 아무것도 지지 않는다. 방정식과 자유물체도가 일치한다 — 이 검산은 반드시 하라.
$g(\theta)$의 부호 오류가 동역학에서 가장 흔한 버그다.

매니퓰레이터 방정식을 **오른쪽에서 왼쪽으로** 읽는 것 — 원하는 운동이 주어졌을 때 어떤 토크가
필요한가? — 이 **역동역학**이며, 모델 기반 제어의 토대다:

$$\tau = M(\theta)\,\ddot\theta_{\text{des}} + C(\theta,\dot\theta)\,\dot\theta + g(\theta)$$

여기에 오차 피드백을 더하면 **계산 토크 제어**가 된다: 모델이 팔 자신의 비선형성을 상쇄하고,
모델이 틀린 부분은 단순한 선형 제어기가 맡는다. 이것이 이 방법의 정직한 설명이다 — 성능은
§7의 파라미터가 정확한 만큼만 좋으며, 그래서 실기계에서 날것 그대로 쓰이는 일은 드물다.

### 6. 작업공간(operational space) 동역학 — 힘 제어로 가는 다리

여기까지는 전부 관절 공간이다. 접촉은 그렇지 않다: 접촉은 말단에서, 작업 공간에서 일어난다.
그 변환이 이 페이지에서 가장 중요한 방정식이다.

여기서 말하는 **작업 공간**은 Khatib의 *operational space* — 말단의 위치·자세를 좌표로
삼는 공간 — 이지, 팔이 닿을 수 있는 부피를 뜻하는 *workspace*가 아니다. 이 위키는 후자를
**작업 영역**이라 부른다.

$\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$에서 출발해 $v = J\dot\theta$를 미분하면,
말단은 자기 자신의 운동 제2법칙을 따르고 그 유효 질량은

$$\Lambda(\theta) = \left(J(\theta)\,M^{-1}(\theta)\,J^\top(\theta)\right)^{-1}$$

$\Lambda$는 **작업 공간 관성 행렬**이다 — 밖에서 볼 때 말단이 각 작업 공간 방향에서 *가진
것처럼 보이는* 질량. 그다음 작업 공간의 힘 명령은 $\tau = J^\top \mathcal{F}$로 관절 토크가
된다. MR 5장의 정역학 쌍대성이 결국 매니퓰레이션 트랙 전체를 떠받치는 결과인 이유가 이것이다.

**2R 팔에 대해 $\theta = (0°, 90°)$에서 계산해 보자.** MR 5장에서 그 자세의 끝점 야코비안은
$J = \begin{pmatrix}-1 & -1\\ 1 & 0\end{pmatrix}$이고, §3에서
$M = \begin{pmatrix}3&1\\1&1\end{pmatrix}$, $\det M = 2$이므로

$$M^{-1} = \tfrac12\begin{pmatrix}1&-1\\-1&3\end{pmatrix} = \begin{pmatrix}0.5&-0.5\\-0.5&1.5\end{pmatrix}, \qquad JM^{-1} = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}$$

$$JM^{-1}J^\top = \begin{pmatrix}0&-1\\0.5&-0.5\end{pmatrix}\begin{pmatrix}-1&1\\-1&0\end{pmatrix} = \begin{pmatrix}1&0\\0&0.5\end{pmatrix} \quad\Longrightarrow\quad \Lambda = \begin{pmatrix}1&0\\0&2\end{pmatrix}$$

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="팔꿈치 90도 자세의 팔과 끝점의 겉보기 질량 타원, 옆으로 1 kg 위로 2 kg">
  <ellipse cx="130" cy="92" rx="26" ry="52" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round">
    <line x1="52" y1="172" x2="130" y2="172"/><line x1="130" y1="172" x2="130" y2="92"/>
  </g>
  <g fill="currentColor"><circle cx="52" cy="172" r="4.5"/><circle cx="130" cy="172" r="4"/><circle cx="130" cy="92" r="4.5"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.85" marker-end="url(#arMk)">
    <line x1="158" y1="92" x2="192" y2="92"/><line x1="130" y1="38" x2="130" y2="16"/>
  </g>
  <defs><marker id="arMk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor">
    <text x="198" y="96">옆으로 밀면: 1 kg처럼 느껴진다</text>
    <text x="140" y="28">위로 밀면: 2 kg처럼 느껴진다</text>
    <text x="198" y="126">&#923; = (J M&#8315;&#185; J&#7488;)&#8315;&#185; = diag(1, 2)</text>
    <text x="198" y="144" opacity="0.85">팔에 실린 실제 질량: 합쳐서 2 kg</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="190">겉보기 질량 타원의 긴 축은 &#8216;어려운&#8217; 방향이다 &#8212; 긴 축이 쉬운 방향인 MR 5장의 가조작성</text>
    <text x="20" y="206">타원과 정반대로 읽는다. 둘은 서로 역수인 두 관점이다.</text>
  </g>
</svg>

결과를 읽자. 팔에 실린 실제 질량은 2 kg인데, 끝점을 옆으로 밀면 **1 kg**처럼, 위로 밀면
**2 kg**처럼 거동한다 — 같은 자세에서, 순전히 기하 때문에 두 배 차이가 난다. 힘 제어 문헌이
독자가 이미 소화했다고 가정하는 두 귀결:

- **충격력은 방향에 의존한다.** 같은 속도로 단단한 면을 치면 무거운 방향에서 두 배의 운동량이
  전달된다. 한 축으로는 안전하게 삽입하는 그리퍼가 다른 축으로는 부재를 손상시킬 수 있다.
- **하나의 강성 게인이 모든 방향에서 옳을 수 없다.** 임피던스 제어기의 폐루프 거동은
  $\Lambda$에 의존하므로, 같은 게인이 방향과 자세에 따라 다른 유효 동역학을 준다.

MR 5장의 가조작성 타원체와의 관계는 정확한 일치가 아니라 정성적이다 — $\Lambda^{-1} = JM^{-1}J^\top$은 *동역학* 가조작성 타원체의 역이고, 5장의 기구학적 $JJ^\top$과는 $M \propto I$일 때만 일치한다. 진술의 방향은 그대로다: 그 타원체의 긴 축은
*움직이기 쉬운* 방향이고, 겉보기 질량 타원의 긴 축은 *움직이기 어려운* 방향이다. 특이점
근처에서 가조작성 타원은 직선으로 붕괴하고, 대응해서 $\Lambda$는 그 방향으로 발산한다 —
팔이 더 이상 움직일 수 없는 방향으로 사실상 무한히 무거워진다.

### 7. 파라미터는 어디서 오는가 — 그리고 sim-to-real 격차

§2의 모든 기호 뒤에는 누군가 측정해야 했던 숫자가 있다: 링크 질량, 질량 중심, 관성 텐서,
관절 마찰, 모터 상수, 감속기 탄성. 정직한 관찰 셋:

1. **CAD 값은 가장자리에서 틀린다.** 케이블, 커버, 실제 공구는 CAD 모델에 거의 없고, 하필
   그것들이 관절에서 가장 먼 곳 — 가장 크게 작용하는 곳 — 에 있다.
2. **마찰이 가장 나쁘게 모델링된 항**이며 이상적인 방정식에는 아예 없다. 실제 제어기는
   유도된 것이 아니라 피팅된 마찰 모델을 들고 다닌다.
3. **이 방정식이 곧 sim-to-real 격차다.** 시뮬레이션에서 학습한 정책이 실기계에서 실패할 때,
   불일치는 대개 인식이 아니라 이 파라미터들에 있다. [[05-construction-robotics/sim-to-real|sim-to-real]]
   연구가 대체로 다루는 것이 이것이고, 도메인 랜덤화가 *이* 양들을 무작위화하는 이유다.

건설 조작에는 네 번째가 있다: **페이로드가 알려져 있지 않고 크다.** 잡은 패널이나 볼트는
$M(\theta)$와 $g(\theta)$를 팔 자신의 링크에 견줄 만큼 바꾸며, 공장과 달리 그 질량을
하드코딩할 수 없다.

### 8. 논문에서 동역학 읽기, 그리고 Mastery로 가는 길

매니퓰레이션 논문이 동역학을 언급할 때, 실제 주장과 장식을 가르는 질문들:

- 제어기가 **토크 수준**인가, 아니면 벤더 제어기에 위치를 명령하는가? 후자라면 컴플라이언스에
  관한 주장 대부분은 의미가 없다.
- $M$, $C$, $g$가 **모델링되었나, 학습되었나, 무시되었나**? "중력 보상"만으로는 완전한
  역동역학보다 훨씬 약한 진술이다.
- 결과를 어떤 **속도**에서 얻었나? §4에 따르면 어려운 항들은 속도의 이차식이므로, 느린
  시연은 모델 오차를 숨긴다.
- **페이로드**가 모델에 있는가?

여기서 Mastery에 도달하려면 이 페이지가 줄 수 없는 세 가지가 필요하다:

| 필요한 것 | 어디서 |
|---|---|
| 완전한 유도(라그랑주·뉴턴–오일러, 재귀 알고리즘) | *Modern Robotics* 8장, [[04-robotics/modern-robotics-book\|책 가이드]] |
| 작업 공간 제어 이론 | Khatib의 operational-space 정식화, 그다음 [[04-robotics/control-theory-ce397\|제어 이론]] |
| 파라미터 감각 | 강체 동역학 시뮬레이터 아무거나 — 링크 질량을 20% 바꾸고 튜닝된 제어기가 무너지는 것을 볼 것 |

이 페이지의 Mastery 시험: 팔과 자세와 방향이 주어졌을 때 접촉이 뻣뻣하게 느껴질지 무르게
느껴질지 예측하고, 맞히는 것.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 매니퓰레이터 방정식을 외워서 쓰고 각 항이 하는 일을 말한다.
- [ ] $M$에 왜 인자가 붙는지 5배 예제로 설명한다.
- [ ] $J$와 $M$에서 $\Lambda$를 계산하고 물리적으로 해석한다.
- [ ] 가조작성 타원과 겉보기 질량 타원이 왜 서로 역수인지 말한다.
- [ ] sim-to-real 실패에 가장 크게 책임 있는 항을 대고 이유를 말한다.

### 스스로 점검

1. $M(\theta)$는 양정치다. 이것이 시뮬레이션에 왜 중요한가?
2. 팔이 $\theta_2 = 0°$(곧게 뻗음)에 있다. $M$과 $h$를 계산하고, 거기서 코리올리 항이
   무엇을 하는지 말하라.
3. $\theta=(0°,90°)$에서 겉보기 질량이 옆으로 1 kg, 위로 2 kg인데 팔의 무게는 2 kg이다.
   겉보기 질량이 실제 질량보다 *작을* 수 있는가?
4. 어떤 논문이 위치 제어 산업용 팔과 손목 힘 센서로 우수한 힘 추종을 보고한다. 무엇을
   확인해야 하는가?
5. 로봇이 3 kg 패널을 잡았다. 매니퓰레이터 방정식의 어느 항이 바뀌는가?

> [!tip]- 정답 · Answers
> 1. 양정치면 가역이므로 $\ddot\theta = M^{-1}(\tau - C\dot\theta - g)$가 언제나 유일한 해를 갖는다 — 시뮬레이터가 항상 한 스텝 적분할 수 있다. 또한 0이 아닌 임의의 운동에 대해 운동 에너지 $\tfrac12\dot\theta^\top M\dot\theta$가 순수하게 양수라는 뜻이고, 에너지 기반 안정성 논증이 성립하는 근거가 그것이다.
> 2. $\cos 0° = 1$이므로 $M = \begin{pmatrix}5&2\\2&1\end{pmatrix}$. 그리고 $h = -\sin 0° = 0$이므로 이 자세에서는 속도와 무관하게 코리올리·원심 항 전체가 사라진다. 일반적 사실이 아니라 진짜 특수한 경우다 — 팔꿈치를 $0°$나 $180°$에서 벗어나게 하면 결합이 돌아온다.
> 3. 끝점이 그 질량 전부에 강체로 붙어 있지 않기 때문이다 — 옆으로 밀면 팔이 회전해서 응답할 수 있으므로 관성의 일부만 저항한다. 겉보기 질량은 금속의 양이 아니라 *한 방향에서 끝점이 보이는 저항*을 잰다. 특이 극한에서는 반대 현상이 일어나 잃어버린 방향으로 $\Lambda$가 무한히 커진다.
> 4. 팔이 실제로 그 아래에서 토크 제어되는지 확인해야 한다. 뻣뻣한 위치 제어 내부 루프가 있다면 그 힘 "제어"는 작은 위치를 명령하는 외부 루프이고, 이는 벤더의 강성이 사이에 낀 어드미턴스 제어다 — 동작할 수는 있지만 안정성이 환경이 무르다는 데 의존하므로, 주장은 단단한 면에 대해 검증되어야 한다. [[04-robotics/contact-force-tactile|접촉·힘·촉각 §5]]를 보라.
> 5. $M(\theta)$와 $g(\theta)$가 모두 크게 바뀐다. 페이로드가 지렛대 팔이 가장 긴 맨 끝에 질량을 더하기 때문이고, $C$도 $M$을 따라 바뀐다. 이 예에서 패널은 움직이는 질량을 두 배 이상으로 만들므로, 무부하로 튜닝한 제어기는 부하 상태에서 크게 틀린다 — 부품 질량이 알려진 공장보다 건설에서 페이로드 인지 제어나 적응 제어가 더 중요한 이유다.

### 출처

- *Modern Robotics* (Lynch & Park) 8장(동역학)·11장(제어) — 공식 무료 PDF는 [[04-robotics/modern-robotics-book|책 가이드]]에. §3의 질량 행렬 형태는 거기서 유도되는 표준 평면 2R 결과다.
- O. Khatib, "A unified approach for motion and force control of robot manipulators: The operational space formulation," *IEEE Journal on Robotics and Automation*, vol. 3, no. 1, pp. 43–53, 1987 — $\Lambda$와 작업 공간 제어의 출처. (저널명은 "Journal *on*"이며 "of"가 아니다.)
- 이 페이지의 수치 예제는 명시된 질량과 길이로부터 여기서 직접 계산한 것이며 어느 출처에서 인용한 것이 아니다. 믿지 말고 다시 계산하라.
