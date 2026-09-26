---
title: 4. Vision–Language–Action
tags: [deep-learning, vla, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Specify a VLA by observation, instruction, action representation, horizon, objective, control interface, and closed-loop evidence, and sweep the chunk length on D4."
mastery-when: "Raise when policy architecture, action representation, data mixture, or adaptation is the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> Object **D4**, a frozen three-step action chunk on a 2-D task plane, from [[03-deep-learning/lab-objects|0. Lab Objects]] · [[02-foundations/lab-kernel|0.7 Lab Kernel]], because this page is Tier A · [[03-deep-learning/vlm/index|3. VLM]], [[02-foundations/rl-robot-learning|7.5 RL §1 and §4]], [[02-foundations/ml-practice|9. ML Practice]] (the Wilson interval of its worked case), [[04-robotics/robot-systems-deployment|10. Robot Systems]], and [[04-robotics/teleoperation-demonstration|12. Teleoperation]].
> [[03-deep-learning/lab-objects|0. Lab Objects]]의 대상 **D4**(2차원 작업 평면 위에 고정한 세 스텝짜리 행동 청크) · 이 페이지는 Tier A이므로 [[02-foundations/lab-kernel|0.7 Lab Kernel]] · [[03-deep-learning/vlm/index|3. VLM]], [[02-foundations/rl-robot-learning|7.5 RL §1과 §4]], [[02-foundations/ml-practice|9. ML 실무]](계산 예제의 Wilson 구간), [[04-robotics/robot-systems-deployment|10. Robot Systems]], [[04-robotics/teleoperation-demonstration|12. Teleoperation]].

## English

*Stands on the VLM encoder of [[03-deep-learning/vlm/index|3. VLM]] and the rate budget of [[04-robotics/robot-systems-deployment|10. Robot Systems]]. First use of object **D4**.*

> [!note] Why this matters · 왜 배우는가
> This page is the top of the learning-and-adaptation layer of the physical-AI stack in [[07-research-program/index|7. Research Program §5]] — the policy that turns an instruction and an image into motion — and in *"install that panel on the frame"* it serves step 3, *decompose the job*, and step 7, *perform the fitting*, whenever a learned policy does them (its chip sits in the learning-and-adaptation band of the [[physical-ai-map|Physical AI Map]]). Without it a learned policy's claims cannot be checked: D4, the track's frozen action chunk ([[03-deep-learning/lab-objects|0. Lab Objects]]), acts on a scene up to $0.20\,\mathrm{s}$ old at $k=3$ and reacts to a change $0.20\,\mathrm{s}$ late, $1.00\,\mathrm{s}$ at $k=20$ (the Worked case); squared error sends two demonstrations that pass either side of an obstacle to $(0,0)$, straight into it (§2); the same normalized chunk moves a second arm $6$ and $3\,\mathrm{cm}$ too far (§7); and $80\%$ against $60\%$ over ten trials ranks nothing (§4). On the dissertation path ([[07-research-program/index|7. Research Program §8]]) it closes block 4, deep-learning sessions 39–44, read with [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning]] §1 on behaviour cloning and compounding error and §4 on fine-tuning kept near the cloned policy by a KL term, and [[05-construction-robotics/imitating-contact|10. Imitating Contact]] §2, §4 and §6 carry its behaviour cloning, its two-demonstrator mean and its choice of action onto the seating of S1, the construction track's 20 kg facade-panel task ([[05-construction-robotics/site-engineering|2.5]]). After it you can specify any VLA in one row — observation, action space, frame, rate, horizon $H$, executed stride $k$, head, evidence — and compute its staleness, reaction latency and head cost before believing its video.

> [!note] First pass · 처음이라면
> About six sessions of 60–90 minutes, rows 39–44 of the [[03-deep-learning/index|deep-learning schedule]]; the first two are the first pass. **Session 1:** the Running object, the picture and the Worked case by hand with the solution covered — $m=2$, a worst age of $0.20\,\mathrm{s}$ at $k=3$, and $\ell=0.20\,\mathrm{s}$ against $1.00\,\mathrm{s}$ at $k=20$. **Session 2:** §1–§3, with [[02-foundations/rl-robot-learning|7.5 §1]] open beside §2; then self-checks 1, 2, 4 and 5 and problems 1–2. **Session 3:** §4 and the §5 lab, self-check 3 and problem 3. **Sessions 4–6:** §6, §7 and §8, one a session, with self-checks 7, 6 and 8; their collapsed *Deeper* notes are second-pass reading. Finish by filling the After-reading row for one real VLA paper, [[01-canonical-papers/notes/4-vla/pi0|π0]] or [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]], and saying which of its numbers you could not find.

### Running object · 이 페이지의 대상

**D4** from [[03-deep-learning/lab-objects|0. Lab Objects]], at the numbers that page freezes. At time $t$, **D4** receives an observation $o_t$ — image features on a real robot, reduced on D4 to the four-number token of the table below — and the instruction $l=$ "move left, then down," and predicts a chunk $a_{t:t+2}$ of three 2-D end-effector deltas. The robot executes only the first $k$ actions before observing again. Write the interface before the architecture:

$$\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l),\qquad a_i=(\Delta x_i,\Delta y_i).$$

| Symbol | Value | What it is |
|---|---:|---|
| $o$ | $(p_x,p_y,g_x,g_y)$ | the observation token: tool position and the target the instruction names, in metres |
| $p_0$ | $(0,0)\,\mathrm{m}$ | tool position at the catalog pose |
| $g$ | $(-0.04,-0.02)\,\mathrm{m}$ | target before the scene changes |
| $a_{1:3}$ | $(-0.02,0)$, $(-0.02,0)$, $(0,-0.02)$ | the frozen chunk, in metres |
| $a_{\max}$ | $0.02\,\mathrm{m}$ | largest delta the interface accepts in one control step |
| $\delta$ | $0.005\,\mathrm{m}$ | the policy's axis-switch band: close $x$ to within $\delta$, then $y$ |
| $\Delta t$ | $0.05\,\mathrm{s}$ | controller period, 20 Hz |
| $t_{\mathrm{inf}}$ | $0.10\,\mathrm{s}$ | one policy forward pass |
| $\sigma$ | $0.002\,\mathrm{m}$ | per-axis perception jitter on the observation token |

The instruction is not decoration here: "left, then down" *is* the axis order the policy plans in, which is why the frozen chunk moves in $x$ twice and then in $y$ once. The $100\,\mathrm{ms}$ of $t_{\mathrm{inf}}$ belongs to the model *and* the computer it runs on: where that time goes on the robot's own GPU — bytes per weight, kernel launches, number formats — is [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing §8]] and [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §11]], both off the dissertation path until a policy runs on board.

*Scope: this page teaches the interface between a language-conditioned policy and a robot — action representation, the behaviour-cloning objective, how long a chunk may be committed, which head produces it and at what cost, what a reported success rate does and does not prove, what changes when one policy drives many bodies, and what it means to learn a task from the prompt. It does not teach the vision–language encoder that produces $o_t$, which is [[03-deep-learning/vlm/index|3. VLM]]; nor how a pretrained backbone is fine-tuned to a new robot, in full or with LoRA, which is [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §8]]; nor the generative head that turns multimodal demonstrations into an action distribution, which is [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]; nor the controller that turns a delta into a torque, which is [[04-robotics/force-compliance-control|13. Force & Compliance Control]]; nor where demonstrations come from, which is [[04-robotics/teleoperation-demonstration|12. Teleoperation]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 402" style="max-width:100%;height:auto" role="img" aria-label="D4's closed loop with the policy edge labelled t_inf = 100 ms, the controller edge 50 ms, a chunk buffer of three actions and an observation from step n minus 2; below, the loop unrolled over control steps showing each chunk's observation step, the age of every executed action, and a 0.20 s reaction to a scene change at step 20">
  <defs><marker id="aD4e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) one loop, two clocks</text>
  <rect x="12" y="44" width="106" height="42" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="65" y="61.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">scene</text>
  <text x="65" y="76.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">l: left, then down</text>
  <rect x="240" y="47" width="84" height="36" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="282" y="69" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">policy π<tspan dy="3" font-size="10">θ</tspan></text>
  <line x1="118" y1="65" x2="238" y2="65" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4e)"/>
  <text x="179" y="45" font-size="11" fill="currentColor" text-anchor="middle">o from step n − m</text>
  <text x="179" y="59" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">m = 2 steps</text>
  <line x1="324" y1="65" x2="423" y2="65" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4e)"/>
  <text x="376" y="59" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">t<tspan dy="3" font-size="10">inf</tspan><tspan dy="-3" dx="3.5">= 100 ms</tspan></text>
  <text x="488" y="37" font-size="11" fill="currentColor" text-anchor="middle">chunk buffer · k = 3</text>
  <rect x="428" y="46" width="120" height="17" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="434" y="59" font-size="11" fill="currentColor">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="542" y="59" font-size="11" fill="currentColor" text-anchor="end">(−0.02, 0)</text>
  <rect x="428" y="63" width="120" height="17" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="434" y="76" font-size="11" fill="currentColor">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="542" y="76" font-size="11" fill="currentColor" text-anchor="end">(−0.02, 0)</text>
  <rect x="428" y="80" width="120" height="17" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="434" y="93" font-size="11" fill="currentColor">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="542" y="93" font-size="11" fill="currentColor" text-anchor="end">(0, −0.02)</text>
  <rect x="425" y="43" width="126" height="57" rx="3" stroke="currentColor" stroke-width="2" fill="none"/>
  <rect x="428" y="146" width="120" height="40" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="488" y="162.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">controller</text>
  <text x="488" y="177.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">20 Hz</text>
  <line x1="488" y1="100" x2="488" y2="144" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4e)"/>
  <rect x="240" y="146" width="84" height="40" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="282" y="162.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">robot</text>
  <text x="282" y="177.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">p ← p + a</text>
  <line x1="428" y1="166" x2="326" y2="166" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4e)"/>
  <text x="376" y="160" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">Δt = 50 ms</text>
  <path d="M240 166 L64 166 L64 88" stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aD4e)" stroke-linejoin="round"/>
  <text x="74" y="160" font-size="11" fill="currentColor" fill-opacity="0.8">the world changes</text>
  <path d="M425 86.5 L396 86.5 L396 116 L178 116 L178 68" stroke="currentColor" stroke-width="1.3" fill="none" stroke-dasharray="5 3" marker-end="url(#aD4e)" stroke-linejoin="round"/>
  <text x="287" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.9">refill only when empty: every k = 3 steps</text>
  <text x="12" y="220" font-size="12" fill="currentColor">(b) the loop unrolled for k = 3</text>
  <text x="100" y="266" font-size="11" fill="currentColor" text-anchor="end">observes</text>
  <text x="100" y="292" font-size="11" fill="currentColor" text-anchor="end">executes</text>
  <text x="100" y="318" font-size="11" fill="currentColor" text-anchor="end">age (steps)</text>
  <text x="100" y="340" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">control step n</text>
  <rect x="108" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="126" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="126" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="126" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">16</text>
  <rect x="144" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="162" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="162" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="162" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">17</text>
  <rect x="180" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="198" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="198" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="198" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">18</text>
  <rect x="216" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="234" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="234" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="234" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">19</text>
  <rect x="252" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="270" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="270" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="270" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">20</text>
  <rect x="288" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="306" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="306" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="306" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">21</text>
  <rect x="324" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="342" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="342" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="342" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">22</text>
  <rect x="360" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="378" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="378" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="378" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">23</text>
  <rect x="396" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="414" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="414" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="414" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">24</text>
  <rect x="432" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="450" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="450" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="450" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">25</text>
  <rect x="468" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="486" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="486" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="486" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">26</text>
  <rect x="504" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="522" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="522" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="522" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">27</text>
  <line x1="180" y1="275" x2="180" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <line x1="288" y1="275" x2="288" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <line x1="396" y1="275" x2="396" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <line x1="504" y1="275" x2="504" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="108" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 108.0 274 Q 144.0 248 179.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4e)"/>
  <circle cx="216" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 216.0 274 Q 252.0 248 287.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4e)"/>
  <circle cx="324" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 324.0 274 Q 360.0 248 395.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4e)"/>
  <circle cx="432" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 432.0 274 Q 468.0 248 503.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4e)"/>
  <line x1="252" y1="238" x2="252" y2="328" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 3"/>
  <text x="247" y="246" font-size="11" fill="currentColor" text-anchor="end">scene changes, n<tspan dy="3" font-size="10">j</tspan><tspan dy="-3" dx="3.5">= 20</tspan></text>
  <path d="M252 351 L252 356 L396 356 L396 351" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/>
  <text x="324" y="372" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">ℓ(3) = (24 − 20) × 0.05 s = 0.20 s</text>
  <text x="12" y="388" font-size="11" fill="currentColor" fill-opacity="0.85">worst age (m + k − 1)Δt = 0.20 s · each arc is t<tspan dy="3" font-size="10">inf</tspan><tspan dy="-3" dx="3.5">= m = 2 steps</tspan></text>
</svg>

D4's closed loop on the catalog numbers, with two clocks: the policy edge takes $t_{\mathrm{inf}}=100\,\mathrm{ms}$, that is $m=2$ control steps, the controller edge $\Delta t=50\,\mathrm{ms}$, and the chunk buffer holds $k=3$ actions — $(-0.02,0)$, $(-0.02,0)$, $(0,-0.02)$ — refilled only when empty, from the observation of step $n-m$. Unrolled below for $k=3$, every executed action is 2 to 4 steps old, so the worst age is $(m+k-1)\Delta t=0.20\,\mathrm{s}$, and a scene change at step 20 first reaches an action at step 24, $\ell(3)=(24-20)\times0.05\,\mathrm{s}=0.20\,\mathrm{s}$ later.

### Worked case · 대상으로 한 번 끝까지

This is the homework object. The problem set will ask you to draw it, derive its latency, and sweep one knob. Do all three here first on the catalog numbers, so the set is a change of knobs rather than a first derivation.

**The chunk itself.** The policy walks an imagined tool from the observed position to the observed target, one axis at a time, never more than $a_{\max}$ per step. From $p_0=(0,0)$ toward $g=(-0.04,-0.02)$:

$$r_1=g-p_0=(-0.04,-0.02),\ |r_{1x}|=0.04>\delta\Rightarrow a_1=(-0.02,0),$$

then $r_2=(-0.02,-0.02)$, still $|r_{2x}|=0.02>\delta$, so $a_2=(-0.02,0)$; then $r_3=(0,-0.02)$ has $|r_{3x}|=0<\delta$, so the policy switches axis and $a_3=(0,-0.02)$. That is the catalog chunk. Its path length is $3\times0.02=0.06\,\mathrm{m}$ while its net displacement is only $\sqrt{0.04^2+0.02^2}=0.0447\,\mathrm{m}$, so the instruction's axis order costs $34\%$ more travel than a straight line — a representation choice with a metre cost, which is §1 in one number.

**The timing, which is where the chunk length comes from.** Inference costs $t_{\mathrm{inf}}$, the controller consumes one action every $\Delta t$, so a chunk of $k$ actions lasts $k\Delta t$ and the next chunk can only be ready in time if

$$k\,\Delta t\ \ge\ t_{\mathrm{inf}}\quad\Longrightarrow\quad k\ \ge\ \left\lceil \frac{t_{\mathrm{inf}}}{\Delta t}\right\rceil=\left\lceil\frac{0.10}{0.05}\right\rceil=2=m,$$

because a controller that runs out of actions has to hold or stop. So $m=2$ is both the inference delay measured in control steps and the smallest schedulable chunk. **Age of an executed action.** The chunk covering steps $[jk,(j+1)k)$ was computed from the scene at step $jk-m$, so the action leaving the buffer at step $n$ is $m+(n\bmod k)$ steps old, and the worst case is

$$\text{age}_{\max}(k)=(m+k-1)\,\Delta t,$$

which for the catalog $k=3$ is $(2+3-1)\times0.05=0.20\,\mathrm{s}$.

**Reaction latency.** If the scene changes at control step $n_j$, the first action that can know about it belongs to the first chunk whose observation step is at or after $n_j$, that is the first boundary $jk\ge n_j+m$:

$$\ell(k)=\Big(k\Big\lceil\tfrac{n_j+m}{k}\Big\rceil-n_j\Big)\Delta t.$$

With $n_j=20$ and $k=3$: $\lceil 22/3\rceil=8$, so the boundary is step $24$ and $\ell=4\times0.05=0.20\,\mathrm{s}$. With $k=20$: $\lceil22/20\rceil=2$, boundary step $40$, $\ell=1.00\,\mathrm{s}$. §5 runs the loop and gets these same numbers from the trace, which is the check that the algebra and the code agree.

**And the objective on the same object.** Two equally good demonstrations at one D4 state are $a=(-1,0)$ and $a=(1,0)$ in normalized units. The MSE-optimal deterministic prediction is their mean $(0,0)$ — neither demonstrated mode. With three demonstrations $(-1,0)$, $(-1,0)$, $(1,0)$ it is $(-1/3,0)$: closer to the more frequent mode, still not a demonstrated action. That is §2, and it is why the output distribution is a design choice and not a detail.

### 1. Action representation is part of the method

Joint position, joint velocity, torque, end-effector pose, delta pose, gripper state, and discrete action tokens have different feasibility and control assumptions. "The model outputs actions" is incomplete without units, frame, rate, horizon, and the downstream controller.

Each representation hands a different job to the layer below it. A joint position is tracked by a position servo, so the policy never touches torque but must respect joint limits. A joint velocity is integrated by that servo, so a small bias drifts into a position error. A torque bypasses the servo and makes the policy answer for the arm's dynamics at the controller's own rate. An end-effector pose leaves inverse kinematics, with its several solutions and its singularities, to a solver downstream. A delta pose is a change, so it means nothing without the frame it is written in and the period it spans. A gripper state is usually one number on a schedule of its own. And a token is a bin index, so its resolution is the bin width, which §6 prices on D4.

If D4 predicts $(0.02,0)$ three times in metres but the low-level interface interprets centimetres, the intended 6 cm motion becomes 0.06 cm. The frame and the rate break the same way. D4's deltas are written in the base frame; send them to an interface that reads deltas in the tool frame, with the tool turned $90^\circ$ in the task plane, and each delta is rotated on its way, so the arm executes $(0,-0.02)$, $(0,-0.02)$, $(0.02,0)$ and stops at $(0.02,-0.04)\,\mathrm{m}$ — $0.0632\,\mathrm{m}$ from the target, farther than the $0.0447\,\mathrm{m}$ it started from. How one motion takes two descriptions in two frames is [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §4]]. And each delta means $0.02\,\mathrm{m}$ per $\Delta t=0.05\,\mathrm{s}$, a tool speed of $0.4\,\mathrm{m/s}$; replay the same chunk on a $50\,\mathrm{Hz}$ interface and the tool follows the right path at $1.0\,\mathrm{m/s}$, two and a half times faster, in $0.06$ instead of $0.15\,\mathrm{s}$. The observation carries a time too: every age on this page assumes its timestamp is right, and a stamp $10\,\mathrm{ms}$ wrong puts the tool's observed position $4\,\mathrm{mm}$ off while it moves at D4's $0.4\,\mathrm{m/s}$, most of the $5\,\mathrm{mm}$ switch band $\delta$ ([[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §9]]; between two computers, [[02-foundations/tools/computer-networks|12.5 §10]]). Representation errors are physical errors. Pool data from several robots and the same kind of error becomes systematic, which §7 measures.

Four canonical policies made four different choices, which is why their success rates cannot be set side by side until these rows are aligned. [[01-canonical-papers/notes/4-vla/rt-1|RT-1]] emits $11$ tokens of $256$ bins — seven for the arm, three for the base, one mode switch — at $3\,\mathrm{Hz}$. [[01-canonical-papers/notes/4-vla/act|ACT]] outputs the next $100$ joint-space actions of a $50\,\mathrm{Hz}$ leader–follower rig. [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] outputs positions for a position controller. And [[01-canonical-papers/notes/4-vla/pi0|π0]] outputs continuous joint commands at $50\,\mathrm{Hz}$, zero-padded to $18$ dimensions (§7).

### 2. Behavior cloning and multimodality

A demonstration file gives, for each observation, the action a person took, and the simplest policy is fitted to those actions by regression. The trouble is what regression returns when two people did different, equally good things: squared error returns their average, and the average of two good paths can be a bad one.

For continuous demonstrations, a simple objective is

$$L_{\mathrm{BC}}=\frac1H\sum_{h=0}^{H-1}\|a_{t+h}-\hat a_{t+h}\|_2^2.$$

