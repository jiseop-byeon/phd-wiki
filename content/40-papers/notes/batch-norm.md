---
title: "Batch Normalization"
authors: Sergey Ioffe, Christian Szegedy
affiliation: Google
venue: ICML
year: 2015
arxiv: https://arxiv.org/abs/1502.03167
pdf: https://arxiv.org/pdf/1502.03167
tags: [paper, foundations, optimization]
status: to-read
---

## English

**One-line summary**: Normalize each layer's activations over the mini-batch (with learnable scale/shift) — training becomes dramatically faster and more stable, enabling the very deep networks that followed.

### Context

Training deep nets in 2014 was fragile: it demanded small learning rates and careful initialization because each layer's input distribution keeps shifting as earlier layers update (the paper calls this *internal covariate shift*). Saturating nonlinearities and depth made it worse.

### Method

> [!tip] Key intuition
> If every layer constantly has to re-adapt to its shifting inputs, standardize those inputs as part of the network itself — then give the network back the freedom to undo it (γ, β) if the identity isn't what it wants.

- For each feature over a mini-batch: $\hat{x} = (x - \mu_B)/\sqrt{\sigma_B^2 + \epsilon}$, then $y = \gamma \hat{x} + \beta$ with learnable $\gamma, \beta$.
- Normalization is inside the graph — gradients flow through $\mu_B$ and $\sigma_B$, so the optimizer can't fight it.
- At inference, replace batch statistics with running averages collected during training.
- Applied before the nonlinearity, typically after conv/FC layers.

### Results

- Matched Inception's ImageNet accuracy with **14× fewer training steps**; enabled much higher learning rates and made initialization far less delicate.
- Slight regularization for free (batch noise), reducing the need for dropout.
- BN-Inception ensemble: top-5 error 4.9%, surpassing human-level (5.1%) on ImageNet classification.

### Limitations & critique

- The *internal covariate shift* explanation was later challenged — Santurkar et al. (2018) argue BN works by smoothing the loss landscape instead.
- Ties samples in a batch together: breaks with small batches, sequence models, and distributed settings — which is why Transformers use **LayerNorm** instead.
- Train/inference statistics mismatch is a recurring source of subtle bugs.

### Impact & follow-ups

Made deep networks routinely trainable — [[40-papers/notes/resnet|ResNet]] uses BN after every convolution and wouldn't train without it. Spawned a normalization family (LayerNorm, InstanceNorm, GroupNorm, RMSNorm); LayerNorm/RMSNorm are structural components of every [[40-papers/notes/attention-is-all-you-need|Transformer]].

### Connections

- Enables: [[40-papers/notes/resnet|ResNet]] · Successor in Transformers: LayerNorm
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 각 층의 활성값을 미니배치 단위로 정규화(학습 가능한 스케일·이동 포함) — 학습이 극적으로 빨라지고 안정되어, 이후의 초심층 네트워크들을 가능하게 했다.

### 배경

2014년의 깊은 네트워크 학습은 취약했다. 앞쪽 층이 업데이트될 때마다 각 층의 입력 분포가 계속 흔들리기 때문에(논문은 이를 *internal covariate shift*라 부른다) 작은 학습률과 조심스러운 초기화가 필수였고, 포화되는 활성함수와 깊이가 이를 악화시켰다.

### 방법

> [!tip] 핵심 직관
> 모든 층이 흔들리는 입력에 계속 재적응해야 한다면, 그 입력의 표준화를 네트워크 안에 넣어버리자 — 대신 표준화가 오히려 방해라면 되돌릴 자유(γ, β)도 함께 준다.

- 미니배치에서 특징별로: $\hat{x} = (x - \mu_B)/\sqrt{\sigma_B^2 + \epsilon}$, 이후 학습 가능한 $\gamma, \beta$로 $y = \gamma \hat{x} + \beta$
- 정규화가 계산 그래프 안에 있다 — $\mu_B$, $\sigma_B$를 통해서도 그래디언트가 흘러서 옵티마이저와 싸우지 않는다.
- 추론 시에는 배치 통계 대신 학습 중 수집한 이동 평균을 사용.
- 주로 conv/FC 층 뒤, 비선형 함수 앞에 적용.

### 결과

- Inception의 ImageNet 정확도를 **14배 적은 학습 스텝**으로 달성; 훨씬 큰 학습률 사용 가능, 초기화 민감도 대폭 감소.
- 배치 노이즈 덕에 공짜 정규화 효과 — dropout 필요성이 줄었다.
- BN-Inception 앙상블: top-5 오류율 4.9%로 인간 수준(5.1%)을 넘어섰다.

### 한계와 비판

- *Internal covariate shift*라는 설명 자체가 나중에 반박됐다 — Santurkar et al.(2018)은 손실 지형을 매끄럽게 만드는 것이 실제 이유라고 주장.
- 배치 안 샘플들을 서로 묶는다: 작은 배치, 시퀀스 모델, 분산 학습에서 깨진다 — Transformer가 **LayerNorm**을 쓰는 이유.
- 학습/추론의 통계 불일치는 미묘한 버그의 단골 원인.

### 영향과 후속 연구

깊은 네트워크 학습을 일상으로 만들었다 — [[40-papers/notes/resnet|ResNet]]은 모든 합성곱 뒤에 BN을 쓰며, BN 없이는 학습되지 않는다. 정규화 계열(LayerNorm, InstanceNorm, GroupNorm, RMSNorm)을 낳았고, LayerNorm/RMSNorm은 모든 [[40-papers/notes/attention-is-all-you-need|Transformer]]의 구조적 구성 요소다.

### 연결

- 가능하게 한 것: [[40-papers/notes/resnet|ResNet]] · Transformer에서의 후계자: LayerNorm
- 계보: [[10-deep-learning/lineage|논문 계보도]]
