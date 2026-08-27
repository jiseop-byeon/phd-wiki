---
title: Sim-to-Real for Field Robots
tags: [construction, sim-to-real, robotics, learning]
study-depth: Working
depth-goal: "Use the task taxonomy, system assumptions, and evaluation criteria to formulate construction-robotics research."
mastery-when: "Raise to Mastery when this task stream or deployment layer is the thesis contribution."
---

## English

Simulation makes dangerous, slow, and expensive robot experience cheap. It does not make
that experience real. **Sim-to-real** is the set of modeling, training, adaptation, and
evaluation practices used to keep a policy useful when its simulator assumptions fail.

> [!info] Depth target
> Read a sim-to-real paper and identify: which gap (dynamics, contact, sensing, task,
> implementation) dominates, which strategy addresses it and at what cost, what real-data
> and intervention budget the transfer consumed, and which rung of the deployment ladder
> the evidence actually reaches. Designing transfer pipelines is a working/mastery topic.

> [!note] Prerequisites
> [[02-foundations/probability|Probability]] · [[02-foundations/rl-basics|RL Basics]] ·
> [[04-robotics/robot-systems-deployment|Robot Systems]] ·
> [[04-robotics/contact-force-tactile|Contact]]

### 1. Where the reality gap comes from

| Gap | Examples in field robots | Typical response |
|---|---|---|
| Dynamics | mass, friction, hydraulic delay, backlash | system identification, parameter randomization, residual models |
| Contact/material | soil, rubble, tire slip, cutting resistance | randomized terrain, learned contact models, online adaptation |
| Sensing | dust, glare, vibration, latency, missing returns | sensor noise/latency models, augmentation, robust estimation |
| Task distribution | unseen sites, geometry, weather, operators | diverse procedural scenes, curriculum, real-data fine-tuning |
| Software/hardware | control rate, saturation, dropped messages | hardware-in-the-loop, action delay and limit randomization |

The important question is not “Was simulation photorealistic?” but **which variables
that affect the policy were represented, varied, or adapted**.

> [!warning] The contact row is not like the others
> The other four gaps are *parameter* problems: the physics is right and the numbers are
> wrong, so identification or randomization closes them. Contact is a **model** problem.
> Rigid-body engines resolve contact as point constraints solved per timestep, and the
> underlying dynamics are genuinely non-smooth — impacts and stick–slip transitions are
> discontinuities, and numerical integrators lose both accuracy and stability exactly there.
> Randomizing the friction coefficient does not fix a contact model that cannot represent
> the contact patch in the first place.
>
> This is why a contact-rich result and a locomotion result are not comparable evidence of
> sim-to-real maturity, even when both come from the same simulator. Legged locomotion
> tolerates a crude contact model because the policy is rejecting disturbance at 50 Hz over
> a foot that only needs to not slip; insertion, drilling and panel seating are *defined* by
> the contact patch the model is failing to represent. Treat "we transferred from
> simulation" as a claim whose strength depends on which side of that line the task sits.

<svg viewBox="0 0 560 282" style="max-width:100%;height:auto" role="img" aria-label="a parameter gap where randomization spans the real curve, next to a contact gap where every simulated curve is smooth and the real one has a jump">
  <g font-size="11" fill="currentColor">
    <text x="50" y="16">a parameter problem</text><text x="330" y="16">a model problem</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.75">
    <text x="50" y="29">dynamics &#183; sensing &#183; task distribution &#183; implementation</text><text x="330" y="29">contact &#8212; friction against slip velocity</text>
  </g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.5" fill="none">
    <polyline points="50,40 50,150 250,150"/>
    <line x1="330" y1="105" x2="530" y2="105"/>
    <line x1="430" y1="44" x2="430" y2="154"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.4" stroke-dasharray="5 4">
    <path d="M50,132 C110,106 180,84 250,72"/>
    <path d="M50,144 C110,122 180,102 250,92"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <path d="M50,138 C110,114 180,93 250,82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.45" stroke-dasharray="5 4">
    <path d="M338,74 C412,74 448,136 522,136"/>
    <path d="M338,86 C412,86 448,124 522,124"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <polyline points="338,66 428,66"/>
    <polyline points="432,144 522,144"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="62" y="58">the real system lies inside the spread</text>
    <text x="330" y="176">every simulated curve is smooth</text>
    <text x="330" y="190">the real one jumps at the stick&#8211;slip transition</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">Left: the physics is right and a number is wrong, so a distribution over that number covers the</text>
    <text x="24" y="228">real system. Right: stick becomes slip discontinuously, and a regularized rigid-body contact</text>
    <text x="24" y="244">passes smoothly through exactly there. Randomizing the friction coefficient slides those curves</text>
    <text x="24" y="260">up and down; it does not give them a shape they cannot take. That is the whole reason a</text>
    <text x="24" y="276">locomotion transfer and an insertion transfer are not comparable evidence.</text>
  </g>
