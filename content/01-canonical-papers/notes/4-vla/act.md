---
title: "ACT / ALOHA — Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware"
authors: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn
affiliation: Stanford University, UC Berkeley, Meta
venue: RSS
year: 2023
arxiv: https://arxiv.org/abs/2304.13705
pdf: https://arxiv.org/pdf/2304.13705
code: https://github.com/tonyzhaozh/act
project: https://tonyzhaozh.github.io/aloha/
tags: [paper, vla, robot-learning]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Zhao et al., RSS 2023** — [arXiv](https://arxiv.org/abs/2304.13705) · [PDF](https://arxiv.org/pdf/2304.13705) · [Code](https://github.com/tonyzhaozh/act) · [Official](https://tonyzhaozh.github.io/aloha/)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] plus [[02-foundations/rl-basics|7. RL Basics §6]], which names the failure ACT is built against: behaviour cloning's **compounding error**. Chunking trades reactivity for fewer decision points — and [[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]] is the classical machinery a chunk replaces.
> [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]와 [[02-foundations/rl-basics|7. RL 기초 §6]] — ACT가 맞서 만들어진 실패를 그 절이 이름 짓는다: 행동 복제의 **복합 오차**. 청킹은 반응성을 내주고 결정 지점 수를 줄이는 거래이며, 청크가 대체하는 고전 기계장치는 [[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]이다.

## English

**One-line summary**: A low-cost open-source bimanual teleoperation rig (ALOHA — the paper's §III states a 20k USD budget; the abstract gives no price) plus Action Chunking with Transformers (ACT) — predict 100 actions at once with a CVAE — makes precise two-handed manipulation learnable from just 50 demonstrations.

### Context

Fine manipulation (threading a zip tie, opening a ziploc, slotting a battery) was assumed to
need expensive robots and force sensing. And single-step behavior cloning fails at precision
tasks for a structural reason: **compounding error** — each small mistake shifts the state
off-distribution, and errors accumulate over hundreds of decisions. Both the hardware cost
and the algorithmic fragility needed fixing at once.

### Method

> [!tip] Key intuition
> Cut the number of decisions: predict a *chunk* of the next 100 actions in one shot, and
> the horizon over which errors compound shrinks 100×. Handle the stylistic variability of
> human demos with a CVAE latent, and smooth chunk boundaries by averaging overlapping
> predictions (temporal ensembling). **Note what chunking does and does not change**: ACT
> explicitly does *not* run open-loop inside a chunk — the paper queries the policy at every
> timestep and ensembles the overlapping predictions, precisely to avoid the jerky motion a
> once-per-k-steps observation would cause. What chunking shortens is the horizon over which
> errors compound, not the observation rate.

- **ALOHA hardware**: two leader arms puppeteer two follower arms (joint-space mapping),
  4 cameras, open-source, built to a stated 20k USD budget (§III, not the abstract) — high-quality bimanual demos at 50 Hz become easy to collect.
- **ACT**: a CVAE whose decoder is a Transformer — conditioned on images + joint positions
  (+ a latent style variable $z$), it outputs the next $k{=}100$ joint-space actions.

<svg viewBox="0 0 620 226" style="max-width:100%;height:auto" role="img" aria-label="single-step prediction versus action chunking, drawn on the same timeline">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="60" y1="61" x2="540" y2="61"/><line x1="60" y1="56" x2="60" y2="66"/><line x1="84" y1="56" x2="84" y2="66"/><line x1="108" y1="56" x2="108" y2="66"/><line x1="132" y1="56" x2="132" y2="66"/><line x1="156" y1="56" x2="156" y2="66"/><line x1="180" y1="56" x2="180" y2="66"/><line x1="204" y1="56" x2="204" y2="66"/><line x1="228" y1="56" x2="228" y2="66"/><line x1="252" y1="56" x2="252" y2="66"/><line x1="276" y1="56" x2="276" y2="66"/><line x1="300" y1="56" x2="300" y2="66"/><line x1="324" y1="56" x2="324" y2="66"/><line x1="348" y1="56" x2="348" y2="66"/><line x1="372" y1="56" x2="372" y2="66"/><line x1="396" y1="56" x2="396" y2="66"/><line x1="420" y1="56" x2="420" y2="66"/><line x1="444" y1="56" x2="444" y2="66"/><line x1="468" y1="56" x2="468" y2="66"/><line x1="492" y1="56" x2="492" y2="66"/><line x1="516" y1="56" x2="516" y2="66"/><line x1="540" y1="56" x2="540" y2="66"/></g>
  <g fill="currentColor" opacity="0.85"><circle cx="60" cy="50" r="3"/><circle cx="84" cy="50" r="3"/><circle cx="108" cy="50" r="3"/><circle cx="132" cy="50" r="3"/><circle cx="156" cy="50" r="3"/><circle cx="180" cy="50" r="3"/><circle cx="204" cy="50" r="3"/><circle cx="228" cy="50" r="3"/><circle cx="252" cy="50" r="3"/><circle cx="276" cy="50" r="3"/><circle cx="300" cy="50" r="3"/><circle cx="324" cy="50" r="3"/><circle cx="348" cy="50" r="3"/><circle cx="372" cy="50" r="3"/><circle cx="396" cy="50" r="3"/><circle cx="420" cy="50" r="3"/><circle cx="444" cy="50" r="3"/><circle cx="468" cy="50" r="3"/><circle cx="492" cy="50" r="3"/><circle cx="516" cy="50" r="3"/><circle cx="540" cy="50" r="3"/></g>
  <rect x="60" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/><rect x="180" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/><rect x="300" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/><rect x="420" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="60" y1="141" x2="540" y2="141"/><line x1="60" y1="136" x2="60" y2="146"/><line x1="84" y1="136" x2="84" y2="146"/><line x1="108" y1="136" x2="108" y2="146"/><line x1="132" y1="136" x2="132" y2="146"/><line x1="156" y1="136" x2="156" y2="146"/><line x1="180" y1="136" x2="180" y2="146"/><line x1="204" y1="136" x2="204" y2="146"/><line x1="228" y1="136" x2="228" y2="146"/><line x1="252" y1="136" x2="252" y2="146"/><line x1="276" y1="136" x2="276" y2="146"/><line x1="300" y1="136" x2="300" y2="146"/><line x1="324" y1="136" x2="324" y2="146"/><line x1="348" y1="136" x2="348" y2="146"/><line x1="372" y1="136" x2="372" y2="146"/><line x1="396" y1="136" x2="396" y2="146"/><line x1="420" y1="136" x2="420" y2="146"/><line x1="444" y1="136" x2="444" y2="146"/><line x1="468" y1="136" x2="468" y2="146"/><line x1="492" y1="136" x2="492" y2="146"/><line x1="516" y1="136" x2="516" y2="146"/><line x1="540" y1="136" x2="540" y2="146"/></g>
  <g fill="currentColor" opacity="0.85"><circle cx="60" cy="130" r="4"/><circle cx="180" cy="130" r="4"/><circle cx="300" cy="130" r="4"/><circle cx="420" cy="130" r="4"/><circle cx="540" cy="130" r="4"/></g>
  <g font-size="11" fill="currentColor">
    <text x="60" y="32">single-step policy &#8212; one decision every tick</text>
    <text x="60" y="106">action chunking &#8212; one decision per chunk</text>
    <text x="60" y="88" font-size="10.5" opacity="0.85">21 decisions across the window; each one can drift a little further from the demonstrated states</text>
    <text x="60" y="166" font-size="10.5" opacity="0.85">5 decisions - but ACT still queries every timestep and ensembles overlapping chunks</text>
    <text x="30" y="186" opacity="0.9">Chunking does not make each prediction better &#8212; it makes fewer of them,</text>
    <text x="30" y="200" opacity="0.9">so compounding error has fewer chances to accumulate.</text>
    <text x="30" y="216" opacity="0.9">What it spends is reactivity: nothing that happens mid-chunk can change the plan until the next decision.</text>
  </g>
</svg>

- **Temporal ensembling**: at each timestep, average all previously predicted actions for
  that step — smooth control without re-planning jitter.
- Trained per task from ~50 human demos (~10 minutes of data); runs on a single GPU.

### Results

- **80–90% success** on real fine-manipulation tasks (slot a battery, open a translucent cup
  lid, ziploc opening) from 50 demos — tasks where prior imitation baselines score near zero.
- Ablations: chunking is the decisive ingredient; the CVAE and ensembling each add measurably.
- Democratized data collection: the ALOHA design was adopted far beyond the paper.

### Limitations & critique

- Per-task policies with no language conditioning — a specialist, not a generalist
  (later merged into VLAs: chunked action heads are now standard in π0/GR00T-class models).
- Fixed chunk size trades reactivity for stability; ensembling can blur genuinely multimodal
  choices that [[diffusion-policy|Diffusion Policy]] represents explicitly.
- Joint-space cloning ties policies to the specific embodiment.

### Impact & follow-ups

Twin legacies: (1) **action chunking** became a core VLA design element; (2) **ALOHA** became
the field's data-collection workhorse — Mobile ALOHA, ALOHA 2, and the bimanual datasets
behind π0/GR00T-era training all trace here. With [[diffusion-policy|Diffusion Policy]], it
defined how modern policies output actions.

> [!question] Reading the claim · 핵심 주장 읽는 법
> The scope of "fine manipulation with low-cost hardware" is per-task specialist policies (~50 demonstrations each) — it is not a generality claim. And this paper actually contains two contributions (the ALOHA hardware and the ACT algorithm) — read it while asking what share of the success belongs to each.

### Connections

- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets §11]] — how to read the success rates in this paper's tables: trials, initial-state distribution, seen/unseen split, and whose evaluation it is
- [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection]] — the interface spectrum this sits at one end of, and what its data does and does not contain
- Parallel: [[diffusion-policy|Diffusion Policy]] (generative chunking) · Previous: [[vae|VAE]] (the CVAE machinery)
- Next: Mobile ALOHA, Octo, π0
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 저비용 오픈소스 양팔 원격조작 장비(ALOHA — 논문 §III가 밝힌 예산은 2만 달러, 초록에는 가격이 없다)와 Action Chunking with Transformers(ACT) — CVAE로 100개 행동을 한 번에 예측 — 로 시연 50개만으로 정밀한 양손 조작을 학습 가능하게 만들었다.

