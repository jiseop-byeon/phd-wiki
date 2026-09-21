---
title: 4. Vision–Language–Action
tags: [deep-learning, vla, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Specify a VLA by observation, instruction, action representation, horizon, objective, control interface, and closed-loop evidence, and sweep the chunk length on D4."
mastery-when: "Raise when policy architecture, action representation, data mixture, or adaptation is the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> Object **D4** from [[03-deep-learning/lab-objects|0. Lab Objects]] · [[02-foundations/lab-kernel|0.65 Lab Kernel]], because this page is Tier A · [[03-deep-learning/vlm/index|3. VLM]], [[02-foundations/rl-basics|7. RL §6]], [[04-robotics/robot-systems-deployment|10. Robot Systems]], and [[04-robotics/teleoperation-demonstration|12. Teleoperation]].
> [[03-deep-learning/lab-objects|0. Lab Objects]]의 대상 **D4** · 이 페이지는 Tier A이므로 [[02-foundations/lab-kernel|0.65 Lab Kernel]] · [[03-deep-learning/vlm/index|3. VLM]], [[02-foundations/rl-basics|7. RL §6]], [[04-robotics/robot-systems-deployment|10. Robot Systems]], [[04-robotics/teleoperation-demonstration|12. Teleoperation]].

## English

*Stands on the VLM encoder of [[03-deep-learning/vlm/index|3. VLM]] and the rate budget of [[04-robotics/robot-systems-deployment|10. Robot Systems]]. First use of object **D4**.*

> [!note] First pass
> Read the running object, the worked case, §§1–3, and problems 1–2. Return to §4 when a paper reports a success rate, and to §5 when one changes its chunk length.

### Running object · 이 페이지의 대상

**D4** from [[03-deep-learning/lab-objects|0. Lab Objects]], at the numbers that page freezes. At time $t$, **D4** receives image features $o_t$, instruction $l=$ "move left, then down," and predicts a chunk $a_{t:t+2}$ of three 2-D end-effector deltas. The robot executes only the first $k$ actions before observing again. Write the interface before the architecture:

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

The instruction is not decoration here: "left, then down" *is* the axis order the policy plans in, which is why the frozen chunk moves in $x$ twice and then in $y$ once.

*Scope: this page teaches the interface between a language-conditioned policy and a robot — action representation, the behaviour-cloning objective, how long a chunk may be committed, and what a reported success rate does and does not prove. It does not teach the vision–language encoder that produces $o_t$, which is [[03-deep-learning/vlm/index|3. VLM]]; nor how a pretrained backbone is fine-tuned to a new robot, in full or with LoRA, which is [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §8]]; nor the generative head that turns multimodal demonstrations into an action distribution, which is [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]; nor the controller that turns a delta into a torque, which is [[04-robotics/force-compliance-control|11. Force & Compliance Control]]; nor where demonstrations come from, which is [[04-robotics/teleoperation-demonstration|12. Teleoperation]].*

### Homework diagram · 과제가 그릴 그림

One closed loop, and the problem set asks for exactly this one. The figure is the worked case on the catalog numbers, with the loop unrolled underneath for $k=3$.

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

Four things the drawing has to get right, each of which is a claim about the system.
**Two clocks, not one.** Label the policy edge with $t_{\mathrm{inf}}=100\,\mathrm{ms}$ and the controller edge with $\Delta t=50\,\mathrm{ms}$. A single rate on the loop is the most common wrong drawing, and every latency number on this page comes from the two being different.
**The buffer as a box with a length.** Draw the chunk buffer holding $k$ actions and mark that it is refilled only when it empties, from an observation taken $m=2$ steps earlier, while its last $m$ actions are still to run. That box is where the open-loop interval lives.
**The observation edge carries an age.** Write $n-m$ on it, not $n$. The action leaving the buffer at step $n$ was computed from a scene that is $m+(n\bmod k)$ steps old.
**No arrow from the buffer to the scene.** The robot changes the world; the buffered plan does not. A loop drawn with that arrow has assumed the model's prediction is the world, which is the error §4 is about.

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

If D4 predicts $(0.02,0)$ three times in metres but the low-level interface interprets centimetres, the intended 6 cm motion becomes 0.06 cm. Representation errors are physical errors.

### 2. Behavior cloning and multimodality

For continuous demonstrations, a simple objective is

$$L_{\mathrm{BC}}=\frac1H\sum_{h=0}^{H-1}\|a_{t+h}-\hat a_{t+h}\|_2^2.$$

If equally valid demonstrations pass left and right of an obstacle, their MSE mean may go through it. On D4, two demonstrations at one state are $a=(-1,0)$ and $a=(1,0)$. The MSE-optimal deterministic action is their mean $(0,0)$: neither demonstrated mode, and a collision if the obstacle sits at the origin of the local action frame. Discrete tokens, mixture models, diffusion, and flow policies are alternative output distributions; they do not remove the need for good demonstrations and closed-loop recovery.

