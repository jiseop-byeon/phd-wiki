---
title: 10. Robot Systems, Embodiment & Deployment
tags: [robotics, systems, deployment, ros]
study-depth: Working
wiki-support: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

*Group F. Stands on [[04-robotics/state-estimation-slam|3]], [[04-robotics/planning-decision-making|4]], [[04-robotics/control-theory-ce397|5]] plus signal processing and [[02-foundations/se3-geometry|SE(3)]].
What an algorithm still needs before it is a robot: clocks, frames, rates, logs, and the failures that live between blocks.*

A paper algorithm becomes a robot only when sensors, clocks, coordinate frames, computers, networks, controllers, actuators, safety logic, and logging work together. Systems literacy lets a reader determine what was actually deployed and where a reported improvement may have originated.

> [!info] Depth target
> Decompose a robot into its runtime pipeline; interpret action interfaces, timing, frames, middleware, reliability, simulation, and logging; and diagnose failures at subsystem boundaries. This is not a ROS installation or electronics tutorial.

> [!note] Prerequisites
> [[02-foundations/lab-plants|0.6 Lab Plants]] (plant P6 — *plant* is control's word for the system being controlled, and P6 is the catalog's cart with a camera and a controller on one clock) · [[02-foundations/signal-processing|Signal Processing]] · [[02-foundations/se3-geometry|3D Geometry & SE(3)]] · [[04-robotics/state-estimation-slam|State Estimation]] · [[04-robotics/planning-decision-making|Planning]] · [[04-robotics/control-theory-ce397|Control Theory]]. §6.5's temporal logic assumes no logic course: it defines the propositions and connectives it uses.

> [!note] Why this matters · 왜 배우는가
> This page is not one layer of the robot stack of [[07-research-program/index|7. Research Program §5]] but the runtime beside it — clocks, frames, the execution layer and the logs, the *systems* column of the [[physical-ai-map|Physical AI Map]] — and in *"install that panel on the frame"* it carries two steps, *decompose the job* with the behavior tree of §6 and the "deliver A, then B" specification of §6.5, and *verify completion* with §8's calibration record and §10's failure taxonomy, while its timing budget runs under every other step. Without it a correct algorithm fails in ways no retraining repairs: on P6, the catalog's cart with a 50 Hz camera and a 200 Hz controller, a goal that reaches the controller 200 ms old is 130 ms over its 70 ms budget and 20 mm (41 counts) behind the cart (Worked case), and a controller set for 2000 instead of 2048 counts/m is 24 mm wrong after one metre on every run, which no random seed reveals (§8). The budget returns as the staleness check of [[04-robotics/capstone-panel-contact|26. Capstone §5]] and its step 8, the frames as the frame chain of S1, the construction track's 20 kg facade-panel task ([[05-construction-robotics/site-engineering|2.5 §2]], block 6), and the rates of §2–§3 as the budget [[03-deep-learning/vla/index|deep learning 4]] stands on (block 4); here it is block 2 of the dissertation path, robotics sessions 86–89 ([[07-research-program/index|7 §8]]). After it you can add up a loop's latency term by term, draw a TF tree with each transform's direction and stamp, and name the subsystem a failure started in rather than the one where it ended.

> [!note] First pass · 처음이라면
> About four sessions of 60–90 minutes, robotics sessions 86–89 — a checklist page more than a narrative. **Session 1:** the Running object, the picture and the Worked case, then §1–§3; leave §3's Deeper note. End by rebuilding P6's budget with the page covered: $70$ ms as $3.5$ vision periods and $14$ ticks, where it sits in §3's sum, and the $200$ ms goal's $130$ ms, $40$ ticks and $41$ counts. **Session 2:** §4–§6; end by drawing §4's panel-cell TF tree with each edge's direction and stamp, and §6's example tree at the tick where `batteryOK` fails. **Session 3:** §6.5 — run its listing — then §7–§11; end by walking §9's ladder on the panel task and placing one field failure in §10's taxonomy, then self-check 5 and 6. **Session 4:** the rest of the self-check and the problem set, whose lab sweeps §5's queue depth. The Deeper notes (the Eppner paper's two other axes, the worst-case sampling term, and §6.5's synthesis cost and signal temporal logic) are for when a paper needs them.

### Running object · 이 페이지의 대상

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]]. A *plant* is control's word for the physical system being controlled, and P6 is the catalog's cart on a clock: a cart on a straight rail, driven by one motor, its position $p$ counted by an encoder. A camera watches it and a vision node publishes a goal for the cart; a controller reads the encoder and writes a motor command. P6 freezes four numbers, and the page adds one:

| Symbol | Value | What it is |
|---|---:|---|
| $N$ | $2048$ counts/m | encoder resolution, so one count is $1000/2048=0.488$ mm |
| $T_{\text{cam}}$ | $20$ ms | vision period: a goal every $20$ ms, $50$ Hz |
| $T_{\text{ctrl}}$ | $5$ ms | control period, $200$ Hz; one period is a **tick**, the moment the controller reads the encoder and writes a command |
| budget | $70$ ms | the time allowed from the camera's exposure midpoint to the force applied at the cart |
| $v$ | $0.10$ m/s | the cart's speed in the Worked case (this page) |

The **budget** is the number this page is about: a goal older than it at the moment it acts is late, however good the goal was when it was made. §3 builds such a budget term by term, §8 uses the same encoder for a calibration error, and §11 the same clock for a policy's inference time.

*Scope: this page teaches the runtime concerns that sit between an algorithm and a robot — the loop, action interfaces, the latency budget with its deadlines and jitter, frames and the TF tree, middleware vocabulary, the execution layer and its behavior trees, the architecture lineages behind that layer and the formal task specifications of §6.5 (linear temporal logic, model checking versus reactive synthesis, realizability, the GR(1) fragment and signal temporal logic, taught from Boolean propositions up), reliability, staged deployment and the failure taxonomy. It does not teach ROS 2 itself, which is the pages of [[04-robotics/ros2/index|25. ROS 2]], nor control design ([[04-robotics/control-theory-ce397|5. Control]]), estimation ([[04-robotics/state-estimation-slam|3. State Estimation]]) or planning ([[04-robotics/planning-decision-making|4. Planning]]). It teaches what to check about them, and it is not an electronics or installation tutorial.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 356" style="max-width:100%;height:auto" role="img" aria-label="P6 on one time axis in milliseconds: vision ticks every 20 ms above, control ticks every 5 ms below, the five instants of one cycle, the 70 ms budget bar with its sampling segment, and a 200 ms stale goal drawn lighter">
  <line x1="96.6" y1="142" x2="530" y2="142" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="96.6" y1="118" x2="96.6" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="136" y1="118" x2="136" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="175.4" y1="118" x2="175.4" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="214.8" y1="118" x2="214.8" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="254.2" y1="118" x2="254.2" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="293.6" y1="118" x2="293.6" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="333" y1="118" x2="333" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="372.4" y1="118" x2="372.4" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="411.8" y1="118" x2="411.8" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="451.2" y1="118" x2="451.2" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="490.6" y1="118" x2="490.6" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="530" y1="118" x2="530" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="96.6" y1="142" x2="96.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="106.5" y1="142" x2="106.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="116.3" y1="142" x2="116.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="126.2" y1="142" x2="126.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="136" y1="142" x2="136" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="145.8" y1="142" x2="145.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="155.7" y1="142" x2="155.7" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="165.6" y1="142" x2="165.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="175.4" y1="142" x2="175.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="185.2" y1="142" x2="185.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="195.1" y1="142" x2="195.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="204.9" y1="142" x2="204.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="214.8" y1="142" x2="214.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="224.7" y1="142" x2="224.7" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="234.5" y1="142" x2="234.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="244.3" y1="142" x2="244.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="254.2" y1="142" x2="254.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="264.1" y1="142" x2="264.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="273.9" y1="142" x2="273.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="283.8" y1="142" x2="283.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="293.6" y1="142" x2="293.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="303.4" y1="142" x2="303.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="313.3" y1="142" x2="313.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="323.1" y1="142" x2="323.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="333" y1="142" x2="333" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="342.9" y1="142" x2="342.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="352.7" y1="142" x2="352.7" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="362.5" y1="142" x2="362.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="372.4" y1="142" x2="372.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="382.2" y1="142" x2="382.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="392.1" y1="142" x2="392.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="401.9" y1="142" x2="401.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="411.8" y1="142" x2="411.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="421.6" y1="142" x2="421.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="431.5" y1="142" x2="431.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="441.4" y1="142" x2="441.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="451.2" y1="142" x2="451.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="461.1" y1="142" x2="461.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="470.9" y1="142" x2="470.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="480.8" y1="142" x2="480.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="490.6" y1="142" x2="490.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="500.4" y1="142" x2="500.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="510.3" y1="142" x2="510.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="520.1" y1="142" x2="520.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="530" y1="142" x2="530" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="136" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">0</text>
  <text x="175.4" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">20</text>
  <text x="214.8" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">40</text>
  <text x="254.2" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">60</text>
  <text x="293.6" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">80</text>
  <text x="333" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">100</text>
  <text x="372.4" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">120</text>
  <text x="411.8" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">140</text>
  <text x="451.2" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">160</text>
  <text x="490.6" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">180</text>
  <text x="530" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">200 ms</text>
  <text x="530" y="111" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">vision · 50 Hz: a tall tick every 20 ms</text>
  <text x="530" y="178" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">control · 200 Hz: a short tick every 5 ms</text>
  <circle cx="136" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <text x="136" y="110" font-size="11.5" fill="currentColor" text-anchor="middle">exposure midpoint</text>
  <circle cx="244.3" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M244.3 138 V32 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="36" font-size="11.5" fill="currentColor">vision publish</text>
  <circle cx="258.1" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M258.1 138 V50 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="54" font-size="11.5" fill="currentColor">controller’s TF lookup</text>
  <circle cx="264.1" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M264.1 138 V68 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="72" font-size="11.5" fill="currentColor">controller tick that consumes the goal</text>
  <circle cx="273.9" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M273.9 138 V86 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="90" font-size="11.5" fill="currentColor">current reaches the motor</text>
  <rect x="96.6" y="190" width="19.7" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="3 2"/>
  <rect x="116.3" y="190" width="19.7" height="16" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="3 2"/>
  <rect x="136" y="190" width="137.9" height="16" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.3"/>
  <text x="204.9" y="202" font-size="11.5" fill="currentColor" text-anchor="middle" font-weight="600">70 ms budget</text>
  <text x="204.9" y="223" font-size="11" fill="currentColor" text-anchor="middle">70/20 = 3.5 vision periods</text>
  <text x="204.9" y="237" font-size="11" fill="currentColor" text-anchor="middle">70/5 = 14 control ticks</text>
  <text x="91.6" y="195" font-size="11" fill="currentColor" text-anchor="end">sampling</text>
  <text x="91.6" y="209" font-size="11" fill="currentColor" text-anchor="end">½T<tspan dy="3">cam</tspan><tspan dy="-3" dx="3">= 10 ms</tspan></text>
  <text x="91.6" y="223" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">worst 20 ms</text>
  <line x1="273.9" y1="206" x2="273.9" y2="260" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5" stroke-dasharray="3 3"/>
  <rect x="136" y="262" width="394" height="10" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="130" y="271" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">200 ms late</text>
  <text x="530" y="256" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">40 ticks on a stale goal (200/5)</text>
  <path d="M273.9 278 v6 H530.0 v-6" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="401.9" y="298" font-size="11" fill="currentColor" text-anchor="middle">200 − 70 = 130 ms over budget</text>
  <text x="12" y="312" font-size="11" fill="currentColor">At 0.10 m/s the cart moves 20 mm while that goal ages 200 ms:</text>
  <text x="12" y="326" font-size="11" fill="currentColor">20 mm ÷ 0.488 mm per count (1000/2048) = 41 counts the goal never knew about.</text>
  <text x="12" y="344" font-size="11" fill="currentColor" fill-opacity="0.7">P6 fixes only the bar’s two ends; the three instants inside it are illustrative.</text>
</svg>

P6 at its catalog rates on one time axis in milliseconds: vision ticks every $20\,\mathrm{ms}$ above, control ticks every $5\,\mathrm{ms}$ below, and the five instants of one cycle — from the exposure midpoint through the controller's TF lookup (its request for the goal's frame at the goal's time stamp, §4) to current reaching the motor — inside the $70\,\mathrm{ms}$ budget of $3.5$ vision periods and $14$ control ticks. The sampling segment $\tfrac12 T_{\text{cam}}=10\,\mathrm{ms}$ (worst $20\,\mathrm{ms}$) lies before the exposure midpoint, so P6's $70\,\mathrm{ms}$ does not contain it and §3's latency $L$ does: the budget is $L-\tfrac12T_{\text{cam}}$, an $L$ of $80\,\mathrm{ms}$ on average. The lighter bar is a goal that reaches the controller $200\,\mathrm{ms}$ late: $130\,\mathrm{ms}$ over budget, $40$ control ticks on a stale goal, and at $0.10\,\mathrm{m/s}$ the cart has moved $20\,\mathrm{mm}$, $41$ counts of $0.488\,\mathrm{mm}$, that the goal never knew about.

### Worked case · 대상으로 한 번 끝까지

One cycle of P6 held against its budget, in four steps and with the catalog's numbers. The budget and the tick are the Running object's; three words are used before the section that defines them, and each is glossed where it first appears.

**Step 1 — the budget in P6's own units.** $70\,\mathrm{ms}$ is $70/20=3.5$ vision periods and $70/5=14$ control ticks: while one exposure travels to the force it causes, three or four newer frames are taken and the controller ticks fourteen times. The budget starts at the exposure midpoint, the instant the image stands for, so the wait before that instant — $10\,\mathrm{ms}$ on average, the picture's dashed segment — is not in it; §3 counts that wait as the first term of the latency $L$.

**Step 2 — a goal 200 ms old.** A vision message that reaches the controller $200\,\mathrm{ms}$ after its exposure midpoint is $200-70=130\,\mathrm{ms}$ over budget, and $200/5=40$ ticks ran on it. A goal older than the budget is **stale** (§3 adds up what makes it so, and §5 shows one line of middleware configuration doing it). The age is also a distance: at $v=0.10\,\mathrm{m/s}$ the cart travels $0.10\times0.200=0.020\,\mathrm{m}=20\,\mathrm{mm}$, and at $0.488\,\mathrm{mm}$ a count that is $20/0.488=40.96\approx41$ counts the goal never knew about. The estimator of [[04-robotics/state-estimation-slam|3. State Estimation]] cannot save you: the goal is late, not noisy.

**Step 3 — does every tick finish on time?** Five ticks' measured response times, from the moment each tick is released to the end of its work, are $1.2, 1.5, 4.8, 1.3, 1.4\,\mathrm{ms}$. Each has a **deadline** of one period, $5\,\mathrm{ms}$, the time by which its work must be done. The mean is $2.04\,\mathrm{ms}$; the **jitter**, the spread from the fastest to the slowest (§3 defines both terms), is $4.8-1.2=\mathbf{3.6}\,\mathrm{ms}$; there are **zero** deadline misses; and the margin at the worst tick is $5.0-4.8=0.2\,\mathrm{ms}$ — that tick used $96\%$ of its period. *Non-example — quoting the mean as the rate:* $1000/2.04=490\,\mathrm{Hz}$ describes a loop that does not exist. The loop is $200\,\mathrm{Hz}$, and one tick in five came within $0.2\,\mathrm{ms}$ of missing; put the same work under the $1\,\mathrm{ms}$ deadline of a haptic servo that renders stiff contact ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]) and all five miss, with no change to the mean at all.

**Step 4 — the reading.** Rate, latency and noise are three different marks on the timeline: steps 1–2 are latency, step 3 is a deadline check at a fixed rate, and none of them is noise that filtering removes. When "nothing happens" on this plant, suspect a TF stamp or a QoS mismatch (quality of service, the middleware's delivery settings, §5) before a wrong gain — that drill is [[04-robotics/ros2/qos-executors-time|25.5]] — and what P6's sensors do contribute as noise, sensor by sensor, is [[04-robotics/sensor-models|3.2 Sensor Models & Noise]].

### 1. The closed robot stack

A robot's blocks run at different rates — a 30 Hz camera, a 10 Hz policy and a 1 kHz motor controller are not inconsistent — so the age of the data each block acts on, and the interfaces between them, have to be designed rather than assumed. The loop they form:

```mermaid
flowchart LR
    S["Sensors"] --> PRE["Preprocess"] --> EST["Estimate"] --> PP["Plan / Policy"] --> C["Controller"] --> A["Actuators"] --> W["Physical world"]
    W --> S
    LOG["Clock · frames · logs · safety"] -.-> EST
    LOG -.-> PP
    LOG -.-> C
```

Every arrow in it carries data of some age, and §3 counts that age.

> [!tip] The four axes a robot system is actually designed along
> The stack above is a data-flow picture. The *design* picture — the one that decides whether
> a system works on a deadline — is Eppner et al.'s post-mortem of the winning entry to the
> Amazon Picking Challenge 2015 (RSS 2016). They argue a robotic system is placed along four
> spectra, and that the winning system's placement along each of them differed from most other entries:
>
> | Axis | The trade |
> |---|---|
> | **Modularity vs. integration** | clean interfaces are debuggable; tightly integrated ones exploit information a module boundary would have discarded |
> | **Generality vs. assumptions** | every assumption you are willing to state buys performance and costs a failure mode when it breaks |
> | **Computation vs. embodiment** | a compliant gripper or a funnel-shaped fixture solves in mechanics what would otherwise be a perception and control problem |
> | **Planning vs. feedback** | deliberating in advance versus reacting during execution, and how much of each the task's uncertainty justifies |
>
> The third axis is the one most often skipped by a learning-first reader, and it is the same
> observation [[04-robotics/grasping|15 §5]] makes about extrinsic dexterity: geometry you
> arrange in advance is capability you do not have to compute. The Deeper note below gives the
> winning team's concrete choices on two other axes.

> [!note]- Deeper · 더 깊이
> The paper also names concrete choices on two other axes. On *modularity vs. integration*, the
> team matched perception to the gripper: a suction cup succeeds once it touches any pickable side,
> so object recognition only had to deliver a rough bounding-box pose, not an exact one. On
> *planning vs. feedback*, picks came from pre-defined sequences of force-guarded feedback
> controllers switched by sensor events (touch the object, then turn on suction), with the arm on a
> mobile base so that motion planning was mostly unnecessary.

### 2. Embodiment and action interfaces

The same learned model can behave differently when its low-level interface and control rate change, so a result about a robot's "action" means little until it names the physical command and the body that executes it. Embodiment includes morphology, actuator and transmission, sensing, compliance, payload, limits, and environment coupling. Motors, hydraulics, gearing, backlash, saturation, underactuation, and bandwidth determine which actions are meaningful. One geared electric drive opened up, with its two equations, torque–speed line, reflected inertia and thermal limit, is [[04-robotics/actuators-drives|10.5 Actuators & Drives]]; the physics under the two kinds of drive is [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics]] for the electric one and [[02-foundations/fluid-power|0.6.3 Fluid Power]] for the hydraulic one.

When a paper says “action,” identify whether it means joint position, velocity, torque, motor current, end-effector pose, [[04-robotics/force-compliance-control|impedance target]] (a desired stiffness and damping around a reference, not a position to hit exactly), or a high-level skill. An end-effector-pose action does not reach a motor until [[04-robotics/modern-robotics/ch06-inverse-kinematics|inverse kinematics (MR ch.6)]] resolves it — including its branch choices and singularities — and a waypoint action does not become motion until [[04-robotics/modern-robotics/ch09-trajectory-generation|time scaling (MR ch.9)]] gives it a velocity profile inside the actuator limits. On a wheeled base, both sit on the [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|nonholonomic kinematics of MR ch.13]].

### 3. Timing and a latency budget

*In one sentence:* a robot always acts on the world as it was a moment ago, and this section adds up how long that moment is, stage by stage, and asks whether the slowest cycle still finishes on time.

*If you need only one thing from this section:* a latency budget is a sum of named terms, not a frame rate — the $70\,\mathrm{ms}$ below is the formula's terms after the exposure midpoint, so it is $L-\tfrac12T_{\text{cam}}$ — and a delay is a distance, $7\,\mathrm{cm}$ at $1\,\mathrm{m/s}$; P6's goal $200\,\mathrm{ms}$ late is the Worked case above.

#### The example budget, and what a delay costs

| Component | Example latency |
|---|---:|
| Camera exposure/readout | 15 ms |
| Network inference | 40 ms |
| Communication | 10 ms |
| Command processing | 5 ms |
| **Observation-to-action** | **70 ms** |

At 1 m/s, 70 ms corresponds to 7 cm of motion before the new command has effect. Frequency is not latency: a 30 Hz system may still act on old frames. Check sampling rate, inference rate, jitter, deadline misses, queueing, timestamp policy, and whether latency was measured end-to-end. Whether a distance like those 7 cm is too large depends on what it would correct: set against an estimate's σ, it is the staleness distance of [[04-robotics/capstone-panel-contact|26. Capstone §5]].

#### The latency budget, term by term

**The budget, as a sum.** **Observation-to-action latency** $L$ is the elapsed time from the physical event to the moment the command derived from that event takes effect on the actuator. It is not one measurement but a sum of named terms, each of which some component owns:

$$L=\tfrac12 T_{\text{cam}}+t_{\text{exp}}+t_{\text{tx}}+t_{\text{inf}}+t_{\text{dec}}+T_{\text{ctrl}}$$

The terms add because the stages are in series and each must finish before the next begins. Each one:

- $\tfrac12 T_{\text{cam}}$ — **sampling latency**. The event occurs at a uniformly random moment inside one frame period $T_{\text{cam}}$, so on average it waits half a period before it is sampled at all, and a full period in the worst case. This is the term that does not appear in a block diagram and is the reason a *rate* is not a *latency*.
- $t_{\text{exp}}$ — **exposure and readout**, from the exposure midpoint, the instant the image stands for, to the last row leaving the sensor (the half-exposure before the midpoint belongs to the sampling wait); what each costs on a moving base, and which instant the image's stamp should name, is [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §2 and §9]].
- $t_{\text{tx}}$ — **transport**, the wire or bus to whichever computer runs the model; what a network adds, and what one lost packet costs under TCP and under UDP, is [[02-foundations/tools/computer-networks|12.5 Computer Networks §1]], and a latency measured across two machines also carries their clock offset ([[02-foundations/tools/linux-shell|12.1 §11]]).
- $t_{\text{inf}}$ — **inference**, the forward pass itself. This is the only term most papers report.
- $t_{\text{dec}}$ — **decoding and IPC** (inter-process communication, the hand-off between two programs on one computer), turning a network output into a command message and delivering it.
- $T_{\text{ctrl}}$ — **actuation**, one controller period before the command is applied.

