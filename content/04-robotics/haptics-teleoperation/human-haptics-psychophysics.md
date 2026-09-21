---
title: 24.1 Human Haptics & Psychophysics
tags: [haptics, psychophysics, hri]
study-depth: Working
wiki-support: Working
depth-goal: "Turn a frozen psychometric table into a threshold, a JND, and a Weber fraction on plant P3, and translate a touch claim into a stimulus, receptor/site, task, psychometric measure, and uncertainty statement."
mastery-when: "Master staircase design, psychometric modeling, and multisensory inference when human perception is the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]] — here the handle is a stimulus generator, not a controlled loop. Proportions and their uncertainty from [[02-foundations/probability|3. Probability]]. Nothing else: the arithmetic on this page is linear interpolation.
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3**. 여기서 핸들은 제어 루프가 아니라 자극 발생기다. 비율과 그 불확실성은 [[02-foundations/probability|3. 확률]]. 그 밖에는 필요 없다. 이 페이지의 계산은 선형 보간이다.

## English

*The perception end of the haptics track. First use of plant **P3** as a stimulus generator rather than as a rendering loop; the loop itself is [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]].*

### Running object · 이 페이지의 대상

Every number on this page comes from one frozen experiment, stated once here and never changed later. **The response counts are illustrative values defined on this page so that the arithmetic is exact. They are nobody's measured data, and no empirical claim may be cited from them.**

**Delivery device: plant P3**, the 1-DoF translating handle of [[02-foundations/lab-plants|0.6 Lab Plants]] — effective mass $m=0.04\,\mathrm{kg}$, damping $b=0.8\,\mathrm{N\cdot s/m}$, hand $k_h=400\,\mathrm{N/m}$, $b_h=8\,\mathrm{N\cdot s/m}$. The handle is the stimulus generator: it pushes the hand along $+x$ with a commanded force, so *the stimulus* on this page is a force in newtons, applied at one grasp point, on one hand. The P3 catalog freezes no amplifier limit — the $2.0\,\mathrm{N}$ saturation in [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]'s problem set is a number invented for that problem — so this experiment adds one assumption of its own: the handle holds any force from $0$ to $6\,\mathrm{N}$ steadily.

**Task: a two-interval, two-alternative forced choice.** Each trial renders the reference force $F_{\text{ref}}=5.00\,\mathrm{N}$ for one second, pauses half a second, renders a comparison force $F_c$ for one second, and asks *which interval pushed harder?* Interval order is randomised and the participant must answer even when unsure.

**Frozen record: six comparison levels, 40 trials each, 240 trials, one participant.**

| $F_c$ (N) | judged stronger | of | $p$ |
|---:|---:|---:|---:|
| 4.40 | 5 | 40 | 0.125 |
| 4.70 | 11 | 40 | 0.275 |
| 5.00 | 19 | 40 | 0.475 |
| 5.30 | 26 | 40 | 0.650 |
| 5.60 | 33 | 40 | 0.825 |
| 5.90 | 37 | 40 | 0.925 |

Here $p$ is the proportion of the 40 trials at that level on which the participant called the *comparison* interval stronger. §5 says what to draw, §6 turns the table into a threshold, a JND, and a Weber fraction, and the problem set repeats the whole exercise at a lower reference force.

### 1. Touch is an active sensing loop

**Cutaneous** cues arise from skin deformation; **kinesthetic/proprioceptive** cues arise from muscles, tendons, joints, and skin stretch during limb motion. Haptic perception combines both with motor commands and often with vision and sound. Passive stimulation asks what a delivered cue evokes; active touch also lets the person choose an exploratory motion. Texture, hardness, temperature, weight, and exact shape invite different exploratory procedures (the stereotyped hand motions people use to probe a property, such as lateral sliding for texture, pressing for hardness, or static contact for temperature), so a device should be evaluated with the movement the target task actually requires.

The common receptor labels are useful but approximate. In the names, SA = slowly adapting (keeps firing during a sustained stimulus) and RA = rapidly adapting (fires mainly when the stimulus changes); type I has a small receptive field and type II a large one.

| Afferent class | Adaptation/field | Especially informative about |
|---|---|---|
| SA-I / Merkel | slow, small field | sustained pressure, edges, coarse form |
| RA-I / Meissner | rapid, small field | low-frequency transients, slip onset |
| SA-II / Ruffini | slow, large field | skin stretch, hand configuration |
| RA-II / Pacinian | rapid, large field | high-frequency vibration and impacts |

Frequency bands overlap and depend on contactor size, site, preload, and waveform. A statement such as “250 Hz is optimal” is incomplete without those conditions.

### 2. Threshold, PSE, and JND

A **psychometric function** maps physical stimulus $x$ to response probability, for example $P(\text{comparison judged stronger}\mid x)$. Its midpoint can define the **point of subjective equality** (PSE). In a two-alternative comparison, one common convention reads the just-noticeable difference (JND) off the curve: $x_{75}$ and $x_{25}$ are the stimulus levels judged stronger 75% and 25% of the time, so half their gap measures how far the stimulus must move from the PSE before judgments shift reliably.

$$\mathrm{JND}=\frac{x_{75}-x_{25}}{2}.$$

This is not a universal definition: yes/no detection, $n$-alternative choice, and fitted functions use different chance levels and threshold criteria. A 50% threshold is meaningful only after the response task is specified.

**The five terms, defined.** Each one is a *convention applied to a curve*, not a property of skin, so each carries its task with it. §6 computes all five on the running object.

- **Two-alternative forced choice (2AFC)** — a *response task*, defined by three conditions: exactly two alternatives are offered, a response is required on every trial, and the experimenter fixes which alternative counts as the reference. *Example*: the two intervals of the running object. *Non-example*: "rate the force from 1 to 7", a rating scale whose midpoint is a criterion the participant chooses rather than a chance level the design fixes. It matters because the number of alternatives fixes chance level — $1/2$ here — and chance level is what makes one value of $p$ a threshold rather than another.
- **Threshold $x_p$** — a *stimulus level*, namely the level at which the response probability equals a criterion $p$ that you name. So "the threshold" without both a $p$ and a task is not yet a quantity, and two papers reporting "the threshold" of the same cue may be reporting different points on the same curve.
- **Point of subjective equality (PSE)** — the *threshold at $p=0.5$* on a comparison curve: the comparison level as likely to be called stronger as weaker. *Non-example*: the reference force. When $\mathrm{PSE}\neq F_{\text{ref}}$ the difference is a constant bias of this participant with this device and this interval order, which is a finding about the pair, not noise to be averaged away.
- **JND** — a *stimulus difference*: half the span between the 25% and 75% thresholds, by the convention in the formula above. It measures the width of the uncertain region, not a step at which perception switches on.
- **Weber fraction $k$** — a *dimensionless ratio*, the JND divided by the reference intensity it was measured at:

$$k=\frac{\mathrm{JND}}{I},$$

where $I$ is the operating-point intensity (the PSE, in §6), so $k$ is the only one of the five that can be compared across operating points, and even then only locally.

**Weber's law** is the local empirical approximation $\Delta I/I\approx k$. It predicts that the absolute increment needed for discrimination grows with the reference intensity. Integrating equal relative increments motivates Fechner's logarithmic scale (perceived magnitude grows roughly with the logarithm of physical intensity), but neither law is exact across all intensities or modalities.

Worked interpretation: if a force JND is 8% near 5 N, a first estimate of a noticeable increment is $0.08(5)=0.4$ N. This does not prove that every participant notices 5.4 N; it describes a criterion-dependent population response near that operating point.

### 3. Choosing an experiment

| Question | Useful method | Main risk |
|---|---|---|
| find an approximate threshold quickly | staircase / adaptive up–down | convergence depends on rule and lapses |
| estimate a full psychometric curve | constant stimuli | many trials; order and fatigue |
| let users match a sensation | adjustment | response and anchoring bias |
| compare two interfaces | within-subject counterbalanced study | carryover and learning |

Measure false alarms as well as hits. Signal-detection analysis separates sensitivity (how well a person can actually tell stimulus from no stimulus) from response criterion (how willing they are to say "yes" when unsure), because a cautious and a liberal participant can have the same sensitivity but very different hit rates. Randomize condition order, include training, predefine exclusions, and record contact force, motion, latency, and task success rather than relying only on preference.

### 4. Multisensory and workload claims

Under particular Gaussian/noise assumptions, two estimates with variances $\sigma_v^2$ and $\sigma_h^2$ combine by precision weighting:

$$\hat x=\frac{\sigma_v^{-2}x_v+\sigma_h^{-2}x_h}{\sigma_v^{-2}+\sigma_h^{-2}}.$$

