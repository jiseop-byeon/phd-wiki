---
title: 23. Human Intent & Trajectory Prediction
tags: [robotics, hri, prediction, human, construction]
study-depth: Working
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
> [[02-foundations/probability|Probability]] · [[04-robotics/video-action-understanding|20. Video Representation & Action Understanding]] · [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]] · [[04-robotics/hri-safety|11. Human–Robot Interaction & Safety]]

> [!note] First pass · 처음이라면
> Read §1 — intent classification and trajectory forecasting are different problems and papers do not always say which they solved — then §3, then §4. Calibration is where the research actually is, which is why §4 comes before the survey material.

### 1. Two different problems

| | Intent prediction | Trajectory forecasting |
|---|---|---|
| Output | discrete latent decision — cross / not cross, hand over / withdraw | continuous future positions $\hat{x}_{t+1:t+H}$ |
| Ground truth | an event that did or did not occur | a recorded path |
| Metric | accuracy, AUC, F1 — **conditioned on time-to-event** | ADE / FDE, minADE over $k$ samples |
| Failure mode | confident wrong class | plausible but wrong mode |
| What it feeds | a discrete decision (stop, warn, yield) | a continuous plan (cost map, MPC constraint) |

They are often solved by the same network and reported in the same paper, but they are not the same claim. **"We predict pedestrian intent" and "we forecast pedestrian trajectories" answer different questions and fail differently.** A trajectory model with low ADE can still be useless if it never places mass on the crossing mode; an intent classifier can be right about crossing and useless for planning because it says nothing about *where*.

### 2. The observable cue cascade

Intent is latent. What is measurable, roughly in order of lead time:

| Cue | Lead | Observable at range? | Source |
|---|---|---|---|
| Gaze | longest | **no** beyond a few metres | [[04-robotics/human-pose-gaze\|21. §4]] |
| Head / body orientation | long | yes | [[04-robotics/human-pose-gaze\|21. §4–§5]] |
| Gait change, deceleration | medium | yes, from a tracked box | [[04-robotics/human-pose-gaze\|21. §5]] |
| Proximity to boundary (curb, machine envelope) | medium | yes, needs scene geometry | — |
| Trajectory curvature toward target | short | yes | §1 above |
| Contact / entry | zero | yes | too late |

This is the same cascade as [[04-robotics/egocentric-perception|22. §4]], seen from outside instead of from the head. **The design decision in any intent system is which rung you commit to,** because that fixes both the lead time and the ceiling on reliability.

> [!warning] The "subtle cue" trap
> The cues that carry the most intent information are the ones that stop being resolvable first. A study that establishes gaze as predictive using close-range or instrumented data has not shown that a vehicle or robot camera can use it. Always state the distance at which the cue was measured and the distance at which the system must work.

### 3. Early versus accurate is the actual research object

Let $T$ be the event time. Performance must be reported as a function of time-to-event $\Delta = T - t$:

$$\text{AUC}(\Delta), \qquad \text{Acc}(\Delta)$$

Reporting a single number at one $\Delta$, or worse averaged over all $\Delta$, hides the only property that matters for deployment: **the largest $\Delta$ at which the predictor still clears the decision threshold.** Call it the usable horizon $\Delta^\*$:

$$\Delta^{*} = \max\{\Delta : \text{performance}(\Delta) \geq \text{threshold}\}$$

A system whose $\Delta^*$ is shorter than the actuator's stopping time is a detector wearing a predictor's name.

> [!example] Worked example
> A vehicle at 30 km/h ($8.3\,\mathrm{m/s}$) needs 1.2 s to brake plus 0.3 s of pipeline latency: 1.5 s of required lead. Model A reaches AUC 0.85 only at $\Delta = 0.8\,\mathrm{s}$; model B holds AUC 0.78 out to $\Delta = 2.0\,\mathrm{s}$. **Model A cannot be used at all** at this speed, despite the better headline number. The correct comparison is $\Delta^*$ against the required lead, not peak performance.

