---
title: 1. Research Questions & Claims
tags: [research, claims, methodology]
study-depth: Working
wiki-support: Working
depth-goal: "Apply the procedure when forming claims, running experiments, analyzing failure, and writing."
mastery-when: "Mastery means consistently producing defensible work, not memorizing the page."
---

> [!note] Prerequisites · 선수 지식
> [[01-canonical-papers/how-to-read|How to Read Papers]] · [[02-foundations/ml-practice|ML Practice & Evaluation]] · [[02-foundations/lab-plants|0.6 Lab Plants]] (P2 and P3, which the running study names) · [[02-foundations/probability|3. Probability §6]] (p-value, confidence interval, and the tests the pilot is read with)
> [[01-canonical-papers/how-to-read|How to Read Papers]] · [[02-foundations/ml-practice|ML 실무와 평가]] · [[02-foundations/lab-plants|0.6 Lab Plants]](관통 연구가 쓰는 장치 P2, P3) · [[02-foundations/probability|3. 확률 §6]](p-값, 신뢰구간, 파일럿을 읽는 검정)

## English

*Stands on [[02-foundations/ml-practice|9. ML Practice]] and [[02-foundations/probability|3. Probability §6]]. The first page of Research Practice and the first use of **RS1** ([[06-research-practice/index|Research Practice]]), the running study every page in this section shares: here it becomes a claim, on page 2 an experiment, on page 4 a paper, and on page 6 a rung of evidence.*

A topic names an area; a research question specifies an uncertain relationship that evidence can resolve. “Apply VLA to construction” is a direction. A useful question identifies the intervention, comparator, outcome, conditions, and scope.

> [!info] Depth target
> Turn a broad interest into a falsifiable question; separate research gaps from missing implementations; and align contribution and claim strength with evidence.

> [!note] First pass · 처음이라면
> Read the running object and the worked case. They take one vague sentence about RS1 to a claim that twenty numbers can contradict, and fill the table that says which sentences those numbers license. Then read §4 (claim types) and §7 (the table in general). Sections 1–3, 5 and 6 make the same moves on other examples; come back to them when you write your own question.

### Running object · 이 페이지의 대상

**RS1 — the running study of Research Practice.** Every page in this section works on the same small study, so that a question, its design, its failures, its write-up and its claim to impact can be followed on one set of numbers. Each page restates it in full; its numbers never change.

*Question.* Does impedance control (**B**) make the planar arm's contact with a panel safer than position control with a force-threshold stop (**A**)?

*Plant* (the system being controlled). The arm is **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]]: planar 2R, unit links, a 1 kg point mass at the end of each link. The panel's stiffness is that of **P3**'s wall, $k_w = 400$ N/m.

*Trial.* One trial = the arm approaches the panel and makes contact. The recorded outcome is the trial's peak contact force in newtons, and the trial is a **success** when that peak is at most 10 N.

*Pilot.* Ten trials per controller. **The data are illustrative — invented for teaching and frozen — not a measurement of any real controller.**

| Trial | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A — position control + force-threshold stop (N) | 8.1 | 9.4 | 12.6 | 9.8 | 13.9 | 7.7 | 9.9 | 9.1 | 14.8 | 11.3 |
| B — impedance control (N) | 6.2 | 7.9 | 8.4 | 5.9 | 7.1 | 10.6 | 6.8 | 7.5 | 8.0 | 6.6 |

| Controller | Successes (peak ≤ 10 N) | Mean (N) | Sample sd (N) | Median (N) |
|---|---:|---:|---:|---:|
| A | 6/10 | 10.66 | 2.414 | 9.85 |
| B | 9/10 | 7.50 | 1.356 | 7.30 |

Trial numbers are labels within one controller: A's third trial and B's third trial share nothing, so every comparison below is unpaired. The comparison statistics this page and the later ones use, all recomputed from these twenty numbers: difference of means $10.66 - 7.50 = 3.16$ N, Welch standard error $0.8756$ N, and $t = 3.609$ on $14.16$ degrees of freedom. Which test fits which outcome is [[02-foundations/probability|3. Probability §6]]; the arithmetic on RS1 is [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]]'s worked case.

What RS1 leaves unfixed on purpose: B's target impedance, A's stop threshold, the approach speed and direction. A real study must state all of them. This page uses their absence as the first thing a vague claim hides.

*Scope: this page teaches how to turn RS1 from a topic into a falsifiable, scoped claim, and how to fill the claim–evidence table that says which sentences the pilot licenses. It does not teach how many trials the confirmatory run needs or how to assign and randomize them ([[06-research-practice/experimental-design-reproducibility|2. Experimental Design]]), how to derive the tests ([[02-foundations/probability|3. Probability §6]]), how to write the result up ([[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]]), or which rung of deployment evidence it reaches ([[06-research-practice/real-world-impact|6. Real-World Impact]]).*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 590" style="max-width:100%;height:auto" role="img" aria-label="Two panels: the vague draft and the rewritten RS1 claim with their scope, intervention, comparator, outcome and withdrawal brackets, and RS1's twenty pilot peaks on a force axis with the 10 N line fixed before the pilot and the 9 to 10 N band shaded">
  <text x="16" y="22" font-size="12.5" fill="currentColor"><tspan font-weight="bold">1</tspan><tspan dx="7">The claim’s anatomy</tspan></text>
  <text x="16" y="44" font-size="11" font-style="italic" opacity="0.7" fill="currentColor">Draft (worked case, Step 1)</text>
  <text x="16" y="64" font-size="12" textLength="98.4" lengthAdjust="spacing" fill="currentColor">impedance control</text>
  <text x="117.8" y="64" font-size="12" textLength="35.4" lengthAdjust="spacing" fill="currentColor">makes</text>
  <text x="156.5" y="64" font-size="12" textLength="69.7" lengthAdjust="spacing" fill="currentColor">robot contact</text>
  <text x="229.6" y="64" font-size="12" textLength="26.8" lengthAdjust="spacing" fill="currentColor">safer</text>
  <path d="M16 68 V72 H114.4 V68 M65.2 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="16" y="91" font-size="11" fill="currentColor">I · only a family name</text>
  <path d="M156.5 68 V72 H226.2 V68 M191.4 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="191.4" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="191.4" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">S</text>
  <path d="M229.6 68 V72 H256.4 V68 M243 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="243" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="243" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">Y</text>
  <line x1="304" y1="64" x2="360" y2="64" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="1 3"/>
  <path d="M300 68 V72 H364 V68 M332 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="332" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="332" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">C</text>
  <line x1="396" y1="64" x2="452" y2="64" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="1 3"/>
  <path d="M392 68 V72 H456 V68 M424 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="424" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="424" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">R</text>
  <text x="548" y="91" font-size="11" text-anchor="end" opacity="0.7" fill="currentColor">dashed = left empty</text>
  <text x="16" y="117" font-size="11" font-style="italic" opacity="0.7" fill="currentColor">Rewritten claim (worked case, Step 3)</text>
  <text x="16" y="137" font-size="11.5" textLength="487.4" lengthAdjust="spacing" fill="currentColor">On the planar arm P2 approaching and contacting a 400 N/m panel under the RS1 trial protocol</text>
  <path d="M16 141 V145 H503.4 V141 M259.7 145 V148.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="259.7" y="161" font-size="11" text-anchor="middle" fill="currentColor">S · scope: P2, the 400 N/m panel, the RS1 trial</text>
  <text x="16" y="182" font-size="11.5" textLength="419.8" lengthAdjust="spacing" fill="currentColor">— with B’s target impedance and A’s stop threshold as reported in the methods —</text>
  <text x="16" y="202" font-size="11.5" textLength="112.8" lengthAdjust="spacing" fill="currentColor">impedance control (B)</text>
  <text x="132" y="202" font-size="11.5" textLength="47.5" lengthAdjust="spacing" fill="currentColor">produces</text>
  <text x="182.8" y="202" font-size="11.5" textLength="166.9" lengthAdjust="spacing" fill="currentColor">a lower mean peak contact force</text>
  <path d="M16 206 V210 H128.8 V206 M72.4 210 V213.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="72.4" y="226" font-size="11" text-anchor="middle" fill="currentColor">I · intervention: B</text>
  <path d="M182.8 206 V210 H349.6 V206 M266.2 210 V213.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="266.2" y="226" font-size="11" text-anchor="middle" fill="currentColor">Y · outcome: peak contact force, N</text>
  <text x="16" y="247" font-size="11.5" textLength="22.5" lengthAdjust="spacing" fill="currentColor">than</text>
  <text x="41.8" y="247" font-size="11.5" textLength="234.7" lengthAdjust="spacing" fill="currentColor">position control with a force-threshold stop (A)</text>
  <text x="276.5" y="247" font-size="11.5" textLength="3.2" lengthAdjust="spacing" fill="currentColor">.</text>
  <path d="M41.8 251 V255 H276.5 V251 M159.1 255 V258.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="159.1" y="271" font-size="11" text-anchor="middle" fill="currentColor">C · comparator: A</text>
  <text x="16" y="292" font-size="11.5" textLength="105.9" lengthAdjust="spacing" fill="currentColor">Secondary outcome:</text>
  <text x="125.1" y="292" font-size="11.5" textLength="261.2" lengthAdjust="spacing" fill="currentColor">a larger share of B’s contacts stay at or below 10 N</text>
  <text x="386.3" y="292" font-size="11.5" textLength="3.2" lengthAdjust="spacing" fill="currentColor">.</text>
  <path d="M125.1 296 V300 H386.3 V296 M255.7 300 V303.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="255.7" y="316" font-size="11" text-anchor="middle" fill="currentColor">Y · secondary outcome: success at ≤ 10 N</text>
  <path d="M16 327 V331 H503.4 V327 M259.7 331 V334.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="259.7" y="348" font-size="11" text-anchor="middle" fill="currentColor">R · withdrawn if the Welch 95% CI for μ<tspan dy="3" font-size="9.5">A</tspan><tspan dx="3.1" dy="-3">− μ</tspan><tspan dy="3" font-size="9.5">B</tspan><tspan dx="3.1" dy="-3">does not lie entirely above 0;</tspan></text>
  <text x="259.7" y="363" font-size="11" text-anchor="middle" fill="currentColor">the secondary claim, if Fisher’s exact test does not reject at α = 0.05, two-sided</text>
  <line x1="16" y1="381" x2="544" y2="381" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="16" y="403" font-size="12.5" fill="currentColor"><tspan font-weight="bold">2</tspan><tspan dx="7">The operational definition, drawn</tspan></text>
  <rect x="268" y="425" width="44" height="80" fill="currentColor" fill-opacity="0.13"/>
  <line x1="92" y1="505" x2="532" y2="505" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M92 505V510 M136 505V510 M180 505V510 M224 505V510 M268 505V510 M312 505V510 M356 505V510 M400 505V510 M444 505V510 M488 505V510 M532 505V510" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="92" y="523" font-size="11" text-anchor="middle" fill="currentColor">5</text>
  <text x="136" y="523" font-size="11" text-anchor="middle" fill="currentColor">6</text>
  <text x="180" y="523" font-size="11" text-anchor="middle" fill="currentColor">7</text>
  <text x="224" y="523" font-size="11" text-anchor="middle" fill="currentColor">8</text>
  <text x="268" y="523" font-size="11" text-anchor="middle" fill="currentColor">9</text>
  <text x="312" y="523" font-size="11" text-anchor="middle" fill="currentColor">10</text>
  <text x="356" y="523" font-size="11" text-anchor="middle" fill="currentColor">11</text>
  <text x="400" y="523" font-size="11" text-anchor="middle" fill="currentColor">12</text>
  <text x="444" y="523" font-size="11" text-anchor="middle" fill="currentColor">13</text>
  <text x="488" y="523" font-size="11" text-anchor="middle" fill="currentColor">14</text>
  <text x="532" y="523" font-size="11" text-anchor="middle" fill="currentColor">15</text>
  <text x="312" y="540" font-size="11" text-anchor="middle" fill="currentColor">peak contact force per trial (N)</text>
  <line x1="312" y1="415" x2="312" y2="505" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="318" y="423" font-size="11" fill="currentColor">10 N, fixed before the pilot</text>
  <circle cx="210.8" cy="443" r="4" fill="currentColor"/>
  <circle cx="228.4" cy="443" r="4" fill="currentColor"/>
  <circle cx="272.4" cy="443" r="4" fill="currentColor"/>
  <circle cx="285.6" cy="443" r="4" fill="currentColor"/>
  <circle cx="303.2" cy="438" r="4" fill="currentColor"/>
  <circle cx="307.6" cy="448" r="4" fill="currentColor"/>
  <circle cx="369.2" cy="443" r="4" fill="currentColor"/>
  <circle cx="426.4" cy="443" r="4" fill="currentColor"/>
  <circle cx="483.6" cy="443" r="4" fill="currentColor"/>
  <circle cx="523.2" cy="443" r="4" fill="currentColor"/>
  <circle cx="131.6" cy="479" r="4" fill="currentColor"/>
  <circle cx="144.8" cy="479" r="4" fill="currentColor"/>
  <circle cx="162.4" cy="479" r="4" fill="currentColor"/>
  <circle cx="171.2" cy="479" r="4" fill="currentColor"/>
  <circle cx="184.4" cy="479" r="4" fill="currentColor"/>
  <circle cx="202" cy="479" r="4" fill="currentColor"/>
  <circle cx="219.6" cy="474" r="4" fill="currentColor"/>
  <circle cx="224" cy="484" r="4" fill="currentColor"/>
  <circle cx="241.6" cy="479" r="4" fill="currentColor"/>
  <circle cx="338.4" cy="479" r="4" fill="currentColor"/>
  <text x="20" y="447" font-size="12.5" font-weight="bold" fill="currentColor">A</text>
  <text x="20" y="483" font-size="12.5" font-weight="bold" fill="currentColor">B</text>
  <text x="38" y="447" font-size="12" fill="currentColor">6/10</text>
  <text x="38" y="483" font-size="12" fill="currentColor">9/10</text>
  <text x="38" y="423" font-size="11" opacity="0.7" fill="currentColor">≤ 10 N</text>
  <text x="16" y="563" font-size="11" opacity="0.9" fill="currentColor">Shaded: the 9–10 N band. Four of A’s peaks sit in it (9.1, 9.4, 9.8, 9.9),</text>
  <text x="16" y="578" font-size="11" opacity="0.9" fill="currentColor">so the verdict moves when the line moves: the line is part of the claim.</text>
