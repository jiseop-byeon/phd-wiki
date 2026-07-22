---
title: 9. Contact, Force & Tactile Interaction
tags: [robotics, contact, manipulation, tactile]
---

## English

Once a robot touches the world, geometry alone is insufficient. Contact introduces forces, friction, impacts, changing modes, deformation, and uncertainty. These effects are central to grasping, assembly, excavation, wiping, drilling, and handling flexible materials.

> [!info] Depth target
> Read contact-rich manipulation papers by identifying the contact model, sensing, control mode, material assumptions, and evaluation. Detailed complementarity solvers and continuum mechanics remain optional working/mastery topics.

> [!note] Prerequisites
> [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/optimization|Optimization]] · [[04-robotics/modern-robotics/ch05-velocity-kinematics|Statics and Jacobians]] · [[04-robotics/modern-robotics/ch08-dynamics|Dynamics]] · [[04-robotics/modern-robotics/ch12-grasping|Grasping]]

### 1. Why contact changes the problem

A contact is typically **unilateral**: objects may push but do not pull through an ordinary surface. Motion can switch among separation, impact, sticking, and sliding. This makes the dynamics hybrid and often nonsmooth.

For a gap $\phi(q)\ge 0$ and normal force $f_n\ge 0$, ideal rigid contact is summarized by

$$\phi(q)f_n=0$$

If separated, force is zero; if normal force is positive, the gap is closed. This complementarity is an idealized model, not a literal description of material deformation.

### 2. Normal force and friction

Coulomb friction is commonly approximated by

$$\lVert f_t\rVert\le \mu f_n$$

where $f_n$ is normal force, $f_t$ tangential force, and $\mu$ the friction coefficient. Forces inside the friction cone can be consistent with sticking; boundary or exceeded conditions indicate impending or actual slip under the model. The cone is a *force-feasibility bound* — whether the contact actually sticks or slides also depends on relative motion and the contact law. Real friction depends on material, speed, pressure, wear, and surface state.

### 3. Rigid and compliant models

| Model | Useful when | Main limitation |
|---|---|---|
| Rigid contact | deformation is small relative to task scale | impacts and mode switches are nonsmooth |
| Penalty/compliant contact | simulation needs continuous penetration forces | stiffness and damping are hard to identify |
| Learned/residual model | repeatable mismatch remains in data | extrapolation and physical consistency |

Simulator contact parameters are often numerical compromises. Success under one simulator setting is not evidence of robustness to real material variation.

### 4. Grasp and wrench language

A contact force produces a force and moment—a **wrench**—on the object. The grasp map combines contact forces into an object wrench. **Form closure** immobilizes an object through geometry under a specified contact model; **force closure** uses admissible contact forces, commonly including friction, to resist arbitrary external wrenches. Required contact counts depend on dimension, friction and contact assumptions, and general-position conditions.

### 5. Position, force, impedance, and admittance

| Mode | What is regulated |
|---|---|
| Position control | pose or trajectory error |
| Force control | measured contact force |
| Impedance control | desired relationship from motion error to force |
| Admittance control | desired motion response to measured force |

Impedance does not simply “control both position and force.” It shapes interaction behavior, often as a virtual mass–spring–damper. Admittance is useful when a stiff, accurate position-controlled robot can convert measured force into a compliant motion command.

### 6. Scenario: cleaning a wall

A pure position controller commands the tool 2 cm beyond an estimated wall. A 1 cm wall-location error can cause very different force because contact stiffness is high. An impedance controller instead permits pose error while shaping the restoring force; a force controller regulates normal force directly but still needs tangential motion and stability handling. The best architecture depends on actuator bandwidth, sensing, surface variation, and safety limits.

### 7. Force, tactile, and material state

- Wrist force/torque sensing measures net wrench but not the full pressure distribution.
- Tactile arrays can estimate contact location, pressure, shear, and slip cues.
- Proprioception observes the robot internally; exteroception senses the external world.
- Vision can observe global geometry while tactile sensing resolves local contact ambiguity.

Rope, cloth, soil, wet concrete, cables, and bulk material have high-dimensional, changing state. Their behavior depends on history and unobserved material properties, making representation and prediction difficult.

### 8. Learning and sim-to-real

Learning may estimate residual dynamics, contact state, friction/material properties, grasp scores, or a tactile-conditioned policy. Domain randomization can broaden training conditions, but the chosen randomization distribution defines what variation was covered. Privileged simulator state can aid training while being unavailable at deployment; check how the policy replaces it at test time.

### 9. Evaluation and paper language

Measure task success, peak/mean force, force-tracking error, slip/drop rate, object or surface damage, recovery, safety violations, and robustness across materials and friction. “Contact-rich,” “compliant,” and “robust” require explicit task and perturbation definitions.

> [!warning] Reading the claim
> A higher task success rate does not identify whether the gain came from tactile sensing, better control, safer force limits, or easier contact conditions. Look for matched baselines and ablations across sensing, controller, material, and initialization.

