---
title: Probability & Random Processes · 확률과 랜덤 프로세스
tags: [foundations]
---

## English

Probability is the substrate under estimation, filtering, and every loss function in deep
learning. This page compresses a full course into the parts this research actually uses.

### 1. Core language

- Axioms → conditional probability $P(A|B) = P(A\cap B)/P(B)$ → **Bayes' rule**:
  $P(\theta|x) \propto P(x|\theta)P(\theta)$ — the grammar of all state estimation.
- Independence vs conditional independence (the assumption behind factor graphs and
  naive Bayes alike).

### 2. Random variables

- PMF/PDF/CDF; expectation as the integral that linearizes everything: $E[aX+bY]=aE[X]+bE[Y]$.
- Variance, covariance, correlation; conditional expectation $E[X|Y]$ — the best
  mean-square estimator, which is *why* estimation theory keeps computing it.
- The distributions that carry robotics: **Gaussian** (closed under linear maps and
  conditioning — the reason Kalman filtering works), Bernoulli/categorical (classification
  losses), exponential/Poisson (event arrivals, sensor dropout).

### 3. Multiple variables & transformations

- Joint/marginal/conditional PDFs; derived distributions of $g(X)$.
- Sums of independent RVs → convolution of densities.
- **LLN**: averages converge — why Monte Carlo and SGD work at all.
- **CLT**: sums become Gaussian — why noise models default to Gaussian and why batch
  statistics stabilize ([[canonical-papers/notes/batch-norm|BatchNorm]]).

### 4. Estimation

- **MLE**: $\hat\theta = \arg\max_\theta \log p(x|\theta)$. Cross-entropy training *is* MLE;
  MSE regression is MLE under Gaussian noise.
- **MAP** adds a prior — weight decay is a Gaussian prior in disguise.
- Bayesian filtering loop (predict–update) = Bayes' rule applied to a state-space model;
  with linear-Gaussian assumptions it collapses to the Kalman filter (→ [[20-robotics/index|control track]]).

### 5. Random processes (the useful minimum)

- A random process is an indexed family of RVs; characterized by mean and autocorrelation.
- **Stationarity / WSS**: statistics don't drift — the assumption behind spectral analysis
  and steady-state filters ([[50-foundations/signal-processing|signal processing]]).
- **White noise**: flat spectrum, uncorrelated samples — the default disturbance model in
  control and the $\epsilon$ injected in diffusion models.
- Markov property: the future depends only on the present state — the modeling assumption
  of MDPs, world models, and diffusion chains alike.

### 6. Where it appears in this wiki

- Cross-entropy/MSE losses = MLE (every training objective in [[canonical-papers/canonical-list|the paper list]])
- Diffusion models = a designed Markov chain of Gaussians (section 6)
- VAE's ELBO = Bayes + Jensen (upcoming note)
- SLAM/state estimation for construction sites = Bayesian filtering at scale

## 한국어

확률은 추정, 필터링, 그리고 딥러닝의 모든 손실함수 아래에 깔린 토대다.
이 페이지는 한 학기 분량을 이 연구가 실제로 쓰는 부분으로 압축한다.

### 1. 핵심 언어

- 공리 → 조건부 확률 $P(A|B) = P(A\cap B)/P(B)$ → **베이즈 정리**:
  $P(\theta|x) \propto P(x|\theta)P(\theta)$ — 모든 상태 추정의 문법.
- 독립과 조건부 독립 (팩터 그래프와 나이브 베이즈가 공유하는 가정).

### 2. 확률 변수

- PMF/PDF/CDF; 모든 것을 선형화하는 적분으로서의 기댓값: $E[aX+bY]=aE[X]+bE[Y]$
- 분산, 공분산, 상관; 조건부 기댓값 $E[X|Y]$ — 평균제곱 기준 최적 추정기라서
  추정 이론이 끊임없이 이것을 계산하는 것이다.
- 로보틱스를 떠받치는 분포들: **가우시안**(선형 변환과 조건화에 닫혀 있다 — 칼만 필터가
  작동하는 이유), 베르누이/카테고리(분류 손실), 지수/포아송(사건 도착, 센서 드롭아웃).

### 3. 다변수와 변환

- 결합/주변/조건부 PDF; $g(X)$의 유도 분포.
- 독립 확률변수의 합 → 밀도의 합성곱.
- **큰 수의 법칙**: 평균은 수렴한다 — 몬테카를로와 SGD가 애초에 작동하는 이유.
- **중심극한정리**: 합은 가우시안이 된다 — 노이즈 모델이 가우시안을 기본값으로 쓰는 이유,
  배치 통계가 안정되는 이유([[canonical-papers/notes/batch-norm|BatchNorm]]).

### 4. 추정

- **MLE**: $\hat\theta = \arg\max_\theta \log p(x|\theta)$. 교차 엔트로피 학습이 *곧* MLE이고,
  MSE 회귀는 가우시안 노이즈 아래의 MLE다.
- **MAP**은 사전 분포를 더한다 — weight decay는 변장한 가우시안 사전 분포다.
- 베이지안 필터링 루프(예측–갱신) = 상태공간 모델에 베이즈 정리를 적용한 것;
  선형-가우시안 가정에서 칼만 필터로 접힌다 (→ [[20-robotics/index|제어 트랙]]).

### 5. 랜덤 프로세스 (유용한 최소한)

- 랜덤 프로세스는 인덱스가 달린 확률변수의 족; 평균과 자기상관으로 특성화된다.
- **정상성 / WSS**: 통계량이 표류하지 않는다 — 스펙트럼 분석과 정상 상태 필터의 전제
  ([[50-foundations/signal-processing|신호처리]]).
- **백색 잡음**: 평평한 스펙트럼, 무상관 샘플 — 제어의 기본 외란 모델이자
  디퓨전 모델이 주입하는 $\epsilon$.
- 마르코프 성질: 미래는 현재 상태에만 의존 — MDP, 월드모델, 디퓨전 체인이 공유하는 가정.

### 6. 이 위키에서 등장하는 곳

- 교차 엔트로피/MSE 손실 = MLE ([[canonical-papers/canonical-list|논문 리스트]]의 모든 학습 목적함수)
- 디퓨전 모델 = 설계된 가우시안 마르코프 체인 (6번 섹션)
- VAE의 ELBO = 베이즈 + 옌센 (작성 예정 노트)
- 건설 현장 SLAM/상태 추정 = 대규모 베이지안 필터링