This is a model, not a universal law of sensory dominance. Reliability, temporal alignment, task relevance, priors, attention, and conflict determine whether cues fuse, compete, or remain separate. Likewise, moving a warning from vision to touch does not automatically reduce workload; representative multitask testing is necessary.

**Worked: the fusion the homework asks.** $\sigma_v=2\,\mathrm{mm}$, $\sigma_h=4\,\mathrm{mm}$ gives weights $4:1$, so $\hat x=\tfrac45 x_v+\tfrac15 x_h$, not vision alone. A force JND of $8\%$ near $5\,\mathrm{N}$ is a *population* increment of $0.4\,\mathrm{N}$; $5.2$ versus $5.0$ is half a JND and does not license “every participant notices.” Detection of a $250\,\mathrm{Hz}$ vibration is not insertion success: the chain is detectability $\to$ action $\to$ outcome.

### 5. Homework diagram

One figure, two panels. The problem set asks for the same figure drawn from a different table, so draw it once here properly.

<svg viewBox="0 0 560 486" style="max-width:100%;height:auto" role="img" aria-label="Panel A traces the stimulus from commanded force through the P3 handle and the hand to the response, with the 1 s, 0.5 s, 1 s trial timeline and the decision criterion living only in the response, and panel B joins the six frozen proportions with straight segments and drops the 0.25, 0.50 and 0.75 crossings to x25 = 4.65, PSE = 5.0429 and x75 = 5.4714 N, with a 2 JND brace of 0.8214 N and the reference 5.00 N marked 43 mN left of the PSE.">
  <text x="10" y="18" font-size="12.5" fill="currentColor">A · where the stimulus comes from</text>
  <rect x="8" y="30" width="92" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="54" y="55.8">commanded</text><text x="54" y="70.2">force F<tspan font-size="11" dy="3">c</tspan></text></g>
  <line x1="103" y1="59" x2="110.5" y2="59" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="117,59 110,62.4 110,55.6" fill="currentColor"/>
  <rect x="120" y="30" width="124" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="182" y="48.5">P3 handle</text><text x="182" y="63">m = 0.04 kg</text><text x="182" y="77.5">b = 0.8 N·s/m</text></g>
  <line x1="247" y1="59" x2="254.5" y2="59" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,59 254,62.4 254,55.6" fill="currentColor"/>
  <rect x="264" y="30" width="124" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="326" y="48.5">hand</text><text x="326" y="63">k<tspan font-size="11" dy="3">h</tspan><tspan dy="-3" dx="4">= 400 N/m</tspan></text><text x="326" y="77.5">b<tspan font-size="11" dy="3">h</tspan><tspan dy="-3" dx="4">= 8 N·s/m</tspan></text></g>
  <line x1="391" y1="59" x2="398.5" y2="59" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="405,59 398,62.4 398,55.6" fill="currentColor"/>
  <rect x="408" y="30" width="144" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="480" y="48.5">response:</text><text x="480" y="63">which interval</text><text x="480" y="77.5">pushed harder?</text><text x="254" y="51">+x</text></g>
  <text x="18" y="104" font-size="11" fill="currentColor" opacity="0.8">one trial</text>
  <rect x="18" y="110" width="110" height="18" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <rect x="128" y="110" width="55" height="18" fill="none" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <rect x="183" y="110" width="110" height="18" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="73" y="123">F<tspan font-size="11" dy="3">ref</tspan><tspan dy="-3" dx="4">= 5.00 N</tspan></text><text x="238" y="123">F<tspan font-size="11" dy="3">c</tspan></text></g>
  <line x1="295" y1="119" x2="305.5" y2="119" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="311,119 305,122 305,116" fill="currentColor"/>
  <text x="315" y="123" font-size="11.5" fill="currentColor">respond</text>
  <g font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8"><text x="73" y="143">1 s</text><text x="155.5" y="143">0.5 s</text><text x="238" y="143">1 s</text></g>
  <line x1="480" y1="90" x2="480" y2="97" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="414" y="110" font-size="11" fill="currentColor">not in the chain:</text>
  <g font-size="11" fill="currentColor" opacity="0.9"><text x="414" y="124">the decision criterion.</text><text x="414" y="138">It lives only in this</text><text x="414" y="152">box, so a threshold</text><text x="414" y="166">needs a stated p.</text></g>
  <line x1="8" y1="172" x2="552" y2="172" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="3 4"/>
  <text x="10" y="196" font-size="12.5" fill="currentColor">B · the curve: proportion judged stronger against comparison force</text>
  <g stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"><line x1="66" y1="402" x2="536" y2="402"/><line x1="66" y1="402" x2="66" y2="222"/><line x1="62" y1="402" x2="66" y2="402"/></g>
  <text x="59" y="406" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0</text>
  <line x1="62" y1="357" x2="66" y2="357" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="361" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0.25</text>
  <line x1="62" y1="312" x2="66" y2="312" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="316" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0.50</text>
  <line x1="62" y1="267" x2="66" y2="267" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="271" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0.75</text>
  <line x1="62" y1="222" x2="66" y2="222" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="226" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">1</text>
  <text x="59" y="212" font-size="12" fill="currentColor" text-anchor="end" opacity="0.9">p</text>
  <line x1="93.6" y1="402" x2="93.6" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="93.6" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">4.4</text>
  <line x1="176.6" y1="402" x2="176.6" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="176.6" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">4.7</text>
  <line x1="259.5" y1="402" x2="259.5" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="259.5" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.0</text>
  <line x1="342.5" y1="402" x2="342.5" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="342.5" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.3</text>
  <line x1="425.4" y1="402" x2="425.4" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="425.4" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.6</text>
  <line x1="508.4" y1="402" x2="508.4" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="508.4" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.9</text>
  <text x="548" y="435" font-size="12" fill="currentColor" text-anchor="end" opacity="0.85">F<tspan font-size="11" dy="3">c</tspan><tspan dy="-3" dx="4.2">(N)</tspan></text>
  <line x1="259.5" y1="222" x2="259.5" y2="394" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" stroke-dasharray="1.5 2.5"/>
  <polygon points="259.5,393.0 254.5,402.0 264.5,402.0" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="259.5" y="216" font-size="12" fill="currentColor" text-anchor="middle">F<tspan font-size="11" dy="3">ref</tspan><tspan dy="-3" dx="4.2">= 5.00 N</tspan></text>
  <g stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="5 3"><line x1="66" y1="357" x2="162.8" y2="357"/><line x1="162.8" y1="357" x2="162.8" y2="402"/></g>
  <text x="162.8" y="435" font-size="12" fill="currentColor" text-anchor="middle">x<tspan font-size="11" dy="3">25</tspan><tspan dy="-3" dx="4.2">= 4.65</tspan></text>
  <g stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="5 3"><line x1="66" y1="312" x2="271.4" y2="312"/><line x1="271.4" y1="312" x2="271.4" y2="402"/></g>
  <text x="271.4" y="435" font-size="12" fill="currentColor" text-anchor="middle">PSE = 5.0429</text>
  <g stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="5 3"><line x1="66" y1="267" x2="389.9" y2="267"/><line x1="389.9" y1="267" x2="389.9" y2="402"/></g>
  <text x="389.9" y="435" font-size="12" fill="currentColor" text-anchor="middle">x<tspan font-size="11" dy="3">75</tspan><tspan dy="-3" dx="4.2">= 5.4714</tspan></text>
  <polyline points="93.6,379.5 176.6,352.5 259.5,316.5 342.5,285 425.4,253.5 508.4,235.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/>
  <g fill="currentColor"><circle cx="93.6" cy="379.5" r="4.2"/><circle cx="176.6" cy="352.5" r="4.2"/><circle cx="259.5" cy="316.5" r="4.2"/><circle cx="342.5" cy="285" r="4.2"/><circle cx="425.4" cy="253.5" r="4.2"/><circle cx="508.4" cy="235.5" r="4.2"/></g>
  <g font-size="11" fill="currentColor" opacity="0.8"><text x="403.3" y="301.2">straight segments =</text><text x="403.3" y="315.2">linear interpolation</text><text x="403.3" y="329.2">(§6); nothing fitted</text></g>
  <line x1="259.5" y1="388" x2="271.4" y2="388" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1.1"><line x1="259.5" y1="385" x2="259.5" y2="391"/><line x1="271.4" y1="385" x2="271.4" y2="391"/></g>
  <text x="277.4" y="392" font-size="11.5" fill="currentColor">bias +43 mN</text>
  <path d="M162.8 446.0 q0 6 6 6 L270.3 452.0 q6 0 6 6 q0 -6 6 -6 L383.9 452.0 q6 0 6 -6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <text x="276.3" y="473" font-size="12" fill="currentColor" text-anchor="middle">2 JND = 0.8214 N   (JND = 0.4107 N)</text>
