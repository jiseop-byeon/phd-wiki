---
title: "DETR — End-to-End Object Detection with Transformers"
authors: Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko
affiliation: Facebook AI Research
venue: ECCV
year: 2020
arxiv: https://arxiv.org/abs/2005.12872
pdf: https://arxiv.org/pdf/2005.12872
code: https://github.com/facebookresearch/detr
tags: [paper, computer-vision]
status: to-read
---

**Carion et al., ECCV 2020** — [arXiv](https://arxiv.org/abs/2005.12872) · [PDF](https://arxiv.org/pdf/2005.12872) · [Code](https://github.com/facebookresearch/detr)

> [!note] 수학 준비물 · Math on-ramp
> 헝가리안 매칭 = 예측과 정답의 최적 1:1 짝짓기(할당 문제, [[02-foundations/optimization|최적화]]의 조합 버전). 여기서는 "이 손실이 유일 대응 위에서 계산된다"는 것만 알면 논문이 읽힌다 — 알고리즘 내부는 블랙박스로 둬도 된다.

## English

**One-line summary**: Detection as direct *set prediction* — a Transformer decodes N object queries against image features, and Hungarian matching replaces anchors, NMS, and all hand-designed detection machinery.

### Context

Both [[faster-r-cnn|two-stage]] and [[yolo|one-stage]] detectors relied on the same crutches:
anchor boxes encoding priors, and NMS deduplicating predictions — non-differentiable
post-processing outside the learned model. The question: can detection be a *pure*
end-to-end mapping from image to a set of boxes?

### Method

> [!tip] Key intuition
> A detection output is a *set* — unordered, no duplicates. So make the loss set-aware:
> bipartite-match predictions to ground truth (Hungarian algorithm) and penalize each
> matched pair. Duplicates now hurt by construction, and NMS becomes unnecessary.

- CNN backbone → [[attention-is-all-you-need|Transformer]] encoder-decoder; **N learned
  object queries** cross-attend to image features, each emitting (class, box) — including
  "no object."
- **Hungarian (bipartite) matching loss**: unique assignment prediction↔GT, then class +
  L1/GIoU box loss on matches.
- Extends to panoptic segmentation with a mask head.

### Results

- Matches tuned Faster R-CNN on COCO (~42 AP) with a conceptually minimal pipeline;
  notably better on large objects (global attention), weaker on small ones.

### Limitations & critique

- Slow convergence (500 epochs) and small-object weakness — fixed by Deformable DETR,
  DAB/DN-DETR, and today's DINO-DETR family.
- N fixed queries cap the number of detectable objects.

### Impact & follow-ups

Made "queries + bipartite matching" the modern detection/segmentation grammar
(Mask2Former, DINO-DETR — COCO leaders) and exported *learned queries* everywhere:
[[blip-2|BLIP-2]]'s Q-Former and [[octo|Octo]]'s readout tokens are DETR queries in new
clothes.

### Connections

- Previous: [[faster-r-cnn|Faster R-CNN]], [[yolo|YOLO]], [[attention-is-all-you-need|Transformer]]
- Next: Deformable DETR, [[sam|SAM]]-era segmentation, [[blip-2|BLIP-2]] (queries)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 검출을 직접적인 *집합 예측*으로 — Transformer가 N개의 물체 쿼리를 이미지 특징에 대해 디코딩하고, 헝가리안 매칭이 앵커·NMS 등 수작업 검출 장치 전부를 대체한다.

### 배경

[[faster-r-cnn|2단계]]든 [[yolo|1단계]]든 같은 목발에 의지했다: 사전 지식을 박아 넣은 앵커
박스, 그리고 예측 중복을 제거하는 NMS — 학습된 모델 밖의 미분 불가능한 후처리다. 질문:
검출이 이미지에서 박스 집합으로 가는 *순수한* end-to-end 사상이 될 수 있는가?

### 방법

> [!tip] 핵심 직관
> 검출의 출력은 *집합*이다 — 순서 없고, 중복 없다. 그러니 손실을 집합답게 만들어라:
> 예측과 정답을 이분 매칭(헝가리안 알고리즘)하고 매칭된 쌍마다 벌점을 준다. 이제 중복은
> 구조적으로 손해가 되고, NMS는 불필요해진다.

- CNN 백본 → [[attention-is-all-you-need|Transformer]] 인코더-디코더; **학습된 물체 쿼리
  N개**가 이미지 특징에 cross-attention하며 각자 (클래스, 박스)를 출력 — "물체 없음" 포함.
- **헝가리안(이분) 매칭 손실**: 예측↔정답의 유일 대응 후, 매칭에 대해 클래스 + L1/GIoU
  박스 손실.
- 마스크 헤드를 붙이면 panoptic 분할로 확장.

### 결과

- 개념적으로 최소인 파이프라인으로 COCO에서 튜닝된 Faster R-CNN과 대등(~42 AP);
  큰 물체에서 특히 강하고(전역 어텐션), 작은 물체에서 약하다.

### 한계와 비판

- 느린 수렴(500 에폭)과 작은 물체 약점 — Deformable DETR, DAB/DN-DETR, 오늘날의
  DINO-DETR 계열이 해결.
- 고정된 쿼리 수 N이 검출 가능한 물체 수의 상한.

### 영향과 후속 연구

"쿼리 + 이분 매칭"을 현대 검출/분할의 문법으로 만들었고(Mask2Former, DINO-DETR — COCO
선두), *학습된 쿼리*를 도처에 수출했다: [[blip-2|BLIP-2]]의 Q-Former와 [[octo|Octo]]의
readout 토큰은 새 옷을 입은 DETR 쿼리다.

### 연결

- 이전: [[faster-r-cnn|Faster R-CNN]], [[yolo|YOLO]], [[attention-is-all-you-need|Transformer]]
- 다음: Deformable DETR, [[sam|SAM]] 시대의 분할, [[blip-2|BLIP-2]] (쿼리)
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 검출을 집합 예측으로 보는 관점과 헝가리안 매칭의 역할을 설명할 수 있다
- [ ] NMS가 불필요해지는 구조적 이유를 말할 수 있다
- [ ] 물체 쿼리가 무엇을 배우는지, 고정 N의 한계는 무엇인지 말할 수 있다
- [ ] 학습된 쿼리 아이디어가 어디로 수출됐는지(Q-Former, readout) 말할 수 있다