### After reading

- Explain unilateral contact and complementarity qualitatively.
- Interpret the friction-cone inequality and its assumptions.
- Distinguish form closure from force closure.
- Compare force, impedance, and admittance control.
- Identify what tactile sensing adds beyond wrist force and vision.
- Audit material variation and contact-related failure metrics.

### Self-check

1. Why can increasing position gain be dangerous during contact?
2. A tangential force is 6 N, normal force 10 N, and $\mu=0.5$. Is sticking allowed by the simple cone?
3. Why may a policy trained with one friction coefficient fail even with perfect perception?
4. What should a tactile-policy ablation hold constant?

> [!tip]- Answers
> 1. Small pose/model errors can generate large forces and instability. 2. No: $6>0.5\times10=5$ N. 3. Feasible forces, slip transitions, and dynamics change. 4. Demonstrations, architecture capacity, controller, initialization, materials, and evaluation protocol; remove or replace tactile information without making the rest easier.

### Sources

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation (Tedrake) — force control & contact chapters](https://manipulation.csail.mit.edu/)
- [Modern Robotics course wiki — ch. 12 videos & software](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)

## 한국어

로봇이 세계에 닿는 순간 기하만으로는 부족하다. 접촉은 힘, 마찰, 충격, 모드 전환, 변형,
불확실성을 끌고 들어온다. 이 효과들은 파지, 조립, 굴착, 닦기, 천공, 유연 재료 취급의
중심에 있다.

> [!info] 깊이 목표
> 접촉이 많은(contact-rich) 매니퓰레이션 논문에서 접촉 모델, 센싱, 제어 모드, 재료 가정,
> 평가를 짚어내며 읽는다. Complementarity 솔버와 연속체 역학의 세부는 선택적
> 실무/숙달 주제다.

> [!note] 선수 지식
> [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/optimization|최적화]] · [[04-robotics/modern-robotics/ch05-velocity-kinematics|정역학과 야코비안]] · [[04-robotics/modern-robotics/ch08-dynamics|동역학]] · [[04-robotics/modern-robotics/ch12-grasping|파지]]

### 1. 접촉이 문제를 바꾸는 이유

접촉은 보통 **단방향(unilateral)**이다: 물체는 밀 수 있지만 평범한 표면을 통해 당길 수는
없다. 운동은 분리·충격·고착(sticking)·미끄럼(sliding) 사이를 오간다. 그래서 동역학이
하이브리드가 되고 대개 비매끄럽다.

간극 $\phi(q)\ge 0$와 법선력 $f_n\ge 0$에 대해 이상적 강체 접촉은

$$\phi(q)f_n=0$$

으로 요약된다. 떨어져 있으면 힘이 0이고, 법선력이 양수면 간극이 닫혀 있다. 이
complementarity는 이상화된 모델이지 재료 변형의 문자 그대로의 기술이 아니다.

### 2. 법선력과 마찰

Coulomb 마찰은 흔히

$$\lVert f_t\rVert\le \mu f_n$$

로 근사한다. $f_n$은 법선력, $f_t$는 접선력, $\mu$는 마찰 계수다. 마찰 원뿔 안의 힘은
고착과 양립할 수 있고, 경계·초과 조건은 이 모델 아래 임박한·실제의 미끄럼을 나타낸다.
원뿔은 *힘의 실행 가능성 경계*다 — 실제로 고착하는지 미끄러지는지는 상대 운동과 접촉
법칙에도 의존한다.
실제 마찰은 재료, 속도, 압력, 마모, 표면 상태에 의존한다.

### 3. 강체 모델과 유연 모델

| 모델 | 유용한 경우 | 주된 한계 |
|---|---|---|
| 강체 접촉 | 변형이 과제 스케일 대비 작을 때 | 충격·모드 전환이 비매끄러움 |
| 페널티/유연 접촉 | 시뮬레이션에 연속적 침투력이 필요할 때 | 강성·감쇠의 동정이 어려움 |
| 학습/잔차 모델 | 반복 가능한 불일치가 데이터에 남을 때 | 외삽과 물리적 일관성 |

시뮬레이터의 접촉 파라미터는 대개 수치적 타협이다. 한 시뮬레이터 설정에서의 성공이
실제 재료 변동에 대한 강건성의 증거는 아니다.

### 4. 파지와 렌치의 언어

접촉력은 물체에 힘과 모멘트 — **렌치(wrench)** — 를 만든다. Grasp map은 접촉력들을
물체 렌치로 결합한다. **Form closure**는 명시된 접촉 모델 아래 기하만으로 물체를
고정하고, **force closure**는 허용 접촉력(대개 마찰 포함)으로 임의 외부 렌치에
저항한다. 필요한 접촉 수는 차원, 마찰·접촉 가정, 일반 위치 조건에 의존한다.

### 5. 위치, 힘, 임피던스, 어드미턴스

