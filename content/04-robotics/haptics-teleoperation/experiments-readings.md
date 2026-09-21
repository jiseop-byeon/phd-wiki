---
title: 24.6 Experiments & Reading Map
tags: [haptics, research-practice, reading-guide]
study-depth: Working
wiki-support: Working
depth-goal: "Design a haptics study whose manipulation, measurements, statistical unit, safety controls, and claims line up, and turn a raw staircase record into a threshold whose criterion you can state."
mastery-when: "Master psychometric/statistical models and protocol validation when human evidence carries the thesis claim."
---

> [!note] Prerequisites · 선수 지식
> Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]] as the stimulus generator. The psychometric function, the JND and the Weber fraction from [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §2]], whose constant-stimuli table this page's staircase is the alternative to.
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P3**를 자극 발생기로 쓴다. 심리측정 함수, JND, Weber 분수는 [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §2]]. 이 페이지의 staircase는 그 페이지 constant-stimuli 표의 대안이다.

## English

*The research-practice end of the haptics track: a reading map and a protocol checklist. It keeps plant **P3** only as the stimulus generator [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]] made it.*

### Running object · 이 페이지의 대상

This page is a reading map, so its object is not a machine but a **record**: one frozen staircase run, defined here and unchanged afterwards. **The trial-by-trial responses below are illustrative values this page defines so the arithmetic is exact. They are nobody's measured data.**

**The run.** Plant **P3**, the 1-DoF handle of [[02-foundations/lab-plants|0.6 Lab Plants]], holds a pedestal force of $F_0=5.00\,\mathrm{N}$ and adds an increment $\Delta F$ in one of two intervals. The participant answers *which interval was stronger?* — the same 2AFC task as [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]], but now the experimenter moves $\Delta F$ between trials instead of sampling a fixed grid of levels.

**The rule: two-down, one-up, fixed step $0.05\,\mathrm{N}$, starting at $\Delta F=0.60\,\mathrm{N}$.** Two consecutive correct answers lower the level by one step; a single wrong answer raises it by one step. A **reversal** is a trial at which the direction of travel changes, and the level recorded at a reversal is the level of that trial.

**Frozen record: 24 trials.** `C` = correct, `W` = wrong.

| # | $\Delta F$ (N) | resp | # | $\Delta F$ (N) | resp |
|---:|---:|:---|---:|---:|:---|
| 1 | 0.60 | C | 13 | 0.50 | W |
| 2 | 0.60 | C | 14 | 0.55 | C |
| 3 | 0.55 | C | 15 | 0.55 | C |
| 4 | 0.55 | W | 16 | 0.50 | W |
| 5 | 0.60 | C | 17 | 0.55 | C |
| 6 | 0.60 | C | 18 | 0.55 | C |
| 7 | 0.55 | C | 19 | 0.50 | C |
| 8 | 0.55 | C | 20 | 0.50 | W |
| 9 | 0.50 | C | 21 | 0.55 | C |
| 10 | 0.50 | C | 22 | 0.55 | C |
| 11 | 0.45 | W | 23 | 0.50 | C |
| 12 | 0.50 | C | 24 | 0.50 | C |

§6 says what to draw from it and §7 converts it into a threshold, a JND, and a named criterion — which is the whole point of §2's insistence on an estimand, done once on a real record.

### 1. From an idea to a claim

Write the causal chain before building the interface:

$$\text{actuator command}\rightarrow\text{delivered mechanical stimulus}\rightarrow\text{perception/action}\rightarrow\text{task outcome}.$$

Each arrow needs a measurement. A motor command is not a measured skin stimulus; a questionnaire is not controller performance; faster completion does not identify which cue caused the improvement. A strong study combines physical calibration, behavioral outcomes, and subjective reports.

### 2. Minimal protocol

1. **Question and estimand:** “Does shear cue A reduce peak contact force relative to vibration B for novice operators?” is testable; “Is haptics better?” is not. The estimand is the precise quantity the study is designed to estimate, here the mean reduction in peak contact force.
2. **Participants and exclusions:** population, handedness if relevant, sensorimotor conditions, prior experience, stopping criteria.
3. **Conditions:** feedback mode, delay, gain, task difficulty, and any secondary workload.
4. **Design:** within-subject designs reduce between-person variance; counterbalance order and include enough practice to separate learning from treatment.
5. **Primary outcome:** choose before seeing results—peak force, path error, success, time, detection threshold, or calibrated confidence.
6. **Instrumentation:** synchronize haptic state, command, measured force, events, video, and survey identifiers; document clocks and missing packets.
7. **Analysis unit:** trials nested within participants are not independent participants. Report participant count, repetitions, exclusions, uncertainty, and effect size.
8. **Ethics and safety:** informed consent, voluntary withdrawal, privacy/de-identification, fatigue breaks, hardware stops, and incident handling belong in the design, not an appendix added later.

**Three terms this page leans on, defined.** §7 uses all three on the running object.

- **Estimand** — the *quantity a study is designed to estimate*, written down before the data exist, and made of three parts: the population it refers to, the measurement it is built from, and the contrast or criterion that pins it to one number. *Example*: "the mean reduction in peak contact force, in newtons, for novice operators, cue A against cue B". *Non-example*: "whether haptics helps", which names no quantity — and, more subtly, "the JND", which names a measurement but leaves out the criterion, so §7 Step 5 can produce two different numbers for that one word. It matters because design, sample size and analysis are all choices *about* the estimand, so a study without one cannot be underpowered or overpowered, only unfalsifiable.
- **Adaptive staircase** — a *procedure*, not a statistic: the level presented on the next trial is chosen from the responses already given, by a rule fixed in advance. Its defining parts are the start level, the step size, the up/down rule, and the stopping condition; change any one and you have a different procedure. *Example*: the 2-down/1-up run of the running object. *Non-example*: the method of constant stimuli in [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]], where the levels are fixed before the session and the participant's answers never move them. It matters because the rule, not the experimenter's judgement, decides *which point of the psychometric curve* the run settles on — the one-line derivation in §7 Step 3.
- **Reversal** — a *trial*: the one at which the direction of travel changes, from descending to ascending or back. *Non-example*: a wrong answer during a run that was already ascending, which continues the direction and is not a reversal, and a correct answer that is only the first of a needed pair. It matters because the threshold is averaged over reversals rather than over trials, so it is the reversal count that says whether a run was long enough — which is exactly what the problem set's twelve-trial record fails.

NASA-TLX measures six self-reported workload dimensions—mental, physical, temporal demand, perceived performance, effort, and frustration. It complements objective data; it does not reveal the physical cause of workload. Use the official scoring procedure appropriate to raw or weighted TLX and report which variant was used.

### 3. Evidence ladder

| Evidence | Supports | Does not yet support |
|---|---|---|
| actuator bench response | delivered device dynamics | human detectability or usefulness |
| psychophysical threshold | cue detectability under tested conditions | better task control |
| controlled task improvement | causal effect in that protocol | field deployment generality |
| representative workload study | performance under a closer context | long-term adoption or safety |
| field/longitudinal study | operational behavior over time | mechanism without additional controls |

### 4. Annotated reading sequence