If equally valid demonstrations pass left and right of an obstacle, their MSE mean may go through it. On D4, two demonstrations at one state are $a=(-1,0)$ and $a=(1,0)$. The MSE-optimal deterministic action is their mean $(0,0)$: neither demonstrated mode, and a collision if the obstacle sits at the origin of the local action frame. Discrete tokens, mixture models, diffusion, and flow policies are alternative output distributions; they do not remove the need for good demonstrations and closed-loop recovery. The figure draws the averaging on D4 and, ahead of §6, what each kind of action head returns instead: a token head, which classifies each action number into one of a fixed set of bins; a denoiser, which refines random noise into a whole chunk; and ACT's CVAE, a regression that also takes a latent variable $z$ beside the observation.

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="At one D4 state, squared error fits the normalized demonstrations (-1, 0) and (1, 0) with (0, 0), inside an obstacle at the origin, and a 2 : 1 record with (-1/3, 0), which no demonstrator took; below, what a token head, a denoiser and a CVAE decoded at z = 0 each return on the 1 : 1 record">
  <defs><marker id="aBce" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) what squared error returns at one D4 state</text>
  <rect x="346.0" y="40" width="36.0" height="92" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <text x="364.0" y="37" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">obstacle</text>
  <text x="184" y="74" font-size="11" fill="currentColor" text-anchor="end">two demos, 1 : 1</text>
  <circle cx="244.0" cy="70" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="484.0" cy="70" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="244.0" y="60" font-size="10" fill="currentColor" text-anchor="middle">demo (−1, 0)</text>
  <text x="484.0" y="60" font-size="10" fill="currentColor" text-anchor="middle">demo (1, 0)</text>
  <path d="M 359.0 65 L 369.0 75 M 359.0 75 L 369.0 65" stroke="currentColor" stroke-width="2.0"/>
  <text x="372.0" y="86" font-size="11" fill="currentColor" font-weight="bold">fit (0, 0)</text>
  <text x="184" y="116" font-size="11" fill="currentColor" text-anchor="end">three demos, 2 : 1</text>
  <circle cx="244.0" cy="112" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="244.0" cy="105" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="484.0" cy="112" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M 319.0 107 L 329.0 117 M 319.0 117 L 329.0 107" stroke="currentColor" stroke-width="2.0"/>
  <text x="304.0" y="131" font-size="11" fill="currentColor"><tspan font-weight="bold">fit (−1/3, 0)</tspan>: no demonstrator's action</text>
  <line x1="196.0" y1="146" x2="532.0" y2="146" stroke="currentColor" stroke-width="0.9"/>
  <line x1="244.0" y1="146" x2="244.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="244.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">−1</text>
  <line x1="324.0" y1="146" x2="324.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="324.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">−1/3</text>
  <line x1="364.0" y1="146" x2="364.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="364.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="484.0" y1="146" x2="484.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="484.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <text x="184" y="150" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.8">normalized Δx (Δy = 0)</text>
  <text x="12" y="192" font-size="12" fill="currentColor">(b) what each head of §6 returns on the 1 : 1 record</text>
  <line x1="364.0" y1="202" x2="364.0" y2="344" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <text x="184" y="226" font-size="11" fill="currentColor" text-anchor="end">token head</text>
  <rect x="236.0" y="208.0" width="16" height="22.0" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="0.9"/>
  <rect x="476.0" y="208.0" width="16" height="22.0" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="0.9"/>
  <text x="244.0" y="204.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="484.0" y="204.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="196" y="244" font-size="10.5" fill="currentColor">sample or arg max: one mode · average the bins: (0, 0) again</text>
  <text x="184" y="276" font-size="11" fill="currentColor" text-anchor="end">denoiser</text>
  <circle cx="244.0" cy="264" r="3.4" fill="currentColor"/>
  <circle cx="244.0" cy="272" r="3.4" fill="currentColor"/>
  <circle cx="484.0" cy="268" r="3.4" fill="currentColor"/>
  <text x="196" y="294" font-size="10.5" fill="currentColor">every sample lands in one mode</text>
  <text x="184" y="324" font-size="11" fill="currentColor" text-anchor="end">CVAE, z = 0 (ACT)</text>
  <rect x="240.0" y="316" width="8" height="8" fill="currentColor"/>
  <text x="244.0" y="310" font-size="10" fill="currentColor" text-anchor="middle">chunk t</text>
  <rect x="480.0" y="316" width="8" height="8" fill="currentColor"/>
  <text x="484.0" y="310" font-size="10" fill="currentColor" text-anchor="middle">chunk t+1</text>
  <line x1="252.0" y1="320" x2="354.0" y2="320" stroke="currentColor" stroke-width="1.1" marker-end="url(#aBce)"/>
  <line x1="476.0" y1="320" x2="374.0" y2="320" stroke="currentColor" stroke-width="1.1" marker-end="url(#aBce)"/>
  <path d="M 359.5 315.5 L 368.5 324.5 M 359.5 324.5 L 368.5 315.5" stroke="currentColor" stroke-width="1.8"/>
  <text x="364.0" y="310" font-size="10" fill="currentColor" text-anchor="middle">ensembled</text>
  <text x="196" y="342" font-size="10.5" fill="currentColor">no latent picks a mode · averaging chunks that disagree lands between</text>
  <line x1="196.0" y1="356" x2="532.0" y2="356" stroke="currentColor" stroke-width="0.9"/>
  <line x1="244.0" y1="356" x2="244.0" y2="360" stroke="currentColor" stroke-width="0.9"/>
  <text x="244.0" y="371" font-size="10" fill="currentColor" text-anchor="middle">−1</text>
  <line x1="364.0" y1="356" x2="364.0" y2="360" stroke="currentColor" stroke-width="0.9"/>
  <text x="364.0" y="371" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="484.0" y1="356" x2="484.0" y2="360" stroke="currentColor" stroke-width="0.9"/>
  <text x="484.0" y="371" font-size="10" fill="currentColor" text-anchor="middle">1</text>
</svg>

At one D4 state, in normalized units, squared error fits the two demonstrations $(-1,0)$ and $(1,0)$ with their mean $(0,0)$, inside an obstacle at the origin, and a $2:1$ record with $(-1/3,0)$, an action no demonstrator took. Below, what §6's three heads return on the $1:1$ record: a token head holds $0.5$ on each mode and returns one only if it samples or takes the arg max, every sample of a denoiser lands in a mode, and ACT's CVAE, decoded at $z=0$ with its overlapping chunks averaged, can land between them.

The word doing the work in that averaging argument is the objective's name, and the name has three conditions that papers drop one at a time.

> **Behaviour cloning, defined.** **Behaviour cloning** is a *training objective* — supervised regression or classification of the demonstrator's action given the observation — not an architecture, not a policy class, and not "imitation learning" in general. Three defining conditions. The data are **(observation, action) pairs produced by a demonstrator**, so the label is an action and not a return. The loss is a **supervised discrepancy on the action alone**, with no reward signal and no environment interaction while training. And the expectation is taken **under the demonstrator's state distribution**, not the learner's — the condition that makes it a distribution-shift problem rather than ordinary regression.
>
> $$\theta^\star=\arg\min_\theta\ \mathbb E_{(o,a)\sim\mathcal D_{\text{demo}}}\big[c\big(a,\pi_\theta(o)\big)\big]$$
>
> where $\mathcal D_{\text{demo}}$ is the demonstration set, $c$ the per-action cost (squared error for continuous actions, cross-entropy for tokenized ones; 7.5 §1 writes the same imitation loss as $\ell$, but on this page $\ell$ is the reaction latency) and $\pi_\theta$ the policy — and the subscript on the expectation is the whole difficulty, because at deployment the states are drawn from $\pi_\theta$'s own visits and nothing in this objective has looked at those. That mismatch is **covariate shift**, and its cost is **compounding error**: a small mistake moves the robot to a state no demonstration visited, where the next mistake is likelier, so over a $T$-step task plain behaviour cloning's expected cost can grow as $O(\epsilon T^2)$ for a per-step error rate $\epsilon$, against $O(\epsilon T)$ for DAgger. Those are the two bounds of [[02-foundations/rl-robot-learning|7.5 §1]], which also writes behaviour cloning as maximum likelihood, with squared error as the Gaussian case.
>
> - **Example**: fitting D4's three deltas to the catalog chunk under squared error. The loss is computable from logged data alone, which is exactly why the method scales to teleoperated datasets.
> - **Non-example**: DAgger and any method that queries the expert on states the *learner* reached. It keeps the supervised loss but replaces condition three — the change that buys the $O(\epsilon T)$ bound — which is why it is a different algorithm with a different data-collection cost, not a tweak.
> - **Non-example**: offline RL on the same demonstration file. Same bytes, but it uses reward and a value estimate, so condition two fails and its failure modes are value-function failures rather than compounding-error ones.
> - **Why it matters**: the two-mode mean $(0,0)$ above is not a bug in the fit — it is the exact minimizer under condition two. Low validation loss on demonstrator states therefore predicts closed-loop success only when the policy stays on those states, which is the claim §4 asks papers to separate from the loss curve.

### 3. Chunking trades smoothness against feedback

Long chunks cut the number of decisions a task needs: a $T$-step task becomes about $T/k$ of them, which is [[02-foundations/rl-robot-learning|7.5 §1]]'s cheap remedy for compounding error. At a $1\%$ error per decision, $500$ single steps finish cleanly $0.99^{500}=0.7\%$ of the time and $50$ chunks of ten $0.99^{50}=60.5\%$ (7.5's $k$ is a chunk executed in full, $H=k$ in this page's notation). Chunks also cut the forward passes per second and can preserve coordinated motion, but they delay correction. If inference takes 100 ms and the robot executes 10 actions at 20 Hz, a full open-loop chunk lasts 0.5 s. Receding execution—predict 10, execute 2, observe again—restores feedback at extra compute cost. What one forward pass is inside a token policy — a causally masked decoder emitting one token at a time, with a KV cache that spares each step from rerunning the prefix — is [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer §3 and §7]].

The worked case turned that sentence into two formulas, $\text{age}_{\max}=(m+k-1)\Delta t$ and $\ell(k)$, and §5 measures what is bought on the other side. First the object being traded:

> **Action chunking, defined.** **Action chunking** is a property of a policy's *decision granularity* — how many future actions one observation commits the robot to — and therefore a property of the interface, not of the architecture or the loss. Three defining conditions. One forward pass **emits $H\ge2$ actions indexed by future time**, not a single action. Some **stride $k\le H$ of them is executed before the next observation is consumed**, and $k$ is a second number that papers often leave unstated. And over that stride the robot is **open loop**: no observation enters between the committed actions.
>
> $$\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l)\ \longrightarrow\ \text{execute }a_{t:t+k-1}\ \longrightarrow\ \text{observe at }t+k$$
>
> where $H$ is the predicted horizon, $k$ the executed stride, and $o_{\le t}$ everything observed up to the prediction — so $H$ sets what the network must learn to represent while $k$ alone sets the latency, which is why reporting only $H$ describes the network and not the robot.
>
> - **Example**: D4 with $H=k=3$ at 20 Hz. One observation commits $0.15\,\mathrm{s}$ of motion and, with $m=2$ steps of inference delay, the oldest action executed is $0.20\,\mathrm{s}$ stale.
> - **Non-example**: a policy that predicts $H=10$ and executes one before re-observing. That is a multi-step prediction *objective*; $k=1$ leaves the interface exactly as unchunked as a single-step policy, and the $k=1$ row of §5 shows it buys none of chunking's smoothness.
> - **Non-example**: one command that the controller takes many cycles to track, such as "move to this pose." The commitment is real but it is one decision, so the horizon lives in the controller's interpolator rather than in the policy's output, and none of the arithmetic above applies to it.
> - **Why it matters**: $k$ is the only knob that appears on both sides of the trade — it lengthens the reaction latency $\ell(k)$ and it divides the number of independent perception draws per second, so smoothness and responsiveness cannot be tuned separately. §5 is that sentence as a table.

### 4. What VLA evidence proves

A VLA paper usually reports one success rate beside a video, and neither says which ability improved or how far the number can be trusted. Separate semantic generalization (choosing the relevant object), motor competence (executing contact-rich motion), embodiment transfer, and recovery. Success rate must define episode, reset, intervention, tolerance, and environment variation. An impressive video is a sample, not an estimator.

**How much a success rate says.** A success rate is a count, and a count carries an interval — the Wilson interval, derived in part 4 of the worked case of [[02-foundations/ml-practice|9. ML Practice]] (more in [[06-research-practice/experimental-design-reproducibility|research practice 2, Experimental Design §4]], block 5 of the path). At 95%, $8$ successes in $10$ trials give $[0.49,\ 0.94]$ and $6$ in $10$ give $[0.31,\ 0.83]$, so a ten-trial table showing $80\%$ against $60\%$ has not ranked the two policies. At $100$ trials each the intervals, $[0.71,\ 0.87]$ and $[0.50,\ 0.69]$, no longer overlap; they first separate at about $85$ trials per policy. A clean run proves less than it seems: $n$ successes in a row exclude, at 95%, only failure rates above $1-0.05^{1/n}\approx3/n$, so thirty straight successes still allow a failure rate of $9.5\%$. Ask for $n$ beside every percentage, and for the intervals whenever two percentages are compared. A claim of embodiment transfer raises further questions of its own, collected in §7.

**After cloning: learning from the robot's own trials.** The closed-loop trials this section counts are also the data behaviour cloning never sees, the robot's own states, where §2's compounding error happens. [[02-foundations/rl-robot-learning|7.5 §4]] fine-tunes the cloned policy on them with RL: it keeps improving on task reward — often a binary success check like the detector of [[03-deep-learning/vlm/index|3. VLM §4]] — while a KL term, a penalty on how far the new policy's action distribution has drifted from the cloned one's, holds it near what the demonstrations taught. The term's weight $\beta$ sets how much reward one unit of drift must buy, and $\beta\to\infty$ returns the cloned policy unchanged. Because the policy now acts in order to learn, one of that section's honest safety answers is a filter after the policy that projects every command into a certified safe set, whatever the network outputs; D4's interface limit, $\pm a_{\max}$ on each axis, is the simplest such set. Newer recipes add the operator: π\*0.6's RECAP trains on demonstrations, the robot's own rollouts and the corrections an operator makes during execution, by conditioning the policy on an estimated advantage — how much better an action did than the policy's average choice in that state ([[01-canonical-papers/notes/4-vla/pi0|π0]]). Either claim is a closed-loop one and owes the same counts: success before and after, each with its $n$ and interval, and the robot hours the trials cost.

Read [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/act|ACT]], and [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] in that order before newer generalist policies.

### 5. The chunk-length sweep

Which $k$ should this robot run? The worked case priced what a longer chunk costs — staleness and reaction latency — and this lab measures what it buys on the other side of §3's trade. It is the picture at the top of the page with one knob. The episode is 3 s at 20 Hz; the target sits at $g=(-0.04,-0.02)$ until control step $20$ and then moves to $(-0.04,+0.02)$, which is a scene change the policy can only learn about through a new observation. Perception jitter is a frozen sine pair rather than a random draw, so the table below is identical on every machine.

Two things are measured. **Travel** is $\sum_n\lVert a_n\rVert$, the path the tool actually walks, against the $0.10\,\mathrm{m}$ the task needs (6 cm out, 4 cm back up); it goes up when jitter makes consecutive plans disagree. **Reversals** count steps where $a_n^\top a_{n+1}<0$, a direction flip the operator sees as chatter. Against them stand $\ell(k)$ from the worked case and the time to get back within 5 mm of the moved target.

```python
import numpy as np

dt, t_inf = 0.05, 0.10                 # 20 Hz control period, 100 ms inference
m = int(np.ceil(t_inf / dt))           # inference delay, in control steps
N, njump = 60, 20                      # 3 s episode; the target moves at t = 1.0 s
amax, delta, sigma = 0.02, 0.005, 0.002               # metres
g_before = np.array([-0.04, -0.02])    # "move left, then down"
g_after = np.array([-0.04, 0.02])      # the panel is re-seated: the target is now up

def jitter(s):                         # frozen perception jitter, no RNG
    return sigma * np.array([np.sin(7.0 * s + 1.0), np.sin(11.0 * s + 2.0)])

def chunk(p_hat, g_hat, k):            # D4's policy: one axis at a time
    out, q = [], p_hat.copy()
    for _ in range(k):
        r = g_hat - q
        a = np.zeros(2)
        if abs(r[0]) > delta:
            a[0] = np.clip(r[0], -amax, amax)
        elif abs(r[1]) > delta:
            a[1] = np.clip(r[1], -amax, amax)
        out.append(a)
        q = q + a
    return out

def run(k):
    p, traj, acts, src, plan, obs = np.zeros(2), [], [], [], [], 0
    for n in range(N):
        if n % k == 0:                             # a new chunk starts here
            obs = max(n - m, 0)                    # the scene it was computed from
            g_seen = g_before if obs < njump else g_after
            plan = chunk(p + jitter(n + 100), g_seen + jitter(obs), k)
        a = plan[n % k]
        traj.append(p.copy()); acts.append(a); src.append(obs)
        p = p + a
    traj.append(p.copy())
    acts = np.array(acts)
    travel = float(np.sum(np.linalg.norm(acts, axis=1)))
    rev = int(np.sum(np.sum(acts[:-1] * acts[1:], axis=1) < 0))
    react = next(((n - njump) * dt for n in range(njump, N) if src[n] >= njump), None)
    reacq = next(((n - njump) * dt for n in range(njump, N + 1)
                  if np.linalg.norm(traj[n] - g_after) <= 0.005), None)
    return travel, rev, react, reacq

for k in (1, 2, 3, 4, 5, 10, 20):
    travel, rev, react, reacq = run(k)
    closed = (k * int(np.ceil((njump + m) / k)) - njump) * dt       # worked case
    assert abs(closed - react) < 1e-12
    print(f"{k:>3} {k*dt:>5.2f} {'yes' if k*dt >= t_inf else 'no':>4} {(m+k-1)*dt:>5.2f} {travel*100:>7.2f} "
          f"{rev:>3} {react*1000:>6.0f} {reacq:>5.2f}")
```

| $k$ | $k\Delta t$ (s) | schedulable | worst age (s) | travel (cm) | reversals | $\ell(k)$ (ms) | re-acquire (s) |
|---:|---:|:--|---:|---:|---:|---:|---:|
| 1 | 0.05 | no | 0.10 | 31.30 | 6 | 100 | 0.25 |
| 2 | 0.10 | yes | 0.15 | 30.59 | 10 | 100 | 0.20 |
| 3 | 0.15 | yes | 0.20 | 19.86 | 0 | 200 | 0.35 |
| 4 | 0.20 | yes | 0.25 | 13.19 | 0 | 200 | 0.35 |
| 5 | 0.25 | yes | 0.30 | 14.83 | 0 | 250 | 0.40 |
| 10 | 0.50 | yes | 0.55 | 10.30 | 0 | 500 | 0.60 |
| 20 | 1.00 | yes | 1.05 | 9.38 | 0 | 1000 | 1.10 |

Five readings, in the order a reviewer should take them.

**The $k=1$ row is not an option on this robot.** One action per forward pass needs a 50 ms inference budget and this policy takes 100 ms, so the controller would starve. It is in the table because it is the limit people imagine when they say "just replan every step," and it does not even win the thing it is imagined to win: its reaction latency is the same 100 ms as $k=2$, because below $k=m$ the inference delay, not the chunk, sets the floor.

**Chattering has a threshold, not a slope.** Reversals are 6 and 10 at $k=1,2$ and exactly zero from $k=3$ up. The jitter did not change; what changed is that a chunk of three or more commits to an axis for long enough that the next draw of noise cannot reverse it mid-motion.

**Travel falls by a factor of 3.3 across the column**, 31.30 cm down to 9.38 cm against a task that needs 10 cm — a little under it, because the policy stops once it is within $\delta=5\,\mathrm{mm}$ of the target it sees on each axis. Replanning every step spends more than three times the necessary motion re-deciding, which on hardware is wear, heat, and audible noise, and none of it appears in an offline action MSE.

**The latency column is the price, and it grows with $k$ — but not in proportion.** For the change at step 20 it reads 100, 100, 200, 200, 250, 500 and 1000 ms, matching $\ell(k)$ from the worked case row for row — the `assert` in the listing is that check. Move the change to another step and each entry moves between $m\Delta t=100\,\mathrm{ms}$ and the worst action age $(m+k-1)\Delta t$, depending on where the change falls between two chunk boundaries; the [[03-deep-learning/index|deep-learning index]]'s cumulative problem 3(c) proves both bounds. At $k=3$ that is anything from 100 to 200 ms. A target that moves once per second is tracked by $k\le5$ and missed entirely by $k=20$.

**One number in the table is not part of the trend.** Travel at $k=5$ (14.83 cm) is higher than at $k=4$ (13.19 cm). The jitter is a fixed sequence, so where the chunk boundaries land inside it matters at the 10% level; the factor of 3.3 across the whole column is the effect, and a 12% difference between neighbours is phase. A paper reporting the second kind of difference as a result owes you several seeds.

The design conclusion for this robot: $k$ between 3 and 5 — a commitment of 0.15–0.25 s — removes every reversal and more than half the wasted travel while keeping reaction within 250 ms. Going further to $k=20$ saves a further 5.5 cm of travel and costs three quarters of a second of blindness, which is only a good trade if nothing in the scene moves.

### 6. Two action heads: tokens and denoisers

*In one sentence:* the action head turns the policy's features into the numbers the robot executes, and its two families pay differently — a token head decodes one number at a time, and a denoiser, a network that refines random noise into the whole chunk, pays a fixed number of passes for all of it — so the choice follows the chunk length and the control budget.

*If you need only one thing from this section:* the crossover — a token head needs $D\times H$ sequential passes and a denoiser $N$ whatever $H$ is, so on D4 with $D=2$ and $N=10$ tokens are cheaper below $H=5$ and denoising above it (the **Denoisers** paragraph and the table below).

§1 said the action representation is part of the method. The head that produces it is the other half, and the field has settled on two families plus a hybrid. Both answer §2's averaging problem, and they pay for it differently.