### 배경

정밀 조작(케이블 타이 끼우기, 지퍼백 열기, 배터리 슬롯 넣기)은 비싼 로봇과 힘 센서가
필요하다고 여겨졌다. 그리고 단일 스텝 행동 복제는 구조적 이유로 정밀 과제에 실패한다:
**복합 오차** — 작은 실수마다 상태가 분포 밖으로 밀려나고, 수백 번의 결정에 걸쳐 오차가
누적된다. 하드웨어 비용과 알고리즘 취약성을 동시에 고쳐야 했다.

### 방법

> [!tip] 핵심 직관
> 결정의 횟수를 줄여라: 다음 100개 행동의 *청크*를 한 번에 예측하면 오차가 누적되는
> 지평이 100배 줄어든다. 인간 시연의 스타일 변동성은 CVAE 잠재변수로 다루고, 청크
> 경계는 겹치는 예측들의 평균(temporal ensembling)으로 매끄럽게 만든다.

- **ALOHA 하드웨어**: 리더 팔 두 개로 팔로워 팔 두 개를 인형처럼 조종(관절 공간 매핑),
  카메라 4대, 오픈소스, 논문 §III가 밝힌 2만 달러 예산(초록에는 가격이 없다) — 50 Hz 고품질 양팔 시연 수집이 쉬워진다.