</svg>

**Panel A — where the stimulus comes from.** A left-to-right chain of four boxes: `commanded force F_c` $\to$ `P3 handle: m = 0.04 kg, b = 0.8 N·s/m` $\to$ `hand: k_h = 400 N/m, b_h = 8 N·s/m` $\to$ `response: which interval pushed harder?`. Under the chain draw the trial as a timeline bar: 1 s at $F_{\text{ref}}$, a 0.5 s gap, 1 s at $F_c$, then the response. Mark $+x$ as the direction the handle pushes. Then write beside the last box the one quantity the chain does not carry: the participant's decision criterion, which exists only inside that box and is why a threshold needs a stated $p$.

**Panel B — the curve.** Comparison force on the horizontal axis, 4.3 to 6.0 N; proportion judged stronger on the vertical, 0 to 1. Plot the six frozen points and join consecutive points with *straight segments*, not a smooth S-curve, because those segments are exactly the linear interpolation of §6 and the figure must show that no psychometric function has been fitted. Draw horizontal lines at $p=0.25$, $0.50$, $0.75$, drop a vertical from each crossing to the axis, and label the three feet $x_{25}$, PSE, $x_{75}$. Brace $x_{25}$ to $x_{75}$ and label the brace $2\,\mathrm{JND}$. Finally mark $F_{\text{ref}}=5.00\,\mathrm{N}$ with a differently styled tick, so that the gap between the reference and the PSE — the bias of Step 7 — is visible rather than asserted.

### 6. Worked case: threshold, JND, and Weber fraction

**Step 1 — the interpolation rule.** Between two tested levels the table says nothing, so the weakest assumption that still lets a threshold exist is a straight line through the two bracketing points. With $(x_i,p_i)$ and $(x_{i+1},p_{i+1})$ the rows on either side of the criterion $p$,

$$x_p=x_i+(x_{i+1}-x_i)\,\frac{p-p_i}{p_{i+1}-p_i}$$

where $x_p$ is the threshold in newtons, $x_i$ and $x_{i+1}$ are the bracketing comparison forces and $p_i,p_{i+1}$ their proportions, since the fraction is simply how far along that segment the criterion sits.

**Step 2 — $x_{25}$.** The criterion $0.250$ falls between rows 1 and 2, where $p$ runs $0.125\to0.275$, so

$$x_{25}=4.40+(4.70-4.40)\frac{0.250-0.125}{0.275-0.125}=4.40+0.30(0.8333)=4.65\ \mathrm{N}.$$

**Step 3 — the PSE.** The criterion $0.500$ falls between rows 3 and 4, where $p$ runs $0.475\to0.650$, so

$$x_{50}=5.00+0.30\,\frac{0.500-0.475}{0.650-0.475}=5.00+0.30(0.1429)=5.0429\ \mathrm{N}.$$

**Step 4 — $x_{75}$.** The criterion $0.750$ falls between rows 4 and 5, where $p$ runs $0.650\to0.825$, so

$$x_{75}=5.30+0.30\,\frac{0.750-0.650}{0.825-0.650}=5.30+0.30(0.5714)=5.4714\ \mathrm{N}.$$

**Step 5 — the JND.** Substituting the two outer thresholds into §2's convention,

$$\mathrm{JND}=\frac{x_{75}-x_{25}}{2}=\frac{5.4714-4.65}{2}=\frac{0.8214}{2}=0.4107\ \mathrm{N}.$$

**Step 6 — the Weber fraction.** Dividing by the operating point the JND was measured at,

$$k=\frac{\mathrm{JND}}{\mathrm{PSE}}=\frac{0.4107}{5.0429}=0.0814,$$

so this participant's force discrimination near 5 N is $8.1\%$ — and §2's illustrative "$8\%$ near $5\,\mathrm{N}$, giving $0.4\,\mathrm{N}$" is the rounded version of exactly this pair of numbers.

**Step 7 — the bias, which is not the JND.** The PSE sits above the reference by

$$\mathrm{PSE}-F_{\text{ref}}=5.0429-5.00=+0.0429\ \mathrm{N}\ (43\ \mathrm{mN}),$$

so the comparison must exceed the reference by 43 mN before the two intervals feel equal. That is a tenth of a JND — small, but it is a property of this handle, this hand and this interval order, not noise. Note also that the midpoint of the 25–75 span, $(4.65+5.4714)/2=5.0607\,\mathrm{N}$, is not the PSE either: the two differ by $0.0179\,\mathrm{N}$ because the interpolated curve is not symmetric. The JND is half a *span*; it is not a distance from the PSE.

**Step 8 — is the device fine enough?** The experiment above commands force directly, but on P3 a force normally arises from pressing into the virtual wall, and there position quantization becomes force quantization. One encoder count of the catalog handle moves it

$$\Delta x=r_m\frac{2\pi}{N}=0.010\,\frac{2\pi}{1024}=6.14\times10^{-5}\ \mathrm{m}\quad(61.4\ \mu\mathrm{m}),$$

and against the default wall $k_w=400\,\mathrm{N/m}$ that one count changes the rendered force by $\Delta F=k_w\Delta x=400(6.14\times10^{-5})=0.0245\,\mathrm{N}$, so the JND is

$$\frac{\mathrm{JND}}{\Delta F}=\frac{0.4107}{0.0245}=16.7\ \text{counts}$$

wide. The force step is about seventeen times finer than the smallest difference this participant can use, so encoder quantization is *not* what limits this experiment — and the same JND is $\mathrm{JND}/k_w=0.4107/400=1.03\,\mathrm{mm}$ of hand motion into the wall. Both statements have to be checked before blaming a null result on the hardware.

**Step 9 — what the four numbers do not license.** $0.4107\,\mathrm{N}$ is a criterion-dependent figure for one participant at one operating point with one hand posture. It does not say that a $0.41\,\mathrm{N}$ step is always noticed and a $0.40\,\mathrm{N}$ step never is, because the interpolated curve is not a step; it does not transfer to a different grasp, a different reference force (the problem set measures that), or a different task; and with 40 trials per level the proportions themselves carry sampling error, so the last digit of $5.0429$ is arithmetic, not evidence.

### Self-check

1. §6 reports two numbers about the same curve: a JND of $0.4107\,\mathrm{N}$ and a bias of $+43\,\mathrm{mN}$. If this participant's whole curve slid $0.1\,\mathrm{N}$ to the right, which of the two would change, and what does that tell you about what each one measures?
2. A colleague reads Step 5 and says "so this participant cannot feel anything below $0.41\,\mathrm{N}$." Name two separate errors in that sentence.
3. Of §2's five terms, only the Weber fraction can be carried between operating points. Why — and what does the problem set's $2\,\mathrm{N}$ result say about how far it carries?
4. Why can a clearer vibration fail to improve a teleoperation task?

> [!tip]- Answers
> 1. Only the bias. A JND is a *width* — half the span $x_{75}-x_{25}$ — so adding the same $0.1\,\mathrm{N}$ to all three thresholds leaves the difference, and therefore the JND, at $0.4107\,\mathrm{N}$; the PSE moves with the curve, so the bias becomes $+143\,\mathrm{mN}$. A width measures how uncertain this participant is, a bias measures where this participant, this handle and this interval order sit relative to the reference. Reporting one in place of the other is the commonest way a psychophysics table becomes uninterpretable.
> 2. First, $0.41\,\mathrm{N}$ is not a detection threshold at all: it is half the $25$–$75$ span of a *comparison* curve around a $5\,\mathrm{N}$ pedestal, so it says nothing about absolute detection and everything about discrimination near $5\,\mathrm{N}$. Second, the interpolated curve is continuous, not a step — at $0.40\,\mathrm{N}$ below the PSE the participant is already right well above chance — so no level exists below which nothing is felt. Step 9 adds a third: one participant, one posture, 40 trials per level.
> 3. Because $k=\mathrm{JND}/I$ divides the increment by the intensity it was measured at, so it is dimensionless and the operating point cancels; the other four are a task, a level, a level and a difference, each pinned to its own reference. How far it carries is exactly what the problem set measures: $k$ rose from $8.14\%$ at $5.04\,\mathrm{N}$ to $8.96\%$ at $2.03\,\mathrm{N}$, so Weber's law held qualitatively (the absolute JND shrank, $0.4107\to0.1821\,\mathrm{N}$) and failed quantitatively over that range. "Comparable across operating points" means locally comparable.
> 4. Detectability is only one link. The cue may arrive late, encode the wrong state, conflict with vision, consume attention, or fail to change an actionable decision. Test perception, control behaviour, and task outcome separately.

