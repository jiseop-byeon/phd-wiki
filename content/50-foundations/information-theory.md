---
title: Information Theory
tags: [foundations]
---

## English

Everything in deep learning that involves a probability distribution eventually speaks
information theory: cross-entropy loss, KL divergence, the ELBO, contrastive learning,
even "perplexity." This page is the complete working set for reading modern papers —
no prior background assumed.

### 1. Surprise and entropy

- **Surprise** of an outcome: $-\log p(x)$. Rare events carry more information (a sensor
  reading you predicted perfectly tells you nothing).
- **Entropy** = expected surprise:
  $H(p) = -\sum_x p(x)\log p(x)$
  — how unpredictable a source is, in bits (log base 2) or nats (log base e).
  Uniform distribution = maximum entropy; deterministic = zero.
- Intuition anchor: entropy is the average number of yes/no questions needed to identify
  an outcome — the *compression limit* of the source (Shannon).

### 2. Cross-entropy — the loss function you already use

- $H(p, q) = -\sum_x p(x)\log q(x)$: the cost of encoding data from true distribution $p$
  using a code optimized for your model $q$.
- Classification training: $p$ = one-hot label, $q$ = softmax output ⇒
  cross-entropy loss $= -\log q(\text{correct class})$. **Minimizing cross-entropy = MLE**
  (see [[50-foundations/probability|probability]]).
- Language models: per-token cross-entropy is *the* pretraining objective
  ([[canonical-papers/notes/gpt-3|GPT-3]]); **perplexity** $= e^{H(p,q)}$ — "the model is as
  confused as if choosing among perplexity-many options."

### 3. KL divergence — the distance-that-isn't

- $D_{KL}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$
  — the *extra* bits paid for using $q$ when the truth is $p$.
- **Non-negativity, proved in two lines** (Jensen's inequality — $\log$ is concave):
  $$-D_{KL}(p\|q) = E_p\Big[\log\frac{q}{p}\Big] \le \log E_p\Big[\frac{q}{p}\Big] = \log \sum_x q(x) = 0$$
  Equality iff $p = q$. This tiny proof powers the ELBO's validity and half of learning theory.
- **Gaussian KL, closed form** (the formula inside every VAE implementation): for
  $\mathcal{N}(\mu_1,\sigma_1^2)$ vs $\mathcal{N}(\mu_2,\sigma_2^2)$:
  $$D_{KL} = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac12$$
  Against a standard normal prior ($\mu_2=0, \sigma_2=1$) this is the exact regularizer
  term coded in [[canonical-papers/notes/vae|VAE]] losses.
- Properties that matter: $\ge 0$, zero iff $p = q$, and **asymmetric** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$ true, fit $q$): mode-**covering** — $q$ spreads to cover all of $p$'s mass.
  - Reverse KL (used in variational inference): mode-**seeking** — $q$ locks onto one mode.
  This asymmetry explains VAE blurriness and why RL-style objectives collapse to narrow behaviors.
- Where you've seen it:
  - [[canonical-papers/notes/vae|VAE]]: the ELBO's regularizer $D_{KL}(q_\phi(z|x)\,\|\,p(z))$.
  - [[canonical-papers/notes/instructgpt|InstructGPT/RLHF]]: per-token KL penalty keeping the
    policy near the SFT model — literally "don't drift too many bits from the reference."
  - [[canonical-papers/notes/ddpm|DDPM]]: the variational bound is a sum of KL terms between
    Gaussians (which is why it collapses to MSE).
  - Knowledge distillation: student minimizes KL to teacher's soft labels.

