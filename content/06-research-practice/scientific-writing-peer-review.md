---
title: 4. Scientific Writing & Peer Review
tags: [research, writing, peer-review]
study-depth: Working
wiki-support: Working
depth-goal: "Apply the procedure when forming claims, running experiments, analyzing failure, and writing."
mastery-when: "Mastery means consistently producing defensible work, not memorizing the page."
---

> [!note] Prerequisites · 선수 지식
> [[06-research-practice/research-questions-claims|Research Questions & Claims]] (RS1 and the claim this page writes up) · [[06-research-practice/experimental-design-reproducibility|Experimental Design]] · [[06-research-practice/failure-analysis-system-evaluation|Failure Analysis]] · [[02-foundations/probability|3. Probability §6]] (p-value, confidence interval, the test-choice table) · [[02-foundations/ml-practice|9. ML Practice §4]] (standard deviation against standard error)
> [[06-research-practice/research-questions-claims|연구 질문과 주장]](RS1과 이 페이지가 논문으로 쓰는 주장) · [[06-research-practice/experimental-design-reproducibility|실험 설계]] · [[06-research-practice/failure-analysis-system-evaluation|실패 분석]] · [[02-foundations/probability|3. 확률 §6]](p-값, 신뢰구간, 검정 선택 표) · [[02-foundations/ml-practice|9. ML 실무 §4]](표준편차와 표준오차의 차이)

## English

*Stands on [[06-research-practice/research-questions-claims|1. Research Questions & Claims]], which turned RS1 into a claim, and on [[02-foundations/probability|3. Probability §6]]. Here RS1's claim becomes a paper: one argument, one results table, one figure, one limitations paragraph and one review exchange, all on the pilot's twenty numbers.*

Scientific writing aligns a claim with evidence and makes its boundary inspectable. Clarity is not decoration: ambiguous scope, hidden assumptions, and missing protocol prevent readers from evaluating the work.

> [!note] First pass · 처음이라면
> Read the running object, then the worked case: RS1's results table, in which every number is paired with the one sentence it licenses and the neighbouring sentence it does not. Then §4 (the figure), §6 (the limitations paragraph) and §7 (the review), each of which now carries its RS1 instance. Sections 1–3, 5, 8 and 9 are the general craft; read §8 before your first rebuttal.

### Running object · 이 페이지의 대상

**RS1**, the running study of Research Practice, restated in full from [[06-research-practice/research-questions-claims|1. Research Questions & Claims]]. *Question:* does impedance control (**B**) make the planar arm's contact with a panel safer than position control with a force-threshold stop (**A**)? *Plant:* **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (planar 2R, unit links, a 1 kg point mass at the end of each link), against a panel with **P3**'s wall stiffness, $k_w = 400$ N/m. *Trial:* the arm approaches the panel and makes contact; the outcome is the peak contact force in newtons, and a trial succeeds when that peak is at most 10 N. *Pilot:* ten unpaired trials per controller. **The data are illustrative — invented for teaching and frozen — not a measurement of any real controller.**

| Trial | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A — position control + force-threshold stop (N) | 8.1 | 9.4 | 12.6 | 9.8 | 13.9 | 7.7 | 9.9 | 9.1 | 14.8 | 11.3 |
| B — impedance control (N) | 6.2 | 7.9 | 8.4 | 5.9 | 7.1 | 10.6 | 6.8 | 7.5 | 8.0 | 6.6 |

| Controller | Successes (peak ≤ 10 N) | Mean (N) | Sample sd (N) | Median (N) |
|---|---:|---:|---:|---:|
| A | 6/10 | 10.66 | 2.414 | 9.85 |
| B | 9/10 | 7.50 | 1.356 | 7.30 |

**The claim being written up** is the one page 1 ended on, with its outcomes ranked before the pilot: primary, the mean peak contact force (B lower than A); secondary, the share of contacts at or below 10 N. The pilot licenses the first inside its boundary and not the second, and this page's job is to write exactly that.

*Scope: this page teaches how to write RS1's claim up — the paper-level argument, one results table and one figure for the pilot, the sentence each number licenses, a limitations paragraph, and one review exchange. It does not teach how the claim was formed ([[06-research-practice/research-questions-claims|1. Research Questions & Claims]]), how the experiment is designed and sized ([[06-research-practice/experimental-design-reproducibility|2. Experimental Design]]), tests beyond the three used here ([[02-foundations/probability|3. Probability §6]]), or where to submit ([[06-research-practice/venue-strategy|5. Venue Strategy]]).*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 290" style="max-width:100%;height:auto" role="img" aria-label="RS1 pilot as the paper's figure: every trial's peak contact force as a dot on a 5 to 15 N axis, the 10 N line fixed before the pilot with the success side shaded, each controller's mean with its 95% interval, and beside it the difference of means, 3.16 N with Welch 95% interval 1.28 to 5.04">
  <rect x="72" y="30" width="150" height="128" fill="currentColor" fill-opacity="0.08"/>
  <line x1="72" y1="158" x2="372" y2="158" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M72 158V163 M102 158V163 M132 158V163 M162 158V163 M192 158V163 M222 158V163 M252 158V163 M282 158V163 M312 158V163 M342 158V163 M372 158V163" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="72" y="176" font-size="11" text-anchor="middle" fill="currentColor">5</text>
  <text x="102" y="176" font-size="11" text-anchor="middle" fill="currentColor">6</text>
  <text x="132" y="176" font-size="11" text-anchor="middle" fill="currentColor">7</text>
  <text x="162" y="176" font-size="11" text-anchor="middle" fill="currentColor">8</text>
  <text x="192" y="176" font-size="11" text-anchor="middle" fill="currentColor">9</text>
  <text x="222" y="176" font-size="11" text-anchor="middle" fill="currentColor">10</text>
  <text x="252" y="176" font-size="11" text-anchor="middle" fill="currentColor">11</text>
  <text x="282" y="176" font-size="11" text-anchor="middle" fill="currentColor">12</text>
  <text x="312" y="176" font-size="11" text-anchor="middle" fill="currentColor">13</text>
  <text x="342" y="176" font-size="11" text-anchor="middle" fill="currentColor">14</text>
  <text x="372" y="176" font-size="11" text-anchor="middle" fill="currentColor">15</text>
  <text x="222" y="193" font-size="11" text-anchor="middle" fill="currentColor">peak contact force per trial (N)</text>
  <line x1="222" y1="22" x2="222" y2="158" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="228" y="28" font-size="11" fill="currentColor">10 N, fixed before the pilot</text>
  <text x="77" y="43" font-size="11" opacity="0.8" fill="currentColor">success: peak ≤ 10 N</text>
  <circle cx="369" cy="24" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="369" y="28" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">1</text>
  <circle cx="153" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="165" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="195" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="204" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="216" cy="61.5" r="3.6" fill="currentColor"/>
  <circle cx="219" cy="70.5" r="3.6" fill="currentColor"/>
  <circle cx="261" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="300" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="339" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="366" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="99" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="108" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="120" cy="113.5" r="3.6" fill="currentColor"/>
  <circle cx="126" cy="122.5" r="3.6" fill="currentColor"/>
  <circle cx="135" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="147" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="159" cy="113.5" r="3.6" fill="currentColor"/>
  <circle cx="162" cy="122.5" r="3.6" fill="currentColor"/>
  <circle cx="174" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="240" cy="118" r="3.6" fill="currentColor"/>
  <text x="16" y="70" font-size="12.5" font-weight="bold" fill="currentColor">A</text>
  <text x="16" y="122" font-size="12.5" font-weight="bold" fill="currentColor">B</text>
  <circle cx="38" cy="66" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="38" y="70" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">2</text>
  <path d="M190 86 H293.6 M190 82 V90 M293.6 82 V90" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M241.8 81 L246.8 86 L241.8 91 L236.8 86 Z" fill="currentColor"/>
  <path d="M117.9 138 H176.1 M117.9 134 V142 M176.1 134 V142" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M147 133 L152 138 L147 143 L142 138 Z" fill="currentColor"/>
  <text x="301.6" y="90" font-size="11" opacity="0.85" fill="currentColor">mean, 95% CI</text>
  <circle cx="383.6" cy="86" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="383.6" y="90" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">3</text>
  <line x1="446" y1="36" x2="446" y2="158" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <line x1="430" y1="158" x2="542" y2="158" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M430 158V163 M446 158V163 M462 158V163 M478 158V163 M494 158V163 M510 158V163 M526 158V163 M542 158V163" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="446" y="176" font-size="11" text-anchor="middle" fill="currentColor">0</text>
  <text x="478" y="176" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <text x="510" y="176" font-size="11" text-anchor="middle" fill="currentColor">4</text>
  <text x="542" y="176" font-size="11" text-anchor="middle" fill="currentColor">6</text>
  <text x="486" y="193" font-size="11" text-anchor="middle" fill="currentColor">A − B (N)</text>
  <text x="495" y="28" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">difference of means</text>
  <circle cx="430.9" cy="24" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="430.9" y="28" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">3</text>
  <path d="M466.5 96 H526.6 M466.5 92 V100 M526.6 92 V100" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M496.6 91 L501.6 96 L496.6 101 L491.6 96 Z" fill="currentColor"/>
  <text x="496.6" y="84" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">3.16 N</text>
  <text x="496.6" y="116" font-size="11" text-anchor="middle" fill="currentColor">[1.28, 5.04]</text>
  <text x="496.6" y="130" font-size="11" text-anchor="middle" opacity="0.8" fill="currentColor">Welch 95% CI</text>
  <circle cx="23" cy="214" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="23" y="218" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">4</text>
  <text x="38" y="218" font-size="11" font-style="italic" opacity="0.9" fill="currentColor">Figure 1. RS1 pilot (illustrative data): peak contact force (N) of every trial, arm P2 against a 400 N/m</text>
  <text x="38" y="233" font-size="11" font-style="italic" opacity="0.9" fill="currentColor">panel, ten unpaired trials per controller, none excluded. Dots are single trials; the diamond and bar</text>
  <text x="38" y="248" font-size="11" font-style="italic" opacity="0.9" fill="currentColor">under each row are the mean and its 95% t-interval (A 10.66 N [8.93, 12.39], B 7.50 N [6.53, 8.47]).</text>
  <text x="38" y="263" font-size="11" font-style="italic" opacity="0.9" fill="currentColor">Dashed line: the 10 N success threshold, fixed before the pilot; the shaded side counts as success.</text>
  <text x="38" y="278" font-size="11" font-style="italic" opacity="0.9" fill="currentColor">Right: the difference of means A − B, 3.16 N, with its Welch 95% interval [1.28, 5.04].</text>
</svg>

RS1's pilot as the paper's one figure: every trial's peak contact force is a dot, A's ten on the upper row and B's ten below, against the 10 N success line fixed before the pilot, so six of A's dots and nine of B's fall on the shaded success side. Under each row sit the mean and its 95% t-interval, A 10.66 N [8.93, 12.39] and B 7.50 N [6.53, 8.47], and on the right is the number the claim is about, the difference of means, 3.16 N with Welch 95% interval [1.28, 5.04]. The circled numbers mark the four parts a results figure owes its reader: the line fixed in advance, every trial, the interval that answers the claim, and a caption that reads without the body text.

### Worked case · 대상으로 한 번 끝까지

The results table for RS1's pilot, with exact numbers, then where each number comes from, then the sentence each number licenses.

**Step 1 — the table.**

| Quantity | A | B | Comparison |
|---|---:|---:|---|
| Trials (unpaired) | 10 | 10 | — |
| Peak force ↓, mean ± sd (N) | 10.66 ± 2.41 | 7.50 ± 1.36 | A − B $= 3.16$ N, Welch 95% CI $[1.28,\ 5.04]$; $t = 3.61$, 14.2 df, $p = 0.003$ |
| Peak force ↓, median [min, max] (N) | 9.85 [7.7, 14.8] | 7.30 [5.9, 10.6] | — |
| Successes, peak ≤ 10 N ↑ | 6/10 | 9/10 | B − A $= +0.30$, Newcombe 95% CI $[-0.08,\ 0.60]$; Fisher exact $p = 0.30$ |
| Success rate ↑, Wilson 95% CI | 0.60 [0.31, 0.83] | 0.90 [0.60, 0.98] | the intervals overlap on $[0.60,\ 0.83]$ |

*Table 1. RS1 pilot on arm P2 against a 400 N/m panel, ten unpaired trials per controller (illustrative data). Arrows give the direction of improvement. Peak force: sample mean ± sample standard deviation, and median with the range; the comparison is the difference of means with a Welch 95% confidence interval and a two-sided p. Success: peak at most 10 N, the threshold fixed before the pilot; rates carry Wilson 95% score intervals, and the comparison is the difference of rates with Newcombe's 95% interval and Fisher's exact test, two-sided. All twenty trials are reported and none was excluded.*

**Step 2 — where each number comes from.** Four procedures, each defined once here because Table 1 prints its output.

> [!info] Definition — Wilson score interval
> **What kind of thing it is:** a confidence-interval procedure, in the sense of [[02-foundations/probability|3. Probability §6]], for a success probability $p$ from $k$ successes in $n$ trials. **Defining conditions:** (1) the $n$ trials are independent; (2) they share one success probability $p$; (3) the interval is the set of every $p$ that a two-sided score test at level $\alpha$ would not reject, where the score statistic $(\hat p - p)/\sqrt{p(1-p)/n}$ uses the standard error at the candidate $p$, not at $\hat p$. Solving that quadratic in $p$ gives
> $$\frac{\hat p + \dfrac{z^2}{2n} \pm z\sqrt{\dfrac{\hat p(1-\hat p)}{n} + \dfrac{z^2}{4n^2}}}{1 + \dfrac{z^2}{n}}$$
> with $\hat p = k/n$ and $z = 1.96$ for 95% (Wilson 1927). The centre is a weighted average of $\hat p$ and $\tfrac12$, so it is pulled toward the middle, and the interval never leaves $[0, 1]$.
> **Example.** B's 9/10: $z^2/n = 0.384$, so the centre is $(0.9 + 0.192)/1.384 = 0.789$ and the half-width $1.96\sqrt{0.009 + 0.0096}/1.384 = 0.193$, giving $[0.596,\ 0.982]$. A's 6/10: centre $0.572$, half-width $0.260$, giving $[0.313,\ 0.832]$.
> **Non-example.** The Wald interval $\hat p \pm z\sqrt{\hat p(1-\hat p)/n}$ uses the standard error at $\hat p$. For 9/10 it is $0.9 \pm 0.186 = [0.714,\ 1.086]$, which admits success probabilities above 1, and at 10/10 it collapses to the single point 1.
> **Why it matters.** At ten trials the two procedures disagree by more than 0.1 at each end ($0.714$ against $0.596$ below, $1.086$ against $0.982$ above): a table printing the Wald interval tells the reader B's rate is at least 0.71, when 9 of 10 is compatible with 0.60 (Brown, Cai & DasGupta 2001).

> [!info] Definition — Newcombe interval for a difference of two rates
> **What kind of thing it is:** a confidence-interval procedure for $p_B - p_A$, the difference between two success probabilities, built from the two Wilson intervals. **Defining conditions:** (1) two independent groups of trials, each satisfying the Wilson conditions; (2) each group's Wilson limits $[l, u]$ computed first; (3) each end of the difference's interval combines the two distances that pull the difference in that direction — for the lower end, how far B's rate could fall ($\hat p_B - l_B$) and how far A's could rise ($u_A - \hat p_A$):
> $$\Big[\ \hat d - \sqrt{(\hat p_B - l_B)^2 + (u_A - \hat p_A)^2}\ ,\ \ \hat d + \sqrt{(u_B - \hat p_B)^2 + (\hat p_A - l_A)^2}\ \Big], \qquad \hat d = \hat p_B - \hat p_A$$
> which is Newcombe's hybrid score method (Newcombe 1998). The two distances add in quadrature because the two groups are independent, so their uncertainties add like variances.
> **Example.** RS1: $\hat d = 0.30$. Lower end $0.30 - \sqrt{(0.9 - 0.596)^2 + (0.832 - 0.6)^2} = 0.30 - \sqrt{0.0924 + 0.0538} = 0.30 - 0.382 = -0.08$; upper end $0.30 + \sqrt{(0.982 - 0.9)^2 + (0.6 - 0.313)^2} = 0.30 + \sqrt{0.0067 + 0.0824} = 0.30 + 0.298 = 0.60$.
> **Non-example.** The two Wilson intervals' overlap, $[0.60,\ 0.83]$, read as the answer. Overlap of two intervals is not the interval of their difference; two intervals can overlap while the difference's interval excludes zero.
> **Why it matters.** It says what the pilot is compatible with: anything from B succeeding slightly less often than A to 60 points more often. That range, not the p-value alone, is why "no effect" is as unlicensed as "B succeeds more often".