### Problem set · 과제

Tier B. Using **P3** from [[02-foundations/lab-plants|0.6]] and this page. Hand calculation only — the Euler loop for this handle lives on [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]], and nothing here needs a simulator.

Same participant, same handle, same 2AFC task, but the reference is moved down to $F_{\text{ref}}=2.00\,\mathrm{N}$ and six new comparison levels are run, 40 trials each. This table is the problem set's own frozen record, again illustrative and not measured:

| $F_c$ (N) | 1.70 | 1.85 | 2.00 | 2.15 | 2.30 | 2.45 |
|---|---:|---:|---:|---:|---:|---:|
| judged stronger (of 40) | 4 | 10 | 18 | 27 | 34 | 38 |

1. **Draw.** Draw §5's two panels for this table, with the horizontal axis now 1.6 to 2.5 N. Mark $F_{\text{ref}}=2.00\,\mathrm{N}$, the three criterion lines, and the $2\,\mathrm{JND}$ brace. In panel A, change only what actually changed.
2. **Derive.** (a) $x_{25}$, the PSE and $x_{75}$ by §6's rule. One of the three needs no interpolation — say which and why. (b) The JND and the Weber fraction $k$. (c) The bias $\mathrm{PSE}-F_{\text{ref}}$. (d) The JND in P3 encoder counts of wall force, and as a penetration in millimetres.
3. **Interpret.** (a) Compare $k$ with the $8.14\%$ of §6: the absolute JND fell, the fraction rose. Which half of Weber's law survived, and which did not? (b) A device reflects $5.2\,\mathrm{N}$ versus $5.0\,\mathrm{N}$ and the paper claims every participant notices. Using §6's numbers, what exactly is wrong? (c) Another paper says "users detected the 250 Hz vibration, therefore the cue improved insertion". Which arrows of the causal chain were skipped, and what would you measure at each? (d) Two sensors, $\sigma_v=2\,\mathrm{mm}$ and $\sigma_h=4\,\mathrm{mm}$, are fused by precision weighting. Write $\hat x$, then say what "vision dominates, so haptic noise does not matter" dropped from the model.

> [!tip]- Solutions
> 1. Panel A is unchanged except for the two force labels: the chain, the handle constants and the timeline are the same object. Panel B has six new points at $p=0.100,0.250,0.450,0.675,0.850,0.950$; the $p=0.25$ line meets the data exactly at a tested level, so that foot lands on a plotted point rather than inside a segment.
> 2. (a) $p=0.250$ *is* the measured proportion at $1.85\,\mathrm{N}$, so $x_{25}=1.85\,\mathrm{N}$ with no interpolation — the criterion coincided with a tested level. $x_{50}=2.00+0.15(0.500-0.450)/(0.675-0.450)=2.00+0.15(0.2222)=2.0333\,\mathrm{N}$. $x_{75}=2.15+0.15(0.750-0.675)/(0.850-0.675)=2.15+0.15(0.4286)=2.2143\,\mathrm{N}$. (b) $\mathrm{JND}=(2.2143-1.85)/2=0.3643/2=0.1821\,\mathrm{N}$ and $k=0.1821/2.0333=0.0896$, i.e. $9.0\%$. (c) $\mathrm{PSE}-F_{\text{ref}}=2.0333-2.00=+0.0333\,\mathrm{N}$ (33 mN), a smaller absolute bias than at 5 N but a larger one relative to the JND. (d) $0.1821/0.0245=7.4$ counts, and $0.1821/400=4.55\times10^{-4}\,\mathrm{m}=0.46\,\mathrm{mm}$ of penetration. The margin over quantization has fallen by more than half, from about 17 counts to about 7; it is still comfortable, but this is the direction in which a low-force experiment eventually becomes a hardware experiment.
> 3. (a) The qualitative half survived: the absolute increment shrank with the reference, $0.4107\to0.1821\,\mathrm{N}$ for $5.04\to2.03\,\mathrm{N}$. The quantitative half did not: $k$ rose from $8.14\%$ to $8.96\%$, so $\Delta I/I$ is not constant across this range. Weber's law is a local approximation and these two operating points are not in the same locality. (b) $5.2$ versus $5.0$ is a $0.2\,\mathrm{N}$ difference against a $0.41\,\mathrm{N}$ JND — about half a JND, which is inside the uncertain region, and even at exactly one JND the convention only fixes the 75% point of one participant's curve. Neither "every participant" nor "notices" follows. (c) Detectability $\to$ action $\to$ task outcome. Measure the delivered skin stimulus (not the command), the control behaviour (contact force, timing), and the insertion outcome, separately; detection is one link of three. (d) $\hat x=(\sigma_v^{-2}x_v+\sigma_h^{-2}x_h)/(\sigma_v^{-2}+\sigma_h^{-2})=\tfrac45x_v+\tfrac15x_h$. The weights are $4:1$, not $1:0$, so "dominates" dropped both the haptic term and the assumption list (Gaussian, independent, temporally aligned).

## 한국어

*햅틱 트랙의 지각 쪽 끝이다. 장치 **P3**를 렌더링 루프가 아니라 자극 발생기로 쓰는 첫 페이지이고, 루프 자체는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]에 있다.*

### 이 페이지의 대상 · Running object

이 페이지의 모든 숫자는 얼어붙은 실험 하나에서 나온다. 여기서 한 번 정하고 뒤에서 절대 바꾸지 않는다. **아래 응답 횟수는 계산이 딱 떨어지도록 이 페이지에서 정의한 예시 값이다. 누군가가 측정한 데이터가 아니며, 여기서 어떤 경험적 주장도 인용할 수 없다.**

**전달 장치는 장치 P3**, [[02-foundations/lab-plants|0.6 Lab Plants]]의 1자유도 병진 핸들이다. 유효 질량 $m=0.04\,\mathrm{kg}$, 댐핑 $b=0.8\,\mathrm{N\cdot s/m}$, 손 $k_h=400\,\mathrm{N/m}$, $b_h=8\,\mathrm{N\cdot s/m}$. 핸들이 곧 자극 발생기다. 명령된 힘으로 손을 $+x$ 방향으로 민다. 그래서 이 페이지에서 *자극*은 한 손의 한 파지점에 가해지는 뉴턴 단위의 힘이다. P3 카탈로그는 증폭기 한계를 고정하지 않는다. [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]] 과제의 $2.0\,\mathrm{N}$ 포화는 그 문제를 위해 만든 숫자다. 그래서 이 실험은 가정 하나를 더 둔다. 핸들이 $0$에서 $6\,\mathrm{N}$까지 어떤 힘이든 꾸준히 낼 수 있다고 본다.

**과제는 2구간 2대안 강제 선택이다.** 매 시행마다 기준 힘 $F_{\text{ref}}=5.00\,\mathrm{N}$를 1초 동안 내고, 0.5초 쉬고, 비교 힘 $F_c$를 1초 동안 낸 뒤 *어느 구간이 더 세게 밀었는가*를 묻는다. 구간 순서는 무작위이고, 확신이 없어도 반드시 답해야 한다.

**얼어붙은 기록: 비교 수준 여섯, 각 40시행, 총 240시행, 참가자 한 명.**

| $F_c$ (N) | 더 세다고 판정 | 중 | $p$ |
|---:|---:|---:|---:|
| 4.40 | 5 | 40 | 0.125 |
| 4.70 | 11 | 40 | 0.275 |
| 5.00 | 19 | 40 | 0.475 |
| 5.30 | 26 | 40 | 0.650 |
| 5.60 | 33 | 40 | 0.825 |
| 5.90 | 37 | 40 | 0.925 |

$p$는 그 수준의 40시행 중 참가자가 *비교* 구간을 더 세다고 답한 비율이다. §5가 무엇을 그릴지 말하고, §6이 이 표를 임계값·JND·Weber 분수로 바꾸며, 과제는 더 낮은 기준 힘에서 같은 일을 다시 한다.

### 1. 촉각은 능동 센싱 루프다

