---
title: 5. Information Theory
tags: [foundations]
study-depth: Literacy
depth-goal: "Read the notation and recurring ideas accurately; return for deeper derivations when a paper requires them."
mastery-when: "Raise to Working or Mastery when the thesis objective depends directly on these formulations."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §6]] (log rules — §0 below re-states them) · [[02-foundations/probability|3. Probability §1–2]] (distributions, expectation)
> [[02-foundations/engineering-math|0.5 §6]](로그 규칙 — 아래 §0이 다시 정리한다) · [[02-foundations/probability|3. 확률 §1–2]](분포·기댓값)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/probability|3. Probability]] and the logs from [[02-foundations/engineering-math|0.5]]. Second applied pillar: it names what those objectives all measure,
which is that cross-entropy is maximum likelihood is KL.*

Everything in deep learning that involves a probability distribution eventually speaks
information theory: cross-entropy loss, KL divergence, the ELBO, contrastive learning,
even "perplexity." This page is the complete working set for reading modern papers —
no prior background assumed.

### 0. Prerequisite: the three log rules

Everything on this page runs on logarithms. If these three lines are not second nature,
read [[02-foundations/engineering-math|0.5 Engineering Math §6]] first (5 minutes):
$\log(ab) = \log a + \log b$ (products of probabilities become sums — why losses are sums);
$\log(a^n) = n \log a$; and base 2 vs base $e$ only changes units (**bits** vs **nats**) by
a constant factor. Also remember: probabilities live in $[0,1]$, so log-probabilities are
$\le 0$ — a "smaller cross-entropy" means log-probs closer to zero.

### 1. Surprise and entropy

- **Surprise** of an outcome: $-\log p(x)$. Rare events carry more information (a sensor
  reading you predicted perfectly tells you nothing).
- **Entropy** = expected surprise:
  $H(p) = -\sum_x p(x)\log p(x)$
  — how unpredictable a source is, in bits (log base 2) or nats (log base e).
  Uniform distribution = maximum entropy; deterministic = zero.
- Intuition anchor: entropy is the average number of yes/no questions needed to identify
  an outcome — the *compression limit* of the source (Shannon).
- **Worked numbers** — a coin with $P(\text{H}) = 0.9$:
  $H = -0.9\log_2 0.9 - 0.1\log_2 0.1 = 0.9(0.152) + 0.1(3.322) \approx 0.47$ bits —
  less than half the fair coin's 1 bit, because the outcome is mostly predictable.
  And the KL from this coin to a fair coin:
  $D_{KL} = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5} \approx 0.763 - 0.232 = 0.53$
  bits — the *extra* cost per toss of encoding the biased coin with the fair-coin code.
  Run these two computations by hand once; every formula on this page becomes concrete.

### 2. Cross-entropy — the loss function you already use

- $H(p, q) = -\sum_x p(x)\log q(x)$: the cost of encoding data from true distribution $p$
  using a code optimized for your model $q$.
- **Worked, in bits.** True $p = (0.7,\,0.2,\,0.1)$, model $q = (0.5,\,0.3,\,0.2)$.
  $$H(p) = -[0.7\log_2 0.7 + 0.2\log_2 0.2 + 0.1\log_2 0.1] = 1.157\ \text{bits}$$
  $$H(p,q) = -[0.7\log_2 0.5 + 0.2\log_2 0.3 + 0.1\log_2 0.2] = 1.280\ \text{bits}$$
  The model costs $1.280$ bits per symbol where $1.157$ was achievable — an overpayment of
  $0.123$ bits. Hold that number; §3 shows it is exactly the KL.
