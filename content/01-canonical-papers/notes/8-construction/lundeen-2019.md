---
title: "Geometrically Adaptive Robotized Construction Work (Lundeen et al., 2019)"
authors: Kurt M. Lundeen, Vineet R. Kamat, Carol C. Menassa, Wes McGee
affiliation: University of Michigan
venue: Automation in Construction
year: 2019
pdf: https://doi.org/10.1016/j.autcon.2018.12.020
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Lundeen et al.**, "Autonomous motion planning and task execution in geometrically adaptive robotized construction work," *Automation in Construction* 2019 — [DOI](https://doi.org/10.1016/j.autcon.2018.12.020)

> [!note] Math on-ramp · 수학 준비물
> [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]] and [[04-robotics/planning-decision-making|4. Planning §7]] (replanning). The claim is adaptation to *as-built* rather than as-designed geometry — a sensing-and-replanning loop, so check both halves.
> [[04-robotics/geometric-perception-calibration|3.5 기하 인식]]과 [[04-robotics/planning-decision-making|4. 계획 §7]](replanning). 주장은 설계도가 아니라 *실제 시공된* 형상에 적응한다는 것 — 감지와 재계획의 루프이므로 양쪽 절반을 모두 확인하라.

## English

**One-line summary**: A construction manipulator senses as-built geometry and adapts its motion plan and task execution on the fly — the paper that operationalizes construction's core difference from factory automation: the workpiece never matches the drawing.

> [!tip] Key intuition · 핵심 직관
> Measuring as-built geometry reveals the mismatch that a fixed design-based path would ignore. Updating the plan from that observation makes execution respond to the encountered instance, with adaptation bounded by the engineered task and sensing model.

**Why read it**: it is the middle step of the Michigan line. [[vision-guided-assembly|Feng 2015]] showed marker-based vision guidance; Lundeen replaces "detect a fiducial" with "sense the actual as-built geometry and re-plan," so the robot handles per-instance variability autonomously instead of replaying fixed trajectories; [[liang-lfd|Liang 2020]] then replaces the remaining task scripting with human demonstration. Evidence is lab-testbed demonstration of sensor-driven adaptive execution — a **testbed, not a site** — with autonomy at the task-execution level inside a structured experiment.

**Critique through this wiki's lens**: the adaptation is model-based and sensor-driven, not learned — every new task class still needs engineering. That is precisely the gap the next step in the line (demonstration, then hierarchical imitation) exists to close.

**Limitations.** Adaptation is bounded by the engineered task model and sensed geometry in a testbed. It does not establish new-task learning or reliability under the full variation of active construction work.

> [!question] Reading the claim · 핵심 주장 읽는 법
> Adaptive execution means responding to sensed geometry in the tested task model. It does not imply learning a new trade or general deployment on an active site. Check what geometric variation was handled and which task logic remained engineered.

## 한국어

**한 줄 요약**: 건설 매니퓰레이터가 준공(as-built) 기하를 감지해 모션 계획과 과제 실행을 즉석에서 적응시킨다 — 건설이 공장 자동화와 다른 핵심, 즉 "작업 대상은 도면과 결코 일치하지 않는다"를 실제로 구현한 논문.

> [!tip] 핵심 직관 · Key intuition
> 시공 형상을 측정하면 고정 설계 경로가 놓칠 불일치가 드러난다. 그 관측으로 계획을 갱신해 마주친 개별 상황에 실행을 맞춘다. 적응 범위는 공학적으로 만든 과제·센싱 모델에 묶인다.

**읽는 이유**: 미시간 계열의 중간 단계다. [[vision-guided-assembly|Feng 2015]]가 마커 기반 비전 유도를 보였다면, Lundeen은 "마커를 검출한다"를 "실제 준공 기하를 감지하고 다시 계획한다"로 바꿔, 로봇이 고정 궤적을 재생하는 대신 개체별 변동을 자율적으로 처리하게 한다; 이어서 [[liang-lfd|Liang 2020]]이 남은 과제 스크립팅을 인간 시연으로 대체한다. 증거는 센서 기반 적응 실행의 실험실 테스트베드 시연 — **현장이 아니라 테스트베드** — 이고, 자율성은 구조화된 실험 안의 과제 실행 수준이다.

**이 위키의 렌즈로 본 비판**: 이 적응은 모델 기반·센서 기반이지 학습된 것이 아니다 — 새로운 과제 부류마다 여전히 엔지니어링이 필요하다. 바로 그 간극을 메우려고 계열의 다음 단계(시연, 그다음 계층적 모방)가 존재한다.

**한계.** 적응은 시험 환경의 공학적 과제 모델과 센싱 형상에 묶인다. 새 과제 학습이나 실제 시공 변동 전체의 신뢰성을 확립하지 않는다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 적응 실행은 시험한 과제 모델에서 센싱 형상에 반응한다는 뜻이다. 새로운 공종 학습이나 실제 현장의 일반 배포를 뜻하지 않는다. 처리한 형상 변동과 여전히 공학적으로 정한 과제 논리를 확인한다.

### 연결

- 이전: [[vision-guided-assembly|Feng 2015]] · 다음: [[liang-lfd|Liang 2020]] (미시간 계열: 비전 유도 → 기하 적응 → 시연 학습)

### 읽고 나면 말할 수 있어야 하는 것 · After reading (○)

- [ ] Explain why as-built geometric variability breaks pre-programmed automation · 준공 기하 변동성이 왜 사전 프로그래밍된 자동화를 깨뜨리는지 설명할 수 있다
- [ ] Describe the sense → replan → execute adaptation loop · 감지 → 재계획 → 실행의 적응 루프를 말할 수 있다
- [ ] State this paper's position in the Michigan line (Feng → Lundeen → Liang → Yu) · 미시간 계열(Feng → Lundeen → Liang → Yu)에서 이 논문의 위치를 말할 수 있다
