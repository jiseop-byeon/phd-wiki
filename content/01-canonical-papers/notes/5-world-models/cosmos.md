---
title: "Cosmos — World Foundation Model Platform for Physical AI"
authors: NVIDIA (Niket Agarwal, Arslan Ali, Maciej Bala, et al.)
affiliation: NVIDIA
venue: arXiv
year: 2025
arxiv: https://arxiv.org/abs/2501.03575
pdf: https://arxiv.org/pdf/2501.03575
code: https://github.com/nvidia-cosmos/cosmos-predict1
tags: [paper, world-models, generative]
status: note-complete
last_verified: 2026-09-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**NVIDIA, 2025** — [arXiv](https://arxiv.org/abs/2501.03575) · [PDF](https://arxiv.org/pdf/2501.03575) · [Code](https://github.com/nvidia-cosmos/cosmos-predict1)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]] and [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]] (the generator halves), plus [[05-construction-robotics/sim-to-real|Sim-to-Real §4]] — the claim that matters here is whether generated video is *usable as training experience*, which is a transfer-evidence question, not a video-quality one.
> [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]과 [[01-canonical-papers/notes/6-diffusion/latent-diffusion|잠재 디퓨전]](생성기 절반), 그리고 [[05-construction-robotics/sim-to-real|Sim-to-Real §4]] — 여기서 중요한 주장은 생성된 영상이 *학습 경험으로 쓸 수 있는가*이고, 그것은 영상 품질이 아니라 전이 증거의 문제다.

## English

**One-line summary**: An open platform of video world foundation models — tokenizers plus diffusion and autoregressive generators pretrained on ~20M hours of raw video — built to be *post-trained* into simulators, data engines, and policy evaluators for robots and autonomous vehicles.

### Context

[[sora|Sora]] showed video generation scales; [[genie|Genie]] showed actions can be learned
in; [[gr00t-n1|GR00T]]'s data pyramid needs a middle layer of synthetic experience. What was
missing: an *open, reusable* stack purpose-built for physical AI — where the video model is
not the product but the **infrastructure** other robot models train on.

### Method

> [!tip] Key intuition
> Treat the world model like a foundation LLM: pretrain generalist video models on
> internet-scale physical data, then let each robotics team *post-train* them into what
> they need — a camera-conditioned simulator, a synthetic data generator, or a
> policy-evaluation environment.

- **Data**: ~20M hours of **raw** video, curated down to about 10^8 clips for pretraining (driving, manipulation,
  human activity), heavy filtering/dedup pipelines described openly.
- **Tokenizers (Cosmos Tokenizer)**: continuous and discrete video tokenizers at multiple
  compression rates — released standalone, widely reused.
- **Two WFM families**: diffusion-based ([[ddpm|DDPM]]-lineage, continuous latents) and
  autoregressive ([[gpt-3|GPT]]-lineage, discrete tokens) video generators (up to ~14B),
  both text/image/video-conditionable.
- **Post-training recipes**: camera-controlled generation, robot instruction-following
  video prediction, multi-view driving generation — plus guardrail models; weights and
  code released openly.

### Results

**What it measured.** The abstract reports no quantitative result. [Abstract checked](https://arxiv.org/abs/2501.03575).

- Competitive video generation focused on *physical plausibility* benchmarks (3D
  consistency, physics alignment) rather than aesthetics.
- Demonstrated post-trained variants for robotics and autonomous driving downstream tasks;
  tokenizers outperform prior open video tokenizers.
- Functions as the world-model layer of the [[gr00t-n1|GR00T]] ecosystem (synthetic/neural
  trajectory generation).

### Limitations & critique

- Physics correctness is still benchmark-limited; generated data inherits generator biases —
  the sim-to-real question just moves up one level.
- Enormous training footprint (~10k H100s); "open" at weights level, not reproducible at
  data level.
- Platform breadth (tokenizer/diffusion/AR/guardrails) makes rigorous comparison to
  single-purpose world models hard.

### Impact & follow-ups

The clearest industrial bet that **world models are infrastructure for physical AI**:
synthetic data for [[gr00t-n1|GR00T]]-class VLAs, closed-loop policy evaluation, and
Cosmos-Reason/Transfer successors. For data-scarce domains — construction sites included —
this "pretrain a world model, post-train to your domain" pattern is the one to watch.

**The families since.**

- **Cosmos-Transfer1** (March 2025): world generation controlled by segmentation, depth or edge maps with adaptive weights across the frame — aimed at sim-to-real and at enriching driving data.
- **Cosmos-Reason1** (March 2025; 7B and 56B): a vision–language model for physical common sense that states embodied decisions, such as the next step, in language through long chains of thought.
- **Cosmos-Predict2.5** and **Cosmos-Transfer2.5** (October 2025): Predict2.5 is flow-based, unifies text-, image- and video-to-world generation, uses Cosmos-Reason1 to ground its text, trains on 200M curated clips and comes at 2B and 14B, for synthetic data, policy evaluation and closed-loop simulation; Transfer2.5 translates sim-to-real and real-to-real at 3.5 times smaller than Transfer1. Released under the NVIDIA Open Model License.
- A **Cosmos-Reason2-2B** model is the vision–language backbone of [[gr00t-n1|GR00T N1.7]].

In [[03-deep-learning/world-models/index|5. World Models §6]]'s terms, Predict and Transfer are renderers built to feed planners, and Reason has become part of one.

> [!question] Reading the claim · 핵심 주장 읽는 법
> "World foundation model platform" is a claim about a platform — reusable infrastructure — not a claim to have achieved accurate physical simulation; the paper itself concedes the physics benchmarks remain approximate. Read it as a declaration of what is being built rather than of what has been achieved.

### Connections

- Previous: [[sora|Sora]] (the thesis), [[genie|Genie]] (interactivity), [[ddpm|DDPM]]/[[gpt-3|GPT]] (the two generator families)
- Next: GR00T data pipelines, Cosmos-Reason/Transfer · Domain link: [[05-construction-robotics/index|construction robotics]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 오픈 비디오 월드 파운데이션 모델 플랫폼 — 약 2천만 시간의 **원본** 비디오에서 선별한 데이터로 사전학습된 토크나이저 + 디퓨전·자기회귀 생성기 — 로봇과 자율주행을 위한 시뮬레이터·데이터 엔진·정책 평가기로 *사후학습*되도록 설계됐다.

### 배경

[[sora|Sora]]는 비디오 생성이 스케일함을, [[genie|Genie]]는 행동을 학습해 넣을 수 있음을
보였고, [[gr00t-n1|GR00T]]의 데이터 피라미드는 합성 경험이라는 중간층을 필요로 한다.
빠져 있던 것: physical AI 전용의 *열려 있고 재사용 가능한* 스택 — 비디오 모델이 제품이
아니라 다른 로봇 모델들이 그 위에서 학습하는 **인프라**인 것.

### 방법

> [!tip] 핵심 직관
> 월드모델을 파운데이션 LLM처럼 다뤄라: 인터넷 규모의 물리 데이터로 범용 비디오 모델을
> 사전학습하고, 각 로보틱스 팀이 필요한 것으로 *사후학습*하게 하라 — 카메라 조건
> 시뮬레이터든, 합성 데이터 생성기든, 정책 평가 환경이든.

- **데이터**: 약 2천만 시간의 **원본** 비디오를 물리 동역학 중심으로 선별해 사전학습용 약 10^8개 클립으로 줄인 것(주행, 조작, 인간 활동),
  필터링/중복 제거 파이프라인을 공개적으로 기술.
- **토크나이저(Cosmos Tokenizer)**: 여러 압축률의 연속·이산 비디오 토크나이저 —
  단독 공개되어 널리 재사용됨.
- **두 WFM 계열**: 디퓨전 기반([[ddpm|DDPM]] 계보, 연속 잠재)과 자기회귀
  기반([[gpt-3|GPT]] 계보, 이산 토큰) 비디오 생성기(최대 ~14B), 모두 텍스트/이미지/비디오
  조건 가능.
- **사후학습 레시피**: 카메라 제어 생성, 로봇 지시-추종 비디오 예측, 다중 시점 주행 생성 —
  가드레일 모델 포함; 가중치와 코드 공개.

### 결과

**무엇을 쟀는가.** 초록에 정량 결과가 제시되지 않았다. [초록 확인](https://arxiv.org/abs/2501.03575).

- 미적 품질보다 *물리적 그럴듯함* 벤치마크(3D 일관성, 물리 정합)에 집중한 경쟁력 있는
  비디오 생성.
- 로보틱스·자율주행 다운스트림용 사후학습 변형 시연; 토크나이저는 기존 오픈 비디오
  토크나이저를 능가.
- [[gr00t-n1|GR00T]] 생태계의 월드모델 층으로 기능 (합성/신경 궤적 생성).

### 한계와 비판

- 물리 정확성은 여전히 벤치마크 수준에 갇혀 있다; 생성된 데이터는 생성기의 편향을
  물려받는다 — sim-to-real 문제가 한 층 위로 이동했을 뿐.
- 막대한 학습 규모(H100 약 1만 장); 가중치 수준의 "오픈"일 뿐 데이터 수준에서 재현
  불가능.
- 플랫폼의 폭(토크나이저/디퓨전/AR/가드레일)이 단일 목적 월드모델과의 엄밀한 비교를
  어렵게 한다.

### 영향과 후속 연구

**월드모델은 physical AI의 인프라**라는 가장 분명한 산업적 베팅: [[gr00t-n1|GR00T]]급
VLA를 위한 합성 데이터, 폐루프 정책 평가, Cosmos-Reason/Transfer 후속들. 데이터가 귀한
도메인 — 건설 현장 포함 — 에서 "월드모델을 사전학습하고 내 도메인으로 사후학습"하는 이
패턴이 주시해야 할 방향이다.

**그 뒤의 계열.**

- **Cosmos-Transfer1**(2025년 3월): 분할·깊이·윤곽 지도로 제어하는 세계 생성으로, 화면의 곳마다 가중치를 적응적으로 둔다. sim-to-real과 주행 데이터 보강을 겨냥한다.
- **Cosmos-Reason1**(2025년 3월, 7B와 56B): 물리 상식을 위한 시각–언어 모델로, 다음 단계 같은 체화된 결정을 긴 사고 사슬을 거쳐 언어로 말한다.
- **Cosmos-Predict2.5**와 **Cosmos-Transfer2.5**(2025년 10월): Predict2.5는 flow 기반으로 텍스트·이미지·비디오→세계 생성을 하나로 묶고, Cosmos-Reason1로 텍스트를 접지하며, 정선된 클립 2억 개로 학습해 2B와 14B로 나왔다. 합성 데이터, 정책 평가, 폐루프 시뮬레이션을 위한 것이다. Transfer2.5는 Transfer1보다 3.5배 작으면서 sim-to-real과 real-to-real 변환을 한다. NVIDIA Open Model License로 공개했다.
- **Cosmos-Reason2-2B** 모델이 [[gr00t-n1|GR00T N1.7]]의 시각–언어 백본이다.

[[03-deep-learning/world-models/index|5. 월드모델 §6]]의 말로 하면, Predict와 Transfer는 플래너를 먹이려고 만든 렌더러이고, Reason은 플래너의 일부가 되었다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "world foundation model platform"은 플랫폼(재사용 가능한 인프라) 주장이지 물리 시뮬레이션의 정확성 달성 주장이 아니다 — 물리 벤치마크는 아직 근사 수준임을 논문도 인정한다. "무엇이 됐다"보다 "무엇을 지으려는가"의 선언으로 읽어라.

### 연결

- 이전: [[sora|Sora]] (명제), [[genie|Genie]] (상호작용성), [[ddpm|DDPM]]/[[gpt-3|GPT]] (두 생성기 계보)
- 다음: GR00T 데이터 파이프라인, Cosmos-Reason/Transfer · 도메인 연결: [[05-construction-robotics/index|건설로봇]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] State what "world models as infrastructure" means — what a pretrained WFM is post-trained into · "월드모델을 인프라로"의 의미, 즉 사전학습된 WFM을 사후학습해 무엇으로 만드는가를 말할 수 있다
- [ ] State the difference between diffusion-family and autoregressive-family WFMs · 디퓨전 계열과 자기회귀 계열 WFM의 차이를 말할 수 있다
- [ ] Explain where the sim-to-real problem *moves to* when synthetic data is used · 합성 데이터를 쓸 때 sim-to-real 문제가 어디로 이동하는지 설명할 수 있다
- [ ] Name the layer Cosmos occupies in the GR00T ecosystem · GR00T 생태계에서 Cosmos가 맡는 층을 말할 수 있다