**Discrete tokens.** Cut each action dimension into bins and classify, so control becomes next-token prediction and the whole apparatus of a pretrained language model transfers unchanged. [[01-canonical-papers/notes/4-vla/rt-1|RT-1]] uses $11$ dimensions at $256$ bins each; [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]] maps the same $256$ bins onto reserved LM tokens. Quantization is rarely the accuracy limit: on **D4**, $256$ bins spread over $\pm a_{\max}=\pm0.02\,\mathrm{m}$ give a step of $0.04/256=0.16\,\mathrm{mm}$, about thirteen times finer than the page's own perception jitter $\sigma=2\,\mathrm{mm}$. The cost is sequential: one decode per token, so a chunk of $H$ actions in $D$ dimensions needs $D\times H$ forward passes — $2\times3=6$ for D4's frozen chunk. That is what caps autoregressive token policies near $6\,\mathrm{Hz}$ in OpenVLA's measurements. Compression changes the count but not the principle: FAST (Pertsch et al., 2025) tokenizes a whole chunk after a discrete cosine transform, so a smooth high-frequency chunk needs far fewer than $D\times H$ tokens, and π0-FAST matched the diffusion π0 while training up to five times faster ([[01-canonical-papers/notes/4-vla/pi0|π0]]).

**Denoisers.** Sample the whole chunk instead: [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] denoises a $16$-action chunk conditioned on the observation, at about $10$ DDIM-style steps at inference — DDIM being a deterministic sampler that visits only a few of the noise levels the network was trained on ([[03-deep-learning/diffusion/index|6. Diffusion & Flow §1]]) — and executes the first few before re-planning, the receding horizon of [[04-robotics/mpc|7. MPC]]. [[01-canonical-papers/notes/4-vla/pi0|π0]] replaces diffusion with flow matching — training the network to predict the velocity that carries noise to data along a chosen path, then integrating it in a few steps ([[03-deep-learning/diffusion/index|6. Diffusion & Flow §3]]) — in a separate action expert on a VLM backbone, and reports $50\,\mathrm{Hz}$ continuous chunks. Its cost is $N$ passes *whatever the chunk length*, which gives the crossover: a token head is cheaper while $D\times H<N$, a denoiser once the chunk is longer. On D4 with $D=2$ and $N=10$, the crossover sits at $H=5$ — below it, tokens; above it, denoising.

**Why ten passes fit the budget.** π0 is one transformer with two sets of weights: image and text tokens pass through the $3$B PaliGemma weights, robot-state and action tokens through a $300$M set of their own, and the two meet only in self-attention. The split is what makes $N$ passes affordable. The observation is encoded once and its keys and values are cached, so each of π0's ten flow steps reruns only the small expert on the action tokens. On an RTX 4090 the ten steps together take $27\,\mathrm{ms}$, less than the single $32\,\mathrm{ms}$ pass over the observation, in a $73\,\mathrm{ms}$ total on board. The collapsed note below says what this split is called and how it differs from a mixture of experts.

> [!note]- Deeper · 더 깊이
> **A mixture of transformers, not of experts.** π0 calls its split a mixture of experts with two elements. Liang et al. (2024), studying the same split for text, images and speech, call it a **Mixture of Transformers**: every weight except the embeddings — feed-forward layers, attention projections, layer norms — is kept separate per modality, while attention still runs over the whole sequence, and in their 7B text-and-image setting it matched a dense model at $55.8\%$ of the training FLOPs. Unlike the usual mixture of experts ([[03-deep-learning/foundations/attention-transformer|1.2 §9]]), no learned gate chooses: a token's type decides its weights.

**A third answer, and what they share.** [[01-canonical-papers/notes/4-vla/act|ACT]] keeps plain regression but trains it as a CVAE, the conditional form of the variational autoencoder whose latent-variable model is [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs §1]]: its decoder takes a latent variable $z$ beside the observation, so the variation between demonstrations goes into $z$ instead of blurring the fit. At test time it fixes the latent at the prior mean, zero, and decodes deterministically (Zhao et al. 2023, §IV-B), so on the robot no latent picks a mode. All three exist because $L_{\mathrm{BC}}$ under a unimodal head returns the average of valid actions: for the two demonstrations $(-1,0)$ and $(1,0)$ it returns $(0,0)$, straight into the obstacle. A token head keeps both modes *in its bin distribution* — but only if the action is **sampled or taken as the argmax**; average the distribution and $(0,0)$ returns. A denoiser draws one mode by construction. A CVAE could draw one per sampled latent, but ACT decodes one chunk at $z=0$, and its temporal ensembling — executing at each step a weighted average of the actions that the overlapping chunks predicted for that step — can, near a fork, bring §2's mean back ([[05-construction-robotics/imitating-contact|10. Imitating Contact §4]]). §2's figure draws all three.

| | tokens | denoiser (diffusion or flow) | CVAE regression |
|---|---|---|---|
| passes per chunk | $D\times H$, sequential | $N$, independent of $H$ | $1$ |
| multimodality | in the bin distribution, if you sample | by construction | in training, through the latent; ACT decodes at $z=0$ |
| precision limit | bin width (on D4, $0.16\,\mathrm{mm}$) | denoising steps cut for speed | regression variance |
| what it inherits | a pretrained LM's weights and language generalization | diffusion's sampler, and MPC's receding horizon | a plain Transformer decoder |

So the choice follows the budget of §3 rather than fashion: keep tokens when the language backbone's generalization is the point and chunks are short; move to a denoiser when the chunk is long or the demonstrations are strongly multimodal; and in either case check the head against $\ell(k)$ before believing a demo video.

**Reasoning is paid in the same currency.** A token head can also be taught to write before it acts. RT-2 tried this as a small variant that states a plan in words — "Plan: pick energy drink" — before its action tokens ([[01-canonical-papers/notes/4-vla/rt-2|RT-2]]). Embodied chain-of-thought (ECoT; Zawalski et al. 2024) makes it systematic: OpenVLA is fine-tuned to write a plan, the current sub-task, a movement primitive, object bounding boxes and the gripper's position in the image, and only then the action, from reasoning labels generated automatically by pretrained detectors and a large language model. That raised OpenVLA's absolute success rate by $28$ points on generalization tasks — new objects, scenes, viewpoints and instructions — with no additional robot data. Every reasoning token is a sequential decode, exactly like an action token, and ECoT's tokens per step went from $7$ to $350$. On D4, a chain of that length would turn the token head's $6$ passes into $343+6=349$. The paper's remedy is §3's trade in another place: regenerate the high-level plan and sub-task only every fifth step, which made inference about a quarter faster and, on a three-task subset, succeeded $72\%$ of the time against $63\%$ for reasoning afresh at every step. What reasoning buys is generalization and a failure you can read — a wrong bounding box shows where the policy went wrong. What it costs is rate, so a reasoning policy's control frequency belongs in the same row as its success rate. The collapsed note below places two production systems on this trade.

> [!note]- Deeper · 더 깊이
> **Two production arrangements.** Gemini Robotics 1.5 builds the idea into a production VLA, interleaving its actions with multi-level reasoning in natural language beside a separate embodied-reasoning model for planning and progress estimation ([[01-canonical-papers/notes/4-vla/gemini-robotics|Gemini Robotics]]). Generalist's GEN-0 argues for the opposite arrangement: sensing and acting tokens in asynchronous, continuous-time streams, with no fast–slow split. Both are claims about where the reasoning's decodes are spent, which is the question the arithmetic above asks.

### 7. One policy, many bodies: the embodiment gap

*In one sentence:* once one policy is trained on many robots, the same action numbers mean different motions on different bodies, and each generalist design is a way of telling the policy which body it is driving.

*If you need only one thing from this section:* a normalized label does not say which robot it came from — D4's normalized chunk replayed on arm B overshoots by $6$ and $3\,\mathrm{cm}$, two and a half times the intended motion (**The gap on D4, in numbers**).

§1 showed that a unit error is a physical error on one robot. Pool demonstrations from many robots and the same error becomes systematic, because each robot's logs speak its own action convention. [[01-canonical-papers/notes/4-vla/open-x-embodiment|Open X-Embodiment]] pooled 22 robots, aligned their actions only coarsely, and its authors say plainly that "the same action vector may induce very different motions for different robots." That sentence is the **embodiment gap** as a policy sees it: everything that makes one action mean different motions on two bodies, or one motion need different actions — units and scale, coordinate frame, absolute or delta values, control rate, action dimension, kinematic limits, and where the camera sits.

**The gap on D4, in numbers.** Pool D4 with a second arm, B, that logs the same kind of 2-D end-effector delta but allows $a_{\max}=0.05\,\mathrm{m}$ per step at $5\,\mathrm{Hz}$, and normalize each dataset by its own limit so that both fill $[-1,1]$.

- D4's frozen chunk becomes $(-1,0)$, $(-1,0)$, $(0,-1)$.
- Executed on B, the same numbers move $(-0.05,0)$, $(-0.05,0)$, $(0,-0.05)$: $0.10\,\mathrm{m}$ left and $0.05\,\mathrm{m}$ down in $3\times0.2=0.6\,\mathrm{s}$, where D4 moves $0.04$ and $0.02\,\mathrm{m}$ in $0.15\,\mathrm{s}$.
- Aimed at D4's target $g=(-0.04,-0.02)$, B overshoots by $6$ and $3\,\mathrm{cm}$ — two and a half times the intended motion — at $0.05/0.2=0.25\,\mathrm{m/s}$ where D4 moves at $0.02/0.05=0.4\,\mathrm{m/s}$.

Nothing in a normalized label says which robot it came from. Only the observation can, and only if the camera view or the proprioception differs enough to tell.

**Five designs, each paying somewhere.** The generalist policies close the gap in five ways.