- Classification training: $p$ = one-hot label, $q$ = softmax output ⇒
<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="two bars of bits per symbol, the entropy floor and the longer cost of coding with the model, with the excess marked as the KL divergence">
  <g fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2">
    <rect x="90" y="34" width="231.4" height="26" rx="3"/>
    <rect x="90" y="76" width="231.4" height="26" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2">
    <rect x="321.4" y="76" width="24.6" height="26" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="3 3">
    <line x1="321.4" y1="28" x2="321.4" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="24" y="51">H(p) = 1.157 bits</text>
    <text x="24" y="93">H(p, q) = 1.280 bits</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="356" y="93">KL = 0.123</text>
    <text x="315" y="126" text-anchor="end">the floor &#8212; no code beats this</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="160">Entropy is a floor set by the data: no code, however clever, gets below 1.157 bits per symbol.</text>
    <text x="24" y="176">Your model&#8217;s code pays 1.280, and the excess is exactly the KL. So minimising cross-entropy is</text>
    <text x="24" y="192">minimising KL &#8212; the floor is a constant you do not control, and every bit of training progress is</text>
    <text x="24" y="208">the dark band getting narrower.</text>
  </g>
</svg>

  cross-entropy loss $= -\log q(\text{correct class})$. Every other term is multiplied by
  $p(x) = 0$ and vanishes — which is why the loss in code is a *single* log. If the model
  gives the correct class probability $0.5$, the loss is $-\log 0.5 = 0.693$ nats ($=1$ bit);
  at $0.9$ it is $0.105$; at $0.99$, $0.010$. The loss falls steeply at first and then barely
  moves — most of the training signal comes from examples the model still gets wrong.
  **Minimizing cross-entropy = MLE** (see [[02-foundations/probability|probability]]).
- Language models: per-token cross-entropy is *the* pretraining objective
  ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]); **perplexity** $= e^{H(p,q)}$ — "the model is as
  confused as if choosing among perplexity-many options."

### 3. KL divergence — the distance-that-isn't

- $D_{KL}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$
  — the *extra* bits paid for using $q$ when the truth is $p$.
- **Same numbers as §2, computed directly:**
  $$D_{KL} = 0.7\log_2\tfrac{0.7}{0.5} + 0.2\log_2\tfrac{0.2}{0.3} + 0.1\log_2\tfrac{0.1}{0.2} = 0.340 - 0.117 - 0.100 = 0.123\ \text{bits}$$
  — exactly $H(p,q) - H(p) = 1.280 - 1.157$. Two things become visible: individual terms
  **can be negative** (the middle one is), yet the total never is; and the total is zero only
  when $q = p$ everywhere.

<svg viewBox="0 0 480 120" style="max-width:100%;height:auto" role="img" aria-label="cross-entropy equals entropy plus KL">
  <g fill="currentColor" opacity="0.10"><rect x="30" y="74" width="105" height="30" transform="translate(180,0)"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <rect x="30" y="32" width="180" height="30" rx="3"/>
    <rect x="30" y="74" width="180" height="30" rx="3"/>
    <rect x="210" y="74" width="105" height="30" rx="3"/>
  </g>
  <g font-size="12.5" fill="currentColor" text-anchor="middle">
    <text x="120" y="52">H(p)</text><text x="120" y="94">H(p)</text><text x="262" y="94">KL(p‖q)</text>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="20" opacity="0.85">H(p, q)  =  H(p)  +  KL(p‖q)</text>
    <text x="228" y="52" opacity="0.8">the floor: no code can beat it</text>
    <text x="330" y="94" opacity="0.8">what q costs you extra</text>
  </g>
</svg>


- **Non-negativity, proved in two lines** (Jensen's inequality — $\log$ is concave):
  $$-D_{KL}(p\|q) = E_p\Big[\log\frac{q}{p}\Big] \le \log E_p\Big[\frac{q}{p}\Big] = \log \sum_x q(x) = 0$$
  Equality iff $p = q$. This tiny proof powers the ELBO's validity and half of learning theory.
- **Gaussian KL, closed form** (the formula inside every VAE implementation): for
  $\mathcal{N}(\mu_1,\sigma_1^2)$ vs $\mathcal{N}(\mu_2,\sigma_2^2)$:
  $$D_{KL} = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac12$$
  Against a standard normal prior ($\mu_2=0, \sigma_2=1$) this is the exact regularizer
  term coded in [[01-canonical-papers/notes/6-diffusion/vae|VAE]] losses.
- Properties that matter: $\ge 0$, zero iff $p = q$, and **asymmetric** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$ true, fit $q$): mode-**covering** — $q$ spreads to cover all of $p$'s mass.
  - Reverse KL (used in *variational inference* — approximating an intractable distribution
    by picking the closest member of a simple family): mode-**seeking** — $q$ locks onto one mode.
  This asymmetry contributes to VAEs' limited posterior coverage and to RL-style objectives
  collapsing to narrow behaviors — though classical VAE blur is *primarily* the Gaussian
  pixel likelihood averaging plausible outputs (see the self-check answer below).
