---
title: 9. ML Practice & Evaluation
tags: [foundations]
study-depth: Working
wiki-support: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/neural-network-basics|0.8]] (training, validation, hyperparameters) · [[02-foundations/probability|3. Probability §1]] (conditional probability, for precision/recall) and [[02-foundations/probability|§6]] (the Student $t$ distribution and the confidence interval, which §4 and the worked case use)
> [[02-foundations/neural-network-basics|0.8]](학습·검증·하이퍼파라미터) · [[02-foundations/probability|3. 확률 §1]](정밀도·재현율을 위한 조건부 확률)과 [[02-foundations/probability|§6]](§4와 계산 예제가 쓰는 스튜던트 $t$ 분포와 신뢰구간)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/neural-network-basics|0.8]] and [[02-foundations/probability|3. Probability]]. Every page before this one was a tool for reading a method;
this is the tool for reading the claim that the method worked. Read it before any results table.*

The craft knowledge every paper assumes: how models are trained, validated, and — above
all — *measured*. This page is the decoder for every "Results" table in the wiki.

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]], this page sits on the mathematics floor under the last layer, task completion — how anyone knows that a layer got better — and in *"install that panel on the frame"* it serves the last step, *verify completion*: both the robot's check that the panel is seated and your check that a paper's system really seats it (its chip is on the [[physical-ai-map|Physical AI Map]]). Without it a table reads the way its authors hope: this page's crack detector, E1, scores $97\%$ accuracy where answering "fine" every time scores $94\%$, its precision falls from $0.80$ to $0.27$ on a better-built site, and a 16-point gain turns out to be one best seed against one worst seed, shrinking to $4.0\pm8.9$ points over four. Later pages build on this one section by section — [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]] turns this page's §1, §4 and §5 into design choices, [[04-robotics/system-identification|5.5 System Identification]] uses §1–§2, [[04-robotics/state-estimation-slam|3. State Estimation]] and [[04-robotics/tactile-visuotactile|14. Tactile Sensing]] use §3's metrics, and [[05-construction-robotics/imitating-contact|10. Imitating Contact]] reports its trials of a learned policy seating the panel by §1 and §5 — and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) it is tested by question 14 of block 1's [[02-foundations/overview#Gate check — are the foundations done?|foundations gate]] and is the reading half of block 5, research practice 2's trial design and Wilson interval. After it you can recompute precision, recall, AUC and an interval from a table's counts, and say what a table must state before its margin can be believed.

> [!note] First pass · 처음이라면
> About three sessions of 60–90 minutes. **Session 1:** the Running object and the picture, §1, then the two pieces the worked case needs — the *success rate* entry near the end of §3's dictionary, and §4's third bullet, on seeds, with its three quantities $s$, SE and the $t$ interval. **Session 2:** parts 1–4 of the worked case after §4 — the four counted metrics, AUC, the base rate and the three intervals, all on E1. **Session 3:** part 5, one seed against four, then §5, the traps, which are that object read wrong; finish with problem 1 and self-checks 1, 4 and 5. The rest of §3 is a dictionary to keep open next to a results table, and §2 and §6 are second-pass reading, absorbed by using them.

### Running object · 이 페이지의 대상

Evaluation is not a machine, so none of the six *plants* of [[02-foundations/lab-plants|0.6 Lab Plants]] — the wiki's frozen example systems **P1**–**P6**, *plant* being control's word for the system being controlled — fits. The nearest catalog entry is **P5**'s crack detector, and it is the wrong shape: P5 specifies *probabilities* — $P(+ \mid c) = 0.95$, $P(+ \mid \neg c) = 0.05$, $P(c) = 0.01$ — which is what a Bayes update needs, while every metric on this page is a ratio of **counts** on a finite test set, and that finiteness is the whole subject of §4. So this page freezes its own object and never changes its numbers afterwards. Every number in it is invented on purpose: it is a teaching object, not a measurement.

**E1 — one crack detector, three records.** The model scores each wall panel in $[0, 1]$, and a panel is *flagged* when its score reaches the deployed threshold $\tau = 0.55$.

**E1a, the full audit.** 1,000 panels, 60 of them really cracked. At $\tau = 0.55$ the detector flags 50, of which 40 are real:

| | predicted crack | predicted fine |
|---|---|---|
| **really cracked** | TP = 40 | FN = 20 |
| **really fine** | FP = 10 | TN = 930 |

**E1b, the score slice.** Seven panels **chosen to span the score range** — three cracked, four sound — with the raw scores recorded before any threshold, so that a sweep can be done by hand:

| truth | cracked | cracked | cracked | fine | fine | fine | fine |
|---|---:|---:|---:|---:|---:|---:|---:|
| score | 0.90 | 0.80 | 0.60 | 0.70 | 0.50 | 0.40 | 0.20 |

E1b is not a random sample of the site, so no rate computed on it estimates a deployment rate — it is here for ordering and for sweeping, and the self-check asks you to say why that distinction is not a technicality.

**E1c, the trial record.** Two further runs of the same system. A **site pilot**: a robot inspector attempts 10 independent panels and succeeds on 9. And a **seed record**: this method and the method it is compared against are each retrained on four random seeds under one matched recipe — same schedule, same budget, same 25-episode benchmark — giving successes out of 25 of 21, 22, 20, 19 (ours) and 18, 19, 20, 21 (the prior method). The published two-row table in §6 quotes one seed of each, our best and the prior method's worst: $22/25 = 0.88$ against $18/25 = 0.72$.

*Scope: this page teaches how to read a results table — what each metric counts, what it hides, and how wide its uncertainty is. It does not teach how to design the experiment that produced the table, which is [[06-research-practice/experimental-design-reproducibility|Experimental Design & Reproducibility]], nor the hypothesis tests behind the intervals, which are [[02-foundations/probability|3. Probability §6]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 426" style="max-width:100%;height:auto" role="img" aria-label="E1 in three panels: the confusion matrix at threshold 0.55 with the precision column and recall row ringed and TN shaded; the ROC operating point at FPR 0.011, TPR 0.667 with precision 0.80, or 0.27 at a tenth of the crack rate; and the normal, Wilson and bootstrap intervals for 9 of 10">
  <defs><marker id="aMl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">1 · the 2×2 box (E1a, τ = 0.55)</text>
  <rect x="178" y="124" width="78" height="44" stroke="none" fill="currentColor" fill-opacity="0.16"/>
  <rect x="100" y="80" width="156" height="88" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <line x1="178" y1="80" x2="178" y2="168" stroke="currentColor" stroke-width="1.2"/>
  <line x1="100" y1="124" x2="256" y2="124" stroke="currentColor" stroke-width="1.2"/>
  <text x="139" y="46" font-size="11" fill="currentColor" text-anchor="middle">predicted</text>
  <text x="139" y="60" font-size="11" fill="currentColor" text-anchor="middle">crack</text>
  <text x="217" y="46" font-size="11" fill="currentColor" text-anchor="middle">predicted</text>
  <text x="217" y="60" font-size="11" fill="currentColor" text-anchor="middle">fine</text>
  <text x="84" y="99" font-size="11" fill="currentColor" text-anchor="end">really</text>
  <text x="84" y="113" font-size="11" fill="currentColor" text-anchor="end">cracked</text>
  <text x="84" y="143" font-size="11" fill="currentColor" text-anchor="end">really</text>
  <text x="84" y="157" font-size="11" fill="currentColor" text-anchor="end">fine</text>
  <text x="139" y="106" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">TP = 40</text>
  <text x="217" y="106" font-size="12" fill="currentColor" text-anchor="middle">FN = 20</text>
  <text x="139" y="150" font-size="12" fill="currentColor" text-anchor="middle">FP = 10</text>
  <text x="217" y="150" font-size="12" fill="currentColor" text-anchor="middle">TN = 930</text>
  <rect x="96" y="69" width="86" height="110" rx="7" stroke="currentColor" stroke-width="2.2" fill="none"/>
  <rect x="89" y="76" width="178" height="52" rx="7" stroke="currentColor" stroke-width="2.2" fill="none" stroke-dasharray="6 3"/>
  <text x="217" y="196" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">neither ratio</text>
  <text x="217" y="210" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">uses this cell</text>
  <line x1="217" y1="182" x2="217" y2="172" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" marker-end="url(#aMl)"/>
  <line x1="14" y1="234" x2="40" y2="234" stroke="currentColor" stroke-width="2.2"/>
  <text x="46" y="238" font-size="11" fill="currentColor">precision = 40/50 = 0.80: the column</text>
  <line x1="14" y1="250" x2="40" y2="250" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <text x="46" y="254" font-size="11" fill="currentColor">recall = 40/60 = 0.667: the row</text>
  <text x="316" y="20" font-size="12" fill="currentColor">2 · ROC axes, one point</text>
  <line x1="346" y1="226" x2="526" y2="226" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <line x1="346" y1="226" x2="346" y2="46" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <line x1="346" y1="226" x2="346" y2="230" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="346" y="242" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <line x1="342" y1="226" x2="346" y2="226" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="339" y="230" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <line x1="436" y1="226" x2="436" y2="230" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="436" y="242" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="342" y1="136" x2="346" y2="136" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="339" y="140" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.5</text>
  <line x1="526" y1="226" x2="526" y2="230" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="526" y="242" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="342" y1="46" x2="346" y2="46" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="339" y="50" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">1</text>
  <text x="436" y="258" font-size="11" fill="currentColor" text-anchor="middle">FPR</text>
  <text x="339" y="38" font-size="11" fill="currentColor" text-anchor="end">TPR</text>
  <line x1="346" y1="226" x2="526" y2="46" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6" stroke-dasharray="4 4"/>
  <text x="490" y="107.2" font-size="11" fill="currentColor" fill-opacity="0.7">chance</text>
  <circle cx="347.9" cy="106" r="4.5" stroke="none" fill="currentColor"/>
  <text x="357.9" y="50" font-size="11" fill="currentColor">precision 0.80</text>
  <text x="357.9" y="65" font-size="11" fill="currentColor" fill-opacity="0.85">at 6% cracked</text>
  <text x="357.9" y="84" font-size="11" fill="currentColor">0.27: same point</text>
  <text x="357.9" y="99" font-size="11" fill="currentColor" fill-opacity="0.85">at 0.6% cracked</text>
  <text x="357.9" y="118" font-size="11" fill="currentColor" fill-opacity="0.85">(0.011, 0.667)</text>
  <text x="12" y="292" font-size="12" fill="currentColor">3 · three 95% intervals on 9/10 (E1c pilot)</text>
  <line x1="64" y1="380" x2="448" y2="380" stroke="currentColor" stroke-width="1.3"/>
  <line x1="64" y1="380" x2="64" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="64" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <line x1="160" y1="380" x2="160" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="160" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.25</text>
  <line x1="256" y1="380" x2="256" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="256" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="352" y1="380" x2="352" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="352" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.75</text>
  <line x1="448" y1="380" x2="448" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="448" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="409.6" y1="378" x2="409.6" y2="308" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="1 3"/>
  <line x1="448" y1="380" x2="448" y2="312" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="3 3"/>
  <line x1="338.2" y1="318" x2="448" y2="318" stroke="currentColor" stroke-width="2.4"/>
  <line x1="338.2" y1="313" x2="338.2" y2="323" stroke="currentColor" stroke-width="1.6"/>
  <line x1="448" y1="318" x2="481" y2="318" stroke="currentColor" stroke-width="2.4" stroke-dasharray="3 2"/>
  <line x1="481" y1="313" x2="481" y2="323" stroke="currentColor" stroke-width="1.6"/>
  <text x="330.2" y="322" font-size="11" fill="currentColor" text-anchor="end">normal approximation [0.714, 1.086]</text>
  <line x1="292.8" y1="338" x2="441.1" y2="338" stroke="currentColor" stroke-width="2.4"/>
  <line x1="292.8" y1="333" x2="292.8" y2="343" stroke="currentColor" stroke-width="1.6"/>
  <line x1="441.1" y1="333" x2="441.1" y2="343" stroke="currentColor" stroke-width="1.6"/>
  <text x="284.8" y="342" font-size="11" fill="currentColor" text-anchor="end">Wilson [0.596, 0.982]</text>
  <line x1="332.8" y1="358" x2="448" y2="358" stroke="currentColor" stroke-width="2.4"/>
  <line x1="332.8" y1="353" x2="332.8" y2="363" stroke="currentColor" stroke-width="1.6"/>
  <line x1="448" y1="353" x2="448" y2="363" stroke="currentColor" stroke-width="1.6"/>
  <text x="324.8" y="362" font-size="11" fill="currentColor" text-anchor="end">percentile bootstrap [0.70, 1.00]</text>
  <circle cx="448" cy="318" r="3.6" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.0"/>
  <text x="548" y="305" font-size="11" fill="currentColor" text-anchor="end">leaves the axis at 1</text>
  <text x="456" y="342" font-size="11" fill="currentColor" fill-opacity="0.85">inside [0, 1]</text>
  <text x="456" y="362" font-size="11" fill="currentColor" fill-opacity="0.85">capped at 1.00</text>
  <path d="M404.6 389 L409.6 382 L414.6 389 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="409.6" y="414" font-size="11" fill="currentColor" text-anchor="middle">p̂ = 0.9 (9 of 10)</text>
</svg>

E1 in three panels, first E1a's confusion matrix at $\tau=0.55$ — $TP=40$, $FN=20$, $FP=10$, $TN=930$ — with the precision column ($40/50=0.80$) and the recall row ($40/60=0.667$) ringed, crossing at TP, and TN shaded because neither ratio uses it. On the ROC axes — true-positive rate against false-positive rate, defined in part 2 of the worked case — the same detector is one point, $(\text{FPR},\ \text{TPR})=(0.011,\ 0.667)$, with precision $0.80$ at 6% cracked and $0.27$ at 0.6% cracked, though the point itself does not move. The strip holds three 95% intervals on E1c's pilot of 9 of 10, $\hat p=0.9$, all three derived in part 4 of the worked case: the normal approximation $[0.714,\ 1.086]$ runs off the axis at $1$, Wilson $[0.596,\ 0.982]$ stays inside $[0,1]$, and the percentile bootstrap $[0.70,\ 1.00]$ is capped at $1.00$.

### 1. Data splits — the one sacred rule

A number measured on data that shaped the model — directly, or through a choice made while looking at it — says little about new panels, and it errs on the flattering side. This section is the rule that keeps a test number honest, and the quiet ways it gets broken.

- **Train / validation / test**: fit on train; tune hyperparameters and pick checkpoints
  on validation; touch test **once**, at the end. Every time a decision is influenced by
  test performance, the test set silently becomes a validation set — and reported numbers
  inflate.
  - *What kind of thing it is:* a partition of the available data $\mathcal{D}$ into three **disjoint** subsets, each with one job. The two conditions that make it a split rather than three folders are disjointness and a shared distribution:
  $$\mathcal{D} = \mathcal{D}_{\text{tr}} \cup \mathcal{D}_{\text{val}} \cup \mathcal{D}_{\text{te}}, \qquad \mathcal{D}_{\text{tr}} \cap \mathcal{D}_{\text{val}} = \mathcal{D}_{\text{tr}} \cap \mathcal{D}_{\text{te}} = \mathcal{D}_{\text{val}} \cap \mathcal{D}_{\text{te}} = \varnothing$$
  and each subset is drawn from the same distribution as the deployment data, so the test error $\hat R_{\text{te}} = \frac{1}{|\mathcal{D}_{\text{te}}|}\sum_{(x,y)\in\mathcal{D}_{\text{te}}} L(f(x), y)$ — the average loss over test examples, $|\cdot|$ counting them — is an unbiased estimate of the error on new data *only if* nothing about $\mathcal{D}_{\text{te}}$ influenced $f$. Worked: 10,000 samples split 80/10/10 give 8,000 / 1,000 / 1,000.
  - **Non-example:** 10,000 frames from 20 robot videos, shuffled and split 80/10/10. The sets are disjoint as *frames* but not as *episodes* — neighbouring, nearly identical frames land on both sides — so the test number measures interpolation between frames of scenes the model has already seen. The unit you split on must be the unit you want to generalize over: episode, scene, site or robot.
- **Distribution shift**: test data from a different distribution than train (new site,
  new robot, new lighting) — the *actual* condition of robotics. This is why papers report
  "seen/unseen" splits ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]]) and OOD evaluations, and
  why [[01-canonical-papers/notes/3-vlm/clip|CLIP]]'s robustness results mattered so much.
  - *Definition:* $p_{\text{tr}}(x, y) \ne p_{\text{te}}(x, y)$, where $p(x, y)$ is the joint distribution of inputs and labels. Since $p(x, y) = p(x)\,p(y \mid x) = p(y)\,p(x \mid y)$, there are three named kinds, depending on which factor moves:
    - **covariate shift** — $p(x)$ changes, $p(y \mid x)$ does not: new lighting, same meaning of "crack". This is also the imitation-learning failure mode, where the policy's own states are the shifted inputs ([[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]]);
    - **label (prior) shift** — $p(y)$ changes, $p(x \mid y)$ does not: the crack rate drops from 6% to 0.6%, and a crack still looks like a crack. The ROC-versus-precision table in the worked case (after §4) is exactly this case;
    - **concept shift** — $p(y \mid x)$ itself changes: a site adopts a stricter definition of a reportable crack, so the same image gets a different label.
  - **Out-of-distribution (OOD)** inputs are the extreme case: test inputs from regions where $p_{\text{tr}}(x)$ is essentially zero, so the model has no data to interpolate from.
- Data leakage: test information sneaking into training (duplicates, temporal overlap,
  pretraining contamination — the [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] paper's own
  headache). First thing to suspect when numbers look too good.
  - *Definition:* any path by which information from $\mathcal{D}_{\text{te}}$ (or $\mathcal{D}_{\text{val}}$) reaches the fitted model or the choices made about it, which breaks the "nothing about $\mathcal{D}_{\text{te}}$ influenced $f$" condition above. Its forms are exact or near-duplicate examples on both sides, temporal overlap (training on data recorded after the test period), contamination of a pretraining corpus, and **preprocessing fitted on all the data** — for instance normalization means and variances computed before the split, which quietly carries test statistics into training.

### 2. Overfitting and the regularization umbrella

A model can fit its training data ever better while getting worse on data it has not seen — a crack detector that has learned one site's lighting rather than the crack. This section shows how two loss curves reveal it, and what each of the four standard remedies changes.

- **Overfitting**: train loss ↓ while validation loss ↑ — memorizing instead of
  generalizing. **Underfitting**: both stay high. Diagnose with **learning curves** before
  anything else.
  - *The quantity behind both words* is the **generalization gap**, the difference between the average loss on held-out data and on training data at the same parameters $\theta_k$ after $k$ epochs:
  $$\text{gap}_k = R_{\text{val}}(\theta_k) - R_{\text{tr}}(\theta_k)$$
  so a learning curve is just $R_{\text{tr}}$ and $R_{\text{val}}$ plotted against $k$. **Overfitting** is named by two conditions together: $R_{\text{tr}}$ still falling *and* $R_{\text{val}}$ rising, so the gap grows. **Underfitting** is $R_{\text{tr}}$ itself staying high, so the model cannot even fit the data it sees. Worked: epoch 10 at train 0.40 / validation 0.45 (gap 0.05, both still falling — neither); epoch 50 at train 0.05 / validation 0.70 (gap 0.65, validation up from 0.45 — overfitting).
  - **Non-example:** a large but *constant* gap with validation loss still falling is not overfitting yet; it says the validation data are harder or differently distributed, and stopping there would throw away progress.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="training and validation loss against epochs: at epoch 10 train 0.40 and validation 0.45, both falling; validation bottoms out near epoch 21 and rises to 0.70 at epoch 50 while training falls to 0.05">
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6"><line x1="62.0" y1="196.0" x2="530.0" y2="196.0"/><line x1="62.0" y1="196.0" x2="62.0" y2="24.0"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6"><line x1="62.0" y1="196.0" x2="62.0" y2="200.0"/><line x1="140.0" y1="196.0" x2="140.0" y2="200.0"/><line x1="218.0" y1="196.0" x2="218.0" y2="200.0"/><line x1="296.0" y1="196.0" x2="296.0" y2="200.0"/><line x1="374.0" y1="196.0" x2="374.0" y2="200.0"/><line x1="452.0" y1="196.0" x2="452.0" y2="200.0"/><line x1="530.0" y1="196.0" x2="530.0" y2="200.0"/><line x1="58.0" y1="196.0" x2="62.0" y2="196.0"/><line x1="58.0" y1="154.5" x2="62.0" y2="154.5"/><line x1="58.0" y1="113.0" x2="62.0" y2="113.0"/><line x1="58.0" y1="71.5" x2="62.0" y2="71.5"/><line x1="58.0" y1="30.0" x2="62.0" y2="30.0"/></g>
  <text x="62.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="140.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">10</text>
  <text x="218.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">20</text>
  <text x="296.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">30</text>
  <text x="374.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">40</text>
  <text x="452.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">50</text>
  <text x="530.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">60</text>
  <text x="55.0" y="200.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0</text>
  <text x="55.0" y="158.5" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.25</text>
  <text x="55.0" y="117.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.5</text>
  <text x="55.0" y="75.5" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.75</text>
  <text x="55.0" y="34.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">1</text>
  <text x="296.0" y="227.0" font-size="12" fill="currentColor" text-anchor="middle">epoch</text>
  <text x="55.0" y="20.0" font-size="12" fill="currentColor" text-anchor="end">loss</text>
  <line x1="225.8" y1="30.0" x2="225.8" y2="92.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="225.8" y1="125.0" x2="225.8" y2="196.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <text x="230.8" y="38.0" font-size="12" fill="currentColor">early stopping</text>
  <polyline points="62.0,30.0 65.9,37.6 69.8,44.9 73.7,51.8 77.6,58.4 81.5,64.7 85.4,70.6 89.3,76.3 93.2,81.7 97.1,86.9 101.0,91.8 104.9,96.4 108.8,100.9 112.7,105.1 116.6,109.2 120.5,113.0 124.4,116.6 128.3,120.1 132.2,123.4 136.1,126.6 140.0,129.6 143.9,132.5 147.8,135.2 151.7,137.8 155.6,140.2 159.5,142.6 163.4,144.8 167.3,147.0 171.2,149.0 175.1,150.9 179.0,152.8 182.9,154.5 186.8,156.2 190.7,157.8 194.6,159.3 198.5,160.7 202.4,162.1 206.3,163.4 210.2,164.6 214.1,165.8 218.0,166.9 221.9,168.0 225.8,169.0 229.7,170.0 233.6,170.9 237.5,171.8 241.4,172.7 245.3,173.5 249.2,174.2 253.1,174.9 257.0,175.6 260.9,176.3 264.8,176.9 268.7,177.5 272.6,178.1 276.5,178.6 280.4,179.1 284.3,179.6 288.2,180.1 292.1,180.5 296.0,181.0 299.9,181.4 303.8,181.7 307.7,182.1 311.6,182.5 315.5,182.8 319.4,183.1 323.3,183.4 327.2,183.7 331.1,184.0 335.0,184.2 338.9,184.5 342.8,184.7 346.7,184.9 350.6,185.1 354.5,185.3 358.4,185.5 362.3,185.7 366.2,185.9 370.1,186.1 374.0,186.2 377.9,186.4 381.8,186.5 385.7,186.6 389.6,186.8 393.5,186.9 397.4,187.0 401.3,187.1 405.2,187.2 409.1,187.3 413.0,187.4 416.9,187.5 420.8,187.6 424.7,187.7 428.6,187.8 432.5,187.8 436.4,187.9 440.3,188.0 444.2,188.1 448.1,188.1 452.0,188.2 455.9,188.2 459.8,188.3 463.7,188.3 467.6,188.4 471.5,188.4 475.4,188.5 479.3,188.5 483.2,188.6 487.1,188.6 491.0,188.6 494.9,188.7 498.8,188.7 502.7,188.7 506.6,188.8 510.5,188.8 514.4,188.8 518.3,188.8 522.2,188.9 526.1,188.9 530.0,188.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="62.0,21.7 65.9,29.3 69.8,36.6 73.7,43.5 77.6,50.1 81.5,56.4 85.4,62.3 89.3,68.0 93.2,73.4 97.1,78.6 101.0,83.5 104.9,88.1 108.8,92.6 112.7,96.8 116.6,100.9 120.5,104.7 124.4,108.3 128.3,111.8 132.2,115.1 136.1,118.3 140.0,121.3 143.9,124.0 147.8,126.5 151.7,128.8 155.6,130.8 159.5,132.7 163.4,134.5 167.3,136.1 171.2,137.5 175.1,138.9 179.0,140.1 182.9,141.1 186.8,142.1 190.7,142.9 194.6,143.7 198.5,144.3 202.4,144.9 206.3,145.3 210.2,145.7 214.1,146.0 218.0,146.2 221.9,146.3 225.8,146.4 229.7,146.4 233.6,146.3 237.5,146.1 241.4,145.9 245.3,145.6 249.2,145.3 253.1,144.9 257.0,144.5 260.9,144.0 264.8,143.4 268.7,142.8 272.6,142.2 276.5,141.5 280.4,140.8 284.3,140.0 288.2,139.2 292.1,138.3 296.0,137.4 299.9,136.5 303.8,135.6 307.7,134.6 311.6,133.5 315.5,132.5 319.4,131.4 323.3,130.2 327.2,129.1 331.1,127.9 335.0,126.7 338.9,125.5 342.8,124.2 346.7,122.9 350.6,121.6 354.5,120.3 358.4,118.9 362.3,117.5 366.2,116.1 370.1,114.7 374.0,113.2 377.9,111.7 381.8,110.2 385.7,108.7 389.6,107.2 393.5,105.6 397.4,104.1 401.3,102.5 405.2,100.9 409.1,99.3 413.0,97.6 416.9,95.9 420.8,94.3 424.7,92.6 428.6,90.9 432.5,89.1 436.4,87.4 440.3,85.6 444.2,83.9 448.1,82.1 452.0,80.3 455.9,78.5 459.8,76.6 463.7,74.8 467.6,72.9 471.5,71.1 475.4,69.2 479.3,67.3 483.2,65.4 487.1,63.4 491.0,61.5 494.9,59.5 498.8,57.6 502.7,55.6 506.6,53.6 510.5,51.6 514.4,49.6 518.3,47.6 522.2,45.5 526.1,43.5 530.0,41.4" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>
  <circle cx="140.0" cy="129.6" r="3.6" fill="currentColor"/>
  <circle cx="140.0" cy="121.3" r="3.6" fill="currentColor"/>
  <line x1="140.0" y1="121.3" x2="140.0" y2="129.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <circle cx="452.0" cy="188.2" r="3.6" fill="currentColor"/>
  <circle cx="452.0" cy="80.3" r="3.6" fill="currentColor"/>
  <line x1="452.0" y1="80.3" x2="452.0" y2="188.2" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="147.0" y="105.3" font-size="12" fill="currentColor">epoch 10: 0.40 / 0.45</text>
  <text x="147.0" y="119.3" font-size="11" fill="currentColor" fill-opacity="0.8">gap 0.05, both falling</text>
  <text x="444.0" y="64.3" font-size="12" fill="currentColor" text-anchor="end">epoch 50: 0.05 / 0.70</text>
  <text x="444.0" y="78.3" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">gap 0.65: overfitting</text>
  <line x1="62.0" y1="248" x2="90.0" y2="248" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="96.0" y="252" font-size="12" fill="currentColor">validation loss — turns back up</text>
  <line x1="300" y1="248" x2="328" y2="248" stroke="currentColor" stroke-width="2"/>
  <text x="334" y="252" font-size="12" fill="currentColor">training loss — keeps falling</text>
</svg>

Training and validation loss through the two epochs of the example above: at epoch 10 they sit at $0.40$ and $0.45$, both still falling, and at epoch 50 at $0.05$ and $0.70$, a gap of $0.65$ with validation rising — overfitting. The shape between the two epochs is drawn for illustration; early stopping keeps the checkpoint at the validation minimum, the thin vertical line marked *early stopping*.


- Regularization methods share one broad goal — *reduce harmful overfit* — but work through
  different mechanisms: weight decay (a Gaussian prior — [[02-foundations/probability|3. Probability §4]]),
  dropout ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]), data augmentation
  ([[01-canonical-papers/notes/1-foundations/vgg|VGG]] onward), early stopping, and — the modern twist —
  *more data instead of more constraints* ([[01-canonical-papers/notes/1-foundations/scaling-laws|scaling laws]]).
  - *Definition:* a **regularizer** is any change to the learning procedure meant to lower the *validation* loss rather than the training loss. The explicit kind adds a penalty $\Omega$ on the parameters, weighted by a hyperparameter $\lambda \ge 0$:
  $$\min_\theta\ \frac{1}{N}\sum_{i=1}^{N} L\big(f_\theta(x_i), y_i\big) + \lambda\, \Omega(\theta), \qquad \Omega(\theta) = \tfrac12 \lVert\theta\rVert^2 \ \text{for L2}$$
  so a larger $\lambda$ trades training fit for smaller weights. The four named methods, each with its mechanism:
    - **Weight decay** shrinks every weight by a fixed factor each step, $w \leftarrow w(1 - \eta\lambda)$ with learning rate $\eta$; with $\eta = 0.1$ and $\lambda = 0.01$ the factor is $0.999$, and 1,000 steps with no opposing gradient leave $0.999^{1000} = 0.368$ of a weight. It equals the L2 penalty above for plain SGD (§6 has why it does not under Adam).
    - **Dropout** zeroes each hidden unit independently with probability $p$ during training and rescales the survivors, $\tilde h_j = m_j h_j / (1 - p)$ with $m_j \sim \text{Bernoulli}(1 - p)$, so the expected activation is unchanged and inference simply uses $h$. With $p = 0.5$, $h = (2, 4)$ and mask $m = (1, 0)$, the layer passes $(4, 0)$.
    - **Data augmentation** trains on $(T(x), y)$ for random transformations $T$ (crops, flips, colour jitter) chosen so that the label is unchanged. **Non-example:** a horizontal flip applied to a "turn left" demonstration is not augmentation, because it changes the correct label.
    - **Early stopping** keeps the checkpoint with the lowest validation loss, $\hat k = \arg\min_k R_{\text{val}}(\theta_k)$, which is the thin vertical line marked *early stopping* in the figure.

