---
title: "MR Ch.09 — Trajectory Generation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P2, time one named joint move with a trapezoidal and a cubic scaling, say which actuator limit binds each, and predict how the answer moves when the drive changes."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.9** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> Differentiating polynomials ([[02-foundations/engineering-math|0.5 §1]]) and the idea of separating path from timing are all you need — the lightest chapter in the track. Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (*plant*: control's word for the system being controlled; P2 is the catalog's planar two-link arm) carries the worked move, whose two end poses are the contact configurations of [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]] and the two IK branches of [[04-robotics/modern-robotics/ch06-inverse-kinematics|ch.6]]; §2's remark on torque uses the equation of motion of [[04-robotics/modern-robotics/ch08-dynamics|ch.8]].
> 다항식 미분([[02-foundations/engineering-math|0.5 §1]])과 경로/시간의 분리라는 아이디어만 있으면 된다 — 이 장은 트랙에서 가장 가벼운 장이다. 계산은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**(장치(plant)는 제어 공학에서 제어 대상 시스템을 부르는 말이고, P2는 카탈로그의 평면 2링크 팔이다)로 하고, 그 이동의 두 끝 자세는 [[04-robotics/modern-robotics/ch02-configuration-space|2장]]의 접촉 컨피규레이션이자 [[04-robotics/modern-robotics/ch06-inverse-kinematics|6장]]의 IK 가지 둘이다. §2의 토크 이야기는 [[04-robotics/modern-robotics/ch08-dynamics|8장]]의 운동 방정식을 쓴다.

## English

**Core question**: how do we turn "go from A to B" into a smooth, executable function of time?

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this chapter is the motion-and-task-planning layer's hand-off to manipulation, and in *"install that panel on the frame"* it serves *move the component*: a path becomes a command the motors can follow only once it is timed (its chip sits in the planning band of the [[physical-ai-map|Physical AI Map]]). Timed carelessly, a move is illegal or slow — squeezed into the trapezoid's $4.327\,\mathrm{s}$, a cubic asks the elbow of **P2**, the catalog's planar two-link arm ([[02-foundations/lab-plants|0.6]]), for $1.089\,\mathrm{rad/s}$ against its $0.8\,\mathrm{rad/s}$ limit, and the fastest legal cubic takes $5.890\,\mathrm{s}$, $36\,\%$ longer (Worked case, parts B–C). Later pages build on it — [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]] supplies the paths and shows that this page's straight one goes $0.414\,\mathrm{m}$ into the panel, [[04-robotics/actuators-drives|10.5 Actuators & Drives §3]] says where $v_{\max}$ and $a_{\max}$ come from, [[04-robotics/capstone-panel-contact|26. Capstone §3]] caps the same trapezoid by tip speed, and [[04-robotics/ros2/manipulation-moveit2|25.8 MoveIt 2 §1]] times its plans the same way — in block 2 of the dissertation path ([[07-research-program/index|7. Research Program §8]], robotics sessions 22–24). After it you can time any joint move with a trapezoid or a polynomial, say which limit binds before computing, and predict what a change of drive does to the time.

> [!note] First pass · 처음이라면
> About three 60–90-minute sessions, robotics 22–24. **Session 1:** the Running object with its warning, the picture and the whole Worked case — the trapezoid (A) and the cubic (B) on the elbow flip, their comparison (C), and the crossover $\Delta\theta^\dagger$ that says in advance which limit binds (D), with its figure. End with self-check 4 by hand: a $0.5\,\mathrm{rad}$ move, the one regime where the cubic is acceleration-bound. **Session 2:** §1–§3 — the chapter's list with its worked example, path, trajectory and time scaling defined together, and the trapezoid. **Session 3:** the self-check and the problem set. The collapsed *Deeper* note on the general time-optimal problem is second pass.

### Running object · 이 페이지의 대상

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], the catalog's planar two-link arm, and one named move on it: the **elbow flip** between the two configurations that put the tip on the panel target $(1,1)$, derived in [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]] — ch.6's two IK branches.

$$\theta^{\text{start}} = (0°,\ 90°) \ \longrightarrow\ \theta^{\text{goal}} = (90°,\ -90°), \qquad \Delta\theta_1 = +\tfrac{\pi}{2} = 1.5708\ \mathrm{rad}, \quad \Delta\theta_2 = -\pi = -3.1416\ \mathrm{rad}$$

so the elbow travels exactly twice as far as the shoulder, because it swings from $+90°$ to $-90°$ while the shoulder turns a quarter turn; the whole page depends on that fact. The **path** is the straight line between those two points of joint space, $\theta(s) = \theta^{\text{start}} + s\,\Delta\theta$ with $s \in [0,1]$; this page only chooses $s(t)$.

**Actuator limits, frozen here.** 0.6 freezes P2's drive on [[04-robotics/actuators-drives|10.5 Actuators & Drives]], whose joint turns at up to $2.4\,\mathrm{rad/s}$ unloaded; the two numbers below are a planning specification that stays well inside what that drive can do, and this page never changes them, so every joint of P2 obeys

$$|\dot\theta_i| \le v_{\max} = 0.8\ \mathrm{rad/s}, \qquad |\ddot\theta_i| \le a_{\max} = 2\ \mathrm{rad/s^2}$$

which are the same two numbers §1's worked example uses, now attached to the plant.