> [!info] Definition — Welch interval for a difference of means
> **What kind of thing it is:** a confidence-interval procedure for $\mu_A - \mu_B$, the difference between two population means, from two independent samples. **Defining conditions:** (1) the two samples are independent of each other (unpaired); (2) each sample mean is roughly normal, so the data are not heavily skewed or dominated by outliers at this $n$; (3) the two variances are **not** assumed equal, so each sample keeps its own $s^2$. Then
> $$\bar y_A - \bar y_B \pm t_{0.975,\,\nu}\,\mathrm{SE}, \qquad \mathrm{SE} = \sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}, \qquad \nu = \frac{\mathrm{SE}^4}{\dfrac{(s_A^2/n_A)^2}{n_A - 1} + \dfrac{(s_B^2/n_B)^2}{n_B - 1}}$$
> where $\bar y$, $s$ and $n$ are each sample's mean, standard deviation and size, $\nu$ is the Welch–Satterthwaite degrees of freedom, and $t_{0.975,\nu}$ is the Student-$t$ quantile (Welch 1947; Satterthwaite 1946). SE adds the two variances because the samples are independent, and $\nu$ falls toward the noisier sample's $n - 1$ when its variance dominates, so an unequal pair is judged with a wider $t$.
> **Example.** RS1: $s_A^2/n_A = 2.414^2/10 = 0.583$ and $s_B^2/n_B = 1.356^2/10 = 0.184$, so $\mathrm{SE} = \sqrt{0.767} = 0.876$ N and $\nu = 0.767^2/(0.583^2/9 + 0.184^2/9) = 14.2$. With $t_{0.975,\,14.2} = 2.142$ the interval is $3.16 \pm 1.88 = [1.28,\ 5.04]$ N, and $t = 3.16/0.876 = 3.61$ gives a two-sided $p = 0.003$.
> **Non-example.** Two ±1 sd bars that overlap. A's $10.66 \pm 2.41$ spans $[8.25,\ 13.07]$ and B's $7.50 \pm 1.36$ spans $[6.14,\ 8.86]$; they overlap on $[8.25,\ 8.86]$, yet the interval for the difference clears zero by more than a newton. A standard deviation describes the spread of single trials, not the uncertainty of a mean ([[02-foundations/ml-practice|9. ML Practice §4]]).
> **Why it matters.** The claim is about a difference, so the table must carry the difference's interval; neither arm's own interval, nor its bars, answers the question.

> [!info] Definition — Fisher's exact test
> **What kind of thing it is:** a hypothesis test, a p-value procedure in the sense of [[02-foundations/probability|3. Probability §6]], for whether two success probabilities differ, computed from a $2 \times 2$ table of counts. **Defining conditions:** (1) two independent groups of trials; (2) a binary outcome per trial; (3) the null hypothesis that both groups share one success probability; (4) the test conditions on the table's margins — the group sizes $n_A$, $n_B$ and the total number of successes $m$ — so that under the null the number $X$ of successes in group A is hypergeometric,
> $$P(X = x) = \frac{\binom{n_A}{x}\binom{n_B}{m - x}}{\binom{n_A + n_B}{m}}$$
> and the two-sided $p$ is the total probability of every table at most as probable as the observed one (Fisher 1935).
> **Example.** RS1: $n_A = n_B = 10$, $m = 15$, observed $x = 6$. The possible $x$ run from 5 to 10 with numerators $252, 2100, 5400, 5400, 2100, 252$ over $\binom{20}{15} = 15504$. The observed table has probability $2100/15504 = 0.135$, the tables at most that probable are $x = 5, 6, 9, 10$, and so $p = (252 + 2100 + 2100 + 252)/15504 = 4704/15504 = 0.303$.
> **Non-example.** The chi-square test on the same table. It approximates the same null with a large-sample distribution, and the usual rule of thumb asks for an expected count of at least five in every cell; RS1's two failure cells expect $10 \times 5/20 = 2.5$ each. At ten trials per arm the approximation is the wrong tool, and the exact test is the one [[02-foundations/probability|3. Probability §6]]'s table names for two unpaired success counts.
> **Why it matters.** It is the honest p-value for the success row, and at $0.30$ it is what keeps "B succeeds more often" out of the abstract.

**Step 3 — the sentence each number licenses.**

> [!info] Definition — licensed sentence
> **What kind of thing it is:** a relation between a sentence in a paper and a number in its results. The number *licenses* the sentence when the sentence says no more than the number measured. **Defining conditions — all four:** (1) *same quantity*: the sentence is about the quantity the number estimates, under its operational definition; (2) *same comparison*: any comparison in the sentence is the one that produced the number, with the same arms and protocol; (3) *scope inside the sample*: the population, conditions and evidence rung the sentence speaks for lie inside those the trials covered; (4) *strength inside the uncertainty*: the certainty the sentence implies is no greater than the interval or test attached to the number allows.
> $$\text{licensed}(s, x) \iff \text{qty}(s) = \text{qty}(x) \ \wedge\ \text{cmp}(s) = \text{cmp}(x) \ \wedge\ \text{scope}(s) \subseteq \text{scope}(x) \ \wedge\ \text{strength}(s) \le \text{strength}(x)$$
> where $s$ is the sentence, $x$ the number together with its interval or test, qty the quantity and cmp the comparison, so failing any one condition is enough to unlicense the sentence.
> **Example.** "B stayed at or below 10 N in 9 of 10 pilot trials", licensed by B's count 9/10.
> **Non-example.** "B is safer", from the same 9/10. It fails condition (1), because safety is not the quantity counted, and condition (3), because one arm, one panel and ten trials do not cover the places where "safer" will be read.
> **Why it matters.** It is §1's picture of the claim box inside the evidence box, checked one sentence at a time. Every "the claim is too strong" review names a sentence that fails one of the four.

| Number in Table 1 | The sentence it licenses | The neighbour it does not | Condition the neighbour fails |
|---|---|---|---|
| B: 9/10 | "B stayed at or below 10 N in 9 of 10 pilot trials." | "B is safer." | (1) quantity, (3) scope |
| B: 0.90 [0.60, 0.98] | "Under this protocol, B's success probability is plausibly anywhere from 0.60 to 0.98." | "B succeeds in 90% of contacts." | (4) strength: the interval reaches down to 0.60 |
| A: 6/10 | "A did so in 6 of 10." | "A fails 40% of the time." | (3) and (4): a population rate from ten trials, without its interval [0.31, 0.83] |
| 3.16 N [1.28, 5.04] | "B's mean peak force was 3.16 N lower than A's (95% CI 1.28 to 5.04 N)." | "B reduces contact force by 30%." | (1): the ratio $3.16/10.66 = 0.30$ is a different quantity, with its own unreported interval |
| $t = 3.61$, $p = 0.003$ | "A difference this large would be unlikely if the two mean peak forces were equal (Welch $p = 0.003$)." | "There is a 99.7% chance that B is better." | (1): $p$ is not the probability of a hypothesis ([[02-foundations/probability\|3. Probability §6]]) |
| $+0.30$ $[-0.08,\ 0.60]$, Fisher $p = 0.30$ | "The pilot cannot distinguish the two success rates: B − A $= +0.30$, 95% CI $-0.08$ to $+0.60$ (Fisher exact $p = 0.30$)." | "Impedance control does not change the success rate." | (4): the interval runs up to $+0.60$, so "no change" is only one of the values the data allow |
| B's maximum, 10.6 N | "B's highest pilot peak, 10.6 N, was lower than A's, 14.8 N." | "B keeps contact force below 11 N." | (3): the largest of ten trials is not a bound on the eleventh |

**Step 4 — the Results paragraph, assembled only from licensed sentences.**

> Across ten unpaired trials per controller, B's mean peak contact force was 7.50 N (sd 1.36) against A's 10.66 N (sd 2.41), a difference of 3.16 N (Welch 95% CI 1.28 to 5.04 N; $t = 3.61$, 14.2 df, $p = 0.003$; Table 1, Figure 1). B stayed at or below the prespecified 10 N limit in 9 of 10 trials (Wilson 95% CI 0.60 to 0.98) and A in 6 of 10 (0.31 to 0.83); the pilot cannot distinguish these rates (difference $+0.30$, 95% CI $-0.08$ to $+0.60$; Fisher exact $p = 0.30$). B's highest peak was 10.6 N and A's 14.8 N.

Every number in the paragraph is a cell of Table 1, and every verb is one the table licenses. What the paragraph does not say — safer, 30% lower, never above 11 N — is exactly the right-hand column of Step 3.

### 1. Paper-level argument

| Section | Primary job |
|---|---|
| Abstract | problem, method, strongest scoped evidence, implication |
| Introduction | importance, precise gap, approach, contributions |
| Related work | taxonomy and difference, not a citation inventory |
| Method | variables, assumptions, algorithm/system, reproducible detail |
| Experiments | questions, protocol, baselines, metrics, results |
| Discussion | interpretation, mechanisms, generalization, trade-offs |
| Limitations | boundary of validity and unresolved risks |

Do not let the introduction promise general capability while experiments test one narrow condition.

<svg viewBox="0 0 560 226" style="max-width:100%;height:auto" role="img" aria-label="a claim box drawn inside an evidence box, and the same two boxes with the claim spilling outside the evidence">
  <g font-size="11" fill="currentColor">
    <text x="40" y="16">defensible</text><text x="310" y="16">the common failure</text>
  </g>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.7">
    <rect x="40" y="30" width="210" height="104" rx="4"/>
    <rect x="310" y="46" width="150" height="72" rx="4"/>
  </g>
  <g fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.4">
    <rect x="70" y="52" width="150" height="60" rx="3"/>
    <rect x="340" y="30" width="200" height="104" rx="3" fill-opacity="0.16"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="145" y="46">what the evidence covers</text>
    <text x="145" y="86">what the paper claims</text>
    <text x="400" y="80">what the evidence</text><text x="400" y="93">covers</text>
    <text x="440" y="153">what the paper claims</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none">
    <line x1="440" y1="142" x2="440" y2="136"/>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.85">
    <text x="310" y="170">this overhang is exactly what gets attacked</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="24" y="188">A reviewer is not measuring how large the result is. They are measuring whether one box sits</text>
    <text x="24" y="204">inside the other. Every &#8220;the claim is too strong&#8221; review is a report of the shaded band, and the</text>
    <text x="24" y="220">cheapest fix is almost never a new experiment &#8212; it is narrowing the sentence until it fits.</text>
  </g>
</svg>

An argument is a sequence of dependencies because later claims only make sense after earlier assumptions are visible. For example, [[04-robotics/grasping|Grasping]] moves from closure to grasp quality and then to learning: resisting a wrench is one question, margin against uncertainty is another, and predicting a useful grasp from observations is another. A learned score cannot silently inherit every guarantee of the mechanical model.

**The reading this gives you.** Read a draft by tracing the same chain. Does the problem motivate the chosen model, does the experiment test that model's promised advantage, and does the conclusion stay within those observations? A section can be individually clear while the argument between sections is still missing.