**Cutaneous** cue는 피부 변형에서, **kinesthetic·proprioceptive** cue는 사지가 움직일 때 근육·힘줄·관절과 피부 신장에서 나온다. 햅틱 지각은 이 둘을 운동 명령과, 흔히 시각·청각과도 결합한다. 수동 자극은 주어진 cue가 무엇을 불러일으키는지 묻고, 능동 촉각은 사람이 탐색 동작까지 고른다. 질감, 경도, 온도, 무게, 정확한 형상은 서로 다른 탐색 절차(사람이 어떤 성질을 알아내려고 쓰는 정형화된 손동작. 질감에는 옆으로 문지르기, 경도에는 누르기, 온도에는 가만히 대고 있기)를 부르므로, 장치는 목표 과제가 실제로 요구하는 움직임으로 평가해야 한다.

흔히 쓰는 수용기 이름표는 유용하지만 근사다. 이름에서 SA는 slowly adapting(지속 자극 동안 계속 발화), RA는 rapidly adapting(주로 자극이 변할 때 발화)이고, I형은 수용장이 작고 II형은 크다.

| 구심신경 부류 | 적응·수용장 | 특히 잘 알려 주는 것 |
|---|---|---|
| SA-I / Merkel | 느림, 작은 수용장 | 지속 압력, 경계, 거친 형태 |
| RA-I / Meissner | 빠름, 작은 수용장 | 저주파 과도, 미끄럼 시작 |
| SA-II / Ruffini | 느림, 큰 수용장 | 피부 신장, 손 자세 |
| RA-II / Pacinian | 빠름, 큰 수용장 | 고주파 진동과 충격 |

주파수 대역은 서로 겹치고 접촉자 크기, 부위, 예압, 파형에 따라 달라진다. "250 Hz가 최적"이라는 진술은 그 조건들 없이는 불완전하다.

### 2. 임계값, PSE, JND

**심리측정 함수**는 물리 자극 $x$를 반응 확률로 사상한다. 예를 들어 $P(\text{비교 자극이 더 강하다고 판정}\mid x)$이다. 그 중간점이 **주관적 등가점**(PSE)을 정의할 수 있다. 2대안 비교에서 흔한 관례 하나는 곡선에서 최소 식별차(JND)를 읽는 것이다. $x_{75}$와 $x_{25}$는 더 강하다고 판정되는 비율이 각각 75%와 25%인 자극 수준이므로, 그 간격의 절반은 판단이 믿을 만하게 바뀌려면 자극이 PSE에서 얼마나 움직여야 하는지를 잰다.

$$\mathrm{JND}=\frac{x_{75}-x_{25}}{2}.$$

이것은 보편적 정의가 아니다. yes/no 검출, $n$대안 선택, 적합된 함수는 각각 다른 chance level과 임계 기준을 쓴다. 50% 임계값이라는 말은 반응 과제를 명시한 뒤에만 의미를 갖는다.

**다섯 용어의 정의.** 다섯 모두 피부의 성질이 아니라 *곡선에 적용한 관례*다. 그래서 각각 자기 과제를 달고 다녀야 한다. §6이 이 다섯을 running object 위에서 전부 계산한다.

- **2대안 강제 선택(2AFC)** — *반응 과제*이고, 조건 셋으로 정의된다. 대안이 정확히 둘 제시되고, 매 시행 응답이 강제되며, 어느 쪽이 기준인지를 실험자가 고정한다. *예*: running object의 두 구간. *반례*: "힘을 1에서 7로 평정하라". 이것은 평정 척도이고 그 중간점은 설계가 고정한 chance level이 아니라 참가자가 고르는 기준이다. 중요한 이유는 대안의 수가 chance level을 정하고($1/2$), chance level이 어떤 $p$가 임계값이 될지를 정하기 때문이다.
- **임계값 $x_p$** — *자극 수준*이다. 반응 확률이 당신이 이름 붙인 기준 $p$와 같아지는 수준. 그래서 $p$와 과제가 둘 다 없는 "그 임계값"은 아직 양이 아니고, 같은 cue의 "임계값"을 보고한 두 논문이 같은 곡선의 다른 점을 보고한 것일 수 있다.
- **주관적 등가점(PSE)** — 비교 곡선에서 *$p=0.5$인 임계값*이다. 더 세다고 답할 확률과 더 약하다고 답할 확률이 같아지는 비교 수준. *반례*: 기준 힘. $\mathrm{PSE}\neq F_{\text{ref}}$이면 그 차이는 이 참가자가 이 장치와 이 구간 순서에서 갖는 일정한 편향이고, 평균으로 지워 버릴 잡음이 아니라 그 쌍에 관한 발견이다.
- **JND** — *자극 차이*다. 위 공식의 관례대로 25%와 75% 임계값 사이 간격의 절반. 지각이 켜지는 계단의 위치가 아니라 불확실 구간의 폭을 잰다.
- **Weber 분수 $k$** — *무차원 비*다. JND를 그것을 잰 기준 세기로 나눈 값:

$$k=\frac{\mathrm{JND}}{I},$$

여기서 $I$는 작동점의 세기(§6에서는 PSE)다. 다섯 중 작동점을 가로질러 비교할 수 있는 유일한 양이 $k$이고, 그것조차 국소적으로만 그렇다.

**Weber 법칙**은 국소적인 경험 근사 $\Delta I/I\approx k$다. 구별에 필요한 절대 증가량이 기준 세기와 함께 커진다고 예측한다. 같은 상대 증가량을 적분하면 Fechner의 로그 척도(지각된 크기가 물리 세기의 로그에 대략 비례해 커진다)가 동기를 얻지만, 두 법칙 중 어느 것도 모든 세기와 모든 감각 양상에서 정확하지는 않다.

계산해 읽기: 5 N 부근에서 힘 JND가 8%라면 알아챌 만한 증가량의 첫 추정은 $0.08(5)=0.4$ N이다. 이것은 모든 참가자가 5.4 N을 알아챈다는 증명이 아니라, 그 작동점 부근에서 기준에 의존하는 모집단 반응을 서술한 것이다.

### 3. 실험 고르기

| 질문 | 쓸 만한 방법 | 주된 위험 |
|---|---|---|
| 대략의 임계값을 빨리 찾기 | staircase · 적응적 up–down | 수렴이 규칙과 실수율에 달림 |
| 전체 심리측정 곡선 추정 | constant stimuli | 시행이 많고 순서·피로가 개입 |
| 사용자가 감각을 맞추게 하기 | adjustment | 반응 편향과 anchoring |
| 두 인터페이스 비교 | within-subject counterbalanced | 이월 효과와 학습 |

hit뿐 아니라 false alarm도 재라. 신호 검출 분석이 민감도(자극이 있을 때와 없을 때를 실제로 얼마나 잘 구별하는가)와 반응 기준(확신이 없을 때 "있다"고 답하려는 경향)을 분리해 준다. 신중한 참가자와 대담한 참가자는 민감도가 같아도 hit 비율이 크게 다를 수 있기 때문이다. 조건 순서를 무작위화하고, 훈련을 넣고, 제외 기준을 미리 정하고, 선호도에만 기대지 말고 접촉력·운동·지연·과제 성공을 기록하라.

### 4. 다감각과 workload 주장

특정한 가우시안·잡음 가정 아래에서 분산이 $\sigma_v^2$와 $\sigma_h^2$인 두 추정치는 정밀도 가중으로 결합된다.

$$\hat x=\frac{\sigma_v^{-2}x_v+\sigma_h^{-2}x_h}{\sigma_v^{-2}+\sigma_h^{-2}}.$$

이것은 모델이지 감각 우세의 보편 법칙이 아니다. 신뢰도, 시간 정렬, 과제 관련성, prior, 주의, 충돌이 cue가 융합할지 경쟁할지 따로 남을지를 결정한다. 마찬가지로 경고를 시각에서 촉각으로 옮긴다고 workload가 자동으로 줄지 않는다. 대표성 있는 다중 과제 시험이 필요하다.

**계산해 읽기: 과제가 묻는 융합.** $\sigma_v=2\,\mathrm{mm}$, $\sigma_h=4\,\mathrm{mm}$이면 가중이 $4:1$이므로 $\hat x=\tfrac45x_v+\tfrac15x_h$이지 시각 단독이 아니다. $5\,\mathrm{N}$ 부근 힘 JND $8\%$는 *모집단* 증분 $0.4\,\mathrm{N}$이고, $5.2$ 대 $5.0$은 JND의 절반이라 "모든 참가자가 알아챈다"를 허락하지 않는다. $250\,\mathrm{Hz}$ 진동을 검출했다는 것은 삽입 성공이 아니다. 사슬은 검출 가능성 $\to$ 행동 $\to$ 결과다.

### 5. 과제가 그릴 그림

그림 하나, 패널 둘. 과제는 다른 표로 같은 그림을 그리라고 하므로, 여기서 한 번 제대로 그려 둔다.