The word doing the work in that paragraph is the objective's name, and the name has three conditions that papers drop one at a time.

> **Behaviour cloning, defined.** **Behaviour cloning** is a *training objective* — supervised regression or classification of the demonstrator's action given the observation — not an architecture, not a policy class, and not "imitation learning" in general. Three defining conditions. The data are **(observation, action) pairs produced by a demonstrator**, so the label is an action and not a return. The loss is a **supervised discrepancy on the action alone**, with no reward signal and no environment interaction while training. And the expectation is taken **under the demonstrator's state distribution**, not the learner's — the condition that makes it a distribution-shift problem rather than ordinary regression.
>
> $$\theta^\star=\arg\min_\theta\ \mathbb E_{(o,a)\sim\mathcal D_{\text{demo}}}\big[\ell\big(a,\pi_\theta(o)\big)\big]$$
>
> where $\mathcal D_{\text{demo}}$ is the demonstration set, $\ell$ the per-action loss (squared error for continuous actions, cross-entropy for tokenized ones) and $\pi_\theta$ the policy — and the subscript on the expectation is the whole difficulty, because at deployment the states are drawn from $\pi_\theta$'s own visits and nothing in this objective has looked at those.
>
> - **Example**: fitting D4's three deltas to the catalog chunk under squared error. The loss is computable from logged data alone, which is exactly why the method scales to teleoperated datasets.
> - **Non-example**: DAgger and any method that queries the expert on states the *learner* reached. It keeps the supervised loss but replaces condition three, which is why it is a different algorithm with a different data-collection cost, not a tweak.
> - **Non-example**: offline RL on the same demonstration file. Same bytes, but it uses reward and a value estimate, so condition two fails and its failure modes are value-function failures rather than compounding-error ones.
> - **Why it matters**: the two-mode mean $(0,0)$ above is not a bug in the fit — it is the exact minimizer under condition two. Low validation loss on demonstrator states therefore predicts closed-loop success only when the policy stays on those states, which is the claim §4 asks papers to separate from the loss curve.

### 3. Chunking trades smoothness against feedback

Long chunks reduce compounding autoregressive calls and can preserve coordinated motion, but they delay correction. If inference takes 100 ms and the robot executes 10 actions at 20 Hz, a full open-loop chunk lasts 0.5 s. Receding execution—predict 10, execute 2, observe again—restores feedback at extra compute cost. What one autoregressive call is inside the model, a causally masked decoder emitting one token at a time with a KV cache that spares each step from rerunning the prefix, is [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer §3 and §7]].

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
> - **Why it matters**: $k$ is the only knob that appears on both sides of the trade — it multiplies the reaction latency $\ell(k)$ and it divides the number of independent perception draws per second, so smoothness and responsiveness cannot be tuned separately. §5 is that sentence as a table.

### 4. What VLA evidence proves

Separate semantic generalization (choosing the relevant object), motor competence (executing contact-rich motion), embodiment transfer, and recovery. Success rate must define episode, reset, intervention, tolerance, and environment variation. An impressive video is a sample, not an estimator.

Read [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/act|ACT]], and [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] in that order before newer generalist policies.

### 5. The chunk-length sweep

