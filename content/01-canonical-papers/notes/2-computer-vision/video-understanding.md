---
title: "Video Understanding — I3D & SlowFast"
authors: João Carreira, Andrew Zisserman (I3D) · Christoph Feichtenhofer, Haoqi Fan, Jitendra Malik, Kaiming He (SlowFast)
affiliation: DeepMind, Oxford (I3D) · Facebook AI Research (SlowFast)
venue: CVPR 2017 · ICCV 2019
year: 2017
arxiv: https://arxiv.org/abs/1705.07750
pdf: https://arxiv.org/pdf/1705.07750
project: https://arxiv.org/abs/1812.03982
tags: [paper, computer-vision, video]
status: note-complete
last_verified: 2026-07-22
---

**Carreira & Zisserman, CVPR 2017 · Feichtenhofer et al., ICCV 2019** — [I3D arXiv](https://arxiv.org/abs/1705.07750) · [PDF](https://arxiv.org/pdf/1705.07750) · [SlowFast arXiv](https://arxiv.org/abs/1812.03982)

## English

**One-line summary**: The two canonical answers to "how do CNNs watch video": inflate 2D filters into 3D and inherit ImageNet weights (I3D), or process time at two rates — a slow semantic pathway and a fast motion pathway (SlowFast).

### Context

Action recognition lagged image recognition for years: video architectures couldn't decide
between frame-wise 2D CNNs (+LSTM/optical flow) and data-starved 3D CNNs, and no video
dataset played ImageNet's role. Kinetics (300k clips) + these two architectures closed the
gap — and video understanding matters for robotics because *demonstrations, ego-video, and
site monitoring are all video*.

### Method

> [!tip] Key intuition
> I3D: a video network shouldn't start from scratch — copy every pretrained 2D k×k filter
> k times along time (÷k) and a 3D network is born already knowing ImageNet.
> SlowFast: semantics change slowly, motion changes fast — so give each its own pathway and
> frame rate, like the ventral/dorsal streams of visual cortex.

- **I3D**: inflate Inception-v1 to 3D; two-stream (RGB + optical flow) variants; pretrain
  ImageNet → Kinetics → transfer to downstream tasks.
- **SlowFast**: Slow path (low fps, wide channels) + Fast path (high fps, ~1/8 channels)
  with lateral connections; no optical flow, end-to-end, better accuracy/FLOPs.

### Results

- I3D: ~80% on Kinetics; transferred to then-SOTA 97.9%/80.9% on UCF-101/HMDB-51 —
  established Kinetics pretraining as the video ImageNet moment.
- SlowFast: SOTA on Kinetics and AVA action detection with a better compute trade-off,
  no optical flow needed.

### Limitations & critique

- Clip-level classification: seconds-long clips, no long-horizon temporal reasoning.
- 3D convs are compute-hungry; the paradigm was later absorbed by video transformers
  (TimeSformer, ViViT, VideoMAE) and by [[jepa|V-JEPA]]-style self-supervision.

### Impact & follow-ups

Defined video backbones for a generation — action recognition on construction sites
(worker activity, safety events) still commonly runs SlowFast-class models. Conceptually,
the two-rate idea re-echoes in [[gr00t-n1|GR00T]]'s slow/fast dual system.

### Connections

- Previous: [[alexnet|CNN era]], two-stream networks · Next: video transformers, [[jepa|V-JEPA]], [[sora|video generation]]
- Domain: [[05-construction-robotics/index|site activity monitoring]] · Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: "CNN은 비디오를 어떻게 보는가"에 대한 두 가지 정전적 답: 2D 필터를 3D로 부풀려 ImageNet 가중치를 상속하거나(I3D), 시간을 두 속도로 — 느린 의미 경로와 빠른 운동 경로로 — 처리하거나(SlowFast).

### 배경

행동 인식은 수년간 이미지 인식에 뒤처졌다: 비디오 구조는 프레임별 2D CNN(+LSTM/광류)과
데이터에 굶주린 3D CNN 사이에서 갈팡질팡했고, ImageNet의 역할을 하는 비디오 데이터셋이
없었다. Kinetics(30만 클립) + 이 두 구조가 격차를 닫았다 — 그리고 비디오 이해가
로보틱스에 중요한 이유: *시연, 1인칭 비디오, 현장 모니터링이 전부 비디오*이기 때문이다.

### 방법

> [!tip] 핵심 직관
> I3D: 비디오 네트워크가 맨땅에서 시작할 이유가 없다 — 사전학습된 2D k×k 필터를 시간
> 방향으로 k번 복사(÷k)하면 이미 ImageNet을 아는 3D 네트워크가 태어난다.
> SlowFast: 의미는 천천히, 운동은 빠르게 변한다 — 각각에 자기만의 경로와 프레임
> 레이트를 줘라, 시각 피질의 복측/배측 흐름처럼.

- **I3D**: Inception-v1을 3D로 팽창; two-stream(RGB + 광류) 변형; ImageNet → Kinetics
  사전학습 → 다운스트림 전이.
- **SlowFast**: Slow 경로(낮은 fps, 넓은 채널) + Fast 경로(높은 fps, 채널 약 1/8)와
  측면 연결; 광류 없이 end-to-end, 더 나은 정확도/FLOPs.

### 결과

- I3D: Kinetics 약 80%; UCF-101/HMDB-51로 전이해 당시 SOTA 97.9%/80.9% — Kinetics
  사전학습을 비디오의 ImageNet 모먼트로 확립.
- SlowFast: Kinetics·AVA 행동 검출 SOTA를 더 나은 연산 균형으로, 광류 없이.

### 한계와 비판

- 클립 수준 분류: 수 초짜리 클립, 긴 지평의 시간 추론은 없다.
- 3D 합성곱은 연산 대식가; 이 패러다임은 이후 비디오 트랜스포머(TimeSformer, ViViT,
  VideoMAE)와 [[jepa|V-JEPA]]식 자기지도에 흡수됐다.

### 영향과 후속 연구

한 세대의 비디오 백본을 정의 — 건설 현장의 행동 인식(작업자 활동, 안전 이벤트)은 지금도
SlowFast급 모델을 흔히 돌린다. 개념적으로 두-속도 아이디어는 [[gr00t-n1|GR00T]]의
느림/빠름 이중 시스템에서 다시 메아리친다.

### 연결

- 이전: [[alexnet|CNN 시대]], two-stream 네트워크 · 다음: 비디오 트랜스포머, [[jepa|V-JEPA]], [[sora|비디오 생성]]
- 도메인: [[05-construction-robotics/index|현장 활동 모니터링]] · 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] I3D 팽창(2D 필터→3D)의 요지와 ImageNet 상속의 이점을 말할 수 있다
- [ ] SlowFast 두 경로의 분업(의미 vs 운동)을 설명할 수 있다
- [ ] Kinetics 사전학습이 비디오의 ImageNet 모먼트인 이유를 말할 수 있다
- [ ] 클립 수준 분류의 한계와 현장 모니터링 응용의 간극을 말할 수 있다
