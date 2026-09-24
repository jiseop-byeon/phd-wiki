---
title: "10. Imitating Contact: A Learned Policy Seats the Panel"
tags: [construction-robotics, manipulation, imitation-learning]
study-depth: Mastery
wiki-support: Working
depth-goal: "Carry a learned policy on S1 from demonstrations to a seated panel: say what behaviour cloning assumes and where the assumption breaks, price the break in millimetres and in seating probability, choose the action and the architecture that keep the policy inside the site's bounds, and say how many trials a success claim needs."
mastery-when: "Already raised: imitation learning for manipulation is a Mastery area of the study-depth guide, and this page teaches the dissertation sentence as one object, a learned policy run into the site tolerance."
---

> [!abstract] Depth target · 깊이 목표
> **Mastery** — the learning half of the research program, defended at the depth of its contact half: what a cloned policy assumes, what the assumption costs on S1, the construction track's facade-panel task ([[05-construction-robotics/site-engineering|2.5]]), in millimetres, and which fix pays for itself on a site.
> **Mastery** — 연구 프로그램의 학습 절반을 접촉 절반과 같은 깊이로 방어한다. 복제한 정책이 무엇을 가정하는지, 그 가정이 S1에서 몇 밀리미터의 값을 치르는지, 어떤 해법이 현장에서 제값을 하는지.

> [!note] Prerequisites · 선수 지식
> S1 at the pin, with its lead-in, its two stiffnesses and its capture arithmetic ([[05-construction-robotics/construction-manipulation|9]], its Worked case); the work package's phases and the evidence ladder ([[05-construction-robotics/site-engineering|2.5 §1, §5]]); behaviour cloning, covariate shift, compounding error and DAgger as first met ([[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]]); the corpus log and what demonstration data contains ([[04-robotics/teleoperation-demonstration|12. Teleoperation §6]] and its Worked case); target impedance ([[04-robotics/force-compliance-control|13. Force & Compliance §2]]) and the classical loop that switches to it before contact ([[04-robotics/capstone-panel-contact|26. Capstone §4]]); the residual policy ([[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §8]]); the stop chain, the hold and the one-way license ([[05-construction-robotics/hrc-worker-centered|6. HRC §6–§8]]); behaviour cloning's objective, chunking, success rates and action heads ([[03-deep-learning/vla/index|VLA §2–§4, §6]]); and the Wilson interval with the trial arithmetic ([[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]], its Worked case; [[06-research-practice/experimental-design-reproducibility|Experimental Design §4]]).
> 핀 앞의 S1, 그 리드인과 두 강성과 포착 계산([[05-construction-robotics/construction-manipulation|9]]의 계산 절). 작업 묶음의 단계와 증거 사다리([[05-construction-robotics/site-engineering|2.5 §1, §5]]). 처음 만난 모습의 행동 복제, 공변량 이동, 복합 오차, DAgger([[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]]). 코퍼스 기록과 시연 데이터가 담는 것([[04-robotics/teleoperation-demonstration|12. 원격조작 §6]]과 그 계산 절). 목표 임피던스([[04-robotics/force-compliance-control|13. 힘·컴플라이언스 §2]])와 접촉 전에 그리로 전환하는 고전 루프([[04-robotics/capstone-panel-contact|26. 캡스톤 §4]]). 잔차 정책([[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §8]]). 정지 사슬, 지지, 한 방향 허가([[05-construction-robotics/hrc-worker-centered|6. HRC §6–§8]]). 행동 복제의 목적함수, 청킹, 성공률, 행동 헤드([[03-deep-learning/vla/index|VLA §2–§4, §6]]). 그리고 Wilson 구간과 시행 수 계산([[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]의 계산 절, [[06-research-practice/experimental-design-reproducibility|실험 설계 §4]]).

## English

*The last page of the construction track. It stands on [[05-construction-robotics/construction-manipulation|9]], which priced S1 at the instant a hole meets its pin, and on [[04-robotics/teleoperation-demonstration|12]], which logged how demonstrations are made; the [[04-robotics/capstone-panel-contact|robotics capstone]] closed the classical loop on a panel, and this page runs a learned policy into the site tolerance.*

> [!note] Why this matters · 왜 배우는가
> In *"Install that panel on the frame"*, the worked instance of the physical-AI stack in [[07-research-program/index|7. Research Program §5]], this page is the learning half of "performs the fitting": the learning-and-adaptation layer brought down onto the contact step, where a policy learned from demonstrations seats the panel (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it a learned policy's promise is read off the wrong number: a cloned policy that errs on only $0.02$ of its states per step seats S1's panel with probability $0.98^{25}=0.603$, because an error in any of the first $25$ of the phase's $40$ steps drifts the hole off the demonstrations and past the pin's $4\,\mathrm{mm}$ lead-in — and nineteen seatings in twenty on a mock-up still leave a Wilson interval reaching down to $0.764$. It is block 7 of the dissertation path ([[07-research-program/index|7. Research Program §8]]), the last before an experiment, and it stands on every block before it, [[05-construction-robotics/construction-manipulation|9]]'s capture arithmetic and [[04-robotics/teleoperation-demonstration|12. Teleoperation §6]]'s demonstrations among them; running it for real needs a cluster to train on ([[02-foundations/tools/gpu-clusters|12.7 GPU Clusters]]) and a mock-up whose pin returns to the same place every trial ([[02-foundations/tools/mechanical-design-fabrication|12.9 §7]]). After it you can carry a learned policy from demonstrations to a seated panel and say, in millimetres and in seating probability, where it breaks and which fix pays for itself on a site.

> [!note] First pass · 처음이라면
> Read the Running object and look at the picture: S1's last 40 mm, the corridor the demonstrations covered, and what one error does to a cloned policy, to DAgger and to a residual on the classical base. Then §1–§3, for the task as a learning problem, what behaviour cloning assumes and the compounding error it causes in millimetres, and the Worked case after §8, which turns a per-step error of 0.02 into a seating probability of 0.603. §4–§7 choose the fixes — a head for two demonstrators, DAgger, the action, a bounded residual — and §8 and the §9 lab are for judging a claim.

### Running object · 이 페이지의 대상

**S1** from [[05-construction-robotics/site-engineering|2.5]] at the moment [[05-construction-robotics/construction-manipulation|9]] left it: the $20\,\mathrm{kg}$ facade panel above its bracket, each $18\,\mathrm{mm}$ hole about to drop over a $16\,\mathrm{mm}$ pin whose tapered nose captures a radial error of up to $4\,\mathrm{mm}$. Page 9 priced that instant with the hole wherever the error budget leaves it. This page follows the panel through the last $40\,\mathrm{mm}$ of its descent, where something has to keep correcting the hole while the panel is lowered, and asks whether a policy learned from demonstrations can be that something. The same seating is worked for every policy on the page; only who chooses the correction changes.

| Symbol | Value | What it is |
|---|---:|---|
| $r_c$, $K_d$, $K_{\text{stiff}}$, $W$ | $4\,\mathrm{mm}$; $500$ and $10^5\,\mathrm{N/m}$; $196\,\mathrm{N}$ | 9's lead-in, lateral target impedance, stiff loop and panel weight, unchanged |
| $\sigma_0$ | $1.35\,\mathrm{mm}$ per axis | the hole's offset when the phase starts: 9's budget, read as two-sigma bounds |
| phase | $40\,\mathrm{mm}$ at $10\,\mathrm{mm/s}$, $10\,\mathrm{Hz}$ | $T=40$ steps of $0.1\,\mathrm{s}$, one millimetre of descent each |
| $c$ | $0.2\,\mathrm{mm}$ per step along the wall | creep of base and arm while the panel is lowered; none toward the wall |
| $\sigma_w$ | $0.1\,\mathrm{mm}$ per step | sway, on each axis |
| $\sigma_v$ | $0.5\,\mathrm{mm}$ | the robot camera's error on the hole's offset: the policy's only view |
| operator | $u=-k_E\,(x+\nu)+\eta$, $k_E=0.5$, $\sigma_\nu=\sigma_\eta=0.1\,\mathrm{mm}$ | corrects half the offset seen in a close-up view the logger did not record, with hand noise |
| corpus | $120$ attempts, $96$ seated, $8$ discarded, $88$ usable, $4.0\,\mathrm{h}$; routes $-60$ and $+60\,\mathrm{mm}$, split $58/38$; $11$ with a recovery | S1's session, logged in 12's format and with 12's counts |
| $\epsilon$ | $0.02$ per step | the cloned policy's error rate on the operator's own states (§3); §9's fitted policy measures $0.0225$ |
| $k_0$, $B$ | $0.25$; $0.3\,\mathrm{mm}$ per step | the classical base's visual gain, and the bound on a learned residual (§7) |
| $F_{\lim}$ | $20\,\mathrm{N}$ | lateral force allowed at seating, about a tenth of $W$ |

The first row is 9's and S1's, and the corpus row takes 12's counts; every other number is this page's own and a course number, frozen so that each claim can be checked and not measured on any machine. The creep is chosen so that the phase cannot be flown open loop: uncorrected, it carries the hole $0.2\times40=8\,\mathrm{mm}$, twice the lead-in. The corpus reuses 12's counts so that 12's corpus metrics carry over unchanged: yield $88/120=0.733$, $164\,\mathrm{s}$ per usable demonstration, mode entropy $0.968$ bits over the two routes, and recovery coverage $11/88=0.125$ ([[04-robotics/teleoperation-demonstration|12. Teleoperation]], Worked case, Step 6).

*Scope: this page teaches imitation learning for one contact task end to end — the task as a learning problem, behaviour cloning and the compounding error it causes, two demonstrators averaged, DAgger, the choice of action, a residual bounded by the site, and how a success claim is judged — on S1's seating phase, with a NumPy lab. It does not teach how demonstrations are collected ([[04-robotics/teleoperation-demonstration|12]]), impedance control itself ([[04-robotics/force-compliance-control|13]]), the internals of generative action heads ([[03-deep-learning/diffusion/index|6. Diffusion & Flow]]), RL fine-tuning ([[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §4]]) or the separation distance ([[05-construction-robotics/hrc-worker-centered|6. HRC §6]]); it uses their results.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 360" style="max-width:100%;height:auto" role="img" aria-label="Offset of S1's hole along the wall against height above the pin tips over the last 40 mm. The demonstrations' band narrows from plus or minus 4 mm to between minus 0.12 and 0.92 mm. A cloned policy whose first error comes at 24 mm drifts 0.2 mm per step and reaches the pin 6.0 mm off, outside the 4 mm lead-in; one whose first error comes at 9 mm reaches it 3.0 mm off and seats, so it seats with probability 0.98 to the 25th, 0.603. DAgger takes the same error back; a residual on the base pushed by its bound every step settles at 2.0 mm.">
<text x="12" y="18" font-size="12" fill="currentColor" font-weight="600">S1’s last 40 mm: the hole’s offset along the wall while the panel is lowered</text>
<polygon points="50.0,89.0 60.2,124.5 70.5,141.4 80.8,148.5 91.0,151.0 101.2,151.6 111.5,151.7 121.8,151.7 132.0,151.6 142.2,151.6 152.5,151.6 162.8,151.6 173.0,151.6 183.2,151.6 193.5,151.6 203.8,151.6 214.0,151.6 224.2,151.6 234.5,151.6 244.8,151.6 255.0,151.6 265.2,151.6 275.5,151.6 285.8,151.6 296.0,151.6 306.2,151.6 316.5,151.6 326.8,151.6 337.0,151.6 347.2,151.6 357.5,151.6 367.8,151.6 378.0,151.6 388.2,151.6 398.5,151.6 408.8,151.6 419.0,151.6 429.2,151.6 439.5,151.6 449.8,151.6 460.0,151.6 460.0,172.4 449.8,172.4 439.5,172.4 429.2,172.4 419.0,172.4 408.8,172.4 398.5,172.4 388.2,172.4 378.0,172.4 367.8,172.4 357.5,172.4 347.2,172.4 337.0,172.4 326.8,172.4 316.5,172.4 306.2,172.4 296.0,172.4 285.8,172.4 275.5,172.4 265.2,172.4 255.0,172.4 244.8,172.4 234.5,172.4 224.2,172.4 214.0,172.4 203.8,172.4 193.5,172.4 183.2,172.4 173.0,172.4 162.8,172.4 152.5,172.4 142.2,172.4 132.0,172.4 121.8,172.5 111.5,172.6 101.2,172.9 91.0,174.0 80.8,177.5 70.5,186.6 60.2,207.5 50.0,251.0" fill="currentColor" fill-opacity="0.12" stroke="none"/>
<line x1="50.0" y1="170.0" x2="460.0" y2="170.0" stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="2 3"/>
<line x1="306.2" y1="38.0" x2="306.2" y2="260.0" stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="4 3"/>
<text x="383.1" y="44.0" font-size="10.5" fill="currentColor" text-anchor="middle">last 15 mm</text>
<polyline points="50.0,170.0 60.2,166.0 70.5,164.0 80.8,163.0 91.0,162.5 101.2,162.2 111.5,162.1 121.8,162.1 132.0,162.0 142.2,162.0 152.5,162.0 162.8,162.0 173.0,162.0 183.2,162.0 193.5,162.0 203.8,162.0 214.0,162.0 224.2,162.0 234.5,162.0 244.8,162.0 255.0,162.0 265.2,162.0 275.5,162.0 285.8,162.0 296.0,162.0 306.2,162.0 316.5,162.0 326.8,162.0 337.0,162.0 347.2,162.0 357.5,162.0 367.8,162.0 378.0,162.0 388.2,162.0 398.5,162.0 408.8,162.0 419.0,162.0 429.2,162.0 439.5,162.0 449.8,162.0 460.0,162.0" fill="none" stroke="currentColor" stroke-opacity="0.55" stroke-width="1"/>
<polyline points="50.0,170.0 60.2,160.0 70.5,152.5 80.8,146.9 91.0,142.7 101.2,139.5 111.5,137.1 121.8,135.3 132.0,134.0 142.2,133.0 152.5,132.3 162.8,131.7 173.0,131.3 183.2,131.0 193.5,130.7 203.8,130.5 214.0,130.4 224.2,130.3 234.5,130.2 244.8,130.2 255.0,130.1 265.2,130.1 275.5,130.1 285.8,130.1 296.0,130.0 306.2,130.0 316.5,130.0 326.8,130.0 337.0,130.0 347.2,130.0 357.5,130.0 367.8,130.0 378.0,130.0 388.2,130.0 398.5,130.0 408.8,130.0 419.0,130.0 429.2,130.0 439.5,130.0 449.8,130.0 460.0,130.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="1.5 3"/>
<polyline points="203.8,162.0 214.0,146.0 224.2,142.0 234.5,138.0 244.8,134.0 255.0,130.0 265.2,126.0 275.5,122.0 285.8,118.0 296.0,114.0 306.2,110.0 316.5,106.0 326.8,102.0 337.0,98.0 347.2,94.0 357.5,90.0 367.8,86.0 378.0,82.0 388.2,78.0 398.5,74.0 408.8,70.0 419.0,66.0 429.2,62.0 439.5,58.0 449.8,54.0 460.0,50.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
<polyline points="357.5,162.0 367.8,146.0 378.0,142.0 388.2,138.0 398.5,134.0 408.8,130.0 419.0,126.0 429.2,122.0 439.5,118.0 449.8,114.0 460.0,110.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
<polyline points="203.8,162.0 214.0,146.0 224.2,154.0 234.5,158.0 244.8,160.0 255.0,161.0 265.2,161.5 275.5,161.8 285.8,161.9 296.0,161.9 306.2,162.0 316.5,162.0 326.8,162.0 337.0,162.0 347.2,162.0 357.5,162.0 367.8,162.0 378.0,162.0 388.2,162.0 398.5,162.0 408.8,162.0 419.0,162.0 429.2,162.0 439.5,162.0 449.8,162.0 460.0,162.0" fill="none" stroke="currentColor" stroke-width="1.6"/>
<circle cx="214.0" cy="146.0" r="2.8" fill="currentColor"/>
<circle cx="367.8" cy="146.0" r="2.8" fill="currentColor"/>
<line x1="466.0" y1="90.0" x2="466.0" y2="250.0" stroke="currentColor" stroke-width="2.5"/>
<line x1="462.0" y1="90.0" x2="470.0" y2="90.0" stroke="currentColor" stroke-width="1.5"/>
<line x1="462.0" y1="250.0" x2="470.0" y2="250.0" stroke="currentColor" stroke-width="1.5"/>
<text x="474.0" y="54.0" font-size="10.5" fill="currentColor">6.0: misses</text>
<text x="474.0" y="94.0" font-size="10.5" fill="currentColor">lead-in ±4</text>
<text x="474.0" y="114.0" font-size="10.5" fill="currentColor">3.0: seats</text>
<text x="474.0" y="134.0" font-size="10.5" fill="currentColor">residual ≤ 2.0</text>
<text x="474.0" y="166.0" font-size="10.5" fill="currentColor">DAgger 0.4</text>
<text x="80.8" y="46.0" font-size="10.5" fill="currentColor">BC seats only if its first error falls</text>
<text x="80.8" y="60.0" font-size="10.5" fill="currentColor">in the last 15 mm: 0.98²⁵ = 0.603</text>
<line x1="50.0" y1="260.0" x2="460.0" y2="260.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="50.0" y1="260.0" x2="50.0" y2="30.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="50.0" y1="260.0" x2="50.0" y2="264.0" stroke="currentColor"/><text x="50.0" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">40</text>
<line x1="152.5" y1="260.0" x2="152.5" y2="264.0" stroke="currentColor"/><text x="152.5" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">30</text>
<line x1="255.0" y1="260.0" x2="255.0" y2="264.0" stroke="currentColor"/><text x="255.0" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<line x1="357.5" y1="260.0" x2="357.5" y2="264.0" stroke="currentColor"/><text x="357.5" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">10</text>
<line x1="460.0" y1="260.0" x2="460.0" y2="264.0" stroke="currentColor"/><text x="460.0" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="46.0" y1="250.0" x2="50.0" y2="250.0" stroke="currentColor"/><text x="43.0" y="254.0" font-size="10.5" fill="currentColor" text-anchor="end">-4</text>
<line x1="46.0" y1="210.0" x2="50.0" y2="210.0" stroke="currentColor"/><text x="43.0" y="214.0" font-size="10.5" fill="currentColor" text-anchor="end">-2</text>
<line x1="46.0" y1="170.0" x2="50.0" y2="170.0" stroke="currentColor"/><text x="43.0" y="174.0" font-size="10.5" fill="currentColor" text-anchor="end">0</text>
<line x1="46.0" y1="130.0" x2="50.0" y2="130.0" stroke="currentColor"/><text x="43.0" y="134.0" font-size="10.5" fill="currentColor" text-anchor="end">2</text>
<line x1="46.0" y1="90.0" x2="50.0" y2="90.0" stroke="currentColor"/><text x="43.0" y="94.0" font-size="10.5" fill="currentColor" text-anchor="end">4</text>
<line x1="46.0" y1="50.0" x2="50.0" y2="50.0" stroke="currentColor"/><text x="43.0" y="54.0" font-size="10.5" fill="currentColor" text-anchor="end">6</text>
<text x="43.0" y="28.0" font-size="10.5" fill="currentColor" text-anchor="end">mm</text>
<text x="255.0" y="290.0" font-size="10.5" fill="currentColor" text-anchor="middle">height above the pin tips (mm), one control step per millimetre</text>
<text x="12" y="308.0" font-size="10.5" fill="currentColor">shaded: where the 88 demonstrations keep the hole, mean ± 3σ (0.92 mm edge at the pin)</text>
<text x="12" y="322.0" font-size="10.5" fill="currentColor">dashed: cloned policy, first error at 24 mm and at 9 mm, adrift 0.2 mm a step</text>
<text x="12" y="336.0" font-size="10.5" fill="currentColor">solid: DAgger, the same error at 24 mm, taken back</text>
<text x="12" y="350.0" font-size="10.5" fill="currentColor">dotted: base + residual pushed by +B every step: never past 2.0 mm along the wall</text>
</svg>

S1's last $40\,\mathrm{mm}$, one control step per millimetre of descent. The shaded band is where the 88 demonstrations keep the hole, narrowing to an edge of $0.92\,\mathrm{mm}$ at the pin; a cloned policy that errs leaves it and, having never been shown those states, stops correcting, so the creep carries it $0.2\,\mathrm{mm}$ a step — an error at $24\,\mathrm{mm}$ reaches the pin $6.0\,\mathrm{mm}$ off and one at $9\,\mathrm{mm}$ $3.0\,\mathrm{mm}$ off, so it seats only if its first error falls in the last $15\,\mathrm{mm}$, with probability $0.98^{25}=0.603$. DAgger takes the same error back within a few steps, and a residual on the classical base, pushed by its bound on every step, never gets past $2.0\,\mathrm{mm}$ along the wall.

### 1. The seating task as a learning problem

*In one sentence:* the last $40\,\mathrm{mm}$ of S1 become an imitation-learning problem once five things are written down — what the policy sees, what it commands, how the hole moves, what counts as seated, and who demonstrated it.

**Where it sits.** [[05-construction-robotics/site-engineering|2.5 §1]] splits S1's work package into acquire, transport, align, hold and fasten, and verify. The seating is the end of *align*: its safe state is retreat and rescan, because no one is at the panel yet and a miss costs only time. The phase after it, hold and fasten, puts a worker's hands on the panel, which is why §7 ends with the worker and not with the pin.

**What the policy sees and commands.** It observes $o_t$, the robot camera's estimate of the hole's offset from its pin on each horizontal axis, and, once the nose touches, the wrist force (§6). It commands $u_t$, a correction of the lateral impedance target per step, rendered by the $500\,\mathrm{N/m}$ lateral impedance of [[04-robotics/force-compliance-control|13. §2]]. On each axis the hole then moves as

$$x_{t+1}=x_t+u_t+c+w_t,\qquad o_t=x_t+v_t,$$

because each step adds the command, the creep and the sway to where the hole was, while the camera reports where it is with an error: $x_t$ is the offset in millimetres, $c=0.2$ along the wall and $0$ toward it, $w_t$ the sway with $\sigma_w=0.1$ and $v_t$ the camera's error with $\sigma_v=0.5\,\mathrm{mm}$.

**What counts as seated.** Three conditions, and a policy must meet all of them:

$$S=\mathbb 1\big[r_T\le r_c\big]\cdot\mathbb 1\big[K\,r_T\le F_{\lim}\big]\cdot\mathbb 1\big[t_{\text{seat}}\le T\big],\qquad r_T=\sqrt{x_T^2+y_T^2},$$

since the hole must land inside the lead-in, the lead-in's correction must not push the building harder than $F_{\lim}=20\,\mathrm{N}$ through whatever stiffness $K$ holds the target, and the phase must end on time. Through the $500\,\mathrm{N/m}$ impedance the second condition is automatic, because a seating at the lead-in's edge costs $500\times0.004=2\,\mathrm{N}$; through a stiff $10^5\,\mathrm{N/m}$ loop it allows only $r_T\le0.2\,\mathrm{mm}$, which is §6's subject. The third fails a policy that stalls or retreats; the lab's descent never stops, so there it always holds.

**Who demonstrated it.** The operator corrects half of what a close-up view shows, $u=-0.5\,(x+\nu)+\eta$, and the log keeps the camera's offset and the command, not the view. The operator's closed loop settles where the correction cancels the creep, $m=(1-0.5)\,m+0.2$, so $m=0.4\,\mathrm{mm}$ along the wall, with a variance that solves the same balance,

$$s^2=\frac{k_E^2\sigma_\nu^2+\sigma_\eta^2+\sigma_w^2}{1-(1-k_E)^2}=\frac{0.0025+0.01+0.01}{0.75}=0.030,\qquad s=0.173\,\mathrm{mm},$$

so the operator's seatings sit within $0.4\pm3\times0.173=[-0.12,\ 0.92]\,\mathrm{mm}$ along the wall. That band, step by step, is the *demonstrated corridor*: the region the demonstrations cover, and the shaded band of the picture. Outside it a fitted policy has little or no data, which is what [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]] calls leaving the support. Without any correction the creep alone takes the hole $8\,\mathrm{mm}$; with the operator's it seats every time (§9: $1.000$, $95\%$ of seatings within $0.71\,\mathrm{mm}$). The question of the page is how much of that a policy fitted to the log keeps.

### 2. Behaviour cloning on contact

*In one sentence:* behaviour cloning fits the operator's commands as if every logged pair were an independent draw from the states the policy will meet, and a policy that acts meets neither condition.

> **Behaviour cloning, defined.** **Behaviour cloning** (BC) is a *training objective*: supervised regression of the demonstrator's command on what the policy observes. It is not an architecture, not a policy class and not imitation learning in general. Three defining conditions, the three of [[03-deep-learning/vla/index|VLA §2]] written here for contact. The data are **(observation, command) pairs a demonstrator produced**, so every label is a command, not a return and not a force the policy should feel. The loss is a **supervised discrepancy on the command alone**, fitted with no reward and without letting the policy act. And the average is taken **under the demonstrator's state distribution**, which is where the i.i.d. assumption of supervised learning enters: the fit treats the pairs as independent draws from the distribution the policy will be scored on.
>
> $$\hat\theta=\arg\min_\theta\ \frac1N\sum_{i=1}^{N}\big\lVert u_i-\pi_\theta(o_i)\big\rVert^2,\qquad (o_i,u_i)\sim d_{\pi^*}$$
>
> where $u_i$ is the operator's command, $o_i$ the logged camera offset, $\pi_\theta$ the policy and $d_{\pi^*}$ the distribution of states the operator's own seatings visit; the squared error is the Gaussian maximum likelihood of [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]], so nothing in it has seen a state the policy reached on its own.
>
> - **Example**: §9's table. The 88 seatings of 40 steps give $3{,}520$ pairs per axis, fitted by least squares on one indicator per cell of (step, $0.25\,\mathrm{mm}$ bin of the camera's offset). With indicator features the normal equations are diagonal, so each cell's command is the mean of the operator's commands that fell in it, and a cell nothing fell in returns $0$.
> - **Non-example**: the same table refitted after the operator has labelled states the *policy* reached. The loss is unchanged, but the distribution in condition three is the learner's; that is DAgger (§5), and it is a different algorithm with a different cost.
> - **Why it matters**: a loss on held-out demonstrations is condition three's number, the open-loop evaluation of [[02-foundations/ml-practice|9. ML Practice §5]]. The seating rate is the closed-loop number, and the whole page lives in the difference.