**Where the table's 70 ms sits in this sum.** The table above and P6's budget both start at the exposure midpoint, so they leave out the first term. Two rows are one term each, $t_{\text{exp}}=15$ and $t_{\text{inf}}=40\,\mathrm{ms}$. "Communication", $10\,\mathrm{ms}$, is $t_{\text{tx}}+t_{\text{dec}}$, because in the picture's cycle the image goes straight to inference and what travels afterwards is the goal, from the vision node to the controller (published at $55\,\mathrm{ms}$, consumed by the tick at $65$). "Command processing", $5\,\mathrm{ms}$, is $T_{\text{ctrl}}$, P6's control period. So a budget counted from mid-exposure is $L-\tfrac12T_{\text{cam}}$ — at P6's $50\,\mathrm{Hz}$, $70\,\mathrm{ms}$ of budget is an $L$ of $80\,\mathrm{ms}$ on average and $90\,\mathrm{ms}$ at worst. Two later pages use the letter differently: [[04-robotics/capstone-panel-contact|26. Capstone]] writes $L$ for this budget itself, and the staleness ledger of [[04-robotics/ros2/simulation-and-control|25.7]] for the shorter span from mid-exposure to the goal's arrival at the controller, adding the periods after it.

**Non-example:** adding the *rates* is not a budget. "A 30 Hz camera, a 25 Hz policy and a 500 Hz controller" does not reduce to any latency at all, because rates do not add, and the fastest stage in a series chain still contributes its own fixed delay. Two systems with identical rates can differ by 50 ms in $L$ purely in queueing and timestamp policy.

#### Deadlines and jitter

**Deadline and jitter, defined.** A periodic task with period $T$ is **released** at $r_k=r_0+kT$ and finishes at $f_k$, so its **response time** is $R_k=f_k-r_k$. Its **deadline** $D$ is the time after release by which it must finish, usually $D=T$, and a **deadline miss** is any instance with $R_k>D$. The strength of the deadline is a separate claim from its value, and there are three:

- **hard** — a single miss is a system failure (the loop holding a stiff contact, a brake release);
- **firm** — a late result is worthless and is discarded, but discarding it is survivable (a dropped perception frame);
- **soft** — a late result is degraded but still worth having (a map update, an operator display).

**Jitter** is the *spread* of a timing quantity across instances, never its mean, and it is reported peak-to-peak:

$$J=\max_k R_k-\min_k R_k$$

since what a deadline argument needs is the extreme and not the centre — a standard deviation hides exactly the tail that misses. The Worked case's step 3 applies both definitions to P6's control loop: $3.6\,\mathrm{ms}$ of jitter, zero misses, $0.2\,\mathrm{ms}$ of margin. Release jitter and output jitter are defined the same way on the other two instants. Jitter survives only if the log keeps it: a tick time printed with `%.3f` rounds a $120\,\mu\mathrm{s}$ lateness away, as step 5 of the Worked case of [[02-foundations/tools/config-data-formats|12.4 Config and Data Formats]] shows; and the rules that keep a C++ tick's worst case inside its period are [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code §9]].

#### The budget to scale, and one visuomotor loop added up

P6's own budget was worked in the Worked case. Budgets tighten by more than an order of magnitude when the loop renders stiff contact: a haptic servo must close in about $1\,\mathrm{ms}$ with bounded jitter, against this page's $70\,\mathrm{ms}$ observation-to-action budget, so the millisecond is the unit rather than the frame ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]]). The table's budget, drawn to scale:

<svg viewBox="0 0 560 190" style="max-width:100%;height:auto" role="img" aria-label="The 70 ms budget of the table drawn to scale at 5 px per ms from the exposure midpoint: exposure and readout 15, inference 40, communication 10, command 5, with P6's 10 ms sampling wait drawn before its left end, outside the budget">
  <rect x="110.0" y="58" width="50.0" height="30" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <text x="104.0" y="67" font-size="10.5" fill="currentColor" text-anchor="end">sampling wait</text>
  <text x="104.0" y="80" font-size="10.5" fill="currentColor" text-anchor="end">½T<tspan dy="3" font-size="10">cam</tspan><tspan dy="-3" dx="2">= 10 ms</tspan></text>
  <text x="104.0" y="93" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.75">not in the budget</text>
  <rect x="160.0" y="58" width="75.0" height="30" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.1"/>
  <text x="197.5" y="78" font-size="11" fill="currentColor" text-anchor="middle">15</text>
  <rect x="235.0" y="58" width="200.0" height="30" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.1"/>
  <text x="335.0" y="78" font-size="11" fill="currentColor" text-anchor="middle">40</text>
  <rect x="435.0" y="58" width="50.0" height="30" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.1"/>
  <text x="460.0" y="78" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <rect x="485.0" y="58" width="25.0" height="30" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.1"/>
  <text x="497.5" y="78" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <text x="197.5" y="102" font-size="10.5" fill="currentColor" text-anchor="middle">exposure / readout</text>
  <text x="335.0" y="102" font-size="10.5" fill="currentColor" text-anchor="middle">inference</text>
  <line x1="460.0" y1="88" x2="460.0" y2="108" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="460.0" y="119" font-size="10.5" fill="currentColor" text-anchor="middle">comms</text>
  <line x1="497.5" y1="88" x2="507.5" y2="108" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="503.5" y="119" font-size="10.5" fill="currentColor" text-anchor="start">command</text>
  <line x1="160.0" y1="38" x2="160.0" y2="58" stroke="currentColor" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="3 3"/>
  <line x1="510.0" y1="38" x2="510.0" y2="58" stroke="currentColor" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="3 3"/>
  <text x="160.0" y="33" font-size="11" fill="currentColor" text-anchor="middle">exposure midpoint</text>
  <text x="510.0" y="33" font-size="11" fill="currentColor" text-anchor="end">command takes effect</text>
  <path d="M160.0 130 v6 H510.0 v-6" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="335.0" y="151" font-size="11" fill="currentColor" text-anchor="middle">70 ms budget = L − ½T<tspan dy="3" font-size="10">cam</tspan></text>
  <text x="335.0" y="167" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">at 1 m/s the robot travels 7 cm inside the budget</text>
</svg>

The table's $70\,\mathrm{ms}$ drawn to scale from the exposure midpoint to the command taking effect: exposure and readout $15$, inference $40$, communication $10$ and command processing $5\,\mathrm{ms}$, with P6's sampling wait $\tfrac12T_{\text{cam}}=10\,\mathrm{ms}$ dashed before the left end because the budget does not count it. Inference is $40/70=57\%$ of the budget, and at $1\,\mathrm{m/s}$ the robot moves $7\,\mathrm{cm}$ inside it — so "we run at $30\,\mathrm{Hz}$" answers a different question from "how stale was the frame you acted on?".



> [!example] Worked example · 계산 예제
> **Adding up one loop.** Take a representative visuomotor stack: 30 Hz camera (mean sampling
> latency $\tfrac{1}{2}\times 33.3 = 16.7$ ms), exposure and readout 12 ms, transport to the GPU
> host 5 ms, policy inference 40 ms, action decoding and IPC 3 ms, and a 500 Hz joint
> controller (2 ms). Total $16.7 + 12 + 5 + 40 + 3 + 2 = \mathbf{79}$ ms.
>
> **What it costs, twice over.** As *staleness*: the end-effector moving at 0.3 m/s has
> travelled $0.3 \times 0.079 = 24$ mm by the time its own image produces an action. Against a
> $\pm 10$ mm grasp tolerance you must either slow to $0.010/0.079 = 0.13$ m/s or predict
> forward. As *dead time in a feedback loop*, a delay $T$ contributes $360 fT$ degrees of
> phase lag at a signal frequency $f$ in Hz, because a delay of $T$ seconds is the fraction $fT$ of one period.
> If the loop had 90° margin before the delay and must retain 45°, the delay may use at most 45° at the
> crossover frequency $f$: $360fT\le 45°$, so $f\le 45°/(360T)$. With $T=0.079$ s this
> gives the illustrative crossover budget $(90°-45°)/(360T)=\mathbf{1.6}$ Hz. This is not
> a universal cap: the plant and controller determine the pre-delay margin, and adding delay
> can move the crossover. [[04-robotics/control-theory-ce397|5. Control §5.5]] derives this
> conditional budget and explains when it applies.
>
> **The reading this gives you.** Halving inference time (40 → 20 ms) moves the total to 59 ms
> and, under the same illustrative 90°/45° assumptions, the budget to
> $45°/(360°\times0.059\,\mathrm{s})=2.1$ Hz — real, but a 1.3× gain,
> not the 2× the headline suggests, because inference is only half the budget. It also tells you what to ask of any paper
> reporting a policy frequency: 10 Hz inference is not a 10 Hz loop, and the difference is
> everything the rest of this table holds.

The $79$ ms is a mean; the Deeper note below redoes it with the sampling term at its worst.

> [!note]- Deeper · 더 깊이
> **Mean versus worst case.** The jitter distinction of the Worked case's step 3 re-reads this total. The $79$ ms ($78.7$ ms before rounding) is the *mean* budget; replacing the sampling term $\tfrac12 T_{\text{cam}}=16.7$ ms by its worst case $T_{\text{cam}}=33.3$ ms gives $16.7+78.7=\mathbf{95.3}$ ms. That $16.7$ ms gap is jitter and not bias, so no calibration removes it: a controller tuned on the mean budget meets a disturbance that is $16.7/78.7=21\%$ staler than designed, and at $0.3$ m/s the end-effector's staleness runs from $0.3\times0.0787=24$ mm to $0.3\times0.0953=29$ mm between one frame and the next.

### 4. Coordinate frames and TF trees

*In one sentence:* every position a robot uses is written from some viewpoint at some moment, and the TF tree is the bookkeeping that gives one answer to "where is this thing, seen from there, at that time".

*If you need only one thing from this section:* a loop closure rewrites only the `map` → `odom` edge, so a goal stored in `map` jumps $30\,\mathrm{cm}$ while the robot stands still, worked in the example that ends this section.

Common frames include world, map, odom, base, sensor, end-effector, tool, and object. Every transform needs a direction and timestamp. A plausible numeric matrix in the wrong convention can create a systematic failure that learning cannot repair reliably.

**A transform, and the direction that names it.** A transform ${}^{a}T_{b}\in SE(3)$ has two readings that are the same matrix: it takes the coordinates of a point in frame $b$ to its coordinates in frame $a$, and it *is* the pose of frame $b$ expressed in frame $a$. Written with both indices, transforms chain by cancelling the inner one, and invert by transposing the rotation:

$${}^{a}T_{c}={}^{a}T_{b}\,{}^{b}T_{c},\qquad {}^{b}T_{a}=\big({}^{a}T_{b}\big)^{-1}=\begin{pmatrix}R^{\top} & -R^{\top}t\\ 0 & 1\end{pmatrix}$$

The inverse takes that form because undoing the transform must undo the rotation before it undoes the translation. **Non-example, and this is the "plausible matrix" above:** the inverse is *not* the same rotation with a negated translation. Take ${}^{a}T_{b}$ with a $90°$ yaw and $t=(1,0)$ m. The correct inverse translation is $-R^{\top}t=(0,1)$ m, while negating gives $(-1,0)$ m — identical magnitude, perfectly plausible in a log, and $1.41$ m wrong. [[02-foundations/se3-geometry|SE(3)]] supplies this algebra; a TF tree supplies the runtime bookkeeping.

**A TF tree, defined.** It is a directed graph whose nodes are frames and whose edges are timestamped parent-to-child transforms, subject to three conditions that make it a *tree*: every frame has exactly one parent; exactly one frame, the root, has none; and there are no cycles. Three consequences follow, and each is a failure mode when it is violated. There is exactly one path between any two frames, so a lookup is unambiguous and is just the composition along that path. Two publishers writing the same child frame is an error rather than a merge, because a frame with two parents is not a tree — the effect is a transform that flickers between two answers. And because every edge carries a stamp, a lookup is a query *at a time*, interpolated between the stamps that bracket it; a query outside the buffer fails rather than extrapolating, which is the correct behaviour and a common source of "it works in the bag but not live" (a *bag* is ROS's recorded log of the message streams, replayed later; §5).

**The conventions worth memorising.** REP-103 (a ROS Enhancement Proposal, one of the project's written conventions) fixes axes and units: right-handed, $x$ forward, $y$ left, $z$ up on a robot body, ENU (east–north–up) in geographic frames, SI units and radians. REP-105 fixes the mobile-robot chain, `map` → `odom` → `base_link` → sensor frames, each the parent of the next. `odom` is continuous but drifts without bound; `map` is drift-free but discontinuous. The reason for *that* ordering is the one-parent rule: `base_link` already has `odom` as its parent and cannot have a second, so a localisation system may not re-parent it and publishes the `map` → `odom` edge instead, folding the entire global correction into that single transform. Every "the map jumped" story is that edge being rewritten.

**The panel cell's tree.** In the cell of [[04-robotics/capstone-panel-contact|26. Capstone]], P2 — the catalog's two-link arm ([[02-foundations/lab-plants|0.6]]) — stands on a fixed base and reads the panel's range with a sensor on its tool, P5, the catalog's range sensor. Four edges, each parent → child: `world` → `base_link`, the arm's mounting, static; `base_link` → `tool`, forward kinematics, republished every tick and stamped with the joint reading it came from; `tool` → `range_sensor`, the sensor's mounting on the tool, static, from calibration; and `range_sensor` → `panel`, the range the sensor read — fused to $11.6$ cm in 26's step 1 — stamped when the reading was taken, with the arm at home. The panel in the arm's frame is the lookup `base_link` → `panel`, three edges composed down the tree, and it must use `base_link` → `tool` **at the reading's stamp**: composed with the tool's pose after the arm has moved off home, the same $11.6$ cm range puts the panel wherever the tool now points.

For example, suppose the base sits at $(1.0, 2.0)$ m in odom and a goal is stored in map at $(5.0, 2.0)$ m. While `map` → `odom` is the identity the goal is at odom $(5.0, 2.0)$, $4.00$ m ahead. A loop closure now corrects the global estimate by 30 cm, which is published as a `map` → `odom` translation of $(0.30, 0)$ m, so the same stored goal is at odom $(4.70, 2.0)$ and is $3.70$ m ahead: the goal moved 30 cm while the robot did not move at all. A path held in odom did not move, which is the whole reason a local controller is fed odom. The problem is not necessarily a bad transform matrix; it can be combining correct transforms from incompatible times. **The reading this gives you.** Trace each goal, observation, and command through its frame and timestamp. State where global correction is allowed to change a reference and how the downstream controller handles that change.

### 5. Middleware literacy

Middleware carries every message between the blocks of §1, and its settings are part of the timing: one line of configuration moves the oldest goal a stalled controller is handed from $0$ to $180\,\mathrm{ms}$ old (the queue paragraph below). The vocabulary first, then P6's traffic on it.

| Concept | Role |
|---|---|
| node | running component |
| topic/message | asynchronous data stream and schema |
| service | request/response operation |
| action | longer operation with feedback/cancellation |
| TF | time-indexed frame transforms |
| bag/log | recorded streams for replay and analysis |
| QoS | delivery, durability, reliability, and queue policy |

ROS is one implementation ecosystem, not the system architecture itself. “Runs on ROS” says little about latency, determinism, safety, or deployment quality.

**Each row is a promise about time as well as data.** Put P6's traffic on the table and the row is forced. The $50\,\mathrm{Hz}$ goal is a *topic*, because each goal replaces the one $20\,\mathrm{ms}$ before it, so a lost one is repaired by the next. "Drive the cart to $p=0.5\,\mathrm{m}$" is an *action*, because it runs for seconds, reports progress, and must be cancellable when the goal changes. Setting a controller gain is a *service* or parameter call, one request and one reply, because it must not be lost without anyone noticing. And the cart's frames are *TF*, because a goal is useless without the frame and the stamp it was measured in (§4).

**The queue is a term in §3's budget.** The middleware buffers messages under a history depth $N$ ([[04-robotics/ros2/qos-executors-time|25.5 Quality of Service §2]]) — a bounded buffer between a producer and a consumer, with a rule for what to drop when it is full, exactly as between two threads ([[02-foundations/tools/concurrency|12.8 Concurrency §6]]); DDS, the middleware under ROS 2, is [[02-foundations/tools/computer-networks|12.5 Computer Networks §8]]. Under the default profile, keep-last $10$, a controller that stalls for $200\,\mathrm{ms}$ resumes on a queue of goals and is handed the oldest first, $(10-1)\times20=180\,\mathrm{ms}$ after it was published — and older still since its exposure midpoint, so "$110\,\mathrm{ms}$ over the $70\,\mathrm{ms}$ budget" is a lower bound — and it reaches the newest goal only at its tenth callback. Nothing in the algorithm changed; one line of configuration did. That is why "runs on ROS" is not a latency claim: the same node graph has a different worst-case goal age under a different profile.

### 6. Behavior orchestration and task execution

*In one sentence:* something has to decide which planner or controller runs right now and what happens when it fails, and a behavior tree makes that decision again at every tick from three possible answers: done, failed, or still working.

*If you need only one thing from this section:* the three-valued tick (Success, Failure, Running) and what it buys in the example tree below, where `batteryOK` turning false mid-drive halts `FollowPath` on the very next tick and enters recovery.

#### The execution layer and its vocabulary

Between the task command and the planner/controller usually sits an **execution layer**
— a finite-state machine (FSM), behavior tree, or task executive — that decides *which*
planner, policy, or controller runs now, and what happens when it fails.

```mermaid
flowchart TD
    T["Task command"] --> X["State machine / behavior tree / executive"]
    X --> PL["Planner or learned policy"] --> CT["Controller"]
    CT --> X
```

Core vocabulary: **states/behaviors** with **transitions** fired by **guards**
(conditions); **preconditions** checked before an action and **postconditions** verified
after; **timeouts** and **retries**; **fallbacks** and **recovery behaviors** when a
step fails; **action servers** with feedback and **cancellation**. A worked skeleton:

```
Idle → Detect object → Plan grasp → Execute → Verify
                                        ├─ success → Place
                                        └─ failure → Replan / Request help / Safe stop
```

Behavior trees compose these modularly and are common in field systems; FSMs are simpler
but tangle as states multiply.

#### Behavior trees, defined by what a tick returns

**Behavior tree, defined by what a tick returns.** A behavior tree is a rooted tree whose leaves are **actions** (do something) and **conditions** (test something), and whose interior nodes are **control-flow nodes**. It is executed by a **tick**: a signal injected at the root at a fixed rate and propagated to children according to each node's type. Every ticked node returns exactly one of three statuses, and that three-valued return is the entire design:

$$\text{tick}(n)\in\{\,\textsf{Success},\ \textsf{Failure},\ \textsf{Running}\,\}$$

**Running** is the status an FSM has no equivalent for, since it means "started, not finished, tick me again": a long action therefore does not block the tree, and the status propagates upward, because a node with a Running child is itself Running. The three node families are each defined by what they return:

- **Sequence** — ticks its children left to right. Returns **Failure** at the first child that fails, **Running** at the first that is Running, and **Success** only when every child has succeeded. It is a logical **AND** over its children, and it is how a precondition is written: put the condition first, and the action after it never runs while the condition is false.
- **Fallback** (also called **selector**) — ticks left to right and returns **Success** at the first child that succeeds, **Running** at the first that is Running, and **Failure** only when every child has failed. It is a logical **OR**, and it is the recovery construct, since the children after the first are the alternatives tried in order.
- **Decorator** — has **exactly one child**, and transforms either the child's returned status or whether the child is ticked at all. `Inverter` swaps Success and Failure; `RetryUntilSuccessful(n)` re-ticks a failing child up to $n$ times; `Timeout(ms)` fails a child that runs too long; `RateController(hz)` ticks its child only at the given rate and repeats the last status in between. The one-child rule is exactly what separates a decorator from a control-flow node.

#### The tick contract, one tree, and what a tree is not

**The tick contract** is the part that gets skipped and then produces bugs. Three clauses: a tick re-enters from the **root** every cycle, so conditions are re-evaluated continuously and an action that is already Running is abandoned the moment an earlier sibling's condition turns false — that reactivity is what a tree buys over a chain of calls. A node that was Running and is no longer on the ticked path must therefore be explicitly **halted**, so every action node owes a halt implementation as well as a tick. And status is *returned*, never stored as a transition, because there are no edges between siblings at all.

*Example.* `Fallback[ Sequence[ batteryOK, Sequence[ ComputePath, FollowPath ] ], Sequence[ ClearCostmaps, Spin ] ]`. The robot navigates while the battery holds; if either navigation step returns Failure the fallback moves on to the recovery branch; and if `batteryOK` goes false mid-drive, the very next tick from the root fails the inner sequence at its condition, halts `FollowPath` without waiting for it to finish, and enters recovery. [[04-robotics/ros2/navigation-nav2|25.9 Nav2 §2]] reads one production tree, including the composite variants (`PipelineSequence`, `RecoveryNode`) and the 1 Hz replanning decorator.

<svg viewBox="0 0 560 394" style="max-width:100%;height:auto" role="img" aria-label="The example behavior tree of section 6 drawn at two consecutive ticks from the root, each node marked with the status it returns: at tick k FollowPath is Running and Running propagates to the root; at tick k+1 batteryOK fails, the navigation sequence fails, FollowPath is halted and the recovery branch runs">
  <text x="12" y="26" font-size="12" font-weight="600" fill="currentColor">tick k: the battery holds, FollowPath is still driving</text>
  <line x1="280" y1="66" x2="150" y2="80" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="280" y1="66" x2="440" y2="80" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="150" y1="102" x2="70" y2="116" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="150" y1="102" x2="222" y2="116" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="222" y1="138" x2="164" y2="152" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="222" y1="138" x2="282" y2="152" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="440" y1="102" x2="386" y2="116" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="440" y1="102" x2="498" y2="116" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <rect x="230.0" y="44" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="236.0" y="59" font-size="11" fill="currentColor" fill-opacity="1">? Fallback</text>
  <rect x="311.0" y="47" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="319.0" y="59" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="100.0" y="80" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="106.0" y="95" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="181.0" y="83" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="189.0" y="95" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="390.0" y="80" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="396.0" y="95" font-size="11" fill="currentColor" fill-opacity="0.5">→ Sequence</text>
  <rect x="471.0" y="83" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="479.0" y="95" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="20.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="26.0" y="131" font-size="11" fill="currentColor" fill-opacity="1">batteryOK</text>
  <rect x="101.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="109.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">S</text>
  <rect x="172.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="178.0" y="131" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="253.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="261.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="336.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="339.0" y="131" font-size="11" fill="currentColor" fill-opacity="0.5">ClearCostmaps</text>
  <rect x="417.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="425.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="448.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="454.0" y="131" font-size="11" fill="currentColor" fill-opacity="0.5">Spin</text>
  <rect x="529.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="537.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="114.0" y="152" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="120.0" y="167" font-size="11" fill="currentColor" fill-opacity="1">ComputePath</text>
  <rect x="195.0" y="155" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="203.0" y="167" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">S</text>
  <rect x="232.0" y="152" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="238.0" y="167" font-size="11" fill="currentColor" fill-opacity="1">FollowPath</text>
  <rect x="313.0" y="155" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="321.0" y="167" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <text x="442" y="168" font-size="10.5" fill="currentColor" fill-opacity="0.7" text-anchor="middle">not ticked</text>
  <line x1="8" y1="188" x2="552" y2="188" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="12" y="204" font-size="12" font-weight="600" fill="currentColor">tick k+1: batteryOK turns false</text>
  <line x1="280" y1="244" x2="150" y2="258" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="280" y1="244" x2="440" y2="258" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="150" y1="280" x2="70" y2="294" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="150" y1="280" x2="222" y2="294" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="222" y1="316" x2="164" y2="330" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="222" y1="316" x2="282" y2="330" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="440" y1="280" x2="386" y2="294" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="440" y1="280" x2="498" y2="294" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <rect x="230.0" y="222" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="236.0" y="237" font-size="11" fill="currentColor" fill-opacity="1">? Fallback</text>
  <rect x="311.0" y="225" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="319.0" y="237" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="100.0" y="258" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="106.0" y="273" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="181.0" y="261" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="189.0" y="273" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">F</text>
  <rect x="390.0" y="258" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="396.0" y="273" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="471.0" y="261" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="479.0" y="273" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="20.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="26.0" y="309" font-size="11" fill="currentColor" fill-opacity="1">batteryOK</text>
  <rect x="101.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="109.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">F</text>
  <rect x="172.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="178.0" y="309" font-size="11" fill="currentColor" fill-opacity="0.5">→ Sequence</text>
  <rect x="253.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="261.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">H</text>
  <rect x="336.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="339.0" y="309" font-size="11" fill="currentColor" fill-opacity="1">ClearCostmaps</text>
  <rect x="417.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="425.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">S</text>
  <rect x="448.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="454.0" y="309" font-size="11" fill="currentColor" fill-opacity="1">Spin</text>
  <rect x="529.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="537.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="114.0" y="330" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="120.0" y="345" font-size="11" fill="currentColor" fill-opacity="0.5">ComputePath</text>
  <rect x="195.0" y="333" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="203.0" y="345" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="232.0" y="330" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="238.0" y="345" font-size="11" fill="currentColor" fill-opacity="0.5">FollowPath</text>
  <rect x="313.0" y="333" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="321.0" y="345" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">H</text>
  <text x="340.0" y="339" font-size="10.5" fill="currentColor" fill-opacity="0.8">halted: was Running,</text>
  <text x="340.0" y="352" font-size="10.5" fill="currentColor" fill-opacity="0.8">now off the ticked path</text>
  <text x="342" y="230" font-size="10.5" fill="currentColor" fill-opacity="0.8">the fallback moves on</text>
  <text x="342" y="242" font-size="10.5" fill="currentColor" fill-opacity="0.8">to the recovery branch</text>
  <text x="12" y="368" font-size="11" fill="currentColor">S Success · F Failure · R Running · H halted · – not ticked</text>
  <text x="12" y="384" font-size="11" fill="currentColor" fill-opacity="0.8">Solid edges carry this tick; dashed edges were not ticked.</text>
</svg>

The example tree at two consecutive ticks from the root, each node marked with the status it returns. At tick $k$ the battery holds: `batteryOK` and `ComputePath` return Success, `FollowPath` returns Running, and Running propagates up through both sequences to the root, while the recovery branch is not ticked at all. At tick $k+1$ `batteryOK` returns Failure, so the navigation sequence fails at its first child without ticking the path sequence, the Running `FollowPath` and its sequence are halted, and the fallback ticks the recovery branch, where `ClearCostmaps` succeeds and `Spin` runs.

**Non-example.** A tree is not an if-then-else chain evaluated once at the start of the task, and a sequence is not a program's `;` — read it that way and the re-ticking looks like wasted work instead of the mechanism. Nor is it a state machine with nicer syntax: an FSM keeps its control flow in transition edges, of which there can be up to $n(n-1)$, and every recovery rule must be duplicated on each state it can fire from, whereas a tree's control flow is only sibling order plus a three-valued return. That is what makes recovery **scoped** — the nearest enclosing fallback decides who recovers, so a planner failure need not invoke the whole system's last resort.

*Why it matters when reading.* When a paper says the robot "recovered" or "retried", a fallback node did it and not the policy: check who detects failure, who chooses the response, and what counts as terminal.

### 6.5 Architecture lineages and formal task specifications

*In one sentence:* robot software settled on three layers that run at three speeds, and temporal logic is a way to write down what those layers must always, eventually, or never do, precisely enough for a computer to check a design or to build a controller from the rule.

*If you need only one thing from this section:* a specification can be satisfiable and still not realizable; the panel-delivery formula below is met by a fault-free run that delivers A and then B, yet no controller can guarantee it, because the zone sensor may fail before the first delivery.

The execution layer of §6 is the middle tier of a design robotics reached after two extremes failed, and temporal logic states what that design must guarantee precisely enough to check or to generate it.

#### Three architecture lineages

- **Sense–plan–act** (the Shakey-era deliberative pipeline): sensing builds a world model, a planner reasons on it, a controller executes. The planner is a bottleneck the controller waits on, and the controller never sees sensors directly, so the robot cannot react while it thinks.
- **Subsumption** (Brooks 1986): parallel reactive behaviours, each wiring sensors to actuators; a higher layer *suppresses* a lower one's input or *inhibits* its output. No world model, so reaction is fast; no long-horizon planning either.
- **Three-layer** (Gat 1998): a fast *controller*, a *sequencer* (executive) that picks the active behaviour and handles failure, and a slow *deliberator*. Each runs at its own rate, and only the deliberator may be slow.

| Tier | Rate | ROS 2 realisation |
|---|---|---|
| controller | fastest | `ros2_control` controller manager, `update_rate` default 100 Hz ([[04-robotics/ros2/simulation-and-control\|ROS 2 control]]) |
| sequencer | medium | behaviour tree; Nav2's `bt_navigator` re-ticks the planner once per second by default ([[04-robotics/ros2/navigation-nav2\|Nav2 §2]]) |
| deliberator | per task | task planner or TAMP ([[04-robotics/planning-decision-making\|4 §7]]), or a VLA/LLM planner emitting goals |

Tiers talk through §5's split: topics carry data, services and actions carry commands with a reply. **The reading this gives you.** "The LLM plans" replaces the deliberator only; recovery still lives in the sequencer and stability in the controller.

#### Temporal logic, from propositions up

**Temporal logic.** A **proposition** is a named fact that is true or false at each step, such as $\mathit{near}$ or $\mathit{stop}$, and the Boolean connectives combine propositions within one step: $\neg\varphi$ (not), $\varphi\wedge\psi$ (and), $\varphi\vee\psi$ (or), and $\varphi\rightarrow\psi$ (if $\varphi$ then $\psi$), which is false only when $\varphi$ holds and $\psi$ does not, so it is true *vacuously* at every step where $\varphi$ is false. Temporal logic is logic about sequences over time: a formula is judged true or false of a whole run — a list of steps, each recording which propositions hold — rather than of one moment. LTL (Pnueli 1977) adds four operators to Boolean propositions over discrete steps: $\mathsf{X}\,\varphi$ (next step), $\mathsf{F}\,\varphi$ (eventually), $\mathsf{G}\,\varphi$ (always), $\varphi\,\mathsf{U}\,\psi$ ($\varphi$ at every step until $\psi$, which must occur). Patterns: safety $\mathsf{G}\,\neg\mathit{collision}$; liveness $\mathsf{G}\mathsf{F}\,\mathit{atCharger}$ (from every step, a charger visit still lies ahead, so on an infinite run the robot returns infinitely often); response $\mathsf{G}(\mathit{req}\rightarrow\mathsf{F}\,\mathit{grant})$; sequencing $\mathsf{F}(a\wedge\mathsf{F}\,b)$.

#### Model checking, synthesis, and the logics robots actually use

*Model checking* asks whether every behaviour of a given design satisfies $\varphi$, and returns yes or a counterexample. *Reactive synthesis* builds a controller that satisfies $\varphi$ against every sequence of environment inputs, choosing each output from the past alone, because a real robot must act before it sees the next input.

That causality is what separates two words. $\varphi$ is *satisfiable* if some input–output run meets it, and *realizable* if one controller wins against all inputs. With environment inputs $\mathit{req},\mathit{obst}$ and output $\mathit{move}$, $\mathsf{G}(\mathit{req}\rightarrow\mathsf{X}\,\mathit{move})\wedge\mathsf{G}(\mathit{obst}\rightarrow\neg\mathit{move})$ is satisfiable (any obstacle-free run), but not realizable: $\mathit{req}$ at $t$ and $\mathit{obst}$ at $t+1$ leave no valid $\mathit{move}$ at $t+1$.

Synthesis for full LTL is expensive, so robotics synthesizes controllers from a restricted fragment, GR(1), and judges continuous signals with signal temporal logic; the Deeper note says why and how.

> [!note]- Deeper · 더 깊이
> **Why a fragment.** Synthesis for full LTL is doubly exponential in formula size (Pnueli & Rosner 1989). Roughly, turning the formula into an automaton costs one exponential, and making that automaton deterministic, so the controller always knows which obligations are pending, costs another. So robotics uses fragments such as GR(1), *Generalized Reactivity(1)* (initial conditions, `always` step constraints, `always eventually` goals), solvable in time polynomial in the game's state space (Piterman, Pnueli & Sa'ar 2006) and applied to reactive mission and motion planning by Kress-Gazit, Fainekos & Pappas (2009).
>
> **Signal temporal logic.** For continuous signals, signal temporal logic adds time intervals and real-valued predicates, with a robustness score saying by how much a signal satisfies or violates the formula (Maler & Nickovic 2004; Donzé & Maler 2010). For "distance always above 2 m" the score is the worst margin: a run whose closest approach is 2.5 m scores $+0.5$ m, and one that dips to 1.8 m scores $-0.2$ m.

#### Writing one specification, and checking it on a log

**Writing a spec.** "Always keep 2 m from any worker; eventually deliver panel A then panel B; if the zone sensor fails, stop." Let $\mathit{near}$ = within 2 m of a worker (from perception), $\mathit{fail}$ = zone-sensor fault, $\mathit{dA},\mathit{dB}$ = panel delivered, $\mathit{stop}$ = zero velocity commanded. Reading "stop" as "by the next step, and stay stopped":

$$\varphi = \mathsf{G}\,\neg\mathit{near} \;\wedge\; \mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB}) \;\wedge\; \mathsf{G}(\mathit{fail}\rightarrow\mathsf{X}\,\mathsf{G}\,\mathit{stop})$$

