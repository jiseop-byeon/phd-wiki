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



<svg viewBox="0 0 620 234" style="max-width:100%;height:auto" role="img" aria-label="the autonomy spectrum drawn as the human's shrinking share of moment-to-moment decisions">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="150" y1="26" x2="150" y2="196"/><line x1="430" y1="26" x2="430" y2="196"/></g>
  <rect x="150" y="29" width="269.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="42" font-size="10.5" fill="currentColor" text-anchor="end">Direct teleoperation</text>
  <rect x="150" y="56" width="218.1" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="69" font-size="10.5" fill="currentColor" text-anchor="end">Assisted teleoperation</text>
  <rect x="150" y="83" width="166.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="96" font-size="10.5" fill="currentColor" text-anchor="end">Shared autonomy</text>
  <rect x="150" y="110" width="115.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="123" font-size="10.5" fill="currentColor" text-anchor="end">Supervisory control</text>
  <rect x="150" y="137" width="63.5" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="150" font-size="10.5" fill="currentColor" text-anchor="end">Conditional autonomy</text>
  <rect x="150" y="164" width="12.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="177" font-size="10.5" fill="currentColor" text-anchor="end">Full autonomy</text>
  <g font-size="10.5" fill="currentColor">
    <text x="152" y="20">human&#39;s share of the moment-to-moment decisions &#8594;</text><text x="456" y="20">&#8592; robot&#39;s share</text>
    <text x="20" y="210" opacity="0.9">The bar is the human's share. No rung is &#8220;autonomous&#8221; by itself &#8212;</text>
    <text x="20" y="224" opacity="0.9">name the task, the domain, who may intervene, and who resets.</text>
  </g>
</svg>



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

**The standards a paper will cite.** Safety sections quote standard numbers as shorthand, and
the shorthand carries the actual claim. You are reading them, not certifying against them —
but you cannot check a safety claim without knowing which document defines the term.

| Standard | Covers | What it gives a reader |
|---|---|---|
| **ISO 10218-1 / -2** | industrial robots (part 1: the robot; part 2: the system/cell) | the base requirements; **revised in 2025**, first update since 2011 |
| **ISO/TS 15066:2016** | collaborative applications, biomechanical limits | the origin of PFL thresholds — but see the warning below |
| **ISO 13482:2014** | personal care robots | the standard for service robots in physical contact with people |
| **ISO 3691-4** | driverless industrial trucks — AGVs and AMRs | the mobile-base standard; a wheeled site robot is read against this, not 10218 |

> [!warning] ISO/TS 15066 no longer stands alone — and most papers predate that
> ISO 10218-1:2025 and ISO 10218-2:2025 came into force **1 April 2025** and folded the
> collaborative-application and power-and-force-limiting requirements of ISO/TS 15066:2016
> **into the 10218 series**. The revision also drops the terms *collaborative robot* and
> *collaborative operation* in favour of **collaborative application** — the argument being
> that only a use of a robot, not a robot by itself, can be designed and verified as
> collaborative.
> A paper written before 2025 that cites "ISO/TS 15066" is citing the document that was
> current when it was written; that is correct practice and not an error. **What is an error
> is repeating it now as the live authority**, or calling a machine "a 15066-compliant
> cobot" — under the current wording compliance is a property of the application, not of the
> arm you bought.

**The four methods of safe interaction**, named the same way across the series, are the
vocabulary every pHRI paper's safety paragraph is written in:

| Method | The mechanism | What it costs |
|---|---|---|
| Safety-rated monitored stop | robot halts while a person is in the shared space; motion resumes when they leave | throughput — no concurrent work |
| Hand guiding | the operator moves the robot through a hand-operated device | requires the human at the robot |
| **Speed and separation monitoring (SSM)** | keep a *protective separation distance*; slow or stop as it closes | needs reliable person tracking |
| **Power and force limiting (PFL)** | contact is permitted, bounded by force/pressure limits per body region | caps speed and payload by design |

The two that generate research are the last two, and they fail differently. SSM's separation
distance is a **sum**, not a threshold: how far the human travels while you react, plus how
far the robot travels before it begins stopping, plus its stopping distance, plus the
uncertainty of both position estimates. Every learned-perception paper that claims to enable
SSM is making a claim about the *uncertainty* terms, and a detector's latency enters the
distance directly. PFL's limits are **per body region** — the tolerable force and pressure on
a hand differ from those on a face — so "under the force limit" is meaningless without saying
which region and which contact type (transient vs quasi-static) was assumed.

