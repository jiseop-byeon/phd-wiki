---
title: "Impedance Control: An Approach to Manipulation (Parts I–III)"
authors: Neville Hogan
affiliation: MIT
venue: ASME Journal of Dynamic Systems, Measurement, and Control
year: 1985
doi: https://doi.org/10.1115/1.3140702
tags: [paper, manipulation, control]
status: note-complete
last_verified: 2026-08-21
study-depth: Mastery
wiki-support: Literacy
depth-goal: "Critique the assumptions and defend why regulating impedance is the right control objective in contact."
mastery-when: "Already at Mastery — the force-control layer is the contribution's closest dependency."
---

**Hogan, *ASME J. Dyn. Sys., Meas., Control*, vol. 107, no. 1, 1985** — Part I: Theory, pp. 1–7 ([DOI](https://doi.org/10.1115/1.3140702)) · Part II: Implementation, pp. 8–16 · Part III: Applications, pp. 17–24. An undivided earlier version appeared at the 1984 American Control Conference, pp. 304–313.

> [!note] Math on-ramp · 수학 준비물
> You need the manipulator equation and the external-wrench term ([[02-foundations/manipulator-kinematics-dynamics|10. §2]]), and what an impedance $Z = F/v$ is ([[04-robotics/force-compliance-control|13. §2]]). The argument is about *causality* — which variable is the cause and which the effect — so read it as physics, not as a control recipe.
> 매니퓰레이터 방정식과 외부 렌치 항([[02-foundations/manipulator-kinematics-dynamics|10. §2]]), 그리고 임피던스 $Z = F/v$가 무엇인지([[04-robotics/force-compliance-control|13. §2]])가 필요하다. 논증의 핵심이 *인과* — 어느 변수가 원인이고 어느 것이 결과인가 — 이므로, 제어 레시피가 아니라 물리로 읽어라.

## English

**One-line summary**: A manipulator in contact cannot be controlled as a pure position source or a pure force source, because the environment imposes the dual constraint; the controller should instead regulate the *impedance* — the dynamic relation between motion and force — at the interaction port.

### Context

Before this, contact control was a choice between two incomplete answers: control position and let the force be whatever it becomes, or control force and let the position drift. Both break in the way [[04-robotics/force-compliance-control|13. §1]] describes, because contact makes the two variables two faces of one thing.

### Method

> [!tip] Key intuition
> Ask what the environment *is*. Inertias and rigid constraints are *admittances*: you hand them a force and they decide the motion. A wall will not accept a position command — it accepts your push and tells you where your hand stops. At an interaction port the two sides have to be causal duals, so if the environment is the admittance, the robot is the one that must be the impedance. A robot that insists on commanding position anyway puts two position sources on one variable — a conflict with no solution. Command the *relation* between force and motion instead, and there is nothing to fight about.

Part I develops the physical-systems and port argument, and it is the part to read closely: the causality analysis is why impedance control is a claim about physics rather than a tuning preference. Part II gives the nonlinear implementation on manipulator dynamics. Part III applies it to contact and constrained motion.

### Results

The result is conceptual rather than numerical: a control objective, a justification for it, and an implementation on the manipulator equation. Its value is measured by what came after — every compliant manipulation controller in use is a descendant.

### Limitations & critique

- Impedance control **needs a torque-controlled, backdrivable arm**. On a position-controlled industrial arm you get admittance control instead, with the vendor's stiffness in series ([[04-robotics/force-compliance-control|13. §2]]) — a different system with different failure modes.
- The framework says *what* to regulate, not what values to choose; the achievable range is bounded, and Colgate and Hogan's 1988 passivity result is where that bound gets stated.
- Rendering a desired impedance depends on the dynamic model, so it inherits the parameter problem of [[02-foundations/manipulator-kinematics-dynamics|10. §7]].

### Connections

- [[04-robotics/force-compliance-control|13. Force & Compliance Control]] — the concept page this anchors
- [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] — the equation it acts on

### After reading

- [ ] State the causality argument in one sentence.
- [ ] Say what hardware impedance control requires and what you get without it.
- [ ] Name what the framework does not tell you.

## 한국어

**한 줄 요약**: 접촉 중인 매니퓰레이터는 순수한 위치 소스로도 순수한 힘 소스로도 제어될 수 없다. 환경이 이중의 제약을 부과하기 때문이다. 제어기는 대신 상호작용 포트에서 *임피던스* — 운동과 힘의 동적 관계 — 를 조절해야 한다.

### 배경

이전까지 접촉 제어는 불완전한 두 답 사이의 선택이었다: 위치를 제어하고 힘은 되는 대로 두거나, 힘을 제어하고 위치가 표류하게 두거나. 둘 다 [[04-robotics/force-compliance-control|13. §1]]이 묘사하는 방식으로 깨진다. 접촉이 두 변수를 한 대상의 두 얼굴로 만들기 때문이다.

### 방법

> [!tip] 핵심 직관
> 환경이 *무엇인지* 물어라. 관성과 강체 구속은 *어드미턴스*다. 힘을 건네면 운동을 정해서 돌려준다. 벽은 위치 명령을 받지 않는다 — 미는 힘을 받아 손이 어디서 멈추는지를 알려줄 뿐이다. 상호작용 포트의 양쪽은 인과적으로 서로 쌍대여야 하므로, 환경이 어드미턴스라면 임피던스여야 하는 쪽은 로봇이다. 그런데도 로봇이 위치를 명령하겠다고 고집하면 하나의 변수에 위치 소스가 둘 놓이는 것이고, 해가 없는 충돌이다. 대신 힘과 운동의 *관계*를 명령하면 싸울 것이 없어진다.

Part I이 물리 시스템과 포트 논증을 전개하며, 정독할 부분이다: 인과 분석이야말로 임피던스 제어가 튜닝 취향이 아니라 물리에 관한 주장인 이유다. Part II는 매니퓰레이터 동역학 위의 비선형 구현을, Part III는 접촉과 구속 운동에의 적용을 다룬다.

### 결과

결과가 수치가 아니라 개념이다: 제어 목표, 그것에 대한 정당화, 그리고 매니퓰레이터 방정식 위의 구현. 그 값어치는 뒤에 온 것들로 측정된다 — 현재 쓰이는 모든 유연 조작 제어기가 그 후손이다.

### 한계와 비판

- 임피던스 제어는 **토크 제어되고 역구동 가능한 팔을 요구한다.** 위치 제어 산업용 팔에서는 벤더의 강성이 직렬로 낀 어드미턴스 제어를 얻게 된다([[04-robotics/force-compliance-control|13. §2]]) — 실패 모드가 다른 다른 시스템이다.
- 이 틀은 *무엇을* 조절할지 말하지 어떤 값을 고를지는 말하지 않는다. 구현 가능한 범위에는 한계가 있고, 그 한계를 진술하는 것이 Colgate와 Hogan의 1988년 수동성 결과다.
- 원하는 임피던스를 구현하는 것이 동역학 모델에 의존하므로, [[02-foundations/manipulator-kinematics-dynamics|10. §7]]의 파라미터 문제를 그대로 물려받는다.

### 연결

- [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]] — 이 논문이 앵커인 개념 페이지
- [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]] — 그것이 작용하는 방정식

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 인과 논증을 한 문장으로 말한다.
- [ ] 임피던스 제어가 요구하는 하드웨어와, 그것이 없을 때 얻게 되는 것을 말한다.
- [ ] 이 틀이 말해 주지 않는 것을 댄다.