| design | how the body enters the policy | what it costs |
|---|---|---|
| coarse alignment (the RT-X models of [[01-canonical-papers/notes/4-vla/open-x-embodiment\|OXE]]) | one 7-D end-effector action — position, rotation and gripper, or their rates — and one canonical camera per dataset; frames and absolute-or-delta conventions left as each robot had them | the policy must recognize the body from the image, and two robots that look alike share one convention |
| pad to the largest body ([[01-canonical-papers/notes/4-vla/pi0\|π0]]) | an 18-D action — two 6-DoF arms, two grippers, a mobile base and a torso lift — zero-padded for smaller robots, missing cameras masked | D4 would fill 2 of 18 dimensions: free for a denoiser, whose $N$ passes do not depend on width, while a token head would decode $18\times3=54$ tokens for D4's chunk instead of $6$ |
| a head per body ([[01-canonical-papers/notes/4-vla/octo\|Octo]], [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]]) | a shared trunk, with new observation and action tokens and a small head for each new robot (Octo), or embodiment-specific encoders and decoders around one model (GR00T) | every new body needs data of its own; Octo's recipe is about $100$ demonstrations and $5$ hours of fine-tuning |
| latent actions from video (the idea of [[01-canonical-papers/notes/5-world-models/genie\|Genie]], at the base of GR00T's data) | actions inferred as discrete codes between video frames, with no action labels ([[03-deep-learning/diffusion/vae-gan\|6.1 §10]]) | a latent action is not a command: a body-specific layer must still map it to one |
| learned transfer across bodies ([[01-canonical-papers/notes/4-vla/gemini-robotics\|Gemini Robotics]] 1.5) | one VLA trained on heterogeneous multi-embodiment data with a Motion Transfer mechanism in its architecture; its successor's on-device model adapts to a new body with a few hours of data | the mechanism is described in a technical report but not released, and the evaluation is the company's |

Three recent developments stretch the table — GR00T N1.7's actions shared with human video, Skild AI's policy trained across $100{,}000$ simulated bodies, and pretraining on up to a million hours of human video and device recordings — and the collapsed note below gives their numbers and what each leaves to check.

> [!note]- Deeper · 더 깊이
> **GR00T N1.7.** GR00T's later versions moved part of the way back toward a shared convention: N1.7 (2026) represents actions as *relative* end-effector deltas shared by robots and human video, which is what lets $20{,}000$ hours of human video train the same head ([[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]]). It is a coarse alignment in OXE's spirit, so the questions below apply to it too: in what units, in which frame, at what rate.
>
> **Skild AI's omni-bodied policy.** Skild AI pushes the fifth design furthest: an "omni-bodied" policy trained in simulation across $100{,}000$ different robot bodies, reported to control bodies left out of training and to re-adapt within seconds after losing a limb ([Skild AI](https://www.skild.ai/blogs/omni-bodied)). Those are company demonstrations, and the same post warns that clean, controlled videos can create an illusion of competence.
>
> **Human hands are becoming the largest body in the pool.** GR00T N1.7 pretrains on $20{,}000$ hours of human video; DYNA-2 (Dyna Robotics, August 2026) on more than a million hours of head-mounted human video with no robot data at all, recovering pseudo-actions from 3D hand poses ([Dyna](https://www.dyna.co/dyna-2)); GEN-0 (Generalist AI, 2025) on over $270{,}000$ hours of real manipulation recorded by thousands of devices and robots ([Generalist AI](https://generalistai.com/blog)). DYNA-2 states its gains as power laws, and the exponents are worth reading before the adjectives. Held-out human-data error falls as $D^{-0.0184}$, so a thousandfold more video lowers it by about $12\%$; zero-shot robot-action error falls as $D^{-0.0713}$, about $39\%$ per thousandfold. The gains are real, smooth and slow, and a customer deployment passed $87\%$ of the time against $46\%$ for its predecessor at the same post-training budget. The gap these models still have to cross is this section's own: a human hand is a body with its own kinematics, and a pseudo-action is an estimate of what it did.

**What the evidence says.** OXE's results split on how much data the target robot already has. On five robots with small datasets of their own, RT-1-X trained on the pool beat each lab's original method on four, and its mean success was $50\%$ higher than that of either the original method or RT-1 trained on the robot's own data. With a lot of data, it lost. On the WidowX's Bridge tasks it scored $27\%$ at both evaluation sites, against $40\%$ and $30\%$ for RT-1 trained on that data alone; on the Google robot's RT-1 tasks, $73\%$ against $92\%$. The 55B RT-2-X recovered — $50\%$, $30\%$ and $91\%$ — so the paper reads the loss as underfitting: a small model spends its capacity on the other bodies. Transfer of skills is also real. RT-2-X roughly tripled RT-2's score on emergent skills whose objects and motions appear only in the WidowX's data, and removing that dataset significantly reduced the gain.

**What to ask of a cross-embodiment claim**, adding to §4's evidence ladder:

- the action convention of each dataset — units, frame, absolute or delta, rate — and how it was converted;
- how the body is identified: by the image alone, by padding, or by a head of its own;
- how much data the target robot contributes;
- the specialist trained on that data alone, as the baseline, because OXE shows the verdict flips with it.

A construction machine sits at the far end of both axes. It will have little data of its own for a long time, which is where pooling helped. And its body is unlike anything in the pool — the OXE note finds nothing construction-like there — which is where coarse alignment is weakest and the D4-and-B arithmetic bites hardest. For such a body, convert the convention explicitly, in physical units and seconds, rather than trusting the policy to infer it from a camera image.

### 8. A demonstration as the prompt: in-context imitation

Everything so far teaches a policy by changing its weights. In-context learning — the finding of [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] that a large model can pick up a task from examples in its prompt, with no weight update — has a robot form: put a demonstration of the new task into the policy's context and let it imitate.

> **In-context imitation, defined.** **In-context imitation learning** is a property of a *trained policy at test time*: it performs a task it was not trained on, specified only by demonstrations placed in its input. Three defining conditions. The demonstration is **in the input**, as observation–action sequences, not in the training set. **No parameter changes** between receiving the demonstration and acting. And the task is **new** to the model, since imitating a task it already learned is retrieval or conditioning, not learning.
>
> $$a_{t:t+H-1}\sim\pi_\theta\big(\,\cdot\mid \underbrace{(o,a)^{\text{demo}}_{1:T}}_{\text{the prompt}},\ o_{\le t}\big),\qquad \theta\ \text{fixed}$$
>
> where $(o,a)^{\text{demo}}_{1:T}$ is the demonstration written into the input as $T$ observation–action pairs of the new task, $o_{\le t}$ is what the robot has observed of its own attempt so far, $a_{t:t+H-1}$ is the chunk it emits, and "$\theta$ fixed" says that no gradient step happens between reading the prompt and acting — so the whole task specification lives in the input and none of it in the weights.
>
> - **Example**: GEN-1.5's "physical prompting" below — a few seconds of a new task, dropped into the context of a model that is not retrained.
> - **Non-example**: fine-tuning on the same five-minute demonstration set. The data are identical; condition two fails, and it costs a training run.
> - **Non-example**: a language instruction naming a skill the policy was trained on. The input specifies the task, but condition three fails: nothing new is learned.
> - **Why it matters**: it moves the cost of a new task from a training run to the prompt, where it is paid at every step in tokens and latency (the price below), and a success rate counts as learning only while condition three holds, which is why the questions at the end of this section start with what pretraining already contained.

**Three steps to 2026.** Keypoint Action Tokens (Di Palo and Johns, 2024) wrote visual keypoints and action trajectories as text and let an off-the-shelf GPT-4 Turbo, trained only on language, imitate from a few demonstrations — on par with diffusion policies in the low-data regime ([arXiv:2403.19578](https://arxiv.org/abs/2403.19578)). ICRT (Fu et al., 2024) trained a causal transformer on sensorimotor trajectories and prompted it on a Franka with teleoperated trajectories of an unseen task ([arXiv:2408.15980](https://arxiv.org/abs/2408.15980)). **GEN-1.5** (Generalist AI, August 2026) calls it *physical prompting*: a $3$–$12$ s sensorimotor demonstration, recorded with handheld grippers or by the robot itself, is placed in the context of a multimodal model that keeps $30$ s of memory and emits actions at $100$ Hz ([Generalist AI](https://generalistai.com/blog/gen-1.5)). Across ten short dexterous tasks — jars, zippers, a wallet — one demonstration gave $59\pm10\%$ success with no gradient step, and ten gradient steps on five minutes of data, about fifty demonstrations, gave $83\pm9\%$. The company says nothing in the architecture or training was built for in-context learning, and names the limits itself: short-horizon tasks, modest rates, skills more brittle than fine-tuned ones. Skild AI's S1 (August 2026) — a company's product name, not S1, the construction track's facade-panel task of [[05-construction-robotics/site-engineering|2.5]] — takes a *video* demonstration instead and translates it to its own body, reporting $66\%$ on tasks unseen in pretraining against $9\%$ for a VLA baseline, and one demonstration worth about $380$ post-training episodes by its estimate ([Skild AI](https://skild.ai/blogs/s1)) — a company number again, with no task list to check it against.

**The price of a prompt, on D4.** A demonstration in the context is paid in tokens. Twelve seconds at D4's $20$ Hz is $240$ steps; with one observation token and $D=2$ action tokens per step, that is $720$ tokens encoded before the first action. With a key–value cache they are encoded once, but every later token still attends over them, so the prompt adds to each step's attention cost for as long as it stays in the context — the sequential budget of §6, now spent on memory instead of reasoning. Held as images instead, at $10$ frames a second and $256$ tokens a frame on a PaliGemma-sized backbone, thirty seconds of demonstration need a key–value cache of about $1.42$ GB; that count is self-check 7 of [[03-deep-learning/foundations/sequence-models|1.1 Sequence Models]], whose §13 shows the hybrids that shrink it, and the cache itself is [[03-deep-learning/foundations/attention-transformer|1.2 §7]] — both off the path until prompts get long. The same twelve seconds at GEN-1.5's $100$ Hz is $1{,}200$ action steps.

**What to ask of an in-context claim**, beside §4's evidence ladder:

- was the task, or one close to it, in pretraining — the line between learning and retrieval;
- how many trials, and what counts as success;
- how long the prompt is, and what latency it adds before the first action;
- the fine-tuned result at matched data, because GEN-1.5's own numbers price the choice: seconds of demonstration and no training for $59\%$, five minutes and a short training run for $83\%$.

For a construction crew the appeal is plain — show a new fixing task once with a handheld gripper and let the machine do it — and so is the caution: the evidence so far is short, simple, table-scale tasks.

### After reading

For any VLA, fill one row containing observation, language, action space/frame/rate, horizon $H$, executed stride $k$, training data/objective, controller, replanning, and evidence ladder. If the paper gives $H$ but not $k$, the row is incomplete and so is its latency claim. Name the action head too — tokens, denoiser or CVAE — and say which of §6's costs it pays. For a policy trained on many robots, say how the body enters it — alignment, padding, a head of its own or latent actions — and count the tokens decoded before the first action, reasoning included. For a claim of learning from the prompt, separate it from retrieval and from fine-tuning at matched data.

### Self-check

1. D4's interface accepts $a_{\max}=0.02\,\mathrm{m}$ per step at 20 Hz. What is the fastest tool speed this action representation can express, and what happens to a demonstration recorded at twice that speed?
2. A policy reports $H=16$ and 5 Hz inference. What is the longest open-loop interval consistent with that, and what extra number do you need to pin it down?
3. Why does the $k=2$ row of §5 have *more* reversals than $k=1$, although its chunk is longer?
4. A lab replaces the MSE head with a mixture of two Gaussians and the offline action error gets worse. Give a reading of that result under which the policy improved.
5. Which of D4's frozen numbers would have to change for the axis-at-a-time plan to cost the same travel as a straight line?
6. A cross-embodiment policy fine-tuned on 5,000 demonstrations of your arm succeeds $70\%$ of the time; a specialist trained on those 5,000 alone succeeds $75\%$. Before calling it negative transfer, what do you check, and which of OXE's results does it resemble?
7. ECoT raised OpenVLA's success by $28$ points. On §6's scale, what did that cost, and what would you ask before putting it on a 20 Hz arm?
8. A company reports $59\%$ success on new tasks from one demonstration placed in the prompt. Which of §8's three conditions would you check first, and what comparison turns the number into a decision?

> [!tip]- Answers
> 1. $a_{\max}/\Delta t=0.02/0.05=0.4\,\mathrm{m/s}$. A demonstration at $0.8\,\mathrm{m/s}$ cannot be represented: every label saturates at the clip, so the cloned policy is systematically slow and the error is invisible in a per-step loss computed *after* clipping. Units and limits are part of the label, not of the deployment.
> 2. $t_{\mathrm{inf}}=0.2\,\mathrm{s}$, and the open-loop interval is $k$ actions long, not $H$: anything from $k=H=16$ down to the smallest schedulable $k=\lceil t_{\mathrm{inf}}/\Delta t\rceil$. Without the control period $\Delta t$ and the executed stride $k$ the latency is unknown — that is why the After-reading row asks for both.
> 3. Reversals are counted per step, and both rows are in the regime where a fresh, independently jittered plan arrives faster than the tool can finish a 2 cm move. Which of the two counts more depends on where the boundaries land in the frozen jitter sequence. The result to quote is the threshold at $k=3$, not the difference between 6 and 10.
> 4. Offline error is measured against individual demonstrated actions, and the MSE head minimizes it by predicting the mean of modes. A mixture that puts half its mass on each of $(-1,0)$ and $(1,0)$ has a *higher* average distance to any single label while being the only one of the two that ever outputs a demonstrated action. The evidence that settles it is closed-loop success, not the loss.
> 5. The target. The travel penalty is $\lVert g\rVert_1/\lVert g\rVert_2$, so it is $1$ only when the target lies on an axis: $g=(-0.06,0)$ would cost the same 6 cm by either plan. No change to $a_{\max}$, $\delta$, or the rates removes it, because it is a property of the instruction's axis order and the target direction.
> 6. First the counting of §4: at $100$ trials each, $70\%$ and $75\%$ have overlapping intervals, $[0.60,\ 0.78]$ and $[0.66,\ 0.82]$, so nothing has been ranked yet. Then the conventions of §7: whether your arm's actions entered the pool in the same units, frame and rate as its labels — the D4-and-B case shows a normalized label moving a body two and a half times too far. If both hold up, it resembles OXE's large-data regime, where RT-1-X lost to the specialist ($27\%$ against $40\%$, $73\%$ against $92\%$) and the 55B RT-2-X closed the gap. The next experiment is therefore capacity — a larger model, or a head of its own for your arm — reported against the specialist baseline.
> 7. Sequential decodes: $7$ tokens per step became $350$, so D4's $6$ passes per chunk would become $349$. Ask for the control frequency actually reached and how the chain is scheduled — ECoT's own five-step hold of the plan and sub-task ran about a quarter faster and scored $72\%$ against $63\%$ on its subset — and whether the gain was measured on the kind of generalization your task needs: new objects, scenes, viewpoints or instructions. A plan held for five steps is a chunk of plans, so §3's age arithmetic applies to it: at 20 Hz the plan acting on the fifth step is at least $0.20\,\mathrm{s}$ older than the scene.
> 8. Condition three first: whether these tasks, or ones close to them, were in pretraining, because imitating a task already learned is retrieval, and a strong model will do it from any cue. Then the comparison at matched data: GEN-1.5's own fine-tune reached $83\%$ with five minutes of data and ten gradient steps, so the decision is whether $24$ points and less brittleness are worth a short training run per task. Add the prompt's cost in latency and the trial count behind the $59\%$.

### Problem set · 과제

Tier A. Using **D4** from [[03-deep-learning/lab-objects|0. Lab Objects]], this page, and [[02-foundations/lab-kernel|0.7 Lab Kernel]]. Original object and original problems — change the knobs in §5's listing; do not rewrite the loop. State the tier in your answer sheet.

1. **Draw.** The picture above, redrawn for the robot of problem 2 — its controller re-flashed to $50\,\mathrm{Hz}$, inference still $100\,\mathrm{ms}$ — at $k=5$: the loop with its two clocks labelled ($\Delta t$ on the controller edge, $t_{\mathrm{inf}}$ on the policy edge) and the chunk buffer as a box of length $k$; then the loop unrolled over control steps $45$–$59$, with the chunk boundaries, each chunk's observation step, the age of every executed action, and a scene change at $t=1.0\,\mathrm{s}$. Mark on the loop the one edge that does **not** exist, and say in a sentence what believing in it would mean.
2. **Derive.** The robot is re-flashed to run its controller at $50\,\mathrm{Hz}$ while inference still costs $100\,\mathrm{ms}$. (a) The smallest schedulable chunk $m$. (b) The worst-case action age at $k=5$. (c) $\ell(k)$ for a scene change at $t=1.0\,\mathrm{s}$, for $k=5$ and $k=20$. (d) Compare (c) against the 20 Hz numbers in §5 and say in one sentence what a faster controller did and did not buy.
3. **Do.** Fill the `?` in the patch below and re-run §5's sweep with it. The target now moves *twice* — up at step 20 and back down at step 40, one second apart — so a chunk long enough can spend a whole event chasing the previous one. Report travel, reversals, and the latency to each of the two changes for $k\in\{2,3,5,10,20\}$, and name the largest $k$ whose reaction to a change still arrives *before* the next change. The ideal travel for this episode is 14 cm (6 out, 4 up, 4 down).

```python
# patch to the §5 listing — fill ?, keep the rest of the loop
N, njump, njump2 = 80, 20, 40          # 4 s episode, two scene changes

def target(obs):                       # which target the observation at step obs saw
    if obs < njump:
        return g_before
    return ?                           # g_after until njump2, then g_before again

def lag(src, e):                       # latency from change e to the first informed action
    n = next((n for n in range(e, N) if ?), None)    # src[n] is at or after e
    return None if n is None else (n - e) * dt

# in run(): replace the g_seen lines with
#     plan = chunk(p + jitter(n + 100), target(obs) + jitter(obs), k)
# and return travel, rev, lag(src, njump), lag(src, njump2)
```

> [!note]- How to draw it · 그리는 법
> - Two clocks, not one: label the policy edge with $t_{\mathrm{inf}}$ and the controller edge with $\Delta t$. A single rate on the loop is the most common wrong drawing, and every latency number on this page comes from the two being different.
> - Draw the chunk buffer as a box of length $k$ and mark that it is refilled only when it empties, from an observation taken $m$ steps earlier, while its last $m$ actions are still to run. That box is where the open-loop interval lives.
> - Write the observation edge's age as $n-m$, not $n$: the action leaving the buffer at step $n$ was computed from a scene that is $m+(n\bmod k)$ steps old.
> - Draw no arrow from the buffer to the scene. The robot changes the world and the buffered plan does not; a loop drawn with that arrow has assumed the model's prediction is the world, which is the error §4 is about.
> - In the unrolled strip, put a boundary every $k$ steps and an arc from each chunk's observation step to its first action, $m$ steps long. With $m=k=5$ each arc starts exactly where the previous chunk began, so a scene change that falls on a boundary is read one chunk later.

> [!tip]- Solutions
> 1. Scene → observation (aged $n-m$) → policy ($t_{\mathrm{inf}}=100\,\mathrm{ms}$) → chunk buffer (length $k=5$) → controller ($\Delta t=20\,\mathrm{ms}$) → robot → scene, with the refill edge from the buffer back to the observation closing only every $k$ steps. Now $m=\lceil0.10/0.02\rceil=5=k$, so every refill uses the observation taken one chunk earlier: the chunks that start at steps $45$, $50$ and $55$ were computed from steps $40$, $45$ and $50$, and in every chunk the executed actions are $5,6,7,8,9$ steps old, a worst age of $9\times0.02=0.18\,\mathrm{s}$. The scene change at $t=1.0\,\mathrm{s}$ is step $50$. The chunk that starts there was computed from step $45$ and cannot know it, so the first informed action is at step $55$: $\ell=5\times0.02=0.10\,\mathrm{s}$, against the picture's $0.20\,\mathrm{s}$ at $20\,\mathrm{Hz}$ and $k=3$. The edge that does not exist is buffer → scene: the plan does not move the world, only the executed action does. Drawing it is assuming the prediction is the state, which is how an open-loop chunk gets reported as if it had been verified.
> 2. (a) $\Delta t=0.02\,\mathrm{s}$, so $m=\lceil 0.10/0.02\rceil=5$ — the faster controller *raised* the minimum chunk from 2 steps to 5. (b) $(m+k-1)\Delta t=(5+4)\times0.02=0.18\,\mathrm{s}$, against $0.30\,\mathrm{s}$ at 20 Hz. (c) The change is now at step $n_j=50$; $k=5$: $\lceil 55/5\rceil=11$, boundary 55, $\ell=5\times0.02=0.10\,\mathrm{s}$; $k=20$: $\lceil55/20\rceil=3$, boundary 60, $\ell=10\times0.02=0.20\,\mathrm{s}$. (d) At equal $k$ the faster controller cut latency (0.25 → 0.10 s at $k=5$) and smoothed the motion, but it bought nothing against the inference clock: the shortest committed interval is still $t_{\mathrm{inf}}=0.10\,\mathrm{s}$ of motion, now spelled as 5 actions instead of 2.
> 3. Blanks: `return g_after if obs < njump2 else g_before` and `src[n] >= e`. Running it: $k=2$ gives 36.22 cm, 9 reversals, lags $0.10/0.10\,\mathrm{s}$; $k=3$ gives 28.78 cm, 0, $0.20/0.10$; $k=5$ gives 20.60 cm, 0, $0.25/0.25$; $k=10$ gives 14.10 cm, 0, $0.50/0.50$; $k=20$ gives 13.90 cm, 0, $1.00/1.00$. The changes are $1.00\,\mathrm{s}$ apart, so $k=20$'s reaction arrives exactly as the next change happens — it never acts on a target that is still there — and the largest $k$ that still reacts in time is **10**. Two things are worth saying about the last two rows. Travel has saturated: 14.10 against 13.90 cm is a 1.4% gain for twice the blindness, and the ideal is 14 cm, so $k=10$ is already spending essentially nothing on re-deciding. And the smoothness column stopped paying at $k=3$. Past that point a longer chunk is buying a quantity the robot has already bought, with latency it cannot get back.


### Sources

The notes linked from §1–§7 carry each paper's own citation. The numbers of §6 and §7 that come from a paper body rather than a note are from:

- Black, K. et al. "π0: A Vision-Language-Action Flow Model for General Robot Control." arXiv:2410.24164, 2024 — the two sets of weights, the cached observation and ten flow steps (appendix Table I: $14$, $32$ and $27\,\mathrm{ms}$, $73\,\mathrm{ms}$ on board), and the 18-dimensional zero-padded action.
- Open X-Embodiment Collaboration. "Open X-Embodiment: Robotic Learning Datasets and RT-X Models." *ICRA*, 2024, pp. 6892–6903 — the coarse 7-D alignment, and Table I's large-data comparison.
- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C. & Levine, S. "Robotic Control via Embodied Chain-of-Thought Reasoning." *CoRL*, 2024 — the reasoning steps, the $28$-point gain, $7$ against $350$ tokens per step, and the five-step hold (Table 2).
- Liang, W., Yu, L., Luo, L., Iyer, S. et al. "Mixture-of-Transformers: A Sparse and Scalable Architecture for Multi-Modal Foundation Models." arXiv:2411.04996, 2024 — per-modality weights under global self-attention, and $55.8\%$ of the FLOPs in the 7B text-and-image setting.
- Di Palo, N. & Johns, E. "Keypoint Action Tokens Enable In-Context Imitation Learning in Robotics." arXiv:2403.19578, 2024; Fu, L. et al. "In-Context Imitation Learning via Next-Token Prediction." arXiv:2408.15980, 2024 — the two research steps before physical prompting.
- Generalist AI. "GEN-1.5: Embodied Foundation Models are One-Shot Learners" (2026-08-19) and "GEN-0" (2025-11-04), company posts — physical prompting, $59$ and $83\%$, the 270,000 hours.
- Dyna Robotics. "Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models" (August 2026), company report — the power laws, the fine-tuning budgets and the $87$ against $46\%$.
- Gemini Robotics Team. "Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer." arXiv:2510.03342, 2025 — Motion Transfer and thinking before acting.

## 한국어

*[[03-deep-learning/vlm/index|3. VLM]]의 인코더와 [[04-robotics/robot-systems-deployment|10. Robot Systems]]의 주기 예산 위에 선다. 대상 **D4**를 처음 쓴다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 학습과 적응 층의 꼭대기, 곧 지시와 이미지를 움직임으로 바꾸는 정책이다. "*저 패널을 프레임에 설치해*"에서는 학습된 정책이 맡을 때의 셋째 단계 *작업 분해*와 일곱째 단계 *끼움 수행*을 받친다([[physical-ai-map|피지컬 AI 지도]]의 학습과 적응 띠에 이 페이지의 자리가 있다). 이것 없이는 학습된 정책의 주장을 확인할 수 없다. 이 트랙이 고정해 둔 행동 청크 D4([[03-deep-learning/lab-objects|0. Lab Objects]])는 $k=3$에서 최대 $0.20\,\mathrm{s}$ 묵은 장면에 따라 움직이고 변화에 $0.20\,\mathrm{s}$ 늦게, $k=20$이면 $1.00\,\mathrm{s}$ 늦게 반응한다(계산 절). 제곱 오차는 장애물 양쪽으로 지나간 두 시연을 $(0,0)$, 곧 장애물 한가운데로 보낸다(§2). 같은 정규화 청크가 둘째 팔을 $6$ cm와 $3$ cm 더 멀리 보낸다(§7). 그리고 시행 열 번의 $80\%$ 대 $60\%$는 아무 순위도 정하지 못한다(§4). 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 4를 닫는 페이지로 딥러닝 회차 39–44이고, 행동 복제와 복합 오차를 다루는 [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL]] §1, 그리고 복제된 정책 근처에 KL 항으로 붙들어 두는 파인튜닝을 다루는 §4와 함께 읽는다. [[05-construction-robotics/imitating-contact|10. 접촉 모방]]의 §2, §4, §6은 이 페이지의 행동 복제, 두 시연자의 평균, 행동의 선택을 S1(건설 트랙의 20 kg 외장 패널 과제, [[05-construction-robotics/site-engineering|2.5]])의 안착으로 가져간다. 이 페이지를 마치면 어떤 VLA든 한 줄로 — 관측, 행동 공간, 프레임, 주기, 지평 $H$, 실행 stride $k$, 헤드, 증거 — 명세하고, 그 영상을 믿기 전에 묵은 정도, 반응 지연, 헤드 비용을 계산할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 여섯 번쯤이고, [[03-deep-learning/index|딥러닝 학습 일정]]의 39–44행이다. 앞의 두 회차가 첫 읽기다. **첫 회차:** 대상, 그림, 그리고 풀이를 가린 채 손으로 하는 계산 절. $m=2$, $k=3$의 최악 나이 $0.20\,\mathrm{s}$, 그리고 $k=20$의 $1.00\,\mathrm{s}$에 대한 $\ell=0.20\,\mathrm{s}$다. **둘째 회차:** §2 옆에 [[02-foundations/rl-robot-learning|7.5 §1]]을 펴 두고 §1–§3을 읽은 뒤, 스스로 점검 1, 2, 4, 5와 과제 1–2를 푼다. **셋째 회차:** §4와 §5 실습, 스스로 점검 3, 과제 3. **넷째–여섯째 회차:** §6, §7, §8을 한 회차에 하나씩, 스스로 점검 7, 6, 8과 함께. 접힌 *더 깊이* 메모는 두 번째 읽기로 미룬다. 마지막으로 실제 VLA 논문 하나 — [[01-canonical-papers/notes/4-vla/pi0|π0]]나 [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]] — 로 읽고 나면 줄을 채우고, 찾지 못한 숫자가 무엇인지 말한다.

### 이 페이지의 대상 · Running object

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D4**를 그 페이지가 고정한 숫자 그대로 쓴다. 시간 $t$에 **D4**는 관측 $o_t$ — 실제 로봇에서는 image feature이고, D4에서는 아래 표의 숫자 네 개짜리 토큰으로 줄였다 — 와 "왼쪽으로 간 다음 아래로"라는 instruction $l$을 받고, 2차원 말단 delta 행동 세 개의 chunk를 예측한다. 로봇은 그 가운데 처음 $k$개만 실행하고 다시 관측한다. architecture보다 먼저 $\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l)$와 $a_i=(\Delta x_i,\Delta y_i)$라는 interface를 쓴다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $o$ | $(p_x,p_y,g_x,g_y)$ | 관측 토큰: 도구 위치와 instruction이 가리키는 목표, 단위는 미터 |
| $p_0$ | $(0,0)\,\mathrm{m}$ | 카탈로그 자세의 도구 위치 |
| $g$ | $(-0.04,-0.02)\,\mathrm{m}$ | 장면이 바뀌기 전 목표 |
| $a_{1:3}$ | $(-0.02,0)$, $(-0.02,0)$, $(0,-0.02)$ | 고정된 chunk, 단위는 미터 |
| $a_{\max}$ | $0.02\,\mathrm{m}$ | 한 제어 스텝에서 interface가 받는 최대 delta |
| $\delta$ | $0.005\,\mathrm{m}$ | 정책의 축 전환 폭: $x$를 $\delta$ 안으로 맞춘 뒤 $y$ |
| $\Delta t$ | $0.05\,\mathrm{s}$ | 제어기 주기, 20 Hz |
| $t_{\mathrm{inf}}$ | $0.10\,\mathrm{s}$ | 정책 순전파 1회 |
| $\sigma$ | $0.002\,\mathrm{m}$ | 관측 토큰의 축별 지각 흔들림 |

여기서 instruction은 장식이 아니다. "왼쪽으로 간 다음 아래로"가 정책이 계획하는 축 순서 자체이고, 그래서 고정된 chunk가 $x$로 두 번, $y$로 한 번 움직인다. $t_{\mathrm{inf}}$의 $100\,\mathrm{ms}$는 모델*과* 그것이 도는 컴퓨터가 함께 정한다. 로봇 자신의 GPU에서 그 시간이 어디로 가는지 — 가중치당 바이트, 커널 실행, 숫자 형식 — 는 [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산 §8]]과 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §11]]이 다루고, 둘 다 정책이 로봇 위에서 돌기 전까지는 학위논문 경로 밖이다.