- **ACT**: 디코더가 Transformer인 CVAE — 이미지 + 관절 위치(+ 스타일 잠재변수 $z$)를
  조건으로 다음 $k{=}100$개의 관절 공간 행동을 출력.

<svg viewBox="0 0 620 214" style="max-width:100%;height:auto" role="img" aria-label="단일 스텝 예측과 행동 청킹을 같은 타임라인 위에 그린 것">
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="60" y1="61" x2="540" y2="61"/><line x1="60" y1="56" x2="60" y2="66"/><line x1="84" y1="56" x2="84" y2="66"/><line x1="108" y1="56" x2="108" y2="66"/><line x1="132" y1="56" x2="132" y2="66"/><line x1="156" y1="56" x2="156" y2="66"/><line x1="180" y1="56" x2="180" y2="66"/><line x1="204" y1="56" x2="204" y2="66"/><line x1="228" y1="56" x2="228" y2="66"/><line x1="252" y1="56" x2="252" y2="66"/><line x1="276" y1="56" x2="276" y2="66"/><line x1="300" y1="56" x2="300" y2="66"/><line x1="324" y1="56" x2="324" y2="66"/><line x1="348" y1="56" x2="348" y2="66"/><line x1="372" y1="56" x2="372" y2="66"/><line x1="396" y1="56" x2="396" y2="66"/><line x1="420" y1="56" x2="420" y2="66"/><line x1="444" y1="56" x2="444" y2="66"/><line x1="468" y1="56" x2="468" y2="66"/><line x1="492" y1="56" x2="492" y2="66"/><line x1="516" y1="56" x2="516" y2="66"/><line x1="540" y1="56" x2="540" y2="66"/></g>
  <g fill="currentColor" opacity="0.85"><circle cx="60" cy="50" r="3"/><circle cx="84" cy="50" r="3"/><circle cx="108" cy="50" r="3"/><circle cx="132" cy="50" r="3"/><circle cx="156" cy="50" r="3"/><circle cx="180" cy="50" r="3"/><circle cx="204" cy="50" r="3"/><circle cx="228" cy="50" r="3"/><circle cx="252" cy="50" r="3"/><circle cx="276" cy="50" r="3"/><circle cx="300" cy="50" r="3"/><circle cx="324" cy="50" r="3"/><circle cx="348" cy="50" r="3"/><circle cx="372" cy="50" r="3"/><circle cx="396" cy="50" r="3"/><circle cx="420" cy="50" r="3"/><circle cx="444" cy="50" r="3"/><circle cx="468" cy="50" r="3"/><circle cx="492" cy="50" r="3"/><circle cx="516" cy="50" r="3"/><circle cx="540" cy="50" r="3"/></g>
  <rect x="60" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/><rect x="180" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/><rect x="300" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/><rect x="420" y="120" width="112" height="20" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.9"/>
  <g stroke="currentColor" stroke-width="1" opacity="0.4"><line x1="60" y1="141" x2="540" y2="141"/><line x1="60" y1="136" x2="60" y2="146"/><line x1="84" y1="136" x2="84" y2="146"/><line x1="108" y1="136" x2="108" y2="146"/><line x1="132" y1="136" x2="132" y2="146"/><line x1="156" y1="136" x2="156" y2="146"/><line x1="180" y1="136" x2="180" y2="146"/><line x1="204" y1="136" x2="204" y2="146"/><line x1="228" y1="136" x2="228" y2="146"/><line x1="252" y1="136" x2="252" y2="146"/><line x1="276" y1="136" x2="276" y2="146"/><line x1="300" y1="136" x2="300" y2="146"/><line x1="324" y1="136" x2="324" y2="146"/><line x1="348" y1="136" x2="348" y2="146"/><line x1="372" y1="136" x2="372" y2="146"/><line x1="396" y1="136" x2="396" y2="146"/><line x1="420" y1="136" x2="420" y2="146"/><line x1="444" y1="136" x2="444" y2="146"/><line x1="468" y1="136" x2="468" y2="146"/><line x1="492" y1="136" x2="492" y2="146"/><line x1="516" y1="136" x2="516" y2="146"/><line x1="540" y1="136" x2="540" y2="146"/></g>
  <g fill="currentColor" opacity="0.85"><circle cx="60" cy="130" r="4"/><circle cx="180" cy="130" r="4"/><circle cx="300" cy="130" r="4"/><circle cx="420" cy="130" r="4"/><circle cx="540" cy="130" r="4"/></g>
  <g font-size="11" fill="currentColor">
    <text x="60" y="32">단일 스텝 정책 &#8212; 매 틱마다 결정 하나</text>
    <text x="60" y="106">행동 청킹 &#8212; 청크당 결정 하나</text>
    <text x="60" y="88" font-size="10.5" opacity="0.85">이 구간에서 결정 21번; 하나하나가 시연된 상태에서 조금씩 더 벗어날 수 있다</text>
    <text x="60" y="166" font-size="10.5" opacity="0.85">결정 5번 - 다만 ACT는 매 스텝 질의하고 겹치는 청크를 앙상블한다</text>
    <text x="30" y="192" opacity="0.9">청킹은 예측 하나하나를 더 좋게 만들지 않는다 &#8212; 예측 횟수를 줄여서 복합 오차가 쌓일 기회를 줄인다.</text>
    <text x="30" y="207" opacity="0.9">그 대가로 내주는 것은 반응성이다: 청크 도중에 일어난 일은 다음 결정 지점까지 계획을 바꿀 수 없다.</text>
  </g>
