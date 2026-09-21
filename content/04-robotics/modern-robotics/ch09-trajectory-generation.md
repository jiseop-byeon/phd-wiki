---
title: "MR Ch.09 — Trajectory Generation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P2, time one named joint move with a trapezoidal and a cubic scaling, say which actuator limit binds each, and predict how the answer moves when the gearing changes."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.9** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> Differentiating polynomials ([[02-foundations/engineering-math|0.5 §1]]) and the idea of separating path from timing are all you need — the lightest chapter in the track. Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] carries the worked move.
> 다항식 미분([[02-foundations/engineering-math|0.5 §1]])과 경로/시간의 분리라는 아이디어만 있으면 된다 — 이 장은 트랙에서 가장 가벼운 장이다. 계산은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**로 한다.

## English

**Core question**: how do we turn "go from A to B" into a smooth, executable function of time?

### Running plant · 이 페이지의 장치

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]], and one named move on it: the **elbow flip** between the two configurations that put the tip on the panel target $(1,1)$, derived in [[04-robotics/modern-robotics/ch02-configuration-space|ch.2]].

$$\theta^{\text{start}} = (0°,\ 90°) \ \longrightarrow\ \theta^{\text{goal}} = (90°,\ -90°), \qquad \Delta\theta_1 = +\tfrac{\pi}{2} = 1.5708\ \mathrm{rad}, \quad \Delta\theta_2 = -\pi = -3.1416\ \mathrm{rad}$$

so the elbow travels exactly twice as far as the shoulder, which is the fact the whole page turns on. The **path** is the straight line between those two points of joint space, $\theta(s) = \theta^{\text{start}} + s\,\Delta\theta$ with $s \in [0,1]$; this page only chooses $s(t)$.

**Actuator limits, frozen here** (0.6 gives P2 geometry, not motors, so this page defines them and never changes them): every joint of P2 obeys

$$|\dot\theta_i| \le v_{\max} = 0.8\ \mathrm{rad/s}, \qquad |\ddot\theta_i| \le a_{\max} = 2\ \mathrm{rad/s^2}$$

which are the same two numbers the generic example in §1 already uses, now attached to the plant.

> [!warning] A time scaling is not a collision check · 시간 스케일링은 충돌 검사가 아니다
> This straight joint-space path is *not* collision-free against the panel: [[04-robotics/modern-robotics/ch10-motion-planning|ch.10]] shows it drives the arm $\sqrt{2}-1 = 0.414\,\mathrm{m}$ into the wall at its midpoint. Timing a path and clearing a path are different questions, and this chapter answers only the first.
> 이 직선 관절 경로는 패널에 대해 충돌이 없지 *않다*. [[04-robotics/modern-robotics/ch10-motion-planning|10장]]이 중간점에서 팔이 벽 안으로 $\sqrt{2}-1 = 0.414\,\mathrm{m}$ 들어감을 보인다. 경로에 시간을 입히는 것과 경로를 비우는 것은 다른 질문이고, 이 장은 앞의 것만 답한다.

### Homework diagram · 과제가 그릴 그림