### 4. Mutual information

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — how many bits knowing $Y$ tells you about $X$; zero iff independent.
- **InfoNCE / contrastive learning** ([[canonical-papers/notes/clip|CLIP]]'s objective) is a
  lower bound on mutual information between views/modalities — "maximize what the image
  embedding tells you about the text embedding." Written out for a batch of $N$ pairs with
  similarity $s(\cdot,\cdot)$ and temperature $\tau$:
  $$\mathcal{L} = -\frac1N\sum_i \log\frac{e^{s(x_i,y_i)/\tau}}{\sum_j e^{s(x_i,y_j)/\tau}}$$
  — cross-entropy where "the classes" are the other samples in the batch; it satisfies
  $I(X;Y) \ge \log N - \mathcal{L}$, so bigger batches permit tighter bounds (why CLIP
  used batch size 32k).
- Representation learning framings (information bottleneck): keep what predicts the label,
  discard the rest — compression as a theory of generalization.

### 5. The ELBO, derived honestly

Goal: maximize $\log p_\theta(x)$, intractable because of the latent $z$. Introduce any
distribution $q(z|x)$ and use Jensen's inequality:

$$\log p_\theta(x) = \log \int p_\theta(x|z)p(z)\,dz \ge E_{q}[\log p_\theta(x|z)] - D_{KL}(q(z|x)\,\|\,p(z))$$

The gap between the two sides is exactly $D_{KL}(q(z|x)\,\|\,p_\theta(z|x))$ — so maximizing
the ELBO simultaneously (1) raises the likelihood bound and (2) pulls $q$ toward the true
posterior. Every VAE, diffusion, and world-model paper writes some version of this line.

### 6. Quick reference table

| Quantity | Formula | Deep learning role |
|---|---|---|
| Entropy $H(p)$ | $-E_p[\log p]$ | uncertainty; exploration bonuses in RL |
| Cross-entropy $H(p,q)$ | $-E_p[\log q]$ | the classification/LM loss |
| KL $D_{KL}(p\|q)$ | $E_p[\log p/q]$ | VAE regularizer, RLHF penalty, distillation |
| Mutual info $I(X;Y)$ | $H(X)-H(X|Y)$ | contrastive learning (CLIP), info bottleneck |
| Perplexity | $e^{H(p,q)}$ | LM evaluation |
| ELBO | $E_q[\log p(x|z)] - D_{KL}(q\|p)$ | VAE/diffusion/world-model training |

## 한국어

딥러닝에서 확률 분포가 등장하는 모든 것은 결국 정보이론의 언어로 말한다: 교차 엔트로피
손실, KL divergence, ELBO, 대조학습, 심지어 "perplexity"까지. 이 페이지는 최신 논문을
읽는 데 필요한 전부를 사전지식 없이 따라올 수 있게 담았다.

### 1. 놀라움과 엔트로피

- 사건의 **놀라움**: $-\log p(x)$. 드문 사건일수록 정보가 많다 (완벽히 예측한 센서 값은
  아무것도 알려주지 않는다).
- **엔트로피** = 놀라움의 기댓값:
  $H(p) = -\sum_x p(x)\log p(x)$
  — 소스가 얼마나 예측 불가능한가를 비트(밑 2) 또는 나트(밑 e)로 잰 것.
  균등 분포 = 최대 엔트로피; 결정론적 = 0.
- 직관의 닻: 엔트로피는 결과 하나를 알아내는 데 필요한 예/아니오 질문의 평균 개수 —
  그 소스의 *압축 한계*다 (섀넌).

### 2. 교차 엔트로피 — 이미 쓰고 있는 그 손실함수

- $H(p, q) = -\sum_x p(x)\log q(x)$: 진짜 분포가 $p$인 데이터를, 내 모델 $q$에 최적화된
  부호로 인코딩할 때의 비용.
- 분류 학습: $p$ = 원-핫 라벨, $q$ = 소프트맥스 출력 ⇒ 교차 엔트로피 손실
  $= -\log q(\text{정답 클래스})$. **교차 엔트로피 최소화 = MLE**
  ([[50-foundations/probability|확률]] 참고).
- 언어모델: 토큰별 교차 엔트로피가 사전학습 목적함수 *그 자체*다
  ([[canonical-papers/notes/gpt-3|GPT-3]]); **perplexity** $= e^{H(p,q)}$ — "모델이
  perplexity개의 선택지 사이에서 고민하는 것만큼 헷갈려 한다."

### 3. KL divergence — 거리 같지만 거리가 아닌 것

- $D_{KL}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$
  — 진실이 $p$인데 $q$를 썼을 때 *추가로* 내는 비트.
- **비음수성, 두 줄 증명** (옌센 부등식 — $\log$는 오목):
  $$-D_{KL}(p\|q) = E_p\Big[\log\frac{q}{p}\Big] \le \log E_p\Big[\frac{q}{p}\Big] = \log \sum_x q(x) = 0$$
  등호는 $p = q$일 때만. 이 작은 증명이 ELBO의 유효성과 학습 이론의 절반을 떠받친다.
- **가우시안 KL의 닫힌 형태** (모든 VAE 구현 속의 그 공식):
  $\mathcal{N}(\mu_1,\sigma_1^2)$ vs $\mathcal{N}(\mu_2,\sigma_2^2)$에 대해:
  $$D_{KL} = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac12$$
  표준 정규 사전($\mu_2=0, \sigma_2=1$)에 대한 이 식이 [[canonical-papers/notes/vae|VAE]]
  손실에 코딩되는 정규화 항 그 자체다.
- 중요한 성질: $\ge 0$, $p = q$일 때만 0, 그리고 **비대칭** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$가 참, $q$를 적합): 모드 **커버링** — $q$가 $p$의 질량 전체를 덮으려 퍼진다.
  - Reverse KL (변분 추론에서 사용): 모드 **시킹** — $q$가 한 모드에 들러붙는다.
  이 비대칭이 VAE의 흐릿함과, RL식 목적함수가 좁은 행동으로 붕괴하는 이유를 설명한다.
