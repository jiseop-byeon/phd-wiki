---
title: "AlexNet — ImageNet Classification with Deep CNNs"
authors: Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton
affiliation: University of Toronto
venue: NeurIPS
year: 2012
pdf: https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
project: https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
tags: [paper, foundations, computer-vision]
status: note-complete
last_verified: 2026-07-22
---

**Krizhevsky et al., NeurIPS 2012** — [PDF](https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) · [Official](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)

## English

**One-line summary**: A deep CNN trained on GPUs crushed ImageNet 2012 by a 10%p margin, ending the hand-crafted-features era and starting the deep learning revolution.

### Context

Through the 2000s, computer vision meant hand-engineered features (SIFT, HOG) fed into shallow classifiers (SVMs). CNNs existed since LeNet (1998) but were dismissed as untrainable at scale. Three things converged by 2012: the ImageNet dataset (1.2M labeled images), consumer GPUs, and practical training tricks. AlexNet was the demonstration that put them together.

### Method

> [!tip] Key intuition
> Nothing conceptually new — LeNet scaled up ~1000×. The contribution is proving that scale (data + compute + depth) beats hand-crafted engineering, plus the tricks that made scale trainable.

- 8 learned layers: 5 convolutional + 3 fully connected, ~60M parameters.
- **ReLU** activation — trains several times faster than tanh/sigmoid; arguably the paper's most durable technical legacy.
- **Dropout** (0.5) in FC layers to fight overfitting; aggressive **data augmentation** (crops, flips, color jitter).
- **GPU training** — model split across two GTX 580s (3GB each); training took 5–6 days.
- Local response normalization and overlapping pooling (both later abandoned).

### Results

- ILSVRC-2012: **top-5 error 15.3%** vs. 26.2% for the runner-up — an unheard-of margin for the field.
- Ablations showed depth mattered: removing any conv layer hurt performance.

### Limitations & critique

- Architecture is ad-hoc (filter sizes 11/5/3, split-GPU topology) — designed around 2012 hardware limits, not principle.
- LRN and overlapping pooling didn't survive later scrutiny.
- 60M parameters on 1.2M images required heavy regularization; the overfitting battle shaped many design choices.

### Impact & follow-ups

Started the modern era: within two years every vision benchmark was CNN-dominated. Direct line to [[01-canonical-papers/notes/1-foundations/vgg|VGG]] (depth, principled), GoogLeNet, and [[01-canonical-papers/notes/1-foundations/resnet|ResNet]] (depth without degradation). ReLU, dropout, and augmentation remain standard practice today.

### Connections

- Next: [[01-canonical-papers/notes/1-foundations/vgg|VGG]] → [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: GPU로 학습한 깊은 CNN이 ImageNet 2012를 2위와 10%p 차이로 압도 — 수작업 특징 시대를 끝내고 딥러닝 혁명을 연 논문.

### 배경

2000년대의 컴퓨터비전은 손으로 설계한 특징(SIFT, HOG)을 얕은 분류기(SVM)에 넣는 방식이었다. CNN은 LeNet(1998) 이래 존재했지만 큰 규모로는 학습이 안 된다고 여겨졌다. 2012년까지 세 가지가 갖춰졌다: ImageNet 데이터셋(라벨된 이미지 120만 장), 소비자용 GPU, 그리고 실용적인 학습 기법들. AlexNet은 이 셋을 합치면 무슨 일이 일어나는지 보여준 실증이었다.

### 방법

> [!tip] 핵심 직관
> 개념적으로 새로운 건 없다 — LeNet을 1000배쯤 키운 것이다. 기여는 "규모(데이터+연산+깊이)가 수작업 설계를 이긴다"는 증명과, 그 규모를 학습 가능하게 만든 기법들이다.

- 학습 레이어 8층: 합성곱 5층 + 완전연결 3층, 약 6천만 파라미터.
- **ReLU** 활성함수 — tanh/sigmoid보다 몇 배 빠르게 수렴. 이 논문이 남긴 가장 오래가는 기술 유산.
- 완전연결층에 **Dropout**(0.5), 공격적인 **데이터 증강**(크롭, 좌우반전, 색상 변형).
- **GPU 학습** — 모델을 GTX 580 두 장(각 3GB)에 나눠 싣고 5~6일 학습.
- Local response normalization과 overlapping pooling (둘 다 이후 폐기됨).

### 결과

- ILSVRC-2012: **top-5 오류율 15.3%** vs 2위 26.2% — 이 분야에서 전례 없는 격차.
- 절제 실험에서 깊이의 중요성 확인: 합성곱 층을 하나만 빼도 성능이 떨어졌다.

### 한계와 비판

- 구조가 임기응변식(필터 크기 11/5/3, GPU 분할 토폴로지) — 원리가 아니라 2012년 하드웨어 한계에 맞춘 설계.
- LRN과 overlapping pooling은 이후 검증에서 살아남지 못했다.
- 120만 장에 6천만 파라미터라 과적합과의 싸움이 설계 전반을 지배했다.

### 영향과 후속 연구

현대 딥러닝의 출발점. 2년 안에 모든 비전 벤치마크가 CNN으로 넘어갔다. [[01-canonical-papers/notes/1-foundations/vgg|VGG]](깊이의 원리화), GoogLeNet, [[01-canonical-papers/notes/1-foundations/resnet|ResNet]](열화 없는 깊이)으로 직결된다. ReLU·dropout·데이터 증강은 지금도 표준이다.

### 연결

- 다음: [[01-canonical-papers/notes/1-foundations/vgg|VGG]] → [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 이 논문이 증명한 것(규모 > 수작업 설계)을 말할 수 있다
- [ ] 살아남은 유산 셋(ReLU·dropout·증강)과 버려진 것(LRN 등)을 구분할 수 있다
- [ ] 구조가 임기응변이었다는 비판의 근거를 말할 수 있다
