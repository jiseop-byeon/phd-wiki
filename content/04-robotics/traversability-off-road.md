---
title: 17. Traversability & Off-Road Autonomy
tags: [robotics, navigation, unstructured]
study-depth: Working
wiki-support: Working
depth-goal: "Say what traversability actually is in current research, judge whether a paper claims adaptation or generalization, and read a field-autonomy result for what it established."
mastery-when: "Raise to Mastery only if terrain interaction or the traversability model itself becomes the contribution — the research program keeps navigation supporting."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to choose a traversability approach, and to see through the most
> common overclaim in the area.
> **Working** — traversability 접근법을 고르고, 이 분야에서 가장 흔한 과잉 주장을 꿰뚫어 볼 만큼.

> [!note] Before you start · 시작 전 점검
> You need occupancy and cost representations ([[04-robotics/planning-decision-making|4. Planning §2]]), MPC ([[04-robotics/mpc|MPC]]), and self-supervision — a training signal built from the data's own structure rather than labels ([[02-foundations/ml-practice|9. ML Practice]]).
> 점유·비용 표현([[04-robotics/planning-decision-making|4. 계획 §2]]), MPC([[04-robotics/mpc|MPC]]), 그리고 자기지도 — 라벨이 아니라 데이터 자신의 구조에서 만든 학습 신호([[02-foundations/ml-practice|9. ML 실무]]) — 가 필요하다.

## English

### 1. The idea that reorganised the field

A classical planner builds an occupancy grid, marks occupied cells as obstacles, and plans
around them. Put that robot in tall grass and it stops, because grass returns lidar hits and
lidar hits mean obstacle.

The correction is the premise of everything on this page:

> **Traversability is not a geometric predicate. It is a robot-specific, velocity-conditioned
> affordance learned from the robot's own experience of driving somewhere.**

BADGR is the canonical statement. It trains a predictive model on **self-supervised
off-policy real-world data** — no simulator, no human labels — with events like collision
and bumpiness auto-labelled from onboard sensors, using only RGB and GPS. The result is a
robot that drives *through* the grass and prefers smooth concrete, having learned both
preferences from consequences rather than from geometry.

Three consequences worth stating, because they are what a textbook does not prepare you for:

- **The same scene has different costmaps for different robots.** A 12-ton tracked vehicle
  and a quadruped disagree about a rubble pile, and neither is wrong.
- **Cost depends on commanded speed.** Terrain that is fine at 1 m/s is not fine at 10 m/s,
  so a costmap conditioned on velocity is a different object from a static one.
- **Terrain that a planner calls impassable is often passable.** The Verti-Wheelers line
  makes this its thesis: boulders, fallen trunks and rocky outcrops that classical planners
  label non-traversable are crossable by *ordinary wheeled robots with no hardware
  modification*, given a 6-DoF kinodynamic model. That reframes traversability as a
  **modelling** problem rather than a segmentation problem.

### 2. Where the supervision comes from

Every method here is defined by what it uses as a label, and that is the useful axis.

| Supervision source | What it means | Representative |
|---|---|---|
| **Onboard event detection** | collisions and bumpiness auto-labelled from sensors | BADGR |
| **Proprioceptive consequence** | IMU and shock feedback — literally how it felt to drive there | *How Does It Feel?* |
| **Velocity tracking** | did the robot achieve the speed it commanded? | Wild Visual Navigation |
| **Predicted proprioception** | predict the experience a vehicle *would* undergo, from geometry | ScaTE |
| **An existing stack** | distil a slow classical pipeline into a fast learned one | RoadRunner |

**Wild Visual Navigation** is the system the current field is organised around. It runs
online, vision-only, on DINO features, supervised by the robot's own velocity tracking, with
**training and inference concurrent onboard** an ANYmal — and its claim is carefully
limited: *less than five minutes of in-field training* from a short human demonstration,
then 1.4 km of footpath following and high grass.

**How Does It Feel?** pairs vision with proprioceptive IMU and shock feedback and conditions
the costmap on commanded velocity, reporting a **57% reduction in interventions** against an
occupancy baseline over courses of 400 m to 3,150 m.

**SALON** is the sharpest current statement of the same thesis: online adaptation producing
joint **cost and speed** maps while actively avoiding unfamiliar terrain, claiming
kilometre-scale routes after *seconds* of real data, matching methods that need
"100–1000× more data".