**RS1's argument, section by section.** The section table above, filled for the pilot of the running object. The link RS1's chain must not break is the verb: the abstract says *was lower* (row 2 of the claim–evidence table in [[06-research-practice/research-questions-claims|1. Research Questions & Claims]]'s worked case), never *is safer* (row 4).

| Section | RS1's version |
|---|---|
| Abstract | the licensed sentence that ends page 1's worked case, and nothing stronger |
| Introduction | why peak contact force matters when an arm meets a panel; the gap stated as a comparison: does a compliant controller lower the peak against a soft panel, relative to one that stops on a force threshold, under one protocol? |
| Method | P2 and its frozen numbers, $k_w = 400$ N/m, B's target impedance, A's stop threshold, the approach speed and direction, the trial, and the 10 N line fixed before the pilot |
| Experiments | ten unpaired trials per controller; Table 1 (worked case) and Figure 1 (§4) |
| Discussion | the candidate mechanism, labelled as a candidate (§5) |
| Limitations | the paragraph in §6 |

### 2. Claim–method–evidence sentences

Prefer: “Under held-out material layouts, our policy improved closed-loop success from X to Y over matched BC, with Z trials per condition.”

Avoid: “Our intelligent framework significantly revolutionizes robust construction autonomy.” The second sentence lacks an operational claim, comparator, scope, and evidence.

These are hypothetical sentence templates; fill numerical results only from the actual experiment.

**Before:** “Our method robustly handles diverse objects.” **Problem:** diverse and robust have no test boundary. **After:** “On the held-out object set, we report grasp success against a matched baseline, with attempts and failures separated by material.”

**Before:** “Our architecture improves data efficiency.” **Problem:** an advantage at one training budget does not describe a learning curve. **After:** “We compare the methods across predeclared demonstration budgets with the same evaluation protocol and report uncertainty for each budget.”

**Before:** “The robot autonomously completes the task.” **Problem:** assistance can be hidden inside completion. **After:** “We distinguish autonomous completion from completion after an operator stop or reset, retaining every initiated attempt.”

**The reading this gives you.** A useful sentence gives the reader somewhere to check its nouns and verbs: the split, comparator, metric, and accounting rule. Replace the reporting templates with actual outcomes only when those records exist.

### 3. Related work as a taxonomy

Group papers by problem assumption, representation, supervision, planning/control interface, or evaluation regime. End each group by stating the unresolved distinction your work tests. Chronological lists are useful only when history itself explains the research gap.

**Before:** “Paper A used vision. Paper B added touch. Paper C proposed a new planner. Our system combines their advantages.” **Problem:** the reader learns an inventory but cannot locate an unresolved comparison. The final sentence also promises benefits that combining components alone does not establish.

**After:** “We organize grasping methods by when they obtain contact information. Methods that commit from a pre-contact image depend on assumptions about friction and geometry. Methods that update after contact can react to slip, but their value depends on whether sensing and control respond before failure. Our comparison holds the planner fixed and tests that timing boundary.”

This rewrite uses an assumption and an interface as the organizing axes. Actual papers and citations must then be placed in the appropriate groups. **The reading this gives you.** Ask whether each group changes the experiment you would design. If removing the related-work paragraph leaves the claimed gap unchanged, the paragraph may still be a bibliography in prose.

### 4. Figures and tables

A system figure should show runtime information flow, trained/frozen components, frames or rates when relevant, and train/inference differences. A result table needs units, direction of improvement, uncertainty, trial count, and clear best-value conventions. Captions should be understandable without searching the body for basic definitions. The tools that make such a figure and table — a file that survives printing at a column's width, text at its print size, error bars that say what they are, and entries printed to the digits the data support — are [[02-foundations/tools/latex-figures-references|12.6 Writing Tools §6–§9]].

A visual comparison is persuasive because readers perceive height and separation before inspecting a protocol. That makes missing denominators especially consequential. A success-rate bar from a small sample can look just as precise as a bar supported by much more independent exposure.

For example, show the same grasping result first as a bar and then with trial counts, uncertainty intervals, and individual condition labels. The bar invites a ranking. The expanded display lets a reader see whether the apparent lead is uncertain, whether one material dominates the average, and whether repeated runs share the same objects. Neither display changes the data; the second changes which conclusions are visibly defensible.

**The reading this gives you.** Check the unit behind each dot, bar, or interval. A caption should identify the aggregation, interval procedure, and exclusions. If the plot claims generalization, its condition labels should expose the shift rather than hide it in an overall mean.

**RS1's figure.** The picture at the top of the page as the paper prints it, Figure 1: that picture is the complete drawing, and this version drops the difference-of-means panel, whose number the caption sends to the worked case's Table 1. That table already follows this section's table rules: units, a direction arrow on every outcome row, an interval on every comparison and every rate, $n$ per arm, and a caption that names each procedure.

<svg viewBox="0 0 560 230" style="max-width:100%;height:auto" role="img" aria-label="RS1 pilot: the twenty peak contact forces as dots on one axis, the 10 N success line, and each controller's mean with its 95% confidence interval">
  <rect x="90" y="34" width="220" height="146" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.45">
    <line x1="90" y1="190" x2="530" y2="190"/>
    <line x1="90" y1="190" x2="90" y2="195"/><line x1="134" y1="190" x2="134" y2="195"/><line x1="178" y1="190" x2="178" y2="195"/><line x1="222" y1="190" x2="222" y2="195"/><line x1="266" y1="190" x2="266" y2="195"/><line x1="310" y1="190" x2="310" y2="195"/><line x1="354" y1="190" x2="354" y2="195"/><line x1="398" y1="190" x2="398" y2="195"/><line x1="442" y1="190" x2="442" y2="195"/><line x1="486" y1="190" x2="486" y2="195"/><line x1="530" y1="190" x2="530" y2="195"/>
  </g>
  <line x1="310" y1="30" x2="310" y2="190" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" opacity="0.8"/>
  <g fill="currentColor">
    <circle cx="208.8" cy="80" r="4"/><circle cx="226.4" cy="80" r="4"/><circle cx="270.4" cy="80" r="4"/><circle cx="283.6" cy="80" r="4"/><circle cx="301.2" cy="75" r="4"/><circle cx="305.6" cy="85" r="4"/><circle cx="367.2" cy="80" r="4"/><circle cx="424.4" cy="80" r="4"/><circle cx="481.6" cy="80" r="4"/><circle cx="521.2" cy="80" r="4"/>
    <circle cx="129.6" cy="140" r="4"/><circle cx="142.8" cy="140" r="4"/><circle cx="160.4" cy="140" r="4"/><circle cx="169.2" cy="140" r="4"/><circle cx="182.4" cy="140" r="4"/><circle cx="200.0" cy="140" r="4"/><circle cx="217.6" cy="135" r="4"/><circle cx="222.0" cy="145" r="4"/><circle cx="239.6" cy="140" r="4"/><circle cx="336.4" cy="140" r="4"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6">
    <line x1="263.1" y1="104" x2="414.8" y2="104"/><line x1="263.1" y1="100" x2="263.1" y2="108"/><line x1="414.8" y1="100" x2="414.8" y2="108"/>
    <line x1="157.3" y1="164" x2="242.7" y2="164"/><line x1="157.3" y1="160" x2="157.3" y2="168"/><line x1="242.7" y1="160" x2="242.7" y2="168"/>
  </g>
  <g fill="currentColor">
    <path d="M339.0 99 L344 104 L339.0 109 L334 104 Z"/>
    <path d="M200.0 159 L205 164 L200.0 169 L195 164 Z"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="90" y="206">5</text><text x="134" y="206">6</text><text x="178" y="206">7</text><text x="222" y="206">8</text><text x="266" y="206">9</text><text x="310" y="206">10</text><text x="354" y="206">11</text><text x="398" y="206">12</text><text x="442" y="206">13</text><text x="486" y="206">14</text><text x="530" y="206">15</text>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="20" y="84">A</text><text x="20" y="144">B</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.85">
    <text x="20" y="99">6/10 &#8804; 10 N</text>
    <text x="20" y="159">9/10 &#8804; 10 N</text>
    <text x="96" y="46">success: peak &#8804; 10 N</text>
    <text x="316" y="40">10 N, fixed before the pilot</text>
    <text x="420" y="107">mean, 95% CI</text>
  </g>
  <text x="310" y="224" font-size="11" fill="currentColor" text-anchor="middle">peak contact force per trial (N)</text>
</svg>

*Figure 1. RS1 pilot (illustrative data): the peak contact force of every trial, ten unpaired trials per controller on arm P2 against a 400 N/m panel. Dots are single trials; the diamond and bar under each row are the mean and its 95% t-interval (A: 10.66 N, [8.93, 12.39]; B: 7.50 N, [6.53, 8.47]). The dashed line is the 10 N success threshold, fixed before the pilot, and the shaded side counts as success. The difference of means, 3.16 N with Welch 95% CI [1.28, 5.04], is in Table 1.*

**The figure it replaces.** The default is two bars at the means with ±1 sd whiskers. A's would span 8.25 to 13.07 N and B's 6.14 to 8.86 N, so the whiskers overlap, and a reader who takes overlap for "no difference" concludes the opposite of Table 1 (Cumming & Finch 2005). The bars also hide what the dots show at a glance: four of A's ten peaks stacked just under the line, which is why the success count is fragile, and B's single peak above it (Weissgerber et al. 2015).

### 5. Results versus discussion

Results report measured outcomes. Discussion interprets causes, limitations, and transfer. “Method A had fewer failures” is a result; “tactile feedback enabled earlier slip recovery” is a mechanistic interpretation requiring diagnostic evidence.

**Before:** “The tactile system had fewer failures because it understood contact.” **Problem:** the first clause describes an outcome, while the second invents a mechanism without identifying a measurement. **After, results:** “The tactile condition had fewer observed failures under the matched protocol.” **After, discussion:** “Earlier slip detection is a candidate explanation; synchronized sensing and recovery logs are needed to test it.”

**Before:** “The model generalized, proving it learned transferable physical knowledge.” **Problem:** success on a held-out set does not identify the representation responsible. **After, results:** “The model completed tasks on the declared held-out layouts.” **After, discussion:** “This supports transfer across those layouts; transfer to different materials remains untested.”

These hypothetical examples show why keeping interpretation separate is useful even when both parts are eventually supported. **The reading this gives you.** Ask what could be copied directly from a measurement record and what requires an additional argument. Put the extra argument beside its supporting analysis, with alternatives visible.

**RS1.** *Results:* "B's mean peak contact force was 3.16 N lower than A's (95% CI 1.28 to 5.04 N)." *Discussion:* "A candidate explanation is that B's compliance gives the controller time to shape the contact, which lasts about 0.22 s against a 400 N/m panel under the half-sine model of [[04-robotics/force-compliance-control|13. Force & Compliance Control]]; force–time traces would test it." The first sentence is copied from Table 1. The second needs a measurement the pilot did not record, so it stays a candidate.

### 6. Limitations

State untested environments, data and compute dependencies, hardware assumptions, intervention/reset, failure modes, safety boundaries, and likely distribution shifts. A limitation section does not weaken a paper; it prevents unsupported generalization.

**Before:** “Future work will address more challenging conditions.” **Problem:** the reader cannot tell whether a relevant condition failed or was never tested. **After:** “Wet surfaces were not included in evaluation; the present evidence does not establish transfer when contact friction changes.”

**Before:** “The system occasionally needs human assistance.” **Problem:** the phrase hides the trigger and its effect on the autonomy claim. **After:** “The operator resets the robot after loss of localization. These episodes are retained as failed autonomous attempts, and assisted completion is reported separately.”

These are hypothetical boundaries that a real limitation section should replace with documented conditions. Explain whether the boundary is in sensing, training coverage, control, or evaluation. A reader can then decide which change would be needed to use the method elsewhere.

**The reading this gives you.** A limitation should predict where the claim may stop holding. A future-work promise is useful only after the existing failure or missing evidence is explicit; it cannot substitute for that description.

**RS1's limitations paragraph, as it would appear in the paper.**

> The pilot compared ten unpaired trials per controller on one arm model (P2) against one panel stiffness (400 N/m), with a single setting each of B's target impedance, A's stop threshold, and the approach speed and direction. Peak contact force is a proxy for one hazard, excess force on the panel; it does not measure others, such as clamping or damage to the tool. The success-rate comparison is uninformative at this size: the 95% interval for the difference runs from $-0.08$ to $+0.60$, and a ten-trial design detects a true difference of 0.6 against 0.9 with Fisher's exact test at $\alpha = 0.05$ in only about 15% of runs. Against a stiff structure the contact is about sixteen times shorter under the half-sine model ($\sqrt{10^5/400} = 15.8$), so these results do not establish B's advantage there.

Each sentence names a boundary a reader can check — the model, the stiffness, the parameter settings, the proxy, the power, the contact regime — and none offers future work in place of the boundary. The 15% is exact enumeration over all $11 \times 11$ possible pilot outcomes; the normal approximation gives 33%, and [[06-research-practice/real-world-impact|6. Real-World Impact]] derives both.

### 7. Peer review

Decompose each comment into factual correction, clarity request, missing evidence, scope dispute, or preference. Respond with:

- **Agree:** acknowledge and revise.
- **Clarify:** explain the misunderstanding and improve the paper so others do not share it.
- **Revise:** add analysis, experiment, citation, or limitation.
- **Rebut:** respectfully show why the requested conclusion does not follow, using evidence and scope.

State exactly where the manuscript changed. Do not claim a new experiment proves more than it measures.

For example, “novelty is unclear” can point to different defects. Check whether the nearest prior method is accurately described, whether the manuscript states a concrete difference from it, and whether the experiment establishes why that difference matters. A system contribution can be legitimate even if no network component is new, but integration effort alone does not answer these questions.

A useful response might explain that the difference is the contact-time state update, add the missing comparison to the taxonomy, and narrow the contribution if the experiment only supports the integrated system. **The reading this gives you.** Treat the comment as a request to locate a missing link in the argument. More adjectives about novelty do not supply that link; a traceable assumption, interface, or evaluation difference does.

**RS1 under review.** Suppose the first draft had kept "safer". A reviewer writes: *"The paper concludes that impedance control is safer, but the success rates (9/10 against 6/10) do not differ significantly, and the 10 N threshold is not justified — it looks chosen to favour B."*

Decomposed, the comment holds a **scope dispute** ("safer"), a point of **missing evidence** (the success comparison), and a **factual question** with an implied accusation (where the threshold came from).

**Response (Agree + Clarify + Revise).** "We agree that 'safer' overstated the evidence and have replaced it throughout (abstract, §1, §6) with the measured claim: a lower mean peak contact force in a ten-trial-per-arm pilot on one arm model and one panel stiffness. We also agree that the success rates are not distinguishable (difference +0.30, 95% CI −0.08 to +0.60; Fisher exact p = 0.30); the revised Results now say so in those words, and the Limitations state the design's power at this size, about 0.15 against a true 0.6-versus-0.9 difference. On the threshold: the 10 N line was fixed in the study plan before the pilot (Appendix A, dated), and the prespecified primary outcome was peak force, not success; its difference is 3.16 N (Welch 95% CI 1.28 to 5.04 N). For transparency, the new Table S2 lists the success counts at 8, 9, 11 and 12 N. We draw no inference from them, because a threshold chosen after seeing the data would leave its p-value uninterpretable."

Every element is traceable to a place in the manuscript, and the claim moves toward the data rather than the data toward the claim. Note what the response does not do. It does not switch to the 9 N line, where the same twenty trials give $p = 0.005$ ([[06-research-practice/research-questions-claims|1. Research Questions & Claims]], worked case, Step 2): reporting that as a result would turn the reviewer's suspicion into a fact. Whether an exchange like this happens before the decision is the venue's rule: [[06-research-practice/venue-strategy|5. Venue Strategy §2]] records which venues take a rebuttal, which take a reply with a revised paper, and which take neither, and its worked case weighs that difference when it routes RS1's paper.

### 8. Worked example: one review comment, one compliant response

**Reviewer**: "The 85% success rate is unconvincing — only one scene was tested, and the
baseline appears untuned."

**Response (Agree + Revise + Clarify)**: "We agree the single-scene evaluation limited the claim.
We added two held-out scenes with randomized object layouts (§5.2, Table 3): success is
85%, 80%, 80% (17/20, 16/20, 16/20 per scene; binomial SE ≈ 8 %p at this n, so this sample does not clearly separate scene-level performance). On tuning: the BC baseline used the
same demonstrations, encoder, and a 12-configuration hyperparameter sweep identical to
ours (App. C); we now state this in §5.1. We have narrowed the abstract's claim from
'robust manipulation' to 'consistent success across three tabletop scenes.'"

The SE in the response is the binomial standard error $\sqrt{p(1-p)/n}$ for one scene: with $p = 0.85$ and $n = 20$ it is $\sqrt{0.1275/20} \approx 0.080$, and with $p = 0.80$ it is $\sqrt{0.16/20} \approx 0.089$, so about 8 %p. The same kind of bound is worked through in [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §4]].

Every element is traceable: the concern is restated, the evidence is located, the
comparison protocol is specified, and the claim is renegotiated to match the data.

### 9. Artifact alignment

Paper, appendix, code, data, model, configuration, logs, and video should refer to compatible versions and identifiers. Videos illustrate behavior but do not replace trial distributions and failure counts. Keeping the paper itself in the repository, beside the scripts and data that make its figures, is [[02-foundations/tools/latex-figures-references|12.6 §10]].

Alignment matters because individually valid artifacts can describe different experiments. A table may use a checkpoint selected before a controller change, while the released configuration and demonstration video use the later controller. The reader can run the code successfully and still fail to reproduce the reported result.

For example, give each grasping run an identifier that links its configuration, checkpoint, calibration, raw log, and analysis output. Connect every table entry to the included run identifiers and document exclusions. Preserve failed runs too. If a video illustrates a different configuration, label that difference instead of presenting it as the source of the table.

**The reading this gives you.** Trace a result backward from figure to analysis to raw attempt. Ask whether the path ends at the same software and hardware settings that the method describes. Reproducible artifacts are an inspectable chain of evidence, not simply a repository containing files with plausible names.

### After reading

- Write a scoped claim–method–evidence sentence.
- Explain each paper section's distinct job.
- Organize related work as a useful taxonomy.
- Separate measured results from mechanistic interpretation.
- Write limitations as validity boundaries.
- Classify and answer reviewer comments with traceable revisions.
- Build RS1's results table with Wilson, Welch and Fisher entries, and pair each number with the sentence it licenses and the neighbour it does not.
- Design a results figure that shows every trial and the interval the claim is about.

### Self-check

1. What is missing from “our method is robust in the real world”?
2. Why should results and discussion be separated?
3. What makes a response letter easy to verify?
4. Why is a polished demonstration video insufficient evidence?
5. Table 1 prints B's success as 0.90 [0.60, 0.98]. A co-author wants "0.90 ± 0.19" instead. What is wrong with it?
6. Why does RS1's Results paragraph say "the pilot cannot distinguish these rates" rather than "the rates did not differ"?

> [!tip]- Answers
> 1. Method, comparator, operational definition of robustness/real world, conditions, trials, metrics, uncertainty, and failures. 2. It distinguishes observations from causal or generalizing interpretation. 3. Quote/decompose the concern, answer directly, describe evidence/revision, and give exact locations. 4. Selection bias, omitted failures/resets, unknown exposure, and missing matched baselines. 5. "± 0.19" is the Wald half-width, $1.96\sqrt{0.9 \times 0.1/10} = 0.186$. It makes the interval symmetric, $[0.71,\ 1.09]$, which reaches past 1, and it moves the lower end up from the Wilson interval's 0.60, telling the reader B's rate is at least 0.71 when 9 of 10 is compatible with 0.60. Near 0 or 1 an honest interval is lopsided, and a symmetric "±" cannot say so. 6. Because $p = 0.30$ is not evidence of equal rates ([[02-foundations/probability|3. Probability §6]], misreading 3). The difference's 95% interval, $-0.08$ to $+0.60$, contains zero and also a 60-point advantage, and a ten-trial design detects a true 0.6-against-0.9 difference only about 15% of the time. "Did not differ" asserts equality, which fails condition (4) of the licensed-sentence definition; "cannot distinguish" states what the test showed.

