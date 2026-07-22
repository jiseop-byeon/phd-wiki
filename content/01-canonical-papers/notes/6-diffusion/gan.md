---
title: "GAN — Generative Adversarial Networks"
authors: Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, Yoshua Bengio
affiliation: Université de Montréal
venue: NeurIPS
year: 2014
arxiv: https://arxiv.org/abs/1406.2661
pdf: https://arxiv.org/pdf/1406.2661
tags: [paper, generative]
status: to-read
---

**Goodfellow et al., NeurIPS 2014** — [arXiv](https://arxiv.org/abs/1406.2661) · [PDF](https://arxiv.org/pdf/1406.2661)

> [!note] 수학 준비물 · Math on-ramp
> $\min_G \max_D$ 읽는 법: 안쪽 $\max_D$를 먼저 고정된 $G$에 대한 "최선의 판별자"로 읽고, 바깥 $\min_G$는 그 최선의 판별자를 상대로 한 생성자 최적화로 읽어라 — 두 플레이어가 번갈아 움직이는 [[02-foundations/optimization|최적화]] 문제다. 기댓값 표기는 [[02-foundations/probability|확률 §2]].

## English

**One-line summary**: Train a generator against a discriminator in a minimax game — no likelihood, no Markov chain, just an adversary as the loss function; a decade of sharp-but-unstable generative modeling followed.

### Context

In 2014, generative models either required tractable likelihoods (restrictive
architectures) or expensive inference ([[vae|VAE]]'s bound, MCMC). Discriminative deep nets,
meanwhile, were excellent. The lateral move: what if a *classifier* supplies the training
signal for generation, replacing the likelihood entirely?

### Method

> [!tip] Key intuition
> Counterfeiter vs police: the generator $G$ maps noise to fake samples; the discriminator
> $D$ learns to tell fake from real; $G$ improves precisely by fooling the *current* $D$.
> The loss function is not fixed — it is a co-evolving neural network.

- Objective: $\min_G \max_D \; E_{x}[\log D(x)] + E_{z}[\log(1 - D(G(z)))]$.
- Theory: at optimum, the game minimizes the Jensen–Shannon divergence between real and
  generated distributions; the paper proves $p_g = p_{data}$ at the (idealized) equilibrium.
- Practical trick from day one: train $G$ to maximize $\log D(G(z))$ instead (non-saturating
  loss) to keep gradients alive early.
- Sampling is one forward pass — no chain, no inference network.

### Results

- Plausible samples on MNIST/TFD/CIFAR-10 — visibly sharper than likelihood-based
  contemporaries, if unstable to train.
- Established that a learned adversary is a viable substitute for an explicit density.

### Limitations & critique

- **Training instability** and **mode collapse** are structural, not incidental — a decade of
  fixes followed (DCGAN, WGAN, spectral norm, StyleGAN's engineering).
- No likelihood ⇒ evaluation is fraught (FID etc. are proxies with known blind spots).
- The minimax equilibrium of the theory is rarely what SGD actually finds.

### Impact & follow-ups

Dominated image generation until ~2021 (StyleGAN2's faces, pix2pix/CycleGAN translation),
then ceded the frontier to [[ddpm|diffusion]] — which trades the adversarial game for a
stable regression loss. The adversarial *idea* survives everywhere: GAN losses sharpen VAE
decoders (VQGAN — inside [[01-canonical-papers/canonical-list|Latent Diffusion]]), and
adversarial training frames robustness research.

### Connections

- Contrast: [[vae|VAE]] (stable, blurry) vs GAN (sharp, unstable) — [[ddpm|DDPM]] resolves the tension
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 생성기를 판별기와의 minimax 게임으로 학습 — 우도도, 마르코프 체인도 없이 적대자가 곧 손실함수다; 선명하지만 불안정한 생성 모델링의 10년이 여기서 시작됐다.

### 배경

2014년의 생성 모델은 계산 가능한 우도(제한된 구조)를 요구하거나 비싼 추론([[vae|VAE]]의
하한, MCMC)을 요구했다. 반면 판별용 심층망은 이미 훌륭했다. 옆으로 비껴간 발상:
*분류기*가 생성의 학습 신호를 공급하게 해서 우도를 통째로 대체하면 어떨까?

### 방법

> [!tip] 핵심 직관
> 위조범 대 경찰: 생성기 $G$는 노이즈를 가짜 샘플로 사상하고, 판별기 $D$는 진짜와 가짜를
> 구별하도록 학습하며, $G$는 정확히 *현재의* $D$를 속이는 방향으로 개선된다.
> 손실함수가 고정되어 있지 않다 — 함께 진화하는 신경망이다.

- 목적함수: $\min_G \max_D \; E_{x}[\log D(x)] + E_{z}[\log(1 - D(G(z)))]$
- 이론: 최적점에서 이 게임은 실제 분포와 생성 분포 사이의 Jensen–Shannon 발산을 최소화하며,
  (이상화된) 균형에서 $p_g = p_{data}$임을 증명.
- 첫날부터 쓰인 실전 트릭: 초기 그래디언트를 살리기 위해 $G$는 $\log D(G(z))$ 최대화로 학습
  (non-saturating loss).
- 샘플링은 forward pass 한 번 — 체인도 추론망도 없다.

### 결과

- MNIST/TFD/CIFAR-10에서 그럴듯한 샘플 — 우도 기반 동시대 모델보다 눈에 띄게 선명하다,
  학습이 불안정하다는 대가와 함께.
- 학습된 적대자가 명시적 밀도의 유효한 대체물임을 확립.

### 한계와 비판

- **학습 불안정**과 **모드 붕괴**는 우연이 아니라 구조적이다 — 이후 10년간 수정의 역사가
  이어진다(DCGAN, WGAN, spectral norm, StyleGAN의 공학).
- 우도가 없다 ⇒ 평가가 어렵다(FID 등은 알려진 맹점이 있는 대리 지표).
- 이론의 minimax 균형은 SGD가 실제로 찾는 것과 거의 다르다.

### 영향과 후속 연구

~2021년까지 이미지 생성을 지배했고(StyleGAN2의 얼굴, pix2pix/CycleGAN 변환), 이후
최전선을 [[ddpm|디퓨전]]에 내줬다 — 적대적 게임을 안정적인 회귀 손실로 맞바꾼 것이
디퓨전이다. 적대적 *아이디어* 자체는 도처에 살아 있다: GAN 손실이 VAE 디코더를 선명하게
만들고(VQGAN — [[01-canonical-papers/canonical-list|Latent Diffusion]] 내부), 적대적 학습은
강건성 연구의 틀이다.

### 연결

- 대비: [[vae|VAE]] (안정, 흐릿) vs GAN (선명, 불안정) — 이 긴장을 [[ddpm|DDPM]]이 해소한다
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] minimax 게임에서 손실함수가 함께 진화한다는 것의 의미를 말할 수 있다
- [ ] 불안정과 모드 붕괴가 구조적인 이유를 말할 수 있다
- [ ] 디퓨전이 무엇을 맞바꿔 GAN을 대체했는지 말할 수 있다