**How acting breaks the assumption.** Ross, Gordon and Bagnell open their paper with it: sequential prediction such as imitation learning, where future observations depend on earlier actions, violates the i.i.d. assumption of statistical learning. On S1 it breaks twice. The pairs are *not independent*: the 40 pairs of one seating share its start offset and its history of sway, and each state is the last one plus a command. And they are *not identically distributed* with what the policy meets: once it acts, its states come from its own distribution $d_\pi$, covariate shift in the sense of [[02-foundations/ml-practice|9. ML Practice §1]], where the inputs move while the right command for each state does not.

**What the log did not hold.** Contact adds a third break, the state-action consistency of [[04-robotics/teleoperation-demonstration|12. §6]]: the operator acted on a close-up view the log did not keep. Where the corpus is wide, the camera still predicts the command; where it is narrow, it hardly does. Late in the phase the true offset varies with $s^2=0.03$ while the camera adds $\sigma_v^2=0.25$, so the best prediction of the offset from the camera shrinks each reading by the share of its variance that is signal,

$$g=\frac{s^2}{s^2+\sigma_v^2}=\frac{0.03}{0.03+0.25}=0.107,$$

and the cloned correction is $0.5\times0.107=0.054$ per step where the operator's was $0.5$; early in the phase, where offsets spread $1.35\,\mathrm{mm}$, $g=0.879$ and the cloned gain is $0.44$. Read as a linear loop, the weak late gain leaves the cloned hole at the operator's $0.4\,\mathrm{mm}$ but spreads it $0.32\,\mathrm{mm}$ instead of $0.173$, past the corridor's $0.92\,\mathrm{mm}$ edge about $5\%$ of the time against the operator's $0.13\%$. The lab measures the consequence directly. Graded on the operator's own states, the fitted table gives a command the operator would not give — more than $3\sigma_\eta=0.3\,\mathrm{mm}$ from $-0.5x$ — on $0.0225$ of steps; graded on its own states, on $0.233$. A corpus in which the operator watches only the logged camera, so that the log holds everything the operator acted on, removes most of the problem: BC fitted to it seats $0.953$ against $0.875$ (§9).

### 3. Compounding error in millimetres

*In one sentence:* an error rate a cloned policy shows on the operator's states is multiplied by the horizon twice once the policy acts, because an error can leave it where it was never shown anything, and a learner trained where it goes pays it once.

> **Compounding error, defined.** **Compounding error** is a *property of a policy running in closed loop over a horizon*, not of its training loss: the growth of its expected cost with the horizon $T$ beyond what its per-step error on the demonstrator's states would predict. Three defining conditions. The **per-step error is measured on the demonstrator's distribution**, $\epsilon=E_{s\sim d_{\pi^*}}[\ell(s,\pi)]$, with $\ell$ the 0-1 loss of a command the demonstrator would not give. **Errors change the states that follow**, so the policy is scored on its own $d_\pi$. And the policy **has no data where errors take it**, outside the support of the demonstrations, so one error can be followed by more. Theorem 2.1 of Ross, Gordon and Bagnell, which they credit to Ross and Bagnell (2010), bounds a cloned policy's cost quadratically, and they note the bound is tight — some problems reach it, and the three conditions are the way there; their Theorem 3.2 bounds DAgger's linearly once it has run enough iterations:
>
> $$J(\pi)\le J(\pi^*)+T^2\epsilon\ \ \text{(BC)},\qquad J(\hat\pi)\le J(\pi^*)+u\,T\,\epsilon_N+O(1)\ \ \text{(DAgger)}$$
>
> where $J$ sums a per-step cost in $[0,1]$ over the $T$ steps, $\pi^*$ is the demonstrator, $\epsilon_N$ the smallest average per-step error any policy of the class reaches over the states the $N$ DAgger iterations visited, and $u$ bounds how much one wrong command raises the cost-to-go; so the quadratic is the price of the third condition, and a learner trained where it goes pays linearly.
>
> - **Example**: S1 with a cost of $1$ for each step spent outside the demonstrated corridor. The operator's $J(\pi^*)\approx0$: it leaves the $\pm3\sigma$ band on $0.27\%$ of steps, about $0.11$ step per seating. With $\epsilon=0.02$ and $T=40$, BC's bound is $T^2\epsilon=32$ of the $40$ steps adrift; DAgger's is $0.8$ if one takes $\epsilon_N=0.02$, ignores the $O(1)$ term and takes $u=1$, which holds for an error that leaves the hole within $1.44\,\mathrm{mm}$, since one operator step, $0.5x+0.2\le0.92$, brings it back into the corridor.
> - **Non-example**: an open-loop replay of the mean demonstration. Its error grows too, but it never looks at the state, so condition two fails; there is no distribution to shift, only a drift no data could fix.
> - **Why it matters**: the horizon becomes a design variable. Shortening the phase or chunking the commands (§4) cuts what the error compounds over, DAgger removes the square (§5), and a base that corrects everywhere removes condition three (§7).

**The worst case, on S1.** The theorem's worst case is a policy that, after its first error, never gets back. On S1 it has a physical form: outside the corridor the fitted table has nothing, so it stops correcting and the creep adds $0.2\,\mathrm{mm}$ a step. The hole leaves at the corridor's edge, $b=1\,\mathrm{mm}$ after rounding $0.92$ up, so the lead-in absorbs $(4-1)/0.2=15$ steps adrift. A first error at step $\tau$ leaves $N_{\text{off}}=T-\tau+1$ steps adrift, the error's own step included, and since that first error falls at step $\tau$ with probability $\epsilon(1-\epsilon)^{\tau-1}$,

$$E[N_{\text{off}}]=\sum_{\tau=1}^{T}\epsilon\,(1-\epsilon)^{\tau-1}\,(T-\tau+1)=12.84\ \text{steps},$$

or $12.84\times0.2=2.57\,\mathrm{mm}$ of expected drift, $86\%$ of the $3\,\mathrm{mm}$ the lead-in leaves. Its first-order form, $\epsilon T(T+1)/2=16.4$ steps, is the theorem's square in plain sight, and the bound itself is $32$ steps, which in the model, where each step adrift adds exactly $c$, is $6.4\,\mathrm{mm}$.

**The horizon.** Keeping the bound on the steps adrift inside the $15$ the lead-in absorbs needs $T^2\epsilon\le15$, so $T\le\sqrt{15/0.02}=27.4$ steps: the bound covers a $27\,\mathrm{mm}$ phase, not a $40\,\mathrm{mm}$ one. DAgger's $uT\epsilon_N\le15$, with the same $u=1$ and $\epsilon_N=0.02$ and its $O(1)$ term ignored, holds up to $T=750$ steps. Exactly, the expected steps adrift reach $15$ at $T=44$, so the $40$-step phase sits just inside the lead-in on average — and the average hides the tail. Seating needs the first error to come in the last $15$ steps, so its probability is $(1-\epsilon)^{T-15}$: $0.904$ for a $20\,\mathrm{mm}$ phase, $0.603$ for $40$, $0.403$ for $60$ and $0.269$ for $80$, falling below $0.9$ from $T=21$. The Worked case carries these through; §9 measures the fitted table's own two error rates, $0.0225$ on the operator's states and $0.233$ on its own, the theorem's two distributions made into numbers.

### 4. Two demonstrators, one mean

*In one sentence:* when the operators reach the bracket by two routes, a head that regresses the mean command drives between them, and a chunk does not change that unless the head can hold one route.

**Two routes.** Before the last $40\,\mathrm{mm}$, S1's corpus has the multimodality of 12's log. A scaffold tie crosses the straight line to the bracket, and the operators pass the panel's lower edge $60\,\mathrm{mm}$ to its left or its right, each through a gap of half-width $10\,\mathrm{mm}$; the 96 seated attempts split $58$ left and $38$ right. A unimodal head trained with squared error returns the conditional mean, because the mean is what minimizes squared error ([[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]], and [[03-deep-learning/vla/index|VLA §2]] for the same failure on D4, the deep-learning track's action chunk of [[03-deep-learning/lab-objects|0. Lab Objects]]):

$$\bar u=\frac{58\times(-60)+38\times60}{96}=-12.5\,\mathrm{mm},$$

$47.5\,\mathrm{mm}$ from the nearer route and $37.5\,\mathrm{mm}$ outside its gap — into the tie. It is not a worse version of either operator; it is neither. The corpus's mode entropy, $0.968$ bits, says the routes are nearly balanced, not that they are separable: balanced at $48/48$ the entropy reaches $1.000$ and the mean moves to $0\,\mathrm{mm}$, $60\,\mathrm{mm}$ from both ([[04-robotics/teleoperation-demonstration|12. §6]]).

**What a multimodal head changes.** A head that represents the distribution rather than its mean — tokens that are sampled, a denoiser, a decoder whose latent is sampled ([[03-deep-learning/vla/index|VLA §6]]) — puts mass $0.604$ on $-60$ and $0.396$ on $+60\,\mathrm{mm}$, and each sample is one route. Diffusion Policy's abstract names graceful handling of multimodal action distributions among the formulation's advantages ([[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]). But a head that re-decides at every step while the panel is still at the fork switches route between two consecutive decisions with probability $2\times0.604\times0.396=0.478$: it dithers in front of the tie. Once the panel is on one side, the camera itself says which route it is on and the ambiguity is gone; the danger is the decisions made at the fork.

**What a chunk changes.** A chunk commits several commands to one observation ([[03-deep-learning/vla/index|VLA §3]]). With a multimodal head, a chunk long enough to carry the panel past the tie commits the route; with a unimodal head, the chunk is the mean trajectory and still goes through the tie. [[01-canonical-papers/notes/4-vla/act|ACT]] trains its chunks as a CVAE so that the demonstrators' variability does not blur the fit, but at test time fixes the latent at zero, the prior's mean, and decodes deterministically: nothing picks a route at run time, and its temporal ensembling of overlapping chunks can, near a fork, average two routes back into the mean. Chunking also shortens the horizon of §3: if a chunk's error rate were a step's $0.02$, deciding every $5$ steps leaves $8$ decisions of which the first $5$ are fatal, $0.98^5=0.904$, and every $10$ steps leaves $4$ with the first $3$ fatal, $0.98^3=0.941$, against $0.603$ step by step. It is not quite a step's rate, because a chunk runs open loop: it must predict the creep, and it cannot see the sway, which over $10$ steps alone spreads $0.1\sqrt{10}=0.32\,\mathrm{mm}$.

### 5. DAgger on a site

*In one sentence:* DAgger lets the policy drive, has the operator say what they would have commanded in every state the policy reached, adds those labels to the corpus and refits — and on a site each round costs operator time and puts a learner's errors next to a real building.

> **DAgger, defined.** **DAgger** (dataset aggregation; Ross, Gordon and Bagnell, 2011) is an *iterative procedure for collecting data and training*, not a loss and not a policy class. Four defining conditions. At round $i$ the robot runs a **mixture** $\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i$ of the demonstrator and the current learner. The demonstrator **labels every state the mixture visited** with the command it would have given there, whether or not it was in control. The new pairs are **aggregated** with all earlier ones, never swapped for them. And the next learner is **trained on the aggregate**, with the same supervised loss as BC.
>
> $$\mathcal D\leftarrow\mathcal D\cup\big\{(o,\pi^*(s)):\ s\sim d_{\pi_i}\big\},\qquad \hat\pi_{i+1}=\arg\min_\pi\sum_{(o,u)\in\mathcal D}\big\lVert u-\pi(o)\big\rVert^2$$
>
> where $d_{\pi_i}$ is the distribution of states the mixture reaches, $o$ the logged observation of state $s$ and $\pi^*(s)$ the demonstrator's label; Ross et al. typically take $\beta_1=1$, so the first round is the demonstrations themselves, and offer $\beta_i=p^{i-1}$ or the parameter-free $\beta_i=\mathbb 1[i=1]$ for later rounds — so the training distribution is pulled toward the one the policy runs on.
>
> - **Example**: §9's rounds on S1. The 88 demonstrations are round zero; each round the current table makes $20$ seating attempts, the operator labels all $800$ states they visit with the command the close-up view calls for, and the table is refitted on everything so far. Two rounds take the seating rate from $0.875$ to $0.980$.
> - **Non-example**: $88$ more demonstrations. Their states still come from $d_{\pi^*}$, so condition two fails; §9 prices it: doubling the corpus gives $0.940$.
> - **Why it matters**: it removes the third condition of §3's box by buying the demonstrator's labels at the states the learner chose, and on a site that purchase has costs the algorithm does not show.

**What a round costs.** 12's log took $4.0\,\mathrm{h}$ for $120$ attempts: $120\,\mathrm{s}$ per attempt, and $164\,\mathrm{s}$ per usable demonstration once the discarded and failed ones are paid for. A DAgger attempt is labelled whether or not it seats — its failures are the labels it exists to collect — so it costs $120\,\mathrm{s}$, and a round of $20$ costs $40\,\mathrm{min}$. On §9's numbers:

| Operator time | Policy | Seats (§9) |
|---:|---|---:|
| $4.0\,\mathrm{h}$ | BC on the 88 demonstrations | $0.875$ |
| $4.7\,\mathrm{h}$ | one DAgger round | $0.950$ |
| $5.3\,\mathrm{h}$ | two rounds | $0.980$ |
| $6.7\,\mathrm{h}$ | four rounds | $0.995$ |
| $8.0\,\mathrm{h}$ | BC on 176 demonstrations | $0.940$ |
| $16.0\,\mathrm{h}$ | BC on 352 demonstrations | $0.960$ |

Two rounds, eighty minutes of attempts, buy more than twelve extra hours of demonstrations, because they are spent where the policy fails rather than where the operator never does. 12's recovery coverage, $11/88=0.125$, counts the recoveries operators happened to show; DAgger's labels are recoveries at the states this policy actually reaches.

**What the algorithm does not show.** First, the learner drives. The states DAgger needs are those the policy reaches by erring, and on S1 that is a $196\,\mathrm{N}$ panel off its corridor above a bracket bolted to the building: after one round, $5\%$ of the scored attempts still reached the pin more than $4\,\mathrm{mm}$ off. In align a miss is recoverable by retreat and rescan ([[05-construction-robotics/site-engineering|2.5 §1]]), and §7's bounds keep it so; rounds belong on the mock-up or behind those bounds. Second, the labels are given without control. Kelly et al.'s HG-DAgger starts from this: DAgger's sampling requires the expert to label without being fully in control, which can decrease safety and, with human experts, is likely to degrade the labels through perceived actuator lag. In their variant the novice drives until the expert judges it has entered an unsafe region, the expert then takes control and steers back, and labels are collected only during those recoveries, while the expert has uninterrupted control. On S1 plain DAgger has the operator label by moving a leader that does not move the panel — exactly the situation HG-DAgger avoids. Third, $\beta$: §9 uses the parameter-free schedule, the corpus as round zero and the learner alone afterwards.

### 6. What the action should be: position targets or impedance targets

*In one sentence:* a learned correction becomes a force through whatever holds the target, so the action decides whether a millimetre of error is a hundred newtons or half a newton, and it decides which force the demonstrations must have recorded.

> **Impedance target, defined.** An **impedance target** is an *action* that names where a virtual spring is anchored and how stiff it is, $a=(x_d,\,K)$, which a classical impedance controller then renders at its own rate ([[04-robotics/force-compliance-control|13. §2]]); it is not a pose the robot must reach. Three defining conditions. The policy **commands the anchor, not the pose**: where the tool ends up is settled by contact. The **stiffness is part of the action**, fixed or chosen by the policy, so the policy commands a relation between error and force. And a **controller below the policy closes the loop** at a rate the policy does not run at, so contact forces are shaped between the policy's decisions.
>
> $$F=K\,(x_d-x)$$
>
> where $x$ is where the tool is, $x_d$ the commanded anchor and $K$ the commanded stiffness, so an error in the anchor reaches the building as $K$ times itself, and the same millimetre is a different force under a different $K$.
>
> - **Example**: S1's lateral target at $K_d=500\,\mathrm{N/m}$. A hole the lead-in pushes $3.29\,\mathrm{mm}$ sideways costs $500\times0.00329=1.6\,\mathrm{N}$, and every seating inside the $4\,\mathrm{mm}$ lead-in stays under $2\,\mathrm{N}$.
> - **Non-example**: a position target into a stiff vendor loop. The policy's output looks the same, a pose, but the stiffness is the loop's $10^5\,\mathrm{N/m}$, so the same $3.29\,\mathrm{mm}$ costs $329\,\mathrm{N}$, $1.7$ times the panel's weight (9, Step 3).
> - **Why it matters**: [[04-robotics/force-compliance-control|13. §6]] argues that a learned layer should command compliance and leave its rendering to a classical loop; on S1 that becomes a number, because under the $20\,\mathrm{N}$ limit a stiff loop allows $0.2\,\mathrm{mm}$ at seating and the impedance allows the whole lead-in.

**Even the operator fails a stiff loop.** The operator's own seatings land within $0.71\,\mathrm{mm}$ $95\%$ of the time (§9), which through the stiff loop is $10^5\times0.00071=71\,\mathrm{N}$ and through the impedance $0.36\,\mathrm{N}$. Staying under $20\,\mathrm{N}$ stiffly needs $r_T\le0.2\,\mathrm{mm}$, and the creep alone centres the operator's offset at $0.4\,\mathrm{mm}$ along the wall. With position targets into a stiff loop, no policy on this page, the demonstrator included, meets condition two of §1 reliably; with impedance targets every seated policy does. §9 therefore scores every policy through the impedance.

**What the demonstrations must contain.** The seating is followed by the hold, and the hold ends with the panel's weight moving from the robot to its fasteners: the robot carries the $196\,\mathrm{N}$ while the worker fastens, and lets go only after the release test ([[05-construction-robotics/hrc-worker-centered|6. HRC §7]]). With the hold's vertical target stiffness, $K_z=10^4\,\mathrm{N/m}$, carrying $196\,\mathrm{N}$ puts the anchor $196.2/10^4=19.6\,\mathrm{mm}$ above the grip point; handing the load to the fastened panel moves the anchor down those $19.6\,\mathrm{mm}$ while the panel, now carried by its fasteners, does not move at all. A log of positions records nothing during the most consequential seconds of the task, and a policy cloned from positions learns to command where the tool was — which carries the weight forever. The anchor has to be recovered from force: $x_d=x+F/K$. DexForce does exactly this for a dexterous hand: from kinesthetic demonstrations with measured contact forces it computes force-informed targets, the observed fingertip position plus a hand-tuned parameter times the measured contact force, and reports $76\%$ average success over six tasks for policies trained on them against near-zero success for policies trained on the observed positions. So S1's log must hold the wrist force, or the operator's commanded anchor, synchronized with the pose ([[04-robotics/teleoperation-demonstration|12. §4.5]] on what an interface records and what it drops) — the action-space question [[04-robotics/force-compliance-control|13. §6]] says arrives twice, once for what the teleoperator commands and once for what the policy emits.

### 7. A learned residual, bounded by the site

*In one sentence:* keep the classical loop as the base, let the learned policy add a correction clipped to a bound the site sets, and let a worker's presence shrink that bound but never grow it.

**The base.** The robotics capstone estimates where the panel is, switches to impedance before contact and presses ([[04-robotics/capstone-panel-contact|26. §4]]), and it reads the panel only once ([[04-robotics/capstone-panel-contact|26. §7]]). Run every step on S1, the same loop moves the lateral target by a fixed share of what the camera shows, $u_0=-k_0\,o_t$ with $k_0=0.25$, through the $500\,\mathrm{N/m}$ impedance. It needs no demonstrations, and it corrects everywhere, including states no one demonstrated.

**The residual.** A residual policy, as [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §8]] defines it, keeps that base fixed and adds a learned correction clipped to a bound:

$$u_t=-k_0\,o_t+\operatorname{clip}\big(r_\phi(t,o_t),\,-B,\,B\big),$$

so whatever the correction outputs, the command stays within $B$ of a controller whose behaviour is known. Silver et al. and Johannink et al. both learn an unbounded correction on top of an existing controller, by reinforcement learning, and the clip is 7.5 Sim-to-Real §8's addition; here $r_\phi$ is fitted by the least squares of §2 to the operator's command minus the base's, on the same 88 demonstrations. The zero an empty cell returns is now the base's correction, not a runaway. That one change takes the same corpus and the same fit from $0.875$ to $1.000$ (§9).

