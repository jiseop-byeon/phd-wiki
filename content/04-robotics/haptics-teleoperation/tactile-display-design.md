---
title: 24.2 Tactile Display Design
tags: [haptics, tactile, hri]
study-depth: Working
wiki-support: Working
depth-goal: "Derive what a frozen vibrotactile actuator actually delivers to skin at two frequencies, and what its array spacing can and cannot resolve, before choosing a tactile actuation family from the perceptual variable, body site, bandwidth, workspace, and task."
mastery-when: "Master transducer dynamics and psychophysical validation when the tactile display is the research contribution."
---

> [!note] Prerequisites · 선수 지식
> Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the handle is the delivery device that carries the tactor. A second-order mass–spring–damper and its magnitude response from [[04-robotics/control-theory-ce397|5. Control Theory §5]], and the idea of a transfer function from [[02-foundations/signal-processing|6. Signal Processing]]. Detection thresholds and the JND from [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §2]].
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3**. 핸들이 tactor를 싣는 전달 장치다. 2차 질량–스프링–댐퍼와 그 크기 응답은 [[04-robotics/control-theory-ce397|5. 제어 이론 §5]], 전달함수 개념은 [[02-foundations/signal-processing|6. 신호처리]]. 검출 임계값과 JND는 [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §2]].

## English

*The actuation end of the haptics track. Uses plant **P3** as the thing the skin is in contact with; [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]] is the same handle used to measure the person instead of to drive them.*

### Running object · 이 페이지의 대상

One frozen display, defined here and unchanged for the rest of the page. **Every value in it is an illustrative number this page defines so the arithmetic is exact. It is not a datasheet, and it is not anyone's measurement.**

**Where it sits: on plant P3.** The 1-DoF translating handle of [[02-foundations/lab-plants|0.6 Lab Plants]] is the delivery device, and a voice-coil tactor is bonded into its grip, so one handle drives two paths at once. The kinesthetic path keeps the catalog numbers — effective mass $m=0.04\,\mathrm{kg}$, virtual wall $k_w=400\,\mathrm{N/m}$ at $x_w=0.030\,\mathrm{m}$ — and the tactile path is the device below. Keep the two apart: the tactor's $4\,\mathrm{g}$ moving mass is a different mass from the handle's $0.04\,\mathrm{kg}$, and a force delivered to skin is not the force delivered to the arm.

**T1 — the tactor.**

| Symbol | Value | Meaning |
|---|---:|---|
| $m_t$ | $0.0040\,\mathrm{kg}$ | moving mass, coil plus contactor |
| $k_t$ | $1580\,\mathrm{N/m}$ | suspension stiffness |
| $\zeta$ | $0.25$ | damping ratio |
| $k_f$ | $0.30\,\mathrm{N/A}$ | coil force constant |
| $i_{\max}$ | $0.10\,\mathrm{A}$ | amplifier current limit |
| contactor | $6\,\mathrm{mm}$ flat disc | what touches skin |

**T2 — the skin, as exactly two numbers.** At this site and preload, the detection threshold in *displacement amplitude* is $1.0\,\mu\mathrm{m}$ at $100\,\mathrm{Hz}$ and $0.20\,\mu\mathrm{m}$ at $250\,\mathrm{Hz}$. The only property of the skin this page uses is that ratio, $5{:}1$ in favour of $250\,\mathrm{Hz}$.

**T3 — the sleeve.** A tactor sleeve wrapped around the handle grip, circumference $C=100\,\mathrm{mm}$, worn against the palmar skin of the closed hand, whose illustrative two-point limen is $d_2=10\,\mathrm{mm}$. A forearm strap at the same circumference would have $d_2=35\,\mathrm{mm}$.

§6 says what to draw and §7 works T1–T3 end to end; the problem set retunes the suspension and moves the sleeve.

### 1. Start from the information, not the actuator

A tactile display deliberately stimulates skin. A kinesthetic display primarily applies force or motion to a limb, although its handle also stimulates skin. Before choosing hardware, write the target variable: contact onset, direction, slip, roughness, local shape, friction, softness, or temperature. Then ask whether realism or discriminable communication is the goal.

| Display family | Controlled cue | Strength | Typical limitation |
|---|---|---|---|
| ERM (eccentric rotating mass) “rumble” motor | coupled vibration frequency/amplitude | cheap, salient | slow envelope; frequency and amplitude coupled |
| LRA (linear resonant actuator) / voice coil / piezo | shaped vibration | faster, richer waveform | resonance, stroke, mounting dependence |
| tactor array | spatial-temporal pattern | direction and alerts | masking, wiring, body-site acuity |
| skin stretch / shear | tangential deformation | direction, slip, friction illusion | preload and no-slip contact must be controlled |
| pin/shape display | pressure distribution/local shape | spatial form | actuator density, bulk, bandwidth |
| variable-friction surface | friction during active scan | texture on flat screens | requires finger motion and tracking |
| Peltier thermal display | heat flow/temperature cue | material and temperature cues | slow dynamics, heat sinking, safety |

### 2. A waveform is not a percept

For a sinusoid $a(t)=A\sin(2\pi ft)$, the physical variables include frequency, amplitude, phase, duration, attack/decay envelope, body site, contact area, and preload. Perception depends on all of them. Equal motor voltage does not imply equal skin acceleration, and equal acceleration does not imply equal perceived magnitude across frequencies.