This is satisfiable — any fault-free run that keeps clear of workers and delivers A then B meets it — but not realizable as written, and one environment strategy shows why. The environment controls $\mathit{fail}$, so let it raise $\mathit{fail}$ at $t_0$, before anything has been delivered. The third conjunct then demands $\mathit{stop}$ at every step from $t_1$ on; a robot commanded to zero velocity delivers nothing; so $\mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB})$ is false on that run whatever the controller chooses. One input sequence that defeats every controller proves the formula not realizable, the same argument as the $\mathit{req}/\mathit{obst}$ example above. So weaken the liveness part to $\mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB})\vee\mathsf{F}\,\mathit{fail}$, which that strategy satisfies, or state as an assumption that no fault occurs before the deliveries; the log below shows what the weakening lets through, and the conjunct that closes it.

> [!example] Worked example · 계산 예제
> **Assumption: finite-trace semantics.** The logged steps $t_0,\dots,t_5$ are the whole run; $\mathsf{G}$ and $\mathsf{F}$ range over the remaining steps, and $\mathsf{X}$ at the last step is false. Trace: $t_0\,\{\}$, $t_1\,\{\mathit{dB}\}$, $t_2\,\{\mathit{dA}\}$, $t_3\,\{\mathit{fail}\}$, $t_4\,\{\mathit{stop}\}$, $t_5\,\{\mathit{stop}\}$.
>
> **$\mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB})$ is false.** $\mathit{dA}$ holds only at $t_2$, and the only $\mathit{dB}$ is at $t_1$, before it. The unordered $\mathsf{F}\,\mathit{dA}\wedge\mathsf{F}\,\mathit{dB}$ is true; only the nested form sees that B went first.
>
> **$\mathsf{G}(\mathit{fail}\rightarrow\mathsf{X}\,\mathsf{G}\,\mathit{stop})$ is true.** The implication is vacuous except at $t_3$, where it needs $\mathit{stop}$ at $t_4$ and $t_5$, which holds. The same-step $\mathsf{G}(\mathit{fail}\rightarrow\mathit{stop})$ is false at $t_3$: one step of reaction is a requirement decision, not notation.
>
> **The reading this gives you.** With $\mathsf{G}\,\neg\mathit{near}$ true, the full $\varphi$ is false and the weakened spec is true — but not because this run is a correct fault stop. B was delivered at $t_1$, before A at $t_2$, and the fault came only at $t_3$: the disjunct $\mathsf{F}\,\mathit{fail}$ excuses an order violation that happened before any fault. The weakening needs a conjunct a later fault cannot excuse, "no B until A", written with the *weak until* $\neg\mathit{dB}\ \mathsf{W}\ \mathit{dA}=\mathsf{G}\,\neg\mathit{dB}\vee(\neg\mathit{dB}\ \mathsf{U}\ \mathit{dA})$, which also holds if B never comes. It is false on this log and true on a fault-first log $\{\},\{\mathit{fail}\},\{\mathit{stop}\},\{\mathit{stop}\}$, and it keeps the weakened spec realizable, because the robot alone decides $\mathit{dA}$ and $\mathit{dB}$ and can always hold B back.

```python
def ev(f, tr, i=0):  # LTL on a finite trace; X at the last step is false
    op, a = f[0], f[1:]
    if op == 'ap':  return a[0] in tr[i]
    if op == 'not': return not ev(a[0], tr, i)
    if op == 'and': return ev(a[0], tr, i) and ev(a[1], tr, i)
    if op == 'or':  return ev(a[0], tr, i) or ev(a[1], tr, i)
    if op == 'imp': return not ev(a[0], tr, i) or ev(a[1], tr, i)
    if op == 'X':   return i + 1 < len(tr) and ev(a[0], tr, i + 1)
    if op == 'F':   return any(ev(a[0], tr, j) for j in range(i, len(tr)))
    if op == 'G':   return all(ev(a[0], tr, j) for j in range(i, len(tr)))
    if op == 'U':   return any(ev(a[1], tr, j) and all(ev(a[0], tr, k) for k in range(i, j))
                               for j in range(i, len(tr)))

dA, dB, fail, stop, near = (('ap', s) for s in ['dA', 'dB', 'fail', 'stop', 'near'])
tr = [set(), {'dB'}, {'dA'}, {'fail'}, {'stop'}, {'stop'}]
seq = ('F', ('and', dA, ('F', dB)))
react = ('G', ('imp', fail, ('X', ('G', stop))))
print(ev(seq, tr), ev(('and', ('F', dA), ('F', dB)), tr))         # False True
print(ev(react, tr), ev(('G', ('imp', fail, stop)), tr))           # True False
safe = ('G', ('not', near))
print(ev(('and', safe, ('and', seq, react)), tr),                  # False
      ev(('and', safe, ('and', ('or', seq, ('F', fail)), react)), tr))  # True
order = ('or', ('G', ('not', dB)), ('U', ('not', dB), dA))         # no B until A: the weak until
print(ev(order, tr), ev(order, [set(), {'fail'}, {'stop'}, {'stop'}]))  # False True
```

**What to check in papers.** *Who controls each proposition*: if workers can walk toward the robot, $\mathsf{G}\,\neg\mathit{near}$ needs an assumption about human motion or must become a response; the distance itself is a standards question ([[04-robotics/hri-safety|HRI & Safety §6]]). *Grounding*: the guarantee is about the abstraction, only as good as the perception that sets $\mathit{near}$ and the controller that realises $\mathit{stop}$. *Semantics*: infinite-trace LTL and finite-trace evaluation of a log can disagree, most visibly on $\mathsf{X}$ and $\mathsf{G}$ at the end of the run.

### 7. Reliability and safety mechanisms

A dead node can leave a live command: downstream hardware may keep executing the last setpoint it accepted, so silence is not a stop. The mechanisms below exist to turn silence, staleness and faults into decisions.

- Watchdog: detects missing or unhealthy updates.
- Heartbeat: periodic liveness signal.
- Timeout: declares data or command stale.
- Graceful degradation: continues with reduced capability.
- Fail-safe state: moves toward a condition intended to reduce risk.
- Emergency stop: independent means to halt hazardous motion — one that cuts power rather than asking for it, which is why it is wired and not sent as a message ([[02-foundations/basic-circuits-electronics|0.6.2 §11]]).

Best-effort average timing is different from deterministic deadline behavior. Safety claims require system-level evidence, not merely a stable policy output.

For example, if a planner stops publishing while the actuator continues its previous motion, absence of new commands is not a stop command. A heartbeat can reveal liveness, but freshness and validity of the actual control data need their own checks. ROS 2 can make the middleware watch for both: a subscription's *deadline* policy declares the longest gap between messages it accepts, and a publisher's *liveliness* with its lease duration how long it may stay quiet before it counts as lost ([[04-robotics/ros2/qos-executors-time|25.5 §2]]). **The reading this gives you.** Ask who detects silence, who owns the timeout, and what command the hardware executes afterward. Test resumption as well as stopping; an old queued command should not silently regain authority when the node returns.

### 8. Calibration, configuration, and reproducibility

A random seed does not reproduce an experiment whose calibration or hardware differs: P6's controller set for $2000$ instead of $2048$ counts/m is $24\,\mathrm{mm}$ wrong after one metre on every run, and no seed reveals it (worked below). So record intrinsic/extrinsic calibration, zero offsets, units, frame conventions, controller gains, firmware, model weights, software commit, hardware revision, and runtime configuration.

**Worked: plant P6.** Calibration numbers enter every later number, so they are recorded with the run. P6's encoder is $2048$ counts/m. A controller configured with a nominal $2000$ counts/m converts each count to $0.500\,\mathrm{mm}$ instead of $0.488\,\mathrm{mm}$, so after the cart has truly travelled $1\,\mathrm{m}$, $2048$ counts, it believes it is at $2048/2000=1.024\,\mathrm{m}$. That is $24\,\mathrm{mm}$, or $49$ counts, of error that grows with distance and repeats exactly on every run, and no number of seeds reveals it, because nothing random produced it. A clock offset is the same kind of error in time: if the vision node's clock runs $10\,\mathrm{ms}$ ahead of the controller's, every goal is $10\,\mathrm{ms}$ older than its stamp says, a hidden term in §3's budget worth $1\,\mathrm{mm}$ at $0.10\,\mathrm{m/s}$. How each calibration is estimated, the temporal one included, is [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration §5]], and the list a lab must keep so that a run can be traced back to the hardware state it used is [[06-research-practice/experimental-design-reproducibility|Experimental Design §7]].

### 9. Simulation and staged deployment

Success in simulation is not evidence of deployment: each rung of the ladder below tests something the rung before it could not, and a claim is only as strong as the highest rung it reached.

| Stage | Purpose |
|---|---|
| simulation | fast and controlled development |
| software-in-the-loop | exercise software interfaces around simulated plant/sensors |
| hardware-in-the-loop | include physical compute/controllers or hardware interfaces |
| shadow mode | observe live inputs without commanding the robot |
| staged deployment | increase speed, autonomy, and environment difficulty gradually |

**The ladder on the panel task.** Take the press of [[04-robotics/capstone-panel-contact|26. Capstone]], a 10 N press on a panel whose position is estimated. *Simulation* is 26's lab: the whole loop, with the true face known to the code. *Software-in-the-loop* runs the same controller code against that simulated arm through the real middleware, so §5's queues and §3's budget are real while the physics is not. *Hardware-in-the-loop* moves the $1\,\mathrm{ms}$ controller onto the robot's own computer and drives the arm with no panel in the cell. *Shadow mode* puts the panel back but sends no press: the planner and the range estimate run live, and each run logs the stop point it would have commanded — $1.161$ m in 26's worked case — beside the face position measured by hand, which shows the estimate's error before any force depends on it. *Staged deployment* then presses at a reduced force and approach speed and raises them only while the logged peak forces stay inside the limit.

For a worked instance of this ladder on a force-producing device — bring-up in safe layers,
then a debugging order that separates numerical instability from mechanical resonance from a
friction limit cycle — see
[[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability §6]].

A [[05-construction-robotics/digital-twin-workflows|digital twin]] (a model of a specific real site or machine, kept updated from it) is not automatically a validated predictor. Ask what is synchronized, calibrated, and experimentally checked. [[05-construction-robotics/sim-to-real|Domain randomization]] (training across randomly varied simulator parameters so the real world looks like one more sample) covers only the factors and ranges that were randomized.

### 10. Failure taxonomy

The event you see is often not the failure that caused it: a collision at $t=12.4$ s can start in a pose stream that stopped refreshing at $t=10.3$ s. Separate sensor, estimation, planning, policy, control, communication, compute, mechanical, operator, and environment failures. A collision alone can originate from stale sensing, wrong localization, infeasible planning, poor tracking, or actuator saturation. The worked case of [[06-research-practice/failure-analysis-system-evaluation|3. Failure Analysis & System Evaluation]] applies this separation to a whole log, F1 — six failures in 200 hours of a test rig, each with one initiating category and its contributing faults and outcome kept beside it.

In the collision above, accurate tracking of the wrong path that the stale poses produced is evidence against a tracking-error diagnosis. The complete hypothetical investigation is in [[06-research-practice/failure-analysis-system-evaluation|Failure Analysis §7]]. **The reading this gives you.** Record the earliest observed contract violation separately from the downstream outcome. A missing freshness check can contribute to propagation even after the initiating estimator defect is found, so the fix may need to cross a subsystem boundary.

### 11. Resource constraints

A parameter count alone does not say whether a policy fits a robot's clock: a 3-billion-parameter policy on a Jetson Thor needs $22\,\mathrm{ms}$ just to read its weights once, longer than P6's $20\,\mathrm{ms}$ vision period (worked below). Onboard/offboard compute changes latency, network dependence, power, thermal limits, privacy, and failure modes. Report compute, memory, bandwidth, battery/power, thermal throttling, payload, and real-time load—not model parameter count alone.