<svg viewBox="0 0 560 285" style="max-width:100%;height:auto" role="img" aria-label="performance against time before the event, with a decision threshold and the lead time the platform requires">
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
    <text x="64" y="137" font-size="9.5" opacity="0.85">decision threshold</text>
    <text x="330" y="42" font-size="9.5" opacity="0.85">required lead, 1.5 s</text>
    <text x="258" y="147" text-anchor="end" font-size="10">&#916;*&#7488;</text>
    <text x="446" y="115" font-size="10">&#916;*&#7495;</text>
    <text x="54" y="44" text-anchor="end" font-size="9.5">1.0</text><text x="54" y="127" text-anchor="end" font-size="9.5">0.75</text><text x="54" y="177" text-anchor="end" font-size="9.5">0.6</text>
    <text x="60" y="206" text-anchor="middle" font-size="9.5">0</text><text x="148" y="206" text-anchor="middle" font-size="9.5">0.5</text><text x="236" y="206" text-anchor="middle" font-size="9.5">1.0</text><text x="324" y="206" text-anchor="middle" font-size="9.5">1.5</text><text x="412" y="206" text-anchor="middle" font-size="9.5">2.0</text><text x="500" y="206" text-anchor="middle" font-size="9.5">2.5</text>
    <text x="282" y="222" text-anchor="middle" font-size="9.5">time before the event &#916; (s)</text>
    <text x="14" y="112" font-size="9.5">AUC</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="243">Model A has the better headline number and cannot be used here: its usable</text>
    <text x="20" y="259">horizon &#916;* = 1.15 s falls short of the 1.5 s this platform needs, while model B</text>
    <text x="20" y="275">holds the threshold out to 2.15 s. Compare &#916;*, not peak performance.</text>
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

Conformal prediction deserves emphasis because the mathematics is elementary — exchangeability plus a quantile — and the output is exactly what a safety decision needs: not "probably crossing" but "crossing is in the 90%-coverage prediction set." This is also the machinery behind ask-for-help policies in [[04-robotics/hri-safety|11. HRI & Safety]]: a robot that knows its prediction set is ambiguous is a robot that knows when to defer to a human.

**A calibrated 0.7 supports a decision rule. An uncalibrated 0.9 does not.**

### 5. Class imbalance and the base rate

Most pedestrians near a road do not cross in the next two seconds; most workers near a machine do not enter its envelope. Positive rates of a few percent are normal, with two consequences:

- **Accuracy is meaningless.** A constant "no" predictor scores 95%+. Report AUC, precision–recall (not ROC alone, which is optimistic under imbalance), and the operating point actually used.
- **Precision at the deployed threshold is the whole story.** A warning system with 20% precision produces four false alarms per true one, and will be ignored or disabled by the workers it is meant to protect. Alarm fatigue is a system failure mode, not a human failing.

### 6. Trajectory forecasting, briefly

When the output is a path rather than a decision:

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

That last row is the substantive difference and a genuine research opening. **A worker who interacts with the same robot daily changes their behaviour in response to it,** so the predictor's training distribution shifts because the predictor is deployed. Road-crossing datasets contain no such feedback loop. Anyone claiming a road-trained intent model transfers to a worksite has to address it.

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
- compute a usable horizon $\Delta^*$ and compare it against a required lead time;
- explain calibration, name two ways to fix it, and say why conformal prediction fits safety decisions;
- explain why accuracy is the wrong metric under a low base rate;
- name the human-masked ablation and what it tests;
- state the feedback-loop difference between road pedestrians and repeat coworkers.

### Self-check

1. A model reports 96% accuracy on crossing prediction. Why is this uninformative, and what should be reported instead?
2. A robot needs 0.9 s to stop. Model A: AUC 0.9 at $\Delta=0.5$ s, 0.6 at $\Delta=1.0$ s. Model B: AUC 0.8 flat to $\Delta=1.5$ s. Which is deployable?
3. Why can a model win on minADE$_{20}$ and still be unusable by a planner?
4. What single ablation tests whether an intent model is actually reading the human?
5. Why is a worksite intent model's training distribution non-stationary in a way a road dataset's is not?

