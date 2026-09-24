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
- [[02-foundations/lab-plants|0.6 Lab Plants]] — six numbered plants (P1–P6) frozen for every problem set in Foundations and Robotics
- [[02-foundations/basic-mechanics|0.6.1 Basic Mechanics]] — the first of three pages of physics under the plants, taken where your degree left a gap: forces, springs, damping and friction, the mass–spring–damper, energy, torque and inertia, on P3's handle and P2's arm
- [[02-foundations/basic-circuits-electronics|0.6.2 Basic Circuits & Electronics]] — P6's motor drive and load-cell chain: Ohm's and Kirchhoff's laws, the RC filter, PWM and the H-bridge, op-amps, the Wheatstone bridge, the ADC and grounding
- [[02-foundations/fluid-power|0.6.3 Fluid Power]] — hydraulics, pneumatics and vacuum on an excavator's boom cylinder and S1's vacuum lifter: pressure, flow and power, the oil column as a spring, valve latency and a vacuum hold's margin
- [[02-foundations/lab-kernel|0.7 Lab Kernel]] — explicit Euler, symplectic Euler, plotting rules
- [[02-foundations/neural-network-basics|0.8 What a Neural Network Is]] — layers, loss, batch, epoch, hyperparameter: the ML vocabulary pages 1–9 assume, for a reader who has only done engineering math
- [[02-foundations/linear-algebra|1. Linear Algebra]] — matrices as maps, rank/SVD, the geometry behind attention and LoRA
- [[02-foundations/calculus-backprop|2. Calculus & Backpropagation]] — chain rule to backprop, vanishing/exploding gradients as architecture history
- [[02-foundations/probability|3. Probability & Random Processes]] — Bayes to Kalman, MLE as the origin of many standard losses
- [[02-foundations/optimization|4. Optimization]] — problem anatomy, convexity, KKT, LP/QP/NLP/MIP, and where each shows up in robotics
- [[02-foundations/information-theory|5. Information Theory]] — entropy, cross-entropy, KL divergence, mutual information, the ELBO
- [[02-foundations/signal-processing|6. Signal Processing]] — sampling, FFT, filtering, sensor-pipeline habits
- [[02-foundations/rl-basics|7. Reinforcement Learning Basics]] — MDPs, value functions, policy gradients/PPO, model-based RL → world models
- [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning]] — RL versus imitation, reward design and shaping, exploration and curriculum, RL on a real machine, reading an RL results section, learning the reward from preferences
- [[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]] — rotations, quaternions, homogeneous transforms — the language of robot actions and camera poses
- [[02-foundations/ml-practice|9. ML Practice & Evaluation]] — data splits, overfitting, and the metrics dictionary for reading results tables

When pages 0.5–9 are done, take the **gate check** at the end of
[[02-foundations/overview|0. Overview]]: fourteen common cumulative questions that decide
whether to start the paper track. Eleven or more is a pass; question 15 is an optional
manipulation check.

### Specialization track

Page 10 is **not part of the common curriculum**. Pages 0–9 are the common introductory
map; for a specific paper or optional path, follow that page's prerequisite box. Page 10
belongs to the dissertation path of [[07-research-program/index|7. Research Program §8]], where it follows the gate.
The *Modern Robotics* notes cover [[04-robotics/modern-robotics/ch08-dynamics|ch.8 dynamics]]
and [[04-robotics/modern-robotics/ch11-robot-control|ch.11 control]]; page 10 reorganizes the
ch.5, ch.8, and ch.11 ideas into one path through operational-space inertia and force control.

- [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] — the manipulator equation, Coriolis coupling, computed torque, and the operational-space inertia $\Lambda$ that makes force control readable

### Interview track

Track 11 is also outside the common curriculum. It prepares coding interviews and research-lab implementation interviews: complexity, data structures, sorting, greedy algorithms, dynamic programming, graph search, interview-ready Python and C++, and ten robotics and AI problems written from a blank editor. A*, Kalman, IK, and attention as *engineering* stay on the robotics and foundations course pages; 11.6 and 11.8 are the interview implementations of those tools.

- [[02-foundations/algorithms/index|11. Algorithms & Data Structures]] — eight pages, each algorithm with its invariant, complexity, tested code, and interview pitfalls

Skip the interview track unless a coding interview or a lab implementation interview is next. If the contribution is manipulation, read [[02-foundations/manipulator-kinematics-dynamics|10]] before [[04-robotics/contact-force-tactile|Contact, Force & Tactile]], not this track.

### Tools track

Track 12 is outside the common curriculum too, for a different reason: it teaches the tools the ROS 2 track and the experiments use and this wiki had not taught — the Linux shell, Git, Python for research code, config and data formats, networks, LaTeX and figures, GPU clusters, concurrency, and the mechanical design of a rig. Each page is taken when its need first arrives, not in one block.