- Where you've seen it:
  - [[01-canonical-papers/notes/6-diffusion/vae|VAE]]: the ELBO's regularizer $D_{KL}(q_\phi(z|x)\,\|\,p(z))$.
  - [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]]: per-token KL penalty keeping the
    policy near the SFT model — literally "don't drift too many bits from the reference."
  - [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]: the variational bound is a sum of KL terms between
    Gaussians (which is why it collapses to MSE).
  - Knowledge distillation: student minimizes KL to teacher's soft labels.

### 4. Mutual information

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — how many bits knowing $Y$ tells you about $X$; zero iff independent.
- **Worked, with the crack detector from [[02-foundations/probability|3. Probability §1]].**
  $X$ = crack present ($P = 0.01$), $Y$ = alarm fires, with $P(Y{=}1|X{=}1) = 0.95$ and
  $P(Y{=}1|X{=}0) = 0.05$. Then $P(Y{=}1) = 0.95(0.01) + 0.05(0.99) = 0.059$. Computing the
  four joint terms gives $I(X;Y) = 0.037$ bits, while $H(X) = 0.081$ bits. So the alarm
  removes **46% of the uncertainty** about whether a crack is there — informative, but
  nothing like "knowing." That single ratio is the honest version of the sentence
  "our sensor detects cracks with 95% accuracy": high sensitivity on a rare event still
  leaves most of the question open, which is the same fact Bayes' rule showed as
  $P(X|Y) = 0.16$.
- **InfoNCE / contrastive learning** ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]'s objective) is a
  lower bound on mutual information between views/modalities — "maximize what the image
  embedding tells you about the text embedding." Written out for a batch of $N$ pairs with
  similarity $s(\cdot,\cdot)$ and temperature $\tau$:
  $$\mathcal{L} = -\frac1N\sum_i \log\frac{e^{s(x_i,y_i)/\tau}}{\sum_j e^{s(x_i,y_j)/\tau}}$$
  — cross-entropy where "the classes" are the other samples in the batch; it satisfies
  $I(X;Y) \ge \log N - \mathcal{L}$, so bigger batches permit tighter bounds (why CLIP
  used batch size 32k). Caveat: how tight this MI bound is depends on the negative-sampling
  scheme and distributional assumptions — treat it as guiding intuition, not a guarantee.
- Representation learning framings (information bottleneck): keep what predicts the label,
  discard the rest — compression as a theory of generalization.

### 5. The ELBO, derived honestly

Goal: maximize $\log p_\theta(x)$, intractable because of the **latent** $z$ — a variable the
model uses but never observes (the "code" behind an image, the compressed state behind a
sensor stream); to get $p(x)$ you would have to integrate over every value it could take. The trick that
makes $q$ appear: multiply and divide the integrand by any distribution $q(z|x)$, which
turns the integral into an expectation over $q$ — then Jensen's inequality ($\log$ is
concave, so $\log E \ge E \log$) drops the log inside:

$$\log p_\theta(x) = \log E_{q}\!\left[\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \;\ge\; E_{q}\!\left[\log\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \quad\text{(Jensen)}$$

Now split that single log with $\log\frac{p(x|z)\,p(z)}{q} = \log p(x|z) + \log\frac{p(z)}{q}$
and take the expectation term by term — the first piece is the reconstruction term, the
second is *minus* a KL:

$$= \underbrace{E_{q}[\log p_\theta(x|z)]}_{\text{reconstruction}} \;+\; \underbrace{E_{q}\!\left[\log\frac{p(z)}{q(z|x)}\right]}_{-\,D_{KL}(q\,\|\,p(z))} \;=\; E_{q}[\log p_\theta(x|z)] - D_{KL}(q(z|x)\,\|\,p(z))$$

(the second expectation is $-E_q[\log\frac{q}{p(z)}]$, which is exactly $-D_{KL}(q\|p(z))$ by
its definition in §3.) The gap between the two sides is exactly $D_{KL}(q(z|x)\,\|\,p_\theta(z|x))$ — so maximizing
the ELBO simultaneously (1) raises the likelihood bound and (2) pulls $q$ toward the true
posterior. Many foundational VAE, diffusion, and latent world-model papers use this ELBO
or a closely related variational objective (though not all — flow matching and
non-variational world models take different routes).

### 6. Quick reference table

| Quantity | Formula | Deep learning role |
|---|---|---|
| Entropy $H(p)$ | $-E_p[\log p]$ | uncertainty; exploration bonuses in RL |
| Cross-entropy $H(p,q)$ | $-E_p[\log q]$ | the classification/LM loss |
| KL $D_{KL}(p\|q)$ | $E_p[\log p/q]$ | VAE regularizer, RLHF penalty, distillation |
| Mutual info $I(X;Y)$ | $H(X)-H(X|Y)$ | contrastive learning (CLIP), info bottleneck |
| Perplexity | $e^{H(p,q)}$ | LM evaluation |
| ELBO | $E_q[\log p(x|z)] - D_{KL}(q\|p)$ | VAE/diffusion/world-model training |

### Self-check

1. Compute the entropy of a coin with $P(\text{H}) = 0.99$, and say why it is smaller than the 0.9 coin's.
2. A classifier assigns probability 0.25 to the correct class. What is this sample's cross-entropy loss in nats?
3. How does using reverse KL (instead of forward KL) in a VAE connect to blurry samples?
4. In CLIP's InfoNCE, how much can doubling the batch size improve the mutual-information bound?

> [!tip]- Answers
> 1. $H = -0.99\log_2 0.99 - 0.01\log_2 0.01 \approx 0.08$ bits — the more predictable, the smaller the average surprise.
> 2. $-\ln 0.25 = \ln 4 \approx 1.39$ nats.
> 3. Reverse KL is mode-seeking — $q$ latches onto one mode. VAE blur is *primarily* the Gaussian likelihood (pixel averaging); the KL asymmetry pushes the latent toward covering only part of the posterior — together they yield conservative (average-like) samples.
> 4. $I \ge \log N - \mathcal{L}$, so the bound's ceiling rises by $\log 2 \approx 0.69$ nats (= 1 bit).

## 한국어

*[[02-foundations/probability|3. 확률]]과 [[02-foundations/engineering-math|0.5]]의 로그 위에 선다. 둘째 응용 기둥이고, 목적함수들이 공통으로 재는 것에
이름을 붙인다 — 교차 엔트로피가 곧 최대우도이고 곧 KL이다.*

딥러닝에서 확률 분포가 등장하는 모든 것은 결국 정보이론의 언어로 말한다: 교차 엔트로피
손실, KL divergence, ELBO, 대조학습, 심지어 "perplexity"까지. 이 페이지는 최신 논문을
읽는 데 필요한 전부를 사전지식 없이 따라올 수 있게 담았다.

### 0. 사전 준비: 로그의 세 규칙

이 페이지 전체가 로그로 굴러간다. 아래 세 줄이 자동으로 나오지 않으면
[[02-foundations/engineering-math|0.5 공업수학 §6]]을 먼저 읽어라 (5분이면 된다):
$\log(ab) = \log a + \log b$ (확률의 곱이 합이 된다 — 손실이 합인 이유);
$\log(a^n) = n \log a$; 그리고 밑 2와 밑 $e$는 단위(**비트** vs **나트**)만 상수배 바꾼다.
하나 더: 확률은 $[0,1]$에 살므로 로그 확률은 $\le 0$이다 — "교차 엔트로피가 작다" =
로그 확률이 0에 가깝다는 뜻.

### 1. 놀라움과 엔트로피

- 사건의 **놀라움**: $-\log p(x)$. 드문 사건일수록 정보가 많다 (완벽히 예측한 센서 값은
  아무것도 알려주지 않는다).
- **엔트로피** = 놀라움의 기댓값:
  $H(p) = -\sum_x p(x)\log p(x)$
  — 소스가 얼마나 예측 불가능한가를 비트(밑 2) 또는 나트(밑 e)로 잰 것.
  균등 분포 = 최대 엔트로피; 결정론적 = 0.
- 직관의 닻: 엔트로피는 결과 하나를 알아내는 데 필요한 예/아니오 질문의 평균 개수 —
  그 소스의 *압축 한계*다 (섀넌).
- **숫자로 한 번** — $P(\text{앞}) = 0.9$인 동전:
  $H = -0.9\log_2 0.9 - 0.1\log_2 0.1 \approx 0.47$ 비트 — 공정 동전(1비트)의 절반 이하다.
  결과가 대부분 예측 가능하기 때문. 이 동전과 공정 동전 사이의 KL:
  $D_{KL} = 0.9\log_2\frac{0.9}{0.5} + 0.1\log_2\frac{0.1}{0.5} \approx 0.53$ 비트 —
  편향 동전을 공정 동전용 부호로 인코딩할 때 토스당 내는 *추가* 비용이다.
  이 두 계산을 손으로 한 번 해 보라 — 이 페이지의 모든 공식이 구체화된다.

### 2. 교차 엔트로피 — 이미 쓰고 있는 그 손실함수

- $H(p, q) = -\sum_x p(x)\log q(x)$: 진짜 분포가 $p$인 데이터를, 내 모델 $q$에 최적화된
  부호로 인코딩할 때의 비용.
- **비트 단위 계산 예제.** 참분포 $p = (0.7,\,0.2,\,0.1)$, 모델 $q = (0.5,\,0.3,\,0.2)$.
  $$H(p) = -[0.7\log_2 0.7 + 0.2\log_2 0.2 + 0.1\log_2 0.1] = 1.157\ \text{비트}$$
  $$H(p,q) = -[0.7\log_2 0.5 + 0.2\log_2 0.3 + 0.1\log_2 0.2] = 1.280\ \text{비트}$$
  $1.157$이면 되는 자리에 모델이 심볼당 $1.280$비트를 치른다 — $0.123$비트를 더 낸 것이다.
  이 숫자를 기억해 두라. 3절에서 이것이 정확히 KL임을 보인다.
- 분류 학습: $p$ = 원-핫 라벨, $q$ = 소프트맥스 출력 ⇒ 교차 엔트로피 손실
<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="심볼당 비트 수를 나타내는 두 막대. 엔트로피 바닥과 모델의 부호가 치르는 더 긴 비용, 그 초과분이 KL로 표시되어 있다">
  <g fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2">
    <rect x="90" y="34" width="231.4" height="26" rx="3"/>
    <rect x="90" y="76" width="231.4" height="26" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="1.2">
    <rect x="321.4" y="76" width="24.6" height="26" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.45" stroke-dasharray="3 3">
    <line x1="321.4" y1="28" x2="321.4" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="24" y="51">H(p) = 1.157 비트</text>
    <text x="24" y="93">H(p, q) = 1.280 비트</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="356" y="93">KL = 0.123</text>
    <text x="315" y="126" text-anchor="end">바닥 &#8212; 어떤 부호도 이보다 낮출 수 없다</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="160">엔트로피는 데이터가 정하는 바닥이다: 아무리 영리한 부호도 심볼당 1.157비트 아래로 내려가지</text>
    <text x="24" y="176">못한다. 내 모델의 부호는 1.280을 치르고, 그 초과분이 정확히 KL이다. 그래서 교차 엔트로피를</text>
    <text x="24" y="192">줄이는 것이 곧 KL을 줄이는 것이다 &#8212; 바닥은 내가 건드릴 수 없는 상수이고, 학습의 진전은 전부</text>
    <text x="24" y="208">저 짙은 띠가 좁아지는 것이다.</text>
  </g>
</svg>

  $= -\log q(\text{정답 클래스})$. 나머지 항은 전부 $p(x) = 0$이 곱해져 사라진다 — 코드에서
  보는 손실이 로그 *하나*인 이유가 이것이다. 모델이 정답 클래스에 확률 $0.5$를 주면 손실은
  $-\log 0.5 = 0.693$ 나트($=1$비트), $0.9$면 $0.105$, $0.99$면 $0.010$이다. 손실이 처음엔
  가파르게 떨어지다 이후 거의 움직이지 않는다 — 학습 신호의 대부분은 모델이 아직 틀리는
  예제에서 온다. **교차 엔트로피 최소화 = MLE**
  ([[02-foundations/probability|확률]] 참고).
- 언어모델: 토큰별 교차 엔트로피가 사전학습 목적함수 *그 자체*다
  ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]); **perplexity** $= e^{H(p,q)}$ — "모델이
  perplexity개의 선택지 사이에서 고민하는 것만큼 헷갈려 한다."