Regularization helps because fitting every training detail can make a model depend on accidental cues. A crack detector may learn a particular site’s lighting rather than the defect pattern. Augmentation can discourage that shortcut only if its transformations preserve the intended label and resemble meaningful variation. **The reading this gives you.** Read the learning curves together with the split and augmentation policy. Better validation loss on neighboring frames cannot demonstrate generalization to a new site, regardless of how many regularizers the method lists.

### 3. The metrics dictionary (read any Results table)

A results table names its metrics in a word — mAP, FID, success rate — and each word hides a formula with its own denominator and its own way of flattering a method. This section is the dictionary: what each metric counts, so that you can recompute it and see what it leaves out.

| Task | Metric | What it means |
|---|---|---|
| Classification | accuracy, top-5 | fraction correct (top-5: truth within 5 guesses — ImageNet convention) |
| Classification (imbalanced) | precision / recall / F1 | of flagged, how many real / of real, how many caught / their harmonic mean |
| Detection | **IoU**, **mAP** | box overlap ratio; mean over classes of average precision — at IoU 0.5 (PASCAL VOC) or averaged over IoU 0.50–0.95 (COCO); check which before comparing |
| Segmentation | mIoU | IoU averaged over classes |
| Generation (image) | **FID** | distribution distance between generated and real features — lower is better |
| Language modeling | perplexity | $2^{\text{cross-entropy}}$ in bits ([[02-foundations/information-theory\|5. Info Theory §2]]) |
| Translation/captioning | BLEU | n-gram overlap with references |
| Robotics | **success rate** | fraction of trials achieving the goal — plus *which* trials (seen/unseen) matters more than the number |
| Retrieval | recall@k | truth within top-k results |

Accuracy, precision, recall, $F_1$ and AUC are the metrics this page derives in full, and they are worked on **E1** in the worked case after §4 — with the base-rate collapse that makes an AUC on a balanced benchmark nearly uninformative about a deployment. The rest of the dictionary follows here.

#### The rest of the dictionary, with formulas

The table's one-line glosses are enough to recognize a metric; these are enough to recompute one. Each is a number computed from predictions and ground truth over a test set.

- **Top-$k$ accuracy.** The fraction of items whose true class is among the $k$ highest-scoring classes,
  $$\text{Acc}@k = \frac{1}{N}\sum_{i=1}^{N} \mathbb{1}\big[y_i \in \text{top-}k(\hat p_i)\big]$$
  so top-1 is ordinary accuracy, and top-5 forgives any ranking error inside the first five. An item whose true class the model ranks third counts as correct for top-5 and wrong for top-1, which is the whole gap between the two columns of an ImageNet table.
- **IoU (intersection over union).** For a predicted region $A$ and a ground-truth region $B$ (boxes or pixel masks), with $|\cdot|$ the area:
  $$\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
  which is 1 for a perfect match and 0 for no overlap. Boxes $[0,2]\times[0,2]$ and $[1,3]\times[1,3]$ overlap in a $1 \times 1$ square, so $\text{IoU} = 1/(4 + 4 - 1) = 1/7 = 0.143$. A detection counts as a TP only if its IoU with an unmatched ground-truth object reaches the threshold (0.5 for PASCAL VOC), so these two boxes would be a false positive *and* a miss.
- **AP and mAP.** Rank one class's detections by confidence; after the $n$-th detection record precision $P_n$ and recall $R_n$. Average precision is the area under that precision–recall curve,
  $$\text{AP} = \sum_{n} \big(R_n - R_{n-1}\big)\, P^{\text{interp}}_n, \qquad P^{\text{interp}}_n = \max_{m \ge n} P_m, \qquad \text{mAP} = \frac{1}{C}\sum_{c=1}^{C} \text{AP}_c$$
  where $R_0 = 0$, the interpolated precision is the best precision at this recall or higher, and mAP averages over the $C$ classes. Worked: two real objects, three detections ranked TP, FP, TP give $P = 1, 0.5, 0.667$ and $R = 0.5, 0.5, 1.0$, so $P^{\text{interp}} = 1, 0.667, 0.667$, and $\text{AP} = 0.5(1) + 0(0.667) + 0.5(0.667) = 0.833$. COCO additionally averages mAP over IoU thresholds $0.50, 0.55, \dots, 0.95$, so a COCO number and a VOC number are not the same quantity.
- **mIoU (segmentation).** Per class $c$, pixel counts give $\text{IoU}_c = TP_c / (TP_c + FP_c + FN_c)$; mIoU is their mean over classes. A class with $TP = 80$, $FP = 10$, $FN = 10$ has IoU $0.8$; a rare class with $TP = 5$, $FP = 10$, $FN = 5$ has $0.25$; mIoU is $0.525$ — the rare class pulls it down exactly as much as the common one pushes it up, which is the point of averaging per class.
- **FID (Fréchet Inception distance).** Fit a Gaussian to Inception-network features of real images, mean $\mu_r$ and covariance $\Sigma_r$, and another to generated images, $\mu_g, \Sigma_g$. FID is the Fréchet distance between the two Gaussians:
  $$\text{FID} = \lVert \mu_r - \mu_g \rVert^2 + \operatorname{Tr}\Big(\Sigma_r + \Sigma_g - 2\big(\Sigma_r \Sigma_g\big)^{1/2}\Big)$$
  so the first term penalizes a shifted average and the trace term a wrong spread; $\operatorname{Tr}$ is the sum of diagonal entries. In one dimension it reduces to $(\mu_r - \mu_g)^2 + (\sigma_r - \sigma_g)^2$: real $\mathcal{N}(0, 1^2)$ against generated $\mathcal{N}(0.5, 2^2)$ gives $0.25 + 1 = 1.25$. Lower is better, and FID depends on the sample count, so compare only at equal $N$.
- **Perplexity.** The exponentiated average next-token cross-entropy of a language model on held-out text of $N$ tokens:
  $$\text{PPL} = \exp\Big(-\frac{1}{N}\sum_{t=1}^{N} \ln p\big(x_t \mid x_{<t}\big)\Big) = 2^{H}, \quad H = -\frac{1}{N}\sum_{t=1}^{N} \log_2 p\big(x_t \mid x_{<t}\big)$$
  so it reads as "the model is as uncertain as a uniform choice among PPL tokens". If the model gives the true tokens probabilities $0.5$, $0.25$, $0.125$, then $H = (1 + 2 + 3)/3 = 2$ bits and $\text{PPL} = 4$. Perplexities computed with different tokenizers are not comparable, because $N$ counts different units.
- **BLEU.** A geometric mean of *clipped* $n$-gram precisions $p_n$ (each candidate $n$-gram counts at most as often as it appears in the reference), times a brevity penalty for candidates shorter than the reference:
  $$\text{BLEU} = \text{BP} \cdot \exp\Big(\sum_{n=1}^{4} \tfrac14 \log p_n\Big), \qquad \text{BP} = \begin{cases} 1 & c > r \\ e^{\,1 - r/c} & c \le r \end{cases}$$
  with $c$ and $r$ the candidate and reference lengths. Candidate "the cat sat on the mat" against reference "the cat is on the mat": $p_1 = 5/6$, $p_2 = 3/5$, $p_3 = 1/4$, $p_4 = 0/3$, $\text{BP} = 1$. **The boundary case:** one zero $p_4$ makes sentence-level BLEU exactly $0$ for a nearly correct sentence, which is why BLEU is computed over a whole corpus or with smoothing; the two-gram version here would be $\sqrt{(5/6)(3/5)} = 0.707$.
- **Success rate.** The fraction of trials achieving the goal: for $n$ independent trials with $k$ successes, $\hat p = k/n$, with binomial standard error
  $$\text{SE}\big(\hat p\big) = \sqrt{\frac{\hat p\,(1 - \hat p)}{n}}$$
  so the uncertainty shrinks only as $\sqrt n$ and is largest at $\hat p = 0.5$. At E1c's 9 of 10 it is $0.095$. *Which interval* to print around it is the part that goes wrong: the normal approximation, the Wilson interval ([[06-research-practice/experimental-design-reproducibility|Experiment Design §4]]) and the percentile bootstrap disagree at $n = 10$; all three are computed on E1c in the worked case after §4, where the Wilson interval gets its formula. The number is meaningless without the episode definition (§5). The same interval is worked against the Wald interval — the normal approximation's other name — on RS1, the research-practice track's frozen study comparing two force controllers on a panel ([[06-research-practice/index|6. Research Practice]]), whose pilot went 9/10 and 6/10, in the worked case of [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing]].
- **Recall@$k$ (retrieval).** The fraction of queries whose correct item is ranked within the first $k$ results, $\frac{1}{|Q|}\sum_{q \in Q} \mathbb{1}[\text{rank}_q \le k]$ over the query set $Q$. Three queries whose true items rank 1, 4 and 12 give recall@5 $= 2/3$. It shares a name with classification recall but not a denominator: here the denominator is queries, not positives.

- Read metrics adversarially: success rate on *what* distribution, of *how many* trials,
  with *what* variance? 9 successes in 10 trials has a wide confidence interval — report
  the counts and the uncertainty, not just "90%".

### 4. The grammar of experiments

A results table is an argument that one change caused one number; this section is how that argument is built — a tuned baseline, an ablation that changes one thing, enough seeds — and where it breaks.

- **Baseline**: what you must beat (and it must be *tuned* — weak baselines are the
  field's chronic sin). **Ablation**: remove one component to show it mattered — the
  evidence connecting method to result. **SOTA**: state of the art; impressive but
  fragile — benchmark-specific and often compute-confounded.
  - *Ablation, precisely:* a controlled comparison between the full method and the same method with exactly one component $c$ removed or replaced, everything else — data, compute budget, recipe, seeds, evaluation protocol — held fixed. Its output is an estimated effect,
  $$\Delta_c = M(\text{full}) - M(\text{full} \setminus c)$$
  where $M$ is the reported metric. Full method 76% success, the same method without action chunking 58%: $\Delta = 18$ percentage points attributed to chunking — and only to chunking if nothing else changed. **Non-example:** removing a component *and* shortening training to save compute measures both changes at once, so no $\Delta$ can be attributed to either.
  - *Baseline, precisely:* the comparison method must satisfy the same conditions — same data, same budget, same protocol — and be tuned with a search comparable to the proposed method's. A baseline that fails any one of them is not a baseline for that claim.
- Fair comparison checklist when reading: same data? same compute/params? same evaluation
  protocol? tuned baselines? If a table doesn't answer these, the numbers are decoration.
- Seeds and variance: deep learning results wobble across random seeds; serious reporting
  states the number of runs and an uncertainty measure fit to the experiment (std, standard
  error, CI, or paired tests), and robotics papers report over several *rollouts and scenes*. **Know which one you are looking at**: the standard deviation
  $\sigma$ says how much *individual runs* scatter and does not shrink as you add runs; the
  standard error $\sigma/\sqrt{n}$ says how well the *mean* is pinned down and does. At
  $n = 4$ they differ by a factor of 2, so a paper plotting the smaller one gets visually
  tighter error bars for free — check the caption before comparing two papers' bars. A seed that replays the same run, and still does after code is added, is [[02-foundations/tools/python-research-code|12.3 Python for Research Code §7]]; a caption that says which of the three its bars are is [[02-foundations/tools/latex-figures-references|12.6 Writing Tools §8]].
  - *The three quantities, written out* for $n$ runs with results $x_1, \dots, x_n$ and mean $\bar x$:
  $$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar x)^2}, \qquad \text{SE} = \frac{s}{\sqrt n}, \qquad \text{95\% CI} = \bar x \pm t_{0.975,\,n-1}\cdot \text{SE}$$
  The sample standard deviation $s$ divides by $n - 1$ because $\bar x$ was estimated from the same numbers; SE shrinks with $\sqrt n$ because averaging cancels run-to-run noise; and the **confidence interval** multiplies SE by a Student-$t$ quantile $t_{0.975,\,n-1}$, which is larger than the normal 1.96 when $n$ is small. It is a procedure that covers the true mean in 95% of repeated experiments, not a 95% probability statement about this one interval. The quantile $t_{0.975,\,\nu}$ is the value that a Student-$t$ variable with $\nu=n-1$ degrees of freedom exceeds with probability 2.5%. For Gaussian run-to-run noise, $(\bar x-\mu)/\text{SE}$ follows exactly that distribution ([[02-foundations/probability|3. Probability §6]] defines it): dividing by an *estimated* SE rather than the true one adds spread, so its tails are heavier than those of the standard normal, whose 97.5% point is $1.96$. It shrinks toward $1.96$ as runs accumulate, $t_{0.975,3}=3.182$, $t_{0.975,6}=2.447$ and $t_{0.975,30}=2.042$. Worked, four seeds at 72, 76, 80, 84% success: $\bar x = 78$, $s = 5.16$, $\text{SE} = 2.58$, $t_{0.975,3} = 3.18$, so the 95% CI is $[69.8, 86.2]$. The same four runs can therefore be drawn with bars of $\pm 2.6$, $\pm 5.2$ or $\pm 8.2$ points, depending on which quantity the caption names. How to test a *difference* between two methods is [[02-foundations/probability|3. Probability §6]]; the worked case just below runs that difference on E1c's two four-seed records, and the published 16-point gap does not survive it.

### Worked case · 대상으로 한 번 끝까지

**1. The four counted metrics, and why accuracy lies.** E1a's table is the **confusion matrix** of a binary classifier at one threshold: every test item lands in exactly one cell, named by whether the *prediction* was positive or negative and whether it was *true* or *false*. **TP** (true positive) = predicted crack, really cracked; **FP** (false positive, a false alarm) = predicted crack, really fine; **FN** (false negative, a miss) = predicted fine, really cracked; **TN** (true negative) = predicted fine, really fine. Every metric here is a ratio of those four counts:

$$\text{Accuracy} = \frac{TP + TN}{TP + FP + FN + TN}, \quad P = \text{Precision} = \frac{TP}{TP + FP}, \quad R = \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = \frac{2PR}{P + R}$$

so precision divides by the *predicted*-positive column and recall by the *really*-positive row, which is why the two answer different questions. $F_1$ is the harmonic mean of $P$ and $R$. Both precision and recall ignore TN, so they stay informative when negatives vastly outnumber positives. Substituting E1a's counts:

- **Accuracy** $= \frac{TP+TN}{1000} = \frac{970}{1000} = 97.0\%$ — and a detector that simply says "fine" every single time scores $\frac{940}{1000} = 94.0\%$. Accuracy is nearly useless here, and that 94% is the **non-example** that shows why: a metric which a constant answer nearly matches is not measuring the skill you care about.
- **Precision** $= \frac{TP}{TP+FP} = \frac{40}{50} = 0.80$ — of what you flagged, 80% was real. This is the number an inspector cares about: how often a dispatch is wasted.
- **Recall** $= \frac{TP}{TP+FN} = \frac{40}{60} = 0.667$ — of the real cracks you caught two-thirds. **20 cracks were missed**, and that is the number a safety engineer cares about.
- **F1** $= \frac{2PR}{P+R} = \frac{2(0.80)(0.667)}{1.467} = 0.727$ — the harmonic mean, which stays low if *either* is low. **Non-example:** the arithmetic mean of the same two numbers is $0.733$, and it scores a lopsided precision $0.9$ with recall $0.5$ at $0.70$ — barely lower — where the harmonic mean of that pair is $0.643$. Hiding a bad half behind a good one is exactly what $F_1$ refuses to do.

The lesson to carry into every Results table: precision and recall trade against each other through one threshold knob, so a paper reporting only the flattering one has told you half a sentence. And in construction the asymmetry is real — a false alarm costs an inspection, a missed crack can cost a structure.

**2. Ranking with no threshold at all: AUC on E1b.** Sweep the threshold and each setting gives a *true positive rate* $\text{TPR} = TP/(TP+FN)$ (that is recall) and a *false positive rate* $\text{FPR} = FP/(FP+TN)$. Plotting TPR against FPR traces the **ROC curve**, and the area under it is the **AUC**. AUC has an exact meaning worth carrying: it is the probability that a randomly chosen positive is scored above a randomly chosen negative. Take E1b's cracked panels $0.90, 0.80, 0.60$ against its sound ones $0.70, 0.50, 0.40, 0.20$: of the $3 \times 4 = 12$ pairs, 11 are ordered correctly, so $\text{AUC} = 11/12 = 0.917$ — no threshold involved. Written as the pair count it is:

$$\text{AUC} = \frac{1}{n_+ n_-} \sum_{i=1}^{n_+} \sum_{j=1}^{n_-} \Big( \mathbb{1}\big[s_i^+ > s_j^-\big] + \tfrac12\, \mathbb{1}\big[s_i^+ = s_j^-\big] \Big)$$

where $s_i^+$ are the $n_+$ positive items' scores, $s_j^-$ the $n_-$ negatives', and $\mathbb{1}[\cdot]$ is 1 when its condition holds and 0 otherwise; a tie counts half, since it is a coin flip. The one wrong pair above is the cracked $0.60$ below the sound $0.70$. AUC $= 0.5$ is chance ordering and $1$ is perfect. **Non-example:** AUC is not accuracy at the best threshold. Sweeping E1b, the best any single threshold does is 6 of 7 panels right, $0.857$ (at $\tau = 0.75$ and again at the deployed $\tau = 0.55$), while the AUC of those same seven scores is $0.917$, because AUC never commits to a threshold and is paid only for the ordering. **Why it matters:** a paper that reports only AUC has told you the model ranks well, and nothing about what happens when somebody has to pick a threshold and dispatch an inspector.