<svg viewBox="0 0 560 486" style="max-width:100%;height:auto" role="img" aria-label="패널 A는 명령 힘에서 P3 핸들과 손을 거쳐 응답으로 가는 자극과 1초, 0.5초, 1초의 시행 타임라인, 응답 안에만 있는 결정 기준을 보이고, 패널 B는 얼어붙은 여섯 비율을 직선 구간으로 이어 0.25, 0.50, 0.75의 교차점을 x25 = 4.65, PSE = 5.0429, x75 = 5.4714 N으로 내리고 0.8214 N의 2 JND 괄호와 PSE보다 43 mN 왼쪽의 기준 힘 5.00 N을 표시한다.">
  <text x="10" y="18" font-size="12.5" fill="currentColor">A · 자극이 어디서 오는가</text>
  <rect x="8" y="30" width="92" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="54" y="55.8">명령 힘</text><text x="54" y="70.2">F<tspan font-size="11" dy="3">c</tspan></text></g>
  <line x1="103" y1="59" x2="110.5" y2="59" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="117,59 110,62.4 110,55.6" fill="currentColor"/>
  <rect x="120" y="30" width="124" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="182" y="48.5">P3 핸들</text><text x="182" y="63">m = 0.04 kg</text><text x="182" y="77.5">b = 0.8 N·s/m</text></g>
  <line x1="247" y1="59" x2="254.5" y2="59" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,59 254,62.4 254,55.6" fill="currentColor"/>
  <rect x="264" y="30" width="124" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="326" y="48.5">손</text><text x="326" y="63">k<tspan font-size="11" dy="3">h</tspan><tspan dy="-3" dx="4">= 400 N/m</tspan></text><text x="326" y="77.5">b<tspan font-size="11" dy="3">h</tspan><tspan dy="-3" dx="4">= 8 N·s/m</tspan></text></g>
  <line x1="391" y1="59" x2="398.5" y2="59" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="405,59 398,62.4 398,55.6" fill="currentColor"/>
  <rect x="408" y="30" width="144" height="58" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="480" y="48.5">응답:</text><text x="480" y="63">어느 구간이</text><text x="480" y="77.5">더 세게 밀었는가?</text><text x="254" y="51">+x</text></g>
  <text x="18" y="104" font-size="11" fill="currentColor" opacity="0.8">시행 하나</text>
  <rect x="18" y="110" width="110" height="18" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <rect x="128" y="110" width="55" height="18" fill="none" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <rect x="183" y="110" width="110" height="18" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="73" y="123">F<tspan font-size="11" dy="3">ref</tspan><tspan dy="-3" dx="4">= 5.00 N</tspan></text><text x="238" y="123">F<tspan font-size="11" dy="3">c</tspan></text></g>
  <line x1="295" y1="119" x2="305.5" y2="119" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="311,119 305,122 305,116" fill="currentColor"/>
  <text x="315" y="123" font-size="11.5" fill="currentColor">응답</text>
  <g font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8"><text x="73" y="143">1 s</text><text x="155.5" y="143">0.5 s</text><text x="238" y="143">1 s</text></g>
  <line x1="480" y1="90" x2="480" y2="97" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="414" y="110" font-size="11" fill="currentColor">사슬이 나르지 않는 양:</text>
  <g font-size="11" fill="currentColor" opacity="0.9"><text x="414" y="124">참가자의 결정 기준.</text><text x="414" y="138">이 상자 안에만 있고,</text><text x="414" y="152">그래서 임계값에는</text><text x="414" y="166">p를 밝혀야 한다.</text></g>
  <line x1="8" y1="172" x2="552" y2="172" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="3 4"/>
  <text x="10" y="196" font-size="12.5" fill="currentColor">B · 곡선: 비교 힘에 대한 “더 세다” 판정 비율</text>
  <g stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"><line x1="66" y1="402" x2="536" y2="402"/><line x1="66" y1="402" x2="66" y2="222"/><line x1="62" y1="402" x2="66" y2="402"/></g>
  <text x="59" y="406" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0</text>
  <line x1="62" y1="357" x2="66" y2="357" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="361" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0.25</text>
  <line x1="62" y1="312" x2="66" y2="312" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="316" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0.50</text>
  <line x1="62" y1="267" x2="66" y2="267" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="271" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">0.75</text>
  <line x1="62" y1="222" x2="66" y2="222" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="59" y="226" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">1</text>
  <text x="59" y="212" font-size="12" fill="currentColor" text-anchor="end" opacity="0.9">p</text>
  <line x1="93.6" y1="402" x2="93.6" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="93.6" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">4.4</text>
  <line x1="176.6" y1="402" x2="176.6" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="176.6" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">4.7</text>
  <line x1="259.5" y1="402" x2="259.5" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="259.5" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.0</text>
  <line x1="342.5" y1="402" x2="342.5" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="342.5" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.3</text>
  <line x1="425.4" y1="402" x2="425.4" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="425.4" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.6</text>
  <line x1="508.4" y1="402" x2="508.4" y2="406" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="508.4" y="418" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">5.9</text>
  <text x="548" y="435" font-size="12" fill="currentColor" text-anchor="end" opacity="0.85">F<tspan font-size="11" dy="3">c</tspan><tspan dy="-3" dx="4.2">(N)</tspan></text>
  <line x1="259.5" y1="222" x2="259.5" y2="394" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" stroke-dasharray="1.5 2.5"/>
  <polygon points="259.5,393.0 254.5,402.0 264.5,402.0" fill="none" stroke="currentColor" stroke-width="1.3"/>
  <text x="259.5" y="216" font-size="12" fill="currentColor" text-anchor="middle">F<tspan font-size="11" dy="3">ref</tspan><tspan dy="-3" dx="4.2">= 5.00 N</tspan></text>
  <g stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="5 3"><line x1="66" y1="357" x2="162.8" y2="357"/><line x1="162.8" y1="357" x2="162.8" y2="402"/></g>
  <text x="162.8" y="435" font-size="12" fill="currentColor" text-anchor="middle">x<tspan font-size="11" dy="3">25</tspan><tspan dy="-3" dx="4.2">= 4.65</tspan></text>
  <g stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="5 3"><line x1="66" y1="312" x2="271.4" y2="312"/><line x1="271.4" y1="312" x2="271.4" y2="402"/></g>
  <text x="271.4" y="435" font-size="12" fill="currentColor" text-anchor="middle">PSE = 5.0429</text>
  <g stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="5 3"><line x1="66" y1="267" x2="389.9" y2="267"/><line x1="389.9" y1="267" x2="389.9" y2="402"/></g>
  <text x="389.9" y="435" font-size="12" fill="currentColor" text-anchor="middle">x<tspan font-size="11" dy="3">75</tspan><tspan dy="-3" dx="4.2">= 5.4714</tspan></text>
  <polyline points="93.6,379.5 176.6,352.5 259.5,316.5 342.5,285 425.4,253.5 508.4,235.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/>
  <g fill="currentColor"><circle cx="93.6" cy="379.5" r="4.2"/><circle cx="176.6" cy="352.5" r="4.2"/><circle cx="259.5" cy="316.5" r="4.2"/><circle cx="342.5" cy="285" r="4.2"/><circle cx="425.4" cy="253.5" r="4.2"/><circle cx="508.4" cy="235.5" r="4.2"/></g>
  <g font-size="11" fill="currentColor" opacity="0.8"><text x="403.3" y="301.2">직선 구간 =</text><text x="403.3" y="315.2">§6의 선형 보간.</text><text x="403.3" y="329.2">적합한 곡선은 없다</text></g>
  <line x1="259.5" y1="388" x2="271.4" y2="388" stroke="currentColor" stroke-width="1.3"/>
  <g stroke="currentColor" stroke-width="1.1"><line x1="259.5" y1="385" x2="259.5" y2="391"/><line x1="271.4" y1="385" x2="271.4" y2="391"/></g>
  <text x="277.4" y="392" font-size="11.5" fill="currentColor">편향 +43 mN</text>
  <path d="M162.8 446.0 q0 6 6 6 L270.3 452.0 q6 0 6 6 q0 -6 6 -6 L383.9 452.0 q6 0 6 -6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <text x="276.3" y="473" font-size="12" fill="currentColor" text-anchor="middle">2 JND = 0.8214 N   (JND = 0.4107 N)</text>
</svg>

