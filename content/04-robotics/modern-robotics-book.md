---
title: "1. Modern Robotics"
tags: [robotics, resource]
---

**Lynch & Park, Cambridge University Press 2017** — [Free official preprint PDF](http://modernrobotics.org) · [Course wiki (videos, software)](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) · [Coursera specialization](https://www.coursera.org/specializations/modernrobotics)

## English

> [!info] Depth target · 깊이 목표
> Track-level ★: read the summarized chapters alongside the book until screw-theory notation (twists, wrenches, PoE, Jacobians) reads fluently. Full exercise sets are optional.
> 트랙 수준 ★: 스크류 이론 표기(twist·wrench·PoE·야코비안)가 술술 읽힐 때까지 요약과 원서를 함께 본다. 연습문제 전체 풀이는 선택이다.

**What it is**: the standard modern textbook for robot kinematics, dynamics, planning, and
control — built on the screw-theory/exponential-coordinates formulation (rather than
classical D-H parameters), which is exactly the formulation modern manipulation research
uses. The authors provide the **full book PDF free** at the official site, plus video
lectures and software (Python/MATLAB/Mathematica) on the course wiki, and a 6-course
Coursera specialization.

**Study path used in this wiki** (chapter notes to be added under `04-robotics/` as studied):

1. Configuration space (Ch. 2) — DoF, topology, constraints
2. Rigid-body motions (Ch. 3) — rotation matrices, twists, **SE(3)**, exponential coordinates
3. Forward kinematics (Ch. 4) — product of exponentials
4. Velocity kinematics & statics (Ch. 5) — the **Jacobian** (the same object as
   [[02-foundations/calculus-backprop|backprop's Jacobian]])
5. Inverse kinematics (Ch. 6) → Dynamics (Ch. 8) → Trajectory generation (Ch. 9) →
   Motion planning (Ch. 10) → Robot control (Ch. 11)

**Why it matters for this wiki**: every VLA paper's action space (end-effector poses,
joint commands) and every simulator's dynamics assume this material; SE(3) fluency is the
entry ticket to manipulation research.

## 한국어

**무엇인가**: 로봇 기구학·동역학·플래닝·제어의 현대 표준 교과서 — 고전 D-H 파라미터 대신
스크류 이론/지수 좌표 정식화를 쓰는데, 이것이 정확히 현대 매니퓰레이션 연구가 쓰는
표기다. 저자들이 공식 사이트에서 **책 전체 PDF를 무료로** 제공하고, 코스 위키에 강의
영상과 소프트웨어(Python/MATLAB/Mathematica), Coursera에 6과목 특화 과정이 있다.

**이 위키의 학습 경로** (공부하며 `04-robotics/` 아래에 챕터 노트 추가 예정):

1. Configuration space (2장) — 자유도, 위상, 제약
2. 강체 운동 (3장) — 회전 행렬, twist, **SE(3)**, 지수 좌표
3. 정기구학 (4장) — product of exponentials
4. 속도 기구학과 정역학 (5장) — **야코비안**
   ([[02-foundations/calculus-backprop|역전파의 야코비안]]과 같은 대상)
5. 역기구학 (6장) → 동역학 (8장) → 궤적 생성 (9장) → 모션 플래닝 (10장) → 로봇 제어 (11장)

**이 위키에서 중요한 이유**: 모든 VLA 논문의 행동 공간(말단 자세, 관절 명령)과 모든
시뮬레이터의 동역학이 이 내용을 전제한다; SE(3)에 능숙해지는 것이 매니퓰레이션 연구의
입장권이다.

### 연결

- [[02-foundations/linear-algebra|1. 선형대수]] (회전 행렬, 고유값) · [[02-foundations/calculus-backprop|2. 미적분]] (야코비안)
- 다음: [[04-robotics/lqr-lqg|LQR/LQG]] → [[04-robotics/mpc|MPC]]
