---
title: 4. Robotics & Control
---

## English

Map of content for robotics and control theory.

### Textbook spine

- **Modern Robotics** (Lynch & Park) — [[04-robotics/modern-robotics-book|book guide]] and
  [[04-robotics/modern-robotics/index|chapter summaries]] (ch. 2–6, 8–11): configuration
  space, rigid-body motions, forward/inverse kinematics, velocity kinematics & statics,
  dynamics, trajectory generation, motion planning, robot control
- Study guides: [[04-robotics/control-theory-ce397|control theory]] ·
  [[04-robotics/lqr-lqg|LQR/LQG]] · [[04-robotics/mpc|MPC]] ·
  [[04-robotics/convex-mpc-legged|convex MPC for legged robots]]

### Control theory track

Depth target: classical control solid, MPC to the level of "understand the formulation
and representative applications" (enough to read modern robotics papers).

1. State-space representation, stability, controllability/observability
2. LQR / LQG
3. MPC — receding horizon formulation, constraints, linear MPC; awareness of nonlinear MPC
4. Bridge to learning-based control (RL policies vs. MPC, hybrid approaches)

## 한국어

로보틱스와 제어 이론 공부의 전체 지도.

### 교재

- **Modern Robotics** (Lynch & Park) — 챕터 요약 (2–6장, 8–11장):
  [[04-robotics/modern-robotics/ch02-configuration-space|2장 C-space]] ·
  [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 강체 운동]] ·
  [[04-robotics/modern-robotics/ch04-forward-kinematics|4장 정기구학]] ·
  [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장 속도 기구학·정역학]] ·
  [[04-robotics/modern-robotics/ch06-inverse-kinematics|6장 역기구학]] ·
  [[04-robotics/modern-robotics/ch08-dynamics|8장 동역학]] ·
  [[04-robotics/modern-robotics/ch09-trajectory-generation|9장 궤적 생성]] ·
  [[04-robotics/modern-robotics/ch10-motion-planning|10장 모션 플래닝]] ·
  [[04-robotics/modern-robotics/ch11-robot-control|11장 로봇 제어]]


교재·가이드: [[04-robotics/modern-robotics-book|Modern Robotics]] · [[04-robotics/control-theory-ce397|제어 이론]] · [[04-robotics/lqr-lqg|LQR/LQG]] · [[04-robotics/mpc|MPC]] · [[04-robotics/convex-mpc-legged|보행 convex MPC]]

### 제어 공부 순서

목표 수준: 고전 제어는 확실하게, MPC는 문제 정식화와 대표적인 응용 사례를
이해하는 정도까지 (최신 로보틱스 논문을 읽을 수 있으면 충분하다).

1. 상태공간 표현, 안정성, 가제어성/가관측성
2. LQR / LQG
3. MPC — receding horizon 정식화, 제약조건 처리, 선형 MPC (비선형 MPC는 개념만)
4. 학습 기반 제어와의 연결 (RL 정책과 MPC의 비교, 하이브리드 방식)
