---
title: Foundations · 기초 과목
---

## English

Course-level foundations supporting the research above (probability, optimization, signal
processing, Bayesian statistics). Source materials (lecture slides, textbooks) live in the
local `reference/` folder — **not published** for copyright reasons; this section holds my
own study notes distilled from them.

### Priority map (for physical-AI construction robotics research)

**Tier 1 — study fully (pillars)**
- Modern Robotics + kinematics/dynamics lectures → notes go to [[20-robotics/index|Robotics & Control]]
- Deep learning course slides → complements the [[canonical-papers/canonical-list|canonical papers]]
- Control theory (CE397 packet) → the MPC track in [[20-robotics/index|Robotics & Control]]
- Optimization (LP → NLP → MIP) — the language of MPC, trajectory optimization, and task allocation

**Tier 2 — study the useful half, reference the rest**
- Probability & random processes — estimation, filtering, and ML theory all stand on this
- Signal processing — sampling, filtering, FFT for sensor pipelines (LiDAR, IMU, vision)

**Tier 3 — look up on demand**
- Stochastic processes (advanced: WSS, convergence theory) — needed only for deep estimation theory
- Bayesian statistics — becomes Tier 1 only if research turns to uncertainty quantification

### Study notes

- [[50-foundations/optimization|Optimization]] — problem anatomy, convexity, KKT, LP/QP/NLP/MIP, and where each shows up in robotics
- [[50-foundations/probability|Probability & Random Processes]] — Bayes to Kalman, MLE as the origin of every loss function
- [[50-foundations/signal-processing|Signal Processing]] — sampling, FFT, filtering, sensor-pipeline habits

## 한국어

위의 연구를 받치는 과목 수준의 기초(확률, 최적화, 신호처리, 베이지안 통계).
원본 자료(강의 슬라이드, 교재)는 로컬 `reference/` 폴더에 있으며 저작권 때문에
**게시하지 않는다** — 이 섹션에는 그 자료에서 소화한 내 공부 노트만 올린다.

### 우선순위 지도 (physical AI 건설로봇 연구 기준)

**1순위 — 전체를 공부 (기둥 과목)**
- Modern Robotics + 기구학/동역학 강의 → 노트는 [[20-robotics/index|로보틱스 & 제어]]에
- 딥러닝 강의 슬라이드 → [[canonical-papers/canonical-list|핵심 논문 리스트]]와 상호 보완
- 제어 이론 (CE397 교재) → [[20-robotics/index|로보틱스 & 제어]]의 MPC 트랙
- 최적화 (LP → NLP → MIP) — MPC·궤적 최적화·작업 할당의 공용 언어

**2순위 — 필요한 절반만 공부, 나머지는 참조**
- 확률과 랜덤 프로세스 — 추정, 필터링, ML 이론의 공통 토대
- 신호처리 — 센서 파이프라인(LiDAR, IMU, 비전)을 위한 샘플링·필터링·FFT

**3순위 — 필요할 때 찾아보기 (사전처럼)**
- 확률 과정 심화 (WSS, 수렴 이론) — 추정 이론을 깊게 팔 때만 필요
- 베이지안 통계 — 연구가 불확실성 정량화로 향할 때만 1순위로 승격

### 공부 노트

- [[50-foundations/optimization|최적화]] — 문제의 구조, 볼록성, KKT, LP/QP/NLP/MIP와 로보틱스에서의 등장 지점
- [[50-foundations/probability|확률과 랜덤 프로세스]] — 베이즈에서 칼만까지, 모든 손실함수의 기원으로서의 MLE
- [[50-foundations/signal-processing|신호처리]] — 샘플링, FFT, 필터링, 센서 파이프라인 습관