The lab is the homework diagram with one knob. The episode is 3 s at 20 Hz; the target sits at $g=(-0.04,-0.02)$ until control step $20$ and then moves to $(-0.04,+0.02)$, which is a scene change the policy can only learn about through a new observation. Perception jitter is a frozen sine pair rather than a random draw, so the table below is identical on every machine.

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
    print(f"{k:>3} {k*dt >= t_inf!s:>6} {(m+k-1)*dt:>5.2f} {travel*100:>7.2f} "
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

**Travel falls by a factor of 3.3 across the column**, 31.30 cm down to 9.38 cm against a task that needs 10 cm. Replanning every step spends more than three times the necessary motion re-deciding, which on hardware is wear, heat, and audible noise, and none of it appears in an offline action MSE.

**The latency column is the price, and it is linear in $k$:** 100, 100, 200, 200, 250, 500, 1000 ms, matching $\ell(k)$ from the worked case row for row — the `assert` in the listing is that check. A target that moves once per second is tracked by $k\le5$ and missed entirely by $k=20$.

**One number in the table is not part of the trend.** Travel at $k=5$ (14.83 cm) is higher than at $k=4$ (13.19 cm). The jitter is a fixed sequence, so where the chunk boundaries land inside it matters at the 10% level; the factor of 3.3 across the whole column is the effect, and a 12% difference between neighbours is phase. A paper reporting the second kind of difference as a result owes you several seeds.

The design conclusion for this robot: $k$ between 3 and 5 — a commitment of 0.15–0.25 s — removes every reversal and more than half the wasted travel while keeping reaction within 250 ms. Going further to $k=20$ saves a further 5.5 cm of travel and costs three quarters of a second of blindness, which is only a good trade if nothing in the scene moves.

### After reading

For any VLA, fill one row containing observation, language, action space/frame/rate, horizon $H$, executed stride $k$, training data/objective, controller, replanning, and evidence ladder. If the paper gives $H$ but not $k$, the row is incomplete and so is its latency claim.

### Self-check

1. D4's interface accepts $a_{\max}=0.02\,\mathrm{m}$ per step at 20 Hz. What is the fastest tool speed this action representation can express, and what happens to a demonstration recorded at twice that speed?
2. A policy reports $H=16$ and 5 Hz inference. What is the longest open-loop interval consistent with that, and what extra number do you need to pin it down?
3. Why does the $k=2$ row of §5 have *more* reversals than $k=1$, although its chunk is longer?
4. A lab replaces the MSE head with a mixture of two Gaussians and the offline action error gets worse. Give a reading of that result under which the policy improved.
5. Which of D4's frozen numbers would have to change for the axis-at-a-time plan to cost the same travel as a straight line?

> [!tip]- Answers
> 1. $a_{\max}/\Delta t=0.02/0.05=0.4\,\mathrm{m/s}$. A demonstration at $0.8\,\mathrm{m/s}$ cannot be represented: every label saturates at the clip, so the cloned policy is systematically slow and the error is invisible in a per-step loss computed *after* clipping. Units and limits are part of the label, not of the deployment.
> 2. $t_{\mathrm{inf}}=0.2\,\mathrm{s}$, and the open-loop interval is $k$ actions long, not $H$: anything from $k=H=16$ down to the smallest schedulable $k=\lceil t_{\mathrm{inf}}/\Delta t\rceil$. Without the control period $\Delta t$ and the executed stride $k$ the latency is unknown — that is why the After-reading row asks for both.
> 3. Reversals are counted per step, and both rows are in the regime where a fresh, independently jittered plan arrives faster than the tool can finish a 2 cm move. Which of the two counts more depends on where the boundaries land in the frozen jitter sequence. The result to quote is the threshold at $k=3$, not the difference between 6 and 10.
> 4. Offline error is measured against individual demonstrated actions, and the MSE head minimizes it by predicting the mean of modes. A mixture that puts half its mass on each of $(-1,0)$ and $(1,0)$ has a *higher* average distance to any single label while being the only one of the two that ever outputs a demonstrated action. The evidence that settles it is closed-loop success, not the loss.
> 5. The target. The travel penalty is $\lVert g\rVert_1/\lVert g\rVert_2$, so it is $1$ only when the target lies on an axis: $g=(-0.06,0)$ would cost the same 6 cm by either plan. No change to $a_{\max}$, $\delta$, or the rates removes it, because it is a property of the instruction's axis order and the target direction.

### Problem set · 과제

Tier A. Using **D4** from [[03-deep-learning/lab-objects|0. Lab Objects]], this page, and [[02-foundations/lab-kernel|0.65 Lab Kernel]]. Original object and original problems — change the knobs in §5's listing; do not rewrite the loop. State the tier in your answer sheet.

1. **Draw.** The closed loop of the homework diagram, with the two clocks labelled ($\Delta t$ on the controller edge, $t_{\mathrm{inf}}$ on the policy edge), the chunk buffer drawn as a box of length $k$, and the observation edge annotated with its age. Mark on your drawing the one edge that does **not** exist, and say in a sentence what believing in it would mean.
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

> [!tip]- Solutions
> 1. Scene → observation (aged $n-m$) → policy ($t_{\mathrm{inf}}$) → chunk buffer (length $k$) → controller ($\Delta t$) → robot → scene, with the refill edge from the buffer back to the observation closing only every $k$ steps. The edge that does not exist is buffer → scene: the plan does not move the world, only the executed action does. Drawing it is assuming the prediction is the state, which is how an open-loop chunk gets reported as if it had been verified.
> 2. (a) $\Delta t=0.02\,\mathrm{s}$, so $m=\lceil 0.10/0.02\rceil=5$ — the faster controller *raised* the minimum chunk from 2 steps to 5. (b) $(m+k-1)\Delta t=(5+4)\times0.02=0.18\,\mathrm{s}$, against $0.30\,\mathrm{s}$ at 20 Hz. (c) The change is now at step $n_j=50$; $k=5$: $\lceil 55/5\rceil=11$, boundary 55, $\ell=5\times0.02=0.10\,\mathrm{s}$; $k=20$: $\lceil55/20\rceil=3$, boundary 60, $\ell=10\times0.02=0.20\,\mathrm{s}$. (d) At equal $k$ the faster controller cut latency (0.25 → 0.10 s at $k=5$) and smoothed the motion, but it bought nothing against the inference clock: the shortest committed interval is still $t_{\mathrm{inf}}=0.10\,\mathrm{s}$ of motion, now spelled as 5 actions instead of 2.
> 3. Blanks: `return g_after if obs < njump2 else g_before` and `src[n] >= e`. Running it: $k=2$ gives 36.22 cm, 9 reversals, lags $0.10/0.10\,\mathrm{s}$; $k=3$ gives 28.78 cm, 0, $0.20/0.10$; $k=5$ gives 20.60 cm, 0, $0.25/0.25$; $k=10$ gives 14.10 cm, 0, $0.50/0.50$; $k=20$ gives 13.90 cm, 0, $1.00/1.00$. The changes are $1.00\,\mathrm{s}$ apart, so $k=20$'s reaction arrives exactly as the next change happens — it never acts on a target that is still there — and the largest $k$ that still reacts in time is **10**. Two things are worth saying about the last two rows. Travel has saturated: 14.10 against 13.90 cm is a 1.4% gain for twice the blindness, and the ideal is 14 cm, so $k=10$ is already spending essentially nothing on re-deciding. And the smoothness column stopped paying at $k=3$. Past that point a longer chunk is buying a quantity the robot has already bought, with latency it cannot get back.

## 한국어

*[[03-deep-learning/vlm/index|3. VLM]]의 인코더와 [[04-robotics/robot-systems-deployment|10. Robot Systems]]의 주기 예산 위에 선다. 대상 **D4**를 처음 쓴다.*

> [!note] 처음이라면
> 대상, 계산, §1–3, 문제 1–2를 먼저 한다. 논문이 성공률을 보고하면 §4로, chunk 길이를 바꾸면 §5로 돌아온다.

### 이 페이지의 대상 · Running object

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D4**를 그 페이지가 고정한 숫자 그대로 쓴다. 시간 $t$에 **D4**는 image feature $o_t$와 "왼쪽으로 간 다음 아래로"라는 instruction $l$을 받고, 2차원 말단 delta 행동 세 개의 chunk를 예측한다. architecture보다 먼저 $\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l)$와 $a_i=(\Delta x_i,\Delta y_i)$라는 interface를 쓴다.

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