> [!tip]- Answers
> 1. Base rate — a constant "no" scores similarly. Report AUC and precision–recall at the deployed operating point, as a function of time-to-event. 2. B. A's performance collapses before the 0.9 s the actuator needs; B clears threshold out to 1.5 s. 3. minADE rewards one lucky sample among twenty; the planner needs a probability distribution over futures, which the metric does not require the model to provide. 4. Mask or remove the pedestrian and re-evaluate; near-equal performance means the model learned scene priors. 5. The worker adapts to the deployed robot, so deployment changes the data-generating process — a feedback loop absent from passive road recordings.

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
> [[02-foundations/probability|확률]] · [[04-robotics/video-action-understanding|20. 비디오 표현과 행동 이해]] · [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]] · [[04-robotics/hri-safety|11. Human–Robot Interaction & Safety]]

> [!note] 처음이라면 · First pass
> 먼저 §1 — 의도 분류와 궤적 예측은 다른 문제이고 논문이 어느 쪽을 풀었는지 늘 밝히지는 않는다 — 그다음 §3, 그다음 §4. 연구가 실제로 있는 곳이 보정이라서 §4를 조망 자료보다 앞에 둔다.

### 1. 서로 다른 두 문제

| | 의도 예측 | 궤적 예측 |
|---|---|---|
| 출력 | 이산 잠재 결정 — 건넌다/안 건넌다, 건넨다/거둔다 | 연속 미래 위치 $\hat{x}_{t+1:t+H}$ |
| 정답 | 일어났거나 안 일어난 사건 | 기록된 경로 |
| 지표 | 정확도·AUC·F1 — **time-to-event로 조건화된** | ADE / FDE, $k$개 샘플의 minADE |
| 실패 방식 | 확신에 찬 오분류 | 그럴듯하지만 틀린 모드 |
| 무엇을 먹이나 | 이산 결정(정지·경고·양보) | 연속 계획(코스트맵, MPC 제약) |

같은 네트워크로 풀고 같은 논문에서 보고되는 일이 잦지만 **같은 주장이 아니다.** "보행자 의도를 예측한다"와 "보행자 궤적을 예측한다"는 다른 질문에 답하고 다르게 실패한다. ADE가 낮은 궤적 모델도 횡단 모드에 확률을 전혀 주지 않으면 쓸모없고, 의도 분류기는 횡단 여부를 맞혀도 *어디로*를 말하지 않아 계획에 못 쓴다.

### 2. 관측 가능한 단서 사슬

의도는 잠재변수다. 측정 가능한 것을 선행 시간 순으로:

| 단서 | 선행 | 원거리 관측? | 출처 |
|---|---|---|---|
| 시선 | 가장 김 | 수 미터 넘으면 **불가** | [[04-robotics/human-pose-gaze\|21. §4]] |
| 머리·몸 방향 | 김 | 가능 | [[04-robotics/human-pose-gaze\|21. §4–§5]] |
| 보행 변화, 감속 | 중간 | 가능, 추적 박스로 | [[04-robotics/human-pose-gaze\|21. §5]] |
| 경계(연석·기계 반경)와의 근접 | 중간 | 가능, 장면 기하 필요 | — |
| 목표를 향한 궤적 곡률 | 짧음 | 가능 | 위 §1 |
| 접촉·진입 | 0 | 가능 | 이미 늦음 |

이는 [[04-robotics/egocentric-perception|22. §4]]와 같은 사슬을 머리가 아니라 바깥에서 본 것이다. **어떤 의도 시스템에서도 설계 결정은 어느 단에 걸 것인가이며**, 그 선택이 선행 시간과 신뢰도 상한을 동시에 고정한다.

