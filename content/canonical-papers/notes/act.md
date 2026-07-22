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
status: to-read
---

**Zhao et al., RSS 2023** — [arXiv](https://arxiv.org/abs/2304.13705) · [PDF](https://arxiv.org/pdf/2304.13705) · [Code](https://github.com/tonyzhaozh/act) · [Official](https://tonyzhaozh.github.io/aloha/)

## English

**One-line summary**: A $20k open-source bimanual teleoperation rig (ALOHA) plus Action Chunking with Transformers (ACT) — predict 100 actions at once with a CVAE — makes precise two-handed manipulation learnable from just 50 demonstrations.

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
> predictions (temporal ensembling).

- **ALOHA hardware**: two leader arms puppeteer two follower arms (joint-space mapping),
  4 cameras, ~$20k, open-source — high-quality bimanual demos at 50 Hz become easy to collect.
- **ACT**: a CVAE whose decoder is a Transformer — conditioned on images + joint positions
  (+ a latent style variable $z$), it outputs the next $k{=}100$ joint-space actions.
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

### Connections

- Parallel: [[diffusion-policy|Diffusion Policy]] (generative chunking) · Previous: [[vae|VAE]] (the CVAE machinery)
- Next: Mobile ALOHA, Octo, π0
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 2천만 원대 오픈소스 양팔 원격조작 장비(ALOHA)와 Action Chunking with Transformers(ACT) — CVAE로 100개 행동을 한 번에 예측 — 로 시연 50개만으로 정밀한 양손 조작을 학습 가능하게 만들었다.

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
  카메라 4대, 약 $20k, 오픈소스 — 50 Hz 고품질 양팔 시연 수집이 쉬워진다.
- **ACT**: 디코더가 Transformer인 CVAE — 이미지 + 관절 위치(+ 스타일 잠재변수 $z$)를
  조건으로 다음 $k{=}100$개의 관절 공간 행동을 출력.
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
- 고정 청크 크기는 반응성을 안정성과 맞바꾼다; ensembling은 [[diffusion-policy|Diffusion
  Policy]]가 명시적으로 표현하는 진짜 다봉적 선택지를 뭉갤 수 있다.
- 관절 공간 복제는 정책을 특정 로봇 형태에 묶는다.

### 영향과 후속 연구

두 갈래 유산: (1) **행동 청킹**은 VLA의 핵심 설계 요소가 됐다; (2) **ALOHA**는 분야의
데이터 수집 주력 장비가 됐다 — Mobile ALOHA, ALOHA 2, 그리고 π0/GR00T 시대 학습의
양팔 데이터셋들이 모두 여기서 나온다. [[diffusion-policy|Diffusion Policy]]와 함께
현대 정책이 행동을 출력하는 방식을 정의했다.

### 연결

- 병행: [[diffusion-policy|Diffusion Policy]] (생성형 청킹) · 이전: [[vae|VAE]] (CVAE 기계장치)
- 다음: Mobile ALOHA, Octo, π0
- 계보: [[10-deep-learning/lineage|논문 계보도]]
