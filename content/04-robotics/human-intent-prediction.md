---
title: 23. Human Intent & Trajectory Prediction
tags: [robotics, hri, prediction, human, construction]
study-depth: Working
wiki-support: Working
depth-goal: "Separate intent from trajectory, read the early-versus-accurate trade-off correctly, and evaluate a prediction claim including its calibration and its class imbalance."
mastery-when: "Raise to Mastery when a predictor or its uncertainty is a contribution of the thesis rather than a component."
---

## English

*The end of group J. Stands on [[04-robotics/hri-safety|11. HRI & Safety]], [[04-robotics/human-pose-gaze|21]], [[04-robotics/video-action-understanding|20]] and probability.
Where timing and calibration matter more than accuracy, because the prediction is an interface to a decision rather than an answer.*

A robot sharing space with a person acts on a guess about what the person will do. That guess is the interface between perception and every downstream decision — and it is worth exactly as much as its *timing* and its *calibration*, not its accuracy.

> [!info] Depth target
> Distinguish intent classification from trajectory forecasting and know which one a paper solved; read a time-to-event curve; explain why a well-calibrated 0.7 is more useful than a poorly calibrated 0.9; identify the standard evaluation traps in pedestrian-intent benchmarks; and map the formulation onto human–robot collaboration.

> [!note] Prerequisites
> [[02-foundations/probability|Probability]] · [[02-foundations/ml-practice|9. ML Practice & Evaluation]] (AUC, ROC, precision–recall, F1) · [[04-robotics/video-action-understanding|20. Video Representation & Action Understanding]] · [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]] · [[04-robotics/hri-safety|11. Human–Robot Interaction & Safety]]

> [!note] First pass · 처음이라면
> Read the running object and the five derivations on it, then §1 — intent classification and trajectory forecasting are different problems and papers do not always say which they solved — then §3, then §4. Calibration is where the research actually is, which is why §4 comes before the survey material. Second pass: §2 and §5, the cue cascade and the base rate; §6 for the best-of-$k$ trajectory metrics; §7 for the move from roads to shared workspaces; §8 and §9 are the checklists to keep beside a paper.

### Running object · 이 페이지의 대상

Prediction is evaluated on a log, not on a plant, so no object from [[02-foundations/lab-plants|0.6 Lab Plants]] fits. This page freezes its own log — **I20**, one afternoon of a crossing-intent system on a mobile base — and never changes its numbers afterwards. It has three parts, one for each thing the page has to evaluate.

**Part 1 — twenty judgements.** Each case $i$ is a probability $\hat p_i$ that a worker will enter the robot's path within the next 2 s, and the outcome $y_i \in \{0,1\}$ that followed. The cases are listed in increasing $\hat p$; the index is a label, not a time.

| case | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\hat p_i$ | 0.05 | 0.10 | 0.10 | 0.15 | 0.20 | 0.25 | 0.25 | 0.30 | 0.45 | 0.50 |
| $y_i$ | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |

| case | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\hat p_i$ | 0.50 | 0.55 | 0.65 | 0.70 | 0.70 | 0.75 | 0.85 | 0.90 | 0.90 | 0.95 |
| $y_i$ | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |

Nine of the twenty events occurred, so the base rate on this log is $\bar p = 9/20 = 0.45$. That is far higher than a real deployment's few percent — the log is the subset the system flagged as worth judging, which is exactly the population a calibration claim is about, and §5 handles what happens when you put it back on the full frame stream.

**Part 2 — one trajectory.** Case 20 also carries a path, sampled at 1 Hz on the ground plane, in metres. The three observed positions are $(-2.00, 0)$, $(-1.00, 0)$, $(0.00, 0)$; the three true future positions and the model's three predicted ones are:

| step | $t+1$ | $t+2$ | $t+3$ |
|---|---|---|---|
| truth $x_k$ | $(1.00,\ 0.00)$ | $(2.00,\ 0.00)$ | $(3.00,\ 0.00)$ |
| model $\hat x_k$ | $(1.00,\ 0.30)$ | $(2.30,\ 0.40)$ | $(3.60,\ 0.80)$ |

**Part 3 — the early-versus-accurate curve, and the platform it has to serve.** Recall at a fixed false-positive rate $\alpha = 0.05$, as a function of time to event. Read $\mathrm{Recall}_{\mathrm{FPR}=0.05}(\Delta)$ as: set the alarm threshold so that $5\%$ of the cases where no one enters are flagged anyway, then count the fraction of real entries that were already flagged $\Delta$ seconds before they happened ($\Delta = T - t$, the time left to the event; §3 states the construction and why it is reported as a curve):

| $\Delta$ (s) | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 |
|---|---:|---:|---:|---:|---:|
| $\mathrm{Recall}_{\mathrm{FPR}=0.05}(\Delta)$ | 0.92 | 0.84 | 0.72 | 0.60 | 0.48 |

The platform is a mobile base at $v = 1.5\ \mathrm{m/s}$ with a maximum deceleration $a = 1.5\ \mathrm{m/s^2}$ and a perception-to-brake latency $t_{\mathrm{lat}} = 0.45$ s, and the safety case requires recall $\ge 0.75$ at that same $\alpha$.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 482" style="max-width:100%;height:auto" role="img" aria-label="Intent-prediction picture: the reliability diagram of the twenty I20 forecasts in five bins with their gaps to the diagonal, the recall-against-lead-time curve with the usable horizon 1.375 s falling 75 ms short of the 1.45 s the base needs, and the case-20 trajectory with its three displacement errors">
  <text x="16" y="24" font-size="12" fill="currentColor" font-weight="600">1. reliability diagram</text>
  <rect x="58" y="58" width="192" height="192" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" fill="none"/>
  <line x1="96.4" y1="250" x2="96.4" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="134.8" y1="250" x2="134.8" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="173.2" y1="250" x2="173.2" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="211.6" y1="250" x2="211.6" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="58" y1="250" x2="250" y2="58" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7" stroke-dasharray="5 3"/>
  <line x1="58" y1="250" x2="58" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="250" x2="58" y2="250" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="58" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.0</text>
  <text x="51" y="254" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.0</text>
  <line x1="96.4" y1="250" x2="96.4" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="211.6" x2="58" y2="211.6" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="96.4" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.2</text>
  <text x="51" y="215.6" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.2</text>
  <line x1="134.8" y1="250" x2="134.8" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="173.2" x2="58" y2="173.2" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="134.8" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.4</text>
  <text x="51" y="177.2" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.4</text>
  <line x1="173.2" y1="250" x2="173.2" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="134.8" x2="58" y2="134.8" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="173.2" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.6</text>
  <text x="51" y="138.8" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.6</text>
  <line x1="211.6" y1="250" x2="211.6" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="96.4" x2="58" y2="96.4" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="211.6" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.8</text>
  <text x="51" y="100.4" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.8</text>
  <line x1="250" y1="250" x2="250" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="58" x2="58" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="250" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.0</text>
  <text x="51" y="62" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">1.0</text>
  <text x="154" y="282" font-size="11" fill="currentColor" text-anchor="middle">forecast p̂ (bin mean)</text>
  <text x="28" y="48" font-size="11" fill="currentColor">observed frequency</text>
  <rect x="63.2" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="101.6" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="140" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="178.4" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="216.8" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <text x="244.2" y="223.1" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">bars: n = 4 in each bin</text>
  <line x1="77.2" y1="202" x2="77.2" y2="230.8" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="77.2" cy="202" r="4" stroke="none" fill="currentColor"/>
  <circle cx="106" cy="202" r="4" stroke="none" fill="currentColor"/>
  <circle cx="154" cy="154" r="4" stroke="none" fill="currentColor"/>
  <line x1="192.4" y1="154" x2="192.4" y2="115.6" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="192.4" cy="154" r="4" stroke="none" fill="currentColor"/>
  <line x1="230.8" y1="106" x2="230.8" y2="77.2" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="230.8" cy="106" r="4" stroke="none" fill="currentColor"/>
  <text x="77.2" y="193" font-size="11" fill="currentColor" text-anchor="middle">0.15</text>
  <text x="113" y="216" font-size="11" fill="currentColor">0.00</text>
  <text x="161" y="168" font-size="11" fill="currentColor">0.00</text>
  <text x="198.4" y="169" font-size="11" fill="currentColor">0.20</text>
  <text x="230.8" y="123" font-size="11" fill="currentColor" text-anchor="middle">0.15</text>
  <text x="300" y="24" font-size="12" fill="currentColor" font-weight="600">2. time-to-event</text>
  <rect x="330" y="58" width="210" height="192" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" fill="none"/>
  <line x1="330" y1="250" x2="330" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="330" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="382.5" y1="250" x2="382.5" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="382.5" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.0</text>
  <line x1="435" y1="250" x2="435" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="435" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.5</text>
  <line x1="487.5" y1="250" x2="487.5" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="487.5" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2.0</text>
  <line x1="540" y1="250" x2="540" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="540" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2.5</text>
  <line x1="326" y1="250" x2="330" y2="250" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="254" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.4</text>
  <line x1="326" y1="186" x2="330" y2="186" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="190" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.6</text>
  <line x1="326" y1="122" x2="330" y2="122" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="126" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.8</text>
  <line x1="326" y1="58" x2="330" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="62" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">1.0</text>
  <text x="435" y="282" font-size="11" fill="currentColor" text-anchor="middle">time to event Δ (s)</text>
  <text x="300" y="48" font-size="11" fill="currentColor">recall at FPR 0.05</text>
  <line x1="330" y1="138" x2="540" y2="138" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" stroke-dasharray="5 3"/>
  <text x="536" y="132" font-size="11" fill="currentColor" text-anchor="end">required recall 0.75</text>
  <path d="M330 83.6 L382.5 109.2 L435 147.6 L487.5 186 L540 224.4" stroke="currentColor" stroke-width="1.9" fill="none" stroke-linejoin="round"/>
  <circle cx="330" cy="83.6" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="382.5" cy="109.2" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="435" cy="147.6" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="487.5" cy="186" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="540" cy="224.4" r="3.4" stroke="none" fill="currentColor"/>
  <line x1="421.9" y1="138" x2="421.9" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <line x1="429.8" y1="60" x2="429.8" y2="250" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 2.5"/>
  <circle cx="421.9" cy="138" r="4.4" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="415.9" y="211.6" font-size="11" fill="currentColor" text-anchor="end">Δ* = 1.375 s</text>
  <text x="435.8" y="74" font-size="11" fill="currentColor">t<tspan dy="3.1" font-size="8.6">stop</tspan><tspan dx="3.1" dy="-3.1">+ t</tspan><tspan dy="3.1" font-size="8.6">lat</tspan><tspan dx="3.1" dy="-3.1">= 1.45 s</tspan></text>
  <line x1="421.9" y1="235.6" x2="429.8" y2="235.6" stroke="currentColor" stroke-width="1.2"/>
  <text x="435.8" y="239.6" font-size="11" fill="currentColor">−0.075 s</text>
  <text x="435.8" y="223.6" font-size="11" fill="currentColor">misses by 75 ms</text>
  <text x="16" y="314" font-size="12" fill="currentColor" font-weight="600">Part 2 from above (m): observed, true and predicted</text>
  <line x1="19.8" y1="404" x2="445.4" y2="404" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.35"/>
  <path d="M194.6 404 L270.6 381.2 L369.4 373.6 L468.2 343.2" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.8" stroke-dasharray="5 3" stroke-linejoin="round"/>
  <circle cx="42.6" cy="404" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="118.6" cy="404" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="194.6" cy="404" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="270.6" cy="404" r="4.2" stroke="none" fill="currentColor"/>
  <circle cx="346.6" cy="404" r="4.2" stroke="none" fill="currentColor"/>
  <circle cx="422.6" cy="404" r="4.2" stroke="none" fill="currentColor"/>
  <rect x="266.6" y="377.2" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <rect x="365.4" y="369.6" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <rect x="464.2" y="339.2" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <line x1="270.6" y1="404" x2="270.6" y2="381.2" stroke="currentColor" stroke-width="1.5"/>
  <line x1="346.6" y1="404" x2="369.4" y2="373.6" stroke="currentColor" stroke-width="1.5"/>
  <line x1="422.6" y1="404" x2="468.2" y2="343.2" stroke="currentColor" stroke-width="3.4"/>
  <text x="277.6" y="400.6" font-size="11" fill="currentColor">0.30</text>
  <text x="365" y="396.8" font-size="11" fill="currentColor">0.50</text>
  <text x="452.4" y="381.6" font-size="11" fill="currentColor">1.00 (FDE)</text>
  <circle cx="20" cy="424" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="30" y="428" font-size="11" fill="currentColor">observed</text>
  <circle cx="87.2" cy="424" r="4.2" stroke="none" fill="currentColor"/>
  <text x="97.2" y="428" font-size="11" fill="currentColor">true</text>
  <rect x="124.2" y="420" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <text x="138.2" y="428" font-size="11" fill="currentColor">model</text>
  <text x="16" y="452" font-size="11" fill="currentColor" fill-opacity="0.9">ECE = 0.2 × (0.15 + 0 + 0 + 0.20 + 0.15) = 0.100; the top two bins sit below the diagonal (overconfident).</text>
  <text x="16" y="468" font-size="11" fill="currentColor" fill-opacity="0.9">ADE = (0.30 + 0.50 + 1.00) / 3 = 0.60 m and FDE = 1.00 m; constant velocity hits (1, 0), (2, 0), (3, 0) exactly.</text>
</svg>

The log I20 in three views. The reliability diagram bins the twenty forecasts four to a bin, with gaps to the diagonal of $0.15$, $0$, $0$, $0.20$ and $0.15$, so $\mathrm{ECE} = 0.100$ and the top two bins sit below the diagonal, overconfident; the time-to-event curve crosses the required recall of $0.75$ at $\Delta^{*} = 1.375$ s, $75$ ms short of the $t_{\mathrm{stop}} + t_{\mathrm{lat}} = 1.45$ s the base needs. Beside it, case 20's trajectory from above: the model's three displacement errors, $0.30$, $0.50$ and $1.00$ m, give $\mathrm{ADE} = 0.60$ m and $\mathrm{FDE} = 1.00$ m, while constant velocity hits the true path exactly.

### Worked on I20 · I20로 한 번 끝까지

**1. What calibration is, before any score.**

> [!info] Definition — calibration
> A **property of a probabilistic forecaster**, not a score and not accuracy: the forecaster is
> calibrated when its stated probability equals the conditional frequency of the event among the
> cases where it stated that probability. Four conditions make it precise. It is conditional on
> the **forecast value**, not marginal. It must hold at **every** value in the range, not on
> average. It is a statement about a **distribution of cases**, so a single case is neither
> calibrated nor not. And it constrains only honesty, not **sharpness**: how far the forecasts
> move away from the base rate is a separate virtue.
> $$\mathbb{P}\big(y = 1 \mid \hat p = p\big) = p \quad \text{for every } p \in [0,1]$$
> where $\hat p$ is the forecast, $y$ the binary outcome, and the probability is over the case
> distribution the forecaster is deployed on.
> **Example.** In I20 the four cases near $0.50$ (cases 9–12) average $\hat p = 0.50$ and the
> event occurred in two of them, a frequency of $0.50$. Calibrated, in that bin.
> **Non-example 1 — accuracy.** Thresholding I20 at $0.5$ classifies 14 of 20 correctly, an
> accuracy of $70\%$, and that number would not change if every $\hat p$ were replaced by $0.99$
> or $0.51$. Accuracy cannot see confidence.
> **Non-example 2 — AUC.** AUC depends only on the **ranking**, so any strictly increasing
> transform of the forecasts leaves it untouched. Square every $\hat p_i$ in I20: AUC stays at
> $0.7172$ to the last digit while the five-bin ECE below moves from $0.100$ to $0.177$ and the
> Brier score from $0.226$ to $0.249$. A paper reporting only AUC has reported nothing about
> calibration.
> **Non-example 3 — the constant forecaster.** Saying $0.45$ on all twenty cases is *perfectly*
> calibrated and useless: zero sharpness, $\mathrm{AUC} = 0.5$. Calibration alone is never the claim.
> **Why it matters.** Downstream is a decision rule that weighs a probability against a cost. If
> $0.7$ does not mean $0.7$, the product $\text{cost} \times \text{probability}$ is not a number
> anyone can act on, and §5's precision arithmetic silently becomes fiction.

**2. The Brier score on I20.**

> [!info] Definition — Brier score
> A **proper scoring rule** for binary forecasts: the mean squared error between the stated
> probability and the realised outcome, a dimensionless number in $[0,1]$, lower better. Three
> conditions: the outcome is coded $0/1$; the forecast is a probability, not a logit or a score;
> and "proper" means the expected score is uniquely minimised by reporting your honest belief,
> so no forecaster gains by shading toward confidence or toward the middle.
> $$\mathrm{BS} = \frac{1}{N}\sum_{i=1}^{N}\big(\hat p_i - y_i\big)^2$$
> where $N$ is the number of cases, $\hat p_i$ the $i$-th forecast and $y_i \in \{0,1\}$ its
> outcome.
> **Example.** I20 scores $0.2258$, worked below.
> **Non-example.** It is not $1 - \text{accuracy}$, which is $0.30$ here. Nor is a Brier of
> $0.2258$ "good" on its own: the constant base-rate forecaster scores $\bar p(1-\bar p) = 0.2475$
> on the same log, so all the model's ranking and all its confidence together buy $0.0218$.
> **Why it matters.** It is the one number that a forecaster cannot improve by lying, so it is the
> reference against which the next definition's blind spot becomes visible.

Sum the twenty squared residuals. Grouping them the way the bins will group them keeps the arithmetic checkable:

| cases | squared residuals | subtotal |
|---|---|---:|
| 1–4 | $0.05^2 + 0.10^2 + 0.10^2 + 0.85^2$ | 0.7450 |
| 5–8 | $0.20^2 + 0.25^2 + 0.25^2 + 0.70^2$ | 0.6550 |
| 9–12 | $0.45^2 + 0.50^2 + 0.50^2 + 0.55^2$ | 1.0050 |
| 13–16 | $0.35^2 + 0.70^2 + 0.30^2 + 0.75^2$ | 1.2650 |
| 17–20 | $0.15^2 + 0.10^2 + 0.90^2 + 0.05^2$ | 0.8450 |
| | **total** | **4.5150** |