For construction, note which standard applies to what: a tracked or wheeled base moving on
site is read against **ISO 3691-4**, an arm working next to a person against **ISO 10218**,
and neither was written for an outdoor, unfenced, weather-exposed site with a changing
layout. That gap is a legitimate thing to say in a paper — but say it against the named
standard, not against "safety" in general.

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
> 1. The exposure is small and may omit rare hazards, distribution shift, severity, and system failures. Put a number on it: by the rule of three ([[06-research-practice/experimental-design-reproducibility|Experimental Design §4]]), zero failures in 20 trials is still consistent with a true failure rate as high as $3/20 = 15\%$ — one collision every seven runs. 2. The operator may miss hazards, distrust the interface, be overloaded, or lack authority. 3. Skill, mental models, speed, workload, and risk response differ. 4. Task, operating domain, human role, intervention/reset, safety fallback, duration, and failure handling.

### Sources


- The perception layer these decisions run on: [[04-robotics/video-action-understanding|20. Video & Action Understanding]], [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]], [[04-robotics/egocentric-perception|22. Egocentric Perception]], [[04-robotics/human-intent-prediction|23. Human Intent & Trajectory Prediction]] — autonomy and authority are decisions; those pages are what the decision is made from.
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

<svg viewBox="0 0 620 234" style="max-width:100%;height:auto" role="img" aria-label="순간순간의 결정에서 사람의 몫이 줄어드는 것으로 그린 자율성 스펙트럼">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="150" y1="26" x2="150" y2="196"/><line x1="430" y1="26" x2="430" y2="196"/></g>
  <rect x="150" y="29" width="269.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="42" font-size="10.5" fill="currentColor" text-anchor="end">직접 원격조작</text>
  <rect x="150" y="56" width="218.1" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="69" font-size="10.5" fill="currentColor" text-anchor="end">보조 원격조작</text>
  <rect x="150" y="83" width="166.6" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="96" font-size="10.5" fill="currentColor" text-anchor="end">공유 자율</text>
  <rect x="150" y="110" width="115.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="123" font-size="10.5" fill="currentColor" text-anchor="end">감독 제어</text>
  <rect x="150" y="137" width="63.5" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="150" font-size="10.5" fill="currentColor" text-anchor="end">조건부 자율</text>
  <rect x="150" y="164" width="12.0" height="18" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.9"/>
  <text x="144" y="177" font-size="10.5" fill="currentColor" text-anchor="end">완전 자율</text>
  <g font-size="10.5" fill="currentColor">
    <text x="152" y="20">순간순간의 결정 중 사람의 몫 &#8594;</text><text x="456" y="20">&#8592; 로봇의 몫</text>
    <text x="20" y="210" opacity="0.9">막대는 사람의 몫이다. 어느 단도 그 자체로 &#8220;자율&#8221;이 아니다 &#8212;</text>
    <text x="20" y="224" opacity="0.9">과제·영역·개입 권한·리셋 주체를 함께 말해야 한다.</text>
  </g>
</svg>



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
높은 신뢰가 자동으로 좋은 것이 아니다: **보정된 신뢰**(calibrated trust)란 의존이 시스템의
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

**논문이 인용할 표준들.** 안전 절은 표준 번호를 약칭처럼 인용하고, 그 약칭이 실제 주장을
지고 있다. 우리는 인증하는 것이 아니라 읽는 것이지만, 어느 문서가 그 용어를 정의하는지
모르면 안전 주장을 검증할 수 없다.

| 표준 | 대상 | 읽는 사람에게 주는 것 |
|---|---|---|
| **ISO 10218-1 / -2** | 산업용 로봇(1부: 로봇, 2부: 시스템·셀) | 기본 요구사항. **2025년 개정**, 2011년 이후 첫 갱신 |
| **ISO/TS 15066:2016** | 협동 응용, 생체역학 한계 | PFL 임계값의 출처 — 다만 아래 경고를 보라 |
| **ISO 13482:2014** | 개인 돌봄 로봇 | 사람과 물리적으로 접촉하는 서비스 로봇의 표준 |
| **ISO 3691-4** | 무인 산업 차량 — AGV·AMR | 이동 베이스의 표준. 바퀴형 현장 로봇은 10218이 아니라 이쪽으로 읽는다 |