</svg>

### 2. Main strategies

- **System identification** fits simulator parameters to measured trajectories. It makes
  one simulator more faithful but can overfit one machine and one operating condition.
  The stream's canonical payoff is [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL]]:
  a learned neural-network valve/actuator model makes the excavator simulator faithful
  enough that the RL policy runs on the real M545 without fine-tuning.
- **Domain randomization** trains across a distribution of dynamics, sensing, and scene
  parameters. Success depends on whether the real system lies inside a useful training
  distribution; “more random” is not automatically better.
- **Teacher–student / privileged learning** lets a teacher observe simulator-only state
  (terrain parameters, perfect pose) and distills behavior into a student using deployable
  observations. Always check what information exists at test time.
- **Residual learning** keeps a model-based controller and learns a correction. This can
  reduce the search space, but safety still depends on how the residual is bounded.
- **Real-data adaptation** fine-tunes representations, dynamics, or policies using a
  small real dataset. Report how much real machine time and human intervention it costs.
- **Parallel simulation** creates experience quickly; it improves sample throughput, not
  simulator validity. Thousands of environments can repeat the same wrong physics.

### 3. A deployment ladder

1. Simulator-only evaluation with held-out parameters —
   [[01-canonical-papers/notes/8-construction/exact-2024|ExACT]] sits here: end-to-end
   imitation from multimodal sensors to hydraulic valve commands, validated in simulation
   only, so its claim stops at this rung.
2. Hardware-in-the-loop and timing/saturation tests.
3. Slow, supervised real trials inside a safety envelope.
4. Adaptation without changing the evaluation cases.
5. Repeated operation across materials, machines, sites, and days.

Zero-shot transfer means no target-domain training update before deployment; it does not
mean no real-system knowledge was used to build or tune the simulator.

### 4. Reading the evidence

> [!warning] Reading the claim · 핵심 주장 읽는 법
> “Successful sim-to-real transfer” proves transfer only for the reported machine,
> operating range, and intervention protocol. Find the randomized variables, real-data
> budget, safety controller, failed trials, and whether evaluation conditions were used
> while tuning. A video is evidence of possibility, not a transfer distribution.

Useful measures include real/sim performance ratio, interventions per hour, constraint
violations, performance across parameter shifts, adaptation data/time, and degradation
outside the training range.

### After reading

- Separate dynamics, contact, sensing, task, and implementation gaps.
- Explain system identification, domain randomization, privileged learning, residuals,
  and real-data adaptation without treating them as interchangeable.
- Identify simulator-only information and the real-data budget in a paper.
- State what evidence would support generalization beyond one machine and one soil bin.

### Self-check

1. A team scales training from 100 to 10,000 parallel environments and reports better
   sim performance. Why might the real-machine result not improve at all?
2. Egli RL transferred zero-shot to the real M545. What did "zero-shot" cost upstream,
   and what does the term not mean?
3. A teacher policy uses ground-truth soil parameters; the student uses joint and
   pressure signals. What is the single most important check before believing the
   deployment claim?
4. ExACT and ExT both apply imitation learning to excavation. Why do their claims sit on
   different rungs of the deployment ladder?

> [!tip]- Answers
> 1. Parallelism raises sample throughput, not simulator validity: 10,000 environments can repeat the same wrong hydraulics, contact, and sensing physics. If the dominant gap is a modeling error rather than sample scarcity, more samples converge harder onto the wrong optimum.
> 2. Upstream it cost real-machine data and engineering to fit the neural-network valve/actuator model — real-system knowledge baked into the simulator. "Zero-shot" means no target-domain training update before deployment; it does not mean the simulator was built without real data, nor that transfer holds beyond the identified machine and operating range.
> 3. Whether every observation the student consumes actually exists, at deployment rate and latency, on the real machine — and whether the distillation was evaluated with realistic noise on those signals. Privileged learning fails silently when test-time observability is quietly optimistic.
> 4. ExACT is validated in simulation only, so its evidence stops at rung 1 (simulator-only evaluation); ExT reports centimeter-level transfer on a real machine, reaching the supervised real-trial rungs. Same method family, different evidentiary weight — the ladder, not the method name, sets the claim.

