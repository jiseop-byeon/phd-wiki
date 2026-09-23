---
title: "JEPA Line — From LeCun's Position Paper to I-JEPA, V-JEPA 2 and LeWorldModel"
authors: Yann LeCun (2022) · Mahmoud Assran et al. (I-JEPA) · Meta AI (V-JEPA 1–2) · Balestriero & LeCun (LeJEPA) · Maes et al. (LeWorldModel)
affiliation: Meta AI (FAIR), NYU
venue: OpenReview 2022 · CVPR 2023 · 2024–2026
year: 2022
pdf: https://openreview.net/forum?id=BZ5a1r-kVsf
arxiv: https://arxiv.org/abs/2301.08243
project: https://arxiv.org/abs/2506.09985
tags: [paper, world-models, self-supervised]
status: note-complete
last_verified: 2026-09-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**LeCun, 2022 · Assran et al., CVPR 2023 · Meta AI, 2024–25 · 2025–26 follow-ups** — [Position paper](https://openreview.net/forum?id=BZ5a1r-kVsf) · [I-JEPA arXiv](https://arxiv.org/abs/2301.08243) · [V-JEPA 2 arXiv](https://arxiv.org/abs/2506.09985) · [LeJEPA arXiv](https://arxiv.org/abs/2511.08544) · [LeWorldModel arXiv](https://arxiv.org/abs/2603.19312)

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

- I-JEPA: better linear probes with ~10× less pretraining compute than MAE specifically, a body
  comparison — the abstract gives only the absolute cost, 16 A100 GPUs in under 72 hours. Less pretraining
  compute on ViT-H.
- V-JEPA 2: state-of-the-art motion understanding and video QA among video encoders;
  planning by optimizing actions against latent predictions works on real robots without
  task-specific training.

### Limitations & critique

- Representation prediction can't *render* — no synthetic data generation, no
  visualization of what the model believes (the [[cosmos|Cosmos]]/[[genie|Genie]] tradeoff
  in reverse).
- Collapse had to be prevented by careful EMA/architecture asymmetries until LeJEPA (2025)
  replaced those heuristics with one regularizer; the "cost module" and hierarchy of the 2022
  blueprint remain mostly unbuilt.
- Robot results are early-stage (short-horizon tabletop) relative to VLA benchmarks. A 2026
  preprint audit, ARC-Bench, reports that released JEPA world models often rank candidate
  actions wrongly in manipulation — the top-scored action is usually not the best — and that
  closed-loop replanning hides the defect.

### Impact & follow-ups

The strongest counter-programme to generative world models — and increasingly the *encoder*
of choice inside them (latent prediction backbones in robot models). The
generative-vs-latent debate ([[sora|Sora]]/[[cosmos|Cosmos]] vs JEPA) is one of the live
questions of physical AI.

**After V-JEPA 2 (2025–2026).**

- **LeJEPA** (Balestriero & LeCun, 2025): a theory of JEPAs that finds the isotropic Gaussian to be the embedding distribution that minimizes downstream prediction risk, and one regularizer, SIGReg, that pushes embeddings toward it — a single trade-off hyperparameter and linear time and memory, in place of the EMA and stop-gradient heuristics above.
- **Planning in a JEPA-style latent.** DINO-WM (Zhou, Pan, LeCun and Pinto, 2024) learns dynamics on frozen DINOv2 patch features from offline trajectories and plans toward an image goal by optimizing actions; PLDM (Sobal et al., 2025) sets such latent-dynamics planning against offline RL on reward-free navigation data. **LeWorldModel** (Maes, Le Lidec, Scieur, LeCun and Balestriero, 2026) is the first JEPA trained stably end to end from pixels with two loss terms, a next-embedding prediction and a Gaussian regularizer: about $15$M parameters, a single GPU for a few hours, planning up to $48$ times faster than foundation-model-based world models while staying competitive on 2D and 3D control tasks.
- **VL-JEPA** (Chen et al., 2025) carries the idea to vision–language: it predicts the embedding of the answer text instead of its tokens, with $50\%$ fewer trainable parameters than a token-space model in a controlled comparison and $2.85$ times fewer decoding operations when it decodes selectively.
- **The 2026 robotics wave.** Action-conditioned JEPA world models for goal-conditioned robot planning, JEPA-space vision–language–action policies (JEPA-WAM) and JEPA-style imitation (JEPA Policy) appeared within a few months, mostly as unreviewed preprints. Read them with the ARC-Bench audit above in hand: a planner is only as good as the ranking its latent distance produces.
- **AMI Labs.** LeCun left Meta and launched AMI Labs in Paris in March 2026 to build JEPA-based world models for robotics and industry ([TechCrunch](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/), 2026-03-09). LeWorldModel, the line's planning paper of that month, lists Mila, NYU, Samsung SAIL and Brown as affiliations. Where the line sits among the other things called world models is [[03-deep-learning/world-models/index|5. World Models §6]].

> [!question] Reading the claim · 핵심 주장 읽는 법
> Representation prediction is an architectural idea instantiated in different image, video, and robotics studies. Their evidence is not interchangeable. Identify the version, training observations, and downstream procedure before treating a prediction result as a planning capability.

### Connections

- Previous: [[mae|MAE]] (the generative cousin it critiques), [[dreamer|Dreamer]] (latent-space kin)
- Next: latent world models for VLAs, LeWorldModel · Contrast: [[sora|Sora]], [[cosmos|Cosmos]], [[world-labs|World Labs]]
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
- 붕괴(collapse)는 EMA/구조 비대칭으로 조심스럽게 막아야 했다. LeJEPA(2025)가 그 요령들을
  정규화 항 하나로 바꾸기 전까지다. 2022 청사진의 "비용 모듈"과 계층 구조는 대부분 아직
  지어지지 않았다.
- 로봇 결과는 VLA 벤치마크 대비 초기 단계(짧은 지평의 탁상 과제). 2026년의 프리프린트 감사
  ARC-Bench는 공개된 JEPA 월드모델이 조작 과제에서 행동 후보의 순위를 자주 틀리게 매긴다고
  보고한다 — 가장 높은 점수를 받은 행동이 대개 최선이 아니다 — 그리고 폐루프 재계획이 그
  결함을 가린다고 한다.

### 영향과 후속 연구

생성형 월드모델에 대한 가장 강력한 대항 프로그램 — 그리고 점점 그 생성형 모델들 *안의*
인코더로 채택되는 중(로봇 모델의 잠재 예측 백본). 생성 vs 잠재
논쟁([[sora|Sora]]/[[cosmos|Cosmos]] vs JEPA)은 physical AI의 살아 있는 쟁점 중 하나다.

**V-JEPA 2 이후 (2025–2026).**

- **LeJEPA**(Balestriero·LeCun, 2025): JEPA의 이론으로, 하류 예측 위험을 최소로 하는 임베딩 분포가 등방성 가우시안임을 보이고, 임베딩을 그쪽으로 미는 정규화 항 하나(SIGReg)를 낸다. 위의 EMA·stop-gradient 요령 대신 교환 하이퍼파라미터 하나와 선형 시간·메모리로 된다.
- **JEPA식 잠재 공간에서 계획하기.** DINO-WM(Zhou, Pan, LeCun, Pinto, 2024)은 고정된 DINOv2 패치 특징 위에서 오프라인 궤적으로 동역학을 배우고, 행동을 최적화해 이미지 목표로 계획한다. PLDM(Sobal 외, 2025)은 그런 잠재 동역학 계획을 보상 없는 내비게이션 데이터 위의 오프라인 RL과 견준다. **LeWorldModel**(Maes, Le Lidec, Scieur, LeCun, Balestriero, 2026)은 픽셀에서 끝까지 안정적으로 학습하는 첫 JEPA로, 손실 항은 다음 임베딩 예측과 가우시안 정규화 둘뿐이다. 파라미터 약 $1{,}500$만 개, GPU 한 장으로 몇 시간이면 학습되고, 2D·3D 제어 과제에서 경쟁력을 유지하면서 파운데이션 모델 기반 월드모델보다 최대 $48$배 빨리 계획한다.
- **VL-JEPA**(Chen 외, 2025)는 이 발상을 시각–언어로 옮긴다. 답 텍스트의 토큰이 아니라 임베딩을 예측하며, 통제된 비교에서 토큰 공간 모델보다 학습 파라미터가 $50\%$ 적고, 선택적으로 디코딩하면 디코딩 연산이 $2.85$배 줄어든다.
- **2026년의 로봇 물결.** 목표 조건 로봇 계획을 위한 행동 조건 JEPA 월드모델, JEPA 공간의 시각–언어–행동 정책(JEPA-WAM), JEPA식 모방학습(JEPA Policy)이 몇 달 사이에 나왔고, 대부분 심사 전 프리프린트다. 위의 ARC-Bench 감사를 손에 들고 읽어라. 플래너는 잠재 거리가 만드는 순위만큼만 좋다.
- **AMI Labs.** LeCun은 Meta를 떠나 2026년 3월 파리에서 AMI Labs를 출범시켰고, 로봇과 산업을 위한 JEPA 기반 월드모델을 만든다고 밝혔다([TechCrunch](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/), 2026-03-09). 같은 달 나온 이 계열의 계획 논문 LeWorldModel의 소속은 Mila, NYU, Samsung SAIL, Brown이다. 이 계열이 "월드모델"이라 불리는 다른 것들 사이 어디에 서는지는 [[03-deep-learning/world-models/index|5. 월드모델 §6]]에 있다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 표현 예측은 영상·비디오·로봇 연구에서 서로 다르게 구현된 구조 아이디어다. 증거를 서로 바꿔 쓸 수 없다. 예측 결과를 계획 능력으로 읽기 전에 버전, 학습 관측, 후속 절차를 확인한다.

### 연결

- 이전: [[mae|MAE]] (비판 대상인 생성형 사촌), [[dreamer|Dreamer]] (잠재 공간의 친척)
- 다음: VLA를 위한 잠재 월드모델, LeWorldModel · 대비: [[sora|Sora]], [[cosmos|Cosmos]], [[world-labs|World Labs]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Give the argument for predicting representations rather than pixels · 픽셀 예측 대신 표현 예측이라는 논거를 설명할 수 있다
- [ ] Name I-JEPA's three parts (context encoder, target encoder, predictor) and the role of the EMA · I-JEPA의 세 부품(문맥 인코더/타깃 인코더/예측기)과 EMA의 역할을 말할 수 있다
- [ ] Outline V-JEPA 2's zero-shot robot planning procedure · V-JEPA 2의 zero-shot 로봇 플래닝 절차를 개요 수준에서 말할 수 있다
- [ ] State the trade-off of not being able to render (the contrast with the generative camp) · 렌더링 불가라는 트레이드오프(생성 진영과의 대비)를 말할 수 있다
- [ ] Say what LeJEPA's SIGReg replaces, and what LeWorldModel shows about the cost of planning in a latent · LeJEPA의 SIGReg가 무엇을 대신하는지, LeWorldModel이 잠재 공간 계획의 비용에 대해 무엇을 보이는지 말할 수 있다