*범위: 이 페이지는 언어 조건 정책과 로봇 사이의 interface를 가르친다 — 행동 표현, behaviour cloning 목적함수, chunk를 얼마나 오래 확정해도 되는지, 어떤 헤드가 그것을 어떤 비용으로 만드는지, 보고된 success rate가 무엇을 증명하고 무엇을 증명하지 않는지, 정책 하나가 여러 몸을 몰 때 무엇이 달라지는지, 프롬프트에서 과제를 배운다는 것이 무엇인지. $o_t$를 만드는 vision–language 인코더는 가르치지 않는다. 그것은 [[03-deep-learning/vlm/index|3. VLM]]이다. 사전학습된 backbone을 새 로봇에 맞게 전체로든 LoRA로든 파인튜닝하는 법도 아니다. 그것은 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §8]]이다. 다봉 시연을 행동 분포로 바꾸는 생성 head도 아니다. 그것은 [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]다. delta를 토크로 바꾸는 제어기도 아니다. 그것은 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]다. 시연이 어디서 오는지도 아니다. 그것은 [[04-robotics/teleoperation-demonstration|12. 원격조작]]이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 402" style="max-width:100%;height:auto" role="img" aria-label="정책 변에 t_inf = 100 ms, 제어기 변에 50 ms, 행동 세 개짜리 chunk 버퍼와 스텝 n − 2의 관측을 적은 D4의 폐루프와, 그 루프를 제어 스텝으로 펼쳐 관측 스텝, 실행되는 행동의 나이, 스텝 20의 장면 변화에 대한 0.20 s 반응을 보인 시간선">
  <defs><marker id="aD4k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) 루프 하나, 시계 둘</text>
  <rect x="12" y="44" width="106" height="42" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="65" y="61.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">장면</text>
  <text x="65" y="76.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">l: 왼쪽, 그다음 아래</text>
  <rect x="240" y="47" width="84" height="36" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="282" y="69" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">정책 π<tspan dy="3" font-size="10">θ</tspan></text>
  <line x1="118" y1="65" x2="238" y2="65" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4k)"/>
  <text x="179" y="45" font-size="11" fill="currentColor" text-anchor="middle">o는 스텝 n − m의 관측</text>
  <text x="179" y="59" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">m = 2 스텝</text>
  <line x1="324" y1="65" x2="423" y2="65" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4k)"/>
  <text x="376" y="59" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">t<tspan dy="3" font-size="10">inf</tspan><tspan dy="-3" dx="3.5">= 100 ms</tspan></text>
  <text x="488" y="37" font-size="11" fill="currentColor" text-anchor="middle">chunk 버퍼 · k = 3</text>
  <rect x="428" y="46" width="120" height="17" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="434" y="59" font-size="11" fill="currentColor">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="542" y="59" font-size="11" fill="currentColor" text-anchor="end">(−0.02, 0)</text>
  <rect x="428" y="63" width="120" height="17" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="434" y="76" font-size="11" fill="currentColor">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="542" y="76" font-size="11" fill="currentColor" text-anchor="end">(−0.02, 0)</text>
  <rect x="428" y="80" width="120" height="17" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="434" y="93" font-size="11" fill="currentColor">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="542" y="93" font-size="11" fill="currentColor" text-anchor="end">(0, −0.02)</text>
  <rect x="425" y="43" width="126" height="57" rx="3" stroke="currentColor" stroke-width="2" fill="none"/>
  <rect x="428" y="146" width="120" height="40" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="488" y="162.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">제어기</text>
  <text x="488" y="177.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">20 Hz</text>
  <line x1="488" y1="100" x2="488" y2="144" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4k)"/>
  <rect x="240" y="146" width="84" height="40" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="282" y="162.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">로봇</text>
  <text x="282" y="177.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">p ← p + a</text>
  <line x1="428" y1="166" x2="326" y2="166" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD4k)"/>
  <text x="376" y="160" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">Δt = 50 ms</text>
  <path d="M240 166 L64 166 L64 88" stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aD4k)" stroke-linejoin="round"/>
  <text x="74" y="160" font-size="11" fill="currentColor" fill-opacity="0.8">세계가 바뀐다</text>
  <path d="M425 86.5 L396 86.5 L396 116 L178 116 L178 68" stroke="currentColor" stroke-width="1.3" fill="none" stroke-dasharray="5 3" marker-end="url(#aD4k)" stroke-linejoin="round"/>
  <text x="287" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.9">비었을 때만 다시 채움: k = 3 스텝마다</text>
  <text x="12" y="220" font-size="12" fill="currentColor">(b) k = 3으로 펼친 루프</text>
  <text x="100" y="266" font-size="11" fill="currentColor" text-anchor="end">관측</text>
  <text x="100" y="292" font-size="11" fill="currentColor" text-anchor="end">실행</text>
  <text x="100" y="318" font-size="11" fill="currentColor" text-anchor="end">나이 (스텝)</text>
  <text x="100" y="340" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">제어 스텝 n</text>
  <rect x="108" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="126" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="126" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="126" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">16</text>
  <rect x="144" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="162" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="162" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="162" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">17</text>
  <rect x="180" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="198" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="198" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="198" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">18</text>
  <rect x="216" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="234" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="234" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="234" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">19</text>
  <rect x="252" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="270" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="270" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="270" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">20</text>
  <rect x="288" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="306" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="306" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="306" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">21</text>
  <rect x="324" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="342" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="342" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="342" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">22</text>
  <rect x="360" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="378" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="378" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="378" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">23</text>
  <rect x="396" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="414" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="414" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="414" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">24</text>
  <rect x="432" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="450" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">2</tspan></text>
  <text x="450" y="318" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="450" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">25</text>
  <rect x="468" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.22" stroke-opacity="0.6"/>
  <text x="486" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">3</tspan></text>
  <text x="486" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">4</text>
  <text x="486" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">26</text>
  <rect x="504" y="278" width="36" height="20" stroke="currentColor" stroke-width="0.8" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.6"/>
  <text x="522" y="292" font-size="11" fill="currentColor" text-anchor="middle">a<tspan dy="3" font-size="10">1</tspan></text>
  <text x="522" y="318" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="522" y="340" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">27</text>
  <line x1="180" y1="275" x2="180" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <line x1="288" y1="275" x2="288" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <line x1="396" y1="275" x2="396" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <line x1="504" y1="275" x2="504" y2="301" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="108" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 108.0 274 Q 144.0 248 179.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4k)"/>
  <circle cx="216" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 216.0 274 Q 252.0 248 287.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4k)"/>
  <circle cx="324" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 324.0 274 Q 360.0 248 395.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4k)"/>
  <circle cx="432" cy="277" r="3.2" stroke="none" fill="currentColor"/>
  <path d="M 432.0 274 Q 468.0 248 503.0 273" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aD4k)"/>
  <line x1="252" y1="238" x2="252" y2="328" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 3"/>
  <text x="247" y="246" font-size="11" fill="currentColor" text-anchor="end">장면 변화, n<tspan dy="3" font-size="10">j</tspan><tspan dy="-3" dx="3.5">= 20</tspan></text>
  <path d="M252 351 L252 356 L396 356 L396 351" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/>
  <text x="324" y="372" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">ℓ(3) = (24 − 20) × 0.05 s = 0.20 s</text>
  <text x="12" y="388" font-size="11" fill="currentColor" fill-opacity="0.85">최악의 나이 (m + k − 1)Δt = 0.20 s · 호 하나가 t<tspan dy="3" font-size="10">inf</tspan><tspan dy="-3" dx="3.5">= m = 2 스텝</tspan></text>
</svg>

카탈로그 숫자로 그린 D4의 폐루프이고, 시계가 둘이다. 정책 변은 $t_{\mathrm{inf}}=100\,\mathrm{ms}$, 곧 제어 스텝 $m=2$개를 쓰고 제어기 변은 $\Delta t=50\,\mathrm{ms}$이며, chunk 버퍼는 행동 $k=3$개 — $(-0.02,0)$, $(-0.02,0)$, $(0,-0.02)$ — 를 담고 비었을 때만 스텝 $n-m$의 관측으로 다시 채워진다. 아래에 $k=3$으로 펼친 루프에서 실행되는 행동은 모두 2–4 스텝 묵었으므로 최악의 나이는 $(m+k-1)\Delta t=0.20\,\mathrm{s}$이고, 스텝 20의 장면 변화는 스텝 24에야 행동에 닿아 $\ell(3)=(24-20)\times0.05\,\mathrm{s}=0.20\,\mathrm{s}$ 늦는다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. 과제는 이 그림을 그리고, 지연을 유도하고, 손잡이 하나를 쓸어 보라고 한다. 카탈로그 숫자로 여기서 먼저 하면 과제는 손잡이를 바꾸는 일이지 첫 유도가 아니다.

**chunk 자체.** 정책은 상상 속 도구를 관측된 위치에서 관측된 목표까지 한 번에 한 축씩, 한 스텝에 $a_{\max}$를 넘지 않게 걷게 한다. $p_0=(0,0)$에서 $g=(-0.04,-0.02)$로 가면 $r_1=(-0.04,-0.02)$, $|r_{1x}|=0.04>\delta$이므로 $a_1=(-0.02,0)$이다. 다음 $r_2=(-0.02,-0.02)$도 $|r_{2x}|=0.02>\delta$이므로 $a_2=(-0.02,0)$, 그다음 $r_3=(0,-0.02)$는 $|r_{3x}|=0<\delta$라 축을 바꿔 $a_3=(0,-0.02)$다. 이것이 카탈로그 chunk다. 경로 길이는 $3\times0.02=0.06\,\mathrm{m}$인데 알짜 변위는 $\sqrt{0.04^2+0.02^2}=0.0447\,\mathrm{m}$뿐이므로, instruction의 축 순서가 직선보다 $34\%$ 더 걷게 만든다. 표현 선택이 미터 단위 비용을 갖는다는 §1이 숫자 하나로 여기 있다.

**타이밍, chunk 길이가 나오는 자리.** 추론에 $t_{\mathrm{inf}}$가 들고 제어기는 $\Delta t$마다 행동을 하나씩 쓰므로, 행동 $k$개의 chunk는 $k\Delta t$ 동안 버티고 다음 chunk는 $k\Delta t\ge t_{\mathrm{inf}}$일 때만 제때 준비된다. 즉 $k\ge\lceil t_{\mathrm{inf}}/\Delta t\rceil=\lceil 0.10/0.05\rceil=2=m$이다. 행동이 떨어진 제어기는 멈추거나 붙들고 있어야 하기 때문이다. **실행되는 행동의 나이.** 스텝 $[jk,(j+1)k)$를 덮는 chunk는 스텝 $jk-m$의 장면에서 계산됐으므로 스텝 $n$에 나가는 행동은 $m+(n\bmod k)$ 스텝 묵었고, 최악은 $(m+k-1)\Delta t$다. 카탈로그 $k=3$이면 $(2+3-1)\times0.05=0.20\,\mathrm{s}$다.

**반응 지연.** 장면이 제어 스텝 $n_j$에서 바뀌면 그것을 알 수 있는 첫 행동은 관측 스텝이 $n_j$ 이상인 첫 chunk, 즉 $jk\ge n_j+m$인 첫 경계에 속한다. 그래서 $\ell(k)=(k\lceil(n_j+m)/k\rceil-n_j)\Delta t$다. $n_j=20$, $k=3$이면 $\lceil22/3\rceil=8$이라 경계는 스텝 24, $\ell=0.20\,\mathrm{s}$다. $k=20$이면 $\lceil22/20\rceil=2$, 경계는 스텝 40, $\ell=1.00\,\mathrm{s}$다. §5는 루프를 돌려 이 숫자를 흔적에서 다시 얻는다. 대수와 코드가 맞는지 확인하는 것이 그 검사다.

**같은 대상 위의 목적함수.** D4의 한 상태에서 똑같이 좋은 시연 둘이 정규화 단위로 $a=(-1,0)$과 $(1,0)$이면 MSE-optimal 결정 예측은 평균 $(0,0)$이고, 시연의 어느 봉우리(mode)도 아니다. 시연이 $(-1,0)$, $(-1,0)$, $(1,0)$이면 $(-1/3,0)$이다. 더 잦은 봉우리 쪽으로 기울었을 뿐 여전히 시연된 행동이 아니다. 이것이 §2이고, 출력 분포가 세부가 아니라 설계 선택인 이유다.

### 1. 행동 표현도 방법이다

관절 위치·속도·torque, 말단 pose·delta pose, gripper, action token은 물리 가정이 다르다. 단위·frame·rate·horizon·하위 controller가 없으면 "행동 출력"은 불완전하다.

표현마다 아래 층에 넘기는 일이 다르다. 관절 위치는 위치 서보가 추종하므로 정책은 torque를 만지지 않지만 관절 한계는 지켜야 한다. 관절 속도는 그 서보가 적분하므로 작은 편향이 위치 오차로 쌓여 간다. torque는 서보를 건너뛰어, 팔의 동역학을 제어기 자신의 주기로 정책이 책임지게 만든다. 말단 pose는 해가 여럿이고 특이점이 있는 역기구학을 아래쪽 풀이기에 맡긴다. delta pose는 변화량이므로 어느 frame에서 쓰였는지, 어느 주기에 걸친 것인지 없이는 아무 뜻이 없다. gripper 상태는 보통 자기 일정으로 움직이는 숫자 하나다. 그리고 token은 구간 번호이므로 해상도가 구간 폭이고, §6이 D4에서 그 값을 매긴다.

D4가 $(0.02,0)$을 미터로 세 번 예측했는데 하위 interface가 센티미터로 해석하면, 의도한 6 cm가 0.06 cm가 된다. frame과 rate도 같은 식으로 깨진다. D4의 변화량은 base frame에서 쓴 것이다. 이것을 tool frame에서 변화량을 읽는 interface에 보내고 도구가 작업 평면 안에서 $90^\circ$ 돌아가 있으면, 변화량마다 가는 길에 회전되어 팔은 $(0,-0.02)$, $(0,-0.02)$, $(0.02,0)$을 실행하고 $(0.02,-0.04)\,\mathrm{m}$에서 멈춘다. 목표에서 $0.0632\,\mathrm{m}$ 떨어진 곳으로, 출발점의 $0.0447\,\mathrm{m}$보다 더 멀다. 하나의 운동이 두 frame에서 두 가지로 기술되는 방식은 [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §4]]에 있다. 또 변화량 하나는 $\Delta t=0.05\,\mathrm{s}$당 $0.02\,\mathrm{m}$, 곧 도구 속도 $0.4\,\mathrm{m/s}$를 뜻한다. 같은 chunk를 $50\,\mathrm{Hz}$ interface에서 재생하면 도구는 맞는 경로를 $1.0\,\mathrm{m/s}$로, 두 배 반 빠르게, $0.15\,\mathrm{s}$가 아니라 $0.06\,\mathrm{s}$에 지나간다. 관측에도 시각이 붙는다. 이 페이지의 나이 계산은 모두 그 타임스탬프가 맞다고 가정하고, $10\,\mathrm{ms}$ 틀린 타임스탬프는 도구가 D4의 $0.4\,\mathrm{m/s}$로 움직이는 동안 관측된 도구 위치를 $4\,\mathrm{mm}$, 곧 축 전환 폭 $\delta=5\,\mathrm{mm}$의 대부분만큼 어긋나게 한다([[04-robotics/perception-sensors-rigs|3.6 인식 센서 §9]]; 두 컴퓨터 사이라면 [[02-foundations/tools/computer-networks|12.5 §10]]). 표현 오차는 물리 오차다. 여러 로봇의 데이터를 모으면 같은 종류의 오차가 체계적이 되고, §7이 그것을 잰다.

canonical 목록의 정책 넷은 저마다 다른 선택을 했고, 그래서 이 행들을 맞추기 전에는 성공률을 나란히 놓을 수 없다. [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]은 $256$구간짜리 토큰 $11$개 — 팔 일곱, 이동 베이스 셋, 모드 전환 하나 — 를 $3\,\mathrm{Hz}$로 낸다. [[01-canonical-papers/notes/4-vla/act|ACT]]는 $50\,\mathrm{Hz}$ leader–follower 장비의 다음 관절 공간 행동 $100$개를 낸다. [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]는 위치 제어기에 줄 위치를 낸다. 그리고 [[01-canonical-papers/notes/4-vla/pi0|π0]]는 $18$차원으로 0을 채운 연속 관절 명령을 $50\,\mathrm{Hz}$로 낸다(§7).

### 2. Behavior cloning과 다봉성

시연 파일은 관측마다 사람이 한 행동을 주고, 가장 단순한 정책은 그 행동들에 회귀로 맞춘다. 문제는 두 사람이 서로 다르지만 똑같이 좋은 일을 했을 때 회귀가 돌려주는 것이다. 제곱 오차는 둘의 평균을 돌려주고, 좋은 경로 둘의 평균은 나쁜 경로일 수 있다.

$L_{BC}=H^{-1}\sum_h\|a_{t+h}-\hat a_{t+h}\|^2$. 장애물의 좌우로 지나가는 시연을 평균하면 장애물 중앙으로 갈 수 있다. D4의 한 상태에서 시연이 $(-1,0)$과 $(1,0)$이면 MSE-optimal 결정 행동은 평균 $(0,0)$이다. 시연의 어느 봉우리도 아니고, 장애물이 국소 행동 원점에 있으면 충돌한다. token·mixture·diffusion·flow는 출력 분포의 대안이지, 나쁜 시연과 recovery 문제를 없애지 않는다. 그림은 D4 위의 평균 내기를, 그리고 §6에 앞서 행동 헤드마다 대신 무엇을 돌려주는지 그린다. 토큰 헤드는 행동 숫자 하나하나를 정해진 구간 가운데 하나로 분류하고, 노이즈 제거기는 무작위 노이즈를 청크 전체로 다듬으며, ACT의 CVAE는 관측 옆에 잠재변수 $z$도 받는 회귀다.

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="D4의 한 상태에서 정규화한 시연 행동 (−1, 0)과 (1, 0)을 제곱 오차로 적합하면 원점의 장애물 한가운데 (0, 0)이 되고, 2 : 1 기록이면 (−1/3, 0)으로 어느 시연도 아니다. 아래는 토큰 헤드, 노이즈 제거기, z = 0의 CVAE가 같은 1 : 1 기록에서 각각 무엇을 내놓는지 보인다">
  <defs><marker id="aBck" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) D4의 한 상태에서 제곱 오차가 돌려주는 것</text>
  <rect x="346.0" y="40" width="36.0" height="92" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <text x="364.0" y="37" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">장애물</text>
  <text x="184" y="74" font-size="11" fill="currentColor" text-anchor="end">시연 둘, 1 : 1</text>
  <circle cx="244.0" cy="70" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="484.0" cy="70" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="244.0" y="60" font-size="10" fill="currentColor" text-anchor="middle">시연 (−1, 0)</text>
  <text x="484.0" y="60" font-size="10" fill="currentColor" text-anchor="middle">시연 (1, 0)</text>
  <path d="M 359.0 65 L 369.0 75 M 359.0 75 L 369.0 65" stroke="currentColor" stroke-width="2.0"/>
  <text x="372.0" y="86" font-size="11" fill="currentColor" font-weight="bold">적합 (0, 0)</text>
  <text x="184" y="116" font-size="11" fill="currentColor" text-anchor="end">시연 셋, 2 : 1</text>
  <circle cx="244.0" cy="112" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="244.0" cy="105" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="484.0" cy="112" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M 319.0 107 L 329.0 117 M 319.0 117 L 329.0 107" stroke="currentColor" stroke-width="2.0"/>
  <text x="304.0" y="131" font-size="11" fill="currentColor"><tspan font-weight="bold">적합 (−1/3, 0)</tspan>: 어느 시연자의 행동도 아니다</text>
  <line x1="196.0" y1="146" x2="532.0" y2="146" stroke="currentColor" stroke-width="0.9"/>
  <line x1="244.0" y1="146" x2="244.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="244.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">−1</text>
  <line x1="324.0" y1="146" x2="324.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="324.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">−1/3</text>
  <line x1="364.0" y1="146" x2="364.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="364.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="484.0" y1="146" x2="484.0" y2="150" stroke="currentColor" stroke-width="0.9"/>
  <text x="484.0" y="161" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <text x="184" y="150" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.8">정규화한 Δx (Δy = 0)</text>
  <text x="12" y="192" font-size="12" fill="currentColor">(b) §6의 세 헤드가 1 : 1 기록에서 돌려주는 것</text>
  <line x1="364.0" y1="202" x2="364.0" y2="344" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <text x="184" y="226" font-size="11" fill="currentColor" text-anchor="end">토큰 헤드</text>
  <rect x="236.0" y="208.0" width="16" height="22.0" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="0.9"/>
  <rect x="476.0" y="208.0" width="16" height="22.0" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="0.9"/>
  <text x="244.0" y="204.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="484.0" y="204.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="196" y="244" font-size="10.5" fill="currentColor">표본이나 arg max: 봉우리 하나 · 분포의 평균: 다시 (0, 0)</text>
  <text x="184" y="276" font-size="11" fill="currentColor" text-anchor="end">노이즈 제거기</text>
  <circle cx="244.0" cy="264" r="3.4" fill="currentColor"/>
  <circle cx="244.0" cy="272" r="3.4" fill="currentColor"/>
  <circle cx="484.0" cy="268" r="3.4" fill="currentColor"/>
  <text x="196" y="294" font-size="10.5" fill="currentColor">표본 하나하나가 봉우리 하나에 떨어진다</text>
  <text x="184" y="324" font-size="11" fill="currentColor" text-anchor="end">CVAE, z = 0 (ACT)</text>
  <rect x="240.0" y="316" width="8" height="8" fill="currentColor"/>
  <text x="244.0" y="310" font-size="10" fill="currentColor" text-anchor="middle">청크 t</text>
  <rect x="480.0" y="316" width="8" height="8" fill="currentColor"/>
  <text x="484.0" y="310" font-size="10" fill="currentColor" text-anchor="middle">청크 t+1</text>
  <line x1="252.0" y1="320" x2="354.0" y2="320" stroke="currentColor" stroke-width="1.1" marker-end="url(#aBck)"/>
  <line x1="476.0" y1="320" x2="374.0" y2="320" stroke="currentColor" stroke-width="1.1" marker-end="url(#aBck)"/>
  <path d="M 359.5 315.5 L 368.5 324.5 M 359.5 324.5 L 368.5 315.5" stroke="currentColor" stroke-width="1.8"/>
  <text x="364.0" y="310" font-size="10" fill="currentColor" text-anchor="middle">앙상블</text>
  <text x="196" y="342" font-size="10.5" fill="currentColor">봉우리를 고르는 잠재변수가 없다 · 어긋난 청크를 평균하면 그 사이로</text>
  <line x1="196.0" y1="356" x2="532.0" y2="356" stroke="currentColor" stroke-width="0.9"/>
  <line x1="244.0" y1="356" x2="244.0" y2="360" stroke="currentColor" stroke-width="0.9"/>
  <text x="244.0" y="371" font-size="10" fill="currentColor" text-anchor="middle">−1</text>
  <line x1="364.0" y1="356" x2="364.0" y2="360" stroke="currentColor" stroke-width="0.9"/>
  <text x="364.0" y="371" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="484.0" y1="356" x2="484.0" y2="360" stroke="currentColor" stroke-width="0.9"/>
  <text x="484.0" y="371" font-size="10" fill="currentColor" text-anchor="middle">1</text>
</svg>

D4의 한 상태에서 정규화 단위로, 제곱 오차는 두 시연 $(-1,0)$과 $(1,0)$을 평균 $(0,0)$, 곧 원점의 장애물 안으로 적합하고, $2:1$ 기록은 어느 시연자도 하지 않은 행동 $(-1/3,0)$으로 적합한다. 아래는 §6의 세 헤드가 $1:1$ 기록에서 돌려주는 것이다. 토큰 헤드는 두 봉우리에 $0.5$씩 두고 표본을 뽑거나 arg max를 취할 때만 하나를 돌려주고, 노이즈 제거기의 표본은 하나하나가 봉우리 하나에 떨어지며, $z=0$에서 디코딩하고 겹치는 청크를 평균하는 ACT의 CVAE는 그 사이에 떨어질 수 있다.

그 평균 논증에서 일하는 단어는 목적함수의 이름이고, 그 이름에는 논문들이 하나씩 떨어뜨리는 조건 셋이 있다.

