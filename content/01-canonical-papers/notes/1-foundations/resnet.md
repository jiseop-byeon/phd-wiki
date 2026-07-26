---
title: "ResNet — Deep Residual Learning for Image Recognition"
authors: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
affiliation: Microsoft Research Asia
venue: CVPR
year: 2016
arxiv: https://arxiv.org/abs/1512.03385
pdf: https://arxiv.org/pdf/1512.03385
tags: [paper, foundations, computer-vision]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**He et al., CVPR 2016** — [arXiv](https://arxiv.org/abs/1512.03385) · [PDF](https://arxiv.org/pdf/1512.03385)

## English

**One-line summary**: Identity shortcut connections let networks learn residuals instead of full mappings, breaking the depth barrier — 152 layers, ILSVRC-2015 winner, and the origin of the skip connections inside every Transformer.

### Context

After [[01-canonical-papers/notes/1-foundations/vgg|VGG]], deeper should have meant better — but past ~20 layers, adding layers made *training* error worse (the **degradation problem**). This is not overfitting: a deeper net containing an identity copy of a shallower one should never be worse, yet optimizers couldn't find that solution. The problem was optimization, not capacity.

### Method

> [!tip] Key intuition
> Don't ask a stack of layers to learn the full mapping $H(x)$; ask it to learn the *correction* $F(x) = H(x) - x$ and add $x$ back. Learning "do nothing" now means pushing weights to zero — trivially easy — so depth stops hurting.

- **Residual block**: output $= F(x) + x$, with the shortcut being parameter-free identity; when dimensions change, a 1×1 conv projects the shortcut.
- **Bottleneck block** (1×1 → 3×3 → 1×1) keeps computation manageable at 50/101/152 layers.
- Batch normalization after every convolution; no dropout.
- Gradients flow directly through shortcuts, so very deep networks remain trainable.

### Results

- ILSVRC-2015 classification winner: **top-5 error 3.57%** (ensemble) with 152 layers — deeper *and* less compute than VGG-19.
- Also won ImageNet detection/localization and COCO detection/segmentation the same year — evidence that better backbones transfer everywhere.
- On CIFAR-10, trained networks over 1000 layers deep — demonstrating the degradation problem was solved.

### Limitations & critique

- Why residuals work so well was (and partly remains) under-theorized; the "ensemble of shallow paths" interpretation came later.
- Very deep ResNets show diminishing returns; width and other axes matter too (WideResNet, ResNeXt).
- Original post-activation block order was later refined (pre-activation, ResNet-v2).

### Impact & follow-ups

The default vision backbone for nearly a decade, and still the standard baseline. More importantly, the residual connection became a universal ingredient: every [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] block is `x + Sublayer(x)` — ResNet's idea, applied twice per layer, in every LLM, VLM, and VLA today.

### Connections

- Previous: [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] → [[01-canonical-papers/notes/1-foundations/vgg|VGG]]
- Next: ViT (transformers enter vision, on residual foundations)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 항등 지름길(identity shortcut)로 전체 매핑 대신 잔차(residual)를 학습하게 해 깊이의 벽을 부순 논문 — 152층, ILSVRC-2015 우승, 그리고 오늘날 모든 Transformer 안에 들어 있는 skip connection의 기원.

### 배경

[[01-canonical-papers/notes/1-foundations/vgg|VGG]] 이후 "더 깊으면 더 좋아야" 했지만, 20층을 넘기면 층을 더할수록 *학습* 오차부터 나빠졌다(**열화 문제**). 이는 과적합이 아니다: 얕은 네트워크에 항등 층만 얹은 더 깊은 네트워크는 이론상 절대 더 나쁠 수 없는데, 옵티마이저가 그 해를 찾지 못한 것이다. 즉 용량이 아니라 최적화의 문제였다.

### 방법

> [!tip] 핵심 직관
> 층 무더기에게 전체 매핑 $H(x)$를 배우라고 하지 말고, *보정량* $F(x) = H(x) - x$만 배우게 한 뒤 $x$를 다시 더해준다. 이제 "아무것도 안 하기"는 가중치를 0으로 만들면 되는 아주 쉬운 일이 되고, 깊이가 더 이상 해가 되지 않는다.

- **Residual 블록**: 출력 $= F(x) + x$. 지름길은 파라미터 없는 항등 연결이고, 차원이 바뀔 때만 1×1 합성곱으로 투영.
- **병목(bottleneck) 블록** (1×1 → 3×3 → 1×1)으로 50/101/152층에서도 연산량 유지.
- 모든 합성곱 뒤에 batch normalization; dropout은 쓰지 않음.
- 그래디언트가 지름길을 타고 직접 흐르므로 매우 깊어도 학습이 된다.

### 결과

- ILSVRC-2015 분류 우승: 152층으로 **top-5 오류율 3.57%**(앙상블) — VGG-19보다 깊으면서 연산은 오히려 적다.
- 같은 해 ImageNet 검출/localization, COCO 검출/분할까지 석권 — 좋은 백본은 어디로든 전이된다는 증거.
- CIFAR-10에서는 1000층 넘는 네트워크도 학습시켜 열화 문제 해결을 실증.

### 한계와 비판

- 왜 이렇게 잘 되는지에 대한 이론은 당시에도(지금도 일부) 부족하다; "얕은 경로들의 앙상블" 해석은 나중에 나왔다.
- 아주 깊어지면 수확 체감; 폭 등 다른 축도 중요하다(WideResNet, ResNeXt).
- 원래의 블록 순서(post-activation)는 이후 개선판(pre-activation, ResNet-v2)으로 다듬어졌다.

### 영향과 후속 연구

이후 거의 10년간 비전의 기본 백본이었고 지금도 표준 베이스라인이다. 더 중요한 유산은 residual 연결이 보편 재료가 됐다는 것: 모든 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] 블록이 `x + Sublayer(x)` 구조다 — ResNet의 아이디어가 오늘날 모든 LLM·VLM·VLA의 층마다 두 번씩 쓰이고 있다.

### 연결

- 이전: [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] → [[01-canonical-papers/notes/1-foundations/vgg|VGG]]
- 다음: ViT (residual 토대 위에서 트랜스포머가 비전에 진입)
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] State the evidence that degradation is an optimization problem rather than overfitting (training error worsens too) · 열화 문제가 과적합이 아니라 최적화 문제인 증거(학습 오차부터 나빠짐)를 말할 수 있다
- [ ] Explain why the $F(x) + x$ structure makes "doing nothing" easy · $F(x) + x$ 구조가 "아무것도 안 하기"를 왜 쉽게 만드는지 설명할 수 있다
- [ ] Say how the bottleneck block (1×1 → 3×3 → 1×1) adds depth while preserving compute · 병목 블록(1×1→3×3→1×1)이 깊이를 늘리면서 연산을 지키는 방식을 말할 수 있다
- [ ] Say where and how residual connections survive inside the Transformer · residual 연결이 Transformer의 어디에 어떻게 살아 있는지 말할 수 있다
