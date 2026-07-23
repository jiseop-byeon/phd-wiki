---
title: "DINO & DINOv2 — Self-Supervised Vision Features that Just Work"
authors: Mathilde Caron et al. (DINO) · Maxime Oquab, Timothée Darcet et al. (DINOv2)
affiliation: Meta AI (FAIR), Inria
venue: ICCV 2021 · TMLR 2024
year: 2021
arxiv: https://arxiv.org/abs/2104.14294
pdf: https://arxiv.org/pdf/2104.14294
code: https://github.com/facebookresearch/dinov2
project: https://arxiv.org/abs/2304.07193
tags: [paper, computer-vision, self-supervised]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Caron et al., ICCV 2021 · Oquab et al., 2023** — [DINO arXiv](https://arxiv.org/abs/2104.14294) · [PDF](https://arxiv.org/pdf/2104.14294) · [DINOv2 arXiv](https://arxiv.org/abs/2304.07193) · [Code](https://github.com/facebookresearch/dinov2)

## English

**One-line summary**: Self-distillation with no labels — a student ViT matches an EMA teacher across augmented views — yields features with emergent segmentation; scaled up (DINOv2), it became the frozen vision backbone the robotics world runs on.

### Context

Contrastive self-supervision (MoCo/SimCLR) needed large batches of negatives;
[[mae|masked reconstruction]] optimized for fine-tuning, not frozen features. The prize:
*general-purpose visual features* usable frozen, without labels — vision's equivalent of a
pretrained LM.

### Method

> [!tip] Key intuition
> Be your own teacher: the teacher is just an EMA copy of the student. Show teacher global
> crops and student local crops, make the student match the teacher's output distribution —
> with centering+sharpening to prevent everyone collapsing to the same answer.

- **DINO (2021)**: student/EMA-teacher ViTs, multi-crop views, cross-entropy on softmax
  outputs; no negatives, no contrastive pairs. Discovery: self-attention maps segment
  objects *without any supervision*; k-NN classification works remarkably well.
- **DINOv2 (2023)**: the recipe industrialized — curated 142M-image dataset (LVD-142M,
  retrieval-based curation), DINO + iBOT (masked token) objectives, scaled to ViT-g, then
  distilled down; released as frozen backbones at multiple sizes.

### Results

- DINOv2 frozen features rival or beat weakly-supervised models across classification,
  depth, segmentation — *without fine-tuning*; the strongest "features that just work" of
  the open ecosystem.

### Limitations & critique

- No language alignment — pairs with text encoders ([[clip|CLIP]]/SigLIP) rather than
  replacing them; data curation pipeline is compute-heavy and partially opaque.
- Object-centric bias from curation; dense correspondence still trails specialist methods.

### Impact & follow-ups

The de-facto frozen vision encoder of embodied AI: [[openvla|OpenVLA]] fuses DINOv2+SigLIP
exactly because DINOv2 contributes spatial/geometric detail that CLIP-style features lack.
Also the backbone behind [[depth-anything|Depth Anything]]-class dense predictors.

### Connections

- Previous: [[vit|ViT]], contrastive SSL, [[mae|MAE]] (the other SSL pole)
- Next: [[openvla|OpenVLA]] (fused encoder), [[depth-anything|Depth Anything]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 라벨 없는 자기 증류 — 학생 ViT가 증강된 뷰에 대해 EMA 교사를 맞추는 것만으로, 분할이 창발하는 특징을 얻었다; 이를 산업 규모로 키운 DINOv2는 로보틱스 세계가 돌리는 고정 시각 백본이 됐다.

### 배경

대조 자기지도(MoCo/SimCLR)는 큰 배치의 음성 쌍이 필요했고, [[mae|마스크 복원]]은 고정
특징이 아니라 파인튜닝에 최적화됐다. 상금은: 라벨 없이, 얼려서 바로 쓸 수 있는
*범용 시각 특징* — 비전판 사전학습 LM이다.

### 방법

> [!tip] 핵심 직관
> 스스로의 교사가 되어라: 교사는 학생의 EMA 복사본일 뿐이다. 교사에게는 전역 크롭을,
> 학생에게는 국소 크롭을 보여주고 학생이 교사의 출력 분포를 맞추게 하라 — 모두가 같은
> 답으로 붕괴하는 것은 centering+sharpening으로 막는다.

- **DINO (2021)**: 학생/EMA 교사 ViT, 멀티크롭 뷰, softmax 출력에 대한 교차 엔트로피;
  음성 쌍도 대조 쌍도 없음. 발견: self-attention 맵이 *아무 감독 없이* 물체를 분할하고,
  k-NN 분류가 놀랍게 잘 된다.
- **DINOv2 (2023)**: 레시피의 산업화 — 검색 기반 큐레이션의 1.42억 장 데이터셋(LVD-142M),
  DINO + iBOT(마스크 토큰) 목적함수, ViT-g까지 스케일 후 증류; 여러 크기의 고정 백본으로
  공개.

### 결과

- DINOv2 고정 특징이 분류·깊이·분할 전반에서 약지도 모델과 대등하거나 우세 —
  *파인튜닝 없이*; 오픈 생태계에서 가장 강한 "그냥 되는 특징".

### 한계와 비판

- 언어 정렬이 없다 — 텍스트 인코더([[clip|CLIP]]/SigLIP)를 대체하기보다 짝을 이룬다;
  데이터 큐레이션 파이프라인이 연산 집약적이고 일부 불투명.
- 큐레이션에서 오는 물체 중심 편향; 밀집 대응(correspondence)은 전문 기법에 아직 뒤진다.

### 영향과 후속 연구

체화 AI의 사실상 표준 고정 시각 인코더: [[openvla|OpenVLA]]가 DINOv2+SigLIP을 융합하는
이유가 정확히 CLIP류 특징에 없는 공간/기하 디테일을 DINOv2가 보태기 때문이다.
[[depth-anything|Depth Anything]]류 밀집 예측기의 백본이기도 하다.

### 연결

- 이전: [[vit|ViT]], 대조 SSL, [[mae|MAE]] (SSL의 반대 극)
- 다음: [[openvla|OpenVLA]] (융합 인코더), [[depth-anything|Depth Anything]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 학생/EMA 교사 자기 증류 구조와 라벨이 필요 없는 이유를 설명할 수 있다
- [ ] 붕괴(모두 같은 출력)를 막는 장치를 말할 수 있다
- [ ] 감독 없이 분할이 창발한 관찰의 의미를 말할 수 있다
- [ ] DINOv2가 로봇/VLA의 고정 백본으로 선택되는 이유를 말할 수 있다
