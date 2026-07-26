---
title: "ControlNet — Adding Conditional Control to Text-to-Image Diffusion Models"
authors: Lvmin Zhang, Anyi Rao, Maneesh Agrawala
affiliation: Stanford University
venue: ICCV
year: 2023
arxiv: https://arxiv.org/abs/2302.05543
pdf: https://arxiv.org/pdf/2302.05543
code: https://github.com/lllyasviel/ControlNet
tags: [paper, generative, diffusion]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Zhang et al., ICCV 2023** — [arXiv](https://arxiv.org/abs/2302.05543) · [PDF](https://arxiv.org/pdf/2302.05543) · [Code](https://github.com/lllyasviel/ControlNet)

## English

**One-line summary**: Clone the diffusion U-Net's encoder as a trainable side-branch, connect it through zero-initialized layers, and any spatial signal — edges, pose, depth — becomes a precise control input without touching the base model.

### Context

[[latent-diffusion|Stable Diffusion]] followed *text*, but text can't say "this exact pose,
this exact layout." Fine-tuning the whole model per condition type risks catastrophic
forgetting and needs big paired data. The engineering question: how do you add tight
spatial control to a frozen 860M-parameter model with maybe 50k condition-image pairs?

### Method

> [!tip] Key intuition
> Don't modify the pretrained network — *shadow* it. A trainable copy of the encoder reads
> the condition; its outputs enter the frozen U-Net through **zero convolutions**, so at
> step zero the model is exactly the original, and control grows in from nothing without
> ever breaking the base.

- Frozen base [[u-net|U-Net]]; trainable encoder clone takes the condition map (Canny
  edges, human pose, depth, segmentation, scribbles…).
- **Zero-initialized 1×1 convs** at every junction — the no-op start that makes training
  stable on small datasets.
- One ControlNet per condition type; composable at inference.

### Results

- Faithful spatial control across a dozen condition types, robust even with <50k training
  pairs and on a single consumer GPU; quality comparable to fully fine-tuned alternatives.

### Limitations & critique

- One branch per condition (memory adds up); control fidelity vs prompt freedom trades off;
  inherits base-model biases.
- The zero-conv "sudden convergence" behavior is empirical — theory came later.

### Impact & follow-ups

Turned generative models into *controllable* tools — the pattern (frozen base + zero-init
side network) is now a general adaptation idiom alongside [[lora|LoRA]]. In robotics
pipelines: pose/depth-conditioned data augmentation and layout-controlled synthetic scene
generation for training data.

### Connections

- Previous: [[latent-diffusion|Stable Diffusion]], [[u-net|U-Net]] · Sibling idiom: [[lora|LoRA]]
- Uses: [[depth-anything|Depth Anything]] maps as conditions · Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 디퓨전 U-Net의 인코더를 학습 가능한 곁가지로 복제하고 0으로 초기화된 층으로 연결 — 에지, 포즈, 깊이 등 어떤 공간 신호든 원본 모델을 건드리지 않고 정밀한 제어 입력이 된다.

### 배경

[[latent-diffusion|Stable Diffusion]]은 *텍스트*를 따르지만, 텍스트로는 "정확히 이 포즈,
정확히 이 배치"를 말할 수 없다. 조건 종류마다 전체 모델을 파인튜닝하면 파국적 망각의
위험과 대규모 짝 데이터가 필요하다. 공학적 질문: 조건-이미지 쌍 5만 개 남짓으로, 얼린
8.6억 파라미터 모델에 어떻게 빡빡한 공간 제어를 더하는가?

### 방법

> [!tip] 핵심 직관
> 사전학습 네트워크를 수정하지 말고 *그림자*를 붙여라. 인코더의 학습 가능한 복사본이
> 조건을 읽고, 그 출력이 **zero convolution**을 거쳐 얼린 U-Net에 들어간다 — 학습 0스텝에서
> 모델은 정확히 원본이고, 제어는 무(無)에서 자라나며 베이스를 결코 망가뜨리지 않는다.

- 얼린 베이스 [[u-net|U-Net]]; 학습 가능한 인코더 복제본이 조건 맵(Canny 에지, 인체 포즈,
  깊이, 분할, 낙서…)을 받는다.
- 모든 접합부에 **0 초기화 1×1 합성곱** — 작은 데이터셋에서도 학습을 안정하게 만드는
  no-op 출발점.
- 조건 종류당 ControlNet 하나; 추론 시 조합 가능.

### 결과

- 십여 가지 조건 유형에서 충실한 공간 제어, 학습 쌍 5만 개 미만·소비자용 GPU 한 장으로도
  강건; 전체 파인튜닝 대안들과 견줄 품질.

### 한계와 비판

- 조건당 가지 하나(메모리가 쌓인다); 제어 충실도와 프롬프트 자유도의 트레이드오프;
  베이스 모델의 편향을 상속.
- zero-conv의 "급작스러운 수렴" 현상은 경험적 — 이론은 나중에 왔다.

### 영향과 후속 연구

생성 모델을 *제어 가능한* 도구로 바꿨다 — "얼린 베이스 + 0 초기화 곁가지" 패턴은
[[lora|LoRA]]와 나란히 범용 적응 관용구가 됐다. 로보틱스 파이프라인에서는: 포즈/깊이
조건 데이터 증강, 학습 데이터용 배치 제어 합성 장면 생성.

### 연결

- 이전: [[latent-diffusion|Stable Diffusion]], [[u-net|U-Net]] · 형제 관용구: [[lora|LoRA]]
- 활용: [[depth-anything|Depth Anything]] 깊이맵을 조건으로 · 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Name the safety device in the frozen-base plus zero-conv side-branch pattern · 얼린 베이스 + zero-conv 곁가지 패턴의 안전장치를 말할 수 있다
- [ ] State the cost of having one branch per condition · 조건별 브랜치 방식의 비용을 말할 수 있다
- [ ] Explain why, together with LoRA, it became the general adaptation idiom · LoRA와 함께 범용 적응 관용구가 된 이유를 말할 수 있다