> **Behaviour cloning의 정의.** **Behaviour cloning**은 *학습 목적함수*다. 관측이 주어졌을 때 시연자의 행동을 지도 회귀 또는 분류로 맞추는 것이지 architecture도, 정책 계열도, imitation learning 일반도 아니다. 정의 조건 셋. 자료는 **시연자가 만든 (관측, 행동) 쌍**이므로 label이 return이 아니라 행동이다. 손실은 **행동에만 걸리는 지도 오차**이고, 학습 중에 reward도 환경 상호작용도 없다. 그리고 기대값은 **시연자의 상태 분포**에서 취한다. 학습된 정책의 분포가 아니다. 이 조건이 평범한 회귀가 아니라 분포 이동 문제로 만든다.
>
> $$\theta^\star=\arg\min_\theta\ \mathbb E_{(o,a)\sim\mathcal D_{\text{demo}}}\big[c\big(a,\pi_\theta(o)\big)\big]$$
>
> $\mathcal D_{\text{demo}}$는 시연 집합, $c$는 행동당 비용(연속 행동이면 제곱오차, token이면 cross-entropy다. 7.5 §1은 같은 모방 손실을 $\ell$로 쓰지만, 이 페이지에서 $\ell$은 반응 지연이라 $c$로 쓴다), $\pi_\theta$는 정책이다. 기대값의 아래첨자가 난점 전부인데, 배포 시 상태는 $\pi_\theta$ 자신이 방문해 뽑히고 이 목적함수는 그 상태를 한 번도 본 적이 없기 때문이다. 그 어긋남이 **공변량 이동**(covariate shift)이고, 그 대가가 **복합 오차**(compounding error)다. 작은 실수 하나가 로봇을 어느 시연도 가 보지 않은 상태로 옮기고 거기서는 다음 실수가 더 잦아지므로, $T$스텝 과제에서 순수 행동 복제의 기대 비용은 스텝당 오류율 $\epsilon$에 대해 $O(\epsilon T^2)$로 자랄 수 있고 DAgger는 $O(\epsilon T)$다. [[02-foundations/rl-robot-learning|7.5 §1]]의 두 상한이고, 그 절은 행동 복제를 최대우도로도 적는다. 제곱오차는 그 가우시안 경우다.
>
> - **예**: D4의 delta 세 개를 카탈로그 chunk에 제곱오차로 맞추기. 손실이 기록된 자료만으로 계산되고, 그래서 원격조작 데이터셋으로 규모를 키울 수 있다.
> - **비예**: DAgger를 비롯해 *학습자*가 도달한 상태에서 전문가에게 다시 묻는 모든 방법. 지도 손실은 그대로 두고 셋째 조건을 바꾸므로 — $O(\epsilon T)$ 상한을 사는 것이 이 변경이다 — 조정이 아니라 자료 수집 비용이 다른 별개 알고리즘이다.
> - **비예**: 같은 시연 파일에 offline RL. 바이트는 같지만 reward와 가치 추정을 쓰므로 둘째 조건이 깨지고, 실패 양상도 복합 오차가 아니라 가치함수의 실패다.
> - **왜 중요한가**: 위의 두 봉우리의 평균 $(0,0)$은 적합 실패가 아니라 둘째 조건 아래의 정확한 최소점이다. 그러므로 시연자 상태에서의 낮은 validation loss는 정책이 그 상태 위에 머무를 때만 폐루프 성공을 예측하고, 그 주장을 loss 곡선과 분리하라는 것이 §4의 요구다.

### 3. Chunking의 교환

긴 chunk는 과제에 드는 결정의 수를 줄인다. $T$스텝 과제가 결정 약 $T/k$개가 되고, 이것이 복합 오차에 대한 [[02-foundations/rl-robot-learning|7.5 §1]]의 값싼 처방이다. 결정당 오류가 $1\%$면 단일 스텝 $500$번은 $0.99^{500}=0.7\%$만 깨끗하게 끝나고, 열 개짜리 chunk $50$개는 $0.99^{50}=60.5\%$가 깨끗하게 끝난다(7.5의 $k$는 통째로 실행하는 chunk, 이 페이지 표기로 $H=k$다). chunk는 초당 순전파 수도 줄이고 조화로운 움직임을 지킬 수 있지만, 보정을 늦춘다. 추론이 100 ms이고 로봇이 20 Hz로 행동 10개를 실행하면 전체 open-loop chunk는 0.5초다. 10개를 예측하고 2개만 실행한 뒤 다시 관측하면 feedback을 회복하지만 계산량이 늘어난다. 토큰 정책에서 순전파 한 번이 무엇인지 — 토큰을 하나씩 내는 인과 마스크 디코더와, 매 스텝이 앞부분을 다시 돌리지 않게 하는 KV 캐시 — 는 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer §3과 §7]]에 있다.

계산 절이 그 문장을 $(m+k-1)\Delta t$와 $\ell(k)$ 두 식으로 바꿨고, §5가 반대쪽에서 무엇을 사는지 잰다. 먼저 거래되는 대상부터.

> **Action chunking의 정의.** **Action chunking**은 정책의 *결정 단위* 성질이다. 관측 하나가 로봇에게 미래 행동 몇 개를 확정시키는가이고, 따라서 architecture나 손실이 아니라 interface의 성질이다. 정의 조건 셋. 순전파 한 번이 **미래 시각으로 색인된 행동 $H\ge2$개를 내놓는다**. 단일 행동이 아니다. 그중 **$k\le H$개를 다음 관측을 쓰기 전에 실행하고**, 이 $k$는 논문이 자주 말하지 않는 두 번째 숫자다. 그리고 그 구간 동안 로봇은 **개루프**다. 확정된 행동 사이로 관측이 들어오지 않는다.
>
> $$\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l)\ \longrightarrow\ a_{t:t+k-1}\ \text{실행}\ \longrightarrow\ t+k\text{에 재관측}$$
>
> $H$는 예측 horizon, $k$는 실행 stride, $o_{\le t}$는 예측 시점까지의 관측 전부다. $H$는 신경망이 무엇을 표현하도록 배워야 하는지를 정하고 지연을 정하는 것은 $k$뿐이므로, $H$만 보고하는 것은 신경망을 설명한 것이지 로봇을 설명한 것이 아니다.
>
> - **예**: 20 Hz에서 $H=k=3$인 D4. 관측 하나가 $0.15\,\mathrm{s}$의 움직임을 확정하고, 추론 지연 $m=2$ 스텝까지 더하면 실행되는 가장 오래된 행동은 $0.20\,\mathrm{s}$ 묵었다.
> - **비예**: $H=10$을 예측하고 하나만 실행한 뒤 다시 관측하는 정책. 그것은 다단계 예측 *목적함수*이고, $k=1$은 interface를 단일 스텝 정책과 똑같이 두므로 §5의 $k=1$ 행이 보이듯 chunking의 매끄러움을 하나도 사지 못한다.
> - **비예**: 제어기가 여러 주기에 걸쳐 추종하는 명령 하나, 예를 들어 "이 pose로 가라". 확정은 실재하지만 결정은 하나이므로 horizon이 정책 출력이 아니라 제어기의 보간기에 살고, 위의 산수는 하나도 적용되지 않는다.
> - **왜 중요한가**: $k$는 거래의 양쪽에 동시에 나타나는 유일한 손잡이다. 반응 지연 $\ell(k)$를 늘리고, 초당 독립적인 지각 표본 수를 나눈다. 그래서 매끄러움과 반응성을 따로 조율할 수 없다. §5가 그 문장을 표로 만든 것이다.

### 4. 증거 읽기

VLA 논문은 보통 영상 옆에 성공률 하나를 보고하는데, 둘 다 어느 능력이 나아졌는지도, 그 숫자를 얼마나 믿을 수 있는지도 말하지 않는다. semantic generalization, motor competence, embodiment transfer, recovery를 나눈다. success rate에는 episode·reset·intervention·tolerance·환경 변동 정의가 필요하다. 인상적인 영상은 추정량이 아니라 표본 하나다.

**성공률 하나가 말해 주는 만큼.** 성공률은 셈이고, 셈에는 구간이 따른다. [[02-foundations/ml-practice|9. ML 실무]]의 계산 예제 4번에서 유도한 Wilson 구간이다(더 자세히는 경로의 블록 5인 [[06-research-practice/experimental-design-reproducibility|연구 실무 2, 실험 설계 §4]]). 95%에서 $10$번 가운데 $8$번 성공은 $[0.49,\ 0.94]$, $10$번 가운데 $6$번은 $[0.31,\ 0.83]$이므로, $80\%$ 대 $60\%$를 보여 주는 10회짜리 표는 두 정책의 순위를 정하지 못했다. 각각 $100$번이면 구간 $[0.71,\ 0.87]$과 $[0.50,\ 0.69]$가 더는 겹치지 않고, 처음 갈라지는 것은 정책당 약 $85$번에서다. 실패 없는 연속 성공은 보이는 것보다 덜 증명한다. $n$번 연속 성공은 95%에서 $1-0.05^{1/n}\approx3/n$보다 큰 실패율만 배제하므로, 서른 번 연속 성공도 실패율 $9.5\%$를 허용한다. 모든 백분율 옆에 $n$을, 두 백분율을 견줄 때는 구간을 요구하라. embodiment 전이 주장은 따로 물을 것이 더 있고, §7에 모았다.

**복제 다음: 로봇 자신의 시행에서 배우기.** 이 절이 세는 폐루프 시행은 행동 복제가 한 번도 보지 못하는 데이터, 곧 로봇 자신의 상태이기도 하고, §2의 복합 오차가 일어나는 곳이 거기다. [[02-foundations/rl-robot-learning|7.5 §4]]는 복제된 정책을 그 위에서 RL로 파인튜닝한다. 과제 보상 — 흔히 [[03-deep-learning/vlm/index|3. VLM §4]]의 판정기 같은 이진 성공 판정 — 으로 계속 개선하되, KL 항, 곧 새 정책의 행동 분포가 복제된 정책의 분포에서 얼마나 멀어졌는지에 매기는 벌점이 정책을 시연이 가르친 것 근처에 붙들어 둔다. 그 항의 가중치 $\beta$는 이탈 한 단위가 사야 할 보상의 양을 정하고, $\beta\to\infty$면 복제된 정책이 그대로 돌아온다. 이제 정책은 배우려고 행동하므로, 그 절이 꼽는 정직한 안전 대책 가운데 하나는 정책 뒤에 두어 신경망이 무엇을 내든 모든 명령을 인증된 안전 집합 안으로 투영하는 필터다. 축마다 $\pm a_{\max}$인 D4의 interface 한계가 가장 단순한 그런 집합이다. 더 새로운 레시피는 조작자를 더한다. π\*0.6의 RECAP은 시연, 로봇 자신의 실행, 실행 중 조작자가 한 수정으로 학습하되, 정책을 추정한 어드밴티지 — 그 상태에서 정책의 평균적 선택보다 그 행동이 얼마나 나았는가 — 에 조건화한다([[01-canonical-papers/notes/4-vla/pi0|π0]]). 어느 쪽이든 폐루프 주장이므로 같은 셈을 치러야 한다. 전후의 성공률을 각각 $n$과 구간과 함께, 그리고 그 시행에 든 로봇 시간을.

새로운 범용 정책보다 먼저 [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/act|ACT]], [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]를 그 순서로 읽어라.

### 5. Chunk 길이 쓸기

이 로봇은 어떤 $k$로 돌아야 하는가? 계산 절이 긴 chunk의 비용 — 묵은 정도와 반응 지연 — 을 매겼고, 이 랩은 §3의 교환 반대편에서 긴 chunk가 사는 것을 잰다. 랩은 맨 위의 그림에 손잡이 하나를 붙인 것이다. episode는 20 Hz로 3초이고, 목표는 제어 스텝 20까지 $g=(-0.04,-0.02)$에 있다가 $(-0.04,+0.02)$로 옮겨 간다. 정책은 새 관측을 통해서만 이 변화를 알 수 있다. 지각 흔들림은 난수가 아니라 고정된 sine 쌍이므로 아래 표는 어떤 기계에서도 같다. 코드는 영어 절에 한 번만 싣는다.

재는 것은 둘이다. **이동거리**는 $\sum_n\lVert a_n\rVert$, 도구가 실제로 걸은 경로이고 과제에 필요한 $0.10\,\mathrm{m}$(나갈 때 6 cm, 올라올 때 4 cm)와 견준다. 흔들림 때문에 연속한 계획이 어긋나면 올라간다. **방향 반전**은 $a_n^\top a_{n+1}<0$인 스텝 수로, 조작자가 채터로 느끼는 것이다. 그 반대편에 계산 절의 $\ell(k)$와 옮겨 간 목표의 5 mm 안으로 되돌아오는 시간이 선다.

| $k$ | $k\Delta t$ (s) | 스케줄 가능 | 최악 나이 (s) | 이동거리 (cm) | 반전 | $\ell(k)$ (ms) | 재획득 (s) |
|---:|---:|:--|---:|---:|---:|---:|---:|
| 1 | 0.05 | 아니오 | 0.10 | 31.30 | 6 | 100 | 0.25 |
| 2 | 0.10 | 예 | 0.15 | 30.59 | 10 | 100 | 0.20 |
| 3 | 0.15 | 예 | 0.20 | 19.86 | 0 | 200 | 0.35 |
| 4 | 0.20 | 예 | 0.25 | 13.19 | 0 | 200 | 0.35 |
| 5 | 0.25 | 예 | 0.30 | 14.83 | 0 | 250 | 0.40 |
| 10 | 0.50 | 예 | 0.55 | 10.30 | 0 | 500 | 0.60 |
| 20 | 1.00 | 예 | 1.05 | 9.38 | 0 | 1000 | 1.10 |

읽는 순서는 다섯이다.

**$k=1$ 행은 이 로봇에서 선택지가 아니다.** 순전파마다 행동 하나면 추론 예산이 50 ms여야 하는데 이 정책은 100 ms를 쓰므로 제어기가 굶는다. 그런데도 표에 둔 이유는 "매 스텝 다시 계획하면 되지 않나"라고 할 때 떠올리는 한계가 그것이기 때문이고, 그 한계는 기대하던 것조차 사지 못한다. 반응 지연이 $k=2$와 똑같은 100 ms다. $k<m$에서는 chunk가 아니라 추론 지연이 바닥을 정하기 때문이다.

**채터에는 기울기가 아니라 문턱이 있다.** 반전은 $k=1,2$에서 6과 10이고 $k=3$부터 정확히 0이다. 흔들림은 그대로다. 바뀐 것은 chunk가 셋 이상이면 한 축을 충분히 오래 붙들어 다음 잡음 표본이 움직임 중간에 방향을 뒤집지 못한다는 점이다.

**이동거리는 열 전체에서 3.3배 줄어든다.** 31.30 cm에서 9.38 cm로, 과제가 필요로 하는 10 cm를 상대로. 10 cm보다 조금 적은 것은 정책이 자기가 보는 목표에 축마다 $\delta=5\,\mathrm{mm}$ 안으로 들어서면 멈추기 때문이다. 매 스텝 다시 계획하면 필요한 움직임의 세 배 넘게를 다시 결정하는 데 쓰고, 하드웨어에서 그것은 마모와 발열과 소음인데 offline action MSE에는 하나도 나타나지 않는다.

**지연 열이 대가이고, $k$와 함께 자라지만 비례하지는 않는다.** 스텝 20의 변화에 대해 100, 100, 200, 200, 250, 500, 1000 ms로, 계산 절의 $\ell(k)$와 행마다 일치한다. 코드의 `assert`가 그 검사다. 변화를 다른 스텝으로 옮기면 각 값은 변화가 두 chunk 경계 사이 어디에 떨어지느냐에 따라 $m\Delta t=100\,\mathrm{ms}$와 최악 행동 나이 $(m+k-1)\Delta t$ 사이를 움직이고, 그 위아래 한계는 [[03-deep-learning/index|딥러닝 인덱스]]의 누적 과제 3(c)가 증명한다. $k=3$이면 100에서 200 ms 사이 어디든이다. 1초에 한 번 움직이는 목표는 $k\le5$면 추종되고 $k=20$이면 통째로 놓친다.

**표의 숫자 하나는 추세가 아니다.** $k=5$의 이동거리 14.83 cm가 $k=4$의 13.19 cm보다 크다. 흔들림이 고정된 수열이라 chunk 경계가 그 안 어디에 떨어지는지가 10% 수준에서 영향을 준다. 열 전체의 3.3배가 효과이고 이웃 사이의 12%는 위상이다. 두 번째 종류의 차이를 결과로 보고하는 논문에는 seed를 여러 개 요구해야 한다.

이 로봇의 설계 결론: $k$가 3에서 5 사이 — 확정 구간 0.15–0.25초 — 이면 반전이 전부 사라지고 낭비된 이동의 절반 이상이 사라지며 반응은 250 ms 안에 머문다. $k=20$까지 가면 이동거리를 $5.5\,\mathrm{cm}$ 더 아끼는 대신 0.75초의 눈감음을 치르는데, 장면이 전혀 움직이지 않을 때만 좋은 거래다.

### 6. 두 가지 행동 헤드: 토큰과 노이즈 제거기

*한 문장으로:* 행동 헤드는 정책의 특징을 로봇이 실행할 숫자로 바꾸고, 두 계열은 그 값을 다르게 치른다. 토큰 헤드는 숫자를 하나씩 디코드하고, 노이즈 제거기 — 무작위 노이즈를 청크 전체로 다듬어 가는 신경망 — 는 청크 전체에 정해진 횟수의 패스를 치른다. 그래서 선택은 청크 길이와 제어 예산을 따른다.

*이 절에서 하나만 가져간다면:* 교차점이다. 토큰 헤드는 순차 패스가 $D\times H$번, 노이즈 제거기는 $H$와 무관하게 $N$번 필요하므로, $D=2$, $N=10$인 D4에서는 $H=5$ 아래에서는 토큰이, 위에서는 노이즈 제거가 싸다(아래 **노이즈 제거기** 단락과 표).

§1은 행동 표현도 방법의 일부라고 했다. 그것을 만들어 내는 헤드가 나머지 절반이고, 분야는 두 계열과 하나의 절충으로 정리됐다. 둘 다 §2의 평균 문제에 답하지만, 치르는 값이 다르다.

**이산 토큰.** 행동 차원마다 구간으로 자르고 분류한다. 제어가 다음 토큰 예측이 되므로 사전학습된 언어 모델의 장치 전체가 그대로 옮겨 온다. [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]은 $11$차원에 각 $256$구간을 쓰고, [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]는 같은 $256$구간을 예약된 LM 토큰에 대응시킨다. 양자화가 정확도의 한계인 경우는 드물다. **D4**에서 $256$구간을 $\pm a_{\max}=\pm0.02\,\mathrm{m}$에 펼치면 한 칸이 $0.04/256=0.16\,\mathrm{mm}$로, 이 페이지의 지각 지터 $\sigma=2\,\mathrm{mm}$보다 열세 배쯤 촘촘하다. 대가는 순차성이다. 토큰 하나에 디코드 한 번이므로 $D$차원 행동 $H$개의 청크에는 $D\times H$번의 전방 패스가 든다. D4의 고정 청크는 $2\times3=6$번이다. OpenVLA의 측정에서 자기회귀 토큰 정책의 제어 주기가 $6\,\mathrm{Hz}$ 근처에서 막히는 이유가 이것이다. 압축은 개수를 바꾸지 원리를 바꾸지 않는다. FAST(Pertsch 외, 2025)는 청크 전체를 이산 코사인 변환한 뒤 토큰으로 만들므로, 매끄러운 고주파 청크에는 $D\times H$개보다 훨씬 적은 토큰이 들고, π0-FAST는 학습을 최대 다섯 배 빠르게 하면서 디퓨전 π0와 맞먹었다([[01-canonical-papers/notes/4-vla/pi0|π0]]).

**노이즈 제거기.** 대신 청크 전체를 표본으로 뽑는다. [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]는 관측을 조건으로 행동 $16$개의 청크를 추론 시 약 $10$번의 DDIM식 스텝으로 복원하고 — DDIM은 신경망이 학습한 노이즈 수준 가운데 몇 개만 들르는 결정론적 샘플러다([[03-deep-learning/diffusion/index|6. Diffusion & Flow §1]]) — 앞의 몇 개만 실행한 뒤 다시 계획한다. [[04-robotics/mpc|7. MPC]]의 receding horizon이다. [[01-canonical-papers/notes/4-vla/pi0|π0]]는 확산 대신 flow matching — 정해 둔 경로를 따라 노이즈를 데이터로 옮기는 속도를 예측하도록 신경망을 학습하고, 그것을 몇 스텝 적분하는 것([[03-deep-learning/diffusion/index|6. Diffusion & Flow §3]]) — 을 VLM 백본 위의 별도 행동 전문가에 넣고 $50\,\mathrm{Hz}$ 연속 청크를 보고한다. 비용은 *청크 길이와 무관하게* $N$번의 패스이고, 여기서 교차점이 나온다. $D\times H<N$인 동안은 토큰 헤드가 싸고, 청크가 그보다 길어지면 노이즈 제거기가 싸다. $D=2$, $N=10$인 D4에서 교차점은 $H=5$다. 그 아래면 토큰, 위면 노이즈 제거다.