**Worked: a policy on P6's clock.** A parameter count sets an inference floor only together with the bytes each parameter takes and the memory bandwidth, because at batch size one a dense model reads every weight from memory at least once per forward pass and does little arithmetic with each — memory-bound, in the terms of [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing §3]]. Suppose P6's vision node were a 3-billion-parameter policy on a Jetson Thor, the robot computer of [[03-deep-learning/foundations/gpu-computing|1.4 §8]]. In bf16, 16-bit floats at $2$ bytes per weight, its weights are $6.0\,\mathrm{GB}$, and reading them once at $273\,\mathrm{GB/s}$ takes $22.0\,\mathrm{ms}$, longer than the $20\,\mathrm{ms}$ vision period before any arithmetic is done, while the same weights in NVFP4 — NVIDIA's 4-bit format with a shared scale per block of $16$, about $0.56$ byte per weight — read in $6.2\,\mathrm{ms}$ ([[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §11]]). The rate a policy actually runs at then reaches its success rate. OpenVLA's authors served their 7B policy in int8 at $1.2\,\mathrm{Hz}$ on their evaluation GPU, against the $5\,\mathrm{Hz}$ controller its training data were recorded with, and success on eight BridgeData V2 tasks fell from $71.3\%$ in bf16 to $58.1\%$; int4 ran at $3\,\mathrm{Hz}$ and matched bf16 at $71.9\%$ ([[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]). A resource report therefore gives the bytes, the hardware and the rate the loop really ran at, not the parameter count alone.

### After reading

- Draw a sense–estimate–plan–control–act pipeline.
- Identify the physical command represented by “action.”
- Distinguish rate, latency, jitter, and deadline.
- Trace a transform with correct direction and timestamp.
- Explain why ROS use or simulation success is not deployment evidence.
- Locate the execution layer (FSM/behavior tree) and what it does on failure.
- Assign a failure to its likely originating subsystem rather than its final symptom.

> [!tip] Going deeper · 더 깊이
> There is no robotics-systems textbook, and the absence is itself the field's complaint. The closest substitutes are three, and none of them is about robots exclusively: Eppner et al. (RSS 2016) on what the Amazon Picking Challenge actually taught, which is the rare paper written about integration instead of a method; the [ROS 2 concepts](https://docs.ros.org/en/rolling/Concepts.html) documentation for §5, read as a specification rather than a tutorial; and the [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/) for the vocabulary of §7 and §8, which robotics borrows without citing. Tedrake's [manipulation notes](https://manipulation.csail.mit.edu/) carry the systems chapters closest to this page's framing.

### Self-check

1. Why can a 50 Hz policy still have 200 ms latency?
2. Which records are needed to replay a field failure?
3. Why might an offboard VLA fail despite unchanged model accuracy?
4. What does hardware-in-the-loop establish—and not establish?
5. In a three-layer architecture, which tier may be slow, and in which tiers do Nav2's recovery subtree and a `ros2_control` joint controller sit?
6. On the finite trace $\{a\},\{b\},\{a\},\{\}$, is $\mathsf{G}(a\rightarrow\mathsf{X}\,b)$ true? Does a formula holding on every logged run show that it is realizable?

> [!tip]- Answers
> 1. Queues, batching, old timestamps, transport, and asynchronous stages can preserve high throughput while increasing age. 2. Synchronized raw sensors, transforms, commands, feedback, clocks, configuration, software/hardware versions, and operator events. 3. Network delay/loss, stale observations, deadline misses, or safe fallback. 4. It validates selected hardware/software interfaces and timing; it does not by itself validate real-world perception, contact, or task safety. 5. Only the deliberator may be slow; the recovery subtree is sequencer (executive) logic, and the joint controller is the controller tier. 6. False: $a$ at $t_2$ needs $b$ at $t_3$, which is empty (the step-$t_0$ obligation is met at $t_1$). No: logs are sample runs, so they show at most satisfiability; realizability needs one controller that wins against every environment input sequence, which is a synthesis question.

### Problem set · 과제

Tier A. Plant **P6** from [[02-foundations/lab-plants|0.6]], with its end-to-end budget unchanged at $70\,\mathrm{ms}$ from camera mid-exposure to applied force; each item changes the other numbers as it says. The weekend ROS 2 path is [[04-robotics/ros2/index|25]]; this page is the budget and the log.

1. **Draw.** The picture above for a cheaper $30\,\mathrm{Hz}$ camera, with the same $200\,\mathrm{Hz}$ controller and $70\,\mathrm{ms}$ budget: one cycle as a timeline — exposure midpoint, vision publish, TF lookup, controller tick, current to the motor — with the budget as a bar, both periods on the same axis, and the sampling term as a segment of its own. Overlay a goal that reaches the controller $100\,\mathrm{ms}$ after exposure.
2. **Derive.** An upgraded cart: a finer encoder, $N=4096$ counts/m; the cheaper $30\,\mathrm{Hz}$ camera; a $500\,\mathrm{Hz}$ controller; a goal that reaches the controller $150\,\mathrm{ms}$ after its exposure midpoint; and the cart at $0.25\,\mathrm{m/s}$. (a) One encoder count in millimetres. (b) Vision period and control period. (c) By how much is the budget blown, and how many control ticks ran on the stale goal? (d) How far does the cart move during that age, in millimetres and in encoder counts? (e) Which of these answers would a better estimator change?
3. **Do.** §5's queue as a sweep. A controller stalls for $200\,\mathrm{ms}$ while goals keep arriving every $20\,\mathrm{ms}$; its subscription keeps the last $N$ of them. Fill `?`, run it for $N\in\{1,2,5,10\}$, and print, per depth, the goals waiting, the age of the first goal handed over, and its excess over the budget. Then interpret: which depths hand the controller a goal older than the budget, and by how much? These ages count from publish, not from the exposure midpoint — are they upper or lower bounds on the true age?

```python
from collections import deque
PERIOD, STALL, BUDGET = 20, 200, 70          # ms: vision period, controller stall, budget
for N in (1, 2, 5, 10):                      # keep-last depth
    q = deque(maxlen=?)                      # the subscription's queue
    for t_pub in range(PERIOD, STALL + 1, PERIOD):
        q.append(t_pub)                      # each goal carries its publish time
    oldest_age = STALL - ?                   # age of the first goal handed over at resume
    over = max(0, oldest_age - ?)
    print(N, len(q), oldest_age, over)
```

> [!note]- How to draw it · 그리는 법
> - A single time axis in milliseconds: tall ticks every $33.3\,\mathrm{ms}$ above it for the vision node, short ticks every $5\,\mathrm{ms}$ below it for the controller. Both on the *same* axis is the point: two rates are two tick spacings, and nothing drawn so far is a latency.
> - The five instants, left to right: the exposure midpoint, the vision publish, the controller's TF lookup, the controller tick that consumes the goal, and current reaching the motor.
> - A bar spanning the first and the last, labelled $70\,\mathrm{ms}$, with both counts written beneath it: $2.1$ vision periods now, and still $14$ control ticks.
> - The sampling term $\tfrac12 T_{\text{cam}}=16.7\,\mathrm{ms}$ (worst case $33.3\,\mathrm{ms}$) as a segment of its own, not hidden inside the camera box: at worst it is nearly half the budget before any processing starts.
> - The stale overlay, in a lighter line from the same exposure midpoint: a $100\,\mathrm{ms}$ bar for the late goal, with its excess over the budget and the control ticks it spans written along it.
> - Under the axis, the consequence in the units the encoder speaks: how far the cart travels at $0.10\,\mathrm{m/s}$ during that age, in millimetres and in encoder counts.
> - The drawing is wrong the moment an arrow labelled "$30\,\mathrm{Hz}$" stands in for a delay, or a noise cloud appears around the goal: rate, latency and noise stay three separate marks, and no estimator on [[04-robotics/state-estimation-slam|3. State Estimation]] repairs lateness.

> [!tip]- Solutions
> 1. Vision ticks every $33.3\,\mathrm{ms}$, control every $5\,\mathrm{ms}$. The $70\,\mathrm{ms}$ bar now covers $2.1$ vision periods and still $14$ control ticks: the budget has the same length, the camera's tick spacing does not. The sampling term is $\tfrac12T_{\text{cam}}=16.7\,\mathrm{ms}$ on average and $33.3\,\mathrm{ms}$ at worst, against $10$ and $20\,\mathrm{ms}$ at $50\,\mathrm{Hz}$. The $100\,\mathrm{ms}$ goal is $30\,\mathrm{ms}$ over budget and spans $20$ control ticks; at $0.10\,\mathrm{m/s}$ the cart moved $10\,\mathrm{mm}$, $20.5$ counts. Force is still applied on a control edge, not a vision edge.
> 2. (a) $1000/4096=0.244\,\mathrm{mm}$, half P6's $0.488$. (b) $1000/30=33.3\,\mathrm{ms}$ and $1000/500=2\,\mathrm{ms}$. (c) $150-70=80\,\mathrm{ms}$ over; $150/2=75$ stale ticks — more than P6's $40$ although the goal is younger, because the faster loop runs more often on the same stale goal. (d) $0.25\times0.150=0.0375\,\mathrm{m}=37.5\,\mathrm{mm}$, and $0.0375\times4096=153.6$ counts ($37.5\,\mathrm{mm}$ over the unrounded $0.2441\,\mathrm{mm}$ count). (e) None: the finer encoder halves the size of a count, but the goal is still late, not noisy, and no estimator on [[04-robotics/state-estimation-slam|3]] repairs lateness.
> 3. `maxlen=N`, `q[0]`, `BUDGET`. It prints `1 1 0 0`, `2 2 20 0`, `5 5 80 10` and `10 10 180 110`: the oldest goal handed over is $(N-1)\times20\,\mathrm{ms}$ old, over the budget only at $N\ge5$, by $10$ and $110\,\mathrm{ms}$, and the controller reaches the newest goal only at its $N$-th callback. The ages count from publish, and every goal was already some tens of milliseconds old when it was published — $55\,\mathrm{ms}$ in the picture's illustrative cycle — so they are lower bounds: counted from the exposure midpoint, even $N=2$ could be over. The fix is a depth of $1$, or 25.5's *lifespan* policy, which drops goals older than a stated age ([[04-robotics/ros2/qos-executors-time|25.5 §2]]). "Nothing happens" on this plant is often a TF stamp or a QoS mismatch, not a wrong gain — that drill is [[04-robotics/ros2/qos-executors-time|25.5]].

### Sources

- C. Eppner, S. Höfer, R. Jonschkowski, R. Martín-Martín, A. Sieverling, V. Wall, O. Brock, "Lessons from the Amazon Picking Challenge: Four Aspects of Building Robotic Systems," *RSS 2016* (journal version: *Autonomous Robots*, 2018, DOI 10.1007/s10514-018-9761-2) — the challenge ran in 2015; the paper is 2016.

- R. A. Brooks, "A Robust Layered Control System for a Mobile Robot," *IEEE Journal of Robotics and Automation*, 2(1):14–23, 1986 — subsumption.
- N. J. Nilsson, "Shakey the Robot," SRI International Technical Note 323, 1984.
- E. Gat, "On Three-Layer Architectures," in D. Kortenkamp, R. P. Bonasso, R. Murphy (eds.), *Artificial Intelligence and Mobile Robots*, AAAI Press / MIT Press, 1998.
- A. Pnueli, "The Temporal Logic of Programs," *FOCS 1977*.
- A. Pnueli, R. Rosner, "On the Synthesis of a Reactive Module," *POPL 1989* — doubly exponential LTL synthesis.
- N. Piterman, A. Pnueli, Y. Sa'ar, "Synthesis of Reactive(1) Designs," *VMCAI 2006*, LNCS 3855 — GR(1).
- H. Kress-Gazit, G. E. Fainekos, G. J. Pappas, "Temporal-Logic-Based Reactive Mission and Motion Planning," *IEEE Transactions on Robotics*, 25(6), 2009.
- O. Maler, D. Nickovic, "Monitoring Temporal Properties of Continuous Signals," *FORMATS/FTRTFT 2004*, LNCS 3253 — signal temporal logic.
- A. Donzé, O. Maler, "Robust Satisfaction of Temporal Logic over Real-Valued Signals," *FORMATS 2010*, LNCS 6246.
- G. De Giacomo, M. Y. Vardi, "Linear Temporal Logic and Linear Dynamic Logic on Finite Traces," *IJCAI 2013* — finite-trace semantics.
- E. M. Clarke, O. Grumberg, D. Kroening, D. Peled, H. Veith, *Model Checking*, 2nd ed., MIT Press, 2018.

- [ROS 2 Concepts](https://docs.ros.org/en/rolling/Concepts.html)
- [MIT Manipulation (Tedrake) — systems chapters](https://manipulation.csail.mit.edu/)
- [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/)

## 한국어

*F군이다. [[04-robotics/state-estimation-slam|3]]·[[04-robotics/planning-decision-making|4]]·[[04-robotics/control-theory-ce397|5]]번과 신호처리·[[02-foundations/se3-geometry|SE(3)]] 위에 선다.
알고리즘이 로봇이 되기까지 더 필요한 것 — 클럭, 좌표계, 주기, 로그, 그리고 블록 사이에 사는 실패들.*

논문의 알고리즘은 센서, 클럭, 좌표계, 컴퓨터, 네트워크, 제어기, 액추에이터, 안전 로직,
로깅이 함께 작동할 때에만 로봇이 된다. 시스템 문해력은 실제로 무엇이 배포됐고, 보고된
개선이 어느 하위 시스템에서 비롯됐을 수 있는지를 읽게 해 준다.

> [!info] 깊이 목표
> 로봇을 런타임 파이프라인으로 분해한다; 행동 인터페이스, 타이밍, 좌표계, 미들웨어,
> 신뢰성, 시뮬레이션, 로깅을 해석한다; 하위 시스템 경계에서 실패를 진단한다. ROS 설치법이나
> 전자공학 튜토리얼이 아니다.

> [!note] 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]](장치 P6 — 장치(plant)는 제어공학에서 제어 대상 시스템을 부르는 말이고, P6은 카메라와 제어기가 한 시계 위에 있는 카탈로그의 카트다) · [[02-foundations/signal-processing|신호처리]] · [[02-foundations/se3-geometry|3D 기하와 SE(3)]] · [[04-robotics/state-estimation-slam|상태 추정]] · [[04-robotics/planning-decision-making|계획]] · [[04-robotics/control-theory-ce397|제어 이론]]. §6.5의 시간 논리는 논리학 강의를 가정하지 않는다. 쓰는 명제와 연결사를 그 자리에서 정의한다.

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 로봇 스택 가운데 한 층이 아니라 그 옆에서 도는 런타임 — 클럭, 좌표계, 실행 계층, 로그 — 이고 [[physical-ai-map|피지컬 AI 지도]]의 *시스템* 열에 놓이며, "*저 패널을 프레임에 설치해*"에서는 §6의 behavior tree와 §6.5의 "A를, 그다음 B를 배달하라" 명세로 *작업을 분해하는* 단계를, §8의 보정 기록과 §10의 실패 분류로 *완료를 검증하는* 단계를 맡고, 그 시간 예산은 나머지 모든 단계 밑에서 돈다. 이것이 없으면 올바른 알고리즘도 재학습으로는 고칠 수 없는 방식으로 실패한다 — 카메라 50 Hz, 제어기 200 Hz인 카탈로그의 카트 P6에서 제어기에 200 ms 묵어서 닿은 목표는 70 ms 예산을 130 ms 넘기고 카트보다 20 mm(41 카운트) 뒤처져 있으며(계산 절), 2048 대신 2000 counts/m로 설정된 제어기는 매 실행 1 m마다 24 mm씩 틀리는데 어떤 랜덤 시드도 그것을 드러내지 못한다(§8). 예산은 [[04-robotics/capstone-panel-contact|26. 캡스톤 §5]]와 그 8단계의 낡음 검사로, 좌표계는 건설 트랙의 20 kg 외장 패널 과제 S1의 좌표계 사슬([[05-construction-robotics/site-engineering|2.5 §2]], 블록 6)로, §2–§3의 주기는 [[03-deep-learning/vla/index|딥러닝 4]]가 딛고 선 예산(블록 4)으로 다시 나오고, 이 페이지 자체는 학위논문 경로의 블록 2, 로보틱스 86–89회차다([[07-research-program/index|7 §8]]). 이 페이지를 마치면 루프의 지연을 항마다 더하고, TF 트리를 변환마다 방향과 스탬프를 붙여 그리고, 실패를 끝난 곳이 아니라 시작된 하위 시스템의 이름으로 부를 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 약 넷, 로보틱스 86–89회차이고, 이야기보다 체크리스트에 가까운 페이지다. **1회차:** 이 페이지의 대상, 그림, 계산 절, 그다음 §1–§3. §3의 더 깊이 노트는 남겨 둔다. 페이지를 가리고 P6의 예산을 다시 세우며 끝낸다: $70$ ms가 비전 주기 $3.5$개, 틱 $14$개라는 것, 그것이 §3의 합에서 놓이는 자리, 그리고 $200$ ms 묵은 목표의 $130$ ms, $40$틱, $41$카운트. **2회차:** §4–§6. §4의 패널 셀 TF 트리를 간선마다 방향과 스탬프를 붙여 그리고, §6의 예제 트리를 `batteryOK`가 실패하는 tick에서 그리며 끝낸다. **3회차:** §6.5 — listing을 돌린다 — 그다음 §7–§11. §9의 사다리를 패널 과제에 대 보고 현장 실패 하나를 §10의 분류에 넣은 뒤, 스스로 점검 5, 6번으로 끝낸다. **4회차:** 나머지 스스로 점검과 과제. 과제의 실습은 §5의 큐 깊이를 쓸어 본다. 더 깊이 노트(Eppner 논문의 다른 두 축, 샘플링 항의 최악값, §6.5의 합성 비용과 signal temporal logic)는 논문이 그것을 요구할 때 읽는다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**. 장치(plant)는 제어공학에서 제어 대상인 물리 시스템을 부르는 말이고, P6은 카탈로그의 '시계 위의 카트'다. 곧은 레일 위에서 모터 하나로 움직이는 카트이고, 그 위치 $p$를 엔코더가 센다. 카메라가 카트를 보고 비전 노드가 카트의 목표를 발행하며, 제어기는 엔코더를 읽고 모터 명령을 쓴다. P6이 고정하는 숫자는 넷이고, 이 페이지가 하나를 더한다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $N$ | $2048$ counts/m | 엔코더 분해능. 한 카운트는 $1000/2048=0.488$ mm |
| $T_{\text{cam}}$ | $20$ ms | 비전 주기: $20$ ms마다 목표 하나, $50$ Hz |
| $T_{\text{ctrl}}$ | $5$ ms | 제어 주기, $200$ Hz. 한 주기가 **틱**(tick), 곧 제어기가 엔코더를 읽고 명령을 쓰는 순간이다 |
| 예산 | $70$ ms | 카메라 노출 중간점부터 카트에 힘이 가해질 때까지 허락된 시간 |
| $v$ | $0.10$ m/s | 계산 절의 카트 속도(이 페이지) |

**예산**이 이 페이지의 주제다. 목표가 쓰이는 순간 예산보다 늙었다면, 만들어질 때 아무리 좋은 목표였어도 늦은 것이다. §3은 그런 예산을 항마다 쌓고, §8은 같은 엔코더로 보정 오차를, §11은 같은 시계로 정책의 추론 시간을 따진다.

*범위: 이 페이지는 알고리즘과 로봇 사이에 앉은 런타임 사안들을 가르친다 — 루프, 행동 인터페이스, 데드라인과 지터를 포함한 지연 예산, 좌표계와 TF 트리, 미들웨어 어휘, 실행 계층과 그 behavior tree, 그 계층 뒤의 아키텍처 계보와 §6.5의 형식적 작업 명세(선형 시간 논리, 모델 검사와 반응형 합성의 차이, 실현 가능성, GR(1) 부분 논리, signal temporal logic을 불리언 명제부터 쌓아 올린다), 신뢰성, 단계적 배포와 실패 분류. ROS 2 자체는 가르치지 않는다. 그것은 [[04-robotics/ros2/index|25. ROS 2]]의 페이지들이다. 제어 설계([[04-robotics/control-theory-ce397|5. 제어]]), 상태 추정([[04-robotics/state-estimation-slam|3. 상태 추정]]), 계획([[04-robotics/planning-decision-making|4. 계획]])도 마찬가지다. 이 페이지가 가르치는 것은 그것들에 대해 무엇을 확인할지이며, 전자공학이나 설치 튜토리얼이 아니다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 356" style="max-width:100%;height:auto" role="img" aria-label="P6를 밀리초 시간축 하나에 그린 그림: 위에 20 ms마다 비전 눈금, 아래에 5 ms마다 제어 눈금, 한 주기의 다섯 시점, 샘플링 구간이 붙은 70 ms 예산 막대, 옅게 그린 200 ms짜리 늦은 목표">
  <line x1="96.6" y1="142" x2="530" y2="142" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <line x1="96.6" y1="118" x2="96.6" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="136" y1="118" x2="136" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="175.4" y1="118" x2="175.4" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="214.8" y1="118" x2="214.8" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="254.2" y1="118" x2="254.2" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="293.6" y1="118" x2="293.6" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="333" y1="118" x2="333" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="372.4" y1="118" x2="372.4" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="411.8" y1="118" x2="411.8" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="451.2" y1="118" x2="451.2" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="490.6" y1="118" x2="490.6" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="530" y1="118" x2="530" y2="142" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="96.6" y1="142" x2="96.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="106.5" y1="142" x2="106.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="116.3" y1="142" x2="116.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="126.2" y1="142" x2="126.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="136" y1="142" x2="136" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="145.8" y1="142" x2="145.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="155.7" y1="142" x2="155.7" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="165.6" y1="142" x2="165.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="175.4" y1="142" x2="175.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="185.2" y1="142" x2="185.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="195.1" y1="142" x2="195.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="204.9" y1="142" x2="204.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="214.8" y1="142" x2="214.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="224.7" y1="142" x2="224.7" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="234.5" y1="142" x2="234.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="244.3" y1="142" x2="244.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="254.2" y1="142" x2="254.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="264.1" y1="142" x2="264.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="273.9" y1="142" x2="273.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="283.8" y1="142" x2="283.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="293.6" y1="142" x2="293.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="303.4" y1="142" x2="303.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="313.3" y1="142" x2="313.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="323.1" y1="142" x2="323.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="333" y1="142" x2="333" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="342.9" y1="142" x2="342.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="352.7" y1="142" x2="352.7" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="362.5" y1="142" x2="362.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="372.4" y1="142" x2="372.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="382.2" y1="142" x2="382.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="392.1" y1="142" x2="392.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="401.9" y1="142" x2="401.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="411.8" y1="142" x2="411.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="421.6" y1="142" x2="421.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="431.5" y1="142" x2="431.5" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="441.4" y1="142" x2="441.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="451.2" y1="142" x2="451.2" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="461.1" y1="142" x2="461.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="470.9" y1="142" x2="470.9" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="480.8" y1="142" x2="480.8" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="490.6" y1="142" x2="490.6" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="500.4" y1="142" x2="500.4" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="510.3" y1="142" x2="510.3" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="520.1" y1="142" x2="520.1" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="530" y1="142" x2="530" y2="149" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="136" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">0</text>
  <text x="175.4" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">20</text>
  <text x="214.8" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">40</text>
  <text x="254.2" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">60</text>
  <text x="293.6" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">80</text>
  <text x="333" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">100</text>
  <text x="372.4" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">120</text>
  <text x="411.8" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">140</text>
  <text x="451.2" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">160</text>
  <text x="490.6" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">180</text>
  <text x="530" y="162" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">200 ms</text>
  <text x="530" y="111" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">비전 · 50 Hz: 20 ms마다 긴 눈금</text>
  <text x="530" y="178" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">제어 · 200 Hz: 5 ms마다 짧은 눈금</text>
  <circle cx="136" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <text x="136" y="110" font-size="11.5" fill="currentColor" text-anchor="middle">노출 중간점</text>
  <circle cx="244.3" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M244.3 138 V32 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="36" font-size="11.5" fill="currentColor">비전 발행</text>
  <circle cx="258.1" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M258.1 138 V50 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="54" font-size="11.5" fill="currentColor">제어기의 TF 조회</text>
  <circle cx="264.1" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M264.1 138 V68 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="72" font-size="11.5" fill="currentColor">목표를 소비하는 제어 틱</text>
  <circle cx="273.9" cy="142" r="2.4" fill="currentColor" fill-opacity="1"/>
  <path d="M273.9 138 V86 H285.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="289.9" y="90" font-size="11.5" fill="currentColor">모터로 전류가 나감</text>
  <rect x="96.6" y="190" width="19.7" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="3 2"/>
  <rect x="116.3" y="190" width="19.7" height="16" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.8" stroke-dasharray="3 2"/>
  <rect x="136" y="190" width="137.9" height="16" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.3"/>
  <text x="204.9" y="202" font-size="11.5" fill="currentColor" text-anchor="middle" font-weight="600">70 ms 예산</text>
  <text x="204.9" y="223" font-size="11" fill="currentColor" text-anchor="middle">70/20 = 3.5 비전 주기</text>
  <text x="204.9" y="237" font-size="11" fill="currentColor" text-anchor="middle">70/5 = 14 제어 틱</text>
  <text x="91.6" y="195" font-size="11" fill="currentColor" text-anchor="end">샘플링</text>
  <text x="91.6" y="209" font-size="11" fill="currentColor" text-anchor="end">½T<tspan dy="3">cam</tspan><tspan dy="-3" dx="3">= 10 ms</tspan></text>
  <text x="91.6" y="223" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">최악 20 ms</text>
  <line x1="273.9" y1="206" x2="273.9" y2="260" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5" stroke-dasharray="3 3"/>
  <rect x="136" y="262" width="394" height="10" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="130" y="271" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">200 ms 늦음</text>
  <text x="530" y="256" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">낡은 목표 위의 40틱 (200/5)</text>
  <path d="M273.9 278 v6 H530.0 v-6" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="401.9" y="298" font-size="11" fill="currentColor" text-anchor="middle">200 − 70 = 130 ms 예산 초과</text>
  <text x="12" y="312" font-size="11" fill="currentColor">0.10 m/s면 그 목표가 200 ms 늙는 동안 카트가 20 mm를 간다:</text>
  <text x="12" y="326" font-size="11" fill="currentColor">카운트당 0.488 mm(1000/2048)이므로 목표가 전혀 몰랐던 41 카운트다.</text>
  <text x="12" y="344" font-size="11" fill="currentColor" fill-opacity="0.7">P6이 정하는 것은 막대의 두 끝뿐이고, 그 사이 세 시점은 예시 위치다.</text>
</svg>

카탈로그 주기 그대로의 P6을 밀리초 시간축 하나에 그렸다. 위에는 $20\,\mathrm{ms}$마다 비전 눈금, 아래에는 $5\,\mathrm{ms}$마다 제어 눈금이 있고, 한 주기의 다섯 시점 — 노출 중간점부터 제어기의 TF 조회(목표의 스탬프 시각에 목표의 좌표계가 어디 있었는지 묻는 요청, §4)를 거쳐 모터에 전류가 나가는 순간까지 — 가 비전 주기 $3.5$개, 제어 틱 $14$개인 $70\,\mathrm{ms}$ 예산 안에 든다. 샘플링 구간 $\tfrac12 T_{\text{cam}}=10\,\mathrm{ms}$(최악 $20\,\mathrm{ms}$)는 노출 중간점 앞에 있으므로 P6의 $70\,\mathrm{ms}$에는 들지 않고 §3의 지연 $L$에는 든다. 곧 예산은 $L-\tfrac12T_{\text{cam}}$이고 $L$은 평균 $80\,\mathrm{ms}$다. 옅은 막대는 제어기에 $200\,\mathrm{ms}$ 늦게 도착한 목표로, 예산을 $130\,\mathrm{ms}$ 넘기고 낡은 목표 위에서 제어 틱 $40$개가 돌며, 그동안 $0.10\,\mathrm{m/s}$의 카트는 목표가 전혀 몰랐던 $20\,\mathrm{mm}$, 곧 $0.488\,\mathrm{mm}$짜리 카운트 $41$개만큼 움직였다.

### 대상으로 한 번 끝까지 · Worked case

P6의 한 주기를 그 예산에 대 보는 네 단계이고, 숫자는 카탈로그의 것이다. 예산과 틱은 이 페이지의 대상에서 정의했다. 그 말을 정의하는 절보다 먼저 쓰는 낱말이 셋 있고, 각각 처음 나오는 자리에서 풀어 쓴다.

**1단계 — P6 자신의 단위로 본 예산.** $70\,\mathrm{ms}$는 비전 주기 $70/20=3.5$개, 제어 틱 $70/5=14$개다. 노출 하나가 그것이 낳는 힘까지 가는 동안 더 새로운 프레임이 서너 장 찍히고 제어기는 열네 번 틱한다. 예산은 영상이 나타내는 순간인 노출 중간점에서 시작하므로, 그 순간 이전의 기다림 — 평균 $10\,\mathrm{ms}$, 그림의 점선 구간 — 은 예산에 들지 않는다. §3은 그 기다림을 지연 $L$의 첫 항으로 센다.

**2단계 — 200 ms 묵은 목표.** 노출 중간점에서 $200\,\mathrm{ms}$ 뒤에 제어기에 닿은 비전 메시지는 예산을 $200-70=130\,\mathrm{ms}$ 넘기고, 그 위에서 틱 $200/5=40$개가 돈다. 예산보다 늙은 목표를 **낡았다**(stale)고 한다(§3은 무엇이 목표를 낡게 만드는지 더해 보고, §5는 미들웨어 설정 한 줄이 그렇게 만드는 것을 보여 준다). 나이는 거리이기도 하다. $v=0.10\,\mathrm{m/s}$면 카트는 $0.10\times0.200=0.020\,\mathrm{m}=20\,\mathrm{mm}$를 가고, 한 카운트가 $0.488\,\mathrm{mm}$이므로 목표가 전혀 몰랐던 $20/0.488=40.96\approx41$카운트다. [[04-robotics/state-estimation-slam|3. 상태 추정]]의 추정기는 구하지 못한다. 목표가 늦은 것이지 잡음이 아니다.

**3단계 — 모든 틱이 제시간에 끝나는가.** 다섯 틱의 응답 시간, 곧 각 틱이 릴리스된 순간부터 그 일이 끝날 때까지를 재면 $1.2, 1.5, 4.8, 1.3, 1.4\,\mathrm{ms}$다. 틱마다 한 주기 $5\,\mathrm{ms}$의 **데드라인**(deadline), 곧 그때까지는 일이 끝나야 하는 시한이 있다. 평균은 $2.04\,\mathrm{ms}$이고, 가장 빠른 것부터 가장 느린 것까지의 퍼짐인 **지터**(jitter)는 $4.8-1.2=\mathbf{3.6}\,\mathrm{ms}$다(두 말은 §3이 정의한다). 데드라인 미스는 **0회**, 최악의 틱에서 여유는 $5.0-4.8=0.2\,\mathrm{ms}$ — 그 틱은 제 주기의 $96\%$를 썼다. *비예 — 평균을 주파수로 인용하기:* $1000/2.04=490\,\mathrm{Hz}$는 존재하지 않는 루프를 묘사한다. 루프는 $200\,\mathrm{Hz}$이고, 다섯 틱 중 하나는 미스까지 $0.2\,\mathrm{ms}$를 남겼다. 같은 일을 단단한 접촉을 렌더링하는 햅틱 서보의 $1\,\mathrm{ms}$ 데드라인([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]) 아래 두면 평균은 하나도 달라지지 않은 채 다섯 개 전부가 미스한다.

**4단계 — 독법.** 주기, 지연, 잡음은 타임라인 위의 서로 다른 세 표시다. 1–2단계는 지연이고 3단계는 고정 주기에서의 데드라인 검사이며, 어느 것도 걸러서 없앨 잡음이 아니다. 이 장치에서 "아무 일도 안 일어나면" 이득을 의심하기 전에 TF 스탬프나 QoS 불일치(서비스 품질, 곧 미들웨어의 전달 설정, §5)를 먼저 의심하라. 그 연습이 [[04-robotics/ros2/qos-executors-time|25.5]]이고, P6의 센서들이 실제로 보태는 잡음은 센서마다 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]에 있다.

### 1. 닫힌 로봇 스택

로봇의 블록들은 서로 다른 주기로 돈다 — 30 Hz 카메라, 10 Hz 정책, 1 kHz 모터 제어기는 모순이 아니다 — 그러니 각 블록이 쓰는 데이터의 나이(age)와 블록 사이의 인터페이스는 가정하지 말고 설계해야 한다. 그 블록들이 이루는 루프:

```mermaid
flowchart LR
    S["센서"] --> PRE["전처리"] --> EST["추정"] --> PP["계획 / 정책"] --> C["제어기"] --> A["액추에이터"] --> W["물리 세계"]
    W --> S
    LOG["클럭 · 좌표계 · 로그 · 안전"] -.-> EST
    LOG -.-> PP
    LOG -.-> C
```

그림의 화살표마다 어떤 나이의 데이터가 실려 있고, §3이 그 나이를 센다.

> [!tip] 로봇 시스템이 실제로 설계되는 네 축
> 위의 스택은 데이터 흐름 그림이다. *설계* 그림 — 마감이 있는 상황에서 시스템이 돌아가느냐를
> 가르는 그림 — 은 Eppner 등이 Amazon Picking Challenge 2015 우승 시스템을 사후 분석한
> 것(RSS 2016)이다. 로봇 시스템은 네 개의 스펙트럼 위에 놓이며, 우승 시스템은 각 스펙트럼 위에서
> 대부분의 다른 참가작과 다른 **위치**를 골랐다는 주장이다:
>
> | 축 | 무엇과 무엇을 바꾸는가 |
> |---|---|
> | **모듈성 대 통합** | 깨끗한 인터페이스는 디버깅이 되고, 촘촘히 통합된 쪽은 모듈 경계가 버렸을 정보를 활용한다 |
> | **일반성 대 가정** | 기꺼이 명시하는 가정 하나하나가 성능을 사고, 그 가정이 깨질 때의 실패 모드를 지불한다 |
> | **연산 대 embodiment** | 순응형 그리퍼나 깔때기 모양 지그는 원래라면 인식·제어 문제였을 것을 역학으로 푼다 |
> | **계획 대 피드백** | 미리 숙고할 것인가 실행 중에 반응할 것인가, 그리고 과제의 불확실성이 각각을 얼마나 정당화하는가 |
>
> 학습 중심으로 읽는 사람이 가장 자주 건너뛰는 것이 세 번째 축이고, 이는 [[04-robotics/grasping|15 §5]]의
> extrinsic dexterity와 같은 관찰이다 — **미리 배치해 둔 기하는 계산하지 않아도 되는 능력이다.**
> 우승 팀이 다른 두 축에서 한 구체적 선택은 아래 더 깊이 노트에 있다.

> [!note]- 더 깊이 · Deeper
> 논문은 다른 두 축에서도 구체적 선택을 밝힌다. *모듈성 대 통합*에서는 인식을 그리퍼에 맞췄다:
> 흡착 컵은 집을 수 있는 면 하나에 닿기만 하면 성공하므로, 물체 인식은 정확한 pose가 아니라
> 대략적인 바운딩 박스 pose만 내면 됐다. *계획 대 피드백*에서는 미리 정한 힘 감시 피드백 제어기
> 열을 센서 이벤트(물체에 닿으면 흡착을 켠다)로 전환해 집기 동작을 만들었고, 팔을 이동 베이스에
> 올려 모션 플래닝이 대부분 필요 없게 했다.

### 2. Embodiment와 행동 인터페이스

같은 학습 모델도 저수준 인터페이스와 제어 주기가 바뀌면 다르게 행동할 수 있으므로, 로봇의 "action"에 관한 결과는 그것이 어떤 물리적 명령이고 어떤 몸이 실행하는지 밝히기 전까지는 거의 아무것도 말하지 않는다. Embodiment는 형태, 액추에이터와 전동 장치, 센싱, 컴플라이언스, 페이로드, 한계, 환경
결합을 포함한다. 모터·유압·기어비·백래시·포화·부족구동·대역폭이 어떤 행동이 의미
있는지를 결정한다. 기어 달린 전기 구동계 하나를 열어 본 것, 곧 두 방정식, 토크–속도 선, 반사 관성, 열 한계가 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]다. 두 종류의 구동 밑에 깔린 물리는 전기 쪽이 [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자]], 유압 쪽이 [[02-foundations/fluid-power|0.6.3 유체 동력]]이다.