> [!important] The claim divergence — read every paper for this
> WVN, *How Does It Feel?* and SALON all claim **fast in-field adaptation and explicitly
> disclaim generalization**. **V-STRONG** claims the opposite: "unprecedented performance for
> generalization to new environments" on zero- and few-shot tasks. That disagreement is the
> most interesting open question in the thread, and the two claims require completely
> different evidence. When you read a traversability paper, the first thing to establish is
> which of the two it is claiming — the abstracts do not always make it obvious.

### 3. The geometric side did not go away

Two things a learning-first reading would miss.

**The elevation map underneath.** Nearly every legged-navigation paper assumes a
robot-centric 2.5D elevation map that propagates pose-estimate drift and sensor uncertainty
into a **per-cell variance** — Fankhauser, Bloesch and Hutter's formulation, shipped as the
`elevation_mapping` ROS package. Learned traversability usually runs *on top of* this, not
instead of it.

**Risk-aware geometric planning.** STEP is the counterweight: uncertainty-aware
traversability evaluation, **tail-risk assessment via Conditional Value-at-Risk (CVaR)**,
and a risk-constrained kinodynamic MPC solved by sequential quadratic programming. It is not
a learning paper and makes no generalization claim; it plugs straight into the material in
[[04-robotics/mpc|MPC]] and it is the traversability module of the NeBula stack that
competed in DARPA SubT.

CVaR is worth knowing as a modelling choice rather than a detail: optimising the *mean*
outcome and optimising the *worst decile* give different plans, and on terrain where the
failure is a rollover rather than a delay, the second is the right objective.

### 4. What the field programmes established

**DARPA SubT** (2018–2021) is the largest empirical event in unstructured-environment
autonomy. Team CERBERUS won the Systems track with a **heterogeneous legged-plus-aerial
system-of-systems** — four ANYmal C quadrupeds as the backbone — with resilient multi-modal
SLAM under communication- and GPS-denied conditions. That result, more than any single
paper, converted "legged robots in the field" from a demonstration into an engineering
result. The other complete published stack is **NeBula**, whose organising idea is
**belief-space, uncertainty-aware modular autonomy**: reasoning and deciding over
distributions rather than over point estimates.

**DARPA RACER** (2021 → completion announced January 2026) took the same question to speed.
Its stated goal was off-road traversal limited only by sensor performance, mechanical
constraints and safety, with parity to a human driver as the minimum bar; its stack ran
**without GPS and without pre-mapped routes**, on a drive-by-wire Polaris RZR and a ~12-ton
tracked platform. DARPA names the **perception architecture** as the headline outcome and
cites retraining for a new environment dropping from weeks to a day.

> [!warning] Three citation traps in this area
> - **DARPA publishes no speed or distance figures for RACER.** Do not attribute a top speed
>   to the programme; use paper-level numbers instead — RoadRunner reports up to 15 m/s on
>   the Polaris RZR, with 20 m/s in some tests.
> - **RACER expands to *Robotic Autonomy in Complex Environments with Resiliency*,** not
>   "Rapid Autonomy". And there is a **name collision**: a separate paper titled "RACER:
>   Epistemic Risk-Sensitive RL" is a 1/10-scale rally-car method with no connection to the
>   programme.
> - **CODa is an urban campus dataset**, not off-road, despite being cited that way.

### 5. Datasets, and what each one actually established

| Dataset | What it established |
|---|---|
| **RUGD** (IROS 2019) | made off-road **semantic segmentation** a measurable task — images only |
| **RELLIS-3D** (ICRA 2021) | forced **LiDAR** into the conversation; its diagnostic finding is that **models designed for urban segmentation fail on it** |
| **TartanDrive** (ICRA 2022) | ~200k off-road interactions across 7 modalities — reframed off-road learning around **dynamics** rather than segmentation |
| **GOOSE** (ICRA 2024) | 10,000 labelled image + point-cloud pairs, and — the real contribution — a **published ontology** that made cross-dataset off-road labelling comparable. Now a standing ICRA benchmark |
| **GOOSE-Ex** (ICRA 2025) | adds 5,000 frames from a **robotic excavator** and a quadruped, for cross-embodiment |

GOOSE-Ex is the one to notice from this wiki's angle: an off-road perception dataset that
includes construction machinery is the nearest existing bridge between this page and
[[05-construction-robotics/construction-manipulation|9. Construction Manipulation]].

