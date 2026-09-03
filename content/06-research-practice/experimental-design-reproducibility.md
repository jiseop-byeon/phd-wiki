---
title: 2. Experimental Design & Reproducibility
tags: [research, experiments, reproducibility]
study-depth: Working
depth-goal: "Apply the procedure when forming claims, running experiments, analyzing failure, and writing."
mastery-when: "Mastery means consistently producing defensible work, not memorizing the page."
---

## English

An experiment should distinguish the proposed explanation from plausible alternatives. In robotics, this requires controlling not only models and datasets but scenes, hardware, calibration, operators, resets, timing, and exposure to failures.

> [!note] Prerequisites
> Read [[02-foundations/ml-practice|ML Practice & Evaluation]] first. That page teaches how to read results; this page focuses on designing evidence.

### 1. Variables and units of analysis

- **Independent variable:** factor intentionally changed.
- **Dependent variable:** measured outcome.
- **Control variables:** conditions held fixed or modeled.
- **Experimental unit:** independent entity assigned to a condition—seed, scene, object, participant, robot, or site.

Repeated frames from one robot run are not thousands of independent trials.

When the experimental unit is a *person*, this page's logic still applies but the measurement procedures are their own settled subject — [[06-research-practice/psychophysics-human-measurement|8. Psychophysics & Human Measurement]] is this page's toolbox for that case.

For example, a tactile grasping study may assign surface conditions to objects while training several policy seeds. Repeated attempts on the same object help estimate performance on that object; they do not create new independent materials. Decide whether the intended claim concerns new objects, new surfaces, or training variability before choosing an aggregation. **The reading this gives you.** Look for the entity that could have been independently assigned to another condition. That entity determines which observations are clustered and what population the uncertainty can reasonably describe.