<svg viewBox="0 0 560 270" style="max-width:100%;height:auto" role="img" aria-label="the ROC curve of E1b as a staircase on a grid of 3 cracked by 4 sound panels: 11 of the 12 cells lie under it, so AUC = 11/12; the missing cell is the pair where the cracked 0.60 scored below the sound 0.70; thresholds 0.75 and 0.55 are marked">
  <rect x="170.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="170.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="222.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="222.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="222.0" y="42.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="274.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="274.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="274.0" y="42.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="326.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="326.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="326.0" y="42.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"><line x1="170.0" y1="222.0" x2="170.0" y2="42.0"/><line x1="222.0" y1="222.0" x2="222.0" y2="42.0"/><line x1="274.0" y1="222.0" x2="274.0" y2="42.0"/><line x1="326.0" y1="222.0" x2="326.0" y2="42.0"/><line x1="378.0" y1="222.0" x2="378.0" y2="42.0"/><line x1="170.0" y1="222.0" x2="378.0" y2="222.0"/><line x1="170.0" y1="162.0" x2="378.0" y2="162.0"/><line x1="170.0" y1="102.0" x2="378.0" y2="102.0"/><line x1="170.0" y1="42.0" x2="378.0" y2="42.0"/></g>
  <rect x="170.0" y="42.0" width="52.0" height="60.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3"/>
  <polyline points="170.0,222.0 170.0,162.0 170.0,102.0 222.0,102.0 222.0,42.0 274.0,42.0 326.0,42.0 378.0,42.0" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <text x="176.0" y="196.0" font-size="11" fill="currentColor">0.90</text>
  <text x="176.0" y="136.0" font-size="11" fill="currentColor">0.80</text>
  <text x="196.0" y="117.0" font-size="11" fill="currentColor" text-anchor="middle">0.70</text>
  <text x="228.0" y="76.0" font-size="11" fill="currentColor">0.60</text>
  <text x="248.0" y="57.0" font-size="11" fill="currentColor" text-anchor="middle">0.50</text>
  <text x="300.0" y="57.0" font-size="11" fill="currentColor" text-anchor="middle">0.40</text>
  <text x="352.0" y="57.0" font-size="11" fill="currentColor" text-anchor="middle">0.20</text>
  <text x="170.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="222.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1/4</text>
  <text x="274.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1/2</text>
  <text x="326.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">3/4</text>
  <text x="378.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1</text>
  <text x="162.0" y="226.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0</text>
  <text x="162.0" y="166.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">1/3</text>
  <text x="162.0" y="106.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">2/3</text>
  <text x="162.0" y="46.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">1</text>
  <text x="274.0" y="254.0" font-size="12" fill="currentColor" text-anchor="middle">FPR (false alarms among the 4 sound panels)</text>
  <text x="162.0" y="32.0" font-size="12" fill="currentColor" text-anchor="end">TPR</text>
  <circle cx="170.0" cy="102.0" r="5" fill="currentColor"/>
  <circle cx="222.0" cy="42.0" r="5" fill="currentColor"/>
  <text x="160.0" y="124.0" font-size="12" fill="currentColor" text-anchor="end">τ = 0.75</text>
  <text x="230.0" y="34.0" font-size="12" fill="currentColor">τ = 0.55 (deployed)</text>
  <text x="394.0" y="52.0" font-size="12" fill="currentColor" font-weight="600">AUC = 11/12 = 0.917</text>
  <text x="394.0" y="68.0" font-size="11" fill="currentColor" fill-opacity="0.85">11 of 12 cells shaded</text>
  <text x="394.0" y="128.0" font-size="11" fill="currentColor">walk the scores from high to low:</text>
  <text x="394.0" y="144.0" font-size="11" fill="currentColor">↑ a cracked panel</text>
  <text x="394.0" y="160.0" font-size="11" fill="currentColor">→ a sound panel</text>
  <text x="12" y="54.0" font-size="11" fill="currentColor">the one wrong pair:</text>
  <text x="12" y="69.0" font-size="11" fill="currentColor">cracked 0.60 below</text>
  <text x="12" y="84.0" font-size="11" fill="currentColor">sound 0.70</text>
  <line x1="128.0" y1="65.0" x2="192.0" y2="72.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
</svg>

E1b's seven scores walked from high to low: each cracked panel steps the curve up a third and each sound panel steps it right a quarter, so the $3\times4$ grid of cracked-against-sound pairs holds $11$ shaded cells under the staircase, $\text{AUC}=11/12=0.917$. The one empty cell is the only mis-ordered pair, the cracked $0.60$ below the sound $0.70$; the dots are the two thresholds that each get 6 of 7 panels right, $\tau=0.75$ at $(0,\ 2/3)$ and the deployed $\tau=0.55$ at $(1/4,\ 1)$.

**3. The same ROC point, a different base rate.** That threshold-independence is why AUC is reported, and the base-rate independence hiding behind it is why it misleads. E1a sits at $\text{TPR} = 40/60 = 0.667$ and $\text{FPR} = 10/940 = 0.011$. Move that same detector to a better-built site where only **0.6%** of panels are cracked instead of 6%, and out of 1,000 panels it now yields $TP = 0.667 \times 6 = 4.0$ and $FP = (10/940) \times 994 = 10.6$:

| | 6% cracked | 0.6% cracked |
|---|---|---|
| TPR | 0.667 | 0.667 — unchanged |
| FPR | 0.011 | 0.011 — unchanged |
| ROC point | identical | identical |
| **Precision** | **0.80** | **0.27** |

The ROC curve and the AUC do not move at all, while precision collapses by a factor of three. **TPR and FPR are conditional rates within the actual-positive and actual-negative groups**, so preserving the two class-conditional score distributions preserves the ROC curve even when the positive prevalence changes. Precision instead conditions on a positive prediction and therefore depends on prevalence. So an AUC measured on a balanced benchmark tells you almost nothing about how a system behaves in a deployment where positives are rare — the situation in [[04-robotics/human-intent-prediction|23. Intent prediction §5]], and in every alarm system on a site. When a paper reports AUC, ask for precision at a stated recall, on the deployment base rate.

**4. How wide is "9 out of 10"? A bootstrap on E1c.**

> [!info] Definition — percentile bootstrap confidence interval
> **What kind of thing it is:** an interval estimate produced by a *procedure*, not a formula read off an assumed distribution. Three conditions make a bootstrap a bootstrap: (1) each **resample** draws $n$ items **with replacement** from the observed sample of size $n$, so an item may appear twice or not at all; (2) the statistic is recomputed on every resample, and their spread is the **bootstrap distribution** $\hat\theta^*$; (3) the **percentile** interval is the $\alpha/2$ and $1-\alpha/2$ quantiles of that distribution,
> $$\text{CI}_{1-\alpha} = \Big[\,Q_{\alpha/2}\big(\hat\theta^*\big),\ Q_{1-\alpha/2}\big(\hat\theta^*\big)\,\Big]$$
> where $Q_q$ is the smallest attainable value the bootstrap distribution reaches with probability at least $q$, and $\alpha = 0.05$ for a 95% interval. The whole trick is that the sample you have stands in for the population you do not.
> **Example.** E1c's pilot, derived below: $[0.70,\ 1.00]$.
> **Non-example.** Ten successes out of ten. Every resample of an all-success sample is all successes, so the bootstrap distribution is the single point $1.00$ and the "95% interval" is $[1.00,\ 1.00]$ — certainty claimed from ten trials. A bootstrap can never reach outside the range of the data it was handed, so it fails hardest exactly where the data are thinnest.
> **Why it matters.** Robotics papers quote bootstrap intervals over tens of rollouts. Knowing that the ends of such an interval are attainable sample values, and that its granularity is $1/n$, is what stops you reading $[0.70,\ 1.00]$ as a measurement rather than as an admission of ignorance.

For a **binary** outcome the bootstrap needs no simulation at all, and it is worth doing by hand once. Drawing one item from E1c's ten pilot trials returns a success with probability $\hat p = 9/10$, and the $n$ draws are independent, so resampling with replacement *is* sampling from a Bernoulli with parameter $\hat p$ and the bootstrap distribution is exactly binomial:

$$\Pr\Big[\hat p^* = \frac{x}{n}\Big] = \binom{n}{x}\,\hat p^{\,x}\,(1-\hat p)^{\,n-x}$$

because $x$, the number of successes in one resample, counts $n$ independent draws each succeeding with probability $\hat p$. With $n = 10$ and $\hat p = 0.9$:

| $x$ | $\hat p^* = x/10$ | $\Pr[\hat p^* = x/10]$ | cumulative |
|---:|---:|---:|---:|
| $\le 5$ | $\le 0.5$ | 0.0016 | 0.0016 |
| 6 | 0.6 | 0.0112 | 0.0128 |
| 7 | 0.7 | 0.0574 | 0.0702 |
| 8 | 0.8 | 0.1937 | 0.2639 |
| 9 | 0.9 | 0.3874 | 0.6513 |
| 10 | 1.0 | 0.3487 | 1.0000 |

The 2.5% quantile is the smallest value whose cumulative probability reaches $0.025$, which is $x = 7$ at $0.0702$, and the 97.5% quantile is $x = 10$. The percentile bootstrap 95% interval for the pilot is therefore $[0.70,\ 1.00]$, and three properties of it are the lesson.

It is **discrete**. Only multiples of $0.1$ are attainable with ten trials, so no interval can land on 95%: this one actually carries $1 - 0.0128 = 98.7\%$ of the bootstrap distribution, and dropping $x = 7$ from it would leave $92.98\%$. It is **bounded by the data**: the upper end is $1.00$ because no resample can beat the best you saw, and $0.9^{10} = 0.349$ of all resamples miss the single failure entirely. And it is **not** the other two intervals. The normal approximation on the same counts, $\hat p$ plus or minus $1.96$ binomial standard errors (the SE of §3's success rate, the $1.96$ of §4), is $0.9 \pm 1.96\sqrt{0.9 \times 0.1/10} = 0.9 \pm 0.186 = [0.714,\ 1.086]$, which runs off the end of the axis.

The **Wilson** (score) interval turns the question around. It keeps every true $p$ whose own standard error makes 9 of 10 unsurprising, $\lvert\hat p-p\rvert\le z\sqrt{p(1-p)/n}$ with $z=1.96$, and solving that inequality — a quadratic in $p$ — gives its two ends,
$$p_{\pm}=\frac{\hat p+\frac{z^2}{2n}}{1+\frac{z^2}{n}}\ \pm\ \frac{z}{1+\frac{z^2}{n}}\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}$$
so at $n=10$ its centre is $1.092/1.384=0.789$, pulled from $0.9$ toward $\tfrac12$, and its half-width is $1.416\times0.1364=0.193$: $[0.596,\ 0.982]$, inside $[0,1]$ and far wider at the bottom. It can never leave $[0,1]$, because the standard error it tests with is computed at the candidate $p$ and shrinks to zero at $p=0$ and $p=1$, so no candidate beyond either end can look plausible. It asks which true $p$ could plausibly have produced 9 of 10, not which resamples of those 10 are plausible.

**Report the counts.** "90%" and "9/10" are the same estimate with completely different uncertainty, and only the second lets a reader recompute any of this.

**5. One seed or four? The same experiment, two claims.** E1c's seed record holds four runs per method, so the published pair is one row of a table with three more rows behind it. Using the sample standard deviation and standard error of §4, ours at 84, 88, 80, 76% gives $\bar x_A = 82.0$ and $s_A = 5.16$; the prior method at 72, 76, 80, 84% gives $\bar x_B = 78.0$ and $s_B = 5.16$; each has $\text{SE} = 5.16/\sqrt4 = 2.58$ points. The difference of the means is **4.0** points, not 16. An interval on a *difference* needs the two standard errors combined, which for equal group sizes $n$ is

$$\big(\bar x_A - \bar x_B\big) \pm t_{0.975,\,2n-2}\; s_p \sqrt{\tfrac1n + \tfrac1n}, \qquad s_p^2 = \frac{(n-1)s_A^2 + (n-1)s_B^2}{2n-2}$$

and three steps give it. First, independent errors add in variance even when the means are subtracted: if both methods share one run-to-run variance $\sigma^2$, then $\operatorname{Var}(\bar x_A-\bar x_B)=\sigma^2/n+\sigma^2/n=\sigma^2\big(\tfrac1n+\tfrac1n\big)$, so the spread of a difference is larger than either alone. Second, the shared $\sigma^2$ is estimated by pooling. §4's $s^2$ divides by $n-1$ so that its average over repeated experiments is exactly $\sigma^2$, which means each group's sum of squared deviations, $(n-1)s^2$, averages $(n-1)\sigma^2$; adding the two sums and dividing by the total $2n-2$ therefore averages $\sigma^2$ too. That is $s_p^2$, and it is why each variance is weighted by its degrees of freedom (with equal $n$, simply the mean of $s_A^2$ and $s_B^2$). Third, each group spends one degree of freedom on its own mean, so for Gaussian run-to-run noise the difference divided by its estimated standard error follows a Student $t$ with $2n-2$ degrees of freedom (§4), hence $t_{0.975,\,2n-2}$. When the two variances clearly differ, Welch's version ([[02-foundations/probability|3. Probability §6]]) drops the pooling. Here $s_A = s_B$ makes $s_p = 5.16$, the standard error of the difference is $5.16\sqrt{0.5} = 3.65$ points, $t_{0.975,\,6} = 2.447$, and

$$4.0 \pm 2.447 \times 3.65 = 4.0 \pm 8.9 = [-4.9,\ 12.9]$$

so the interval contains zero and four seeds per method cannot separate the two. Nothing was faked to get the headline: $88 - 72 = 16$ is the best seed of one method against the worst seed of the other, and both numbers sit in the same honest record. **A single-seed gap is a statistic of the seeds you chose to print.** The same eight runs support "a 16-point gain" and "a 4-point difference indistinguishable from none", and the only thing that decides which sentence a reader gets is whether the counts and the seed count were printed.

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="four seeds per method: ours at 84, 88, 80 and 76 percent with mean 82, the prior method at 72, 76, 80 and 84 with mean 78; the published pair is 88 against 72, a 16-point gap, while the difference of the means is 4.0 with a 95 percent interval from -4.9 to 12.9, which contains zero">
  <line x1="150.0" y1="128.0" x2="530.0" y2="128.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="150.0" y1="128.0" x2="150.0" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="184.5" y1="128.0" x2="184.5" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="219.1" y1="128.0" x2="219.1" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="253.6" y1="128.0" x2="253.6" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="288.2" y1="128.0" x2="288.2" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="322.7" y1="128.0" x2="322.7" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="357.3" y1="128.0" x2="357.3" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="391.8" y1="128.0" x2="391.8" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="426.4" y1="128.0" x2="426.4" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="460.9" y1="128.0" x2="460.9" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="495.5" y1="128.0" x2="495.5" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="530.0" y1="128.0" x2="530.0" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="184.5" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">72</text>
  <text x="253.6" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">76</text>
  <text x="322.7" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">80</text>
  <text x="391.8" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">84</text>
  <text x="460.9" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">88</text>
  <text x="530.0" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">92</text>
  <text x="340.0" y="158.0" font-size="12" fill="currentColor" text-anchor="middle">success over 25 episodes (%)</text>
  <text x="138.0" y="48.0" font-size="12" fill="currentColor" text-anchor="end">ours</text>
  <line x1="150.0" y1="44.0" x2="530.0" y2="44.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <circle cx="391.8" cy="44.0" r="5" fill="currentColor"/>
  <circle cx="460.9" cy="44.0" r="5" fill="currentColor"/>
  <circle cx="322.7" cy="44.0" r="5" fill="currentColor"/>
  <circle cx="253.6" cy="44.0" r="5" fill="currentColor"/>
  <line x1="357.3" y1="31.0" x2="357.3" y2="57.0" stroke="currentColor" stroke-width="2"/>
  <text x="357.3" y="27.0" font-size="11" fill="currentColor" text-anchor="middle">mean 82.0</text>
  <text x="138.0" y="96.0" font-size="12" fill="currentColor" text-anchor="end">prior method</text>
  <line x1="150.0" y1="92.0" x2="530.0" y2="92.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <circle cx="184.5" cy="92.0" r="5" fill="currentColor"/>
  <circle cx="253.6" cy="92.0" r="5" fill="currentColor"/>
  <circle cx="322.7" cy="92.0" r="5" fill="currentColor"/>
  <circle cx="391.8" cy="92.0" r="5" fill="currentColor"/>
  <line x1="288.2" y1="79.0" x2="288.2" y2="105.0" stroke="currentColor" stroke-width="2"/>
  <text x="288.2" y="75.0" font-size="11" fill="currentColor" text-anchor="middle">mean 78.0</text>
  <circle cx="460.9" cy="44.0" r="10" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3 2"/>
  <circle cx="184.5" cy="92.0" r="10" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3 2"/>
  <text x="548" y="70" font-size="11" fill="currentColor" text-anchor="end">published: 88 vs 72</text>
  <line x1="150.0" y1="214.0" x2="530.0" y2="214.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="150.0" y1="214.0" x2="150.0" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="150.0" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">−10</text>
  <line x1="213.3" y1="214.0" x2="213.3" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="213.3" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">−5</text>
  <line x1="276.7" y1="214.0" x2="276.7" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="276.7" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <line x1="340.0" y1="214.0" x2="340.0" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="340.0" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">5</text>
  <line x1="403.3" y1="214.0" x2="403.3" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="403.3" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">10</text>
  <line x1="466.7" y1="214.0" x2="466.7" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="466.7" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">15</text>
  <line x1="530.0" y1="214.0" x2="530.0" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="530.0" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">20</text>
  <line x1="276.7" y1="195.0" x2="276.7" y2="214.0" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="138.0" y="198.0" font-size="12" fill="currentColor" text-anchor="end">difference</text>
  <text x="138.0" y="212.0" font-size="12" fill="currentColor" text-anchor="end">of means (pts)</text>
  <line x1="214.2" y1="202.0" x2="440.5" y2="202.0" stroke="currentColor" stroke-width="2.4"/>
  <line x1="214.2" y1="197.0" x2="214.2" y2="207.0" stroke="currentColor" stroke-width="1.6"/>
  <line x1="440.5" y1="197.0" x2="440.5" y2="207.0" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="327.3" cy="202.0" r="4" fill="currentColor"/>
  <text x="214.2" y="192.0" font-size="11" fill="currentColor">4.0 ± 8.9 = [−4.9, 12.9]: contains 0</text>
  <path d="M479.3 196.0 L485.3 202.0 L479.3 208.0 L473.3 202.0 Z" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="479.3" y="192.0" font-size="11" fill="currentColor" text-anchor="middle">16: published</text>
</svg>

E1c's seed record: four seeds per method under one matched recipe. The published pair, our best seed at $88\%$ against the prior method's worst at $72\%$, makes a 16-point gap, while the means are $82.0\%$ and $78.0\%$ and the 95% interval on their difference, $[-4.9,\ 12.9]$ points, contains zero.

### 5. Evaluation pitfalls to watch for in papers

A results table can be arithmetically right and still mislead: the runs shown were picked, the comparison ran in an easier regime, or the method was handed information a deployment will not have. Each trap below is named with E1's own numbers, so that you can recognise it in a paper.

- **Cherry-picking**: qualitative figures show the best runs — ask what the *median* rollout looks like. E1c is the arithmetic of it: the published $0.88$ is the best of four seeds and the median seed is $0.82$, so the headline is a maximum wearing the clothes of an average.
- **Statistical vs practical significance**: error-bar overlap alone does not settle significance — check what the bars represent (std? standard error? CI?), the number of runs, and pairedness. A +0.3%p gain may be noise or may matter (on a saturated benchmark); +5%p from one seed can be luck. Ask for variance first — E1c's own numbers are 16 points on one seed and $4.0 \pm 8.9$ points on four.
  - The two are different questions. **Statistical significance** asks whether the observed difference would be unlikely if the true difference were zero — a p-value below a stated level such as 0.05 ([[02-foundations/probability|3. Probability §6]]). **Practical significance** asks whether the difference is large enough to matter for the task, judged by the effect size and its CI against a threshold fixed in advance. The first tends toward "yes" as $n$ grows, even for a negligible effect; the second does not change with $n$, which is why a paper needs both. Effect size and power, the two numbers that turn a practical threshold into a number of trials, are defined and worked on RS1 in the worked case of [[06-research-practice/experimental-design-reproducibility|2. Experimental Design]].
- **Oracle information**: does the method quietly use ground-truth state, perfect calibration, or human resets that deployment won't have? E1a's ground truth is one — the row of 60 "really cracked" panels: somebody opened a wall to produce it, and the detector will never have that row on site.
- **Open-loop vs closed-loop evaluation**: predicting a good trajectory offline (open-loop) is far easier than executing under feedback with compounding errors (closed-loop) — robotics numbers are only comparable within the same regime. E1a and E1c's pilot are the two regimes of one system — 1,000 stored images scored, against 10 panels a robot actually drove to — and no arithmetic turns the first number into the second.
  - *Defined by where the input states come from.* **Open-loop** evaluation feeds the policy $\pi$ the states of a recorded dataset and scores its outputs against the recorded actions, for example $\frac{1}{N}\sum_{i=1}^{N} \lVert \pi(o_i) - a_i \rVert$ over $N$ logged pairs $(o_i, a_i)$, so the policy's mistakes never change what it sees next. **Closed-loop** evaluation executes $\pi$'s actions, so the next observation is produced by those actions, and it scores the outcome (success rate over rollouts). A low open-loop error does not imply closed-loop success, because in closed loop small errors move the policy into states the dataset never contained — covariate shift ([[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §1]]).
- **Episode definition**: "success rate" depends on time limits, reset conditions, and what counts as success — two papers' 80% can mean different things. E1c's $9/10$ is undefined until that sentence is written: flagged and reached? flagged, reached and photographed inside the time limit? The bootstrap in the worked case is exact arithmetic on a number this definition has to fix first.
- **Benchmark saturation**: near-ceiling benchmarks reward overfitting to quirks; gains there generalize least. E1a's 97% accuracy is that ceiling by construction, since 94% of it comes free from answering "fine".

### 6. The training recipe, as vocabulary

An experimental section spends a paragraph on how the model was trained, in terms this wiki's
optimization page does not name. You are not reproducing the run — but these decide whether a
reported number is a property of the *method* or of the *recipe*, and an ablation that changes
one of them is not comparing what it claims. Running such a recipe on a shared cluster — the batch job, its chain of restarts, the checkpoint and how often to write it — is [[02-foundations/tools/gpu-clusters|12.7 GPU Clusters §4–§7]].

| Term | What it is | Why it appears in the claim |
|---|---|---|
| **Learning-rate schedule** | the step size varies over training — often a linear **warmup**, then **cosine decay**; the configured minimum may be zero or nonzero | the final learning rate moves the last points of accuracy, so "same architecture, different schedule" is not a fair comparison. Why a schedule warms up at all, and how its peak moves with the batch size, is [[03-deep-learning/foundations/training-at-scale\|1.3 Training at Scale §9]] |
| **Weight decay / AdamW** | AdamW shrinks weights directly, $w \leftarrow w(1-\eta\lambda)$, *decoupled* from the adaptive step — it is not an L2 term in the loss at all | the Gaussian-prior reading in [[02-foundations/probability\|3. Probability §4]] is an L2 penalty, and that equals weight decay **for SGD**. Under Adam the adaptive denominator distorts it per-coordinate, which is the whole reason AdamW exists; the update is worked through in [[02-foundations/optimization\|4. Optimization §3]] |
| **Gradient accumulation** | average gradients over several forward passes before one optimizer step | a paper's "batch size 4096" may be 8 × 512 accumulated, which matches a true batch of 4,096 only when the loss is a sum over examples and the optimizer step is the same — check the loss and the implementation; the contrastive-loss exception is in the *Deeper* note below |
| **Mixed precision** (fp16/bf16) | compute in 16 bits with an fp32 master copy of the weights. **fp16 additionally needs loss scaling**; **bf16 does not** | halves activation memory and raises throughput, so a claim that a model fits or trains faster should name its precision; what 16 bits do not shrink, and why bf16 needs no loss scaling, are in the *Deeper* note below |
| **EMA of weights** | keep a slowly-moving average of the parameters and *evaluate that*, not the live weights | a free fraction of a point on many benchmarks. Diffusion papers use it almost universally (DDPM: decay 0.9999, an appendix figure); policy papers vary and often only the **code** reveals it — Diffusion Policy uses it in its configs without mentioning it in the paper. Distinct from the EMA *teacher* of [[01-canonical-papers/notes/2-computer-vision/dino\|DINO]], which is a target network, not an evaluation trick |
| **Initialization** | Xavier/He scaling keeps activation variance stable across depth | rarely load-bearing now that normalization layers exist, but named when a paper trains without them. Where each scale comes from, a per-layer variance factor held at one, is [[03-deep-learning/foundations/training-at-scale\|1.3 Training at Scale §1]] |

**The two-row table the abstract will quote.** These are E1c's published rows, reprinted here where the recipe vocabulary is:

| Method | Success | Trials | Training |
|---|---:|---:|---|
| Ours | 0.88 | 25 | new schedule, one seed |
| Prior SOTA | 0.72 | 25 | new schedule, one seed |

The 16-point gap is the claim. It silently depends on $n=25$ and on one seed per method. The *Training* column passes the check of the warning below — both rows ran the new schedule, so this gap is no recipe mismatch — and still the gap does not survive: E1c holds the other three seeds of each method under that same recipe, and four seeds each leave $4.0 \pm 8.9$ points, an interval containing zero, so twelve of the sixteen points were the choice of seed rather than the method. Had the prior method kept its 2021 recipe, a recipe gap would hide inside the same sixteen points, and only retraining it on the new schedule would expose it. Separately $22/25$ vs $18/25$ is a thin binomial.