논문이 "action"이라 하면 그것이 관절 위치·속도·토크·모터 전류·말단 pose·[[04-robotics/force-compliance-control|임피던스 타깃]]
(정확히 도달할 위치가 아니라 기준 주위의 원하는 강성과 감쇠)·상위 스킬 중 무엇인지 확인하라. 말단 pose 행동은
[[04-robotics/modern-robotics/ch06-inverse-kinematics|역기구학(MR 6장)]]이 — 가지 선택과
특이점까지 포함해 — 풀어 주기 전까지 모터에 닿지 않고, 웨이포인트 행동은
[[04-robotics/modern-robotics/ch09-trajectory-generation|시간 스케일링(MR 9장)]]이 액추에이터
한계 안의 속도 프로파일을 줄 때 비로소 운동이 된다. 바퀴 베이스에서는 이 둘이
[[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR 13장의 비홀로노믹 기구학]] 위에
앉는다.

### 3. 타이밍과 지연 예산

*한 문장으로:* 로봇은 언제나 조금 전의 세계를 보고 행동한다. 이 절은 그 '조금 전'이 얼마인지 단계마다 더해 보고, 가장 느린 주기도 제시간에 끝나는지 묻는다.

*이 절에서 하나만 가져간다면:* 지연 예산은 프레임 주파수가 아니라 이름 붙은 항들의 합이고 — 아래의 $70\,\mathrm{ms}$는 식의 항 가운데 노출 중간점 뒤의 것들이라 $L-\tfrac12T_{\text{cam}}$이다 — 지연은 곧 거리다. $1\,\mathrm{m/s}$에서 $7\,\mathrm{cm}$다. $200\,\mathrm{ms}$ 늦은 P6의 목표는 위의 계산 절에 풀려 있다.

#### 예시 예산, 그리고 지연이 치르는 값

| 구성요소 | 예시 지연 |
|---|---:|
| 카메라 노출/판독 | 15 ms |
| 네트워크 추론 | 40 ms |
| 통신 | 10 ms |
| 명령 처리 | 5 ms |
| **관측→행동** | **70 ms** |

1 m/s에서 70 ms는 새 명령이 효과를 내기 전 7 cm의 이동에 해당한다. **주파수는 지연이 아니다**: 30 Hz 시스템도 옛 프레임 위에서 행동할 수 있다. 샘플링 주기, 추론 주기, 지터, 데드라인 미스, 큐잉, 타임스탬프 정책, 그리고 지연이 끝-끝으로 측정됐는지 확인하라. 그 7 cm가 너무 큰지는 그것이 무엇을 고치느냐에 달렸다. 추정의 σ와 견준 것이 [[04-robotics/capstone-panel-contact|26. 캡스톤 §5]]의 낡음 거리다.

#### 지연 예산, 항 하나씩

**예산을 합으로 쓰면.** **관측-행동 지연** $L$은 물리적 사건이 일어난 순간부터 그 사건에서 나온 명령이 구동기에 효과를 내는 순간까지의 경과 시간이다. 측정값 하나가 아니라 이름 붙은 항들의 합이고, 각 항에는 그것을 책임지는 구성 요소가 있다:

$$L=\tfrac12 T_{\text{cam}}+t_{\text{exp}}+t_{\text{tx}}+t_{\text{inf}}+t_{\text{dec}}+T_{\text{ctrl}}$$

단계들이 직렬이고 앞 단계가 끝나야 다음이 시작되므로 항들이 더해진다. 각 항은:

- $\tfrac12 T_{\text{cam}}$ — **샘플링 지연**. 사건은 한 프레임 주기 $T_{\text{cam}}$ 안의 임의의 순간에 일어나므로, 표본으로 잡히기까지 평균 반 주기, 최악의 경우 한 주기를 기다린다. 블록 다이어그램에 나타나지 않는 항이자 *주파수*가 *지연*이 아닌 이유다.
- $t_{\text{exp}}$ — **노출과 판독**. 영상이 나타내는 순간인 노출 중간점부터 마지막 행이 센서를 떠날 때까지(중간점 앞의 노출 절반은 샘플링 대기에 속한다). 움직이는 베이스에서 각각이 치르는 값과, 영상의 스탬프가 어느 순간을 가리켜야 하는지는 [[04-robotics/perception-sensors-rigs|3.6 인식 센서 §2, §9]]이다.
- $t_{\text{tx}}$ — **전송**. 모델을 돌리는 컴퓨터까지의 선이나 버스. 네트워크가 더하는 것과, 패킷 하나를 잃으면 TCP와 UDP에서 각각 얼마를 치르는지는 [[02-foundations/tools/computer-networks|12.5 컴퓨터 네트워크 §1]]이고, 두 기계에 걸쳐 잰 지연에는 두 시계의 오프셋도 들어 있다([[02-foundations/tools/linux-shell|12.1 §11]]).
- $t_{\text{inf}}$ — **추론**. 순전파 그 자체. 대부분의 논문이 보고하는 유일한 항이다.
- $t_{\text{dec}}$ — **디코딩과 IPC**(inter-process communication, 한 컴퓨터 안의 두 프로그램 사이의 전달). 신경망 출력을 명령 메시지로 바꾸고 전달하는 데 드는 시간.
- $T_{\text{ctrl}}$ — **구동**. 명령이 적용되기까지의 제어 주기 하나.

**표의 70 ms가 이 합에서 놓이는 자리.** 위의 표와 P6의 예산은 둘 다 노출 중간점에서 시작하므로 첫 항을 뺀다. 두 행은 각각 항 하나로, $t_{\text{exp}}=15$, $t_{\text{inf}}=40\,\mathrm{ms}$다. "통신" $10\,\mathrm{ms}$는 $t_{\text{tx}}+t_{\text{dec}}$다. 그림의 주기에서는 영상이 곧바로 추론으로 들어가고, 그 뒤에 이동하는 것은 비전 노드에서 제어기로 가는 목표이기 때문이다($55\,\mathrm{ms}$에 발행되어 $65\,\mathrm{ms}$의 틱이 소비한다). "명령 처리" $5\,\mathrm{ms}$는 P6의 제어 주기 $T_{\text{ctrl}}$이다. 그래서 노출 중간점부터 센 예산은 $L-\tfrac12T_{\text{cam}}$이다. P6의 $50\,\mathrm{Hz}$에서 예산 $70\,\mathrm{ms}$는 평균 $80\,\mathrm{ms}$, 최악 $90\,\mathrm{ms}$의 $L$이다. 뒤의 두 페이지는 이 글자를 다르게 쓴다. [[04-robotics/capstone-panel-contact|26. 캡스톤]]은 이 예산 자체를 $L$로 쓰고, [[04-robotics/ros2/simulation-and-control|25.7]]의 낡음 장부는 노출 중간점부터 목표가 제어기에 닿을 때까지의 더 짧은 구간을 $L$로 쓴 뒤 그 뒤에 주기들을 더한다.

**비예:** *주파수*를 더하는 것은 예산이 아니다. "30 Hz 카메라, 25 Hz 정책, 500 Hz 제어기"는 어떤 지연으로도 환원되지 않는다. 주파수는 더해지지 않고, 직렬 사슬에서는 가장 빠른 단계도 제 몫의 고정 지연을 보태기 때문이다. 주파수가 똑같은 두 시스템이 큐잉과 타임스탬프 정책만으로 $L$에서 50 ms 차이가 날 수 있다.

#### 데드라인과 지터

**데드라인과 지터의 정의.** 주기 $T$인 주기 작업은 $r_k=r_0+kT$에 **릴리스**되어 $f_k$에 끝나므로 **응답 시간**은 $R_k=f_k-r_k$다. **데드라인** $D$는 릴리스 이후 그때까지는 끝나야 하는 시각이고(보통 $D=T$), $R_k>D$인 인스턴스가 **데드라인 미스**다. 데드라인의 강도는 그 값과는 별개의 주장이고, 세 가지가 있다:

- **hard** — 한 번의 미스가 시스템 실패다(단단한 접촉을 쥐고 있는 루프, 브레이크 해제);
- **firm** — 늦은 결과는 쓸모가 없어 버려지지만 버려도 살아남는다(놓친 인지 프레임);
- **soft** — 늦은 결과는 질이 떨어져도 여전히 값이 있다(지도 갱신, 운전자 화면).

**지터**는 인스턴스에 걸친 타이밍 양의 *퍼짐*이지 결코 그 평균이 아니며, 최대-최소로 보고한다:

$$J=\max_k R_k-\min_k R_k$$

데드라인 논증에 필요한 것은 중심이 아니라 극단이기 때문이다 — 표준편차는 미스를 내는 꼬리를 정확히 가려 버린다. 계산 절의 3단계가 두 정의를 P6의 제어 루프에 적용한다: 지터 $3.6\,\mathrm{ms}$, 미스 0회, 여유 $0.2\,\mathrm{ms}$. 릴리스 지터와 출력 지터도 나머지 두 시점에 대해 같은 방식으로 정의한다. 지터는 로그가 간직할 때만 남는다. `%.3f`로 찍은 틱 시각은 $120\,\mu\mathrm{s}$의 늦음을 반올림해 지워 버린다. [[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식]]의 계산 절 5단계가 보이는 그대로다. 그리고 C++ 틱의 최악의 경우를 주기 안에 붙잡아 두는 규칙은 [[04-robotics/ros2/cpp-for-robot-code|25.0 로봇 코드를 위한 C++ §9]]이다.

#### 축척대로 그린 예산, 그리고 시각–운동 루프 하나의 합

P6 자신의 예산은 계산 절에서 풀었다. 루프가 단단한 접촉을 렌더링하면 예산이 한 자릿수 넘게 빡빡해진다. 이 페이지의 관측-행동 예산 $70\,\mathrm{ms}$에 견주어 햅틱 서보는 유계 지터로 약 $1\,\mathrm{ms}$ 안에 닫혀야 하므로 단위가 프레임이 아니라 밀리초다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성]]). 표의 예산을 실제 비율로 그리면:

<svg viewBox="0 0 560 190" style="max-width:100%;height:auto" role="img" aria-label="표의 70 ms 예산을 노출 중간점부터 ms당 5 px의 실제 비율로 그린 그림: 노출과 판독 15, 추론 40, 통신 10, 명령 5, 그리고 그 왼쪽 끝 앞, 예산 밖에 P6의 샘플링 대기 10 ms">
  <rect x="110.0" y="58" width="50.0" height="30" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <text x="104.0" y="67" font-size="10.5" fill="currentColor" text-anchor="end">샘플링 대기</text>
  <text x="104.0" y="80" font-size="10.5" fill="currentColor" text-anchor="end">½T<tspan dy="3" font-size="10">cam</tspan><tspan dy="-3" dx="2">= 10 ms</tspan></text>
  <text x="104.0" y="93" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.75">예산에 들지 않음</text>
  <rect x="160.0" y="58" width="75.0" height="30" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.1"/>
  <text x="197.5" y="78" font-size="11" fill="currentColor" text-anchor="middle">15</text>
  <rect x="235.0" y="58" width="200.0" height="30" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.1"/>
  <text x="335.0" y="78" font-size="11" fill="currentColor" text-anchor="middle">40</text>
  <rect x="435.0" y="58" width="50.0" height="30" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.1"/>
  <text x="460.0" y="78" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <rect x="485.0" y="58" width="25.0" height="30" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.1"/>
  <text x="497.5" y="78" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <text x="197.5" y="102" font-size="10.5" fill="currentColor" text-anchor="middle">노출 / 판독</text>
  <text x="335.0" y="102" font-size="10.5" fill="currentColor" text-anchor="middle">추론</text>
  <line x1="460.0" y1="88" x2="460.0" y2="108" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="460.0" y="119" font-size="10.5" fill="currentColor" text-anchor="middle">통신</text>
  <line x1="497.5" y1="88" x2="507.5" y2="108" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="503.5" y="119" font-size="10.5" fill="currentColor" text-anchor="start">명령</text>
  <line x1="160.0" y1="38" x2="160.0" y2="58" stroke="currentColor" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="3 3"/>
  <line x1="510.0" y1="38" x2="510.0" y2="58" stroke="currentColor" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="3 3"/>
  <text x="160.0" y="33" font-size="11" fill="currentColor" text-anchor="middle">노출 중간점</text>
  <text x="510.0" y="33" font-size="11" fill="currentColor" text-anchor="end">명령이 효과를 냄</text>
  <path d="M160.0 130 v6 H510.0 v-6" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="335.0" y="151" font-size="11" fill="currentColor" text-anchor="middle">70 ms 예산 = L − ½T<tspan dy="3" font-size="10">cam</tspan></text>
  <text x="335.0" y="167" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1 m/s면 로봇은 이 예산 안에서 7 cm를 간다</text>
</svg>

표의 $70\,\mathrm{ms}$를 노출 중간점부터 명령이 효과를 낼 때까지 실제 비율로 그렸다. 노출과 판독 $15$, 추론 $40$, 통신 $10$, 명령 처리 $5\,\mathrm{ms}$이고, 왼쪽 끝 앞의 점선은 예산이 세지 않는 P6의 샘플링 대기 $\tfrac12T_{\text{cam}}=10\,\mathrm{ms}$다. 추론이 예산의 $40/70=57\%$이고 $1\,\mathrm{m/s}$면 로봇은 그 안에서 $7\,\mathrm{cm}$를 가니, "$30\,\mathrm{Hz}$로 돈다"는 "그 프레임이 얼마나 낡았나"와 다른 질문에 답한다.

> [!example] 계산 예제 · Worked example
> **루프 하나를 더해 보기.** 대표적인 시각–운동 스택을 잡자: 30 Hz 카메라(평균 샘플링 지연
> $\tfrac{1}{2}\times 33.3 = 16.7$ ms), 노출과 판독 12 ms, GPU 호스트로의 전송 5 ms, 정책 추론
> 40 ms, 행동 디코딩과 프로세스 간 통신 3 ms, 500 Hz 관절 제어기(2 ms). 합
> $16.7 + 12 + 5 + 40 + 3 + 2 = \mathbf{79}$ ms.
>
> **대가는 두 번 치른다.** *낡음*으로: 0.3 m/s로 움직이는 말단은 자기 이미지가 행동을
> 만들어 낼 때쯤 이미 $0.3 \times 0.079 = 24$ mm를 갔다. $\pm 10$ mm 파지 허용 오차 앞에서는
> $0.010/0.079 = 0.13$ m/s로 늦추거나 앞을 예측해야 한다. *피드백 루프의 죽은 시간*으로 보면
> 지연 $T$는 신호 주파수 $f$(Hz)에서 $360 fT$도의 위상 지연을 더한다. $T$초 지연이 한 주기의 $fT$만큼이기 때문이다.
> 지연 전 여유가 90°이고 45°를 남겨야 한다고 가정하면, 교차 주파수 $f$에서 지연이 쓸 수 있는 몫은
> 최대 45°다: $360fT\le 45°$, 따라서 $f\le 45°/(360T)$. $T=0.079$ s를 넣으면 예시 교차 주파수 예산은 $(90°-45°)/(360T)=\mathbf{1.6}$ Hz다. 이것은
> 보편 상한이 아니다. 지연 전 여유는 장치와 제어기가 정하고, 지연을 넣으면 교차 주파수도
> 움직일 수 있다. [[04-robotics/control-theory-ce397|5. 제어 §5.5]]가 이 조건부 예산을 유도한다.
>
> **여기서 얻는 독법.** 추론 시간을 절반으로(40 → 20 ms) 줄이면 합은 59 ms이고, 위와 같은
> 90°/45° 가정의 예시 예산은 $45°/(360°\times0.059\,\mathrm{s})=2.1$ Hz가 된다 — 실질적인 개선이지만 표제가 암시하는
> 2배가 아니라 1.3배다. 추론이 예산의 절반뿐이기 때문이다. 그리고 정책 주파수를 보고하는 어떤 논문에든 무엇을 물어야 하는지도
> 알려 준다: 10 Hz 추론은 10 Hz 루프가 아니고, 그 차이가 이 표의 나머지 전부다.

$79$ ms는 평균이다. 샘플링 항을 최악값으로 두고 다시 한 계산은 아래 더 깊이 노트에 있다.

> [!note]- 더 깊이 · Deeper
> **평균과 최악.** 계산 절 3단계의 지터 구분이 이 합을 다시 읽게 한다. $79$ ms(반올림 전 $78.7$ ms)는 *평균* 예산이다. 샘플링 항 $\tfrac12 T_{\text{cam}}=16.7$ ms를 최악값 $T_{\text{cam}}=33.3$ ms로 바꾸면 $16.7+78.7=\mathbf{95.3}$ ms가 된다. 그 $16.7$ ms 차이는 편향이 아니라 지터이므로 어떤 보정으로도 없앨 수 없다. 평균 예산에 맞춰 튜닝한 제어기는 설계보다 $16.7/78.7=21\%$ 더 늙은 외란을 만나고, $0.3$ m/s에서 말단의 낡음은 프레임마다 $0.3\times0.0787=24$ mm와 $0.3\times0.0953=29$ mm 사이를 오간다.

### 4. 좌표계와 TF 트리

*한 문장으로:* 로봇이 쓰는 모든 위치는 어떤 관점에서 어떤 순간에 적힌 것이고, TF 트리는 "이것이 저기서 보면, 그 시각에, 어디에 있는가"에 답을 하나만 주는 장부다.

*이 절에서 하나만 가져간다면:* 루프 폐쇄는 `map` → `odom` 간선 하나만 다시 쓰므로, `map`에 저장된 목표는 로봇이 가만히 있는데도 $30\,\mathrm{cm}$ 튄다. 이 절 끝의 예가 그것을 계산한다.

흔한 프레임: world, map, odom, base, sensor, end-effector, tool, object. 모든 변환에는
방향과 타임스탬프가 필요하다. 그럴듯한 숫자 행렬이라도 관례가 틀리면 학습이 안정적으로
고칠 수 없는 계통적 실패를 만든다.

**변환, 그리고 그 이름을 정하는 방향.** 변환 ${}^{a}T_{b}\in SE(3)$에는 같은 행렬에 대한 두 가지 독법이 있다. 프레임 $b$에서 표현한 점의 좌표를 프레임 $a$의 좌표로 옮기고, 동시에 프레임 $a$에서 표현한 프레임 $b$의 pose *이다*. 위아래 첨자를 다 쓰면 변환은 안쪽 첨자가 지워지며 이어지고, 회전을 전치해서 역을 얻는다:

$${}^{a}T_{c}={}^{a}T_{b}\,{}^{b}T_{c},\qquad {}^{b}T_{a}=\big({}^{a}T_{b}\big)^{-1}=\begin{pmatrix}R^{\top} & -R^{\top}t\\ 0 & 1\end{pmatrix}$$

역이 이 꼴인 것은 변환을 되돌리려면 평행이동을 되돌리기 전에 회전을 먼저 되돌려야 하기 때문이다. **비예, 그리고 이것이 위에서 말한 "그럴듯한 행렬"이다:** 역은 같은 회전에 평행이동만 부호를 뒤집은 것이 *아니다*. ${}^{a}T_{b}$가 $90°$ 요와 $t=(1,0)$ m라고 하자. 올바른 역의 평행이동은 $-R^{\top}t=(0,1)$ m인데, 부호만 뒤집으면 $(-1,0)$ m가 나온다 — 크기는 똑같고 로그에서 완벽하게 그럴듯하며 $1.41$ m 틀렸다. [[02-foundations/se3-geometry|SE(3)]]가 이 대수를 주고, TF 트리가 런타임 장부를 준다.

**TF 트리의 정의.** 노드가 프레임이고 간선이 타임스탬프가 찍힌 부모→자식 변환인 방향 그래프이되, 그것을 *트리*로 만드는 조건이 셋이다. 모든 프레임은 부모가 정확히 하나이고, 부모가 없는 프레임은 뿌리 하나뿐이며, 순환이 없다. 여기서 귀결이 셋 따라 나오고 각각은 조건이 깨졌을 때의 실패 양상이다. 임의의 두 프레임 사이 경로가 정확히 하나이므로 조회가 모호하지 않고 그 경로를 따른 합성일 뿐이다. 같은 자식 프레임을 두 발행자가 쓰는 것은 병합이 아니라 오류다. 부모가 둘인 프레임은 트리가 아니기 때문이고, 증상은 두 답 사이를 깜빡이는 변환이다. 그리고 모든 간선이 스탬프를 지니므로 조회는 *시각에 대한* 질의이고 그 시각을 감싸는 두 스탬프 사이에서 보간된다. 버퍼 밖의 질의는 외삽하지 않고 실패하는데, 이것이 올바른 동작이자 "bag에서는 되는데 실시간에서는 안 된다"의 흔한 출처다(*bag*은 ROS가 메시지 흐름을 기록해 두었다가 나중에 재생하는 로그다, §5).

**외워 둘 관례.** REP-103(ROS Enhancement Proposal, ROS 프로젝트가 글로 정한 관례 가운데 하나)이 축과 단위를 고정한다. 오른손 좌표계, 로봇 몸체에서 $x$ 앞, $y$ 왼쪽, $z$ 위, 지리 프레임에서는 ENU(동–북–위), 단위는 SI와 라디안. REP-105는 이동 로봇의 사슬 `map` → `odom` → `base_link` → 센서 프레임을 고정하며, 각각이 다음의 부모다. `odom`은 연속이지만 한없이 드리프트하고, `map`은 드리프트가 없지만 불연속이다. *그* 순서인 이유는 부모가 하나라는 규칙이다. `base_link`는 이미 `odom`을 부모로 가지고 둘을 가질 수 없으므로 위치추정 시스템은 그것의 부모를 바꿀 수 없고, 대신 `map` → `odom` 간선을 발행해 전역 보정 전체를 그 변환 하나에 접어 넣는다. "지도가 튀었다"는 이야기는 전부 그 간선이 다시 쓰인 것이다.

**패널 셀의 트리.** [[04-robotics/capstone-panel-contact|26. 캡스톤]]의 셀에서는 카탈로그의 두 링크 팔 P2([[02-foundations/lab-plants|0.6]])가 고정된 베이스에 서서, 도구에 단 센서, 곧 카탈로그의 거리 센서 P5로 패널까지의 거리를 읽는다. 간선은 넷이고 모두 부모 → 자식이다. `world` → `base_link`는 팔의 설치로 정적이다. `base_link` → `tool`은 순기구학으로, 틱마다 다시 발행되고 그것을 낳은 관절 측정의 시각이 스탬프로 찍힌다. `tool` → `range_sensor`는 도구 위 센서의 설치로 정적이며 보정에서 온다. `range_sensor` → `panel`은 센서가 읽은 거리로 — 26의 1단계에서 $11.6$ cm로 융합된다 — 팔이 홈에 있을 때 잰 시각이 스탬프로 찍힌다. 팔의 좌표계에서 본 패널은 조회 `base_link` → `panel`, 곧 트리를 따라 내려가는 간선 셋의 합성이고, 이때 `base_link` → `tool`은 **측정의 스탬프 시각의 것**을 써야 한다. 팔이 홈을 떠난 뒤의 도구 자세와 합성하면, 똑같은 $11.6$ cm 거리가 패널을 도구가 지금 가리키는 곳 아무 데나 놓는다.

예를 들어 베이스가 odom에서 $(1.0, 2.0)$ m에 있고 목표가 map에서 $(5.0, 2.0)$ m로 저장되어 있다고 하자. `map` → `odom`이 항등인 동안 목표는 odom $(5.0, 2.0)$, 즉 $4.00$ m 앞이다. 이제 루프 폐쇄가 전역 추정을 30 cm 보정하고 이것이 `map` → `odom`의 평행이동 $(0.30, 0)$ m로 발행되면, 저장된 그대로의 목표가 odom $(4.70, 2.0)$, $3.70$ m 앞이 된다. 로봇은 전혀 움직이지 않았는데 목표가 30 cm 움직인 것이다. odom에 쥐고 있던 경로는 움직이지 않았고, 지역 제어기에 odom을 먹이는 이유 전부가 그것이다. 행렬이 틀린 것이 아니라 서로 다른 시각의 올바른 변환을 섞은 문제일 수 있다. **여기서 얻는 독법.** 목표·관측·명령의 좌표계와 시각을 추적한다. 전역 보정이 어디서 기준을 바꾸고 하류 제어기가 이를 어떻게 처리하는지 밝힌다.

### 5. 미들웨어 문해력

미들웨어는 §1의 블록 사이 모든 메시지를 나르고, 그 설정도 타이밍의 일부다. 설정 한 줄이, 멈췄던 제어기가 넘겨받는 가장 오래된 목표의 나이를 $0$에서 $180\,\mathrm{ms}$로 바꾼다(아래 큐 문단). 먼저 어휘, 그다음 그 위에 P6의 통신.

| 개념 | 역할 |
|---|---|
| node | 실행 중인 구성요소 |
| topic/message | 비동기 데이터 스트림과 스키마 |
| service | 요청/응답 연산 |
| action | 피드백·취소가 있는 긴 연산 |
| TF | 시간 인덱스된 프레임 변환 |
| bag/log | 재생·분석용 기록 스트림 |
| QoS | 전달·보존·신뢰성·큐 정책 |

ROS는 하나의 구현 생태계이지 시스템 구조 그 자체가 아니다. "ROS에서 돈다"는 지연,
결정론, 안전, 배포 품질에 대해 거의 말해 주지 않는다.

**행마다 데이터뿐 아니라 시간에 관한 약속이 들어 있다.** P6의 통신을 표에 올려 보면 어느 행을 쓸지가 정해진다. $50\,\mathrm{Hz}$ 목표는 *topic*이다. 목표 하나가 $20\,\mathrm{ms}$ 앞의 것을 대체하므로, 하나를 잃어도 다음 것이 메워 주기 때문이다. "카트를 $p=0.5\,\mathrm{m}$로 몰아라"는 *action*이다. 몇 초 동안 돌고, 진행 상황을 보고하고, 목표가 바뀌면 취소될 수 있어야 하기 때문이다. 제어기 이득 설정은 *service*나 파라미터 호출이다. 요청 하나에 응답 하나이고, 아무도 모르게 사라지면 안 되기 때문이다. 그리고 카트의 프레임은 *TF*다. 목표는 그것이 측정된 프레임과 스탬프 없이는 쓸모가 없기 때문이다(§4).

**큐는 §3 예산의 한 항이다.** 미들웨어는 메시지를 history depth $N$ 아래 쌓아 둔다([[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS) §2]]). 생산자와 소비자 사이의 유한 버퍼이고, 가득 찼을 때 무엇을 버릴지 규칙이 있다는 점에서 두 스레드 사이의 큐와 똑같다([[02-foundations/tools/concurrency|12.8 동시성 §6]]). ROS 2 밑의 미들웨어인 DDS는 [[02-foundations/tools/computer-networks|12.5 컴퓨터 네트워크 §8]]이다. 기본 프로파일인 keep-last $10$에서, $200\,\mathrm{ms}$ 멈췄던 제어기는 쌓인 목표들 앞에서 다시 돌기 시작해 가장 오래된 것부터 받는다. 발행된 지 $(10-1)\times20=180\,\mathrm{ms}$ 된 목표이고, 노출 중간점부터 세면 그보다 더 묵었으므로 "$70\,\mathrm{ms}$ 예산을 $110\,\mathrm{ms}$ 넘겼다"는 하한이다. 그리고 가장 새 목표에는 열 번째 콜백에서야 닿는다. 알고리즘은 하나도 바뀌지 않았고 설정 한 줄이 바뀌었다. "ROS에서 돈다"가 지연에 대한 주장이 아닌 이유가 이것이다. 같은 노드 그래프라도 프로파일이 다르면 최악의 목표 나이가 다르다.

### 6. 행동 오케스트레이션과 과제 실행

*한 문장으로:* 지금 어느 계획기나 제어기를 돌릴지, 그리고 실패하면 무엇을 할지 누군가는 정해야 하고, behavior tree는 매 tick마다 세 가지 답 — 끝났다, 실패했다, 아직 하는 중이다 — 가운데 하나로 그 결정을 새로 내린다.

*이 절에서 하나만 가져간다면:* 3값 tick(Success, Failure, Running)과 그것이 아래 예제 트리에서 사 주는 것이다. 주행 중에 `batteryOK`가 거짓이 되면 바로 다음 tick이 `FollowPath`를 halt하고 복구로 들어간다.

#### 실행 계층과 그 어휘

과제 명령과 플래너/제어기 사이에는 보통 **실행 계층**이 있다 — 유한상태기계(FSM),
behavior tree, 또는 task executive — 지금 *어느* 플래너·정책·제어기를 돌릴지, 실패하면
무엇을 할지를 결정한다.

```mermaid
flowchart TD
    T["과제 명령"] --> X["상태기계 / behavior tree / executive"]
    X --> PL["플래너 또는 학습 정책"] --> CT["제어기"]
    CT --> X
```

핵심 어휘: **가드**(조건)로 발화되는 **전이**를 가진 **상태/행동**; 행동 전에 검사하는
**precondition**과 후에 검증하는 **postcondition**; **timeout**과 **retry**; 단계가
실패했을 때의 **fallback**과 **recovery behavior**; 피드백과 **취소**가 있는 **action
server**. 뼈대 예제:

```
Idle → 물체 감지 → 파지 계획 → 실행 → 검증
                                  ├─ 성공 → 놓기
                                  └─ 실패 → 재계획 / 도움 요청 / 안전 정지
```

Behavior tree는 이를 모듈적으로 합성하고 필드 시스템에서 흔하다; FSM은 단순하지만
상태가 늘면 얽힌다.

#### tick이 반환하는 것으로 정의하는 behavior tree

**tick이 무엇을 반환하는가로 정의하는 behavior tree.** Behavior tree는 잎이 **action**(무언가를 한다)과 **condition**(무언가를 검사한다)이고 내부 노드가 **제어 흐름 노드**인 뿌리 있는 트리다. 실행은 **tick**으로 이루어진다. 정해진 주기로 뿌리에 주입되어 각 노드의 종류에 따라 자식으로 전파되는 신호다. tick된 모든 노드는 세 상태 중 정확히 하나를 반환하고, 이 3값 반환이 설계의 전부다:

$$\text{tick}(n)\in\{\,\textsf{Success},\ \textsf{Failure},\ \textsf{Running}\,\}$$

**Running**은 FSM에 대응물이 없는 상태다. "시작했고 아직 안 끝났으니 다시 tick하라"는 뜻이므로 긴 action이 트리를 막지 않고, Running인 자식을 가진 노드는 자신도 Running이기 때문에 위로 전파된다. 세 노드 계열은 각각 무엇을 반환하는지로 정의된다:

- **Sequence** — 자식을 왼쪽에서 오른쪽으로 tick한다. 실패하는 첫 자식에서 **Failure**, Running인 첫 자식에서 **Running**, 모든 자식이 성공했을 때만 **Success**를 반환한다. 자식들에 대한 논리 **AND**이고, 선행 조건을 쓰는 방법이 이것이다. 조건을 앞에 두면 조건이 거짓인 동안 뒤의 action은 절대 돌지 않는다.
- **Fallback**(**selector**라고도 한다) — 왼쪽에서 오른쪽으로 tick하며, 성공하는 첫 자식에서 **Success**, Running인 첫 자식에서 **Running**, 모든 자식이 실패했을 때만 **Failure**를 반환한다. 논리 **OR**이며, 첫째 뒤의 자식들이 순서대로 시도되는 대안이므로 이것이 복구 구성물이다.
- **Decorator** — 자식이 **정확히 하나**이고, 그 자식이 반환한 상태나 자식을 tick할지 여부 자체를 바꾼다. `Inverter`는 Success와 Failure를 맞바꾸고, `RetryUntilSuccessful(n)`은 실패하는 자식을 최대 $n$번 다시 tick하며, `Timeout(ms)`는 너무 오래 도는 자식을 실패시키고, `RateController(hz)`는 주어진 주기로만 자식을 tick하고 그 사이에는 마지막 상태를 되풀이한다. 자식이 하나라는 규칙이 decorator를 제어 흐름 노드와 갈라놓는 바로 그것이다.

#### tick 계약, 트리 하나, 그리고 트리가 아닌 것

**tick 계약**은 건너뛰었다가 버그를 만드는 부분이다. 조항이 셋이다. tick은 매 주기 **뿌리**에서 다시 들어오므로 조건이 계속 재평가되고, 앞선 형제의 조건이 거짓이 되는 순간 이미 Running이던 action이 버려진다 — 호출 사슬에 견주어 트리가 사 주는 것이 그 반응성이다. 따라서 Running이었다가 tick 경로에서 빠진 노드는 명시적으로 **halt**되어야 하고, 그래서 모든 action 노드는 tick뿐 아니라 halt 구현까지 진다. 그리고 상태는 *반환*될 뿐 전이로 저장되지 않는다. 형제 사이에는 애초에 간선이 없기 때문이다.

*예.* `Fallback[ Sequence[ batteryOK, Sequence[ ComputePath, FollowPath ] ], Sequence[ ClearCostmaps, Spin ] ]`. 배터리가 버티는 동안 로봇은 주행한다. 주행 단계 중 하나가 Failure를 반환하면 fallback이 복구 가지로 넘어간다. 그리고 주행 중에 `batteryOK`가 거짓이 되면 뿌리에서 오는 바로 다음 tick이 안쪽 sequence를 그 조건에서 실패시키고, `FollowPath`가 끝나기를 기다리지 않고 halt한 뒤 복구로 들어간다. [[04-robotics/ros2/navigation-nav2|25.9 Nav2 §2]]가 실제 제품의 트리 하나를 읽는다. 합성 변종(`PipelineSequence`, `RecoveryNode`)과 1 Hz 재계획 decorator까지 들어 있다.

