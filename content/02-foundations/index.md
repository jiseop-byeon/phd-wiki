---
title: 2. Foundations
---

## English

Course-level foundations supporting the research above (probability, optimization, signal
processing, Bayesian statistics). Source materials (lecture slides, textbooks) live in the
local `reference/` folder — **not published** for copyright reasons; this section holds my
own study notes distilled from them.

### Priority map (for physical-AI construction robotics research)

**Tier 1 — study fully (pillars)**
- Modern Robotics + kinematics/dynamics lectures → notes go to [[04-robotics/index|Robotics & Control]]
- Deep learning course slides → complements the [[01-canonical-papers/canonical-list|canonical papers]]
- Control theory (CE397 packet) → the MPC track in [[04-robotics/index|Robotics & Control]]
- Optimization (LP → NLP → MIP) — the language of MPC, trajectory optimization, and task allocation

**Tier 2 — study the useful half, reference the rest**
- Probability & random processes — estimation, filtering, and ML theory all stand on this
- Signal processing — sampling, filtering, FFT for sensor pipelines (LiDAR, IMU, vision)

**Tier 3 — look up on demand**
- Stochastic processes (advanced: WSS, convergence theory) — needed only for deep estimation theory
- Bayesian statistics — becomes Tier 1 only if research turns to uncertainty quantification

### Study notes

Start with [[02-foundations/overview|0. Overview]] — the prerequisite engineering-math
checklist and the map of how these pages connect to each other and to the papers.

The pages below are designed to be **sufficient background for every paper in this
wiki**: math core (linear algebra, calculus, probability), the two applied pillars
(optimization, information theory), and two domain bridges (signal processing, RL).

- [[02-foundations/overview|0. Overview]] — prerequisites, study order, connection map
- [[02-foundations/engineering-math|0.1 Engineering Math]] — the assumed undergraduate math, self-contained: derivatives to Euler's formula, plus a notation dictionary
- [[02-foundations/linear-algebra|1. Linear Algebra]] — matrices as maps, rank/SVD, the geometry behind attention and LoRA
- [[02-foundations/calculus-backprop|2. Calculus & Backpropagation]] — chain rule to backprop, vanishing/exploding gradients as architecture history
- [[02-foundations/probability|3. Probability & Random Processes]] — Bayes to Kalman, MLE as the origin of every loss function
- [[02-foundations/optimization|4. Optimization]] — problem anatomy, convexity, KKT, LP/QP/NLP/MIP, and where each shows up in robotics
- [[02-foundations/information-theory|5. Information Theory]] — entropy, cross-entropy, KL divergence, mutual information, the ELBO
- [[02-foundations/signal-processing|6. Signal Processing]] — sampling, FFT, filtering, sensor-pipeline habits
- [[02-foundations/rl-basics|7. Reinforcement Learning Basics]] — MDPs, value functions, policy gradients/PPO, model-based RL → world models
- [[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]] — rotations, quaternions, homogeneous transforms — the language of robot actions and camera poses
- [[02-foundations/ml-practice|9. ML Practice & Evaluation]] — data splits, overfitting, and the metrics dictionary for reading results tables

## 한국어

위의 연구를 받치는 과목 수준의 기초(확률, 최적화, 신호처리, 베이지안 통계).
원본 자료(강의 슬라이드, 교재)는 로컬 `reference/` 폴더에 있으며 저작권 때문에
**게시하지 않는다** — 이 섹션에는 그 자료에서 소화한 내 공부 노트만 올린다.

### 우선순위 지도 (physical AI 건설로봇 연구 기준)

**1순위 — 전체를 공부 (기둥 과목)**
- Modern Robotics + 기구학/동역학 강의 → 노트는 [[04-robotics/index|로보틱스 & 제어]]에
- 딥러닝 강의 슬라이드 → [[01-canonical-papers/canonical-list|핵심 논문 리스트]]와 상호 보완
- 제어 이론 (CE397 교재) → [[04-robotics/index|로보틱스 & 제어]]의 MPC 트랙
- 최적화 (LP → NLP → MIP) — MPC·궤적 최적화·작업 할당의 공용 언어

**2순위 — 필요한 절반만 공부, 나머지는 참조**
- 확률과 랜덤 프로세스 — 추정, 필터링, ML 이론의 공통 토대
- 신호처리 — 센서 파이프라인(LiDAR, IMU, 비전)을 위한 샘플링·필터링·FFT

**3순위 — 필요할 때 찾아보기 (사전처럼)**
- 확률 과정 심화 (WSS, 수렴 이론) — 추정 이론을 깊게 팔 때만 필요
- 베이지안 통계 — 연구가 불확실성 정량화로 향할 때만 1순위로 승격

### 공부 노트

[[02-foundations/overview|0. Overview]]에서 시작하라 — 사전 공업수학 체크리스트와,
이 페이지들이 서로·논문들과 어떻게 연결되는지의 지도가 있다.

아래 페이지들은 **이 위키의 모든 논문을 읽는 데 충분한 배경**이 되도록 설계했다:
수학 핵심(선형대수, 미적분, 확률), 응용 기둥 둘(최적화, 정보이론), 도메인 다리 둘(신호처리, RL).

- [[02-foundations/overview|0. Overview]] — 사전 지식, 학습 순서, 연결 지도
- [[02-foundations/engineering-math|0.1 공업수학]] — 전제되는 학부 수학을 자체 완결로: 미분부터 오일러 공식까지 + 표기법 사전
- [[02-foundations/linear-algebra|1. 선형대수]] — 사상으로서의 행렬, 랭크/SVD, 어텐션과 LoRA 뒤의 기하
- [[02-foundations/calculus-backprop|2. 미적분과 역전파]] — 연쇄 법칙에서 역전파까지, 구조 설계사(史)로서의 그래디언트 소실/폭발
- [[02-foundations/probability|3. 확률과 랜덤 프로세스]] — 베이즈에서 칼만까지, 모든 손실함수의 기원으로서의 MLE
- [[02-foundations/optimization|4. 최적화]] — 문제의 구조, 볼록성, KKT, LP/QP/NLP/MIP와 로보틱스에서의 등장 지점
- [[02-foundations/information-theory|5. 정보이론]] — 엔트로피, 교차 엔트로피, KL divergence, 상호 정보량, ELBO
- [[02-foundations/signal-processing|6. 신호처리]] — 샘플링, FFT, 필터링, 센서 파이프라인 습관
- [[02-foundations/rl-basics|7. 강화학습 기초]] — MDP, 가치 함수, 정책 그래디언트/PPO, 모델 기반 RL → 월드모델
- [[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]] — 회전, 쿼터니언, 동차 변환 — 로봇 행동과 카메라 자세의 언어
- [[02-foundations/ml-practice|9. ML 실무와 평가]] — 데이터 분할, 과적합, 결과 표를 읽는 지표 사전