**패널 A — 자극이 어디서 오는가.** 왼쪽에서 오른쪽으로 상자 넷의 사슬: `명령 힘 F_c` $\to$ `P3 핸들: m = 0.04 kg, b = 0.8 N·s/m` $\to$ `손: k_h = 400 N/m, b_h = 8 N·s/m` $\to$ `응답: 어느 구간이 더 세게 밀었는가?`. 사슬 아래에 시행을 타임라인 막대로 그린다. $F_{\text{ref}}$로 1초, 0.5초 공백, $F_c$로 1초, 그다음 응답. 핸들이 미는 방향을 $+x$로 표시한다. 그리고 마지막 상자 옆에, 사슬이 나르지 *않는* 양 하나를 적는다. 참가자의 결정 기준이다. 그 상자 안에만 있고, 임계값에 $p$를 명시해야 하는 이유가 바로 그것이다.

**패널 B — 곡선.** 가로축은 비교 힘 4.3에서 6.0 N, 세로축은 더 세다고 판정한 비율 0에서 1. 얼어붙은 여섯 점을 찍고 이웃한 점끼리 매끈한 S자가 아니라 *직선 구간*으로 잇는다. 그 직선들이 정확히 §6의 선형 보간이고, 심리측정 함수를 적합한 적이 없다는 것을 그림이 보여야 하기 때문이다. $p=0.25$, $0.50$, $0.75$에 수평선을 긋고, 각 교차점에서 축으로 수직선을 내리고, 세 발을 $x_{25}$, PSE, $x_{75}$로 이름 붙인다. $x_{25}$에서 $x_{75}$까지 괄호를 치고 $2\,\mathrm{JND}$라고 적는다. 마지막으로 $F_{\text{ref}}=5.00\,\mathrm{N}$을 다른 모양의 눈금으로 표시해서, 기준과 PSE 사이의 간격 — Step 7의 편향 — 이 주장이 아니라 눈에 보이게 한다.

### 6. 대상으로 한 번 끝까지: 임계값, JND, Weber 분수

**Step 1 — 보간 규칙.** 시험한 두 수준 사이에서 표는 아무 말도 하지 않는다. 그래도 임계값이 존재하게 하는 가장 약한 가정은 양쪽 점을 잇는 직선이다. 기준 $p$의 양옆 행을 $(x_i,p_i)$, $(x_{i+1},p_{i+1})$이라 하면

$$x_p=x_i+(x_{i+1}-x_i)\,\frac{p-p_i}{p_{i+1}-p_i}$$

이다. $x_p$는 뉴턴 단위의 임계값, $x_i$와 $x_{i+1}$은 양옆 비교 힘, $p_i,p_{i+1}$은 그 비율이다. 분수는 기준이 그 구간의 어디쯤에 있는지를 나타낼 뿐이기 때문이다.

**Step 2 — $x_{25}$.** 기준 $0.250$은 1행과 2행 사이, $p$가 $0.125\to0.275$로 가는 구간에 있으므로

$$x_{25}=4.40+(4.70-4.40)\frac{0.250-0.125}{0.275-0.125}=4.40+0.30(0.8333)=4.65\ \mathrm{N}.$$

**Step 3 — PSE.** 기준 $0.500$은 3행과 4행 사이, $p$가 $0.475\to0.650$인 구간에 있으므로

$$x_{50}=5.00+0.30\,\frac{0.500-0.475}{0.650-0.475}=5.00+0.30(0.1429)=5.0429\ \mathrm{N}.$$

**Step 4 — $x_{75}$.** 기준 $0.750$은 4행과 5행 사이, $p$가 $0.650\to0.825$인 구간에 있으므로

$$x_{75}=5.30+0.30\,\frac{0.750-0.650}{0.825-0.650}=5.30+0.30(0.5714)=5.4714\ \mathrm{N}.$$

**Step 5 — JND.** 바깥쪽 임계값 둘을 §2의 관례에 넣으면

$$\mathrm{JND}=\frac{x_{75}-x_{25}}{2}=\frac{5.4714-4.65}{2}=\frac{0.8214}{2}=0.4107\ \mathrm{N}.$$

**Step 6 — Weber 분수.** JND를 잰 작동점으로 나누면

$$k=\frac{\mathrm{JND}}{\mathrm{PSE}}=\frac{0.4107}{5.0429}=0.0814,$$

이므로 이 참가자의 5 N 부근 힘 변별은 $8.1\%$다. §2의 예시 "$5\,\mathrm{N}$ 부근 $8\%$, 증분 $0.4\,\mathrm{N}$"은 바로 이 두 숫자를 반올림한 것이다.

**Step 7 — 편향은 JND가 아니다.** PSE는 기준보다

$$\mathrm{PSE}-F_{\text{ref}}=5.0429-5.00=+0.0429\ \mathrm{N}\ (43\ \mathrm{mN})$$

만큼 위에 있다. 비교 힘이 기준보다 43 mN 커져야 두 구간이 같게 느껴진다는 뜻이다. JND의 10분의 1이라 작지만, 이 핸들과 이 손과 이 구간 순서의 성질이지 잡음이 아니다. 25–75 구간의 중점 $(4.65+5.4714)/2=5.0607\,\mathrm{N}$도 PSE가 아니다. 보간된 곡선이 대칭이 아니어서 둘은 $0.0179\,\mathrm{N}$ 다르다. JND는 *구간*의 절반이지 PSE에서 잰 거리가 아니다.

**Step 8 — 장치는 충분히 곱나?** 위 실험은 힘을 직접 명령하지만, P3에서 힘은 보통 가상 벽을 파고들며 생기고 거기서는 위치 양자화가 곧 힘 양자화다. 카탈로그 핸들의 엔코더 한 카운트는

$$\Delta x=r_m\frac{2\pi}{N}=0.010\,\frac{2\pi}{1024}=6.14\times10^{-5}\ \mathrm{m}\quad(61.4\ \mu\mathrm{m})$$

만큼 핸들을 움직이고, 기본 벽 $k_w=400\,\mathrm{N/m}$에서 그 한 카운트는 렌더링되는 힘을 $\Delta F=k_w\Delta x=400(6.14\times10^{-5})=0.0245\,\mathrm{N}$만큼 바꾼다. 그러므로 JND의 폭은

$$\frac{\mathrm{JND}}{\Delta F}=\frac{0.4107}{0.0245}=16.7\ \text{카운트}$$

다. 힘의 한 단은 이 참가자가 쓸 수 있는 최소 차이보다 약 17배 곱기 때문에, 엔코더 양자화는 이 실험의 한계가 *아니다*. 같은 JND는 벽 안으로 $\mathrm{JND}/k_w=0.4107/400=1.03\,\mathrm{mm}$ 손을 움직인 것과 같다. 영(null) 결과를 하드웨어 탓으로 돌리기 전에 이 두 진술을 모두 확인해야 한다.

**Step 9 — 네 숫자가 허락하지 않는 것.** $0.4107\,\mathrm{N}$은 한 참가자가 한 작동점에서 한 파지 자세로 낸, 기준에 의존하는 값이다. $0.41\,\mathrm{N}$ 단은 항상 알아채고 $0.40\,\mathrm{N}$ 단은 절대 못 알아챈다는 뜻이 아니다. 보간된 곡선은 계단이 아니기 때문이다. 다른 파지, 다른 기준 힘(과제가 그것을 잰다), 다른 과제로 옮겨 가지도 않는다. 그리고 수준당 40시행이므로 비율 자체가 표본 오차를 달고 있어, $5.0429$의 마지막 자리는 산술이지 증거가 아니다.

### 스스로 점검