**열 번의 통과가 예산에 들어가는 이유.** π0는 가중치 두 벌을 가진 transformer 하나다. 이미지와 텍스트 토큰은 $3$B PaliGemma 가중치를, 로봇 상태와 행동 토큰은 자기 몫의 $300$M 가중치를 지나고, 둘은 self-attention에서만 만난다. $N$번의 통과를 감당할 수 있게 하는 것이 이 분할이다. 관측은 한 번 인코딩하고 그 key와 value를 캐시에 두므로, π0의 flow 스텝 열 번은 매번 행동 토큰 위의 작은 expert만 다시 돌린다. RTX 4090에서 열 스텝을 합쳐 $27\,\mathrm{ms}$로, 관측을 한 번 지나는 $32\,\mathrm{ms}$보다 짧고, 로봇 위 전체는 $73\,\mathrm{ms}$다. 아래의 접힌 메모가 이 분할의 이름과, 그것이 mixture of experts와 어떻게 다른지 말한다.

> [!note]- 더 깊이 · Deeper
> **전문가가 아니라 transformer의 혼합.** π0는 이 분할을 원소 둘짜리 mixture of experts라고 부른다. 같은 분할을 텍스트·이미지·음성에 대해 연구한 Liang 외(2024)는 **Mixture of Transformers**(MoT)라고 부른다. 임베딩을 뺀 모든 가중치 — feed-forward 층, attention 투영, layer norm — 를 모달리티마다 따로 두되 attention은 여전히 시퀀스 전체에 걸치고, 그들의 7B 텍스트·이미지 설정에서 밀집 모델과 같은 성능을 학습 FLOPs의 $55.8\%$로 냈다. 보통의 mixture of experts([[03-deep-learning/foundations/attention-transformer|1.2 §9]])와 달리 학습된 게이트가 고르지 않는다. 토큰의 종류가 가중치를 정한다.

**세 번째 답, 그리고 셋의 공통점.** [[01-canonical-papers/notes/4-vla/act|ACT]]는 평범한 회귀를 유지하되 CVAE로 학습한다. CVAE는 [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN §1]]의 잠재변수 모델을 쓰는 변분 오토인코더의 조건부 형태로, 디코더가 관측 옆에 잠재변수 $z$를 받으므로 시연 사이의 변동이 적합을 흐리는 대신 $z$에 담긴다. 실행할 때는 잠재변수를 사전분포의 평균인 0에 고정하고 결정적으로 디코딩하므로(Zhao 외 2023, §IV-B), 로봇 위에서 봉우리를 고르는 잠재변수는 없다. 셋 모두 존재하는 이유는 단봉 헤드 아래의 $L_{\mathrm{BC}}$가 타당한 행동들의 평균을 돌려주기 때문이다. 시연 $(-1,0)$과 $(1,0)$에 대해 그것은 장애물 한가운데인 $(0,0)$이다. 토큰 헤드는 두 봉우리를 *구간 분포 안에* 간직하지만, 행동을 **표본으로 뽑거나 argmax로 고를 때만** 그렇다. 분포를 평균 내면 $(0,0)$이 돌아온다. 노이즈 제거기는 구성상 한 봉우리를 뽑는다. CVAE는 잠재변수를 뽑을 때마다 하나를 뽑을 수 있지만, ACT는 $z=0$에서 청크 하나를 디코딩하고, 시간 앙상블 — 스텝마다 겹치는 청크들이 그 스텝에 대해 예측한 행동의 가중평균을 실행하는 것 — 이 갈림길 근처에서 §2의 평균을 다시 불러올 수 있다([[05-construction-robotics/imitating-contact|10. 접촉 모방 §4]]). §2의 그림이 셋을 모두 그린다.

| | 토큰 | 노이즈 제거기(확산·flow) | CVAE 회귀 |
|---|---|---|---|
| 청크당 패스 | $D\times H$번, 순차 | $N$번, $H$와 무관 | $1$번 |
| 다봉성 | 표본으로 뽑으면 구간 분포 안에 | 구성상 | 학습에서 잠재변수로. ACT는 $z=0$으로 디코딩한다 |
| 정밀도 한계 | 구간 폭(D4에서 $0.16\,\mathrm{mm}$) | 속도를 위해 줄인 스텝 수 | 회귀 분산 |
| 물려받는 것 | 사전학습 LM의 가중치와 언어 일반화 | 확산의 샘플러, MPC의 receding horizon | 평범한 트랜스포머 디코더 |

그러니 선택은 유행이 아니라 §3의 예산을 따른다. 언어 백본의 일반화가 요점이고 청크가 짧으면 토큰을 유지하고, 청크가 길거나 시연이 강하게 다봉이면 노이즈 제거기로 옮기며, 어느 쪽이든 시연 영상을 믿기 전에 헤드를 $\ell(k)$에 대어 확인한다.

**추론도 같은 화폐로 치른다.** 토큰 헤드는 행동하기 전에 글을 쓰도록 배울 수도 있다. RT-2는 행동 토큰 앞에 계획을 말로 적는 작은 변형 — "Plan: pick energy drink" — 으로 이것을 시도했다([[01-canonical-papers/notes/4-vla/rt-2|RT-2]]). Embodied chain-of-thought(ECoT, Zawalski 외 2024)는 그것을 체계로 만든다. OpenVLA를 미세조정해 계획, 지금의 하위 과제, 움직임 기본 동작, 물체의 bounding box, 이미지 속 그리퍼 위치를 쓰고 그다음에야 행동을 내게 하며, 추론 label은 사전학습된 검출기와 대규모 언어 모델이 자동으로 만든다. 그것으로 OpenVLA의 절대 성공률이 일반화 과제 — 새 물체, 장면, 시점, 지시 — 에서 로봇 데이터를 더하지 않고 $28$%p 올랐다. 추론 토큰 하나하나가 행동 토큰과 똑같은 순차 디코딩이고, ECoT의 스텝당 토큰은 $7$개에서 $350$개가 되었다. D4에서 그 길이의 사슬은 토큰 헤드의 $6$번 통과를 $343+6=349$번으로 바꾼다. 논문의 처방은 §3의 교환을 다른 곳에 쓰는 것이다. 상위 계획과 하위 과제를 다섯 스텝마다 한 번만 새로 만들자 추론이 약 4분의 1 빨라졌고, 과제 세 개짜리 부분집합에서 성공률이 매 스텝 새로 추론할 때의 $63\%$에 비해 $72\%$였다. 추론이 사는 것은 일반화와 읽을 수 있는 실패다 — 틀린 bounding box가 정책이 어디서 어긋났는지 보여 준다. 치르는 것은 rate이므로, 추론하는 정책의 제어 주파수는 성공률과 같은 행에 적어야 한다. 아래의 접힌 메모가 실제 제품 둘을 이 교환 위에 놓는다.

> [!note]- 더 깊이 · Deeper
> **제품의 두 배치.** Gemini Robotics 1.5는 이 발상을 실제 제품 VLA에 넣어, 계획과 진행 추정을 맡는 별도의 체화 추론 모델 옆에서 행동 사이사이에 자연어로 된 여러 층의 추론을 끼운다([[01-canonical-papers/notes/4-vla/gemini-robotics|Gemini Robotics]]). Generalist의 GEN-0은 반대 배치를 주장한다. 빠른 층과 느린 층을 나누지 않고, 감지 토큰과 행동 토큰을 비동기 연속 시간 흐름으로 둔다. 둘 다 추론의 디코딩을 어디에 쓰느냐에 관한 주장이고, 위의 셈이 묻는 질문이 그것이다.

### 7. 정책 하나, 몸 여럿: embodiment 격차

*한 문장으로:* 정책 하나를 여러 로봇으로 학습하면 같은 행동 숫자가 몸마다 다른 움직임을 뜻하게 되고, 범용 정책의 설계는 저마다 정책에게 지금 어느 몸을 움직이는지 알려 주는 방법이다.

*이 절에서 하나만 가져간다면:* 정규화된 label은 그것이 어느 로봇에서 왔는지 말하지 않는다. D4의 정규화된 chunk를 팔 B에서 재생하면 $6$과 $3\,\mathrm{cm}$를 지나쳐 의도한 움직임의 두 배 반을 간다(**D4에서 숫자로 본 격차**).

§1은 로봇 하나에서 단위 오류가 물리적 오류임을 보였다. 여러 로봇의 시연을 한데 모으면 같은 오류가 체계적이 된다. 로봇마다 로그가 자기 행동 규약으로 말하기 때문이다. [[01-canonical-papers/notes/4-vla/open-x-embodiment|Open X-Embodiment]]는 로봇 22대를 모으고 행동을 거칠게만 맞췄으며, 저자들은 같은 행동 벡터가 로봇마다 매우 다른 움직임을 낳을 수 있다고 분명히 적는다. 그 문장이 정책이 보는 **embodiment 격차**(embodiment gap)다. 한 행동이 두 몸에서 다른 움직임을 뜻하게 하거나 한 움직임에 다른 행동이 필요하게 만드는 모든 것 — 단위와 스케일, 좌표계, 절대값인지 변화량인지, 제어 주기, 행동 차원, 기구학적 한계, 카메라가 놓인 곳.

**D4에서 숫자로 본 격차.** D4를 둘째 팔 B와 합친다. B는 같은 종류의 2차원 end-effector 변화량을 기록하지만 $5\,\mathrm{Hz}$에서 스텝당 $a_{\max}=0.05\,\mathrm{m}$까지 허용한다. 각 데이터셋을 자기 한계로 정규화해 둘 다 $[-1,1]$을 채우게 한다.

- D4의 고정 chunk는 $(-1,0)$, $(-1,0)$, $(0,-1)$이 된다.
- 같은 숫자를 B에서 실행하면 $(-0.05,0)$, $(-0.05,0)$, $(0,-0.05)$만큼 움직인다. $3\times0.2=0.6\,\mathrm{s}$ 동안 왼쪽으로 $0.10\,\mathrm{m}$, 아래로 $0.05\,\mathrm{m}$이고, D4는 $0.15\,\mathrm{s}$ 동안 $0.04$와 $0.02\,\mathrm{m}$를 움직인다.
- D4의 목표 $g=(-0.04,-0.02)$를 겨누면 B는 $6$과 $3\,\mathrm{cm}$를 지나친다 — 의도한 움직임의 두 배 반이다. 속도는 D4의 $0.02/0.05=0.4\,\mathrm{m/s}$ 대신 $0.05/0.2=0.25\,\mathrm{m/s}$다.

정규화된 label 어디에도 그것이 어느 로봇에서 왔는지 적혀 있지 않다. 말해 줄 수 있는 것은 관측뿐이고, 그것도 카메라 시점이나 고유수용 감각이 가려낼 만큼 다를 때뿐이다.

**설계 다섯, 각자 어딘가에서 치른다.** 범용 정책들은 격차를 다섯 가지로 메운다.

| 설계 | 몸이 정책에 들어가는 방식 | 대가 |
|---|---|---|
| 거친 정렬([[01-canonical-papers/notes/4-vla/open-x-embodiment\|OXE]]의 RT-X 모델) | 7차원 end-effector 행동 하나 — 위치, 회전, 그리퍼, 또는 그 변화율 — 와 데이터셋마다 대표 카메라 하나. 좌표계와 절대·변화량 규약은 각 로봇의 것 그대로 | 정책이 이미지에서 몸을 알아봐야 하고, 닮아 보이는 두 로봇은 한 규약을 나눠 쓴다 |
| 가장 큰 몸에 맞춰 채우기([[01-canonical-papers/notes/4-vla/pi0\|π0]]) | 18차원 행동 — 6자유도 팔 둘, 그리퍼 둘, 이동 베이스, 몸통 승강 — 을 작은 로봇은 0으로 채우고, 없는 카메라는 가린다 | D4는 18차원 가운데 2개를 채운다. $N$번 통과가 폭과 무관한 노이즈 제거기에는 공짜지만, 토큰 헤드는 D4의 chunk에 $6$개 대신 $18\times3=54$개 토큰을 디코딩해야 한다 |
| 몸마다 헤드([[01-canonical-papers/notes/4-vla/octo\|Octo]], [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]]) | 공유 몸통에 새 로봇마다 새 관측·행동 토큰과 작은 헤드를 붙이거나(Octo), 모델 하나 둘레에 embodiment별 인코더와 디코더를 둔다(GR00T) | 새 몸마다 자기 데이터가 필요하다. Octo의 방법은 시연 약 $100$개와 미세조정 $5$시간이다 |
| 비디오에서 잠재 행동([[01-canonical-papers/notes/5-world-models/genie\|Genie]]의 발상, GR00T 데이터의 바닥) | 행동 label 없이 비디오 프레임 사이의 이산 코드로 추론한 행동([[03-deep-learning/diffusion/vae-gan\|6.1 §10]]) | 잠재 행동은 명령이 아니다. 몸에 맞춘 층이 여전히 그것을 명령으로 옮겨야 한다 |
| 몸 사이의 학습된 전이([[01-canonical-papers/notes/4-vla/gemini-robotics\|Gemini Robotics]] 1.5) | 여러 몸의 이질적인 데이터로 학습한 VLA 하나가 구조 안에 Motion Transfer 메커니즘을 두고, 후속의 온디바이스 모델은 새 몸에 몇 시간의 데이터로 적응한다 | 메커니즘은 기술 보고서에 설명될 뿐 공개되지 않았고, 평가는 회사의 것이다 |

최근의 세 흐름이 이 표를 늘린다. 사람 비디오와 행동을 공유하는 GR00T N1.7, 시뮬레이션 속 몸 $100{,}000$종에 걸쳐 학습한 Skild AI의 정책, 그리고 최대 백만 시간에 이르는 사람 비디오와 장치 기록으로 하는 사전학습이다. 아래의 접힌 메모가 그 숫자들과, 각각이 확인할 거리로 남기는 것을 적는다.

