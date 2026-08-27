---
title: 2. Foundations
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

## English

Course-level foundations supporting the research above (probability, optimization, signal
processing, Bayesian statistics). Source materials (lecture slides, textbooks) live in the
local `reference/` folder — **not published** for copyright reasons; this section holds my
own study notes distilled from them.

### Priority map (for physical-AI construction robotics research)

**Tier 1 — study fully (pillars)**
- Modern Robotics + kinematics/dynamics lectures → notes go to [[04-robotics/index|Robotics & Physical Systems]]
- Deep learning course slides → complements the [[01-canonical-papers/canonical-list|canonical papers]]
- Control theory (CE397 packet) → the MPC track in [[04-robotics/index|Robotics & Physical Systems]]
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

The pages below provide the **minimum conceptual background needed to begin reading every
paper in this wiki** (individual papers may require deeper references): math core (linear algebra, calculus, probability), the two applied pillars
(optimization, information theory), and two domain bridges (signal processing, RL).

- [[02-foundations/overview|0. Overview]] — prerequisites, study order, connection map
- [[02-foundations/engineering-math|0.5 Engineering Math]] — the assumed undergraduate math, self-contained: derivatives to Euler's formula, plus a notation dictionary
- [[02-foundations/neural-network-basics|0.7 What a Neural Network Is]] — layers, loss, batch, epoch, hyperparameter: the ML vocabulary pages 1–9 assume, for a reader who has only done engineering math
- [[02-foundations/linear-algebra|1. Linear Algebra]] — matrices as maps, rank/SVD, the geometry behind attention and LoRA
- [[02-foundations/calculus-backprop|2. Calculus & Backpropagation]] — chain rule to backprop, vanishing/exploding gradients as architecture history
- [[02-foundations/probability|3. Probability & Random Processes]] — Bayes to Kalman, MLE as the origin of many standard losses
- [[02-foundations/optimization|4. Optimization]] — problem anatomy, convexity, KKT, LP/QP/NLP/MIP, and where each shows up in robotics
- [[02-foundations/information-theory|5. Information Theory]] — entropy, cross-entropy, KL divergence, mutual information, the ELBO
- [[02-foundations/signal-processing|6. Signal Processing]] — sampling, FFT, filtering, sensor-pipeline habits
- [[02-foundations/rl-basics|7. Reinforcement Learning Basics]] — MDPs, value functions, policy gradients/PPO, model-based RL → world models
- [[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]] — rotations, quaternions, homogeneous transforms — the language of robot actions and camera poses
- [[02-foundations/ml-practice|9. ML Practice & Evaluation]] — data splits, overfitting, and the metrics dictionary for reading results tables

When the eleven pages (0.5–9) are done, take the **gate check** at the end of
[[02-foundations/overview|0. Overview]]: twelve cumulative questions that decide whether to
start the paper track. Nine or more is a pass.

### Specialization track

Page 10 is **not part of the common curriculum** — pages 0–9 remain the whole prerequisite
for reading every paper in this wiki. It belongs to the manipulation-first path in
[[07-research-program/index|7. Research Program]], and exists because the *Modern Robotics*
chapter summaries stop at kinematics, while contact-rich manipulation needs the dynamics
half and the equation that carries it into task space.

- [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] — the manipulator equation, Coriolis coupling, computed torque, and the operational-space inertia $\Lambda$ that makes force control readable

Skip it unless manipulation is your contribution area; read it before
[[04-robotics/contact-force-tactile|Contact, Force & Tactile]] if it is.

## 한국어

위의 연구를 받치는 과목 수준의 기초(확률, 최적화, 신호처리, 베이지안 통계).
원본 자료(강의 슬라이드, 교재)는 로컬 `reference/` 폴더에 있으며 저작권 때문에
**게시하지 않는다** — 이 섹션에는 그 자료에서 소화한 내 공부 노트만 올린다.

### 우선순위 지도 (physical AI 건설로봇 연구 기준)

