---
title: 11. Human–Robot Interaction & Safety
tags: [robotics, hri, safety, construction]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

When people operate, supervise, share space with, or depend on a robot, task success alone is not enough. Human–robot interaction studies authority, information, workload, trust, and performance; safety analysis asks which hazards can cause harm and how risk is reduced.

> [!info] Depth target
> Read HRI and safety claims — autonomy level, intervention, trust, hazard/risk — precisely, and audit human-study designs. Running human studies requires dedicated methods training beyond this page.

> [!warning] Scope
> This page is a literacy guide for reading research, not a certification or legal-compliance guide. Applicable laws and standards must be checked from current official sources for the specific machine, workplace, and jurisdiction.

> [!note] Prerequisites
> [[02-foundations/ml-practice|ML Practice & Evaluation]] · [[04-robotics/robot-systems-deployment|Robot Systems]] — §9 connects onward to [[05-construction-robotics/index|Construction Robotics]] (the next track, not a prerequisite).

### 1. Autonomy is a spectrum

| Mode | Human and robot roles |
|---|---|
| Direct teleoperation | human continuously commands motion |
| Assisted teleoperation | robot stabilizes, filters, or avoids constraints |
| Shared autonomy | authority is blended or allocated between human and autonomy |
| Supervisory control | human sets goals and monitors autonomous execution |
| Conditional autonomy | robot acts within a defined operating condition and requests help |
| Full autonomy | robot performs the scoped task without runtime intervention |

The label “autonomous” is incomplete without the task, operating domain, intervention policy, reset procedure, and fallback.

### 2. Human in, on, and out of the loop

- **In the loop:** human input is part of normal decision/action execution.
- **On the loop:** autonomy acts while a human supervises and may intervene.
- **Out of the loop:** no runtime human role within the stated scope.

Intervention, approval, takeover, teleoperation recovery, and physical reset are different. Papers should report which occurred and whether they count as failures.

### 3. Shared control and authority

Shared autonomy combines human command $u_h$ and autonomous command $u_r$ through arbitration, constraints, or role allocation. A simple blend $u=\alpha u_h+(1-\alpha)u_r$ illustrates the idea but can be unsafe or confusing if commands conflict. Check how intent is inferred, authority changes, conflict is communicated, and the human can override.

### 4. Human performance

Relevant constructs include workload, situation awareness, attention, reaction time, fatigue, skill, mental model, and trust. High trust is not automatically good: **calibrated trust** means reliance matches system capability and uncertainty. Self-reported trust should be paired with behavior and task outcomes.

### 5. Interfaces

Visual, audio, haptic, and physical interfaces can show state, intent, uncertainty, warnings, and required action. “Intuitive,” “transparent,” or “natural” are claims requiring measurements. More alarms can reduce safety through alarm fatigue; more explanations can increase workload.

### 6. Safety vocabulary

| Term | Meaning |
|---|---|
| Hazard | potential source or situation of harm |
| Risk | combination of likelihood/exposure and consequence under a method |
| Safety constraint/envelope | boundary intended to keep operation within acceptable conditions |
| Safe stop | controlled transition intended to reduce risk |
| Emergency stop | dedicated means for urgent hazardous-motion stopping |
| Fail-safe | failure leads toward a lower-risk state |
| Fail-operational | selected function continues despite specified failures |
| Near miss | event without harm that could plausibly have produced it |

No learned policy is “safe” merely because it had zero collisions in a small test. Safety is a system property involving sensing, control, hardware, people, environment, procedures, and evidence.

### 7. Human-study design

Within-subject studies compare conditions on the same participant; between-subject studies assign different participants. Counterbalancing helps separate condition effects from practice, fatigue, and order effects. Report participant population, expertise, sample size, exclusions, task realism, objective and subjective measures, and appropriate ethics/IRB review.

### 8. Evaluation

Measure task quality/time, intervention and reset rate, takeover time, workload, situation awareness, trust calibration, safety violations, near misses, productivity, usability, and learning/fatigue. A lower intervention rate may mean better autonomy—or reluctant, overloaded, or poorly informed operators.

### 9. Construction and field context

Heavy machinery adds blind spots, momentum, noise, dust, vibration, PPE, remote operation, spotters, mixed work zones, trained operators, workflow constraints, and consequential failure. State who holds responsibility, who can stop the machine, and how communication works during degraded operation.

### 10. Worked interpretation

An automated excavator receives a goal from an operator, plans and executes a digging cycle, and allows override. This is supervisory or shared autonomy depending on continuous authority—not simply “fully autonomous.” Evaluation should report overrides, planner/controller failures, unsafe approaches, productivity, operator workload, and the operating conditions in which autonomy was enabled.

### After reading

- Describe autonomy using task, domain, intervention, and reset—not one adjective.
- Distinguish human-in/on/out-of-the-loop roles.
- Explain authority allocation and override in shared control.
- Distinguish hazard, risk, fail-safe, and fail-operational.
- Audit human-study population, order effects, and ecological validity.
- Interpret safety and trust claims from measured evidence.