> [!note]- 더 깊이 · Deeper
> **GR00T N1.7.** GR00T의 후속 버전은 공유 규약 쪽으로 일부 되돌아왔다. N1.7(2026)은 행동을 로봇과 사람 비디오가 함께 쓰는 *상대* end-effector 변화량으로 나타내고, 그래서 사람 비디오 $20{,}000$시간이 같은 헤드를 학습시킬 수 있다([[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]]). OXE 방식의 거친 정렬이므로 아래 질문이 그대로 적용된다. 어떤 단위로, 어느 좌표계에서, 어떤 주기로.
>
> **Skild AI의 옴니바디 정책.** Skild AI는 다섯째 설계를 가장 멀리 민다. 시뮬레이션에서 로봇 몸 $100{,}000$종에 걸쳐 학습한 "옴니바디" 정책으로, 학습에서 뺀 몸을 제어하고 다리를 잃은 뒤 몇 초 안에 다시 적응한다고 보고한다([Skild AI](https://www.skild.ai/blogs/omni-bodied)). 회사의 시연이고, 같은 글이 깨끗하게 통제된 영상이 능력의 착시를 만들 수 있다고 스스로 경고한다.
>
> **사람 손이 모인 데이터에서 가장 큰 몸이 되어 간다.** GR00T N1.7은 사람 비디오 $20{,}000$시간으로 사전학습하고, DYNA-2(Dyna Robotics, 2026년 8월)는 로봇 데이터 없이 머리에 단 카메라로 찍은 사람 비디오 100만 시간 이상으로 사전학습하며 의사 행동을 3D 손 자세에서 복원하고([Dyna](https://www.dyna.co/dyna-2)), GEN-0(Generalist AI, 2025)은 수천 대의 장치와 로봇이 기록한 실제 조작 $270{,}000$시간 이상으로 사전학습한다([Generalist AI](https://generalistai.com/blog)). DYNA-2는 이득을 거듭제곱 법칙으로 적는데, 형용사보다 지수를 먼저 읽을 만하다. 보류한 사람 데이터의 오차는 $D^{-0.0184}$로 떨어지므로 비디오를 천 배 늘려도 약 $12\%$ 낮아지고, zero-shot 로봇 행동 오차는 $D^{-0.0713}$로 천 배마다 약 $39\%$ 떨어진다. 이득은 실재하고, 매끄럽고, 느리다. 그리고 같은 사후학습 예산에서 고객 현장 합격률이 이전 모델의 $46\%$에 비해 $87\%$였다. 이 모델들이 아직 건너야 할 격차는 이 절 자신의 것이다. 사람 손도 제 기구학을 가진 몸이고, 의사 행동은 그 손이 한 일의 추정이다.

**증거가 말하는 것.** OXE의 결과는 대상 로봇이 이미 가진 데이터가 얼마인지에 따라 갈린다. 자기 데이터가 적은 로봇 다섯에서, 모은 데이터로 학습한 RT-1-X는 넷에서 각 연구실의 원래 방법을 이겼고, 평균 성공률이 원래 방법이나 그 로봇 데이터로만 학습한 RT-1보다 $50\%$ 높았다. 데이터가 많을 때는 졌다. WidowX의 Bridge 과제에서 두 평가 장소 모두 $27\%$로, 그 데이터로만 학습한 RT-1의 $40\%$와 $30\%$에 못 미쳤고, Google 로봇의 RT-1 과제에서는 $92\%$ 대비 $73\%$였다. 55B RT-2-X는 회복했다 — $50\%$, $30\%$, $91\%$. 그래서 논문은 그 패배를 과소적합으로 읽는다. 작은 모델은 용량을 다른 몸들에 쓴다. 기술의 전이도 실재한다. RT-2-X는 물체와 동작이 WidowX 데이터에만 있는 창발 기술에서 RT-2의 점수를 대략 세 배로 올렸고, 그 데이터셋을 빼자 이득이 크게 줄었다.

**교차-embodiment 주장에 물을 것**, §4의 증거 사다리에 더해:

- 각 데이터셋의 행동 규약 — 단위, 좌표계, 절대·변화량, 주기 — 과 그것을 어떻게 변환했는가.
- 몸을 무엇으로 알아보는가. 이미지만으로, 채우기로, 아니면 자기 헤드로.
- 대상 로봇이 데이터를 얼마나 보태는가.
- 그 데이터만으로 학습한 전문 모델을 기준선으로. OXE는 판정이 그것에 따라 뒤집힘을 보인다.

건설 기계는 두 축 모두의 먼 끝에 있다. 오랫동안 자기 데이터가 적을 것이고, 모으기가 도움이 된 곳이 거기다. 그리고 몸이 모인 데이터의 어떤 것과도 다르다 — OXE 노트는 거기서 건설 비슷한 것을 하나도 찾지 못한다 — 거친 정렬이 가장 약하고 D4와 B의 계산이 가장 아프게 무는 곳이 거기다. 그런 몸에서는 정책이 카메라 이미지로 규약을 짐작하리라 믿지 말고, 물리 단위와 초로 규약을 명시적으로 변환하라.

### 8. 시연을 프롬프트로: in-context 모방학습

지금까지는 모두 가중치를 바꿔서 정책을 가르쳤다. In-context learning — 큰 모델이 가중치 갱신 없이 프롬프트의 예시에서 과제를 익힌다는 [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]의 발견 — 에는 로봇판이 있다. 새 과제의 시연을 정책의 문맥에 넣고 흉내 내게 하는 것이다.

> **In-context 모방학습의 정의.** **In-context 모방학습**(in-context imitation learning)은 *시험 때의 학습된 정책*이 갖는 성질이다. 학습하지 않은 과제를 입력에 넣은 시연만으로 지정받아 수행한다. 정의 조건은 셋이다. 시연은 학습 데이터가 아니라 관측–행동 시퀀스로 **입력 안에** 있다. 시연을 받고 행동하기까지 **파라미터가 바뀌지 않는다**. 그리고 과제는 모델에게 **새것**이다. 이미 배운 과제를 흉내 내는 것은 학습이 아니라 검색이나 조건화다.
>
> $$a_{t:t+H-1}\sim\pi_\theta\big(\,\cdot\mid \underbrace{(o,a)^{\text{demo}}_{1:T}}_{\text{프롬프트}},\ o_{\le t}\big),\qquad \theta\ \text{고정}$$
>
> $(o,a)^{\text{demo}}_{1:T}$는 새 과제의 관측–행동 쌍 $T$개로 입력에 적어 넣은 시연, $o_{\le t}$는 로봇이 자기 시도에서 지금까지 관측한 것, $a_{t:t+H-1}$은 로봇이 내는 청크이고, "$\theta$ 고정"은 프롬프트를 읽고 행동하기까지 경사 스텝이 하나도 없다는 뜻이다. 그래서 과제의 명세 전부가 입력에 있고 가중치에는 하나도 없다.
>
> - **예**: 아래 GEN-1.5의 "physical prompting". 새 과제의 몇 초를 다시 학습하지 않는 모델의 문맥에 넣는다.
> - **비예**: 같은 5분짜리 시연 묶음으로 미세조정하기. 데이터는 같지만 둘째 조건이 깨지고, 학습을 한 번 돌려야 한다.
> - **비예**: 정책이 학습한 기술을 이름으로 부르는 언어 지시. 입력이 과제를 지정하지만 셋째 조건이 깨진다. 새로 배우는 것이 없다.
> - **왜 중요한가**: 새 과제의 비용을 학습 한 번에서 프롬프트로 옮긴다. 그 비용은 스텝마다 토큰과 지연으로 치르고(아래의 값), 성공률은 셋째 조건이 성립할 때만 학습의 증거가 된다. 이 절 끝의 질문들이 사전학습에 이미 무엇이 있었는지부터 묻는 이유다.

**2026년까지 세 걸음.** Keypoint Action Tokens(Di Palo·Johns, 2024)는 시각 키포인트와 행동 궤적을 텍스트로 적어, 언어로만 학습한 기성 GPT-4 Turbo가 시연 몇 개로 흉내 내게 했고, 데이터가 적은 영역에서 디퓨전 정책과 대등했다([arXiv:2403.19578](https://arxiv.org/abs/2403.19578)). ICRT(Fu 외, 2024)는 감각운동 궤적으로 인과 트랜스포머를 학습하고, Franka에서 처음 보는 과제의 원격조작 궤적으로 프롬프트했다([arXiv:2408.15980](https://arxiv.org/abs/2408.15980)). **GEN-1.5**(Generalist AI, 2026년 8월)는 이것을 *physical prompting*이라 부른다. 손에 드는 그리퍼나 로봇 자신으로 기록한 $3$–$12$초짜리 감각운동 시연을, $30$초의 기억을 지니고 $100$ Hz로 행동을 내는 멀티모달 모델의 문맥에 넣는다([Generalist AI](https://generalistai.com/blog/gen-1.5)). 병, 지퍼, 지갑 같은 짧은 손재주 과제 열 개에서 시연 하나는 경사 스텝 없이 $59\pm10\%$ 성공을 냈고, 5분 분량 데이터, 곧 시연 약 쉰 개로 경사 스텝 열 번을 밟자 $83\pm9\%$였다. 회사는 구조에도 학습에도 in-context learning을 위해 만든 것이 없다고 하고, 한계도 스스로 적는다. 짧은 지평의 과제, 수수한 성공률, 미세조정한 기술보다 부서지기 쉬운 기술. Skild AI의 S1(2026년 8월) — 회사의 제품 이름으로, [[05-construction-robotics/site-engineering|2.5]]가 정한 건설 트랙의 외장 패널 과제 S1과는 다르다 — 은 대신 *비디오* 시연을 받아 제 몸으로 옮기며, 사전학습에 없던 과제에서 VLA 기준선 $9\%$ 대비 $66\%$, 시연 하나가 사후학습 에피소드 약 $380$개와 맞먹는다고 추정한다([Skild AI](https://skild.ai/blogs/s1)). 이것도 회사 숫자이고, 대조해 볼 과제 목록이 없다.

**D4에서 본 프롬프트의 값.** 문맥 속 시연은 토큰으로 치른다. D4의 $20$ Hz에서 12초는 $240$ 스텝이고, 스텝마다 관측 토큰 하나와 행동 토큰 $D=2$개면 첫 행동 전에 $720$개 토큰을 인코딩한다. key–value 캐시가 있으면 한 번만 인코딩하지만, 뒤의 모든 토큰이 여전히 그것들에 주의를 두므로, 프롬프트는 문맥에 남아 있는 동안 스텝마다 attention 비용을 더한다. §6의 순차 예산을 이번에는 추론이 아니라 기억에 쓰는 것이다. 시연을 대신 이미지로 — PaliGemma 크기의 백본에서 초당 $10$프레임, 프레임마다 토큰 $256$개로 — 지니면 30초짜리 시연에 약 $1.42$ GB의 key–value 캐시가 든다. 그 셈은 [[03-deep-learning/foundations/sequence-models|1.1 시퀀스 모델]]의 스스로 점검 7이고, 그 페이지의 §13이 캐시를 줄이는 하이브리드를 보이며, 캐시 자체는 [[03-deep-learning/foundations/attention-transformer|1.2 §7]]이다. 둘 다 프롬프트가 길어지기 전까지는 경로 밖이다. GEN-1.5의 $100$ Hz에서 같은 12초는 행동 $1{,}200$ 스텝이다.

**in-context 주장에 물을 것**, §4의 증거 사다리에 더해:

- 그 과제, 또는 그와 가까운 과제가 사전학습에 있었는가 — 학습과 검색 사이의 선.
- 시행은 몇 번이고, 무엇을 성공으로 쳤는가.
- 프롬프트는 얼마나 길고, 첫 행동 전에 지연을 얼마나 더하는가.
- 같은 데이터로 미세조정한 결과. GEN-1.5 자신의 숫자가 선택의 값을 매긴다. 시연 몇 초에 학습 없이 $59\%$, 5분과 짧은 학습으로 $83\%$.

건설 작업반에게 끌리는 점은 분명하다 — 새 고정 작업을 손에 드는 그리퍼로 한 번 보여 주고 기계가 하게 한다 — 그리고 주의할 점도 분명하다. 지금까지의 증거는 짧고 단순한 탁상 규모 과제다.

### 읽고 나면

VLA 하나를 observation·language·action/frame/rate·horizon $H$·실행 stride $k$·data/objective·controller·replanning·evidence로 한 줄에 명세할 수 있다. 논문이 $H$는 주고 $k$를 주지 않았다면 그 줄은 불완전하고 지연 주장도 불완전하다. 행동 헤드가 토큰인지 노이즈 제거기인지 CVAE인지도 적고, §6의 비용 가운데 무엇을 치르는지 말한다. 여러 로봇으로 학습한 정책이라면 몸이 어떻게 들어가는지 — 정렬, 채우기, 자기 헤드, 잠재 행동 — 말하고, 첫 행동 전에 디코딩하는 토큰을 추론까지 포함해 센다. 프롬프트에서 배운다는 주장이라면 검색과도, 같은 데이터의 미세조정과도 갈라 읽는다.

### 스스로 점검

1. D4의 interface는 20 Hz에서 스텝당 $a_{\max}=0.02\,\mathrm{m}$를 받는다. 이 행동 표현이 나타낼 수 있는 가장 빠른 도구 속도는 얼마이고, 그 두 배로 기록된 시연은 어떻게 되는가?
2. 어떤 정책이 $H=16$, 추론 5 Hz라고 보고했다. 이와 모순되지 않는 가장 긴 개루프 구간은 얼마이고, 확정하려면 어떤 숫자가 더 필요한가?
3. §5에서 $k=2$의 반전이 $k=1$보다 *많은* 이유는 무엇인가? chunk는 더 긴데도.
4. MSE head를 2성분 가우시안 혼합으로 바꿨더니 offline action error가 나빠졌다. 그런데도 정책이 좋아졌다고 읽을 수 있는 독법을 대라.
5. 축을 하나씩 쓰는 계획이 직선과 같은 이동거리를 쓰려면 D4의 고정 숫자 중 무엇이 바뀌어야 하는가?
6. 당신의 팔로 모은 시연 5,000개로 미세조정한 교차-embodiment 정책이 $70\%$ 성공하고, 그 5,000개만으로 학습한 전문 모델이 $75\%$ 성공한다. 음의 전이라고 부르기 전에 무엇을 확인하며, OXE의 어느 결과와 닮았는가?
7. ECoT는 OpenVLA의 성공률을 $28$%p 올렸다. §6의 잣대로 그 대가는 무엇이었고, 20 Hz 팔에 올리기 전에 무엇을 묻겠는가?
8. 어느 회사가 프롬프트에 넣은 시연 하나로 새 과제에서 $59\%$ 성공을 보고한다. §8의 세 조건 가운데 무엇을 먼저 확인하겠으며, 어떤 비교가 그 숫자를 결정으로 바꾸는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $a_{\max}/\Delta t=0.02/0.05=0.4\,\mathrm{m/s}$. $0.8\,\mathrm{m/s}$의 시연은 표현되지 않는다. 모든 label이 클립에 걸리므로 복제된 정책은 체계적으로 느리고, 클립 *이후*에 계산한 스텝별 손실에는 그 오차가 보이지 않는다. 단위와 한계는 배포가 아니라 label의 일부다.
> 2. $t_{\mathrm{inf}}=0.2\,\mathrm{s}$이고 개루프 구간의 길이는 $H$가 아니라 행동 $k$개다. $k=H=16$부터 스케줄 가능한 최소 $k=\lceil t_{\mathrm{inf}}/\Delta t\rceil$까지 무엇이든 될 수 있다. 제어 주기 $\Delta t$와 실행 stride $k$가 없으면 지연은 미정이고, 그래서 읽고 나면 줄이 둘 다를 요구한다.
> 3. 반전은 스텝마다 세고, 두 행 모두 새로 흔들린 계획이 도구가 2 cm를 끝내기도 전에 도착하는 영역에 있다. 둘 중 어느 쪽이 더 많은지는 경계가 고정된 흔들림 수열의 어디에 떨어지는지가 정한다. 인용할 결과는 $k=3$의 문턱이지 6과 10의 차이가 아니다.
> 4. offline error는 개별 시연 행동을 상대로 재고, MSE head는 봉우리들의 평균을 내놓아 그것을 최소화한다. $(-1,0)$과 $(1,0)$에 절반씩 질량을 둔 혼합은 어떤 단일 label과의 평균 거리가 *더 크면서*, 둘 중 시연된 행동을 실제로 내놓는 유일한 쪽이다. 판정하는 증거는 loss가 아니라 폐루프 성공이다.
> 5. 목표다. 이동거리 벌점은 $\lVert g\rVert_1/\lVert g\rVert_2$이므로 목표가 축 위에 있을 때만 1이다. $g=(-0.06,0)$이면 어느 계획이든 같은 6 cm다. $a_{\max}$나 $\delta$나 주기를 바꿔도 없어지지 않는다. instruction의 축 순서와 목표 방향의 성질이기 때문이다.
> 6. 먼저 §4의 셈이다. 각각 $100$번이라면 $70\%$와 $75\%$의 구간 $[0.60,\ 0.78]$과 $[0.66,\ 0.82]$가 겹치므로 아직 아무것도 순위가 정해지지 않았다. 그다음 §7의 규약이다. 당신 팔의 행동이 label과 같은 단위, 좌표계, 주기로 모은 데이터에 들어갔는가 — D4와 B의 경우는 정규화된 label이 몸을 두 배 반이나 멀리 움직이는 것을 보인다. 둘 다 문제가 없다면 OXE의 데이터가 많은 영역과 닮았다. 거기서 RT-1-X는 전문 모델에 졌고($27\%$ 대 $40\%$, $73\%$ 대 $92\%$) 55B RT-2-X가 그 차이를 메웠다. 그러니 다음 실험은 용량이다 — 더 큰 모델, 또는 당신 팔만의 헤드 — 이고, 전문 모델 기준선과 나란히 보고한다.
> 7. 순차 디코딩이다. 스텝당 토큰 $7$개가 $350$개가 되었으므로 D4의 chunk당 $6$번 통과는 $349$번이 된다. 실제로 도달한 제어 주파수와 사슬을 어떻게 스케줄하는지 물어라 — ECoT 자신의 다섯 스텝 계획·하위 과제 유지는 약 4분의 1 빨랐고 부분집합에서 $63\%$ 대비 $72\%$였다 — 그리고 이득을 당신 과제에 필요한 종류의 일반화, 곧 새 물체·장면·시점·지시에서 쟀는지. 다섯 스텝 동안 유지하는 계획은 계획의 chunk이므로 §3의 나이 계산이 그대로 적용된다. 20 Hz에서 다섯째 스텝에 작용하는 계획은 장면보다 적어도 $0.20\,\mathrm{s}$ 늙었다.
> 8. 셋째 조건이 먼저다. 그 과제, 또는 그와 가까운 과제가 사전학습에 있었는가. 이미 배운 과제를 흉내 내는 것은 검색이고, 강한 모델은 어떤 단서로도 그것을 해낸다. 그다음은 같은 데이터에서의 비교다. GEN-1.5 자신의 미세조정은 5분 분량 데이터와 경사 스텝 열 번으로 $83\%$에 닿았으므로, 결정은 $24$%p와 덜 부서지는 기술이 과제마다 짧은 학습 한 번의 값어치가 있느냐다. 프롬프트가 더하는 지연과 $59\%$ 뒤의 시행 수도 함께 본다.

### 과제 · Problem set

Tier A. [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D4**, 이 페이지, [[02-foundations/lab-kernel|0.7 Lab Kernel]]. 영어 절 §5의 손잡이를 바꿔라. 루프를 다시 쓰지 마라. 답안에 tier를 명시하라.

1. **그리기.** 위의 그림을 과제 2의 로봇 — 제어기를 $50\,\mathrm{Hz}$로 다시 올렸고 추론은 여전히 $100\,\mathrm{ms}$ — 에 대해 $k=5$로 다시 그린다. 시계 둘을 표시한 루프(제어기 변에 $\Delta t$, 정책 변에 $t_{\mathrm{inf}}$)와 길이 $k$인 상자로 그린 chunk 버퍼를 그리고, 이어서 제어 스텝 $45$–$59$로 펼친 루프에 chunk 경계, 각 chunk의 관측 스텝, 실행되는 모든 행동의 나이, $t=1.0\,\mathrm{s}$의 장면 변화를 그린다. 루프에서 존재하지 **않는** 변 하나를 표시하고, 그것을 믿으면 무슨 뜻이 되는지 한 문장으로 쓴다.
2. **유도.** 제어기를 $50\,\mathrm{Hz}$로 다시 올리고 추론은 여전히 $100\,\mathrm{ms}$다. (a) 스케줄 가능한 최소 chunk $m$. (b) $k=5$의 최악 행동 나이. (c) $t=1.0\,\mathrm{s}$의 장면 변화에 대해 $k=5$와 $k=20$의 $\ell(k)$. (d) (c)를 §5의 20 Hz 숫자와 비교해 더 빠른 제어기가 무엇을 사고 무엇을 사지 못했는지 한 문장으로.
3. **실행.** 영어 절 패치의 `?`를 채우고 §5의 쓸기를 다시 돌린다. 이제 목표가 *두 번* 움직인다. 스텝 20에 위로, 스텝 40에 다시 아래로, 1초 간격이다. 충분히 긴 chunk는 한 사건 내내 앞 사건을 쫓는 데 쓸 수 있다. $k\in\{2,3,5,10,20\}$에 대해 이동거리·반전·두 변화 각각의 지연을 보고하고, 어떤 변화에 대한 반응이 *다음* 변화보다 먼저 도착하는 가장 큰 $k$를 말한다. 이 episode의 이상적 이동거리는 14 cm다(나갈 때 6, 위로 4, 아래로 4).

> [!note]- 그리는 법 · How to draw it
> - 시계는 하나가 아니라 둘이다. 정책 변에 $t_{\mathrm{inf}}$, 제어기 변에 $\Delta t$를 적는다. 루프에 주기를 하나만 적는 것이 가장 흔한 오답이고, 이 페이지의 지연 숫자는 전부 둘이 다르다는 데서 나온다.
> - chunk 버퍼는 길이 $k$인 상자로 그리고, 비었을 때만 다시 채워지지만 그 채움이 쓰는 관측은 $m$ 스텝 앞, 마지막 행동 $m$개가 아직 남아 있을 때 찍힌다고 표시한다. 개루프 구간이 사는 자리가 그 상자다.
> - 관측 변의 나이는 $n$이 아니라 $n-m$으로 적는다. 스텝 $n$에 버퍼에서 나가는 행동은 $m+(n\bmod k)$ 스텝 묵은 장면에서 계산됐다.
> - 버퍼에서 장면으로 가는 화살표는 그리지 않는다. 세계를 바꾸는 것은 로봇이지 버퍼 속 계획이 아니다. 그 화살표를 그린 루프는 예측을 곧 세계로 가정한 것이고, §4가 다루는 오류가 그것이다.
> - 펼친 띠에는 $k$ 스텝마다 경계를 두고, 각 chunk의 관측 스텝에서 첫 행동까지 길이 $m$인 호를 그린다. $m=k=5$이면 호마다 바로 앞 chunk가 시작한 자리에서 출발하므로, 경계에 떨어진 장면 변화는 chunk 하나 늦게 읽힌다.

> [!tip]- 정답 · Solutions
> 1. 장면 → 관측(나이 $n-m$) → 정책($t_{\mathrm{inf}}=100\,\mathrm{ms}$) → chunk 버퍼(길이 $k=5$) → 제어기($\Delta t=20\,\mathrm{ms}$) → 로봇 → 장면. 버퍼에서 관측으로 돌아가는 변은 $k$ 스텝마다만 닫힌다. 이제 $m=\lceil0.10/0.02\rceil=5=k$이므로 다시 채울 때마다 chunk 하나 앞의 관측을 쓴다. 스텝 $45$, $50$, $55$에서 시작하는 chunk는 스텝 $40$, $45$, $50$의 관측으로 계산됐고, 어느 chunk에서나 실행되는 행동은 $5,6,7,8,9$ 스텝 묵었으므로 최악의 나이는 $9\times0.02=0.18\,\mathrm{s}$다. $t=1.0\,\mathrm{s}$의 장면 변화는 스텝 $50$이다. 거기서 시작하는 chunk는 스텝 $45$에서 계산되어 변화를 알 수 없으므로, 처음으로 변화를 아는 행동은 스텝 $55$에 있다. $\ell=5\times0.02=0.10\,\mathrm{s}$로, 그림의 $20\,\mathrm{Hz}$, $k=3$일 때의 $0.20\,\mathrm{s}$와 비교된다. 없는 변은 버퍼 → 장면이다. 계획이 세계를 움직이지 않고 실행된 행동만 움직인다. 그 변을 그리는 것은 예측을 상태로 가정하는 것이고, 개루프 chunk가 검증된 것처럼 보고되는 경로가 그것이다.
> 2. (a) $\Delta t=0.02\,\mathrm{s}$이므로 $m=\lceil 0.10/0.02\rceil=5$. 더 빠른 제어기가 최소 chunk를 2에서 5로 *올렸다*. (b) $(5+4)\times0.02=0.18\,\mathrm{s}$, 20 Hz의 $0.30\,\mathrm{s}$와 비교된다. (c) 변화는 이제 스텝 $n_j=50$이다. $k=5$: $\lceil55/5\rceil=11$, 경계 55, $\ell=0.10\,\mathrm{s}$. $k=20$: $\lceil55/20\rceil=3$, 경계 60, $\ell=0.20\,\mathrm{s}$. (d) 같은 $k$에서 더 빠른 제어기는 지연을 줄이고($k=5$에서 0.25 → 0.10초) 움직임을 매끄럽게 했지만, 추론 시계에 대해서는 아무것도 사지 못했다. 가장 짧은 확정 구간은 여전히 $t_{\mathrm{inf}}=0.10\,\mathrm{s}$의 움직임이고, 이제 행동 2개가 아니라 5개로 적힐 뿐이다.
> 3. 빈칸은 `return g_after if obs < njump2 else g_before`와 `src[n] >= e`다. 돌려 보면 $k=2$는 36.22 cm, 반전 9, 지연 $0.10/0.10\,\mathrm{s}$. $k=3$은 28.78 cm, 0, $0.20/0.10$. $k=5$는 20.60 cm, 0, $0.25/0.25$. $k=10$은 14.10 cm, 0, $0.50/0.50$. $k=20$은 13.90 cm, 0, $1.00/1.00$이다. 변화 간격이 $1.00\,\mathrm{s}$이므로 $k=20$의 반응은 다음 변화와 정확히 동시에 도착한다. 아직 거기 있는 목표에 대해서는 한 번도 움직이지 못한다는 뜻이고, 제때 반응하는 가장 큰 $k$는 **10**이다. 마지막 두 행에서 할 말이 둘이다. 이동거리는 포화했다. 14.10 대 13.90 cm는 눈감는 시간을 두 배로 치르고 1.4%를 얻은 것이고, 이상값이 14 cm이므로 $k=10$은 이미 다시 결정하는 데 사실상 아무것도 쓰지 않는다. 그리고 매끄러움 열은 $k=3$에서 값을 다 치렀다. 그 뒤의 긴 chunk는 로봇이 이미 산 것을 다시 사면서 되돌릴 수 없는 지연을 치른다.

### 출처 · Sources

§1–§7이 잇는 노트들이 각 논문의 인용을 담는다. §6과 §7의 숫자 가운데 노트가 아니라 논문 본문에서 온 것의 출처는 다음과 같다.

- Black, K. 외. "π0: A Vision-Language-Action Flow Model for General Robot Control." arXiv:2410.24164, 2024 — 가중치 두 벌, 캐시한 관측과 flow 스텝 열 번(부록 Table I: $14$, $32$, $27\,\mathrm{ms}$, 로봇 위 $73\,\mathrm{ms}$), 0으로 채운 18차원 행동.
- Open X-Embodiment Collaboration. "Open X-Embodiment: Robotic Learning Datasets and RT-X Models." *ICRA*, 2024, pp. 6892–6903 — 거친 7차원 정렬과 Table I의 대규모 데이터 비교.
- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C. & Levine, S. "Robotic Control via Embodied Chain-of-Thought Reasoning." *CoRL*, 2024 — 추론 단계, $28$%p 이득, 스텝당 토큰 $7$ 대 $350$, 다섯 스텝 유지(Table 2).
- Liang, W., Yu, L., Luo, L., Iyer, S. 외. "Mixture-of-Transformers: A Sparse and Scalable Architecture for Multi-Modal Foundation Models." arXiv:2411.04996, 2024 — 전역 self-attention 아래 모달리티별 가중치, 7B 텍스트·이미지 설정에서 FLOPs의 $55.8\%$.
- Di Palo, N. & Johns, E. "Keypoint Action Tokens Enable In-Context Imitation Learning in Robotics." arXiv:2403.19578, 2024; Fu, L. 외. "In-Context Imitation Learning via Next-Token Prediction." arXiv:2408.15980, 2024 — physical prompting 이전의 두 연구 걸음.
- Generalist AI. "GEN-1.5: Embodied Foundation Models are One-Shot Learners"(2026-08-19)와 "GEN-0"(2025-11-04), 회사 글 — physical prompting, $59$와 $83\%$, 27만 시간.
- Dyna Robotics. "Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models"(2026년 8월), 회사 보고서 — 거듭제곱 법칙, 미세조정 예산, $87$ 대 $46\%$.
- Gemini Robotics Team. "Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer." arXiv:2510.03342, 2025 — Motion Transfer와 행동 전의 생각.