### Sources


- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — which simulator actually models terrain and contact, and what each one leaves out.
- [Tobin et al., *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World*](https://arxiv.org/abs/1703.06907)
- [Peng et al., *Sim-to-Real Transfer of Robotic Control with Dynamics Randomization*](https://arxiv.org/abs/1710.06537)
- [Lee et al., *Learning Quadrupedal Locomotion over Challenging Terrain*](https://www.science.org/doi/10.1126/scirobotics.abc5986) — privileged learning example

## 한국어

시뮬레이션은 위험하고 느리며 비싼 로봇 경험을 싸게 만든다. 그 경험을 현실로 만들어 주지는
않는다. **Sim-to-real**은 시뮬레이터의 가정이 깨져도 정책이 쓸모 있도록 만드는 모델링·학습·
적응·평가 방법의 묶음이다.

> [!info] 깊이 목표
> Sim-to-real 논문을 읽고 다음을 짚는다: 어느 격차(동역학·접촉·센싱·과제·구현)가
> 지배적인지, 어떤 전략이 어떤 비용으로 이를 다루는지, 전이가 소비한 실데이터·개입
> 예산은 얼마인지, 증거가 배치 사다리의 어느 단에 실제로 도달하는지. 전이 파이프라인
> 설계는 실무/숙달 단계의 주제다.

> [!note] 선수 지식
> [[02-foundations/probability|확률]] · [[02-foundations/rl-basics|RL 기초]] ·
> [[04-robotics/robot-systems-deployment|로봇 시스템]] · [[04-robotics/contact-force-tactile|접촉]]

### 1. Reality gap은 어디서 생기나

| 격차 | 필드 로봇의 예 | 대표 대응 |
|---|---|---|
| 동역학 | 질량·마찰·유압 지연·백래시 | 시스템 식별, 파라미터 랜덤화, 잔차 모델 |
| 접촉·재료 | 흙·잔해·타이어 슬립·절삭 저항 | 지형 랜덤화, 학습 접촉 모델, 온라인 적응 |
| 센싱 | 먼지·눈부심·진동·지연·LiDAR 누락 | 노이즈/지연 모델, 증강, 강건 추정 |
| 과제 분포 | 새로운 현장·형상·날씨·작업자 | 절차적 장면, 커리큘럼, 실제 데이터 파인튜닝 |
| 구현 | 제어 주기·포화·메시지 손실 | hardware-in-the-loop, 지연·한계 랜덤화 |

핵심 질문은 “그래픽이 사실적인가?”가 아니라 **정책에 영향을 주는 변수를 무엇까지 표현·
변동·적응했는가**다.

> [!warning] 접촉 행은 나머지와 성격이 다르다
> 다른 네 격차는 *파라미터* 문제다. 물리는 맞고 숫자가 틀렸으니 동정이나 랜덤화가 메운다. 접촉은
> **모델** 문제다. 강체 엔진은 접촉을 매 시간 단계마다 푸는 점 구속으로 처리하는데, 바탕 동역학이
> 실제로 비평활하다 — 충격과 고착–미끄러짐 천이가 불연속이고, 수치 적분기는 정확히 거기서 정확도와
> 안정성을 함께 잃는다. **마찰 계수를 랜덤화한다고, 접촉 패치를 애초에 표현하지 못하는 접촉 모델이
> 고쳐지지는 않는다.**
>
> 그래서 접촉이 많은 결과와 보행 결과는 같은 시뮬레이터에서 나왔더라도 sim-to-real 성숙도의 증거로
> 비교할 수 없다. 사족보행은 거친 접촉 모델을 견딘다 — 정책이 50 Hz로 외란을 기각하고 있고 발은
> 미끄러지지만 않으면 되기 때문이다. 반면 삽입·드릴링·패널 안착은 그 모델이 표현하지 못하는 접촉
> 패치로 *정의되는* 과제다. "시뮬레이션에서 전이했다"는 주장의 강도는 과제가 이 선의 어느 쪽에
> 있느냐에 달려 있다.
<svg viewBox="0 0 560 266" style="max-width:100%;height:auto" role="img" aria-label="랜덤화가 실제 곡선을 덮는 파라미터 격차와, 시뮬레이션 곡선은 모두 매끄러운데 실제는 도약하는 접촉 격차">
  <g font-size="11" fill="currentColor">
    <text x="50" y="16">파라미터 문제</text><text x="330" y="16">모델 문제</text>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.75">
    <text x="50" y="29">동역학 &#183; 센싱 &#183; 과제 분포 &#183; 구현</text><text x="330" y="29">접촉 &#8212; 미끄럼 속도에 대한 마찰력</text>
  </g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.5" fill="none">
    <polyline points="50,40 50,150 250,150"/>
    <line x1="330" y1="105" x2="530" y2="105"/>
    <line x1="430" y1="44" x2="430" y2="154"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.4" stroke-dasharray="5 4">
    <path d="M50,132 C110,106 180,84 250,72"/>
    <path d="M50,144 C110,122 180,102 250,92"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <path d="M50,138 C110,114 180,93 250,82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" opacity="0.45" stroke-dasharray="5 4">
    <path d="M338,74 C412,74 448,136 522,136"/>
    <path d="M338,86 C412,86 448,124 522,124"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <polyline points="338,66 428,66"/>
    <polyline points="432,144 522,144"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="62" y="58">실제는 이 퍼짐 안에 있다</text>
    <text x="330" y="176">시뮬레이션 곡선은 모두 매끄럽다</text>
    <text x="330" y="190">실제는 고착&#8211;미끄럼 천이에서 도약한다</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">왼쪽: 물리는 맞고 숫자가 틀렸으니, 그 숫자에 대한 분포가 실제 시스템을 덮는다. 오른쪽: 고착이</text>
    <text x="24" y="228">미끄럼으로 넘어가는 순간이 불연속인데, 정규화된 강체 접촉은 하필 그 자리를 매끄럽게 지난다.</text>
    <text x="24" y="244">마찰 계수를 흔들면 저 곡선들이 위아래로 움직일 뿐, 그들이 가질 수 없는 형태를 만들어 주지는</text>
    <text x="24" y="260">않는다. 보행 전이와 삽입 전이가 비교 가능한 증거가 아닌 이유가 이것 하나다.</text>
  </g>
</svg>


### 2. 주요 전략

- **시스템 식별**은 측정 궤적에 시뮬레이터 파라미터를 맞춘다. 한 조건에는 정확해지지만 한
  기계에 과적합할 수 있다. 이 스트림의 정본 성과가
  [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL]]이다: 학습된 신경망
  밸브/액추에이터 모델이 굴착기 시뮬레이터를 충분히 충실하게 만들어 RL 정책이 파인튜닝
  없이 실제 M545에서 돈다.
- **도메인 랜덤화**는 동역학·센싱·장면 파라미터의 분포에서 학습한다. 현실이 유용한 학습
  분포 안에 있어야 하며, 무조건 더 많이 흔든다고 좋아지지 않는다.
- **교사–학생/privileged learning**은 교사가 완벽한 자세나 지반 파라미터 같은 시뮬레이터
  전용 상태를 보고, 배치 가능한 관측만 쓰는 학생에게 행동을 증류한다. 시험 때 가능한
  정보를 반드시 확인하라.
- **잔차 학습**은 모델 기반 제어기를 유지하고 보정량만 학습한다. 탐색 공간을 줄이지만 잔차
  한계와 안전 보장은 별개다.
- **실데이터 적응**은 소량의 실제 데이터로 표현·동역학·정책을 조정한다. 실제 장비 시간과
  인간 개입 비용을 보고해야 한다.
- **병렬 시뮬레이션**은 경험 생산량을 늘릴 뿐 물리의 타당성을 보장하지 않는다.

### 3. 배치 사다리

1. 보지 않은 파라미터에서 시뮬레이터 평가 —
   [[01-canonical-papers/notes/8-construction/exact-2024|ExACT]]가 여기에 있다:
   멀티모달 센서에서 유압 밸브 명령까지의 end-to-end 모방이지만 시뮬레이션 검증뿐이라
   주장은 이 단에서 멈춘다
2. hardware-in-the-loop와 지연·포화 시험
3. 안전 영역 안의 저속·감독 실제 시험
4. 평가 사례를 보며 튜닝하지 않는 적응
5. 재료·기계·현장·날짜를 바꾼 반복 운용

Zero-shot transfer는 배치 전에 목표 도메인 학습 업데이트가 없다는 뜻이지, 시뮬레이터를
만드는 데 실제 시스템 지식을 전혀 쓰지 않았다는 뜻이 아니다.

### 4. 증거 읽기

> [!warning] 주장 읽기
> “성공적인 sim-to-real”은 보고된 기계·운용 범위·개입 규약에서만 전이를 증명한다. 랜덤화한
> 변수, 실데이터 예산, 안전 제어기, 실패 시행, 평가 조건을 튜닝에 썼는지 확인하라. 영상은
> 가능성의 증거이지 전이 분포의 증거가 아니다.

유용한 측정값은 현실/시뮬 성능 비율, 시간당 개입, 제약 위반, 파라미터 변화별 성능, 적응
데이터·시간, 학습 범위 밖의 성능 저하다.

### 읽고 나면 말할 수 있어야 하는 것

- 동역학·접촉·센싱·과제·구현 격차를 구분한다.
- 시스템 식별, 도메인 랜덤화, privileged learning, 잔차, 실데이터 적응을 구별한다.
- 논문의 시뮬레이터 전용 정보와 실데이터 예산을 찾는다.
- 한 기계·한 토조를 넘어선 일반화를 지지할 증거를 말한다.

### 스스로 점검

1. 병렬 환경을 100개에서 10,000개로 늘려 시뮬레이션 성능이 좋아졌다. 실기계 결과는 왜
   전혀 나아지지 않을 수 있는가?
2. Egli RL은 실제 M545에 zero-shot으로 전이했다. "zero-shot"이 상류에서 무엇을
   지불했으며, 이 용어가 뜻하지 않는 것은?
3. 교사 정책은 지반 파라미터의 정답을 쓰고, 학생은 관절·압력 신호를 쓴다. 배치 주장을
   믿기 전에 가장 중요한 단일 확인 사항은?
4. ExACT와 ExT는 둘 다 굴착에 모방 학습을 적용한다. 두 주장은 왜 배치 사다리의 다른
   단에 있는가?

> [!tip]- 정답 · Answers
> 1. 병렬화는 샘플 생산량을 올릴 뿐 시뮬레이터 타당성을 올리지 않는다: 10,000개 환경이 같은 잘못된 유압·접촉·센싱 물리를 반복할 수 있다. 지배적 격차가 샘플 부족이 아니라 모델링 오류라면, 더 많은 샘플은 잘못된 최적점에 더 세게 수렴한다.
> 2. 상류에서는 신경망 밸브/액추에이터 모델을 맞추기 위한 실기계 데이터와 엔지니어링 — 실제 시스템 지식을 시뮬레이터에 구워 넣은 것 — 을 지불했다. "Zero-shot"은 배치 전 목표 도메인 학습 업데이트가 없다는 뜻이지, 시뮬레이터를 실데이터 없이 만들었다거나 식별된 기계·운용 범위 너머로 전이가 유지된다는 뜻이 아니다.
> 3. 학생이 소비하는 모든 관측이 실기계에서 배치 주기와 지연으로 실제로 존재하는지 — 그리고 그 신호의 현실적 노이즈 아래에서 증류가 평가되었는지. Privileged learning은 시험 시점 관측 가능성이 조용히 낙관적일 때 소리 없이 실패한다.
> 4. ExACT는 시뮬레이션 검증뿐이라 증거가 1단(시뮬레이터 평가)에서 멈춘다; ExT는 실기계에서 센티미터급 전이를 보고해 감독 실기 시험 단까지 도달한다. 같은 방법 계열, 다른 증거 무게 — 주장을 정하는 것은 방법 이름이 아니라 사다리다.

### 출처


- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — 어느 시뮬레이터가 실제로 지형과 접촉을 모델링하는가, 그리고 각각이 무엇을 빠뜨리는가.
- [Tobin et al., Domain Randomization](https://arxiv.org/abs/1703.06907)
- [Peng et al., Dynamics Randomization](https://arxiv.org/abs/1710.06537)
- [Lee et al., challenging-terrain locomotion](https://www.science.org/doi/10.1126/scirobotics.abc5986)