</svg>

- **Temporal ensembling**: 각 시점에 대해 이전에 예측된 모든 행동을 평균 —
  재계획 떨림 없는 부드러운 제어.
- 과제당 인간 시연 약 50개(약 10분 분량)로 학습; GPU 한 장에서 구동.

### 결과

- 실제 정밀 조작 과제(배터리 슬롯, 반투명 컵 뚜껑, 지퍼백)에서 시연 50개로 **80~90% 성공**
  — 기존 모방학습 베이스라인이 0에 가까운 과제들이다.
- 절제 실험: 결정적 재료는 청킹; CVAE와 ensembling도 각각 측정 가능한 기여.
- 데이터 수집의 민주화: ALOHA 설계는 논문을 훨씬 넘어 채택됐다.

### 한계와 비판

- 언어 조건 없는 과제별 정책 — 범용이 아닌 전문가 (이후 VLA에 흡수: 청크 행동 헤드는
  이제 π0/GR00T급 모델의 표준이다).
- 고정 청크 크기는 반응성을 안정성과 맞바꾼다; ensembling은 [[diffusion-policy|Diffusion Policy]]가 명시적으로 표현하는 진짜 다봉적 선택지를 뭉갤 수 있다.
- 관절 공간 복제는 정책을 특정 로봇 형태에 묶는다.

