---
title: "JEPA Line — From LeCun's Position Paper to I-JEPA and V-JEPA 2"
authors: Yann LeCun (2022) · Mahmoud Assran et al. (I-JEPA) · Meta AI (V-JEPA 1–2)
affiliation: Meta AI (FAIR), NYU
venue: OpenReview 2022 · CVPR 2023 · 2024–2025
year: 2022
pdf: https://openreview.net/forum?id=BZ5a1r-kVsf
arxiv: https://arxiv.org/abs/2301.08243
project: https://arxiv.org/abs/2506.09985
tags: [paper, world-models, self-supervised]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**LeCun, 2022 · Assran et al., CVPR 2023 · Meta AI, 2024–25** — [Position paper](https://openreview.net/forum?id=BZ5a1r-kVsf) · [I-JEPA arXiv](https://arxiv.org/abs/2301.08243) · [V-JEPA 2 arXiv](https://arxiv.org/abs/2506.09985)

> [!note] Math on-ramp · 수학 준비물
> [[02-foundations/calculus-backprop|2. Calculus §5]]'s stop-gradient paragraph and [[02-foundations/information-theory|5. Information Theory §4]]. The architectural claim is negative — predict in representation space *instead of* pixels — so the question to carry is what stops the representation from collapsing to a constant.
> [[02-foundations/calculus-backprop|2. 미적분 §5]]의 stop-gradient 단락과 [[02-foundations/information-theory|5. 정보이론 §4]]. 이 논문의 구조적 주장은 부정형이다 — 픽셀 *대신* 표현 공간에서 예측하라 — 그러므로 들고 갈 질문은 "무엇이 표현이 상수로 붕괴하는 것을 막는가"다.

## English

**One-line summary**: Predict in *representation space*, not pixel space — LeCun's architectural manifesto, made real by I-JEPA (images), V-JEPA (video), and V-JEPA 2 (zero-shot robot planning from 1M hours of video).

### Context

Generative world models ([[dreamer|Dreamer]], [[sora|Sora]]) pay to predict every pixel —
including leaves fluttering and sensor noise that no plan depends on. LeCun's 2022 position
paper ("A Path Towards Autonomous Machine Intelligence") argues the abstraction level is
the bug: predict *abstract representations* of the future, ignore the unpredictable
details, and build hierarchical world models for planning.

### Method

> [!tip] Key intuition
> Don't ask "what will the pixels be?" — ask "what will be *true* about the scene?"
> A Joint-Embedding Predictive Architecture embeds context and target separately and
> predicts the target's *embedding*; whatever is unpredictable (exact textures, noise)
> simply doesn't survive into the representation.

- **JEPA blueprint (2022)**: energy-based, non-generative prediction in latent space;
  proposed hierarchy of world models + a configurable "cost module" — also a broadside
  against autoregressive LLMs as a path to reasoning.
- **I-JEPA (CVPR 2023)**: a context ViT encoder sees one block of an image and predicts
  (via a light predictor) the representations of masked target blocks produced by an
  EMA target encoder — no hand-crafted augmentations, no pixel loss. Strong linear-probe
  features at a fraction of [[mae|MAE]]-style compute.
- **V-JEPA (2024) / V-JEPA 2 (2025)**: the same recipe on video (masked spatiotemporal
  prediction); V-JEPA 2 pretrains on **1M+ hours** of internet video, then a small
  action-conditioned head (V-JEPA 2-AC, ~62h robot data) yields **zero-shot planning** for
  reach/grasp/pick-place on a Franka arm in new labs — plus strong physical-reasoning
  benchmark results.

### Results

- I-JEPA: better linear probes than pixel-reconstruction methods with ~10× less pretraining
  compute on ViT-H.
- V-JEPA 2: state-of-the-art motion understanding and video QA among video encoders;
  planning by optimizing actions against latent predictions works on real robots without
  task-specific training.

### Limitations & critique

- Representation prediction can't *render* — no synthetic data generation, no
  visualization of what the model believes (the [[cosmos|Cosmos]]/[[genie|Genie]] tradeoff
  in reverse).
- Collapse must be prevented by careful EMA/architecture asymmetries; the "cost module"
  and hierarchy of the 2022 blueprint remain mostly unbuilt.
- Robot results are early-stage (short-horizon tabletop) relative to VLA benchmarks.

### Impact & follow-ups

The strongest counter-programme to generative world models — and increasingly the *encoder*
of choice inside them (latent prediction backbones in robot models). The
generative-vs-latent debate ([[sora|Sora]]/[[cosmos|Cosmos]] vs JEPA) is one of the live
questions of physical AI.

> [!question] Reading the claim · 핵심 주장 읽는 법
> Representation prediction is an architectural idea instantiated in different image, video, and robotics studies. Their evidence is not interchangeable. Identify the version, training observations, and downstream procedure before treating a prediction result as a planning capability.

### Connections

- Previous: [[mae|MAE]] (the generative cousin it critiques), [[dreamer|Dreamer]] (latent-space kin)
- Next: latent world models for VLAs · Contrast: [[sora|Sora]], [[cosmos|Cosmos]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 픽셀 공간이 아니라 *표현 공간*에서 예측하라 — LeCun의 구조 선언문이 I-JEPA(이미지), V-JEPA(비디오), V-JEPA 2(100만 시간 비디오로 zero-shot 로봇 플래닝)로 현실화된 계보.

### 배경

생성형 월드모델([[dreamer|Dreamer]], [[sora|Sora]])은 모든 픽셀을 예측하는 값을 치른다 —
어떤 계획도 의존하지 않는 나뭇잎의 흔들림과 센서 노이즈까지. LeCun의 2022년 입장
논문("A Path Towards Autonomous Machine Intelligence")의 주장: 버그는 추상화 수준에 있다.
미래의 *추상 표현*을 예측하고, 예측 불가능한 디테일은 무시하고, 플래닝을 위한 계층적
월드모델을 지어라.

### 방법

> [!tip] 핵심 직관
> "픽셀이 어떻게 될까?"가 아니라 "장면에서 무엇이 *참*이 될까?"를 물어라.
> Joint-Embedding Predictive Architecture는 문맥과 타깃을 따로 임베딩하고 타깃의
> *임베딩*을 예측한다; 예측 불가능한 것(정확한 질감, 노이즈)은 애초에 표현 속에
> 살아남지 못한다.

- **JEPA 청사진 (2022)**: 에너지 기반, 비생성적 잠재 공간 예측; 월드모델의 계층과 구성
  가능한 "비용 모듈"을 제안 — 자기회귀 LLM이 추론으로 가는 길이라는 통념에 대한 정면
  반박이기도 하다.
- **I-JEPA (CVPR 2023)**: 문맥 ViT 인코더가 이미지의 한 블록을 보고, EMA 타깃 인코더가
  만든 마스크된 타깃 블록들의 표현을 (가벼운 예측기로) 예측 — 수작업 증강도, 픽셀 손실도
  없음. [[mae|MAE]]류 대비 몇 분의 일의 연산으로 강한 linear-probe 특징.
- **V-JEPA (2024) / V-JEPA 2 (2025)**: 같은 레시피를 비디오에(마스크된 시공간 예측);
  V-JEPA 2는 인터넷 비디오 **100만 시간 이상**으로 사전학습 후, 작은 행동 조건 헤드(V-JEPA 2-AC,
  로봇 데이터 약 62시간)로 새 실험실의 Franka 팔에서 reach/grasp/pick-place **zero-shot
  플래닝** — 물리 추론 벤치마크에서도 강세.

### 결과

- I-JEPA: ViT-H 기준 약 10분의 1의 사전학습 연산으로 픽셀 복원 기법보다 나은 linear probe.
- V-JEPA 2: 비디오 인코더 중 최고 수준의 운동 이해·비디오 QA; 잠재 예측에 대해 행동을
  최적화하는 플래닝이 과제별 학습 없이 실제 로봇에서 작동.

### 한계와 비판

- 표현 예측은 *렌더링*하지 못한다 — 합성 데이터 생성도, 모델의 믿음의 시각화도 불가
  ([[cosmos|Cosmos]]/[[genie|Genie]] 트레이드오프의 정반대편).
- 붕괴(collapse)를 EMA/구조 비대칭으로 조심스럽게 막아야 한다; 2022 청사진의 "비용 모듈"과
  계층 구조는 대부분 아직 지어지지 않았다.
- 로봇 결과는 VLA 벤치마크 대비 초기 단계(짧은 지평의 탁상 과제).

### 영향과 후속 연구

생성형 월드모델에 대한 가장 강력한 대항 프로그램 — 그리고 점점 그 생성형 모델들 *안의*
인코더로 채택되는 중(로봇 모델의 잠재 예측 백본). 생성 vs 잠재
논쟁([[sora|Sora]]/[[cosmos|Cosmos]] vs JEPA)은 physical AI의 살아 있는 쟁점 중 하나다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 표현 예측은 영상·비디오·로봇 연구에서 서로 다르게 구현된 구조 아이디어다. 증거를 서로 바꿔 쓸 수 없다. 예측 결과를 계획 능력으로 읽기 전에 버전, 학습 관측, 후속 절차를 확인한다.

### 연결

- 이전: [[mae|MAE]] (비판 대상인 생성형 사촌), [[dreamer|Dreamer]] (잠재 공간의 친척)
- 다음: VLA를 위한 잠재 월드모델 · 대비: [[sora|Sora]], [[cosmos|Cosmos]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Give the argument for predicting representations rather than pixels · 픽셀 예측 대신 표현 예측이라는 논거를 설명할 수 있다
- [ ] Name I-JEPA's three parts (context encoder, target encoder, predictor) and the role of the EMA · I-JEPA의 세 부품(문맥 인코더/타깃 인코더/예측기)과 EMA의 역할을 말할 수 있다
- [ ] Outline V-JEPA 2's zero-shot robot planning procedure · V-JEPA 2의 zero-shot 로봇 플래닝 절차를 개요 수준에서 말할 수 있다
- [ ] State the trade-off of not being able to render (the contrast with the generative camp) · 렌더링 불가라는 트레이드오프(생성 진영과의 대비)를 말할 수 있다
