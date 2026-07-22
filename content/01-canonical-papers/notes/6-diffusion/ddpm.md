---
title: "DDPM — Denoising Diffusion Probabilistic Models"
authors: Jonathan Ho, Ajay Jain, Pieter Abbeel
affiliation: UC Berkeley
venue: NeurIPS
year: 2020
arxiv: https://arxiv.org/abs/2006.11239
pdf: https://arxiv.org/pdf/2006.11239
code: https://github.com/hojonathanho/diffusion
tags: [paper, generative, diffusion]
status: to-read
---

**Ho et al., NeurIPS 2020** — [arXiv](https://arxiv.org/abs/2006.11239) · [PDF](https://arxiv.org/pdf/2006.11239) · [Code](https://github.com/hojonathanho/diffusion)

> [!note] 수학 준비물 · Math on-ramp
> 필요한 전부: [[02-foundations/probability|확률 §3]]의 가우시안 닫힘 성질, [[02-foundations/information-theory|정보이론 §5]]의 ELBO, [[02-foundations/engineering-math|0.5 §6]]의 로그. 폐쇄형의 유도 감각은 두 스텝이면 잡힌다: $x_2 = \sqrt{1-\beta_2}\,x_1 + \sqrt{\beta_2}\,\epsilon_2$에 $x_1 = \sqrt{1-\beta_1}\,x_0 + \sqrt{\beta_1}\,\epsilon_1$을 대입하면, $x_0$의 계수는 $\sqrt{(1-\beta_1)(1-\beta_2)} = \sqrt{\bar\alpha_2}$가 되고 두 개의 독립 가우시안 노이즈는 분산이 더해져 하나의 $\epsilon$으로 합쳐진다(분산 $1-\bar\alpha_2$). $t$스텝이어도 같은 논리다.

## English

**One-line summary**: Destroy data with a fixed Gaussian noising chain, train a network to reverse it one step at a time — the variational objective collapses to simple noise-prediction regression, and generation quality jumps past GANs' stability problems.

### Context

The generative landscape was a trade-off: [[gan|GANs]] sharp but unstable and mode-dropping;
[[vae|VAEs]] stable but blurry. Diffusion probabilistic models (Sohl-Dickstein 2015) had the
right skeleton — a fixed forward corruption, a learned reverse — but underperformed for five
years. DDPM found the parameterization that makes them work.

### Method

> [!tip] Key intuition
> Generating from scratch is hard; *removing a little noise* is easy regression. Chain a
> thousand tiny denoising steps and the easy problems compose into generation. The magic:
> the correct variational objective reduces to "predict the noise that was added" — plain MSE.

- **Forward process** (fixed, no learning): $q(x_t|x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}\,x_{t-1}, \beta_t I)$;
  closed form allows jumping to any $t$: $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon$.
- **Reverse process**: learn $p_\theta(x_{t-1}|x_t)$, Gaussian with predicted mean.
- **The key reparameterization**: predict the noise $\epsilon_\theta(x_t, t)$ instead of the mean;
  the (weighted) ELBO becomes $E_{t,x_0,\epsilon}\big[\|\epsilon - \epsilon_\theta(x_t,t)\|^2\big]$ — the "simple loss."
- U-Net backbone with timestep embedding; ~1000 steps at inference.
- Connection shown in the paper: this objective matches **denoising score matching** — the
  bridge to [[score-sde|score-based models]].

### Results

- CIFAR-10 FID **3.17** — best-in-class at publication, from a stable regression objective
  with none of GANs' adversarial fragility.
- High-quality 256×256 samples (LSUN); progressive generation and interpolation in noise space.

### Limitations & critique

- **Sampling cost**: ~1000 network evaluations per sample (DDIM soon cut this to ~50;
  distillation later to 1–4).
- Log-likelihoods lag autoregressive models despite great samples.
- Pixel-space diffusion at high resolution is compute-hungry — solved by moving to latent
  space ([[01-canonical-papers/canonical-list|Latent Diffusion]]).

### Impact & follow-ups

Made diffusion the dominant generative paradigm: Stable Diffusion, Imagen, video generation
(Sora), and — critically for this wiki — **robot action generation**: Diffusion Policy denoises
action trajectories exactly this way, and π0's flow matching is this idea's continuous-time
descendant. The noise-prediction U-Net/DiT recipe is today's default generative backbone.

### Connections

