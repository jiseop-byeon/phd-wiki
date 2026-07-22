---
title: "Faster R-CNN — Towards Real-Time Object Detection with Region Proposal Networks"
authors: Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun
affiliation: Microsoft Research
venue: NeurIPS
year: 2015
arxiv: https://arxiv.org/abs/1506.01497
pdf: https://arxiv.org/pdf/1506.01497
tags: [paper, computer-vision]
status: to-read
---

**Ren et al., NeurIPS 2015** — [arXiv](https://arxiv.org/abs/1506.01497) · [PDF](https://arxiv.org/pdf/1506.01497)

## English

**One-line summary**: Replace hand-crafted region proposals with a learned Region Proposal Network sharing the backbone — making detection fully end-to-end learnable and defining the two-stage paradigm.

### Context

R-CNN → Fast R-CNN had made classification-of-regions fast, but region *proposals* still
came from Selective Search — a hand-crafted CPU algorithm that dominated runtime (~2s per
image) and capped quality. The last non-learned component had to go.

### Method

> [!tip] Key intuition
> The backbone's features already know where objects might be — attach a tiny network that
> slides over them and asks, at each location and for a few reference box shapes
> ("anchors"), *object or not, and how should the box shift?*

- **RPN**: per anchor (multi-scale/aspect reference boxes), predict objectness + box
  regression; ~300 learned proposals replace ~2000 hand-crafted ones.
- Stage two: Fast R-CNN head classifies/refines pooled proposal features (RoI pooling);
  **backbone shared** between both stages, trained jointly.

### Results

- SOTA on PASCAL VOC and COCO at 5 fps — proposals now cost ~10ms; learned proposals also
  *improved* accuracy (mAP ~70%+ VOC07).

### Limitations & critique

- Two-stage pipeline with NMS, anchors, and many hyperparameters — the complexity
  [[yolo|YOLO]] (speed) and [[detr|DETR]] (end-to-end sets) later attacked from both sides.
- Per-region computation limits throughput vs single-shot detectors.

### Impact & follow-ups

Defined the accuracy-first detector family: Mask R-CNN (adds segmentation), FPN
(multi-scale), Cascade R-CNN. In robotics/construction perception, two-stage detectors
remain the choice when precision beats latency.

### Connections

- Previous: [[vgg|VGG]]/R-CNN line · Parallel: [[yolo|YOLO]] · Next: [[detr|DETR]], Mask R-CNN
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 수작업 영역 제안을 백본을 공유하는 학습된 Region Proposal Network로 교체 — 검출을 완전히 end-to-end 학습 가능하게 만들고 2단계 패러다임을 정의했다.

### 배경

R-CNN → Fast R-CNN이 "영역의 분류"는 빠르게 만들었지만, 영역 *제안*은 여전히 Selective
Search — 이미지당 약 2초를 잡아먹으며 품질의 상한이 되는 수작업 CPU 알고리즘 — 에서
나왔다. 마지막 남은 비학습 구성 요소를 없애야 했다.

### 방법

> [!tip] 핵심 직관
> 백본의 특징은 이미 물체가 있을 법한 곳을 알고 있다 — 그 위를 슬라이딩하는 작은
> 네트워크를 붙여, 각 위치에서 몇 가지 기준 박스 모양("앵커")마다 *물체인가 아닌가,
> 박스를 어떻게 움직여야 하는가*를 묻게 하라.

- **RPN**: 앵커(다중 스케일/종횡비 기준 박스)마다 물체성 점수 + 박스 회귀 예측;
  수작업 제안 ~2000개를 학습된 제안 ~300개가 대체.
- 2단계: Fast R-CNN 헤드가 풀링된 제안 특징을 분류/정제(RoI pooling);
  두 단계가 **백본을 공유**하며 공동 학습.

### 결과

- PASCAL VOC·COCO에서 SOTA를 5 fps로 — 제안 비용이 ~10ms로; 학습된 제안이 정확도까지
  *끌어올렸다* (VOC07 mAP 70%+).

### 한계와 비판

- NMS, 앵커, 수많은 하이퍼파라미터가 딸린 2단계 파이프라인 — 이 복잡성을
  [[yolo|YOLO]](속도)와 [[detr|DETR]](end-to-end 집합 예측)가 양쪽에서 공격하게 된다.
- 영역별 연산이 단발(single-shot) 검출기 대비 처리량을 제한.

### 영향과 후속 연구

정확도 우선 검출기 계열을 정의: Mask R-CNN(분할 추가), FPN(다중 스케일), Cascade R-CNN.
로보틱스/건설 인식에서 정밀도가 지연보다 중요할 때는 여전히 2단계 검출기가 선택지다.

### 연결

- 이전: [[vgg|VGG]]/R-CNN 계열 · 병행: [[yolo|YOLO]] · 다음: [[detr|DETR]], Mask R-CNN
- 계보: [[10-deep-learning/lineage|논문 계보도]]