여기서 instruction은 장식이 아니다. "왼쪽으로 간 다음 아래로"가 정책이 계획하는 축 순서 자체이고, 그래서 고정된 chunk가 $x$로 두 번, $y$로 한 번 움직인다.

*범위: 이 페이지는 언어 조건 정책과 로봇 사이의 interface를 가르친다 — 행동 표현, behaviour cloning 목적함수, chunk를 얼마나 오래 확정해도 되는지, 보고된 success rate가 무엇을 증명하고 무엇을 증명하지 않는지. $o_t$를 만드는 vision–language 인코더는 가르치지 않는다. 그것은 [[03-deep-learning/vlm/index|3. VLM]]이다. 사전학습된 backbone을 새 로봇에 맞게 전체로든 LoRA로든 파인튜닝하는 법도 아니다. 그것은 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §8]]이다. 다봉 시연을 행동 분포로 바꾸는 생성 head도 아니다. 그것은 [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]다. delta를 토크로 바꾸는 제어기도 아니다. 그것은 [[04-robotics/force-compliance-control|11. 힘·컴플라이언스 제어]]다. 시연이 어디서 오는지도 아니다. 그것은 [[04-robotics/teleoperation-demonstration|12. 원격조작]]이다.*

### 과제가 그릴 그림 · Homework diagram

폐루프 하나, 과제가 요구하는 것이 정확히 이 그림이다. 그림은 카탈로그 숫자로 그린 계산 절이고, 아래에 $k=3$으로 루프를 펼쳐 놓았다.

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

그림이 맞혀야 할 것이 넷이고, 각각이 시스템에 대한 주장이다.
**시계는 하나가 아니라 둘.** 정책 변에 $t_{\mathrm{inf}}=100\,\mathrm{ms}$, 제어기 변에 $\Delta t=50\,\mathrm{ms}$를 적는다. 루프에 주기를 하나만 적는 것이 가장 흔한 오답이고, 이 페이지의 지연 숫자는 전부 둘이 다르다는 데서 나온다.
**버퍼는 길이를 가진 상자.** chunk 버퍼가 행동 $k$개를 담고 있고, 버퍼는 비었을 때만 다시 채워지지만 그 채움이 쓰는 관측은 $m=2$ 스텝 앞, 마지막 행동 $m$개가 아직 남아 있을 때 찍힌다고 표시한다. 개루프 구간이 사는 자리가 그 상자다.
**관측 변에는 나이가 붙는다.** $n$이 아니라 $n-m$을 적는다. 스텝 $n$에 버퍼에서 나가는 행동은 $m+(n\bmod k)$ 스텝 묵은 장면에서 계산됐다.
**버퍼에서 장면으로 가는 화살표는 없다.** 세계를 바꾸는 것은 로봇이지 버퍼 속 계획이 아니다. 그 화살표를 그린 루프는 예측을 곧 세계로 가정한 것이고, §4가 다루는 오류가 그것이다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. 과제는 이 그림을 그리고, 지연을 유도하고, 손잡이 하나를 쓸어 보라고 한다. 카탈로그 숫자로 여기서 먼저 하면 과제는 손잡이를 바꾸는 일이지 첫 유도가 아니다.

