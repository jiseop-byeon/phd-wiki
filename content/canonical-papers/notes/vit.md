---
title: "ViT — An Image is Worth 16x16 Words"
authors: Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, et al.
affiliation: Google Research (Brain)
venue: ICLR
year: 2021
arxiv: https://arxiv.org/abs/2010.11929
pdf: https://arxiv.org/pdf/2010.11929
code: https://github.com/google-research/vision_transformer
tags: [paper, foundations, computer-vision]
status: to-read
---

**Dosovitskiy et al., ICLR 2021** — [arXiv](https://arxiv.org/abs/2010.11929) · [PDF](https://arxiv.org/pdf/2010.11929) · [Code](https://github.com/google-research/vision_transformer)

## English

**One-line summary**: Cut an image into 16×16 patches, treat them as tokens, and feed a plain Transformer — with enough pretraining data, it beats the best CNNs, unifying vision and language under one architecture.

### Context

CNNs owned vision because their inductive biases (locality, translation equivariance) fit images. Post-[[canonical-papers/notes/attention-is-all-you-need|Transformer]], hybrid attempts added attention *into* CNNs. ViT asked the blunt question: is convolution necessary at all, or does enough data replace the inductive bias?

### Method

> [!tip] Key intuition
> Convolution is a hard-coded prior about images. A Transformer has to *learn* locality — expensive in data, but strictly more flexible. Below a data threshold CNNs win; above it, the learned prior wins.

- Split image into fixed 16×16 patches → linear projection per patch → add learned position embeddings → prepend a `[class]` token → standard Transformer encoder, unchanged.
- Supervised pretraining at scale (ImageNet-21k, then JFT-300M internal dataset), fine-tuned at higher resolution downstream.
- Deliberately minimal vision-specific design — the point was to change nothing.

### Results

- Pretrained on JFT-300M, **ViT-L/16 beats ResNet-based SOTA (BiT) on ImageNet (~88.5% top-1)** with substantially less pretraining compute.
- On small data (ImageNet-1k only), ViT *loses* to comparable CNNs — cleanly demonstrating the data-vs-inductive-bias tradeoff.
- Attention maps show the model learns local-to-global attention patterns by itself.

### Limitations & critique

- Data-hungry: the headline results relied on a 300M-image private dataset (DeiT soon showed strong ImageNet-only training with distillation/augmentation).
- Quadratic attention cost in the number of patches; plain ViT lacks multi-scale features that dense prediction tasks want (fixed by Swin and hierarchical variants).
- Purely supervised pretraining — the self-supervised chapter came later ([[canonical-papers/notes/mae|MAE]], DINO).

### Impact & follow-ups

Ended the CNN monopoly and unified modalities: one token-based architecture for text and images made [[canonical-papers/notes/clip|CLIP]]-style multimodal training natural, and ViT is now the default vision encoder inside VLMs and VLAs (SigLIP, DINOv2 backbones). Successors: DeiT, Swin, [[canonical-papers/notes/mae|MAE]], DINO/DINOv2.

### Connections

- Previous: [[canonical-papers/notes/resnet|ResNet]] (the baseline it dethroned), [[canonical-papers/notes/attention-is-all-you-need|Transformer]]
- Next: [[canonical-papers/notes/mae|MAE]], CLIP
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 이미지를 16×16 패치로 잘라 토큰처럼 취급하고 순정 Transformer에 넣는다 — 충분한 사전학습 데이터만 있으면 최고의 CNN을 이기며, 비전과 언어를 하나의 구조로 통일했다.

### 배경

CNN이 비전을 지배한 것은 그 귀납 편향(지역성, 평행이동 등변성)이 이미지에 잘 맞았기 때문이다. [[canonical-papers/notes/attention-is-all-you-need|Transformer]] 이후의 시도들은 어텐션을 CNN *안에* 끼워 넣는 절충이었다. ViT는 직설적으로 물었다: 합성곱이 필요하긴 한가? 데이터가 충분하면 귀납 편향을 대체하지 않을까?

### 방법

> [!tip] 핵심 직관
> 합성곱은 이미지에 대한 하드코딩된 사전 지식이다. Transformer는 지역성을 *배워야* 한다 — 데이터는 더 들지만 엄격히 더 유연하다. 데이터가 문턱 아래면 CNN이 이기고, 그 위면 학습된 사전 지식이 이긴다.

- 이미지를 고정 16×16 패치로 분할 → 패치별 선형 투영 → 학습된 위치 임베딩 추가 → `[class]` 토큰을 앞에 붙임 → 표준 Transformer 인코더를 그대로 사용.
- 대규모 지도 사전학습(ImageNet-21k, 이후 내부 데이터셋 JFT-300M), 다운스트림에서는 더 높은 해상도로 파인튜닝.
- 비전 특화 설계를 의도적으로 최소화 — "아무것도 안 바꾸는 것"이 논문의 요점.

### 결과

- JFT-300M 사전학습 시 **ViT-L/16이 ResNet 계열 SOTA(BiT)를 ImageNet에서 추월(top-1 약 88.5%)**, 사전학습 연산은 오히려 훨씬 적다.
- 작은 데이터(ImageNet-1k만)에서는 동급 CNN에 *진다* — 데이터 vs 귀납 편향의 트레이드오프를 깔끔하게 실증.
- 어텐션 맵을 보면 지역→전역 어텐션 패턴을 스스로 학습한다.

### 한계와 비판

- 데이터 대식가: 대표 결과가 3억 장짜리 비공개 데이터셋에 의존 (곧 DeiT가 증류·증강으로 ImageNet만으로도 강한 학습을 보임).
- 패치 수에 대한 어텐션의 제곱 비용; 순정 ViT는 밀집 예측 과제가 원하는 다중 스케일 특징이 없다(Swin 등 계층적 변형이 해결).
- 순수 지도 사전학습 — 자기지도 챕터는 이후에 온다([[canonical-papers/notes/mae|MAE]], DINO).

### 영향과 후속 연구

CNN 독점을 끝내고 모달리티를 통일했다: 텍스트와 이미지가 같은 토큰 기반 구조를 쓰게 되면서 [[canonical-papers/notes/clip|CLIP]]식 멀티모달 학습이 자연스러워졌고, ViT는 현재 VLM·VLA의 기본 비전 인코더다(SigLIP, DINOv2 백본). 후속: DeiT, Swin, [[canonical-papers/notes/mae|MAE]], DINO/DINOv2.

### 연결

- 이전: [[canonical-papers/notes/resnet|ResNet]] (왕좌에서 내려온 베이스라인), [[canonical-papers/notes/attention-is-all-you-need|Transformer]]
- 다음: [[canonical-papers/notes/mae|MAE]], CLIP
- 계보: [[10-deep-learning/lineage|논문 계보도]]