> [!warning] ISO/TS 15066은 더 이상 단독으로 존재하지 않는다 — 그리고 대부분의 논문은 그 이전이다
> ISO 10218-1:2025와 ISO 10218-2:2025가 **2025년 4월 1일** 발효되면서 ISO/TS 15066:2016의
> 협동 응용·역량 제한(PFL) 요구사항을 **10218 시리즈 안으로 흡수했다.** 개정판은 *협동 로봇*과
> *협동 운전*이라는 용어도 버리고 **협동 응용**(collaborative application)을 쓴다 — 로봇 자체가
> 아니라 로봇의 사용만이 협동적이라고 설계·검증될 수 있다는 논거다.
> 2025년 이전에 쓰인 논문이 "ISO/TS 15066"을 인용하는 것은 당시의 현행 문서를 인용한 것이고
> 올바른 관행이지 오류가 아니다. **오류는 그것을 지금도 살아 있는 권위로 되풀이하는 것**,
> 또는 어떤 기계를 "15066 준수 협동로봇"이라 부르는 것이다 — 현재 표현으로 준수는 사놓은 팔이
> 아니라 응용의 성질이다.

**안전한 상호작용의 네 가지 방법**은 시리즈 전체에서 같은 이름으로 불리며, 모든 pHRI 논문의
안전 문단이 쓰이는 어휘다:

| 방법 | 기구 | 대가 |
|---|---|---|
| 안전 정격 감시 정지 | 사람이 공유 공간에 있는 동안 로봇이 멈추고, 나가면 재개 | 처리량 — 동시 작업이 불가능 |
| Hand guiding | 조작자가 손으로 조작하는 장치로 로봇을 움직인다 | 사람이 로봇 옆에 있어야 함 |
| **속도·이격 감시(SSM)** | *보호 이격 거리*를 유지하고, 거리가 좁혀지면 감속·정지 | 신뢰할 수 있는 사람 추적이 필요 |
| **역량 제한(PFL)** | 접촉을 허용하되 신체 부위별 힘·압력 한계로 제한 | 설계상 속도와 가반하중이 묶임 |

연구를 낳는 것은 뒤의 둘이고, 둘은 서로 다르게 실패한다. SSM의 이격 거리는 임계값이 아니라
**합**이다: 반응하는 동안 사람이 이동한 거리 + 로봇이 정지를 시작하기 전에 이동한 거리 +
정지 거리 + 두 위치 추정의 불확실성. SSM을 가능하게 한다고 주장하는 모든 학습 기반 인지
논문은 사실 *불확실성* 항에 대한 주장을 하고 있고, 검출기의 지연이 그 거리에 직접 들어간다.
PFL의 한계는 **신체 부위별**이다 — 손에 허용되는 힘과 압력은 얼굴의 것과 다르다 — 그래서
"힘 한계 이하"는 어느 부위, 어떤 접촉 유형(과도 접촉 대 준정적 접촉)을 가정했는지 밝히지
않으면 아무 의미가 없다.

건설에서는 어느 표준이 무엇에 적용되는지를 구분하라: 현장에서 움직이는 궤도·바퀴형 베이스는
**ISO 3691-4**로, 사람 옆에서 일하는 팔은 **ISO 10218**로 읽는다. 그리고 둘 중 어느 것도
울타리 없이 날씨에 노출되고 배치가 계속 바뀌는 옥외 현장을 위해 쓰이지 않았다. 그 빈틈을
논문에서 지적하는 것은 정당하다 — 다만 "안전" 일반이 아니라 이름을 댄 표준에 대고 말하라.

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
> 1. 노출이 작고 희귀 위험, 분포 이동, 심각도, 시스템 실패를 놓칠 수 있다. 숫자로 말하면: rule of three([[06-research-practice/experimental-design-reproducibility|실험 설계 §4]])에 따라 20회에서 실패 0은 참 실패율이 $3/20 = 15\%$ — 일곱 번에 한 번꼴의 충돌 — 까지와도 양립한다.
> 2. 운용자가 위험을 놓치거나, 인터페이스를 불신하거나, 과부하이거나, 권한이 없을 때.
> 3. 숙련, 멘탈 모델, 속도, 작업 부하, 위험 반응이 다르다.
> 4. 과제, 운용 도메인, 인간 역할, 개입/리셋, 안전 폴백, 지속 시간, 실패 처리.

### 출처


- 이 결정들이 딛고 선 인지 층: [[04-robotics/video-action-understanding|20. 비디오·행동 이해]], [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]], [[04-robotics/egocentric-perception|22. 자기중심 인지]], [[04-robotics/human-intent-prediction|23. 인간 의도·궤적 예측]] — 자율성과 권한은 결정이고, 그 페이지들이 그 결정의 근거다.
- [NIST Human-Robot Interaction](https://www.nist.gov/topics/human-robot-interaction)
- [NIST Robotics Test Methods](https://www.nist.gov/programs-projects/robotic-systems-smart-manufacturing-program)
- [ACM/IEEE International Conference on Human-Robot Interaction (HRI)](https://humanrobotinteraction.org/) — 분야 대표 학회; 인간 대상 연구 설계의 실제 기준을 보여주는 논문들
