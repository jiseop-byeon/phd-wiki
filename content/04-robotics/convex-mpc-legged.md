---
title: "8. Convex MPC (Legged Robots)"
tags: [robotics, control, resource]
study-depth: Literacy
depth-goal: "Read the MPC formulation and recognize its assumptions and role in a complete robot system."
mastery-when: "Raise to Working or Mastery when legged control or MPC design is used directly."
---

**Key references** — Di Carlo et al., *Dynamic Locomotion in the MIT Cheetah 3 Through Convex Model-Predictive Control*, IROS 2018 · [IEEE](https://ieeexplore.ieee.org/document/8594448) · Kim et al., *Highly Dynamic Quadruped Locomotion via Whole-Body Impulse Control and MPC* (open access) · [arXiv](https://arxiv.org/abs/1909.06586) · [PDF](https://arxiv.org/pdf/1909.06586)

## English

*Last of group D and its worked application. Stands on [[04-robotics/mpc|7. MPC]], [[04-robotics/contact-force-tactile|9. Contact]] and the [[04-robotics/modern-robotics/index|MR chapters]].
The cleanest case study of the skill the optimization page teaches: choose the approximation that makes the problem convex.*

> [!info] Depth target · 깊이 목표
> Understand why the problem is convexified and what the simplification costs. This is a representative-application read, not a controller-design guide.
> 왜 문제를 볼록화했고 그 단순화의 대가가 무엇인지 이해하는 것이 목표다. 대표 응용 읽기이지 제어기 설계 가이드가 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/mpc|7. MPC]] (the formulation being applied) · [[02-foundations/optimization|4. Optimization §5]] (QP) · [[04-robotics/contact-force-tactile|9. Contact §2]] (the friction cone that becomes the constraint set) · [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8]] (what the single-rigid-body approximation throws away)
> [[04-robotics/mpc|7. MPC]] (적용되는 정식화) · [[02-foundations/optimization|4. 최적화 §5]] (QP) · [[04-robotics/contact-force-tactile|9. 접촉 §2]] (제약 집합이 되는 마찰 원뿔) · [[04-robotics/modern-robotics/ch08-dynamics|MR 8장]] (단일 강체 근사가 버리는 것)

