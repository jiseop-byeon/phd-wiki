---
title: "Kindle et al. — Deflection and Backlash Compensation for a Construction Drilling Robot"
authors: Julien Kindle, Michael Loetscher, Andrea Alessandretti, Cesar Cadena, Marco Hutter
affiliation: ETH Zurich, Hilti
venue: IEEE Robotics and Automation Letters
year: 2025
journal-ref: "IEEE RA-L 10(1), 288–295, Jan 2025 (accepted Nov 2024 — the DOI stem reads 2024)"
arxiv: https://arxiv.org/abs/2501.14280
tags: [paper, construction, manipulation, calibration]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if end-effector accuracy under load becomes the thesis contribution."
---

**Kindle, Loetscher, Alessandretti, Cadena & Hutter**, "Enhancing Robotic Precision in Construction: A Modular Factor Graph-Based Framework to Deflection and Backlash Compensation Using High-Accuracy Accelerometers" — [arXiv:2501.14280](https://arxiv.org/abs/2501.14280); the arXiv comment field states acceptance to IEEE RA-L in November 2024.

> [!note] Math on-ramp · 수학 준비물
> Factor graphs as a way to fuse measurements into a consistent estimate ([[04-robotics/state-estimation-slam|3. State Estimation §4]]), and the reason a commanded joint angle is not the achieved one: compliance under load, which is the manipulator equation's world meeting real gears ([[02-foundations/manipulator-kinematics-dynamics|10. §7]]).
> 측정값들을 일관된 추정으로 융합하는 방법으로서의 factor graph([[04-robotics/state-estimation-slam|3. 상태 추정 §4]]), 그리고 명령한 관절각이 실제 관절각이 아닌 이유: 하중 하의 변형 — 매니퓰레이터 방정식의 세계가 실제 감속기와 만나는 지점이다([[02-foundations/manipulator-kinematics-dynamics|10. §7]]).

## English

**One-line summary**: A modular factor-graph framework that compensates arm deflection and gear backlash using high-accuracy accelerometers, evaluated on a 700 kg tracked construction drilling robot under simulated site disturbances.

### Context

Overhead drilling is the construction task with the clearest business case and, mechanically, one of the least forgiving: the robot pushes hard along the bit axis, and everything between the motors and the drill bit bends. A hole in the wrong place is not a soft failure — it is a hole in the wrong place.

This is where the abstraction of [[02-foundations/manipulator-kinematics-dynamics|10]] meets its limit. Forward kinematics maps *commanded* joint angles to an end-effector pose. Under thrust, the achieved angles are not the commanded ones, and gear backlash means the error is not even a fixed function of load.

### Method

> [!tip] Key intuition
> If you cannot compute where the tool is, measure it. Accelerometers on the structure sense the deflection the encoders cannot see, and a factor graph fuses those measurements with the kinematic model into a consistent estimate of the actual pose.

The platform, in the paper's own description, "weights about 700 kg and is composed of a base with rubber tracks, an extendable lifting column, a Doosan manipulator, and a drilling end effector" — identified in the paper as the **Hilti Jaibot**. This is, as far as this wiki found, the closest thing to a peer-reviewed paper about that machine.

### Results

The reported improvement is a **50% reduction in the 95% xy error threshold** against the Virtual Joint Method baseline — **and 31% when that baseline itself incorporates base tilt compensation**. Quote both: the 50% alone measures the gain over the weaker comparison. Seven datasets were captured "under conditions simulating realistic construction site disturbances" — wooden pallets, tilted surfaces, outdoor temperature variation — and released publicly.

> [!question] Reading the claim · 핵심 주장 읽는 법
> Read the setting precisely: **conditions *simulating* site disturbances**, in a controlled
> setup, not an active construction site. That is the middle rung of
> [[05-construction-robotics/construction-manipulation|9. §3]] — and it is an honest and
> well-designed version of that rung, with a public dataset, rather than a paper claiming
> more than it did.
> 설정을 정확히 읽어라: 통제된 셋업에서의 **현장 교란을 *모사한* 조건**이지 가동 중인 건설
> 현장이 아니다. [[05-construction-robotics/construction-manipulation|9. §3]]의 중간
> 단계이며, 자기가 한 것보다 더 주장하는 논문이 아니라 공개 데이터셋까지 갖춘 정직하고 잘
> 설계된 판본의 그 단계다.

### Limitations & critique

- **It solves accuracy, not contact.** Compensating deflection tells you where the bit is; it does not regulate the force it applies ([[04-robotics/force-compliance-control|13]]). Both are needed for drilling and this paper is the first.
- Extra sensors on the structure is a hardware answer — effective, and a constraint on retrofitting.
- Temperature is one of the disturbances, which is a good sign about how seriously the site was modelled, and also a hint at how many other such variables exist.
- One platform. The method is presented as modular, but modularity is a claim until someone ports it.

### Connections

- [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]] — the general treatment of the error budget this paper compensates term by term
- [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §7]] — where model parameters stop matching reality
- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — the task matrix row this belongs to
- [[04-robotics/state-estimation-slam|3. State Estimation & SLAM]] — factor graphs