**What the bound guarantees.** The worst a residual can do is push $+B$ on every step. The base pulls back by $k_0$ times the offset, and along the wall the creep adds $c$, so the mean offset settles where the pull balances the push:

$$\bar x_\infty=\frac{B+c}{k_0}=\frac{0.3+0.2}{0.25}=2.0\,\mathrm{mm},\qquad \bar y_\infty=\frac{B}{k_0}=\frac{0.3}{0.25}=1.2\,\mathrm{mm},$$

$2.33\,\mathrm{mm}$ from the pin whatever the network outputs, with the base loop's spread $\sqrt{(k_0^2\sigma_v^2+\sigma_w^2)/(1-(1-k_0)^2)}=0.242\,\mathrm{mm}$: $6.9$ standard deviations inside the lead-in. The base alone ($B=0$) settles at $c/k_0=0.8\,\mathrm{mm}$ and seats $1.000$ with $95\%$ of seatings within $1.24\,\mathrm{mm}$; the residual tightens that to $1.08\,\mathrm{mm}$. How large may $B$ be? Keeping the worst case four standard deviations inside the lead-in needs $\sqrt{((B+0.2)/0.25)^2+(B/0.25)^2}\le4-4\times0.242=3.03\,\mathrm{mm}$, so $B\le0.43\,\mathrm{mm}$ per step. As on the soil of S2, the construction track's trench task ([[05-construction-robotics/site-engineering|2.5]]), in 7.5 Sim-to-Real §8, one number trades what the residual may fix against how far a wrong one can take the hole.

**The worker.** The seating is the last step before hold and fasten, and a worker may reach in early to guide the panel. [[05-construction-robotics/hrc-worker-centered|6. HRC §8]] fixes what an estimate of the worker may do: the admissible set is computed from measured state with worst-case human terms, and an estimate may only select inside it. On S1, $B$ belongs to that set. When the tracker of [[05-construction-robotics/hrc-worker-centered|6. §6]] measures a person within reach of the panel, $B$ drops to $0$ and the seating finishes on the base alone, which §9 seats every time with $95\%$ within $1.24\,\mathrm{mm}$; tightening costs precision, not safety. An estimate that the worker is attentive may slow the descent or shrink $B$ further, and it may never raise $B$ above $0.3$. The bound is not a safety function — the stop chain of 6 §6 still owns the stop — but it keeps the policy's worst case inside what the safety functions assume. The impedance target of §6 is also the hold's own action: soft along the wall and stiff against gravity, as [[05-construction-robotics/hrc-worker-centered|6. §7]] sizes it.

### 8. Evaluating the claim

*In one sentence:* a seating rate is a count with an interval, a trained policy is one draw of a corpus, and the rung it was measured on decides which starts it has met.

**A count and its interval.** A success rate is $k$ successes in $n$ trials, and its uncertainty is the Wilson interval defined in [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]] (Worked case, Step 2), which never leaves $[0,1]$. §9's BC seats $1{,}750$ of $2{,}000$: $[0.860,\ 0.889]$. Nineteen of twenty on a mock-up gives $[0.764,\ 0.991]$, compatible with a failure rate of nearly one in four ([[03-deep-learning/vla/index|VLA §4]] reads ten-trial tables the same way).

**A clean run.** With no failures in $n$ trials, a failure rate $p$ is ruled out at $95\%$ once $(1-p)^n\le0.05$, so

$$n\ge\frac{\ln0.05}{\ln(1-p)},$$

because $(1-p)^n$ is the chance of $n$ straight successes at that rate: $23$ straight seatings rule out BC's $12.5\%$, $59$ rule out $5\%$, $124$ rule out 9's $2.4\%$, and $598$ rule out DAgger's $0.5\%$ ([[06-research-practice/experimental-design-reproducibility|Experimental Design §4]] gives the rule of three, $n\approx3/p$, for large $n$). Telling §9's BC from its fourth DAgger round at their own rates, $0.875$ against $0.995$, takes $65$ trials each before the two Wilson intervals separate.

**A policy is one draw of a corpus.** The interval above covers the rollouts of one trained policy. Refitting BC on five other corpora of 88 gives $0.817$ to $0.879$ (§9), a spread of $0.062$ against the interval's half-width of $0.015$; a seed captures only software randomness ([[06-research-practice/experimental-design-reproducibility|Experimental Design §4]]), and a claim about a method needs several corpora or seeds as well as many trials.

**The rung.** [[05-construction-robotics/site-engineering|2.5 §5]] ties each rung of the evidence ladder to the budget terms it measures, and the mock-up measures the arm, tool and part terms, and the map and base terms only against targets the lab arranged. On site the base term grows, and 9's site case puts the start at $2.66\,\mathrm{mm}$ per axis. Rescored from that start (§9), BC falls from $0.875$ to $0.656$ and the fourth DAgger round from $0.995$ to $0.848$, because both were taught on the mock-up's starts; the residual on the base stays at $1.000$. What a claim must also state is its counting rule — whether an attempt the operator rescued counts, and whether resets are timed ([[05-construction-robotics/site-engineering|2.5 §5]]) — and its force, since a seating that pushed $70\,\mathrm{N}$ into the bracket is not the seating of §1.

### Worked case · 대상으로 한 번 끝까지

One number trail on S1's last $40\,\mathrm{mm}$, from a per-step error to the probability of seating inside the $4\,\mathrm{mm}$ lead-in, for the cloned policy, for DAgger and for a residual on the classical base. It sits here because it uses §1's corridor, §3's worst case, §5's recovery and §7's bound. These are course computations on frozen numbers, not measurements: the problem set's Do item samples the same model, and §9's lab sets fitted policies against it.

**Step 1 — the corridor and the room left.** The operator's closed loop settles at $c/k_E=0.2/0.5=0.4\,\mathrm{mm}$ along the wall with $s=\sqrt{0.0225/0.75}=0.173\,\mathrm{mm}$ (§1), so its seatings keep within $0.4+3\times0.173=0.92\,\mathrm{mm}$, rounded up to an edge $b=1\,\mathrm{mm}$. A hole that leaves the corridor there and drifts $c$ per step reaches the lead-in's rim after

$$n_m=\frac{r_c-b}{c}=\frac{4-1}{0.2}=15\ \text{steps},$$

since each step adrift adds one creep to the offset: the lead-in absorbs fifteen steps adrift, the last $15\,\mathrm{mm}$ of descent.

**Step 2 — how often the phase is clean.** With $\epsilon=0.02$ on each of $40$ steps, a cloned seating contains no error with probability $0.98^{40}=0.446$, so more than half of all seatings contain at least one.

**Step 3 — the cloned policy, worst case.** After its first error it never returns (the third condition of §3). A first error at step $\tau$ leaves $41-\tau$ steps adrift, so it seats only if $41-\tau\le15$, that is if the first $25$ steps are clean:

$$P_{\text{BC}}=(1-\epsilon)^{T-n_m}=0.98^{25}=0.603,$$

because the model's steps err independently. The expected time adrift is $E[N_{\text{off}}]=12.84$ steps, $2.57\,\mathrm{mm}$ of drift, against Theorem 2.1's bound of $T^2\epsilon=32$ steps, $6.4\,\mathrm{mm}$ in the model.

**Step 4 — DAgger.** Take $\epsilon_N=0.02$, ignore the $O(1)$ term of Theorem 3.2, and let every error be taken back on the next step, $u=1$ — true of an error that leaves the hole within $1.44\,\mathrm{mm}$, since one operator step, $0.5x+0.2\le0.92$, returns it to the corridor, and the model's error leaves it at $1.2\,\mathrm{mm}$. The expected time outside the corridor is then $uT\epsilon_N=0.8$ steps, $0.16\,\mathrm{mm}$ of drift. §9's rounds err on $0.069$ to $0.158$ of their own states by its $0.3\,\mathrm{mm}$ test, so $\epsilon_N=0.02$ is this case's assumption, not a measurement. A miss would need the last $16$ steps all to be errors, $0.02^{16}=6.6\times10^{-28}$: $P_{\text{DAgger}}=1.000$ to any precision a trial could show.

**Step 5 — the residual on the base.** Whatever the residual outputs, its worst is $+B$ on every step, which settles at $(B+c)/k_0=2.0\,\mathrm{mm}$ along the wall and $B/k_0=1.2\,\mathrm{mm}$ toward it, $\sqrt{2.0^2+1.2^2}=2.33\,\mathrm{mm}$ from the pin. The base loop's spread is $0.242\,\mathrm{mm}$, so the lead-in's rim is $(4-2.33)/0.242=6.9$ standard deviations away: $P=1.000$, and a better residual only moves the hole closer.

**Step 6 — the force at seating.** Through the $500\,\mathrm{N/m}$ impedance, the residual's worst seating pushes $500\times0.00233=1.2\,\mathrm{N}$ sideways and the operator's $95$th-percentile seating, $0.71\,\mathrm{mm}$, pushes $0.36\,\mathrm{N}$; through a stiff $10^5\,\mathrm{N/m}$ loop the same two cost $233$ and $71\,\mathrm{N}$, against $F_{\lim}=20\,\mathrm{N}$.

**Step 7 — the horizon.** Longer phases compound: $P_{\text{BC}}=0.98^{T-15}$ is $0.904$ for $T=20$, $0.603$ for $40$, $0.403$ for $60$ and $0.269$ for $80$, while DAgger's stays at $1.000$ and the residual's worst case at $2.33\,\mathrm{mm}$. Theorem 2.1 keeps the expected steps adrift under the $15$ the lead-in absorbs only up to $T=27$; Theorem 3.2, on Step 4's assumptions, up to $T=750$.

**The reading this gives you.** Three numbers carry the page: $0.603$, a $2\%$ error compounded over a $40\,\mathrm{mm}$ phase; $1.000$, the same error learned back where it happens; and $2.33\,\mathrm{mm}$, the most a bounded residual can do. §9's fitted table errs at a measured $0.0225$ and still seats $0.875$, not the $0.566$ its measured rate gives in the worst case, because in the lab not every error is absorbing — the lab happens to sit inside the model's worst case.

### 9. Lab: BC, DAgger and a residual on S1's seating

Everything is frozen in the running object. The listing generates $352$ demonstrations from the operator (the corpus is the first $88$), fits the table of §2 by least squares, grades it on the operator's own states, and scores the operator, BC, four DAgger rounds, the base alone, BC as a residual and BC from a camera-logged corpus on $2{,}000$ seatings each, with Wilson intervals. It then sweeps the size of the corpus, rescores three policies from the site's start, and refits BC on five other corpora. Every learned policy meets the same $2{,}000$ starts and the same noise, seed $3$, so differences between its rows are the policies'. NumPy and the standard library only; it runs in under a second.

```python
import numpy as np

T, SIG0, RC = 40, 1.35, 4.0              # steps in the last 40 mm, start offset per axis (mm), lead-in (mm)
CREEP = np.array([0.2, 0.0])             # creep per step along the wall (x) and toward it (y), mm
SW, SV = 0.1, 0.5                        # sway per step, and the camera's error on the hole offset, mm
KE, SNU, SETA = 0.5, 0.1, 0.1            # operator: gain, error of the close-up view, hand noise (mm)
K0, B = 0.25, 0.3                        # the base's visual gain, and the residual's bound (mm per step)
BW, XMAX = 0.25, 12.0                    # the table: 0.25 mm bins over +-12 mm, one row per step
NB = int(2 * XMAX / BW)

def operator(t, o, x, rng):              # corrects half of what the close-up view shows, by hand
    return -KE * (x + rng.normal(0, SNU, x.shape)) + rng.normal(0, SETA, x.shape)

def operator_cam(t, o, x, rng):          # the same operator watching only the logged camera
    return -KE * o + rng.normal(0, SETA, o.shape)

def cells(t, o):                         # the table cell of each observed offset at step t
    return t * NB + np.clip(((o + XMAX) // BW).astype(int), 0, NB - 1)

def fit(data, target, n=None):           # least squares on one indicator per cell: the cell means
    tabs = []
    for a in (0, 1):                     # one table per axis
        c = np.concatenate([cells(t, o[:n, a]) for t, o, u in data])
        y = np.concatenate([target(o[:n], u[:n])[:, a] for t, o, u in data])
        tabs.append(np.bincount(c, y, T * NB) / (np.bincount(c, None, T * NB) + 1e-9))
    return tabs                          # a cell with no data returns 0: nothing was learned there

def table(tabs, t, o):
    return np.stack([tabs[a][cells(t, o[:, a])] for a in (0, 1)], axis=1)

def run(policy, n, seed, sig0=SIG0, labeler=None, grade=None):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, sig0, (n, 2)); data, miss = [], 0
    for t in range(T):
        o = x + rng.normal(0, SV, (n, 2))                    # the camera: the policy's only view
        u = policy(t, o, x, rng)
        g = u if grade is None else grade(t, o)              # the command being graded
        miss += np.sum(np.abs(g[:, 0] + KE * x[:, 0]) > 3 * SETA)   # one the operator would not give
        if labeler is not None:                              # log (step, camera, label)
            data.append((t, o, u if labeler is policy else labeler(t, o, x, rng)))
        x = x + u + CREEP + rng.normal(0, SW, (n, 2))
    return np.hypot(x[:, 0], x[:, 1]), data, miss / (n * T)

def wilson(k, n, z=1.96):
    p = k / n; mid = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return mid - half, mid + half

def row(name, r, eps=None, hours=None):
    k = int(np.sum(r <= RC)); lo, hi = wilson(k, r.size)
    extra = "" if eps is None else f"   mistakes {eps:.3f}   operator {hours:4.1f} h"
    print(f"{name:<16} seats {k / r.size:.3f} [{lo:.3f}, {hi:.3f}]   p95 {np.percentile(r, 95):5.2f} mm{extra}")

cloned = lambda tabs: (lambda t, o, x, rng: table(tabs, t, o))
resid = lambda tabs, b: (lambda t, o, x, rng: -K0 * o + np.clip(table(tabs, t, o), -b, b))
EVAL, DEMO_H, TRY_H = 2000, 164 / 3600, 120 / 3600    # rollouts per score; hours per demo, per attempt

_, corpus, _ = run(operator, 352, 1, labeler=operator)       # 352 demonstrations; the corpus is the first 88
bc = fit(corpus, lambda o, u: u, 88)
_, _, eps = run(operator, EVAL, 2, grade=lambda t, o: table(bc, t, o))
print(f"BC's mistakes on the operator's own states: {eps:.4f}")
r, _, e = run(operator, EVAL, 3); row("operator", r, e, 0.0)
r, _, e = run(cloned(bc), EVAL, 3); row("BC, 88 demos", r, e, 88 * DEMO_H)
data, tabs = [(t, o[:88], u[:88]) for t, o, u in corpus], bc
for k in range(1, 5):                                         # DAgger: 20 attempts by the policy, relabeled
    _, new, _ = run(cloned(tabs), 20, 100 + k, labeler=operator)
    data += new; tabs = fit(data, lambda o, u: u)
    r, _, e = run(cloned(tabs), EVAL, 3); row(f"DAgger round {k}", r, e, 88 * DEMO_H + 20 * k * TRY_H)
dag = tabs
res = fit(corpus, lambda o, u: u + K0 * o, 88)               # the residual learns operator minus base
row("base alone", run(resid(res, 0.0), EVAL, 3)[0])
row("BC as residual", run(resid(res, B), EVAL, 3)[0])
_, cam, _ = run(operator_cam, 88, 5, labeler=operator_cam)    # a corpus logged from what the operator saw
row("BC, camera log", run(cloned(fit(cam, lambda o, u: u)), EVAL, 3)[0])
print("BC alone against the size of the corpus:")
for n in (22, 44, 88, 176, 352):
    r, _, e = run(cloned(fit(corpus, lambda o, u: u, n)), EVAL, 3); row(f"  {n} demos", r, e, n * DEMO_H)
print("the same policies from the site's start, 2.66 mm per axis:")
for name, pol in (("BC, 88 demos", cloned(bc)), ("DAgger round 4", cloned(dag)), ("BC as residual", resid(res, B))):
    row(name, run(pol, EVAL, 4, sig0=2.66)[0])
seats = [np.mean(run(cloned(fit(run(operator, 88, s, labeler=operator)[1], lambda o, u: u)), EVAL, 3)[0] <= RC)
         for s in (11, 21, 31, 41, 51)]
print("BC from five other corpora of 88:", " ".join(f"{p:.3f}" for p in seats))
```

It prints, first, BC's mistakes on the operator's own states, $0.0225$, and then:

| Policy | Seats | 95% Wilson | 95% of seatings within | Mistakes on its own states | Operator time |
|---|---:|---|---:|---:|---:|
| operator | $1.000$ | $[0.998,\ 1.000]$ | $0.71\,\mathrm{mm}$ | $0.007$ | — |
| BC, 88 demonstrations | $0.875$ | $[0.860,\ 0.889]$ | $7.28\,\mathrm{mm}$ | $0.233$ | $4.0\,\mathrm{h}$ |
| DAgger, round 1 | $0.950$ | $[0.939,\ 0.958]$ | $4.03\,\mathrm{mm}$ | $0.158$ | $4.7\,\mathrm{h}$ |
| DAgger, round 2 | $0.980$ | $[0.973,\ 0.985]$ | $1.14\,\mathrm{mm}$ | $0.093$ | $5.3\,\mathrm{h}$ |
| DAgger, round 3 | $0.981$ | $[0.974,\ 0.986]$ | $1.14\,\mathrm{mm}$ | $0.086$ | $6.0\,\mathrm{h}$ |
| DAgger, round 4 | $0.995$ | $[0.991,\ 0.997]$ | $0.99\,\mathrm{mm}$ | $0.069$ | $6.7\,\mathrm{h}$ |
| base alone | $1.000$ | $[0.998,\ 1.000]$ | $1.24\,\mathrm{mm}$ | | |
| BC as residual | $1.000$ | $[0.998,\ 1.000]$ | $1.08\,\mathrm{mm}$ | | |
| BC, camera-logged corpus | $0.953$ | $[0.943,\ 0.961]$ | $3.87\,\mathrm{mm}$ | | |

The sweep over the corpus, BC alone:

| Demonstrations | Seats | 95% Wilson | 95% of seatings within | Mistakes on its own states | Operator time |
|---:|---:|---|---:|---:|---:|
| $22$ | $0.556$ | $[0.535,\ 0.578]$ | $10.26\,\mathrm{mm}$ | $0.522$ | $1.0\,\mathrm{h}$ |
| $44$ | $0.734$ | $[0.714,\ 0.752]$ | $10.01\,\mathrm{mm}$ | $0.369$ | $2.0\,\mathrm{h}$ |
| $88$ | $0.875$ | $[0.860,\ 0.889]$ | $7.28\,\mathrm{mm}$ | $0.233$ | $4.0\,\mathrm{h}$ |
| $176$ | $0.940$ | $[0.929,\ 0.950]$ | $4.91\,\mathrm{mm}$ | $0.158$ | $8.0\,\mathrm{h}$ |
| $352$ | $0.960$ | $[0.950,\ 0.967]$ | $3.19\,\mathrm{mm}$ | $0.142$ | $16.0\,\mathrm{h}$ |

From the site's start, $2.66\,\mathrm{mm}$ per axis: BC $0.656$ $[0.635,\ 0.677]$, DAgger's fourth round $0.848$ $[0.832,\ 0.863]$, BC as residual $1.000$ $[0.998,\ 1.000]$ with $95\%$ within $1.04\,\mathrm{mm}$. BC from five other corpora of 88: $0.865$, $0.817$, $0.879$, $0.840$, $0.859$.

Seven readings, each tagged with the claim it tests.

**The two distributions are two numbers** (tests §2 and §3). The fitted table gives a command the operator would not give on $0.0225$ of the operator's own states and on $0.233$ of its own: ten times more, on the same table, because only the states changed.

**The worst case is a bound** (tests the Worked case). With the measured error of $0.0225$, the worst case predicts $0.9775^{25}=0.566$; the table seats $0.875$. Not every error in the lab is absorbing: many are commands off by more than $0.3\,\mathrm{mm}$ that still leave the hole inside the corridor, and an error against the creep is carried back into it. The lab happens to sit inside the model's worst case; nothing guarantees it, because the lab counts commands more than $0.3\,\mathrm{mm}$ off rather than Theorem 2.1's 0-1 loss, and smaller deviations still move the state.

**Relabelling beats collecting** (tests §5). One DAgger round, $40$ minutes of attempts, takes BC from $0.875$ to $0.950$; two rounds reach $0.980$ at $5.3\,\mathrm{h}$ of operator time, above the $0.960$ of four times the corpus at $16.0\,\mathrm{h}$. The mistakes on the policy's own states fall with every round, from $0.233$ to $0.069$.

**The residual's zero is the base's correction** (tests §7). Same corpus, same fit: as a policy the table seats $0.875$, as a residual on the base $1.000$. The base alone also seats $1.000$, so on this start the learned part buys precision, $1.08$ against $1.24\,\mathrm{mm}$, and the bound buys robustness.

**What the log held** (tests §2 and §6). A corpus in which the operator watched only the logged camera seats $0.953$ against $0.875$ for the same number of demonstrations: nearly two thirds of BC's failures, $12.5\%$ down to $4.7\%$, came from the operator acting on a view the log did not keep.

**The site is another start distribution** (tests §8). From $2.66\,\mathrm{mm}$ per axis BC falls to $0.656$ and DAgger's fourth round to $0.848$, because every round was run from the mock-up's starts; the residual stays at $1.000$.

**A policy is one draw** (tests §8). Five other corpora of 88 give BC between $0.817$ and $0.879$, a spread four times the half-width of the interval that one trained policy's $2{,}000$ seatings earn.

> [!important] The dissertation sentence, as one object
> The research program states the contribution as *learning and control for contact-rich mobile manipulation in human-centered construction environments* ([[07-research-program/index|7. §3]]). On S1's last $40\,\mathrm{mm}$ each part of that sentence has now been taught on one object. *Learning*: what behaviour cloning fits and where it breaks (§2–§3), two demonstrators averaged (§4), DAgger (§5), all measured in §9. *Control*: the impedance target that turns an error into a force (§6) and the classical base a learned residual corrects (§7). *Contact-rich manipulation*: the lead-in, the force limit and the load handed to the fasteners (§1, §6). *Mobile*: the base term that makes the site's start $2.66\,\mathrm{mm}$ (§8, from 9). *Human-centered*: the bound a worker's presence may tighten and never widen (§7). *Construction environments*: the creep, the site's start and the rung the evidence stands on (§1, §8).

### After reading

- [ ] Write S1's seating as a learning problem: observation, command, dynamics, the three conditions of success, and the demonstrator.
- [ ] State behaviour cloning's three conditions and the two ways acting breaks the i.i.d. assumption, and say what the operator's close-up view did to the cloned gain.
- [ ] Turn a per-step error into steps adrift, millimetres and a seating probability, and give the horizon of BC and of DAgger.
- [ ] Say what a unimodal head does with two routes, and what a chunk and a multimodal head each change.
- [ ] Cost a DAgger round in operator time and name the two costs the algorithm itself does not show.
- [ ] Choose between position and impedance targets by the force a millimetre becomes, and say which force the log must hold.
- [ ] Bound a residual's worst case and say what a worker's presence may do to the bound.
- [ ] Read a success claim with its Wilson interval, the trials that rule out a failure rate, the number of corpora behind it, and its rung.

