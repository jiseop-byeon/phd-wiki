---
title: "Swin Transformer — Hierarchical Vision Transformer using Shifted Windows"
authors: Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, Baining Guo
affiliation: Microsoft Research Asia
venue: ICCV
year: 2021
arxiv: https://arxiv.org/abs/2103.14030
pdf: https://arxiv.org/pdf/2103.14030
code: https://github.com/microsoft/Swin-Transformer
tags: [paper, computer-vision]
status: to-read
---

**Liu et al., ICCV 2021** — [arXiv](https://arxiv.org/abs/2103.14030) · [PDF](https://arxiv.org/pdf/2103.14030) · [Code](https://github.com/microsoft/Swin-Transformer)

## English

**One-line summary**: Windowed attention with shifted windows + hierarchical downsampling gives Transformers linear complexity and multi-scale features — making ViT usable as a general *backbone* for detection and segmentation.

### Context

[[vit|ViT]] proved Transformers do vision, but at one fixed low resolution with quadratic
attention cost — fine for classification, unusable for dense prediction where CNN backbones
provided feature *pyramids*. Could a Transformer be shaped like a CNN backbone without
giving up attention?

### Method

> [!tip] Key intuition
> Compute attention only inside local windows (linear cost), then *shift* the window grid
> every other layer so information crosses window borders. Merge patches stage by stage
> and you get a feature pyramid — CNN-like structure, attention-like modeling.

- **W-MSA / SW-MSA**: attention within 7×7 windows; alternating shifted windows connect
  neighborhoods (with efficient cyclic-shift masking).
- **Hierarchy**: patch merging halves resolution and doubles channels across 4 stages —
  drop-in replacement for ResNet backbones in FPN/Mask R-CNN heads.
- Relative position bias inside windows.

### Results

- SOTA at publication: COCO detection (~58 box AP) and ADE20K segmentation (~53.5 mIoU) as
  a backbone; strong ImageNet accuracy with better accuracy/FLOPs trade-off than ViT.

### Limitations & critique

- Windowing reintroduces hand-designed locality — architecturally elegant question ("was
  ViT's purity the point?"); plain ViT + strong pretraining ([[mae|MAE]], DINOv2) later
  matched it, and plain-ViT detectors (ViTDet) reduced the need for hierarchy.

### Impact & follow-ups

The default Transformer backbone of the 2021–23 era for dense prediction, and the design
bridge showing attention and convolutional inductive biases can be mixed freely
(ConvNeXt answered from the CNN side).

### Connections

- Previous: [[vit|ViT]], [[resnet|ResNet]] (the backbone role it took over)
- Next: [[sam|SAM]]-era dense models, ViTDet · Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 창(window) 안에서만 어텐션을 계산하고 창을 번갈아 이동시키는 설계 + 계층적 다운샘플링으로, Transformer에 선형 복잡도와 다중 스케일 특징을 부여 — ViT를 검출·분할용 범용 *백본*으로 만들었다.

### 배경

[[vit|ViT]]는 Transformer가 비전을 할 수 있음을 증명했지만, 고정된 저해상도와 제곱
어텐션 비용 탓에 분류에는 좋아도 CNN 백본이 특징 *피라미드*를 제공하던 밀집 예측에는
쓸 수 없었다. 어텐션을 포기하지 않고 Transformer를 CNN 백본의 모양으로 만들 수 있을까?

### 방법

> [!tip] 핵심 직관
> 어텐션을 국소 창 안에서만 계산하고(선형 비용), 층마다 창 격자를 *이동*시켜 정보가 창
> 경계를 넘게 하라. 단계마다 패치를 병합하면 특징 피라미드가 생긴다 — CNN 같은 구조에
> 어텐션의 모델링 능력.

- **W-MSA / SW-MSA**: 7×7 창 내부 어텐션; 이동된 창이 번갈아 이웃을 연결(효율적인 순환
  이동 마스킹).
- **계층 구조**: 패치 병합이 4단계에 걸쳐 해상도를 반으로, 채널을 두 배로 — FPN/Mask
  R-CNN 헤드에서 ResNet 백본의 즉시 대체재.
- 창 내부의 상대 위치 편향.

### 결과

- 발표 시점 SOTA: 백본으로서 COCO 검출(~58 box AP), ADE20K 분할(~53.5 mIoU);
  ImageNet에서도 ViT보다 나은 정확도/FLOPs 균형.

### 한계와 비판

- 창 분할은 수작업 지역성의 재도입이다 — "ViT의 순수함이 핵심 아니었나"라는 구조적 질문;
  이후 순수 ViT + 강한 사전학습([[mae|MAE]], DINOv2)이 따라잡았고, 순수 ViT
  검출기(ViTDet)가 계층 구조의 필요성을 줄였다.

### 영향과 후속 연구

2021~23년 밀집 예측의 기본 Transformer 백본이자, 어텐션과 합성곱 귀납 편향을 자유로이
섞을 수 있음을 보인 설계 다리 (CNN 진영에서는 ConvNeXt가 응답했다).

### 연결

- 이전: [[vit|ViT]], [[resnet|ResNet]] (백본 역할의 인수인계)
- 다음: [[sam|SAM]] 시대의 밀집 모델, ViTDet · 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 창 어텐션 + 이동 창의 요지(선형 비용 + 경계 통신)를 말할 수 있다
- [ ] 계층 백본이 밀집 예측에 필요한 이유를 말할 수 있다
- [ ] 순정 ViT + 강한 사전학습이 다시 이긴 흐름을 말할 수 있다