### After reading

- [ ] Say why forward kinematics is not enough on a machine that pushes hard.
- [ ] State what the accelerometers see that the encoders cannot.
- [ ] Place the evaluation on the ladder, quoting the phrase that puts it there.

## 한국어

**한 줄 요약**: 고정밀 가속도계를 써서 팔의 변형과 감속기 백래시를 보상하는 모듈형 factor-graph 프레임워크. 700 kg 궤도형 건설 드릴링 로봇에서 현장 교란을 모사한 조건으로 평가했다.

### 배경

천장 드릴링은 사업성이 가장 분명하면서 역학적으로는 가장 관대하지 않은 건설 작업 중 하나다: 로봇이 비트 축을 따라 세게 밀고, 모터와 드릴 비트 사이의 모든 것이 휜다. 잘못된 자리의 구멍은 부드러운 실패가 아니다 — 잘못된 자리에 뚫린 구멍이다.

[[02-foundations/manipulator-kinematics-dynamics|10번]]의 추상이 한계를 만나는 지점이 여기다. 순기구학은 *명령한* 관절각을 말단 자세로 사상한다. 추력이 걸리면 실제 각도가 명령한 각도가 아니고, 감속기 백래시 때문에 그 오차는 하중의 고정된 함수조차 아니다.

### 방법

> [!tip] 핵심 직관
> 공구가 어디 있는지 계산할 수 없다면 재라. 구조물에 붙인 가속도계가 엔코더가 볼 수 없는 변형을 감지하고, factor graph가 그 측정값을 기구학 모델과 융합해 실제 자세의 일관된 추정을 만든다.

플랫폼은 논문 자신의 서술로 "약 700 kg이고 고무 궤도 베이스, 신축 리프팅 컬럼, Doosan 매니퓰레이터, 드릴링 말단장치로 구성"되며, 논문에서 **Hilti Jaibot**으로 식별된다. 이 위키가 찾은 범위에서 그 기계에 관한 심사 논문에 가장 가까운 것이다.

### 결과

보고된 개선은 Virtual Joint Method 기준선 대비 **95% xy 오차 임계값의 50% 감소**이고, 기준선이 베이스 기울기 보상을 포함할 때는 **31% 감소**이다. 둘 다 인용하라 — 50%만 떼면 더 약한 비교 대상에 대한 이득을 재는 것이다. "현실적인 건설 현장 교란을 모사하는 조건" — 나무 팔레트, 기울어진 면, 실외 온도 변화 — 에서 데이터셋 일곱 개를 취득해 공개했다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 설정을 정확히 읽어라: 통제된 셋업에서의 **현장 교란을 *모사한* 조건**이지 가동 중인 건설 현장이 아니다. [[05-construction-robotics/construction-manipulation|9. §3]]의 중간 단계이며, 자기가 한 것보다 더 주장하는 논문이 아니라 공개 데이터셋까지 갖춘 정직하고 잘 설계된 판본의 그 단계다.
> Conditions *simulating* site disturbances, in a controlled setup — the middle rung, done honestly.

### 한계와 비판

- **정확도를 풀지 접촉을 풀지 않는다.** 변형을 보상하면 비트가 어디 있는지는 알 수 있지만, 그것이 가하는 힘을 조절하지는 않는다([[04-robotics/force-compliance-control|13]]). 드릴링에는 둘 다 필요하고 이 논문은 앞의 것이다.
- 구조물에 센서를 더 다는 것은 하드웨어적 답이다 — 효과적이고, 개조에는 제약이다.
- 온도가 교란 중 하나라는 점은 현장을 얼마나 진지하게 모델링했는지에 대한 좋은 신호이자, 그런 변수가 또 얼마나 많을지에 대한 암시이기도 하다.
- 플랫폼 하나. 방법이 모듈형으로 제시되지만, 모듈성은 누군가 이식하기 전까지는 주장이다.

### 연결

- [[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 매니퓰레이션]] — 이 논문이 항별로 보상하는 오차 예산의 일반적 취급
- [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학 §7]] — 모델 파라미터가 현실과 어긋나기 시작하는 곳
- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 이것이 속하는 작업 매트릭스의 행
- [[04-robotics/state-estimation-slam|3. 상태 추정·SLAM]] — factor graph

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 세게 미는 기계에서 순기구학만으로 부족한 이유를 말한다.
- [ ] 가속도계가 엔코더는 볼 수 없는 무엇을 보는지 말한다.
- [ ] 평가를 사다리에 놓고, 거기 놓이게 만드는 표현을 인용한다.