$$\mathrm{BS} = \frac{4.5150}{20} = 0.2258$$

Now the reference, because a squared error means nothing until something else has been squared too. The constant forecaster that always says the base rate scores $\bar p(1-\bar p) = 0.45 \times 0.55 = 0.2475$, so the **Brier skill score** is

$$\mathrm{BSS} = 1 - \frac{\mathrm{BS}}{\bar p(1-\bar p)} = 1 - \frac{0.2258}{0.2475} = 0.088$$

**Eight point eight percent.** The model beats "say the base rate every time" by that much, and one case is responsible for most of what is left: case 19 said $0.90$ and the event did not happen, contributing $0.81$ of the $4.515$ total — **18% of the whole score from one judgement out of twenty.** That fragility is not a flaw in the object; it is what $N = 20$ means, and it is why calibration claims need calibration sets of hundreds.

**3. The five-bin ECE, and the choice that is not the model's.**

> [!info] Definition — expected calibration error
> A **scalar summary of the reliability diagram**: the occupancy-weighted mean absolute gap
> between observed frequency and mean forecast, dimensionless, in $[0,1]$. It is an *estimator*,
> and four conditions have to be fixed before it has a value: a **binning scheme** — how many
> bins, and equal-width or equal-mass; the gap taken between each bin's **observed frequency**
> and that bin's **mean forecast** (not the bin's midpoint); the **absolute value applied after
> the bin average**, so opposite-signed errors inside one bin cancel before they are ever seen;
> and bins **weighted by occupancy**, so a bin holding one case counts once.
> $$\mathrm{ECE} = \sum_{b=1}^{B} \frac{n_b}{N}\,\Big| \mathrm{freq}(b) - \overline{\hat p}(b) \Big|$$
> where $B$ is the number of bins, $n_b$ the count in bin $b$, $N$ the total, $\mathrm{freq}(b)$
> the observed event frequency in that bin and $\overline{\hat p}(b)$ the mean forecast in it.
> **Example.** I20 with five equal-width bins: $0.100$, worked below.
> **Non-example — ECE is not a property of the model.** The same twenty forecasts and the same
> twenty outcomes give $0.055$ with two bins and $0.270$ with ten. Coarse bins average
> opposite-signed gaps into nothing; fine bins leave single cases defining a bin, where the only
> possible frequencies are $0$ and $1$. **An ECE quoted without its binning is unreadable**, and
> the direction of the bias is not even fixed in advance. A second non-example: $\mathrm{ECE} = 0$
> does not mean useful. The constant $0.45$ forecaster has $\mathrm{ECE} = 0$ exactly, because all
> twenty cases land in one bin whose mean and frequency are both $0.45$.
> **Why it matters.** It is the scalar every "uncertainty-aware" paper reports, and the binning is
> the line those papers most often leave out.

Bin the twenty cases into five equal-width bins. Each bin happens to hold four cases, so every weight $n_b/N$ is $4/20 = 0.2$:

| bin | cases | $n_b$ | mean $\hat p$ | observed freq | $\lvert \text{gap} \rvert$ |
|---|---|---:|---:|---:|---:|
| $[0.0, 0.2)$ | 1–4 | 4 | 0.10 | 1/4 = 0.25 | 0.15 |
| $[0.2, 0.4)$ | 5–8 | 4 | 0.25 | 1/4 = 0.25 | 0.00 |
| $[0.4, 0.6)$ | 9–12 | 4 | 0.50 | 2/4 = 0.50 | 0.00 |
| $[0.6, 0.8)$ | 13–16 | 4 | 0.70 | 2/4 = 0.50 | 0.20 |
| $[0.8, 1.0]$ | 17–20 | 4 | 0.90 | 3/4 = 0.75 | 0.15 |

$$\mathrm{ECE} = 0.2\,\big(0.15 + 0.00 + 0.00 + 0.20 + 0.15\big) = 0.2 \times 0.50 = 0.100$$

Read the sign column, not just the total, because the signs are the diagnosis. The bottom bin's frequency exceeds its forecast and the top two bins' frequencies fall short of theirs: the model is pushed toward both extremes relative to what happens, which is textbook **overconfidence** and exactly what temperature scaling in §4's table is for. And notice what the total conceals: a model that said $0.70$ and was right half the time is reported by the same $0.100$ as a model with three smaller errors spread differently.

**4. ADE and FDE on Part 2.**

> [!info] Definition — ADE and FDE
> Two **lengths in metres**, both built from the Euclidean displacement between a predicted and a
> true position at matching timestamps. **ADE** (average displacement error) averages that
> displacement over the whole forecast horizon; **FDE** (final displacement error) is the same
> displacement at the last step only. Conditions: a stated observation window and a stated horizon
> $H$; **one** predicted trajectory, not a set — best-of-$k$ over samples is $\mathrm{minADE}_k$
> and a different object (§6); positions compared **step by step in the same frame** at the same
> sampling rate.
> $$\mathrm{ADE} = \frac{1}{H}\sum_{k=1}^{H}\big\lVert \hat x_k - x_k \big\rVert_2, \qquad \mathrm{FDE} = \big\lVert \hat x_H - x_H \big\rVert_2$$
> where $x_k$ is the true position at step $k$, $\hat x_k$ the predicted one, and $H$ the horizon
> in steps.
> **Example.** Part 2 gives $\mathrm{ADE} = 0.60$ m and $\mathrm{FDE} = 1.00$ m.
> **Non-example.** ADE is not the distance between the two endpoints — that is FDE. FDE is not the
> worst error over the horizon either; the two coincide here only because this error happens to
> grow monotonically, and a model that overshoots early and recovers has its maximum in the
> middle. Neither is a distance measured *along* a path.
> **Why it matters.** Their ratio is the shape of the error over the horizon — $1.00/0.60 = 1.67$
> here — which no single number reports, and a planner's constraint lives at the horizon, not at
> its average.

The per-step displacements come out of three right triangles, so the arithmetic is exact:

- $t+1$: $\hat x_1 - x_1 = (0.00,\ 0.30)$, $\lVert\cdot\rVert = 0.30$ m;
- $t+2$: $(0.30,\ 0.40)$, $\lVert\cdot\rVert = \sqrt{0.09 + 0.16} = 0.50$ m;
- $t+3$: $(0.60,\ 0.80)$, $\lVert\cdot\rVert = \sqrt{0.36 + 0.64} = 1.00$ m.

$$\mathrm{ADE} = \frac{0.30 + 0.50 + 1.00}{3} = \frac{1.80}{3} = 0.60\ \mathrm{m}, \qquad \mathrm{FDE} = 1.00\ \mathrm{m}$$

Now run the baseline the whole Schöller critique in Sources is about. The three observed positions are $1.00$ m apart on a straight line at 1 Hz, so a **constant-velocity** extrapolation is $x_t + k\,(1.00, 0)$, which is $(1,0), (2,0), (3,0)$ — the truth, exactly. On this walk, $\mathrm{ADE}_{\mathrm{CV}} = \mathrm{FDE}_{\mathrm{CV}} = 0$.

The object is built that way on purpose, and the point is not that constant velocity is always exact. The point is that **the published $\mathrm{ADE} = 0.60$ m does not tell you it was beaten by arithmetic**, and no benchmark table is obliged to. The problem set turns the pedestrian and the ranking reverses; that reversal is the reading, not either number.

**5. The usable horizon $\Delta^{*}$ against what the platform needs.** The usable horizon $\Delta^{*}$ is the longest lead time at which the curve still meets its requirement (§3 defines it for any operating metric). Part 3's requirement is recall $\ge 0.75$. The curve is $0.84$ at $\Delta = 1.0$ s and $0.72$ at $\Delta = 1.5$ s, so it crosses between them; interpolating linearly, the fraction of the interval used is $(0.84 - 0.75)/(0.84 - 0.72) = 0.09/0.12 = 0.75$, so

$$\Delta^{*} = 1.0 + 0.75 \times (1.5 - 1.0) = 1.375\ \mathrm{s}$$

The platform's requirement is a separate calculation with no model in it. Braking from $v$ at constant $a$ takes $t_{\mathrm{stop}} = v/a$ and covers $v^2/2a$, so

$$t_{\mathrm{stop}} = \frac{1.5}{1.5} = 1.00\ \mathrm{s}, \qquad d_{\mathrm{stop}} = \frac{1.5^2}{2 \times 1.5} = 0.75\ \mathrm{m}, \qquad \Delta_{\mathrm{req}} = t_{\mathrm{stop}} + t_{\mathrm{lat}} = 1.00 + 0.45 = 1.45\ \mathrm{s}$$

$\Delta^{*} = 1.375\ \mathrm{s} < \Delta_{\mathrm{req}} = 1.45\ \mathrm{s}$. **The system misses by 75 milliseconds**, and nothing in a headline AUC, a Brier score or an ECE would have said so — those three numbers are all computed with $\Delta$ averaged away.

The useful move is to ask what the shortfall costs, because it is the platform side that is cheap to change. Solving $v/a + t_{\mathrm{lat}} \le \Delta^{*}$ for $v$:

$$v \le a\big(\Delta^{*} - t_{\mathrm{lat}}\big) = 1.5 \times (1.375 - 0.45) = 1.39\ \mathrm{m/s}$$

so capping the base at $1.39\ \mathrm{m/s}$ — a $7\%$ speed reduction — makes this exact predictor sufficient. Shaving $75$ ms off $t_{\mathrm{lat}}$ does the same. Either is a smaller intervention than a better model, and neither is visible from the benchmark table. **A predictor is not slow or fast; it is slow or fast relative to a deceleration and a latency that belong to the robot.**

### 1. Two different problems

| | Intent prediction | Trajectory forecasting |
|---|---|---|
| Output | discrete latent decision — cross / not cross, hand over / withdraw | continuous future positions $\hat{x}_{t+1:t+H}$ |
| Ground truth | an event that did or did not occur | a recorded path |
| Metric | accuracy, AUC, F1 — **conditioned on time-to-event** | ADE / FDE, minADE over $k$ samples |
| Failure mode | confident wrong class | plausible but wrong mode |
| What it feeds | a discrete decision (stop, warn, yield) | a continuous plan (cost map, MPC constraint) |

In the right-hand column, ADE (average displacement error) is the Euclidean distance between predicted and true positions averaged over the forecast horizon, FDE (final displacement error) is that distance at the last step only — both are defined in full, with their conditions and non-examples, on I20 above — and minADE over $k$ samples keeps the best of $k$ sampled futures (§6).

They are often solved by the same network and reported in the same paper, but they are not the same claim. **"We predict pedestrian intent" and "we forecast pedestrian trajectories" answer different questions and fail differently.** A trajectory model with low ADE can still be useless if it never places mass on the crossing mode; an intent classifier can be right about crossing and useless for planning because it says nothing about *where*.

### 2. The observable cue cascade

Intent is latent. What is measurable, roughly in order of lead time:

| Cue | Lead | Observable at range? | Source |
|---|---|---|---|
| Gaze | longest | **no** beyond a few metres | [[04-robotics/human-pose-gaze\|21. §4]] |
| Head / body orientation | long | yes | [[04-robotics/human-pose-gaze\|21. §4–§5]] |
| Gait change, deceleration | medium | yes, from a tracked box | [[04-robotics/human-pose-gaze\|21. §5]] |
| Proximity to boundary (curb, machine envelope) | medium | yes, if the boundary is in the same ground frame (below) | [[04-robotics/hri-safety\|11.]], its hazard boundary |
| Trajectory curvature toward target | short | yes | §1 above |
| Contact / entry | zero | yes | too late |

Proximity is a relation between the person and the scene, not something read off the person. It is the signed distance from the person's tracked ground position $x$ to the boundary, positive outside; for a machine envelope modelled as a circle of radius $R_h$ about the base $x_{\mathrm{base}}$, it is $d = \lVert x - x_{\mathrm{base}}\rVert - R_h$, the same boundary [[04-robotics/hri-safety|11. HRI & Safety]] measures every separation distance from ($R_h = 2.25$ m for its P2 cell). Computing it takes scene geometry — two inputs beyond the person's track: the boundary itself in the robot's ground frame, from a site map or from the machine's own reach, and the person's ground position in that frame, from a depth sensor or from the ray through the foot of a tracked box meeting a known ground plane ([[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §1]], the pinhole model).

This is the same cascade as [[04-robotics/egocentric-perception|22. §4]], seen from outside instead of from the head. **The design decision in any intent system is which rung you commit to,** because that fixes both the lead time and the ceiling on reliability.

> [!warning] The "subtle cue" trap
> The cues that carry the most intent information are the ones that stop being resolvable first. A study that establishes gaze as predictive using close-range or instrumented data has not shown that a vehicle or robot camera can use it. Always state the distance at which the cue was measured and the distance at which the system must work.

### 3. Early versus accurate is the actual research object

Let $T$ be the event time. Performance must be reported as a function of time-to-event $\Delta = T - t$:

$$\text{AUC}(\Delta), \qquad \text{Recall}_{\mathrm{FPR}=\alpha}(\Delta)$$

Read it as a curve rather than a score, because reporting one number at one $\Delta$, or averaging over all $\Delta$, hides the deployment tradeoff. AUC summarizes ranking across thresholds; an action needs a chosen operating point, calibration, and costs. For a deployed operating metric, define the usable horizon $\Delta^\*$ — in other words, the longest lead time at which the chosen metric still clears its requirement:

$$\Delta^{*} = \max\{\Delta : \text{operating-metric}(\Delta) \geq \text{requirement}\}$$

A system whose $\Delta^*$ is shorter than the actuator's stopping time is a detector wearing a predictor's name.

> [!example] Worked example — required lead time · 계산 예제 — 필요한 선행 시간
> A vehicle at 30 km/h ($8.3\,\mathrm{m/s}$) needs 1.2 s to brake plus 0.3 s of pipeline latency: 1.5 s of required lead. At the same allowed false-positive rate, suppose model A meets the required recall only to 1.15 s while model B meets it to 2.15 s (the figure below). A does not meet **this braking requirement at this operating point**, despite a better peak AUC. Compare operating-point $\Delta^*$ with required lead time; AUC alone cannot make the braking decision.

<svg viewBox="0 0 560 285" style="max-width:100%;height:auto" role="img" aria-label="recall at a fixed false-positive rate against time before the event, with the required recall and the lead time the platform requires">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="60" y1="190" x2="504" y2="190"/><line x1="60" y1="190" x2="60" y2="36"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="148" y1="190" x2="148" y2="195"/><line x1="236" y1="190" x2="236" y2="195"/><line x1="324" y1="190" x2="324" y2="195"/><line x1="412" y1="190" x2="412" y2="195"/><line x1="500" y1="190" x2="500" y2="195"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.45" stroke-dasharray="4 3">
    <line x1="60" y1="123.3" x2="504" y2="123.3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.75" stroke-dasharray="6 4">
    <line x1="324" y1="46" x2="324" y2="190"/>
  </g>
  <path d="M 60.0 63.3 L 130.4 73.3 L 200.8 90.0 L 262.4 123.3 L 324.0 146.7 L 412.0 166.7 L 500.0 180.0" fill="none" stroke="currentColor" stroke-width="1.8" opacity="0.9"/>
  <path d="M 60.0 100.0 L 130.4 103.3 L 200.8 106.7 L 271.2 108.3 L 324.0 110.0 L 412.0 113.3 L 438.4 123.3 L 500.0 146.7" fill="none" stroke="currentColor" stroke-width="1.8" opacity="0.9" stroke-dasharray="7 3"/>
  <g fill="currentColor"><circle cx="262.4" cy="123.3" r="4"/><circle cx="438.4" cy="123.3" r="4"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="150" y="58">model A</text>
    <text x="150" y="96">model B</text>
    <text x="64" y="137" font-size="9.5" opacity="0.85">required recall</text>
    <text x="330" y="42" font-size="9.5" opacity="0.85">required lead, 1.5 s</text>
    <text x="258" y="147" text-anchor="end" font-size="10">&#916;*&#7488;</text>
    <text x="446" y="115" font-size="10">&#916;*&#7495;</text>
    <text x="54" y="44" text-anchor="end" font-size="9.5">1.0</text><text x="54" y="127" text-anchor="end" font-size="9.5">0.75</text><text x="54" y="177" text-anchor="end" font-size="9.5">0.6</text>
    <text x="60" y="206" text-anchor="middle" font-size="9.5">0</text><text x="148" y="206" text-anchor="middle" font-size="9.5">0.5</text><text x="236" y="206" text-anchor="middle" font-size="9.5">1.0</text><text x="324" y="206" text-anchor="middle" font-size="9.5">1.5</text><text x="412" y="206" text-anchor="middle" font-size="9.5">2.0</text><text x="500" y="206" text-anchor="middle" font-size="9.5">2.5</text>
    <text x="282" y="222" text-anchor="middle" font-size="9.5">time before the event &#916; (s)</text>
    <text x="14" y="112" font-size="9.5">recall @ FPR=α</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="243">Model A has the better headline number and cannot be used here: its usable</text>
    <text x="20" y="259">horizon &#916;* = 1.15 s falls short of the 1.5 s this platform needs, while model B</text>
    <text x="20" y="275">holds the required recall out to 2.15 s. Compare &#916;*, not peak performance.</text>
  </g>
</svg>

### 4. Calibration — why this is the thesis-relevant part

A predictor that outputs probabilities is only useful downstream if those probabilities mean something. Calibration asks:

$$\mathbb{P}\big(y = 1 \mid \hat{p} = p\big) \;\overset{?}{=}\; p$$

Among all cases where the model said 0.7, did the event occur 70% of the time? Deep classifiers are routinely **overconfident**, and the standard fixes are cheap:

| Tool | What it gives | Cost |
|---|---|---|
| Reliability diagram, ECE | a picture and a scalar of miscalibration | free, diagnostic only |
| Temperature scaling | recalibrated probabilities from a held-out set | one parameter |
| **Conformal prediction** | a set/interval with a **distribution-free coverage guarantee** under exchangeability | a held-out calibration set |

ECE (expected calibration error) is the scalar behind the diagram: bin the predictions by $\hat p$, take each bin's gap between the observed event frequency and its mean $\hat p$, and average those gaps weighted by how many cases fall in each bin. It is worked on I20 above, where the same twenty forecasts give $0.100$ with five bins and $0.270$ with ten, so **ask a paper for its binning before you compare two ECEs.** The sign pattern of I20's bins is the overconfidence this row diagnoses. Temperature scaling divides the logits by one scalar $T$ fitted on held-out data. A larger $T$ flattens the softmax ([[02-foundations/calculus-backprop|2. Calculus & Backprop §6]]), which pulls overconfident probabilities toward uniform without changing which class ranks first: logits $(2, 0)$ give 0.88 at $T = 1$ and 0.73 at $T = 2$.

Conformal prediction deserves emphasis because the mathematics is elementary — exchangeability (the calibration cases and the new case are equally likely to arrive in any order; i.i.d. draws satisfy it, but it is a weaker assumption) plus a quantile — and its set-valued output can support a defer policy. The usual guarantee is **marginal coverage over exchangeable cases**, not a 90% probability for this individual scene or every subgroup. A set containing both `crossing` and `not crossing` still needs an explicit action rule, such as slow down or ask for help. See [[04-robotics/hri-safety|11. HRI & Safety]].

> [!example] Worked example · 계산 예제
> **Building a conformal interval.** On 10 held-out pedestrians, the distances (m) between the predicted and true position 2 s ahead are 0.2, 0.3, 0.35, 0.4, 0.5, 0.55, 0.6, 0.7, 0.9, 1.4. For 90% coverage ($\alpha = 0.1$), split conformal takes the $\lceil (n+1)(1-\alpha) \rceil = \lceil 11 \times 0.9 \rceil = 10$th smallest residual, here 1.4 m. So for a new pedestrian the output is a disc of radius 1.4 m around the predicted point, which contains the true position in at least 90% of exchangeable cases.
>
> **The reading this gives you.** With only 10 calibration cases the rule picks the largest residual, so one unusual pedestrian sets the radius. A tight interval therefore needs enough calibration data from the deployment distribution.

**A calibrated 0.7 supports a decision rule. An uncalibrated 0.9 does not.**

### 5. Class imbalance and the base rate

Most pedestrians near a road do not cross in the next two seconds; most workers near a machine do not enter its envelope. Positive rates of a few percent are normal, with two consequences:

- **Accuracy is meaningless.** A constant "no" predictor scores 95%+. Report AUC, precision–recall (not ROC alone, which is optimistic under imbalance), and the operating point actually used.
- **Precision at the deployed threshold is the whole story.** A warning system with 20% precision produces four false alarms per true one, and will be ignored or disabled by the workers it is meant to protect. Alarm fatigue is a system failure mode, not a human failing.

> [!example] Worked example — base rates · 계산 예제 — 기저율
> **Why a 90% detector gets switched off.** Suppose a crossing-intent detector achieves a 90%
> true-positive rate at a 5% false-positive rate, and the event it predicts — a worker entering
> the robot's path within the next 2 s — is true in 2% of the frames it judges. Then
>
> $$\text{precision} = \frac{0.90 \times 0.02}{0.90 \times 0.02 + 0.05 \times 0.98} = \frac{0.0180}{0.0670} = \mathbf{26.9\%}$$
>
> Seven of every ten stops are false. At one decision per second over an 8-hour shift that is
> 28,800 judgements, of which $0.98 \times 28{,}800 \times 0.05 = \mathbf{1{,}411}$ are false
> alarms — roughly three per minute. No crew leaves that system enabled.
>
> **What it would take.** To reach 90% precision at the same 2% base rate, solve
> $0.90 \times 0.02 = 0.90\,(0.90 \times 0.02 + \text{FPR} \times 0.98)$ for FPR: **0.2%**. The
> false-positive rate has to fall by a factor of 25, and within realistic true-positive rates (0.8–1.0) the TPR shifts that requirement only proportionally —
> the false-positive rate is the lever.
>
> **The reading this gives you.** ROC curves and AUC hide this completely, because both are
> independent of the base rate. When an intent paper reports AUC on a balanced dataset and the
> deployment is 2% positive, the reported number and the operational number are answering
> different questions. Look for precision at a stated recall, on the deployment base rate — and
> if the paper does not give one, you can compute it yourself from its ROC point and the rate
> its own setting implies.

### 6. Trajectory forecasting, briefly

When the output is a path rather than a decision, the headline metric of this literature is a best-of-$k$ version of ADE and FDE.

> [!info] Definition — $\mathrm{minADE}_k$ and $\mathrm{minFDE}_k$
> Two **lengths in metres**, the best-of-$k$ versions of ADE and FDE: the model draws $k$ sampled
> futures for one observed history, and only the sample closest to the truth is scored. Four
> conditions. The $k$ samples come from **one forecaster for one history**, and $k$ is part of the
> name: $\mathrm{minADE}_5$ and $\mathrm{minADE}_{20}$ are different quantities. The minimum is
> over **whole trajectories** — each sample's ADE is computed over the full horizon and then the best
> sample is kept, not the best sample at each step. $\mathrm{minADE}_k$ and $\mathrm{minFDE}_k$ each
> take **their own** minimum, so they may be scored on different samples. And **no probability
> enters**: whatever weights the model puts on its samples are ignored, and a benchmark figure is
> this per-case number averaged over the test cases.
> $$\mathrm{minADE}_k=\min_{m=1,\dots,k}\frac{1}{H}\sum_{t=1}^{H}\big\lVert\hat x^{(m)}_t-x_t\big\rVert_2,\qquad \mathrm{minFDE}_k=\min_{m=1,\dots,k}\big\lVert\hat x^{(m)}_H-x_H\big\rVert_2$$
> where $\hat x^{(m)}_t$ is sample $m$'s position at step $t$, and $x_t$ and $H$ are as in the ADE
> box of worked step 4.
> **Example.** Part 2's straight walk, with a forecaster that emits $k = 2$ samples: the model's
> curving path and the constant-velocity line. Their ADEs are $0.60$ and $0.00$ m, so
> $\mathrm{minADE}_2 = 0.00$ m and $\mathrm{minFDE}_2 = 0.00$ m — a perfect score for a forecaster
> that never said which of its two guesses it believed. Add a third sample walking backward,
> $(-1, 0), (-2, 0), (-3, 0)$, whose errors are $2$, $4$ and $6$ m and whose ADE is $4.00$ m:
> $\mathrm{minADE}_3$ is still $0.00$, because adding a sample can never raise a minimum.
> **Non-example.** The mean ADE over the $k$ samples is not $\mathrm{minADE}_k$: it is
> $(0.60 + 0.00)/2 = 0.30$ m for the two-sample set and $(0.60 + 0.00 + 4.00)/3 = 1.53$ m for the
> three. That average does penalise the backward guess; $\mathrm{minADE}_k$ cannot.
> **Why it matters.** It measures **coverage** — whether some sample came close — and a planner
> needs the probability of each future, which this number never asks for. That is the trap §8
> lists.

Three things follow:

- **Multimodality is the point.** The future is genuinely multi-valued; a model that regresses one path averages incompatible options and produces a trajectory no one would walk. Report $\text{minADE}_k$ / $\text{minFDE}_k$ over $k$ sampled futures, and be aware that these reward *coverage*, not calibration — a model can win by sampling diversely and believing nothing.
- **Interaction matters.** Social pooling, graph, and attention-based models exist because pedestrians condition on each other and on vehicles.
- **Metric caution.** minADE at $k=20$ says "one of twenty guesses was close." That is not the same as a usable prediction, and a planner cannot consume twenty futures without a probability over them.

### 7. From roads to shared workspaces

The formulation transfers to human–robot collaboration with three substitutions:

| Road setting | Shared workspace |
|---|---|
| crossing / not crossing | reach into workspace, hand over, step into envelope |
| curb, crosswalk | exclusion zone, machine envelope, task boundary |
| vehicle plans a stop | robot slows, yields, re-plans, or asks |
| pedestrian is a stranger | worker is trained, repeated, and adapts to the robot |

That last row is the substantive difference and a genuine research opening. **A worker who interacts with the same robot daily changes their behaviour in response to it,** so the predictor's training distribution shifts because the predictor is deployed. Road-crossing datasets contain no such feedback loop. Anyone claiming a road-trained intent model transfers to a worksite has to address it. Two formal ways to put the prediction inside the robot's decision — goal inference with a QMDP action choice, and a Stackelberg game in which the human responds to the robot, the same feedback loop — are [[04-robotics/hri-safety|11. HRI & Safety §3.5]].

### 8. Evaluation traps specific to this literature

| Trap | What goes wrong |
|---|---|
| Observation window leakage | frames at or after the event enter the input; performance is inflated and the model is a detector |
| Splitting by clip, not by person or scene | the same pedestrian appears in train and test; results measure memorisation |
| Averaging over time-to-event | hides $\Delta^*$, the only deployment-relevant quantity |
| ROC under heavy imbalance | looks strong while precision at threshold is unusable |
| Reporting only minADE$_k$ | rewards diversity, not belief; no probability for the planner |
| Ignoring scene context leakage | crosswalk position alone predicts crossing; the model may not use the human at all |

The last one deserves the same treatment as scene bias in [[04-robotics/video-action-understanding|20. §2]]: **ablate the human.** If a model with the pedestrian masked out performs nearly as well, the paper has built a scene prior, not an intent model.

### 9. Reading claims and evaluations

| Paper phrase | Check before accepting it |
|---|---|
| predicts pedestrian intent | intent classification or trajectory; is a time-to-event curve reported |
| early prediction | what is $\Delta^*$ at the deployed threshold |
| uncertainty-aware | is calibration measured (ECE, reliability diagram) or only a softmax reported |
| outperforms SOTA | same split protocol; split by person/scene or by clip |
| uses subtle behavioural cues | at what distance were the cues resolvable; human-masked ablation |
| real-time | end-to-end latency including detection and tracking, added to the required lead |

### After reading

You should be able to:

- state the difference between intent classification and trajectory forecasting and which metric belongs to each;
- compute a Brier score, a Brier skill score and a binned ECE from a log you are handed, and say what the binning did to the last one;
- compute ADE and FDE for a predicted path and for a constant-velocity baseline on the same path;
- compute a usable horizon $\Delta^*$ and compare it against a required lead time;
- explain calibration, name two ways to fix it, and say why conformal prediction fits safety decisions;
- explain why accuracy is the wrong metric under a low base rate;
- name the human-masked ablation and what it tests;
- state the feedback-loop difference between road pedestrians and repeat coworkers.

> [!tip] Going deeper · 더 깊이
> No textbook, and the two halves of §1 go different ways. For intent classification, PIE (ICCV 2019) is the reference dataset and its paper states the problem most cleanly. For trajectory forecasting, read Social LSTM (CVPR 2016) then Social GAN (CVPR 2018) — the second exists because the first predicted one future for a problem with many, and that disagreement is still the field's live question. For §4, calibration is not this field's own topic: Guo et al. (ICML 2017) for calibration of neural networks and Angelopoulos & Bates for conformal prediction, both in Sources below, are where that machinery lives.

### Self-check

1. A model reports 96% accuracy on crossing prediction. Why is this uninformative, and what should be reported instead?
2. A robot needs 0.9 s to stop. At a fixed allowed FPR, model A meets the required recall only to $\Delta=0.5$ s; model B meets it to $\Delta=1.5$ s. Which meets this operating requirement, and what does AUC alone fail to decide?
3. Why can a model win on minADE$_{20}$ and still be unusable by a planner?
4. What single ablation tests whether an intent model is actually reading the human?
5. Why is a worksite intent model's training distribution non-stationary in a way a road dataset's is not?

> [!tip]- Answers
> 1. Base rate — a constant "no" scores similarly. Report AUC for ranking and precision–recall plus the chosen deployed operating point as functions of time-to-event. 2. B meets this stated requirement; A does not provide enough lead at that operating point. AUC alone does not choose the threshold, encode braking cost, or establish calibration. 3. minADE rewards one lucky sample among twenty; the planner needs a probability distribution over futures, which the metric does not require the model to provide. 4. Mask or remove the pedestrian and re-evaluate; near-equal performance means the model learned scene priors. 5. The worker adapts to the deployed robot, so deployment changes the data-generating process — a feedback loop absent from passive road recordings.

**Worked: three claim-readings this page licenses.** 96% accuracy on a 94% “no” base rate is a constant-no score. minADE$_{20}=0.18\,\mathrm{m}$ does not give a calibrated set for a stop. Week-four worksite labels are not JAAD: coworkers adapted to the robot.

### Problem set · 과제

Tier A. Using **I20** from the running object above, and this page only. One outcome flips, the pedestrian turns, and the platform changes; the twenty forecasts do not.

1. **Draw.** Redraw both panels of the picture above for the changed object. Panel 1: the reliability diagram after case 19 (which forecast $0.90$) turns out to have been a $y = 1$ after all — show which single point moves and in which direction, and mark the diagonal it moves toward. Panel 2: the same time-to-event curve against a faster platform, $v = 2.0\ \mathrm{m/s}$, $a = 1.6\ \mathrm{m/s^2}$, $t_{\mathrm{lat}} = 0.30$ s, with both verticals drawn and the gap between them signed.
2. **Derive.** (a) With case 19 flipped to $y = 1$ and nothing else changed: the new Brier score, the new base rate, the new Brier skill score, and the new five-bin ECE. (b) The pedestrian of Part 2 turns instead of walking straight: the true future is now $(1.00,\ 0.15)$, $(2.42,\ 0.56)$, $(3.75,\ 1.00)$, the observed history and the model's prediction are unchanged. Compute ADE and FDE for the model and for the constant-velocity baseline. (c) $\Delta^{*}$ is unchanged at $1.375$ s; compute $\Delta_{\mathrm{req}}$ for the faster platform of panel 2 and say whether it now passes.
3. **Interpret.** The vendor reads the part (a) result and reports "recalibrated: ECE improved from $0.100$ to $0.090$." Two of the three numbers you computed in (a) moved much further than the ECE did. Say what actually changed in the log, why ECE is the least sensitive of the three to it, and what you would require the vendor to report instead.

4. **Do.** Fill the `?` so that one script recomputes the whole worked derivation from I20 — Brier, skill score, five-bin ECE and AUC; ADE and FDE for the model and the constant-velocity baseline; $\Delta^{*}$ against the required lead — and check each against the page. Then use it for the three things the page only asserts: square every forecast and confirm that AUC stays put while Brier and ECE move; recompute the ECE with $2$ and $10$ bins; and flip case 19 to check your 2(a). What does the squared forecaster's skill score say that its ECE does not?

```python
import numpy as np
p = np.array([0.05, 0.10, 0.10, 0.15, 0.20, 0.25, 0.25, 0.30, 0.45, 0.50,
              0.50, 0.55, 0.65, 0.70, 0.70, 0.75, 0.85, 0.90, 0.90, 0.95])    # I20, Part 1
y = np.array([0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1])
def ece(p, y, B=5):
    b = np.minimum((p*B).astype(int), B - 1)                   # equal-width bins, top edge closed
    return sum(? for k in range(B) if (b == k).any())         # occupancy-weighted gap
def scores(p, y):
    bs = np.mean((p - y)**2)                                   # Brier score
    bss = ?                                                    # skill against the base-rate forecaster
    pos, neg = p[y == 1], p[y == 0]
    auc = np.mean([(a > b) + 0.5*(a == b) for a in pos for b in neg])   # Mann-Whitney, ties count half
    return round(float(bs), 5), round(float(bss), 3), round(float(ece(p, y)), 4), round(float(auc), 4)
def ade_fde(pred, truth):
    d = np.linalg.norm(np.array(pred) - np.array(truth), axis=1)
    return round(float(d.mean()), 3), round(float(d[-1]), 3)
obs = np.array([(-2.0, 0.0), (-1.0, 0.0), (0.0, 0.0)])          # Part 2, 1 Hz
truth = [(1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]
model = [(1.0, 0.3), (2.3, 0.4), (3.6, 0.8)]
cv = [? for k in (1, 2, 3)]                                    # constant-velocity baseline
dt = np.array([0.5, 1.0, 1.5, 2.0, 2.5])                        # Part 3
rec = np.array([0.92, 0.84, 0.72, 0.60, 0.48])
d_star = float(np.interp(-0.75, -rec, dt))                      # last lead time with recall >= 0.75
d_req = ?                                                       # stopping time v/a plus latency
print("I20", scores(p, y), "squared", scores(p**2, y))
print("ECE by bins", [round(float(ece(p, y, B)), 3) for B in (2, 5, 10)])
print("model", ade_fde(model, truth), "cv", ade_fde(cv, truth))
print("usable", round(d_star, 3), "required", round(d_req, 3))
y2 = y.copy(); y2[18] = 1                                        # case 19 flips to an event
print("flipped", scores(p, y2))
```

> [!note]- How to draw it · 그리는 법
> - **Panel 1, the reliability diagram**: a unit square, $\hat p$ across and observed frequency up, with the $45^\circ$ diagonal drawn as the calibrated line.
> - **Five equal-width bins on the horizontal axis**: for each, one point at (bin mean $\hat p$, bin observed frequency), and a bar above the axis showing how many of the twenty cases fell in it.
> - **Draw the vertical gap from each point to the diagonal and label it** — the weighted average of those five gaps is the whole of §4's scalar. A point below the diagonal is overconfident, one above it underconfident.
> - **Panel 2, the time-to-event curve**: $\Delta$ across, recall up, the five points of Part 3 joined, and the horizontal requirement line at $0.75$.
> - **Drop a vertical where the curve crosses the requirement and label it $\Delta^{*}$**, then draw a second vertical at the required lead $t_{\mathrm{stop}} + t_{\mathrm{lat}}$, with $t_{\mathrm{stop}} = v/a$. The signed distance between the two verticals is the answer, and its sign is the deployment decision.
> - **Beside panel 2, the trajectory of Part 2 from above**: the three observed positions, the three true future ones and the three predicted ones.
> - **The three displacement segments that ADE averages**, with the last one thickened because it alone is FDE.

