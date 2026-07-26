---
title: "VAE — Auto-Encoding Variational Bayes"
authors: Diederik P. Kingma, Max Welling
affiliation: University of Amsterdam
venue: ICLR
year: 2014
arxiv: https://arxiv.org/abs/1312.6114
pdf: https://arxiv.org/pdf/1312.6114
tags: [paper, generative]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Kingma & Welling, ICLR 2014** — [arXiv](https://arxiv.org/abs/1312.6114) · [PDF](https://arxiv.org/pdf/1312.6114)

> [!note] 수학 준비물 · Math on-ramp
> [[02-foundations/information-theory|정보이론 §5]]의 ELBO 유도(옌센 부등식)와 [[02-foundations/calculus-backprop|미적분 §5]]의 stop-gradient/샘플링 문제를 먼저 보라 — 이 논문의 두 기여(ELBO, reparameterization)가 정확히 그 두 지점의 해답이다.

## English

**One-line summary**: Make latent-variable inference trainable by backprop — an encoder amortizes posterior inference, the reparameterization trick lets gradients flow through sampling, and the ELBO ties it together.

### Context

Latent-variable generative models $p(x) = \int p(x|z)p(z)dz$ are attractive (compressed
representations, principled likelihoods) but the posterior $p(z|x)$ is intractable for
neural likelihoods. Classical variational inference optimized per-datapoint; MCMC didn't
scale. The 2013 question: can *one neural network* learn to do inference for all datapoints
at once, trained jointly with the generator?

### Method

> [!tip] Key intuition
> Two ideas: (1) **amortize** — train an encoder $q_\phi(z|x)$ that outputs the approximate
> posterior in one forward pass; (2) **reparameterize** — write $z = \mu + \sigma \odot \epsilon$,
> $\epsilon \sim \mathcal{N}(0,I)$, so the randomness is an *input* and gradients pass through
> $\mu, \sigma$.

- Maximize the **ELBO** (evidence lower bound):
  $\log p(x) \ge E_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x)\,\|\,p(z))$
  — reconstruction term + regularizer pulling the posterior toward the prior.
- Encoder and decoder are neural nets trained end-to-end with SGD on the ELBO.
- Gaussian prior/posterior make the KL term closed-form.

### Results

- Trained on MNIST/Frey faces: coherent samples, smooth interpolatable latent spaces, and
  likelihood competitive with contemporary methods — with a *single* SGD-trainable objective.
- Amortized inference: encoding a new datapoint costs one forward pass.

### Limitations & critique

- Samples are characteristically **blurry**: Gaussian likelihood + KL regularization trade
  sharpness for coverage.
- Posterior collapse: with powerful decoders the latent can be ignored.
- The ELBO is a lower bound — how loose it is went unquantified for years.

### Impact & follow-ups

The ELBO + reparameterization toolkit became load-bearing infrastructure: [[ddpm|DDPM]]'s
training objective *is* a VAE-style variational bound over a fixed noising chain; VQ-VAE
tokenizers feed autoregressive and diffusion models ([[01-canonical-papers/notes/6-diffusion/latent-diffusion|Latent Diffusion]]
runs diffusion inside a VAE's latent space); world models (Dreamer line) learn latent
dynamics with exactly these tools.

### Connections

- Contrast: [[gan|GAN]] (sharp samples, no likelihood) · Next: [[ddpm|DDPM]] (a deep VAE with fixed encoder)
- Foundations: [[02-foundations/probability|probability]] (Bayes, MLE)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 잠재변수 추론을 역전파로 학습 가능하게 만든 논문 — 인코더가 사후분포 추론을 상각(amortize)하고, reparameterization 트릭이 샘플링을 통과하는 그래디언트를 허용하며, ELBO가 이 전부를 하나의 목적함수로 묶는다.

### 배경

잠재변수 생성 모델 $p(x) = \int p(x|z)p(z)dz$은 매력적이지만(압축된 표현, 원리적인 우도),
신경망 우도에서 사후분포 $p(z|x)$는 계산 불가능하다. 고전 변분 추론은 데이터포인트마다
따로 최적화했고 MCMC는 스케일되지 않았다. 2013년의 질문: *하나의 신경망*이 모든
데이터포인트의 추론을 한 번에 배우면서, 생성기와 동시에 학습될 수 있을까?

### 방법

> [!tip] 핵심 직관
> 두 아이디어: (1) **상각** — 근사 사후분포를 forward pass 한 번에 출력하는 인코더
> $q_\phi(z|x)$를 학습하라. (2) **재매개변수화** — $z = \mu + \sigma \odot \epsilon$,
> $\epsilon \sim \mathcal{N}(0,I)$로 쓰면 무작위성이 *입력*이 되고, 그래디언트가 $\mu, \sigma$를
> 통과해 흐른다.

- **ELBO**(증거 하한)를 최대화:
  $\log p(x) \ge E_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x)\,\|\,p(z))$
  — 복원 항 + 사후분포를 사전분포 쪽으로 당기는 정규화 항.
- 인코더와 디코더는 ELBO에 대해 SGD로 end-to-end 학습되는 신경망.
- 가우시안 사전/사후분포를 쓰면 KL 항이 닫힌 형태가 된다.

### 결과

- MNIST/Frey faces에서: 일관된 샘플, 부드럽게 보간되는 잠재 공간, 당대 기법과 경쟁하는
  우도 — *단 하나의* SGD 학습 가능한 목적함수로.
- 상각된 추론: 새 데이터포인트의 인코딩 비용은 forward pass 한 번.

### 한계와 비판

- 샘플이 특징적으로 **흐릿하다**: 가우시안 우도 + KL 정규화가 선명함을 커버리지와 맞바꾼다.
- 사후분포 붕괴: 디코더가 강력하면 잠재변수가 무시될 수 있다.
- ELBO는 하한일 뿐 — 얼마나 느슨한지는 오랫동안 정량화되지 않았다.

### 영향과 후속 연구

ELBO + reparameterization 도구 상자는 하중을 받치는 인프라가 됐다: [[ddpm|DDPM]]의 학습
목적함수는 고정된 노이즈 체인 위의 VAE식 변분 하한*이고*, VQ-VAE 토크나이저는 자기회귀·
디퓨전 모델에 공급되며([[01-canonical-papers/notes/6-diffusion/latent-diffusion|Latent Diffusion]]은 VAE의 잠재 공간
안에서 디퓨전을 돌린다), 월드모델(Dreamer 계열)은 정확히 이 도구들로 잠재 동역학을 학습한다.

### 연결

- 대비: [[gan|GAN]] (선명한 샘플, 우도 없음) · 다음: [[ddpm|DDPM]] (인코더가 고정된 깊은 VAE)
- 기초: [[02-foundations/probability|확률]] (베이즈, MLE)
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] State the role of the ELBO's two terms (reconstruction and regularization) · ELBO 두 항(복원/정규화)의 역할을 말할 수 있다
- [ ] Explain the problem reparameterization solves (backpropagating through sampling) · reparameterization이 푸는 문제(샘플링 통과 역전파)를 설명할 수 있다
- [ ] Name the causes of blurriness (Gaussian likelihood plus KL) · 흐릿함의 원인(가우시안 우도 + KL)을 말할 수 있다
- [ ] Identify where the ELBO machinery is reused in DDPM and world models · ELBO 기계장치가 DDPM·월드모델에서 재사용되는 지점을 말할 수 있다