- Previous: [[vae|VAE]] (the variational machinery), [[gan|GAN]] (the rival it displaced)
- Next: [[score-sde|Score SDE]] (unifying view), DDIM, Latent Diffusion → Diffusion Policy
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 고정된 가우시안 노이즈 체인으로 데이터를 파괴하고, 그것을 한 스텝씩 되돌리는 네트워크를 학습 — 변분 목적함수가 단순한 노이즈 예측 회귀로 접히고, 생성 품질이 GAN의 안정성 문제를 우회해 도약한다.

### 배경

생성 모델의 지형은 트레이드오프였다: [[gan|GAN]]은 선명하지만 불안정하고 모드를 놓치며,
[[vae|VAE]]는 안정적이지만 흐릿하다. 디퓨전 확률 모델(Sohl-Dickstein 2015)은 올바른 뼈대 —
고정된 순방향 손상, 학습된 역방향 — 를 갖고 있었지만 5년간 성능이 나빴다. DDPM이
작동하게 만드는 매개변수화를 찾아냈다.

### 방법

> [!tip] 핵심 직관
> 처음부터 생성하는 건 어렵지만, *약간의 노이즈를 제거하는 것*은 쉬운 회귀 문제다.
> 천 개의 작은 잡음 제거 스텝을 이으면 쉬운 문제들이 합성되어 생성이 된다. 마법은:
> 올바른 변분 목적함수가 "추가된 노이즈를 예측하라"로 환원된다는 것 — 그냥 MSE다.

- **순방향 과정** (고정, 학습 없음): $q(x_t|x_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}\,x_{t-1}, \beta_t I)$;
  닫힌 형태 덕에 임의의 $t$로 점프 가능: $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon$
- **역방향 과정**: 예측된 평균을 갖는 가우시안 $p_\theta(x_{t-1}|x_t)$를 학습.
- **결정적 재매개변수화**: 평균 대신 노이즈 $\epsilon_\theta(x_t, t)$를 예측;
  (가중된) ELBO가 $E_{t,x_0,\epsilon}\big[\|\epsilon - \epsilon_\theta(x_t,t)\|^2\big]$가 된다 — "simple loss".
- 타임스텝 임베딩을 가진 U-Net 백본; 추론 시 약 1000 스텝.
- 논문이 보인 연결: 이 목적함수는 **denoising score matching**과 일치한다 —
  [[score-sde|score 기반 모델]]로 가는 다리.

### 결과

- CIFAR-10 FID **3.17** — 발표 시점 최고 수준을, GAN의 적대적 취약성 없이 안정적인
  회귀 목적함수로 달성.
- 256×256 고품질 샘플(LSUN); 점진적 생성과 노이즈 공간 보간.

### 한계와 비판

- **샘플링 비용**: 샘플당 네트워크 평가 약 1000회 (곧 DDIM이 ~50회로, 이후 증류가 1~4회로 단축).
- 샘플 품질에 비해 로그 우도는 자기회귀 모델에 뒤진다.
- 고해상도 픽셀 공간 디퓨전은 연산 대식가 — 잠재 공간으로 옮겨 해결된다
  ([[01-canonical-papers/canonical-list|Latent Diffusion]]).

### 영향과 후속 연구

디퓨전을 지배적 생성 패러다임으로 만들었다: Stable Diffusion, Imagen, 비디오 생성(Sora),
그리고 이 위키에 결정적으로 — **로봇 행동 생성**: Diffusion Policy는 정확히 이 방식으로 행동
궤적의 노이즈를 제거하고, π0의 flow matching은 이 아이디어의 연속 시간 후손이다.
노이즈 예측 U-Net/DiT 레시피는 오늘날 생성 모델의 기본 백본이다.

### 연결

- 이전: [[vae|VAE]] (변분 기계장치), [[gan|GAN]] (밀어낸 경쟁자)
- 다음: [[score-sde|Score SDE]] (통합 관점), DDIM, Latent Diffusion → Diffusion Policy
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 순방향 폐쇄형 $x_t = \sqrt{\bar\alpha_t}x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon$을 가우시안 닫힘 성질로 유도할 수 있다
- [ ] 네트워크가 무엇을 입력받아 무엇을 예측하도록 학습되는지(노이즈 예측) 말할 수 있다
- [ ] 학습(임의의 $t$ 한 스텝)과 샘플링(전 스텝 역방향)의 비대칭을 설명할 수 있다
- [ ] VAE·GAN 대비 디퓨전이 무엇을 얻고 무엇을 지불했는지(학습 안정성 vs 샘플링 비용) 말할 수 있다