| 모드 | 조절 대상 |
|---|---|
| 위치 제어 | pose 또는 궤적 오차 |
| 힘 제어 | 측정된 접촉력 |
| 임피던스 제어 | 운동 오차 → 힘의 원하는 관계 |
| 어드미턴스 제어 | 측정 힘 → 운동 응답의 원하는 관계 |

임피던스는 단순히 "위치와 힘을 동시에 제어"하는 것이 아니다. 상호작용 거동을 — 대개
가상 질량-스프링-댐퍼로 — *형성*한다. 어드미턴스는 강성 높고 정확한 위치 제어 로봇이
측정 힘을 유연한 운동 명령으로 바꿀 때 유용하다.

### 6. 시나리오: 벽 닦기

순수 위치 제어기가 도구를 추정 벽면보다 2 cm 안쪽으로 명령한다. 접촉 강성이 높아 벽
위치의 1 cm 오차가 완전히 다른 힘을 만들 수 있다. 임피던스 제어기는 pose 오차를
허용하면서 복원력을 형성하고, 힘 제어기는 법선력을 직접 조절하지만 접선 운동과 안정성
처리가 따로 필요하다. 최선의 구조는 액추에이터 대역폭, 센싱, 표면 변동, 안전 한계에
달려 있다.

### 7. 힘, 촉각, 재료 상태

- 손목 힘/토크 센서는 합성 렌치를 재지만 전체 압력 분포는 못 잰다.
- 촉각 어레이는 접촉 위치, 압력, 전단, 미끄럼 신호를 추정할 수 있다.
- Proprioception은 로봇 내부를, exteroception은 외부 세계를 감지한다.
- 비전은 전역 기하를 보고, 촉각은 국소 접촉의 모호성을 푼다.

로프, 천, 흙, 젖은 콘크리트, 케이블, 벌크 재료는 고차원의 변하는 상태를 갖는다. 이력과
관측 안 되는 재료 성질에 의존해 표현과 예측이 어렵다.

### 8. 학습과 sim-to-real

학습은 잔차 동역학, 접촉 상태, 마찰/재료 성질, 파지 점수, 촉각 조건부 정책을 추정할 수
있다. Domain randomization은 학습 조건을 넓히지만, 선택한 randomization 분포가 곧
"어떤 변동까지 커버했는가"를 정의한다. 시뮬레이터의 특권 정보(privileged state)는 학습을
돕지만 배포 시에는 없다 — 정책이 시험 시점에 그것을 무엇으로 대체하는지 확인하라.

### 9. 평가와 논문 표현

과제 성공, 최대/평균 힘, 힘 추종 오차, 미끄럼/낙하율, 물체·표면 손상, 회복, 안전 위반,
재료·마찰에 걸친 강건성을 재라. "Contact-rich", "compliant", "robust"는 명시적 과제·교란
정의를 요구하는 주장이다.

> [!warning] 주장 읽는 법 · Reading the claim
> 성공률 상승만으로는 이득이 촉각 센싱, 더 나은 제어, 안전한 힘 한계, 쉬운 접촉 조건 중
> 어디서 왔는지 알 수 없다. 센싱·제어기·재료·초기화에 걸친 짝지은 베이스라인과 절제
> 실험을 찾아라.

### 읽고 나면 말할 수 있어야 하는 것

- 단방향 접촉과 complementarity를 정성적으로 설명할 수 있다
- 마찰 원뿔 부등식과 그 가정을 해석할 수 있다
- form closure와 force closure를 구분할 수 있다
- 힘·임피던스·어드미턴스 제어를 비교할 수 있다
- 촉각이 손목 힘·비전 너머에 더하는 것을 짚을 수 있다
- 재료 변동과 접촉 관련 실패 지표를 검사할 수 있다

### 스스로 점검

1. 접촉 중에 위치 이득을 올리는 것이 위험할 수 있는 이유는?
2. 접선력 6 N, 법선력 10 N, $\mu=0.5$. 단순 원뿔에서 고착이 허용되는가?
3. 인식이 완벽해도 한 마찰 계수로 학습한 정책이 실패할 수 있는 이유는?
4. 촉각 정책의 절제 실험에서 무엇을 고정해야 하는가?

> [!tip]- 정답 · Answers
> 1. 작은 pose/모델 오차가 큰 힘과 불안정을 만들 수 있다.
> 2. 아니다: $6>0.5\times10=5$ N.
> 3. 실행 가능한 힘, 미끄럼 전이, 동역학이 달라진다.
> 4. 시연, 모델 용량, 제어기, 초기화, 재료, 평가 프로토콜 — 나머지를 쉽게 만들지 않으면서 촉각 정보만 제거·대체해야 한다.

### 출처

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation (Tedrake) — 힘 제어·접촉 관련 장](https://manipulation.csail.mit.edu/)
- [Modern Robotics 코스 위키 — 12장 영상·소프트웨어](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)
