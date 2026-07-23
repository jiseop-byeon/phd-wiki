---
title: "Adam — A Method for Stochastic Optimization"
authors: Diederik P. Kingma, Jimmy Ba
affiliation: University of Amsterdam, University of Toronto
venue: ICLR
year: 2015
arxiv: https://arxiv.org/abs/1412.6980
pdf: https://arxiv.org/pdf/1412.6980
tags: [paper, foundations, optimization]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Kingma & Ba, ICLR 2015** — [arXiv](https://arxiv.org/abs/1412.6980) · [PDF](https://arxiv.org/pdf/1412.6980)

## English

**One-line summary**: Per-parameter adaptive learning rates from bias-corrected first and second moment estimates — the default optimizer of deep learning ever since.

### Context

SGD needs careful learning-rate tuning, and one global rate fits all parameters poorly when gradients vary wildly in scale. Momentum (velocity accumulation) and RMSProp (per-parameter scaling by recent gradient magnitude) each fixed part of the problem. Adam unified them with a principled correction.

### Method

> [!tip] Key intuition
> Track a running mean of gradients (where to go) and a running mean of squared gradients (how noisy/steep each direction is), then step each parameter by mean/√(variance) — every parameter gets its own effective learning rate.

- First moment: $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$; second moment: $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$.
- **Bias correction** $\hat{m}_t = m_t/(1-\beta_1^t)$, $\hat{v}_t = v_t/(1-\beta_2^t)$ — fixes the zero-initialization bias early in training (the paper's key technical contribution over RMSProp+momentum).
- Update: $\theta_t = \theta_{t-1} - \alpha\, \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon)$.
- Famous defaults that mostly just work: $\alpha=10^{-3}$, $\beta_1=0.9$, $\beta_2=0.999$.

### Results

- Faster, more robust convergence than SGD/AdaGrad/RMSProp across logistic regression, MLPs, and CNNs — with minimal tuning.
- Normalizing by the running second moment makes the effective step much less sensitive to raw
  gradient scale (roughly $\alpha$-sized in typical regimes — the exact bound depends on $\beta_1, \beta_2, \epsilon$ and moment history).

### Limitations & critique

- The original convergence proof was flawed (fixed by AMSGrad, 2018) — though the practical impact of the flaw is minimal.
- On some vision tasks, well-tuned SGD+momentum generalizes better — a long-running debate.
- L2 regularization interacts badly with adaptivity; **AdamW** (2019) decoupled weight decay and is today's true default for training Transformers.

### Impact & follow-ups

Arguably the most-used algorithm in deep learning; virtually every model in this wiki — from [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] to VLAs — was trained with Adam or AdamW. Follow-ups: AMSGrad, AdamW, and recent memory-efficient variants (Adafactor, 8-bit Adam, Lion).

### Connections

- Used by: essentially every note in `01-canonical-papers/notes/`
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 그래디언트의 1차·2차 모멘트 추정(편향 보정 포함)으로 파라미터마다 적응적 학습률을 주는 옵티마이저 — 이후 딥러닝의 기본값.

### 배경

SGD는 학습률 튜닝에 민감하고, 그래디언트 스케일이 파라미터마다 크게 다를 때 전역 학습률 하나로는 부족하다. 모멘텀(속도 누적)과 RMSProp(최근 그래디언트 크기로 파라미터별 스케일링)이 각각 문제의 일부를 해결했고, Adam은 이 둘을 원리적인 보정과 함께 통합했다.

### 방법

> [!tip] 핵심 직관
> 그래디언트의 이동 평균(어디로 갈지)과 그래디언트 제곱의 이동 평균(각 방향이 얼마나 가파르고 시끄러운지)을 추적한 뒤, 평균/√(분산)으로 스텝을 밟는다 — 파라미터마다 사실상 자기만의 학습률을 갖게 된다.

- 1차 모멘트: $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$; 2차 모멘트: $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$
- **편향 보정** $\hat{m}_t = m_t/(1-\beta_1^t)$, $\hat{v}_t = v_t/(1-\beta_2^t)$ — 0으로 초기화된 모멘트가 학습 초반에 과소평가되는 문제를 교정 (RMSProp+모멘텀 대비 이 논문의 핵심 기여).
- 업데이트: $\theta_t = \theta_{t-1} - \alpha\, \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon)$
- 유명한 기본값, 대체로 그냥 통한다: $\alpha=10^{-3}$, $\beta_1=0.9$, $\beta_2=0.999$

### 결과

- 로지스틱 회귀, MLP, CNN 전반에서 SGD/AdaGrad/RMSProp보다 빠르고 안정적인 수렴 — 튜닝은 거의 불필요.
- 이동 2차 모멘트로 정규화하므로 유효 스텝이 그래디언트의 원래 스케일에 훨씬 덜 민감하다
  (통상적으로 대략 $\alpha$ 크기 — 정확한 상한은 $\beta_1, \beta_2, \epsilon$과 모멘트 이력에 따라 달라진다).

### 한계와 비판

- 원 논문의 수렴 증명에 결함이 있었다(AMSGrad 2018가 수정) — 실무 영향은 미미하지만.
- 일부 비전 과제에서는 잘 튜닝된 SGD+모멘텀의 일반화가 더 좋다는 오랜 논쟁이 있다.
- L2 정규화가 적응성과 나쁘게 상호작용 — weight decay를 분리한 **AdamW**(2019)가 Transformer 학습의 진짜 기본값이 됐다.

### 영향과 후속 연구

딥러닝에서 가장 많이 쓰인 알고리즘이라 해도 과언이 아니다. [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]부터 VLA까지 이 위키의 거의 모든 모델이 Adam/AdamW로 학습됐다. 후속: AMSGrad, AdamW, 메모리 효율 변형들(Adafactor, 8-bit Adam, Lion).

### 연결

- 쓰이는 곳: `01-canonical-papers/notes/`의 사실상 모든 노트
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 1차 모멘트(방향)와 2차 모멘트(스케일)가 각각 무엇을 제공하는지 말할 수 있다
- [ ] 0 초기화된 모멘트에 편향 보정이 필요한 이유를 설명할 수 있다
- [ ] 2차 모멘트 정규화가 유효 스텝을 그래디언트 스케일에 덜 민감하게 만드는 이유와 실용적 의미를 말할 수 있다
- [ ] AdamW가 원래 Adam의 무엇을 분리해서 고쳤는지 말할 수 있다