### Self-check

1. The fitted table's loss on held-out demonstrations is low. Why does that not predict its seating rate?
2. Why does the cloned policy of §2 settle at the operator's $0.4\,\mathrm{mm}$ yet spread nearly twice as wide?
3. A colleague proposes collecting 88 more demonstrations instead of running DAgger. What does §5's table say, and why?
4. If a chunk's error rate were a step's, chunks of $10$ would raise §3's worst case from $0.603$ to $0.941$ (§4). What does the chunk cost on S1?
5. Why may an estimate of the worker's state lower $B$ but never raise it?
6. A policy that outputs position targets into a stiff loop seats $99\%$ of panels on a mock-up. Is S1's seating solved?

> [!tip]- Answers
> 1. Because that loss is condition three of §2's box: it is averaged over the operator's states. The policy is scored on its own states, where the fitted table errs ten times as often ($0.233$ against $0.0225$, §9), and an error there is followed by more because the table has no data outside the corridor.
> 2. Because where the corpus is narrow the camera hardly predicts the command. Late in the phase the true offset varies by $0.03\,\mathrm{mm}^2$ and the camera adds $0.25$, so the fit shrinks the operator's gain by $0.03/0.28=0.107$, to $0.054$ per step. A weak gain still cancels the creep at $0.4\,\mathrm{mm}$, where the operator's command was $-0.2$, but it lets the sway spread the hole to $0.32\,\mathrm{mm}$ instead of $0.173$.
> 3. That doubling the corpus (another $4.0\,\mathrm{h}$) gives $0.940$, while one DAgger round ($40\,\mathrm{min}$) gives $0.950$ and two ($80\,\mathrm{min}$) $0.980$. New demonstrations come from the operator's distribution, where the policy already does well; relabelled attempts come from the policy's own, where it fails.
> 4. Open-loop time. For $10$ steps, $1\,\mathrm{s}$, the chunk cannot see the hole: it must predict the creep, and the sway alone spreads the hole $0.32\,\mathrm{mm}$ before the next look. And its rate of error per decision is not a step's: a wrong chunk is ten wrong commands.
> 5. Because the bound is part of the admissible set, which [[05-construction-robotics/hrc-worker-centered|6. HRC §8]] computes only from measured state with worst-case human terms. A lower $B$ keeps the residual's worst case closer to the base, which is safe whatever the estimate got wrong; a higher $B$ would let an estimate move the bound that protects the worker it mispredicts.
> 6. No. Condition two of §1 fails: a seating $0.71\,\mathrm{mm}$ off, which even the operator produces $5\%$ of the time, pushes $71\,\mathrm{N}$ sideways through $10^5\,\mathrm{N/m}$, and only seatings within $0.2\,\mathrm{mm}$ stay under $20\,\mathrm{N}$. The claim needs its force, its counting rule and its rung before the $99\%$ means anything, and the handover at the end of the hold needs a logged force (§6).

### Problem set · 과제

Tier A. S1's last millimetres, with [[04-robotics/teleoperation-demonstration|12]], [[04-robotics/force-compliance-control|13]] and [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]] behind them. The lab fits tables by least squares on sampled demonstrations; there is no physics simulator.

1. **Draw.** The picture for a policy twice as good on the operator's states, $\epsilon=0.01$, lowering the panel over its last $60\,\mathrm{mm}$ ($T=60$): the corridor, a cloned policy whose first error comes at $40\,\mathrm{mm}$ and one whose first error comes at $10\,\mathrm{mm}$, their offsets at the pin, the line where the last $15\,\mathrm{mm}$ begin, the seating probability, and a residual on the base at $B=0.4\,\mathrm{mm}$ per step pushed by its bound every step.
2. **Derive.** (a) For $\epsilon=0.01$ and $T=60$: the probability that the cloned policy seats, the expected steps adrift, Theorem 2.1's bound, and the phase lengths at which the bounds of BC and of DAgger ($u=1$) reach the $15$ steps the lead-in absorbs. (b) On site the creep grows to $c=0.3\,\mathrm{mm}$ per step: the operator's offset and corridor edge (rounded up to the next tenth of a millimetre, as §3 rounded $0.92$ up to $1$), the steps adrift the lead-in absorbs (whole steps), BC's worst-case seating at $\epsilon=0.02$ and $T=40$, and the residual's worst case at $B=0.3$. (c) The largest $B$ that keeps the residual's worst case four base-loop standard deviations inside the lead-in at $c=0.3$. (d) The Wilson interval for $38$ seatings in $40$.
3. **Do.** Fill the `?` so that the script samples the Worked case's model — the cloned policy adrift from its first error, DAgger taking every error back, and a residual pushed by $+B$ — and reproduces Steps 3–5, then sweeps the phase over $T=20,\ 40,\ 60,\ 80$ at $\epsilon=0.02$ and at $\epsilon=0.01$. Read the sweep: at which of these lengths does the cloned policy first seat less than $90\%$ of the time, for each $\epsilon$, and what does the DAgger column do?

```python
import numpy as np
C, EDGE, RC, K0, BND = 0.2, 1.0, 4.0, 0.25, 0.3   # creep (mm/step), corridor edge, lead-in (mm), base gain, bound
NM = round((RC - EDGE) / C)                        # steps adrift the lead-in can absorb: 15
rng = np.random.default_rng(7)

def cloned(eps, T, n=200_000):                     # worst case: adrift from the first error to the pin
    err = rng.random((n, T)) < eps
    first = np.where(err.any(axis=1), ?, T + 1)    # the first error's step, counted from 1
    return ?                                       # steps adrift, the error's own step included

def dagger(eps, T, n=200_000):                     # every error is taken back on the next step
    err = rng.random((n, T)) < eps
    return np.where(err.all(axis=1), T, np.argmin(err[:, ::-1], axis=1))  # errors in a row at the end

def residual_worst(T):                             # base plus a residual pushing +B every step
    m = np.zeros(2)
    for _ in range(T):
        m = (1 - K0) * m + np.array([?, BND])      # along the wall the creep adds to the push
    return float(np.hypot(*m))

for eps in (0.02, 0.01):
    for T in (20, 40, 60, 80):
        n_off = cloned(eps, T)
        print(f"eps {eps} T {T}: cloned seats {np.mean(n_off <= NM):.3f} (formula {(1 - eps) ** max(T - NM, 0):.3f}),"
              f" adrift {n_off.mean():5.2f} steps; DAgger seats {np.mean(dagger(eps, T) <= NM):.3f}")
print("residual pushed by +B every step, offset at the pin:", round(residual_worst(40), 2), "mm")
```

4. **Interpret.** A paper reports: "our BC policy inserts panels with 95% success over 20 trials on a mock-up." (a) Give the Wilson interval and the failure rates it cannot exclude. (b) How often would §9's BC, which seats $0.875$, show at least $19$ of $20$? (c) How many straight successes would rule out a $5\%$ failure rate? (d) Place the claim on the ladder and say what the site would change, with §9's numbers. (e) Name three more things the paper must state before its 95% can be compared with anything.

> [!note]- How to draw it · 그리는 법
> - **The axes**: height above the pin tips from $60$ to $0\,\mathrm{mm}$, one step per millimetre, and the offset along the wall from $-4.5$ to $10\,\mathrm{mm}$; the pin's axis at $0$ and the lead-in as a bar from $-4$ to $4\,\mathrm{mm}$ at the pin.
> - **The corridor**: the operator's mean $0.4\,(1-0.5^t)$ plus and minus three standard deviations, $\pm4.05\,\mathrm{mm}$ at the top, narrowing within five steps to $[-0.12,\ 0.92]\,\mathrm{mm}$ — the same band as the picture, with $20$ more steps of it.
> - **The two cloned policies**: an error at $40\,\mathrm{mm}$ (step $20$) leaves $41$ steps adrift and reaches the pin at $1+0.2\times41=9.2\,\mathrm{mm}$; one at $10\,\mathrm{mm}$ (step $50$) leaves $11$ steps and reaches it at $3.2\,\mathrm{mm}$, inside the lead-in. Mark the line at $15\,\mathrm{mm}$ and write the seating probability $0.99^{45}=0.636$.
> - **The residual**: at $B=0.4$ the worst case settles at $(0.4+0.2)/0.25=2.4\,\mathrm{mm}$ along the wall and $0.4/0.25=1.6\,\mathrm{mm}$ toward it, $2.88\,\mathrm{mm}$ from the pin; draw its along-wall path rising to $2.4$.
> - The drawing is wrong if the cloned policy's slope depends on how late the error came: every error sets the hole drifting at the same $0.2\,\mathrm{mm}$ per step, and only the number of steps left differs.

> [!tip]- Solutions
> 1. As in the How-to-draw list: errors at $40$ and $10\,\mathrm{mm}$ end at $9.2$ and $3.2\,\mathrm{mm}$, seating probability $0.636$, residual worst case $2.4\,\mathrm{mm}$ along the wall and $2.88\,\mathrm{mm}$ from the pin.
> 2. (a) $0.99^{60-15}=0.99^{45}=0.636$; $E[N_{\text{off}}]=15.17$ steps, $3.03\,\mathrm{mm}$; the bound $T^2\epsilon=36$ steps; BC's bound reaches $15$ at $T=\sqrt{15/0.01}=38.7$ steps and DAgger's at $T=15/0.01=1500$. (b) The operator settles at $0.3/0.5=0.6\,\mathrm{mm}$ with the same $s=0.173\,\mathrm{mm}$, so the edge is $0.6+0.52=1.12\,\mathrm{mm}$, rounded up to $1.2$; the lead-in absorbs $(4-1.2)/0.3=9.3$, so $9$ whole steps; BC seats $0.98^{40-9}=0.98^{31}=0.535$; the residual's worst case is $(0.3+0.3)/0.25=2.4\,\mathrm{mm}$ along the wall and $1.2\,\mathrm{mm}$ toward it, $2.68\,\mathrm{mm}$ from the pin. (c) $\sqrt{((B+0.3)/0.25)^2+(B/0.25)^2}\le4-4\times0.242=3.03\,\mathrm{mm}$ gives $B\le0.36\,\mathrm{mm}$ per step: the stronger creep eats about $0.06$ of the $0.43$ that §7 allowed. (d) $z^2/n=0.096$; centre $(0.95+0.048)/1.096=0.911$, half-width $1.96\sqrt{0.95\times0.05/40+3.8416/6400}/1.096=0.076$: $[0.835,\ 0.986]$.
> 3. The blanks are `err.argmax(axis=1) + 1`, `T + 1 - first` and `BND + C`. The filled script:
>
> ```python
> import numpy as np
> C, EDGE, RC, K0, BND = 0.2, 1.0, 4.0, 0.25, 0.3   # creep (mm/step), corridor edge, lead-in (mm), base gain, bound
> NM = round((RC - EDGE) / C)                        # steps adrift the lead-in can absorb: 15
> rng = np.random.default_rng(7)
>
> def cloned(eps, T, n=200_000):                     # worst case: adrift from the first error to the pin
>     err = rng.random((n, T)) < eps
>     first = np.where(err.any(axis=1), err.argmax(axis=1) + 1, T + 1)   # the first error's step, counted from 1
>     return T + 1 - first                           # steps adrift, the error's own step included
>
> def dagger(eps, T, n=200_000):                     # every error is taken back on the next step
>     err = rng.random((n, T)) < eps
>     return np.where(err.all(axis=1), T, np.argmin(err[:, ::-1], axis=1))  # errors in a row at the end
>
> def residual_worst(T):                             # base plus a residual pushing +B every step
>     m = np.zeros(2)
>     for _ in range(T):
>         m = (1 - K0) * m + np.array([BND + C, BND])   # along the wall the creep adds to the push
>     return float(np.hypot(*m))
>
> for eps in (0.02, 0.01):
>     for T in (20, 40, 60, 80):
>         n_off = cloned(eps, T)
>         print(f"eps {eps} T {T}: cloned seats {np.mean(n_off <= NM):.3f} (formula {(1 - eps) ** max(T - NM, 0):.3f}),"
>               f" adrift {n_off.mean():5.2f} steps; DAgger seats {np.mean(dagger(eps, T) <= NM):.3f}")
> print("residual pushed by +B every step, offset at the pin:", round(residual_worst(40), 2), "mm")
> ```
>
> It prints, for $\epsilon=0.02$ at $T=20,\ 40,\ 60,\ 80$, cloned seatings of $0.904$, $0.604$, $0.403$ and $0.268$ against the formula's $0.904$, $0.603$, $0.403$ and $0.269$, with $3.70$, $12.82$, $25.58$ and $40.85$ steps adrift against the exact $3.71$, $12.84$, $25.58$ and $40.73$; for $\epsilon=0.01$, $0.950$, $0.777$, $0.638$ and $0.520$ against $0.951$, $0.778$, $0.636$ and $0.520$, with $1.97$, $7.26$, $15.08$ and $25.40$ steps adrift; DAgger seats $1.000$ in every row; and the residual's worst case is $2.33\,\mathrm{mm}$. Among the four lengths the cloned policy first seats less than $90\%$ of the time at $T=40$ for both rates — by the formula from $T=21$ at $\epsilon=0.02$ and from $T=26$ at $\epsilon=0.01$ — so halving the error lengthens the phase BC seats nine times in ten by only five millimetres: the part above the last $15\,\mathrm{mm}$ doubles, from about $5$ to about $10\,\mathrm{mm}$, while the lead-in's $15\,\mathrm{mm}$ stay fixed. The DAgger column never leaves $1.000$: without the third condition of §3 no error is carried to the pin.
> 4. (a) $19/20$ gives the Wilson interval $[0.764,\ 0.991]$, so any failure rate up to $23.6\%$ is compatible with the report. (b) At $p=0.875$, $P(X\ge19)=20\times0.875^{19}\times0.125+0.875^{20}=0.267$: about one such experiment in four would print the paper's sentence for a policy that fails one seating in eight. (c) $n\ge\ln0.05/\ln0.95=58.4$, so $59$ straight successes. (d) A full-scale mock-up at best, which licenses "it survives realistic geometry and scale" and measures only the arm, tool and part terms ([[05-construction-robotics/site-engineering|2.5 §5]]); on site the start widens to $2.66\,\mathrm{mm}$, and §9's BC falls from $0.875$ to $0.656$ while a residual on a classical base holds $1.000$. (e) Any three of: how many corpora or seeds were trained and how far they spread; the counting rule for interventions and resets; the start distribution and the creep during the approach; whether "success" includes a force limit and through what stiffness the targets were tracked; the corpus's size, yield and routes.

### Sources

- S. Ross, G. J. Gordon, J. A. Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning," *AISTATS 2011*, PMLR vol. 15, pp. 627–635; [arXiv:1011.0686](https://arxiv.org/abs/1011.0686), read at [ar5iv](https://ar5iv.labs.arxiv.org/html/1011.0686) — the abstract's i.i.d. sentence (§2); Theorem 2.1, credited to Ross and Bagnell (2010), with its $[0,1]$ cost, its 0-1 loss and its tightness, and Theorem 3.2 with the definition of $\epsilon_N$ (§3); Algorithm 3.1 with $\beta_1=1$, $\beta_i=p^{i-1}$ and $\beta_i=\mathbb 1[i=1]$ (§5). See also the [[01-canonical-papers/notes/4-vla/dagger|DAgger note]].
- M. Kelly, C. Sidrane, K. Driggs-Campbell, M. J. Kochenderfer, "HG-DAgger: Interactive Imitation Learning with Human Experts," *ICRA 2019*, pp. 8077–8083, DOI 10.1109/ICRA.2019.8793698; [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — labels given without control, which can decrease safety and are likely to be of lower quality (abstract), and the expert taking control in unsafe regions with labels collected only then (§5).
- T. Z. Zhao, V. Kumar, S. Levine, C. Finn, "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware," *RSS 2023*, [arXiv:2304.13705](https://arxiv.org/abs/2304.13705) — ACT's chunks; its CVAE, trained for the demonstrators' variability, with the latent set to the prior's mean, zero, at test time to decode deterministically; and temporal ensembling as an exponentially weighted average of overlapping chunks, as the paper states (§4). See also the [[01-canonical-papers/notes/4-vla/act|ACT note]].
- C. Chi et al., "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion," *RSS 2023*, [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) — graceful handling of multimodal action distributions, as its abstract states (§4); see the [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy note]].
- C. Chen, Z. Yu, H. Choi, M. Cutkosky, J. Bohg, "DexForce: Extracting Force-informed Actions from Kinesthetic Demonstrations for Dexterous Manipulation," [arXiv:2501.10356](https://arxiv.org/abs/2501.10356), 2025 — force-informed targets $x_f=x_o+k_f f$ and $76\%$ average success over six tasks against near-zero for policies trained on observed positions (§6).
- T. Silver, K. Allen, J. Tenenbaum, L. Kaelbling, "Residual Policy Learning," [arXiv:1812.06298](https://arxiv.org/abs/1812.06298), 2018 — a residual learned on top of an initial controller (§7).
- T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, S. Levine, "Residual Reinforcement Learning for Robot Control," *ICRA 2019*, pp. 6023–6029, DOI 10.1109/ICRA.2019.8794127; [arXiv:1812.03201](https://arxiv.org/abs/1812.03201) — the final policy as a superposition of a conventional controller's signal and an RL residual (§7).
- E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association* 22(158):209–212, 1927 — the score interval, as worked in [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]] (§8, §9).
- Within this wiki: [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] (S1 at the pin), [[04-robotics/teleoperation-demonstration|12. Teleoperation]] (the corpus log and its metrics), [[04-robotics/capstone-panel-contact|26. Capstone]] (the classical loop), [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real]] (the residual), [[05-construction-robotics/hrc-worker-centered|6. HRC]] (the worker's bounds).
- Every course number on this page was computed here with NumPy 2.0.2 from S1's frozen values and this page's own; the demonstrations, rollouts and sites are sampled, not measured.

## 한국어

*건설 트랙의 마지막 페이지다. 구멍이 핀을 만나는 순간의 S1(건설 트랙의 외장 패널 과제, [[05-construction-robotics/site-engineering|2.5]])에 값을 매긴 [[05-construction-robotics/construction-manipulation|9]]와, 시연이 어떻게 만들어지는지 기록한 [[04-robotics/teleoperation-demonstration|12]] 위에 선다. [[04-robotics/capstone-panel-contact|로보틱스 캡스톤]]은 패널 위에서 고전 루프를 닫았고, 이 페이지는 학습한 정책을 현장 허용오차까지 몰고 간다.*

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]가 피지컬 AI 스택의 사례로 드는 "*저 패널을 프레임에 설치해*"에서, 이 페이지는 "끼움을 수행한다"의 학습 절반이다. 학습·적응 층을 접촉 단계까지 끌어내려, 시연에서 배운 정책이 패널을 앉힌다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 이것 없이는 학습된 정책의 약속을 엉뚱한 숫자로 읽는다. 자기 상태의 $0.02$에서만 틀리는 복제 정책도 S1의 패널을 $0.98^{25}=0.603$의 확률로만 앉힌다. 단계의 $40$스텝 가운데 앞 $25$스텝 어디에서든 오류가 나면 구멍이 시연 밖으로 떠나 핀의 $4\,\mathrm{mm}$ 리드인을 넘기 때문이다. 목업에서 스무 번 중 열아홉 번 앉혀도 Wilson 구간은 $0.764$까지 내려간다. 이 페이지는 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])의 7 블록, 곧 실험 전의 마지막 블록이고, 앞의 모든 블록 — [[05-construction-robotics/construction-manipulation|9]]의 포착 계산과 [[04-robotics/teleoperation-demonstration|12. 원격조작 §6]]의 시연을 포함해 — 위에 선다. 실제로 돌리려면 학습할 클러스터([[02-foundations/tools/gpu-clusters|12.7 GPU 클러스터]])와 매 시행 핀이 같은 자리로 돌아오는 목업([[02-foundations/tools/mechanical-design-fabrication|12.9 §7]])이 필요하다. 이 페이지를 마치면 학습된 정책을 시연에서 앉힌 패널까지 끌고 가고, 그것이 어디서 깨지는지와 어느 해법이 현장에서 제값을 하는지를 밀리미터와 안착 확률로 말할 수 있다.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고 그림을 본다. S1의 마지막 40 mm, 시연이 덮은 회랑, 그리고 오류 하나가 복제한 정책과 DAgger와 고전 기본 제어기 위의 잔차에 각각 무슨 일을 하는지다. 그다음 §1–§3에서 학습 문제로서의 작업, 행동 복제가 가정하는 것, 그 가정이 밀리미터로 만드는 복합 오차를 읽고, §8 뒤의 계산 절에서 스텝당 오류 0.02가 안착 확률 0.603이 되는 과정을 본다. §4–§7은 해법을 고른다. 시연자 둘을 위한 헤드, DAgger, 행동, 한계를 둔 잔차다. §8과 §9의 랩은 주장을 판정할 때 읽는다.

### 이 페이지의 대상 · Running object

[[05-construction-robotics/site-engineering|2.5]]의 **S1**을 [[05-construction-robotics/construction-manipulation|9]]가 놓아둔 순간부터 이어 간다. 브래킷 위의 $20\,\mathrm{kg}$ 외장 패널이고, $18\,\mathrm{mm}$ 구멍마다 반지름 방향 오차를 $4\,\mathrm{mm}$까지 붙잡는 뾰족한 끝을 가진 $16\,\mathrm{mm}$ 핀 위로 막 내려앉으려 한다. 9는 그 순간을 오차 예산이 구멍을 놓아둔 자리에서 값으로 매겼다. 이 페이지는 패널이 내려오는 마지막 $40\,\mathrm{mm}$를 따라간다. 패널을 내리는 동안 누군가는 구멍을 계속 바로잡아야 하고, 이 페이지는 시연에서 학습한 정책이 그 누군가가 될 수 있는지 묻는다. 페이지의 모든 정책이 같은 안착을 푼다. 바뀌는 것은 보정을 고르는 주체뿐이다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $r_c$, $K_d$, $K_{\text{stiff}}$, $W$ | $4\,\mathrm{mm}$; $500$과 $10^5\,\mathrm{N/m}$; $196\,\mathrm{N}$ | 9의 리드인, 옆 방향 목표 임피던스, 단단한 루프, 패널 무게. 그대로 쓴다 |
| $\sigma_0$ | 축마다 $1.35\,\mathrm{mm}$ | 단계가 시작될 때 구멍의 어긋남. 9의 예산을 2시그마 경계로 읽은 것 |
| 단계 | $10\,\mathrm{mm/s}$로 $40\,\mathrm{mm}$, $10\,\mathrm{Hz}$ | $0.1\,\mathrm{s}$짜리 스텝 $T=40$개, 스텝마다 1밀리미터씩 내려간다 |
| $c$ | 벽을 따라 스텝마다 $0.2\,\mathrm{mm}$ | 패널을 내리는 동안 베이스와 팔의 크리프(creep). 벽 쪽으로는 없다 |
| $\sigma_w$ | 스텝마다 $0.1\,\mathrm{mm}$ | 각 축의 흔들림 |
| $\sigma_v$ | $0.5\,\mathrm{mm}$ | 로봇 카메라가 구멍의 어긋남을 재는 오차. 정책이 보는 유일한 것 |
| 조작자 | $u=-k_E\,(x+\nu)+\eta$, $k_E=0.5$, $\sigma_\nu=\sigma_\eta=0.1\,\mathrm{mm}$ | 로거가 기록하지 않은 근접 화면에서 본 어긋남의 절반을 손 잡음과 함께 바로잡는다 |
| 코퍼스 | 시도 $120$, 안착 $96$, 폐기 $8$, 사용 가능 $88$, $4.0\,\mathrm{h}$; 경로 $-60$과 $+60\,\mathrm{mm}$, $58/38$로 나뉨; 복구가 담긴 것 $11$ | 12의 형식과 12의 개수로 기록한 S1의 세션 |
| $\epsilon$ | 스텝마다 $0.02$ | 조작자 자신의 상태에서 복제 정책이 내는 오류율(§3). §9의 적합 정책은 $0.0225$를 잰다 |
| $k_0$, $B$ | $0.25$; 스텝마다 $0.3\,\mathrm{mm}$ | 고전 기본 제어기의 시각 이득, 그리고 학습 잔차의 한계(§7) |
| $F_{\lim}$ | $20\,\mathrm{N}$ | 안착 때 허용하는 옆 힘. $W$의 약 10분의 1 |

