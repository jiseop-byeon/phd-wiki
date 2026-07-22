---
title: "DDIM — Denoising Diffusion Implicit Models"
authors: Jiaming Song, Chenlin Meng, Stefano Ermon
affiliation: Stanford University
venue: ICLR
year: 2021
arxiv: https://arxiv.org/abs/2010.02502
pdf: https://arxiv.org/pdf/2010.02502
tags: [paper, generative, diffusion]
status: to-read
---

**Song et al., ICLR 2021** — [arXiv](https://arxiv.org/abs/2010.02502) · [PDF](https://arxiv.org/pdf/2010.02502)

## English

**One-line summary**: The same trained DDPM network admits a *non-Markovian, deterministic* sampler — 10–50 steps instead of 1000, plus an invertible latent space enabling interpolation and editing.

### Context

[[ddpm|DDPM]]'s quality came with a bill: ~1000 sequential network calls per sample. The
training objective, though, only ever uses marginals $q(x_t|x_0)$ — raising a subversive
question: is the Markovian 1000-step *reverse chain* actually required by the trained model?

### Method

> [!tip] Key intuition
> Many different generative processes share the same marginals the network was trained on.
> Choose the *deterministic* one: each step uses the predicted noise to jump toward the
> implied $x_0$, then re-project to the next (sparser) noise level — an ODE in disguise.

- A family of non-Markovian processes indexed by $\sigma$; $\sigma = 0$ gives deterministic
  DDIM, recovering DDPM at the stochastic end — **no retraining**, same $\epsilon_\theta$.
- Deterministic mapping noise↔image = a consistent latent space: interpolation in $x_T$,
  reconstruction, and editing become well-defined.
- Later understood as a discretization of the [[score-sde|probability-flow ODE]].

### Results

- 10–50 step samples with quality near 1000-step DDPM (10–100× speedup); smooth latent
  interpolations; near-exact inversion.

### Limitations & critique

- Very few steps still degrade fine detail — the gap later closed by higher-order solvers
  (DPM-Solver) and distillation (consistency models).
- Deterministic sampling trades away diversity knobs available to stochastic samplers.

### Impact & follow-ups

Made diffusion *deployable*: every practical system (Stable Diffusion samplers,
[[diffusion-policy|Diffusion Policy]]'s ~10-step inference) rides DDIM or its ODE-solver
descendants; DDIM inversion underpins image/trajectory editing methods.

### Connections

- Previous: [[ddpm|DDPM]] · Theory: [[score-sde|Score SDE]] (the ODE view) · Next: DPM-Solver, [[flow-matching|Flow Matching]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 학습된 DDPM 네트워크 그대로 *비마르코프·결정론적* 샘플러를 쓸 수 있다 — 1000 스텝 대신 10~50 스텝, 덤으로 보간과 편집이 가능한 가역 잠재 공간까지.

### 배경

[[ddpm|DDPM]]의 품질에는 청구서가 따라왔다: 샘플당 순차 네트워크 호출 약 1000번. 그런데
학습 목적함수는 주변 분포 $q(x_t|x_0)$만 쓴다 — 전복적인 질문이 나온다: 마르코프식 1000
스텝 *역방향 체인*이 학습된 모델에 정말 필수인가?

### 방법

> [!tip] 핵심 직관
> 네트워크가 학습한 주변 분포를 공유하는 생성 과정은 여럿이다. 그중 *결정론적인* 것을
> 골라라: 각 스텝은 예측된 노이즈로 함의된 $x_0$ 쪽으로 점프한 뒤 다음(더 성긴) 노이즈
> 수준으로 재투영한다 — 변장한 ODE다.

- $\sigma$로 인덱싱되는 비마르코프 과정의 족; $\sigma = 0$이면 결정론적 DDIM, 확률적
  극단에서 DDPM 복원 — **재학습 없음**, 같은 $\epsilon_\theta$.
- 노이즈↔이미지의 결정론적 사상 = 일관된 잠재 공간: $x_T$에서의 보간, 복원, 편집이
  잘 정의된다.
- 나중에 [[score-sde|확률 흐름 ODE]]의 이산화로 이해됨.

### 결과

- 10~50 스텝으로 1000 스텝 DDPM에 근접한 품질(10~100배 가속); 매끄러운 잠재 보간;
  거의 정확한 역변환.

### 한계와 비판

- 스텝을 극단적으로 줄이면 세부 품질 저하 — 이후 고차 솔버(DPM-Solver)와 증류(consistency
  모델)가 격차를 닫는다.
- 결정론적 샘플링은 확률적 샘플러가 가진 다양성 조절 손잡이를 내준다.

### 영향과 후속 연구

디퓨전을 *배포 가능*하게 만들었다: 모든 실용 시스템(Stable Diffusion 샘플러,
[[diffusion-policy|Diffusion Policy]]의 ~10 스텝 추론)이 DDIM 또는 그 ODE 솔버 후손 위를
달린다; DDIM 역변환은 이미지/궤적 편집 기법들의 토대다.

### 연결

- 이전: [[ddpm|DDPM]] · 이론: [[score-sde|Score SDE]] (ODE 관점) · 다음: DPM-Solver, [[flow-matching|Flow Matching]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]
