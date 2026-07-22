---
title: "Convex MPC for Legged Robots (MIT Cheetah) — Study Guide"
tags: [robotics, control, resource]
---

**Key references** — Di Carlo et al., *Dynamic Locomotion in the MIT Cheetah 3 Through Convex Model-Predictive Control*, IROS 2018 · [IEEE](https://ieeexplore.ieee.org/document/8594448) · Kim et al., *Highly Dynamic Quadruped Locomotion via Whole-Body Impulse Control and MPC* (open access) · [arXiv](https://arxiv.org/abs/1909.06586) · [PDF](https://arxiv.org/pdf/1909.06586)

## English

**What it is**: the paper that made real-time MPC standard on legged robots. The trick is a
*deliberate simplification*: approximate the robot as a single rigid body (ignore leg
dynamics), linearize the rotation dynamics around the current yaw, and treat ground
reaction forces as the decision variables with friction-cone constraints — the problem
becomes a **convex QP** solved at hundreds of Hz, exactly the machinery of
[[02-foundations/optimization|4. Optimization §5]]. Cheetah 3 galloped on this; the
follow-up (Kim et al., open access) pairs the MPC with whole-body impulse control — the
standard two-level stack (slow MPC plans forces, fast WBC tracks them) that echoes
[[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]'s System 2/System 1 split.

**Why read it here**: it is the cleanest case study of the modeling craft this wiki's
optimization page teaches — *choose the approximation that makes the problem convex, and
buy back accuracy with re-solving speed*. Also the classical baseline that learned
locomotion policies (RL) are compared against.

**Suggested path**: [[02-foundations/optimization|optimization page]] → the arXiv paper's
§III–IV (dynamics simplification + QP) → skim the IROS original for results.

## 한국어

**무엇인가**: 보행 로봇에서 실시간 MPC를 표준으로 만든 논문. 비결은 *의도된 단순화*다:
로봇을 단일 강체로 근사하고(다리 동역학 무시), 회전 동역학을 현재 요(yaw) 주변에서
선형화하고, 지면 반력을 마찰 원뿔 제약이 달린 결정 변수로 삼는다 — 문제가 수백 Hz로
풀리는 **볼록 QP**가 된다. 정확히 [[02-foundations/optimization|4. 최적화 §5]]의
기계장치다. Cheetah 3가 이걸로 질주했고, 후속(Kim et al., 공개 접근)은 MPC를 전신 임펄스
제어와 결합한다 — 느린 MPC가 힘을 계획하고 빠른 WBC가 추종하는 표준 2단 스택으로,
[[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]의 System 2/System 1 분할과 공명한다.

**여기서 읽는 이유**: 이 위키 최적화 페이지가 가르치는 모델링 기술 — *문제를 볼록하게
만드는 근사를 고르고, 정확도는 재풀이 속도로 되산다* — 의 가장 깔끔한 사례 연구다.
학습 기반 보행 정책(RL)이 비교당하는 고전 베이스라인이기도 하다.

**권장 경로**: [[02-foundations/optimization|최적화 페이지]] → arXiv 논문의 §III~IV
(동역학 단순화 + QP) → IROS 원문은 결과 위주로 훑기.

### 연결

- 기초: [[02-foundations/optimization|최적화]] · 이전: [[04-robotics/mpc|MPC]]
- 반향: [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] (이중 시스템)