One figure, three stacked panels sharing a horizontal time axis that runs from $0$ to $6\,\mathrm{s}$. Plot the **elbow** only.

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
    <text x="80" y="18" font-size="11" font-weight="bold">elbow θ₂ (deg)</text>
    <text x="137" y="124" font-size="11" text-anchor="end" font-weight="bold">speed |θ</text>
    <text x="137" y="124" font-size="11" font-weight="bold">₂| (rad/s)</text>
    <circle cx="134.1" cy="114.5" r="0.8" fill="currentColor"/>
    <text x="96" y="229" font-size="11" text-anchor="end" font-weight="bold">d|θ</text>
    <text x="96" y="229" font-size="11" font-weight="bold">₂|/dt (rad/s²)</text>
    <circle cx="93.1" cy="219.5" r="0.8" fill="currentColor"/>
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
    <text x="518.9" y="141.4" font-size="11" text-anchor="end">v<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">= 0.8</tspan></text>
    <text x="518.9" y="249" font-size="11" text-anchor="end">a<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">= 2</tspan></text>
    <text x="117.8" y="305" font-size="11">−a<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">= −2</tspan></text>
    <text x="243.4" y="198.2" font-size="11" text-anchor="middle">at v<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">for 3.527 s (81.5 % of the move)</tspan></text>
    <text x="97.1" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="392.3" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="126.9" y="273.3" font-size="11" opacity="0.8">cubic peak 0.543 rad/s² (27 % of a<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1">)</tspan></text>
    </g>
    <line x1="350" y1="14" x2="372" y2="14" stroke="currentColor" stroke-width="2.2"/>
    <text x="377" y="18" font-size="11" fill="currentColor">trapezoid</text>
    <line x1="450" y1="14" x2="472" y2="14" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <text x="477" y="18" font-size="11" fill="currentColor">cubic</text>
  </g>
</svg>

- **Top, $\theta_2(t)$.** Two curves from $90°$ down to $-90°$: the trapezoid's (straight in the middle, parabolic at both ends) and the cubic's (an S-curve). Mark where each one arrives.
- **Middle, the speed $|\dot\theta_2(t)|$.** Draw the limit $v_{\max} = 0.8\,\mathrm{rad/s}$ as a horizontal dashed line. The trapezoid is a trapezoid: a $0.4\,\mathrm{s}$ ramp up, a flat top *on* the dashed line, a $0.4\,\mathrm{s}$ ramp down. The cubic is a single parabola that just kisses the dashed line at its midpoint. Shade the trapezoid's flat top and label it with its duration.
- **Bottom, $d|\dot\theta_2|/dt$.** Draw $a_{\max} = 2\,\mathrm{rad/s^2}$ as a dashed line. The trapezoid is two rectangles, $+a_{\max}$ then $-a_{\max}$, with zero between — and it *touches* the dashed line. The cubic is a straight line falling from a small positive value through zero to its negative, nowhere near the dashed line. Write the cubic's peak next to it.

The figure's whole message is which dashed line each profile touches. The problem set asks for the same three panels after the joint is re-geared, and the answer changes which line is touched.

### Worked on the plant · 장치로 한 번 끝까지

Both joints ride one scaling $s(t)$, so joint $i$ has $\dot\theta_i = \Delta\theta_i\,\dot s$ and $\ddot\theta_i = \Delta\theta_i\,\ddot s$. Every peak is therefore proportional to $|\Delta\theta_i|$, and the joint with the largest $|\Delta\theta_i|$ hits its limit first. Here that is the elbow, at $|\Delta\theta_2| = \pi = 3.1416\,\mathrm{rad}$, exactly twice the shoulder. **Design the scaling for the elbow and the shoulder follows for free.**

**A — the trapezoid.** First decide whether a cruise phase exists at all. Ramping to $v_{\max}$ and straight back down covers $2 \cdot \tfrac12 a_{\max}t_a^2$ with $t_a = v_{\max}/a_{\max}$, i.e.

$$\Delta\theta^{*} = \frac{v_{\max}^2}{a_{\max}} = \frac{0.8^2}{2} = 0.32\ \mathrm{rad}$$

and since our $3.1416\,\mathrm{rad}$ is far above that, the profile is a true trapezoid rather than a triangle. Then:

- ramp time $t_a = v_{\max}/a_{\max} = 0.8/2 = 0.4\ \mathrm{s}$, covering $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16\ \mathrm{rad}$ on the way up and $0.16\,\mathrm{rad}$ on the way down;
- cruise distance $3.1416 - 0.32 = 2.8216\ \mathrm{rad}$, at $0.8\,\mathrm{rad/s}$, taking $2.8216/0.8 = 3.5270\ \mathrm{s}$;
- total $T_{\text{trap}} = 0.4 + 3.5270 + 0.4 = \mathbf{4.327\ s}$, of which the cruise is $3.5270/4.327 = 81.5\,\%$.

Check the shoulder, which rides the same $s(t)$ at half the amplitude: peak velocity $0.5 \times 0.8 = 0.4\,\mathrm{rad/s}$ and peak acceleration $0.5 \times 2 = 1\,\mathrm{rad/s^2}$. Both are at half their limits, so the shoulder is idle in the binding sense — it never constrains anything.

**B — the cubic, on the same move.** For $s(t) = 3t^2/T^2 - 2t^3/T^3$ the unit-move peaks are $\dot s_{\max} = 1.5/T$ at $t = T/2$ and $|\ddot s|_{\max} = 6/T^2$ at the two ends, so the elbow's peaks are $1.5\,\Delta\theta/T$ and $6\,\Delta\theta/T^2$. Invert each limit separately for the shortest admissible duration:

$$T_v = \frac{1.5\,\Delta\theta}{v_{\max}} = \frac{1.5 \times 3.1416}{0.8} = 5.8905\ \mathrm{s}, \qquad T_a = \sqrt{\frac{6\,\Delta\theta}{a_{\max}}} = \sqrt{\frac{6 \times 3.1416}{2}} = 3.0700\ \mathrm{s}$$

because a longer $T$ lowers both peaks, so each limit sets a floor and the move must satisfy the larger of the two. Here $T_v > T_a$, so $T_{\text{cubic}} = \mathbf{5.890\ s}$ and **velocity is the binding limit**. Confirm by back-substitution: at that duration the peak acceleration is $6 \times 3.1416/5.8905^2 = 0.543\,\mathrm{rad/s^2}$, only $27\,\%$ of $a_{\max}$ — the motor's torque is almost entirely unused.

**C — read the two against each other.** Force the cubic into the trapezoid's duration and it asks for $1.5 \times 3.1416/4.327 = 1.089\,\mathrm{rad/s}$, which is $36\,\%$ over $v_{\max}$: at $T = 4.327\,\mathrm{s}$ the cubic is simply not executable on this joint. Compare the two admissible durations instead:

$$\frac{T_{\text{cubic}}}{T_{\text{trap}}} = \frac{5.8905}{4.3270} = 1.361 \quad\Longrightarrow\quad \text{the trapezoid finishes } 26.5\,\% \text{ sooner}$$

and the reason is visible in the middle panel of the diagram: the trapezoid sits *at* $v_{\max}$ for $81.5\,\%$ of the move, while the cubic reaches $v_{\max}$ at one instant and is below it everywhere else. Spending the whole move at the limit is the entire advantage, and it is paid for with a discontinuous acceleration at the two corners.

**D — which limit binds, in general.** Setting $T_v = T_a$ and solving gives the crossover for a cubic:

$$\Delta\theta^{\dagger} = \frac{8}{3}\cdot\frac{v_{\max}^2}{a_{\max}} = \frac{8}{3}\cdot\frac{0.64}{2} = 0.853\ \mathrm{rad}$$

because $1.5\Delta\theta/v_{\max} = \sqrt{6\Delta\theta/a_{\max}}$ squares to $2.25\Delta\theta^2/v_{\max}^2 = 6\Delta\theta/a_{\max}$. Above $0.853\,\mathrm{rad}$ velocity binds; below it acceleration binds. Both moves on this page — the elbow's $3.1416$ and §1's $1.2$ — are above it, which is why both are velocity-bound. The problem set moves the plant to the other side of this line without changing $\Delta\theta$ at all.

### 1. The chapter in one list

- **Path vs trajectory**: a path is geometry $\theta(s), s\in[0,1]$; a trajectory adds
  **time scaling** $s(t)$ — MR's clean separation that lets you design shape and timing
  independently.
- **Point-to-point time scalings**: cubic ($s = 3t^2/T^2 - 2t^3/T^3$: zero endpoint
  velocities) and quintic (zero endpoint accelerations too — smoother torques);
  **trapezoidal** velocity profiles (accelerate–cruise–decelerate) — what industrial
  controllers actually run.
- **Via points**: interpolate through waypoints with splines — watch for overshoot between
  close points.
- **Time-optimal time scaling**: given actuator limits and the
  [[04-robotics/modern-robotics/ch08-dynamics|dynamics]], find the fastest $s(t)$ along a
  fixed path — an [[02-foundations/optimization|optimization]] problem with a classic
  bang-bang structure (at every instant the path acceleration sits at its maximum or its
  minimum, never in between — typically full acceleration, then a switch to full deceleration).
- Smoothness matters physically: discontinuous acceleration = torque spikes = vibration
  (the torque is $\tau = M(\theta)\ddot\theta + c + g$ from ch.8, and $c$, $g$ vary smoothly
  with the state, so a jump in $\ddot\theta$ is a jump in commanded torque)
  ([[02-foundations/signal-processing|signal processing]]'s frequency lens applies).

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
> The claim of infeasibility *is* $0.9>0.8$. A cubic on P2 that ignores contact still does not bound $F_n$ on a P3-stiffness wall.

### 2. Time scaling, defined

A **time scaling** is a *function* $s: [0,T] \to [0,1]$, not a path and not a trajectory. It has three defining conditions, and dropping any one of them breaks something specific:

- **Endpoints**: $s(0) = 0$ and $s(T) = 1$, so the move starts at the start and finishes at the goal.
- **Monotonicity**: $\dot s(t) \ge 0$, so the robot never retraces the path. A scaling that dips backwards is a different path, not a different timing.
- **Smoothness to the order the hardware needs**: at least $C^1$ so velocity is continuous; $C^2$ if torque must be continuous.

The trajectory is then the composition $\theta(t) = \theta(s(t))$, and differentiating it once and twice gives the two identities every calculation on this page uses:

$$\dot\theta(t) = \frac{d\theta}{ds}\,\dot s, \qquad \ddot\theta(t) = \frac{d\theta}{ds}\,\ddot s + \frac{d^2\theta}{ds^2}\,\dot s^2$$

where the second term vanishes for a straight-line path in joint space, because $d^2\theta/ds^2 = 0$ there, which is why P2's elbow flip reduces to $\ddot\theta_i = \Delta\theta_i\,\ddot s$.

- **Example**: the cubic $s = 3t^2/T^2 - 2t^3/T^3$. Check the conditions: $s(0)=0$, $s(T)=1$, $\dot s = 6t/T^2 - 6t^2/T^3 = (6t/T^2)(1 - t/T) \ge 0$ on $[0,T]$, and $\dot s(0) = \dot s(T) = 0$.
- **Non-example**: $s(t) = \sin(2\pi t/T)$. It is smooth and it starts at $0$, but it is not monotone and $s(T) = 0 \neq 1$ — it returns to the start, so it is not a point-to-point scaling at all.
- **Why it matters**: because the scaling is a separate object, an actuator-limit question ("can this motor do it?") never touches the geometry, and a clearance question ("does this path hit the panel?") never touches the timing. Mixing them is how a planner gets blamed for a motor's limits.

### 3. The trapezoidal profile, defined

A **trapezoidal velocity profile** is the time scaling whose *velocity* $\dot s$ is piecewise linear with three phases — constant acceleration $+a_{\max}$, constant velocity $v_{\max}$, constant deceleration $-a_{\max}$ — so that both actuator limits are attained rather than approached. Applied to a joint move of size $\Delta\theta$, its duration is

$$T_{\text{trap}} = \frac{\Delta\theta}{v_{\max}} + \frac{v_{\max}}{a_{\max}} \qquad \text{when } \Delta\theta \ge \frac{v_{\max}^2}{a_{\max}}$$

because the cruise covers $\Delta\theta - v_{\max}^2/a_{\max}$ at speed $v_{\max}$ while the two ramps take $v_{\max}/a_{\max}$ between them. Check it on the elbow: $3.1416/0.8 + 0.8/2 = 3.9270 + 0.4 = 4.327\,\mathrm{s}$, the number derived the long way above.

- **Example**: P2's elbow flip, $T_{\text{trap}} = 4.327\,\mathrm{s}$ with an $81.5\,\%$ cruise.
- **Degenerate case, not a non-example**: when $\Delta\theta < v_{\max}^2/a_{\max}$ the cruise phase has negative length, the profile collapses to a **triangle**, and the duration is $T_{\text{tri}} = 2\sqrt{\Delta\theta/a_{\max}}$ with a peak velocity $a_{\max}T/2$ that never reaches $v_{\max}$. Using the trapezoid formula there returns a *longer* time than the triangle takes, which is the standard way this calculation is got wrong.
- **Non-example**: a velocity profile that is trapezoidal in *shape* but whose top is at $0.6\,v_{\max}$. It is a perfectly legal time scaling and it is not the trapezoidal profile, because the defining property is saturation of both limits, not the silhouette.
- **Why it matters**: its two parameters *are* the machine's two spec numbers, so a datasheet maps onto it without solving anything. That is why industrial controllers run it and why it is the baseline any fancier scaling has to beat. Both are joint limits, though: a trapezoid that saturates them can still drive the tip past a task-space speed limit, which [[04-robotics/capstone-panel-contact|26. Capstone §3]] catches and repairs with a tip-speed cap.

**Wiki connections**: [[01-canonical-papers/notes/4-vla/act|action chunks]] and
[[01-canonical-papers/notes/4-vla/diffusion-policy|denoised trajectories]] are *learned*
replacements for exactly this chapter; classical time scaling still wraps learned outputs
on real hardware for safety/limits.

### Self-check

1. For the cubic scaling $s(t) = 3t^2/T^2 - 2t^3/T^3$, compute $s(0), s(T), \dot s(0), \dot s(T)$ and confirm the boundary conditions.
2. What does quintic scaling buy over cubic, and what does it cost?
3. Why is the trapezoidal velocity profile the industrial default?
4. P2's shoulder alone must move $\Delta\theta_1 = \pi/2$ with this page's frozen limits. Which limit binds, and what is the trapezoid's duration?

> [!tip]- Answers
> 1. $s(0)=0$, $s(T)=1$; $\dot s = 6t/T^2 - 6t^2/T^3$, so $\dot s(0) = \dot s(T) = 0$ — it starts and ends at rest, which is exactly the point-to-point requirement.
> 2. Quintic also zeroes the endpoint *accelerations*, so torque is continuous at the ends (no jolt). The cost is a higher peak velocity for the same duration ($1.875/T$ vs $1.5/T$) — note the peak *acceleration* is actually lower than cubic's ($5.77/T^2$ vs $6/T^2$), so it is speed, not torque, that you pay.
> 3. Its parameters *are* the actuator limits: maximum velocity and maximum acceleration appear directly in the profile, so a machine spec maps onto it one-to-one without solving anything.
> 4. $\Delta\theta_1 = 1.5708 > \Delta\theta^{*} = 0.32$, so it is still a true trapezoid, and $1.5708 > \Delta\theta^{\dagger} = 0.853$, so velocity binds. $T_{\text{trap}} = 1.5708/0.8 + 0.4 = 1.963 + 0.4 = 2.363\,\mathrm{s}$ — the $\Delta\theta/v_{\max}$ term is exactly half the elbow's, while the $v_{\max}/a_{\max}$ ramp term does not scale with the move at all.

### Problem set · 과제

Tier B. Using only this page, its prerequisites, and [[02-foundations/lab-plants|0.6]]. Same plant **P2** and the same elbow flip, $|\Delta\theta_2| = \pi\,\mathrm{rad}$, but the joint is re-geared: a taller gear ratio raises the top speed and cuts the torque, giving $v_{\max} = 1.6\,\mathrm{rad/s}$ and $a_{\max} = 0.5\,\mathrm{rad/s^2}$.

1. **Draw.** The same three stacked panels for the elbow under the new limits. Before drawing, decide which of the two dashed lines each profile touches now — the shapes change, and one of them loses a phase entirely.
2. **Derive.** (a) The trapezoid: evaluate $v_{\max}^2/a_{\max}$ first and say what kind of profile results, then give its duration and its peak velocity. (b) The cubic: compute $T_v$ and $T_a$, state $T_{\text{cubic}}$ and which limit binds. (c) The ratio $T_{\text{cubic}}/T_{\text{trap}}$, and show that under these conditions the ratio does not depend on $\Delta\theta$ or on $a_{\max}$ at all.
3. **Interpret.** The re-gearing doubled the top speed and quartered the acceleration. Did the elbow flip get faster or slower, and by how much against the frozen-limit numbers? Which of the two limits is worth buying, and what does the crossover $\Delta\theta^{\dagger}$ say about when that answer flips?

> [!tip]- Solutions
> 1. Velocity: the trapezoid's flat top disappears, so the middle panel shows a triangle peaking at $1.2533\,\mathrm{rad/s}$, below the new $v_{\max}$ dashed line at $1.6$. Acceleration: both profiles now press against the $a_{\max}$ line — the triangle touches it over both halves, and the cubic touches it at the two endpoints.
> 2. (a) $v_{\max}^2/a_{\max} = 2.56/0.5 = 5.12\,\mathrm{rad} > \pi$, so the move is too short to reach top speed and the profile is a **triangle**: $T_{\text{tri}} = 2\sqrt{\pi/0.5} = 2 \times 2.5066 = 5.013\,\mathrm{s}$, peak velocity $a_{\max}T/2 = 0.5 \times 2.5066 = 1.2533\,\mathrm{rad/s}$, comfortably under $1.6$. (b) $T_v = 1.5\pi/1.6 = 2.945\,\mathrm{s}$, $T_a = \sqrt{6\pi/0.5} = 6.140\,\mathrm{s}$, so $T_{\text{cubic}} = 6.140\,\mathrm{s}$ and **acceleration** binds — the limit has swapped. (c) $6.140/5.013 = 1.2247$. When both profiles are acceleration-bound the durations are $2\sqrt{\Delta\theta/a_{\max}}$ and $\sqrt{6\Delta\theta/a_{\max}}$, whose ratio is $\sqrt{6}/2 = \sqrt{3/2} = 1.2247$ with $\Delta\theta$ and $a_{\max}$ cancelling.
> 3. Slower, in both cases: $5.013$ against $4.327\,\mathrm{s}$ for the trapezoid ($+15.9\,\%$) and $6.140$ against $5.890\,\mathrm{s}$ for the cubic ($+4.2\,\%$). Buying top speed was worthless here because the move never reaches it; the acceleration is what was worth keeping. The crossover says when: $\Delta\theta^{\dagger} = \tfrac83 v_{\max}^2/a_{\max}$ rises from $0.853$ to $13.65\,\mathrm{rad}$, so under the new gearing every move shorter than $13.65\,\mathrm{rad}$ is acceleration-bound. Top speed only starts paying above that, and P2's joints never travel that far in one move.

## 한국어

**핵심 질문**: "A에서 B로 가라"를 매끄럽고 실행 가능한 시간 함수로 어떻게 바꾸는가?

### 이 페이지의 장치 · Running plant

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**, 그리고 그 위의 이름 붙은 이동 하나. 말단을 패널 목표 $(1,1)$에 두는 두 자세 사이의 **엘보 뒤집기**이며, 두 자세는 [[04-robotics/modern-robotics/ch02-configuration-space|2장]]에서 유도했다.

$$\theta^{\text{start}} = (0°,\ 90°) \ \longrightarrow\ \theta^{\text{goal}} = (90°,\ -90°), \qquad \Delta\theta_1 = +\tfrac{\pi}{2} = 1.5708\ \mathrm{rad}, \quad \Delta\theta_2 = -\pi = -3.1416\ \mathrm{rad}$$

이므로 엘보가 어깨보다 정확히 두 배 멀리 간다. 이 페이지 전체가 이 사실 위에서 돈다. **경로**는 관절 공간의 두 점을 잇는 직선 $\theta(s) = \theta^{\text{start}} + s\,\Delta\theta$, $s \in [0,1]$이고, 이 페이지는 $s(t)$만 고른다.

**여기서 고정하는 액추에이터 한계**(0.6은 P2의 기하를 주지 기구동을 주지 않으므로, 이 페이지가 정의하고 다시 바꾸지 않는다): P2의 모든 관절은

$$|\dot\theta_i| \le v_{\max} = 0.8\ \mathrm{rad/s}, \qquad |\ddot\theta_i| \le a_{\max} = 2\ \mathrm{rad/s^2}$$

를 지킨다. §1의 일반 예제가 이미 쓰던 그 두 숫자를 이제 장치에 붙인 것이다.

### 과제가 그릴 그림 · Homework diagram

그림 하나, 가로 시간축($0$부터 $6\,\mathrm{s}$)을 공유하는 세 단. **엘보**만 그린다.

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
    <text x="80" y="18" font-size="11" font-weight="bold">엘보 θ₂ (deg)</text>
    <text x="137" y="124" font-size="11" text-anchor="end" font-weight="bold">속력 |θ</text>
    <text x="137" y="124" font-size="11" font-weight="bold">₂| (rad/s)</text>
    <circle cx="134.1" cy="114.5" r="0.8" fill="currentColor"/>
    <text x="96" y="229" font-size="11" text-anchor="end" font-weight="bold">d|θ</text>
    <text x="96" y="229" font-size="11" font-weight="bold">₂|/dt (rad/s²)</text>
    <circle cx="93.1" cy="219.5" r="0.8" fill="currentColor"/>
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
    <text x="518.9" y="141.4" font-size="11" text-anchor="end">v<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">= 0.8</tspan></text>
    <text x="518.9" y="249" font-size="11" text-anchor="end">a<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">= 2</tspan></text>
    <text x="117.8" y="305" font-size="11">−a<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1" dx="3.3">= −2</tspan></text>
    <text x="243.4" y="198.2" font-size="11" text-anchor="middle">v<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1">에 3.527 s 붙어 있음 (이동의 81.5 %)</tspan></text>
    <text x="97.1" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="392.3" y="141.4" font-size="11" text-anchor="middle">0.4 s</text>
    <text x="126.9" y="273.3" font-size="11" opacity="0.8">3차 최댓값 0.543 rad/s² (a<tspan dy="3.1" font-size="8.6">max</tspan><tspan dy="-3.1">의 27 %)</tspan></text>
    </g>
    <line x1="350" y1="14" x2="372" y2="14" stroke="currentColor" stroke-width="2.2"/>
    <text x="377" y="18" font-size="11" fill="currentColor">사다리꼴</text>
    <line x1="450" y1="14" x2="472" y2="14" stroke="currentColor" stroke-width="2" stroke-opacity="0.5"/>
    <text x="477" y="18" font-size="11" fill="currentColor">3차</text>
  </g>
</svg>

- **위, $\theta_2(t)$.** $90°$에서 $-90°$로 내려가는 곡선 둘: 사다리꼴(가운데가 직선, 양 끝이 포물선)과 3차(S자). 각각 언제 도착하는지 표시한다.
- **가운데, 속력 $|\dot\theta_2(t)|$.** 한계 $v_{\max} = 0.8\,\mathrm{rad/s}$를 가로 점선으로 긋는다. 사다리꼴은 말 그대로 사다리꼴이다. $0.4\,\mathrm{s}$ 상승, 점선 *위에* 붙은 평평한 꼭대기, $0.4\,\mathrm{s}$ 하강. 3차는 중간에서 점선을 살짝 스치는 포물선 하나다. 사다리꼴의 평평한 부분을 칠하고 그 길이를 적는다.
- **아래, $d|\dot\theta_2|/dt$.** $a_{\max} = 2\,\mathrm{rad/s^2}$를 점선으로 긋는다. 사다리꼴은 직사각형 둘, $+a_{\max}$ 다음 $-a_{\max}$, 사이는 0이며 점선에 *닿는다*. 3차는 작은 양수에서 0을 지나 음수로 내려가는 직선이고 점선 근처에도 못 간다. 3차의 최댓값을 옆에 적는다.

이 그림이 말하려는 전부는 각 프로파일이 어느 점선에 닿느냐다. 과제는 관절의 기어비를 바꾼 뒤 같은 세 단을 요구하고, 답에서 닿는 점선이 바뀐다.

### 장치로 한 번 끝까지 · Worked on the plant

두 관절이 하나의 스케일링 $s(t)$를 타므로 관절 $i$는 $\dot\theta_i = \Delta\theta_i\,\dot s$, $\ddot\theta_i = \Delta\theta_i\,\ddot s$다. 따라서 모든 최댓값이 $|\Delta\theta_i|$에 비례하고, $|\Delta\theta_i|$가 가장 큰 관절이 먼저 한계에 닿는다. 여기서는 엘보이며 $|\Delta\theta_2| = \pi = 3.1416\,\mathrm{rad}$, 어깨의 정확히 두 배다. **엘보에 맞춰 스케일링을 설계하면 어깨는 저절로 따라온다.**

**A — 사다리꼴.** 먼저 순항 구간이 존재하는지부터 정한다. $v_{\max}$까지 올렸다가 곧바로 내리면 $t_a = v_{\max}/a_{\max}$일 때 $2 \cdot \tfrac12 a_{\max}t_a^2$를 이동하므로

$$\Delta\theta^{*} = \frac{v_{\max}^2}{a_{\max}} = \frac{0.8^2}{2} = 0.32\ \mathrm{rad}$$

이고, 우리의 $3.1416\,\mathrm{rad}$이 그보다 훨씬 크므로 삼각형이 아니라 진짜 사다리꼴이다. 그다음:

- 상승 시간 $t_a = v_{\max}/a_{\max} = 0.8/2 = 0.4\ \mathrm{s}$, 올라가며 $\tfrac12 \cdot 2 \cdot 0.4^2 = 0.16\ \mathrm{rad}$, 내려가며 $0.16\,\mathrm{rad}$;
- 순항 거리 $3.1416 - 0.32 = 2.8216\ \mathrm{rad}$, $0.8\,\mathrm{rad/s}$로 $2.8216/0.8 = 3.5270\ \mathrm{s}$;
- 합계 $T_{\text{trap}} = 0.4 + 3.5270 + 0.4 = \mathbf{4.327\ s}$, 그중 순항이 $3.5270/4.327 = 81.5\,\%$.

같은 $s(t)$를 절반 진폭으로 타는 어깨를 확인한다. 최대 속도 $0.5 \times 0.8 = 0.4\,\mathrm{rad/s}$, 최대 가속도 $0.5 \times 2 = 1\,\mathrm{rad/s^2}$. 둘 다 한계의 절반이라 어깨는 아무것도 구속하지 않는다.

**B — 같은 이동의 3차.** $s(t) = 3t^2/T^2 - 2t^3/T^3$의 단위 이동 최댓값은 $t = T/2$에서 $\dot s_{\max} = 1.5/T$, 양 끝에서 $|\ddot s|_{\max} = 6/T^2$이므로 엘보의 최댓값은 $1.5\,\Delta\theta/T$와 $6\,\Delta\theta/T^2$다. 두 한계를 각각 뒤집어 최소 허용 시간을 구한다:

$$T_v = \frac{1.5\,\Delta\theta}{v_{\max}} = \frac{1.5 \times 3.1416}{0.8} = 5.8905\ \mathrm{s}, \qquad T_a = \sqrt{\frac{6\,\Delta\theta}{a_{\max}}} = \sqrt{\frac{6 \times 3.1416}{2}} = 3.0700\ \mathrm{s}$$

$T$가 길어지면 두 최댓값이 모두 내려가므로 각 한계가 하한을 하나씩 주고 이동은 둘 중 큰 쪽을 만족해야 한다. 여기서는 $T_v > T_a$이므로 $T_{\text{cubic}} = \mathbf{5.890\ s}$, **속도가 걸리는 한계**다. 되대입해 확인하면 그 시간에서 최대 가속도는 $6 \times 3.1416/5.8905^2 = 0.543\,\mathrm{rad/s^2}$, $a_{\max}$의 $27\,\%$에 불과하다. 모터의 토크를 거의 쓰지 않는다.

**C — 둘을 맞대어 읽기.** 3차를 사다리꼴의 시간에 억지로 밀어 넣으면 $1.5 \times 3.1416/4.327 = 1.089\,\mathrm{rad/s}$를 요구하는데 이는 $v_{\max}$의 $36\,\%$ 초과다. $T = 4.327\,\mathrm{s}$에서 3차는 이 관절로 실행 자체가 불가능하다. 대신 각자 허용되는 시간끼리 비교한다:

$$\frac{T_{\text{cubic}}}{T_{\text{trap}}} = \frac{5.8905}{4.3270} = 1.361 \quad\Longrightarrow\quad \text{사다리꼴이 } 26.5\,\% \text{ 먼저 끝난다}$$

이유는 그림 가운데 단에 보인다. 사다리꼴은 이동의 $81.5\,\%$ 동안 $v_{\max}$에 *붙어* 있고, 3차는 한순간만 $v_{\max}$에 닿고 나머지는 그 아래다. 이동 내내 한계에 붙어 있는 것이 이득의 전부이며, 그 대가는 양 모서리의 불연속 가속도다.

**D — 일반적으로 어느 한계가 걸리는가.** $T_v = T_a$로 놓고 풀면 3차의 교차점이 나온다:

$$\Delta\theta^{\dagger} = \frac{8}{3}\cdot\frac{v_{\max}^2}{a_{\max}} = \frac{8}{3}\cdot\frac{0.64}{2} = 0.853\ \mathrm{rad}$$

$1.5\Delta\theta/v_{\max} = \sqrt{6\Delta\theta/a_{\max}}$를 제곱하면 $2.25\Delta\theta^2/v_{\max}^2 = 6\Delta\theta/a_{\max}$가 되기 때문이다. $0.853\,\mathrm{rad}$ 위에서는 속도가, 아래에서는 가속도가 걸린다. 이 페이지의 두 이동 — 엘보의 $3.1416$과 §1의 $1.2$ — 은 모두 그 위이고, 그래서 둘 다 속도 구속이다. 과제는 $\Delta\theta$를 전혀 건드리지 않고 장치를 이 선의 반대편으로 옮긴다.

### 1. 이 장을 목록 하나로

- **경로 vs 궤적**: 경로는 기하 $\theta(s), s\in[0,1]$; 궤적은 **시간 스케일링** $s(t)$를
  더한 것 — 모양과 타이밍을 독립적으로 설계하게 해주는 MR의 깔끔한 분리.
- **점대점 시간 스케일링**: 3차($s = 3t^2/T^2 - 2t^3/T^3$: 양 끝 속도 0)와 5차(양 끝
  가속도까지 0 — 토크가 더 매끄럽다); **사다리꼴** 속도 프로파일(가속–순항–감속) — 산업
  제어기가 실제로 도는 방식.
- **경유점**: 스플라인으로 웨이포인트들을 통과 — 가까운 점 사이의 오버슈트를 조심.
- **시간 최적 스케일링**: 액추에이터 한계와
  [[04-robotics/modern-robotics/ch08-dynamics|동역학]]이 주어졌을 때 고정 경로 위에서 가장
  빠른 $s(t)$ 찾기 — 고전적 뱅뱅 구조(매 순간 경로 가속도가 최댓값이나 최솟값에 붙어 있고 그 사이 값은 쓰지 않는다 — 보통 최대 가속 후 최대 감속으로 전환)를 갖는 [[02-foundations/optimization|최적화]] 문제.
- 매끄러움은 물리적으로 중요하다: 불연속 가속도 = 토크 스파이크 = 진동
  (8장의 토크는 $\tau = M(\theta)\ddot\theta + c + g$이고 $c$, $g$는 상태에 따라 매끄럽게
  변하므로, $\ddot\theta$가 튀면 명령 토크도 튄다)
  ([[02-foundations/signal-processing|신호처리]]의 주파수 렌즈가 적용된다).

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
> 실행 불가 주장은 곧 $0.9>0.8$이다. 접촉을 무시한 P2 3차는 P3 강성 벽의 $F_n$을 여전히 묶지 못한다.

### 2. 시간 스케일링의 정의

**시간 스케일링**은 *함수* $s: [0,T] \to [0,1]$이다. 경로도 궤적도 아니다. 정의 조건이 셋이고, 하나씩 빠질 때마다 구체적으로 무언가가 깨진다:

- **양 끝**: $s(0) = 0$, $s(T) = 1$. 출발점에서 출발해 목표에서 끝난다.
- **단조성**: $\dot s(t) \ge 0$. 로봇이 경로를 되짚지 않는다. 거꾸로 내려가는 스케일링은 다른 타이밍이 아니라 다른 경로다.
- **하드웨어가 요구하는 차수까지의 매끄러움**: 속도가 연속이려면 최소 $C^1$, 토크가 연속이어야 하면 $C^2$.

궤적은 합성 $\theta(t) = \theta(s(t))$이고, 한 번·두 번 미분하면 이 페이지의 모든 계산이 쓰는 항등식 둘이 나온다:

$$\dot\theta(t) = \frac{d\theta}{ds}\,\dot s, \qquad \ddot\theta(t) = \frac{d\theta}{ds}\,\ddot s + \frac{d^2\theta}{ds^2}\,\dot s^2$$

관절 공간의 직선 경로에서는 $d^2\theta/ds^2 = 0$이라 둘째 항이 사라지고, 그래서 P2의 엘보 뒤집기가 $\ddot\theta_i = \Delta\theta_i\,\ddot s$로 줄어든다.

- **예**: 3차 $s = 3t^2/T^2 - 2t^3/T^3$. 조건을 확인하면 $s(0)=0$, $s(T)=1$, $\dot s = 6t/T^2 - 6t^2/T^3 = (6t/T^2)(1 - t/T) \ge 0$($[0,T]$ 위에서), 그리고 $\dot s(0) = \dot s(T) = 0$.
- **반례**: $s(t) = \sin(2\pi t/T)$. 매끄럽고 $0$에서 시작하지만 단조가 아니고 $s(T) = 0 \neq 1$이다. 출발점으로 돌아오므로 애초에 점대점 스케일링이 아니다.
- **왜 중요한가**: 스케일링이 별개의 대상이라서, 액추에이터 한계 질문("이 모터가 할 수 있나?")이 기하를 건드리지 않고, 여유 공간 질문("이 경로가 패널에 부딪히나?")이 타이밍을 건드리지 않는다. 둘을 섞는 것이 모터의 한계를 계획기 탓으로 돌리는 방식이다.

### 3. 사다리꼴 프로파일의 정의

**사다리꼴 속도 프로파일**은 *속도* $\dot s$가 구간별 일차인 시간 스케일링이다. 구간은 셋 — 일정 가속 $+a_{\max}$, 일정 속도 $v_{\max}$, 일정 감속 $-a_{\max}$ — 이고, 두 액추에이터 한계에 접근하는 것이 아니라 실제로 도달한다. 크기 $\Delta\theta$인 관절 이동에 적용하면 소요 시간은

$$T_{\text{trap}} = \frac{\Delta\theta}{v_{\max}} + \frac{v_{\max}}{a_{\max}} \qquad (\Delta\theta \ge \frac{v_{\max}^2}{a_{\max}}\text{일 때})$$

이다. 순항이 $\Delta\theta - v_{\max}^2/a_{\max}$를 속도 $v_{\max}$로 덮고 두 램프가 합쳐서 $v_{\max}/a_{\max}$를 쓰기 때문이다. 엘보로 확인하면 $3.1416/0.8 + 0.8/2 = 3.9270 + 0.4 = 4.327\,\mathrm{s}$, 위에서 길게 유도한 그 숫자다.

- **예**: P2의 엘보 뒤집기, $T_{\text{trap}} = 4.327\,\mathrm{s}$, 순항 $81.5\,\%$.
- **축퇴하는 경우이지 반례는 아닌 것**: $\Delta\theta < v_{\max}^2/a_{\max}$이면 순항 구간의 길이가 음수가 되어 프로파일이 **삼각형**으로 무너지고, 소요 시간은 $T_{\text{tri}} = 2\sqrt{\Delta\theta/a_{\max}}$, 최대 속도는 $v_{\max}$에 닿지 못하는 $a_{\max}T/2$다. 거기에 사다리꼴 공식을 쓰면 삼각형이 실제로 걸리는 것보다 *긴* 시간이 나오고, 이 계산이 틀리는 표준적인 방식이 그것이다.
- **반례**: 모양은 사다리꼴인데 꼭대기가 $0.6\,v_{\max}$인 속도 프로파일. 완전히 합법적인 시간 스케일링이지만 사다리꼴 프로파일은 아니다. 정의하는 성질은 실루엣이 아니라 두 한계의 포화이기 때문이다.
- **왜 중요한가**: 파라미터 둘이 곧 기계 사양의 숫자 둘이라, 데이터시트가 아무것도 풀지 않고 그대로 대응된다. 산업 제어기가 이것을 돌리는 이유이자, 더 정교한 스케일링이 이겨야 하는 기준선인 이유다. 다만 둘 다 관절 한계다. 두 한계를 포화시키는 사다리꼴도 말단을 작업 공간의 속도 한계 너머로 몰 수 있고, [[04-robotics/capstone-panel-contact|26. 캡스톤 §3]]이 그것을 잡아 말단 속도 상한으로 고친다.

**위키 연결**: [[01-canonical-papers/notes/4-vla/act|행동 청크]]와
[[01-canonical-papers/notes/4-vla/diffusion-policy|노이즈 제거된 궤적]]은 정확히 이 장의 *학습된*
대체물이고, 실제 하드웨어에서는 안전/한계를 위해 고전적 시간 스케일링이 학습 출력을 여전히
감싼다.

### 스스로 점검

1. 3차 스케일링 $s(t) = 3t^2/T^2 - 2t^3/T^3$에서 $s(0), s(T), \dot s(0), \dot s(T)$를 계산해 경계 조건을 확인하라.
2. 5차 스케일링이 3차보다 나은 점은 무엇이고, 그 대가는 무엇인가?
3. 사다리꼴 속도 프로파일이 산업 제어기의 기본값인 실용적 이유는?
4. P2 어깨만 이 페이지의 고정 한계로 $\Delta\theta_1 = \pi/2$ 움직인다. 어느 한계가 걸리고, 사다리꼴 소요 시간은 얼마인가?

> [!tip]- 정답
> 1. $s(0)=0$, $s(T)=1$이고 $\dot s = 6t/T^2 - 6t^2/T^3$이므로 $\dot s(0) = \dot s(T) = 0$이다. 양 끝에서 정지하며, 이것이 점대점 이동이 요구하는 조건 그대로다.
> 2. 5차는 양 끝의 *가속도*까지 0으로 만들어 끝에서 토크가 연속이다(덜컥거림이 없다). 대가는 같은 소요 시간에서 최대 속도가 커지는 것이다($1.875/T$ 대 $1.5/T$). 최대 *가속도*는 오히려 3차보다 작으므로($5.77/T^2$ 대 $6/T^2$) 치르는 것은 토크가 아니라 속도다.
> 3. 파라미터가 곧 액추에이터 한계이기 때문이다. 최대 속도와 최대 가속도가 프로파일에 그대로 들어가므로 기계 사양이 아무것도 풀지 않고 1:1로 대응된다.
> 4. $\Delta\theta_1 = 1.5708$은 $\Delta\theta^{*} = 0.32$보다 크므로 여전히 진짜 사다리꼴이고, $\Delta\theta^{\dagger} = 0.853$보다도 크므로 속도가 걸린다. $T_{\text{trap}} = 1.5708/0.8 + 0.4 = 1.963 + 0.4 = 2.363\,\mathrm{s}$다. $\Delta\theta/v_{\max}$ 항만 엘보의 절반이고, 램프 항 $v_{\max}/a_{\max}$는 이동 크기와 아예 무관하다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6]]만 쓴다. 장치는 같은 **P2**, 이동도 같은 엘보 뒤집기 $|\Delta\theta_2| = \pi\,\mathrm{rad}$이지만 관절의 기어비를 바꾼다. 감속비를 낮춰 최고 속도를 올리고 토크를 깎아 $v_{\max} = 1.6\,\mathrm{rad/s}$, $a_{\max} = 0.5\,\mathrm{rad/s^2}$.