> [!note]- Deeper · 더 깊이
> **The recipe terms, with their formulas, and the details behind the table.**
>
> **Warmup and cosine decay.** A learning-rate schedule is a function $\eta_t$ of the step $t$. Linear warmup over the first $T_w$ steps, then cosine decay from $\eta_{\max}$ to $\eta_{\min}$ by the last step $T$:
> $$\eta_t = \eta_{\max}\,\frac{t}{T_w} \ \ (t \le T_w), \qquad \eta_t = \eta_{\min} + \tfrac12\big(\eta_{\max} - \eta_{\min}\big)\Big(1 + \cos\frac{\pi\,(t - T_w)}{T - T_w}\Big) \ \ (t > T_w)$$
> so the rate climbs from 0, then follows half a cosine down to $\eta_{\min}$. With no warmup, $\eta_{\max} = 10^{-3}$, $\eta_{\min} = 0$ and $T = 10{,}000$, the rate is $8.54 \times 10^{-4}$ at step 2,500, $5 \times 10^{-4}$ at step 5,000 and $0$ at the end; a 1,000-step warmup is at $2.5 \times 10^{-4}$ on step 250. Warmup can stabilize Adam's early second-moment estimate (its running average of squared gradients, [[02-foundations/optimization|4. Optimization §3]]) and large-batch training, and specific post-norm recipes (LayerNorm placed after each residual sublayer, [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]) can fail without it.
>
> **Weight decay (AdamW form).** Every step multiplies each weight by $(1 - \eta\lambda)$ *in addition to* the adaptive gradient step, rather than adding $\lambda w$ to the gradient before Adam rescales it. The two coincide only for plain SGD, since SGD applies no per-coordinate rescaling; §2 has the arithmetic, [[02-foundations/optimization|4. Optimization §3]] the full update.
>
> **Gradient accumulation.** Split a batch of $B = KB_\mu$ examples into $K$ microbatches of $B_\mu$, compute each microbatch's mean gradient $g_k$, and step once with
> $$g = \frac{1}{K}\sum_{k=1}^{K} g_k$$
> which equals the full-batch mean gradient because the microbatches are the same size and the loss is a sum over examples. $8 \times 512$ is a nominal batch of 4,096. **Non-example:** a contrastive loss is *not* a sum over examples — each example's term depends on the others in its batch, the negatives that a loss such as [[01-canonical-papers/notes/3-vlm/clip|CLIP]]'s must score as non-matches — so accumulation gives 511 negatives per example, not 4,095, unless features are gathered across microbatches. Batch statistics and stochastic operations need not match either.
>
> **Mixed precision.** 16-bit formats trade range for memory. fp16's largest value is 65,504 and its smallest positive value about $6 \times 10^{-8}$; bf16 keeps fp32's 8 exponent bits, so its range reaches about $3.4 \times 10^{38}$, with coarser mantissa precision — which is exactly why bf16 drops loss scaling and why large models train stably in 16 bits. **Loss scaling** multiplies the loss by a factor $S$ before the backward pass and divides the gradients by $S$ before the update, so small gradients survive fp16. A gradient of $10^{-8}$ becomes $0$ in fp16, while $S = 1024$ lifts it to about $1.02 \times 10^{-5}$, which fp16 represents. What 16 bits do not shrink are the per-parameter model states: under Adam they stay at 16 bytes per parameter, 2 + 2 + 4 + 4 + 4 for 16-bit weights and gradients, the fp32 master copy and Adam's two moments, as fp32 Adam's 4 + 4 + 4 + 4 does ([[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §4–§5]]).
>
> **EMA of weights.** A second copy $\bar\theta$ updated after every optimizer step:
> $$\bar\theta_t = \beta\,\bar\theta_{t-1} + (1 - \beta)\,\theta_t$$
> so $\bar\theta$ averages roughly the last $1/(1-\beta)$ steps, with older weights discounted geometrically. At DDPM's $\beta = 0.9999$ that window is 10,000 steps, and a weight's influence halves after about 6,931 steps; the averaged copy is the one evaluated and released.
>
> **Initialization.** Draw each weight with zero mean and a variance set by the layer's fan-in $n_{\text{in}}$ and fan-out $n_{\text{out}}$, so activation variance neither explodes nor vanishes with depth: Xavier (for tanh-like activations) uses $\operatorname{Var}(w) = 2/(n_{\text{in}} + n_{\text{out}})$, and He (for ReLU, which zeroes half its inputs) uses $\operatorname{Var}(w) = 2/n_{\text{in}}$. A ReLU layer with $n_{\text{in}} = 512$ gets standard deviation $\sqrt{2/512} = 0.0625$.

> [!warning] Recipe differences masquerading as method differences
> The most common unfair comparison in this literature is a new method trained with a modern
> recipe against a baseline reproduced with the original one. **Check that the baseline's
> schedule, optimizer, precision and epoch budget match the proposed method's** before
> believing a margin — and note that when they do match, the honest papers say so explicitly.

> [!tip] Going deeper · 더 깊이
> This page is the reading half; the doing half is [[06-research-practice/experimental-design-reproducibility|Experimental Design & Reproducibility]], which is where the same ideas become choices you have to make. For the statistics underneath, Murphy's free [*Probabilistic Machine Learning: An Introduction*](https://probml.github.io/pml-book/book1.html) ch.4–6.

### Self-check

1. A model picks its best checkpoint by test accuracy. What went wrong, and in which
   direction is the reported number biased?
2. Precision 0.9 / recall 0.3 crack detector: what does it miss, and when is that
   acceptable on a construction site?
3. Why is FID computed on *features* (embeddings from Inception, an image-classification CNN) instead of pixels?
4. In a VLA paper, "76% success on unseen instructions" — list three questions you'd ask
   before believing it matters.
5. E1b's precision at the deployed threshold is $0.75$. Why is it wrong to read that as an
   estimate of the detector's precision on site, and which number computed on E1b *is*
   trustworthy?

> [!tip]- Answers
> 1. The test set was used as a validation set — the reported number is biased upward (optimistic); true generalization is lower.
> 2. It misses 70% of real cracks (recall 0.3). It is unacceptable as a first-pass screen or as the sole safety gate, because anything it does not flag never reaches inspection. It is acceptable only as a prioritisation aid on top of an inspection regime that still covers every panel: its flags are trustworthy (precision 0.9), so they can be fast-tracked while misses are caught by the regular inspection.
> 3. Pixel distance ignores perceptual quality (a one-pixel shift is punished heavily) — Inception feature space reflects semantic similarity, so distribution distance is measured there.
> 4. ① How many trials, with what variance? ② What does "unseen" mean (new objects? new instructions? new scenes?) ③ Against which baseline, and is there failure analysis?
> 5. E1b was chosen to span the score range, so 3 of its 7 panels are cracked — a 43% base rate against the site's 6%. Precision conditions on a positive *prediction*, so it moves with the base rate (worked case, part 3) and the $0.75$ describes the slice and nothing else. The AUC of $0.917$ is the trustworthy one: it depends only on how the scores of the cracked panels are ordered against the scores of the sound ones, and mixing the two groups in any proportion leaves that ordering alone.

### Problem set · 과제

Tier B. Hand derivation on **E1**, using only this page, its prerequisites and the object frozen above. A different threshold, a different base rate and a longer pilot than the worked case.

1. **Draw.** From E1b's seven scores, draw the $2\times2$ confusion matrix at threshold $\tau = 0.65$ and again at $\tau = 0.45$, and put both operating points on the ROC axes. Label each point with its precision. What does the step between the two points tell you about the panels scoring between $0.45$ and $0.65$?
2. **Derive.** Take the $\tau = 0.65$ point, unchanged, to a site where 1% of panels are cracked, and compute its precision over 1,000 panels. Then, holding TPR fixed, find the FPR that would give precision $0.5$ at that base rate, and state by what factor the detector must improve.
3. **Interpret.** Suppose E1c's site pilot runs on 10 more panels and ends at 18 successes out of 20, so $\hat p$ is still $0.9$. (a) Read the new percentile bootstrap off the binomial, as the worked case did for 10 trials. Which end of $[0.70,\ 1.00]$ moved, which did not, and why? (b) Recompute the normal-approximation and Wilson intervals at $n=20$. A referee asks for "the success rate with error bars": which of §4's three quantities, and which of the three intervals, should the pilot's row carry — and what else must be printed beside it before a reader can check your answer?

> [!note]- How to draw it · 그리는 법
> - One $2\times2$ box per threshold, columns labelled by the *prediction* and rows by the *truth*; a panel is flagged when its score reaches $\tau$, and the four cells together must hold all seven of E1b's panels.
> - Ring the column precision divides by and the row recall divides by in two different styles; TP is the cell where the two rings cross.
> - Shade TN and write beside it that neither ratio uses this cell.
> - ROC axes: FPR across, TPR up, both from 0 to 1, with the chance diagonal; put both operating points on the same axes and write each one's precision beside it.
> - Precision is not a coordinate of the ROC plot: move a point to another base rate and it stays put while its precision changes. The worked case writes $0.27$ under $0.80$ for its point, and item 2 does the same for the $\tau=0.65$ point.
> - The interval strip does not depend on $\tau$. If you redraw it for item 3, take a horizontal axis from 0 to 1, mark $\hat p=0.9$, stack the normal-approximation, Wilson and percentile-bootstrap intervals for 18 of 20 above it with the picture's ten-trial ones faint beside them, and mark where the normal approximation still leaves the axis.
> - A correct strip answers the question part 4 of the worked case turns on: which of the three intervals may be printed under a success rate from a few trials.

> [!tip]- Solutions
> 1. At $\tau = 0.65$ the flags are the cracked $0.90$ and $0.80$ plus the sound $0.70$: $TP = 2$, $FN = 1$, $FP = 1$, $TN = 3$, so precision $2/3 = 0.667$, recall $2/3 = 0.667$, and the point is $(\text{FPR},\ \text{TPR}) = (0.25,\ 0.667)$. At $\tau = 0.45$ the cracked $0.60$ and the sound $0.50$ join them: $TP = 3$, $FN = 0$, $FP = 2$, $TN = 2$, precision $3/5 = 0.600$, recall $1.000$, point $(0.50,\ 1.00)$. Exactly one cracked panel and one sound panel score inside $[0.45,\ 0.65)$, so crossing that band buys the last crack at the price of one more false alarm — recall $0.667 \to 1.000$ while FPR $0.25 \to 0.50$ — and precision *falls* while recall rises, which is the trade-off the worked case names, drawn on seven panels.
> 2. At 1% of 1,000 panels there are 10 cracked and 990 sound. Holding the point fixed, $TP = 0.667 \times 10 = 6.67$ and $FP = 0.25 \times 990 = 247.5$, so precision $= 6.67/254.17 = 0.026$ — a factor of 25 below the $0.667$ computed on E1b, where 3 of 7 panels were cracked. For precision $0.5$ the false alarms must fall to $FP = TP = 6.67$, that is $\text{FPR} = 6.67/990 = 0.0067$: the false-positive rate has to improve by a factor of 37 with recall held. That factor is the concrete content of "ask for precision at a stated recall, on the deployment base rate."
> 3. (a) With $n=20$ and $\hat p=0.9$ the bootstrap distribution is binomial again. Its cumulative probability is $0.0113$ at $x=14$ and $0.0432$ at $x=15$, so the 2.5% quantile is $x=15$, $\hat p^*=0.75$, and the 97.5% quantile is still $x=20$: the interval is $[0.75,\ 1.00]$. The lower end moved up one step of the new, finer $1/20$ grid. The upper end cannot move: every resample that misses both failures scores $1.00$, and that is $0.9^{20}=0.122$ of them, far more than the $2.5\%$ the upper quantile may cut off. More trials at the same $\hat p$ narrow a percentile bootstrap from below only, and its top stays at $1.00$ as long as $\hat p^{\,n}$, the share of all-success resamples, exceeds $0.025$. (b) Normal approximation: $\text{SE}=\sqrt{0.9\times0.1/20}=0.067$, so $0.9\pm0.131=[0.769,\ 1.031]$, still off the axis. Wilson: centre $0.996/1.192=0.836$ and half-width $1.644\times0.0831=0.137$, so $[0.699,\ 0.972]$, about $1/\sqrt2$ of the ten-trial width ($0.273$ against $0.386$). Not $s$ and not SE — those describe scatter across *runs*, and the pilot is one run of 20 Bernoulli trials, so there is no run-to-run spread to report. The row should carry Wilson $[0.699,\ 0.972]$: the bootstrap cannot see above its own data and the normal approximation leaves the axis. Beside it must appear $k$ and $n$ — "18/20", not "90%" — and the episode definition of §5, because without those two the interval cannot be recomputed or even interpreted.

### From reading experiments to designing them

Continue with [[06-research-practice/index|Research Practice]] for research questions, controlled robot experiments, failure diagnosis, reproducibility, and peer review.

The transition matters because recognizing an unfair comparison after publication is easier than preventing one before collection. For example, turn a concern about shared scenes into a site-level split, and a concern about hidden resets into a declared intervention rule. **The reading this gives you.** Carry one concrete uncertainty into the research-practice pages and design the record that would answer it. The next step is an experiment whose outcome could change your claim.

### Sources