> [!tip]- Solutions
> 1. Panel 1: only the top bin's point moves, from $(0.90,\ 0.75)$ up to $(0.90,\ 1.00)$ — past the diagonal, from overconfident (frequency below the forecast) to underconfident (frequency above it); the other four points and all five bars are untouched, because the flip changes an outcome, not a forecast. Panel 2: $\Delta^{*}$ stays at $1.375$ s while the required-lead vertical moves out to $1.55$ s, so the gap that was $-0.075$ s becomes $-0.175$ s — a faster base with a shorter latency is still worse off, because $v/a$ grew more than $t_{\mathrm{lat}}$ shrank.
> 2. (a) Case 19's residual changes from $(0.90-0)^2 = 0.81$ to $(0.90-1)^2 = 0.01$, so the total falls from $4.515$ to $3.715$ and $\mathrm{BS} = 3.715/20 = \mathbf{0.1858}$. The base rate becomes $10/20 = \mathbf{0.50}$, the reference is $0.50 \times 0.50 = 0.2500$, and $\mathrm{BSS} = 1 - 0.1858/0.2500 = \mathbf{0.257}$. Only the top bin's ECE term changes, its frequency going from $0.75$ to $1.00$ and its gap from $0.15$ to $|1.00-0.90| = 0.10$, so $\mathrm{ECE} = 0.2\,(0.15 + 0 + 0 + 0.20 + 0.10) = \mathbf{0.090}$.
> (b) Model errors $\hat x_k - x_k$: $(0.00,\ 0.15) \to 0.15$; $(-0.12,-0.16) \to 0.20$; $(-0.15,-0.20) \to 0.25$. $\mathrm{ADE} = 0.60/3 = \mathbf{0.20\ \mathrm{m}}$, $\mathrm{FDE} = \mathbf{0.25\ \mathrm{m}}$. Constant velocity still predicts $(1,0), (2,0), (3,0)$, giving errors $\lVert(0,-0.15)\rVert = 0.15$, $\lVert(-0.42,-0.56)\rVert = 0.70$, $\lVert(-0.75,-1.00)\rVert = 1.25$, so $\mathrm{ADE}_{\mathrm{CV}} = 2.10/3 = \mathbf{0.70\ \mathrm{m}}$ and $\mathrm{FDE}_{\mathrm{CV}} = \mathbf{1.25\ \mathrm{m}}$. The ranking has completely reversed from the straight walk, on the same model and the same baseline. That is the reading: an ADE is a statement about the *test set's* motion as much as about the model, which is why the constant-velocity control belongs in every table.
> (c) $t_{\mathrm{stop}} = 2.0/1.6 = 1.25$ s, $\Delta_{\mathrm{req}} = 1.25 + 0.30 = 1.55$ s $> 1.375$ s. It fails, and by more than before. The stopping distance also grows from $0.75$ m to $2.0^2/(2\times1.6) = 1.25$ m.
> 3. What changed is one outcome out of twenty — not the model, which emitted the identical twenty probabilities in both versions. The Brier score moved $18\%$ and the skill score nearly tripled, from $0.088$ to $0.257$, while ECE moved $10\%$, because ECE collapses each bin to a single frequency before taking a difference and a $0.75 \to 1.00$ move inside one bin of four is a small change to a bounded gap, while the same flip removes the single largest squared residual in the log. Require the vendor to report $N$, the binning, the base rate, the Brier skill score against the base-rate forecaster, and the reliability diagram itself; an ECE alone at $N = 20$ is a number one worker's afternoon can move either way.
> 4. The blanks are `1 - bs/(y.mean()*(1 - y.mean()))`, `(b == k).mean()*abs(y[b == k].mean() - p[b == k].mean())`, `obs[-1] + k*(obs[-1] - obs[-2])` and `1.5/1.5 + 0.45`. The filled script:
>
> ```python
> import numpy as np
> p = np.array([0.05, 0.10, 0.10, 0.15, 0.20, 0.25, 0.25, 0.30, 0.45, 0.50,
>               0.50, 0.55, 0.65, 0.70, 0.70, 0.75, 0.85, 0.90, 0.90, 0.95])    # I20, Part 1
> y = np.array([0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1])
> def ece(p, y, B=5):
>     b = np.minimum((p*B).astype(int), B - 1)                   # equal-width bins, top edge closed
>     return sum((b == k).mean()*abs(y[b == k].mean() - p[b == k].mean()) for k in range(B) if (b == k).any())
> def scores(p, y):
>     bs = np.mean((p - y)**2)                                   # Brier score
>     bss = 1 - bs/(y.mean()*(1 - y.mean()))                     # skill against the base-rate forecaster
>     pos, neg = p[y == 1], p[y == 0]
>     auc = np.mean([(a > b) + 0.5*(a == b) for a in pos for b in neg])   # Mann-Whitney, ties count half
>     return round(float(bs), 5), round(float(bss), 3), round(float(ece(p, y)), 4), round(float(auc), 4)
> def ade_fde(pred, truth):
>     d = np.linalg.norm(np.array(pred) - np.array(truth), axis=1)
>     return round(float(d.mean()), 3), round(float(d[-1]), 3)
> obs = np.array([(-2.0, 0.0), (-1.0, 0.0), (0.0, 0.0)])          # Part 2, 1 Hz
> truth = [(1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]
> model = [(1.0, 0.3), (2.3, 0.4), (3.6, 0.8)]
> cv = [obs[-1] + k*(obs[-1] - obs[-2]) for k in (1, 2, 3)]       # constant-velocity baseline
> dt = np.array([0.5, 1.0, 1.5, 2.0, 2.5])                        # Part 3
> rec = np.array([0.92, 0.84, 0.72, 0.60, 0.48])
> d_star = float(np.interp(-0.75, -rec, dt))                      # last lead time with recall >= 0.75
> d_req = 1.5/1.5 + 0.45                                          # stopping time v/a plus latency
> print("I20", scores(p, y), "squared", scores(p**2, y))
> print("ECE by bins", [round(float(ece(p, y, B)), 3) for B in (2, 5, 10)])
> print("model", ade_fde(model, truth), "cv", ade_fde(cv, truth))
> print("usable", round(d_star, 3), "required", round(d_req, 3))
> y2 = y.copy(); y2[18] = 1                                        # case 19 flips to an event
> print("flipped", scores(p, y2))
> ```
>
> It prints `I20 (0.22575, 0.088, 0.1, 0.7172)` and `squared (0.24898, -0.006, 0.1765, 0.7172)`, `ECE by bins [0.055, 0.1, 0.27]`, `model (0.6, 1.0) cv (0.0, 0.0)`, `usable 1.375 required 1.45` and `flipped (0.18575, 0.257, 0.09, 0.795)` — every number of the worked derivation, the two non-examples of step 3, and your 2(a). The squared forecaster's skill score is $-0.006$: it is now *worse* than always saying the base rate, a verdict its ECE of $0.177$ reports only as "less calibrated" and its unchanged AUC not at all. The flip also moves AUC, from $0.7172$ to $0.795$, because it changes which cases are events.
### Sources

**Pedestrian intent**