</svg>

Panel 1 brackets RS1's claim from below with its scope S, intervention I, comparator C, outcome Y and the rule R that would withdraw it: the vague draft "impedance control makes robot contact safer" fills only I, and that only with a family name, while the worked case's rewritten claim fills all five. Panel 2 draws the operational definition — the twenty pilot peaks on a force axis from 5 to 15 N, with the 10 N line fixed before the pilot, A at 6/10 and B at 9/10. Four of A's peaks, 9.1, 9.4, 9.8 and 9.9 N, sit in the shaded 9–10 N band, so the verdict moves when the line moves: the line is part of the claim.

### Worked case · 대상으로 한 번 끝까지

Five steps on RS1: from a sentence no result could contradict, to a claim that twenty numbers can test, to the table that says which sentences those numbers license.

**Step 1 — the vague claim, and the slots it leaves empty.** A first draft of RS1's abstract says: *"Impedance control makes robot contact safer."* Read it against the things a research question has to name.

> [!info] Definition — research question
> **What kind of thing it is:** a question about a relationship whose answer is uncertain before the evidence and settled by it. **Defining conditions — all five:** it names (1) the **scope** $S$, the embodiment, environment, task and population it is asked about; (2) the **intervention** $I$; (3) the **comparator** $C$, matched to $I$ on everything except the factor under test; (4) the **outcome** $Y$, with an operational definition (Step 2); and (5) it can be answered **no**, because some possible value of $Y$ would mean the intervention did not help. As a tuple,
> $$Q = (S,\ I,\ C,\ Y), \qquad \text{with at least one possible result that answers } Q \text{ negatively}$$
> so a question is a comparison of $Y$ under $I$ with $Y$ under $C$, inside $S$. Clinical research calls the same slots PICO: population, intervention, comparison, outcome (Richardson et al. 1995).
> **Example.** "On P2 approaching a 400 N/m panel under the RS1 trial, does impedance control (B) give a lower peak contact force than position control with a force-threshold stop (A)?"
> **Non-example.** "Impedance control for safe contact" names an $I$ and nothing else. It is a topic, and no result could answer it.
> **Why it matters.** Each empty slot is a part of the experiment that cannot yet be designed: without $C$ there is no baseline to run, without $Y$ nothing to record, and without $S$ no way to say where the answer stops applying.

Against those slots the draft fills one, and fills it with the name of a family:

| Slot | What the draft says | What is missing |
|---|---|---|
| $S$, scope | "robot contact" | which arm, which surface, which approach |
| $I$, intervention | "impedance control" | *which* impedance: the claim is about one target stiffness and damping, and RS1 has not stated them |
| $C$, comparator | — | safer *than what* |
| $Y$, outcome | "safer" | a measurement |
| answerable "no" | — | a result that would count against it |

**Step 2 — give "safer" an operational definition.** RS1 already carries one: record each trial's peak contact force, and call the trial a success when that peak is at most 10 N.

> [!info] Definition — operational definition
> **What kind of thing it is:** a measurement rule, a procedure that maps each trial to a value of the outcome so that two people applying it to the same trial record the same value. **Defining conditions:** it names (1) the signal and the instrument that records it, (2) the time window and the aggregation over it, (3) the unit, (4) the threshold, if the outcome is cut into success and failure, and (5) it is fixed **before** the data it will be applied to. For RS1,
> $$Y_i = \max_{t \in W_i} F_i(t), \qquad S_i = \mathbb{1}\big[\,Y_i \le 10\ \text{N}\,\big]$$
> where $F_i(t)$ is the contact force of trial $i$ at time $t$, $W_i$ is its contact window, $Y_i$ its peak force in newtons, $S_i$ its success indicator, and $\mathbb{1}[\cdot]$ equals 1 when the bracket holds and 0 otherwise, so every trial yields one number and one bit.
> **Example.** A's seventh trial peaks at $Y = 9.9$ N, so $S = 1$; its tenth peaks at $11.3$ N, so $S = 0$.
> **Non-example.** The same rule with the line drawn after the dots were seen: the table below.
> **Why it matters.** A claim's verdict is a function of its definition. Move the line and a different claim is being tested, even though the word "safer" has not changed.

The non-example in numbers. Four of A's ten peaks sit just under the line, between 9 and 10 N (9.1, 9.4, 9.8, 9.9), so RS1's counts are unusually sensitive to where it is drawn:

| Line drawn at | A successes | B successes | Gap | Fisher exact $p$ |
|---|---:|---:|---:|---:|
| 9 N | 2/10 | 9/10 | 0.7 | 0.005 |
| **10 N, fixed before the pilot** | **6/10** | **9/10** | **0.3** | **0.30** |
| 12 N | 7/10 | 10/10 | 0.3 | 0.21 |

Not one measurement differs between the rows. An analyst who drew the line after looking could report $p = 0.005$ from the same twenty trials that give $p = 0.30$ at the prespecified 10 N. That is why condition (5) belongs to the definition rather than to good manners: undisclosed choices made after seeing the data can make almost any comparison look significant (Simmons, Nelson & Simonsohn 2011). Fisher's exact test is the choice of [[02-foundations/probability|3. Probability §6]] for two unpaired success counts; its arithmetic on RS1 is worked in [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]].

**Step 3 — the rewritten claim, and the rule that would withdraw it.**

> *On the planar arm P2 approaching and contacting a 400 N/m panel under the RS1 trial protocol — with B's target impedance and A's stop threshold as reported in the methods — impedance control (B) produces a lower mean peak contact force than position control with a force-threshold stop (A). Secondary outcome: a larger share of B's contacts stay at or below 10 N.*

The rule, written down before the confirmatory run: *the primary claim is withdrawn if the Welch 95% confidence interval for $\mu_A - \mu_B$, the difference of the two mean peak forces, does not lie entirely above zero; the secondary claim is withdrawn if Fisher's exact test does not reject equal success probabilities at $\alpha = 0.05$, two-sided.* Peak force is primary because it keeps each trial's distance from the line, where the success count keeps only its side; what that choice costs in trials is the worked case of [[06-research-practice/real-world-impact|6. Real-World Impact]].

> [!info] Definition — falsifiable claim
> **What kind of thing it is:** a statement about a research question $(S, I, C, Y)$, paired with a planned measurement and a rule for when its author gives it up. **Defining conditions — all four:** (1) its outcome has an operational definition; (2) it names the set $R$ of possible results that would **withdraw** it; (3) $R$ is **not empty**, so at least one result the measurement can produce contradicts the claim; (4) $R$ is fixed **before** the result is seen.
> $$R \subseteq \Omega, \qquad R \neq \varnothing, \qquad \text{the claim is withdrawn} \iff o \in R$$
> where $\Omega$ is the set of results the planned measurement can produce and $o$ is the one it does produce, so the claim is at risk exactly when $R$ is not empty. The idea is Popper's: a statement says something about the world only by forbidding some outcomes.
> **Example.** Step 3's primary claim, with $R$ = "the Welch 95% CI for $\mu_A - \mu_B$ does not lie entirely above zero".
> **Non-example.** "Impedance control makes contact safer" has $R = \varnothing$: any outcome can be absorbed ("safety is more than force"). The 9 N row of Step 2 fails the other way. Its $R$ is not empty, but it was chosen after $o$ was seen, so it forbids nothing that had not already failed to happen.
> **Why it matters.** A claim that forbids nothing cannot be supported either, since no result would have counted against it. And a nonempty $R$ is not yet a strong test: how likely the measurement is to stay outside $R$ when the claim is true is the power of the test ([[02-foundations/probability|3. Probability §6]]), and the number of trials sets it.

That last point is concrete for RS1. Even if B's true success probability really is 0.9 against A's 0.6, ten trials per arm give the success comparison only about a one-in-three chance of clearing its rule by the normal approximation, and about one in seven for the exact test the rule actually names ([[06-research-practice/real-world-impact|6. Real-World Impact]] derives both). Tested that way, a true secondary claim would usually be withdrawn.

**Step 4 — fill the claim–evidence table with the pilot's numbers.** The table of §7, one row for each claim a draft might make about RS1, with three more columns: the claim type of §4, the pilot's evidence, and a verdict. The two intervals and both p-values are computed in [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]]'s worked case.

| Intended claim | Type (§4) | Necessary comparison | Metric | Boundary | Pilot evidence (10 per arm) | Verdict |
|---|---|---|---|---|---|---|
| B stayed at or below 10 N in 9 of 10 pilot trials | descriptive | none | count $k/n$ | these ten trials | 9/10 | licensed as written |
| B's mean peak force is lower than A's | comparative | A against B, same arm, panel and trial | $\bar y_A - \bar y_B$ in N, Welch 95% CI | P2, 400 N/m, RS1 trial | $3.16$ N, CI $[1.28,\ 5.04]$; $t = 3.61$ on $14.2$ df, $p = 0.003$ | licensed for this pilot, inside the boundary |
| B succeeds more often than A | comparative | the same | difference of success proportions, its 95% CI, Fisher exact test | the same | $0.90$ against $0.60$: $+0.30$, CI $[-0.08,\ 0.60]$; $p = 0.30$ | not licensed: the pilot cannot tell them apart |
| B is safer than A | safety / reliability | hazard definition, exposure, severity, supervision | exceedances and near misses per unit exposure | not certification | one force proxy on 20 trials | not licensed |
| B's advantage holds on stiffer panels | generalization | the same comparison across panel stiffnesses | difference per stiffness | a named stiffness range | none: one panel | untested, and the physics changes |
| B is gentler because its compliance absorbs the impact | mechanistic | force–time traces; the same controller with its target stiffness changed | impact duration, energy absorbed | — | peak values only | not licensed |

Two rows carry the lesson.

*Row 3 against row 2.* The gap between 9/10 and 6/10 looks large, and it is the row most drafts would lead with. Yet if the two success probabilities were equal, a split at least this uneven among the fifteen successes would still arise with probability $0.30$. The same twenty trials support row 2 at $p = 0.003$ for two reasons. The mean uses every trial's distance from the line, while the count uses only the side of the line each trial fell on; and four of A's peaks sit just under the line, where the count scores them as successes, so the counts show a smaller gap than the forces do. [[06-research-practice/real-world-impact|6. Real-World Impact]] separates the two reasons in trials.

*Row 5's boundary.* The boundary column is not modesty. Under the half-sine contact model of [[04-robotics/force-compliance-control|13. Force & Compliance Control]], for an approach along $y$ at P2's frozen pose, where the apparent mass is $\Lambda_y = 2$ kg, the contact lasts

$$t_c = \pi\sqrt{\Lambda_y / k}$$

because tool and panel act as a mass on a spring and contact ends after half a period. That is $\pi\sqrt{2/400} = 0.222$ s against RS1's panel and $\pi\sqrt{2/10^5} = 0.014$ s against a $10^5$ N/m structure. A controller with two tenths of a second to shape the impact faces a different problem from one with fourteen milliseconds, so the soft-panel result says nothing about a stiff panel until a stiff panel is tested.

**Step 5 — the sentence the pilot licenses.** Reading the licensed rows together:

> In a ten-trial-per-arm pilot on the P2 arm against a 400 N/m panel, B's mean peak contact force was 3.16 N lower than A's (95% CI 1.28 to 5.04 N); B stayed at or below 10 N in 9 of 10 trials and A in 6 of 10, a difference this pilot cannot distinguish from chance (95% CI $-0.08$ to $+0.60$; Fisher exact $p = 0.30$).

Every clause has a row, and every row it leaves out — safer, stiffer panels, the mechanism — is left out on purpose. That sentence is what the next pages take: [[06-research-practice/experimental-design-reproducibility|2. Experimental Design]] decides how the confirmatory run is assigned and sized, [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]] turns each number into a table cell and the sentence it licenses, and [[06-research-practice/real-world-impact|6. Real-World Impact]] asks which rung of evidence the pilot stands on and what the next rung costs. What the sentence should not do is go to an archival venue on its own ahead of the confirmatory run: pilot and confirmation are one claim, and [[06-research-practice/venue-strategy|5. Venue Strategy]]'s worked case shows the journal rules then refusing the second as a mere extension of the first.

### 1. Topic → problem → question

| Level | Example |
|---|---|
| Topic | VLA for construction manipulation |
| Problem | scarce demonstrations limit adaptation to new material layouts |
| Question | Under a fixed demonstration budget, does action-chunk fine-tuning of a pretrained VLA improve closed-loop success on held-out layouts over vision-only behavior cloning? |

The final question states a condition, intervention, comparator, outcome, and test distribution. It can be answered negatively.

**Before:** “We study construction manipulation.” **Problem:** an area does not identify an assumption that can fail. **After:** “Factory grasp planners often rely on an assumed friction coefficient μ; wet or dusty site surfaces can violate that assumption.” This turns a topic into a specific mismatch between a model and its operating conditions.

**Before:** “We will add touch to solve the mismatch.” **Problem:** installing a sensor is an intervention, not an answerable question. **After:** “When the assumed μ is wrong, how much does estimating friction from touch during contact recover lost grasp success, compared with the same planner using fixed μ?”

**The reading this gives you.** Follow the chain from surface condition to model error to a measurable outcome. Define how friction mismatch is established and keep the grasp planner comparable. A negative answer is informative: it could show that the available contact observations do not arrive early enough to change the grasp decision.

The worked case makes the same move on RS1, from "impedance control makes robot contact safer" to a question with every slot filled and a claim with a rule that would withdraw it.

### 2. A gap is not merely “nobody has done this”

A defensible gap may be an unexplained failure, incompatible assumptions, missing evidence, poor generalization, unrealistic evaluation, or a theoretically/operationally important trade-off. Adding a model to a new dataset is an engineering activity unless it tests a consequential question.

A gap needs a reason why the missing evidence matters. “Nobody has attached a VLA to this excavator” could reflect an uninteresting port, unavailable hardware, or a difficult unsolved assumption. Those possibilities imply very different research projects, even though the novelty sentence sounds identical.

For example, a policy trained on visual demonstrations may not observe changing material resistance before the bucket commits to a motion. The consequential gap is whether the available observations support timely adaptation under that hidden variation. Testing a VLA on the machine becomes useful when the experiment can distinguish this information limitation from an implementation failure or a poor action interface.

**The reading this gives you.** Look for the bridge between missing work and a predicted failure mechanism. Ask what the existing method assumes, which site condition breaks it, and what observation would resolve the uncertainty. A credible gap survives even if another group has already built a superficially similar system.

### 3. Hypotheses and contributions

- **Hypothesis:** expected relationship that can be tested.
- **Engineering objective:** system capability to build.
- **Scientific contribution:** new knowledge supported by evidence.
- **System contribution:** integration or capability whose novelty may lie in architecture, deployment, or evaluation.
- **Artifact contribution:** useful code, dataset, benchmark, or platform.

A project can contribute a system without inventing a new algorithm, but must identify what knowledge or capability the system establishes beyond assembly effort.

**Before:** “Our contribution is a tactile sensor.” **Problem:** a component name does not specify what knowledge or capability was established. **After:** “We provide a contact-state estimation interface and evaluate whether its updates recover grasp performance under friction mismatch.” The artifact and its scientific question now have separate jobs.

**Before:** “We hypothesize that our system is novel and useful.” **Problem:** novelty is a relation to prior work, and usefulness has no defined outcome here. **After:** “We predict that contact-time friction updates reduce failures associated with incorrect assumed μ, under a matched grasping protocol.”

These are proposed statements, not results. The contribution sentence must eventually say what the evidence supports, including a narrower outcome if the prediction fails. **The reading this gives you.** Check whether the claimed contribution is an artifact, an observed relationship, or a capability, and whether the paper supplies the corresponding evidence.

### 4. Claim types

| Claim | Required caution |
|---|---|
| Descriptive | claims must stay within the studied sample |
| Comparative | performance relative to a defined baseline and setting |
| Causal | alternative explanations must be controlled or modeled |
| Generalization | target distribution and shift must be defined |
| Mechanistic | evidence must isolate why the method works |
| Safety/reliability | exposure, severity, rare failures, and system boundaries matter |

In the last row, **exposure** means how much operating time, distance, or how many trials could have produced the failure: zero collisions in 10 trials and zero collisions in 10,000 trials are very different evidence.

“Performance drops when component X is removed” supports a scoped dependency; it does not prove the author's complete causal story.

**Before:** “Touch explains the improvement because the full system scored higher.” **Problem:** a comparative result does not isolate a mechanism when training data or control logic also changed. **After:** “The complete system outperformed the baseline in the tested conditions; a matched tactile ablation is needed to attribute the difference to touch.”

**Before:** “The robot is safe because no collision occurred.” **Problem:** a sample outcome omits exposure and the role of supervision. **After:** “No collision was observed under the stated trial and intervention protocol; this supports a bounded observation about the tested system.”

These hypothetical rewrites preserve the observation while reducing the inferred claim. **The reading this gives you.** Underline the verb: describes, exceeds, causes, transfers, or prevents. Then ask whether the comparison and sampling procedure can actually support that kind of statement.

The worked case gives every row of this table an RS1 instance, with the pilot's evidence beside it and a verdict: only the descriptive row and the peak-force comparison survive twenty trials.

### 5. Scope and assumptions

Write the population, environment, embodiment, sensors, data regime, task, intervention policy, and evaluation horizon. Assumptions are not weaknesses by default; hidden assumptions are.

Scope makes the experiment interpretable because the same intervention can answer different questions under different conditions. A friction estimator evaluated on familiar dry objects tests adaptation within a known regime. Evaluation on held-out wet surfaces tests a different boundary, even if the task and success metric keep the same names.

For the tactile grasping question, record material preparation, how friction mismatch is induced or verified, the contact observations available before action, and what the operator may change. Also state whether grasp geometry and object identity appeared in training. A policy can exploit those cues without estimating friction, so an apparently successful test may support a narrower explanation than intended.

**The reading this gives you.** Try completing the sentence “This result applies when…”. Each missing condition is a question for the methods section. Separate an explicit simplification from an untested transfer claim; knowing the model's boundary is what lets a later study deliberately move it.

### 6. Worked rewrite

Weak: **Can world models improve construction robots?**

Stronger: **For autonomous excavation in variable soil, does a learned latent dynamics model reduce bucket-path tracking error and recovery interventions relative to model-free behavior cloning when both use the same demonstrations and MPC safety constraints?**

(MPC is model predictive control, which re-solves a short-horizon constrained optimization every cycle; see [[04-robotics/mpc|MPC]].) This still needs operational definitions for soil variation, intervention, and the world-model planning procedure. The worked case defines the term in full on RS1's success rule, and shows what moving one threshold does to a verdict.

**Before, as a proposed abstract:** “Construction robots need robust manipulation. We introduce a tactile intelligence framework for reliable grasping in challenging environments.” It names a motivation and a tool, but a reader cannot identify the assumption being tested or imagine a result that would contradict the promise.

**After, as a proposed abstract:** “Grasp planners that assume known friction may lose success when site surfaces become wet or dusty. We ask whether estimating μ from tactile observations during contact recovers this loss relative to the same planner using fixed μ. We compare the conditions under matched objects, sensing opportunities, and intervention rules, with held-out surface conditions. We report grasp success, recovery behavior, and estimation timing. The experiment tests whether the observed contact information is useful before the grasp decision; it does not establish general construction autonomy.”

This is a study proposal, so it intentionally contains no invented result. After testing, replace the reporting intention with the measured outcome and uncertainty. The strongest final sentence must follow that outcome, including a negative one.

### 7. Claim–evidence table

Before experiments, make this table:

| Intended claim | Necessary comparison | Metric | Boundary |
|---|---|---|---|
| better data efficiency | same model/evaluation at several data budgets | learning curve and uncertainty | tested tasks/layouts only |
| better recovery | matched failure perturbations | recovery success/time | specified failure types |
| safer operation | comparable exposure and hazard definitions | violations, near misses, severity | not certification |

**Before:** “Claim: robust grasping; evidence: a successful video.” **Problem:** neither variation nor the denominator is visible. **After:** “Claim: improved recovery under specified surface shifts; evidence: matched attempts, failure records, and uncertainty for each held-out condition.”

**Before:** “Claim: tactile friction estimation is the cause; evidence: full model versus the old system.” **Problem:** the systems differ along uncontrolled axes. **After:** “Claim: benefit from contact-time updates; evidence: the same planner with updates enabled or disabled, matched sensing and compute, plus diagnostics linking updates to decisions.”

Use the table before data collection to discover evidence you cannot currently obtain. **The reading this gives you.** A missing comparison is a design decision: add it, narrow the claim, or leave that question explicitly unanswered. Filling the table after writing can hide this choice behind an attractive but irrelevant metric.

The worked case fills this table for RS1, with three more columns — the claim type, the pilot's evidence and a verdict — so that the rows the pilot cannot fill are visible before anyone writes the abstract.

### After reading

- Convert a topic into a falsifiable question.
- Explain why absence of prior implementation is not automatically a research gap.
- Distinguish hypothesis, engineering objective, and contribution.
- Match claim type to the evidence it requires.
- State scope and assumptions before using words such as robust or general.
- Rewrite a vague claim about RS1 as a falsifiable one, with its withdrawal rule, and fill its claim–evidence table from the pilot.
- Explain why an operational definition, threshold included, must be fixed before the data.

### Self-check

1. Rewrite “Does diffusion help robot planning?” as a testable question.
2. Why can a larger benchmark score fail to establish the claimed mechanism?
3. What would falsify a data-efficiency claim?
4. RS1's pilot gives $p = 0.003$ for the difference in mean peak force. Why does that not license "B is safer"?
5. RS1's success line sits at 10 N. Why must it have been drawn before the pilot, and what does the table in Step 2 of the worked case show happens if it was not?

> [!tip]- Answers
> 1. Specify task/distribution, diffusion intervention, matched comparator, data budgets, metric, and closed-loop conditions. 2. Several components or data changes may differ; score alone does not isolate cause. 3. No advantage across predeclared low-data budgets under matched compute/model/evaluation, or an advantage explained by unequal data or tuning. 4. The p-value is about one proxy outcome, peak force, on one arm, one panel and twenty trials. "Safer" is a safety claim, which §4 says needs a hazard definition, exposure, severity and the role of supervision; and a p-value is neither the size of an effect nor the probability that B is better ([[02-foundations/probability|3. Probability §6]]). What $p = 0.003$ licenses is row 2 of the table: B's mean peak force was lower in this pilot, by 3.16 N (95% CI 1.28 to 5.04 N). 5. The line is part of the claim's operational definition, so drawing it after the data lets the data choose the claim. The same twenty trials give Fisher $p = 0.30$ at the prespecified 10 N and $p = 0.005$ at 9 N, because four of A's peaks sit between 9 and 10 N; a line chosen after looking forbids nothing that had not already failed to happen.

### Problem set · 과제

Tier B. Hand work on RS1, using only this page, its prerequisites and the pilot frozen in the running object. A different claim from the worked case: the worked case tested means with the line at 10 N; these items move the line, and then test a claim with no line at all.

1. **Draw.** Redraw the second panel of the picture above with the success line at 12 N instead of 10 N. Count each row's successes and circle every dot whose category changed. Then redraw the claim's anatomy for the secondary claim under this definition. Which bracket changed, and which stayed the same?
2. **Derive.** A co-author proposes a claim with no threshold: "a B contact is gentler than an A contact". (a) Rewrite it as a falsifiable claim about $\theta = P(Y_A > Y_B)$, the probability that a randomly chosen A trial peaks higher than a randomly chosen B trial, naming $S$, $I$, $C$, $Y$ and a withdrawal rule. (b) Estimate $\theta$ from the pilot by counting, over all $10 \times 10$ cross pairs, how often A's peak is the higher one. (c) Which value of $\theta$ means "no difference", and why does this claim not depend on where any line is drawn?
3. **Interpret.** A draft abstract reads: "Impedance control eliminates excessive contact forces." (a) Which claim type of §4 is it, and exactly which result would it forbid, if "excessive" means RS1's 10 N? (b) Does the pilot support it, fail to support it, or contradict it? (c) Write the strongest sentence about excessive forces that the pilot does license, and say what a reliability version of the claim ("B exceeds 10 N in fewer than 10% of contacts") would need.