### Problem set · 과제

Tier B. Hand derivation on RS1, using only this page, its prerequisites and the pilot frozen in the running object. A different table from the worked case: the same twenty trials under a 12 N success line, and a different review.

1. **Draw.** The picture at the top of the page, with the success line moved to 12 N: mark the dots that change side. Then add the figure's second panel: the two success rates as points with Wilson 95% intervals on a 0–1 axis, for the 10 N and the 12 N definitions (four intervals), each labelled with its $k/n$. Mark where each pair of intervals overlaps.
2. **Derive.** Build the success rows of Table 1 under the 12 N definition. (a) The Wilson 95% interval for B's 10/10 and for A's 7/10, by hand. (b) The Newcombe 95% interval for B − A, and Fisher's exact $p$ for 7/10 against 10/10, listing the possible tables. (c) The sentence each number licenses, one unlicensed neighbour, and what else the table must now print because the definition changed.
3. **Interpret.** A second reviewer writes: "The success rates do not differ significantly (p = 0.30), so the paper shows that impedance control has no effect on contact safety. Reject." (a) Decompose the comment with §7's categories. (b) Write a compliant response of at most five sentences. (c) Which parts of the manuscript change, and which must not?

> [!note]- How to draw it · 그리는 법
> - Draw it by hand before writing any plotting code: one horizontal axis of peak contact force from 5 to 15 N, the success line as a dashed vertical line, and the success side shaded.
> - Label the line with where its value came from. The 10 N line was fixed before the pilot; a line moved after the data were seen must say so, or the reader cannot tell a prespecified threshold from a chosen one.
> - Every trial as a dot, A's ten on one row and B's ten on the row below: dots, not bars, so a reader can count the dots on each side of the line (at 10 N, the four A peaks just under it and B's single peak above it). Offset near-ties vertically so that no dot hides another.
> - Under each row, the mean with its 95% t-interval, and beside the strip the difference of means with its Welch interval, because the claim is about the difference and neither row's own interval answers it. Moving the success line moves none of these.
> - The second panel on a 0–1 axis: each success rate as a point with its Wilson 95% interval and its $k/n$, one pair per success definition, with the stretch where each pair overlaps marked.
> - Check each Wilson interval by its shape: its centre is pulled toward one half, so none of these four is symmetric about its point, and none passes 0 or 1. A symmetric interval, one that pokes past 1, or one that shrinks to a single point at $k = n$ is the Wald interval of the definition's non-example.
> - The caption: units, $n$ per arm, that the trials are unpaired, what the dots, diamonds, bars and intervals are, where each threshold came from, and that no trial was excluded. A figure that needs the body text before it can be read has failed.

> [!tip]- Solutions
> 1. The strip is unchanged except for the line: A's 11.3 N and B's 10.6 N cross to the success side, so the counts become 7/10 and 10/10. Second panel: at 10 N, A is $0.60\ [0.31,\ 0.83]$ and B $0.90\ [0.60,\ 0.98]$, overlapping on $[0.60,\ 0.83]$; at 12 N, A is $0.70\ [0.40,\ 0.89]$ and B $1.00\ [0.72,\ 1.00]$, overlapping on $[0.72,\ 0.89]$. B's 12 N interval has its upper end pinned at 1 and still reaches down to 0.72, which is the picture of "ten out of ten is not certainty".
> 2. (a) With $z^2/n = 0.384$: for 10/10 the centre is $(1 + 0.192)/1.384 = 0.861$ and the half-width $1.96\sqrt{0 + 0.0096}/1.384 = 0.139$, so $[0.722,\ 1.000]$; for 7/10 the centre is $(0.7 + 0.192)/1.384 = 0.645$ and the half-width $1.96\sqrt{0.021 + 0.0096}/1.384 = 0.248$, so $[0.397,\ 0.892]$. (b) Newcombe, with $\hat d = 1.0 - 0.7 = 0.30$: lower end $0.30 - \sqrt{(1.0 - 0.722)^2 + (0.892 - 0.7)^2} = 0.30 - \sqrt{0.0773 + 0.0369} = 0.30 - 0.338 = -0.04$; upper end $0.30 + \sqrt{(1.0 - 1.0)^2 + (0.7 - 0.397)^2} = 0.30 + 0.303 = 0.60$. Fisher: the margins are $n_A = n_B = 10$ and $m = 17$ successes, so $x$, A's successes, runs from 7 to 10. The numerators are $\binom{10}{7}\binom{10}{10} = 120$, $\binom{10}{8}\binom{10}{9} = 450$, $\binom{10}{9}\binom{10}{8} = 450$ and $\binom{10}{10}\binom{10}{7} = 120$, over $\binom{20}{17} = 1140$. The observed $x = 7$ has probability $120/1140 = 0.105$; the tables at most that probable are $x = 7$ and $x = 10$, so $p = 240/1140 = 0.211$. (c) "Under a 12 N criterion, B stayed below the line in all 10 trials (Wilson 95% CI 0.72 to 1.00) and A in 7 of 10 (0.40 to 0.89); the pilot cannot distinguish these rates either (difference $+0.30$, 95% CI $-0.04$ to $+0.60$; Fisher exact $p = 0.21$)." An unlicensed neighbour: "B never exceeds 12 N", which fails condition (3), since ten trials bound nothing about the eleventh, and condition (4), since the interval reaches down to 0.72. Because the line moved after the data were seen, the table must keep the prespecified 10 N rows and label the 12 N rows as a post hoc sensitivity analysis; printed alone, they would be the forking path of page 1's Step 2.
> 3. (a) A factual misreading — "not significant" read as "no effect", misreading 3 of [[02-foundations/probability|3. Probability §6]] — and a scope dispute, since after the first review the paper claims nothing about "contact safety" in general. "Reject" is a recommendation to the editor, not a point to answer. (b) "We agree that the pilot does not distinguish the two success rates, and the revised Results state exactly that (Fisher exact p = 0.30). We respectfully disagree that this shows no effect: a p-value above 0.05 is not evidence of equal rates, and the 95% interval for the difference, −0.08 to +0.60, includes a large benefit as well as none; the Limitations also state that a ten-trial design detects a true 0.6-versus-0.9 difference only about 15% of the time. The paper's prespecified primary outcome is peak contact force, whose difference is 3.16 N (Welch 95% CI 1.28 to 5.04 N, p = 0.003). The paper makes no claim about contact safety in general; the abstract claims only the lower mean peak force in this pilot." That is Clarify plus Rebut, and each sentence points at evidence or a location. (c) Changes: the power sentence in Limitations, if the first revision had not already added it. Must not change: the peak-force result and the scoped claim. A rebuttal that retreats to "no effect" deletes a licensed finding, and one that inflates the success comparison to win the argument commits the error the first review caught.

### Sources

- [Simon Peyton Jones — *How to Write a Great Research Paper* (Microsoft Research)](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/) — the classic talk on claim-first writing
- [IEEE T-RO — Information for Reviewers](https://www.ieee-ras.org/publications/t-ro/t-ro-information-for-reviewers/) — what reviewers at a flagship robotics journal are asked to check
- Edwin B. Wilson, "Probable inference, the law of succession, and statistical inference", *Journal of the American Statistical Association* 22(158):209–212 (1927) — the score interval of Table 1's success rows
- Lawrence D. Brown, T. Tony Cai & Anirban DasGupta, "Interval estimation for a binomial proportion", *Statistical Science* 16(2):101–133 (2001) — why the Wald interval fails at small $n$ and the Wilson interval is recommended
- Robert G. Newcombe, "Interval estimation for the difference between independent proportions: comparison of eleven methods", *Statistics in Medicine* 17(8):873–890 (1998) — the hybrid score interval of Table 1's success comparison
- B. L. Welch, "The generalization of 'Student's' problem when several different population variances are involved", *Biometrika* 34(1–2):28–35 (1947), and F. E. Satterthwaite, "An approximate distribution of estimates of variance components", *Biometrics Bulletin* 2(6):110–114 (1946) — the unequal-variance interval and its degrees of freedom
- R. A. Fisher, *The Design of Experiments* (Oliver & Boyd, 1935) — the exact test on a table with fixed margins
- Geoff Cumming & Sue Finch, "Inference by eye: confidence intervals and how to read pictures of data", *American Psychologist* 60(2):170–180 (2005) — what overlapping bars do and do not show
- Tracey L. Weissgerber, Natasa M. Milic, Stacey J. Winham & Vesna D. Garovic, "Beyond bar and line graphs: time for a new data presentation paradigm", *PLOS Biology* 13(4):e1002128 (2015) — why small-sample results should be shown as individual points

## 한국어

*RS1을 주장으로 바꾼 [[06-research-practice/research-questions-claims|1. 연구 질문과 주장]]과 [[02-foundations/probability|3. 확률 §6]] 위에 선다. 여기서 RS1의 주장은 논문이 된다. 논증 하나, 결과 표 하나, 그림 하나, 한계 문단 하나, 심사 문답 하나가 모두 파일럿의 숫자 스무 개 위에 선다.*

과학적 글쓰기는 주장을 증거와 정렬하고 그 경계를 검사 가능하게 만든다. 명료함은 장식이
아니다: 모호한 범위, 숨은 가정, 빠진 프로토콜은 독자의 평가 자체를 막는다.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고, 이어서 계산 예제를 읽는다. RS1의 결과 표에서 숫자 하나하나를 그것이 허락하는 문장 하나, 그리고 허락하지 않는 이웃 문장과 짝지어 둔 곳이다. 그다음 §4(그림), §6(한계 문단), §7(심사)를 읽는다. 세 절 모두 이제 RS1의 사례를 담고 있다. 1–3절, 5절, 8–9절은 일반적인 기술이다. 첫 반박문을 쓰기 전에는 §8을 읽는다.

### 이 페이지의 대상 · Running object

Research Practice의 관통 연구 RS1을 [[06-research-practice/research-questions-claims|1. 연구 질문과 주장]]에서 그대로 다시 적는다. *질문:* 임피던스 제어(B)는 평면 팔이 패널에 닿는 접촉을, 힘 문턱에서 멈추는 위치 제어(A)보다 더 안전하게 만드는가? *장치:* [[02-foundations/lab-plants|0.6 Lab Plants]]의 P2(평면 2R, 링크 길이 1 m, 각 링크 끝에 1 kg 점질량)가 P3 벽의 강성 $k_w = 400$ N/m를 가진 패널을 만난다. *시행:* 팔이 패널에 다가가 접촉한다. 결과는 뉴턴 단위의 최대 접촉력이고, 그 최댓값이 10 N 이하이면 성공이다. *파일럿:* 제어기마다 대응 없는 시행 10회. **이 데이터는 교육용으로 지어낸 예시이며 고정되어 있다. 실제 제어기를 측정한 값이 아니다.**

| 시행 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A — 위치 제어 + 힘 문턱 정지 (N) | 8.1 | 9.4 | 12.6 | 9.8 | 13.9 | 7.7 | 9.9 | 9.1 | 14.8 | 11.3 |
| B — 임피던스 제어 (N) | 6.2 | 7.9 | 8.4 | 5.9 | 7.1 | 10.6 | 6.8 | 7.5 | 8.0 | 6.6 |

| 제어기 | 성공(최대 ≤ 10 N) | 평균 (N) | 표본 표준편차 (N) | 중앙값 (N) |
|---|---:|---:|---:|---:|
| A | 6/10 | 10.66 | 2.414 | 9.85 |
| B | 9/10 | 7.50 | 1.356 | 7.30 |

**논문으로 쓸 주장.** 1쪽이 끝에 도달한 바로 그 주장이고, 결과의 순위는 파일럿 전에 정해 두었다. 주 결과는 평균 최대 접촉력(B가 A보다 낮음), 부차 결과는 10 N 이하에 머문 접촉의 비율이다. 파일럿은 앞의 것을 경계 안에서 허락하고 뒤의 것은 허락하지 않는다. 이 페이지가 할 일은 정확히 그만큼을 쓰는 것이다.

*범위: 이 페이지는 RS1의 주장을 논문으로 쓰는 법을 가르친다. 논문 수준의 논증, 파일럿을 위한 결과 표 하나와 그림 하나, 숫자마다 허락되는 문장, 한계 문단, 심사 문답 하나다. 주장을 어떻게 세웠는지([[06-research-practice/research-questions-claims|1. 연구 질문과 주장]]), 실험을 어떻게 설계하고 크기를 정하는지([[06-research-practice/experimental-design-reproducibility|2. 실험 설계]]), 여기서 쓰는 세 가지 밖의 검정([[02-foundations/probability|3. 확률 §6]]), 어디에 투고할지([[06-research-practice/venue-strategy|5. Venue 전략]])는 가르치지 않는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 290" style="max-width:100%;height:auto" role="img" aria-label="논문의 그림으로 그린 RS1 파일럿: 5–15 N 축 위에 모든 시행의 최대 접촉력을 점으로, 파일럿 전에 고정한 10 N 선과 칠한 성공 쪽, 제어기마다 평균과 95% 구간, 그리고 옆에 평균의 차 3.16 N과 Welch 95% 구간 1.28–5.04">
  <rect x="72" y="30" width="150" height="128" fill="currentColor" fill-opacity="0.08"/>
  <line x1="72" y1="158" x2="372" y2="158" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M72 158V163 M102 158V163 M132 158V163 M162 158V163 M192 158V163 M222 158V163 M252 158V163 M282 158V163 M312 158V163 M342 158V163 M372 158V163" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="72" y="176" font-size="11" text-anchor="middle" fill="currentColor">5</text>
  <text x="102" y="176" font-size="11" text-anchor="middle" fill="currentColor">6</text>
  <text x="132" y="176" font-size="11" text-anchor="middle" fill="currentColor">7</text>
  <text x="162" y="176" font-size="11" text-anchor="middle" fill="currentColor">8</text>
  <text x="192" y="176" font-size="11" text-anchor="middle" fill="currentColor">9</text>
  <text x="222" y="176" font-size="11" text-anchor="middle" fill="currentColor">10</text>
  <text x="252" y="176" font-size="11" text-anchor="middle" fill="currentColor">11</text>
  <text x="282" y="176" font-size="11" text-anchor="middle" fill="currentColor">12</text>
  <text x="312" y="176" font-size="11" text-anchor="middle" fill="currentColor">13</text>
  <text x="342" y="176" font-size="11" text-anchor="middle" fill="currentColor">14</text>
  <text x="372" y="176" font-size="11" text-anchor="middle" fill="currentColor">15</text>
  <text x="222" y="193" font-size="11" text-anchor="middle" fill="currentColor">시행별 최대 접촉력 (N)</text>
  <line x1="222" y1="22" x2="222" y2="158" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="228" y="28" font-size="11" fill="currentColor">10 N, 파일럿 전에 고정</text>
  <text x="77" y="43" font-size="11" opacity="0.8" fill="currentColor">성공: 최댓값 ≤ 10 N</text>
  <circle cx="352.6" cy="24" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="352.6" y="28" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">1</text>
  <circle cx="153" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="165" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="195" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="204" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="216" cy="61.5" r="3.6" fill="currentColor"/>
  <circle cx="219" cy="70.5" r="3.6" fill="currentColor"/>
  <circle cx="261" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="300" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="339" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="366" cy="66" r="3.6" fill="currentColor"/>
  <circle cx="99" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="108" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="120" cy="113.5" r="3.6" fill="currentColor"/>
  <circle cx="126" cy="122.5" r="3.6" fill="currentColor"/>
  <circle cx="135" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="147" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="159" cy="113.5" r="3.6" fill="currentColor"/>
  <circle cx="162" cy="122.5" r="3.6" fill="currentColor"/>
  <circle cx="174" cy="118" r="3.6" fill="currentColor"/>
  <circle cx="240" cy="118" r="3.6" fill="currentColor"/>
  <text x="16" y="70" font-size="12.5" font-weight="bold" fill="currentColor">A</text>
  <text x="16" y="122" font-size="12.5" font-weight="bold" fill="currentColor">B</text>
  <circle cx="38" cy="66" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="38" y="70" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">2</text>
  <path d="M190 86 H293.6 M190 82 V90 M293.6 82 V90" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M241.8 81 L246.8 86 L241.8 91 L236.8 86 Z" fill="currentColor"/>
  <path d="M117.9 138 H176.1 M117.9 134 V142 M176.1 134 V142" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M147 133 L152 138 L147 143 L142 138 Z" fill="currentColor"/>
  <text x="301.6" y="90" font-size="11" opacity="0.85" fill="currentColor">평균, 95% 신뢰구간</text>
  <circle cx="411" cy="86" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="411" y="90" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">3</text>
  <line x1="446" y1="36" x2="446" y2="158" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.6"/>
  <line x1="430" y1="158" x2="542" y2="158" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <path d="M430 158V163 M446 158V163 M462 158V163 M478 158V163 M494 158V163 M510 158V163 M526 158V163 M542 158V163" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="446" y="176" font-size="11" text-anchor="middle" fill="currentColor">0</text>
  <text x="478" y="176" font-size="11" text-anchor="middle" fill="currentColor">2</text>
  <text x="510" y="176" font-size="11" text-anchor="middle" fill="currentColor">4</text>
  <text x="542" y="176" font-size="11" text-anchor="middle" fill="currentColor">6</text>
  <text x="486" y="193" font-size="11" text-anchor="middle" fill="currentColor">A − B (N)</text>
  <text x="495" y="28" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">평균의 차</text>
  <circle cx="458.1" cy="24" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="458.1" y="28" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">3</text>
  <path d="M466.5 96 H526.6 M466.5 92 V100 M526.6 92 V100" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M496.6 91 L501.6 96 L496.6 101 L491.6 96 Z" fill="currentColor"/>
  <text x="496.6" y="84" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">3.16 N</text>
  <text x="496.6" y="116" font-size="11" text-anchor="middle" fill="currentColor">[1.28, 5.04]</text>
  <text x="496.6" y="130" font-size="11" text-anchor="middle" opacity="0.8" fill="currentColor">Welch 95% 구간</text>
  <circle cx="23" cy="214" r="7.5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="23" y="218" font-size="11" text-anchor="middle" font-weight="bold" fill="currentColor">4</text>
  <text x="38" y="218" font-size="11" opacity="0.9" fill="currentColor">그림 1. RS1 파일럿(예시 데이터): 모든 시행의 최대 접촉력(N). 400 N/m 패널에 대한 팔 P2, 제어기당</text>
  <text x="38" y="233" font-size="11" opacity="0.9" fill="currentColor">대응 없는 시행 10회, 제외한 시행 없음. 점은 시행 하나이고, 각 줄 아래의 다이아몬드와 막대는 평균과</text>
  <text x="38" y="248" font-size="11" opacity="0.9" fill="currentColor">그 95% t-구간이다(A 10.66 N [8.93, 12.39], B 7.50 N [6.53, 8.47]). 점선은 파일럿 전에 고정한 10 N</text>
  <text x="38" y="263" font-size="11" opacity="0.9" fill="currentColor">성공 문턱이고, 칠한 쪽이 성공이다. 오른쪽은 평균의 차 A − B = 3.16 N과 그 Welch 95% 구간</text>
  <text x="38" y="278" font-size="11" opacity="0.9" fill="currentColor">[1.28, 5.04]다.</text>
</svg>

RS1 파일럿을 논문의 그림 하나로 그린 것으로, 시행마다 최대 접촉력을 점 하나로 찍었고(위 줄에 A의 열 개, 아래 줄에 B의 열 개), 파일럿 전에 고정한 10 N 성공선의 칠한 성공 쪽에 A의 점 여섯 개와 B의 점 아홉 개가 떨어진다. 각 줄 아래에는 평균과 그 95% t-구간(A 10.66 N [8.93, 12.39], B 7.50 N [6.53, 8.47])이, 오른쪽에는 주장이 겨냥하는 숫자인 평균의 차 3.16 N과 그 Welch 95% 구간 [1.28, 5.04]가 있다. 동그라미 친 번호는 결과 그림이 독자에게 갖춰 주어야 할 네 부분, 곧 미리 고정한 선, 모든 시행, 주장에 답하는 구간, 본문 없이 읽히는 캡션을 가리킨다.

### 대상으로 한 번 끝까지 · Worked case

RS1 파일럿의 결과 표를 정확한 숫자로 만들고, 숫자마다 출처를 밝힌 다음, 숫자마다 허락되는 문장을 적는다.

**1단계 — 표.**

| 양 | A | B | 비교 |
|---|---:|---:|---|
| 시행 수(대응 없음) | 10 | 10 | — |
| 최대 접촉력 ↓, 평균 ± 표준편차 (N) | 10.66 ± 2.41 | 7.50 ± 1.36 | A − B $= 3.16$ N, Welch 95% 신뢰구간 $[1.28,\ 5.04]$; $t = 3.61$, 자유도 14.2, $p = 0.003$ |
| 최대 접촉력 ↓, 중앙값 [최소, 최대] (N) | 9.85 [7.7, 14.8] | 7.30 [5.9, 10.6] | — |
| 성공, 최대 ≤ 10 N ↑ | 6/10 | 9/10 | B − A $= +0.30$, Newcombe 95% 신뢰구간 $[-0.08,\ 0.60]$; Fisher 정확 검정 $p = 0.30$ |
| 성공률 ↑, Wilson 95% 신뢰구간 | 0.60 [0.31, 0.83] | 0.90 [0.60, 0.98] | 두 구간은 $[0.60,\ 0.83]$에서 겹친다 |

*표 1. 400 N/m 패널에 대한 팔 P2의 RS1 파일럿, 제어기당 대응 없는 시행 10회(예시 데이터). 화살표는 개선 방향이다. 최대 접촉력: 표본 평균 ± 표본 표준편차, 그리고 중앙값과 범위. 비교는 평균의 차와 Welch 95% 신뢰구간, 양측 p다. 성공: 최댓값 10 N 이하이며 문턱은 파일럿 전에 고정했다. 성공률에는 Wilson 95% 점수 구간을 붙였고, 비교는 비율의 차와 그 Newcombe 95% 구간, 그리고 양측 Fisher 정확 검정이다. 스무 시행을 모두 보고했고 제외한 시행은 없다.*

**2단계 — 숫자마다 어디서 왔는가.** 표 1이 결과를 인쇄하는 절차 넷을 여기서 한 번씩 정의한다.

> [!info] 정의 — Wilson 점수 구간
> **무엇인가:** $n$번 시행 중 $k$번 성공에서 성공 확률 $p$에 대한 신뢰구간 절차다([[02-foundations/probability|3. 확률 §6]]의 뜻에서). **정의 조건:** (1) $n$번의 시행이 독립이고, (2) 모두 같은 성공 확률 $p$를 가지며, (3) 구간은 수준 $\alpha$의 양측 점수 검정이 기각하지 않는 모든 $p$의 집합이다. 여기서 점수 통계량 $(\hat p - p)/\sqrt{p(1-p)/n}$은 $\hat p$가 아니라 후보 $p$에서의 표준오차를 쓴다. 그 $p$에 대한 이차식을 풀면
> $$\frac{\hat p + \dfrac{z^2}{2n} \pm z\sqrt{\dfrac{\hat p(1-\hat p)}{n} + \dfrac{z^2}{4n^2}}}{1 + \dfrac{z^2}{n}}$$
> 이고, $\hat p = k/n$, 95%라면 $z = 1.96$이다(Wilson 1927). 중심은 $\hat p$와 $\tfrac12$의 가중 평균이어서 가운데 쪽으로 끌려오고, 구간은 $[0, 1]$을 벗어나지 않는다.
> **예.** B의 9/10: $z^2/n = 0.384$이므로 중심은 $(0.9 + 0.192)/1.384 = 0.789$, 반폭은 $1.96\sqrt{0.009 + 0.0096}/1.384 = 0.193$이고 구간은 $[0.596,\ 0.982]$다. A의 6/10: 중심 $0.572$, 반폭 $0.260$, 구간 $[0.313,\ 0.832]$.
> **반례.** Wald 구간 $\hat p \pm z\sqrt{\hat p(1-\hat p)/n}$은 $\hat p$에서의 표준오차를 쓴다. 9/10이면 $0.9 \pm 0.186 = [0.714,\ 1.086]$으로 1을 넘는 성공 확률을 허용하고, 10/10에서는 점 1 하나로 쪼그라든다.
> **왜 중요한가.** 시행이 열 번이면 두 절차는 양 끝에서 0.1 넘게 어긋난다(아래 끝 $0.714$ 대 $0.596$, 위 끝 $1.086$ 대 $0.982$). Wald 구간을 인쇄한 표는 B의 성공률이 적어도 0.71이라고 말하지만, 10번 중 9번은 0.60과도 양립한다(Brown, Cai & DasGupta 2001).

> [!info] 정의 — 두 비율의 차에 대한 Newcombe 구간
> **무엇인가:** 두 성공 확률의 차 $p_B - p_A$에 대한 신뢰구간 절차로, 두 Wilson 구간으로 만든다. **정의 조건:** (1) 각각 Wilson 조건을 만족하는 독립인 두 시행 집단, (2) 각 집단의 Wilson 한계 $[l, u]$를 먼저 계산하고, (3) 차이 구간의 각 끝은 차이를 그 방향으로 끄는 두 거리를 합친다. 아래 끝이라면 B의 비율이 내려갈 수 있는 거리($\hat p_B - l_B$)와 A의 비율이 올라갈 수 있는 거리($u_A - \hat p_A$)다.
> $$\Big[\ \hat d - \sqrt{(\hat p_B - l_B)^2 + (u_A - \hat p_A)^2}\ ,\ \ \hat d + \sqrt{(u_B - \hat p_B)^2 + (\hat p_A - l_A)^2}\ \Big], \qquad \hat d = \hat p_B - \hat p_A$$
> 이것이 Newcombe의 혼합 점수(hybrid score) 방법이다(Newcombe 1998). 두 집단이 독립이므로 불확실성이 분산처럼 더해지고, 그래서 두 거리를 제곱해 더한 뒤 제곱근을 취한다.
> **예.** RS1: $\hat d = 0.30$. 아래 끝 $0.30 - \sqrt{(0.9 - 0.596)^2 + (0.832 - 0.6)^2} = 0.30 - \sqrt{0.0924 + 0.0538} = 0.30 - 0.382 = -0.08$, 위 끝 $0.30 + \sqrt{(0.982 - 0.9)^2 + (0.6 - 0.313)^2} = 0.30 + \sqrt{0.0067 + 0.0824} = 0.30 + 0.298 = 0.60$.
> **반례.** 두 Wilson 구간이 겹치는 구간 $[0.60,\ 0.83]$을 답으로 읽는 것. 두 구간의 겹침은 차이의 구간이 아니다. 두 구간이 겹쳐도 차이의 구간은 0을 배제할 수 있다.
> **왜 중요한가.** 파일럿이 무엇과 양립하는지 말해 준다. B가 A보다 조금 덜 성공하는 경우부터 60%p 더 성공하는 경우까지다. p-값만이 아니라 이 범위가, "효과 없음"이 "B가 더 자주 성공한다"만큼이나 허락되지 않는 이유다.

> [!info] 정의 — 평균의 차에 대한 Welch 구간
> **무엇인가:** 독립인 두 표본에서 두 모평균의 차 $\mu_A - \mu_B$에 대한 신뢰구간 절차다. **정의 조건:** (1) 두 표본이 서로 독립(대응 없음)이고, (2) 각 표본 평균이 대략 정규여서 이 $n$에서 데이터가 심하게 치우치거나 이상치에 좌우되지 않으며, (3) 두 분산이 같다고 가정하지 **않는다**. 각 표본은 자기 $s^2$를 쓴다. 그러면
> $$\bar y_A - \bar y_B \pm t_{0.975,\,\nu}\,\mathrm{SE}, \qquad \mathrm{SE} = \sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}, \qquad \nu = \frac{\mathrm{SE}^4}{\dfrac{(s_A^2/n_A)^2}{n_A - 1} + \dfrac{(s_B^2/n_B)^2}{n_B - 1}}$$
> 이다. $\bar y$, $s$, $n$은 각 표본의 평균, 표준편차, 크기이고, $\nu$는 Welch–Satterthwaite 자유도, $t_{0.975,\nu}$는 Student-$t$ 분위수다(Welch 1947; Satterthwaite 1946). 표본이 독립이므로 SE는 두 분산을 더하고, 한쪽 분산이 지배하면 $\nu$는 잡음이 큰 표본의 $n - 1$ 쪽으로 내려간다. 그래서 분산이 다른 쌍은 더 넓은 $t$로 판정된다.
> **예.** RS1: $s_A^2/n_A = 2.414^2/10 = 0.583$, $s_B^2/n_B = 1.356^2/10 = 0.184$이므로 $\mathrm{SE} = \sqrt{0.767} = 0.876$ N, $\nu = 0.767^2/(0.583^2/9 + 0.184^2/9) = 14.2$다. $t_{0.975,\,14.2} = 2.142$로 구간은 $3.16 \pm 1.88 = [1.28,\ 5.04]$ N이고, $t = 3.16/0.876 = 3.61$은 양측 $p = 0.003$을 준다.
> **반례.** 서로 겹치는 ±1 표준편차 막대 두 개. A의 $10.66 \pm 2.41$은 $[8.25,\ 13.07]$, B의 $7.50 \pm 1.36$은 $[6.14,\ 8.86]$에 걸쳐 $[8.25,\ 8.86]$에서 겹치지만, 차이의 구간은 0에서 1 N 넘게 떨어져 있다. 표준편차는 시행 하나하나의 흩어짐을 말하지 평균의 불확실성을 말하지 않는다([[02-foundations/ml-practice|9. ML 실무 §4]]).
> **왜 중요한가.** 주장은 차이에 관한 것이므로 표에는 차이의 구간이 있어야 한다. 어느 쪽의 구간이나 막대도 그 질문에 답하지 않는다.

> [!info] 정의 — Fisher 정확 검정
> **무엇인가:** $2 \times 2$ 개수 표에서 두 성공 확률이 다른지 보는 가설 검정, 곧 [[02-foundations/probability|3. 확률 §6]]의 뜻에서의 p-값 절차다. **정의 조건:** (1) 독립인 시행 집단 둘, (2) 시행마다 이진 결과, (3) 두 집단의 성공 확률이 같다는 귀무가설, (4) 표의 주변합 — 집단 크기 $n_A$, $n_B$와 전체 성공 수 $m$ — 에 조건을 건다. 그러면 귀무가설 아래 집단 A의 성공 수 $X$는 초기하 분포를 따르고
> $$P(X = x) = \frac{\binom{n_A}{x}\binom{n_B}{m - x}}{\binom{n_A + n_B}{m}}$$
> 양측 $p$는 관측한 표보다 확률이 크지 않은 모든 표의 확률의 합이다(Fisher 1935).
> **예.** RS1: $n_A = n_B = 10$, $m = 15$, 관측 $x = 6$. 가능한 $x$는 5부터 10까지이고 분자는 $252, 2100, 5400, 5400, 2100, 252$, 분모는 $\binom{20}{15} = 15504$다. 관측한 표의 확률은 $2100/15504 = 0.135$, 그보다 확률이 크지 않은 표는 $x = 5, 6, 9, 10$이므로 $p = (252 + 2100 + 2100 + 252)/15504 = 4704/15504 = 0.303$이다.
> **반례.** 같은 표에 대한 카이제곱 검정. 같은 귀무가설을 대표본 분포로 근사하는데, 흔한 경험칙은 모든 칸의 기대 개수가 5 이상이기를 요구한다. RS1의 실패 두 칸은 기대 개수가 각각 $10 \times 5/20 = 2.5$다. 제어기당 10회에서 근사는 맞지 않는 도구이고, 대응 없는 두 성공 횟수에 대해 [[02-foundations/probability|3. 확률 §6]]의 표가 지정하는 것이 정확 검정이다.
> **왜 중요한가.** 성공 행에 대한 정직한 p-값이고, $0.30$이라는 그 값이 "B가 더 자주 성공한다"를 초록에서 막는다.

**3단계 — 숫자마다 허락되는 문장.**

> [!info] 정의 — 허락된 문장
> **무엇인가:** 논문의 문장과 결과의 숫자 사이의 관계다. 문장이 숫자가 잰 것보다 더 말하지 않을 때 숫자가 그 문장을 *허락한다*. **정의 조건 — 넷 모두:** (1) *같은 양*: 문장은 숫자가 추정하는 양에 대해, 그 조작적 정의 아래에서 말한다. (2) *같은 비교*: 문장 속 비교는 같은 제어기와 절차로 그 숫자를 낳은 바로 그 비교다. (3) *표본 안의 범위*: 문장이 대변하는 모집단, 조건, 증거의 단이 시행이 덮은 범위 안에 있다. (4) *불확실성 안의 강도*: 문장이 풍기는 확실성이 숫자에 붙은 구간이나 검정이 허용하는 것보다 크지 않다.
> $$\text{licensed}(s, x) \iff \text{qty}(s) = \text{qty}(x) \ \wedge\ \text{cmp}(s) = \text{cmp}(x) \ \wedge\ \text{scope}(s) \subseteq \text{scope}(x) \ \wedge\ \text{strength}(s) \le \text{strength}(x)$$
> 여기서 $s$는 문장, $x$는 구간이나 검정을 함께 가진 숫자, qty는 양, cmp는 비교다. 그래서 조건 하나만 어겨도 문장은 허락을 잃는다.
> **예.** "B는 파일럿 10회 중 9회에서 10 N 이하에 머물렀다"는 B의 개수 9/10이 허락한다.
> **반례.** 같은 9/10에서 나온 "B가 더 안전하다". 안전은 센 양이 아니므로 조건 (1)을 어기고, 팔 하나, 패널 하나, 시행 열 번은 "더 안전하다"가 읽힐 자리를 덮지 못하므로 조건 (3)을 어긴다.
> **왜 중요한가.** §1의 그림, 곧 증거 상자 안의 주장 상자를 문장 하나씩 확인하는 것이다. "주장이 과하다"는 심사평은 모두 넷 중 하나를 어긴 문장을 가리킨다.

| 표 1의 숫자 | 그 숫자가 허락하는 문장 | 허락하지 않는 이웃 문장 | 이웃이 어긴 조건 |
|---|---|---|---|
| B: 9/10 | "B는 파일럿 10회 중 9회에서 10 N 이하에 머물렀다." | "B가 더 안전하다." | (1) 양, (3) 범위 |
| B: 0.90 [0.60, 0.98] | "이 절차에서 B의 성공 확률은 0.60에서 0.98 사이 어디든 그럴듯하다." | "B는 접촉의 90%에서 성공한다." | (4) 강도: 구간이 0.60까지 내려간다 |
| A: 6/10 | "A는 10회 중 6회 그랬다." | "A는 40%의 경우 실패한다." | (3)과 (4): 구간 [0.31, 0.83] 없이 시행 열 번으로 모집단 비율을 말한다 |
| 3.16 N [1.28, 5.04] | "B의 평균 최대 접촉력은 A보다 3.16 N 낮았다(95% 신뢰구간 1.28–5.04 N)." | "B는 접촉력을 30% 줄인다." | (1): 비 $3.16/10.66 = 0.30$은 다른 양이고, 그 구간은 보고되지 않았다 |
| $t = 3.61$, $p = 0.003$ | "두 평균 최대 접촉력이 같다면 이만큼 큰 차이는 나오기 어렵다(Welch $p = 0.003$)." | "B가 더 나을 확률이 99.7%다." | (1): $p$는 가설의 확률이 아니다([[02-foundations/probability\|3. 확률 §6]]) |
| $+0.30$ $[-0.08,\ 0.60]$, Fisher $p = 0.30$ | "파일럿은 두 성공률을 구별하지 못한다. B − A $= +0.30$, 95% 신뢰구간 $-0.08$–$+0.60$(Fisher 정확 검정 $p = 0.30$)." | "임피던스 제어는 성공률을 바꾸지 않는다." | (4): 구간이 $+0.60$까지 이어지므로 "변화 없음"은 데이터가 허용하는 여러 값 중 하나일 뿐이다 |
| B의 최댓값 10.6 N | "B의 파일럿 최댓값 10.6 N은 A의 14.8 N보다 낮았다." | "B는 접촉력을 11 N 아래로 유지한다." | (3): 열 번 중 최댓값은 열한 번째에 대한 한계가 아니다 |

**4단계 — 허락된 문장만으로 조립한 Results 문단.**

> 제어기당 대응 없는 시행 10회에서, B의 평균 최대 접촉력은 7.50 N(표준편차 1.36)으로 A의 10.66 N(표준편차 2.41)보다 3.16 N 낮았다(Welch 95% 신뢰구간 1.28–5.04 N; $t = 3.61$, 자유도 14.2, $p = 0.003$; 표 1, 그림 1). B는 미리 정한 10 N 한계 이하에 10회 중 9회(Wilson 95% 신뢰구간 0.60–0.98), A는 10회 중 6회(0.31–0.83) 머물렀다. 파일럿은 이 두 비율을 구별하지 못한다(차이 $+0.30$, 95% 신뢰구간 $-0.08$–$+0.60$; Fisher 정확 검정 $p = 0.30$). B의 최댓값은 10.6 N, A의 최댓값은 14.8 N이었다.

문단의 모든 숫자는 표 1의 칸이고, 모든 동사는 표가 허락하는 것이다. 문단이 말하지 않는 것 — 더 안전하다, 30% 낮다, 11 N을 넘지 않는다 — 은 정확히 3단계 표의 오른쪽 열이다.

### 1. 논문 수준의 논증

| 섹션 | 주된 역할 |
|---|---|
| Abstract | 문제, 방법, 범위가 한정된 가장 강한 증거, 함의 |
| Introduction | 중요성, 정확한 gap, 접근, 기여 |
| Related work | 분류 체계와 차이 — 인용 목록이 아니라 |
| Method | 변수, 가정, 알고리즘/시스템, 재현 가능한 세부 |
| Experiments | 질문, 프로토콜, 베이스라인, 지표, 결과 |
| Discussion | 해석, 기전, 일반화, 트레이드오프 |
| Limitations | 유효성의 경계와 미해결 위험 |

Introduction이 일반적 능력을 약속하고 실험은 좁은 조건 하나만 시험하게 두지 말라.

<svg viewBox="0 0 560 226" style="max-width:100%;height:auto" role="img" aria-label="증거 상자 안에 들어 있는 주장 상자와, 주장이 증거 밖으로 삐져나온 같은 두 상자">
  <g font-size="11" fill="currentColor">
    <text x="40" y="16">방어 가능한 경우</text><text x="310" y="16">흔한 실패</text>
  </g>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.7">
    <rect x="40" y="30" width="210" height="104" rx="4"/>
    <rect x="310" y="46" width="150" height="72" rx="4"/>
  </g>
  <g fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.4">
    <rect x="70" y="52" width="150" height="60" rx="3"/>
    <rect x="340" y="30" width="200" height="104" rx="3" fill-opacity="0.16"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="145" y="46">증거가 덮는 범위</text>
    <text x="145" y="86">논문이 하는 주장</text>
    <text x="400" y="86">증거가 덮는 범위</text>
    <text x="440" y="153">논문이 하는 주장</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" fill="none">
    <line x1="440" y1="142" x2="440" y2="136"/>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.85">
    <text x="310" y="170">이 삐져나온 폭이 정확히 공격받는 지점이다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="24" y="188">심사자가 재는 것은 결과가 얼마나 큰가가 아니다. 두 상자 중 하나가 다른 하나 안에 들어가는가다.</text>
    <text x="24" y="204">&#8220;주장이 과하다&#8221;는 모든 심사평은 저 음영 띠에 대한 보고이고, 가장 싼 교정은 새 실험이</text>
    <text x="24" y="220">거의 아니다 &#8212; 문장이 맞을 때까지 좁히는 것이다.</text>
  </g>
</svg>

논증은 의존 관계의 순서다. 뒤의 주장을 이해하려면 앞의 가정이 보여야 한다. 예를 들어 [[04-robotics/grasping|파지]]는 닫힘에서 파지 품질을 거쳐 학습으로 이동한다. 렌치를 버티는가, 불확실성에 대한 여유가 있는가, 관측에서 쓸 만한 파지를 예측하는가는 서로 다른 질문이다. 학습 점수가 역학 모델의 보장을 자동으로 물려받지는 않는다.

**여기서 얻는 독법.** 초안에서도 같은 사슬을 찾는다. 문제가 선택한 모델을 필요로 하는가, 실험은 모델이 약속한 이점을 시험하는가, 결론은 관찰 범위에 머무는가를 본다. 각 절이 명료해도 절 사이의 논증은 빠져 있을 수 있다.

**절별로 본 RS1의 논증.** 위의 섹션 표를 이 페이지의 대상인 파일럿으로 채운 것이다. RS1의 사슬이 끊어져서는 안 되는 고리는 동사다. 초록은 *낮았다*([[06-research-practice/research-questions-claims|1. 연구 질문과 주장]] 계산 예제의 주장–증거 표 2행)라고 말하지, 결코 *더 안전하다*(4행)라고 말하지 않는다.

| 섹션 | RS1의 형태 |
|---|---|
| Abstract | 1쪽 계산 예제를 끝맺는 허락된 문장, 그 이상은 없음 |
| Introduction | 팔이 패널을 만날 때 최대 접촉력이 왜 중요한가. gap은 비교로 적는다. 한 절차 아래에서, 컴플라이언트한 제어기가 힘 문턱에서 멈추는 제어기에 비해 부드러운 패널에 대한 최댓값을 낮추는가? |
| Method | P2와 그 고정된 숫자, $k_w = 400$ N/m, B의 목표 임피던스, A의 정지 문턱, 접근 속도와 방향, 시행, 파일럿 전에 고정한 10 N 선 |
| Experiments | 제어기당 대응 없는 시행 10회. 표 1(계산 예제)과 그림 1(§4) |
| Discussion | 후보 기전, 후보라고 밝혀서(§5) |
| Limitations | §6의 문단 |

### 2. 주장–방법–증거 문장

권장: "Held-out 자재 배치에서, 우리 정책은 짝지은 BC 대비 폐루프 성공률을 X에서 Y로
높였다 (조건당 Z회 시행)."

피하라: "우리의 지능적 프레임워크는 강건한 건설 자율성을 혁신한다." 두 번째 문장에는
조작적 주장, 비교 대상, 범위, 증거가 없다.

다음은 가상 문장 틀이다. 수치 결과는 실제 실험에서 얻은 것만 채운다.

**수정 전:** “다양한 물체를 강건하게 다룬다.” **문제:** 다양성과 강건성의 시험 경계가 없다. **수정 후:** “보지 못한 물체 집합에서 짝지은 베이스라인 대비 파지 성공을 보고하고, 재료별 시도와 실패를 구분한다.”

**수정 전:** “구조가 데이터 효율을 높인다.” **문제:** 한 학습 예산에서의 이점은 학습 곡선이 아니다. **수정 후:** “미리 정한 시연 예산별로 같은 평가 절차에서 비교하고 각 예산의 불확실성을 보고한다.”

**수정 전:** “로봇이 자율적으로 과제를 마친다.” **문제:** 완료 안에 보조가 숨을 수 있다. **수정 후:** “자율 완료와 운전자 정지·리셋 뒤 완료를 구분하고 시작한 모든 시도를 유지한다.”

**여기서 얻는 독법.** 좋은 문장은 분할, 비교 대상, 지표, 집계 규칙을 확인할 위치를 준다. 실제 기록이 있을 때만 보고 계획의 틀을 결과 문장으로 바꾼다.

### 3. Related work는 분류 체계다

문제 가정, 표현, 지도 방식, 계획/제어 인터페이스, 평가 체제로 논문들을 묶어라. 각 묶음의
끝에 당신의 연구가 시험하는 미해결 차이를 적어라. 연대순 나열은 역사 자체가 gap을
설명할 때만 유용하다.

**수정 전:** “논문 A는 시각을 썼다. B는 촉각을 추가했다. C는 새 계획기를 제안했다. 우리 시스템은 장점을 결합한다.” **문제:** 독자는 목록만 얻고 미해결 비교를 찾지 못한다. 부품 결합만으로 입증되지 않은 이점도 약속한다.

**수정 후:** “파지 방법을 접촉 정보를 얻는 시점으로 나눈다. 접촉 전 영상으로 결정을 끝내는 방법은 마찰과 형상 가정에 의존한다. 접촉 뒤 갱신하는 방법은 미끄러짐에 반응할 수 있지만, 실패 전에 센싱과 제어가 반응해야 유용하다. 본 비교는 계획기를 고정하고 이 시간 경계를 시험한다.”

가정과 인터페이스가 분류축이 됐다. 실제 논문과 인용은 해당 집단에 배치한다. **여기서 얻는 독법.** 각 집단이 설계할 실험을 바꾸는지 묻는다. 관련연구 문단을 지워도 주장한 gap이 그대로라면 아직 문장으로 쓴 참고문헌 목록일 수 있다.

### 4. 그림과 표

시스템 그림은 런타임 정보 흐름, 학습/동결 구성요소, 필요하면 프레임·주기, 학습/추론
차이를 보여야 한다. 결과 표에는 단위, 개선 방향, 불확실성, 시행 수, 명확한 최고값 표기가
필요하다. 캡션은 본문을 뒤지지 않고도 이해돼야 한다. 그런 그림과 표를 만드는 도구 — 단 폭으로 인쇄해도 버티는 파일, 인쇄 크기의 글자, 자기가 무엇인지 말하는 오차 막대, 데이터가 받쳐 주는 자릿수로 찍은 항목 — 는 [[02-foundations/tools/latex-figures-references|12.6 글쓰기 도구 §6–§9]]이다.

독자는 절차보다 높이와 간격을 먼저 보기 때문에 그림은 설득력이 강하다. 그래서 분모 누락이 중요하다. 작은 표본의 성공률 막대도 훨씬 많은 독립 노출로 얻은 막대처럼 정밀해 보일 수 있다.

같은 파지 결과를 먼저 막대로, 다음에는 시행 수·불확실성 구간·조건 이름과 함께 그려 보자. 막대는 순위를 보게 한다. 보강한 그림은 우위가 불확실한지, 특정 재료가 평균을 좌우하는지, 반복 시행이 같은 물체를 공유하는지 보게 한다. 데이터는 같지만 방어 가능한 결론이 드러나는 정도가 달라진다.

**여기서 얻는 독법.** 점·막대·구간 뒤의 단위를 확인한다. 캡션에는 집계, 구간 계산 방식, 제외 규칙이 있어야 한다. 일반화를 주장한다면 조건 이름이 분포 이동을 드러내야 한다. 전체 평균 속에 감추면 안 된다.

**RS1의 그림.** 맨 위의 그림을 논문이 싣는 모양, 곧 그림 1로 옮긴 것이다. 완성본은 그 그림이고, 여기서는 평균의 차 칸을 빼며 그 숫자는 캡션이 계산 예제의 표 1로 보낸다. 그 표는 이미 이 절의 표 규칙을 따른다. 단위, 결과 행마다 붙은 개선 방향 화살표, 모든 비교와 모든 비율에 붙은 구간, 제어기당 $n$, 그리고 절차마다 이름을 밝힌 캡션이다.

<svg viewBox="0 0 560 230" style="max-width:100%;height:auto" role="img" aria-label="RS1 파일럿: 최대 접촉력 스무 개를 한 축 위의 점으로, 10 N 성공선, 그리고 제어기마다 평균과 95% 신뢰구간">
  <rect x="90" y="34" width="220" height="146" fill="currentColor" fill-opacity="0.06"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.45">
    <line x1="90" y1="190" x2="530" y2="190"/>
    <line x1="90" y1="190" x2="90" y2="195"/><line x1="134" y1="190" x2="134" y2="195"/><line x1="178" y1="190" x2="178" y2="195"/><line x1="222" y1="190" x2="222" y2="195"/><line x1="266" y1="190" x2="266" y2="195"/><line x1="310" y1="190" x2="310" y2="195"/><line x1="354" y1="190" x2="354" y2="195"/><line x1="398" y1="190" x2="398" y2="195"/><line x1="442" y1="190" x2="442" y2="195"/><line x1="486" y1="190" x2="486" y2="195"/><line x1="530" y1="190" x2="530" y2="195"/>
  </g>
  <line x1="310" y1="30" x2="310" y2="190" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 3" opacity="0.8"/>
  <g fill="currentColor">
    <circle cx="208.8" cy="80" r="4"/><circle cx="226.4" cy="80" r="4"/><circle cx="270.4" cy="80" r="4"/><circle cx="283.6" cy="80" r="4"/><circle cx="301.2" cy="75" r="4"/><circle cx="305.6" cy="85" r="4"/><circle cx="367.2" cy="80" r="4"/><circle cx="424.4" cy="80" r="4"/><circle cx="481.6" cy="80" r="4"/><circle cx="521.2" cy="80" r="4"/>
    <circle cx="129.6" cy="140" r="4"/><circle cx="142.8" cy="140" r="4"/><circle cx="160.4" cy="140" r="4"/><circle cx="169.2" cy="140" r="4"/><circle cx="182.4" cy="140" r="4"/><circle cx="200.0" cy="140" r="4"/><circle cx="217.6" cy="135" r="4"/><circle cx="222.0" cy="145" r="4"/><circle cx="239.6" cy="140" r="4"/><circle cx="336.4" cy="140" r="4"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6">
    <line x1="263.1" y1="104" x2="414.8" y2="104"/><line x1="263.1" y1="100" x2="263.1" y2="108"/><line x1="414.8" y1="100" x2="414.8" y2="108"/>
    <line x1="157.3" y1="164" x2="242.7" y2="164"/><line x1="157.3" y1="160" x2="157.3" y2="168"/><line x1="242.7" y1="160" x2="242.7" y2="168"/>
  </g>
  <g fill="currentColor">
    <path d="M339.0 99 L344 104 L339.0 109 L334 104 Z"/>
    <path d="M200.0 159 L205 164 L200.0 169 L195 164 Z"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="90" y="206">5</text><text x="134" y="206">6</text><text x="178" y="206">7</text><text x="222" y="206">8</text><text x="266" y="206">9</text><text x="310" y="206">10</text><text x="354" y="206">11</text><text x="398" y="206">12</text><text x="442" y="206">13</text><text x="486" y="206">14</text><text x="530" y="206">15</text>
  </g>
  <g font-size="12" fill="currentColor">
    <text x="20" y="84">A</text><text x="20" y="144">B</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.85">
    <text x="20" y="99">6/10 &#8804; 10 N</text>
    <text x="20" y="159">9/10 &#8804; 10 N</text>
    <text x="96" y="46">성공: 최댓값 &#8804; 10 N</text>
    <text x="316" y="40">10 N, 파일럿 전에 고정</text>
    <text x="420" y="107">평균, 95% 신뢰구간</text>
  </g>
  <text x="310" y="224" font-size="11" fill="currentColor" text-anchor="middle">시행별 최대 접촉력 (N)</text>
</svg>

*그림 1. RS1 파일럿(예시 데이터): 400 N/m 패널에 대한 팔 P2의 제어기당 대응 없는 시행 10회, 모든 시행의 최대 접촉력. 점은 시행 하나이고, 각 줄 아래의 다이아몬드와 막대는 평균과 그 95% t-구간이다(A: 10.66 N, [8.93, 12.39]; B: 7.50 N, [6.53, 8.47]). 점선은 파일럿 전에 고정한 10 N 성공 문턱이고, 칠한 쪽이 성공이다. 평균의 차 3.16 N과 Welch 95% 신뢰구간 [1.28, 5.04]는 표 1에 있다.*

**이 그림이 대신하는 그림.** 흔한 기본값은 평균 위치의 막대 둘에 ±1 표준편차 수염을 단 것이다. A의 수염은 8.25–13.07 N, B는 6.14–8.86 N에 걸치므로 수염이 겹친다. 겹침을 "차이 없음"으로 읽는 독자는 표 1과 정반대의 결론을 낸다(Cumming & Finch 2005). 막대는 점이 한눈에 보여 주는 것도 감춘다. 선 바로 아래 쌓인 A의 최댓값 넷, 곧 성공 개수가 흔들리기 쉬운 이유, 그리고 선 위에 있는 B의 최댓값 하나다(Weissgerber 등 2015).

### 5. Results와 Discussion

Results는 측정된 결과를 보고한다. Discussion은 원인, 한계, 이전 가능성을 해석한다.
"방법 A의 실패가 적었다"는 result다; "촉각 피드백이 더 이른 미끄럼 회복을 가능하게 했다"
는 진단 증거를 요구하는 기전적 해석이다.

**수정 전:** “촉각 시스템은 접촉을 이해했기 때문에 실패가 적었다.” **문제:** 앞은 결과이고 뒤는 측정 대상을 밝히지 않은 기전이다. **결과로 분리:** “짝지은 절차에서 촉각 조건의 관찰 실패가 적었다.” **논의로 분리:** “더 이른 미끄러짐 감지가 후보 설명이다. 이를 시험하려면 동기화된 센싱·회복 로그가 필요하다.”

**수정 전:** “모델이 일반화했으므로 전이 가능한 물리 지식을 배웠다.” **문제:** 보지 못한 집합의 성공만으로 원인 표현을 알 수 없다. **결과로 분리:** “선언한 미관측 배치에서 과제를 완료했다.” **논의로 분리:** “해당 배치 사이의 전이를 지지한다. 다른 재료로의 전이는 시험하지 않았다.”

가상 예제지만 두 부분에 모두 증거가 생긴 뒤에도 이 구분은 유용하다. **여기서 얻는 독법.** 측정 기록에서 바로 옮길 수 있는 것과 추가 논증이 필요한 것을 구분한다. 추가 논증은 근거 분석 곁에 두고 대안 설명도 보이게 한다.

**RS1.** *결과:* "B의 평균 최대 접촉력은 A보다 3.16 N 낮았다(95% 신뢰구간 1.28–5.04 N)." *논의:* "후보 설명은 B의 컴플라이언스가 제어기에게 접촉을 다듬을 시간을 준다는 것이다. [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]의 반정현 모델에서 400 N/m 패널과의 접촉은 약 0.22 s 이어진다. 힘–시간 기록으로 이를 시험할 수 있다." 첫 문장은 표 1에서 그대로 옮긴 것이다. 둘째 문장은 파일럿이 기록하지 않은 측정이 필요하므로 후보로 남는다.

### 6. Limitations

시험하지 않은 환경, 데이터·컴퓨트 의존성, 하드웨어 가정, 개입/리셋, 실패 모드, 안전
경계, 가능성 높은 분포 이동을 명시하라. Limitations는 논문을 약하게 만드는 것이 아니라
근거 없는 일반화를 막는다.

**수정 전:** “더 어려운 조건은 향후 연구에서 다룬다.” **문제:** 관련 조건에서 실패했는지 아예 시험하지 않았는지 알 수 없다. **수정 후:** “젖은 표면은 평가에 포함하지 않았다. 현재 증거는 접촉 마찰이 바뀔 때의 전이를 확립하지 않는다.”

**수정 전:** “가끔 사람의 도움이 필요하다.” **문제:** 개입 원인과 자율성 주장에 미치는 영향이 숨는다. **수정 후:** “위치 추정이 끊기면 운전자가 로봇을 리셋한다. 해당 에피소드는 자율 시도의 실패로 남기고 보조 완료를 별도 보고한다.”

가상의 경계이므로 실제 한계 절에서는 기록된 조건으로 바꾼다. 경계가 센싱, 학습 범위, 제어, 평가 중 어디에 있는지 설명한다. 그래야 다른 곳에서 쓰려는 독자가 필요한 변경을 판단한다.

**여기서 얻는 독법.** 한계는 주장이 어디서 더 이상 성립하지 않을지 예측하게 해야 한다. 향후 연구의 약속은 기존 실패나 빠진 증거를 먼저 명시한 뒤에야 쓸모가 있다. 약속이 설명을 대신할 수는 없다.

**논문에 들어갈 RS1의 한계 문단.**

> 파일럿은 팔 모델 하나(P2)와 패널 강성 하나(400 N/m)에서, B의 목표 임피던스, A의 정지 문턱, 접근 속도와 방향을 각각 한 설정으로 두고 제어기당 대응 없는 시행 10회를 비교했다. 최대 접촉력은 위험 하나, 곧 패널에 가해지는 과도한 힘의 대리 지표이며, 끼임이나 공구 손상 같은 다른 위험은 재지 않는다. 이 크기에서 성공률 비교는 정보가 없다. 차이의 95% 구간은 $-0.08$에서 $+0.60$까지이고, 시행 10회 설계는 참인 0.6 대 0.9의 차이를 $\alpha = 0.05$의 Fisher 정확 검정으로 약 15%의 경우에만 검출한다. 뻣뻣한 구조물에 대해서는 반정현 모델에서 접촉이 약 16배 짧아지므로($\sqrt{10^5/400} = 15.8$), 이 결과는 그곳에서의 B의 이점을 확립하지 않는다.

문장마다 독자가 확인할 수 있는 경계 — 모델, 강성, 파라미터 설정, 대리 지표, 검정력, 접촉 체제 — 를 하나씩 밝히고, 어느 문장도 경계 대신 향후 연구를 내밀지 않는다. 15%는 가능한 파일럿 결과 $11 \times 11$개를 모두 열거한 정확한 값이다. 정규근사로는 33%이고, 둘 다 [[06-research-practice/real-world-impact|6. 실세계 임팩트]]에서 유도한다.

### 7. Peer review

각 코멘트를 사실 정정, 명료화 요청, 증거 부족, 범위 이견, 선호로 분해하라. 응답 방식:

- **Agree:** 인정하고 수정한다.
- **Clarify:** 오해를 설명하고, 다른 독자가 같은 오해를 하지 않게 논문을 고친다.
- **Revise:** 분석·실험·인용·한계를 추가한다.
- **Rebut:** 증거와 범위로, 요구된 결론이 따라 나오지 않음을 정중히 보인다.

원고의 어디가 바뀌었는지 정확히 밝혀라. 새 실험이 측정한 것 이상을 증명한다고 주장하지
말라.

예를 들어 “novelty is unclear”는 서로 다른 결함을 가리킬 수 있다. 가장 가까운 선행 방법을 정확히 설명했는지, 원고가 구체적 차이를 밝혔는지, 실험이 그 차이가 중요한 이유를 보여 주는지 확인한다. 새 신경망 부품이 없어도 시스템 기여는 성립할 수 있다. 통합 노력만으로 이 질문에 답하지는 못한다.

접촉 중 상태 갱신이 차이라고 설명하고, 관련연구 분류에 빠진 비교를 넣고, 실험이 통합 시스템만 지지하면 기여 범위를 줄이는 답변이 가능하다. **여기서 얻는 독법.** 코멘트를 논증의 빠진 고리를 찾으라는 요청으로 읽는다. 신규성을 강조하는 형용사를 더해도 고리는 생기지 않는다. 확인 가능한 가정·인터페이스·평가의 차이가 필요하다.

**심사받는 RS1.** 첫 초안이 "더 안전하다"를 그대로 두었다고 하자. 심사자가 이렇게 쓴다. *"이 논문은 임피던스 제어가 더 안전하다고 결론짓지만, 성공률(9/10 대 6/10)은 유의하게 다르지 않고, 10 N 문턱에는 근거가 없다. B에 유리하도록 고른 것처럼 보인다."*

분해하면 이 코멘트에는 범위 이견("더 안전하다"), 증거 부족(성공 비교), 그리고 암묵적 의심이 담긴 사실 질문(문턱이 어디서 왔는가)이 들어 있다.

**응답 (Agree + Clarify + Revise).** "'더 안전하다'가 증거를 넘어섰다는 데 동의하며, 이를 전부(초록, §1, §6) 측정한 주장으로 바꿨습니다. 팔 모델 하나와 패널 강성 하나에서 제어기당 10회 파일럿의 평균 최대 접촉력이 더 낮았다는 것입니다. 성공률을 구별할 수 없다는 데에도 동의합니다(차이 +0.30, 95% 신뢰구간 −0.08–+0.60; Fisher 정확 검정 p = 0.30). 수정한 Results는 이를 그 말 그대로 적었고, Limitations에는 이 크기에서 설계의 검정력, 곧 참인 0.6 대 0.9의 차이에 대해 약 0.15를 밝혔습니다. 문턱에 대해: 10 N 선은 파일럿 전에 연구 계획서에서 고정했고(부록 A, 날짜 기재), 미리 정한 주 결과는 성공이 아니라 최대 접촉력이었습니다. 그 차이는 3.16 N(Welch 95% 신뢰구간 1.28–5.04 N)입니다. 투명성을 위해 새 표 S2에 8, 9, 11, 12 N에서의 성공 개수를 실었습니다. 그로부터는 어떤 추론도 하지 않습니다. 데이터를 본 뒤 고른 문턱은 그 p-값을 해석할 수 없게 만들기 때문입니다."

모든 요소가 원고의 한 자리로 추적되고, 데이터가 주장 쪽으로 옮겨 가는 것이 아니라 주장이 데이터 쪽으로 옮겨 간다. 응답이 하지 않는 일도 보자. 9 N 선으로 바꾸지 않는다. 그 선에서는 같은 스무 시행이 $p = 0.005$를 준다([[06-research-practice/research-questions-claims|1. 연구 질문과 주장]] 계산 예제 2단계). 그것을 결과로 보고하면 심사자의 의심이 사실이 된다. 이런 교환이 결정 전에 일어나는지는 venue의 규칙이다. [[06-research-practice/venue-strategy|5. Venue 전략 §2]]는 어느 venue가 반박문을 받고, 어느 venue가 수정본과 함께 응답을 받고, 어느 venue가 둘 다 받지 않는지를 기록하며, 그 worked case는 RS1의 논문을 보낼 곳을 정할 때 바로 그 차이를 따진다.

### 8. 예제: 리뷰 코멘트 하나, 규범적 응답 하나

**리뷰어**: "85% 성공률은 설득력이 없다 — 장면 하나에서만 시험됐고 베이스라인이 튜닝되지
않은 것으로 보인다."

**응답 (Agree + Revise + Clarify)**: "단일 장면 평가가 주장을 제한한다는 데 동의합니다. 물체
배치를 무작위화한 held-out 장면 2개를 추가했습니다(§5.2, 표 3): 성공률 85%, 80%, 80%(장면당 17/20, 16/20, 16/20. 이 $n$에서 이항 표준오차가 약 8%p이므로 이 표본만으로는 장면별 성능 차이를 명확히 분리하기 어렵습니다). 튜닝에 대해: BC 베이스라인은 같은 시연·인코더와, 저희와
동일한 12개 구성 하이퍼파라미터 탐색을 사용했습니다(부록 C); §5.1에 명시했습니다.
초록의 주장을 'robust manipulation'에서 '세 탁상 장면에 걸친 일관된 성공'으로
좁혔습니다."

응답의 표준오차는 장면 하나의 이항 표준오차 $\sqrt{p(1-p)/n}$이다. $p = 0.85$, $n = 20$이면 $\sqrt{0.1275/20} \approx 0.080$이고, $p = 0.80$이면 $\sqrt{0.16/20} \approx 0.089$이므로 약 8%p다. 같은 종류의 한계는 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §4]]에서 따라가 볼 수 있다.

