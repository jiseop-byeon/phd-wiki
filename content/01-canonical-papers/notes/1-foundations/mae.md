---
title: "MAE — Masked Autoencoders Are Scalable Vision Learners"
authors: Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, Ross Girshick
affiliation: Facebook AI Research (FAIR)
venue: CVPR
year: 2022
arxiv: https://arxiv.org/abs/2111.06377
pdf: https://arxiv.org/pdf/2111.06377
code: https://github.com/facebookresearch/mae
tags: [paper, foundations, computer-vision, self-supervised]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**He et al., CVPR 2022** — [arXiv](https://arxiv.org/abs/2111.06377) · [PDF](https://arxiv.org/pdf/2111.06377) · [Code](https://github.com/facebookresearch/mae)

## English

**One-line summary**: Mask 75% of image patches and reconstruct the pixels with an asymmetric encoder-decoder — BERT-style pretraining finally made simple, fast, and scalable for vision.

### Context

[[01-canonical-papers/notes/1-foundations/bert|BERT]]'s masked-prediction pretraining transformed NLP, but naive ports to vision underperformed contrastive methods (MoCo, SimCLR, DINO). Why the gap? Images are spatially redundant — masking 15% is trivially solvable by interpolation — and pixel reconstruction seemed too low-level a target. [[01-canonical-papers/notes/1-foundations/vit|ViT]] provided the missing substrate: images as patch tokens.

### Method

> [!tip] Key intuition
> Language is information-dense; images are redundant. So mask *much more* (75%, not 15%) — now reconstruction requires understanding objects and scenes, not copying neighbors. And since the encoder never sees masked patches, high masking also makes pretraining 3×+ faster.

- **Asymmetric design**: the large encoder processes *only the 25% visible patches*; a lightweight decoder takes encoded patches + mask tokens and reconstructs pixel values (normalized per patch).
- Loss: simple MSE on masked patches only. No negatives, no momentum encoder, no augmentation beyond crops — radically simpler than contrastive pipelines.
- After pretraining, the decoder is discarded; the encoder is fine-tuned.

### Results

- ViT-Huge pretrained with MAE on **ImageNet-1k only**: **87.8% top-1** — surpassing all previous ImageNet-1k-only methods and rivaling supervised JFT-300M pretraining.
- Strong transfer to detection/segmentation (surpassing supervised pretraining), with clean scaling as models grow.
- Reconstructions from 75~90% masking are semantically plausible — evidence of learned holistic understanding.

### Limitations & critique

- Learned features are optimized for fine-tuning, not linear probing — frozen-feature quality lags DINO-style methods (which is why DINOv2, not MAE, became the frozen backbone of choice for VLMs).
- Pixel targets bias toward low-level fidelity; follow-ups replaced them with tokenized or feature targets (BEiT, MaskFeat, I-JEPA's latent prediction).

### Impact & follow-ups

Closed the pretraining-paradigm gap between vision and language, making self-supervised ViT pretraining routine. Its latent-space successor I-JEPA feeds directly into the world-model line (V-JEPA), and masked-reconstruction pretraining now appears in robot learning on visual encoders and action sequences alike.

### Connections

- Previous: [[01-canonical-papers/notes/1-foundations/bert|BERT]] (the idea), [[01-canonical-papers/notes/1-foundations/vit|ViT]] (the substrate)
- Next: DINOv2, I-JEPA → world models
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 이미지 패치의 75%를 가리고 비대칭 인코더-디코더로 픽셀을 복원 — BERT식 사전학습을 비전에서 마침내 단순하고 빠르고 확장 가능하게 만든 논문.

### 배경

[[01-canonical-papers/notes/1-foundations/bert|BERT]]의 마스크 예측 사전학습이 NLP를 바꿨지만, 비전으로의 단순 이식은 대조학습(MoCo, SimCLR, DINO)에 밀렸다. 왜? 이미지는 공간적으로 중복이 많아 15% 마스킹은 주변 보간만으로 풀리고, 픽셀 복원은 목표로서 너무 저수준으로 보였다. [[01-canonical-papers/notes/1-foundations/vit|ViT]]가 빠져 있던 토대 — 이미지의 패치 토큰화 — 를 제공했다.

### 방법

> [!tip] 핵심 직관
> 언어는 정보 밀도가 높고 이미지는 중복이 많다. 그러니 *훨씬 많이* 가리자(15%가 아니라 75%) — 이제 복원은 이웃 복사가 아니라 물체와 장면의 이해를 요구한다. 게다가 인코더가 가린 패치를 아예 안 보므로, 높은 마스킹 비율은 사전학습을 3배 이상 빠르게도 만든다.

- **비대칭 설계**: 큰 인코더는 *보이는 25% 패치만* 처리; 가벼운 디코더가 인코딩된 패치 + 마스크 토큰을 받아 픽셀 값을 복원(패치별 정규화).
- 손실: 가린 패치에 대해서만 단순 MSE. 음성 쌍도, 모멘텀 인코더도, 크롭 이상의 증강도 없음 — 대조학습 파이프라인보다 급진적으로 단순하다.
- 사전학습 후 디코더는 버리고 인코더만 파인튜닝.

### 결과

- **ImageNet-1k만으로** MAE 사전학습한 ViT-Huge: **top-1 87.8%** — ImageNet-1k 단독 기준 기존 모든 방법을 넘고, JFT-300M 지도 사전학습에 필적.
- 검출·분할 전이에서 지도 사전학습을 상회, 모델이 커질수록 깔끔하게 스케일.
- 75~90% 마스킹에서도 의미적으로 그럴듯한 복원 — 전체적 이해가 학습됐다는 증거.

### 한계와 비판

- 특징이 파인튜닝에 최적화되어 있고 linear probing에는 약하다 — 고정 백본으로는 DINO 계열이 선호되는 이유(VLM의 고정 비전 인코더로 DINOv2가 쓰이는 배경).
- 픽셀 목표는 저수준 충실도로 치우친다; 후속 연구는 토큰화된 목표나 특징 목표로 대체(BEiT, MaskFeat, I-JEPA의 잠재 공간 예측).

### 영향과 후속 연구

비전과 언어 사이의 사전학습 패러다임 격차를 닫고, 자기지도 ViT 사전학습을 일상으로 만들었다. 잠재 공간 버전의 후계자 I-JEPA는 월드모델 계열(V-JEPA)로 직결되고, 마스크-복원 사전학습은 로봇 학습에서도 시각 인코더와 행동 시퀀스 양쪽에 등장한다.

### 연결

- 이전: [[01-canonical-papers/notes/1-foundations/bert|BERT]] (아이디어), [[01-canonical-papers/notes/1-foundations/vit|ViT]] (토대)
- 다음: DINOv2, I-JEPA → 월드모델
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 이미지에서 75% 마스킹이 필요한 이유(언어 대비 중복성)를 설명할 수 있다
- [ ] 비대칭 인코더/디코더가 계산 효율을 어떻게 사는지 말할 수 있다
- [ ] 픽셀 복원 목표의 한계와 잠재 예측(I-JEPA)으로의 이동을 말할 수 있다
- [ ] 파인튜닝엔 강하고 linear probe엔 약한 특성이 백본 선택에 주는 함의를 말할 수 있다
