---
title: "Depth Anything — Unleashing the Power of Large-Scale Unlabeled Data"
authors: Lihe Yang, Bingyi Kang, Zilong Huang, Xiaogang Xu, Jiashi Feng, Hengshuang Zhao
affiliation: University of Hong Kong, TikTok
venue: CVPR
year: 2024
arxiv: https://arxiv.org/abs/2401.10891
pdf: https://arxiv.org/pdf/2401.10891
code: https://github.com/LiheYoung/Depth-Anything
tags: [paper, computer-vision, 3d]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Yang et al., CVPR 2024** — [arXiv](https://arxiv.org/abs/2401.10891) · [PDF](https://arxiv.org/pdf/2401.10891) · [Code](https://github.com/LiheYoung/Depth-Anything)

> [!note] Math on-ramp · 수학 준비물
> [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §1–2]] is the load-bearing prerequisite: monocular depth is *scale-ambiguous* because projection divides by $Z$, and that page's worked example shows exactly what is lost. Read the paper's claims against that, not against the pretty depth maps.
> 핵심 선수 지식은 [[04-robotics/geometric-perception-calibration|3.5 기하 인식 §1–2]]다: 투영이 $Z$로 나누기 때문에 단안 깊이는 *스케일이 모호*하고, 그 페이지의 계산 예제가 무엇이 사라지는지 정확히 보여준다. 예쁜 깊이 맵이 아니라 그 사실에 논문의 주장을 대조하라.

## English

**One-line summary**: A monocular depth foundation model built by pseudo-labeling 62M unlabeled images with a teacher and forcing the student to survive harder augmentations — robust metric/relative depth for any image, from one camera.

### Context

Monocular depth (MiDaS lineage) mixed labeled datasets but hit the labeled-data ceiling:
depth sensors are expensive, and diverse ground truth is scarce. Meanwhile robots want
depth from *any* RGB camera without LiDAR. The [[sam|SAM]]-era question: can scale on
*unlabeled* images buy depth robustness?

### Method

> [!tip] Key intuition
> A teacher's pseudo-labels on easy views teach the student nothing new — unless you make
> the student's life harder. Strong perturbations (color jitter, CutMix) force the student
> to extract *more* from the same pseudo-labels than the teacher did.

- Teacher (trained on 1.5M labeled images) pseudo-labels **62M unlabeled** images; student
  trains on both, with strong augmentations applied *only to the student*.
- **Semantic anchoring**: feature-alignment loss to a frozen [[dino|DINOv2]] encoder
  imports semantic priors without hurting depth detail.
- Affine-invariant (relative) depth training across mixed datasets; metric heads fine-tuned
  per benchmark. V2 (2024) scales further with synthetic labels.

### Results

- Strong zero-shot relative depth on unseen datasets, surpassing MiDaS variants; SOTA
  fine-tuned metric depth (NYUv2, KITTI) at publication; robust to low light, blur, art.

### Limitations & critique

- Monocular depth is inherently scale-ambiguous — metric accuracy depends on fine-tuning
  domain; pseudo-label quality caps the ceiling (teacher biases inherited).
- Per-frame prediction: temporal consistency in video requires extra machinery.

### Impact & follow-ups

Made "depth from any camera" a practical commodity — used as geometric conditioning for
[[controlnet|ControlNet]]-style generation, robot manipulation pipelines without depth
sensors, and cheap site-scanning workflows. Feeds the same appetite [[vggt|VGGT]] answers
with full multi-view geometry.

### Connections

- Previous: MiDaS lineage, [[dino|DINOv2]] (semantic anchor), [[sam|SAM]] (data-engine ethos)
- Next: [[vggt|VGGT]] · Domain: [[05-construction-robotics/index|low-cost site sensing]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 교사 모델로 6,200만 장의 무라벨 이미지에 의사 라벨을 붙이고, 학생에게 더 어려운 증강을 버티게 해 만든 단안 깊이 파운데이션 모델 — 카메라 한 대로 어떤 이미지에서든 강건한 상대/절대 깊이를 얻는다.

### 배경

단안 깊이(MiDaS 계열)는 라벨된 데이터셋들을 섞었지만 라벨 데이터의 천장에 부딪혔다: 깊이
센서는 비싸고 다양한 정답 데이터는 귀하다. 한편 로봇은 LiDAR 없이 *아무* RGB 카메라에서
깊이를 원한다. [[sam|SAM]] 시대의 질문: *무라벨* 이미지의 규모로 깊이의 강건함을 살 수
있는가?

### 방법

> [!tip] 핵심 직관
> 쉬운 입력에 대한 교사의 의사 라벨은 학생에게 새로울 게 없다 — 학생의 삶을 어렵게
> 만들지 않는 한. 강한 교란(색 변형, CutMix)이 학생으로 하여금 같은 의사 라벨에서
> 교사보다 *더 많이* 뽑아내게 강제한다.

- 교사(라벨 150만 장으로 학습)가 **무라벨 6,200만 장**에 의사 라벨; 학생은 둘 다로
  학습하되 강한 증강은 *학생에게만*.
- **의미론 앵커**: 얼린 [[dino|DINOv2]] 인코더에 대한 특징 정렬 손실로, 깊이 디테일을
  해치지 않고 의미론적 사전 지식을 수입.
- 혼합 데이터셋에 걸친 아핀 불변(상대) 깊이 학습; 절대 깊이 헤드는 벤치마크별 파인튜닝.
  V2(2024)는 합성 라벨로 추가 스케일.

### 결과

- 처음 보는 데이터셋에서 MiDaS 변형들을 능가하는 zero-shot 상대 깊이; 발표 시점 파인튜닝
  절대 깊이 SOTA(NYUv2, KITTI); 저조도·블러·그림에도 강건.

### 한계와 비판

- 단안 깊이는 본질적으로 스케일이 모호하다 — 절대 정확도는 파인튜닝 도메인에 의존;
  의사 라벨 품질이 천장(교사의 편향을 상속).
- 프레임별 예측: 비디오의 시간 일관성에는 추가 장치가 필요.

### 영향과 후속 연구

"아무 카메라에서나 깊이"를 실용 상품으로 만들었다 — [[controlnet|ControlNet]]식 생성의
기하 조건, 깊이 센서 없는 로봇 조작 파이프라인, 저비용 현장 스캐닝 워크플로에 쓰인다.
[[vggt|VGGT]]가 완전한 다시점 기하로 답하는 것과 같은 수요를 먹는다.

### 연결

- 이전: MiDaS 계열, [[dino|DINOv2]] (의미론 앵커), [[sam|SAM]] (데이터 엔진 정신)
- 다음: [[vggt|VGGT]] · 도메인: [[05-construction-robotics/index|저비용 현장 센싱]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain why combining teacher pseudo-labels with strong student-only augmentation works · 교사 의사 라벨 + 학생만의 강한 증강 조합이 왜 작동하는지 설명할 수 있다
- [ ] State the difference between relative and absolute depth, and monocular scale ambiguity · 상대 깊이와 절대 깊이의 차이, 단안의 스케일 모호성을 말할 수 있다
- [ ] Say what aligning to DINOv2 features adds · DINOv2 특징 정렬이 더하는 것을 말할 수 있다
- [ ] State its use and its limits for low-cost sensing on site · 현장 저비용 센싱에서의 쓰임과 한계를 말할 수 있다