<svg viewBox="0 0 560 394" style="max-width:100%;height:auto" role="img" aria-label="§6의 예제 behavior tree를 뿌리에서 오는 연속한 두 tick에 그리고 노드마다 반환한 상태를 적은 그림: tick k에는 FollowPath가 Running이고 Running이 뿌리까지 올라간다. tick k+1에는 batteryOK가 실패해 주행 sequence가 실패하고, FollowPath가 halt되며 복구 가지가 돈다">
  <text x="12" y="26" font-size="12" font-weight="600" fill="currentColor">tick k: 배터리는 버티고, FollowPath는 아직 주행 중</text>
  <line x1="280" y1="66" x2="150" y2="80" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="280" y1="66" x2="440" y2="80" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="150" y1="102" x2="70" y2="116" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="150" y1="102" x2="222" y2="116" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="222" y1="138" x2="164" y2="152" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="222" y1="138" x2="282" y2="152" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="440" y1="102" x2="386" y2="116" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="440" y1="102" x2="498" y2="116" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <rect x="230.0" y="44" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="236.0" y="59" font-size="11" fill="currentColor" fill-opacity="1">? Fallback</text>
  <rect x="311.0" y="47" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="319.0" y="59" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="100.0" y="80" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="106.0" y="95" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="181.0" y="83" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="189.0" y="95" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="390.0" y="80" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="396.0" y="95" font-size="11" fill="currentColor" fill-opacity="0.5">→ Sequence</text>
  <rect x="471.0" y="83" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="479.0" y="95" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="20.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="26.0" y="131" font-size="11" fill="currentColor" fill-opacity="1">batteryOK</text>
  <rect x="101.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="109.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">S</text>
  <rect x="172.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="178.0" y="131" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="253.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="261.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="336.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="339.0" y="131" font-size="11" fill="currentColor" fill-opacity="0.5">ClearCostmaps</text>
  <rect x="417.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="425.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="448.0" y="116" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="454.0" y="131" font-size="11" fill="currentColor" fill-opacity="0.5">Spin</text>
  <rect x="529.0" y="119" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="537.0" y="131" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="114.0" y="152" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="120.0" y="167" font-size="11" fill="currentColor" fill-opacity="1">ComputePath</text>
  <rect x="195.0" y="155" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="203.0" y="167" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">S</text>
  <rect x="232.0" y="152" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="238.0" y="167" font-size="11" fill="currentColor" fill-opacity="1">FollowPath</text>
  <rect x="313.0" y="155" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="321.0" y="167" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <text x="442" y="168" font-size="10.5" fill="currentColor" fill-opacity="0.7" text-anchor="middle">tick되지 않음</text>
  <line x1="8" y1="188" x2="552" y2="188" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="12" y="204" font-size="12" font-weight="600" fill="currentColor">tick k+1: batteryOK가 거짓이 된다</text>
  <line x1="280" y1="244" x2="150" y2="258" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="280" y1="244" x2="440" y2="258" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="150" y1="280" x2="70" y2="294" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="150" y1="280" x2="222" y2="294" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="222" y1="316" x2="164" y2="330" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="222" y1="316" x2="282" y2="330" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="3 3"/>
  <line x1="440" y1="280" x2="386" y2="294" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <line x1="440" y1="280" x2="498" y2="294" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <rect x="230.0" y="222" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="236.0" y="237" font-size="11" fill="currentColor" fill-opacity="1">? Fallback</text>
  <rect x="311.0" y="225" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="319.0" y="237" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="100.0" y="258" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="106.0" y="273" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="181.0" y="261" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="189.0" y="273" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">F</text>
  <rect x="390.0" y="258" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="396.0" y="273" font-size="11" fill="currentColor" fill-opacity="1">→ Sequence</text>
  <rect x="471.0" y="261" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="479.0" y="273" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="20.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="26.0" y="309" font-size="11" fill="currentColor" fill-opacity="1">batteryOK</text>
  <rect x="101.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="109.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">F</text>
  <rect x="172.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="178.0" y="309" font-size="11" fill="currentColor" fill-opacity="0.5">→ Sequence</text>
  <rect x="253.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="261.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">H</text>
  <rect x="336.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="339.0" y="309" font-size="11" fill="currentColor" fill-opacity="1">ClearCostmaps</text>
  <rect x="417.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="425.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">S</text>
  <rect x="448.0" y="294" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.9"/>
  <text x="454.0" y="309" font-size="11" fill="currentColor" fill-opacity="1">Spin</text>
  <rect x="529.0" y="297" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.9"/>
  <text x="537.0" y="309" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1" font-weight="700">R</text>
  <rect x="114.0" y="330" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="120.0" y="345" font-size="11" fill="currentColor" fill-opacity="0.5">ComputePath</text>
  <rect x="195.0" y="333" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="203.0" y="345" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">–</text>
  <rect x="232.0" y="330" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.0" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.45" stroke-dasharray="3 2"/>
  <text x="238.0" y="345" font-size="11" fill="currentColor" fill-opacity="0.5">FollowPath</text>
  <rect x="313.0" y="333" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="321.0" y="345" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.5">H</text>
  <text x="340.0" y="339" font-size="10.5" fill="currentColor" fill-opacity="0.8">halt됨: Running이었는데</text>
  <text x="340.0" y="352" font-size="10.5" fill="currentColor" fill-opacity="0.8">tick 경로에서 빠졌다</text>
  <text x="342" y="230" font-size="10.5" fill="currentColor" fill-opacity="0.8">fallback이 다음 자식인</text>
  <text x="342" y="242" font-size="10.5" fill="currentColor" fill-opacity="0.8">복구 가지로 넘어간다</text>
  <text x="12" y="368" font-size="11" fill="currentColor">S 성공 · F 실패 · R 실행 중 · H halt됨 · – tick되지 않음</text>
  <text x="12" y="384" font-size="11" fill="currentColor" fill-opacity="0.8">실선 간선은 이번 tick이 지나간 곳, 점선은 tick되지 않은 곳이다.</text>
</svg>

예제 트리를 뿌리에서 오는 연속한 두 tick에 그리고, 노드마다 반환한 상태를 적었다. tick $k$에는 배터리가 버틴다. `batteryOK`와 `ComputePath`가 Success, `FollowPath`가 Running을 반환하고, Running이 두 sequence를 거쳐 뿌리까지 올라가며, 복구 가지는 아예 tick되지 않는다. tick $k+1$에는 `batteryOK`가 Failure를 반환하므로 주행 sequence가 경로 sequence를 tick하지도 않은 채 첫 자식에서 실패하고, Running이던 `FollowPath`와 그 sequence가 halt되며, fallback이 복구 가지를 tick해 `ClearCostmaps`는 성공하고 `Spin`이 돈다.

**비예.** 트리는 과제 시작 때 한 번 평가되는 if-then-else 사슬이 아니고, sequence는 프로그램의 `;`이 아니다 — 그렇게 읽으면 다시 tick하는 것이 메커니즘이 아니라 낭비로 보인다. 문법만 예쁜 상태 기계도 아니다. FSM은 제어 흐름을 전이 간선에 두고 그 수가 최대 $n(n-1)$까지 가며 복구 규칙 하나하나를 그것이 발동할 수 있는 모든 상태마다 복제해야 하는 반면, 트리의 제어 흐름은 형제의 순서와 3값 반환뿐이다. 이것이 복구에 **범위**를 주는 장치다. 가장 가까운 바깥 fallback이 누가 복구할지를 정하므로, 플래너의 실패가 시스템 전체의 최후 수단을 부를 필요가 없다.

*읽을 때 왜 중요한가.* 논문이 로봇이 "회복했다", "재시도했다"고 하면 정책이 아니라 fallback 노드가 한 일이다. 누가 실패를 감지하고, 누가 대응을 고르고, 무엇이 종료 조건인지 확인하라.

### 6.5 아키텍처 계보와 형식적 작업 명세

*한 문장으로:* 로봇 소프트웨어는 세 속도로 도는 세 층에 자리를 잡았고, 시간 논리는 그 층들이 항상, 언젠가, 또는 결코 해서는 안 되는 일을 컴퓨터가 설계를 검사하거나 그 규칙에서 제어기를 만들 수 있을 만큼 정확히 적는 방법이다.

*이 절에서 하나만 가져간다면:* 명세는 충족 가능하면서도 실현 불가능할 수 있다. 아래의 패널 배달 식은 A 다음 B를 배달하는 고장 없는 실행이면 만족되지만, 첫 배달 전에 구역 센서가 고장 날 수 있으므로 어떤 제어기도 그것을 보장하지 못한다.

§6의 실행 계층은 두 극단이 실패한 뒤 로보틱스가 도달한 설계의 가운데 층이고, 시간 논리는 그 설계가 보장해야 할 것을 검사하거나 생성할 수 있을 만큼 정확하게 적는 언어다.

#### 아키텍처의 세 계보

- **Sense–plan–act** (Shakey 시대의 숙고형 파이프라인): 센싱이 세계 모델을 만들고, 플래너가 그 위에서 추론하고, 제어기가 실행한다. 제어기는 병목인 플래너를 기다려야 하고, 센서를 직접 보지 못하므로 로봇은 생각하는 동안 반응하지 못한다.
- **Subsumption** (Brooks 1986): 각자 센서를 액추에이터에 잇는 반응형 행동들이 병렬로 돈다. 상위 층은 하위 층의 입력을 *억제*(suppress)하거나 출력을 *차단*(inhibit)한다. 세계 모델이 없어 반응은 빠르지만 긴 지평의 계획도 없다.
- **Three-layer** (Gat 1998): 빠른 *controller*, 활성 행동을 고르고 실패를 처리하는 *sequencer*(executive), 느린 *deliberator*. 층마다 제 주기로 돌고, 느려도 되는 것은 deliberator뿐이다.

| 층 | 주기 | ROS 2에서의 구현 |
|---|---|---|
| controller | 가장 빠름 | `ros2_control` 컨트롤러 매니저, `update_rate` 기본 100 Hz ([[04-robotics/ros2/simulation-and-control\|ROS 2 제어]]) |
| sequencer | 중간 | behavior tree; Nav2의 `bt_navigator`는 기본 트리에서 플래너를 1초에 한 번 다시 tick한다 ([[04-robotics/ros2/navigation-nav2\|Nav2 §2]]) |
| deliberator | 과제 단위 | 과제 플래너나 TAMP ([[04-robotics/planning-decision-making\|4 §7]]), 또는 목표를 내놓는 VLA/LLM 플래너 |

층 사이 통신은 §5의 구분을 따른다: 토픽은 데이터를, 서비스와 액션은 응답이 있는 명령을 나른다. **여기서 얻는 독법.** "LLM이 계획한다"는 deliberator만 바꾼 것이다. 회복은 여전히 sequencer에, 안정성은 여전히 controller에 있다.

#### 명제에서 출발하는 시간 논리

**시간 논리.** **명제**(proposition)는 $\mathit{near}$나 $\mathit{stop}$처럼 단계마다 참 또는 거짓인 이름 붙은 사실이고, 불리언 연결사는 한 단계 안에서 명제를 묶는다: $\neg\varphi$(아니다), $\varphi\wedge\psi$(그리고), $\varphi\vee\psi$(또는), 그리고 $\varphi\rightarrow\psi$($\varphi$이면 $\psi$). 마지막 것은 $\varphi$가 참이고 $\psi$가 거짓일 때만 거짓이므로, $\varphi$가 거짓인 단계에서는 *공허하게*(vacuously) 참이다. 시간 논리는 시간에 따른 열(sequence)에 대한 논리다: 식의 참·거짓을 한 순간이 아니라 실행 전체 — 단계마다 어떤 명제가 참인지 적은 목록 — 에 대해 판정한다. LTL(Pnueli 1977)은 이산 단계마다의 불리언 명제에 네 연산자를 더한다: $\mathsf{X}\,\varphi$(다음 단계), $\mathsf{F}\,\varphi$(언젠가), $\mathsf{G}\,\varphi$(항상), $\varphi\,\mathsf{U}\,\psi$($\psi$가 올 때까지 매 단계 $\varphi$, 그리고 $\psi$는 반드시 온다). 패턴: 안전성 $\mathsf{G}\,\neg\mathit{collision}$, 활성(liveness) $\mathsf{G}\mathsf{F}\,\mathit{atCharger}$(어느 단계에서 보든 충전소 방문이 아직 앞에 남아 있으므로, 무한 실행에서 로봇은 무한히 자주 돌아온다), 응답 $\mathsf{G}(\mathit{req}\rightarrow\mathsf{F}\,\mathit{grant})$, 순서 $\mathsf{F}(a\wedge\mathsf{F}\,b)$.

#### 모델 검사, 합성, 그리고 로봇이 실제로 쓰는 논리

*모델 검사*는 주어진 설계의 모든 거동이 $\varphi$를 만족하는지 묻고, 예 또는 반례 궤적을 돌려준다. *반응형 합성*은 모든 환경 입력 열에 대해 $\varphi$를 만족하는 제어기를 만들며, 각 출력은 과거만 보고 고른다. 실제 로봇은 다음 입력을 보기 전에 행동해야 하기 때문이다.

이 인과성이 두 낱말을 가른다. $\varphi$는 어떤 입출력 실행 하나라도 만족하면 *충족 가능*(satisfiable), 한 제어기가 모든 입력을 이기면 *실현 가능*(realizable)이다. 환경 입력 $\mathit{req},\mathit{obst}$와 출력 $\mathit{move}$에 대해 $\mathsf{G}(\mathit{req}\rightarrow\mathsf{X}\,\mathit{move})\wedge\mathsf{G}(\mathit{obst}\rightarrow\neg\mathit{move})$는 충족 가능하지만(장애물 없는 실행 아무거나) 실현 불가능하다: $t$에 $\mathit{req}$, $t+1$에 $\mathit{obst}$가 오면 $t+1$의 $\mathit{move}$는 어느 값도 둘을 함께 만족하지 못한다.

완전한 LTL의 합성은 비싸므로, 로보틱스는 제한된 부분 논리 GR(1)에서 제어기를 합성하고 연속 신호는 signal temporal logic으로 판정한다. 이유와 방법은 더 깊이 노트에 있다.

> [!note]- 더 깊이 · Deeper
> **왜 부분 논리인가.** 완전한 LTL의 합성은 식 크기에 대해 이중 지수적이다(Pnueli & Rosner 1989). 대략, 식을 오토마톤으로 바꾸는 데 지수 하나, 제어기가 어떤 의무가 남아 있는지 늘 알도록 그 오토마톤을 결정적으로 만드는 데 또 지수 하나가 든다. 그래서 로보틱스는 GR(1), 곧 *Generalized Reactivity(1)* 같은 부분 논리를 쓴다(초기 조건, `always` 단계 제약, `always eventually` 목표). GR(1)은 게임 상태 공간 크기의 다항 시간에 풀리고(Piterman, Pnueli & Sa'ar 2006), Kress-Gazit, Fainekos & Pappas(2009)가 반응형 임무·운동 계획에 적용했다.
>
> **Signal temporal logic.** 연속 신호에는 signal temporal logic이 시간 구간과 실수값 술어를 붙이고, robustness 점수가 신호가 식을 얼마나 여유 있게 만족하거나 위반하는지 말해 준다(Maler & Nickovic 2004; Donzé & Maler 2010). "거리가 항상 2 m 초과"라면 점수는 가장 나쁜 여유다: 가장 가까이 온 거리가 2.5 m인 실행은 $+0.5$ m, 1.8 m까지 파고든 실행은 $-0.2$ m를 받는다.

#### 명세 하나 쓰기, 그리고 로그 위에서 검사하기

**명세 쓰기.** "작업자와 항상 2 m를 유지하라; 언젠가 패널 A를, 그다음 패널 B를 배달하라; 구역 센서가 고장 나면 멈춰라." $\mathit{near}$ = 작업자 2 m 이내(인식이 설정), $\mathit{fail}$ = 구역 센서 고장, $\mathit{dA},\mathit{dB}$ = 패널 배달 완료, $\mathit{stop}$ = 영속도 명령으로 두자. "멈춰라"를 "다음 단계까지 멈추고 계속 멈춰 있어라"로 읽으면:

$$\varphi = \mathsf{G}\,\neg\mathit{near} \;\wedge\; \mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB}) \;\wedge\; \mathsf{G}(\mathit{fail}\rightarrow\mathsf{X}\,\mathsf{G}\,\mathit{stop})$$

이 식은 충족 가능하다 — 고장 없이 작업자와 떨어져 A 다음 B를 배달하는 실행이면 된다 — 하지만 이 그대로는 실현 불가능하며, 환경의 전략 하나가 그 이유를 보여 준다. $\mathit{fail}$은 환경이 정하므로, 아무것도 배달되기 전인 $t_0$에 환경이 $\mathit{fail}$을 올린다고 하자. 그러면 세 번째 연언항이 $t_1$부터 모든 단계에서 $\mathit{stop}$을 요구하고, 영속도 명령을 받은 로봇은 아무것도 배달하지 못하므로, 제어기가 무엇을 고르든 그 실행에서 $\mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB})$는 거짓이다. 모든 제어기를 이기는 입력 열 하나면 실현 불가능함이 증명되고, 이는 위의 $\mathit{req}/\mathit{obst}$ 예와 같은 논증이다. 그래서 활성 부분을 그 전략도 만족하는 $\mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB})\vee\mathsf{F}\,\mathit{fail}$로 약화하거나, 배달 전에는 고장이 없다는 가정을 명시해야 한다. 아래 로그는 이 약화가 무엇을 통과시키는지, 그리고 그것을 막는 연언항을 보여 준다.

> [!example] 계산 예제 · Worked example
> **가정: 유한 궤적 의미론.** 기록된 $t_0,\dots,t_5$가 실행 전체다. $\mathsf{G}$와 $\mathsf{F}$는 남은 단계에 걸치고, 마지막 단계의 $\mathsf{X}$는 거짓이다. 궤적: $t_0\,\{\}$, $t_1\,\{\mathit{dB}\}$, $t_2\,\{\mathit{dA}\}$, $t_3\,\{\mathit{fail}\}$, $t_4\,\{\mathit{stop}\}$, $t_5\,\{\mathit{stop}\}$.
>
> **$\mathsf{F}(\mathit{dA}\wedge\mathsf{F}\,\mathit{dB})$: 거짓.** $\mathit{dA}$는 $t_2$에서만 참이고, 유일한 $\mathit{dB}$는 그보다 앞선 $t_1$에 있다. 순서 없는 $\mathsf{F}\,\mathit{dA}\wedge\mathsf{F}\,\mathit{dB}$는 참이다. B가 먼저였다는 사실은 중첩된 형태만 잡아낸다.
>
> **$\mathsf{G}(\mathit{fail}\rightarrow\mathsf{X}\,\mathsf{G}\,\mathit{stop})$: 참.** 함의는 $t_3$을 빼면 공허하게 참이고, $t_3$에서는 $t_4$와 $t_5$의 $\mathit{stop}$을 요구하는데 둘 다 성립한다. 같은 단계 형태 $\mathsf{G}(\mathit{fail}\rightarrow\mathit{stop})$는 $t_3$에서 거짓이다. 한 단계의 반응 지연을 허용할지는 표기가 아니라 요구사항의 결정이다.
>
> **여기서 얻는 독법.** $\mathsf{G}\,\neg\mathit{near}$가 참이므로 전체 $\varphi$는 거짓이고 약화한 명세는 참이다 — 하지만 이 실행이 올바른 고장 정지여서가 아니다. B는 $t_1$에, A보다 먼저 배달됐고 고장은 $t_3$에야 왔다. 선언항 $\mathsf{F}\,\mathit{fail}$이 고장보다 먼저 일어난 순서 위반까지 눈감아 준 것이다. 약화에는 나중의 고장이 눈감아 줄 수 없는 연언항, "A 전에는 B 없음"이 필요하고, 이것은 *약한 until*로 $\neg\mathit{dB}\ \mathsf{W}\ \mathit{dA}=\mathsf{G}\,\neg\mathit{dB}\vee(\neg\mathit{dB}\ \mathsf{U}\ \mathit{dA})$라 쓴다. B가 끝내 오지 않아도 참이다. 이 로그에서는 거짓이고 고장이 먼저 온 로그 $\{\},\{\mathit{fail}\},\{\mathit{stop}\},\{\mathit{stop}\}$에서는 참이며, 약화한 명세를 여전히 실현 가능하게 둔다. $\mathit{dA}$와 $\mathit{dB}$는 로봇 혼자 정하므로 로봇은 언제든 B를 미뤄 둘 수 있기 때문이다.

코드는 영어 절에 있고, 네 줄의 출력은 차례로 `False True`, `True False`, `False True`, `False True`다. 마지막 줄이 순서 연언항이 이 로그를 거부하고 고장이 먼저 온 로그를 받아들인다는 것이다.

**논문에서 확인할 것.** *누가 각 명제를 통제하는가*: 작업자가 로봇 쪽으로 걸어올 수 있다면 $\mathsf{G}\,\neg\mathit{near}$에는 사람의 움직임에 대한 가정이 필요하거나 응답 형태로 바뀌어야 한다. 거리 자체는 표준의 문제다([[04-robotics/hri-safety|HRI와 안전 §6]]). *접지(grounding)*: 보장은 추상화에 대한 것이므로 $\mathit{near}$를 설정하는 인식과 $\mathit{stop}$을 실현하는 제어기만큼만 좋다. *의미론*: 무한 궤적 LTL과 로그의 유한 궤적 평가는 서로 다를 수 있고, 실행 끝의 $\mathsf{X}$와 $\mathsf{G}$에서 가장 잘 드러난다.

### 7. 신뢰성과 안전 장치

노드가 죽어도 명령은 살아 있을 수 있다. 하류 하드웨어가 마지막으로 받은 설정값을 계속 실행할 수 있으므로 침묵은 정지가 아니다. 아래 수단들은 침묵과 낡음과 고장을 결정으로 바꾸기 위해 있다.

- Watchdog: 누락되거나 비정상인 갱신을 감지.
- Heartbeat: 주기적 생존 신호.
- Timeout: 데이터·명령의 만료 선언.
- Graceful degradation: 축소된 능력으로 지속.
- Fail-safe state: 위험을 낮추도록 의도된 상태로 이동.
- 비상 정지: 위험한 운동을 멈추는 독립 수단. 전원을 요청하는 것이 아니라 끊는 수단이고, 그래서 메시지로 보내지 않고 배선으로 건다([[02-foundations/basic-circuits-electronics|0.6.2 §11]]).

평균이 좋은 best-effort 타이밍과 결정론적 데드라인 거동은 다르다. 안전 주장은 안정된
정책 출력만이 아니라 시스템 수준의 증거를 요구한다.

예를 들어 계획기가 발행을 멈췄는데 구동기가 이전 동작을 계속한다면 새 명령의 부재는 정지 명령이 아니다. 하트비트는 생존 여부를 알려 주지만 제어 데이터의 최신성과 유효성은 별도로 검사해야 한다. ROS 2에서는 미들웨어가 둘 다 지켜보게 할 수 있다. 구독의 *deadline* 정책은 메시지 사이의 가장 긴 허용 간격을, 발행자의 *liveliness*와 그 임대 기간(lease duration)은 발행자가 조용히 있어도 되는 시간을 선언한다([[04-robotics/ros2/qos-executors-time|25.5 §2]]). **여기서 얻는 독법.** 누가 침묵을 감지하고 타임아웃을 소유하며 이후 하드웨어가 어떤 명령을 실행하는지 묻는다. 정지뿐 아니라 복귀도 시험한다. 노드가 돌아올 때 대기열의 옛 명령이 권한을 되찾으면 안 된다.

