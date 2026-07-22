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

## 한국어

실험은 제안한 설명과 가능한 대안을 구분해야 한다. 로봇에서는 model·dataset뿐 아니라 scene, hardware, calibration, operator, reset, timing과 failure exposure까지 설계 대상이다.

Independent/dependent/control variable과 진짜 experimental unit을 정의하라. 한 trajectory의 수천 frame은 독립 trial 수천 개가 아니다. Baseline은 practical system, simpler method, 필요하면 oracle을 포함하되 oracle 정보가 배포 불가능함을 표시한다. 같은 task를 두 방법에 적용할 수 있으면 paired comparison과 순서 randomization을 고려한다.

Repeatability·reproducibility·replicability는 커뮤니티마다 용법이 다르므로 논문에서 정의한다. Code뿐 아니라 data split, configuration, calibration, frame, controller, firmware, hardware, raw log와 exclusion까지 남겨야 physical experiment를 재구성할 수 있다.