- E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association* 22(158):209–212 (1927) — the score interval of the worked case's part 4, as the wiki's [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]] also cites it.
- K. P. Murphy, [*Probabilistic Machine Learning: An Introduction*](https://probml.github.io/pml-book/book1.html) (MIT Press, 2022), ch.4–6 — the statistics under §2–§5.
- The papers named in §1, §2 and §6 are read in the wiki's own notes: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/3-vlm/clip|CLIP]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]], [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/vgg|VGG]], [[01-canonical-papers/notes/1-foundations/scaling-laws|scaling laws]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] and [[01-canonical-papers/notes/2-computer-vision/dino|DINO]].
- E1 is a teaching object: its counts and scores were invented for this page, and every number derived from them was computed here.

## 한국어

*[[02-foundations/neural-network-basics|0.8]]과 [[02-foundations/probability|3. 확률]] 위에 선다. 앞의 페이지들이 방법을 읽는 도구였다면,
이 페이지는 그 방법이 통했다는 주장을 읽는 도구다. 어떤 결과 표든 읽기 전에 읽어라.*

모든 논문이 전제하는 장인적 지식: 모델을 어떻게 학습·검증하고, 무엇보다 어떻게 *재는가*.
이 페이지는 위키의 모든 "Results" 표를 읽는 해독기다.

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 마지막 층인 작업 완료, 곧 어떤 층이 나아졌다는 것을 누구든 어떻게 아는가 밑에 깔린 수학 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 있다). "*저 패널을 프레임에 설치해*"에서는 마지막 단계인 *완료 검증*을 받친다. 패널이 제자리에 앉았는지 로봇이 확인하는 일과, 논문의 시스템이 정말 패널을 앉히는지 내가 확인하는 일 둘 다다. 이것 없이는 표가 저자들이 바라는 대로 읽힌다. 이 페이지의 균열 감지기 E1은 정확도 $97\%$를 내지만 언제나 "정상"이라고만 답해도 $94\%$가 나오고, 더 잘 지은 현장으로 가면 정밀도가 $0.80$에서 $0.27$로 떨어지며, 16포인트 향상은 알고 보면 한쪽의 최고 시드와 다른 쪽의 최저 시드를 맞붙인 것이어서 시드 넷으로 보면 $4.0\pm8.9$포인트로 줄어든다. 뒤 페이지들은 이 페이지를 절 단위로 가져다 쓴다. [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성]]은 이 페이지의 §1, §4, §5를 설계의 선택으로 바꾸고, [[04-robotics/system-identification|5.5 시스템 식별]]은 §1–§2를, [[04-robotics/state-estimation-slam|3. 상태 추정]]과 [[04-robotics/tactile-visuotactile|14. 촉각 센싱]]은 §3의 지표를 쓰며, [[05-construction-robotics/imitating-contact|10. 접촉 모방]]은 학습된 정책이 패널을 앉히는 시행을 §1과 §5에 따라 보고한다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 1 [[02-foundations/overview#통과 점검 — 기초는 끝났는가|기초 통과 점검]]의 14번 문제가 이 페이지를 검사하고, 블록 5에서는 연구 실무 2의 시행 설계와 Wilson 구간을 읽는 쪽 절반이 된다. 이 페이지를 마치면 표의 개수에서 정밀도, 재현율, AUC, 구간을 다시 계산하고, 표의 격차를 믿기 전에 표가 무엇을 밝혀야 하는지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 세 번쯤 든다. **첫 회차:** 이 페이지의 대상과 그림, §1, 그리고 계산 예제가 필요로 하는 두 조각인 §3 사전 끝 무렵의 *성공률* 항목과, 시드를 다루는 §4의 셋째 항목(세 양 $s$, SE, $t$ 구간)을 읽는다. **둘째 회차:** §4 뒤 계산 예제의 1–4번, 곧 세어서 만드는 네 지표, AUC, 기저율, 구간 셋을 모두 E1 위에서 푼다. **셋째 회차:** 시드 하나와 넷을 견주는 5번을 풀고, 그 대상을 잘못 읽는 방법들인 §5의 함정을 읽은 뒤, 과제 1번과 스스로 점검 1, 4, 5번을 푼다. §3의 나머지는 결과 표 옆에 펴 두는 사전이고, §2와 §6은 두 번째 읽기로, 쓰면서 몸에 붙는다.

### 이 페이지의 대상 · Running object

평가는 기계가 아니므로 [[02-foundations/lab-plants|0.6 Lab Plants]]의 *장치*(plant, 제어에서 제어 대상인 시스템을 부르는 말) 여섯, 곧 이 위키가 고정해 둔 예제 시스템 **P1**–**P6** 가운데 맞는 것이 없다. 가장 가까운 카탈로그 항목은 **P5**의 균열 감지기인데 모양이 다르다. P5는 *확률* — $P(+ \mid c) = 0.95$, $P(+ \mid \neg c) = 0.05$, $P(c) = 0.01$ — 로 규정되어 있고 그것은 베이즈 갱신에 필요한 것인 반면, 이 페이지의 모든 지표는 유한한 test 집합 위 **개수**의 비이고 그 유한성이 §4의 주제 전부다. 그래서 이 페이지는 자기 대상을 고정하고 이후로 숫자를 바꾸지 않는다. 그 안의 모든 숫자는 일부러 지어낸 것이다. 측정값이 아니라 교육용 대상이다.

**E1 — 균열 감지기 하나, 기록 셋.** 모델은 벽체 패널마다 $[0, 1]$의 점수를 매기고, 점수가 배포 문턱값 $\tau = 0.55$에 닿으면 그 패널을 *플래그*한다.

**E1a, 전수 감사.** 패널 1,000장, 그중 60장이 실제로 균열이다. $\tau = 0.55$에서 감지기는 50장을 플래그했고 그중 40장이 진짜다.

| | 균열로 예측 | 정상으로 예측 |
|---|---|---|
| **실제 균열** | TP = 40 | FN = 20 |
| **실제 정상** | FP = 10 | TN = 930 |

**E1b, 점수 조각.** 손으로 문턱값을 훑을 수 있도록 **점수 범위를 고루 덮게 고른** 패널 일곱 장 — 균열 셋, 정상 넷 — 과 문턱값을 대기 전에 기록한 원 점수다.

| 실제 | 균열 | 균열 | 균열 | 정상 | 정상 | 정상 | 정상 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 점수 | 0.90 | 0.80 | 0.60 | 0.70 | 0.50 | 0.40 | 0.20 |

E1b는 현장의 무작위 표본이 아니므로 여기서 계산한 어떤 비율도 배포 시의 비율을 추정하지 않는다. 순서와 문턱값 훑기를 위해 있을 뿐이고, 그 구분이 왜 말장난이 아닌지는 스스로 점검이 묻는다.

**E1c, 시행 기록.** 같은 시스템의 다른 두 실행이다. **현장 파일럿**: 로봇 점검기가 독립적인 패널 10장을 시도해 9장에 성공했다. 그리고 **시드 기록**: 이 방법과 비교 대상 방법을 각각 랜덤 시드 넷으로, 레시피를 맞춘 채 — 같은 스케줄, 같은 예산, 같은 25 에피소드 벤치마크 — 다시 학습시켜 25번 중 성공이 21, 22, 20, 19(우리)와 18, 19, 20, 21(기존 방법)이 나왔다. §6에 실린 두 행 표는 각각 시드 하나, 곧 우리 쪽의 최고 시드와 기존 방법의 최저 시드를 인용한 것이다. $22/25 = 0.88$ 대 $18/25 = 0.72$.

*범위: 이 페이지는 결과 표를 읽는 법을 가르친다. 각 지표가 무엇을 세고, 무엇을 감추고, 불확실성이 얼마나 넓은지다. 그 표를 만든 실험을 설계하는 법은 가르치지 않는다. 그것은 [[06-research-practice/experimental-design-reproducibility|실험 설계와 재현성]]이고, 구간 뒤에 있는 가설 검정은 [[02-foundations/probability|3. 확률 §6]]이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 426" style="max-width:100%;height:auto" role="img" aria-label="E1을 세 칸에: 문턱값 0.55의 혼동 행렬과 정밀도 열·재현율 행 테두리, 칠한 TN; FPR 0.011, TPR 0.667의 ROC 동작점과 정밀도 0.80, 균열 비율이 10분의 1이면 0.27; 10번 중 9번에 대한 정규근사·Wilson·부트스트랩 구간">
  <defs><marker id="aMlK" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">1 · 2×2 상자 (E1a, τ = 0.55)</text>
  <rect x="178" y="124" width="78" height="44" stroke="none" fill="currentColor" fill-opacity="0.16"/>
  <rect x="100" y="80" width="156" height="88" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <line x1="178" y1="80" x2="178" y2="168" stroke="currentColor" stroke-width="1.2"/>
  <line x1="100" y1="124" x2="256" y2="124" stroke="currentColor" stroke-width="1.2"/>
  <text x="139" y="46" font-size="11" fill="currentColor" text-anchor="middle">균열로</text>
  <text x="139" y="60" font-size="11" fill="currentColor" text-anchor="middle">예측</text>
  <text x="217" y="46" font-size="11" fill="currentColor" text-anchor="middle">정상으로</text>
  <text x="217" y="60" font-size="11" fill="currentColor" text-anchor="middle">예측</text>
  <text x="84" y="99" font-size="11" fill="currentColor" text-anchor="end">실제</text>
  <text x="84" y="113" font-size="11" fill="currentColor" text-anchor="end">균열</text>
  <text x="84" y="143" font-size="11" fill="currentColor" text-anchor="end">실제</text>
  <text x="84" y="157" font-size="11" fill="currentColor" text-anchor="end">정상</text>
  <text x="139" y="106" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">TP = 40</text>
  <text x="217" y="106" font-size="12" fill="currentColor" text-anchor="middle">FN = 20</text>
  <text x="139" y="150" font-size="12" fill="currentColor" text-anchor="middle">FP = 10</text>
  <text x="217" y="150" font-size="12" fill="currentColor" text-anchor="middle">TN = 930</text>
  <rect x="96" y="69" width="86" height="110" rx="7" stroke="currentColor" stroke-width="2.2" fill="none"/>
  <rect x="89" y="76" width="178" height="52" rx="7" stroke="currentColor" stroke-width="2.2" fill="none" stroke-dasharray="6 3"/>
  <text x="217" y="196" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">두 비 모두</text>
  <text x="217" y="210" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">이 칸을 안 쓴다</text>
  <line x1="217" y1="182" x2="217" y2="172" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" marker-end="url(#aMlK)"/>
  <line x1="14" y1="234" x2="40" y2="234" stroke="currentColor" stroke-width="2.2"/>
  <text x="46" y="238" font-size="11" fill="currentColor">정밀도 = 40/50 = 0.80: 열</text>
  <line x1="14" y1="250" x2="40" y2="250" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <text x="46" y="254" font-size="11" fill="currentColor">재현율 = 40/60 = 0.667: 행</text>
  <text x="316" y="20" font-size="12" fill="currentColor">2 · ROC 축과 점 하나</text>
  <line x1="346" y1="226" x2="526" y2="226" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <line x1="346" y1="226" x2="346" y2="46" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <line x1="346" y1="226" x2="346" y2="230" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="346" y="242" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <line x1="342" y1="226" x2="346" y2="226" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="339" y="230" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <line x1="436" y1="226" x2="436" y2="230" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="436" y="242" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="342" y1="136" x2="346" y2="136" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="339" y="140" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.5</text>
  <line x1="526" y1="226" x2="526" y2="230" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="526" y="242" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="342" y1="46" x2="346" y2="46" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="339" y="50" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">1</text>
  <text x="436" y="258" font-size="11" fill="currentColor" text-anchor="middle">FPR</text>
  <text x="339" y="38" font-size="11" fill="currentColor" text-anchor="end">TPR</text>
  <line x1="346" y1="226" x2="526" y2="46" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6" stroke-dasharray="4 4"/>
  <text x="490" y="107.2" font-size="11" fill="currentColor" fill-opacity="0.7">우연 수준</text>
  <circle cx="347.9" cy="106" r="4.5" stroke="none" fill="currentColor"/>
  <text x="357.9" y="50" font-size="11" fill="currentColor">정밀도 0.80</text>
  <text x="357.9" y="65" font-size="11" fill="currentColor" fill-opacity="0.85">균열 6%에서</text>
  <text x="357.9" y="84" font-size="11" fill="currentColor">0.27: 같은 점</text>
  <text x="357.9" y="99" font-size="11" fill="currentColor" fill-opacity="0.85">균열 0.6%에서</text>
  <text x="357.9" y="118" font-size="11" fill="currentColor" fill-opacity="0.85">(0.011, 0.667)</text>
  <text x="12" y="292" font-size="12" fill="currentColor">3 · 9/10에 대한 95% 구간 셋 (E1c 파일럿)</text>
  <line x1="64" y1="380" x2="448" y2="380" stroke="currentColor" stroke-width="1.3"/>
  <line x1="64" y1="380" x2="64" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="64" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <line x1="160" y1="380" x2="160" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="160" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.25</text>
  <line x1="256" y1="380" x2="256" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="256" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="352" y1="380" x2="352" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="352" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.75</text>
  <line x1="448" y1="380" x2="448" y2="385" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="448" y="398" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <line x1="409.6" y1="378" x2="409.6" y2="308" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="1 3"/>
  <line x1="448" y1="380" x2="448" y2="312" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="3 3"/>
  <line x1="338.2" y1="318" x2="448" y2="318" stroke="currentColor" stroke-width="2.4"/>
  <line x1="338.2" y1="313" x2="338.2" y2="323" stroke="currentColor" stroke-width="1.6"/>
  <line x1="448" y1="318" x2="481" y2="318" stroke="currentColor" stroke-width="2.4" stroke-dasharray="3 2"/>
  <line x1="481" y1="313" x2="481" y2="323" stroke="currentColor" stroke-width="1.6"/>
  <text x="330.2" y="322" font-size="11" fill="currentColor" text-anchor="end">정규근사 [0.714, 1.086]</text>
  <line x1="292.8" y1="338" x2="441.1" y2="338" stroke="currentColor" stroke-width="2.4"/>
  <line x1="292.8" y1="333" x2="292.8" y2="343" stroke="currentColor" stroke-width="1.6"/>
  <line x1="441.1" y1="333" x2="441.1" y2="343" stroke="currentColor" stroke-width="1.6"/>
  <text x="284.8" y="342" font-size="11" fill="currentColor" text-anchor="end">Wilson [0.596, 0.982]</text>
  <line x1="332.8" y1="358" x2="448" y2="358" stroke="currentColor" stroke-width="2.4"/>
  <line x1="332.8" y1="353" x2="332.8" y2="363" stroke="currentColor" stroke-width="1.6"/>
  <line x1="448" y1="353" x2="448" y2="363" stroke="currentColor" stroke-width="1.6"/>
  <text x="324.8" y="362" font-size="11" fill="currentColor" text-anchor="end">백분위 부트스트랩 [0.70, 1.00]</text>
  <circle cx="448" cy="318" r="3.6" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.0"/>
  <text x="548" y="305" font-size="11" fill="currentColor" text-anchor="end">1에서 축을 벗어난다</text>
  <text x="456" y="342" font-size="11" fill="currentColor" fill-opacity="0.85">[0, 1] 안</text>
  <text x="456" y="362" font-size="11" fill="currentColor" fill-opacity="0.85">1.00에서 막힘</text>
  <path d="M404.6 389 L409.6 382 L414.6 389 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="409.6" y="414" font-size="11" fill="currentColor" text-anchor="middle">p̂ = 0.9 (10번 중 9번)</text>
</svg>

E1을 세 칸에 그린 것으로, 첫 칸은 $\tau=0.55$에서 E1a의 혼동 행렬 — $TP=40$, $FN=20$, $FP=10$, $TN=930$ — 이며, 정밀도가 나누는 열($40/50=0.80$)과 재현율이 나누는 행($40/60=0.667$)에 테두리를 둘러 TP에서 만나게 하고 두 비 모두 쓰지 않는 TN은 칠했다. ROC 축(참양성률 대 거짓양성률, 계산 예제 2번에서 정의한다) 위에서 같은 감지기는 점 하나 $(\text{FPR},\ \text{TPR})=(0.011,\ 0.667)$이고, 그 정밀도는 균열 6%에서 $0.80$, 균열 0.6%에서 $0.27$이지만 점 자체는 움직이지 않는다. 구간 띠는 E1c 파일럿 10번 중 9번($\hat p=0.9$)에 대한 95% 구간 셋이고 셋 모두 계산 예제 4번에서 유도하며, 정규근사 $[0.714,\ 1.086]$은 $1$에서 축을 벗어나고 Wilson $[0.596,\ 0.982]$는 $[0,1]$ 안에 머물며 백분위 부트스트랩 $[0.70,\ 1.00]$은 $1.00$에서 잘린다.

### 1. 데이터 분할 — 단 하나의 신성한 규칙

모델을 만드는 데 쓰인 데이터로 잰 숫자는, 직접 쓰였든 그 데이터를 보면서 내린 선택을 통해 스며들었든, 새 패널에 대해 말해 주는 것이 적고 좋아 보이는 쪽으로 틀린다. 이 절은 test 숫자를 정직하게 지키는 규칙과, 그 규칙이 소리 없이 깨지는 방식들이다.

- **Train / validation / test**: train으로 적합하고, validation으로 하이퍼파라미터 튜닝과
  체크포인트 선택을 하고, test는 맨 끝에 **한 번만** 만진다. 결정이 test 성능의 영향을
  받는 순간 test는 조용히 validation이 되고 — 보고 수치는 부풀려진다.
  - *무엇인가:* 가진 데이터 $\mathcal{D}$를 각자 한 가지 일을 맡는 **서로소**인 부분집합 셋으로 나눈 분할이다. 폴더 세 개가 아니라 분할이 되게 하는 두 조건은 서로소성과 같은 분포다.
  $$\mathcal{D} = \mathcal{D}_{\text{tr}} \cup \mathcal{D}_{\text{val}} \cup \mathcal{D}_{\text{te}}, \qquad \mathcal{D}_{\text{tr}} \cap \mathcal{D}_{\text{val}} = \mathcal{D}_{\text{tr}} \cap \mathcal{D}_{\text{te}} = \mathcal{D}_{\text{val}} \cap \mathcal{D}_{\text{te}} = \varnothing$$
  그리고 각 부분집합은 배포 데이터와 같은 분포에서 뽑는다. 그래야 test 오차 $\hat R_{\text{te}} = \frac{1}{|\mathcal{D}_{\text{te}}|}\sum_{(x,y)\in\mathcal{D}_{\text{te}}} L(f(x), y)$ — test 예제에 대한 평균 손실이고 $|\cdot|$는 개수 — 가 새 데이터 오차의 불편 추정이 되는데, $\mathcal{D}_{\text{te}}$의 어떤 것도 $f$에 영향을 주지 않았을 *때에만* 그렇다. 계산 예: 샘플 10,000개를 80/10/10으로 나누면 8,000 / 1,000 / 1,000이다.
  - **반례:** 로봇 영상 20개에서 나온 프레임 10,000장을 섞어 80/10/10으로 나눈다. *프레임*으로는 서로소이지만 *에피소드*로는 아니다. 거의 똑같은 이웃 프레임이 양쪽에 들어가므로, test 수치는 이미 본 장면의 프레임 사이 보간을 잴 뿐이다. 나누는 단위는 일반화하고 싶은 단위여야 한다. 에피소드, 장면, 현장, 로봇.
- **분포 이동**: train과 다른 분포의 test(새 현장, 새 로봇, 새 조명) — 로보틱스의 *실제*
  조건이다. 논문들이 "seen/unseen" 분할([[01-canonical-papers/notes/4-vla/rt-1|RT-1]])과 OOD
  평가를 보고하는 이유이고, [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 강건성 결과가 그토록
  중요했던 이유다.
  - *정의:* $p_{\text{tr}}(x, y) \ne p_{\text{te}}(x, y)$이고, $p(x, y)$는 입력과 라벨의 결합분포다. $p(x, y) = p(x)\,p(y \mid x) = p(y)\,p(x \mid y)$이므로 어느 인수가 움직이느냐에 따라 이름 붙은 종류가 셋이다.
    - **공변량 이동**(covariate shift) — $p(x)$는 바뀌고 $p(y \mid x)$는 그대로다. 조명은 새롭지만 "균열"의 뜻은 같다. 정책 자신의 상태가 이동된 입력이 되는 모방 학습의 실패 방식도 이것이다([[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]]).
    - **라벨(사전) 이동** — $p(y)$는 바뀌고 $p(x \mid y)$는 그대로다. 균열 비율이 6%에서 0.6%로 떨어져도 균열은 여전히 균열처럼 보인다. 계산 예제(§4 뒤)의 ROC 대 정밀도 표가 정확히 이 경우다.
    - **개념 이동**(concept shift) — $p(y \mid x)$ 자체가 바뀐다. 현장이 보고 대상 균열의 정의를 더 엄격하게 바꾸면 같은 이미지가 다른 라벨을 받는다.
  - **분포 밖(OOD)** 입력은 극단적인 경우다. $p_{\text{tr}}(x)$가 사실상 0인 영역에서 온 test 입력이라, 모델이 보간할 데이터가 없다.
- 데이터 누수: test 정보가 학습에 스며드는 것(중복, 시간적 겹침, 사전학습 오염 —
  [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] 논문 스스로의 골칫거리). 숫자가 너무 좋아 보일
  때 첫 번째로 의심할 것.
  - *정의:* $\mathcal{D}_{\text{te}}$(또는 $\mathcal{D}_{\text{val}}$)의 정보가 적합된 모델이나 그 모델에 대한 선택에 닿는 모든 경로이고, 위의 "$\mathcal{D}_{\text{te}}$의 어떤 것도 $f$에 영향을 주지 않았다"는 조건을 깨뜨린다. 형태는 양쪽에 걸친 완전 중복·유사 중복 예제, 시간적 겹침(test 기간 이후에 기록한 데이터로 학습), 사전학습 말뭉치 오염, 그리고 **전체 데이터에 맞춘 전처리**다. 예컨대 분할 전에 계산한 정규화 평균과 분산은 test 통계를 학습에 조용히 실어 나른다.

### 2. 과적합과 정규화라는 우산

모델은 학습 데이터에는 점점 더 잘 맞으면서도 보지 못한 데이터에서는 점점 나빠질 수 있다. 균열이 아니라 한 현장의 조명을 배운 균열 감지기가 그렇다. 이 절은 손실 곡선 두 개로 그것을 알아보는 법과, 표준적인 처방 네 가지가 각각 무엇을 바꾸는지를 보인다.

- **과적합**: train 손실은 ↓인데 validation 손실이 ↑ — 일반화 대신 암기. **과소적합**:
  둘 다 높음. 무엇보다 먼저 **학습 곡선**으로 진단하라.
  - *두 단어 뒤에 있는 양*은 **일반화 격차**, 곧 $k$ 에포크 뒤의 같은 파라미터 $\theta_k$에서 보류 데이터 평균 손실과 학습 데이터 평균 손실의 차이다.
  $$\text{gap}_k = R_{\text{val}}(\theta_k) - R_{\text{tr}}(\theta_k)$$
  그래서 학습 곡선은 $R_{\text{tr}}$과 $R_{\text{val}}$을 $k$에 대해 그린 것일 뿐이다. **과적합**은 두 조건이 함께일 때의 이름이다. $R_{\text{tr}}$은 아직 떨어지고 *동시에* $R_{\text{val}}$은 올라가서 격차가 커진다. **과소적합**은 $R_{\text{tr}}$ 자체가 높게 머무는 것, 곧 보고 있는 데이터조차 맞추지 못하는 것이다. 계산 예: 에포크 10에서 학습 0.40 / 검증 0.45(격차 0.05, 둘 다 아직 하강 — 어느 쪽도 아님), 에포크 50에서 학습 0.05 / 검증 0.70(격차 0.65, 검증이 0.45에서 올라감 — 과적합).
  - **반례:** 격차가 크더라도 *일정하고* 검증 손실이 아직 떨어지고 있다면 아직 과적합이 아니다. 검증 데이터가 더 어렵거나 분포가 다르다는 뜻이고, 거기서 멈추면 진전을 버리게 된다.

<svg viewBox="0 0 560 262" style="max-width:100%;height:auto" role="img" aria-label="에포크에 따른 학습·검증 손실: 에포크 10에서 학습 0.40, 검증 0.45로 둘 다 하강하고, 검증은 에포크 21 근처에서 바닥을 찍은 뒤 에포크 50에서 0.70으로 오르며 학습은 0.05로 내려간다">
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6"><line x1="62.0" y1="196.0" x2="530.0" y2="196.0"/><line x1="62.0" y1="196.0" x2="62.0" y2="24.0"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6"><line x1="62.0" y1="196.0" x2="62.0" y2="200.0"/><line x1="140.0" y1="196.0" x2="140.0" y2="200.0"/><line x1="218.0" y1="196.0" x2="218.0" y2="200.0"/><line x1="296.0" y1="196.0" x2="296.0" y2="200.0"/><line x1="374.0" y1="196.0" x2="374.0" y2="200.0"/><line x1="452.0" y1="196.0" x2="452.0" y2="200.0"/><line x1="530.0" y1="196.0" x2="530.0" y2="200.0"/><line x1="58.0" y1="196.0" x2="62.0" y2="196.0"/><line x1="58.0" y1="154.5" x2="62.0" y2="154.5"/><line x1="58.0" y1="113.0" x2="62.0" y2="113.0"/><line x1="58.0" y1="71.5" x2="62.0" y2="71.5"/><line x1="58.0" y1="30.0" x2="62.0" y2="30.0"/></g>
  <text x="62.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="140.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">10</text>
  <text x="218.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">20</text>
  <text x="296.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">30</text>
  <text x="374.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">40</text>
  <text x="452.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">50</text>
  <text x="530.0" y="212.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">60</text>
  <text x="55.0" y="200.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0</text>
  <text x="55.0" y="158.5" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.25</text>
  <text x="55.0" y="117.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.5</text>
  <text x="55.0" y="75.5" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.75</text>
  <text x="55.0" y="34.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">1</text>
  <text x="296.0" y="227.0" font-size="12" fill="currentColor" text-anchor="middle">에포크</text>
  <text x="55.0" y="20.0" font-size="12" fill="currentColor" text-anchor="end">손실</text>
  <line x1="225.8" y1="30.0" x2="225.8" y2="92.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <line x1="225.8" y1="125.0" x2="225.8" y2="196.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <text x="230.8" y="38.0" font-size="12" fill="currentColor">조기 종료</text>
  <polyline points="62.0,30.0 65.9,37.6 69.8,44.9 73.7,51.8 77.6,58.4 81.5,64.7 85.4,70.6 89.3,76.3 93.2,81.7 97.1,86.9 101.0,91.8 104.9,96.4 108.8,100.9 112.7,105.1 116.6,109.2 120.5,113.0 124.4,116.6 128.3,120.1 132.2,123.4 136.1,126.6 140.0,129.6 143.9,132.5 147.8,135.2 151.7,137.8 155.6,140.2 159.5,142.6 163.4,144.8 167.3,147.0 171.2,149.0 175.1,150.9 179.0,152.8 182.9,154.5 186.8,156.2 190.7,157.8 194.6,159.3 198.5,160.7 202.4,162.1 206.3,163.4 210.2,164.6 214.1,165.8 218.0,166.9 221.9,168.0 225.8,169.0 229.7,170.0 233.6,170.9 237.5,171.8 241.4,172.7 245.3,173.5 249.2,174.2 253.1,174.9 257.0,175.6 260.9,176.3 264.8,176.9 268.7,177.5 272.6,178.1 276.5,178.6 280.4,179.1 284.3,179.6 288.2,180.1 292.1,180.5 296.0,181.0 299.9,181.4 303.8,181.7 307.7,182.1 311.6,182.5 315.5,182.8 319.4,183.1 323.3,183.4 327.2,183.7 331.1,184.0 335.0,184.2 338.9,184.5 342.8,184.7 346.7,184.9 350.6,185.1 354.5,185.3 358.4,185.5 362.3,185.7 366.2,185.9 370.1,186.1 374.0,186.2 377.9,186.4 381.8,186.5 385.7,186.6 389.6,186.8 393.5,186.9 397.4,187.0 401.3,187.1 405.2,187.2 409.1,187.3 413.0,187.4 416.9,187.5 420.8,187.6 424.7,187.7 428.6,187.8 432.5,187.8 436.4,187.9 440.3,188.0 444.2,188.1 448.1,188.1 452.0,188.2 455.9,188.2 459.8,188.3 463.7,188.3 467.6,188.4 471.5,188.4 475.4,188.5 479.3,188.5 483.2,188.6 487.1,188.6 491.0,188.6 494.9,188.7 498.8,188.7 502.7,188.7 506.6,188.8 510.5,188.8 514.4,188.8 518.3,188.8 522.2,188.9 526.1,188.9 530.0,188.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="62.0,21.7 65.9,29.3 69.8,36.6 73.7,43.5 77.6,50.1 81.5,56.4 85.4,62.3 89.3,68.0 93.2,73.4 97.1,78.6 101.0,83.5 104.9,88.1 108.8,92.6 112.7,96.8 116.6,100.9 120.5,104.7 124.4,108.3 128.3,111.8 132.2,115.1 136.1,118.3 140.0,121.3 143.9,124.0 147.8,126.5 151.7,128.8 155.6,130.8 159.5,132.7 163.4,134.5 167.3,136.1 171.2,137.5 175.1,138.9 179.0,140.1 182.9,141.1 186.8,142.1 190.7,142.9 194.6,143.7 198.5,144.3 202.4,144.9 206.3,145.3 210.2,145.7 214.1,146.0 218.0,146.2 221.9,146.3 225.8,146.4 229.7,146.4 233.6,146.3 237.5,146.1 241.4,145.9 245.3,145.6 249.2,145.3 253.1,144.9 257.0,144.5 260.9,144.0 264.8,143.4 268.7,142.8 272.6,142.2 276.5,141.5 280.4,140.8 284.3,140.0 288.2,139.2 292.1,138.3 296.0,137.4 299.9,136.5 303.8,135.6 307.7,134.6 311.6,133.5 315.5,132.5 319.4,131.4 323.3,130.2 327.2,129.1 331.1,127.9 335.0,126.7 338.9,125.5 342.8,124.2 346.7,122.9 350.6,121.6 354.5,120.3 358.4,118.9 362.3,117.5 366.2,116.1 370.1,114.7 374.0,113.2 377.9,111.7 381.8,110.2 385.7,108.7 389.6,107.2 393.5,105.6 397.4,104.1 401.3,102.5 405.2,100.9 409.1,99.3 413.0,97.6 416.9,95.9 420.8,94.3 424.7,92.6 428.6,90.9 432.5,89.1 436.4,87.4 440.3,85.6 444.2,83.9 448.1,82.1 452.0,80.3 455.9,78.5 459.8,76.6 463.7,74.8 467.6,72.9 471.5,71.1 475.4,69.2 479.3,67.3 483.2,65.4 487.1,63.4 491.0,61.5 494.9,59.5 498.8,57.6 502.7,55.6 506.6,53.6 510.5,51.6 514.4,49.6 518.3,47.6 522.2,45.5 526.1,43.5 530.0,41.4" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>
  <circle cx="140.0" cy="129.6" r="3.6" fill="currentColor"/>
  <circle cx="140.0" cy="121.3" r="3.6" fill="currentColor"/>
  <line x1="140.0" y1="121.3" x2="140.0" y2="129.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <circle cx="452.0" cy="188.2" r="3.6" fill="currentColor"/>
  <circle cx="452.0" cy="80.3" r="3.6" fill="currentColor"/>
  <line x1="452.0" y1="80.3" x2="452.0" y2="188.2" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="147.0" y="105.3" font-size="12" fill="currentColor">에포크 10: 0.40 / 0.45</text>
  <text x="147.0" y="119.3" font-size="11" fill="currentColor" fill-opacity="0.8">격차 0.05, 둘 다 하강</text>
  <text x="444.0" y="64.3" font-size="12" fill="currentColor" text-anchor="end">에포크 50: 0.05 / 0.70</text>
  <text x="444.0" y="78.3" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">격차 0.65: 과적합</text>
  <line x1="62.0" y1="248" x2="90.0" y2="248" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="96.0" y="252" font-size="12" fill="currentColor">검증 손실 — 다시 올라간다</text>
  <line x1="300" y1="248" x2="328" y2="248" stroke="currentColor" stroke-width="2"/>
  <text x="334" y="252" font-size="12" fill="currentColor">학습 손실 — 계속 내려간다</text>
</svg>

위 예제의 두 에포크를 지나는 학습·검증 손실이다. 에포크 10에서는 $0.40$과 $0.45$로 둘 다 아직 내려가고, 에포크 50에서는 $0.05$와 $0.70$으로 격차가 $0.65$이며 검증 손실이 오르고 있으니 과적합이다. 두 에포크 사이의 모양은 설명을 위해 그린 것이고, 조기 종료는 검증 손실이 가장 낮은 자리, 곧 *조기 종료*라고 적힌 가는 세로선의 체크포인트를 남긴다.


- "정규화"라 불리는 방법들은 *해로운 과적합을 줄인다*는 넓은 목표를 공유하지만, 작동
  기제는 서로 다르다: weight decay(가우시안 사전 — [[02-foundations/probability|3. 확률 §4]]),
  dropout([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]), 데이터 증강
  ([[01-canonical-papers/notes/1-foundations/vgg|VGG]] 이후), early stopping, 그리고 현대적 반전 —
  *제약 대신 더 많은 데이터*([[01-canonical-papers/notes/1-foundations/scaling-laws|스케일링 법칙]]).
  - *정의:* **정규화 기법**은 학습 손실이 아니라 *검증* 손실을 낮추려는, 학습 절차에 가하는 모든 변경이다. 명시적인 종류는 파라미터에 벌점 $\Omega$를 하이퍼파라미터 $\lambda \ge 0$로 가중해 더한다.
  $$\min_\theta\ \frac{1}{N}\sum_{i=1}^{N} L\big(f_\theta(x_i), y_i\big) + \lambda\, \Omega(\theta), \qquad \Omega(\theta) = \tfrac12 \lVert\theta\rVert^2 \ \text{for L2}$$
  그래서 $\lambda$가 클수록 학습 적합을 내주고 작은 가중치를 산다. 이름 붙은 네 방법과 각각의 작동 기제:
    - **Weight decay**는 매 스텝 모든 가중치를 고정된 비율로 줄인다. 학습률 $\eta$에 대해 $w \leftarrow w(1 - \eta\lambda)$이고, $\eta = 0.1$, $\lambda = 0.01$이면 비율이 $0.999$라 반대 방향 그래디언트 없이 1,000스텝이 지나면 가중치의 $0.999^{1000} = 0.368$만 남는다. 순수 SGD에서는 위의 L2 벌점과 같다(Adam에서 같지 않은 이유는 §6).
    - **Dropout**은 학습 중 각 은닉 유닛을 확률 $p$로 독립적으로 0으로 만들고 살아남은 것을 키운다. $m_j \sim \text{Bernoulli}(1 - p)$에 대해 $\tilde h_j = m_j h_j / (1 - p)$이므로 활성값의 기댓값이 그대로이고, 추론에서는 그냥 $h$를 쓴다. $p = 0.5$, $h = (2, 4)$, 마스크 $m = (1, 0)$이면 층은 $(4, 0)$을 내보낸다.
    - **데이터 증강**은 라벨이 바뀌지 않도록 고른 무작위 변환 $T$(자르기, 뒤집기, 색 흔들기)에 대해 $(T(x), y)$로 학습한다. **반례:** "왼쪽으로 돌기" 시연에 좌우 뒤집기를 적용하는 것은 증강이 아니다. 올바른 라벨을 바꾸기 때문이다.
    - **Early stopping**은 검증 손실이 가장 낮은 체크포인트 $\hat k = \arg\min_k R_{\text{val}}(\theta_k)$를 남기는 것이고, 그림에서 *조기 종료*라고 적힌 가는 세로선이 그것이다.

학습 자료의 세부를 모두 맞추면 우연한 단서에 의존할 수 있어 정규화가 필요하다. 균열 검출기가 결함보다 특정 현장의 조명을 배울 수 있다. 증강은 변환이 정답을 보존하고 의미 있는 변동을 닮을 때 그 지름길을 억제한다. **여기서 얻는 독법.** 학습 곡선을 분할·증강 정책과 함께 본다. 정규화 목록이 길어도 이웃 프레임의 검증 손실 개선만으로 새 현장 일반화를 보이지는 못한다.

### 3. 지표 사전 (어떤 Results 표든 읽기)

결과 표는 지표를 한 단어로 적는다. mAP, FID, 성공률 같은 단어마다 제 분모와 방법을 돋보이게 하는 제 방식을 가진 식이 숨어 있다. 이 절은 그 사전이다. 각 지표가 무엇을 세는지 알아야 다시 계산할 수 있고, 무엇을 빠뜨리는지 볼 수 있다.

| 과제 | 지표 | 의미 |
|---|---|---|
| 분류 | accuracy, top-5 | 맞춘 비율 (top-5: 정답이 5개 후보 안 — ImageNet 관례) |
| 분류 (불균형) | precision / recall / F1 | 표시한 것 중 진짜 비율 / 진짜 중 잡아낸 비율 / 둘의 조화평균 |
| 검출 | **IoU**, **mAP** | 박스 겹침 비율; 클래스별 평균 정밀도의 평균 — IoU 0.5 기준(PASCAL VOC)이거나 IoU 0.50–0.95에 걸친 평균(COCO); 비교 전에 어느 쪽인지 확인 |
| 분할 | mIoU | 클래스 평균 IoU |
| 생성 (이미지) | **FID** | 생성/실제 특징 분포 사이 거리 — 낮을수록 좋다 |
| 언어모델 | perplexity | 비트 기준 $2^{\text{교차 엔트로피}}$ ([[02-foundations/information-theory\|5. 정보이론 §2]]) |
| 번역/캡셔닝 | BLEU | 참조문과의 n-gram 겹침 |
| 로보틱스 | **success rate** | 목표 달성 시행 비율 — 숫자보다 *어떤* 시행(seen/unseen)인지가 더 중요 |
| 검색 | recall@k | 정답이 상위 k개 안 |

정확도·정밀도·재현율·$F_1$·AUC는 이 페이지가 끝까지 유도하는 지표이고, §4 뒤의 계산 예제에서 **E1**로 다룬다. 균형 잡힌 벤치마크의 AUC가 배포에 대해 거의 아무것도 말해 주지 않게 만드는 기저율 붕괴까지 거기 있다. 사전의 나머지는 여기서 이어진다.

#### 사전의 나머지, 수식과 함께

표의 한 줄 풀이는 지표를 알아보는 데 충분하고, 아래 내용은 지표를 다시 계산하는 데 충분하다. 모두 test 집합 위의 예측과 정답으로 계산하는 숫자다.

- **Top-$k$ 정확도.** 참 클래스가 점수 상위 $k$개 클래스 안에 드는 항목의 비율이다.
  $$\text{Acc}@k = \frac{1}{N}\sum_{i=1}^{N} \mathbb{1}\big[y_i \in \text{top-}k(\hat p_i)\big]$$
  그래서 top-1은 보통의 정확도이고, top-5는 상위 다섯 안의 순위 오류를 봐준다. 참 클래스를 3위로 매긴 항목은 top-5에서는 맞고 top-1에서는 틀리며, ImageNet 표의 두 열 차이가 통째로 그것이다.
- **IoU(합집합 대비 교집합).** 예측 영역 $A$와 정답 영역 $B$(박스나 픽셀 마스크)에 대해, $|\cdot|$를 넓이로 두면
  $$\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
  이고, 완벽히 일치하면 1, 전혀 겹치지 않으면 0이다. 박스 $[0,2]\times[0,2]$와 $[1,3]\times[1,3]$은 $1 \times 1$ 정사각형만큼 겹치므로 $\text{IoU} = 1/(4 + 4 - 1) = 1/7 = 0.143$이다. 검출은 아직 짝지어지지 않은 정답 물체와의 IoU가 문턱값(PASCAL VOC는 0.5)에 닿아야 TP로 세므로, 이 두 박스는 거짓양성*이면서* 놓침이 된다.
- **AP와 mAP.** 한 클래스의 검출을 신뢰도 순으로 늘어놓고, $n$번째 검출 뒤의 정밀도 $P_n$과 재현율 $R_n$을 기록한다. 평균 정밀도는 그 정밀도–재현율 곡선 아래 넓이다.
  $$\text{AP} = \sum_{n} \big(R_n - R_{n-1}\big)\, P^{\text{interp}}_n, \qquad P^{\text{interp}}_n = \max_{m \ge n} P_m, \qquad \text{mAP} = \frac{1}{C}\sum_{c=1}^{C} \text{AP}_c$$
  $R_0 = 0$이고, 보간 정밀도는 이 재현율 이상에서의 최고 정밀도이며, mAP는 클래스 $C$개에 대해 평균한다. 계산 예: 실제 물체 둘, 검출 셋이 TP, FP, TP 순이면 $P = 1, 0.5, 0.667$, $R = 0.5, 0.5, 1.0$이므로 $P^{\text{interp}} = 1, 0.667, 0.667$이고 $\text{AP} = 0.5(1) + 0(0.667) + 0.5(0.667) = 0.833$이다. COCO는 여기에 더해 IoU 문턱값 $0.50, 0.55, \dots, 0.95$에 대해 mAP를 평균하므로, COCO 수치와 VOC 수치는 같은 양이 아니다.
- **mIoU(분할).** 클래스 $c$마다 픽셀 개수로 $\text{IoU}_c = TP_c / (TP_c + FP_c + FN_c)$를 구하고, mIoU는 클래스에 대한 평균이다. $TP = 80$, $FP = 10$, $FN = 10$인 클래스는 IoU $0.8$, $TP = 5$, $FP = 10$, $FN = 5$인 드문 클래스는 $0.25$이고 mIoU는 $0.525$다. 흔한 클래스가 끌어올리는 만큼 드문 클래스가 끌어내리는 것, 그것이 클래스별로 평균하는 이유다.
- **FID(Fréchet Inception distance).** 실제 이미지의 Inception 신경망 특징에 평균 $\mu_r$, 공분산 $\Sigma_r$인 가우시안을, 생성 이미지에 $\mu_g, \Sigma_g$인 가우시안을 맞춘다. FID는 두 가우시안 사이의 Fréchet 거리다.
  $$\text{FID} = \lVert \mu_r - \mu_g \rVert^2 + \operatorname{Tr}\Big(\Sigma_r + \Sigma_g - 2\big(\Sigma_r \Sigma_g\big)^{1/2}\Big)$$
  첫 항은 평균이 어긋난 것을, 대각합($\operatorname{Tr}$, 대각 성분의 합) 항은 퍼짐이 틀린 것을 벌한다. 1차원에서는 $(\mu_r - \mu_g)^2 + (\sigma_r - \sigma_g)^2$로 줄어든다. 실제 $\mathcal{N}(0, 1^2)$ 대 생성 $\mathcal{N}(0.5, 2^2)$이면 $0.25 + 1 = 1.25$다. 낮을수록 좋고, 표본 수에 따라 달라지므로 같은 $N$에서만 비교한다.
- **Perplexity.** 보류 텍스트 토큰 $N$개에서 언어 모델의 평균 다음 토큰 교차 엔트로피를 지수로 올린 값이다.
  $$\text{PPL} = \exp\Big(-\frac{1}{N}\sum_{t=1}^{N} \ln p\big(x_t \mid x_{<t}\big)\Big) = 2^{H}, \quad H = -\frac{1}{N}\sum_{t=1}^{N} \log_2 p\big(x_t \mid x_{<t}\big)$$
  그래서 "모델이 PPL개의 토큰 중 균등하게 고르는 만큼 불확실하다"로 읽는다. 모델이 참 토큰들에 확률 $0.5$, $0.25$, $0.125$를 주면 $H = (1 + 2 + 3)/3 = 2$비트이고 $\text{PPL} = 4$다. $N$이 서로 다른 단위를 세므로, 토크나이저가 다른 perplexity끼리는 비교할 수 없다.
- **BLEU.** *잘라낸*(clipped) $n$-gram 정밀도 $p_n$(후보의 각 $n$-gram은 참조문에 나온 횟수까지만 센다)의 기하평균에, 참조문보다 짧은 후보에 대한 간결성 벌점을 곱한다.
  $$\text{BLEU} = \text{BP} \cdot \exp\Big(\sum_{n=1}^{4} \tfrac14 \log p_n\Big), \qquad \text{BP} = \begin{cases} 1 & c > r \\ e^{\,1 - r/c} & c \le r \end{cases}$$
  $c$와 $r$은 후보와 참조문의 길이다. 후보 "the cat sat on the mat", 참조 "the cat is on the mat"이면 $p_1 = 5/6$, $p_2 = 3/5$, $p_3 = 1/4$, $p_4 = 0/3$, $\text{BP} = 1$이다. **경계 사례:** $p_4$ 하나가 0이면 거의 맞는 문장의 문장 단위 BLEU가 정확히 $0$이 된다. BLEU를 말뭉치 전체로 계산하거나 평활화를 쓰는 이유다. 여기서 2-gram 버전은 $\sqrt{(5/6)(3/5)} = 0.707$이다.
- **성공률.** 목표를 달성한 시행의 비율이다. 독립 시행 $n$번에 성공 $k$번이면 $\hat p = k/n$이고 이항 표준오차는
  $$\text{SE}\big(\hat p\big) = \sqrt{\frac{\hat p\,(1 - \hat p)}{n}}$$
  이므로 불확실성은 $\sqrt n$로만 줄고 $\hat p = 0.5$에서 가장 크다. E1c의 10번 중 9번이면 $0.095$다. 정작 틀리는 부분은 *어느 구간*을 인쇄하느냐다. 정규근사, Wilson 구간([[06-research-practice/experimental-design-reproducibility|실험 설계 §4]]), 백분위 부트스트랩이 $n = 10$에서 서로 다르고, 셋 모두 §4 뒤의 계산 예제에서 E1c로 계산하며 Wilson 구간의 식도 거기서 준다. 에피소드 정의(§5)가 없으면 이 숫자는 의미가 없다. 같은 구간을 Wald 구간(정규근사의 다른 이름)과 견주어 계산한 곳이 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기]]의 계산 절로, 연구 실무 트랙이 고정해 둔 연구 RS1([[06-research-practice/index|6. 연구 실무]]: 패널 위에서 힘 제어기 둘을 비교하는 연구)의 파일럿 9/10과 6/10을 쓴다.
- **Recall@$k$(검색).** 질의 집합 $Q$에 대해 정답 항목이 상위 $k$개 결과 안에 드는 질의의 비율, $\frac{1}{|Q|}\sum_{q \in Q} \mathbb{1}[\text{rank}_q \le k]$다. 정답 순위가 1, 4, 12인 질의 셋이면 recall@5 $= 2/3$이다. 분류의 재현율과 이름은 같지만 분모가 다르다. 여기서 분모는 양성이 아니라 질의다.

- 지표는 적대적으로 읽어라: *어떤* 분포에서, *몇 번의* 시행으로, *분산은* 얼마인 success
  rate인가? 10회 중 9회 성공은 신뢰구간이 넓다 — "90%"만이 아니라 횟수와 불확실성을
  함께 봐야 한다.

### 4. 실험의 문법

결과 표는 변화 하나가 숫자 하나를 낳았다는 논증이다. 이 절은 그 논증이 어떻게 세워지는지, 곧 튜닝된 베이스라인, 하나만 바꾼 절제 실험, 충분한 시드와, 그것이 어디서 무너지는지를 다룬다.

- **베이스라인**: 이겨야 하는 대상(그리고 *튜닝된* 것이어야 한다 — 약한 베이스라인은 이
  분야의 고질병). **절제 실험**(ablation): 구성 요소 하나를 빼서 그것이 중요했음을 보이기
  — 방법과 결과를 잇는 증거. **SOTA**: 최고 성능; 인상적이지만 취약하다 — 벤치마크
  특정적이고 연산량과 교락되기 일쑤.
  - *절제 실험, 정확히:* 전체 방법과, 구성요소 $c$ 하나만 빼거나 바꾸고 나머지 — 데이터, 연산 예산, 레시피, 시드, 평가 규약 — 는 고정한 같은 방법 사이의 통제된 비교다. 결과는 추정된 효과다.
  $$\Delta_c = M(\text{full}) - M(\text{full} \setminus c)$$
  $M$은 보고 지표다. 전체 방법 성공률 76%, 행동 청킹을 뺀 같은 방법 58%면 $\Delta = 18$%p가 청킹 몫이다 — 다른 것이 아무것도 바뀌지 않았을 때에만 청킹 몫이다. **반례:** 구성요소를 빼면서 *동시에* 연산을 아끼려고 학습을 줄이면 두 변화를 한꺼번에 잰 것이라 어느 쪽에도 $\Delta$를 돌릴 수 없다.
  - *베이스라인, 정확히:* 비교 대상도 같은 조건 — 같은 데이터, 같은 예산, 같은 규약 — 을 만족해야 하고, 제안 방법과 비슷한 규모의 탐색으로 튜닝되어야 한다. 하나라도 어기면 그 주장에 대한 베이스라인이 아니다.
- 읽을 때의 공정 비교 체크리스트: 같은 데이터? 같은 연산/파라미터? 같은 평가 프로토콜?
  튜닝된 베이스라인? 표가 이에 답하지 않으면 그 숫자는 장식이다.
- 시드와 분산: 딥러닝 결과는 랜덤 시드에 따라 흔들린다; 진지한 보고는 실행 횟수와 실험에
  맞는 불확실성 지표(표준편차·표준오차·신뢰구간·짝지은 검정)를 명시한다 — 로보틱스
  논문은 여러 *롤아웃과 장면*에 걸쳐 보고한다. **지금 보는 것이 어느 쪽인지 알아야 한다**:
  표준편차 $\sigma$는 *개별 실행*이 얼마나 흩어지는지를 말하고 실행을 늘려도 줄지 않는다.
  표준오차 $\sigma/\sqrt{n}$은 *평균*이 얼마나 단단히 고정됐는지를 말하고 줄어든다.
  $n = 4$면 둘이 2배 차이이므로, 작은 쪽을 그린 논문은 공짜로 더 좁은 오차 막대를 얻는다 —
  두 논문의 막대를 비교하기 전에 캡션을 확인하라. 같은 실행을 재현하고, 코드를 더한 뒤에도 여전히 재현하는 시드는
  [[02-foundations/tools/python-research-code|12.3 연구 코드를 위한 Python §7]]이고, 막대가 셋 가운데 무엇인지 말하는 캡션은 [[02-foundations/tools/latex-figures-references|12.6 글쓰기 도구 §8]]이다.
  - *세 양을 풀어 쓰면* 결과가 $x_1, \dots, x_n$이고 평균이 $\bar x$인 실행 $n$번에 대해
  $$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar x)^2}, \qquad \text{SE} = \frac{s}{\sqrt n}, \qquad \text{95\% CI} = \bar x \pm t_{0.975,\,n-1}\cdot \text{SE}$$
  이다. 표본 표준편차 $s$는 $\bar x$를 같은 숫자들로 추정했기 때문에 $n - 1$로 나눈다. SE는 평균을 내면 실행 간 잡음이 상쇄되므로 $\sqrt n$에 따라 줄어든다. **신뢰구간**은 SE에 Student-$t$ 분위수 $t_{0.975,\,n-1}$을 곱하는데, $n$이 작으면 이 값이 정규분포의 1.96보다 크다. 신뢰구간은 반복 실험의 95%에서 참 평균을 덮는 절차이지, 이 구간 하나에 대한 95% 확률 진술이 아니다. 분위수 $t_{0.975,\,\nu}$는 자유도 $\nu=n-1$인 스튜던트 $t$ 변수가 확률 2.5%로 넘는 값이다. 실행 간 잡음이 가우시안이면 $(\bar x-\mu)/\text{SE}$가 정확히 그 분포를 따른다([[02-foundations/probability|3. 확률 §6]]이 정의한다). 참 SE가 아니라 *추정한* SE로 나누면 흩어짐이 더해지므로 꼬리가 표준정규분포보다 두껍고, 표준정규분포의 97.5% 점은 $1.96$이다. 실행이 쌓일수록 $1.96$ 쪽으로 줄어서 $t_{0.975,3}=3.182$, $t_{0.975,6}=2.447$, $t_{0.975,30}=2.042$다. 계산 예, 시드 넷의 성공률이 72, 76, 80, 84%면 $\bar x = 78$, $s = 5.16$, $\text{SE} = 2.58$, $t_{0.975,3} = 3.18$이므로 95% CI는 $[69.8, 86.2]$다. 같은 네 실행을 캡션이 어느 양을 말하느냐에 따라 $\pm 2.6$, $\pm 5.2$, $\pm 8.2$점 막대로 그릴 수 있다. 두 방법의 *차이*를 검정하는 법은 [[02-foundations/probability|3. 확률 §6]]에 있다. 바로 아래 계산 예제가 E1c의 네 시드 기록 둘로 그 차이를 내는데, 발표된 16포인트 격차는 거기서 살아남지 못한다.

