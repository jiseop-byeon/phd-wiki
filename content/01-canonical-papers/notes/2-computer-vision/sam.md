---
title: "SAM — Segment Anything"
authors: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, et al.
affiliation: Meta AI (FAIR)
venue: ICCV
year: 2023
arxiv: https://arxiv.org/abs/2304.02643
pdf: https://arxiv.org/pdf/2304.02643
code: https://github.com/facebookresearch/segment-anything
tags: [paper, computer-vision]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Kirillov et al., ICCV 2023** — [arXiv](https://arxiv.org/abs/2304.02643) · [PDF](https://arxiv.org/pdf/2304.02643) · [Code](https://github.com/facebookresearch/segment-anything)

## English

**One-line summary**: A promptable segmentation foundation model — point/box/mask prompts in, valid mask out — trained via a model-in-the-loop data engine that produced 1.1B masks, making segmentation zero-shot.

### Context

Segmentation models were dataset-bound: train on COCO classes, segment COCO classes.
[[gpt-3|Foundation-model]] thinking suggested a different target: one model, *promptable*,
working zero-shot on anything — but no billion-mask dataset existed to train it. So the
dataset had to be built *by* the model.

### Method

> [!tip] Key intuition
> Two moves: (1) define a task general enough to pretrain on — "return a valid mask for
> *any* prompt, even ambiguous ones"; (2) bootstrap data with a flywheel: the model helps
> annotate, annotations improve the model, until annotation is fully automatic.

- Architecture: heavy **ViT image encoder** ([[mae|MAE]]-pretrained) run once per image +
  light prompt encoder + fast mask decoder (~50 ms) — interactive by design; outputs 3 masks
  to resolve prompt ambiguity.
- **Data engine → SA-1B**: assisted-manual → semi-automatic → fully automatic stages;
  final dataset **11M images, 1.1B masks**, released.

### Results

- Zero-shot transfer to 23 segmentation datasets, often matching or beating supervised
  specialists; strong zero-shot edge detection, proposal generation, and
  text-prompt composition with [[clip|CLIP]]-style encoders.

### Limitations & critique

- Class-agnostic: SAM knows *where* things are, not *what* they are — needs pairing with
  detectors/VLMs (Grounded-SAM) for semantics.
- Heavy encoder limits real-time robot use (addressed by MobileSAM/FastSAM, SAM 2 for video).
- Mask granularity ambiguity (part vs whole) is only partially resolved by multi-mask output.

### Impact & follow-ups

Made segmentation an off-the-shelf capability: in robotics and construction perception,
SAM(+detector) is the default tool for object masks, progress monitoring, and data
labeling. SAM 2 (2024) extended promptable segmentation to video/streaming — directly
useful for site monitoring.

### Connections

- Previous: [[mae|MAE]] (encoder), [[detr|DETR]]-era mask decoders, [[clip|CLIP]] (composition)
- Domain: [[05-construction-robotics/index|site perception]] · Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 프롬프트 가능한 분할 파운데이션 모델 — 점/박스/마스크 프롬프트를 넣으면 유효한 마스크가 나온다 — 모델이 참여하는 데이터 엔진으로 11억 개 마스크를 만들어 분할을 zero-shot으로 만들었다.

### 배경

분할 모델은 데이터셋에 묶여 있었다: COCO 클래스로 학습하면 COCO 클래스만 분할한다.
[[gpt-3|파운데이션 모델]]식 사고는 다른 목표를 제시했다: 하나의 모델이 *프롬프트*를 받아
무엇이든 zero-shot으로 분할하는 것 — 그런데 이를 학습시킬 10억 마스크 데이터셋이 없었다.
그래서 데이터셋을 모델*로* 만들어야 했다.

### 방법

> [!tip] 핵심 직관
> 두 수: (1) 사전학습할 만큼 일반적인 과제를 정의하라 — "*어떤* 프롬프트든, 모호해도,
> 유효한 마스크를 반환하라"; (2) 플라이휠로 데이터를 부트스트랩하라: 모델이 주석을 돕고,
> 주석이 모델을 개선하고, 결국 주석이 완전 자동이 될 때까지.

- 구조: 이미지당 한 번 도는 무거운 **ViT 이미지 인코더**([[mae|MAE]] 사전학습) + 가벼운
  프롬프트 인코더 + 빠른 마스크 디코더(~50 ms) — 설계부터 인터랙티브; 프롬프트 모호성을
  풀기 위해 마스크 3개를 출력.
- **데이터 엔진 → SA-1B**: 보조 수동 → 반자동 → 완전 자동 단계;
  최종 **1,100만 이미지, 11억 마스크** 공개.

### 결과

- 23개 분할 데이터셋으로 zero-shot 전이, 지도학습 전문 모델과 대등하거나 우세한 경우 다수;
  zero-shot 에지 검출·제안 생성, [[clip|CLIP]]류 인코더와의 텍스트 프롬프트 조합도 강력.

### 한계와 비판

- 클래스 불가지: SAM은 *어디에* 있는지는 알지만 *무엇*인지는 모른다 — 의미론은
  검출기/VLM과의 결합(Grounded-SAM)이 필요.
- 무거운 인코더가 실시간 로봇 사용을 제한 (MobileSAM/FastSAM, 비디오용 SAM 2가 대응).
- 마스크 입도의 모호성(부분 vs 전체)은 다중 마스크 출력으로 부분적으로만 해소.

### 영향과 후속 연구

분할을 기성품 능력으로 만들었다: 로보틱스·건설 인식에서 SAM(+검출기)은 물체 마스크, 공정
모니터링, 데이터 라벨링의 기본 도구다. SAM 2(2024)는 프롬프트 분할을 비디오/스트리밍으로
확장 — 현장 모니터링에 직접 유용하다.

### 연결

- 이전: [[mae|MAE]] (인코더), [[detr|DETR]] 시대의 마스크 디코더, [[clip|CLIP]] (조합)
- 도메인: [[05-construction-robotics/index|현장 인식]] · 계보: [[03-deep-learning/lineage|논문 계보도]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "Segment anything" means "find the boundary of anything", not "know what it is" — class-agnosticism is part of the design. And the qualifier *promptable* carries half the claim: this is not a claim to segment everything correctly on its own, without a prompt.
>
> "segment anything"은 "무엇이든 경계를 찾는다"이지 "무엇인지 안다"가 아니다 — 클래스 불가지가 설계의 일부다. 그리고 promptable이라는 단서가 주장의 절반이다: 프롬프트 없이 모든 것을 알아서 분할한다는 주장이 아니다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain why framing the task as *promptable segmentation* makes it suitable for pretraining · "프롬프트 가능한 분할"이라는 과제 정의가 왜 사전학습에 적합한지 설명할 수 있다
- [ ] Describe how the three-stage data engine (assisted-manual → semi-automatic → automatic) produced 1.1 billion masks · 데이터 엔진 3단계(보조 수동→반자동→자동)가 11억 마스크를 만든 과정을 말할 수 있다
- [ ] Separate what SAM knows (boundaries) from what it does not (classes), and name the complementary pairing (detector + SAM) · SAM이 아는 것(경계)과 모르는 것(클래스)을 구분하고, 보완 조합(검출기+SAM)을 말할 수 있다
- [ ] Say why splitting a heavy encoder from a light decoder is decisive for interactive use · 무거운 인코더/가벼운 디코더 분리가 인터랙티브 사용에 왜 결정적인지 말할 수 있다