An eccentric rotating mass produces centrifugal force approximately proportional to $m r\omega^2$; changing speed changes both frequency and force amplitude. An LRA or voice-coil actuator offers more independent waveform control but is shaped by its own transfer function (how much it amplifies and delays each input frequency; see [[02-foundations/signal-processing#5. Bridge to control: transforms|Signal Processing §5]]), for example a large response near its resonance and a weak one away from it. Therefore characterize **the acceleration or skin displacement at the contact site**, not merely the command signal.

**Three terms, defined.** The first two belong to the hardware, the third to the pair of hardware and person, and confusing them is how "we drove it at 250 Hz" becomes a perceptual claim. §7 computes all three on T1 and T2.

- **Magnitude response** $Z(f)$ — a *function of frequency*, not a number: the steady-state amplitude of the output per unit amplitude of a sinusoidal input, at each frequency separately. It is defined only for a linear, time-invariant system driven long enough to settle. *Example*: the contactor displacement per newton of coil force, computed in §7 Step 3. *Non-example*: the command amplitude, which is the same at every frequency by construction and therefore carries no information about what the skin received. It matters because a constant command through a non-constant $Z$ is a *varying* stimulus, which is the whole content of "a waveform is not a percept".
- **Resonance frequency** $f_0$ — the *frequency at which an underdamped second-order system's response peaks*, set by its own mass and stiffness and not by the drive:

$$f_0=\frac{1}{2\pi}\sqrt{\frac{k_t}{m_t}},$$

so it moves only if you change the suspension or the moving mass, which is exactly the knob the problem set turns. *Non-example*: the frequency the designer wants to display. A tactor driven far from $f_0$ is not broken; it is quieter, by an amount §7 computes.

- **Sensation level (SL)** — the *amount by which a delivered stimulus exceeds that person's detection threshold at that frequency*, in decibels:

$$\mathrm{SL}=20\log_{10}\frac{Z}{Z_{\text{th}}},$$

because the stimulus and the threshold are amplitudes, so the field convention of $20\log_{10}$ applies. $\mathrm{SL}=0$ is threshold and negative SL is undetectable. *Non-example*: the amplitude alone. Two frequencies at the same displacement are not equally strong, because $Z_{\text{th}}$ differs between them — which is why SL, and not micrometres, is what may be compared across frequencies.

### 3. Spatial and temporal design

Two nearby stimuli can merge, mask one another, or create apparent motion depending on spacing and timing. Acuity differs sharply between fingertip, palm, forearm, torso, and hairy skin. A wearable array must be tested in its actual placement, under motion and workload. Use a small vocabulary of well-separated signals before increasing symbol count; multidimensional scaling (placing the patterns as points on a map whose distances match how different users judge them) or confusion matrices (a table counting how often pattern A was reported as pattern B) reveal which patterns users actually distinguish.

**Two-point limen, defined.** The **two-point limen** $d_2$ is a *distance*: the smallest separation at which two simultaneous contacts are reported as two rather than one. Its defining conditions are all external to the device — a named body site, contactor size and shape, contact force, and the judgement asked for — so a single number is meaningless without them, and the same skin gives different values under different conditions. *Example*: the $10\,\mathrm{mm}$ of T3, an illustrative value for the palmar hand. *Non-example*: the array pitch, which is a property you chose when you drew the sleeve and which says nothing about what can be told apart. It matters because $d_2$ caps the number of *locations* a spatial vocabulary can use, whatever the actuator count, and §7 Step 8 turns that cap into bits.

### 4. Contact, slip, and material cues

Humans regulate grip before gross slip using distributed pressure, skin stretch, vibration, and prior knowledge. A teleoperator that returns only normal force omits much of this evidence. Contact-location devices move a contact patch; shear devices deform skin without gross slip; vibration can reproduce impact transients; variable-friction displays alter tangential force during exploration. No single cue is “touch.”

For hard contact, a low-frequency force loop and a short high-frequency transient may be combined. This can improve perceived hardness without demanding an unrealistically stiff stable virtual spring (a sampled spring can be rendered stably only up to a stiffness set by the device damping and the sample period; see [[04-robotics/haptics-teleoperation/rendering-sampling-stability#2. Why a digital spring can create energy|24.4 §2]]), but the transient is open-loop energy and must remain within device and safety limits.

### 5. Design checklist

1. What physical event should the user detect or estimate?
2. Which skin site remains in reliable contact during the task?
3. What stimulus dimensions can the hardware control independently?
4. What is the measured transfer from command to skin?
5. Are patterns distinguishable under task workload, not just in isolation?
6. Does the cue improve a decision or task outcome, and what false alarms does it create?

**Worked: the three readings the homework asks.** “250 Hz on an ERM” still leaves amplitude, envelope, preload, area, site free; independent amplitude wants an LRA/voice coil/piezo because ERM couples $F\propto\omega^2$. Equal voltage is not equal percept across frequency. Table-top array then worn forearm skips contact reliability and workload; discriminability typically collapses.

### 6. Homework diagram

One figure, two panels, and the problem set asks for the same figure with the suspension retuned and the sleeve moved.

**Panel A — what reaches the skin.** Log–log axes: frequency from 20 to 1000 Hz across, displacement amplitude from $0.1$ to $100\,\mu\mathrm{m}$ up. Draw the T1 magnitude response $Z(f)$: flat and low at the left, a peak at $f_0=100\,\mathrm{Hz}$, then a falling tail. Mark the two operating points with their values, $(100\,\mathrm{Hz},\,38.0\,\mu\mathrm{m})$ and $(250\,\mathrm{Hz},\,3.52\,\mu\mathrm{m})$. On the same axes plot the two frozen T2 thresholds, $(100\,\mathrm{Hz},\,1.0\,\mu\mathrm{m})$ and $(250\,\mathrm{Hz},\,0.20\,\mu\mathrm{m})$, and join them with a dashed line. Shade the vertical gap above each threshold point and write the sensation level in it. Along the top, draw the command as a flat line labelled $i_{\max}=0.10\,\mathrm{A}$ at both frequencies: the point of the panel is that the flat line at the top produces the unflat curve below it.

**Panel B — what can be told apart.** Unroll the sleeve into a straight $100\,\mathrm{mm}$ line. Put 16 tactor marks on it at $6.25\,\mathrm{mm}$ pitch and draw each contactor to scale as a $6\,\mathrm{mm}$ disc, so the $0.25\,\mathrm{mm}$ gaps are visible. Underneath, draw a second ruler divided into $d_2=10\,\mathrm{mm}$ segments and bracket the tactors that fall inside each one. Write the two counts side by side: 16 actuators, 10 resolvable sites. Neither panel may be drawn from the command; both are drawn from the delivered quantity.

### 7. Worked case: what T1 delivers, and what T3 can resolve

**Step 1 — the model.** Treat the tactor as one mass on a suspension, driven by the coil force and moving against the grip, with $z$ the contactor displacement:

$$m_t\ddot z+c_t\dot z+k_tz=F_0\sin(2\pi ft),$$

so the only unknowns are the drive amplitude $F_0$ and the damping coefficient $c_t$, since $m_t$ and $k_t$ are frozen in T1.

**Step 2 — the three constants.** The amplifier limit fixes the force, the damping ratio fixes the damper, and the suspension fixes the peak:

$$F_0=k_fi_{\max}=0.30(0.10)=0.030\ \mathrm{N},\qquad c_t=2\zeta\sqrt{k_tm_t}=0.5\sqrt{1580(0.0040)}=0.5\sqrt{6.32}=1.2570\ \mathrm{N\cdot s/m},$$

and $f_0=\frac{1}{2\pi}\sqrt{k_t/m_t}=\frac{1}{2\pi}\sqrt{395000}=100.0\,\mathrm{Hz}$, which is why 100 Hz was chosen as one of the two test frequencies.

**Step 3 — the magnitude response.** For the steady sinusoid, the displacement amplitude is the drive divided by the magnitude of the complex stiffness,

$$Z(f)=\frac{F_0}{\sqrt{(k_t-m_t\omega^2)^2+(c_t\omega)^2}},\qquad \omega=2\pi f,$$

where $k_t-m_t\omega^2$ is the spring fighting the inertia and $c_t\omega$ is the damper, so at resonance the first term vanishes and only damping limits the motion.

**Step 4 — at 100 Hz.** $\omega=628.32\,\mathrm{rad/s}$, so $m_t\omega^2=0.0040(394784)=1579.14$ and $k_t-m_t\omega^2=1580-1579.14=0.86\,\mathrm{N/m}$, while $c_t\omega=1.2570(628.32)=789.78\,\mathrm{N/m}$. The spring–inertia term is three orders of magnitude smaller, so the denominator is $\sqrt{0.86^2+789.78^2}=789.78$ and

$$Z(100)=\frac{0.030}{789.78}=3.80\times10^{-5}\ \mathrm{m}=38.0\ \mu\mathrm{m},$$

which the resonance shortcut $F_0/(2\zeta k_t)=0.030/790=3.80\times10^{-5}\,\mathrm{m}$ confirms. The acceleration amplitude is $a=\omega^2Z=394784(3.80\times10^{-5})=15.0\,\mathrm{m/s^2}$, i.e. $1.53\,g$.

**Step 5 — at 250 Hz, same current.** $\omega=1570.80\,\mathrm{rad/s}$, so $m_t\omega^2=0.0040(2467401)=9869.60$ and $k_t-m_t\omega^2=1580-9869.60=-8289.60\,\mathrm{N/m}$: past resonance the inertia now dominates the spring. With $c_t\omega=1.2570(1570.80)=1974.46$, the denominator is $\sqrt{8289.60^2+1974.46^2}=8521.50$ and

$$Z(250)=\frac{0.030}{8521.50}=3.52\times10^{-6}\ \mathrm{m}=3.52\ \mu\mathrm{m},$$

with acceleration $a=2467401(3.52\times10^{-6})=8.69\,\mathrm{m/s^2}$, i.e. $0.885\,g$.

**Step 6 — the same command, two different stimuli, and two different stories.** The current was identical, yet

$$\frac{Z(100)}{Z(250)}=\frac{38.0}{3.52}=10.8\quad(20.7\ \mathrm{dB}),\qquad\frac{a(100)}{a(250)}=\frac{15.0}{8.69}=1.73\quad(4.7\ \mathrm{dB}),$$

because acceleration carries the factor $\omega^2$ that displacement does not. A paper reporting displacement says the 250 Hz cue is eleven times weaker; the same device reported in acceleration says it is less than twice as weak. Neither is wrong, and neither is a perceptual claim, which is why §2 insists on naming the delivered variable.

**Step 7 — against the skin.** Applying §2's definition to T2's two thresholds,

$$\mathrm{SL}(100)=20\log_{10}\frac{38.0}{1.0}=31.6\ \mathrm{dB},\qquad \mathrm{SL}(250)=20\log_{10}\frac{3.52}{0.20}=24.9\ \mathrm{dB},$$

so the 250 Hz cue is only $6.7\,\mathrm{dB}$ weaker to the person even though its displacement is $20.7\,\mathrm{dB}$ smaller, since the skin's threshold is five times lower there, worth $20\log_{10}5=14.0\,\mathrm{dB}$, and $20.7-14.0=6.7$. The actuator's rolloff and the skin's sensitivity point in opposite directions and largely cancel — which is the real reason a device can be usable at a frequency its own response curve seems to forbid, and the reason the problem set's retuning buys less than it looks like it should.

**Step 8 — the spatial limit, which the electronics cannot move.** With $d_2=10\,\mathrm{mm}$ on a $C=100\,\mathrm{mm}$ sleeve, the number of sites that can be told apart is

$$N_{\max}=\left\lfloor\frac{C}{d_2}\right\rfloor=\left\lfloor\frac{100}{10}\right\rfloor=10,$$

so a 16-tactor sleeve has a pitch of $C/16=6.25\,\mathrm{mm}$, which is below the limen, and six of its actuators buy no new location. In information terms the design claims $\log_2 16=4.00$ bits per single-site pattern and supports at most $\log_2 10=3.32$ bits. The $6\,\mathrm{mm}$ contactors at that pitch also leave only $0.25\,\mathrm{mm}$ between neighbours, so they additionally couple through the sleeve and the skin, which degrades the vocabulary further rather than leaving it at 10.

**Step 9 — the two limits are not the same kind of thing.** Step 6's shortfall is a *transducer* limit: more current, a different suspension, or a different actuator family moves it. Step 8's is a *receiver* limit, fixed by the site you chose, and no actuator quality moves it at all. A design review that answers a spatial-resolution objection with a better amplifier has confused the two.

### Self-check

1. Step 6 gives two honest summaries of the same 250 Hz cue on T1: eleven times weaker, and less than twice as weak. Which delivered variable is each one reporting, and is either of them a perceptual claim?
2. Step 7 finds the 250 Hz cue only $6.7\,\mathrm{dB}$ down *to the person* although its displacement is $20.7\,\mathrm{dB}$ down. Where did the other $14.0\,\mathrm{dB}$ go, and what does that say about reading a tactor's response curve as a usability limit?
3. A reviewer objects that the sleeve's 16 tactors deliver only 10 distinguishable sites, and the team proposes a higher-current amplifier. Why can that proposal not work, whatever current it buys?
4. Why is a 250 Hz command not enough to specify a tactile stimulus?

> [!tip]- Answers
> 1. The first reports **displacement**, $38.0$ against $3.52\,\mu\mathrm{m}$, a ratio of $10.8$; the second reports **acceleration**, $15.0$ against $8.69\,\mathrm{m/s^2}$, a ratio of $1.73$. They differ by exactly the $\omega^2$ that acceleration carries and displacement does not, $(250/100)^2=6.25$, and $10.8/6.25=1.73$. Neither is a perceptual claim: both are properties of T1 alone, and nothing about the skin has entered yet. Naming the delivered variable is therefore part of the measurement, not a formatting choice.
> 2. Into T2. The skin's detection threshold is five times lower at $250\,\mathrm{Hz}$ than at $100\,\mathrm{Hz}$, worth $20\log_{10}5=14.0\,\mathrm{dB}$, and $20.7-14.0=6.7$. The actuator's rolloff and the receiver's rising sensitivity point in opposite directions and mostly cancel, so a response curve alone cannot say where a device stops being usable — only sensation level, which is the curve measured against that person's threshold at each frequency, can. This is also why the problem set's retuning buys so little: $4.7\,\mathrm{dB}$ gained at 250 Hz against $20.7\,\mathrm{dB}$ lost at 100 Hz.
> 3. Because the binding limit is in the receiver, not the transducer. $N_{\max}=\lfloor C/d_2\rfloor=\lfloor100/10\rfloor=10$ contains no actuator quantity at all: it is the sleeve circumference divided by the two-point limen of the chosen skin site. More current raises sensation level, which Step 6's ceiling is about, and moves nothing in Step 8. The design claims $\log_2 16=4.00$ bits and supports $\log_2 10=3.32$; only a longer path on the skin, a more acute site, or a vocabulary that stops relying on single-site location closes that gap.
> 4. The actuator and mounting determine delivered acceleration and displacement; preload, contact area, body site, waveform envelope, and individual sensitivity determine perception. Frequency is only one coordinate, and on T1 the same command at two frequencies delivers stimuli an order of magnitude apart.

### Problem set · 과제

Tier B. Using **P3** from [[02-foundations/lab-plants|0.6]], T1–T3 above, and this page. Hand calculation only; no simulator.

Two knobs move, nothing else. The suspension is stiffened to $k_t'=9860\,\mathrm{N/m}$ with the same moving mass, damping ratio, force constant and current limit; and the sleeve, still $C=100\,\mathrm{mm}$, is moved from the hand to a forearm strap where the illustrative two-point limen is $d_2'=35\,\mathrm{mm}$.

1. **Draw.** Redraw §6's panel A for the stiffened tactor on the same axes as the original, keeping the old curve as a faint line so the two crossings are visible, and redraw panel B for the forearm strap with the same 16 tactors.
2. **Derive.** (a) The new $c_t'$ and $f_0'$. (b) $Z'(100)$ and $Z'(250)$, with the spring–inertia and damping terms shown separately as in Steps 4 and 5. (c) The two sensation levels. (d) How many decibels the retuning gained at 250 Hz and how many it lost at 100 Hz. (e) $N_{\max}'$ and the bits available on the forearm.
3. **Interpret.** (a) The retuning moved $f_0$ onto the frequency where the skin is most sensitive. Using (c) and (d), was it a good trade, and what would have to be true about the intended signal for the answer to flip? (b) A team specifies its cue as "250 Hz on an ERM". Which physical variables are still free, and why is the ERM the wrong family if they need amplitude independent of frequency? (c) The same sleeve is validated on a table and then worn on a moving forearm under a real task. Which two design-checklist items of §5 were skipped, and what happens to the vocabulary — before any of §7 Step 8's arithmetic is applied?

> [!tip]- Solutions
> 1. Panel A: the peak moves to 250 Hz and drops, because a stiffer suspension both shifts $f_0$ and reduces the resonant amplitude $F_0/(2\zeta k_t)$; the two curves cross between the operating points. Panel B: the same 16 marks at $6.25\,\mathrm{mm}$, but the ruler beneath now has $35\,\mathrm{mm}$ segments, so only two brackets fit across the sleeve.
> 2. (a) $c_t'=0.5\sqrt{9860(0.0040)}=0.5\sqrt{39.44}=3.1401\,\mathrm{N\cdot s/m}$ and $f_0'=\frac{1}{2\pi}\sqrt{9860/0.0040}=\frac{1}{2\pi}\sqrt{2465000}=249.9\,\mathrm{Hz}$. (b) At 100 Hz: $k_t'-m_t\omega^2=9860-1579.14=8280.86$, $c_t'\omega=1972.96$, denominator $8512.65$, so $Z'(100)=0.030/8512.65=3.52\times10^{-6}\,\mathrm{m}=3.52\,\mu\mathrm{m}$. At 250 Hz: $k_t'-m_t\omega^2=9860-9869.60=-9.60$, $c_t'\omega=4932.40$, denominator $4932.41$, so $Z'(250)=0.030/4932.41=6.08\times10^{-6}\,\mathrm{m}=6.08\,\mu\mathrm{m}$, which the shortcut $0.030/(2(0.25)(9860))=6.09\times10^{-6}$ confirms. (c) $\mathrm{SL}'(100)=20\log_{10}(3.52/1.0)=10.9\,\mathrm{dB}$ and $\mathrm{SL}'(250)=20\log_{10}(6.08/0.20)=29.7\,\mathrm{dB}$. (d) Gained $29.7-24.9=4.7\,\mathrm{dB}$ at 250 Hz; lost $31.6-10.9=20.7\,\mathrm{dB}$ at 100 Hz. (e) $N_{\max}'=\lfloor100/35\rfloor=2$ sites, so $\log_2 2=1.00$ bit against the 4.00 bits the 16 tactors were meant to carry.
> 3. (a) A bad trade for any signal that uses both frequencies: $4.7\,\mathrm{dB}$ bought at 250 Hz cost $20.7\,\mathrm{dB}$ at 100 Hz, and the reason the gain is so small is Step 7 — the skin had already paid back most of the old rolloff. It flips only if the display is genuinely single-frequency near 250 Hz, where the lost band costs nothing, or if $10.9\,\mathrm{dB}$ at 100 Hz still clears the margin the task needs under workload. (b) Amplitude, envelope, duration, preload, contact area, and body site are all still free. An ERM couples frequency to force, $F\propto\omega^2$, so amplitude cannot be set independently; that needs an LRA, voice coil, or piezo. (c) Checklist items 2 and 5: which skin site stays in reliable contact during the task, and whether patterns remain distinguishable under workload. Preload is lost and regained as the arm moves, masking rises, and the table-top vocabulary collapses — the arithmetic of Step 8 gives an *upper* bound of 2 sites on the forearm, and losing contact reliability means the worn system does not even reach it.

## 한국어

*햅틱 트랙의 구동 쪽 끝이다. 장치 **P3**를 피부가 닿아 있는 물체로 쓴다. [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]]은 같은 핸들을 사람을 구동하는 대신 사람을 재는 데 쓴 페이지다.*

### 이 페이지의 대상 · Running object

얼어붙은 디스플레이 하나를 여기서 정의하고 페이지 끝까지 바꾸지 않는다. **안의 모든 값은 계산이 딱 떨어지도록 이 페이지에서 정의한 예시 숫자다. 데이터시트가 아니고, 누군가의 측정값도 아니다.**

**어디에 놓이나: 장치 P3 위.** [[02-foundations/lab-plants|0.6 Lab Plants]]의 1자유도 병진 핸들이 전달 장치이고, 그 그립 안에 voice-coil tactor를 붙인다. 그래서 핸들 하나가 두 경로를 동시에 구동한다. 역각 경로는 카탈로그 숫자를 그대로 쓴다. 유효 질량 $m=0.04\,\mathrm{kg}$, 가상 벽 $k_w=400\,\mathrm{N/m}$, 벽 위치 $x_w=0.030\,\mathrm{m}$. 촉각 경로는 아래 장치다. 둘을 섞지 마라. tactor의 $4\,\mathrm{g}$ 가동 질량은 핸들의 $0.04\,\mathrm{kg}$와 다른 질량이고, 피부에 전달된 힘은 팔에 전달된 힘이 아니다.

**T1 — tactor.**

| 기호 | 값 | 뜻 |
|---|---:|---|
| $m_t$ | $0.0040\,\mathrm{kg}$ | 가동 질량, 코일과 접촉자 |
| $k_t$ | $1580\,\mathrm{N/m}$ | 서스펜션 강성 |
| $\zeta$ | $0.25$ | 감쇠비 |
| $k_f$ | $0.30\,\mathrm{N/A}$ | 코일 힘 상수 |
| $i_{\max}$ | $0.10\,\mathrm{A}$ | 증폭기 전류 한계 |
| 접촉자 | 지름 $6\,\mathrm{mm}$ 평면 원판 | 피부에 닿는 면 |

**T2 — 피부, 숫자 딱 둘.** 이 부위와 이 예압에서 *변위 진폭* 기준 검출 임계값은 $100\,\mathrm{Hz}$에서 $1.0\,\mu\mathrm{m}$, $250\,\mathrm{Hz}$에서 $0.20\,\mu\mathrm{m}$다. 이 페이지가 피부에서 쓰는 성질은 그 비 $5{:}1$, 즉 $250\,\mathrm{Hz}$ 쪽이 유리하다는 것뿐이다.

**T3 — 슬리브.** 핸들 그립을 감는 tactor 슬리브, 둘레 $C=100\,\mathrm{mm}$. 착용 부위는 손을 쥐었을 때의 손바닥 피부이고, 예시 two-point limen은 $d_2=10\,\mathrm{mm}$다. 같은 둘레의 팔뚝 밴드라면 $d_2=35\,\mathrm{mm}$가 된다.

§6이 무엇을 그릴지 말하고 §7이 T1–T3를 끝까지 계산한다. 과제는 서스펜션을 다시 튜닝하고 슬리브를 옮긴다.

### 1. 액추에이터가 아니라 정보에서 시작한다

Tactile display는 피부를 의도적으로 자극한다. Kinesthetic display는 주로 사지에 힘이나 운동을 가하지만, 그 손잡이도 피부를 자극한다. 하드웨어를 고르기 전에 목표 변수를 적어라. 접촉 시작, 방향, 미끄럼, 거칠기, 국소 형상, 마찰, 부드러움, 온도 중 무엇인가. 그다음 사실적 재현이 목적인지 구별 가능한 전달이 목적인지 물어라.

| 디스플레이 계열 | 제어하는 cue | 강점 | 통상적 한계 |
|---|---|---|---|
| ERM(편심 회전 질량) "럼블" 모터 | 결합된 진동 주파수·진폭 | 싸고 뚜렷함 | 느린 포락선. 주파수와 진폭이 묶임 |
| LRA(선형 공진 액추에이터) · voice coil · 피에조 | 성형된 진동 | 더 빠르고 풍부한 파형 | 공진, 스트로크, 장착 의존성 |
| Tactor 배열 | 시공간 패턴 | 방향과 경보 | masking, 배선, 부위별 예민도 |
| 피부 신장 · 전단 | 접선 방향 변형 | 방향, 미끄럼, 마찰 착시 | 예압과 미끄러지지 않는 접촉을 통제해야 함 |
| 핀 · 형상 디스플레이 | 압력 분포 · 국소 형상 | 공간적 형태 | 액추에이터 밀도, 부피, 대역폭 |
| 가변 마찰 표면 | 능동 스캔 중의 마찰 | 평평한 화면 위의 질감 | 손가락 운동과 추적이 필요 |
| 펠티에 열 디스플레이 | 열 흐름 · 온도 cue | 재질과 온도 cue | 느린 동역학, 방열, 안전 |

### 2. 파형은 지각이 아니다

사인파 $a(t)=A\sin(2\pi ft)$에서 물리 변수는 주파수, 진폭, 위상, 지속 시간, attack·decay 포락선, 신체 부위, 접촉 면적, 예압을 포함한다. 지각은 그 전부에 달려 있다. 같은 모터 전압이 같은 피부 가속도를 뜻하지 않고, 같은 가속도가 주파수를 가로질러 같은 지각 크기를 뜻하지도 않는다.

편심 회전 질량은 대략 $mr\omega^2$에 비례하는 원심력을 만든다. 속도를 바꾸면 주파수와 힘 진폭이 함께 바뀐다. LRA나 voice coil 액추에이터는 파형을 더 독립적으로 제어하게 해 주지만 자기 전달함수(입력 주파수마다 얼마나 증폭하고 지연시키는가. [[02-foundations/signal-processing#5. 제어로 가는 다리: 변환|신호 처리 §5]] 참고)에 의해 성형된다. 예를 들어 공진 근처에서는 크게, 공진에서 먼 곳에서는 약하게 반응한다. 그러므로 명령 신호가 아니라 **접촉점에서의 가속도나 피부 변위**를 특성화하라.

**세 용어의 정의.** 앞의 둘은 하드웨어의 것이고 셋째는 하드웨어와 사람이 이루는 쌍의 것이다. 이 셋을 섞는 순간 "250 Hz로 구동했다"가 지각에 관한 주장으로 둔갑한다. §7이 T1과 T2 위에서 셋을 모두 계산한다.

- **크기 응답** $Z(f)$ — 숫자가 아니라 *주파수의 함수*다. 정현 입력의 단위 진폭당 정상상태 출력 진폭을, 주파수마다 따로. 선형 시불변 시스템이 정착할 만큼 길게 구동될 때만 정의된다. *예*: §7 Step 3에서 계산하는, 코일 힘 1 N당 접촉자 변위. *반례*: 명령 진폭. 설계상 모든 주파수에서 같으므로 피부가 무엇을 받았는지에 대해 아무 정보도 나르지 않는다. 중요한 이유는, 일정한 명령이 일정하지 않은 $Z$를 통과하면 *변하는* 자극이 되기 때문이다. "파형은 지각이 아니다"의 내용이 통째로 이것이다.
- **공진 주파수** $f_0$ — *부족감쇠 2차 시스템의 응답이 가장 커지는 주파수*다. 구동이 아니라 자기 질량과 강성이 정한다:

$$f_0=\frac{1}{2\pi}\sqrt{\frac{k_t}{m_t}},$$

그러므로 서스펜션이나 가동 질량을 바꿀 때만 움직이고, 그것이 바로 과제가 돌리는 손잡이다. *반례*: 설계자가 표시하고 싶은 주파수. $f_0$에서 먼 곳에서 구동되는 tactor는 고장 난 것이 아니라 더 조용한 것이고, 그 양을 §7이 계산한다.

- **감각 수준(SL)** — *전달된 자극이 그 사람의 그 주파수 검출 임계값을 얼마나 넘는가*를 데시벨로 쓴 값이다:

$$\mathrm{SL}=20\log_{10}\frac{Z}{Z_{\text{th}}},$$

자극과 임계값이 모두 진폭이므로 이 분야의 관례인 $20\log_{10}$을 쓴다. $\mathrm{SL}=0$이 임계값이고 음수면 검출되지 않는다. *반례*: 진폭 하나만 보는 것. 변위가 같은 두 주파수가 똑같이 강하지 않은 이유는 $Z_{\text{th}}$가 다르기 때문이고, 그래서 주파수를 가로질러 비교할 수 있는 것은 마이크로미터가 아니라 SL이다.

### 3. 공간과 시간 설계

가까운 두 자극은 간격과 타이밍에 따라 합쳐지거나, 서로를 masking하거나, apparent motion을 만든다. 예민도는 손끝, 손바닥, 팔뚝, 몸통, 털 있는 피부 사이에서 크게 다르다. 착용형 배열은 실제 착용 위치에서, 움직임과 workload 아래에서 시험해야 한다. 기호 수를 늘리기 전에 충분히 떨어진 신호의 작은 어휘부터 쓰라. 다차원 척도법(사용자가 느끼는 차이가 거리와 맞도록 패턴들을 지도 위의 점으로 배치하는 방법)이나 혼동 행렬(패턴 A가 패턴 B로 보고된 횟수를 센 표)이 사용자가 실제로 구별하는 패턴을 드러낸다.

**Two-point limen의 정의.** **Two-point limen** $d_2$는 *거리*다. 동시에 닿은 두 접촉이 하나가 아니라 둘로 보고되는 최소 간격. 정의 조건이 전부 장치 바깥에 있다. 명시된 신체 부위, 접촉자의 크기와 모양, 접촉력, 그리고 무엇을 판단하게 했는가. 그래서 그 조건들 없는 단일 숫자는 뜻이 없고, 같은 피부도 조건이 달라지면 다른 값을 준다. *예*: T3의 $10\,\mathrm{mm}$, 손바닥 피부의 예시 값. *반례*: 배열 피치. 슬리브를 그릴 때 당신이 고른 값이고 무엇을 구별할 수 있는지에 대해 아무 말도 하지 않는다. 중요한 이유는 액추에이터 수와 무관하게 공간 어휘가 쓸 수 있는 *위치*의 수를 $d_2$가 제한하기 때문이고, §7 Step 8이 그 상한을 비트로 바꾼다.

### 4. 접촉, 미끄럼, 재질 cue

사람은 분포된 압력, 피부 신장, 진동, 사전 지식을 써서 큰 미끄럼이 나기 전에 파지력을 조절한다. 정상력만 돌려주는 원격조작기는 이 증거의 상당 부분을 빠뜨린다. 접촉 위치 장치는 접촉 패치를 움직이고, 전단 장치는 큰 미끄럼 없이 피부를 변형시키며, 진동은 충격 과도를 재현할 수 있고, 가변 마찰 디스플레이는 탐색 중 접선력을 바꾼다. 어느 한 cue도 "촉각"이 아니다.

단단한 접촉에는 저주파 힘 루프와 짧은 고주파 과도를 결합할 수 있다. 이렇게 하면 비현실적으로 뻣뻣한 안정 가상 스프링(샘플링된 스프링은 장치 감쇠와 샘플 주기가 정하는 강성까지만 안정하게 렌더링된다. [[04-robotics/haptics-teleoperation/rendering-sampling-stability#2. 디지털 스프링이 에너지를 만들 수 있는 이유|24.4 §2]] 참고)을 요구하지 않고도 지각되는 경도를 높일 수 있다. 다만 그 과도는 개루프 에너지이므로 장치와 안전의 한계 안에 머물러야 한다.

### 5. 설계 체크리스트

1. 사용자가 검출하거나 추정해야 할 물리적 사건은 무엇인가?
2. 과제 중에 믿을 만한 접촉을 유지하는 피부 부위는 어디인가?
3. 하드웨어가 독립적으로 제어할 수 있는 자극 차원은 무엇인가?
4. 명령에서 피부까지의 측정된 전달은 무엇인가?
5. 패턴이 고립된 상태가 아니라 과제 workload 아래에서 구별되는가?
6. 그 cue가 결정이나 과제 결과를 개선하는가, 그리고 어떤 오경보를 만드는가?

**계산해 읽기: 과제가 묻는 세 독해.** "ERM의 250 Hz"는 진폭·포락선·예압·면적·부위를 여전히 자유롭게 남긴다. 진폭을 독립적으로 쓰려면 LRA·voice coil·피에조가 필요하다. ERM은 $F\propto\omega^2$로 둘을 묶기 때문이다. 같은 전압은 주파수를 가로질러 같은 지각이 아니다. 탁자에서 시험한 배열을 팔뚝에 착용하는 것은 접촉 신뢰성과 workload를 건너뛴 것이고, 구별 성능은 보통 무너진다.

### 6. 과제가 그릴 그림

그림 하나, 패널 둘. 과제는 서스펜션을 다시 튜닝하고 슬리브를 옮긴 채 같은 그림을 그리라고 한다.

**패널 A — 피부에 도달하는 것.** 로그–로그 축. 가로는 주파수 20에서 1000 Hz, 세로는 변위 진폭 $0.1$에서 $100\,\mu\mathrm{m}$. T1의 크기 응답 $Z(f)$를 그린다. 왼쪽에서는 낮고 평평하다가 $f_0=100\,\mathrm{Hz}$에서 봉우리를 이루고 그 뒤로 떨어진다. 작동점 둘을 값과 함께 표시한다. $(100\,\mathrm{Hz},\,38.0\,\mu\mathrm{m})$과 $(250\,\mathrm{Hz},\,3.52\,\mu\mathrm{m})$. 같은 축 위에 얼어붙은 T2 임계값 둘, $(100\,\mathrm{Hz},\,1.0\,\mu\mathrm{m})$과 $(250\,\mathrm{Hz},\,0.20\,\mu\mathrm{m})$을 찍고 점선으로 잇는다. 각 임계값 위의 세로 간격을 칠하고 그 안에 감각 수준을 적는다. 맨 위에는 두 주파수에서 똑같은 명령을 평평한 선으로 그리고 $i_{\max}=0.10\,\mathrm{A}$라고 쓴다. 위의 평평한 선이 아래의 평평하지 않은 곡선을 만든다는 것이 이 패널의 요점이다.

**패널 B — 구별할 수 있는 것.** 슬리브를 길이 $100\,\mathrm{mm}$의 직선으로 펼친다. 그 위에 tactor 16개를 $6.25\,\mathrm{mm}$ 피치로 찍고, 접촉자 하나하나를 지름 $6\,\mathrm{mm}$ 원판으로 축척에 맞게 그려서 $0.25\,\mathrm{mm}$ 틈이 보이게 한다. 그 아래에 $d_2=10\,\mathrm{mm}$ 눈금의 두 번째 자를 그리고, 각 눈금 안에 들어가는 tactor들을 괄호로 묶는다. 두 숫자를 나란히 적는다. 액추에이터 16개, 구별되는 위치 10개. 어느 패널도 명령에서 그려서는 안 된다. 둘 다 전달된 양에서 그린다.

### 7. 대상으로 한 번 끝까지: T1이 전달하는 것과 T3가 구별하는 것

**Step 1 — 모델.** tactor를 서스펜션 위의 질량 하나로 보고, 코일 힘이 그것을 그립에 대해 구동한다고 하자. $z$를 접촉자 변위라 하면

$$m_t\ddot z+c_t\dot z+k_tz=F_0\sin(2\pi ft),$$

이고 $m_t$와 $k_t$는 T1에서 얼어 있으므로 미지수는 구동 진폭 $F_0$와 감쇠 계수 $c_t$뿐이다.

**Step 2 — 상수 셋.** 증폭기 한계가 힘을, 감쇠비가 댐퍼를, 서스펜션이 봉우리를 정한다:

$$F_0=k_fi_{\max}=0.30(0.10)=0.030\ \mathrm{N},\qquad c_t=2\zeta\sqrt{k_tm_t}=0.5\sqrt{1580(0.0040)}=0.5\sqrt{6.32}=1.2570\ \mathrm{N\cdot s/m},$$

그리고 $f_0=\frac{1}{2\pi}\sqrt{k_t/m_t}=\frac{1}{2\pi}\sqrt{395000}=100.0\,\mathrm{Hz}$다. 시험 주파수 둘 중 하나로 100 Hz를 고른 이유가 이것이다.

**Step 3 — 크기 응답.** 정상 정현파에서 변위 진폭은 구동력을 복소 강성의 크기로 나눈 값이다:

$$Z(f)=\frac{F_0}{\sqrt{(k_t-m_t\omega^2)^2+(c_t\omega)^2}},\qquad \omega=2\pi f,$$

여기서 $k_t-m_t\omega^2$은 관성과 싸우는 스프링, $c_t\omega$는 댐퍼다. 공진에서는 앞 항이 사라지고 감쇠만이 운동을 제한하기 때문이다.

**Step 4 — 100 Hz에서.** $\omega=628.32\,\mathrm{rad/s}$이므로 $m_t\omega^2=0.0040(394784)=1579.14$, $k_t-m_t\omega^2=1580-1579.14=0.86\,\mathrm{N/m}$, 그리고 $c_t\omega=1.2570(628.32)=789.78\,\mathrm{N/m}$다. 스프링–관성 항이 세 자릿수 작으므로 분모는 $\sqrt{0.86^2+789.78^2}=789.78$이고

$$Z(100)=\frac{0.030}{789.78}=3.80\times10^{-5}\ \mathrm{m}=38.0\ \mu\mathrm{m},$$

공진 지름길 $F_0/(2\zeta k_t)=0.030/790=3.80\times10^{-5}\,\mathrm{m}$이 이를 확인해 준다. 가속도 진폭은 $a=\omega^2Z=394784(3.80\times10^{-5})=15.0\,\mathrm{m/s^2}$, 즉 $1.53\,g$다.

**Step 5 — 같은 전류, 250 Hz에서.** $\omega=1570.80\,\mathrm{rad/s}$이므로 $m_t\omega^2=0.0040(2467401)=9869.60$, $k_t-m_t\omega^2=1580-9869.60=-8289.60\,\mathrm{N/m}$. 공진을 지나면 관성이 스프링을 압도한다. $c_t\omega=1.2570(1570.80)=1974.46$이므로 분모는 $\sqrt{8289.60^2+1974.46^2}=8521.50$이고

$$Z(250)=\frac{0.030}{8521.50}=3.52\times10^{-6}\ \mathrm{m}=3.52\ \mu\mathrm{m},$$

가속도는 $a=2467401(3.52\times10^{-6})=8.69\,\mathrm{m/s^2}$, 즉 $0.885\,g$다.

**Step 6 — 같은 명령, 다른 자극 둘, 다른 이야기 둘.** 전류는 똑같았는데도

$$\frac{Z(100)}{Z(250)}=\frac{38.0}{3.52}=10.8\quad(20.7\ \mathrm{dB}),\qquad\frac{a(100)}{a(250)}=\frac{15.0}{8.69}=1.73\quad(4.7\ \mathrm{dB})$$

이다. 가속도는 변위가 지고 있지 않은 $\omega^2$ 인자를 함께 지기 때문이다. 변위로 보고하는 논문은 250 Hz cue가 11배 약하다고 말하고, 같은 장치를 가속도로 보고하면 두 배도 안 약하다고 말한다. 둘 다 틀리지 않았고, 둘 다 지각에 관한 주장이 아니다. §2가 전달된 변수를 이름 붙이라고 고집하는 이유다.

**Step 7 — 피부에 대고 읽기.** §2의 정의를 T2의 임계값 둘에 적용하면

$$\mathrm{SL}(100)=20\log_{10}\frac{38.0}{1.0}=31.6\ \mathrm{dB},\qquad \mathrm{SL}(250)=20\log_{10}\frac{3.52}{0.20}=24.9\ \mathrm{dB}$$

이다. 변위는 $20.7\,\mathrm{dB}$ 작지만 사람에게는 $6.7\,\mathrm{dB}$만 약하다. 250 Hz에서 피부 임계값이 5배 낮고 그것이 $20\log_{10}5=14.0\,\mathrm{dB}$의 값을 하기 때문이며, $20.7-14.0=6.7$이다. 액추에이터의 감쇠와 피부의 예민도가 반대 방향을 가리키며 상당 부분 상쇄된다. 응답 곡선만 보면 못 쓸 것 같은 주파수에서 장치가 실제로는 쓸 만한 진짜 이유이고, 과제의 재튜닝이 기대만큼 벌어 주지 못하는 이유이기도 하다.

**Step 8 — 전자회로가 옮길 수 없는 공간 한계.** $C=100\,\mathrm{mm}$ 슬리브에 $d_2=10\,\mathrm{mm}$이면 구별되는 위치의 수는

$$N_{\max}=\left\lfloor\frac{C}{d_2}\right\rfloor=\left\lfloor\frac{100}{10}\right\rfloor=10$$

이다. 그러므로 tactor 16개 슬리브의 피치는 $C/16=6.25\,\mathrm{mm}$로 limen보다 좁고, 액추에이터 여섯 개는 새 위치를 하나도 사 주지 않는다. 정보로 말하면 설계는 단일 위치 패턴당 $\log_2 16=4.00$비트를 주장하지만 실제로는 최대 $\log_2 10=3.32$비트를 지지한다. 게다가 그 피치에서 지름 $6\,\mathrm{mm}$ 접촉자들 사이에는 $0.25\,\mathrm{mm}$밖에 남지 않으므로 슬리브와 피부를 통해 서로 결합하고, 어휘는 10에 머무는 것이 아니라 그보다 더 나빠진다.

**Step 9 — 두 한계는 같은 종류가 아니다.** Step 6의 부족은 *변환기* 한계다. 전류를 늘리거나, 서스펜션을 바꾸거나, 액추에이터 계열을 바꾸면 움직인다. Step 8의 것은 *수신자* 한계이고, 당신이 고른 부위가 정한다. 액추에이터 품질로는 조금도 움직이지 않는다. 공간 해상도 지적에 더 좋은 증폭기로 답하는 설계 리뷰는 둘을 혼동한 것이다.

### 스스로 점검

1. Step 6은 T1의 같은 250 Hz cue를 정직하게 두 가지로 요약한다. 열한 배 약하다, 그리고 두 배도 안 되게 약하다. 각각 전달량 중 무엇을 보고하는가? 둘 중 지각에 대한 주장은 있는가?
2. Step 7에서 250 Hz cue의 변위는 $20.7\,\mathrm{dB}$ 작은데 *사람에게는* $6.7\,\mathrm{dB}$만 약하다. 나머지 $14.0\,\mathrm{dB}$은 어디로 갔는가? 그것은 tactor의 응답 곡선을 사용 가능 한계로 읽는 일에 대해 무엇을 말하는가?
3. 리뷰어가 슬리브의 tactor 16개가 구별 가능한 자리를 10개밖에 못 준다고 지적하자, 팀이 더 센 전류의 증폭기를 제안한다. 전류를 아무리 키워도 그 제안이 통하지 않는 이유는?
4. 250 Hz라는 명령만으로 촉각 자극을 규정할 수 없는 이유는?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 첫째는 **변위**를 보고한다. $38.0$ 대 $3.52\,\mu\mathrm{m}$, 비는 $10.8$이다. 둘째는 **가속도**를 보고한다. $15.0$ 대 $8.69\,\mathrm{m/s^2}$, 비는 $1.73$이다. 둘의 차이는 가속도가 달고 변위가 달지 않는 $\omega^2$, 즉 $(250/100)^2=6.25$이고 실제로 $10.8/6.25=1.73$이다. 어느 쪽도 지각에 대한 주장이 아니다. 둘 다 T1만의 성질이고 아직 피부는 등장하지 않았다. 그러므로 전달량의 이름을 대는 일은 표기 취향이 아니라 측정의 일부다.
> 2. T2로 갔다. 피부의 검출 임계값은 $250\,\mathrm{Hz}$에서 $100\,\mathrm{Hz}$의 5분의 1이고 그 값은 $20\log_{10}5=14.0\,\mathrm{dB}$이며 $20.7-14.0=6.7$이다. 액추에이터의 롤오프와 수용자의 감도가 반대 방향을 가리켜 대부분 상쇄된다. 그래서 응답 곡선만으로는 장치가 어디서 못 쓰게 되는지 말할 수 없고, 각 주파수에서 그 사람의 임계값에 대어 잰 sensation level만 그것을 말할 수 있다. 과제의 재조정이 그토록 적게 버는 이유도 같다. 250 Hz에서 $4.7\,\mathrm{dB}$을 얻고 100 Hz에서 $20.7\,\mathrm{dB}$을 잃는다.
> 3. 묶여 있는 한계가 변환기가 아니라 수용자 쪽에 있기 때문이다. $N_{\max}=\lfloor C/d_2\rfloor=\lfloor100/10\rfloor=10$에는 액추에이터 양이 하나도 들어 있지 않다. 슬리브 둘레를 고른 피부 부위의 two-point limen으로 나눈 값일 뿐이다. 전류를 키우면 sensation level이 올라가고 그것은 Step 6의 천장에 관한 일이며, Step 8은 꿈쩍도 하지 않는다. 설계는 $\log_2 16=4.00$비트를 주장하고 $\log_2 10=3.32$비트를 떠받친다. 그 간격은 피부 위 경로를 더 길게 잡거나, 더 예민한 부위로 옮기거나, 단일 자리 위치에 기대지 않는 어휘를 쓸 때만 닫힌다.
> 4. 액추에이터와 장착이 전달되는 가속도·변위를 정하고, 예압·접촉 면적·신체 부위·파형 포락선·개인 감수성이 지각을 정한다. 주파수는 좌표 하나일 뿐이고, T1에서는 같은 명령이 두 주파수에서 한 자릿수만큼 다른 자극을 전달한다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P3**, 위의 T1–T3, 그리고 이 페이지를 쓴다. 손 계산만 한다. 시뮬레이터는 없다.

손잡이 둘만 움직이고 나머지는 그대로다. 서스펜션을 $k_t'=9860\,\mathrm{N/m}$로 뻣뻣하게 만들되 가동 질량, 감쇠비, 힘 상수, 전류 한계는 같다. 그리고 둘레 $C=100\,\mathrm{mm}$ 그대로인 슬리브를 손에서 팔뚝 밴드로 옮긴다. 거기 예시 two-point limen은 $d_2'=35\,\mathrm{mm}$다.

1. **그려라.** 뻣뻣해진 tactor로 §6의 패널 A를 원래와 같은 축 위에 다시 그려라. 옛 곡선을 옅게 남겨 두 곡선이 어디서 교차하는지 보이게 하라. 패널 B는 같은 tactor 16개로 팔뚝 밴드에 맞춰 다시 그려라.
2. **유도하라.** (a) 새 $c_t'$와 $f_0'$. (b) $Z'(100)$과 $Z'(250)$. Step 4·5처럼 스프링–관성 항과 감쇠 항을 따로 보여라. (c) 감각 수준 둘. (d) 재튜닝이 250 Hz에서 몇 dB를 벌고 100 Hz에서 몇 dB를 잃었는가. (e) 팔뚝에서의 $N_{\max}'$와 쓸 수 있는 비트.
3. **해석하라.** (a) 재튜닝은 $f_0$를 피부가 가장 예민한 주파수로 옮겼다. (c)와 (d)를 써서, 좋은 거래였는가? 답이 뒤집히려면 의도한 신호에 대해 무엇이 참이어야 하는가? (b) 어떤 팀이 cue를 "ERM의 250 Hz"로 규정한다. 아직 자유인 물리 변수는 무엇이고, 진폭을 주파수와 독립으로 써야 한다면 ERM이 틀린 계열인 이유는? (c) 같은 슬리브를 탁자에서 검증한 뒤 실제 과제 중 움직이는 팔뚝에 착용한다. §5 체크리스트의 어느 두 항목을 건너뛰었고, §7 Step 8의 계산을 적용하기도 전에 어휘에 무슨 일이 일어나는가?

> [!tip]- 정답 · Solutions
> 1. 패널 A: 봉우리가 250 Hz로 옮겨 가면서 낮아진다. 뻣뻣한 서스펜션은 $f_0$를 옮기는 동시에 공진 진폭 $F_0/(2\zeta k_t)$를 줄이기 때문이다. 두 곡선은 작동점 사이에서 교차한다. 패널 B: $6.25\,\mathrm{mm}$ 피치의 같은 16개 표시. 다만 아래 자의 눈금이 $35\,\mathrm{mm}$가 되어 슬리브 전체에 괄호가 둘밖에 들어가지 않는다.
> 2. (a) $c_t'=0.5\sqrt{9860(0.0040)}=0.5\sqrt{39.44}=3.1401\,\mathrm{N\cdot s/m}$, $f_0'=\frac{1}{2\pi}\sqrt{9860/0.0040}=\frac{1}{2\pi}\sqrt{2465000}=249.9\,\mathrm{Hz}$. (b) 100 Hz에서 $k_t'-m_t\omega^2=9860-1579.14=8280.86$, $c_t'\omega=1972.96$, 분모 $8512.65$이므로 $Z'(100)=0.030/8512.65=3.52\times10^{-6}\,\mathrm{m}=3.52\,\mu\mathrm{m}$. 250 Hz에서 $k_t'-m_t\omega^2=9860-9869.60=-9.60$, $c_t'\omega=4932.40$, 분모 $4932.41$이므로 $Z'(250)=0.030/4932.41=6.08\times10^{-6}\,\mathrm{m}=6.08\,\mu\mathrm{m}$. 지름길 $0.030/(2(0.25)(9860))=6.09\times10^{-6}$이 확인해 준다. (c) $\mathrm{SL}'(100)=20\log_{10}(3.52/1.0)=10.9\,\mathrm{dB}$, $\mathrm{SL}'(250)=20\log_{10}(6.08/0.20)=29.7\,\mathrm{dB}$. (d) 250 Hz에서 $29.7-24.9=4.7\,\mathrm{dB}$ 벌고, 100 Hz에서 $31.6-10.9=20.7\,\mathrm{dB}$ 잃었다. (e) $N_{\max}'=\lfloor100/35\rfloor=2$ 위치이므로 $\log_2 2=1.00$비트. tactor 16개가 나르기로 했던 4.00비트에 견줘 그렇다.
> 3. (a) 두 주파수를 모두 쓰는 신호라면 나쁜 거래다. 250 Hz에서 산 $4.7\,\mathrm{dB}$의 값으로 100 Hz에서 $20.7\,\mathrm{dB}$를 치렀고, 벌이가 그토록 적은 이유가 Step 7이다. 피부가 이미 옛 감쇠의 대부분을 되갚아 주고 있었다. 뒤집히는 경우는 두 가지다. 디스플레이가 정말로 250 Hz 부근 단일 주파수여서 잃은 대역이 아무 값도 하지 않거나, 100 Hz의 $10.9\,\mathrm{dB}$가 workload 아래에서도 과제가 요구하는 여유를 여전히 넘거나. (b) 진폭, 포락선, 지속 시간, 예압, 접촉 면적, 부위가 모두 자유롭다. ERM은 주파수와 힘을 $F\propto\omega^2$로 묶으므로 진폭을 독립으로 정할 수 없다. LRA, voice coil, 피에조가 필요하다. (c) 체크리스트 항목 2와 5다. 과제 중 믿을 만한 접촉을 유지하는 부위, 그리고 workload 아래에서도 패턴이 구별되는가. 팔이 움직이면 예압이 사라졌다 돌아오고 masking이 늘어 탁자 위 어휘가 무너진다. Step 8의 계산은 팔뚝에서 위치 2개라는 *상한*을 줄 뿐이고, 접촉 신뢰성을 잃은 착용 시스템은 그 상한에 닿지도 못한다.