### 6. Reading a traversability paper

| Question | What a vague answer hides |
|---|---|
| Adaptation or generalization? | They need different evidence and the field disagrees |
| What supplied the labels? | The supervision source *is* the method |
| Is the costmap conditioned on speed? | An unconditioned costmap is wrong at some speed |
| Which robot, and would the map transfer? | Traversability is robot-specific by construction |
| Is there a geometric layer underneath? | Most learned methods sit on an elevation map they do not mention |
| Distance and intervention count, not just success | Field autonomy's honest metric is interventions per kilometre |

### After reading

- [ ] State why tall grass is the canonical counterexample to occupancy mapping.
- [ ] Name three supervision sources and the paper for each.
- [ ] Explain the adaptation-versus-generalization divergence and why it matters.
- [ ] Say what CVaR buys over optimising the mean.
- [ ] Name what SubT and RACER each established, without attributing numbers DARPA did not publish.

### Self-check

1. A paper reports a traversability model trained on one robot and deployed on another with
   no retraining. What should you check first?
2. Why does a costmap need to know the commanded velocity?
3. A learned traversability system reports 95% success on a 2 km course. What is the more
   informative number to ask for?
4. Someone cites "RACER" for a reinforcement-learning method on a small car. What has
   happened?
5. Your project involves an excavator on rough ground. Which dataset on this page is the
   nearest starting point, and what is still missing from it?

> [!tip]- Answers
> 1. Whether the paper claims *adaptation* or *generalization*, and whether the second robot's dynamics are close enough for the first robot's learned consequences to be valid. Traversability is robot-specific by construction — a rubble pile a tracked vehicle crosses easily may roll a quadruped — so cross-robot transfer is a strong claim needing its own evidence, not a free consequence of the visual features being general.
> 2. Because traversability is a function of what the robot is trying to do, not only of what the terrain is. Ruts that are comfortable at 1 m/s can pitch a vehicle at 10 m/s, so a single static cost is wrong at one end of the speed range. Conditioning on commanded velocity is what lets one map serve a whole speed envelope — and it is why *How Does It Feel?* and SALON both do it.
> 3. **Interventions per kilometre**, plus the distance itself. Success rate on a fixed course conflates "drove it cleanly" with "drove it after three operator rescues", and the intervention count is the number that tracks deployability. *How Does It Feel?*'s headline is exactly this — a 57% reduction in interventions — rather than a success percentage.
> 4. A name collision. The DARPA programme is *Robotic Autonomy in Complex Environments with Resiliency*; a separate, unrelated paper uses RACER for an epistemic risk-sensitive RL method on a 1/10-scale rally car. Both are real; citing one for the other is a common error.
> 5. **GOOSE-Ex**, because it is the only off-road perception dataset here containing a robotic excavator, and it was built for cross-embodiment generalization. What is still missing is everything about the machine's own state — no actuator, joint, hydraulic-pressure or force channel is released, which is the same gap [[06-research-practice/simulators-benchmarks-datasets|7. §8]] documents across the whole construction dataset landscape.

### Sources