첫 행은 9와 S1의 것이고, 코퍼스 행은 12의 개수를 가져온다. 나머지는 모두 이 페이지의 교과 숫자로, 모든 주장을 확인할 수 있게 고정한 것이지 어떤 기계에서 잰 것이 아니다. 크리프는 이 단계를 열린 루프로 돌릴 수 없게 고른 값이다. 보정하지 않으면 구멍을 $0.2\times40=8\,\mathrm{mm}$, 리드인의 두 배만큼 옮긴다. 코퍼스는 12의 개수를 그대로 써서 12의 코퍼스 지표가 바뀌지 않고 넘어온다. 수율 $88/120=0.733$, 사용 가능한 시연당 $164\,\mathrm{s}$, 두 경로에 대한 모드 엔트로피 $0.968$비트, 복구 포함률 $11/88=0.125$다([[04-robotics/teleoperation-demonstration|12. 원격조작]]의 계산 절 6단계).

*범위: 이 페이지는 접촉 작업 하나의 모방학습을 처음부터 끝까지 가르친다. 학습 문제로서의 작업, 행동 복제와 그것이 만드는 복합 오차, 평균으로 뭉개진 시연자 둘, DAgger, 행동의 선택, 현장이 한계를 긋는 잔차, 성공 주장의 판정이다. 대상은 S1의 안착 단계이고 NumPy 랩이 붙는다. 시연을 모으는 법([[04-robotics/teleoperation-demonstration|12]]), 임피던스 제어 자체([[04-robotics/force-compliance-control|13]]), 생성형 행동 헤드의 내부([[03-deep-learning/diffusion/index|6. Diffusion & Flow]]), RL 파인튜닝([[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §4]]), 이격 거리([[05-construction-robotics/hrc-worker-centered|6. HRC §6]])는 가르치지 않고 그 결과를 쓴다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 360" style="max-width:100%;height:auto" role="img" aria-label="마지막 40 mm 동안 핀 끝 위의 높이에 대한 S1 구멍의 벽 방향 어긋남. 시연의 띠는 플러스마이너스 4 mm에서 마이너스 0.12와 0.92 mm 사이로 좁아진다. 첫 오류가 24 mm에서 난 복제 정책은 한 스텝에 0.2 mm씩 표류해 6.0 mm 어긋난 채 핀에 닿아 4 mm 리드인 밖에 떨어지고, 첫 오류가 9 mm에서 난 정책은 3.0 mm로 닿아 앉는다. 그래서 앉을 확률은 0.98의 25제곱, 0.603이다. DAgger는 같은 오류를 되돌리고, 매 스텝 한계만큼 미는 잔차를 단 기본 제어기는 2.0 mm에 머문다.">
<text x="12" y="18" font-size="12" fill="currentColor" font-weight="600">S1의 마지막 40 mm: 패널을 내리는 동안 벽을 따라 잰 구멍의 어긋남</text>
<polygon points="50.0,89.0 60.2,124.5 70.5,141.4 80.8,148.5 91.0,151.0 101.2,151.6 111.5,151.7 121.8,151.7 132.0,151.6 142.2,151.6 152.5,151.6 162.8,151.6 173.0,151.6 183.2,151.6 193.5,151.6 203.8,151.6 214.0,151.6 224.2,151.6 234.5,151.6 244.8,151.6 255.0,151.6 265.2,151.6 275.5,151.6 285.8,151.6 296.0,151.6 306.2,151.6 316.5,151.6 326.8,151.6 337.0,151.6 347.2,151.6 357.5,151.6 367.8,151.6 378.0,151.6 388.2,151.6 398.5,151.6 408.8,151.6 419.0,151.6 429.2,151.6 439.5,151.6 449.8,151.6 460.0,151.6 460.0,172.4 449.8,172.4 439.5,172.4 429.2,172.4 419.0,172.4 408.8,172.4 398.5,172.4 388.2,172.4 378.0,172.4 367.8,172.4 357.5,172.4 347.2,172.4 337.0,172.4 326.8,172.4 316.5,172.4 306.2,172.4 296.0,172.4 285.8,172.4 275.5,172.4 265.2,172.4 255.0,172.4 244.8,172.4 234.5,172.4 224.2,172.4 214.0,172.4 203.8,172.4 193.5,172.4 183.2,172.4 173.0,172.4 162.8,172.4 152.5,172.4 142.2,172.4 132.0,172.4 121.8,172.5 111.5,172.6 101.2,172.9 91.0,174.0 80.8,177.5 70.5,186.6 60.2,207.5 50.0,251.0" fill="currentColor" fill-opacity="0.12" stroke="none"/>
<line x1="50.0" y1="170.0" x2="460.0" y2="170.0" stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="2 3"/>
<line x1="306.2" y1="38.0" x2="306.2" y2="260.0" stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="4 3"/>
<text x="383.1" y="44.0" font-size="10.5" fill="currentColor" text-anchor="middle">마지막 15 mm</text>
<polyline points="50.0,170.0 60.2,166.0 70.5,164.0 80.8,163.0 91.0,162.5 101.2,162.2 111.5,162.1 121.8,162.1 132.0,162.0 142.2,162.0 152.5,162.0 162.8,162.0 173.0,162.0 183.2,162.0 193.5,162.0 203.8,162.0 214.0,162.0 224.2,162.0 234.5,162.0 244.8,162.0 255.0,162.0 265.2,162.0 275.5,162.0 285.8,162.0 296.0,162.0 306.2,162.0 316.5,162.0 326.8,162.0 337.0,162.0 347.2,162.0 357.5,162.0 367.8,162.0 378.0,162.0 388.2,162.0 398.5,162.0 408.8,162.0 419.0,162.0 429.2,162.0 439.5,162.0 449.8,162.0 460.0,162.0" fill="none" stroke="currentColor" stroke-opacity="0.55" stroke-width="1"/>
<polyline points="50.0,170.0 60.2,160.0 70.5,152.5 80.8,146.9 91.0,142.7 101.2,139.5 111.5,137.1 121.8,135.3 132.0,134.0 142.2,133.0 152.5,132.3 162.8,131.7 173.0,131.3 183.2,131.0 193.5,130.7 203.8,130.5 214.0,130.4 224.2,130.3 234.5,130.2 244.8,130.2 255.0,130.1 265.2,130.1 275.5,130.1 285.8,130.1 296.0,130.0 306.2,130.0 316.5,130.0 326.8,130.0 337.0,130.0 347.2,130.0 357.5,130.0 367.8,130.0 378.0,130.0 388.2,130.0 398.5,130.0 408.8,130.0 419.0,130.0 429.2,130.0 439.5,130.0 449.8,130.0 460.0,130.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="1.5 3"/>
<polyline points="203.8,162.0 214.0,146.0 224.2,142.0 234.5,138.0 244.8,134.0 255.0,130.0 265.2,126.0 275.5,122.0 285.8,118.0 296.0,114.0 306.2,110.0 316.5,106.0 326.8,102.0 337.0,98.0 347.2,94.0 357.5,90.0 367.8,86.0 378.0,82.0 388.2,78.0 398.5,74.0 408.8,70.0 419.0,66.0 429.2,62.0 439.5,58.0 449.8,54.0 460.0,50.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
<polyline points="357.5,162.0 367.8,146.0 378.0,142.0 388.2,138.0 398.5,134.0 408.8,130.0 419.0,126.0 429.2,122.0 439.5,118.0 449.8,114.0 460.0,110.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>
<polyline points="203.8,162.0 214.0,146.0 224.2,154.0 234.5,158.0 244.8,160.0 255.0,161.0 265.2,161.5 275.5,161.8 285.8,161.9 296.0,161.9 306.2,162.0 316.5,162.0 326.8,162.0 337.0,162.0 347.2,162.0 357.5,162.0 367.8,162.0 378.0,162.0 388.2,162.0 398.5,162.0 408.8,162.0 419.0,162.0 429.2,162.0 439.5,162.0 449.8,162.0 460.0,162.0" fill="none" stroke="currentColor" stroke-width="1.6"/>
<circle cx="214.0" cy="146.0" r="2.8" fill="currentColor"/>
<circle cx="367.8" cy="146.0" r="2.8" fill="currentColor"/>
<line x1="466.0" y1="90.0" x2="466.0" y2="250.0" stroke="currentColor" stroke-width="2.5"/>
<line x1="462.0" y1="90.0" x2="470.0" y2="90.0" stroke="currentColor" stroke-width="1.5"/>
<line x1="462.0" y1="250.0" x2="470.0" y2="250.0" stroke="currentColor" stroke-width="1.5"/>
<text x="474.0" y="54.0" font-size="10.5" fill="currentColor">6.0: 놓침</text>
<text x="474.0" y="94.0" font-size="10.5" fill="currentColor">리드인 ±4</text>
<text x="474.0" y="114.0" font-size="10.5" fill="currentColor">3.0: 앉음</text>
<text x="474.0" y="134.0" font-size="10.5" fill="currentColor">잔차 ≤ 2.0</text>
<text x="474.0" y="166.0" font-size="10.5" fill="currentColor">DAgger 0.4</text>
<text x="80.8" y="46.0" font-size="10.5" fill="currentColor">BC는 첫 오류가 마지막 15 mm에서</text>
<text x="80.8" y="60.0" font-size="10.5" fill="currentColor">날 때만 앉는다: 0.98²⁵ = 0.603</text>
<line x1="50.0" y1="260.0" x2="460.0" y2="260.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="50.0" y1="260.0" x2="50.0" y2="30.0" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="50.0" y1="260.0" x2="50.0" y2="264.0" stroke="currentColor"/><text x="50.0" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">40</text>
<line x1="152.5" y1="260.0" x2="152.5" y2="264.0" stroke="currentColor"/><text x="152.5" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">30</text>
<line x1="255.0" y1="260.0" x2="255.0" y2="264.0" stroke="currentColor"/><text x="255.0" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">20</text>
<line x1="357.5" y1="260.0" x2="357.5" y2="264.0" stroke="currentColor"/><text x="357.5" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">10</text>
<line x1="460.0" y1="260.0" x2="460.0" y2="264.0" stroke="currentColor"/><text x="460.0" y="276.0" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="46.0" y1="250.0" x2="50.0" y2="250.0" stroke="currentColor"/><text x="43.0" y="254.0" font-size="10.5" fill="currentColor" text-anchor="end">-4</text>
<line x1="46.0" y1="210.0" x2="50.0" y2="210.0" stroke="currentColor"/><text x="43.0" y="214.0" font-size="10.5" fill="currentColor" text-anchor="end">-2</text>
<line x1="46.0" y1="170.0" x2="50.0" y2="170.0" stroke="currentColor"/><text x="43.0" y="174.0" font-size="10.5" fill="currentColor" text-anchor="end">0</text>
<line x1="46.0" y1="130.0" x2="50.0" y2="130.0" stroke="currentColor"/><text x="43.0" y="134.0" font-size="10.5" fill="currentColor" text-anchor="end">2</text>
<line x1="46.0" y1="90.0" x2="50.0" y2="90.0" stroke="currentColor"/><text x="43.0" y="94.0" font-size="10.5" fill="currentColor" text-anchor="end">4</text>
<line x1="46.0" y1="50.0" x2="50.0" y2="50.0" stroke="currentColor"/><text x="43.0" y="54.0" font-size="10.5" fill="currentColor" text-anchor="end">6</text>
<text x="43.0" y="28.0" font-size="10.5" fill="currentColor" text-anchor="end">mm</text>
<text x="255.0" y="290.0" font-size="10.5" fill="currentColor" text-anchor="middle">핀 끝 위의 높이(mm), 1밀리미터마다 제어 한 스텝</text>
<text x="12" y="308.0" font-size="10.5" fill="currentColor">음영: 시연 88개가 구멍을 둔 곳, 평균 ± 3σ (핀에서 가장자리 0.92 mm)</text>
<text x="12" y="322.0" font-size="10.5" fill="currentColor">파선: 복제 정책, 첫 오류가 24 mm와 9 mm에서, 한 스텝에 0.2 mm씩 표류</text>
<text x="12" y="336.0" font-size="10.5" fill="currentColor">실선: DAgger, 24 mm에서 같은 오류를 되돌린다</text>
<text x="12" y="350.0" font-size="10.5" fill="currentColor">점선: 기본 제어기 + 매 스텝 +B로 미는 잔차: 벽 방향으로 2.0 mm를 넘지 않는다</text>
</svg>

S1의 마지막 $40\,\mathrm{mm}$이고, 1밀리미터 내려갈 때마다 제어 스텝 하나다. 음영 띠는 시연 88개가 구멍을 둔 곳으로, 핀에서는 가장자리 $0.92\,\mathrm{mm}$까지 좁아진다. 오류를 낸 복제 정책은 띠를 벗어나고, 그런 상태를 본 적이 없으므로 보정을 멈춘다. 그래서 크리프가 스텝마다 $0.2\,\mathrm{mm}$씩 끌고 간다 — $24\,\mathrm{mm}$에서 난 오류는 핀에 $6.0\,\mathrm{mm}$ 어긋난 채, $9\,\mathrm{mm}$에서 난 오류는 $3.0\,\mathrm{mm}$ 어긋난 채 닿으므로, 첫 오류가 마지막 $15\,\mathrm{mm}$에서 날 때만 앉고 그 확률은 $0.98^{25}=0.603$이다. DAgger는 같은 오류를 몇 스텝 안에 되돌리고, 고전 기본 제어기 위의 잔차는 매 스텝 한계만큼 밀려도 벽을 따라 $2.0\,\mathrm{mm}$를 넘지 않는다.

### 1. 학습 문제로서의 안착 작업

*한 문장으로:* S1의 마지막 $40\,\mathrm{mm}$는 다섯 가지를 적는 순간 모방학습 문제가 된다. 정책이 무엇을 보는가, 무엇을 명령하는가, 구멍이 어떻게 움직이는가, 무엇을 안착으로 치는가, 누가 시연했는가다.

**어디에 놓이는가.** [[05-construction-robotics/site-engineering|2.5 §1]]은 S1의 작업 묶음을 집기, 운반, 정렬, 지지·체결, 확인으로 나눈다. 안착은 *정렬*의 끝이다. 정렬의 안전 상태는 후퇴 후 재스캔이다. 아직 패널에 아무도 없고 놓치면 시간만 잃기 때문이다. 그다음 단계인 지지·체결은 작업자의 손을 패널에 올려놓는다. §7이 핀이 아니라 작업자로 끝나는 이유다.

**정책이 보는 것과 명령하는 것.** 정책은 $o_t$를 관측한다. 로봇 카메라가 두 수평 축 각각에서 추정한 구멍과 핀 사이의 어긋남이고, 핀 끝이 닿은 뒤에는 손목 힘이 더해진다(§6). 정책은 $u_t$를 명령한다. 스텝마다 옆 방향 임피던스 목표를 고치는 양이고, [[04-robotics/force-compliance-control|13. §2]]의 $500\,\mathrm{N/m}$ 옆 방향 임피던스가 이를 구현한다. 그러면 각 축에서 구멍은 이렇게 움직인다.

$$x_{t+1}=x_t+u_t+c+w_t,\qquad o_t=x_t+v_t,$$

스텝마다 구멍이 있던 자리에 명령과 크리프와 흔들림이 더해지고, 카메라는 그 자리를 오차와 함께 알려 주기 때문이다. $x_t$는 밀리미터 단위의 어긋남, $c$는 벽을 따라 $0.2$이고 벽 쪽으로 $0$, $w_t$는 $\sigma_w=0.1$인 흔들림, $v_t$는 $\sigma_v=0.5\,\mathrm{mm}$인 카메라 오차다.

**무엇을 안착으로 치는가.** 세 조건이고, 정책은 셋을 모두 지켜야 한다.

$$S=\mathbb 1\big[r_T\le r_c\big]\cdot\mathbb 1\big[K\,r_T\le F_{\lim}\big]\cdot\mathbb 1\big[t_{\text{seat}}\le T\big],\qquad r_T=\sqrt{x_T^2+y_T^2},$$

구멍은 리드인 안에 떨어져야 하고, 리드인이 바로잡는 동안 목표를 붙든 강성 $K$를 거쳐 건물을 $F_{\lim}=20\,\mathrm{N}$보다 세게 밀어서는 안 되며, 단계는 제시간에 끝나야 하기 때문이다. $500\,\mathrm{N/m}$ 임피던스를 거치면 둘째 조건은 저절로 지켜진다. 리드인 가장자리에서의 안착이 $500\times0.004=2\,\mathrm{N}$이기 때문이다. 단단한 $10^5\,\mathrm{N/m}$ 루프를 거치면 $r_T\le0.2\,\mathrm{mm}$만 허용되고, 그것이 §6의 주제다. 셋째 조건은 멈추거나 물러서는 정책을 떨어뜨린다. 랩의 하강은 멈추지 않으므로 거기서는 늘 지켜진다.

**누가 시연했는가.** 조작자는 근접 화면이 보여 주는 것의 절반을 바로잡는다. $u=-0.5\,(x+\nu)+\eta$이고, 로그는 화면이 아니라 카메라의 어긋남과 명령을 남긴다. 조작자의 폐루프는 보정이 크리프를 상쇄하는 곳에 자리 잡는다. $m=(1-0.5)\,m+0.2$이므로 벽을 따라 $m=0.4\,\mathrm{mm}$이고, 분산은 같은 균형을 푼다.

$$s^2=\frac{k_E^2\sigma_\nu^2+\sigma_\eta^2+\sigma_w^2}{1-(1-k_E)^2}=\frac{0.0025+0.01+0.01}{0.75}=0.030,\qquad s=0.173\,\mathrm{mm},$$

그래서 조작자의 안착은 벽을 따라 $0.4\pm3\times0.173=[-0.12,\ 0.92]\,\mathrm{mm}$ 안에 놓인다. 스텝마다 이어지는 이 띠가 *시연 회랑*(demonstrated corridor)이다. 시연이 덮는 영역이고 그림의 음영 띠다. 그 밖에서 적합한 정책은 자료가 거의 또는 전혀 없고, [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]]이 지지집합을 벗어난다고 부르는 것이 그것이다. 아무 보정이 없으면 크리프만으로 구멍이 $8\,\mathrm{mm}$ 움직이고, 조작자의 보정이 있으면 매번 앉는다(§9: $1.000$, 안착의 $95\%$가 $0.71\,\mathrm{mm}$ 안). 이 페이지의 물음은 로그에 맞춘 정책이 그중 얼마를 지키느냐다.

### 2. 접촉 위의 행동 복제

*한 문장으로:* 행동 복제는 기록된 쌍 하나하나를 정책이 만날 상태에서 독립으로 뽑은 것처럼 조작자의 명령에 맞추는데, 움직이는 정책은 두 조건 모두를 만나지 못한다.

> **행동 복제의 정의.** **행동 복제**(behaviour cloning, BC)는 *학습 목적함수*다. 정책이 관측하는 것에 대해 시연자의 명령을 지도 회귀하는 것이다. 아키텍처도, 정책 계열도, 모방학습 일반도 아니다. 정의 조건 셋은 [[03-deep-learning/vla/index|VLA §2]]의 셋을 접촉에 맞춰 쓴 것이다. 자료는 **시연자가 만든 (관측, 명령) 쌍**이므로 모든 라벨은 명령이고, return도 정책이 느껴야 할 힘도 아니다. 손실은 **명령에 대한 지도 불일치뿐**이고, 보상 없이, 정책이 움직이지 않은 채 맞춘다. 그리고 평균은 **시연자의 상태 분포 위에서** 취한다. 지도학습의 i.i.d. 가정이 들어오는 곳이 여기다. 적합은 쌍들을 정책이 평가받을 분포에서 독립으로 뽑은 것처럼 다룬다.
>
> $$\hat\theta=\arg\min_\theta\ \frac1N\sum_{i=1}^{N}\big\lVert u_i-\pi_\theta(o_i)\big\rVert^2,\qquad (o_i,u_i)\sim d_{\pi^*}$$
>
> $u_i$는 조작자의 명령, $o_i$는 기록된 카메라 어긋남, $\pi_\theta$는 정책, $d_{\pi^*}$는 조작자 자신의 안착이 지나는 상태의 분포다. 제곱 오차는 [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]]의 가우시안 최대우도이므로, 그 안의 어떤 항도 정책이 스스로 도달한 상태를 본 적이 없다.
>
> - **예**: §9의 표. 40스텝짜리 안착 88개가 축마다 $3{,}520$쌍을 주고, (스텝, 카메라 어긋남의 $0.25\,\mathrm{mm}$ 구간) 칸마다 지시 특성 하나를 둔 최소제곱으로 맞춘다. 지시 특성이면 정규방정식이 대각이므로 각 칸의 명령은 그 칸에 떨어진 조작자 명령의 평균이고, 아무것도 떨어지지 않은 칸은 $0$을 돌려준다.
> - **비예**: 조작자가 *정책*이 도달한 상태에 라벨을 붙인 뒤 다시 맞춘 같은 표. 손실은 같지만 셋째 조건의 분포가 학습자의 것이다. 그것은 DAgger(§5)이고, 비용이 다른 다른 알고리즘이다.
> - **왜 중요한가**: 떼어 둔 시연 위의 손실은 셋째 조건의 숫자이고 [[02-foundations/ml-practice|9. ML Practice §5]]의 열린 루프 평가다. 안착률은 폐루프 숫자이고, 이 페이지 전체가 둘의 차이 안에 산다.

**움직임이 가정을 깨는 방식.** Ross, Gordon, Bagnell은 논문을 이 문장으로 연다. 미래 관측이 이전 행동에 달린 모방학습 같은 순차 예측은 통계적 학습의 i.i.d. 가정을 어긴다. S1에서는 두 번 깨진다. 쌍들은 *독립이 아니다*. 한 안착의 40쌍은 시작 어긋남과 흔들림의 이력을 함께 나누고, 각 상태는 직전 상태에 명령을 더한 것이다. 그리고 정책이 만나는 것과 *같은 분포가 아니다*. 정책이 움직이기 시작하면 상태는 자기 분포 $d_\pi$에서 나온다. [[02-foundations/ml-practice|9. ML Practice §1]]의 뜻의 공변량 이동이고, 입력은 움직여도 각 상태의 올바른 명령은 그대로다.