### 3. KL divergence — 거리 같지만 거리가 아닌 것

- $D_{KL}(p\,\|\,q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)$
  — 진실이 $p$인데 $q$를 썼을 때 *추가로* 내는 비트.
- **2절과 같은 숫자를, 이번엔 직접 계산:**
  $$D_{KL} = 0.7\log_2\tfrac{0.7}{0.5} + 0.2\log_2\tfrac{0.2}{0.3} + 0.1\log_2\tfrac{0.1}{0.2} = 0.340 - 0.117 - 0.100 = 0.123\ \text{비트}$$
  — 정확히 $H(p,q) - H(p) = 1.280 - 1.157$이다. 두 가지가 눈에 보인다: 개별 항은 **음수가 될
  수 있지만**(가운데 항이 그렇다) 총합은 결코 음수가 되지 않으며, 총합이 0이 되는 것은 모든
  곳에서 $q = p$일 때뿐이다.

<svg viewBox="0 0 480 120" style="max-width:100%;height:auto" role="img" aria-label="교차 엔트로피 = 엔트로피 + KL">
  <g fill="currentColor" opacity="0.10"><rect x="30" y="74" width="105" height="30" transform="translate(180,0)"/></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <rect x="30" y="32" width="180" height="30" rx="3"/>
    <rect x="30" y="74" width="180" height="30" rx="3"/>
    <rect x="210" y="74" width="105" height="30" rx="3"/>
  </g>
  <g font-size="12.5" fill="currentColor" text-anchor="middle">
    <text x="120" y="52">H(p)</text><text x="120" y="94">H(p)</text><text x="262" y="94">KL(p‖q)</text>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="20" opacity="0.85">H(p, q)  =  H(p)  +  KL(p‖q)</text>
    <text x="228" y="52" opacity="0.8">바닥: 어떤 부호도 이보다 낮출 수 없다</text>
    <text x="330" y="94" opacity="0.8">q를 써서 더 내는 비용</text>
  </g>