모든 요소가 추적 가능하다: 우려를 재진술하고, 증거의 위치를 밝히고, 비교 프로토콜을
명시하고, 주장을 데이터에 맞게 재협상했다.

### 9. 산출물 정렬

논문, 부록, 코드, 데이터, 모델, 설정, 로그, 비디오는 호환되는 버전과 식별자를 참조해야
한다. 비디오는 행동을 보여 주지만 시행 분포와 실패 횟수를 대신하지 못한다. 논문 자체를 그 그림을 만드는 스크립트, 데이터와 함께 저장소에 두는 법은 [[02-foundations/tools/latex-figures-references|12.6 §10]]이다.

각각 올바른 산출물도 서로 다른 실험을 설명할 수 있다. 표는 제어기를 바꾸기 전 체크포인트를 쓰고, 공개 설정과 시연 영상은 나중 제어기를 쓸 수 있다. 독자가 코드를 정상 실행해도 보고 결과를 재현하지 못하는 이유다.

파지 시행마다 설정, 체크포인트, 보정, 원본 로그, 분석 출력을 연결하는 식별자를 붙인다. 표의 각 항목을 포함한 시행 식별자로 연결하고 제외 규칙을 기록한다. 실패 시행도 보존한다. 다른 설정을 보여 주는 영상이면 차이를 표시하고 표의 출처인 것처럼 제시하지 않는다.