### Self-check

1. Why is “zero collisions in 20 trials” insufficient evidence of safety?
2. When might fewer interventions indicate worse HRI?
3. Why should experienced operators and general participants not be pooled casually?
4. What information is missing from the phrase “fully autonomous construction robot”?

> [!tip]- Answers
> 1. The exposure is small and may omit rare hazards, distribution shift, severity, and system failures. 2. The operator may miss hazards, distrust the interface, be overloaded, or lack authority. 3. Skill, mental models, speed, workload, and risk response differ. 4. Task, operating domain, human role, intervention/reset, safety fallback, duration, and failure handling.

### Sources

- [NIST Human-Robot Interaction](https://www.nist.gov/topics/human-robot-interaction)
- [NIST Robotics Test Methods](https://www.nist.gov/programs-projects/robotic-systems-smart-manufacturing-program)
- [ACM/IEEE International Conference on Human-Robot Interaction (HRI)](https://humanrobotinteraction.org/) — the field's flagship venue; its papers set the de facto standard for human-study design

## 한국어

사람이 로봇을 조작·감독하거나, 공간을 공유하거나, 로봇에 의존할 때 과제 성공만으로는
부족하다. 인간-로봇 상호작용(HRI)은 권한, 정보, 작업 부하, 신뢰, 성능을 연구하고, 안전
분석은 어떤 위험 요인이 해를 낳을 수 있고 위험을 어떻게 줄이는지 묻는다.

> [!info] 깊이 목표
> HRI·안전 주장 — 자율성 수준, 개입, 신뢰, hazard/risk — 을 정확히 읽고 인간 대상 연구
> 설계를 검사한다. 인간 대상 연구를 직접 수행하려면 이 페이지 너머의 전문 방법론 훈련이
> 필요하다.

> [!warning] 범위
> 이 페이지는 연구를 읽기 위한 문해력 가이드이지 인증·법규 준수 가이드가 아니다. 해당
> 기계·작업장·관할권에 적용되는 법과 표준은 최신 공식 출처에서 확인해야 한다.

> [!note] 선수 지식
> [[02-foundations/ml-practice|ML 실무와 평가]] · [[04-robotics/robot-systems-deployment|로봇 시스템]] — §9는 [[05-construction-robotics/index|건설로봇]](다음 트랙, 선수 지식 아님)으로 이어진다.

### 1. 자율성은 스펙트럼이다

| 모드 | 사람과 로봇의 역할 |
|---|---|
| 직접 원격조작 | 사람이 운동을 연속적으로 명령 |
| 보조 원격조작 | 로봇이 안정화·필터링·제약 회피를 수행 |
| 공유 자율성 | 권한이 사람과 자율성 사이에 혼합·배분됨 |
| 감독 제어 | 사람이 목표를 정하고 자율 실행을 감시 |
| 조건부 자율성 | 정의된 운용 조건 안에서 행동하고 도움을 요청 |
| 완전 자율성 | 범위가 정해진 과제를 런타임 개입 없이 수행 |

"autonomous"라는 라벨은 과제, 운용 도메인, 개입 정책, 리셋 절차, 폴백 없이는 불완전하다.

### 2. Human in / on / out of the loop

- **In the loop:** 사람 입력이 정상적 결정·행동 실행의 일부다.
- **On the loop:** 자율성이 행동하고 사람은 감독하며 개입할 수 있다.
- **Out of the loop:** 명시된 범위 안에서 런타임 인간 역할이 없다.

개입, 승인, 인수(takeover), 원격조작 회복, 물리적 리셋은 서로 다르다. 논문은 무엇이
일어났고 그것이 실패로 집계되는지 보고해야 한다.

### 3. 공유 제어와 권한

공유 자율성은 사람 명령 $u_h$와 자율 명령 $u_r$을 중재(arbitration), 제약, 역할 배분으로
결합한다. 단순 혼합 $u=\alpha u_h+(1-\alpha)u_r$은 아이디어를 보여 주지만 두 명령이
충돌하면 위험하거나 혼란스러울 수 있다. 의도를 어떻게 추론하고, 권한이 어떻게 바뀌고,
충돌이 어떻게 전달되고, 사람이 어떻게 override하는지 확인하라.

### 4. 인간 성능

작업 부하, 상황 인식, 주의, 반응 시간, 피로, 숙련, 멘탈 모델, 신뢰가 관련 구성 개념이다.
높은 신뢰가 자동으로 좋은 것이 아니다: **보정된 신뢰(calibrated trust)**란 의존이 시스템의
능력과 불확실성에 맞는 상태다. 자기 보고 신뢰는 행동·과제 결과와 짝지어 읽어야 한다.

### 5. 인터페이스

시각·청각·햅틱·물리 인터페이스는 상태, 의도, 불확실성, 경고, 요구 행동을 보여 줄 수
있다. "Intuitive", "transparent", "natural"은 측정을 요구하는 주장이다. 경보가 많으면
경보 피로로 오히려 안전이 떨어질 수 있고, 설명이 많으면 작업 부하가 늘 수 있다.

### 6. 안전 어휘

| 용어 | 의미 |
|---|---|
| Hazard | 잠재적 해의 원천·상황 |
| Risk | 정해진 방법 아래 가능성/노출과 결과의 결합 |
| 안전 제약/엔벨로프 | 허용 조건 안에 운용을 유지하려는 경계 |
| Safe stop | 위험을 낮추려는 통제된 전이 |
| 비상 정지 | 긴급한 위험 운동 정지를 위한 전용 수단 |
| Fail-safe | 실패가 더 낮은 위험 상태로 이어짐 |
| Fail-operational | 명시된 실패에도 선택 기능이 지속 |
| Near miss | 해는 없었지만 그럴듯하게 해를 낳을 수 있었던 사건 |

작은 시험에서 충돌이 없었다는 이유만으로 학습 정책이 "안전"한 것은 아니다. 안전은 센싱,
제어, 하드웨어, 사람, 환경, 절차, 증거가 얽힌 시스템 속성이다.

### 7. 인간 대상 연구 설계

Within-subject 연구는 같은 참가자에게 조건들을 비교하고, between-subject 연구는 참가자를
나눠 배정한다. Counterbalancing은 조건 효과를 연습·피로·순서 효과와 분리하는 데 돕는다.
참가자 모집단, 전문성, 표본 크기, 제외, 과제 현실성, 객관·주관 지표, 적절한 윤리/IRB
심의를 보고하라.

### 8. 평가

과제 품질/시간, 개입·리셋 빈도, 인수 시간, 작업 부하, 상황 인식, 신뢰 보정, 안전 위반,
near miss, 생산성, 사용성, 학습·피로 효과를 재라. 낮은 개입률은 더 나은 자율성을 뜻할
수도 있고 — 꺼리거나, 과부하거나, 정보가 부족한 운용자를 뜻할 수도 있다.

### 9. 건설·현장 맥락

중장비는 사각지대, 관성, 소음, 먼지, 진동, PPE, 원격 운용, 신호수(spotter), 혼재 작업
구역, 숙련 운용자, 공정 제약, 결과가 무거운 실패를 더한다. 책임이 누구에게 있고, 누가
기계를 멈출 수 있고, 성능 저하 운용 중 소통이 어떻게 되는지를 명시하라.

### 10. 해석 예제

자동화 굴착기가 운용자에게서 목표를 받아 굴착 사이클을 계획·실행하고 override를
허용한다. 이는 연속적 권한 여부에 따라 감독 제어 또는 공유 자율성이다 — 단순히 "완전
자율"이 아니다. 평가는 override, 플래너/제어기 실패, 위험 접근, 생산성, 운용자 작업
부하, 그리고 자율성이 켜져 있던 운용 조건을 보고해야 한다.

### 읽고 나면 말할 수 있어야 하는 것

- 자율성을 형용사 하나가 아니라 과제·도메인·개입·리셋으로 기술할 수 있다
- human-in/on/out-of-the-loop 역할을 구분할 수 있다
- 공유 제어의 권한 배분과 override를 설명할 수 있다
- hazard·risk·fail-safe·fail-operational을 구분할 수 있다
- 인간 연구의 모집단·순서 효과·생태적 타당성을 검사할 수 있다
- 안전·신뢰 주장을 측정된 증거로부터 해석할 수 있다

### 스스로 점검

1. "20회 시행에서 충돌 0"이 안전의 증거로 불충분한 이유는?
2. 개입이 적은 것이 오히려 나쁜 HRI를 나타낼 수 있는 경우는?
3. 숙련 운용자와 일반 참가자를 함부로 합치면 안 되는 이유는?
4. "완전 자율 건설로봇"이라는 문구에 빠진 정보는?

> [!tip]- 정답 · Answers
> 1. 노출이 작고 희귀 위험, 분포 이동, 심각도, 시스템 실패를 놓칠 수 있다.
> 2. 운용자가 위험을 놓치거나, 인터페이스를 불신하거나, 과부하이거나, 권한이 없을 때.
> 3. 숙련, 멘탈 모델, 속도, 작업 부하, 위험 반응이 다르다.
> 4. 과제, 운용 도메인, 인간 역할, 개입/리셋, 안전 폴백, 지속 시간, 실패 처리.

### 출처

- [NIST Human-Robot Interaction](https://www.nist.gov/topics/human-robot-interaction)
- [NIST Robotics Test Methods](https://www.nist.gov/programs-projects/robotic-systems-smart-manufacturing-program)
- [ACM/IEEE International Conference on Human-Robot Interaction (HRI)](https://humanrobotinteraction.org/) — 분야 대표 학회; 인간 대상 연구 설계의 실제 기준을 보여주는 논문들
