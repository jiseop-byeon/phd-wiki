---
title: "DDIM — Denoising Diffusion Implicit Models"
authors: Jiaming Song, Chenlin Meng, Stefano Ermon
affiliation: Stanford University
venue: ICLR
year: 2021
arxiv: https://arxiv.org/abs/2010.02502
pdf: https://arxiv.org/pdf/2010.02502
tags: [paper, generative, diffusion]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Song et al., ICLR 2021** — [arXiv](https://arxiv.org/abs/2010.02502) · [PDF](https://arxiv.org/pdf/2010.02502)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]] is mandatory here. The key permission is stated in that note: the training loss only constrains the *marginals* $q(x_t|x_0)$, so any sampler consistent with them is legal — which is exactly the freedom DDIM spends.
> 여기서는 [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]이 필수다. 핵심 허가는 그 노트에 적혀 있다: 학습 손실은 *주변분포* $q(x_t|x_0)$만 제약하므로 그것과 일관된 어떤 샘플러도 허용된다 — DDIM이 쓰는 자유가 정확히 그것이다.

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

- **The step, concretely**: at noise level $t$ the network predicts the noise
  $\epsilon_\theta(x_t, t)$, from which you *read off the implied clean image*
  $\hat x_0 = (x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta)/\sqrt{\bar\alpha_t}$ (just the
  [[ddpm|DDPM]] marginal solved for $x_0$). Then you *re-noise $\hat x_0$ to the next, lower
  level* $t'$: $x_{t'} = \sqrt{\bar\alpha_{t'}}\,\hat x_0 + \sqrt{1-\bar\alpha_{t'}}\,\epsilon_\theta$.
  Guess-the-clean-image, re-noise-a-little-less, repeat — no random term, so you can take big
  jumps in $t$.
- Why this is *allowed*: DDPM's loss only ever constrained the marginals $q(x_t|x_0)$, never
  the specific reverse chain. A whole *family* of processes indexed by injected noise $\sigma$
  shares those marginals; $\sigma=0$ is the deterministic recipe above, $\sigma=\text{max}$
  recovers stochastic DDPM — **no retraining, same $\epsilon_\theta$**.
- That deterministic map has a continuous-time limit — an ODE — which is why "fewer steps"
  is legitimate: you are numerically integrating a smooth trajectory, not truncating a
  random walk.
- Deterministic mapping noise↔image = a consistent latent space: interpolation in $x_T$,
  reconstruction, and editing become well-defined.
- The ODE connection is drawn in the paper itself (§4.3) and later unified with the [[score-sde|probability-flow ODE]] framing.

### Results

- 10–50 step samples with quality near 1000-step DDPM (10–50× speedup); smooth latent
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

- **단계, 구체적으로**: 노이즈 수준 $t$에서 네트워크가 노이즈 $\epsilon_\theta(x_t, t)$를
  예측하고, 거기서 *함의된 깨끗한 이미지를 읽어낸다*
  $\hat x_0 = (x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta)/\sqrt{\bar\alpha_t}$ (그냥
  [[ddpm|DDPM]] marginal을 $x_0$에 대해 푼 것). 그다음 *$\hat x_0$를 다음의 더 낮은
  수준* $t'$로 다시 노이즈화한다:
  $x_{t'} = \sqrt{\bar\alpha_{t'}}\,\hat x_0 + \sqrt{1-\bar\alpha_{t'}}\,\epsilon_\theta$.
  깨끗한 이미지 추정 → 조금 덜 노이즈화 → 반복 — 무작위 항이 없으니 $t$를 크게 건너뛸 수 있다.
- 왜 *허용*되나: DDPM의 손실은 marginal $q(x_t|x_0)$만 제약했지 특정 역방향 체인을 제약한
  적이 없다. 주입 노이즈 $\sigma$로 인덱싱되는 과정의 *족* 전체가 그 marginal을 공유한다;
  $\sigma=0$이 위의 결정론적 레시피, $\sigma=\text{max}$가 확률적 DDPM을 복원 — **재학습
  없음, 같은 $\epsilon_\theta$**.
- 그 결정론적 사상은 연속 시간 극한(ODE)을 가진다 — 그래서 "스텝 수 감소"가 정당하다:
  무작위 보행을 잘라내는 게 아니라 매끄러운 궤적을 수치 적분하는 것이다.
- 노이즈↔이미지의 결정론적 사상 = 일관된 잠재 공간: $x_T$에서의 보간, 복원, 편집이
  잘 정의된다.
- ODE 연결은 논문 자신이 이미 그렸고(§4.3), 이후 [[score-sde|확률 흐름 ODE]] 프레임으로 널리 활용됐다.

### 결과

- 10~50 스텝으로 1000 스텝 DDPM에 근접한 품질(10~50배 가속); 매끄러운 잠재 보간;
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

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain why the observation that training only uses the marginals licenses a reinterpretation · 학습은 주변 분포만 쓴다는 관찰이 왜 재해석을 허용하는지 설명할 수 있다
- [ ] State what the consistent latent space created by deterministic sampling is used for (interpolation, inversion) · 결정론적 샘플링이 만드는 일관된 잠재 공간의 용도(보간·역변환)를 말할 수 있다
- [ ] Explain the principle by which steps are reduced without retraining · 재학습 없이 스텝을 줄이는 원리를 말할 수 있다
- [ ] State how it is now understood as a discretization of the probability-flow ODE · 확률 흐름 ODE의 이산화라는 사후적 이해를 말할 수 있다