**여기서 얻는 독법.** 그림에서 분석을 거쳐 원본 시도까지 거슬러 간다. 방법 절의 소프트웨어·하드웨어 설정에서 경로가 끝나는지 본다. 재현 가능한 산출물은 그럴듯한 이름의 파일을 모은 저장소가 아니라 확인 가능한 증거 사슬이다.

### 읽고 나면 말할 수 있어야 하는 것

- 범위가 한정된 주장–방법–증거 문장을 쓸 수 있다
- 논문 각 섹션의 고유한 역할을 설명할 수 있다
- Related work를 유용한 분류 체계로 조직할 수 있다
- 측정된 결과와 기전적 해석을 분리할 수 있다
- Limitations를 유효성 경계로 쓸 수 있다
- 리뷰어 코멘트를 분류하고 추적 가능한 수정으로 답할 수 있다
- Wilson, Welch, Fisher 항목으로 RS1의 결과 표를 만들고, 숫자마다 허락되는 문장과 허락되지 않는 이웃 문장을 짝지을 수 있다
- 모든 시행과 주장이 겨냥하는 구간을 보여 주는 결과 그림을 설계할 수 있다

### 스스로 점검

1. "우리 방법은 실세계에서 강건하다"에 빠진 것은?
2. Results와 Discussion을 분리해야 하는 이유는?
3. 검증하기 쉬운 응답 편지의 조건은?
4. 잘 다듬은 데모 비디오가 증거로 불충분한 이유는?
5. 표 1은 B의 성공을 0.90 [0.60, 0.98]로 인쇄한다. 공저자가 대신 "0.90 ± 0.19"로 쓰자고 한다. 무엇이 문제인가?
6. RS1의 Results 문단은 왜 "두 비율은 다르지 않았다"가 아니라 "파일럿은 이 두 비율을 구별하지 못한다"라고 쓰는가?