> [!note] Verification is not validation · 검증과 타당성 확인은 다르다
> Two different questions hide under the word "testing", and a design that answers one does
> not answer the other. *Verification* asks whether the system was built the way it was
> specified: does the code match the spec, are the interlocks wired as documented, is the
> model version the one reported. *Validation* asks whether the specification is the right
> one: does the benchmark's definition of success match the behaviour a user actually wants,
> does the test environment represent the deployment environment. A robot can pass every
> verification test and still be validated against the wrong target — and the failure will
> look like a modelling problem rather than a design one.
>
> Deciding which of the two a study is producing belongs in the design, before the runs
> start. Two further consequences. The variables and units above serve verification claims
> naturally, while validation usually needs a comparison the experiment was not built for.
> And neither ends at publication: a deployed system meets changing environments and ageing
> hardware, so staying inside acceptable risk is something to keep checking, not something
> established once. Synthesised from Giseop Kim's essay
> [AI가 만든 결과를 검증하는 능력](https://gisbi-kim.github.io/ai-verification-for-robotics/).

### 2. Comparisons

A strong baseline isolates the proposed contribution. Include a practical existing system, a simpler method, and when useful an **oracle** that uses unavailable information to estimate an upper bound. The oracle must be labeled; it is not a deployable competitor.

Use paired comparisons when the same scenes/tasks can be evaluated under both conditions. Randomize or counterbalance order to reduce learning, battery, wear, weather, and operator effects.

A comparison is explanatory only when the changed factors match the question. Suppose a new tactile architecture also receives additional demonstrations and a different pretrained encoder, while the baseline is trained from scratch. A higher score could come from the architecture, data, representation, or their interaction. This is the confound identified in the self-check; putting it in the design prevents an ambiguous headline result.

For a system-level comparison, the complete packages can still be useful competitors if their resources are disclosed. For an architecture claim, add a comparison with matched data, initialization, tuning opportunity, and control interface.

**The reading this gives you.** Read the baseline description as a list of information and resources available to each method. Ask which difference the reported outcome can isolate. An oracle answers how much headroom better information might offer; it cannot establish that a deployable method actually obtains that information.

### 3. Variation and splits

Separate training/tuning/test data and document the unit of split. Random frames from the same trajectory leak scene, object, and temporal information. Test across relevant variation: tasks, layouts, materials, lighting/weather, hardware, operators, speed, and failure perturbations.

> [!example] Worked example · 계산 예제
> **A small reported gain needs a variability context.** In a hypothetical experiment, seed-to-seed standard deviation is 4 percentage points. With 3 independent seeds, the standard error of the mean is 4/√3 ≈ 2.3 percentage points; with 5 it is about 1.8, and with 10 about 1.3.
>
> A 3 percentage point improvement is of a similar scale to this uncertainty. Standard error is not a confidence interval, and the uncertainty of a difference also depends on the baseline and whether the design is paired. These values alone therefore establish neither significance nor its absence.
>
> **The reading this gives you.** Ask for seed count, variation, and the comparison design before interpreting a small improvement. Additional seeds measure training variability; they do not repair leakage from splitting neighboring frames across training and test, or substitute for testing genuinely new surfaces.

### 4. Trials and uncertainty

Report trial count, independent runs, failures, exclusions, aggregation, and an uncertainty measure appropriate to the design. A seed captures only software randomness; physical trials vary through calibration, wear, temperature, material, timing, and people.

Predeclare primary outcomes when many metrics and conditions make cherry-picking likely. Statistical significance and practical importance are different ([[02-foundations/ml-practice|ML Practice §5]]). Two literacy-level tools for reasoning about n: a success rate from $n$ trials has a 95% CI half-width of **at most** $\pm 1/\sqrt{n}$ (10 trials → ±32%p; 100 → ±10%p). **That bound is the widest the interval ever gets, and it is reached only at $p = 0.5$** — near 0 or 1 it is far too pessimistic (at $p = 0.9$, $n = 10$, the true half-width is ±19%p), and it produces impossible bounds above 100%, so at high success rates use a Wilson or exact interval instead. Second: if zero failures are observed in $n$ trials, the rule of three puts the 95% **upper confidence bound** on the true failure rate at $\approx 3/n$ — an approximation that only holds for $n \gtrsim 30$; at $n = 10$ the exact bound is 26%, not 30%, and at $n = 5$ it is 45%, not 60%.

<svg viewBox="0 0 470 214" style="max-width:100%;height:auto" role="img" aria-label="how the uncertainty of a success rate shrinks with the number of trials">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="55" y1="24" x2="55" y2="140"/><line x1="55" y1="140" x2="415" y2="140"/><line x1="55.0" y1="140" x2="55.0" y2="146"/><line x1="100.8" y1="140" x2="100.8" y2="146"/><line x1="173.4" y1="140" x2="173.4" y2="146"/><line x1="252.9" y1="140" x2="252.9" y2="146"/><line x1="325.5" y1="140" x2="325.5" y2="146"/><line x1="405.0" y1="140" x2="405.0" y2="146"/></g>
  <path d="M55.0 90.8L58.8 92.2L62.7 93.6L66.5 94.9L70.4 96.2L74.2 97.5L78.1 98.7L81.9 99.9L85.8 101.0L89.6 102.2L93.5 103.2L97.3 104.3L101.2 105.3L105.0 106.3L108.9 107.3L112.7 108.2L116.6 109.1L120.4 110.0L124.3 110.9L128.1 111.7L132.0 112.5L135.8 113.3L139.7 114.1L143.5 114.8L147.4 115.6L151.2 116.3L155.1 116.9L158.9 117.6L162.8 118.2L166.6 118.9L170.5 119.5L174.3 120.1L178.2 120.6L182.0 121.2L185.9 121.7L189.7 122.3L193.6 122.8L197.4 123.3L201.3 123.7L205.1 124.2L209.0 124.7L212.8 125.1L216.7 125.5L220.5 125.9L224.4 126.3L228.2 126.7L232.1 127.1L235.9 127.5L239.8 127.9L243.6 128.2L247.5 128.5L251.3 128.9L255.2 129.2L259.0 129.5L262.9 129.8L266.7 130.1L270.6 130.4L274.4 130.7L278.3 130.9L282.1 131.2L286.0 131.4L289.8 131.7L293.6 131.9L297.5 132.2L301.3 132.4L305.2 132.6L309.0 132.8L312.9 133.0L316.7 133.2L320.6 133.4L324.4 133.6L328.3 133.8L332.1 134.0L336.0 134.1L339.8 134.3L343.7 134.5L347.5 134.6L351.4 134.8L355.2 134.9L359.1 135.1L362.9 135.2L366.8 135.4L370.6 135.5L374.5 135.6L378.3 135.7L382.2 135.9L386.0 136.0L389.9 136.1L393.7 136.2L397.6 136.3L401.4 136.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M55.0 74.0L58.8 77.7L62.7 81.3L66.5 84.6L70.4 87.7L74.2 90.7L78.1 93.5L81.9 96.1L85.8 98.6L89.6 100.9L93.5 103.1L97.3 105.2L101.2 107.2L105.0 109.1L108.9 110.8L112.7 112.5L116.6 114.0L120.4 115.5L124.3 116.9L128.1 118.2L132.0 119.4L135.8 120.6L139.7 121.7L143.5 122.7L147.4 123.7L151.2 124.6L155.1 125.5L158.9 126.3L162.8 127.1L166.6 127.8L170.5 128.5L174.3 129.2L178.2 129.8L182.0 130.4L185.9 130.9L189.7 131.4L193.6 131.9L197.4 132.4L201.3 132.8L205.1 133.2L209.0 133.6L212.8 133.9L216.7 134.3L220.5 134.6L224.4 134.9L228.2 135.2L232.1 135.5L235.9 135.7L239.8 136.0L243.6 136.2L247.5 136.4L251.3 136.6L255.2 136.8L259.0 137.0L262.9 137.2L266.7 137.3L270.6 137.5L274.4 137.6L278.3 137.8L282.1 137.9L286.0 138.0L289.8 138.1L293.6 138.2L297.5 138.3L301.3 138.4L305.2 138.5L309.0 138.6L312.9 138.7L316.7 138.7L320.6 138.8L324.4 138.9L328.3 138.9L332.1 139.0L336.0 139.1L339.8 139.1L343.7 139.2L347.5 139.2L351.4 139.3L355.2 139.3L359.1 139.3L362.9 139.4L366.8 139.4L370.6 139.4L374.5 139.5L378.3 139.5L382.2 139.5L386.0 139.6L389.9 139.6L393.7 139.6L397.6 139.6L401.4 139.7" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/>
  <g fill="currentColor"><circle cx="100.8" cy="105.2" r="3.5"/><circle cx="252.9" cy="129.0" r="3.5"/><circle cx="405.0" cy="136.5" r="3.5"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="55.0" y="158">5</text><text x="100.8" y="158">10</text><text x="173.4" y="158">30</text><text x="252.9" y="158">100</text><text x="325.5" y="158">300</text><text x="405.0" y="158">1000</text>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="10" y="34">uncertainty</text>
    <text x="106.8" y="101.2">&#177;32%p</text>
    <text x="258.9" y="125.0">&#177;10%p</text>
    <text x="365.0" y="130.5">&#177;3%p</text>
    <text x="316" y="172">number of trials n (log scale)</text>
  </g>
  <g stroke="currentColor"><line x1="55" y1="180" x2="85" y2="180" stroke-width="2"/><line x1="55" y1="196" x2="85" y2="196" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="92" y="184">maximum CI half-width, &#8776; 1/&#8730;n</text><text x="92" y="200">rule of three: 95% upper bound on failure rate after zero failures, 3/n (n &#8807; 30)</text></g>
</svg>



### 5. Ablations and budgets

An ablation may remove or change architecture, objective, data, sensing, controller, or hyperparameter. Hold the rest constant enough to isolate interpretation. Compare data, compute, tuning effort, pretrained assets, sensors, and control interface—not architecture names alone.

Budget matching matters because removing a component may also remove resources. If the tactile model receives more optimization steps than its ablation, the comparison changes both information and training effort. Conversely, forcing an ablation to use an unsuitable inherited hyperparameter can make a useful simpler method look artificially weak.

For example, evaluate the full and reduced grasping policies with declared training budgets and comparable tuning opportunities. Keep demonstrations, test conditions, and the downstream controller fixed for the question about tactile information. If additional compute is required to exploit touch, report that trade-off explicitly rather than hiding it in the component label.

**The reading this gives you.** Ask what remained matched and what was retuned. An ablation supports a conclusion under that resource allocation. A separate equal-compute comparison may be needed to ask which system is preferable under a deployment budget. Neither comparison automatically answers the other's question.

### 6. Reproducibility vocabulary

Terminology differs across communities, so define it. A useful convention is:

- **Repeatability:** same team, setup, and procedure obtains compatible results.
- **Reproducibility:** independent team uses provided artifacts/procedure and obtains compatible results.
- **Replicability:** independent implementation or study tests the same claim.

The distinction is useful because a repeated number can come from very different evidence. Your own team rerunning a saved grasping configuration checks internal consistency. Another team using the released checkpoint checks whether the provided artifacts and instructions transfer. A separate implementation testing the same friction hypothesis probes dependence on the original code and engineering choices.

Report what was actually repeated: data, implementation, hardware, protocol, or the scientific claim. Do not rely on the label alone, especially when a venue defines these words differently.

**The reading this gives you.** Inspect the shared and changed ingredients behind a reproduction statement. A successful rerun on the original logs establishes less about new physical conditions than a study on independently prepared surfaces, even if both are described with the same convenient word.

### 7. Artifact checklist

Record code commit, dependencies/container, model and data versions, splits, seeds, training commands, configurations, calibration, frame conventions, controller gains, firmware, hardware revision, trial protocol, raw logs, exclusions, and analysis scripts. Provide enough detail to reconstruct what physically happened.

A checklist becomes useful when its entries reconstruct a specific attempt. For example, a tactile grasp can fail because the saved sensor calibration no longer matches the mounted pad. Releasing training code does not reveal that discrepancy. The trial record must connect the calibration and hardware state to the checkpoint and command stream used that day.

Link each reported run to a configuration snapshot and a raw log, and preserve the analysis command that produced its result. Record exclusions with reasons so another reader can recover the denominator. Also document the reset procedure: a carefully prepared starting pose may be an essential experimental condition.

**The reading this gives you.** Choose one result and ask whether its complete path back to a physical attempt is recoverable. Missing entries identify a reproducibility limitation more precisely than a general statement that the code is available.

### 8. Worked design

Claim: tactile sensing improves insertion recovery. Use the same robot, controller, demonstrations, objects, initial offsets, and failure perturbations. Compare vision-only and vision+tactile in randomized paired trials. Report insertion success, peak force, recovery time, damage, interventions, latency, and failure taxonomy across held-out clearances/materials.

Which of these choices to make is settled by the claim–evidence table in [[06-research-practice/research-questions-claims|Research Questions §7]], filled before any run. For a complete design of the friction question in [[06-research-practice/research-questions-claims|Research Questions §1]], start with the uncertainty: does contact-time estimation of μ recover grasp success lost when the planner assumes incorrect friction? This is a proposed experiment, not a report of an advantage already observed.

Define the intervention as enabling friction updates from the available tactile stream. Use the same planner with fixed μ as the comparator, and keep grasp candidates, demonstrations, control interface, and sensing opportunities comparable. A reference-friction condition can diagnose headroom if its privileged information is labeled. It must not be presented as an equally deployable policy.

Define units before counting trials. Objects and independently prepared surface conditions support claims about physical variation; training seeds support claims about optimization variability. Attempts within one object-condition group are repeated observations. Record their grouping rather than treating every sensor frame as independent evidence. Hold out the surface conditions needed for the transfer claim and keep them out of tuning.

Randomize or counterbalance method order within matched conditions. Record surface preparation, contact timing, failed grasps, operator stops, and resets. Predeclare whether an intervention ends the autonomous attempt. Otherwise one method can receive more rescue and appear better without making better decisions.

Choose the sample size from the required precision and the claim, using §4's uncertainty tools as planning guides. Do not select a convenient count and declare reliability afterward; a rare-failure claim needs a different exposure argument from an average-performance comparison. Use appropriate intervals and preserve clustering in the analysis.

Report success with uncertainty, recovery behavior, estimation timing, and failure categories for each condition. Include the cost of unnecessary corrections and the effect of compute latency. A finding that updates arrive after the decisive contact would locate a useful sensing boundary even without a success-rate gain. The final claim should distinguish this mechanistic evidence from the broader question of transfer across construction tasks.

### After reading

- Identify variables and the true experimental unit.
- Design a matched baseline and label oracle information.
- Detect temporal/scene leakage in robot datasets.
- Choose trials and uncertainty appropriate to physical variation.
- Specify artifacts needed to reconstruct hardware and software conditions.

### Self-check

1. Why are 10,000 video frames from one run not 10,000 trials?
2. When is a paired design useful?
3. What is unfair about comparing a pretrained model with extra data to a scratch baseline without disclosure?
4. Why does sharing code alone not reproduce a robot experiment?

> [!tip]- Answers
> 1. Frames share the same scene, state trajectory, calibration, and failure event. 2. When both methods can face the same task/scene/participant, reducing nuisance variation. 3. The comparison confounds architecture with data and pretraining. 4. Hardware, calibration, timing, control, materials, configuration, and procedures also determine outcomes.

### Sources

- [National Academies — *Reproducibility and Replicability in Science* (2019)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science) — the landmark report; note it splits the terms differently (reproducibility = same data + same computation, replicability = new data) than the ACM-style convention presented above
- [Artifact Evaluation (artifact-eval.org)](https://www.artifact-eval.org/) — what independent artifact reviewers actually check
- [Sandve et al., *Ten Simple Rules for Reproducible Computational Research* (PLOS Comp Biol 2013)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)

## 한국어

실험은 제안한 설명을 그럴듯한 대안들과 구분해야 한다. 로보틱스에서는 모델·데이터셋만이
아니라 장면, 하드웨어, 보정, 운용자, 리셋, 타이밍, 실패 노출까지 통제 대상이다.

> [!note] 선수 지식
> [[02-foundations/ml-practice|ML 실무와 평가]]를 먼저 읽어라. 그 페이지는 결과를 *읽는*
> 법을, 이 페이지는 증거를 *설계하는* 법을 다룬다.

### 1. 변수와 분석 단위

- **독립 변수:** 의도적으로 바꾸는 요인.
- **종속 변수:** 측정되는 결과.
- **통제 변수:** 고정하거나 모델링하는 조건.
- **실험 단위:** 조건에 배정되는 독립적 개체 — 시드, 장면, 물체, 참가자, 로봇, 현장.

한 로봇 실행의 반복 프레임들은 수천 개의 독립 시행이 아니다.

실험 단위가 *사람*일 때도 이 페이지의 논리는 그대로 적용되지만, 측정 절차는 그 자체로 정착된 별도 주제다 — [[06-research-practice/psychophysics-human-measurement|8. 심리물리와 인간 측정]]이 그 경우를 위한 이 페이지의 공구함이다.

예를 들어 촉각 파지 연구는 물체별 표면 조건을 배정하고 여러 정책 시드를 학습할 수 있다. 같은 물체의 반복 시도는 그 물체의 성능 추정을 돕지만 새로운 독립 재료를 만들지는 않는다. 새 물체, 새 표면, 학습 변동 중 무엇을 주장할지 먼저 정하고 집계한다. **여기서 얻는 독법.** 독립적으로 다른 조건에 배정될 수 있었던 대상을 찾는다. 그 대상에 따라 관측의 군집과 불확실성이 설명할 모집단이 정해진다.

> [!note] 검증과 타당성 확인은 다르다 · Verification is not validation
> "테스트"라는 한 단어 아래 서로 다른 두 질문이 숨어 있고, 한쪽에 답하는 설계가 다른 쪽에는
> 답하지 못한다. *Verification*(검증)은 시스템이 명세대로 만들어졌는지 묻는다. 코드가 명세와
> 맞는가, 인터록이 문서대로 배선됐는가, 모델 버전이 보고된 그것인가. *Validation*(타당성 확인)은
> 그 명세 자체가 옳은지 묻는다. 벤치마크의 성공 정의가 사용자가 실제로 원하는 행동과 같은가,
> 시험 환경이 배치 환경을 대표하는가. 로봇은 모든 verification 시험을 통과하고도 틀린 목표에
> validation될 수 있다. 그리고 그 실패는 설계 문제가 아니라 모델링 문제처럼 보인다.
>
> 이 연구가 둘 중 무엇을 생산하는지 정하는 일은 실행 전 설계 단계에 속한다. 귀결이 둘 더 있다.
> 위의 변수와 단위는 verification 주장을 자연스럽게 받쳐 주지만, validation은 대개 그 실험이
> 만들어지지 않은 비교를 요구한다. 그리고 둘 다 출판에서 끝나지 않는다. 배치된 시스템은 변하는
> 환경과 늙어 가는 하드웨어를 만나므로, 허용 가능한 위험 안에 머무는지는 한 번 확립하는 것이
> 아니라 계속 확인하는 일이다. 김기섭의 에세이
> [AI가 만든 결과를 검증하는 능력](https://gisbi-kim.github.io/ai-verification-for-robotics/)을
> 요약·재구성한 것이다.

### 2. 비교

강한 베이스라인은 제안된 기여를 분리한다. 실용적인 기존 시스템, 더 단순한 방법,
필요하면 사용할 수 없는 정보로 상한을 추정하는 **oracle**을 포함하라. Oracle은 표시돼야
하며 배포 가능한 경쟁자가 아니다.

같은 장면/과제를 두 조건에서 평가할 수 있으면 짝지은 비교를 써라. 학습·배터리·마모·
날씨·운용자 효과를 줄이도록 순서를 무작위화하거나 counterbalance하라.

바꾼 요인이 질문과 맞아야 설명력 있는 비교가 된다. 새 촉각 구조에 시연과 사전학습 인코더도 추가하고 베이스라인은 처음부터 학습했다고 하자. 점수 차이는 구조, 데이터, 표현 또는 상호작용에서 올 수 있다. 자가점검에서 지적한 혼입을 설계 단계에서 막아야 대표 결과의 의미가 흐려지지 않는다.

시스템 수준 비교라면 자원을 공개한 전체 패키지끼리의 경쟁도 유익하다. 구조에 대한 주장이면 데이터, 초기화, 튜닝 기회, 제어 인터페이스를 맞춘 비교를 추가한다.

**여기서 얻는 독법.** 베이스라인 설명을 각 방법이 가진 정보와 자원 목록으로 읽는다. 결과가 어느 차이를 분리할 수 있는지 묻는다. 오라클은 더 좋은 정보가 줄 여지를 보여 준다. 배포 가능한 방법이 그 정보를 실제 얻는다는 증거는 아니다.

### 3. 변동과 분할

학습/튜닝/시험 데이터를 분리하고 분할의 단위를 문서화하라. 같은 궤적의 무작위 프레임은
장면·물체·시간 정보를 누출한다. 관련 변동 전반 — 과제, 배치, 재료, 조명/날씨, 하드웨어,
운용자, 속도, 실패 교란 — 에 걸쳐 시험하라.

> [!example] 계산 예제 · Worked example
> **작은 개선에는 변동 정보가 필요하다.** 가상 실험에서 시드 간 표준편차가 4%p다. 독립 시드 3개면 평균의 표준오차는 4/√3 ≈ 2.3%p다. 5개면 약 1.8%p, 10개면 약 1.3%p다.
>
> 3%p 개선은 이 불확실성과 비슷한 규모다. 표준오차는 신뢰구간이 아니다. 차이의 불확실성은 베이스라인의 변동과 짝지은 설계 여부에도 달려 있다. 이 값만으로 유의하거나 유의하지 않다고 판정할 수 없다.
>
> **여기서 얻는 독법.** 작은 개선을 읽기 전에 시드 수, 변동, 비교 설계를 확인한다. 시드를 늘리면 학습 변동을 측정한다. 이웃 프레임을 학습과 시험으로 나눈 누수를 고치거나 새로운 표면의 시험을 대신하지는 못한다.

### 4. 시행 수와 불확실성

시행 수, 독립 실행, 실패, 제외, 집계 방식, 설계에 맞는 불확실성 지표를 보고하라. 시드는
소프트웨어 무작위성만 잡는다; 물리 시행은 보정, 마모, 온도, 재료, 타이밍, 사람을 통해
변한다.

지표와 조건이 많아 체리피킹이 쉬울 때는 주요 결과(primary outcome)를 미리 선언하라.
통계적 유의성과 실질적 중요성은 다르다([[02-foundations/ml-practice|ML 실무 §5]]).
시행 수를 가늠하는 문해력 수준의 도구 둘: $n$회 시행의 성공률 신뢰구간은 대략
**최대** $\pm 1/\sqrt{n}$이다(10회 → ±32%p; 100회 → ±10%p). **이 값은 구간이 가장 넓어질 때의 크기이고 $p = 0.5$에서만 도달한다** — 0이나 1 근처에서는 지나치게 비관적이고($p = 0.9$, $n = 10$이면 실제 반폭은 ±19%p), 100%를 넘는 불가능한 상한을 만든다. 그러니 성공률이 높을 때는 Wilson이나 정확 구간을 써라. 둘째, $n$회에서 실패 0이면 3의
법칙(rule of three)은 참 실패율의 95% **상한**을 $\approx 3/n$으로 준다 — $n \gtrsim 30$에서만 성립하는 근사이고, $n = 10$이면 정확한 상한이 30%가 아니라 26%, $n = 5$면 60%가 아니라 45%다.

<svg viewBox="0 0 470 214" style="max-width:100%;height:auto" role="img" aria-label="시행 횟수에 따라 성공률의 불확실성이 줄어드는 방식">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="55" y1="24" x2="55" y2="140"/><line x1="55" y1="140" x2="415" y2="140"/><line x1="55.0" y1="140" x2="55.0" y2="146"/><line x1="100.8" y1="140" x2="100.8" y2="146"/><line x1="173.4" y1="140" x2="173.4" y2="146"/><line x1="252.9" y1="140" x2="252.9" y2="146"/><line x1="325.5" y1="140" x2="325.5" y2="146"/><line x1="405.0" y1="140" x2="405.0" y2="146"/></g>
  <path d="M55.0 90.8L58.8 92.2L62.7 93.6L66.5 94.9L70.4 96.2L74.2 97.5L78.1 98.7L81.9 99.9L85.8 101.0L89.6 102.2L93.5 103.2L97.3 104.3L101.2 105.3L105.0 106.3L108.9 107.3L112.7 108.2L116.6 109.1L120.4 110.0L124.3 110.9L128.1 111.7L132.0 112.5L135.8 113.3L139.7 114.1L143.5 114.8L147.4 115.6L151.2 116.3L155.1 116.9L158.9 117.6L162.8 118.2L166.6 118.9L170.5 119.5L174.3 120.1L178.2 120.6L182.0 121.2L185.9 121.7L189.7 122.3L193.6 122.8L197.4 123.3L201.3 123.7L205.1 124.2L209.0 124.7L212.8 125.1L216.7 125.5L220.5 125.9L224.4 126.3L228.2 126.7L232.1 127.1L235.9 127.5L239.8 127.9L243.6 128.2L247.5 128.5L251.3 128.9L255.2 129.2L259.0 129.5L262.9 129.8L266.7 130.1L270.6 130.4L274.4 130.7L278.3 130.9L282.1 131.2L286.0 131.4L289.8 131.7L293.6 131.9L297.5 132.2L301.3 132.4L305.2 132.6L309.0 132.8L312.9 133.0L316.7 133.2L320.6 133.4L324.4 133.6L328.3 133.8L332.1 134.0L336.0 134.1L339.8 134.3L343.7 134.5L347.5 134.6L351.4 134.8L355.2 134.9L359.1 135.1L362.9 135.2L366.8 135.4L370.6 135.5L374.5 135.6L378.3 135.7L382.2 135.9L386.0 136.0L389.9 136.1L393.7 136.2L397.6 136.3L401.4 136.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M55.0 74.0L58.8 77.7L62.7 81.3L66.5 84.6L70.4 87.7L74.2 90.7L78.1 93.5L81.9 96.1L85.8 98.6L89.6 100.9L93.5 103.1L97.3 105.2L101.2 107.2L105.0 109.1L108.9 110.8L112.7 112.5L116.6 114.0L120.4 115.5L124.3 116.9L128.1 118.2L132.0 119.4L135.8 120.6L139.7 121.7L143.5 122.7L147.4 123.7L151.2 124.6L155.1 125.5L158.9 126.3L162.8 127.1L166.6 127.8L170.5 128.5L174.3 129.2L178.2 129.8L182.0 130.4L185.9 130.9L189.7 131.4L193.6 131.9L197.4 132.4L201.3 132.8L205.1 133.2L209.0 133.6L212.8 133.9L216.7 134.3L220.5 134.6L224.4 134.9L228.2 135.2L232.1 135.5L235.9 135.7L239.8 136.0L243.6 136.2L247.5 136.4L251.3 136.6L255.2 136.8L259.0 137.0L262.9 137.2L266.7 137.3L270.6 137.5L274.4 137.6L278.3 137.8L282.1 137.9L286.0 138.0L289.8 138.1L293.6 138.2L297.5 138.3L301.3 138.4L305.2 138.5L309.0 138.6L312.9 138.7L316.7 138.7L320.6 138.8L324.4 138.9L328.3 138.9L332.1 139.0L336.0 139.1L339.8 139.1L343.7 139.2L347.5 139.2L351.4 139.3L355.2 139.3L359.1 139.3L362.9 139.4L366.8 139.4L370.6 139.4L374.5 139.5L378.3 139.5L382.2 139.5L386.0 139.6L389.9 139.6L393.7 139.6L397.6 139.6L401.4 139.7" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/>
  <g fill="currentColor"><circle cx="100.8" cy="105.2" r="3.5"/><circle cx="252.9" cy="129.0" r="3.5"/><circle cx="405.0" cy="136.5" r="3.5"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="55.0" y="158">5</text><text x="100.8" y="158">10</text><text x="173.4" y="158">30</text><text x="252.9" y="158">100</text><text x="325.5" y="158">300</text><text x="405.0" y="158">1000</text>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="10" y="34">불확실성</text>
    <text x="106.8" y="101.2">&#177;32%p</text>
    <text x="258.9" y="125.0">&#177;10%p</text>
    <text x="365.0" y="130.5">&#177;3%p</text>
    <text x="316" y="172">시행 횟수 n (로그 축)</text>
  </g>
  <g stroke="currentColor"><line x1="55" y1="180" x2="85" y2="180" stroke-width="2"/><line x1="55" y1="196" x2="85" y2="196" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="92" y="184">신뢰구간 반폭의 최대치, &#8776; 1/&#8730;n</text><text x="92" y="200">3의 법칙: 실패 0회 뒤 실패율의 95% 상한, 3/n (n &#8807; 30)</text></g>
</svg>



### 5. 절제와 예산

절제는 구조, 목적함수, 데이터, 센싱, 제어기, 하이퍼파라미터를 제거하거나 바꿀 수 있다.
해석을 분리할 만큼 나머지를 고정하라. 구조 이름만이 아니라 데이터, 컴퓨트, 튜닝 노력,
사전학습 자산, 센서, 제어 인터페이스를 비교하라.

구성요소를 빼면서 자원도 뺄 수 있으므로 예산 정렬이 중요하다. 촉각 모델을 절제 모델보다 더 오래 학습하면 정보와 학습 노력이 함께 바뀐다. 반대로 절제 모델에 맞지 않는 하이퍼파라미터를 그대로 강요해도 단순한 방법을 부당하게 약화할 수 있다.

전체·축소 파지 정책에 학습 예산과 대등한 튜닝 기회를 명시한다. 촉각 정보의 가치를 묻는 비교에서는 시연, 시험 조건, 하류 제어기를 고정한다. 촉각을 활용하려면 연산이 더 필요할 경우 그 교환 관계를 드러낸다. 부품 이름 안에 숨기지 않는다.

**여기서 얻는 독법.** 무엇을 맞추고 무엇을 재튜닝했는지 묻는다. 절제는 해당 자원 배분 아래의 결론을 지지한다. 배포 예산에서 어느 시스템이 더 나은지는 별도의 동일 연산 비교가 필요할 수 있다. 두 비교가 서로의 질문에 자동으로 답하지는 않는다.

### 6. 재현성 어휘

용어가 커뮤니티마다 다르므로 정의하고 써라. 유용한 관례:

- **Repeatability:** 같은 팀·장비·절차로 양립 가능한 결과를 얻는다.
- **Reproducibility:** 독립 팀이 제공된 산출물·절차로 양립 가능한 결과를 얻는다.
- **Replicability:** 독립 구현·연구가 같은 주장을 시험한다.

같은 숫자의 반복도 서로 다른 증거에서 올 수 있어 이 구분이 유용하다. 자기 팀이 저장한 파지 설정을 다시 돌리면 내부 일관성을 확인한다. 다른 팀이 공개 체크포인트를 쓰면 산출물과 설명의 이전 가능성을 확인한다. 별도 구현으로 같은 마찰 가설을 시험하면 원래 코드와 공학적 선택에 대한 의존성을 살핀다.

데이터, 구현, 하드웨어, 절차, 과학적 주장 중 무엇을 반복했는지 적는다. 학회마다 용어 정의가 다를 수 있으므로 명칭에만 기대지 않는다.

**여기서 얻는 독법.** 재현 주장 뒤에서 공유한 것과 바꾼 것을 본다. 원래 로그의 재실행은 독립적으로 준비한 표면에서의 연구보다 새 물리 조건에 대해 적은 것을 말한다. 편의상 같은 단어를 쓰더라도 그렇다.

### 7. 산출물 체크리스트

코드 커밋, 의존성/컨테이너, 모델·데이터 버전, 분할, 시드, 학습 명령, 설정, 보정, 프레임
관례, 제어기 이득, 펌웨어, 하드웨어 리비전, 시행 프로토콜, 원시 로그, 제외, 분석
스크립트를 기록하라. 물리적으로 무슨 일이 있었는지 재구성할 수 있을 만큼 상세해야 한다.

목록은 특정 시도를 재구성할 때 유용해진다. 예를 들어 저장된 센서 보정이 장착한 패드와 맞지 않아 촉각 파지가 실패할 수 있다. 학습 코드 공개만으로는 이 차이를 알 수 없다. 시행 기록이 그날의 보정·하드웨어 상태를 체크포인트와 명령 스트림으로 연결해야 한다.

보고한 시행마다 설정 스냅샷과 원본 로그를 연결하고 결과를 만든 분석 명령을 보존한다. 제외 이유도 남겨 다른 독자가 분모를 복원하게 한다. 리셋 절차도 기록한다. 정성껏 준비한 시작 자세가 핵심 실험 조건일 수 있다.

**여기서 얻는 독법.** 결과 하나를 골라 실제 시도까지의 전체 경로를 복원할 수 있는지 묻는다. 빠진 항목은 코드가 공개됐다는 일반 문구보다 재현성 한계를 정확히 알려 준다.

### 8. 설계 예제

주장: 촉각 센싱이 삽입 회복을 개선한다. 같은 로봇, 제어기, 시연, 물체, 초기 오프셋,
실패 교란을 쓰라. vision-only와 vision+tactile을 무작위 짝지은 시행으로 비교하라. 삽입
성공, 최대 힘, 회복 시간, 손상, 개입, 지연, 실패 분류를 held-out 공차/재료에 걸쳐
보고하라.

이 선택들 중 무엇을 할지는 [[06-research-practice/research-questions-claims|연구 질문 §7]]의 주장–증거 표가 결판내며, 그 표는 어떤 실행보다 먼저 채운다. [[06-research-practice/research-questions-claims|연구 질문 §1]]의 마찰 질문을 끝까지 설계하자. 불확실성은 접촉 중 μ 추정이 잘못된 마찰 가정 때문에 잃은 파지 성공을 회복하는가다. 이점이 이미 관찰됐다는 보고가 아니라 제안 실험이다.

개입은 주어진 촉각 스트림으로 마찰 갱신을 켜는 것이다. 비교 대상은 고정 μ를 쓰는 같은 계획기다. 파지 후보, 시연, 제어 인터페이스, 센싱 기회를 대등하게 유지한다. 기준 마찰을 아는 조건은 특권 정보를 표시하면 개선 여지를 진단할 수 있다. 똑같이 배포 가능한 정책으로 제시하지 않는다.

시행을 세기 전에 단위를 정한다. 물체와 독립적으로 준비한 표면 조건은 물리적 변동의 주장을 지지한다. 학습 시드는 최적화 변동을 다룬다. 같은 물체·조건의 시도는 반복 관측이다. 센서 프레임을 독립 증거로 세지 말고 군집을 남긴다. 전이 주장에 필요한 표면 조건은 튜닝에서 제외한다.

짝지은 조건 안에서 방법 순서를 무작위화하거나 균형 배치한다. 표면 준비, 접촉 시점, 파지 실패, 운전자 정지, 리셋을 기록한다. 개입이 자율 시도를 끝내는지 미리 선언한다. 그렇지 않으면 한 방법이 더 많은 구조를 받고도 더 좋은 결정을 한 것처럼 보인다.

표본 수는 필요한 정밀도와 주장에 맞춰 정하고 §4의 도구를 계획 지침으로 쓴다. 편한 시행 수를 고른 뒤 신뢰성을 선언하지 않는다. 희귀 실패의 노출 논증은 평균 성능 비교와 다르다. 적절한 구간을 쓰고 분석에서 군집 구조를 보존한다.

조건별 성공과 불확실성, 회복 행동, 추정 시점, 실패 분류를 보고한다. 불필요한 보정의 비용과 연산 지연도 포함한다. 갱신이 결정적 접촉 뒤에 도착한다는 결과는 성공률 개선이 없어도 유용한 센싱 경계다. 최종 주장은 이 기전 증거와 건설 과제 전반의 전이 질문을 구분해야 한다.

### 읽고 나면 말할 수 있어야 하는 것

- 변수와 진짜 실험 단위를 식별할 수 있다
- 짝지은 베이스라인을 설계하고 oracle 정보를 표시할 수 있다
- 로봇 데이터셋의 시간·장면 누출을 탐지할 수 있다
- 물리적 변동에 맞는 시행 수와 불확실성을 고를 수 있다
- 하드웨어·소프트웨어 조건을 재구성하는 데 필요한 산출물을 명시할 수 있다

### 스스로 점검

1. 한 실행의 비디오 프레임 10,000장이 10,000 시행이 아닌 이유는?
2. 짝지은 설계는 언제 유용한가?
3. 추가 데이터로 사전학습된 모델을 공개 없이 scratch 베이스라인과 비교하면 무엇이 불공정한가?
4. 코드 공유만으로 로봇 실험이 재현되지 않는 이유는?

> [!tip]- 정답 · Answers
> 1. 프레임들이 같은 장면, 상태 궤적, 보정, 실패 사건을 공유한다.
> 2. 두 방법이 같은 과제/장면/참가자를 마주할 수 있어 방해 변동이 줄어들 때.
> 3. 구조와 데이터·사전학습이 교란(confound)된다.
> 4. 하드웨어, 보정, 타이밍, 제어, 재료, 설정, 절차도 결과를 결정한다.

### 출처

- [National Academies — *Reproducibility and Replicability in Science* (2019)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science) — 기념비적 보고서; 단 본문에 제시한 ACM식 관례와 용어 구분이 다르다(reproducibility = 같은 데이터·같은 계산, replicability = 새 데이터)
- [Artifact Evaluation (artifact-eval.org)](https://www.artifact-eval.org/) — 독립 artifact 리뷰어가 실제로 확인하는 것
- [Sandve et al., *Ten Simple Rules for Reproducible Computational Research* (PLOS Comp Biol 2013)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