</svg>


- **비음수성, 두 줄 증명** (옌센 부등식 — $\log$는 오목):
  $$-D_{KL}(p\|q) = E_p\Big[\log\frac{q}{p}\Big] \le \log E_p\Big[\frac{q}{p}\Big] = \log \sum_x q(x) = 0$$
  등호는 $p = q$일 때만. 이 작은 증명이 ELBO의 유효성과 학습 이론의 절반을 떠받친다.
- **가우시안 KL의 닫힌 형태** (모든 VAE 구현 속의 그 공식):
  $\mathcal{N}(\mu_1,\sigma_1^2)$ vs $\mathcal{N}(\mu_2,\sigma_2^2)$에 대해:
  $$D_{KL} = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1-\mu_2)^2}{2\sigma_2^2} - \frac12$$
  표준 정규 사전($\mu_2=0, \sigma_2=1$)에 대한 이 식이 [[01-canonical-papers/notes/6-diffusion/vae|VAE]]
  손실에 코딩되는 정규화 항 그 자체다.
- 중요한 성질: $\ge 0$, $p = q$일 때만 0, 그리고 **비대칭** — $D_{KL}(p\|q) \ne D_{KL}(q\|p)$.
  - Forward KL ($p$가 참, $q$를 적합): 모드 **커버링** — $q$가 $p$의 질량 전체를 덮으려 퍼진다.
  - Reverse KL(*변분 추론*에서 사용 — 계산 불가능한 분포를, 다루기 쉬운 분포 가족 중
    가장 가까운 것으로 근사하는 방법): 모드 **시킹** — $q$가 한 모드에 들러붙는다.
  이 비대칭은 VAE의 제한적 사후분포 커버리지와 RL식 목적함수가 좁은 행동으로 붕괴하는
  현상에 기여한다 — 단 고전적 VAE 흐릿함의 *주원인*은 가우시안 픽셀 우도의 평균화다
  (아래 스스로 점검 정답 참고).