### 영향과 후속 연구

두 갈래 유산: (1) **행동 청킹**은 VLA의 핵심 설계 요소가 됐다; (2) **ALOHA**는 분야의
데이터 수집 주력 장비가 됐다 — Mobile ALOHA, ALOHA 2, 그리고 π0/GR00T 시대 학습의
양팔 데이터셋들이 모두 여기서 나온다. [[diffusion-policy|Diffusion Policy]]와 함께
현대 정책이 행동을 출력하는 방식을 정의했다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "fine manipulation with low-cost hardware"의 범위는 과제별 전문 정책(과제당 시연 ~50개)이다 — 범용성 주장이 아니다. 그리고 이 논문은 사실 두 개의 기여(ALOHA 하드웨어, ACT 알고리즘)를 담고 있다 — 성공의 몇 %가 어느 쪽 덕인지 분리해 생각하며 읽어라.

### 연결

- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋 §11]] — 이 논문 표의 성공률을 읽는 법: 시행 횟수, 초기 상태 분포, seen/unseen 분할, 그리고 누구의 평가인가
- [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]] — 이것이 한쪽 끝에 놓이는 인터페이스 스펙트럼, 그리고 그 데이터에 무엇이 있고 없는지
- 병행: [[diffusion-policy|Diffusion Policy]] (생성형 청킹) · 이전: [[vae|VAE]] (CVAE 기계장치)
- 다음: Mobile ALOHA, Octo, π0
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain why compounding error arises and how 100-step chunking reduces it · 복합 오차가 왜 생기고, 100-스텝 청킹이 그것을 어떻게 줄이는지 설명할 수 있다
- [ ] Say what the CVAE latent $z$ absorbs from the demonstrations (stylistic variation) · CVAE 잠재변수 $z$가 시연의 무엇(스타일 변동)을 흡수하는지 말할 수 있다
- [ ] Say what temporal ensembling averages and what side effect it has (blurring genuinely multimodal choices) · temporal ensembling이 무엇을 평균하고, 어떤 부작용(다봉 선택지의 뭉개짐)이 있는지 말할 수 있다
- [ ] Explain why the ALOHA hardware is as important a contribution as the method · ALOHA 하드웨어가 방법론만큼 중요한 기여인 이유를 말할 수 있다
