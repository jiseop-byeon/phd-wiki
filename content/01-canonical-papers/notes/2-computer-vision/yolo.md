---
title: "YOLO — You Only Look Once: Unified, Real-Time Object Detection"
authors: Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi
affiliation: University of Washington, Allen Institute for AI, Facebook AI Research
venue: CVPR
year: 2016
arxiv: https://arxiv.org/abs/1506.02640
pdf: https://arxiv.org/pdf/1506.02640
tags: [paper, computer-vision]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Redmon et al., CVPR 2016** — [arXiv](https://arxiv.org/abs/1506.02640) · [PDF](https://arxiv.org/pdf/1506.02640)

> [!note] Math on-ramp · 수학 준비물
> [[02-foundations/ml-practice|9. ML Practice §3]] for IoU/mAP, and one framing worth holding: YOLO replaces a search with a *regression*, so its errors are systematically different from [[01-canonical-papers/notes/2-computer-vision/faster-r-cnn|Faster R-CNN]]'s — the speed/accuracy trade the paper reports is not a free lunch.
> IoU·mAP는 [[02-foundations/ml-practice|9. ML 실무 §3]], 그리고 붙들고 갈 관점 하나: YOLO는 탐색을 *회귀*로 바꿨으므로 오류의 성격이 [[01-canonical-papers/notes/2-computer-vision/faster-r-cnn|Faster R-CNN]]과 체계적으로 다르다 — 논문이 보고하는 속도/정확도 거래는 공짜가 아니다.

## English

**One-line summary**: Detection as a single regression — one forward pass predicts all boxes and classes from a grid — trading some accuracy for 45+ fps and creating the real-time detection family robots actually deploy.

### Context

[[faster-r-cnn|Two-stage detectors]] were accurate but pipeline-heavy: proposals, per-region
heads, tuned stages. For robots, vehicles, and video, latency is a hard constraint. YOLO's
reframing: stop treating detection as "classify many regions" — treat the *whole image →
all boxes* as one function.

### Method

> [!tip] Key intuition
> Look at the image once, the way a human glances at a scene. Divide it into an S×S grid;
> each cell directly regresses a few boxes, confidences, and class probabilities. The
> network sees full-image context for every prediction — and speed is architectural, not
> an optimization.

- Single CNN, single loss: 7×7 grid × (2 boxes × 5 values + 20 class probs) as one output
  tensor; NMS cleans overlaps.
- Full-image context reduces background false positives vs region-based methods.

### Results

- **45 fps** (155 fps for Fast YOLO) at competitive VOC mAP (63.4) — an order of magnitude
  faster than contemporaries; generalizes better to artwork/new domains.

### Limitations & critique

- Struggles with small, clustered objects (grid cells own limited boxes) and unusual aspect
  ratios; localization error dominates its mistakes.
- v1's specific design aged fast — anchors, multi-scale, better necks arrived in v2/v3; the
  YOLO name outlived the method.

### Impact & follow-ups

Founded the real-time detection lineage (YOLOv2–v8+, SSD, RetinaNet with focal loss) that
dominates deployed perception — site safety monitoring, equipment tracking, and most
embedded robot detectors run YOLO descendants.

> [!question] Reading the claim · 핵심 주장 읽는 법
> The original speed–accuracy trade-off belongs to its detector and measurement setup. The family name does not make later YOLO versions the same method. Check resolution, hardware, object scale, and which version produced the reported result.

### Connections

- Contrast: [[faster-r-cnn|Faster R-CNN]] (accuracy-first) · Next: [[detr|DETR]] (removes NMS/anchors)
- Domain: [[05-construction-robotics/index|construction robotics]] site perception
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 검출을 단일 회귀로 — forward pass 한 번에 그리드에서 모든 박스와 클래스를 예측 — 약간의 정확도를 45+ fps와 맞바꿔, 로봇이 실제로 배치하는 실시간 검출 계열을 만들었다.

### 배경

[[faster-r-cnn|2단계 검출기]]는 정확하지만 파이프라인이 무겁다: 제안, 영역별 헤드, 튜닝된
단계들. 로봇·차량·비디오에서 지연은 강한 제약이다. YOLO의 재프레이밍: 검출을 "여러 영역의
분류"로 다루지 말고, *이미지 전체 → 모든 박스*를 하나의 함수로 다루자.

### 방법

> [!tip] 핵심 직관
> 사람이 장면을 한 번 훑어보듯 이미지를 한 번만 보라. S×S 그리드로 나누고, 각 칸이 몇 개의
> 박스·신뢰도·클래스 확률을 직접 회귀한다. 모든 예측이 이미지 전체 문맥을 본다 — 그리고
> 속도는 최적화가 아니라 구조에서 나온다.

- 단일 CNN, 단일 손실: 7×7 그리드 × (박스 2개 × 값 5 + 클래스 확률 20)이 하나의 출력 텐서;
  겹침은 NMS로 정리.
- 이미지 전체 문맥 덕에 영역 기반 방법보다 배경 오검출이 적다.

### 결과

- 경쟁력 있는 VOC mAP(63.4)를 **45 fps**로 (Fast YOLO는 155 fps) — 동시대 대비 한 자릿수
  빠름; 그림 등 새 도메인으로의 일반화도 더 좋다.

### 한계와 비판

- 작고 몰려 있는 물체(그리드 칸당 박스 수 제한)와 특이한 종횡비에 약하다; 오류의 대부분이
  위치 오차.
- v1의 구체 설계는 빨리 낡았다 — 앵커, 다중 스케일, 개선된 넥이 v2/v3에서 등장; YOLO라는
  이름이 방법론보다 오래 살아남았다.

### 영향과 후속 연구

실시간 검출 계보(YOLOv2–v8+, SSD, focal loss의 RetinaNet)를 창시 — 배치된 인식 시스템의
지배자다. 현장 안전 모니터링, 장비 추적, 임베디드 로봇 검출기 대부분이 YOLO 후손을 돌린다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 원래 속도–정확도 교환 관계는 해당 검출기와 측정 설정의 결과다. 이름이 같아도 후속 YOLO 버전은 같은 방법이 아니다. 해상도, 하드웨어, 물체 크기, 결과의 버전을 확인한다.

### 연결

- 대비: [[faster-r-cnn|Faster R-CNN]] (정확도 우선) · 다음: [[detr|DETR]] (NMS/앵커 제거)
- 도메인: [[05-construction-robotics/index|건설로봇]] 현장 인식
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Describe the composition of the S×S grid output tensor (boxes, confidence, classes) · S×S 그리드 출력 텐서의 구성(박스·신뢰도·클래스)을 말할 수 있다
- [ ] Explain what it means that the speed comes from the architecture (a single forward pass) · 속도가 구조에서 나온다는 것(단일 forward)의 의미를 설명할 수 있다
- [ ] Give the structural reason it is weak on small, clustered objects · 작고 몰린 물체에 약한 구조적 이유를 말할 수 있다
- [ ] Separate what survived from v1 (the framing) from what was discarded (the detailed design) · v1에서 살아남은 것(프레이밍)과 버려진 것(세부 설계)을 구분할 수 있다