### 대상으로 한 번 끝까지 · Worked case

**1. 세어서 만드는 네 지표, 그리고 정확도가 거짓말하는 이유.** E1a의 표가 한 문턱값에서 이진 분류기의 **혼동 행렬**(confusion matrix)이다. 모든 test 항목은 정확히 한 칸에 들어가고, 칸의 이름은 *예측*이 양성이었는지 음성이었는지, 그것이 *맞았는지(true)* 틀렸는지(false)로 붙는다. **TP**(참양성) = 균열로 예측, 실제 균열. **FP**(거짓양성, 오경보) = 균열로 예측, 실제 정상. **FN**(거짓음성, 놓침) = 정상으로 예측, 실제 균열. **TN**(참음성) = 정상으로 예측, 실제 정상. 여기의 모든 지표는 이 네 개수의 비다.

$$\text{Accuracy} = \frac{TP + TN}{TP + FP + FN + TN}, \quad P = \text{Precision} = \frac{TP}{TP + FP}, \quad R = \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = \frac{2PR}{P + R}$$

정밀도는 *예측* 양성 열로, 재현율은 *실제* 양성 행으로 나누므로 두 값은 서로 다른 질문에 답한다. $F_1$은 $P$와 $R$의 조화평균이다. 정밀도와 재현율은 둘 다 TN을 쓰지 않으므로, 음성이 양성보다 압도적으로 많아도 정보를 잃지 않는다. E1a의 개수를 대입하면:

- **정확도(accuracy)** $= \frac{TP+TN}{1000} = \frac{970}{1000} = 97.0\%$ — 그런데 무조건 "정상"이라고만 답하는 감지기도 $\frac{940}{1000} = 94.0\%$가 나온다. 여기서 정확도는 거의 무용하고, 그 94%가 이유를 보여 주는 **반례**다. 상수로 답해도 거의 따라잡히는 지표는 우리가 원하는 능력을 재고 있지 않다.
- **정밀도(precision)** $= \frac{TP}{TP+FP} = \frac{40}{50} = 0.80$ — 플래그한 것 중 80%가 진짜였다. 점검자가 신경 쓰는 숫자다: 출동이 얼마나 헛되는가.
- **재현율(recall)** $= \frac{TP}{TP+FN} = \frac{40}{60} = 0.667$ — 실제 균열 중 3분의 2를 잡았다. **균열 20개를 놓쳤고**, 이것이 안전 담당자가 신경 쓰는 숫자다.
- **F1** $= \frac{2PR}{P+R} = \frac{2(0.80)(0.667)}{1.467} = 0.727$ — 조화평균이라 *둘 중 하나만* 낮아도 낮게 유지된다. **반례:** 같은 두 수의 산술평균은 $0.733$이고, 정밀도 $0.9$·재현율 $0.5$처럼 한쪽으로 쏠린 쌍도 산술평균은 $0.70$으로 매겨 겨우 조금 낮을 뿐인데, 그 쌍의 조화평균은 $0.643$이다. 나쁜 절반을 좋은 절반 뒤에 숨기는 일이야말로 $F_1$이 거부하는 것이다.

모든 Results 표에 들고 갈 교훈: 정밀도와 재현율은 문턱값 하나로 서로 맞바꾸는 값이므로, 유리한 쪽만 보고한 논문은 문장의 절반만 말한 것이다. 그리고 건설에서는 이 비대칭이 실제다 — 오경보는 점검 한 번을 낭비하지만, 놓친 균열은 구조물을 대가로 할 수 있다.

**2. 문턱값 없이 순서만: E1b의 AUC.** 문턱값을 훑으면 각 설정이 *참양성률* $\text{TPR} = TP/(TP+FN)$(즉 재현율)과 *거짓양성률* $\text{FPR} = FP/(FP+TN)$을 준다. TPR을 FPR에 대해 그린 것이 **ROC 곡선**이고 그 아래 넓이가 **AUC**다. AUC에는 들고 다닐 만한 정확한 뜻이 있다. *무작위로 고른 양성이 무작위로 고른 음성보다 높은 점수를 받을 확률*이다. E1b의 균열 패널 $0.90, 0.80, 0.60$과 정상 패널 $0.70, 0.50, 0.40, 0.20$을 보면, $3 \times 4 = 12$쌍 중 11쌍이 옳게 정렬되므로 $\text{AUC} = 11/12 = 0.917$이다 — 문턱값이 개입하지 않는다. 쌍 세기로 쓰면 다음과 같다.

$$\text{AUC} = \frac{1}{n_+ n_-} \sum_{i=1}^{n_+} \sum_{j=1}^{n_-} \Big( \mathbb{1}\big[s_i^+ > s_j^-\big] + \tfrac12\, \mathbb{1}\big[s_i^+ = s_j^-\big] \Big)$$

$s_i^+$는 양성 항목 $n_+$개의 점수, $s_j^-$는 음성 $n_-$개의 점수이고, $\mathbb{1}[\cdot]$은 조건이 성립하면 1, 아니면 0이다. 동점은 동전 던지기이므로 절반으로 센다. 위에서 틀린 한 쌍은 균열 패널의 $0.60$이 정상 패널의 $0.70$보다 낮은 쌍이다. AUC $= 0.5$는 우연 수준의 정렬이고 $1$은 완벽한 정렬이다. **반례:** AUC는 최적 문턱값에서의 정확도가 아니다. E1b를 훑으면 단일 문턱값이 낼 수 있는 최고는 일곱 장 중 여섯 장, $0.857$이고($\tau = 0.75$에서, 그리고 배포 문턱값 $\tau = 0.55$에서 다시), 같은 일곱 점수의 AUC는 $0.917$이다. AUC는 문턱값을 아예 정하지 않고 순서에 대해서만 값을 받기 때문이다. **왜 중요한가:** AUC만 보고한 논문은 모델이 순위를 잘 매긴다는 말만 한 것이고, 누군가 문턱값을 정해 점검자를 출동시켜야 할 때 무슨 일이 벌어지는지는 아무 말도 하지 않은 것이다.