**1순위 — 전체를 공부 (기둥 과목)**
- Modern Robotics + 기구학/동역학 강의 → 노트는 [[04-robotics/index|로보틱스 & Physical Systems]]에
- 딥러닝 강의 슬라이드 → [[01-canonical-papers/canonical-list|핵심 논문 리스트]]와 상호 보완
- 제어 이론 (CE397 교재) → [[04-robotics/index|로보틱스 & Physical Systems]]의 MPC 트랙
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

아래 페이지들은 **이 위키의 모든 논문을 읽기 시작하는 데 필요한 최소 개념 배경**을
제공한다(개별 논문을 깊게 이해하려면 추가 자료가 필요할 수 있다): 수학 핵심(선형대수, 미적분, 확률), 응용 기둥 둘(최적화, 정보이론), 도메인 다리 둘(신호처리, RL).

- [[02-foundations/overview|0. Overview]] — 사전 지식, 학습 순서, 연결 지도
- [[02-foundations/engineering-math|0.5 공업수학]] — 전제되는 학부 수학을 자체 완결로: 미분부터 오일러 공식까지 + 표기법 사전
- [[02-foundations/neural-network-basics|0.7 신경망이란 무엇인가]] — 층·손실·배치·에포크·하이퍼파라미터: 1~9페이지가 전제하는 ML 어휘를 공업수학만 한 독자를 위해
- [[02-foundations/linear-algebra|1. 선형대수]] — 사상으로서의 행렬, 랭크/SVD, 어텐션과 LoRA 뒤의 기하
- [[02-foundations/calculus-backprop|2. 미적분과 역전파]] — 연쇄 법칙에서 역전파까지, 구조 설계사(史)로서의 그래디언트 소실/폭발
- [[02-foundations/probability|3. 확률과 랜덤 프로세스]] — 베이즈에서 칼만까지, 많은 표준 손실함수의 기원으로서의 MLE
- [[02-foundations/optimization|4. 최적화]] — 문제의 구조, 볼록성, KKT, LP/QP/NLP/MIP와 로보틱스에서의 등장 지점
- [[02-foundations/information-theory|5. 정보이론]] — 엔트로피, 교차 엔트로피, KL divergence, 상호 정보량, ELBO
- [[02-foundations/signal-processing|6. 신호처리]] — 샘플링, FFT, 필터링, 센서 파이프라인 습관
- [[02-foundations/rl-basics|7. 강화학습 기초]] — MDP, 가치 함수, 정책 그래디언트/PPO, 모델 기반 RL → 월드모델
- [[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]] — 회전, 쿼터니언, 동차 변환 — 로봇 행동과 카메라 자세의 언어
- [[02-foundations/ml-practice|9. ML 실무와 평가]] — 데이터 분할, 과적합, 결과 표를 읽는 지표 사전

열한 페이지(0.5~9)를 마쳤으면 [[02-foundations/overview|0. Overview]] 끝의 **통과 점검**을 보라:
논문 트랙으로 넘어갈지를 판정하는 누적 12문항이고, 9개 이상이면 통과다.

### 전문화 트랙

10번은 **공통 커리큘럼이 아니다** — 이 위키의 모든 논문을 읽기 위한 선수 지식은 여전히
0~9번 전부다. 10번은 [[07-research-program/index|7. 연구 프로그램]]의 매니퓰레이션 우선
경로에 속하며, *Modern Robotics* 챕터 요약이 기구학에서 멈추는 반면 접촉이 많은 조작은
동역학 절반과 그것을 작업 공간으로 옮기는 방정식을 필요로 하기 때문에 존재한다.

- [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]] — 매니퓰레이터 방정식, 코리올리 결합, 계산 토크, 그리고 힘 제어를 읽을 수 있게 만드는 작업 공간 관성 $\Lambda$

매니퓰레이션이 기여 영역이 아니라면 건너뛰고, 맞다면
[[04-robotics/contact-force-tactile|접촉·힘·촉각]]보다 먼저 읽어라.
