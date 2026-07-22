---
title: "VGG — Very Deep Convolutional Networks"
authors: Karen Simonyan, Andrew Zisserman
affiliation: University of Oxford (VGG group)
venue: ICLR
year: 2015
arxiv: https://arxiv.org/abs/1409.1556
pdf: https://arxiv.org/pdf/1409.1556
tags: [paper, foundations, computer-vision]
status: to-read
---

## English

**One-line summary**: Showed that depth itself is the key variable — stacking uniform 3×3 convolutions to 16–19 layers beats shallower nets with fancier filters.

### Context

After [[40-papers/notes/alexnet|AlexNet]], everyone knew CNNs worked, but architectures were ad-hoc: mixed filter sizes (11×11, 5×5), arbitrary layer counts. The open question was *which* design dimension actually mattered. VGG's answer: keep everything minimal and uniform, and push depth.

### Method

> [!tip] Key intuition
> Two stacked 3×3 convs see a 5×5 receptive field, three see 7×7 — with fewer parameters and more nonlinearities in between. So small filters + depth strictly dominate large filters.

- Uniform design: only 3×3 convolutions (stride 1) and 2×2 max-pooling; channel width doubles after each pool (64→128→256→512).
- Configurations from 11 to 19 weight layers; VGG-16 and VGG-19 became the standard variants.
- Training used scale jittering augmentation; deeper nets initialized from shallower ones.
- Cost: ~138M parameters (VGG-16), most in the FC layers — very heavy by modern standards.

### Results

- ILSVRC-2014: **top-5 error 7.3%** (2nd place in classification behind GoogLeNet; 1st in localization).
- Features transferred exceptionally well: VGG became the default backbone for detection, segmentation, and perceptual losses for years.

### Limitations & critique

- Parameter count is enormous for its accuracy; the FC layers are wasteful (later replaced by global average pooling in successors).
- Naively stacking further (>19 layers) stopped helping — the degradation problem that [[40-papers/notes/resnet|ResNet]] later diagnosed and solved.

### Impact & follow-ups

Established the "small uniform filters, double width after downsampling" template that virtually all later CNNs follow. VGG features powered perceptual loss and style transfer research. Superseded as a backbone by [[40-papers/notes/resnet|ResNet]].

### Connections

- Previous: [[40-papers/notes/alexnet|AlexNet]] · Next: [[40-papers/notes/resnet|ResNet]]
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 균일한 3×3 합성곱만 16~19층 쌓으면 복잡한 필터를 쓴 얕은 네트워크를 이긴다 — "깊이"가 핵심 변수임을 보인 논문.

### 배경

[[40-papers/notes/alexnet|AlexNet]] 이후 CNN이 통한다는 건 모두 알았지만, 구조 설계는 임기응변이었다(11×11, 5×5 등 뒤섞인 필터, 근거 없는 층수). 어떤 설계 변수가 실제로 중요한가가 열린 질문이었고, VGG의 답은: 모든 걸 최소한으로 통일하고 깊이만 밀어붙여 보자.

### 방법

> [!tip] 핵심 직관
> 3×3 합성곱 두 개를 쌓으면 5×5의 수용 영역을, 세 개면 7×7을 커버한다 — 파라미터는 더 적고 중간의 비선형성은 더 많다. 즉 작은 필터 + 깊이가 큰 필터를 엄격하게 지배한다.

- 균일한 설계: 3×3 합성곱(stride 1)과 2×2 max-pooling만 사용; 풀링마다 채널을 2배로(64→128→256→512).
- 11층부터 19층까지 실험; VGG-16과 VGG-19가 표준 변형이 됨.
- 스케일 지터링 증강으로 학습; 깊은 모델은 얕은 모델의 가중치로 초기화.
- 대가: 파라미터 약 1.38억 개(VGG-16), 대부분 완전연결층에 몰림 — 현대 기준으로 매우 무겁다.

### 결과

- ILSVRC-2014: **top-5 오류율 7.3%** (분류 2위 — 1위는 GoogLeNet; localization은 1위).
- 특징의 전이 성능이 탁월해서 이후 수년간 검출·분할·perceptual loss의 기본 백본이 됐다.

### 한계와 비판

- 정확도 대비 파라미터가 지나치게 많다; 완전연결층이 특히 낭비 (후속 모델들은 global average pooling으로 대체).
- 19층 이상 그냥 쌓으면 성능이 더 늘지 않았다 — 이후 [[40-papers/notes/resnet|ResNet]]이 진단하고 해결한 "열화(degradation) 문제".

### 영향과 후속 연구

"작고 균일한 필터, 다운샘플링마다 채널 2배"라는 템플릿을 확립 — 이후 거의 모든 CNN이 이를 따른다. VGG 특징은 perceptual loss와 스타일 전이 연구의 기반이 됐다. 백본 자리는 [[40-papers/notes/resnet|ResNet]]에게 넘어간다.

### 연결

- 이전: [[40-papers/notes/alexnet|AlexNet]] · 다음: [[40-papers/notes/resnet|ResNet]]
- 계보: [[10-deep-learning/lineage|논문 계보도]]