1. **그리기.** 새 한계에서 엘보의 같은 세 단. 그리기 전에 두 프로파일이 각각 어느 점선에 닿는지부터 정하라. 모양이 바뀌고, 한쪽은 구간 하나를 통째로 잃는다.
2. **유도.** (a) 사다리꼴: 먼저 $v_{\max}^2/a_{\max}$를 계산해 어떤 프로파일이 되는지 말하고, 소요 시간과 최대 속도를 구하라. (b) 3차: $T_v$와 $T_a$를 계산해 $T_{\text{cubic}}$과 걸리는 한계를 말하라. (c) 비 $T_{\text{cubic}}/T_{\text{trap}}$를 구하고, 이 조건에서 그 비가 $\Delta\theta$에도 $a_{\max}$에도 의존하지 않음을 보여라.
3. **해석.** 기어비 변경이 최고 속도를 두 배로, 가속도를 1/4로 만들었다. 엘보 뒤집기는 빨라졌는가 느려졌는가, 고정 한계의 숫자 대비 얼마인가? 둘 중 어느 한계를 사는 것이 값어치가 있고, 교차점 $\Delta\theta^{\dagger}$는 그 답이 언제 뒤집히는지에 대해 무엇을 말하는가?

> [!tip]- 정답 · Solutions
> 1. 속도: 사다리꼴의 평평한 꼭대기가 사라지므로 가운데 단은 $1.2533\,\mathrm{rad/s}$에서 꼭짓점을 찍는 삼각형이고, 새 $v_{\max}$ 점선 $1.6$보다 아래다. 가속도: 이제 두 프로파일 모두 $a_{\max}$ 선에 붙는다. 삼각형은 양쪽 절반 내내 닿아 있고 3차는 양 끝점에서 닿는다.
> 2. (a) $v_{\max}^2/a_{\max} = 2.56/0.5 = 5.12\,\mathrm{rad} > \pi$이므로 최고 속도에 도달하기에는 이동이 짧고 프로파일은 **삼각형**이다. $T_{\text{tri}} = 2\sqrt{\pi/0.5} = 2 \times 2.5066 = 5.013\,\mathrm{s}$, 최대 속도 $a_{\max}T/2 = 0.5 \times 2.5066 = 1.2533\,\mathrm{rad/s}$로 $1.6$보다 여유 있게 아래다. (b) $T_v = 1.5\pi/1.6 = 2.945\,\mathrm{s}$, $T_a = \sqrt{6\pi/0.5} = 6.140\,\mathrm{s}$이므로 $T_{\text{cubic}} = 6.140\,\mathrm{s}$, **가속도**가 걸린다. 한계가 뒤바뀌었다. (c) $6.140/5.013 = 1.2247$. 두 프로파일이 모두 가속도 구속이면 소요 시간이 $2\sqrt{\Delta\theta/a_{\max}}$와 $\sqrt{6\Delta\theta/a_{\max}}$이고, 비는 $\sqrt{6}/2 = \sqrt{3/2} = 1.2247$로 $\Delta\theta$와 $a_{\max}$가 약분된다.
> 3. 둘 다 느려졌다. 사다리꼴은 $4.327$에서 $5.013\,\mathrm{s}$로 $+15.9\,\%$, 3차는 $5.890$에서 $6.140\,\mathrm{s}$로 $+4.2\,\%$. 여기서 최고 속도를 산 것은 소용이 없었다. 이동이 거기에 닿지 못하기 때문이다. 지킬 값어치가 있었던 것은 가속도다. 교차점이 그 시점을 말한다. $\Delta\theta^{\dagger} = \tfrac83 v_{\max}^2/a_{\max}$가 $0.853$에서 $13.65\,\mathrm{rad}$으로 올라가므로, 새 기어비에서는 $13.65\,\mathrm{rad}$보다 짧은 모든 이동이 가속도 구속이다. 최고 속도는 그 위에서야 값을 하기 시작하고, P2의 관절은 한 번의 이동으로 그만큼 가지 않는다.