- [[02-foundations/tools/index|12. Code, Tools & File Formats]] — nine pages, each tool priced on an object the wiki already uses, and when to take each; the C++ page, [[04-robotics/ros2/cpp-for-robot-code|25.0]], heads the ROS 2 track

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
- [[02-foundations/lab-plants|0.6 Lab Plants]] — 기초·로보틱스 과제에 쓰는 장치 여섯 개(P1–P6)
- [[02-foundations/basic-mechanics|0.6.1 기초 역학]] — 장치 밑에 깔린 물리 세 페이지의 첫째. 학위 과정이 빠뜨린 곳만 한다. 힘, 스프링, 감쇠와 마찰, 질량–스프링–댐퍼, 에너지, 토크와 관성을 P3의 핸들과 P2의 팔 위에서
- [[02-foundations/basic-circuits-electronics|0.6.2 기초 회로와 전자]] — P6의 모터 구동계와 로드셀 사슬: 옴과 키르히호프의 법칙, RC 필터, PWM과 H-브리지, 연산 증폭기, 휘트스톤 브리지, ADC와 접지
- [[02-foundations/fluid-power|0.6.3 유체 동력]] — 굴착기 붐 실린더와 S1의 진공 리프터 위의 유압·공압·진공: 압력, 유량과 동력, 스프링으로서의 기름 기둥, 밸브 지연, 진공 파지의 여유
- [[02-foundations/lab-kernel|0.7 Lab Kernel]] — 명시적 오일러, 심플렉틱 오일러, 플롯 규약
- [[02-foundations/neural-network-basics|0.8 신경망이란 무엇인가]] — 층·손실·배치·에포크·하이퍼파라미터: 1~9페이지가 전제하는 ML 어휘를 공업수학만 한 독자를 위해
- [[02-foundations/linear-algebra|1. 선형대수]] — 사상으로서의 행렬, 랭크/SVD, 어텐션과 LoRA 뒤의 기하
- [[02-foundations/calculus-backprop|2. 미적분과 역전파]] — 연쇄 법칙에서 역전파까지, 구조 설계사(史)로서의 그래디언트 소실/폭발
- [[02-foundations/probability|3. 확률과 랜덤 프로세스]] — 베이즈에서 칼만까지, 많은 표준 손실함수의 기원으로서의 MLE
- [[02-foundations/optimization|4. 최적화]] — 문제의 구조, 볼록성, KKT, LP/QP/NLP/MIP와 로보틱스에서의 등장 지점
- [[02-foundations/information-theory|5. 정보이론]] — 엔트로피, 교차 엔트로피, KL divergence, 상호 정보량, ELBO
- [[02-foundations/signal-processing|6. 신호처리]] — 샘플링, FFT, 필터링, 센서 파이프라인 습관
- [[02-foundations/rl-basics|7. 강화학습 기초]] — MDP, 가치 함수, 정책 그래디언트/PPO, 모델 기반 RL → 월드모델
- [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL]] — RL 대 모방, 보상 설계와 셰이핑, 탐색과 커리큘럼, 실제 기계 위의 RL, RL 결과 절 읽기, 선호로부터 보상 학습
- [[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]] — 회전, 쿼터니언, 동차 변환 — 로봇 행동과 카메라 자세의 언어
- [[02-foundations/ml-practice|9. ML 실무와 평가]] — 데이터 분할, 과적합, 결과 표를 읽는 지표 사전

0.5~9 페이지를 마쳤으면 [[02-foundations/overview|0. Overview]] 끝의 **통과 점검**(gate check)을 보라:
논문 트랙으로 넘어갈지를 판정하는 공통 누적 14문항이고, 11개 이상이면 통과다. 15번은
매니퓰레이션 경로의 선택 점검이다.

### 전문화 트랙

10번은 **공통 커리큘럼이 아니다**. 0~9번은 공통 입문 지도이고, 개별 논문과 선택 경로의
선수 지식은 해당 페이지의 선수 상자를 따른다. 10번은 [[07-research-program/index|7. 연구 프로그램 §8]]의
학위논문 경로에 속하고, 거기서 통과 점검 바로 뒤에 온다. *Modern Robotics* 노트도
[[04-robotics/modern-robotics/ch08-dynamics|8장 동역학]]과
[[04-robotics/modern-robotics/ch11-robot-control|11장 제어]]를 다루지만, 10번은 5·8·11장의
핵심을 작업공간 관성과 힘 제어까지 한 흐름으로 재구성한다.

- [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]] — 매니퓰레이터 방정식, 코리올리 결합, 계산 토크, 그리고 힘 제어를 읽을 수 있게 만드는 작업 공간 관성 $\Lambda$

### 인터뷰 트랙

11번 트랙도 공통 교과과정 밖에 있다. 코딩 인터뷰와 연구실 구현 인터뷰를 준비한다: 복잡도, 자료구조, 정렬, 그리디 알고리즘, 동적 계획법, 그래프 탐색, 인터뷰용 Python·C++, 그리고 빈 편집기에서 쓰는 로봇·AI 문제 열 개. A*·칼만·IK·attention의 *공학*은 로보틱스와 기초 교과 페이지에 두고, 11.6과 11.8은 그 도구의 면접 구현이다.

- [[02-foundations/algorithms/index|11. 알고리즘과 자료구조]] — 여덟 페이지, 알고리즘마다 불변식·복잡도·검증된 코드·인터뷰 함정

코딩 인터뷰나 연구실 구현 인터뷰가 아니면 이 트랙은 건너뛴다. 기여가 매니퓰레이션이면 [[04-robotics/contact-force-tactile|접촉·힘·촉각]]보다 먼저 읽을 것은 이 트랙이 아니라 [[02-foundations/manipulator-kinematics-dynamics|10]]이다.

### 도구 트랙

12번 트랙도 공통 교과과정 밖에 있지만 이유가 다르다. ROS 2 트랙과 실험이 쓰는데도 이 위키가 가르치지 않았던 도구를 가르친다 — 리눅스 셸, Git, 연구 코드를 위한 Python, 설정과 데이터 형식, 네트워크, LaTeX와 그림, GPU 클러스터, 동시성, 그리고 리그의 기계 설계. 한 덩어리로 하지 않고, 페이지마다 그 필요가 처음 생길 때 한다.

- [[02-foundations/tools/index|12. 코드·도구·파일 형식]] — 아홉 페이지. 도구마다 위키가 이미 쓰는 대상 위에서 값을 매기고, 각각을 언제 할지 적는다. C++ 페이지 [[04-robotics/ros2/cpp-for-robot-code|25.0]]은 ROS 2 트랙의 맨 앞에 있다