<svg viewBox="0 0 560 270" style="max-width:100%;height:auto" role="img" aria-label="E1b의 ROC 곡선을 균열 3장 × 정상 4장의 격자 위 계단으로 그린 것: 12칸 중 11칸이 그 아래에 있어 AUC = 11/12이고, 빠진 칸은 균열 0.60이 정상 0.70보다 낮게 매겨진 쌍이며, 문턱값 0.75와 0.55를 표시했다">
  <rect x="170.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="170.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="222.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="222.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="222.0" y="42.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="274.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="274.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="274.0" y="42.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="326.0" y="162.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="326.0" y="102.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <rect x="326.0" y="42.0" width="52.0" height="60.0" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35"><line x1="170.0" y1="222.0" x2="170.0" y2="42.0"/><line x1="222.0" y1="222.0" x2="222.0" y2="42.0"/><line x1="274.0" y1="222.0" x2="274.0" y2="42.0"/><line x1="326.0" y1="222.0" x2="326.0" y2="42.0"/><line x1="378.0" y1="222.0" x2="378.0" y2="42.0"/><line x1="170.0" y1="222.0" x2="378.0" y2="222.0"/><line x1="170.0" y1="162.0" x2="378.0" y2="162.0"/><line x1="170.0" y1="102.0" x2="378.0" y2="102.0"/><line x1="170.0" y1="42.0" x2="378.0" y2="42.0"/></g>
  <rect x="170.0" y="42.0" width="52.0" height="60.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3"/>
  <polyline points="170.0,222.0 170.0,162.0 170.0,102.0 222.0,102.0 222.0,42.0 274.0,42.0 326.0,42.0 378.0,42.0" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <text x="176.0" y="196.0" font-size="11" fill="currentColor">0.90</text>
  <text x="176.0" y="136.0" font-size="11" fill="currentColor">0.80</text>
  <text x="196.0" y="117.0" font-size="11" fill="currentColor" text-anchor="middle">0.70</text>
  <text x="228.0" y="76.0" font-size="11" fill="currentColor">0.60</text>
  <text x="248.0" y="57.0" font-size="11" fill="currentColor" text-anchor="middle">0.50</text>
  <text x="300.0" y="57.0" font-size="11" fill="currentColor" text-anchor="middle">0.40</text>
  <text x="352.0" y="57.0" font-size="11" fill="currentColor" text-anchor="middle">0.20</text>
  <text x="170.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="222.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1/4</text>
  <text x="274.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1/2</text>
  <text x="326.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">3/4</text>
  <text x="378.0" y="237.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1</text>
  <text x="162.0" y="226.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">0</text>
  <text x="162.0" y="166.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">1/3</text>
  <text x="162.0" y="106.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">2/3</text>
  <text x="162.0" y="46.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="end">1</text>
  <text x="274.0" y="254.0" font-size="12" fill="currentColor" text-anchor="middle">FPR (정상 패널 4장 중 오경보)</text>
  <text x="162.0" y="32.0" font-size="12" fill="currentColor" text-anchor="end">TPR</text>
  <circle cx="170.0" cy="102.0" r="5" fill="currentColor"/>
  <circle cx="222.0" cy="42.0" r="5" fill="currentColor"/>
  <text x="160.0" y="124.0" font-size="12" fill="currentColor" text-anchor="end">τ = 0.75</text>
  <text x="230.0" y="34.0" font-size="12" fill="currentColor">τ = 0.55 (배포)</text>
  <text x="394.0" y="52.0" font-size="12" fill="currentColor" font-weight="600">AUC = 11/12 = 0.917</text>
  <text x="394.0" y="68.0" font-size="11" fill="currentColor" fill-opacity="0.85">12칸 중 11칸 칠함</text>
  <text x="394.0" y="128.0" font-size="11" fill="currentColor">점수를 높은 쪽부터 걸으면:</text>
  <text x="394.0" y="144.0" font-size="11" fill="currentColor">↑ 균열 패널</text>
  <text x="394.0" y="160.0" font-size="11" fill="currentColor">→ 정상 패널</text>
  <text x="12" y="54.0" font-size="11" fill="currentColor">틀린 한 쌍:</text>
  <text x="12" y="69.0" font-size="11" fill="currentColor">균열 0.60이</text>
  <text x="12" y="84.0" font-size="11" fill="currentColor">정상 0.70보다 낮다</text>
  <line x1="124.0" y1="65.0" x2="192.0" y2="72.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
</svg>

E1b의 점수 일곱 개를 높은 쪽부터 걸은 그림이다. 균열 패널 하나마다 곡선이 3분의 1씩 올라가고 정상 패널 하나마다 4분의 1씩 오른쪽으로 가므로, 균열 대 정상 쌍의 $3\times4$ 격자에서 계단 아래 칠한 칸이 $11$개, 곧 $\text{AUC}=11/12=0.917$이다. 빈 칸 하나가 순서가 틀린 유일한 쌍, 곧 정상 $0.70$보다 낮은 균열 $0.60$이고, 두 점은 각각 일곱 장 중 여섯 장을 맞히는 두 문턱값, $(0,\ 2/3)$의 $\tau=0.75$와 $(1/4,\ 1)$의 배포 문턱값 $\tau=0.55$다.

**3. 같은 ROC 점, 다른 기저율.** 그 문턱값 독립성이 AUC를 보고하는 이유이고, 그 뒤에 숨은 기저율 독립성이 AUC가 오도하는 이유다. E1a는 $\text{TPR} = 40/60 = 0.667$, $\text{FPR} = 10/940 = 0.011$에 있다. 같은 감지기를 더 잘 지어진 현장, 균열이 6%가 아니라 **0.6%** 수준인 곳으로 옮기면 패널 1,000장에서 $TP = 0.667 \times 6 = 4.0$, $FP = (10/940) \times 994 = 10.6$이 된다.

| | 균열 6% | 균열 0.6% |
|---|---|---|
| TPR | 0.667 | 0.667 — 그대로 |
| FPR | 0.011 | 0.011 — 그대로 |
| ROC 점 | 동일 | 동일 |
| **정밀도** | **0.80** | **0.27** |

ROC 곡선도 AUC도 전혀 움직이지 않는데 정밀도는 세 배로 무너진다. **TPR과 FPR은 실제 양성군과 실제 음성군 안에서 각각 계산되는 조건부 비율**이므로 두 클래스의 조건부 점수분포가 그대로라면 양성 비율이 바뀌어도 ROC 곡선은 유지된다. 반면 정밀도는 양성으로 예측된 표본에 조건화하므로 기저율에 의존한다. 그러므로 균형 잡힌 벤치마크에서 잰 AUC는 양성이 드문 현장에서 시스템이 어떻게 굴지에 대해 거의 아무것도 말해 주지 않는다 — [[04-robotics/human-intent-prediction|23. 의도 예측 §5]]의 상황이고, 현장의 모든 경보 시스템의 상황이다. 논문이 AUC를 보고하면, 배포 기저율 위에서 명시된 재현율에 대한 정밀도를 요구하라.

**4. "10번 중 9번"은 얼마나 넓은가: E1c의 부트스트랩.**

> [!info] 정의 — 백분위 부트스트랩 신뢰구간
> **무엇인가:** 가정한 분포에서 읽어 내는 공식이 아니라 *절차*가 만들어 내는 구간 추정이다. 부트스트랩을 부트스트랩이게 하는 조건이 셋이다. (1) **재표본** 하나는 크기 $n$인 관측 표본에서 $n$개를 **복원추출**로 뽑으므로 어떤 항목은 두 번 나오고 어떤 항목은 안 나온다. (2) 재표본마다 통계량을 다시 계산하고, 그 흩어짐이 **부트스트랩 분포** $\hat\theta^*$다. (3) **백분위** 구간은 그 분포의 $\alpha/2$, $1-\alpha/2$ 분위수다.
> $$\text{CI}_{1-\alpha} = \Big[\,Q_{\alpha/2}\big(\hat\theta^*\big),\ Q_{1-\alpha/2}\big(\hat\theta^*\big)\,\Big]$$
> $Q_q$는 부트스트랩 분포가 확률 $q$ 이상으로 도달하는 가장 작은 값이고, 95% 구간이면 $\alpha = 0.05$다. 요령의 전부는 가지고 있지 않은 모집단 자리에 가지고 있는 표본을 세우는 것이다.
> **예.** 아래에서 유도하는 E1c 파일럿: $[0.70,\ 1.00]$.
> **반례.** 10번 중 10번 성공. 성공만 든 표본의 재표본은 모두 성공뿐이라 부트스트랩 분포가 점 $1.00$ 하나가 되고 "95% 구간"은 $[1.00,\ 1.00]$이 된다. 시행 열 번으로 확실성을 주장하는 셈이다. 부트스트랩은 건네받은 데이터의 범위 밖으로 결코 나가지 못하므로, 데이터가 가장 얇은 곳에서 가장 크게 실패한다.
> **왜 중요한가.** 로보틱스 논문은 롤아웃 수십 번에 대해 부트스트랩 구간을 인용한다. 그런 구간의 양 끝이 표본이 실제로 낼 수 있는 값이고 눈금이 $1/n$이라는 것을 알아야, $[0.70,\ 1.00]$을 측정이 아니라 무지의 고백으로 읽게 된다.

**이진** 결과에서는 부트스트랩에 시뮬레이션이 아예 필요 없고, 한 번은 손으로 해 볼 값어치가 있다. E1c의 파일럿 시행 열 개에서 하나를 뽑으면 확률 $\hat p = 9/10$로 성공이 나오고 $n$번의 뽑기가 독립이므로, 복원추출 재표본은 모수 $\hat p$인 베르누이에서 뽑는 것과 *같고* 부트스트랩 분포는 정확히 이항이다.

$$\Pr\Big[\hat p^* = \frac{x}{n}\Big] = \binom{n}{x}\,\hat p^{\,x}\,(1-\hat p)^{\,n-x}$$

재표본 하나의 성공 수 $x$가 각각 확률 $\hat p$로 성공하는 독립 뽑기 $n$번을 세기 때문이다. $n = 10$, $\hat p = 0.9$이면:

| $x$ | $\hat p^* = x/10$ | $\Pr[\hat p^* = x/10]$ | 누적 |
|---:|---:|---:|---:|
| $\le 5$ | $\le 0.5$ | 0.0016 | 0.0016 |
| 6 | 0.6 | 0.0112 | 0.0128 |
| 7 | 0.7 | 0.0574 | 0.0702 |
| 8 | 0.8 | 0.1937 | 0.2639 |
| 9 | 0.9 | 0.3874 | 0.6513 |
| 10 | 1.0 | 0.3487 | 1.0000 |

2.5% 분위수는 누적 확률이 $0.025$에 닿는 가장 작은 값, 곧 누적 $0.0702$의 $x = 7$이고 97.5% 분위수는 $x = 10$이다. 그래서 파일럿의 백분위 부트스트랩 95% 구간은 $[0.70,\ 1.00]$이고, 이 구간의 성질 셋이 교훈이다.

**이산적이다.** 시행이 열 번이면 $0.1$의 배수만 나올 수 있어 어떤 구간도 95%에 정확히 앉지 못한다. 이 구간은 실제로 부트스트랩 분포의 $1 - 0.0128 = 98.7\%$를 담고, 여기서 $x = 7$을 빼면 $92.98\%$가 된다. **데이터에 갇혀 있다.** 위쪽 끝이 $1.00$인 것은 어떤 재표본도 본 것보다 잘할 수 없기 때문이고, 재표본의 $0.9^{10} = 0.349$는 하나뿐인 실패를 아예 건너뛴다. 그리고 **다른 두 구간이 아니다.** 같은 개수에 대한 정규근사, 곧 $\hat p$에 이항 표준오차의 $1.96$배를 더하고 빼는 구간(표준오차는 §3의 성공률 항목, $1.96$은 §4)은 $0.9 \pm 1.96\sqrt{0.9 \times 0.1/10} = 0.9 \pm 0.186 = [0.714,\ 1.086]$으로 축 밖으로 나간다.

**Wilson** 구간(점수 구간)은 질문을 뒤집는다. 자기 표준오차로 보았을 때 10번 중 9번이 놀랍지 않은 참 $p$를 모두 남기는데, 곧 $z=1.96$에서 $\lvert\hat p-p\rvert\le z\sqrt{p(1-p)/n}$이고, $p$에 대한 이차 부등식인 이것을 풀면 두 끝이
$$p_{\pm}=\frac{\hat p+\frac{z^2}{2n}}{1+\frac{z^2}{n}}\ \pm\ \frac{z}{1+\frac{z^2}{n}}\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}$$
이므로, $n=10$에서 중심은 $1.092/1.384=0.789$로 $0.9$에서 $\tfrac12$ 쪽으로 끌려오고 반폭은 $1.416\times0.1364=0.193$이어서 구간은 $[0.596,\ 0.982]$다. $[0,1]$ 안에 있으면서 아래쪽이 훨씬 넓다. 이 구간은 $[0,1]$을 결코 벗어나지 못한다. 검정에 쓰는 표준오차를 후보 $p$에서 계산하고 그 값이 $p=0$과 $p=1$에서 0으로 줄어들어, 양 끝 밖의 어떤 후보도 그럴듯해 보일 수 없기 때문이다. 10번 중 9번을 낼 법한 참 $p$가 무엇인지를 묻지, 그 열 개의 재표본 중 무엇이 그럴듯한지를 묻지 않는다.

**개수를 보고하라.** "90%"와 "9/10"은 같은 추정이지만 불확실성이 전혀 다르고, 독자가 이 계산을 다시 해 볼 수 있게 하는 것은 뒤쪽뿐이다.

**5. 시드 하나인가 넷인가: 같은 실험, 두 개의 주장.** E1c의 시드 기록에는 방법마다 실행이 넷 있으므로, 발표된 두 값은 뒤에 세 행이 더 있는 표의 한 행이다. §4의 표본 표준편차와 표준오차를 쓰면, 84, 88, 80, 76%인 우리 쪽은 $\bar x_A = 82.0$, $s_A = 5.16$이고, 72, 76, 80, 84%인 기존 방법은 $\bar x_B = 78.0$, $s_B = 5.16$이며, 각각 $\text{SE} = 5.16/\sqrt4 = 2.58$점이다. 평균의 차는 16점이 아니라 **4.0**점이다. *차이*에 구간을 붙이려면 두 표준오차를 합성해야 하고, 집단 크기가 $n$으로 같으면

$$\big(\bar x_A - \bar x_B\big) \pm t_{0.975,\,2n-2}\; s_p \sqrt{\tfrac1n + \tfrac1n}, \qquad s_p^2 = \frac{(n-1)s_A^2 + (n-1)s_B^2}{2n-2}$$

이고, 세 단계로 나온다. 첫째, 독립인 오차는 평균을 빼더라도 분산이 더해진다. 두 방법이 실행 간 분산 $\sigma^2$ 하나를 공유하면 $\operatorname{Var}(\bar x_A-\bar x_B)=\sigma^2/n+\sigma^2/n=\sigma^2\big(\tfrac1n+\tfrac1n\big)$이므로, 차이의 흩어짐은 어느 한쪽보다 크다. 둘째, 공유하는 $\sigma^2$는 합쳐서(pooling) 추정한다. §4의 $s^2$가 $n-1$로 나누는 것은 반복 실험에 걸친 평균이 정확히 $\sigma^2$가 되게 하려는 것이고, 따라서 각 집단의 편차제곱합 $(n-1)s^2$의 평균은 $(n-1)\sigma^2$다. 두 합을 더해 전체 $2n-2$로 나누면 그 평균도 $\sigma^2$가 된다. 그것이 $s_p^2$이고, 각 분산에 자유도만큼 가중치를 주는 이유다(집단 크기가 같으면 그냥 $s_A^2$와 $s_B^2$의 평균). 셋째, 각 집단이 자기 평균에 자유도를 하나씩 쓰므로, 실행 간 잡음이 가우시안이면 차이를 추정 표준오차로 나눈 값은 자유도 $2n-2$인 스튜던트 $t$를 따르고(§4), 그래서 $t_{0.975,\,2n-2}$를 쓴다. 두 분산이 뚜렷이 다르면 풀링을 버리는 Welch 판본([[02-foundations/probability|3. 확률 §6]])을 쓴다. 여기서는 $s_A = s_B$라 $s_p = 5.16$, 차이의 표준오차가 $5.16\sqrt{0.5} = 3.65$점, $t_{0.975,\,6} = 2.447$이므로

$$4.0 \pm 2.447 \times 3.65 = 4.0 \pm 8.9 = [-4.9,\ 12.9]$$

이고 구간이 0을 포함한다. 방법마다 시드 넷으로는 둘을 가를 수 없다. 헤드라인을 만들려고 조작한 것은 없다. $88 - 72 = 16$은 한 방법의 가장 좋은 시드와 다른 방법의 가장 나쁜 시드를 맞붙인 것이고, 두 숫자 모두 같은 정직한 기록 안에 있다. **시드 하나짜리 격차는 인쇄하기로 고른 시드의 통계량이다.** 같은 실행 여덟 개가 "16포인트 향상"도, "없는 것과 구별되지 않는 4포인트 차이"도 뒷받침하고, 독자가 어느 문장을 받을지는 개수와 시드 수를 인쇄했는지만이 결정한다.

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="방법마다 시드 넷: 우리는 84, 88, 80, 76퍼센트로 평균 82, 기존 방법은 72, 76, 80, 84로 평균 78; 발표된 쌍은 88 대 72로 16포인트 격차이지만 평균의 차는 4.0이고 95퍼센트 구간은 -4.9에서 12.9로 0을 포함한다">
  <line x1="150.0" y1="128.0" x2="530.0" y2="128.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="150.0" y1="128.0" x2="150.0" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="184.5" y1="128.0" x2="184.5" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="219.1" y1="128.0" x2="219.1" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="253.6" y1="128.0" x2="253.6" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="288.2" y1="128.0" x2="288.2" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="322.7" y1="128.0" x2="322.7" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="357.3" y1="128.0" x2="357.3" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="391.8" y1="128.0" x2="391.8" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="426.4" y1="128.0" x2="426.4" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="460.9" y1="128.0" x2="460.9" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="495.5" y1="128.0" x2="495.5" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="530.0" y1="128.0" x2="530.0" y2="132.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="184.5" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">72</text>
  <text x="253.6" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">76</text>
  <text x="322.7" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">80</text>
  <text x="391.8" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">84</text>
  <text x="460.9" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">88</text>
  <text x="530.0" y="144.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">92</text>
  <text x="340.0" y="158.0" font-size="12" fill="currentColor" text-anchor="middle">에피소드 25번 중 성공 (%)</text>
  <text x="138.0" y="48.0" font-size="12" fill="currentColor" text-anchor="end">우리</text>
  <line x1="150.0" y1="44.0" x2="530.0" y2="44.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <circle cx="391.8" cy="44.0" r="5" fill="currentColor"/>
  <circle cx="460.9" cy="44.0" r="5" fill="currentColor"/>
  <circle cx="322.7" cy="44.0" r="5" fill="currentColor"/>
  <circle cx="253.6" cy="44.0" r="5" fill="currentColor"/>
  <line x1="357.3" y1="31.0" x2="357.3" y2="57.0" stroke="currentColor" stroke-width="2"/>
  <text x="357.3" y="27.0" font-size="11" fill="currentColor" text-anchor="middle">평균 82.0</text>
  <text x="138.0" y="96.0" font-size="12" fill="currentColor" text-anchor="end">기존 방법</text>
  <line x1="150.0" y1="92.0" x2="530.0" y2="92.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <circle cx="184.5" cy="92.0" r="5" fill="currentColor"/>
  <circle cx="253.6" cy="92.0" r="5" fill="currentColor"/>
  <circle cx="322.7" cy="92.0" r="5" fill="currentColor"/>
  <circle cx="391.8" cy="92.0" r="5" fill="currentColor"/>
  <line x1="288.2" y1="79.0" x2="288.2" y2="105.0" stroke="currentColor" stroke-width="2"/>
  <text x="288.2" y="75.0" font-size="11" fill="currentColor" text-anchor="middle">평균 78.0</text>
  <circle cx="460.9" cy="44.0" r="10" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3 2"/>
  <circle cx="184.5" cy="92.0" r="10" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3 2"/>
  <text x="548" y="70" font-size="11" fill="currentColor" text-anchor="end">발표된 쌍: 88 대 72</text>
  <line x1="150.0" y1="214.0" x2="530.0" y2="214.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="150.0" y1="214.0" x2="150.0" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="150.0" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">−10</text>
  <line x1="213.3" y1="214.0" x2="213.3" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="213.3" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">−5</text>
  <line x1="276.7" y1="214.0" x2="276.7" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="276.7" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <line x1="340.0" y1="214.0" x2="340.0" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="340.0" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">5</text>
  <line x1="403.3" y1="214.0" x2="403.3" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="403.3" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">10</text>
  <line x1="466.7" y1="214.0" x2="466.7" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="466.7" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">15</text>
  <line x1="530.0" y1="214.0" x2="530.0" y2="218.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="530.0" y="230.0" font-size="11" fill="currentColor" fill-opacity="0.8" text-anchor="middle">20</text>
  <line x1="276.7" y1="195.0" x2="276.7" y2="214.0" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="138.0" y="198.0" font-size="12" fill="currentColor" text-anchor="end">평균의 차</text>
  <text x="138.0" y="212.0" font-size="12" fill="currentColor" text-anchor="end">(포인트)</text>
  <line x1="214.2" y1="202.0" x2="440.5" y2="202.0" stroke="currentColor" stroke-width="2.4"/>
  <line x1="214.2" y1="197.0" x2="214.2" y2="207.0" stroke="currentColor" stroke-width="1.6"/>
  <line x1="440.5" y1="197.0" x2="440.5" y2="207.0" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="327.3" cy="202.0" r="4" fill="currentColor"/>
  <text x="214.2" y="192.0" font-size="11" fill="currentColor">4.0 ± 8.9 = [−4.9, 12.9]: 0을 포함</text>
  <path d="M479.3 196.0 L485.3 202.0 L479.3 208.0 L473.3 202.0 Z" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="479.3" y="192.0" font-size="11" fill="currentColor" text-anchor="middle">16: 발표된 격차</text>
</svg>

E1c의 시드 기록이다. 레시피를 맞춘 채 방법마다 시드 넷을 돌렸다. 발표된 쌍, 곧 우리 쪽 최고 시드 $88\%$와 기존 방법의 최저 시드 $72\%$는 16포인트 격차를 만들지만, 평균은 $82.0\%$와 $78.0\%$이고 그 차이의 95% 구간 $[-4.9,\ 12.9]$포인트는 0을 포함한다.

### 5. 논문에서 경계할 평가 함정

결과 표는 산수가 맞아도 오도할 수 있다. 보여 준 실행을 골라냈거나, 비교를 더 쉬운 체제에서 했거나, 배포 때는 없을 정보를 방법에 건넸을 때다. 아래 함정마다 E1의 숫자로 이름을 붙여, 논문에서 알아볼 수 있게 한다.

- **체리피킹**: 정성적 그림은 최고 실행을 보여준다 — *중앙값* 롤아웃은 어떤지 물어라. E1c가 그 산수다. 발표된 $0.88$은 시드 넷 중 최고이고 중앙값 시드는 $0.82$이므로, 헤드라인은 평균의 옷을 입은 최댓값이다.
- **통계적 vs 실질적 유의성**: 오차 막대 겹침만으로 유의성을 판정할 수 없다 — 막대가 무엇인지(표준편차? 표준오차? 신뢰구간?), 실행 횟수, 짝지음 여부를 확인하라. +0.3%p는 노이즈일 수도, (포화된 벤치마크에서는) 의미 있을 수도 있다; 시드 하나의 +5%p는 운일 수 있다. 분산부터 확인하라 — E1c의 숫자가 시드 하나로는 16점, 넷으로는 $4.0 \pm 8.9$점이다.
  - 둘은 다른 질문이다. **통계적 유의성**은 참 차이가 0이라면 관측된 차이가 나오기 어려운지를 묻는다. 0.05 같은 정해 둔 수준 아래의 p-값이다([[02-foundations/probability|3. 확률 §6]]). **실질적 유의성**은 차이가 과제에 의미 있을 만큼 큰지를 묻고, 효과 크기와 그 신뢰구간을 미리 정한 문턱에 대 보아 판단한다. 앞의 것은 $n$이 커지면 무시할 만한 효과에서도 "유의하다" 쪽으로 기울고, 뒤의 것은 $n$에 따라 바뀌지 않는다. 논문에 둘 다 필요한 이유다. 실질적 문턱을 시행 수로 바꾸는 두 숫자, 효과 크기와 검정력은 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계]]의 계산 절에서 RS1로 정의하고 계산한다.
- **오라클 정보**: 배포 환경에는 없을 실측 상태, 완벽한 캘리브레이션, 사람의 리셋을 조용히 쓰고 있지 않은가? E1a의 정답, 곧 "실제 균열" 60장의 행이 그런 것이다. 누군가 벽을 열어야 나오는 행이고, 현장의 감지기는 그 행을 결코 가질 수 없다.
- **개루프 vs 폐루프 평가**: 오프라인에서 좋은 궤적을 예측하는 것(개루프)은 피드백과 복합 오차 아래에서 실행하는 것(폐루프)보다 훨씬 쉽다 — 로보틱스 수치는 같은 체제 안에서만 비교 가능하다. E1a와 E1c의 파일럿이 한 시스템의 두 체제다. 저장된 이미지 1,000장을 채점한 것과 로봇이 실제로 찾아간 패널 10장이고, 어떤 산수도 앞의 수치를 뒤의 수치로 바꿔 주지 않는다.
  - *입력 상태가 어디서 오는지로 정의된다.* **개루프** 평가는 정책 $\pi$에 기록된 데이터셋의 상태를 넣고 출력을 기록된 행동과 비교해 채점한다. 예컨대 기록 쌍 $(o_i, a_i)$ $N$개에 대해 $\frac{1}{N}\sum_{i=1}^{N} \lVert \pi(o_i) - a_i \rVert$이므로, 정책의 실수가 다음에 보는 것을 바꾸지 않는다. **폐루프** 평가는 $\pi$의 행동을 실행하므로 다음 관측을 그 행동이 만들고, 결과(롤아웃 성공률)를 채점한다. 개루프 오차가 낮다고 폐루프 성공이 따라오지는 않는다. 폐루프에서는 작은 오차가 정책을 데이터셋에 없던 상태로 옮기기 때문이다. 공변량 이동이다([[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §1]]).