1. §6은 같은 곡선에서 숫자 둘을 보고한다. JND $0.4107\,\mathrm{N}$과 편향 $+43\,\mathrm{mN}$이다. 이 참가자의 곡선 전체가 오른쪽으로 $0.1\,\mathrm{N}$ 미끄러진다면 둘 중 무엇이 바뀌는가? 그 사실이 각 숫자가 무엇을 재는지에 대해 무엇을 말해 주는가?
2. 동료가 Step 5를 읽고 "그러면 이 참가자는 $0.41\,\mathrm{N}$ 아래로는 아무것도 못 느낀다"고 말한다. 이 문장의 서로 다른 오류 둘을 지적하라.
3. §2의 다섯 용어 중 작동점을 옮겨 가며 쓸 수 있는 것은 Weber 분수뿐이다. 왜인가? 그리고 과제의 $2\,\mathrm{N}$ 결과는 그것이 얼마나 멀리까지 옮겨 가는지에 대해 무엇을 말하는가?
4. 더 선명한 진동이 원격조작 과제를 개선하지 못할 수 있는 이유는?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 편향만 바뀐다. JND는 *폭*, 즉 $x_{75}-x_{25}$의 절반이므로 세 임계값에 같은 $0.1\,\mathrm{N}$을 더해도 차이는 그대로여서 JND는 $0.4107\,\mathrm{N}$에 머문다. PSE는 곡선을 따라 움직이므로 편향은 $+143\,\mathrm{mN}$이 된다. 폭은 이 참가자가 얼마나 불확실한지를 재고, 편향은 이 참가자와 이 핸들과 이 구간 순서가 기준에 대해 어디에 앉아 있는지를 잰다. 하나를 다른 하나 자리에 보고하는 것이 심리물리 표를 해석 불가능하게 만드는 가장 흔한 방법이다.
> 2. 첫째, $0.41\,\mathrm{N}$은 검출 임계값이 아니다. $5\,\mathrm{N}$ 받침 둘레의 *비교* 곡선에서 $25$–$75$ 구간의 절반이므로, 절대 검출에 대해서는 아무 말도 하지 않고 $5\,\mathrm{N}$ 부근의 변별에 대해서만 말한다. 둘째, 보간된 곡선은 계단이 아니라 연속이다. PSE보다 $0.40\,\mathrm{N}$ 낮은 곳에서도 참가자는 이미 우연 수준보다 훨씬 자주 맞힌다. 그러므로 그 아래로는 아무것도 느끼지 못하는 수준 같은 것은 없다. Step 9가 셋째를 더한다. 참가자 한 명, 자세 하나, 수준당 40시행이다.
> 3. $k=\mathrm{JND}/I$는 증분을 그것을 잰 세기로 나누므로 무차원이고 작동점이 약분되기 때문이다. 나머지 넷은 과제, 수준, 수준, 차이이고 각각 자기 기준에 붙박여 있다. 얼마나 멀리 가는지는 과제가 바로 그것을 잰다. $k$는 $5.04\,\mathrm{N}$에서 $8.14\%$, $2.03\,\mathrm{N}$에서 $8.96\%$로 올랐다. 그래서 Weber 법칙은 정성적으로는 살아남고(절대 JND가 $0.4107\to0.1821\,\mathrm{N}$로 줄었다) 이 범위에서 정량적으로는 깨졌다. "작동점을 가로질러 비교 가능"은 국소적으로 비교 가능하다는 뜻이다.
> 4. 검출 가능성은 사슬의 한 고리일 뿐이다. cue가 늦게 도착하거나, 틀린 상태를 부호화하거나, 시각과 충돌하거나, 주의를 소모하거나, 실행 가능한 결정을 바꾸지 못할 수 있다. 지각과 제어 행동과 과제 결과를 따로 시험하라.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P3**와 이 페이지를 쓴다. 손 계산만 한다. 이 핸들의 오일러 루프는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]에 있고, 여기서는 시뮬레이터가 필요 없다.

같은 참가자, 같은 핸들, 같은 2AFC 과제. 다만 기준을 $F_{\text{ref}}=2.00\,\mathrm{N}$로 낮추고 새 비교 수준 여섯을 각 40시행 돌린다. 이 표가 과제의 얼어붙은 기록이고, 역시 예시 값이지 측정값이 아니다.

| $F_c$ (N) | 1.70 | 1.85 | 2.00 | 2.15 | 2.30 | 2.45 |
|---|---:|---:|---:|---:|---:|---:|
| 더 세다고 판정 (40 중) | 4 | 10 | 18 | 27 | 34 | 38 |

1. **그려라.** 이 표로 §5의 두 패널을 그려라. 가로축은 이제 1.6에서 2.5 N이다. $F_{\text{ref}}=2.00\,\mathrm{N}$, 기준선 셋, $2\,\mathrm{JND}$ 괄호를 표시하라. 패널 A에서는 실제로 바뀐 것만 바꿔라.
2. **유도하라.** (a) §6의 규칙으로 $x_{25}$, PSE, $x_{75}$. 셋 중 하나는 보간이 필요 없다. 어느 것이고 왜인가. (b) JND와 Weber 분수 $k$. (c) 편향 $\mathrm{PSE}-F_{\text{ref}}$. (d) JND를 P3 엔코더 카운트 수의 벽 힘으로, 그리고 밀리미터 단위 침투로.
3. **해석하라.** (a) $k$를 §6의 $8.14\%$와 비교하라. 절대 JND는 줄고 분수는 올랐다. Weber 법칙의 어느 절반이 살아남았고 어느 절반이 죽었는가? (b) 어떤 장치가 $5.2\,\mathrm{N}$ 대 $5.0\,\mathrm{N}$을 반사하고 논문이 모든 참가자가 알아챈다고 주장한다. §6의 숫자로, 정확히 무엇이 틀렸는가? (c) 다른 논문이 "사용자가 250 Hz 진동을 검출했으므로 그 cue가 삽입을 개선했다"고 한다. 인과 사슬의 어느 화살표를 건너뛰었고, 각각에서 무엇을 재겠는가? (d) 센서 둘, $\sigma_v=2\,\mathrm{mm}$와 $\sigma_h=4\,\mathrm{mm}$를 정밀도 가중으로 융합한다. $\hat x$를 쓰고, "시각이 우세하므로 햅틱 잡음은 상관없다"가 모델에서 무엇을 떨어뜨렸는지 말하라.

> [!tip]- 정답 · Solutions
> 1. 패널 A는 힘 라벨 둘 말고는 그대로다. 사슬, 핸들 상수, 타임라인은 같은 대상이다. 패널 B에는 $p=0.100,0.250,0.450,0.675,0.850,0.950$의 새 점 여섯이 들어간다. $p=0.25$ 선이 시험한 수준에서 데이터를 정확히 만나므로, 그 발은 구간 안이 아니라 찍은 점 위에 떨어진다.
> 2. (a) $p=0.250$은 $1.85\,\mathrm{N}$에서 측정된 비율 *그 자체*이므로 $x_{25}=1.85\,\mathrm{N}$, 보간이 없다. 기준이 시험한 수준과 일치했다. $x_{50}=2.00+0.15(0.500-0.450)/(0.675-0.450)=2.00+0.15(0.2222)=2.0333\,\mathrm{N}$. $x_{75}=2.15+0.15(0.750-0.675)/(0.850-0.675)=2.15+0.15(0.4286)=2.2143\,\mathrm{N}$. (b) $\mathrm{JND}=(2.2143-1.85)/2=0.3643/2=0.1821\,\mathrm{N}$, $k=0.1821/2.0333=0.0896$, 즉 $9.0\%$. (c) $\mathrm{PSE}-F_{\text{ref}}=2.0333-2.00=+0.0333\,\mathrm{N}$(33 mN). 5 N일 때보다 절대 편향은 작지만 JND 대비로는 크다. (d) $0.1821/0.0245=7.4$ 카운트, $0.1821/400=4.55\times10^{-4}\,\mathrm{m}=0.46\,\mathrm{mm}$ 침투. 양자화 대비 여유가 약 17 카운트에서 약 7 카운트로 절반 넘게 줄었다. 아직 넉넉하지만, 저힘 실험이 언젠가 하드웨어 실험으로 바뀌는 방향이 이쪽이다.
> 3. (a) 정성적 절반은 살아남았다. 기준이 $5.04\to2.03\,\mathrm{N}$로 내려가자 절대 증분도 $0.4107\to0.1821\,\mathrm{N}$로 줄었다. 정량적 절반은 죽었다. $k$가 $8.14\%$에서 $8.96\%$로 올랐으므로 이 범위에서 $\Delta I/I$는 상수가 아니다. Weber 법칙은 국소 근사이고 이 두 작동점은 같은 국소가 아니다. (b) $5.2$ 대 $5.0$은 $0.2\,\mathrm{N}$ 차이이고 JND는 $0.41\,\mathrm{N}$이다. JND의 절반쯤이라 불확실 구간 안이며, 정확히 1 JND라 해도 그 관례는 한 참가자 곡선의 75% 점을 고정할 뿐이다. "모든 참가자"도 "알아챈다"도 따라 나오지 않는다. (c) 검출 $\to$ 행동 $\to$ 과제 결과. 전달된 피부 자극(명령이 아님), 제어 행동(접촉력, 타이밍), 삽입 결과를 따로 잰다. 검출은 세 고리 중 하나다. (d) $\hat x=(\sigma_v^{-2}x_v+\sigma_h^{-2}x_h)/(\sigma_v^{-2}+\sigma_h^{-2})=\tfrac45x_v+\tfrac15x_h$. 가중은 $4:1$이지 $1:0$이 아니므로, "우세"는 햅틱 항과 가정 목록(가우시안, 독립, 시간 정렬)을 함께 떨어뜨렸다.