> [!warning] A time scaling is not a collision check · 시간 스케일링은 충돌 검사가 아니다
> This straight joint-space path is *not* collision-free against ch.2's panel, the half-plane $x \ge 1$. Both ends only touch the face $x = 1$, which this wiki counts as free, but at the midpoint $(45°,\ 0°)$ the arm is straight and the tip sits at $(1.414,\ 1.414)$, $\sqrt2 - 1 = 0.414\,\mathrm{m}$ past the face. [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]] finds this with its edge test and plans around it. Timing a path and clearing a path are different questions, and this chapter answers only the first.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 363" style="max-width:100%;height:auto" role="img" aria-label="the elbow flip on P2 in three stacked panels over 0 to 6 s: elbow angle, elbow speed against the 0.8 rad/s limit, and the rate of change of speed against the 2 rad/s² limit, for the trapezoid (4.327 s) and the cubic (5.890 s)">
  <g transform="translate(0 3)">
    <g stroke="currentColor" stroke-width="1" opacity="0.55"><line x1="80" y1="26" x2="80" y2="102"/><line x1="80" y1="98" x2="534" y2="98"/><line x1="80" y1="128.4" x2="80" y2="204"/><line x1="80" y1="204" x2="534" y2="204"/><line x1="80" y1="247.7" x2="80" y2="316.3"/><line x1="80" y1="282" x2="534" y2="282"/><line x1="80" y1="316.3" x2="534" y2="316.3"/></g>
    <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="76" y1="30" x2="80" y2="30"/><line x1="76" y1="64" x2="80" y2="64"/><line x1="76" y1="98" x2="80" y2="98"/><line x1="76" y1="175.2" x2="80" y2="175.2"/><line x1="76" y1="146.4" x2="80" y2="146.4"/><line x1="76" y1="254" x2="80" y2="254"/><line x1="76" y1="310" x2="80" y2="310"/><line x1="80" y1="316.3" x2="80" y2="320.3"/><line x1="155.7" y1="316.3" x2="155.7" y2="320.3"/><line x1="231.3" y1="316.3" x2="231.3" y2="320.3"/><line x1="307" y1="316.3" x2="307" y2="320.3"/><line x1="382.7" y1="316.3" x2="382.7" y2="320.3"/><line x1="458.3" y1="316.3" x2="458.3" y2="320.3"/><line x1="534" y1="316.3" x2="534" y2="320.3"/></g>
    <line x1="80" y1="64" x2="534" y2="64" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
    <g stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 3" opacity="0.5"><line x1="407.4" y1="30" x2="407.4" y2="316.3"/><line x1="525.7" y1="30" x2="525.7" y2="316.3"/></g>
    <path d="M80 30 L82.9 30 L85.7 30 L88.6 30.1 L91.4 30.1 L94.3 30.2 L97.1 30.3 L100 30.4 L102.8 30.5 L105.7 30.7 L108.6 30.8 L111.4 31 L114.3 31.1 L117.1 31.3 L120 31.5 L122.8 31.8 L125.7 32 L128.5 32.2 L131.4 32.5 L134.3 32.8 L137.1 33.1 L140 33.4 L142.8 33.7 L145.7 34 L148.5 34.3 L151.4 34.7 L154.2 35 L157.1 35.4 L159.9 35.8 L162.8 36.2 L165.7 36.6 L168.5 37 L171.4 37.4 L174.2 37.8 L177.1 38.3 L179.9 38.7 L182.8 39.2 L185.6 39.7 L188.5 40.1 L191.4 40.6 L194.2 41.1 L197.1 41.6 L199.9 42.1 L202.8 42.6 L205.6 43.2 L208.5 43.7 L211.3 44.2 L214.2 44.8 L217.1 45.3 L219.9 45.9 L222.8 46.5 L225.6 47 L228.5 47.6 L231.3 48.2 L234.2 48.8 L237 49.4 L239.9 50 L242.8 50.6 L245.6 51.2 L248.5 51.8 L251.3 52.4 L254.2 53 L257 53.7 L259.9 54.3 L262.7 54.9 L265.6 55.6 L268.5 56.2 L271.3 56.8 L274.2 57.5 L277 58.1 L279.9 58.8 L282.7 59.4 L285.6 60.1 L288.4 60.7 L291.3 61.4 L294.2 62 L297 62.7 L299.9 63.3 L302.7 64 L305.6 64.6 L308.4 65.3 L311.3 65.9 L314.1 66.6 L317 67.2 L319.8 67.9 L322.7 68.5 L325.6 69.2 L328.4 69.8 L331.3 70.5 L334.1 71.1 L337 71.7 L339.8 72.4 L342.7 73 L345.5 73.7 L348.4 74.3 L351.3 74.9 L354.1 75.5 L357 76.1 L359.8 76.8 L362.7 77.4 L365.5 78 L368.4 78.6 L371.2 79.2 L374.1 79.7 L377 80.3 L379.8 80.9 L382.7 81.5 L385.5 82.1 L388.4 82.6 L391.2 83.2 L394.1 83.7 L396.9 84.3 L399.8 84.8 L402.7 85.3 L405.5 85.8 L408.4 86.3 L411.2 86.8 L414.1 87.3 L416.9 87.8 L419.8 88.3 L422.6 88.8 L425.5 89.2 L428.4 89.7 L431.2 90.1 L434.1 90.6 L436.9 91 L439.8 91.4 L442.6 91.8 L445.5 92.2 L448.3 92.6 L451.2 92.9 L454.1 93.3 L456.9 93.6 L459.8 94 L462.6 94.3 L465.5 94.6 L468.3 94.9 L471.2 95.2 L474 95.5 L476.9 95.7 L479.7 96 L482.6 96.2 L485.5 96.4 L488.3 96.6 L491.2 96.8 L494 97 L496.9 97.2 L499.7 97.3 L502.6 97.5 L505.4 97.6 L508.3 97.7 L511.2 97.8 L514 97.9 L516.9 97.9 L519.7 98 L522.6 98 L525.4 98 L528.3 98 L531.1 98 L534 98" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <path d="M80 30 L82.9 30 L85.7 30.1 L88.6 30.3 L91.4 30.5 L94.3 30.8 L97.1 31.1 L100 31.5 L102.8 32 L105.7 32.5 L108.6 33.1 L111.4 33.7 L114.3 34.4 L117.1 35 L120 35.7 L122.8 36.3 L125.7 37 L128.5 37.6 L131.4 38.3 L134.3 39 L137.1 39.6 L140 40.3 L142.8 40.9 L145.7 41.6 L148.5 42.2 L151.4 42.9 L154.2 43.5 L157.1 44.2 L159.9 44.8 L162.8 45.5 L165.7 46.1 L168.5 46.8 L171.4 47.4 L174.2 48.1 L177.1 48.8 L179.9 49.4 L182.8 50.1 L185.6 50.7 L188.5 51.4 L191.4 52 L194.2 52.7 L197.1 53.3 L199.9 54 L202.8 54.6 L205.6 55.3 L208.5 55.9 L211.3 56.6 L214.2 57.2 L217.1 57.9 L219.9 58.6 L222.8 59.2 L225.6 59.9 L228.5 60.5 L231.3 61.2 L234.2 61.8 L237 62.5 L239.9 63.1 L242.8 63.8 L245.6 64.4 L248.5 65.1 L251.3 65.7 L254.2 66.4 L257 67 L259.9 67.7 L262.7 68.4 L265.6 69 L268.5 69.7 L271.3 70.3 L274.2 71 L277 71.6 L279.9 72.3 L282.7 72.9 L285.6 73.6 L288.4 74.2 L291.3 74.9 L294.2 75.5 L297 76.2 L299.9 76.9 L302.7 77.5 L305.6 78.2 L308.4 78.8 L311.3 79.5 L314.1 80.1 L317 80.8 L319.8 81.4 L322.7 82.1 L325.6 82.7 L328.4 83.4 L331.3 84 L334.1 84.7 L337 85.3 L339.8 86 L342.7 86.7 L345.5 87.3 L348.4 88 L351.3 88.6 L354.1 89.3 L357 89.9 L359.8 90.6 L362.7 91.2 L365.5 91.9 L368.4 92.5 L371.2 93.2 L374.1 93.8 L377 94.5 L379.8 95.1 L382.7 95.7 L385.5 96.2 L388.4 96.6 L391.2 97 L394.1 97.3 L396.9 97.6 L399.8 97.8 L402.7 97.9 L405.5 98 L408.4 98 L411.2 98 L414.1 98 L416.9 98 L419.8 98 L422.6 98 L425.5 98 L428.4 98 L431.2 98 L434.1 98 L436.9 98 L439.8 98 L442.6 98 L445.5 98 L448.3 98 L451.2 98 L454.1 98 L456.9 98 L459.8 98 L462.6 98 L465.5 98 L468.3 98 L471.2 98 L474 98 L476.9 98 L479.7 98 L482.6 98 L485.5 98 L488.3 98 L491.2 98 L494 98 L496.9 98 L499.7 98 L502.6 98 L505.4 98 L508.3 98 L511.2 98 L514 98 L516.9 98 L519.7 98 L522.6 98 L525.4 98 L528.3 98 L531.1 98 L534 98" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="407.4" cy="98" r="3.2" fill="currentColor"/>
    <circle cx="525.7" cy="98" r="3.2" fill="currentColor" fill-opacity="0.55"/>
    <rect x="110.3" y="146.4" width="266.9" height="57.6" fill="currentColor" fill-opacity="0.1"/>
    <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3" opacity="0.85"><line x1="80" y1="146.4" x2="534" y2="146.4"/></g>
    <path d="M80 204 L81.9 203 L83.8 202.1 L85.7 201.1 L87.6 200.1 L89.5 199.2 L91.4 198.3 L93.3 197.3 L95.2 196.4 L97.1 195.5 L99 194.6 L100.9 193.7 L102.8 192.8 L104.7 191.9 L106.6 191.1 L108.5 190.2 L110.4 189.4 L112.3 188.5 L114.2 187.7 L116.1 186.9 L118 186 L119.9 185.2 L121.8 184.4 L123.7 183.6 L125.6 182.8 L127.5 182.1 L129.4 181.3 L131.3 180.5 L133.2 179.8 L135.1 179 L137 178.3 L138.9 177.6 L140.8 176.9 L142.7 176.2 L144.6 175.5 L146.5 174.8 L148.4 174.1 L150.3 173.4 L152.2 172.7 L154.1 172.1 L156 171.4 L157.9 170.8 L159.8 170.1 L161.7 169.5 L163.6 168.9 L165.5 168.3 L167.4 167.7 L169.3 167.1 L171.2 166.5 L173.1 165.9 L175 165.4 L176.9 164.8 L178.8 164.3 L180.7 163.7 L182.6 163.2 L184.5 162.7 L186.4 162.1 L188.3 161.6 L190.2 161.1 L192.1 160.6 L194 160.1 L195.9 159.7 L197.8 159.2 L199.7 158.7 L201.6 158.3 L203.5 157.9 L205.4 157.4 L207.3 157 L209.2 156.6 L211.1 156.2 L213 155.8 L214.9 155.4 L216.8 155 L218.7 154.6 L220.6 154.3 L222.5 153.9 L224.4 153.5 L226.3 153.2 L228.2 152.9 L230.1 152.5 L232 152.2 L233.9 151.9 L235.8 151.6 L237.7 151.3 L239.6 151 L241.5 150.8 L243.4 150.5 L245.3 150.2 L247.2 150 L249.1 149.8 L251 149.5 L252.9 149.3 L254.8 149.1 L256.7 148.9 L258.6 148.7 L260.5 148.5 L262.4 148.3 L264.3 148.1 L266.2 148 L268.1 147.8 L270 147.7 L271.9 147.5 L273.8 147.4 L275.7 147.3 L277.6 147.1 L279.5 147 L281.4 146.9 L283.3 146.8 L285.2 146.8 L287.1 146.7 L289 146.6 L290.9 146.6 L292.8 146.5 L294.7 146.5 L296.6 146.4 L298.5 146.4 L300.4 146.4 L302.3 146.4 L304.2 146.4 L306.1 146.4 L307.9 146.4 L309.8 146.5 L311.7 146.5 L313.6 146.5 L315.5 146.6 L317.4 146.6 L319.3 146.7 L321.2 146.8 L323.1 146.9 L325 147 L326.9 147.1 L328.8 147.2 L330.7 147.3 L332.6 147.4 L334.5 147.6 L336.4 147.7 L338.3 147.9 L340.2 148 L342.1 148.2 L344 148.4 L345.9 148.6 L347.8 148.7 L349.7 148.9 L351.6 149.2 L353.5 149.4 L355.4 149.6 L357.3 149.8 L359.2 150.1 L361.1 150.3 L363 150.6 L364.9 150.9 L366.8 151.1 L368.7 151.4 L370.6 151.7 L372.5 152 L374.4 152.3 L376.3 152.7 L378.2 153 L380.1 153.3 L382 153.7 L383.9 154 L385.8 154.4 L387.7 154.8 L389.6 155.1 L391.5 155.5 L393.4 155.9 L395.3 156.3 L397.2 156.7 L399.1 157.1 L401 157.6 L402.9 158 L404.8 158.5 L406.7 158.9 L408.6 159.4 L410.5 159.8 L412.4 160.3 L414.3 160.8 L416.2 161.3 L418.1 161.8 L420 162.3 L421.9 162.8 L423.8 163.4 L425.7 163.9 L427.6 164.5 L429.5 165 L431.4 165.6 L433.3 166.1 L435.2 166.7 L437.1 167.3 L439 167.9 L440.9 168.5 L442.8 169.1 L444.7 169.7 L446.6 170.4 L448.5 171 L450.4 171.7 L452.3 172.3 L454.2 173 L456.1 173.6 L458 174.3 L459.9 175 L461.8 175.7 L463.7 176.4 L465.6 177.1 L467.5 177.8 L469.4 178.6 L471.3 179.3 L473.2 180.1 L475.1 180.8 L477 181.6 L478.9 182.3 L480.8 183.1 L482.7 183.9 L484.6 184.7 L486.5 185.5 L488.4 186.3 L490.3 187.2 L492.2 188 L494.1 188.8 L496 189.7 L497.9 190.5 L499.8 191.4 L501.7 192.3 L503.6 193.1 L505.5 194 L507.4 194.9 L509.3 195.8 L511.2 196.7 L513.1 197.7 L515 198.6 L516.9 199.5 L518.8 200.5 L520.7 201.4 L522.6 202.4 L524.5 203.4 L526.4 204 L528.3 204 L530.2 204 L532.1 204 L534 204" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <polyline points="80,204 110.3,146.4 377.1,146.4 407.4,204 534,204" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="302.9" cy="146.4" r="2.6" fill="currentColor" fill-opacity="0.6"/>
    <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3" opacity="0.85"><line x1="80" y1="254" x2="534" y2="254"/><line x1="80" y1="310" x2="534" y2="310"/></g>
    <rect x="80" y="254" width="30.3" height="28" fill="currentColor" fill-opacity="0.12"/>
    <rect x="377.1" y="282" width="30.3" height="28" fill="currentColor" fill-opacity="0.12"/>
    <path d="M80 282 L80 254 L110.3 254 L110.3 282 L377.1 282 L377.1 310 L407.4 310 L407.4 282 L534 282" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M80 274.4 L525.7 289.6" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <g fill="currentColor">
    <text x="80" y="18" font-size="11" font-weight="bold">elbow θ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> (deg)</tspan></text>
    <text x="137" y="124" font-size="11" text-anchor="end" font-weight="bold">speed |θ̇</text>
    <text x="137" y="124" font-size="11" font-weight="bold"><tspan dy="3.5">2</tspan><tspan dy="-3.5">| (rad/s)</tspan></text>
    <text x="96" y="229" font-size="11" text-anchor="end" font-weight="bold">d|θ̇</text>
    <text x="96" y="229" font-size="11" font-weight="bold"><tspan dy="3.5">2</tspan><tspan dy="-3.5">|/dt (rad/s²)</tspan></text>
    <text x="73" y="34" font-size="11" text-anchor="end">90°</text>
    <text x="73" y="68" font-size="11" text-anchor="end">0°</text>
    <text x="73" y="102" font-size="11" text-anchor="end">−90°</text>
    <text x="73" y="208" font-size="11" text-anchor="end">0</text>
    <text x="73" y="179.2" font-size="11" text-anchor="end">0.4</text>
    <text x="73" y="150.4" font-size="11" text-anchor="end">0.8</text>
    <text x="73" y="258" font-size="11" text-anchor="end">2</text>
    <text x="73" y="286" font-size="11" text-anchor="end">0</text>
    <text x="73" y="314" font-size="11" text-anchor="end">−2</text>
    <text x="80" y="332.3" font-size="11" text-anchor="middle">0</text>
    <text x="155.7" y="332.3" font-size="11" text-anchor="middle">1</text>
    <text x="231.3" y="332.3" font-size="11" text-anchor="middle">2</text>
    <text x="307" y="332.3" font-size="11" text-anchor="middle">3</text>
    <text x="382.7" y="332.3" font-size="11" text-anchor="middle">4</text>
    <text x="458.3" y="332.3" font-size="11" text-anchor="middle">5</text>
    <text x="534" y="332.3" font-size="11" text-anchor="middle">6</text>
    <text x="307" y="347.3" font-size="11" text-anchor="middle">time (s)</text>
    <text x="407.4" y="113" font-size="11" text-anchor="middle">4.327 s</text>
    <text x="525.7" y="113" font-size="11" text-anchor="middle">5.890 s</text>
    <text x="202.6" y="71.6" font-size="11" text-anchor="end">trapezoid</text>
    <text x="246.5" y="44.4" font-size="11" opacity="0.75">cubic</text>
    <text x="518.9" y="141.4" font-size="11" text-anchor="end">v<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">= 0.8</tspan></text>
    <text x="518.9" y="249" font-size="11" text-anchor="end">a<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">= 2</tspan></text>
    <text x="117.8" y="305" font-size="11">−a<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">= −2</tspan></text>
    <text x="243.4" y="198.2" font-size="11" text-anchor="middle">at v<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">for 3.527 s (81.5 % of the move)</tspan></text>
    <text x="97.1" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="392.3" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="126.9" y="273.3" font-size="11" opacity="0.8">cubic peak 0.543 rad/s² (27 % of a<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1">)</tspan></text>
    </g>
    <line x1="350" y1="14" x2="372" y2="14" stroke="currentColor" stroke-width="2.2"/>
    <text x="377" y="18" font-size="11" fill="currentColor">trapezoid</text>
    <line x1="450" y1="14" x2="472" y2="14" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <text x="477" y="18" font-size="11" fill="currentColor">cubic</text>
  </g>
</svg>

The elbow flip on plant **P2**, $|\Delta\theta_2| = \pi$, timed two ways on one $0$–$6\,\mathrm{s}$ axis: the elbow angle on top, its speed $|\dot\theta_2|$ in the middle against $v_{\max} = 0.8\,\mathrm{rad/s}$, and the rate of change of that speed at the bottom against $a_{\max} = 2\,\mathrm{rad/s^2}$. The trapezoid finishes at $4.327\,\mathrm{s}$ — $0.4\,\mathrm{s}$ ramps at $\pm a_{\max}$ around $3.527\,\mathrm{s}$ spent at $v_{\max}$, $81.5\,\%$ of the move — while the cubic needs $5.890\,\mathrm{s}$, touches $v_{\max}$ only at its midpoint, and peaks at $0.543\,\mathrm{rad/s^2}$, $27\,\%$ of $a_{\max}$. The figure's whole message is which dashed line each profile touches: the trapezoid both, the cubic only the velocity limit.

### Worked case · 대상으로 한 번 끝까지

Both joints ride one time scaling $s(t)$ — a monotone map from $[0, T]$ onto $[0, 1]$ that says how far along the path the arm is at time $t$, defined in §2 — so joint $i$ has $\dot\theta_i = \Delta\theta_i\,\dot s$ and $\ddot\theta_i = \Delta\theta_i\,\ddot s$. Every peak is therefore proportional to $|\Delta\theta_i|$, and the joint with the largest $|\Delta\theta_i|$ hits its limit first. Here that is the elbow, at $|\Delta\theta_2| = \pi = 3.1416\,\mathrm{rad}$, exactly twice the shoulder. **Design the scaling for the elbow and the shoulder follows for free.**

**A — the trapezoid** (constant acceleration $+a_{\max}$, cruise at $v_{\max}$, constant deceleration $-a_{\max}$; defined in §3). First decide whether a cruise phase exists at all, because a short move never reaches $v_{\max}$: ramping to $v_{\max}$ and straight back down covers $2 \cdot \tfrac12 a_{\max}t_a^2$ with $t_a = v_{\max}/a_{\max}$, i.e.

$$\Delta\theta^{*} = \frac{v_{\max}^2}{a_{\max}} = \frac{0.8^2}{2} = 0.32\ \mathrm{rad}$$

and since our $3.1416\,\mathrm{rad}$ is far above that, the profile is a true trapezoid rather than a triangle. Then:

- ramp time $t_a = v_{\max}/a_{\max} = 0.8/2 = 0.4\ \mathrm{s}$, covering $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16\ \mathrm{rad}$ on the way up and $0.16\,\mathrm{rad}$ on the way down;
- cruise distance $3.1416 - 0.32 = 2.8216\ \mathrm{rad}$, at $0.8\,\mathrm{rad/s}$, taking $2.8216/0.8 = 3.5270\ \mathrm{s}$;
- total $T_{\text{trap}} = 0.4 + 3.5270 + 0.4 = \mathbf{4.327\ s}$, of which the cruise is $3.5270/4.327 = 81.5\,\%$.

Check the shoulder, which rides the same $s(t)$ at half the amplitude: peak velocity $0.5 \times 0.8 = 0.4\,\mathrm{rad/s}$ and peak acceleration $0.5 \times 2 = 1\,\mathrm{rad/s^2}$. Both are at half their limits, so the shoulder is idle in the binding sense — it never constrains anything.

**B — the cubic, on the same move.** For $s(t) = 3t^2/T^2 - 2t^3/T^3$, differentiating gives $\dot s = (6t/T^2)(1 - t/T)$ and $\ddot s = (6/T^2)(1 - 2t/T)$, so the unit-move peaks are $\dot s_{\max} = 1.5/T$ at $t = T/2$ and $|\ddot s|_{\max} = 6/T^2$ at the two ends, and the elbow's peaks are $1.5\,\Delta\theta/T$ and $6\,\Delta\theta/T^2$. Invert each limit separately for the shortest admissible duration:

$$T_v = \frac{1.5\,\Delta\theta}{v_{\max}} = \frac{1.5 \times 3.1416}{0.8} = 5.8905\ \mathrm{s}, \qquad T_a = \sqrt{\frac{6\,\Delta\theta}{a_{\max}}} = \sqrt{\frac{6 \times 3.1416}{2}} = 3.0700\ \mathrm{s}$$

because a longer $T$ lowers both peaks, so each limit sets a floor and the move must satisfy the larger of the two. Here $T_v > T_a$, so $T_{\text{cubic}} = \mathbf{5.890\ s}$ and **velocity is the binding limit**. Confirm by back-substitution: at that duration the peak acceleration is $6 \times 3.1416/5.8905^2 = 0.543\,\mathrm{rad/s^2}$, only $27\,\%$ of $a_{\max}$ — the motor's torque is almost entirely unused.

**C — read the two against each other.** Force the cubic into the trapezoid's duration and it asks for $1.5 \times 3.1416/4.327 = 1.089\,\mathrm{rad/s}$, which is $36\,\%$ over $v_{\max}$: at $T = 4.327\,\mathrm{s}$ the cubic is simply not executable on this joint. Compare the two admissible durations instead:

$$\frac{T_{\text{cubic}}}{T_{\text{trap}}} = \frac{5.8905}{4.3270} = 1.361 \quad\Longrightarrow\quad \text{the trapezoid finishes } 26.5\,\% \text{ sooner}$$

and the reason is visible in the middle panel of the picture: the trapezoid sits *at* $v_{\max}$ for $81.5\,\%$ of the move, while the cubic reaches $v_{\max}$ at one instant and is below it everywhere else. Spending the whole move at the limit is the entire advantage, and it is paid for with a discontinuous acceleration at the two corners.

**D — which limit binds, in general.** Setting $T_v = T_a$ and solving gives the crossover for a cubic:

$$\Delta\theta^{\dagger} = \frac{8}{3}\cdot\frac{v_{\max}^2}{a_{\max}} = \frac{8}{3}\cdot\frac{0.64}{2} = 0.853\ \mathrm{rad}$$

because $1.5\Delta\theta/v_{\max} = \sqrt{6\Delta\theta/a_{\max}}$ squares to $2.25\Delta\theta^2/v_{\max}^2 = 6\Delta\theta/a_{\max}$. Above $0.853\,\mathrm{rad}$ velocity binds; below it acceleration binds. Two moves on this page — the elbow's $3.1416$ here and the $1.2$ of §1's worked example — are above it, which is why both are velocity-bound; a $0.5\,\mathrm{rad}$ move is below it, and self-check 4 times one. The problem set moves the plant to the other side of this line without changing $\Delta\theta$ at all.

<svg viewBox="0 0 560 306" style="max-width:100%;height:auto" role="img" aria-label="Duration against move size for one joint at P2's frozen limits, 0.8 rad/s and 2 rad/s²: the trapezoid and the fastest cubic. Below 0.32 rad the trapezoid is a triangle; below 0.853 rad the cubic is acceleration-bound, above it velocity-bound. The moves 0.5, 1.2, π/2 and π rad are marked.">
  <defs><marker id="mr09dure" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <rect x="62" y="36" width="107.3" height="226" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.6"><line x1="62" y1="262" x2="502" y2="262"/><line x1="62" y1="262" x2="62" y2="36"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="62.0" y1="262" x2="62.0" y2="266"/><line x1="124.9" y1="262" x2="124.9" y2="266"/><line x1="187.7" y1="262" x2="187.7" y2="266"/><line x1="250.6" y1="262" x2="250.6" y2="266"/><line x1="313.4" y1="262" x2="313.4" y2="266"/><line x1="376.3" y1="262" x2="376.3" y2="266"/><line x1="439.1" y1="262" x2="439.1" y2="266"/><line x1="502.0" y1="262" x2="502.0" y2="266"/><line x1="58" y1="262.0" x2="62" y2="262.0"/><line x1="58" y1="229.7" x2="62" y2="229.7"/><line x1="58" y1="197.4" x2="62" y2="197.4"/><line x1="58" y1="165.1" x2="62" y2="165.1"/><line x1="58" y1="132.9" x2="62" y2="132.9"/><line x1="58" y1="100.6" x2="62" y2="100.6"/><line x1="58" y1="68.3" x2="62" y2="68.3"/><line x1="58" y1="36.0" x2="62" y2="36.0"/></g>
  <polyline points="62.0,262.0 63.3,261.4 64.5,260.8 65.8,260.2 67.0,259.6 68.3,259.0 69.6,258.4 70.8,257.8 72.1,257.2 73.3,256.5 74.6,255.9 75.8,255.3 77.1,254.7 78.4,254.1 79.6,253.5 80.9,252.9 82.1,252.3 83.4,251.7 84.6,251.1 85.9,250.5 87.2,249.9 88.4,249.3 89.7,248.7 90.9,248.1 92.2,247.5 93.4,246.9 94.7,246.3 96.0,245.6 97.2,245.0 98.5,244.4 99.7,243.8 101.0,243.2 102.2,242.6 103.5,242.0 104.8,241.4 106.0,240.8 107.3,240.2 108.5,239.6 109.8,239.0 111.0,238.4 112.3,237.8 113.6,237.2 114.8,236.6 116.1,236.0 117.3,235.4 118.6,234.8 119.8,234.1 121.1,233.5 122.4,232.9 123.6,232.3 124.9,231.7 126.1,231.1 127.4,230.5 128.6,229.9 129.9,229.3 131.2,228.7 132.4,228.1 133.7,227.5 134.9,226.9 136.2,226.3 137.4,225.7 138.7,225.1 140.0,224.5 141.2,223.9 142.5,223.3 143.7,222.6 145.0,222.0 146.2,221.4 147.5,220.8 148.8,220.2 150.0,219.6 151.3,219.0 152.5,218.4 153.8,217.8 155.0,217.2 156.3,216.6 157.6,216.0 158.8,215.4 160.1,214.8 161.3,214.2 162.6,213.6 163.8,213.0 165.1,212.4 166.4,211.8 167.6,211.1 168.9,210.5 170.1,209.9 171.4,209.3 172.6,208.7 173.9,208.1 175.2,207.5 176.4,206.9 177.7,206.3 178.9,205.7 180.2,205.1 181.4,204.5 182.7,203.9 184.0,203.3 185.2,202.7 186.5,202.1 187.7,201.5 189.0,200.9 190.2,200.2 191.5,199.6 192.8,199.0 194.0,198.4 195.3,197.8 196.5,197.2 197.8,196.6 199.0,196.0 200.3,195.4 201.6,194.8 202.8,194.2 204.1,193.6 205.3,193.0 206.6,192.4 207.8,191.8 209.1,191.2 210.4,190.6 211.6,190.0 212.9,189.4 214.1,188.7 215.4,188.1 216.6,187.5 217.9,186.9 219.2,186.3 220.4,185.7 221.7,185.1 222.9,184.5 224.2,183.9 225.4,183.3 226.7,182.7 228.0,182.1 229.2,181.5 230.5,180.9 231.7,180.3 233.0,179.7 234.2,179.1 235.5,178.5 236.8,177.9 238.0,177.2 239.3,176.6 240.5,176.0 241.8,175.4 243.0,174.8 244.3,174.2 245.6,173.6 246.8,173.0 248.1,172.4 249.3,171.8 250.6,171.2 251.8,170.6 253.1,170.0 254.3,169.4 255.6,168.8 256.9,168.2 258.1,167.6 259.4,167.0 260.6,166.4 261.9,165.7 263.1,165.1 264.4,164.5 265.7,163.9 266.9,163.3 268.2,162.7 269.4,162.1 270.7,161.5 271.9,160.9 273.2,160.3 274.5,159.7 275.7,159.1 277.0,158.5 278.2,157.9 279.5,157.3 280.7,156.7 282.0,156.1 283.3,155.5 284.5,154.8 285.8,154.2 287.0,153.6 288.3,153.0 289.5,152.4 290.8,151.8 292.1,151.2 293.3,150.6 294.6,150.0 295.8,149.4 297.1,148.8 298.3,148.2 299.6,147.6 300.9,147.0 302.1,146.4 303.4,145.8 304.6,145.2 305.9,144.6 307.1,144.0 308.4,143.3 309.7,142.7 310.9,142.1 312.2,141.5 313.4,140.9 314.7,140.3 315.9,139.7 317.2,139.1 318.5,138.5 319.7,137.9 321.0,137.3 322.2,136.7 323.5,136.1 324.7,135.5 326.0,134.9 327.3,134.3 328.5,133.7 329.8,133.1 331.0,132.5 332.3,131.8 333.5,131.2 334.8,130.6 336.1,130.0 337.3,129.4 338.6,128.8 339.8,128.2 341.1,127.6 342.3,127.0 343.6,126.4 344.9,125.8 346.1,125.2 347.4,124.6 348.6,124.0 349.9,123.4 351.1,122.8 352.4,122.2 353.7,121.6 354.9,120.9 356.2,120.3 357.4,119.7 358.7,119.1 359.9,118.5 361.2,117.9 362.5,117.3 363.7,116.7 365.0,116.1 366.2,115.5 367.5,114.9 368.7,114.3 370.0,113.7 371.3,113.1 372.5,112.5 373.8,111.9 375.0,111.3 376.3,110.7 377.5,110.1 378.8,109.4 380.1,108.8 381.3,108.2 382.6,107.6 383.8,107.0 385.1,106.4 386.3,105.8 387.6,105.2 388.9,104.6 390.1,104.0 391.4,103.4 392.6,102.8 393.9,102.2 395.1,101.6 396.4,101.0 397.7,100.4 398.9,99.8 400.2,99.2 401.4,98.6 402.7,97.9 403.9,97.3 405.2,96.7 406.5,96.1 407.7,95.5 409.0,94.9 410.2,94.3 411.5,93.7 412.7,93.1 414.0,92.5 415.3,91.9 416.5,91.3 417.8,90.7 419.0,90.1 420.3,89.5 421.5,88.9 422.8,88.3 424.1,87.7 425.3,87.1 426.6,86.4 427.8,85.8 429.1,85.2 430.3,84.6 431.6,84.0 432.9,83.4 434.1,82.8 435.4,82.2 436.6,81.6 437.9,81.0 439.1,80.4 440.4,79.8 441.7,79.2 442.9,78.6 444.2,78.0 445.4,77.4 446.7,76.8 447.9,76.2 449.2,75.5 450.5,74.9 451.7,74.3 453.0,73.7 454.2,73.1 455.5,72.5 456.7,71.9 458.0,71.3 459.3,70.7 460.5,70.1 461.8,69.5 463.0,68.9 464.3,68.3 465.5,67.7 466.8,67.1 468.1,66.5 469.3,65.9 470.6,65.3 471.8,64.7 473.1,64.0 474.3,63.4 475.6,62.8 476.9,62.2 478.1,61.6 479.4,61.0 480.6,60.4 481.9,59.8 483.1,59.2 484.4,58.6 485.7,58.0 486.9,57.4 488.2,56.8 489.4,56.2 490.7,55.6 491.9,55.0 493.2,54.4 494.5,53.8 495.7,53.2 497.0,52.5 498.2,51.9 499.5,51.3 500.7,50.7 502.0,50.1" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="2 3" opacity="0.5"/>
  <polyline points="62.0,261.4 63.3,256.4 64.5,254.1 65.8,252.3 67.0,250.8 68.3,249.5 69.6,248.3 70.8,247.2 72.1,246.2 73.3,245.2 74.6,244.3 75.8,243.4 77.1,242.6 78.4,241.8 79.6,241.1 80.9,240.3 82.1,239.6 83.4,238.9 84.6,238.3 85.9,237.6 87.2,237.0 88.4,236.4 89.7,235.8 90.9,235.2 92.2,234.6 93.4,234.0 94.7,233.5 96.0,232.9 97.2,232.4 98.5,231.9 99.7,231.4 101.0,230.9 102.2,230.4 103.5,229.9 104.8,229.4 106.0,228.9 107.3,228.4 108.5,228.0 109.8,227.5 111.0,227.1 112.3,226.6 113.6,226.2 114.8,225.8 116.1,225.3 117.3,224.9 118.6,224.5 119.8,224.1 121.1,223.7 122.4,223.3 123.6,222.9 124.9,222.5 126.1,222.1 127.4,221.7 128.6,221.3 129.9,220.9 131.2,220.5 132.4,220.1 133.7,219.8 134.9,219.4 136.2,219.0 137.4,218.7 138.7,218.3 140.0,218.0 141.2,217.6 142.5,217.3 143.7,216.9 145.0,216.6 146.2,216.2 147.5,215.9 148.8,215.5 150.0,215.2 151.3,214.9 152.5,214.5 153.8,214.2 155.0,213.9 156.3,213.6 157.6,213.2 158.8,212.9 160.1,212.6 161.3,212.3 162.6,212.0 163.8,211.7 165.1,211.4 166.4,211.1 167.6,210.7 168.9,210.4 170.1,210.1 171.4,209.8 172.6,209.5 173.9,209.2 175.2,208.9 176.4,208.7 177.7,208.4 178.9,208.1 180.2,207.8 181.4,207.5 182.7,207.2 184.0,206.9 185.2,206.6 186.5,206.4 187.7,206.1 189.0,205.8 190.2,205.5 191.5,205.2 192.8,205.0 194.0,204.7 195.3,204.4 196.5,204.2 197.8,203.9 199.0,203.6 200.3,203.3 201.6,203.1 202.8,202.8 204.1,202.6 205.3,202.3 206.6,202.0 207.8,201.8 209.1,201.5 210.4,201.3 211.6,201.0 212.9,200.7 214.1,200.5 215.4,200.2 216.6,200.0 217.9,199.7 219.2,199.5 220.4,199.2 221.7,199.0 222.9,198.7 224.2,198.5 225.4,198.2 226.7,198.0 228.0,197.8 229.2,197.5 230.5,197.3 231.7,197.0 233.0,196.8 234.2,196.5 235.5,196.3 236.8,196.1 238.0,195.8 239.3,195.6 240.5,195.4 241.8,195.1 243.0,194.9 244.3,194.7 245.6,194.4 246.8,194.2 248.1,194.0 249.3,193.7 250.6,193.5 251.8,193.3 253.1,193.1 254.3,192.8 255.6,192.6 256.9,192.4 258.1,192.2 259.4,191.9 260.6,191.7 261.9,191.5 263.1,191.3 264.4,191.0 265.7,190.8 266.9,190.6 268.2,190.4 269.4,190.2 270.7,190.0 271.9,189.7 273.2,189.5 274.5,189.3 275.7,189.1 277.0,188.9 278.2,188.7 279.5,188.4 280.7,188.2 282.0,188.0 283.3,187.8 284.5,187.6 285.8,187.4 287.0,187.2 288.3,187.0 289.5,186.8 290.8,186.6 292.1,186.4 293.3,186.1 294.6,185.9 295.8,185.7 297.1,185.5 298.3,185.3 299.6,185.1 300.9,184.9 302.1,184.7 303.4,184.5 304.6,184.3 305.9,184.1 307.1,183.9 308.4,183.7 309.7,183.5 310.9,183.3 312.2,183.1 313.4,182.9 314.7,182.7 315.9,182.5 317.2,182.3 318.5,182.1 319.7,181.9 321.0,181.7 322.2,181.5 323.5,181.3 324.7,181.2 326.0,181.0 327.3,180.8 328.5,180.6 329.8,180.4 331.0,180.2 332.3,180.0 333.5,179.8 334.8,179.6 336.1,179.4 337.3,179.2 338.6,179.1 339.8,178.9 341.1,178.7 342.3,178.5 343.6,178.3 344.9,178.1 346.1,177.9 347.4,177.7 348.6,177.6 349.9,177.4 351.1,177.2 352.4,177.0 353.7,176.8 354.9,176.6 356.2,176.5 357.4,176.3 358.7,176.1 359.9,175.9 361.2,175.7 362.5,175.5 363.7,175.4 365.0,175.2 366.2,175.0 367.5,174.8 368.7,174.6 370.0,174.5 371.3,174.3 372.5,174.1 373.8,173.9 375.0,173.8 376.3,173.6 377.5,173.4 378.8,173.2 380.1,173.1 381.3,172.9 382.6,172.7 383.8,172.5 385.1,172.4 386.3,172.2 387.6,172.0 388.9,171.8 390.1,171.7 391.4,171.5 392.6,171.3 393.9,171.1 395.1,171.0 396.4,170.8 397.7,170.6 398.9,170.5 400.2,170.3 401.4,170.1 402.7,169.9 403.9,169.8 405.2,169.6 406.5,169.4 407.7,169.3 409.0,169.1 410.2,168.9 411.5,168.8 412.7,168.6 414.0,168.4 415.3,168.3 416.5,168.1 417.8,167.9 419.0,167.8 420.3,167.6 421.5,167.4 422.8,167.3 424.1,167.1 425.3,166.9 426.6,166.8 427.8,166.6 429.1,166.4 430.3,166.3 431.6,166.1 432.9,166.0 434.1,165.8 435.4,165.6 436.6,165.5 437.9,165.3 439.1,165.1 440.4,165.0 441.7,164.8 442.9,164.7 444.2,164.5 445.4,164.3 446.7,164.2 447.9,164.0 449.2,163.9 450.5,163.7 451.7,163.5 453.0,163.4 454.2,163.2 455.5,163.1 456.7,162.9 458.0,162.8 459.3,162.6 460.5,162.4 461.8,162.3 463.0,162.1 464.3,162.0 465.5,161.8 466.8,161.7 468.1,161.5 469.3,161.3 470.6,161.2 471.8,161.0 473.1,160.9 474.3,160.7 475.6,160.6 476.9,160.4 478.1,160.3 479.4,160.1 480.6,160.0 481.9,159.8 483.1,159.6 484.4,159.5 485.7,159.3 486.9,159.2 488.2,159.0 489.4,158.9 490.7,158.7 491.9,158.6 493.2,158.4 494.5,158.3 495.7,158.1 497.0,158.0 498.2,157.8 499.5,157.7 500.7,157.5 502.0,157.4" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="2 3" opacity="0.5"/>
  <polyline points="62.0,261.4 63.3,256.4 64.5,254.1 65.8,252.3 67.0,250.8 68.3,249.5 69.6,248.3 70.8,247.2 72.1,246.2 73.3,245.2 74.6,244.3 75.8,243.4 77.1,242.6 78.4,241.8 79.6,241.1 80.9,240.3 82.1,239.6 83.4,238.9 84.6,238.3 85.9,237.6 87.2,237.0 88.4,236.4 89.7,235.8 90.9,235.2 92.2,234.6 93.4,234.0 94.7,233.5 96.0,232.9 97.2,232.4 98.5,231.9 99.7,231.4 101.0,230.9 102.2,230.4 103.5,229.9 104.8,229.4 106.0,228.9 107.3,228.4 108.5,228.0 109.8,227.5 111.0,227.1 112.3,226.6 113.6,226.2 114.8,225.8 116.1,225.3 117.3,224.9 118.6,224.5 119.8,224.1 121.1,223.7 122.4,223.3 123.6,222.9 124.9,222.5 126.1,222.1 127.4,221.7 128.6,221.3 129.9,220.9 131.2,220.5 132.4,220.1 133.7,219.8 134.9,219.4 136.2,219.0 137.4,218.7 138.7,218.3 140.0,218.0 141.2,217.6 142.5,217.3 143.7,216.9 145.0,216.6 146.2,216.2 147.5,215.9 148.8,215.5 150.0,215.2 151.3,214.9 152.5,214.5 153.8,214.2 155.0,213.9 156.3,213.6 157.6,213.2 158.8,212.9 160.1,212.6 161.3,212.3 162.6,212.0 163.8,211.7 165.1,211.4 166.4,211.1 167.6,210.7 168.9,210.4 170.1,209.9 171.4,209.3 172.6,208.7 173.9,208.1 175.2,207.5 176.4,206.9 177.7,206.3 178.9,205.7 180.2,205.1 181.4,204.5 182.7,203.9 184.0,203.3 185.2,202.7 186.5,202.1 187.7,201.5 189.0,200.9 190.2,200.2 191.5,199.6 192.8,199.0 194.0,198.4 195.3,197.8 196.5,197.2 197.8,196.6 199.0,196.0 200.3,195.4 201.6,194.8 202.8,194.2 204.1,193.6 205.3,193.0 206.6,192.4 207.8,191.8 209.1,191.2 210.4,190.6 211.6,190.0 212.9,189.4 214.1,188.7 215.4,188.1 216.6,187.5 217.9,186.9 219.2,186.3 220.4,185.7 221.7,185.1 222.9,184.5 224.2,183.9 225.4,183.3 226.7,182.7 228.0,182.1 229.2,181.5 230.5,180.9 231.7,180.3 233.0,179.7 234.2,179.1 235.5,178.5 236.8,177.9 238.0,177.2 239.3,176.6 240.5,176.0 241.8,175.4 243.0,174.8 244.3,174.2 245.6,173.6 246.8,173.0 248.1,172.4 249.3,171.8 250.6,171.2 251.8,170.6 253.1,170.0 254.3,169.4 255.6,168.8 256.9,168.2 258.1,167.6 259.4,167.0 260.6,166.4 261.9,165.7 263.1,165.1 264.4,164.5 265.7,163.9 266.9,163.3 268.2,162.7 269.4,162.1 270.7,161.5 271.9,160.9 273.2,160.3 274.5,159.7 275.7,159.1 277.0,158.5 278.2,157.9 279.5,157.3 280.7,156.7 282.0,156.1 283.3,155.5 284.5,154.8 285.8,154.2 287.0,153.6 288.3,153.0 289.5,152.4 290.8,151.8 292.1,151.2 293.3,150.6 294.6,150.0 295.8,149.4 297.1,148.8 298.3,148.2 299.6,147.6 300.9,147.0 302.1,146.4 303.4,145.8 304.6,145.2 305.9,144.6 307.1,144.0 308.4,143.3 309.7,142.7 310.9,142.1 312.2,141.5 313.4,140.9 314.7,140.3 315.9,139.7 317.2,139.1 318.5,138.5 319.7,137.9 321.0,137.3 322.2,136.7 323.5,136.1 324.7,135.5 326.0,134.9 327.3,134.3 328.5,133.7 329.8,133.1 331.0,132.5 332.3,131.8 333.5,131.2 334.8,130.6 336.1,130.0 337.3,129.4 338.6,128.8 339.8,128.2 341.1,127.6 342.3,127.0 343.6,126.4 344.9,125.8 346.1,125.2 347.4,124.6 348.6,124.0 349.9,123.4 351.1,122.8 352.4,122.2 353.7,121.6 354.9,120.9 356.2,120.3 357.4,119.7 358.7,119.1 359.9,118.5 361.2,117.9 362.5,117.3 363.7,116.7 365.0,116.1 366.2,115.5 367.5,114.9 368.7,114.3 370.0,113.7 371.3,113.1 372.5,112.5 373.8,111.9 375.0,111.3 376.3,110.7 377.5,110.1 378.8,109.4 380.1,108.8 381.3,108.2 382.6,107.6 383.8,107.0 385.1,106.4 386.3,105.8 387.6,105.2 388.9,104.6 390.1,104.0 391.4,103.4 392.6,102.8 393.9,102.2 395.1,101.6 396.4,101.0 397.7,100.4 398.9,99.8 400.2,99.2 401.4,98.6 402.7,97.9 403.9,97.3 405.2,96.7 406.5,96.1 407.7,95.5 409.0,94.9 410.2,94.3 411.5,93.7 412.7,93.1 414.0,92.5 415.3,91.9 416.5,91.3 417.8,90.7 419.0,90.1 420.3,89.5 421.5,88.9 422.8,88.3 424.1,87.7 425.3,87.1 426.6,86.4 427.8,85.8 429.1,85.2 430.3,84.6 431.6,84.0 432.9,83.4 434.1,82.8 435.4,82.2 436.6,81.6 437.9,81.0 439.1,80.4 440.4,79.8 441.7,79.2 442.9,78.6 444.2,78.0 445.4,77.4 446.7,76.8 447.9,76.2 449.2,75.5 450.5,74.9 451.7,74.3 453.0,73.7 454.2,73.1 455.5,72.5 456.7,71.9 458.0,71.3 459.3,70.7 460.5,70.1 461.8,69.5 463.0,68.9 464.3,68.3 465.5,67.7 466.8,67.1 468.1,66.5 469.3,65.9 470.6,65.3 471.8,64.7 473.1,64.0 474.3,63.4 475.6,62.8 476.9,62.2 478.1,61.6 479.4,61.0 480.6,60.4 481.9,59.8 483.1,59.2 484.4,58.6 485.7,58.0 486.9,57.4 488.2,56.8 489.4,56.2 490.7,55.6 491.9,55.0 493.2,54.4 494.5,53.8 495.7,53.2 497.0,52.5 498.2,51.9 499.5,51.3 500.7,50.7 502.0,50.1" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
  <polyline points="62.0,261.5 63.3,257.4 64.5,255.5 65.8,254.1 67.0,252.9 68.3,251.8 69.6,250.8 70.8,249.9 72.1,249.1 73.3,248.3 74.6,247.6 75.8,246.8 77.1,246.2 78.4,245.5 79.6,244.9 80.9,244.3 82.1,243.7 83.4,243.2 84.6,242.6 85.9,242.1 87.2,241.6 88.4,241.1 89.7,240.6 90.9,240.1 92.2,239.6 93.4,239.2 94.7,238.7 96.0,238.3 97.2,237.8 98.5,237.4 99.7,237.0 101.0,236.6 102.2,236.2 103.5,235.8 104.8,235.4 106.0,235.0 107.3,234.6 108.5,234.1 109.8,233.7 111.0,233.3 112.3,232.9 113.6,232.5 114.8,232.1 116.1,231.7 117.3,231.3 118.6,230.9 119.8,230.5 121.1,230.1 122.4,229.7 123.6,229.3 124.9,228.9 126.1,228.5 127.4,228.1 128.6,227.7 129.9,227.3 131.2,226.9 132.4,226.5 133.7,226.1 134.9,225.7 136.2,225.3 137.4,224.9 138.7,224.5 140.0,224.1 141.2,223.7 142.5,223.3 143.7,222.9 145.0,222.4 146.2,222.0 147.5,221.6 148.8,221.2 150.0,220.8 151.3,220.4 152.5,220.0 153.8,219.6 155.0,219.2 156.3,218.8 157.6,218.4 158.8,218.0 160.1,217.6 161.3,217.2 162.6,216.8 163.8,216.4 165.1,216.0 166.4,215.6 167.6,215.2 168.9,214.8 170.1,214.4 171.4,214.0 172.6,213.6 173.9,213.2 175.2,212.8 176.4,212.4 177.7,212.0 178.9,211.6 180.2,211.1 181.4,210.7 182.7,210.3 184.0,209.9 185.2,209.5 186.5,209.1 187.7,208.7 189.0,208.3 190.2,207.9 191.5,207.5 192.8,207.1 194.0,206.7 195.3,206.3 196.5,205.9 197.8,205.5 199.0,205.1 200.3,204.7 201.6,204.3 202.8,203.9 204.1,203.5 205.3,203.1 206.6,202.7 207.8,202.3 209.1,201.9 210.4,201.5 211.6,201.1 212.9,200.7 214.1,200.3 215.4,199.8 216.6,199.4 217.9,199.0 219.2,198.6 220.4,198.2 221.7,197.8 222.9,197.4 224.2,197.0 225.4,196.6 226.7,196.2 228.0,195.8 229.2,195.4 230.5,195.0 231.7,194.6 233.0,194.2 234.2,193.8 235.5,193.4 236.8,193.0 238.0,192.6 239.3,192.2 240.5,191.8 241.8,191.4 243.0,191.0 244.3,190.6 245.6,190.2 246.8,189.8 248.1,189.4 249.3,189.0 250.6,188.5 251.8,188.1 253.1,187.7 254.3,187.3 255.6,186.9 256.9,186.5 258.1,186.1 259.4,185.7 260.6,185.3 261.9,184.9 263.1,184.5 264.4,184.1 265.7,183.7 266.9,183.3 268.2,182.9 269.4,182.5 270.7,182.1 271.9,181.7 273.2,181.3 274.5,180.9 275.7,180.5 277.0,180.1 278.2,179.7 279.5,179.3 280.7,178.9 282.0,178.5 283.3,178.1 284.5,177.7 285.8,177.2 287.0,176.8 288.3,176.4 289.5,176.0 290.8,175.6 292.1,175.2 293.3,174.8 294.6,174.4 295.8,174.0 297.1,173.6 298.3,173.2 299.6,172.8 300.9,172.4 302.1,172.0 303.4,171.6 304.6,171.2 305.9,170.8 307.1,170.4 308.4,170.0 309.7,169.6 310.9,169.2 312.2,168.8 313.4,168.4 314.7,168.0 315.9,167.6 317.2,167.2 318.5,166.8 319.7,166.4 321.0,165.9 322.2,165.5 323.5,165.1 324.7,164.7 326.0,164.3 327.3,163.9 328.5,163.5 329.8,163.1 331.0,162.7 332.3,162.3 333.5,161.9 334.8,161.5 336.1,161.1 337.3,160.7 338.6,160.3 339.8,159.9 341.1,159.5 342.3,159.1 343.6,158.7 344.9,158.3 346.1,157.9 347.4,157.5 348.6,157.1 349.9,156.7 351.1,156.3 352.4,155.9 353.7,155.5 354.9,155.1 356.2,154.6 357.4,154.2 358.7,153.8 359.9,153.4 361.2,153.0 362.5,152.6 363.7,152.2 365.0,151.8 366.2,151.4 367.5,151.0 368.7,150.6 370.0,150.2 371.3,149.8 372.5,149.4 373.8,149.0 375.0,148.6 376.3,148.2 377.5,147.8 378.8,147.4 380.1,147.0 381.3,146.6 382.6,146.2 383.8,145.8 385.1,145.4 386.3,145.0 387.6,144.6 388.9,144.2 390.1,143.8 391.4,143.3 392.6,142.9 393.9,142.5 395.1,142.1 396.4,141.7 397.7,141.3 398.9,140.9 400.2,140.5 401.4,140.1 402.7,139.7 403.9,139.3 405.2,138.9 406.5,138.5 407.7,138.1 409.0,137.7 410.2,137.3 411.5,136.9 412.7,136.5 414.0,136.1 415.3,135.7 416.5,135.3 417.8,134.9 419.0,134.5 420.3,134.1 421.5,133.7 422.8,133.3 424.1,132.9 425.3,132.5 426.6,132.0 427.8,131.6 429.1,131.2 430.3,130.8 431.6,130.4 432.9,130.0 434.1,129.6 435.4,129.2 436.6,128.8 437.9,128.4 439.1,128.0 440.4,127.6 441.7,127.2 442.9,126.8 444.2,126.4 445.4,126.0 446.7,125.6 447.9,125.2 449.2,124.8 450.5,124.4 451.7,124.0 453.0,123.6 454.2,123.2 455.5,122.8 456.7,122.4 458.0,122.0 459.3,121.6 460.5,121.2 461.8,120.7 463.0,120.3 464.3,119.9 465.5,119.5 466.8,119.1 468.1,118.7 469.3,118.3 470.6,117.9 471.8,117.5 473.1,117.1 474.3,116.7 475.6,116.3 476.9,115.9 478.1,115.5 479.4,115.1 480.6,114.7 481.9,114.3 483.1,113.9 484.4,113.5 485.7,113.1 486.9,112.7 488.2,112.3 489.4,111.9 490.7,111.5 491.9,111.1 493.2,110.7 494.5,110.3 495.7,109.9 497.0,109.4 498.2,109.0 499.5,108.6 500.7,108.2 502.0,107.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <line x1="102.2" y1="262" x2="102.2" y2="36" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4 3" opacity="0.7"/>
  <line x1="169.3" y1="262" x2="169.3" y2="36" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4 3" opacity="0.7"/>
  <circle cx="124.9" cy="228.9" r="3" fill="currentColor"/>
  <circle cx="124.9" cy="222.5" r="3" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="212.9" cy="200.7" r="3" fill="currentColor"/>
  <circle cx="212.9" cy="189.4" r="3" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="259.5" cy="185.7" r="3" fill="currentColor"/>
  <circle cx="259.5" cy="166.9" r="3" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="456.9" cy="122.3" r="3" fill="currentColor"/>
  <circle cx="456.9" cy="71.8" r="3" fill="currentColor" fill-opacity="0.5"/>
  <line x1="422" y1="44" x2="508" y2="44" stroke="currentColor" stroke-width="1.2" marker-end="url(#mr09dure)"/>
  <g font-size="11" fill="currentColor">
    <text x="62.0" y="278" text-anchor="middle" font-size="10">0</text>
    <text x="124.9" y="278" text-anchor="middle" font-size="10">0.5</text>
    <text x="187.7" y="278" text-anchor="middle" font-size="10">1</text>
    <text x="250.6" y="278" text-anchor="middle" font-size="10">1.5</text>
    <text x="313.4" y="278" text-anchor="middle" font-size="10">2</text>
    <text x="376.3" y="278" text-anchor="middle" font-size="10">2.5</text>
    <text x="439.1" y="278" text-anchor="middle" font-size="10">3</text>
    <text x="502.0" y="278" text-anchor="middle" font-size="10">3.5</text>
    <text x="55" y="266.0" text-anchor="end" font-size="10">0</text>
    <text x="55" y="233.7" text-anchor="end" font-size="10">1</text>
    <text x="55" y="201.4" text-anchor="end" font-size="10">2</text>
    <text x="55" y="169.1" text-anchor="end" font-size="10">3</text>
    <text x="55" y="136.9" text-anchor="end" font-size="10">4</text>
    <text x="55" y="104.6" text-anchor="end" font-size="10">5</text>
    <text x="55" y="72.3" text-anchor="end" font-size="10">6</text>
    <text x="55" y="40.0" text-anchor="end" font-size="10">7</text>
    <text x="282.0" y="294" text-anchor="middle">move size Δθ (rad)</text>
    <text x="8" y="20">duration (s)</text>
    <text x="414.0" y="152.1" text-anchor="middle">trapezoid</text>
    <text x="388.9" y="96.6" text-anchor="end" opacity="0.8">fastest cubic</text>
    <text x="102.2" y="30" text-anchor="middle" font-size="10">Δθ* = 0.32</text>
    <text x="169.3" y="30" text-anchor="middle" font-size="10">Δθ† = 0.853</text>
    <text x="135.8" y="104" text-anchor="middle" font-size="10" opacity="0.8">cubic:</text>
    <text x="135.8" y="117" text-anchor="middle" font-size="10" opacity="0.8">acceleration</text>
    <text x="135.8" y="130" text-anchor="middle" font-size="10" opacity="0.8">binds</text>
    <text x="175.3" y="110" font-size="10" opacity="0.8">cubic: velocity binds</text>
    <text x="418" y="48" text-anchor="end" font-size="10">new drive, Δθ† = 13.65 →</text>
    <text x="330" y="200" font-size="10" opacity="0.8">Δθ (rad)</text><text x="392" y="200" font-size="10" opacity="0.8">trapezoid</text><text x="452" y="200" font-size="10" opacity="0.8">cubic</text>
    <text x="330" y="215" font-size="10">0.5</text><text x="392" y="215" font-size="10">1.025 s</text><text x="452" y="215" font-size="10">1.225 s, a binds</text>
    <text x="330" y="229" font-size="10">1.2</text><text x="392" y="229" font-size="10">1.900 s</text><text x="452" y="229" font-size="10">2.250 s, v binds</text>
    <text x="330" y="243" font-size="10">π/2</text><text x="392" y="243" font-size="10">2.363 s</text><text x="452" y="243" font-size="10">2.945 s, v binds</text>
    <text x="330" y="257" font-size="10">π</text><text x="392" y="257" font-size="10">4.327 s</text><text x="452" y="257" font-size="10">5.890 s, v binds</text>
  </g>
</svg>

Duration against move size for one joint at P2's frozen limits, $0.8\,\mathrm{rad/s}$ and $2\,\mathrm{rad/s^2}$: the trapezoid (dark) and the fastest legal cubic (light), which is the larger of its two floors $T_v = 1.5\Delta\theta/v_{\max}$ and $T_a = \sqrt{6\Delta\theta/a_{\max}}$ (dotted). Below $\Delta\theta^* = 0.32\,\mathrm{rad}$ the trapezoid loses its cruise and becomes a triangle; below $\Delta\theta^\dagger = 0.853\,\mathrm{rad}$ (shaded) the cubic is acceleration-bound, above it velocity-bound, and the table lists the page's four moves. The problem set's faster, weaker drive moves $\Delta\theta^\dagger$ to $13.65\,\mathrm{rad}$, off the chart.

### 1. The chapter in one list

A planner hands over a path with no clock, and the motors need a clock that keeps them inside two limits. This section is the chapter's toolbox for adding one — polynomial scalings, via points, the time-optimal scaling — and §2–§3 define the two objects the worked case used; path, trajectory and time scaling are defined together in §2.

*In one sentence:* a trajectory is a path plus a time scaling, the cubic and quintic are the polynomial scalings fixed by their end conditions, and the fastest scaling under actuator limits rides those limits the whole way.

- **Point-to-point time scalings**: cubic ($s = 3t^2/T^2 - 2t^3/T^3$: zero endpoint
  velocities) and quintic (zero endpoint accelerations too — smoother torques);
  **trapezoidal** velocity profiles (accelerate–cruise–decelerate) — what industrial
  controllers actually run.
  - The quintic's numbers, derived: with $u = t/T$ it is $s = 10u^3 - 15u^4 + 6u^5$, the one quintic with $s$, $\dot s$ and $\ddot s$ fixed at both ends ($0, 0, 0$ and $1, 0, 0$). Then $\dot s = (30/T)\,u^2(1-u)^2$ peaks at $u = \tfrac12$ at $30/16 = 1.875/T$, and $\ddot s = (60/T^2)\,u(1-u)(1-2u)$ peaks where $1 - 6u + 6u^2 = 0$, at $u = \tfrac12 - \sqrt3/6 = 0.2113$, with value $(10/\sqrt3)/T^2 = 5.77/T^2$. Those are the two coefficients the worked example below uses.

> **Cubic and quintic time scalings, defined.** A **polynomial time scaling** is *a time scaling (§2) that is a polynomial in $t$*, with one coefficient per boundary condition it meets (MR §9.2.2.1). The **cubic** meets four: the **endpoints**, $s(0) = 0$ and $s(T) = 1$, and **rest at both ends**, $\dot s(0) = \dot s(T) = 0$. The **quintic** meets six: those four and **zero acceleration at both ends**, $\ddot s(0) = \ddot s(T) = 0$.
>
> $$s_3 = 3u^2 - 2u^3, \qquad s_5 = 10u^3 - 15u^4 + 6u^5, \qquad u = t/T$$
>
> where $u$ is normalized time, which is why $T$ only stretches a fixed shape; the coefficients come from the boundary conditions, one equation each, and the peaks are $\dot s = 1.5/T$ and $|\ddot s| = 6/T^2$ for the cubic, $1.875/T$ and $5.77/T^2$ for the quintic.
>
> - **Example**: the elbow flip. The cubic needs $T = 5.890\,\mathrm{s}$; the quintic, peaking higher in speed, needs $1.875\pi/0.8 = 7.363\,\mathrm{s}$. Both are velocity-bound.
> - **Non-example**: $s = t/T$, linear interpolation. It meets the endpoints but not rest: at $T = \pi/0.8 = 3.927\,\mathrm{s}$ the elbow jumps from $0$ to $0.8\,\mathrm{rad/s}$ at $t = 0$, an infinite acceleration. The cubic removes that jump but keeps one in acceleration, $0.543\,\mathrm{rad/s^2}$ at $t = 0$: an infinite jerk (jerk is the rate of change of acceleration), which MR warns can set the robot vibrating, and the jump the quintic removes.

- **Via points**: a path through intermediate configurations. ch.10's legal version of the elbow flip goes through $E = (135°,\ -45°)$; timed leg by leg, each leg rest to rest, it takes $(3\pi/4)/0.8 + 0.4 = 3.345\,\mathrm{s}$ to $E$ and $(\pi/4)/0.8 + 0.4 = 1.382\,\mathrm{s}$ on to the goal, $4.727\,\mathrm{s}$ in all against the direct flip's $4.327\,\mathrm{s}$ — the price of not going through the panel. A spline through $E$ — a chain of polynomials joined smoothly at the via points — that does not stop there is faster, but a spline through close via points can overshoot between them, so its peaks must be checked against the limits like any other scaling; [[04-robotics/capstone-panel-contact|26. Capstone]] step 3 times its own legs rest to rest.
- **Time-optimal time scaling**: given actuator limits and the
  [[04-robotics/modern-robotics/ch08-dynamics|dynamics]], find the fastest $s(t)$ along a
  fixed path — an [[02-foundations/optimization|optimization]] problem with a classic
  bang-bang structure (at every instant the path acceleration sits at its maximum or its
  minimum, never in between — typically full acceleration, then a switch to full deceleration).
  - With constant limits on one joint the structure takes two lines to see. A move that starts and ends at rest has $|\dot\theta(t)| \le \min(a_{\max}t,\ v_{\max},\ a_{\max}(T - t))$ at every instant, so the distance it can cover in time $T$ is at most the area under that bound — which is exactly the trapezoid of the worked case, reached only by full acceleration, cruise at the limit, full deceleration. So the elbow flip's $4.327\,\mathrm{s}$ cannot be beaten under these limits; drop the speed limit and the bound becomes a triangle, the pure bang-bang flip taking $2\sqrt{\pi/2} = 2.507\,\mathrm{s}$. The note below states the general problem, where the limits vary along the path.

> [!note]- Deeper · 더 깊이
> **Time-optimal time scaling, defined.** A **time-optimal time scaling** is *the solution of a minimization*: of all time scalings of one path, the one that finishes first (MR §9.4). Three conditions pose it. The **path is fixed**, so only $s(t)$ is chosen. The motion is **rest to rest and monotone**: $s(0) = \dot s(0) = \dot s(T) = 0$, $s(T) = 1$, $\dot s \ge 0$. And the **actuator limits hold at every instant**: torque (acceleration) limits become bounds on the path acceleration, $L(s,\dot s) \le \ddot s \le U(s,\dot s)$, which MR derives through the dynamics, and velocity limits bound the path speed, $\dot s \le \dot s_{\max}(s)$.
>
> $$T = \int_0^1 \frac{ds}{\dot s(s)} \ \to\ \min \quad \text{subject to} \quad L(s,\dot s) \le \ddot s \le U(s,\dot s),\ \ 0 \le \dot s \le \dot s_{\max}(s)$$
>
> where $\dot s(s)$ is the path speed at each point of the path and $\dot s_{\max}(s)$ its bound (in MR's torque-only setting, the velocity limit curve where $L = U$); the objective has this shape because time is the integral of $1/\dot s$, so the optimum keeps $\dot s$ as high as these bounds allow everywhere (MR, after eq. 9.39). On the elbow flip this page's limits give $|\ddot s| \le 2/\pi = 0.637\,\mathrm{1/s^2}$ and $\dot s \le 0.8/\pi = 0.255\,\mathrm{1/s}$, and the speed bound is what puts a cruise in the optimum.
>
> - **Example**: the elbow flip's $4.327\,\mathrm{s}$ trapezoid; with no speed limit, the bang-bang triangle's $2.507\,\mathrm{s}$.
> - **Non-example**: the cubic at its limit, $5.890\,\mathrm{s}$: the fastest *cubic*, a best $T$ for one fixed shape, and $1.361$ times the optimum. "Time-optimal" must name its limits: under MR's torque limits $L$ and $U$ change along the path, and the trapezoid is in general no longer optimal.

> [!example] Worked example · 계산 예제
> One joint moves $\Delta\theta = 1.2$ rad in $T = 2$ s. Scale the unit-move peaks by $\Delta\theta$:
> - **Cubic**: peak velocity $1.5 \cdot 1.2/2 = 0.9$ rad/s; peak acceleration $6 \cdot 1.2/2^2 = 1.8$ rad/s².
> - **Quintic**: peak velocity $1.875 \cdot 1.2/2 = 1.125$ rad/s; peak acceleration $5.77 \cdot 1.2/2^2 \approx 1.73$ rad/s².
>
> Now suppose the actuator allows $v_{\max} = 0.8$ rad/s and $a_{\max} = 2$ rad/s², and run a **trapezoidal** profile instead:
> - Accelerate: $v_{\max}/a_{\max} = 0.4$ s, covering $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16$ rad. Decelerate: the same 0.4 s and 0.16 rad.
> - Cruise: the remaining $1.2 - 0.32 = 0.88$ rad at 0.8 rad/s takes $1.1$ s.
> - Total: $0.4 + 1.1 + 0.4 = 1.9$ s — faster than the 2 s polynomial moves.
>
> **Which limit binds**: velocity. Both polynomials stay under $a_{\max}$ (1.8 and 1.73 < 2) but exceed $v_{\max}$ (0.9 and 1.125 > 0.8), so at $T = 2$ s neither is executable on this joint; the trapezoid saturates $v_{\max}$ by construction.
>
> The claim of infeasibility *is* $0.9>0.8$. And a timing, however legal, says nothing about how hard the tool presses once it touches the panel; that is [[04-robotics/contact-force-tactile|9. Contact]]'s question.

### 2. Time scaling, defined

Because the timing is a separate object, an actuator-limit question ("can this motor do it?") never touches the geometry, and a clearance question ("does this path hit the panel?") never touches the timing; mixing them is how a planner gets blamed for a motor's limits. That separation rests on three definitions, path, trajectory and time scaling.

- **Path vs trajectory**: a path is geometry $\theta(s), s\in[0,1]$; a trajectory adds
  **time scaling** $s(t)$ — MR's clean separation that lets you design shape and timing
  independently.

> **Path and trajectory, defined.** A **path** is *a map from a parameter to configurations*, $\theta: [0,1] \to \mathcal{C}$, with $\theta(0)$ the start and $\theta(1)$ the goal: geometry with no time in it. A **trajectory** is *a map from time to configurations* with exactly two parts, a path and a time scaling $s: [0,T] \to [0,1]$ (below), composed (MR §9.1).
>
> $$\theta(t) = \theta\big(s(t)\big), \qquad \theta(s) = \theta^{\text{start}} + s\,\big(\theta^{\text{goal}} - \theta^{\text{start}}\big),\ \ s \in [0, 1]$$
>
> where the second formula is the straight line in joint space that this page times; because the two parts meet only in the composition, each can be changed without touching the other.
>
> - **Example**: the elbow flip passes $\theta(0.5) = (45°,\ 0°)$ whatever the timing: the trapezoid gets there at $t = 2.163\,\mathrm{s}$, the cubic at $2.945\,\mathrm{s}$ — one path, two trajectories.
> - **Non-example**: that straight line read as the tip's path. It is straight in joint space only: the tip starts and ends at $(1,1)$ yet passes $(1.414,\ 1.414)$ at $s = 0.5$, $0.414\,\mathrm{m}$ inside the panel. A path is a curve in C-space, so what the tool does along it must be checked in the workspace, as the Running object's warning says.

A **time scaling** is a *function* $s: [0,T] \to [0,1]$, not a path and not a trajectory. It has three defining conditions, and dropping any one of them breaks something specific:

- **Endpoints**: $s(0) = 0$ and $s(T) = 1$, so the move starts at the start and finishes at the goal.
- **Monotonicity**: $\dot s(t) \ge 0$, so the robot never retraces the path. A scaling that dips backwards is a different path, not a different timing.
- **Smoothness to the order the hardware needs**: at least $C^1$ — one continuous derivative — so velocity is continuous; $C^2$, two continuous derivatives, if torque must be continuous, because the commanded torque is $\tau = M(\theta)\ddot\theta + c + g$ of [[04-robotics/modern-robotics/ch08-dynamics|ch.8]] and $c$ and $g$ vary smoothly with the state, so a jump in $\ddot\theta$ is a jump in $\tau$: a torque spike that can set the arm vibrating ([[02-foundations/signal-processing|signal processing]]'s frequency lens applies).

The trajectory is then the composition $\theta(t) = \theta(s(t))$, and differentiating it once and twice gives the two identities every calculation on this page uses:

$$\dot\theta(t) = \frac{d\theta}{ds}\,\dot s, \qquad \ddot\theta(t) = \frac{d\theta}{ds}\,\ddot s + \frac{d^2\theta}{ds^2}\,\dot s^2$$

where the second term vanishes for a straight-line path in joint space, because $d^2\theta/ds^2 = 0$ there, which is why P2's elbow flip reduces to $\ddot\theta_i = \Delta\theta_i\,\ddot s$.

- **Example**: the cubic $s = 3t^2/T^2 - 2t^3/T^3$. Check the conditions: $s(0)=0$, $s(T)=1$, $\dot s = 6t/T^2 - 6t^2/T^3 = (6t/T^2)(1 - t/T) \ge 0$ on $[0,T]$, and $\dot s(0) = \dot s(T) = 0$. On the elbow flip with $T = 5.8905\,\mathrm{s}$ it reaches $s = 0.5$ at $t = 2.945\,\mathrm{s}$, with the elbow at $0°$ moving at its peak, $\pi \cdot 1.5/5.8905 = 0.8\,\mathrm{rad/s}$.
- **Non-example**: $s(t) = \sin(2\pi t/T)$. It is smooth and it starts at $0$, but it is not monotone and $s(T) = 0 \neq 1$ — it returns to the start, so it is not a point-to-point scaling at all.

### 3. The trapezoidal profile, defined

A datasheet gives two numbers, a top speed and an acceleration, and the trapezoid is the time scaling whose two parameters are exactly those: set them at the limits and nothing needs solving. That is why industrial controllers run it, and why it is the baseline any fancier scaling has to beat.

A **trapezoidal velocity profile** is the rest-to-rest time scaling whose *velocity* $\dot s$ is piecewise linear with three phases — constant acceleration, constant velocity, constant deceleration of the same size (MR §9.2.2.2). Its two free parameters are the cruise speed and the ramp acceleration, and this page sets them at the actuator limits, so the elbow ramps at $\pm a_{\max}$ and cruises at $v_{\max}$, attaining both limits rather than approaching them — the choice MR identifies as the fastest straight-line motion those limits allow, and §1's area argument shows why. Applied to a joint move of size $\Delta\theta$, its duration is

$$T_{\text{trap}} = \frac{\Delta\theta}{v_{\max}} + \frac{v_{\max}}{a_{\max}} \qquad \text{when } \Delta\theta \ge \frac{v_{\max}^2}{a_{\max}}$$

because the cruise covers $\Delta\theta - v_{\max}^2/a_{\max}$ at speed $v_{\max}$ while the two ramps take $v_{\max}/a_{\max}$ between them. Check it on the elbow: $3.1416/0.8 + 0.8/2 = 3.9270 + 0.4 = 4.327\,\mathrm{s}$, the number derived the long way above.

- **Example**: P2's elbow flip, $T_{\text{trap}} = 4.327\,\mathrm{s}$ with an $81.5\,\%$ cruise.
- **Degenerate case, not a non-example**: when $\Delta\theta < v_{\max}^2/a_{\max}$ the cruise phase has negative length, the profile collapses to a **triangle**, and the duration is $T_{\text{tri}} = 2\sqrt{\Delta\theta/a_{\max}}$ with a peak velocity $a_{\max}T/2$ that never reaches $v_{\max}$. Using the trapezoid formula there returns a *longer* time than the triangle takes, which is the standard way this calculation is got wrong.
- **Non-example**: a trapezoid for each joint, each at its own limits. The shoulder's alone would finish in $2.363\,\mathrm{s}$, when the elbow, on its $4.327\,\mathrm{s}$ profile, is still $1.411\,\mathrm{rad}$ from its goal: the joints no longer share one $s(t)$, so the arm leaves the straight joint-space path, and a clearance check made on that path no longer covers the motion.
- **Same shape, not the fastest**: the page's profile with its top lowered to $0.6\,v_{\max} = 0.48\,\mathrm{rad/s}$ is still trapezoidal, but it takes $3.1416/0.48 + 0.48/2 = 6.785\,\mathrm{s}$, longer than the cubic's $5.890\,\mathrm{s}$: the speed comes from saturating both limits, not from the silhouette.
- **Joint limits, not tip limits**: both of its numbers are joint limits, so a trapezoid that saturates them can still drive the tip past a task-space speed limit, which [[04-robotics/capstone-panel-contact|26. Capstone §3]] catches and repairs with a tip-speed cap.

**Wiki connections**: [[01-canonical-papers/notes/4-vla/act|action chunks]] and
[[01-canonical-papers/notes/4-vla/diffusion-policy|denoised trajectories]] are *learned*
replacements for exactly this chapter; classical time scaling still wraps learned outputs
on real hardware for safety/limits.

### Self-check

1. For the cubic scaling $s(t) = 3t^2/T^2 - 2t^3/T^3$, compute $s(0), s(T), \dot s(0), \dot s(T)$ and confirm the boundary conditions.
2. What does quintic scaling buy over cubic, and what does it cost?
3. Why is the trapezoidal velocity profile the industrial default?
4. One joint of P2 moves $\Delta\theta = 0.5\,\mathrm{rad}$ under this page's frozen limits. Does the trapezoid keep a cruise, which limit binds the fastest cubic, and what are the two durations?

> [!tip]- Answers
> 1. $s(0)=0$, $s(T)=1$; $\dot s = 6t/T^2 - 6t^2/T^3$, so $\dot s(0) = \dot s(T) = 0$ — it starts and ends at rest, which is exactly the point-to-point requirement.
> 2. Quintic also zeroes the endpoint *accelerations*, so torque is continuous at the ends (no jolt). The cost is a higher peak velocity for the same duration ($1.875/T$ vs $1.5/T$) — note the peak *acceleration* is actually lower than cubic's ($5.77/T^2$ vs $6/T^2$), so it is speed, not torque, that you pay.
> 3. Its parameters can be set directly to the actuator limits: maximum velocity and maximum acceleration appear directly in the profile, so a machine spec maps onto it one-to-one without solving anything.
> 4. $0.5 > \Delta\theta^{*} = 0.32$, so the trapezoid keeps a short cruise: $T_{\text{trap}} = 0.5/0.8 + 0.4 = 0.625 + 0.4 = 1.025\,\mathrm{s}$, with $0.225\,\mathrm{s}$ at $v_{\max}$. But $0.5 < \Delta\theta^{\dagger} = 0.853$, so the cubic is acceleration-bound: $T_a = \sqrt{6 \cdot 0.5/2} = \sqrt{1.5} = 1.225\,\mathrm{s}$ against $T_v = 1.5 \cdot 0.5/0.8 = 0.9375\,\mathrm{s}$, and at $1.225\,\mathrm{s}$ its peak speed is only $1.5 \cdot 0.5/1.225 = 0.612\,\mathrm{rad/s}$. The cubic now touches the acceleration line and never the velocity line — the one regime the worked case never shows — and takes $1.195$ times the trapezoid's time.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same plant **P2** and the same elbow flip, $|\Delta\theta_2| = \pi\,\mathrm{rad}$, but the elbow gets a different drive, faster and weaker, whose planning specification is $v_{\max} = 1.6\,\mathrm{rad/s}$ and $a_{\max} = 0.5\,\mathrm{rad/s^2}$: twice the top speed and a quarter of the acceleration.

1. **Draw.** The picture above, for the elbow under the new limits. Before drawing, decide which of the two dashed lines each profile touches now — the shapes change, and one of them loses a phase entirely.
2. **Derive.** (a) The trapezoid: evaluate $v_{\max}^2/a_{\max}$ first and say what kind of profile results, then give its duration and its peak velocity. (b) The cubic: compute $T_v$ and $T_a$, state $T_{\text{cubic}}$ and which limit binds. (c) The ratio $T_{\text{cubic}}/T_{\text{trap}}$, and show that under these conditions the ratio does not depend on $\Delta\theta$ or on $a_{\max}$ at all.
3. **Interpret.** The new drive doubled the top speed and cut the acceleration to a quarter. Did the elbow flip get faster or slower, and by how much against the frozen-limit numbers? Which of the two limits is worth buying, and what does the crossover $\Delta\theta^{\dagger}$ say about when that answer flips?

> [!note]- How to draw it · 그리는 법
> - Three stacked panels sharing one time axis, the elbow only: the angle $\theta_2(t)$ on top, the speed $|\dot\theta_2|$ in the middle, and its rate of change $d|\dot\theta_2|/dt$ at the bottom.
> - Draw the limits first, as horizontal dashed lines at the values in force: $v_{\max}$ in the middle panel, $\pm a_{\max}$ in the bottom one.
> - Top: both curves run from $90°$ down to $-90°$. The trapezoid's is straight in the middle and parabolic at the ends, the cubic's is an S-curve; mark where each one arrives.
> - Middle: the trapezoid ramps up, runs flat on the $v_{\max}$ line, and ramps down — and if the move ends before the ramps reach $v_{\max}$, there is no flat top. The cubic is a single parabola peaking at its midpoint.
> - Bottom: the trapezoid is rectangles at $+a_{\max}$ and $-a_{\max}$ with zero between; the cubic is one straight line falling through zero. Write each profile's peak beside it.
> - Shade any stretch a profile spends on a limit and label its duration (in the picture above, $3.527\,\mathrm{s}$ at $v_{\max}$).
> - Check: each profile, timed as fast as its limits allow, touches at least one dashed line — which one is the whole message of the figure.

> [!tip]- Solutions
> 1. Velocity: the trapezoid's flat top disappears, so the middle panel shows a triangle peaking at $1.2533\,\mathrm{rad/s}$, below the new $v_{\max}$ dashed line at $1.6$. Acceleration: both profiles now press against the $a_{\max}$ line — the triangle touches it over both halves, and the cubic touches it at the two endpoints.
> 2. (a) $v_{\max}^2/a_{\max} = 2.56/0.5 = 5.12\,\mathrm{rad} > \pi$, so the move is too short to reach top speed and the profile is a **triangle**: $T_{\text{tri}} = 2\sqrt{\pi/0.5} = 2 \times 2.5066 = 5.013\,\mathrm{s}$, peak velocity $a_{\max}T/2 = 0.5 \times 2.5066 = 1.2533\,\mathrm{rad/s}$, comfortably under $1.6$. (b) $T_v = 1.5\pi/1.6 = 2.945\,\mathrm{s}$, $T_a = \sqrt{6\pi/0.5} = 6.140\,\mathrm{s}$, so $T_{\text{cubic}} = 6.140\,\mathrm{s}$ and **acceleration** binds — the limit has swapped. (c) $6.140/5.013 = 1.2247$. When both profiles are acceleration-bound the durations are $2\sqrt{\Delta\theta/a_{\max}}$ and $\sqrt{6\Delta\theta/a_{\max}}$, whose ratio is $\sqrt{6}/2 = \sqrt{3/2} = 1.2247$ with $\Delta\theta$ and $a_{\max}$ cancelling.
> 3. Slower, in both cases: $5.013$ against $4.327\,\mathrm{s}$ for the trapezoid ($+15.9\,\%$) and $6.140$ against $5.890\,\mathrm{s}$ for the cubic ($+4.2\,\%$). Buying top speed was worthless here because the move never reaches it; the acceleration is what was worth keeping. The crossover says when: $\Delta\theta^{\dagger} = \tfrac83 v_{\max}^2/a_{\max}$ rises from $0.853$ to $13.65\,\mathrm{rad}$, so under the new drive every move shorter than $13.65\,\mathrm{rad}$ is acceleration-bound. Top speed only starts paying above that, and P2's joints never travel that far in one move.

## 한국어

**핵심 질문**: "A에서 B로 가라"를 매끄럽고 실행 가능한 시간 함수로 어떻게 바꾸는가?

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 장은 모션·과제 계획 층이 조작 층에 일을 넘기는 자리다. "*저 패널을 프레임에 설치해*"에서는 *부재를 옮기는* 단계를 받친다. 경로는 시간을 입혀야 비로소 모터가 따를 수 있는 명령이 되기 때문이다. 이 페이지의 칩은 [[physical-ai-map|피지컬 AI 지도]]의 계획 띠에 있다. 시간을 아무렇게나 입히면 이동은 불법이 되거나 느려진다. 사다리꼴의 $4.327\,\mathrm{s}$에 3차를 억지로 넣으면 카탈로그의 평면 2링크 팔 **P2**([[02-foundations/lab-plants|0.6]])의 엘보에 한계 $0.8\,\mathrm{rad/s}$를 넘는 $1.089\,\mathrm{rad/s}$를 요구하고, 합법적인 가장 빠른 3차는 $36\,\%$ 더 긴 $5.890\,\mathrm{s}$가 걸린다('대상으로 한 번 끝까지' B–C). 뒤 페이지들이 이 위에 선다. [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]은 경로를 공급하고 이 페이지의 직선 경로가 패널 안으로 $0.414\,\mathrm{m}$ 들어감을 보이며, [[04-robotics/actuators-drives|10.5 액추에이터·구동계 §3]]은 $v_{\max}$와 $a_{\max}$가 어디서 오는지 말하고, [[04-robotics/capstone-panel-contact|26. 캡스톤 §3]]은 같은 사다리꼴을 말단 속도로 제한하며, [[04-robotics/ros2/manipulation-moveit2|25.8 MoveIt 2 §1]]은 같은 방식으로 계획에 시간을 입힌다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 2, 로보틱스 22–24회차다. 이 페이지를 마치면 어떤 관절 이동이든 사다리꼴이나 다항식으로 시간을 입히고, 계산 전에 어느 한계가 걸릴지 말하며, 구동계를 바꾸면 시간이 어떻게 되는지 예측할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 세 번쯤, 로보틱스 22–24회차다. **첫 회차:** 경고가 붙은 이 페이지의 대상, 그림, 그리고 '대상으로 한 번 끝까지' 전체. 엘보 뒤집기의 사다리꼴(A)과 3차(B), 둘의 비교(C), 어느 한계가 걸릴지 미리 말해 주는 교차점 $\Delta\theta^\dagger$(D)와 그 그림이다. 끝으로 스스로 점검 4번을 손으로 푼다. 3차가 가속도 구속이 되는 유일한 경우인 $0.5\,\mathrm{rad}$ 이동이다. **둘째 회차:** §1–§3. 계산 예제가 있는 이 장의 목록, 함께 정의하는 경로·궤적·시간 스케일링, 그리고 사다리꼴. **셋째 회차:** 스스로 점검과 과제. 일반적인 시간 최적 문제를 다룬 접힌 *더 깊이* 메모는 두 번째 읽기다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 카탈로그의 평면 2링크 팔, 그리고 그 위의 이름 붙은 이동 하나. 말단을 패널 목표 $(1,1)$에 두는 두 컨피규레이션 사이의 **엘보 뒤집기**이며, 두 컨피규레이션은 [[04-robotics/modern-robotics/ch02-configuration-space|2장]]에서 유도했고 6장의 IK 가지 둘이다.

$$\theta^{\text{start}} = (0°,\ 90°) \ \longrightarrow\ \theta^{\text{goal}} = (90°,\ -90°), \qquad \Delta\theta_1 = +\tfrac{\pi}{2} = 1.5708\ \mathrm{rad}, \quad \Delta\theta_2 = -\pi = -3.1416\ \mathrm{rad}$$

이므로 엘보가 어깨보다 정확히 두 배 멀리 간다. 어깨가 4분의 1바퀴 도는 동안 엘보는 $+90°$에서 $-90°$까지 휘돌기 때문이고, 이 페이지 전체가 이 사실에 달려 있다. **경로**는 관절 공간의 두 점을 잇는 직선 $\theta(s) = \theta^{\text{start}} + s\,\Delta\theta$, $s \in [0,1]$이고, 이 페이지는 $s(t)$만 고른다.

**여기서 고정하는 액추에이터 한계.** 0.6은 P2의 구동계를 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]에 고정해 두었고, 그 관절은 무부하로 최대 $2.4\,\mathrm{rad/s}$까지 돈다. 아래 두 숫자는 그 구동계가 할 수 있는 범위 안쪽에 넉넉히 머무는 계획 사양이고, 이 페이지는 이것을 바꾸지 않는다. 그래서 P2의 모든 관절은

$$|\dot\theta_i| \le v_{\max} = 0.8\ \mathrm{rad/s}, \qquad |\ddot\theta_i| \le a_{\max} = 2\ \mathrm{rad/s^2}$$

를 지킨다. §1의 계산 예제가 쓰는 그 두 숫자를 이제 장치에 붙인 것이다.

> [!warning] 시간 스케일링은 충돌 검사가 아니다 · A time scaling is not a collision check
> 이 직선 관절 경로는 2장의 패널, 곧 반평면 $x \ge 1$에 대해 충돌이 없지 *않다*. 양 끝은 면 $x = 1$에 닿기만 하고 이 위키는 그것을 자유로 치지만, 중간점 $(45°,\ 0°)$에서는 팔이 곧게 펴져 말단이 $(1.414,\ 1.414)$, 곧 면에서 $\sqrt2 - 1 = 0.414\,\mathrm{m}$ 지나친 자리에 있다. [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]이 간선 검사로 이것을 찾아내고 돌아가는 길을 계획한다. 경로에 시간을 입히는 것과 경로에 충돌이 없는지 확인하는 것은 다른 질문이고, 이 장은 앞의 것만 답한다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 363" style="max-width:100%;height:auto" role="img" aria-label="P2의 엘보 뒤집기를 0~6 s 위 세 단으로: 엘보 각, 0.8 rad/s 한계에 대한 엘보 속력, 2 rad/s² 한계에 대한 속력 변화율. 사다리꼴(4.327 s)과 3차(5.890 s)">
  <g transform="translate(0 3)">
    <g stroke="currentColor" stroke-width="1" opacity="0.55"><line x1="80" y1="26" x2="80" y2="102"/><line x1="80" y1="98" x2="534" y2="98"/><line x1="80" y1="128.4" x2="80" y2="204"/><line x1="80" y1="204" x2="534" y2="204"/><line x1="80" y1="247.7" x2="80" y2="316.3"/><line x1="80" y1="282" x2="534" y2="282"/><line x1="80" y1="316.3" x2="534" y2="316.3"/></g>
    <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="76" y1="30" x2="80" y2="30"/><line x1="76" y1="64" x2="80" y2="64"/><line x1="76" y1="98" x2="80" y2="98"/><line x1="76" y1="175.2" x2="80" y2="175.2"/><line x1="76" y1="146.4" x2="80" y2="146.4"/><line x1="76" y1="254" x2="80" y2="254"/><line x1="76" y1="310" x2="80" y2="310"/><line x1="80" y1="316.3" x2="80" y2="320.3"/><line x1="155.7" y1="316.3" x2="155.7" y2="320.3"/><line x1="231.3" y1="316.3" x2="231.3" y2="320.3"/><line x1="307" y1="316.3" x2="307" y2="320.3"/><line x1="382.7" y1="316.3" x2="382.7" y2="320.3"/><line x1="458.3" y1="316.3" x2="458.3" y2="320.3"/><line x1="534" y1="316.3" x2="534" y2="320.3"/></g>
    <line x1="80" y1="64" x2="534" y2="64" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
    <g stroke="currentColor" stroke-width="0.9" stroke-dasharray="1.5 3" opacity="0.5"><line x1="407.4" y1="30" x2="407.4" y2="316.3"/><line x1="525.7" y1="30" x2="525.7" y2="316.3"/></g>
    <path d="M80 30 L82.9 30 L85.7 30 L88.6 30.1 L91.4 30.1 L94.3 30.2 L97.1 30.3 L100 30.4 L102.8 30.5 L105.7 30.7 L108.6 30.8 L111.4 31 L114.3 31.1 L117.1 31.3 L120 31.5 L122.8 31.8 L125.7 32 L128.5 32.2 L131.4 32.5 L134.3 32.8 L137.1 33.1 L140 33.4 L142.8 33.7 L145.7 34 L148.5 34.3 L151.4 34.7 L154.2 35 L157.1 35.4 L159.9 35.8 L162.8 36.2 L165.7 36.6 L168.5 37 L171.4 37.4 L174.2 37.8 L177.1 38.3 L179.9 38.7 L182.8 39.2 L185.6 39.7 L188.5 40.1 L191.4 40.6 L194.2 41.1 L197.1 41.6 L199.9 42.1 L202.8 42.6 L205.6 43.2 L208.5 43.7 L211.3 44.2 L214.2 44.8 L217.1 45.3 L219.9 45.9 L222.8 46.5 L225.6 47 L228.5 47.6 L231.3 48.2 L234.2 48.8 L237 49.4 L239.9 50 L242.8 50.6 L245.6 51.2 L248.5 51.8 L251.3 52.4 L254.2 53 L257 53.7 L259.9 54.3 L262.7 54.9 L265.6 55.6 L268.5 56.2 L271.3 56.8 L274.2 57.5 L277 58.1 L279.9 58.8 L282.7 59.4 L285.6 60.1 L288.4 60.7 L291.3 61.4 L294.2 62 L297 62.7 L299.9 63.3 L302.7 64 L305.6 64.6 L308.4 65.3 L311.3 65.9 L314.1 66.6 L317 67.2 L319.8 67.9 L322.7 68.5 L325.6 69.2 L328.4 69.8 L331.3 70.5 L334.1 71.1 L337 71.7 L339.8 72.4 L342.7 73 L345.5 73.7 L348.4 74.3 L351.3 74.9 L354.1 75.5 L357 76.1 L359.8 76.8 L362.7 77.4 L365.5 78 L368.4 78.6 L371.2 79.2 L374.1 79.7 L377 80.3 L379.8 80.9 L382.7 81.5 L385.5 82.1 L388.4 82.6 L391.2 83.2 L394.1 83.7 L396.9 84.3 L399.8 84.8 L402.7 85.3 L405.5 85.8 L408.4 86.3 L411.2 86.8 L414.1 87.3 L416.9 87.8 L419.8 88.3 L422.6 88.8 L425.5 89.2 L428.4 89.7 L431.2 90.1 L434.1 90.6 L436.9 91 L439.8 91.4 L442.6 91.8 L445.5 92.2 L448.3 92.6 L451.2 92.9 L454.1 93.3 L456.9 93.6 L459.8 94 L462.6 94.3 L465.5 94.6 L468.3 94.9 L471.2 95.2 L474 95.5 L476.9 95.7 L479.7 96 L482.6 96.2 L485.5 96.4 L488.3 96.6 L491.2 96.8 L494 97 L496.9 97.2 L499.7 97.3 L502.6 97.5 L505.4 97.6 L508.3 97.7 L511.2 97.8 L514 97.9 L516.9 97.9 L519.7 98 L522.6 98 L525.4 98 L528.3 98 L531.1 98 L534 98" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <path d="M80 30 L82.9 30 L85.7 30.1 L88.6 30.3 L91.4 30.5 L94.3 30.8 L97.1 31.1 L100 31.5 L102.8 32 L105.7 32.5 L108.6 33.1 L111.4 33.7 L114.3 34.4 L117.1 35 L120 35.7 L122.8 36.3 L125.7 37 L128.5 37.6 L131.4 38.3 L134.3 39 L137.1 39.6 L140 40.3 L142.8 40.9 L145.7 41.6 L148.5 42.2 L151.4 42.9 L154.2 43.5 L157.1 44.2 L159.9 44.8 L162.8 45.5 L165.7 46.1 L168.5 46.8 L171.4 47.4 L174.2 48.1 L177.1 48.8 L179.9 49.4 L182.8 50.1 L185.6 50.7 L188.5 51.4 L191.4 52 L194.2 52.7 L197.1 53.3 L199.9 54 L202.8 54.6 L205.6 55.3 L208.5 55.9 L211.3 56.6 L214.2 57.2 L217.1 57.9 L219.9 58.6 L222.8 59.2 L225.6 59.9 L228.5 60.5 L231.3 61.2 L234.2 61.8 L237 62.5 L239.9 63.1 L242.8 63.8 L245.6 64.4 L248.5 65.1 L251.3 65.7 L254.2 66.4 L257 67 L259.9 67.7 L262.7 68.4 L265.6 69 L268.5 69.7 L271.3 70.3 L274.2 71 L277 71.6 L279.9 72.3 L282.7 72.9 L285.6 73.6 L288.4 74.2 L291.3 74.9 L294.2 75.5 L297 76.2 L299.9 76.9 L302.7 77.5 L305.6 78.2 L308.4 78.8 L311.3 79.5 L314.1 80.1 L317 80.8 L319.8 81.4 L322.7 82.1 L325.6 82.7 L328.4 83.4 L331.3 84 L334.1 84.7 L337 85.3 L339.8 86 L342.7 86.7 L345.5 87.3 L348.4 88 L351.3 88.6 L354.1 89.3 L357 89.9 L359.8 90.6 L362.7 91.2 L365.5 91.9 L368.4 92.5 L371.2 93.2 L374.1 93.8 L377 94.5 L379.8 95.1 L382.7 95.7 L385.5 96.2 L388.4 96.6 L391.2 97 L394.1 97.3 L396.9 97.6 L399.8 97.8 L402.7 97.9 L405.5 98 L408.4 98 L411.2 98 L414.1 98 L416.9 98 L419.8 98 L422.6 98 L425.5 98 L428.4 98 L431.2 98 L434.1 98 L436.9 98 L439.8 98 L442.6 98 L445.5 98 L448.3 98 L451.2 98 L454.1 98 L456.9 98 L459.8 98 L462.6 98 L465.5 98 L468.3 98 L471.2 98 L474 98 L476.9 98 L479.7 98 L482.6 98 L485.5 98 L488.3 98 L491.2 98 L494 98 L496.9 98 L499.7 98 L502.6 98 L505.4 98 L508.3 98 L511.2 98 L514 98 L516.9 98 L519.7 98 L522.6 98 L525.4 98 L528.3 98 L531.1 98 L534 98" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="407.4" cy="98" r="3.2" fill="currentColor"/>
    <circle cx="525.7" cy="98" r="3.2" fill="currentColor" fill-opacity="0.55"/>
    <rect x="110.3" y="146.4" width="266.9" height="57.6" fill="currentColor" fill-opacity="0.1"/>
    <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3" opacity="0.85"><line x1="80" y1="146.4" x2="534" y2="146.4"/></g>
    <path d="M80 204 L81.9 203 L83.8 202.1 L85.7 201.1 L87.6 200.1 L89.5 199.2 L91.4 198.3 L93.3 197.3 L95.2 196.4 L97.1 195.5 L99 194.6 L100.9 193.7 L102.8 192.8 L104.7 191.9 L106.6 191.1 L108.5 190.2 L110.4 189.4 L112.3 188.5 L114.2 187.7 L116.1 186.9 L118 186 L119.9 185.2 L121.8 184.4 L123.7 183.6 L125.6 182.8 L127.5 182.1 L129.4 181.3 L131.3 180.5 L133.2 179.8 L135.1 179 L137 178.3 L138.9 177.6 L140.8 176.9 L142.7 176.2 L144.6 175.5 L146.5 174.8 L148.4 174.1 L150.3 173.4 L152.2 172.7 L154.1 172.1 L156 171.4 L157.9 170.8 L159.8 170.1 L161.7 169.5 L163.6 168.9 L165.5 168.3 L167.4 167.7 L169.3 167.1 L171.2 166.5 L173.1 165.9 L175 165.4 L176.9 164.8 L178.8 164.3 L180.7 163.7 L182.6 163.2 L184.5 162.7 L186.4 162.1 L188.3 161.6 L190.2 161.1 L192.1 160.6 L194 160.1 L195.9 159.7 L197.8 159.2 L199.7 158.7 L201.6 158.3 L203.5 157.9 L205.4 157.4 L207.3 157 L209.2 156.6 L211.1 156.2 L213 155.8 L214.9 155.4 L216.8 155 L218.7 154.6 L220.6 154.3 L222.5 153.9 L224.4 153.5 L226.3 153.2 L228.2 152.9 L230.1 152.5 L232 152.2 L233.9 151.9 L235.8 151.6 L237.7 151.3 L239.6 151 L241.5 150.8 L243.4 150.5 L245.3 150.2 L247.2 150 L249.1 149.8 L251 149.5 L252.9 149.3 L254.8 149.1 L256.7 148.9 L258.6 148.7 L260.5 148.5 L262.4 148.3 L264.3 148.1 L266.2 148 L268.1 147.8 L270 147.7 L271.9 147.5 L273.8 147.4 L275.7 147.3 L277.6 147.1 L279.5 147 L281.4 146.9 L283.3 146.8 L285.2 146.8 L287.1 146.7 L289 146.6 L290.9 146.6 L292.8 146.5 L294.7 146.5 L296.6 146.4 L298.5 146.4 L300.4 146.4 L302.3 146.4 L304.2 146.4 L306.1 146.4 L307.9 146.4 L309.8 146.5 L311.7 146.5 L313.6 146.5 L315.5 146.6 L317.4 146.6 L319.3 146.7 L321.2 146.8 L323.1 146.9 L325 147 L326.9 147.1 L328.8 147.2 L330.7 147.3 L332.6 147.4 L334.5 147.6 L336.4 147.7 L338.3 147.9 L340.2 148 L342.1 148.2 L344 148.4 L345.9 148.6 L347.8 148.7 L349.7 148.9 L351.6 149.2 L353.5 149.4 L355.4 149.6 L357.3 149.8 L359.2 150.1 L361.1 150.3 L363 150.6 L364.9 150.9 L366.8 151.1 L368.7 151.4 L370.6 151.7 L372.5 152 L374.4 152.3 L376.3 152.7 L378.2 153 L380.1 153.3 L382 153.7 L383.9 154 L385.8 154.4 L387.7 154.8 L389.6 155.1 L391.5 155.5 L393.4 155.9 L395.3 156.3 L397.2 156.7 L399.1 157.1 L401 157.6 L402.9 158 L404.8 158.5 L406.7 158.9 L408.6 159.4 L410.5 159.8 L412.4 160.3 L414.3 160.8 L416.2 161.3 L418.1 161.8 L420 162.3 L421.9 162.8 L423.8 163.4 L425.7 163.9 L427.6 164.5 L429.5 165 L431.4 165.6 L433.3 166.1 L435.2 166.7 L437.1 167.3 L439 167.9 L440.9 168.5 L442.8 169.1 L444.7 169.7 L446.6 170.4 L448.5 171 L450.4 171.7 L452.3 172.3 L454.2 173 L456.1 173.6 L458 174.3 L459.9 175 L461.8 175.7 L463.7 176.4 L465.6 177.1 L467.5 177.8 L469.4 178.6 L471.3 179.3 L473.2 180.1 L475.1 180.8 L477 181.6 L478.9 182.3 L480.8 183.1 L482.7 183.9 L484.6 184.7 L486.5 185.5 L488.4 186.3 L490.3 187.2 L492.2 188 L494.1 188.8 L496 189.7 L497.9 190.5 L499.8 191.4 L501.7 192.3 L503.6 193.1 L505.5 194 L507.4 194.9 L509.3 195.8 L511.2 196.7 L513.1 197.7 L515 198.6 L516.9 199.5 L518.8 200.5 L520.7 201.4 L522.6 202.4 L524.5 203.4 L526.4 204 L528.3 204 L530.2 204 L532.1 204 L534 204" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <polyline points="80,204 110.3,146.4 377.1,146.4 407.4,204 534,204" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="302.9" cy="146.4" r="2.6" fill="currentColor" fill-opacity="0.6"/>
    <g stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3" opacity="0.85"><line x1="80" y1="254" x2="534" y2="254"/><line x1="80" y1="310" x2="534" y2="310"/></g>
    <rect x="80" y="254" width="30.3" height="28" fill="currentColor" fill-opacity="0.12"/>
    <rect x="377.1" y="282" width="30.3" height="28" fill="currentColor" fill-opacity="0.12"/>
    <path d="M80 282 L80 254 L110.3 254 L110.3 282 L377.1 282 L377.1 310 L407.4 310 L407.4 282 L534 282" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M80 274.4 L525.7 289.6" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <g fill="currentColor">
    <text x="80" y="18" font-size="11" font-weight="bold">엘보 θ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> (deg)</tspan></text>
    <text x="137" y="124" font-size="11" text-anchor="end" font-weight="bold">속력 |θ̇</text>
    <text x="137" y="124" font-size="11" font-weight="bold"><tspan dy="3.5">2</tspan><tspan dy="-3.5">| (rad/s)</tspan></text>
    <text x="96" y="229" font-size="11" text-anchor="end" font-weight="bold">d|θ̇</text>
    <text x="96" y="229" font-size="11" font-weight="bold"><tspan dy="3.5">2</tspan><tspan dy="-3.5">|/dt (rad/s²)</tspan></text>
    <text x="73" y="34" font-size="11" text-anchor="end">90°</text>
    <text x="73" y="68" font-size="11" text-anchor="end">0°</text>
    <text x="73" y="102" font-size="11" text-anchor="end">−90°</text>
    <text x="73" y="208" font-size="11" text-anchor="end">0</text>
    <text x="73" y="179.2" font-size="11" text-anchor="end">0.4</text>
    <text x="73" y="150.4" font-size="11" text-anchor="end">0.8</text>
    <text x="73" y="258" font-size="11" text-anchor="end">2</text>
    <text x="73" y="286" font-size="11" text-anchor="end">0</text>
    <text x="73" y="314" font-size="11" text-anchor="end">−2</text>
    <text x="80" y="332.3" font-size="11" text-anchor="middle">0</text>
    <text x="155.7" y="332.3" font-size="11" text-anchor="middle">1</text>
    <text x="231.3" y="332.3" font-size="11" text-anchor="middle">2</text>
    <text x="307" y="332.3" font-size="11" text-anchor="middle">3</text>
    <text x="382.7" y="332.3" font-size="11" text-anchor="middle">4</text>
    <text x="458.3" y="332.3" font-size="11" text-anchor="middle">5</text>
    <text x="534" y="332.3" font-size="11" text-anchor="middle">6</text>
    <text x="307" y="347.3" font-size="11" text-anchor="middle">시간 (s)</text>
    <text x="407.4" y="113" font-size="11" text-anchor="middle">4.327 s</text>
    <text x="525.7" y="113" font-size="11" text-anchor="middle">5.890 s</text>
    <text x="202.6" y="71.6" font-size="11" text-anchor="end">사다리꼴</text>
    <text x="246.5" y="44.4" font-size="11" opacity="0.75">3차</text>
    <text x="518.9" y="141.4" font-size="11" text-anchor="end">v<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">= 0.8</tspan></text>
    <text x="518.9" y="249" font-size="11" text-anchor="end">a<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">= 2</tspan></text>
    <text x="117.8" y="305" font-size="11">−a<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1" dx="3.3">= −2</tspan></text>
    <text x="243.4" y="198.2" font-size="11" text-anchor="middle">v<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1">에 3.527 s 붙어 있음 (이동의 81.5 %)</tspan></text>
    <text x="97.1" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="392.3" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="126.9" y="273.3" font-size="11" opacity="0.8">3차 최댓값 0.543 rad/s² (a<tspan dy="3.1" font-size="10">max</tspan><tspan dy="-3.1">의 27 %)</tspan></text>
    </g>
    <line x1="350" y1="14" x2="372" y2="14" stroke="currentColor" stroke-width="2.2"/>
    <text x="377" y="18" font-size="11" fill="currentColor">사다리꼴</text>
    <line x1="450" y1="14" x2="472" y2="14" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <text x="477" y="18" font-size="11" fill="currentColor">3차</text>
  </g>
</svg>

P2의 엘보 뒤집기 $|\Delta\theta_2| = \pi$에 두 방식으로 시간을 입혀 $0$–$6\,\mathrm{s}$ 축 하나에 그렸다 — 위 단은 엘보 각, 가운데 단은 $v_{\max} = 0.8\,\mathrm{rad/s}$ 점선에 대한 속력 $|\dot\theta_2|$, 아래 단은 $a_{\max} = 2\,\mathrm{rad/s^2}$ 점선에 대한 그 속력의 변화율이다. 사다리꼴은 $\pm a_{\max}$의 $0.4\,\mathrm{s}$ 램프 사이에서 $3.527\,\mathrm{s}$, 곧 이동의 $81.5\,\%$ 동안 $v_{\max}$에 붙어 있다가 $4.327\,\mathrm{s}$에 끝나고, 3차는 중간에서 한순간만 $v_{\max}$에 닿고 가속도는 $a_{\max}$의 $27\,\%$인 $0.543\,\mathrm{rad/s^2}$까지만 올라가며 $5.890\,\mathrm{s}$가 걸린다. 이 그림이 말하려는 전부는 각 프로파일이 어느 점선에 닿느냐이고, 사다리꼴은 둘 다, 3차는 속도 한계에만 닿는다.

### 대상으로 한 번 끝까지 · Worked case

두 관절이 하나의 시간 스케일링 $s(t)$ — 시각 $t$에 팔이 경로를 얼마나 갔는지를 말하는, $[0, T]$에서 $[0, 1]$로 가는 단조 함수, §2에서 정의 — 를 타므로 관절 $i$는 $\dot\theta_i = \Delta\theta_i\,\dot s$, $\ddot\theta_i = \Delta\theta_i\,\ddot s$다. 따라서 모든 최댓값이 $|\Delta\theta_i|$에 비례하고, $|\Delta\theta_i|$가 가장 큰 관절이 먼저 한계에 닿는다. 여기서는 엘보이며 $|\Delta\theta_2| = \pi = 3.1416\,\mathrm{rad}$, 어깨의 정확히 두 배다. **엘보에 맞춰 스케일링을 설계하면 어깨는 저절로 따라온다.**

**A — 사다리꼴**(일정 가속 $+a_{\max}$, $v_{\max}$로 순항, 일정 감속 $-a_{\max}$; §3에서 정의). 먼저 순항 구간이 존재하는지부터 정한다. 짧은 이동은 $v_{\max}$에 닿지 못하기 때문이다. $v_{\max}$까지 올렸다가 곧바로 내리면 $t_a = v_{\max}/a_{\max}$일 때 $2 \cdot \tfrac12 a_{\max}t_a^2$를 이동하므로

$$\Delta\theta^{*} = \frac{v_{\max}^2}{a_{\max}} = \frac{0.8^2}{2} = 0.32\ \mathrm{rad}$$

이고, 우리의 $3.1416\,\mathrm{rad}$이 그보다 훨씬 크므로 삼각형이 아니라 진짜 사다리꼴이다. 그다음:

- 상승 시간 $t_a = v_{\max}/a_{\max} = 0.8/2 = 0.4\ \mathrm{s}$, 올라가며 $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16\ \mathrm{rad}$, 내려가며 $0.16\,\mathrm{rad}$;
- 순항 거리 $3.1416 - 0.32 = 2.8216\ \mathrm{rad}$, $0.8\,\mathrm{rad/s}$로 $2.8216/0.8 = 3.5270\ \mathrm{s}$;
- 합계 $T_{\text{trap}} = 0.4 + 3.5270 + 0.4 = \mathbf{4.327\ s}$, 그중 순항이 $3.5270/4.327 = 81.5\,\%$.

같은 $s(t)$를 절반 진폭으로 타는 어깨를 확인한다. 최대 속도 $0.5 \times 0.8 = 0.4\,\mathrm{rad/s}$, 최대 가속도 $0.5 \times 2 = 1\,\mathrm{rad/s^2}$. 둘 다 한계의 절반이라 어깨는 아무것도 구속하지 않는다.

**B — 같은 이동의 3차.** $s(t) = 3t^2/T^2 - 2t^3/T^3$을 미분하면 $\dot s = (6t/T^2)(1 - t/T)$, $\ddot s = (6/T^2)(1 - 2t/T)$이므로 단위 이동 최댓값은 $t = T/2$에서 $\dot s_{\max} = 1.5/T$, 양 끝에서 $|\ddot s|_{\max} = 6/T^2$이고, 엘보의 최댓값은 $1.5\,\Delta\theta/T$와 $6\,\Delta\theta/T^2$다. 두 한계를 각각 뒤집어 최소 허용 시간을 구한다:

$$T_v = \frac{1.5\,\Delta\theta}{v_{\max}} = \frac{1.5 \times 3.1416}{0.8} = 5.8905\ \mathrm{s}, \qquad T_a = \sqrt{\frac{6\,\Delta\theta}{a_{\max}}} = \sqrt{\frac{6 \times 3.1416}{2}} = 3.0700\ \mathrm{s}$$

$T$가 길어지면 두 최댓값이 모두 내려가므로 각 한계가 하한을 하나씩 주고 이동은 둘 중 큰 쪽을 만족해야 한다. 여기서는 $T_v > T_a$이므로 $T_{\text{cubic}} = \mathbf{5.890\ s}$, **속도가 걸리는 한계**다. 되대입해 확인하면 그 시간에서 최대 가속도는 $6 \times 3.1416/5.8905^2 = 0.543\,\mathrm{rad/s^2}$, $a_{\max}$의 $27\,\%$에 불과하다. 모터의 토크를 거의 쓰지 않는다.

**C — 둘을 맞대어 읽기.** 3차를 사다리꼴의 시간에 억지로 밀어 넣으면 $1.5 \times 3.1416/4.327 = 1.089\,\mathrm{rad/s}$를 요구하는데 이는 $v_{\max}$의 $36\,\%$ 초과다. $T = 4.327\,\mathrm{s}$에서 3차는 이 관절로 실행 자체가 불가능하다. 대신 각자 허용되는 시간끼리 비교한다:

$$\frac{T_{\text{cubic}}}{T_{\text{trap}}} = \frac{5.8905}{4.3270} = 1.361 \quad\Longrightarrow\quad \text{사다리꼴이 } 26.5\,\% \text{ 먼저 끝난다}$$

이유는 그림 가운데 단에 보인다. 사다리꼴은 이동의 $81.5\,\%$ 동안 $v_{\max}$에 *붙어* 있고, 3차는 한순간만 $v_{\max}$에 닿고 나머지는 그 아래다. 이동 내내 한계에 붙어 있는 것이 이득의 전부이며, 그 대가는 양 모서리의 불연속 가속도다.

**D — 일반적으로 어느 한계가 걸리는가.** $T_v = T_a$로 놓고 풀면 3차의 교차점이 나온다:

$$\Delta\theta^{\dagger} = \frac{8}{3}\cdot\frac{v_{\max}^2}{a_{\max}} = \frac{8}{3}\cdot\frac{0.64}{2} = 0.853\ \mathrm{rad}$$

$1.5\Delta\theta/v_{\max} = \sqrt{6\Delta\theta/a_{\max}}$를 제곱하면 $2.25\Delta\theta^2/v_{\max}^2 = 6\Delta\theta/a_{\max}$가 되기 때문이다. $0.853\,\mathrm{rad}$ 위에서는 속도가, 아래에서는 가속도가 걸린다. 이 페이지의 두 이동 — 여기의 엘보 $3.1416$과 §1 계산 예제의 $1.2$ — 은 모두 그 위이고, 그래서 둘 다 속도 구속이다. $0.5\,\mathrm{rad}$ 이동은 그 아래에 있고, 스스로 점검 4번이 그것에 시간을 입힌다. 과제는 $\Delta\theta$를 전혀 건드리지 않고 장치를 이 선의 반대편으로 옮긴다.

<svg viewBox="0 0 560 306" style="max-width:100%;height:auto" role="img" aria-label="P2의 고정 한계 0.8 rad/s, 2 rad/s²에서 관절 이동 크기에 대한 소요 시간: 사다리꼴과 가장 빠른 3차. 0.32 rad 아래에서 사다리꼴은 삼각형이고, 0.853 rad 아래에서 3차는 가속도가, 위에서는 속도가 걸린다. 0.5, 1.2, π/2, π rad 이동을 표시했다.">
  <defs><marker id="mr09durk" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <rect x="62" y="36" width="107.3" height="226" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.6"><line x1="62" y1="262" x2="502" y2="262"/><line x1="62" y1="262" x2="62" y2="36"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5"><line x1="62.0" y1="262" x2="62.0" y2="266"/><line x1="124.9" y1="262" x2="124.9" y2="266"/><line x1="187.7" y1="262" x2="187.7" y2="266"/><line x1="250.6" y1="262" x2="250.6" y2="266"/><line x1="313.4" y1="262" x2="313.4" y2="266"/><line x1="376.3" y1="262" x2="376.3" y2="266"/><line x1="439.1" y1="262" x2="439.1" y2="266"/><line x1="502.0" y1="262" x2="502.0" y2="266"/><line x1="58" y1="262.0" x2="62" y2="262.0"/><line x1="58" y1="229.7" x2="62" y2="229.7"/><line x1="58" y1="197.4" x2="62" y2="197.4"/><line x1="58" y1="165.1" x2="62" y2="165.1"/><line x1="58" y1="132.9" x2="62" y2="132.9"/><line x1="58" y1="100.6" x2="62" y2="100.6"/><line x1="58" y1="68.3" x2="62" y2="68.3"/><line x1="58" y1="36.0" x2="62" y2="36.0"/></g>
  <polyline points="62.0,262.0 63.3,261.4 64.5,260.8 65.8,260.2 67.0,259.6 68.3,259.0 69.6,258.4 70.8,257.8 72.1,257.2 73.3,256.5 74.6,255.9 75.8,255.3 77.1,254.7 78.4,254.1 79.6,253.5 80.9,252.9 82.1,252.3 83.4,251.7 84.6,251.1 85.9,250.5 87.2,249.9 88.4,249.3 89.7,248.7 90.9,248.1 92.2,247.5 93.4,246.9 94.7,246.3 96.0,245.6 97.2,245.0 98.5,244.4 99.7,243.8 101.0,243.2 102.2,242.6 103.5,242.0 104.8,241.4 106.0,240.8 107.3,240.2 108.5,239.6 109.8,239.0 111.0,238.4 112.3,237.8 113.6,237.2 114.8,236.6 116.1,236.0 117.3,235.4 118.6,234.8 119.8,234.1 121.1,233.5 122.4,232.9 123.6,232.3 124.9,231.7 126.1,231.1 127.4,230.5 128.6,229.9 129.9,229.3 131.2,228.7 132.4,228.1 133.7,227.5 134.9,226.9 136.2,226.3 137.4,225.7 138.7,225.1 140.0,224.5 141.2,223.9 142.5,223.3 143.7,222.6 145.0,222.0 146.2,221.4 147.5,220.8 148.8,220.2 150.0,219.6 151.3,219.0 152.5,218.4 153.8,217.8 155.0,217.2 156.3,216.6 157.6,216.0 158.8,215.4 160.1,214.8 161.3,214.2 162.6,213.6 163.8,213.0 165.1,212.4 166.4,211.8 167.6,211.1 168.9,210.5 170.1,209.9 171.4,209.3 172.6,208.7 173.9,208.1 175.2,207.5 176.4,206.9 177.7,206.3 178.9,205.7 180.2,205.1 181.4,204.5 182.7,203.9 184.0,203.3 185.2,202.7 186.5,202.1 187.7,201.5 189.0,200.9 190.2,200.2 191.5,199.6 192.8,199.0 194.0,198.4 195.3,197.8 196.5,197.2 197.8,196.6 199.0,196.0 200.3,195.4 201.6,194.8 202.8,194.2 204.1,193.6 205.3,193.0 206.6,192.4 207.8,191.8 209.1,191.2 210.4,190.6 211.6,190.0 212.9,189.4 214.1,188.7 215.4,188.1 216.6,187.5 217.9,186.9 219.2,186.3 220.4,185.7 221.7,185.1 222.9,184.5 224.2,183.9 225.4,183.3 226.7,182.7 228.0,182.1 229.2,181.5 230.5,180.9 231.7,180.3 233.0,179.7 234.2,179.1 235.5,178.5 236.8,177.9 238.0,177.2 239.3,176.6 240.5,176.0 241.8,175.4 243.0,174.8 244.3,174.2 245.6,173.6 246.8,173.0 248.1,172.4 249.3,171.8 250.6,171.2 251.8,170.6 253.1,170.0 254.3,169.4 255.6,168.8 256.9,168.2 258.1,167.6 259.4,167.0 260.6,166.4 261.9,165.7 263.1,165.1 264.4,164.5 265.7,163.9 266.9,163.3 268.2,162.7 269.4,162.1 270.7,161.5 271.9,160.9 273.2,160.3 274.5,159.7 275.7,159.1 277.0,158.5 278.2,157.9 279.5,157.3 280.7,156.7 282.0,156.1 283.3,155.5 284.5,154.8 285.8,154.2 287.0,153.6 288.3,153.0 289.5,152.4 290.8,151.8 292.1,151.2 293.3,150.6 294.6,150.0 295.8,149.4 297.1,148.8 298.3,148.2 299.6,147.6 300.9,147.0 302.1,146.4 303.4,145.8 304.6,145.2 305.9,144.6 307.1,144.0 308.4,143.3 309.7,142.7 310.9,142.1 312.2,141.5 313.4,140.9 314.7,140.3 315.9,139.7 317.2,139.1 318.5,138.5 319.7,137.9 321.0,137.3 322.2,136.7 323.5,136.1 324.7,135.5 326.0,134.9 327.3,134.3 328.5,133.7 329.8,133.1 331.0,132.5 332.3,131.8 333.5,131.2 334.8,130.6 336.1,130.0 337.3,129.4 338.6,128.8 339.8,128.2 341.1,127.6 342.3,127.0 343.6,126.4 344.9,125.8 346.1,125.2 347.4,124.6 348.6,124.0 349.9,123.4 351.1,122.8 352.4,122.2 353.7,121.6 354.9,120.9 356.2,120.3 357.4,119.7 358.7,119.1 359.9,118.5 361.2,117.9 362.5,117.3 363.7,116.7 365.0,116.1 366.2,115.5 367.5,114.9 368.7,114.3 370.0,113.7 371.3,113.1 372.5,112.5 373.8,111.9 375.0,111.3 376.3,110.7 377.5,110.1 378.8,109.4 380.1,108.8 381.3,108.2 382.6,107.6 383.8,107.0 385.1,106.4 386.3,105.8 387.6,105.2 388.9,104.6 390.1,104.0 391.4,103.4 392.6,102.8 393.9,102.2 395.1,101.6 396.4,101.0 397.7,100.4 398.9,99.8 400.2,99.2 401.4,98.6 402.7,97.9 403.9,97.3 405.2,96.7 406.5,96.1 407.7,95.5 409.0,94.9 410.2,94.3 411.5,93.7 412.7,93.1 414.0,92.5 415.3,91.9 416.5,91.3 417.8,90.7 419.0,90.1 420.3,89.5 421.5,88.9 422.8,88.3 424.1,87.7 425.3,87.1 426.6,86.4 427.8,85.8 429.1,85.2 430.3,84.6 431.6,84.0 432.9,83.4 434.1,82.8 435.4,82.2 436.6,81.6 437.9,81.0 439.1,80.4 440.4,79.8 441.7,79.2 442.9,78.6 444.2,78.0 445.4,77.4 446.7,76.8 447.9,76.2 449.2,75.5 450.5,74.9 451.7,74.3 453.0,73.7 454.2,73.1 455.5,72.5 456.7,71.9 458.0,71.3 459.3,70.7 460.5,70.1 461.8,69.5 463.0,68.9 464.3,68.3 465.5,67.7 466.8,67.1 468.1,66.5 469.3,65.9 470.6,65.3 471.8,64.7 473.1,64.0 474.3,63.4 475.6,62.8 476.9,62.2 478.1,61.6 479.4,61.0 480.6,60.4 481.9,59.8 483.1,59.2 484.4,58.6 485.7,58.0 486.9,57.4 488.2,56.8 489.4,56.2 490.7,55.6 491.9,55.0 493.2,54.4 494.5,53.8 495.7,53.2 497.0,52.5 498.2,51.9 499.5,51.3 500.7,50.7 502.0,50.1" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="2 3" opacity="0.5"/>
  <polyline points="62.0,261.4 63.3,256.4 64.5,254.1 65.8,252.3 67.0,250.8 68.3,249.5 69.6,248.3 70.8,247.2 72.1,246.2 73.3,245.2 74.6,244.3 75.8,243.4 77.1,242.6 78.4,241.8 79.6,241.1 80.9,240.3 82.1,239.6 83.4,238.9 84.6,238.3 85.9,237.6 87.2,237.0 88.4,236.4 89.7,235.8 90.9,235.2 92.2,234.6 93.4,234.0 94.7,233.5 96.0,232.9 97.2,232.4 98.5,231.9 99.7,231.4 101.0,230.9 102.2,230.4 103.5,229.9 104.8,229.4 106.0,228.9 107.3,228.4 108.5,228.0 109.8,227.5 111.0,227.1 112.3,226.6 113.6,226.2 114.8,225.8 116.1,225.3 117.3,224.9 118.6,224.5 119.8,224.1 121.1,223.7 122.4,223.3 123.6,222.9 124.9,222.5 126.1,222.1 127.4,221.7 128.6,221.3 129.9,220.9 131.2,220.5 132.4,220.1 133.7,219.8 134.9,219.4 136.2,219.0 137.4,218.7 138.7,218.3 140.0,218.0 141.2,217.6 142.5,217.3 143.7,216.9 145.0,216.6 146.2,216.2 147.5,215.9 148.8,215.5 150.0,215.2 151.3,214.9 152.5,214.5 153.8,214.2 155.0,213.9 156.3,213.6 157.6,213.2 158.8,212.9 160.1,212.6 161.3,212.3 162.6,212.0 163.8,211.7 165.1,211.4 166.4,211.1 167.6,210.7 168.9,210.4 170.1,210.1 171.4,209.8 172.6,209.5 173.9,209.2 175.2,208.9 176.4,208.7 177.7,208.4 178.9,208.1 180.2,207.8 181.4,207.5 182.7,207.2 184.0,206.9 185.2,206.6 186.5,206.4 187.7,206.1 189.0,205.8 190.2,205.5 191.5,205.2 192.8,205.0 194.0,204.7 195.3,204.4 196.5,204.2 197.8,203.9 199.0,203.6 200.3,203.3 201.6,203.1 202.8,202.8 204.1,202.6 205.3,202.3 206.6,202.0 207.8,201.8 209.1,201.5 210.4,201.3 211.6,201.0 212.9,200.7 214.1,200.5 215.4,200.2 216.6,200.0 217.9,199.7 219.2,199.5 220.4,199.2 221.7,199.0 222.9,198.7 224.2,198.5 225.4,198.2 226.7,198.0 228.0,197.8 229.2,197.5 230.5,197.3 231.7,197.0 233.0,196.8 234.2,196.5 235.5,196.3 236.8,196.1 238.0,195.8 239.3,195.6 240.5,195.4 241.8,195.1 243.0,194.9 244.3,194.7 245.6,194.4 246.8,194.2 248.1,194.0 249.3,193.7 250.6,193.5 251.8,193.3 253.1,193.1 254.3,192.8 255.6,192.6 256.9,192.4 258.1,192.2 259.4,191.9 260.6,191.7 261.9,191.5 263.1,191.3 264.4,191.0 265.7,190.8 266.9,190.6 268.2,190.4 269.4,190.2 270.7,190.0 271.9,189.7 273.2,189.5 274.5,189.3 275.7,189.1 277.0,188.9 278.2,188.7 279.5,188.4 280.7,188.2 282.0,188.0 283.3,187.8 284.5,187.6 285.8,187.4 287.0,187.2 288.3,187.0 289.5,186.8 290.8,186.6 292.1,186.4 293.3,186.1 294.6,185.9 295.8,185.7 297.1,185.5 298.3,185.3 299.6,185.1 300.9,184.9 302.1,184.7 303.4,184.5 304.6,184.3 305.9,184.1 307.1,183.9 308.4,183.7 309.7,183.5 310.9,183.3 312.2,183.1 313.4,182.9 314.7,182.7 315.9,182.5 317.2,182.3 318.5,182.1 319.7,181.9 321.0,181.7 322.2,181.5 323.5,181.3 324.7,181.2 326.0,181.0 327.3,180.8 328.5,180.6 329.8,180.4 331.0,180.2 332.3,180.0 333.5,179.8 334.8,179.6 336.1,179.4 337.3,179.2 338.6,179.1 339.8,178.9 341.1,178.7 342.3,178.5 343.6,178.3 344.9,178.1 346.1,177.9 347.4,177.7 348.6,177.6 349.9,177.4 351.1,177.2 352.4,177.0 353.7,176.8 354.9,176.6 356.2,176.5 357.4,176.3 358.7,176.1 359.9,175.9 361.2,175.7 362.5,175.5 363.7,175.4 365.0,175.2 366.2,175.0 367.5,174.8 368.7,174.6 370.0,174.5 371.3,174.3 372.5,174.1 373.8,173.9 375.0,173.8 376.3,173.6 377.5,173.4 378.8,173.2 380.1,173.1 381.3,172.9 382.6,172.7 383.8,172.5 385.1,172.4 386.3,172.2 387.6,172.0 388.9,171.8 390.1,171.7 391.4,171.5 392.6,171.3 393.9,171.1 395.1,171.0 396.4,170.8 397.7,170.6 398.9,170.5 400.2,170.3 401.4,170.1 402.7,169.9 403.9,169.8 405.2,169.6 406.5,169.4 407.7,169.3 409.0,169.1 410.2,168.9 411.5,168.8 412.7,168.6 414.0,168.4 415.3,168.3 416.5,168.1 417.8,167.9 419.0,167.8 420.3,167.6 421.5,167.4 422.8,167.3 424.1,167.1 425.3,166.9 426.6,166.8 427.8,166.6 429.1,166.4 430.3,166.3 431.6,166.1 432.9,166.0 434.1,165.8 435.4,165.6 436.6,165.5 437.9,165.3 439.1,165.1 440.4,165.0 441.7,164.8 442.9,164.7 444.2,164.5 445.4,164.3 446.7,164.2 447.9,164.0 449.2,163.9 450.5,163.7 451.7,163.5 453.0,163.4 454.2,163.2 455.5,163.1 456.7,162.9 458.0,162.8 459.3,162.6 460.5,162.4 461.8,162.3 463.0,162.1 464.3,162.0 465.5,161.8 466.8,161.7 468.1,161.5 469.3,161.3 470.6,161.2 471.8,161.0 473.1,160.9 474.3,160.7 475.6,160.6 476.9,160.4 478.1,160.3 479.4,160.1 480.6,160.0 481.9,159.8 483.1,159.6 484.4,159.5 485.7,159.3 486.9,159.2 488.2,159.0 489.4,158.9 490.7,158.7 491.9,158.6 493.2,158.4 494.5,158.3 495.7,158.1 497.0,158.0 498.2,157.8 499.5,157.7 500.7,157.5 502.0,157.4" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="2 3" opacity="0.5"/>
  <polyline points="62.0,261.4 63.3,256.4 64.5,254.1 65.8,252.3 67.0,250.8 68.3,249.5 69.6,248.3 70.8,247.2 72.1,246.2 73.3,245.2 74.6,244.3 75.8,243.4 77.1,242.6 78.4,241.8 79.6,241.1 80.9,240.3 82.1,239.6 83.4,238.9 84.6,238.3 85.9,237.6 87.2,237.0 88.4,236.4 89.7,235.8 90.9,235.2 92.2,234.6 93.4,234.0 94.7,233.5 96.0,232.9 97.2,232.4 98.5,231.9 99.7,231.4 101.0,230.9 102.2,230.4 103.5,229.9 104.8,229.4 106.0,228.9 107.3,228.4 108.5,228.0 109.8,227.5 111.0,227.1 112.3,226.6 113.6,226.2 114.8,225.8 116.1,225.3 117.3,224.9 118.6,224.5 119.8,224.1 121.1,223.7 122.4,223.3 123.6,222.9 124.9,222.5 126.1,222.1 127.4,221.7 128.6,221.3 129.9,220.9 131.2,220.5 132.4,220.1 133.7,219.8 134.9,219.4 136.2,219.0 137.4,218.7 138.7,218.3 140.0,218.0 141.2,217.6 142.5,217.3 143.7,216.9 145.0,216.6 146.2,216.2 147.5,215.9 148.8,215.5 150.0,215.2 151.3,214.9 152.5,214.5 153.8,214.2 155.0,213.9 156.3,213.6 157.6,213.2 158.8,212.9 160.1,212.6 161.3,212.3 162.6,212.0 163.8,211.7 165.1,211.4 166.4,211.1 167.6,210.7 168.9,210.4 170.1,209.9 171.4,209.3 172.6,208.7 173.9,208.1 175.2,207.5 176.4,206.9 177.7,206.3 178.9,205.7 180.2,205.1 181.4,204.5 182.7,203.9 184.0,203.3 185.2,202.7 186.5,202.1 187.7,201.5 189.0,200.9 190.2,200.2 191.5,199.6 192.8,199.0 194.0,198.4 195.3,197.8 196.5,197.2 197.8,196.6 199.0,196.0 200.3,195.4 201.6,194.8 202.8,194.2 204.1,193.6 205.3,193.0 206.6,192.4 207.8,191.8 209.1,191.2 210.4,190.6 211.6,190.0 212.9,189.4 214.1,188.7 215.4,188.1 216.6,187.5 217.9,186.9 219.2,186.3 220.4,185.7 221.7,185.1 222.9,184.5 224.2,183.9 225.4,183.3 226.7,182.7 228.0,182.1 229.2,181.5 230.5,180.9 231.7,180.3 233.0,179.7 234.2,179.1 235.5,178.5 236.8,177.9 238.0,177.2 239.3,176.6 240.5,176.0 241.8,175.4 243.0,174.8 244.3,174.2 245.6,173.6 246.8,173.0 248.1,172.4 249.3,171.8 250.6,171.2 251.8,170.6 253.1,170.0 254.3,169.4 255.6,168.8 256.9,168.2 258.1,167.6 259.4,167.0 260.6,166.4 261.9,165.7 263.1,165.1 264.4,164.5 265.7,163.9 266.9,163.3 268.2,162.7 269.4,162.1 270.7,161.5 271.9,160.9 273.2,160.3 274.5,159.7 275.7,159.1 277.0,158.5 278.2,157.9 279.5,157.3 280.7,156.7 282.0,156.1 283.3,155.5 284.5,154.8 285.8,154.2 287.0,153.6 288.3,153.0 289.5,152.4 290.8,151.8 292.1,151.2 293.3,150.6 294.6,150.0 295.8,149.4 297.1,148.8 298.3,148.2 299.6,147.6 300.9,147.0 302.1,146.4 303.4,145.8 304.6,145.2 305.9,144.6 307.1,144.0 308.4,143.3 309.7,142.7 310.9,142.1 312.2,141.5 313.4,140.9 314.7,140.3 315.9,139.7 317.2,139.1 318.5,138.5 319.7,137.9 321.0,137.3 322.2,136.7 323.5,136.1 324.7,135.5 326.0,134.9 327.3,134.3 328.5,133.7 329.8,133.1 331.0,132.5 332.3,131.8 333.5,131.2 334.8,130.6 336.1,130.0 337.3,129.4 338.6,128.8 339.8,128.2 341.1,127.6 342.3,127.0 343.6,126.4 344.9,125.8 346.1,125.2 347.4,124.6 348.6,124.0 349.9,123.4 351.1,122.8 352.4,122.2 353.7,121.6 354.9,120.9 356.2,120.3 357.4,119.7 358.7,119.1 359.9,118.5 361.2,117.9 362.5,117.3 363.7,116.7 365.0,116.1 366.2,115.5 367.5,114.9 368.7,114.3 370.0,113.7 371.3,113.1 372.5,112.5 373.8,111.9 375.0,111.3 376.3,110.7 377.5,110.1 378.8,109.4 380.1,108.8 381.3,108.2 382.6,107.6 383.8,107.0 385.1,106.4 386.3,105.8 387.6,105.2 388.9,104.6 390.1,104.0 391.4,103.4 392.6,102.8 393.9,102.2 395.1,101.6 396.4,101.0 397.7,100.4 398.9,99.8 400.2,99.2 401.4,98.6 402.7,97.9 403.9,97.3 405.2,96.7 406.5,96.1 407.7,95.5 409.0,94.9 410.2,94.3 411.5,93.7 412.7,93.1 414.0,92.5 415.3,91.9 416.5,91.3 417.8,90.7 419.0,90.1 420.3,89.5 421.5,88.9 422.8,88.3 424.1,87.7 425.3,87.1 426.6,86.4 427.8,85.8 429.1,85.2 430.3,84.6 431.6,84.0 432.9,83.4 434.1,82.8 435.4,82.2 436.6,81.6 437.9,81.0 439.1,80.4 440.4,79.8 441.7,79.2 442.9,78.6 444.2,78.0 445.4,77.4 446.7,76.8 447.9,76.2 449.2,75.5 450.5,74.9 451.7,74.3 453.0,73.7 454.2,73.1 455.5,72.5 456.7,71.9 458.0,71.3 459.3,70.7 460.5,70.1 461.8,69.5 463.0,68.9 464.3,68.3 465.5,67.7 466.8,67.1 468.1,66.5 469.3,65.9 470.6,65.3 471.8,64.7 473.1,64.0 474.3,63.4 475.6,62.8 476.9,62.2 478.1,61.6 479.4,61.0 480.6,60.4 481.9,59.8 483.1,59.2 484.4,58.6 485.7,58.0 486.9,57.4 488.2,56.8 489.4,56.2 490.7,55.6 491.9,55.0 493.2,54.4 494.5,53.8 495.7,53.2 497.0,52.5 498.2,51.9 499.5,51.3 500.7,50.7 502.0,50.1" fill="none" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
  <polyline points="62.0,261.5 63.3,257.4 64.5,255.5 65.8,254.1 67.0,252.9 68.3,251.8 69.6,250.8 70.8,249.9 72.1,249.1 73.3,248.3 74.6,247.6 75.8,246.8 77.1,246.2 78.4,245.5 79.6,244.9 80.9,244.3 82.1,243.7 83.4,243.2 84.6,242.6 85.9,242.1 87.2,241.6 88.4,241.1 89.7,240.6 90.9,240.1 92.2,239.6 93.4,239.2 94.7,238.7 96.0,238.3 97.2,237.8 98.5,237.4 99.7,237.0 101.0,236.6 102.2,236.2 103.5,235.8 104.8,235.4 106.0,235.0 107.3,234.6 108.5,234.1 109.8,233.7 111.0,233.3 112.3,232.9 113.6,232.5 114.8,232.1 116.1,231.7 117.3,231.3 118.6,230.9 119.8,230.5 121.1,230.1 122.4,229.7 123.6,229.3 124.9,228.9 126.1,228.5 127.4,228.1 128.6,227.7 129.9,227.3 131.2,226.9 132.4,226.5 133.7,226.1 134.9,225.7 136.2,225.3 137.4,224.9 138.7,224.5 140.0,224.1 141.2,223.7 142.5,223.3 143.7,222.9 145.0,222.4 146.2,222.0 147.5,221.6 148.8,221.2 150.0,220.8 151.3,220.4 152.5,220.0 153.8,219.6 155.0,219.2 156.3,218.8 157.6,218.4 158.8,218.0 160.1,217.6 161.3,217.2 162.6,216.8 163.8,216.4 165.1,216.0 166.4,215.6 167.6,215.2 168.9,214.8 170.1,214.4 171.4,214.0 172.6,213.6 173.9,213.2 175.2,212.8 176.4,212.4 177.7,212.0 178.9,211.6 180.2,211.1 181.4,210.7 182.7,210.3 184.0,209.9 185.2,209.5 186.5,209.1 187.7,208.7 189.0,208.3 190.2,207.9 191.5,207.5 192.8,207.1 194.0,206.7 195.3,206.3 196.5,205.9 197.8,205.5 199.0,205.1 200.3,204.7 201.6,204.3 202.8,203.9 204.1,203.5 205.3,203.1 206.6,202.7 207.8,202.3 209.1,201.9 210.4,201.5 211.6,201.1 212.9,200.7 214.1,200.3 215.4,199.8 216.6,199.4 217.9,199.0 219.2,198.6 220.4,198.2 221.7,197.8 222.9,197.4 224.2,197.0 225.4,196.6 226.7,196.2 228.0,195.8 229.2,195.4 230.5,195.0 231.7,194.6 233.0,194.2 234.2,193.8 235.5,193.4 236.8,193.0 238.0,192.6 239.3,192.2 240.5,191.8 241.8,191.4 243.0,191.0 244.3,190.6 245.6,190.2 246.8,189.8 248.1,189.4 249.3,189.0 250.6,188.5 251.8,188.1 253.1,187.7 254.3,187.3 255.6,186.9 256.9,186.5 258.1,186.1 259.4,185.7 260.6,185.3 261.9,184.9 263.1,184.5 264.4,184.1 265.7,183.7 266.9,183.3 268.2,182.9 269.4,182.5 270.7,182.1 271.9,181.7 273.2,181.3 274.5,180.9 275.7,180.5 277.0,180.1 278.2,179.7 279.5,179.3 280.7,178.9 282.0,178.5 283.3,178.1 284.5,177.7 285.8,177.2 287.0,176.8 288.3,176.4 289.5,176.0 290.8,175.6 292.1,175.2 293.3,174.8 294.6,174.4 295.8,174.0 297.1,173.6 298.3,173.2 299.6,172.8 300.9,172.4 302.1,172.0 303.4,171.6 304.6,171.2 305.9,170.8 307.1,170.4 308.4,170.0 309.7,169.6 310.9,169.2 312.2,168.8 313.4,168.4 314.7,168.0 315.9,167.6 317.2,167.2 318.5,166.8 319.7,166.4 321.0,165.9 322.2,165.5 323.5,165.1 324.7,164.7 326.0,164.3 327.3,163.9 328.5,163.5 329.8,163.1 331.0,162.7 332.3,162.3 333.5,161.9 334.8,161.5 336.1,161.1 337.3,160.7 338.6,160.3 339.8,159.9 341.1,159.5 342.3,159.1 343.6,158.7 344.9,158.3 346.1,157.9 347.4,157.5 348.6,157.1 349.9,156.7 351.1,156.3 352.4,155.9 353.7,155.5 354.9,155.1 356.2,154.6 357.4,154.2 358.7,153.8 359.9,153.4 361.2,153.0 362.5,152.6 363.7,152.2 365.0,151.8 366.2,151.4 367.5,151.0 368.7,150.6 370.0,150.2 371.3,149.8 372.5,149.4 373.8,149.0 375.0,148.6 376.3,148.2 377.5,147.8 378.8,147.4 380.1,147.0 381.3,146.6 382.6,146.2 383.8,145.8 385.1,145.4 386.3,145.0 387.6,144.6 388.9,144.2 390.1,143.8 391.4,143.3 392.6,142.9 393.9,142.5 395.1,142.1 396.4,141.7 397.7,141.3 398.9,140.9 400.2,140.5 401.4,140.1 402.7,139.7 403.9,139.3 405.2,138.9 406.5,138.5 407.7,138.1 409.0,137.7 410.2,137.3 411.5,136.9 412.7,136.5 414.0,136.1 415.3,135.7 416.5,135.3 417.8,134.9 419.0,134.5 420.3,134.1 421.5,133.7 422.8,133.3 424.1,132.9 425.3,132.5 426.6,132.0 427.8,131.6 429.1,131.2 430.3,130.8 431.6,130.4 432.9,130.0 434.1,129.6 435.4,129.2 436.6,128.8 437.9,128.4 439.1,128.0 440.4,127.6 441.7,127.2 442.9,126.8 444.2,126.4 445.4,126.0 446.7,125.6 447.9,125.2 449.2,124.8 450.5,124.4 451.7,124.0 453.0,123.6 454.2,123.2 455.5,122.8 456.7,122.4 458.0,122.0 459.3,121.6 460.5,121.2 461.8,120.7 463.0,120.3 464.3,119.9 465.5,119.5 466.8,119.1 468.1,118.7 469.3,118.3 470.6,117.9 471.8,117.5 473.1,117.1 474.3,116.7 475.6,116.3 476.9,115.9 478.1,115.5 479.4,115.1 480.6,114.7 481.9,114.3 483.1,113.9 484.4,113.5 485.7,113.1 486.9,112.7 488.2,112.3 489.4,111.9 490.7,111.5 491.9,111.1 493.2,110.7 494.5,110.3 495.7,109.9 497.0,109.4 498.2,109.0 499.5,108.6 500.7,108.2 502.0,107.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <line x1="102.2" y1="262" x2="102.2" y2="36" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4 3" opacity="0.7"/>
  <line x1="169.3" y1="262" x2="169.3" y2="36" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4 3" opacity="0.7"/>
  <circle cx="124.9" cy="228.9" r="3" fill="currentColor"/>
  <circle cx="124.9" cy="222.5" r="3" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="212.9" cy="200.7" r="3" fill="currentColor"/>
  <circle cx="212.9" cy="189.4" r="3" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="259.5" cy="185.7" r="3" fill="currentColor"/>
  <circle cx="259.5" cy="166.9" r="3" fill="currentColor" fill-opacity="0.5"/>
  <circle cx="456.9" cy="122.3" r="3" fill="currentColor"/>
  <circle cx="456.9" cy="71.8" r="3" fill="currentColor" fill-opacity="0.5"/>
  <line x1="422" y1="44" x2="508" y2="44" stroke="currentColor" stroke-width="1.2" marker-end="url(#mr09durk)"/>
  <g font-size="11" fill="currentColor">
    <text x="62.0" y="278" text-anchor="middle" font-size="10">0</text>
    <text x="124.9" y="278" text-anchor="middle" font-size="10">0.5</text>
    <text x="187.7" y="278" text-anchor="middle" font-size="10">1</text>
    <text x="250.6" y="278" text-anchor="middle" font-size="10">1.5</text>
    <text x="313.4" y="278" text-anchor="middle" font-size="10">2</text>
    <text x="376.3" y="278" text-anchor="middle" font-size="10">2.5</text>
    <text x="439.1" y="278" text-anchor="middle" font-size="10">3</text>
    <text x="502.0" y="278" text-anchor="middle" font-size="10">3.5</text>
    <text x="55" y="266.0" text-anchor="end" font-size="10">0</text>
    <text x="55" y="233.7" text-anchor="end" font-size="10">1</text>
    <text x="55" y="201.4" text-anchor="end" font-size="10">2</text>
    <text x="55" y="169.1" text-anchor="end" font-size="10">3</text>
    <text x="55" y="136.9" text-anchor="end" font-size="10">4</text>
    <text x="55" y="104.6" text-anchor="end" font-size="10">5</text>
    <text x="55" y="72.3" text-anchor="end" font-size="10">6</text>
    <text x="55" y="40.0" text-anchor="end" font-size="10">7</text>
    <text x="282.0" y="294" text-anchor="middle">이동 크기 Δθ (rad)</text>
    <text x="8" y="20">소요 시간 (s)</text>
    <text x="414.0" y="152.1" text-anchor="middle">사다리꼴</text>
    <text x="388.9" y="96.6" text-anchor="end" opacity="0.8">가장 빠른 3차</text>
    <text x="102.2" y="30" text-anchor="middle" font-size="10">Δθ* = 0.32</text>
    <text x="169.3" y="30" text-anchor="middle" font-size="10">Δθ† = 0.853</text>
    <text x="135.8" y="104" text-anchor="middle" font-size="10" opacity="0.8">3차:</text>
    <text x="135.8" y="117" text-anchor="middle" font-size="10" opacity="0.8">가속도가</text>
    <text x="135.8" y="130" text-anchor="middle" font-size="10" opacity="0.8">걸림</text>
    <text x="175.3" y="110" font-size="10" opacity="0.8">3차: 속도가 걸림</text>
    <text x="418" y="48" text-anchor="end" font-size="10">새 구동계, Δθ† = 13.65 →</text>
    <text x="330" y="200" font-size="10" opacity="0.8">Δθ (rad)</text><text x="392" y="200" font-size="10" opacity="0.8">사다리꼴</text><text x="452" y="200" font-size="10" opacity="0.8">3차</text>
    <text x="330" y="215" font-size="10">0.5</text><text x="392" y="215" font-size="10">1.025 s</text><text x="452" y="215" font-size="10">1.225 s, 가속도</text>
    <text x="330" y="229" font-size="10">1.2</text><text x="392" y="229" font-size="10">1.900 s</text><text x="452" y="229" font-size="10">2.250 s, 속도</text>
    <text x="330" y="243" font-size="10">π/2</text><text x="392" y="243" font-size="10">2.363 s</text><text x="452" y="243" font-size="10">2.945 s, 속도</text>
    <text x="330" y="257" font-size="10">π</text><text x="392" y="257" font-size="10">4.327 s</text><text x="452" y="257" font-size="10">5.890 s, 속도</text>
  </g>
</svg>

P2의 고정 한계 $0.8\,\mathrm{rad/s}$, $2\,\mathrm{rad/s^2}$에서 관절 하나의 이동 크기에 대한 소요 시간이다. 사다리꼴(진한 선)과 합법적인 가장 빠른 3차(옅은 선)를 그렸고, 3차는 두 하한 $T_v = 1.5\Delta\theta/v_{\max}$와 $T_a = \sqrt{6\Delta\theta/a_{\max}}$(점선) 가운데 큰 쪽이다. $\Delta\theta^* = 0.32\,\mathrm{rad}$ 아래에서 사다리꼴은 순항을 잃고 삼각형이 되고, $\Delta\theta^\dagger = 0.853\,\mathrm{rad}$ 아래(음영)에서 3차는 가속도 구속, 그 위에서는 속도 구속이며, 표는 이 페이지의 네 이동을 적었다. 과제의 바뀐 구동계는 $\Delta\theta^\dagger$를 그림 밖의 $13.65\,\mathrm{rad}$으로 옮긴다.

### 1. 이 장을 목록 하나로

계획기는 시계가 없는 경로를 넘겨주고, 모터에는 두 한계 안에 머무는 시계가 필요하다. 이 절은 그 시계를 입히는 이 장의 도구 목록이다. 다항식 스케일링, 경유점, 시간 최적 스케일링이 있고, '대상으로 한 번 끝까지'가 쓴 두 대상은 §2–§3이 정의한다. 경로, 궤적, 시간 스케일링은 §2에서 함께 정의한다.

*한 문장으로:* 궤적은 경로에 시간 스케일링을 더한 것이고, 3차와 5차는 끝 조건으로 정해지는 다항식 스케일링이며, 액추에이터 한계 아래 가장 빠른 스케일링은 내내 그 한계를 타고 간다.

- **점대점 시간 스케일링**: 3차($s = 3t^2/T^2 - 2t^3/T^3$: 양 끝 속도 0)와 5차(양 끝
  가속도까지 0 — 토크가 더 매끄럽다); **사다리꼴** 속도 프로파일(가속–순항–감속) — 산업
  제어기가 실제로 도는 방식.
  - 5차의 숫자를 유도하면: $u = t/T$로 $s = 10u^3 - 15u^4 + 6u^5$이고, 양 끝에서 $s$, $\dot s$, $\ddot s$를($0, 0, 0$과 $1, 0, 0$으로) 고정하는 유일한 5차식이다. 그러면 $\dot s = (30/T)\,u^2(1-u)^2$은 $u = \tfrac12$에서 최대 $30/16 = 1.875/T$이고, $\ddot s = (60/T^2)\,u(1-u)(1-2u)$는 $1 - 6u + 6u^2 = 0$인 $u = \tfrac12 - \sqrt3/6 = 0.2113$에서 최대이며 그 값은 $(10/\sqrt3)/T^2 = 5.77/T^2$이다. 아래 계산 예제가 쓰는 두 계수가 이것이다.

> **3차와 5차 시간 스케일링의 정의.** **다항식 시간 스케일링**(polynomial time scaling)은 *$t$의 다항식인 시간 스케일링*(§2)이고, 만족하는 경계 조건 하나마다 계수가 하나씩이다(MR §9.2.2.1). **3차**는 넷을 만족한다. **양 끝** $s(0) = 0$, $s(T) = 1$과 **양 끝의 정지** $\dot s(0) = \dot s(T) = 0$이다. **5차**는 여섯을 만족한다. 그 넷에 **양 끝의 가속도 0**, 곧 $\ddot s(0) = \ddot s(T) = 0$을 더한다.
>
> $$s_3 = 3u^2 - 2u^3, \qquad s_5 = 10u^3 - 15u^4 + 6u^5, \qquad u = t/T$$
>
> 여기서 $u$는 정규화한 시간이라 $T$는 정해진 모양을 늘일 뿐이다. 계수는 경계 조건에서 하나씩 나오고, 최댓값은 3차가 $\dot s = 1.5/T$, $|\ddot s| = 6/T^2$, 5차가 $1.875/T$, $5.77/T^2$다.
>
> - **예**: 엘보 뒤집기. 3차는 $T = 5.890\,\mathrm{s}$가 필요하고, 속도 최댓값이 더 높은 5차는 $1.875\pi/0.8 = 7.363\,\mathrm{s}$가 필요하다. 둘 다 속도 구속이다.
> - **비예**: 선형 보간 $s = t/T$. 양 끝은 만족하지만 정지는 만족하지 않는다. $T = \pi/0.8 = 3.927\,\mathrm{s}$이면 $t = 0$에서 엘보 속도가 $0$에서 $0.8\,\mathrm{rad/s}$로 뛴다. 무한대의 가속도다. 3차는 그 도약을 없애지만 가속도의 도약, 곧 $t = 0$에서의 $0.543\,\mathrm{rad/s^2}$은 남긴다. 무한대의 저크(저크는 가속도의 변화율이다)이고, MR이 로봇을 떨게 할 수 있다고 경고하는 것이며, 5차가 없애는 것이 바로 이 도약이다.

- **경유점**: 중간 컨피규레이션을 지나는 경로. 10장이 찾은, 패널을 뚫지 않는 엘보 뒤집기는 $E = (135°,\ -45°)$를 지난다. 구간마다 정지에서 정지로 시간을 입히면 $E$까지 $(3\pi/4)/0.8 + 0.4 = 3.345\,\mathrm{s}$, 거기서 목표까지 $(\pi/4)/0.8 + 0.4 = 1.382\,\mathrm{s}$, 합해 $4.727\,\mathrm{s}$로, 직접 뒤집기의 $4.327\,\mathrm{s}$보다 길다. 패널을 뚫지 않는 값이다. $E$에서 멈추지 않고 지나가는 스플라인(경유점에서 매끄럽게 이어 붙인 다항식들)은 더 빠르지만, 가까운 경유점들을 지나는 스플라인은 그 사이에서 오버슈트할 수 있으므로 다른 스케일링처럼 최댓값을 한계와 견주어 확인해야 한다. [[04-robotics/capstone-panel-contact|26. 캡스톤]]의 3단계는 자기 구간들을 정지에서 정지로 시간을 입힌다.
- **시간 최적 스케일링**: 액추에이터 한계와
  [[04-robotics/modern-robotics/ch08-dynamics|동역학]]이 주어졌을 때 고정 경로 위에서 가장
  빠른 $s(t)$ 찾기 — 고전적 뱅뱅 구조(매 순간 경로 가속도가 최댓값이나 최솟값에 붙어 있고 그 사이 값은 쓰지 않는다 — 보통 최대 가속 후 최대 감속으로 전환)를 갖는 [[02-foundations/optimization|최적화]] 문제.
  - 관절 하나에 한계가 일정하면 이 구조는 두 줄로 보인다. 정지에서 출발해 정지로 끝나는 이동은 매 순간 $|\dot\theta(t)| \le \min(a_{\max}t,\ v_{\max},\ a_{\max}(T - t))$이므로, 시간 $T$ 동안 갈 수 있는 거리는 그 상한 아래의 넓이를 넘지 못한다. 그 넓이가 바로 '대상으로 한 번 끝까지'의 사다리꼴이고, 최대 가속, 한계에서의 순항, 최대 감속으로만 거기 닿는다. 그래서 이 한계에서 엘보 뒤집기의 $4.327\,\mathrm{s}$는 더 줄일 수 없다. 속도 한계를 없애면 상한이 삼각형이 되고, 순수 뱅뱅 뒤집기는 $2\sqrt{\pi/2} = 2.507\,\mathrm{s}$가 걸린다. 한계가 경로를 따라 바뀌는 일반 문제는 아래 메모가 세운다.

> [!note]- 더 깊이 · Deeper
> **시간 최적 스케일링의 정의.** **시간 최적 스케일링**(time-optimal time scaling)은 *최소화 문제의 해*다. 한 경로의 모든 시간 스케일링 가운데 가장 먼저 끝나는 것이다(MR §9.4). 세 조건이 문제를 세운다. **경로는 고정**이라 $s(t)$만 고른다. 운동은 **정지에서 정지로, 단조롭게** 간다. $s(0) = \dot s(0) = \dot s(T) = 0$, $s(T) = 1$, $\dot s \ge 0$이다. 그리고 **액추에이터 한계가 매 순간 지켜진다**. 토크(가속도) 한계는 경로 가속도의 범위 $L(s,\dot s) \le \ddot s \le U(s,\dot s)$가 되고(MR은 이것을 동역학을 거쳐 유도한다), 속도 한계는 경로 속도를 $\dot s \le \dot s_{\max}(s)$로 묶는다.
>
> $$T = \int_0^1 \frac{ds}{\dot s(s)} \ \to\ \min \quad \text{제약:} \quad L(s,\dot s) \le \ddot s \le U(s,\dot s),\ \ 0 \le \dot s \le \dot s_{\max}(s)$$
>
> 여기서 $\dot s(s)$는 경로의 각 지점에서의 경로 속도이고 $\dot s_{\max}(s)$는 그 상한이다(토크 한계만 있는 MR의 설정에서는 $L = U$가 되는 속도 한계 곡선). 시간은 $1/\dot s$의 적분이므로 최적해는 어디서나 이 범위가 허용하는 만큼 $\dot s$를 높게 유지한다(MR, 식 9.39 뒤). 엘보 뒤집기에서 이 페이지의 한계는 $|\ddot s| \le 2/\pi = 0.637\,\mathrm{1/s^2}$와 $\dot s \le 0.8/\pi = 0.255\,\mathrm{1/s}$를 주고, 최적해에 순항 구간을 넣는 것은 속도 상한이다.
>
> - **예**: 엘보 뒤집기의 $4.327\,\mathrm{s}$ 사다리꼴. 속도 한계가 없으면 뱅뱅 삼각형의 $2.507\,\mathrm{s}$.
> - **비예**: 한계까지 몰아붙인 3차, $5.890\,\mathrm{s}$. 가장 빠른 *3차*, 곧 정해진 한 모양 안에서의 최선의 $T$이고, 최적의 $1.361$배다. "시간 최적"은 한계를 밝혀야 한다. MR의 토크 한계 아래에서는 $L$과 $U$가 경로를 따라 바뀌고, 사다리꼴은 일반적으로 더 이상 최적이 아니다.

> [!example] 계산 예제 · Worked example
> 관절 하나가 $T = 2$ s 동안 $\Delta\theta = 1.2$ rad 움직인다. 단위 이동의 최댓값에 $\Delta\theta$를 곱한다:
> - **3차**: 최대 속도 $1.5 \cdot 1.2/2 = 0.9$ rad/s, 최대 가속도 $6 \cdot 1.2/2^2 = 1.8$ rad/s².
> - **5차**: 최대 속도 $1.875 \cdot 1.2/2 = 1.125$ rad/s, 최대 가속도 $5.77 \cdot 1.2/2^2 \approx 1.73$ rad/s².
>
> 이제 액추에이터 한계가 $v_{\max} = 0.8$ rad/s, $a_{\max} = 2$ rad/s²라 하고 **사다리꼴** 프로파일을 쓴다:
> - 가속: $v_{\max}/a_{\max} = 0.4$ s 동안 $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16$ rad 이동. 감속도 똑같이 0.4 s, 0.16 rad.
> - 순항: 남은 $1.2 - 0.32 = 0.88$ rad를 0.8 rad/s로 가는 데 $1.1$ s.
> - 합계: $0.4 + 1.1 + 0.4 = 1.9$ s — 2 s짜리 다항식 이동보다 빠르다.
>
> **어느 한계가 걸리는가**: 속도다. 두 다항식 모두 가속도는 $a_{\max}$ 아래지만(1.8, 1.73 < 2) 속도는 $v_{\max}$를 넘으므로(0.9, 1.125 > 0.8) $T = 2$ s로는 이 관절에서 실행할 수 없다. 사다리꼴은 구성상 $v_{\max}$에 딱 맞춘다.
>
> 실행 불가 주장은 곧 $0.9>0.8$이다. 그리고 시간 스케일링은 아무리 합법적이어도 도구가 패널에 닿은 뒤 얼마나 세게 누르는지에 대해서는 아무것도 말하지 않는다. 그것은 [[04-robotics/contact-force-tactile|9. 접촉]]의 질문이다.

### 2. 시간 스케일링의 정의

시간 입히기가 별개의 대상이라서, 액추에이터 한계 질문("이 모터가 할 수 있나?")은 기하를 건드리지 않고 여유 공간 질문("이 경로가 패널에 부딪히나?")은 타이밍을 건드리지 않는다. 둘을 섞는 것이 모터의 한계를 계획기 탓으로 돌리는 방식이다. 그 분리는 경로, 궤적, 시간 스케일링이라는 세 정의 위에 선다.

- **경로 vs 궤적**: 경로는 기하 $\theta(s), s\in[0,1]$; 궤적은 **시간 스케일링** $s(t)$를
  더한 것 — 모양과 타이밍을 독립적으로 설계하게 해주는 MR의 깔끔한 분리.

> **경로와 궤적의 정의.** **경로**(path)는 *매개변수에서 컨피규레이션으로 가는 사상* $\theta: [0,1] \to \mathcal{C}$이고, $\theta(0)$이 출발, $\theta(1)$이 목표다. 시간이 들어 있지 않은 기하다. **궤적**(trajectory)은 *시간에서 컨피규레이션으로 가는 사상*이고, 경로와 시간 스케일링 $s: [0,T] \to [0,1]$(아래), 정확히 두 부분을 합성한 것이다(MR §9.1).
>
> $$\theta(t) = \theta\big(s(t)\big), \qquad \theta(s) = \theta^{\text{start}} + s\,\big(\theta^{\text{goal}} - \theta^{\text{start}}\big),\ \ s \in [0, 1]$$
>
> 여기서 둘째 식은 이 페이지가 시간을 입히는 관절 공간의 직선이다. 두 부분은 합성에서만 만나므로 하나를 바꿔도 다른 하나는 그대로다.
>
> - **예**: 엘보 뒤집기는 타이밍과 상관없이 $\theta(0.5) = (45°,\ 0°)$를 지난다. 사다리꼴은 $t = 2.163\,\mathrm{s}$에, 3차는 $2.945\,\mathrm{s}$에 거기 닿는다. 경로 하나, 궤적 둘이다.
> - **비예**: 그 직선을 말단의 경로로 읽는 것. 관절 공간에서만 직선이다. 말단은 $(1,1)$에서 출발해 $(1,1)$로 돌아오지만 $s = 0.5$에서 패널 안 $0.414\,\mathrm{m}$인 $(1.414,\ 1.414)$을 지난다. 경로는 C-space의 곡선이므로, 그 위에서 도구가 하는 일은 이 페이지의 대상에 붙은 경고처럼 작업 영역에서 따로 확인해야 한다.

**시간 스케일링**은 *함수* $s: [0,T] \to [0,1]$이다. 경로도 궤적도 아니다. 정의 조건이 셋이고, 하나씩 빠질 때마다 구체적으로 무언가가 깨진다:

- **양 끝**: $s(0) = 0$, $s(T) = 1$. 출발점에서 출발해 목표에서 끝난다.
- **단조성**: $\dot s(t) \ge 0$. 로봇이 경로를 되짚지 않는다. 거꾸로 내려가는 스케일링은 다른 타이밍이 아니라 다른 경로다.
- **하드웨어가 요구하는 차수까지의 매끄러움**: 속도가 연속이려면 최소 $C^1$(도함수 하나가 연속), 토크가 연속이어야 하면 $C^2$(도함수 둘이 연속). 명령 토크가 [[04-robotics/modern-robotics/ch08-dynamics|8장]]의 $\tau = M(\theta)\ddot\theta + c + g$이고 $c$와 $g$는 상태에 따라 매끄럽게 변하므로, $\ddot\theta$가 튀면 $\tau$도 튀기 때문이다. 팔을 떨게 할 수 있는 토크 스파이크다([[02-foundations/signal-processing|신호처리]]의 주파수 렌즈가 적용된다).

궤적은 합성 $\theta(t) = \theta(s(t))$이고, 한 번·두 번 미분하면 이 페이지의 모든 계산이 쓰는 항등식 둘이 나온다:

$$\dot\theta(t) = \frac{d\theta}{ds}\,\dot s, \qquad \ddot\theta(t) = \frac{d\theta}{ds}\,\ddot s + \frac{d^2\theta}{ds^2}\,\dot s^2$$

관절 공간의 직선 경로에서는 $d^2\theta/ds^2 = 0$이라 둘째 항이 사라지고, 그래서 P2의 엘보 뒤집기가 $\ddot\theta_i = \Delta\theta_i\,\ddot s$로 줄어든다.

- **예**: 3차 $s = 3t^2/T^2 - 2t^3/T^3$. 조건을 확인하면 $s(0)=0$, $s(T)=1$, $\dot s = 6t/T^2 - 6t^2/T^3 = (6t/T^2)(1 - t/T) \ge 0$($[0,T]$ 위에서), 그리고 $\dot s(0) = \dot s(T) = 0$. $T = 5.8905\,\mathrm{s}$인 엘보 뒤집기에서는 $t = 2.945\,\mathrm{s}$에 $s = 0.5$에 닿고, 그때 엘보는 $0°$에서 최고 속도 $\pi \cdot 1.5/5.8905 = 0.8\,\mathrm{rad/s}$로 움직인다.
- **비예**: $s(t) = \sin(2\pi t/T)$. 매끄럽고 $0$에서 시작하지만 단조가 아니고 $s(T) = 0 \neq 1$이다. 출발점으로 돌아오므로 애초에 점대점 스케일링이 아니다.

### 3. 사다리꼴 프로파일의 정의

데이터시트는 숫자 둘, 최고 속도와 가속도를 준다. 사다리꼴은 파라미터 둘이 정확히 그 둘인 시간 스케일링이라, 한계에 맞춰 두기만 하면 아무것도 풀 필요가 없다. 산업 제어기가 이것을 돌리는 이유이자, 더 정교한 스케일링이 이겨야 하는 기준선인 이유다.

**사다리꼴 속도 프로파일**은 정지에서 출발해 정지로 끝나며 *속도* $\dot s$가 구간별 일차인 시간 스케일링이다. 구간은 셋 — 일정 가속, 일정 속도, 같은 크기의 일정 감속 — 이다(MR §9.2.2.2). 자유 파라미터는 순항 속도와 램프 가속도 둘이고, 이 페이지는 그것을 액추에이터 한계에 맞춰 엘보가 $\pm a_{\max}$로 가감속하고 $v_{\max}$로 순항하게 한다. 그래서 두 한계에 접근하는 것이 아니라 실제로 도달하며, MR은 이 선택을 그 한계 아래에서 가능한 가장 빠른 직선 운동으로 꼽는다. 그 이유는 §1의 넓이 논증이 보여 준다. 크기 $\Delta\theta$인 관절 이동에 적용하면 소요 시간은

$$T_{\text{trap}} = \frac{\Delta\theta}{v_{\max}} + \frac{v_{\max}}{a_{\max}} \qquad (\Delta\theta \ge \frac{v_{\max}^2}{a_{\max}}\text{일 때})$$

이다. 순항이 $\Delta\theta - v_{\max}^2/a_{\max}$를 속도 $v_{\max}$로 덮고 두 램프가 합쳐서 $v_{\max}/a_{\max}$를 쓰기 때문이다. 엘보로 확인하면 $3.1416/0.8 + 0.8/2 = 3.9270 + 0.4 = 4.327\,\mathrm{s}$, 위에서 길게 유도한 그 숫자다.

- **예**: P2의 엘보 뒤집기, $T_{\text{trap}} = 4.327\,\mathrm{s}$, 순항 $81.5\,\%$.
- **축퇴하는 경우이지 비예는 아닌 것**: $\Delta\theta < v_{\max}^2/a_{\max}$이면 순항 구간의 길이가 음수가 되어 프로파일이 **삼각형**으로 무너지고, 소요 시간은 $T_{\text{tri}} = 2\sqrt{\Delta\theta/a_{\max}}$, 최대 속도는 $v_{\max}$에 닿지 못하는 $a_{\max}T/2$다. 거기에 사다리꼴 공식을 쓰면 삼각형이 실제로 걸리는 것보다 *긴* 시간이 나오고, 이 계산이 틀리는 표준적인 방식이 그것이다.
- **비예**: 관절마다 제 한계에 맞춘 사다리꼴 하나씩. 어깨만 따로 보면 $2.363\,\mathrm{s}$에 끝나는데, 그때 $4.327\,\mathrm{s}$짜리 프로파일을 타는 엘보는 아직 목표에서 $1.411\,\mathrm{rad}$ 떨어져 있다. 관절들이 더 이상 하나의 $s(t)$를 공유하지 않으므로 팔은 관절 공간의 직선 경로를 벗어나고, 그 경로에서 한 여유 공간 검사는 이 운동을 더 이상 보장하지 않는다.
- **모양은 같아도 가장 빠르지는 않다**: 이 페이지의 프로파일에서 꼭대기만 $0.6\,v_{\max} = 0.48\,\mathrm{rad/s}$로 낮춘 것도 사다리꼴이지만, $3.1416/0.48 + 0.48/2 = 6.785\,\mathrm{s}$가 걸려 3차의 $5.890\,\mathrm{s}$보다도 길다. 빠름은 실루엣이 아니라 두 한계의 포화에서 나온다.
- **말단 한계가 아니라 관절 한계**: 두 숫자 모두 관절 한계이므로, 두 한계를 포화시키는 사다리꼴도 말단을 작업 공간의 속도 한계 너머로 몰 수 있다. [[04-robotics/capstone-panel-contact|26. 캡스톤 §3]]이 그것을 잡아 말단 속도 상한으로 고친다.

**위키 연결**: [[01-canonical-papers/notes/4-vla/act|행동 청크]]와
[[01-canonical-papers/notes/4-vla/diffusion-policy|노이즈 제거된 궤적]]은 정확히 이 장의 *학습된*
대체물이고, 실제 하드웨어에서는 안전/한계를 위해 고전적 시간 스케일링이 학습 출력을 여전히
감싼다.

### 스스로 점검

1. 3차 스케일링 $s(t) = 3t^2/T^2 - 2t^3/T^3$에서 $s(0), s(T), \dot s(0), \dot s(T)$를 계산해 경계 조건을 확인하라.
2. 5차 스케일링이 3차보다 나은 점은 무엇이고, 그 대가는 무엇인가?
3. 사다리꼴 속도 프로파일이 산업 제어기의 기본값인 실용적 이유는?
4. P2의 관절 하나가 이 페이지의 고정 한계로 $\Delta\theta = 0.5\,\mathrm{rad}$ 움직인다. 사다리꼴에 순항이 남는가, 가장 빠른 3차에는 어느 한계가 걸리는가, 두 소요 시간은 얼마인가?

> [!tip]- 정답
> 1. $s(0)=0$, $s(T)=1$이고 $\dot s = 6t/T^2 - 6t^2/T^3$이므로 $\dot s(0) = \dot s(T) = 0$이다. 양 끝에서 정지하며, 이것이 점대점 이동이 요구하는 조건 그대로다.
> 2. 5차는 양 끝의 *가속도*까지 0으로 만들어 끝에서 토크가 연속이다(덜컥거림이 없다). 대가는 같은 소요 시간에서 최대 속도가 커지는 것이다($1.875/T$ 대 $1.5/T$). 최대 *가속도*는 오히려 3차보다 작으므로($5.77/T^2$ 대 $6/T^2$) 치르는 것은 토크가 아니라 속도다.
> 3. 파라미터를 액추에이터 한계에 그대로 맞출 수 있기 때문이다. 최대 속도와 최대 가속도가 프로파일에 그대로 들어가므로 기계 사양이 아무것도 풀지 않고 1:1로 대응된다.
> 4. $0.5 > \Delta\theta^{*} = 0.32$이므로 사다리꼴에는 짧은 순항이 남는다. $T_{\text{trap}} = 0.5/0.8 + 0.4 = 0.625 + 0.4 = 1.025\,\mathrm{s}$이고 그중 $0.225\,\mathrm{s}$가 $v_{\max}$에서다. 그러나 $0.5 < \Delta\theta^{\dagger} = 0.853$이므로 3차는 가속도 구속이다. $T_a = \sqrt{6 \cdot 0.5/2} = \sqrt{1.5} = 1.225\,\mathrm{s}$가 $T_v = 1.5 \cdot 0.5/0.8 = 0.9375\,\mathrm{s}$보다 길고, $1.225\,\mathrm{s}$에서 최고 속도는 $1.5 \cdot 0.5/1.225 = 0.612\,\mathrm{rad/s}$뿐이다. 3차가 이제 가속도 선에만 닿고 속도 선에는 닿지 않는다 — '대상으로 한 번 끝까지'가 보여 주지 않은 유일한 경우다 — 그리고 사다리꼴의 $1.195$배가 걸린다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 장치는 같은 **P2**, 이동도 같은 엘보 뒤집기 $|\Delta\theta_2| = \pi\,\mathrm{rad}$이지만, 엘보에 더 빠르고 더 약한 다른 구동계를 단다. 그 계획 사양은 $v_{\max} = 1.6\,\mathrm{rad/s}$, $a_{\max} = 0.5\,\mathrm{rad/s^2}$로, 최고 속도는 두 배, 가속도는 4분의 1이다.

1. **그리기.** 새 한계에서 엘보에 대한 위의 그림. 그리기 전에 두 프로파일이 각각 어느 점선에 닿는지부터 정하라. 모양이 바뀌고, 한쪽은 구간 하나를 통째로 잃는다.
2. **유도.** (a) 사다리꼴: 먼저 $v_{\max}^2/a_{\max}$를 계산해 어떤 프로파일이 되는지 말하고, 소요 시간과 최대 속도를 구하라. (b) 3차: $T_v$와 $T_a$를 계산해 $T_{\text{cubic}}$과 걸리는 한계를 말하라. (c) 비 $T_{\text{cubic}}/T_{\text{trap}}$를 구하고, 이 조건에서 그 비가 $\Delta\theta$에도 $a_{\max}$에도 의존하지 않음을 보여라.
3. **해석.** 새 구동계는 최고 속도를 두 배로, 가속도를 4분의 1로 만들었다. 엘보 뒤집기는 빨라졌는가 느려졌는가, 고정 한계의 숫자 대비 얼마인가? 둘 중 어느 한계를 사는 것이 값어치가 있고, 교차점 $\Delta\theta^{\dagger}$는 그 답이 언제 뒤집히는지에 대해 무엇을 말하는가?

> [!note]- 그리는 법 · How to draw it
> - 시간축 하나를 공유하는 세 단에 엘보만 그린다. 위는 각 $\theta_2(t)$, 가운데는 속력 $|\dot\theta_2|$, 아래는 그 변화율 $d|\dot\theta_2|/dt$.
> - 한계부터, 지금 적용되는 값으로 가로 점선을 긋는다. 가운데 단에 $v_{\max}$, 아래 단에 $\pm a_{\max}$.
> - 위: 두 곡선 모두 $90°$에서 $-90°$로 내려간다. 사다리꼴은 가운데가 직선이고 양 끝이 포물선, 3차는 S자다. 각각 언제 도착하는지 표시한다.
> - 가운데: 사다리꼴은 올라가서 $v_{\max}$ 선 위를 평평하게 달리고 내려온다. 램프가 $v_{\max}$에 닿기 전에 이동이 끝나면 평평한 꼭대기는 없다. 3차는 중간에서 꼭짓점을 찍는 포물선 하나다.
> - 아래: 사다리꼴은 $+a_{\max}$와 $-a_{\max}$의 직사각형이고 사이는 0이다. 3차는 0을 지나 내려가는 직선 하나다. 각 프로파일의 최댓값을 옆에 적는다.
> - 프로파일이 한계에 붙어 있는 구간을 칠하고 그 길이를 적는다(위의 그림에서는 $v_{\max}$에 $3.527\,\mathrm{s}$).
> - 확인: 한계가 허용하는 만큼 빠르게 시간을 입힌 프로파일은 적어도 점선 하나에 닿는다. 어느 점선이냐가 이 그림이 말하는 전부다.

> [!tip]- 정답 · Solutions
> 1. 속도: 사다리꼴의 평평한 꼭대기가 사라지므로 가운데 단은 $1.2533\,\mathrm{rad/s}$에서 꼭짓점을 찍는 삼각형이고, 새 $v_{\max}$ 점선 $1.6$보다 아래다. 가속도: 이제 두 프로파일 모두 $a_{\max}$ 선에 붙는다. 삼각형은 양쪽 절반 내내 닿아 있고 3차는 양 끝점에서 닿는다.
> 2. (a) $v_{\max}^2/a_{\max} = 2.56/0.5 = 5.12\,\mathrm{rad} > \pi$이므로 최고 속도에 도달하기에는 이동이 짧고 프로파일은 **삼각형**이다. $T_{\text{tri}} = 2\sqrt{\pi/0.5} = 2 \times 2.5066 = 5.013\,\mathrm{s}$, 최대 속도 $a_{\max}T/2 = 0.5 \times 2.5066 = 1.2533\,\mathrm{rad/s}$로 $1.6$보다 여유 있게 아래다. (b) $T_v = 1.5\pi/1.6 = 2.945\,\mathrm{s}$, $T_a = \sqrt{6\pi/0.5} = 6.140\,\mathrm{s}$이므로 $T_{\text{cubic}} = 6.140\,\mathrm{s}$, **가속도**가 걸린다. 한계가 뒤바뀌었다. (c) $6.140/5.013 = 1.2247$. 두 프로파일이 모두 가속도 구속이면 소요 시간이 $2\sqrt{\Delta\theta/a_{\max}}$와 $\sqrt{6\Delta\theta/a_{\max}}$이고, 비는 $\sqrt{6}/2 = \sqrt{3/2} = 1.2247$로 $\Delta\theta$와 $a_{\max}$가 약분된다.
> 3. 둘 다 느려졌다. 사다리꼴은 $4.327$에서 $5.013\,\mathrm{s}$로 $+15.9\,\%$, 3차는 $5.890$에서 $6.140\,\mathrm{s}$로 $+4.2\,\%$. 여기서 최고 속도를 산 것은 소용이 없었다. 이동이 거기에 닿지 못하기 때문이다. 지킬 값어치가 있었던 것은 가속도다. 교차점이 그 시점을 말한다. $\Delta\theta^{\dagger} = \tfrac83 v_{\max}^2/a_{\max}$가 $0.853$에서 $13.65\,\mathrm{rad}$으로 올라가므로, 새 구동계에서는 $13.65\,\mathrm{rad}$보다 짧은 모든 이동이 가속도 구속이다. 최고 속도는 그 위에서야 값을 하기 시작하고, P2의 관절은 한 번의 이동으로 그만큼 가지 않는다.