**로그가 담지 않은 것.** 접촉은 셋째로 깨지는 자리를 더한다. [[04-robotics/teleoperation-demonstration|12. §6]]의 상태–행동 일관성이다. 조작자는 로그가 남기지 않은 근접 화면을 보고 움직였다. 코퍼스가 넓은 곳에서는 카메라가 여전히 명령을 예측하지만, 좁은 곳에서는 거의 예측하지 못한다. 단계 후반에 실제 어긋남은 $s^2=0.03$으로 흩어지는데 카메라는 $\sigma_v^2=0.25$를 더하므로, 카메라로 어긋남을 가장 잘 예측하는 값은 읽을 때마다 분산 가운데 신호의 몫만큼 줄어든다.

$$g=\frac{s^2}{s^2+\sigma_v^2}=\frac{0.03}{0.03+0.25}=0.107,$$

그래서 복제된 보정은 조작자의 $0.5$ 대신 스텝마다 $0.5\times0.107=0.054$다. 어긋남이 $1.35\,\mathrm{mm}$로 흩어진 단계 초반에는 $g=0.879$, 복제 이득은 $0.44$다. 선형 루프로 읽으면, 약한 후반 이득은 복제한 구멍을 조작자의 $0.4\,\mathrm{mm}$에 두되 $0.173$ 대신 $0.32\,\mathrm{mm}$로 퍼뜨리고, 회랑의 $0.92\,\mathrm{mm}$ 가장자리 너머에 있는 시간이 조작자의 $0.13\%$ 대신 약 $5\%$가 된다. 랩은 그 결과를 곧바로 잰다. 조작자 자신의 상태에서 채점하면 적합한 표는 스텝의 $0.0225$에서 조작자라면 내리지 않았을 명령 — $-0.5x$에서 $3\sigma_\eta=0.3\,\mathrm{mm}$보다 먼 명령 — 을 내고, 자기 상태에서 채점하면 $0.233$에서 낸다. 조작자가 기록되는 카메라만 보게 해서 조작자가 보고 움직인 모든 것이 로그에 남는 코퍼스는 문제의 대부분을 없앤다. 그 코퍼스에 맞춘 BC는 $0.875$ 대신 $0.953$으로 앉는다(§9).

### 3. 밀리미터로 잰 복합 오차

*한 문장으로:* 복제 정책이 조작자의 상태에서 보이는 오류율은 정책이 움직이면 지평에 두 번 곱해진다. 오류 하나가 아무것도 보여 준 적 없는 곳에 정책을 둘 수 있기 때문이다. 자기가 가는 곳에서 학습한 학습자는 한 번만 곱한다.

> **복합 오차의 정의.** **복합 오차**(compounding error)는 학습 손실의 성질이 아니라 *지평에 걸쳐 폐루프로 도는 정책의 성질*이다. 시연자의 상태에서 잰 스텝당 오류가 예측하는 것을 넘어 지평 $T$와 함께 커지는 기대 비용이다. 정의 조건 셋. **스텝당 오류는 시연자의 분포에서 잰다**. $\epsilon=E_{s\sim d_{\pi^*}}[\ell(s,\pi)]$이고 $\ell$은 시연자라면 내리지 않았을 명령의 0-1 손실이다. **오류가 뒤따르는 상태를 바꾼다**. 그래서 정책은 자기 $d_\pi$에서 평가받는다. 그리고 정책은 **오류가 데려가는 곳에 자료가 없다**. 시연의 지지집합 밖이므로 오류 하나 뒤에 오류가 더 올 수 있다. Ross, Gordon, Bagnell의 정리 2.1은 — 그들이 Ross와 Bagnell(2010)의 것으로 밝힌 — 복제 정책의 비용을 이차로 묶고, 그들은 이 상한이 빡빡하다고 적는다. 어떤 문제는 거기에 닿고, 세 조건이 그리로 가는 길이다. 그들의 정리 3.2는 반복을 충분히 돌린 DAgger의 비용을 일차로 묶는다.
>
> $$J(\pi)\le J(\pi^*)+T^2\epsilon\ \ \text{(BC)},\qquad J(\hat\pi)\le J(\pi^*)+u\,T\,\epsilon_N+O(1)\ \ \text{(DAgger)}$$
>
> $J$는 $[0,1]$ 안의 스텝당 비용을 $T$스텝에 걸쳐 더한 것, $\pi^*$는 시연자, $\epsilon_N$은 $N$번의 DAgger 반복이 지난 상태들에서 정책 계열이 도달하는 가장 작은 평균 스텝당 오류, $u$는 틀린 명령 하나가 남은 비용을 얼마나 올리는지의 상한이다. 그래서 이차항은 셋째 조건의 값이고, 자기가 가는 곳에서 학습한 학습자는 일차로 치른다.
>
> - **예**: 시연 회랑 밖에서 보낸 스텝마다 비용 $1$을 매긴 S1. 조작자의 $J(\pi^*)\approx0$이다. 조작자는 스텝의 $0.27\%$에서, 안착당 약 $0.11$스텝 $\pm3\sigma$ 띠를 벗어난다. $\epsilon=0.02$, $T=40$이면 BC의 상한은 $40$스텝 가운데 $T^2\epsilon=32$스텝 표류다. DAgger의 상한은 $\epsilon_N=0.02$로 두고 $O(1)$ 항을 무시하고 $u=1$로 두면 $0.8$인데, 이 $u$ 값은 구멍을 $1.44\,\mathrm{mm}$ 안에 두는 오류에서 성립한다. 조작자의 한 스텝, $0.5x+0.2\le0.92$가 그것을 회랑 안으로 되돌리기 때문이다.
> - **비예**: 평균 시연을 열린 루프로 재생하는 것. 오류가 커지기는 하지만 상태를 보지 않으므로 둘째 조건이 깨진다. 이동할 분포가 없고, 어떤 자료로도 고칠 수 없는 표류만 있다.
> - **왜 중요한가**: 지평이 설계 변수가 된다. 단계를 줄이거나 명령을 청크로 묶으면(§4) 오류가 복합되는 길이가 줄고, DAgger는 제곱을 없애며(§5), 어디서나 바로잡는 기본 제어기는 셋째 조건을 없앤다(§7).

**S1 위의 최악의 경우.** 정리의 최악의 경우는 첫 오류 뒤로 다시 돌아오지 못하는 정책이다. S1에서는 그것이 물리적 모양을 갖는다. 회랑 밖에서 적합한 표는 아무것도 가지고 있지 않으므로 보정을 멈추고, 크리프가 스텝마다 $0.2\,\mathrm{mm}$를 더한다. 구멍은 회랑 가장자리 $b=1\,\mathrm{mm}$($0.92$를 올림)에서 떠나므로 리드인은 표류 $(4-1)/0.2=15$스텝을 받아 준다. 스텝 $\tau$의 첫 오류는 그 오류의 스텝을 포함해 $N_{\text{off}}=T-\tau+1$스텝의 표류를 남기고, 첫 오류가 스텝 $\tau$에 떨어질 확률은 $\epsilon(1-\epsilon)^{\tau-1}$이므로

$$E[N_{\text{off}}]=\sum_{\tau=1}^{T}\epsilon\,(1-\epsilon)^{\tau-1}\,(T-\tau+1)=12.84\ \text{스텝},$$

곧 기대 표류 $12.84\times0.2=2.57\,\mathrm{mm}$로, 리드인이 남겨 둔 $3\,\mathrm{mm}$의 $86\%$다. 그 일차 형태 $\epsilon T(T+1)/2=16.4$스텝이 정리의 제곱을 드러내 보이고, 상한 자체는 $32$스텝이고, 표류 스텝마다 정확히 $c$가 더해지는 모델에서는 $6.4\,\mathrm{mm}$다.

**지평.** 표류 스텝의 상한을 리드인이 받아 주는 $15$ 안에 두려면 $T^2\epsilon\le15$, 곧 $T\le\sqrt{15/0.02}=27.4$스텝이어야 한다. 상한은 $40\,\mathrm{mm}$가 아니라 $27\,\mathrm{mm}$ 단계를 덮는다. DAgger의 $uT\epsilon_N\le15$는 같은 $u=1$, $\epsilon_N=0.02$로 두고 $O(1)$ 항을 무시하면 $T=750$스텝까지 성립한다. 정확히 계산하면 기대 표류 스텝은 $T=44$에서 $15$에 이르므로, $40$스텝 단계는 평균으로는 리드인 안에 겨우 들어온다 — 그리고 평균은 꼬리를 감춘다. 안착하려면 첫 오류가 마지막 $15$스텝에 와야 하므로 그 확률은 $(1-\epsilon)^{T-15}$다. $20\,\mathrm{mm}$ 단계에서 $0.904$, $40$에서 $0.603$, $60$에서 $0.403$, $80$에서 $0.269$이고, $T=21$부터 $0.9$ 아래다. 계산 절이 이 숫자들을 끝까지 끌고 가고, §9는 적합한 표 자신의 두 오류율, 조작자 상태에서 $0.0225$와 자기 상태에서 $0.233$을 잰다. 정리의 두 분포가 숫자가 된 것이다.

### 4. 시연자 둘, 평균 하나

*한 문장으로:* 조작자들이 두 경로로 브래킷에 이를 때, 평균 명령으로 회귀하는 헤드는 그 사이로 몰고 가며, 헤드가 한 경로를 붙들 수 없으면 청크도 그것을 바꾸지 못한다.

**두 경로.** 마지막 $40\,\mathrm{mm}$ 전에, S1의 코퍼스는 12의 로그와 같은 다봉성을 갖는다. 비계 연결재가 브래킷으로 가는 직선을 가로지르고, 조작자들은 패널의 아래 모서리를 그 왼쪽이나 오른쪽 $60\,\mathrm{mm}$로 지나게 하며, 둘 다 반폭 $10\,\mathrm{mm}$의 틈을 지난다. 앉은 시도 96개는 왼쪽 $58$, 오른쪽 $38$로 나뉜다. 제곱 오차로 학습한 단봉 헤드는 조건부 평균을 돌려준다. 제곱 오차를 최소로 만드는 것이 평균이기 때문이다([[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]], D4(딥러닝 트랙의 행동 청크, [[03-deep-learning/lab-objects|0. Lab Objects]]) 위의 같은 실패는 [[03-deep-learning/vla/index|VLA §2]]).

$$\bar u=\frac{58\times(-60)+38\times60}{96}=-12.5\,\mathrm{mm},$$

가까운 경로에서 $47.5\,\mathrm{mm}$, 그 틈에서 $37.5\,\mathrm{mm}$ 벗어난 곳 — 연결재 속이다. 어느 조작자의 서툰 판도 아니고, 어느 쪽도 아니다. 코퍼스의 모드 엔트로피 $0.968$비트는 두 경로가 거의 균형이라는 것을 말할 뿐 갈라져 있다는 것을 말하지 않는다. $48/48$로 균형을 맞추면 엔트로피는 $1.000$이 되고 평균은 둘 모두에서 $60\,\mathrm{mm}$ 떨어진 $0\,\mathrm{mm}$로 간다([[04-robotics/teleoperation-demonstration|12. §6]]).

**다봉 헤드가 바꾸는 것.** 평균이 아니라 분포를 표현하는 헤드 — 샘플링하는 토큰, 노이즈 제거기, 잠재변수를 표본으로 뽑는 디코더([[03-deep-learning/vla/index|VLA §6]]) — 는 $-60$에 $0.604$, $+60\,\mathrm{mm}$에 $0.396$의 질량을 두고, 표본 하나가 경로 하나다. Diffusion Policy의 초록은 다봉 행동 분포를 매끄럽게 다룬다는 점을 이 정식화의 장점으로 꼽는다([[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]). 그러나 패널이 아직 갈림길에 있는 동안 스텝마다 다시 고르는 헤드는 연속한 두 결정 사이에서 확률 $2\times0.604\times0.396=0.478$로 경로를 바꾼다. 연결재 앞에서 머뭇거린다. 패널이 한쪽으로 들어서면 카메라 자신이 어느 경로에 있는지 말해 주므로 모호함은 사라진다. 위험은 갈림길에서 내리는 결정들이다.

**청크가 바꾸는 것.** 청크는 관측 하나에 명령 여럿을 묶는다([[03-deep-learning/vla/index|VLA §3]]). 다봉 헤드라면, 패널을 연결재 너머로 데려갈 만큼 긴 청크가 경로를 확정한다. 단봉 헤드라면 청크는 평균 궤적이고 여전히 연결재를 지난다. [[01-canonical-papers/notes/4-vla/act|ACT]]는 시연자들의 변동이 적합을 흐리지 않도록 청크를 CVAE로 학습하지만, 시험 때는 잠재변수를 사전분포의 평균인 영에 고정하고 결정론적으로 디코딩한다. 실행 중에 경로를 고르는 것은 없고, 겹치는 청크의 시간 앙상블은 갈림길 근처에서 두 경로를 다시 평균으로 되돌릴 수 있다. 청크는 §3의 지평도 줄인다. 청크의 오류율이 스텝의 $0.02$와 같다면, $5$스텝마다 결정하면 결정 $8$개 가운데 처음 $5$개가 치명적이어서 $0.98^5=0.904$, $10$스텝마다면 $4$개 가운데 처음 $3$개가 치명적이어서 $0.98^3=0.941$로, 스텝마다의 $0.603$보다 높다. 정확히 스텝의 비율은 아니다. 청크는 열린 루프로 달리기 때문이다. 크리프를 예측해야 하고 흔들림은 보지 못하며, $10$스텝 동안 흔들림만으로 구멍이 $0.1\sqrt{10}=0.32\,\mathrm{mm}$ 퍼진다.

### 5. 현장의 DAgger

*한 문장으로:* DAgger는 정책이 몰게 두고, 정책이 도달한 모든 상태에서 조작자가 무엇을 명령했을지 말하게 하고, 그 라벨을 코퍼스에 더해 다시 맞춘다 — 그리고 현장에서는 라운드마다 조작자의 시간이 들고 학습자의 오류가 실제 건물 곁에 놓인다.

> **DAgger의 정의.** **DAgger**(dataset aggregation; Ross, Gordon, Bagnell, 2011)는 손실도 정책 계열도 아닌, *자료를 모으고 학습하는 반복 절차*다. 정의 조건 넷. 라운드 $i$에서 로봇은 시연자와 현재 학습자의 **혼합** $\pi_i=\beta_i\pi^*+(1-\beta_i)\hat\pi_i$를 돌린다. 시연자는 **혼합이 지난 모든 상태에** 거기서 내렸을 명령으로 라벨을 붙인다. 자기가 조종하고 있었든 아니든 그렇다. 새 쌍은 이전의 모든 쌍에 **모아 더하고**, 그것들과 바꾸지 않는다. 그리고 다음 학습자는 BC와 같은 지도 손실로 **모은 전체에서 학습한다**.
>
> $$\mathcal D\leftarrow\mathcal D\cup\big\{(o,\pi^*(s)):\ s\sim d_{\pi_i}\big\},\qquad \hat\pi_{i+1}=\arg\min_\pi\sum_{(o,u)\in\mathcal D}\big\lVert u-\pi(o)\big\rVert^2$$
>
> $d_{\pi_i}$는 혼합이 도달하는 상태의 분포, $o$는 상태 $s$의 기록된 관측, $\pi^*(s)$는 시연자의 라벨이다. Ross 등은 보통 $\beta_1=1$로 두어 첫 라운드를 시연 자체로 삼고, 뒤의 라운드에는 $\beta_i=p^{i-1}$이나 파라미터 없는 $\beta_i=\mathbb 1[i=1]$을 제시한다. 그래서 학습 분포가 정책이 달릴 분포 쪽으로 당겨진다.
>
> - **예**: S1 위의 §9 라운드. 시연 88개가 영 번째 라운드다. 라운드마다 현재 표가 안착을 $20$번 시도하고, 조작자는 그 시도가 지나는 상태 $800$개 모두에 근접 화면이 요구하는 명령으로 라벨을 붙이고, 표는 지금까지의 모든 것에서 다시 맞춘다. 두 라운드가 안착률을 $0.875$에서 $0.980$으로 올린다.
> - **비예**: 시연 $88$개 더. 그 상태도 여전히 $d_{\pi^*}$에서 나오므로 둘째 조건이 깨진다. §9가 값을 매긴다. 코퍼스를 두 배로 하면 $0.940$이다.
> - **왜 중요한가**: 학습자가 고른 상태에서 시연자의 라벨을 사서 §3 정의의 셋째 조건을 없앤다. 현장에서는 그 구매에 알고리즘이 보여 주지 않는 비용이 붙는다.

**라운드 하나의 값.** 12의 로그는 시도 $120$번에 $4.0\,\mathrm{h}$가 걸렸다. 시도당 $120\,\mathrm{s}$이고, 폐기되고 실패한 것까지 치르면 사용 가능한 시연당 $164\,\mathrm{s}$다. DAgger의 시도는 앉든 못 앉든 라벨이 붙는다 — 그 실패가 바로 모으려는 라벨이다 — 그래서 시도당 $120\,\mathrm{s}$이고 시도 $20$번짜리 라운드 하나는 $40\,\mathrm{min}$이다. §9의 숫자로는 이렇다.

| 조작자 시간 | 정책 | 안착(§9) |
|---:|---|---:|
| $4.0\,\mathrm{h}$ | 시연 88개 위의 BC | $0.875$ |
| $4.7\,\mathrm{h}$ | DAgger 한 라운드 | $0.950$ |
| $5.3\,\mathrm{h}$ | 두 라운드 | $0.980$ |
| $6.7\,\mathrm{h}$ | 네 라운드 | $0.995$ |
| $8.0\,\mathrm{h}$ | 시연 176개 위의 BC | $0.940$ |
| $16.0\,\mathrm{h}$ | 시연 352개 위의 BC | $0.960$ |

두 라운드, 80분의 시도가 열두 시간 넘게 더 모은 시연보다 많은 것을 산다. 조작자가 결코 실패하지 않는 곳이 아니라 정책이 실패하는 곳에 쓰이기 때문이다. 12의 복구 포함률 $11/88=0.125$는 조작자들이 우연히 보여 준 복구를 센다. DAgger의 라벨은 이 정책이 실제로 도달하는 상태에서의 복구다.

**알고리즘이 보여 주지 않는 것.** 첫째, 학습자가 몬다. DAgger에 필요한 상태는 정책이 틀려서 도달하는 상태이고, S1에서 그것은 건물에 볼트로 고정된 브래킷 위에서 회랑을 벗어난 $196\,\mathrm{N}$ 패널이다. 한 라운드 뒤에도 채점한 시도의 $5\%$는 핀에 $4\,\mathrm{mm}$보다 크게 어긋난 채 닿았다. 정렬 단계에서 놓침은 후퇴 후 재스캔으로 되돌릴 수 있고([[05-construction-robotics/site-engineering|2.5 §1]]), §7의 한계가 그것을 그렇게 지켜 준다. 라운드는 목업에서, 아니면 그 한계 뒤에서 돌려야 한다. 둘째, 라벨은 조종하지 않은 채 붙인다. Kelly 등의 HG-DAgger는 여기서 출발한다. DAgger의 표본 추출은 전문가가 시스템을 완전히 조종하지 않은 채 라벨을 붙이도록 요구하는데, 이는 안전을 떨어뜨릴 수 있고, 사람 전문가라면 느껴지는 구동기 지연 때문에 라벨의 질도 떨어뜨릴 가능성이 크다. 그들의 변형에서는 초심자 정책이 몰다가 전문가가 안전하지 않은 영역에 들어섰다고 판단하면 전문가가 조종을 넘겨받아 되돌리고, 라벨은 전문가가 끊김 없이 조종하는 그 복구 동안에만 모은다. S1에서 보통의 DAgger는 조작자가 패널을 움직이지 않는 리더를 움직여 라벨을 붙이게 하는데 — HG-DAgger가 피하는 바로 그 상황이다. 셋째, $\beta$다. §9는 파라미터 없는 일정, 곧 코퍼스를 영 번째 라운드로 두고 그 뒤로는 학습자만 쓰는 일정을 쓴다.

### 6. 행동은 무엇이어야 하나: 위치 목표냐 임피던스 목표냐

*한 문장으로:* 학습한 보정은 목표를 붙든 것을 거쳐 힘이 되므로, 행동이 오차 1밀리미터가 백 뉴턴이 될지 반 뉴턴이 될지를 정하고, 시연이 어떤 힘을 기록했어야 하는지도 정한다.

> **임피던스 목표의 정의.** **임피던스 목표**(impedance target)는 가상 스프링을 어디에 매고 얼마나 단단하게 할지를 이름 짓는 *행동*, $a=(x_d,\,K)$다. 고전 임피던스 제어기가 자기 주기로 그것을 구현한다([[04-robotics/force-compliance-control|13. §2]]). 로봇이 도달해야 할 자세가 아니다. 정의 조건 셋. 정책은 **자세가 아니라 고정점을 명령한다**. 공구가 실제로 어디에 놓일지는 접촉이 정한다. **강성이 행동의 일부다**. 고정이든 정책이 고르든, 정책은 오차와 힘 사이의 관계를 명령한다. 그리고 **정책 아래의 제어기가 루프를 닫는다**. 정책이 돌지 않는 주기로 닫으므로 접촉력은 정책의 결정 사이에서 모양이 잡힌다.
>
> $$F=K\,(x_d-x)$$
>
> $x$는 공구가 있는 곳, $x_d$는 명령한 고정점, $K$는 명령한 강성이다. 그래서 고정점의 오차는 $K$배가 되어 건물에 닿고, 같은 1밀리미터가 다른 $K$에서는 다른 힘이다.
>
> - **예**: $K_d=500\,\mathrm{N/m}$인 S1의 옆 방향 목표. 리드인이 옆으로 $3.29\,\mathrm{mm}$ 미는 구멍은 $500\times0.00329=1.6\,\mathrm{N}$이 들고, $4\,\mathrm{mm}$ 리드인 안의 모든 안착은 $2\,\mathrm{N}$ 아래다.
> - **비예**: 단단한 제조사 루프로 들어가는 위치 목표. 정책의 출력은 똑같이 자세로 보이지만 강성은 루프의 $10^5\,\mathrm{N/m}$이므로, 같은 $3.29\,\mathrm{mm}$가 패널 무게의 $1.7$배인 $329\,\mathrm{N}$이 든다(9의 3단계).
> - **왜 중요한가**: [[04-robotics/force-compliance-control|13. §6]]은 학습 층이 컴플라이언스를 명령하고 그 구현은 고전 루프에 맡겨야 한다고 논한다. S1에서는 그것이 숫자가 된다. $20\,\mathrm{N}$ 한계 아래에서 단단한 루프는 안착 때 $0.2\,\mathrm{mm}$를, 임피던스는 리드인 전체를 허용한다.

**조작자도 단단한 루프에서는 떨어진다.** 조작자 자신의 안착은 $95\%$가 $0.71\,\mathrm{mm}$ 안에 떨어지고(§9), 단단한 루프를 거치면 그것은 $10^5\times0.00071=71\,\mathrm{N}$, 임피던스를 거치면 $0.36\,\mathrm{N}$이다. 단단한 루프로 $20\,\mathrm{N}$ 아래에 머물려면 $r_T\le0.2\,\mathrm{mm}$여야 하는데, 크리프만으로도 조작자의 어긋남은 벽을 따라 $0.4\,\mathrm{mm}$에 중심을 둔다. 단단한 루프로 들어가는 위치 목표라면 이 페이지의 어떤 정책도, 시연자까지도 §1의 둘째 조건을 믿을 만하게 지키지 못한다. 임피던스 목표라면 앉은 정책은 모두 지킨다. 그래서 §9는 모든 정책을 임피던스를 거쳐 채점한다.

**시연이 담아야 하는 것.** 안착 뒤에는 지지가 오고, 지지는 패널의 무게가 로봇에서 체결재로 옮겨 가며 끝난다. 작업자가 체결하는 동안 로봇이 $196\,\mathrm{N}$을 들고 있다가, 놓기 시험을 통과한 뒤에야 놓는다([[05-construction-robotics/hrc-worker-centered|6. HRC §7]]). 지지 단계의 수직 목표 강성 $K_z=10^4\,\mathrm{N/m}$로 $196\,\mathrm{N}$을 들면 고정점은 잡은 점보다 $196.2/10^4=19.6\,\mathrm{mm}$ 위에 있다. 체결된 패널에 하중을 넘기면 고정점이 그 $19.6\,\mathrm{mm}$만큼 내려가는데, 이제 체결재가 붙든 패널은 전혀 움직이지 않는다. 위치 로그는 작업에서 가장 중대한 몇 초 동안 아무것도 기록하지 않고, 위치로 복제한 정책은 공구가 있던 곳을 명령하도록 배운다 — 무게를 영원히 들고 있는 명령이다. 고정점은 힘에서 되살려야 한다. $x_d=x+F/K$다. DexForce가 정확히 이것을 다지 로봇 손에 대해 한다. 접촉력을 잰 운동감각 시연에서, 관측한 손끝 위치에 손으로 조정한 파라미터와 잰 접촉력의 곱을 더해 힘을 반영한 목표를 계산하고, 그 목표로 학습한 정책이 여섯 작업에서 평균 $76\%$로 성공하는 반면 관측한 위치로 학습한 정책은 거의 영에 가까웠다고 보고한다. 그러니 S1의 로그는 손목 힘이나 조작자가 명령한 고정점을 자세와 동기화해 담아야 한다([[04-robotics/teleoperation-demonstration|12. §4.5]]: 인터페이스가 기록하는 것과 버리는 것). [[04-robotics/force-compliance-control|13. §6]]이 두 번 도착한다고 말한 행동 공간의 물음이다. 원격조작자가 명령하는 것에서 한 번, 정책이 내놓는 것에서 한 번.

### 7. 현장이 한계를 긋는 학습 잔차

*한 문장으로:* 고전 루프를 기본으로 두고, 학습한 정책은 현장이 정한 한계로 자른 보정만 더하게 하고, 작업자가 있으면 그 한계를 좁힐 수는 있어도 넓힐 수는 없게 한다.

**기본 제어기.** 로보틱스 캡스톤은 패널이 어디 있는지 추정하고, 접촉 전에 임피던스로 전환하고, 누른다([[04-robotics/capstone-panel-contact|26. §4]]). 패널은 단 한 번 읽는다([[04-robotics/capstone-panel-contact|26. §7]]). 같은 루프를 S1에서 스텝마다 돌리면, 카메라가 보여 주는 것의 고정된 몫만큼 옆 방향 목표를 옮긴다. $u_0=-k_0\,o_t$, $k_0=0.25$이고 $500\,\mathrm{N/m}$ 임피던스를 거친다. 시연이 필요 없고, 아무도 시연하지 않은 상태까지 포함해 어디서나 바로잡는다.

**잔차.** [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §8]]이 정의한 잔차 정책은 그 기본 제어기를 고정하고 한계로 자른 학습 보정을 더한다.