### 8. 보정, 설정, 재현성

보정이나 하드웨어가 다르면 랜덤 시드는 실험을 재현하지 못한다. 2048 대신 2000 counts/m로 설정된 P6의 제어기는 매 실행 1 m마다 $24\,\mathrm{mm}$씩 틀리고, 어떤 시드도 그것을 드러내지 못한다(아래 계산). 그러니 내부/외부 보정, 영점, 단위, 프레임 관례, 제어기 이득, 펌웨어, 모델 가중치, 소프트웨어 커밋, 하드웨어 리비전, 런타임 설정을 기록하라.

**계산: 장치 P6.** 보정 숫자는 그 뒤의 모든 숫자에 들어가므로 실행과 함께 기록한다. P6의 엔코더는 $2048$ counts/m다. 명목값 $2000$ counts/m로 설정된 제어기는 카운트 하나를 $0.488\,\mathrm{mm}$가 아니라 $0.500\,\mathrm{mm}$로 바꾸므로, 카트가 실제로 $1\,\mathrm{m}$, 곧 $2048$ 카운트를 간 뒤에 자신이 $2048/2000=1.024\,\mathrm{m}$에 있다고 믿는다. 거리에 따라 자라고 매 실행에서 똑같이 되풀이되는 $24\,\mathrm{mm}$, 곧 $49$ 카운트의 오차이고, 무작위로 생긴 것이 아니므로 시드를 몇 번 바꿔도 드러나지 않는다. 시계 오프셋은 시간에서 생기는 같은 종류의 오차다. 비전 노드의 시계가 제어기의 시계보다 $10\,\mathrm{ms}$ 앞서 가면 모든 목표는 스탬프가 말하는 것보다 $10\,\mathrm{ms}$ 더 묵었고, 이것은 §3 예산에 숨은 항으로 $0.10\,\mathrm{m/s}$에서 $1\,\mathrm{mm}$다. 시간 보정까지 포함해 각 보정을 어떻게 추정하는지는 [[04-robotics/geometric-perception-calibration|3.5 기하 인식과 보정 §5]]에, 실행 하나를 그때의 하드웨어 상태까지 거슬러 추적할 수 있도록 실험실이 남겨야 할 목록은 [[06-research-practice/experimental-design-reproducibility|실험 설계 §7]]에 있다.

### 9. 시뮬레이션과 단계적 배포

시뮬레이션의 성공은 배포의 증거가 아니다. 아래 사다리의 단은 저마다 앞 단이 시험하지 못한 것을 시험하고, 주장은 그것이 오른 가장 높은 단만큼만 강하다.

| 단계 | 목적 |
|---|---|
| 시뮬레이션 | 빠르고 통제된 개발 |
| software-in-the-loop | 시뮬레이션된 장치/센서 주위로 소프트웨어 인터페이스 시험 |
| hardware-in-the-loop | 실제 컴퓨트/제어기·하드웨어 인터페이스 포함 |
| shadow mode | 로봇에 명령하지 않고 라이브 입력 관찰 |
| 단계적 배포 | 속도·자율성·환경 난이도를 점진적으로 상승 |

**패널 과제 위의 사다리.** 추정한 위치의 패널을 10 N으로 누르는 [[04-robotics/capstone-panel-contact|26. 캡스톤]]의 누르기를 보자. *시뮬레이션*은 26의 랩이다. 루프 전체를 돌리고, 참 면은 코드가 안다. *Software-in-the-loop*은 같은 제어기 코드를 실제 미들웨어를 거쳐 그 시뮬레이션 팔에 대고 돌리므로, 물리는 가짜여도 §5의 큐와 §3의 예산은 진짜다. *Hardware-in-the-loop*은 $1\,\mathrm{ms}$ 제어기를 로봇 자신의 컴퓨터로 옮기고, 셀에 패널 없이 팔을 몬다. *Shadow mode*는 패널을 되돌려 놓되 누르기 명령은 보내지 않는다. 계획기와 거리 추정은 실제로 돌고, 실행마다 명령했을 정지점 — 26의 계산 절에서는 $1.161$ m — 을 손으로 잰 면의 위치 옆에 기록하므로, 어떤 힘도 추정에 기대기 전에 추정의 오차가 드러난다. *단계적 배포*는 그다음 줄인 힘과 접근 속도로 먼저 누르고, 기록된 최대 힘이 한계 안에 머무는 동안에만 그것을 올린다.

이 사다리를 힘을 내는 장치에서 실제로 밟아 본 사례 — 안전한 층으로 나눈 기동, 그리고 수치
불안정과 기계 공진과 마찰 한계주기를 갈라 주는 디버깅 순서 — 는
[[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링·샘플링·안정성 §6]]에 있다.

[[05-construction-robotics/digital-twin-workflows|디지털 트윈]](특정 실제 현장이나 기계를 본뜨고 그로부터 계속 갱신되는 모델)이 자동으로 검증된 예측기인 것은 아니다. 무엇이 동기화·보정·실험 검증됐는지
물어라. [[05-construction-robotics/sim-to-real|Domain randomization]](시뮬레이터 매개변수를 무작위로 바꿔 가며 학습해 실제 세계가 표본 하나로 보이게 하는 방법)은 무작위화한 요인과 범위만 커버한다.

### 10. 실패 분류

눈에 보이는 사건이 그것을 일으킨 실패가 아닌 경우가 많다. $t=12.4$ s의 충돌은 $t=10.3$ s부터 갱신되지 않은 위치 스트림에서 시작할 수 있다. 센서, 추정, 계획, 정책, 제어, 통신, 컴퓨트, 기계, 운용자, 환경 실패를 분리하라. 충돌 하나만 해도 오래된 센싱, 잘못된 위치 추정, 실행 불가능한 계획, 나쁜 추종, 액추에이터 포화 어디서든 비롯될 수 있다. [[06-research-practice/failure-analysis-system-evaluation|3. 실패 분석·시스템 평가]]의 worked case는 이 분리를 로그 하나 전체, F1에 적용한다. 시험 장비 200시간의 실패 여섯 건에 시작 범주를 하나씩 붙이고, 기여 결함과 결과를 그 옆에 둔다.

위의 충돌에서, 낡은 위치가 만든 잘못된 경로를 정확히 추종했다면 그것은 추종 오차 진단에 반하는 증거다. 가상의 전체 조사는 [[06-research-practice/failure-analysis-system-evaluation|실패 분석 §7]]에 있다. **여기서 얻는 독법.** 처음 관찰한 약속 위반과 하류 결과를 따로 기록한다. 추정기의 시작 결함을 찾았어도 최신성 검사가 없어 전파됐을 수 있다. 수정이 하위 시스템 경계를 넘어야 하는 이유다.

### 11. 자원 제약

파라미터 수만으로는 정책이 로봇의 시계에 맞는지 알 수 없다. Jetson Thor 위의 30억 파라미터 정책은 가중치를 한 번 읽는 데만 $22\,\mathrm{ms}$가 걸려 P6의 $20\,\mathrm{ms}$ 비전 주기보다 길다(아래 계산). 온보드/오프보드 컴퓨트는 지연, 네트워크 의존, 전력, 열 한계, 프라이버시, 실패 모드를
바꾼다. 모델 파라미터 수만이 아니라 컴퓨트, 메모리, 대역폭, 배터리/전력, 열 스로틀링,
페이로드, 실시간 부하를 보고하라.

**계산: P6의 시계 위의 정책.** 파라미터 수가 추론 시간의 하한을 정하는 것은 파라미터 하나가 차지하는 바이트 수, 그리고 메모리 대역폭과 함께일 때뿐이다. 배치 크기 1의 밀집(dense) 모델은 순전파 한 번마다 모든 가중치를 메모리에서 적어도 한 번 읽고 가중치마다 산술은 조금밖에 하지 않기 때문이다. [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산 §3]]의 말로 메모리 한계(memory-bound)다. P6의 비전 노드가 [[03-deep-learning/foundations/gpu-computing|1.4 §8]]의 로봇 컴퓨터 Jetson Thor 위의 30억 파라미터 정책이라고 하자. 가중치 하나에 2바이트인 16비트 부동소수 bf16이면 가중치가 $6.0\,\mathrm{GB}$이고 $273\,\mathrm{GB/s}$로 한 번 읽는 데 $22.0\,\mathrm{ms}$가 걸려, 산술을 하나도 하기 전에 이미 $20\,\mathrm{ms}$ 비전 주기보다 길다. 같은 가중치를 NVFP4 — 16개 묶음마다 스케일 하나를 공유하는 NVIDIA의 4비트 형식으로, 가중치당 약 $0.56$바이트 — 로 두면 $6.2\,\mathrm{ms}$에 읽는다([[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §11]]). 그리고 정책이 실제로 도는 주기가 성공률에까지 닿는다. OpenVLA 저자들은 7B 정책을 int8로 평가용 GPU에서 $1.2\,\mathrm{Hz}$로 돌렸는데, 학습 데이터를 기록한 제어기는 $5\,\mathrm{Hz}$였고, BridgeData V2 과제 여덟 개의 성공률이 bf16의 $71.3\%$에서 $58.1\%$로 떨어졌다. int4는 $3\,\mathrm{Hz}$로 돌며 $71.9\%$로 bf16과 같았다([[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]). 그래서 자원 보고는 파라미터 수만이 아니라 바이트, 하드웨어, 그리고 루프가 실제로 돈 주기를 적는다.

### 읽고 나면 말할 수 있어야 하는 것

- sense–estimate–plan–control–act 파이프라인을 그릴 수 있다
- "action"이 나타내는 물리적 명령을 짚을 수 있다
- 주기·지연·지터·데드라인을 구분할 수 있다
- 방향·타임스탬프가 맞는 변환을 추적할 수 있다
- ROS 사용이나 시뮬레이션 성공이 배포 증거가 아닌 이유를 설명할 수 있다
- 실행 계층(FSM/behavior tree)의 위치와 실패 시 역할을 짚을 수 있다
- 실패를 최종 증상이 아니라 유력한 발원 하위 시스템에 배정할 수 있다

> [!tip] 더 깊이 · Going deeper
> 로보틱스 시스템 교과서는 없고, 그 부재 자체가 이 분야의 불평이다. 가장 가까운 대체물이 셋인데 어느 것도 로봇만을 다루지는 않는다: Eppner 외(RSS 2016)는 Amazon Picking Challenge가 실제로 무엇을 가르쳤는지에 관한 글로, 방법이 아니라 통합에 대해 쓰인 드문 논문이다. §5는 [ROS 2 개념 문서](https://docs.ros.org/en/rolling/Concepts.html)를 튜토리얼이 아니라 명세로 읽어라. §7·§8의 어휘는 [NASA 시스템 엔지니어링 핸드북](https://www.nasa.gov/reference/systems-engineering-handbook/)에서 오는데, 로보틱스는 그것을 인용 없이 빌려 쓴다. Tedrake의 [매니퓰레이션 노트](https://manipulation.csail.mit.edu/)에 이 페이지의 틀에 가장 가까운 시스템 장들이 있다.

### 스스로 점검

1. 50 Hz 정책이 여전히 200 ms 지연을 가질 수 있는 이유는?
2. 현장 실패를 재생하려면 어떤 기록이 필요한가?
3. 모델 정확도가 그대로인데 오프보드 VLA가 실패할 수 있는 이유는?
4. hardware-in-the-loop가 입증하는 것과 입증하지 못하는 것은?
5. 3층 아키텍처에서 느려도 되는 층은 어디이고, Nav2의 회복 서브트리와 `ros2_control` 관절 제어기는 각각 어느 층에 있는가?
6. 유한 궤적 $\{a\},\{b\},\{a\},\{\}$에서 $\mathsf{G}(a\rightarrow\mathsf{X}\,b)$는 참인가? 기록된 모든 실행에서 식이 성립하면 실현 가능하다는 뜻인가?

> [!tip]- 정답 · Answers
> 1. 큐, 배칭, 오래된 타임스탬프, 전송, 비동기 단계들이 높은 처리율을 유지하면서 데이터 나이를 키울 수 있다.
> 2. 동기화된 원시 센서, 변환, 명령, 피드백, 클럭, 설정, 소프트웨어/하드웨어 버전, 운용자 이벤트.
> 3. 네트워크 지연/손실, 오래된 관측, 데드라인 미스, 안전 폴백.
> 4. 선택된 하드웨어/소프트웨어 인터페이스와 타이밍은 검증하지만, 실세계 인식·접촉·과제 안전을 그 자체로 검증하지는 않는다.
> 5. 느려도 되는 것은 deliberator뿐이다. 회복 서브트리는 sequencer(executive)의 논리이고, 관절 제어기는 controller 층이다.
> 6. 거짓이다: $t_2$의 $a$는 $t_3$의 $b$를 요구하는데 $t_3$은 비어 있다($t_0$의 의무는 $t_1$에서 채워진다). 아니다: 로그는 표본 실행이라 기껏해야 충족 가능성을 보여 준다. 실현 가능성은 모든 환경 입력 열을 이기는 제어기 하나가 있어야 하므로 합성의 문제다.

### 과제 · Problem set

Tier A. [[02-foundations/lab-plants|0.6]]의 **P6**. 종단 간 예산은 카메라 노출 중간부터 힘까지 $70\,\mathrm{ms}$ 그대로이고, 나머지 숫자는 문항마다 밝힌 대로 바꾼다. 주말 ROS 2 경로는 [[04-robotics/ros2/index|25]]. 템플릿은 영어 절에 있다.

1. **그리기.** 더 싼 $30\,\mathrm{Hz}$ 카메라에 대한 위의 그림. 제어기 $200\,\mathrm{Hz}$와 $70\,\mathrm{ms}$ 예산은 같다. 한 주기의 타임라인 — 노출 중간, 비전 발행, TF 조회, 제어 틱, 모터 전류 — 과 막대로 그린 예산, 같은 축 위의 두 주기, 따로 한 구간으로 그린 샘플링 항. 노출 뒤 $100\,\mathrm{ms}$에 제어기에 닿는 목표를 겹쳐 그려라.
2. **유도.** 업그레이드한 카트: 더 촘촘한 엔코더 $N=4096$ counts/m, 더 싼 $30\,\mathrm{Hz}$ 카메라, $500\,\mathrm{Hz}$ 제어기, 노출 중간점에서 $150\,\mathrm{ms}$ 뒤에 제어기에 닿는 목표, 그리고 $0.25\,\mathrm{m/s}$로 움직이는 카트. (a) 엔코더 한 카운트의 mm. (b) 비전 주기와 제어 주기. (c) 예산이 얼마나 깨지고, 낡은 목표 위에서 제어 틱이 몇 개 도는가? (d) 그 나이 동안 카트가 가는 거리를 mm와 엔코더 카운트로. (e) 이 답들 가운데 더 좋은 추정기가 바꿀 수 있는 것은?
3. **실행.** §5의 큐를 스윕으로. 목표가 $20\,\mathrm{ms}$마다 계속 도착하는 동안 제어기가 $200\,\mathrm{ms}$ 멈추고, 그 구독은 목표를 마지막 $N$개까지 쥔다. 영어 절 템플릿의 `?`를 채워 $N\in\{1,2,5,10\}$에 대해 돌리고, 깊이마다 기다리는 목표 수, 처음 넘겨받는 목표의 나이, 그 예산 초과분을 출력하라. 그리고 해석하라: 어느 깊이가 예산보다 늙은 목표를 제어기에 넘기며, 얼마나 넘기는가? 이 나이는 노출 중간점이 아니라 발행부터 센 것이다 — 참 나이의 상한인가 하한인가?

> [!note]- 그리는 법 · How to draw it
> - 밀리초 단위 시간 축 하나: 위쪽에 비전 노드의 긴 눈금을 $33.3\,\mathrm{ms}$마다, 아래쪽에 제어기의 짧은 눈금을 $5\,\mathrm{ms}$마다. 둘을 *같은* 축에 올리는 것이 요점이다. 두 주기는 두 눈금 간격일 뿐이고, 여기까지 그린 것 중 지연인 것은 하나도 없다.
> - 왼쪽부터 다섯 시점: 노출 중간점, 비전 발행, 제어기의 TF 조회, 목표를 소비하는 제어 틱, 모터로 전류가 나가는 순간.
> - 첫 점과 마지막 점을 잇고 $70\,\mathrm{ms}$라 적은 막대, 그리고 그 아래에 적은 두 개수: 이제 비전 주기 $2.1$개, 제어 틱은 그대로 $14$개.
> - 카메라 상자 안에 숨기지 않고 따로 한 구간으로 그린 샘플링 항 $\tfrac12 T_{\text{cam}}=16.7\,\mathrm{ms}$(최악 $33.3\,\mathrm{ms}$). 최악이면 처리가 시작되기도 전에 예산의 거의 절반이다.
> - 늦은 목표 겹쳐 그리기: 같은 노출 중간점에서 옅은 선으로 출발하는 $100\,\mathrm{ms}$짜리 막대와, 막대를 따라 적은 예산 초과분과 그것이 덮는 제어 틱 수.
> - 축 아래에는 그 결과를 엔코더가 쓰는 단위로: 그 나이 동안 $0.10\,\mathrm{m/s}$의 카트가 가는 거리를 mm와 엔코더 카운트로.
> - 지연 대신 세워 둔 "$30\,\mathrm{Hz}$" 화살표나 목표 주위의 잡음 구름이 들어오는 순간 그림은 틀렸다. 주기·지연·잡음은 서로 다른 세 표시로 남고, [[04-robotics/state-estimation-slam|3. 상태 추정]]의 어떤 추정기도 늦음을 고치지는 못한다.

> [!tip]- 정답 · Solutions
> 1. 비전 눈금은 $33.3\,\mathrm{ms}$마다, 제어는 $5\,\mathrm{ms}$마다. $70\,\mathrm{ms}$ 막대는 이제 비전 주기 $2.1$개, 제어 틱은 그대로 $14$개를 덮는다. 예산의 길이는 같고 카메라 눈금 간격이 다를 뿐이다. 샘플링 항은 평균 $\tfrac12T_{\text{cam}}=16.7\,\mathrm{ms}$, 최악 $33.3\,\mathrm{ms}$로, $50\,\mathrm{Hz}$의 $10$과 $20\,\mathrm{ms}$보다 크다. $100\,\mathrm{ms}$짜리 목표는 예산을 $30\,\mathrm{ms}$ 넘기고 제어 틱 $20$개에 걸치며, 그동안 $0.10\,\mathrm{m/s}$의 카트는 $10\,\mathrm{mm}$, $20.5$카운트를 움직였다. 힘은 여전히 비전 에지가 아니라 제어 에지에서 나간다.
> 2. (a) $1000/4096=0.244\,\mathrm{mm}$, P6의 $0.488$의 절반. (b) $1000/30=33.3\,\mathrm{ms}$와 $1000/500=2\,\mathrm{ms}$. (c) $150-70=80\,\mathrm{ms}$ 초과, 낡은 틱 $150/2=75$개 — 목표는 더 젊은데도 P6의 $40$개보다 많다. 더 빠른 루프가 같은 낡은 목표 위에서 더 자주 돌기 때문이다. (d) $0.25\times0.150=0.0375\,\mathrm{m}=37.5\,\mathrm{mm}$, 곧 $0.0375\times4096=153.6$카운트(반올림하지 않은 카운트 크기 $0.2441\,\mathrm{mm}$로 $37.5\,\mathrm{mm}$를 나눈 값). (e) 없다. 더 촘촘한 엔코더는 카운트 하나의 크기를 절반으로 줄이지만 목표는 여전히 잡음이 아니라 늦은 것이고, [[04-robotics/state-estimation-slam|3]]의 어떤 추정기도 늦음을 고치지 못한다.
> 3. `maxlen=N`, `q[0]`, `BUDGET`. 출력은 `1 1 0 0`, `2 2 20 0`, `5 5 80 10`, `10 10 180 110`이다. 처음 넘겨받는 목표는 $(N-1)\times20\,\mathrm{ms}$ 묵었고, $N\ge5$에서만 예산을 각각 $10$, $110\,\mathrm{ms}$ 넘기며, 제어기는 $N$번째 콜백에서야 가장 새 목표에 닿는다. 나이는 발행부터 센 것이고 목표는 발행될 때 이미 수십 밀리초 묵었으므로 — 그림의 예시 주기에서는 $55\,\mathrm{ms}$ — 이 값들은 하한이다. 노출 중간점부터 세면 $N=2$도 넘을 수 있다. 해법은 깊이 $1$, 또는 정해진 나이보다 늙은 목표를 버리는 25.5의 *lifespan* 정책이다([[04-robotics/ros2/qos-executors-time|25.5 §2]]). 이 장치에서 "아무 일도 안 일어남"은 종종 이득이 아니라 TF 스탬프나 QoS다([[04-robotics/ros2/qos-executors-time|25.5]]).

### 출처

- C. Eppner, S. Höfer, R. Jonschkowski, R. Martín-Martín, A. Sieverling, V. Wall, O. Brock, "Lessons from the Amazon Picking Challenge: Four Aspects of Building Robotic Systems," *RSS 2016* (journal version: *Autonomous Robots*, 2018, DOI 10.1007/s10514-018-9761-2) — the challenge ran in 2015; the paper is 2016.

- R. A. Brooks, "A Robust Layered Control System for a Mobile Robot," *IEEE Journal of Robotics and Automation*, 2(1):14–23, 1986 — subsumption.
- N. J. Nilsson, "Shakey the Robot," SRI International Technical Note 323, 1984.
- E. Gat, "On Three-Layer Architectures," in D. Kortenkamp, R. P. Bonasso, R. Murphy (eds.), *Artificial Intelligence and Mobile Robots*, AAAI Press / MIT Press, 1998.
- A. Pnueli, "The Temporal Logic of Programs," *FOCS 1977*.
- A. Pnueli, R. Rosner, "On the Synthesis of a Reactive Module," *POPL 1989* — doubly exponential LTL synthesis.
- N. Piterman, A. Pnueli, Y. Sa'ar, "Synthesis of Reactive(1) Designs," *VMCAI 2006*, LNCS 3855 — GR(1).
- H. Kress-Gazit, G. E. Fainekos, G. J. Pappas, "Temporal-Logic-Based Reactive Mission and Motion Planning," *IEEE Transactions on Robotics*, 25(6), 2009.
- O. Maler, D. Nickovic, "Monitoring Temporal Properties of Continuous Signals," *FORMATS/FTRTFT 2004*, LNCS 3253 — signal temporal logic.
- A. Donzé, O. Maler, "Robust Satisfaction of Temporal Logic over Real-Valued Signals," *FORMATS 2010*, LNCS 6246.
- G. De Giacomo, M. Y. Vardi, "Linear Temporal Logic and Linear Dynamic Logic on Finite Traces," *IJCAI 2013* — finite-trace semantics.
- E. M. Clarke, O. Grumberg, D. Kroening, D. Peled, H. Veith, *Model Checking*, 2nd ed., MIT Press, 2018.

- [ROS 2 Concepts](https://docs.ros.org/en/rolling/Concepts.html)
- [MIT Manipulation (Tedrake) — 시스템 관련 장](https://manipulation.csail.mit.edu/)
- [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/)