1. **Hannaford & Okamura, “Haptics,” Springer Handbook of Robotics, 2nd ed., 2016.** The compact field map: human sensing → device design → rendering → stability → tactile displays. [Official chapter page](https://handbookofrobotics.org/view-chapter/42), [DOI](https://doi.org/10.1007/978-3-319-32552-1_42).
2. **Hayward & MacLean, “Do It Yourself Haptics: Part I,” IEEE RAM 14(4), 2007.** The best hardware-to-software bridge: transducers, impedance/admittance, DC motors, mechanisms, quantization, real-time loops, and practical limitations. [DOI](https://doi.org/10.1109/M-RA.2007.907921).
3. **MacLean, “Haptic Interaction Design for Everyday Interfaces,” RHFE 4(1), 2008.** Read for active touch, multisensory attention, haptic icons, shared control, and why technical realism is not the same as usefulness. [DOI](https://doi.org/10.1518/155723408X342826).
4. **Weir & Colgate, “Stability of Haptic Displays.”** Read the virtual-wall energy derivation, Z-width, quantization, virtual coupling, and PO/PC sections; treat later circuit implementations as specialized depth.
5. **Gillespie & Cutkosky, “Stable User-Specific Haptic Rendering of the Virtual Wall,” ASME IMECE, 1996.** A sampled, switched wall is not merely an LTI spring. The half-sample predictor and threshold-crossing correction depend on a limited high-frequency human/device model; the early experiment was qualitative. [DOI](https://doi.org/10.1115/IMECE1996-0362).
6. **Hannaford & Ryu, “Time-Domain Passivity Control of Haptic Interfaces,” IEEE TRA 18(1), 2002.** Follow the power sign, energy observer, and adaptive dissipative element. The method avoids an exact environment model but still faces noise, zero velocity, saturation, and performance tradeoffs. [DOI](https://doi.org/10.1109/70.988969).
7. **Raju, Verghese & Sheridan, “Design Issues in 2-Port Network Models of Bilateral Remote Manipulation,” ICRA 1989.** A classic bridge from desired port impedances and human/task models to stable gain selection. Its guarantee is over the specified passive termination class and model assumptions. [DOI](https://doi.org/10.1109/ROBOT.1989.100162).
8. **Colonnese & Okamura, “Stability and quantization-error analysis of haptic rendering of virtual stiffness and damping,” IJRR 35(9):1103–1120, 2016** (online 2015). The one paper that puts sampling, position quantization, time delay, and the velocity-estimate low-pass filter into a single one-DOF model and derives the tradeoffs between them, including sufficient conditions for quantization-error passivity and necessary conditions for the absence of (malicious- and uncoupled-touch) limit cycles. Verified on a Phantom Premium 1.5; the abstract states no numerical result. Cite the volume, not the year alone — it appeared online in 2015 and in print in 2016. [DOI](https://doi.org/10.1177/0278364915596234).
9. **Salisbury, Conti & Barbagli, "Haptic rendering: introductory concepts," IEEE CG&A 24(2), 2004.** The survey that frames rendering as a loop of collision, force computation and actuation; read it before any rendering paper. [DOI](https://doi.org/10.1109/MCG.2004.1274058).
10. **Ruspini, Kolarov & Khatib, "The haptic display of complex graphical environments," SIGGRAPH 1997; Zilles & Salisbury, "A constraint-based god-object method for haptic display," IROS 1995.** The two proxy papers. Ruspini names the three failures of penalty rendering; Zilles and Salisbury introduced the constrained point two years earlier. [DOI](https://doi.org/10.1145/258734.258878) · [DOI](https://doi.org/10.1109/IROS.1995.525876).
11. **Kuchenbecker, Fiene & Niemeyer, "Improving contact realism through event-based haptic feedback," IEEE TVCG 12(2), 2006.** Read with its WHC 2005 conference version, which carries the nine-subject realism study; note that realism was rated, not measured by task. [DOI](https://doi.org/10.1109/TVCG.2006.32) · [DOI](https://doi.org/10.1109/WHC.2005.52).
12. **Richard & Cutkosky, "Friction modeling and display in haptic applications involving user performance," ICRA 2002.** The Karnopp implementation plus a twenty-subject Fitts study showing moderate friction helps and high stiction hurts. [DOI](https://doi.org/10.1109/ROBOT.2002.1013425).

The algorithms in items 9–12 — penalty and proxy rendering, event-based transients and friction display — are worked through in [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 Haptic Rendering Algorithms]].

### 5. How the supplied course materials were selected

| Local material class | Public learning use |
|---|---|
| syllabus and lecture decks | track scope, prerequisite map, concepts, and version caveats |
| MATLAB templates and Jacobian script | original derivations and implementation checklist; no submitted solution copied |
| Hapkit slides and mechanical files | transmission and sensing reasoning in 24.3–24.4; build instructions and original files are not published |
| assignments and student drafts | identify required competencies and common mistakes; no answer key or personal work published |
| project options/rubric | transferable project-design and evaluation criteria; private contacts and unverified claims excluded |
| consent, recruitment, pre/post surveys | ethics, eligibility, workload, privacy, and measurement design; no form copied or treated as a reusable approval |
| licensed readings | annotated concepts and official DOI/publisher links; PDFs remain private |

The packet covers the first half of a full haptics course particularly well. It does not contain all later lecture/lab materials named in the syllabus—such as the complete CHAI3D, advanced teleoperation, and ROS sequence—so this guide does not reconstruct those lectures or claim to cover them.

**Worked: the three readings the homework asks.** “Haptics is better” with TLX and time down has no named estimand and skipped the skin stimulus. $n=600$ is nested trials; the unit is 20 people. Bench response is not detectability; task improvement is not field generality.

### 6. Homework diagram

One plot, and the problem set asks for the same plot from a shorter record under a different rule.

<svg viewBox="0 0 560 350" style="max-width:100%;height:auto" role="img" aria-label="A 24-trial two-down one-up staircase on 0.05 N rows with filled markers for correct and open ones for wrong, eight numbered reversals of which the first two are struck out, a dashed line at 0.5167 N labelled 70.7% correct, and the causal chain with only the stimulus-to-perception arrow ticked.">
  <circle cx="58" cy="17" r="3.8" fill="currentColor"/>
  <text x="67" y="21" font-size="11" fill="currentColor">correct</text>
  <circle cx="127.5" cy="17" r="3.8" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="136.5" y="21" font-size="11" fill="currentColor">wrong</text>
  <circle cx="196.7" cy="17" r="7.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="208.7" y="21" font-size="11" fill="currentColor">reversal</text>
  <circle cx="279.1" cy="17" r="7.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <line x1="270.1" y1="26" x2="288.1" y2="8" stroke="currentColor" stroke-width="1.5"/>
  <text x="292.1" y="21" font-size="11" fill="currentColor">discarded (§7 Step 2)</text>
  <g stroke="currentColor" stroke-width="0.8" stroke-opacity="0.28"><line x1="53" y1="200" x2="403" y2="200"/><line x1="53" y1="170" x2="403" y2="170"/><line x1="53" y1="140" x2="403" y2="140"/><line x1="53" y1="110" x2="403" y2="110"/><line x1="53" y1="80" x2="403" y2="80"/><line x1="53" y1="50" x2="403" y2="50"/></g>
  <g font-size="11" fill="currentColor" text-anchor="end" opacity="0.8"><text x="49" y="204">0.40</text><text x="49" y="174">0.45</text><text x="49" y="144">0.50</text><text x="49" y="114">0.55</text><text x="49" y="84">0.60</text><text x="49" y="54">0.65</text></g>
  <text x="14" y="38" font-size="11.5" fill="currentColor" opacity="0.9">ΔF (N)</text>
  <line x1="53" y1="208" x2="403" y2="208" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55"/>
  <g stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55">
    <line x1="58" y1="208" x2="58" y2="213"/><line x1="72.8" y1="208" x2="72.8" y2="211"/><line x1="87.6" y1="208" x2="87.6" y2="211"/><line x1="102.3" y1="208" x2="102.3" y2="213"/><line x1="117.1" y1="208" x2="117.1" y2="211"/><line x1="131.9" y1="208" x2="131.9" y2="211"/><line x1="146.7" y1="208" x2="146.7" y2="211"/><line x1="161.5" y1="208" x2="161.5" y2="213"/><line x1="176.3" y1="208" x2="176.3" y2="211"/>
    <line x1="191" y1="208" x2="191" y2="211"/><line x1="205.8" y1="208" x2="205.8" y2="211"/><line x1="220.6" y1="208" x2="220.6" y2="213"/><line x1="235.4" y1="208" x2="235.4" y2="211"/><line x1="250.2" y1="208" x2="250.2" y2="211"/><line x1="265" y1="208" x2="265" y2="211"/><line x1="279.7" y1="208" x2="279.7" y2="213"/><line x1="294.5" y1="208" x2="294.5" y2="211"/><line x1="309.3" y1="208" x2="309.3" y2="211"/>
    <line x1="324.1" y1="208" x2="324.1" y2="211"/><line x1="338.9" y1="208" x2="338.9" y2="213"/><line x1="353.7" y1="208" x2="353.7" y2="211"/><line x1="368.4" y1="208" x2="368.4" y2="211"/><line x1="383.2" y1="208" x2="383.2" y2="211"/><line x1="398" y1="208" x2="398" y2="213"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8"><text x="58" y="225">1</text><text x="102.3" y="225">4</text><text x="161.5" y="225">8</text><text x="220.6" y="225">12</text><text x="279.7" y="225">16</text><text x="338.9" y="225">20</text><text x="398" y="225">24</text></g>
  <text x="228" y="240" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">trial number</text>
  <line x1="53" y1="130" x2="406" y2="130" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 3"/>
  <g font-size="12" fill="currentColor"><text x="411" y="134">70.7% correct,</text><text x="411" y="149">2-down/1-up,</text><text x="411" y="164">5.00 N pedestal</text></g>
  <g font-size="11" fill="currentColor" opacity="0.75"><text x="411" y="183">0.5167 N = mean of</text><text x="411" y="197">reversals 3–8</text></g>
  <g stroke="currentColor" stroke-width="1.3" stroke-opacity="0.75">
    <line x1="62.4" y1="80" x2="68.4" y2="80"/><line x1="74.7" y1="83.9" x2="85.6" y2="106.1"/><line x1="92" y1="110" x2="97.9" y2="110"/><line x1="104.3" y1="106.1" x2="115.2" y2="83.9"/><line x1="121.5" y1="80" x2="127.5" y2="80"/><line x1="133.9" y1="83.9" x2="144.8" y2="106.1"/><line x1="151.1" y1="110" x2="157.1" y2="110"/><line x1="163.4" y1="113.9" x2="174.3" y2="136.1"/>
    <line x1="180.7" y1="140" x2="186.6" y2="140"/><line x1="193" y1="143.9" x2="203.9" y2="166.1"/><line x1="207.8" y1="166.1" x2="218.7" y2="143.9"/><line x1="225" y1="140" x2="231" y2="140"/><line x1="237.3" y1="136.1" x2="248.2" y2="113.9"/><line x1="254.6" y1="110" x2="260.6" y2="110"/><line x1="266.9" y1="113.9" x2="277.8" y2="136.1"/><line x1="281.7" y1="136.1" x2="292.6" y2="113.9"/>
    <line x1="298.9" y1="110" x2="304.9" y2="110"/><line x1="311.2" y1="113.9" x2="322.1" y2="136.1"/><line x1="328.5" y1="140" x2="334.5" y2="140"/><line x1="340.8" y1="136.1" x2="351.7" y2="113.9"/><line x1="358.1" y1="110" x2="364" y2="110"/><line x1="370.4" y1="113.9" x2="381.3" y2="136.1"/><line x1="387.6" y1="140" x2="393.6" y2="140"/>
  </g>
  <g fill="currentColor">
    <circle cx="58" cy="80" r="3.8"/><circle cx="72.8" cy="80" r="3.8"/><circle cx="87.6" cy="110" r="3.8"/><circle cx="117.1" cy="80" r="3.8"/><circle cx="131.9" cy="80" r="3.8"/><circle cx="146.7" cy="110" r="3.8"/><circle cx="161.5" cy="110" r="3.8"/><circle cx="176.3" cy="140" r="3.8"/><circle cx="191" cy="140" r="3.8"/><circle cx="220.6" cy="140" r="3.8"/><circle cx="250.2" cy="110" r="3.8"/>
    <circle cx="265" cy="110" r="3.8"/><circle cx="294.5" cy="110" r="3.8"/><circle cx="309.3" cy="110" r="3.8"/><circle cx="324.1" cy="140" r="3.8"/><circle cx="353.7" cy="110" r="3.8"/><circle cx="368.4" cy="110" r="3.8"/><circle cx="383.2" cy="140" r="3.8"/><circle cx="398" cy="140" r="3.8"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="102.3" cy="110" r="3.8"/><circle cx="205.8" cy="170" r="3.8"/><circle cx="235.4" cy="140" r="3.8"/><circle cx="279.7" cy="140" r="3.8"/><circle cx="338.9" cy="140" r="3.8"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="102.3" cy="110" r="7.5"/><circle cx="131.9" cy="80" r="7.5"/><circle cx="205.8" cy="170" r="7.5"/><circle cx="265" cy="110" r="7.5"/><circle cx="279.7" cy="140" r="7.5"/><circle cx="309.3" cy="110" r="7.5"/><circle cx="338.9" cy="140" r="7.5"/><circle cx="368.4" cy="110" r="7.5"/></g>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="91.3" y="102">1</text><text x="131.9" y="68">2</text><text x="205.8" y="192">3</text><text x="265" y="98">4</text><text x="279.7" y="162">5</text><text x="309.3" y="98">6</text><text x="338.9" y="162">7</text><text x="368.4" y="98">8</text></g>
  <g stroke="currentColor" stroke-width="1.6"><line x1="93.5" y1="118.8" x2="111.1" y2="101.2"/><line x1="123.1" y1="88.8" x2="140.7" y2="71.2"/></g>
  <text x="8" y="260" font-size="11" fill="currentColor" opacity="0.9">§1’s causal chain: the tick marks the one arrow this plot measures</text>
  <rect x="8" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor" text-anchor="middle"><text x="67" y="292.2">actuator</text><text x="67" y="305.8">command</text></g>
  <line x1="129" y1="295" x2="140.5" y2="295" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="147,295 140,298.4 140,291.6" fill="currentColor"/>
  <rect x="132" y="328" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <rect x="150" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor" text-anchor="middle"><text x="209" y="285.5">delivered</text><text x="209" y="299">mechanical</text><text x="209" y="312.5">stimulus</text></g>
  <line x1="271" y1="295" x2="282.5" y2="295" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="289,295 282,298.4 282,291.6" fill="currentColor"/>
  <rect x="274" y="328" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <polyline points="276.2,334 279,337.5 284.5,329.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
  <rect x="292" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor" text-anchor="middle"><text x="351" y="292.2">perception /</text><text x="351" y="305.8">action</text></g>
  <line x1="413" y1="295" x2="424.5" y2="295" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="431,295 424,298.4 424,291.6" fill="currentColor"/>
  <rect x="416" y="328" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <rect x="434" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor" text-anchor="middle"><text x="493" y="292.2">task</text><text x="493" y="305.8">outcome</text></g>
</svg>

Trial number 1 to 24 across; $\Delta F$ up, from $0.40$ to $0.65\,\mathrm{N}$ ruled in $0.05\,\mathrm{N}$ rows, because the step size is fixed and the level can therefore only ever sit on a row. Plot the 24 levels and join consecutive trials into one continuous track. Use a filled marker for a correct trial and an open marker for a wrong one, so the rule is readable off the figure: the track only descends after two filled markers in a row, and it rises immediately after any open one. Circle every trial at which the direction of travel changes and number the circles $1$ to $8$. Strike through the first two circles — §7 Step 2 discards them — and draw a horizontal line at the mean of the remaining six, labelled with the criterion it estimates rather than with the word "threshold": *70.7% correct, 2-down/1-up, 5.00 N pedestal*. Beside the plot copy §1's causal chain and put a tick under the single arrow this figure measures, leaving the other two arrows blank.

### 7. Worked case: a staircase record becomes a threshold, and a JND

**Step 1 — find the reversals.** Walk the record and mark every trial where the direction changes. The rule descends only after two consecutive `C` and ascends on any `W`, which gives eight reversals:

| reversal | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| trial | 4 | 6 | 11 | 15 | 16 | 18 | 20 | 22 |
| $\Delta F$ (N) | 0.55 | 0.60 | 0.45 | 0.55 | 0.50 | 0.55 | 0.50 | 0.55 |

**Step 2 — average the settled part.** Discard the first two reversals, because the run starts at a deliberately easy level and its early travel records the start point rather than the participant, and average the rest:

$$\widehat{\Delta F}=\frac{0.45+0.55+0.50+0.55+0.50+0.55}{6}=\frac{3.10}{6}=0.5167\ \mathrm{N},$$

an even number of reversals being used so that the peaks and troughs of the track contribute equally.

**Step 3 — which probability did that estimate?** This is the step papers skip, and it is one line of algebra. Assume trials are independent and the probability correct $p$ is locally constant near the settled level. Under 2-down/1-up the level steps *down* exactly when two consecutive trials are correct, with probability $p^2$, and *up* otherwise, with probability $1-p^2$. At a level the track neither leaves upward nor downward on average, those two are equal, so

$$p^2=1-p^2\quad\Longrightarrow\quad p^2=\tfrac12\quad\Longrightarrow\quad p=\sqrt{0.5}=0.7071,$$

and the estimate is therefore the $70.7\%$-correct point of this participant's curve — not the $75\%$ point, not "the threshold". (The frozen record scores $19/24=79.2\%$ correct overall, above $70.7\%$, which is ordinary sampling noise on 24 trials and not evidence that the rule failed.) [[06-research-practice/psychophysics-human-measurement|8. Psychophysics & Human Measurement §2]] runs the same argument for any 1-up-$n$-down rule, $p^\ast=2^{-1/n}$, and its §7 simulates staircases on a frozen observer to measure what a finite step and a start not yet forgotten add to the estimate.

**Step 4 — name the quantity.** $\widehat{\Delta F}=0.5167\,\mathrm{N}$ is a *difference* threshold: the increment on a $5.00\,\mathrm{N}$ pedestal at which this participant is $70.7\%$ correct. That is a JND, but only once the criterion is attached to it. Its Weber fraction is

$$k=\frac{\widehat{\Delta F}}{F_0}=\frac{0.5167}{5.00}=0.1033,$$

i.e. $10.3\%$, since the pedestal is the operating point the increment was measured on.

**Step 5 — compare it with the other method, and see the estimand problem appear.** [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]] measured the same participant on the same handle at the same $5\,\mathrm{N}$ operating point by constant stimuli and got $\mathrm{JND}=0.4107\,\mathrm{N}$, $k=8.1\%$. This staircase gives $0.5167\,\mathrm{N}$, $26\%$ larger. Neither is wrong and neither is noise: one is half the $25$–$75$ span of a *judged-stronger* curve about its PSE, the other is the increment for $70.7\%$ *correct* in a difference-detection task. They are different points on different functions. A paper that reports "the JND" without its criterion and its task has produced a number no other lab can reproduce or compare, which is §2's estimand requirement restated as arithmetic.

**Step 6 — check it against the device.** Using the P3 wall quantum of [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]], $\Delta F_{\text{count}}=0.0245\,\mathrm{N}$: the threshold is $0.5167/0.0245=21.1$ counts, or $0.5167/400=1.29\,\mathrm{mm}$ of penetration. The staircase's own step of $0.05\,\mathrm{N}$ is $0.05/0.0245=2.0$ counts, so the resolution of this experiment was set by the experimenter's step size and not by the hardware — but a step of $0.02\,\mathrm{N}$ would be $0.8$ of a count, below what the device can distinguish, and the track would stall on quantization while the write-up reported a converged threshold.

**Step 7 — what one record supports.** This is one participant and 24 trials, so it supports a single-participant estimate with wide uncertainty and nothing about a population. Run 20 participants and the unit for any treatment claim is still the participant: you analyse 20 threshold estimates, not 480 trials, which is §2 item 7 and the self-check below. On §3's ladder this number sits in the "psychophysical threshold" row — it supports cue detectability under the tested conditions, and not better task control.

### Self-check

1. Step 2 averages six reversals and Step 3 shows the rule targets $70.7\%$ correct. Why is the second step not optional bookkeeping — what exactly is unreported if a paper gives only $\widehat{\Delta F}=0.5167\,\mathrm{N}$?
2. The same participant, the same handle and the same $5\,\mathrm{N}$ operating point give $0.4107\,\mathrm{N}$ in 24.1 and $0.5167\,\mathrm{N}$ here, $26\%$ apart. Which of the two is wrong, and what is the question that decides it?
3. Step 6 says a $0.02\,\mathrm{N}$ staircase step would be a mistake on this hardware. Show the arithmetic, and say what the write-up would report instead of the mistake.
4. A within-subject study has 20 people and 30 trials per person. Is $n=600$?

> [!tip]- Answers
> 1. A stimulus level without its criterion is not a quantity: $0.5167\,\mathrm{N}$ is the increment at which *this* rule holds the participant, and the rule is what fixes which point on the curve that is. Change 2-down/1-up to 3-down/1-up and the same record, the same skin and the same handle deliver $p=0.5^{1/3}=0.7937$ instead — a different point, and a number no reader can convert without being told the rule. What is unreported is therefore the estimand itself, which is §2 item 1 restated as arithmetic.
> 2. Neither is wrong, and the gap is not noise. The question that decides it is *what was the participant asked to do*. Constant stimuli measured half the $25$–$75$ span of a **judged-stronger** curve about its PSE; the staircase measured the increment for $70.7\%$ **correct** in a difference-detection task. Two tasks, two criteria, two functions; the numbers are comparable only through a stated psychometric model, and a paper that reports "the JND" bare has produced a figure no other lab can reproduce.
> 3. One encoder count against the default wall is $\Delta F_{\text{count}}=0.0245\,\mathrm{N}$, so a $0.02\,\mathrm{N}$ step is $0.02/0.0245=0.82$ of a count — below the device's own quantum, where a commanded step down may not change the delivered force at all. Compare the $0.05\,\mathrm{N}$ step actually used, $0.05/0.0245=2.0$ counts, which the hardware can resolve. The track would then stall on quantization rather than on the participant, and the write-up would report a beautifully converged threshold that measures the encoder.
> 4. Not for a participant-level treatment claim. Trials are nested, repeated observations. Analyse that dependence, for example with participant-level summaries or a hierarchical/mixed model (a regression that gives each participant their own baseline, so repeated trials from one person are not counted as independent people); report both 20 participants and 600 trials.

### Problem set · 과제

Tier C — this page is the track's reading map, so its homework stays claim-reading; §7 is the derivation it still owes you, and items 1 and 2 below are that derivation on a changed rule. Using this page, [[02-foundations/lab-plants|0.6]], and [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]] for comparison.

Same handle, same $5.00\,\mathrm{N}$ pedestal, same $0.05\,\mathrm{N}$ step, but the rule is changed to **three-down, one-up** and the run starts at $\Delta F=0.50\,\mathrm{N}$. Twelve trials, again illustrative:

| # | $\Delta F$ (N) | resp | # | $\Delta F$ (N) | resp |
|---:|---:|:---|---:|---:|:---|
| 1 | 0.50 | C | 7 | 0.50 | C |
| 2 | 0.50 | C | 8 | 0.50 | C |
| 3 | 0.50 | C | 9 | 0.45 | C |
| 4 | 0.45 | C | 10 | 0.45 | C |
| 5 | 0.45 | W | 11 | 0.45 | C |
| 6 | 0.50 | C | 12 | 0.40 | W |

1. **Draw.** Draw §6's plot for this record, with the same $0.05\,\mathrm{N}$ rows. Mark the reversals and say why the strike-through part of §6's instruction cannot be carried out here.
2. **Derive.** (a) The reversal trials and their levels. (b) A threshold estimate, and the sentence you must attach to it about how it was averaged. (c) The criterion probability of a 3-down/1-up rule, and of a 1-up/1-down rule, by §7 Step 3's argument. (d) The Weber fraction, and the estimate in P3 encoder counts.
3. **Interpret.** (a) A paper runs a 1-up/1-down staircase in a 2AFC task, reports the result as "the detection threshold", and compares it with another lab's constant-stimuli JND. Name the two separate estimand errors, using (c) for the first. (b) A study reports "haptics is better" with NASA-TLX down and completion time down. Which estimand is missing, and which arrow of actuator $\to$ stimulus $\to$ perception $\to$ outcome was not measured? (c) Twenty people, thirty trials each, $n=600$ in the t-test. What is the analysis unit, and what must the report still say? (d) Place "actuator bench response" and "controlled task improvement" on the evidence ladder. What does each not yet support?

> [!tip]- Solutions
> 1. The track descends only after three filled markers in a row, so it spends longer on each level than §6's figure does. There are three reversals, and §6 discards the first two and averages six — here that would leave one. The discard rule cannot be applied, which is the finding, not an inconvenience.
> 2. (a) Trial 5 at $0.45$, trial 8 at $0.50$, trial 12 at $0.40$. (b) Averaging all three gives $(0.45+0.50+0.40)/3=0.45\,\mathrm{N}$, and the attached sentence must say that it is the mean of *all three* reversals of a 12-trial run, an odd number, with no burn-in discarded — so peaks and troughs do not contribute equally and the estimate carries the start point. Six or more reversals are the usual minimum; this run should be treated as a pilot. (c) A down step now needs three consecutive correct, with probability $p^3$, so stationarity gives $p^3=1-p^3$, $p^3=0.5$ and $p=0.5^{1/3}=0.7937$: the $79.4\%$-correct point. For 1-up/1-down the down step needs one correct, so $p=1-p$ and $p=0.5$ — which in a two-alternative task is chance, so the rule tracks a level at which the participant is guessing and estimates nothing. (d) $k=0.45/5.00=0.090$, i.e. $9.0\%$; and $0.45/0.0245=18.4$ counts, about $1.13\,\mathrm{mm}$ of penetration.
> 3. (a) First, the rule targets $p=0.5$, which is chance in 2AFC, so the "threshold" is not a threshold at all — no stimulus level is identified. Second, even a valid staircase number is a different estimand from a constant-stimuli JND (§7 Step 5): different task, different criterion, different point on the curve. The two must be compared through a stated psychometric model or not at all. (b) The estimand should be a named quantity (peak contact force, not "better"). TLX is self-reported workload, not the mechanical stimulus; time does not identify which cue caused the change. Calibrate the skin stimulus. (c) The participant is the unit for a treatment claim; trials are nested. Report $20$ people *and* $600$ trials, with a hierarchical/mixed model or participant-level summaries. (d) Bench response supports delivered dynamics, not detectability. Task improvement supports a causal effect in that protocol, not field generality.

## 한국어

*햅틱 트랙의 연구 실무 쪽 끝이다. 읽기 지도이자 프로토콜 체크리스트다. 장치 **P3**는 [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]]이 만들어 둔 자극 발생기로만 쓴다.*

### 이 페이지의 대상 · Running object

이 페이지는 읽기 지도이므로 대상이 기계가 아니라 **기록**이다. 얼어붙은 staircase 한 번의 기록을 여기서 정하고 뒤에서 바꾸지 않는다. **아래의 시행별 응답은 계산이 딱 떨어지도록 이 페이지에서 정의한 예시 값이다. 누군가가 측정한 데이터가 아니다.**

**실험.** [[02-foundations/lab-plants|0.6 Lab Plants]]의 1자유도 핸들 **P3**가 받침 힘 $F_0=5.00\,\mathrm{N}$을 유지하고, 두 구간 중 하나에 증분 $\Delta F$를 얹는다. 참가자는 *어느 구간이 더 셌는가*에 답한다. [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]]과 같은 2AFC 과제이되, 이제 실험자가 고정된 수준 격자를 표집하는 대신 시행 사이에 $\Delta F$를 움직인다.

**규칙: 2-down 1-up, 고정 단 $0.05\,\mathrm{N}$, 시작 $\Delta F=0.60\,\mathrm{N}$.** 연속 두 번 맞히면 한 단 내리고, 한 번 틀리면 한 단 올린다. **Reversal**은 진행 방향이 바뀌는 시행이고, reversal에 기록하는 수준은 그 시행의 수준이다.

**얼어붙은 기록: 24 시행.** `C`는 정답, `W`는 오답.

| # | $\Delta F$ (N) | 응답 | # | $\Delta F$ (N) | 응답 |
|---:|---:|:---|---:|---:|:---|
| 1 | 0.60 | C | 13 | 0.50 | W |
| 2 | 0.60 | C | 14 | 0.55 | C |
| 3 | 0.55 | C | 15 | 0.55 | C |
| 4 | 0.55 | W | 16 | 0.50 | W |
| 5 | 0.60 | C | 17 | 0.55 | C |
| 6 | 0.60 | C | 18 | 0.55 | C |
| 7 | 0.55 | C | 19 | 0.50 | C |
| 8 | 0.55 | C | 20 | 0.50 | W |
| 9 | 0.50 | C | 21 | 0.55 | C |
| 10 | 0.50 | C | 22 | 0.55 | C |
| 11 | 0.45 | W | 23 | 0.50 | C |
| 12 | 0.50 | C | 24 | 0.50 | C |

§6이 여기서 무엇을 그릴지 말하고, §7이 이것을 임계값과 JND와 이름 붙은 기준으로 바꾼다. estimand를 명시하라는 §2의 요구를 실제 기록 위에서 한 번 해 보는 것이 그 전부다.

### 1. 아이디어에서 주장까지

인터페이스를 만들기 전에 인과 사슬을 먼저 쓴다.

$$\text{액추에이터 명령}\rightarrow\text{실제 전달된 역학 자극}\rightarrow\text{지각·행동}\rightarrow\text{과제 결과}.$$

화살표마다 측정이 필요하다. 모터 명령은 측정된 피부 자극이 아니고, 설문은 제어기 성능이 아니며, 수행 시간이 줄었다는 것만으로 어떤 cue가 그 개선을 일으켰는지 알 수 없다. 강한 연구는 물리적 보정, 행동 결과, 주관 보고 셋을 함께 놓는다.

### 2. 최소 프로토콜

1. **질문과 estimand:** "전단 cue A가 초보 조작자에게서 진동 B 대비 최대 접촉력을 줄이는가"는 검정 가능하고, "햅틱이 더 나은가"는 아니다. Estimand는 연구가 추정하도록 설계된 정확한 양이고, 여기서는 최대 접촉력의 평균 감소량이다.
2. **참가자와 제외:** 모집단, 필요하면 손잡이, 감각운동 조건, 사전 경험, 중단 기준.
3. **조건:** 피드백 방식, 지연, 이득, 과제 난이도, 부가 workload.
4. **설계:** within-subject는 사람 간 분산을 줄인다. 순서를 counterbalance하고, 학습을 처치와 분리할 만큼 연습을 넣는다.
5. **주 결과 지표:** 결과를 보기 전에 고른다 — 최대 힘, 경로 오차, 성공, 시간, 검출 임계값, 또는 보정된 확신도.
6. **계측:** 햅틱 상태, 명령, 측정된 힘, 이벤트, 영상, 설문 식별자를 동기화한다. 시계와 유실 패킷을 문서화한다.
7. **분석 단위:** 참가자 안에 nested된 trial은 독립 참가자가 아니다. 참가자 수, 반복 수, 제외, 불확실성, 효과 크기를 보고한다.
8. **윤리와 안전:** 사전 동의, 자발적 철회, 개인정보 비식별, 피로 휴식, 하드웨어 정지, 사고 처리는 나중에 붙이는 부록이 아니라 설계에 속한다.

**이 페이지가 기대는 세 용어의 정의.** §7이 셋을 모두 running object 위에서 쓴다.

- **Estimand** — 데이터가 존재하기 전에 적어 두는, *연구가 추정하도록 설계된 양*이다. 세 부분으로 이루어진다. 어느 모집단을 가리키는가, 어떤 측정으로 만들어지는가, 어떤 대조나 기준이 그것을 숫자 하나로 못 박는가. *예*: "초보 조작자에서 cue A 대 cue B의 뉴턴 단위 첨두 접촉력 평균 감소량". *반례*: "햅틱이 도움이 되는가". 양을 하나도 이름 붙이지 않았다. 더 미묘한 반례는 "그 JND"다. 측정은 이름 붙였지만 기준을 빼서, §7 Step 5가 그 한 단어에 서로 다른 숫자 둘을 만들어 낼 수 있다. 중요한 이유는 설계도 표본 크기도 분석도 전부 estimand*에 관한* 선택이기 때문이다. estimand 없는 연구는 검정력이 모자라지도 넘치지도 못하고 그저 반증 불가능하다.
- **적응적 staircase** — 통계량이 아니라 *절차*다. 다음 시행에 제시할 수준을 이미 받은 응답에서, 미리 고정한 규칙으로 고른다. 정의 부분은 시작 수준, 단 크기, up/down 규칙, 중단 조건이고, 하나만 바꿔도 다른 절차가 된다. *예*: running object의 2-down 1-up run. *반례*: [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]]의 constant stimuli. 수준을 세션 전에 고정하고 참가자의 응답이 그것을 움직이지 않는다. 중요한 이유는 실험자의 판단이 아니라 규칙이 run이 가라앉을 *심리측정 곡선 위의 점*을 정하기 때문이다. §7 Step 3의 한 줄 유도가 그것이다.
- **Reversal** — *시행*이다. 진행 방향이 내림에서 오름으로, 또는 그 반대로 바뀌는 그 시행. *반례*: 이미 올라가고 있던 run에서 나온 오답. 방향을 이어 가므로 reversal이 아니다. 필요한 쌍의 첫 번째인 정답도 마찬가지다. 중요한 이유는 임계값을 시행이 아니라 reversal 위에서 평균하기 때문이다. run이 충분히 길었는지는 reversal 개수가 말하고, 과제의 12 시행짜리 기록이 실패하는 지점이 바로 그것이다.

NASA-TLX는 정신적·신체적·시간적 요구, 지각된 수행, 노력, 좌절의 여섯 자기보고 workload 차원을 잰다. 객관 데이터를 보완할 뿐 workload의 물리적 원인을 드러내지는 않는다. raw와 weighted 중 해당하는 공식 채점 절차를 쓰고 어느 쪽을 썼는지 보고한다.

### 3. 증거의 사다리

| 증거 | 지지하는 것 | 아직 지지하지 못하는 것 |
|---|---|---|
| 액추에이터 벤치 응답 | 전달된 장치 동역학 | 사람의 검출 가능성이나 유용성 |
| 심리물리 임계값 | 시험한 조건에서 cue의 검출 가능성 | 더 나은 과제 제어 |
| 통제된 과제 개선 | 그 프로토콜 안에서의 인과 효과 | 현장 배치로의 일반화 |
| 대표성 있는 workload 연구 | 더 가까운 맥락에서의 수행 | 장기 채택이나 안전 |
| 현장·종단 연구 | 시간에 걸친 운용 행동 | 추가 통제 없이는 기전 |

### 4. 주석 달린 읽기 순서

1. **Hannaford & Okamura, "Haptics," Springer Handbook of Robotics 2판, 2016.** 압축된 분야 지도다. 인간 감각 → 장치 설계 → 렌더링 → 안정성 → 촉각 디스플레이. [공식 장 페이지](https://handbookofrobotics.org/view-chapter/42), [DOI](https://doi.org/10.1007/978-3-319-32552-1_42).
2. **Hayward & MacLean, "Do It Yourself Haptics: Part I," IEEE RAM 14(4), 2007.** 하드웨어와 소프트웨어를 잇는 최고의 다리다. 변환기, 임피던스/어드미턴스, DC 모터, 기구, 양자화, 실시간 루프, 그리고 실제 한계. [DOI](https://doi.org/10.1109/M-RA.2007.907921).
3. **MacLean, "Haptic Interaction Design for Everyday Interfaces," RHFE 4(1), 2008.** 능동적 촉각, 다감각 주의, haptic icon, shared control, 그리고 기술적 사실성이 유용성과 같지 않은 이유를 읽어라. [DOI](https://doi.org/10.1518/155723408X342826).
4. **Weir & Colgate, "Stability of Haptic Displays."** 가상 벽의 에너지 유도, Z-width, 양자화, virtual coupling, PO/PC 절을 읽어라. 뒤의 회로 구현은 전문 심화로 다룬다.
5. **Gillespie & Cutkosky, "Stable User-Specific Haptic Rendering of the Virtual Wall," ASME IMECE, 1996.** 샘플링되고 스위칭되는 벽은 그냥 LTI 스프링이 아니다. 반 샘플 예측기와 임계 통과 보정은 제한된 고주파 인간·장치 모델에 기대며, 초기 실험은 정성적이었다. [DOI](https://doi.org/10.1115/IMECE1996-0362).
6. **Hannaford & Ryu, "Time-Domain Passivity Control of Haptic Interfaces," IEEE TRA 18(1), 2002.** 일률의 부호, 에너지 관측기, 적응적 소산 요소를 따라가라. 이 방법은 정확한 환경 모델을 피하지만 잡음, 영속도, 포화, 성능 절충은 여전히 남는다. [DOI](https://doi.org/10.1109/70.988969).
7. **Raju, Verghese & Sheridan, "Design Issues in 2-Port Network Models of Bilateral Remote Manipulation," ICRA 1989.** 원하는 포트 임피던스와 인간·과제 모델에서 안정한 이득 선택으로 가는 고전적 다리다. 그 보장은 명시한 수동적 termination 부류와 모델 가정 위에서만 성립한다. [DOI](https://doi.org/10.1109/ROBOT.1989.100162).
8. **Colonnese & Okamura, "Stability and quantization-error analysis of haptic rendering of virtual stiffness and damping," IJRR 35(9):1103–1120, 2016**(온라인 2015). 샘플링, 위치 양자화, 시간 지연, 속도 추정용 저역통과 필터를 1자유도 모델 하나에 함께 넣고 그 사이의 절충을 유도한 논문이다. 양자화 오차 수동성의 충분조건과, (malicious·uncoupled touch) 극한 주기가 없기 위한 필요조건을 함께 제시한다. Phantom Premium 1.5로 검증했고, 초록에는 수치 결과가 없다. 연도만 쓰지 말고 권호를 써라 — 2015년에 온라인, 2016년에 지면으로 나왔다. [DOI](https://doi.org/10.1177/0278364915596234).
9. **Salisbury, Conti, Barbagli, "Haptic rendering: introductory concepts," IEEE CG&A 24(2), 2004.** 렌더링을 충돌 검출·힘 계산·구동의 루프로 틀 짓는 서베이다. 어떤 렌더링 논문보다 먼저 읽어라. [DOI](https://doi.org/10.1109/MCG.2004.1274058).
10. **Ruspini, Kolarov, Khatib, "The haptic display of complex graphical environments," SIGGRAPH 1997; Zilles & Salisbury, "A constraint-based god-object method for haptic display," IROS 1995.** proxy 논문 둘이다. Ruspini는 벌점 렌더링의 세 실패에 이름을 붙였고, Zilles와 Salisbury는 2년 앞서 제약된 점을 도입했다. [DOI](https://doi.org/10.1145/258734.258878) · [DOI](https://doi.org/10.1109/IROS.1995.525876).
11. **Kuchenbecker, Fiene, Niemeyer, "Improving contact realism through event-based haptic feedback," IEEE TVCG 12(2), 2006.** 피험자 9명의 현실감 연구를 담은 WHC 2005 학회 판본과 함께 읽어라. 현실감은 과제로 잰 것이 아니라 평가 점수였다는 점을 기억하라. [DOI](https://doi.org/10.1109/TVCG.2006.32) · [DOI](https://doi.org/10.1109/WHC.2005.52).
12. **Richard & Cutkosky, "Friction modeling and display in haptic applications involving user performance," ICRA 2002.** Karnopp 구현과, 적당한 마찰은 돕고 높은 정지 마찰은 해친다는 피험자 20명의 Fitts 연구. [DOI](https://doi.org/10.1109/ROBOT.2002.1013425).

9–12번의 알고리즘 — 벌점·proxy 렌더링, 사건 기반 과도 신호, 마찰 표시 — 은 [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 햅틱 렌더링 알고리즘]]에서 계산 예제와 함께 풀어 둔다.

### 5. 제공된 과목 자료를 어떻게 선별했는가

| 로컬 자료 부류 | 공개 학습 용도 |
|---|---|
| syllabus와 강의 슬라이드 | 트랙 범위, 선수 지식 지도, 개념, 판본 단서 |
| MATLAB 템플릿과 야코비안 스크립트 | 독자적 유도와 구현 체크리스트. 제출 답안은 옮기지 않음 |
| Hapkit 슬라이드와 기구 파일 | 24.3–24.4의 전동·센싱 논리. 제작 지침과 원본 파일은 공개하지 않음 |
| 과제와 학생 초안 | 필요한 역량과 흔한 오류 식별. 정답지나 개인 작업물은 공개하지 않음 |
| 프로젝트 선택지와 평가표 | 이전 가능한 프로젝트 설계·평가 기준. 사적 연락처와 미검증 주장은 제외 |
| 동의서, 모집 자료, 사전·사후 설문 | 윤리, 참가 자격, workload, 개인정보, 측정 설계. 양식을 옮기거나 재사용 가능한 승인으로 취급하지 않음 |
| 라이선스 읽기 자료 | 주석 단 개념과 공식 DOI·출판사 링크. PDF는 비공개 |

이 자료 묶음은 햅틱 과목 전반부를 특히 잘 덮는다. syllabus가 예고한 후반 강의·실습 자료 전부 — 완전한 CHAI3D, 고급 원격조작, ROS 순서 같은 것 — 를 담고 있지는 않다. 그래서 이 안내는 그 강의들을 복원하지 않으며, 다룬다고 주장하지도 않는다.

**계산해 읽기: 과제가 묻는 세 독해.** TLX가 내려가고 시간이 줄었다는 "햅틱이 더 낫다"에는 이름 붙은 estimand가 없고 피부 자극을 건너뛰었다. $n=600$은 nested trial이고 단위는 사람 20명이다. 벤치 응답은 검출 가능성이 아니고, 과제 개선은 현장 일반화가 아니다.

### 6. 과제가 그릴 그림

그림 하나. 과제는 더 짧은 기록을 다른 규칙으로 받아 같은 그림을 그리라고 한다.

<svg viewBox="0 0 560 350" style="max-width:100%;height:auto" role="img" aria-label="0.05 N 간격의 줄 위를 오가는 24시행 2-down 1-up staircase로, 정답은 채운 표식과 오답은 빈 표식, 번호를 단 reversal 여덟 개 중 앞의 둘에 줄을 긋고, 0.5167 N 점선에 70.7% 정답 기준을 붙이고, 인과 사슬에서는 자극에서 지각으로 가는 화살표에만 체크했다.">
  <circle cx="58" cy="17" r="3.8" fill="currentColor"/>
  <text x="67" y="21" font-size="11" fill="currentColor">정답</text>
  <circle cx="108.1" cy="17" r="3.8" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="117.1" y="21" font-size="11" fill="currentColor">오답</text>
  <circle cx="162.3" cy="17" r="7.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="174.3" y="21" font-size="11" fill="currentColor">reversal</text>
  <circle cx="244.7" cy="17" r="7.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <line x1="235.7" y1="26" x2="253.7" y2="8" stroke="currentColor" stroke-width="1.5"/>
  <text x="257.7" y="21" font-size="11" fill="currentColor">버림 (§7 Step 2)</text>
  <g stroke="currentColor" stroke-width="0.8" stroke-opacity="0.28"><line x1="53" y1="200" x2="403" y2="200"/><line x1="53" y1="170" x2="403" y2="170"/><line x1="53" y1="140" x2="403" y2="140"/><line x1="53" y1="110" x2="403" y2="110"/><line x1="53" y1="80" x2="403" y2="80"/><line x1="53" y1="50" x2="403" y2="50"/></g>
  <g font-size="11" fill="currentColor" text-anchor="end" opacity="0.8"><text x="49" y="204">0.40</text><text x="49" y="174">0.45</text><text x="49" y="144">0.50</text><text x="49" y="114">0.55</text><text x="49" y="84">0.60</text><text x="49" y="54">0.65</text></g>
  <text x="14" y="38" font-size="11.5" fill="currentColor" opacity="0.9">ΔF (N)</text>
  <line x1="53" y1="208" x2="403" y2="208" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55"/>
  <g stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55">
    <line x1="58" y1="208" x2="58" y2="213"/><line x1="72.8" y1="208" x2="72.8" y2="211"/><line x1="87.6" y1="208" x2="87.6" y2="211"/><line x1="102.3" y1="208" x2="102.3" y2="213"/><line x1="117.1" y1="208" x2="117.1" y2="211"/><line x1="131.9" y1="208" x2="131.9" y2="211"/><line x1="146.7" y1="208" x2="146.7" y2="211"/><line x1="161.5" y1="208" x2="161.5" y2="213"/><line x1="176.3" y1="208" x2="176.3" y2="211"/>
    <line x1="191" y1="208" x2="191" y2="211"/><line x1="205.8" y1="208" x2="205.8" y2="211"/><line x1="220.6" y1="208" x2="220.6" y2="213"/><line x1="235.4" y1="208" x2="235.4" y2="211"/><line x1="250.2" y1="208" x2="250.2" y2="211"/><line x1="265" y1="208" x2="265" y2="211"/><line x1="279.7" y1="208" x2="279.7" y2="213"/><line x1="294.5" y1="208" x2="294.5" y2="211"/><line x1="309.3" y1="208" x2="309.3" y2="211"/>
    <line x1="324.1" y1="208" x2="324.1" y2="211"/><line x1="338.9" y1="208" x2="338.9" y2="213"/><line x1="353.7" y1="208" x2="353.7" y2="211"/><line x1="368.4" y1="208" x2="368.4" y2="211"/><line x1="383.2" y1="208" x2="383.2" y2="211"/><line x1="398" y1="208" x2="398" y2="213"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8"><text x="58" y="225">1</text><text x="102.3" y="225">4</text><text x="161.5" y="225">8</text><text x="220.6" y="225">12</text><text x="279.7" y="225">16</text><text x="338.9" y="225">20</text><text x="398" y="225">24</text></g>
  <text x="228" y="240" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">시행 번호</text>
  <line x1="53" y1="130" x2="406" y2="130" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 3"/>
  <g font-size="12" fill="currentColor"><text x="411" y="134">70.7% 정답,</text><text x="411" y="149">2-down 1-up,</text><text x="411" y="164">받침 5.00 N</text></g>
  <g font-size="11" fill="currentColor" opacity="0.75"><text x="411" y="183">0.5167 N = reversal</text><text x="411" y="197">3–8의 평균</text></g>
  <g stroke="currentColor" stroke-width="1.3" stroke-opacity="0.75">
    <line x1="62.4" y1="80" x2="68.4" y2="80"/><line x1="74.7" y1="83.9" x2="85.6" y2="106.1"/><line x1="92" y1="110" x2="97.9" y2="110"/><line x1="104.3" y1="106.1" x2="115.2" y2="83.9"/><line x1="121.5" y1="80" x2="127.5" y2="80"/><line x1="133.9" y1="83.9" x2="144.8" y2="106.1"/><line x1="151.1" y1="110" x2="157.1" y2="110"/><line x1="163.4" y1="113.9" x2="174.3" y2="136.1"/>
    <line x1="180.7" y1="140" x2="186.6" y2="140"/><line x1="193" y1="143.9" x2="203.9" y2="166.1"/><line x1="207.8" y1="166.1" x2="218.7" y2="143.9"/><line x1="225" y1="140" x2="231" y2="140"/><line x1="237.3" y1="136.1" x2="248.2" y2="113.9"/><line x1="254.6" y1="110" x2="260.6" y2="110"/><line x1="266.9" y1="113.9" x2="277.8" y2="136.1"/><line x1="281.7" y1="136.1" x2="292.6" y2="113.9"/>
    <line x1="298.9" y1="110" x2="304.9" y2="110"/><line x1="311.2" y1="113.9" x2="322.1" y2="136.1"/><line x1="328.5" y1="140" x2="334.5" y2="140"/><line x1="340.8" y1="136.1" x2="351.7" y2="113.9"/><line x1="358.1" y1="110" x2="364" y2="110"/><line x1="370.4" y1="113.9" x2="381.3" y2="136.1"/><line x1="387.6" y1="140" x2="393.6" y2="140"/>
  </g>
  <g fill="currentColor">
    <circle cx="58" cy="80" r="3.8"/><circle cx="72.8" cy="80" r="3.8"/><circle cx="87.6" cy="110" r="3.8"/><circle cx="117.1" cy="80" r="3.8"/><circle cx="131.9" cy="80" r="3.8"/><circle cx="146.7" cy="110" r="3.8"/><circle cx="161.5" cy="110" r="3.8"/><circle cx="176.3" cy="140" r="3.8"/><circle cx="191" cy="140" r="3.8"/><circle cx="220.6" cy="140" r="3.8"/><circle cx="250.2" cy="110" r="3.8"/>
    <circle cx="265" cy="110" r="3.8"/><circle cx="294.5" cy="110" r="3.8"/><circle cx="309.3" cy="110" r="3.8"/><circle cx="324.1" cy="140" r="3.8"/><circle cx="353.7" cy="110" r="3.8"/><circle cx="368.4" cy="110" r="3.8"/><circle cx="383.2" cy="140" r="3.8"/><circle cx="398" cy="140" r="3.8"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="102.3" cy="110" r="3.8"/><circle cx="205.8" cy="170" r="3.8"/><circle cx="235.4" cy="140" r="3.8"/><circle cx="279.7" cy="140" r="3.8"/><circle cx="338.9" cy="140" r="3.8"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="102.3" cy="110" r="7.5"/><circle cx="131.9" cy="80" r="7.5"/><circle cx="205.8" cy="170" r="7.5"/><circle cx="265" cy="110" r="7.5"/><circle cx="279.7" cy="140" r="7.5"/><circle cx="309.3" cy="110" r="7.5"/><circle cx="338.9" cy="140" r="7.5"/><circle cx="368.4" cy="110" r="7.5"/></g>
  <g font-size="11.5" fill="currentColor" text-anchor="middle"><text x="91.3" y="102">1</text><text x="131.9" y="68">2</text><text x="205.8" y="192">3</text><text x="265" y="98">4</text><text x="279.7" y="162">5</text><text x="309.3" y="98">6</text><text x="338.9" y="162">7</text><text x="368.4" y="98">8</text></g>
  <g stroke="currentColor" stroke-width="1.6"><line x1="93.5" y1="118.8" x2="111.1" y2="101.2"/><line x1="123.1" y1="88.8" x2="140.7" y2="71.2"/></g>
  <text x="8" y="260" font-size="11" fill="currentColor" opacity="0.9">§1의 인과 사슬: 체크는 이 그림이 재는 단 하나의 화살표</text>
  <rect x="8" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor" text-anchor="middle"><text x="67" y="292.2">액추에이터</text><text x="67" y="305.8">명령</text></g>
  <line x1="129" y1="295" x2="140.5" y2="295" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="147,295 140,298.4 140,291.6" fill="currentColor"/>
  <rect x="132" y="328" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <rect x="150" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <g font-size="11" fill="currentColor" text-anchor="middle"><text x="209" y="292.2">실제 전달된</text><text x="209" y="305.8">역학 자극</text></g>
  <line x1="271" y1="295" x2="282.5" y2="295" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="289,295 282,298.4 282,291.6" fill="currentColor"/>
  <rect x="274" y="328" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <polyline points="276.2,334 279,337.5 284.5,329.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
  <rect x="292" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="351" y="299" font-size="11" fill="currentColor" text-anchor="middle">지각·행동</text>
  <line x1="413" y1="295" x2="424.5" y2="295" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="431,295 424,298.4 424,291.6" fill="currentColor"/>
  <rect x="416" y="328" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <rect x="434" y="270" width="118" height="50" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="493" y="299" font-size="11" fill="currentColor" text-anchor="middle">과제 결과</text>
</svg>

가로는 시행 번호 1에서 24, 세로는 $\Delta F$를 $0.40$에서 $0.65\,\mathrm{N}$까지 $0.05\,\mathrm{N}$ 간격의 줄로 긋는다. 단 크기가 고정이므로 수준은 언제나 줄 위에만 있을 수 있기 때문이다. 24개 수준을 찍고 이웃 시행을 이어 하나의 연속된 궤적으로 만든다. 정답은 채운 표식, 오답은 빈 표식으로 그려서 규칙이 그림에서 바로 읽히게 한다. 궤적은 채운 표식이 둘 연달아야만 내려가고, 빈 표식이 나오면 곧바로 올라간다. 진행 방향이 바뀌는 시행마다 동그라미를 치고 $1$에서 $8$까지 번호를 매긴다. 첫 두 동그라미에는 줄을 긋는다. §7 Step 2가 버리는 것들이다. 남은 여섯의 평균에 수평선을 긋되, 라벨에 "임계값"이라고 쓰지 말고 그것이 추정하는 기준을 쓴다. *70.7% 정답, 2-down 1-up, 받침 5.00 N*. 그림 옆에는 §1의 인과 사슬을 옮겨 적고, 이 그림이 재는 단 하나의 화살표 아래에만 체크를 하고 나머지 둘은 비워 둔다.

### 7. 대상으로 한 번 끝까지: staircase 기록이 임계값과 JND가 되기까지

**Step 1 — reversal 찾기.** 기록을 따라가며 방향이 바뀌는 시행을 표시한다. 규칙은 연속 `C` 둘 뒤에만 내려가고 `W` 하나에 바로 올라가므로 reversal은 여덟이다.

| reversal | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 시행 | 4 | 6 | 11 | 15 | 16 | 18 | 20 | 22 |
| $\Delta F$ (N) | 0.55 | 0.60 | 0.45 | 0.55 | 0.50 | 0.55 | 0.50 | 0.55 |

**Step 2 — 가라앉은 부분만 평균.** 첫 두 reversal은 버린다. 일부러 쉬운 수준에서 시작했기 때문에 초반 궤적은 참가자가 아니라 시작점을 기록하고 있다. 나머지를 평균하면

$$\widehat{\Delta F}=\frac{0.45+0.55+0.50+0.55+0.50+0.55}{6}=\frac{3.10}{6}=0.5167\ \mathrm{N}$$

이다. 궤적의 마루와 골이 똑같이 기여하도록 reversal 개수를 짝수로 쓴다.

**Step 3 — 그것은 어느 확률을 추정했나?** 논문이 건너뛰는 단계이고, 대수 한 줄이면 된다. 시행이 독립이고 가라앉은 수준 근처에서 정답 확률 $p$가 국소적으로 일정하다고 하자. 2-down 1-up에서 수준이 *내려가는* 것은 연속 두 시행을 맞힐 때뿐이므로 확률 $p^2$이고, *올라가는* 것은 그 밖의 경우이므로 $1-p^2$다. 궤적이 평균적으로 위로도 아래로도 떠나지 않는 수준에서 둘이 같으므로

$$p^2=1-p^2\quad\Longrightarrow\quad p^2=\tfrac12\quad\Longrightarrow\quad p=\sqrt{0.5}=0.7071$$

이고, 따라서 이 추정값은 이 참가자 곡선의 $70.7\%$ 정답 점이다. $75\%$ 점도 아니고 그냥 "임계값"도 아니다. (얼어붙은 기록의 전체 정답률은 $19/24=79.2\%$로 $70.7\%$보다 높지만, 24 시행의 평범한 표본 변동이지 규칙이 실패했다는 증거가 아니다.) [[06-research-practice/psychophysics-human-measurement|8. 심리물리와 인간 측정 §2]]는 같은 논증을 모든 1-up-$n$-down 규칙으로 넓혀 $p^\ast=2^{-1/n}$을 얻고, 그 §7은 고정된 관찰자 위에서 staircase를 시뮬레이션해 유한한 단과 아직 잊히지 않은 시작점이 추정값에 더하는 몫을 잰다.

**Step 4 — 양에 이름 붙이기.** $\widehat{\Delta F}=0.5167\,\mathrm{N}$은 *차이* 임계값이다. $5.00\,\mathrm{N}$ 받침 위에서 이 참가자가 $70.7\%$ 맞히는 증분. 기준을 함께 달아 놓을 때에만 그것이 JND다. Weber 분수는

$$k=\frac{\widehat{\Delta F}}{F_0}=\frac{0.5167}{5.00}=0.1033,$$

즉 $10.3\%$다. 증분을 잰 작동점이 곧 받침이기 때문이다.

**Step 5 — 다른 방법과 비교하면 estimand 문제가 눈앞에 나타난다.** [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]]은 같은 참가자를 같은 핸들의 같은 $5\,\mathrm{N}$ 작동점에서 constant stimuli로 재어 $\mathrm{JND}=0.4107\,\mathrm{N}$, $k=8.1\%$를 얻었다. 이 staircase는 $0.5167\,\mathrm{N}$, $26\%$ 더 크다. 어느 쪽도 틀리지 않았고 어느 쪽도 잡음이 아니다. 하나는 *더 세다고 판정* 곡선의 PSE 둘레 $25$–$75$ 구간의 절반이고, 다른 하나는 차이 검출 과제에서 $70.7\%$ *정답*이 되는 증분이다. 서로 다른 함수의 서로 다른 점이다. 기준과 과제 없이 "그 JND"를 보고한 논문은 다른 연구실이 재현할 수도 비교할 수도 없는 숫자를 만든 것이고, 이것이 §2의 estimand 요구를 산술로 다시 쓴 것이다.

**Step 6 — 장치에 대고 확인하기.** [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]]의 P3 벽 양자 $\Delta F_{\text{count}}=0.0245\,\mathrm{N}$을 쓰면, 임계값은 $0.5167/0.0245=21.1$ 카운트이고 침투로는 $0.5167/400=1.29\,\mathrm{mm}$다. staircase 자신의 단 $0.05\,\mathrm{N}$은 $0.05/0.0245=2.0$ 카운트이므로 이 실험의 해상도는 하드웨어가 아니라 실험자가 고른 단이 정했다. 다만 단을 $0.02\,\mathrm{N}$로 잡았다면 $0.8$ 카운트로 장치가 구별하지 못하는 크기이고, 궤적은 양자화 위에서 멈춰 있는데 보고서에는 수렴한 임계값이 적히게 된다.

**Step 7 — 기록 하나가 지지하는 것.** 참가자 한 명, 24 시행이므로 불확실성이 큰 개인 추정값을 지지할 뿐 모집단에 대해서는 아무것도 지지하지 않는다. 20명을 돌려도 어떤 처치 주장에서든 단위는 여전히 참가자다. 480 trial이 아니라 임계값 추정치 20개를 분석한다. §2의 7번 항목이고 아래 자가 점검이다. §3의 사다리에서 이 숫자는 "심리물리 임계값" 줄에 앉는다. 시험한 조건에서의 검출 가능성을 지지하지, 더 나은 과제 제어를 지지하지 않는다.

### 스스로 점검

1. Step 2는 reversal 여섯을 평균하고 Step 3은 이 규칙이 $70.7\%$ 정답을 겨냥함을 보인다. 두 번째 단계가 왜 선택적인 장부 정리가 아닌가? 논문이 $\widehat{\Delta F}=0.5167\,\mathrm{N}$만 준다면 정확히 무엇이 보고되지 않은 것인가?
2. 같은 참가자, 같은 핸들, 같은 $5\,\mathrm{N}$ 작동점인데 24.1은 $0.4107\,\mathrm{N}$, 여기는 $0.5167\,\mathrm{N}$로 $26\%$ 벌어진다. 둘 중 틀린 쪽은 어디이고, 그것을 가르는 질문은 무엇인가?
3. Step 6은 이 하드웨어에서 $0.02\,\mathrm{N}$ 계단이 실수라고 말한다. 계산을 보이고, 그 실수 대신 보고서에 무엇이 적히게 될지 말하라.
4. within-subject 연구에서 20명이 각 30 trial을 했다면 $n=600$인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 기준 없는 자극 수준은 양이 아니다. $0.5167\,\mathrm{N}$은 *이* 규칙이 참가자를 붙들어 두는 증분이고, 그것이 곡선 위 어느 점인지는 규칙이 정한다. 2-down/1-up을 3-down/1-up으로 바꾸면 같은 기록, 같은 피부, 같은 핸들이 $p=0.5^{1/3}=0.7937$을 내놓는다. 다른 점이고, 규칙을 듣지 않은 독자는 환산할 수 없는 숫자다. 그러니 보고되지 않은 것은 estimand 자체이고, 이것이 §2 항목 1을 산술로 다시 쓴 것이다.
> 2. 어느 쪽도 틀리지 않았고 그 간격은 잡음이 아니다. 가르는 질문은 *참가자가 무엇을 하라고 요구받았는가*다. constant stimuli는 **더 세다고 판정**한 곡선의 PSE 둘레 $25$–$75$ 구간의 절반을 쟀고, staircase는 차이 검출 과제에서 $70.7\%$ **정답**이 되는 증분을 쟀다. 과제 둘, 기준 둘, 함수 둘이다. 두 숫자는 명시된 심리측정 모형을 거쳐야만 비교되고, "그 JND"를 맨몸으로 보고한 논문은 다른 연구실이 재현할 수 없는 값을 낸 것이다.
> 3. 기본 벽에서 엔코더 한 카운트는 $\Delta F_{\text{count}}=0.0245\,\mathrm{N}$이므로 $0.02\,\mathrm{N}$ 계단은 $0.02/0.0245=0.82$ 카운트다. 장치 자체의 양자보다 작아서, 한 계단 내리라는 명령이 전달되는 힘을 전혀 바꾸지 못할 수 있다. 실제로 쓴 $0.05\,\mathrm{N}$ 계단은 $0.05/0.0245=2.0$ 카운트라 하드웨어가 구별한다. 그러면 트랙은 참가자가 아니라 양자화 위에서 멈추고, 보고서에는 엔코더를 잰 값이 아름답게 수렴한 임계값으로 적힌다.
> 4. 참가자 수준의 처치 주장에서는 아니다. trial은 참가자 안에 nested된 반복 관측이다. 참가자별 요약이나 위계·혼합 모델(참가자마다 자기 기준선을 주어 한 사람의 반복 trial을 서로 독립인 사람처럼 세지 않는 회귀)로 그 의존성을 다루고, 참가자 20명과 trial 600회를 모두 보고하라.

### 과제 · Problem set

Tier C — 이 페이지는 트랙의 읽기 지도이므로 과제도 주장 읽기로 남는다. §7이 이 페이지가 갚아야 할 유도이고, 아래 1번과 2번이 규칙을 바꿔 그 유도를 다시 하는 것이다. 이 페이지와 [[02-foundations/lab-plants|0.6]], 그리고 비교용으로 [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1 §6]]을 쓴다.

같은 핸들, 같은 $5.00\,\mathrm{N}$ 받침, 같은 $0.05\,\mathrm{N}$ 단. 다만 규칙을 **3-down 1-up**으로 바꾸고 $\Delta F=0.50\,\mathrm{N}$에서 시작한다. 12 시행이고 역시 예시 값이다.

| # | $\Delta F$ (N) | 응답 | # | $\Delta F$ (N) | 응답 |
|---:|---:|:---|---:|---:|:---|
| 1 | 0.50 | C | 7 | 0.50 | C |
| 2 | 0.50 | C | 8 | 0.50 | C |
| 3 | 0.50 | C | 9 | 0.45 | C |
| 4 | 0.45 | C | 10 | 0.45 | C |
| 5 | 0.45 | W | 11 | 0.45 | C |
| 6 | 0.50 | C | 12 | 0.40 | W |

1. **그려라.** 이 기록으로 §6의 그림을 같은 $0.05\,\mathrm{N}$ 줄 위에 그려라. reversal을 표시하고, §6의 줄 긋는 지시를 여기서는 수행할 수 없는 이유를 말하라.
2. **유도하라.** (a) reversal 시행과 그 수준. (b) 임계값 추정값과, 그것을 어떻게 평균했는지에 대해 반드시 함께 붙여야 하는 문장. (c) §7 Step 3의 논증으로, 3-down 1-up 규칙의 기준 확률과 1-up 1-down 규칙의 기준 확률. (d) Weber 분수와, 그 추정값을 P3 엔코더 카운트로.
3. **해석하라.** (a) 어떤 논문이 2AFC 과제에서 1-up 1-down staircase를 돌리고 결과를 "검출 임계값"으로 보고한 뒤 다른 연구실의 constant-stimuli JND와 비교한다. 서로 다른 두 estimand 오류에 이름을 붙여라. 첫째는 (c)를 쓴다. (b) 어떤 연구가 NASA-TLX가 내려가고 완료 시간이 줄었으니 "햅틱이 더 낫다"고 보고한다. 빠진 estimand는 무엇이고, 액추에이터 $\to$ 자극 $\to$ 지각 $\to$ 결과의 어느 화살표가 재지지 않았는가? (c) 20명이 각 30 trial, t-검정에서 $n=600$. 분석 단위는 무엇이고, 보고가 여전히 말해야 하는 것은? (d) 증거 사다리에 "액추에이터 벤치 응답"과 "통제된 과제 개선"을 놓아라. 각각이 아직 지지하지 못하는 것은?

> [!tip]- 정답 · Solutions
> 1. 궤적은 채운 표식이 셋 연달아야만 내려가므로 §6의 그림보다 한 수준에 더 오래 머문다. reversal은 셋이다. §6은 앞의 둘을 버리고 여섯을 평균하는데, 여기서는 그러면 하나가 남는다. 줄 긋기를 수행할 수 없다는 것 자체가 결과이지 불편이 아니다.
> 2. (a) 시행 5에서 $0.45$, 시행 8에서 $0.50$, 시행 12에서 $0.40$. (b) 셋을 모두 평균하면 $(0.45+0.50+0.40)/3=0.45\,\mathrm{N}$이고, 붙여야 할 문장은 이것이 12 시행짜리 run의 reversal *전부*, 즉 홀수 개의 평균이며 burn-in을 하나도 버리지 않았다는 것이다. 그래서 마루와 골이 똑같이 기여하지 않고 추정값이 시작점을 함께 지고 있다. 보통은 reversal 여섯 이상을 최소로 보므로 이 run은 예비 실험으로 다뤄야 한다. (c) 이제 한 단 내려가려면 연속 셋을 맞혀야 하므로 확률은 $p^3$이고, 정상성에서 $p^3=1-p^3$, $p^3=0.5$, $p=0.5^{1/3}=0.7937$, 즉 $79.4\%$ 정답 점이다. 1-up 1-down은 한 번만 맞히면 내려가므로 $p=1-p$에서 $p=0.5$인데, 2대안 과제에서 그것은 chance다. 참가자가 찍고 있는 수준을 추적하는 셈이라 아무것도 추정하지 못한다. (d) $k=0.45/5.00=0.090$, 즉 $9.0\%$. 그리고 $0.45/0.0245=18.4$ 카운트, 침투로는 약 $1.13\,\mathrm{mm}$.
> 3. (a) 첫째, 그 규칙은 $p=0.5$를 겨냥하는데 2AFC에서 그것은 chance이므로 "임계값"이 애초에 임계값이 아니다. 어떤 자극 수준도 식별되지 않았다. 둘째, 유효한 staircase 숫자라 해도 constant-stimuli JND와는 다른 estimand다(§7 Step 5). 과제가 다르고 기준이 다르고 곡선 위의 점이 다르다. 둘을 비교하려면 명시한 심리측정 모델을 거치거나, 아니면 비교하지 말아야 한다. (b) Estimand는 이름 붙은 양이어야 한다(첨두 접촉력이지 "더 낫다"가 아님). TLX는 자기보고 workload이지 역학 자극이 아니고, 시간은 어느 cue가 변화를 일으켰는지 가리지 않는다. 피부 자극을 보정하라. (c) 처치 주장의 단위는 참가자이고 trial은 nested다. 사람 $20$명 *과* trial $600$회를, 위계·혼합 모델이나 참가자별 요약과 함께 보고한다. (d) 벤치 응답은 전달된 동역학을 지지하지 검출 가능성을 지지하지 않는다. 과제 개선은 그 프로토콜 안의 인과 효과를 지지하지 현장 일반화를 지지하지 않는다.