**chunk 자체.** 정책은 상상 속 도구를 관측된 위치에서 관측된 목표까지 한 번에 한 축씩, 한 스텝에 $a_{\max}$를 넘지 않게 걷게 한다. $p_0=(0,0)$에서 $g=(-0.04,-0.02)$로 가면 $r_1=(-0.04,-0.02)$, $|r_{1x}|=0.04>\delta$이므로 $a_1=(-0.02,0)$이다. 다음 $r_2=(-0.02,-0.02)$도 $|r_{2x}|=0.02>\delta$이므로 $a_2=(-0.02,0)$, 그다음 $r_3=(0,-0.02)$는 $|r_{3x}|=0<\delta$라 축을 바꿔 $a_3=(0,-0.02)$다. 이것이 카탈로그 chunk다. 경로 길이는 $3\times0.02=0.06\,\mathrm{m}$인데 알짜 변위는 $\sqrt{0.04^2+0.02^2}=0.0447\,\mathrm{m}$뿐이므로, instruction의 축 순서가 직선보다 $34\%$ 더 걷게 만든다. 표현 선택이 미터 단위 비용을 갖는다는 §1이 숫자 하나로 여기 있다.

**타이밍, chunk 길이가 나오는 자리.** 추론에 $t_{\mathrm{inf}}$가 들고 제어기는 $\Delta t$마다 행동을 하나씩 쓰므로, 행동 $k$개의 chunk는 $k\Delta t$ 동안 버티고 다음 chunk는 $k\Delta t\ge t_{\mathrm{inf}}$일 때만 제때 준비된다. 즉 $k\ge\lceil t_{\mathrm{inf}}/\Delta t\rceil=\lceil 0.10/0.05\rceil=2=m$이다. 행동이 떨어진 제어기는 멈추거나 붙들고 있어야 하기 때문이다. **실행되는 행동의 나이.** 스텝 $[jk,(j+1)k)$를 덮는 chunk는 스텝 $jk-m$의 장면에서 계산됐으므로 스텝 $n$에 나가는 행동은 $m+(n\bmod k)$ 스텝 묵었고, 최악은 $(m+k-1)\Delta t$다. 카탈로그 $k=3$이면 $(2+3-1)\times0.05=0.20\,\mathrm{s}$다.

**반응 지연.** 장면이 제어 스텝 $n_j$에서 바뀌면 그것을 알 수 있는 첫 행동은 관측 스텝이 $n_j$ 이상인 첫 chunk, 즉 $jk\ge n_j+m$인 첫 경계에 속한다. 그래서 $\ell(k)=(k\lceil(n_j+m)/k\rceil-n_j)\Delta t$다. $n_j=20$, $k=3$이면 $\lceil22/3\rceil=8$이라 경계는 스텝 24, $\ell=0.20\,\mathrm{s}$다. $k=20$이면 $\lceil22/20\rceil=2$, 경계는 스텝 40, $\ell=1.00\,\mathrm{s}$다. §5는 루프를 돌려 이 숫자를 흔적에서 다시 얻는다. 대수와 코드가 맞는지 확인하는 것이 그 검사다.

**같은 대상 위의 목적함수.** D4의 한 상태에서 똑같이 좋은 시연 둘이 정규화 단위로 $a=(-1,0)$과 $(1,0)$이면 MSE-optimal 결정 예측은 평균 $(0,0)$이고, 어느 시연 mode도 아니다. 시연이 $(-1,0)$, $(-1,0)$, $(1,0)$이면 $(-1/3,0)$이다. 더 잦은 mode 쪽으로 기울었을 뿐 여전히 시연된 행동이 아니다. 이것이 §2이고, 출력 분포가 세부가 아니라 설계 선택인 이유다.

### 1. 행동 표현도 방법이다

관절 위치·속도·torque, 말단 pose·delta pose, gripper, action token은 물리 가정이 다르다. 단위·frame·rate·horizon·하위 controller가 없으면 "행동 출력"은 불완전하다.

D4가 $(0.02,0)$을 미터로 세 번 예측했는데 하위 interface가 센티미터로 해석하면, 의도한 6 cm가 0.06 cm가 된다. 표현 오차는 물리 오차다.

### 2. Behavior cloning과 다봉성

$L_{BC}=H^{-1}\sum_h\|a_{t+h}-\hat a_{t+h}\|^2$. 장애물의 좌우로 지나가는 시연을 평균하면 장애물 중앙으로 갈 수 있다. D4의 한 상태에서 시연이 $(-1,0)$과 $(1,0)$이면 MSE-optimal 결정 행동은 평균 $(0,0)$이다. 어느 시연 mode도 아니고, 장애물이 국소 행동 원점에 있으면 충돌한다. token·mixture·diffusion·flow는 출력 분포의 대안이지, 나쁜 시연과 recovery 문제를 없애지 않는다.

저 문단에서 일하는 단어는 목적함수의 이름이고, 그 이름에는 논문들이 하나씩 떨어뜨리는 조건 셋이 있다.

