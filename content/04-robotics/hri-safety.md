---
title: 11. Human–Robot Interaction & Safety
tags: [robotics, hri, safety, construction]
---

## English

When people operate, supervise, share space with, or depend on a robot, task success alone is not enough. Human–robot interaction studies authority, information, workload, trust, and performance; safety analysis asks which hazards can cause harm and how risk is reduced.

> [!warning] Scope
> This page is a literacy guide for reading research, not a certification or legal-compliance guide. Applicable laws and standards must be checked from current official sources for the specific machine, workplace, and jurisdiction.

> [!note] Prerequisites
> [[02-foundations/ml-practice|ML Practice & Evaluation]] · [[04-robotics/robot-systems-deployment|Robot Systems]] · [[05-construction-robotics/index|Construction Robotics]]

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

## 한국어

사람이 로봇을 조작·감독하거나 근처에서 함께 일하면 task success만으로 충분하지 않다. HRI는 authority, 정보, workload, trust와 human performance를 보고 safety는 어떤 hazard가 harm으로 이어지며 risk를 어떻게 줄이는지 본다. 이 페이지는 연구 문해력 가이드이지 인증·법규 준수 안내가 아니다.

Teleoperation, assisted teleoperation, shared autonomy, supervisory control, conditional autonomy와 full autonomy를 한 단어로 합치지 말라. Task, operating domain, intervention, reset과 fallback을 함께 적어야 autonomy level을 해석할 수 있다.

Human-in-the-loop는 정상 실행에 사람 입력이 필요하고, on-the-loop는 autonomy를 감독·개입하며, out-of-the-loop는 정의된 범위에서 runtime 역할이 없다. Intervention, takeover, recovery teleoperation과 physical reset은 서로 다르다.

Hazard는 잠재적 harm의 원천, risk는 정해진 방법 아래 가능성·노출과 결과의 결합이다. Fail-safe와 fail-operational도 다르다. 작은 실험에서 collision이 없었다는 이유만으로 learned policy가 안전한 것은 아니다.

건설 현장에서는 blind spot, 중장비 관성, noise/dust/PPE, spotter, remote operation, mixed work zone과 trained operator의 역할을 포함해야 한다. 논문의 “intuitive, transparent, trustworthy, safe”가 어떤 객관·주관 지표로 측정됐는지 확인하라.

위 영어 절의 After reading과 Self-check로 autonomy, authority, human study와 safety claim을 정확히 읽을 수 있는지 점검하라.