> [!note]- How to draw it · 그리는 법
> - **The operational definition on one axis:** a horizontal force axis from 5 to 15 N, A's ten peaks as dots on one row and B's ten on the row below. The dots never move; only the line does.
> - **The line comes first:** draw the success line and label it before placing a single dot, because the line is part of the claim — the worked case's reads *10 N, fixed before the pilot*.
> - **Each row's count, written left of the line** — 6/10 and 9/10 in the worked case.
> - **Mark where the verdict is fragile:** the worked case shades the 9–10 N band, which holds four of A's peaks (9.1, 9.4, 9.8, 9.9); move the line across it and the verdict moves.
> - **The claim's anatomy:** write the claim across the page and bracket its phrases from below — S (scope), I (intervention), C (comparator), Y (outcome, with its threshold) — and put a fifth bracket, R, under the whole sentence for the result that would withdraw it.
> - **Leave empty every bracket a phrase does not pin down:** the vague draft's "robot contact" and "safer" leave S and Y empty, and it has no C or R at all.

> [!tip]- Solutions
> 1. At 12 N, A's successes are 8.1, 9.4, 9.8, 7.7, 9.9, 9.1 and 11.3, so 7/10, and all ten of B's peaks are below the line, so 10/10. Circle A's 11.3 and B's 10.6: they are the only dots that change category. In the anatomy, S, I and C are untouched; the Y bracket changed, because the threshold is part of the outcome's operational definition, and R changed with it, because the withdrawal rule is stated on Y. So "success at 12 N" is a different claim from "success at 10 N". Since 10 N was fixed before the pilot, the 12 N version may be reported only as a labelled sensitivity analysis beside the prespecified result, never in its place.
> 2. (a) "On P2 approaching a 400 N/m panel under the RS1 trial, an A contact peaks higher than a B contact more often than not: $\theta = P(Y_A > Y_B) > 0.5$." S, I and C are those of the worked case; Y is still the peak force, now compared across pairs of trials rather than against a line. Withdrawal rule, fixed before the confirmatory run: withdraw the claim if a two-sided Mann–Whitney test of $\theta = 0.5$ ([[02-foundations/probability|3. Probability §6]]) does not reject at $\alpha = 0.05$. (b) Sort both rows. B's six lowest peaks (5.9, 6.2, 6.6, 6.8, 7.1, 7.5) lie below all ten of A's, giving $6 \times 10 = 60$ pairs; B's 7.9 and 8.0 lie below nine of A's (only A's 7.7 is lower), giving 18; B's 8.4 lies below eight (A's 7.7 and 8.1 are lower), giving 8; B's 10.6 lies below four (11.3, 12.6, 13.9, 14.8), giving 4. There are no ties, so $\hat\theta = (60 + 18 + 8 + 4)/100 = 90/100 = 0.90$. (c) $\theta = 0.5$: an A trial is as likely to peak lower as higher. The claim uses only the order of the peaks, so moving a success line anywhere leaves all hundred pair comparisons unchanged. It is the same pair-counting quantity as the AUC of [[02-foundations/ml-practice|9. ML Practice]]'s worked case, with A's peaks in the role of the positives.
> 3. (a) A safety/reliability claim, and a universal one: "eliminates" forbids any B contact above 10 N, so a single such contact contradicts it. (b) It is contradicted. B's sixth trial peaked at 10.6 N. The claim was falsifiable, and the pilot falsified it. (c) "In the pilot, peaks above 10 N fell from 4 of 10 trials under A to 1 of 10 under B" is licensed, as a descriptive count (row 1 of the worked case's table). The comparative version, "B exceeds 10 N less often", is row 3 and is not licensed at $p = 0.30$. A reliability version needs exposure: if B truly exceeded 10 N in 10% of contacts, $n$ contacts would all stay below the line with probability $0.9^n$, and that falls to 0.05 only at $n = \ln 0.05 / \ln 0.9 = 28.4$. So B would need 29 contacts with no exceedance at all before the 95% upper bound on its exceedance rate drops below 10%. Allowing one exceedance, as the pilot already has, raises the count to 46, the smallest $n$ with $0.9^n + n(0.1)(0.9)^{n-1} \le 0.05$ (it is $0.048$ at 46 and $0.052$ at 45).

### Sources

- [DARPA — the Heilmeier Catechism](https://www.darpa.mil/about/heilmeier-catechism) — the classic checklist for stating what you are trying to do, what is new, and why it matters
- [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) — how a major venue operationalizes claim–evidence alignment
- Karl R. Popper, *Logik der Forschung* (Springer, 1934); English edition *The Logic of Scientific Discovery* (Hutchinson, 1959) — falsifiability: a statement is empirical only if some possible observation would contradict it
- W. Scott Richardson, Mark C. Wilson, Jim Nishikawa & Robert S. Hayward, "The well-built clinical question: a key to evidence-based decisions", *ACP Journal Club* 123(3):A12–A13 (1995) — the PICO slots that the research-question definition adapts
- Joseph P. Simmons, Leif D. Nelson & Uri Simonsohn, "False-positive psychology: undisclosed flexibility in data collection and analysis allows presenting anything as significant", *Psychological Science* 22(11):1359–1366 (2011) — why a threshold chosen after the data invalidates its p-value

## 한국어

*[[02-foundations/ml-practice|9. ML 실무]]와 [[02-foundations/probability|3. 확률 §6]] 위에 선다. Research Practice의 첫 페이지이자, 이 섹션의 모든 페이지가 함께 쓰는 관통 연구 RS1([[06-research-practice/index|연구 실무]])을 처음 쓰는 곳이다. RS1은 여기서 주장이 되고, 2쪽에서 실험이, 4쪽에서 논문이, 6쪽에서 증거 사다리의 한 단이 된다.*

Topic은 영역의 이름이고, research question은 증거가 해소할 수 있는 불확실한 관계를
명시한다. "건설에 VLA 적용"은 방향이다. 쓸모 있는 질문은 개입(intervention), 비교
대상(comparator), 결과(outcome), 조건, 범위를 짚는다.

> [!info] 깊이 목표
> 넓은 관심을 반증 가능한 질문으로 바꾼다; research gap과 "아직 구현이 없음"을 구분한다;
> 기여와 주장 강도를 증거에 맞춘다.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상과 계산 예제를 먼저 읽는다. 둘은 RS1에 관한 모호한 문장 하나를 스무 개의 숫자가 반박할 수 있는 주장으로 바꾸고, 그 숫자들이 어떤 문장을 허락하는지 말해 주는 표를 채운다. 그다음 §4(주장의 유형)와 §7(표 일반)을 읽는다. 1–3절과 5–6절은 다른 예제에서 같은 동작을 한다. 자기 질문을 쓸 때 돌아오면 된다.

### 이 페이지의 대상 · Running object

**RS1 — Research Practice의 관통 연구.** 이 섹션의 모든 페이지는 같은 작은 연구 하나를 다룬다. 질문, 설계, 실패, 논문, 임팩트 주장을 한 벌의 숫자 위에서 따라가기 위해서다. 페이지마다 전부 다시 적고, 숫자는 절대 바꾸지 않는다.

*질문.* 임피던스 제어(B)는 평면 팔이 패널에 닿는 접촉을, 힘 문턱에서 멈추는 위치 제어(A)보다 더 안전하게 만드는가?

*장치.* 팔은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 P2다. 평면 2R이고 링크 길이는 1 m, 각 링크 끝에 1 kg 점질량이 있다. 패널 강성은 P3 벽의 강성과 같은 $k_w = 400$ N/m다.

*시행.* 시행 한 번은 팔이 패널에 다가가 접촉하는 것이다. 기록하는 결과는 그 시행의 최대 접촉력(뉴턴)이고, 최댓값이 10 N 이하이면 그 시행은 성공이다.

*파일럿.* 제어기마다 10회. **이 데이터는 교육용으로 지어낸 예시이며 고정되어 있다. 실제 제어기를 측정한 값이 아니다.**

| 시행 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A — 위치 제어 + 힘 문턱 정지 (N) | 8.1 | 9.4 | 12.6 | 9.8 | 13.9 | 7.7 | 9.9 | 9.1 | 14.8 | 11.3 |
| B — 임피던스 제어 (N) | 6.2 | 7.9 | 8.4 | 5.9 | 7.1 | 10.6 | 6.8 | 7.5 | 8.0 | 6.6 |

| 제어기 | 성공(최대 ≤ 10 N) | 평균 (N) | 표본 표준편차 (N) | 중앙값 (N) |
|---|---:|---:|---:|---:|
| A | 6/10 | 10.66 | 2.414 | 9.85 |
| B | 9/10 | 7.50 | 1.356 | 7.30 |

시행 번호는 한 제어기 안의 이름표일 뿐이다. A의 3번 시행과 B의 3번 시행은 공유하는 것이 없으므로 아래의 모든 비교는 대응 없는(unpaired) 비교다. 이 페이지와 이후 페이지가 쓰는 비교 통계는 모두 이 스무 개 숫자에서 다시 계산한 것이다. 평균의 차 $10.66 - 7.50 = 3.16$ N, Welch 표준오차 $0.8756$ N, 자유도 $14.16$에서 $t = 3.609$. 어떤 결과에 어떤 검정이 맞는지는 [[02-foundations/probability|3. 확률 §6]]에, RS1 위의 계산은 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]의 계산 예제에 있다.

RS1이 일부러 정하지 않은 것: B의 목표 임피던스, A가 멈추는 힘 문턱, 접근 속도와 방향. 실제 연구라면 모두 밝혀야 한다. 이 페이지는 이 빈자리를 모호한 주장이 가장 먼저 숨기는 것으로 쓴다.

*범위: 이 페이지는 RS1을 주제에서 반증 가능하고 범위가 정해진 주장으로 바꾸는 법, 그리고 파일럿이 어떤 문장을 허락하는지 말해 주는 주장–증거 표를 채우는 법을 가르친다. 확인 실험에 시행이 몇 번 필요한지와 시행을 어떻게 배정하고 무작위화하는지([[06-research-practice/experimental-design-reproducibility|2. 실험 설계]]), 검정을 유도하는 법([[02-foundations/probability|3. 확률 §6]]), 결과를 논문으로 쓰는 법([[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]), 결과가 배치 증거의 어느 단에 오르는지([[06-research-practice/real-world-impact|6. 실세계 임팩트]])는 가르치지 않는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 545" style="max-width:100%;height:auto" role="img" aria-label="그림 두 장: 모호한 초안과 고쳐 쓴 RS1 주장에 범위·개입·비교 대상·결과·철회 괄호를 친 해부도, 그리고 파일럿 전에 고정한 10 N 선과 9–10 N 띠를 칠한 힘 축 위의 파일럿 최대 접촉력 스무 개">
  <text x="16" y="22" font-size="12.5" fill="currentColor"><tspan font-weight="bold">1</tspan><tspan dx="7">주장의 해부도</tspan></text>
  <text x="16" y="44" font-size="11" font-style="italic" opacity="0.7" fill="currentColor">초안(계산 예제 1단계)</text>
  <text x="16" y="64" font-size="12" textLength="75.4" lengthAdjust="spacing" fill="currentColor">임피던스 제어</text>
  <text x="91.4" y="64" font-size="12" textLength="12" lengthAdjust="spacing" fill="currentColor">가</text>
  <text x="106.7" y="64" font-size="12" textLength="51.4" lengthAdjust="spacing" fill="currentColor">로봇 접촉</text>
  <text x="158.1" y="64" font-size="12" textLength="12" lengthAdjust="spacing" fill="currentColor">을</text>
  <text x="173.4" y="64" font-size="12" textLength="63.4" lengthAdjust="spacing" fill="currentColor">더 안전하게</text>
  <text x="240.2" y="64" font-size="12" textLength="36" lengthAdjust="spacing" fill="currentColor">만든다</text>
  <path d="M16 68 V72 H91.4 V68 M53.7 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="16" y="91" font-size="11" fill="currentColor">I · 계열 이름뿐</text>
  <path d="M106.7 68 V72 H158.1 V68 M132.4 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="132.4" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="132.4" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">S</text>
  <path d="M173.4 68 V72 H236.8 V68 M205.1 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="205.1" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="205.1" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">Y</text>
  <line x1="306.2" y1="64" x2="362.2" y2="64" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="1 3"/>
  <path d="M302.2 68 V72 H366.2 V68 M334.2 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="334.2" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="334.2" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">C</text>
  <line x1="398.2" y1="64" x2="454.2" y2="64" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="1 3"/>
  <path d="M394.2 68 V72 H458.2 V68 M426.2 72 V75.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="3 2.5"/>
  <circle cx="426.2" cy="87" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
  <text x="426.2" y="91" font-size="11" text-anchor="middle" opacity="0.6" fill="currentColor">R</text>
  <text x="548" y="91" font-size="11" text-anchor="end" opacity="0.7" fill="currentColor">점선 = 비어 있음</text>
  <text x="16" y="117" font-size="11" font-style="italic" opacity="0.7" fill="currentColor">고쳐 쓴 주장(계산 예제 3단계)</text>
  <text x="16" y="137" font-size="11.5" textLength="357.1" lengthAdjust="spacing" fill="currentColor">RS1 시행 절차에 따라 평면 팔 P2가 400 N/m 패널에 다가가 접촉할 때</text>
  <path d="M16 141 V145 H373.1 V141 M194.5 145 V148.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="194.5" y="161" font-size="11" text-anchor="middle" fill="currentColor">S · 범위: P2, 400 N/m 패널, RS1 시행</text>
  <text x="16" y="182" font-size="11.5" textLength="338.3" lengthAdjust="spacing" fill="currentColor">— B의 목표 임피던스와 A의 정지 문턱은 방법 절에 보고한 대로 —</text>
  <text x="16" y="202" font-size="11.5" textLength="87.5" lengthAdjust="spacing" fill="currentColor">임피던스 제어(B)</text>
  <text x="103.5" y="202" font-size="11.5" textLength="11.5" lengthAdjust="spacing" fill="currentColor">는</text>
  <text x="118.2" y="202" font-size="11.5" textLength="131.7" lengthAdjust="spacing" fill="currentColor">힘 문턱 정지 위치 제어(A)</text>
  <text x="249.9" y="202" font-size="11.5" textLength="23" lengthAdjust="spacing" fill="currentColor">보다</text>
  <text x="276.1" y="202" font-size="11.5" textLength="86.9" lengthAdjust="spacing" fill="currentColor">평균 최대 접촉력</text>
  <text x="363.1" y="202" font-size="11.5" textLength="40.9" lengthAdjust="spacing" fill="currentColor">이 낮다.</text>
  <path d="M16 206 V210 H103.5 V206 M59.8 210 V213.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="59.8" y="226" font-size="11" text-anchor="middle" fill="currentColor">I · 개입: B</text>
  <path d="M118.2 206 V210 H249.9 V206 M184.1 210 V213.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="184.1" y="226" font-size="11" text-anchor="middle" fill="currentColor">C · 비교 대상: A</text>
  <path d="M276.1 206 V210 H363.1 V206 M319.6 210 V213.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="319.6" y="226" font-size="11" text-anchor="middle" fill="currentColor">Y · 결과: 최대 접촉력(N)</text>
  <text x="16" y="247" font-size="11.5" textLength="52.4" lengthAdjust="spacing" fill="currentColor">부차 결과:</text>
  <text x="71.7" y="247" font-size="11.5" textLength="189.4" lengthAdjust="spacing" fill="currentColor">B의 접촉 중 10 N 이하에 머무는 비율</text>
  <text x="261.1" y="247" font-size="11.5" textLength="55.7" lengthAdjust="spacing" fill="currentColor">이 더 크다.</text>
  <path d="M71.7 251 V255 H261.1 V251 M166.4 255 V258.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="166.4" y="271" font-size="11" text-anchor="middle" fill="currentColor">Y · 부차 결과: 10 N 이하면 성공</text>
  <path d="M16 282 V286 H404 V282 M210 286 V289.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9"/>
  <text x="210" y="303" font-size="11" text-anchor="middle" fill="currentColor">R · μ<tspan dy="3" font-size="9.5">A</tspan><tspan dx="3.1" dy="-3">− μ</tspan><tspan dy="3" font-size="9.5">B</tspan><tspan dy="-3">의 Welch 95% 신뢰구간이 완전히 0보다 위에 있지 않으면 철회.</tspan></text>
  <text x="210" y="318" font-size="11" text-anchor="middle" fill="currentColor">부차 주장은 Fisher 정확 검정이 양측 α = 0.05에서 기각하지 못하면 철회</text>
  <line x1="16" y1="336" x2="544" y2="336" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="16" y="358" font-size="12.5" fill="currentColor"><tspan font-weight="bold">2</tspan><tspan dx="7">조작적 정의를 그림으로</tspan></text>
  <rect x="268" y="380" width="44" height="80" fill="currentColor" fill-opacity="0.13"/>
  <line x1="92" y1="460" x2="532" y2="460" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M92 460V465 M136 460V465 M180 460V465 M224 460V465 M268 460V465 M312 460V465 M356 460V465 M400 460V465 M444 460V465 M488 460V465 M532 460V465" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="92" y="478" font-size="11" text-anchor="middle" fill="currentColor">5</text>
  <text x="136" y="478" font-size="11" text-anchor="middle" fill="currentColor">6</text>
  <text x="180" y="478" font-size="11" text-anchor="middle" fill="currentColor">7</text>
  <text x="224" y="478" font-size="11" text-anchor="middle" fill="currentColor">8</text>
  <text x="268" y="478" font-size="11" text-anchor="middle" fill="currentColor">9</text>
  <text x="312" y="478" font-size="11" text-anchor="middle" fill="currentColor">10</text>
  <text x="356" y="478" font-size="11" text-anchor="middle" fill="currentColor">11</text>
  <text x="400" y="478" font-size="11" text-anchor="middle" fill="currentColor">12</text>
  <text x="444" y="478" font-size="11" text-anchor="middle" fill="currentColor">13</text>
  <text x="488" y="478" font-size="11" text-anchor="middle" fill="currentColor">14</text>
  <text x="532" y="478" font-size="11" text-anchor="middle" fill="currentColor">15</text>
  <text x="312" y="495" font-size="11" text-anchor="middle" fill="currentColor">시행별 최대 접촉력 (N)</text>
  <line x1="312" y1="370" x2="312" y2="460" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="318" y="378" font-size="11" fill="currentColor">10 N, 파일럿 전에 고정</text>
  <circle cx="210.8" cy="398" r="4" fill="currentColor"/>
  <circle cx="228.4" cy="398" r="4" fill="currentColor"/>
  <circle cx="272.4" cy="398" r="4" fill="currentColor"/>
  <circle cx="285.6" cy="398" r="4" fill="currentColor"/>
  <circle cx="303.2" cy="393" r="4" fill="currentColor"/>
  <circle cx="307.6" cy="403" r="4" fill="currentColor"/>
  <circle cx="369.2" cy="398" r="4" fill="currentColor"/>
  <circle cx="426.4" cy="398" r="4" fill="currentColor"/>
  <circle cx="483.6" cy="398" r="4" fill="currentColor"/>
  <circle cx="523.2" cy="398" r="4" fill="currentColor"/>
  <circle cx="131.6" cy="434" r="4" fill="currentColor"/>
  <circle cx="144.8" cy="434" r="4" fill="currentColor"/>
  <circle cx="162.4" cy="434" r="4" fill="currentColor"/>
  <circle cx="171.2" cy="434" r="4" fill="currentColor"/>
  <circle cx="184.4" cy="434" r="4" fill="currentColor"/>
  <circle cx="202" cy="434" r="4" fill="currentColor"/>
  <circle cx="219.6" cy="429" r="4" fill="currentColor"/>
  <circle cx="224" cy="439" r="4" fill="currentColor"/>
  <circle cx="241.6" cy="434" r="4" fill="currentColor"/>
  <circle cx="338.4" cy="434" r="4" fill="currentColor"/>
  <text x="20" y="402" font-size="12.5" font-weight="bold" fill="currentColor">A</text>
  <text x="20" y="438" font-size="12.5" font-weight="bold" fill="currentColor">B</text>
  <text x="38" y="402" font-size="12" fill="currentColor">6/10</text>
  <text x="38" y="438" font-size="12" fill="currentColor">9/10</text>
  <text x="38" y="378" font-size="11" opacity="0.7" fill="currentColor">≤ 10 N</text>
  <text x="16" y="518" font-size="11" opacity="0.9" fill="currentColor">칠한 띠: 9–10 N. A의 최댓값 넷(9.1, 9.4, 9.8, 9.9)이 그 안에 있어서</text>
  <text x="16" y="533" font-size="11" opacity="0.9" fill="currentColor">선이 움직이면 판정도 움직인다. 선은 주장의 일부다.</text>
</svg>

첫째 장은 RS1의 주장에 아래에서 범위 S, 개입 I, 비교 대상 C, 결과 Y, 그리고 주장을 철회시킬 규칙 R의 괄호를 친다 — 모호한 초안 "임피던스 제어가 로봇 접촉을 더 안전하게 만든다"는 I 하나만, 그것도 계열 이름으로만 채우고, 계산 예제에서 고쳐 쓴 주장은 다섯을 모두 채운다. 둘째 장은 조작적 정의를 그림으로 옮긴 것으로, 5 N에서 15 N까지의 힘 축 위에 파일럿 최대 접촉력 스무 개와 파일럿 전에 고정한 10 N 선이 있고, A는 6/10, B는 9/10이다. A의 최댓값 넷, 9.1, 9.4, 9.8, 9.9 N이 칠한 9–10 N 띠 안에 있어서 선이 움직이면 판정도 움직인다 — 선은 주장의 일부다.

### 대상으로 한 번 끝까지 · Worked case

RS1 위의 다섯 단계. 어떤 결과도 반박할 수 없는 문장에서, 스무 개의 숫자가 시험할 수 있는 주장으로, 그리고 그 숫자들이 어떤 문장을 허락하는지 말해 주는 표로 간다.

**1단계 — 모호한 주장과 그것이 비워 둔 칸.** RS1 초록의 첫 초안은 이렇게 말한다. *"임피던스 제어가 로봇 접촉을 더 안전하게 만든다."* 연구 질문이 반드시 밝혀야 하는 것들에 대어 읽어 본다.

> [!info] 정의 — 연구 질문
> **무엇인가:** 증거가 나오기 전에는 답이 불확실하고 증거가 그 답을 정하는, 어떤 관계에 대한 질문이다. **정의 조건 — 다섯 모두:** (1) 질문이 겨냥하는 embodiment, 환경, 과제, 모집단, 곧 **범위** $S$를 밝히고, (2) **개입** $I$를, (3) 시험하는 요인 외에는 $I$와 모두 맞춘 **비교 대상** $C$를, (4) 조작적 정의(2단계)를 갖춘 **결과** $Y$를 밝히며, (5) '아니오'로 답할 수 있어야 한다. 곧 $Y$가 가질 수 있는 어떤 값은 개입이 도움이 되지 않았다는 뜻이어야 한다. 튜플로 쓰면
> $$Q = (S,\ I,\ C,\ Y), \qquad Q\text{에 '아니오'로 답하는 가능한 결과가 적어도 하나 있음}$$
> 이므로 질문은 범위 $S$ 안에서 $I$ 아래의 $Y$와 $C$ 아래의 $Y$를 비교하는 것이다. 임상 연구는 같은 칸을 PICO(모집단, 개입, 비교, 결과)라 부른다(Richardson 등 1995).
> **예.** "RS1 시행에서 400 N/m 패널로 다가가는 P2에 대해, 임피던스 제어(B)는 힘 문턱 정지 위치 제어(A)보다 최대 접촉력이 낮은가?"
> **반례.** "안전한 접촉을 위한 임피던스 제어"는 $I$ 말고는 아무것도 밝히지 않는다. 주제일 뿐이고, 어떤 결과도 여기에 답할 수 없다.
> **왜 중요한가.** 빈칸 하나하나가 아직 설계할 수 없는 실험의 한 부분이다. $C$가 없으면 돌릴 베이스라인이 없고, $Y$가 없으면 기록할 것이 없으며, $S$가 없으면 답이 어디서부터 적용되지 않는지 말할 방법이 없다.

이 칸들에 대어 보면 초안은 한 칸만 채우고, 그 한 칸도 제어 방식의 계열 이름으로 채운다.

| 칸 | 초안이 말하는 것 | 빠진 것 |
|---|---|---|
| $S$, 범위 | "로봇 접촉" | 어떤 팔, 어떤 표면, 어떤 접근 |
| $I$, 개입 | "임피던스 제어" | *어떤* 임피던스인가. 주장은 목표 강성과 감쇠 한 쌍에 관한 것인데 RS1은 그 값을 밝히지 않았다 |
| $C$, 비교 대상 | — | *무엇보다* 안전한가 |
| $Y$, 결과 | "더 안전하게" | 측정 |
| '아니오'로 답할 수 있음 | — | 주장에 반하는 것으로 칠 결과 |

**2단계 — "더 안전하게"에 조작적 정의를 준다.** RS1에는 이미 하나가 있다. 시행마다 최대 접촉력을 기록하고, 그 최댓값이 10 N 이하이면 성공으로 친다.

> [!info] 정의 — 조작적 정의
> **무엇인가:** 측정 규칙, 곧 시행 하나하나를 결과의 값 하나로 옮기는 절차다. 두 사람이 같은 시행에 적용하면 같은 값을 기록해야 한다. **정의 조건:** (1) 신호와 그것을 기록하는 측정 장치, (2) 시간 창과 그 위의 집계 방식, (3) 단위, (4) 결과를 성공과 실패로 자른다면 그 문턱을 밝히고, (5) 적용할 데이터보다 **먼저** 고정한다. RS1이라면
> $$Y_i = \max_{t \in W_i} F_i(t), \qquad S_i = \mathbb{1}\big[\,Y_i \le 10\ \text{N}\,\big]$$
> 이다. $F_i(t)$는 시행 $i$의 시각 $t$에서의 접촉력, $W_i$는 그 시행의 접촉 구간, $Y_i$는 뉴턴 단위 최대 접촉력, $S_i$는 성공 지표이고, $\mathbb{1}[\cdot]$은 괄호 안이 참이면 1, 아니면 0이다. 그래서 시행마다 숫자 하나와 비트 하나가 나온다.
> **예.** A의 7번 시행은 최댓값이 $Y = 9.9$ N이므로 $S = 1$이고, 10번 시행은 $11.3$ N이므로 $S = 0$이다.
> **반례.** 같은 규칙이지만 점을 본 뒤에 선을 그은 경우다. 아래 표가 그것이다.
> **왜 중요한가.** 주장의 판정은 정의의 함수다. 선을 옮기면 "더 안전하게"라는 말은 그대로여도 다른 주장을 시험하게 된다.

반례를 숫자로 보자. A의 최댓값 열 개 중 넷이 선 바로 아래, 9 N과 10 N 사이에 있다(9.1, 9.4, 9.8, 9.9). 그래서 RS1의 개수는 선을 어디에 긋느냐에 유난히 민감하다.

| 선의 위치 | A 성공 | B 성공 | 차이 | Fisher 정확 검정 $p$ |
|---|---:|---:|---:|---:|
| 9 N | 2/10 | 9/10 | 0.7 | 0.005 |
| **10 N, 파일럿 전에 고정** | **6/10** | **9/10** | **0.3** | **0.30** |
| 12 N | 7/10 | 10/10 | 0.3 | 0.21 |

행 사이에 달라진 측정값은 하나도 없다. 데이터를 본 뒤 선을 그은 분석가는, 미리 정한 10 N에서 $p = 0.30$을 주는 바로 그 스무 시행에서 $p = 0.005$를 보고할 수 있다. 조건 (5)가 예의가 아니라 정의의 일부인 이유다. 데이터를 본 뒤 밝히지 않고 내린 선택들은 거의 어떤 비교든 유의하게 보이게 만들 수 있다(Simmons, Nelson & Simonsohn 2011). 대응 없는 두 성공 횟수에는 [[02-foundations/probability|3. 확률 §6]]이 Fisher 정확 검정을 고르고, RS1 위의 계산은 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]에 있다.

**3단계 — 고쳐 쓴 주장과, 그것을 철회시킬 규칙.**

> *RS1 시행 절차에 따라 평면 팔 P2가 400 N/m 패널에 다가가 접촉할 때 — B의 목표 임피던스와 A의 정지 문턱은 방법 절에 보고한 대로 — 임피던스 제어(B)는 힘 문턱 정지 위치 제어(A)보다 평균 최대 접촉력이 낮다. 부차 결과: B의 접촉 중 10 N 이하에 머무는 비율이 더 크다.*

확인 실험 전에 적어 두는 규칙: *두 평균 최대 접촉력의 차 $\mu_A - \mu_B$에 대한 Welch 95% 신뢰구간이 완전히 0보다 위에 있지 않으면 주 주장을 철회한다. Fisher 정확 검정이 양측 $\alpha = 0.05$에서 두 성공 확률이 같다는 가설을 기각하지 못하면 부차 주장을 철회한다.* 최대 접촉력을 주 결과로 삼는 것은 그것이 시행마다 선에서 얼마나 떨어졌는지를 간직하기 때문이다. 성공 횟수는 선의 어느 쪽인지만 간직한다. 그 선택이 시행 수로 얼마의 비용인지는 [[06-research-practice/real-world-impact|6. 실세계 임팩트]]의 계산 예제다.

> [!info] 정의 — 반증 가능한 주장
> **무엇인가:** 연구 질문 $(S, I, C, Y)$에 대한 진술로, 계획한 측정, 그리고 저자가 그 진술을 포기할 때를 정한 규칙과 짝을 이룬다. **정의 조건 — 넷 모두:** (1) 결과에 조작적 정의가 있다. (2) 진술을 철회시킬 가능한 결과들의 집합 $R$을 밝힌다. (3) $R$은 **공집합이 아니다**. 곧 측정이 낼 수 있는 결과 중 적어도 하나가 주장에 반한다. (4) $R$은 결과를 보기 **전에** 고정한다.
> $$R \subseteq \Omega, \qquad R \neq \varnothing, \qquad \text{주장을 철회한다} \iff o \in R$$
> 여기서 $\Omega$는 계획한 측정이 낼 수 있는 결과의 집합이고 $o$는 실제로 나온 결과다. 그래서 주장은 $R$이 공집합이 아닐 때에만 위험을 진다. 이 발상은 포퍼의 것이다. 진술은 어떤 결과를 금지함으로써만 세계에 대해 무언가를 말한다.
> **예.** 3단계의 주 주장. $R$ = "$\mu_A - \mu_B$의 Welch 95% 신뢰구간이 완전히 0보다 위에 있지 않음".
> **반례.** "임피던스 제어가 접촉을 더 안전하게 만든다"는 $R = \varnothing$이다. 어떤 결과든 흡수할 수 있다("안전은 힘 이상의 것이다"). 2단계의 9 N 행은 반대 방향으로 실패한다. $R$은 공집합이 아니지만 $o$를 본 뒤에 골랐으므로, 이미 일어나지 않았다고 확인된 결과만 금지할 뿐이다.
> **왜 중요한가.** 아무것도 금지하지 않는 주장은 지지받을 수도 없다. 어떤 결과도 그것에 반하는 것으로 치지 않았을 것이기 때문이다. 그리고 $R$이 공집합이 아니라고 곧 강한 시험인 것은 아니다. 주장이 참일 때 측정이 $R$ 밖에 머물 확률이 검정의 검정력이고([[02-foundations/probability|3. 확률 §6]]), 그것을 정하는 것은 시행 수다.

마지막 점은 RS1에서 구체적이다. B의 참 성공 확률이 정말로 0.9이고 A가 0.6이어도, 제어기당 10회로는 성공 비교가 규칙을 통과할 확률이 정규근사로 약 3분의 1, 규칙이 실제로 지정한 정확 검정으로는 약 7분의 1에 불과하다(둘 다 [[06-research-practice/real-world-impact|6. 실세계 임팩트]]에서 유도한다). 그렇게 시험하면 참인 부차 주장도 대개 철회된다.

**4단계 — 파일럿의 숫자로 주장–증거 표를 채운다.** §7의 표에, 초안이 RS1에 대해 할 법한 주장마다 한 행씩 두고 열 셋을 더한다. §4의 주장 유형, 파일럿의 증거, 판정이다. 두 구간과 두 p-값의 계산은 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]의 계산 예제에 있다.