> [!tip]- 정답 · Answers
> 1. 방법, 비교 대상, 강건성/실세계의 조작적 정의, 조건, 시행 수, 지표, 불확실성, 실패.
> 2. 관찰과 인과적·일반화 해석을 구분하기 위해.
> 3. 우려를 인용·분해하고, 직접 답하고, 증거/수정을 기술하고, 정확한 위치를 준다.
> 4. 선택 편향, 생략된 실패/리셋, 알 수 없는 노출, 짝지은 베이스라인 부재.
> 5. "± 0.19"는 Wald 반폭 $1.96\sqrt{0.9 \times 0.1/10} = 0.186$이다. 구간을 대칭 $[0.71,\ 1.09]$로 만들어 1을 넘기고, 아래 끝을 Wilson 구간의 0.60에서 끌어올린다. 10번 중 9번은 0.60과도 양립하는데 독자에게는 B의 성공률이 적어도 0.71이라고 말하는 셈이다. 0이나 1 근처에서 정직한 구간은 한쪽으로 치우치고, 대칭 "±"는 그것을 말할 수 없다.
> 6. $p = 0.30$은 두 비율이 같다는 증거가 아니기 때문이다([[02-foundations/probability|3. 확률 §6]]의 오독 3). 차이의 95% 구간 $-0.08$–$+0.60$은 0도, 60%p의 우위도 담고 있고, 시행 10회 설계는 참인 0.6 대 0.9의 차이를 약 15%의 경우에만 검출한다. "다르지 않았다"는 같음을 단언하므로 허락된 문장 정의의 조건 (4)를 어기고, "구별하지 못한다"는 검정이 보여 준 것만 말한다.

