---
title: "PlaNet — Learning Latent Dynamics for Planning from Pixels"
authors: Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, James Davidson
affiliation: Google Brain, DeepMind, University of Toronto
venue: ICML
year: 2019
arxiv: https://arxiv.org/abs/1811.04551
pdf: https://arxiv.org/pdf/1811.04551
code: https://github.com/google-research/planet
tags: [paper, world-models, rl]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Hafner et al., ICML 2019** — [arXiv](https://arxiv.org/abs/1811.04551) · [PDF](https://arxiv.org/pdf/1811.04551) · [Code](https://github.com/google-research/planet)

> [!note] 수학 준비물 · Math on-ramp
> Training the RSSM is [[01-canonical-papers/notes/6-diffusion/vae|VAE]]'s ELBO unrolled over a sequence (prerequisite: [[02-foundations/information-theory|5. Information Theory §5]]). CEM planning is derivative-free optimization — sample, score, keep the best, refit.
> RSSM 학습은 [[01-canonical-papers/notes/6-diffusion/vae|VAE]]의 ELBO를 시퀀스로 편 것이다(준비물: [[02-foundations/information-theory|정보이론 §5]]). CEM은 미분 없는 최적화 — 샘플→상위 k 선택→분포 재적합의 반복일 뿐이다.

## English

**One-line summary**: The RSSM — a latent dynamics model with both deterministic and stochastic paths — makes *planning* in latent space work from pixels, at ~200× the sample efficiency of model-free RL.

### Context

[[world-models|World Models]] showed the dream is trainable but used a stagewise pipeline
and evolution strategies. The open engineering question: what latent dynamics architecture
is accurate enough, over long horizons, that you can *plan* through it — on continuous
control from raw pixels?

### Method

> [!tip] Key intuition
> Pure stochastic latents forget; pure deterministic latents can't represent uncertainty.
> Give the model both lanes — a deterministic GRU spine for memory plus stochastic state
> for uncertainty — and multi-step predictions stay sharp enough to search over.

- **RSSM (Recurrent State-Space Model)**: state = (deterministic $h_t$, stochastic $z_t$);
  trained by reconstruction + KL ([[vae|ELBO]]-style) on experience.
- **Planning instead of a policy**: at each step, CEM (cross-entropy method) searches action
  sequences in latent space, executes the first action, replans — model-predictive control
  with a learned model ([[04-robotics/index|MPC]], literally).
- Latent overshooting trains multi-step prediction consistency.

### Results

- Matches or approaches D4PG on 6 DeepMind Control Suite tasks from pixels with **~200×
  fewer environment interactions**; far ahead of A3C.
- One agent, one set of hyperparameters across tasks — early evidence latent models
  generalize across control problems.

### Limitations & critique

- Online CEM planning is compute-heavy at action time, and shooting-style planning
  struggles with long horizons and sparse rewards.
- Reconstruction-based training wastes capacity on visual detail irrelevant to control
  (the critique [[jepa|JEPA]] later generalizes).
- No learned value/policy — exactly what [[dreamer|Dreamer]] adds a year later.

### Impact & follow-ups

The RSSM became *the* standard world-model backbone: [[dreamer|Dreamer v1–v3]] keep it
nearly unchanged, and robotics latent-dynamics models inherit it. Also a clean conceptual
bridge between learned world models and classical [[04-robotics/index|MPC]].

### Connections

- Previous: [[world-models|World Models]] · Next: [[dreamer|Dreamer]]
- Foundations: [[vae|VAE/ELBO]], [[02-foundations/rl-basics|RL basics]], MPC ([[04-robotics/index|control track]])
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 결정론적 경로와 확률적 경로를 모두 가진 잠재 동역학 모델 RSSM으로, 픽셀에서 잠재 공간 *플래닝*을 작동시켰다 — 모델 프리 RL 대비 약 200배의 샘플 효율.

### 배경

[[world-models|World Models]]가 꿈이 훈련 가능함을 보였지만 단계별 파이프라인과 진화
전략을 썼다. 남은 공학적 질문: 어떤 잠재 동역학 구조가 긴 지평에서도 충분히 정확해서
그것을 통해 *계획*할 수 있는가 — 그것도 픽셀 입력의 연속 제어에서?

### 방법

> [!tip] 핵심 직관
> 순수 확률적 잠재변수는 잘 잊고, 순수 결정론적 잠재변수는 불확실성을 표현하지 못한다.
> 두 차선을 모두 줘라 — 기억을 담당하는 결정론적 GRU 척추 + 불확실성을 담는 확률적 상태
> — 그러면 다중 스텝 예측이 탐색을 버틸 만큼 선명해진다.

- **RSSM (순환 상태공간 모델)**: 상태 = (결정론적 $h_t$, 확률적 $z_t$);
  경험에 대한 복원 + KL([[vae|ELBO]]식)로 학습.
- **정책 대신 플래닝**: 매 스텝 CEM(cross-entropy method)이 잠재 공간에서 행동 시퀀스를
  탐색하고, 첫 행동만 실행 후 재계획 — 학습된 모델로 하는 모델 예측 제어
  ([[04-robotics/index|MPC]] 그 자체).
- Latent overshooting으로 다중 스텝 예측 일관성을 학습.

### 결과

- 픽셀 입력 DeepMind Control Suite 6개 과제에서 **환경 상호작용 약 200분의 1**로 D4PG에
  필적; A3C는 큰 폭으로 앞선다.
- 과제 전반에 단일 에이전트·단일 하이퍼파라미터 — 잠재 모델이 제어 문제를 가로질러
  일반화한다는 이른 증거.

### 한계와 비판

- 온라인 CEM 플래닝은 행동 시점 연산이 무겁고, 슈팅식 플래닝은 긴 지평과 희소 보상에서
  고전한다.
- 복원 기반 학습은 제어와 무관한 시각 디테일에 용량을 낭비한다
  ([[jepa|JEPA]]가 나중에 일반화하는 비판).
- 학습된 가치/정책이 없다 — 정확히 1년 뒤 [[dreamer|Dreamer]]가 더하는 것.

### 영향과 후속 연구

RSSM은 월드모델의 표준 백본이 됐다: [[dreamer|Dreamer v1–v3]]가 거의 그대로 유지하고,
로보틱스 잠재 동역학 모델들이 이를 물려받는다. 학습된 월드모델과 고전
[[04-robotics/index|MPC]] 사이의 깔끔한 개념적 다리이기도 하다.

### 연결

- 이전: [[world-models|World Models]] · 다음: [[dreamer|Dreamer]]
- 기초: [[vae|VAE/ELBO]], [[02-foundations/rl-basics|RL 기초]], MPC ([[04-robotics/index|제어 트랙]])
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Say why the RSSM needs both a deterministic and a stochastic path · RSSM의 결정론적/확률적 두 경로가 각각 왜 필요한지 말할 수 있다
- [ ] Describe the CEM planning procedure (sample → evaluate → keep the elites → resample) · CEM 플래닝의 절차(샘플→평가→상위 선택→재샘플)를 말할 수 있다
- [ ] Explain where the ~200× sample efficiency comes from · ~200× 샘플 효율이 어디서 오는지 설명할 수 있다
- [ ] State the cost of online planning and Dreamer's replacement for it (amortizing into a policy) · 온라인 플래닝의 비용과 Dreamer의 대체(정책 상각)를 말할 수 있다