| 의도한 주장 | 유형(§4) | 필요한 비교 | 지표 | 경계 | 파일럿 증거(제어기당 10회) | 판정 |
|---|---|---|---|---|---|---|
| B는 파일럿 10회 중 9회에서 10 N 이하에 머물렀다 | 기술적 | 없음 | 개수 $k/n$ | 이 열 번의 시행 | 9/10 | 적힌 그대로 허락됨 |
| B의 평균 최대 접촉력은 A보다 낮다 | 비교적 | 같은 팔·패널·시행에서 A 대 B | $\bar y_A - \bar y_B$ (N), Welch 95% 신뢰구간 | P2, 400 N/m, RS1 시행 | $3.16$ N, 신뢰구간 $[1.28,\ 5.04]$; 자유도 $14.2$에서 $t = 3.61$, $p = 0.003$ | 이 파일럿에 대해, 경계 안에서 허락됨 |
| B가 A보다 더 자주 성공한다 | 비교적 | 위와 같음 | 성공 비율의 차와 그 95% 신뢰구간, Fisher 정확 검정 | 위와 같음 | $0.90$ 대 $0.60$: $+0.30$, 신뢰구간 $[-0.08,\ 0.60]$; $p = 0.30$ | 허락되지 않음: 파일럿은 둘을 구별하지 못한다 |
| B가 A보다 안전하다 | 안전/신뢰성 | hazard 정의, 노출, 심각도, 감독 | 노출 단위당 초과와 near miss | 인증이 아님 | 20회 시행 위의 힘 대리 지표 하나 | 허락되지 않음 |
| B의 이점은 더 뻣뻣한 패널에서도 유지된다 | 일반화 | 여러 패널 강성에서 같은 비교 | 강성별 차이 | 명시한 강성 범위 | 없음: 패널 하나 | 시험하지 않음, 그리고 물리가 바뀐다 |
| B는 컴플라이언스가 충격을 흡수하기 때문에 더 부드럽다 | 기전적 | 힘–시간 기록; 목표 강성만 바꾼 같은 제어기 | 충격 지속 시간, 흡수 에너지 | — | 최댓값만 있음 | 허락되지 않음 |