### 과제 · Problem set

Tier B. RS1 위의 손 유도다. 이 페이지, 선수 지식, 이 페이지의 대상에 고정한 파일럿만 쓴다. 계산 예제와 다른 표다. 같은 스무 시행을 12 N 성공선 아래에서 다시 표로 만들고, 다른 심사평에 답한다.

1. **그리기.** 성공선을 12 N으로 옮겨 맨 위의 그림을 다시 그리고, 선의 반대편으로 넘어간 점을 표시한다. 그다음 그림에 두 번째 패널을 더한다. 0–1 축 위에 두 성공률을 점과 Wilson 95% 구간으로, 10 N과 12 N 정의 둘 다(구간 넷) 그리고 각각에 $k/n$을 적는다. 구간 쌍마다 겹치는 곳을 표시한다.
2. **유도.** 12 N 정의 아래에서 표 1의 성공 행을 만든다. (가) B의 10/10과 A의 7/10에 대한 Wilson 95% 구간을 손으로. (나) B − A에 대한 Newcombe 95% 구간, 그리고 가능한 표를 나열해 구하는 7/10 대 10/10의 Fisher 정확 검정 $p$. (다) 숫자마다 허락되는 문장, 허락되지 않는 이웃 문장 하나, 그리고 정의가 바뀌었으므로 표가 추가로 인쇄해야 하는 것.
3. **해석.** 두 번째 심사자가 이렇게 쓴다. "성공률이 유의하게 다르지 않으므로(p = 0.30), 이 논문은 임피던스 제어가 접촉 안전에 아무 효과가 없음을 보인다. 게재 불가." (가) §7의 범주로 코멘트를 분해한다. (나) 다섯 문장 이내의 규범적 응답을 쓴다. (다) 원고의 어느 부분이 바뀌고, 어느 부분은 바뀌면 안 되는가?

> [!note]- 그리는 법 · How to draw it
> - 그리는 코드를 쓰기 전에 손으로 그린다. 5 N에서 15 N까지의 최대 접촉력 가로축 하나, 점선 세로선으로 그은 성공선, 그리고 칠한 성공 쪽.
> - 선에는 그 값이 어디서 왔는지 적는다. 10 N 선은 파일럿 전에 고정했다. 데이터를 본 뒤 옮긴 선이라면 그렇다고 밝혀야 한다. 그러지 않으면 독자는 미리 정한 문턱과 나중에 고른 문턱을 구별할 수 없다.
> - 모든 시행을 점으로, 한 줄에 A의 열 개, 그 아래 줄에 B의 열 개. 막대가 아니라 점이어야 독자가 선 양쪽의 점을 셀 수 있다(10 N에서는 선 바로 아래 A의 최댓값 넷과 선 위의 B의 최댓값 하나). 거의 겹치는 점은 위아래로 비껴 찍어 서로 가리지 않게 한다.
> - 각 줄 아래에 평균과 그 95% t-구간, 띠 옆에 평균의 차와 그 Welch 구간. 주장은 차이에 관한 것이고 어느 줄의 구간도 그 질문에 답하지 않기 때문이다. 성공선을 옮겨도 이것들은 하나도 움직이지 않는다.
> - 두 번째 패널은 0–1 축이다. 성공률마다 점과 Wilson 95% 구간, 그리고 $k/n$을 적고, 성공 정의마다 한 쌍을 두며, 쌍마다 겹치는 구간을 표시한다.
> - Wilson 구간은 모양으로 검사한다. 중심이 1/2 쪽으로 당겨지므로 이 네 구간 중 어느 것도 자기 점을 중심으로 대칭이 아니고, 어느 것도 0이나 1을 넘지 않는다. 대칭인 구간, 1을 넘는 구간, $k = n$에서 점 하나로 줄어든 구간은 정의의 반례인 Wald 구간이다.
> - 캡션: 단위, 제어기당 $n$, 시행이 대응 없음, 점·다이아몬드·막대·구간이 각각 무엇인지, 문턱마다 어디서 왔는지, 제외한 시행이 없다는 것. 본문을 읽어야 이해되는 그림은 실패한 것이다.

> [!tip]- 정답 · Solutions
> 1. 선만 빼면 띠 그림은 그대로다. A의 11.3 N과 B의 10.6 N이 성공 쪽으로 넘어가 개수가 7/10과 10/10이 된다. 두 번째 패널: 10 N에서 A는 $0.60\ [0.31,\ 0.83]$, B는 $0.90\ [0.60,\ 0.98]$로 $[0.60,\ 0.83]$에서 겹친다. 12 N에서 A는 $0.70\ [0.40,\ 0.89]$, B는 $1.00\ [0.72,\ 1.00]$으로 $[0.72,\ 0.89]$에서 겹친다. B의 12 N 구간은 위 끝이 1에 붙어 있으면서도 0.72까지 내려간다. "열 번 중 열 번은 확실성이 아니다"를 그린 그림이다.
> 2. (가) $z^2/n = 0.384$로, 10/10은 중심 $(1 + 0.192)/1.384 = 0.861$, 반폭 $1.96\sqrt{0 + 0.0096}/1.384 = 0.139$이므로 $[0.722,\ 1.000]$이다. 7/10은 중심 $(0.7 + 0.192)/1.384 = 0.645$, 반폭 $1.96\sqrt{0.021 + 0.0096}/1.384 = 0.248$이므로 $[0.397,\ 0.892]$다. (나) Newcombe는 $\hat d = 1.0 - 0.7 = 0.30$에서 아래 끝 $0.30 - \sqrt{(1.0 - 0.722)^2 + (0.892 - 0.7)^2} = 0.30 - \sqrt{0.0773 + 0.0369} = 0.30 - 0.338 = -0.04$, 위 끝 $0.30 + \sqrt{(1.0 - 1.0)^2 + (0.7 - 0.397)^2} = 0.30 + 0.303 = 0.60$이다. Fisher는 주변합이 $n_A = n_B = 10$, 성공 $m = 17$이므로 A의 성공 수 $x$가 7부터 10까지다. 분자는 $\binom{10}{7}\binom{10}{10} = 120$, $\binom{10}{8}\binom{10}{9} = 450$, $\binom{10}{9}\binom{10}{8} = 450$, $\binom{10}{10}\binom{10}{7} = 120$이고 분모는 $\binom{20}{17} = 1140$이다. 관측한 $x = 7$의 확률은 $120/1140 = 0.105$, 그보다 확률이 크지 않은 표는 $x = 7$과 $x = 10$이므로 $p = 240/1140 = 0.211$이다. (다) "12 N 기준에서 B는 10회 모두 선 아래에 머물렀고(Wilson 95% 신뢰구간 0.72–1.00) A는 10회 중 7회였다(0.40–0.89). 파일럿은 이 두 비율도 구별하지 못한다(차이 $+0.30$, 95% 신뢰구간 $-0.04$–$+0.60$; Fisher 정확 검정 $p = 0.21$)." 허락되지 않는 이웃: "B는 12 N을 결코 넘지 않는다." 열 번의 시행은 열한 번째에 대해 아무 한계도 주지 않으므로 조건 (3)을, 구간이 0.72까지 내려가므로 조건 (4)를 어긴다. 선을 데이터를 본 뒤에 옮겼으므로 표는 미리 정한 10 N 행을 유지하고 12 N 행에는 사후 민감도 분석이라는 이름을 붙여야 한다. 12 N 행만 인쇄하면 1쪽 2단계의 갈림길이 된다.
> 3. (가) 사실 정정이 필요한 오독 — "유의하지 않음"을 "효과 없음"으로 읽은 것, [[02-foundations/probability|3. 확률 §6]]의 오독 3 — 과 범위 이견이다. 첫 심사 이후 논문은 "접촉 안전" 일반에 대해 아무것도 주장하지 않는다. "게재 불가"는 편집자에게 하는 권고이지 답할 논점이 아니다. (나) "파일럿이 두 성공률을 구별하지 못한다는 데 동의하며, 수정한 Results가 바로 그것을 적었습니다(Fisher 정확 검정 p = 0.30). 그러나 이것이 효과 없음을 보인다는 데에는 정중히 동의하지 않습니다. 0.05보다 큰 p-값은 두 비율이 같다는 증거가 아니고, 차이의 95% 신뢰구간 −0.08–+0.60은 효과 없음과 함께 큰 이점도 담고 있습니다. 시행 10회 설계가 참인 0.6 대 0.9의 차이를 약 15%의 경우에만 검출한다는 것도 Limitations에 밝혔습니다. 논문이 미리 정한 주 결과는 최대 접촉력이고, 그 차이는 3.16 N(Welch 95% 신뢰구간 1.28–5.04 N, p = 0.003)입니다. 논문은 접촉 안전 일반에 대해 아무것도 주장하지 않으며, 초록은 이 파일럿에서 평균 최대 접촉력이 더 낮았다는 것만 주장합니다." Clarify에 Rebut을 더한 응답이고, 문장마다 증거나 원고의 위치를 가리킨다. (다) 바뀌는 것: 첫 수정에서 아직 넣지 않았다면 Limitations의 검정력 문장. 바뀌면 안 되는 것: 최대 접촉력 결과와 범위를 정한 주장. "효과 없음"으로 물러서는 반박은 허락된 결과를 지우고, 논쟁에서 이기려고 성공 비교를 부풀리는 반박은 첫 심사가 잡아낸 바로 그 오류를 저지른다.

### 출처

- [Simon Peyton Jones — *How to Write a Great Research Paper* (Microsoft Research)](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/) — 주장 우선 글쓰기의 고전 강연
- [IEEE T-RO — Information for Reviewers](https://www.ieee-ras.org/publications/t-ro/t-ro-information-for-reviewers/) — 대표 로보틱스 저널의 리뷰어 점검 항목
- Edwin B. Wilson, "Probable inference, the law of succession, and statistical inference", *Journal of the American Statistical Association* 22(158):209–212 (1927) — 표 1 성공 행의 점수 구간
- Lawrence D. Brown, T. Tony Cai & Anirban DasGupta, "Interval estimation for a binomial proportion", *Statistical Science* 16(2):101–133 (2001) — 작은 $n$에서 Wald 구간이 실패하고 Wilson 구간을 권하는 이유
- Robert G. Newcombe, "Interval estimation for the difference between independent proportions: comparison of eleven methods", *Statistics in Medicine* 17(8):873–890 (1998) — 표 1 성공 비교의 혼합 점수 구간
- B. L. Welch, "The generalization of 'Student's' problem when several different population variances are involved", *Biometrika* 34(1–2):28–35 (1947), 그리고 F. E. Satterthwaite, "An approximate distribution of estimates of variance components", *Biometrics Bulletin* 2(6):110–114 (1946) — 분산이 다른 경우의 구간과 그 자유도
- R. A. Fisher, *The Design of Experiments* (Oliver & Boyd, 1935) — 주변합을 고정한 표 위의 정확 검정
- Geoff Cumming & Sue Finch, "Inference by eye: confidence intervals and how to read pictures of data", *American Psychologist* 60(2):170–180 (2005) — 겹치는 막대가 보여 주는 것과 보여 주지 않는 것
- Tracey L. Weissgerber, Natasa M. Milic, Stacey J. Winham & Vesna D. Garovic, "Beyond bar and line graphs: time for a new data presentation paradigm", *PLOS Biology* 13(4):e1002128 (2015) — 작은 표본의 결과를 개별 점으로 보여야 하는 이유
