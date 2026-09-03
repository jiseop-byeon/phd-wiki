---
title: "Dex-Net 2.0 — Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics"
authors: Jeffrey Mahler, Jacky Liang, Sherdil Niyaz, et al.
affiliation: UC Berkeley
venue: RSS
year: 2017
arxiv: https://arxiv.org/abs/1703.09312
pdf: https://arxiv.org/pdf/1703.09312
project: http://berkeleyautomation.github.io/dex-net
tags: [paper, manipulation, grasping]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when grasp synthesis is part of the thesis contribution."
---

**Mahler et al., RSS 2017** — [arXiv](https://arxiv.org/abs/1703.09312) · [PDF](https://arxiv.org/pdf/1703.09312) · [Official](http://berkeleyautomation.github.io/dex-net)

> [!note] Math on-ramp · 수학 준비물
> You need the analytic side first: friction cones, force closure, and the $\epsilon$ quality metric ([[04-robotics/grasping|15. §2–§4]]) — because those are literally the labels this network is trained on. Then supervised classification from images ([[02-foundations/neural-network-basics|0.7]]).
> 해석적 쪽이 먼저다: 마찰 원뿔, force closure, $\epsilon$ 품질 지표([[04-robotics/grasping|15. §2~§4]]) — 이 네트워크가 학습하는 라벨이 문자 그대로 그것들이기 때문이다. 그다음 이미지로부터의 지도 분류([[02-foundations/neural-network-basics|0.7]]).

## English

**One-line summary**: Train a grasp-quality CNN entirely on synthetic depth images paired with analytic grasp metrics, so robust grasps can be predicted from a depth image with no real-world grasp attempts in training.

### Context

Two traditions had stalled against each other. Analytic grasp planning ([[04-robotics/grasping|15. §2–§4]]) is principled but needs an object model and a friction estimate. Learning from real grasp attempts is model-free but needs an enormous number of physical trials.

### Method

> [!tip] Key intuition
> Do not choose between them — compose them. Let the analytic theory *label* a synthetic dataset, and let a network learn to predict those labels from depth images. The physics generates the supervision; the network supplies the speed and the tolerance to real sensor noise.

The pipeline is the one drawn in [[04-robotics/grasping|15. §5]]: object models → simulated grasps → analytic quality → labelled dataset → a network mapping depth image to grasp score.

### Results

All figures below are **from the paper's own abstract**:

- **6.7 million** point clouds, grasps, and analytic grasp metrics in the dataset.
- Grasps planned in **0.8 s** with a **93% success rate** on eight known objects with adversarial geometry, over **1,000 trials** on an ABB YuMi.
- **3× faster** than registering point clouds to a precomputed dataset.
- **99% precision** — one false positive out of 69 grasps classified as robust — on a dataset of **40 novel household objects**.

### Limitations & critique

- **The analytic label is the assumption.** The network can only learn the quality function it was shown, so the whole result rests on the simulated contact physics being a good enough proxy — including an assumed $\mu$, which [[04-robotics/grasping|15. §6]] says is exactly what a construction site will not give you.
- Planar, parallel-jaw, top-down grasps on rigid objects. The later 6-DoF work ([[01-canonical-papers/notes/7-robotics/anygrasp|AnyGrasp]], Contact-GraspNet) exists because this scope is narrow.
- Isolated objects, not dense clutter.
- "99% precision" is a precision figure on classified-robust grasps, not a success rate — read the two numbers as answering different questions.

> [!question] Reading the claim · 핵심 주장 읽는 법
> The network predicts a robustness label defined by the analytic training model. It does not remove that model’s contact assumptions. Check the friction and grasp family, and distinguish precision among accepted grasps from success across all attempted tasks.

### Connections

- [[04-robotics/grasping|15. Grasping]] — the concept page, whose §5 is this pipeline
- [[01-canonical-papers/notes/7-robotics/anygrasp|AnyGrasp]] — where the line went next

### After reading

- [ ] Explain what the analytic theory is doing inside a learned pipeline.
- [ ] Name the assumption the whole result rests on.
- [ ] Distinguish the 93% and the 99% and say what each measures.

## 한국어

**한 줄 요약**: 해석적 파지 지표와 짝지은 합성 깊이 이미지만으로 파지 품질 CNN을 학습시켜, 학습에 실제 파지 시도를 하나도 쓰지 않고 깊이 이미지에서 견고한 파지를 예측한다.

### 배경

두 전통이 서로에게 막혀 있었다. 해석적 파지 계획([[04-robotics/grasping|15. §2~§4]])은 원리적이지만 물체 모델과 마찰 추정치가 필요하다. 실제 파지 시도로부터의 학습은 모델이 필요 없지만 엄청난 수의 물리적 시행이 필요하다.

### 방법

> [!tip] 핵심 직관
> 둘 중 하나를 고르지 말고 합성하라. 해석 이론이 합성 데이터셋에 *라벨을 붙이게* 하고, 네트워크가 깊이 이미지에서 그 라벨을 예측하도록 배우게 하라. 물리가 지도 신호를 만들고, 네트워크가 속도와 실제 센서 잡음에 대한 관용을 공급한다.

파이프라인은 [[04-robotics/grasping|15. §5]]에 그려진 그것이다: 물체 모델 → 시뮬레이션 파지 → 해석적 품질 → 라벨된 데이터셋 → 깊이 이미지에서 파지 점수로 가는 네트워크.

### 결과

아래 수치는 전부 **논문 자신의 초록**에서 온 것이다:

- 데이터셋에 포인트 클라우드·파지·해석 지표 **670만 개**.
- ABB YuMi에서 **1,000회 이상 시행**, 적대적 형상의 알려진 물체 8개에 대해 **0.8초** 계획에 **93% 성공률**.
- 미리 계산된 데이터셋에 포인트 클라우드를 정합하는 것보다 **3배 빠름**.
- 새로운 생활용품 **40개** 데이터셋에서 **99% 정밀도** — robust로 분류한 파지 69개 중 거짓 양성 1개.

### 한계와 비판

- **해석적 라벨이 곧 가정이다.** 네트워크는 자기가 본 품질 함수만 배울 수 있으므로, 결과 전체가 시뮬레이션 접촉 물리가 충분히 좋은 대리라는 데 걸려 있다 — 가정된 $\mu$까지 포함해서. [[04-robotics/grasping|15. §6]]이 말하듯 건설 현장이 주지 않는 것이 정확히 그것이다.
- 강체 물체에 대한 평면·평행 조·위에서 내려오는 파지. 이후의 6자유도 연구([[01-canonical-papers/notes/7-robotics/anygrasp|AnyGrasp]], Contact-GraspNet)가 존재하는 이유가 이 범위의 좁음이다.
- 조밀한 잡동사니가 아니라 고립된 물체.
- "99% 정밀도"는 robust로 분류된 파지에 대한 정밀도이지 성공률이 아니다 — 두 숫자를 서로 다른 질문에 답하는 것으로 읽어라.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 망은 해석적 학습 모델이 정의한 강건성 라벨을 예측한다. 그 모델의 접촉 가정을 없애지는 않는다. 마찰과 파지 종류를 확인하고 채택한 파지의 정밀도와 전체 시도 과제의 성공을 구분한다.

### 연결

- [[04-robotics/grasping|15. 파지]] — §5가 이 파이프라인인 개념 페이지
- [[01-canonical-papers/notes/7-robotics/anygrasp|AnyGrasp]] — 이 계보가 다음에 간 곳

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 학습 파이프라인 안에서 해석 이론이 무엇을 하고 있는지 설명한다.
- [ ] 결과 전체가 걸려 있는 가정을 댄다.
- [ ] 93%와 99%를 구분하고 각각이 무엇을 재는지 말한다.