- A. Rasouli, I. Kotseruba, T. Kunic, and J. K. Tsotsos, "PIE: A Large-Scale Dataset and Models for Pedestrian Intention Estimation and Trajectory Prediction," [*ICCV 2019*](https://openaccess.thecvf.com/content_ICCV_2019/html/Rasouli_PIE_A_Large-Scale_Dataset_and_Models_for_Pedestrian_Intention_Estimation_ICCV_2019_paper.html).
- A. Rasouli, I. Kotseruba, and J. K. Tsotsos, JAAD — [Joint Attention in Autonomous Driving](https://data.nvision2.eecs.yorku.ca/JAAD_dataset/), *ICCVW 2017*.

**Trajectory forecasting — verified citations**

- A. Alahi, K. Goel, V. Ramanathan, A. Robicquet, L. Fei-Fei, and S. Savarese, "Social LSTM: Human Trajectory Prediction in Crowded Spaces," *CVPR 2016*, pp. 961–971 — one LSTM per person plus a social pooling layer over spatial neighbours. No arXiv preprint exists; cite the CVF or IEEE record.
- A. Gupta, J. Johnson, L. Fei-Fei, S. Savarese, and A. Alahi, "Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks," *CVPR 2018*, pp. 2255–2264. [arXiv:1803.10892](https://arxiv.org/abs/1803.10892) — recasts the task as multimodal, with a variety loss that explicitly rewards diverse samples.
- T. Salzmann, B. Ivanovic, P. Chakravarty, and M. Pavone, "Trajectron++: Dynamically-Feasible Trajectory Forecasting with Heterogeneous Data," *ECCV 2020*. [arXiv:2001.03093](https://arxiv.org/abs/2001.03093) — enforces agent dynamics so outputs are kinematically feasible, and can condition on the ego-agent's own plan. That last property is what makes it usable *inside* a planning loop.

**Benchmarks, and where their protocol came from**

- S. Pellegrini, A. Ess, K. Schindler, and L. van Gool, "You'll Never Walk Alone: Modeling Social Behavior for Multi-Target Tracking," *ICCV 2009*, pp. 261–268 — the ETH and HOTEL scenes.
- A. Lerner, Y. Chrysanthou, and D. Lischinski, "Crowds by Example," *Computer Graphics Forum*, vol. 26, no. 3, pp. 655–664, 2007 (Eurographics) — the UNIV, ZARA1, and ZARA2 scenes.
- A. Robicquet, A. Sadeghian, A. Alahi, and S. Savarese, "Learning Social Etiquette: Human Trajectory Understanding in Crowded Scenes," *ECCV 2016*, pp. 549–565 — the Stanford Drone Dataset: eight campus scenes, roughly 19,000 agents across pedestrians, bikers, skateboarders, cars, buses, and golf carts.

> [!note] The "ETH/UCY benchmark" is a convention, not a dataset
> Neither source paper was written as a prediction benchmark — one is a tracking paper, the other
> a crowd-simulation authoring paper. The five-scene leave-one-out protocol with 8 observed and 12
> predicted frames at 2.5 Hz was established by Social LSTM in 2016 and inherited unexamined
> since. If your page or paper discusses evaluation, that provenance is the point.

**The critiques — read these before believing a leaderboard**

- C. Schöller, V. Aravantinos, F. Lay, and A. Knoll, "What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction," *IEEE RA-L*, vol. 5, no. 2, 2020 (ICRA 2020). [arXiv:1903.07933](https://arxiv.org/abs/1903.07933) — a constant-velocity model beats state-of-the-art neural predictors on the standard benchmarks. The diagnosis: the networks fail to exploit extra inputs, learn dataset biases instead, barely use motion history, and cannot learn interaction from data this thin.
- O. Makansi, J. von Kügelgen, F. Locatello, et al., "You Mostly Walk Alone: Analyzing Feature Attribution in Trajectory Prediction," *ICLR 2022*. [arXiv:2110.05304](https://arxiv.org/abs/2110.05304) — a Shapley-value attribution showing that these methods are not in fact reasoning about interactions. This is the mechanism behind Schöller's empirical result; the pair is stronger than either alone.

**Intent in a shared workspace — the manipulation-relevant line**

- H. S. Koppula and A. Saxena, "Anticipating Human Activities Using Object Affordances for Reactive Robotic Response," *IEEE TPAMI*, vol. 38, no. 1, 2016 (earlier version *RSS 2013*) — an anticipatory temporal CRF over object affordances. The canonical "intent, not trajectory" reference: it predicts what the human is about to do *with which object*.
- J. Mainprice and D. Berenson, "Human-Robot Collaborative Manipulation Planning Using Early Prediction of Human Motion," *IROS 2013*, pp. 299–306 — predicts human workspace occupancy as a swept volume, then plans against it. The reference for turning a prediction into an actual planning cost.
- R. Luo, R. Hayne, and D. Berenson, "Unsupervised Early Prediction of Human Reaching for Human-Robot Collaboration in Shared Workspaces," *Autonomous Robots*, vol. 42, pp. 631–648, 2018 — a two-layer GMM learned online with no offline training and no labelling, adapting to new operators. The most directly relevant to a deployed cell, where you cannot pretrain on your specific operator.

**Calibration**

- C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
- A. N. Angelopoulos and S. Bates, "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification," [arXiv:2107.07511](https://arxiv.org/abs/2107.07511)

## 한국어

*J군의 끝이다. [[04-robotics/hri-safety|11. HRI·안전]]·[[04-robotics/human-pose-gaze|21]]·[[04-robotics/video-action-understanding|20]]번과 확률 위에 선다.
정확도보다 시점과 보정이 더 중요해지는 지점이다 — 예측이 답이 아니라 결정으로 가는 인터페이스이기 때문이다.*

사람과 공간을 공유하는 로봇은 그 사람이 무엇을 할지에 대한 추측 위에서 행동한다. 그 추측은 인지와 모든 하위 결정 사이의 인터페이스이고, 그 값어치는 정확도가 아니라 정확히 **시점(timing)과 보정(calibration)** 만큼이다.

> [!info] 깊이 목표
> 의도 분류와 궤적 예측을 구분하고 논문이 푼 것이 어느 쪽인지 안다; time-to-event 곡선을
> 읽는다; 잘 보정된 0.7이 나쁘게 보정된 0.9보다 유용한 이유를 설명한다; 보행자 의도
> 벤치마크의 표준 평가 함정을 짚는다; 이 정식화를 인간–로봇 협업에 사상한다.

> [!note] 선수 지식
> [[02-foundations/probability|확률]] · [[02-foundations/ml-practice|9. ML 실무와 평가]](AUC, ROC, precision–recall, F1) · [[04-robotics/video-action-understanding|20. 비디오 표현과 행동 이해]] · [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]] · [[04-robotics/hri-safety|11. Human–Robot Interaction & Safety]]

> [!note] 처음이라면 · First pass
> 먼저 이 페이지의 대상과 그 위에서 하는 다섯 개의 유도, 그다음 §1 — 의도 분류와 궤적 예측은 다른 문제이고 논문이 어느 쪽을 풀었는지 늘 밝히지는 않는다 — 그다음 §3, 그다음 §4. 연구가 실제로 있는 곳이 보정이라서 §4를 조망 자료보다 앞에 둔다. 두 번째 읽기: 단서 사슬과 기저율인 §2·§5, best-of-$k$ 궤적 지표인 §6, 도로에서 공유 작업공간으로 옮기는 §7, 그리고 논문 옆에 두고 쓰는 점검표 §8·§9.

### 이 페이지의 대상 · Running object

예측은 장치가 아니라 로그 위에서 평가되므로 [[02-foundations/lab-plants|0.6 Lab Plants]]의 대상이 맞지 않는다. 그래서 이 페이지는 자기 로그를 고정한다. 이동 베이스에 올린 횡단 의도 시스템의 오후 한나절, **I20** 이고, 이후로 숫자를 바꾸지 않는다. 페이지가 평가해야 할 것 하나씩에 대응하는 세 부분으로 되어 있다.

**1부 — 판정 스무 건.** 각 사례 $i$는 작업자가 앞으로 2초 안에 로봇 경로로 들어올 확률 $\hat p_i$와 뒤이어 일어난 결과 $y_i \in \{0,1\}$다. $\hat p$ 오름차순으로 적었고, 번호는 시각이 아니라 이름표다.

| 사례 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\hat p_i$ | 0.05 | 0.10 | 0.10 | 0.15 | 0.20 | 0.25 | 0.25 | 0.30 | 0.45 | 0.50 |
| $y_i$ | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |

| 사례 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\hat p_i$ | 0.50 | 0.55 | 0.65 | 0.70 | 0.70 | 0.75 | 0.85 | 0.90 | 0.90 | 0.95 |
| $y_i$ | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |

스무 건 중 아홉 건에서 사건이 일어났으므로 이 로그의 기저율은 $\bar p = 9/20 = 0.45$다. 실제 배포의 몇 %보다 훨씬 높은데, 이 로그는 시스템이 판정할 가치가 있다고 걸러낸 부분집합이고 보정 주장이 대상으로 삼는 모집단이 바로 그것이다. 전체 프레임 스트림으로 되돌릴 때 무슨 일이 생기는지는 §5가 다룬다.

**2부 — 궤적 하나.** 사례 20에는 경로도 붙어 있다. 지면 위에서 1 Hz로 샘플링한 미터 좌표다. 관측된 세 위치는 $(-2.00, 0)$, $(-1.00, 0)$, $(0.00, 0)$이고, 참 미래 세 위치와 모델의 예측 세 위치는:

| 스텝 | $t+1$ | $t+2$ | $t+3$ |
|---|---|---|---|
| 정답 $x_k$ | $(1.00,\ 0.00)$ | $(2.00,\ 0.00)$ | $(3.00,\ 0.00)$ |
| 모델 $\hat x_k$ | $(1.00,\ 0.30)$ | $(2.30,\ 0.40)$ | $(3.60,\ 0.80)$ |

**3부 — 조기성 대 정확도 곡선, 그리고 그것이 지켜야 할 플랫폼.** 오경보율 $\alpha = 0.05$를 고정한 recall을 사건까지 남은 시간의 함수로 적는다. $\mathrm{Recall}_{\mathrm{FPR}=0.05}(\Delta)$는 이렇게 읽는다. 아무도 들어오지 않는 경우의 $5\%$가 어차피 경보를 받도록 경보 문턱값을 정하고, 실제 진입 중 일어나기 $\Delta$초 전에 이미 경보를 받은 비율을 센다($\Delta = T - t$, 사건까지 남은 시간이다. 이 구성과 그것을 곡선으로 보고하는 이유는 §3이 말한다):

| $\Delta$ (초) | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 |
|---|---:|---:|---:|---:|---:|
| $\mathrm{Recall}_{\mathrm{FPR}=0.05}(\Delta)$ | 0.92 | 0.84 | 0.72 | 0.60 | 0.48 |

플랫폼은 $v = 1.5\ \mathrm{m/s}$로 달리는 이동 베이스이고 최대 감속 $a = 1.5\ \mathrm{m/s^2}$, 인지에서 제동까지의 지연 $t_{\mathrm{lat}} = 0.45$초이며, 안전 논거는 같은 $\alpha$에서 recall $\ge 0.75$를 요구한다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 482" style="max-width:100%;height:auto" role="img" aria-label="의도 예측 그림: I20의 예측 스무 개를 다섯 구간으로 묶어 대각선까지의 간격을 표시한 reliability diagram, 사용 가능 지평 1.375초가 베이스에 필요한 1.45초에 75 ms 못 미치는 선행 시간 대 recall 곡선, 그리고 변위 오차 셋을 표시한 사례 20의 궤적">
  <text x="16" y="24" font-size="12" fill="currentColor" font-weight="600">1. reliability diagram</text>
  <rect x="58" y="58" width="192" height="192" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" fill="none"/>
  <line x1="96.4" y1="250" x2="96.4" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="134.8" y1="250" x2="134.8" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="173.2" y1="250" x2="173.2" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="211.6" y1="250" x2="211.6" y2="58" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22"/>
  <line x1="58" y1="250" x2="250" y2="58" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7" stroke-dasharray="5 3"/>
  <line x1="58" y1="250" x2="58" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="250" x2="58" y2="250" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="58" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.0</text>
  <text x="51" y="254" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.0</text>
  <line x1="96.4" y1="250" x2="96.4" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="211.6" x2="58" y2="211.6" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="96.4" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.2</text>
  <text x="51" y="215.6" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.2</text>
  <line x1="134.8" y1="250" x2="134.8" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="173.2" x2="58" y2="173.2" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="134.8" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.4</text>
  <text x="51" y="177.2" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.4</text>
  <line x1="173.2" y1="250" x2="173.2" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="134.8" x2="58" y2="134.8" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="173.2" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.6</text>
  <text x="51" y="138.8" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.6</text>
  <line x1="211.6" y1="250" x2="211.6" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="96.4" x2="58" y2="96.4" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="211.6" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.8</text>
  <text x="51" y="100.4" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.8</text>
  <line x1="250" y1="250" x2="250" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <line x1="54" y1="58" x2="58" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="250" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.0</text>
  <text x="51" y="62" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">1.0</text>
  <text x="154" y="282" font-size="11" fill="currentColor" text-anchor="middle">예측 p̂ (구간 평균)</text>
  <text x="28" y="48" font-size="11" fill="currentColor">관측 빈도</text>
  <rect x="63.2" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="101.6" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="140" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="178.4" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <rect x="216.8" y="230" width="28" height="20" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6" fill="currentColor" fill-opacity="0.14"/>
  <text x="244.2" y="223.1" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">막대: 구간마다 n = 4</text>
  <line x1="77.2" y1="202" x2="77.2" y2="230.8" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="77.2" cy="202" r="4" stroke="none" fill="currentColor"/>
  <circle cx="106" cy="202" r="4" stroke="none" fill="currentColor"/>
  <circle cx="154" cy="154" r="4" stroke="none" fill="currentColor"/>
  <line x1="192.4" y1="154" x2="192.4" y2="115.6" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="192.4" cy="154" r="4" stroke="none" fill="currentColor"/>
  <line x1="230.8" y1="106" x2="230.8" y2="77.2" stroke="currentColor" stroke-width="2.2"/>
  <circle cx="230.8" cy="106" r="4" stroke="none" fill="currentColor"/>
  <text x="77.2" y="193" font-size="11" fill="currentColor" text-anchor="middle">0.15</text>
  <text x="113" y="216" font-size="11" fill="currentColor">0.00</text>
  <text x="161" y="168" font-size="11" fill="currentColor">0.00</text>
  <text x="198.4" y="169" font-size="11" fill="currentColor">0.20</text>
  <text x="230.8" y="123" font-size="11" fill="currentColor" text-anchor="middle">0.15</text>
  <text x="300" y="24" font-size="12" fill="currentColor" font-weight="600">2. time-to-event</text>
  <rect x="330" y="58" width="210" height="192" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" fill="none"/>
  <line x1="330" y1="250" x2="330" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="330" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <line x1="382.5" y1="250" x2="382.5" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="382.5" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.0</text>
  <line x1="435" y1="250" x2="435" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="435" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1.5</text>
  <line x1="487.5" y1="250" x2="487.5" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="487.5" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2.0</text>
  <line x1="540" y1="250" x2="540" y2="254" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="540" y="266" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">2.5</text>
  <line x1="326" y1="250" x2="330" y2="250" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="254" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.4</text>
  <line x1="326" y1="186" x2="330" y2="186" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="190" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.6</text>
  <line x1="326" y1="122" x2="330" y2="122" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="126" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0.8</text>
  <line x1="326" y1="58" x2="330" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
  <text x="323" y="62" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">1.0</text>
  <text x="435" y="282" font-size="11" fill="currentColor" text-anchor="middle">사건까지 남은 시간 Δ (s)</text>
  <text x="300" y="48" font-size="11" fill="currentColor">FPR 0.05에서의 recall</text>
  <line x1="330" y1="138" x2="540" y2="138" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" stroke-dasharray="5 3"/>
  <text x="536" y="132" font-size="11" fill="currentColor" text-anchor="end">요구 recall 0.75</text>
  <path d="M330 83.6 L382.5 109.2 L435 147.6 L487.5 186 L540 224.4" stroke="currentColor" stroke-width="1.9" fill="none" stroke-linejoin="round"/>
  <circle cx="330" cy="83.6" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="382.5" cy="109.2" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="435" cy="147.6" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="487.5" cy="186" r="3.4" stroke="none" fill="currentColor"/>
  <circle cx="540" cy="224.4" r="3.4" stroke="none" fill="currentColor"/>
  <line x1="421.9" y1="138" x2="421.9" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <line x1="429.8" y1="60" x2="429.8" y2="250" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 2.5"/>
  <circle cx="421.9" cy="138" r="4.4" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="415.9" y="211.6" font-size="11" fill="currentColor" text-anchor="end">Δ* = 1.375 s</text>
  <text x="435.8" y="74" font-size="11" fill="currentColor">t<tspan dy="3.1" font-size="8.6">stop</tspan><tspan dx="3.1" dy="-3.1">+ t</tspan><tspan dy="3.1" font-size="8.6">lat</tspan><tspan dx="3.1" dy="-3.1">= 1.45 s</tspan></text>
  <line x1="421.9" y1="235.6" x2="429.8" y2="235.6" stroke="currentColor" stroke-width="1.2"/>
  <text x="435.8" y="239.6" font-size="11" fill="currentColor">−0.075 s</text>
  <text x="435.8" y="223.6" font-size="11" fill="currentColor">75 ms 모자람</text>
  <text x="16" y="314" font-size="12" fill="currentColor" font-weight="600">2부를 위에서 본 것 (m): 관측, 정답, 예측</text>
  <line x1="19.8" y1="404" x2="445.4" y2="404" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.35"/>
  <path d="M194.6 404 L270.6 381.2 L369.4 373.6 L468.2 343.2" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.8" stroke-dasharray="5 3" stroke-linejoin="round"/>
  <circle cx="42.6" cy="404" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="118.6" cy="404" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="194.6" cy="404" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <circle cx="270.6" cy="404" r="4.2" stroke="none" fill="currentColor"/>
  <circle cx="346.6" cy="404" r="4.2" stroke="none" fill="currentColor"/>
  <circle cx="422.6" cy="404" r="4.2" stroke="none" fill="currentColor"/>
  <rect x="266.6" y="377.2" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <rect x="365.4" y="369.6" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <rect x="464.2" y="339.2" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <line x1="270.6" y1="404" x2="270.6" y2="381.2" stroke="currentColor" stroke-width="1.5"/>
  <line x1="346.6" y1="404" x2="369.4" y2="373.6" stroke="currentColor" stroke-width="1.5"/>
  <line x1="422.6" y1="404" x2="468.2" y2="343.2" stroke="currentColor" stroke-width="3.4"/>
  <text x="277.6" y="400.6" font-size="11" fill="currentColor">0.30</text>
  <text x="365" y="396.8" font-size="11" fill="currentColor">0.50</text>
  <text x="452.4" y="381.6" font-size="11" fill="currentColor">1.00 (FDE)</text>
  <circle cx="20" cy="424" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="30" y="428" font-size="11" fill="currentColor">관측</text>
  <circle cx="61" cy="424" r="4.2" stroke="none" fill="currentColor"/>
  <text x="71" y="428" font-size="11" fill="currentColor">정답</text>
  <rect x="98" y="420" width="8" height="8" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.3"/>
  <text x="112" y="428" font-size="11" fill="currentColor">모델</text>
  <text x="16" y="452" font-size="11" fill="currentColor" fill-opacity="0.9">ECE = 0.2 × (0.15 + 0 + 0 + 0.20 + 0.15) = 0.100. 위의 두 구간이 대각선 아래에 있다(과신).</text>
  <text x="16" y="468" font-size="11" fill="currentColor" fill-opacity="0.9">ADE = (0.30 + 0.50 + 1.00) / 3 = 0.60 m, FDE = 1.00 m. 등속 외삽은 (1, 0), (2, 0), (3, 0)을 정확히 맞힌다.</text>
</svg>

로그 I20을 세 가지로 본 그림이다. Reliability diagram은 스무 개의 예측을 구간마다 넷씩 묶고 대각선까지의 간격이 $0.15$, $0$, $0$, $0.20$, $0.15$라 $\mathrm{ECE} = 0.100$이며 위의 두 구간은 대각선 아래, 곧 과신이다. Time-to-event 곡선은 요구 recall $0.75$를 $\Delta^{*} = 1.375$초에서 가로질러 베이스에 필요한 $t_{\mathrm{stop}} + t_{\mathrm{lat}} = 1.45$초에 $75$ ms 모자라고, 그 옆 위에서 본 사례 20의 궤적에서는 모델의 변위 오차 셋 $0.30$, $0.50$, $1.00$ m가 $\mathrm{ADE} = 0.60$ m, $\mathrm{FDE} = 1.00$ m를 주는 반면 등속 외삽은 참 경로를 정확히 맞힌다.

### I20으로 한 번 끝까지 · Worked on I20

**1. 점수를 매기기 전에, 보정이란 무엇인가.**

> [!info] 정의 — 보정(calibration)
> 점수도 정확도도 아니라 **확률 예측기의 성질**이다. 예측기가 어떤 확률을 말한 사례들 안에서
> 사건의 조건부 빈도가 그 확률과 같을 때 보정돼 있다고 한다. 조건 넷이 이것을 정밀하게 만든다.
> 주변(marginal)이 아니라 **예측값에 조건부**다. 평균이 아니라 범위 안의 **모든** 값에서 성립해야
> 한다. **사례의 분포**에 관한 진술이라 사례 하나는 보정됐다고도 아니라고도 할 수 없다. 그리고
> 정직함만 제약할 뿐 **뾰족함(sharpness)** 은 제약하지 않는다. 예측이 기저율에서 얼마나 멀리
> 움직이느냐는 별개의 미덕이다.
> $$\mathbb{P}\big(y = 1 \mid \hat p = p\big) = p \quad \text{모든 } p \in [0,1] \text{에 대해}$$
> $\hat p$는 예측, $y$는 이진 결과이고, 확률은 예측기가 배포되는 사례 분포에 대한 것이다.
> **예.** I20에서 $0.50$ 근처 네 사례(9–12번)는 $\hat p$ 평균이 $0.50$이고 그중 둘에서 사건이
> 일어나 빈도가 $0.50$이다. 그 구간에서는 보정돼 있다.
> **반례 1 — 정확도.** I20을 $0.5$에서 자르면 스무 건 중 열넷을 맞혀 정확도 $70\%$인데, 모든
> $\hat p$를 $0.99$로 바꾸든 $0.51$로 바꾸든 그 숫자는 그대로다. 정확도는 확신을 보지 못한다.
> **반례 2 — AUC.** AUC는 **순위**에만 의존하므로 예측에 단조증가 변환을 아무리 걸어도 꿈쩍하지
> 않는다. I20의 $\hat p_i$를 전부 제곱해 보라. AUC는 마지막 자리까지 $0.7172$ 그대로인데 아래의
> 5구간 ECE는 $0.100$에서 $0.177$로, Brier 점수는 $0.226$에서 $0.249$로 움직인다. AUC만 보고한
> 논문은 보정에 대해 아무것도 보고하지 않은 것이다.
> **반례 3 — 상수 예측기.** 스무 건 모두에 $0.45$라고 말하면 *완벽하게* 보정돼 있으면서
> 쓸모없다. 뾰족함이 0이고 $\mathrm{AUC} = 0.5$다. 보정만으로는 결코 주장이 되지 않는다.
> **왜 중요한가.** 하위에 있는 것은 확률을 비용과 견주는 결정 규칙이다. $0.7$이 $0.7$을 뜻하지
> 않으면 $\text{비용} \times \text{확률}$은 누구도 행동의 근거로 삼을 수 없는 값이고, §5의 정밀도
> 산수는 조용히 허구가 된다.

**2. I20의 Brier 점수.**

> [!info] 정의 — Brier 점수
> 이진 예측에 대한 **엄밀 채점 규칙(proper scoring rule)** 이다. 말한 확률과 실현된 결과 사이의
> 평균제곱오차이고, $[0,1]$의 무차원 수이며 낮을수록 좋다. 조건이 셋이다. 결과는 $0/1$로
> 부호화하고, 예측은 로짓이나 점수가 아니라 확률이어야 하며, "엄밀"하다는 것은 기대 점수가 자기
> 진짜 믿음을 말할 때만 최소가 된다는 뜻이다. 확신 쪽으로든 가운데 쪽으로든 눙쳐서 이득을 보는
> 예측기는 없다.
> $$\mathrm{BS} = \frac{1}{N}\sum_{i=1}^{N}\big(\hat p_i - y_i\big)^2$$
> $N$은 사례 수, $\hat p_i$는 $i$번째 예측, $y_i \in \{0,1\}$은 그 결과다.
> **예.** I20은 $0.2258$이고 아래에서 계산한다.
> **반례.** $1 - \text{정확도}$가 아니다. 그건 여기서 $0.30$이다. $0.2258$이라는 값 자체가
> "좋다"는 뜻도 아니다. 같은 로그에서 상수 기저율 예측기가 $\bar p(1-\bar p) = 0.2475$를 받으므로,
> 모델의 순위 판별력과 확신을 다 합쳐 산 것이 $0.0218$이다.
> **왜 중요한가.** 거짓말로는 개선할 수 없는 유일한 숫자이고, 그래서 다음 정의의 맹점이 드러나는
> 기준선이 된다.

스무 개의 제곱 잔차를 더한다. 뒤에서 구간이 묶는 방식대로 묶어 두면 검산하기 쉽다:

| 사례 | 제곱 잔차 | 소계 |
|---|---|---:|
| 1–4 | $0.05^2 + 0.10^2 + 0.10^2 + 0.85^2$ | 0.7450 |
| 5–8 | $0.20^2 + 0.25^2 + 0.25^2 + 0.70^2$ | 0.6550 |
| 9–12 | $0.45^2 + 0.50^2 + 0.50^2 + 0.55^2$ | 1.0050 |
| 13–16 | $0.35^2 + 0.70^2 + 0.30^2 + 0.75^2$ | 1.2650 |
| 17–20 | $0.15^2 + 0.10^2 + 0.90^2 + 0.05^2$ | 0.8450 |
| | **합계** | **4.5150** |

$$\mathrm{BS} = \frac{4.5150}{20} = 0.2258$$

이제 기준선을 잡는다. 제곱오차는 다른 무언가도 제곱해 보기 전에는 아무 뜻이 없기 때문이다. 늘 기저율만 말하는 상수 예측기는 $\bar p(1-\bar p) = 0.45 \times 0.55 = 0.2475$를 받으므로 **Brier skill score** 는

$$\mathrm{BSS} = 1 - \frac{\mathrm{BS}}{\bar p(1-\bar p)} = 1 - \frac{0.2258}{0.2475} = 0.088$$

**8.8%.** 모델이 "매번 기저율을 말하기"를 이기는 폭이 그만큼이고, 남은 것의 대부분에 사례 하나가 책임이 있다. 19번은 $0.90$이라 말했고 사건은 일어나지 않아 $4.515$ 중 $0.81$을 혼자 냈다. **스무 건 중 한 판정에서 점수 전체의 18%가 나온 것이다.** 이 취약함은 대상의 결함이 아니라 $N = 20$이 뜻하는 바이고, 보정 주장에 수백 건짜리 보정 집합이 필요한 이유다.

**3. 5구간 ECE, 그리고 모델의 것이 아닌 선택.**

> [!info] 정의 — 기대 보정 오차(ECE)
> **Reliability diagram의 스칼라 요약** 이다. 관측 빈도와 평균 예측값 사이 절대 간격을 구간 점유
> 수로 가중 평균한 값이고, 무차원이며 $[0,1]$에 있다. 이것은 *추정량* 이고, 값을 가지려면 조건
> 넷이 먼저 정해져야 한다. **구간 나누기 방식** — 구간 수, 그리고 등폭인지 등질량인지. 간격은 각
> 구간의 **관측 빈도** 와 그 구간의 **평균 예측값** 사이에서 잰다(구간 중점이 아니다). **절댓값은
> 구간 평균을 낸 뒤에** 씌우므로, 한 구간 안의 반대 부호 오차는 보이기도 전에 상쇄된다. 그리고
> 구간은 **점유 수로 가중** 하므로 사례 하나짜리 구간은 한 번만 센다.
> $$\mathrm{ECE} = \sum_{b=1}^{B} \frac{n_b}{N}\,\Big| \mathrm{freq}(b) - \overline{\hat p}(b) \Big|$$
> $B$는 구간 수, $n_b$는 구간 $b$의 사례 수, $N$은 전체, $\mathrm{freq}(b)$는 그 구간의 관측 사건
> 빈도, $\overline{\hat p}(b)$는 그 구간의 평균 예측값이다.
> **예.** 등폭 5구간의 I20은 $0.100$이고 아래에서 계산한다.
> **반례 — ECE는 모델의 성질이 아니다.** 똑같은 스무 예측과 똑같은 스무 결과가 2구간에서는
> $0.055$, 10구간에서는 $0.270$을 준다. 성긴 구간은 반대 부호 간격을 평균으로 지우고, 촘촘한
> 구간은 사례 하나가 구간을 정의하게 두어 가능한 빈도가 $0$과 $1$뿐이 된다. **구간 나누기를 밝히지
> 않은 ECE는 읽을 수 없고**, 치우치는 방향조차 미리 정해져 있지 않다. 두 번째 반례:
> $\mathrm{ECE} = 0$이 유용함을 뜻하지 않는다. 상수 $0.45$ 예측기는 스무 건이 한 구간에 들어가고
> 그 구간의 평균과 빈도가 모두 $0.45$라서 $\mathrm{ECE} = 0$이 정확히 성립한다.
> **왜 중요한가.** "불확실성 인지"를 내건 논문이 전부 보고하는 스칼라이고, 그 논문들이 가장 자주
> 빼먹는 줄이 구간 나누기다.

스무 사례를 등폭 5구간에 넣는다. 공교롭게 구간마다 네 건씩이라 모든 가중치 $n_b/N$이 $4/20 = 0.2$다:

| 구간 | 사례 | $n_b$ | 평균 $\hat p$ | 관측 빈도 | $\lvert \text{간격} \rvert$ |
|---|---|---:|---:|---:|---:|
| $[0.0, 0.2)$ | 1–4 | 4 | 0.10 | 1/4 = 0.25 | 0.15 |
| $[0.2, 0.4)$ | 5–8 | 4 | 0.25 | 1/4 = 0.25 | 0.00 |
| $[0.4, 0.6)$ | 9–12 | 4 | 0.50 | 2/4 = 0.50 | 0.00 |
| $[0.6, 0.8)$ | 13–16 | 4 | 0.70 | 2/4 = 0.50 | 0.20 |
| $[0.8, 1.0]$ | 17–20 | 4 | 0.90 | 3/4 = 0.75 | 0.15 |

$$\mathrm{ECE} = 0.2\,\big(0.15 + 0.00 + 0.00 + 0.20 + 0.15\big) = 0.2 \times 0.50 = 0.100$$

합계만 보지 말고 부호를 읽어라. 진단이 부호에 있다. 맨 아래 구간은 빈도가 예측값보다 높고 위 두 구간은 빈도가 예측값에 못 미친다. 즉 모델이 실제 일어나는 바에 비해 양 극단으로 밀려 있고, 이것이 교과서적인 **과확신** 이며 §4 표의 temperature scaling이 겨냥하는 바로 그것이다. 그리고 합계가 가리는 것도 보라. $0.70$이라 말하고 절반만 맞힌 모델과, 작은 오차 셋이 다르게 퍼진 모델을 같은 $0.100$이 보고한다.

**4. 2부 위의 ADE와 FDE.**

> [!info] 정의 — ADE와 FDE
> 둘 다 **미터 단위 길이** 이고, 같은 시각끼리 짝지은 예측 위치와 참 위치 사이의 유클리드 변위로
> 만든다. **ADE**(average displacement error)는 그 변위를 예측 구간 전체에 걸쳐 평균하고,
> **FDE**(final displacement error)는 마지막 스텝의 같은 변위다. 조건: 관측 창과 구간 $H$를
> 명시할 것; 예측 궤적이 집합이 아니라 **하나** 일 것 — 표본 $k$개의 최선은
> $\mathrm{minADE}_k$이고 다른 대상이다(§6); 같은 좌표계에서 같은 샘플링 주기로 **스텝마다**
> 비교할 것.
> $$\mathrm{ADE} = \frac{1}{H}\sum_{k=1}^{H}\big\lVert \hat x_k - x_k \big\rVert_2, \qquad \mathrm{FDE} = \big\lVert \hat x_H - x_H \big\rVert_2$$
> $x_k$는 스텝 $k$의 참 위치, $\hat x_k$는 예측 위치, $H$는 스텝 단위 구간이다.
> **예.** 2부는 $\mathrm{ADE} = 0.60$ m, $\mathrm{FDE} = 1.00$ m다.
> **반례.** ADE는 두 끝점 사이 거리가 아니다. 그게 FDE다. FDE도 구간 내 최대 오차가 아니다. 여기서
> 둘이 일치하는 건 이 오차가 마침 단조증가하기 때문이고, 초반에 넘어갔다 회복하는 모델은 최댓값이
> 가운데 있다. 어느 쪽도 경로를 *따라* 잰 거리가 아니다.
> **왜 중요한가.** 둘의 비가 구간에 걸친 오차의 모양이고 — 여기서는 $1.00/0.60 = 1.67$ — 숫자
> 하나로는 보고되지 않으며, 플래너의 제약은 평균이 아니라 구간 끝에 걸린다.

스텝별 변위가 직각삼각형 셋에서 나오므로 산수가 정확히 떨어진다:

- $t+1$: $\hat x_1 - x_1 = (0.00,\ 0.30)$, $\lVert\cdot\rVert = 0.30$ m;
- $t+2$: $(0.30,\ 0.40)$, $\lVert\cdot\rVert = \sqrt{0.09 + 0.16} = 0.50$ m;
- $t+3$: $(0.60,\ 0.80)$, $\lVert\cdot\rVert = \sqrt{0.36 + 0.64} = 1.00$ m.

$$\mathrm{ADE} = \frac{0.30 + 0.50 + 1.00}{3} = \frac{1.80}{3} = 0.60\ \mathrm{m}, \qquad \mathrm{FDE} = 1.00\ \mathrm{m}$$

이제 출처의 Schöller 비판이 통째로 겨누는 그 기준선을 돌려 보자. 관측된 세 위치가 1 Hz에서 직선 위로 $1.00$ m씩 떨어져 있으므로 **등속** 외삽은 $x_t + k\,(1.00, 0)$, 즉 $(1,0), (2,0), (3,0)$ — 정답 그 자체다. 이 보행에서 $\mathrm{ADE}_{\mathrm{CV}} = \mathrm{FDE}_{\mathrm{CV}} = 0$이다.

대상을 일부러 그렇게 만들었고, 요점은 등속이 늘 정확하다는 게 아니다. 요점은 **출판된 $\mathrm{ADE} = 0.60$ m가 자기가 산수에 졌다는 사실을 말해 주지 않는다** 는 것이고, 어떤 벤치마크 표도 그걸 말할 의무가 없다는 것이다. 과제에서는 보행자가 방향을 틀고 순위가 뒤집힌다. 읽어야 할 것은 그 뒤집힘이지 두 숫자 중 어느 쪽도 아니다.

**5. 가용 지평 $\Delta^{*}$와 플랫폼이 요구하는 것.** 가용 지평 $\Delta^{*}$는 곡선이 여전히 요구를 만족하는 가장 긴 선행 시간이다(§3이 어떤 운용 지표에 대해서든 정의한다). 3부의 요구는 recall $\ge 0.75$다. 곡선은 $\Delta = 1.0$초에서 $0.84$, $1.5$초에서 $0.72$이므로 그 사이에서 가로지른다. 선형 보간하면 구간에서 쓴 비율이 $(0.84 - 0.75)/(0.84 - 0.72) = 0.09/0.12 = 0.75$이므로

$$\Delta^{*} = 1.0 + 0.75 \times (1.5 - 1.0) = 1.375\ \mathrm{s}$$

플랫폼 쪽 요구는 모델이 전혀 들어가지 않는 별개의 계산이다. 일정한 $a$로 $v$에서 제동하면 $t_{\mathrm{stop}} = v/a$가 걸리고 $v^2/2a$를 지나므로

$$t_{\mathrm{stop}} = \frac{1.5}{1.5} = 1.00\ \mathrm{s}, \qquad d_{\mathrm{stop}} = \frac{1.5^2}{2 \times 1.5} = 0.75\ \mathrm{m}, \qquad \Delta_{\mathrm{req}} = t_{\mathrm{stop}} + t_{\mathrm{lat}} = 1.00 + 0.45 = 1.45\ \mathrm{s}$$

$\Delta^{*} = 1.375\ \mathrm{s} < \Delta_{\mathrm{req}} = 1.45\ \mathrm{s}$. **75밀리초가 모자란다.** 그리고 헤드라인 AUC도, Brier 점수도, ECE도 그 사실을 말해 주지 않았을 것이다. 셋 다 $\Delta$를 평균으로 지워 버린 채 계산되기 때문이다.

쓸 만한 수는 그 모자람의 값을 묻는 것이다. 바꾸기 싼 쪽이 플랫폼이기 때문이다. $v/a + t_{\mathrm{lat}} \le \Delta^{*}$를 $v$에 대해 풀면

$$v \le a\big(\Delta^{*} - t_{\mathrm{lat}}\big) = 1.5 \times (1.375 - 0.45) = 1.39\ \mathrm{m/s}$$

이므로 베이스 속도를 $1.39\ \mathrm{m/s}$로 — $7\%$ — 낮추면 바로 이 예측기로 충분해진다. $t_{\mathrm{lat}}$에서 $75$ ms를 깎아도 같다. 어느 쪽도 더 나은 모델보다 작은 개입이고, 둘 다 벤치마크 표에서는 보이지 않는다. **예측기는 느리거나 빠른 것이 아니라, 로봇의 감속도와 지연에 비해 느리거나 빠르다.**

### 1. 서로 다른 두 문제

| | 의도 예측 | 궤적 예측 |
|---|---|---|
| 출력 | 이산 잠재 결정 — 건넌다/안 건넌다, 건넨다/거둔다 | 연속 미래 위치 $\hat{x}_{t+1:t+H}$ |
| 정답 | 일어났거나 안 일어난 사건 | 기록된 경로 |
| 지표 | 정확도·AUC·F1 — **time-to-event로 조건화된** | ADE / FDE, $k$개 샘플의 minADE |
| 실패 방식 | 확신에 찬 오분류 | 그럴듯하지만 틀린 모드 |
| 무엇을 먹이나 | 이산 결정(정지·경고·양보) | 연속 계획(코스트맵, MPC 제약) |

오른쪽 열에서 ADE(average displacement error)는 예측 위치와 실제 위치 사이의 유클리드 거리를 예측 구간 전체에 걸쳐 평균한 값, FDE(final displacement error)는 마지막 시점에서의 그 거리다. 둘의 조건과 반례를 갖춘 완전한 정의는 위의 I20 위에 있다. $k$개 샘플의 minADE는 샘플링한 $k$개 미래 중 가장 가까운 것만 남긴다(§6).

같은 네트워크로 풀고 같은 논문에서 보고되는 일이 잦지만 **같은 주장이 아니다.** "보행자 의도를 예측한다"와 "보행자 궤적을 예측한다"는 다른 질문에 답하고 다르게 실패한다. ADE가 낮은 궤적 모델도 횡단 모드에 확률을 전혀 주지 않으면 쓸모없고, 의도 분류기는 횡단 여부를 맞혀도 *어디로*를 말하지 않아 계획에 못 쓴다.

### 2. 관측 가능한 단서 사슬

의도는 잠재변수다. 측정 가능한 것을 선행 시간 순으로:

| 단서 | 선행 | 원거리 관측? | 출처 |
|---|---|---|---|
| 시선 | 가장 김 | 수 미터 넘으면 **불가** | [[04-robotics/human-pose-gaze\|21. §4]] |
| 머리·몸 방향 | 김 | 가능 | [[04-robotics/human-pose-gaze\|21. §4–§5]] |
| 보행 변화, 감속 | 중간 | 가능, 추적 박스로 | [[04-robotics/human-pose-gaze\|21. §5]] |
| 경계(연석·기계 반경)와의 근접 | 중간 | 가능, 경계가 같은 지면 좌표계에 있다면(아래) | [[04-robotics/hri-safety\|11.]], 그 위험 경계 |
| 목표를 향한 궤적 곡률 | 짧음 | 가능 | 위 §1 |
| 접촉·진입 | 0 | 가능 | 이미 늦음 |

근접은 사람만 보고 읽어 내는 것이 아니라 사람과 장면 사이의 관계다. 추적한 사람의 지면 위치 $x$에서 경계까지의 부호 있는 거리이고, 바깥쪽이 양수다. 기계 반경을 베이스 $x_{\mathrm{base}}$ 둘레 반지름 $R_h$의 원으로 두면 $d = \lVert x - x_{\mathrm{base}}\rVert - R_h$이며, [[04-robotics/hri-safety|11. HRI와 안전]]이 모든 이격 거리를 재는 기준 경계가 바로 이것이다(그 P2 셀에서 $R_h = 2.25$ m). 그것을 계산하려면 장면 기하 — 사람의 추적 궤적 말고도 입력 둘 — 가 필요하다. 하나는 로봇의 지면 좌표계에서의 경계 자체로, 현장 지도나 기계 자신의 도달 범위에서 온다. 다른 하나는 같은 좌표계에서의 사람의 지면 위치로, 깊이 센서에서 오거나, 추적 상자의 발 쪽 픽셀을 지나는 광선이 알려진 지면 평면과 만나는 점에서 온다([[04-robotics/geometric-perception-calibration|3.5 기하 인식 §1]], 핀홀 모형).

이는 [[04-robotics/egocentric-perception|22. §4]]와 같은 사슬을 머리가 아니라 바깥에서 본 것이다. **어떤 의도 시스템에서도 설계 결정은 어느 단에 걸 것인가이며**, 그 선택이 선행 시간과 신뢰도 상한을 동시에 고정한다.

> [!warning] "subtle cue" 함정
> 의도 정보를 가장 많이 담은 단서가 가장 먼저 분해 불가능해진다. 근거리나 계측 장비로 시선의 예측력을 입증한 연구가, 차량·로봇 카메라가 그것을 쓸 수 있음을 보인 것은 아니다. **단서를 측정한 거리와 시스템이 작동해야 하는 거리를 항상 밝혀라.**

### 3. 조기성 vs 정확도가 진짜 연구 대상이다

사건 시각을 $T$라 하면, 성능은 time-to-event $\Delta = T - t$의 함수로 보고돼야 한다:

$$\text{AUC}(\Delta), \qquad \text{Recall}_{\mathrm{FPR}=\alpha}(\Delta)$$

점수가 아니라 곡선으로 읽어라. 한 $\Delta$에서의 숫자 하나나 모든 $\Delta$의 평균은 배포 절충을 가리기 때문이다. AUC는 여러 임계값에서의 순위 판별력을 요약하지만 실제 행동에는 정해진 동작점, 보정, 비용이 필요하다. 배포 동작점의 지표에 대해 가용 지평 $\Delta^*$를 정의하자 — 다시 말해, 고른 지표가 요구조건을 아직 넘기는 가장 긴 선행 시간이다:

$$\Delta^{*} = \max\{\Delta : \text{동작점 지표}(\Delta) \geq \text{요구조건}\}$$

$\Delta^*$가 구동기의 정지 시간보다 짧은 시스템은 **예측기라는 이름을 쓴 검출기다.**

> [!example] 계산 예제 — 필요한 선행 시간 · Worked example
> 30 km/h($8.3\,\mathrm{m/s}$) 차량이 제동에 1.2초, 파이프라인 지연 0.3초 → 필요한 선행 1.5초. 같은 허용 오경보율에서 모델 A가 요구 recall을 1.15초까지만, 모델 B가 2.15초까지 만족한다고 하자(아래 그림). A는 peak AUC가 더 좋아도 **이 동작점의 제동 요구조건**을 만족하지 못한다. 동작점의 $\Delta^*$와 필요 선행 시간을 비교해야 하며 AUC만으로 제동 결정을 내릴 수 없다.

<svg viewBox="0 0 560 285" style="max-width:100%;height:auto" role="img" aria-label="사건 전 남은 시간에 대한 성능, 결정 임계값과 플랫폼이 요구하는 선행 시간과 함께">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="60" y1="190" x2="504" y2="190"/><line x1="60" y1="190" x2="60" y2="36"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="148" y1="190" x2="148" y2="195"/><line x1="236" y1="190" x2="236" y2="195"/><line x1="324" y1="190" x2="324" y2="195"/><line x1="412" y1="190" x2="412" y2="195"/><line x1="500" y1="190" x2="500" y2="195"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.45" stroke-dasharray="4 3">
    <line x1="60" y1="123.3" x2="504" y2="123.3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.75" stroke-dasharray="6 4">
    <line x1="324" y1="46" x2="324" y2="190"/>
  </g>
  <path d="M 60.0 63.3 L 130.4 73.3 L 200.8 90.0 L 262.4 123.3 L 324.0 146.7 L 412.0 166.7 L 500.0 180.0" fill="none" stroke="currentColor" stroke-width="1.8" opacity="0.9"/>
  <path d="M 60.0 100.0 L 130.4 103.3 L 200.8 106.7 L 271.2 108.3 L 324.0 110.0 L 412.0 113.3 L 438.4 123.3 L 500.0 146.7" fill="none" stroke="currentColor" stroke-width="1.8" opacity="0.9" stroke-dasharray="7 3"/>
  <g fill="currentColor"><circle cx="262.4" cy="123.3" r="4"/><circle cx="438.4" cy="123.3" r="4"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="150" y="58">모델 A</text>
    <text x="150" y="96">모델 B</text>
    <text x="64" y="137" font-size="9.5" opacity="0.85">요구 recall</text>
    <text x="330" y="42" font-size="9.5" opacity="0.85">필요 선행 1.5초</text>
    <text x="258" y="147" text-anchor="end" font-size="10">&#916;*&#7488;</text>
    <text x="446" y="115" font-size="10">&#916;*&#7495;</text>
    <text x="54" y="44" text-anchor="end" font-size="9.5">1.0</text><text x="54" y="127" text-anchor="end" font-size="9.5">0.75</text><text x="54" y="177" text-anchor="end" font-size="9.5">0.6</text>
    <text x="60" y="206" text-anchor="middle" font-size="9.5">0</text><text x="148" y="206" text-anchor="middle" font-size="9.5">0.5</text><text x="236" y="206" text-anchor="middle" font-size="9.5">1.0</text><text x="324" y="206" text-anchor="middle" font-size="9.5">1.5</text><text x="412" y="206" text-anchor="middle" font-size="9.5">2.0</text><text x="500" y="206" text-anchor="middle" font-size="9.5">2.5</text>
    <text x="282" y="222" text-anchor="middle" font-size="9.5">사건까지 남은 시간 &#916; (초)</text>
    <text x="14" y="112" font-size="9.5">recall @ FPR=α</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="243">모델 A가 헤드라인 숫자는 더 좋지만 여기서는 쓸 수 없다: 가용 지평</text>
    <text x="20" y="259">&#916;* = 1.15초가 이 플랫폼에 필요한 1.5초에 못 미치고, 모델 B는 2.15초까지</text>
    <text x="20" y="275">요구 recall을 유지한다. 최고 성능이 아니라 &#916;*를 필요 선행과 비교하라.</text>
  </g>
</svg>

### 4. 보정(calibration) — 여기가 논문이 될 부분이다

확률을 출력하는 예측기는 그 확률이 의미를 가질 때만 하위에서 쓸모가 있다. 보정은 이렇게 묻는다:

$$\mathbb{P}\big(y = 1 \mid \hat{p} = p\big) \;\overset{?}{=}\; p$$

모델이 0.7이라 말한 사례 전체에서 사건이 70% 일어났는가? 딥 분류기는 **일상적으로 과확신**이고, 표준 처방은 싸다:

| 도구 | 주는 것 | 비용 |
|---|---|---|
| Reliability diagram, ECE | 오보정의 그림과 스칼라 | 무료, 진단만 |
| Temperature scaling | held-out으로 재보정된 확률 | 파라미터 1개 |
| **Conformal prediction** | 교환가능성 하에 **분포 무관 커버리지 보장**이 붙은 집합/구간 | held-out 보정 집합 |

ECE(expected calibration error)는 그 그림 뒤의 스칼라다. 예측을 $\hat p$ 구간(bin)으로 나누고, 구간마다 실제 사건 빈도와 평균 $\hat p$의 차이를 구한 뒤, 구간에 든 사례 수로 가중 평균한다. 위의 I20에서 끝까지 계산해 두었는데, 똑같은 스무 예측이 5구간에서 $0.100$, 10구간에서 $0.270$을 준다. 그러니 **두 ECE를 비교하기 전에 논문의 구간 나누기를 물어라.** I20 구간들의 부호 패턴이 이 행이 진단하는 과확신이다. Temperature scaling은 held-out 데이터로 맞춘 스칼라 하나 $T$로 로짓을 나눈다. $T$가 클수록 softmax가 평평해지므로([[02-foundations/calculus-backprop|2. 미적분과 역전파 §6]]) 어느 클래스가 1등인지는 바꾸지 않은 채 과확신 확률을 균등 쪽으로 당긴다: 로짓 $(2, 0)$은 $T = 1$에서 0.88, $T = 2$에서 0.73이 된다.

Conformal prediction의 수학은 교환가능성(보정 사례와 새 사례가 어떤 순서로 도착해도 확률이 같다는 가정; i.i.d. 추출이면 성립하지만 그보다 약한 가정이다) + 분위수이며, 집합 출력은 defer 정책에 유용하다. 다만 보통의 보장은 교환가능한 사례 전체에 대한 **주변적 coverage**이지 이 한 장면이나 모든 하위집단의 90% 확률이 아니다. `횡단`과 `비횡단`이 모두 든 집합에는 감속이나 사람에게 질문하기 같은 별도 행동 규칙이 필요하다. [[04-robotics/hri-safety|11. HRI & Safety]]로 이어진다.

> [!example] 계산 예제 · Worked example
> **conformal 구간 만들기.** held-out 보행자 10명에서 2초 뒤 예측 위치와 실제 위치 사이 거리(m)가 0.2, 0.3, 0.35, 0.4, 0.5, 0.55, 0.6, 0.7, 0.9, 1.4였다. 90% coverage($\alpha = 0.1$)를 원하면 split conformal은 $\lceil (n+1)(1-\alpha) \rceil = \lceil 11 \times 0.9 \rceil = 10$번째로 작은 잔차, 즉 1.4 m를 쓴다. 따라서 새 보행자에 대한 출력은 예측 지점을 중심으로 한 반지름 1.4 m 원판이고, 교환가능한 사례의 최소 90%에서 실제 위치를 담는다.
>
> **여기서 얻는 독법.** 보정 사례가 10개뿐이면 규칙이 가장 큰 잔차를 고르므로 특이한 보행자 한 명이 반지름을 정한다. 좁은 구간을 얻으려면 배포 분포에서 온 보정 데이터가 충분해야 한다.

**보정된 0.7은 결정 규칙을 지지한다. 보정 안 된 0.9는 그러지 못한다.**

### 5. 클래스 불균형과 기저율

도로 근처 보행자 대부분은 다음 2초 안에 건너지 않고, 기계 근처 작업자 대부분은 작업반경에 들어가지 않는다. 양성률 수 %가 정상이고, 귀결이 둘이다:

- **정확도는 무의미하다.** 무조건 "아니오"가 95% 이상을 받는다. AUC와 **precision–recall**(불균형에서 낙관적인 ROC 단독이 아니라), 그리고 실제 사용한 동작점을 보고하라.
- **배포 임계값에서의 precision이 전부다.** precision 20%인 경고 시스템은 참 하나당 오경보 넷을 낸다. 보호하려던 작업자가 무시하거나 꺼버린다. **알람 피로는 인간의 결함이 아니라 시스템 실패 양식이다.**

> [!example] 계산 예제 — 기저율 · Worked example
> **90%짜리 검출기가 꺼지는 이유.** 횡단 의도 검출기가 오탐률 5%에서 정탐률 90%를 낸다고 하자.
> 그리고 그것이 예측하는 사건 — 작업자가 앞으로 2초 안에 로봇 경로로 들어오는 것 — 은 판정
> 프레임의 2%에서 참이다. 그러면
>
> $$\text{정밀도} = \frac{0.90 \times 0.02}{0.90 \times 0.02 + 0.05 \times 0.98} = \frac{0.0180}{0.0670} = \mathbf{26.9\%}$$
>
> 정지 열 번 중 일곱 번이 헛것이다. 8시간 교대 동안 초당 한 번 판정하면 28,800번이고, 그중
> $0.98 \times 28{,}800 \times 0.05 = \mathbf{1{,}411}$번이 오경보다 — 분당 세 번꼴. 그런
> 시스템을 켜 두는 작업조는 없다.
>
> **필요한 조건.** 같은 2% 기저율에서 정밀도 90%에 닿으려면
> $0.90 \times 0.02 = 0.90\,(0.90 \times 0.02 + \text{FPR} \times 0.98)$을 FPR에 대해 풀면
> FPR = 0.2%가 나온다. 오탐률이 **25배** 떨어져야 하고, 현실적인 정탐률(0.8–1.0) 안에서 정탐률은 그 요구를 비례적으로만 옮긴다 — 지렛대는 오탐률이다.
>
> **여기서 얻는 독법.** ROC 곡선과 AUC는 이것을 완전히 가린다. 둘 다 기저율과 무관하기
> 때문이다. 균형 잡힌 데이터셋에서 AUC를 보고한 의도 논문이 2% 양성인 현장에 놓이면, 보고된
> 숫자와 운용상의 숫자는 서로 다른 질문에 답하고 있는 것이다. *배포 기저율 위에서, 명시된
> 재현율에 대한 정밀도*를 찾아라. 논문이 주지 않는다면 그 ROC 점과 논문 자신의 설정이 함축하는
> 비율로 직접 계산할 수 있다.

### 6. 궤적 예측, 간단히

출력이 결정이 아니라 경로일 때, 이 문헌의 대표 지표는 ADE와 FDE의 best-of-$k$ 판이다.

> [!info] 정의 — $\mathrm{minADE}_k$와 $\mathrm{minFDE}_k$
> 두 개의 **미터 단위 길이** 이고, ADE와 FDE의 best-of-$k$ 판이다. 모델이 관측 이력 하나에 대해 미래
> 샘플 $k$개를 뽑고, 정답에 가장 가까운 샘플 하나만 채점한다. 조건이 넷이다. $k$개 샘플은 **이력
> 하나에 대한 예측기 하나** 에서 나오고, $k$는 이름의 일부다. $\mathrm{minADE}_5$와 $\mathrm{minADE}_{20}$은
> 다른 양이다. 최솟값은 **궤적 전체** 에 대해 취한다 — 샘플마다 예측 구간 전체의 ADE를 계산한 뒤 가장
> 좋은 샘플을 남기는 것이지, 스텝마다 가장 좋은 샘플을 고르는 것이 아니다. $\mathrm{minADE}_k$와
> $\mathrm{minFDE}_k$는 **각자의** 최솟값을 취하므로 서로 다른 샘플에서 점수가 나올 수 있다. 그리고
> **확률이 들어가지 않는다.** 모델이 샘플에 어떤 가중치를 두든 무시되고, 벤치마크 숫자는 이 사례별
> 값을 테스트 사례에 걸쳐 평균한 것이다.
> $$\mathrm{minADE}_k=\min_{m=1,\dots,k}\frac{1}{H}\sum_{t=1}^{H}\big\lVert\hat x^{(m)}_t-x_t\big\rVert_2,\qquad \mathrm{minFDE}_k=\min_{m=1,\dots,k}\big\lVert\hat x^{(m)}_H-x_H\big\rVert_2$$
> $\hat x^{(m)}_t$는 샘플 $m$의 스텝 $t$ 위치이고, $x_t$와 $H$는 유도 4단계 ADE 상자와 같다.
> **예.** 2부의 직선 보행에서, 샘플 $k = 2$개 — 모델의 휘는 경로와 등속 직선 — 를 내는 예측기를
> 생각하자. 두 샘플의 ADE는 $0.60$과 $0.00$ m이므로 $\mathrm{minADE}_2 = 0.00$ m, $\mathrm{minFDE}_2 = 0.00$ m다
> — 두 추측 중 무엇을 믿는지 끝내 말하지 않은 예측기가 만점을 받는다. 뒤로 걷는 셋째 샘플
> $(-1, 0), (-2, 0), (-3, 0)$을 더하면 오차는 $2$, $4$, $6$ m이고 ADE는 $4.00$ m지만, $\mathrm{minADE}_3$은
> 여전히 $0.00$이다. 샘플을 더해서 최솟값이 커질 수는 없기 때문이다.
> **반례.** $k$개 샘플의 ADE 평균은 $\mathrm{minADE}_k$가 아니다. 두 샘플 집합에서는 $(0.60 + 0.00)/2 = 0.30$ m,
> 세 샘플에서는 $(0.60 + 0.00 + 4.00)/3 = 1.53$ m다. 그 평균은 뒤로 걷는 추측을 벌하지만
> $\mathrm{minADE}_k$는 벌할 수 없다.
> **왜 중요한가.** 이 지표가 재는 것은 **커버리지** — 어떤 샘플이 가까이 왔는가 — 이고, 플래너에게
> 필요한 것은 각 미래의 확률인데 이 숫자는 그것을 한 번도 묻지 않는다. §8이 적는 함정이 그것이다.

여기서 세 가지가 따른다:

- **다중모드성이 핵심이다.** 미래는 진짜로 다가(多價)다. 경로 하나를 회귀하는 모델은 양립 불가능한 선택지를 평균해서 아무도 걷지 않을 궤적을 만든다. $k$개 샘플에 대한 $\text{minADE}_k$/$\text{minFDE}_k$를 보고하되, 이 지표는 **보정이 아니라 커버리지를 보상**한다는 걸 알아라 — 다양하게 뿌리고 아무것도 믿지 않는 모델이 이길 수 있다.
- **상호작용이 중요하다.** 보행자는 서로에게, 차량에게 조건화된다. Social pooling·그래프·어텐션 모델이 존재하는 이유다.
- **지표 주의.** $k=20$의 minADE는 "스무 번 추측 중 하나가 가까웠다"는 뜻이다. 쓸 수 있는 예측과 같지 않고, 플래너는 확률 없이 스무 개의 미래를 소비할 수 없다.

### 7. 도로에서 공유 작업공간으로

정식화는 치환 셋으로 인간–로봇 협업에 옮겨간다:

| 도로 상황 | 공유 작업공간 |
|---|---|
| 횡단 / 비횡단 | 작업공간에 손 넣기, 물건 건네기, 반경 안으로 들어서기 |
| 연석, 횡단보도 | 통제구역, 기계 작업반경, 작업 경계 |
| 차량이 정지를 계획 | 로봇이 감속·양보·재계획하거나 **묻는다** |
| 보행자는 낯선 사람 | 작업자는 훈련됐고 반복되며 **로봇에 적응한다** |

마지막 행이 실질적 차이이자 진짜 연구 개구부다. **매일 같은 로봇과 일하는 작업자는 그 로봇에 반응해 행동을 바꾼다.** 그래서 예측기가 배포됐다는 사실 때문에 학습 분포가 이동한다. 도로 횡단 데이터셋에는 이런 피드백 루프가 없다. 도로에서 학습한 의도 모델이 현장에 전이된다고 주장하려면 이걸 다뤄야 한다. 예측을 로봇의 결정 안에 넣는 두 형식 — QMDP로 행동을 고르는 목표 추론, 그리고 사람이 로봇에 반응하는 Stackelberg 게임(바로 이 피드백 루프) — 은 [[04-robotics/hri-safety|11. HRI·안전 §3.5]]에 있다.

### 8. 이 문헌 특유의 평가 함정

| 함정 | 무엇이 잘못되나 |
|---|---|
| 관측 창 누수 | 사건 시점 이후 프레임이 입력에 들어감 → 성능 부풀림, 모델은 검출기 |
| 사람·장면이 아니라 클립으로 분할 | 같은 보행자가 train과 test에 등장 → 암기를 측정 |
| time-to-event에 대해 평균 | 배포에 유일하게 중요한 $\Delta^*$를 가림 |
| 심한 불균형에서 ROC | 강해 보이는데 임계값에서의 precision은 못 씀 |
| minADE$_k$만 보고 | 다양성을 보상하고 믿음을 보상하지 않음; 플래너에 줄 확률이 없음 |
| 장면 맥락 누수 무시 | 횡단보도 위치만으로 횡단이 예측됨 → 모델이 사람을 안 볼 수도 |

마지막 항목은 [[04-robotics/video-action-understanding|20. §2]]의 장면 편향과 같은 처방이 필요하다: **사람을 ablate 하라.** 보행자를 마스킹한 모델이 거의 같은 성능이면, 그 논문은 의도 모델이 아니라 **장면 사전확률**을 만든 것이다.

### 9. 주장과 평가 읽기

| 논문 문구 | 받아들이기 전에 확인할 것 |
|---|---|
| 보행자 의도를 예측한다 | 의도 분류인가 궤적인가; time-to-event 곡선이 있는가 |
| 조기 예측 | 배포 임계값에서 $\Delta^*$가 얼마인가 |
| 불확실성 인지 | 보정을 측정했는가(ECE, reliability diagram), softmax만 보고했는가 |
| SOTA를 능가 | 같은 분할 프로토콜인가; 사람·장면 분할인가 클립 분할인가 |
| 미묘한 행동 단서 사용 | 그 단서가 어느 거리에서 분해됐나; 사람 마스킹 ablation |
| real-time | 검출·추적 포함 end-to-end 지연, 그리고 그것을 필요 선행에 더했는가 |

### 읽고 나면 말할 수 있어야 하는 것

다음을 할 수 있어야 한다:

- 의도 분류와 궤적 예측의 차이와 각각의 지표를 말한다;
- 주어진 로그에서 Brier 점수·Brier skill score·구간 ECE를 계산하고, 구간 나누기가 마지막 값에 무슨 짓을 했는지 말한다;
- 예측 경로와 같은 경로의 등속 기준선에 대해 ADE와 FDE를 계산한다;
- 가용 지평 $\Delta^*$를 계산하고 필요 선행 시간과 비교한다;
- 보정을 설명하고, 고치는 방법 둘을 들고, conformal prediction이 안전 결정에 맞는 이유를 말한다;
- 낮은 기저율에서 정확도가 왜 틀린 지표인지 설명한다;
- 사람 마스킹 ablation과 그것이 검증하는 바를 말한다;
- 도로 보행자와 반복 협업 작업자 사이의 피드백 루프 차이를 말한다.

> [!tip] 더 깊이 · Going deeper
> 교과서는 없고, §1의 두 절반은 서로 다른 길로 간다. 의도 분류 쪽은 PIE(ICCV 2019)가 기준 데이터셋이고 그 논문이 문제를 가장 깔끔하게 진술한다. 궤적 예측 쪽은 Social LSTM(CVPR 2016) 다음 Social GAN(CVPR 2018)을 읽어라 — 두 번째가 존재하는 이유는 첫 번째가 미래가 여럿인 문제에 하나의 미래를 예측했기 때문이고, 그 이견은 지금도 이 분야의 살아 있는 질문이다. §4의 보정은 이 분야 고유의 주제가 아니다. 그 기계장치는 아래 출처의 Guo 외(ICML 2017, 신경망 보정)와 Angelopoulos & Bates(conformal prediction)에 있다.

### 스스로 점검

1. 어떤 모델이 횡단 예측에서 96% 정확도를 보고했다. 왜 정보가 없고, 대신 무엇을 보고해야 하나?
2. 로봇이 정지에 0.9초 필요하다. 같은 허용 FPR에서 A는 요구 recall을 $\Delta=0.5$s까지만, B는 $\Delta=1.5$s까지 만족한다. 어느 쪽이 이 운용 요구를 만족하며, AUC만으로는 무엇을 결정하지 못하는가?
3. minADE$_{20}$에서 이기고도 플래너가 못 쓰는 이유는?
4. 의도 모델이 실제로 사람을 읽는지 검증하는 단일 ablation은?
5. 현장 의도 모델의 학습 분포가 도로 데이터셋과 달리 비정상(non-stationary)인 이유는?

> [!tip]- 정답
> 1. 기저율 때문 — 무조건 "아니오"가 비슷한 점수를 받는다. 순위 판별용 AUC와 precision–recall, 선택한 배포 동작점을 time-to-event의 함수로 보고해야 한다. 2. B가 이 요구를 만족하고 A는 해당 동작점에서 선행 시간이 부족하다. AUC만으로는 임계값·제동 비용·보정을 결정하지 못한다. 3. minADE는 스무 개 중 운 좋은 하나를 보상한다; 플래너는 미래에 대한 확률분포가 필요한데 지표가 그것을 요구하지 않는다. 4. 보행자를 마스킹·제거하고 재평가한다; 성능이 비슷하면 장면 사전확률을 학습한 것이다. 5. 작업자가 배포된 로봇에 적응하므로 배포 자체가 데이터 생성 과정을 바꾼다 — 수동적 도로 녹화에는 없는 피드백 루프다.

**계산: 이 페이지가 허가하는 세 가지 주장 읽기.** "아니오" 기저율이 94%인 데서 96% 정확도는 무조건 "아니오"의 점수다. minADE$_{20}=0.18\,\mathrm{m}$는 정지에 쓸 보정된 집합을 주지 않는다. 4주 차 현장 레이블은 JAAD가 아니다. 동료 작업자들이 로봇에 적응했다.

### 과제 · Problem set

Tier A. 위의 대상 **I20**, 그리고 이 페이지만 사용한다. 결과 하나가 뒤집히고, 보행자가 방향을 틀고, 플랫폼이 바뀐다. 스무 개의 예측은 그대로다.

1. **그려라.** 바뀐 대상으로 위의 그림의 패널 둘을 다시 그려라. 패널 1: $0.90$을 예측했던 19번 사례가 사실은 $y = 1$이었다고 하자. 점 하나가 어느 방향으로 움직이는지 표시하고, 그것이 향해 가는 대각선을 표시하라. 패널 2: 같은 time-to-event 곡선을 더 빠른 플랫폼($v = 2.0\ \mathrm{m/s}$, $a = 1.6\ \mathrm{m/s^2}$, $t_{\mathrm{lat}} = 0.30$초)에 대해 그리고, 수직선 둘과 그 사이 부호 있는 간격을 표시하라.
2. **유도하라.** (a) 19번 사례를 $y = 1$로 뒤집고 나머지는 그대로일 때, 새 Brier 점수·새 기저율·새 Brier skill score·새 5구간 ECE. (b) 2부의 보행자가 직진 대신 방향을 튼다. 참 미래가 $(1.00,\ 0.15)$, $(2.42,\ 0.56)$, $(3.75,\ 1.00)$이고 관측 이력과 모델 예측은 그대로다. 모델과 등속 기준선의 ADE·FDE를 구하라. (c) $\Delta^{*}$는 $1.375$초로 그대로다. 패널 2의 더 빠른 플랫폼에 대해 $\Delta_{\mathrm{req}}$를 구하고 이제 통과하는지 말하라.
3. **해석하라.** 업체가 (a)의 결과를 읽고 "재보정 완료: ECE가 $0.100$에서 $0.090$으로 개선"이라 보고한다. (a)에서 구한 셋 중 둘은 ECE보다 훨씬 크게 움직였다. 로그에서 실제로 바뀐 것이 무엇인지, ECE가 셋 중 그것에 가장 둔감한 이유가 무엇인지, 그리고 업체에 대신 무엇을 요구할지 말하라.

4. **실행.** 영어 절 템플릿의 `?`를 채워, 스크립트 하나가 I20에서 풀이 전체를 다시 계산하게 하라. Brier, 기술 점수, 다섯 칸 ECE와 AUC. 모형과 등속 기준선의 ADE와 FDE. 필요한 선행 시간에 맞선 $\Delta^{*}$. 각각을 페이지와 맞춰 본다. 그다음 페이지가 주장만 하는 세 가지에 써라. 모든 예측을 제곱해 AUC는 그대로이고 Brier와 ECE는 움직이는지 확인하고, ECE를 $2$칸과 $10$칸으로 다시 계산하고, 사례 19를 뒤집어 2(a)를 확인한다. 제곱한 예측기의 기술 점수는 ECE가 말하지 않는 무엇을 말하는가?

> [!note]- 그리는 법 · How to draw it
> - **패널 1, reliability diagram.** 단위 정사각형에 가로는 $\hat p$, 세로는 관측 빈도, 그리고 보정된 선인 $45^\circ$ 대각선을 긋는다.
> - **가로축을 등폭 5구간으로 나눈다.** 구간마다 (구간 평균 $\hat p$, 구간 관측 빈도)에 점 하나를 찍고, 축 위에 스무 사례 중 몇 개가 그 구간에 들었는지 막대로 표시한다.
> - **각 점에서 대각선까지 수직 간격을 그리고 값을 적는다.** 그 다섯 간격의 가중 평균이 §4 스칼라의 전부다. 대각선 아래의 점은 과신, 위의 점은 과소 확신이다.
> - **패널 2, time-to-event 곡선.** 가로는 $\Delta$, 세로는 recall, 3부의 다섯 점을 잇고, $0.75$에 수평 요구선을 긋는다.
> - **곡선이 요구선을 가로지르는 지점에서 수직선을 내려 $\Delta^{*}$라 적는다.** 그다음 필요 선행 $t_{\mathrm{stop}} + t_{\mathrm{lat}}$($t_{\mathrm{stop}} = v/a$)에 두 번째 수직선을 긋는다. 두 수직선 사이의 부호 있는 거리가 답이고, 그 부호가 배포 결정이다.
> - **패널 2 옆에는 2부의 궤적을 위에서 본 그림.** 관측된 세 위치, 참 미래 세 위치, 예측 세 위치.
> - **ADE가 평균하는 변위 선분 셋을 그리되 마지막 하나만 굵게 그린다.** 그것 혼자가 FDE다.

> [!tip]- 정답 · Solutions
> 1. 패널 1: 맨 위 구간의 점 하나만 $(0.90,\ 0.75)$에서 $(0.90,\ 1.00)$으로 올라간다. 대각선을 지나쳐, 빈도가 예측에 못 미치던 과신 쪽에서 예측을 넘어서는 과소 확신 쪽으로 간다. 나머지 네 점과 다섯 막대는 그대로다. 뒤집힌 것이 예측이 아니라 결과이기 때문이다. 패널 2: $\Delta^{*}$는 $1.375$초로 그대로인데 필요 선행 수직선이 $1.55$초로 밀려나, $-0.075$초였던 간격이 $-0.175$초가 된다. 더 빠르고 지연이 짧은 베이스가 오히려 나빠지는 이유는 $v/a$가 늘어난 폭이 $t_{\mathrm{lat}}$이 줄어든 폭보다 크기 때문이다.
> 2. (a) 19번의 잔차가 $(0.90-0)^2 = 0.81$에서 $(0.90-1)^2 = 0.01$로 바뀌어 합계가 $4.515$에서 $3.715$가 되므로 $\mathrm{BS} = 3.715/20 = \mathbf{0.1858}$이다. 기저율은 $10/20 = \mathbf{0.50}$, 기준은 $0.50 \times 0.50 = 0.2500$, 따라서 $\mathrm{BSS} = 1 - 0.1858/0.2500 = \mathbf{0.257}$. ECE는 맨 위 구간 항만 바뀌어 빈도가 $0.75$에서 $1.00$, 간격이 $0.15$에서 $|1.00-0.90| = 0.10$이 되므로 $\mathrm{ECE} = 0.2\,(0.15 + 0 + 0 + 0.20 + 0.10) = \mathbf{0.090}$이다.
> (b) 모델 오차 $\hat x_k - x_k$: $(0.00,\ 0.15) \to 0.15$, $(-0.12,-0.16) \to 0.20$, $(-0.15,-0.20) \to 0.25$. $\mathrm{ADE} = 0.60/3 = \mathbf{0.20\ \mathrm{m}}$, $\mathrm{FDE} = \mathbf{0.25\ \mathrm{m}}$. 등속은 여전히 $(1,0), (2,0), (3,0)$을 내놓아 오차가 $\lVert(0,-0.15)\rVert = 0.15$, $\lVert(-0.42,-0.56)\rVert = 0.70$, $\lVert(-0.75,-1.00)\rVert = 1.25$이므로 $\mathrm{ADE}_{\mathrm{CV}} = 2.10/3 = \mathbf{0.70\ \mathrm{m}}$, $\mathrm{FDE}_{\mathrm{CV}} = \mathbf{1.25\ \mathrm{m}}$다. 같은 모델, 같은 기준선인데 직진 보행에서와 순위가 완전히 뒤집혔다. 그것이 읽어야 할 바다. ADE는 모델에 관한 진술인 만큼이나 *시험 집합의 움직임* 에 관한 진술이고, 그래서 모든 표에 등속 대조군이 들어가야 한다.
> (c) $t_{\mathrm{stop}} = 2.0/1.6 = 1.25$초, $\Delta_{\mathrm{req}} = 1.25 + 0.30 = 1.55$초 $> 1.375$초. 통과하지 못하고, 전보다 더 못 미친다. 제동거리도 $0.75$ m에서 $2.0^2/(2\times1.6) = 1.25$ m로 늘어난다.
> 3. 바뀐 것은 스무 건 중 결과 하나다. 모델이 아니다. 모델은 두 판본 모두에서 똑같은 스무 확률을 내놓았다. 그런데 Brier 점수는 $18\%$ 움직였고 skill score는 $0.088$에서 $0.257$로 거의 세 배가 된 반면 ECE는 $10\%$만 움직였다. ECE가 차이를 내기 전에 각 구간을 빈도 하나로 눌러 버리기 때문이고, 네 건짜리 구간 안에서 $0.75 \to 1.00$은 유계인 간격에 작은 변화인 데 비해 같은 뒤집힘이 로그에서 가장 큰 제곱 잔차 하나를 통째로 없애기 때문이다. 업체에는 $N$, 구간 나누기, 기저율, 기저율 예측기 대비 Brier skill score, 그리고 reliability diagram 자체를 요구하라. $N = 20$에서 ECE 하나는 작업자 한 사람의 오후가 어느 쪽으로든 밀어낼 수 있는 숫자다.
> 4. 빈칸은 영어 절 정답과 같다. 스크립트는 `I20 (0.22575, 0.088, 0.1, 0.7172)`와 `squared (0.24898, -0.006, 0.1765, 0.7172)`, `ECE by bins [0.055, 0.1, 0.27]`, `model (0.6, 1.0) cv (0.0, 0.0)`, `usable 1.375 required 1.45`, `flipped (0.18575, 0.257, 0.09, 0.795)`를 찍는다. 풀이의 모든 숫자, 3단계의 두 비예, 그리고 2(a)다. 제곱한 예측기의 기술 점수는 $-0.006$으로, 이제 늘 기저율을 말하는 것보다 *나쁘다*. ECE $0.177$은 그것을 "덜 보정됐다"로만 전하고, 그대로인 AUC는 전혀 전하지 않는다. 뒤집기는 어느 사례가 사건인지를 바꾸므로 AUC도 $0.7172$에서 $0.795$로 움직인다.
### 출처

**보행자 의도**

- A. Rasouli, I. Kotseruba, T. Kunic, and J. K. Tsotsos, "PIE: A Large-Scale Dataset and Models for Pedestrian Intention Estimation and Trajectory Prediction," [*ICCV 2019*](https://openaccess.thecvf.com/content_ICCV_2019/html/Rasouli_PIE_A_Large-Scale_Dataset_and_Models_for_Pedestrian_Intention_Estimation_ICCV_2019_paper.html).
- A. Rasouli, I. Kotseruba, and J. K. Tsotsos, JAAD — [Joint Attention in Autonomous Driving](https://data.nvision2.eecs.yorku.ca/JAAD_dataset/), *ICCVW 2017*.

**궤적 예측 — 검증된 인용**

- A. Alahi, K. Goel, V. Ramanathan, A. Robicquet, L. Fei-Fei, and S. Savarese, "Social LSTM: Human Trajectory Prediction in Crowded Spaces," *CVPR 2016*, pp. 961–971 — 사람마다 LSTM 하나에 공간 이웃을 묶는 social pooling 층을 얹는다. arXiv 프리프린트가 없다. CVF나 IEEE 기록을 인용하라.
- A. Gupta, J. Johnson, L. Fei-Fei, S. Savarese, and A. Alahi, "Social GAN: Socially Acceptable Trajectories with Generative Adversarial Networks," *CVPR 2018*, pp. 2255–2264. [arXiv:1803.10892](https://arxiv.org/abs/1803.10892) — 과제를 다봉(multimodal) 문제로 재정의하고, 다양한 표본을 명시적으로 보상하는 variety loss를 쓴다.
- T. Salzmann, B. Ivanovic, P. Chakravarty, and M. Pavone, "Trajectron++: Dynamically-Feasible Trajectory Forecasting with Heterogeneous Data," *ECCV 2020*. [arXiv:2001.03093](https://arxiv.org/abs/2001.03093) — 에이전트 동역학을 강제해 운동학적으로 실현 가능한 출력만 내고, 자차의 계획에 조건부로 예측할 수 있다. 마지막 성질 덕분에 계획 루프 *안에서* 쓸 수 있다.

**벤치마크, 그리고 그 프로토콜의 출처**

- S. Pellegrini, A. Ess, K. Schindler, and L. van Gool, "You'll Never Walk Alone: Modeling Social Behavior for Multi-Target Tracking," *ICCV 2009*, pp. 261–268 — ETH와 HOTEL 장면.
- A. Lerner, Y. Chrysanthou, and D. Lischinski, "Crowds by Example," *Computer Graphics Forum*, vol. 26, no. 3, pp. 655–664, 2007 (Eurographics) — UNIV, ZARA1, ZARA2 장면.
- A. Robicquet, A. Sadeghian, A. Alahi, and S. Savarese, "Learning Social Etiquette: Human Trajectory Understanding in Crowded Scenes," *ECCV 2016*, pp. 549–565 — Stanford Drone Dataset. 캠퍼스 8개 장면, 보행자·자전거·스케이트보드·자동차·버스·골프카트 약 19,000 에이전트.

> [!note] "ETH/UCY 벤치마크"는 데이터셋이 아니라 관행이다
> 두 원논문 중 어느 쪽도 예측 벤치마크로 쓰려고 만든 것이 아니다. 하나는 추적 논문이고
> 다른 하나는 군중 시뮬레이션 저작 논문이다. 2.5 Hz에서 8프레임 관측·12프레임 예측이라는
> 5장면 leave-one-out 프로토콜은 2016년 Social LSTM이 정한 뒤 검토 없이 상속되어 왔다.
> 평가를 논한다면 바로 그 내력이 핵심이다.

**비판 — 리더보드를 믿기 전에 읽어라**

- C. Schöller, V. Aravantinos, F. Lay, and A. Knoll, "What the Constant Velocity Model Can Teach Us About Pedestrian Motion Prediction," *IEEE RA-L*, vol. 5, no. 2, 2020 (ICRA 2020). [arXiv:1903.07933](https://arxiv.org/abs/1903.07933) — 등속 모델이 표준 벤치마크에서 최신 신경망 예측기를 이긴다. 진단은 네 가지다. 추가 입력을 활용하지 못하고, 대신 데이터셋 편향을 학습하며, 운동 이력을 거의 쓰지 않고, 이 정도 데이터로는 상호작용을 배울 수 없다.
- O. Makansi, J. von Kügelgen, F. Locatello, et al., "You Mostly Walk Alone: Analyzing Feature Attribution in Trajectory Prediction," *ICLR 2022*. [arXiv:2110.05304](https://arxiv.org/abs/2110.05304) — Shapley 값 기반 기여도 분석으로, 이 방법들이 실제로는 상호작용을 추론하지 않음을 보인다. Schöller의 실험 결과에 대한 메커니즘 설명이다. 둘을 함께 인용하면 각각보다 강하다.

**공유 작업공간에서의 의도 — 조작과 직결되는 계보**

- H. S. Koppula and A. Saxena, "Anticipating Human Activities Using Object Affordances for Reactive Robotic Response," *IEEE TPAMI*, vol. 38, no. 1, 2016 (이전 판본 *RSS 2013*) — 물체 어포던스 위의 anticipatory temporal CRF. "궤적이 아니라 의도"의 정본 인용이다. 사람이 *어느 물체로* 무엇을 하려는지를 예측한다.
- J. Mainprice and D. Berenson, "Human-Robot Collaborative Manipulation Planning Using Early Prediction of Human Motion," *IROS 2013*, pp. 299–306 — 사람의 작업공간 점유를 쓸고 지나간 부피로 예측한 뒤 그것을 피해 계획한다. 예측을 실제 계획 비용으로 바꾸는 참조점이다.
- R. Luo, R. Hayne, and D. Berenson, "Unsupervised Early Prediction of Human Reaching for Human-Robot Collaboration in Shared Workspaces," *Autonomous Robots*, vol. 42, pp. 631–648, 2018 — 오프라인 학습도 라벨링도 없이 온라인으로 학습하는 2층 GMM으로, 새로운 작업자에 적응한다. 특정 작업자로 사전학습할 수 없는 실제 셀에 가장 직접적으로 맞는다.

**보정**

- C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," *ICML 2017*. [arXiv:1706.04599](https://arxiv.org/abs/1706.04599)
- A. N. Angelopoulos and S. Bates, "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification," [arXiv:2107.07511](https://arxiv.org/abs/2107.07511)