> [!warning] "subtle cue" 함정
> 의도 정보를 가장 많이 담은 단서가 가장 먼저 분해 불가능해진다. 근거리나 계측 장비로 시선의 예측력을 입증한 연구가, 차량·로봇 카메라가 그것을 쓸 수 있음을 보인 것은 아니다. **단서를 측정한 거리와 시스템이 작동해야 하는 거리를 항상 밝혀라.**

### 3. 조기성 vs 정확도가 진짜 연구 대상이다

사건 시각을 $T$라 하면, 성능은 time-to-event $\Delta = T - t$의 함수로 보고돼야 한다:

$$\text{AUC}(\Delta), \qquad \text{Acc}(\Delta)$$

한 $\Delta$에서의 숫자 하나, 더 나쁘게는 모든 $\Delta$에 대한 평균은 배포에 유일하게 중요한 성질을 가린다: **예측기가 결정 임계값을 여전히 넘기는 가장 큰 $\Delta$.** 이를 가용 지평 $\Delta^*$라 하자:

$$\Delta^{*} = \max\{\Delta : \text{성능}(\Delta) \geq \text{임계값}\}$$

$\Delta^*$가 구동기의 정지 시간보다 짧은 시스템은 **예측기라는 이름을 쓴 검출기다.**

> [!example] 계산 예제
> 30 km/h($8.3\,\mathrm{m/s}$) 차량이 제동에 1.2초, 파이프라인 지연 0.3초 → 필요한 선행 1.5초. 모델 A는 AUC 0.85를 $\Delta = 0.8\,\mathrm{s}$에서만 달성하고, 모델 B는 AUC 0.78을 $\Delta = 2.0\,\mathrm{s}$까지 유지한다. **이 속도에서 A는 아예 쓸 수 없다** — 헤드라인 숫자가 더 좋은데도. 올바른 비교는 최고 성능이 아니라 **$\Delta^*$ 대 필요 선행 시간**이다.

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
    <text x="64" y="137" font-size="9.5" opacity="0.85">결정 임계값</text>
    <text x="330" y="42" font-size="9.5" opacity="0.85">필요 선행 1.5초</text>
    <text x="258" y="147" text-anchor="end" font-size="10">&#916;*&#7488;</text>
    <text x="446" y="115" font-size="10">&#916;*&#7495;</text>
    <text x="54" y="44" text-anchor="end" font-size="9.5">1.0</text><text x="54" y="127" text-anchor="end" font-size="9.5">0.75</text><text x="54" y="177" text-anchor="end" font-size="9.5">0.6</text>
    <text x="60" y="206" text-anchor="middle" font-size="9.5">0</text><text x="148" y="206" text-anchor="middle" font-size="9.5">0.5</text><text x="236" y="206" text-anchor="middle" font-size="9.5">1.0</text><text x="324" y="206" text-anchor="middle" font-size="9.5">1.5</text><text x="412" y="206" text-anchor="middle" font-size="9.5">2.0</text><text x="500" y="206" text-anchor="middle" font-size="9.5">2.5</text>
    <text x="282" y="222" text-anchor="middle" font-size="9.5">사건까지 남은 시간 &#916; (초)</text>
    <text x="14" y="112" font-size="9.5">AUC</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="243">모델 A가 헤드라인 숫자는 더 좋지만 여기서는 쓸 수 없다: 가용 지평</text>
    <text x="20" y="259">&#916;* = 1.15초가 이 플랫폼에 필요한 1.5초에 못 미치고, 모델 B는 2.15초까지</text>
    <text x="20" y="275">임계값을 유지한다. 최고 성능이 아니라 &#916;*를 필요 선행과 비교하라.</text>
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

Conformal prediction을 강조하는 이유는 수학이 초등적이고(교환가능성 + 분위수) 출력이 정확히 안전 결정이 필요로 하는 형태이기 때문이다 — "아마 건널 것"이 아니라 "90% 커버리지 예측 집합 안에 횡단이 있다". 이건 [[04-robotics/hri-safety|11. HRI & Safety]]의 ask-for-help 정책을 떠받치는 기계장치이기도 하다: **자기 예측 집합이 모호하다는 걸 아는 로봇이 사람에게 넘길 때를 아는 로봇이다.**