- 이미 만난 곳들:
  - [[01-canonical-papers/notes/6-diffusion/vae|VAE]]: ELBO의 정규화 항 $D_{KL}(q_\phi(z|x)\,\|\,p(z))$
  - [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]]: 정책을 SFT 모델 근처에 붙잡는
    토큰별 KL 페널티 — 말 그대로 "기준에서 너무 많은 비트만큼 벗어나지 마라".
  - [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]: 변분 하한이 가우시안 사이 KL 항들의 합이다
    (그래서 MSE로 접힌다).
  - 지식 증류: 학생이 교사의 소프트 라벨에 대한 KL을 최소화.

### 4. 상호 정보량

- $I(X;Y) = D_{KL}(p(x,y)\,\|\,p(x)p(y)) = H(X) - H(X|Y)$
  — $Y$를 알면 $X$에 대해 몇 비트를 알게 되는가; 독립일 때만 0.
- **[[02-foundations/probability|3. 확률 §1]]의 균열 감지기로 계산해 보면.**
  $X$ = 균열 있음($P = 0.01$), $Y$ = 경보 울림, $P(Y{=}1|X{=}1) = 0.95$,
  $P(Y{=}1|X{=}0) = 0.05$. 그러면 $P(Y{=}1) = 0.95(0.01) + 0.05(0.99) = 0.059$이고, 네 개의
  결합 항을 계산하면 $I(X;Y) = 0.037$비트, 한편 $H(X) = 0.081$비트다. 즉 경보는 균열 유무에
  대한 불확실성 중 **46퍼센트**를 없앤다 — 정보가 있긴 하지만 "안다"와는 거리가 멀다. 이 비 하나가
  "우리 센서는 95% 정확도로 균열을 감지한다"는 문장의 정직한 판본이다: 희귀 사건에 대한 높은
  민감도는 여전히 질문의 대부분을 열어둔 채로 남기고, 베이즈 정리가 $P(X|Y) = 0.16$으로 보여준
  것과 같은 사실이다.
- **InfoNCE / 대조학습** ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 목적함수)은 뷰/모달리티 간
  상호 정보량의 하한이다 — "이미지 임베딩이 텍스트 임베딩에 대해 알려주는 양을 최대화하라."
  유사도 $s(\cdot,\cdot)$와 온도 $\tau$, $N$쌍 배치에 대해 써보면:
  $$\mathcal{L} = -\frac1N\sum_i \log\frac{e^{s(x_i,y_i)/\tau}}{\sum_j e^{s(x_i,y_j)/\tau}}$$
  — "클래스"가 배치 안의 다른 샘플들인 교차 엔트로피다; $I(X;Y) \ge \log N - \mathcal{L}$을
  만족하므로 배치가 클수록 더 빡빡한 하한이 가능하다 (CLIP이 배치 32k를 쓴 이유).
  단서: 이 상호 정보량 하한이 얼마나 빡빡한지는 음성 샘플링 방식과 분포 가정에 의존한다 —
  보장이 아니라 안내하는 직관으로 읽어라.
- 표현 학습의 틀(information bottleneck): 라벨을 예측하는 것만 남기고 버려라 —
  압축을 일반화의 이론으로 보는 관점.

### 5. ELBO, 정직하게 유도하기

목표: $\log p_\theta(x)$ 최대화 — **잠재변수(latent)** $z$ 때문에 계산 불가. 잠재변수란
모델이 쓰지만 관측되지는 않는 변수다(이미지 뒤의 "코드", 센서 스트림 뒤의 압축된 상태).
$p(x)$를 얻으려면 $z$가 가질 수 있는 모든 값에 대해 적분해야 한다. $q$가 등장하는 트릭:
적분 안을 아무 분포 $q(z|x)$로 곱하고 나눠 $q$에 대한 기댓값으로 바꾼 뒤, 옌센
부등식($\log$은 오목이므로 $\log E \ge E \log$)으로 로그를 안으로 떨어뜨린다:

$$\log p_\theta(x) = \log E_{q}\!\left[\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \;\ge\; E_{q}\!\left[\log\frac{p_\theta(x|z)p(z)}{q(z|x)}\right] \quad\text{(옌센)}$$

이제 그 로그 하나를 $\log\frac{p(x|z)\,p(z)}{q} = \log p(x|z) + \log\frac{p(z)}{q}$로 쪼개고
항별로 기댓값을 취하면 — 첫 조각은 재구성 항, 둘째는 *마이너스* KL이다:

$$= \underbrace{E_{q}[\log p_\theta(x|z)]}_{\text{재구성}} \;+\; \underbrace{E_{q}\!\left[\log\frac{p(z)}{q(z|x)}\right]}_{-\,D_{KL}(q\,\|\,p(z))} \;=\; E_{q}[\log p_\theta(x|z)] - D_{KL}(q(z|x)\,\|\,p(z))$$

(둘째 기댓값은 $-E_q[\log\frac{q}{p(z)}]$이고, §3의 정의에 의해 정확히 $-D_{KL}(q\|p(z))$다.)
양변의 간극이 정확히 $D_{KL}(q(z|x)\,\|\,p_\theta(z|x))$다 — 그래서 ELBO 최대화는 동시에
(1) 우도 하한을 올리고 (2) $q$를 진짜 사후분포로 끌어당긴다. 기초적인 VAE·디퓨전·잠재
월드모델 논문 다수가 이 ELBO 또는 밀접한 변분 목적함수를 쓴다 (전부는 아니다 — flow
matching이나 비변분 월드모델은 다른 길을 간다).

### 6. 빠른 참조 표

| 양 | 공식 | 딥러닝에서의 역할 |
|---|---|---|
| 엔트로피 $H(p)$ | $-E_p[\log p]$ | 불확실성; RL의 탐험 보너스 |
| 교차 엔트로피 $H(p,q)$ | $-E_p[\log q]$ | 분류/언어모델 손실 |
| KL $D_{KL}(p\|q)$ | $E_p[\log p/q]$ | VAE 정규화, RLHF 페널티, 증류 |
| 상호 정보량 $I(X;Y)$ | $H(X)-H(X|Y)$ | 대조학습(CLIP), 정보 병목 |
| Perplexity | $e^{H(p,q)}$ | 언어모델 평가 |
| ELBO | $E_q[\log p(x|z)] - D_{KL}(q\|p)$ | VAE/디퓨전/월드모델 학습 |

### 스스로 점검 · Self-check

1. $P(\text{H}) = 0.99$인 동전의 엔트로피를 계산하고, 0.9 동전보다 작은 이유를 말하라.
2. 분류기가 정답 클래스에 확률 0.25를 줬다. 이 샘플의 교차 엔트로피 손실(나트)은?
3. VAE에서 forward KL 대신 reverse KL을 쓰는 것이 흐릿한 샘플과 어떻게 연결되는가?
4. CLIP의 InfoNCE에서 배치를 2배로 키우면 상호 정보량 하한은 얼마나 좋아질 수 있는가?

> [!tip]- 정답 · Answers
> 1. $H = -0.99\log_2 0.99 - 0.01\log_2 0.01 \approx 0.08$ 비트 — 더 예측 가능할수록 놀라움의 평균이 작다.
> 2. $-\ln 0.25 = \ln 4 \approx 1.39$ 나트.
> 3. reverse KL은 모드 시킹 — $q$가 한 모드에 들러붙는다. VAE의 흐릿함은 주로 가우시안 우도(픽셀 평균화) 때문이고, KL의 비대칭은 잠재 분포가 사후분포의 일부만 덮는 쪽으로 작동한다 — 둘이 합쳐져 보수적(평균적) 샘플이 나온다.
> 4. $I \ge \log N - \mathcal{L}$이므로 하한의 천장이 $\log 2 \approx 0.69$ 나트(= 1비트)만큼 올라간다.