> **Behaviour cloning의 정의.** **Behaviour cloning**은 *학습 목적함수*다. 관측이 주어졌을 때 시연자의 행동을 지도 회귀 또는 분류로 맞추는 것이지 architecture도, 정책 계열도, imitation learning 일반도 아니다. 정의 조건 셋. 자료는 **시연자가 만든 (관측, 행동) 쌍**이므로 label이 return이 아니라 행동이다. 손실은 **행동에만 걸리는 지도 오차**이고, 학습 중에 reward도 환경 상호작용도 없다. 그리고 기대값은 **시연자의 상태 분포**에서 취한다. 학습된 정책의 분포가 아니다. 이 조건이 평범한 회귀가 아니라 분포 이동 문제로 만든다.
>
> $$\theta^\star=\arg\min_\theta\ \mathbb E_{(o,a)\sim\mathcal D_{\text{demo}}}\big[\ell\big(a,\pi_\theta(o)\big)\big]$$
>
> $\mathcal D_{\text{demo}}$는 시연 집합, $\ell$은 행동당 손실(연속 행동이면 제곱오차, token이면 cross-entropy), $\pi_\theta$는 정책이다. 기대값의 아래첨자가 난점 전부인데, 배포 시 상태는 $\pi_\theta$ 자신이 방문해 뽑히고 이 목적함수는 그 상태를 한 번도 본 적이 없기 때문이다.
>
> - **예**: D4의 delta 세 개를 카탈로그 chunk에 제곱오차로 맞추기. 손실이 기록된 자료만으로 계산되고, 그래서 원격조작 데이터셋으로 규모를 키울 수 있다.
> - **비예**: DAgger를 비롯해 *학습자*가 도달한 상태에서 전문가에게 다시 묻는 모든 방법. 지도 손실은 그대로 두고 셋째 조건을 바꾸므로, 조정이 아니라 자료 수집 비용이 다른 별개 알고리즘이다.
> - **비예**: 같은 시연 파일에 offline RL. 바이트는 같지만 reward와 가치 추정을 쓰므로 둘째 조건이 깨지고, 실패 양상도 누적 오차가 아니라 가치함수의 실패다.
> - **왜 중요한가**: 위의 두 mode 평균 $(0,0)$은 적합 실패가 아니라 둘째 조건 아래의 정확한 최소점이다. 그러므로 시연자 상태에서의 낮은 validation loss는 정책이 그 상태 위에 머무를 때만 폐루프 성공을 예측하고, 그 주장을 loss 곡선과 분리하라는 것이 §4의 요구다.

### 3. Chunking의 교환

긴 chunk는 호출 횟수와 흔들림을 줄이지만 보정을 늦춘다. 추론이 100 ms이고 로봇이 20 Hz로 행동 10개를 실행하면 전체 open-loop chunk는 0.5초다. 10개를 예측하고 2개만 실행한 뒤 다시 관측하면 feedback을 회복하지만 계산량이 늘어난다. 모델 안에서 자기회귀 호출 한 번이 무엇인지, 곧 토큰을 하나씩 내는 인과 마스크 디코더와 매 스텝이 앞부분을 다시 돌리지 않게 하는 KV 캐시는 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer §3과 §7]]에 있다.

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
> - **왜 중요한가**: $k$는 거래의 양쪽에 동시에 나타나는 유일한 손잡이다. 반응 지연 $\ell(k)$에 곱해지고, 초당 독립적인 지각 표본 수를 나눈다. 그래서 매끄러움과 반응성을 따로 조율할 수 없다. §5가 그 문장을 표로 만든 것이다.

### 4. 증거 읽기

semantic generalization, motor competence, embodiment transfer, recovery를 나눈다. success rate에는 episode·reset·intervention·tolerance·환경 변동 정의가 필요하다.

### 5. Chunk 길이 쓸기

랩은 과제 그림에 손잡이 하나를 붙인 것이다. episode는 20 Hz로 3초이고, 목표는 제어 스텝 20까지 $g=(-0.04,-0.02)$에 있다가 $(-0.04,+0.02)$로 옮겨 간다. 정책은 새 관측을 통해서만 이 변화를 알 수 있다. 지각 흔들림은 난수가 아니라 고정된 sine 쌍이므로 아래 표는 어떤 기계에서도 같다. 코드는 영어 절에 한 번만 싣는다.

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

**이동거리는 열 전체에서 3.3배 줄어든다.** 31.30 cm에서 9.38 cm로, 과제가 필요로 하는 10 cm를 상대로. 매 스텝 다시 계획하면 필요한 움직임의 세 배 넘게를 다시 결정하는 데 쓰고, 하드웨어에서 그것은 마모와 발열과 소음인데 offline action MSE에는 하나도 나타나지 않는다.

