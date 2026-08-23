---
title: PointNet and PointNet++
authors: Charles R. Qi et al.
affiliation: Stanford University
venue: CVPR / NeurIPS
year: 2017
arxiv: https://arxiv.org/abs/1612.00593
pdf: https://arxiv.org/pdf/1612.00593
tags: [paper, computer-vision, point-cloud]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Qi et al., CVPR 2017** — [arXiv](https://arxiv.org/abs/1612.00593) · [PDF](https://arxiv.org/pdf/1612.00593)

> [!note] Math on-ramp · 수학 준비물
> [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §3]] for what a point cloud is and which frame it lives in. The paper's core is one property from [[02-foundations/linear-algebra|1. Linear Algebra §1]]: max-pooling over points is **permutation-invariant**, which is exactly what an unordered set demands.
> 포인트 클라우드가 무엇이고 어느 프레임에 사는지는 [[04-robotics/geometric-perception-calibration|3.5 기하 인식 §3]]. 논문의 핵심은 [[02-foundations/linear-algebra|1. 선형대수 §1]]에서 오는 성질 하나다: 점들에 대한 max-pooling은 **순열 불변**이고, 그것이 순서 없는 집합이 요구하는 바로 그것이다.

## English

**One-line summary**: PointNet feeds every point through the same feature function and aggregates with a symmetric max-pool, making the output invariant to point order; PointNet++ adds a hierarchy of local neighborhoods so geometry is captured at multiple scales.

### Context

A point cloud is an *unordered set* of 3D samples — permuting the points changes nothing about the scene. Before PointNet, deep methods dodged this by voxelizing (memory-hungry, quantized) or rendering multi-view images (loses 3D structure). The open question: can a network consume raw points directly and still be provably indifferent to their order?

### Method

> [!tip] Key intuition
> Any function that is symmetric in its inputs is order-invariant. So: apply one shared per-point encoder $h$, collapse with a symmetric operation (max), and decode the pooled vector — $g(\max_i h(x_i))$ is the whole trick.

- **PointNet**: shared MLP per point → max-pool to a global feature → task heads for classification, or concatenated back per-point for segmentation. Small alignment networks (T-Net) predict transforms to canonicalize input and feature spaces.
- The paper proves the architecture can approximate any continuous set function, and shows a "critical point set" — a sparse skeleton of points that fully determines the output — explaining robustness to missing points.
- What the symmetry does *not* give: invariance to rotations, density variation, calibration error, or occlusion. Order invariance is a narrow, precise property.
- **PointNet++** (NeurIPS 2017, arXiv 1706.02413): farthest-point-sample centers, group neighbors in metric balls, run a small PointNet per group, repeat hierarchically — local structure at growing scales, with multi-scale/multi-resolution grouping to handle non-uniform density (a LiDAR reality).

### Results

- ModelNet40 shape classification on par with or better than voxel baselines at a fraction of the compute (multi-view CNNs like MVCNN still edged it on raw accuracy — the win was efficiency and directness, not every leaderboard); strong ShapeNet part segmentation and S3DIS indoor semantic segmentation.
- Notably robust to point dropout — with the critical-point-set analysis giving the reason rather than just the number.
- PointNet++ improves precisely where PointNet is weakest: fine local geometry and scenes with uneven sampling density.

### Limitations & critique

- Vanilla PointNet has no local context below the global pool — fine structures blur; PointNet++ fixes this at the cost of sampling/grouping hyperparameters.
- Not rotation-invariant; T-Net helps with pose canonicalization but is learned, not guaranteed.
- Scaling to large outdoor scenes requires block partitioning; modern systems often reach for sparse-voxel convolutions or point transformers instead.

### Impact & follow-ups

The grammar of an entire subfield: nearly every point-cloud architecture since either extends the shared-encoder-plus-symmetric-pool pattern or defines itself against it (sparse conv nets, KPConv, Point Transformer). **Construction connection**: LiDAR site segmentation, material and object recognition, and traversability estimation all start from unordered 3D samples — these papers are the literacy anchor for reading that literature, even where modern systems use different backbones.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "Permutation-invariant" is often read as generic robustness. It is not — a rotated, sparser, or miscalibrated cloud is a different input, and site conditions (dust, rain, reflective surfaces) attack exactly those axes.

### Connections

- Robotics foundations: [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]] (point clouds, registration, calibration)
- Construction stream: [[05-construction-robotics/site-perception|site-perception stream]]
- Applied on site: [[01-canonical-papers/notes/8-construction/cho-slam|Cho SLAM]]

## 한국어

**한 줄 요약**: PointNet은 모든 점을 같은 특징 함수에 통과시킨 뒤 대칭적인 max-pool로 집계해 출력이 점 순서에 불변하게 만들고, PointNet++는 국소 이웃의 계층을 추가해 여러 스케일의 기하 구조를 포착한다.

### 배경

