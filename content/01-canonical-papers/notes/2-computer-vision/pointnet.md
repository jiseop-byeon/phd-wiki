---
title: PointNet and PointNet++
authors: Charles R. Qi et al.
venue: CVPR / NeurIPS
year: 2017
pdf: https://arxiv.org/abs/1612.00593
tags: [paper, computer-vision, point-cloud]
status: note-complete
last_verified: 2026-07-23
---

## English

**One-line summary:** PointNet processes points with shared features and a symmetric
aggregation so output is invariant to input order; PointNet++ adds hierarchical local
neighborhoods to capture geometry at multiple scales.

For points $\{x_i\}$, the pattern $g(\max_i h(x_i))$ explains the key invariance. It does
not make the network invariant to rotations, density changes, calibration error, or
occlusion. PointNet++ samples centers, groups neighborhoods, and applies PointNet-like
encoders locally.

**Construction connection:** LiDAR site segmentation, material/object recognition, and
robot traversability start from unordered 3D samples. These papers are literacy anchors;
modern systems may use sparse voxels or point transformers instead.

## 한국어

**한 줄:** PointNet은 각 점에 같은 특징 함수를 적용한 뒤 대칭 집계해 입력 순서 불변성을
얻고, PointNet++는 다중 스케일 국소 이웃의 계층을 추가한다. 순서 불변성이 회전·밀도·보정
오차·가림 불변성을 뜻하지는 않는다. 건설 LiDAR 논문의 역사적 문법을 익히는 진입점이다.

### 읽고 나면 말할 수 있어야 하는 것

- 대칭 집계가 permutation invariance를 만드는 이유를 설명한다.
- PointNet++가 PointNet에 추가한 국소 구조를 말한다.
- 최신 포인트 모델이 등장해도 이 논문을 알아야 하는 이유를 설명한다.