**What it is**: the paper that made real-time MPC standard on legged robots. The trick is a
*deliberate simplification*: approximate the robot as a single rigid body (ignore leg
dynamics), linearize the rotation dynamics under a small roll-and-pitch assumption — the single state matrix uses the *average* reference yaw over the horizon, while each step's input matrix uses that step's reference yaw and footholds (the first step uses the current robot state) — and treat ground
reaction forces as the decision variables and approximate each circular friction cone by
linear facets (a friction pyramid). Those linear inequalities keep the problem a **convex
QP**, solved in the condensed form of [[04-robotics/mpc|7. MPC §2]], that solved in under a millisecond in the reported implementation and was re-run at
tens of Hz (Di Carlo et al.'s abstract says 20–30 Hz while their experiments ran at 25 to 50 Hz depending on gait, so the 50 Hz [[04-robotics/mpc|7. MPC §2]] sizes is the top of the paper's own range, not a disagreement) — exactly the machinery of
[[02-foundations/optimization|4. Optimization §5]]. Cheetah 3 galloped on this; the
follow-up (Kim et al., open access) pairs the MPC with whole-body impulse control — the
standard two-level stack (slow MPC plans forces, fast WBC tracks them) that echoes
[[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]'s System 2/System 1 split.

**Why read it here**: it is the cleanest case study of the modeling craft this wiki's
optimization page teaches — *choose the approximation that makes the problem convex, and
buy back accuracy with re-solving speed*. Also the classical baseline that learned
locomotion policies (RL) are compared against.

**Suggested path**: [[02-foundations/optimization|optimization page]] → Di Carlo et al. (IROS 2018; open copy on MIT DSpace)
§III–IV (simplified dynamics + QP), skimming §V for results → Kim et al. (arXiv 1909.06586) §III–IV for the MPC + whole-body impulse control stack.

## 한국어

*D군의 마지막이자 그 응용 사례다. [[04-robotics/mpc|7. MPC]]·[[04-robotics/contact-force-tactile|9. 접촉]]과 [[04-robotics/modern-robotics/index|MR 챕터 요약]] 위에 선다.
최적화 페이지가 가르치는 기술 — 문제를 볼록하게 만드는 근사를 고르는 것 — 의 가장 깔끔한 사례 연구다.*

**무엇인가**: 보행 로봇에서 실시간 MPC를 표준으로 만든 논문. 비결은 *의도된 단순화*다:
로봇을 단일 강체로 근사하고(다리 동역학 무시), 회전 동역학을 롤과 피치가 작다는 가정 아래 선형화하되 — 상태 행렬 하나는 지평 전체 기준 궤적의 *평균* 요를 쓰고, 단계별 입력 행렬은 그 단계의 기준 요와 발 위치를 쓴다(첫 단계는 현재 로봇 상태) — 지면 반력을 결정 변수로 삼되 원형 마찰 원뿔을 선형 면들로 이루어진 마찰 피라미드로
근사한다. 이 선형 부등식 덕분에 보고된 구현에서 1밀리초 안에 풀리고 수십 Hz로 다시 도는
(Di Carlo 등의 초록은 20~30 Hz지만 실험은 보행 방식에 따라 25~50 Hz로 돌았다. 그러니 [[04-robotics/mpc|7. MPC §2]]가 잡는 50 Hz는 논문 자신의 범위 상단이지 불일치가 아니다)
**볼록 QP**가 되며, [[04-robotics/mpc|7. MPC §2]]의 condensed 형태로 푼다. 정확히 [[02-foundations/optimization|4. 최적화 §5]]의
기계장치다. Cheetah 3가 이걸로 질주했고, 후속(Kim et al., 공개 접근)은 MPC를 전신 임펄스
제어와 결합한다 — 느린 MPC가 힘을 계획하고 빠른 WBC가 추종하는 표준 2단 스택으로,
[[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]의 System 2/System 1 분할과 공명한다.

**여기서 읽는 이유**: 이 위키 최적화 페이지가 가르치는 모델링 기술 — *문제를 볼록하게
만드는 근사를 고르고, 정확도는 재풀이 속도로 되산다* — 의 가장 깔끔한 사례 연구다.
학습 기반 보행 정책(RL)이 비교당하는 고전 베이스라인이기도 하다.

**권장 경로**: [[02-foundations/optimization|최적화 페이지]] → Di Carlo 외(IROS 2018; MIT DSpace 공개본) §III~IV(단순화 동역학 + QP), 결과는 §V를 훑기 → Kim 외(arXiv 1909.06586) §III~IV에서 MPC + 전신 임펄스 제어 스택.

### 연결

- 기초: [[02-foundations/optimization|최적화]] · 이전: [[04-robotics/mpc|MPC]]
- 반향: [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] (이중 시스템)

### After reading · 읽고 나면 말할 수 있어야 하는 것

- [ ] Say what the single-rigid-body approximation throws away and what it buys (convexity) · 단일 강체 근사가 버리는 것과 사는 것(볼록성)을 말할 수 있다
- [ ] Describe the setup in which ground reaction forces are the decision variables and friction cones the constraints · 지면 반력 + 마찰 원뿔이 결정 변수·제약이 되는 구성을 말할 수 있다
- [ ] Explain the division of labor in the slow-MPC + fast-WBC two-level stack · 느린 MPC + 빠른 WBC 2단 스택의 분업을 말할 수 있다
- [ ] State the modeling craft this case teaches: choose the approximation that makes the problem convex · 이 사례가 가르치는 모델링 기술(볼록하게 만드는 근사 선택)을 말할 수 있다