- 이미 만난 곳들:
  - [[canonical-papers/notes/vae|VAE]]: ELBO의 정규화 항 $D_{KL}(q_\phi(z|x)\,\|\,p(z))$
  - [[canonical-papers/notes/instructgpt|InstructGPT/RLHF]]: 정책을 SFT 모델 근처에 붙잡는
    토큰별 KL 페널티 — 말 그대로 "기준에서 너무 많은 비트만큼 벗어나지 마라".
  - [[canonical-papers/notes/ddpm|DDPM]]: 변분 하한이 가우시안 사이 KL 항들의 합이다
    (그래서 MSE로 접힌다).
  - 지식 증류: 학생이 교사의 소프트 라벨에 대한 KL을 최소화.

### 4. 상호 정보량

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — $Y$를 알면 $X$에 대해 몇 비트를 알게 되는가; 독립일 때만 0.
- **InfoNCE / 대조학습** ([[canonical-papers/notes/clip|CLIP]]의 목적함수)은 뷰/모달리티 간
  상호 정보량의 하한이다 — "이미지 임베딩이 텍스트 임베딩에 대해 알려주는 양을 최대화하라."
  유사도 $s(\cdot,\cdot)$와 온도 $\tau$, $N$쌍 배치에 대해 써보면:
  $$\mathcal{L} = -\frac1N\sum_i \log\frac{e^{s(x_i,y_i)/\tau}}{\sum_j e^{s(x_i,y_j)/\tau}}$$
  — "클래스"가 배치 안의 다른 샘플들인 교차 엔트로피다; $I(X;Y) \ge \log N - \mathcal{L}$을
  만족하므로 배치가 클수록 더 빡빡한 하한이 가능하다 (CLIP이 배치 32k를 쓴 이유).
- 표현 학습의 틀(information bottleneck): 라벨을 예측하는 것만 남기고 버려라 —
  압축을 일반화의 이론으로 보는 관점.

### 5. ELBO, 정직하게 유도하기

목표: $\log p_\theta(x)$ 최대화 — 잠재변수 $z$ 때문에 계산 불가. 아무 분포 $q(z|x)$나
도입하고 옌센 부등식을 쓰면:

$$\log p_\theta(x) = \log \int p_\theta(x|z)p(z)\,dz \ge E_{q}[\log p_\theta(x|z)] - D_{KL}(q(z|x)\,\|\,p(z))$$

양변의 간극이 정확히 $D_{KL}(q(z|x)\,\|\,p_\theta(z|x))$다 — 그래서 ELBO 최대화는 동시에
(1) 우도 하한을 올리고 (2) $q$를 진짜 사후분포로 끌어당긴다. 모든 VAE·디퓨전·월드모델
논문이 이 한 줄의 어떤 버전을 쓰고 있다.

### 6. 빠른 참조 표

| 양 | 공식 | 딥러닝에서의 역할 |
|---|---|---|
| 엔트로피 $H(p)$ | $-E_p[\log p]$ | 불확실성; RL의 탐험 보너스 |
| 교차 엔트로피 $H(p,q)$ | $-E_p[\log q]$ | 분류/언어모델 손실 |
| KL $D_{KL}(p\|q)$ | $E_p[\log p/q]$ | VAE 정규화, RLHF 페널티, 증류 |
| 상호 정보량 $I(X;Y)$ | $H(X)-H(X|Y)$ | 대조학습(CLIP), 정보 병목 |
| Perplexity | $e^{H(p,q)}$ | 언어모델 평가 |
| ELBO | $E_q[\log p(x|z)] - D_{KL}(q\|p)$ | VAE/디퓨전/월드모델 학습 |