두 행이 교훈을 담는다.

*2행과 견준 3행.* 9/10과 6/10의 차이는 커 보이고, 초안 대부분이 앞세울 행이다. 그러나 두 성공 확률이 같더라도, 성공 열다섯 번이 이만큼 이상 치우쳐 나뉠 확률이 $0.30$이다. 같은 스무 시행이 2행을 $p = 0.003$으로 지지하는 이유는 둘이다. 평균은 모든 시행이 선에서 떨어진 거리를 쓰는 반면 개수는 각 시행이 선의 어느 쪽에 떨어졌는지만 쓴다. 그리고 A의 최댓값 넷이 선 바로 아래 있어 개수는 그것들을 성공으로 치므로, 개수가 보여 주는 차이가 힘이 보여 주는 차이보다 작다. [[06-research-practice/real-world-impact|6. 실세계 임팩트]]가 두 이유를 시행 수로 갈라 본다.

*5행의 경계.* 경계 열은 겸손이 아니다. [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]의 반정현 접촉 모델에서, 겉보기 질량이 $\Lambda_y = 2$ kg인 P2의 고정 자세로 $y$ 방향에서 다가가면 접촉은

$$t_c = \pi\sqrt{\Lambda_y / k}$$

동안 이어진다. 공구와 패널이 스프링 위의 질량처럼 움직이고 접촉은 반주기 뒤에 끝나기 때문이다. RS1의 패널에서는 $\pi\sqrt{2/400} = 0.222$ s, $10^5$ N/m 구조물에서는 $\pi\sqrt{2/10^5} = 0.014$ s다. 충격을 다듬을 시간이 10분의 2초인 제어기와 14 ms인 제어기는 서로 다른 문제를 푼다. 그래서 부드러운 패널의 결과는 뻣뻣한 패널을 시험하기 전까지 그 패널에 대해 아무것도 말하지 않는다.

**5단계 — 파일럿이 허락하는 문장.** 허락된 행들을 함께 읽으면 다음과 같다.

> 400 N/m 패널에 대한 P2 팔의 제어기당 10회 파일럿에서, B의 평균 최대 접촉력은 A보다 3.16 N 낮았다(95% 신뢰구간 1.28–5.04 N). B는 10회 중 9회, A는 10회 중 6회 10 N 이하에 머물렀으나, 이 파일럿은 그 차이를 우연과 구별하지 못한다(95% 신뢰구간 $-0.08$–$+0.60$; Fisher 정확 검정 $p = 0.30$).

절마다 표의 행이 있고, 문장이 빼 놓은 행 — 안전, 더 뻣뻣한 패널, 기전 — 은 일부러 뺀 것이다. 다음 페이지들이 가져가는 것이 이 문장이다. [[06-research-practice/experimental-design-reproducibility|2. 실험 설계]]는 확인 실험을 어떻게 배정하고 몇 번 돌릴지 정하고, [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]는 숫자 하나하나를 표의 칸과 그것이 허락하는 문장으로 바꾸며, [[06-research-practice/real-world-impact|6. 실세계 임팩트]]는 파일럿이 증거의 어느 단에 서 있고 다음 단이 얼마인지 묻는다. 이 문장이 해서는 안 되는 일은 확인 실험보다 먼저 혼자 아카이브 venue로 가는 것이다. 파일럿과 확인 실험은 주장 하나이고, [[06-research-practice/venue-strategy|5. Venue 전략]]의 worked case는 그러면 저널 규칙이 둘째를 첫째의 단순한 확장으로 보고 거절한다는 것을 보인다.