- G. Kahn, P. Abbeel, S. Levine, "BADGR: An Autonomous Self-Supervised Learning-Based Navigation System," *IEEE RA-L*, vol. 6, no. 2, pp. 1312–1319, 2021 ([arXiv:2002.05700](https://arxiv.org/abs/2002.05700)).
- J. Frey, M. Mattamala, N. Chebrolu, et al., "Fast Traversability Estimation for Wild Visual Navigation," RSS 2023 ([arXiv:2305.08510](https://arxiv.org/abs/2305.08510)). Journal version: M. Mattamala et al., *Autonomous Robots*, vol. 49, no. 3, art. 19, 2025 — **the same system, two papers**; cite RSS for priority and the journal for the full description.
- M. Guaman Castro, S. Triest, W. Wang, et al., "How Does It Feel? Self-Supervised Costmap Learning for Off-Road Vehicle Traversability," ICRA 2023 ([arXiv:2209.10788](https://arxiv.org/abs/2209.10788)).
- M. Sivaprakasam, S. Triest, C. Ho, et al., "SALON: Self-supervised Adaptive Learning for Off-road Navigation," ICRA 2025 ([arXiv:2412.07826](https://arxiv.org/abs/2412.07826)).
- S. Jung, J. Lee, X. Meng, B. Boots, A. Lambert, "V-STRONG: Visual Self-Supervised Traversability Learning for Off-road Navigation," ICRA 2024 ([arXiv:2312.16016](https://arxiv.org/abs/2312.16016)) — the zero-shot generalization claim.
- D. D. Fan, K. Otsu, Y. Kubo, et al., "STEP: Stochastic Traversability Evaluation and Planning for Risk-Aware Off-road Navigation," RSS 2021 ([arXiv:2103.02828](https://arxiv.org/abs/2103.02828)).
- P. Fankhauser, M. Bloesch, M. Hutter, "Probabilistic Terrain Mapping for Mobile Robots With Uncertain Localization," *IEEE RA-L*, vol. 3, no. 4, pp. 3019–3026, 2018 — the `elevation_mapping` package.
- J. Frey, M. Patel, D. Atha, et al., "RoadRunner," accepted *IEEE T-FR* ([arXiv:2402.19341](https://arxiv.org/abs/2402.19341)); M. Patel et al., "RoadRunner M&M," *IEEE RA-L*, vol. 9, no. 12, pp. 11425–11432, 2024.
- A. Datar, C. Pan, M. Nazeri, X. Xiao, "Toward Wheeled Mobility on Vertically Challenging Terrain," ICRA 2024, pp. 16322–16329 ([arXiv:2303.00998](https://arxiv.org/abs/2303.00998)) — the Verti-Wheelers line, from George Mason University.
- M. Tranzatto, T. Miki, M. Dharmadhikari, et al., "CERBERUS in the DARPA Subterranean Challenge," *Science Robotics*, vol. 7, no. 66, eabp9742, 2022. Fuller account: *Field Robotics*, vol. 4, no. 1, pp. 249–312, 2024. NeBula: A. Agha et al. ([arXiv:2103.11470](https://arxiv.org/abs/2103.11470)).
- Datasets: RUGD (IROS 2019); P. Jiang et al., "RELLIS-3D," ICRA 2021 ([arXiv:2011.12954](https://arxiv.org/abs/2011.12954)); S. Triest et al., "TartanDrive," ICRA 2022 ([arXiv:2205.01791](https://arxiv.org/abs/2205.01791)); P. Mortimer et al., "GOOSE," ICRA 2024 ([arXiv:2310.16788](https://arxiv.org/abs/2310.16788)); R. Hagmanns et al., "GOOSE-Ex," ICRA 2025 ([arXiv:2409.18788](https://arxiv.org/abs/2409.18788)).

**Within this wiki**

- [[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]] — the pose estimate whose drift the elevation map propagates
- [[04-robotics/mpc|MPC]] — what STEP's risk-constrained planner is a variant of
- [[04-robotics/legged-locomotion|18. Legged Locomotion]] — the robots most of this work runs on
- [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] — the construction end of terrain interaction

## 한국어

### 1. 이 분야를 재편한 발상

고전적 계획기는 점유 격자를 만들고, 점유된 셀을 장애물로 표시하고, 그것을 돌아간다. 그 로봇을
키 큰 풀밭에 놓으면 멈춘다. 풀이 라이다 반사를 만들고, 라이다 반사는 곧 장애물이기 때문이다.

그에 대한 교정이 이 페이지 전체의 전제다:

> **Traversability는 기하학적 술어가 아니다. 로봇마다 다르고 속도에 조건부이며, 로봇 자신이
> 거기를 주행한 경험에서 학습되는 어포던스다.**

BADGR가 그 정본 진술이다. **자기지도 off-policy 실세계 데이터**로 예측 모델을 학습한다 —
시뮬레이터도, 사람의 라벨도 없이 — 충돌이나 덜컹거림 같은 사건을 온보드 센서로 자동 라벨링하고,
RGB와 GPS만 쓴다. 결과는 풀을 *통과해* 주행하고 매끈한 콘크리트를 선호하는 로봇이며, 두 선호를
기하가 아니라 결과에서 배운 것이다.

교과서가 대비시켜 주지 않는 귀결 셋:

- **같은 장면이 로봇마다 다른 costmap을 갖는다.** 12톤 궤도 차량과 4족 로봇은 잔해 더미에 대해
  의견이 다르고, 둘 다 틀리지 않았다.
- **비용이 명령 속도에 의존한다.** 1 m/s에서 괜찮은 지형이 10 m/s에서는 괜찮지 않으므로, 속도를
  조건으로 하는 costmap은 정적인 것과 다른 대상이다.
- **계획기가 통과 불가라고 부르는 지형이 흔히 통과 가능하다.** Verti-Wheelers 계열이 이것을 자기
  주장으로 삼는다: 고전적 계획기가 비주행 가능으로 표시하는 바위, 쓰러진 줄기, 노두를 *하드웨어를
  전혀 개조하지 않은 평범한 바퀴 로봇이* 6자유도 기구·동역학 모델만 있으면 넘는다. Traversability를
  분할(segmentation) 문제가 아니라 **모델링** 문제로 재프레이밍한다.

### 2. 지도 신호는 어디서 오는가

여기의 모든 방법이 무엇을 라벨로 쓰는가로 정의되고, 그것이 쓸모 있는 축이다.

| 지도 신호의 출처 | 뜻 | 대표 |
|---|---|---|
| **온보드 사건 검출** | 충돌과 덜컹거림을 센서로 자동 라벨링 | BADGR |
| **고유수용감각적 결과** | IMU와 충격 피드백 — 문자 그대로 거기를 달린 느낌 | *How Does It Feel?* |
| **속도 추종** | 로봇이 명령한 속도를 달성했는가? | Wild Visual Navigation |
| **예측된 고유수용감각** | 차량이 겪게 *될* 경험을 기하로부터 예측 | ScaTE |
| **기존 스택** | 느린 고전 파이프라인을 빠른 학습 모델로 증류 | RoadRunner |

**Wild Visual Navigation**이 현재 분야가 조직되어 있는 시스템이다. 온라인으로, 비전만으로, DINO
특징 위에서, 로봇 자신의 속도 추종을 지도 신호 삼아, **학습과 추론을 ANYmal 온보드에서 동시에**
돌린다 — 그리고 주장을 신중하게 제한한다: 짧은 사람 시연으로부터 *5분 미만의 현장 학습*, 그다음
1.4 km의 오솔길 추종과 키 큰 풀.

**How Does It Feel?** 은 비전을 고유수용감각 IMU·충격 피드백과 짝짓고 costmap을 명령 속도에
조건화해, 400 m~3,150 m 코스에서 점유 기반 기준선 대비 **개입 57% 감소**를 보고한다.

**SALON**이 같은 주장의 가장 날카로운 현재 진술이다: 낯선 지형을 능동적으로 피하면서 **비용과
속도**를 함께 담은 지도를 만드는 온라인 적응. 실제 데이터 *수 초* 만에 킬로미터 규모 경로를
주장하며, "100~1000배 많은 데이터"를 필요로 하는 방법들과 대등하다고 말한다.

> [!important] 주장의 분기 — 모든 논문을 이것으로 읽어라
> WVN, *How Does It Feel?*, SALON은 전부 **빠른 현장 적응을 주장하고 일반화를 명시적으로
> 부인한다.** **V-STRONG**은 정반대를 주장한다: zero-shot·few-shot 과제에서 "새 환경으로의
> 일반화에서 전례 없는 성능". 이 불일치가 이 갈래에서 가장 흥미로운 열린 질문이고, 두 주장은
> 완전히 다른 증거를 요구한다. Traversability 논문을 읽을 때 가장 먼저 확정할 것은 둘 중 어느
> 쪽을 주장하는가이며, 초록이 늘 분명히 밝혀 주지는 않는다.

### 3. 기하학적 쪽이 사라진 것은 아니다

학습 위주로만 읽으면 놓치는 것 둘.

**밑에 깔린 고도 지도.** 거의 모든 레그드 내비게이션 논문이, 자세 추정 드리프트와 센서 불확실성을
**셀별 분산**으로 전파하는 로봇 중심 2.5D 고도 지도를 가정한다 — Fankhauser, Bloesch, Hutter의
정식화이며 `elevation_mapping` ROS 패키지로 배포된다. 학습된 traversability는 대개 이것을 *대신*
하는 것이 아니라 이것 *위에서* 돈다.

**위험 인지 기하 계획.** STEP이 그 균형추다: 불확실성 인지 traversability 평가, **Conditional
Value-at-Risk(CVaR)를 통한 꼬리 위험 평가**, 그리고 순차 이차 계획법으로 푸는 위험 제약
기구·동역학 MPC. 학습 논문이 아니고 일반화를 주장하지 않는다. [[04-robotics/mpc|MPC]]의 내용에
곧바로 연결되며, DARPA SubT에 나간 NeBula 스택의 traversability 모듈이다.

CVaR은 세부가 아니라 모델링 선택으로 알아 둘 가치가 있다: *평균* 결과를 최적화하는 것과 *최악
10분위*를 최적화하는 것은 다른 계획을 낳고, 실패가 지연이 아니라 전복인 지형에서는 후자가 옳은
목적함수다.

### 4. 필드 프로그램이 확립한 것

**DARPA SubT**(2018~2021)가 비정형 환경 자율성에서 가장 큰 경험적 사건이다. Team CERBERUS가
**이종 레그드+공중 시스템의 시스템** — ANYmal C 4족 넷을 중추로 — 으로, 통신과 GNSS가 거부된
조건에서 견고한 다중 모달 SLAM과 함께 시스템 부문을 우승했다. 그 결과가 어떤 단일 논문보다도
"필드의 레그드 로봇"을 실연에서 공학적 결과로 바꿔 놓았다. 발표된 다른 완결 스택은 **NeBula**이고,
그 조직 원리는 **믿음 공간(belief-space)의 불확실성 인지 모듈형 자율성**이다: 점 추정이 아니라
분포 위에서 추론하고 결정한다.

**DARPA RACER**(2021 → 2026년 1월 완료 발표)는 같은 질문을 속도로 가져갔다. 명시된 목표는 센서
성능·기계적 제약·안전만이 제한하는 오프로드 주행이었고 최소 기준선이 사람 운전자와의 대등함이었다.
스택은 **GNSS 없이, 사전 지도 없이** 돌았고, 드라이브 바이 와이어 Polaris RZR과 약 12톤 궤도
플랫폼 위에서였다. DARPA는 **인식 아키텍처**를 대표 성과로 지목하며, 새 환경에 대한 재학습이 몇
주에서 하루로 줄었다고 밝힌다.

> [!warning] 이 분야의 인용 함정 셋
> - **DARPA는 RACER의 속도나 거리 수치를 발표하지 않는다.** 프로그램에 최고 속도를 귀속시키지
>   말고 논문 수준 수치를 쓰라 — RoadRunner가 Polaris RZR에서 15 m/s까지, 일부 시험에서 20 m/s를
>   보고한다.
> - **RACER는 *Robotic Autonomy in Complex Environments with Resiliency*의 약자**이지 "Rapid
>   Autonomy"가 아니다. 그리고 **이름 충돌**이 있다: "RACER: Epistemic Risk-Sensitive RL"이라는
>   별개 논문은 1/10 스케일 랠리카 방법으로 이 프로그램과 무관하다.
> - **CODa는 도심 캠퍼스 데이터셋**이지 오프로드가 아니다. 그렇게 인용되는 일이 있지만 아니다.

### 5. 데이터셋과, 각각이 실제로 확립한 것

| 데이터셋 | 확립한 것 |
|---|---|
| **RUGD** (IROS 2019) | 오프로드 **의미 분할**을 측정 가능한 과제로 만들었다 — 이미지만 |
| **RELLIS-3D** (ICRA 2021) | **LiDAR**를 대화에 끌어들였다. 진단적 발견은 **도심 분할용으로 설계된 모델이 여기서 실패한다**는 것 |
| **TartanDrive** (ICRA 2022) | 7개 모달리티에 걸친 약 20만 오프로드 상호작용 — 오프로드 학습을 분할이 아니라 **동역학** 중심으로 재편 |
| **GOOSE** (ICRA 2024) | 라벨된 이미지+포인트 클라우드 쌍 1만 개, 그리고 진짜 기여인 **공개된 온톨로지** — 데이터셋을 가로지르는 오프로드 라벨링을 비교 가능하게 만들었다. 지금은 상설 ICRA 벤치마크 |
| **GOOSE-Ex** (ICRA 2025) | **로봇 굴착기**와 4족에서 5,000 프레임을 추가, 교차 embodiment용 |

이 위키의 각도에서 눈여겨볼 것은 GOOSE-Ex다: 건설 기계를 포함한 오프로드 인식 데이터셋이,
이 페이지와 [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] 사이의
가장 가까운 기존 다리다.

### 6. Traversability 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 적응인가 일반화인가? | 요구되는 증거가 다르고 분야의 의견이 갈린다 |
| 라벨을 무엇이 공급했는가? | 지도 신호의 출처가 곧 방법이다 |
| Costmap이 속도에 조건화되어 있는가? | 조건화되지 않은 costmap은 어떤 속도에서 틀리다 |
| 어느 로봇이며, 그 지도가 이전되겠는가? | Traversability는 구조적으로 로봇마다 다르다 |
| 밑에 기하 층이 있는가? | 대부분의 학습 방법은 언급하지 않는 고도 지도 위에 앉아 있다 |
| 성공률이 아니라 거리와 개입 횟수 | 필드 자율성의 정직한 지표는 킬로미터당 개입 수다 |

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 키 큰 풀이 왜 점유 지도의 정본 반례인지 말한다.
- [ ] 지도 신호의 출처 셋과 각각의 논문을 댄다.
- [ ] 적응 대 일반화의 분기를 설명하고 왜 중요한지 말한다.
- [ ] CVaR이 평균 최적화에 비해 무엇을 사는지 말한다.
- [ ] SubT와 RACER가 각각 확립한 것을, DARPA가 발표하지 않은 수치를 붙이지 않고 말한다.

### 스스로 점검

1. 어떤 논문이 한 로봇에서 학습한 traversability 모델을 재학습 없이 다른 로봇에 배치했다고
   보고한다. 무엇을 먼저 확인해야 하는가?
2. Costmap이 왜 명령 속도를 알아야 하는가?
3. 학습 기반 traversability 시스템이 2 km 코스에서 95% 성공을 보고한다. 더 정보가 되는 숫자는?
4. 누군가 소형 자동차의 강화학습 방법에 "RACER"를 인용한다. 무슨 일이 일어난 것인가?
5. 프로젝트가 거친 지반 위의 굴착기를 다룬다. 이 페이지에서 가장 가까운 출발점은 무엇이고,
   거기에 여전히 없는 것은?

> [!tip]- 정답 · Answers
> 1. 그 논문이 *적응*을 주장하는지 *일반화*를 주장하는지, 그리고 두 번째 로봇의 동역학이 첫 로봇이 학습한 결과가 유효할 만큼 가까운지. Traversability는 구조적으로 로봇마다 다르다 — 궤도 차량이 쉽게 넘는 잔해 더미가 4족을 굴릴 수 있다 — 그러니 로봇 간 이전은 시각 특징이 일반적이라는 데서 공짜로 따라 나오는 것이 아니라 자기 증거가 필요한 강한 주장이다.
> 2. Traversability가 지형이 무엇인가만이 아니라 로봇이 무엇을 하려 하는가의 함수이기 때문이다. 1 m/s에서 편안한 골이 10 m/s에서는 차량을 튀어 오르게 할 수 있으므로, 단일 정적 비용은 속도 범위의 한쪽 끝에서 틀린다. 명령 속도에 조건화하는 것이 지도 하나로 속도 포락선 전체를 감당하게 만들고, *How Does It Feel?* 과 SALON이 둘 다 그렇게 하는 이유다.
> 3. **킬로미터당 개입 횟수**, 그리고 거리 그 자체. 고정 코스의 성공률은 "깨끗하게 주행했다"와 "조작자가 세 번 구해 준 뒤 주행했다"를 뭉뚱그리고, 배치 가능성을 추적하는 숫자는 개입 횟수다. *How Does It Feel?* 의 대표 수치가 성공률이 아니라 정확히 이것 — 개입 57% 감소 — 이다.
> 4. 이름 충돌이다. DARPA 프로그램은 *Robotic Autonomy in Complex Environments with Resiliency*이고, 별개의 무관한 논문이 1/10 스케일 랠리카의 epistemic risk-sensitive RL 방법에 RACER를 쓴다. 둘 다 실재하며, 하나를 다른 하나로 인용하는 것이 흔한 오류다.
> 5. **GOOSE-Ex.** 여기서 로봇 굴착기를 담은 유일한 오프로드 인식 데이터셋이고 교차 embodiment 일반화를 위해 만들어졌기 때문이다. 여전히 없는 것은 기계 자신의 상태 전부다 — 액추에이터·관절·유압·힘 채널이 하나도 공개되지 않으며, 이는 [[06-research-practice/simulators-benchmarks-datasets|7. §8]]이 건설 데이터셋 전반에 대해 기록한 바로 그 공백이다.

### 출처

- G. Kahn, P. Abbeel, S. Levine, "BADGR: An Autonomous Self-Supervised Learning-Based Navigation System," *IEEE RA-L*, vol. 6, no. 2, pp. 1312–1319, 2021 ([arXiv:2002.05700](https://arxiv.org/abs/2002.05700)).
- J. Frey, M. Mattamala, N. Chebrolu, et al., "Fast Traversability Estimation for Wild Visual Navigation," RSS 2023 ([arXiv:2305.08510](https://arxiv.org/abs/2305.08510)). 저널판: M. Mattamala et al., *Autonomous Robots*, vol. 49, no. 3, art. 19, 2025 — **같은 시스템, 두 논문**. 우선권은 RSS를, 전체 서술은 저널판을 인용하라.
- M. Guaman Castro, S. Triest, W. Wang, et al., "How Does It Feel? Self-Supervised Costmap Learning for Off-Road Vehicle Traversability," ICRA 2023 ([arXiv:2209.10788](https://arxiv.org/abs/2209.10788)).
- M. Sivaprakasam, S. Triest, C. Ho, et al., "SALON: Self-supervised Adaptive Learning for Off-road Navigation," ICRA 2025 ([arXiv:2412.07826](https://arxiv.org/abs/2412.07826)).
- S. Jung, J. Lee, X. Meng, B. Boots, A. Lambert, "V-STRONG," ICRA 2024 ([arXiv:2312.16016](https://arxiv.org/abs/2312.16016)) — zero-shot 일반화 주장.
- D. D. Fan, K. Otsu, Y. Kubo, et al., "STEP," RSS 2021 ([arXiv:2103.02828](https://arxiv.org/abs/2103.02828)).
- P. Fankhauser, M. Bloesch, M. Hutter, "Probabilistic Terrain Mapping for Mobile Robots With Uncertain Localization," *IEEE RA-L*, vol. 3, no. 4, pp. 3019–3026, 2018 — `elevation_mapping` 패키지.
- J. Frey, M. Patel, D. Atha, et al., "RoadRunner," *IEEE T-FR* 게재 확정 ([arXiv:2402.19341](https://arxiv.org/abs/2402.19341)); M. Patel et al., "RoadRunner M&M," *IEEE RA-L*, vol. 9, no. 12, pp. 11425–11432, 2024.
- A. Datar, C. Pan, M. Nazeri, X. Xiao, "Toward Wheeled Mobility on Vertically Challenging Terrain," ICRA 2024, pp. 16322–16329 ([arXiv:2303.00998](https://arxiv.org/abs/2303.00998)) — Verti-Wheelers 계열, 조지메이슨대.
- M. Tranzatto, T. Miki, M. Dharmadhikari, et al., "CERBERUS in the DARPA Subterranean Challenge," *Science Robotics*, vol. 7, no. 66, eabp9742, 2022. 더 자세한 서술: *Field Robotics*, vol. 4, no. 1, pp. 249–312, 2024. NeBula: A. Agha et al. ([arXiv:2103.11470](https://arxiv.org/abs/2103.11470)).
- 데이터셋: RUGD (IROS 2019); P. Jiang et al., "RELLIS-3D," ICRA 2021 ([arXiv:2011.12954](https://arxiv.org/abs/2011.12954)); S. Triest et al., "TartanDrive," ICRA 2022 ([arXiv:2205.01791](https://arxiv.org/abs/2205.01791)); P. Mortimer et al., "GOOSE," ICRA 2024 ([arXiv:2310.16788](https://arxiv.org/abs/2310.16788)); R. Hagmanns et al., "GOOSE-Ex," ICRA 2025 ([arXiv:2409.18788](https://arxiv.org/abs/2409.18788)).

**이 위키 안에서**

- [[04-robotics/state-estimation-slam|3. 상태 추정·위치추정·SLAM]] — 고도 지도가 드리프트를 전파하는 그 자세 추정
- [[04-robotics/mpc|MPC]] — STEP의 위험 제약 계획기가 그 변형인 것
- [[04-robotics/legged-locomotion|18. 레그드 로코모션]] — 이 연구 대부분이 돌아가는 로봇들
- [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 자율화]] — 지형 상호작용의 건설 쪽 끝