$$u_t=-k_0\,o_t+\operatorname{clip}\big(r_\phi(t,o_t),\,-B,\,B\big),$$

그래서 보정이 무엇을 내놓든 명령은 행동을 아는 제어기에서 $B$ 안에 머문다. Silver 등과 Johannink 등은 둘 다 기존 제어기 위에 한계 없는 보정을 강화학습으로 배우고, clip은 7.5 Sim-to-Real §8이 더한 것이다. 여기서는 $r_\phi$를 같은 시연 88개에서 조작자의 명령에서 기본 제어기의 명령을 뺀 것에 §2의 최소제곱으로 맞춘다. 빈 칸이 돌려주는 영은 이제 폭주가 아니라 기본 제어기의 보정이다. 이 하나의 변화가 같은 코퍼스, 같은 적합을 $0.875$에서 $1.000$으로 올린다(§9).

**한계가 보장하는 것.** 잔차가 할 수 있는 최악은 매 스텝 $+B$로 미는 것이다. 기본 제어기는 어긋남의 $k_0$배만큼 되당기고, 벽을 따라서는 크리프가 $c$를 더하므로, 평균 어긋남은 당김과 밂이 균형을 이루는 곳에 자리 잡는다.

$$\bar x_\infty=\frac{B+c}{k_0}=\frac{0.3+0.2}{0.25}=2.0\,\mathrm{mm},\qquad \bar y_\infty=\frac{B}{k_0}=\frac{0.3}{0.25}=1.2\,\mathrm{mm},$$

신경망이 무엇을 내놓든 핀에서 $2.33\,\mathrm{mm}$이고, 기본 루프의 퍼짐 $\sqrt{(k_0^2\sigma_v^2+\sigma_w^2)/(1-(1-k_0)^2)}=0.242\,\mathrm{mm}$로 보면 리드인 안쪽으로 표준편차 $6.9$개다. 기본 제어기만 쓰면($B=0$) $c/k_0=0.8\,\mathrm{mm}$에 자리 잡고, 안착의 $95\%$가 $1.24\,\mathrm{mm}$ 안에 들며 $1.000$으로 앉는다. 잔차는 그것을 $1.08\,\mathrm{mm}$로 좁힌다. $B$는 얼마까지 커도 되는가? 최악의 경우를 리드인 안쪽으로 표준편차 네 개만큼 두려면 $\sqrt{((B+0.2)/0.25)^2+(B/0.25)^2}\le4-4\times0.242=3.03\,\mathrm{mm}$이어야 하므로 스텝마다 $B\le0.43\,\mathrm{mm}$다. 7.5 Sim-to-Real §8의 S2(건설 트랙의 트렌치 굴착 과제, [[05-construction-robotics/site-engineering|2.5]]) 흙에서처럼, 숫자 하나가 잔차가 고칠 수 있는 것과 틀린 잔차가 구멍을 데려갈 수 있는 거리를 맞바꾼다.

**작업자.** 안착은 지지·체결 직전의 마지막 스텝이고, 작업자는 패널을 이끌려고 일찍 손을 뻗을 수 있다. [[05-construction-robotics/hrc-worker-centered|6. HRC §8]]은 작업자에 대한 추정이 할 수 있는 일을 정한다. 허용 집합은 잰 상태와 최악의 인간 항으로만 계산하고, 추정은 그 안에서 고르기만 한다. S1에서 $B$는 그 집합에 속한다. [[05-construction-robotics/hrc-worker-centered|6. §6]]의 추적기가 패널에 손이 닿는 거리 안의 사람을 재면 $B$는 $0$으로 떨어지고, 안착은 기본 제어기만으로 끝난다. §9에서 그것은 매번 앉고 $95\%$가 $1.24\,\mathrm{mm}$ 안이다. 좁히는 값은 정밀도이지 안전이 아니다. 작업자가 주의를 기울이고 있다는 추정은 하강을 늦추거나 $B$를 더 줄일 수는 있어도, $B$를 $0.3$보다 올릴 수는 없다. 한계는 안전 기능이 아니다 — 정지는 여전히 6 §6의 정지 사슬이 맡는다 — 그러나 정책의 최악의 경우를 안전 기능이 가정하는 범위 안에 붙들어 둔다. §6의 임피던스 목표는 지지 단계 자신의 행동이기도 하다. [[05-construction-robotics/hrc-worker-centered|6. §7]]이 정한 대로 벽을 따라서는 무르게, 중력에 맞서서는 단단하게다.

### 8. 주장 평가하기

*한 문장으로:* 안착률은 구간을 가진 셈이고, 학습한 정책은 코퍼스를 한 번 뽑은 것이며, 그것을 잰 사다리 단이 그 정책이 어떤 시작점을 만났는지 정한다.

**셈과 그 구간.** 성공률은 $n$번 시행에서 $k$번의 성공이고, 그 불확실성은 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]](계산 절 2단계)가 정의한 Wilson 구간이다. 이 구간은 $[0,1]$을 벗어나지 않는다. §9의 BC는 $2{,}000$번 가운데 $1{,}750$번 앉는다. $[0.860,\ 0.889]$다. 목업에서 스무 번 가운데 열아홉 번은 $[0.764,\ 0.991]$로, 거의 넷에 하나인 실패율과도 양립한다([[03-deep-learning/vla/index|VLA §4]]가 10회 표를 같은 방식으로 읽는다).

**실패 없는 연속.** $n$번 시행에 실패가 없으면 $(1-p)^n\le0.05$일 때 실패율 $p$가 $95\%$로 배제되므로

$$n\ge\frac{\ln0.05}{\ln(1-p)},$$

$(1-p)^n$이 그 비율에서 $n$번 연속 성공할 확률이기 때문이다. BC의 $12.5\%$를 배제하려면 $23$번, $5\%$는 $59$번, 9의 $2.4\%$는 $124$번, DAgger의 $0.5\%$는 $598$번 연속 안착해야 한다([[06-research-practice/experimental-design-reproducibility|실험 설계 §4]]는 큰 $n$에 대한 3의 규칙 $n\approx3/p$을 준다). §9의 BC와 네 번째 DAgger 라운드를 각자의 비율 $0.875$와 $0.995$에서 구별하려면, 두 Wilson 구간이 갈라지기까지 정책마다 $65$번의 시행이 든다.

**정책은 코퍼스를 한 번 뽑은 것이다.** 위의 구간은 학습한 정책 하나의 롤아웃을 덮는다. 시연 88개짜리 다른 코퍼스 다섯 개로 BC를 다시 맞추면 $0.817$에서 $0.879$가 나온다(§9). 퍼짐 $0.062$가 구간의 반폭 $0.015$보다 크다. 시드는 소프트웨어의 무작위성만 담으므로([[06-research-practice/experimental-design-reproducibility|실험 설계 §4]]), 방법에 대한 주장에는 많은 시행과 함께 여러 코퍼스나 시드가 필요하다.

**사다리 단.** [[05-construction-robotics/site-engineering|2.5 §5]]는 증거 사다리의 단마다 그 단이 재는 예산 항을 묶고, 목업은 팔·공구·부품 항을 재고, 지도와 베이스 항은 실험실이 마련한 표적에 대고서만 잰다. 현장에서는 베이스 항이 커지고, 9의 현장 경우는 시작점을 축마다 $2.66\,\mathrm{mm}$로 둔다. 그 시작점에서 다시 채점하면(§9) BC는 $0.875$에서 $0.656$으로, 네 번째 DAgger 라운드는 $0.995$에서 $0.848$로 떨어진다. 둘 다 목업의 시작점에서 배웠기 때문이다. 기본 제어기 위의 잔차는 $1.000$에 머문다. 주장이 함께 밝혀야 할 것은 집계 규칙 — 조작자가 구해 낸 시도를 세는지, 되돌리기 시간을 재는지([[05-construction-robotics/site-engineering|2.5 §5]]) — 과 힘이다. 브래킷을 $70\,\mathrm{N}$으로 민 안착은 §1의 안착이 아니다.

### 대상으로 한 번 끝까지 · Worked case

S1의 마지막 $40\,\mathrm{mm}$ 위에서 스텝당 오류부터 $4\,\mathrm{mm}$ 리드인 안에 앉을 확률까지 숫자 하나의 흐름을, 복제 정책과 DAgger와 고전 기본 제어기 위의 잔차에 대해 따라간다. §1의 회랑, §3의 최악의 경우, §5의 되돌림, §7의 한계를 쓰므로 여기에 둔다. 고정한 숫자 위의 교과 계산이지 측정이 아니다. 과제의 실행 문항이 같은 모델을 표본 추출하고, §9의 랩이 적합한 정책을 그 옆에 세운다.

**1단계 — 회랑과 남은 여유.** 조작자의 폐루프는 벽을 따라 $c/k_E=0.2/0.5=0.4\,\mathrm{mm}$에, $s=\sqrt{0.0225/0.75}=0.173\,\mathrm{mm}$로 자리 잡으므로(§1) 그 안착은 $0.4+3\times0.173=0.92\,\mathrm{mm}$ 안에 머물고, 이를 올려 가장자리 $b=1\,\mathrm{mm}$로 둔다. 거기서 회랑을 떠나 스텝마다 $c$씩 표류하는 구멍은

$$n_m=\frac{r_c-b}{c}=\frac{4-1}{0.2}=15\ \text{스텝},$$

뒤에 리드인의 테두리에 닿는다. 표류하는 스텝마다 어긋남에 크리프가 하나씩 더해지기 때문이다. 리드인은 표류 열다섯 스텝, 곧 하강의 마지막 $15\,\mathrm{mm}$를 받아 준다.

**2단계 — 단계가 깨끗할 확률.** $40$스텝 각각에서 $\epsilon=0.02$이면, 복제한 안착에 오류가 하나도 없을 확률은 $0.98^{40}=0.446$이다. 안착의 절반 넘게는 오류를 적어도 하나 담는다.

**3단계 — 복제 정책, 최악의 경우.** 첫 오류 뒤로 다시 돌아오지 못한다(§3의 셋째 조건). 스텝 $\tau$의 첫 오류는 표류 $41-\tau$스텝을 남기므로, $41-\tau\le15$, 곧 처음 $25$스텝이 깨끗할 때만 앉는다.

$$P_{\text{BC}}=(1-\epsilon)^{T-n_m}=0.98^{25}=0.603,$$

모델의 스텝들이 독립으로 틀리기 때문이다. 기대 표류 시간은 $E[N_{\text{off}}]=12.84$스텝, 표류 $2.57\,\mathrm{mm}$이고, 정리 2.1의 상한 $T^2\epsilon=32$스텝, 모델에서 $6.4\,\mathrm{mm}$와 견준다.

**4단계 — DAgger.** $\epsilon_N=0.02$로 두고 정리 3.2의 $O(1)$ 항을 무시하고, 모든 오류를 다음 스텝에 되돌린다고 하자($u=1$). 구멍을 $1.44\,\mathrm{mm}$ 안에 두는 오류라면 참이다. 조작자의 한 스텝, $0.5x+0.2\le0.92$가 그것을 회랑으로 되돌리고, 모델의 오류는 구멍을 $1.2\,\mathrm{mm}$에 둔다. 그러면 회랑 밖의 기대 시간은 $uT\epsilon_N=0.8$스텝, 표류 $0.16\,\mathrm{mm}$다. §9의 라운드는 그 $0.3\,\mathrm{mm}$ 시험으로 자기 상태의 $0.069$에서 $0.158$에서 틀리므로, $\epsilon_N=0.02$는 측정이 아니라 이 계산의 가정이다. 놓치려면 마지막 $16$스텝이 모두 오류여야 하고, 그 확률은 $0.02^{16}=6.6\times10^{-28}$이다. 시행이 보여 줄 수 있는 어떤 정밀도에서도 $P_{\text{DAgger}}=1.000$이다.

**5단계 — 기본 제어기 위의 잔차.** 잔차가 무엇을 내놓든 최악은 매 스텝 $+B$이고, 그것은 벽을 따라 $(B+c)/k_0=2.0\,\mathrm{mm}$, 벽 쪽으로 $B/k_0=1.2\,\mathrm{mm}$, 핀에서 $\sqrt{2.0^2+1.2^2}=2.33\,\mathrm{mm}$에 자리 잡는다. 기본 루프의 퍼짐은 $0.242\,\mathrm{mm}$이므로 리드인의 테두리는 표준편차 $(4-2.33)/0.242=6.9$개만큼 떨어져 있다. $P=1.000$이고, 더 나은 잔차는 구멍을 더 가까이 둘 뿐이다.

**6단계 — 안착 때의 힘.** $500\,\mathrm{N/m}$ 임피던스를 거치면 잔차의 최악의 안착은 옆으로 $500\times0.00233=1.2\,\mathrm{N}$을 밀고, 조작자의 $95$번째 백분위 안착 $0.71\,\mathrm{mm}$는 $0.36\,\mathrm{N}$을 민다. 단단한 $10^5\,\mathrm{N/m}$ 루프를 거치면 같은 둘이 $F_{\lim}=20\,\mathrm{N}$에 맞서 $233$과 $71\,\mathrm{N}$이 든다.

**7단계 — 지평.** 단계가 길수록 복합된다. $P_{\text{BC}}=0.98^{T-15}$는 $T=20$에서 $0.904$, $40$에서 $0.603$, $60$에서 $0.403$, $80$에서 $0.269$이고, DAgger는 $1.000$에, 잔차의 최악은 $2.33\,\mathrm{mm}$에 머문다. 정리 2.1은 기대 표류 스텝을 리드인이 받아 주는 $15$ 아래로 $T=27$까지만, 정리 3.2는 4단계의 가정 위에서 $T=750$까지 붙든다.

**여기서 얻는 독법.** 숫자 셋이 이 페이지를 나른다. $0.603$은 $40\,\mathrm{mm}$ 단계에 걸쳐 복합된 $2\%$ 오류이고, $1.000$은 같은 오류를 그것이 일어나는 곳에서 되돌리도록 배운 것이며, $2.33\,\mathrm{mm}$는 한계를 둔 잔차가 할 수 있는 최대다. §9의 적합한 표는 잰 오류가 $0.0225$인데도, 그 비율이 최악의 경우에 주는 $0.566$이 아니라 $0.875$로 앉는다. 랩의 오류가 모두 흡수적인(한 번 나면 돌아오지 못하는) 오류는 아니기 때문이다 — 랩은 모델의 최악의 경우 안에 마침 놓인다.

### 9. 랩: S1 안착 위의 BC, DAgger, 잔차

모든 것이 이 페이지의 대상에 고정되어 있다. 코드(영어 절)는 조작자로부터 시연 $352$개를 만들고(코퍼스는 처음 $88$개), §2의 표를 최소제곱으로 맞추고, 조작자 자신의 상태에서 채점한 뒤, 조작자, BC, DAgger 네 라운드, 기본 제어기만, 잔차로서의 BC, 카메라로 기록한 코퍼스의 BC를 각각 $2{,}000$번의 안착으로 Wilson 구간과 함께 채점한다. 그다음 코퍼스 크기를 훑고, 세 정책을 현장의 시작점에서 다시 채점하고, 다른 코퍼스 다섯 개에서 BC를 다시 맞춘다. 학습한 정책은 모두 같은 시작점 $2{,}000$개와 같은 잡음(시드 $3$)을 만나므로 행 사이의 차이는 정책의 차이다. NumPy와 표준 라이브러리만 쓰고, 1초 안에 돈다.

출력은 먼저 조작자 상태에서 BC의 오류 $0.0225$를 찍고, 이어서 다음을 찍는다.

| 정책 | 안착 | 95% Wilson | 안착의 95%가 드는 반지름 | 자기 상태에서의 오류 | 조작자 시간 |
|---|---:|---|---:|---:|---:|
| 조작자 | $1.000$ | $[0.998,\ 1.000]$ | $0.71\,\mathrm{mm}$ | $0.007$ | — |
| BC, 시연 88개 | $0.875$ | $[0.860,\ 0.889]$ | $7.28\,\mathrm{mm}$ | $0.233$ | $4.0\,\mathrm{h}$ |
| DAgger 1라운드 | $0.950$ | $[0.939,\ 0.958]$ | $4.03\,\mathrm{mm}$ | $0.158$ | $4.7\,\mathrm{h}$ |
| DAgger 2라운드 | $0.980$ | $[0.973,\ 0.985]$ | $1.14\,\mathrm{mm}$ | $0.093$ | $5.3\,\mathrm{h}$ |
| DAgger 3라운드 | $0.981$ | $[0.974,\ 0.986]$ | $1.14\,\mathrm{mm}$ | $0.086$ | $6.0\,\mathrm{h}$ |
| DAgger 4라운드 | $0.995$ | $[0.991,\ 0.997]$ | $0.99\,\mathrm{mm}$ | $0.069$ | $6.7\,\mathrm{h}$ |
| 기본 제어기만 | $1.000$ | $[0.998,\ 1.000]$ | $1.24\,\mathrm{mm}$ | | |
| 잔차로서의 BC | $1.000$ | $[0.998,\ 1.000]$ | $1.08\,\mathrm{mm}$ | | |
| BC, 카메라로 기록한 코퍼스 | $0.953$ | $[0.943,\ 0.961]$ | $3.87\,\mathrm{mm}$ | | |

코퍼스 크기에 대한 훑기, BC만:

| 시연 | 안착 | 95% Wilson | 안착의 95%가 드는 반지름 | 자기 상태에서의 오류 | 조작자 시간 |
|---:|---:|---|---:|---:|---:|
| $22$ | $0.556$ | $[0.535,\ 0.578]$ | $10.26\,\mathrm{mm}$ | $0.522$ | $1.0\,\mathrm{h}$ |
| $44$ | $0.734$ | $[0.714,\ 0.752]$ | $10.01\,\mathrm{mm}$ | $0.369$ | $2.0\,\mathrm{h}$ |
| $88$ | $0.875$ | $[0.860,\ 0.889]$ | $7.28\,\mathrm{mm}$ | $0.233$ | $4.0\,\mathrm{h}$ |
| $176$ | $0.940$ | $[0.929,\ 0.950]$ | $4.91\,\mathrm{mm}$ | $0.158$ | $8.0\,\mathrm{h}$ |
| $352$ | $0.960$ | $[0.950,\ 0.967]$ | $3.19\,\mathrm{mm}$ | $0.142$ | $16.0\,\mathrm{h}$ |

현장의 시작점, 축마다 $2.66\,\mathrm{mm}$에서: BC $0.656$ $[0.635,\ 0.677]$, 네 번째 DAgger 라운드 $0.848$ $[0.832,\ 0.863]$, 잔차로서의 BC $1.000$ $[0.998,\ 1.000]$, $95\%$가 $1.04\,\mathrm{mm}$ 안. 시연 88개짜리 다른 코퍼스 다섯 개에서의 BC: $0.865$, $0.817$, $0.879$, $0.840$, $0.859$.

읽을거리 일곱, 각각 시험하는 주장을 붙였다.

**두 분포는 두 숫자다**(§2와 §3을 시험). 적합한 표는 조작자 자신의 상태에서 $0.0225$, 자기 상태에서 $0.233$의 비율로 조작자라면 내리지 않았을 명령을 낸다. 같은 표에서 열 배다. 바뀐 것은 상태뿐이다.