### 1. Topic → problem → question

| 수준 | 예 |
|---|---|
| Topic | 건설 매니퓰레이션을 위한 VLA |
| Problem | 부족한 시연이 새로운 자재 배치에의 적응을 제한한다 |
| Question | 고정된 시연 예산 아래, 사전학습 VLA의 action-chunk 파인튜닝이 held-out 배치에서 vision-only 행동 복제보다 폐루프 성공률을 높이는가? |

최종 질문은 조건, 개입, 비교 대상, 결과, 시험 분포를 명시한다. **부정적으로도 답할 수
있어야 한다.**

**수정 전:** “건설 현장 조작을 연구한다.” **문제:** 영역 이름에는 실패할 가정이 없다. **수정 후:** “공장용 파지 계획기는 가정한 마찰계수 μ에 의존하는 경우가 많다. 젖거나 먼지가 묻은 현장 표면은 그 가정을 깨뜨릴 수 있다.” 주제가 모델과 운용 조건의 구체적 불일치로 바뀐다.

**수정 전:** “촉각을 추가해 이를 해결한다.” **문제:** 센서 설치는 개입이지 답할 수 있는 질문이 아니다. **수정 후:** “가정한 μ가 틀렸을 때, 접촉 중 촉각으로 마찰을 추정하면 고정 μ를 쓰는 같은 계획기 대비 잃어버린 파지 성공률을 얼마나 회복하는가?”

**여기서 얻는 독법.** 표면 조건에서 모델 오차를 거쳐 측정 결과로 이어지는 사슬을 찾는다. 마찰 오추정을 어떻게 확인할지 정하고 파지 계획기는 비교 가능하게 유지한다. 부정적 답도 유익하다. 접촉 관측이 파지 결정을 바꾸기에 너무 늦게 들어온다는 경계를 드러낼 수 있다.

계산 예제는 같은 동작을 RS1에서 한다. "임피던스 제어가 로봇 접촉을 더 안전하게 만든다"에서 출발해, 모든 칸을 채운 질문과 철회 규칙을 갖춘 주장에 이른다.

### 2. Gap은 "아무도 안 했다"가 아니다

방어 가능한 gap은 설명되지 않은 실패, 양립 불가능한 가정, 빠진 증거, 나쁜 일반화,
비현실적 평가, 이론적·운용적으로 중요한 트레이드오프일 수 있다. 새 데이터셋에 모델을
얹는 것은 중대한 질문을 시험하지 않는 한 엔지니어링 활동이다.

빠진 증거가 왜 중요한지를 설명해야 gap이 된다. “아무도 이 굴착기에 VLA를 붙이지 않았다”는 말은 단순 이식, 장비 부재, 어려운 미해결 가정 중 어느 것이든 뜻할 수 있다. 신규성 문장은 같아 보여도 각각 다른 연구가 된다.

예를 들어 시각 시연으로 학습한 정책은 버킷 동작을 시작하기 전에 달라진 재료 저항을 보지 못할 수 있다. 중요한 gap은 숨은 변동 아래에서 주어진 관측으로 제때 적응할 수 있는가다. VLA를 기계에 올리는 실험은 이 정보 한계를 구현 실패나 부적절한 행동 인터페이스와 구별할 수 있을 때 유익하다.

**여기서 얻는 독법.** 빠진 연구와 예상 실패 기전을 연결하는 고리를 찾는다. 기존 방법은 무엇을 가정하고, 현장의 어떤 조건이 이를 깨며, 어떤 관찰로 불확실성을 해소할지 묻는다. 설득력 있는 gap은 다른 집단이 비슷하게 생긴 시스템을 이미 만들었더라도 남는다.

### 3. 가설과 기여

- **가설:** 시험 가능한 기대 관계.
- **엔지니어링 목표:** 구축할 시스템 능력.
- **과학적 기여:** 증거가 지지하는 새 지식.
- **시스템 기여:** 구조·배포·평가에 신규성이 있을 수 있는 통합·능력.
- **산출물 기여:** 유용한 코드, 데이터셋, 벤치마크, 플랫폼.

새 알고리즘 없이 시스템으로 기여할 수 있다 — 단 조립 노력 너머에 그 시스템이 어떤
지식·능력을 확립하는지 밝혀야 한다.

**수정 전:** “기여는 촉각 센서다.” **문제:** 부품 이름만으로는 어떤 지식이나 능력을 확립했는지 알 수 없다. **수정 후:** “접촉 상태 추정 인터페이스를 제공하고, 그 갱신이 마찰 오추정 아래 파지 성능을 회복하는지 평가한다.” 산출물과 과학적 질문의 역할이 나뉜다.

**수정 전:** “시스템이 새롭고 유용하다고 가설을 세운다.” **문제:** 신규성은 선행연구와의 관계이고 유용성에는 결과 정의가 없다. **수정 후:** “짝지은 파지 절차에서 접촉 중 마찰 갱신이 잘못 가정한 μ와 관련된 실패를 줄일 것으로 예측한다.”

이는 결과가 아니라 제안 단계의 문장이다. 최종 기여 문장은 예측이 실패했을 때의 더 좁은 결론까지 포함해 증거가 지지하는 것을 적어야 한다. **여기서 얻는 독법.** 기여가 산출물인지, 관찰된 관계인지, 능력인지 구별하고 그에 맞는 증거가 있는지 본다.

### 4. 주장의 유형

| 주장 | 요구되는 주의 |
|---|---|
| 기술적(descriptive) | 관찰된 표본을 넘어 일반화하지 말 것 |
| 비교적 | 정의된 베이스라인·설정 대비 성능 |
| 인과적 | 대안 설명이 통제·모델링돼야 함 |
| 일반화 | 대상 분포와 이동(shift)이 정의돼야 함 |
| 기전적(mechanistic) | 방법이 *왜* 통하는지 분리하는 증거 |
| 안전/신뢰성 | 노출, 심각도, 희귀 실패, 시스템 경계가 중요 |

마지막 행의 **노출**(exposure)은 그 실패를 낳을 수 있었던 운용 시간, 거리, 시행 수의 양이다. 10회 시행에서 충돌 0과 10,000회 시행에서 충돌 0은 전혀 다른 증거다.

"구성요소 X를 빼면 성능이 떨어진다"는 범위가 한정된 의존성을 지지할 뿐,
저자의 완전한 인과 이야기를 증명하지 않는다.

**수정 전:** “전체 시스템의 점수가 높으므로 촉각이 개선의 원인이다.” **문제:** 학습 데이터나 제어 논리도 달라졌다면 비교 결과로 기전을 분리할 수 없다. **수정 후:** “시험 조건에서 전체 시스템이 베이스라인보다 좋았다. 차이를 촉각에 귀속하려면 짝지은 촉각 절제가 필요하다.”

**수정 전:** “충돌이 없었으므로 로봇은 안전하다.” **문제:** 표본 결과에 노출량과 감독 역할이 빠져 있다. **수정 후:** “명시한 시행·개입 절차에서 충돌은 관찰되지 않았다. 이는 시험한 시스템에 한정된 관찰을 지지한다.”

가상의 고쳐 쓰기는 관찰을 보존하면서 추론 범위를 줄인다. **여기서 얻는 독법.** 기술한다, 앞선다, 유발한다, 전이한다, 방지한다 중 어느 동사를 쓰는지 본다. 비교와 표집 절차가 실제로 그 종류의 문장을 지지할 수 있는지 묻는다.

계산 예제는 이 표의 행마다 RS1의 사례를 하나씩 주고, 옆에 파일럿의 증거와 판정을 붙인다. 스무 시행을 견디는 것은 기술적 행과 최대 접촉력 비교뿐이다.

### 5. 범위와 가정

모집단, 환경, embodiment, 센서, 데이터 체제, 과제, 개입 정책, 평가 지평을 적어라.
가정은 그 자체로 약점이 아니다 — **숨긴 가정**이 약점이다.

범위가 있어야 실험을 해석할 수 있다. 같은 개입도 조건에 따라 다른 질문에 답한다. 익숙한 마른 물체에서 시험한 마찰 추정기는 알려진 조건 안의 적응을 다룬다. 보지 못한 젖은 표면에서의 평가는 과제와 성공 지표 이름이 같아도 다른 경계를 시험한다.

촉각 파지 질문에서는 재료 준비, 마찰 오추정의 유도·확인 방법, 행동 전에 이용 가능한 접촉 관측, 운전자가 바꿀 수 있는 것을 기록한다. 파지 형상과 물체 정체성이 학습에 있었는지도 밝힌다. 정책은 마찰을 추정하지 않고도 이런 단서를 쓸 수 있다. 성공한 시험이 의도보다 좁은 설명만 지지할 수 있는 이유다.

**여기서 얻는 독법.** “이 결과는 …일 때 적용된다”를 완성해 본다. 빠진 조건은 방법 절에 물어볼 질문이다. 명시한 단순화와 시험하지 않은 전이 주장을 구분한다. 모델의 경계를 알아야 후속 연구가 그 경계를 의도적으로 옮길 수 있다.

### 6. 고쳐 쓰기 예제

약함: **월드모델이 건설로봇을 개선할 수 있는가?**

더 강함: **가변 토질의 자율 굴착에서, 학습된 잠재 동역학 모델이 같은 시연과 MPC 안전
제약을 쓰는 model-free 행동 복제 대비 버킷 경로 추종 오차와 회복 개입을 줄이는가?**

(MPC는 모델 예측 제어로, 매 주기 짧은 지평의 제약 최적화를 다시 푼다. [[04-robotics/mpc|MPC]] 참고.) 이것도 토질 변동, 개입, 월드모델 계획 절차의 조작적 정의가 더 필요하다. 조작적 정의는 계산 예제에서 RS1의 성공 규칙 위에 완전히 정의되고, 문턱 하나를 옮기면 판정이 어떻게 되는지도 거기서 보인다.

**수정 전, 제안 단계의 초록:** “건설로봇에는 강건한 조작이 필요하다. 어려운 환경에서 신뢰성 있는 파지를 위한 촉각 지능 프레임워크를 제안한다.” 동기와 도구는 있지만 시험할 가정이 없다. 독자는 약속에 반하는 결과를 상상하기 어렵다.

**수정 후, 제안 단계의 초록:** “마찰을 안다고 가정한 파지 계획기는 현장 표면이 젖거나 먼지가 묻으면 성공률이 떨어질 수 있다. 접촉 중 촉각으로 μ를 추정하면 고정 μ를 쓰는 같은 계획기 대비 이 손실을 회복하는지 묻는다. 물체, 센싱 기회, 개입 규칙을 맞추고 보지 못한 표면 조건에서 비교한다. 파지 성공, 회복 행동, 추정 시점을 보고한다. 이 실험은 관찰한 접촉 정보가 파지 결정 전에 유용한지 시험한다. 일반적인 건설 자율성을 확립하지는 않는다.”

연구 제안이므로 결과를 지어 넣지 않는다. 시험 뒤에는 보고 계획을 측정 결과와 불확실성으로 바꾼다. 최종 결론은 부정 결과까지 포함해 실제 관찰을 따라야 한다.

### 7. 주장–증거 표

실험 전에 이 표를 만들어라:

| 의도한 주장 | 필요한 비교 | 지표 | 경계 |
|---|---|---|---|
| 더 나은 데이터 효율 | 여러 데이터 예산에서 같은 모델/평가 | 학습 곡선과 불확실성 | 시험한 과제/배치에 한정 |
| 더 나은 회복 | 짝지은 실패 교란 | 회복 성공/시간 | 명시된 실패 유형 |
| 더 안전한 운용 | 대등한 노출과 hazard 정의 | 위반, near miss, 심각도 | 인증이 아님 |

**수정 전:** “주장: 강건한 파지. 증거: 성공 영상.” **문제:** 변동 조건과 분모가 보이지 않는다. **수정 후:** “주장: 명시한 표면 이동에서 회복 개선. 증거: 보지 못한 조건별 짝지은 시도, 실패 기록, 불확실성.”

**수정 전:** “주장: 촉각 마찰 추정이 원인. 증거: 전체 모델과 구형 시스템 비교.” **문제:** 통제하지 않은 축도 달라진다. **수정 후:** “주장: 접촉 중 갱신의 이점. 증거: 같은 계획기에서 갱신을 켜고 끈 비교, 대등한 센싱·연산, 갱신이 결정으로 이어지는 진단.”

