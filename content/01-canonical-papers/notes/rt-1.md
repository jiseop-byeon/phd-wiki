---
title: "RT-1 — Robotics Transformer for Real-World Control at Scale"
authors: Anthony Brohan, Noah Brown, Justice Carbajal, et al.
affiliation: Google (Robotics at Google, Everyday Robots)
venue: RSS
year: 2023
arxiv: https://arxiv.org/abs/2212.06817
pdf: https://arxiv.org/pdf/2212.06817
code: https://github.com/google-research/robotics_transformer
project: https://robotics-transformer1.github.io
tags: [paper, vla, robot-learning]
status: to-read
---

**Brohan et al., RSS 2023** — [arXiv](https://arxiv.org/abs/2212.06817) · [PDF](https://arxiv.org/pdf/2212.06817) · [Code](https://github.com/google-research/robotics_transformer) · [Official](https://robotics-transformer1.github.io)

## English

**One-line summary**: The GPT bet applied to robots — one Transformer, 130k real teleoperation episodes across 700+ tasks, actions as discrete tokens — showing that scale and diversity of *robot data* produce a single generalist policy.

### Context

Robot learning circa 2022 was one-model-per-task: a policy trained on hundreds of demos of
a single skill, brittle to any distribution shift. Meanwhile [[gpt-3|NLP]] and
[[clip|vision]] had shown that big Transformers + diverse data yield generalists. The open
question: does that recipe survive contact with the physical world, where data is
expensive, slow, and closed-loop at real-time rates?

### Method

> [!tip] Key intuition
> Treat manipulation as sequence modeling: images and an instruction in, discretized action
> tokens out. If the model and data are diverse enough, new instructions become
> recombinations of seen skills — generalization by interpolation in task space.

- **Data**: 130k episodes, 13 mobile manipulators, 17 months, 700+ language-labeled kitchen
  tasks (pick/place/open/close/drawer operations).
- **Architecture**: EfficientNet-B3 conditioned on the instruction embedding via **FiLM**
  layers → **TokenLearner** compresses to 8 visual tokens → decoder-only Transformer (35M
  params — small, for 3 Hz real-time control).
- **Actions as tokens**: 11 dimensions (7 arm, 3 base, 1 mode switch), each discretized to
  256 bins — control becomes next-token classification.
- Absorbs heterogeneous data: adding simulation data and even another robot's (Kuka) data
  improves the corresponding skills without hurting the rest.

### Results

- **97%** success on seen instructions; **76%** on never-seen instructions; **83%/59%**
  robustness to distractors/new backgrounds — all far above prior imitation baselines (e.g., Gato, BC-Z).
- Performance scales with data *diversity* more than data quantity — the paper's most
  consequential ablation.
- Executes SayCan-style long-horizon sequences (up to 50 steps) as the low-level policy.

### Limitations & critique

- Imitation-only: capped at demonstrator quality; no recovery behaviors beyond what data contains.
- Vision module is task-trained, not web-pretrained — semantic knowledge is limited to the
  700 tasks (exactly the gap [[rt-2|RT-2]] closes with VLM pretraining).
- Discretized independent action dims can't represent multimodal trajectories well
  (the gap [[diffusion-policy|Diffusion Policy]] targets).
- Single embodiment class, kitchen domain; 3 Hz is slow for dynamic tasks.

### Impact & follow-ups

Proved robot-side scaling works and defined the VLA data flywheel. Direct line to
[[rt-2|RT-2]] (swap the from-scratch backbone for a VLM) and Open X-Embodiment/RT-X
(cross-robot data pooling). Its action-tokenization scheme persists in OpenVLA and beyond.

### Connections

- Previous: [[attention-is-all-you-need|Transformer]], BC-Z · Next: [[rt-2|RT-2]], [[diffusion-policy|Diffusion Policy]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: GPT의 베팅을 로봇에 적용 — Transformer 하나, 700개+ 과제에 걸친 13만 실제 원격조작 에피소드, 행동의 이산 토큰화 — *로봇 데이터*의 규모와 다양성이 단일 범용 정책을 만든다는 것을 보였다.

### 배경

2022년경의 로봇 학습은 과제당 모델 하나였다: 한 가지 기술의 시연 수백 개로 학습된 정책은
어떤 분포 이동에도 취약했다. 한편 [[gpt-3|NLP]]와 [[clip|비전]]은 큰 Transformer + 다양한
데이터가 범용 모델을 만든다는 것을 보여준 상태였다. 열린 질문: 그 레시피가 물리 세계 —
데이터가 비싸고 느리며 실시간 폐루프인 곳 — 와의 접촉에서도 살아남는가?

### 방법

> [!tip] 핵심 직관
> 매니퓰레이션을 시퀀스 모델링으로 취급하라: 이미지와 지시가 들어가고, 이산화된 행동
> 토큰이 나온다. 모델과 데이터가 충분히 다양하면 새로운 지시는 본 적 있는 기술들의
> 재조합이 된다 — 과제 공간에서의 보간에 의한 일반화.

- **데이터**: 13만 에피소드, 모바일 매니퓰레이터 13대, 17개월, 언어 라벨이 달린 주방 과제
  700개+ (집기/놓기/열기/닫기/서랍 조작).
- **구조**: 지시 임베딩을 **FiLM** 층으로 조건화한 EfficientNet-B3 → **TokenLearner**가
  시각 토큰 8개로 압축 → 디코더 전용 Transformer (3500만 파라미터 — 3 Hz 실시간 제어를
  위해 의도적으로 작게).
- **행동의 토큰화**: 11차원(팔 7, 베이스 3, 모드 1)을 각각 256 구간으로 이산화 —
  제어가 다음 토큰 분류 문제가 된다.
- 이질적 데이터 흡수: 시뮬레이션 데이터와 심지어 다른 로봇(Kuka)의 데이터를 더하면
  해당 기술이 좋아지고 나머지는 다치지 않는다.

### 결과

- 본 지시 **97%** 성공; 처음 보는 지시 **76%**; 방해물/새 배경에 대한 강건성 **83%/59%** —
  기존 모방학습 베이스라인(Gato, BC-Z)을 큰 폭으로 상회.
- 성능은 데이터 양보다 데이터 *다양성*에 따라 스케일 — 이 논문에서 가장 파급력 있는 절제 실험.
- SayCan식 장기 시퀀스(최대 50 스텝)의 하위 정책으로 작동.

### 한계와 비판

- 순수 모방학습: 시연자 품질이 상한; 데이터에 없는 회복 행동은 없다.
- 비전 모듈이 과제 데이터로만 학습됨 — 의미 지식이 700개 과제에 갇혀 있다
  (정확히 [[rt-2|RT-2]]가 VLM 사전학습으로 메우는 간극).
- 차원별 독립 이산화는 다봉(multimodal) 궤적을 잘 표현하지 못한다
  ([[diffusion-policy|Diffusion Policy]]가 겨냥한 간극).
- 단일 로봇 계열, 주방 도메인; 3 Hz는 동적 과제에 느리다.

### 영향과 후속 연구

로봇 쪽 스케일링이 작동함을 증명하고 VLA 데이터 플라이휠을 정의했다. [[rt-2|RT-2]]
(백본을 VLM으로 교체)와 Open X-Embodiment/RT-X(로봇 간 데이터 풀링)로 직결. 행동
토큰화 방식은 OpenVLA 등에 그대로 이어진다.

### 연결

- 이전: [[attention-is-all-you-need|Transformer]], BC-Z · 다음: [[rt-2|RT-2]], [[diffusion-policy|Diffusion Policy]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]