- **에피소드 정의**: "성공률"은 시간 제한, 리셋 조건, 성공의 정의에 의존한다 — 두 논문의 80%는 다른 것을 의미할 수 있다. E1c의 $9/10$도 그 문장을 쓰기 전에는 정의되지 않는다. 플래그하고 도달하면 성공인가, 플래그하고 도달해서 제한 시간 안에 촬영까지 해야 성공인가? 계산 예제의 부트스트랩은 이 정의가 먼저 고정해 줘야 하는 숫자 위의 정확한 산수다.
- **벤치마크 포화**: 천장 근처의 벤치마크는 그 벤치마크의 버릇에 과적합하는 것을 보상한다 — 거기서의 이득이 가장 일반화되지 않는다. E1a의 정확도 97%가 구조적으로 그 천장이다. 그중 94%는 "정상"이라고만 답해도 공짜로 나온다.

### 6. 학습 레시피, 어휘로서

실험 절은 모델을 어떻게 학습시켰는지에 한 문단을 쓰는데, 그 용어들을 이 위키의 최적화
페이지는 다루지 않는다. 우리가 그 실행을 재현하는 것은 아니다 — 그러나 이것들이 보고된
숫자가 *방법*의 성질인지 *레시피*의 성질인지를 가르고, 이 중 하나를 바꾼 절제 실험은 자기가
주장하는 것을 비교하고 있지 않다. 그런 레시피를 공유 클러스터에서 돌리는 법 — 배치 작업, 재시작의 사슬, 체크포인트와 그것을 쓰는 간격 — 은 [[02-foundations/tools/gpu-clusters|12.7 GPU 클러스터 §4–§7]]이다.

| 용어 | 무엇인가 | 왜 주장에 등장하는가 |
|---|---|---|
| **학습률 스케줄** | 학습 도중 스텝 크기가 변한다 — 흔히 선형 **warmup** 뒤 **cosine decay**를 쓰며, 설정된 최소 학습률은 0일 수도 비영 값일 수도 있다 | 마지막 학습률이 정확도 끝자리 몇 점을 좌우하므로 "같은 구조, 다른 스케줄"은 공정한 비교가 아니다. 스케줄이 애초에 왜 warmup으로 시작하는지, 그 정점이 배치 크기에 따라 어떻게 움직이는지는 [[03-deep-learning/foundations/training-at-scale\|1.3 대규모 학습 §9]]에 있다 |
| **Weight decay / AdamW** | AdamW는 가중치를 $w \leftarrow w(1-\eta\lambda)$로 직접 줄인다. 적응 스텝과 *분리*되어 있고, 손실 안의 L2 항이 아예 아니다 | [[02-foundations/probability\|3. 확률 §4]]의 가우시안 사전 해석은 L2 페널티이고, 그것이 weight decay와 같아지는 것은 **SGD에서**다. Adam에서는 적응 분모가 그것을 좌표마다 왜곡하며, AdamW가 존재하는 이유가 바로 그것이다. 갱신식은 [[02-foundations/optimization\|4. 최적화 §3]]에서 풀어 둔다 |
| **그래디언트 누적** | 여러 번의 순전파 그래디언트를 모아 한 번 optimizer step을 밟는다 | 논문의 "배치 크기 4096"이 실은 8 × 512를 누적한 것일 수 있고, 그것이 진짜 배치 4,096과 같아지는 것은 손실이 예제에 대한 합이고 optimizer step이 같을 때뿐이다. 손실 정의와 구현을 확인한다. 대조 손실이라는 예외는 아래 *더 깊이* 메모에 있다 |
| **혼합 정밀도**(fp16/bf16) | 16비트로 계산하되 가중치의 fp32 마스터 사본을 둔다. **fp16은 손실 스케일링이 추가로 필요하고, bf16은 필요 없다** | 활성값 메모리를 절반으로 줄이고 처리량을 올리므로, 모델이 들어간다거나 더 빨리 학습된다는 주장은 정밀도를 밝혀야 한다. 16비트가 줄이지 못하는 것과 bf16에 손실 스케일링이 필요 없는 이유는 아래 *더 깊이* 메모에 있다 |
| **가중치 EMA** | 파라미터의 느리게 움직이는 평균을 유지하고, 살아 있는 가중치가 아니라 *그것을* 평가한다 | 여러 벤치마크에서 공짜로 얻는 소수점 몇 자리. 확산 모델은 거의 예외 없이 쓰고(DDPM: 감쇠 0.9999. 부록 수치다), 정책 논문은 제각각이라 **코드**에서야 드러나는 일이 많다 — Diffusion Policy는 논문에 쓰지 않은 채 설정 파일에서 쓴다. [[01-canonical-papers/notes/2-computer-vision/dino\|DINO]]의 EMA *교사*와는 다르다 — 그쪽은 타깃 네트워크이지 평가 요령이 아니다 |
| **초기화** | Xavier/He 스케일링이 깊이에 걸쳐 활성 분산을 안정시킨다 | 정규화 층이 있는 지금은 결정적인 경우가 드물지만, 정규화 없이 학습하는 논문은 이것을 명시한다. 각 스케일이 어디서 나오는지 — 층마다의 분산 인수를 1로 유지하는 것 — 는 [[03-deep-learning/foundations/training-at-scale\|1.3 대규모 학습 §1]]에 있다 |

**초록이 인용할 두 행짜리 표.** E1c에서 발표된 두 행을, 레시피 어휘가 있는 여기에 다시 싣는다:

| 방법 | 성공 | 시행 | 학습 |
|---|---:|---:|---|
| 우리 | 0.88 | 25 | 새 스케줄, 시드 하나 |
| 기존 SOTA | 0.72 | 25 | 새 스케줄, 시드 하나 |

16포인트 격차가 주장이다. 그 주장은 $n=25$와 방법마다 시드 하나에 말없이 의존한다. *학습* 열은 아래 경고의 점검을 통과한다. 두 행 모두 새 스케줄로 학습했으므로 이 격차는 레시피 불일치가 아니다. 그런데도 격차는 살아남지 못한다. E1c에는 같은 레시피로 돌린 방법마다 나머지 시드 셋이 있고, 시드 넷씩으로 보면 $4.0 \pm 8.9$점이 남아 그 구간이 0을 포함하므로, 16점 중 12점은 방법이 아니라 어느 시드를 골랐느냐였다. 기존 방법이 2021년 레시피를 그대로 썼다면 같은 16점 안에 레시피 격차까지 숨어 있었을 것이고, 그것은 새 스케줄로 다시 학습시켜야만 드러난다. 별도로 $22/25$ 대 $18/25$는 얇은 이항이다.

> [!note]- 더 깊이 · Deeper
> **레시피 용어의 수식, 그리고 표 뒤의 세부.**
>
> **Warmup과 cosine decay.** 학습률 스케줄은 스텝 $t$의 함수 $\eta_t$다. 처음 $T_w$스텝 동안 선형 warmup, 그 뒤 마지막 스텝 $T$까지 $\eta_{\max}$에서 $\eta_{\min}$으로 cosine decay를 하면
> $$\eta_t = \eta_{\max}\,\frac{t}{T_w} \ \ (t \le T_w), \qquad \eta_t = \eta_{\min} + \tfrac12\big(\eta_{\max} - \eta_{\min}\big)\Big(1 + \cos\frac{\pi\,(t - T_w)}{T - T_w}\Big) \ \ (t > T_w)$$
> 이므로 학습률이 0에서 올라간 뒤 반 주기 코사인을 따라 $\eta_{\min}$까지 내려간다. warmup 없이 $\eta_{\max} = 10^{-3}$, $\eta_{\min} = 0$, $T = 10{,}000$이면 스텝 2,500에서 $8.54 \times 10^{-4}$, 스텝 5,000에서 $5 \times 10^{-4}$, 끝에서 $0$이다. 1,000스텝 warmup은 스텝 250에서 $2.5 \times 10^{-4}$다. warmup은 Adam의 초기 2차 모멘트 추정(제곱 그래디언트의 이동 평균, [[02-foundations/optimization|4. 최적화 §3]])과 큰 배치 학습을 안정화할 수 있고, 특정 post-norm 레시피(LayerNorm을 각 residual 서브레이어 뒤에 두는 방식, [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]])는 warmup이 없으면 실패할 수 있다.
>
> **Weight decay(AdamW 형태).** Adam이 재척도하기 전에 그래디언트에 $\lambda w$를 더하는 것이 아니라, 적응 그래디언트 스텝과 *별도로* 매 스텝 각 가중치에 $(1 - \eta\lambda)$를 곱한다. SGD는 좌표별 재척도를 하지 않으므로 둘은 순수 SGD에서만 일치한다. 산수는 §2, 전체 갱신식은 [[02-foundations/optimization|4. 최적화 §3]]에 있다.
>
> **그래디언트 누적.** 예제 $B = KB_\mu$개의 배치를 $B_\mu$개씩 microbatch $K$개로 나누고, 각 microbatch의 평균 그래디언트 $g_k$를 구해 다음으로 한 번 스텝을 밟는다.
> $$g = \frac{1}{K}\sum_{k=1}^{K} g_k$$
> microbatch 크기가 같고 손실이 예제에 대한 합이므로 전체 배치 평균 그래디언트와 같다. $8 \times 512$는 명목 배치 4,096이다. **반례:** 대조 손실은 예제에 대한 합이 *아니다*. 각 예제의 항이 같은 배치의 다른 예제들, 곧 [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 손실 같은 대조 손실이 짝이 아니라고 점수 매겨야 하는 negatives에 의존하므로, microbatch를 넘어 특징을 모으지 않으면 누적은 예제당 negative를 4,095개가 아니라 511개만 준다. 배치 통계와 확률 연산도 같지 않을 수 있다.
>
> **혼합 정밀도.** 16비트 형식은 범위를 메모리와 맞바꾼다. fp16의 최댓값은 65,504, 가장 작은 양수는 약 $6 \times 10^{-8}$이다. bf16은 fp32의 지수 8비트를 유지하므로 범위가 약 $3.4 \times 10^{38}$까지 가고, 대신 가수 정밀도가 거칠다. bf16이 손실 스케일링을 버릴 수 있고 큰 모델이 16비트에서 안정적으로 학습되는 이유가 바로 이것이다. **손실 스케일링**은 역전파 전에 손실에 $S$를 곱하고 갱신 전에 그래디언트를 $S$로 나누어, 작은 그래디언트가 fp16에서 살아남게 한다. 그래디언트 $10^{-8}$은 fp16에서 $0$이 되지만, $S = 1024$면 약 $1.02 \times 10^{-5}$로 올라가 fp16이 표현할 수 있다. 16비트가 줄이지 못하는 것은 파라미터마다 붙는 모델 상태다. Adam에서는 16비트 가중치와 그래디언트, fp32 마스터 사본, Adam의 두 모멘트로 파라미터당 2 + 2 + 4 + 4 + 4 = 16바이트이고, fp32 Adam의 4 + 4 + 4 + 4와 같다([[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §4–§5]]).
>
> **가중치 EMA.** 옵티마이저 스텝마다 갱신하는 두 번째 사본 $\bar\theta$다.
> $$\bar\theta_t = \beta\,\bar\theta_{t-1} + (1 - \beta)\,\theta_t$$
> 그래서 $\bar\theta$는 대략 최근 $1/(1-\beta)$스텝을 평균하고, 오래된 가중치는 기하급수적으로 할인된다. DDPM의 $\beta = 0.9999$면 그 창이 10,000스텝이고 한 가중치의 영향은 약 6,931스텝 뒤에 절반이 된다. 평가하고 공개하는 것은 이 평균 사본이다.
>
> **초기화.** 각 가중치를 평균 0, 층의 fan-in $n_{\text{in}}$과 fan-out $n_{\text{out}}$으로 정한 분산으로 뽑아서, 활성 분산이 깊이에 따라 폭발하지도 사라지지도 않게 한다. Xavier(tanh류 활성함수용)는 $\operatorname{Var}(w) = 2/(n_{\text{in}} + n_{\text{out}})$, He(입력의 절반을 0으로 만드는 ReLU용)는 $\operatorname{Var}(w) = 2/n_{\text{in}}$을 쓴다. $n_{\text{in}} = 512$인 ReLU 층의 표준편차는 $\sqrt{2/512} = 0.0625$다.

> [!warning] 방법 차이로 위장한 레시피 차이
> 이 문헌에서 가장 흔한 불공정 비교는, 새 방법은 현대적 레시피로 학습시키고 베이스라인은
> 원래 레시피로 재현하는 것이다. 격차를 믿기 전에 **베이스라인의 스케줄·옵티마이저·정밀도·
> 에폭 예산이 제안 방법과 일치하는지 확인하라** — 그리고 일치할 때는 정직한 논문들이 그렇다고
> 명시한다는 점도 함께 기억하라.

> [!tip] 더 깊이 · Going deeper
> 이 페이지는 읽는 쪽 절반이다. 하는 쪽 절반은 [[06-research-practice/experimental-design-reproducibility|실험 설계와 재현성]]이고, 거기서 같은 개념들이 직접 내려야 하는 결정이 된다. 아래 깔린 통계는 Murphy의 무료 교재 [*Probabilistic Machine Learning: An Introduction*](https://probml.github.io/pml-book/book1.html) 4~6장.

### 스스로 점검

1. 어떤 모델이 test 정확도로 최적 체크포인트를 골랐다. 무엇이 잘못됐고, 보고 수치는 어느
   방향으로 편향되는가?
2. Precision 0.9 / recall 0.3인 균열 감지기: 무엇을 놓치고, 건설 현장에서 그것이 언제
   용인 가능한가?
3. FID는 왜 픽셀이 아니라 *특징*(이미지 분류용 CNN인 Inception의 임베딩)에서 계산하는가?
4. VLA 논문의 "unseen 지시 76% 성공" — 믿기 전에 물어야 할 질문 세 개를 들어라.
5. 배포 문턱값에서 E1b의 정밀도는 $0.75$다. 이것을 현장 정밀도의 추정으로 읽으면 왜
   틀리고, E1b에서 계산한 숫자 중 믿을 수 있는 것은 무엇인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 테스트가 검증 집합 역할을 해버렸다 — 보고 수치는 위로(낙관적으로) 편향되고, 실제 일반화 성능은 그보다 낮다.
> 2. 진짜 균열의 70%를 놓친다(재현율 0.3). 1차 스크리닝이나 유일한 안전 관문으로는 불가하다. 표시하지 않은 것은 점검에 아예 올라가지 않기 때문이다. 모든 패널을 여전히 점검하는 체계 위에서 우선순위를 정하는 보조 수단으로만 용인 가능하다: 표시는 믿을 만하므로(정밀도 0.9) 먼저 처리하고, 놓친 것은 정규 점검이 잡는다.
> 3. 픽셀 거리는 지각 품질과 무관하다(한 픽셀 평행이동에도 크게 벌점) — Inception 특징 공간이 의미적 유사성을 반영하기 때문에 특징 분포 거리로 잰다.
> 4. ① 몇 회 시행이고 분산은 얼마인가 ② "unseen"의 정의는(새 물체? 새 지시문? 새 장면?) ③ 어떤 베이스라인 대비이며 실패 사례 분석이 있는가.
> 5. E1b는 점수 범위를 덮도록 고른 것이라 일곱 장 중 셋이 균열, 곧 기저율 43%인데 현장은 6%다. 정밀도는 양성 *예측*에 조건화하므로 기저율을 따라 움직이고(계산 예제 3번), $0.75$는 그 조각만을 설명한다. 믿을 수 있는 것은 AUC $0.917$이다. 균열 패널의 점수가 정상 패널의 점수에 대해 어떻게 정렬되는지에만 의존하고, 두 군을 어떤 비율로 섞어도 그 정렬은 그대로이기 때문이다.

### 과제 · Problem set

Tier B. **E1** 위의 손 유도. 이 페이지와 선수 지식, 위에 고정한 대상만 쓴다. 계산 예제와는 문턱값도, 기저율도, 파일럿 길이도 다르다.

1. **그리기.** E1b의 점수 일곱 개로 문턱값 $\tau = 0.65$에서, 그리고 $\tau = 0.45$에서 $2\times2$ 혼동 행렬을 그리고 두 동작점을 ROC 축 위에 찍어라. 점마다 정밀도를 적는다. 두 점 사이의 계단은 점수가 $0.45$와 $0.65$ 사이인 패널에 대해 무엇을 말하는가?
2. **유도.** $\tau = 0.65$의 점을 그대로 들고 패널의 1%가 균열인 현장으로 옮겨, 패널 1,000장에 대한 정밀도를 구하라. 그다음 TPR을 고정한 채 그 기저율에서 정밀도 $0.5$를 주는 FPR을 찾고, 감지기가 몇 배 좋아져야 하는지 말하라.
3. **해석.** E1c의 현장 파일럿을 패널 10장 더 돌려 20번 중 18번 성공으로 끝났다고 하자. $\hat p$는 여전히 $0.9$다. (가) 계산 예제가 시행 10번에 대해 한 것처럼 새 백분위 부트스트랩을 이항분포에서 읽어라. $[0.70,\ 1.00]$의 어느 끝이 움직였고 어느 끝이 움직이지 않았으며, 왜인가? (나) $n=20$에서 정규근사 구간과 Wilson 구간을 다시 계산하라. 심사자가 "성공률에 오차 막대"를 요구한다. §4의 세 양 중 무엇을, 세 구간 중 무엇을 그 행에 실어야 하고, 독자가 그 답을 검산하려면 옆에 무엇이 더 인쇄되어 있어야 하는가?

> [!note]- 그리는 법 · How to draw it
> - 문턱값마다 $2\times2$ 상자 하나. 열에는 *예측*, 행에는 *실제*를 붙인다. 점수가 $\tau$에 닿으면 플래그되고, 네 칸을 합치면 E1b의 패널 일곱 장이 모두 들어가야 한다.
> - 정밀도가 나누는 열과 재현율이 나누는 행을 서로 다른 모양으로 두른다. 두 테두리가 만나는 칸이 TP다.
> - TN은 칠하고 옆에 두 비 모두 이 칸을 쓰지 않는다고 적는다.
> - ROC 축은 가로 FPR, 세로 TPR, 둘 다 0에서 1까지이고 우연 수준 대각선을 긋는다. 두 동작점을 같은 축에 찍고 점마다 정밀도를 옆에 적는다.
> - 정밀도는 ROC 그림의 좌표가 아니다. 점을 다른 기저율로 옮기면 점은 그대로이고 정밀도만 바뀐다. 계산 예제는 자기 점에 대해 $0.80$ 아래에 $0.27$을 적고, 2번은 $\tau=0.65$의 점에 대해 같은 일을 한다.
> - 구간 띠는 $\tau$에 의존하지 않는다. 3번을 위해 다시 그린다면 0에서 1까지의 가로축에 $\hat p=0.9$를 찍고, 그 위로 20번 중 18번에 대한 정규근사, Wilson, 백분위 부트스트랩 구간을 쌓되 그림의 시행 10번짜리 구간을 옆에 흐리게 두고, 정규근사가 여전히 축을 벗어나는 지점을 표시한다.
> - 제대로 그린 띠는 계산 예제 4번이 기대는 질문에 답한다. 시행 몇 번짜리 성공률 밑에 셋 중 무엇을 인쇄해도 되는가.

> [!tip]- 정답 · Solutions
> 1. $\tau = 0.65$에서 플래그되는 것은 균열 $0.90$·$0.80$과 정상 $0.70$이다. $TP = 2$, $FN = 1$, $FP = 1$, $TN = 3$이므로 정밀도 $2/3 = 0.667$, 재현율 $2/3 = 0.667$, 점은 $(\text{FPR},\ \text{TPR}) = (0.25,\ 0.667)$이다. $\tau = 0.45$에서는 균열 $0.60$과 정상 $0.50$이 합류해 $TP = 3$, $FN = 0$, $FP = 2$, $TN = 2$, 정밀도 $3/5 = 0.600$, 재현율 $1.000$, 점은 $(0.50,\ 1.00)$이다. $[0.45,\ 0.65)$ 구간에는 균열 하나와 정상 하나가 정확히 하나씩 있으므로, 그 띠를 건너면 마지막 균열을 오경보 하나의 값으로 산다. 재현율은 $0.667 \to 1.000$, FPR은 $0.25 \to 0.50$이고 재현율이 오르는 동안 정밀도는 *내려간다*. 계산 예제의 맞바꿈을 패널 일곱 장에 그린 것이다.
> 2. 1,000장의 1%면 균열 10장, 정상 990장이다. 점을 고정하면 $TP = 0.667 \times 10 = 6.67$, $FP = 0.25 \times 990 = 247.5$이므로 정밀도는 $6.67/254.17 = 0.026$이다. 일곱 장 중 셋이 균열이던 E1b에서 계산한 $0.667$의 25분의 1이다. 정밀도 $0.5$를 얻으려면 오경보가 $FP = TP = 6.67$까지 내려가야 하므로 $\text{FPR} = 6.67/990 = 0.0067$, 곧 재현율을 유지한 채 거짓양성률이 37배 좋아져야 한다. 그 배수가 "배포 기저율 위에서 명시된 재현율에 대한 정밀도를 요구하라"의 구체적 내용이다.
> 3. (가) $n=20$, $\hat p=0.9$에서도 부트스트랩 분포는 이항이다. 누적 확률이 $x=14$에서 $0.0113$, $x=15$에서 $0.0432$이므로 2.5% 분위수는 $x=15$, 곧 $\hat p^*=0.75$이고, 97.5% 분위수는 여전히 $x=20$이다. 구간은 $[0.75,\ 1.00]$이다. 아래쪽 끝은 더 촘촘해진 $1/20$ 눈금으로 한 칸 올라갔다. 위쪽 끝은 움직일 수 없다. 실패 둘을 모두 건너뛴 재표본은 $1.00$이 되는데 그런 재표본이 $0.9^{20}=0.122$로, 위쪽 분위수가 잘라 낼 수 있는 $2.5\%$보다 훨씬 많기 때문이다. $\hat p$가 같은 채 시행을 늘리면 백분위 부트스트랩은 아래쪽에서만 좁아지고, 성공만 나온 재표본의 몫 $\hat p^{\,n}$이 $0.025$보다 큰 동안 위쪽 끝은 $1.00$에 머문다. (나) 정규근사: $\text{SE}=\sqrt{0.9\times0.1/20}=0.067$이므로 $0.9\pm0.131=[0.769,\ 1.031]$로 여전히 축 밖으로 나간다. Wilson: 중심 $0.996/1.192=0.836$, 반폭 $1.644\times0.0831=0.137$이므로 $[0.699,\ 0.972]$이고, 너비는 시행 10번일 때의 약 $1/\sqrt2$다($0.273$ 대 $0.386$). $s$도 SE도 아니다. 둘은 *실행* 사이의 흩어짐을 말하는데 파일럿은 베르누이 시행 20번짜리 실행 하나라 실행 간 흩어짐이 없다. 그 행에는 Wilson $[0.699,\ 0.972]$를 실어야 한다. 부트스트랩은 자기 데이터 위를 보지 못하고 정규근사는 축을 벗어난다. 그리고 옆에는 $k$와 $n$이 — "90%"가 아니라 "18/20"이 — 그리고 §5의 에피소드 정의가 인쇄되어 있어야 한다. 그 둘이 없으면 구간을 다시 계산할 수도, 해석할 수도 없다.

### 실험을 읽는 것에서 설계하는 것으로

연구 질문·통제된 로봇 실험·실패 진단·재현성·peer review는 [[06-research-practice/index|Research Practice]]로 이어진다.

논문이 나온 뒤 불공정한 비교를 찾는 것보다 수집 전에 막는 것이 어려워 이 전환이 필요하다. 장면 공유의 우려를 현장 단위 분할로, 숨은 리셋의 우려를 사전 개입 규칙으로 바꾼다. **여기서 얻는 독법.** 구체적 불확실성 하나를 연구실무로 가져가 답할 기록을 설계한다. 다음 단계는 결과에 따라 내 주장이 바뀔 수 있는 실험이다.

### 출처 · Sources

- E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association* 22(158):209–212 (1927) — 계산 예제 4번의 점수 구간. 이 위키의 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사]]도 같은 문헌을 인용한다.
- K. P. Murphy, [*Probabilistic Machine Learning: An Introduction*](https://probml.github.io/pml-book/book1.html) (MIT Press, 2022), 4–6장 — §2–§5 아래 깔린 통계.
- §1, §2, §6에서 이름을 부른 논문은 이 위키의 노트로 읽는다. [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/3-vlm/clip|CLIP]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]], [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/vgg|VGG]], [[01-canonical-papers/notes/1-foundations/scaling-laws|스케일링 법칙]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]], [[01-canonical-papers/notes/2-computer-vision/dino|DINO]].
- E1은 교육용 대상이다. 그 개수와 점수는 이 페이지를 위해 지어낸 것이고, 거기서 나온 모든 숫자는 여기서 직접 계산했다.