**지연 열이 대가이고 $k$에 선형이다.** 100, 100, 200, 200, 250, 500, 1000 ms로, 계산 절의 $\ell(k)$와 행마다 일치한다. 코드의 `assert`가 그 검사다. 1초에 한 번 움직이는 목표는 $k\le5$면 추종되고 $k=20$이면 통째로 놓친다.

**표의 숫자 하나는 추세가 아니다.** $k=5$의 이동거리 14.83 cm가 $k=4$의 13.19 cm보다 크다. 흔들림이 고정된 수열이라 chunk 경계가 그 안 어디에 떨어지는지가 10% 수준에서 영향을 준다. 열 전체의 3.3배가 효과이고 이웃 사이의 12%는 위상이다. 두 번째 종류의 차이를 결과로 보고하는 논문에는 seed를 여러 개 요구해야 한다.

이 로봇의 설계 결론: $k$가 3에서 5 사이 — 확정 구간 0.15–0.25초 — 이면 반전이 전부 사라지고 낭비된 이동의 절반 이상이 사라지며 반응은 250 ms 안에 머문다. $k=20$까지 가면 이동거리를 $5.5\,\mathrm{cm}$ 더 아끼는 대신 0.75초의 눈감음을 치르는데, 장면이 전혀 움직이지 않을 때만 좋은 거래다.

### 읽고 나면

VLA 하나를 observation·language·action/frame/rate·horizon $H$·실행 stride $k$·data/objective·controller·replanning·evidence로 한 줄에 명세할 수 있다. 논문이 $H$는 주고 $k$를 주지 않았다면 그 줄은 불완전하고 지연 주장도 불완전하다.

### 스스로 점검

1. D4의 interface는 20 Hz에서 스텝당 $a_{\max}=0.02\,\mathrm{m}$를 받는다. 이 행동 표현이 나타낼 수 있는 가장 빠른 도구 속도는 얼마이고, 그 두 배로 기록된 시연은 어떻게 되는가?
2. 어떤 정책이 $H=16$, 추론 5 Hz라고 보고했다. 이와 모순되지 않는 가장 긴 개루프 구간은 얼마이고, 확정하려면 어떤 숫자가 더 필요한가?
3. §5에서 $k=2$의 반전이 $k=1$보다 *많은* 이유는 무엇인가? chunk는 더 긴데도.
4. MSE head를 2성분 가우시안 혼합으로 바꿨더니 offline action error가 나빠졌다. 그런데도 정책이 좋아졌다고 읽을 수 있는 독법을 대라.
5. 축을 하나씩 쓰는 계획이 직선과 같은 이동거리를 쓰려면 D4의 고정 숫자 중 무엇이 바뀌어야 하는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $a_{\max}/\Delta t=0.02/0.05=0.4\,\mathrm{m/s}$. $0.8\,\mathrm{m/s}$의 시연은 표현되지 않는다. 모든 label이 클립에 걸리므로 복제된 정책은 체계적으로 느리고, 클립 *이후*에 계산한 스텝별 손실에는 그 오차가 보이지 않는다. 단위와 한계는 배포가 아니라 label의 일부다.
> 2. $t_{\mathrm{inf}}=0.2\,\mathrm{s}$이고 개루프 구간의 길이는 $H$가 아니라 행동 $k$개다. $k=H=16$부터 스케줄 가능한 최소 $k=\lceil t_{\mathrm{inf}}/\Delta t\rceil$까지 무엇이든 될 수 있다. 제어 주기 $\Delta t$와 실행 stride $k$가 없으면 지연은 미정이고, 그래서 읽고 나면 줄이 둘 다를 요구한다.
> 3. 반전은 스텝마다 세고, 두 행 모두 새로 흔들린 계획이 도구가 2 cm를 끝내기도 전에 도착하는 영역에 있다. 둘 중 어느 쪽이 더 많은지는 경계가 고정된 흔들림 수열의 어디에 떨어지는지가 정한다. 인용할 결과는 $k=3$의 문턱이지 6과 10의 차이가 아니다.
> 4. offline error는 개별 시연 행동을 상대로 재고, MSE head는 mode들의 평균을 내놓아 그것을 최소화한다. $(-1,0)$과 $(1,0)$에 절반씩 질량을 둔 혼합은 어떤 단일 label과의 평균 거리가 *더 크면서*, 둘 중 시연된 행동을 실제로 내놓는 유일한 쪽이다. 판정하는 증거는 loss가 아니라 폐루프 성공이다.
> 5. 목표다. 이동거리 벌점은 $\lVert g\rVert_1/\lVert g\rVert_2$이므로 목표가 축 위에 있을 때만 1이다. $g=(-0.06,0)$이면 어느 계획이든 같은 6 cm다. $a_{\max}$나 $\delta$나 주기를 바꿔도 없어지지 않는다. instruction의 축 순서와 목표 방향의 성질이기 때문이다.

### 과제 · Problem set

