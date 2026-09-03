---
title: "Genie — Generative Interactive Environments"
authors: Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, et al.
affiliation: Google DeepMind, University of British Columbia
venue: ICML
year: 2024
arxiv: https://arxiv.org/abs/2402.15391
pdf: https://arxiv.org/pdf/2402.15391
project: https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/
tags: [paper, world-models, generative]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Bruce et al., ICML 2024** — [arXiv](https://arxiv.org/abs/2402.15391) · [PDF](https://arxiv.org/pdf/2402.15391) · [Genie 2 (Official)](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/5-world-models/world-models|World Models]] and [[02-foundations/information-theory|5. Information Theory §5]] (latent variables and the ELBO). The distinctive move — learning a latent *action* space from unlabeled video — is a latent-variable argument, so hold that section's definition of "latent" firmly.
> [[01-canonical-papers/notes/5-world-models/world-models|World Models]]와 [[02-foundations/information-theory|5. 정보이론 §5]](잠재변수와 ELBO). 이 논문의 독특한 수 — 레이블 없는 영상에서 잠재 *행동* 공간을 배우는 것 — 은 잠재변수 논증이므로, 그 절의 "잠재" 정의를 단단히 붙들고 가라.

## English

**One-line summary**: From ~30k hours of *unlabeled* gameplay video (filtered from a ~244k-hour crawl), learn a latent action space and an action-controllable video model — turning any image into a playable world, no action labels ever provided.

### Context

World models so far needed action-labeled experience ([[dreamer|Dreamer]]'s own rollouts,
robot teleop logs) — exactly the scarce resource. The internet has endless video but no
action labels. Genie's question: can *actions themselves* be discovered unsupervised from
video, making the whole internet a training ground for interactive environments?

### Method

> [!tip] Key intuition
> Between two consecutive frames, *something* happened — call it a latent action. Force all
> frame-to-frame transitions through a tiny discrete codebook (8 codes), and the model must
> invent a consistent, controllable action vocabulary on its own.

- Three parts, all spatiotemporal transformers (11B total):
  **video tokenizer** (VQ) → **latent action model** (infers the discrete action between
  frames, 8-code codebook) → **dynamics model** (MaskGIT-style, predicts next frame tokens
  given history + latent action).
- Trained on ~30k hours of 2D-platformer internet video (filtered down from ~244k crawled hours), *no labels of any kind*.
- At inference: prompt with any image (photo, sketch), then *play* it frame by frame by
  choosing latent actions.

### Results

**What it measured.** Per the [abstract](https://arxiv.org/abs/2402.15391): The model has 11B parameters. That is model size, not a behavioral score; the abstract reports no quantitative result for controllability or physical fidelity.

- The learned 8-action space is consistent across prompts (maps to left/right/jump-like
  controls) — semantics of control emerge without supervision.
- Generalizes to out-of-distribution prompts: real photos and hand drawings become
  playable worlds.
- Demonstrated latent actions transfer: policies can be trained in imagined environments
  and mapped to real action spaces — a path to RL without action-labeled data.
- **Genie 2 (2024)**: scaled to 3D worlds with minutes-long consistent rollouts, framed as
  a training ground for embodied agents.

### Limitations & critique

- 1 FPS interaction and short consistent horizons (v1); hallucinated physics — plausible ≠
  correct, the standing issue for using generated worlds as training grounds.
- 2D-game-biased data (v1); latent actions may not match real robot action granularity.
- Closed models; evaluation of "world quality" remains ad hoc.

### Impact & follow-ups

Founded the *foundation world model* category: world models trained on internet video
rather than an agent's own experience. Genie 2 and [[cosmos|Cosmos]] compete to be the
simulator that generates embodied training data at scale — the base of
[[gr00t-n1|GR00T]]'s data pyramid.

> [!question] Reading the claim · 핵심 주장 읽는 법
> Action-controllable generated video demonstrates a learned interactive representation. It does not establish physically accurate dynamics or alignment between latent actions and robot controls. Check what an action changes and how consistency is evaluated across time.

### Connections

- Previous: [[dreamer|Dreamer]] (agent-experience world models), [[vae|VQ-VAE machinery]]
- Parallel: [[sora|Sora]] (video generation as simulation, no actions) · Next: [[cosmos|Cosmos]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: *라벨 없는* 게임플레이 비디오 약 3만 시간(약 24.4만 시간 크롤에서 필터링)에서 잠재 행동 공간과 행동 제어 가능한 비디오 모델을 학습 — 행동 라벨을 한 번도 주지 않고, 아무 이미지나 플레이 가능한 세계로 바꾼다.

### 배경

지금까지의 월드모델은 행동 라벨이 달린 경험([[dreamer|Dreamer]]의 자체 롤아웃, 로봇
원격조작 로그)이 필요했다 — 정확히 그 희소 자원 말이다. 인터넷에는 비디오가 무한하지만
행동 라벨이 없다. Genie의 질문: *행동 그 자체*를 비디오에서 비지도로 발견해서, 인터넷
전체를 상호작용 환경의 훈련장으로 만들 수 있을까?

### 방법

> [!tip] 핵심 직관
> 연속된 두 프레임 사이에 *무언가* 일어났다 — 그것을 잠재 행동이라 부르자. 모든 프레임 간
> 전이를 아주 작은 이산 코드북(8개)에 통과시키도록 강제하면, 모델은 일관되고 제어 가능한
> 행동 어휘를 스스로 발명할 수밖에 없다.

- 세 부분, 모두 시공간 트랜스포머 (총 11B):
  **비디오 토크나이저**(VQ) → **잠재 행동 모델**(프레임 사이의 이산 행동을 추론, 8코드
  코드북) → **동역학 모델**(MaskGIT식, 이력 + 잠재 행동에서 다음 프레임 토큰 예측).
- 2D 플랫포머 인터넷 비디오 약 3만 시간(약 24.4만 시간 크롤에서 필터링)으로 학습, *어떤 라벨도 없이*.
- 추론: 아무 이미지(사진, 스케치)로 프롬프트한 뒤 잠재 행동을 골라가며 프레임 단위로 *플레이*.

### 결과

**무엇을 쟀는가.** [초록](https://arxiv.org/abs/2402.15391) 기준: 모델 크기는 11B 파라미터다. 행동 점수가 아니다. 초록에 제어 가능성이나 물리적 충실도의 정량 결과는 없다.

- 학습된 8개 행동 공간이 프롬프트를 가로질러 일관된다(좌/우/점프류 조작에 대응) —
  감독 없이 제어의 의미론이 창발.
- 분포 밖 프롬프트로 일반화: 실사진과 손그림이 플레이 가능한 세계가 된다.
- 잠재 행동의 전이 가능성 시연: 상상된 환경에서 정책을 학습해 실제 행동 공간으로 매핑 —
  행동 라벨 없는 RL로 가는 길.
- **Genie 2 (2024)**: 3D 세계로 확장, 수 분 길이의 일관된 롤아웃 — 체화 에이전트의
  훈련장으로 자리매김.

### 한계와 비판

- 1 FPS 상호작용과 짧은 일관성 지평(v1); 환각된 물리 — 그럴듯함 ≠ 정확함, 생성된 세계를
  훈련장으로 쓸 때의 상시 문제.
- 2D 게임 편향 데이터(v1); 잠재 행동이 실제 로봇 행동의 입도와 안 맞을 수 있다.
- 비공개 모델; "세계 품질"의 평가가 여전히 임기응변적.

### 영향과 후속 연구

*파운데이션 월드모델* 범주를 창시했다: 에이전트 자신의 경험이 아니라 인터넷 비디오로
학습되는 월드모델. Genie 2와 [[cosmos|Cosmos]]가 체화 학습 데이터를 대규모로 생성하는
시뮬레이터 자리를 두고 경쟁 중 — [[gr00t-n1|GR00T]] 데이터 피라미드의 바닥이다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 행동으로 제어하는 생성 영상은 학습한 상호작용 표현을 보여 준다. 물리적으로 정확한 동역학이나 잠재 행동과 로봇 제어의 정렬을 확립하지 않는다. 행동이 바꾸는 것과 시간 일관성의 평가를 확인한다.

### 연결

- 이전: [[dreamer|Dreamer]] (에이전트 경험 월드모델), [[vae|VQ-VAE 기계장치]]
- 병행: [[sora|Sora]] (행동 없는, 시뮬레이션으로서의 비디오 생성) · 다음: [[cosmos|Cosmos]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain the mechanism by which latent actions are discovered (the 8-code bottleneck) · 잠재 행동이 발견되는 메커니즘(8-코드 병목)을 설명할 수 있다
- [ ] Name the three components (tokenizer, latent action model, dynamics model) · 세 구성요소(토크나이저/잠재 행동 모델/동역학 모델)를 말할 수 있다
- [ ] State what it means to claim that action-unlabeled internet video becomes a training ground · 행동 라벨 없는 인터넷 비디오가 훈련장이 된다는 주장의 의미를 말할 수 있다
- [ ] State the plausible ≠ physically correct problem · 그럴듯함 ≠ 물리적 정확함 문제를 말할 수 있다
