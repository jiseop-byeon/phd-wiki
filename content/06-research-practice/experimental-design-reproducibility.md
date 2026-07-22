---
title: 2. Experimental Design & Reproducibility
tags: [research, experiments, reproducibility]
---

## English

An experiment should distinguish the proposed explanation from plausible alternatives. In robotics, this requires controlling not only models and datasets but scenes, hardware, calibration, operators, resets, timing, and exposure to failures.

> [!note] Prerequisite
> Read [[02-foundations/ml-practice|ML Practice & Evaluation]] first. That page teaches how to read results; this page focuses on designing evidence.

### 1. Variables and units of analysis

- **Independent variable:** factor intentionally changed.
- **Dependent variable:** measured outcome.
- **Control variables:** conditions held fixed or modeled.
- **Experimental unit:** independent entity assigned to a condition—seed, scene, object, participant, robot, or site.

Repeated frames from one robot run are not thousands of independent trials.

### 2. Comparisons

A strong baseline isolates the proposed contribution. Include a practical existing system, a simpler method, and when useful an **oracle** that uses unavailable information to estimate an upper bound. The oracle must be labeled; it is not a deployable competitor.

Use paired comparisons when the same scenes/tasks can be evaluated under both conditions. Randomize or counterbalance order to reduce learning, battery, wear, weather, and operator effects.

### 3. Variation and splits

Separate training/tuning/test data and document the unit of split. Random frames from the same trajectory leak scene, object, and temporal information. Test across relevant variation: tasks, layouts, materials, lighting/weather, hardware, operators, speed, and failure perturbations.

### 4. Trials and uncertainty

Report trial count, independent runs, failures, exclusions, aggregation, and an uncertainty measure appropriate to the design. A seed captures only software randomness; physical trials vary through calibration, wear, temperature, material, timing, and people.

Predeclare primary outcomes when many metrics and conditions make cherry-picking likely. Statistical significance and practical importance are different.

### 5. Ablations and budgets

An ablation may remove or change architecture, objective, data, sensing, controller, or hyperparameter. Hold the rest constant enough to isolate interpretation. Compare data, compute, tuning effort, pretrained assets, sensors, and control interface—not architecture names alone.

### 6. Reproducibility vocabulary

Terminology differs across communities, so define it. A useful convention is:

- **Repeatability:** same team, setup, and procedure obtains compatible results.
- **Reproducibility:** independent team uses provided artifacts/procedure and obtains compatible results.
- **Replicability:** independent implementation or study tests the same claim.

### 7. Artifact checklist

Record code commit, dependencies/container, model and data versions, splits, seeds, training commands, configurations, calibration, frame conventions, controller gains, firmware, hardware revision, trial protocol, raw logs, exclusions, and analysis scripts. Provide enough detail to reconstruct what physically happened.

### 8. Worked design

Claim: tactile sensing improves insertion recovery. Use the same robot, controller, demonstrations, objects, initial offsets, and failure perturbations. Compare vision-only and vision+tactile in randomized paired trials. Report insertion success, peak force, recovery time, damage, interventions, latency, and failure taxonomy across held-out clearances/materials.

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

- [National Academies — *Reproducibility and Replicability in Science* (2019)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science) — the report that anchors the reproducibility vocabulary
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

### 2. 비교

강한 베이스라인은 제안된 기여를 분리한다. 실용적인 기존 시스템, 더 단순한 방법,
필요하면 사용할 수 없는 정보로 상한을 추정하는 **oracle**을 포함하라. Oracle은 표시돼야
하며 배포 가능한 경쟁자가 아니다.

같은 장면/과제를 두 조건에서 평가할 수 있으면 짝지은 비교를 써라. 학습·배터리·마모·
날씨·운용자 효과를 줄이도록 순서를 무작위화하거나 counterbalance하라.

### 3. 변동과 분할

학습/튜닝/시험 데이터를 분리하고 분할의 단위를 문서화하라. 같은 궤적의 무작위 프레임은
장면·물체·시간 정보를 누출한다. 관련 변동 전반 — 과제, 배치, 재료, 조명/날씨, 하드웨어,
운용자, 속도, 실패 교란 — 에 걸쳐 시험하라.

### 4. 시행 수와 불확실성

시행 수, 독립 실행, 실패, 제외, 집계 방식, 설계에 맞는 불확실성 지표를 보고하라. 시드는
소프트웨어 무작위성만 잡는다; 물리 시행은 보정, 마모, 온도, 재료, 타이밍, 사람을 통해
변한다.

지표와 조건이 많아 체리피킹이 쉬울 때는 주요 결과(primary outcome)를 미리 선언하라.
통계적 유의성과 실질적 중요성은 다르다.

### 5. 절제와 예산

절제는 구조, 목적함수, 데이터, 센싱, 제어기, 하이퍼파라미터를 제거하거나 바꿀 수 있다.
해석을 분리할 만큼 나머지를 고정하라. 구조 이름만이 아니라 데이터, 컴퓨트, 튜닝 노력,
사전학습 자산, 센서, 제어 인터페이스를 비교하라.

### 6. 재현성 어휘

용어가 커뮤니티마다 다르므로 정의하고 써라. 유용한 관례:

- **Repeatability:** 같은 팀·장비·절차로 양립 가능한 결과를 얻는다.
- **Reproducibility:** 독립 팀이 제공된 산출물·절차로 양립 가능한 결과를 얻는다.
- **Replicability:** 독립 구현·연구가 같은 주장을 시험한다.

### 7. 산출물 체크리스트

코드 커밋, 의존성/컨테이너, 모델·데이터 버전, 분할, 시드, 학습 명령, 설정, 보정, 프레임
관례, 제어기 이득, 펌웨어, 하드웨어 리비전, 시행 프로토콜, 원시 로그, 제외, 분석
스크립트를 기록하라. 물리적으로 무슨 일이 있었는지 재구성할 수 있을 만큼 상세해야 한다.

### 8. 설계 예제

주장: 촉각 센싱이 삽입 회복을 개선한다. 같은 로봇, 제어기, 시연, 물체, 초기 오프셋,
실패 교란을 쓰라. vision-only와 vision+tactile을 무작위 짝지은 시행으로 비교하라. 삽입
성공, 최대 힘, 회복 시간, 손상, 개입, 지연, 실패 분류를 held-out 공차/재료에 걸쳐
보고하라.

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

- [National Academies — *Reproducibility and Replicability in Science* (2019)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science) — 재현성 어휘의 기준이 되는 보고서
- [Artifact Evaluation (artifact-eval.org)](https://www.artifact-eval.org/) — 독립 artifact 리뷰어가 실제로 확인하는 것
- [Sandve et al., *Ten Simple Rules for Reproducible Computational Research* (PLOS Comp Biol 2013)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