Tier A. [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D4**, 이 페이지, [[02-foundations/lab-kernel|0.65 Lab Kernel]]. 영어 절 §5의 손잡이를 바꿔라. 루프를 다시 쓰지 마라. 답안에 tier를 명시하라.

1. **그리기.** 과제 그림의 폐루프. 시계 둘을 표시하고(제어기 변에 $\Delta t$, 정책 변에 $t_{\mathrm{inf}}$), chunk 버퍼를 길이 $k$인 상자로 그리고, 관측 변에 나이를 적는다. 존재하지 **않는** 변 하나를 표시하고, 그것을 믿으면 무슨 뜻이 되는지 한 문장으로 쓴다.
2. **유도.** 제어기를 $50\,\mathrm{Hz}$로 다시 올리고 추론은 여전히 $100\,\mathrm{ms}$다. (a) 스케줄 가능한 최소 chunk $m$. (b) $k=5$의 최악 행동 나이. (c) $t=1.0\,\mathrm{s}$의 장면 변화에 대해 $k=5$와 $k=20$의 $\ell(k)$. (d) (c)를 §5의 20 Hz 숫자와 비교해 더 빠른 제어기가 무엇을 사고 무엇을 사지 못했는지 한 문장으로.
3. **실행.** 영어 절 패치의 `?`를 채우고 §5의 쓸기를 다시 돌린다. 이제 목표가 *두 번* 움직인다. 스텝 20에 위로, 스텝 40에 다시 아래로, 1초 간격이다. 충분히 긴 chunk는 한 사건 내내 앞 사건을 쫓는 데 쓸 수 있다. $k\in\{2,3,5,10,20\}$에 대해 이동거리·반전·두 변화 각각의 지연을 보고하고, 어떤 변화에 대한 반응이 *다음* 변화보다 먼저 도착하는 가장 큰 $k$를 말한다. 이 episode의 이상적 이동거리는 14 cm다(나갈 때 6, 위로 4, 아래로 4).

> [!tip]- 정답 · Solutions
> 1. 장면 → 관측(나이 $n-m$) → 정책($t_{\mathrm{inf}}$) → chunk 버퍼(길이 $k$) → 제어기($\Delta t$) → 로봇 → 장면. 버퍼에서 관측으로 돌아가는 변은 $k$ 스텝마다만 닫힌다. 없는 변은 버퍼 → 장면이다. 계획이 세계를 움직이지 않고 실행된 행동만 움직인다. 그 변을 그리는 것은 예측을 상태로 가정하는 것이고, 개루프 chunk가 검증된 것처럼 보고되는 경로가 그것이다.
> 2. (a) $\Delta t=0.02\,\mathrm{s}$이므로 $m=\lceil 0.10/0.02\rceil=5$. 더 빠른 제어기가 최소 chunk를 2에서 5로 *올렸다*. (b) $(5+4)\times0.02=0.18\,\mathrm{s}$, 20 Hz의 $0.30\,\mathrm{s}$와 비교된다. (c) 변화는 이제 스텝 $n_j=50$이다. $k=5$: $\lceil55/5\rceil=11$, 경계 55, $\ell=0.10\,\mathrm{s}$. $k=20$: $\lceil55/20\rceil=3$, 경계 60, $\ell=0.20\,\mathrm{s}$. (d) 같은 $k$에서 더 빠른 제어기는 지연을 줄이고($k=5$에서 0.25 → 0.10초) 움직임을 매끄럽게 했지만, 추론 시계에 대해서는 아무것도 사지 못했다. 가장 짧은 확정 구간은 여전히 $t_{\mathrm{inf}}=0.10\,\mathrm{s}$의 움직임이고, 이제 행동 2개가 아니라 5개로 적힐 뿐이다.
> 3. 빈칸은 `return g_after if obs < njump2 else g_before`와 `src[n] >= e`다. 돌려 보면 $k=2$는 36.22 cm, 반전 9, 지연 $0.10/0.10\,\mathrm{s}$. $k=3$은 28.78 cm, 0, $0.20/0.10$. $k=5$는 20.60 cm, 0, $0.25/0.25$. $k=10$은 14.10 cm, 0, $0.50/0.50$. $k=20$은 13.90 cm, 0, $1.00/1.00$이다. 변화 간격이 $1.00\,\mathrm{s}$이므로 $k=20$의 반응은 다음 변화와 정확히 동시에 도착한다. 아직 거기 있는 목표에 대해서는 한 번도 움직이지 못한다는 뜻이고, 제때 반응하는 가장 큰 $k$는 **10**이다. 마지막 두 행에서 할 말이 둘이다. 이동거리는 포화했다. 14.10 대 13.90 cm는 눈감는 시간을 두 배로 치르고 1.4%를 얻은 것이고, 이상값이 14 cm이므로 $k=10$은 이미 다시 결정하는 데 사실상 아무것도 쓰지 않는다. 그리고 매끄러움 열은 $k=3$에서 값을 다 치렀다. 그 뒤의 긴 chunk는 로봇이 이미 산 것을 다시 사면서 되돌릴 수 없는 지연을 치른다.