**최악의 경우는 한계다**(계산 절을 시험). 잰 오류 $0.0225$로 최악의 경우는 $0.9775^{25}=0.566$을 예측하는데, 표는 $0.875$로 앉는다. 랩의 오류가 모두 흡수적인(한 번 나면 돌아오지 못하는) 오류는 아니다. 상당수는 $0.3\,\mathrm{mm}$보다 크게 틀렸어도 구멍을 회랑 안에 두는 명령이고, 크리프를 거스르는 오류는 크리프가 회랑 안으로 되돌려 놓는다. 랩은 모델의 최악의 경우 안에 마침 놓인다. 그것을 보장하는 것은 없다. 랩이 세는 것은 정리 2.1의 0-1 손실이 아니라 $0.3\,\mathrm{mm}$ 넘게 틀린 명령이고, 그보다 작은 어긋남도 상태를 움직이기 때문이다.

**다시 라벨 붙이기가 더 모으기를 이긴다**(§5를 시험). DAgger 한 라운드, $40$분의 시도가 BC를 $0.875$에서 $0.950$으로 올리고, 두 라운드는 조작자 시간 $5.3\,\mathrm{h}$에 $0.980$에 이르러, $16.0\,\mathrm{h}$에 네 배 코퍼스가 낸 $0.960$을 넘는다. 정책 자기 상태에서의 오류는 라운드마다 $0.233$에서 $0.069$로 준다.

**잔차의 영은 기본 제어기의 보정이다**(§7을 시험). 같은 코퍼스, 같은 적합이다. 정책으로서 표는 $0.875$로, 기본 제어기 위의 잔차로서는 $1.000$으로 앉는다. 기본 제어기만으로도 $1.000$이므로, 이 시작점에서 학습한 부분은 정밀도($1.24$ 대신 $1.08\,\mathrm{mm}$)를 사고 한계는 견고함을 산다.

**로그가 담은 것**(§2와 §6을 시험). 조작자가 기록되는 카메라만 보고 만든 코퍼스는 같은 시연 수로 $0.875$ 대신 $0.953$으로 앉는다. BC의 실패 가운데 거의 3분의 2, $12.5\%$에서 $4.7\%$로 줄어든 몫은 조작자가 로그에 남지 않은 화면을 보고 움직인 데서 왔다.

**현장은 다른 시작점 분포다**(§8을 시험). 축마다 $2.66\,\mathrm{mm}$에서 BC는 $0.656$으로, 네 번째 DAgger 라운드는 $0.848$로 떨어진다. 모든 라운드를 목업의 시작점에서 돌렸기 때문이다. 잔차는 $1.000$에 머문다.

**정책은 한 번 뽑은 것이다**(§8을 시험). 시연 88개짜리 다른 코퍼스 다섯 개가 BC를 $0.817$에서 $0.879$ 사이에 둔다. 학습한 정책 하나의 $2{,}000$번 안착이 얻는 구간 반폭의 네 배인 퍼짐이다.

> [!important] 학위논문 문장, 대상 하나로
> 연구 프로그램은 기여를 *인간 중심 건설 환경에서 접촉이 많은 모바일 매니퓰레이션을 위한 학습과 제어*로 적는다([[07-research-program/index|7. §3]]). S1의 마지막 $40\,\mathrm{mm}$ 위에서 그 문장의 각 부분을 이제 대상 하나로 가르쳤다. *학습*: 행동 복제가 무엇을 맞추고 어디서 깨지는가(§2–§3), 평균으로 뭉개진 시연자 둘(§4), DAgger(§5), 그리고 §9의 측정. *제어*: 오차를 힘으로 바꾸는 임피던스 목표(§6)와 학습 잔차가 바로잡는 고전 기본 제어기(§7). *접촉이 많은 매니퓰레이션*: 리드인, 힘 한계, 체결재에 넘기는 하중(§1, §6). *모바일*: 현장의 시작점을 $2.66\,\mathrm{mm}$로 만드는 베이스 항(§8, 9에서). *인간 중심*: 작업자가 있으면 좁힐 수는 있어도 넓힐 수는 없는 한계(§7). *건설 환경*: 크리프, 현장의 시작점, 증거가 선 사다리 단(§1, §8).

### 읽고 나면

- [ ] S1의 안착을 학습 문제로 적는다. 관측, 명령, 동역학, 성공의 세 조건, 시연자.
- [ ] 행동 복제의 세 조건과, 움직임이 i.i.d. 가정을 깨는 두 방식을 말하고, 조작자의 근접 화면이 복제 이득에 무슨 일을 했는지 말한다.
- [ ] 스텝당 오류를 표류 스텝, 밀리미터, 안착 확률로 바꾸고, BC와 DAgger의 지평을 댄다.
- [ ] 단봉 헤드가 두 경로에 무슨 일을 하는지, 청크와 다봉 헤드가 각각 무엇을 바꾸는지 말한다.
- [ ] DAgger 한 라운드를 조작자 시간으로 값 매기고, 알고리즘 자체가 보여 주지 않는 두 비용을 댄다.
- [ ] 1밀리미터가 되는 힘으로 위치 목표와 임피던스 목표 사이를 고르고, 로그가 담아야 할 힘을 말한다.
- [ ] 잔차의 최악의 경우를 묶고, 작업자가 있을 때 한계에 무엇을 해도 되는지 말한다.
- [ ] 성공 주장을 Wilson 구간, 실패율을 배제하는 시행 수, 그 뒤의 코퍼스 수, 사다리 단과 함께 읽는다.

### 스스로 점검

1. 적합한 표의 떼어 둔 시연 위 손실이 낮다. 왜 그것이 안착률을 예측하지 못하는가?
2. §2의 복제 정책은 왜 조작자의 $0.4\,\mathrm{mm}$에 자리 잡으면서도 거의 두 배로 퍼지는가?
3. 동료가 DAgger 대신 시연 88개를 더 모으자고 제안한다. §5의 표는 무엇을 말하고, 왜 그런가?
4. 청크의 오류율이 스텝의 것과 같다면, $10$개짜리 청크는 §3의 최악의 경우를 $0.603$에서 $0.941$로 올린다(§4). S1에서 청크는 무엇을 치르는가?
5. 작업자 상태에 대한 추정은 왜 $B$를 낮출 수는 있어도 올릴 수는 없는가?
6. 위치 목표를 단단한 루프로 내보내는 정책이 목업에서 패널의 $99\%$를 앉힌다. S1의 안착은 풀렸는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 그 손실은 §2 정의의 셋째 조건, 곧 조작자의 상태 위의 평균이기 때문이다. 정책은 자기 상태에서 평가받고, 거기서 적합한 표는 열 배 자주 틀리며($0.0225$ 대신 $0.233$, §9), 회랑 밖에는 자료가 없으므로 그곳의 오류 뒤에는 오류가 더 온다.
> 2. 코퍼스가 좁은 곳에서는 카메라가 명령을 거의 예측하지 못하기 때문이다. 단계 후반에 실제 어긋남은 $0.03\,\mathrm{mm}^2$로 흩어지고 카메라는 $0.25$를 더하므로, 적합은 조작자의 이득을 $0.03/0.28=0.107$배, 스텝당 $0.054$로 줄인다. 약한 이득도 조작자의 명령이 $-0.2$였던 $0.4\,\mathrm{mm}$에서 크리프는 상쇄하지만, 흔들림이 구멍을 $0.173$ 대신 $0.32\,\mathrm{mm}$로 퍼뜨리게 둔다.
> 3. 코퍼스를 두 배로 하면(다시 $4.0\,\mathrm{h}$) $0.940$이고, DAgger 한 라운드($40\,\mathrm{min}$)는 $0.950$, 두 라운드($80\,\mathrm{min}$)는 $0.980$이라고 말한다. 새 시연은 정책이 이미 잘하는 조작자의 분포에서 오고, 다시 라벨 붙인 시도는 정책이 실패하는 자기 분포에서 온다.
> 4. 열린 루프의 시간이다. $10$스텝, $1\,\mathrm{s}$ 동안 청크는 구멍을 보지 못한다. 크리프를 예측해야 하고, 다음에 보기 전까지 흔들림만으로 구멍이 $0.32\,\mathrm{mm}$ 퍼진다. 그리고 결정당 오류율은 스텝의 것이 아니다. 틀린 청크는 틀린 명령 열 개다.
> 5. 한계는 허용 집합의 일부이고, [[05-construction-robotics/hrc-worker-centered|6. HRC §8]]은 그 집합을 잰 상태와 최악의 인간 항으로만 계산하기 때문이다. $B$를 낮추면 잔차의 최악의 경우가 기본 제어기에 더 가까워지고, 추정이 무엇을 틀렸든 안전하다. $B$를 올리면 추정이, 그것이 잘못 예측한 바로 그 작업자를 지키는 한계를 옮기게 된다.
> 6. 아니다. §1의 둘째 조건이 깨진다. 조작자조차 $5\%$는 내는 $0.71\,\mathrm{mm}$ 어긋난 안착은 $10^5\,\mathrm{N/m}$를 거쳐 옆으로 $71\,\mathrm{N}$을 밀고, $0.2\,\mathrm{mm}$ 안의 안착만 $20\,\mathrm{N}$ 아래에 머문다. $99\%$가 무엇을 뜻하려면 그 주장은 힘, 집계 규칙, 사다리 단을 밝혀야 하고, 지지 끝의 하중 넘기기에는 기록된 힘이 필요하다(§6).

### 과제 · Problem set

Tier A. S1의 마지막 밀리미터들이고, 그 뒤에 [[04-robotics/teleoperation-demonstration|12]], [[04-robotics/force-compliance-control|13]], [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]]이 있다. 랩은 표본 추출한 시연에 최소제곱으로 표를 맞추고, 물리 시뮬레이터는 없다.

1. **그리기.** 조작자 상태에서 두 배 나은 정책, $\epsilon=0.01$이 패널을 마지막 $60\,\mathrm{mm}$에 걸쳐 내리는 경우($T=60$)의 그림: 회랑, 첫 오류가 $40\,\mathrm{mm}$에서 난 복제 정책과 $10\,\mathrm{mm}$에서 난 복제 정책, 핀에서의 두 어긋남, 마지막 $15\,\mathrm{mm}$가 시작되는 선, 안착 확률, 그리고 매 스텝 한계만큼 밀리는 스텝당 $B=0.4\,\mathrm{mm}$의 기본 제어기 위 잔차.
2. **유도.** (a) $\epsilon=0.01$, $T=60$에서: 복제 정책이 앉을 확률, 기대 표류 스텝, 정리 2.1의 상한, 그리고 BC와 DAgger($u=1$)의 상한이 리드인이 받아 주는 $15$스텝에 이르는 단계 길이. (b) 현장에서 크리프가 스텝마다 $c=0.3\,\mathrm{mm}$로 커진다: 조작자의 어긋남과 회랑 가장자리(§3이 $0.92$를 $1$로 올렸듯 다음 0.1밀리미터로 올림), 리드인이 받아 주는 표류 스텝(정수 스텝), $\epsilon=0.02$, $T=40$에서 BC의 최악의 안착, $B=0.3$에서 잔차의 최악의 경우. (c) $c=0.3$에서 잔차의 최악의 경우를 리드인 안쪽으로 기본 루프 표준편차 네 개만큼 두는 가장 큰 $B$. (d) $40$번 가운데 $38$번 안착의 Wilson 구간.
3. **실행.** 영어 절 템플릿의 `?`를 채워, 스크립트가 계산 절의 모델 — 첫 오류부터 표류하는 복제 정책, 모든 오류를 되돌리는 DAgger, $+B$로 밀리는 잔차 — 을 표본 추출해 3–5단계를 다시 내게 하고, 이어서 $\epsilon=0.02$와 $\epsilon=0.01$에서 단계를 $T=20,\ 40,\ 60,\ 80$으로 훑게 하라. 훑기를 읽어라. 각 $\epsilon$에서 복제 정책이 이 길이들 가운데 처음으로 $90\%$ 아래로 앉는 것은 어디인가, 그리고 DAgger 열은 무엇을 하는가?
4. **해석.** 어떤 논문이 보고한다. "우리의 BC 정책은 목업에서 20번 시행에 95% 성공으로 패널을 끼운다." (a) Wilson 구간과 그것이 배제하지 못하는 실패율을 대라. (b) $0.875$로 앉는 §9의 BC는 얼마나 자주 $20$번 가운데 $19$번 이상을 보이겠는가? (c) $5\%$ 실패율을 배제하려면 몇 번 연속 성공해야 하는가? (d) 주장을 사다리에 놓고, 현장이 무엇을 바꿀지 §9의 숫자로 말하라. (e) 논문의 95%를 무엇과 견주기 전에 밝혀야 할 것 셋을 더 대라.

> [!note]- 그리는 법 · How to draw it
> - **축**: 핀 끝 위의 높이 $60$에서 $0\,\mathrm{mm}$까지, 1밀리미터마다 스텝 하나, 그리고 벽을 따라 잰 어긋남 $-4.5$에서 $10\,\mathrm{mm}$까지. $0$에 핀의 축, 핀에 $-4$에서 $4\,\mathrm{mm}$까지의 막대로 리드인.
> - **회랑**: 조작자 평균 $0.4\,(1-0.5^t)$에 표준편차 세 개를 더하고 뺀 띠. 위에서 $\pm4.05\,\mathrm{mm}$이고 다섯 스텝 안에 $[-0.12,\ 0.92]\,\mathrm{mm}$로 좁아진다 — 그림과 같은 띠가 $20$스텝 더 이어진다.
> - **복제 정책 둘**: $40\,\mathrm{mm}$(스텝 $20$)의 오류는 표류 $41$스텝을 남겨 핀에 $1+0.2\times41=9.2\,\mathrm{mm}$로 닿고, $10\,\mathrm{mm}$(스텝 $50$)의 오류는 $11$스텝을 남겨 리드인 안인 $3.2\,\mathrm{mm}$로 닿는다. $15\,\mathrm{mm}$에 선을 긋고 안착 확률 $0.99^{45}=0.636$을 적는다.
> - **잔차**: $B=0.4$이면 최악의 경우는 벽을 따라 $(0.4+0.2)/0.25=2.4\,\mathrm{mm}$, 벽 쪽으로 $0.4/0.25=1.6\,\mathrm{mm}$, 핀에서 $2.88\,\mathrm{mm}$에 자리 잡는다. 벽 방향 경로를 $2.4$까지 올라가게 그린다.
> - 복제 정책의 기울기가 오류가 얼마나 늦게 났는지에 따라 달라지면 그림이 틀린 것이다. 모든 오류는 스텝마다 같은 $0.2\,\mathrm{mm}$로 표류하고, 다른 것은 남은 스텝 수뿐이다.

> [!tip]- 정답 · Solutions
> 1. 그리는 법 목록과 같다. $40$과 $10\,\mathrm{mm}$의 오류는 $9.2$와 $3.2\,\mathrm{mm}$에서 끝나고, 안착 확률은 $0.636$, 잔차의 최악은 벽을 따라 $2.4\,\mathrm{mm}$, 핀에서 $2.88\,\mathrm{mm}$다.
> 2. (a) $0.99^{60-15}=0.99^{45}=0.636$. $E[N_{\text{off}}]=15.17$스텝, $3.03\,\mathrm{mm}$. 상한 $T^2\epsilon=36$스텝. BC의 상한은 $T=\sqrt{15/0.01}=38.7$스텝에서, DAgger의 상한은 $T=15/0.01=1500$에서 $15$에 이른다. (b) 조작자는 같은 $s=0.173\,\mathrm{mm}$로 $0.3/0.5=0.6\,\mathrm{mm}$에 자리 잡으므로 가장자리는 $0.6+0.52=1.12\,\mathrm{mm}$, 올려서 $1.2$다. 리드인은 $(4-1.2)/0.3=9.3$, 곧 정수 $9$스텝을 받아 준다. BC는 $0.98^{40-9}=0.98^{31}=0.535$로 앉는다. 잔차의 최악은 벽을 따라 $(0.3+0.3)/0.25=2.4\,\mathrm{mm}$, 벽 쪽으로 $1.2\,\mathrm{mm}$, 핀에서 $2.68\,\mathrm{mm}$다. (c) $\sqrt{((B+0.3)/0.25)^2+(B/0.25)^2}\le4-4\times0.242=3.03\,\mathrm{mm}$에서 스텝마다 $B\le0.36\,\mathrm{mm}$다. 더 센 크리프가 §7이 허락한 $0.43$ 가운데 약 $0.06$을 먹는다. (d) $z^2/n=0.096$. 중심 $(0.95+0.048)/1.096=0.911$, 반폭 $1.96\sqrt{0.95\times0.05/40+3.8416/6400}/1.096=0.076$이므로 $[0.835,\ 0.986]$.
> 3. 빈칸은 영어 절 정답과 같다. `err.argmax(axis=1) + 1`, `T + 1 - first`, `BND + C`. 스크립트는 $\epsilon=0.02$, $T=20,\ 40,\ 60,\ 80$에서 복제 정책의 안착 $0.904$, $0.604$, $0.403$, $0.268$을 공식의 $0.904$, $0.603$, $0.403$, $0.269$와 함께, 표류 $3.70$, $12.82$, $25.58$, $40.85$스텝을 정확값 $3.71$, $12.84$, $25.58$, $40.73$과 함께 찍는다. $\epsilon=0.01$에서는 $0.950$, $0.777$, $0.638$, $0.520$을 $0.951$, $0.778$, $0.636$, $0.520$과 함께, 표류 $1.97$, $7.26$, $15.08$, $25.40$스텝을 찍는다. DAgger는 모든 행에서 $1.000$으로 앉고, 잔차의 최악은 $2.33\,\mathrm{mm}$다. 네 길이 가운데 복제 정책이 처음 $90\%$ 아래로 앉는 것은 두 비율 모두 $T=40$이다 — 공식으로는 $\epsilon=0.02$에서 $T=21$부터, $\epsilon=0.01$에서 $T=26$부터다. 그래서 오류를 절반으로 줄여도 BC가 열에 아홉 번 앉는 단계는 5밀리미터만 길어진다. 마지막 $15\,\mathrm{mm}$ 위의 부분이 약 $5$에서 약 $10\,\mathrm{mm}$로 두 배가 될 뿐이고, 리드인의 $15\,\mathrm{mm}$는 그대로이기 때문이다. DAgger 열은 $1.000$을 떠나지 않는다. §3의 셋째 조건이 없으면 어떤 오류도 핀까지 실려 가지 않는다.
> 4. (a) $19/20$은 Wilson 구간 $[0.764,\ 0.991]$을 주므로 $23.6\%$까지의 어떤 실패율도 보고와 양립한다. (b) $p=0.875$에서 $P(X\ge19)=20\times0.875^{19}\times0.125+0.875^{20}=0.267$이다. 여덟 번에 한 번 실패하는 정책으로도 그런 실험 넷 가운데 하나쯤은 논문의 문장을 찍는다. (c) $n\ge\ln0.05/\ln0.95=58.4$이므로 $59$번 연속 성공. (d) 잘해야 실물 크기 목업이고, "실제 기하와 규모를 견딘다"를 허락하며 팔·공구·부품 항만 잰다([[05-construction-robotics/site-engineering|2.5 §5]]). 현장에서는 시작점이 $2.66\,\mathrm{mm}$로 넓어지고, §9의 BC는 $0.875$에서 $0.656$으로 떨어지는 반면 고전 기본 제어기 위의 잔차는 $1.000$을 지킨다. (e) 다음 가운데 셋. 코퍼스나 시드를 몇 개 학습했고 얼마나 퍼졌는가, 개입과 되돌리기의 집계 규칙, 시작점 분포와 접근 중의 크리프, "성공"에 힘 한계가 들어 있는가와 목표를 어떤 강성으로 추종했는가, 코퍼스의 크기·수율·경로.

### 출처

- S. Ross, G. J. Gordon, J. A. Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning," *AISTATS 2011*, PMLR vol. 15, pp. 627–635; [arXiv:1011.0686](https://arxiv.org/abs/1011.0686), [ar5iv](https://ar5iv.labs.arxiv.org/html/1011.0686)에서 읽음 — 초록의 i.i.d. 문장(§2), Ross와 Bagnell(2010)의 것으로 밝힌 정리 2.1과 그 $[0,1]$ 비용·0-1 손실·빡빡함, $\epsilon_N$의 정의를 담은 정리 3.2(§3), $\beta_1=1$, $\beta_i=p^{i-1}$, $\beta_i=\mathbb 1[i=1]$을 담은 알고리즘 3.1(§5). [[01-canonical-papers/notes/4-vla/dagger|DAgger 노트]]도 보라.
- M. Kelly, C. Sidrane, K. Driggs-Campbell, M. J. Kochenderfer, "HG-DAgger: Interactive Imitation Learning with Human Experts," *ICRA 2019*, pp. 8077–8083, DOI 10.1109/ICRA.2019.8793698; [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — 조종 없이 붙인 라벨은 안전을 떨어뜨릴 수 있고 질이 떨어질 가능성이 크다는 것(초록), 그리고 안전하지 않은 영역에서 전문가가 조종을 넘겨받고 그때만 라벨을 모으는 방식(§5).
- T. Z. Zhao, V. Kumar, S. Levine, C. Finn, "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware," *RSS 2023*, [arXiv:2304.13705](https://arxiv.org/abs/2304.13705) — ACT의 청크, 시연자들의 변동을 위해 학습하되 시험 때는 잠재변수를 사전분포의 평균인 영에 두고 결정론적으로 디코딩하는 CVAE, 그리고 겹치는 청크의 지수 가중 평균인 시간 앙상블. 논문이 밝힌 대로다(§4). [[01-canonical-papers/notes/4-vla/act|ACT 노트]]도 보라.
- C. Chi et al., "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion," *RSS 2023*, [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) — 초록이 밝힌 다봉 행동 분포의 매끄러운 처리(§4). [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy 노트]]도 보라.
- C. Chen, Z. Yu, H. Choi, M. Cutkosky, J. Bohg, "DexForce: Extracting Force-informed Actions from Kinesthetic Demonstrations for Dexterous Manipulation," [arXiv:2501.10356](https://arxiv.org/abs/2501.10356), 2025 — 힘을 반영한 목표 $x_f=x_o+k_f f$, 그리고 관측한 위치로 학습한 정책의 거의 영에 가까운 성공에 맞선 여섯 작업 평균 $76\%$(§6).
- T. Silver, K. Allen, J. Tenenbaum, L. Kaelbling, "Residual Policy Learning," [arXiv:1812.06298](https://arxiv.org/abs/1812.06298), 2018 — 초기 제어기 위에서 학습한 잔차(§7).
- T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, S. Levine, "Residual Reinforcement Learning for Robot Control," *ICRA 2019*, pp. 6023–6029, DOI 10.1109/ICRA.2019.8794127; [arXiv:1812.03201](https://arxiv.org/abs/1812.03201) — 기존 제어기의 신호와 RL 잔차의 중첩으로서의 최종 정책(§7).
- E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association* 22(158):209–212, 1927 — [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]에서 계산한 점수 구간(§8, §9).
- 이 위키 안에서: [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]](핀 앞의 S1), [[04-robotics/teleoperation-demonstration|12. 원격조작]](코퍼스 기록과 그 지표), [[04-robotics/capstone-panel-contact|26. 캡스톤]](고전 루프), [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real]](잔차), [[05-construction-robotics/hrc-worker-centered|6. HRC]](작업자의 한계).
- 이 페이지의 교과 숫자는 모두 S1의 고정값과 이 페이지의 고정값에서 NumPy 2.0.2로 여기서 계산했다. 시연, 롤아웃, 현장은 표본으로 뽑은 것이지 잰 것이 아니다.