수집 전에 표를 쓰면 지금 얻을 수 없는 증거가 드러난다. **여기서 얻는 독법.** 빠진 비교는 설계상의 선택이다. 비교를 추가하거나, 주장을 줄이거나, 답하지 못한 질문으로 남긴다. 글을 쓴 뒤 표를 채우면 보기 좋지만 무관한 지표가 이 선택을 가릴 수 있다.

계산 예제는 RS1에 대해 이 표를 채우며 열 셋 — 주장 유형, 파일럿의 증거, 판정 — 을 더한다. 누가 초록을 쓰기도 전에 파일럿이 채우지 못하는 행이 드러난다.

### 읽고 나면 말할 수 있어야 하는 것

- topic을 반증 가능한 질문으로 변환할 수 있다
- 선행 구현의 부재가 자동으로 research gap이 아닌 이유를 설명할 수 있다
- 가설·엔지니어링 목표·기여를 구분할 수 있다
- 주장 유형을 그것이 요구하는 증거와 짝지을 수 있다
- robust·general 같은 단어를 쓰기 전에 범위와 가정을 명시할 수 있다
- RS1에 관한 모호한 주장을 철회 규칙까지 갖춘 반증 가능한 주장으로 고쳐 쓰고, 파일럿으로 주장–증거 표를 채울 수 있다
- 조작적 정의는 문턱까지 포함해 데이터보다 먼저 고정해야 하는 이유를 설명할 수 있다

### 스스로 점검

1. "디퓨전이 로봇 계획에 도움이 되는가?"를 시험 가능한 질문으로 다시 써라.
2. 더 큰 벤치마크 점수가 주장한 기전을 확립하지 못할 수 있는 이유는?
3. 데이터 효율 주장을 반증하는 것은 무엇인가?
4. RS1 파일럿은 평균 최대 접촉력의 차이에 대해 $p = 0.003$을 준다. 그런데도 "B가 더 안전하다"가 허락되지 않는 이유는?
5. RS1의 성공 선은 10 N에 있다. 그 선을 파일럿 전에 그어야 했던 이유는 무엇이고, 그러지 않았을 때 어떻게 되는지 계산 예제 2단계의 표는 무엇을 보여 주는가?

> [!tip]- 정답 · Answers
> 1. 과제/분포, 디퓨전 개입, 짝지은 비교 대상, 데이터 예산, 지표, 폐루프 조건을 명시한다.
> 2. 여러 구성요소나 데이터가 함께 달라졌을 수 있다 — 점수만으로는 원인을 분리하지 못한다.
> 3. 미리 선언한 저데이터 예산들에서 대등한 컴퓨트/모델/평가 아래 이점이 없거나, 이점이 불평등한 데이터·튜닝으로 설명되는 것.
> 4. p-값은 대리 결과 하나, 곧 최대 접촉력에 대한 것이고, 팔 하나, 패널 하나, 시행 스무 번 위의 것이다. "더 안전하다"는 안전 주장이고, §4는 안전 주장에 hazard 정의, 노출, 심각도, 감독의 역할이 필요하다고 말한다. 또 p-값은 효과의 크기도, B가 더 나을 확률도 아니다([[02-foundations/probability|3. 확률 §6]]). $p = 0.003$이 허락하는 것은 표의 2행이다. 이 파일럿에서 B의 평균 최대 접촉력이 3.16 N 낮았다(95% 신뢰구간 1.28–5.04 N).
> 5. 선은 주장의 조작적 정의의 일부이므로, 데이터를 본 뒤에 그으면 데이터가 주장을 고르게 된다. 같은 스무 시행이 미리 정한 10 N에서는 Fisher $p = 0.30$을, 9 N에서는 $p = 0.005$를 준다. A의 최댓값 넷이 9 N과 10 N 사이에 있기 때문이다. 보고 나서 고른 선은 이미 일어나지 않았다고 확인된 결과만 금지할 뿐이다.

### 과제 · Problem set

Tier B. RS1 위의 손 계산이다. 이 페이지, 선수 지식, 이 페이지의 대상에 고정한 파일럿만 쓴다. 계산 예제와 다른 주장이다. 계산 예제는 선을 10 N에 두고 평균을 시험했고, 여기서는 선을 옮긴 다음 선이 아예 없는 주장을 시험한다.

1. **그리기.** 위 그림의 두 번째 장을, 성공 선을 10 N 대신 12 N에 두고 다시 그린다. 줄마다 성공을 세고, 범주가 바뀐 점에 모두 동그라미를 친다. 그다음 이 정의 아래의 부차 주장에 대해 주장의 해부도를 다시 그린다. 어느 괄호가 바뀌었고 어느 괄호가 그대로인가?
2. **유도.** 공저자가 문턱 없는 주장을 제안한다. "B의 접촉은 A의 접촉보다 부드럽다." (가) 이를 $\theta = P(Y_A > Y_B)$, 곧 무작위로 고른 A 시행이 무작위로 고른 B 시행보다 최댓값이 높을 확률에 대한 반증 가능한 주장으로 고쳐 쓰고, $S$, $I$, $C$, $Y$와 철회 규칙을 밝힌다. (나) $10 \times 10$개의 교차 쌍 전부에서 A의 최댓값이 더 높은 경우를 세어 파일럿으로 $\theta$를 추정한다. (다) "차이 없음"을 뜻하는 $\theta$의 값은 무엇이고, 이 주장이 선의 위치에 의존하지 않는 이유는?
3. **해석.** 초록 초안에 이렇게 적혀 있다. "임피던스 제어는 과도한 접촉력을 없앤다." (가) §4의 어느 주장 유형이며, "과도한"이 RS1의 10 N을 뜻한다면 정확히 어떤 결과를 금지하는가? (나) 파일럿은 이 주장을 지지하는가, 지지하지 못하는가, 반박하는가? (다) 과도한 힘에 대해 파일럿이 실제로 허락하는 가장 강한 문장을 쓰고, 신뢰성 버전("B는 접촉의 10% 미만에서만 10 N을 넘는다")에는 무엇이 필요한지 말한다.

> [!note]- 그리는 법 · How to draw it
> - **조작적 정의를 한 축 위에:** 5 N에서 15 N까지의 가로 힘 축을 긋고, 한 줄에 A의 최대 접촉력 열 개를 점으로, 그 아래 줄에 B의 열 개를 찍는다. 점은 움직이지 않고 선만 움직인다.
> - **선이 먼저다:** 점을 하나라도 찍기 전에 성공 선을 긋고 이름을 붙인다. 선은 주장의 일부이기 때문이다 — 계산 예제의 선에는 *10 N, 파일럿 전에 고정*이라고 적혀 있다.
> - **줄마다 개수를 선 왼쪽에 적는다.** 계산 예제에서는 6/10과 9/10.
> - **판정이 흔들리는 곳을 표시한다:** 계산 예제는 A의 최댓값 넷(9.1, 9.4, 9.8, 9.9)이 들어 있는 9–10 N 띠를 칠한다. 선을 그 띠 너머로 옮기면 판정이 움직인다.
> - **주장의 해부도:** 주장을 가로로 적고 구절마다 아래에서 괄호를 친다 — S(범위), I(개입), C(비교 대상), Y(결과, 문턱까지) — 그리고 문장 전체 아래에 주장을 철회시킬 결과를 적는 다섯 번째 괄호 R을 둔다.
> - **구절이 못 박지 못한 괄호는 모두 비워 둔다:** 모호한 초안의 "로봇 접촉"과 "더 안전하게"는 S와 Y를 비워 두고, C와 R은 아예 없다.

> [!tip]- 정답 · Solutions
> 1. 12 N에서 A의 성공은 8.1, 9.4, 9.8, 7.7, 9.9, 9.1, 11.3으로 7/10이고, B의 최댓값 열 개는 모두 선 아래라 10/10이다. 범주가 바뀐 점은 A의 11.3과 B의 10.6뿐이니 둘에 동그라미를 친다. 해부도에서 S, I, C는 그대로다. 문턱은 결과의 조작적 정의의 일부이므로 Y 괄호가 바뀌었고, 철회 규칙이 Y 위에 적혀 있으므로 R도 함께 바뀌었다. 그러니 "12 N에서의 성공"은 "10 N에서의 성공"과 다른 주장이다. 10 N은 파일럿 전에 고정했으므로, 12 N 버전은 미리 정한 결과 옆에 이름을 붙인 민감도 분석으로만 보고할 수 있고 그 자리를 대신할 수는 없다.
> 2. (가) "RS1 시행에서 400 N/m 패널로 다가가는 P2에 대해, A의 접촉이 B의 접촉보다 최댓값이 높은 경우가 그 반대보다 많다. 곧 $\theta = P(Y_A > Y_B) > 0.5$." S, I, C는 계산 예제와 같다. Y는 여전히 최대 접촉력이지만 이제 선과 비교하지 않고 시행 쌍끼리 비교한다. 확인 실험 전에 고정하는 철회 규칙: $\theta = 0.5$에 대한 양측 Mann–Whitney 검정([[02-foundations/probability|3. 확률 §6]])이 $\alpha = 0.05$에서 기각하지 못하면 철회한다. (나) 두 줄을 정렬한다. B의 가장 낮은 여섯(5.9, 6.2, 6.6, 6.8, 7.1, 7.5)은 A의 열 개 모두보다 낮아 $6 \times 10 = 60$쌍이다. B의 7.9와 8.0은 A의 아홉보다 낮아(A의 7.7만 더 낮다) 18쌍, B의 8.4는 A의 여덟보다 낮아(A의 7.7과 8.1이 더 낮다) 8쌍, B의 10.6은 A의 넷(11.3, 12.6, 13.9, 14.8)보다 낮아 4쌍이다. 동점이 없으므로 $\hat\theta = (60 + 18 + 8 + 4)/100 = 90/100 = 0.90$이다. (다) $\theta = 0.5$, 곧 A 시행이 더 낮을 가능성과 더 높을 가능성이 같은 경우다. 이 주장은 최댓값들의 순서만 쓰므로 성공 선을 어디로 옮겨도 쌍 비교 백 개는 하나도 바뀌지 않는다. [[02-foundations/ml-practice|9. ML 실무]]의 계산 예제에 나오는 AUC와 같은 쌍 세기 양이고, A의 최댓값이 양성 역할을 한다.
> 3. (가) 안전/신뢰성 주장이고, 게다가 보편 주장이다. "없앤다"는 10 N을 넘는 B의 접촉을 하나도 허용하지 않으므로 그런 접촉 하나가 주장을 반박한다. (나) 반박된다. B의 6번 시행이 10.6 N이었다. 주장은 반증 가능했고, 파일럿이 그것을 반증했다. (다) "파일럿에서 10 N을 넘은 시행은 A 아래 10회 중 4회에서 B 아래 10회 중 1회로 줄었다"는 기술적 개수로서 허락된다(계산 예제 표의 1행). 비교 버전 "B가 10 N을 덜 자주 넘는다"는 3행이고 $p = 0.30$에서 허락되지 않는다. 신뢰성 버전에는 노출이 필요하다. B가 정말로 접촉의 10%에서 10 N을 넘는다면 접촉 $n$번이 모두 선 아래에 머물 확률은 $0.9^n$이고, 이것은 $n = \ln 0.05 / \ln 0.9 = 28.4$에 가서야 0.05로 떨어진다. 그러니 초과율의 95% 상한이 10% 아래로 내려가려면 B는 초과가 전혀 없는 접촉 29회가 필요하다. 파일럿처럼 초과를 하나 허용하면 그 수는 46으로 오른다. $0.9^n + n(0.1)(0.9)^{n-1} \le 0.05$를 만족하는 가장 작은 $n$이다(46에서 $0.048$, 45에서 $0.052$).

### 출처

- [DARPA — Heilmeier Catechism](https://www.darpa.mil/about/heilmeier-catechism) — 무엇을 하려는지, 무엇이 새로운지, 왜 중요한지를 묻는 고전적 체크리스트
- [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) — 주요 학회가 주장–증거 정렬을 어떻게 운영화하는지
- Karl R. Popper, *Logik der Forschung* (Springer, 1934); 영어판 *The Logic of Scientific Discovery* (Hutchinson, 1959) — 반증 가능성: 어떤 가능한 관찰이 진술에 반할 수 있을 때에만 그 진술은 경험적이다
- W. Scott Richardson, Mark C. Wilson, Jim Nishikawa & Robert S. Hayward, "The well-built clinical question: a key to evidence-based decisions", *ACP Journal Club* 123(3):A12–A13 (1995) — 연구 질문 정의가 빌려 온 PICO 칸
- Joseph P. Simmons, Leif D. Nelson & Uri Simonsohn, "False-positive psychology: undisclosed flexibility in data collection and analysis allows presenting anything as significant", *Psychological Science* 22(11):1359–1366 (2011) — 데이터를 본 뒤 고른 문턱이 p-값을 무효로 만드는 이유