포인트 클라우드는 3D 샘플의 *순서 없는 집합*이다 — 점들의 순서를 바꿔도 장면은 그대로다. PointNet 이전의 딥러닝 방법들은 이를 회피했다: 복셀화(메모리 폭식, 양자화 손실)하거나 다시점 이미지로 렌더링(3D 구조 상실)했다. 열린 질문: 네트워크가 날 점들을 직접 먹으면서도 순서에 무관함을 증명 가능하게 보장할 수 있는가?

### 방법

> [!tip] 핵심 직관
> 입력에 대해 대칭인 함수는 순서 불변이다. 그러니: 공유된 점별 인코더 $h$를 적용하고, 대칭 연산(max)으로 뭉갠 뒤, 풀링된 벡터를 디코딩하라 — $g(\max_i h(x_i))$가 트릭의 전부다.

- **PointNet**: 점별 공유 MLP → max-pool로 전역 특징 → 분류는 그대로 헤드로, 분할은 점별 특징에 다시 이어붙여 처리. 작은 정렬 네트워크(T-Net)가 입력·특징 공간을 정규 자세로 맞추는 변환을 예측한다.
- 논문은 이 구조가 임의의 연속 집합 함수를 근사할 수 있음을 증명하고, 출력을 완전히 결정하는 희소한 점 골격인 "critical point set"을 보여 점 손실에 대한 강건성을 설명한다.
- 대칭성이 주지 *않는* 것: 회전, 밀도 변화, 보정 오차, 가림에 대한 불변성. 순서 불변성은 좁고 정확한 성질이다.
- **PointNet++**(NeurIPS 2017, arXiv 1706.02413): farthest point sampling으로 중심을 뽑고, 거리 공(ball) 안에서 이웃을 묶고, 그룹마다 작은 PointNet을 돌리고, 이를 계층적으로 반복 — 커지는 스케일의 국소 구조를 얻으며, 다중 스케일/다중 해상도 grouping으로 불균일 밀도(LiDAR의 현실)에 대응한다.

### 결과

- ModelNet40 형상 분류에서 복셀 기준선과 대등하거나 더 나은 성능을 훨씬 적은 연산으로 (MVCNN 같은 다시점 CNN은 순수 정확도에서 여전히 근소 우세 — 승리는 모든 리더보드가 아니라 효율성과 직접성이었다); ShapeNet 부품 분할과 S3DIS 실내 의미 분할에서도 강력하다.
- 점 탈락(dropout)에 눈에 띄게 강건하다 — 숫자만이 아니라 critical-point-set 분석이 그 이유를 제공한다.
- PointNet++는 정확히 PointNet의 약점에서 개선한다: 미세한 국소 기하와 샘플링 밀도가 고르지 않은 장면.

### 한계와 비판

- 순수 PointNet은 전역 풀링 아래 국소 문맥이 없다 — 미세 구조가 뭉개진다; PointNet++가 이를 고치지만 샘플링/grouping 하이퍼파라미터가 대가다.
- 회전 불변이 아니다; T-Net이 자세 정규화를 돕지만 학습된 것이지 보장이 아니다.
- 대규모 실외 장면으로 확장하려면 블록 분할이 필요하다; 현대 시스템은 종종 희소 복셀 컨볼루션이나 point transformer를 대신 쓴다.

### 영향과 후속 연구

한 하위 분야 전체의 문법: 이후 거의 모든 포인트 클라우드 아키텍처가 공유 인코더 + 대칭 풀링 패턴을 확장하거나 그에 맞서 자신을 정의한다(sparse conv 네트워크, KPConv, Point Transformer). **건설 연결**: LiDAR 현장 분할, 자재·객체 인식, 주행 가능성 추정은 모두 순서 없는 3D 샘플에서 출발한다 — 최신 시스템이 다른 backbone을 쓰더라도, 이 논문들은 그 문헌을 읽기 위한 문해력의 닻이다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "permutation-invariant"는 흔히 범용 강건성으로 오독된다. 아니다 — 회전됐거나, 더 희소하거나, 보정이 어긋난 클라우드는 다른 입력이고, 현장 조건(먼지, 비, 반사면)은 정확히 그 축들을 공격한다.

### 연결

- 로보틱스 기초: [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]] (포인트 클라우드, 정합, 보정)
- 건설 스트림: [[05-construction-robotics/site-perception|site-perception stream]]
- 현장 적용: [[01-canonical-papers/notes/8-construction/cho-slam|Cho SLAM]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain why the symmetric aggregation $g(\max_i h(x_i))$ produces permutation invariance, and what it does *not* guarantee (invariance to rotation, density, calibration or occlusion) · 대칭 집계 $g(\max_i h(x_i))$가 permutation invariance를 만드는 이유와, 그것이 보장하지 않는 것(회전·밀도·보정·가림)을 설명할 수 있다
- [ ] Say what PointNet++ added (hierarchical local neighborhoods, density-adaptive grouping) · PointNet++가 PointNet에 추가한 것(계층적 국소 이웃, 밀도 대응 grouping)을 말할 수 있다
- [ ] Explain why this paper still matters despite newer point models (sparse convolutions, point transformers) · 최신 포인트 모델(sparse conv, point transformer)이 있어도 이 논문을 알아야 하는 이유를 설명할 수 있다