**보정된 0.7은 결정 규칙을 지지한다. 보정 안 된 0.9는 그러지 못한다.**

### 5. 클래스 불균형과 기저율

도로 근처 보행자 대부분은 다음 2초 안에 건너지 않고, 기계 근처 작업자 대부분은 작업반경에 들어가지 않는다. 양성률 수 %가 정상이고, 귀결이 둘이다:

- **정확도는 무의미하다.** 무조건 "아니오"가 95% 이상을 받는다. AUC와 **precision–recall**(불균형에서 낙관적인 ROC 단독이 아니라), 그리고 실제 사용한 동작점을 보고하라.
- **배포 임계값에서의 precision이 전부다.** precision 20%인 경고 시스템은 참 하나당 오경보 넷을 낸다. 보호하려던 작업자가 무시하거나 꺼버린다. **알람 피로는 인간의 결함이 아니라 시스템 실패 양식이다.**

### 6. 궤적 예측, 간단히

출력이 결정이 아니라 경로일 때:

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

마지막 행이 실질적 차이이자 진짜 연구 개구부다. **매일 같은 로봇과 일하는 작업자는 그 로봇에 반응해 행동을 바꾼다.** 그래서 예측기가 배포됐다는 사실 때문에 학습 분포가 이동한다. 도로 횡단 데이터셋에는 이런 피드백 루프가 없다. 도로에서 학습한 의도 모델이 현장에 전이된다고 주장하려면 이걸 다뤄야 한다.

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

### 읽은 뒤

다음을 할 수 있어야 한다:

- 의도 분류와 궤적 예측의 차이와 각각의 지표를 말한다;
- 가용 지평 $\Delta^*$를 계산하고 필요 선행 시간과 비교한다;
- 보정을 설명하고, 고치는 방법 둘을 들고, conformal prediction이 안전 결정에 맞는 이유를 말한다;
- 낮은 기저율에서 정확도가 왜 틀린 지표인지 설명한다;
- 사람 마스킹 ablation과 그것이 검증하는 바를 말한다;
- 도로 보행자와 반복 협업 작업자 사이의 피드백 루프 차이를 말한다.

### 자가 점검

1. 어떤 모델이 횡단 예측에서 96% 정확도를 보고했다. 왜 정보가 없고, 대신 무엇을 보고해야 하나?
2. 로봇이 정지에 0.9초 필요하다. A: $\Delta=0.5$s에서 AUC 0.9, $\Delta=1.0$s에서 0.6. B: $\Delta=1.5$s까지 AUC 0.8 평탄. 어느 쪽이 배포 가능한가?
3. minADE$_{20}$에서 이기고도 플래너가 못 쓰는 이유는?
4. 의도 모델이 실제로 사람을 읽는지 검증하는 단일 ablation은?
5. 현장 의도 모델의 학습 분포가 도로 데이터셋과 달리 비정상(non-stationary)인 이유는?

> [!tip]- 정답
> 1. 기저율 때문 — 무조건 "아니오"가 비슷한 점수를 받는다. 배포 동작점에서의 AUC와 precision–recall을 time-to-event의 함수로 보고해야 한다. 2. B. A는 구동기가 필요로 하는 0.9초 전에 성능이 무너지고, B는 1.5초까지 임계값을 넘긴다. 3. minADE는 스무 개 중 운 좋은 하나를 보상한다; 플래너는 미래에 대한 확률분포가 필요한데 지표가 그것을 요구하지 않는다. 4. 보행자를 마스킹·제거하고 재평가한다; 성능이 비슷하면 장면 사전확률을 학습한 것이다. 5. 작업자가 배포된 로봇에 적응하므로 배포 자체가 데이터 생성 과정을 바꾼다 — 수동적 도로 녹화에는 없는 피드백 루프다.

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
